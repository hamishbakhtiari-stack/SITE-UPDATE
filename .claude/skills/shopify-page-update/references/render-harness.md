# Rendering and measuring locally

The storefront is unreachable from this environment and `cdn.shopify.com` is blocked. So to see
what a change does, rebuild the fragment locally against the theme's **real** CSS files and
measure it. Done properly this is accurate to the pixel for layout and spacing. Done carelessly
it produces confident, wrong numbers — which is worse than no numbers.

---

## Setup

Chromium is pre-installed. On this image the binary is at:

```
/opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

`chromium` is **not** on `PATH` — calling it bare fails silently and leaves no screenshot, which
looks like a rendering problem and is not. Always use the full path.

Pull the theme's CSS to disk once and reuse: `assets/cstm-style.css`, `assets/resposive.css`,
`assets/custom.css`, `assets/section-main-product.css`, `assets/component-price.css`. Recreate
only the handful of `base.css` defaults you actually need (below) rather than pulling 82KB.

---

## THE TRAP: Chromium clamps window width to ~500px

```bash
# WRONG — silently renders at ~500px wide, not 390
chrome --headless --window-size=390,900 --screenshot=out.png page.html
```

Text wraps differently at 500px than at 390px, so every line count, element height and total
height you measure is wrong — and wrong in the flattering direction. A spacing estimate given to
the owner on this project was built on a clamped render and had to be corrected.

**Fix: render inside an iframe** sized to the real width, in an outer window ≥520px.

```html
<!-- f-390.html -->
<!doctype html><html><head><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}
iframe{width:390px;height:700px;border:0;display:block}</style></head>
<body><iframe src="page.html" scrolling="no"></iframe></body></html>
```

```bash
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$CH --headless --no-sandbox --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=560,700 \
    --virtual-time-budget=2000 --screenshot=raw.png f-390.html
python3 -c "from PIL import Image; Image.open('raw.png').crop((0,0,780,1400)).save('out.png')"
```

`--force-device-scale-factor=2` gives a retina-density image (crop to `width*2 × height*2`), which
is what makes it legible on the owner's phone.

---

## Measuring, not eyeballing

Screenshots tell you whether it looks right. Numbers tell you what changed. Get both.

Probe **through the iframe** (same clamping problem otherwise) with
`--allow-file-access-from-files` so the parent can reach the child document:

```html
<script>window.addEventListener('load',function(){
  var d0=document.getElementById('fr').contentDocument;
  var out=[]; var c=d0.querySelector('.product__info-container');
  [].forEach.call(c.children,function(el){
    var cs=d0.defaultView.getComputedStyle(el);
    var r=el.getBoundingClientRect();
    out.push((el.className||el.tagName)+' h='+Math.round(r.height)
             +' mt='+cs.marginTop+' mb='+cs.marginBottom
             +' fs='+cs.fontSize+' lh='+cs.lineHeight);
  });
  var atc=d0.getElementById('atc').getBoundingClientRect();
  var p=document.createElement('pre');
  p.textContent='PROBE ATCTOP='+Math.round(atc.top)+'\n'+out.join('\n');
  document.body.appendChild(p);});</script>
```

```bash
$CH --headless --no-sandbox --disable-gpu --allow-file-access-from-files \
    --window-size=560,1500 --virtual-time-budget=2500 --dump-dom probe.html \
    | sed 's/<[^>]*>//g' | grep -E 'PROBE|h='
```

This is how "tighten the spacing" became: *Add to cart moved from 581px to 432px; 91px of that was
the quantity block, 42px was bullets dropping from five lines to four, 8px the price line-height,
8px the body text.* That level of detail is what lets the owner make a real decision.

Track one **anchor metric** per layout question — here, the y-offset of the Add to Cart button.
Measure before, measure after, quote the delta.

---

## Getting the CSS environment right

**Include Dawn's box-sizing reset.** Omitting it produced a false "the button overflows on
mobile" report:

```css
*,*::before,*::after{box-sizing:border-box}
```

**Minimal `base.css` stand-in** (Dawn sets `html{font-size:62.5%}`, so `1rem` = 10px):

```css
html{font-size:62.5%}
body{margin:0;font-size:1.5rem;letter-spacing:.06rem;line-height:1.8;font-family:Inter,Arial,sans-serif}
.page-width{max-width:1400px;margin:0 auto;padding:0 5rem}
@media(max-width:749px){.page-width{padding:0 20px!important}}
```

**Extract the right `<style>` block.** A naive `liq.index("<style>")` once matched a tiny inline
style inside an SVG's markup, so none of the real CSS applied and the render showed cards
overlapping. Select the block by searching for a distinctive selector it contains
(e.g. `.vr-v2`), not by position.

**Load order matters and is not obvious.** `cstm-style.css` and `resposive.css` load in `<head>`;
`section-main-product.css` and `component-price.css` load in the section body and therefore win
ties. A section's own inline `<style>` is later still, so it wins equal-specificity ties against
all of them. Replicate that order in the harness or your specificity reasoning will be wrong.

---

## Known limits — say these out loud

- **App blocks cannot render** — Judge.me, Klaviyo, Microsoft Clarity. Anything styling them is
  unverified. Say so and ask the owner to eyeball it.
- **No webfonts** — the harness falls back to a serif. Fine for measuring boxes, misleading for
  judging type. Caption it.
- **Video refs cannot be resolved** — `shopify://files/videos/X.mp4` either works or silently does
  nothing. The owner has to click it in preview.
- **Placeholder shapes are not his assets.** Label them every time.

---

## Liquid-specific rendering gotchas

**`white-space: pre-line` and the output tag.** The FAQ answers are a `textarea` printed raw, so
newlines collapsed and formatting was lost. `pre-line` fixes it — but then the newline and
indentation *around* the Liquid tag render too. The output tag must sit inline with its container:

```liquid
<div class="custom-faq-answer">{{ block.settings.answer }}</div>
```

Not on its own indented line, or every answer gains a blank line top and bottom. Caught in the
render, before pushing.

**A `+` rotated 180° looks identical to a `+`.** The FAQ's open/closed indicator did nothing for
this reason. Rotate a plus by 45° to make a cross.

**`[br]` placeholders.** Some sections run `| replace: '[br]', '<br>'`. Put the separator *before*
the break (`Sydney · [br]2–3 days`), so line one ends on the separator rather than line two
opening with a dangling one. Trailing spaces are trimmed at a forced break, so `· [br]` renders
cleanly.
