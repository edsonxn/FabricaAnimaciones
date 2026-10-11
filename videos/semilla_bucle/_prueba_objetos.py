import sys
import os
import time
import cv2
import numpy as np

sys.path.insert(0, os.path.abspath("../../nucleo"))
sys.path.insert(0, os.path.abspath("."))

import boceto as B
import objetos as O

h = B.Hoja()

def hoja_de(fn, u=1.0):
    h.limpiar()
    fn(h, u)
    im = (np.clip(h.componer(), 0, 1) * 255).astype(np.uint8)
    return im

def escena1(h, u):
    # Pompón maduro inicial + semilla saliendo
    O.pompon_maduro().dibujar(h, 540, 1350, 1.2, u=u)
    O.semilla("feliz", "sonrisa", "abierto", brazos="saludo").dibujar(h, 640, 880, 1.1, rot=0.2, u=u)
    O.espiral_viento().dibujar(h, 450, 650, 0.8, rot=-0.2, u=u)

def escena2(h, u):
    # Vuelo en las alturas + mariposa
    O.paisaje_colinas().dibujar(h, 540, 1400, 1.0, u=u)
    O.casa_aldea().dibujar(h, 300, 1600, 0.9, u=u)
    O.semilla("abiertos", "sonrisa", "abierto", mira=1).dibujar(h, 540, 720, 1.0, rot=-0.1, u=u)
    O.mariposa(aleteo=0.5).dibujar(h, 780, 680, 1.1, rot=-0.2, u=u)

def escena3(h, u):
    # Tormenta: nubarrones, rayo, gota gigante, picada
    O.nube_tormenta().dibujar(h, 540, 420, 1.3, u=u)
    O.rayo().dibujar(h, 300, 480, 0.9, u=u)
    O.gota_gigante().dibujar(h, 540, 780, 1.0, u=u)
    O.semilla("miedo", "temblor", "plegado", brazos="agarrar").dibujar(h, 680, 1200, 0.9, rot=0.5, u=u)

def escena4(h, u):
    # Grieta en invierno + bufanda y nieve
    O.suelo_grieta().dibujar(h, 540, 1100, 1.0, u=u)
    O.semilla("dormido", "ronca", "pequeno").dibujar(h, 540, 1160, 0.85, u=u)
    O.bufanda().dibujar(h, 540, 1160, 0.85, u=u)
    O.copo_nieve(65).dibujar(h, 250, 750, 1.1, u=u)
    O.copo_nieve(50).dibujar(h, 820, 850, 0.9, u=u)

def escena5(h, u):
    # Primavera: raíces bajo tierra + brote elástico
    O.suelo_grieta().dibujar(h, 540, 1100, 1.0, u=u)
    O.raices().dibujar(h, 540, 1150, 1.0, u=u)
    O.brote_verde().dibujar(h, 540, 1020, 1.2, u=u)

def escena6(h, u):
    # Flor de diente de león abierta + abejita
    O.hoja_diente_leon().dibujar(h, 320, 1380, 1.1, rot=-0.5, u=u)
    O.hoja_diente_leon().dibujar(h, 760, 1380, 1.1, rot=0.5, flip=True, u=u)
    O.flor_amarilla(apertura=1.0).dibujar(h, 540, 1050, 1.25, u=u)
    O.abeja(aleteo=0.8).dibujar(h, 780, 820, 1.1, rot=-0.3, u=u)
    O.chispa_polen().dibujar(h, 420, 780, 1.2, u=u)

ims = []
for f in (escena1, escena2, escena3, escena4, escena5, escena6):
    t0 = time.time()
    im = hoja_de(f)
    print(f.__name__, round(time.time() - t0, 2), 's')
    ims.append(cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA))

fila1 = np.hstack(ims[:3])
fila2 = np.hstack(ims[3:])
mosaico = np.vstack([fila1, fila2])
cv2.imwrite('previews/objetos_semilla.jpg', cv2.cvtColor(mosaico, cv2.COLOR_RGB2BGR))
print("Guardado en previews/objetos_semilla.jpg")
