---
name: shopify-page-update
description: "Update Shopify online store pages safely via the Admin GraphQL API (Shopify MCP). Use for editing page copy, headlines, hero text, FAQ answers, CTAs, images, section settings, SEO title/meta description, handles, publish status, or page templates. Covers both layers: page records (pageUpdate) and theme templates/sections (themeFilesUpsert). Triggers: update page, edit page copy, change headline, fix typo on site, update FAQ, edit landing page, change section, publish/unpublish page, page SEO, template suffix."
argument-hint: "[page-handle] [what to change]"
metadata:
  author: SitComfort
  version: "1.0.0"
---

# Shopify Page Update

Edit live Shopify online store pages through the Shopify MCP server without
breaking the theme. Store: **SitComfort** (`www.sitcomfort.com.au`, AUD, AEST).

## When to Use

- "Change the headline on the 7-Day Reset page"
- "Fix the typo in the FAQ answer about shipping"
- "Add a section to the About us page" / "reorder the sections"
- "Update the meta description for /pages/returns-refunds-warranty"
- "Unpublish the Tester Program page" / "change a page handle"
- Any copy, image, or layout change to a `/pages/*` URL

Not for: product pages (`templates/product.*.json`, use product tooling for
product fields), collections, blog articles, or checkout. The theme-file
mechanics below still apply if you do touch those templates.

## The Two Layers — Decide This First

A Shopify page URL is rendered from **two** separate records. Editing the wrong
one silently does nothing on the live page.

| Layer | Holds | Edited with |
|-------|-------|-------------|
| **Page record** (`gid://shopify/Page/…`) | title, handle, `body` HTML, publish state, `templateSuffix`, metafields | `pageUpdate` |
| **Theme template** (`templates/page.<suffix>.json`) | every section, block, setting and most visible copy | `themeFilesUpsert` |

Rule of thumb: **if the page has a `templateSuffix`, the visible content is
almost certainly in the theme template, not in `body`.** Most SitComfort pages
do (`7-day-reset`, `about-us`, `faq-page`, `contact`, `policy`, …). See
`references/store-map.md`.

The one exception: pages on `templates/page.json` or `page.policy.json` render
`page.content` — that copy *is* the `body` field, so `pageUpdate` is correct.

## Workflow

### 1. Locate the page

```graphql
{ pages(first: 5, query: "handle:7-day-reset") {
    nodes { id title handle isPublished templateSuffix bodySummary updatedAt } } }
```

Run with `mcp__Shopify__graphql_query`. Note the `id` and `templateSuffix`.

### 2. Pick the layer

- `templateSuffix` is null or `policy` → the copy is in `body` → **step 4a**.
- `templateSuffix` is set → open `templates/page.<suffix>.json` → **step 4b**.
- Copy is not in either → it is hardcoded in `sections/<type>.liquid` or a
  snippet → **step 4c** (rarer; only edit Liquid when a setting can't do it).

### 3. Take a backup — always, before the first write

The main theme is live. Duplicate it, or save the exact current file body to the
scratchpad so a rollback is one upsert away. See
`references/safety-and-rollback.md`. Never skip this for theme-file edits.

### 4a. Page record edit

```graphql
mutation UpdatePage($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) {
    page { id title handle isPublished updatedAt }
    userErrors { code field message } } }
```

`PageUpdateInput` accepts only: `title`, `handle`, `body`, `isPublished`,
`publishDate`, `templateSuffix`, `metafields`, `redirectNewHandle`. It is a
partial update — send only what changes. **There is no `seo` field**; page SEO
lives in metafields (`references/page-content.md`).

Changing a handle changes the live URL — pass `redirectNewHandle: true` so the
old URL 301s, and say so in your summary.

### 4b. Theme template edit (most page edits)

1. Read the current file from the **MAIN** theme (`references/theme-templates.md`
   has the query).
2. Save it to the scratchpad unchanged — that is the rollback copy.
3. `python3 scripts/theme_json.py outline <file>` to find the section holding the
   copy, then make the **minimal** edit to that one setting.
4. `python3 scripts/theme_json.py diff <before> <after>` and confirm only the
   intended keys moved.
5. Upsert the whole file with `themeFilesUpsert` (it replaces the file entirely).

Hard rules: keep the auto-generated `/* … */` banner, keep existing section and
block IDs byte-identical (`order` and `block_order` reference them), never
reformat the whole file, never invent a `type` that has no matching
`sections/<type>.liquid`.

### 4c. Liquid section edit

Same read → back up → minimal edit → upsert loop, on `sections/<name>.liquid`.
Changing a section's `{% schema %}` can drop merchant-entered settings — read
`references/theme-templates.md` before touching schema.

### 5. Verify

- Re-query the page or file and check `updatedAt` / `checksumMd5` changed.
- Live URL: `https://www.sitcomfort.com.au/pages/<handle>`
- Unpublished theme: `https://www.sitcomfort.com.au/pages/<handle>?preview_theme_id=<numeric id>`
- Report exactly what changed, on which theme, and the rollback path.

## Guardrails

- **Read before every write.** Upserts replace the whole file; a blind write
  discards whatever the theme editor changed since you last looked.
- **Confirm before anything outward-facing and hard to reverse**: publishing or
  unpublishing a page, changing a handle, publishing a theme, or deleting a
  section. Copy fixes on an already-live page are ordinary work — just do them.
- **One page, one change set.** Don't tidy unrelated sections along the way.
- No built-in Shopify MCP tool covers pages or themes — go through
  `graphql_query` / `graphql_mutation`, and `graphql_schema` /
  `search_docs_chunks` when you need to check a field before using it.
- Always select `userErrors { field message }` and treat a non-empty array as a
  failure, even when HTTP 200 comes back.

## References

| Topic | File |
|-------|------|
| Page records, body HTML, SEO metafields, publishing | `references/page-content.md` |
| Theme JSON templates, sections, blocks, Liquid, upserts | `references/theme-templates.md` |
| Copy-paste queries and mutations | `references/graphql-recipes.md` |
| Backups, previews, rollback, verification | `references/safety-and-rollback.md` |
| Live page → template map for this store | `references/store-map.md` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/theme_json.py` | Parse/outline/patch/diff theme JSON templates (handles the auto-generated banner). Python 3, no dependencies. |
