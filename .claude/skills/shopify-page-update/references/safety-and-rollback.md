# Safety, Preview, Verification, Rollback

The published theme serves real customers. Every write here is live within
seconds and there is no version history you can roll back from the API — your
backup is the only undo.

## Before the first write

Pick one, in order of preference:

**1. Save the current file body.** Fast, sufficient for a copy edit.

```bash
# after reading the file, write the exact body to the scratchpad
$SCRATCH/page.faq-page.before.json
```

Re-upserting that file restores the previous state byte for byte. Keep it until
the change is verified on the live page.

**2. Duplicate the theme.** For multi-file or structural changes.

```graphql
mutation Backup($id: ID!, $name: String) {
  themeDuplicate(id: $id, name: $name) {
    newTheme { id name role }
    userErrors { field message }
  }
}
```

Name it plainly: `"Backup before FAQ rewrite 2026-09-18"`. The duplicate is
unpublished and costs nothing but a theme slot (a store holds ~20).

**3. Build on an unpublished copy and publish after review.** For a redesign or
anything the user wants to see before customers do. Duplicate, edit the copy,
send a preview link, publish only on their explicit go-ahead.

## Preview links

- Live page: `https://www.sitcomfort.com.au/pages/<handle>`
- Unpublished theme: `https://www.sitcomfort.com.au/pages/<handle>?preview_theme_id=<numeric-id>`
  — the numeric part of the GID only, e.g. `163967992065`.

## Verification, every time

1. **Re-read** the file or page. `checksumMd5` / `updatedAt` must have changed.
2. **Re-parse** a JSON template you wrote: `python3 scripts/theme_json.py validate <file>`.
   Catches a truncated or double-escaped body before a customer does.
3. **Load the page.** WebFetch the live URL and confirm the new copy is present
   and the old copy is gone. A 200 with stale content means you edited an
   unpublished theme, or a different template than the page uses.
4. **Check `userErrors`** on every mutation — Shopify returns HTTP 200 with a
   populated `userErrors` array for validation failures.

## Rollback

```graphql
mutation Rollback($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename } userErrors { filename message }
  }
}
```

Send the saved `.before.json` body verbatim, banner included. For a page record,
re-send the previous field values with `pageUpdate`. If you duplicated the theme
instead, `themePublish` the backup — but flag to the user that this also reverts
anything else changed in the theme editor since the duplicate was made.

## Ask first

Confirm with the user before:

- publishing or unpublishing a page, or deleting one
- changing a handle (the URL, and anything linking to it, moves)
- publishing a theme
- deleting a section, or any change that removes content rather than editing it
- editing a shared `sections/*.liquid` that other pages render

Don't ask for ordinary copy fixes, typo corrections, or setting tweaks the user
already described — do those and report what changed.

## Concurrency

The merchant may be in the theme editor right now. Read immediately before you
write, keep the gap short, and if `checksumMd5` differs from the value you read
a few minutes ago, re-read and re-apply your edit on top rather than overwriting
their work.
