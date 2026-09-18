# The safe write protocol

Theme files are live code for a business. There is no staging, no code review and no undo beyond
what you kept yourself. This protocol exists so that every push is provably exactly what you
intended — not "looks right", *provably*.

---

## Before any write

**Confirm you are on the unpublished duplicate.** Writes to the live/MAIN theme are blocked by
the connector, but treat that as a backstop, not a plan. Note the theme ID and reuse it.

**Snapshot the current live state to disk.** Pull the file and save it. You need this to diff
against, and you need it if something goes wrong.

---

## The loop

```
1. pull live  →  save as baseline
2. build candidate locally (edit the parsed JSON in Python, not by hand)
3. diff candidate vs live, key-by-key, on the PARSED structure
4. run the guard script            → non-zero exit means stop
5. push via themeFilesUpsert
6. re-query checksumMd5            → compare to local md5sum
7. update baseline + decisions log
```

### Step 2 — build by editing parsed JSON

Load the JSON, mutate the specific keys, dump with `ensure_ascii=False, indent=2`. Never
hand-edit template JSON as text. Hand-editing is how you lose a `™`, flip a U+2011 to a hyphen,
or break quoting inside a `custom_liquid` blob.

### Step 3 — diff the parsed structure

Flatten both documents to leaf paths and compare. The output you want reads like:

```
keys 424 -> 424
DIFF /sections/main/blocks/text_z3HGpc/settings/text
  - 'Cushion, lumbar support, and a 7-Day Reset plan to retrain it.'
  + 'Cushion, lumbar support, and a 7-Day Reset plan to retrain how you sit.'
total diffs 6 | order equal: True | block_order equal: True
```

If you cannot state the exact number of changed keys, you do not know what you are shipping.
`scripts/diff_template.py` does this.

Also assert `order` and every `block_order` are unchanged unless reordering is the point — a lost
`block_order` silently reshuffles the page.

### Step 6 — checksum verification is not optional

```graphql
query {
  theme(id: "gid://shopify/OnlineStoreTheme/<ID>") {
    files(filenames: ["templates/product.X.json"], first: 1) {
      nodes { size checksumMd5 }
    }
  }
}
```

Compare to `md5sum` of the local candidate. They should match exactly.

This is what caught the transcription bug described below. Nothing else would have — the file
parsed fine, the page rendered fine, and the corrupted region was 16 bytes inside a 39KB blob.

---

## Shopify GraphQL mechanics

### themeFilesUpsert with a block string

```graphql
mutation {
  themeFilesUpsert(
    themeId: "gid://shopify/OnlineStoreTheme/<ID>"
    files: [{ filename: "templates/product.X.json", body: { type: TEXT, value: """<file bytes>""" } }]
  ) { upsertedThemeFiles { filename } userErrors { filename code message } }
}
```

### THE ESCAPING TRAP — this is the one that bit

**Inside `"""..."""`, backslashes are literal.** Copy the file's bytes exactly as `cat` prints
them. Do not "helpfully" escape anything.

What went wrong: the file contained a JS selector written in JSON as

```
'a[href*=\"/cart/add\"]'
```

It was transcribed into the block string as `'a[href*=\\"/cart/add\\"]'` — an extra backslash on
each quote. Four selectors, eight occurrences, +16 bytes. It was not functionally broken (in JS,
`\"` inside a single-quoted string is just `"`), but it was an unintended modification of the
owner's code, and only the checksum revealed it.

Other block-string properties worth knowing:
- Block strings **normalise line endings**. For a CRLF file (some section `.liquid` files are
  CRLF), send the value as a **regular escaped GraphQL string** instead, or the file silently
  converts to LF.
- Block strings **trim the trailing newline**, so a pushed file can read back one byte shorter
  with zero line differences. Harmless, but know it before you chase it.
- Verify the content contains no `"""` sequence before choosing a block string.

### The auto-generated banner

Shopify prepends a `/* IMPORTANT: The contents of this file are auto-generated... */` comment
block to template JSON **on read**. Push *without* it; it comes back on the next read. It is ~363
bytes, which explains an otherwise confusing size difference between what you sent and what you
see. Strip it before parsing:

```python
s = re.sub(r'^\s*/\*.*?\*/\s*', '', s, count=1, flags=re.S)
```

### Getting large files without burning context

A `cat` of a 39KB file may be persisted to a tool-results file rather than printed. Read it back
in chunks with `head -c` / `tail -c +N | head -c` when you need to transcribe it, or better, avoid
transcription entirely by keeping the authoritative copy on disk and only diffing.

---

## Template JSON conventions

- **Disable, don't delete.** `"disabled": true` on a section or block keeps it visible and
  toggleable in the theme editor. Removing it from `order` loses the settings. Every removal on
  this project used `disabled`.
- **Block IDs are load-bearing.** Some CSS is keyed to generated IDs
  (`div#shopify-block-ATkRMa2FoTExLYjJUV__judge_me_reviews_preview_badge_Pg8JrN`). Renaming or
  recreating a block breaks those rules silently.
- **Stale template IDs lurk in CSS.** Rules like
  `img.chairId3_template--22109812392193__…` reference templates that no longer exist. When a
  rule "isn't applying", check whether it is keyed to a dead template ID.

---

## Writing to `config/settings_data.json`

This file is **global** — it drives every page, not just the one you are working on. It also
contains app-embed blocks.

**Known risk:** Shopify will not serialise app-embed blocks for apps that have been *uninstalled*,
so rewriting this file silently prunes them. On this store, PageFly was pruned that way on an
earlier write. Blocks for *installed* apps persist fine.

If you must write it: snapshot first, then after the write verify **each app-embed block
individually** is byte-identical. On this store that means judge-me `judgeme_core`, klaviyo
`klaviyo-onsite-embed`, clarity `brandAgents_js`, judge-me `cart_drawer_widget`, clarity
`clarity_js`.

For a single-string change, recommend the owner edits it in Theme settings instead. Rewriting a
46KB global file for one word is a bad trade.

---

## Keep a decisions log

Maintain a running `DECISIONS.md` alongside the work: what changed, why, what was measured, what
was verified, what is still open, and which topics are closed. It is what makes the next session
possible and stops settled arguments from being reopened. Record the owner's reasoning in his own
words where he gave it.
