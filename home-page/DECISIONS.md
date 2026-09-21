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
- **§1 vs §9/§10** — "Start your 7-**D**ay Reset" (hero) vs "Start your 7-**d**ay reset" (FAQ, CTA banner). The lowercase form is retired naming.
- **§2 benefits** — heading has stray spaces inside the span: `quietly <span>  straining </span>   your body.`
- **§5 comparison** — `LumbarEase™ ` card title has a trailing space.
- **§7 video reviews** — Sarah L.'s quote opens with a straight `"` and never closes; the other two use curly `“ ”`.
- **§9 FAQ** — uses retired names "7-Day SitComfort Reset Program" and "7-Day SitComfort Reset". Standard is "7-Day Reset" / "7-Day Reset Program".
- **§9 FAQ** — `non‑slippery` contains U+2011 (non-breaking hyphen). Preserve it byte-for-byte unless deliberately changed.
- **§10 CTA banner** — `30-day  money back guarantee` has a double space; PDP wording is "money-back".

## Changes shipped

_None yet._
