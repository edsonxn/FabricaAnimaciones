# -*- coding: utf-8 -*-
import cv2, numpy as np, docu as D, docu_fx as X
from motor import W, H
def base(nombre, t=2.0, tono=(0.8, 0.72, 0.62)):
    lz = np.zeros((H, W, 3), np.float32)
    X.clip_bg(lz, nombre, t, 6, 1.0, z0=1.05, z1=1.15, tono=tono)
    return lz
cuadros = []
# A: serif amarillo condensado, mediano, como la referencia (centrado sobre la imagen, palabra a palabra)
lz = base("pluma")
pal = D.bloque_texto([[("Nadie", 0), ("Ha", 0), ("Podido", 0), ("Leerlo", 0)]], W * 0.5, H * 0.66, "serif_cond", 84, D.AMARILLO)
D.dibujar_bloque(lz, pal, 3.0, "serif_cond", 84, deriva=0)
cuadros.append(D.acabado(lz, 2.0))
# B: cursiva blanca con escaneo + línea punteada (tu captura '134 METROS')
lz = base("paginas1", tono=(0.6, 0.55, 0.5))
X.linea_medida(lz, (300, 640), (1620, 600), 1.0, "240 páginas", 3.0, 0.0, 78)
cuadros.append(D.acabado(lz, 2.0))
# C: subtítulo pequeño en cursiva
lz = base("biblioteca", tono=(0.9, 0.78, 0.62))
cap = X.titular([("Cuando", 0), ("de", 0), ("pronto,", 0), ("ve", 0), ("algo", 0), ("que", 0), ("no", 0), ("entiende", 0)], W / 2, H * 0.80, 40, "pop_sbi", lineas=(3,), espacio=0.22)
X.caption(lz, cap, 3.0, 40)
cuadros.append(D.acabado(lz, 2.0))
# D: cifra roja + serif blanco condensado
lz = base("monedas", tono=(0.7, 0.66, 0.6))
D.numero(lz, "600", 640, 420, 280, 3.0, 0.0, color=D.ROJO, fnt="abril_cond", pop=False)
pal = D.bloque_texto([[("Ducados", 0), ("De", 0), ("Oro", 0)]], 640, 640, "serif_cond", 76, D.BLANCO)
D.dibujar_bloque(lz, pal, 3.0, "serif_cond", 76, deriva=0)
cuadros.append(D.acabado(lz, 2.0))
hoja = np.vstack([np.hstack(cuadros[:2]), np.hstack(cuadros[2:])])
hoja = cv2.resize(hoja, (1920, 1080), interpolation=cv2.INTER_AREA)
cv2.imwrite("previews/letra_opciones.jpg", cv2.cvtColor((np.clip(hoja, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
print("ok")
