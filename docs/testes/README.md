# Testes de tela (sem aparelho)

Rodam o app real (`www/index.html`) num navegador de teste (Playwright) no tamanho do iPhone 15 Pro Max.
Requer Node 22 e `playwright` (`npm i -g playwright` e `npx playwright install chromium`).

| Arquivo | O que faz |
|---|---|
| `test_onboarding.js` | Fluxo completo do onboarding: boas-vindas, apelido/Pular, "Já tenho conta", dica do 2, primeira partida direta, cartão para os pais, Coleção, editar perfil, nomes padrão. Saída: `ok`/`FALHA` por passo. Prints em `OUT=<pasta>` |
| `test_colecao.js` | Dica da Coleção vazia e a partida perfeita |
| `test_abertura.js` | Abre a página 4 vezes e conta erros de JavaScript |
| `telas_*.js` | Geram prints das telas (onboarding, Perfil, primeira vez) |

Uso: `OUT=./saida node docs/testes/test_onboarding.js` (no Windows, no Git Bash). Alguns testes pedem o caminho de
saída como primeiro argumento. Nota: o navegador de teste às vezes mostra um erro de script do Firebase ao abrir o
arquivo direto (`file://`); não vem do app e não aparece no aparelho.
