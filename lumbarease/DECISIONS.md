# LumbarEase PDP — decisions log

Same process and treatment as ErgoRelief (see ../ergorelief/DECISIONS.md, including its closed topics and rules).
Working theme: **164269687041** (the same unpublished copy as ErgoRelief, so both go live in one publish). Live: 164208705793.
Product: LumbarEase™ Lumbar Support, handle `lumbarease`, variant 48772058022145, $62 (compare-at $79). Not free shipping.
Baseline: `baseline/product.lumbarEase.json` (live = working checksum 4635b2742ba60225a979da2a954ae2dd at start).
The template structure is identical to the original ErgoRelief page (same section types, same order).

## Hero + trust strip (PUSHED 2026-09-23)
Owner: "start with the hero section and do exactly the same as ErgoRelief".
- Same layout/CSS as ErgoRelief/ComfortBundle: media_size small, padding 8/24, 320px photo, 14px corners, hero anchor CSS (badge rule keyed to UtwgBq), eyebrow pill, quantity disabled (69 of 74 orders contain LumbarEase; only 2 multi-unit, both two-product carts).
- Headline: the old one was ErgoRelief's line ("Reduce seat pressure and stay comfortable…") on the LumbarEase page. New: "Stop slumping by 2pm." (the owner's own sign-off in the product description; 1 line at 26px).
- Body: "Memory foam lumbar support, plus a 7-Day Reset plan to retrain how you sit."
- Bullets (all 1 line at 402px; before, 2 of 4 wrapped): Curve holds your lower back in place / Fills the gap your chair leaves / Adjustable straps stop it sliding down / 7-Day Reset builds the habit in a week. Removes the retired "SitComfort… programme" wording.
- Reset tab: "included free with every ComfortBundle™" → "included with every LumbarEase™".
- Trust strip: same as ErgoRelief ("Sydney dispatch · Express shipping · 30-day money-back").
- Measured (harness, 402px, lead photo is a stand-in): ATC 1107 → 867px (−240px, trust strip included).
- PUSHED (commit 00a8aab). Verified checksumMd5 d539c09740fd88cf62ddd93cdc8b46d5 = local, size 30506. ErgoRelief template unchanged (164e0c48…). Live untouched.

## Sections 2–11 + CTAs (PUSHED 2026-09-23)
Owner approved the full plan ("Yes"). Built by `build_rest.py` from the pushed hero state. At section level, every difference from ErgoRelief's final page is product-specific: names, images, links, LumbarEase copy.
- 2 Image-with-text: "Leaning back isn't the fix." / "A soft chair back doesn't hold your spine's curve — it just moves where you slump. LumbarEase™ keeps your lower back supported in the same position the whole time you sit." (from the product description). 4 bullets disabled; button bug (linked to own page) → add LumbarEase. 1034 → 766px.
- 3 Why One Product Isn't Enough: CB copy/blocks verbatim (bundle pitch) + subheading "The ComfortBundle™ pairs this lumbar support with the ErgoRelief™ seat cushion — so seat and spine are supported together, then reinforced over 7 days." Heading kept, button → bundle page, white bg. Same content as ER before → ~−321px.
- 4 7-Day Reset: lock note "…included with LumbarEase™"; button adds LumbarEase (opt-in settings already in 7days.liquid, unchanged).
- 5 Every-day: disabled (−660px).
- 6 All-Day Support: "Firm-but-forgiving support that holds its shape — so it keeps working after the first week, not just on day one." Button → add LumbarEase. Diagram hidden ≤991px (the product image stays, same call as ErgoRelief; the owner hasn't seen LumbarEase's images, so it's worth confirming). Also cleared the teal subheading that repeated the page title. 1526 → 1133px.
- 7–11: mirrored from CB exactly like ErgoRelief (no "Free"; FAQ + banner buttons add LumbarEase; LumbarEase's own photo kept in "Australian, end to end").
- CTAs: sc-cta-delegate (ErgoRelief's fixed version) from the start. The build asserts every /cart/add link uses LumbarEase's variant and no bundle/ErgoRelief variant appears.
- Mobile total ≈ −1,880px (hero −240, s2 −268, s3 ~−321, s5 −660, s6 −393).
- PUSHED (commit 6b79375). Verified checksumMd5 1dff1c559a9ed629e69171da28497ff9 = local, size 38770. ErgoRelief template + 7days.liquid unchanged. Live untouched.

## Headline change (PUSHED 2026-09-23)
Owner didn't like "Stop slumping by 2pm." and asked whether it's good enough for a product page. My answer: no. It's an ad hook, it reads two ways ("stop by 2pm" vs "the 2pm slump"), and it names the problem rather than the benefit (ErgoRelief's "Sit longer without the ache." states a benefit).
- New: "Sit upright without trying." (the Description tab's own words, "sitting upright without thinking about it"). 1 line at 26px on 402px (30px tall).
- "Stop slumping by 2pm." is still a good Meta ad hook.
- PUSHED (commit d191e80). Verified checksumMd5 2153535f7d8463eb8a9cd87c8127b74e = local, size 38776. 1 key changed. Live untouched.
