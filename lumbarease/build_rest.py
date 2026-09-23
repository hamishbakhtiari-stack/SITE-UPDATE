#!/usr/bin/env python3
"""LumbarEase sections 2-11 + CTA delegate: the same treatment as ErgoRelief's final page.
Owner approved the whole plan in one go ("Yes"). Reads the pushed hero state, writes the candidate.

2  pws_image_with_text   one job: "Leaning back isn't the fix." (from the product description); bullets
                         disabled; button -> add LumbarEase
3  one_product           ComfortBundle copy verbatim (bundle pitch) + subheading naming ErgoRelief;
                         heading kept; button -> bundle page; white bg; CB one-product CSS
4  7days                 lock note names LumbarEase; button adds LumbarEase (opt-in settings already in the section)
5  every_day             disabled
6  single_support        durability line; button -> add LumbarEase; diagram hidden <=991px
7-11                     mirrored from ComfortBundle; no free shipping; buttons add LumbarEase
CTA                      sc-cta-delegate: every /cart/add link goes through the hero's own Add to Cart
"""
import copy
import json
import re

BASE = 'candidate/product.lumbarEase.json'
CB = 'baseline/product.ComfortBundle.json'
ER = 'baseline/product.ergoRelief.final.json'
OUT = 'candidate/product.lumbarEase.json'
LE_VAR, CB_VAR, ER_VAR = '48772058022145', '49378080227585', '48771729031425'
ATC = f'/cart/add?id={LE_VAR}&quantity=1&return_to=/cart'


def load(p):
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(p, encoding='utf-8').read(), count=1, flags=re.S))


le, cb, er = load(BASE), load(CB), load(ER)
S, C, E = le['sections'], cb['sections'], er['sections']
main = S['main']

# CTA delegate (ErgoRelief's fixed version), second block in main.
assert 'custom_liquid_cartAddLink' not in main['blocks']
main['blocks']['custom_liquid_cartAddLink'] = copy.deepcopy(E['main']['blocks']['custom_liquid_cartAddLink'])
assert 'sc-cta-delegate' in main['blocks']['custom_liquid_cartAddLink']['settings']['custom_liquid']
bo = main['block_order']
bo.insert(bo.index('custom_liquid_heroAnchor') + 1, 'custom_liquid_cartAddLink')

# Anchor CSS: ErgoRelief's final anchor = hero CSS + badge rule + one-product + single-support + feature-highlight.
er_anchor = E['main']['blocks']['custom_liquid_heroAnchor']['settings']['custom_liquid'].replace(
    'judge_me_reviews_preview_badge_qB9XCU', 'judge_me_reviews_preview_badge_UtwgBq')
le_anchor = main['blocks']['custom_liquid_heroAnchor']['settings']
assert er_anchor.startswith(le_anchor['custom_liquid'][:-len('</style>')]), 'LE hero CSS drifted from ER'
le_anchor['custom_liquid'] = er_anchor

# 2 -- image with text
s2 = S['pws_image_with_text_bTKkTU']
s2['settings']['heading'] = "Leaning back isn't the fix."
s2['blocks']['icon_list_mwrwGe']['settings']['text'] = (
    "A soft chair back doesn't hold your spine's curve — it just moves where you slump. "
    "LumbarEase™ keeps your lower back supported in the same position the whole time you sit.")
for b in ('icon_list_DUyxWa', 'icon_list_rdYrwQ', 'icon_list_qY8HDt', 'icon_list_jixVXV'):
    s2['blocks'][b]['disabled'] = True
s2['settings']['button_text'] = 'Add LumbarEase to cart'
s2['settings']['button_link'] = ATC

# 3 -- Why One Product Isn't Enough (sells the bundle)
s3, c3 = S['one_product_PTdiHH'], C['one_product_PTdiHH']
for k, v in c3['settings'].items():
    if k not in ('heading', 'button_link', 'bg_color'):
        s3['settings'][k] = v
s3['blocks'] = copy.deepcopy(c3['blocks'])
assert s3['block_order'] == c3['block_order']
s3['settings']['subheading'] = ('The ComfortBundle™ pairs this lumbar support with the ErgoRelief™ seat cushion — '
                                'so seat and spine are supported together, then reinforced over 7 days.')
assert s3['settings']['button_link'] == 'shopify://products/comfortbundle-complete-system'

# 4 -- 7-Day Reset
S['7days_Grhwr4']['settings'].update({
    'lock_text_override': 'Days 4–7 unlock when you start the Reset — included with LumbarEase™',
    'button_adds_product': True,
})

# 5 -- every-day section off
S['every_day_section_jYJzBQ']['disabled'] = True

# 6 -- All-Day Support
s6 = S['single_support_section_R8ffeX']['settings']
s6['description'] = ('Firm-but-forgiving support that holds its shape — '
                     'so it keeps working after the first week, not just on day one.')
s6['subheading'] = ''  # repeated the page title; ErgoRelief's is blank
s6['button_text'] = 'Add LumbarEase to cart'
s6['button_link'] = ATC

# 7 -- Real people: ComfortBundle verbatim
vr, cvr = S['video_reviews_CJJRFe'], copy.deepcopy(C['video_reviews_K3ixGw'])
vr['blocks'], vr['block_order'], vr['settings'] = cvr['blocks'], cvr['block_order'], cvr['settings']

# 8 -- Australian, end to end: CB copy/blocks; LE's own photo kept; extra blocks disabled
fh, cfh = S['feature_highlight_kEKcXt'], C['feature_highlight_kEKcXt']
for k in ('heading', 'heading_span', 'subheading', 'bg_color', 'image_position',
          'padding_top_desktop', 'padding_bottom_desktop', 'padding_top_mobile', 'padding_bottom_mobile'):
    fh['settings'][k] = cfh['settings'][k]
extras = [b for b in fh['block_order'] if b not in cfh['blocks']]
for b in cfh['blocks']:
    fh['blocks'][b] = copy.deepcopy(cfh['blocks'][b])
for b in extras:
    fh['blocks'][b]['disabled'] = True
fh['block_order'] = list(cfh['block_order']) + extras

# 9 -- FAQ: CB verbatim, no "Free", button adds LumbarEase
fq, cfq = S['faq_bMxpUE'], copy.deepcopy(C['faq_bMxpUE'])
ship = cfq['blocks']['faq_Prjczy']['settings']
assert ship['answer'].count('Free express shipping across Australia') == 1
ship['answer'] = ship['answer'].replace('Free express shipping across Australia', 'Express shipping across Australia')
cfq['settings']['button_link'] = ATC
fq['blocks'], fq['block_order'], fq['settings'] = cfq['blocks'], cfq['block_order'], cfq['settings']

# 10 -- Judge.me widget spacing
S['apps_fUnDPm']['custom_css'] = list(C['177934200903caf21b']['custom_css'])

# 11 -- closing banner
ccta = copy.deepcopy(C['cta_section_tEApVF']['settings'])
assert ccta['subheading'].count('Free express shipping from Sydney') == 1
ccta['subheading'] = ccta['subheading'].replace('Free express shipping from Sydney', 'Express shipping from Sydney')
ccta['button_text'] = 'Start your 7-Day Reset'
ccta['button_link'] = ATC
S['cta_section_tEApVF']['settings'] = ccta

# Guards
raw = json.dumps(le)
links = re.findall(r'/cart/add\?id=(\d+)', raw)
assert links and set(links) == {LE_VAR}, links
assert CB_VAR not in raw and ER_VAR not in raw, 'another product variant leaked in'
dumped = json.dumps(le, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
assert sorted(main['block_order']) == sorted(main['blocks'])
json.dump(le, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT, '| /cart/add links:', len(links))
