"""Kapak OLCUMU — referans kapaklar ile bizim taslaklari ayni sayilarla karsilastirir (CLAUDE.md md. 21).

    python kapak-olc.py --ref ref1.jpg ref2.jpg ... --biz A.jpg B.jpg [--rapor rapor.md]

Olculenler (1280x720'ye olceklenmis goruntu uzerinde):
  doygunluk   ortalama HSV S (0-1)                 renklilik (Hasler-Susstrunk M)
  parlaklik   ortalama HSV V (0-1)                 kontrast  luminans std (0-1)
  ayrinti     kenar yogunlugu: Sobel > esik orani  siyah     V<0,12 piksel orani (siluet/golge kutlesi)
  beyaz       V>0,92 ve S<0,15 orani (kontur/yazi) baslik    ust %25 banttaki doygun+kenarli piksel orani
  sicak       kirmizi-turuncu-sari tonlarin orani  palet     6 baskin renk (k-means)
"""
import argparse, colorsys
import numpy as np
from PIL import Image

W, H = 1280, 720


def oku(yol):
    im = Image.open(yol).convert("RGB")
    # YouTube maxres'te ust/alt siyah bant olabilir (4:3 sd): 16:9 icerige kirp
    a = np.asarray(im).astype(np.float32) / 255
    satir = a.mean(axis=(1, 2)); sutun = a.mean(axis=(0, 2))
    y = np.where(satir > 0.02)[0]; x = np.where(sutun > 0.02)[0]
    if len(y) and len(x):
        im = im.crop((x[0], y[0], x[-1] + 1, y[-1] + 1))
    return np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255


def hsv(a):
    mx = a.max(axis=2); mn = a.min(axis=2)
    v = mx; s = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    return h, s, v


def sobel(l):
    gx = np.zeros_like(l); gy = np.zeros_like(l)
    gx[:, 1:-1] = l[:, 2:] - l[:, :-2]; gy[1:-1, :] = l[2:, :] - l[:-2, :]
    return np.hypot(gx, gy)


def palet(a, k=6, it=12):
    x = a.reshape(-1, 3)[::37]
    rng = np.random.default_rng(1); c = x[rng.choice(len(x), k, replace=False)]
    for _ in range(it):
        lab = np.argmin(((x[:, None] - c[None]) ** 2).sum(2), 1)
        c = np.array([x[lab == i].mean(0) if (lab == i).any() else c[i] for i in range(k)])
    pay = np.bincount(lab, minlength=k) / len(lab)
    sira = np.argsort(-pay)
    return [("#%02x%02x%02x" % tuple(int(v * 255) for v in c[i]), round(float(pay[i]) * 100)) for i in sira]


def olc(yol):
    a = oku(yol); h, s, v = hsv(a)
    l = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    rg = a[..., 0] - a[..., 1]; yb = 0.5 * (a[..., 0] + a[..., 1]) - a[..., 2]
    renk = np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    e = sobel(l) > 0.12
    ust = slice(0, int(H * 0.25))
    baslik = ((s[ust] > 0.45) & (v[ust] > 0.55) | e[ust]).mean()
    sicak = ((s > 0.35) & (v > 0.35) & ((h < 0.17) | (h > 0.95))).mean()
    return {"doygunluk": s.mean(), "parlaklik": v.mean(), "kontrast": l.std(), "renklilik": renk,
            "ayrinti": e.mean(), "siyah": (v < 0.12).mean(), "beyaz": ((v > 0.92) & (s < 0.15)).mean(),
            "baslik": baslik, "sicak": sicak, "palet": palet(a)}


ALAN = ["doygunluk", "parlaklik", "kontrast", "renklilik", "ayrinti", "siyah", "beyaz", "baslik", "sicak"]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ref", nargs="+", required=True)
    p.add_argument("--biz", nargs="*", default=[])
    p.add_argument("--rapor")
    a = p.parse_args()
    R = [olc(f) for f in a.ref]
    ort = {k: float(np.mean([r[k] for r in R])) for k in ALAN}
    sd = {k: float(np.std([r[k] for r in R])) for k in ALAN}
    satir = ["| ölçü | referans ort. (±sd) | " + " | ".join(f"biz: {f.split('/')[-1].split(chr(92))[-1]}" for f in a.biz) + " |",
             "|---|---|" + "---|" * len(a.biz)]
    B = [olc(f) for f in a.biz]
    for k in ALAN:
        hucre = []
        for b in B:
            fark = (b[k] - ort[k]) / (sd[k] + 1e-6)
            isaret = "✓" if abs(fark) <= 1 else ("▲" if fark > 0 else "▼")
            hucre.append(f"{b[k]:.3f} ({fark:+.1f}σ {isaret})")
        satir.append(f"| {k} | {ort[k]:.3f} (±{sd[k]:.3f}) | " + " | ".join(hucre) + " |")
    pal = {}
    for r in R:
        for c, pay in r["palet"][:3]:
            pal[c] = pal.get(c, 0) + pay
    metin = "\n".join(satir)
    metin += "\n\nReferans baskın renkler (ilk 3, kapak başına): " + ", ".join(
        " ".join(c for c, _ in r["palet"][:3]) for r in R[:8]) + " …"
    for f, b in zip(a.biz, B):
        metin += f"\n{f.split(chr(92))[-1].split('/')[-1]} palet: " + ", ".join(f"{c} %{p}" for c, p in b["palet"])
    print(metin)
    if a.rapor:
        open(a.rapor, "w", encoding="utf-8").write(metin + "\n")
