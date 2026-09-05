/** Secili kliplerin birden cok fazini uretir - hareket okunurlugu testi.
 *  node faz-tarama.js --klipler jump-standing,duck,dodge-right,arm-wave --fazlar 0,0.2,0.4,0.6,0.8 --dizin <yol> */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME=process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream'};
const arg=(a,d)=>{const i=process.argv.indexOf('--'+a);return i>-1?process.argv[i+1]:d;};
(async()=>{
  const KLIPLER=arg('klipler','jump-standing,duck,dodge-right,arm-wave').split(',');
  const FAZLAR=arg('fazlar','0,0.2,0.4,0.6,0.8').split(',').map(Number);
  const DIZIN=path.resolve(arg('dizin','../04-ciktilar/faz'));
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});
    fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',
    args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:1280,height:720});
  pg.on('pageerror',e=>console.log('HATA:',e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=1280&h=720&tema=b&toplam=264`,{waitUntil:'load',timeout:240000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  fs.mkdirSync(DIZIN,{recursive:true});
  for(const k of KLIPLER){
    for(const f of FAZLAR){
      const veri=await pg.evaluate((k,f)=>window.siluetKaresi(k,f,700,950),k,f);
      if(!veri){console.log('YOK',k,f);continue;}
      const d=path.join(DIZIN,`${k}-faz${String(Math.round(f*100)).padStart(3,'0')}.png`);
      fs.writeFileSync(d,Buffer.from(veri.split(',')[1],'base64'));
      console.log('->',path.basename(d));
    }
  }
  await b.close(); s.close();
})();
