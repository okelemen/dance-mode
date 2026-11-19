"""HUMAN TETRIS 33: kapak A/B'yi verilen arka planlarla kurar, olcer (kapak-olc / kapak-siluet-olc) ve REF | A | B sayfasini
(1280 + 320x180 telefon boyu) yazar.   python kapak-33-hepsi.py varlik-33-kapak-p0 varlik-33-kapak-m3"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
T = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\kapak-taslak\33"
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR\REF-085-HumanWarmUp-bgFolOzkqxM\kapak.jpg"
AYAR = {"A": ["--siluet", "D259886", "D255536", "--x", "0.2", "0.8", "--boy", "0.9", "0.9", "--tasma", "0.15"],
        "B": ["--siluet", "S1220742", "D259887", "--x", "0.18", "0.81", "--boy", "0.92", "0.9", "--maks-gen", "0.44", "--tasma", "0.15"]}
py = sys.executable
for arka in sys.argv[1:]:
    for k, ek in AYAR.items():
        c = os.path.join(T, "%s-%s.jpg" % (k, arka.split("kapak-")[-1]))
        out = subprocess.run([py, os.path.join(BURA, "kapak-pvp-33.py"), *ek, "--arka", arka, "--cikti", c], capture_output=True, text=True, encoding="utf-8").stdout
        print("==", os.path.basename(c)); print("\n".join(l for l in out.splitlines() if "cakisma" in l or "kontrast" in l))
r = subprocess.run([py, os.path.join(BURA, "kapak-olc.py"), "--ref", REF, "--biz", *[os.path.join(T, f) for f in sorted(os.listdir(T)) if f[:2] in ("A-", "B-")]],
                   capture_output=True, text=True, encoding="utf-8").stdout
print("\n".join(l for l in r.splitlines() if any(w in l for w in ("doygunluk", "parlaklik", "renklilik", "|  ", "biz", "A-", "B-"))))
for f in sorted(os.listdir(T)):
    if f[:2] in ("A-", "B-"):
        s = subprocess.run([py, os.path.join(BURA, "kapak-siluet-olc.py"), "--ref", REF, "--biz", os.path.join(T, f)], capture_output=True, text=True, encoding="utf-8").stdout
        print(f, [l for l in s.splitlines() if l.strip()][-1])
