// Gera marketing/loja/recurso_grafico_1024x500_v2.png (gráfico de destaque do Google Play).
// Feito para a página do Play no computador: o título do app cobre a esquerda e a base fica escura,
// então o conteúdo fica no centro-direita, com letra grande e poucos elementos.  Uso: node gerar_recurso_grafico.js
const { chromium } = require('playwright');
const path = require('path');
const AQUI = __dirname, ROOT = path.resolve(AQUI, '..', '..');
const FONTE = 'file://' + path.join(ROOT, 'www', 'fonts', 'nunito-latin.woff2');
const TELA = 'file://' + path.join(AQUI, '01_jornada.png');
const sc = 236 / 690; // recorte do celular na imagem de loja (1080x1920)
const html = `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:Nunito;src:url(${FONTE}) format("woff2");font-weight:200 1000}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1024px;height:500px;overflow:hidden;position:relative;font-family:Nunito,sans-serif;color:#fff;
 background:radial-gradient(circle at 80% 42%,rgba(255,255,255,.22),transparent 45%),linear-gradient(120deg,#2f9e00 0%,#12896b 55%,#0b6e9c 100%)}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.13) 2px,transparent 2px);background-size:28px 28px}
.deco{position:absolute;font-size:64px;opacity:.28}
.owl{position:absolute;left:292px;top:48px;font-size:104px;line-height:1;filter:drop-shadow(0 6px 0 rgba(0,0,0,.18))}
h1{position:absolute;left:292px;top:178px;font-size:72px;line-height:1.04;font-weight:900;letter-spacing:-1px;text-shadow:0 5px 0 rgba(0,0,0,.2)}
.pill{position:absolute;left:292px;top:352px;background:#fff;color:#1f7a00;font-weight:900;font-size:32px;border-radius:100px;padding:10px 30px;box-shadow:0 6px 0 rgba(0,0,0,.18)}
.phone{position:absolute;left:792px;top:34px;width:236px;height:480px;overflow:hidden;border-radius:46px;box-shadow:0 22px 44px rgba(0,0,0,.4);transform:rotate(-5deg);transform-origin:50% 60%}
.phone img{position:absolute;display:block;width:${1080 * sc}px;left:${-200 * sc}px;top:${-530 * sc}px}
</style>
<div class="dots"></div>
<div class="deco" style="left:36px;top:64px">🦊</div><div class="deco" style="left:150px;top:300px">🐼</div><div class="deco" style="left:40px;top:380px">🦄</div>
<div class="owl">🦉</div>
<h1>Tabuada vira<br>aventura!</h1>
<div class="pill">Grátis para começar</div>
<div class="phone"><img src="${TELA}"></div>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1024, height: 500 }, deviceScaleFactor: 1 });
  require('fs').writeFileSync('/tmp/rg.html', html); await p.goto('file:///tmp/rg.html', { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(700);
  await p.screenshot({ path: path.join(AQUI, 'recurso_grafico_1024x500_v2.png') });
  await b.close(); console.log('ok');
})();
