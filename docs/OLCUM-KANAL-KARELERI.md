# Altı kanal — kare ölçümü

> Ölçüm: 30 Ağustos 2026. Her kanalın **en çok izlenen** videosundan bir oynanış
> karesi. Kareler `docs/kanal-kareleri/` altında.

| Kanal | Medyan parlaklık | Siyah piksel | Parlak piksel | Doygunluk | Baskın tonlar |
|---|---:|---:|---:|---:|---|
| Prime & Prep | **0,708** | %0,1 | %61,7 | 0,39 | turuncu 30° (%62) |
| FLEM | 0,187 | %4,4 | %4,5 | 0,20 | pembe 330° (%44) |
| Dance Mode | 0,184 | %2,3 | %8,4 | 0,22 | magenta 300° (%55) |
| Escapify | 0,145 | %0,1 | %13,0 | **0,81** | mor 270° (%62) |
| Stay on Beat | 0,084 | %39,0 | %8,5 | 0,74 | cyan 180° (%45) |
| Beat Motion | **0,030** | %63,9 | %3,1 | 0,50 | **yeşil 90° (%57)** |

## Düzeltme: "koyu zemin" nişin kuralı değil

Daha önce ölçümü tek kanal (STAY ON BEAT) üzerinde yapmış ve "neon ancak siyahın
üstünde neon olur" sonucuna varmıştım. Altı kanala bakınca bu genelleme yanlış:

- Parlaklık **24 kat** aralıkta: 0,030 ile 0,708 arası.
- Sadece iki kanal karanlık (Stay on Beat, Beat Motion). Diğer dördünde siyah
  piksel oranı %5'in altında.
- Escapify'da **siyah yok** (%0,1) ve doygunluk 0,81 — her piksel doygun mor.
- Dance Mode doygunluğu **0,22** — neredeyse gri; magenta ışıkla yıkanmış beton.
  Ve medyanı en yüksek kanal o (396 B).

Doğru genelleme: **kazandıran şey karanlık değil, palet disiplini.** Altısında da
bir ya da iki ton kareyi domine ediyor, üçüncü bir aile neredeyse yok.

## Ölçülen paletlerden türetilen ortamlar

| Ortam | Kaynak | Ne alındı |
|---|---|---|
| `MAGENTA HALL` | Dance Mode | Zemin `#140f15`, magenta `#ff2fd0`, turuncu aksan `#ff8800`. Koyu değil — magenta ışıkla yıkanmış koridor. |
| `ACID LAB` | Beat Motion | Zemin saf siyah, yeşil `#bbff77` + turuncu `#dd7722` + koyu kırmızı `#882222`. Kütüphanenin en karanlık ortamı. |
| `VIOLET VOID` | Escapify | Zemin `#361256` — siyah yok. Mavi `#0055ff`, asit sarısı `#ccff00`, mor. Doygunluk sonuna kadar açık. |

Bu üçü kütüphanedeki boşlukları kapatıyor: elimizdeki 19 ortamın hepsi siyah
zeminliydi ve hiçbirinde yeşil/turuncu aile yoktu.

## Bizde olmayan öğeler

**İlerleme çubuğu** — Escapify, FLEM ve Prime & Prep'te var, bizde yok.
"Ne kadar kaldı" hissi tutma oranına doğrudan etki eder. Escapify ayrıca
mesafe sayacı gösteriyor (618 m).

**Tam ekran kartlar** — Prime & Prep oynanışı tamamen kapatan "GREAT" kartı
kullanıyor. Biz bunun tersini yaptık (övgüleri üst banda taşıdık); hangisinin
doğru olduğu ölçülmedi.
