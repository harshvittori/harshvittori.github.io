// Renders each card in src/og-cards.html to its PNG (1200x630). Needs Playwright: npm i playwright
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const exe = process.env.CHROME_PATH; const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'og-cards.html')); await p.evaluate(() => document.fonts.ready);
  for (const card of await p.$$('.card')) {
    const out = await card.getAttribute('data-out');
    await card.screenshot({ path: path.join(__dirname, '..', out) }); console.log('wrote', out);
  }
  await b.close();
})();
