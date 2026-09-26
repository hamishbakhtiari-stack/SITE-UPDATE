# Video testimonials carousel — tablet sizing (26 Sep 2026)

- Live theme (untouched): `164269687041` "SitComfort — ErgoRelief PDP CRO"
- Working copy (duplicated from live first): `164379558145`
  "SitComfort — Video carousel tablet fix (Claude, DO NOT PUBLISH)"
- File changed: `snippets/video-reviews.liquid` only. It is the `video_reviews` block in
  `main-product`, used by product.ComfortBundle / product.ergoRelief / product.lumbarEase.
  `sections/video-reviews.liquid` (the separate section) is a different component and was not touched.
- Checksums: before `16e790514a1ccb51263eb9c217443cb1`, after `c04f0ef48ee9b08a3ad520b16e2f76fb`
  (the copy theme's checksum matches the local file).

## Change
Swiper breakpoints `0:2.5 / 600:2 / 900:4` became `0:2.5 / 600:3.3 / 990:4`. The pre-Swiper
CSS slide widths were updated to match: `calc((100% - 23px) / 3.3)` from 600px and
`calc((100% - 30px) / 4)` from 990px.

## Measured (harness: real theme CSS + Swiper 11.2.10, iframe at true width)
| Viewport | Before | After |
|---|---|---|
| 390×844 | 2.5 cards, 150×265 (ComfortBundle) / 134×236 (ergo/lumbar) | unchanged |
| 768×1024 | 2 cards, 295×522 | 3.3 cards, 175×309 |
| 1024×768 | 4 cards, 108×190 (2-col desktop layout) | unchanged |
| 1440×900 | 4 cards, 143×251 | unchanged |

Tablet range after the change: 158–216px wide and 279–381px tall; the tallest is at 749px on ComfortBundle.
Pre-Swiper widths equal post-Swiper widths at every width tested, so nothing jumps when Swiper loads.

`.video-card1 img { height: 420px }` (custom.css) matches nothing. The cards contain only
`<video poster>`, and the poster fills the 9:16 video box, so poster cards are never taller.
