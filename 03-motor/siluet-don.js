/** Klip + faz + govde donusu ile siluet karesi uretir (inceleme araci).
 *  node siluet-don.js --klipler push-pose,push-it --fazlar 0,0.5 --donler 0,0.6 --dizin <yol> */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME=process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream'};
const arg=(a,d)=>{const i=process.argv.indexOf('--'+a);return i>-1?process.argv[i+1]:d;};
(async()=>{
  const KL=arg('klipler','idle').split(','), FZ=arg('fazlar','0').split(',').map(Number), DN=arg('donler','0').split(',').map(Number);
  const DIZIN=path.resolve(arg('dizin','../04-ciktilar/siluet-don'));
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:1280,height:720});
  pg.on('pageerror',e=>console.log('HATA:',e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=1280&h=720&tema=b&toplam=64`,{waitUntil:'load',timeout:240000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  fs.mkdirSync(DIZIN,{recursive:true});
  for(const k of KL) for(const dn of DN) for(const f of FZ){
    const v=await pg.evaluate((k,f,dn)=>window.siluetKaresi(k,f,700,950,dn),k,f,dn);
    if(!v){console.log('YOK',k);continue;}
    fs.writeFileSync(path.join(DIZIN,`${k}_d${Math.round(dn*100)}_f${Math.round(f*100)}.png`),Buffer.from(v.split(',')[1],'base64'));
  }
  console.log('bitti'); await b.close(); s.close();
})();
