const {chromium}=require('playwright');
const OUT='/tmp/claude-0/bq/handoff/screenshots/';
(async()=>{
const E=require('child_process').execSync('ls /opt/pw-browsers/chromium-1194/chrome-linux*/chrome | head -1').toString().trim();
const launch={executablePath:E};
const b=await chromium.launch(launch);
const ctxOpts=v=>({viewport:v});
// Google Fonts is unreachable from the sandbox: serve the same families locally from @fontsource woff2 files
const FD=__dirname+'/fonts/';const fs=require('fs');
const ff=(fam,w,file)=>`@font-face{font-family:'${fam}';font-style:normal;font-weight:${w};font-display:swap;src:url(data:font/woff2;base64,${fs.readFileSync(FD+file).toString('base64')}) format('woff2')}`;
const FONTCSS=[ff('Bagel Fat One',400,'fontsource-bagel-fat-one-5.3.0/package/files/bagel-fat-one-latin-400-normal.woff2'),
 ...[400,500,600,700].map(w=>ff('Rubik',w,`fontsource-rubik-5.3.0/package/files/rubik-latin-${w}-normal.woff2`)),
 ff('VT323',400,'fontsource-vt323-5.3.0/package/files/vt323-latin-400-normal.woff2')].join('\n');
const html=require('fs').readFileSync('/home/claude/blobsquatch.html','utf8');
const wrap='<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><style>[hidden]{display:none!important}body{margin:0}</style><body>'+html+'</body>';
const errs=[];
async function page(v){const c=await b.newContext(ctxOpts(v));await c.route(/fonts\.googleapis\.com/,r=>r.fulfill({status:200,contentType:'text/css',body:FONTCSS}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));await p.setContent(wrap,{waitUntil:'load'});await p.waitForTimeout(1500);return p}
const fontsOk=async p=>p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family).join(','));

const view=(pg,sel)=>pg.evaluate(s=>{const e=document.querySelector(s);scrollTo(0,e.getBoundingClientRect().top+scrollY-90)},sel);
// ---- desktop ----
const p=await page({width:1280,height:900});
console.log('fonts loaded:',await fontsOk(p));
await p.screenshot({path:OUT+'01-desktop-full.jpg',fullPage:true,type:'jpeg',quality:80});
const st=await p.$('#stage');await st.scrollIntoViewIfNeeded();await p.waitForTimeout(300);
const shot=async n=>{await st.screenshot({path:OUT+n});console.log(n,await p.evaluate(()=>[S.mode,+S.t.toFixed(2),S.glance]))};
await shot('hero-rest.png');
// approach: hold S.t mid-dolly
await p.click('#goBtn',{force:true});await p.evaluate(()=>{window.__h=setInterval(()=>{if(S.mode==='approach')S.t=1.3},2)});await p.waitForTimeout(400);
await shot('hero-approach.png');
await p.evaluate(()=>{clearInterval(window.__h)});
await p.waitForFunction(()=>S.mode==='ready');await p.waitForTimeout(400);
await shot('hero-ready.png');
// twig: hold S.t
await p.evaluate(()=>{window.__h=setInterval(()=>{if(S.mode==='twig')S.t=.25},2)});
await p.click('#snapBtn',{force:true});await p.waitForTimeout(400);
await shot('hero-twig.png');
await p.evaluate(()=>{clearInterval(window.__h);window.__h=setInterval(()=>{if(S.mode==='glance')S.t=.42},2)});
await p.waitForFunction(()=>S.mode==='glance');await p.waitForTimeout(400);
await shot('hero-glance.png');
await p.evaluate(()=>clearInterval(window.__h));
await p.waitForFunction(()=>S.mode==='frozen');await p.waitForTimeout(1300);
await shot('hero-photo-developing.png');
await p.waitForTimeout(3200);
await shot('hero-photo-developed.png');
await p.click('#backWoods',{force:true});await p.waitForTimeout(200);
// pump
await p.click('#preview .chip[data-pct="5"]',{force:true});await view(p,'#stage');await p.waitForTimeout(500);await shot('pump-1.png');
await p.waitForTimeout(170);await shot('pump-2.png');
await p.click('#preview .chip[data-pct="-5"]',{force:true});await view(p,'#stage');await p.waitForTimeout(600);await shot('dump.png');
await p.click('#preview .chip[data-pct="0"]',{force:true});
// NFT section
const nft=await p.$('#nft .pols');await nft.scrollIntoViewIfNeeded();await p.waitForTimeout(200);await nft.screenshot({path:OUT+'nft-examples.png'});
// revealed-trait grid via (currently unused) renderNFT
await p.evaluate(()=>{const out=document.createElement('canvas');out.width=1440;out.height=720;out.id='grid';document.body.prepend(out);const g=out.getContext('2d');const c=document.createElement('canvas');c.width=c.height=360;
 const list=[{pose:'Glance Left',setting:'Night',film:'Polaroid'},{pose:'Glance Right',setting:'Dawn Fog',film:'Disposable'},{pose:'Mid-Stride',setting:'Snow',film:'Trail Cam'},{pose:'Wave',setting:'Rain',film:'Polaroid'},{pose:'Startled',setting:'Campfire',film:'Disposable'},{pose:'Glance Left',setting:'Night',film:'Night Vision'},{pose:'Wave',setting:'Snow',film:'Polaroid'},{pose:'Mid-Stride',setting:'Night',film:'Polaroid',ultra:true}];
 list.forEach((n,i)=>{renderNFT(c,n);g.drawImage(c,(i%4)*360,Math.floor(i/4)*360)})});
await (await p.$('#grid')).screenshot({path:OUT+'nft-renderNFT-trait-grid.jpg',type:'jpeg',quality:82});
await p.evaluate(()=>document.getElementById('grid').remove());
// game
const gb=await p.$('#gameBox');await view(p,'#gameBox');await p.waitForTimeout(300);
await gb.screenshot({path:OUT+'game-start.png'});
await p.click('#gPlay',{force:true});
await p.waitForFunction(()=>G.actor&&G.actor.mi>0,{timeout:15000}).catch(()=>{});
await gb.screenshot({path:OUT+'game-playing.png'});
// force a long MID-layer peek so we can aim, focus-lock and snap it
await p.evaluate(()=>{const a=makeActor('squatch');a.li=1;a.fx=LAYERS[1].trees[1];a.moves=[{type:'peek',tree:1,side:1,out:.2,hold:30,inn:.2},{type:'dash',f0:LAYERS[1].trees[1],f1:1.15}];a.mi=0;a.mt=0;G.actor=a;G.gap=99});
await p.waitForTimeout(400);
const box=await gb.boundingBox();
const pt=await p.evaluate(()=>{const a=G.actor,L=lay(a.li),h=actorH(a);return [a.fx*GW+h*.15,L.y-h*.55]});
await p.mouse.move(box.x+pt[0]-40,box.y+pt[1]-30);await p.mouse.move(box.x+pt[0],box.y+pt[1],{steps:4});
await p.waitForFunction(()=>G.focus>=1,{timeout:5000}).catch(()=>{});await p.waitForTimeout(100);
console.log('focus',await p.evaluate(()=>G.focus));
await gb.screenshot({path:OUT+'game-focus-lock.png'});
await p.mouse.down();await p.mouse.up();await p.waitForTimeout(200);
await gb.screenshot({path:OUT+'game-snap-pop.png'});
console.log('score',await p.evaluate(()=>[G.score,G.clear,G.roundBest&&G.roundBest.label]));
// force round cleared
await p.evaluate(()=>{G.clear=Math.max(G.clear,NEED(G.round));G.sight=SIGHTS;G.actor=null;G.laugh=null;G.gap=0});await p.waitForTimeout(400);
await gb.screenshot({path:OUT+'game-round-cleared.png'});
console.log('state',await p.evaluate(()=>G.state));
await p.click('#gPlay',{force:true});await p.waitForTimeout(300);
await p.evaluate(()=>{G.clear=0;G.sight=SIGHTS;G.actor=null;G.laugh=null;G.gap=0});await p.waitForTimeout(400);
await gb.screenshot({path:OUT+'game-over.png'});
console.log('state',await p.evaluate(()=>G.state));
// Barry crossing during play
await p.click('#gPlay',{force:true});await p.evaluate(()=>{G.barry={fx:.45};G.barryT=99});await p.waitForTimeout(150);
await gb.screenshot({path:OUT+'game-barry.png'});

// ---- mobile ----
const m=await page({width:390,height:844});
console.log('overflow-x mobile',await m.evaluate(()=>document.documentElement.scrollWidth>innerWidth));
await m.screenshot({path:OUT+'02-mobile-full.jpg',fullPage:true,type:'jpeg',quality:80});
const ms=await m.$('#stage');
await ms.screenshot({path:OUT+'hero-mobile-rest.png'});
await m.click('#goBtn',{force:true});await m.waitForFunction(()=>S.mode==='ready');await m.waitForTimeout(300);
await ms.screenshot({path:OUT+'hero-mobile-ready.png'});
await m.evaluate(()=>{document.getElementById('backWoods').click()});
await m.click('#preview .chip[data-pct="5"]',{force:true});await view(m,'#stage');await m.waitForTimeout(500);await ms.screenshot({path:OUT+'pump-mobile.png'});
await m.click('#preview .chip[data-pct="-5"]',{force:true});await view(m,'#stage');await m.waitForTimeout(500);await ms.screenshot({path:OUT+'dump-mobile.png'});
const mg=await m.$('#gameBox');await view(m,'#gameBox');await m.waitForTimeout(200);await mg.screenshot({path:OUT+'game-mobile-start.png'});
console.log('errors',errs);
await b.close()})();
