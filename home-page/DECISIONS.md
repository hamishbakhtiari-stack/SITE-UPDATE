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

### 2026-09-21 — §1 Hero review, and a CORRECTION to it

**CORRECTION — my headline finding was wrong.** I claimed the broken media query in
`custom-hero-section.liquid` meant the hero used desktop padding on mobile, wasting 188px above
the fold. Hamish's mobile render disproves it: there is **almost no gap between the header and the
hero image**, and the gap below the guarantee list is roughly the configured mobile value, not
120px. So the hero's mobile padding is behaving about as configured — another stylesheet
(`cstm-style.css` / `resposive.css`, neither of which I have read) is evidently handling it.

The broken CSS is still really there:

```css
@media screen and (max-width: 749px) {
    {                                  <- no selector, rule is discarded
      padding-top: var(--pt-mobile) !important;
```

But it is a **latent** bug, not an active one. Its effect is masked. Fixing it could *change*
current mobile spacing on all four templates rather than improve it. **Do not touch it** without
first reading the CSS that is actually doing the work. Exactly the rule I wrote down after the §5
failure, and I skipped it again by asserting layout from code without a render.

**RETRACTED — the em dash.** I predicted "Sit longer without pain —" would orphan the dash onto
line 2 on mobile. It does not. It renders "Sit longer without / pain — in 7 days." with the dash
mid-line. No fix needed.

**SOFTENED — the dead overlay.** `overlay_color`, `overlay_opacity` and `overlay_direction` are
read by the CSS but absent from the schema, so the overlay div renders at opacity 0. Still true.
But on mobile the photo is a block *above* the text, not behind it, so there is no contrast
problem. Desktop not seen. Not worth acting on.

**STILL TRUE, verified independently of rendering — the schema is invalid JSON.**

```json
"id": "guarantee_label",
"label": "Guarantee Label",     <- trailing comma, no following key
},
```

Confirmed by parsing it. One character. Affects the theme editor, not the storefront.

**NEW, from the render — the primary CTA is below the fold on mobile.** Measured as proportions of
the first screen (approximate, read off the screenshot):

| band | share of first screen |
|---|---|
| announcement bar + header | ~27% |
| hero photo | ~33% |
| subheading / heading / body / separator label | ~33% |
| "Start Your 7-Day Reset" | begins at ~95%, cut off by the browser toolbar |

The photo alone takes a third of the first screen. Text-only levers that would lift the button:
the separator label wraps to 2 lines, and the body text wraps to 2 lines; tightening either saves
roughly a line each. **Not proposed as copy — Hamish's call.**

Also noted: the hero body text says "A complete support system", which is the same phrase he just
asked to stop repeating on the ComfortBundle card. Consistency point, not raised as a fix.

### 2026-09-21 — §5 card review 3 of 3: ComfortBundle (card_gCtPhR). Section complete.

Text-only. Section file untouched (`f895d180…`). 2 keys changed.
Verified: 19118 bytes, md5 `c09cf9aa993654b9fa159e62180e295e`.

**Hamish's instruction: don't say "complete system" twice.** The heading is `product.title` —
"ComfortBundle™ Complete System" — and cannot change without the section file, so the subtitle had
to drop both words. It said "Complete support system". Counted before and after in the build:
**complete x2 / system x2 → x1 / x1**, now only in the heading.

**Changed**

| key | before | after |
|---|---|---|
| `subtitle` | Complete support system | ErgoRelief™ + LumbarEase™ together |
| `feature_5` | *(empty)* | One makes the other work |

The new subtitle also closes the biggest gap found in the original review: **the card never said
what was in the bundle.** A visitor scanning three cards could not tell the middle one contained
the other two. It does now, in the most prominent line available.

`feature_5` is his own PDP wording — `one_product_PTdiHH` → `feature_pJJif9` "One makes the other
work" — which is the actual argument for the pair over either alone, and reads as a closer under
the new subtitle.

`reset_tag` "7-Day Reset included" left untouched: correct naming, and it already carries the
Reset, so the subtitle did not need to repeat it. Features 1-4 untouched — "Spine alignment" and
"Pressure relief" restating the side products is *correct* on a bundle card; that is the claim.

**All three cards now show 5 features.** The original 2 / 4 / 2 asymmetry is gone — the bundle no
longer looks fuller only because the outer cards were kept short.

---

## §5 "Engineered for real support" — final state

| | |
|---|---|
| `templates/index.json` | 19118 bytes, `c09cf9aa993654b9fa159e62180e295e` |
| `sections/comparison-Section.liquid` | 8867 bytes, `f895d180f30e7af98ad57c5090679ada` — **never modified** |

Shipped across four text-only pushes: heading NBSP, subheading replaced, three `button_url`
cleared, and all three cards' subtitles rewritten plus every empty feature slot filled.

**Still open — all require the section file, none attempted:**
1. `title` and `image` overrides are dead on all three cards (product data wins). This is also why
   ErgoRelief's rows sit ~18px above LumbarEase's — one product title wraps, the other does not.
2. Product images render through `img_url: 'medium'`, a fixed 240px. Minor; **leave it.**
3. The middle card sits ~30px lower than the outer two. Cause never established.
4. `card_Uq9cab.feature_1` "Lumbar support" still echoes its heading — the weakest line left in
   the section. Text-only, but outside the agreed per-card scope. Raise separately.

**Blocked on building and proving the render harness** (`references/render-harness.md`) against a
screenshot Hamish has already seen. Nothing touching markup ships before that.

### 2026-09-21 — §5 card review 2 of 3: LumbarEase (card_Uq9cab)

Text-only, same scope as ErgoRelief. Section file untouched (`f895d180…`).
4 keys changed. Verified: 19079 bytes, md5 `63feadce68da5fcfa4851e869ff371e8`.

**Findings.** Worse repetition than ErgoRelief: **"lumbar" x3 and "support" x3** across the four
visible lines. Three of the four were the same two words reordered —

    LumbarEase™ Lumbar Support     (product.title)
    Targeted lumbar support        (subtitle)
    Lumbar support                 (feature_1)
    Posture positioning            (feature_2)

Also 2 of 5 feature slots used, same as ErgoRelief before the fix. `title` ("LumbarEase™ ", with
its trailing space) and `image` are both dead — product data wins. The trailing space was **left
alone**: it is inert while the section file stands, and cleaning it would be a diff with no effect.

**Changed**

| key | before | after |
|---|---|---|
| `subtitle` | Targeted lumbar support | Stops the slump before it starts |
| `feature_3` | *(empty)* | Contoured to your lower back |
| `feature_4` | *(empty)* | Straps that won't slide down |
| `feature_5` | *(empty)* | Breathable, washable cover |

From the PDP's own LumbarEase list (`comparison_products_DgmnVi` → `box2_item1`, `box2_item4`, and
`box2_item2`+`box2_item3` merged into one line). Chosen for the three standard lumbar-support
objections: wrong shape / digs in, it slides down the chair, it gets hot and can't be cleaned.
`feature_4` is the real differentiator — the adjustable dual straps.

The subtitle draws on his collection-page line "the slump that starts an hour into your day never
sets in". All four are <= 32 characters, the one-line budget.

Repetition after: lumbar x2, support x2 (from x3 and x3). The remainder is `feature_1`
"Lumbar support", which still echoes the heading — **left unchanged, out of the agreed scope.**
Worth raising with Hamish separately; it is the weakest line left on the card.

`feature_5` deliberately reads "Breathable, washable cover" rather than repeating ErgoRelief's
"Breathable mesh, stays cool" verbatim — both products have the same cover, but two identical
lines side by side in a comparison row read as filler.

Build asserted block_order, section settings and every other key on all three cards byte-identical;
ErgoRelief and ComfortBundle untouched.

**Height: ESTIMATE.** ~+54px on this card, same as ErgoRelief. Desktop likely absorbs it into the
dead space below the button; mobile is real. Not harness-measured.

**Remaining in §5:** the ComfortBundle card.

### 2026-09-21 — §5 card review 1 of 3: ErgoRelief (card_QeERNL)

Text-only. Section file untouched (`f895d180f30e7af98ad57c5090679ada`).
4 keys changed. Verified: 18988 bytes, md5 `2bd3e40a7311e1a287d506e365ac8f79`.

**Review findings**

- Two settings on this card are dead: `title` ("ErgoRelief™") loses to `product.title`, and
  `image` (`ErgoRelief.webp`) loses to `product.featured_image`. Editing either in the theme
  editor does nothing. Root cause is the section file; **not touched.**
- The four visible lines repeated themselves — `seat` x2, `cushion` x2, `pressure` x2 in ~10 words.
  Heading "ErgoRelief™ Seat Cushion", subtitle "Pressure-relieving seat cushion", feature_1
  "Pressure relief". Three of four lines carried one idea.
- Only 2 of 5 feature slots used; the Liquid loops `(1..5)` so three rendered nothing.
- Measured off Hamish's desktop screenshot (approximate): **~90px of dead space below the
  ErgoRelief button**, against ~38px on the bundle card — the direct consequence of 2 features
  vs 4 in an equal-height row.

**Changed**

| key | before | after |
|---|---|---|
| `subtitle` | Pressure-relieving seat cushion | Takes the weight off your tailbone |
| `feature_3` | *(empty)* | Foam that won't flatten |
| `feature_4` | *(empty)* | Breathable mesh, stays cool |
| `feature_5` | *(empty)* | Fits most chairs and car seats |

Features 3-5 are shortened from the PDP's own ErgoRelief list
(`comparison_products_DgmnVi` → `box1_item1`, `box1_item2`, `box1_item5`), picked because they
answer the three standard cushion objections: it'll flatten, it'll get hot, it won't fit my chair.
All are <= 32 characters, the one-line budget for the ~213px feature text column.

`feature_1` "Pressure relief" and `feature_2` "Lower body alignment" left **unchanged** — that was
the agreed scope (fill 3-5, rewrite subtitle), not a rewrite of his existing two.

Build asserted that `block_order`, section settings, and every other key on all three cards were
byte-identical; ComfortBundle and LumbarEase cards completely untouched.

**Height: ESTIMATE.** 3 feature rows ~18px each = ~+54px on this card. On desktop it likely fills
the ~90px of dead space rather than growing the row. On mobile, where cards stack, ~+54px is real.
Not harness-measured.

Still open on this card, needs the section file: the dead `title` override, which is also why
ErgoRelief's rows sit ~18px above LumbarEase's.

### 2026-09-21 — §5 text-only pass (after the revert). 3 fixes, no markup touched.

Hamish chose the text-only option. **`sections/comparison-Section.liquid` was not touched** and
remains at `f895d180f30e7af98ad57c5090679ada`.

5 keys changed. Verified: 18905 bytes, md5 `fbb4e3666bca1f669694e60be2b9ed12`.

1. `heading` — `Engineered for real support\u00a0—`. Same words, the space before the em dash is
   now U+00A0, so the dash cannot orphan onto line 2 on mobile.
2. `subheading` — "Most customers choose the full system for complete relief" →
   "From targeted relief to complete support — start where your pain starts." Removes the claim
   contradicted by the store's own data (bundle: 0 orders in 730 days vs 72 and 68).
3. Three `button_url` values cleared → the `{% elsif %}` branch runs, which carries no
   `target="_blank"`. Buttons stay in the same tab.

**Pre-flight on #3, written down before pushing.** Clearing `button_url` moves the anchor to
`{% elsif product != blank %}`. If `product` did not resolve, that branch is skipped and *no
button renders at all*. Evidence it resolves: Hamish's own desktop screenshot shows `$89 / $71 /
Save $18.00` and `5.0 (15)` on the cards — every one of those is printed from `product`. If it
were nil they would all be blank. Both branches emit the same `<a class="btn-globel
btn-globel--solid">` with the same label, so only `href` and `target` differ. No visual change.

The build script also **asserted** that `block_order`, and every one of `title`, `subtitle`,
`image`, `icon`, `feature_1..5`, `button_label`, `show_reset_tag`, `reset_tag`, `best_value` and
`featured_product` were byte-identical before and after — i.e. nothing markup-adjacent moved.

Still deliberately NOT done: card titles, subtitles, image resolution, feature copy, the middle
card offset. All need the section file or a height measurement. **Blocked on building and proving
the render harness.**

---

## Process rules added after the §5 failure — these are binding

1. **Two risk classes, never mixed in one push.** Text-only template settings cannot restructure a
   layout. Markup and CSS changes can. They travel separately so a revert costs one thing.
2. **Before changing markup, read the CSS that sizes it.** The §5 failure happened because
   `cstm-style.css` was skipped twice to save context — and that file holds
   `.product-image-wrap img`, the rule that would have shown the image had no width pinned and
   that `image_tag`'s intrinsic `width`/`height` would therefore take over.
3. **Prove the instrument before trusting it.** The first thing any new render harness renders is
   the section *unchanged*, checked against a screenshot Hamish has already seen. If it does not
   match reality, the harness is wrong and gets thrown out — it never gets used to validate a
   change first.
4. **One risky change per push.**
5. **Hamish is not the renderer.** "Worth a preview now" was verification outsourced to him after
   the fact. If it cannot be verified here, it does not ship: describe it and let him decide.
6. `references/render-harness.md` exists and was ignored for this entire project. **Read it before
   any layout work.** It documents the iframe technique, the Chromium path, the box-sizing reset
   and the CSS load order.

### 2026-09-21 — §5 REVERTED IN FULL. Section is back to its pre-review state.

Hamish sent renders of what I shipped: the card images blew up to several hundred pixels, the
cards ballooned, the row broke. He asked for a full undo. Done, both files, verified:

| file | size | md5 | |
|---|---|---|---|
| `sections/comparison-Section.liquid` | 8867 | `f895d180f30e7af98ad57c5090679ada` | identical to the original |
| `templates/index.json` | 18993 | `0338f0ea79ccd2158402da5e05d8418e` | identical to pre-§5 |

Nothing from that work survives. Sections 7, 8, 10 and the FAQ are untouched by this revert.

#### What I broke, and the exact mechanism

Replacing `<img src="{{ product.featured_image | img_url: 'medium' }}">` with `image_tag` was the
error. The original `<img>` carried **no `width`/`height` attributes**, so the theme's CSS alone
decided the rendered size. `image_tag` writes intrinsic `width` and `height` attributes onto the
tag from the source image. This theme's `.product-image-wrap img` rules evidently do not pin a
width, so those attributes became the size and the image rendered at its intrinsic dimensions
instead of ~180px. Every card grew with it.

`img_url: 'medium'` being a fixed 240px was a real finding. The fix was not. A 240px image in a
~180px box was a minor sharpness issue on retina; what I shipped in its place destroyed the
layout. **The cure was far worse than the disease, and the disease was cosmetic.**

#### Rule this produces — this is the second time

`references/lessons.md` #8 already says: *render before pushing, even for a change that is
"obviously" just CSS.* I did not render. I pushed markup changes to three product cards on
reasoning alone, and told Hamish "worth a preview now" — making him the renderer.

**Never again ship a change to image markup, or to any markup that CSS is currently sizing,
without seeing it rendered first.** Specifically:
- Swapping a bare `<img>` for `image_tag` is NOT a like-for-like change. It adds `width`, `height`,
  `srcset` and `sizes`. On a theme whose CSS assumes an unsized `<img>`, that changes layout.
- If a render cannot be produced here, the change does not ship. Describe it and let Hamish
  decide, rather than pushing and asking him to check.
- Bundling a risky markup change with four safe copy changes cost him all five. **Separate the
  risky edit into its own push** so a revert does not take the good work with it.

#### The findings that were real and remain unfixed

Recorded so they are not lost, but **nothing is to be actioned without approval and a render**:

1. Subheading "Most customers choose the full system" — contradicted by sales data (bundle: 0
   orders in 730 days vs 72 and 68). **Template-only, zero layout risk.**
2. All three card buttons open a new tab via a hard-coded `target="_blank"`. Fixable by clearing
   the three `button_url` values. **Template-only, zero layout risk.**
3. Mobile heading orphans the em dash onto line 2. Fixable with a U+00A0. **Template-only.**
4. Card title/subtitle repetition, and the outer-card misalignment caused by one title wrapping.
   **Needs the section file — do not touch without a render.**
5. Images at a fixed 240px. **Real but minor. Not worth the risk. Leave it.**

Items 1-3 carry no layout risk at all and could ship separately if he wants them. Items 4 and 5
should stay closed unless he asks.

### 2026-09-21 — §5 "Engineered for real support": all proposed changes shipped (REVERTED — see above)

Two pushes. Verified by checksum, and every other template re-read and confirmed unchanged.

| file | size | md5 | |
|---|---|---|---|
| `sections/comparison-Section.liquid` | 9175 | `c94991ffdbb720952a62d65e52bfb330` | matches local, CRLF preserved |
| `templates/index.json` | 19288 | `fe62b3c82ebdb730e31e0bf7b6ab69c0` | matches local, 9 keys changed |
| `product.ComfortBundle.json` | 39409 | `ee9abc87…` | unchanged |
| `collection.json` | 12354 | `4ced7bb0…` | unchanged |
| `collection.custom-collection.json` | 12454 | `2eab3a44…` | unchanged |
| `product.ergoRelief.json` | 27848 | `241b858f…` | unchanged |
| `product.lumbarEase.json` | 27882 | `b8396197…` | unchanged |

Blast radius checked before editing the section file: `page.about-us`, `page.7-day-reset`,
`page.7-day-sitting`, `page.faq-page` and `collection.custom-collection` were read and none uses
`comparison-Section`. Both section edits are backwards compatible anyway (override-wins-if-set,
and a pure image-quality change), so a template that does not set an override renders identically.

**Section file (2 edits, CRLF preserved):**
1. Heading precedence flipped — `block.settings.title` now wins when set, else the product title.
   Fixes the ~18px card misalignment and the title/subtitle echo in one change.
2. `img_url: 'medium'` (fixed 240px) replaced with `image_url` + `image_tag`, `widths:
   '180, 270, 360, 540, 720'`, `sizes: '(min-width: 990px) 190px, (min-width: 750px) 30vw, 70vw'`,
   `loading: 'lazy'`. **Which image wins was deliberately NOT changed** — the product photo is still
   preferred over the block override, so the lifestyle shots Hamish currently sees stay. Swapping
   to the `.webp` product shots would be a photography decision, and photography is his.

**Template (9 keys):**
3. Heading now `Engineered for real support\u00a0—` — a non-breaking space welds the em dash to
   "support" so it can't orphan onto line 2 on mobile.
4. Subheading → "From targeted relief to complete support — start where your pain starts."
   His own line from the collection page. The false "most customers choose the full system" claim
   is gone.
5. Card subtitles → the collection pages' copy. Taken from **`collection.custom-collection.json`**,
   not `collection.json`, because that version says "7-Day Reset" rather than the retired
   "7-Day Pain Relief Reset", and is shorter.
6. All three `button_url` cleared → the `{% elsif %}` branch runs, which has no `target="_blank"`,
   keeps the custom `button_label` and resolves to the same product URLs. **New-tab bug fixed with
   no code change.**
7. `LumbarEase™ ` trailing space removed (it now renders, so it mattered).

Card headings are now the short names: ErgoRelief™ / ComfortBundle™ / LumbarEase™ — all one line,
so the three cards should align.

**Mobile height — ESTIMATE, not a harness measurement.** The subtitles go from 1 line to roughly 5
each at ~256px card width (measured off Hamish's phone screenshot), ~15px type at 1.5 line-height:
**about +270px across the three cards.** Flagged to him. Not measured in the iframe harness because
the real webfont is unavailable here and a fallback font would give the wrong line count — his
theme preview is the more accurate check.

**NOT done, and why:**
- **Feature list copy.** Criticised in the review but no specific replacement was ever proposed, so
  nothing was invented. Still generic nouns; open.
- **The middle card sitting ~30px low.** No fix was proposed — cause not established. Open.

Guard updated: the three `button_url` values are locked empty, and the heading is locked with its
U+00A0, so a later edit that reintroduces either defect fails the pre-push check.

### 2026-09-21 — §5 review, part 3: copy

**Heading: keep.** "Engineered for real support — not just softness" makes a claim and draws a
contrast. Only the mobile dash break needs fixing (part 2).

**Every card says the same thing twice.** Title and subtitle restate the category:

| rendered title | subtitle | repeated |
|---|---|---|
| ErgoRelief™ Seat Cushion | Pressure-relieving seat cushion | "seat cushion" |
| ComfortBundle™ Complete System | Complete support system | "complete … system" |
| LumbarEase™ Lumbar Support | Targeted lumbar support | "lumbar support" |

On the LumbarEase card "lumbar" appears **four times** in ~8 words of copy: title (LumbarEase,
Lumbar), subtitle (lumbar), feature 1 (Lumbar support). The subtitle is the only line free to add
information and it spends it repeating the title.

**The bundle card never says what is in the bundle.** It reads "Complete support system" plus four
abstract nouns. Nowhere does it say **ErgoRelief™ + LumbarEase™**. A visitor scanning three cards
cannot tell the middle one contains the other two — the only hint is the "7-Day Reset included"
badge. This is the section's biggest persuasion gap and it is a copy fix, not a layout one.

**Features are category labels, not benefits.** "Pressure relief", "Lower body alignment", "Lumbar
support", "Posture positioning", "All-day comfort", "Breathable materials" — nouns with no
mechanism and no payoff, against the PDP's "High-density memory foam — holds its shape instead of
flattening over time" and "Adjustable dual straps — stay tight instead of sliding down the
backrest". Two of the bundle's four features ("Pressure relief", "Spine alignment") just restate
the side products', so the bundle looks richer mainly because the outer cards were kept to two.

**Buttons are fine.** "View ErgoRelief™ / View Full System / View LumbarEase™" — consistent and
appropriately low-commitment for a chooser. Note the theme applies `text-transform: capitalize`,
so casing typed into `button_label` does not matter.

#### Recommendation: the copy this section needs is already on the collection page

`templates/collection.json` → `collection_products_czKeWp` holds Hamish's own, better versions:

- sub_heading: *"From targeted relief to complete support — start where your pain starts."*
  Makes no customer-behaviour claim, and does the job the current subheading fails at.
- ErgoRelief: *"Memory foam seat cushion with a tailbone cut-out that takes the pressure off your
  lower body during long sitting sessions — at your desk, in the car, or on the couch."*
- ComfortBundle: *"ErgoRelief™ and LumbarEase™ together, plus a guided 7-Day Pain Relief Reset —
  the complete system for people who've tried everything else and are still uncomfortable by 10am."*
- LumbarEase: *"Curved lumbar support with adjustable straps that holds your lower back's natural
  curve, so the slump that starts an hour into your day never sets in."*

Two caveats: these are 2–3 lines each against the current one-liners, so card heights grow — needs
measuring against the mobile-height rule before shipping. And "7-Day Pain Relief Reset" is retired
naming; it would become "7-Day Reset".

#### Parked, NOT this section

`templates/collection.json` points its bundle card at product handle `comfortbundle` and its
buttons at `shopify://products/comfortbundle™` (with a ™). The real handle is
`comfortbundle-complete-system`. Both look wrong and would mean a dead link on the live collection
page. Not verified, not in scope here — raise when we reach the collection page.

### 2026-09-21 — §5 review, part 2: findings from Hamish's live screenshots

He sent a desktop and a mobile render of the section. Same section as the review above
(`comparison_section_ytnPWC`). Measurements below are read off the screenshots and are
**approximate** — worth confirming in the iframe harness before quoting them as final.

**Correction to the earlier review.** I estimated the card images render into a ~380px box; they
are about **180px** on desktop. `img_url: 'medium'` is 240px, so on a 1x desktop screen they are
fine. The upscale is ~1.5x on a 2x desktop display and, at roughly 256px on the phone render,
~2x on mobile. Still worth fixing, smaller than stated.

**New: the heading breaks badly on mobile.** It renders as

```
Engineered for real support
— not just softness
```

The em dash is orphaned onto line 2. Cause: `heading` ends `support —` with a normal space before
the dash, and the Liquid emits `{{ heading }}` then whitespace then `<span>{{ heading_span }}</span>`,
so the browser can break at that space. **Fix is one setting** — a non-breaking space (U+00A0)
between "support" and "—" glues them together. No code change.

**New: the two outer cards are misaligned all the way down, and the dead `title` override is why.**
"ErgoRelief™ Seat Cushion" fits one line; "LumbarEase™ Lumbar Support" wraps to two. Everything
below shifts by one line height (~18px in the screenshot): subtitles at y176 vs y194, ratings at
y445 vs y462, prices y477 vs y494, buttons y531 vs y549. The two side cards are structurally
identical (2 features each) and should line up exactly.

This connects to finding #4 in the review above. `{% if product.title != blank %}` always wins, so
the short names typed into the `title` settings ("ErgoRelief™", "ComfortBundle™", "LumbarEase™")
never render. If the override worked, all three headings would be one line and the rows would
align by themselves. **The dead override is the root cause of the misalignment, not a separate
cosmetic issue.**

**New: the middle card sits ~30px lower than the side cards.** Side cards top at y118 and bottom
at y640; the ComfortBundle card runs y150 to y680 — only ~8px taller but offset ~32px down. Reads
as a row that failed to align rather than a deliberately featured card. Needs harness measurement
to say why (likely the "Best Value" badge sitting above the card edge).

**Positive: mobile leads with ComfortBundle.** On the phone render the Best Value card is first,
directly under the subheading, not third. Good ordering — worth keeping.

**Mobile height:** the single ComfortBundle card nearly fills the viewport. Three stacked will be a
long scroll. Not measured; flagging only.

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


---

## S6 — Hero, Phase 1: three text settings, no markup (2026-09-21)

**Scope.** `templates/index.json` only, `custom_hero_section_Yh4kcV`, three settings. Risk class:
text-only. `sections/custom-hero-section.liquid` was NOT opened and NOT touched — it is shared by
`index`, `page.about-us`, `page.7-day-reset` and `page.7-day-sitting`, so anything done to it has
a four-template blast radius.

| Setting | Before | After |
|---|---|---|
| `subheading` | `The 7-Day relief system` | *(blank)* |
| `separator_label` | `ErgoRelief™ cushion • LumbarEase™ support • Guided 7-Day Reset` | *(blank)* |
| `body_text` | `<p>A complete support system for people who sit 6+ hours a day.</p>` | `<p>A cushion, a lumbar support, and a 7-day plan to retrain how you sit.</p>` |

**Why blanking is safe.** All three are wrapped in `{%- if section.settings.X != blank -%}` in the
section file, so an empty value removes the element and its wrapper entirely rather than leaving
an empty box. No CSS change, no markup change, no new selector.

**Why each one.**

- `subheading` — the eyebrow read "The 7-Day relief system" directly above a headline ending
  "in 7 days." Same promise twice, in two type sizes, before the reader has been told what the
  product is.
- `separator_label` — a two-line trademark list plus its divider rule sat between the body copy
  and the CTA. It pushed the button down without answering anything a cold visitor is asking on
  first screen. The product names are reassurance, not a headline; they belong below the CTA.
  (Phase 2 is where they go back, after the badge row.)
- `body_text` — "A complete support system for people who sit 6+ hours a day" describes the
  audience, not the product. The replacement names the three things in the box.

**Expected effect, and what it is not.** Removing the eyebrow (~30px) and the divider + label
block (~61px) takes roughly 91px out from above the CTA on a 390px viewport. On the numbers, that
should move "Start your 7-Day Reset" from about 52px below the fold to about 39px above it.

**This is arithmetic, not a measurement.** There is still no proven render harness, so the fold
figure is a calculation from the mockup's box model, not something observed. It needs a look in
theme preview on a real phone before it is treated as fact.

**Push record.**

- Working theme `164208705793` (UNPUBLISHED) — `templates/index.json`
  `c09cf9aa993654b9fa159e62180e295e` (19118 B) → `5d1180fb0d021404731a676972288e5c` (19034 B).
- Verified by `checksumMd5` on a fresh read: matches local `md5sum` exactly.
- Live theme `164124164353` re-checked in the same query: unchanged at
  `5d7e33bffcd39ae15a15d3903fe7b8a0`, 18026 B.
- `diff_template.py` against the previous baseline: exactly 3 diffs, all three the ones above.
  `order` unchanged, every `block_order` unchanged, 311 keys before and after.
- `check_template.py` against `locked.json`: PASS.

**A push went out wrong and was corrected — process rule added.**

The first attempt landed at 19033 bytes, one short, md5 `d3aa8e74…`. The three hero changes were
correct; the corruption was elsewhere. Cause: the body was transcribed into the GraphQL variable
with non-ASCII characters written literally, and the U+00A0 in
`comparison_section_ytnPWC.settings.heading` ("Engineered for real support —") arrived as a
plain space. That is a guarded value, and `locked.json` says in as many words why it must be a
non-breaking space: a plain space lets the em dash orphan onto line 2 on mobile.

Confirmed by hypothesis test before re-pushing — substituting a plain space into the local
candidate reproduced the server's md5 and byte count exactly. Re-pushed with the corrected body;
the second push verified byte-exact.

**Rule 7 (new).** Any theme-file body sent over GraphQL is built with
`json.dumps(body, ensure_ascii=True)`, so every non-ASCII character travels as an explicit
`\uXXXX` escape. Invisible characters — U+00A0, U+2011, U+200B — do not survive being typed by
hand, and `check_template.py` cannot catch it because the guard runs against the candidate on
disk, not against what actually goes over the wire. The `checksumMd5` verify is the only thing
that catches this class of error, which is why it is not optional.

**Not done, deliberately.** Phase 2 (a `custom-liquid` section under the hero carrying the rating
row, the three badges, and the product-names line) is designed but not started — it needs the go
-ahead. Hero photo height, the invalid schema JSON in the section file, the dead overlay settings
and the latent selector-less media query are all still untouched.

**Still open.** Whether to add a short "Dispatched from Sydney" line under the badge row in Phase
2. Badge Option B loses "from Australia", and that is the thing that separates SitComfort from the
overseas sellers.

---

## S6b — Hero Phase 1 reverted (2026-09-21)

Hamish looked at it on his phone and said: *"Dont like it at all, my current is better."*

Reverted. `templates/index.json` on theme `164208705793` is back to
`c09cf9aa993654b9fa159e62180e295e` (19118 B), verified by `checksumMd5` on a fresh read, and
`diff_template.py` against the pre-Phase-1 file shows 0 diffs across all 311 keys. Live theme
`164124164353` re-checked in the same query: unchanged at `5d7e33bffcd39ae15a15d3903fe7b8a0`.
The hero settings are exactly as they were before S6.

**The fold target was actually met** — in his screenshot both buttons clear the fold, which is
what Phase 1 was for. So this was not a failed mechanic. It was the wrong trade: the page got
shorter and worse.

**What I think went wrong, for the next attempt.** Three things came out in one push. The eyebrow
and the product-names line were doing more than taking up space — between them they told a cold
visitor what category this is and what is physically in the box, before the CTA. Removing both
left a headline, one sentence and two buttons on a lot of white. Shorter, but generic: it could
be any wellness brand.

**Process note.** This was inside one risk class (text-only settings) so it did not violate rule
1, but it bundled three independent copy decisions into a single reviewable unit. Rule 4 says one
risky change per push; the spirit of it applies to copy too. Next time on the hero: change one
element, look at it, then decide on the next.

**Standing constraint added to `locked.json`.** Do not re-propose blanking the eyebrow or the
product-names line as a bundle. The hero is not to be changed again without a specific brief from
Hamish about what he wants different.

**Still true and still unused:** rule 7 (build theme-file bodies with `ensure_ascii=True`) is kept
in `locked.json` — it is about the push mechanism, not about the hero, and it earned its place.

---

## S6c — Standing rule: what the home hero is for (2026-09-21) — PERMANENTLY CLOSED

Hamish, in his own words:

> *"Mine is clwarer, i dont care if cta is not in cold, people should look at my home page and
> tell why I exist , mine has ebwbrow , a conplete sitting system, etc"*

**The rule.** The home page's job is to make a stranger understand why SitComfort exists. CTA
position relative to the fold is not a goal, and is never a reason to remove anything.

**These three stay, and are not to be touched:**

1. The eyebrow — `subheading`: "The 7-Day relief system". Names the category before anything else.
2. The system line — `body_text`: "A complete support system for people who sit 6+ hours a day."
   The words *complete support system* are the point.
3. The product-names line — `separator_label`: "ErgoRelief™ cushion • LumbarEase™ support •
   Guided 7-Day Reset". Says what is physically in the box.

**Closed topics on the home page, from here on.** Fold position. Scroll depth. Above-the-fold CTA
placement. Shortening the hero to move the button up. None of these are to be raised again as an
argument for changing home-page copy.

**Why this is written down.** My entire hero rework was built on the fold premise, and the
premise was wrong for this page. The mockup, Phase 1, and the parked Phase 2 all inherited it.
Anything still carrying that reasoning is void, not pending.

**Phase 2 is parked, not queued.** It was designed partly around the same fold logic. If the
rating row and the badges come back, it will be as an additive proposal justified on its own
terms, and only when Hamish asks.

---

## S7 — The three badges replace the three dot points (2026-09-21)

Hamish: *"Can you add those 3 badges now?"* — and, confirmed against his earlier plan, the badges
take the place of the three guarantee dot points rather than sitting beside them.

**What changed, in `templates/index.json` only:**

1. `custom_hero_section_Yh4kcV.settings.guarantee_label` → blank. That removes the
   `<ul>` of "Express shipping from Australia / 30-day money-back guarantee / Easy returns".
2. New section `badge_row` (type `custom-liquid`), inserted in `order` at index 1, directly after
   the hero. It carries the three badge images at 78×78, left-aligned, inside `page-width` with a
   600px max-width so they line up under the hero's content column.

The eyebrow, the "complete support system" line and the product-names line are all untouched, per
the S6c standing rule.

**Shopify refused the tidier version, and that is worth recording.** The first attempt put the
three `<img>` tags straight into `guarantee_label`, which would have placed them inside the hero
exactly where the dot points were. The Admin API rejected the whole push:

> Setting 'guarantee_label' is invalid. All top level nodes must be `<p>`, `<ul>`, `<ol>` or
> `<h1>`-`<h6>` tags and Tag `<img>` is not permitted

That is a server-side rule on `richtext` settings. Nothing was written — the mutation is atomic,
and a verify confirmed the file was still the reverted baseline. So the badges cannot live in that
field, and the only route into the hero's own markup is editing
`sections/custom-hero-section.liquid`, which renders **four** templates: `index`,
`page.about-us`, `page.7-day-reset`, `page.7-day-sitting`. Not worth four pages for a gap size.

**The honest downside.** Because it is a separate section, the badges sit below the hero's own
bottom padding — about 52px under the buttons on mobile, 120px on desktop — rather than the ~20px
the dot points had. Needs a look; the fix, if wanted, is the hero's `pb_mobile` / `pb_desktop`,
not a negative-margin hack.

**Also checked and rejected:** `sections/icon-subhead.liquid` sounded like a badge row but renders
a single image plus a heading. No existing section does a three-badge row.

**Markup safety.** Every image carries `width`/`height` attributes *and* inline
`width`/`height`/`object-fit`. The stylesheet was read first: nothing in `cstm-style.css` targets
an `img` inside the hero content, and inline styles win regardless. This is the exact inverse of
the comparison-section failure, which was an image with no pinned width at all.

The section's own `<style>` neutralises the `color-scheme-1 gradient` background via
`[id$='__badge_row']`, an attribute-suffix selector, because the rendered wrapper id carries a
template prefix that cannot be known ahead of time.

**Escaping.** All HTML uses single-quoted attributes, so the setting value contains no `"` at all
and nothing depends on quote-escaping surviving the trip to the Admin API. Rule 7 (`ensure_ascii`)
still applied to the body.

**Push record.** Theme `164208705793`: `c09cf9aa993654b9fa159e62180e295e` (19118 B) →
`c7d2e73f153d8ce89121009bd4c957d9` (20245 B), verified by `checksumMd5` on a fresh read. Live
theme `164124164353` re-checked in the same query: unchanged at `5d7e33bffcd39ae15a15d3903fe7b8a0`.
Assertions held: every other section byte-identical, all `block_order` untouched, existing render
order undisturbed apart from the insertion. Guard PASS.

**Not verified:** how it looks. No render harness. Needs Hamish's eyes on preview.

---

## S7b — Badge row fixed: teal band removed, PDP treatment adopted (2026-09-21)

Hamish sent two screenshots: the home page with the badges sitting on a **teal band** as white
tiles, and the ErgoRelief PDP showing what he actually wants — badge above, label below, three
columns, on white, with a hairline rule top and bottom.

**Two separate defects, both mine.**

**1. The teal band.** `config/settings_data.json` defines `scheme-1` as background `#1a7a6e` — the
brand teal. I had set `badge_row` to `"color_scheme": "scheme-1"` on the guess that scheme-1 meant
"default white". It does not. Now `scheme-2` (`#ffffff`, black text).

The `<style>` override I had written to neutralise it (`[id$='__badge_row'] .color-scheme-1
{background:transparent !important}`) did not take effect — the band rendered teal regardless. Not
investigated further, because the correct fix was never a CSS override; it was using the right
scheme. The section's own CSS now also sets `.sc-badges{background:#ffffff}` as a second line of
defence.

**The scheme table, so this is never guessed again:**

| scheme | background | text |
|---|---|---|
| scheme-1 | `#1a7a6e` (brand teal) | `#ffffff` |
| **scheme-2** | **`#ffffff`** | `#000000` |
| scheme-3 | `#fafafa` | `#000000` |
| scheme-4 | `#121212` | `#ffffff` |
| scheme-5 | `#334fb4` | `#ffffff` |

**2. The wrong image files.** The PDP block is `icon_with_text_yQWCyd` inside `main-product`, and
it uses `shopify://shop_images/free-ship.png`, `30-day.png`, `easy-return.png`. I had used
`1_e9a7bfbe….webp`, `2_b49003e3….webp`, `3_a6ed0058….webp` — the same artwork, but with white
baked into the file, which is exactly why they read as white tiles on the teal. Now using the
PDP's PNGs.

**The layout now mirrors the PDP:** three equal columns at every width, badge centred above its
label, hairline rules above and below, 900px max width, centred. 80px badges on desktop, 62px on
mobile.

Note the PDP's `icon-with-text` is a **block of `main-product`**, not a section, so it cannot be
reused on the home page. `sections/multicolumn.liquid` was considered and rejected: it only offers
1 or 2 columns on mobile (`columns_mobile`), and the PDP reference is 3 across on mobile.

**Copy.** Labels are the home page's own wording — "Express shipping from Australia", "30-day
money-back guarantee", "Easy returns". Deliberately *not* copied character-for-character from the
PDP, whose "30‑day" carries the retired U+2011 non-breaking hyphen.

**The guard did its job.** `check_template.py` refused the push:
`sections.badge_row.settings.color_scheme: 'scheme-2' (expected 'scheme-1')`. The lock was wrong,
not the change, so it was corrected in the same commit — which is the documented procedure for a
deliberate change to a guarded value.

**Push record.** Theme `164208705793`: `c7d2e73f153d8ce89121009bd4c957d9` →
`1154ed692c59e06099e2bca240345669` (20752 B), verified by `checksumMd5`. Live theme unchanged at
`5d7e33bffcd39ae15a15d3903fe7b8a0`. Assertions: only `badge_row.custom_liquid` and
`badge_row.color_scheme` changed; the hero section asserted byte-identical; order and every
`block_order` untouched.

**New rule 8.** Never guess a `color_scheme` value. Read `config/settings_data.json` →
`current.color_schemes` first. Scheme numbering is per-store and carries no standard meaning.

---

## S7c — Rules removed, gap closed (2026-09-21)

Hamish: *"Much better, now you need to remove two lines, move it up and fill the empty gap"* —
the two hairline rules out, and the dead white space between the buttons and the badges gone.

**Changed:** `badge_row.settings.custom_liquid` only. The hero section's settings were asserted
byte-identical; no `.liquid` file touched.

1. `border-top` / `border-bottom` removed from `.sc-badges__grid`.
2. The grid's own top padding dropped to 0 (bottom 28px desktop / 26px mobile, so the grey
   benefit section that follows does not crowd the labels).
3. Mobile badges 62 → 66px, now that there is room.
4. **The gap itself:** `.hero-banner{padding-bottom:14px !important}` inside a
   `max-width:749px` media query.

**Why the gap was ~120px and not 52px.** Measured off Hamish's screenshot: button bottom to the
top rule was about 285 screenshot px at a 920/390 ≈ 2.36 scale, so roughly 121 CSS px. That is
`pb_desktop` (120), not `pb_mobile` (52). The cause is the latent bug already logged against
`sections/custom-hero-section.liquid`: its mobile media query is **selector-less** —

```css
@media screen and (max-width: 749px) {
  {  padding-top: var(--pt-mobile) !important; ... }
}
```

— so the whole block is invalid and the mobile padding override never applies. `pb_mobile: 52`
has no effect; the desktop 120px governs mobile too.

*(This partly reinstates a finding I retracted in S5. The retraction was about padding-**top**,
where the rendered page showed no 120px gap above the photo. That observation stands. The
bottom padding is a separate measurement and it does show 120px. Both can be true — the hero's
background image is absolutely positioned, so the top is not a clean test of the rule.)*

**Why the fix is an override and not a settings change.** `pb_mobile` is inert, so changing it
does nothing. Lowering `pb_desktop` would fix mobile but wreck the desktop hero. Editing the
`.liquid` to repair the media query would touch a file shared by four templates. The override
lives in `badge_row`'s own `<style>`, which is rendered **only by the home template**, so
`page.about-us`, `page.7-day-reset` and `page.7-day-sitting` are untouched.

`!important` on a class selector beats the hero's non-important ID rule regardless of
specificity, so the outcome is deterministic whichever rule was previously winning — the fix does
not depend on my diagnosis being right.

**Push record.** `1154ed692c59e06099e2bca240345669` → `f895d769d5e58ac9e888c3d8a17715ee`
(20722 B), verified by `checksumMd5`. Live theme unchanged at `5d7e33bffcd39ae15a15d3903fe7b8a0`.
Guard PASS. Exactly one setting changed.

**Desktop deliberately left alone.** The 120px below the hero buttons on desktop is the hero's
intended airy spacing and Hamish has only been reviewing mobile. Not changed without seeing it.

---

## S7d — Desktop: smaller badges, under the CTA, gap closed (2026-09-21)

Hamish: *"the badges on mobile are fine but in desktop version they should be smaller and sit
below CTA"* — with a desktop screenshot of the current hero he doesn't like.

Three faults in that screenshot, all desktop-only:

1. Badges at 80px, too heavy for desktop.
2. The grid was `max-width:900px; margin:0 auto` — centred on the **page**, so it floated in the
   middle rather than sitting under the CTA, which lives in the hero's left column.
3. A large dead gap between the buttons and the badges.

**Changed:**

| | Before | After |
|---|---|---|
| `custom_hero_section_Yh4kcV.pb_desktop` | 120 | 36 |
| badge grid (desktop) | `max-width:900px; margin:0 auto` | `max-width:600px; margin:0` |
| badge image (desktop) | 80px | 56px |
| label (desktop) | 15px | 14px |
| gap (desktop) | 12px | 16px |

600px is not arbitrary — `.hero-banner__content` is `max-width:600px` in `cstm-style.css`, so the
badge grid now occupies exactly the hero's own content column and lines up under the buttons.

**Mobile is untouched:** 66px badges, full width, 3-up, and its own
`.hero-banner{padding-bottom:14px !important}` override still in force.

**A coupling worth remembering.** Because the hero's mobile media query is invalid (S7c), the
`pb_desktop` value governs **both** breakpoints. Dropping it 120 → 36 would have changed mobile
too, except that the badge_row override pins mobile to 14px with `!important`. So the two changes
are a pair: if that override is ever removed, mobile's bottom padding silently becomes whatever
`pb_desktop` is. Recorded in `locked.json`, and `pb_desktop` is now a guarded value.

**Side effect, stated plainly.** The hero's background image is `object-fit: contain`, so a
shorter section renders a slightly smaller photo. Reducing `pb_desktop` by 84px shrinks the hero,
and the photo with it. That is the intended trade — the dead space was the complaint — but it is a
visual change to the photo, not only to the spacing, and it needs Hamish's eyes.

**Push record.** `f895d769d5e58ac9e888c3d8a17715ee` → `cd46e12b6bb4df268cad556af9df7a20`
(20743 B), verified by `checksumMd5`. Live unchanged at `5d7e33bffcd39ae15a15d3903fe7b8a0`.
Exactly two settings changed; every other hero setting asserted byte-identical, so no copy moved.
Guard PASS after adding `pb_desktop`.

---

## S7e — iPad: the hero had no tablet rules at all (2026-09-21)

Hamish: *"what about ipads?"* with a tablet screenshot showing "See How It Works" sitting **behind
the hero photo**.

**Diagnosis — and it is a pre-existing theme bug, not something this session introduced.**

`assets/resposive.css` is where the hero's responsive behaviour actually lives. Its hero rules are
all inside `@media screen and (max-width: 749px)`:

```css
.hero-banner__bg      { position: static; }        /* photo stops being a background */
.hero-banner__overlay { display: none !important; }
.hero-banner__content { max-width: 100%; }
.hero-banner         { padding-top: 0 !important; }
.hero-banner__inner   { margin-top: 30px; }
```

Between **750px and 1024px there are no hero rules anywhere in the theme.** Tablets therefore fall
through to the desktop layout:

- `.hero-banner__bg` absolutely positioned, `object-position: right`
- `.hero-banner__overlay` = `linear-gradient(270deg, transparent 36.85%, #ffffff 46.38%)`, so white
  covers only the left ~53.6%
- `.hero-banner__content { max-width: 600px }` — about **78%** of a 768px iPad

Everything between 54% and 78% of the width sits on the photo with no white behind it. That is
exactly the button in the screenshot. Nothing about it is vertical, and this session's changes were
all vertical, so it predates them.

**Fix.** Extend the theme's own proven ≤749px treatment up to 1024px, replicated
declaration-for-declaration rather than invented, inside `badge_row`'s style block — which renders
only from the home template, so `page.about-us`, `page.7-day-reset` and `page.7-day-sitting` keep
the old behaviour. The photo stacks above the text on tablet, exactly as it already does on phones.

Badges at tablet: grid uncapped, 62px, sitting between the 56px desktop and 66px mobile sizes.

**Why not just widen the white gradient.** At 768px the hero photo is `object-fit: contain` and
ends up nearly full-width. Pushing the white far enough right to clear a 600px content column
(~82%) would bury almost the whole photo. Stacking is the only treatment that keeps both the words
and the picture.

**Correction to S7c, now that the real stylesheet has been read.** S7c said the hero's mobile
`padding-top` behaved because of settings. It does not — `resposive.css` carries
`.hero-banner { padding-top: 0 !important; }` at ≤749px. That, not `pt_mobile`, is why there is no
gap above the photo on phones. The selector-less media query inside `custom-hero-section.liquid` is
still invalid and still does nothing; the conclusion in S7c was right, the mechanism named for the
top was not.

Also found: `resposive.css` hard-codes
`#hero-banner-template--22073865371905__custom_hero_section_Yh4kcV { padding-bottom: 60px; }` — a
**different template id** from this theme's, so it is almost certainly dead. Either way the
badge_row override is `!important` and wins. Left alone.

**A smell worth naming.** `badge_row`'s style block is becoming a de-facto home-page stylesheet: it
now carries badge styling, a mobile hero padding override, and a whole tablet hero treatment. It
works and it is scoped, but the right long-term home is a proper snippet or a repaired
`custom-hero-section.liquid`. Not today — that file renders four templates.

**Push record.** `cd46e12b6bb4df268cad556af9df7a20` → `7f1ab390847cb149ed21379fe66c8564`
(21107 B), verified by `checksumMd5`. Live unchanged at `5d7e33bffcd39ae15a15d3903fe7b8a0`. Only
`badge_row.custom_liquid` changed; hero settings asserted byte-identical; the ≤749px block asserted
intact so signed-off mobile could not drift. Guard PASS.

**Not verified:** the tablet render. Needs Hamish's eyes at iPad width.

---

## S8 — Benefit section: desktop size (2026-09-21)

Hamish: *"feedback on copy and layout? my feedback, I think this section on desktop is too big"*.

**Copy verdict: keep it.** The heading — "Sitting all day is quietly straining your body." — is the
strongest line on the page; "quietly" does the work. The three labels are consistent noun phrases
and sit correctly as problem-agitation before the product is introduced. The one with the most bite
is "Lower back pain by midday" because it has a time anchor; the other two are slightly more
abstract. Not changed — no instruction to, and copy changes here need Hamish's call.

Noted but not touched: the heading value carries sloppy whitespace —
`<span>  straining </span>   your body.` — double and triple spaces. HTML collapses them, so there
is no visual effect. Left alone rather than spend a guarded-value change on nothing.

**Layout: he is right, and the numbers say why.** Measured from `cstm-style.css`, not from the
screenshot:

| | Before | After (desktop) |
|---|---|---|
| section padding | 100 top + 100 bottom | 65 + 65 |
| `.benefit-item-image` | 180×180, 30px padding | 140×140, 24px padding |
| `.benefit-item h4` | 24px/35px, max-width 254px | 19px/27px, max-width 232px |
| `.benefit-grid` | margin-top 30, gap 30 | 28 / 24 |
| `.heading-h2` (≥1025px) | 50px/60px | 42px/52px |

That was roughly 590px of section height to deliver three short phrases, 200px of it empty padding.
Now roughly 430px.

**Mechanism: per-section `custom_css`.** Shopify supports a `custom_css` array on a section in the
template JSON — the PDP already uses it on `apps_JXNAik`. Shopify scopes every rule to that one
section instance, so `cstm-style.css` is untouched and any other template using `benefit-section`
is unaffected. **Media queries work inside it** — confirmed by this push succeeding and the file
verifying byte-exact.

This is a much better tool than the previous pattern of stuffing overrides into `badge_row`'s
style block, and it is the right home for per-section styling from here on. The tablet/mobile hero
overrides in `badge_row` cannot move to it, though — they target the *hero* section, not the
section carrying the CSS.

Every rule is gated `min-width: 750px` (or 1025px for the heading) so the signed-off mobile layout
cannot move.

**A push was rejected first, correctly.** `padding_top_desktop: 64` returned
`Setting 'padding_top_desktop' must be a step in the range` — the schema declares `"step": 5`, so
only multiples of 5 are legal. Changed to 65. The mutation is atomic, so nothing was written and no
verify was needed to confirm the file was untouched.

**Rule 9.** Before setting a `range` value, read its `step` in the section schema. Shopify validates
it server-side and rejects the whole file.

**Push record.** `7f1ab390847cb149ed21379fe66c8564` → `3e45b721f022f1daadccc33fe7e60ddb`
(21586 B), verified by `checksumMd5`. Live unchanged at `5d7e33bffcd39ae15a15d3903fe7b8a0`.
Assertions: every other section byte-identical, the three benefit blocks (labels and icons)
byte-identical so no copy moved, only the two desktop paddings changed plus the new `custom_css`
key. Guard PASS.

**Not verified:** the render. Needs Hamish's eyes on desktop.

**Still open on this section:** the `corner-image` wave sits `bottom: -10px; right: 0` and is
clipped by the section edge on desktop; it is hidden entirely below 1024px. Worth a look, not
touched.

---

## S9 — One number for the daily reset, site-wide + Introducing copy (2026-09-21)

Hamish: *"lets first update the copy, FAQ should be 2-3 min too, update it in all pages"*, then
approved the proposed section copy with *"lets do the copy"*.

**The audit.** Parsed all 30 templates and walked every string value. The daily-reset duration was
stated in **12 places across 8 templates**, with **four different numbers**:

| Claim | Where |
|---|---|
| "Two minutes a day" | index — Introducing bullet |
| "2–3 mins/day" | index — How it works |
| "under 5 minutes a day" | all three PDP 7-Day Reset tabs |
| "5–10 minutes" | index FAQ, collection FAQ, ComfortBundle FAQ, faq-page, 7-day-sitting FAQ + hero, 7-day-reset hero |

All are being set to **2–3 minutes**, per Hamish.

Deliberately NOT changed, because they mean something else: "Soft cushions feel great for ten
minutes" (a different claim), "20-30 minutes into a desk day" (onset of pain), "the 20-Minute Rule"
(a Day-4 technique), "Each day takes a few minutes" (compatible, not contradictory).

**Method.** Replacements were applied to each template's **raw stored body** as literal string
substitutions, not by re-serialising parsed JSON — so every other byte is untouched by
construction, and formatting differences between templates (some end with a trailing newline,
index does not) cannot be disturbed. Each result was re-parsed as JSON before pushing and verified
by `checksumMd5` after.

**Done and verified byte-exact (5 of 8):**

| Template | md5 |
|---|---|
| `page.faq-page.json` | `8c0f118c75d300f7576d9a9444f60bb1` |
| `page.7-day-sitting.json` | `fc803e84c9c4dfaad029637ae0f67728` |
| `page.7-day-reset.json` | `9e97e8ba39db6d6d398f7b68ccf8ff6f` |
| `collection.custom-collection.json` | `1319a5d901d1fb389819db42d5cc02e1` |
| `index.json` | `665d900dd1a79d0e77e21a616de16331` |

**Still outstanding (3):** `product.ComfortBundle.json`, `product.ergoRelief.json`,
`product.lumbarEase.json` — each has "● Takes under 5 minutes a day" in its 7-Day Reset tab, and
ComfortBundle also has the 5–10 FAQ. Until these land the contradiction still exists, just moved.

**The Introducing section copy (index), approved:**

| | Before | After |
|---|---|---|
| subheading | …guided daily videos delivered to your phone. | …one short video a day, straight to your inbox. |
| bullet 1 | `<strong>Adaptive support -</strong> Memory foam…` | `<strong>Adaptive support</strong> — Memory foam…` |
| bullet 2 | …Two minutes a day. Seven days. A measurable difference. | …Two to three minutes a day. Seven days. No app, no login. |
| bullet 3 | …Better posture that sticks — long after day 7 | …Better posture that holds long after day 7. |

Reasoning: "delivered to your phone" implied an app, contradicting the FAQ's "no app, no login";
"a measurable difference" promised measurement the page never delivers, so it was swapped for the
no-app fact, which is concrete and differentiating; bullet 3 was missing its full stop and its
internal em dash fought the label dash. The em dash now sits **outside** `<strong>` so punctuation
is not bolded.

**Heading left alone.** "7-Day relief system" does repeat the hero eyebrow verbatim, but this is
the only place the system is named, and the eyebrow is a locked value. Flagged, not changed.

**A push was rejected first, and it was my error repeating itself.** `collection.custom-collection`
came back `Invalid JSON` because I wrote `\\\"` where the file needs `\"` in
`<a href="/pages/contact">` — the identical escaping slip from S6. The mutation is atomic so
nothing was written. **This is now the second time.** Any file containing an escaped quote gets that
line checked character by character before the call.

Live theme unchanged throughout at `5d7e33bffcd39ae15a15d3903fe7b8a0`.

**S9 continued — PDPs.** `product.lumbarEase.json` → `4635b2742ba60225a979da2a954ae2dd`
(27880 B) and `product.ergoRelief.json` → `a27e12b15c0aab8999fc25fc68c87418` (27846 B), both
verified by `checksumMd5`, both with "● Takes under 5 minutes a day" → "● Takes 2–3 minutes a day".
Sources were confirmed against the live working-theme checksums before building, so neither was
built on a stale copy.

**`product.ComfortBundle.json` is the last outstanding file** (39409 B). It needs two changes: the
same collapsible-tab bullet, and its FAQ `faq_Mt6Leh` "about 5–10 minutes" → "about 2–3 minutes".
Prepared locally and verified to parse: target `650bdbd03485b525ec44973562464eaa`, 39406 B.

**A note on method cost, for next time.** Whole-file rewrites are the only way Shopify lets you
change a template, so a one-line copy fix on a 39 KB PDP means re-sending all 39 KB by hand. That is
where the two escaping errors this session came from. For a change this small on a file this large,
the theme editor is the lower-risk tool; the API path is worth it when several values change at
once, as on the home page.

**S9 complete — and a much better push method found.**

`product.ComfortBundle.json` was the last file and the hardest: 39 KB containing two embedded
`<script>` blocks with triple-nested escaped quotes (`a[href^=\\\"/cart/add?\\\"]`). Hand-copying
42 K of escaped text is exactly where both of this session's escaping failures came from, so it was
not attempted.

**Base64 was considered and rejected** — `OnlineStoreThemeFileBodyInputType` accepts it, but 52 K
characters of base64 have no redundancy at all, so a single-character slip is invisible and the
whole file has to be re-sent.

**What worked: the `URL` body type.** `themeFilesUpsert` accepts
`body: { type: URL, value: <staged upload url> }`, so the file never has to pass through a tool
call as text:

1. `stagedUploadsCreate(resource: FILE, mimeType: "application/json", httpMethod: POST)`
2. `curl -F` the local file to the returned target with its signed parameters, file field last
3. `themeFilesUpsert` with `type: URL` pointing at `resourceUrl`

Google returned `ETag "650bdbd03485b525ec44973562464eaa"` on upload — the exact md5 expected — so
the bytes were proven correct *before* the theme write. The theme then verified at the same md5,
39406 B.

Two quirks worth knowing: `upsertedThemeFiles` came back **empty with no userErrors** for a URL
push, so success cannot be read from the mutation response — only the `checksumMd5` check confirms
it. And outbound HTTP is partly blocked here: `cdn.shopify.com` fails, but
`shopify-staged-uploads.storage.googleapis.com` is reachable (its 403 on the bucket root is a real
HTTP response, not a proxy rejection).

**Rule 10. For any theme file large enough that hand-copying is risky — and certainly anything with
nested escapes — use the staged-upload + `type: URL` route. It removes transcription from the
process entirely and the upload ETag proves the bytes before anything is written.** That supersedes
the earlier note suggesting the theme editor for these; this is better than both.

**Final site-wide audit**, all 30 templates re-fetched and every string walked:

| Phrase | Count | Verdict |
|---|---|---|
| "2–3 minutes" | 10, across all 8 templates | the single number, as intended |
| "2–3 mins" | 1 (index, How it works) | consistent |
| "a few minutes" | 3 (PDP tabs) | compatible, left alone |
| "20-30 minutes" | 1 (ErgoRelief, onset of pain) | different claim, left alone |

**Stale numbers remaining: none.** No "5–10 minutes", no "under 5 minutes", no "Two minutes".
