#!/usr/bin/env python3
"""CTA fix. The AJAX /cart/add script (custom_liquid_cartAddLink, copied from CB's delegate block, where it
never runs because CB's capture-phase delegate intercepts first) called cart.renderContents() but did not
remove `is-empty` from <cart-drawer> (Dawn product-form.js line 104 does). From an empty cart the drawer
opened showing 'Your cart is empty'. Replace it with CB's proven approach, narrowed: route every in-page
/cart/add link through the hero's own Add to Cart button. Links to other pages are untouched."""
import json, re
BASE = 'baseline/product.ergoRelief.after-s11.json'
OUT = 'candidate/product.ergoRelief.json'
VARIANT = '48771729031425'

JS = """<script>
/* sc-cta-delegate (ErgoRelief): every in-page add-to-cart link (/cart/add?...) goes through the
   hero's own Add to Cart button, so it opens the cart drawer exactly like that button does,
   including from an empty cart. Links to other pages (e.g. the ComfortBundle page) are untouched.
   If the hero button is missing or disabled, the link works on its own (adds, then goes to /cart).
   Never silent: if the drawer has not opened within 3s, go to /cart. */
(function () {
  var SEL = 'a[href^="/cart/add?"]';

  function drawerIsOpen() {
    var d = document.querySelector('cart-drawer');
    var n = document.querySelector('cart-notification');
    return (d && d.classList.contains('active')) ||
           (n && n.classList.contains('active')) ||
           document.body.classList.contains('overflow-hidden');
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest(SEL);
    if (!el) return;

    var submit = document.querySelector('product-form form [name="add"]');
    if (!submit || submit.disabled) return;

    e.preventDefault();
    e.stopImmediatePropagation();
    submit.click();

    var t0 = Date.now();
    var iv = setInterval(function () {
      if (drawerIsOpen()) { clearInterval(iv); return; }
      if (Date.now() - t0 > 3000) {
        clearInterval(iv);
        window.location.href = '/cart';
      }
    }, 150);
  }, true);
})();
</script>"""

er = json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', open(BASE, encoding='utf-8').read(), count=1, flags=re.S))
blk = er['sections']['main']['blocks']['custom_liquid_cartAddLink']
assert 'renderContents' in blk['settings']['custom_liquid']
blk['settings']['custom_liquid'] = JS

# Every add-to-cart link on this page must add ErgoRelief (the hero button adds that same variant).
links = re.findall(r'/cart/add\?id=(\d+)', json.dumps(er))
assert links and set(links) == {VARIANT}, links
dumped = json.dumps(er, ensure_ascii=False).lower()
for bad in ('free shipping', 'free express', 'express free', 'ships free', 'free delivery'):
    assert bad not in dumped, bad
json.dump(er, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', OUT, '| /cart/add links:', len(links))
