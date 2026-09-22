#!/usr/bin/env python3
"""Section 4 (7days): already identical to ComfortBundle (both use sitewide settings).
Only change: page-only lock note, so it doesn't say the Reset comes with the ComfortBundle
on a page whose hero and Reset tab say it comes with ErgoRelief.
Requires sections/7days.liquid with the lock_text_override setting (opt-in, blank elsewhere)."""
import json, re
BASE = 'baseline/product.ergoRelief.after-s3b.json'
OUT = 'candidate/product.ergoRelief.json'
er = json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(BASE, encoding='utf-8').read(), count=1, flags=re.S))
er['sections']['7days_P3eEBF']['settings']['lock_text_override'] = (
    'Days 4–7 unlock when you start the Reset — included with ErgoRelief™')
dumped = json.dumps(er, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT)
