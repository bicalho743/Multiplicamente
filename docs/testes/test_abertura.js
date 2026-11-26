const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const f of ['_antes_tmp.html', 'index.html']) {
    const res = [];
    for (let i = 0; i < 4; i++) {
      const ctx = await b.newContext({ ...devices['iPhone 15 Pro Max'] });
      const page = await ctx.newPage(); const errs = []; page.on('pageerror', e => errs.push(String(e).slice(0, 90)));
      await page.goto('file://' + require('path').resolve(__dirname, '..', '..', 'www') + '/' + f); await page.waitForTimeout(4500);
      res.push(errs.length); await ctx.close();
    }
    console.log(f, 'erros em 4 aberturas:', JSON.stringify(res));
  }
  await b.close();
})();
