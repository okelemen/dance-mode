// =====================================================================
// POZ DUVARI (POSE WALL) — poz geometrisi. Kural kaynağı:
//   Masaüstü/POZ-DUVARI/TALIMATLAR.md, poz listesi POZ-DUVARI/poz-defteri.md (v2: 80 poz)
// Hem sahne3.html (tarayıcı) hem node betikleri (ölçüm) bu modülü kullanır.
//
// Figür 2B piktogram: kalça (0,0), y yukarı. Her uzuv MUTLAK açıyla verilir:
//   a = 0 aşağı, 90 ekran-sağ, 180 yukarı, -90 ekran-sol.
// "sol"/"sag" = EKRANIN solu/sağı (kişinin değil). Kollar [üst kol, ön kol],
// bacaklar [uyluk, baldır]. govde: kalçadan boyna açı (180 dik), bas: başın
// gövdeye göre ek açısı. yan: 1 -> profil (omuz/kalça eklemleri üst üste).
// Figür otomatik yere oturtulur (en alçak nokta + kalınlık = zemin).
// temas: [P1 noktası, P2 noktası, aralık] -> P2 yatayda kaydırılır; sahne
// temas noktasını iki panelin birleşim çizgisine koyar.
// =====================================================================

export const BOY = { govde: 55, boyun: 20, bas: 14, ust: 30, on: 28, uyluk: 46, baldir: 46, omuz: 48,
                     omuzEn: 11, kalcaEn: 7, ayak: 12 };
export const KALINLIK = { govde: 24, kol: 11, bacak: 15, ayak: 10 };

const yon = a => { const r = a * Math.PI / 180; return [Math.sin(r), -Math.cos(r)]; };
const ekle = (p, a, l) => { const d = yon(a); return [p[0] + d[0] * l, p[1] + d[1] * l]; };

const VARSAYILAN = {
  govde: 180, bas: 0, yan: 0,
  sol: [-12, -6], sag: [12, 6],
  solB: [-6, -3], sagB: [6, 3],
};

export function figur(tanim) {
  const p = { ...VARSAYILAN, ...tanim };
  const kalca = [0, 0];
  const boyun = ekle(kalca, p.govde, BOY.govde);
  const bas = ekle(boyun, p.govde + p.bas, BOY.boyun);
  const omuz = ekle(kalca, p.govde, BOY.omuz);
  // Omuz ve kalça eklemleri gövdenin iki yanında (kesit 1: tek merkezden çıkan
  // kollar gövdeye gömülüyordu). Profilde (yan) üst üste.
  const oEn = p.yan ? 0 : BOY.omuzEn, kEn = p.yan ? 0 : BOY.kalcaEn;
  const sagA = p.govde + 90, solA = p.govde - 90;
  const omuzSol = ekle(omuz, -solA, oEn), omuzSag = ekle(omuz, -sagA, oEn);
  const kalcaSol = ekle(kalca, -solA, kEn), kalcaSag = ekle(kalca, -sagA, kEn);
  const solDir = ekle(omuzSol, p.sol[0], BOY.ust), solEl = ekle(solDir, p.sol[1], BOY.on);
  const sagDir = ekle(omuzSag, p.sag[0], BOY.ust), sagEl = ekle(sagDir, p.sag[1], BOY.on);
  const solDiz = ekle(kalcaSol, p.solB[0], BOY.uyluk), solAyak = ekle(solDiz, p.solB[1], BOY.baldir);
  const sagDiz = ekle(kalcaSag, p.sagB[0], BOY.uyluk), sagAyak = ekle(sagDiz, p.sagB[1], BOY.baldir);
  // ayak: bilekten yatay; gövde merkezinden dışa ya da baldırın gittiği yöne
  const ayakYon = (bilek, diz, kalcaX, vars) => {
    const dx = bilek[0] - kalcaX;
    const s = Math.abs(dx) > 6 ? Math.sign(dx) : (Math.abs(bilek[0] - diz[0]) > 4 ? Math.sign(bilek[0] - diz[0]) : vars);
    return [bilek[0] + s * BOY.ayak, bilek[1] - 2];
  };
  const solUc = ayakYon(solAyak, solDiz, kalca[0], -1), sagUc = ayakYon(sagAyak, sagDiz, kalca[0], 1);
  const n = { kalca, boyun, bas, omuz, omuzSol, omuzSag, kalcaSol, kalcaSag, solDir, solEl, sagDir, sagEl,
              solDiz, solAyak, sagDiz, sagAyak, solUc, sagUc };
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

// İki figürü yerleştirir. Dönüş: { p1, p2 } (çift merkezi 0)
export function cift(poz) {
  const a = figur(poz.p1), b = figur(poz.p2);
  const ara = poz.ara || 115;
  let p1 = kaydir(a, -ara / 2), p2 = kaydir(b, ara / 2);
  if (poz.temas) {
    const [n1, n2, bosluk = 0] = poz.temas;
    p2 = kaydir(p2, p1[n1][0] + bosluk - p2[n2][0]);
  }
  const xs = [...Object.values(p1), ...Object.values(p2)].map(q => q[0]);
  const orta = (Math.min(...xs) + Math.max(...xs)) / 2;
  return { p1: kaydir(p1, -orta), p2: kaydir(p2, -orta) };
}

// temaslı pozda birleşim çizgisinin figür birimindeki x'i
export function dikisX(poz, c) {
  const [n1, , bosluk = 0] = poz.temas;
  return c.p1[n1][0] + bosluk / 2;
}

// ------------------------------------------------------------ YARDIMCI
const ters = v => v && [-v[0], -v[1]];
// ayna: ekranda soldan sağa çevir (P2 çoğunlukla P1'in aynası)
export function ayna(f) {
  const o = { ...f };
  if ('govde' in f) o.govde = -f.govde;
  if ('bas' in f) o.bas = -f.bas;
  o.sol = ters(f.sag || VARSAYILAN.sag); o.sag = ters(f.sol || VARSAYILAN.sol);
  o.solB = ters(f.sagB || VARSAYILAN.sagB); o.sagB = ters(f.solB || VARSAYILAN.solB);
  return o;
}
const BEL_SOL = [-45, 20];
const AYAKTA = { solB: [-3, -2], sagB: [3, 2] };
const AYNA = (f, ek = {}) => ({ p1: f, p2: ayna(f), ...ek });
const IKIZ = (f, ek = {}) => ({ p1: f, p2: f, ...ek });

// ------------------------------------------------------------ POZLAR (no = poz-defteri.md v2)
export const POZLAR = {
  // ---------------- TUR 1 · EASY
  1:  { ad: 'Star', ...IKIZ({ sol: [-130, -130], sag: [130, 130], solB: [-25, -25], sagB: [25, 25] }) },
  2:  { ad: 'High Five', ...AYNA({ sag: [120, 150] }, { temas: ['sagEl', 'solEl'] }) },
  3:  { ad: 'Rocket', ...IKIZ({ sol: [-160, 168], sag: [160, -168], ...AYAKTA }) },
  4:  { ad: 'Mirror', ...AYNA({ sol: [-90, -90] }) },
  5:  { ad: 'Big Arch', ...AYNA({ govde: 174, sag: [165, 125], sol: BEL_SOL }, { temas: ['sagEl', 'solEl'] }) },
  6:  { ad: 'Robot', p1: { sol: [-90, 180], sag: [90, 180] }, p2: { sol: [-90, 0], sag: [90, 0] } },
  7:  { ad: 'Flamingo', ...AYNA({ sol: [-90, -90], sag: [90, 90], sagB: [80, 0] }) },
  8:  { ad: 'Scarecrow', ...AYNA({ sol: [-90, -20], sag: [90, 20], bas: 22, ...AYAKTA }) },
  9:  { ad: 'Point the Way', ...IKIZ({ sag: [135, 135], sol: BEL_SOL, sagB: [22, 15] }) },
  10: { ad: 'Heart', ...IKIZ({ sol: [-150, 130], sag: [150, -130] }) },
  11: { ad: 'Dino Arms', ...IKIZ({ sol: [-25, -80], sag: [25, 80], solB: [-15, 5], sagB: [15, -5] }) },
  12: { ad: 'Goalkeeper', ...IKIZ({ sol: [-110, -110], sag: [110, 110], solB: [-40, -10], sagB: [40, 10] }) },
  13: { ad: 'Wave Hello', ...AYNA({ sag: [150, 175], sol: BEL_SOL }) },
  14: { ad: 'Muscles', ...IKIZ({ sol: [-90, 150], sag: [90, -150] }) },
  15: { ad: 'Hand on Chin', ...AYNA({ sag: [60, -150], sol: BEL_SOL }) },
  16: { ad: 'Lean', ...AYNA({ govde: 160, sol: [150, 150], sag: [160, 160] }) },
  17: { ad: 'Salute', ...IKIZ({ sag: [100, -130], ...AYAKTA }) },
  18: { ad: 'Step Out', ...AYNA({ solB: [-35, -35], sagB: [5, 3], sol: [-60, -60], sag: [30, 30] }) },
  19: { ad: 'Arms Crossed', ...IKIZ({ sol: [-10, 110], sag: [10, -110], ...AYAKTA }) },
  20: { ad: 'Disco', ...AYNA({ sag: [150, 150], sol: [-30, -30], sagB: [15, 10] }) },

  // ---------------- TUR 2 · MEDIUM
  21: { ad: 'Back to Back', ...AYNA({ yan: 1, sol: [-15, -110], sag: [-15, -110], ...AYAKTA }, { temas: ['kalca', 'kalca', 26] }) },
  22: { ad: 'Bridge Hands', ...AYNA({ govde: 155, sol: [125, 125], sag: [130, 130], solB: [-10, -8], sagB: [0, 0] }, { temas: ['sagEl', 'solEl'] }) },
  23: { ad: 'Low and High', p1: { sol: [-25, 75], sag: [25, -75], solB: [-75, -15], sagB: [75, 15] },
        p2: { sol: [-163, -170], sag: [163, 170], solB: [-2, -1], sagB: [2, 1] } },
  24: { ad: 'Lunge Twins', ...AYNA({ sol: [-163, -170], sag: [163, 170], sagB: [80, 0], solB: [-40, -75] }) },
  25: { ad: 'Tree', ...AYNA({ sol: [-160, 168], sag: [160, -168], sagB: [70, -40] }) },
  26: { ad: 'Archer', ...AYNA({ sol: [-90, -90], sag: [-90, 90], solB: [-25, -25], sagB: [25, 25] }) },
  27: { ad: 'Teapot', ...AYNA({ govde: 192, sol: BEL_SOL, sag: [100, 40] }) },
  28: { ad: 'Superhero', ...AYNA({ sag: [165, 175], sol: BEL_SOL, solB: [-15, -10], sagB: [15, 10] }) },
  29: { ad: 'Side Bend', ...AYNA({ govde: 205, sag: [210, 235], sol: [-15, -10] }) },
  30: { ad: 'Hands on Knees', ...IKIZ({ solB: [-40, 10], sagB: [40, -10], sol: [-25, -15], sag: [25, 15] }) },
  31: { ad: 'Side Kick', ...AYNA({ sagB: [95, 92], sol: [-30, 150], sag: [30, -150] }) },
  32: { ad: 'Surfer', ...AYNA({ govde: 175, solB: [-45, -15], sagB: [45, 15], sol: [-100, -100], sag: [80, 80] }) },
  33: { ad: 'Windmill', ...AYNA({ govde: 165, sol: [-150, -150], sag: [30, 30], solB: [-25, -25], sagB: [25, 25] }) },
  34: { ad: 'Bow', ...AYNA({ yan: 1, govde: 120, sol: [10, 5], sag: [10, 5], ...AYAKTA }) },
  35: { ad: 'Runner', ...AYNA({ yan: 1, govde: 172, sagB: [110, 10], solB: [-30, -70], sag: [50, 150], sol: [-45, -20] }) },
  36: { ad: 'Zombie', ...AYNA({ yan: 1, sol: [90, 90], sag: [90, 90], solB: [-10, -5], sagB: [12, 5] }) },
  37: { ad: 'Penguin', ...IKIZ({ sol: [-12, -60], sag: [12, 60], ...AYAKTA }) },
  38: { ad: 'Cross Legs', ...IKIZ({ solB: [12, 10], sagB: [-12, -10], sol: [-100, -100], sag: [100, 100] }) },
  39: { ad: 'Floor Reach', ...AYNA({ yan: 1, govde: 95, bas: 30, sol: [0, 0], sag: [0, 0], solB: [-8, -3], sagB: [8, 3] }) },
  40: { ad: 'Fists Up', ...AYNA({ sol: [-30, 160], sag: [30, -160], solB: [-15, -5], sagB: [25, 10] }) },

  // ---------------- TUR 3 · HARD
  41: { ad: 'Airplane', ...AYNA({ govde: 160, sol: [-110, -110], sag: [70, 70], solB: [-75, -75], sagB: [5, 3] }) },
  42: { ad: 'Wall Sit Pair', ...AYNA({ yan: 1, solB: [-90, 0], sagB: [-90, 0], sol: [-15, -110], sag: [-15, -110] }, { temas: ['kalca', 'kalca', 26] }) },
  43: { ad: 'Leaning Tower', ...AYNA({ govde: 150, sol: [100, 100], sag: [105, 105], solB: [-15, -12], sagB: [-5, -5] }, { temas: ['sagEl', 'solEl'] }) },
  44: { ad: 'Warrior Three', ...AYNA({ yan: 1, govde: 90, sol: [90, 90], sag: [90, 90], solB: [0, 0], sagB: [-90, -90] }) },
  45: { ad: 'Dancer', ...AYNA({ yan: 1, govde: 150, sag: [125, 125], sol: [-90, -100], solB: [-60, -170], sagB: [0, 0] }) },
  46: { ad: 'Crab and Tall', p1: { yan: 1, govde: -100, bas: -30, sol: [-5, 0], sag: [-5, 0], solB: [85, 0], sagB: [85, 0] },
        p2: { sol: [-170, -178], sag: [170, 178], ...AYAKTA } },
  47: { ad: 'Ski Jump', ...AYNA({ yan: 1, govde: 140, sol: [-30, -30], sag: [-30, -30], solB: [60, -20], sagB: [60, -20] }) },
  48: { ad: 'Seesaw', p1: { yan: 1, govde: 165, solB: [85, -15], sagB: [85, -15], sol: [100, 100], sag: [100, 100] },
        p2: { yan: 1, govde: 160, sol: [-60, -60], sag: [-60, -60], solB: [-5, -5], sagB: [-5, -5] },
        temas: ['sagEl', 'solEl'] },
  49: { ad: 'Side Plank Star', p1: { govde: 115, solB: [-65, -65], sagB: [-65, -65], sag: [5, 5], sol: [175, 175] },
        p2: { sol: [-130, -130], sag: [130, 130], solB: [-25, -25], sagB: [25, 25] } },
  50: { ad: 'Low Lunge', ...AYNA({ yan: 1, govde: 125, sol: [5, 5], sag: [5, 5], sagB: [80, 5], solB: [-75, -82] }) },
  51: { ad: 'Chair', ...AYNA({ yan: 1, govde: 150, sol: [150, 150], sag: [150, 150], solB: [55, -20], sagB: [55, -20] }) },
  52: { ad: 'Half Moon', ...AYNA({ govde: 95, sag: [5, 5], sol: [178, 178], sagB: [3, 0], solB: [-92, -92] }) },
  53: { ad: 'Knee Hug', ...AYNA({ yan: 1, sagB: [120, 10], solB: [0, 0], sag: [70, 40], sol: [70, 40] }) },
  54: { ad: 'Side Lunge', ...AYNA({ sagB: [50, -5], solB: [-75, -75], sol: [-20, 70], sag: [20, -70] }) },
  55: { ad: 'Superman', ...AYNA({ yan: 1, govde: 83, bas: -10, sol: [100, 100], sag: [100, 100], solB: [-97, -97], sagB: [-97, -97] }) },
  56: { ad: 'Hips Up', ...AYNA({ yan: 1, govde: -65, bas: -25, sol: [92, 92], sag: [92, 92], solB: [120, 0], sagB: [120, 0] }) },
  57: { ad: 'Mountain Climber', ...AYNA({ yan: 1, govde: 72, sol: [0, 0], sag: [0, 0], solB: [-105, -105], sagB: [45, -60] }) },
  58: { ad: 'Down Dog', ...AYNA({ yan: 1, govde: 45, bas: 10, sol: [35, 35], sag: [35, 35], solB: [-35, -35], sagB: [-35, -35] }) },
  59: { ad: 'Lunge Twist', ...AYNA({ yan: 1, sagB: [80, 0], solB: [-40, -75], sol: [-90, -90], sag: [90, 90] }) },
  60: { ad: 'Triangle', ...AYNA({ govde: 105, sag: [5, 5], sol: [178, 178], solB: [-35, -35], sagB: [35, 35] }) },

  // ---------------- TUR 4 · FINAL
  61: { ad: 'Statue', ...AYNA({ sagB: [110, 10], sag: [175, 180], sol: BEL_SOL }) },
  62: { ad: 'Tunnel', ...AYNA({ govde: 165, sol: [160, 135], sag: [150, 115], solB: [-8, -5] }, { temas: ['sagEl', 'solEl'] }) },
  63: { ad: 'Boat', ...AYNA({ yan: 1, govde: 205, sol: [100, 100], sag: [100, 100], solB: [128, 128], sagB: [128, 128] }, { temas: ['sagUc', 'solUc', 4] }) },
  64: { ad: 'Lightning', ...AYNA({ sol: [-130, -50], sag: [50, 130], sagB: [40, -30] }) },
  65: { ad: 'Table and Chair', p1: { yan: 1, govde: 90, sol: [0, 0], sag: [0, 0], solB: [0, -90], sagB: [0, -90] },
        p2: { yan: 1, govde: 180, solB: [-90, 0], sagB: [-90, 0], sol: [-90, -90], sag: [-90, -90] } },
  66: { ad: 'Skater', ...AYNA({ govde: 160, sagB: [15, -5], solB: [-55, -55], sol: [-70, -70], sag: [130, 130] }) },
  67: { ad: 'Fold Down', ...IKIZ({ govde: 0, sol: [-60, 30], sag: [60, -30], solB: [-15, -15], sagB: [15, 15] }) },
  68: { ad: 'Thinker and Scratcher', p1: { solB: [-85, 100], sagB: [85, -100], sag: [60, -150], sol: [-40, -20] },
        p2: { sag: [150, -120], sol: BEL_SOL } },
  69: { ad: 'Frog', ...IKIZ({ govde: 175, solB: [-75, -10], sagB: [75, 10], sol: [-5, -5], sag: [5, 5] }) },
  70: { ad: 'Lunge Punch', ...AYNA({ yan: 1, sagB: [75, 0], solB: [-40, -70], sag: [90, 90], sol: [30, 150] }) },
  71: { ad: 'Warrior Two', ...AYNA({ sagB: [55, -5], solB: [-55, -55], sol: [-90, -90], sag: [90, 90], bas: 15 }) },
  72: { ad: 'Hero Kneel', ...AYNA({ yan: 1, sagB: [90, 0], solB: [-15, -90], sag: [170, 175], sol: [40, 20] }) },
  73: { ad: 'Hand to Toe', ...AYNA({ yan: 1, sagB: [90, 90], solB: [0, 0], sag: [85, 88], sol: [-30, -20] }) },
  74: { ad: 'Squat Arms Up', ...IKIZ({ solB: [-80, -10], sagB: [80, 10], sol: [-165, -172], sag: [165, 172] }) },
  75: { ad: 'Toe Touch Sit', ...AYNA({ yan: 1, govde: 135, solB: [90, 90], sagB: [90, 90], sol: [100, 95], sag: [100, 95] }) },
  76: { ad: 'Bird Dog', ...AYNA({ yan: 1, govde: 90, sol: [0, 0], sag: [90, 90], solB: [0, -90], sagB: [-90, -90] }) },
  77: { ad: 'Rock Star', ...AYNA({ solB: [-35, -15], sagB: [35, 15], sol: [-70, -100], sag: [30, -60] }) },
  78: { ad: 'Victory Lunge', ...AYNA({ sagB: [60, 0], solB: [-60, -60], sol: [-140, -140], sag: [140, 140] }) },
  79: { ad: 'Big Hug', ...AYNA({ yan: 1, sol: [80, 110], sag: [75, 105] }, { temas: ['sagEl', 'solEl'] }) },
  80: { ad: 'Champions', ...AYNA({ sol: [-145, -150], sag: [135, 130] }, { temas: ['sagEl', 'solEl'] }) },
};
