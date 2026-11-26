# MultiplicaMente

App de tabuada para crianças. Responda em português, passo a passo e sem jargão.
Trabalho no PC: ver bicalho743/meu-enxoval-em-dia/docs/CLAUDE-NO-PC.md

## Ids e contas (resumo)
| Item | Valor |
|---|---|
| Tipo | **Capacitor 8** (`www/` + `ios/` + `android/`). Não é Expo nem site |
| Bundle iOS / pacote Android | `com.solano.multiplicamente` |
| Apple Team | `78UAFVLGA9` (Solano Bicalho, Individual) |
| App Store Connect (app id) | `6833585676` |
| Codemagic (appId) | `6af482847e217e7e1a698645` (integração `MultiplicaMente ASC`) |
| Expo / EAS | não usa |
| RevenueCat | projeto `proj19ead3d1` existe, mas **o app não usa** (vazio; só "Test Store") |
| Supabase / Render | não usa |
| Firebase | `multiplicamente-ccacc` (Auth: e-mail, Google no Android, Apple no iOS; Firestore) |
| Google Play | `com.solano.multiplicamente`, em produção (1.0.29) |
| Instagram / Upload-Post | perfil Upload-Post `@vidaemmetodo01` (nome "Multiplicamente"); Instagram `vidaemmetodo01` |
| Site / páginas do app | repo `bicalho743/Candeia_Tec`, pasta `apps/multiplicamente/` (privacidade, termos, suporte, excluir conta) |

## Onde paramos (26/11/2026)
**Em revisão na Apple:** versão 1.0.29, **compilação 11** (Notas em inglês com o vídeo, conta demo = "não é necessária").
- 20/11: Apple pediu ajuste da classificação etária (2.3.6): "Verificação de idade" passou para Não; "Controles parentais" Sim. Respondido e reenviado.
- 25/11: Apple pediu "conta de demonstração com assinatura expirada" (2.1). O app não tem assinatura (Premium é compra única). Respondido. **Aguardando a Apple.** Se ela responder, rodar `asc-conferir-envio`.
- Não anexar o build 12 a esta versão: o vídeo e as Notas descrevem o build 11 (Premium libera 7 a 10; aba Config).

**No TestFlight, sem testar no aparelho:** build 12 (branch `claude/affectionate-lovelace-1iw52q`) com onboarding novo, Perfil com as configurações (sem aba Config) e tabuadas 2 a 4 grátis.

**Git:** a branch está 29 commits à frente do `main` e o `main` tem 1 commit que ela não tem (`0f9c60b`, troca do e-mail de contato; já feita na branch). Nada foi juntado ao `main`. Juntar com uma PR (merge normal, sem rebase) **só depois da aprovação da Apple**, junto com a versão 1.0.30.

**Versão 1.0.30 (pronta no código, SEM publicar):** tabuadas 2 a 4 grátis; Perfil no lugar da aba Config; onboarding (`docs/onboarding/`). Antes de publicar, trocar juntos: textos da App Store e do Google Play (`marketing/appstore/textos.md`), `index.html` do repositório, páginas do Candeia_Tec ("Config" → "Perfil"), Notas e roteiro do vídeo da Apple, e o post do Instagram (diz "2 ao 6 grátis").

**Google Play / redes (pendências do usuário):**
- Subir o gráfico novo `marketing/loja/recurso_grafico_1024x500_v2.png` (Play Console → Presença na loja → Página principal da loja). O que está no ar diz "2 ao 5 grátis".
- Link da bio do Instagram: usar `https://play.google.com/store/apps/details?id=com.solano.multiplicamente` (o atual não abre). Nome do perfil ainda "Vida em Metodo".
- Post do carrossel publicado em 18/11: https://www.instagram.com/p/Df3RR4MCBYI/ (confirmar se as 7 imagens entraram).

**Decisões pendentes (do usuário):**
1. Quando juntar a branch ao `main` e publicar a 1.0.30 (Android: gerar o .aab no PC; iOS: Codemagic).
2. Integrar ou não o RevenueCat (hoje as vendas só aparecem no Play Console e no App Store Connect). Se sim, numa versão futura com testes.
3. Criar conta de demonstração por e-mail para a Apple (hoje o texto diz que não é necessária).

**Arquivos do trabalho:** textos e artes das lojas em `marketing/appstore/` (iOS), `marketing/loja/` (Google Play e gráficos), `marketing/social/` (posts), `marketing/telas/`; onboarding em `docs/onboarding/`; testes de tela em `docs/testes/`.

## Dados do app
- Tipo: Capacitor (app web em `www/`, projetos nativos em `ios/` e `android/`). Não usa Expo.
- Bundle / pacote: `com.solano.multiplicamente`
- App Store Connect: app id `6833585676`
- Codemagic: appId `6af482847e217e7e1a698645`
- Versão atual: 1.0.29, build iOS 1.0.29 (3) (enviada para revisão da Apple em 12/11/2026).
  A versão fica em `ios/App/App.xcodeproj/project.pbxproj` (MARKETING_VERSION) e
  `android/app/build.gradle` (versionName/versionCode); a versão da loja tem que ser igual.
- Compra dentro do app: "MultiplicaMente Premium" (`premium_unlock`, não consumível).
- Política de privacidade: https://bicalho743.github.io/Multiplicamente/privacidade.html (GitHub Pages)

## Workflows do Codemagic (`codemagic.yaml`)
- `ios-app-store`: compila o .ipa assinado e envia ao TestFlight. O número do build vem de `$BUILD_NUMBER`.
- `asc-preparar-revisao`: roda `scripts/asc_preparar_revisao.py`, que preenche no App Store Connect a URL de
  privacidade, os direitos de conteúdo, a categoria, a compilação, o copyright e o contato da revisão, e
  imprime no fim o que ainda falta. Passe `REVIEW_CONTACT_PHONE` nas variables ao disparar. Não envia para revisão.
- `asc-preco-premium`: roda `scripts/asc_preco_premium.py`; mostra o cadastro da compra Premium e define o preço
  (variables `PRECO`, `TERRITORIO`; `SO_MOSTRAR=1` só mostra). Em 17/11/2026 ficou em R$ 9,99, país base Brasil
  (estava R$ 9,90).
- `asc-conferir-envio`: SÓ LEITURA (`scripts/asc_conferir_envio.py`). Mostra a compilação anexada, as Notas, a conta
  demo, o estado da compra Premium e os envios; termina com "PENDENTE: ..." ou "Pronto para o clique final".
  Rode antes de reenviar à revisão (variable opcional `BUILD_ESPERADA`, padrão 11).
- Todos usam a integração `MultiplicaMente ASC` e `instance_type: mac_mini_m2` (o plano não tem Linux).

## Loja
- Textos, imagens e roteiro do App Store Connect: `marketing/appstore/`.
- Contato da revisão: Solano Bicalho, contato@candeiatec.com.br. Copyright: 2026 Candeia Tec.
- Pelo site apenas: práticas de privacidade (salvar e Publicar), preços, classificação etária e o clique
  final em "Adicionar para revisão".

- Gráfico de destaque do Google Play: `marketing/loja/recurso_grafico_1024x500_v2.png` (gerar: `node marketing/loja/gerar_recurso_grafico.js`).
  Feito para a página do Play no computador (conteúdo no centro-direita, letra grande, sem número de tabuadas grátis).
  O que está no ar dizia "Tabuadas do 2 ao 5 grátis" (não bate com o app).

## Situação da revisão (atualize aqui)
- 13/11/2026: a Apple respondeu "Guideline 2.1 - Information Needed" (não é recusa; pediu informações).
- Resposta pronta em `marketing/appstore/resposta_revisao_2_1.md`: roteiro do vídeo e texto em inglês para "Notas".
- Pendente (usuário): gravar o vídeo no iPhone pelo TestFlight, subir (Drive ou YouTube não listado), criar uma
  conta de demonstração que não seja excluída, colar o texto com link/e-mail/senha em Notas, responder na
  Central de Resoluções e reenviar.
- 16/11/2026: e-mail de contato da política (`privacidade.html`) e da página do app (`index.html`) trocado para
  contato@candeiatec.com.br no branch `claude/affectionate-lovelace-1iw52q`; só vai ao ar quando entrar no `main`.
- 16/11/2026: provedor Apple ativado no Firebase (Authentication → Método de login).
- 17/11/2026: usuário testou o build 9 no aparelho: entrar com a Apple e excluir conta funcionando.
- 17/11/2026: a compra `premium_unlock` está como "Faltam metadados": falta a captura de tela para a revisão
  (e as notas da revisão estão vazias). Sem isso a compra não segue junto com o app. Pendente (usuário, pelo site).

- 18/11/2026: conferência antes do reenvio: versão 1.0.29 "Rejeitada" ainda com a compilação 3, Notas antigas
  (624 caracteres) e compra Premium sem captura de tela. Nada foi reenviado. Vídeo no Google Fotos (link nas Notas).

- 20/11/2026: a Apple analisou o build 11 e respondeu Guideline 2.3.6 (metadados): a classificação etária declarava
  "Verificação de idade" (`ageAssurance`) = Sim e "Controles parentais" (`parentalControls`) = Sim, e o revisor (iPad Air)
  não achou nenhum dos dois. Plano: mudar "Verificação de idade" para Não (o app não verifica idade), manter "Controles
  parentais" = Sim e responder dizendo onde estão (portão de adultos com ano de nascimento + PIN do relatório; compras,
  conta, apagar perfil). Não precisa de build novo. `asc-conferir-envio` agora mostra a declaração etária.

- 20/11/2026: usuário mudou "Verificação de idade" para Não (confirmado pela API), respondeu à Apple e reenviou a
  versão 1.0.29 (build 11 mantido; a 12 não foi anexada).
- 25/11/2026: a Apple (iPad Air) pediu na Guideline 2.1 "conta de demonstração com assinatura expirada". O app não tem
  assinatura: o Premium é compra única não consumível. O usuário respondeu explicando isso e o passo a passo para
  testar a compra e a restauração (no build 11 o Premium libera 7 a 10). Aguardando a Apple; se ela responder de novo,
  rodar `asc-conferir-envio` para ver o estado.
- 24/11/2026: o app NÃO usa RevenueCat (compra pelo `BillingPlugin` no Android e StoreKit 2 no iOS), então vendas do Play
  não aparecem no RevenueCat (projeto `proj19ead3d1` vazio, só "Test Store"). Vendas: ver Play Console e App Store Connect.
  Integrar o RevenueCat só numa versão futura, com testes.

## Entrar com a Apple (iOS) — em teste
- 16 e 17/11/2026: builds 1.0.29 (8) a (11) enviados ao TestFlight a partir do branch `claude/affectionate-lovelace-1iw52q`
  (ainda não está no `main`; a versão em revisão na Apple continua sendo o build 3).
- Build 9: corrige "Excluir conta" (no build 3 a conta era excluída mas aparecia "Não foi possível excluir") e,
  em conta da Apple, pede nova confirmação e tenta desfazer o vínculo (revogação; só funciona de fato se o
  provedor Apple do Firebase tiver Services ID, Team ID, Key ID e chave configurados).
- Build 11 (17/11/2026): "Excluir conta" ganhou a caixinha "Apagar também os jogadores e o progresso guardados neste celular" (desmarcada por padrão).
- Build 10 (17/11/2026): primeira tela só com nome e personagem (botão Jogar); o PIN dos pais é criado na
  primeira vez que abrem o relatório; a conta na nuvem saiu da tela inicial e virou a folha `mCloud`, aberta
  pelo perfil e por Config (atrás da pergunta para adultos). Ao entrar na conta, volta para a lista de jogadores.
  Pendente (usuário): testar no aparelho os fluxos de conta pelo caminho novo. Se falhar, o build 9 é a reserva.
- `marketing/appstore/resposta_revisao_2_1.md` já descreve o build 11 (fluxo novo) com Entrar com a Apple.
- Cuidado: `asc-preparar-revisao` escolhe a compilação mais recente e regrava as "Notas" com o texto curto do
  script; não rode depois que o usuário colar as notas da resposta 2.1 sem antes atualizar `REVIEW_NOTES`.
- Botão "Entrar com a Apple" só no iOS; plugin nativo `AppleSignInPlugin` em `ios/App/App/AppDelegate.swift`
  (jsName `SignInWithApple`) e permissão em `ios/App/App/App.entitlements`. No Android segue o Google.
- O workflow `ios-app-store` roda `scripts/asc_ligar_apple_login.py` (liga a permissão no App ID) e recria o
  perfil de assinatura "MultiplicaMente Apple Login" a cada build.
- Pendente (usuário): testar no aparelho (entrar com a Apple, sair, entrar, excluir conta).
- Também neste branch: apagar perfil pede o portão para adultos; rodapé de Config com privacidade, contato e versão.

## Versão 1.0.30 (planejada; só no branch, SEM build; o build 11 é o que está em revisão)
- Tabuadas 2 a 4 grátis; Premium libera 5 a 10 (`FREE_TABLES`/`PREMIUM_TABLES` em `www/index.html` e textos do app).
- A aba "Config" saiu: volume, modo escuro, Premium, conta e rodapé legal agora ficam no **Perfil** (toque no personagem
  com o selo "Perfil" no topo da Home). Lista de jogadores: todos os cartões com o mesmo visual (verde).
- Ao publicar, trocar juntos: textos da App Store e do Google Play (`marketing/appstore/textos.md`), `index.html` do
  repositório, páginas do site (candeia_tec: suporte e excluir conta dizem "Config" → "Perfil"), Notas da Apple
  (`REVIEW_NOTES` e `resposta_revisao_2_1.md`: "Config" → "Perfil", "fase 7" → "fase 5") e o post/legenda
  (`marketing/social/`, que hoje diz "2 ao 6 grátis").
- Quem já usa o app no Google Play perde o acesso às tabuadas 5 e 6 (o progresso fica salvo).

## Onboarding (aprovado e programado para a 1.0.30; sem build)
- Telas e decisões em `docs/onboarding/` (`00_fluxo.png`, `README.md`; gerar de novo: `node docs/onboarding/gerar.js`).
- Segue o guia da Candeia Tec: sem cadastro na entrada, apelido em vez de nome, "Já tenho conta (adultos)", primeira
  partida direto em "Sem tempo", dica no primeiro toque, cartão para os pais após a primeira vitória, editar apelido e
  personagem no Perfil. Sem SDK de analytics (usar as métricas das lojas).
- Aprovado em 18/11/2026 e programado: boas-vindas (`#welcomeBox`) → apelido e personagem (pulável; em branco vira
  "Jogador", "Jogador 2"...) → Home com dica no 2 (`maybeShowFirstTapHint`, grava `mm_hint_tap`) → primeira partida do
  jogador direto em "Sem tempo" (`openSpeed`) → cartão `mParents` uma vez após a 1ª vitória (grava `mm_parent_card`).
  "Já tenho conta (adultos)" na primeira tela abre a folha `mCloud` em modo "entrar" atrás da pergunta para adultos.
  Perfil: "Editar apelido e personagem" (`mEditProfile`). Coleção vazia mostra a dica (`#collTip`).
- Testado em navegador (fluxos completos, sem erros). Build 12 (18/11/2026) enviado ao TestFlight com o onboarding, o Perfil
  e as tabuadas 2 a 4 grátis; falta testar no aparelho. A versão em revisão continua sendo a do build 11.
- Ao publicar a 1.0.30, também trocar: Notas da Apple ("type any name" → apelido; "Config" → "Perfil"), roteiro do vídeo,
  página de suporte (candeia_tec) e a política de privacidade do site (já ajustada aqui para "apelido ou nome").

## Android
- O .aab assinado é gerado no computador do usuário. O keystore `multiplicamente.jks` não fica no repositório
  (está no .gitignore). Para gerar pelo Codemagic, o usuário precisa enviar o keystore em Settings → Code signing
  identities → Android keystores (reference name `multiplicamente_keystore`) e criar um workflow `android-play`.

## Ambiente do Claude Code
- **No PC (Windows):** não há proxy. O token do Codemagic vem da variável de usuário `CM_API_TOKEN`, enviada no header
  `x-auth-token`. Scripts em python3/bash: rodar no Git Bash ou trocar por `python`. Build de iPhone nunca no Windows
  (Codemagic ou EAS). App Store Connect e Play Console: pelo Chrome já logado.
- **Na nuvem (antigo):** use o ambiente "Multiplicamente": nele o proxy injeta o token da API do Codemagic (header
  `x-auth-token: proxy-injected`). Disparar: POST https://api.codemagic.io/builds
  {"appId":"6af482847e217e7e1a698645","workflowId":"ios-app-store","branch":"main"};
  status: GET /builds/<id>; log de uma etapa: GET /builds/<id>/step/<buildActions[]._id>.

## Regras
- Nunca envie para revisão nem publique sem o usuário pedir.
- Google Play ainda não configurado para envio automático.
