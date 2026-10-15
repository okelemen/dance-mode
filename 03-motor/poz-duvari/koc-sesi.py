"""POZ DUVARI - koc sesi (TTS) izi. GitHub Actions'ta kosar (koc-sesi.yml).

Bolum JSON'undaki "koc" cumlelerini Kokoro (kokoro-onnx, Apache-2.0) ile
okutur ve her birini kendi zamanina yerlestirir -> tek WAV (bolum uzunlugunda).
Kullanici karari (16 Eki 2026): koc sesi yapay ses (TTS). Ingilizce konusma
YouTube otomatik dublajinin calismasi icin sart (POZ-DUVARI/TALIMATLAR.md §3).

    python koc-sesi.py <bolum.json> <model.onnx> <voices.bin> <cikti.wav> [--ses am_michael] [--hiz 1.1]

Cakisma kurali: bir cumle bir sonrakinin baslangicina tasiyorsa once hizlanir
(en fazla 1.45); yine sigmiyorsa sonu kisa fade ile kesilir ve log'a yazilir.
Sayim (Three/Two/One), "Hold it!" ve ovgu kisa cumledir, zamani kaydirilmaz.
"""
import json, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro


def arg(ad, vars):
    return sys.argv[sys.argv.index(ad) + 1] if ad in sys.argv else vars


bolum_yol, model, sesler, cikti = sys.argv[1:5]
SES = arg("--ses", "am_michael")
HIZ = float(arg("--hiz", "1.1"))

B = json.load(open(bolum_yol, encoding="utf-8"))
OLCU = 60 / B["bpm"] * 4
SURE = B["toplam_olcu"] * OLCU
koc = sorted(B["koc"], key=lambda c: c["t"])

tts = Kokoro(model, sesler)
SR = 24000
iz = np.zeros(int(SURE * SR) + SR, dtype=np.float32)
log = []

for i, c in enumerate(koc):
    sonraki = koc[i + 1]["t"] if i + 1 < len(koc) else SURE
    pencere = max(0.3, sonraki - c["t"] - 0.08)
    hiz = HIZ
    while True:
        ses, sr = tts.create(c["metin"], voice=SES, speed=hiz, lang="en-us")
        assert sr == SR, sr
        # bastaki/sondaki sessizligi kirp (zamanlama vurgusu kelimenin kendisinde olsun)
        esik = 0.01 * np.max(np.abs(ses))
        idx = np.where(np.abs(ses) > esik)[0]
        if len(idx):
            ses = ses[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.06 * SR)]
        uzun = len(ses) / SR
        if uzun <= pencere or hiz >= 1.45 or c.get("kisa"):
            break
        hiz = min(1.45, hiz * pencere / uzun * 1.02 + 0.02)
    kesildi = False
    if uzun > pencere and not c.get("kisa"):
        n = int(pencere * SR)
        f = min(n, int(0.08 * SR))
        ses = ses[:n].copy()
        ses[-f:] *= np.linspace(1, 0, f)
        kesildi = True
    a = int(c["t"] * SR)
    iz[a:a + len(ses)] += ses[: len(iz) - a]
    log.append({"t": c["t"], "metin": c["metin"], "sn": round(len(ses) / SR, 2),
                "pencere": round(pencere, 2), "hiz": round(hiz, 2), "kesildi": kesildi})
    print(f"{c['t']:7.2f}  {len(ses)/SR:4.2f}/{pencere:4.2f} sn  hiz {hiz:.2f}{'  KESILDI' if kesildi else ''}  {c['metin']}")

iz = iz[: int(SURE * SR)]
tepe = np.max(np.abs(iz)) or 1
iz = iz / tepe * 0.89                     # -1 dBFS tepe
sf.write(cikti, iz, SR, subtype="PCM_16")
json.dump({"ses": SES, "hiz": HIZ, "sure": SURE, "cumleler": log},
          open(cikti.replace(".wav", "-log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"-> {cikti}  {SURE:.1f} sn  {len(log)} cumle  kesilen {sum(x['kesildi'] for x in log)}")
