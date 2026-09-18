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
