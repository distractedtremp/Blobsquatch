import numpy as np, json
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
im=np.asarray(Image.open('master.jpg').convert('RGB')).astype(float)
H,W,_=im.shape; R,G,B=im[...,0],im[...,1],im[...,2]
ratio=G/np.maximum(R,1)
core=(R>118)&(B>80)&(G>0.42*R)&(R>G+25)
lab,n=ndi.label(core);sz=ndi.sum(core,lab,range(1,n+1));core=lab==(1+np.argmax(sz))
c0=ndi.binary_closing(core,iterations=3);filled=ndi.binary_fill_holes(c0);holes=filled&~c0
bgh=ndi.binary_dilation(holes&(G>R+5),iterations=2)&holes
hl,hn=ndi.label(holes)
for i in range(1,hn+1):
    m=hl==i
    if (m&bgh).sum()>0.3*m.sum(): holes[m]=False
core=c0|holes
core=ndi.binary_erosion(core,iterations=2)
# ---- matting in an edge band ----
band=ndi.binary_dilation(core,iterations=26)&~core
bgm=~ndi.binary_dilation(core,iterations=30)
def nconv(mask,sig):
    w=ndi.gaussian_filter(mask.astype(float),sig)
    out=np.stack([ndi.gaussian_filter(im[...,c]*mask,sig) for c in range(3)],-1)
    return out/np.maximum(w,1e-6)[...,None]
bgc=nconv(bgm,18); chc=nconv(core,10)
d=chc-bgc; a=np.sum((im-bgc)*d,-1)/np.maximum(np.sum(d*d,-1),1)
a=np.clip(a,0,1); alpha=np.where(core,1.0,np.where(band,a,0.0))
alpha=np.where(alpha<.06,0,alpha)
alpha[band&(G>R-8)]=0
alpha[band&(R<95)]=0
# unpremultiply edge colour
col=im.copy()
eb=band&(alpha>0)
col[eb]=np.clip((im[eb]-(1-alpha[eb,None])*bgc[eb])/np.maximum(alpha[eb,None],.25),0,255)
# blend edge colour toward the local character colour where alpha is small (kills teal fringe)
wgt=np.clip(alpha*1.6,0,1)[...,None]
col=np.where(eb[...,None],col*wgt+chc*(1-wgt),col)
# drop the ground shadow (dark) from the alpha: only pinkish pixels survive
dark=(R<110)&~ndi.binary_fill_holes(core)
alpha[dark&~core]=0
full=np.dstack([col,alpha*255]).astype(np.uint8)
Image.fromarray(full,'RGBA').save('cut_full.png')
np.save('alpha.npy',alpha)
print('ok',alpha.sum())
