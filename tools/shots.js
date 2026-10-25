// Screenshot the site in its main states. Serve the repo root first:
//   python3 -m http.server 8765   then   node tools/shots.js <outdir>
const {chromium}=require('playwright');
const OUT=(process.argv[2]||'shots')+'/',URL=process.env.URL||'http://localhost:8765/';
(async()=>{
require('fs').mkdirSync(OUT,{recursive:true});
const b=await chromium.launch();const errs=[];
async function page(v){const c=await b.newContext({viewport:v});const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));await p.goto(URL,{waitUntil:'load'});await p.waitForTimeout(1500);return p}
const p=await page({width:1280,height:900});
await p.screenshot({path:OUT+'desktop-full.jpg',fullPage:true,type:'jpeg',quality:75});
const st=await p.$('#stage');await st.scrollIntoViewIfNeeded();await p.waitForTimeout(300);
const shot=n=>st.screenshot({path:OUT+n});
await shot('hero-rest.png');
await p.click('#goBtn',{force:true});await p.evaluate(()=>{window.__h=setInterval(()=>{if(S.mode==='approach')S.t=2.0},2)});await p.waitForTimeout(400);
await shot('hero-approach.png');await p.evaluate(()=>clearInterval(window.__h));
await p.waitForFunction(()=>S.mode==='ready');await p.click('#snapBtn',{force:true});
await p.evaluate(()=>{window.__h=setInterval(()=>{if(S.mode==='glance')S.t=.5},2)});
await p.waitForFunction(()=>S.mode==='glance');await p.waitForTimeout(400);await shot('hero-glance.png');
await p.evaluate(()=>clearInterval(window.__h));
await p.waitForFunction(()=>S.mode==='frozen');await p.waitForTimeout(4600);await shot('hero-photo.png');
await p.click('#backWoods',{force:true});await p.waitForTimeout(200);
await p.click('#preview .chip[data-pct="5"]',{force:true});await p.waitForTimeout(500);await shot('pump-1.png');
await p.waitForTimeout(240);await shot('pump-2.png');
await p.evaluate(()=>{pct=12;ph=Math.PI/2*7+.1});await p.waitForTimeout(60);await shot('pump-pop.png');
await p.click('#preview .chip[data-pct="-5"]',{force:true});await p.waitForTimeout(600);await shot('dump.png');
await p.click('#preview .chip[data-pct="0"]',{force:true});
const gb=await p.$('#gameBox');await gb.scrollIntoViewIfNeeded();await p.click('#gPlay',{force:true});
await p.waitForFunction(()=>G.actor&&G.actor.mi>0,{timeout:15000}).catch(()=>{});await p.waitForTimeout(300);
await gb.screenshot({path:OUT+'game-playing.png'});
const m=await page({width:390,height:844});
await m.screenshot({path:OUT+'mobile-full.jpg',fullPage:true,type:'jpeg',quality:70});
console.log('errors:',JSON.stringify(errs));
await b.close();
})();
