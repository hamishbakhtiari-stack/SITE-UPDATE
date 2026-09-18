# Page Records — `pageUpdate`, body HTML, SEO, publishing

The page record is the thin layer: title, handle, an HTML `body`, publish state,
which template renders it, and metafields. Everything visual usually lives in the
theme template (`theme-templates.md`).

Scopes: `write_content` or `write_online_store_pages`.

## Read a page

```graphql
query FindPage($q: String!) {
  pages(first: 5, query: $q) {
    nodes {
      id title handle isPublished publishedAt updatedAt
      templateSuffix
      body
      metafields(first: 20) { nodes { namespace key type value } }
    }
  }
}
```

Variables: `{"q": "handle:7-day-reset"}`. Other useful filters: `title:*reset*`,
`published_status:unpublished`, `updated_at:>2026-01-01`.

Fetch `body` only when you intend to edit it — some pages carry large HTML.

## Update a page

```graphql
mutation UpdatePage($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) {
    page { id title handle isPublished templateSuffix updatedAt }
    userErrors { code field message }
  }
}
```

`PageUpdateInput` — the complete field list:

| Field | Type | Notes |
|-------|------|-------|
| `title` | String | Shown in admin and, by default, as the SEO title |
| `handle` | String | The URL slug. Changing it changes the live URL |
| `body` | String | Page HTML. Only rendered by templates that output `page.content` |
| `isPublished` | Boolean | Visible on the storefront |
| `publishDate` | DateTime | ISO 8601; schedules visibility |
| `templateSuffix` | String | `"about-us"` → `templates/page.about-us.json`. `null`/`""` → default `templates/page.json` |
| `metafields` | [MetafieldInput!] | Namespace + key + value + type |
| `redirectNewHandle` | Boolean | With a new `handle`, auto-creates the 301 from the old URL |

Partial update: omitted fields are left alone. Passing `body` replaces the whole
HTML string — read it first, edit the substring, send the full result back.

There is **no `seo` field** on `PageUpdateInput`, and no `pageUpdate` shortcut
for meta tags. Use metafields (below).

## Editing `body` HTML

- Only templates that render `page.content` show it. On this store that is
  `templates/page.json` and `templates/page.policy.json` — i.e. the policy pages.
- Keep the theme's existing markup conventions; the theme styles `.rte` children,
  so plain `<h2>`, `<p>`, `<ul>` behave. Avoid inline `style` attributes and
  `<script>`.
- Escape for JSON transport, not for HTML: send real `<h2>`, not `&lt;h2&gt;`.

## SEO title and meta description

Stored as metafields in the `global` namespace, applied to the storefront's
`<title>` and `<meta name="description">`:

```graphql
mutation PageSeo($id: ID!) {
  pageUpdate(id: $id, page: { metafields: [
    { namespace: "global", key: "title_tag",       type: "single_line_text_field", value: "Returns, Refunds & Warranty | SitComfort" },
    { namespace: "global", key: "description_tag", type: "multi_line_text_field",  value: "30-day comfort guarantee, free returns across Australia…" }
  ]}) {
    page { id metafields(first: 10) { nodes { namespace key value } } }
    userErrors { code field message }
  }
}
```

- Read the existing metafields first: some were created with the legacy `string`
  type. Match the type already stored, or the write is rejected.
- Missing `title_tag` → Shopify falls back to the page title. Missing
  `description_tag` → search engines improvise from the page body.
- Practical lengths: title ≈ 60 chars, description ≈ 155 chars.
- `{ namespace: "seo", key: "hidden", type: "number_integer", value: "1" }` adds
  `noindex,nofollow` and drops the page from the sitemap. Deleting the metafield
  (`metafieldsDelete`) re-exposes it. Check this before debugging "why isn't this
  page ranking" — one SitComfort page already has it set.

## Creating a page

```graphql
mutation CreatePage($page: PageCreateInput!) {
  pageCreate(page: $page) { page { id handle } userErrors { code field message } }
}
```

Same field shape. To use a custom layout, create the template file first
(`templates/page.<suffix>.json`), then set `templateSuffix` to `<suffix>` —
pointing at a template that doesn't exist renders the default one with no error.

## Publishing

- `isPublished: true/false` flips storefront visibility immediately.
- `publishDate` in the future with `isPublished: true` schedules it.
- Unpublishing leaves the URL returning 404 — confirm with the user first, and
  consider a URL redirect (`urlRedirectCreate`) if the page had traffic.

## Deleting

`pageDelete(id:)` is permanent and breaks inbound links. Prefer unpublishing.
Always confirm with the user before calling it.
