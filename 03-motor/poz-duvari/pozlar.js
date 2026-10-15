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

export const BOY = { govde: 55, boyun: 20, bas: 14, ust: 30, on: 28, uyluk: 46, baldir: 46, omuz: 50 };
export const KALINLIK = { govde: 24, kol: 11, bacak: 15 };

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
  const solDir = ekle(omuz, p.sol[0], BOY.ust), solEl = ekle(solDir, p.sol[1], BOY.on);
  const sagDir = ekle(omuz, p.sag[0], BOY.ust), sagEl = ekle(sagDir, p.sag[1], BOY.on);
  const solDiz = ekle(kalca, p.solB[0], BOY.uyluk), solAyak = ekle(solDiz, p.solB[1], BOY.baldir);
  const sagDiz = ekle(kalca, p.sagB[0], BOY.uyluk), sagAyak = ekle(sagDiz, p.sagB[1], BOY.baldir);
  const n = { kalca, boyun, bas, omuz, solDir, solEl, sagDir, sagEl, solDiz, solAyak, sagDiz, sagAyak };
  // yere oturt: uzuv uçlarının alt kenarı y=0
  let enAlt = Infinity;
  for (const [ad, q] of Object.entries(n)) {
    const r = ad === 'bas' ? BOY.bas : /Ayak|Diz/.test(ad) ? KALINLIK.bacak / 2
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
       p1: { sol: [-172, -178], sag: [172, 178], solB: [-3, -2], sagB: [3, 2] },
       p2: { sol: [-172, -178], sag: [172, 178], solB: [-3, -2], sagB: [3, 2] }, ara: 110 },
  4: { ad: 'Mirror Wave', koc: 'Mirror!', ipucu: 'Player one, left arm out. Player two, right arm out.',
       p1: { sol: [-90, -90] }, p2: { sag: [90, 90] }, ara: 120 },
  5: { ad: 'Big Arch', koc: 'Big arch!', ipucu: 'Inside hands up and together. Outside hand on your hip.',
       p1: { govde: 174, sag: [165, 125], sol: BEL_SOL },
       p2: { govde: 186, sol: [-165, -125], sag: BEL_SAG }, temas: ['sagEl', 'solEl'] },
  6: { ad: 'Robot', koc: 'Robot!', ipucu: 'Player one, arms up. Player two, arms down.',
       p1: { sol: [-90, 180], sag: [90, 180] }, p2: { sol: [-90, 0], sag: [90, 0] }, ara: 135 },
  13: { ad: 'Low and High', koc: 'Low and high!', ipucu: 'Player one, squat low. Player two, reach up tall!',
       p1: { sol: [-25, 75], sag: [25, -75], solB: [-75, -15], sagB: [75, 15] },
       p2: { sol: [-176, -179], sag: [176, 179], solB: [-2, -1], sagB: [2, 1] }, ara: 135 },
  14: { ad: 'Lunge Twins', koc: 'Lunge twins!', ipucu: 'Step forward into a lunge, arms up!',
       p1: { sol: [-178, -180], sag: [178, 180], sagB: [80, 0], solB: [-40, -75] },
       p2: { sol: [-178, -180], sag: [178, 180], solB: [-80, 0], sagB: [40, 75] }, ara: 150 },
};
