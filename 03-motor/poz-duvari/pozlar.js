// =====================================================================
// POZ DUVARI (POSE WALL) — poz geometrisi. Kural kaynağı:
//   Masaüstü/POZ-DUVARI/TALIMATLAR.md, poz listesi POZ-DUVARI/poz-defteri.md
// Hem sahne3.html (tarayıcı) hem node betikleri (ölçüm) bu modülü kullanır.
//
// Figür 2B piktogram: kalça (0,0), y yukarı. Her uzuv MUTLAK açıyla verilir:
//   a = 0 aşağı, 90 ekran-sağ, 180 yukarı, -90 ekran-sol.
// "sol"/"sag" = EKRANIN solu/sağı (kişinin değil). Kollar [üst kol, ön kol],
// bacaklar [uyluk, baldır]. govde: kalçadan boyna açı (180 dik).
// Figür otomatik yere oturtulur (en alçak nokta + kalınlık = zemin).
// temas: [P1 noktası, P2 noktası] -> P2 yatayda kaydırılır, iki nokta buluşur.
// =====================================================================

export const BOY = { govde: 55, boyun: 20, bas: 14, ust: 30, on: 28, uyluk: 46, baldir: 46, omuz: 48,
                     omuzEn: 11, kalcaEn: 7, ayak: 12 };
export const KALINLIK = { govde: 24, kol: 11, bacak: 15, ayak: 10 };

const yon = a => { const r = a * Math.PI / 180; return [Math.sin(r), -Math.cos(r)]; };
const ekle = (p, a, l) => { const d = yon(a); return [p[0] + d[0] * l, p[1] + d[1] * l]; };

const VARSAYILAN = {
  govde: 180, bas: 0,
  sol: [-12, -6], sag: [12, 6],
  solB: [-6, -3], sagB: [6, 3],
};

// kalça eli: üst kol dışa-aşağı, ön kol kalçaya döner
const BEL_SOL = [-45, 20], BEL_SAG = [45, -20];

export function figur(tanim) {
  const p = { ...VARSAYILAN, ...tanim };
  const kalca = [0, 0];
  const boyun = ekle(kalca, p.govde, BOY.govde);
  const bas = ekle(boyun, p.govde + p.bas, BOY.boyun);
  const omuz = ekle(kalca, p.govde, BOY.omuz);
  // Omuz ve kalça eklemleri gövdenin iki yanında (16 Eki kesiti: tek merkez
  // noktadan çıkan kollar gövdeye gömülüyor, figür sütun gibi okunuyordu).
  const sagA = p.govde + 90, solA = p.govde - 90;   // gövdeye dik, ekran sağı/solu
  const omuzSol = ekle(omuz, -solA, BOY.omuzEn), omuzSag = ekle(omuz, -sagA, BOY.omuzEn);
  const kalcaSol = ekle(kalca, -solA, BOY.kalcaEn), kalcaSag = ekle(kalca, -sagA, BOY.kalcaEn);
  const solDir = ekle(omuzSol, p.sol[0], BOY.ust), solEl = ekle(solDir, p.sol[1], BOY.on);
  const sagDir = ekle(omuzSag, p.sag[0], BOY.ust), sagEl = ekle(sagDir, p.sag[1], BOY.on);
  const solDiz = ekle(kalcaSol, p.solB[0], BOY.uyluk), solAyak = ekle(solDiz, p.solB[1], BOY.baldir);
  const sagDiz = ekle(kalcaSag, p.sagB[0], BOY.uyluk), sagAyak = ekle(sagDiz, p.sagB[1], BOY.baldir);
  // ayak: bilekten yatay, gövde merkezinden dışa (yan duruşta baldırın gittiği yöne)
  const ayakYon = (bilek, diz, kalcaX, vars) => {
    const dx = bilek[0] - kalcaX;
    const s = Math.abs(dx) > 6 ? Math.sign(dx) : (Math.abs(bilek[0] - diz[0]) > 4 ? Math.sign(bilek[0] - diz[0]) : vars);
    return [bilek[0] + s * BOY.ayak, bilek[1] - 2];
  };
  const solUc = ayakYon(solAyak, solDiz, kalca[0], -1), sagUc = ayakYon(sagAyak, sagDiz, kalca[0], 1);
  const n = { kalca, boyun, bas, omuz, omuzSol, omuzSag, kalcaSol, kalcaSag, solDir, solEl, sagDir, sagEl,
              solDiz, solAyak, sagDiz, sagAyak, solUc, sagUc };
  // yere oturt: uzuv uçlarının alt kenarı y=0
  let enAlt = Infinity;
  for (const [ad, q] of Object.entries(n)) {
    const r = ad === 'bas' ? BOY.bas : /Uc/.test(ad) ? KALINLIK.ayak / 2 : /Ayak|Diz/.test(ad) ? KALINLIK.bacak / 2
            : /El|Dir/.test(ad) ? KALINLIK.kol / 2 : KALINLIK.govde / 2;
    enAlt = Math.min(enAlt, q[1] - r);
  }
  for (const q of Object.values(n)) q[1] -= enAlt;
  return n;
}

export function kaydir(n, dx) {
  const o = {};
  for (const [ad, q] of Object.entries(n)) o[ad] = [q[0] + dx, q[1]];
  return o;
}

// İki figürü yerleştirir. Dönüş: { p1, p2 } (merkez 0 civarında)
export function cift(poz) {
  const a = figur(poz.p1), b = figur(poz.p2);
  let ara = poz.ara || 115;
  let p1 = kaydir(a, -ara / 2), p2 = kaydir(b, ara / 2);
  if (poz.temas) {
    const [n1, n2] = poz.temas;
    const dx = p1[n1][0] - p2[n2][0];
    p2 = kaydir(p2, dx);
  }
  // çifti panelde ortala (asimetrik pozlar sola/sağa kaymasın)
  const xs = [...Object.values(p1), ...Object.values(p2)].map(q => q[0]);
  const orta = (Math.min(...xs) + Math.max(...xs)) / 2;
  p1 = kaydir(p1, -orta); p2 = kaydir(p2, -orta);
  return { p1, p2 };
}

// ------------------------------------------------------------ POZLAR
// no = poz-defteri.md numarası. koc = koç sesinin söyleyeceği ad,
// ipucu = asimetrik pozlarda oyunculara ayrı komut (dublaj için konuşma).
export const POZLAR = {
  1: { ad: 'Star', koc: 'Star!',
       p1: { sol: [-130, -130], sag: [130, 130], solB: [-25, -25], sagB: [25, 25] },
       p2: { sol: [-130, -130], sag: [130, 130], solB: [-25, -25], sagB: [25, 25] }, ara: 150 },
  2: { ad: 'High Five', koc: 'High five!', ipucu: 'Reach up and touch hands!',
       p1: { sag: [120, 150] }, p2: { sol: [-120, -150] }, temas: ['sagEl', 'solEl'] },
  3: { ad: 'Rocket', koc: 'Rocket!', ipucu: 'Hands together, reach up high!',
       p1: { sol: [-160, 168], sag: [160, -168], solB: [-3, -2], sagB: [3, 2] },
       p2: { sol: [-160, 168], sag: [160, -168], solB: [-3, -2], sagB: [3, 2] }, ara: 110 },
  4: { ad: 'Mirror Wave', koc: 'Mirror!', ipucu: 'Player one, left arm. Player two, right arm.',
       p1: { sol: [-90, -90] }, p2: { sag: [90, 90] }, ara: 120 },
  5: { ad: 'Big Arch', koc: 'Big arch!', ipucu: 'Inside hands up. Outside hand on hip.',
       p1: { govde: 174, sag: [165, 125], sol: BEL_SOL },
       p2: { govde: 186, sol: [-165, -125], sag: BEL_SAG }, temas: ['sagEl', 'solEl'] },
  6: { ad: 'Robot', koc: 'Robot!', ipucu: 'Player one up. Player two down.',
       p1: { sol: [-90, 180], sag: [90, 180] }, p2: { sol: [-90, 0], sag: [90, 0] }, ara: 135 },
  13: { ad: 'Low and High', koc: 'Low and high!', ipucu: 'Player one low. Player two tall!',
       p1: { sol: [-25, 75], sag: [25, -75], solB: [-75, -15], sagB: [75, 15] },
       p2: { sol: [-163, -170], sag: [163, 170], solB: [-2, -1], sagB: [2, 1] }, ara: 135 },
  14: { ad: 'Lunge Twins', koc: 'Lunge twins!', ipucu: 'Step forward into a lunge, arms up!',
       p1: { sol: [-163, -170], sag: [163, 170], sagB: [80, 0], solB: [-40, -75] },
       p2: { sol: [-163, -170], sag: [163, 170], solB: [-80, 0], sagB: [40, 75] }, ara: 150 },
};
