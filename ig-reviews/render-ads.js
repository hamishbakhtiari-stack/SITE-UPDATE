const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const [name, h] of [['ad-feed', 1350], ['ad-story', 1920]]) {
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + __dirname + '/' + name + '.html');
    await p.evaluate(() => document.fonts.ready);
    await (await p.$('#ad')).screenshot({ path: `${__dirname}/${name}.png` });
  }
  await b.close();
})();
