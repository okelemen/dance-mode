"""TETRIS MODE PVP - kullanicinin Suno parcasini bolum suresine dizer (yerel ses hazirlama, md. 9 serbest).

    python muzik-duzen.py <muzik.wav> <bolum.json> <cikti.wav> [--ilk 0.4238]

Victory Rush (147,8 sn, 81 olcu, enerji hic dusmuyor, sonda sert durus): ilk vurus t=0'a cekilir; parca bir kez
tam (0-80), sonra govde (8-80) tekrarlanir, en son (son N olcu + orijinal bitis) ile kapanir. Ekleme noktalari olcu
basina en yakin GERCEK vurusa (onset tepe) oturtulur, 40 ms esit-guc gecisle birlestirilir (hakem BPM'de faz std
~56 ms; hesaplanan olcu noktasindan kesince vurus kayiyordu). Toplam = bolum suresi, son 0,6 sn yumusak.
"""
import json, sys
import numpy as np
import soundfile as sf

m_yol, b_yol, cikti = sys.argv[1:4]
B = json.load(open(b_yol, encoding="utf-8"))
ILK = float(sys.argv[sys.argv.index("--ilk") + 1]) if "--ilk" in sys.argv else 0.4238
x, sr = sf.read(m_yol, dtype="float32", always_2d=True)
OLCU = 60 / B["bpm"] * 4
hedef = int(B["toplam_olcu"] * OLCU * sr)

mono = x.mean(1)
hop = 256
e = np.array([np.sum(mono[i:i + 1024] ** 2) for i in range(0, len(mono) - 1024, hop)])
fark = np.maximum(0, np.diff(np.log(e + 1e-9), prepend=0))

def vurus(t, pen=0.08):
    """t civarindaki en guclu onset (ornek indeksi)"""
    a = max(0, int((t - pen) * sr / hop)); b = min(len(fark), int((t + pen) * sr / hop))
    return (a + int(np.argmax(fark[a:b]))) * hop

def olcu_ornek(k):
    return vurus(ILK + k * OLCU)

N_OLCU = int((len(mono) / sr - ILK) / OLCU)        # 81
GOVDE = 8
parcalar = [(olcu_ornek(0), olcu_ornek(N_OLCU - 1))]
toplam = N_OLCU - 1
while toplam + (N_OLCU - 1 - GOVDE) <= B["toplam_olcu"] - 4:
    parcalar.append((olcu_ornek(GOVDE), olcu_ornek(N_OLCU - 1)))
    toplam += N_OLCU - 1 - GOVDE
kalan = B["toplam_olcu"] - toplam
parcalar.append((olcu_ornek(N_OLCU - kalan), len(mono)))   # orijinal bitisle kapanis
print("parcalar (olcu):", [(round((a / sr - ILK) / OLCU, 2), round((b / sr - ILK) / OLCU, 2)) for a, b in parcalar], "kalan", kalan)

XF = int(0.04 * sr)
out = x[parcalar[0][0]:parcalar[0][1] + XF].copy()
for a, b in parcalar[1:]:
    seg = x[a:b + XF].copy()
    w = np.linspace(0, np.pi / 2, XF)[:, None]
    out[-XF:] = out[-XF:] * np.cos(w) + seg[:XF] * np.sin(w)
    out = np.concatenate([out, seg[XF:]])
out = out[:hedef] if len(out) >= hedef else np.pad(out, ((0, hedef - len(out)), (0, 0)))
fd = int(0.6 * sr); out[-fd:] *= np.linspace(1, 0, fd)[:, None]
sf.write(cikti, out, sr, subtype="PCM_24")
print(f"-> {cikti}  {len(out) / sr:.2f} sn (hedef {hedef / sr:.2f})")
