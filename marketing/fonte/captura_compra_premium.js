const { chromium, devices } = require('playwright');
(async () => {
  const out = process.argv[2];
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ ...devices['iPhone 15 Pro Max'], viewport: { width: 430, height: 932 }, screen: { width: 430, height: 932 } });
  const page = await ctx.newPage();
  await page.goto('file://' + require('path').resolve(__dirname, '..', '..', 'www') + '/index.html', { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  await page.fill('#newName', 'Ana');
  await page.click('text=Jogar');
  await page.waitForTimeout(1200);
  await page.evaluate(() => { localStorage.removeItem('mm_play_premium'); localStorage.removeItem('mm_cupom_premium'); showPremium(); });
  await page.waitForTimeout(900);
  await page.screenshot({ path: out });
  await browser.close();
})();
