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
SURE = 60.0  # kullanici: 1 dakikalik video

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
TURLAR = [(10, 3.4), (50, 7.4), (100, 8.2), (240, 8.3), (500, 8.8), (1000, 13.7)]  # 6 tur, 60 sn  # REF-080: 6 tur 10 -> 1000
ACILIS = 0.7  # yeni meyve yukaridan duser + seker
SONUC = 1.0
CIZGI_PAY = 0.6  # tur suresinin ilk %60'i kabukta cizgiler (z, y); son %40 soldan saga supurme (x)
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


def dilim_say(m, cx, cy, cz):
    """x dilimi basina (soldan saga) kup sayisi; toplam = kup_say."""
    A, R = m["A"], m["R"]
    xs = -A + (np.arange(cx + 1) + 0.5) * (2 * A / (cx + 1))
    ys = -R + (np.arange(cy + 1) + 0.5) * (2 * R / (cy + 1))
    zs = -R + (np.arange(cz + 1) + 0.5) * (2 * R / (cz + 1))
    Y, Z = np.meshgrid(ys, zs, indexing="ij")
    return np.array([int(icinde(np.full_like(Y, x), Y, Z, m).sum()) for x in xs])


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
        # REF-080 sirasi: once z (yatay) + y (kameraya dik halkalar) cizgileri, sonra x supurmesi soldan saga
        sira = [("z", j, cz) for j in range(1, cz + 1)] + [("y", j, cy) for j in range(1, cy + 1)]
        sira += [("x", j, cx) for j in range(1, cx + 1)]
        n_c = cz + cy
        for i, (eks, j, c) in enumerate(sira, 1):
            if i <= n_c:
                tt = kes_bas + tc * CIZGI_PAY * (i / n_c) ** US
            else:
                tt = kes_bas + tc * CIZGI_PAY + tc * (1 - CIZGI_PAY) * ((i - n_c) / cx) ** 0.85
            yar = m["A"] if eks == "x" else m["R"]
            if eks == "x":
                konum = -yar + j * 2 * yar / (c + 1)  # soldan (dar uc) saga
            else:
                konum = yar - j * 2 * yar / (c + 1)
            kesimler.append([round(tt, 4), eks, round(konum, 5), j])
        dilim = dilim_say(m, cx, cy, cz)
        turlar.append({
            "bas": round(bas, 4), "kes_bas": round(kes_bas, 4), "kes_son": round(kes_son, 4),
            "son": round(son, 4), "n": n, "cx": cx, "cy": cy, "cz": cz,
            "kup": int(dilim.sum()), "dilim": dilim.tolist(), "kesimler": kesimler,
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
