const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices['iPhone 15 Pro Max'], viewport: { width: 430, height: 932 }, screen: { width: 430, height: 932 } });
  const page = await ctx.newPage(); const errs = []; page.on('pageerror', e => errs.push(String(e) + ' @ ' + String(e.stack).split('\n').slice(1,4).join(' / ')));
  await page.goto('file://' + require('path').resolve(__dirname, '..', '..', 'www') + '/index.html'); await page.evaluate(() => localStorage.clear());
  await page.goto('file://' + require('path').resolve(__dirname, '..', '..', 'www') + '/index.html'); await page.waitForTimeout(2600);
  await page.click('#welcomeBox >> text=Jogar'); await page.fill('#newName', 'Ana'); await page.click('#addPlayerForm button.btn-green'); await page.waitForTimeout(1000);
  await page.click('#tapHint button');
  await page.evaluate(() => document.querySelectorAll('.htab')[2].click()); await page.waitForTimeout(500);
  console.log('dica com 0 criaturas:', JSON.stringify((await page.textContent('#collTip')).trim()));
  await page.screenshot({ path: process.argv[2] + '/colecao.png' });
  // depois de ganhar uma partida perfeita a dica some
  await page.evaluate(() => { document.querySelectorAll('.htab')[0].click(); startGame(2); GS.ok = 10; endGame(true); closeWin(); });
  await page.waitForTimeout(900); await page.evaluate(() => { closeModal('mParents'); document.querySelectorAll('.htab')[2].click(); }); await page.waitForTimeout(400);
  console.log('dica depois de resgatar:', JSON.stringify((await page.textContent('#collTip')).trim()), '| criaturas:', await page.evaluate(() => document.getElementById('storyProgress').textContent));
  console.log('erros:', JSON.stringify(errs));
  await b.close();
})();
