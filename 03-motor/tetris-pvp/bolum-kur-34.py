"""HUMAN TETRIS 34 bolum JSON'u (REF-086 yapi, 3P CO-OP, cilali 3D oyuncak blok sehri) - bolum-kur-32.py'den; ozel tur MIRROR
(29 SPEED, 30 MIRROR, 31 FREEZE, 32 SPEED, 33 BLIND -> 34 MIRROR). Giris KANCA (motor TEMA.acilis='kanca'). Motor 31 (sahne31.html).
SURE 3:15-3:20 (TALIMATLAR §3) -> 110 olcu = 196,2 sn (134,535 BPM; Solo Run On Neon Steps, solo-34-dizili.wav 110 olcu):
  acilis (kanca + geri sarma + blok kulesi + CAN YOUR TEAM CLEAR ALL 24?) 2 olcu (ilk duvar <= 5 sn; mobil paket md. 1)
  normal duvar 15 vurus: kart 2 / say 8 / buyu 3 / gec 2   (hakem uc pozu sirayla gosterir)
  MIRROR turu 6 duvar 16 vurus (say 9: ters siluet icin bir vurus fazla), d.ayna
  tur kartlari (ROUND 2, MIRROR ROUND, FINAL ROUND, BOSS WALL) 1'er olcu; BOSS WALL 29 vurus: kart 2 / say 12 / buyu 6 / gec 9
  sonuc 3 + RUTBE 3 + abone 3 olcu
CO-OP skor: d.skor = takimin gectigi duvar; 7. duvarda GREEN, 16. (MIRROR) duvarda PINK gec kalir -> 22/24 SILVER (27: 21/24).
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 134.5354
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-34.json"), encoding="utf-8"))
assert len(DUVAR) == 24

Z_NORMAL = {"kart": 2, "say": 8, "buyu": 3, "gec": 2}
Z_AYNA = {"kart": 2, "say": 9, "buyu": 3, "gec": 2}
Z_BOSS = {"kart": 2, "say": 12, "buyu": 6, "gec": 9}
OY = ("p1", "p2", "p3")
OUT = {"p1": set(), "p2": {16}, "p3": {7}}   # CO-OP: biri gec kalirsa takim o duvari kacirir -> 22/24 SILVER
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(vur, sure_olcu, **k):
    kartlar.append(dict(t=round(vur * V, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
vur = 8
skor = 0
plan = [(1, None, 6), (2, ("02", "ROUND 2"), 6), (3, ("03", "MIRROR ROUND", "EVERYTHING IS FLIPPED!"), 6),
        (4, ("04", "FINAL ROUND"), 5), (5, ("!", "BOSS WALL", "ALL THREE TOGETHER!"), 1)]
no = 0
for tur, tk, n in plan:
    if tk:
        kart(vur, 1, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        vur += 4
    for j in range(n):
        d = DUVAR[no]; no += 1
        ayna = tur == 3
        Z = Z_BOSS if tur == 5 else Z_AYNA if ayna else Z_NORMAL
        out = {o: no in OUT[o] for o in OY}
        if not any(out.values()):
            skor += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(vur * V, 4), "z": z, "p1": d["p1"], "p2": d["p2"], "p3": d["p3"],
                         "out": out, "skor": skor, "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "ayna": ayna,
                         "nasil": no <= 2})
        vur += sum(Z.values())
assert skor == 22, skor
rutbe = "GOLD" if skor == 24 else "SILVER" if skor >= 18 else "BRONZE"
assert vur % 4 == 0, vur
kart(vur, 3, tip="sonuc", skor=skor, toplam=len(duvarlar), rutbe=rutbe); vur += 12
kart(vur, 3, tip="rutbe"); vur += 12
kart(vur, 3, tip="abone"); vur += 12
TOPLAM = vur // 4
assert TOPLAM == 110, TOPLAM
assert 195 <= TOPLAM * O <= 200, TOPLAM * O
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]

SURE = TOPLAM * O
bos = lambda t: not any(k["t"] - 0.2 <= t <= k["t"] + k["sure"] + 0.2 or k["t"] <= t + 3.2 <= k["t"] + k["sure"] for k in kartlar) and \
    not any(d["t0"] + d["z"]["kart"] + d["z"]["say"] + d["z"]["buyu"] - 0.1 <= t + s <= d["t0"] + d["z"]["sure"] for d in duvarlar for s in (0, 3.2))
abone, t = [], 18.0                     # motor 29: abone satiri ustte, HOW TO PLAY seridiyle (ilk 2 duvar) cakismasin
while t < SURE - 30:
    q = t
    while not bos(q) and q < t + 6:
        q += 0.1
    if bos(q):
        abone.append(round(q, 2)); t = q + 15
    else:
        t += 1
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-34", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Solo Run On Neon Steps.wav (Suno; HT 12'den beri ilk, kullanici 20 Kas) -> 01-muzik/human-tetris-34/solo-34-dizili.wav (134,535 BPM, 110 olcu)",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-34.py. Motor 03-motor/sahne31.html (3P CO-OP oyuncak blok sehri, MIRROR, jole kup hakem). Referans REF-086 (yapi), mekan bizden (kullanici 20 Kas 2026).",
         "tema": {"acilis": "kanca", "varlik": "/03-motor/tetris-pvp/varlik-34s1/", "karakter": "/03-motor/tetris-pvp/varlik-34-karakter/",
                  "maskeVarlik": "/03-motor/tetris-pvp/varlik-34s1/", "turAd": {"1": "ROUND 1", "2": "ROUND 2", "3": "MIRROR ROUND", "4": "FINAL ROUND"},
                  "renk": ["#1ad2ff", "#ff2ad2", "#2ee860"], "acik": ["#d6f6ff", "#ffd6f4", "#d6ffe0"], "koyu": ["#0a5ad8", "#b0108c", "#0a8a2a"],
                  "ad": ["BLUE", "PINK", "GREEN"], "aboneAlt": "NEW CHALLENGE EVERY DAY", "yuzDy": 0}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-34.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
