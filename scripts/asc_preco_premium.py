"""Define o preço da compra "MultiplicaMente Premium" no App Store Connect.

Roda no Codemagic (workflow "asc-preco-premium"). Variáveis opcionais:
  PRECO       preço ao cliente no país base (padrão 9.99)
  TERRITORIO  país base, código de 3 letras (padrão BRA)
  SO_MOSTRAR  se "1", só mostra o preço atual e não altera nada
Os outros países são recalculados pela Apple a partir do país base.
"""
import os
import sys

from asc_ligar_apple_login import API, call

APP_ID = os.environ.get("ASC_APP_ID", "6833585676")
PRODUTO = os.environ.get("PRODUTO", "premium_unlock")
PRECO = os.environ.get("PRECO", "9.99")
TERRITORIO = os.environ.get("TERRITORIO", "BRA")
SO_MOSTRAR = os.environ.get("SO_MOSTRAR", "") == "1"


def todas(path):
    itens, inc = [], []
    while path:
        r = call("GET", path)
        itens += r.get("data", [])
        inc += r.get("included", [])
        prox = (r.get("links") or {}).get("next")
        path = prox[len(API):] if prox else None
    return itens, inc


def mostrar(iap_id):
    try:
        r = call("GET", f"/v2/inAppPurchases/{iap_id}/iapPriceSchedule?include=baseTerritory")
        base = ((r["data"].get("relationships") or {}).get("baseTerritory") or {}).get("data") or {}
        print(f"   País base: {base.get('id')}")
        precos, inc = todas(f"/v1/inAppPurchasePriceSchedules/{r['data']['id']}/manualPrices"
                            "?include=inAppPurchasePricePoint,territory&limit=200")
        pontos = {i["id"]: i["attributes"] for i in inc if i["type"] == "inAppPurchasePricePoints"}
        for p in precos:
            rel = p["relationships"]
            pp = pontos.get(rel["inAppPurchasePricePoint"]["data"]["id"], {})
            print(f"   Preço manual: {rel['territory']['data']['id']} {pp.get('customerPrice')} "
                  f"(início {p['attributes'].get('startDate')})")
    except Exception as e:
        print(f"   (não foi possível ler o preço: {e})")


def main():
    iaps, _ = todas(f"/v1/apps/{APP_ID}/inAppPurchasesV2?filter[productId]={PRODUTO}")
    if not iaps:
        sys.exit(f"Compra {PRODUTO} não encontrada.")
    iap = iaps[0]
    print(f"== {iap['attributes']['name']} ({PRODUTO}) — estado: {iap['attributes'].get('state')}")
    print("== Cadastro da compra (o que a Apple exige para enviar junto com o app)")
    a = iap["attributes"]
    print(f"   Tipo: {a.get('inAppPurchaseType')} | notas da revisão: {'ok' if a.get('reviewNote') else 'VAZIO'}"
          f" | compartilhamento familiar: {a.get('familySharable')}")
    for nome, caminho in (("Idiomas", "inAppPurchaseLocalizations"), ("Captura para a revisão", "appStoreReviewScreenshot"),
                          ("Disponibilidade", "inAppPurchaseAvailability")):
        try:
            r = call("GET", f"/v2/inAppPurchases/{iap['id']}/{caminho}")
            d = r.get("data")
            if isinstance(d, list):
                print(f"   {nome}: " + (", ".join(f"{x['attributes'].get('locale')} [{x['attributes'].get('name')} / "
                      f"{x['attributes'].get('description')}] ({x['attributes'].get('state')})" for x in d) or "NENHUM"))
            else:
                at = (d or {}).get("attributes") or {}
                print(f"   {nome}: " + (str({k: at.get(k) for k in ('fileName', 'assetDeliveryState', 'availableInNewTerritories') if k in at}) if d else "FALTA"))
        except Exception as e:
            print(f"   {nome}: FALTA ou sem acesso ({str(e)[:120]})")
    print("== Preço atual")
    mostrar(iap["id"])
    if SO_MOSTRAR:
        return
    pontos, _ = todas(f"/v2/inAppPurchases/{iap['id']}/pricePoints?filter[territory]={TERRITORIO}&limit=200")
    alvo = next((p for p in pontos if float(p["attributes"]["customerPrice"]) == float(PRECO)), None)
    if not alvo:
        perto = sorted(pontos, key=lambda p: abs(float(p["attributes"]["customerPrice"]) - float(PRECO)))[:5]
        sys.exit(f"Não existe o preço {PRECO} em {TERRITORIO}. Mais próximos: "
                 f"{[p['attributes']['customerPrice'] for p in perto]}")
    print(f"== Definindo {TERRITORIO} {alvo['attributes']['customerPrice']} como preço base")
    call("POST", "/v1/inAppPurchasePriceSchedules", {
        "data": {
            "type": "inAppPurchasePriceSchedules",
            "relationships": {
                "inAppPurchase": {"data": {"type": "inAppPurchases", "id": iap["id"]}},
                "baseTerritory": {"data": {"type": "territories", "id": TERRITORIO}},
                "manualPrices": {"data": [{"type": "inAppPurchasePrices", "id": "${preco1}"}]},
            },
        },
        "included": [{
            "type": "inAppPurchasePrices",
            "id": "${preco1}",
            "attributes": {"startDate": None},
            "relationships": {
                "inAppPurchaseV2": {"data": {"type": "inAppPurchases", "id": iap["id"]}},
                "inAppPurchasePricePoint": {"data": {"type": "inAppPurchasePricePoints", "id": alvo["id"]}},
            },
        }],
    })
    print("== Preço depois da alteração")
    mostrar(iap["id"])


if __name__ == "__main__":
    main()
