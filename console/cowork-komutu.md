# Cowork / Claude in Chrome'a yapıştır

Chrome'da console.anthropic.com açık ve giriş yapılmış olsun. Sonra şunu yapıştır:

---

Claude Console'da Workbench'i aç ve yeni bir prompt oluştur, adı "Angie".
1. Modeli en güncel Sonnet olarak seç.
2. System Prompt alanına aşağıdaki SISTEM metnini yapıştır; {{SIMDI}} yerine bugünün tarihini, saatini ve gününü yaz.
3. "Add tool" ile aşağıdaki ARACLAR listesindeki 7 aracı tek tek ekle (name, description, input_schema).
4. Kullanıcı mesajı olarak "bugün takvimimde ne var" yaz ve çalıştır.
5. Claude takvim aracını çağırırsa tool result olarak şunu ver:
   [{"summary":"Diş hekimi","start":"2026-10-15T14:00"}]
6. Her adımdan sonra durup ekranda ne gördüğünü bana bir cümleyle söyle. API anahtarı oluşturma, ödeme ayarına dokunma.

SISTEM:
<sistem-mesaji.md içeriği>

ARACLAR:
<araclar.json içeriği>
