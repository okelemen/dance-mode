"""KESIM SAYACI - zaman plani.

Tek dogruluk kaynagi: Blender sahnesi (sahne.py), yazi katmani (hud.py) ve ses (ses.py)
hepsi bu dosyanin urettigi plan JSON'unu okur. Kup sayilari burada geometriden hesaplanir.

Kullanim: python plan.py --meyve avokado --cikti plan-avokado.json
"""
import argparse
import json
import math

import numpy as np

FPS = 30
SURE = 60.0

# Meyve sekli: x ekseni boyunca yatan donel govde. r(xn) = Rmax * f(xn)/fmax
MEYVELER = {
    "avokado": {
        "A": 1.15,      # yarim boy (x)
        "R": 0.78,      # en genis yaricap
        "boyun": 0.55,  # dar uc / genis uc orani
        "cekirdek": {"x": 0.28, "r": 0.40},  # x: A'ya oranla merkez, r: R'ye oranla yaricap
    }
}

# Turlar: (kesim sayisi, kesim suresi sn). Acilis 0.4 sn + sonuc 1.3 sn eklenir -> toplam 60 sn
TURLAR = [(6, 2.8), (50, 6.2), (150, 9.0), (400, 12.0), (1000, 18.0)]  # kural: kucukten (6) 1000'e
ACILIS = 0.4
SONUC = 2.0
US = 0.7  # kesim hizlanma ussu (<1 = hizlanir)


def profil(xn, boyun):
    xn = np.clip(xn, -1.0, 1.0)
    s = (xn + 1.0) / 2.0
    return np.sqrt(np.maximum(0.0, 1.0 - xn * xn)) * (boyun + (1.0 - boyun) * s)


def fmax(boyun):
    xs = np.linspace(-1, 1, 20001)
    return float(profil(xs, boyun).max())


def icinde(x, y, z, m):
    """Meyvenin merkezine gore (x,y,z) noktasi govdenin icinde mi."""
    fm = fmax(m["boyun"])
    xn = x / m["A"]
    rr = m["R"] * profil(xn, m["boyun"]) / fm
    return (np.abs(xn) <= 1.0) & (y * y + z * z <= rr * rr)


def eksen_bol(n):
    cx = math.ceil(n / 3)
    cy = math.ceil((n - cx) / 2)
    cz = n - cx - cy
    return cx, cy, cz


def kup_say(m, cx, cy, cz):
    """Kesimlerle olusan hucrelerden merkezi meyvenin icinde kalanlar = kup sayisi."""
    A, R = m["A"], m["R"]
    xs = -A + (np.arange(cx + 1) + 0.5) * (2 * A / (cx + 1))
    ys = -R + (np.arange(cy + 1) + 0.5) * (2 * R / (cy + 1))
    zs = -R + (np.arange(cz + 1) + 0.5) * (2 * R / (cz + 1))
    say = 0
    Y, Z = np.meshgrid(ys, zs, indexing="ij")
    for x in xs:  # bellek dostu: x dilim dilim
        say += int(icinde(np.full_like(Y, x), Y, Z, m).sum())
    return say


def plan_kur(meyve):
    m = MEYVELER[meyve]
    turlar = []
    t = 0.0
    for n, tc in TURLAR:
        cx, cy, cz = eksen_bol(n)
        bas = t
        kes_bas = bas + ACILIS
        kes_son = kes_bas + tc
        son = kes_son + SONUC
        kesimler = []
        for i in range(1, n + 1):
            tt = kes_bas + tc * (i / n) ** US
            if i <= cx:
                eks, j, c = "x", i, cx
            elif i <= cx + cy:
                eks, j, c = "y", i - cx, cy
            else:
                eks, j, c = "z", i - cx - cy, cz
            # kesim duzlemi: sagdan sola / arkadan one / ustten alta
            yar = m["A"] if eks == "x" else m["R"]
            konum = yar - j * 2 * yar / (c + 1)
            kesimler.append([round(tt, 4), eks, round(konum, 5), j])
        turlar.append({
            "bas": round(bas, 4), "kes_bas": round(kes_bas, 4), "kes_son": round(kes_son, 4),
            "son": round(son, 4), "n": n, "cx": cx, "cy": cy, "cz": cz,
            "kup": kup_say(m, cx, cy, cz), "kesimler": kesimler,
        })
        t = son
    assert abs(t - SURE) < 1e-6, t
    return {"meyve": meyve, "fps": FPS, "sure": SURE, "kare": int(SURE * FPS), "sekil": m,
            "fmax": fmax(m["boyun"]), "turlar": turlar}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--meyve", default="avokado")
    ap.add_argument("--cikti", required=True)
    a = ap.parse_args()
    p = plan_kur(a.meyve)
    with open(a.cikti, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False)
    for tr in p["turlar"]:
        print(f"tur {tr['bas']:5.1f}-{tr['son']:5.1f}s  kesim {tr['n']:4d}  ({tr['cx']},{tr['cy']},{tr['cz']})  kup {tr['kup']:,}")
