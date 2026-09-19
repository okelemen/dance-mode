# Maximum Energy — ölçüm notu (19 Eylül 2026)

Kaynak: `Masaüstü/Maximum Energy.mp3` (Suno, REF-043 prompt'u: 140 BPM istendi). Kopya: `01-muzik/maximum-energy.mp3`.
Süre 161,16 sn.

| | |
|---|---|
| **BPM** | **142,25** (hi-hat bandı tarak + sabit ızgara faz testi; hakem betiği 142,28) |
| İlk vuruş | 0,0117 sn · ölçü başı = vuruş 0 (kick 1'de, snare 3'te) |
| Drop | **27,006 sn** (vuruş 64 = 16. ölçü başı), RMS −19 → −13 dB |
| Tempo | **0–90 sn SABİT** (faz ±20 ms). **90–130 sn arası hızlanıyor**: sabit 142,25 ızgarasında −550 ms birikme (yerel ~144 BPM); 135 sn sonrası dağınık |

## Yöntem notu
- `muzik-tempo-duzelt.py` bu parçada YANLIŞ ölçtü (kick zarfı 132–136 verdi) ve parçayı
  %5 hızlandırdı → çıktı silindi. Trap/halftime'da kick düzensiz; ölçüt **hi-hat bandı (5–11 kHz)**.
- librosa beat_track 143,55 verdi (ızgara çözünürlüğü artefaktı), kullanılmadı.

## Kullanım
- Kesit: `maximum-energy-142-kesit50.wav` = 27,006 sn'den 36 ölçü + drop'un 8–21. ölçüleri (14) = 50 ölçü, 84,35 sn.
- **Tam bölüme YETMEZ:** 2:41 ve ikinci yarısı kayıyor. Tam bölüm için ya Suno'da Extend edilip
  yeniden ölçülür ya da yalnız 27–88 sn'lik sabit gövde döngülenir (muzik-uzat.py).
