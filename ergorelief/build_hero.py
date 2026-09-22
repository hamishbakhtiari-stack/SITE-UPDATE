#!/usr/bin/env python3
"""Build the ErgoRelief hero candidate from the live baseline.

Mirrors the ComfortBundle hero: same main.settings, same hero-anchor CSS
(hero rules only -- the one-product / feature-highlight rules in the CB anchor
belong to later sections and are ported when we reach them), headline moved
above the title, body line under price, tighter bullets, quantity disabled.

Edits the parsed JSON; never hand-edit the template text.
"""
import json
import re
import sys

BASE = 'baseline/product.ergoRelief.json'
CB = 'baseline/product.ComfortBundle.json'
OUT = 'candidate/product.ergoRelief.json'


def load(path):
    raw = open(path, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S))


def hero_css(cb):
    """Hero-only slice of the ComfortBundle anchor block."""
    css = cb['sections']['main']['blocks']['custom_liquid_heroAnchor']['settings']['custom_liquid']
    cut = '@media screen and (max-width:749px){.one-product-content'
    tail = '@media screen and (max-width:749px){.product__info-container .price .price-item'
    head_end = css.index(cut)
    tail_start = css.index(tail)
    assert css.count(cut) == 1 and css.count(tail) == 1
    assert css.endswith('</style>')
    hero = css[:head_end] + css[tail_start:]
    # Nothing from later sections may leak in.
    for later in ('one-product', 'feature-', 'sub-heading-high'):
        assert later not in hero, later
    return hero


def main():
    er = load(BASE)
    cb = load(CB)
    main_sec = er['sections']['main']
    blocks = main_sec['blocks']
    order = main_sec['block_order']

    # 1. main.settings -> ComfortBundle values (layout of photo + padding).
    main_sec['settings'].update({
        'media_size': 'small',
        'padding_top': 8,
        'padding_bottom': 24,
    })

    # 2. Hero anchor: CB hero CSS, plus the review-badge spacing CB gets from a
    #    block-ID rule in custom.css (keyed to CB's block, so it misses ER's).
    css = hero_css(cb)
    badge_rule = ('@media screen and (max-width:749px){'
                  '[id$="__judge_me_reviews_preview_badge_qB9XCU"]'
                  '{margin-top:.5rem!important;margin-bottom:.5rem!important}}')
    css = css[:-len('</style>')] + badge_rule + '</style>'
    blocks['custom_liquid_heroAnchor'] = {'type': 'custom_liquid', 'settings': {'custom_liquid': css}}

    # 3. Eyebrow pill, same as CB.
    blocks['custom_liquid_AwKGzJ'] = {
        'type': 'custom_liquid',
        'settings': {'custom_liquid': '<div class="bst"><p>Better Sitting in 7 Days</p></div>'},
    }

    # 4. Headline (subtitle style -> 26px bold via anchor CSS), above the title.
    blocks['text_jwDAhr']['settings']['text'] = 'Sit longer without the ache.'

    # 5. Body line under price, same role as CB's text_z3HGpc.
    blocks['text_bodyER'] = {
        'type': 'text',
        'settings': {'text': 'Memory foam cushion, plus a 7-Day Reset plan to retrain how you sit.',
                     'text_style': 'body'},
    }

    # 6. Bullets: one line each, mechanism not adjectives. Facts from the product description.
    bp = blocks['bullet_point_6Fn37y']['settings']
    bp['bullet-point-1'] = 'Cut-out takes pressure off your tailbone'
    bp['bullet-point-2'] = 'Contour cradles your hips and thighs'
    bp['bullet-point-3'] = 'Anti-slip base stays put on any chair'
    bp['bullet-point-4'] = '7-Day Reset builds the habit in a week'

    # 6b. Reset tab: this is the ErgoRelief page, not the bundle.
    tab = blocks['collapsible_tab_fri6mY']['settings']
    old = 'included free with every ComfortBundle™'
    assert tab['content'].count(old) == 1
    tab['content'] = tab['content'].replace(old, 'included with every ErgoRelief™')

    # 7. Quantity selector off (74 orders: 2 multi-unit, both two-product carts).
    blocks['quantity_selector']['disabled'] = True

    # 8. New block order: anchor, eyebrow, headline, title, badge, price, body, bullets, rest.
    head = ['custom_liquid_heroAnchor', 'custom_liquid_AwKGzJ', 'text_jwDAhr', 'title',
            'judge_me_reviews_preview_badge_qB9XCU', 'price', 'text_bodyER', 'bullet_point_6Fn37y']
    rest = [b for b in order if b not in head]
    main_sec['block_order'] = head + rest
    assert sorted(main_sec['block_order']) == sorted(blocks), 'block_order / blocks mismatch'

    # Standing fact: ErgoRelief does NOT ship free. No copy on this page may say so.
    dumped = json.dumps(er, ensure_ascii=False).lower()
    for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
        assert bad not in dumped, f'free-shipping claim found: {bad!r}'

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(er, fh, ensure_ascii=False, indent=2)
    print('wrote', OUT)


if __name__ == '__main__':
    sys.exit(main())
