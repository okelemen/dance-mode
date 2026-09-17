# Golden Groove — ölçüm notu (17 Eylül 2026)

Kaynak: `Masaüstü/suno müzik/Golden Groove.mp3` (Suno, 130 BPM brief'iyle üretildi).
Süre 182,160 sn · 48 kHz stereo.
Kullanım: bölüm 09 BAL (MEK-004 petek).

## Sonuç

| | |
|---|---|
| **BPM** | **134,140** (Suno 130 istenmesine rağmen 134 verdi) |
| İlk vuruş | 0,410 sn → kırpıldı, `01-muzik/golden-groove-134.wav` |
| Tempo | **SABİT** — faz eğimi +0,0001 ms/sn, birikme yok |
| Ölçü süresi | 1,78916 sn |
| Parça | 101,58 ölçü |

## Dört yöntem, dört farklı sayı

| Yöntem | Betik | Sonuç |
|---|---|---|
| Tarak, tüm parça | `olc-tempo-kayma.py` | 135,250 |
| Otokorelasyon | `analiz-bpm.py` | 134,734 |
| İnce tarak taraması | `hizala.py` | 134,217 |
| Vuruş izleme + doğrusal oturtma | `olc-bpm-hakem.py` (bu iş için yazıldı) | 134,447 |
| **Faz eğimi sıfırlama** | bu notun altındaki yöntem | **134,140** |

## HAKEM YÖNTEM: faz eğimi sıfırlama

Soru "hangi sayı en güzel" değil, **"hangi ızgara 10 dakikada kaymaz"**.
Ölçüt doğrudan bu: sabit ızgara kurulur, parça 10 saniyelik pencerelere
bölünür, her pencerede kick'in ızgaraya göre ortalama faz hatası ölçülür ve
bu hataların **zamana göre eğimi** hesaplanır. Doğru BPM, eğimi sıfır yapan
BPM'dir — çünkü eğim = birikme hızı.

134,140'ta eğim +0,0001 ms/sn, en kötü pencere hatası 24 ms (bir vuruş 447 ms).

## Yanlış alarm: "parça hızlanıyor"

30 saniyelik pencerelerle yerel tempo taraması şunu verdi:

```
  15 sn: 133,56    45 sn: 134,01    75 sn: 134,25
 105 sn: 134,57   135 sn: 135,00   165 sn: 135,52
```

Düzenli bir hızlanma gibi duruyor (dakikada 0,65 BPM) ve tempo düzeltme aracı
yazıldı (`03-motor/muzik-tempo-duzelt.py`, dilim dilim `atempo`). Düzeltme
kaymayı 2,27 → 0,88 BPM'e indirdi ama **ikinci tur fayda etmedi (0,81)** —
yani kalan şey gürültüydü.

**Sabit ızgara faz testi hızlanmayı çürüttü:** ham parçada 134,30 ızgarasında
hata 0→180 sn boyunca ±24 ms bandında salınıyor, **birikme yok**. Pencereli
tarama yanılıyordu: parça ilerledikçe aranjman değişiyor (davul deseni,
ofbeat öğeler) ve pencere tepesi kayıyor.

**DERS:** tempo kaymasına pencereli tarak yöntemiyle karar verilmez. Karar
ölçütü sabit ızgaranın faz hatasının BİRİKMESİDİR. Bu yüzden parça
**esnetilmedi** — tını korundu.

## Tam bölüm için

134,140 BPM'de ölçü 1,78916 sn. Süre kuralı 570–630 sn:

| Ölçü | Süre | |
|---|---|---|
| 330 | 590,4 sn = 9:50,4 | ✔ |
| 336 | 601,2 sn = 10:01,2 | ✔ |
| 340 | 608,3 sn = 10:08,3 | ✔ |

Parça 101,58 ölçü olduğu için `muzik-uzat.py` ile uzatılacak (giriş bir kez,
gövde tekrar, çıkış bir kez; kesimler tam ölçü sınırında).
