# Test senaryoları

| # | Mesaj | Beklenen | Sahte araç sonucu |
|---|---|---|---|
| 1 | bugün takvimimde ne var | `takvim` bugün 00:00–23:59 | `[{"summary":"Diş hekimi","start":"2026-10-15T14:00"}]` |
| 2 | peki ya yarın | `takvim` yarının aralığı (hafıza) | `[]` → "yarın etkinlik yok" |
| 3 | bugünkü maillerimi özetle | `gmail` `newer_than:1d -category:promotions` | 2 mail + 1 reklam; reklam atlanmalı |
| 4 | yarına rapor yazmayı ekle | `gorev_ekle`, son_tarih = yarın | `{"ok":true}` |
| 5 | rapor görevini tamamladım | önce `gorevleri_getir`, sonra `gorev_guncelle` | listede "Rapor yaz" |
| 6 | Mehmet'in numarası ne | `kisileri_getir`; yoksa uydurmamalı | `[]` → "bulamadım" |

Her cevapta kontrol: Türkçe, kısa, yıldız/alt tire/# yok.
