#!/usr/bin/env python3
"""Sections 7-11 mirrored from ComfortBundle (owner: 'mirror ... only no free shipping ... do all together').

7  video_reviews_V3QqMX      <- CB video_reviews_K3ixGw verbatim (blocks, order, settings). Review count
                               comes from the Judge.me badge per product, so it differs automatically.
8  feature_highlight_kEKcXt  <- CB text/blocks/order + CB feature-highlight CSS. Kept ER's own photo +
                               corner image (CB's photo/alt show both products); ER's 2 extra blocks disabled.
9  faq_bMxpUE                <- CB verbatim except: shipping answer drops 'Free'; button adds ErgoRelief.
10 apps_JXNAik (Judge.me)    <- CB custom_css (white bg, clamp padding). Widget block untouched.
11 cta_section_tEApVF        <- CB verbatim except: subheading drops 'Free'; button adds ErgoRelief and says
                               'Start your 7-Day Reset' (CB's 'Get the full system' adds the bundle there).
"""
import copy, json, re
BASE = 'baseline/product.ergoRelief.after-s6.json'
CB = 'baseline/product.ComfortBundle.json'
OUT = 'candidate/product.ergoRelief.json'
ER_VAR, CB_VAR = '48771729031425', '49378080227585'
ER_ATC = f'/cart/add?id={ER_VAR}&quantity=1&return_to=/cart'


def load(p):
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(p, encoding='utf-8').read(), count=1, flags=re.S))


er, cb = load(BASE), load(CB)
S, C = er['sections'], cb['sections']

# 7 -- Real people
vr = S['video_reviews_V3QqMX']
cvr = copy.deepcopy(C['video_reviews_K3ixGw'])
vr['blocks'], vr['block_order'], vr['settings'] = cvr['blocks'], cvr['block_order'], cvr['settings']

# 8 -- Australian, end to end
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

# 9 -- FAQ
fq = S['faq_bMxpUE']
cfq = copy.deepcopy(C['faq_bMxpUE'])
ship = cfq['blocks']['faq_Prjczy']['settings']
old = 'Free express shipping across Australia'
assert ship['answer'].count(old) == 1
ship['answer'] = ship['answer'].replace(old, 'Express shipping across Australia')
assert cfq['settings']['button_link'] == f'/cart/add?id={CB_VAR}&quantity=1&return_to=/cart'
cfq['settings']['button_link'] = ER_ATC
fq['blocks'], fq['block_order'], fq['settings'] = cfq['blocks'], cfq['block_order'], cfq['settings']

# 10 -- Judge.me reviews widget
S['apps_JXNAik']['custom_css'] = list(C['177934200903caf21b']['custom_css'])

# 11 -- closing banner
cta = S['cta_section_tEApVF']
ccta = copy.deepcopy(C['cta_section_tEApVF']['settings'])
old = 'Free express shipping from Sydney'
assert ccta['subheading'].count(old) == 1
ccta['subheading'] = ccta['subheading'].replace(old, 'Express shipping from Sydney')
ccta['button_text'] = 'Start your 7-Day Reset'
ccta['button_link'] = ER_ATC
cta['settings'] = ccta

# CB feature-highlight CSS -> ER anchor
css = C['main']['blocks']['custom_liquid_heroAnchor']['settings']['custom_liquid']
fcss = css[css.index('.sub-heading-high'):css.index('@media screen and (max-width:749px){.product__info-container .price .price-item')]
anchor = S['main']['blocks']['custom_liquid_heroAnchor']['settings']
assert '.feature-grid' not in anchor['custom_liquid']
anchor['custom_liquid'] = anchor['custom_liquid'][:-len('</style>')] + fcss + '</style>'

dumped = json.dumps(er, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
assert CB_VAR not in json.dumps(er), 'bundle variant leaked into ErgoRelief page'
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT)
