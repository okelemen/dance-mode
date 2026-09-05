/** Cue penceresi ile klip suresini karsilastirir: hareket ne kadar hizlaniyor? */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME=process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream'};
const arg=(a,d)=>{const i=process.argv.indexOf('--'+a);return i>-1?process.argv[i+1]:d;};
(async()=>{
  const BOLUM=arg('bolum',''), TOPLAM=+arg('toplam',286);
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});
    fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',
    args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:640,height:360});
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b&toplam=${TOPLAM}`+(BOLUM?`&bolum=${encodeURIComponent(BOLUM)}`:''),{waitUntil:'load',timeout:240000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  const veri=await pg.evaluate(()=>{
    const T=window.__T;
    const kl={}; for(const [ad,v] of Object.entries(T.aksiyon)) kl[ad]=v.klip.duration;
    
    const NN = T.NOTALAR || [];
    return {kl, notalar:NN.map(n=>({tip:n.tip,klip:n.klip,t:n.t,pencere:n.pencere}))};
  });
  console.log(JSON.stringify(veri).slice(0,200));
  fs.writeFileSync(path.join(__dirname,'..','04-ciktilar','tempo.json'),JSON.stringify(veri));
  await b.close(); s.close();
})();
