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

## Entrar com a Apple (iOS) — em teste
- 16/11/2026: builds 1.0.29 (8) e (9) enviados ao TestFlight a partir do branch `claude/affectionate-lovelace-1iw52q`
  (ainda não está no `main`; a versão em revisão na Apple continua sendo o build 3).
- Build 9: corrige "Excluir conta" (no build 3 a conta era excluída mas aparecia "Não foi possível excluir") e,
  em conta da Apple, pede nova confirmação e tenta desfazer o vínculo (revogação; só funciona de fato se o
  provedor Apple do Firebase tiver Services ID, Team ID, Key ID e chave configurados).
- `marketing/appstore/resposta_revisao_2_1.md` já descreve o build 9 com Entrar com a Apple.
- Cuidado: `asc-preparar-revisao` escolhe a compilação mais recente e regrava as "Notas" com o texto curto do
  script; não rode depois que o usuário colar as notas da resposta 2.1 sem antes atualizar `REVIEW_NOTES`.
- Botão "Entrar com a Apple" só no iOS; plugin nativo `AppleSignInPlugin` em `ios/App/App/AppDelegate.swift`
  (jsName `SignInWithApple`) e permissão em `ios/App/App/App.entitlements`. No Android segue o Google.
- O workflow `ios-app-store` roda `scripts/asc_ligar_apple_login.py` (liga a permissão no App ID) e recria o
  perfil de assinatura "MultiplicaMente Apple Login" a cada build.
- Pendente (usuário): testar no aparelho (entrar com a Apple, sair, entrar, excluir conta).
- Também neste branch: apagar perfil pede o portão para adultos; rodapé de Config com privacidade, contato e versão.

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
