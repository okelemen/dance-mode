"""HUMAN TETRIS 26. video (poz-sec-25.py kopyasi; son 4 video = 22, 23 ikili, 24, 25; 17-25 adlari elenir; 24/25/26 kapak siluetleri yakinlik olcutunde).
HUMAN TETRIS 25. video (referanssiz, 1v1, 4 tur x 6 duvar = 24 duvar / 48 poz): poz-sec-24.py kopyasi.
25: son 4 video = 21, 22, 23 (ikili) + 24 (varlik-24s/poz); 17-24 adlari dogrudan elenir; 24 ve 25 kapak siluetleri de yakinlik olcutune girer.
24: son 4 video = 20, 21, 22 (tek kisilik maskeler) + 23 (ikili maskeler); 22'de kullanilan 40 ad dogrudan elenir (ad tekrari yok).
Kullanici 7 Kas 2026: "uygun silüet bulamadıysan öncekilerden harmanla ... ilk Tetris videolarından bulup onları yapabilirsin"
(yeni CC0 kaynak tukendi: Openclipart yeni aday ~3, svgsilh / publicdomainvectors 403, Wikimedia 429).
Havuz: ilk videolar (varlik = POSE WALL/TETRIS 1-2, varlik-03, varlik-04, varlik-05) tek kisilik maskeler.
Elenen: son videolarla (16, 17, 19, 20 + 20/21 kapak siluetleri) IoU >= 0,78 olanlar; havuz icinde IoU >= 0,70 ikizler (ilk gelen kalir);
adi havada / ters / ziplama okunanlar. Siralama: maske yuksekligi (ayakta -> yere yakin) -> EASY / NORMAL / HARD.
Cikti: aday-olcu-24.json (her adayin olcusu), konsola tablo."""
import glob, json, os, re
import numpy as np
from PIL import Image

BURA = os.path.dirname(os.path.abspath(__file__))
REF = r"C:\Users\eleme\OneDrive\Masaüstü\REFERANSLAR"
N = 128
ESIK_YAKIN, ESIK_IC = 0.78, 0.70
HAVUZ = ("varlik/poz", "varlik-03/poz", "varlik-04/poz", "varlik-05/poz")
YAKIN = ("varlik-22/poz", "varlik-23/grup", "varlik-24s/tetris-varlik/poz", "varlik-25-e13/tetris-varlik/poz")
YASAK = re.compile(r"jump|hop|leap|head-?stand|hand-?stand|cartwheel|wheel|flip|invert|upside|fly|air|dive|fall", re.I)


def maske(yol):
    im = np.array(Image.open(yol).convert("RGBA"))
    a = im[:, :, 3] > 40
    if a.mean() > 0.97:
        a = im[:, :, :3].mean(2) < 100
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = a.shape; s = max(h, w)
    kare = np.zeros((s, s), bool); kare[s - h:, (s - w) // 2:(s - w) // 2 + w] = a
    return np.array(Image.fromarray(kare.astype(np.uint8) * 255).resize((N, N), Image.BILINEAR)) > 127


def iou(a, b):
    return max((a & b).sum() / max(1, (a | b).sum()), (a & b[:, ::-1]).sum() / max(1, (a | b[:, ::-1]).sum()))


def boy(yol):
    """maske kutusunun cerceveye gore yuksekligi ve genisligi (900x740 cerceve; ayakta ~0,92)"""
    al = Image.open(yol).getchannel("A"); x0, y0, x1, y1 = al.getbbox()
    return (y1 - y0) / al.height, (x1 - x0) / al.width


yakin = {}
for d in YAKIN:
    for f in glob.glob(os.path.join(BURA, d, "*.png")):
        yakin[d + "/" + os.path.basename(f)] = maske(f)
for k in ("273073", "277859", "230147", "272052", "309217", "268844"):          # 20. kapak
    yakin["20-kapak/" + k] = maske(os.path.join(REF, "OC-dans-siluet", k + "-2000.png"))
for k in ("269945", "313361"):                                                  # 21. kapak A
    yakin["21-kapak/" + k] = maske(os.path.join(REF, "OC-dans-siluet", "buyuk", k + ".png"))
for k in ("291176", "259634"):                                                  # 21. kapak B
    yakin["21-kapak/" + k] = maske(os.path.join(REF, "OC-yoga-siluet", k + "-2000.png"))
for k in ("266208", "274664"):                                                  # 22. kapak (yoga)
    yakin["22-kapak/" + k] = maske(os.path.join(REF, "OC-yoga-siluet", k + "-2000.png"))
for k in ("268843",):
    yakin["22-kapak/" + k] = maske(os.path.join(REF, "OC-dans-siluet", "buyuk", k + ".png"))
yakin["22-kapak/285133"] = maske(os.path.join(REF, "OC-yoga-siluet", "285133-2000.png"))
n_yakin = sum(len(glob.glob(os.path.join(BURA, d, "*.png"))) for d in YAKIN)
for k in ("336199", "273074", "281291", "255374", "222008", "267319", "281290", "275917", "302308", "266681", "256953"):    # 24 + 25 kapak siluetleri (D / Y)
    for yol in (os.path.join(REF, "OC-dans-siluet", "buyuk", k + ".png"), os.path.join(REF, "OC-yoga-siluet", k + "-2000.png"), os.path.join(REF, "OC-dans-siluet", k + "-2000.png")):
        if os.path.exists(yol): yakin["kapak/" + k] = maske(yol)
yakin["kapak/309217"] = maske(os.path.join(REF, "OC-dans-siluet", "309217-2000.png"))
assert n_yakin > 100 and len(yakin) >= n_yakin + 18, (len(yakin), n_yakin)
KULLANILDI = {os.path.basename(f) for d in ("varlik-17/poz", "varlik-19/poz", "varlik-20/poz", "varlik-21/poz", "varlik-22/poz", "varlik-24s/tetris-varlik/poz", "varlik-25-e13/tetris-varlik/poz") for f in glob.glob(os.path.join(BURA, d, "*.png"))}
assert len(KULLANILDI) > 150, len(KULLANILDI)       # bos sayim = kirik komut

dosyalar = [f for d in HAVUZ for f in sorted(glob.glob(os.path.join(BURA, d, "*.png")))]
assert len(dosyalar) > 380, len(dosyalar)
secilen, olcu, elenen = [], {}, {"yasak": 0, "yakin": 0, "ikiz": 0}
for f in dosyalar:
    ad = os.path.relpath(f, BURA).replace("\\", "/")
    if YASAK.search(os.path.basename(f)):
        elenen["yasak"] += 1; continue
    if os.path.basename(f) in KULLANILDI:
        elenen.setdefault("ad", 0); elenen["ad"] += 1; continue
    m = maske(f)
    en, deg = max(((e, iou(m, v)) for e, v in yakin.items()), key=lambda x: x[1])
    if deg >= ESIK_YAKIN:
        elenen["yakin"] += 1; continue
    ikiz = [(s, iou(m, olcu[s]["_m"])) for s in secilen]
    if ikiz and max(ikiz, key=lambda x: x[1])[1] >= ESIK_IC:
        elenen["ikiz"] += 1; continue
    h, w = boy(f)
    olcu[ad] = {"_m": m, "yakin": en, "yakin_iou": round(float(deg), 3), "boy": round(h, 3), "gen": round(w, 3)}
    secilen.append(ad)
print("havuz", len(dosyalar), "elenen", elenen, "kalan", len(secilen))
cikti = {k: {kk: vv for kk, vv in v.items() if kk != "_m"} for k, v in olcu.items()}
json.dump(cikti, open(os.path.join(BURA, "aday-olcu-26.json"), "w", encoding="utf-8"), indent=1)
for k in sorted(cikti, key=lambda k: -cikti[k]["boy"]):
    v = cikti[k]
    print("%-48s boy %.2f gen %.2f  yakin %.2f %s" % (k, v["boy"], v["gen"], v["yakin_iou"], v["yakin"][-30:]))
