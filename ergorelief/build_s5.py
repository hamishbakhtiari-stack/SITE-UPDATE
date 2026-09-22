#!/usr/bin/env python3
"""Section 5 (every_day_section_jYJzBQ): disable (not delete), same as ComfortBundle.
Everything in it is repeated elsewhere: hero headline/bullets, section 2, the 'pairs
best with LumbarEase' note (verbatim in single_support), and section 3's bundle CTA."""
import json, re
BASE = 'baseline/product.ergoRelief.after-s4.json'
OUT = 'candidate/product.ergoRelief.json'
er = json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(BASE, encoding='utf-8').read(), count=1, flags=re.S))
assert not er['sections']['every_day_section_jYJzBQ'].get('disabled')
er['sections']['every_day_section_jYJzBQ']['disabled'] = True
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT)
