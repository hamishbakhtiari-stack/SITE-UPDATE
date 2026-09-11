# SitComfort — Home Hero Redesign Spec

Scope: home page hero (above-the-fold) only. Overrides nothing else on the site.
Source of truth for the rebuild in `sections/hero-banner.liquid` and `preview/hero.html`.

## 1. Diagnosis of the current hero

Observed on `sitcomfort.com.au` (mobile, iOS Safari):

| # | Issue | Severity | Why it costs money |
|---|---|---|---|
| H1 | Image consumes the entire first viewport. Headline, value prop and CTA all sit below the fold. | Critical | The first screen sells nothing. A visitor must scroll before they learn what is sold or why. |
| H2 | No price and no offer in the hero. The announcement bar promises "Save $51" and the hero never reinforces it. | Critical | The strongest lever (a real $51 saving off a $168 anchor) is spent on a 32px bar and then dropped. |
| H3 | Zero social proof above the fold — no rating, no review count, no "Australian owned". | High | Unknown brand + $117 price + no proof = the visitor leaves to check Amazon. |
| H4 | Two CTAs at near-identical visual weight ("Start Your 7-Day Reset" / "See How It Works"). | High | Splits intent. A primary CTA needs a clear weight advantage over the secondary. |
| H5 | Primary CTA label is not commerce-clear. "Start Your 7-Day Reset" does not signal add-to-cart. | High | Ambiguous CTAs depress click-through; the visitor cannot predict what happens next. |
| H6 | Trust points are a plain bulleted list in body-copy weight. | Medium | Reads as paragraph, not as reassurance. Not scannable in the 2–3s scan window. |
| H7 | Large dead whitespace between the bullets and the next section. | Medium | Wastes the most valuable screen real estate on the site. |
| H8 | Eyebrow text clips behind the sticky header on scroll. | Medium | Looks broken; erodes the "premium" positioning. |
| H9 | Product is barely visible — grey cushion on a grey chair in a low-contrast room. | Medium | The thing being sold is not legible at thumbnail size. |

## 2. Redesign principles

1. **Offer-first, not image-first.** On mobile the order becomes rating → headline → subhead → image → price+save → CTA. The image is capped by `aspect-ratio`, never full-bleed-tall, so the CTA lands inside the first viewport on a 390×844 device.
2. **One primary action.** Solid teal `Add ComfortBundle — $117` at full width. The secondary becomes a low-weight text link, not a second pill.
3. **Proof before price.** Rating row sits above the headline so credibility is established before the number is seen.
4. **Price anchoring in the hero.** `$117` next to struck-through `$168` and a `SAVE $51` chip — the same offer the announcement bar makes, finally cashed in.
5. **Risk reversal adjacent to the CTA.** The 30-day guarantee sits directly under the button, where hesitation actually occurs.
6. **Trust strip as icons, not bullets.** Three SVG + label pairs in a row.

## 3. Tokens (brand palette is fixed — not up for redesign)

| Token | Value | Use |
|---|---|---|
| `--sc-teal` | `#1A7A6E` | Primary CTA fill, links, eyebrow |
| `--sc-teal-dark` | `#14615A` | CTA hover/active |
| `--sc-teal-tint` | `#E8F2F0` | Section wash, chip backgrounds |
| `--sc-gold` | `#C9A84C` | Star fills, SAVE chip fill |
| `--sc-cream` | `#F9F6F0` | Hero background |
| `--sc-ink` | `#1C1C1C` | Headings, body |
| `--sc-muted` | `#5A5A56` | Subhead, secondary text |
| `--sc-line` | `#E2DED4` | Hairlines, borders |

### Contrast verification (WCAG 2.2 AA)

| Pair | Ratio | Result |
|---|---|---|
| `#1A7A6E` on `#FFFFFF` | 5.23:1 | Pass (normal text) |
| `#FFFFFF` on `#1A7A6E` (CTA) | 5.23:1 | Pass |
| `#1C1C1C` on `#F9F6F0` | 16.4:1 | Pass |
| `#5A5A56` on `#F9F6F0` | 6.43:1 | Pass |
| `#1C1C1C` on `#C9A84C` (SAVE chip) | 7.48:1 | Pass |
| `#C9A84C` on `#FFFFFF` | 2.28:1 | **Fail — gold is never used for text.** Gold is restricted to star glyphs and chip fills, and every star row is paired with a text equivalent ("4.8 out of 5"). |

## 4. Type scale

| Role | Mobile | Desktop | Spec |
|---|---|---|---|
| Eyebrow | 13px | 14px | 600, `letter-spacing: .08em`, uppercase |
| Headline | `clamp(34px, 8.5vw, 44px)` | 60px | 700, `line-height: 1.08`, `text-wrap: balance` |
| Subhead | 17px | 19px | 400, `line-height: 1.5` |
| Price | 32px | 38px | 700 |
| CTA | 17px | 17px | 600 |
| Trust strip | 13px | 14px | 500 |

## 5. Layout

- **Mobile (< 900px):** single column, 20px side gutters, image at `aspect-ratio: 4/3` with `object-fit: cover`.
- **Desktop (>= 900px):** two columns `1.05fr / 1fr`, copy left, image right at `aspect-ratio: 4/5`, with a floating proof card overlapping the image's lower-left corner.
- Image uses `width`/`height` + `aspect-ratio` so no CLS. Hero image is `fetchpriority="high"`, `loading="eager"` (it is the LCP element); everything below stays lazy.

## 6. Accessibility

- Single `<h1>` in the hero.
- Star rating is `role="img"` with an `aria-label` carrying the full text value; decorative SVGs are `aria-hidden="true"`.
- All interactive targets >= 48px tall (exceeds the WCAG 2.2 24px minimum and the 44/48 native guidance), 8px+ gaps.
- Visible `:focus-visible` ring at 3px, never removed.
- `prefers-reduced-motion: reduce` collapses the entrance fade to the final state.

## 7. Copy

**Shipping copy**

- Eyebrow: `The 7-Day Relief System`
- H1: `Sit longer without pain — in 7 days.`
- Sub: `The seat cushion, lumbar support and guided reset program for people who sit 6+ hours a day.`
- Primary CTA: `Add ComfortBundle — $117`
- Secondary: `See how the 7-Day Reset works`
- Reassurance: `30-day money-back guarantee · Free express shipping Australia-wide`

**A/B alternates for the H1** (same layout, swap the string):

- B — pain-led: `Your chair isn't the problem. Your lower back is.`
- C — objection-led: `You've tried the $1,000 chair. Try the $117 fix.`

## 8. Claims risk — read before publishing

"in 7 days" is a health-outcome claim. Risk register item **R2 (no physiotherapist backing)** is still open. Without a named practitioner endorsing the program, this phrasing is exposed on two fronts: Meta ad policy on health claims, and ACCC rules on misleading representations. The layout does not depend on the claim — if R2 stays open, swap the H1 for alternate **B** or **C** above and the design is unaffected. This is a copy decision, not a design blocker.

Review counts and star ratings in this hero must be wired to real review data before publishing. The section renders the rating block only when `show_rating` is enabled, so it ships **off** by default rather than hardcoding numbers the store cannot yet substantiate.
