# MultiplicaMente

App de tabuada para crianças. Responda em português, passo a passo e sem jargão.

## Dados do app
- Tipo: Capacitor (app web em `www/`, projetos nativos em `ios/` e `android/`). Não usa Expo.
- Bundle / pacote: `com.solano.multiplicamente`
- App Store Connect: app id `6833585676`
- Codemagic: appId `6af482847e217e7e1a698645`
- Versão atual: 1.0.29 (enviada para revisão da Apple em 12/11/2026).
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

## Regras
- Nunca envie para revisão nem publique sem o usuário pedir.
- Google Play ainda não configurado para envio automático.
