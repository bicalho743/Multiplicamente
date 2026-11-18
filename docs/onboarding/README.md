# Onboarding do MultiplicaMente (proposta para a versão 1.0.30)

Segue o [Guia de onboarding para os apps Candeia Tec](https://claude.ai/artifact/9FnveWCwAkT5TTBwmLkh4d).
**Status: aprovado pelo usuário em 18/11/2026 e programado em `www/index.html` (branch `claude/affectionate-lovelace-1iw52q`), sem build.** Visão geral dos desenhos: `00_fluxo.png`.

## Passo 1: ficha de público
| Pergunta | MultiplicaMente |
|---|---|
| Quem usa? | Crianças de 6 a 10 anos (2º ao 5º ano) |
| Quem paga? | Pais e responsáveis (não é quem usa) |
| Em que momento instala? | Lição de casa de tabuada, ou o pai procura um jeito de a criança treinar |
| Primeiro resultado | A criança vence a primeira tabuada (a do 2) e resgata a primeira criatura |
| O que muda de uma pessoa para outra? | Nada que valha pergunta: só apelido e personagem |
| Precisa de conta? | Não. Conta opcional, só para adultos, no Perfil |
| Teste grátis ou plano? | Tabuadas 2 a 4 grátis; Premium (5 a 10) com pagamento único. Sem teste |
| Notificações? | Não usa |
| Regras especiais | Criança: sem cadastro, e-mail, nome real ou localização na entrada; compra, conta e relatório atrás da pergunta para adultos |

## Vale a pena?
Sim, mas leve: uma tela de boas-vindas, uma de apelido e personagem (pulável) e a primeira partida guiada.
Sem perguntas de personalização (o guia manda evitar quando o público é criança) e sem avisos de teste grátis (não há teste).

## Fluxo proposto
1. `01_boas-vindas`: frase do que a criança ganha, imagem, **Jogar** e "Já tenho conta (adultos)".
2. `02_apelido-personagem`: **apelido** (não nome completo), personagem maior, **Pular**.
3. `03_ja-tenho-conta_adultos` e `04_ja-tenho-conta_entrar`: quem reinstala entra pela pergunta para adultos (Apple ou e-mail) e os jogadores voltam.
4. `05_home-dica-primeiro-toque`: dica única no 2, com "Entendi"; nunca repete.
5. `06_primeira-partida-direta`: a primeira partida vai direto em "Sem tempo", sem a folha de 5 velocidades. As velocidades continuam nas partidas seguintes.
6. `07_cartao-para-os-pais`: uma vez, depois da primeira vitória.
7. `08_colecao-ensina`: tela vazia que explica como resgatar.
8. `09_perfil-editar`: mudar apelido e personagem depois.

## Decisões (aprovadas)
- Trocar "Seu nome" por **apelido**, com opção de pular (o jogador vira "Jogador"). Ajustar o texto da política de privacidade ("nome ou apelido").
- Voltar com um **"Já tenho conta (adultos)"** na primeira tela. Isso reabre a decisão de deixar a nuvem só no Perfil; o link só leva à mesma folha, atrás da pergunta para adultos.
- Primeira partida direto em "Sem tempo".

## Medir
O app promete "sem analytics". **Não adicionar SDK.** Usar o que as lojas já informam: instalações, sessões e retenção do 1º e do 7º dia (Play Console e App Store Connect).

## Checklist de entrega (guia)
- [x] Ficha de público
- [x] Cada pergunta tem destino (apelido e personagem: saudação e avatar)
- [ ] Telas aprovadas antes de programar
- [x] "Já tem uma conta? Entrar" na primeira tela (desenhado)
- [x] Pergunta com "Pular"
- [x] Nenhuma permissão pedida
- [x] Conta antiga não vê o onboarding (quem já tem jogador cai na lista)
- [ ] Política de privacidade com "apelido", se aprovado
- [ ] Versão nova gerada; envio às lojas só quando a usuária pedir

## Como regenerar as imagens
```
node docs/onboarding/gerar.js
```
Usa o app real (`www/index.html`) no tamanho do iPhone 15 Pro Max (1290×2796). O ícone preto de "Pergunta para adultos" na tela 3 é um limite do navegador de teste; no aparelho ele é colorido.
