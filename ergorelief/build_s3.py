#!/usr/bin/env python3
"""Section 3 (one_product_PTdiHH): bring the ComfortBundle version across.

Owner: 'bring most of the content here from bundle page, only title can stay'.
This section SELLS THE BUNDLE (owner: 'is about bundle and encouraging people to click
to Cta and go to bundle page'), so CB copy and photo are used verbatim.
Kept from ErgoRelief: heading, button_link (goes to the ComfortBundle page -- on CB the
button adds the bundle itself), bg_color (white: section 2 directly above is #f4f6f5).
Everything else, blocks and CB's one-product mobile CSS, comes from CB.
"""
import copy, json, re, sys

BASE = 'baseline/product.ergoRelief.after-s0.json'
CB = 'baseline/product.ComfortBundle.json'
OUT = 'candidate/product.ergoRelief.json'
KEY = 'one_product_PTdiHH'
KEEP = ('heading', 'button_link', 'bg_color')


def load(p):
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(p, encoding='utf-8').read(), count=1, flags=re.S))


er, cb = load(BASE), load(CB)
es, cs = er['sections'][KEY], cb['sections'][KEY]
for k, v in cs['settings'].items():
    if k not in KEEP:
        es['settings'][k] = v
assert es['block_order'] == cs['block_order']
es['blocks'] = copy.deepcopy(cs['blocks'])

# CB's one-product CSS (mobile reorder, 70% image, compact icon rows, its icons).
css = cb['sections']['main']['blocks']['custom_liquid_heroAnchor']['settings']['custom_liquid']
start = css.index('@media screen and (max-width:749px){.one-product-content')
end = css.index('.sub-heading-high')
op_css = css[start:end]
assert '.feature-' not in op_css and op_css.count('.one-product-blocks .one-product-block:nth-child') == 4
anchor = er['sections']['main']['blocks']['custom_liquid_heroAnchor']['settings']
assert 'one-product' not in anchor['custom_liquid']
anchor['custom_liquid'] = anchor['custom_liquid'][:-len('</style>')] + op_css + '</style>'

dumped = json.dumps(er, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT)
