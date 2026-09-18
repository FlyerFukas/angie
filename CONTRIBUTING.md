# Katkı Rehberi

Katkıya açığım. Ancak bu projenin çift lisans modeli, katkılar konusunda
alışıldık açık kaynak projelerinden **farklı bir kural** gerektiriyor. Bir satır
kod göndermeden önce bunu okuyun.

---

## Neden özel bir kural var

Angie iki lisansla dağıtılıyor: ticari olmayan kullanım için
[PolyForm Noncommercial 1.0.0](LICENSE), işletmeler için ayrı ve ücretli bir
ticari lisans ([COMMERCIAL.md](COMMERCIAL.md)).

Bir yazılımı ticari lisansla satabilmek için **o yazılımın tamamının telif
hakkına sahip olmak** gerekir. Kabul edilen bir katkının telifi katkıda
bulunanda kalırsa, proje sahibi o satırları ticari lisansa dahil edemez ve
model çalışmaz.

Bu, katkınızın değersiz görüldüğü anlamına gelmez. Tam tersi: kodunuzun
satılabilir bir ürünün parçası olmasının yasal önkoşulu.

---

## Katkı Beyanı (DCO benzeri)

Bir pull request açarak aşağıdakileri beyan etmiş olursunuz:

1. Gönderdiğiniz katkı **sizin özgün eserinizdir**; başka bir kaynaktan
   kopyalanmamıştır. Başka bir kaynaktan alınan bir bölüm varsa, kaynağını ve
   lisansını PR açıklamasında belirtirsiniz.
2. Katkınız üzerindeki **mali hakları** (işleme, çoğaltma, yayma, temsil, umuma
   iletim, FSEK m.21-25) proje sahibi **Furkan Akduman**'a devredersiniz; ya da
   bu mümkün değilse, proje sahibine katkı üzerinde **süresiz, geri alınamaz,
   dünya çapında, alt lisans verilebilir ve münhasır olmayan** bir kullanım
   hakkı tanırsınız; **ticari lisanslama dahil.**
3. Bu devrin/iznin karşılığında bir ücret talep etmezsiniz.
4. İşvereniniz varsa ve katkı çalışma saatlerinizde veya işverenin
   ekipmanıyla üretildiyse, bu devri yapmaya yetkili olduğunuzu teyit
   etmiş olursunuz.

Bu beyanı PR açıklamasına şu satırı ekleyerek onaylayın:

```
Katkı Beyanı: CONTRIBUTING.md'deki koşulları okudum ve kabul ediyorum.
```

Bu satırı içermeyen pull request'ler birleştirilmez. Kişisel bir güvensizlik
değil; modelin çalışması için gereken belgedir.

---

## Katkı kabul edilmeyen durumlar

- **Beyan satırı yoksa:** yukarıdaki sebep
- **Kaynağı belirsiz kod:** başka bir projeden alınmış olabilecek, lisansı
  bilinmeyen bölümler
- **Copyleft lisanslı koddan türetilmiş katkı** (GPL, AGPL, LGPL): bu
  lisanslar türev eserin de aynı lisansla dağıtılmasını zorunlu kılar ve
  ticari lisanslamayı imkânsız hâle getirir
- **Yeni bağımlılık ekleyen ve lisansı izin verici olmayan** katkılar
  kopyalanamayan ya da ticari lisanslamayı engelleyen bir bağımlılık,
  katkının tamamını kullanılamaz hâle getirir

---

## Önce konuşalım

Büyük bir değişiklik planlıyorsanız **önce bir issue açın.** Reddedilecek bir
işe emek harcamanızı istemem. Küçük düzeltmeler (yazım hatası, açık bir bug,
belge iyileştirmesi) için doğrudan PR açabilirsiniz.

Özellikle ilgilendiğim katkılar:

- **Yeni araçlar:** Angie'nin çağırabileceği n8n node'ları: not alma
  (Notion, Obsidian), görev yöneticileri, hava durumu, toplu taşıma
- **Sesli mesaj desteği:** transkripsiyon şu an devre dışı; Groq ya da
  Deepgram gibi bir sağlayıcıyla geri getirilebilir
- **Linux ve macOS başlatma scriptleri:** mevcut scriptler yalnızca Windows
  PowerShell için; `scripts/` altına eşdeğerleri
- **Kalıcı tünel seçenekleri:** adresi değişmeyen bir kurulum (Cloudflare
  named tunnel, ngrok sabit alan adı) ya da yalnızca webhook yolunu açan
  ters vekil yapılandırması
- **Başka dillerde sistem talimatı:** Angie'nin Türkçe dışında da
  konuşabilmesi için `uret-angie.py` içindeki `SISTEM` metninin çeşitlemeleri

---

## Teknik beklentiler

- **Türkçe adlandırma.** Değişken, fonksiyon ve node adları Türkçe
  (`izinli_id`, `Gorevleri Getir`, `uret-angie.py`). Kod tabanı bu konuda
  tutarlı.
- **Açıklama neden'i anlatsın.** Ne yaptığı koddan zaten okunuyor. Yorumlar
  *neden öyle yapıldığını* ve hangi tuzağı önlediğini anlatmalı. Bu projede
  yorumların çoğu n8n'in belgelenmemiş bir davranışını açıklıyor.
- **Workflow JSON'unu elle düzenlemeyin.** `workflows/01-angie.json` üretilen
  bir çıktıdır ve git'e girmez. Değişiklik `scripts/uret-angie.py` içinde
  yapılır; PR'da üreticiyi değiştirin.
- **Üretici çalışsın.** PR'dan önce çalıştırın:
  ```
  py scripts/uret-angie.py
  ```
  Çıktıda eksik hedef ve eksik kaynak `yok` dönmeli.
- **Kişisel veri sızdırmayın.** Telegram kimliği, e-posta adresi ve makine
  yolları koda yazılmaz; ortam değişkeninden okunur. PR'ınızda bunlardan biri
  sabit yazılıysa birleştirilmez.
- **Yeni bağımlılık eklemeyin:** gerekiyorsa önce issue açın. Mevcut kurulum
  yalnızca n8n ve cloudflared'e dayanıyor, bu bilinçli bir tercih.

---

## Katkıda bulunanlar

Kabul edilen katkılar, birleştirildikleri sürümün notlarında ve deponun
katkıda bulunanlar listesinde adınızla anılır. Telif devri, emeğin görünmez
olması anlamına gelmez.
