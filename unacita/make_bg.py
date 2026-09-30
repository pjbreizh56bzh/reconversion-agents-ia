"""Fond A4 à partir de l'image du courrier : on garde bordure, drapeaux, personnages, monument,
et on efface le texte du courrier sous un panneau clair qui accueille le texte du PV."""
import sys
from PIL import Image, ImageDraw, ImageFilter
src,out=sys.argv[1],sys.argv[2]
OPACITE=float(sys.argv[3]) if len(sys.argv)>3 else 0.55   # 1 = image d'origine, 0 = blanc
im=Image.open(src).convert("RGB")            # 1024x1536
W,H=im.size
# efface la signature manuscrite « Le Président » du courrier (encre bleu foncé, bas droite)
import numpy as np, cv2
a=np.array(im); x0,x1,y0,y1=700,950,1240,1400
reg=a[y0:y1,x0:x1].astype(int); r,g,b=reg[...,0],reg[...,1],reg[...,2]
ink=((b>r+25)&(b<175)&(r<110)).astype(np.uint8)*255
ink=cv2.dilate(ink,np.ones((7,7),np.uint8),iterations=2)
m=np.zeros(a.shape[:2],np.uint8); m[y0:y1,x0:x1]=ink
a=cv2.inpaint(a,m,7,cv2.INPAINT_TELEA); im=Image.fromarray(a)
# panneau (coordonnées dans l'image source)
L,T,R,B = 205,150,892,1285
mask=Image.new("L",(W,H),0)
ImageDraw.Draw(mask).rounded_rectangle((L,T,R,B),radius=26,fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(9))
panel=Image.new("RGB",(W,H),(255,255,255))
im=Image.composite(panel,im,mask)
im=Image.blend(Image.new('RGB',im.size,(255,255,255)),im,OPACITE)   # fond plus transparent
im=im.resize((2480,3508),Image.LANCZOS)      # A4 à 300 dpi
im.save(out,quality=90)
print(out,im.size)
