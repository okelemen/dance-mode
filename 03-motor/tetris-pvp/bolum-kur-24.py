"""HUMAN TETRIS 24 bolum JSON'u (referanssiz, 1v1, havuzlu stadyum) - TALIMATLAR §4 mobil paket + ozel turlar + skor.

    python bolum-kur-24.py   ->  bolumler/tetris-mode-24.json

Olcu cizelgesi (130 BPM, olcu 1,846 sn):
  0-2     acilis VS + "WHO WILL WIN? BLUE OR PINK?" (mobil paket md. 1 ve 5: ilk duvar 3,7 sn'de)
  2-38    ROUND 1: 6 duvar x 6 olcu (ilk iki duvarda ustte HOW TO PLAY seridi)
  38-40   ROUND 2 karti; 40-76 6 duvar x 6
  76-78   SPEED ROUND karti; 78-102 6 duvar x 4 olcu (hizli duvar)
  102-104 FINAL ROUND karti; 104-134 5 duvar x 6
  134-136 BOSS WALL karti; 136-144 son duvar 8 olcu (buyuk duvar)
  144-147 sonuc karti (kazanan + skor = bastaki sorunun cevabi); 147-150 RUTBE karti (yorum cagrisi); 150-154 abone + LIKE/COMMENT/SHARE
Skor (yarisan karakterler, mobil paket md. 2-3): OUT duvarlari onceden yazilir, son duvara kadar basa bas; BOSS WALL kazanani belirler.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.abspath(os.path.join(BURA, "..", ".."))
BPM = 130.0
V = 60 / BPM; O = 4 * V
DUVAR = json.load(open(os.path.join(BURA, "duvar-listesi-24.json"), encoding="utf-8"))
assert len(DUVAR) == 24

# vurus cinsinden duvar dongusu: kart (kapi acilir) / say (3-2-1, maskot gosterir, karakterler poza girer) / buyu / gec (tam ekran panel)
Z_NORMAL = {"kart": 4, "say": 12, "buyu": 4, "gec": 4}
Z_HIZLI = {"kart": 2, "say": 8, "buyu": 3, "gec": 3}
Z_BOSS = {"kart": 4, "say": 16, "buyu": 6, "gec": 6}
OUT = {"p1": {4, 10, 16, 24}, "p2": {7, 14, 20}}          # BLUE 20 - 21 PINK (son duvara kadar 20-20)
OVGU = ["PERFECT!", "NICE!", "GREAT!", "AMAZING!", "SUPER!", "WOW!"]

kartlar, duvarlar = [], []
def kart(olcu, sure_olcu, **k):
    kartlar.append(dict(t=round(olcu * O, 4), sure=round(sure_olcu * O, 4), **k))

kart(0, 2, tip="acilis", soru=True)
olcu = 2
skor = {"p1": 0, "p2": 0}
plan = [(1, None, 6, Z_NORMAL), (2, ("02", "ROUND 2"), 6, Z_NORMAL), (3, ("03", "SPEED ROUND", "FASTER WALLS!"), 6, Z_HIZLI),
        (4, ("04", "FINAL ROUND"), 5, Z_NORMAL), (5, ("!", "BOSS WALL", "WINNER TAKES IT ALL"), 1, Z_BOSS)]
no = 0
for tur, tk, n, Z in plan:
    if tk:
        kart(olcu, 2, tip="tur", tur=min(tur, 4), metin=tk[0], alt=tk[1], ek=tk[2] if len(tk) > 2 else None, boss=tur == 5)
        olcu += 2
    for _ in range(n):
        d = DUVAR[no]; no += 1
        out = {o: no in OUT[o] for o in ("p1", "p2")}
        for o in ("p1", "p2"):
            if not out[o]:
                skor[o] += 1
        z = {k: round(v * V, 4) for k, v in Z.items()}; z["sure"] = round(sum(Z.values()) * V, 4)
        duvarlar.append({"no": no, "tur": min(tur, 4), "t0": round(olcu * O, 4), "z": z, "p1": d["p1"], "p2": d["p2"],
                         "out": out, "skor": dict(skor), "ovgu": OVGU[(no - 1) % len(OVGU)], "boss": tur == 5, "hizli": tur == 3,
                         "nasil": no <= 2})
        olcu += sum(Z.values()) // 4
kazanan = "p2" if skor["p2"] > skor["p1"] else "p1"
assert skor == {"p1": 20, "p2": 21}, skor
kart(olcu, 3, tip="sonuc", kazanan=kazanan, skor=skor); olcu += 3
kart(olcu, 3, tip="rutbe"); olcu += 3
kart(olcu, 4, tip="abone"); olcu += 4
TOPLAM = olcu
assert TOPLAM == 154, TOPLAM
assert duvarlar[0]["t0"] <= 5.0, duvarlar[0]["t0"]          # mobil paket md. 1

# SUBSCRIBE her ~15 sn (TALIMATLAR §4), tam ekran kartlarda yok, gec panelinde yok; 3,2 sn
SURE = TOPLAM * O
bos = lambda t: not any(k["t"] - 0.2 <= t <= k["t"] + k["sure"] + 0.2 or k["t"] <= t + 3.2 <= k["t"] + k["sure"] for k in kartlar) and \
    not any(d["t0"] + d["z"]["kart"] + d["z"]["say"] + d["z"]["buyu"] - 0.1 <= t + s <= d["t0"] + d["z"]["sure"] for d in duvarlar for s in (0, 3.2))
abone, t = [], 8.0
while t < SURE - 30:
    q = t
    while not bos(q) and q < t + 6:
        q += 0.1
    if bos(q):
        abone.append(round(q, 2)); t = q + 15
    else:
        t += 1
bolum = {"seri": "HUMAN TETRIS", "bolum": "human-tetris-24", "bpm": BPM, "toplam_olcu": TOPLAM, "toplam_duvar": len(duvarlar),
         "kartlar": kartlar, "duvarlar": duvarlar, "abone": abone, "abone_sure": 3.2,
         "muzik": "Full Energy Drop.wav (Suno, kullanici, 26 Eyl 2026; eski parca) -> fed-130.wav, 130 BPM sabit",
         "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur-24.py. Motor 03-motor/sahne21.html. Referanssiz (kullanici 11 Kas 2026).",
         "tema": {"varlik": "/03-motor/tetris-pvp/varlik-24s/tetris-varlik/", "karakter": "/03-motor/tetris-pvp/varlik-24-karakter/",
                  "aboneAlt": "NEW BATTLE EVERY DAY"}}
yol = os.path.join(KOK, "bolumler", "tetris-mode-24.json")
json.dump(bolum, open(yol, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("->", yol, "olcu", TOPLAM, "sure %.1f sn" % SURE, "duvar", len(duvarlar), "abone", len(abone), "ilk duvar %.2f" % duvarlar[0]["t0"], "skor", skor)
