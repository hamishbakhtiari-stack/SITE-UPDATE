# Lessons — every mistake from the PDP project, and the rule it produced

Each of these actually happened. They are written down because the failure mode is rarely
obvious in advance, and because most of them produced *confident wrong output* rather than an
error message — which is the dangerous kind.

---

## Measurement failures

### 1. Measured at the wrong viewport width and gave the owner wrong numbers

Headless Chromium clamps `--window-size` width to about 500px. A probe asking for 390px actually
ran at ~500px, so line counts and element heights were all wrong. An estimate of "45–65px saved"
went out; the real figure at true 390px was 41px.

**Rule:** measure inside an iframe at the real width. Never quote a number from a bare
`--window-size` render below 500px.

### 2. Estimated instead of measuring, then had to correct it

The "45–65px" above was arithmetic from CSS rules, not a measurement. Two of its three components
were wrong: the price fix saved 8px not 10, and the text change saved 8px not 12–24.

**Rule:** build the harness first, quote numbers second. If you must estimate before measuring,
label it as an estimate.

### 3. Called something a bug without checking which element it applied to

`.price-item--regular` had `line-height: 40px` with a 26px font — apparently dead space. But the
product has a compare-at price, so `.price-item--regular` is the *struck-through* price and the
large visible one is `.price-item--sale`. The finding survived, but the reasoning was wrong and
the saving was smaller than claimed.

**Rule:** before reasoning about an element's styling, confirm which element actually renders.
For price, check `compareAtPrice`.

### 4. Extracted the wrong `<style>` block

`liq.index("<style>")` matched a tiny inline style inside an SVG in the play-icon markup, so none
of the real CSS loaded and the verification render showed cards overlapping the reviews. Looked
like a section bug; was a harness bug.

**Rule:** select a style block by a distinctive selector it contains, not by position. When a
render looks catastrophically wrong, suspect the harness before the code.

### 5. Omitted `box-sizing: border-box` and reported a false overflow

Dawn's global reset was missing from a verify page, producing a "button overflows on mobile"
finding that did not exist.

**Rule:** include the reset in every harness page.

### 6. Called a bare binary that isn't on PATH

`chromium` produced no screenshot and no useful error. The binary is at
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.

**Rule:** full path, always. A missing screenshot is a tooling failure, not a rendering result.

---

## Write failures

### 7. Double-escaped inside a GraphQL block string

Transcribed `'a[href*=\"/cart/add\"]'` as `'a[href*=\\"/cart/add\\"]'`. Backslashes are already
literal in `"""` block strings. Four selectors, eight occurrences, +16 bytes of unintended change
to the owner's JavaScript. Not functionally broken, but shipped without being noticed until the
checksum was compared.

**Rule:** inside `"""`, copy bytes verbatim. Verify every push with `checksumMd5` against a local
`md5sum`. That check is the only thing that catches this class of error.

### 8. Nearly shipped a `white-space: pre-line` formatting bug

With `pre-line`, a Liquid output tag on its own indented line renders the surrounding newline and
indentation, adding a blank line to the top and bottom of every FAQ answer. Caught in the render
with minutes to spare.

**Rule:** render before pushing, even for a change that is "obviously" just CSS.

### 9. Treated a formatting difference as a failure

A pushed `.liquid` read back one byte shorter with zero line differences — GraphQL block strings
trim the trailing newline. Also, Shopify prepends an auto-generated banner comment to template
JSON on read, making the file ~363 bytes larger than what you sent.

**Rule:** know both behaviours so you can distinguish them from real corruption instead of
chasing them.

---

## Judgement failures

### 10. Re-opened a closed topic — three times

Pricing/anchoring was raised repeatedly after being rejected, until the owner wrote *"I beg you, I
ask you a million times to just drop the price argument."*

**Rule:** when a topic is closed, it is closed. Record the decision **and his reasoning** in the
decisions log so it never gets re-derived. Check that log before proposing.

### 11. Raised a section out of order

Prompted *"Have we got to this section? Why you should bring this up now? Dont understand."*

**Rule:** work the page in order; park out-of-scope findings in the log.

### 12. Designed icons after being told not to

Twice. *"You are terrible at creating icons"*, then *"I said I will use my current icons no chanfe."*

**Rule:** never generate or substitute an icon.

### 13. Sent an unlabelled mock and caused a scare

A measuring harness used plain grey circles where the owner's tick SVG goes, and fell back to a
serif font. He saw it and thought his icons and fonts had been changed on the live theme. They
had not — but he had no way to know that from the image.

**Rule:** caption every harness render as a harness render. Name the placeholders.

### 14. Squeezed spacing uniformly and made the page feel packed

Flat 10px gaps between every block "saved" 20px and cost legibility. The owner pushed back. The
standards-based answer — keep Dawn's 15px, keep 16px/1.5 body type, and remove an unnecessary
block instead — saved **149px** rather than 83px *and* looked better.

**Rule:** reach for the block that does not earn its place before you touch the rhythm. Check
proposed spacing against a real standard (8pt grid, WCAG 1.4.12, 16px mobile minimum) rather than
eyeballing "tighter".

### 15. Apologised for something that hadn't happened

Challenged with *"You told me 7 am, it is 7:20 now"* when no such commitment existed. Rather than
reflexively apologising, checking the scheduled-task list and the notification queue showed no
7am task — the scheduled jobs fire at 7pm AEST. The owner confirmed: *"Not scheduled."*

**Rule:** check the record before accepting or denying a claim about what you did. Reflexive
apology for a thing you did not do is its own kind of dishonesty.

---

## What worked and is worth repeating

- **Data settles arguments.** 72 orders answered the quantity-selector question in one query.
  The Files API turned "the crop looks off" into "24% of every frame". Real reviews were already
  in a metafield. Go and look before you reason.
- **Scoped `v2` classes** in a section's own `<style>` beat the global CSS on specificity and
  source order, with no `!important` and no edits to shared files.
- **Opt-in settings for shared sections.** A `center_layout` checkbox defaulting to `false` let
  the PDP change while About Us stayed byte-identical in behaviour.
- **Disable, don't delete.** Keeps everything recoverable from the theme editor.
- **Key-by-key parsed diffs.** "424 keys, exactly these 6 changed" is a sentence you can stand
  behind. Text diffs of a 39KB JSON file are not.
- **One anchor metric per layout question.** The y-offset of Add to Cart turned a vague
  "arrives sooner" into 581px → 432px with a four-line breakdown of where each pixel came from.
- **A decisions log with his own words in it.** It is what keeps settled things settled.
