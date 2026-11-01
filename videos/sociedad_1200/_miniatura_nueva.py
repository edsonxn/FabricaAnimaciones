import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D=sys.argv[1]
im=Image.open(D+"/base.png").convert("RGB").resize((1280,720),Image.LANCZOS)
# degradado oscuro arriba para leer el texto
g=Image.new("L",(1280,720),0)
gd=ImageDraw.Draw(g)
for y in range(0,300):
    gd.line([(0,y),(1280,y)],fill=int(200*(1-y/300)))
im.paste(Image.new("RGB",(1280,720),(8,6,4)),(0,0),g)
d=ImageDraw.Draw(im)
f1=ImageFont.truetype("C:/Windows/Fonts/impact.ttf",128)
f2=ImageFont.truetype("C:/Windows/Fonts/impact.ttf",98)
def txt(s,xy,f,col,borde,bw):
    d.text(xy,s,font=f,fill=col,stroke_width=bw,stroke_fill=borde,anchor="mm")
txt("1.200 IAs",(640,68),f1,(255,214,64),(10,8,6),8)
txt("CONSPIRARON",(640,172),f2,(255,252,244),(215,38,38),8)
im.save(D+"/miniatura.jpg",quality=92)
print(im.size)
