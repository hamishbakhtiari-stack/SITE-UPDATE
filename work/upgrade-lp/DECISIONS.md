# Chair Upgrader LP (P2 "Sarah", LP-B "Upgrade") — decisions log

- Working theme: `164520263937` "SitComfort — Chair Upgrader LP (Claude, DO NOT PUBLISH)",
  duplicated from `164379558145` (Video carousel tablet fix — tested, intended to go live with this).
- Template: `templates/product.upgrade.json`, copied byte-for-byte from `product.ComfortBundle.json`
  (checksum 650bdbd03485b525ec44973562464eaa). URL: `/products/comfortbundle-complete-system?view=upgrade`.
  Not in navigation; ad landing page only.

## Hero (main-product) — approved 2026-09-30
- Eyebrow: kept as original "Better Sitting in 7 Days" (v3). Tried "For the chair you already have" (wrapped the pill to 2 lines — keep pill text ≤ ~24 chars) and "No new chair needed" (repeated the headline).
- Headline: "Fix how you sit, not just what you sit on." → "Upgrade your chair, don't replace it." (v3, owner's line — echoes Sarah's core thought; replaced the P2 lead line "Upgrade your chair, not your whole office.")
- Description → "Seat cushion and strap-on lumbar support for the chair you already own, plus the 7-Day Reset."
- Bullets: value first, then setup (owner's call — setup objections sit right above Add to Cart):
  1 Cushion takes pressure off your tailbone · 2 Lumbar support holds your back's curve ·
  3 Fits most chairs: office, dining and gaming · 4 No tools, no assembly. Straps on and stays put.
- Layout, icons, CTA: unchanged. Gallery = product media (shared with main PDP); open if owner wants a different first image.
- Guard (`locked.json`) updated: headline lock now expects "Upgrade your chair, don't replace it.".

## Section 2 — one_product_PTdiHH ("Why the full system works") — approved 2026-09-30 (v4)
- Heading: "Why [the full system] works" → "Your chair, [fully supported]"
- Subheading → "Support under you and behind you — on the chair you already own. The 7-Day Reset shows you how to set it up."
- Owner rejected "Why a cushion [isn't enough]": copy must stay positive — we are selling. Keep copy plain and grammatical.
- Layout, badge, 4 cards, icons, CTA unchanged.

## Other sections — owner: no changes needed (What's included, 7-Day Reset, All-Day Support, videos/reviews, Australian, FAQ, Judge.me)

## CTA banner — cta_section_tEApVF — approved 2026-09-30 (v5)
- Heading: "Reset your sitting. [br]Reclaim your comfort." → "Upgrade your chair. [br]Keep your comfort." (echoes hero)
- Setting lives in this template only; CTA-section.liquid untouched, so About Us / other pages' banners are unaffected (checksums verified before/after).

## Closed topics
- Compliance: never raise again (owner, 2026-09-30).
