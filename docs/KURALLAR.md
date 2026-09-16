# KURALLAR — her bölümde geçerli, tartışmaya kapalı

Bu dosya kullanıcı kararlarının tutanağı. Bir kural burada yazıyorsa, aksi
yazılı olarak söylenene kadar geçerlidir.

---

## 1. SÜRE — "tam render" ne demek

**Bir bölüm 9,5–10,5 dakika (570–630 sn) olur.**

**"Tam render al" demek = 9,5–10,5 dakikalık BÖLÜM render et demek.**
Elde kısa bir önizleme bölüm dosyası olması bunu değiştirmez: önce iskelet tam
süreye çıkarılır, sonra render alınır.

Ölçü hesabı:

    olcu = saniye / ((60 / BPM) * 4)

| BPM | Ölçü | Süre | |
|---|---|---|---|
| 132,500 | 336 | 608,6 sn = 10:08,6 | ✔ |
| 135,961 | 330 | 582,5 sn = 9:42,5 | ✔ |
| 132,500 | 64 | 115,9 sn = 1:55,9 | ✘ önizleme |

**Geçmiş hata (15 Eyl 2026):** 64 ölçülük `onizleme-elma.json` "tam render"
sanılıp 1:55 olarak çıkarıldı ve yüklenecekler klasörüne kondu. Kullanıcı
reddetti, dosya silindi. Tekrarlamaması için bu madde yazıldı.

## 2. İSKELET UZARKEN NE DEĞİŞİR

Bölüm uzarken **blok UZUNLUĞU değil SAYISI artar.**

- Öğretme bölümü: giriş nefesi + her hareket için bir kademe (8'er ölçü).
- Gövde: 16'lık çalışma blokları + 8'lik molalar.
- Dizilim: (3 çalışma + 1 mola) × N, sonda bir mola.
- Zorluk kademeler arasında artar (c1 → c4), tek blok içinde değil.

## 3. MÜZİK

- Müzik dosyası bölümün ölçü sayısıyla **birebir** aynı olmalı
  (`03-motor/muzik-uzat.py`). Kısa müzik `-shortest` ile videoyu kırpar.
- BPM ölçülür, verilmez (`03-motor/olc-tempo-kayma.py`, ölçüm notları
  `01-muzik/*-OLCUM.md`).
- Müzik depoya girmez (bkz. `.gitignore`), bu yüzden **ses Actions'ta değil
  yerelde eklenir.**

## 4. RENDER HATTI

- Tam bölüm: GitHub Actions `render-bolum.yml`, paralel parçalar,
  `birlestir: hayir` (workflow'un ses yolu 120 BPM'lik HAM mp3'e bağlı).
- `--bolum` değeri **`../bolumler/x.json`** biçiminde yazılır. `bolumler/x.json`
  yazılırsa `render.js` dosyayı bulamaz, sessizce `sabitler.json`'daki 130
  BPM'e düşer ve ses görüntüden kayar — hiçbir hata görünmez.
- Mekân görselleri `07-mekan/` altında ve o klasör `.gitignore`'da. Yeni bir
  mekânın sprite'ları `git add -f` ile alınmazsa runner'da mekân **boş** render
  edilir ve bu ancak dosya indirildikten sonra fark edilir.
- Montaj yerel `ffmpeg` ile (`03-motor/*-montaj.sh`). Doğrulama: süre karşılaştır
  + `ffmpeg -xerror` tam decode + parça sınırlarından kare kontrolü.

## 5. TESLİM

- Biten master `Masaüstü/DANCE-MODE-SEHIR-YUKLENECEK/` klasörüne konur ve
  o klasörün `OKUBENI.md` dosyasına künyesi yazılır.
- O klasöre **önizleme, kesit, kare, not girmez.** Süre kuralına uymayan bir
  çıktı oraya master diye konmaz.
- Oradaki hiçbir dosya sorulmadan taşınmaz/silinmez.
