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

**Behavioural difference to be aware of.** The `/cart/add` href opens the cart *drawer* on the
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

