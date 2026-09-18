# SitComfort Store Map

Snapshot taken 2026-09-18. **Verify before relying on it** — themes get
published and pages get added. The regeneration queries are at the bottom.

Store: SitComfort · `www.sitcomfort.com.au` · AUD · AEST · Basic plan.

## Published theme

| Field | Value |
|-------|-------|
| Name | `ComfortBundle carousel CLS fix (preview)` |
| ID | `gid://shopify/OnlineStoreTheme/163967992065` |
| Role | MAIN |

The store also holds several unpublished themes named `PWS || SitComfort`,
`Copy of PWS || SitComfort …`, and stock `Dawn`. Their names are near-identical,
so never pick a theme by name — always resolve MAIN through the API.

## Pages → templates

| Page | Handle | Published | Template |
|------|--------|-----------|----------|
| 7-Day Reset | `7-day-reset` | yes | `templates/page.7-day-reset.json` |
| 7-Day Sitting | `7-day-sitting` | yes | `templates/page.7-day-sitting.json` |
| About us | `about-us` | yes | `templates/page.about-us.json` |
| Contact | `contact` | yes | `templates/page.contact.json` |
| FAQ | `faq` | yes | `templates/page.faq-page.json` |
| Shipping & Delivery | `shipping-delivery` | yes | `templates/page.policy.json` |
| Returns, Refunds & Warranty | `returns-refunds-warranty` | yes | `templates/page.policy.json` |
| Terms & Conditions | `terms-conditions` | yes | `templates/page.policy.json` |
| Privacy Policy | `privacy-policy` | yes | `templates/page.policy.json` |
| Tester Program | `tester-program` | **no** | `templates/page.pf-3131add1.json` |
| Your Privacy Choices | `data-sharing-opt-out` | **no** | default `templates/page.json` |

Reading this table:

- **The four policy pages share `page.policy.json`**, which renders only
  `main-page` — their copy is the page `body` HTML, edited with `pageUpdate`.
  Editing that template changes all four at once.
- **Everything else is section-driven**: the copy lives in its own template JSON
  and `pageUpdate` on `body` will not show up. `page.faq-page.json`, for example,
  disables `main` entirely and renders a `FAQ` section whose blocks hold every
  question and answer.
- `page.pf-3131add1.json` is a page-builder app template. Editing it by hand can
  be overwritten by the app — prefer the app, or warn the user.

## Known SEO state

- `7-day-reset` carries `seo.hidden = 1` → `noindex,nofollow`, excluded from the
  sitemap. Intentional or not, mention it if the user asks about that page's
  search traffic.
- Most pages have no `global.title_tag`; `7-day-reset` has a
  `global.description_tag` stored with the legacy `string` type — match the
  existing type when updating it.

## Regenerate this map

```graphql
{ pages(first: 50, sortKey: UPDATED_AT, reverse: true) {
    nodes { title handle isPublished templateSuffix } } }
```
```graphql
{ themes(first: 3, roles: [MAIN]) { nodes { id name role } } }
```
```graphql
query T($id: ID!) { theme(id: $id) {
  files(first: 50, filenames: ["templates/page.*.json"]) {
    nodes { filename size checksumMd5 } } } }
```
