# STAY ON BEAT #11 — piksel ve zaman ölçümü

> Kaynak: `youtube.com/watch?v=iX3uYYKH9rQ` · Liam Fitness · 11:15 · 3840×2160 yayınlanmış
> Ölçüm: 29 Ağustos 2026. Video 720p indirildi, 20.237 karenin tamamı tarandı.
> `docs/ANALIZ-PLANI-DETAYLI.md`'de tarif edilen ölçümün ilk turu.
>
> **Her sayının nasıl elde edildiği yazılı.** Ölçemediklerim en sonda ayrı başlık —
> onları tahminle doldurmadım.

---

## 1. Tempo — iki bağımsız yöntem, aynı sonuç

| Yöntem | Sonuç |
|---|---|
| Cue zamanlarından ızgara çözümü | **130,04 BPM** |
| Sesten tempo (onset + tarak filtresi) | **130,15 BPM** |

İkisi 0,1 BPM içinde uyuşuyor. **Vuruş = 0,4614 sn · Ölçü = 1,846 sn.**

Cue ızgarası şöyle çözüldü: combo sayacının her artışı bir cue demek. Sağ üstteki
rakam bölgesi (190×60 px) tüm video boyunca kare kare tarandı, parlak piksel
maskesi kare farkıyla karşılaştırıldı, 0,25 sn'den yakın çift tespitler
birleştirildi. Kalan **966 cue** zamanı için, faz dağılımını en dar yapan periyot
arandı.

**Bize etkisi:** rakip 130 BPM'de. Bizim 120'miz altında kalıyor. Daha önce
kanal analizinde bulduğum 128-142 bandını bu ölçüm doğruluyor.

---

## 2. Yapı — 366 ölçü, molasız

| Ölçüm | Değer |
|---|---|
| Toplam süre | 674,6 sn (11:15) |
| Ölçü sayısı | **366** |
| Toplam cue | **966** |
| Ortalama yoğunluk | **2,64 cue/ölçü** |
| İlk cue | 0,1 sn — daha ilk saniyede |
| Combo ekranda | 647 sn / 674 sn (%96) |

### En önemli bulgu: mola yok

4 ölçülük kayan pencerede yoğunluk aradım. **Ardışık 8 ölçü boyunca 0,5 cue/ölçü
altına inen tek bir aralık bulunamadı.** Yani bu videoda planımızdaki gibi
"nefes" bölümleri yok.

Bunun yerine yoğunluk **sürekli dalgalanıyor**: 0,75 ile 4,25 cue/ölçü arasında,
yaklaşık 20-40 saniyede bir inip çıkıyor. Dinlenme, susarak değil **seyrelterek**
veriliyor.

Ölçülen eğri (4 ölçülük pencere, cue/ölçü):

```
    0 sn  4,00   ████████████████
   22 sn  1,25   █████
   44 sn  4,00   ████████████████
   66 sn  0,50   ██
   89 sn  2,25   █████████
  111 sn  3,75   ███████████████
  133 sn  2,50   ██████████
  155 sn  3,75   ███████████████
  177 sn  2,50   ██████████
  199 sn  3,75   ███████████████
  221 sn  3,00   ████████████
  244 sn  1,25   █████
  266 sn  0,75   ███
  288 sn  1,50   ██████
  310 sn  3,00   ████████████
  332 sn  1,50   ██████
  354 sn  2,00   ████████
  377 sn  3,50   ██████████████
  399 sn  4,00   ████████████████
  421 sn  2,25   █████████
  443 sn  4,00   ████████████████
  465 sn  3,50   ██████████████
  487 sn  1,25   █████
  509 sn  4,00   ████████████████
  532 sn  3,25   █████████████
  554 sn  4,00   ████████████████
  576 sn  0,75   ███
  598 sn  4,25   █████████████████
  620 sn  3,00   ████████████
  642 sn  4,00   ████████████████
  664 sn  1,00   ████
```

Okunacak üç şey:

1. **Videoya 4,00 ile giriyor.** Öğretme bölümü yok, ısınma yok. İlk cue 0,1 sn'de.
2. **Zorluk monoton artmıyor.** Testere dişi gibi: yükselir, düşer, yükselir.
   Tepe değeri sona doğru biraz artıyor (baş tarafta 4,00, 598 sn'de 4,25) ama
   fark küçük. Yani "her tur daha zor" değil, "sürekli nefes al-ver".
3. **Dipler kısa.** En derin dip 0,50 (66 sn), ama iki pencere sonra tekrar 2,25.

### Cue aralıkları

| Aralık | Kaç kez |
|---|---:|
| 0,45-0,50 sn | 430 |
| 0,40-0,45 sn | 313 |
| 0,35-0,40 sn | 35 |
| 1,55-1,60 sn | 15 |

Baskın aralık **bir vuruş** (0,461 sn). Yani cue'lar çeyreklik notalar üzerinde;
sekizlik altbölünme neredeyse hiç yok.

---

## 3. Görüntü — parlaklık, doygunluk, renk

36 kare üzerinden (üç ayrı bölümden):

| Ölçüm | Değer |
|---|---|
| Medyan parlaklık (luma) | **0,045** |
| Neredeyse siyah piksel (<0,06) | **%57,4** |
| Luma < 0,15 | %79,6 |
| Parlak piksel (>0,60) | **%2,7** |
| Medyan doygunluk | **0,72** |
| Doygunluk > 0,5 olan piksel | %72,8 |

**Baskın tonlar** (doygun + parlak pikseller):

| Ton | Pay |
|---|---:|
| 250-270° mor | %33,0 |
| 180-200° cyan | %14,1 |
| 300-310° magenta | %9,2 |
| 210-240° mavi | %8,9 |

En çok geçen parlak renkler: `#301058`, `#281050`, `#280850` (mor ambient),
`#f8f8f8` (yazı/kontur), `#106880` `#106888` (cyan).

Kare başına ayırt edilebilir renk sayısı: **1296-1780** (4 bitlik kuantalama).

---

## 4. Yerleşim ve tipografi

1600×900'e ölçeklenmiş karelerden, kare boyutuna oran olarak:

| Öge | Ölçüm |
|---|---|
| Combo bloğu yüksekliği | kare yüksekliğinin **%24-29**'u |
| Combo sağ boşluğu | **%4,4-4,7** |
| Combo üst kenarı | %0-3 |
| Siluet paneli | solda, kare yüksekliğinin neredeyse tamamı boyunca |

Combo bloğu (rakam + COMBO etiketi + rozet) karenin **dörtte birinden fazlasını**
kaplıyor. Bizde bu oran daha küçük.

---

## 5. Bizim değerlerimizle karşılaştırma

| | STAY ON BEAT #11 | Bizim bölüm-01 |
|---|---|---|
| BPM | **130** | 120 |
| Ölçü | 1,846 sn | 2,000 sn |
| Süre | 11:15 (366 ölçü) | 8:48 (264 ölçü) |
| Ortalama yoğunluk | **2,64 cue/ölçü** | 2,75 cue/ölçü |
| Yoğunluk aralığı | 0,75 - 4,25 | 1,00 - 4,00 |
| Mola | **yok** (seyrelme var) | 3 × 8 ölçü tam mola |
| Giriş | cue 0,1 sn'de | 4 ölçü boş + 32 ölçü öğretme |
| Medyan parlaklık | 0,045 | 0,083 |
| Siyah piksel | %57,4 | %45,4 |

**Yoğunluk ortalamamız neredeyse aynı** (2,75 / 2,64) — burası tutmuş.

Ayrıldığımız üç yer:

1. **Tempo** — 10 BPM yavaşız.
2. **Molalar** — bizde tam sessizlik var, onlarda yok. Bizim molalar 16'şar saniye
   hiçbir şey olmayan aralıklar; izleyicinin video bitti sanma riski var.
3. **Giriş** — biz 36 ölçü (1:12) öğretmeye ayırıyoruz, onlar sıfır. Bu bilinçli
   bir tercih olabilir ama tutma oranına etkisi ölçülmedi.

---

## 6. Ölçemediklerim

Dürüstlük için: aşağıdakiler denendi ama **güvenilir sayı çıkmadı**.

**Nota yaklaşma süresi.** İki yöntem denendi:
- Ufuk satırı ile vuruş çizgisi satırının çapraz korelasyonu → 0,23 sn çıktı ama
  korelasyon gücü 0,34 ve tepe noktaları vuruş periyoduna denk düşüyor. Yani
  yaklaşmayı değil ritmi yakalamış. **Geçersiz.**
- Yol ekseninde yarık tarama (slit-scan) görüntüsü → eğriler görünüyor, perspektif
  ivmesi net, ama başlangıç/bitiş kenarları okunacak keskinlikte değil.

Bu sayı planda "işin tamamı telegraph penceresinde" denen şey; doğru ölçülmeden
kendi 2,0 sn değerimizi değiştirmeyeceğim. Sonraki turda tek bir notayı kare kare
elle takip ederek ölçeceğim — 30-40 kare, kesin sonuç verir.

**Siluet paneli geometrisi.** Otomatik tespit koyu sahne alanlarını panel sandı
(x %0-34 gibi saçma değerler). Elle ölçüm gerekiyor.

**Tipografi ailesi ve harf aralığı.** Punto oranı ölçüldü ama Impact / Arial Black /
Bebas Neue ayrımı ve harf aralığı ölçülmedi.

**Diğer beş kanal.** Bu tur sadece STAY ON BEAT #11 üzerinde yapıldı. Plan en az
iki kanaldan üçer video diyor.
