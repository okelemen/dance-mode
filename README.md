# DANCE MODE

Prosedürel render edilen neon ritim-oyunu / warm-up videoları üreten **ayrı** bir
YouTube kanalı projesi. Ekonomi kanalıyla (`E:\YouTube-Kanal`) hiçbir ilgisi yoktur.

> ## DURUM: Suno üyeliği bekleniyor
> 23 Ağustos 2026 itibarıyla ödeme yapılamadı. Üyelik alınana kadar bu projede
> ilerleme yok. Üyelik gelince → `DANCE-MODE-PLANI.md` içindeki
> **"BURADAN DEVAM ET"** listesinden başla.

---

## Ne nerede

| Yol | İçerik |
|---|---|
| `DANCE-MODE-PLANI.md` | **Ana doküman.** Format analizi, tasarım kararları ve gerekçeleri, iskelet, pipeline, maliyet. Önce bunu oku. |
| `docs/SUNO-BRIEF.md` | Suno başındayken açık tutulacak sayfa. Promptlar ve ayarlar. |
| `docs/MIXAMO-HAREKET-LISTESI.md` | İndirilecek 12 hareket + Mixamo arama terimleri + seçim kuralları. |
| `docs/MAKINE-DURUMU.md` | Donanım, kurulu araçlar, bu makinede yapılamayanlar. |
| `docs/KAYNAK-KANAL.md` | Referans kanalın ölçülen verileri ve çıkarılan kalıplar. |
| `spec/sabitler.json` | Izgara sabitleri, makine okunur. Motor buradan besleniyor. |
| `spec/cue-tipleri.md` | Cue tiplerinin tanımı ve hareket eşlemesi. |
| `spec/bolum-sablonu.json` | Bir bölümün nasıl yazıldığını gösteren örnek. |
| `01-muzik/` | Suno WAV dosyaları buraya iner. |
| `02-hareketler/` | Mixamo FBX dosyaları buraya iner. |
| `03-motor/` | Three.js render motoru. Henüz yazılmadı. |
| `04-ciktilar/` | Render edilmiş mp4 ve kapaklar. |

---

## Üç cümlelik özet

Ekranda çekilmiş tek bir kare yok; her şey kodla çiziliyor. Müzik sabit **120 BPM**
olduğu için 30 fps'te her vuruş tam **15 kareye** oturuyor ve koreografi zamanda değil
**ölçü numarasında** yazılıyor. Motor bir kere yazılıyor, sonrasında yeni bölüm =
yeni bir JSON dosyası.

---

## Fazlar

| Faz | Kapsam | Durum |
|---|---|---|
| **1** | Tepki hareketleri (adım, zıpla, çömel, kaç, yumruk) + motor + ilk bölüm | **Aktif.** 11 klip hazır. |
| **2** | Takip hareketleri (dans + mobilite), üst vücut cue dili | Klipler indi (10 adet), kullanımı bekliyor |
| **3** | İleri cue tipleri (hold, double, mirror, half tempo) | Sonra |

**Kütüphane tamam: 21 klip.** Ama motor önce sadece Faz 1 üstüne kurulacak —
dar bir setle çalışan bir şey çıkarmadan genişletmenin faydası yok.
Faz 2 klipleri indirilmiş halde bekliyor, kaybolma riski yok.

## Değişmeyen kurallar

1. **120 BPM / 30 fps / 1080p.** Tartışmaya kapalı, gerekçesi planda.
2. **Kesme yok.** Tek, kesintisiz kamera.
3. **Tünel hızı sabit.** Ortada değişmez.
4. **Nota vuruştan tam 1 ölçü (2 sn) önce doğar.**
5. **Her hareket nötr duruşta başlar, nötr duruşta biter.**
6. **Beat tespiti yok.** Izgara bizim, müzik ona uyduruluyor.
7. **Render bu makinede yapılmaz**, GitHub Actions'a gider.

---

## Uyarı: yedek yok

Bu klasör OneDrive dışında (bilinçli tercih — `node_modules` senkronu felaket olur).
Şu an **tek nüsha**. GitHub reposu kurulana kadar aklında olsun.
