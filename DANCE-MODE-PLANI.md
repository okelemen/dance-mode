# DANCE MODE — Proje Planı

> Durum: **Suno üyeliği bekleniyor.** Üyelik alınınca "BURADAN DEVAM ET" bölümüne git.
> Son güncelleme: 23 Ağustos 2026

Referans kanal: `@DanceChallengeMode` — "Immersive Dance Mode", 31,5 B abone, 20 video.
Bu, mevcut ekonomi kanalından **tamamen ayrı** bir projedir.

---

## 1. Bu format nedir

Neon bir tünelde ilerleyen, ritim oyunu görünümlü, 8-10 dakikalık "interaktif" dans/warm-up videosu.
Ekranda **çekilmiş tek bir kare yok** — her şey prosedürel render.

Kare 5 katmandan oluşuyor:

| Katman | İçerik | Üretim |
|---|---|---|
| Zemin | Neon highway, kayan grid | Three.js geometri |
| Nota | Halkalar, oklar, adım kareleri | Izgaradan sürülür |
| Dansçı | Siyah siluet | Mixamo mocap → siluet render |
| HUD | COMBO, EPIC!, LEVEL UP, skor | Overlay, vuruşa senkron |
| Ses | 8-10 dk kesintisiz 120 BPM | Suno (instrumental) |

---

## 2. Tasarım kararları (neden böyle)

**Combo sayacı bir yalandır.** İzleyici dans etse de etmese de artıyor. Buna rağmen
çalışıyor, çünkü beyin *önceden haber verilmiş ve zamanında çözülmüş* olayı kendi
başarısı sayıyor. Yani işin tamamı **telegraph penceresinde**.

**Nota, vuruştan 1,5-2 sn önce görünür olmalı.** Kısa olursa izleyici geride kalır,
"beceremiyorum" hisseder ve bırakır. Uzun olursa gerilim ölür.

**Tünel hızı asla değişmez.** İzleyici ilk 20 saniyede yaklaşma süresini öğreniyor ve
o sezgiye güveniyor. Ortada değiştirmek sözleşmeyi bozar.

**Asla kesme yok.** Tek, kesintisiz kamera. Her kesme "bu bir video" der; oysa amaç
"bu bir ekran" dedirtmek.

**Izgara önce, müzik sonra.** Beat tespiti (librosa) YAPMIYORUZ. Sabit BPM seçip
kafesi biz sahipleniyoruz — tespit hatası yok, drift yok. Koreografi zamanda değil
**ölçü numarasında** yazılıyor: "37. ölçünün 3. vuruşunda sol lane, dodge."
Bu insan tarafından okunabilir, versiyonlanabilir, yeniden kullanılabilir.

**Siluetin güzel dans etmesi önemli değil, cue ile aynı anda tepki vermesi önemli.**
Senkron kayarsa yanılsama anında çöker.

---

## 3. Teknik sabitler — KİLİTLİ

### BPM = 120 (30 fps)

Keyfi değil. 30 fps'te tam sayı veren tek dans temposu:

| BPM | Kare/vuruş | |
|---|---|---|
| **120** | **15,000** | ✅ |
| 124 | 14,516 | ✗ |
| 126 | 14,286 | ✗ |
| 128 | 14,063 | ✗ |

Sonuçlar:
- 1 vuruş = 15 kare = 0,5 sn
- 1 ölçü (4 vuruş) = 60 kare = **tam 2 sn**
- 8 ölçülük cümle = 480 kare = **tam 16 sn**

Hiçbir yerde yuvarlama yok.

### Bölüm iskeleti (8:48)

| Bölüm | Ölçü | Süre | Amaç |
|---|---|---|---|
| Öğretme | 32 | 1:04 | Yeni mekaniği tanıt |
| Tur 1 | 48 | 1:36 | |
| Mola | 8 | 0:16 | Nefes |
| Tur 2 | 48 | 1:36 | Yoğunluk artar |
| Mola | 8 | 0:16 | Nefes |
| Tur 3 | 48 | 1:36 | Yoğunluk daha da artar |
| Mola | 8 | 0:16 | Nefes |
| Final | 64 | 2:08 | Combo kapak rakamına koşar |
| **TOPLAM** | **264** | **8:48** | |

Molalar şart. Sürekli zirvede kalan şey zirvesizdir.

---

## 4. Hareket kütüphanesi — 12 klip yeter

**20 videoluk dans arşivine ihtiyaç YOK.** Cue tiplerine karşılık gelen ~12 hareket:

sol adım · sağ adım · zıplama · çömelme · sağa kaçış · sola kaçış ·
kollar yukarı · dönüş · punch · idle · 2 tempo varyasyonu

**Altın kural:** her hareket tam 1 veya 2 ölçü olacak ve **nötr duruşta başlayıp
nötr duruşta bitecek.** Bu sağlanırsa her hareket her hareketten sonra gelebilir
(oyun motorlarındaki animasyon state machine mantığı).

12 hareket, 4'lü dizilişlerle 9 dakikayı doldurmaya fazlasıyla yeten çeşitlilik verir.
**Kombinatorik senin arşivin.** Yeni video = yeni çekim değil, yeni diziliş.

Kaynak: **Mixamo** (mixamo.com) — web sitesi, Adobe hesabıyla ücretsiz giriş,
.fbx indir. Hiçbir Adobe programı kurulmuyor. 12 hareket toplam ~50 MB.

---

## 5. Pipeline

### Blender YOK
Mixamo .fbx/.glb dosyası **doğrudan Three.js içine** yüklenip iskelet animasyonu orada
oynatılıyor. Tek motor, tek koordinat sistemi, ara export yok. Bu makine için
zorunlu, ama zaten daha iyi pipeline.

### Deterministik render
`kare N = zaman N/30`. Duvar saati yok, ekran kaydı yok.
Aynı JSON iki ay sonra render edilirse bit bit aynı video çıkar.

**Kareler diske YAZILMAZ** — doğrudan ffmpeg'e boru ile gider.
(1080p PNG, 16.200 kare, yaklaşık 25 GB; ham RGBA yaklaşık 134 GB.
Boru bir zorunluluk, optimizasyon değil.)

### İş bölümü
> **Laptop = tasarım. Bulut = render.**

Laptopta sadece küçük önizleme (640x360, gerçek zamanlı) koşar.
9 dakikalık 1080p render **bu makinede hiç olmaz** — GitHub Actions üzerinde yapılır.
Private repoda ayda 2000 dk bedava; bölüm başı 30-60 dk, yani ayda 20-30 bölüm ücretsiz.

### Hedef
1080p / 30 fps. 4K yok, 60 fps yok.

---

## 6. Tekrar problemi — en kritik risk

"NEW LEVEL 11" bir **sözdür**. Tutulmazsa izleyici üçüncü videoda anlar ve gider.
Ayrıca YouTube tekrarlayan içerik politikası tam olarak buna bakar.

Her bölüme iki eksende kimlik verilir:

**Biyom** — palet ve geometri (Neon Grid / Uzay / Retro CRT / Sıvı zemin)
**Mekanik** — o bölümde tanıtılan yeni cue tipi (çift lane / tutma notası / ayna modu / yarım tempo)

Videonun ilk 32 ölçüsü yeni mekaniği öğretir. Bu ikisi varsa motorun aynı olması
sorun değil — Mario oyunlarında da motor aynıdır.

---

## 7. SUNO BRIEF

### Ayarlar
- [ ] **Ücretli plana geç (Pro yeterli).** Ücretsiz katman ticari kullanım hakkı VERMEZ.
      Free ile üretilip yayınlanırsa bütün proje boşa gider.
- [ ] **Instrumental modu AÇIK** — vokal yok (dikkat dağıtır, ayrıca söz telifi ayrı dert)
- [ ] **WAV indir, MP3 değil** — zaman esnetme yapılacak, kayıpsız kaynak lazım
- [ ] Uzun tek parça peşinde koşma. 2-4 dakikalık parçalar üret, ölçü sınırında birleştirilir

### Prompt şablonu

```
instrumental synthwave house, 120 BPM, four-on-the-floor kick,
driving arpeggiated bassline, neon retro-futuristic, steady groove,
consistent tempo throughout, no vocals, no tempo changes,
no ambient intro, minimal fills
```

Sondaki üç negatif kritik: tempo değişimi, uzun ambient giriş ve aşırı fill
ızgarayı bozar.

### Biyom varyantları (sadece ilk satır değişir)
- **Neon Grid:** `instrumental synthwave house`
- **Uzay:** `instrumental deep space progressive house, wide pads`
- **Retro CRT:** `instrumental 80s electro chiptune house`

### İLK İŞ: tam bölüm üretme YOK
Önce **tek bir 2 dakikalık test parçası** üret (Neon Grid promptu).
Tempo tutarlılığı ölçülüp prompt ona göre kalibre edilecek.

---

## 8. Suno sonrası: tempo düzeltme

Suno tam 120,000 BPM vermez, yaklaşık verir. WAV dosyaları geldiğinde:

1. Gerçek BPM ölçülür
2. ffmpeg ile mikroskobik zaman esnetme (yaklaşık %0,2 — kulakla duyulmaz), tam 120,000 olur
3. İlk vuruş t=0 noktasına gelecek şekilde kırpılır

Bundan sonra ızgara matematiksel olarak kusursuz.

---

## 9. Maliyet

| Kalem | Tutar |
|---|---|
| Mixamo, Node, ffmpeg, Three.js, Puppeteer | 0 |
| GitHub Actions (private, 2000 dk/ay) | 0 |
| Donanım | 0 |
| **Suno Pro** | **yaklaşık $10/ay** |

**Alt satır: ayda yaklaşık $10, sıfır donanım yatırımı.**
Ekonomi kanalından ucuz — orada video başına AI kredisi yanıyor, burada motor bir
kere yazılıyor ve marjinal maliyet sıfıra iniyor.

*(Fiyat benim bildiğim seviye; ödemeden önce teyit et, bu servisler sık fiyat değiştiriyor.)*

Opsiyonel, şimdilik gerek yok: Move.ai / Rokoko $15-25/ay, kendi mocap çekimin için.
En erken 10. bölümde düşünülür.

---

## 10. Makine durumu

**CPU** i5-7200U (2 çekirdek / 4 thread) · **RAM** 7,7 GB
**GPU** Intel HD 620 + AMD R7 M340 (zayıf) · **C:** 222 GB

### Yapılan disk temizliği (23 Ağu 2026)
CapCut, `AppData\Local` içinde 143 GB şişmişti.

| İşlem | Kazanç |
|---|---|
| Cache\SmartCrop + Cache\recognize silindi | ~86 GB |
| 28 CapCut sürümünün 26'sı silindi (9.2.8 ve 9.1.0 kaldı) | ~42 GB |

**5,1 GB → 133,6 GB boş.** Taslaklara (`Projects\com.lveditor.draft`) dokunulmadı.

> CapCut bu cache'i zamanla yeniden şişirir. Birkaç ayda bir kontrol et.

### Kurulanlar
- [x] Node.js 24.19.0 LTS
- [x] ffmpeg (Gyan)
- [x] Python 3.12
- [x] git (zaten vardı)

### Bu makinede KESİN yapılamayanlar
- Kendi videondan mocap çıkarma (WHAM / Move.ai lokal) — CUDA yok, GPU yetersiz
- 4K render
- 9 dakikalık 1080p render (buluta gider)

### Proje konumu
C: sürücüsünde olacak. **E: (flash bellek) kullanılmayacak** — çıkarılabilir sürücü,
render sırasında çıkarılırsa iş çöper. E: yedek olarak kalsın.

---

## BURADAN DEVAM ET

Suno üyeliği alındığında sırayla:

1. **Suno Pro'ya geç**, instrumental mod açık
2. **Tek bir 2 dk test parçası üret** — yukarıdaki Neon Grid promptu, WAV indir
3. Claude'a getir → gerçek BPM ölçülür, prompt kalibre edilir
4. **Mixamo'dan 12 hareketi indir** (nötr başla / nötr bit kuralına uyanları seç)
5. **Tek ölçülük prototip** — 2 saniye, loop halinde:
   bir tünel + bir hız + bir nota + bir siluet hareketi + bir combo tiki

> Adım 5 en önemlisi. Bu 2 saniye doğru hissettiriyorsa geri kalan 9 dakika sadece
> tekrardır. Yanlış hissettiriyorsa 9 dakika yapmak hiçbir şeyi kurtarmaz.
>
> Bu formatın ekonomisi burada saklı: normal bir kanalda "ilk video" en pahalı şeydir,
> burada ilk **ölçü** en pahalı şeydir. Ondan sonrası çarpma işlemidir.
