# Angie (Türkçe)

**Telegram'da yaşayan Türkçe kişisel asistan.** Takviminde ne olduğunu sor,
maillerini özetlet, görev ekle, bir telefon numarası bul — hepsi düz Türkçe,
telefonundan. Kendi bilgisayarında bir n8n workflow'u olarak çalışır, düşünme
işini Claude yapar.

> English version: [README.md](README.md)

---

## Ne yapıyor

Kendi Telegram botuna mesaj atarsın, Angie Türkçe cevaplar; soru gerçek veri
gerektiriyorsa ilgili aracı çağırır:

| Sen yazarsın | Angie şunu kullanır |
|---|---|
| bugün takvimimde ne var | Google Takvim |
| bugünkü maillerimi özetle | Gmail, reklam mailleri elenir |
| görevlerim neler | görev tablosu |
| yarına rapor yazmayı ekle | görev tablosu, ekleme |
| rapor görevini tamamladım | görev tablosu, güncelleme |
| Mehmet'in numarası ne | kişi tablosu |

Son 15 mesajı hatırlar, yani *peki ya yarın* gibi devam soruları çalışır.

## Nasıl çalışıyor

```
Telegram  ──►  cloudflared tüneli  ──►  n8n (localhost:5678)
                                          │
                                    kimlik kilidi
                                          │
                                      Claude ajanı
                        ┌─────────────┬───┴────┬─────────────┐
                    görevler       kişiler   takvim        gmail
                  (n8n data table)          (Google OAuth)
                                          │
Telegram  ◄───────────  cevap, 4096 karakterlik parçalara bölünür
```

Model çağrısı ve Google API'leri dışında her şey senin makinende kalır.
Görevler ve kişiler n8n'in kendi data table'larında durur — harici veritabanı,
Airtable ya da Baserow hesabı gerekmez.

## Gerekenler

- Windows, Node.js 20+ ve Python 3.10+
- [@BotFather](https://t.me/BotFather) üzerinden alınmış bir Telegram bot token'ı
- Anthropic API anahtarı
- Takvim ve mail istiyorsan bir Google Cloud OAuth istemcisi

## Kurulum

```bash
git clone https://github.com/FlyerFukas/angie.git
cd angie
npm install n8n@2.30.7
```

Tünel programını `bin/` içine indir:

```powershell
Invoke-WebRequest https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -OutFile bin\cloudflared.exe
```

Üreticiye kim olduğunu söyle, workflow'u üret:

```powershell
setx ANGIE_TAKVIM_ID "kendi.adresin@gmail.com"
py scripts\uret-angie.py
py scripts\uret-workflow.py
```

Her şeyi başlat, `http://localhost:5678` adresini aç:

```
Angie-Baslat.cmd
```

n8n arayüzünde dört bağlantı ekle: Telegram API, Anthropic API, Google Calendar
OAuth2, Gmail OAuth2. Google tarafında OAuth istemcisine şu yönlendirme adresini
birebir ekle:

```
http://localhost:5678/rest/oauth2-credential/callback
```

Sonra bağlantıları node'lara eşle ve yayına al:

```powershell
py scripts\baglantilari-kur.py
.\scripts\yayinla.ps1
```

Botuna bir mesaj at. Sana Telegram kimliğini söyleyecek. Botu o kimliğe kilitle:

```powershell
py scripts\baglantilari-kur.py 123456789
.\scripts\yayinla.ps1
```

## Bu proje neyi belgeliyor

Angie, n8n'in
[Angie, Personal AI Assistant with Telegram Voice and Text](https://n8n.io/workflows/2462-angie-personal-ai-assistant-with-telegram-voice-and-text/)
şablonundan yola çıktı. Ama o şablon eski bir n8n sürümü için yazılmış ve 2.x
üzerinde birkaç yerde çalışmıyor. Düzeltmeler ve arkalarındaki n8n davranışları
burada yazılı, çünkü bulmaları gerçekten saat aldı:

1. **`n8n start --tunnel` 2.x'te kaldırılmış.** Bayrak artık yok, Telegram
   webhook'u için harici tünel şart.
2. **Aktivasyon artık `publish:workflow` ve yeniden başlatma.** Tek başına
   `workflow_entity.active = 1` hiçbir şey yapmıyor.
3. **`import:workflow` yayındaki workflow'u pasifleştiriyor.** Import'tan sonra
   mutlaka tekrar yayınla.
4. **İçeri aktarılan JSON'da `id` alanı zorunlu**, yoksa SQLite NOT NULL
   kısıtıyla reddediyor.
5. **Webhook kaydı başlangıçtan 10–30 saniye sonra oluşuyor.** `/healthz` 200
   dönmesi webhook adresinin cevap verdiği anlamına gelmiyor.
6. **CLI komutları çalışan n8n ile çakışıyor** (task broker portu 5679).
   `N8N_RUNNERS_BROKER_PORT=5680` ile çalıştır.
7. **`N8N_EDITOR_BASE_URL` OAuth callback'ini sabitliyor.** Localhost'a
   ayarlarsan değişen tünel adresi Google girişini bozmuyor.
8. **Telegram node'u `parse_mode` boşsa zorla Markdown ekliyor.**
   `GenericFunctions.js` içinde sessizce `Markdown` atanıyor; bu yüzden bir
   değişken adındaki tek bir alt çizgi bile mesajın tamamının
   `can't parse entities` ile reddedilmesine yol açıyor. Angie HTML'e sabitliyor
   ve model çıktısını kaçırıyor.
9. **Takvim alanı e-posta biçiminde kimlik dayatıyor.** Google `primary`
   değerini kabul ediyor, n8n'in regex doğrulaması etmiyor ve
   `Calendar parameter's value is invalid` hatası veriyor.
10. **`export:nodes` sürümleri yanıltıcı raporluyor.** Gerçek en yüksek sürüm,
    node'un derlenmiş kaynağındaki `nodeVersions` bloğunda.

Şablondan taşınan düzeltmeler: oturum anahtarı sabit yazılmıştı, bu yüzden tüm
konuşmalar tek hafızayı paylaşıyordu; sesli mesaj yolunda oturum kimliği
kayboluyordu; 4096 karakterden uzun cevaplar reddediliyordu; fotoğraf
gönderilince ses kontrolü çöküyordu.

## Dosya düzeni

```
Angie/
├── Angie-Baslat.cmd          tünel + n8n başlatır
├── Angie-Durdur.cmd          ikisini de durdurur
├── scripts/
│   ├── uret-angie.py         workflow'u üretir (JSON'u değil bunu düzenle)
│   ├── baglantilari-kur.py   n8n bağlantılarını node'lara eşler, kilidi yazar
│   ├── angie-baslat.ps1      tünel + n8n başlatıcı
│   ├── yayinla.ps1           içeri aktar, yayınla, yeniden başlat
│   └── durum.py              mevcut durumu yazdırır
└── workflows/                üretilen çıktı, git'e girmez
```

Workflow JSON'u bir çıktı dosyası. `scripts/uret-angie.py` içinde değiştir,
çalıştır, sonra `yayinla.ps1` çalıştır — JSON'u elle düzenlersen üzerine yazılır.

## Sınırlar

- Angie yalnızca bilgisayarın açıkken ve tünel çalışırken cevap verir.
- Cloudflare hızlı tünelleri her başlangıçta yeni adres alır. n8n webhook'u
  kendisi yeniden kaydettiği için bu sorun olmuyor, ama uzun vadeli üretim
  kullanımı için tasarlanmış bir yöntem değil.
- Sesli mesaj bu sürümde bağlı değil. Orijinal şablon OpenAI Whisper
  kullanıyordu; Angie Claude üzerinde çalıştığı için transkripsiyon ayrı bir
  sağlayıcı gerektirir.
- Bazı kurumsal ve kampüs ağları `api.telegram.org` adresini tamamen engelliyor.
  Aktivasyon sertifika hatasıyla başarısız olursa önce ağa bak, koda değil.

## Güvenlik

Anahtarlar bu depoya hiç girmiyor — nerede durdukları, tünelin neyi açtığı ve
kimlik kilidinin nasıl çalıştığı için [SECURITY.md](SECURITY.md) dosyasına bak.

## Lisans

MIT — [LICENSE](LICENSE) dosyasına bak.
