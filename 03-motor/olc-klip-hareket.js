/** Ham klip hareket egrisi (kalca/el/ayak dunya konumu) - HAR-007 insan hareketi olcumu.
 *  node olc-klip-hareket.js --klipler a,b --n 61 --cikti ../04-ciktilar/klip-hareket.json */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME=process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream'};
const arg=(a,d)=>{const i=process.argv.indexOf('--'+a);return i>-1?process.argv[i+1]:d;};
(async()=>{
  const KL=arg('klipler','').split(','), N=+arg('n','61'), CIK=path.resolve(arg('cikti','../04-ciktilar/klip-hareket.json'));
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:640,height:360});
  pg.on('pageerror',e=>console.log('HATA:',e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b&toplam=327&bolum=../bolumler/bolum-12-seker.json`,{waitUntil:'load',timeout:240000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  const out={}; for(const k of KL){ out[k]=await pg.evaluate((k,n)=>window.__klipOlc(k,n),k,N); console.log(k, out[k]?out[k].sure.toFixed(3)+' sn':'YOK'); }
  fs.writeFileSync(CIK,JSON.stringify(out)); await b.close(); s.close();
})();
