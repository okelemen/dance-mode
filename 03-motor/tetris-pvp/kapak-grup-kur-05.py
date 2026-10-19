"""TETRIS MODE 5. video KAPAK - 3 kisilik grup siluetleri (REF-056 kapagindaki gibi uc kisi birbirine deger; hareketler FARKLI).

    python kapak-grup-kur-05.py   -> kapak-grup-05.json (varlik.py --mod cadi --yalniz kapak2 okur)

Kullanici 19 Eki 2026: "referans kanalin kapagi cok iyi ... o ne yaptiysa aynisini yap ama siluetin hareketleri farkli olsun".
REF-056 kapaginda: uc kisi sarilmis, ortadaki dizini kaldirmis (sakin). Bizde dikkat ceken, hareketli Halloween pozlari; kurallar §14c:
kameraya donuk, yanlar ayna (simetri), ic eller/kollar ortadakine deger.
"""
import json, os

BURA = os.path.dirname(os.path.abspath(__file__))
_k = open(os.path.join(BURA, "grup-listesi-kur-05.py"), encoding="utf-8").read().split(chr(10) + "TUR1 = [")[0]
_g = {"__file__": os.path.join(BURA, "grup-listesi-kur-05.py")}
exec(compile(_k, "grup-listesi-kur-05.py", "exec"), _g)
on, grup = _g["on"], _g["grup"]

DUA_UST = ([-165, 170], [165, -170])
G = {
    # deneme 2 (kullanici "hic begenmedim"): REF-056 kumesi gibi SIKISIK ve UZUN, kisiler ic ice (yan + bindirme); hareketler farkli.
    # A - "Cadi sapkasi": ortada eller basin ustunde birlesik (sapka ucu, kumeyi uzatir); yanlar dis dizini kaldirir, dis kol kaktus
    "a": dict(grup("Witch Hat Huddle", on("", "cactus", "chest", "kneeup", "tog", govde=174), on("", DUA_UST[0], DUA_UST[1], "tog", "tog"),
                   temas="yan"), bindirme=0.38),
    # B - "Ucan yarasa": ortada Y kollar; yanlar disa egilir, dis kol capraz yukari, dis bacak yana tekme (kanat gibi acilan kume)
    "b": dict(grup("Spooky Kick", on("", "up", "hip", "straight", "tog", govde=196), on("", "v", "v", "tog", "tog"), temas="yan"),
              bindirme=0.34),
}
for k, g in G.items():
    for i, f in enumerate(g["figurler"]):
        f["ad"] = f"{g['ad']} {'ABC'[i]}"
json.dump({"_not": "Kapak grup pozlari (5. video). Figurler soldan saga; temas [sol eklem, sag eklem] ya da 'yan'.", "gruplar": G},
          open(os.path.join(BURA, "kapak-grup-05.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("kapak-grup-05.json:", list(G))
