# SitComfort theme map

Store: sitcomfort.com.au — Dawn-derived theme, heavily customised.
Working theme during the PDP project: **unpublished duplicate `164061970689`**. Confirm the
current working theme ID before any write; do not assume this one is still the right target.

---

## Where things live

### CSS (load order matters — later wins ties)

| File | Loaded | Notes |
|---|---|---|
| `assets/base.css` | head | Dawn core. `html{font-size:62.5%}` so `1rem` = 10px |
| `assets/cstm-style.css` | head | ~54KB of store overrides |
| `assets/custom.css` | head | ~10KB more; **has rules the others don't** |
| `assets/resposive.css` | head | (sic — misspelled) breakpoint overrides |
| `assets/section-main-product.css` | section body | Dawn's PDP styles; **beats head files on ties** |
| `assets/component-price.css` | section body | price element sizing |

A section's own inline `<style>` loads after all of these, so it wins equal-specificity ties.
That is what makes the scoped-`v2`-class pattern work without `!important`.

### Breakpoints in use

`576px`, `749px`, `767px`, `989px`, `991px`, `992px` — inconsistent, and rules for the same
element frequently disagree across them. When something behaves oddly at one width, grep all six.

---

## Quirks that will waste your time if you don't know them

**`.bullte-points`** — the hero bullet wrapper class is spelled that way in the theme (typo,
`bullet` → `bullte`). Grepping for `bullet-point` finds the child items but not the wrapper.
The wrapper and item styles live in `assets/custom.css`, not `cstm-style.css`.

**The CTA delegate.** `custom_liquid_cartDrawerAjax` (a block inside `main`) installs a global
click handler that intercepts **every** buy CTA on the page and routes it through the hero's own
Add to Cart button so they all open the cart drawer. Its selector list:

```
a[href*="/cart/add"], button[id^="commanday-btn-"], button[id^="ergo-checkout-btn-"],
.every-day-btn-wrap a.btn-globel, .cta-banner-button-wrap a.btn-globel,
.custom-faq-bottom a.btn-globel, .system-preview-btn-wrap a.btn-globel
```

Consequences: (a) several CTAs have an empty `button_link` and still "work"; (b) it uses capture
phase + `stopImmediatePropagation` so older per-section handlers never run; (c) adding a new CTA
means adding its selector here or it will not open the drawer; (d) it falls back to `/cart` if
the drawer has not opened in 3s. **Give buttons a real href anyway** —
`/cart/add?id=<variant>&quantity=1&return_to=/cart` — so there is a working no-JS fallback
instead of `<a href="">`, which reloads the page.

**Stale template IDs in CSS.** Rules keyed to template IDs that no longer exist (e.g.
`img.chairId3_template--22109812392193__…`) silently do nothing. If a rule "should" be applying
and isn't, check for a dead template ID.

**Block-ID-keyed CSS.** `div#shopify-block-ATkRMa2FoTExLYjJUV__judge_me_reviews_preview_badge_Pg8JrN`
has margin rules. Recreating that block changes the ID and drops the styling.

**Sale vs regular price classes.** The ComfortBundle has a compare-at price, so the large visible
price is `.price-item--sale.price-item--last` and `.price-item--regular` is the **struck-through**
one. A rule targeting `.price-item--regular` does not do what its name suggests here. Check
`compareAtPrice` before reasoning about price styling.

**Section custom CSS has no reliable media-query support.** In template JSON, a section's
`custom_css` array uses `&` as the section selector but media queries are unreliable. Use
`clamp()` to scale with viewport instead.

**Liquid does not HTML-escape `{{ }}`.** HTML placed in a `text`/`textarea` setting renders as
HTML. Used to add a contact link to the FAQ with no code change.

---

## PDP section inventory (`templates/product.ComfortBundle.json`)

`order`, in page order:

| # | Key | Type | State |
|---|---|---|---|
| 1 | `sc_trust_strip` | custom-liquid | trust bar |
| 2 | `main` | main-product | hero (23 blocks) |
| — | `related-products` | related-products | **disabled** |
| 3 | `one_product_PTdiHH` | one-product | why it works |
| 4 | `full_system_g6H6MD` | full-system | what's included |
| 5 | `7days_iAGRDU` | 7days | 7-Day Reset preview |
| — | `every_day_section_jYJzBQ` | every-day-section | **disabled** (restated hero bullets) |
| 6 | `comparison_products_DgmnVi` | comparison-products | product specs |
| 7 | `video_reviews_K3ixGw` | video-reviews | testimonials |
| 8 | `feature_highlight_kEKcXt` | feature-highlight | Australian, end to end |
| 9 | `faq_bMxpUE` | FAQ | |
| 10 | `177934200903caf21b` | apps | Judge.me widget |
| 11 | `cta_section_tEApVF` | CTA-section | closing banner |

**Locked `main.settings`** (guarded by `check_template.py` — regressions here are bugs):
`media_size: small`, `constrain_to_viewport: true`, `media_fit: contain`,
`padding_top: 8`, `padding_bottom: 24`.

**Hero block order** matters: `custom_liquid_heroAnchor` must stay first (it carries the PDP's
entire custom `<style>` block), and `custom_liquid_cartDrawerAjax` second (the delegate).

---

## Sections shared with other templates

Always grep before editing a section file.

- `CTA-section.liquid` — used by the PDP **and** `page.about-us` (`cta_section_zX77qT`).
  Changes must be opt-in via a setting. The `center_layout` checkbox (default `false`) is the
  established pattern.
- `comparison-products.liquid` — verified PDP-only, safe to rewrite.
- `video-reviews.liquid` — section file; note there is *also* a `video_reviews` block type inside
  `main` rendering `snippets/video-reviews.liquid`. Two different components with similar names.

---

## Product facts

- **ComfortBundle™ Complete System** — handle `comfortbundle-complete-system`
- Single variant `49378080227585`, $117.00, compare-at $168.00
- Judge.me: 47 reviews, 4.98 average. Real review text lives in the
  `judgeme.review_widget_data` product metafield.
- Order history note: as of Sept 2026, **no order contains the bundle SKU** — all 72 orders since
  Jan 2025 are `ergorelief` + `lumbarease` as separate line items. Worth understanding before
  driving traffic to the bundle page.

---

## Open items carried out of the PDP project

- `WIKI.mp4` / `HOLLIE2.mp4` refs unconfirmed — needs a click in preview.
- `wiki.webp` / `Hollie.webp` thumbnails were cut from the older low-res videos.
- "Wiki" may be a handle rather than a name.
- Hero carousel: `video-link-1` and `video-link-5` are the same file (Helen plays twice).
- Judge.me section padding set blind with `clamp()`; may double up with the widget's own spacing.
- "Posture Quick-Reference Guide" is listed in section 4 and the Description accordion but does
  not exist yet.
- `system_preview_lock_text` still uses the short form "the Reset" (judged fine in context).
