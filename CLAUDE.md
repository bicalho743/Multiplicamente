# MultiplicaMente

App de tabuada para crianças. Responda em português, passo a passo e sem jargão.

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

## Onboarding (proposta para a 1.0.30, só desenhos; aguardando aprovação)
- Telas e decisões em `docs/onboarding/` (`00_fluxo.png`, `README.md`; gerar de novo: `node docs/onboarding/gerar.js`).
- Segue o guia da Candeia Tec: sem cadastro na entrada, apelido em vez de nome, "Já tenho conta (adultos)", primeira
  partida direto em "Sem tempo", dica no primeiro toque, cartão para os pais após a primeira vitória, editar apelido e
  personagem no Perfil. Sem SDK de analytics (usar as métricas das lojas).
- Só programar depois da aprovação do usuário.

## Android
- O .aab assinado é gerado no computador do usuário. O keystore `multiplicamente.jks` não fica no repositório
  (está no .gitignore). Para gerar pelo Codemagic, o usuário precisa enviar o keystore em Settings → Code signing
  identities → Android keystores (reference name `multiplicamente_keystore`) e criar um workflow `android-play`.

## Ambiente do Claude Code
- Use o ambiente "Multiplicamente": nele o proxy injeta o token da API do Codemagic (header
  `x-auth-token: proxy-injected`). Disparar: POST https://api.codemagic.io/builds
  {"appId":"6af482847e217e7e1a698645","workflowId":"ios-app-store","branch":"main"};
  status: GET /builds/<id>; log de uma etapa: GET /builds/<id>/step/<buildActions[]._id>.

## Regras
- Nunca envie para revisão nem publique sem o usuário pedir.
- Google Play ainda não configurado para envio automático.
