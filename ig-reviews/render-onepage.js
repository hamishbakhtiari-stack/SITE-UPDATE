const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + __dirname + '/onepage.html');
  await p.evaluate(() => document.fonts.ready);
  for (const id of ['post']) {
    await (await p.$('#' + id)).screenshot({ path: `${__dirname}/onepage.png` });
  }
  await b.close();
})();
