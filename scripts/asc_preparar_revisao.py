"""Prepara a versão do MultiplicaMente no App Store Connect para revisão.

Roda no Codemagic (workflow "asc-preparar-revisao"), que fornece a chave de API
da integração "MultiplicaMente ASC" nas variáveis APP_STORE_CONNECT_*.

O que faz (só preenche; NÃO envia para revisão):
  - URL da política de privacidade (Informações do app, pt-BR)
  - Direitos de conteúdo: não usa conteúdo de terceiros
  - Categoria primária Educação (secundária Jogos > Educativo)
  - Escolhe a compilação válida mais recente da versão e declara criptografia
  - Informações de contato e notas da revisão (sem login obrigatório)
No fim, imprime um resumo do que ainda falta.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

import jwt  # PyJWT

API = "https://api.appstoreconnect.apple.com"
APP_ID = os.environ.get("ASC_APP_ID", "6833585676")
VERSION = os.environ.get("ASC_VERSION", "1.0")
LOCALE = "pt-BR"
PRIVACY_URL = "https://bicalho743.github.io/Multiplicamente/privacidade.html"
REVIEW_NOTES = (
    'O app funciona sem conta e sem internet. Para testar: toque em "Novo jogador", '
    "crie um perfil (nome + PIN de 4 números) e jogue. As tabuadas do 2 ao 6 são grátis; "
    'as do 7 ao 10 são liberadas pela compra não consumível "MultiplicaMente Premium" '
    '(premium_unlock), em Config. "Restaurar compra" também fica em Config. A compra, o '
    "relatório dos pais e as configurações sensíveis ficam atrás de uma pergunta para adultos "
    "(digitar o ano de nascimento; qualquer ano de adulto funciona, ex.: 1985). A conta por "
    "e-mail é opcional (só para sincronizar entre aparelhos) e pode ser excluída em Config → "
    '"Excluir conta e dados da nuvem".'
)

pendencias = []


def chave_privada():
    """Aceita a chave como PEM, PEM com '\\n' literais, base64 puro ou caminho de arquivo."""
    k = os.environ["APP_STORE_CONNECT_PRIVATE_KEY"].strip()
    if k.startswith("@file:"):
        k = open(k[len("@file:"):]).read().strip()
    elif os.path.isfile(k):
        k = open(k).read().strip()
    k = k.replace("\\n", "\n").strip().strip('"').strip("'")
    if "BEGIN" not in k:
        corpo = "".join(k.split())
        linhas = [corpo[i:i + 64] for i in range(0, len(corpo), 64)]
        k = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(linhas) + "\n-----END PRIVATE KEY-----"
    return k + "\n"


def diagnostico_chave():
    bruto = os.environ["APP_STORE_CONNECT_PRIVATE_KEY"]
    k = chave_privada()
    print(f"   chave: {len(bruto)} caracteres, {bruto.count(chr(10))} quebras reais, "
          f"{bruto.count(chr(92) + 'n')} '\\n' literais, tem BEGIN={'BEGIN' in bruto}; "
          f"normalizada: {k.splitlines()[0]} ... {k.splitlines()[-1]}")


def token():
    key_id = os.environ["APP_STORE_CONNECT_KEY_IDENTIFIER"]
    issuer = os.environ["APP_STORE_CONNECT_ISSUER_ID"]
    private_key = chave_privada()
    now = int(time.time())
    return jwt.encode(
        {"iss": issuer, "iat": now, "exp": now + 1000, "aud": "appstoreconnect-v1"},
        private_key,
        algorithm="ES256",
        headers={"kid": key_id, "typ": "JWT"},
    )


def call(method, path, body=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {detail}") from None


def passo(nome, fn):
    print(f"\n== {nome}")
    try:
        fn()
    except Exception as e:  # segue para os próximos passos
        print(f"   ERRO: {e}")
        pendencias.append(f"{nome}: {e}")


def direitos_de_conteudo():
    app = call("GET", f"/v1/apps/{APP_ID}")["data"]
    print(f"   App: {app['attributes']['name']} ({app['attributes']['bundleId']})")
    atual = app["attributes"].get("contentRightsDeclaration")
    if atual:
        print(f"   Já definido: {atual}")
        return
    call("PATCH", f"/v1/apps/{APP_ID}", {"data": {"type": "apps", "id": APP_ID, "attributes": {
        "contentRightsDeclaration": "DOES_NOT_USE_THIRD_PARTY_CONTENT"}}})
    print("   OK: não usa conteúdo de terceiros")


def app_info_editavel():
    infos = call("GET", f"/v1/apps/{APP_ID}/appInfos")["data"]
    for info in infos:
        estado = info["attributes"].get("state") or info["attributes"].get("appStoreState")
        if estado not in ("READY_FOR_DISTRIBUTION", "READY_FOR_SALE", "REPLACED_WITH_NEW_INFO"):
            return info
    return infos[0]


def categorias():
    info = app_info_editavel()
    call("PATCH", f"/v1/appInfos/{info['id']}", {"data": {"type": "appInfos", "id": info["id"],
        "relationships": {"primaryCategory": {"data": {"type": "appCategories", "id": "EDUCATION"}}}}})
    print("   OK: categoria primária Educação")
    try:
        call("PATCH", f"/v1/appInfos/{info['id']}", {"data": {"type": "appInfos", "id": info["id"],
            "relationships": {
                "secondaryCategory": {"data": {"type": "appCategories", "id": "GAMES"}},
                "secondarySubcategoryOne": {"data": {"type": "appCategories", "id": "GAMES_EDUCATIONAL"}},
            }}})
        print("   OK: categoria secundária Jogos > Educativo")
    except RuntimeError as e:
        print(f"   (categoria secundária não aplicada, é opcional: {e})")


def politica_privacidade():
    info = app_info_editavel()
    locs = call("GET", f"/v1/appInfos/{info['id']}/appInfoLocalizations")["data"]
    alvo = next((l for l in locs if l["attributes"]["locale"] == LOCALE), None)
    if alvo is None:
        print(f"   Idiomas existentes: {[l['attributes']['locale'] for l in locs]}")
        alvo = locs[0]
    call("PATCH", f"/v1/appInfoLocalizations/{alvo['id']}", {"data": {
        "type": "appInfoLocalizations", "id": alvo["id"],
        "attributes": {"privacyPolicyUrl": PRIVACY_URL}}})
    print(f"   OK ({alvo['attributes']['locale']}): {PRIVACY_URL}")


def versao():
    vs = call("GET", f"/v1/apps/{APP_ID}/appStoreVersions?filter[platform]=IOS"
                     f"&filter[versionString]={VERSION}")["data"]
    if not vs:
        raise RuntimeError(f"versão {VERSION} não encontrada")
    v = vs[0]
    print(f"   Versão {VERSION}: {v['attributes']['appStoreState']}")
    return v


def compilacao():
    v = versao()
    builds = call("GET", f"/v1/builds?filter[app]={APP_ID}&filter[preReleaseVersion.version]={VERSION}"
                         "&sort=-uploadedDate&limit=20")["data"]
    for b in builds:
        a = b["attributes"]
        print(f"   build {a['version']}: {a['processingState']} expirado={a['expired']} "
              f"criptografia={a.get('usesNonExemptEncryption')}")
    validos = [b for b in builds if b["attributes"]["processingState"] == "VALID" and not b["attributes"]["expired"]]
    if not validos:
        raise RuntimeError("nenhuma compilação VALID para a versão; gere uma nova no Codemagic")
    b = validos[0]
    if b["attributes"].get("usesNonExemptEncryption") is None:
        call("PATCH", f"/v1/builds/{b['id']}", {"data": {"type": "builds", "id": b["id"],
            "attributes": {"usesNonExemptEncryption": False}}})
        print("   OK: criptografia declarada (não usa criptografia própria)")
    call("PATCH", f"/v1/appStoreVersions/{v['id']}/relationships/build",
         {"data": {"type": "builds", "id": b["id"]}})
    print(f"   OK: compilação {b['attributes']['version']} escolhida para a versão {VERSION}")


def contato_revisao():
    v = versao()
    phone = os.environ.get("REVIEW_CONTACT_PHONE", "").strip()
    attrs = {
        "contactFirstName": os.environ.get("REVIEW_CONTACT_FIRST_NAME", "Solano"),
        "contactLastName": os.environ.get("REVIEW_CONTACT_LAST_NAME", "Bicalho"),
        "contactEmail": os.environ.get("REVIEW_CONTACT_EMAIL", "contato@candeiatec.com.br"),
        "demoAccountRequired": False,
        "notes": REVIEW_NOTES,
    }
    if phone:
        attrs["contactPhone"] = phone
    else:
        pendencias.append("Informações de contato: falta o telefone (REVIEW_CONTACT_PHONE)")
    try:
        atual = call("GET", f"/v1/appStoreVersions/{v['id']}/appStoreReviewDetail")["data"]
    except RuntimeError:
        atual = None
    if atual:
        call("PATCH", f"/v1/appStoreReviewDetails/{atual['id']}", {"data": {
            "type": "appStoreReviewDetails", "id": atual["id"], "attributes": attrs}})
    else:
        call("POST", "/v1/appStoreReviewDetails", {"data": {
            "type": "appStoreReviewDetails", "attributes": attrs,
            "relationships": {"appStoreVersion": {"data": {"type": "appStoreVersions", "id": v["id"]}}}}})
    print(f"   OK: contato {attrs['contactFirstName']} {attrs['contactLastName']}, "
          f"{attrs['contactEmail']}, telefone {'preenchido' if phone else 'FALTANDO'}; notas e sem login")


def conferir_textos():
    v = versao()
    locs = call("GET", f"/v1/appStoreVersions/{v['id']}/appStoreVersionLocalizations")["data"]
    for l in locs:
        a = l["attributes"]
        faltam = [c for c in ("description", "keywords", "supportUrl") if not a.get(c)]
        sets = call("GET", f"/v1/appStoreVersionLocalizations/{l['id']}/appScreenshotSets")["data"]
        tipos = [s["attributes"]["screenshotDisplayType"] for s in sets]
        print(f"   {a['locale']}: faltam={faltam or 'nada'} capturas={tipos}")
        if faltam:
            pendencias.append(f"Textos {a['locale']}: faltam {faltam}")
    try:
        idade = call("GET", f"/v1/appInfos/{app_info_editavel()['id']}/ageRatingDeclaration")["data"]
        print(f"   Classificação etária: declarada (id {idade['id']})")
    except RuntimeError as e:
        print(f"   Classificação etária: não consegui ler ({e})")


if __name__ == "__main__":
    for var in ("APP_STORE_CONNECT_KEY_IDENTIFIER", "APP_STORE_CONNECT_ISSUER_ID", "APP_STORE_CONNECT_PRIVATE_KEY"):
        if not os.environ.get(var):
            sys.exit(f"Variável {var} ausente: confira 'integrations: app_store_connect' no codemagic.yaml")
    passo("Formato da chave", diagnostico_chave)
    passo("Direitos de conteúdo", direitos_de_conteudo)
    passo("Categorias", categorias)
    passo("Política de privacidade", politica_privacidade)
    passo("Compilação", compilacao)
    passo("Informações de contato da revisão", contato_revisao)
    passo("Conferência de textos e imagens", conferir_textos)
    print("\n== RESUMO")
    if pendencias:
        print("Ainda falta:")
        for p in pendencias:
            print(" -", p)
    else:
        print("Tudo preenchido. Confira no App Store Connect e clique em 'Adicionar para revisão'.")
    print("Lembrete: 'Práticas de coleta de dados' (Privacidade do app) e 'Preços' não têm API: "
          "confira no site se já estão publicados.")
