# Collection page — review log

Page: `/collections/back-pain-relief-products`
Template: `templates/collection.custom-collection.json`
Reviewed: 2026-09-18. **Review only — nothing pushed.**

## Theme state (checked, do not assume)

| Theme | ID | Role |
|---|---|---|
| SitComfort — CRO fold redesign (Claude) | `164061970689` | **MAIN / live — never write** |
| SitComfort — Collection page CRO (Claude, DO NOT PUBLISH) | `164124164353` | **UNPUBLISHED — working theme** |

The PDP project's working theme (`164061970689`) has since been published, so the skill's theme-map
entry calling it "the unpublished duplicate" is stale.

Working duplicate created 2026-09-18T06:27:37Z from live. Copy verified clean — `checksumMd5` matches
live exactly on `templates/collection.custom-collection.json` (`4f65aaab…`),
`sections/comparison-table.liquid` (`afcee9a8…`) and `assets/cstm-style.css` (`493811c5…`).

**All writes go to `164124164353`. Publishing is the owner's decision, never mine.**
All findings below were read from the live theme as baseline.

## Scope note

All three collections (`frontpage`, `back-pain-relief-products`, `all`) use
`templateSuffix: custom-collection`, so they all render this one template. `templates/collection.json`
is an unused orphan. A change here changes all three collection pages.

## Local baselines (byte-verified against live `checksumMd5`)

`assets/base.css`, `assets/cstm-style.css`, `assets/custom.css`, `assets/resposive.css`
— all four md5-match live. Extracted via jq from the MCP overflow file, not transcribed.

## Verification method

- Code read directly from the theme (authoritative).
- Live rendered content from the owner's page crawl (2026-09-18).
- Layout measured in a local iframe harness at true 390/768/1280px against the four real CSS files.
- Storefront itself is unreachable from this environment (egress blocked), so anything needing the
  live DOM is marked "needs your eyes".

---

# Findings, in page order

## Page level

**P1. `banner` and `product-grid` are both `disabled: true`.**
Consequences:
- `main-collection-banner.liquid` holds the page's only `<h1>` (`collection-hero__title`). Disabled → no `<h1>` in the markup.
- `show_collection_description` is also `false`, and the section is off, so the ~350-word SEO description written for this collection **never renders**. Same for the `all` collection's description.
- The page ignores the actual collection: the three product cards are hardcoded blocks. `frontpage` has 1 product and still shows 3. No filtering/sorting.

**H1 discrepancy — unresolved.** The crawl labels "Choose Your Sitting Support" as H1; the markup
renders it `<h2 class="heading-h2">`. The same crawl labels an `<h6>` in section 3 as "H3", so its
heading levels look normalised rather than literal. One DevTools check settles it. Flagged, not assumed.

## Section 1 — Collection Products ("Choose Your Sitting Support")

**1a. Images have no reserved space → layout shift.** `<img src="..." alt="..." width="" height="">`
— both attributes empty, so no intrinsic aspect ratio, no `loading`, no `srcset`. Three cards.
Mobile CSS is `width:100%; height:auto`, so card height is unknown until each image loads.
`feature-highlight.liquid` in the same template already does this correctly via the `image_tag`
filter — same fix applies here. Relevant given two prior themes were named "CLS fix".

**1b. Oversized image payload.** Source is `image_url: width: 600`. Desktop slot is `max-height:200px`
(~200px wide); ≤1024 caps at `max-width:210px`. Serving 600px into a 200px box is ~9× the pixels.
Mobile (1-col, ~310px) is the only width where 600px is reasonable.

**1c. `custom_title` is dead.** Two blocks set `custom_title` to `{{ block.settings.product.title }}`,
but the section renders `{{ block.settings.title }}`. The setting is never read.

**1d. Naming violation (live).** ComfortBundle card: "a guided **7-Day Pain Relief Reset**".
Standard is "7-Day Reset" / "7-Day Reset Program". Theme-editor text field, no code change.

**1e. Hardcoded five stars.** Stars are the literal string `★★★★★` regardless of the actual value;
only the number next to it is real. Fine at 4.98/5.0, wrong if any rating drops.

Checked and **not** defects: star ratings render correctly ("5.0 (15)", "4.98 (50)") — the `rating`
metafield drop prints its value, confirmed in the crawl. The ghost CTAs on the two side cards keep a
visible teal border inherited from `.btn-globel--solid`. The empty "Save" badge case cannot occur —
all three products have compare-at prices.

## Section 2 — Comparison Table  ← the real problem

The section renders the table **twice**: a div-based version and a `<table>` version.
`cstm-style.css:2487` has `.comparison-table-wrapper table.comparison-table { display: none }`
with **no media query**, so the `<table>` is hidden at every width. Everything written for it —
including a complete, sensible mobile stacked-card treatment with per-row product labels — is dead code.
The visible version is the div one, and it has three defects:

**2a. ≤749px: the ComfortBundle column is entirely off-screen.** Measured at 390px:
`.page-width` gives 350px of content; the row-title column takes `min-width:130px`, leaving ~220px
for `.comp_table_main_row`, whose grid has three `min-width:130px` tracks = 390px. The overflow is
reachable only by horizontal swipe (`overflow-y:auto` forces `overflow-x:auto` per spec).
Result: ErgoRelief fully visible, LumbarEase cut mid-word, **ComfortBundle — the `active_column`,
the product the page is built to sell — not visible at all**, white highlight pill included.

**2b. 750–1024px: the marks area renders on dark teal.** `resposive.css` sets
`.comp_table_main_row { background:#1f8b7b }` at ≤1024, but the per-cell
`.row_cstm_colm { background:#fafafa }` only kicks in at ≤749. So between 750 and 1024px the
green ✓ (#00BC7D) sits on teal (#1f8b7b) at very low contrast and the grey ○ (#CAD5E2) reads as broken.

**2c. All widths: row labels are vertically offset from their marks (~13px on desktop).**
`.blankrow_th` has hardcoded heights (68.39px base, 48.8px ≤1024, 47px ≤749) meant to match the
header height. They no longer do — the `active-column` white pill adds height. The two flex columns
therefore start at different offsets and every label sits ~13px below its row of marks. On mobile the
mismatch also leaves a green sliver below the last row.

**2d. Duplicate sentence + U+2011.** `bottom_heading` = "Most customers choose the ComfortBundle™ for
full‑day relief in under 7 days. " repeats section 1's `best_value_body` almost verbatim. Section 1 uses
a plain hyphen; this one uses **U+2011** (non-breaking hyphen) — the exact character the standing rules
flag — and has a trailing space. Also it is a sentence marked up as `<h2>`.

**2e. Schema default uses a retired name.** Row `row_title` default is "7-day reset" (lowercase d).
Current blocks are correct; a newly added row would inherit the retired form.

**2f. `comparison-table.liquid` is CRLF.** Per the skill: push it as an escaped GraphQL string, never a
`"""` block string, or the line endings silently convert to LF.

Open question for the owner, not a change: ○ vs ✗. The crawl read ○ as "not included", so it is
inferable. **Icons are his — nothing to be restyled or substituted here.**

## Section 3 — Feature Highlight

**3a. Main image alt is a placeholder.** `image_alt` is unset in the template, so alt falls back to
the literal "Feature Image". Theme-editor field, no code change.

**3b. Heading levels go h2 → h6 → h4** within one section (`sub-heading-high` is an `<h6>` chosen for
styling). Reads as a level skip to screen readers and crawlers.

**3c. Tile copy is inconsistent** — "Ergonomic Designed" (ungrammatical), then a mix of Title Case and
sentence case: "Satisfaction guarantee", "Fast shipping from Australia" vs "Premium Memory Foam",
"30-Day Risk-Free Trial". All theme-editor text.

**3d. The guarantee has four names across this page** — "30-day money-back guarantee" (card),
"Satisfaction guarantee" + "30-Day Risk-Free Trial" (tiles), "the return period" (FAQ), and
"30-Day Comfort Guarantee" in the collection description. One name would read as one promise.
*(Naming only. Nothing here about who pays return postage, and no consumer-law angle.)*

## Section 4 — FAQ

Shared file, already carrying the PDP's `.faq-v2` work (`pre-line`, the 45° cross). Blast radius > 1 —
also used by the PDP and `page.faq-page.json`. Changes must stay opt-in.

**4a. Two retired names, live.** "the 7-Day **SitComfort** Reset Program" (Q2) and
"The 7-Day **SitComfort** Reset" (Q4). "SitComfort Reset" is explicitly retired. Theme-editor text.

**4b. Closing CTA stores a retired form.** `button_text` = "Ready to try it? Start your **7-day reset**"
(lowercase d). `text-transform: capitalize` may mask it visually, but the stored copy is wrong.

**4c. `show_logo` is true with no `logo_image` set** → renders nothing. Dead toggle.

**4d. Accordion is not accessible.** `<button class="custom-faq-question">` has no `aria-expanded`,
no `aria-controls`, no `type="button"`; the answer is not hidden from the a11y tree when closed.

Checked and **not** a defect: the arrow icon does rotate on open — base
`.custom-faq-item.active .custom-faq-icon { transform: rotate(180deg) }` covers the arrow variant.

---

# Parked (out of scope — raise only if asked)

- Announcement bar and all price/discount copy: **closed topic, not reopened.**
- `THANKYOU20 (-$46.80)` was live in the cart during the crawl, alongside the founding-customer offer.
  Noted here only because it appeared in the crawl; cart/promo, not this page.
- "Posture Quick-Reference Guide" still doesn't exist (carried over from the PDP project).
- `templates/collection.json` is an unused orphan template.

# Closed topics — do not raise

Pricing / anchoring / value-stacking. Consumer law. Who pays return postage. Icon design.
Ethics commentary on the review cards.

## ICONS — restated by the owner, 2026-09-18, absolute

*"never ever invent or create an icon you are terrible at that"*

Never invent, generate, create, substitute, restyle or recolour an icon. Ever. Use only the icon
assets already in the theme, as they are. Relabelling the *text* beside an existing icon is copy work
and is fine; touching the icon itself is not.

**Harness mocks:** do not use grey placeholder blocks where his icons go. The Shopify CDN is blocked
in this environment so real icons cannot load — render the reserved 60x60 box as an outlined box
carrying the icon's **filename**, so a mock can never be misread as a substituted icon. A caption is
not sufficient on its own; this has now caused concern twice (grey circles on the PDP harness, grey
squares on the collection feature-highlight mock).

# Next step

Owner picks what to action. Then: fresh unpublished duplicate → build locally → key-by-key parsed
diff → guard → push → re-pull `checksumMd5` and compare to local `md5sum`.

---

# CHANGE 1 — FAQ copied from the ComfortBundle PDP  (pushed 2026-09-18)

**Instruction:** make the collection FAQ exactly like the ComfortBundle PDP — copy, layout, all details.

**Target:** theme `164124164353` (unpublished). Live theme untouched and re-verified after the push
(`12406` / `4f65aaab…`, still MAIN).

**What was done.** `sections/faq_xz3t44` in `templates/collection.custom-collection.json` was replaced
wholesale with `sections/faq_bMxpUE` from `templates/product.ComfortBundle.json`. Asserted
programmatically that the two section objects are now **exactly equal**. Layout needed no work: both
pages already render the same shared `sections/FAQ.liquid`, which carries the PDP's `.faq-v2` fixes
(`white-space: pre-line`, the 45° cross). The section key `faq_xz3t44` was kept so `order` is untouched.

**Verification**
- Round-trip check first: re-serialising the untouched baseline reproduced it **byte-identically**, so the
  diff is only the intended change.
- Key-by-key parsed diff: **200 → 204 keys, 45 diffs, all under `/sections/faq_xz3t44/`. Zero diffs
  elsewhere.** Each of the other five sections asserted byte-identical. `order` unchanged.
- Guard `check_template.py` → PASS (22 assertions).
- Pushed as a TEXT GraphQL **variable**, not a `"""` block string — avoids the double-escaping trap
  entirely (the file has 818 quotes, 347 newlines, 26 backslashes).
- `checksumMd5` after push = `780299163b5623540d5b17eea6b27af8` = local `md5sum` of the pushed bytes.
  Confirmed by an **independent re-pull**, not just the mutation response.
- U+2011 in the comparison table's `bottom_heading` confirmed intact.

**Side effects, all intended (the PDP's values):**
- 5 FAQ items → **6** (adds "How do I access the 7-Day Reset?").
- `icon_style` `arrow` → `plus`, which activates the `.faq-v2` 45° cross rotation.
- Heading `Frequently asked / questions` → `Frequently Asked / Questions`.
- `bottom_text` now carries a real link: `Have more questions? <a href="/pages/contact">Contact us</a>`.
- Fixes findings **4a** and **4b** as a by-product: the retired "7-Day SitComfort Reset" (x2) and the
  lowercase "7-day reset" are gone. Verified zero retired forms remain in the FAQ.
- `4c` (`show_logo: true` with no `logo_image`) persists — the PDP has the same, so it is inherited
  by copying exactly, not introduced.
- `4d` (no `aria-expanded`) unchanged — it lives in the shared section file, not the template.

**⚠ One thing that cannot be "exactly like the PDP" — needs your call.**
`button_link` was copied verbatim as `/cart/add?id=49378080227585&quantity=1&return_to=/cart`.
On the PDP that opens the cart drawer, because the `custom_liquid_cartDrawerAjax` delegate inside the
PDP's `main` section intercepts `a[href*="/cart/add"]`. **That delegate does not exist on the collection
page.** So here the same link adds the bundle and hard-navigates to `/cart` — no drawer. It works, but
it is a different experience, and it is the one detail where exact parity is not achievable by copying
the setting. Previous value was `shopify://products/comfortbundle-complete-system` (went to the PDP).
One field to change either way.

---

# CHANGE 2 — Feature Highlight tile copy  (pushed 2026-09-18)

**Owner's position:** inclined to keep the section, invited a challenge. Challenge made; he approved
the copy change and rejected replacing the section with the PDP's version. Outcome: **section, layout
and all six icons kept. Six `title` fields changed. Nothing else.**

**Target:** theme `164124164353` (unpublished). Live re-verified untouched after the push
(`12406` / `4f65aaab…`, still MAIN).

## The challenge, and the evidence behind it

1. **Icon/label mismatch (a real defect).** `Mask_group_3.png` is the envelope — proven by the owner's
   own PDP screenshot, where that same file is labelled "Australian customer support". On the
   collection page it was labelled **"Built for Desk Workers"**. Envelope over a desk-worker claim.
2. **Four of six tiles restated copy already on the page**, and the FAQ push (Change 1) made it worse:
   - "Fast shipping from Australia" ↔ FAQ "Free express shipping across Australia… from our Sydney warehouse"
   - "Satisfaction guarantee" **and** "30-Day Risk-Free Trial" ↔ card "30-day money-back guarantee" ↔ FAQ
     "30-day money-back guarantee" — **four names for one promise on one page**
   - "Built for Desk Workers" ↔ section 1's "Designed for people who sit 6+ hours a day", and this
     section's own heading
3. **"Ergonomic Designed" was ungrammatical**, and casing was mixed Title Case / sentence case.
4. **The gap:** nothing on the collection page said stock, returns and support are physically in
   Australia — the differentiator against overseas dropshippers, already settled as the right message
   on the PDP.

## Why the PDP section was NOT copied wholesale (measured)

Measured in the iframe harness at a true 390px against the four real CSS files:

| variant | section height @390px | vs current |
|---|---|---|
| current (6 tiles) | 1119 px | — |
| PDP's 4 tiles | 1006 px | **−113 px** |
| approved copy change (6 tiles) | 1119 px | **0 px** |

The PDP's 4 tiles are 113px shorter, but `.feature-grid` is `repeat(3, 1fr)` above 991px
(`cstm-style.css:920`), so **4 tiles render 3 + 1 with an orphan on desktop**. Six divides evenly by
both 3 and 2; four does not. It would also have dropped the two product tiles and pulled in the PDP's
photo. Rejected on that basis.

*Parked, different page:* the PDP's own 4 tiles therefore render 3+1 above 991px. The owner's
screenshot looked like a clean 2×2 because it was a ~944px viewport at 2× DPR, which hits the
`≤991px → repeat(2, 1fr)` rule in `resposive.css:246`.

## What changed

| icon (UNCHANGED) | before | after |
|---|---|---|
| `Mask_group.png` | Ergonomic Designed | Ergonomically designed |
| `Mask_group_3.png` (envelope) | Built for Desk Workers | Australian customer support |
| `Mask_group_5.png` (shield) | Satisfaction guarantee | Returns go to Sydney, not overseas |
| `Mask_group_1.png` (truck) | Fast shipping from Australia | Ships from Sydney |
| `premium-memory-foam-icon.png` | Premium Memory Foam | Premium memory foam |
| `Mask_group_2.png` (calendar) | 30-Day Risk-Free Trial | 30 days to change your mind |

Settles the guarantee naming on one phrase ("30 days to change your mind" + the FAQ's
"30-day money-back guarantee"), and fixes finding **3c**.

## Verification

- Round-trip of the new baseline reproduced it **byte-identically** before editing.
- **204 → 204 keys, exactly 6 diffs, every one a `/settings/title`, all inside
  `feature_highlight_UWkmXn`.** Zero diffs elsewhere; the other five sections asserted byte-identical;
  `order` and `block_order` unchanged.
- **All six `icon` values asserted identical before and after** — the build aborts if any icon changes.
- Guard extended to 34 assertions and now **pins all six icon paths**, so a future write cannot
  silently change an icon. PASS.
- Pushed as a TEXT GraphQL variable. Post-push `checksumMd5` =
  `a4858fbd35a20ffd0a725848dd00bc38` = local `md5sum`, confirmed by an independent re-pull.

## Still open in this section

- `image_alt` is unset, so the main photo's alt is the literal string "Feature Image" (finding 3a).
  Raised; not approved in this change, so not touched. One theme-editor field.
- `heading` "Designed for People / Who Sit All Day" near-duplicates section 1's line. Raised as a
  separate question; owner has not ruled, and kept as is.
- **3b** (heading levels h2 → h6 → h4 inside the section) lives in `feature-highlight.liquid`, not the
  template — out of scope for a copy change.

---

# CHANGE 3 — Collection Products card alignment  (pushed 2026-09-18)

**Target:** theme `164124164353` (unpublished). Live re-verified untouched after both pushes
(`12406` / `4f65aaab…` and `8706` / `222d850a…`, still MAIN).

## The finding

`cstm-style.css:1634` sets `.collection-products .products-grid { align-items: center }`. Because the
ComfortBundle card is taller, the two side cards were vertically centred against it and nothing lined
up across the row. Measured in the harness at 1280px:

| | before | after |
|---|---|---|
| card top spread | **80 px** | **0 px** |
| ErgoRelief / LumbarEase top | y=390 | y=310 |
| ComfortBundle top | y=310 | y=310 |

Bottom spread goes from 81px to 161px, which is correct and intended: the bundle card is genuinely
taller because it alone carries the trust line and the "Most customers choose…" block. Tops aligned is
what makes the row scannable.

## The fix

One declaration, scoped, in the section's own `<style>` block:

```css
.cp-v2 .products-grid { align-items: start; }
```

**Shared section → opt-in setting.** `sections/collection-products.liquid` is also used by
`templates/collection.json` (the unused orphan template), so blast radius is 2. Following the house
pattern, the rule is gated behind a new `align_cards` checkbox defaulting to **false**, and enabled
only on `collection.custom-collection.json`. `collection.json` renders byte-identically to before.

## Measured cost: zero, at every width

| width | before | after | delta |
|---|---|---|---|
| 1500 | 1144 | 1144 | **0** |
| 1280 | 1163 | 1163 | **0** |
| 1100 | 1184 | 1184 | **0** |
| 1024 | 1727 | 1727 | **0** |
| 768 | 1696 | 1696 | **0** |
| 390 | 2271 | 2271 | **0** |

## Two approaches tried and rejected — recorded so they are not re-derived

1. **`margin-top: auto` on the price block** to pin CTAs to the card bottom. Rendered and rejected: it
   aligns the cards but punches a ~145px void into the middle of the two side cards, and the CTAs still
   do not align because the bundle has content *below* its button.
2. **`min-height` on `.custom-content`** to equalise description blocks so the price/CTA rows align
   exactly. Rejected on measurement: it is a magic number that only holds at one width. At 1025–1399px
   120px worked, but at ≥1400px (where `.page-width` caps and cards get wider) the bundle's description
   drops to 4 lines and the same rule **added 24px**. A tablet variant added **+72px at 768 and +120px
   at 1024**. Any fixed value breaks as soon as copy or width changes.

Consequence accepted: where descriptions differ in line count the star/price/CTA rows can still sit up
to ~24px apart. The honest fix for that is to even up the three description lengths in copy, not a CSS
hack. Raised with the owner; not actioned.

## Verification

- Section file: pulled to disk and checksum-matched live (`222d850a…`) before editing. LF file, zero
  backslashes, no `"""` sequence. Diff is exactly **3 hunks** (wrapper class, style rule, schema
  setting); schema re-parsed as JSON and the new `align_cards` id confirmed present; no CRLF introduced.
- Template: round-trip byte-identical before editing; **204 → 205 keys, exactly 1 diff**
  (`/sections/collection_products_7hQ9pr/settings/align_cards` absent → true); `order` and every
  `block_order` unchanged.
- Guard extended to 35 assertions. PASS.
- Both pushed as TEXT GraphQL variables. Post-push `checksumMd5`:
  `sections/collection-products.liquid` = `4cf4329421c57c39ad0b62890dc70fd9` (9138 bytes),
  `templates/collection.custom-collection.json` = `bc880091c3a33cc586e53484993976d1` (12582 bytes) —
  both equal to local `md5sum`, confirmed by an independent re-pull.

## Still open on this section (raised, not actioned)

- **Tablet orphan, 577–1024px:** `repeat(2, 1fr)` with 3 cards renders 2 + 1, leaving LumbarEase alone
  with a card's width of dead space. Proposed shape: bundle full-width on top, the two singles 2-up
  below. Needs a measured render.
- **Mobile length:** one card ≈ one full viewport; three cards + header ≈ three screens before the
  comparison table. Descriptions are 4–5 lines of **centred** 16px copy; left-aligning them on mobile
  would read better.
- **`.best-subheading` is `text-align: left` with `max-width: 285px`** inside an otherwise centred card,
  so "Free shipping • 30-day money-back guarantee • Easy returns" wraps with a dangling "• Easy returns"
  opening line two. Same dangling-separator class of bug as the PDP's `[br]` lesson.
- **Header stack:** ~100px between the teal one-line label and the cards (40px collapsed margin + 60px
  `.section-header` margin-bottom), and three tiers of header text.
- **Naming:** the ComfortBundle card still reads "7-Day Pain Relief Reset" (finding 1d).
- **CLS:** card images still carry `width=""` / `height=""` (finding 1a).

---

# CHANGE 4 — Main section copy  (pushed 2026-09-18)

Copy pass on `collection_products_7hQ9pr` — it had been skipped: the layout pass ran, then the layout
fix was built, without ever doing copy → icons → CTA for that section. Owner caught it.

Pushed to `164124164353` in three verified steps, each diffed key-by-key and guard-passed:

| # | change | diffs | checksum |
|---|---|---|---|
| 1 | bundle card: "7-Day Pain Relief Reset" → **"7-Day Reset"** (retired name) | 1 | `fc227a14c5c52bfc7f54a7efeb68bcf7` |
| 2 | header `body_text` "Designed for people who sit 6+ hours a day." → `""` (duplicated the sub-heading's job and the feature section's heading) | 2 | `5d067579703e04305ab287e134471819` |
| 2 | bundle description trimmed 5 lines → 4 ("the complete system for" dropped) so the price/CTA rows line up without CSS | (same push) | |
| 3 | comparison table `bottom_heading` → `""` — same sentence as the bundle card's `best_value_body`, and a full sentence marked up as an `<h2>` | 1 | `e5cab3145898d824dd287e21df855c46` |

All three checksums matched local `md5sum`. Blank settings are guarded by `{% if ... != blank %}` in
both sections, so nothing renders and every value is recoverable from the theme editor.

**Not re-measured.** The harness broke while building the comparison render and was abandoned rather
than spend more of the owner's budget. The claim that trimming the description evens up the rows is
reasoning from line counts, **not a measurement** — verify in preview.

## Still open on this section

- `.best-subheading` is `text-align: left` + `max-width: 285px` in an otherwise centred card, so
  "Free shipping • 30-day money-back guarantee • Easy returns" wraps with a dangling "• Easy returns".
- Dead settings: `custom_title` on the bundle and LumbarEase cards (never rendered by the section);
  `best_value_text: "BEST VALUE"` on ErgoRelief where the badge is off.
- Buttons judged correct as-is: "View ErgoRelief™" / "View LumbarEase™" vs "Start Your 7-Day Reset"
  is a deliberate browse-vs-act split.
- Tablet orphan (2+1 at 577–1024px) and the card images' empty `width=""`/`height=""` remain.

## Process note

Publishing is the owner's. The Shopify connector blocks theme publishing outright, so it can only be
done by him in admin: Online Store → Themes → Publish. Nothing in this project has ever gone live.
