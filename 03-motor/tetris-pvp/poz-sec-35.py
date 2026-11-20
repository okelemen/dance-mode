"""HUMAN TETRIS 35. video (REF-087, CO-OP 2 oyuncu, balon festivali, 24 duvar = 24 ikili es poz): poz-sec-28'den.
35 farki: 23, 27, 28'in pozlari (ad) + 23/27/28 maskeleriyle IoU >= 0,78 olanlar ve 28 kontaginda gozle elenen 13 cikar; eski havuzda
9 aday kaldigi icin (20 Kas sayimi) havuza 35'in yeni adaylari eklenir (ikili-listesi-kur-35.py -> varlik-35-grup, Actions 44713571003).
Yeni adaylar ESKI havuzun butun maskeleriyle de (7, 11, 13, 15, 18) IoU < 0,78 olmali (tekrar yok). FREEZE turuna tek ayak (knee-lift) girmez.
--- 28 notu ---
HUMAN TETRIS 28. video (REFERANSSIZ, CO-OP 2 oyuncu, dev mutfak, 24 duvar = 24 ikili poz): poz-sec-27'den.
28 farki: 23 ve 27'nin pozlari (ad) + 23/27 maskeleriyle IoU >= 0,78 olanlar elenir (son 4 videonun ikili videolari 23 ve 27);
23 ve 27'de gozle elenenler bastan cikar. Turlar: R1 en kolay 6, FREEZE 6 (gectikten sonra 3 sn tutulur -> ayakta, dengeli,
orta-kolay dilim; tek ayak denge pozu FREEZE'e konmaz), R2 6, FINAL en zor 6. Cikti duvar-listesi-28.json (tur alanli).
--- 23 notu ---
HUMAN TETRIS 23. video (REF-078 HumanWarmUp, CO-OP 2 oyuncu, 24 Mission = 24 ikili poz): onceki CO-OP videolarinin ikili maskelerinden harmanlar.
Kullanici 7 Kas 2026: "uygun silüet bulamadıysan öncekilerden harmanla ... ilk Tetris videolarından bulup onları yapabilirsin".
Havuz: 7., 11., 13., 15., 18. videolarin ikili (duo) maskeleri (131 dosya). Oncelik ilk videolar (7 -> 11 -> 13 -> 15 -> 18).
Elenen: adi havada / ters / ziplama / tek ayak tekme okunanlar; havuz icinde IoU >= 0,70 ikizler (ilk gelen = eski video kalir).
Secim: en cesitli 24 (farthest-point, ilk videolara hafif oncelik). Siralama: zorluk = (1 - boy) * 3 + genislik * 0,8 (ayakta -> yere yakin).
Cikti: duvar-listesi-23.json, aday-olcu-23.json, kontak (sari duvar + siyah cift, numarali).

    python poz-sec-23.py [--cikar ad1 ad2 ...] [--kontak yol.jpg]
"""
import argparse, glob, json, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BURA = os.path.dirname(os.path.abspath(__file__))
N = 128
ESIK_IC = 0.70
ADET = 24
HAVUZ = (("07", "varlik-07-poz2/grup"), ("11", "varlik-11-poz2/grup"), ("13", "varlik-13-poz2/grup"), ("15", "varlik-15-poz2/grup"), ("18", "varlik-18-poz2/tetris-varlik/grup"), ("35", "varlik-35-grup"))
YASAK = re.compile(r"jump|hop|leap|head-?stand|hand-?stand|cartwheel|wheel|flip|invert|upside|fly|air|dive|fall|kick|warrior-three|boat|swing|plank|lean-back|recline", re.I)
p = argparse.ArgumentParser()
p.add_argument("--cikar", nargs="*", default=[]); p.add_argument("--sira", nargs="*", type=int, default=[], help="kontaktaki numaralarla yeni sira (1 tabanli)"); p.add_argument("--kontak", default="C:/Users/eleme/OneDrive/Masaüstü/POZ-DUVARI/taslak/HUMAN-TETRIS-35-POZ-KONTAK.jpg")
a = p.parse_args()


def maske(yol):
    im = np.array(Image.open(yol).convert("RGBA"))
    m = im[:, :, 3] > 40
    ys, xs = np.nonzero(m)
    k = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = k.shape; s = max(h, w)
    kare = np.zeros((s, s), bool); kare[s - h:, (s - w) // 2:(s - w) // 2 + w] = k
    return np.array(Image.fromarray(kare.astype(np.uint8) * 255).resize((N, N), Image.BILINEAR)) > 127, h / im.shape[0], w / im.shape[1]


def iou(x, y):
    return max((x & y).sum() / max(1, (x | y).sum()), (x & y[:, ::-1]).sum() / max(1, (x | y[:, ::-1]).sum()))


KULLANILAN23 = [c["grup"] for c in json.load(open(os.path.join(BURA, "duvar-listesi-23.json"), encoding="utf-8"))]
ELENEN23 = ["duo-camel-standing-reach", "duo-reverse-warrior-mirror", "duo-archer-side-squat", "duo-t-arm-tree", "duo-pike-v-and-knee-drive",
            "duo-kneel-t-and-warrior-two", "duo-seated-helper-standing-reach"]
KULLANILAN23 += [c["grup"] for c in json.load(open(os.path.join(BURA, "duvar-listesi-27.json"), encoding="utf-8"))]
KULLANILAN23 += [c["grup"] for c in json.load(open(os.path.join(BURA, "duvar-listesi-28.json"), encoding="utf-8"))]
ELENEN27 = ["tree-pose-arms-overhead", "side-lunge-and-kneel-t", "y-arms-step-out", "garland-squat-side-by-side", "low-squat-w-arms",
            "wide-lunge-down-and-tree", "downward-dog-facing", "seated-lean-and-bow-link",
            "bow-and-cheer", "crescent-tiptoe-arms-high", "low-squat-and-tall-reach", "goddess-squat-prayer", "guard-step-punch-link", "kneeling-back-to-back-arms-high", "inner-knee-lift-arms-up", "hands-behind-head-wide-stance", "wide-horse-v-arms", "kneel-stretch-and-side-bend", "kneel-arms-up-and-standing-bow", "kneel-stand-high-five", "facing-lunge-high-five"]   # + 28 kontak 1-4
M23 = [maske(y)[0] for y in sorted(glob.glob(os.path.join(BURA, "varlik-23", "grup", "*.png")))]
M23 += [maske(y)[0] for y in sorted(glob.glob(os.path.join(BURA, "varlik-27-grup", "*.png")))]
M23 += [maske(y)[0] for y in sorted(glob.glob(os.path.join(BURA, "varlik-28-grup", "*.png")))]
assert len(M23) == 72, len(M23)
ESKI_M = [maske(y)[0] for v, kl in HAVUZ if v != "35" for y in sorted(glob.glob(os.path.join(BURA, kl, "*.png")))]
assert len(ESKI_M) > 120, len(ESKI_M)
print("23 + 27 + 28 maskesi:", len(M23), "eski havuz maskesi:", len(ESKI_M))
aday = []
for sira, (vid, kl) in enumerate(HAVUZ):
    for yol in sorted(glob.glob(os.path.join(BURA, kl, "*.png"))):
        ad = os.path.splitext(os.path.basename(yol))[0]
        if YASAK.search(ad) or ad in a.cikar or ad in KULLANILAN23 or ad in ELENEN23 or any(e in ad for e in ELENEN27):
            continue
        m, boy, gen = maske(yol)
        if any(iou(m, q) >= 0.78 for q in M23) or (vid == "35" and any(iou(m, q) >= 0.78 for q in ESKI_M)):
            continue
        aday.append({"ad": ad, "video": vid, "sira": sira, "yol": yol, "m": m, "boy": boy, "gen": gen})
print("havuz (ad suzgecinden sonra):", len(aday))
kalan = []
for c in aday:                                             # ikiz eleme: eski video once geldigi icin o kalir; ayni ad da ikizdir
    if any(c["ad"] == k["ad"] or iou(c["m"], k["m"]) >= ESIK_IC for k in kalan):
        continue
    kalan.append(c)
print("ikiz elemeden sonra:", len(kalan))
M = np.array([[iou(x["m"], y["m"]) for y in kalan] for x in kalan])
sec = [int(np.argmin([c["boy"] for c in kalan]) * 0)]        # ilk aday (7. video) ile basla
while len(sec) < ADET:
    en = None
    for i, c in enumerate(kalan):
        if i in sec:
            continue
        puan = (1 - M[i, sec].max()) - 0.02 * c["sira"]    # cesitlilik - eski videoya hafif oncelik
        if en is None or puan > en[0]:
            en = (puan, i)
    sec.append(en[1])
S = [kalan[i] for i in sec]
ic = max(M[i, j] for i in sec for j in sec if i != j)
for c in S:
    c["zor"] = (1 - c["boy"]) * 3 + c["gen"] * 0.8
S.sort(key=lambda c: c["zor"])
if a.sira:
    assert sorted(a.sira) == list(range(1, len(S) + 1)), "sira eksik / tekrarli"
    S = [S[i - 1] for i in a.sira]
print("secilen %d, ic en yuksek IoU %.3f" % (len(S), ic))
print("kaynak dagilimi:", {v: sum(1 for c in S if c["video"] == v) for v, _ in HAVUZ})
TUR = ["ROUND 1"] * 6 + ["ROUND 2"] * 6 + ["FREEZE ROUND"] * 6 + ["FINAL ROUND"] * 6
if not a.sira:                                              # zorluk sirasi: 1-6 R1, 7-12 FREEZE (orta-kolay, tutulabilir) videoda 3. tur, 13-18 R2, 19-24 FINAL
    S = S[:6] + S[12:18] + S[6:12] + S[18:]
    TEK = lambda c: any(w in c["ad"] for w in ("knee-lift", "tree", "kneeup"))          # 35: FREEZE'de 3 sn tutulacak -> tek ayak yok, R2 ile takas
    for i in range(12, 18):
        if TEK(S[i]):
            j = next(j for j in range(6, 12) if not TEK(S[j])); S[i], S[j] = S[j], S[i]
json.dump([{"tur": TUR[i], "grup": c["ad"], "video": c["video"]} for i, c in enumerate(S)], open(os.path.join(BURA, "duvar-listesi-35.json"), "w", encoding="utf-8"), indent=1)
json.dump([{"ad": c["ad"], "video": c["video"], "boy": round(c["boy"], 3), "gen": round(c["gen"], 3)} for c in kalan], open(os.path.join(BURA, "aday-olcu-35.json"), "w", encoding="utf-8"), indent=1)
C = 6; KW, KH = 320, 200
sayfa = Image.new("RGB", (C * KW, ((len(S) + C - 1) // C) * (KH + 30)), "#1a0628"); d = ImageDraw.Draw(sayfa); f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
for i, c in enumerate(S):
    al = Image.open(c["yol"]).convert("RGBA").getchannel("A"); al = al.crop(al.getbbox()); al.thumbnail((KW - 40, KH - 24))
    x, y = (i % C) * KW, (i // C) * (KH + 30)
    d.rectangle((x + 6, y + 28, x + KW - 6, y + 28 + KH - 4), fill="#ffe600")
    sayfa.paste((0, 0, 0), (x + (KW - al.width) // 2, y + 28 + KH - 8 - al.height), al)
    d.text((x + 8, y + 6), "%d %s  %s (v%s)" % (i + 1, TUR[i].replace(" ROUND", "")[:6], c["ad"].replace("duo-", "")[:24], c["video"]), font=f, fill="white")
    print("%2d  %-44s v%s  boy %.2f gen %.2f" % (i + 1, c["ad"], c["video"], c["boy"], c["gen"]))
sayfa.save(a.kontak, quality=88); print("->", a.kontak)
