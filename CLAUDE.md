# MultiplicaMente

Trabalho no PC: ver bicalho743/meu-enxoval-em-dia/docs/CLAUDE-NO-PC.md

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
- Os dois usam a integração `MultiplicaMente ASC` e `instance_type: mac_mini_m2` (o plano não tem Linux).

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
- 19/11/2026: contato do site e da política de privacidade (`index.html`, `privacidade.html`) trocado para
  contato@candeiatec.com.br (antes era o e-mail pessoal do Solano).

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

## Onde paramos (26/11/2026)
- **Revisão da Apple (Guideline 2.1):** a resposta está pronta em `marketing/appstore/resposta_revisao_2_1.md`; falta
  o vídeo, a conta de demonstração e reenviar (ver "Situação da revisão"). Conferir no App Store Connect se mudou algo.
- **Contato:** site e política de privacidade com `contato@candeiatec.com.br` desde 19/11 (saiu o e-mail pessoal).
- **Ícone:** o da capa do WhatsApp da Candeia Tec é o `AppIcon-512@2x.png` do iOS (o Android tem moldura interna).
- **Google Play:** envio ainda manual; falta o workflow `android-play` e o keystore no Codemagic.
- **Plano de marketing 2027:** PDF guardado no Hub (Candeia_Tec › Marketing), não neste repositório.
