const { chromium, devices } = require('playwright');
const URL = 'file://' + require('path').resolve(__dirname, '..', '..', 'www') + '/index.html';
const res = []; const ok = (n, c, extra='') => { res.push([c?'ok  ':'FALHA', n, extra]); };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices['iPhone 15 Pro Max'], viewport: { width: 430, height: 932 }, screen: { width: 430, height: 932 } });
  const page = await ctx.newPage(); const errs = []; page.on('pageerror', e => errs.push(String(e)));
  const vis = (sel) => page.evaluate((s) => { const e = document.querySelector(s); if(!e) return false; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return cs.display!=='none' && r.width>0 && r.height>0; }, sel);
  await page.goto(URL); await page.evaluate(() => localStorage.clear()); await page.goto(URL); await page.waitForTimeout(2600);

  // 1. boas-vindas
  ok('1a boas-vindas visível', await vis('#welcomeBox'));
  ok('1b formulário escondido', !(await vis('#addPlayerForm')));
  ok('1c link "Já tenho conta"', (await page.textContent('#welcomeBox')).includes('Já tenho conta (adultos)'));
  await page.click('text=Já tenho conta (adultos)'); await page.waitForTimeout(500);
  ok('2a pergunta para adultos abre', await vis('#mGate .modal-sheet'));
  await page.fill('#gateInput', '1985'); await page.click('#mGate >> text=Continuar'); await page.waitForTimeout(600);
  ok('2b folha "Entrar na sua conta"', (await page.textContent('#cloudTitle')) === 'Entrar na sua conta' && await vis('#mCloud .modal-sheet'));
  await page.evaluate(() => closeModal('mCloud'));

  // 3. Jogar -> apelido e personagem; Pular cria "Jogador"
  await page.click('#welcomeBox >> text=Jogar'); await page.waitForTimeout(400);
  ok('3a formulário aparece, boas-vindas some', await vis('#addPlayerForm') && !(await vis('#welcomeBox')));
  ok('3b placeholder de apelido', (await page.getAttribute('#newName','placeholder')) === 'Como você quer ser chamado?');
  await page.click('#addPlayerForm >> text=Pular'); await page.waitForTimeout(1000);
  const p1 = await page.evaluate(() => ({ nome: P.name, av: P.av, home: document.getElementById('sHome').classList.contains('active') }));
  ok('3c Pular cria "Jogador" e entra na Home', p1.nome === 'Jogador' && p1.home, JSON.stringify(p1));

  // 4. dica do primeiro toque
  await page.waitForTimeout(900);
  ok('4a dica aparece', await vis('#tapHint'));
  await page.screenshot({ path: '' + (process.env.OUT || '.') + '/dica.png' });
  await page.click('#tapHint button'); await page.waitForTimeout(200);
  ok('4b "Entendi" fecha e grava', !(await vis('#tapHint')) && (await page.evaluate(() => localStorage.getItem('mm_hint_tap'))) === '1');

  // 5. primeira partida direto em "Sem tempo"
  await page.evaluate(() => openSpeed(2)); await page.waitForTimeout(500);
  const g1 = await page.evaluate(() => ({ jogo: document.getElementById('sGame').classList.contains('active'), folha: document.getElementById('mSpeed').classList.contains('open'), diff }));
  ok('5a primeira partida começa sem a folha de velocidade', g1.jogo && !g1.folha && g1.diff === 0, JSON.stringify(g1));

  // 6. depois da primeira vitória: cartão para os pais (uma vez)
  await page.evaluate(() => { GS.ok = 10; endGame(true); }); await page.waitForTimeout(400);
  const w = await page.evaluate(() => ({ after: afterWin, nome: document.getElementById('parentsName').textContent }));
  ok('6a cartão agendado para depois da vitória', w.after === 'mParents' && w.nome === 'Jogador', JSON.stringify(w));
  await page.evaluate(() => closeWin()); await page.waitForTimeout(900);
  ok('6b cartão "Para os pais" abre', await vis('#mParents .modal-sheet'));
  ok('6c grava para não repetir', (await page.evaluate(() => localStorage.getItem('mm_parent_card'))) === '1');
  await page.screenshot({ path: '' + (process.env.OUT || '.') + '/pais.png' });
  await page.click('#mParents >> text=Depois'); await page.waitForTimeout(200);

  // 7. depois da 1ª partida a folha de velocidade volta
  await page.evaluate(() => openSpeed(2)); await page.waitForTimeout(400);
  ok('7 segunda partida mostra a folha de velocidade', await vis('#mSpeed .modal-sheet'));
  await page.evaluate(() => closeModal('mSpeed'));

  // 8. Coleção ensina
  await page.evaluate(() => document.querySelectorAll('.htab')[2].click()); await page.waitForTimeout(400);
  await page.evaluate(() => { P.subjects = {}; renderCollection(); }); // a vitória simulada acima já resgatou uma criatura
  ok('8a dica na Coleção vazia', (await page.textContent('#collTip')).includes('Vença a tabuada do 2'));
  await page.evaluate(() => { P.subjects = { mult: { creaturesMap: { 0: [2] } } }; renderCollection(); });
  ok('8b some quando já há criatura', (await page.textContent('#collTip')).trim() === '');

  // 9. editar apelido e personagem
  await page.evaluate(() => document.querySelectorAll('.htab')[0].click());
  await page.click('.home-user'); await page.waitForTimeout(500);
  await page.click('#mProfile >> text=Editar apelido e personagem'); await page.waitForTimeout(400);
  ok('9a folha de edição abre com o apelido atual', (await page.inputValue('#editName')) === 'Jogador');
  await page.fill('#editName', 'Ana');
  await page.click('#editAvGrid .av-btn:nth-child(4)');
  await page.click('#mEditProfile >> text=Salvar'); await page.waitForTimeout(400);
  const e = await page.evaluate(() => ({ nome: P.name, av: P.av, home: document.getElementById('homeName').textContent, salvo: gd().profiles[Pi].name, modal: document.getElementById('profileModalName').textContent, avModal: document.getElementById('profileModalAv').textContent }));
  ok('9b salvou e atualizou Home e Perfil', e.nome === 'Ana' && e.av === '🐼' && e.home === 'Ana' && e.salvo === 'Ana' && e.modal === 'Ana' && e.avModal === '🐼', JSON.stringify(e));
  await page.screenshot({ path: '' + (process.env.OUT || '.') + '/perfil.png' });

  // 10. segundo "Jogador" vira "Jogador 2" (e o apelido vazio no formulário)
  await page.evaluate(() => { closeModal('mProfile'); switchPlayer(); }); await page.waitForTimeout(400);
  await page.click('#addPlayerToggle'); await page.click('#addPlayerForm >> text=Pular'); await page.waitForTimeout(700);
  await page.evaluate(() => { closeModal('mParents'); });
  await page.evaluate(() => { document.getElementById('tapHint')&&document.getElementById('tapHint').remove(); switchPlayer(); }); await page.waitForTimeout(300);
  await page.click('#addPlayerToggle'); await page.click('#addPlayerForm >> text=Pular'); await page.waitForTimeout(500);
  const nomes = await page.evaluate(() => gd().profiles.map(p => p.name));
  ok('10 nomes padrão sem repetir', JSON.stringify(nomes) === JSON.stringify(['Ana', 'Jogador', 'Jogador 2']), JSON.stringify(nomes));

  // 11. com jogadores, volta a lista (sem boas-vindas)
  await page.evaluate(() => switchPlayer()); await page.waitForTimeout(300);
  ok('11 com jogadores não mostra boas-vindas', !(await vis('#welcomeBox')) && await vis('#profilesArea .profile-big'));
  ok('12 sem erros de JavaScript', errs.length === 0, JSON.stringify(errs));
  res.forEach(r => console.log(r.join(' | ')));
  await b.close();
})();
