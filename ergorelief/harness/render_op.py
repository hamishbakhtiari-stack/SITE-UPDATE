#!/usr/bin/env python3
"""Render one-product section. Stand-ins: section photo = grey 651x907 box; block icon
files (one.png...) = grey squares unless the template's anchor CSS swaps them."""
import json, re, sys
tpl, key, out, theme, fonts = sys.argv[1:6]
t = json.load(open(tpl)); s = t['sections'][key]; st = s['settings']
anchor = t['sections']['main']['blocks'].get('custom_liquid_heroAnchor', {}).get('settings', {}).get('custom_liquid', '')
anchor = re.sub(r'<div id="hero-buy-section"></div>', '', anchor)
GREY = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 44 44'%3E%3Crect width='44' height='44' fill='%23ccc'/%3E%3C/svg%3E"
h = st['heading']; pre, rest = h.split('[', 1); hi, post = rest.split(']', 1)
blocks = ''.join(f'<div class="one-product-block"><div class="one-product-icon"><img src="{GREY}" width="44" height="44"></div>'
                 f'<h4>{b["settings"]["block_heading"]}</h4><p>{b["settings"]["block_subheading"]}</p></div>'
                 for b in (s['blocks'][i] for i in s['block_order']) if not b.get('disabled'))
ff = ''.join(f"@font-face{{font-family:{f};font-weight:{w};src:url({fonts}/fontsource-{f.lower()}/files/{f.lower()}-latin-{w}-normal.woff2)}}"
             for f in ('Poppins', 'Inter') for w in (400, 500, 600, 700))
links = ''.join(f'<link rel="stylesheet" href="{theme}/assets/{c}">' for c in ('base.css', 'cstm-style.css', 'resposive.css', 'custom.css'))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}
:root{{--font-body-family:Inter,sans-serif;--font-heading-family:Poppins,sans-serif;--font-body-scale:1;--font-heading-scale:1;--color-foreground:0,0,0;--color-background:255,255,255;--page-width:140rem}}
*,*::before,*::after{{box-sizing:border-box}}html{{font-size:62.5%}}body{{margin:0;font-size:1.5rem;letter-spacing:.06rem;line-height:1.8;font-family:Inter,sans-serif;color:rgba(0,0,0,.75)}}
.stub{{aspect-ratio:651/907;background:#d5dbd9;display:flex;align-items:center;justify-content:center;font:14px Inter;color:#555;width:100%}}</style>{links}
<style>.one-product-wrapper{{background:{st['bg_color']};padding-top:{st['padding_top_desktop']}px;padding-bottom:{st['padding_bottom_desktop']}px}}
@media(max-width:749px){{.one-product-wrapper{{padding-top:{st['padding_top_mobile']}px;padding-bottom:{st['padding_bottom_mobile']}px}}.one-product-grid,.one-product-grid.reverse{{flex-direction:column}}.one-product-blocks{{grid-template-columns:1fr}}}}
.highlight{{color:{st['highlight_color']}}}</style>{anchor}</head><body>
<section id="sec" class="one-product-wrapper"><div class="page-width"><div class="one-product-grid">
<div class="one-product-image"><div class="stub">section photo (stand-in)</div></div>
<div class="one-product-content"><h2 class="heading-h2">{pre}<span class="highlight">{hi}</span>{post}</h2>
<div class="one-product-subheading">{st['subheading']}</div><div class="one-product-badge">{st['badge_text']}</div>
<div class="one-product-blocks">{blocks}</div><a href="#" class="btn-globel btn-globel--solid">{st['button_text']}</a></div></div></div></section></body></html>"""
open(out, 'w').write(html)
