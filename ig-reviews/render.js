const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + __dirname + '/slides.html');
  await p.evaluate(() => document.fonts.ready);
  for (const id of ['s1', 's2', 's3', 's4', 's5', 's6', 'p1']) {
    await (await p.$('#' + id)).screenshot({ path: `${__dirname}/${id}.png` });
  }
  await b.close();
})();
