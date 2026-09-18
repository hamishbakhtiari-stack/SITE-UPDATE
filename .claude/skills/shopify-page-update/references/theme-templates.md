# Theme Templates — where page content actually lives

A page with `templateSuffix: "faq-page"` renders `templates/page.faq-page.json`
from the **published (MAIN)** theme. That JSON file holds the sections, their
settings, and nearly all the visible copy. This is the file you edit for most
page changes.

## Find the main theme

```graphql
{ themes(first: 3, roles: [MAIN]) { nodes { id name role updatedAt } } }
```

`roles: [MAIN]` returns exactly the live theme. Don't guess from a theme list —
this store has several similarly named unpublished copies.

## Read a template

```graphql
query ReadFiles($themeId: ID!, $filenames: [String!]) {
  theme(id: $themeId) {
    files(first: 5, filenames: $filenames) {
      nodes {
        filename contentType size checksumMd5
        body {
          ... on OnlineStoreThemeFileBodyText { content }
          ... on OnlineStoreThemeFileBodyBase64 { contentBase64 }
          ... on OnlineStoreThemeFileBodyUrl { url }
        }
      }
    }
  }
}
```

`filenames` accepts globs: `["templates/page.*.json"]`, `["sections/*.liquid"]`.
Omit `filenames` and you get the whole theme — don't. Record `checksumMd5`; a
changed checksum on re-read is your proof the write landed.

Large files come back as `OnlineStoreThemeFileBodyUrl` instead of inline text —
fetch the URL to get the content.

## File anatomy

```jsonc
/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 * ...
 * ------------------------------------------------------------
 */
{
  "sections": {
    "main":        { "type": "main-page", "disabled": true, "settings": { … } },
    "faq_4TjTJm":  {
      "type": "FAQ",
      "name": "Custom FAQ Section",
      "blocks": {
        "faq_JeXq9g": { "type": "faq", "settings": { "question": "…", "answer": "…" } }
      },
      "block_order": ["faq_JeXq9g", "…"],
      "settings": { "heading": "Frequently Asked Questions", "padding_top": 80, … }
    }
  },
  "order": ["main", "faq_4TjTJm"]
}
```

- **The `/* … */` banner is not valid JSON.** Strip it before parsing, keep it
  when writing back. `scripts/theme_json.py` does both.
- **Section keys** (`faq_4TjTJm`) are IDs referenced by `order`. Never rename or
  regenerate an existing one — the theme editor's per-section state and any
  section-specific CSS keys off them. New sections need a fresh unique key.
- **`type`** must match a file in `sections/` (`type: "FAQ"` →
  `sections/FAQ.liquid`). A typo renders nothing, silently.
- **`blocks` + `block_order`**: both must agree. A block present in `blocks` but
  absent from `block_order` doesn't render; an ID in `block_order` with no block
  breaks the section.
- **`disabled: true`** keeps a section in the file but off the page. That's how
  `main` is switched off on pages whose copy is fully section-driven — which is
  why editing the page `body` on those pages does nothing.
- **`name`** is the label in the theme editor only.
- **Setting values** use Shopify URL schemes: `shopify://pages/contact`,
  `shopify://collections/all`, `shopify://products/<handle>`,
  `shopify://shop_images/logo.webp`. Keep the scheme — don't swap in an absolute
  URL, and don't point at a handle that doesn't exist.
- Copy is plain text with `\n` for line breaks (the section's Liquid decides the
  markup). Curly quotes and `™` appear literally — preserve them.

## Common edits

| Goal | Edit |
|------|------|
| Change a headline | `sections.<id>.settings.heading` |
| Change FAQ copy | `sections.<id>.blocks.<blockId>.settings.question` / `.answer` |
| Add an FAQ | New block under `blocks` with a unique ID, then append that ID to `block_order` |
| Reorder sections | Reorder the `order` array only |
| Hide a section | Add `"disabled": true` — reversible, unlike deleting |
| Swap an image | Point the image setting at another `shopify://shop_images/<file>` |
| Change spacing/colour | The section's `padding_*` / `*_color` settings |

To learn a section's available settings, read its schema:
`sections/<type>.liquid` → the `{% schema %}` block at the bottom lists every
`id`, `type`, and `default`. Only write settings that exist there.

## Write a template

```graphql
mutation UpsertFiles($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    job { id }
    userErrors { filename code field message }
  }
}
```

```json
{ "themeId": "gid://shopify/OnlineStoreTheme/…",
  "files": [ { "filename": "templates/page.faq-page.json",
               "body": { "type": "TEXT", "value": "<entire file, banner included>" } } ] }
```

- The upsert **replaces the whole file**. Send the complete content, always
  built from a fresh read.
- `body.type`: `TEXT` for Liquid/JSON/CSS/JS, `BASE64` or `URL` for binary
  assets.
- Multiple files in one call are applied together — group a template change and
  the section it depends on.
- A returned `job.id` means the write is queued; the file may lag a second or
  two. Re-read to confirm rather than trusting the 200.

## Editing Liquid sections

Only when no setting can express the change. Same read → back up → minimal
edit → upsert loop.

- Changing a setting's `id` in `{% schema %}` orphans the merchant's saved value
  — the setting reverts to its default on every page using the section. Add new
  settings instead of renaming.
- Removing a setting from the schema deletes its stored values.
- Section files are shared: `sections/FAQ.liquid` renders every page that uses
  `type: "FAQ"`. Check who else uses it before you change markup:
  read `templates/*.json` and grep for the type.
- Liquid has no build step, and a syntax error takes down every page using the
  section. Re-read the file and load the live page after writing.

## Round-tripping

`scripts/theme_json.py` re-serialises with `indent=2`, `ensure_ascii=False` and a
trailing newline — the same formatting Shopify writes. A no-op edit round-trips
byte-identically, so `diff` between your before/after files shows only your
change, and the upsert doesn't churn the file. Editing the JSON by hand in an
editor that reformats or ASCII-escapes will rewrite every line and bury the real
change (and mangle `™` and curly quotes).
