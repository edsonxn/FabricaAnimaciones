# -*- coding: utf-8 -*-
"""Retratos (bustos grandes y expresivos) del estilo Kurzgesagt: ojos con destello de estrella de 4 puntas, cejas gruesas, rubor, pelo en 2-3 tonos con filo de luz,
parpadeo, boca que habla, respiración y leve balanceo. Personajes históricos de México diseñados originalmente (rasgos y vestuario de época).

retrato(lz, x, y, s, quien, t, emocion='neutro', habla=0.0, mirar=0.0, alfa=1.0, flip=1, luz_borde=(255, 220, 90))
  (x, y) = base del cuello, s = px por unidad de cabeza (la cabeza mide ~2,3 unidades de alto: s=170 -> ~390 px).
"""
import math

import numpy as np

import plano as P
from motor import circulo, elipse, rect_red, h01, catmull, smooth

PIEL = dict(clara=(246, 206, 170), media=(232, 178, 130), trigueña=(206, 146, 100), morena=(172, 112, 78), oscura=(130, 84, 60))
SOMBRA_PIEL = (120, 52, 76)


def _p(pts, x, y, s, flip=1):
    a = np.asarray(pts, float)
    return np.stack([x + a[:, 0] * s * flip, y + a[:, 1] * s], 1)


def _poly(lz, pts, x, y, s, color, flip=1, alfa=1.0, capa=None):
    lz.relleno(_p(pts, x, y, s, flip), color, alfa=alfa, capa=capa)


def _ell(lz, cx, cy, rx, ry, x, y, s, color, flip=1, alfa=1.0, rot=0.0):
    lz.relleno(elipse(x + cx * s * flip, y + cy * s, rx * s, ry * s, rot * flip, 24), color, alfa=alfa)


# personajes: rasgos (originales; vestuario de la época)
QUIEN = {
    "hidalgo": dict(piel="clara", edad=0.85, pelo=(236, 234, 244), calvo=True, cejas=(226, 224, 236), cejas_g=1.2, ojos=(110, 84, 62), cuello="alzacuello", ropa=(48, 42, 66), ropa2=(255, 255, 255), fw=1.0, nariz=1.1,
                    bigote=None, patillas=None, gorro=None, arrugas=True),
    "morelos": dict(piel="trigueña", edad=0.55, pelo=(52, 38, 40), cejas=(46, 32, 34), cejas_g=1.4, ojos=(60, 40, 36), cuello="camisa", ropa=(134, 92, 62), ropa2=(246, 242, 232), fw=1.05, nariz=1.2,
                    bigote=None, patillas=None, gorro="pañuelo", pano=(250, 248, 244), arrugas=False),
    "allende": dict(piel="clara", edad=0.4, pelo=(60, 44, 40), cejas=(56, 40, 36), cejas_g=1.0, ojos=(70, 90, 110), cuello="casaca", ropa=(52, 86, 160), ropa2=(206, 52, 60), fw=0.96, nariz=1.0,
                    bigote="fino", patillas="largas", gorro="bicornio", arrugas=False),
    "aldama": dict(piel="media", edad=0.4, pelo=(40, 30, 32), cejas=(40, 30, 32), cejas_g=1.1, ojos=(54, 38, 34), cuello="casaca", ropa=(92, 122, 192), ropa2=(246, 242, 232), fw=0.98, nariz=1.0,
                   bigote="fino", patillas="cortas", gorro="bicornio", arrugas=False),
    "josefa": dict(piel="clara", edad=0.35, pelo=(56, 38, 36), cejas=(52, 36, 34), cejas_g=0.8, ojos=(80, 56, 44), cuello="vestido", ropa=(214, 92, 138), ropa2=(250, 232, 200), fw=0.92, nariz=0.85,
                   bigote=None, patillas=None, gorro="peinado", arrugas=False, pesta=True),
    "leona": dict(piel="clara", edad=0.25, pelo=(48, 34, 34), cejas=(48, 34, 34), cejas_g=0.8, ojos=(64, 48, 40), cuello="vestido", ropa=(232, 220, 190), ropa2=(206, 60, 70), fw=0.9, nariz=0.8,
                  bigote=None, patillas=None, gorro="peinado", arrugas=False, pesta=True),
    "iturbide": dict(piel="clara", edad=0.45, pelo=(70, 50, 40), cejas=(62, 44, 38), cejas_g=1.2, ojos=(80, 100, 90), cuello="casaca", ropa=(200, 48, 60), ropa2=(250, 206, 90), fw=1.0, nariz=1.1,
                     bigote="fino", patillas="largas", gorro="bicornio_plumas", arrugas=False),
    "calleja": dict(piel="clara", edad=0.7, pelo=(190, 186, 196), cejas=(150, 146, 156), cejas_g=1.3, ojos=(70, 80, 100), cuello="casaca", ropa=(170, 54, 62), ropa2=(250, 206, 90), fw=1.1, nariz=1.2,
                    bigote=None, patillas="largas", gorro="bicornio", arrugas=True, cara_dura=True),
    "napoleon": dict(piel="clara", edad=0.4, pelo=(86, 62, 48), cejas=(70, 50, 42), cejas_g=1.1, ojos=(80, 100, 130), cuello="casaca", ropa=(46, 76, 150), ropa2=(250, 244, 230), fw=1.0, nariz=1.0,
                     bigote=None, patillas="cortas", gorro="bicornio_lado", arrugas=False),
    "virrey": dict(piel="clara", edad=0.7, pelo=(246, 244, 250), cejas=(200, 198, 206), cejas_g=1.0, ojos=(80, 70, 70), cuello="casaca", ropa=(146, 40, 62), ropa2=(250, 206, 90), fw=1.1, nariz=1.1,
                   bigote=None, patillas=None, gorro="peluca", arrugas=True),
    "guerrero": dict(piel="oscura", edad=0.45, pelo=(30, 26, 32), cejas=(30, 26, 32), cejas_g=1.3, ojos=(36, 28, 28), cuello="camisa", ropa=(214, 190, 140), ropa2=(204, 56, 56), fw=1.02, nariz=1.1,
                     bigote="grueso", patillas=None, gorro="palma", arrugas=False),
    "victoria": dict(piel="morena", edad=0.5, pelo=(50, 38, 36), cejas=(48, 36, 34), cejas_g=1.2, ojos=(50, 36, 32), cuello="camisa", ropa=(112, 150, 108), ropa2=(246, 242, 232), fw=1.0, nariz=1.1,
                     bigote="grueso", patillas="cortas", gorro=None, arrugas=False),
    "matamoros": dict(piel="media", edad=0.45, pelo=(44, 32, 32), cejas=(44, 32, 32), cejas_g=1.2, ojos=(50, 36, 34), cuello="casaca", ropa=(70, 120, 92), ropa2=(246, 242, 232), fw=1.0, nariz=1.0,
                      bigote="fino", patillas="cortas", gorro="bicornio", arrugas=False),
    "galeana": dict(piel="trigueña", edad=0.5, pelo=(40, 30, 30), cejas=(40, 30, 30), cejas_g=1.4, ojos=(44, 32, 30), cuello="camisa", ropa=(96, 80, 90), ropa2=(246, 242, 232), fw=1.08, nariz=1.2,
                    bigote="grueso", patillas="largas", gorro="palma", arrugas=False),
    "campesino": dict(piel="morena", edad=0.5, pelo=(36, 28, 30), cejas=(36, 28, 30), cejas_g=1.2, ojos=(40, 30, 28), cuello="camisa", ropa=(246, 242, 232), ropa2=(204, 56, 56), fw=1.02, nariz=1.1,
                      bigote="fino", patillas=None, gorro="palma", arrugas=False),
    "campesina": dict(piel="morena", edad=0.4, pelo=(34, 26, 30), cejas=(34, 26, 30), cejas_g=1.0, ojos=(40, 30, 28), cuello="rebozo", ropa=(60, 124, 176), ropa2=(240, 190, 80), fw=0.95, nariz=0.9,
                      bigote=None, patillas=None, gorro="trenzas", arrugas=False, pesta=True),
    "criollo": dict(piel="clara", edad=0.45, pelo=(60, 44, 40), cejas=(56, 40, 36), cejas_g=1.0, ojos=(70, 56, 46), cuello="levita", ropa=(46, 42, 62), ropa2=(250, 248, 244), fw=1.0, nariz=1.0,
                    bigote="fino", patillas="largas", gorro=None, arrugas=False),
    "peninsular": dict(piel="clara", edad=0.55, pelo=(210, 206, 214), cejas=(160, 156, 166), cejas_g=1.1, ojos=(80, 80, 100), cuello="levita", ropa=(146, 40, 62), ropa2=(250, 206, 90), fw=1.05, nariz=1.15,
                       bigote=None, patillas=None, gorro="peluca", arrugas=True),
    "esclavo": dict(piel="oscura", edad=0.5, pelo=(28, 24, 28), cejas=(28, 24, 28), cejas_g=1.2, ojos=(34, 28, 28), cuello="camisa", ropa=(226, 214, 190), ropa2=(200, 180, 150), fw=1.0, nariz=1.2,
                    bigote=None, patillas=None, gorro=None, arrugas=False),
    "fernando": dict(piel="clara", edad=0.3, pelo=(60, 44, 40), cejas=(56, 40, 36), cejas_g=1.0, ojos=(80, 70, 80), cuello="casaca", ropa=(150, 40, 66), ropa2=(250, 206, 90), fw=1.0, nariz=1.5,
                     bigote=None, patillas="cortas", gorro="corona", arrugas=False),
    "carlos": dict(piel="clara", edad=0.85, pelo=(246, 244, 250), cejas=(210, 208, 218), cejas_g=1.2, ojos=(80, 78, 96), cuello="casaca", ropa=(150, 40, 66), ropa2=(250, 206, 90), fw=1.12, nariz=1.5,
                   bigote=None, patillas=None, gorro="peluca", arrugas=True),
    "jose": dict(piel="clara", edad=0.5, pelo=(70, 52, 44), cejas=(60, 44, 40), cejas_g=1.1, ojos=(90, 90, 100), cuello="casaca", ropa=(60, 90, 170), ropa2=(250, 206, 90), fw=1.06, nariz=1.1,
                 bigote=None, patillas="largas", gorro="corona", arrugas=False),
    "yermo": dict(piel="clara", edad=0.6, pelo=(60, 54, 60), cejas=(50, 46, 50), cejas_g=1.4, ojos=(60, 56, 66), cuello="levita", ropa=(52, 46, 66), ropa2=(250, 248, 244), fw=1.04, nariz=1.2,
                  bigote="grueso", patillas="largas", gorro=None, arrugas=False, cara_dura=True),
    "mina": dict(piel="clara", edad=0.2, pelo=(56, 40, 36), cejas=(52, 38, 34), cejas_g=1.0, ojos=(80, 100, 90), cuello="casaca", ropa=(62, 120, 90), ropa2=(246, 242, 232), fw=0.95, nariz=1.0,
                 bigote="fino", patillas="cortas", gorro=None, arrugas=False),
    "odonoju": dict(piel="clara", edad=0.7, pelo=(200, 196, 206), cejas=(170, 166, 176), cejas_g=1.2, ojos=(80, 90, 110), cuello="casaca", ropa=(52, 86, 160), ropa2=(250, 206, 90), fw=1.05, nariz=1.1,
                    bigote=None, patillas="largas", gorro="bicornio", arrugas=True),
    "porfirio": dict(piel="media", edad=0.8, pelo=(236, 234, 240), cejas=(220, 218, 226), cejas_g=1.4, ojos=(60, 50, 50), cuello="casaca", ropa=(40, 52, 96), ropa2=(250, 206, 90), fw=1.1, nariz=1.1,
                     bigote="grueso_blanco", patillas=None, gorro=None, arrugas=True),
}


def _emocion(e):
    """(inclinación de cejas, altura cejas, abertura ojo, curva boca, abertura boca)"""
    return dict(neutro=(0.0, 0.0, 1.0, 0.0, 0.0), alegre=(-0.05, 0.05, 0.85, 0.55, 0.25), serio=(0.12, -0.04, 0.9, -0.12, 0.0), sorpresa=(-0.10, 0.20, 1.25, 0.0, 0.55),
                miedo=(-0.30, 0.16, 1.3, -0.2, 0.35), enojo=(0.42, -0.06, 0.8, -0.4, 0.2), triste=(-0.34, 0.02, 0.8, -0.5, 0.0), pensativo=(-0.12, 0.10, 0.95, -0.05, 0.0),
                grito=(0.2, 0.08, 1.1, 0.0, 0.9))[e]


def retrato(lz, x, y, s, quien, t=0.0, emocion="neutro", habla=0.0, mirar=0.0, alfa=1.0, flip=1, luz_borde=(255, 220, 90), seed=0, mano=None):
    import kz_retrato_real as RR
    if RR.hay(quien):                       # personaje histórico real: cuadro de época enmarcado (no el busto dibujado)
        return RR.retrato(lz, x, y, s, quien, t, emocion, habla, mirar, alfa, flip, luz_borde, seed, mano)
    R = QUIEN[quien]
    inc_b, alt_b, ab_ojo, curva_b, ab_b = _emocion(emocion)
    fw = R["fw"]
    piel = PIEL[R["piel"]]
    sombra = P.mezcla(piel, SOMBRA_PIEL, 0.30)
    luzp = P.aclarar(piel, 0.22)
    ph = t * 1.3 + seed
    resp = 0.012 * math.sin(t * 1.9 + seed)
    sway = 0.012 * math.sin(t * 0.8 + seed * 2.0)
    y = y + resp * s * 10
    x = x + sway * s * 4
    # parpadeo cada ~3,4 s, 0,16 s cerrado
    ciclo = (t + seed * 1.7) % 3.4
    cierre = max(0.0, 1.0 - abs(ciclo - 3.3) / 0.08) if ciclo > 3.2 else 0.0
    ab = ab_ojo * (1 - 0.92 * cierre)
    boca_a = ab_b + habla * (0.28 + 0.26 * math.sin(t * 13.0 + seed)) if habla > 0 else ab_b
    A = alfa
    # --- hombros / torso
    _torso(lz, x, y, s, R, flip, A)
    # --- cuello
    _poly(lz, [(-0.52, -0.9), (0.52, -0.9), (0.60, 0.5), (-0.60, 0.5)], x, y, s, sombra, flip, A)
    _poly(lz, [(-0.52, -0.9), (0.36, -0.9), (0.44, 0.5), (-0.60, 0.5)], x, y, s, P.mezcla(piel, sombra, 0.45), flip, A)
    # sombra bajo la barbilla
    _ell(lz, 0.0, -0.55, 0.62, 0.30, x, y, s, sombra, flip, A * 0.85)
    # --- orejas
    for sd in (-1, 1):
        _ell(lz, sd * 1.0 * fw, -1.55, 0.17, 0.30, x, y, s, piel if sd < 0 else sombra, flip, A)
        _ell(lz, sd * 1.0 * fw, -1.55, 0.09, 0.19, x, y, s, sombra if sd < 0 else P.oscurecer(sombra, 0.1), flip, A * 0.6)
    # --- pelo trasero
    _pelo_atras(lz, x, y, s, R, flip, A)
    # --- cabeza
    cara = [(0.0, -2.78), (0.62, -2.62), (0.98 * fw, -2.1), (1.02 * fw, -1.5), (0.86 * fw, -0.95), (0.52 * fw, -0.50), (0.0, -0.36), (-0.52 * fw, -0.50), (-0.86 * fw, -0.95), (-1.02 * fw, -1.5),
            (-0.98 * fw, -2.1), (-0.62, -2.62)]
    cc = catmull(np.array(cara), 8, True)
    lz.relleno(_p(cc, x, y, s, flip), sombra, alfa=A)
    if luz_borde is not None:
        lz.relleno(_p(np.array([(px - 0.05, py) for px, py in cc]), x, y, s, flip), luz_borde, alfa=A * 0.55)
        lz.relleno(_p(cc, x, y, s, flip), sombra, alfa=A)
    c2 = catmull(np.array([(px * 0.965 - 0.04, py * 0.985 - 0.02) for px, py in cara]), 8, True)
    lz.relleno(_p(c2, x, y, s, flip), piel, alfa=A)
    _ell(lz, -0.45, -2.15, 0.34, 0.20, x, y, s, luzp, flip, A * 0.35, rot=-0.4)
    # rubor
    for sd in (-1, 1):
        _ell(lz, sd * 0.66 * fw, -1.18, 0.24, 0.15, x, y, s, (236, 96, 96), flip, A * 0.30)
    # --- nariz
    n = R["nariz"]
    _poly(lz, catmull(np.array([(0.04, -1.55), (0.20 * n, -1.28), (0.18 * n, -1.12), (0.0, -1.08), (-0.14 * n, -1.14), (-0.10 * n, -1.30)]), 5, True), x, y, s, sombra, flip, A * 0.9)
    _ell(lz, 0.02, -1.20, 0.17 * n, 0.14 * n, x, y, s, piel, flip, A)
    _ell(lz, -0.03, -1.26, 0.07 * n, 0.05 * n, x, y, s, luzp, flip, A * 0.7)
    # --- ojos
    dx = mirar * 0.06
    for sd in (-1, 1):
        ex = sd * 0.43 * fw
        ey = -1.66
        _ell(lz, ex, ey, 0.25, 0.17 * ab + 0.012, x, y, s, (252, 250, 246), flip, A)
        if ab > 0.12:
            _ell(lz, ex + dx * sd * 0 + dx, ey, 0.145, 0.145 * min(1.0, ab * 1.1), x, y, s, R["ojos"], flip, A)
            _ell(lz, ex + dx, ey, 0.075, 0.075 * min(1.0, ab * 1.1), x, y, s, (26, 20, 30), flip, A)
            # destello de estrella de 4 puntas + círculo
            hx, hy = ex + dx + 0.06, ey - 0.06
            for ang in (0, 1.5708):
                _poly(lz, [(hx + math.cos(ang) * 0.075, hy + math.sin(ang) * 0.075), (hx + math.cos(ang + 1.5708) * 0.018, hy + math.sin(ang + 1.5708) * 0.018),
                           (hx - math.cos(ang) * 0.075, hy - math.sin(ang) * 0.075), (hx - math.cos(ang + 1.5708) * 0.018, hy - math.sin(ang + 1.5708) * 0.018)], x, y, s, (255, 255, 255), flip, A)
            _ell(lz, ex + dx - 0.05, ey + 0.05, 0.026, 0.026, x, y, s, (255, 255, 255), flip, A * 0.9)
        # párpado superior (sombra) y línea
        _poly(lz, [(ex - 0.27, ey - 0.02 * ab), (ex - 0.14, ey - 0.20 * ab - 0.02), (ex + 0.14, ey - 0.20 * ab - 0.02), (ex + 0.27, ey - 0.02 * ab), (ex + 0.20, ey - 0.09 * ab), (ex - 0.20, ey - 0.09 * ab)],
              x, y, s, P.oscurecer(sombra, 0.35), flip, A * 0.75)
        if R.get("pesta"):
            _poly(lz, [(ex - 0.27, ey), (ex - 0.30, ey - 0.12), (ex - 0.14, ey - 0.20 * ab - 0.02), (ex + 0.14, ey - 0.20 * ab - 0.02), (ex + 0.30, ey - 0.12), (ex + 0.27, ey)], x, y, s, (52, 38, 44), flip, A * 0.55)
        # cejas
        k = 1 + 0.45 * (R["cejas_g"] - 1)
        ang = inc_b * sd * (-1)
        by = -2.0 - alt_b
        _poly(lz, [(ex - 0.34, by + 0.07 - ang * 0.34), (ex - 0.28, by - 0.05 * k - ang * 0.28), (ex + 0.30, by - 0.07 * k + ang * 0.30), (ex + 0.34, by + 0.03 + ang * 0.34),
                   (ex + 0.30, by + 0.05 * k + ang * 0.30), (ex - 0.28, by + 0.08 * k - ang * 0.28)], x, y, s, R["cejas"], flip, A)
    # arrugas
    if R.get("arrugas"):
        for yy, w_ in ((-2.32, 0.42), (-2.22, 0.34)):
            lz.trazo(_p(np.array([(-w_, yy), (0.0, yy - 0.04), (w_, yy)]), x, y, s, flip), P.oscurecer(sombra, 0.1), max(1.2, 0.012 * s), afinar=False, temblor=0.0) if False else None
        for sd in (-1, 1):
            _poly(lz, [(sd * 0.56, -1.30), (sd * 0.62, -1.05), (sd * 0.56, -0.86), (sd * 0.52, -1.05)], x, y, s, sombra, flip, A * 0.45)
    # --- boca
    mw = 0.34
    my = -0.82
    cur = curva_b * 0.10 + (0.04 * boca_a)
    if boca_a > 0.08:
        ap = 0.06 + 0.22 * min(boca_a, 1.0)
        _poly(lz, catmull(np.array([(-mw, my), (-mw * 0.5, my - 0.02 + cur * 0.3), (0, my - 0.03), (mw * 0.5, my - 0.02 + cur * 0.3), (mw, my), (mw * 0.5, my + ap + cur), (0, my + ap * 1.25), (-mw * 0.5, my + ap + cur)]), 4, True),
              x, y, s, (104, 30, 54), flip, A)
        if boca_a > 0.3:
            _poly(lz, catmull(np.array([(-mw * 0.6, my + ap * 0.7), (0, my + ap * 0.5), (mw * 0.6, my + ap * 0.7), (0, my + ap * 1.2)]), 4, True), x, y, s, (236, 110, 120), flip, A * 0.9)
        _poly(lz, [(-mw * 0.8, my - 0.005), (mw * 0.8, my - 0.005), (mw * 0.7, my + 0.07), (-mw * 0.7, my + 0.07)], x, y, s, (252, 250, 244), flip, A * 0.9) if boca_a > 0.4 else None
    else:
        _poly(lz, catmull(np.array([(-mw, my - cur), (-mw * 0.4, my + cur * 0.4), (0, my + cur * 0.5), (mw * 0.4, my + cur * 0.4), (mw, my - cur), (mw * 0.4, my + cur * 0.4 + 0.045), (0, my + cur * 0.5 + 0.06),
                                         (-mw * 0.4, my + cur * 0.4 + 0.045)]), 4, True), x, y, s, P.oscurecer(sombra, 0.4), flip, A)
    # --- barba / bigote / patillas
    _vello(lz, x, y, s, R, flip, A, fw)
    # --- peinado / sombrero
    _pelo_delante(lz, x, y, s, R, flip, A, fw, t)


def _torso(lz, x, y, s, R, flip, A):
    ropa, ropa2 = R["ropa"], R["ropa2"]
    sh = P.oscurecer(ropa, 0.28)
    forma = [(-0.55, -0.10), (-1.5, 0.08), (-2.5, 0.42), (-3.0, 1.2), (-3.1, 3.4), (3.1, 3.4), (3.0, 1.2), (2.5, 0.42), (1.5, 0.08), (0.55, -0.10)]
    _poly(lz, catmull(np.array(forma), 6, True), x, y, s, sh, flip, A)
    forma2 = [(-0.55, -0.10), (-1.5, 0.08), (-2.5, 0.42), (-3.0, 1.2), (-3.1, 3.4), (1.0, 3.4), (1.0, 0.6), (0.55, -0.10)]
    _poly(lz, catmull(np.array(forma2), 6, True), x, y, s, ropa, flip, A)
    _poly(lz, [(-2.3, 1.2), (-1.6, 0.6), (-1.5, 0.75), (-2.1, 1.35)], x, y, s, P.aclarar(ropa, 0.25), flip, A * 0.8)
    c = R["cuello"]
    if c == "alzacuello":
        _poly(lz, [(-0.46, 0.0), (0.46, 0.0), (0.44, 0.45), (-0.44, 0.45)], x, y, s, (255, 255, 255), flip, A)
        _poly(lz, [(-0.45, 0.2), (0.0, 0.5), (0.45, 0.2), (0.9, 1.2), (-0.9, 1.2)], x, y, s, P.oscurecer(ropa, 0.35), flip, A)
        for k in range(5):
            _ell(lz, 0.0, 0.95 + k * 0.45, 0.07, 0.07, x, y, s, P.aclarar(ropa, 0.35), flip, A)
    elif c == "camisa":
        _poly(lz, [(-0.55, 0.15), (0.0, 1.1), (0.55, 0.15), (0.95, 0.5), (0.0, 1.8), (-0.95, 0.5)], x, y, s, ropa2, flip, A)
        _poly(lz, [(-0.4, 0.2), (0.0, 0.9), (0.4, 0.2)], x, y, s, P.mezcla(PIEL[R["piel"]], SOMBRA_PIEL, 0.4), flip, A)
        _poly(lz, [(-2.9, 2.3), (2.9, 2.3), (2.9, 2.75), (-2.9, 2.75)], x, y, s, ropa2 if ropa2 != (246, 242, 232) else (204, 56, 56), flip, A * 0.0)
        if ropa2 == (204, 56, 56):
            pass
    elif c == "casaca":
        _poly(lz, [(-0.55, 0.0), (0.55, 0.0), (0.7, 0.7), (-0.7, 0.7)], x, y, s, ropa2, flip, A)
        _poly(lz, [(-0.45, 0.45), (0.0, 1.0), (0.45, 0.45), (1.3, 1.2), (0.0, 3.4), (-1.3, 1.2)], x, y, s, P.aclarar(ropa, 0.0) if False else (250, 246, 238), flip, A)
        for k in range(6):
            _ell(lz, 0.0, 1.2 + k * 0.36, 0.07, 0.07, x, y, s, (250, 206, 90), flip, A)
        for sd in (-1, 1):
            _poly(lz, [(sd * 1.55, 0.4), (sd * 2.55, 1.15), (sd * 2.35, 1.5), (sd * 1.4, 0.8)], x, y, s, (250, 206, 90), flip, A)
        _poly(lz, [(-2.5, 1.5), (-0.3, 3.4), (0.3, 3.4), (-2.1, 1.3)], x, y, s, (250, 248, 244), flip, A * 0.9)
        _poly(lz, [(2.5, 1.5), (0.3, 3.4), (-0.3, 3.4), (2.1, 1.3)], x, y, s, (250, 248, 244), flip, A * 0.9)
    elif c == "levita":
        _poly(lz, [(-0.45, 0.2), (0.0, 1.5), (0.45, 0.2), (0.7, 0.9), (0.0, 2.6), (-0.7, 0.9)], x, y, s, ropa2, flip, A)
        _poly(lz, [(-0.32, 0.35), (0.32, 0.35), (0.12, 1.3), (-0.12, 1.3)], x, y, s, (206, 60, 70), flip, A)
        for sd in (-1, 1):
            _poly(lz, [(sd * 0.45, 0.2), (sd * 1.4, 0.7), (sd * 0.5, 2.4), (sd * 0.0, 1.5)], x, y, s, P.aclarar(ropa, 0.1), flip, A)
    elif c == "vestido":
        _poly(lz, catmull(np.array([(-1.5, 0.7), (0.0, 1.0), (1.5, 0.7), (1.9, 1.3), (0.0, 1.9), (-1.9, 1.3)]), 6, True), x, y, s, P.mezcla(PIEL[R["piel"]], SOMBRA_PIEL, 0.15), flip, A)
        _poly(lz, catmull(np.array([(-1.7, 1.0), (0.0, 1.5), (1.7, 1.0), (2.2, 1.7), (0.0, 2.3), (-2.2, 1.7)]), 6, True), x, y, s, ropa, flip, A * 0.0)
        _poly(lz, [(-2.4, 1.3), (-1.5, 0.9), (0.0, 1.25), (1.5, 0.9), (2.4, 1.3), (2.9, 3.4), (-2.9, 3.4)], x, y, s, ropa, flip, A)
        _poly(lz, [(-1.6, 0.9), (0.0, 1.3), (1.6, 0.9), (1.5, 1.15), (0.0, 1.6), (-1.5, 1.15)], x, y, s, ropa2, flip, A)
    elif c == "rebozo":
        _poly(lz, [(-0.55, 0.1), (0.0, 0.9), (0.55, 0.1), (2.2, 1.0), (2.9, 3.4), (-2.9, 3.4), (-2.2, 1.0)], x, y, s, ropa, flip, A)
        for k in range(5):
            _poly(lz, [(-2.8 + k * 0.1, 1.6 + k * 0.34), (2.8 - k * 0.1, 1.6 + k * 0.34), (2.8 - k * 0.1, 1.72 + k * 0.34), (-2.8 + k * 0.1, 1.72 + k * 0.34)], x, y, s, ropa2, flip, A * 0.9)


def _pelo_atras(lz, x, y, s, R, flip, A):
    pelo = R["pelo"]
    g = R.get("gorro")
    if g in ("peluca",):
        _poly(lz, catmull(np.array([(0.0, -3.1), (1.25, -2.7), (1.38, -1.4), (1.22, -0.7), (0.7, -0.45), (-0.7, -0.45), (-1.22, -0.7), (-1.38, -1.4), (-1.25, -2.7)]), 6, True), x, y, s, P.oscurecer(pelo, 0.12), flip, A)
    elif g == "peinado":
        _ell(lz, 0.0, -3.0, 0.62, 0.52, x, y, s, P.oscurecer(pelo, 0.2), flip, A)
        _poly(lz, catmull(np.array([(0.0, -2.9), (1.2, -2.5), (1.25, -1.2), (1.0, -0.5), (-1.0, -0.5), (-1.25, -1.2), (-1.2, -2.5)]), 6, True), x, y, s, P.oscurecer(pelo, 0.2), flip, A)
    elif g == "trenzas":
        for sd in (-1, 1):
            _poly(lz, catmull(np.array([(sd * 1.0, -2.0), (sd * 1.25, -1.2), (sd * 1.1, 0.2), (sd * 0.9, 0.9), (sd * 0.75, 0.2), (sd * 0.9, -1.2)]), 5, True), x, y, s, P.oscurecer(pelo, 0.1), flip, A)
    elif not R.get("calvo"):
        _poly(lz, catmull(np.array([(0.0, -3.0), (1.15, -2.65), (1.2, -1.7), (1.05, -1.4), (-1.05, -1.4), (-1.2, -1.7), (-1.15, -2.65)]), 6, True), x, y, s, P.oscurecer(pelo, 0.15), flip, A)


def _pelo_delante(lz, x, y, s, R, flip, A, fw, t):
    pelo = R["pelo"]
    g = R.get("gorro")
    luz_p = P.aclarar(pelo, 0.28) if sum(pelo) < 600 else P.oscurecer(pelo, 0.08)
    if R.get("calvo"):          # cura: calvicie con mechones blancos a los lados
        for sd in (-1, 1):
            _poly(lz, catmull(np.array([(sd * 0.96 * fw, -2.15), (sd * 1.10 * fw, -1.75), (sd * 1.04 * fw, -1.15), (sd * 0.92 * fw, -1.30), (sd * 0.88 * fw, -1.6), (sd * 0.84 * fw, -2.0)]), 4, True), x, y, s, pelo, flip, A)
        _poly(lz, catmull(np.array([(-0.9 * fw, -2.35), (-0.5, -2.6), (0.0, -2.66), (0.5, -2.6), (0.9 * fw, -2.35), (0.6, -2.5), (0.0, -2.56), (-0.6, -2.5)]), 4, True), x, y, s, pelo, flip, A * 0.9)
        _ell(lz, -0.30, -2.40, 0.34, 0.12, x, y, s, (255, 255, 255), flip, A * 0.25, rot=-0.2)
    elif g in ("pañuelo",):
        pano = R.get("pano", (250, 248, 244))
        _poly(lz, catmull(np.array([(-1.06 * fw, -1.9), (-1.0 * fw, -2.6), (-0.4, -3.05), (0.5, -3.05), (1.0 * fw, -2.6), (1.08 * fw, -1.9), (0.9 * fw, -2.1), (0.0, -2.35), (-0.9 * fw, -2.1)]), 6, True), x, y, s, pano, flip, A)
        _poly(lz, catmull(np.array([(-1.06 * fw, -1.9), (-1.0 * fw, -2.6), (-0.4, -3.05), (0.0, -3.0), (-0.3, -2.5), (-0.7, -2.1)]), 6, True), x, y, s, P.oscurecer(pano, 0.0) if False else (255, 255, 255), flip, A * 0.5)
        _poly(lz, [(0.85 * fw, -2.15), (1.55 * fw, -1.8), (1.4 * fw, -1.45), (1.7 * fw, -1.1), (1.25 * fw, -1.2), (1.05 * fw, -1.75)], x, y, s, pano, flip, A)
        _poly(lz, [(-1.0 * fw, -2.3), (1.0 * fw, -2.3), (1.0 * fw, -2.18), (-1.0 * fw, -2.18)], x, y, s, (204, 56, 56), flip, A * 0.0)
        _poly(lz, catmull(np.array([(-1.06 * fw, -1.9), (-0.7, -2.2), (0.0, -2.3), (0.7, -2.2), (1.06 * fw, -1.9), (1.04 * fw, -1.75), (0.0, -2.1), (-1.04 * fw, -1.75)]), 4, True), x, y, s, P.oscurecer(pelo, 0.0), flip, A * 0.0)
        for sd in (-1, 1):
            _poly(lz, catmull(np.array([(sd * 1.0 * fw, -1.9), (sd * 1.1 * fw, -1.4), (sd * 1.0 * fw, -1.0), (sd * 0.92 * fw, -1.3)]), 4, True), x, y, s, pelo, flip, A)
    elif g in ("bicornio", "bicornio_plumas", "bicornio_lado"):
        base = (36, 32, 52)
        if g == "bicornio_lado":
            _poly(lz, catmull(np.array([(-1.9, -2.5), (-1.2, -3.35), (0.4, -3.55), (1.9, -3.05), (2.2, -2.4), (1.0, -2.65), (-0.8, -2.55)]), 6, True), x, y, s, base, flip, A)
            _poly(lz, [(-1.9, -2.5), (-0.8, -2.55), (1.0, -2.65), (2.2, -2.4), (2.2, -2.3), (1.0, -2.55), (-0.8, -2.45), (-1.9, -2.4)], x, y, s, (250, 206, 90), flip, A)
        else:
            _poly(lz, catmull(np.array([(-1.5, -2.35), (-1.2, -3.2), (0.0, -3.5), (1.2, -3.2), (1.5, -2.35), (0.8, -2.65), (0.0, -2.75), (-0.8, -2.65)]), 6, True), x, y, s, base, flip, A)
            _poly(lz, [(-1.5, -2.35), (-0.8, -2.65), (0.0, -2.75), (0.8, -2.65), (1.5, -2.35), (1.5, -2.24), (0.8, -2.54), (0.0, -2.64), (-0.8, -2.54), (-1.5, -2.24)], x, y, s, (250, 206, 90), flip, A)
        _ell(lz, 1.2, -2.5, 0.12, 0.12, x, y, s, (206, 52, 60), flip, A)
        if g == "bicornio_plumas":
            for k in range(5):
                a = -1.2 + k * 0.4
                _poly(lz, catmull(np.array([(0.2, -3.4), (0.4 + 0.5 * math.sin(a), -3.9 - 0.3 * math.cos(a)), (0.1 + 0.8 * math.sin(a), -4.3 - 0.2 * k), (0.3, -3.5)]), 4, True), x, y, s, (255, 255, 255) if k % 2 == 0 else (236, 236, 244), flip, A)
        for sd in (-1, 1):
            _poly(lz, catmull(np.array([(sd * 0.98 * fw, -2.25), (sd * 1.1 * fw, -1.5), (sd * 1.0 * fw, -1.0), (sd * 0.9 * fw, -1.3)]), 4, True), x, y, s, pelo, flip, A)
    elif g == "peluca":
        for k, yy in enumerate((-2.55, -2.0, -1.45, -0.95)):
            for sd in (-1, 1):
                _ell(lz, sd * 1.12 * fw, yy, 0.24, 0.20, x, y, s, (250, 248, 252), flip, A)
        _poly(lz, catmull(np.array([(0.0, -3.1), (1.0 * fw, -2.8), (1.06 * fw, -2.3), (0.0, -2.35), (-1.06 * fw, -2.3), (-1.0 * fw, -2.8)]), 6, True), x, y, s, (250, 248, 252), flip, A)
        _poly(lz, [(-0.9 * fw, -2.35), (0.9 * fw, -2.35), (0.8 * fw, -2.28), (-0.8 * fw, -2.28)], x, y, s, (216, 212, 224), flip, A * 0.9)
    elif g == "peinado":
        _poly(lz, catmull(np.array([(0.0, -2.9), (0.95 * fw, -2.6), (1.02 * fw, -1.9), (0.7, -2.1), (0.0, -2.35), (-0.7, -2.1), (-1.02 * fw, -1.9), (-0.95 * fw, -2.6)]), 6, True), x, y, s, pelo, flip, A)
        _poly(lz, catmull(np.array([(-0.1, -2.95), (0.5, -2.85), (0.2, -2.45), (-0.3, -2.4)]), 4, True), x, y, s, luz_p, flip, A * 0.5)
        _poly(lz, [(0.3, -3.5), (0.7, -3.1), (0.55, -3.0), (0.2, -3.3)], x, y, s, (250, 206, 90), flip, A)
        for k in range(3):
            _ell(lz, 0.3 + k * 0.12, -3.5 - k * 0.1, 0.07, 0.07, x, y, s, (250, 206, 90), flip, A)
    elif g == "palma":
        _poly(lz, catmull(np.array([(-1.1 * fw, -2.0), (-0.95, -2.7), (0.0, -2.85), (0.95, -2.7), (1.1 * fw, -2.0), (0.0, -2.3)]), 6, True), x, y, s, (240, 202, 124), flip, A)
        _poly(lz, catmull(np.array([(-2.4, -2.35), (-1.6, -2.55), (0.0, -2.6), (1.6, -2.55), (2.4, -2.35), (1.6, -2.1), (0.0, -2.2), (-1.6, -2.1)]), 6, True), x, y, s, (232, 188, 108), flip, A)
        _poly(lz, [(-1.0, -2.45), (1.0, -2.45), (1.0, -2.3), (-1.0, -2.3)], x, y, s, (204, 60, 60), flip, A)
        _poly(lz, catmull(np.array([(-0.9, -2.7), (0.0, -2.9), (0.8, -2.7), (0.0, -2.6)]), 4, True), x, y, s, (252, 226, 160), flip, A * 0.6)
        for sd in (-1, 1):
            _poly(lz, catmull(np.array([(sd * 0.98 * fw, -2.1), (sd * 1.08 * fw, -1.5), (sd * 1.0 * fw, -1.0), (sd * 0.9 * fw, -1.35)]), 4, True), x, y, s, pelo, flip, A)
    elif g == "corona":
        _poly(lz, [(-0.85, -2.7), (-0.9, -3.4), (-0.45, -3.0), (0.0, -3.55), (0.45, -3.0), (0.9, -3.4), (0.85, -2.7)], x, y, s, (250, 208, 80), flip, A)
        _poly(lz, [(-0.85, -2.7), (0.85, -2.7), (0.85, -2.55), (-0.85, -2.55)], x, y, s, (226, 160, 40), flip, A)
        _poly(lz, catmull(np.array([(-1.0 * fw, -1.9), (-0.95, -2.6), (0.0, -2.7), (0.95, -2.6), (1.0 * fw, -1.9), (0.0, -2.3)]), 6, True), x, y, s, pelo, flip, A)
    elif g == "trenzas":
        _poly(lz, catmull(np.array([(-1.04 * fw, -1.9), (-0.95, -2.7), (0.0, -2.85), (0.95, -2.7), (1.04 * fw, -1.9), (0.5, -2.45), (0.0, -2.2), (-0.5, -2.45)]), 6, True), x, y, s, pelo, flip, A)
        _poly(lz, [(-0.06, -2.85), (0.06, -2.85), (0.05, -2.2), (-0.05, -2.2)], x, y, s, P.aclarar(pelo, 0.3), flip, A * 0.8)
    else:
        _poly(lz, catmull(np.array([(-1.04 * fw, -1.8), (-1.02 * fw, -2.6), (-0.4, -2.95), (0.5, -2.95), (1.04 * fw, -2.5), (1.06 * fw, -1.8), (0.9 * fw, -2.05), (0.2, -2.35), (-0.6, -2.3), (-0.9 * fw, -2.05)]), 6, True), x, y, s, pelo, flip, A)
        _poly(lz, catmull(np.array([(-0.6, -2.8), (0.2, -2.9), (0.6, -2.7), (0.0, -2.55), (-0.5, -2.6)]), 4, True), x, y, s, luz_p, flip, A * 0.6)


def _vello(lz, x, y, s, R, flip, A, fw):
    pelo = R["pelo"]
    b = R.get("bigote")
    col = (236, 234, 240) if b == "grueso_blanco" else P.oscurecer(pelo, 0.05)
    if b in ("fino", "grueso", "grueso_blanco"):
        g = 1.0 if b != "fino" else 0.55
        _poly(lz, catmull(np.array([(0.0, -1.10), (0.30, -1.07 - 0.02 * g), (0.52, -0.98), (0.44, -0.90 - 0.05 * g), (0.18, -0.96), (0.0, -0.94), (-0.18, -0.96), (-0.44, -0.90 - 0.05 * g), (-0.52, -0.98), (-0.30, -1.07 - 0.02 * g)]), 4, True),
              x, y, s, col, flip, A)
        if b != "fino":
            _poly(lz, catmull(np.array([(0.0, -1.10), (0.30, -1.07), (0.52, -0.98), (0.40, -0.80), (0.0, -0.90), (-0.40, -0.80), (-0.52, -0.98), (-0.30, -1.07)]), 4, True), x, y, s, col, flip, A)
    p = R.get("patillas")
    if p:
        L = 0.78 if p == "largas" else 0.45
        for sd in (-1, 1):
            _poly(lz, catmull(np.array([(sd * 0.96 * fw, -2.0), (sd * 1.0 * fw, -1.5), (sd * 0.90 * fw, -1.5 + L), (sd * 0.72 * fw, -1.5 + L * 0.9), (sd * 0.78 * fw, -1.5)]), 4, True), x, y, s, P.oscurecer(pelo, 0.1), flip, A)
