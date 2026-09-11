# -*- coding: utf-8 -*-
"""Angie workflow'larini uretir (n8n 2.30.7 node semalarina gore)."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workflows")
TRIG = "Telegram Mesaji"

def rl(mode, value):
    return {"__rl": True, "mode": mode, "value": value}

# ---------------------------------------------------------------- kurulum
kurulum = {
    "id": "angieSetupTbl001",
    "name": "Angie Kurulum - Tablolar",
    "nodes": [
        {"id": "s0000000-0000-4000-8000-000000000001", "name": "Kurulum Webhook",
         "type": "n8n-nodes-base.webhook", "typeVersion": 2.1, "position": [0, 0],
         "webhookId": "s0000000-0000-4000-8000-0000000000ff",
         "parameters": {"path": "angie-kurulum", "responseMode": "lastNode", "options": {}}},

        {"id": "s0000000-0000-4000-8000-000000000002", "name": "Eski Gorevleri Sil",
         "type": "n8n-nodes-base.dataTable", "typeVersion": 1.1, "position": [220, 0],
         "onError": "continueRegularOutput",
         "parameters": {"resource": "table", "operation": "delete",
                        "dataTableId": rl("name", "Gorevler"), "options": {}}},

        {"id": "s0000000-0000-4000-8000-000000000003", "name": "Gorevler Tablosu",
         "type": "n8n-nodes-base.dataTable", "typeVersion": 1.1, "position": [440, 0],
         "onError": "continueRegularOutput",
         "parameters": {"resource": "table", "operation": "create", "tableName": "Gorevler",
                        "columns": {"column": [
                            {"name": "baslik", "type": "string"},
                            {"name": "durum", "type": "string"},
                            {"name": "oncelik", "type": "string"},
                            {"name": "son_tarih", "type": "string"},
                            {"name": "notlar", "type": "string"}]},
                        "options": {}}},

        {"id": "s0000000-0000-4000-8000-000000000004", "name": "Kisiler Tablosu",
         "type": "n8n-nodes-base.dataTable", "typeVersion": 1.1, "position": [660, 0],
         "onError": "continueRegularOutput",
         "parameters": {"resource": "table", "operation": "create", "tableName": "Kisiler",
                        "columns": {"column": [
                            {"name": "ad", "type": "string"},
                            {"name": "eposta", "type": "string"},
                            {"name": "telefon", "type": "string"},
                            {"name": "kurum", "type": "string"},
                            {"name": "notlar", "type": "string"}]},
                        "options": {}}},

        {"id": "s0000000-0000-4000-8000-000000000005", "name": "Tablolari Listele",
         "type": "n8n-nodes-base.dataTable", "typeVersion": 1.1, "position": [880, 0],
         "parameters": {"resource": "table", "operation": "list", "returnAll": True, "options": {}}},
    ],
    "connections": {
        "Kurulum Webhook":    {"main": [[{"node": "Eski Gorevleri Sil", "type": "main", "index": 0}]]},
        "Eski Gorevleri Sil": {"main": [[{"node": "Gorevler Tablosu",   "type": "main", "index": 0}]]},
        "Gorevler Tablosu":   {"main": [[{"node": "Kisiler Tablosu",    "type": "main", "index": 0}]]},
        "Kisiler Tablosu":    {"main": [[{"node": "Tablolari Listele",  "type": "main", "index": 0}]]},
    },
    "settings": {"executionOrder": "v1"},
}

with open(os.path.join(OUT, "00-kurulum-tablolar.json"), "w", encoding="utf-8") as f:
    json.dump(kurulum, f, ensure_ascii=False, indent=2)
print("yazildi: 00-kurulum-tablolar.json")
