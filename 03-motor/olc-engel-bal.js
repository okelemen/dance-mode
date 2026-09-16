/** ENG-004 (BUZ) kadraj kaplama olcumu - olc-engel.js'ten uyarlandi: her cue icin kareyi ENGELLI ve ENGELSIZ
 *  basip farki sayar. Kural: vurus aninda engel kadrajin %30'unu gecmez. */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME='C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream','.png':'image/png','.wav':'audio/wav'};
const KARE={"zipla-1": 435, "zipla-2": 543, "zipla-3": 652, "egil-1": 869, "egil-2": 978, "egil-3": 1087, "yanL-1": 1304, "yanR-1": 1413, "yanL-2": 1522, "yanR-2": 1630, "it-1": 1739, "it-2": 1848, "it-3": 1956};
(async()=>{
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream','Cache-Control':'no-store'});
    fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:1280,height:720});
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=1280&h=720&tema=b&toplam=64&bolum=../bolumler/onizleme-bal.json`,{waitUntil:'load',timeout:240000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  const sonuc={};
  for(const [ad,n] of Object.entries(KARE)){
    // Kaplama GEOMETRIK olculuyor: gizleyip yeniden basmak ise yaramadi,
    // cunku kareKur her karede destek parcalarini yeniden gorunur yapiyor.
    // Her gorunur gecit parcasinin 8 kosesi ekrana yansitiliyor, piksel
    // maskesi uzerinde birlestiriliyor - ust sinir degil GERCEK alan.
    sonuc[ad]=await pg.evaluate((n)=>{
      window.kareKur(n);
      const T=window.__T, cam=T.camera, W=1280, H=720;
      const maske=new Uint8Array(W*H);
      const v=new T.THREE.Vector3();
      let say=0;
      T.scene.traverse(o=>{
        if(!o.visible||!o.isMesh) return;
        // UST GRUPLAR DA GORUNUR OLMALI: gizli destek grubunun cocuklari kendi
        // visible bayragini koruyor ve ekranda olmayan eski engeller sayiliyordu
        // (ilk olcum yanL/it icin %84-85 verdi).
        for(let a=o.parent;a;a=a.parent){ if(!a.visible) return; }
        const u=o.parent&&o.parent.userData;
        if(!u||!u.bKutu||o===u.bGolge) return;      // yalnizca BUZ parcalari (golge haric)
        const g=o.geometry; if(!g.boundingBox) g.computeBoundingBox();
        const bb=g.boundingBox; const pts=[];
        for(const x of [bb.min.x,bb.max.x]) for(const y of [bb.min.y,bb.max.y]) for(const z of [bb.min.z,bb.max.z]){
          v.set(x,y,z); o.localToWorld(v); v.project(cam);
          pts.push([(v.x*0.5+0.5)*W, (1-(v.y*0.5+0.5))*H, v.z]);
        }
        if(pts.some(q=>q[2]>1)) return;           // kamera arkasi
        const x0=Math.max(0,Math.floor(Math.min(...pts.map(q=>q[0]))));
        const x1=Math.min(W,Math.ceil(Math.max(...pts.map(q=>q[0]))));
        const y0=Math.max(0,Math.floor(Math.min(...pts.map(q=>q[1]))));
        const y1=Math.min(H,Math.ceil(Math.max(...pts.map(q=>q[1]))));
        for(let y=y0;y<y1;y++) for(let x=x0;x<x1;x++){ const i=y*W+x; if(!maske[i]){maske[i]=1;say++;} }
      });
      return say/(W*H)*100;
    },n);
    for(const gizle of [false]){
      await pg.evaluate((n,gizle)=>{
        window.__GIZLE_ENGEL = gizle;
        window.kareKur(n);
        if(gizle){
          window.__T.scene.traverse(o=>{
            const u=o.userData||{};
            if(u.gPanel||u.gCapL) o.visible=false;         // destek grubu
          });
        }
      },n,gizle);
      const veri=await pg.evaluate(()=>window.kareAl('png'));
      fs.writeFileSync(path.join(KOK,'04-ciktilar',`olc-${ad}-${gizle?'yok':'var'}.png`),Buffer.from(veri.split(',')[1],'base64'));
    }
    console.log('-> %s kadraj kaplama %%%s', ad, sonuc[ad].toFixed(1));
  }
  await b.close(); s.close();
})();
