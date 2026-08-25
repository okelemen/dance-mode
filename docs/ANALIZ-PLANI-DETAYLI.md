# Detayli rakip analizi — plan

> **Ne zaman:** Ilk tam bolum yayina hazir olduktan SONRA.
> **Neden sonra:** Analiz gunler surebilir; once elimizde calisan bir bolum olsun.

Su ana kadarki analizler yuzeyseldi — "koyu zemin, parlak nota" gibi genel
gozlemler. Bu sefer **olculmus veri** cikaracagiz.

---

## Yontem: tahmin degil, piksel olcumu

Videoyu tarayicida oynatip kareyi bir canvas'a cizerek **gercek piksel
degerlerini** okuyabiliyorum. Yani:

- Renkler goz karariyla degil, **hex kodu olarak** okunur
- Yazi boyutu "buyuk" degil, **kare yuksekliginin yuzdesi** olarak olculur
- Konumlar "sag ust" degil, **x/y yuzdesi** olarak yazilir

Bu sayede cikan sayilari dogrudan motora girebiliriz.

---

## Cikarilacaklar

### 1. Tipografi

Her yazi ogesi icin ayri ayri:

| Olculecek | Nasil |
|---|---|
| Punto | Buyuk harf yuksekligi / kare yuksekligi (%) |
| Yazi ailesi | Harf bicimi karsilastirmasi — Impact / Arial Black / Montserrat ExtraBold / Bebas Neue ayrimi |
| Harf araligi | Karakterler arasi bosluk / harf genisligi orani |
| Kontur | Var mi, kalinligi, rengi |
| Golge / parlama | Yaricap ve renk |
| Egim | Italik mi, kac derece |

Ogeler: combo rakami, COMBO etiketi, LEVEL, degerlendirme rozeti,
giris kartlari, final karti, video ici uyarilar.

### 2. Renk paleti

- Her ortamin **tam hex paleti** (zemin, lane, nota, kemer, ufuk, parcacik)
- Doygunluk ve parlaklik degerleri (HSL)
- Kac ortam var, hangi olculerde degisiyor
- Gecis suresi (kare cinsinden)

### 3. Yerlesim

Her ogenin konumu ve boyutu, kare boyutuna oran olarak:
- Siluet paneli: konum, boyut, cerceve kalinligi, kose yaricapi
- Combo blogu, rozet, LEVEL
- Vurus cizgisi yuksekligi
- Notalarin dogum ve vurus konumu

### 4. Hareket ve zamanlama

- Nota yaklasma suresi (kac saniye, kac vurus)
- Tunel akis hizi
- Parcacik yogunlugu (kare basina kac adet), hiz dagilimi
- Nabiz/parlama efektlerinin vurusa gore fazi
- Kamera hareketi var mi

### 5. Oynanis dili

- Cue tipleri ve her birinin gorsel karsiligi
- Nota bicimi: fayans / blok / halka / ok
- Nota uzerindeki simge tasarimi
- Isabet efekti: halka, patlama, parcacik
- Combo sifirlanma kurali
- Zorluk tirmanis egrisi (olcu basina cue sayisi)

### 6. Yapi

- Giris sekansi: kac saniye, kac kart, ne yaziyor
- Bolum uzunluklari ve mola yerleri
- Final sekansi
- Toplam sure ve olcu sayisi

### 7. Metin ve yayin

- Baslik kalibi
- Aciklama yapisi (bolum bolum)
- Etiketler
- Kapak tasarimi: oge yerlesimi, yazi boyutlari, renkler

---

## Hangi kanallar

1. **STAY ON BEAT** (Liam Fitness) — en buyugu, 4,7 Mn'luk videosu var
2. **DANCE MODE** (@DanceChallengeMode) — ilk referansimiz
3. **BEAT MOTION** — ayni ekibin ikinci markasi
4. Arama sonuclarindan cikacak diger benzer kanallar

En az iki kanaldan ucer video, farkli performans seviyelerinden
(en iyi / ortalama / dusuk) — boylece **neyin ise yaradigini** de
gorebiliriz, sadece ne yaptiklarini degil.

---

## Cikti

Bu belge doldurulmus haliyle, arti:
- Olculen degerlerin `spec/` altina makine okunur olarak girilmesi
- Bizim mevcut degerlerimizle **yan yana karsilastirma tablosu**
- Onceliklendirilmis yapilacaklar listesi

---

## Kullanicinin vurguladigi nokta

> "rakiplerimin videolari rengarenk, cok canli, interaktif bir doluluk var"

Yani asil sorun tek tek ogeler degil, **genel doluluk ve canlilik hissi**.
Analizde ozellikle sunlara bakilacak:

- Kare basina kac ayri gorsel oge var (yogunluk sayimi)
- Ekranin yuzde kaci "bos" (koyu, olaysiz alan)
- Ayni anda kac farkli renk goruluyor
- Saniyede kac gorsel olay oluyor (parlama, patlama, yazi, gecis)

Bu dort sayiyi kendi videomuzla karsilastirinca farkin nerede oldugu
sayisal olarak ortaya cikar.
