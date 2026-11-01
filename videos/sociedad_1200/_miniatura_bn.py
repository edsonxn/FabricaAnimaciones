import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D=sys.argv[1]
src=Image.open(D+"/ancho2.png").convert("RGB")           # 1920x1080
W,H=1920,1080
wall=src.copy()
strip=src.crop((0,392,1920,762))                           # fila de robots
canvas=wall.copy()
# fondo: cielo de pared oscurecido arriba
rows=[(0.56,0.45,330,-90),(0.76,0.70,455,-40),(1.0,1.0,675,0)]  # escala, brillo, y_sup, desplazamiento x
rng=np.random.default_rng(3)
for esc_,br,y0,dx in rows:
    s=strip.resize((int(1920*esc_),int(370*esc_)),Image.LANCZOS)
    a=np.asarray(s).astype(np.float32)*br
    s=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    # repetir horizontalmente hasta cubrir
    al=np.ones((s.height,s.width),np.float32)
    n=int(34*esc_)
    al[:n,:]=np.linspace(0,1,n)[:,None]
    mask=Image.fromarray((al*255).astype(np.uint8))
    x=dx-int(rng.integers(0,200))
    while x<W:
        canvas.paste(s,(x,y0),mask); x+=s.width-8
# suelo oscuro bajo la fila delantera
cv=np.asarray(canvas).astype(np.float32)/255
g=cv@np.array([0.299,0.587,0.114],dtype=np.float32)          # B/N
# realzar los ojos (verde brillante) y el contraste
verde=(cv[...,1]>0.6)&(cv[...,0]<0.55)
g=np.clip((g-0.08)*1.45,0,1)**1.15
g[verde]=np.clip(g[verde]*1.4+0.35,0,1)
# viñeta y degradado oscuro arriba-izquierda para el texto
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
vig=1-0.55*(((xx-W/2)/(W/1.25))**2+((yy-H/2)/(H/1.1))**2)
g*=np.clip(vig,0.25,1)
txt=np.clip(1-((yy/ (H*0.55))**1.3)*0.0,0,1)
top=np.clip(1-yy/(H*0.47),0,1)**0.8
g*=1-0.78*top
g=np.clip(g+rng.normal(0,0.045,g.shape).astype(np.float32),0,1)   # grano
im=Image.fromarray((g*255).astype(np.uint8)).convert("RGB").resize((1280,720),Image.LANCZOS)
d=ImageDraw.Draw(im)
f1=ImageFont.truetype("C:/Windows/Fonts/impact.ttf",150)
f2=ImageFont.truetype("C:/Windows/Fonts/impact.ttf",118)
def t(s,xy,f):
    # sombra difusa + borde negro + blanco
    sh=Image.new("L",im.size,0); ImageDraw.Draw(sh).text(xy,s,font=f,fill=255,stroke_width=14)
    sh=sh.filter(ImageFilter.GaussianBlur(10))
    im.paste(Image.new("RGB",im.size,(0,0,0)),(0,0),sh.point(lambda v:int(v*0.9)))
    d.text(xy,s,font=f,fill=(255,255,255),stroke_width=7,stroke_fill=(0,0,0))
t("1,200 IAs",(42,28),f1)
t("CONSPIRARON",(42,178),f2)
im.save(D+"/miniatura_bn.jpg",quality=92); print(im.size)
