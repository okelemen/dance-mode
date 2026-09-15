/** Klibin YATAY YON egrisi: hangi fazda sola, hangi fazda saga yatiyor?
 *  side-to-side gibi iki yone salinan klipte cue yonunu fazla eslestirmek icin.
 *  node olc-yon.js --klip side-to-side --dongu 1.14 */
const http=require('http'),fs=require('fs'),path=require('path'),puppeteer=require('puppeteer-core');
const KOK=path.resolve(__dirname,'..');
const CHROME=process.env.CHROME_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.fbx':'application/octet-stream'};
const arg=(a,d)=>{const i=process.argv.indexOf('--'+a);return i>-1?process.argv[i+1]:d;};
(async()=>{
  const KLIP=arg('klip','side-to-side'), DONGU=+arg('dongu',1.14), N=+arg('n',48);
  const s=http.createServer((q,r)=>{const p=path.join(KOK,decodeURIComponent(q.url.split('?')[0]));
    if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();}
    r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});
    fs.createReadStream(p).pipe(r);});
  await new Promise(r=>s.listen(0,'127.0.0.1',r));
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',
    args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await b.newPage(); await pg.setViewport({width:640,height:360});
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b&toplam=64`,{waitUntil:'load',timeout:240000});
  await pg.waitForFunction('window.HAZIR===true',{timeout:300000});
  const veri=await pg.evaluate(async (KLIP,DONGU,N)=>{
    const A=window.__T.aksiyon[KLIP]; if(!A) return {hata:'klip yok'};
    const sure=A.klip.duration, donguFaz=DONGU/sure;
    const cv=document.createElement('canvas'); cv.width=96; cv.height=128;
    const g=cv.getContext('2d',{willReadFrequently:true});
    const oku=(veri)=>new Promise(res=>{const im=new Image();
      im.onload=()=>{g.clearRect(0,0,96,128); g.drawImage(im,0,0,96,128);
        const d=g.getImageData(0,0,96,128).data; let sx=0,say=0,minx=999,maxx=-1;
        for(let y=0;y<128;y++)for(let x=0;x<96;x++){const q=(y*96+x)*4;
          if(d[q+3]>90&&(d[q]+d[q+1]+d[q+2])>150){sx+=x;say++;if(x<minx)minx=x;if(x>maxx)maxx=x;}}
        res(say>20?{com:(sx/say-48)/48, en:maxx-minx}:null);};
      im.onerror=()=>res(null); im.src=veri;});
    const out=[];
    for(let i=0;i<N;i++){
      const faz=(i/N)*donguFaz;
      const v=window.siluetKaresi(KLIP,faz,240,320);
      const r=v?await oku(v):null;
      out.push({faz:+(i/N).toFixed(3), com:r?+r.com.toFixed(3):null, en:r?r.en:null});
    }
    return {sure:+sure.toFixed(2), donguFaz:+donguFaz.toFixed(4), egri:out};
  },KLIP,DONGU,N);
  console.log(JSON.stringify(veri));
  fs.writeFileSync(path.join(KOK,'04-ciktilar','yon-'+KLIP+'.json'),JSON.stringify(veri,null,1));
  await b.close(); s.close();
})();
