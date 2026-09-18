#!/usr/bin/env python3
"""Pre-push guard for a Shopify template JSON.

Some settings on a page are hard-won — a media size that took three rounds to get
right, a custom CSS rule that fixes a specific mobile bug, a block that must stay
first. They are easy to clobber by accident when rewriting a 39KB file, and the
damage is invisible until someone looks at the page.

This asserts those values are still present. Non-zero exit means DO NOT PUSH.

When the owner deliberately changes a guarded value, update locked.json in the same
breath and say so in the decisions log — an unexplained guard edit is how a guard
stops meaning anything.

Usage:
    python3 check_template.py candidate.json [locked.json]

locked.json schema (all sections optional):
{
  "_why": "free text",
  "settings":        { "<dotted.path.into.json>": <expected value> },
  "css_must_contain":        ["substring that must appear in any custom_liquid blob"],
  "block_must_contain":      { "<block id>": ["substring", ...] },
  "first_block":     { "<section key>": "<block id that must be first>" },
  "first_section":   "<section key that must be first in order>"
}
"""
import json
import re
import sys


def load(path):
    with open(path, encoding='utf-8') as fh:
        raw = fh.read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S))


def dig(doc, dotted):
    """Walk a dotted path, treating each segment as a dict key or list index."""
    node = doc
    for part in dotted.split('.'):
        if isinstance(node, list):
            node = node[int(part)]
        else:
            node = node[part]
    return node


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    doc = load(sys.argv[1])
    lock = load(sys.argv[2] if len(sys.argv) > 2 else 'locked.json')
    fails = []

    for path, want in lock.get('settings', {}).items():
        try:
            got = dig(doc, path)
        except (KeyError, IndexError, TypeError):
            fails.append(f'{path}: MISSING (expected {want!r})')
            continue
        if got != want:
            fails.append(f'{path}: {got!r} (expected {want!r})')

    # Concatenate every custom_liquid / custom_css blob and check required fragments.
    blobs = []

    def collect(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ('custom_liquid', 'custom_css'):
                    blobs.append(value if isinstance(value, str) else json.dumps(value))
                collect(value)
        elif isinstance(node, list):
            for value in node:
                collect(value)

    collect(doc)
    haystack = '\n'.join(blobs)
    for fragment in lock.get('css_must_contain', []):
        if fragment not in haystack:
            fails.append(f'custom css/liquid lost: {fragment!r}')

    for block_id, fragments in lock.get('block_must_contain', {}).items():
        found = [b for b in blobs if all(f in b for f in fragments)]
        if not found:
            missing = [f for f in fragments if f not in haystack]
            fails.append(f'block {block_id}: missing {missing!r}')

    for section_key, block_id in lock.get('first_block', {}).items():
        order = doc.get('sections', {}).get(section_key, {}).get('block_order', [])
        if not order or order[0] != block_id:
            fails.append(f'{section_key}.block_order[0] is {order[:1]} (expected {block_id!r})')

    first_section = lock.get('first_section')
    if first_section:
        order = doc.get('order', [])
        if not order or order[0] != first_section:
            fails.append(f'order[0] is {order[:1]} (expected {first_section!r})')

    if fails:
        print('FAIL - do not push')
        for line in fails:
            print('  -', line)
        return 1

    print('PASS - safe to push')
    return 0


if __name__ == '__main__':
    sys.exit(main())
