# -*- coding: utf-8 -*-
"""n8n'de olusturulmus credential'lari Angie workflow'undaki node'lara baglar.

Kullanim:
    py baglantilari-kur.py            -> sadece credential baglar
    py baglantilari-kur.py 123456789  -> ayrica izinli_id'yi ayarlar

Credential'lari n8n arayuzunden olusturmak gerekir; bu script sadece
olusturulmus olanlari dogru node'lara eslestirir.
"""
import json, os, sqlite3, sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(os.path.expanduser("~"), ".n8n", "database.sqlite")
WF = os.path.join(KOK, "workflows", "01-angie.json")

# node adi -> gereken credential tipi
ESLEME = {
    "Telegram Mesaji":    "telegramApi",
    "Kimlik Bildir":      "telegramApi",
    "Desteklenmiyor":     "telegramApi",
    "Telegram Cevap":     "telegramApi",
    "Anthropic Modeli":   "anthropicApi",
    "Takvim":             "googleCalendarOAuth2Api",
    "Gmail":              "gmailOAuth2",
}


def main():
    con = sqlite3.connect(DB)
    mevcut = {}
    for cid, ad, tip in con.execute("select id, name, type from credentials_entity"):
        mevcut.setdefault(tip, (cid, ad))

    wf = json.load(open(WF, encoding="utf-8"))

    baglandi, eksik = [], []
    for node in wf["nodes"]:
        tip = ESLEME.get(node["name"])
        if not tip:
            continue
        if tip in mevcut:
            cid, ad = mevcut[tip]
            node["credentials"] = {tip: {"id": cid, "name": ad}}
            baglandi.append(f"{node['name']:20} -> {ad} ({tip})")
        else:
            node.pop("credentials", None)
            eksik.append(f"{node['name']:20} -> {tip} BULUNAMADI")

    # izinli_id argumani verildiyse Ayarlar node'una yaz
    if len(sys.argv) > 1:
        tid = sys.argv[1].strip()
        for node in wf["nodes"]:
            if node["name"] == "Ayarlar":
                node["parameters"]["assignments"]["assignments"][0]["value"] = tid
                print(f"izinli_id ayarlandi: {tid}")

    json.dump(wf, open(WF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n--- baglanan ---")
    for s in baglandi:
        print("  ", s)
    if eksik:
        print("\n--- eksik credential ---")
        for s in eksik:
            print("  ", s)
    print(f"\n{WF} guncellendi.")
    print("Simdi: yayinla.ps1 calistir.")
    return 0 if not eksik else 1


if __name__ == "__main__":
    sys.exit(main())
