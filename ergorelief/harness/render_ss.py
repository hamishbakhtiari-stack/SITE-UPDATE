#!/usr/bin/env python3
"""Render single-support-section. Stand-ins: diagram = grey 1316x1195 box, main photo = grey 682x682 box.
Uses the section's own inline <style> verbatim (incl. its stray '}' which kills the 767px block)."""
import json, re, sys
tpl, key, out, theme, fonts, liq = sys.argv[1:7]
t = json.load(open(tpl)); s = t['sections'][key]; st = s['settings']
L = open(liq).read().replace('\r', '')
style = L[L.index('<style>'):L.index('</style>') + 8]
for k in ('bg_color', 'padding_top_desktop', 'padding_bottom_desktop', 'padding_top_mobile', 'padding_bottom_mobile'):
    style = style.replace('{{ section.settings.%s }}' % k, str(st[k]))
feats = ''.join(f'<div class="feature-item"><div class="feature-icon">✓</div><div class="feature-content"><p>{s["blocks"][b]["settings"]["feature_text"]}</p></div></div>'
                for b in s['block_order'] if not s['blocks'][b].get('disabled'))
diag = '<div class="support-image"><div style="aspect-ratio:1316/1195;max-width:350px;width:100%;margin:0 auto;background:#cfd8d5;display:flex;align-items:center;justify-content:center;font:13px Inter;color:#555">diagram (stand-in)</div></div>' if st.get('support_image') else ''
main = '<div class="main-product-image"><div style="aspect-ratio:1;max-width:400px;width:100%;background:#d5dbd9;display:flex;align-items:center;justify-content:center;font:13px Inter;color:#555">photo (stand-in)</div></div>' if st.get('main_image') else ''
sub = f'<span class="single-subheading">{st["subheading"]}</span>' if st.get('subheading') else ''
desc = f'<div class="section-description">{st["description"]}</div>' if st.get('description') else ''
btn = f'<a class=" btn-globel btn-globel--solid">{st["button_text"]}</a>' if st.get('button_text') else ''
ff = ''.join(f"@font-face{{font-family:{f};font-weight:{w};src:url({fonts}/fontsource-{f.lower()}/files/{f.lower()}-latin-{w}-normal.woff2)}}" for f in ('Poppins','Inter') for w in (400,500,600,700))
links = ''.join(f'<link rel="stylesheet" href="{theme}/assets/{c}">' for c in ('base.css','cstm-style.css','resposive.css','custom.css'))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}:root{{--font-body-family:Inter;--font-heading-family:Poppins;--font-body-scale:1;--font-heading-scale:1;--color-foreground:0,0,0;--page-width:140rem}}*,*::before,*::after{{box-sizing:border-box}}html{{font-size:62.5%}}body{{margin:0;font-size:1.5rem;line-height:1.8;font-family:Inter}}</style>{links}</head><body>
<section id="sec" class="single-support-section"><div class="page-width"><div class="single-support-wrapper"><div class="single-support-left">{diag}{main}</div>
<div class="single-support-right"><h2 class="heading-h2">{st['heading']}</h2>{sub}<div class="feature-list">{feats}</div>{desc}{btn}</div></div></div></section>{style}</body></html>"""
open(out, 'w').write(html)
