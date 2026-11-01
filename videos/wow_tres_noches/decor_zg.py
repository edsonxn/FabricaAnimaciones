# -*- coding: utf-8 -*-
"""Decorado 2: ZUL'GURUB (acento SANGRE). La selva de noche con el templo escalonado al fondo (0:41-0:51), la cámara de Hakkar
por dentro (0:51-1:24: el tráiler real colgado como recuerdo, el contagio que salta, el reloj de arena, el círculo de la sala,
el cazador y su lobo que se guarda en la jaula) y el regreso a oscuras con el susto (2:51-2:58)."""
import math

import numpy as np

import anclas as A
import comun as C
import fig as F
import grabado as GR
import grabado_3d as G3
import look as L
from grabado import ORO, SANGRE, TINTA, G, catmull, circ_pts, e_out, lerp, pr, rnd, smooth
from grabado_3d import Camara

# ------------------------------------------------------------------ selva y templo
Z0 = 2600.0                       # frente del primer escalón del templo
NIV, ALT, FON = 5, 200.0, 180.0   # escalones del templo: número, alto, fondo
CAM_S = dict(x=0.0, y=-260.0, z=0.0, guinada=0.0, cabeceo=-4.0, f=1450.0, foco=1900.0, apertura=2.5, bruma=0.36,
             lejos=3400.0)
KF_SELVA = [(A.TR_ZG - 0.8, dict(x=-140.0, y=-240.0, z=-200.0, guinada=-2.0, cabeceo=-3.0)),
            (A.z_blizzard, dict(x=-60.0, y=-250.0, z=170.0, guinada=0.0, cabeceo=-4.0)),
            (A.T_ENTRA + 0.5, dict(x=0.0, y=-300.0, z=720.0, guinada=0.0, cabeceo=-7.5))]


def _escalinata(u):
    """Punto central de la escalinata a la altura u (0 = suelo, 1 = arriba)."""
    return -ALT * NIV * u, Z0 - 260 + (FON * (NIV - 1) + 260) * u


def _palmeras():
    out = []
    for i in range(30):
        lado = -1 if i % 2 else 1
        X = lado * (650 + 2100 * rnd(i, 31))
        Z = 1250 + 2700 * rnd(i, 32)
        if abs(X) < 1450 and Z > Z0 - 150:
            continue
        cerca = Z < 2200                                   # las cercanas, más bajas: que se vea el penacho
        out.append((X, Z, (0.55 if cerca else 0.75) + 0.35 * rnd(i, 33), (rnd(i, 34) - 0.5) * 0.8, i))
    return out


PALMERAS = _palmeras()
# pegatinas reales de Zul'Gurub: (PNJ, X, Y, Z, alto en el mundo, espejo); persona dibujada ≈ 360
_Ye, _Ze = _escalinata(0.62)
_Yt, _Zt = _escalinata(1.0)
PEG_SELVA = [("Gurubashi Berserker", 560.0, 0.0, Z0 - 450, 500.0, True),
             ("Gurubashi Axe Thrower", 760.0, 0.0, Z0 - 330, 400.0, True),
             ("Hakkari Priest", -175.0, _Ye, _Ze, 390.0, False),
             ("Hakkari Priest", 175.0, _Ye, _Ze, 390.0, True),
             ("Bloodlord Mandokir", 0.0, _Yt, _Zt + 60, 430.0, False),
             ("Zulian Tiger", -820.0, 0.0, 1950.0, 230.0, False),
             ("Zulian Tiger", 900.0, 0.0, 1550.0, 230.0, True)]
# estatuas de cobra REALES (recortadas del tráiler) que flanquean el camino: elementos del decorado, sin borde de papel
COBRAS_SELVA = [(-680.0, 1350.0), (330.0, 1350.0), (-700.0, 2050.0)]


def _templo(g, cam, t, luces):
    for i in reversed(range(NIV)):
        w = 2600 - 380 * i
        zf = Z0 + FON * i
        yt = -ALT * (i + 1)
        G3.plano(g, cam, (-w / 2, yt, zf), (1, 0, 0), (0, 1, 0), w, ALT, 0.46, familias=((0.0, 10.0), (60.0, 14.0)),
                 patron=("sillares", 230, 100), quiebre=0.35, tramo=55, luces=luces, oscuro=0.42, junta=5)
        if cam.C[1] < yt:
            G3.plano(g, cam, (-w / 2, yt, zf), (1, 0, 0), (0, 0, 1), w, FON, 0.72, familias=((0.0, 9.0),), luces=luces,
                     oscuro=0.3)
        # friso de serpientes talladas en cada escalón
        xs = np.linspace(-w / 2 + 40, w / 2 - 40, 40)
        G3.trazo3d(g, cam, [(x_, yt + ALT * 0.5 + 18 * math.sin(x_ / 70 + i), zf - 2) for x_ in xs], 6, afilado=0.2,
                   densidad=2)
    # santuario de arriba con la puerta
    zs = Z0 + FON * (NIV - 1) + 40
    ys = -ALT * NIV
    G3.plano(g, cam, (-340, ys - 440, zs), (1, 0, 0), (0, 1, 0), 680, 440, 0.4, familias=((0.0, 10.0), (60.0, 14.0)),
             patron=("sillares", 170, 90), quiebre=0.35, tramo=50, luces=luces, oscuro=0.4, junta=5)
    for j, (wc, hc) in enumerate(((560, 70), (420, 60), (260, 60))):
        G3.plano(g, cam, (-wc / 2, ys - 440 - 70 * j - hc, zs + 8 + 20 * j), (1, 0, 0), (0, 1, 0), wc, hc, 0.5,
                 familias=((0.0, 9.0),), quiebre=0.3, luces=luces, oscuro=0.4)
    for sg, nom in ((-1, "relieve_izq"), (1, "relieve_der")):   # relieves REALES del templo (tráiler de Blizzard)
        C.relieve(g, cam, C.png_video(nom), (sg * 228, ys - 155, zs - 3), (1, 0, 0), 150, 310, t, sem=sg + 5)
    puerta = [(-120, ys - 300, zs - 2), (120, ys - 300, zs - 2), (120, ys, zs - 2), (-120, ys, zs - 2)]
    scr, _ = G3.proyectar(cam, puerta)
    if scr is not None:
        g.macizo(scr)
        brillo = 0.35 + 0.55 * smooth(pr(t, A.z_zg - 0.2, A.z_zg + 0.6)) + 0.08 * math.sin(t * 3)
        c = scr.mean(0)
        g.acento_luz(c[0], c[1], 1.6 * abs(scr[1][0] - scr[0][0]), SANGRE, brillo)
        ojo_k = smooth(pr(t, A.z_fondo - 1.2, A.z_fondo))
        for sg in (-1, 1):                                 # algo mira desde dentro
            g.circ(c[0] + sg * 0.12 * abs(scr[1][0] - scr[0][0]), c[1] - 0.05 * abs(scr[2][1] - scr[0][1]),
                   2.5 + 3 * ojo_k, SANGRE, 0.4 + 0.6 * ojo_k)
    # dintel con el nombre (se talla a «Zul'Gurub»)
    tz = smooth(pr(t, A.z_zg - 0.1, A.z_zg + 0.5))
    if tz > 0.01:
        s = G(t, 640, 120, alfa=True)
        s.figura(np.float32([(4, 8), (636, 4), (632, 116), (8, 112)]), 0.55, contorno=3.0, ang=0, per=5, cruz=False)
        s.texto("ZVL'GVRVB", 320, 64, 72, (0.93, 0.87, 0.77), "capital", tz)
        s.acento(np.float32([(4, 8), (636, 4), (632, 116), (8, 112)]), SANGRE, 0.55 * tz, sem=3)
        q = G3.quad_mundo(cam, (0, ys - 370, zs - 6), (1, 0, 0), (0, 1, 0), 520, 98)
        if q is not None:
            G3.estampar(g, s, q, sombra=0.0)
    # escalinata
    zb = Z0 - 260
    zt = Z0 + FON * (NIV - 1)
    V = np.float32((0, -ALT * NIV, zt - zb))
    av = float(np.linalg.norm(V))
    per = av / 30

    def tono_escalon(a, b, zc):
        f = (b % per) / per
        return np.where(f > 0.62, 0.86, 0.34 + 0.1 * f)
    G3.plano(g, cam, (-170, 0, zb), (1, 0, 0), tuple(V / av), 340, av, tono_escalon, familias=((0.0, per / 5),),
             luces=luces, oscuro=0.45)
    for sg in (-1, 1):
        G3.trazo3d(g, cam, [(sg * 190, -30, zb - 10), (sg * 190, -ALT * NIV - 30, zt)], 38, afilado=0.0, densidad=20)
        G3.trazo3d(g, cam, [(sg * 190, -40, zb - 12), (sg * 190, -ALT * NIV - 40, zt - 2)], 9, color=g.fondo_papel, op=0.45,
                   afilado=0.6, densidad=20)


def _antorcha(g, cam, X, Y, Z, t, f, sem):
    """Antorcha en la escalinata: palo, cuenco y llama; `f` 0..1 encendida. Devuelve la luz (pantalla) o None."""
    G3.trazo3d(g, cam, [(X, Y, Z), (X, Y - 130, Z)], 10, afilado=0.0)
    px, py, zc = cam.pt(X, Y - 130, Z)
    k = cam.k(zc)
    g.figura(np.float32([(px - 20 * k, py), (px + 20 * k, py), (px + 12 * k, py + 16 * k), (px - 12 * k, py + 16 * k)]), 0.5,
             contorno=1.8, ang=0, per=4, cruz=False)
    if f > 0.02:
        GR.llama(g, px, py, 1.3 * k * (0.5 + 0.5 * f), t, sem=sem, color=ORO)
        G3.humo(g, px, py - 70 * k, 0.6 * k, t, sem=sem, op=0.45, alto=220)
        return (px, py - 30 * k, 420 * k * f, 0.7 * f, ORO)
    return None


def _raid(t):
    """La banda de 20 que marcha al templo (entra por la izquierda) y empieza a subir. [(X, Y, Z, i)]"""
    out = []
    p0, p1 = np.float32((-560, 700)), np.float32((-60, Z0 - 330))
    L1 = float(np.linalg.norm(p1 - p0))
    for i in range(20):
        d = (t - (A.z_blizzard - 0.6)) * 300 - i * 85 - (i % 3) * 20
        if d < 0:
            continue
        if d < L1:
            X, Z = p0 + (p1 - p0) * (d / L1)
            Y = 0.0
        else:
            u = min(1.0, (d - L1) / 1500)
            Y, Z = _escalinata(u)
            X = -60 + 40 * ((i % 4) - 1.5)
        out.append((float(X) + 30 * ((i % 3) - 1), Y, float(Z), i))
    return out


def selva(t):
    cam = C.camara(t, KF_SELVA, CAM_S)
    mx, my = 1420 - 0.2 * cam.C[0], 150

    # FONDO cacheado por tick de HERVOR (GR.fondo): cielo, luna, nubes, colina y, con la cámara quieta, el suelo
    def lejos(g, tt):
        cm = C.camara(tt, KF_SELVA, CAM_S)
        hz_ = cm.horizonte()
        GR.cielo(g, tt, hz_ + 60, tono_alto=1.0, tono_bajo=0.6)
        mx_ = 1420 - 0.2 * cm.C[0]
        GR.luna(g, mx_, my, 66, tt, tono_cielo=0.86)
        g.acento_luz(mx_, my, 160, SANGRE, 0.35)
        GR.nube(g, 1500, 220, 480, tt, sem=5, vel=6, tono=0.3)
        GR.nube(g, 380, 140, 420, tt, sem=7, vel=5)
        GR.colina(g, GR.perfil_colina(-60, 1980, hz_ + 4, 40, sem=4, ondas=3.0), tono=0.3, tono2=0.5, ang=-3, per=5.0,
                  contorno=1.6, cruz=False)

    def tono_suelo(a, b, zc):
        senda = np.clip(1 - np.abs(a + 40) / (190 + 0.04 * b), 0, 1) * (b < Z0)
        return 0.6 - 0.28 * senda

    def _luces(tt):
        luces, antorchas = [], []
        for j in range(NIV):
            u = (j + 0.45) / NIV
            y_, z_ = _escalinata(u)
            f = smooth(pr(tt, A.z_blizzard + 0.45 * j, A.z_blizzard + 0.45 * j + 0.4))
            antorchas.append((y_, z_, f, j))
            for sg in (-1, 1):
                luces.append((sg * 240, y_ - 120, z_, 380 * f + 1, 0.55 * f))
        luces.append((0, -ALT * NIV - 150, Z0 + FON * (NIV - 1), 600, 0.5))
        return luces, antorchas

    def suelo(g, tt):
        G3.plano(g, C.camara(tt, KF_SELVA, CAM_S), (-6000, 0, -600), (1, 0, 0), (0, 0, 1), 12000, Z0 + 600, tono_suelo,
                 familias=((0.0, 14.0),), luces=_luces(tt)[0], oscuro=0.25)

    def f_lejos(tt):
        cm = C.camara(tt, KF_SELVA, CAM_S)
        return cm.horizonte(), 0.2 * cm.C[0]

    def f_suelo(tt):
        return G3.firma_cerca(C.camara(tt, KF_SELVA, CAM_S)) + tuple(300 * lz[4] for lz in _luces(tt)[0])
    g = GR.fondo(t, "selva", [(lejos, f_lejos), (suelo, f_suelo)])
    for i in range(4):                                     # murciélagos/cuervos sobre la selva (vuelan sobre la colina)
        cx = (200 + 430 * i + t * (55 + 12 * i)) % 2300 - 150
        GR.cuervo(g, cx, 260 + 50 * i + 18 * math.sin(t * 1.3 + i), 0.55 - 0.08 * i, t * 1.4, fase=i * 1.7)
    luces, antorchas = _luces(t)
    # palmeras y helechos de atrás (detrás o al lado del templo)
    objs = []
    for X, Z, alto, inc, i in PALMERAS:
        if Z > Z0 - 150:
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, alto=alto, inc=inc, i=i: F.palmera(
                c, *cam.pt(X, 0, Z)[:2], cam.k(cam.pt(X, 0, Z)[2]), t, sem=i, alto=alto, inclin=inc)))
    C.figuras(g, cam, objs, cortes=(3200.0,))
    _templo(g, cam, t, luces)
    luz_pant = []
    for y_, z_, f, j in antorchas:
        for sg in (-1, 1):
            r = _antorcha(g, cam, sg * 240, y_ - 20, z_, t, f, j * 2 + (sg > 0))
            if r:
                luz_pant.append(r)
    for sg in (-1, 1):                                     # guardas de piedra al pie de la escalinata
        px, py, zc = cam.pt(sg * 330, 0, Z0 - 330)
        F.estatua_serpiente(g, px, py, 0.8 * cam.k(zc), t, dirx=sg, ojos=smooth(pr(t, A.z_zg, A.z_zg + 0.5)))
    # lo de delante del templo: palmeras, helechos, la banda que marcha
    objs = []
    for X, Z, alto, inc, i in PALMERAS:
        if Z <= Z0 - 150:
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, alto=alto, inc=inc, i=i: F.palmera(
                c, *cam.pt(X, 0, Z)[:2], cam.k(cam.pt(X, 0, Z)[2]), t, sem=i, alto=alto, inclin=inc)))
    for i in range(34):
        X = (rnd(i, 41) - 0.5) * 3600
        Z = 300 + 2200 * rnd(i, 42)
        if abs(X + 40) < 260:
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: F.helecho(c, *cam.pt(X, 0, Z)[:2], 0.9 * cam.k(cam.pt(X, 0, Z)[2]), t,
                                                                   sem=i)))
    # los guardianes REALES de Zul'Gurub (pegatinas): se levantan como un libro desplegable a «Zul'Gurub»
    for j, (nom, X, Y, Z, alto, esp) in enumerate(PEG_SELVA):
        alza = smooth(pr(t, A.z_zg - 0.5 + 0.22 * j, A.z_zg + 0.1 + 0.22 * j))
        if nom.endswith("Tiger"):                          # los tigres rondan entre los helechos
            X = X + 60 * math.sin(t * 0.35 + j)
        C.peg(objs, cam, t, nom, X, Z, alto, Y=Y, alza=alza, espejo=esp, sem=80 + j)
    for j, (X, Z) in enumerate(COBRAS_SELVA):
        C.peg(objs, cam, t, "png:cobra_izq" if X < 0 else "png:cobra_der", X, Z, 330, borde=0, aleteo=0.0, sombra=0.0,
              contacto=1.0, tinta=0.3, sem=20 + j)
    for X, Y, Z, i in _raid(t):
        tipo = ("guerrero", "capa", "sanador", "cazador", "enano")[i % 5]
        objs.append((X, Y, Z, lambda c, X=X, Y=Y, Z=Z, i=i, tipo=tipo: F.persona(
            c, *cam.pt(X, Y, Z)[:2], 0.95 * cam.k(cam.pt(X, Y, Z)[2]), t, tipo, fase=i * 0.7, anda=1.0, dirx=1, sem=i)))
    C.figuras(g, cam, objs)
    # la fecha: cartela que cuelga de una rama, a la izquierda
    op = C.env(t, A.z_13 - 0.3, A.T_ENTRA - 0.5, 0.5, 0.4)
    if op > 0.01:
        rx, rz = -260.0, 1750.0
        G3.trazo3d(g, cam, [(rx - 700, -900, rz + 60), (rx + 420, -840, rz - 30)], 24, afilado=0.3)
        C.cartela_colgada(g, cam, (rx, -520 + 12 * math.sin(t * 1.1), rz), "XIII de Septiembre de MMV", t, ancho=640,
                          alto=120, px=40, op=op, techo=-865, giro=2 * math.sin(t * 0.9))
    G3.iluminar(g, luz_pant + [(mx, my, 700, 0.5)], amb=0.14, fuerza=0.6, acento=0.2)
    G3.particulas(g, t, "polvo", 60, (0, 300, 1920, 1080), sem=11)
    y_nb = cam.pt(0, 0, cam.C[2] + 1400)[1]
    GR.niebla(g, y_nb - 50, y_nb + 20, t, op=0.45, sem=3, vel=16)
    # primer plano: hojas enormes desenfocadas y lianas
    with GR.capa(g, desenfoque=9) as c:
        F.hoja_grande(c, -60, 1120, 1.5, t, ang=-55, sem=1, tono=0.85)
        F.hoja_grande(c, 120, 1150, 1.2, t, ang=-80, sem=2, tono=0.9)
        F.hoja_grande(c, 1990, 1100, 1.4, t, ang=-128, sem=3, tono=0.85)
        F.hoja_grande(c, 1700, 1180, 1.0, t, ang=-100, sem=4, tono=0.9)
        F.liana(c, 230, -20, 520, t, s=1.6, sem=1)
        F.liana(c, 1650, -20, 380, t, s=1.4, sem=2)
    return g


# ------------------------------------------------------------------ la cámara de Hakkar
ANCHO, FONDO, TECHO = 800.0, 3000.0, -950.0
HAKKAR = (0.0, -160.0, 2620.0)
ANILLO = (0.0, 1800.0, 470.0)
CAZADOR = (-470.0, 1250.0)
LOBO = (-300.0, 1180.0)
RELOJ = (240.0, 900.0)
CAM_H = dict(x=0.0, y=-190.0, z=150.0, guinada=0.0, cabeceo=-4.0, f=1400.0, foco=2300.0, apertura=7.0, bruma=0.3,
             lejos=3600.0)
KF_CAMARA = [(A.T_ENTRA, dict(x=0.0, y=-200.0, z=120.0, guinada=0.0, cabeceo=-4.0, foco=2300.0)),
             (A.z_dios, dict(x=-50.0, y=-210.0, z=280.0, guinada=-4.0, cabeceo=-4.0, foco=2200.0)),
             (A.z_enfermedad - 0.4, dict(x=0.0, y=-200.0, z=430.0, guinada=0.0, cabeceo=-3.0, foco=1300.0)),
             (A.z_durar - 1.0, dict(x=40.0, y=-195.0, z=500.0, guinada=2.0, cabeceo=-2.0, foco=1250.0)),
             (A.z_durar - 0.2, dict(x=50.0, y=-195.0, z=520.0, guinada=3.0, cabeceo=-1.0, foco=420.0)),
             (A.z_dentro - 0.5, dict(x=50.0, y=-200.0, z=540.0, guinada=3.0, cabeceo=-1.0, foco=420.0)),
             (A.z_sala + 0.5, dict(x=0.0, y=-470.0, z=470.0, guinada=0.0, cabeceo=13.0, foco=1300.0)),
             (A.z_detalle, dict(x=-70.0, y=-260.0, z=400.0, guinada=-18.0, cabeceo=3.0, foco=760.0)),
             (A.m_guardaban, dict(x=-150.0, y=-240.0, z=500.0, guinada=-22.0, cabeceo=2.0, foco=650.0)),
             (A.TR_FORJAZ, dict(x=-300.0, y=-265.0, z=760.0, guinada=-25.0, cabeceo=3.0, foco=420.0))]
KF_FINAL = [(A.TR_HAKKAR - 0.6, dict(x=0.0, y=-190.0, z=700.0, guinada=0.0, cabeceo=-5.0, foco=1900.0)),
            (A.T_SUSTO, dict(x=0.0, y=-230.0, z=1250.0, guinada=0.0, cabeceo=-9.0, foco=1400.0))]


def _sala(g, cam, t, luces, oscuro_extra=0.0):
    """Suelo, muros, techo, fondo, altar y columnas de la cámara."""
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.92, ang=10, per=6.0)
    G3.plano(g, cam, (-ANCHO, TECHO, -200), (1, 0, 0), (0, 0, 1), 2 * ANCHO, FONDO + 200, 0.93,
             familias=((90.0, 12.0), (0.0, 16.0)), patron=("losas", 260), luces=luces, oscuro=0.1, junta=6)
    for X in (-ANCHO, ANCHO):
        G3.plano(g, cam, (X, TECHO, -200), (0, 0, 1), (0, 1, 0), FONDO + 200, -TECHO, 0.5,
                 familias=((0.0, 9.0), (60.0, 12.0)), patron=("sillares", 200, 95), quiebre=0.35, tramo=55, luces=luces,
                 oscuro=0.58 + oscuro_extra, junta=5)
        zs = np.linspace(0, FONDO, 60)                     # serpiente tallada a lo largo del muro
        sg = 1 if X < 0 else -1
        G3.trazo3d(g, cam, [(X + sg * 3, -640 + 40 * math.sin(z_ / 120 + t * 0.2), z_) for z_ in zs], 16, afilado=0.1,
                   densidad=2)
        G3.trazo3d(g, cam, [(X + sg * 4, -646 + 40 * math.sin(z_ / 120 + t * 0.2), z_) for z_ in zs], 4,
                   color=g.fondo_papel, op=0.5, afilado=0.5, densidad=2)
    G3.plano(g, cam, (-ANCHO, 0, -200), (1, 0, 0), (0, 0, 1), 2 * ANCHO, FONDO + 200, 0.32, familias=((0.0, 9.0),),
             patron=("losas", 180), luces=luces, oscuro=0.42 + oscuro_extra, junta=5, quiebre=0.3, tramo=50)
    G3.plano(g, cam, (-ANCHO, TECHO, FONDO), (1, 0, 0), (0, 1, 0), 2 * ANCHO, -TECHO, 0.5, familias=((0.0, 9.0), (60.0, 12.0)),
             patron=("sillares", 200, 95), quiebre=0.35, tramo=55, luces=luces, oscuro=0.45 + oscuro_extra, junta=5)
    for j, (zf, yt) in enumerate(((2200.0, -80.0), (2300.0, -160.0))):    # dos gradas del altar
        G3.plano(g, cam, (-ANCHO, yt, zf), (1, 0, 0), (0, 1, 0), 2 * ANCHO, 80, 0.4, familias=((0.0, 8.0),), luces=luces,
                 oscuro=0.4)
        G3.plano(g, cam, (-ANCHO, yt, zf), (1, 0, 0), (0, 0, 1), 2 * ANCHO, FONDO - zf, 0.62, familias=((0.0, 9.0),),
                 patron=("losas", 200), luces=luces, oscuro=0.4, junta=4)


def _anillo(g, cam, t, fuerza):
    """Círculo ritual en el suelo (la «sala»): aro de sangre con glifos."""
    cx, cz, r = ANILLO
    a = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    for rr, w in ((r, 10.0), (r * 0.9, 4.0)):
        G3.trazo3d(g, cam, [(cx + rr * math.cos(u), -1, cz + rr * math.sin(u)) for u in a], w, cerrado=True, afilado=0.0,
                   densidad=2)
    out = np.stack([cx + r * 1.03 * np.cos(a), np.full_like(a, -1), cz + r * 1.03 * np.sin(a)], 1)
    inn = np.stack([cx + r * 0.87 * np.cos(a[::-1]), np.full_like(a, -1), cz + r * 0.87 * np.sin(a[::-1])], 1)
    scr, _ = G3.proyectar(cam, np.vstack([out, inn]))
    if scr is not None:
        g.acento(scr, SANGRE, (0.45 + 0.4 * fuerza) * (0.9 + 0.1 * math.sin(t * 4)), aspero=0.6)
    for i in range(16):
        u = i / 16 * 6.2832 + 0.05 * t
        p0 = (cx + r * 0.92 * math.cos(u), -1, cz + r * 0.92 * math.sin(u))
        p1 = (cx + r * 0.99 * math.cos(u + 0.06), -1, cz + r * 0.99 * math.sin(u + 0.06))
        G3.trazo3d(g, cam, [p0, p1], 6, afilado=0.0, densidad=3)


def _brasero(g, cam, X, Z, t, f, sem):
    b = cam.pt(X, 0, Z)
    k = cam.k(b[2])
    G3.sombra_contacto(g, cam, X, Z, 70, 26, op=0.85)
    g.figura(np.float32([(b[0] - 16 * k, b[1]), (b[0] + 16 * k, b[1]), (b[0] + 10 * k, b[1] - 150 * k),
                         (b[0] - 10 * k, b[1] - 150 * k)]), 0.4, contorno=2.0, ang=90, per=4.2, cruz=False)
    cu = catmull(np.float32([(b[0] - 70 * k, b[1] - 150 * k), (b[0] + 70 * k, b[1] - 150 * k), (b[0] + 40 * k, b[1] - 110 * k),
                             (b[0] - 40 * k, b[1] - 110 * k)]), 3, True)
    g.figura(cu, 0.3, contorno=2.4, tono2=0.8, luz=0, ang=0, per=4.2, cruz=False)
    if f > 0.02:
        for j in range(3):
            GR.llama(g, b[0] + (j - 1) * 30 * k, b[1] - 148 * k, (1.3 - 0.3 * abs(j - 1)) * k * f, t, sem=sem * 3 + j,
                     color=SANGRE if j == 1 else ORO)
        G3.particulas(g, t, "brasas", 10, (b[0] - 80 * k, b[1] - 400 * k, b[0] + 80 * k, b[1] - 150 * k), sem=sem, escala=k)
        G3.humo(g, b[0], b[1] - 240 * k, 0.9 * k, t, sem=sem, op=0.4, alto=300)
        return (b[0], b[1] - 190 * k, 700 * k * f, 0.85 * f, ORO)
    return None


def _raid_anillo():
    """Los 7 de la banda en semicírculo ante Hakkar (X, Z, dirx)."""
    cx, cz, r = ANILLO
    out = []
    for i, a in enumerate((215, 182, 150, 30, -2, -35)):  # dos flancos: el centro queda libre para ver a Hakkar
        a = math.radians(a)
        X, Z = cx + r * math.cos(a), cz + r * math.sin(a)
        out.append((X, Z, 1 if X < 0 else -1, i))
    return out


def _cabeza(X, Z):
    return X, -330.0, Z


def camara(t):
    cam = C.camara(t, KF_CAMARA, CAM_H)
    g = G(t)
    hx, hy, hz = HAKKAR
    luz_altar = 0.6 + 0.3 * smooth(pr(t, A.z_hakkar - 0.3, A.z_hakkar + 0.6))
    luces3 = [(sg * 520, -300, z_, 700, 0.85) for sg in (-1, 1) for z_ in (1000, 2000)] + [(0, -400, 2500, 900, luz_altar)]
    _sala(g, cam, t, luces3)
    anillo_f = smooth(pr(t, A.z_sala - 0.8, A.z_sala)) * (1 - 0.6 * smooth(pr(t, A.z_alguien, A.z_alguien + 1.5)))
    _anillo(g, cam, t, anillo_f)
    luces = []
    objs = []
    # Hakkar en su altar
    px, py, zc = cam.pt(hx, hy, hz)
    ojos = smooth(pr(t, A.z_hakkar - 0.2, A.z_hakkar + 0.5))
    boca = 0.35 * smooth(pr(t, A.z_sangre - 0.2, A.z_sangre + 0.3)) * (1 - smooth(pr(t, A.z_segundos, A.z_segundos + 1)))
    objs.append((hx, hy, hz, lambda c: F.hakkar(c, px, py, 0.8 * cam.k(zc), t, ojos=ojos, boca=boca)))
    # columnas
    for sg in (-1, 1):
        for Z in (800.0, 1500.0, 2150.0):
            objs.append((sg * 640, -400, Z, lambda c, X=sg * 640, Z=Z: L._columna(c, cam, X, Z, luces3)))
    # braseros
    for sg in (-1, 1):
        for j, Z in enumerate((1000.0, 2000.0)):
            def br(c, X=sg * 520, Z=Z, j=j):
                r = _brasero(c, cam, X, Z, t, 1.0, int(X) + j)
                if r:
                    luces.append(r)
            objs.append((sg * 520, -100, Z, br))
    # sacerdotes REALES de Hakkar a los lados del altar (pegatinas)
    for j, sg in enumerate((-1, 1)):
        C.peg(objs, cam, t, "Hakkari Priest", sg * 400.0, 2250.0, 390.0, espejo=sg > 0, sem=90 + j,
              alza=smooth(pr(t, A.T_ENTRA + 0.3 * j, A.T_ENTRA + 0.6 + 0.3 * j)))
        C.peg(objs, cam, t, "png:cobra_der" if sg > 0 else "png:cobra_izq", sg * 580.0, 2480.0, 360.0, borde=0,
              aleteo=0.0, sombra=0.0, contacto=1.0, tinta=0.3, sem=95 + j)
    # la banda en el círculo; el contagio salta de uno a otro
    raid = _raid_anillo()
    t_salto = [A.z_saltaba + 0.33 * i for i in range(len(raid))]
    for (X, Z, dx, i) in raid:
        inf = smooth(pr(t, t_salto[i], t_salto[i] + 0.25))
        cae = 0.22 * smooth(pr(t, A.z_drenaba + 0.1 * i, A.z_drenaba + 0.1 * i + 0.8)) * (1 - smooth(pr(t, A.z_alguien,
                                                                                                           A.z_alguien + 1)))
        tipo = ("guerrero", "sanador", "capa", "enano", "guerrero", "capa")[i]
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, dx=dx, i=i, inf=inf, cae=cae, tipo=tipo: F.persona(
            c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, tipo, fase=i, anda=0.0, dirx=dx, cae=cae,
            aura=inf, sem=i, brazos=(0.5 + 0.2 * math.sin(t * 2 + i), 1.2 + 0.3 * math.sin(t * 3 + i)) if i % 2 else None)))
    # el cazador y su lobo
    entra = smooth(pr(t, A.z_alguien - 0.9, A.z_detalle))   # «alguien»: el cazador y su lobo entran por la izquierda
    anda = 1.0 if 0.0 < entra < 1.0 else 0.0
    cxz = (lerp(-900, CAZADOR[0], entra), CAZADOR[1])
    lxz = (lerp(-760, LOBO[0], entra), LOBO[1])
    alza = smooth(pr(t, A.m_cazadores - 0.2, A.m_guardaban))
    if t > A.z_alguien - 0.9:
        objs.append((cxz[0], 0, cxz[1], lambda c: F.persona(c, *cam.pt(cxz[0], 0, cxz[1])[:2], 0.95 * cam.k(cam.pt(cxz[0], 0, cxz[1])[2]),
                                                            t, "cazador", fase=0.3, anda=anda, dirx=1, sem=21,
                                                            brazos=(0.3, 0.2 + 1.9 * alza) if alza > 0 else None)))
    se_va = smooth(pr(t, A.m_guardaban, A.m_pelea + 0.2))
    if se_va < 0.99 and t > A.z_alguien - 0.9:
        ojo = smooth(pr(t, A.z_mascotas - 0.2, A.z_mascotas + 0.3))
        objs.append((lxz[0], 0, lxz[1], lambda c: F.lobo(c, *cam.pt(lxz[0], 0, lxz[1])[:2], 0.95 * cam.k(cam.pt(lxz[0], 0, lxz[1])[2]),
                                                         t, dirx=1, anda=anda, ojo=ojo, grune=ojo, op=1 - se_va, aura=0.6 * ojo)))
    C.figuras(g, cam, objs)
    # el contagio: arcos de sangre que saltan de cabeza en cabeza
    for i in range(len(raid) - 1):
        u = pr(t, t_salto[i] - 0.25, t_salto[i + 1])
        if 0 < u < 1 or (u >= 1 and t < A.z_alguien):
            a = cam.pt(*_cabeza(raid[i][0], raid[i][1]))
            b = cam.pt(*_cabeza(raid[i + 1][0], raid[i + 1][1]))
            k = cam.k(a[2])
            arco = [(lerp(a[0], b[0], v), lerp(a[1], b[1], v) - 140 * k * math.sin(math.pi * v)) for v in np.linspace(0, 1, 14)]
            hasta = max(2, int(14 * min(1.0, u)))
            op = 1.0 if u < 1 else 0.35
            g.trazo(np.float32(arco[:hasta]), 4.0 * k ** 0.5, color=SANGRE, op=op, afilado=0.5)
            if u < 1:
                g.acento_luz(*arco[hasta - 1], 60 * k, SANGRE, 0.9)
    # «le drenaba la vida»: hilos de sangre que suben de los contagiados hacia Hakkar
    dr = C.env(t, A.z_drenaba - 0.1, A.z_segundos, 0.4, 0.8)
    if dr > 0.01:
        b = cam.pt(hx, hy - 650, hz)
        for (X, Z, dx, i) in raid:
            a = cam.pt(*_cabeza(X, Z))
            for j in range(5):
                v = ((t * 0.7 + j / 5 + i * 0.13) % 1.0)
                x_ = lerp(a[0], b[0], v) + 30 * math.sin(v * 9 + i)
                y_ = lerp(a[1], b[1], v ** 0.8)
                g.circ(x_, y_, 3 + 3 * (1 - v), SANGRE, dr * (1 - v))
    # el recuerdo: el tráiler real de Blizzard colgado del muro izquierdo
    op = C.env(t, A.z_fondo + 0.3, A.z_enfermedad - 0.2, 0.5, 0.5)
    C.recuerdo_colgado(g, cam, (-470, -470 + 10 * math.sin(t * 0.8), 1400), (0.9, 0, 0.44), "_crudos/F2CaYDCCI64",
                       32.3 + (t - A.z_fondo) * 0.45, t, ancho=520, alto=292, texto="Hakkar · Dios de la Sangre", op=op,
                       z=1.15, cx=0.5, cy=0.45, tinta=0.22, sem=2)
    if op > 0.01:
        for sg in (-1, 1):
            G3.trazo3d(g, cam, [(-470 + sg * 230 * 0.9, TECHO, 1400 + sg * 230 * 0.44),
                                (-470 + sg * 230 * 0.9, -700, 1400 + sg * 230 * 0.44)], 3.0, afilado=0.0, op=op)
    # «Sangre Corrupta»: cartela colgada sobre el círculo y gotas que llueven del techo
    op = C.env(t, A.z_sangre - 0.15, A.z_enfermedad + 1.2, 0.3, 0.5)
    C.cartela_colgada(g, cam, (0, -500 + 8 * math.sin(t), 1450), "Sangre Corrupta", t, ancho=700, alto=140, px=52, op=op,
                      techo=TECHO, color=SANGRE)
    gotas = C.env(t, A.z_sangre - 0.1, A.z_otro, 0.2, 1.0)
    if gotas > 0.01:
        for i in range(36):
            X = (rnd(i, 61) - 0.5) * 1300
            Z = 900 + 1500 * rnd(i, 62)
            Y = TECHO + ((t * 700 + 1000 * rnd(i, 63)) % 950)
            p0, p1 = cam.pt(X, Y, Z), cam.pt(X, Y + 40, Z)
            g.trazo([p0[:2], p1[:2]], 3.2 * cam.k(p0[2]) ** 0.5, color=SANGRE, op=gotas, afilado=0.7)
    # el reloj de arena: «solo debía durar unos segundos»
    op = C.env(t, A.z_durar - 0.5, A.z_dentro, 0.4, 0.5)
    if op > 0.01:
        X, Z = RELOJ
        G3.plano(g, cam, (X - 80, -70, Z - 80), (1, 0, 0), (0, 1, 0), 160, 70, 0.45, familias=((0.0, 8.0),), contorno=2.0)
        G3.plano(g, cam, (X - 80, -70, Z - 80), (1, 0, 0), (0, 0, 1), 160, 160, 0.7, familias=((0.0, 7.0),))
        lz = F.reloj_arena(t, pr(t, A.z_durar - 0.2, A.z_dentro - 0.2))
        q = G3.quad_mundo(cam, (X, -70 - 125, Z), (1, 0, 0), (0, 1, 0), 170, 250)
        if q is not None:
            G3.estampar(g, lz, q, sombra=0.4, off=(10, 10), op=op)
    # la jaula del cazador: la mascota guardada con la enfermedad dentro
    if t > A.m_cazadores - 0.3:
        mano = cam.pt(cxz[0] + 40, -330 - 90 * alza, cxz[1] - 10)
        k = cam.k(mano[2])
        sang = smooth(pr(t, A.m_pelea, A.m_pelea + 0.6)) * (0.6 + 0.4 * smooth(pr(t, A.m_enfermedad - 0.2,
                                                                                    A.m_enfermedad + 0.4)))
        F.jaula(g, mano[0], mano[1], 0.9 * k, t, sangre=sang)
        if 0.0 < se_va < 1.0:                            # el lobo se deshace en un remolino de tinta hacia la jaula
            lo = cam.pt(lxz[0], -110, lxz[1])
            for j in range(10):
                v = (se_va * 1.6 - j * 0.06)
                if 0 < v < 1:
                    ang = v * 7 + j
                    rr = (1 - v) * 120 * cam.k(lo[2])
                    x_ = lerp(lo[0], mano[0], v) + rr * math.cos(ang)
                    y_ = lerp(lo[1], mano[1] + 60 * k, v) + rr * math.sin(ang) * 0.5
                    g.trazo([(x_, y_), (x_ + 30 * math.cos(ang + 1.4), y_ + 30 * math.sin(ang + 1.4))], 3, op=1 - v * 0.5)
                    g.circ(x_, y_, 3, SANGRE, 0.8 * (1 - v))
        if sang > 0.01:
            luces.append((mano[0], mano[1] + 80 * k, 260 * k, 0.6 * sang, SANGRE))
    sx, sy, _ = cam.pt(hx, hy - 650, hz)
    G3.iluminar(g, luces + [(sx, sy, 600 * cam.k(zc), 0.5 + 0.4 * ojos, SANGRE)], amb=0.12, fuerza=0.62, acento=0.22)
    G3.particulas(g, t, "polvo", 50, (0, 200, 1920, 1080), sem=13)
    G3.particulas(g, t, "ceniza", 25, (0, 0, 1920, 1080), sem=14, op=0.6)
    return g


def camara_final(t):
    """2:51-2:58: de vuelta en la cámara, a oscuras. «Hakkar nunca salió de su templo. No le hizo falta.»"""
    cam = C.camara(t, KF_FINAL, CAM_H)
    g = G(t)
    hx, hy, hz = HAKKAR
    apaga = 1 - 0.8 * smooth(pr(t, A.T_APAGON - 0.3, A.T_APAGON + 0.3))
    luces3 = [(sg * 520, -300, z_, 700, 0.55 * apaga) for sg in (-1, 1) for z_ in (1000, 2000)] + [(0, -400, 2500, 900, 0.7)]
    _sala(g, cam, t, luces3, oscuro_extra=0.15)
    _anillo(g, cam, t, 0.3)
    objs = []
    luces = []
    px, py, zc = cam.pt(hx, hy, hz)
    abre = smooth(pr(t, A.h_falta - 0.2, A.h_falta + 0.6))
    objs.append((hx, hy, hz, lambda c: F.hakkar(c, px, py, 0.8 * cam.k(zc), t, ojos=0.6 + 0.4 * abre, boca=0.25 * abre)))
    for sg in (-1, 1):
        for Z in (800.0, 1500.0, 2150.0):
            objs.append((sg * 640, -400, Z, lambda c, X=sg * 640, Z=Z: L._columna(c, cam, X, Z, luces3)))
        for j, Z in enumerate((1000.0, 2000.0)):
            def br(c, X=sg * 520, Z=Z, j=j):
                r = _brasero(c, cam, X, Z, t, 0.55 * apaga, int(X) + j)
                if r:
                    luces.append(r)
            objs.append((sg * 520, -100, Z, br))
    for i in range(14):                                    # lo que dejó la noche: huesos y cráneos en el círculo
        X = ANILLO[0] + (rnd(i, 71) - 0.5) * 800
        Z = ANILLO[1] + (rnd(i, 72) - 0.5) * 700
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: _huesos(c, cam, X, Z, t, i)))
    C.figuras(g, cam, objs)
    sx, sy, _ = cam.pt(hx, hy - 650, hz)
    G3.iluminar(g, luces + [(sx, sy, 500 * cam.k(zc), 0.4 + 0.4 * abre, SANGRE)], amb=0.08, fuerza=0.7, acento=0.25)
    G3.particulas(g, t, "ceniza", 30, (0, 0, 1920, 1080), sem=15, op=0.6)
    return g


def _huesos(c, cam, X, Z, t, i):
    a_ = rnd(i, 87) * 3.1416
    p0 = cam.pt(X - 45 * math.cos(a_), -8, Z - 45 * math.sin(a_))
    p1 = cam.pt(X + 45 * math.cos(a_), -8, Z + 45 * math.sin(a_))
    G3.sombra_contacto(c, cam, X, Z, 50, 22, op=0.6)
    GR._hueso(c, p0[:2], p1[:2], 10 * cam.k(p0[2]))
    if i % 2 == 0:
        px, py, zc = cam.pt(X + 60, 0, Z - 30)
        GR.craneo(c, px, py - 20 * cam.k(zc), 21 * cam.k(zc), t, ang=0.5 * (rnd(i, 85) - 0.5), mand=0.3 * rnd(i, 86))


def susto(t):
    """EL SUSTO (2:56): la cara de Hakkar, en rojo sangre, llena el cuadro de golpe y se te echa encima."""
    g = G(t)
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.95, ang=10, per=5.0)
    u = t - A.T_SUSTO
    s = 2.15 + 0.9 * e_out(min(1.0, u / 0.6))
    F.cara_hakkar(g, 960, 610 + 40 * u, s, t, ojos=1.0, boca=1.0)
    G3.particulas(g, t, "brasas", 40, (0, 0, 1920, 1080), sem=16, color=SANGRE)
    return g
