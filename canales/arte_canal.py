# -*- coding: utf-8 -*-
"""Arte del canal con el motor de la fábrica: foto de perfil (800x800) y banner (2560x1440).

Uso:  python canales/arte_canal.py "SAPIENS CON WIFI" ["Lema corto"] [estilo]
Salida en canales/arte/: <slug>_perfil.png, <slug>_banner.jpg y <slug>_revision.jpg (perfil en círculo a tamaño
real y a 48 px, y banner con las zonas visibles marcadas: TV = todo; computadora = franja central 2560x423;
celular = zona segura 1546x423). El nombre y el lema deben quedar dentro de la zona segura."""
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "nucleo"))

import cv2  # noqa: E402
import numpy as np  # noqa: E402

import estilos  # noqa: E402

NOMBRE = sys.argv[1] if len(sys.argv) > 1 else "SAPIENS CON WIFI"
LEMA = sys.argv[2] if len(sys.argv) > 2 else "Lo que hacían hace miles de años… y tú sigues haciendo"
estilos.activar(sys.argv[3] if len(sys.argv) > 3 else "doodle_psicodelico")

import dibujos as D  # noqa: E402
import efectos as E  # noqa: E402
import fondos as F  # noqa: E402
from dibujos import AMARILLO, BLANCO, CIAN, NEGRO  # noqa: E402
from motor import H, W, Lienzo, a_uint8, ancho_texto, componer  # noqa: E402

T = 0.37
SALIDA = os.path.join(RAIZ, "canales", "arte")
os.makedirs(SALIDA, exist_ok=True)
slug = re.sub(r"[^a-z0-9]+", "_", unicodedata.normalize("NFD", NOMBRE.lower()).encode("ascii", "ignore").decode()).strip("_")


def texto_ajustado(lz, s, x, y, px, ancho_max, fuente="snap", **kw):
    """Texto con el mayor tamaño <= px que quepa en ancho_max (px del lienzo 1920x1080)."""
    px = min(px, px * ancho_max / max(1.0, ancho_texto(s, fuente, px) * 1.08))
    lz.texto(s, x, y, px, fuente, **kw)
    return px


def pintar(lz, dibujar):
    lz.nuevo(T, wob=1.2)
    fondo = dibujar(lz)
    img = E.acabado(componer(fondo, lz.resolver(), boil=lz.boil), 3)
    return a_uint8(np.clip(img, 0, 1))


def perfil(lz):
    """Cara del cavernícola mirando a cámara, con el wifi saliendo de la cabeza. Se lee a 48 px."""
    fondo = F.rayos(T, "oceano", sat=0.9)
    D.personaje(lz, 960, 1470, 2.35, T, "cave", seed=11, mano_i=(-150, -190), mano_d=(150, -190),
                boca=-0.7, cejas=0.6, mirar=(0, 0), ojos="abiertos")
    D.wifi(lz, 960, 300, 1.55, col=AMARILLO, seed=7)
    return fondo


def banner(lz):
    xs = np.arange(W)[None, :] + (np.arange(H)[:, None] - H / 2) * 0.12
    m = np.clip((xs - W / 2) / 6 + 0.5, 0, 1).astype(np.float32)[..., None]
    fondo = F.cueva(T) * (1 - m) + F.rayos(T, "arcoiris", sat=0.85) * m
    for x, y, s, r in ((70, 300, 0.8, 0.3), (430, 820, 0.7, -0.3), (80, 900, 0.6, 0.5)):
        D.estarcido(lz, x, y, s, 1.0, rot=r)
    # personajes con la cara dentro de la franja que se ve en computadora (y 381-698)
    D.personaje(lz, 215, 930, 1.05, T, "cave", seed=11, mano_i=(-130, -200), mano_d=(150, -330),
                boca=0.5, cejas=0.8, mirar=(1, 0), ojos="abiertos")
    D.telefono(lz, 1840, 470, 0.5, 0.25, seed=97, t=T,
               pantalla=lambda lz: (D.wifi(lz, 0, 20, 0.9, col=CIAN, seed=98), D.ui_camara(lz, T, 99)))
    D.personaje(lz, 1700, 930, 1.05, T, "tu", seed=22, mano_i=(-150, -200), mano_d=(135, -440),
                boca=0.5, cejas=0.8, mirar=(-1, 0), ojos="abiertos")
    # nombre y lema en la zona segura de todos los dispositivos (x 380-1540, y 381-698)
    partes = NOMBRE.split(" ", 1)
    if len(partes) == 2 and len(NOMBRE) > 11:
        texto_ajustado(lz, partes[0], 960, 452, 150, 1060, color=AMARILLO, borde=NEGRO, borde_px=16, rot=-0.03, capa=2)
        texto_ajustado(lz, partes[1], 960, 566, 104, 1060, color=BLANCO, borde=NEGRO, borde_px=13, rot=-0.03, capa=2)
    else:
        texto_ajustado(lz, NOMBRE, 960, 520, 160, 1060, color=AMARILLO, borde=NEGRO, borde_px=16, rot=-0.03, capa=2)
    D.etiqueta(lz, 960, 642, LEMA, px=31, rot=0.01, seed=5)
    return fondo


lz = Lienzo()
# ---- perfil: recorte cuadrado central -> 800x800
p = pintar(lz, perfil)[:, (W - H) // 2:(W + H) // 2]
p = cv2.resize(p, (800, 800), interpolation=cv2.INTER_AREA)
ruta_p = os.path.join(SALIDA, f"{slug}_perfil.png")
cv2.imwrite(ruta_p, cv2.cvtColor(p, cv2.COLOR_RGB2BGR))
# ---- banner: 2560x1440
b = cv2.resize(pintar(lz, banner), (2560, 1440), interpolation=cv2.INTER_LANCZOS4)
ruta_b = os.path.join(SALIDA, f"{slug}_banner.jpg")
cv2.imwrite(ruta_b, cv2.cvtColor(b, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
print(ruta_p, f"{os.path.getsize(ruta_p) / 1e6:.2f} MB")
print(ruta_b, f"{os.path.getsize(ruta_b) / 1e6:.2f} MB")

# ---- hoja de revisión
rev_b = b.copy()
cv2.rectangle(rev_b, (0, 508), (2559, 931), (255, 255, 255), 4)            # computadora
cv2.rectangle(rev_b, (507, 508), (2053, 931), (255, 60, 60), 6)            # celular / zona segura
rev_b = cv2.resize(rev_b, (1280, 720), interpolation=cv2.INTER_AREA)
circ = np.full((720, 520, 3), 30, np.uint8)
mask = np.zeros((400, 400), np.uint8)
cv2.circle(mask, (200, 200), 200, 255, -1, cv2.LINE_AA)
p400 = cv2.resize(p, (400, 400), interpolation=cv2.INTER_AREA)
circ[40:440, 60:460] = (p400 * (mask[..., None] / 255) + 30 * (1 - mask[..., None] / 255)).astype(np.uint8)
m48 = cv2.resize(mask, (48, 48), interpolation=cv2.INTER_AREA)[..., None] / 255
p48 = cv2.resize(p, (48, 48), interpolation=cv2.INTER_AREA)
circ[500:548, 236:284] = (p48 * m48 + 30 * (1 - m48)).astype(np.uint8)
cv2.putText(circ, "perfil 400px y 48px", (60, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
rev = np.hstack([rev_b, circ])
ruta_r = os.path.join(SALIDA, f"{slug}_revision.jpg")
cv2.imwrite(ruta_r, cv2.cvtColor(rev, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print(ruta_r)
