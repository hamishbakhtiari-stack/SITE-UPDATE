---
name: shopify-page-update
description: >
  Safely redesign and edit Shopify theme pages for the SitComfort store — product pages (PDPs),
  landing pages, sections and theme files — with a CRO review process, a verified write protocol
  and a pixel-accurate render harness. Use this skill whenever the user wants to change, review,
  redesign, audit or fix anything on their Shopify site: a product page, a section, copy, layout,
  spacing, a CTA, an FAQ, reviews, a banner, mobile rendering, or a theme file. Also use it when
  they mention SitComfort, ComfortBundle, ErgoRelief, LumbarEase, the 7-Day Reset, a theme ID, a
  template JSON, a .liquid section, or ask to "check the page", "improve conversion", "make it
  look better on mobile", or "why does this look wrong". Use it even when the request sounds like
  a one-line tweak — the write protocol and the standing rules apply to every edit, and skipping
  them is how live sites get broken.
---

# Shopify page update — process, rules and hard-won details

This skill encodes a full PDP redesign that ran across eleven sections of the SitComfort
ComfortBundle product page. Most of what follows is not theory. It is the residue of specific
mistakes, each of which cost real time, and specific instructions from the store owner, each of
which he had to repeat before it stuck.

Read `references/standing-rules.md` **before writing anything**. Those rules override your own
judgement, including when your judgement is right.

---

## The two things that matter most

**1. Never write to the live theme.** All work happens on an unpublished duplicate. The Shopify
connector enforces this, but do not rely on the enforcement — confirm the theme ID before the
first write and keep using it. Publishing is the owner's decision, never yours.

**2. Verify every push by checksum.** After every `themeFilesUpsert`, re-query the file's
`checksumMd5` and compare it to a local `md5sum` of the exact file you built. If they differ, you
changed something you did not intend to. This check caught a real transcription bug that six
layers of careful reading had missed. It costs one query. Run it every time.

---

## Working rhythm

Go **section by section, in page order**. Inside each section, review in this order:

**layout → copy → icons → CTA**

Do not jump ahead. Raising a later section's problem while working an earlier one reads as
unfocused and derails the review. If you notice something out of scope, write it in the decisions
log and raise it when you reach that section.

For each section:

1. **Pull the current state** — the template JSON and any section `.liquid` it uses.
2. **Check blast radius** — before rewriting a section file, confirm which templates render it
   (grep every template in the theme). A section used by two pages needs an opt-in setting, not a
   hard-coded change. See "Shared sections" below.
3. **Diagnose with measurements, not impressions.** Render it. Measure it. "It feels cramped" is
   a starting point; "the price row is a 40px box around an 18px line" is a finding.
4. **Propose, with the reasoning and a mock.** One recommendation, not a menu of options.
5. **Get approval.** Layout and copy can ship together if the owner asks for that.
6. **Build locally, diff key-by-key, run the guard, push, verify by checksum.**
7. **Report plainly** — what changed, what you measured, what you could not verify.

---

## The write protocol

Full detail in `references/safe-push.md`. The shape of it:

```
snapshot live  →  build candidate locally  →  diff parsed key-by-key vs live
              →  run guard script          →  push
              →  re-pull checksumMd5       →  compare to local md5sum
              →  update baseline + decisions log
```

Two rules that exist because breaking them cost hours:

- **Inside a GraphQL `"""block string"""`, copy the file's bytes verbatim.** Backslashes are
  already literal there. Adding escapes silently corrupts embedded JavaScript and CSS. This
  produced a 16-byte drift that the checksum caught and nothing else would have.
- **Diff the parsed structure, not the text.** Flatten both JSON documents to leaf paths and
  compare. You want to be able to say "424 keys, exactly these 6 changed" — anything else means
  you do not actually know what you are shipping.

Keep a `check.py` guard listing settings that were hard-won (see `scripts/check_template.py`).
Non-zero exit means do not push. When the owner deliberately changes a guarded value, update the
guard in the same commit and say so.

---

## Verifying what it looks like

You cannot see the storefront from this environment. `cdn.shopify.com` is blocked, app blocks
(Judge.me, Klaviyo) will not render, and webfonts are unavailable. So build a local harness with
the theme's real CSS files and measure against that. Full recipe in `references/render-harness.md`.

The single most expensive trap:

> **Headless Chromium clamps `--window-size` width to roughly 500px.** Asking for 390px silently
> renders at ~500px. Text wraps differently, so every line count and height you measure is wrong —
> and wrong in the direction that makes mobile look better than it is. Render inside an **iframe**
> sized to the real width instead.

An early spacing estimate given to the owner was built on a clamped render and was simply wrong.
Measure through the iframe harness, then quote numbers.

**Label every mock.** If a harness uses placeholder shapes or fallback fonts, say so in the same
breath as the image. The owner once saw grey circles where his tick icons go and reasonably
concluded his icons had been replaced. They had not. A one-line caption prevents that.

---

## Prefer evidence over opinion

The store's own data settles most arguments faster than reasoning does, and it is right there:

- **Behavioural questions → order history.** "Will removing the quantity selector cost sales?"
  was answered by querying 72 orders: 2 were multi-unit (2.8%), and both were multi-product carts
  whose buyers reached the cart drawer anyway. That turned a debate into a decision.
- **Image and video sizing → the Files API.** Real dimensions turn "the crop looks off" into
  "a 554×972 thumbnail forced into a 287×384 box loses 24% of every frame".
- **Real reviews → the `judgeme.review_widget_data` product metafield.** They are already in the
  store; no export needed.
- **Which templates use a section → grep every template** before touching a shared file.

---

## CSS strategy for this theme

The theme layers `base.css` → `section-*.css` → `cstm-style.css` → `custom.css` → `resposive.css`,
with plenty of duplicated and contradictory rules. Do not edit the global files. Instead:

- Add a **scoped version class** (`.ergo-v2`, `.vr-v2`, `.faq-v2`, `.cta-v2`) on the section
  wrapper and write new rules under it, inside that section's own `<style>` block. A two-class
  selector (specificity 0,2,0) beats the global single-class rules (0,1,0) at every breakpoint,
  so you rarely need `!important` and never need to fight the cascade.
- **Shared sections get an opt-in setting, never a hard-coded change.** The CTA banner is used by
  both the PDP and the About Us page. Centring it meant adding a `center_layout` checkbox
  defaulting to `false`, then enabling it on the PDP only. The other page renders exactly as
  before. This pattern is almost always the right answer when blast radius > 1.
- **Section `custom_css` in template JSON does not reliably support media queries.** Use `clamp()`
  to scale a value with viewport in a single declaration.
- **Liquid does not HTML-escape `{{ }}`.** You can put real HTML into a `text` or `textarea`
  setting — which is how a contact link got into the FAQ with no code change at all. Reach for
  this before editing a section file.

`references/theme-map.md` has the file inventory, the class names that matter, and the live
quirks (including a wrapper class spelled `.bullte-points` and a cart delegate that intercepts
every CTA on the page).

---

## Spacing and typography: standards, not vibes

When asked to tighten a layout, it is easy to squeeze uniformly and end up with something that
reads as cramped. The owner pushed back on exactly this, and he was right. Hold these lines:

- **16px is the mobile body-text minimum.** It is also the threshold below which iOS zooms the
  page on input focus.
- **Body line-height 1.5.** This is what WCAG 1.4.12 expects text to support.
- **Display and heading text: 1.1–1.3.** A 26px price sitting in a 40px line box is dead air, and
  fixing that is not "tightening" — it is removing a defect.
- **Spacing scale, not a flat value.** On an 8-point grid, ~16px separates distinct content
  groups. Dropping every gap to 10px is what makes a page feel packed.

**Get vertical space by removing blocks, not by squeezing type.** Disabling one unused quantity
selector recovered 91px — more than every micro-adjustment combined, with zero crowding. Look for
the block that does not earn its place before you touch the rhythm.

---

## Reporting

The owner reads on a phone and gives blunt feedback. Respect that:

- Lead with what changed and what you measured.
- Send deliverable images **separately, at 2× device scale**, one view per image. Never a contact
  sheet of four frames — it is unreadable at phone size.
- State plainly what you could **not** verify and what needs his eyes (app blocks, video refs,
  anything requiring the live storefront).
- When you get a number wrong, correct it in one sentence with the real number and move on.

---

## Reference files

- `references/standing-rules.md` — the owner's non-negotiables. **Read first, every time.**
- `references/safe-push.md` — the write/verify protocol and Shopify GraphQL mechanics.
- `references/render-harness.md` — building a pixel-accurate local render, and its traps.
- `references/theme-map.md` — theme inventory, class names, known quirks.
- `references/lessons.md` — every mistake made on this project and the rule that prevents it.
- `scripts/check_template.py` — pre-push guard for settings that must not regress.
- `scripts/locked.example.json` — a filled-in guard config from the ComfortBundle PDP; copy and adapt per page.
- `scripts/diff_template.py` — key-by-key diff of two template JSON files.

Both scripts are plain Python 3 with no dependencies. Run `diff_template.py` before every push
and `check_template.py` as the gate — a non-zero exit means stop.
