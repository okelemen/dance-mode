# TALİMATLAR — Dance Mode videoları

Bu dosya her oturumda otomatik okunur. Buradaki maddeler kullanıcı kararıdır;
aksi yazılı olarak söylenene kadar istisnasız uygulanır. Ayrıntı ve gerekçeler:
`C:\Users\eleme\DANCE-MODE\docs\KURALLAR.md`.

## 1. "Tam render al" = 9,5–10,5 dakikalık bölüm

- Kullanıcı "tam render al" dediğinde çıktı **570–630 sn** olur.
- Elde kısa bir önizleme bölüm dosyası olması bunu değiştirmez: önce iskelet
  tam süreye uzatılır (blok **sayısı** artar, uzunluğu değil), sonra render.
- Ölçü hesabı: `olcu = saniye / ((60 / BPM) * 4)`. Müzik dosyası da o kadar ölçü.
- 15 Eyl 2026 hatası: 64 ölçülük önizleme 1:55 olarak "tam render" diye teslim
  edildi, reddedildi, silindi.

## 2. LEVEL 1 → 5 video süresine eşit dağılır

- HUD'daki LEVEL video boyunca **1, 2, 3, 4, 5** diye ilerler; süre beş levele
  eşit paylaştırılır (10 dk'lık bölümde her level ~2 dk).
- Bütün video boyunca "LEVEL 1" yazması ihlaldir.
- Motor tuzağı: `sahne.html`'de seviye ortama bağlı (`seviye: i + 1`); tek
  sahneli bölümde level hiç artmaz. Level bölüm dosyasından, ortamdan bağımsız
  gelmeli.
- Render sonrası kare kontrolünde her level diliminden bir kare okunur.

## 3. Teslim

- Biten master `Masaüstü\DANCE-MODE-SEHIR-YUKLENECEK\` klasörüne konur,
  künyesi o klasörün `OKUBENI.md`'sine yazılır.
- O klasöre önizleme/kesit/kare girmez; 1. ve 2. maddeye uymayan çıktı master
  diye konmaz.
- Render GitHub Actions'ta (`render-bolum.yml`, paralel parça,
  `birlestir: hayir`, `--bolum ../bolumler/x.json`); ses ve montaj yerelde ffmpeg.
