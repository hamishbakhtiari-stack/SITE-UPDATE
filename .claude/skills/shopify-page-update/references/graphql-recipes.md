# GraphQL Recipes

Run these with `mcp__Shopify__graphql_query` (reads) and
`mcp__Shopify__graphql_mutation` (writes). Check an unfamiliar field with
`mcp__Shopify__graphql_schema` (`type_name` is required) or
`mcp__Shopify__search_docs_chunks` before using it.

## List pages

```graphql
{ pages(first: 50, sortKey: UPDATED_AT, reverse: true) {
    nodes { id title handle isPublished updatedAt templateSuffix } } }
```

## Find one page by handle

```graphql
query P($q: String!) {
  pages(first: 5, query: $q) {
    nodes { id title handle isPublished templateSuffix updatedAt
            metafields(first: 20) { nodes { namespace key type value } } } } }
```
`{"q": "handle:about-us"}`

## Page body (only when editing it)

```graphql
query Body($id: ID!) { page(id: $id) { id handle body } }
```

## Update page fields

```graphql
mutation U($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) {
    page { id title handle isPublished templateSuffix updatedAt }
    userErrors { code field message } } }
```
```json
{ "id": "gid://shopify/Page/134630834433",
  "page": { "title": "About Us", "isPublished": true } }
```

## Set SEO metafields

```json
{ "id": "gid://shopify/Page/…",
  "page": { "metafields": [
    { "namespace": "global", "key": "title_tag",       "type": "single_line_text_field", "value": "…" },
    { "namespace": "global", "key": "description_tag", "type": "multi_line_text_field",  "value": "…" } ] } }
```

## Create a page

```graphql
mutation C($page: PageCreateInput!) {
  pageCreate(page: $page) {
    page { id handle } userErrors { code field message } } }
```

## Main theme ID

```graphql
{ themes(first: 3, roles: [MAIN]) { nodes { id name role updatedAt } } }
```

## List a theme's templates

```graphql
query T($id: ID!) {
  theme(id: $id) {
    files(first: 50, filenames: ["templates/page.*.json"]) {
      nodes { filename size checksumMd5 } } } }
```

## Read file bodies

```graphql
query F($id: ID!, $filenames: [String!]) {
  theme(id: $id) {
    files(first: 10, filenames: $filenames) {
      nodes { filename contentType checksumMd5
        body {
          ... on OnlineStoreThemeFileBodyText { content }
          ... on OnlineStoreThemeFileBodyBase64 { contentBase64 }
          ... on OnlineStoreThemeFileBodyUrl { url } } } } } }
```

## Write files

```graphql
mutation W($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    job { id }
    userErrors { filename code field message } } }
```
```json
{ "themeId": "gid://shopify/OnlineStoreTheme/…",
  "files": [ { "filename": "templates/page.faq-page.json",
               "body": { "type": "TEXT", "value": "…full file…" } } ] }
```

## Duplicate a theme (backup)

```graphql
mutation D($id: ID!, $name: String) {
  themeDuplicate(id: $id, name: $name) {
    newTheme { id name role } userErrors { field message } } }
```

## Redirect after a handle change

```graphql
mutation R($redirect: UrlRedirectInput!) {
  urlRedirectCreate(urlRedirect: $redirect) {
    urlRedirect { id path target } userErrors { field message } } }
```
```json
{ "redirect": { "path": "/pages/old-handle", "target": "/pages/new-handle" } }
```
`redirectNewHandle: true` on `pageUpdate` usually creates this for you — check
before adding a duplicate.

## Escaping

Send GraphQL variables as real JSON values. Inside a JSON string: `"` → `\"`,
newline → `\n`, backslash → `\\`. Don't HTML-escape — `<h2>` stays `<h2>`. If
the live page shows `\n` or `&lt;h2&gt;` as text, the body was double-escaped:
re-read, fix, re-upsert.
