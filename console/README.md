# Angie'nin beyni, Claude Console'da

n8n'e dokunmadan Angie'nin davranışını (sistem mesajı + 7 araç) Console
Workbench'te test etmek için. Prompt'u burada sağlamlaştır, sonra
`scripts/uret-angie.py` içindeki `SISTEM`'e taşı.

| Dosya | Ne işe yarar |
|---|---|
| `sistem-mesaji.md` | Workbench'te System Prompt alanına yapıştırılır |
| `araclar.json` | Her eleman Workbench'te "Add tool" ile tek tek eklenir |
| `cowork-komutu.md` | Chrome'daki Claude'a (Cowork) yapıştırılacak hazır görev |
| `test-senaryolari.md` | Sırayla denenecek 6 mesaj ve beklenen davranış |

## Adımlar

1. **Workbench aç** → console.anthropic.com → Workbench → yeni prompt.
   *Neden:* n8n'i başlatıp yayınlamadan saniyeler içinde deneme yapmak.
2. **Model seç** → n8n'dekiyle aynı Sonnet modeli.
   *Neden:* Testte gördüğün davranış Telegram'dakiyle birebir olsun.
3. **System Prompt** → `sistem-mesaji.md`, `{{SIMDI}}` değişkenine
   örn. `15.10.2026 09:00, Perşembe` yaz.
4. **Araçları ekle** → `araclar.json` içindeki 7 aracı ekle.
5. **Çalıştır** → `test-senaryolari.md` mesajlarını sırayla gönder. Claude
   bir araç çağırınca sahte sonucu sen yazarsın (tool result).
   *Neden:* Hangi aracı, hangi parametreyle çağırdığını net görmek.
6. **Düzelt ve kaydet** → beğenmediğin cevapta kuralı düzelt, tekrar çalıştır.
   Bitince prompt'u kaydet, `uret-angie.py` → `yayinla.ps1`.
