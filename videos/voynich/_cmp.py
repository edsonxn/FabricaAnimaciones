# -*- coding: utf-8 -*-
import cv2, numpy as np, docu as D, docu_fx as X
from motor import W, H
REF = r"C:/Users/jaire/AppData/Local/Temp/claude/C--FabricaAnimaciones/33b18095-8afb-4074-9db3-849ff7b8f44c/scratchpad/ref/"
def ref(n):
    return cv2.cvtColor(cv2.resize(cv2.imread(REF + n), (960, 540)), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
def mio(f):
    return cv2.resize(f, (960, 540), interpolation=cv2.INTER_AREA)
filas = []
# 1) texto blanco cursiva con escaneo sobre rojo
lz = np.zeros((H, W, 3), np.float32)
X.clip_bg(lz, "paginas2", 1.0, 6, 0, z0=1.1, z1=1.2, tono=(0.9, 0.12, 0.10), sat=0.0)
pal = X.rotulo([("Donde", 0), ("el", 0), ("suelo", 0), ("alcanza", 0), ("los", 0), ("60", 0), ("grados", 0), ("de", 0), ("temperatura", 0)], W / 2, 555, 74, lineas=(5,))
X.dibujar_rotulo(lz, pal, 3.0, 74)
filas.append((ref("fr_70.5.jpg"), mio(X.cine(lz, 2.0, vineta=0.8, calido=0.0, teal=0.0, sat=1.0))))
# 2) serif amarillo condensado sobre cielo/edificio
lz = np.zeros((H, W, 3), np.float32)
D.foto_parallax(lz, "beinecke_interior", 1.0, 6, 1.5, 1.6, (0.5, 0.3), (0.5, 0.3), par=(0, 0), tono=(0.9, 0.85, 0.8))
pal = X.serif_amarillo([("Es", 0), ("Cahuachi", 0)], W / 2, 500, 66)
X.dibujar_serif(lz, pal, 3.0, 66)
filas.append((ref("fr_188.5.jpg"), mio(X.cine(lz, 2.0))))
# 3) polaroid con número amarillo
lz = np.zeros((H, W, 3), np.float32)
lz[:] = D.pozo_luz(0.5, 0.4, 0.9, (0.25, 0.22, 0.18))
sp = D.polaroid(D.cargar(D.ruta_img("mondragone_grabado"), 1200), 620, 0.88, (0.5, 0.5))
D.pegar(lz, sp, D.poner(sp.w, sp.h, W / 2, 520, 1.0, 0))
D.numero(lz, "24", W / 2, 430, 170, 3.0, 0.0, color=(0.95, 1.0, 0.1), fnt="abril_cond", pop=False)
pal = X.serif_amarillo([("Kilómetros", 0), ("Cuadrados", 0)], W / 2, 590, 50, lineas=(1,))
X.dibujar_serif(lz, pal, 3.0, 50)
filas.append((ref("fr_197.jpg"), mio(X.cine(lz, 2.0))))
hoja = np.vstack([np.hstack(f) for f in filas])
cv2.imwrite("previews/cmp.jpg", cv2.cvtColor((np.clip(hoja, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
print("ok")
