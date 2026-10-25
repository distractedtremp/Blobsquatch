import json,re
src=open('/tmp/claude-0/bq/v14.html').read()
art=json.load(open('/tmp/claude-0/bq/art/art.json'))
a=src.index('/* ---------- characters ---------- */');b=src.index("const Q={hat:")
new='''/* ---------- characters ---------- */
// Blobsquatch is the master art itself (Flat Fuzz), cut into layers: body front/back, two arms, face, happy face.
const P={pink:'#FDACCD',rose:'#E480A6',deep:'#C8608C',eye:'#3A1230'};
const ART=%s;
const SPR={};for(const k in ART){if(k[0]==='_')continue;const im=new Image();im.decoding='async';im.src=ART[k].src;SPR[k]=im;delete ART[k].src}
const SQ_CX=440,SQ_FT=1166,SQ_HM=1025,PIV_L=[176,640],PIV_R=[704,640];
const HEADCLIP=new Path2D('M224,505 C232,380 300,230 485,146 C610,215 690,330 700,505 L705,610 L220,610 Z');
function spr(g,k){const im=SPR[k],a=ART[k];if(im&&im.complete&&im.naturalWidth)g.drawImage(im,a.x,a.y,a.w,a.h)}
function sprPart(g,k,x,y,w,h,dx,dy){const im=SPR[k],a=ART[k];if(!(im&&im.complete&&im.naturalWidth))return;const sx=im.naturalWidth/a.w,sy=im.naturalHeight/a.h;
  g.drawImage(im,(x-a.x)*sx,(y-a.y)*sy,w*sx,h*sy,x+dx,y+dy,w,h)}
function armAt(g,k,p,ang){g.save();g.translate(p[0],p[1]);g.rotate(ang);g.translate(-p[0],-p[1]);spr(g,k);g.restore()}
// Blobsquatch, feet at (0,0), h tall, facing us (or away with o.back)
function squatch(g,h,t,o){
  o=o||{};const s=h/SQ_HM;
  g.save();g.scale(s,s);g.translate(-SQ_CX,-SQ_FT+(o.bob||0)/s);
  if(o.tilt){g.translate(SQ_CX,727);g.rotate(o.tilt);g.translate(-SQ_CX,-727)}
  // arm angles: 0 = hanging at his sides, bigger = raised up and out
  let aL=0,aR=0;
  if(o.arms==='dance'){const a=Math.sin(t*o.sp);aL=2.45+.32*a;aR=2.45-.32*a}
  else if(o.arms==='up'){aL=aR=2.5}
  else if(o.arms==='wave'){aR=2.55+Math.sin(t*9)*.28}
  else if(o.walk){const sw=Math.sin(t*5)*.09;aL=sw;aR=-sw}
  const arms=()=>{if(o.arms==='none')return;armAt(g,'armL',PIV_L,aL);armAt(g,'armR',PIV_R,-aR)};
  if(o.back){
    spr(g,'back');arms();
    const gl=o.glance||0;
    if(gl>0){ // looking back over his shoulder: the face slides round into view
      const sd=o.gside||1,off=sd*((1-gl)*230+40*gl),sx=.55+.4*gl;
      g.save();g.clip(HEADCLIP);g.translate(445+off,0);g.scale(sx,1);g.translate(-445,0);spr(g,'face');g.restore()}
    g.restore();return}
  spr(g,'front');
  if(o.splay)sprPart(g,'front',465,1068,230,102,175,0); // a foot sticking out from behind the tree
  arms();
  if(o.happy)spr(g,'faceHappy');
  g.restore();
}

'''%json.dumps(art,separators=(',',':'))
out=src[:a]+new+src[b:]
# dump scene: fingertips in the new rose
out=out.replace("ctx.fillStyle=P.pink;for(let i=0;i<3;i++){ctx.beginPath();ctx.ellipse(tx+tw/2","ctx.fillStyle=P.rose;for(let i=0;i<3;i++){ctx.beginPath();ctx.ellipse(tx+tw/2")
# developing Polaroid blob: the new fur pink
out=out.replace("pk.addColorStop(0,'rgba(255,79,163,.62)');pk.addColorStop(.55,'rgba(255,110,180,.3)');pk.addColorStop(1,'rgba(255,140,198,0)')","pk.addColorStop(0,'rgba(240,120,172,.62)');pk.addColorStop(.55,'rgba(250,155,198,.3)');pk.addColorStop(1,'rgba(253,172,205,0)')")
assert out.count('P.rose')==1
open('/home/claude/blobsquatch.html','w').write(out)
print(len(src),len(out))
