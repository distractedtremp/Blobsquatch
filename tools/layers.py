import numpy as np, json, base64, io
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
full=np.asarray(Image.open('cut_full.png')).astype(float)
col=full[...,:3]; A=full[...,3]/255; H,W=A.shape
yy,xx=np.mgrid[:H,:W]
dist=lambda c:np.linalg.norm(col-np.array(c,float),axis=2)
FUR=(253,172,205)
wedge=(A>.9)&(col[...,0]<215)&(col[...,1]<140)&(dist(FUR)>35)&(yy>590)&(yy<900)
def cutline(side):
    xs={}
    for y in range(600,1046):
        row=A[y]>.5
        rng=range(0,440) if side<0 else range(W-1,439,-1)
        xr=list(rng)
        # first run = arm
        i=0
        while i<len(xr) and not row[xr[i]]: i+=1
        if i>=len(xr): continue
        outer=xr[i]
        while i<len(xr) and row[xr[i]]: i+=1
        armend=xr[min(i,len(xr)-1)]
        wz=[x for x in xr if wedge[y,x]]
        if wz: xs[y]=(outer,wz[0])
        elif i<len(xr): xs[y]=(outer,armend+(2 if side<0 else -2)*(-1 if side>0 else 1)*0)
    ys=sorted(xs);cut=np.array([xs[y][1] for y in ys],float);out=np.array([xs[y][0] for y in ys],float)
    cut=ndi.median_filter(cut,15);cut=ndi.gaussian_filter1d(cut,4)
    return dict(zip(ys,cut)),dict(zip(ys,out))
layers={};meta={}
LY=[620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980,1000,1020,1040]
LX=[255,237,226,216,207,198,191,182,183,183,183,187,193,190,206,201,219,213,215,210,205,205]
RX=[625,643,654,664,673,683,691,696,697,696,696,693,695,687,676,666,661,665,664,670,675,675]
def armmask(side):
    py=640.; px=176. if side<0 else 704.; r=72.
    ys=np.arange(H);cut=np.interp(ys,LY,LX if side<0 else RX)
    m=(yy>=py)&(yy<=1046)&((xx<cut[:,None]) if side<0 else (xx>cut[:,None]))
    disk=(xx-px)**2+(yy-py)**2<r*r
    return m,disk,(px,py,r)
mL,dL,pL=armmask(-1); mR,dR,pR=armmask(1)
soft=lambda m,s=1.4: np.clip(ndi.gaussian_filter(m.astype(float),s),0,1)
armL=A*soft(mL|dL); armR=A*soft(mR|dR)
body=A*(1-soft(mL&~dL))*(1-soft(mR&~dR))
def rgba(alpha,c=col): return np.dstack([c,alpha*255]).astype(np.uint8)
layers['armL']=rgba(armL);layers['armR']=rgba(armR);layers['front']=rgba(body)
meta['pivL']=pL;meta['pivR']=pR
# ---- face layer ----
fe=((xx-445)/160)**2+((yy-462)/137)**2
facem=soft(fe<1,5)
layers['face']=rgba(A*facem)
# ---- inpaint helper ----
def nconv(img,mask,sig):
    w=ndi.gaussian_filter(mask.astype(float),sig)
    return np.stack([ndi.gaussian_filter(img[...,c]*mask,sig) for c in range(3)],-1)/np.maximum(w,1e-6)[...,None]
patch=col[200:330,380:520]
tex=patch-ndi.gaussian_filter(patch,(6,6,0))
def tiled(hh,ww):
    t=np.concatenate([tex,tex[:,::-1]],1);t=np.concatenate([t,t[::-1]],0)
    reps=(hh//t.shape[0]+2,ww//t.shape[1]+2,1);return np.tile(t,reps)[:hh,:ww]
TEX=tiled(H,W)
# ---- back view: face + belly become fur, toe lines removed ----
facepix=(fe<1)&(dist(FUR)>28)&(A>.5)
fe2=((xx-452)/170)**2+((yy-452)/150)**2
facepix=(fe2<1)&(dist(FUR)>28)&(A>.5)
facepix=ndi.binary_dilation(facepix,iterations=7)&(fe2<1.1)
belly=((xx-440)/150)**2+((yy-772)/172)**2<1
fill=(facepix|belly)
keep=(A>.95)&~ndi.binary_dilation(fill,iterations=4)&(dist(FUR)<45)
base=nconv(col,keep,22);wk=ndi.gaussian_filter(keep.astype(float),22)
base2=nconv(col,keep,90);base=np.where((wk>.08)[...,None],base,base2)
furfill=np.clip(base+TEX,0,255)
w=soft(fill,4)[...,None]
back=col*(1-w)+furfill*w
feet=(yy>1070)&(A>.5)
med=np.stack([ndi.median_filter(back[...,c],size=13) for c in range(3)],-1)
back=np.where(feet[...,None],med,back)
# the back of the head gets a little darker fur crest so it does not read as a blank egg
layers['back']=rgba(body,back)
# ---- happy face: smirk painted out, open grin drawn ----
mouth=(xx>360)&(xx<545)&(yy>500)&(yy<575)&(dist((228,128,166))>40)&(dist(FUR)>25)
mouth=ndi.binary_dilation(mouth,iterations=4)
rose=(fe<1)&(dist((228,128,166))<38)&~mouth
hap=col.copy();rb=nconv(col,rose,10);hap[mouth]=rb[mouth]
S=4;big=Image.new('RGBA',(W*S,H*S),(0,0,0,0));d=ImageDraw.Draw(big)
def bez(p0,p1,p2,n=30):return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in np.linspace(0,1,n)]
top=bez((382,522),(450,534),(522,508));bot=bez((522,508),(470,592),(382,522))
poly=[(x*S,y*S) for x,y in top+bot];d.polygon(poly,fill=(58,18,48,255))
gr=Image.new('RGBA',big.size,(0,0,0,0));gd=ImageDraw.Draw(gr);gd.ellipse([(418*S,548*S),(492*S,585*S)],fill=(240,106,158,255))
mk=Image.new('L',big.size,0);ImageDraw.Draw(mk).polygon(poly,fill=255);big.paste(gr,(0,0),Image.composite(gr,Image.new('RGBA',big.size),mk).split()[3])
sm=np.asarray(big.resize((W,H),Image.LANCZOS)).astype(float);ma=sm[...,3:]/255
hap=hap*(1-ma)+sm[...,:3]*ma
layers['faceHappy']=rgba(A*facem,hap)
# ---- export, cropped, scaled ----
SC=.72;out={}
for k,arr in layers.items():
    im=Image.fromarray(arr,'RGBA');bb=im.getbbox();im=im.crop(bb)
    w2,h2=max(1,round(im.width*SC)),max(1,round(im.height*SC));im=im.resize((w2,h2),Image.LANCZOS)
    buf=io.BytesIO();im.save(buf,'WEBP',quality=86,method=6);b=buf.getvalue()
    out[k]={'x':bb[0],'y':bb[1],'w':bb[2]-bb[0],'h':bb[3]-bb[1],'src':'data:image/webp;base64,'+base64.b64encode(b).decode()}
    im.save(f'L_{k}.png');print(k,bb,len(b)//1024,'KB')
out['_meta']=meta
json.dump(out,open('art.json','w'))
print(meta)
