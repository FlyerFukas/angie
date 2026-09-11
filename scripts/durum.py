# -*- coding: utf-8 -*-
"""Angie'nin n8n icindeki durumunu ozetler: workflow, tablolar, credential'lar."""
import os
import sqlite3

DB = os.path.join(os.path.expanduser("~"), ".n8n", "database.sqlite")
WF_ID = "angieAsistan0001"


def main():
    if not os.path.exists(DB):
        print("n8n veritabani bulunamadi:", DB)
        return 1

    con = sqlite3.connect(DB)

    satir = con.execute(
        "select name, active from workflow_entity where id=?", (WF_ID,)
    ).fetchone()
    if satir:
        print(f"   workflow : {satir[0]} | aktif: {bool(satir[1])}")
    else:
        print("   workflow : henuz iceri aktarilmamis")

    tablolar = [r[0] for r in con.execute("select name from data_table")]
    print("   tablolar :", ", ".join(tablolar) if tablolar else "yok")

    tipler = sorted({r[0] for r in con.execute("select type from credentials_entity")})
    print("   baglanti :", ", ".join(tipler) if tipler else "yok")

    kanca = con.execute(
        "select count(*) from webhook_entity where workflowId=?", (WF_ID,)
    ).fetchone()[0]
    print("   webhook  :", "kayitli" if kanca else "yok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
