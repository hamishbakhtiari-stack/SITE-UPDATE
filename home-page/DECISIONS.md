# Home page (templates/index.json) — decisions log

## Setup — 2026-09-21

| | |
|---|---|
| Live theme at start | `164124164353` — "SitComfort — Collection page CRO (Claude, DO NOT PUBLISH)" (role MAIN) |
| Working theme | **`164208705793`** — "SitComfort — Home page CRO (Claude, DO NOT PUBLISH)" (UNPUBLISHED) |
| Target file | `templates/index.json` — 18026 bytes, md5 `5d7e33bffcd39ae15a15d3903fe7b8a0` |
| Baseline on disk | `home-page/baseline/templates.index.json` — byte-identical, md5 verified against Shopify |

The working theme is a `themeDuplicate` of the live theme, so every file starts byte-identical.
`templates/index.json` in the duplicate returns the same checksum as live — copy verified, not assumed.

Note: the live theme is **no longer** `164061970689` (the ComfortBundle PDP working theme named in
`references/theme-map.md`). That theme map's "working theme" line is stale; its CSS/quirk notes still hold.

## Page structure as found (10 sections, page order)

| # | Key | Type | Section file | Shared with |
|---|---|---|---|---|
| 1 | `custom_hero_section_Yh4kcV` | custom-hero-section | `custom-hero-section.liquid` (7928 B) | home only (to verify) |
| 2 | `benefit_section_xTeUz3` | benefit-section | `benefit-section.liquid` (3157 B) | home only (to verify) |
| 3 | `image_text_TcNMzf` | image-text | `image-text.liquid` (5166 B) | home only (to verify) |
| 4 | `how_it_works_btbqYq` | how-it-works | `how-it-works.liquid` (4233 B) | home only (to verify) |
| 5 | `comparison_section_ytnPWC` | comparison-Section | `comparison-Section.liquid` (8867 B) | distinct from the PDP's `comparison-products` |
| 6 | `7days_9YMijn` | 7days | `7days.liquid` (8440 B) | **also on the PDP** — settings `{}`, all content hard-coded in the file |
| 7 | `video_reviews_wrtQVD` | video-reviews | `video-reviews.liquid` (8892 B) | **also on the PDP** |
| 8 | `feature_highlight_J9ftbk` | feature-highlight | `feature-highlight.liquid` (6058 B) | **also on the PDP** |
| 9 | `faq_XyiMyE` | FAQ | `FAQ.liquid` (8069 B) | **also on the PDP** |
| 10 | `cta_section_G9JXf9` | CTA-section | `CTA-section.liquid` (4321 B) | **PDP and `page.about-us`** |

Five of ten section files are shared with the PDP. Any change to those `.liquid` files needs an
opt-in setting (the `center_layout` checkbox pattern), never a hard-coded change. Blast radius is
to be re-verified by grepping every template before touching any section file.

## Closed topics (carried over — do not reopen)

- **Pricing / anchoring / value-stacking.** Permanently closed.
- **Consumer law.** Permanently banned, in copy and in conversation.
- **Return postage.** Never state who pays.
- **Ethics commentary on the three written review cards.** Position stated; done.
- **Icons.** Never generate, substitute, restyle or recolour. His assets only.
- **Photography.** His. Cropping/sizing is layout and may be discussed.

## Parked observations (raise at the section, not before)

Found while taking the baseline. Not acted on.

- **§1 hero** — `guarantee_label` `<ul>` has stray whitespace: `<li> Express shipping…`, `<li> Easy returns      </li>`.
- **§1 vs §9/§10** — "Start your 7-**D**ay Reset" (hero) vs "Start your 7-**d**ay reset". Fixed in the FAQ 2026-09-21; the CTA banner button is now "Get the full system" so the issue no longer applies there. Hero still to review at §1.
- **§2 benefits** — heading has stray spaces inside the span: `quietly <span>  straining </span>   your body.`
- **§5 comparison** — `LumbarEase™ ` card title has a trailing space.
- **§7 video reviews** — Sarah L.'s quote opens with a straight `"` and never closes; the other two use curly `“ ”`.
- ~~**§9 FAQ** — retired names "7-Day SitComfort Reset Program" / "7-Day SitComfort Reset".~~ Resolved 2026-09-21: answers replaced with the PDP's.
- ~~**§9 FAQ** — `non‑slippery` contains U+2011.~~ Gone with the rewritten answer, 2026-09-21.
- ~~**§10 CTA banner** — `30-day  money back guarantee` double space.~~ Resolved 2026-09-21: subheading replaced with the PDP's.

## Changes shipped

### 2026-09-21 — §5 "Engineered for real support" — review findings (NOTHING CHANGED YET)

Reviewed on request. No push. `comparison-Section.liquid` (8867 B, **CRLF**) is a different file
from the PDP's `comparison-products.liquid` and the collection's `comparison-table.liquid`.
Blast radius not yet fully verified — **grep every template before editing it.**

**1. The subheading is contradicted by the store's own sales data.** "Most customers choose the
full system for complete relief." ShopifyQL, last 730 days, grouped by product:

| product | orders | gross |
|---|---|---|
| ErgoRelief™ Seat Cushion | 72 | $4,872.40 |
| LumbarEase™ Lumbar Support | 68 | $3,999.60 |
| **ComfortBundle™ Complete System** | **0** | **$0** |

Not "fewer" — the bundle has never sold. This confirms the note carried out of the PDP project.
The claim should go or change; it is the highest-value fix in the section.

**2. Every card button opens a new tab.** The section hard-codes `target="_blank"` on the
`button_url` branch. All three cards set `button_url`, so all three hit it. The `{% elsif %}`
fallback to `product.url` has **no** `target="_blank"`, keeps the custom `button_label`, and
resolves to the same URLs. **Clearing the three `button_url` values fixes this with no section
file change** — verified the destinations match (`shopify://products/<handle>` == `product.url`).

**3. The hand-picked card images never render, and the ones that do are 240px.**

```liquid
{% if product.featured_image != blank %}
  <img src="{{ product.featured_image | img_url: 'medium' }}" ...>
{% else %}
  <img src="{{ block.settings.image | image_url }}" class="pro-img" ...>
```

All three products have featured media (1024x1024, 682x682, 682x682), so
`ErgoRelief.webp` / `ComfortBundle.webp` / `LumbarEase.webp` in the block settings are dead
settings. And `img_url: 'medium'` is Shopify's fixed **240x240** named size, upscaled into a
~380px card — roughly 1.6x on a 1x screen, ~3.2x on a 2x phone. Also the deprecated `img_url`
filter, with no `srcset`, `sizes` or `loading="lazy"`, unlike every other image in the theme.
Fixing this needs a section file edit.

**4. `title` overrides are dead too.** `{% if product.title != blank %}` wins, so the headings
render as full product titles, not the short names in the settings:
"ComfortBundle™ Complete System" above the subtitle "Complete support system" — the same words
twice. Same for the other two. (Also makes the `LumbarEase™ ` trailing-space parked item moot.)

**5. Feature lists are lopsided and vague.** ErgoRelief 2, ComfortBundle 4, LumbarEase 2, with
blank slots 3-5. Copy is generic — "Pressure relief", "Lower body alignment" — against the PDP's
"High-density memory foam — holds its shape instead of flattening over time".

**6. Latent:** the sale badge `<span>` renders unconditionally and is only filled when a
compare-at exists, so removing a compare-at price would leave an empty badge chip. All three are
on sale today, so it is not currently visible.

**7. Minor:** `padding_top_desktop` 50 vs `padding_bottom_desktop` 100 — asymmetric, and the
section above it closes with 100, so there is a 150px gap above and 100px below.

Live values the cards read: ErgoRelief $71 (was $89), 5.0 from 15 reviews · ComfortBundle $117
(was $168), 4.98 from 50 · LumbarEase $62 (was $79), 5.0 from 15.

**Unverified:** the star-rating markup outputs `product.metafields.reviews.rating.value` in one
place and the bare `product.metafields.reviews.rating_count` metafield object in another. Whether
those render as numbers or as a raw JSON blob needs a look in preview — not asserted either way.

Pricing/anchoring deliberately not discussed: closed topic.

### 2026-09-21 — Judge.me badge removed from the home page (CLOSED)

It rendered "No reviews". Cause: the Judge.me **preview badge** reads its rating from the product
in scope. On the PDP that is ComfortBundle (47 reviews, 4.98 avg). `templates/index.json` has no
product context, so the block falls through to its empty state and prints "No reviews" — worse
than showing nothing, on the one section whose whole job is social proof.

Deleted rather than disabled: its `settings` were `{}`, so there was nothing to preserve, and it
can never work on this template. The build script asserts `settings == {}` before deleting.

5 of 311 keys changed. Verified: 18993 bytes, md5 `0338f0ea79ccd2158402da5e05d8418e`.
Grep confirms no `judge` reference remains anywhere in the home template.

**Closed topic: no Judge.me preview badge on the home page.** Recorded in `locked.json` too. If a
star rating is ever wanted there it needs a shop-level widget (Judge.me's "all reviews"/shop
rating), not the product preview badge.

Lesson for this project: an `@app` block that works on one template is not portable to another.
Check what context the app block reads before copying it across.

### 2026-09-21 — §7 "Real people. Real relief." brought across from the PDP

Template JSON only. `video-reviews.liquid` hard-codes its `vr-v2` class, so the home page was
already getting the v2 styling — no section file change needed, zero blast radius.
14 of 313 keys changed. Verified: 19238 bytes, md5 `15d90726c25ee00b668254719679a668`.

#### The videos were the real find

The Files API settles an open question carried out of the PDP project (`WIKI.mp4` / `HOLLIE2.mp4`
"unconfirmed — needs a click in preview"). Both exist and are READY. More importantly, the home
page was pointing at the **.MOV** originals, which Shopify only ever transcoded to a single
low-res rendition:

| | home was | home now | renditions |
|---|---|---|---|
| Wiki | `Wiki.MOV` | `WIKI.mp4` | **268x480 only** → 270x480, 404x720, **606x1080**, m3u8 |
| Hollie | `Hollie.MOV` | `HOLLIE2.mp4` | **268x480 only** → 270x480, 404x720, **606x1080**, m3u8 |
| Helen | `Helen.mp4` | unchanged | already the good one |
| Luiza | `Luzio_8b8fc2d5….mp4` | `Luzio.mp4` | see below |

`video-reviews.liquid` deliberately picks the **widest** mp4 source for the popup
(`best_src` loop, with a comment explaining Shopify lists SD first). On the home page that loop
had nothing to choose from — one 268px rendition — so Wiki and Hollie were playing at 268px wide
in a popup sized to `max-width:92vw`. They now play at 606x1080. Durations match (48s / 49s), so
it is the same footage re-uploaded, not a different take.

**Luiza is a genuinely different cut, not just a better encode.** Home was on the 84s version;
the PDP's `Luzio.mp4` is **126s**. Both READY, both full-rendition. The PDP's is what shipped
there, so it came across — but 126s is long for a home-page testimonial and this is a content
choice, not a technical one. **Flagged for Hamish.** The 84s cut also exists as
`Luzio_07927f04-8bb2-4fc2-9899-168a063ba00b.mp4` if he wants it back.

#### Everything else

- **Name chips added.** The section has a `name` setting per video that renders a `.vr-name` chip
  on the thumbnail; home had never set it. Now Luiza / Wiki / Hollie / Helen, as on the PDP. It
  also feeds the thumbnail's `alt` (`vr_alt = block.settings.name | default: 'Customer video review'`),
  so this improves accessibility too.
- ~~**Judge.me preview badge added**~~ — **reverted the same day**; it rendered "No reviews" on
  the home page. See the entry above.
- **Sarah L.'s quote now closes.** Home had an opening `"` and no closing one — resolves a parked
  item from the baseline.
- `bg_color` `#fafafa` → `#f4f6f5`, the PDP's.
- **Thumbnails, review images, names and bios: unchanged**, asserted in the build script.

Parked, still true: `wiki.webp` and `Hollie.webp` were cut from the older low-res videos, so the
thumbnails may look softer than the new 606x1080 footage behind them. Hamish's call — photography
is his. Also still open from the PDP project: "Wiki" may be a handle rather than a name.

Not visually verified — no render, and the Judge.me block will not render in a local harness.

### 2026-09-21 — §8 feature grid: 2 x 2 on desktop, via an opt-in setting

Hamish: keep the bundle content, *"ONLY MAKE SURE THE LAYOUT IS SIMIALR, IT SHJOULD BE 2X2 IN DESKTOP"*.

`feature-highlight.liquid` is shared by at least the home page, the ComfortBundle PDP and the
collection page, so this used the `center_layout` pattern rather than a hard-coded change:

- new setting `two_up_desktop`, a checkbox, **default `false`**
- when on, the section gets an extra `fh-v2` class and emits
  `@media (min-width:992px){ .feature-highlight-section.fh-v2 .feature-grid{ grid-template-columns:repeat(2,1fr)!important } }`
  from its own `<style>` block
- the rule is wrapped in `{% if %}`, so pages that don't opt in emit no extra CSS at all
- `templates/index.json` sets `two_up_desktop: true`; nothing else does

Specificity 0,3,0 plus `!important`, and the section's inline `<style>` loads after the head CSS,
so it wins. The rule itself is not invented — it is the one already proven on the PDP (inside
`custom_liquid_heroAnchor`), just scoped to an opt-in class instead of applying globally.

Verified after push:

| file | size | md5 | |
|---|---|---|---|
| `sections/feature-highlight.liquid` | 6621 | `68e918922f1c1b5fa719acc55871bdf7` | matches local |
| `templates/index.json` | 18911 | `d34673154956c18cf0af49f882c4546f` | matches local, 1 key changed |
| `templates/product.ComfortBundle.json` | 39409 | `ee9abc8743cd84586ba9d9286e1aa26d` | unchanged |
| `templates/collection.json` | 12354 | `4ced7bb043407d51fbd415e54ad3b6fd` | unchanged |
| `templates/collection.custom-collection.json` | 12454 | `2eab3a44c434d9e73e699e91edbb4249` | unchanged |
| `templates/product.ergoRelief.json` | 27848 | `241b858f2101b3279f121f2c7ec3f25e` | unchanged |
| `templates/product.lumbarEase.json` | 27882 | `b8396197463a1c7778a3dc96da5677c4` | unchanged |

The section file's pre-existing `{% if template == 'product.ComfortBundle' %}` image branch was
left exactly as it was — it is a hard-coded template check and the wrong pattern, but changing it
was out of scope here. **Parked** for whenever §8 image sizing comes up.

**Not visually verified.** The rule is the PDP's proven one, but no render was taken. Still open
on this section: the PDP also constrains the main image (260px on phones, 14px radius) and swaps
features 3 and 4 for generated SVG icons. Neither was carried over — the image sizing because it
would change mobile height and that needs measuring first, the icons because substituting his
icons is a standing "never".

Note: the collection page's own feature-highlight still has six features and the
"Designed for People / Who Sit All Day" heading. Untouched, and `two_up_desktop` is off there.

### 2026-09-21 — §8 Feature Highlight brought across from the PDP

Home's "Designed for people / who sit all day" is the same section *type* as the PDP's
"Australian, / end to end" (`feature-highlight`). Hamish asked for the PDP's version, so the
content came across: heading, subheading, main image + alt text, and the four Australian trust
features in the PDP's render order.

18 of 306 keys changed, all inside `feature_highlight_J9ftbk`. `order` unchanged.
Verified: 18879 bytes, md5 `f211fda23ef3e9828ed2333b434e156f`, matching on re-read.

**Blocks were mapped by the icon each one already holds, so not a single icon path changed** —
asserted programmatically in the build script, not by eye:

| home block | icon (unchanged) | was | now |
|---|---|---|---|
| `feature_dXanbn` | `Mask_group_1.png` | Fast shipping from Australia | Ships from Sydney |
| `feature_nY8GdY` | `Mask_group_5.png` | Satisfaction guarantee | Returns go to Sydney, not overseas |
| `feature_UDAbBF` | `Mask_group_2.png` | 30 Days Risk - Free Trial | 30 days to change your mind |
| `feature_VgjLa6` | `Mask_group_3.png` | Built for Desk Workers | Australian customer support |
| `feature_ichrJD` | `Mask_group.png` | Ergonomic Designed | **disabled** |
| `feature_ACCmT7` | `premium-memory-foam-icon.png` | Premium Memory Foam | **disabled** |

Six features down to four, matching the PDP. The two that dropped are disabled, not deleted, so
they stay in the theme editor and can be switched back on.

Settings: `main_image` `Designer_32_1_2_1.webp` → `6-1.webp`; `corner_image` `corner-image.png` →
`corner-image.webp` (the PDP's asset); `image_alt` added (the section supports it and home had
none — a real accessibility/SEO gain); heading, heading_span and subheading now the PDP's.
Background and all four padding values were already identical, so they were left alone.

#### It will NOT look identical to the PDP, and here is exactly why

The PDP's appearance for this section does not come from the section file. It comes from CSS
inside `custom_liquid_heroAnchor`, a block in the PDP's `main` section, which the home page does
not have. `assets/custom.js` is empty and there is no global equivalent. The PDP-only rules are:

```
@media (min-width:992px){ .feature-highlight-section .feature-grid{grid-template-columns:repeat(2,1fr)!important} }
@media (max-width:749px){ .feature-highlight-section .feature-main-image{max-width:260px!important; margin:auto} }
.feature-highlight-section .feature-main-image img{border-radius:14px!important}
.feature-grid .feature-item:nth-child(3) .feature-icon img{content:url("data:image/svg+xml,…30-calendar…")!important}
.feature-grid .feature-item:nth-child(4) .feature-icon img{content:url("data:image/svg+xml,…envelope…")!important}
```

On top of that, `feature-highlight.liquid` itself branches on the template:

```liquid
{% if template == 'product.ComfortBundle' %}   …constrained 260/380px image tag…
{% else %}                                     …plain full-width image tag…
```

So on the home page: the image renders full width with no 14px radius, the feature grid uses the
theme default rather than a forced 2-up, and **features 3 and 4 show Hamish's own
`Mask_group_2.png` and `Mask_group_3.png` instead of the generated 30-calendar and envelope SVGs
the PDP substitutes in**.

The icon difference was left as-is deliberately: substituting his icons for generated SVGs is a
standing "never". If he wants the PDP's exact look, the layout rules can be carried over without
touching the shared section file — a `custom-liquid` section on the home page holding a scoped
`<style>`, the same mechanism `sc_trust_strip` uses on the PDP. **Not done; needs his call.**

### 2026-09-21 (later) — every home-page buy CTA goes to the product page, not the cart

Hamish: *"cta in home page should direct them to product biundle page this should apply for all
CTAs here"*. This reverses the `/cart/add` decision from earlier the same day. **Closed topic:**
the home page sends people to the ComfortBundle product page; it does not add to cart directly.

Audited every link setting on the page. Only two needed changing — the rest already pointed at the
product page:

| section | setting | action |
|---|---|---|
| `custom_hero_section_Yh4kcV` | `btn_primary_url` | already the bundle page — unchanged |
| `custom_hero_section_Yh4kcV` | `btn_secondary_url` | `#Howit_works` — an on-page scroll anchor for "See how it works", not a buy CTA. Left alone. |
| `image_text_TcNMzf` | `button_link` | already the bundle page — unchanged |
| `how_it_works_btbqYq` | `button_link` | already the bundle page — unchanged |
| `comparison_section_ytnPWC/card_QeERNL` | `button_url` | `shopify://products/ergorelief` — the ErgoRelief card's own "View ErgoRelief™" button. Left alone; pointing it at the bundle would be wrong. |
| `comparison_section_ytnPWC/card_gCtPhR` | `button_url` | already the bundle page — unchanged |
| `comparison_section_ytnPWC/card_Uq9cab` | `button_url` | `shopify://products/lumbarease` — same reasoning as the ErgoRelief card. Left alone. |
| **`faq_XyiMyE`** | **`button_link`** | **`/cart/add?…` → `shopify://products/comfortbundle-complete-system`** |
| **`cta_section_G9JXf9`** | **`button_link`** | **`/cart/add?…` → `shopify://products/comfortbundle-complete-system`** |

2 of 303 keys changed. `order` unchanged. Verified: 18517 bytes,
md5 `ad639d51866b14f55232f8814c2741aa`, matching on a fresh read from Shopify.

Side effect worth noting: the cart-drawer question from the previous entry is now moot on the home
page. Nothing there adds to cart, so there is no drawer-vs-page-load difference to resolve, and no
reason to put the delegate script on the home page.

Guard updated in the same commit — both links are now locked to the product page URL.

### 2026-09-21 — CTA banner + FAQ brought across from the ComfortBundle PDP

Pushed to working theme `164208705793`. Template JSON only; **no section file was touched**, so
the PDP and About Us are byte-identical to before. 22 keys changed out of 303. `order` unchanged.

Verified: local `templates/index.json` 18529 bytes md5 `06ec85986eda96947a6ad97535e5a98d`;
Shopify reports the same size and checksum on re-read. Live theme still 18026 / `5d7e33bf…`.

A load/dump round-trip of the live file reproduced Shopify's own bytes exactly, so the 22 key
changes are provably the only byte differences in the file.

**CTA banner** (`cta_section_G9JXf9`) — now matches `cta_section_tEApVF` on the PDP:

| setting | was | now |
|---|---|---|
| `bg_color` | `#0d5c52` | `#0e6b5b` |
| `heading` | Reset your sitting. Reclaim your comfort. | Reset your sitting. `[br]`Reclaim your comfort. |
| `subheading` | Express shipping from Australia · 30-day  money back guarantee · Easy returns | Free express shipping from Sydney · `[br]`2–3 business days · 30-day money-back guarantee |
| `button_text` | Start your 7-day reset | Get the full system |
| `button_link` | `shopify://products/comfortbundle-complete-system` | `/cart/add?id=49378080227585&quantity=1&return_to=/cart` |
| `center_layout` | (absent → false) | `true` |
| `corner_image` | `shopify://shop_images/Mask_group_6.png` | `""` |

`corner_image` was blanked because the PDP banner has none. The original value is recorded here;
re-picking it in the theme editor restores it. Padding was already identical on both pages.

**FAQ** (`faq_XyiMyE`) — the questions were the same on both pages, so the PDP's version came
across whole. Home's five questions all existed on the PDP (only difference: a curly `’` vs a
straight `'` in "What's included in the 7-Day Reset?"). The PDP had a sixth,
"How do I access the 7-Day Reset?", which is now on the home page too.

All six answers are the PDP's. Home's existing block IDs were reused rather than recreated, so
nothing keyed to them can break; only the new question needed a new ID (`faq_Mt6Leh`, same ID it
has on the PDP).

Also changed: `bottom_text` now links Contact us (`<a href="/pages/contact">`), `button_text`
"Start your 7-day reset" → "Start your 7-Day Reset" (fixes the retired lowercase naming),
`button_link` → the same `/cart/add` href, and `icon_style` `arrow` → `plus`.

`icon_style` is not only cosmetic: `FAQ.liquid`'s `.faq-v2` CSS rotates the `+` into a cross when
an item opens, but has no rule for the arrow SVG — so on the home page the arrow never moved and
gave no open/closed feedback. `plus` fixes that.

This retires the "7-Day SitComfort Reset Program" / "7-Day SitComfort Reset" wording that was in
the old home FAQ answers, and the U+2011 in "non‑slippery" is gone with the rewritten answer.

**Behavioural difference to be aware of.** *(Superseded later the same day — the home page no longer uses `/cart/add` at all. Kept for the record.)* The `/cart/add` href opens the cart *drawer* on the
PDP because `custom_liquid_cartDrawerAjax` (a block inside the PDP's `main` section) intercepts
it. That delegate does not exist on the home page, and `assets/custom.js` is empty, so there is
no global equivalent. On the home page the link is a plain navigation: Shopify adds the item and
lands the customer on `/cart`. It works and needs no JavaScript, but it is a page load rather
than a drawer. Putting the drawer on the home page would mean adding the delegate script as a
custom-liquid section — a separate, deliberate change, not bundled into this one.

**Guard updated in the same commit** (`home-page/locked.json`): both `button_link` values were
guarded against exactly this change, so they were re-pointed at the `/cart/add` href, and
`center_layout` / `icon_style` were added.

Not verified: rendered appearance. Needs a look in theme preview, or a harness render.

