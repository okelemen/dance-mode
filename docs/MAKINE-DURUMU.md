# Makine durumu

Son kontrol: **23 Ağustos 2026**

---

## Donanım

| | |
|---|---|
| CPU | Intel i5-7200U @ 2.50GHz — 2 çekirdek / 4 thread (2017 ultrabook) |
| RAM | 7,7 GB |
| GPU | Intel HD Graphics 620 (dahili) + AMD Radeon R7 M340 (zayıf) |
| OS | Windows 10 Pro 19045 |
| C: | 222,4 GB — **133,6 GB boş** |
| E: | 114,6 GB — **çıkarılabilir sürücü (USB)**, ekonomi kanalı projeleri burada |

---

## Kurulu araçlar — doğrulandı

| Araç | Sürüm |
|---|---|
| Node.js | v24.19.0 LTS |
| npm | 11.17.0 |
| ffmpeg | 9.0 (Gyan build) |
| Python | 3.12.10 |
| git | 2.55.0 |

Kurulacaklar (proje başlayınca, npm üzerinden): Three.js, Puppeteer
(Chromium'u kendi indirir, ~300 MB).

---

## Bu makinede KESİN yapılamayanlar

| | Neden |
|---|---|
| Kendi videondan mocap çıkarma (WHAM, 4D-Humans, lokal Move.ai) | CUDA yok — AMD kart, üstelik çok zayıf |
| 4K render | Yetmez, denenmeyecek |
| 9 dakikalık 1080p render | Teknik olarak mümkün ama saatler sürer; buluta gider |
| Blender ile ciddi iş | Acı verir — pipeline'dan bilinçli olarak çıkarıldı |

## Bu makinede rahatça yapılabilenler

- Three.js sahnesini gerçek zamanlı önizleme (640x360)
- Koreografi, ızgara, JSON yazımı — asıl emek zaten burada, hepsi metin
- ffmpeg ile ses analizi ve zaman esnetme
- Mixamo klip işleme

**Özet: bu makine tasarım makinesidir, render makinesi değildir.**
Ve bu formatta o ayrım kurtarıcı — render tek tuşla devredilebilir bir iştir.

---

## İş bölümü

> **Laptop = tasarım. Bulut = render.**

Render hedefi: **GitHub Actions.** Private repoda ayda 2000 dakika ücretsiz;
bölüm başına 30-60 dk sürer → ayda 20-30 bölüm, sıfır maliyet.

Bunu mümkün kılan şey render'ın deterministik olması: ekran kaydı yok, gerçek zamanlı
GPU bağımlılığı yok, `t = kare_no / fps`. Böyle bir iş headless olarak her yerde koşar.

---

## Yapılan disk temizliği (23 Ağu 2026)

CapCut, `AppData\Local` içinde **143,38 GB** şişmişti. Diskte sadece 5,1 GB boş kalmıştı.

| İşlem | Kazanç |
|---|---|
| `Cache\SmartCrop` silindi | 52,95 GB |
| `Cache\recognize` silindi | 32,96 GB |
| 28 CapCut sürümünün 26'sı silindi (9.2.8.3974 ve 9.1.0.3879 kaldı) | ~42 GB |
| **Toplam** | **128,5 GB** |

**5,1 GB → 133,6 GB.** Taslaklara (`User Data\Projects\com.lveditor.draft`) dokunulmadı.

> **Bakım notu:** CapCut bu cache'i zamanla yeniden şişirir ve eski sürümleri
> hiç temizlemez. Birkaç ayda bir kontrol et.

---

## Proje konumu kararı

`C:\Users\eleme\DANCE-MODE` — **OneDrive dışında, bilinçli tercih.**

Masaüstünde sadece `DANCE-MODE.lnk` kısayolu var.

Neden: `node_modules` on binlerce küçük dosya demek; OneDrive senkronu buna boğulur
ve makine kilitlenir. E: kullanılmıyor çünkü çıkarılabilir sürücü — render sırasında
çıkarılırsa iş çöper.

**Bedeli:** şu an bulut yedeği yok, tek nüsha. GitHub reposu kurulunca çözülecek.
