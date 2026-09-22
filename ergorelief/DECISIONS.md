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

## Section 1 — Hero (APPROVED + PUSHED 2026-09-22)
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
- Owner, 2026-09-22: "Ergo Relief doesn't have free shipping." Standing fact. `build_hero.py` now fails if any free-shipping wording shows up in the template. Checked: the template has none (trust row says "Express shipping from Australia"; the Shipping tab doesn't say free).
- Reset tab (`collapsible_tab_fri6mY`): "included free with every ComfortBundle™" → "included with every ErgoRelief™". Approved.
- PUSHED to working theme 164269687041 at 2026-09-22T20:34Z via `themeFilesUpsert` type URL (raw GitHub file at commit daa1935), so nothing was retyped by hand. Verified: checksumMd5 `aecffb111d6cf9b802f7db8f39e1d518` = local md5sum, size 30161 = local. Live theme 164208705793 still `a27e12b1…` (untouched). Guard `locked.json` PASS. 39 leaf diffs.
- New baseline for section 2 onward = `candidate/product.ergoRelief.json`.
- Owner to eyeball in preview: Judge.me stars spacing; the `free-ship.png` icon artwork.

## Section 2 — Image with text `pws_image_with_text_U7pgnH` (APPROVED + PUSHED 2026-09-22)
Owner: "give it a job". Job = the "softness isn't the fix" argument (from his product description). Template settings only; the section .liquid (CRLF) is shared with LumbarEase and was not touched.
- Heading "ErgoRelief™ Seat Cushion" (repeated the page title) → "Softness isn't the fix." Eyebrow "Why ErgoRelief™ Feels Different" kept.
- Intro → "Extra foam only softens the same pressure points. ErgoRelief™'s contour and cut-out change where your weight lands, so the ache doesn't build 20–30 minutes in."
- 4 icon bullets disabled (all restated hero bullets; one used the retired "SitComfort… programme").
- CTA bug fixed: "Buy ErgoRelief™" linked to this same page (reload, nothing added). Now "Add ErgoRelief to cart" → `/cart/add?id=48771729031425&quantity=1&return_to=/cart` (works without JS).
- Added `custom_liquid_cartAddLink` to main (2nd block): ONLY the AJAX /cart/add script from CB's delegate block, so /cart/add links open the drawer. The full CB capture-phase delegate was NOT ported: its selectors (`.every-day-btn-wrap`, `.cta-banner-button-wrap`, `.custom-faq-bottom`…) would make the lower "Get the Full System" (ComfortBundle) buttons add ErgoRelief instead.
- Measured (harness, 402px): section 998 → 766px mobile (−232px). Photo unchanged (can't view it from here).
- PUSHED via themeFilesUpsert URL (commit da446b5). Verified checksumMd5 0b4f2bcf0da6efce42b58373b9cd4362 = local, size 31967. Live untouched (a27e12b1…). Guard PASS. 32 leaf diffs.
- Owner to check in preview: tap the button → drawer opens with ErgoRelief.

## Parked (added)
- `single_support_section_QU6dHr` button "Add ErgoRelief™ To Cart" links to `shopify://products/ergorelief`, the same bug as section 2. Fix when we reach it.

## Section 0 — Trust strip `sc_trust_strip` (PUSHED 2026-09-22)
Owner caught it: the ComfortBundle top bar was missing on ErgoRelief (I raised it at the start, then left it out of the hero push without saying so).
- Copied from CB with one change: "Free shipping" → "Express shipping" (ErgoRelief doesn't ship free). Text: "Sydney dispatch · Express shipping · 30-day money-back".
- Mobile +29px (1 line at 402px, 10.5px uppercase, same styling as CB). ATC in harness 838 → 867.
- `locked.json` now also requires `first_section: sc_trust_strip`.
- PUSHED (commit 63d5ee9). Verified checksumMd5 d2daa6ee7c3830d7b1c05f70a4914aa2 = local, size 32528. Live untouched.

## Section 3 — One product `one_product_PTdiHH` (PUSHED 2026-09-22)
Owner: "bring most of the content here from bundle page, only title can stay unchanged".
- From CB: subheading, badge ("Hips, lower back and spine in one line"), 4 blocks (Pressure off your tailbone / Your lower back keeps its curve / One makes the other work / Then it sticks), button text, and CB's one-product mobile CSS (heading+sub first, image at 70%, compact icon rows, CB's teal block icons), appended to ER heroAnchor.
- Kept from ER: heading "Why [One Product] Isn't Enough"; section photo Designer_5 (his; 651×907, same ratio as CB's); button_link → ComfortBundle page (on CB the button adds the bundle itself); white bg (section 2 directly above is #f4f6f5, so CB's grey would merge them).
- My one deviation: CB copy says "the lumbar support" / "the contoured cut-out" (the bundle buyer owns both). On ErgoRelief the reader doesn't, so named them: "ErgoRelief™'s contoured cut-out…", "LumbarEase™ holds it there…", "…lets LumbarEase™ do its job."
- Measured (harness, 402px): 1722 → 1401px mobile (−321px).
- PUSHED (commit 5b2ea51). Verified checksumMd5 81769fc16cb48190692381472b8c455c = local, size 36325. Live untouched. Guard PASS (added one-product CSS to css_must_contain).
- CORRECTION (owner, 2026-09-22): "section 3 in ErgoRelief is not about ErgoRelief, it is about bundle and encouraging people to click to CTA and go to bundle page." My product-naming edits were wrong: they turned a bundle pitch into ErgoRelief copy. Reverted to CB blocks verbatim, and the section photo is now CB's Designer_4. Only differences from CB now: heading (kept), button_link (→ bundle page), bg white.
  RULE: on single-product pages, section 3 is the BUNDLE upsell. Write for the bundle, not the page's product.
- RE-PUSHED (commit a525d5c). Verified checksumMd5 ae0829d22afc3214c5fde4204c06d9f0 = local, size 36323. Live untouched.
- Subheading (owner approved, 2026-09-22): "The ComfortBundle™ pairs this cushion with LumbarEase™ lumbar support — so seat and spine are supported together, then reinforced over 7 days." It names the bundle so a first-time reader knows what "the lumbar support" in the blocks means, and it stays bundle copy. Evidence: 69 of 74 orders already contain ErgoRelief + LumbarEase, as separate line items.
- PUSHED (commit 45d8418). Verified checksumMd5 9ca24cbf8b0ffab70d01af2de40f6bb7 = local, size 36319. Live untouched.
