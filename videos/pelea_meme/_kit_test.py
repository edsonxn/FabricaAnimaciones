import sys, math
import numpy as np, cv2
import estilos; estilos.activar("guache")
import efectos as E
from motor import Lienzo, componer, a_uint8, W, H
import guache as G

lz = Lienzo()
def guardar(nombre, img):
    im = a_uint8(np.clip(E.acabado(img, 3), 0, 1))
    cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))

# --- fondos
tiles = []
for k in range(5):
    im = G.bioma_img(k, 1920.0 * k, 1.0)
    tiles.append(cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA))
row1 = np.hstack(tiles[:3]); row2 = np.hstack(tiles[3:] + [cv2.resize(G.fondo_mundo(1920 * 1 + 1000, 1.0), (640, 360))])
guardar_small = np.vstack([row1, row2])
cv2.imwrite("previews/bg_test.jpg", cv2.cvtColor(a_uint8(np.clip(guardar_small, 0, 1)), cv2.COLOR_RGB2BGR))

# --- personajes
lz.nuevo(1.0, wob=0.0)
bg = G.bioma_img(0, 0.0, 1.0)
GY = 800
G.hombre(lz, 260, GY, 1.2, 1.0, ph=1.0, paso=1.0, cara="normal", arma_f=G.chancla, brazo_f=(0.4, 0.2))
G.hombre(lz, 560, GY, 1.2, 1.0, cara="brava", brazo_f=(0.3, -0.2), arma_f=G.sarten, agach=0.4)
G.hombre(lz, 860, GY, 1.2, 1.0, cara="grito", sudor=1.0, arma_f=G.pez_espada, brazo_f=(0.2, 0.0))
G.hombre(lz, 1160, GY, 1.2, 1.0, cara="victoria", casco=1.0, arma_f=G.extintor, brazo_f=(0.1, -0.5))
G.hombre(lz, 1460, GY, 1.2, 1.0, cara="ko", arma_f=G.tapa_olla, brazo_f=(0.6, 0.1))
G.hombre(lz, 1700, GY, 1.2, 1.0, cara="asombro", sudor=1.0)
G.escorpion(lz, 420, 450, 0.7, 1.0, paso=1.0, pinza=0.6)
G.tiburon(lz, 1150, 300, 0.55, 1.0, boca=0.8)
G.platillo(lz, 1600, 230, 0.7, 1.0, haz=0.7)
img = componer(bg, lz.resolver(), boil=lz.boil); guardar("kit1", img)

lz.nuevo(1.0, wob=0.0)
bg = G.bioma_img(1, 1920.0, 1.0)
G.trex(lz, 500, GY, 0.85, 1.0, boca=0.7, brazos=1.0, paso=0.0)
G.dragon(lz, 1350, 950, 0.9, 1.0, boca=0.7)
img = componer(bg, lz.resolver(), boil=lz.boil); guardar("kit2", img)
print("ok")
