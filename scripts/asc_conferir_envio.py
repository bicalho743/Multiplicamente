"""Confere (SÓ LEITURA) se a versão do MultiplicaMente está pronta para ser reenviada à revisão.

Roda no Codemagic (workflow "asc-conferir-envio"). Não altera nada e não envia nada.
Mostra: estado da versão, compilação anexada, Notas e conta de demonstração, estado da
compra Premium e se já existe um envio aberto.
"""
import os
import re
import sys

from asc_ligar_apple_login import call

APP_ID = os.environ.get("ASC_APP_ID", "6833585676")
PRODUTO = os.environ.get("PRODUTO", "premium_unlock")
BUILD_ESPERADA = os.environ.get("BUILD_ESPERADA", "11")
problemas = []


def tentar(rotulo, caminho):
    try:
        return call("GET", caminho)
    except Exception as e:
        print(f"   ({rotulo}: {str(e)[:160]})")
        return {}


def main():
    vs = call("GET", f"/v1/apps/{APP_ID}/appStoreVersions?filter[platform]=IOS&limit=10")["data"]
    print("== Versões iOS")
    for v in vs:
        a = v["attributes"]
        print(f"   {a['versionString']}: {a.get('appStoreState')} (criada {a.get('createdDate')})")
    v = next((x for x in vs if x["attributes"]["appStoreState"] in
              ("REJECTED", "PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "METADATA_REJECTED", "INVALID_BINARY")), vs[0])
    vid, est = v["id"], v["attributes"]["appStoreState"]
    print(f"== Versão analisada: {v['attributes']['versionString']} ({est})")

    print("== Compilação anexada")
    b = tentar("build", f"/v1/appStoreVersions/{vid}/build").get("data")
    if not b:
        print("   NENHUMA compilação anexada"); problemas.append("sem compilação anexada")
    else:
        ba = b["attributes"]
        print(f"   build {ba.get('version')} · processamento: {ba.get('processingState')} · expirada: {ba.get('expired')}")
        if str(ba.get("version")) != BUILD_ESPERADA:
            problemas.append(f"compilação anexada é a {ba.get('version')}, esperada {BUILD_ESPERADA}")

    print("== Informações de revisão (Notas)")
    d = (tentar("reviewDetail", f"/v1/appStoreVersions/{vid}/appStoreReviewDetail").get("data") or {}).get("attributes", {})
    notas = d.get("notes") or ""
    print(f"   tamanho das Notas: {len(notas)} caracteres")
    print(f"   contato: {d.get('contactFirstName')} {d.get('contactLastName')} · {d.get('contactEmail')} · telefone: {'ok' if d.get('contactPhone') else 'VAZIO'}")
    print(f"   login obrigatório: {d.get('demoAccountRequired')} · conta demo no campo: {d.get('demoAccountName') or '(vazio)'}")
    checks = [
        ("link do vídeo (photos.app.goo.gl)", "photos.app.goo.gl" in notas),
        ("cita o build 1.0.29 (%s)" % BUILD_ESPERADA, f"({BUILD_ESPERADA})" in notas),
        ("texto novo (Jogar / Sign in with Apple)", "Jogar" in notas and "Sign in with Apple" in notas),
        ("sem marcadores [E-MAIL DEMO]/[SENHA DEMO]", not re.search(r"\[(E-MAIL|SENHA) DEMO\]", notas)),
        ("sem o texto antigo (\"Novo jogador\")", "Novo jogador" not in notas),
        ("conta de demonstração ou aviso 'No demo account'", "Demo account:" in notas or "No demo account" in notas),
    ]
    for nome, ok in checks:
        print(f"   [{'ok' if ok else 'FALTA'}] {nome}")
        if not ok: problemas.append(f"Notas: {nome}")
    if not d.get("contactPhone"): problemas.append("telefone de contato vazio")

    print("== Compra Premium")
    iaps = tentar("iap", f"/v1/apps/{APP_ID}/inAppPurchasesV2?filter[productId]={PRODUTO}").get("data", [])
    if iaps:
        st = iaps[0]["attributes"].get("state")
        print(f"   {PRODUTO}: {st}")
        shot = tentar("captura", f"/v2/inAppPurchases/{iaps[0]['id']}/appStoreReviewScreenshot").get("data")
        print(f"   captura de tela para a revisão: {'enviada' if shot else 'FALTA'}")
        if st != "READY_TO_SUBMIT" and st != "APPROVED": problemas.append(f"compra Premium está {st}")
        if not shot: problemas.append("compra Premium sem captura de tela")
    else:
        problemas.append("compra Premium não encontrada")

    print("== Envios (reviewSubmissions)")
    rs = tentar("envios", f"/v1/apps/{APP_ID}/reviewSubmissions?filter[platform]=IOS&limit=10").get("data", [])
    for r in rs:
        a = r["attributes"]
        print(f"   {r['id']}: {a.get('state')} (enviado {a.get('submittedDate')})")
    if not rs: print("   nenhum")

    print("\n== RESUMO")
    if problemas:
        for p in problemas: print(f"   PENDENTE: {p}")
        print("   -> NÃO está pronto para reenviar.")
    else:
        print("   Tudo conferido. Pronto para o clique final no site.")


if __name__ == "__main__":
    main()
