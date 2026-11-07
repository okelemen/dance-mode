"""Kapakta ana siluetin boyu (Masaustu CLAUDE.md md. 21, 5 Kas 2026 kullanici: "bizimkiler kucuk kaliyor").
Kapak 1280x720'ye indirilir, en buyuk koyu (siyah) bilesen ana siluet sayilir: yukseklik %, genislik %, alan %.
Bizim kapakta siluet boyu referansinkinin altinda kalmaz (yukseklik ve alan >= referansinki; 5 Kas 2026: siluet referanstaki boyutta, kucuk kalmaz).

    python kapak-siluet-olc.py --ref ref.jpg --biz A.jpg B.jpg
"""
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage


def olc(yol):
    a = np.asarray(Image.open(yol).convert("RGB").resize((1280, 720))).astype(int)
    # siluetler beyaz konturlu: koyu gece gogu siluetle birlesmesin diye yalniz beyaz konturun ICINDEKI koyu piksel sayilir
    beyaz = ndimage.binary_dilation(a.min(2) > 215, iterations=2)
    # 19. kapak: ayak alt kenara basinca kontur altta acik kaliyordu -> alt kenar kontur sayilir
    kapali = beyaz.copy(); kapali[-3:, :] = True
    # 21. kapak: genis poz yan kenara degince kontur orada acik kaliyordu -> yan kenarlar da kontur sayilir
    kapali[:, :3] = True; kapali[:, -3:] = True
    m = (a.max(2) < 60) & ndimage.binary_fill_holes(kapali) & ~beyaz
    lab, n = ndimage.label(m)
    if n == 0:
        return None
    s = ndimage.sum(m, lab, range(1, n + 1))
    # ikili/uclu kapakta birden cok figur var: %0,4'ten buyuk butun parcalar birlikte siluet sayilir
    buyuk = [i + 1 for i in range(n) if s[i] > 0.004 * 1280 * 720]
    if not buyuk:
        return None
    yy, xx = np.where(np.isin(lab, buyuk))
    return {"yuk": (yy.max() - yy.min()) / 7.2, "gen": (xx.max() - xx.min()) / 12.8, "alan": len(yy) / 9216}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ref", required=True)
    p.add_argument("--biz", nargs="*", default=[])
    g = p.parse_args()
    r = olc(g.ref)
    if r is None:
        raise SystemExit(f"{g.ref}: beyaz konturlu siluet bulunamadi, elle olc")
    print(f"REF  {g.ref}: yukseklik %{r['yuk']:.1f}  genislik %{r['gen']:.1f}  alan %{r['alan']:.1f}")
    kotu = 0
    for y in g.biz:
        b = olc(y)
        if b is None:
            print(f"YOK   {y}: beyaz konturlu siluet bulunamadi")
            kotu += 1
            continue
        ok = b["yuk"] >= r["yuk"] and b["alan"] >= r["alan"]
        kotu += not ok
        print(f"{'TAMAM' if ok else 'KUCUK'} {y}: yukseklik %{b['yuk']:.1f}  genislik %{b['gen']:.1f}  alan %{b['alan']:.1f}")
    raise SystemExit(1 if kotu else 0)
