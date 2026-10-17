"""TETRIS MODE PVP - ses efektleri (sentez, indirme/telif yok). Zamanlar bolum JSON'undan (sahne4.html ile ayni kaynak).

    python efekt.py <bolum.json> <cikti.wav> [--muzik muzik.wav [--muzik-kazanc 0.5]]

Kullanici (17 Eki 2026): "ses efekti kesinlikle olacak". Sentez fonksiyonlari poz-duvari/efekt.py'den.
Olaylar: VS carpismasi, tur fanfari, 3-2-1-GO bipleri, oyuncu karti pop, duvar sayimi, yaklasan vuus,
en yakinda vurus + gecis vuusu, ovgu piriltisi, kapanis fanfari, SUBSCRIBE tik.
"""
import json, os, sys
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poz-duvari"))
from efekt import SR, vuus, ding, bip, vurus, piril, zap, tik, fanfar, yerlestir  # noqa: E402


def main():
    bolum, cikti = sys.argv[1:3]
    B = json.load(open(bolum, encoding="utf-8"))
    Z = B["zaman"]
    sure = B["toplam_olcu"] * 60 / B["bpm"] * 4
    ef = np.zeros(int(sure * SR) + SR)
    for k in B["kartlar"]:
        t = k["t"]
        if k["tip"] == "vs":
            yerlestir(ef, vuus(0.7, True, 0.9), t)
            yerlestir(ef, vurus(), t + 0.45, 1.0)
            yerlestir(ef, zap(0.4), t + 0.5, 0.7)
        elif k["tip"] == "tur":
            yerlestir(ef, vuus(0.5, True, 0.6), t)
            yerlestir(ef, fanfar(), t + 0.15, 0.9)
        elif k["tip"] == "basla":
            for i in range(3):
                yerlestir(ef, bip(660, 0.18), t + i + 0.02, 0.9)
            yerlestir(ef, bip(1320, 0.4), t + 3.02, 1.0)
            yerlestir(ef, vurus(), t + 3.02, 0.8)
        elif k["tip"] == "wrap":
            yerlestir(ef, fanfar(1.2), t + 0.05, 1.0)
            yerlestir(ef, piril(0.8), t + 0.3, 0.8)
        elif k["tip"] == "abone":
            yerlestir(ef, ding(990, 0.25), t + 0.1, 0.6)
            yerlestir(ef, tik(), t + 1.2, 0.9)
            yerlestir(ef, ding(1760, 0.5), t + 1.25, 0.45)
    for d in B["duvarlar"]:
        t0 = d["t0"]
        a = t0 + Z["kart"]; b = a + Z["say"]; c = b + Z["buyu"]
        yerlestir(ef, ding(990, 0.2), t0 + 0.05, 0.5)                    # oyuncu kartlari pop
        yerlestir(ef, ding(), a + 0.02, 0.6)                             # poz belirdi
        for i in range(3):
            yerlestir(ef, bip([660, 784, 988][i]), a + i + 0.02, 0.9)    # 3-2-1 yukselen
        yerlestir(ef, vuus(Z["buyu"] * 0.6, True, 0.55), c - Z["buyu"] * 0.6)   # duvar yaklasiyor
        yerlestir(ef, vurus(), c - 0.05, 1.0)                            # en yakinda
        yerlestir(ef, vuus(0.6, False, 0.9), c)                          # icinden gecti
        yerlestir(ef, piril(), c + Z["gec"] * 0.35, 0.6)                 # ovgu
    # SUBSCRIBE hatirlatmasi (her ~15 sn, sahne4.html aboneCiz ile ayni zaman): giriste pop, 1,3 sn'de tik + zil
    for ta in B.get("abone", []):
        yerlestir(ef, ding(990, 0.2), ta + 0.05, 0.55)
        yerlestir(ef, tik(), ta + 1.3, 0.9)
        yerlestir(ef, ding(1760, 0.5), ta + 1.35, 0.5)
        yerlestir(ef, piril(0.5), ta + 1.4, 0.35)
    ef = ef[: int(sure * SR)]
    karisim = ef * 0.5
    if "--muzik" in sys.argv:
        m, msr = sf.read(sys.argv[sys.argv.index("--muzik") + 1], dtype="float32", always_2d=True)
        assert msr == SR, f"muzik {msr} Hz, {SR} bekleniyor"
        m = np.pad(m, ((0, max(0, len(ef) - len(m))), (0, 0)))[: len(ef)]
        mg = float(sys.argv[sys.argv.index("--muzik-kazanc") + 1]) if "--muzik-kazanc" in sys.argv else 0.5
        karisim = karisim[:, None] + m * mg
    karisim = karisim / (np.max(np.abs(karisim)) + 1e-9) * 0.89
    sf.write(cikti, karisim.astype(np.float32), SR, subtype="PCM_16")
    print(f"-> {cikti}  {sure:.1f} sn  {len(B['duvarlar'])} duvar, {len(B['kartlar'])} kart")


if __name__ == "__main__":
    main()
