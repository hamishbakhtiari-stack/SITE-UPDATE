#!/usr/bin/env python3
"""Section 2 (pws_image_with_text): give it one job -- 'softness isn't the fix'.

Reads the pushed state (baseline/product.ergoRelief.after-s1.json), writes candidate.
Template settings only; sections/pws_image_with_text.liquid is shared with
LumbarEase and is not touched.
"""
import json
import sys

BASE = 'baseline/product.ergoRelief.after-s1.json'
CB = 'baseline/product.ComfortBundle.json'
OUT = 'candidate/product.ergoRelief.json'
VARIANT = '48771729031425'
KEY = 'pws_image_with_text_U7pgnH'


def load(p):
    import re
    raw = open(p, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S))


def main():
    er = load(BASE)
    sec = er['sections'][KEY]
    st, blocks = sec['settings'], sec['blocks']

    # Headline carries the argument; eyebrow stays.
    st['heading'] = "Softness isn't the fix."
    blocks['icon_list_pdi698']['settings']['text'] = (
        "Extra foam only softens the same pressure points. ErgoRelief™'s contour and "
        "cut-out change where your weight lands, so the ache doesn't build 20–30 minutes in.")

    # Feature bullets repeat the hero -> disabled, not deleted.
    for b in ('icon_list_bM8qg6', 'icon_list_6WDpLk', 'icon_list_NLhAyM', 'icon_list_3cazAc'):
        blocks[b]['disabled'] = True

    # CTA: was a link to this same page (reload, nothing added). Now a real add-to-cart
    # link that also works without JS.
    st['button_text'] = 'Add ErgoRelief to cart'
    st['button_link'] = f'/cart/add?id={VARIANT}&quantity=1&return_to=/cart'

    # Open the cart drawer for /cart/add links, like the hero button does. Only the
    # AJAX-add script from CB's delegate block: the capture-phase catch-all would also
    # hijack the lower 'Get the Full System' (ComfortBundle) buttons.
    cb_js = load(CB)['sections']['main']['blocks']['custom_liquid_cartDrawerAjax']['settings']['custom_liquid']
    first = cb_js[:cb_js.index('</script>') + len('</script>')]
    assert 'a[href^=\\"/cart/add?\\"]' in first and 'sc-cta-delegate' not in first
    m = er['sections']['main']
    m['blocks']['custom_liquid_cartAddLink'] = {'type': 'custom_liquid', 'settings': {'custom_liquid': first}}
    order = m['block_order']
    order.insert(order.index('custom_liquid_heroAnchor') + 1, 'custom_liquid_cartAddLink')
    assert sorted(order) == sorted(m['blocks'])

    dumped = json.dumps(er, ensure_ascii=False).lower()
    for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
        assert bad not in dumped, bad

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(er, fh, ensure_ascii=False, indent=2)
    print('wrote', OUT)


if __name__ == '__main__':
    sys.exit(main())
