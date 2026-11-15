# Resposta à revisão da Apple: Guideline 2.1 (Information Needed)

## Parte 1: Gravar o vídeo no iPhone (você)

Use o iPhone com o app instalado pelo TestFlight (build 1.0.29 (3)) e o iOS mais recente.

**Antes de gravar:**
- Ajustes → Central de Controle → adicione **Gravação de Tela**.
- Apague o app e instale de novo pelo TestFlight, para começar do zero.
- Tenha em mãos um e-mail de teste que ainda não tenha conta no app (ex.: revisao@candeiatec.com.br).

**Roteiro (3 a 5 minutos, sem cortes):**
1. Inicie a gravação e **abra o app** pelo ícone (a Apple exige começar pela abertura).
2. Toque em **Novo jogador** → nome `Ana` → PIN `1234` → **Criar e jogar**.
3. Na Jornada, toque na fase **2** → **Sem tempo**. Responda algumas perguntas certas.
4. Toque em **Ajuda** (as bolinhas aparecem) e **erre uma de propósito** (mostra a explicação).
5. Termine a fase (tela de vitória com a criatura resgatada) → **Continuar**.
6. Mostre as abas **Coleção** e **Recordes** e o botão de relatório (📊), digitando o PIN `1234`.
7. **Conteúdo pago:** toque na fase **7** (bloqueada) → responda a **pergunta para adultos** (ano de nascimento, ex.: 1985) → **Desbloquear** → conclua a compra de teste (no TestFlight não cobra) → mostre a fase 7 liberada.
8. Em **Config**, mostre **Já comprei · Restaurar compra**.
9. **Criar conta:** em Config → **Entrar para salvar na nuvem** → **Criar conta** → e-mail de teste + senha → mostre "Sincronizado".
10. **Sair e entrar:** **Sair da conta** → **Entrar** com o mesmo e-mail e senha.
11. **Excluir conta:** Config → **Excluir conta e dados da nuvem** → pergunta para adultos → **Sim, excluir minha conta** → mostre que voltou para "Sem conta".
12. Pare a gravação.

**Enviar o vídeo:** suba no Google Drive (compartilhar → "Qualquer pessoa com o link") ou no YouTube como **Não listado**, e copie o link.

**Conta de demonstração:** crie no app uma conta só para a Apple (ex.: `revisao.apple@candeiatec.com.br` com uma senha simples) e **não a exclua**. Coloque o e-mail e a senha no texto abaixo.

## Parte 2: Texto para colar em "Notas" (App Review Information)

Substitua `[LINK DO VÍDEO]`, `[E-MAIL DEMO]` e `[SENHA DEMO]`. Depois **salve** e responda à mensagem da Apple na Central de Resoluções dizendo que as notas foram atualizadas e o vídeo está no link.

```
1. SCREEN RECORDING
Recorded on a physical iPhone running the latest iOS (TestFlight build 1.0.29 (3)): [LINK DO VÍDEO]
It starts with launching the app and shows: creating a player profile, playing a level (hint and error explanation), the parents' report (PIN), unlocking the paid content with the In-App Purchase (sandbox), Restore Purchase, account registration, sign-out/sign-in and account deletion.

2. PURPOSE AND TARGET AUDIENCE
MultiplicaMente is an educational game that helps children (ages 6 and up, in Brazil and other Portuguese-speaking countries) learn and practice multiplication, division, addition and subtraction tables. Each table is a level in a journey; children earn stars, rescue collectible creatures and keep daily streaks, which turns repetitive drilling into play. Visual hints show what multiplication means (groups), and wrong answers are explained. Parents get a progress report (accuracy, streaks, progress per table) protected by a PIN. The app has no ads and works offline.

3. HOW TO ACCESS THE MAIN FEATURES
No login is required. Open the app, tap "Novo jogador", type any name and a 4-digit PIN (e.g. 1234), then "Criar e jogar".
- Journey: tap a level number and choose "Sem tempo" (no timer) or a speed.
- Tabs: Jornada (journey), Recordes (records), Coleção (creatures), Config (settings). The chart button opens the parents' report (enter the PIN).
- Paid content: tables 7 to 10 are unlocked by the non-consumable In-App Purchase "MultiplicaMente Premium" (premium_unlock). Tap level 7 or Config > "Desbloquear Premium". A parental gate asks for the adult's year of birth (any adult year, e.g. 1985). "Já comprei · Restaurar compra" restores the purchase.
- Optional account (only to sync progress between devices): Config > "Entrar para salvar na nuvem" > "Criar conta" (email and password). Account deletion: Config > "Excluir conta e dados da nuvem" (deletes the account and its cloud data).
Demo account: [E-MAIL DEMO] / [SENHA DEMO]
There is no user-generated content shared between users and no chat, so no reporting/blocking is needed. The records tab only compares profiles on the same device.

4. EXTERNAL SERVICES
- Apple In-App Purchase (StoreKit 2): the Premium purchase and restore.
- Google Firebase Authentication (email/password): the optional account. Google Sign-In is not offered on iOS.
- Google Cloud Firestore: stores the optional cloud copy of the player profiles and progress.
- Apple StoreKit review prompt (SKStoreReviewController).
No ads, no analytics or tracking SDKs, no AI services. All game content runs locally; fonts and libraries are bundled in the app.

5. REGIONAL DIFFERENCES
The app works the same in all regions. The content is in Brazilian Portuguese. Only the price of the In-App Purchase changes by region, according to Apple's price tiers.

6. REGULATED INDUSTRY / THIRD-PARTY MATERIAL
Not applicable. The app is not in a regulated industry and does not use protected third-party material. Artwork and creatures use standard emoji; the font is Nunito (SIL Open Font License).
```
