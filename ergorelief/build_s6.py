#!/usr/bin/env python3
"""Section 6 (single_support_section_QU6dHr) + section 4 button.
- Mobile/tablet (<=991px, where the section stacks): hide the line-drawing diagram, keep the
  'Thoughtful Details' product image (owner chose after seeing both). Desktop unchanged.
  CSS goes in ER's heroAnchor so it only affects this template (the section is shared with LumbarEase).
- Description: durability line (from the product description) instead of the LumbarEase pitch.
- Button: linked to this same page (reload). Now a real add-to-cart link (opens drawer via cartAddLink).
- Section 4: 7days button adds ErgoRelief on this page (opt-in button_adds_product).
"""
import json, re
BASE = 'baseline/product.ergoRelief.after-s5.json'
OUT = 'candidate/product.ergoRelief.json'
VARIANT = '48771729031425'
er = json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(BASE, encoding='utf-8').read(), count=1, flags=re.S))

st = er['sections']['single_support_section_QU6dHr']['settings']
st['description'] = ('Supportive enough to hold its shape through a full workday — '
                     'so it keeps working after the first week, not just on day one.')
st['button_text'] = 'Add ErgoRelief to cart'
st['button_link'] = f'/cart/add?id={VARIANT}&quantity=1&return_to=/cart'

anchor = er['sections']['main']['blocks']['custom_liquid_heroAnchor']['settings']
rule = '@media screen and (max-width:991px){.single-support-section .support-image{display:none!important}}'
assert rule not in anchor['custom_liquid']
anchor['custom_liquid'] = anchor['custom_liquid'][:-len('</style>')] + rule + '</style>'

er['sections']['7days_P3eEBF']['settings']['button_adds_product'] = True

dumped = json.dumps(er, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT)
