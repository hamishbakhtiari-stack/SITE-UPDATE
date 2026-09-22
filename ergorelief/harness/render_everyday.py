#!/usr/bin/env python3
"""Render every-day-section for height measurement. Card images = grey 60px squares (stand-ins)."""
import json, sys
tpl, key, out, theme, fonts = sys.argv[1:6]
t = json.load(open(tpl)); s = t['sections'][key]; st = s['settings']
pre, rest = st['heading'].split('[', 1); hi, post = rest.split(']', 1)
cards = ''.join(f'<div class="every-day-card"><div class="every-day-card-image"><span style="display:block;width:60px;height:60px;background:#ccc"></span></div><h4>{s["blocks"][b]["settings"]["block_heading"]}</h4></div>' for b in s['block_order'])
ff = ''.join(f"@font-face{{font-family:{f};font-weight:{w};src:url({fonts}/fontsource-{f.lower()}/files/{f.lower()}-latin-{w}-normal.woff2)}}" for f in ('Poppins','Inter') for w in (400,500,600,700))
links = ''.join(f'<link rel="stylesheet" href="{theme}/assets/{c}">' for c in ('base.css','cstm-style.css','resposive.css','custom.css'))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}:root{{--font-body-family:Inter;--font-heading-family:Poppins;--font-body-scale:1;--font-heading-scale:1;--color-foreground:0,0,0;--page-width:140rem}}*,*::before,*::after{{box-sizing:border-box}}html{{font-size:62.5%}}body{{margin:0;font-size:1.5rem;line-height:1.8;font-family:Inter}}
.every-day-wrapper{{position:relative;overflow:hidden;background:{st['bg_color']};padding-top:{st['padding_top_desktop']}px;padding-bottom:{st['padding_bottom_desktop']}px}}@media(max-width:749px){{.every-day-wrapper{{padding-top:{st['padding_top_mobile']}px;padding-bottom:{st['padding_bottom_mobile']}px}}}}.highlight{{color:{st['highlight_color']}}}</style>{links}</head><body>
<section id="sec" class="every-day-wrapper"><div class="page-width"><h2 class="heading-h2">{pre}<span class="highlight">{hi}</span>{post}</h2><div class="notee-text"><p>{st['note']}</p></div><div class="every-day-grid">{cards}</div><div class="every-day-btn-wrap"><a class="btn-globel btn-globel--solid">{st['button_text']}</a></div></div></section></body></html>"""
open(out,'w').write(html)
