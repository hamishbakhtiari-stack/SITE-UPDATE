#!/usr/bin/env python3
"""Render pws_image_with_text from a template JSON. Stand-ins: main image = grey square
(1254x1254 real ratio), tick icon = small grey dot (real icon is a 14x14 PNG)."""
import json, sys
tpl, key, out, theme, fonts = sys.argv[1:6]
t = json.load(open(tpl)); s = t['sections'][key]; st = s['settings']
items = ''
for b in s['block_order']:
    if s['blocks'][b].get('disabled'): continue
    bs = s['blocks'][b]['settings']
    icon = ('<div class="product-image-text__icon"><span style="display:inline-block;width:14px;height:14px;'
            'border-radius:50%;background:#bbb"></span></div>') if bs.get('icon') else ''
    items += f'<div class="product-image-text__item">{icon}<div class="product-image-text__text">{bs.get("text","")}</div></div>'
ff = ''.join(f"@font-face{{font-family:{f};font-weight:{w};src:url({fonts}/fontsource-{f.lower()}/files/{f.lower()}-latin-{w}-normal.woff2)}}"
             for f in ('Poppins', 'Inter') for w in (400, 500, 600, 700))
links = ''.join(f'<link rel="stylesheet" href="{theme}/assets/{c}">' for c in ('base.css', 'cstm-style.css', 'resposive.css', 'custom.css'))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}
:root{{--font-body-family:Inter,sans-serif;--font-heading-family:Poppins,sans-serif;--font-body-scale:1;--font-heading-scale:1;--color-foreground:0,0,0;--color-background:255,255,255;--page-width:140rem}}
*,*::before,*::after{{box-sizing:border-box}}html{{font-size:62.5%}}body{{margin:0;font-size:1.5rem;letter-spacing:.06rem;line-height:1.8;font-family:Inter,sans-serif;color:rgba(0,0,0,.75)}}
.stub-img{{aspect-ratio:1;background:#d5dbd9;border-radius:20px;display:flex;align-items:center;justify-content:center;font:14px Inter;color:#555}}</style>{links}</head><body>
<section id="sec" class="product-image-text" style="background:{st['bg_color']};padding-top:{st['padding_top_desktop']}px;padding-bottom:{st['padding_bottom_desktop']}px"><div class="page-width">
<div class="product-image-text__wrapper" style="flex-direction:{st['image_position']}">
<div class="product-image-text__image"><div class="stub-img">section image (stand-in)</div></div>
<div class="product-image-text__content"><p class="product-image-text__subheading">{st.get('sub_heading','')}</p>
<h2 class="heading-h2">{st.get('heading','')}</h2><div class="product-image-text__list">{items}</div>
{f'<a href="#" class="btn-globel btn-globel--solid">{st["button_text"]}</a>' if st.get('button_text') else ''}</div></div></div></section>
<style>@media screen and (max-width:749px){{.product-image-text{{padding-top:{st['padding_top_mobile']}px!important;padding-bottom:{st['padding_bottom_mobile']}px!important}}}}</style>
</body></html>"""
open(out, 'w').write(html)
