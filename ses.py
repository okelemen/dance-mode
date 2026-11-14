"""KESIM SAYACI - ses: meyve kesimi ve tahta darbesi ayri kayitlardan.

python ses.py --plan plan-avokado.json --cikti ses/avokado.wav
Meyve: KaleidacousticsAudio, "Chopping fruit_Short.wav", Freesound 627197, CC0 (hq mp3 preview).
Tahta: Mixkit #136 "Cutting hard vegetables with knife", Mixkit Free License.
Yatay (z) kesimde tahtaya vurus yok, yalniz meyve kesimi.
"""
import argparse
import json
import subprocess

import numpy as np

SR = 48000
KAYNAK = "ses/mixkit-136.wav"
MEYVE_KAYNAK = "ses/chopping-fruit-CC0-627197.mp3"
VURUS = [2.25, 4.66, 5.64, 6.96, 7.96, 9.56]                       # tahtaya vurus baslangiclari (sn)
KESME = [(0.12, 0.80), (3.28, 3.80), (6.42, 6.92), (7.62, 7.92), (8.90, 9.50)]  # kesme hisirtisi
TAHTA_UST = 0.14


def yukle(yol):
    ham = subprocess.run(["ffmpeg", "-v", "error", "-i", yol, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(ham, np.float32).astype(np.float64)


def yaz(yol, st):
    st = np.clip(st, -1, 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", yol],
                   input=st.astype(np.float32).tobytes(), check=True)


def parca(x, a, b):
    p = x[int(a * SR):int(b * SR)].copy()
    return p / (np.abs(p).max() + 1e-9)


def sar(p, giris=0.004, cikis=0.012):
    n = len(p)
    gi, ci = min(int(giris * SR), n // 2), min(int(cikis * SR), n // 2)
    if gi:
        p[:gi] *= np.linspace(0, 1, gi)
    if ci:
        p[-ci:] *= np.linspace(1, 0, ci)
    return p


def yumusat(p, alt=90, ust=2500):
    """Mikrofon hissini ve gereksiz pes patlamayi yumusak gecisle azalt."""
    pad = 4096
    f = np.fft.rfftfreq(len(p) + 2 * pad, 1 / SR)
    hp = np.clip((f - alt) / alt, 0, 1)
    lp = np.clip((ust * 1.5 - f) / (ust * 0.5), 0, 1)
    buf = np.pad(p, (pad, pad))
    return np.fft.irfft(np.fft.rfft(buf) * np.minimum(hp, lp), n=len(buf))[pad:-pad]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--onaysiz-ses-denemesi", action="store_true",
                    help="Kullanici tarafindan reddedilen eski ses karisimini yalniz karsilastirma icin uret")
    a = ap.parse_args()
    if not a.onaysiz_ses_denemesi:
        ap.error("Avokado ses paketi reddedildi. Yayin icin onayli bagimsiz Foley kaydi gerekli.")
    P = json.load(open(a.plan, encoding="utf-8"))
    R = P["sekil"]["R"]
    MERKEZ_Z = TAHTA_UST + R - 0.03
    x = yukle(KAYNAK)
    meyve_kaydi = yukle(MEYVE_KAYNAK)
    rng = np.random.default_rng(5)
    N = int(P["sure"] * SR)
    sol, sag = np.zeros(N + SR), np.zeros(N + SR)

    def ekle(sinyal, t, g, pan):
        i = int(round(t * SR))
        if i < 0:
            sinyal = sinyal[-i:]
            i = 0
        n = min(len(sinyal), len(sol) - i)
        sol[i:i + n] += sinyal[:n] * g * (1 - pan)
        sag[i:i + n] += sinyal[:n] * g * (1 + pan)

    # CC0 kaydin 1.84-2.15 sn bolumu kisa meyve kesimi; ilk kaydin tislama veren bolumleri kullanilmaz.
    # Mixkit kaydindaki kisa darbe yalniz tahtaya inis icindir, meyve kesimi icin kullanilmaz.
    kesme = yumusat(sar(parca(meyve_kaydi, 1.84, 2.15), 0.008, 0.06), 90, 3500)
    tahta = [yumusat(sar(parca(x, h - 0.03, h + 0.11), 0.003, 0.05), 120, 5000)
             for h in (4.66, 6.96)]
    for tur in P["turlar"]:
        for t, eks, konum, adet in tur["vuruslar"]:
            pan = rng.uniform(-0.1, 0.1)
            g = rng.uniform(0.85, 1.0) * (1.0 if adet == 1 else 1.05)
            ekle(kesme, t - 0.23, g * 0.70, pan)
            if eks != "z":
                ekle(tahta[rng.integers(len(tahta))], t - 0.02, g * 0.52, pan)
    # yeni meyve tahtaya duser (sahne.py DUSUS_ANAHTAR: temas 0.30 sn, sekme inisi 0.53 sn): tok + yumusak pof
    tok = yukle("ses/dusus_tok.wav")
    pof = yukle("ses/dusus_pof.wav")
    for tur in P["turlar"]:
        ekle(tok, tur["bas"] + 0.30, 1.0, 0.0)
        ekle(pof, tur["bas"] + 0.30, 0.8, 0.0)
        ekle(tok, tur["bas"] + 0.53, 0.35, 0.0)
    st = np.stack([sol[:N], sag[:N]], 1)
    st *= 10 ** (-1.5 / 20) / np.abs(st).max()
    yaz(a.cikti, st)
    print("ses yazildi", a.cikti, N / SR, "sn")
