"""Tempo sabitlenmis (muzik-sabitle.py) parcayi bolum suresine OLCU IZGARASINDAN keserek dizer (yerel ses hazirlama).

    python muzik-diz-izgara.py <muzik.wav> <bolum.json> <cikti.wav> --ilk 0.4013 --plan "0-88,8-88,8-88,8-88,77-91"

muzik-duzen.py ekleri en guclu onset'e oturtuyordu; Starlight Sprint'te bu snare/ara vuruslara kayip +-100 ms sapma
yapti (18 Eki 2026 olcumu). Parca sabit tempoda oldugu icin kesim noktasi hesapla bulunur: ilk + olcu * (60/BPM*4).
Her kesim olcu cizgisinden 30 ms once, 20 ms esit-guc gecisle (yeni parcanin kick'i bozulmaz). Toplam olcu = bolum.
"""
import json, sys
import numpy as np
import soundfile as sf

m_yol, b_yol, cikti = sys.argv[1:4]
arg = lambda ad: sys.argv[sys.argv.index(ad) + 1]
B = json.load(open(b_yol, encoding="utf-8"))
ILK = float(arg("--ilk"))
PLAN = [tuple(float(v) for v in p.split("-")) for p in arg("--plan").split(",")]
x, sr = sf.read(m_yol, dtype="float32", always_2d=True)
OLCU = 60 / B["bpm"] * 4
toplam = sum(b - a for a, b in PLAN)
assert abs(toplam - B["toplam_olcu"]) < 1e-6, (toplam, B["toplam_olcu"])
ON, XF = int(0.030 * sr), int(0.020 * sr)

parca = []
for a, b in PLAN:
    s = int((ILK + a * OLCU) * sr) - ON
    e = int((ILK + b * OLCU) * sr) - ON
    parca.append(x[max(0, s):e + XF])
out = parca[0].copy()
for p in parca[1:]:
    t = np.linspace(0, np.pi / 2, XF)[:, None]
    out[-XF:] = out[-XF:] * np.cos(t) + p[:XF] * np.sin(t)
    out = np.concatenate([out, p[XF:]])
hedef = int(B["toplam_olcu"] * OLCU * sr)
out = out[ON:ON + hedef]
if len(out) < hedef:
    out = np.concatenate([out, np.zeros((hedef - len(out), out.shape[1]), dtype=out.dtype)])
f = int(0.6 * sr); out[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(cikti, out, sr)
print(f"-> {cikti}  {len(out) / sr:.2f} sn (hedef {hedef / sr:.2f}), plan {PLAN}")
