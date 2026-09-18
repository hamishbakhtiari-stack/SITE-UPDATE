#!/usr/bin/env python3
"""Key-by-key diff of two Shopify template JSON files.

Text-diffing a 39KB template is useless — one changed setting looks the same as a
mangled custom_liquid blob. This flattens both documents to leaf paths so you can
say exactly how many keys changed and which ones, before you push.

Handles the auto-generated banner comment Shopify prepends on read.

Usage:
    python3 diff_template.py live.json candidate.json
    python3 diff_template.py live.json candidate.json --full   # don't truncate long values

Exit code is 0 always — this is a reporting tool, not a gate. Use check_template.py
as the gate.
"""
import json
import re
import sys


def load(path):
    """Parse a template JSON, stripping Shopify's auto-generated banner if present."""
    with open(path, encoding='utf-8') as fh:
        raw = fh.read()
    # Shopify prepends a /* ... */ banner on read but not on write (~363 bytes).
    stripped = re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S)
    return json.loads(stripped)


def flatten(obj, prefix=''):
    """Yield (path, leaf_value) for every leaf in a nested structure."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from flatten(value, f'{prefix}/{key}')
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from flatten(value, f'{prefix}/{index}')
    else:
        yield prefix, obj


MISSING = '<absent>'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    full = '--full' in sys.argv
    if len(args) != 2:
        print(__doc__)
        return 0

    before, after = load(args[0]), load(args[1])
    flat_before, flat_after = dict(flatten(before)), dict(flatten(after))

    print(f'keys {len(flat_before)} -> {len(flat_after)}')

    changed = 0
    for path in sorted(set(flat_before) | set(flat_after)):
        old, new = flat_before.get(path, MISSING), flat_after.get(path, MISSING)
        if old == new:
            continue
        changed += 1
        # Dense custom_liquid / custom_css blobs are unreadable inline — summarise by delta.
        dense = ('custom_liquid' in path or 'custom_css' in path) and not full
        if dense and isinstance(old, str) and isinstance(new, str):
            print(f'DIFF {path}  ({len(new) - len(old):+d} chars)')
        else:
            limit = None if full else 160
            print(f'DIFF {path}\n  - {trim(old, limit)}\n  + {trim(new, limit)}')

    print(f'total diffs {changed}')

    # Order changes silently reshuffle the page, so call them out separately.
    for label, getter in (
        ('order', lambda d: d.get('order')),
        ('main.block_order', lambda d: d.get('sections', {}).get('main', {}).get('block_order')),
    ):
        same = getter(before) == getter(after)
        print(f'{label} unchanged: {same}' + ('' if same else '   <-- CHECK THIS'))

    return 0


def trim(value, limit):
    text = repr(value)
    if limit and len(text) > limit:
        return text[:limit] + f'... ({len(text)} chars)'
    return text


if __name__ == '__main__':
    sys.exit(main())
