#!/usr/bin/env python3
"""Work with Shopify theme JSON templates (templates/*.json, sections/*.json).

Shopify prefixes these files with an auto-generated /* ... */ banner that is not
valid JSON, so json.load() fails on a file fetched straight from the Admin API.
Every command here strips the banner to read and restores it to write.

Usage:
  theme_json.py outline  FILE
  theme_json.py validate FILE
  theme_json.py get      FILE PATH
  theme_json.py set      FILE PATH VALUE [--json] [-o OUT | -i]
  theme_json.py diff     BEFORE AFTER

PATH is dot-separated, e.g.
  sections.faq_4TjTJm.settings.heading
  sections.faq_4TjTJm.blocks.faq_JeXq9g.settings.answer

Typical loop:
  1. read the file body from the Admin API, save it as page.x.before.json
  2. outline it, find the setting to change
  3. set ... -o page.x.after.json
  4. diff page.x.before.json page.x.after.json   # confirm the change is minimal
  5. validate page.x.after.json
  6. themeFilesUpsert the full contents of page.x.after.json
"""

import argparse
import json
import re
import sys

BANNER_RE = re.compile(r"\A\s*/\*.*?\*/\s*", re.DOTALL)

# Settings most likely to hold visible copy, shown first in `outline`.
COPY_KEYS = (
    "heading", "title", "subheading", "subtitle", "text", "question",
    "answer", "label", "button_text", "caption", "content", "name",
)


def load(path):
    """Return (banner, data). banner is '' when the file has none."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    match = BANNER_RE.match(raw)
    banner = match.group(0) if match else ""
    body = raw[len(banner):] if banner else raw
    try:
        return banner, json.loads(body)
    except json.JSONDecodeError as exc:
        sys.exit(f"{path}: invalid JSON after banner strip: {exc} "
                 "(line/column are relative to the JSON body, banner excluded)")


def dump(path, banner, data):
    text = banner + json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if path == "-":
        sys.stdout.write(text)
    else:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)


def walk(data, path, create=False):
    """Resolve a dot path to (container, final_key)."""
    parts = path.split(".")
    node = data
    for part in parts[:-1]:
        if isinstance(node, dict) and part not in node:
            if not create:
                sys.exit(f"path not found: {path} (missing '{part}')")
            node[part] = {}
        try:
            node = node[part]
        except (KeyError, TypeError, IndexError):
            sys.exit(f"path not found: {path} (missing '{part}')")
    return node, parts[-1]


def flatten(node, prefix=""):
    out = {}
    if isinstance(node, dict):
        for key, value in node.items():
            out.update(flatten(value, f"{prefix}.{key}" if prefix else key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out.update(flatten(value, f"{prefix}[{index}]"))
    else:
        out[prefix] = node
    return out


def cmd_outline(args):
    _, data = load(args.file)
    sections = data.get("sections", {})
    order = data.get("order", list(sections))
    print(f"{args.file}: {len(sections)} section(s), {len(order)} in order\n")
    for position, section_id in enumerate(order, 1):
        section = sections.get(section_id)
        if section is None:
            print(f"{position}. {section_id}  !! in `order` but not in `sections`")
            continue
        flags = " [DISABLED]" if section.get("disabled") else ""
        name = section.get("name")
        label = f' "{name}"' if name else ""
        print(f'{position}. {section_id}  type={section.get("type")!r}{label}{flags}')
        settings = section.get("settings", {})
        for key in COPY_KEYS:
            if settings.get(key):
                print(f"      settings.{key}: {preview(settings[key])}")
        other = [k for k in settings if k not in COPY_KEYS]
        if other:
            print(f'      + {len(other)} other setting(s): {", ".join(sorted(other)[:8])}'
                  + (" …" if len(other) > 8 else ""))
        blocks = section.get("blocks", {})
        if blocks:
            block_order = section.get("block_order", list(blocks))
            print(f"      blocks ({len(blocks)}):")
            for block_id in block_order:
                block = blocks.get(block_id)
                if block is None:
                    print(f"        - {block_id}  !! in `block_order` but not in `blocks`")
                    continue
                first = next(
                    (f"{k}: {preview(block.get('settings', {})[k])}"
                     for k in COPY_KEYS if block.get("settings", {}).get(k)),
                    "",
                )
                print(f'        - {block_id}  type={block.get("type")!r}  {first}')
            orphans = [b for b in blocks if b not in block_order]
            for block_id in orphans:
                print(f"        - {block_id}  !! not in `block_order` (won't render)")
        print()
    strays = [s for s in sections if s not in order]
    for section_id in strays:
        print(f"!! section {section_id} is not in `order` (won't render)")


def preview(value, width=72):
    text = str(value).replace("\n", "\\n")
    return text if len(text) <= width else text[:width] + "…"


def cmd_validate(args):
    banner, data = load(args.file)
    problems = []
    if not banner:
        problems.append("note: no auto-generated banner — fine for a hand-made "
                        "file, but Shopify-fetched templates normally have one")
    sections = data.get("sections")
    if not isinstance(sections, dict):
        sys.exit(f"{args.file}: no `sections` object — is this a theme template?")
    order = data.get("order")
    if not isinstance(order, list):
        problems.append("`order` is missing or not a list")
        order = []
    for section_id in order:
        if section_id not in sections:
            problems.append(f"`order` references unknown section {section_id!r}")
    for section_id in sections:
        if section_id not in order:
            problems.append(f"section {section_id!r} is absent from `order` (won't render)")
    if len(set(order)) != len(order):
        problems.append("`order` contains duplicate IDs")
    for section_id, section in sections.items():
        if not section.get("type"):
            problems.append(f"section {section_id!r} has no `type`")
        blocks = section.get("blocks", {})
        block_order = section.get("block_order")
        if blocks and block_order is None:
            problems.append(f"section {section_id!r} has blocks but no `block_order`")
            block_order = []
        for block_id in block_order or []:
            if block_id not in blocks:
                problems.append(
                    f"section {section_id!r}: `block_order` references unknown block {block_id!r}")
        for block_id in blocks:
            if block_order is not None and block_id not in block_order:
                problems.append(
                    f"section {section_id!r}: block {block_id!r} absent from `block_order`")
    hard = [p for p in problems if not p.startswith("note:")]
    for problem in problems:
        print(("  " if problem.startswith("note:") else "  ERROR: ") + problem)
    if hard:
        print(f"\n{args.file}: {len(hard)} problem(s)")
        return 1
    print(f"{args.file}: OK — {len(sections)} section(s), JSON parses, "
          "order and block_order consistent")
    return 0


def cmd_get(args):
    _, data = load(args.file)
    node, key = walk(data, args.path)
    try:
        value = node[key]
    except (KeyError, TypeError, IndexError):
        sys.exit(f"path not found: {args.path}")
    print(value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False))
    return 0


def cmd_set(args):
    banner, data = load(args.file)
    value = json.loads(args.value) if args.json else args.value
    node, key = walk(data, args.path, create=args.create)
    if not isinstance(node, dict):
        sys.exit(f"cannot set {args.path}: parent is not an object")
    if key not in node and not args.create:
        sys.exit(f"{args.path} does not exist — pass --create to add it "
                 "(check the section's {% schema %} first)")
    node[key] = value
    out = args.file if args.in_place else (args.out or "-")
    dump(out, banner, data)
    if out != "-":
        print(f"wrote {out}", file=sys.stderr)
    return 0


def cmd_diff(args):
    _, before = load(args.before)
    _, after = load(args.after)
    flat_before, flat_after = flatten(before), flatten(after)
    keys = sorted(set(flat_before) | set(flat_after))
    changes = 0
    for key in keys:
        if key not in flat_after:
            print(f"- {key}: {preview(flat_before[key])}")
            changes += 1
        elif key not in flat_before:
            print(f"+ {key}: {preview(flat_after[key])}")
            changes += 1
        elif flat_before[key] != flat_after[key]:
            print(f"~ {key}")
            print(f"    - {preview(flat_before[key])}")
            print(f"    + {preview(flat_after[key])}")
            changes += 1
    print(f"\n{changes} change(s)")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("outline", help="list sections, blocks and copy settings")
    p.add_argument("file")
    p.set_defaults(func=cmd_outline)

    p = sub.add_parser("validate", help="check JSON, order and block_order integrity")
    p.add_argument("file")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("get", help="print one value")
    p.add_argument("file")
    p.add_argument("path")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("set", help="set one value, preserving the banner")
    p.add_argument("file")
    p.add_argument("path")
    p.add_argument("value")
    p.add_argument("--json", action="store_true",
                   help="parse VALUE as JSON instead of a string")
    p.add_argument("--create", action="store_true",
                   help="allow creating a key that doesn't exist yet")
    p.add_argument("-o", "--out", help="write here (default: stdout)")
    p.add_argument("-i", "--in-place", action="store_true")
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("diff", help="structural diff of two templates")
    p.add_argument("before")
    p.add_argument("after")
    p.set_defaults(func=cmd_diff)

    args = parser.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
