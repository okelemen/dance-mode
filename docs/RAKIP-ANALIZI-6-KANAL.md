# 6 Kanal Rakip Analizi

> Ölçüm tarihi: **26 Ağustos 2026**
> Yöntem: YouTube InnerTube verisi (abone/görüntüleme/süre/etiket/açıklama/kategori),
> her kanalın en çok izlenen videosundan 90 sn ses indirilip numpy ile tempo +
> spektrum ölçümü, kapak görselleri maxres olarak indirilip incelendi.
> Tahmin değil, ölçüm. Ölçülemeyeni "ölçemedim" diye yazdım.

---

## 0. Tek cümlelik sonuç

Bu 6 kanal tek bir niş değil, **iki ayrı niş**: soyut ritim şeridi (IP'siz) ve
lisanslı karakter koşusu (IP'li). Bizim projemiz birincisinde. Ve o birincinin
müziği bizim kilitlediğimiz 120 BPM'den **hızlı** — sahadaki medyan **135 BPM**.

---

## 1. Kanal künyeleri

| Kanal | Handle | Abone | Video | Toplam gör. | Medyan | Ortalama | En iyi | 1M+ | Gör./abone |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HIGH QUALITY Immersive (BEAT MOTION) | @highqualityimmersive | 229 B | 40* | 25,9 Mn | 493 B | 862 B | 4,0 Mn | 8 | 113 |
| Liam Fitness (STAY ON BEAT) | @Liam_reality_1 | 63,4 B | 21 | 17,9 Mn | 127 B | 854 B | 5,0 Mn | 8 | 283 |
| Escapify | @Escapify2026 | 60,8 B | 30 | 17,3 Mn | 118 B | 597 B | 10,0 Mn | 3 | 285 |
| Immersive Dance Mode | @DanceChallengeMode | 32,9 B | 20 | 12,4 Mn | **396 B** | 619 B | 2,2 Mn | 4 | 376 |
| FLEM | @FLEM-100 | 25,4 B | 22 | 14,2 Mn | 70 B | 645 B | **11,0 Mn** | 1 | **558** |
| Prime & Prep | @primeandprep | 13,8 B | 17 | 4,4 Mn | 37 B | 258 B | 1,7 Mn | 2 | 318 |

\* Beat Motion'ın 40 videosu var, ilk sayfadan 30'u okunabildi; tablo o 30 üzerinden.

**Okunacak yer medyan sütunu.** Ortalama tek bir viral videoyla şişiyor.
Medyanı en yüksek kanal **Dance Mode (396 B)** — yani en istikrarlı olan o,
en büyük olan değil.

---

## 2. İki farklı niş

### A) Soyut ritim şeridi — IP kullanmıyor
**Dance Mode · Beat Motion · Stay on Beat**

Siyah zemin, neon şerit, siluet dansçı, ayak izi/yumruk simgeli notalar, COMBO sayacı.
Ekranda telifli hiçbir şey yok. Sürdürülebilir. Bizim yolumuz bu.

Üçü **birbirinin kopyası**, hatta muhtemelen aynı ekip/aynı şablon:
Liam Fitness'ta 2 ay önce yüklenmiş **"BEAT MOTION #1"** başlıklı bir video duruyor
(26 B izlenme), sonra marka **STAY ON BEAT**'e dönmüş ve patlamış (5 Mn, 2,6 Mn, 1,8 Mn).
Yani aynı format iki kere denenmiş, ikinci isimle tutmuş.

### B) Lisanslı karakter koşusu — IP üzerine kurulu
**Escapify · FLEM · Prime & Prep**

Subway Surfers, Roblox Obby, Zootopia, Minecraft, Pokémon, Toy Story, Spider-Man,
Paw Patrol, Squid Game, K-Pop Demon Hunters, Sünger Bob...

Bu tarafın en büyük iki vurusu doğrudan IP'den geliyor:
- FLEM · **Zootopia Level → 11,0 Mn** (kanalın toplamının %77'si tek videoda)
- Escapify · **Roblox Obby Run → 10,0 Mn** (toplamın %58'i)

**Riski açıkça söylüyorum:** bu kanallar Disney/Roblox/SYBO markalarını başlıkta,
kapakta ve içerikte kullanıyor. Şu an ceza yemiyorlar ama tek bir telif talebiyle
kanalın gelirinin yarısı gidebilir. FLEM'in kapağında Nick Wilde ve Judy Hopps'un
**doğrudan film render'ı** var. Bu tesadüfen ayakta.

**Bizim için karar:** A grubunda kalıyoruz. Ama B grubundan öğrenilecek şey şu —
**tema ismi aramayı çekiyor.** IP olmadan tema yapılabilir: "Neon Şehir", "Uzay
İstasyonu", "Zombi Kaçışı", "Buz Mağarası". Escapify'ın #11 "Medieval Level"i 18 B
almış ama #18 "Roblox Obby" 10 Mn — fark temanın *aranıyor olması*.

---

## 3. Müzik — ölçülmüş veri

Her kanalın en çok izlenen videosundan 60-150. saniye arası indirildi, mono 22 kHz.

| Kanal | BPM | Kick kilidi | Crest (dB) | Bas payı (<150 Hz) | Spektral merkez |
|---|---:|---:|---:|---:|---:|
| Dance Mode | **142** | **0,73** | 12,6 | 25,9 % | 2325 Hz |
| Escapify | 139 | 0,43 | 17,3 | 11,6 % | 2871 Hz |
| Beat Motion | 135 | 0,50 | 16,0 | 28,4 % | 2052 Hz |
| Prime & Prep | 131 | 0,15 | 18,3 | 24,3 % | 2805 Hz |
| Stay on Beat | 130 | 0,61 | **13,3** | 18,1 % | 2767 Hz |
| FLEM | 128 | 0,29 | 18,6 | 14,2 % | 2749 Hz |

Sütunlar ne demek:
- **Kick kilidi**: davulun vuruş ızgarasına ne kadar sıkı oturduğu (1 = kusursuz
  four-on-the-floor). Yüksekse "dans müziği", düşükse "fon müziği".
- **Crest**: tepe ile ortalama arası fark. **Düşük = daha çok limitlenmiş, daha gür.**
  Telefon hoparlöründe duyulan şey bu.
- **Spektral merkez**: sesin parlaklığı. Yüksek = tiz/çocuksu, düşük = kalın/kulüp.

### Okunan üç şey

**1. Kimse 120 BPM'de değil.** Aralık 128-142, medyan 135. Bizim kilitli 120'miz
tüm sahanın altında. Ritim kanallarının ortalaması 135,7; koşu kanallarının 132,7.

**2. İki müzik tarzı, iki nişe birebir oturuyor.**
- *Ritim kanalları* (Dance Mode, Stay on Beat, Beat Motion): kalın bas (%18-28),
  sıkı four-on-the-floor (0,50-0,73), gür/limitli (12,6-16 dB). Bu **EDM/dance-house**.
  Dance Mode 142 BPM + 0,73 kilit ile en "kulüp" olanı.
- *Koşu kanalları* (Escapify, FLEM, Prime & Prep): ince bas (%11-14 Escapify/FLEM),
  gevşek davul (0,15-0,43), parlak (2749-2871 Hz), dinamik (17-19 dB).
  Bu **çizgi film kovalamaca müziği** — ritim değil, tempo hissi veriyor.

**3. Hiçbirinde telifli müzik yok.** 12 videonun tamamında YouTube'un "Bu videodaki
müzik" bölümü **boş**. Yani hepsi Content ID'ye takılmayan müzik kullanıyor:
telifsiz kütüphane ya da AI üretimi. Suno kararımız sahanın standardı.

### Bize etkisi — BPM kararı yeniden açılmalı

Planda 120 BPM "kilitli" çünkü 30 fps'te tam sayı kare veriyor (15 kare/vuruş).
Gerekçe doğru, ama 120 tek çözüm değil. `1800 / n` formülünde her n tam sayı verir:

| n (kare/vuruş) | BPM | Ölçü (kare) | Değerlendirme |
|---:|---:|---:|---|
| 15 | 120,00 | 60 | Mevcut. Sahanın altında. |
| **14** | **128,57** | **56** | FLEM'in temposu, aralığın alt ucu |
| **13** | **138,46** | **52** | **Medyanın (135) hemen üstü, Dance Mode'a yakın** |
| 12 | 150,00 | 48 | Sahanın üstünde, koşuya kayar |

**Önerim: 138,46 BPM (13 kare/vuruş).** Tam sayı matematiği bozulmuyor,
tempo rakiplerin tam ortasına oturuyor. 8 ölçülük cümle 416 kare = 13,867 sn.

Maliyeti dürüstçe: `01-muzik/bolum-01-neon-grid-120bpm.wav` yeniden üretilir ve
koreografi zaman değil ölçü cinsinden yazıldığı için **koreografi aynen taşınır**.
Motor tarafında değişen tek şey kare/vuruş sabiti. Bu kararı sen vereceksin.

### Suno brief güncellemesi (öneri)

```
instrumental dance house, 138 BPM, hard four-on-the-floor kick,
deep sub bass, driving arpeggiated synth, neon retro-futuristic,
loud and compressed, consistent tempo throughout, no vocals,
no tempo changes, no ambient intro, minimal fills
```
Eklenen: `hard four-on-the-floor` + `deep sub bass` + `loud and compressed`.
Ölçüm bunları söylüyor: kazananlar hem daha basslı hem daha gür.

---

## 4. Kapak tasarımı — şablon net

En iyi 6 videonun maxres kapağı incelendi. A grubunun üçünde **birebir aynı iskelet**:

| Bölge | İçerik |
|---|---|
| Üst şerit | Dev, sıkışık, italik büyük harf başlık — beyaz, siyah kontur + hafif glow |
| Merkez sağ | Siyah siluet, **beyaz parlayan dış çizgi**, aksiyon pozunda (yumruk/adım) |
| Merkez | Perspektifte kaçan neon şerit, üzerinde ayak izi / yumruk simgeli fayanslar |
| Sol alt | **Sarı yıldız patlaması rozeti**: "NEW LEVEL 15" — sarı zemin, siyah kontur |
| Sağ orta | Büyük combo rakamı + altında küçük "COMBO" |
| Kenarlar | Renkli çerçeve (Prime & Prep turuncu), hız çizgileri |

Dance Mode: siyah zemin + cyan/magenta. Stay on Beat: mor/pembe/sarı neon tünel,
kırık cam efekti, daha "sinematik". Beat Motion: siyah + neon yeşil/kırmızı,
kromatik sapma (RGB kayması) efekti.

Escapify tamamen ters gidiyor: **açık mavi gökyüzü, gökkuşağı Roblox blokları,
doygunluk sonuna kadar açık.** Ve 10 Mn almış. Yani "koyu zemin şart" değil —
şart olan **kontrast ve doluluk**.

Ortak nokta, altı kapakta da **ortada siyah siluet var**. İzleyici kendini oraya
koyuyor. Bu pazarlık edilebilir bir öge değil.

---

## 5. Başlık, açıklama, etiket

### Başlık kalıbı
Herkes aynı iskeleti kullanıyor:
```
[MARKA] #[N] | [4K] Immersive Interactive Warm Up | [alt açıklama]
```
- **Sıra numarası istisnasız var.** Dizi hissi = "bir sonrakini bekle".
- `Immersive Interactive Warm Up` ifadesi 6 kanalın 6'sında da geçiyor.
  Bu ifade nişin arama anahtarı; tartışmasız kullanılacak.
- `4K` etiketi 2026'da yaygınlaştı (Escapify, FLEM, Prime & Prep hepsi eklemiş).
- `No Equipment`, `Full Body`, `Easy Daily Routine` kuyruk kelimeler.

### Açıklama kalıbı
Dört bloklu, herkeste aynı:
1. Bir cümlelik kanca ("Turn your screen into a game and your body into the controller.")
2. **🎮 How to play** — nasıl oynanacağı, 3-4 madde
3. **🔥 Why play** — faydalar, 3 madde ("no talking, no distractions")
4. Yorum çağrısı ("Drop a 🔥") + hashtag bloğu

Prime & Prep tek başına farklı bir şey yapıyor: **zaman damgası/bölüm listesi**
koyuyor (`00:44 - Level 2: First Punch`). YouTube'da bölümler ilerleme çubuğunda
görünür ve izleyiciye "ne kadar kaldı" hissi verir. Küçük kanal olmasına rağmen
akıllı hamle; biz de yapmalıyız.

### Etiketler
Sahanın ortak sözlüğü (Escapify + Stay on Beat + Prime & Prep'ten):
```
immersive interactive warm up · interactive warm up · interactive workout ·
fitness gamification · exergaming · home cardio · no equipment workout ·
movement challenge · full body activation · beginner workout · cardio game ·
reaction training · brain break · PE games · viral interactive game · fun fitness
```
`brain break` ve `PE games` dikkat çekici: **okul/öğretmen kitlesi.** Prime & Prep
bunu bilinçli hedefliyor ("PE class activity"). Sınıfta oynatılan video = tek
oynatmada 25 kişi.

Dance Mode ve FLEM'in **hiç etiketi yok** — açıklamadaki hashtag'lerle idare
ediyorlar ve yine de milyonlara ulaşıyorlar. Yani etiket belirleyici değil,
ama bedava; koyacağız.

### Kategori
| Kanal | Kategori |
|---|---|
| Prime & Prep, Beat Motion, Stay on Beat | Sports |
| Dance Mode | Gaming (bir videoda Sports) |
| Escapify | Entertainment |
| FLEM | People & Blogs |

Dört farklı kategori, hepsi milyonluk. **Kategori bu nişte belirleyici değil.**
Sports en yaygını; onu seçeceğiz.

---

## 6. Süre ve yayın temposu

**Süre:** Herkes aynı yere yakınsamış. Başlangıçtaki 2-6 dakikalık videolar
düşük performanslı; bugünkü standart **8-12 dakika**.
- Dance Mode #1: 1:53 → 68 B · Dance Mode #15: 8:36 → 2,2 Mn
- Escapify #7-10: 3:30-3:44 → 33-123 B · Escapify #18: 10:51 → 10 Mn

8 dakika sınırı tesadüf değil: orta reklam ancak 8 dakikadan uzun videolarda açılıyor.
Bizim 8:48'lik iskeletimiz doğru tarafta.

Beat Motion iki kere 32 dakikalık video denemiş (#10, #14): 671 B ve 247 B —
kanal medyanının (493 B) altında ya da civarında. **Uzun sürüm işe yaramıyor.**

**Tempo:** Liderler haftada 1-2 video. Stay on Beat 2 ayda 11 video ile
63 B aboneye çıkmış — bu nişte **hız, kaliteden daha çok kazandırıyor.**

---

## 7. Viral dağılım — asıl önemli gerçek

| Kanal | Ortalama / medyan oranı |
|---|---:|
| FLEM | 9,2× |
| Escapify | 5,1× |
| Prime & Prep | 7,0× |
| Stay on Beat | 6,7× |
| Beat Motion | 1,7× |
| Dance Mode | 1,6× |

FLEM'in ortalaması medyanının **9 katı**. Yani FLEM aslında 70 B'lik bir kanal,
bir kere şimşek çakmış. Aynısı Escapify için de geçerli.

Beat Motion ve Dance Mode ise 1,6-1,7× ile **gerçekten istikrarlı**: her video
tutuyor. Ve ikisi de A grubunda, IP'siz, şablonlu.

**Çıkarım:** IP'li tema piyango; soyut ritim şeridi maaş. Biz maaşı seçtik,
doğru seçmişiz. Ama tek bir videoyla patlamayı beklemek yanlış — **hacim gerekiyor.**
Beat Motion 30+ videoda 229 B aboneye ulaştı.

---

## 8. Bizim projeye somut yapılacaklar

Öncelik sırasıyla:

1. **BPM kararını yeniden aç.** 120 → 138,46 (13 kare/vuruş). Tam sayı matematiği
   korunuyor, tempo sahanın ortasına geliyor. *Senin kararın.*
2. **Suno brief'ini güncelle:** `hard four-on-the-floor` + `deep sub bass` +
   `loud and compressed`. Ölçüm kazananların hem basslı hem gür olduğunu söylüyor.
3. **Kapak şablonunu birebir kur:** dev italik başlık + parlayan siyah siluet +
   sarı yıldız "NEW LEVEL n" rozeti + combo rakamı.
4. **Başlığa `Immersive Interactive Warm Up` ifadesini ve sıra numarasını koy.**
5. **Açıklamaya bölüm zaman damgaları ekle** (Prime & Prep'in yaptığı, kimsenin
   yapmadığı şey).
6. **Etiketlere `brain break` ve `PE games` ekle** — okul kitlesi.
7. **Süre 8-12 dakika**, 32 dakikalık deneme yapma.
8. **Tema ismi ver ama IP kullanma.** "DANCE MODE #3" yerine
   "DANCE MODE #3 | NEON CITY" gibi. Arama hacmi tema isminden geliyor.
9. **Hedef tempo: haftada 1 bölüm.** Motor bir kere yazıldığı için marjinal
   maliyet zaten sıfıra yakın; darboğaz koreografi yazımı olacak.

---

## 9. Ölçemediklerim

Dürüst olmak için: aşağıdakiler bu turda ölçülmedi.
- **Videoların içi** — kare kare piksel ölçümü (renk paleti, tipografi puntosu,
  yerleşim yüzdeleri). `ANALIZ-PLANI-DETAYLI.md` bunu tarif ediyor, ayrı iş.
- **İzlenme süresi / elde tutma** — YouTube dışarıya vermiyor.
- **Kanalların açılış tarihi ve ülkesi** — "Hakkında" sekmesi ayrı istek gerektiriyor.
- **Beat Motion'ın 10 videosu** — ilk sayfada gelmedi.
- Müzik ölçümü **kanal başına tek video, 90 saniye**. Genelleme bu örneklemle sınırlı.
