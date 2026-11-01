# -*- coding: utf-8 -*-
"""Figuras y utilería PROPIAS de «Tres noches» (tramo 4, 14-oct-2026), dibujadas con el pintor del kit «grabado de peste»
(nucleo/grabado.py). No van al kit: son de este video (regla «no reciclar escenas»).
Todas reciben (x, y) = punto del SUELO en pantalla y `s` = escala de pantalla (tamaño del mundo * cam.k(zc)).
  persona   gente de Azeroth de 3/4 (capa, guerrero, enano, médico de la peste, sanador, cazador, mercader); anda, corre, cae
  lobo      la mascota del cazador, de perfil
  hakkar    el Dios de la Sangre: serpiente alada enroscada · cara_hakkar (de frente: el susto)
  palmera, helecho, hoja_grande, liana, estatua_serpiente, pino     selva de Zul'Gurub y bosque de Dun Morogh
  jaula, reloj_arena, barricada, puesto, farol, icono_*             utilería"""
import math

import numpy as np

import grabado as GR
from grabado import ESPECTRO, ORO, PLAGA, SANGRE, TINTA, catmull, circ_pts, lerp, rnd, tr


# ------------------------------------------------------------------ utilidades
def tubo(espina, w0, w1=None, n=6):
    """Contorno de un tubo (cuerpo de serpiente, liana gruesa) alrededor de una espina, de ancho w0 a w1."""
    P = catmull(np.float32(espina), n)
    d = np.gradient(P, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-6
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    w = np.linspace(w0, w0 if w1 is None else w1, len(P))[:, None] / 2
    return np.vstack([P + nrm * w, (P - nrm * w)[::-1]]).astype(np.float32), P, nrm


# ------------------------------------------------------------------ sprites cacheados (rendimiento, 16-oct-2026)
# Multitud y vegetación se ESTAMPAN desde pocas variantes (GR.sprite): la pose se cuantiza a POSES por ciclo y el contorno
# hierve «en tres». Lo grande (primer plano), lo que cae o lleva aura se sigue dibujando en vivo.
POSES = 8                        # poses por ciclo de paso / de vaivén
SPRITE_ALTO = 640                # px: figuras más altas en pantalla se dibujan en vivo


def _r(v, q=0.02):
    return None if v is None else round(float(v) / q) * q


def persona(g, x, y, s, t, tipo="capa", fase=0.0, anda=1.0, dirx=1, tono=0.28, op=1.0, brazos=None, cae=0.0, aura=0.0,
            sem=0, arma=True, color_aura=None):
    if op <= 0.004 or s <= 0.004:
        return
    if not GR.CACHE or cae > 0.001 or 400 * s * g.s > SPRITE_ALTO:
        return _persona(g, x, y, s, t, tipo, fase, anda, dirx, tono, op, brazos, cae, aura, sem, arma, color_aura)
    vel = 0.95 if anda <= 1.2 else 1.75
    if aura > 0.01:                                        # el halo de contagio va EN VIVO (cae fuera de la silueta)
        a = t * 6.2832 * vel + fase
        k_and = min(anda, 1.4)
        ang = dirx * 0.12 * max(0.0, anda - 1.0)
        cx, cy = tr([(0, -190 * (0.74 if tipo == "enano" else 1.0))], x, y - abs(math.cos(a)) * 7 * k_and * s, s, ang, dirx)[0]
        g.acento_luz(cx, cy, 260 * s * (1 + 0.08 * math.sin(t * 5 + sem)), color_aura or SANGRE, 0.75 * aura * op)
        aura = round(aura, 1)
    if anda <= 1e-3:                                       # quieto: la pose no depende de t
        i, tq = 0, 0.0
    else:                                                  # el bajo de la capa usa a/2: ciclo de DOS pasos
        i, h = GR.fase_cuant((t * 6.2832 * vel + fase) * 0.5, 2 * POSES)
        tq = (2 * h - fase) / (6.2832 * vel)
    br = None if brazos is None else (_r(brazos[0]), _r(brazos[1]))
    col = None if color_aura is None else tuple(round(v, 2) for v in color_aura)
    clave = ("persona", tipo, _r(anda, 0.05), dirx, _r(tono), _r(op, 0.05), br, sem if anda > 1e-3 or aura else 0, arma, i,
             aura, col)
    GR.sprite(g, clave, x, y, s, lambda c, ax, ay, s_: _persona(c, ax, ay, s_, tq, tipo, fase, anda, dirx, tono, op, br,
                                                                0.0, aura, sem, arma, col), (-270, -620, 270, 60))


def _vaiven(t, w, sem):
    """Fase del vaivén sin(t*w + sem) cuantizada -> (índice, t equivalente con sem=0)."""
    i, h = GR.fase_cuant(t * w + sem, 2 * POSES)
    return i, h / w


def palmera(g, x, y, s, t, sem=0, alto=1.0, inclin=0.0, op=1.0):
    if s <= 0.004:
        return
    if not GR.CACHE or 1000 * alto * s * g.s > SPRITE_ALTO * 1.6:
        return _palmera(g, x, y, s, t, sem, alto, inclin, op)
    i, _ = GR.fase_cuant(t * 0.9, 2 * POSES)
    tq = i * 6.2832 / (2 * POSES) / 0.9
    GR.sprite(g, ("palmera", sem, _r(alto), _r(inclin), _r(op, 0.05), i), x, y, s,
              lambda c, ax, ay, s_: _palmera(c, ax, ay, s_, tq, sem, alto, inclin, op), (-560, -700 * alto - 420, 560, 40))


def helecho(g, x, y, s, t, sem=0, op=1.0, n=7):
    if s <= 0.004:
        return
    if not GR.CACHE:
        return _helecho(g, x, y, s, t, sem, op, n)
    i, _ = GR.fase_cuant(t * 1.1, 2 * POSES)
    tq = i * 6.2832 / (2 * POSES) / 1.1
    GR.sprite(g, ("helecho", sem, _r(op, 0.05), n, i), x, y, s,
              lambda c, ax, ay, s_: _helecho(c, ax, ay, s_, tq, sem, op, n), (-240, -240, 240, 160))


def pino(g, x, y, s, t, sem=0, op=1.0, nieve=True, tono=0.55):
    if s <= 0.004:
        return
    if not GR.CACHE or 650 * s * g.s > SPRITE_ALTO * 1.6:
        return _pino(g, x, y, s, t, sem, op, nieve, tono)
    i, tq = _vaiven(t, 0.9, sem)                           # el vaivén solo desfasa por sem: todos los pinos comparten
    GR.sprite(g, ("pino", nieve, _r(tono), _r(op, 0.05), i), x, y, s,
              lambda c, ax, ay, s_: _pino(c, ax, ay, s_, tq, 0, op, nieve, tono), (-220, -680, 220, 30))


# ------------------------------------------------------------------ gente
def _persona(g, x, y, s, t, tipo="capa", fase=0.0, anda=1.0, dirx=1, tono=0.28, op=1.0, brazos=None, cae=0.0, aura=0.0,
            sem=0, arma=True, color_aura=None):
    """Figura humana grabada de 3/4, ~380 de alto con s=1 (el enano ~280). `anda` 0 quieto · 1 camina · 2 corre;
    `brazos` = (atrás, delante) en radianes (0 = colgando, pi/2 = al frente, pi = arriba); `cae` 0..1 = se desploma hacia
    atrás; `aura` 0..1 = contagiado (plancha de sangre alrededor)."""
    if op <= 0.004 or s <= 0.004:
        return
    vel = 0.95 if anda <= 1.2 else 1.75
    a = t * 6.2832 * vel + fase
    k_and = min(anda, 1.4)
    sw = math.sin(a) * k_and
    bob = abs(math.cos(a)) * 7 * k_and
    lean = 0.12 * max(0.0, anda - 1.0)
    ang = dirx * lean - dirx * 1.4 * GR.smooth(cae)
    enano = tipo == "enano"
    hs = 0.74 if enano else 1.0                      # alto relativo
    ws = 1.22 if enano else 1.0                      # ancho relativo
    dy = -bob * (1 - cae) + 40 * cae

    def T(p):
        p = np.float32(p) * np.float32((ws, hs))
        return tr(p, x, y + dy * s, s, ang, dirx)

    if aura > 0.01:
        cx, cy = T([(0, -190)])[0]
        g.acento_luz(cx, cy, 260 * s * (1 + 0.08 * math.sin(t * 5 + sem)), color_aura or SANGRE, 0.75 * aura * op)
    # sombra en el suelo (asienta los pies)
    g.trama(tr(circ_pts(0, 0, 70 * ws, 22, 14), x, y, s), 0.75, ang=6, per=4.2, cruz=False, op=0.8 * op * (1 - 0.5 * cae))
    # botas: la de atrás y la de delante alternan con el paso
    for j, sg in enumerate((-1, 1)):
        bx = 26 * sw * sg
        lift = max(0.0, math.sin(a + (0 if sg > 0 else math.pi))) * 16 * k_and
        bota = [(bx - 16, -4 - lift), (bx + 26, -4 - lift), (bx + 28, 6 - lift), (bx - 18, 6 - lift), (bx - 14, -40 - lift),
                (bx + 8, -40 - lift)]
        g.figura(T([bota[4], bota[5], bota[1], bota[2], bota[3], bota[0]]), 0.55, contorno=2.0, op=op, ang=0, per=4.0,
                 cruz=False)
    br = brazos or (0.22 * sw, -0.22 * sw)
    oscuro_traje = {"medico": 0.72, "guerrero": 0.42, "cazador": 0.4, "mercader": 0.22, "sanador": 0.06}.get(tipo, tono)

    def brazo(angulo, delante):
        sx0 = 30 if delante else -26
        hx, hy = sx0, -262
        L = 120
        ex, ey = hx + L * math.sin(angulo) * 0.9, hy + L * math.cos(angulo)
        anchos = 19 if tipo in ("medico", "sanador", "capa") else 16
        manga = tubo([(hx, hy), ((hx + ex) / 2 + 4, (hy + ey) / 2), (ex, ey)], anchos, anchos * 1.25)[0]
        g.figura(T(manga), min(1.0, oscuro_traje + (0.2 if delante else 0.35)), contorno=2.0, op=op, ang=60, per=4.4,
                 cruz=False, tono2=min(1.0, oscuro_traje + 0.5), luz=0)
        g.figura(T(circ_pts(ex, ey + 8, 11, 12)), 0.05, contorno=1.6, op=op, ang=0, per=4, cruz=False)
        return ex, ey + 8

    mano_atras = brazo(br[0], False)
    # cuerpo: capa / sayo con pliegues; el bajo ondea al andar
    o = [5 * math.sin(a * 0.5 + i + sem) * k_and for i in range(5)]
    hem_y = -36
    cuerpo = [(-46, -292), (44, -292), (62, -238), (70 + 6 * sw, -150), (84 + 10 * sw, hem_y + o[0]),
              (40, hem_y + 8 + o[1]), (0, hem_y + o[2]), (-40, hem_y + 8 + o[3]), (-80 - 8 * sw, hem_y + o[4]),
              (-70 - 4 * sw, -150), (-62, -238)]
    pol = T(catmull(np.float32(cuerpo), 4, cerrado=True))
    g.figura(pol, oscuro_traje, contorno=2.4, op=op, tono2=min(1.0, oscuro_traje + 0.45), luz=0, ang=84, per=4.6,
             borde=0.28, rb=16)
    for i, xx in enumerate((-30, 6, 38)):                       # pliegues
        g.trazo(T(catmull(np.float32([(xx * 0.6, -270), (xx * 0.85 + 4 * sw, -160), (xx * 1.25 + 8 * sw, hem_y + 6)]), 5)),
                1.4, op=0.8 * op, sem=sem * 7 + i)
    if tipo == "mercader":                                      # mandil
        g.figura(T([(-24, -220), (30, -220), (34, -90), (-28, -90)]), 0.3, contorno=1.8, op=op, ang=0, per=4.0, cruz=False)
    if tipo == "guerrero":                                      # cinturón y cota
        g.trazo(T([(-60, -170), (64, -170)]), 7, op=op, afilado=0.0)
        g.trama(T([(-58, -290), (60, -290), (66, -175), (-62, -175)]), 0.35, ang=0, per=3.6, modo="lineal", op=op * 0.6)
    # cabeza
    hx, hy = 8, -322
    if tipo == "medico":
        g.figura(T(catmull(np.float32([(-30, -300), (26, -300), (34, -330), (20, -350), (-22, -350), (-34, -328)]), 4, True)),
                 0.7, contorno=2.0, op=op, ang=80, per=4.2)
        pico = [(22, -338), (96, -322), (128, -300), (96, -306), (24, -314)]
        g.figura(T(catmull(np.float32(pico), 4)), 0.3, contorno=2.2, op=op, tono2=0.75, luz=-90, ang=10, per=4.0)
        g.figura(T(circ_pts(18, -334, 9, 12)), 0.0, contorno=1.6, op=op)            # lente del ojo
        g.circ(*T([(19, -334)])[0], 3.2 * s, TINTA, op)
        g.figura(T([(-70, -352), (80, -352), (64, -362), (-60, -362)]), 0.85, contorno=2.0, op=op, ang=0, per=4)  # ala
        g.figura(T([(-36, -360), (38, -360), (32, -420), (-30, -420)]), 0.82, contorno=2.0, op=op, ang=90, per=4.2)
        g.trazo(T([(-30, -372), (32, -372)]), 6, color=g.fondo_papel, op=0.7 * op, afilado=0.0)
    elif tipo == "guerrero":
        cara = circ_pts(hx, hy + 4, 27, 24)
        g.figura(T(cara), 0.12, contorno=2.0, op=op, tono2=0.6, luz=0, ang=0, per=3.8, cruz=False)
        yelmo = [(-30, -322), (-28, -350), (-10, -366), (16, -368), (38, -352), (42, -326), (34, -318), (36, -334),
                 (10, -340), (-18, -334), (-22, -316)]
        g.figura(T(catmull(np.float32(yelmo), 4, True)), 0.45, contorno=2.4, op=op, tono2=0.9, luz=0, ang=20, per=3.8)
        g.trazo(T([(14, -340), (16, -304)]), 6, op=op, afilado=0.0)                  # nasal
        g.trazo(T([(4, -366), (2, -400), (-14, -414)]), 5, op=op, afilado=0.9)      # penacho
    elif tipo == "enano":
        cara = circ_pts(hx, hy + 6, 28, 24)
        g.figura(T(cara), 0.1, contorno=2.0, op=op, tono2=0.55, luz=0, ang=0, per=3.8, cruz=False)
        barba = [(-24, -312), (40, -312), (46, -270), (22, -210), (8, -190), (-6, -214), (-28, -262)]
        g.figura(T(catmull(np.float32(barba), 4, True)), 0.25, contorno=2.2, op=op, ang=88, per=3.4, cruz=False, tono2=0.6,
                 luz=0)
        yelmo = [(-30, -326), (-26, -354), (8, -366), (40, -352), (44, -326)]
        g.figura(T(catmull(np.float32(yelmo + [(8, -334)]), 4, True)), 0.4, contorno=2.4, op=op, tono2=0.85, luz=0, ang=20,
                 per=3.8)
        for sg in (-1, 1):                                     # cuernos
            cx0 = 8 + sg * 34
            g.figura(T(catmull(np.float32([(cx0, -350), (cx0 + sg * 34, -372), (cx0 + sg * 42, -404), (cx0 + sg * 30, -378),
                                            (cx0 - sg * 2, -362)]), 4, True)), 0.05, contorno=1.8, op=op)
        for i in range(3):
            g.trazo(T([(4 + i * 10, -300), (6 + i * 10 + 3 * sw, -232)]), 1.2, op=0.8 * op)
        g.circ(*T([(22, -330)])[0], 3.0 * s, TINTA, op)
    else:                                                       # capucha (capa, sanador, cazador, mercader)
        cap = [(-36, -300), (-38, -340), (-22, -372), (6, -384), (30, -370), (44, -340), (44, -306), (24, -296)]
        tcap = 0.06 if tipo == "sanador" else min(1.0, oscuro_traje + 0.1)
        g.figura(T(catmull(np.float32(cap), 4, True)), tcap, contorno=2.4, op=op, tono2=min(1.0, tcap + 0.4), luz=0,
                 ang=70, per=4.4, modo="contorno", borde=0.3, rb=10)
        hueco = [(10, -350), (34, -344), (40, -318), (26, -302), (10, -310)]
        g.macizo(T(catmull(np.float32(hueco), 4, True)), op)
        if tipo == "mercader":
            g.figura(T([(-30, -360), (40, -366), (46, -384), (-24, -392)]), 0.2, contorno=1.8, op=op, ang=0, per=4)
    # brazo de delante y lo que lleva
    mano = brazo(br[1], True)
    if arma and tipo in ("guerrero",):
        g.figura(T(circ_pts(46, -190, 56, 28)), 0.25, contorno=2.6, op=op, tono2=0.75, luz=0, ang=0, per=4.2,
                 modo="anillos", centro=tuple(T([(46, -190)])[0]), cruz=False)
        g.circ(*T([(46, -190)])[0], 9 * s, TINTA, op)
        g.trazo(T([(mano_atras[0], mano_atras[1] + 60), (mano_atras[0] + 10, mano_atras[1] - 300)]), 5, op=op, afilado=0.0)
        g.figura(T([(mano_atras[0] + 2, mano_atras[1] - 300), (mano_atras[0] + 22, mano_atras[1] - 302),
                    (mano_atras[0] + 13, mano_atras[1] - 350)]), 0.1, contorno=1.6, op=op)
    elif arma and tipo == "sanador":
        top = (mano[0] + 14, mano[1] - 220)
        g.trazo(T([(mano[0] + 4, mano[1] + 80), top]), 6, op=op, afilado=0.0)
        g.figura(T(circ_pts(top[0], top[1] - 14, 16, 16)), 0.0, contorno=2.0, op=op)
        cx, cy = T([(top[0], top[1] - 14)])[0]
        g.acento_luz(cx, cy, 90 * s, ORO, 0.7 * op)
    elif arma and tipo == "medico":
        g.trazo(T([(mano[0] + 4, mano[1] - 30), (mano[0] + 30, mano[1] + 150)]), 5, op=op, afilado=0.0)
    elif arma and tipo == "cazador":
        arco = [(-40, -330), (-70, -250), (-74, -170), (-52, -90)]
        g.trazo(T(catmull(np.float32(arco), 5)), 5, op=op, afilado=0.5)
        g.trazo(T([arco[0], arco[-1]]), 1.0, op=op, afilado=0.0)
    if aura > 0.01:
        g.acento(pol, color_aura or SANGRE, 0.55 * aura * op, sem=sem)


def lobo(g, x, y, s, t, fase=0.0, anda=0.0, dirx=1, op=1.0, ojo=0.0, aura=0.0, grune=0.0):
    """Lobo (mascota del cazador) de perfil, ~330 de largo y ~190 de alto con s=1. (x, y) = suelo bajo el centro."""
    if op <= 0.004 or s <= 0.004:
        return
    a = t * 6.2832 * (1.1 if anda else 0.25) + fase
    resp = 2.5 * math.sin(t * 2.2 + fase)

    def T(p):
        return tr(np.float32(p), x, y, s, 0.0, dirx)
    g.trama(tr(circ_pts(0, 0, 150, 22, 18), x, y, s), 0.75, ang=6, per=4.2, cruz=False, op=0.8 * op)
    if aura > 0.01:
        cx, cy = T([(0, -110)])[0]
        g.acento_luz(cx, cy, 260 * s, SANGRE, 0.8 * aura * op)
    pat = []
    for i, (px, fz) in enumerate(((-100, 0.0), (-70, math.pi), (70, 0.5), (100, math.pi + 0.5))):
        sw = math.sin(a + fz) * (22 if anda else 2)
        pat.append([(px - 10, -90), (px + 10, -90), (px + 8 + sw * 0.5, -44), (px + 12 + sw, -6), (px + 24 + sw, 0),
                    (px - 6 + sw, 0), (px - 4 + sw * 0.5, -44)])
    for i in (1, 3):
        g.figura(T(pat[i]), 0.55, contorno=2.0, op=op, ang=80, per=4.0, cruz=False)
    cola_sw = 14 * math.sin(t * 2.6 + fase)
    cola = [(-130, -118), (-180, -112 + cola_sw), (-222, -84 + cola_sw), (-214, -70 + cola_sw), (-176, -88 + cola_sw * 0.6),
            (-130, -98)]
    g.figura(T(catmull(np.float32(cola), 4, True)), 0.3, contorno=2.0, op=op, ang=20, per=4.2, tono2=0.7, luz=-90)
    cuerpo = [(-136, -128), (-90, -146 + resp), (0, -140 + resp), (80, -150), (118, -158), (126, -120), (110, -80),
              (60, -76), (0, -84), (-80, -78), (-130, -92)]
    pol = T(catmull(np.float32(cuerpo), 5, True))
    g.figura(pol, 0.18, contorno=2.4, op=op, tono2=0.62, luz=-90, ang=24, per=4.2, borde=0.25, rb=14)
    for i in range(7):                                          # pelaje: mechones de buril
        xx = -110 + i * 34
        g.trazo(T([(xx, -138 + resp), (xx + 14, -126), (xx + 10, -112)]), 1.3, op=0.8 * op, sem=i)
    for i in (0, 2):
        g.figura(T(pat[i]), 0.3, contorno=2.0, op=op, ang=80, per=4.0, cruz=False)
    # cabeza: hocico, orejas, ojo
    hb = 6 * math.sin(t * 1.3 + fase) if not anda else 4 * math.sin(a * 2)
    cab = [(106, -150 + hb), (128, -196 + hb), (142, -206 + hb), (150, -186 + hb), (168, -182 + hb), (214, -158 + hb),
           (224, -146 + hb), (216, -136 + hb), (176, -130 + hb + 10 * grune), (150, -118 + hb), (120, -112)]
    g.figura(T(catmull(np.float32(cab), 4, True)), 0.12, contorno=2.4, op=op, tono2=0.55, luz=-60, ang=10, per=4.0)
    g.figura(T([(130, -192 + hb), (136, -236 + hb), (152, -196 + hb)]), 0.5, contorno=1.8, op=op, ang=80, per=4)
    g.circ(*T([(222, -150 + hb)])[0], 5 * s, TINTA, op)
    if grune > 0.05:
        for i in range(3):
            g.trazo(T([(184 + i * 10, -136 + hb), (186 + i * 10, -124 + hb + 6 * grune)]), 2.2, color=g.fondo_papel, op=op)
    ex, ey = T([(170, -172 + hb)])[0]
    g.circ(ex, ey, 6.5 * s, TINTA, op)
    g.circ(ex, ey, 3.2 * s, g.fondo_papel, op)
    if ojo > 0.01:
        g.acento_luz(ex, ey, 40 * s, SANGRE, ojo * op, 1.2)
        g.circ(ex, ey, 3.2 * s, SANGRE, ojo * op)
    if aura > 0.01:
        g.acento(pol, SANGRE, 0.5 * aura * op, sem=5)


# ------------------------------------------------------------------ Hakkar
def _escamas(g, P, nrm, w, op, paso=3, t=0.0):
    """Medias lunas de buril a lo largo del cuerpo (escamas)."""
    for i in range(2, len(P) - 2, paso):
        for v in (-0.25, 0.15):
            c = P[i] + nrm[i] * w[i] * v
            d = P[min(i + 1, len(P) - 1)] - P[i]
            an = math.atan2(d[1], d[0])
            r = w[i] * 0.16
            arco = [(c[0] + r * math.cos(an + u), c[1] + r * math.sin(an + u)) for u in np.linspace(-1.3, 1.3, 6)]
            g.trazo(np.float32(arco), max(1.0, r * 0.18), op=0.85 * op, afilado=0.8)


def hakkar(g, x, y, s, t, op=1.0, ojos=1.0, boca=0.0, alas=1.0, luz=0.0):
    """El Dios de la Sangre: serpiente alada ENROSCADA sobre su altar, cuello en S, alas de plumas, cresta. ~1000 de alto
    con s=1; (x, y) = centro del enroscado en el suelo. `ojos` 0..1 brillo rojo, `boca` 0..1, `luz` aclara (relámpago)."""
    if op <= 0.004:
        return
    ond = math.sin(t * 0.8)
    with g.grupo(x, y, s):
        # alas detrás del cuello
        for lado in (-1, 1):
            GR.ala(g, lado * 70, -560 + 10 * ond, 2.0, t + lado * 0.4, lado=lado, apertura=alas, tono=0.18 - 0.1 * luz, op=op)
        # enroscado: espiral de cuerpo que sube; vueltas de abajo arriba, primero las mitades de atrás y luego las de
        # delante (cada vuelta se apoya en la de abajo y la tapa)
        vueltas = [(430, 150, 0.0, 170), (340, 115, -95, 150), (250, 85, -175, 130)]
        arcos = []
        for i, (rx, ry, yc, w) in enumerate(vueltas):
            for mitad, (u0, u1) in enumerate(((math.pi, 2 * math.pi), (0.0, math.pi))):
                us = np.linspace(u0, u1, 9)
                rr = np.linspace(1.0, 0.92, 9) if mitad else np.linspace(1.02, 1.0, 9)
                esp = [(rx * r_ * math.cos(u) + 20 * math.sin(t * 0.6 + i), yc + ry * r_ * math.sin(u) - 30 * (u / 6.2832))
                       for u, r_ in zip(us, rr)]
                arcos.append((mitad, i, esp, w))
        for mitad, i, esp, w in sorted(arcos, key=lambda a: (a[0], a[1])):
            pol, P, nrm = tubo(esp, w, w * 0.94, 4)
            tn = (0.45 if mitad == 0 else 0.14) - 0.1 * luz
            g.figura(pol, tn, contorno=2.8, op=op, tono2=0.85, luz=-90, ang=95, per=4.6, borde=0.4, rb=40)
            if mitad:
                _escamas(g, P, nrm, np.full(len(P), w), op, paso=3)
                g.trazo(P + nrm * w * 0.3, 1.8, op=0.7 * op)
            g.acento(pol, SANGRE, 0.35 * op, sem=i + 2 + 3 * mitad)
        # cuello en S que sube a la cabeza
        cuello = [(40, -100), (150, -260), (60 + 30 * ond, -420), (-40 + 20 * ond, -560), (0 + 15 * ond, -700)]
        pol, P, nrm = tubo(cuello, 150, 100, 6)
        g.figura(pol, 0.12 - 0.08 * luz, contorno=2.8, op=op, tono2=0.75, luz=0, ang=10, per=4.6, borde=0.4, rb=36)
        _escamas(g, P, nrm, np.linspace(150, 100, len(P)), op, paso=3)
        vientre = (P + nrm * np.linspace(150, 100, len(P))[:, None] * 0.32)
        g.trazo(vientre, 2.0, op=0.8 * op)
        g.acento(pol, SANGRE, 0.3 * op, sem=9)
        hx, hy = 15 * ond, -760
        cara_hakkar(g, hx, hy - 40, 0.85, t, op=op, ojos=ojos, boca=boca, gloria=False)


def cara_hakkar(g, x, y, s, t, op=1.0, ojos=1.0, boca=0.0, gloria=True, color=1.0):
    """La cabeza de Hakkar DE FRENTE: cráneo de víbora anguloso (ancho en la bisagra, hocico estrecho), ceño, ojos rasgados de
    rendija que arden, fosetas, escamas en placas, boca abierta con filas de dientes y dos colmillos, cresta de plumas. ~420 de
    ancho con s=1; (x, y) = centro de la cara. Es también el SUSTO (llena el cuadro)."""
    with g.grupo(x, y, s):
        if gloria:
            g.acento_luz(0, 0, 700, SANGRE, 0.6 * color * op, 1.0)
        for i in range(15):                                    # cresta: plumas largas y afiladas en abanico
            u = i / 14
            an = math.radians(lerp(-170, -10, u)) + 0.05 * math.sin(t * 2.2 + i)
            L = 320 + 110 * math.sin(u * math.pi)
            GR._pluma(g, (60 * math.cos(an), -60 + 50 * math.sin(an)), an, L, 34, 0.35 + 0.3 * (i % 2), op, g.k)
        bj = 130 * boca
        mand = [(-150, 40), (150, 40), (126, 120 + bj), (64, 196 + bj), (0, 214 + bj), (-64, 196 + bj), (-126, 120 + bj)]
        g.figura(catmull(np.float32(mand), 4, True), 0.35, contorno=3.0, op=op, tono2=0.85, luz=90, ang=0, per=4.0, borde=0.4,
                 rb=24)
        if boca > 0.05:
            interior = [(-130, 44), (130, 44), (104, 104 + bj * 0.9), (40, 160 + bj * 0.9), (0, 170 + bj * 0.9),
                        (-40, 160 + bj * 0.9), (-104, 104 + bj * 0.9)]
            ip = catmull(np.float32(interior), 4, True)
            g.macizo(ip, op)
            g.acento(ip, SANGRE, 0.95 * op * color, aspero=0.4)
            g.acento_luz(0, 110 + bj * 0.5, 160, SANGRE, 0.8 * op * color)
            for sg in (-1, 1):                                 # lengua bífida
                g.trazo([(0, 150 + bj * 0.7), (sg * 6, 190 + bj), (sg * 30, 222 + bj)], 7, color=SANGRE, op=op * color,
                        afilado=0.8)
            for j in range(12):                                # dientes de abajo (suben desde la mandíbula)
                u = (j + 0.5) / 12
                xb = lerp(-110, 110, u)
                yb = 104 + bj * 0.9 + 55 * (1 - (2 * u - 1) ** 2)
                g.figura(np.float32([(xb - 8, yb), (xb + 8, yb), (xb + 1, yb - 26)]), 0.0, contorno=1.6, op=op)
        # cráneo: ancho en la bisagra, hocico estrecho; sombra desde arriba (la luz le viene de la boca)
        cran = [(0, -158), (92, -140), (158, -88), (180, -16), (160, 30), (80, 50), (0, 54), (-80, 50), (-160, 30),
                (-180, -16), (-158, -88), (-92, -140)]
        pol = catmull(np.float32(cran), 4, True)
        g.figura(pol, 0.18, contorno=3.2, op=op, tono2=0.9, luz=-90, ang=12, per=4.0, borde=0.45, rb=34)
        for i in range(6):                                     # placas de escamas de la frente
            yy = -138 + i * 22
            ww = 74 - i * 7
            for sg in (-1, 1):
                g.trazo(np.float32([(0, yy), (sg * ww * 0.55, yy + 6), (sg * ww, yy + 18)]), 2.4, op=0.9 * op, afilado=0.5)
        for sg in (-1, 1):
            g.trazo(np.float32([(sg * 18, -10), (sg * 34, 40)]), 2.0, op=0.8 * op)                 # surcos del hocico
            g.macizo(tr(circ_pts(0, 0, 10, 12, 4), sg * 24, 30, 1, sg * 0.6), op)                # fosetas
        # dientes de arriba y colmillos
        if boca > 0.05:
            for j in range(12):
                u = (j + 0.5) / 12
                xb = lerp(-120, 120, u)
                yb = 46 + 6 * (1 - (2 * u - 1) ** 2)
                g.figura(np.float32([(xb - 8, yb), (xb + 8, yb), (xb + 1, yb + 24)]), 0.0, contorno=1.6, op=op)
        for sg in (-1, 1):
            f = catmull(np.float32([(sg * 64, 44), (sg * 88, 44), (sg * 84, 110 + bj * 0.7), (sg * 72, 168 + bj * 0.8),
                                    (sg * 70, 100 + bj * 0.5)]), 4, True)
            g.figura(f, 0.05, contorno=2.4, op=op, tono2=0.5, luz=0, ang=80, per=3.4, cruz=False)
        # ojos rasgados de rendija, con el ceño encima
        for sg in (-1, 1):
            ojo = tr(circ_pts(0, 0, 44, 28, 17), sg * 98, -44, 1, -sg * 0.38)
            g.figura(ojo, 0.0, contorno=3.0, op=op)
            if ojos > 0.01:
                g.acento(ojo, SANGRE, ojos * op * color, aspero=0.2)
                g.acento_luz(sg * 98, -44, 150, SANGRE, 0.9 * ojos * op * color)
            g.macizo(tr(np.float32([(-4, -16), (4, -16), (2, 16), (-2, 16)]), sg * 98, -44, 1, -sg * 0.38), op)
            ceno = [(sg * 30, -64), (sg * 120, -92), (sg * 176, -70), (sg * 150, -62), (sg * 110, -72), (sg * 40, -50)]
            g.figura(catmull(np.float32(ceno), 3, True), 0.75, contorno=2.4, op=op, ang=-20 * sg, per=3.4)
        g.acento(pol, SANGRE, 0.45 * op * color, sem=11)


# ------------------------------------------------------------------ selva de Zul'Gurub
def _palmera(g, x, y, s, t, sem=0, alto=1.0, inclin=0.0, op=1.0):
    """Palmera de selva: tronco anillado que se curva y penacho de frondas de pluma que se mecen. ~700*alto de alto."""
    if s <= 0.004:
        return
    with g.grupo(x, y, s):
        H_ = 700 * alto
        cur = (inclin + 0.25 * (rnd(sem, 1) - 0.5)) * 220
        esp = [(0, 0), (cur * 0.3, -H_ * 0.35), (cur * 0.75, -H_ * 0.7), (cur, -H_)]
        pol, P, nrm = tubo(esp, 46, 28, 6)
        g.figura(pol, 0.25, contorno=2.4, op=op, tono2=0.85, luz=0, ang=0, per=4.4, cruz=False)
        for i in range(2, len(P) - 1, 2):
            w = lerp(46, 28, i / len(P)) / 2
            g.trazo([P[i] - nrm[i] * w, P[i] + nrm[i] * w * 1.05], 2.0, op=0.9 * op, afilado=0.3)
        top = P[-1]
        for j in range(8):
            an = math.radians(-180 + j * 26 + 8 * math.sin(t * 0.9 + j + sem)) if j < 7 else math.radians(-90)
            L = 260 + 80 * rnd(sem, j)
            caida = 0.55 + 0.25 * rnd(sem, j + 9)
            pts = [(top[0], top[1])]
            for u in np.linspace(0.2, 1.0, 5):
                pts.append((top[0] + L * u * math.cos(an), top[1] + L * u * math.sin(an) + caida * L * u * u))
            P2 = catmull(np.float32(pts), 4)
            g.trazo(P2, 7, w1=2.5, op=op, afilado=0.3)
            d = np.gradient(P2, axis=0)
            d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-6
            for i in range(1, len(P2), 2):                   # folíolos colgantes
                for sg in (-1, 1):
                    n_ = np.float32((-d[i, 1], d[i, 0])) * sg
                    Lf = 50 * (1 - i / len(P2)) + 16
                    q = P2[i] + n_ * Lf * 0.6 + np.float32((0, Lf * 0.7))
                    g.trazo([P2[i], q], 3.6, op=0.85 * op, afilado=0.8)
        g.figura(circ_pts(top[0], top[1], 30, 14), 0.6, contorno=2.0, op=op, ang=30, per=4)


def _helecho(g, x, y, s, t, sem=0, op=1.0, n=7):
    """Mata de helecho en el suelo: frondas arqueadas con folíolos."""
    if s <= 0.004:
        return
    with g.grupo(x, y, s):
        for j in range(n):
            an = math.radians(-160 + j * (140 / max(n - 1, 1)) + 6 * math.sin(t * 1.1 + j + sem))
            L = 140 + 60 * rnd(sem, j)
            pts = [(0, 0)] + [(L * u * math.cos(an), L * u * math.sin(an) + 0.5 * L * u * u) for u in (0.33, 0.66, 1.0)]
            P = catmull(np.float32(pts), 4)
            g.trazo(P, 2.4, w1=0.8, op=op, afilado=0.4)
            for i in range(1, len(P) - 1):
                for sg in (-1, 1):
                    q = P[i] + np.float32((sg * 10 * (1 - i / len(P)) + 2, -10 * (1 - i / len(P)) * 0 + 12))
                    g.trazo([P[i], q], 1.6, op=0.85 * op, afilado=0.8)


def hoja_grande(g, x, y, s, t, ang=-60.0, sem=0, op=1.0, tono=0.75):
    """Hoja enorme de primer plano (enmarca y da escala): limbo lanceolado, nervio y nervaduras de buril."""
    a = math.radians(ang + 4 * math.sin(t * 0.7 + sem))
    L, Wd = 520, 150
    loc = [(0, 0), (0.15, 0.55), (0.45, 0.85), (0.8, 0.5), (1.0, 0.0), (0.8, -0.45), (0.45, -0.8), (0.15, -0.5)]
    pts = np.float32([(x + s * L * u * math.cos(a) - s * Wd * v * math.sin(a), y + s * L * u * math.sin(a) + s * Wd * v *
                       math.cos(a)) for u, v in loc])
    pol = catmull(pts, 4, True)
    g.figura(pol, tono, contorno=2.6, op=op, ang=math.degrees(a) + 60, per=5.0, cruz=False)
    tip = (x + s * L * math.cos(a), y + s * L * math.sin(a))
    g.trazo([(x, y), tip], 3.5 * s ** 0.3, color=g.fondo_papel, op=0.7 * op, afilado=0.6)
    for i in range(1, 6):
        u = i / 6
        b = (x + s * L * u * math.cos(a), y + s * L * u * math.sin(a))
        for sg in (-1, 1):
            e = (b[0] + s * L * 0.18 * math.cos(a) - sg * s * Wd * 0.6 * (1 - u * 0.6) * math.sin(a),
                 b[1] + s * L * 0.18 * math.sin(a) + sg * s * Wd * 0.6 * (1 - u * 0.6) * math.cos(a))
            g.trazo([b, e], 2.0 * s ** 0.3, color=g.fondo_papel, op=0.55 * op, afilado=0.7)


def liana(g, x0, y0, largo, t, s=1.0, sem=0, op=1.0):
    """Liana que cuelga desde arriba (primer plano) y se mece; hojitas a lo largo."""
    sw = 22 * math.sin(t * 0.8 + sem)
    pts = [(x0, y0), (x0 + sw * 0.3 + 10, y0 + largo * 0.35), (x0 + sw * 0.7 - 8, y0 + largo * 0.7), (x0 + sw, y0 + largo)]
    P = catmull(np.float32(pts), 6)
    g.trazo(P, 7 * s, w1=4 * s, op=op, afilado=0.2)
    for i in range(3, len(P), 4):
        sg = 1 if i % 8 < 4 else -1
        hj = [P[i], P[i] + np.float32((sg * 26 * s, 6 * s)), P[i] + np.float32((sg * 34 * s, 22 * s)),
              P[i] + np.float32((sg * 10 * s, 14 * s))]
        g.figura(catmull(np.float32(hj), 3, True), 0.55, contorno=1.6, op=op, ang=40, per=4, cruz=False)


def estatua_serpiente(g, x, y, s, t, dirx=1, op=1.0, ojos=0.0):
    """Cabeza de serpiente tallada en piedra (guarda de la escalinata de Zul'Gurub). ~420 de alto con s=1."""
    def T(p):
        return tr(np.float32(p), x, y, s, 0.0, dirx)
    base = [(-110, 0), (110, 0), (100, -60), (-100, -60)]
    g.figura(T(base), 0.45, contorno=2.4, op=op, ang=0, per=4.6, tono2=0.85, luz=0, cruz=False)
    cuello = tubo([(0, -60), (20, -200), (-10, -300), (20, -360)], 110, 90, 5)[0]
    g.figura(T(cuello), 0.3, contorno=2.6, op=op, tono2=0.85, luz=0, ang=0, per=4.4, borde=0.3, rb=20)
    cab = [(0, -330), (80, -372), (170, -366), (196, -338), (150, -312), (60, -300), (-20, -312)]
    g.figura(T(catmull(np.float32(cab), 4, True)), 0.25, contorno=2.6, op=op, tono2=0.8, luz=-90, ang=10, per=4.2)
    g.trazo(T([(70, -322), (190, -336)]), 3, op=op)
    ex, ey = T([(110, -352)])[0]
    g.circ(ex, ey, 9 * s, TINTA, op)
    if ojos > 0.01:
        g.acento_luz(ex, ey, 60 * s, SANGRE, ojos * op)
    for i in range(5):
        g.trazo(T([(-30 + 4 * i, -90 - 46 * i), (40 + 4 * i, -100 - 46 * i)]), 1.6, op=0.8 * op)


# ------------------------------------------------------------------ bosque y afueras (Dun Morogh)
def _pino(g, x, y, s, t, sem=0, op=1.0, nieve=True, tono=0.55):
    """Abeto de montaña: pisos de ramas colgantes con nieve encima, tronco al pie. ~620 de alto con s=1."""
    if s <= 0.004:
        return
    with g.grupo(x, y, s):
        g.figura(np.float32([(-14, 0), (14, 0), (10, -90), (-10, -90)]), 0.7, contorno=2.0, op=op, ang=90, per=4.2,
                 cruz=False)
        for i in range(6):
            yb = -60 - i * 92
            w = 190 - i * 28
            sw = 5 * math.sin(t * 0.9 + i + sem)
            piso = [(-w + sw, yb), (-w * 0.5, yb - 26), (0 + sw * 0.3, yb - 130), (w * 0.5, yb - 26), (w + sw, yb),
                    (w * 0.6, yb - 10), (0, yb - 14), (-w * 0.6, yb - 10)]
            g.figura(catmull(np.float32(piso), 3, True), tono, contorno=2.2, op=op, tono2=min(1.0, tono + 0.3), luz=0,
                     ang=60, per=4.6, cruz=False)
            if nieve:
                cap = [(-w * 0.55 + sw, yb - 30), (0 + sw * 0.3, yb - 128), (w * 0.55 + sw, yb - 30), (w * 0.3, yb - 40),
                       (0, yb - 46), (-w * 0.3, yb - 40)]
                g.papel(catmull(np.float32(cap), 3, True), op)
                g.trazo(catmull(np.float32(cap[:3]), 3), 1.2, op=0.6 * op)


def barricada(g, cam, X, Z, ancho, t, alza=1.0, op=1.0, texto="CUARENTENA"):
    """Empalizada de cuarentena en el mundo (cruces de San Andrés de troncos) con un cartel clavado; `alza` 0..1 la levanta
    del suelo (aparece). Dibuja en g con la cámara (perspectiva)."""
    import grabado_3d as G3
    if alza <= 0.01:
        return
    hgt = 210 * GR.e_out(alza)
    n = int(ancho / 160)
    for i in range(n):
        x0 = X - ancho / 2 + i * 160
        for (xa, xb) in ((x0, x0 + 160), (x0 + 160, x0)):
            G3.trazo3d(g, cam, [(xa, 0, Z), (xb, -hgt, Z)], 16, op=op, afilado=0.0, sem=i)
            G3.trazo3d(g, cam, [(xa, 0, Z), (xb, -hgt, Z)], 5, color=g.fondo_papel, op=0.45 * op, afilado=0.6, sem=i)
    G3.trazo3d(g, cam, [(X - ancho / 2, -hgt * 0.92, Z - 4), (X + ancho / 2, -hgt * 0.92, Z - 4)], 20, op=op, afilado=0.0)
    G3.trazo3d(g, cam, [(X - ancho / 2, -hgt * 0.92 - 4, Z - 6), (X + ancho / 2, -hgt * 0.92 - 4, Z - 6)], 5,
               color=g.fondo_papel, op=0.4 * op, afilado=0.0)
    if texto and alza > 0.5:
        s = GR.G(t, 520, 150, alfa=True)
        perg = GR.silueta_ruido(np.float32([(10, 10), (510, 6), (514, 140), (6, 144)]), 3.0, sem=7, paso=10)
        s.figura(perg, 0.08, contorno=3.0, ang=0, per=5.0, cruz=False)
        s.texto(texto, 260, 78, 64, TINTA, "gotica")
        s.acento(perg, SANGRE, 0.6, sem=4)
        q = G3.quad_mundo(cam, (X, -hgt * 0.92 - 70, Z - 14), (1, 0, 0), (0, 1, 0), 360, 104, giro=-4)
        if q is not None:
            G3.estampar(g, s, q, sombra=0.4, off=(8, 10), op=op * GR.smooth(GR.pr(alza, 0.5, 1.0)))


# ------------------------------------------------------------------ utilería
def jaula(g, x, y, s, t, op=1.0, sangre=0.0, abre=0.0):
    """Jaulita de hierro (el «establo» del cazador: la mascota guardada) con la sangre dentro latiendo. ~120 de alto.
    (x, y) = asa. `abre` 0..1 abre la portezuela."""
    with g.grupo(x, y, s):
        g.trazo(catmull(np.float32([(-18, 10), (0, -6), (18, 10)]), 4), 3.5, op=op, afilado=0.0)
        cuerpo = [(-44, 30), (44, 30), (52, 140), (-52, 140)]
        if sangre > 0.01:
            lat = 0.85 + 0.15 * math.sin(t * 7)
            g.acento(circ_pts(0, 90, 40 * lat, 20), SANGRE, sangre * op, aspero=1.0)
            g.acento_luz(0, 90, 120, SANGRE, 0.6 * sangre * op)
            for i in range(4):
                yy = 60 + ((t * 30 + i * 20) % 70)
                g.circ(-20 + i * 13, yy, 4, SANGRE, sangre * op)
        g.trazo(np.float32([(-50, 30), (50, 30)]), 5, op=op, afilado=0.0)
        g.trazo(np.float32([(-54, 140), (54, 140)]), 6, op=op, afilado=0.0)
        for i in range(7):
            xx = lerp(-46, 46, i / 6)
            if abre > 0.05 and 1 <= i <= 4:
                continue
            g.trazo([(xx, 30), (xx * 1.13, 140)], 3, op=op, afilado=0.0)
        if abre > 0.05:
            ang = math.radians(-100 * abre)
            for i in range(4):
                xx = lerp(-30, 24, i / 3)
                p0 = (-34, 140)
                d = (xx + 34, -110)
                p1 = (p0[0] + d[0] * math.cos(ang) - d[1] * math.sin(ang), p0[1] + d[0] * math.sin(ang) + d[1] * math.cos(ang))
                g.trazo([p0, p1], 3, op=op, afilado=0.0)


def reloj_arena(t, frac, ancho=300, alto=440):
    """Reloj de arena en un lienzo transparente (para estampar en el mundo): bulbos de vidrio, armazón de madera, arena que
    cae. `frac` 0..1 = cuánta arena ha caído."""
    s = GR.G(t, ancho, alto, alfa=True)
    cx = ancho / 2
    for yy in (24, alto - 24):
        s.figura(np.float32([(20, yy - 16), (ancho - 20, yy - 16), (ancho - 20, yy + 16), (20, yy + 16)]), 0.4, contorno=2.4,
                 ang=0, per=4.2, cruz=False)
    for xx in (34, ancho - 34):
        s.figura(np.float32([(xx - 8, 40), (xx + 8, 40), (xx + 8, alto - 40), (xx - 8, alto - 40)]), 0.5, contorno=2.0, ang=90,
                 per=4.2, cruz=False)
    sup = catmull(np.float32([(60, 44), (ancho - 60, 44), (ancho - 66, 150), (cx + 8, 210), (cx - 8, 210), (66, 150)]), 4, True)
    inf = catmull(np.float32([(cx - 8, 230), (cx + 8, 230), (ancho - 66, 290), (ancho - 60, alto - 44), (60, alto - 44),
                              (66, 290)]), 4, True)
    for b in (sup, inf):
        s.figura(b, 0.0, contorno=2.2)
        s.trazo(b[:6] + np.float32((10, 0)), 1.2, color=s.fondo_papel, op=0.6)
    h_sup = 140 * (1 - frac)
    if h_sup > 4:
        s.trama(np.float32([(70, 210 - h_sup), (ancho - 70, 210 - h_sup), (cx + 8, 210), (cx - 8, 210)]), 0.55, ang=0, per=3.4,
                cruz=False)
    h_inf = 120 * frac
    if h_inf > 2:
        s.trama(np.float32([(64, alto - 46), (ancho - 64, alto - 46), (cx + 40, alto - 46 - h_inf), (cx - 40, alto - 46 - h_inf)]),
                0.55, ang=0, per=3.4, cruz=False)
    if 0.0 < frac < 1.0:
        s.trazo([(cx, 210), (cx, alto - 46 - h_inf)], 2.2, op=0.9, afilado=0.0)
    s.acento(sup, SANGRE, 0.25, sem=2)
    return s


def farol(g, cam, X, Z, t, color, fuerza=1.0, sem=0, alto=1.0):
    """Candelero del cementerio con la llama del color de su noche (I sangre · II plaga · III helado). `fuerza` 0 = apagado."""
    import grabado_3d as G3
    b = cam.pt(X, 0, Z)
    k = cam.k(b[2])
    x, y = b[0], b[1]
    h1 = (26 + 160 * alto) * k
    G3.sombra_contacto(g, cam, X, Z, 50, 20, op=0.8)
    g.figura(np.float32([(x - 34 * k, y), (x + 34 * k, y), (x + 14 * k, y - 26 * k), (x - 14 * k, y - 26 * k)]), 0.3,
             contorno=2.2, ang=0, per=4.2, cruz=False)
    g.figura(np.float32([(x - 6 * k, y - 26 * k), (x + 6 * k, y - 26 * k), (x + 6 * k, y - h1), (x - 6 * k, y - h1)]), 0.35,
             contorno=2.0, ang=90, per=4.2, cruz=False)
    g.figura(np.float32([(x - 30 * k, y - h1), (x + 30 * k, y - h1), (x + 20 * k, y - h1 - 14 * k), (x - 20 * k, y - h1 - 14 * k)]),
             0.4, contorno=2.0, ang=0, per=4.2, cruz=False)
    yv = y - h1 - 14 * k
    g.figura(np.float32([(x - 12 * k, yv), (x + 12 * k, yv), (x + 12 * k, yv - 60 * k), (x - 12 * k, yv - 60 * k)]), 0.06,
             contorno=2.0, tono2=0.5, luz=0, ang=90, per=4.0, cruz=False)
    if fuerza > 0.02:
        GR.llama(g, x, yv - 62 * k, (0.6 + 0.6 * fuerza) * k, t, sem=sem, color=color, acento=0.9)
        g.acento_luz(x, yv - 90 * k, 150 * k * (0.6 + 0.5 * fuerza), color, 0.45 * min(fuerza, 1.3))
        G3.humo(g, x, yv - 130 * k, 0.8 * k, t, sem=sem, op=0.4, alto=260)
    else:
        G3.humo(g, x, yv - 64 * k, 0.8 * k, t, sem=sem, op=0.7, alto=320, hebras=2)
    return x, yv - 90 * k, k


def icono_caida(s, t, cx, cy, e=1.0):
    """Relieve: un personaje que cae de un acantilado (el «mal salto»)."""
    s.figura(np.float32([(cx - 130 * e, cy + 140 * e), (cx - 10 * e, cy - 60 * e), (cx + 10 * e, cy - 60 * e),
                         (cx - 30 * e, cy + 140 * e)]), 0.55, contorno=2.2, ang=70, per=3.8, cruz=False)
    fy = cy - 20 * e + 60 * e * ((t * 0.6) % 1.0)
    with s.grupo(cx + 60 * e, fy, 0.32 * e):
        s.figura(circ_pts(0, -90, 26, 14), 0.1, contorno=2.4)
        s.trazo([(0, -64), (10, 30)], 9, afilado=0.0)
        for a1, a2 in ((-2.4, -0.6), (-0.8, 0.6), (2.6, 1.0), (1.2, 2.6)):
            s.trazo([(4, -30 if abs(a1) < 2 else 26), (4 + 70 * math.cos(a1), (-30 if abs(a1) < 2 else 26) + 70 * math.sin(a1))],
                    7, afilado=0.5)
    for i in range(3):
        s.trazo([(cx + 100 * e + i * 14, cy - 50 * e), (cx + 104 * e + i * 14, cy - 10 * e)], 1.6, op=0.7, afilado=0.9)


def icono_jefe(s, t, cx, cy, e=1.0):
    """Relieve: la calavera cornuda de un jefe."""
    GR.craneo(s, cx, cy + 10 * e, 70 * e, t)
    for sg in (-1, 1):
        cuerno = [(cx + sg * 40 * e, cy - 40 * e), (cx + sg * 110 * e, cy - 80 * e), (cx + sg * 130 * e, cy - 150 * e),
                  (cx + sg * 90 * e, cy - 96 * e), (cx + sg * 30 * e, cy - 62 * e)]
        s.figura(catmull(np.float32(cuerno), 4, True), 0.3, contorno=2.2, ang=40 * sg, per=3.8, tono2=0.8, luz=0)


def icono_apuesta(s, t, cx, cy, e=1.0):
    """Relieve: dos dados tirados y una bolsa de monedas."""
    for i, (dx, dy, an) in enumerate(((-60, 20, 0.3), (60, -10, -0.25))):
        q = tr(np.float32([(-40, -40), (40, -40), (40, 40), (-40, 40)]), cx + dx * e, cy + dy * e, e, an)
        s.figura(q, 0.05, contorno=2.6, tono2=0.5, luz=0, ang=30, per=3.6, cruz=False)
        for (px, py) in ((-18, -18), (18, 18), (0, 0))[: 2 + i]:
            pp = tr(np.float32([(px, py)]), cx + dx * e, cy + dy * e, e, an)[0]
            s.circ(pp[0], pp[1], 7 * e, TINTA)
    bolsa = [(cx - 50 * e, cy + 130 * e), (cx + 50 * e, cy + 130 * e), (cx + 40 * e, cy + 80 * e), (cx + 10 * e, cy + 70 * e),
             (cx + 20 * e, cy + 56 * e), (cx - 20 * e, cy + 56 * e), (cx - 10 * e, cy + 70 * e), (cx - 40 * e, cy + 80 * e)]
    s.figura(catmull(np.float32(bolsa), 4, True), 0.2, contorno=2.2, tono2=0.7, luz=0, ang=60, per=3.8)


def relieve(t, icono, op_tallado=1.0, texto=None):
    """Lienzo transparente de una lápida con un relieve tallado (para estampar en la cara de la tumba)."""
    s = GR.G(t, 360, 520, alfa=True)
    arc = [(180 + 170 * math.cos(u), 190 + 170 * math.sin(u)) for u in np.linspace(math.pi, 2 * math.pi, 20)]
    cara = np.float32([(10, 510)] + arc + [(350, 510)])
    s.figura(cara, 0.18, contorno=3.0, tono2=0.6, luz=0, ang=70, per=5.2, borde=0.25, rb=14)
    s.trazo(np.float32([(36, 490)] + [(180 + 140 * math.cos(u), 196 + 140 * math.sin(u)) for u in
                                      np.linspace(math.pi, 2 * math.pi, 18)] + [(324, 490)]), 1.4, op=0.8)
    if op_tallado > 0.01:
        sub = GR.G(t, 360, 520, alfa=True)
        icono(sub, t, 180, 250, 0.95)
        GR.componer(s, sub, 0.0, 0.0, None, op_tallado)
    if texto:
        s.texto(texto, 180, 440, 36, TINTA, "grab", 0.9)
    return s


def puesto(g, cam, X, Z, t, op=1.0):
    """Puesto de mercader (Forjaz): mostrador con espadas colgadas y un toldo. Dibuja en g con perspectiva."""
    import grabado_3d as G3
    G3.plano(g, cam, (X - 220, -150, Z), (1, 0, 0), (0, 1, 0), 440, 150, 0.45, familias=((90.0, 9.0),), quiebre=0.3, tramo=30,
             contorno=2.4)
    G3.plano(g, cam, (X - 230, -160, Z - 60), (1, 0, 0), (0, 0, 1), 460, 70, 0.2, familias=((0.0, 8.0),), contorno=2.0)
    for xx in (X - 210, X + 210):
        G3.trazo3d(g, cam, [(xx, -150, Z + 10), (xx, -470, Z + 10)], 14, op=op, afilado=0.0)
    for j in range(6):                                        # faldón de tela con picos, colgado del travesaño
        x0, x1 = X - 210 + 70 * j, X - 140 + 70 * j
        q = [(x0, -470, Z - 4), (x1, -470, Z - 4), (x1, -400, Z - 4), ((x0 + x1) / 2, -372, Z - 4), (x0, -400, Z - 4)]
        scr, _ = G3.proyectar(cam, q)
        if scr is not None:
            g.figura(scr, 0.12 if j % 2 else 0.7, contorno=2.0, op=op, ang=90, per=4.2, cruz=False)
            if j % 2 == 0:
                g.acento(scr, SANGRE, 0.5 * op, sem=8 + j)
    for i in range(4):                                        # espadas colgadas del travesaño
        xx = X - 150 + i * 100
        G3.trazo3d(g, cam, [(xx, -440, Z + 6), (xx, -300, Z + 6)], 9, op=op, afilado=0.8)
        G3.trazo3d(g, cam, [(xx - 22, -420, Z + 6), (xx + 22, -420, Z + 6)], 8, op=op, afilado=0.0)
    G3.trazo3d(g, cam, [(X - 210, -450, Z + 8), (X + 210, -450, Z + 8)], 10, op=op, afilado=0.0)
