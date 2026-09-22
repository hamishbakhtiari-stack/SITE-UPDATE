#!/usr/bin/env python3
"""Section 3 (one_product_PTdiHH): bring the ComfortBundle version across.

Owner: 'bring most of the content here from bundle page, only title can stay'.
Kept from ErgoRelief: heading, section_image (his photo), button_link (goes to the
ComfortBundle page -- on CB the button adds the bundle itself), bg_color (white:
section 2 directly above is #f4f6f5, so CB's grey would merge the two sections).
Everything else, blocks and CB's one-product mobile CSS, comes from CB.
"""
import copy, json, re, sys

BASE = 'baseline/product.ergoRelief.after-s0.json'
CB = 'baseline/product.ComfortBundle.json'
OUT = 'candidate/product.ergoRelief.json'
KEY = 'one_product_PTdiHH'
KEEP = ('heading', 'section_image', 'button_link', 'bg_color')


def load(p):
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(p, encoding='utf-8').read(), count=1, flags=re.S))


er, cb = load(BASE), load(CB)
es, cs = er['sections'][KEY], cb['sections'][KEY]
for k, v in cs['settings'].items():
    if k not in KEEP:
        es['settings'][k] = v
assert es['block_order'] == cs['block_order']
es['blocks'] = copy.deepcopy(cs['blocks'])

# CB copy assumes the reader is buying both. On this page they are not, so name the
# products; wording otherwise unchanged.
swaps = {
    'feature_pXURKz': ('The contoured cut-out keeps', "ErgoRelief™'s contoured cut-out keeps"),
    'feature_WHamjG': ('The lumbar support holds it there', 'LumbarEase™ holds it there'),
    'feature_pJJif9': ('what lets the lumbar support do its job', 'what lets LumbarEase™ do its job'),
}
for bid, (old, new) in swaps.items():
    sub = es['blocks'][bid]['settings']['block_subheading']
    assert sub.count(old) == 1, bid
    es['blocks'][bid]['settings']['block_subheading'] = sub.replace(old, new)

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
