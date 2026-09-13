# Neon Party Pulse — ölçüm ve hazırlık (13 Eylül 2026)

Kaynak: `Neon Party Pulse.mp3` (masaüstünden alındı, 4,69 MB, 184 kbps,
48 kHz stereo, **203,000 sn**). Kopya: `01-muzik/neon-party-pulse.mp3` +
`neon-party-pulse.wav`.

## BPM — dört yöntem, ikisi yanlış

| Yöntem | Sonuç |
|---|---|
| `analiz-bpm.py` (enerji tepeleri) | 135,92 |
| Otokorelasyon (`bpm_acf`) | 135,80 — 2x/3x/4x katları ±10 ms tutarlı |
| Tarak / comb | 136,65 ❌ |
| Faz eğimi | 138,04 ❌ |
| **Vuruş izleme + doğrusal oturtma** | **135,961** ✅ |

Tarak ve eğim yöntemleri 203 saniyede 1,3 sn ayrışıyordu, yani biri yanlıştı.
Hakem yöntem vuruşları tek tek izleyip eşleşen (indeks, zaman) çiftlerine doğru
oturtuyor; beş turda 135,977 → 135,960'a yakınsadı, kalıntı sapması 20 ms'ye
indi. **Kendi kendini doğruladı:** bu BPM'de 203,000 sn tam **115,000 ölçü**
ediyor. Betik: `03-motor/olc-tempo-kayma.py` (kayma testi) + ölçüm notları.

**Ölçü süresi: 1,7652 sn · ilk vuruş: 3,6120 sn**

## Tempo sabit mi? — evet, ölçüldü

`analiz-bpm.py` dilim dilim 133,99 → 136,59 gösteriyordu; şehir bölümündeki
kayma tuzağı akla geldiği için ikinci yöntemle bakıldı. Sabit ızgaranın faz
hatası parça boyunca **+28 ms** birikiyor (bir vuruş 439 ms). Yani tempo sabit;
dilim farkları ölçüm penceresi kaynaklıymış. Sabit ızgara tutuyor.

## Izgara kayması — yakalanan tuzak

İlk vuruş 3,6120 sn, ölçü 1,7652 sn → ızgara dosya başından **0,0816 sn kaymış**.
`muzik-uzat.py` ölçüleri t=0'dan sayıyordu; olduğu gibi çalıştırılsaydı her
ekleme noktası 82 ms off-beat olacak ve montajda tökezleme bırakacaktı.
Betiğe **isteğe bağlı ofset** eklendi (varsayılan 0 — eski çağrılar bit bit aynı).

## Uzatma

`python muzik-uzat.py ../01-muzik/neon-party-pulse.wav ../01-muzik/neon-party-pulse-298olcu.wav 135.961 114 298 0.0816`

- Kaynak ofset sonrası 114,954 ölçü → tam **114** ölçü kullanıldı.
- Giriş 16 + gövde (16–98 arası, 82 ölçü) ×3 + 20 ölçü + çıkış 16 = **298 ölçü**
- Çıktı: `01-muzik/neon-party-pulse-298olcu.wav` — **526,033 sn = 298,000 ölçü**

## Doğrulama

- Uzatılmış dosya yeniden izlendi: **135,988 BPM**, 526 sn boyunca kayma yok,
  kalıntı 23 ms. Ekleme noktaları ızgarayı bozmamış.
- Ekleme noktalarında **çıtlama yok**: ölçü 16/98/180/262/282'de yerel en büyük
  örnek atlaması 0,10–0,56; parçanın kendi en büyük atlaması 0,56.

## Süre kararı

**SÜRE KURALI DEĞİŞTİ (13 Eylül 2026, kullanıcı):** video uzunluğu artık
**9:30 – 10:30** arası. Eski kural "hedef 8:48 = 528,000 sn" idi (yayınlanan
ilk bölümün süresinden geliyordu) ve artık geçersiz. İlk hesap 8:46 çıkarmıştı;
o eski kurala göreydi.

Bu BPM'de (ölçü 1,7652 sn) aralığa giren ve blok matematiği tutan adaylar —
öğretme 26 ölçü, kalan 8'e bölünmeli:

| Ölçü | Süre | Kalan | Örnek bölünme |
|---|---|---|---|
| **330** | **9:42,5** | 304 | 16 çalışma + 6 mola |
| 338 | 9:56,6 | 312 | 17 çalışma + 5 mola |
| 346 | 10:10,8 | 320 | 17 çalışma + 6 mola |
| 354 | 10:24,9 | 328 | 18 çalışma + 5 mola |

**Seçilen: 330 ölçü = 582,520 sn = 9:42,5.** Gerekçe: aralığın içindeki en kısa
geçerli aday, yani müzik gövdesinin tekrar sayısı en az olan.

## Uzatma (güncel)

`python muzik-uzat.py ../01-muzik/neon-party-pulse.wav ../01-muzik/neon-party-pulse-330olcu.wav 135.961 114 330 0.0816`

- Giriş 16 + gövde (16–98, 82 ölçü) ×3 + 52 ölçü + çıkış 16 = **330 ölçü**
- Çıktı: `01-muzik/neon-party-pulse-330olcu.wav` — **582,520 sn = 330,000 ölçü**

## Doğrulama (güncel)

- Uzatılmış dosya yeniden izlendi: **135,984 BPM**, 9:42 boyunca kayma yok,
  kalıntı 23 ms.
- Ekleme noktaları (ölçü 16/98/180/262/314) **çıtlamasız**: yerel en büyük örnek
  atlaması 0,10–0,63; parçanın kendi maksimumu 0,63.

## AÇIK — tekrar riski

Gövde 82 ölçü (≈2:25) ve **üç tam kez + 52 ölçü** tekrar ediyor. Bölüm-05'te
gövde BİR kez tekrar ederken bile "~4,5 dk'dan sonra tanıdık geliyor" notu
düşülmüştü. 203 saniyelik bir kaynağı 9:42'ye çıkarmanın başka yolu yok.
Seçenekler: (a) böyle bırak, (b) ikinci bir parça verilsin ve bölüm ikiye
bölünsün, (c) daha uzun bir kaynak parça.
