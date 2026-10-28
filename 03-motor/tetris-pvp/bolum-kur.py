"""TETRIS MODE PVP - tam bolum JSON'u (sahne4.html + efekt.py tek kaynak).

    python bolum-kur.py <cikti.json> [--bpm 133.0827] [--ayar ayar-03.json] [--kesit 1,2,16,31]

--ayar: videoya ozel ayar (duvar listesi, tur kartlari, ovgu, tema, muzik, bolum adi). Yoksa 2. video (REF-053) degerleri.
--kesit: yalniz bu duvar numaralari (~1 dk kesit); tur kartlari yalniz kesitteki turlar icin, WRAP/abone karti yok.

Yapi (18 Eki 2026): REF-053 dongusu (kart -> 3-2-1 -> duvar buyur -> gecer), 3 tur x 15 duvar = 45 duvar / 90 poz
(duvar-listesi.json, poz-listesi-kur.py). Her sure VURUS katidir -> muzige kilitli (Victory Rush, hakem 133,08 BPM).
Duvar 28 vurus = 7 olcu (~12,6 sn, REF-053 ~12 sn). Toplam 1320 vurus = 330 olcu = ~9:55 (TALIMATLAR §11: ~10 dk).
SUBSCRIBE her 15 sn (TALIMATLAR §16 kural), tam ekran kartlara denk gelirse kartin bitisine kayar.
"""
import json, math, os, sys

arg = lambda ad, v=None: sys.argv[sys.argv.index(ad) + 1] if ad in sys.argv else v
BURA = os.path.dirname(os.path.abspath(__file__))
AYAR = json.load(open(os.path.join(BURA, arg("--ayar")), encoding="utf-8")) if arg("--ayar") else {}
KESIT = [int(x) for x in arg("--kesit").split(",")] if arg("--kesit") else None
BPM = float(arg("--bpm", AYAR.get("bpm", 133.0827)))
V = 60 / BPM
r = lambda x: round(x, 4)
# duvar_vurus: 6. video (REF-057, dongu 12,0 sn olculdu) 24 vurus; eskiler 28
DV = AYAR.get("duvar_vurus", 28)
ZV = {"kart": 4, "say": 6, "buyu": 12, "gec": 2, **AYAR.get("zaman_vurus", {})}   # 10. video (REF-061): tabela+uyari 6, 3-2-1 6, buyume 4
Z = {"kart": r(ZV["kart"] * V), "say": r(ZV["say"] * V), "buyu": r(ZV["buyu"] * V), "gec": r(ZV["gec"] * V), "sure": r(DV * V)}
KV = AYAR.get("kart_vurus", {})   # kart suresi vurus olarak (varsayilan 8 = 2 olcu); 3. video: tam bolum 9,5-10 dk icin uzun kartlar
KART = 8 * V
KS = lambda tip, v=8: KV.get(tip, v) * V

DUVAR = json.load(open(os.path.join(BURA, AYAR.get("duvar", "duvar-listesi.json")), encoding="utf-8"))
OVGU = AYAR.get("ovgu", ["GREAT!", "EXCELLENT!", "PERFECT!", "AWESOME!", "AMAZING!", "NICE MOVE!"])
TUR_KART = {int(k): tuple(v) for k, v in AYAR["tur_kart"].items()} if "tur_kart" in AYAR else     {1: ("ROUND 1", None), 2: ("ROUND 2", "SKILL CHECK"), 3: ("ROUND 3", "TIME TO GO ALL OUT!")}
for i, d in enumerate(DUVAR):
    d["no"] = i + 1

kartlar, duvarlar = [], []
t = 0.0
GIRIS = AYAR.get("giris_kart", "vs")      # 5. video: "giris" (3 PLAYERS karti, VS yok - REF-056)


def dizi(liste):
    """6. video: kart dizisi [{"tip": ..., "vurus": 8, "metin": ..., "alt": ...}] -> art arda kartlar"""
    global t
    for kd in liste:
        kk = {k_: v_ for k_, v_ in kd.items() if k_ != "vurus"}
        kk.update({"t": r(t), "sure": r(kd.get("vurus", 8) * V)})
        kartlar.append(kk); t += kd.get("vurus", 8) * V


if "giris_dizisi" in AYAR:                 # 6. video (REF-057): acilis boksorleri + karsilama + HOW TO PLAY
    dizi(AYAR["giris_dizisi"])
else:
    kartlar.append({"t": r(t), "sure": r(KS(GIRIS)), "tip": GIRIS}); t += KS(GIRIS)
for tur in sorted({d["tur"] for d in DUVAR}):     # 8. video (REF-059): 4 tur
    if KESIT and not any(d["tur"] == tur and d["no"] in KESIT for d in DUVAR):
        continue
    if str(tur) in AYAR.get("gecis", {}) and not KESIT:   # tur kartindan once iki kiskirtici kart (REF-057)
        dizi(AYAR["gecis"][str(tur)])
    if not AYAR.get("tur_kart_yok"):          # 10. video (REF-061): tur karti yok, gruplar yalniz siralama
        m, alt = TUR_KART[tur]
        k = {"t": r(t), "sure": r(KS("tur")), "tip": "tur", "tur": tur, "metin": m}
        if alt: k["alt"] = alt
        kartlar.append(k); t += KS("tur")
    if tur == min(d["tur"] for d in DUVAR):
        kartlar.append({"t": r(t), "sure": r(KS("basla")), "tip": "basla"}); t += KS("basla")
    for d in [x for x in DUVAR if x["tur"] == tur and (not KESIT or x["no"] in KESIT)]:
        n = d["no"]
        # 5. video (REF-056, 3 oyuncu): duvarda p1/p2 yerine tek "grup" maskesi; duvar listesindeki alanlar aynen tasinir
        duvarlar.append({"no": n, "tur": tur, "t0": r(t), **{k_: v_ for k_, v_ in d.items() if k_ not in ("tur", "no")},
                         "ovgu": OVGU[(n - 1) % len(OVGU)]})
        t += Z["sure"]
        OK_ = AYAR.get("ovgu_kart")           # 10. video (REF-061): birkac duvarda bir siyah ovgu karti
        if OK_ and n % OK_["her"] == 0 and n < len(DUVAR):
            kartlar.append({"t": r(t), "sure": r(OK_["vurus"] * V), "tip": "ovgu_kart", "metin": OK_["metin"][(n // OK_["her"] - 1) % len(OK_["metin"])]})
            t += OK_["vurus"] * V
if not KESIT and "kapanis" in AYAR:       # 6. video: WRAP yerine kendi kapanis kartlarimiz
    dizi(AYAR["kapanis"])
    kartlar.append({"t": r(t), "sure": r(KS("abone", 12)), "tip": "abone"}); t += KS("abone", 12)
elif not KESIT:
    kartlar.append({"t": r(t), "sure": r(KS("wrap")), "tip": "wrap"}); t += KS("wrap")
    kartlar.append({"t": r(t), "sure": r(KS("abone", 12)), "tip": "abone"}); t += KS("abone", 12)
toplam_olcu = round(t / (4 * V))
assert abs(toplam_olcu * 4 * V - t) < 0.01, (t, toplam_olcu)

TAM = {"vs", "giris", "tur", "ovgu_kart", "wrap", "abone", "acilis", "yazi", "nasil"}; AS = 3.2
def bos(x):
    return not any(k["tip"] in TAM and x < k["t"] + k["sure"] and x + AS > k["t"] for k in kartlar)
abone, x = [], 15.0
while x + AS < t:
    u = x
    while not bos(u) and u + AS < t:
        u += 0.5
    if bos(u) and u + AS < t and (not abone or u - abone[-1] >= 10):
        abone.append(r(u))
    x += 15.0

b = {"seri": AYAR.get("seri", "TETRIS MODE PVP"), "bolum": AYAR.get("bolum", "tetris-pvp-01"), "bpm": BPM, "toplam_olcu": toplam_olcu,
     "toplam_duvar": len(duvarlar), "zaman": Z, "kartlar": kartlar, "duvarlar": duvarlar,
     "abone": abone, "abone_sure": AS, "muzik": AYAR.get("muzik", "Victory Rush.wav (Suno, kullanici)"),
     "_not": "Uretici: 03-motor/tetris-pvp/bolum-kur.py. Motor 03-motor/" + AYAR.get("sayfa", "sahne4.html") + "."}
if "tema" in AYAR:
    b["tema"] = AYAR["tema"]
json.dump(b, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{sys.argv[1]}: {len(duvarlar)} duvar, {len(abone)} SUBSCRIBE, {toplam_olcu} olcu = {t:.1f} sn ({int(t // 60)}:{t % 60:04.1f})")
