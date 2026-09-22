#!/bin/bash
# shoot2.sh page.html out.png W H  -- generic: reports #sec height + child tops
P=$(realpath "$1"); OUT=$2; W=${3:-402}; H=${4:-1400}; D=$(dirname "$P"); F="$D/frame2-$(basename "$P")"
cat > "$F" <<H
<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}iframe{width:${W}px;height:${H}px;border:0;display:block}</style></head><body>
<iframe id="fr" src="$(basename "$P")" scrolling="no"></iframe><script>window.addEventListener('load',function(){setTimeout(function(){
var d=document.getElementById('fr').contentDocument,w=d.defaultView,o=[];var s=d.getElementById('sec');
o.push('SECTION h='+Math.round(s.getBoundingClientRect().height));
s.querySelectorAll('.one-product-image,.heading-h2,.one-product-subheading,.one-product-badge,.one-product-block,.btn-globel,.product-image-text__image,.product-image-text__item').forEach(function(e){var r=e.getBoundingClientRect(),cs=w.getComputedStyle(e);o.push(e.className.slice(0,32)+' top='+Math.round(r.top)+' h='+Math.round(r.height)+' fs='+cs.fontSize+' lh='+cs.lineHeight+' fw='+cs.fontWeight)});
var p=document.createElement('pre');p.id='probe';p.textContent=o.join('\n');document.body.appendChild(p)},800)});</script></body></html>
H
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$CH --headless --no-sandbox --disable-gpu --allow-file-access-from-files --window-size=560,$((H+300)) --virtual-time-budget=3000 --dump-dom "$F" 2>/dev/null | python3 -c "import sys,re,html;s=sys.stdin.read();m=re.search(r'<pre id=\"probe\">(.*?)</pre>',s,re.S);print(html.unescape(m.group(1)) if m else 'NO PROBE')"
$CH --headless --no-sandbox --disable-gpu --hide-scrollbars --allow-file-access-from-files --force-device-scale-factor=2 --window-size=560,$H --virtual-time-budget=3000 --screenshot="$OUT.raw.png" "$F" 2>/dev/null
python3 -c "from PIL import Image; Image.open('$OUT.raw.png').crop((0,0,$((W*2)),$((H*2)))).save('$OUT')"; rm -f "$OUT.raw.png"
