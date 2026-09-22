# ErgoRelief PDP — decisions log

Mirrors the ComfortBundle PDP redesign process (skill: shopify-page-update).

## Themes
- Live (MAIN): `164208705793` — "SitComfort — Home page CRO (Claude, DO NOT PUBLISH)" (currently published)
- **Working duplicate: `164269687041`** — "SitComfort — ErgoRelief PDP CRO (Claude, DO NOT PUBLISH)", created 2026-09-22 via `themeDuplicate`. All writes go here. Publishing is the owner's call.

## Target
- Product: ErgoRelief™ Seat Cushion, handle `ergorelief`, template suffix `ergoRelief`
- Template: `templates/product.ergoRelief.json` (live checksum `a27e12b15c0aab8999fc25fc68c87418`)
- Baselines in `baseline/` (as read, including Shopify's auto-generated banner comment).

## Closed topics (carried over — do not raise)
- Pricing / anchoring / value-stacking. Consumer law. Who pays return postage. Ethics commentary.
- Icons: use the owner's existing icons, never design or substitute.
- Photography is the owner's.

## Section inventory (live order)
| # | Key | Type | ComfortBundle equivalent |
|---|---|---|---|
| — | (none) | — | `sc_trust_strip` trust bar |
| 1 | `main` | main-product (19 blocks) | `main` (23 blocks) |
| — | `related-products` | disabled | disabled |
| 2 | `pws_image_with_text_U7pgnH` | pws_image_with_text | — |
| 3 | `one_product_PTdiHH` | one-product | same key |
| 4 | `7days_P3eEBF` | 7days | `7days_iAGRDU` |
| 5 | `every_day_section_jYJzBQ` | every-day-section (**enabled**) | disabled on CB |
| 6 | `single_support_section_QU6dHr` | single-support-section | — |
| 7 | `video_reviews_V3QqMX` | video-reviews | `video_reviews_K3ixGw` |
| 8 | `feature_highlight_kEKcXt` | feature-highlight (6 blocks) | same key (4 blocks) |
| 9 | `faq_bMxpUE` | FAQ (5 blocks) | same key (6 blocks) |
| 10 | `apps_JXNAik` | apps (Judge.me) | `177934200903caf21b` |
| 11 | `cta_section_tEApVF` | CTA-section | same key |

## Log
- 2026-09-22 — duplicated live theme; snapshotted ergoRelief + ComfortBundle templates. No writes yet.

## Section 1 — Hero (proposed 2026-09-22, awaiting approval)
Candidate: `candidate/product.ergoRelief.json`, built by `build_hero.py` (38 leaf diffs, all inside `main`; `order` unchanged; `main.block_order` reordered on purpose).
- Photo layout = ComfortBundle: `media_size` medium→small, 320px constrained height on mobile, 14px rounded corners. Same photo; the owner handles photography.
- Padding 52/100 → 8/24 (CB values).
- Hero anchor CSS = the hero part of CB's anchor only. CB's one-product / feature-highlight rules wait until those sections.
- Order: eyebrow pill → headline → title (small caps) → stars → price → body line → bullets → ATC.
- Headline: "Sit longer without the ache." (1 line at 26px; the old 72-char subtitle was 2 lines at 18px).
- Body: "Memory foam cushion, plus a 7-Day Reset plan to retrain how you sit."
- Bullets (all 1 line at 402px; before, 3 of 4 wrapped): Cut-out takes pressure off your tailbone / Contour cradles your hips and thighs / Anti-slip base stays put on any chair / 7-Day Reset builds the habit in a week. Fixes the retired "SitComfort 7-Day Reset programme".
- Quantity selector disabled. Evidence: 74 orders, all contain ErgoRelief; only 2 have qty>1 (#1051 ×2, #1087 ×3), and both are ErgoRelief+LumbarEase carts.
- Measured (harness, 402px iframe): ATC top 995 → 838px (−157px). The owner's phone shows the old title on 2 lines ("™" glyph width), which the harness renders on 1, so the real before is ~1049px and the real saving is likely larger.

## Parked (raise when we reach it)
- Cart-drawer CTA delegate (`custom_liquid_cartDrawerAjax`): add when we reach the first lower-page CTA.
- `system_preview_lock_text` (global) says Days 4–7 are "included with the ComfortBundle™" — check against ErgoRelief when we reach the 7-Day section.
