// Gera as telas de onboarding PROPOSTAS (docs/onboarding/*.png) a partir do app real (www/index.html).
// Só desenha: não altera o app. Uso (na raiz do repositório):  node docs/onboarding/gerar.js
// Requer: playwright (Node). As imagens saem em 1290x2796 (iPhone 15 Pro Max).
const { chromium, devices } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const OUT = __dirname;
const URL = 'file://' + path.join(ROOT, 'www', 'index.html');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ ...devices['iPhone 15 Pro Max'], viewport: { width: 430, height: 932 }, screen: { width: 430, height: 932 } });
  const page = await ctx.newPage();

  async function abrir(comPerfil) {
    await page.goto(URL, { waitUntil: 'load' });
    await page.evaluate(() => localStorage.clear());
    await page.goto(URL, { waitUntil: 'load' });
    await page.waitForTimeout(2600); // abertura do app
    if (comPerfil) {
      await page.fill('#newName', 'Ana'); await page.click('text=Jogar'); await page.waitForTimeout(900);
    }
  }
  const foto = (nome) => page.screenshot({ path: path.join(OUT, nome) });
  const corpoLogin = (html) => page.evaluate((h) => {
    const b = document.querySelector('#sLogin .login-body');
    b.style.cssText = 'display:flex;flex-direction:column;justify-content:space-between;flex:1;gap:.8rem;padding-bottom:1.2rem';
    b.innerHTML = h;
  }, html);

  const avatares = `<div class="av-grid" style="justify-content:center">${'🦊🐯🐻🐼🦁🐸🐧🦄🤖⚡🌟🎮'.match(/./gu).map((a, i) => `<button class="av-btn${i === 0 ? ' sel' : ''}">${a}</button>`).join('')}</div>`;

  // 1. Boas-vindas
  await abrir(false);
  await corpoLogin(`
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:1rem;padding:0 .4rem">
      <div style="font-size:6rem;line-height:1">🦉</div>
      <div style="font-weight:900;font-size:1.8rem;color:var(--dark);line-height:1.15">Resolva a tabuada e<br>resgate criaturas!</div>
      <div style="font-size:2.3rem;letter-spacing:.35rem">🦊🐼🦄🐸</div>
      <div style="font-weight:700;color:var(--gray-dk);font-size:1rem;line-height:1.4">Uma jornada de fases, do 2 ao 10.<br>Sem anúncios.</div>
    </div>
    <div>
      <button class="btn btn-green" style="font-size:1.3rem;padding:1.1rem">🎮 Jogar</button>
      <button class="link-btn" style="margin-top:.8rem;width:100%;font-size:.95rem">Já tenho conta (adultos)</button>
    </div>`);
  await foto('01_boas-vindas.png');

  // 2. Apelido e personagem (pulável)
  await corpoLogin(`
    <div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.4rem">
        <div class="sec-lbl" style="margin:0;white-space:nowrap">Quem vai jogar?</div>
        <button class="link-btn" style="font-size:.95rem">Pular</button>
      </div>
      <input class="inp" placeholder="Como você quer ser chamado?" style="font-size:1.1rem;padding:.9rem 1rem" maxlength="20">
      <div style="font-size:.78rem;font-weight:700;color:var(--gray-dk);margin:-.1rem 0 .9rem">Pode ser um apelido. Não precisa ser o nome completo.</div>
      <div class="sec-lbl">Escolha seu personagem</div>
      ${avatares}
    </div>
    <button class="btn btn-green" style="font-size:1.3rem;padding:1.1rem">🎮 Jogar</button>`);
  await foto('02_apelido-personagem.png');

  // 3. Já tenho conta: pergunta para adultos e depois a folha de entrada
  await abrir(false);
  await corpoLogin(`
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:1rem;padding:0 .4rem">
      <div style="font-size:6rem;line-height:1">🦉</div>
      <div style="font-weight:900;font-size:1.8rem;color:var(--dark);line-height:1.15">Resolva a tabuada e<br>resgate criaturas!</div>
    </div>
    <div><button class="btn btn-green" style="font-size:1.3rem;padding:1.1rem">🎮 Jogar</button>
    <button class="link-btn" style="margin-top:.8rem;width:100%;font-size:.95rem">Já tenho conta (adultos)</button></div>`);
  await page.evaluate(() => parentGate(() => {})); await page.waitForTimeout(500);
  await foto('03_ja-tenho-conta_adultos.png');
  await page.evaluate(() => { closeModal('mGate'); document.body.classList.add('ios'); });
  await page.evaluate(() => {
    document.querySelector('#mCloud .sheet-title').textContent = 'Entrar na sua conta';
    const sub = document.querySelector('#mCloud .sheet-title').nextElementSibling; if (sub) sub.textContent = 'Para adultos. Seus jogadores voltam para este aparelho.';
    openCloudSection();
  });
  await page.waitForTimeout(500);
  await foto('04_ja-tenho-conta_entrar.png');

  // 5. Home com a dica do primeiro toque
  await abrir(true);
  await page.evaluate(() => {
    const no = [...document.querySelectorAll('.jnode')].find(n => n.textContent.trim().startsWith('2')) || document.querySelector('.jnode');
    const r = no.getBoundingClientRect();
    const ov = document.createElement('div');
    ov.style.cssText = 'position:fixed;inset:0;z-index:250;background:transparent';
    ov.innerHTML = `<div style="position:absolute;left:${r.left - 10}px;top:${r.top - 10}px;width:${r.width + 20}px;height:${r.height + 20}px;border-radius:50%;box-shadow:0 0 0 2000px rgba(0,0,0,.6);border:4px solid #fff"></div>
      <div style="position:absolute;left:24px;right:24px;top:${r.bottom + 28}px;background:#fff;border-radius:22px;padding:1.1rem 1.2rem;text-align:center;box-shadow:0 8px 0 rgba(0,0,0,.15)">
        <div style="font-size:2rem">👆</div>
        <div style="font-weight:900;font-size:1.25rem;color:var(--dark);margin:.2rem 0 .8rem">Toque no 2 para começar!</div>
        <button class="btn btn-green" style="padding:.8rem">Entendi</button></div>`;
    document.body.appendChild(ov);
  });
  await foto('05_home-dica-primeiro-toque.png');

  // 6. Primeira partida: vai direto em "Sem tempo", sem a folha de velocidade
  await abrir(true);
  await page.evaluate(() => { setDiff(0); startGame(2); });
  await page.waitForTimeout(900);
  await foto('06_primeira-partida-direta.png');

  // 7. Cartão para os pais, uma vez, depois da primeira vitória
  await abrir(true);
  await page.evaluate(() => {
    const m = document.createElement('div'); m.className = 'modal-ov open'; m.style.zIndex = 260;
    m.innerHTML = `<div class="modal-sheet"><span class="break-emoji">📊</span>
      <div class="sheet-title">Para os pais</div>
      <div class="sheet-sub">Veja como a Ana está indo: acertos, dias seguidos e progresso de cada tabuada. Fica no <b>Perfil</b>, protegido por PIN.</div>
      <button class="btn btn-green">📊 Ver o relatório</button>
      <button class="btn btn-outline" style="margin-top:.5rem">Depois</button></div>`;
    document.body.appendChild(m);
  });
  await page.waitForTimeout(300);
  await foto('07_cartao-para-os-pais.png');

  // 8. Coleção que ensina (tela vazia com explicação)
  await abrir(true);
  await page.evaluate(() => {
    document.querySelectorAll('.htab')[2].click();
    const t = document.querySelector('#tabCollection');
    const d = document.createElement('div');
    d.style.cssText = 'margin:.7rem .9rem 0;background:var(--green-bg);border:2.5px solid var(--green);border-radius:16px;padding:.8rem 1rem;font-weight:800;color:var(--green-sh);display:flex;gap:.7rem;align-items:center';
    d.innerHTML = '<span style="font-size:2rem">🐢</span><span>Vença a tabuada do 2 para resgatar sua primeira criatura!</span>';
    t.insertBefore(d, t.firstChild);
  });
  await page.waitForTimeout(400);
  await foto('08_colecao-ensina.png');

  // 9. Perfil com "Editar apelido e personagem"
  await abrir(true);
  await page.click('.home-user'); await page.waitForTimeout(600);
  await page.evaluate(() => {
    const av = document.getElementById('profileModalAv'); av.style.position = 'relative';
    av.insertAdjacentHTML('beforeend', '<span style="position:absolute;right:-8px;bottom:-8px;background:#fff;border:2.5px solid var(--green);border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:1rem">✏️</span>');
    const rel = [...document.querySelectorAll('#mProfile .btn')].find(b => b.textContent.includes('Relatório'));
    rel.insertAdjacentHTML('beforebegin', '<button class="btn btn-outline" style="margin-bottom:.35rem;padding:.7rem;font-size:.88rem">✏️ Editar apelido e personagem</button>');
  });
  await foto('09_perfil-editar.png');

  // Visão geral do fluxo
  const legendas = [
    ['01_boas-vindas.png', '1 · Boas-vindas', 'Uma frase do que a criança ganha, imagem e Jogar. "Já tenho conta" para adultos.'],
    ['02_apelido-personagem.png', '2 · Apelido e personagem', 'Uma tela só, com Pular. Apelido em vez de nome.'],
    ['03_ja-tenho-conta_adultos.png', '3 · Já tenho conta', 'Primeiro a pergunta para adultos.'],
    ['04_ja-tenho-conta_entrar.png', '4 · Entrar', 'Apple ou e-mail; os jogadores voltam.'],
    ['05_home-dica-primeiro-toque.png', '5 · Primeiro toque', 'Dica única no 2, com "Entendi".'],
    ['06_primeira-partida-direta.png', '6 · Primeira partida', 'Direto em "Sem tempo", sem a folha de velocidade.'],
    ['07_cartao-para-os-pais.png', '7 · Para os pais', 'Uma vez, depois da primeira vitória.'],
    ['08_colecao-ensina.png', '8 · Coleção que ensina', 'Tela vazia que diz como resgatar.'],
    ['09_perfil-editar.png', '9 · Perfil: editar', 'Mudar apelido e personagem depois.'],
  ];
  const html = `<html><body style="margin:0;background:#f4f1ea;font-family:Nunito,sans-serif;padding:50px 50px 30px">
    <h1 style="font-size:46px;margin:0 0 6px;color:#3c3c3c">MultiplicaMente · onboarding proposto (versão 1.0.30)</h1>
    <p style="font-size:26px;margin:0 0 34px;color:#777">Só desenhos para aprovação. Nada foi programado.</p>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:34px">${legendas.map(([f, t, d]) => `
      <div><img src="file://${OUT}/${f}" style="width:100%;border-radius:28px;box-shadow:0 10px 30px rgba(0,0,0,.18)">
      <div style="font-weight:900;font-size:30px;margin:14px 0 4px;color:#2e8b00">${t}</div>
      <div style="font-weight:700;font-size:24px;color:#555;line-height:1.3">${d}</div></div>`).join('')}</div></body></html>`;
  const fs = require('fs'), os = require('os');
  const tmp = path.join(os.tmpdir(), 'mm_onboarding_fluxo.html');
  fs.writeFileSync(tmp, html);
  const ctx2 = await browser.newContext({ viewport: { width: 2400, height: 1000 }, deviceScaleFactor: 1 });
  const p2 = await ctx2.newPage();
  await p2.goto('file://' + tmp, { waitUntil: 'load' });
  await p2.waitForTimeout(1000);
  await p2.screenshot({ path: path.join(OUT, '00_fluxo.png'), fullPage: true });
  await browser.close();
  console.log('ok');
})();
