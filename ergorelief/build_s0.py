#!/usr/bin/env python3
"""Trust strip above the hero, same as ComfortBundle's sc_trust_strip, minus the
free-shipping claim (ErgoRelief does not ship free)."""
import copy, json, re, sys

BASE = 'baseline/product.ergoRelief.after-s2.json'
CB = 'baseline/product.ComfortBundle.json'
OUT = 'candidate/product.ergoRelief.json'


def load(p):
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(p, encoding='utf-8').read(), count=1, flags=re.S))


er, cb = load(BASE), load(CB)
strip = copy.deepcopy(cb['sections']['sc_trust_strip'])
liq = strip['settings']['custom_liquid']
old = 'Sydney dispatch &middot; Free shipping &middot; 30-day money-back'
assert liq.count(old) == 1
strip['settings']['custom_liquid'] = liq.replace(
    old, 'Sydney dispatch &middot; Express shipping &middot; 30-day money-back')
assert 'sc_trust_strip' not in er['sections']
er['sections'] = {'sc_trust_strip': strip, **er['sections']}
er['order'].insert(0, 'sc_trust_strip')

dumped = json.dumps(er, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT)
