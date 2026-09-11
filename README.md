# SitComfort — Home Hero Redesign

Redesign of the above-the-fold hero on [sitcomfort.com.au](https://www.sitcomfort.com.au).

## Files

| Path | What it is |
|---|---|
| `sections/hero-banner.liquid` | The shipped section. Drop into the theme, add via the theme editor. Self-contained — no theme CSS, JS or snippet dependencies. |
| `preview/hero.html` | Standalone preview: before/after at one phone viewport, plus the desktop layout, the change table, contrast checks and headline variants. Open directly in a browser. |
| `design-system/sitcomfort/pages/hero.md` | Spec: the nine issues found, redesign principles, tokens, type scale, contrast results and copy variants. |
| `assets/hero-comfortbundle.jpg` | Hero photograph, cropped and optimised (960×669, 66 KB). |

## Installing the section

1. Shopify admin → **Online Store → Themes → ⋯ → Edit code**
2. **Sections → Add a new section**, name it `hero-banner`
3. Replace the generated contents with `sections/hero-banner.liquid`
4. **Customize** the home page template → **Add section → SitComfort Hero**
5. Set **Hero product** to ComfortBundle™ Complete System — price, compare-at price, saving and add-to-cart all derive from the variant, so nothing is hardcoded

Remove the old hero section once the new one is in place.

## Section settings

Everything is editable in the theme editor: eyebrow, headline (rich text — `<em>` renders teal), subheading, button label, the secondary link, the reassurance line, and up to four trust points with icons.

Two settings ship **off** on purpose:

- **Show star rating** — renders no rating until there is real review data behind it.
- **Proof card** — the desktop overlay card is blank until given a stat that can be substantiated.

## Before publishing

The headline `Sit longer without pain — in 7 days.` is a health-outcome claim, and risk register item **R2 (no physiotherapist backing)** is open. Two alternates that carry no such claim are in the spec, and swapping either one in leaves the layout untouched.
