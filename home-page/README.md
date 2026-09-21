# Home page working set

    baseline/templates.index.json              byte-verified copy of live templates/index.json
    baseline/templates.index.withbanner.json   same, with Shopify's auto-generated read banner
    candidate/                                 built candidates, pre-push
    harness/                                   local render harness
    renders/                                   screenshots
    locked.json                                pre-push guard config
    DECISIONS.md                               running log

## Before every push

    python3 ../scripts/diff_template.py baseline/templates.index.json candidate/templates.index.json
    python3 ../scripts/check_template.py candidate/templates.index.json locked.json   # non-zero = stop
    # push via themeFilesUpsert to theme 164208705793
    # re-query checksumMd5 and compare to: md5sum candidate/templates.index.json

Never write to the live theme. Publishing is Hamish's call.
