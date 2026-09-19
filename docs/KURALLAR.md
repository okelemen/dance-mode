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

## 2a. LEVEL DAĞILIMI (16 Eyl 2026)

**Her videoda HUD'daki LEVEL video boyunca 1 → 2 → 3 → 4 → 5 ilerler.**
Süre bu beş levele eşit paylaştırılır (10 dakikalık bölümde her level ~2 dk).
Bütün video boyunca "LEVEL 1" yazması kural ihlalidir.

- Sınırlar: `toplam_olcu × k / 5` (k = 1…4). İskelet blok sınırına (tercihen
  mola sonrasına) yuvarlanabilir, dilimler yaklaşık eşit kalır.
- **Motor tuzağı:** `sahne.html`'de seviye ortama bağlı (`seviye: i + 1`).
  Tek sahneli bölümde ortam bir tane olduğu için level hiç artmaz. Level,
  ortamdan bağımsız olarak bölüm dosyasından gelmeli.
- Geçişte "LEVEL UP" duyurusu çıkar.
- Render sonrası kare kontrolünde her dilimden en az bir karede LEVEL okunur.
- İlk ihlal: `DANCE-MODE-06-ELMA-1080p.mp4` baştan sona LEVEL 1.

## 2b. ENGEL = SİLUETİN HAREKETİ (16 Eyl 2026)

Siluetin hareketi engeli **gerçekte geçmek için yapılacak** hareket olur.
Üstte engel → eğil/çömel · yerde alçak engel → zıpla/yüksek adım · bir yanı
kapalı → açık tarafa yana · hedef → o yöne uzan/it · dar geçit → gövdeyi daralt.
Önce engel, sonra hareket; iki hareketle okunabilen engel kullanılmaz. Tam tablo:
`Masaüstü/REFERANSLAR/engel-defteri.md`.

## 3. MÜZİK

- Müzik dosyası bölümün ölçü sayısıyla **birebir** aynı olmalı
  (`03-motor/muzik-uzat.py`). Kısa müzik `-shortest` ile videoyu kırpar.
- BPM ölçülür, verilmez (`03-motor/olc-tempo-kayma.py`, ölçüm notları
  `01-muzik/*-OLCUM.md`).
- Müzik depoya girmez (bkz. `.gitignore`), bu yüzden **ses Actions'ta değil
  yerelde eklenir.**

### 3a. Her video yeni müzik (17 Eyl 2026)

Her bölüm kendi müziğiyle çıkar. Bölüme özel, ölçülmüş müzik yoksa tam render
başlamaz. Hata kaydı: BAL render'ı önceki bölümlerin müziğiyle başlatıldı, iptal edildi.

## 4. RENDER HATTI

- **YEREL RENDER YASAK (19 Eyl 2026, kullanıcı kararı).** Kesit, önizleme, test, tam
  bölüm — her render GitHub Actions'ta (`render-bolum.yml`). Yerelde `node render.js`
  çalıştırılmaz. Yerelde yalnız ölçüm, müzik hazırlama, ffmpeg montaj/ses, kare kontrolü.
  Hata kaydı: müzikli BULUT kesiti yerelde başlatıldı (~55 dk), kullanıcı durdurdu.

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

## 6. KAPAK ŞABLONU — KİLİTLİ (17 Eyl 2026, kullanıcı: "artık stilimiz bu")

Referans: `05-kapak/KAPAK-SABLON-REFERANS.jpg` (Elma, "APPLE RUN").
Üretici: `05-kapak/kapak-sablon.py` — kilitli sabitler dosyanın başında;
referansı piksel farkı 0 ile yeniden üretir.
Tuval 1280×720. Koordinatlar bu tuvalde, piksel.

**Kilitli — sormadan değişmez:**

| Öğe | Kilitli olan | Değer |
|---|---|---|
| Başlık "DANCE MODE" | yazı tipi + konum | Impact, 190 px, sağa eğik (shear 0,22), beyaz dolgu, 8 px siyah kontur, arkada ışıma; **merkez (640, 105)**, en fazla 1180 px genişlik |
| Tema şeridi | sadece konum | **merkez (640, 225)**, başlığın hemen altında, ortada |
| Siluet | sadece konum | **yatay merkez x = 640** (tam orta, yolun ortası); boy 490 px; **üst kenar y = 255** (şeridin altı, hiçbir yazıyı kapatmaz); alt kenar y = 745 (ayak tabanı kareden taşar) |
| NEW LEVEL rozeti (yıldız) | sadece konum | **sol alt, merkez (185, 545)**, yarıçap 150, −10° |
| COMBO rozeti (yıldız) | sadece konum | **sağ alt, merkez (1080, 540)**, yarıçap 170, +8°; sayı + "COMBO" yıldızın içinde |

Katman sırası: arka plan → siluet → başlık → şerit → rozetler. Yazılar
siluetin üstünde durur; siluet yazıyı kapatmaz.

**Serbest — videoya göre değişir:** arka plan karesi, tema adı, renkler (şerit,
ışıma, rozet zeminleri), siluetin pozu, LEVEL ve COMBO sayıları, hız çizgileri.
(Başlık metninin "NEON DANCE MODE" olup olmayacağı ayrı karar; yazı tipi ve
konum yine yukarıdaki gibi.)

## 7. EKRAN BOŞ KALMAZ (18 Eyl 2026, kullanıcı: "izleyici boşluklu ekranı sevmiyor")

Doldurma kuralı (`Masaüstü/REFERANSLAR/doldurma-kurali.md`) artık yalnız zemin
bandı için değil **kadrajın tamamı** için geçerli: zemin, ufuk şeridi, gök,
yanlar. Mekânın taşıyıcı fikri boşluk olsa bile (asılı pist, açık gök) ekran
boş bırakılmaz; boşluk o konseptin kendi öğeleriyle kapatılır. Her mekân
önerisinde eklenti listesi yazılır; kare kontrolünde belirgin, sürekli, düz
renkli alan varsa (gök dâhil) mekân teslim edilmez. İlk uygulandığı yer:
MEK-005 BULUT.

## 8. HER LEVEL BİR MEKÂN (18 Eyl 2026 — "tek sahne" kararının yerine)

Video 5 mekândan oluşur, **her LEVEL bir mekân**; değişim LEVEL UP anında
(`ortam_olcu` = `seviye_olcu`). Mekânlar seçilen ilk mekânın kurgusundan türer;
taşıyıcı fikir korunur, her biri farklı bir hâldir (saat, hava, ışık, gök öğesi;
salt renk değişimi sayılmaz). **Engeller her mekânda o mekânın dünyasından
yeniden kurulur**; hareket aileleri ve engel = hareket kuralı sabit.
Kayıt: `Masaüstü/REFERANSLAR/mekan-defteri.md` → MEK-NNN a…e.

### 8a. Engeller mekâna göre ve her levelde farklı (18 Eyl 2026)

Her mekânın engel nesnesi o mekânın dünyasından ve mekânla uyumlu; bir levelin
engel nesnesi başka bir levelde (ve önceki videolarda) tekrar edilmez. 5 level =
5 ayrı engel dünyası. Öneri yazılırken her level için nesne + mekânla bağı yazılır.
Her levelde TEK engel nesnesi (19 Eyl 2026): dört hareket ailesi aynı nesnenin farklı
duruşlarıyla kurulur; 5 level = 5 nesne.
