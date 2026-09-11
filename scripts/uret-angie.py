# -*- coding: utf-8 -*-
"""Angie ana workflow'unu uretir (n8n 2.30.7 node semalarina gore dogrulanmis)."""
import json, os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(KOK, "workflows")
TRIG = "Telegram Mesaji"

# --- kisiye ozel ayarlar (ortam degiskeninden) -------------------------------
# Bunlar bilerek kod icine yazilmiyor: depo herkese acik.
#
#   setx ANGIE_TAKVIM_ID  "kendi.adresin@gmail.com"
#   setx ANGIE_TELEGRAM_ID "123456789"
#
# TAKVIM_ID: Google Takvim kimligi. Birincil takvimin kimligi hesabinin
#   e-posta adresidir. n8n'in takvim alani e-posta formati dayatir; Google
#   API'nin kabul ettigi "primary" kisayolu burada gecmez.
# TELEGRAM_ID: sadece bu kullanici Angie ile konusabilir. Bos birakirsan
#   bot ilk mesajinda sana kendi ID'ni soyler.
TAKVIM_ID = os.environ.get("ANGIE_TAKVIM_ID", "eposta-adresin@gmail.com")
IZINLI_ID = os.environ.get("ANGIE_TELEGRAM_ID", "")


def rl(mode, value):
    return {"__rl": True, "mode": mode, "value": value}


def kosul(cid, tip, islem, sol, sag="", tekli=True):
    op = {"type": tip, "operation": islem}
    if tekli:
        op["singleValue"] = True
    return {"id": cid, "operator": op, "leftValue": sol, "rightValue": sag}


def if_params(kosullar):
    return {
        "options": {},
        "looseTypeValidation": True,
        "conditions": {
            "options": {"version": 3, "leftValue": "", "caseSensitive": True,
                        "typeValidation": "loose"},
            "combinator": "and",
            "conditions": kosullar,
        },
    }


def fai(anahtar, aciklama):
    return "={{ $fromAI('%s', '%s', 'string') }}" % (anahtar, aciklama)


def ref(alan):
    return "={{ $('%s').first().json.message.%s }}" % (TRIG, alan)


SISTEM = (
    "=Sen Angie'sin, Furkan'in kisisel asistanisin. Her zaman Turkce konusursun.\n\n"
    "Su an: {{ $now.setZone('Europe/Istanbul').setLocale('tr').toFormat('dd.MM.yyyy HH:mm') }} "
    "(Istanbul saati), bugun {{ $now.setZone('Europe/Istanbul').setLocale('tr').toFormat('cccc') }}.\n\n"
    "Kurallar:\n"
    "- Kisa ve net cevap ver; mesajin Telegram'da okunacak.\n"
    "- Bicimlendirme isareti kullanma (yildiz, alt tire, # gibi). Duz metin yaz.\n"
    "- Kullanici tarih belirtmezse bugunu kastettigini varsay.\n"
    "- Takvim sorularinda sadece sorulan araliktaki etkinlikleri soyle; bir haftadan uzak "
    "gelecekteki etkinlikleri sorulmadikca ekleme.\n"
    "- Mail ozetlerken her mail icin gonderen, tarih, konu ve tek cumlelik ozet ver. "
    "Tanitim ve reklam maillerini atla.\n"
    "- Gorev ve kisi bilgilerini hafizandan uydurma, ilgili araci cagir.\n"
    "- Bilmedigin bir seyi bilmiyorum de.\n"
)

BOL_KODU = """// Telegram tek mesajda 4096 karakter kabul eder; uzun cevabi parcalara ayir.
//
// ONEMLI: n8n'in Telegram node'u parse_mode verilmezse ZORLA 'Markdown' ekliyor
// (n8n-nodes-base/dist/nodes/Telegram/GenericFunctions.js icinde
// addAdditionalFields: if (!additionalFields.parse_mode) parse_mode='Markdown').
// Duz metin gondermek mumkun degil. Modelin cevabinda tek bir _ veya *
// gecerse Telegram "can't parse entities" deyip mesaji komple reddediyor.
// Bu yuzden node'larda parse_mode HTML'e sabitlendi ve metni burada kaciriyoruz.
// HTML modunda _ * # guvenli; sadece & < > kacirilmali.
const MAX = 3000;
const kacir = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const cikti = [];
for (const item of $input.all()) {
  let metin = String(item.json.output ?? '').trim();
  if (!metin) metin = 'Bir cevap uretemedim, tekrar dener misin?';
  // Once bol, sonra her parcayi kacir: boylece bir HTML entity ortadan bolunmez.
  for (let i = 0; i < metin.length; i += MAX) {
    cikti.push({ json: { parca: kacir(metin.slice(i, i + MAX)) } });
  }
}
return cikti;"""


def dt_tool(nid, ad, poz, aciklama, islem, tablo, ekstra):
    p = {"descriptionType": "manual", "toolDescription": aciklama,
         "resource": "row", "operation": islem, "dataTableId": rl("name", tablo)}
    p.update(ekstra)
    return {"id": nid, "name": ad, "type": "n8n-nodes-base.dataTableTool",
            "typeVersion": 1.1, "position": poz, "parameters": p}


nodes = [
    # ---------------- giris ----------------
    {"id": "a0000000-0000-4000-8000-000000000001", "name": TRIG,
     "type": "n8n-nodes-base.telegramTrigger", "typeVersion": 1.4, "position": [-220, 300],
     "webhookId": "a0000000-0000-4000-8000-0000000000f1",
     "parameters": {"updates": ["message"], "additionalFields": {}}},

    {"id": "a0000000-0000-4000-8000-000000000002", "name": "Ayarlar",
     "type": "n8n-nodes-base.set", "typeVersion": 3.4, "position": [0, 300],
     "notes": "izinli_id: sadece bu Telegram kullanici ID'si Angie ile konusabilir. Bos birakirsan bot sana ID'ni soyler.",
     "notesInFlow": True,
     "parameters": {
         "includeOtherFields": True,
         "options": {},
         "assignments": {"assignments": [
             {"id": "izin-1", "name": "izinli_id", "type": "string", "value": IZINLI_ID}]}}},

    {"id": "a0000000-0000-4000-8000-000000000003", "name": "Kimlik Ayarli mi",
     "type": "n8n-nodes-base.if", "typeVersion": 2.3, "position": [220, 300],
     "parameters": if_params([kosul("k-bos", "string", "empty", "={{ $json.izinli_id }}")])},

    {"id": "a0000000-0000-4000-8000-000000000004", "name": "Kimlik Bildir",
     "type": "n8n-nodes-base.telegram", "typeVersion": 1.2, "position": [440, 460],
     "webhookId": "a0000000-0000-4000-8000-0000000000f2",
     "parameters": {
         "resource": "message", "operation": "sendMessage",
         "chatId": ref("chat.id"),
         "text": ("=Merhaba! Henuz izinli kullanici ayarlanmamis.\n\n"
                  "Senin Telegram ID'in: {{ $('" + TRIG + "').first().json.message.from.id }}\n\n"
                  "n8n'de Angie workflow'unu ac, Ayarlar node'undaki izinli_id alanina bu "
                  "numarayi yaz, kaydet ve yeniden yayinla. Sonra tekrar yaz."),
         "additionalFields": {"appendAttribution": False, "parse_mode": "HTML"}}},

    {"id": "a0000000-0000-4000-8000-000000000005", "name": "Izinli mi",
     "type": "n8n-nodes-base.if", "typeVersion": 2.3, "position": [440, 200],
     "parameters": if_params([kosul(
         "k-esit", "string", "equals",
         ref("from.id"), "={{ $json.izinli_id }}", tekli=False)])},

    {"id": "a0000000-0000-4000-8000-000000000009", "name": "Metin var mi",
     "type": "n8n-nodes-base.if", "typeVersion": 2.3, "position": [660, 200],
     "parameters": if_params([kosul("k-metin", "string", "notEmpty", ref("text"))])},

    {"id": "a0000000-0000-4000-8000-00000000000a", "name": "Desteklenmiyor",
     "type": "n8n-nodes-base.telegram", "typeVersion": 1.2, "position": [1100, 440],
     "webhookId": "a0000000-0000-4000-8000-0000000000f4",
     "parameters": {
         "resource": "message", "operation": "sendMessage",
         "chatId": ref("chat.id"),
         "text": "=Bu mesaj turunu anlayamiyorum. Bana sadece yazili mesaj gonderebilirsin.",
         "additionalFields": {"appendAttribution": False, "parse_mode": "HTML"}}},

    # ---------------- ajan ----------------
    {"id": "a0000000-0000-4000-8000-00000000000b", "name": "Angie",
     "type": "@n8n/n8n-nodes-langchain.agent", "typeVersion": 3.1, "position": [1360, 220],
     "parameters": {
         "promptType": "define",
         "text": "={{ $('" + TRIG + "').first().json.message.text }}",
         "options": {"systemMessage": SISTEM, "maxIterations": 10}}},

    {"id": "a0000000-0000-4000-8000-00000000000c", "name": "Anthropic Modeli",
     "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic", "typeVersion": 1.5, "position": [1140, 520],
     "parameters": {"model": {"__rl": True, "mode": "list", "value": "claude-sonnet-5",
                               "cachedResultName": "Claude Sonnet 5"}, "options": {}}},

    {"id": "a0000000-0000-4000-8000-00000000000d", "name": "Hafiza",
     "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "typeVersion": 1.4,
     "position": [1280, 520],
     "parameters": {"sessionIdType": "customKey",
                    "sessionKey": ref("from.id"),
                    "contextWindowLength": 15}},

    # ---------------- araclar ----------------
    dt_tool("a0000000-0000-4000-8000-00000000000e", "Gorevleri Getir", [1420, 520],
            "Kullanicinin gorev listesindeki tum gorevleri getirir. Gorevlerle ilgili her soruda once bunu cagir.",
            "get", "Gorevler",
            {"returnAll": True, "matchType": "anyCondition", "filters": {}, "options": {}}),

    dt_tool("a0000000-0000-4000-8000-00000000000f", "Gorev Ekle", [1560, 520],
            "Gorev listesine yeni bir gorev ekler. durum alanina bekliyor yaz. son_tarih varsa YYYY-MM-DD formatinda yaz, yoksa bos birak.",
            "insert", "Gorevler",
            {"columns": {"mappingMode": "defineBelow", "matchingColumns": [], "schema": [],
                         "value": {
                             "baslik": fai("baslik", "Gorevin kisa basligi"),
                             "durum": fai("durum", "Gorev durumu: bekliyor veya tamamlandi"),
                             "oncelik": fai("oncelik", "Oncelik: dusuk, orta veya yuksek"),
                             "son_tarih": fai("son_tarih", "Son tarih YYYY-MM-DD formatinda, yoksa bos birak"),
                             "notlar": fai("notlar", "Varsa ek not, yoksa bos birak")}},
             "options": {}}),

    dt_tool("a0000000-0000-4000-8000-000000000010", "Gorev Guncelle", [1700, 520],
            "Var olan bir gorevi basligina gore bulup durumunu gunceller. Ornegin gorev tamamlandiginda kullan. Once Gorevleri Getir ile tam basligi ogren.",
            "update", "Gorevler",
            {"matchType": "allConditions",
             "filters": {"conditions": [{"keyName": "baslik", "condition": "eq",
                                         "keyValue": fai("baslik", "Guncellenecek gorevin tam basligi")}]},
             "columns": {"mappingMode": "defineBelow", "matchingColumns": [], "schema": [],
                         "value": {"durum": fai("durum", "Yeni durum: bekliyor veya tamamlandi")}},
             "options": {}}),

    dt_tool("a0000000-0000-4000-8000-000000000011", "Kisileri Getir", [1840, 520],
            "Kayitli kisilerin iletisim bilgilerini (e-posta, telefon, kurum) getirir.",
            "get", "Kisiler",
            {"returnAll": True, "matchType": "anyCondition", "filters": {}, "options": {}}),

    dt_tool("a0000000-0000-4000-8000-000000000012", "Kisi Ekle", [1980, 520],
            "Kisi rehberine yeni bir kisi ekler.",
            "insert", "Kisiler",
            {"columns": {"mappingMode": "defineBelow", "matchingColumns": [], "schema": [],
                         "value": {
                             "ad": fai("ad", "Kisinin adi soyadi"),
                             "eposta": fai("eposta", "E-posta adresi, yoksa bos birak"),
                             "telefon": fai("telefon", "Telefon numarasi, yoksa bos birak"),
                             "kurum": fai("kurum", "Calistigi kurum, yoksa bos birak"),
                             "notlar": fai("notlar", "Ek not, yoksa bos birak")}},
             "options": {}}),

    {"id": "a0000000-0000-4000-8000-000000000013", "name": "Takvim",
     "type": "n8n-nodes-base.googleCalendarTool", "typeVersion": 1.3, "position": [2120, 520],
     "parameters": {
         "descriptionType": "manual",
         "toolDescription": "Google Takvim etkinliklerini belirtilen tarih araliginda getirir. Baslangic ve bitis zamanini ISO 8601 formatinda ver.",
         "resource": "event", "operation": "getAll",
         "calendar": rl("id", TAKVIM_ID),
         "returnAll": False, "limit": 25,
         "timeMin": fai("baslangic", "Baslangic zamani ISO 8601: YYYY-MM-DDTHH:mm:ss"),
         "timeMax": fai("bitis", "Bitis zamani ISO 8601: YYYY-MM-DDTHH:mm:ss"),
         "options": {"singleEvents": True, "orderBy": "startTime", "timeZone": "Europe/Istanbul",
                     "fields": "items(summary,start,end,location)"}}},

    {"id": "a0000000-0000-4000-8000-000000000014", "name": "Gmail",
     "type": "n8n-nodes-base.gmailTool", "typeVersion": 2.2, "position": [2260, 520],
     "webhookId": "a0000000-0000-4000-8000-0000000000f5",
     "parameters": {
         "descriptionType": "manual",
         "toolDescription": "Gmail kutusundaki mailleri getirir. Gmail arama sorgusu kullanir, ornek: newer_than:1d -category:promotions",
         "resource": "message", "operation": "getAll",
         "returnAll": False, "limit": 15,
         "simple": True,
         "filters": {"q": fai("arama", "Gmail arama sorgusu, ornek: newer_than:1d -category:promotions")},
         "options": {}}},

    # ---------------- cikis ----------------
    {"id": "a0000000-0000-4000-8000-000000000015", "name": "Cevabi Bol",
     "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1600, 220],
     "parameters": {"jsCode": BOL_KODU}},

    {"id": "a0000000-0000-4000-8000-000000000016", "name": "Telegram Cevap",
     "type": "n8n-nodes-base.telegram", "typeVersion": 1.2, "position": [1820, 220],
     "webhookId": "a0000000-0000-4000-8000-0000000000f6",
     "parameters": {
         "resource": "message", "operation": "sendMessage",
         "chatId": ref("chat.id"),
         "text": "={{ $json.parca }}",
         "additionalFields": {"appendAttribution": False, "parse_mode": "HTML"}}},
]


def m(hedef, idx=0):
    return [{"node": hedef, "type": "main", "index": idx}]


connections = {
    TRIG:                 {"main": [m("Ayarlar")]},
    "Ayarlar":            {"main": [m("Kimlik Ayarli mi")]},
    "Kimlik Ayarli mi":   {"main": [m("Kimlik Bildir"), m("Izinli mi")]},
    "Izinli mi":          {"main": [m("Metin var mi"), []]},
    "Metin var mi":       {"main": [m("Angie"), m("Desteklenmiyor")]},
    "Angie":              {"main": [m("Cevabi Bol")]},
    "Cevabi Bol":         {"main": [m("Telegram Cevap")]},
    "Anthropic Modeli":   {"ai_languageModel": [[{"node": "Angie", "type": "ai_languageModel", "index": 0}]]},
    "Hafiza":             {"ai_memory":        [[{"node": "Angie", "type": "ai_memory", "index": 0}]]},
}
for arac in ["Gorevleri Getir", "Gorev Ekle", "Gorev Guncelle", "Kisileri Getir",
             "Kisi Ekle", "Takvim", "Gmail"]:
    connections[arac] = {"ai_tool": [[{"node": "Angie", "type": "ai_tool", "index": 0}]]}

wf = {
    "id": "angieAsistan0001",
    "name": "Angie - Kisisel Asistan",
    "nodes": nodes,
    "connections": connections,
    "settings": {"executionOrder": "v1", "timezone": "Europe/Istanbul",
                 "saveManualExecutions": True},
}

with open(os.path.join(OUT, "01-angie.json"), "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

adlar = {n["name"] for n in nodes}
eksik = [h["node"] for v in connections.values() for lst in v.values()
         for grp in lst for h in grp if h["node"] not in adlar]
kaynak_eksik = [k for k in connections if k not in adlar]
print("yazildi: 01-angie.json")
print("  node sayisi      :", len(nodes))
print("  eksik hedef      :", eksik or "yok")
print("  eksik kaynak     :", kaynak_eksik or "yok")
print("  arac sayisi      :", sum(1 for k, v in connections.items() if "ai_tool" in v))
