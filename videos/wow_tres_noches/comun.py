# -*- coding: utf-8 -*-
"""Utilidades de las escenas de «Tres noches» (tramo 4, 14-oct-2026): figuras por bandas de profundidad, cámara por
fotogramas clave, cambio de escena con MANCHA DE TINTA (procedural, sin cortes), cartelas y recuerdos colgados en el espacio."""
import math
import os

import cv2
import numpy as np

import grabado as GR
import grabado_3d as G3
from grabado import TINTA, W, H, G, pr, smooth


def env(t, t0, t1=None, a=0.4, b=0.4):
    """Envolvente 0..1: entra en t0 (en `a` s) y sale en t1 (en `b` s)."""
    u = smooth(pr(t, t0, t0 + a))
    if t1 is not None:
        u *= 1 - smooth(pr(t, t1, t1 + b))
    return u


def camara(t, kfs, base):
    """Cámara interpolada entre fotogramas clave [(t, {campos}), ...] sobre una cámara base (dict de Camara)."""
    return G3.kf_camara(t, [(tk, {**base, **d}) for tk, d in kfs])


def figuras(g, cam, objs, cortes=(2600.0, 1500.0, 900.0, 520.0)):
    """objs = [(X, Y, Z, fn)], fn(c) dibuja en la capa c. Se agrupan por bandas de profundidad DE CÁMARA (lejos -> cerca) y
    cada banda se compone con su desenfoque y su bruma (capa_prof). Lo que queda detrás de la cámara no se dibuja."""
    con = []
    for X, Y, Z, fn in objs:
        zc = float(cam.cam((X, Y, Z))[2])
        if zc > cam.cerca + 30:
            con.append((zc, fn))
    con.sort(key=lambda a: -a[0])
    lim = [9e9] + list(cortes) + [0.0]
    for zmax, zmin in zip(lim, lim[1:]):
        grupo = [c for c in con if zmin <= c[0] < zmax]
        if not grupo:
            continue
        zrep = float(np.median([c[0] for c in grupo]))
        with G3.capa_prof(g, cam, zrep) as c:
            for _, fn in grupo:
                fn(c)


_PNG = {}


def png(nombre):
    """Ruta del render REAL de un PNJ de WoW vanilla (nucleo/wow_png.py; índice ya bajado, sin navegador)."""
    if nombre not in _PNG:
        import wow_png
        _PNG[nombre] = wow_png.png(nombre)
    return _PNG[nombre]


def peg(objs, cam, t, nombre, X, Z, alto, Y=0.0, aura=0.0, color_aura=None, **kw):
    """Añade a `objs` una PEGATINA de WoW real de pie en (X, Y, Z) (grabado_3d.pegatina) con, si se da, el aura de
    contagio en la plancha de color. `nombre` = PNJ de Wowhead o «png:<archivo>» (recorte propio del video)."""
    ruta = png_video(nombre[4:]) if nombre.startswith("png:") else png(nombre)

    def fn(c, X=X, Y=Y, Z=Z, kw=kw, aura=aura):
        G3.pegatina(c, cam, ruta, X, Z, alto, t, Y=Y, **kw)
        if aura > 0.01:
            px, py, zc = cam.pt(X, Y - alto * 0.5, Z)
            c.acento_luz(px, py, alto * 0.75 * cam.k(zc), color_aura or GR.SANGRE, 0.7 * aura * kw.get("op", 1.0))
    objs.append((X, Y, Z, fn))


PNG_VIDEO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "png")


def png_video(nombre):
    """Recorte REAL propio del video (png/<nombre>.png: estatuas, relieves del tráiler de Blizzard)."""
    return os.path.join(PNG_VIDEO, nombre + ".png")


def relieve(g, cam, ruta, centro, U, ancho, alto, t, tinta=0.3, color=0.75, op=1.0, sem=0):
    """Imagen REAL plana (relieve tallado, mural) pasada a la estampa y ESTAMPADA sobre una superficie del mundo."""
    if op <= 0.01:
        return
    X, Y, Z = centro
    zc = float(cam.cam(centro)[2])
    if zc < cam.cerca + 20:
        return
    alto_px = int(min(max(alto * cam.k(zc), 24), 900) // 8 * 8 + 8)
    im, A, ac = G3._estampa_png(ruta, alto_px, tinta, color, 0, int(g.k) % 3, False, sem)
    s = G(t, im.shape[1], im.shape[0], alfa=True)
    s.im, s.alfa, s.ac = im, A, ac
    q = G3.quad_mundo(cam, centro, U, (0, 1, 0), ancho, alto)
    if q is not None:
        G3.estampar(g, s, q, sombra=0.0, op=op)


def en_suelo(cam, X, Z, Y=0.0):
    """(sx, sy, k) de un punto del mundo."""
    sx, sy, zc = cam.pt(X, Y, Z)
    return sx, sy, cam.k(zc)


# ------------------------------------------------------------------ cambio de escena: mancha de tinta
_RUIDO = {}
_GX, _GY = np.meshgrid(np.arange(240, dtype=np.float32) * 8 + 4, np.arange(135, dtype=np.float32) * 8 + 4)


def _ruido(sem):
    if sem not in _RUIDO:
        rng = np.random.default_rng(900 + sem)
        r = np.zeros((135, 240), np.float32)
        for k, amp in ((4, 1.0), (9, 0.55), (20, 0.3), (48, 0.14)):
            peq = rng.random((max(2, int(k * 135 / 240) + 1), k)).astype(np.float32)
            r += cv2.resize(peq, (240, 135), interpolation=cv2.INTER_CUBIC) * amp
        _RUIDO[sem] = (r - r.min()) / (np.ptp(r) + 1e-6)
    return _RUIDO[sem]


def mancha(img, u, cx=W / 2, cy=H / 2, sem=0):
    """Tinta que se derrama desde (cx, cy) hasta cubrir el cuadro (u 0..1), con borde de mancha viva y regueros."""
    if u <= 0.002:
        return img
    d = np.sqrt(((_GX - cx) / W) ** 2 + ((_GY - cy) / W) ** 2)
    dmax = max(math.hypot(x - cx, y - cy) for x in (0, W) for y in (0, H)) / W
    campo = 0.72 * d / dmax + 0.42 * _ruido(sem)
    m = np.clip((u * 1.2 - campo) / 0.025, 0, 1)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(m, (0, 0), 1.3)[..., None]
    tinta = np.float32(TINTA) * (0.92 + 0.08 * cv2.resize(_ruido(sem + 50), (W, H))[..., None])
    return img * (1 - m) + tinta * m


# ------------------------------------------------------------------ objetos planos colgados en el espacio
def cartela_colgada(g, cam, centro, texto, t, ancho=760, alto=150, op=1.0, px=46, cadenas=True, techo=None, giro=0.0,
                    U=(1, 0, 0), color=TINTA):
    """Filacteria colgada en el mundo (con cadenas hasta `techo` si se da): se pinta en un lienzo y se estampa en
    perspectiva (nunca pegada a la pantalla)."""
    if op <= 0.01:
        return
    s = G(t, int(ancho * 1.25), int(alto * 1.3), alfa=True)
    GR.cartela(s, s.W / 2, s.H / 2, ancho, texto, t, px=px, color=color)
    X, Y, Z = centro
    Ux, Uy, Uz = U
    if cadenas and techo is not None:
        for sg in (-1, 1):
            G3.trazo3d(g, cam, [(X + sg * ancho * 0.38 * Ux, techo, Z + sg * ancho * 0.38 * Uz),
                                (X + sg * ancho * 0.38 * Ux, Y - alto * 0.45, Z + sg * ancho * 0.38 * Uz)], 3.0, afilado=0.0,
                         op=op)
    q = G3.quad_mundo(cam, centro, U, (0, 1, 0), ancho * 1.25, alto * 1.3, giro)
    if q is not None:
        G3.estampar(g, s, q, sombra=0.3, off=(8, 12), op=op)


def recuerdo_colgado(g, cam, centro, U, nombre, seg, t, ancho=640, alto=400, texto=None, op=1.0, z=1.0, cx=0.5, cy=0.5,
                     tinta=0.25, giro=0.0, sem=0):
    """Un RECUERDO (clip real pasado a tinta, en marco grabado) colgado en una pared o en el aire, en perspectiva."""
    if op <= 0.01:
        return
    m = 70
    s = G(t, ancho + 2 * m, alto + 2 * m + (70 if texto else 0), alfa=True)
    oy = 70 if texto else 0
    GR.recuerdo(s, nombre, seg, m, m + oy, m + ancho, m + oy + alto, t, tinta=tinta, come=1.0, texto=texto, px=38, z=z,
                cx=cx, cy=cy, sem=sem)
    q = G3.quad_mundo(cam, centro, U, (0, 1, 0), s.W, s.H, giro)
    if q is not None:
        G3.estampar(g, s, q, sombra=0.55, off=(16, 22), desenfoque_sombra=14, op=op)
