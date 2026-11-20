"""Kapak siluet havuzu (gozlem 0017): kapakta kullanilmis id kumesi BUTUN 05-kapak/*.py betiklerindeki 6-7 haneli sayilar
+ VIDEO-GECMISI.md'deki S/D/K/O/Y onekli id'lerden turetilir; son kapagin id'leri kumede olmali (assert).
Kalan havuz numarali kontak sayfasi olur.  python siluet-havuz.py <NN> <son kapak id ...>"""
import glob, os, re, sys
from PIL import Image, ImageDraw, ImageFont
NN = sys.argv[1]; SON = sys.argv[2:]
KOK = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
GEC = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\VIDEO-GECMISI.md"
CIK = r"C:\Users\eleme\OneDrive\Masaüstü\POZ-DUVARI\kapak-taslak\%s" % NN
used = set()
for f in glob.glob(os.path.join(KOK, "*.py")):
    if os.path.basename(f) == "siluet-havuz.py": continue
    used |= set(re.findall(r"(?<!\d)(\d{6,7})(?!\d)", open(f, encoding="utf-8", errors="ignore").read()))
used |= set(re.findall(r"\b[SDKOY](\d{6,7})\b", open(GEC, encoding="utf-8").read()))
for s in SON: assert re.sub(r"\D", "", s) in used, s
KAYNAK = [("S", "SVGSILH-dans-siluet/png512", r"(\d+)\.png$"), ("D", "OC-dans-siluet/buyuk", r"(\d+)\.png$"),
          ("K", "OC-dans-siluet", r"(\d+)-2000\.png$"), ("Y", "OC-yoga-siluet", r"(\d+)-2000\.png$")]
havuz = []
for on, d, rx in KAYNAK:
    for f in sorted(glob.glob(os.path.join(REF, d, "*.png"))):
        m = re.search(rx, os.path.basename(f))
        if m and m.group(1) not in used: havuz.append((on + m.group(1), f))
print("kullanilmis", len(used), "havuz", len(havuz))
C, HC, S = 10, 230, 200
n = len(havuz); R = (n + C - 1) // C
sayfa = Image.new("RGB", (C * S, R * HC), "white"); dr = ImageDraw.Draw(sayfa); fn = ImageFont.truetype("arial.ttf", 16)
with open(os.path.join(CIK, "havuz-tum.txt"), "w", encoding="utf-8") as t:
    for i, (ad, f) in enumerate(havuz):
        im = Image.open(f).convert("RGBA"); bb = im.getbbox(); im = im.crop(bb) if bb else im
        im.thumbnail((S - 10, HC - 34)); x, y = (i % C) * S, (i // C) * HC
        bg = Image.new("RGBA", im.size, (225, 235, 245, 255)); bg.alpha_composite(im)
        sayfa.paste(bg.convert("RGB"), (x + (S - im.width) // 2, y + 26)); dr.text((x + 6, y + 4), "%d %s" % (i + 1, ad), fill="black", font=fn)
        t.write("%d\t%s\t%s\n" % (i + 1, ad, f))
sayfa.save(os.path.join(CIK, "havuz-tum.jpg"), quality=85); print(sayfa.size)
