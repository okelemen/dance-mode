/** Birden cok kareyi TEK tarayici oturumunda yakalar.
 *  node kare-coklu.js --bolum bolumler/bolum-06.json --toplam 286 --tema b --kareler 443,886,1329 --dizin <yol> */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME=process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream'};
const arg=(a,d)=>{const i=process.argv.indexOf('--'+a);return i>-1?process.argv[i+1]:d;};
(async()=>{
  const W=+arg('w',1280),H=+arg('h',720),TEMA=arg('tema','b'),TOPLAM=+arg('toplam',286);
  const BOLUM=arg('bolum',''), DIZIN=path.resolve(arg('dizin','../04-ciktilar'));
  const KARELER=arg('kareler','443').split(',').map(Number);
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});
    fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',
    args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:W,height:H});
  const hatalar=[]; pg.on('pageerror',e=>{hatalar.push(e.message);console.log('HATA:',e.message);});
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=${W}&h=${H}&tema=${TEMA}&toplam=${TOPLAM}`+(BOLUM?`&bolum=${encodeURIComponent(BOLUM)}`:''),{waitUntil:'load',timeout:180000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  fs.mkdirSync(DIZIN,{recursive:true});
  for(const n of KARELER){
    const veri=await pg.evaluate(k=>{window.kareKur(k);return window.kareAl();},n);
    const d=path.join(DIZIN,`kare-${String(n).padStart(6,'0')}.png`);
    fs.writeFileSync(d,Buffer.from(veri.split(',')[1],'base64'));
    console.log('->',path.basename(d));
  }
  if(hatalar.length) console.log('SAYFA HATALARI:',hatalar.length);
  await b.close(); s.close();
})();
