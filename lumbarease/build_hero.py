#!/usr/bin/env python3
"""LumbarEase hero + trust strip: same treatment as ErgoRelief (see ergorelief/build_hero.py,
ergorelief/build_s0.py). Layout/CSS identical; copy is LumbarEase's, from its product description.

Edits the parsed JSON; never hand-edit the template text.
"""
import copy
import json
import re
import sys

BASE = 'baseline/product.lumbarEase.json'
CB = 'baseline/product.ComfortBundle.json'
ER = 'baseline/product.ergoRelief.final.json'
OUT = 'candidate/product.lumbarEase.json'
BADGE = 'judge_me_reviews_preview_badge_UtwgBq'


def load(path):
    raw = open(path, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S))


def hero_css(cb):
    """Hero-only slice of the ComfortBundle anchor block (same slice ErgoRelief uses)."""
    css = cb['sections']['main']['blocks']['custom_liquid_heroAnchor']['settings']['custom_liquid']
    cut = '@media screen and (max-width:749px){.one-product-content'
    tail = '@media screen and (max-width:749px){.product__info-container .price .price-item'
    assert css.count(cut) == 1 and css.count(tail) == 1 and css.endswith('</style>')
    hero = css[:css.index(cut)] + css[css.index(tail):]
    for later in ('one-product', 'feature-', 'sub-heading-high'):
        assert later not in hero, later
    return hero


def main():
    le, cb, er = load(BASE), load(CB), load(ER)
    main_sec = le['sections']['main']
    blocks = main_sec['blocks']
    order = main_sec['block_order']

    # 1. main.settings -> same as ComfortBundle / ErgoRelief.
    main_sec['settings'].update({'media_size': 'small', 'padding_top': 8, 'padding_bottom': 24})

    # 2. Hero anchor CSS + review-badge spacing keyed to LE's badge block.
    badge_rule = ('@media screen and (max-width:749px){'
                  f'[id$="__{BADGE}"]'
                  '{margin-top:.5rem!important;margin-bottom:.5rem!important}}')
    css = hero_css(cb)
    css = css[:-len('</style>')] + badge_rule + '</style>'
    blocks['custom_liquid_heroAnchor'] = {'type': 'custom_liquid', 'settings': {'custom_liquid': css}}

    # 3. Eyebrow pill.
    blocks['custom_liquid_AwKGzJ'] = copy.deepcopy(er['sections']['main']['blocks']['custom_liquid_AwKGzJ'])

    # 4. Headline. The old subtitle was ErgoRelief's line ("Reduce seat pressure...").
    #    "Sit upright without trying." -- from the Description tab ("sitting upright without thinking
    #    about it"). Owner rejected the first pick, "Stop slumping by 2pm." (ad hook, reads two ways).
    blocks['text_AcTFLh']['settings']['text'] = 'Sit upright without trying.'

    # 5. Body line under price (was "Targeted back support..."), same role as ER's text_bodyER.
    blocks['text_RdmgPL']['settings']['text'] = (
        'Memory foam lumbar support, plus a 7-Day Reset plan to retrain how you sit.')

    # 6. Bullets: one line each at 402px; facts from the product description.
    bp = blocks['bullet_point_NzNW8e']['settings']
    bp['bullet-point-1'] = 'Curve holds your lower back in place'
    bp['bullet-point-2'] = 'Fills the gap your chair leaves'
    bp['bullet-point-3'] = 'Adjustable straps stop it sliding down'
    bp['bullet-point-4'] = '7-Day Reset builds the habit in a week'

    # 6b. Reset tab: this is the LumbarEase page, not the bundle.
    tab = blocks['collapsible_tab_X3EF6V']['settings']
    old = 'included free with every ComfortBundle™'
    assert tab['content'].count(old) == 1
    tab['content'] = tab['content'].replace(old, 'included with every LumbarEase™')

    # 7. Quantity selector off (orders: 69 of 74 contain LumbarEase; 2 multi-unit, both two-product carts).
    blocks['quantity_selector']['disabled'] = True

    # 8. Block order: anchor, eyebrow, headline, title, badge, price, body, bullets, rest.
    head = ['custom_liquid_heroAnchor', 'custom_liquid_AwKGzJ', 'text_AcTFLh', 'title',
            BADGE, 'price', 'text_RdmgPL', 'bullet_point_NzNW8e']
    main_sec['block_order'] = head + [b for b in order if b not in head]
    assert sorted(main_sec['block_order']) == sorted(blocks)

    # 9. Trust strip above the hero (same as ErgoRelief: "Express shipping", not free).
    assert 'sc_trust_strip' not in le['sections']
    le['sections'] = {'sc_trust_strip': copy.deepcopy(er['sections']['sc_trust_strip']), **le['sections']}
    le['order'].insert(0, 'sc_trust_strip')

    # Standing fact: LumbarEase ($62) does not ship free either.
    dumped = json.dumps(le, ensure_ascii=False).lower()
    for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
        assert bad not in dumped, f'free-shipping claim found: {bad!r}'

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(le, fh, ensure_ascii=False, indent=2)
    print('wrote', OUT)


if __name__ == '__main__':
    sys.exit(main())
