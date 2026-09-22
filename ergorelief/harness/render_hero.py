#!/usr/bin/env python3
"""Render the PDP hero from a template JSON against the theme's real CSS.

Usage: render_hero.py <template.json> <out.html> <theme_dir> <fonts_dir> <photo>

Harness limits (say these with every image):
- header + announcement bar are flat stand-ins at the measured real height
- the Judge.me stars badge is a stand-in (app block, cannot render)
- payment icons are grey placeholder boxes
- the photo is cropped from the owner's own phone screenshot
"""
import json
import re
import sys

tpl, out, theme, fonts, photo = sys.argv[1:6]
raw = open(tpl, encoding='utf-8').read()
t = json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S))
m = t['sections']['main']
S = m['settings']
SID = 'template--er__main'

BULLET_SVG = open(f'{theme}/snippets/bullets_points.liquid').read()
BULLET_SVG = BULLET_SVG[BULLET_SVG.index('<svg'):BULLET_SVG.index('</svg>') + 6]


def strip_scripts(s):
    return re.sub(r'<script.*?</script>', '', s, flags=re.S)


def block_html(bid, b):
    ty, st = b['type'], b.get('settings', {})
    attr = f'id="shopify-block-{SID}__{bid}"'
    if ty == 'custom_liquid':
        s = strip_scripts(st['custom_liquid'])
        if 'enabled_payment_types' in s:
            icons = ''.join('<li class="list-payment__item"><svg class="icon icon--full-color" '
                            'viewBox="0 0 38 24" width="38" height="24"><rect width="38" height="24" '
                            'rx="3" fill="#d9d9d9"/></svg></li>' for _ in range(8))
            s = re.sub(r'\{%-? for type.*?endfor -?%\}', icons, s, flags=re.S)
        return s
    if ty == 'text':
        cls = {'uppercase': ' caption-with-letter-spacing', 'subtitle': ' subtitle'}.get(st.get('text_style'), '')
        return f'<p class="product__text inline-richtext{cls}" {attr}>{st["text"]}</p>'
    if ty == 'title':
        return ('<div class="product__title"><h1>ErgoRelief™ Seat Cushion</h1>'
                '<a href="#" class="product__title"><h2 class="h1">ErgoRelief™ Seat Cushion</h2></a></div>')
    if ty.startswith('shopify://apps/judge-me'):
        return (f'<div {attr} class="shopify-app-block"><div class="jdgm-widget jdgm-preview-badge" '
                'style="display:flex;align-items:center;gap:6px;font-size:14px;line-height:1">'
                '<span style="color:#f5b301;font-size:17px;letter-spacing:1px">★★★★★</span>'
                '<span style="font-weight:600;color:#333">15 reviews</span></div></div>')
    if ty == 'price':
        return (f'<div id="price-{SID}" role="status"><div class="price price--large price--on-sale price--show-badge">'
                '<div class="price__container"><div class="price__regular"><span class="price-item price-item--regular">$71.00</span></div>'
                '<div class="price__sale"><span><s class="price-item price-item--regular">$89</s></span>'
                '<span class="price-item price-item--sale price-item--last">$71</span></div></div>'
                '<span class="badge price__badge-sale color-scheme-4">Save $18</span></div></div>'
                '<div class="product__tax caption rte">Tax included.</div>'
                '<div><form class="installment caption-large"></form></div>')
    if ty == 'bullet_point':
        items = ''.join(f'<div class="bullet-point">{BULLET_SVG}<span>{"" if i < 4 else " "}{st[k]}</span></div>'
                        for i, k in enumerate([f'bullet-point-{n}' for n in range(1, 7)], 1) if st.get(k))
        return f'<div class="bullte-points">{items}</div>'
    if ty == 'quantity_selector':
        return (f'<div id="Quantity-Form-{SID}" class="product-form__input product-form__quantity">'
                '<label class="quantity__label form__label"><span>Quantity</span></label>'
                '<div class="price-per-item__container"><quantity-input class="quantity">'
                '<button class="quantity__button" type="button">−</button>'
                '<input class="quantity__input" type="number" value="1">'
                '<button class="quantity__button" type="button">+</button></quantity-input></div></div>')
    if ty == 'buy_buttons':
        return ('<div><product-form class="product-form"><form><div class="product-form__buttons">'
                '<button id="atc" type="submit" name="add" class="product-form__submit button button--full-width button--primary">'
                '<span>Add ErgoRelief to cart</span></button>'
                f'<a href="#" class="product-detail-btn btn-globel btn-globel--solid">{st.get("worktext","")}</a>'
                '</div></form></product-form></div>')
    if ty == 'icon-with-text':
        lis = ''.join(f'<li class="icon-with-text__item"><span style="display:inline-block;width:50px;height:50px;'
                      f'background:#e6e6e6;border-radius:50%"></span><span class="h4 inline-richtext">{st[f"heading_{n}"]}</span></li>'
                      for n in (1, 2, 3))
        return f'<ul class="icon-with-text icon-with-text--horizontal list-unstyled">{lis}</ul>'
    if ty == 'collapsible_tab':
        return (f'<div class="product__accordion accordion quick-add-hidden"><details><summary><div class="summary__title">'
                f'<h2 class="h4 accordion__title inline-richtext">{st["heading"]}</h2></div></summary></details></div>')
    return ''  # variant_picker (single variant), video_reviews carousel etc. not rendered


info = ''.join(block_html(bid, m['blocks'][bid]) for bid in m['block_order']
               if not m['blocks'][bid].get('disabled') and m['blocks'][bid]['type'] not in ('video_reviews',))
constrain = ' constrain-height' if S.get('constrain_to_viewport') else ''
media = (f'<div class="product-media-container media-type-image media-fit-{S["media_fit"]} global-media-settings gradient{constrain}" '
         'style="--ratio:1.0;--ratio-percent:100.0%;--aspect-ratio:1"><div class="media media--transparent">'
         f'<img src="{photo}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain"></div></div>')

css_files = ['assets/base.css', 'assets/cstm-style.css', 'assets/resposive.css', 'assets/custom.css']
body_css = ['assets/section-main-product.css', 'assets/component-price.css']
link = lambda f: f'<link rel="stylesheet" href="{theme}/{f}">'
font_face = ''.join(
    f"@font-face{{font-family:{fam};font-weight:{w};src:url({fonts}/fontsource-{fam.lower()}/files/{fam.lower()}-latin-{w}-normal.woff2)}}"
    for fam in ('Poppins', 'Inter') for w in (400, 500, 600, 700))

root = """
:root,.color-scheme-2{--color-background:255,255,255;--gradient-background:#ffffff;--color-foreground:0,0,0;--color-background-contrast:191,191,191;--color-shadow:26,122,110;--color-button:26,122,110;--color-button-text:255,255,255;--color-secondary-button:255,255,255;--color-secondary-button-text:26,122,110;--color-link:26,122,110;--color-badge-foreground:0,0,0;--color-badge-background:255,255,255;--color-badge-border:0,0,0}
.color-scheme-4{--color-background:18,18,18;--color-foreground:255,255,255;--color-badge-foreground:255,255,255;--color-badge-background:18,18,18;--color-badge-border:255,255,255}
body{color:rgba(var(--color-foreground),.75);background-color:rgb(var(--color-background))}
:root{--font-body-family:Inter,sans-serif;--font-body-style:normal;--font-body-weight:400;--font-body-weight-bold:700;--font-heading-family:Poppins,sans-serif;--font-heading-style:normal;--font-heading-weight:400;--font-body-scale:1;--font-heading-scale:1;--media-padding:px;--media-border-opacity:.05;--media-border-width:1px;--media-radius:0px;--media-shadow-opacity:0;--media-shadow-visible:0;--page-width:140rem;--page-width-margin:0rem;--badge-corner-radius:4rem;--spacing-sections-desktop:0px;--spacing-sections-mobile:0px;--grid-desktop-vertical-spacing:8px;--grid-desktop-horizontal-spacing:8px;--grid-mobile-vertical-spacing:4px;--grid-mobile-horizontal-spacing:4px;--buttons-radius:0px;--buttons-radius-outset:0px;--buttons-border-width:1px;--buttons-border-opacity:1;--buttons-shadow-opacity:0;--buttons-shadow-visible:0;--buttons-shadow-horizontal-offset:0px;--buttons-shadow-vertical-offset:4px;--buttons-shadow-blur-radius:5px;--buttons-border-offset:0px;--inputs-radius:0px;--inputs-border-width:1px;--inputs-border-opacity:.55;--inputs-shadow-opacity:0;--inputs-margin-offset:0px;--inputs-radius-outset:0px;--variant-pills-radius:40px}
*,*::before,*::after{box-sizing:inherit}
html{box-sizing:border-box;font-size:62.5%;height:100%}
body{display:grid;grid-template-rows:auto auto 1fr auto;grid-template-columns:100%;min-height:100%;margin:0;font-size:1.5rem;letter-spacing:.06rem;line-height:1.8;font-family:var(--font-body-family);font-weight:400}
.list-payment{display:flex;flex-wrap:wrap;justify-content:center;gap:.5rem;margin:0;padding:0;list-style:none}.list-payment__item{display:flex}
.stub-ann{height:38px;background:#1a7a6e;color:#fff;font:14px/38px Poppins,sans-serif;text-align:center}
.stub-hdr{height:72px;border-bottom:1px solid #eee;display:flex;align-items:center;justify-content:center;font:600 20px Poppins,sans-serif;color:#1a7a6e}
"""
sec_css = (f'.section-{SID}-padding{{padding-top:0;padding-bottom:{round(S["padding_bottom"]*0.75)}px}}'
           f'@media screen and (min-width:750px){{.section-{SID}-padding{{padding-top:{S["padding_top"]}px;padding-bottom:{S["padding_bottom"]}px}}}}')

html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>{font_face}{root}</style>{''.join(map(link, css_files))}</head>
<body><div><div class="stub-ann">Announcement bar (stand-in)</div><div class="stub-hdr">Header (stand-in)</div></div>
<main><product-info class="section-{SID}-padding gradient color-scheme-2">{''.join(map(link, body_css))}<style>{sec_css}</style>
<div class="page-width"><div class="product product--{S['media_size']} product--left product--thumbnail_slider product--mobile-hide grid grid--1-col grid--2-col-tablet">
<div class="grid__item product__media-wrapper"><media-gallery class="product__column-sticky flex-media"><slider-component class="slider-mobile-gutter">
<ul class="product__media-list contains-media grid grid--peek list-unstyled slider slider--mobile"><li class="product__media-item grid__item slider__slide is-active">{media}</li></ul>
</slider-component></media-gallery></div>
<div class="product__info-wrapper grid__item"><section id="ProductInfo-{SID}" class="product__info-container product__column-sticky">{info}</section></div>
</div></div></product-info></main></body></html>"""
open(out, 'w', encoding='utf-8').write(html)
print('wrote', out, len(html))
