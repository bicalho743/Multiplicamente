"""Liga a permissão "Sign In with Apple" no identificador do app (App ID).

Roda no Codemagic, dentro do workflow "ios-app-store", antes de gerar o perfil
de assinatura. Usa a chave da integração "MultiplicaMente ASC" (APP_STORE_CONNECT_*).
Se a permissão já estiver ligada, não faz nada.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

import jwt  # PyJWT

API = "https://api.appstoreconnect.apple.com"
BUNDLE = os.environ.get("BUNDLE_IDENTIFIER", "com.solano.multiplicamente")


def chave_privada():
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


def token():
    now = int(time.time())
    return jwt.encode(
        {"iss": os.environ["APP_STORE_CONNECT_ISSUER_ID"], "iat": now, "exp": now + 1000,
         "aud": "appstoreconnect-v1"},
        chave_privada(),
        algorithm="ES256",
        headers={"kid": os.environ["APP_STORE_CONNECT_KEY_IDENTIFIER"], "typ": "JWT"},
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
        raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode(errors='replace')}") from None


def main():
    ids = call("GET", f"/v1/bundleIds?filter[identifier]={BUNDLE}&limit=200")["data"]
    alvo = next((b for b in ids if b["attributes"]["identifier"] == BUNDLE), None)
    if not alvo:
        sys.exit(f"Identificador {BUNDLE} não encontrado.")
    caps = call("GET", f"/v1/bundleIds/{alvo['id']}/bundleIdCapabilities")["data"]
    tipos = [c["attributes"]["capabilityType"] for c in caps]
    print(f"Permissões atuais de {BUNDLE}: {tipos}")
    if "APPLE_ID_AUTH" in tipos:
        print("Sign In with Apple já estava ligado.")
        return
    call("POST", "/v1/bundleIdCapabilities", {"data": {
        "type": "bundleIdCapabilities",
        "attributes": {
            "capabilityType": "APPLE_ID_AUTH",
            "settings": [{"key": "APPLE_ID_AUTH_APP_CONSENT",
                          "options": [{"key": "PRIMARY_APP_CONSENT"}]}],
        },
        "relationships": {"bundleId": {"data": {"type": "bundleIds", "id": alvo["id"]}}},
    }})
    print("Sign In with Apple ligado (app principal).")


if __name__ == "__main__":
    main()
