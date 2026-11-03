import sys; sys.path.insert(0, "C:/FabricaAnimaciones/nucleo")
import numpy as np, mg_cod as C
from PIL import Image
W,H=1920,1080
y=np.linspace(0,1,H)[:,None]*np.ones((1,W)); x=np.linspace(0,1,W)[None,:]*np.ones((H,1))
F=Image.fromarray(np.stack([60+80*x+30*y, 70+60*y+20*x, 50+40*x],-1).astype(np.uint8)).convert("RGBA")
def poner(fn,dt,dur=6,x=.5,y=.5,marcas=None):
    f=F.copy(); a=fn(dt,dur,marcas); im=Image.fromarray(a[...,[2,1,0,3]])
    f.alpha_composite(im,(int(W*x-im.width/2),int(H*y-im.height/2))); return f
piezas=[
 poner(C.puesto(25,"La tele que nadie mira","MISIÓN 02 / SANGRE FRÍA / NUEVA YORK"),4.0,y=.78),
 poner(C.ficha("Guía de TV","Princess Starfish 2, *Operation Saber 3* y Excessive Cakes: películas que no existen.","INTEL / MISIÓN 02"),3.5,x=.7,y=.4),
 poner(C.fallida("Misión fallida","Deshonraste a tu país dañando un retrato del Líder Supremo"),3.0),
 poner(C.logro("Jamás te olvidaremos","Recupera las chapas de Gaz"),1.5,y=.15),
 poner(C.radio("War Pig","El tanque del pantano de CoD 4"),1.5,y=.3),
 poner(C.codigo("8410","Caja fuerte / prisión","Chapas de Gaz"),3.5),
 poner(C.sello(),1.0),
 poner(C.linea("¿Estás roto?",[(2019,"MW","Price a Gaz"),(2022,"MW2","Se repite"),(2023,"MW3","Otra vez"),(2026,"MW4","Gaz a Price")]),5.0),
 poner(C.espejo("Dos sagas, un compositor",(2007,"CoD 4",["Final del puente","Price mata a Zakhaev"]),(2026,"MW4",["Post-créditos","Laswell borra la 141"]),"Stephen Barton"),4.0),
 poner(C.balanza("Lo que el juego castiga",[("Tiro de advertencia a civiles",True,"nada"),("Disparar al retrato",False,"ejecución"),("Mentir por la familia",False,"otra soga")]),4.0),
]
hoja=Image.new("RGB",(640*2,360*5))
for i,p in enumerate(piezas):
    hoja.paste(p.convert("RGB").resize((640,360)),((i%2)*640,(i//2)*360))
hoja.save("E:/FabricaAnimaciones/videos/cod_mw4_secretos/previews/kit_cod.jpg",quality=88)
print("ok")
