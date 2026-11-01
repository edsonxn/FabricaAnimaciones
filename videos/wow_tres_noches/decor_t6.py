# -*- coding: utf-8 -*-
"""Decorados del tramo 6 de «Tres noches» (2:58-5:50, 15-oct-2026), estilo «grabado de peste» en espacio 3D:
  estudio   el gabinete de los médicos de la peste (cdc): por la ventana arde la aldea (el reinicio), la carta del CDC,
            The Lancet, el recuerdo real de Orgrimmar 2005, el globo del mundo real y el mapa de Azeroth
  muelle    Bahía del Botín de noche (cajas, reloj): calabazas de Hallow's End, cajas sospechosas, el reloj de arena, el primer
            necrófago, el mapa con las cajas en las capitales
  calle     una calle de Ventormenta (caen): vendedor, subastador, maestro de vuelo y guardia mordidos a su palabra;
            carteles tachados; recuerdo real de Ventormenta invadida (2008)
  villa     Villadorada y El Cruce: los vivos huyen al campo y los muertos ya esperan
  torre     la torre de los magos (portal): la danza de los que querían ser zombis, la horda que cruza, la emboscada en la
            llegada; cruzas el portal...
  susto2    EL SUSTO de 5:50: el necrófago pegado a la cámara
Pegatinas reales (wow_png): Archmage Malin, Brother Paxton, Booty Bay Bruiser, Kul Tiras Sailor, Flesh Eater, Ghoul Ravener,
Plague Spreader, Rotted One, Auctioneer Jaxon, Dungar Longdrink, Stormwind City Guard, Innkeeper Farley, Marshal Dughan."""
import math

import numpy as np

import anclas as A
import comun as C
import fig as F
import fig2 as F2
import grabado as GR
import grabado_3d as G3
from grabado import ESPECTRO, HIELO, ORO, PLAGA, SANGRE, TINTA, G, circ_pts, e_out, lerp, pr, rnd, smooth


def _k(cam, X, Y, Z):
    px, py, zc = cam.pt(X, Y, Z)
    return px, py, cam.k(zc)


def _cartel(g, cam, centro, texto, t, op=1.0, tacha=0.0, ancho=520, alto=130, techo=None, U=(1, 0, 0), px=46, giro=0.0):
    """Cartela colgada con cadenas y, con `tacha` 0..1, una X de sangre que la tacha (lo que ya no se puede hacer)."""
    if op <= 0.01:
        return
    s = G(t, int(ancho * 1.25), int(alto * 1.3), alfa=True)
    GR.cartela(s, s.W / 2, s.H / 2, ancho, texto, t, px=px)
    if tacha > 0.01:
        for (a, b) in (((0.18, 0.2), (0.82, 0.8)), ((0.82, 0.2), (0.18, 0.8))):
            u = min(1.0, tacha * 2) if a[0] < 0.5 else max(0.0, tacha * 2 - 1)
            if u <= 0:
                continue
            p0 = (a[0] * s.W, a[1] * s.H)
            p1 = (lerp(a[0], b[0], u) * s.W, lerp(a[1], b[1], u) * s.H)
            s.trazo([p0, p1], 16, color=SANGRE, op=0.95, afilado=0.4)
    X, Y, Z = centro
    if techo is not None:
        for sg in (-1, 1):
            G3.trazo3d(g, cam, [(X + sg * ancho * 0.38 * U[0], techo, Z + sg * ancho * 0.38 * U[2]),
                                (X + sg * ancho * 0.38 * U[0], Y - alto * 0.45, Z + sg * ancho * 0.38 * U[2])], 3.0,
                         afilado=0.0, op=op)
    q = G3.quad_mundo(cam, centro, U, (0, 1, 0), ancho * 1.25, alto * 1.3, giro)
    if q is not None:
        G3.estampar(g, s, q, sombra=0.3, off=(8, 12), op=op)


def _colgar(g, cam, lienzo, centro, ancho, t, op=1.0, techo=None, U=(1, 0, 0), giro=0.0, sombra=0.45):
    """Cuelga un lienzo (carta, revista, reloj, mapa) en el aire con cadenas hasta `techo`."""
    if op <= 0.01:
        return
    alto = ancho * lienzo.H / lienzo.W
    X, Y, Z = centro
    if techo is not None:
        for sg in (-1, 1):
            G3.trazo3d(g, cam, [(X + sg * ancho * 0.35 * U[0], techo, Z + sg * ancho * 0.35 * U[2]),
                                (X + sg * ancho * 0.35 * U[0], Y - alto * 0.48, Z + sg * ancho * 0.35 * U[2])], 3.0,
                         afilado=0.0, op=op)
    q = G3.quad_mundo(cam, centro, U, (0, 1, 0), ancho, alto, giro)
    if q is not None:
        G3.estampar(g, lienzo, q, sombra=sombra, off=(12, 18), op=op)


# ====================================================================== 1. EL GABINETE (cdc)
CAM_E = dict(x=0.0, y=-620.0, z=520.0, guinada=0.0, cabeceo=3.0, f=1450.0, foco=1700.0, apertura=5.0, bruma=0.3,
             lejos=2600.0)
KF_ESTUDIO = [(A.TR_ESTUDIO - 0.4, dict(x=0.0, y=-610.0, z=560.0, guinada=0.0, cabeceo=1.0, foco=1800.0)),
              (A.d_quema, dict(x=-15.0, y=-615.0, z=530.0, guinada=-1.0, cabeceo=2.0, foco=1800.0)),
              (A.d_historia + 0.5, dict(x=-20.0, y=-640.0, z=460.0, guinada=-2.0, cabeceo=10.0, foco=950.0)),
              (A.d_escribieron, dict(x=-60.0, y=-650.0, z=430.0, guinada=-11.0, cabeceo=8.0, foco=720.0)),
              (A.d_2007, dict(x=0.0, y=-650.0, z=420.0, guinada=0.0, cabeceo=11.0, foco=980.0)),
              (A.d_lancet, dict(x=50.0, y=-650.0, z=420.0, guinada=11.0, cabeceo=8.0, foco=720.0)),
              (A.d_modelo, dict(x=0.0, y=-660.0, z=400.0, guinada=0.0, cabeceo=5.0, foco=1350.0)),
              (A.d_quince, dict(x=60.0, y=-700.0, z=520.0, guinada=7.0, cabeceo=24.0, foco=900.0)),
              (A.d_azeroth, dict(x=-40.0, y=-960.0, z=820.0, guinada=0.0, cabeceo=52.0, foco=820.0)),
              (A.TR_MUELLE + 0.6, dict(x=-50.0, y=-990.0, z=860.0, guinada=0.0, cabeceo=55.0, foco=800.0))]
VENT = (-380.0, 380.0, -950.0, -260.0)       # ventana del muro del fondo (x0, x1, y0, y1)
Z_FONDO = 2200.0
MESA = (-470.0, 470.0, 1250.0, 1550.0, -280.0)
MEDICOS = ((-430.0, 1380.0), (430.0, 1380.0))
VELAS = [(-330.0, 1300.0), (-120.0, 1520.0), (200.0, 1290.0), (390.0, 1500.0)]


def _vista_ventana(g, cam, t):
    """Lo que se ve por la ventana: cielo, luna y la aldea en la colina; a «reinició» se apagan sus ventanas y a «quema»
    arde entera (Blizzard reinicia los servidores: quemar la aldea para detener la peste)."""
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 60, tono_alto=0.95, tono_bajo=0.55, estrellas=40)
    ox = cam.pt(0, 0, 9000)[0] - 960
    GR.luna(g, 1260 + ox, hz - 330, 52, t, tono_cielo=0.85)
    GR.nube(g, 700 + ox * 0.8, hz - 300, 420, t, sem=31, vel=5, tono=0.3)
    perf = GR.perfil_colina(-100 + ox, 2020 + ox, hz + 30, 60, sem=33, n=16)
    GR.colina(g, perf, tono=0.42, tono2=0.75, ang=-6, per=5.2, contorno=1.8)
    quema = smooth(pr(t, A.d_quema - 0.2, A.d_peste + 0.6))
    apaga = smooth(pr(t, A.d_reinicio, A.d_servidores + 0.3))
    if quema > 0.02:                                        # el resplandor del incendio detrás de la aldea
        g.acento_luz(980 + ox, hz - 60, 760 * quema, SANGRE, 0.8 * quema)
    casas = []
    x = 600 + ox
    for i in range(7):                                      # la aldea en la cresta: casas anchas de tejado a dos aguas
        w = 95 + 40 * rnd(i, 4)
        h = 55 + 30 * rnd(i, 5)
        y = hz + 40 - 26 * math.sin(i * 0.8 + 0.4)
        cx = x + w / 2
        if i == 3:                                          # el campanario de la aldea
            g.macizo(np.float32([(cx - 26, y), (cx + 26, y), (cx + 26, y - 170), (cx, y - 230), (cx - 26, y - 170)]), 0.92)
        g.macizo(np.float32([(x, y), (x + w, y), (x + w, y - h), (cx + w * 0.1, y - h - 48), (x + w * 0.12, y - h - 40),
                             (x, y - h)]), 0.9)
        casas.append((x, w, y, h))
        if apaga < 0.99 and quema < 0.05:
            for dx in (0.3, 0.7):
                g.papel(np.float32([(x + w * dx - 6, y - h * 0.65), (x + w * dx + 6, y - h * 0.65), (x + w * dx + 6, y - h * 0.35),
                                    (x + w * dx - 6, y - h * 0.35)]), 0.9 * (1 - apaga))
                g.acento_luz(x + w * dx, y - h * 0.5, 26, ORO, 0.6 * (1 - apaga))
        x += w + 14 + 30 * rnd(i, 6)
    if quema > 0.02:
        for i, (x, w, y, h) in enumerate(casas):            # cada casa arde a lo largo del tejado, con su columna de humo
            if rnd(i, 7) > 0.3 + 0.7 * quema:
                continue
            for j in range(2):
                GR.llama(g, x + w * (0.25 + 0.5 * j + 0.1 * rnd(i, 20 + j)), y - h - 30 * rnd(i, 30 + j),
                         (0.5 + 0.7 * quema) * (0.6 + 0.8 * rnd(i, 8 + j)), t, sem=i * 3 + j, color=SANGRE if (i + j) % 2 else ORO)
            G3.humo(g, x + w / 2, y - h - 60, 1.0, t, sem=i, op=0.5 * quema, alto=380, hebras=2)
        G3.particulas(g, t, "brasas", 40, (casas[0][0], hz - 420, casas[-1][0] + 120, hz), sem=6, color=SANGRE, op=quema)


def estudio(t):
    cam = C.camara(t, KF_ESTUDIO, CAM_E)
    g = G(t)
    _vista_ventana(g, cam, t)
    x0, x1, y0, y1 = VENT
    lv = [(0.0, -600.0, Z_FONDO - 100, 1600.0, 0.55)]
    fz = 0.35 + 0.5 * smooth(pr(t, A.d_quema, A.d_peste))
    luces = lv + [(X, -360.0, Z, 700.0, 0.5) for X, Z in VELAS]
    pared = dict(familias=((0.0, 15.0),), patron=("sillares", 230, 105), quiebre=0.0, var=0.06, luces=luces, oscuro=0.3, contorno=0.0)
    G3.plano(g, cam, (-1100, -1500, Z_FONDO), (1, 0, 0), (0, 1, 0), 1100 + x0, 1500, 0.3, **pared)       # muro del fondo
    G3.plano(g, cam, (x1, -1500, Z_FONDO), (1, 0, 0), (0, 1, 0), 1100 - x1, 1500, 0.3, **pared)
    G3.plano(g, cam, (x0, -1500, Z_FONDO), (1, 0, 0), (0, 1, 0), x1 - x0, 1500 + y0, 0.3, **pared)
    G3.plano(g, cam, (x0, y1, Z_FONDO), (1, 0, 0), (0, 1, 0), x1 - x0, -y1, 0.3, **pared)
    for sg in (-1, 1):                                      # muros laterales con anaqueles de libros
        X = sg * 1100
        G3.plano(g, cam, (X, -1500, 0), (0, 0, 1), (0, 1, 0), Z_FONDO, 1500, 0.36, **pared)
        for j, yy in enumerate((-1150, -900, -650)):
            G3.plano(g, cam, (X - sg * 5, yy, 700), (0, 0, 1), (0, 1, 0), 1300, 210,
                     lambda a, b, zc, j=j: 0.35 + 0.35 * (0.5 + 0.5 * np.sin(a / 23.0 + j * 7) * np.sin(a / 57.0 + j)),
                     familias=((90.0, 16.0),), quiebre=0.15, luces=luces, oscuro=0.3, contorno=1.6)
            G3.trazo3d(g, cam, [(X - sg * 30, yy + 214, 700), (X - sg * 30, yy + 214, 2000)], 9, afilado=0.0)
    G3.plano(g, cam, (-1100, 0, 0), (1, 0, 0), (0, 0, 1), 2200, Z_FONDO, 0.5, familias=((0.0, 18.0),), patron=("losas", 160),
             luces=luces, oscuro=0.3)
    for i in range(5):                                      # vigas del techo
        G3.trazo3d(g, cam, [(-1100, -1480, 400 + 420 * i), (1100, -1480, 400 + 420 * i)], 30, afilado=0.0)
    # parteluz y alféizar de la ventana; resplandor del fuego que entra
    G3.trazo3d(g, cam, [(0, y0, Z_FONDO - 4), (0, y1, Z_FONDO - 4)], 22, afilado=0.0)
    G3.trazo3d(g, cam, [(x0, (y0 + y1) / 2, Z_FONDO - 4), (x1, (y0 + y1) / 2, Z_FONDO - 4)], 16, afilado=0.0)
    G3.plano(g, cam, (x0 - 40, y1, Z_FONDO - 120), (1, 0, 0), (0, 0, 1), x1 - x0 + 80, 120, 0.4, familias=((0.0, 10.0),),
             contorno=2.0)
    wx, wy, _ = cam.pt(0, (y0 + y1) / 2, Z_FONDO)
    G3.haz(g, wx, wy, 100, 34, 900, t, op=0.2 * fz)
    # la mesa
    mx0, mx1, mz0, mz1, my = MESA
    G3.plano(g, cam, (mx0, my, mz0), (1, 0, 0), (0, 0, 1), mx1 - mx0, mz1 - mz0, 0.25, familias=((0.0, 14.0),), luces=luces,
             oscuro=0.25, contorno=2.4)
    G3.plano(g, cam, (mx0, my, mz0), (1, 0, 0), (0, 1, 0), mx1 - mx0, 70, 0.6, familias=((0.0, 8.0),), contorno=2.2)
    for X in (mx0 + 30, mx1 - 30):
        G3.trazo3d(g, cam, [(X, my + 70, mz0 + 20), (X, 0, mz0 + 20)], 22, afilado=0.0)
    contagio = max(0.25 * smooth(pr(t, A.d_modelo, A.d_epidemia)), smooth(pr(t, A.d_azeroth - 0.4, A.d_ensayado + 0.4)))
    mapa = F2.mapa_azeroth(t, contagio=contagio, foco="Forjaz")
    q = G3.quad_mundo(cam, (-60.0, my - 2, 1405.0), (1, 0, 0), (0, 0, -1), 560, 373)
    if q is not None:
        G3.estampar(g, mapa, q, sombra=0.0)
    objs = []
    for i, (X, Z) in enumerate(VELAS):                      # velas encendidas sobre la mesa
        objs.append((X, my, Z, lambda c, X=X, Z=Z, i=i: F2.vela(c, *cam.pt(X, my, Z)[:2], 1.6 * cam.k(cam.pt(X, my, Z)[2]), t,
                                                                 sem=i)))
    objs.append((-200, my, 1500, lambda c: GR.craneo(c, *cam.pt(-200, my - 45, 1500)[:2], 45 * cam.k(cam.pt(-200, my, 1500)[2]),
                                                     t, tono=0.1)))
    gl = smooth(pr(t, A.d_mundo - 0.6, A.d_mundo))
    if gl > 0.01:                                           # el globo del mundo real
        def globo(c):
            px, py, zc = cam.pt(230, my - 130, 1330)
            F2.globo(c, px, py, 95 * cam.k(zc), t, rojo=smooth(pr(t, A.d_cuarentenas - 0.2, A.d_cuarentenas + 0.6)))
        objs.append((230, my, 1330, globo))
    gira = smooth(pr(t, A.d_dos - 0.3, A.d_dos + 0.5))
    for j, (X, Z) in enumerate(MEDICOS):                    # los dos médicos de la peste (los epidemiólogos)
        op = smooth(pr(t, A.d_historia, A.d_2007))
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, j=j, op=op: F.persona(
            c, *cam.pt(X, 0, Z)[:2], 1.0 * cam.k(cam.pt(X, 0, Z)[2]), t, "medico", anda=0.0, dirx=1 if j == 0 else -1,
            op=op, sem=200 + j, brazos=(0.2, 0.3 + 1.5 * gira * (j == 1) + 1.1 * gira * (j == 0)))))
    C.peg(objs, cam, t, "Archmage Malin", -800.0, 1750.0, 370.0, sem=210, espejo=True)
    C.peg(objs, cam, t, "Brother Paxton", 820.0, 1820.0, 365.0, sem=211)
    for i in range(4):                                      # frascos y cráneos en los anaqueles
        sg = -1 if i % 2 else 1
        X, Z, Y = sg * 1040, 900 + 300 * i, -650 - 250 * (i % 3)
        objs.append((X, Y, Z, lambda c, X=X, Y=Y, Z=Z, i=i: GR.craneo(c, *cam.pt(X, Y - 30, Z)[:2], 32 * cam.k(cam.pt(X, Y, Z)[2]),
                                                                      t, tono=0.2)))
    C.figuras(g, cam, objs)
    # la carta del CDC baja del techo; la revista; el recuerdo real (Orgrimmar, 2005)
    op = C.env(t, A.d_centros - 0.4, A.d_lancet + 0.4, 0.5, 0.6)
    if op > 0.01:
        u = e_out(pr(t, A.d_centros - 0.4, A.d_escribieron + 0.6))
        car = F2.carta(t, escribe=pr(t, A.d_escribieron - 0.4, A.d_datos + 0.3))
        _colgar(g, cam, car, (-330.0, lerp(-1100, -480, u) + 6 * math.sin(t * 1.3), 1200.0), 240, t, op=op, techo=-1480,
                U=(0.92, 0, 0.38), giro=3 * math.sin(t * 0.9))
    op = C.env(t, A.d_lancet - 0.5, A.d_modelo + 0.2, 0.4, 0.6)
    if op > 0.01:
        _colgar(g, cam, F2.revista(t), (380.0, -640.0 + 6 * math.sin(t * 1.1), 1200.0), 260, t, op=op, techo=-1480,
                U=(0.92, 0, -0.38))
    op = C.env(t, A.d_modelo - 0.5, A.d_quince + 0.2, 0.5, 0.6)
    C.recuerdo_colgado(g, cam, (0.0, -690.0 + 8 * math.sin(t), 1750.0), (1, 0, 0), "_crudos/sAEhyHiNdrA",
                       11.0 + (t - A.d_modelo) * 0.8, t, ancho=560, alto=380, texto="Orgrimmar · MMV", op=op, z=1.45,
                       cx=0.5, cy=0.38, tinta=0.25, sem=21)
    l2 = [(*cam.pt(X, my - 70, Z)[:2], 260 * cam.k(cam.pt(X, my, Z)[2]), 0.55) for X, Z in VELAS]
    l2.append((wx, wy, 900, 0.3 + 0.5 * fz, SANGRE if fz > 0.5 else None))
    G3.iluminar(g, [l for l in l2 if l[-1] is not None] + [l[:4] for l in l2 if l[-1] is None], amb=0.14, fuerza=0.62,
                acento=0.12)
    G3.particulas(g, t, "polvo", 60, (300, 150, 1600, 950), sem=22)
    with G3.capa_prof(g, cam, 260) as c:                    # primer plano: cortina de terciopelo oscura (enmarca)
        o = 14 * math.sin(t * 0.7)
        c.figura(np.float32([(-40, -40), (150 + o, -40), (190 + o, 300), (150 + o, 700), (210 + o, 1120), (-40, 1120)]), 0.86,
                 contorno=2.6, ang=88, per=5.5, tono2=0.95, luz=0)
        for xx in (40, 100):
            c.trazo(np.float32([(xx + o * 0.5, -40), (xx + 20 + o, 500), (xx + 40 + o, 1120)]), 2.0, color=c.fondo_papel,
                    op=0.35)
    return g


# ====================================================================== 2. BAHÍA DEL BOTÍN (cajas, reloj)
CAM_M = dict(x=0.0, y=-300.0, z=0.0, guinada=0.0, cabeceo=-2.0, f=1450.0, foco=1400.0, apertura=3.5, bruma=0.42,
             lejos=3400.0)
KF_MUELLE = [(A.TR_MUELLE - 0.6, dict(x=0.0, y=-300.0, z=-120.0, guinada=0.0, cabeceo=-2.0, foco=1500.0)),
             (A.k_octubre, dict(x=-40.0, y=-310.0, z=40.0, guinada=-2.0, cabeceo=-5.0, foco=1750.0)),
             (A.k_rey + 0.3, dict(x=-40.0, y=-320.0, z=110.0, guinada=9.0, cabeceo=-9.0, foco=3500.0)),
             (A.k_halloween, dict(x=0.0, y=-300.0, z=190.0, guinada=0.0, cabeceo=-1.0, foco=1300.0)),
             (A.k_aparecieron, dict(x=20.0, y=-300.0, z=290.0, guinada=0.0, cabeceo=2.0, foco=1150.0)),
             (A.k_abrieron, dict(x=0.0, y=-300.0, z=400.0, guinada=-3.0, cabeceo=4.0, foco=700.0)),
             (A.r_cuenta, dict(x=0.0, y=-320.0, z=460.0, guinada=0.0, cabeceo=-7.0, foco=1050.0)),
             (A.r_cero, dict(x=-30.0, y=-300.0, z=500.0, guinada=-4.0, cabeceo=3.0, foco=560.0)),
             (A.r_mordia, dict(x=10.0, y=-300.0, z=540.0, guinada=3.0, cabeceo=3.0, foco=700.0)),
             (A.r_capitales, dict(x=-20.0, y=-330.0, z=580.0, guinada=-6.0, cabeceo=-6.0, foco=900.0)),
             (A.TR_CALLE + 0.6, dict(x=0.0, y=-350.0, z=720.0, guinada=0.0, cabeceo=-8.0, foco=800.0))]
CAJAS = [(-190.0, 1850.0), (170.0, 1950.0), (-40.0, 2250.0), (260.0, 2450.0), (-280.0, 2600.0), (90.0, 2800.0)]
ABREN = [(-90.0, 1810.0, "capa"), (270.0, 1910.0, "enano"), (60.0, 2200.0, "guerrero")]
CALABAZAS = [(-430.0, 900.0), (430.0, 1150.0), (-430.0, 1500.0), (430.0, 1800.0), (-430.0, 2150.0), (430.0, 2450.0),
             (-430.0, 2800.0), (430.0, 3150.0)]
RELOJ = (0.0, -600.0, 2500.0)
FAROLES_M = ((-470, 1200), (470, 1900), (-470, 2600), (470, 3300))


def _rey(t):
    return C.env(t, A.k_rey - 0.4, A.k_muelles, 0.6, 1.0) + 0.6 * C.env(t, A.r_plaga - 0.2, A.r_mordia, 0.2, 0.4)


def _firma_bahia(t):
    cam = C.camara(t, KF_MUELLE, CAM_M)
    return cam.horizonte(), cam.pt(0, 0, 9000)[0], 100 * _rey(t)


def _bahia(g, cam, t):
    """Fondo: el anillo de acantilados de Bahía del Botín con sus casas sobre pilotes y faroles, y un galeón."""
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 30, tono_alto=0.95, tono_bajo=0.5, estrellas=46)
    ox = cam.pt(0, 0, 9000)[0] - 960
    GR.luna(g, 420 + ox, hz - 360, 60, t, tono_cielo=0.86)
    G3.haz(g, 420 + ox, hz - 360, 80, 12, 700, t, op=0.12)
    GR.nube(g, 1300 + ox * 0.8, hz - 330, 520, t, sem=41, vel=6)
    rey = _rey(t)
    if rey > 0.01:
        F2.corona_lich(g, 1350 + ox * 0.8, hz - 300, 0.95, t, op=min(1.0, rey))
    for sg, x_a, x_b in ((-1, -200, 760), (1, 1160, 2120)):
        perf = GR.perfil_colina(x_a + ox, x_b + ox, hz - 170, 150, sem=44 + sg, n=14, ondas=1.6)
        GR.colina(g, perf, tono=0.5, tono2=0.82, ang=80 * sg, per=5.2, contorno=2.0)
        for i in range(7):                                  # casas de madera sobre pilotes en la ladera
            u = (i + 0.5) / 7
            x = lerp(x_a + 60, x_b - 60, u) + ox
            y = hz - 60 - 110 * math.sin(u * math.pi) * (0.6 + 0.4 * rnd(i, sg + 5))
            w, h = 50 + 20 * rnd(i, 7), 36 + 14 * rnd(i, 8)
            for xx in (x - w * 0.35, x + w * 0.35):
                g.trazo([(xx, y), (xx, y + 40)], 3, afilado=0.0)
            g.figura(np.float32([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h), (x, y - h - 22), (x - w / 2, y - h)]),
                     0.75, contorno=1.6, ang=90, per=4.0, cruz=False)
            g.papel(circ_pts(x, y - h * 0.5, 5, 8), 0.95)
            g.acento_luz(x, y - h * 0.5, 30, ORO, 0.75)


def _galeon(g, cam):
    """El galeón anclado en la bahía (se dibuja DESPUÉS del mar: si no, el agua lo tapa y las velas flotan)."""
    casco = [(1050, -60, 3300), (1700, -60, 3500), (1640, 40, 3500), (1110, 40, 3300)]
    scr, _ = G3.proyectar(cam, casco)
    if scr is not None:
        g.figura(scr, 0.85, contorno=2.4, ang=0, per=4.6, cruz=False)
    for j, (X, Z, hh) in enumerate(((1200, 3350, 700), (1400, 3420, 820), (1580, 3480, 600))):
        G3.trazo3d(g, cam, [(X, -60, Z), (X, -60 - hh, Z)], 10, afilado=0.0)
        vela = [(X - 120, -60 - hh * 0.9, Z), (X + 130, -60 - hh * 0.88, Z), (X + 175, -60 - hh * 0.65, Z),
                (X + 150, -60 - hh * 0.4, Z), (X - 110, -60 - hh * 0.42, Z), (X - 80, -60 - hh * 0.66, Z)]
        scr, _ = G3.proyectar(cam, vela)
        if scr is not None:                                 # vela hinchada y rota (barco fantasma)
            g.figura(GR.catmull(scr, 4, True), 0.32, contorno=1.8, tono2=0.7, luz=0, ang=90, per=4.4, cruz=False)
    lx, ly, _ = cam.pt(1400, -300, 3420)
    g.acento_luz(lx, ly, 60, ORO, 0.6)


def _farol_muelle(c, cam, X, Z, t, sem):
    px, py, zc = cam.pt(X, -230, Z)
    k = cam.k(zc)
    G3.trazo3d(c, cam, [(X, 40, Z), (X, -230, Z)], 12, afilado=0.0)
    GR.llama(c, px, py, 0.7 * k, t, sem=sem, color=ORO)
    return (px, py, 300 * k, 0.5)


def muelle(t):
    cam = C.camara(t, KF_MUELLE, CAM_M)
    luces = [(X, -230, Z, 520, 0.6) for X, Z in FAROLES_M]

    def cerca(g, tt):                                      # el mar, el galeón y el muelle (solo dependen de la cámara)
        cm = C.camara(tt, KF_MUELLE, CAM_M)
        G3.plano(g, cm, (-7000, 40, -600), (1, 0, 0), (0, 0, 1), 14000, 9600, 0.52, familias=((0.0, 15.0),), quiebre=0.55,
                 tramo=60, luces=[(0, 40, 3000, 2600, 0.45)], oscuro=0.2)                 # el mar (trazo quebrado: agua)
        _galeon(g, cm)
        G3.plano(g, cm, (-500, 0, -400), (1, 0, 0), (0, 0, 1), 1000, 4000, 0.42, familias=((0.0, 9.0),),
                 patron=("sillares", 260, 46), luces=luces, oscuro=0.3, contorno=2.4)       # el muelle de tablones
    # FONDO cacheado por tick de HERVOR (GR.fondo): la bahía lejana y, con la cámara quieta, mar, galeón y muelle
    g = GR.fondo(t, "muelle", [(lambda g, tt: _bahia(g, C.camara(tt, KF_MUELLE, CAM_M), tt), lambda tt: _firma_bahia(tt)),
                               (cerca, lambda tt: G3.firma_cerca(C.camara(tt, KF_MUELLE, CAM_M)))])
    objs = []
    lz = []
    for i, Z in enumerate(range(-300, 3600, 260)):         # pilotes
        for sg in (-1, 1):
            X = sg * 490
            objs.append((X, 0, Z, lambda c, X=X, Z=Z: G3.trazo3d(c, cam, [(X, 120, Z), (X, -120, Z)], 18, afilado=0.0)))
    for i, (X, Z) in enumerate(FAROLES_M):
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: lz.append(_farol_muelle(c, cam, X, Z, t, 300 + i))))
    hall = [smooth(pr(t, A.k_halloween + 0.12 * i - 0.2, A.k_halloween + 0.12 * i + 0.2)) for i in range(len(CALABAZAS))]
    for i, (X, Z) in enumerate(CALABAZAS):
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: F2.calabaza(c, cam, X, Z, t, r=46, luz=0.15 + 0.85 * hall[i], sem=i)))
    # el farol II (la segunda noche) se enciende en verde
    if t > A.k_segunda - 0.5:
        def farol2(c):
            fz = smooth(pr(t, A.k_segunda - 0.2, A.k_segunda + 0.4)) * (1 + 0.4 * smooth(pr(t, A.k_proposito, A.k_proposito + 0.5)))
            fx, fy, k = F.farol(c, cam, 260.0, 1250.0, t, PLAGA, fz, sem=301, alto=1.2)
            if fz > 0.02:
                lz.append((fx, fy, 380 * k * fz, 0.6 * fz, PLAGA))
            c.texto("II", *cam.pt(260, 0, 1250)[:2], max(12, int(30 * k)), TINTA, "gara_b", 0.9)
        objs.append((260.0, 0, 1250.0, farol2))
    # las cajas sospechosas
    sosp = smooth(pr(t, A.k_sospechosas - 0.2, A.k_sospechosas + 0.6))
    for i, (X, Z) in enumerate(CAJAS):
        t0 = A.k_aparecieron + 0.25 * i
        alza = smooth(pr(t, t0 - 0.3, t0 + 0.25))
        abre = smooth(pr(t, A.k_abrieron - 0.1 + 0.2 * i, A.k_abrieron + 0.4 + 0.2 * i)) if i < 3 else 0.0
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i, alza=alza, abre=abre: F2.caja(
            c, cam, X, Z, t, lado=130, alza=alza, abre=abre, sem=i, gas=max(0.25 * sosp, abre * (1 - pr(t, A.r_cero, A.r_cero + 2))))))
    # los que abren las cajas: se contagian a «tocaba», el reloj corre, caen a «cero» y se levantan
    for j, (X, Z, tipo) in enumerate(ABREN):
        llega = smooth(pr(t, A.k_cajas - 0.5 + 0.3 * j, A.k_abrieron - 0.2))
        if llega <= 0.01:
            continue
        Xj, Zj = lerp(X + 120 * (1 if j % 2 else -1), X, llega), lerp(Z - 500, Z, llega)
        inc = smooth(pr(t, A.k_abrieron + 0.1, A.k_abrieron + 0.6))
        aura = smooth(pr(t, A.r_tocaba - 0.2 + 0.2 * j, A.r_tocaba + 0.3 + 0.2 * j))
        if j == 2:
            aura = smooth(pr(t, A.r_mordia + 0.2, A.r_mordia + 0.5))
        cae = smooth(pr(t, A.r_cero - 0.1, A.r_morias + 0.2)) if j < 2 else smooth(pr(t, A.r_mordia + 0.4, A.r_siguiente - 0.3))
        sube = smooth(pr(t, A.r_levantabas - 0.2, A.r_necrofago + 0.3)) if j < 2 else smooth(pr(t, A.r_siguiente, A.r_capitales))
        if j == 0:                                          # el primero se levanta como necrófago REAL (pegatina)
            if sube > 0.01:
                C.peg(objs, cam, t, "Flesh Eater", Xj, Zj, 340.0, alza=sube, aura=0.8 * sube, color_aura=PLAGA, sem=320)
        elif sube > 0.01:                                   # los otros, como necrófagos dibujados
            ataca = smooth(pr(t, A.r_mordia - 0.4, A.r_mordia)) * (1 - smooth(pr(t, A.r_mordia + 0.5, A.r_mordia + 1.0))) \
                if j == 1 else 0.0
            dx = 70 * ataca
            objs.append((Xj + dx, 0, Zj, lambda c, Xj=Xj, Zj=Zj, sube=sube, ataca=ataca, dx=dx, j=j: F2.necrofago(
                c, *cam.pt(Xj + dx, 0, Zj)[:2], 0.95 * cam.k(cam.pt(Xj + dx, 0, Zj)[2]), t, fase=j, anda=0.5, ataca=ataca,
                op=sube, sem=330 + j)))
        if sube < 0.99:
            objs.append((Xj, 0, Zj, lambda c, Xj=Xj, Zj=Zj, tipo=tipo, j=j, inc=inc, aura=aura, cae=cae, llega=llega, sube=sube:
                         F.persona(c, *cam.pt(Xj, 0, Zj)[:2], 0.95 * cam.k(cam.pt(Xj, 0, Zj)[2]), t, tipo, fase=j,
                                   anda=1.0 * (1 - llega) + 0.1, dirx=1 if j % 2 else -1, aura=aura, color_aura=PLAGA,
                                   cae=cae, op=1 - sube, sem=310 + j, brazos=(0.2 + 1.1 * inc, 0.3 + 1.3 * inc))))
    C.peg(objs, cam, t, "Booty Bay Bruiser", -380.0, 1400.0, 330.0, sem=340)
    C.peg(objs, cam, t, "Kul Tiras Sailor", 400.0, 2150.0, 360.0, sem=341, espejo=True)
    C.figuras(g, cam, objs)
    # «OCTUBRE DE 2008» colgado del penol; el reloj de arena; el mapa con las cajas en las capitales
    _cartel(g, cam, (-60.0, -560.0 + 6 * math.sin(t), 2300.0), "Octubre · MMVIII", t, op=C.env(t, A.k_octubre - 0.3, A.k_muelles, 0.4, 0.6),
            techo=-1300, ancho=560)
    op = C.env(t, A.r_cuenta - 0.5, A.TR_CALLE - 0.4, 0.5, 0.4)
    if op > 0.01:
        fases = [(A.r_cuenta, A.r_cero, "10:00", 1.0), (A.r_siguiente, A.r_cinco, "10:00", 1.0), (A.r_cinco, A.r_dos, "5:00", 0.85),
                 (A.r_dos, A.r_uno, "2:00", 0.72), (A.r_uno, A.r_uno + 1.6, "1:00", 0.6)]
        frac, txt, esc = 1.0, "0:00", 1.0
        for a_, b_, tx, e_ in fases:
            if t >= a_:
                frac, txt, esc = pr(t, a_, b_), tx, e_
        if A.r_cero < t < A.r_siguiente:
            frac, txt = 1.0, "0:00"
        rel = F.reloj_arena(t, frac)
        X, Y, Z = RELOJ
        _colgar(g, cam, rel, (X, Y + 6 * math.sin(t * 1.4), Z), 250 * esc, t, op=op, techo=-1300)
        _cartel(g, cam, (X, Y + 250 * esc, Z - 4), txt, t, op=op, ancho=300, alto=110, px=58)
    op = C.env(t, A.r_capitales - 0.6, A.TR_CALLE - 0.4, 0.5, 0.4)
    if op > 0.01:
        _colgar(g, cam, F2.mapa_azeroth(t, plaga=pr(t, A.r_capitales - 0.4, A.r_cinco + 0.4), titulo=False),
                (-560.0, -520.0 + 6 * math.sin(t * 0.9), 2300.0), 480, t, op=op, techo=-1300, U=(0.9, 0, 0.44))
    op = C.env(t, A.r_mordia - 0.3, A.r_capitales - 0.2, 0.4, 0.6)
    C.recuerdo_colgado(g, cam, (580.0, -520.0 + 8 * math.sin(t), 2300.0), (0.9, 0, -0.44), "_crudos/fn5-aWcop9k",
                       74.0 + (t - A.r_mordia) * 0.8, t, ancho=500, alto=330, texto="Octubre de MMVIII", op=op, z=1.35,
                       cx=0.5, cy=0.55, tinta=0.25, sem=31)
    G3.iluminar(g, [l for l in lz if l[2] > 1] + [(*cam.pt(0, -600, 2500)[:2], 600, 0.25)], amb=0.2, fuerza=0.6,
                acento=0.12)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 2600)[1]
    GR.niebla(g, y_nb - 50, y_nb + 10, t, op=0.45, sem=42, vel=16)
    with G3.capa_prof(g, cam, 240) as c:                    # primer plano: un barril y un rollo de cuerda, fuera de foco
        px, py, zc = cam.pt(cam.C[0] + 290, 0, cam.C[2] + 300)
        k = cam.k(zc)
        c.figura(np.float32([(px - 70 * k, py), (px + 70 * k, py), (px + 80 * k, py - 120 * k), (px + 70 * k, py - 220 * k),
                             (px - 70 * k, py - 220 * k), (px - 80 * k, py - 120 * k)]), 0.45, contorno=2.6, ang=90, per=5)
        for yy in (-40, -180):
            c.trazo([(px - 76 * k, py + yy * k), (px + 76 * k, py + yy * k)], 7 * k, afilado=0.0)
    return g


# ====================================================================== 3. LA CALLE DE VENTORMENTA (caen)
CAM_C = dict(x=0.0, y=-240.0, z=0.0, guinada=0.0, cabeceo=-3.0, f=1450.0, foco=1300.0, apertura=4.0, bruma=0.45,
             lejos=3200.0)
KF_CALLE = [(A.TR_CALLE - 0.6, dict(x=0.0, y=-250.0, z=-200.0, guinada=0.0, cabeceo=-3.0, foco=1300.0)),
            (A.n_vendedores, dict(x=-40.0, y=-250.0, z=-120.0, guinada=-9.0, cabeceo=-2.0, foco=1250.0)),
            (A.n_subastadores, dict(x=0.0, y=-250.0, z=-90.0, guinada=8.0, cabeceo=-2.0, foco=1350.0)),
            (A.n_vuelo, dict(x=-20.0, y=-260.0, z=-50.0, guinada=-5.0, cabeceo=-3.0, foco=1950.0)),
            (A.n_guardias, dict(x=10.0, y=-260.0, z=-20.0, guinada=5.0, cabeceo=-3.0, foco=2100.0)),
            (A.n_ciudades, dict(x=0.0, y=-300.0, z=40.0, guinada=0.0, cabeceo=-6.0, foco=2600.0)),
            (A.n_vender, dict(x=0.0, y=-300.0, z=100.0, guinada=0.0, cabeceo=-8.0, foco=1350.0)),
            (A.n_economia, dict(x=20.0, y=-290.0, z=160.0, guinada=4.0, cabeceo=-4.0, foco=1250.0)),
            (A.TR_VILLA + 0.6, dict(x=30.0, y=-280.0, z=220.0, guinada=5.0, cabeceo=-3.0, foco=1250.0))]
# (nombre/tipo, X, Z, palabra a la que lo muerden, alto de la pegatina)
MORDIDOS = [("mercader", -380.0, 1550.0, A.n_vendedores, None), ("Auctioneer Jaxon", 360.0, 1700.0, A.n_subastadores, 365.0),
            ("Dungar Longdrink", -330.0, 2300.0, A.n_vuelo, 360.0), ("Stormwind City Guard", 330.0, 2550.0, A.n_guardias, 375.0)]
CARTELES = [("Subasta", A.n_vender, -430.0), ("Grifos", A.n_volar, 0.0), ("Componentes", A.n_escapar, 430.0)]


def _fachadas(g, cam, t, luces, apagan):
    """Las casas de entramado de Ventormenta a los dos lados: zócalo de sillares, entramado de madera arriba, ventanas
    encendidas que se apagan «una por una» (las ciudades que caen), tejados en punta."""
    for sg in (-1, 1):
        X = sg * 620
        for i in range(6):
            z0 = 500 + 520 * i
            G3.plano(g, cam, (X, -360, z0), (0, 0, 1), (0, 1, 0), 500, 360, 0.32, familias=((0.0, 16.0),),
                     patron=("sillares", 220, 100), var=0.06, luces=luces, oscuro=0.3, contorno=2.0)
            G3.plano(g, cam, (X, -900, z0), (0, 0, 1), (0, 1, 0), 500, 540, 0.1, familias=((0.0, 14.0),), luces=luces,
                     oscuro=0.25, contorno=2.4)
            for a in (0, 250, 500):                          # entramado: postes verticales y la viga del piso
                G3.trazo3d(g, cam, [(X, -360, z0 + a), (X, -900, z0 + a)], 12, afilado=0.0)
            G3.trazo3d(g, cam, [(X, -370, z0), (X, -370, z0 + 500)], 14, afilado=0.0)
            G3.trazo3d(g, cam, [(X, -900, z0 - 20), (X - sg * 60, -930, z0 - 20), (X - sg * 60, -930, z0 + 520)], 10,
                       afilado=0.0)
            for j, dz in enumerate((110, 390)):
                ven = [(X, -760, z0 + dz - 50), (X, -760, z0 + dz + 50), (X, -600, z0 + dz + 50), (X, -600, z0 + dz - 50)]
                scr, _ = G3.proyectar(cam, ven)
                if scr is None:
                    continue
                encendida = (1 - apagan[(i * 2 + j + (sg > 0)) % len(apagan)])
                g.figura(scr, 0.95 - 0.85 * encendida, contorno=2.0, ang=0, per=4, cruz=False)
                if encendida > 0.05:
                    g.acento(scr, ORO, 0.8 * encendida, sem=i * 4 + j)


def calle(t):
    cam = C.camara(t, KF_CALLE, CAM_C)
    g = G(t)
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 40, tono_alto=0.95, tono_bajo=0.52, estrellas=40)
    ox = cam.pt(0, 0, 9000)[0] - 960
    with g.grupo(960 + ox, hz + 10, 0.9):                    # la catedral y el castillo al fondo de la calle
        g.macizo([(-260, 0), (260, 0), (260, -200), (140, -200), (140, -420), (100, -520), (60, -420), (60, -260),
                  (-60, -260), (-60, -420), (-100, -520), (-140, -420), (-140, -200), (-260, -200)], 0.8)
        for x_ in (-100, 100):
            g.acento_luz(x_, -330, 40, PLAGA, 0.5 * smooth(pr(t, A.n_ciudades, A.n_una + 1)))
    GR.nube(g, 500 + ox * 0.8, hz - 320, 520, t, sem=51, vel=6, tono=0.3)
    n = 24
    apagan = [smooth(pr(t, A.n_ciudades + 0.12 * i, A.n_ciudades + 0.12 * i + 0.25)) for i in range(n)]
    luces = [(sg * 560, -650, z, 520, 0.35) for sg in (-1, 1) for z in (800, 1800, 2800)]
    G3.plano(g, cam, (-620, 0, -300), (1, 0, 0), (0, 0, 1), 1240, 4000, lambda a, b, zc: 0.45 + 0.1 * np.clip(b / 4000, 0, 1),
             familias=((0.0, 16.0),), patron=("losas", 140), luces=luces, oscuro=0.25)
    _fachadas(g, cam, t, luces, apagan)
    F.puesto(g, cam, -380.0, 1650.0, t)
    objs = []
    # los mordidos: cada uno a SU palabra (aura verde, cae) y luego se levanta (a «levantaba»)
    for i, (nom, X, Z, tm, alto) in enumerate(MORDIDOS):
        aura = smooth(pr(t, tm - 0.1, tm + 0.3))
        cae = smooth(pr(t, tm + 0.3, tm + 0.9))
        sube = smooth(pr(t, A.n_levantaba - 0.2 + 0.15 * i, A.n_levantaba + 0.6 + 0.15 * i))
        if alto is None:
            if sube < 0.99:
                objs.append((X, 0, Z, lambda c, X=X, Z=Z, aura=aura, cae=cae, sube=sube, i=i: F.persona(
                    c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, "mercader", anda=0.0, dirx=1, aura=aura,
                    color_aura=PLAGA, cae=cae, op=1 - sube, sem=400 + i)))
        elif sube < 0.99:
            C.peg(objs, cam, t, nom, X, Z, alto, alza=1 - 0.6 * cae, aura=aura, color_aura=PLAGA,
                  op=(1 - sube) * (1 - 0.85 * cae), sem=400 + i, espejo=X > 0)
        if sube > 0.01:                                      # ya es uno de ellos
            nomg = ("Ghoul Ravener", "Rotted One", "Plague Spreader", "Flesh Eater")[i]
            C.peg(objs, cam, t, nomg, X, Z + 30, 345.0, alza=sube, aura=0.7, color_aura=PLAGA, sem=410 + i, espejo=X < 0)
        # el necrófago (dibujado) que lo muerde, al lado
        Xn, Zn = X - 160 * (1 if X > 0 else -1), Z - 80
        llega = smooth(pr(t, tm - 1.6, tm - 0.1))
        vete = 1 - smooth(pr(t, A.n_levantaba, A.n_levantaba + 0.8))
        if llega > 0.01 and vete > 0.01:
            ataca = smooth(pr(t, tm - 0.4, tm)) * (1 - smooth(pr(t, tm + 0.5, tm + 1.0)))
            Xa = lerp(Xn - 500 * (1 if X > 0 else -1) * 0.5, Xn, llega)
            Za = lerp(Zn + 600, Zn, llega)
            objs.append((Xa, 0, Za, lambda c, Xa=Xa, Za=Za, ataca=ataca, llega=llega, i=i, vete=vete: F2.necrofago(
                c, *cam.pt(Xa, 0, Za)[:2], 0.95 * cam.k(cam.pt(Xa, 0, Za)[2]), t, fase=i * 1.3, anda=1.0 * (1 - llega) + 0.3,
                ataca=ataca, op=min(1.0, llega * 3) * vete, sem=420 + i)))
    # más necrófagos que bajan por la calle desde el fondo (la ciudad que cae), lejos y por los lados
    horda = smooth(pr(t, A.n_ciudades - 0.5, A.n_una + 0.5))
    for i in range(6):
        if horda <= 0.01:
            break
        u = (t * 0.03 + i / 6) % 1.0
        X = (-1 if i % 2 else 1) * (180 + 220 * rnd(i, 61))
        Z = 3600 - 1100 * u
        if i % 3 == 0:
            C.peg(objs, cam, t, ("Rotted One", "Plague Spreader", "Ghoul Ravener")[i % 3], X, Z, 340.0, op=horda,
                  aura=0.6, color_aura=PLAGA, sem=430 + i, Y=-6 * abs(math.sin(t * 4 + i)))
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: F2.necrofago(c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]),
                                                                   t, fase=i, anda=0.9, op=horda, sem=440 + i)))
    # monedas desparramadas a «economía»: el cofre volcado del subastador
    eco = smooth(pr(t, A.n_economia - 0.3, A.n_detuvo + 0.3))
    if eco > 0.01:
        def cofre(c):
            px, py, k = _k(cam, 220, 0, 1600)
            c.figura(np.float32([(px - 70 * k, py), (px + 70 * k, py), (px + 64 * k, py - 70 * k), (px - 64 * k, py - 70 * k)]),
                     0.45, contorno=2.2, ang=90, per=4.2, cruz=False)
            for j in range(16):
                d = 40 + 200 * rnd(j, 71) * eco
                a = rnd(j, 72) * 3.14
                qx, qy, kk = _k(cam, 220 + d * math.cos(a), 0, 1600 - 60 + 120 * rnd(j, 73))
                c.figura(circ_pts(qx, qy - 4 * kk, 11 * kk + 1, 10, 5 * kk + 1), 0.0, contorno=1.2)
                c.acento(circ_pts(qx, qy - 4 * kk, 11 * kk + 1, 10, 5 * kk + 1), ORO, 0.85)
        objs.append((220, 0, 1600, cofre))
    C.figuras(g, cam, objs)
    for nom, tm, X in CARTELES:                              # «No podías vender. No podías volar. No podías comprar...»
        op = C.env(t, tm - 0.3, A.n_economia - 0.6, 0.3, 0.4)
        _cartel(g, cam, (X, -600.0 + 5 * math.sin(t + X), 2300.0), nom, t, op=op, tacha=pr(t, tm + 0.15, tm + 0.6),
                techo=-1300, ancho=380, alto=110, px=44)
    op = C.env(t, A.n_economia - 0.5, A.TR_VILLA - 0.3, 0.5, 0.4)
    C.recuerdo_colgado(g, cam, (0.0, -560.0 + 8 * math.sin(t), 1900.0), (1, 0, 0), "_crudos/f3fIVFmy1rk",
                       252.0 + (t - A.n_economia) * 0.8, t, ancho=500, alto=330, texto="Ventormenta · MMVIII", op=op, z=1.3,
                       cx=0.5, cy=0.55, tinta=0.25, sem=41)
    G3.iluminar(g, [(*cam.pt(0, -400, 2600)[:2], 900, 0.35, PLAGA)], amb=0.3, fuerza=0.55, acento=0.15)
    G3.particulas(g, t, "esporas", 70, (0, 200, 1920, 1080), sem=52, color=PLAGA, op=0.7 * horda + 0.2)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 2400)[1]
    GR.niebla(g, y_nb - 60, y_nb + 10, t, op=0.45, sem=53, vel=18)
    with G3.capa_prof(g, cam, 250) as c:                    # primer plano: un farol de la calle, fuera de foco
        px, py, zc = cam.pt(cam.C[0] - 330, 0, cam.C[2] + 360)
        k = cam.k(zc)
        c.trazo([(px, py), (px, py - 620 * k)], 16 * k, afilado=0.0)
        c.figura(np.float32([(px - 40 * k, py - 620 * k), (px + 40 * k, py - 620 * k), (px + 30 * k, py - 720 * k),
                             (px - 30 * k, py - 720 * k)]), 0.15, contorno=2.4, ang=0, per=5, cruz=False)
    return g


# ====================================================================== 4. VILLADORADA Y EL CRUCE
CAM_V = dict(x=0.0, y=-230.0, z=0.0, guinada=0.0, cabeceo=-2.0, f=1450.0, foco=1700.0, apertura=3.0, bruma=0.5,
             lejos=3400.0)
KF_VILLA = [(A.TR_VILLA - 0.6, dict(x=-60.0, y=-230.0, z=-100.0, guinada=-3.0, foco=1500.0)),
            (A.n_villadorada, dict(x=-20.0, y=-235.0, z=20.0, guinada=3.0, foco=1900.0)),
            (A.n_cruce, dict(x=20.0, y=-240.0, z=90.0, guinada=-4.0, foco=1300.0)),
            (A.TR_TORRE + 0.6, dict(x=40.0, y=-250.0, z=170.0, guinada=0.0, cabeceo=-1.0, foco=1500.0))]
POSADA = (380.0, 2100.0)


def villa(t):
    cam = C.camara(t, KF_VILLA, CAM_V)
    g = G(t)
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 30, tono_alto=0.95, tono_bajo=0.55, estrellas=40)
    ox = cam.pt(0, 0, 9000)[0] - 960
    GR.luna(g, 1500 + ox, hz - 320, 64, t, tono_cielo=0.86)
    for j, (y0, amp, tn) in enumerate(((hz - 70, 80, 0.45), (hz - 20, 50, 0.6))):
        GR.colina(g, GR.perfil_colina(-80, 2000, y0, amp, sem=60 + j, n=14), tono=tn, tono2=tn + 0.3, ang=-8, per=5.4,
                  contorno=1.6, cruz=False)
    G3.plano(g, cam, (-6000, 0, -600), (1, 0, 0), (0, 0, 1), 12000, 6000, 0.6, familias=((0.0, 15.0),),
             luces=[(POSADA[0], -200, POSADA[1] - 200, 900, 0.5)], oscuro=0.2)
    X, Z = POSADA                                            # la posada del León Orgulloso: piedra, entramado, tejado
    G3.plano(g, cam, (X - 400, -420, Z), (1, 0, 0), (0, 1, 0), 800, 420, 0.5, familias=((0.0, 18.0),),
             patron=("sillares", 110, 50), quiebre=0.3, contorno=2.4)
    G3.plano(g, cam, (X - 400, -760, Z), (1, 0, 0), (0, 1, 0), 800, 340, 0.1, familias=((0.0, 12.0),), contorno=2.4)
    for dx in (-400, -200, 0, 200, 400):                    # entramado de madera del piso alto
        G3.trazo3d(g, cam, [(X + dx, -420, Z - 3), (X + dx, -760, Z - 3)], 12, afilado=0.0)
    G3.trazo3d(g, cam, [(X - 410, -425, Z - 4), (X + 410, -425, Z - 4)], 16, afilado=0.0)
    puerta = [(X - 60, 0, Z - 3), (X + 60, 0, Z - 3), (X + 60, -240, Z - 3), (X, -290, Z - 3), (X - 60, -240, Z - 3)]
    scr, _ = G3.proyectar(cam, puerta)
    if scr is not None:
        g.figura(scr, 0.9, contorno=2.4, ang=0, per=4, cruz=False)
    G3.trazo3d(g, cam, [(X + 280, -1000, Z + 120), (X + 280, -1300, Z + 120)], 40, afilado=0.0)
    hx, hy, _ = cam.pt(X + 280, -1320, Z + 120)
    G3.humo(g, hx, hy, 1.0, t, sem=65, op=0.5, alto=360, hebras=2)
    techo = [(X - 460, -760, Z - 40), (X + 460, -760, Z - 40), (X + 380, -1250, Z + 260), (X - 380, -1250, Z + 260)]
    scr, _ = G3.proyectar(cam, techo)
    if scr is not None:
        g.figura(scr, 0.65, contorno=2.6, ang=-20, per=4.6)
    for dx in (-300, -100, 100, 300):
        ven = [(X + dx - 50, -640, Z - 2), (X + dx + 50, -640, Z - 2), (X + dx + 50, -520, Z - 2), (X + dx - 50, -520, Z - 2)]
        scr, _ = G3.proyectar(cam, ven)
        if scr is not None:
            g.figura(scr, 0.9, contorno=2.0, ang=0, per=4, cruz=False)
            g.acento(scr, PLAGA, 0.55)
    objs = []
    for i in range(18):                                      # árboles del Bosque de Elwynn
        Xa = (rnd(i, 81) - 0.5) * 5000
        Za = 1200 + 2600 * rnd(i, 82)
        if abs(Xa - X) < 600 and abs(Za - Z) < 500:
            continue
        objs.append((Xa, 0, Za, lambda c, Xa=Xa, Za=Za, i=i: GR.arbol_seco(c, *cam.pt(Xa, 0, Za)[:2],
                                                                            0.9 * cam.k(cam.pt(Xa, 0, Za)[2]), t, sem=i)))
    for i in range(30):
        Xp = (rnd(i, 83) - 0.5) * 3200
        Zp = 300 + 2200 * rnd(i, 84)
        objs.append((Xp, 0, Zp, lambda c, Xp=Xp, Zp=Zp, i=i: GR.pasto(c, *cam.pt(Xp, 0, Zp)[:2], 1.0 * cam.k(cam.pt(Xp, 0, Zp)[2]),
                                                                       t, n=7, sem=i)))
    # el poste con los dos letreros (Villadorada · El Cruce)
    def poste(c):
        G3.trazo3d(c, cam, [(-420, 0, 1300), (-420, -520, 1300)], 18, afilado=0.0)
    objs.append((-420, 0, 1300, poste))
    # los vivos que huyen hacia la posada
    huye = smooth(pr(t, A.TR_VILLA - 0.3, A.n_muertos + 0.4))
    for j in range(4):
        u = pr(t, A.TR_VILLA - 0.5 + 0.3 * j, A.n_esperando + 0.4)
        Xj = lerp(-200 + 140 * j, X - 200 + 120 * j, u)
        Zj = lerp(1100 + 80 * j, Z - 450 + 60 * j, u)
        para = smooth(pr(t, A.n_muertos - 0.1, A.n_muertos + 0.5))
        objs.append((Xj, 0, Zj, lambda c, Xj=Xj, Zj=Zj, j=j, para=para: F.persona(
            c, *cam.pt(Xj, 0, Zj)[:2], 0.95 * cam.k(cam.pt(Xj, 0, Zj)[2]), t, ("capa", "enano", "mercader", "guerrero")[j],
            fase=j, anda=2.0 * (1 - para) + 0.1, dirx=1, sem=500 + j, brazos=(2.4, 2.6) if para > 0.5 else None)))
    # los muertos ya esperaban: se alzan de la hierba alrededor de la posada
    for i, (dx, dz, nom) in enumerate(((-520, -260, "Rotted One"), (-180, -380, None), (160, -360, "Plague Spreader"),
                                       (480, -300, None), (700, -120, "Ghoul Ravener"), (-760, -100, None))):
        Xg, Zg = X + dx, Z + dz
        sube = smooth(pr(t, A.n_muertos - 0.3 + 0.12 * i, A.n_muertos + 0.4 + 0.12 * i))
        if sube <= 0.01:
            continue
        if nom:
            C.peg(objs, cam, t, nom, Xg, Zg, 340.0, alza=sube, aura=0.7, color_aura=PLAGA, sem=520 + i, espejo=dx > 0)
        else:
            objs.append((Xg, 0, Zg, lambda c, Xg=Xg, Zg=Zg, sube=sube, i=i: F2.necrofago(
                c, *cam.pt(Xg, 0, Zg)[:2], 0.95 * cam.k(cam.pt(Xg, 0, Zg)[2]), t, fase=i, anda=0.2, op=sube, sem=530 + i,
                ataca=smooth(pr(t, A.n_esperando, A.n_esperando + 0.4)))))
    C.peg(objs, cam, t, "Marshal Dughan", X - 560, Z - 520, 370.0, sem=540, alza=1 - 0.97 * smooth(pr(t, A.n_esperando + 0.2,
                                                                                                         A.n_esperando + 0.8)))
    C.figuras(g, cam, objs)
    _cartel(g, cam, (-420.0, -470.0, 1296.0), "Villadorada", t, op=smooth(pr(t, A.n_villadorada - 0.3, A.n_villadorada + 0.2)),
            ancho=360, alto=100, px=40, U=(0.95, 0, -0.3), giro=-4)
    _cartel(g, cam, (-420.0, -350.0, 1296.0), "El Cruce", t, op=smooth(pr(t, A.n_cruce - 0.3, A.n_cruce + 0.2)), ancho=320,
            alto=100, px=40, U=(0.95, 0, 0.3), giro=5)
    G3.iluminar(g, [(*cam.pt(X, -580, Z)[:2], 700, 0.5, PLAGA), (*cam.pt(0, 0, 9000)[:2], 600, 0.3)], amb=0.25, fuerza=0.55,
                acento=0.15)
    G3.particulas(g, t, "esporas", 50, (0, 300, 1920, 1080), sem=62, color=PLAGA, op=0.6)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 2000)[1]
    GR.niebla(g, y_nb - 50, y_nb + 10, t, op=0.55, sem=63, vel=20)
    with G3.capa_prof(g, cam, 240) as c:
        px, py, zc = cam.pt(cam.C[0] + 300, 0, cam.C[2] + 320)
        GR.pasto(c, px, py, 1.6 * cam.k(zc), t, n=14, sem=64)
    return g


# ====================================================================== 5. LA TORRE DE LOS MAGOS (portal)
CAM_T = dict(x=0.0, y=-300.0, z=0.0, guinada=0.0, cabeceo=-2.0, f=1450.0, foco=1500.0, apertura=4.5, bruma=0.35,
             lejos=2800.0)
CENTRO = (0.0, 1500.0)
R_SALA = 1150.0
PORTAL = (0.0, -420.0, 2350.0)
KF_TORRE = [(A.TR_TORRE - 0.6, dict(x=0.0, y=-320.0, z=500.0, guinada=0.0, cabeceo=-3.0, foco=1300.0)),
            (A.p_zombis, dict(x=-40.0, y=-330.0, z=560.0, guinada=-4.0, cabeceo=-1.0, foco=1100.0)),
            (A.p_hordas, dict(x=0.0, y=-360.0, z=600.0, guinada=0.0, cabeceo=-4.0, foco=1500.0)),
            (A.p_invadir, dict(x=20.0, y=-380.0, z=680.0, guinada=2.0, cabeceo=-5.0, foco=1650.0)),
            (A.p_escondian, dict(x=-60.0, y=-330.0, z=760.0, guinada=-8.0, cabeceo=-2.0, foco=1350.0)),
            (A.p_torre, dict(x=40.0, y=-360.0, z=800.0, guinada=4.0, cabeceo=-8.0, foco=1500.0)),
            (A.p_cruzabas, dict(x=0.0, y=-400.0, z=1000.0, guinada=0.0, cabeceo=-1.0, foco=1350.0)),
            (A.p_portal + 0.55, dict(x=0.0, y=-420.0, z=2150.0, guinada=0.0, cabeceo=0.0, foco=300.0))]
# al otro lado del portal (la llegada en Ventormenta): la cámara sale del portal mirando a la sala
KF_LLEGADA = [(A.p_portal + 0.55, dict(x=0.0, y=-380.0, z=2250.0, guinada=180.0, cabeceo=2.0, foco=700.0)),
              (A.T_APAGON2, dict(x=0.0, y=-360.0, z=2130.0, guinada=181.0, cabeceo=3.0, foco=650.0))]
T_CRUCE = A.p_portal + 0.55
EMBOSCADOS = [(-380.0, 1550.0, "Ghoul Ravener"), (-180.0, 1420.0, None), (160.0, 1450.0, "Flesh Eater"), (420.0, 1580.0, None),
              (-560.0, 1800.0, None), (580.0, 1820.0, "Plague Spreader"), (0.0, 1250.0, None)]


def _sala_torre(g, cam, t, luces):
    cx, cz = CENTRO
    n = 12
    for i in range(n):                                       # muro circular: 12 paños de sillares con ventanas ojivales
        a0, a1 = i / n * 6.2832, (i + 1) / n * 6.2832
        P0 = (cx + R_SALA * math.sin(a0), cz + R_SALA * math.cos(a0))
        P1 = (cx + R_SALA * math.sin(a1), cz + R_SALA * math.cos(a1))
        U = np.float32((P1[0] - P0[0], 0, P1[1] - P0[1]))
        L = float(np.linalg.norm(U))
        G3.plano(g, cam, (P0[0], -1500, P0[1]), tuple(U / L), (0, 1, 0), L, 1500, 0.32, familias=((0.0, 15.0),),
                 patron=("sillares", 230, 105), var=0.06, luces=luces, oscuro=0.4, contorno=1.6)
        m = ((P0[0] + P1[0]) / 2, (P0[1] + P1[1]) / 2)
        if i % 2 == 0:
            ven = [(m[0] - 70 * U[0] / L, -700, m[1] - 70 * U[2] / L), (m[0] + 70 * U[0] / L, -700, m[1] + 70 * U[2] / L),
                   (m[0] + 70 * U[0] / L, -1050, m[1] + 70 * U[2] / L), (m[0], -1150, m[1]),
                   (m[0] - 70 * U[0] / L, -1050, m[1] - 70 * U[2] / L)]
            scr, _ = G3.proyectar(cam, ven)
            if scr is not None:
                g.figura(scr, 0.85, contorno=2.4, ang=0, per=4, cruz=False)
                g.acento(scr, ESPECTRO, 0.6)
    G3.plano(g, cam, (cx - 1300, 0, cz - 1300), (1, 0, 0), (0, 0, 1), 2600, 2600, 0.5, familias=((0.0, 18.0),),
             patron=("losas", 170), luces=luces, oscuro=0.3)
    # el círculo arcano del suelo
    anillos = [(cx, 0, cz)]
    for r, w in ((620, 9), (560, 4), (380, 6)):
        P = [(cx + r * math.cos(a), -2, cz + r * math.sin(a)) for a in np.linspace(0, 6.2832, 64)]
        G3.trazo3d(g, cam, P, w, afilado=0.0, cerrado=True)
    for i in range(6):
        a = i / 6 * 6.2832 + 0.3
        G3.trazo3d(g, cam, [(cx + 380 * math.cos(a), -2, cz + 380 * math.sin(a)),
                            (cx + 560 * math.cos(a + 2.09), -2, cz + 560 * math.sin(a + 2.09))], 4, afilado=0.0)
    return anillos


def _torre_cam(t):
    if t < T_CRUCE:
        return C.camara(t, KF_TORRE, CAM_T)
    return C.camara(t, KF_LLEGADA, CAM_T)


def torre(t):
    cam = _torre_cam(t)
    g = G(t)
    luces = [(0, -420, 2350, 1400, 0.7)] + [(R_SALA * 0.85 * math.sin(a), -900, CENTRO[1] + R_SALA * 0.85 * math.cos(a), 600, 0.4)
                                            for a in np.linspace(0, 6.28, 6, endpoint=False)]
    apaga = 1 - 0.85 * smooth(pr(t, A.T_APAGON2 - 0.3, A.T_APAGON2 + 0.3))
    luces = [(x, y, z, r, f * apaga) for x, y, z, r, f in luces]
    _sala_torre(g, cam, t, luces)
    objs = []
    for i in range(8):                                       # columnas de la sala
        a = i / 8 * 6.2832 + 0.39
        X, Z = CENTRO[0] + 860 * math.sin(a), CENTRO[1] + 860 * math.cos(a)
        objs.append((X, 0, Z, lambda c, X=X, Z=Z: (
            G3.plano(c, cam, (X - 70, -1500, Z), (1, 0, 0), (0, 1, 0), 140, 1500, 0.45, familias=((90.0, 9.0),), quiebre=0.2,
                     luces=luces, oscuro=0.45, contorno=2.4),
            G3.sombra_contacto(c, cam, X, Z, 110, 40, op=0.7))))
    # el portal (al fondo; después del cruce, la cámara sale de él y lo tiene detrás)
    px, py, zc = cam.pt(*PORTAL)
    k = cam.k(zc)
    if t < T_CRUCE:
        def port(c, px=px, py=py, k=k):
            G3.trazo3d(c, cam, [(-330, 0, PORTAL[2] + 20), (330, 0, PORTAL[2] + 20)], 30, afilado=0.0)
            F2.portal(c, px, py, 300 * k, 400 * k, t, ESPECTRO, fuerza=0.8 * apaga + 0.2)
        objs.append((PORTAL[0], 0, PORTAL[2], port))
    # los que querían ser zombis: bailan la danza macabra con el aura verde (a «zombis»)
    baile = C.env(t, A.p_zombis - 0.5, A.p_hordas + 0.3, 0.6, 0.6)
    for i in range(5):
        if baile <= 0.01:
            break
        a = i / 5 * 6.2832 + t * 0.35
        X, Z = CENTRO[0] + 380 * math.sin(a), CENTRO[1] + 350 + 220 * math.cos(a)
        if i % 2:
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: (
                c.acento_luz(*cam.pt(X, -200, Z)[:2], 280 * cam.k(cam.pt(X, 0, Z)[2]), PLAGA, 0.6 * baile),
                GR.esqueleto_baila(c, *cam.pt(X, 0, Z)[:2], 0.9 * cam.k(cam.pt(X, 0, Z)[2]), t, i * 1.3, brio=1.1,
                                  op=baile, ojos=1.0))))
        else:
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: F.persona(
                c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, ("capa", "enano", "guerrero")[i % 3], fase=i,
                anda=1.2, dirx=1 if math.cos(t * 0.35 + i) > 0 else -1, aura=1.0, color_aura=PLAGA, op=baile, sem=600 + i,
                brazos=(2.5 + 0.3 * math.sin(t * 5 + i), 2.7))))
    # la horda se organiza y entra por el portal (a «hordas» / «portales» / «invadir»)
    for i in range(12):
        t0 = A.p_hordas - 0.6 + 0.12 * i
        u = pr(t, t0, A.p_invadir + 1.6 + 0.1 * i)
        if u <= 0 or u >= 1 or t >= T_CRUCE:
            continue
        fila, col = i // 4, i % 4
        X0, Z0 = -330 + 220 * col, 1550 + 150 * fila
        X, Z = lerp(X0, PORTAL[0] + (col - 1.5) * 60, smooth(u)), lerp(Z0, PORTAL[2] - 40, smooth(u))
        op = 1 - smooth(pr(u, 0.82, 1.0))
        if i % 4 == 1:
            C.peg(objs, cam, t, ("Ghoul Ravener", "Rotted One", "Flesh Eater")[i % 3], X, Z, 330.0, op=op, aura=0.6,
                  color_aura=PLAGA, sem=620 + i, Y=-8 * abs(math.sin(t * 4 + i)))
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i, op=op: F2.necrofago(
            c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, fase=i * 0.7, anda=1.2, op=op, sem=640 + i)))
    # escondidos donde aparecen los viajeros: tras las columnas, agazapados, con los ojos encendidos
    esc = smooth(pr(t, A.p_escondian - 0.4, A.p_viajeros + 0.2))
    if t >= T_CRUCE:
        esc = 1.0
    for i, (X, Z, nom) in enumerate(EMBOSCADOS):
        if esc <= 0.01:
            break
        if t < T_CRUCE and i >= 4:
            continue
        Zp = Z if t >= T_CRUCE else 2350 - (Z - 1250) * 0.3
        Xp = X * (1.0 if t >= T_CRUCE else 1.4)
        ataca = smooth(pr(t, A.p_esperando - 0.2, A.p_esperando + 0.4)) if t >= T_CRUCE else 0.0
        if nom:
            C.peg(objs, cam, t, nom, Xp, Zp, 340.0, op=esc, aura=0.7, color_aura=PLAGA, sem=660 + i, espejo=X > 0)
            continue
        objs.append((Xp, 0, Zp, lambda c, Xp=Xp, Zp=Zp, i=i, ataca=ataca: F2.necrofago(
            c, *cam.pt(Xp, 0, Zp)[:2], 0.95 * cam.k(cam.pt(Xp, 0, Zp)[2]), t, fase=i, anda=0.15, ataca=ataca, op=esc,
            sem=680 + i, ojos=1.0)))
    C.peg(objs, cam, t, "Archmage Malin", 780.0, 1500.0, 370.0, sem=690, op=1.0 if t < T_CRUCE else 0.0)
    C.figuras(g, cam, objs)
    _cartel(g, cam, (0.0, -1080.0 + 6 * math.sin(t), 1650.0), "Torre de los Magos · Ventormenta", t,
            op=C.env(t, A.p_torre - 0.4, A.p_cruzabas, 0.4, 0.5), techo=-1500, ancho=900, alto=130, px=46)
    op = C.env(t, A.p_hordas - 0.4, A.p_escondian, 0.5, 0.5)
    C.recuerdo_colgado(g, cam, (-560.0, -760.0 + 8 * math.sin(t), 1500.0), (0.9, 0, 0.44), "_crudos/fn5-aWcop9k",
                       217.0 + (t - A.p_hordas) * 0.8, t, ancho=500, alto=330, texto="Las hordas · MMVIII", op=op, z=1.3,
                       cx=0.5, cy=0.5, tinta=0.25, sem=51)
    luzp = [(px, py, 900 * k * apaga + 50, 0.7 * apaga, ESPECTRO)] if t < T_CRUCE else [(960, 800, 1400 * apaga + 50, 0.5 * apaga,
                                                                                       ESPECTRO)]
    G3.iluminar(g, luzp, amb=0.16 + 0.1 * apaga, fuerza=0.6, acento=0.18)
    G3.particulas(g, t, "polvo", 70, (0, 0, 1920, 1080), sem=72, color=ESPECTRO, op=0.6 * apaga)
    if t >= T_CRUCE:                                          # el resplandor del portal a la espalda de la cámara
        g.acento_luz(960, 1080, 1100, ESPECTRO, 0.5 * apaga)
    return g


def flash_portal(t):
    """Blanco del portal al cruzarlo (0..1): crece al acercarse y se abre al salir."""
    return smooth(pr(t, A.p_portal - 0.1, T_CRUCE)) * (1 - smooth(pr(t, T_CRUCE, T_CRUCE + 0.5)))


def susto2(t):
    """EL SUSTO (5:47): el necrófago pegado a la cámara, en verde plaga, y su garra."""
    g = G(t)
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.95, ang=-12, per=5.0)
    u = t - A.T_SUSTO2
    s = 1.55 + 0.5 * e_out(min(1.0, u / 0.5))
    F2.cara_necrofago(g, 1180 - 60 * u, 520 + 30 * u, s, t, boca=1.0)
    G3.particulas(g, t, "esporas", 50, (0, 0, 1920, 1080), sem=76, color=PLAGA)
    return g
