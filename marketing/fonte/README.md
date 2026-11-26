# Scripts que geram imagens de marketing

- `carrossel_vendas_build.py` + `carrossel_vendas_render.js`: carrossel de vendas do Instagram (7 imagens 1080×1350,
  `marketing/social/2026-11 vendas multiplicamente/`). Uso: `python carrossel_vendas_build.py <slides.html>` e depois
  `node carrossel_vendas_render.js <slides.html> <pasta_de_saida>`.
- `captura_compra_premium.js`: tela de compra do Premium (1290×2796) para a revisão da compra no App Store Connect.
- O gráfico de destaque do Google Play é gerado por `marketing/loja/gerar_recurso_grafico.js`; as telas de onboarding por
  `docs/onboarding/gerar.js`.
