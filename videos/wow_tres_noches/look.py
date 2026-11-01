# -*- coding: utf-8 -*-
"""Cuadros de PRUEBA del look «grabado de peste» (sesión 3, 14-oct-2026) para que el usuario apruebe el estilo antes de las
escenas. Tres láminas en ESPACIO 3D (grabado_3d: cámara de perspectiva, suelos y muros con trama en perspectiva, figuras a
distintas profundidades con desenfoque y bruma, claroscuro, haces de luz, partículas, humo, objetos pegados en las paredes):
el cementerio del Ángel, la danza macabra en Forjaz (sangre) y la cripta del recuerdo con el chat (plaga).
`angel()` y la utilería de Forjaz son de ESTE video (no van al kit)."""
import math

import numpy as np

import grabado as GR
import grabado_3d as G3
from grabado import ESPECTRO, ORO, PLAGA, SANGRE, TINTA, G, acabado, catmull, circ_pts, rnd
from grabado_3d import Camara


# ------------------------------------------------------------------ el Ángel de la Resurrección (narradora)
def angel(g, x, y, s, t, ojos=0.0, alas=1.0, op=1.0, gloria=True):
    """El Ángel ESTAMPADO (GR.sprite, 16-oct-2026): se redibuja una vez por tick de HERVOR (túnica, alas y gloria se
    animan a 8 dibujos por segundo, como el contorno); el vaivén y la posición siguen al cuadro exacto."""
    if not GR.CACHE:
        return _angel(g, x, y, s, t, ojos, alas, op, gloria)
    tt = GR.t_tick(t)
    clave = ("angel", GR.hervor(t), round(ojos, 2), round(alas, 2), round(op, 2), gloria)
    GR.sprite(g, clave, x, y + 10 * s * math.sin(t * 1.2), s,
              lambda c, ax, ay, s_: _angel(c, ax, ay - 10 * s_ * math.sin(tt * 1.2), s_, tt, ojos, alas, op, gloria),
              (-540, -640, 540, 310))


def _angel(g, x, y, s, t, ojos=0.0, alas=1.0, op=1.0, gloria=True):
    """El espíritu del cementerio: gloria de rayos detrás, alas abiertas, túnica de pliegues con esclavina y capucha que
    acaba en jirones, brazos abiertos. (x, y) = cintura. `ojos` 0 = cerrados (en paz), 1 = abiertos (susto final)."""
    y = y + 10 * s * math.sin(t * 1.2)
    with g.grupo(x, y, s):
        if gloria:
            R = 330
            g.papel(circ_pts(0, -250, R, 90))
            g.trama(circ_pts(0, -250, R, 90), lambda X, Y: np.clip(0.16 + 0.6 * (np.sqrt(X ** 2 + (Y + 250) ** 2) / R) ** 2,
                                                                   0, 1), modo="rayos", centro=(0, -250), n=150, cruz=False)
            g.trazo(circ_pts(0, -250, R, 90), 2.2, cerrado=True, afilado=0.0)
            g.trazo(circ_pts(0, -250, R * 0.93 + 3 * math.sin(t * 0.9), 90), 1.1, cerrado=True, op=0.7)
            g.acento_luz(0, -250, R * 1.1, ESPECTRO, 0.75, 1.2)
        for lado in (-1, 1):
            GR.ala(g, lado * 38, -205, 1.0, t + lado * 0.3, lado=lado, apertura=alas, tono=0.04, op=op)
        # túnica: pliegues verticales con sombra entre pliegue y pliegue, bajo que ondea y se deshace en jirones
        o = [10 * math.sin(t * 1.7 + i * 0.8) for i in range(8)]
        bajo = [(132 + o[0], 150), (90, 178 + o[1]), (52, 152 + o[2]), (14, 190 + o[3]), (-28, 160 + o[4]),
                (-70, 192 + o[5]), (-112, 162 + o[6]), (-138 + o[7], 140)]
        cuerpo = catmull(np.float32([(-58, -210), (58, -210), (84, -70), (114, 60)] + bajo + [(-110, 60), (-82, -70)]), 5,
                         cerrado=True)
        g.figura(cuerpo, lambda X, Y: 0.03 + 0.55 * (0.5 + 0.5 * np.sin(X / 17.0 + 0.7 * np.sin(Y / 60.0 + t * 0.8))) ** 4
                 + 0.25 * np.clip((Y + 60) / 260, 0, 1) ** 2, contorno=2.6, op=op, ang=90, per=4.4, borde=0.35, rb=28)
        for i in range(-3, 4):
            x0 = i * 17 * math.pi + 4
            pl = [(x0 * 0.35, -150), (x0 * 0.65 + 4 * math.sin(t + i), -40), (x0 * 0.95 + 6 * math.sin(t * 1.3 + i), 80),
                  (x0 * 1.15 + o[i % 8], 158)]
            g.trazo(catmull(np.float32(pl), 6), 1.7, op=0.85 * op, sem=i + 20)
        for i in range(6):
            xs = np.linspace(-100 + 42 * i, -120 + 48 * i + 12 * math.sin(t + i), 6)
            ys = np.linspace(172, 250 + 22 * rnd(i, 3), 6) + 6 * np.sin(np.arange(6) + t * 2 + i)
            g.trazo(np.stack([xs, ys], 1), 2.4, op=0.7 * op, afilado=1.0, sem=i + 40)
        g.acento(cuerpo, ESPECTRO, 0.32, aspero=0.6, sem=3)
        # brazos abiertos: mangas anchas con caída, manos finas
        for lado in (-1, 1):
            br = 6 * math.sin(t * 1.1 + lado)
            manga = [(lado * 50, -200), (lado * 118, -152 + br), (lado * 166, -120 + br), (lado * 158, -80 + br),
                     (lado * 120, -60 + br), (lado * 96, -92 + br), (lado * 66, -120)]
            g.figura(catmull(np.float32(manga), 4, cerrado=True), 0.08, contorno=2.4, op=op, tono2=0.62, luz=90,
                     ang=25 * lado, per=4.4, borde=0.3, rb=14)
            g.trazo(np.float32([(lado * 70, -150), (lado * 120, -110 + br), (lado * 140, -76 + br)]), 1.5, op=0.8 * op)
            mx, my = lado * 172, -102 + br
            for f in range(4):
                fa = math.radians(-25 + f * 14) if lado > 0 else math.radians(180 + 25 - f * 14)
                g.trazo([(mx, my), (mx + 26 * math.cos(fa), my + 26 * math.sin(fa) + 4)], 5.2, op=op, afilado=0.5)
                g.trazo([(mx, my), (mx + 24 * math.cos(fa), my + 24 * math.sin(fa) + 4)], 2.4, color=g.fondo_papel, op=op,
                        afilado=0.7)
            g.figura(circ_pts(mx - lado * 4, my, 11, 16, 9), 0.05, contorno=1.8, op=op, ang=0, per=4, cruz=False)
        # esclavina sobre los hombros (rompe la campana de la túnica)
        escl = catmull(np.float32([(-60, -222), (60, -222), (84, -182), (66, -152), (30, -162), (0, -150), (-30, -162),
                                   (-66, -152), (-84, -182)]), 5, cerrado=True)
        g.figura(escl, 0.05, contorno=2.2, op=op, tono2=0.45, luz=90, ang=-15, per=4.4, borde=0.25, rb=10)
        # capucha y rostro
        cap = catmull(np.float32([(0, -318), (40, -300), (58, -258), (62, -214), (34, -200), (0, -206), (-34, -200),
                                  (-62, -214), (-58, -258), (-40, -300)]), 5, cerrado=True)
        g.figura(cap, 0.22, contorno=2.6, op=op, tono2=0.72, luz=0, ang=70, per=4.4, modo="contorno", borde=0.3, rb=12)
        cara = circ_pts(0, -250, 25, 32, 33)
        g.figura(cara, 0.03, contorno=1.6, op=op, tono2=0.7, luz=-90, ang=0, per=3.6, cruz=False)
        g.trama(circ_pts(0, -278, 32, 30, 14), 0.82, ang=0, per=3.6, cruz=False, op=op)
        if ojos < 0.5:
            for sx in (-1, 1):
                g.trazo([(sx * 15, -252), (sx * 9, -248), (sx * 3, -251)], 1.6, op=op)
        else:
            for sx in (-1, 1):
                g.figura(circ_pts(sx * 10, -252, 6.5, 16, 4.6), 0.0, contorno=1.4, op=op)
                g.circ(sx * 10, -252, 2.6, TINTA, op)
        g.trazo([(0, -246), (-2, -236), (2, -233)], 1.2, op=op)
        g.trazo([(-6, -224), (0, -222), (6, -224)], 1.3, op=op)


# ------------------------------------------------------------------ lámina A: el cementerio (3D)
CAM_A = dict(x=0.0, y=-150.0, z=0.0, guinada=0.0, cabeceo=0.8, f=1500.0, foco=1300.0, apertura=4.5, bruma=0.55,
             lejos=2600.0)


def _camino(b):
    return -60 + 210 * np.clip(b / 1400.0, 0, 1)


def _tumbas():
    """Filas de tumbas repartidas DENTRO del campo de visión (±0,62·Z), sin pisar el sendero ni al Ángel."""
    out, i = [], 0
    for fila, Z in enumerate(np.arange(520, 3400, 240)):
        n = int(3 + Z / 520)
        for j in range(n):
            u = (j + 0.5 + 0.7 * (rnd(fila * 13 + j, 7) - 0.5)) / n
            X = (-0.78 + 1.56 * u) * 0.62 * Z
            Zj = Z + 60 * (rnd(fila * 7 + j, 8) - 0.5)
            if abs(X - _camino(Zj)) < 170 + 0.05 * Zj or (abs(X - 150) < 380 and 1050 < Zj < 1700) or X > 600:
                continue
            out.append((X, Zj, ("arco", "cruz", "plana")[i % 3], 10 * (rnd(i, 5) - 0.5)))
            i += 1
    return out


TUMBAS = _tumbas()


def lamina_cementerio(t, cam=None):
    cam = cam or Camara(**CAM_A)
    g = G(t)
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 70, tono_alto=1.0, tono_bajo=0.56)
    mx, my = 650 - 0.25 * (cam.C[0]), 170
    GR.luna(g, mx, my, 74, t, tono_cielo=0.86)
    G3.haz(g, mx, my, 62, 22, 1100, t, op=0.20)
    GR.nube(g, 1350, 120, 520, t, sem=1, vel=5)
    GR.nube(g, 230, 300, 360, t, sem=3, vel=4, tono=0.28)
    for i in range(3):
        cx = (300 + 520 * i + t * (38 + 9 * i)) % 2300 - 150
        GR.cuervo(g, cx, 230 + 60 * i + 14 * math.sin(t * 0.8 + i), 0.75 - 0.15 * i, t, fase=i * 2.1)
    # horizonte: colinas lejanas con la capilla (ya en la bruma)
    GR.colina(g, GR.perfil_colina(-60, 1980, hz + 10, 26, sem=1), tono=0.26, tono2=0.4, ang=-3, per=5.0, contorno=1.6,
              cruz=False)
    with g.grupo(1500, hz + 12, 0.42):
        g.macizo([(-70, 0), (70, 0), (70, -120), (0, -190), (-70, -120)], 0.85)
        g.macizo([(70, 0), (150, 0), (150, -90), (70, -90)], 0.85)
        g.macizo([(-25, -190), (25, -190), (25, -300), (0, -330), (-25, -300)], 0.85)
        g.papel(circ_pts(0, -240, 9, 14, 13), 0.9)
        g.acento_luz(0, -240, 50, ORO, 0.7)
    # el suelo: trama en perspectiva con el sendero que lleva al Ángel y el charco de luz que ella echa
    ax, ay, az = 150, -250, 1350

    def tono_suelo(a, b, zc):
        base = 0.62 + 0.06 * np.clip(b / 3000.0, 0, 1)
        sendero = np.clip(1 - np.abs(a - _camino(b)) / (70 + 0.03 * b), 0, 1) * (b < 1500)
        return base - 0.34 * sendero
    G3.plano(g, cam, (-5000, 0, 40), (1, 0, 0), (0, 0, 1), 10000, 5200, tono_suelo, familias=((0.0, 14.0),),
             luces=[(ax, 0, az, 950, 0.95)], oscuro=0.2)
    # figuras por bandas de profundidad (lejos -> cerca), cada banda con su desenfoque y bruma
    objs = []
    for i, (X, Z, fm, inc) in enumerate(TUMBAS):
        objs.append((Z, "tumba", X, fm, inc, i))
    objs.append((1500, "arbol", -560))
    for i in range(3):                                   # almas que se acercan al Ángel por la izquierda del sendero
        objs.append((1230 - 110 * i, "alma", -560 + 150 * i + 22 * t, i))
    for i in range(46):                                  # hierba seca por todo el suelo (da escala a cada distancia)
        Z = 450 + 2600 * rnd(i, 21) ** 1.3
        objs.append((Z, "pasto", (rnd(i, 22) - 0.5) * 1.3 * Z, i))
    objs.append((az, "angel", ax))
    bandas = [(2000, 9e9), (1000, 2000), (420, 1000)]
    for zmin, zmax in bandas:
        zc_rep = {2000: 2700, 1000: 1350, 420: 760}[zmin]
        with G3.capa_prof(g, cam, zc_rep) as c:
            if zmin == 1000:                                                    # la reja que se aleja por la derecha
                _reja3d(c, cam, 650, 900, 3400, t)
            for o in sorted([o for o in objs if zmin <= o[0] < zmax], key=lambda o: -o[0]):
                _objeto_cementerio(c, cam, o, t)
        y_nb = cam.pt(0, 0, zmin)[1]
        GR.niebla(g, y_nb - 40, y_nb + 12, t, op=0.45, sem=int(zmin), vel=22)
    # luz: claroscuro (luna + gloria del Ángel); lo demás se hunde en trama
    sx, sy, zc = cam.pt(ax, ay - 250, az)
    G3.iluminar(g, [(mx, my, 760, 0.55), (sx, sy, 900 * cam.k(zc), 0.95)], amb=0.18, fuerza=0.55)
    G3.particulas(g, t, "polvo", 70, (sx - 600, sy - 400, sx + 600, sy + 500), sem=2)
    # primer plano: hierba y dos tumbas enormes, fuera de foco
    with G3.capa_prof(g, cam, 230) as c:
        for i in range(9):
            px, py, zc = cam.pt(-330 + 80 * i, 0, 300 + 60 * rnd(i, 5))
            GR.pasto(c, px, py, 0.9 * cam.k(zc), t, n=8, sem=i)
        px, py, zc = cam.pt(-215, 0, 340)
        GR.lapida(c, px, py, 0.95 * cam.k(zc), "arco", 7, tono=0.8, tono2=0.97, sem=31)
        px, py, zc = cam.pt(255, 0, 400)
        GR.pasto(c, px, py, 1.5 * cam.k(zc), t, n=14, sem=40)
    return acabado(g, vineta=1.15)


def _reja3d(g, cam, X, z0, z1, t, paso=70.0, alto=120.0):
    zs = np.arange(z0, z1, paso)
    for Y in (-alto * 0.2, -alto * 0.8):
        G3.trazo3d(g, cam, [(X, Y, z0), (X, Y, z1)], 4.0, afilado=0.0)
    for i, Z in enumerate(zs):
        top = -alto - (10 if i % 2 else 0)
        G3.trazo3d(g, cam, [(X, 0, Z), (X, top, Z)], 5.0, afilado=0.0, densidad=3)
        px, py, zc = cam.pt(X, top, Z)
        k = cam.k(zc)
        g.macizo([(px - 7 * k, py + 2 * k), (px, py - 18 * k), (px + 7 * k, py + 2 * k), (px, py - 2 * k)])


def _objeto_cementerio(c, cam, o, t):
    tipo = o[1]
    if tipo == "tumba":
        _, _, X, fm, inc, i = o
        Z = o[0]
        G3.sombra_contacto(c, cam, X, Z + 10, 70, 26, op=0.8)
        px, py, zc = cam.pt(X, 0, Z)
        GR.lapida(c, px, py, 0.95 * cam.k(zc), fm, inc, "R.I.P." if fm == "arco" and Z < 1300 else "", sem=i,
                  grieta=Z < 1600)
        if Z < 1800:
            for j in range(2):
                GR.pasto(c, px + (j - 0.5) * 70 * cam.k(zc), py + 2, 1.1 * cam.k(zc), t, n=6, sem=i * 3 + j)
    elif tipo == "pasto":
        px, py, zc = cam.pt(o[2], 0, o[0])
        GR.pasto(c, px, py, 0.9 * cam.k(zc), t, n=7, sem=o[3])
    elif tipo == "arbol":
        X = o[2]
        px, py, zc = cam.pt(X, 0, o[0])
        GR.arbol_seco(c, px, py, 2.3 * cam.k(zc), t, sem=4)
    elif tipo == "alma":
        _, _, X, i = o
        Z = o[0]
        G3.sombra_contacto(c, cam, X, Z, 60, 22, op=0.35, tono=0.6)
        px, py, zc = cam.pt(X, -150, Z)
        GR.fantasma(c, px, py, 0.5 * cam.k(zc), t, fase=i * 1.7, op=0.95)
    elif tipo == "angel":
        X = o[2]
        px, py, zc = cam.pt(X, -250, o[0])
        angel(c, px, py, 0.74 * cam.k(zc), t)


# ------------------------------------------------------------------ lámina B: danza macabra en Forjaz (sala 3D, sangre)
CAM_B = dict(x=0.0, y=-175.0, z=0.0, guinada=0.0, cabeceo=-3.0, f=1350.0, foco=1050.0, apertura=8.0, bruma=0.3,
             lejos=3600.0)


def lamina_danza(t, cam=None):
    cam = cam or Camara(**CAM_B)
    g = G(t)
    fragua = (0, -220, 2700)
    luces = [(fragua[0], fragua[1], fragua[2], 2300, 1.0), (-640, -380, 1300, 520, 0.7), (640, -380, 1300, 520, 0.7)]
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.92, ang=10, per=6.0)
    # techo, muros y suelo de la sala
    G3.plano(g, cam, (-700, -950, 60), (1, 0, 0), (0, 0, 1), 1400, 2600, 0.93, familias=((90.0, 12.0), (0.0, 16.0)),
             patron=("losas", 260), luces=luces, oscuro=0.1, junta=6)
    for X, U in ((-700, (0, 0, 1)), (700, (0, 0, 1))):
        G3.plano(g, cam, (X, -950, 60), U, (0, 1, 0), 2600, 950, 0.48, familias=((0.0, 9.0), (60.0, 12.0)),
                 patron=("sillares", 200, 95), quiebre=0.35, tramo=55, luces=luces, oscuro=0.45, junta=5)
    G3.plano(g, cam, (-700, 0, 60), (1, 0, 0), (0, 0, 1), 1400, 2600, 0.3, familias=((0.0, 9.0),),
             patron=("losas", 180), luces=luces, oscuro=0.4, junta=5, quiebre=0.3, tramo=50)
    G3.plano(g, cam, (-700, -950, 2660), (1, 0, 0), (0, 1, 0), 1400, 950, 0.45, familias=((0.0, 9.0), (60.0, 12.0)),
             patron=("sillares", 200, 95), quiebre=0.35, tramo=55, luces=luces, oscuro=0.4, junta=5)
    # el gran arco del fondo: túnel que se pierde hasta la fragua
    for k_, Z in enumerate((2655, 3000, 3400)):
        aw, ah = 540 - 80 * k_, 900 - 100 * k_
        arc3 = [(-aw, 0, Z)] + [(aw * math.cos(u), -(ah - aw) - aw * math.sin(u), Z) for u in np.linspace(math.pi, 0, 26)] \
            + [(aw, 0, Z)]
        scr, _ = G3.proyectar(cam, arc3)
        if scr is not None:
            g.figura(scr, 0.94 - 0.04 * k_, contorno=3.0 - 0.6 * k_, ang=0, per=5.0, cruz=False)
    fx, fy, fz = cam.pt(0, -60, 3500)
    for i, dx in enumerate((-140, 0, 140)):
        px, py, zc = cam.pt(dx * 1.6, 0, 3500)
        GR.llama(g, px, py, 3.2 * cam.k(zc) * 2.2, t, sem=i, color=ORO)
    g.acento_luz(fx, fy, 420, ORO, 0.75)
    G3.particulas(g, t, "brasas", 40, (fx - 260, fy - 520, fx + 260, fy + 40), sem=5)
    # estandartes clavados en los muros (en perspectiva) y columnas
    for lado, Zc in ((-1, 1050), (1, 1050), (-1, 1800), (1, 1800)):
        q = G3.quad_mundo(cam, (lado * 698, -560, Zc), (0, 0, -lado), (0, 1, 0), 260, 420)
        if q is not None:
            G3.estampar(g, _estandarte(t, lado), q, sombra=0.5, off=(10 * -lado, 14))
    cols = [(lado * 640, Z) for Z in (700, 1400, 2150) for lado in (-1, 1)]
    # suelo: sangre y huesos (en perspectiva)
    for i in range(8):
        X, Z = -520 + 1040 * rnd(i, 81), 600 + 1500 * rnd(i, 82)
        pts = GR.silueta_ruido(circ_pts(0, 0, 70 + 50 * rnd(i, 83), 30, 40 + 30 * rnd(i, 84)), 12, sem=i)
        scr, _ = G3.proyectar(cam, np.stack([X + pts[:, 0], np.zeros(len(pts)), Z + pts[:, 1]], 1))
        if scr is not None:
            g.acento(scr, SANGRE, 0.85, aspero=0.0)
    objs = [(Z, "col", X) for X, Z in cols]
    for i, (X, Z, ph) in enumerate(((-260, 1250, 0.0), (40, 1000, 2.1), (330, 1180, 4.2), (-120, 1650, 1.0))):
        objs.append((Z, "esq", X, ph, i))
    for i in range(7):
        objs.append((700 + 1300 * rnd(i, 91), "huesos", -500 + 1000 * rnd(i, 92), i))
    for Z, *resto in sorted(objs, key=lambda o: -o[0]):
        tipo = resto[0]
        if tipo == "col":
            _columna(g, cam, resto[1], Z, luces)
        elif tipo == "huesos":
            X, i = resto[1], resto[2]
            a_ = rnd(i, 87) * 3.1416
            p0 = cam.pt(X - 45 * math.cos(a_), -8, Z - 45 * math.sin(a_))
            p1 = cam.pt(X + 45 * math.cos(a_), -8, Z + 45 * math.sin(a_))
            G3.sombra_contacto(g, cam, X, Z, 50, 22, op=0.6)
            GR._hueso(g, p0[:2], p1[:2], 10 * cam.k(p0[2]))
            if i % 2 == 0:
                px, py, zc = cam.pt(X + 60, 0, Z - 30)
                GR.craneo(g, px, py - 20 * cam.k(zc), 21 * cam.k(zc), t, ang=0.5 * (rnd(i, 85) - 0.5), mand=0.3 * rnd(i, 86))
        else:
            X, ph, i = resto[1], resto[2], resto[3]
            px, py, zc = cam.pt(X, 0, Z)
            c = G3.nueva_capa(g)
            GR.esqueleto(c, px, py, 0.95 * cam.k(zc) * 0.95, GR.pose_danza(t, ph), t)
            G3.sombra_capa(g, c, (px, py), dirx=(px - fx) / 900, diry=0.55, largo=1.0, op=0.8)
            G3.sombra_contacto(g, cam, X, Z, 70, 26, op=0.9)
            GR.componer(g, c, cam.sigma(zc), cam.niebla(zc))
    # haz de la fragua hacia la cámara
    G3.haz(g, fx, fy - 120, 90, 70, 900, t, op=0.22)
    G3.iluminar(g, [(fx, fy, 1250, 1.0, ORO), (cam.pt(-640, -380, 1300)[0], cam.pt(-640, -380, 1300)[1], 380, 0.6),
                    (cam.pt(640, -380, 1300)[0], cam.pt(640, -380, 1300)[1], 380, 0.6)], amb=0.12, fuerza=0.6, acento=0.25)
    G3.particulas(g, t, "polvo", 50, (fx - 500, fy - 200, fx + 500, 1080), sem=7)
    # la cartela cuelga del techo con dos cadenas (objeto en el espacio, no rótulo pegado a la pantalla)
    s = G(t, 900, 170, alfa=True)
    GR.cartela(s, 450, 85, 700, "Forjaz · Septiembre de MMV", t, px=46)
    for xx in (-290, 290):
        G3.trazo3d(g, cam, [(xx, -950, 1300), (xx, -632, 1300)], 3.0, afilado=0.0)
    q = G3.quad_mundo(cam, (0, -560, 1300), (1, 0, 0), (0, 1, 0), 760, 144)
    if q is not None:
        G3.estampar(g, s, q, sombra=0.3, off=(8, 12))
    # primer plano: un esqueleto enorme y desenfocado que baila a la izquierda
    with G3.capa_prof(g, cam, 480) as c:
        px, py, zc = cam.pt(-250, 0, 480)
        GR.esqueleto(c, px, py, 0.95 * cam.k(zc), GR.pose_danza(t, 5.0, vel=0.9), t)
    return acabado(g, vineta=1.1)


def _columna(g, cam, X, Z, luces):
    b = cam.pt(X, 0, Z)
    a = cam.pt(X, -950, Z)
    k = cam.k(b[2])
    w = 62 * k
    fuste = [(b[0] - w, b[1]), (b[0] + w, b[1]), (a[0] + w, a[1]), (a[0] - w, a[1])]
    lado = 1 if X < 0 else -1                                             # la cara que mira a la fragua, iluminada
    g.figura(np.float32(fuste), 0.1, contorno=2.6, tono2=0.85, luz=0 if lado > 0 else 180, ang=90, per=4.6, borde=0.25,
             rb=10 * k)
    for yy, hh in ((b[1], -40 * k), (a[1] + 60 * k, -60 * k)):
        g.figura(np.float32([(b[0] - w * 1.4, yy), (b[0] + w * 1.4, yy), (b[0] + w * 1.4, yy + hh), (b[0] - w * 1.4, yy + hh)]),
                 0.4, contorno=2.2, ang=0, per=4.2, cruz=False)


def _estandarte(t, lado):
    s = G(t, 260, 420, alfa=True)
    ond = [6 * math.sin(t * 1.4 + lado + k) for k in range(4)]
    est = [(20, 10), (240, 10), (240 + ond[0], 330), (130 + ond[1], 410 + ond[2]), (20 + ond[3], 330)]
    s.figura(np.float32(est), 0.15, contorno=3.0, tono2=0.6, luz=0, ang=90, per=4.4)
    s.acento(np.float32(est), SANGRE, 0.8, sem=lado + 3)
    GR.craneo(s, 130, 180, 46, t)
    s.trazo([(10, 10), (250, 10)], 6, afilado=0.0)
    return s


# ------------------------------------------------------------------ lámina C: la cripta del recuerdo (plaga)
CHAT = [("General", "Thaldrin", "¿alguien abrió las cajas del muelle?", 0.0),
        ("Hermandad", "Mirela", "me salió un reloj... diez minutos", 0.0),
        ("General", "Brok", "¡no te acerques a los guardias!", 0.0),
        ("Susurro", "???", "tengo hambre", 0.0)]
CAM_C = dict(x=-260.0, y=-310.0, z=-480.0, guinada=13.0, cabeceo=1.5, f=1500.0, foco=1700.0, apertura=7.0, bruma=0.18,
             lejos=3000.0)


def _lienzo_recuerdo(t, seg):
    s = G(t, 1100, 800, alfa=True)
    GR.recuerdo(s, "_crudos/cqp86JngGcY", seg, 70, 150, 1030, 730, t, tinta=0.2, come=1.0, texto="Forjaz · Octubre de MMVIII",
                px=44, z=1.3, cx=0.45, cy=0.5)
    return s


def _lienzo_chat(t, corr):
    s = G(t, 700, 340, alfa=True)
    perg = GR.silueta_ruido(np.float32([(18, 22), (682, 14), (690, 318), (12, 326)]), 3.0, sem=4, paso=10)
    s.figura(perg, 0.10, contorno=2.4, ang=0, per=5.0, cruz=False, borde=0.5, rb=26)
    for nx, ny in ((40, 40), (660, 36)):
        s.circ(nx, ny, 9, TINTA)
        s.circ(nx - 2, ny - 2, 3, s.fondo_papel, 0.7)
    GR.chat(s, 40, 300, CHAT, t, corr=corr, ancho=620, px=27, color_canal=(0.30, 0.42, 0.06))
    return s


def _lienzo_reloj(t):
    s = G(t, 380, 380, alfa=True)
    with s.grupo(190, 190, 1.15):
        s.figura(circ_pts(0, 0, 150, 60), 0.0, contorno=3.4)
        s.trazo(circ_pts(0, 0, 132, 60), 1.4, cerrado=True)
        for i in range(12):
            a = i / 12 * 6.2832
            s.trazo([(118 * math.cos(a), 118 * math.sin(a)), (134 * math.cos(a), 134 * math.sin(a))], 3.2, afilado=0.0)
        s.trama(circ_pts(0, 0, 112, 60), 0.10, tono2=0.5, luz=45, ang=0, per=4.5, modo="anillos", centro=(0, 0),
                cruz=False)
        s.texto("9:58", 0, 10, 76, TINTA, "gara_b")
        a = -math.pi / 2 + ((t * 0.6) % 1) * 6.2832
        s.trazo([(0, 0), (100 * math.cos(a), 100 * math.sin(a))], 5, w1=1.5, afilado=0.0)
        s.acento(circ_pts(0, 0, 150, 40), PLAGA, 0.55, sem=7)
    return s


def lamina_recuerdo(t, cam=None, corr=0.45):
    cam = cam or Camara(**CAM_C)
    g = G(t)
    velas = [(-560, -150, 1140), (560, -150, 1140)]
    luces = [(x, y - 40, z, 700, 0.95) for x, y, z in velas] + [(-40, -380, 1100, 650, 0.8)]
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.9, ang=10, per=6.0)
    G3.plano(g, cam, (-1300, -720, -500), (1, 0, 0), (0, 0, 1), 2600, 1710, 0.95, familias=((90.0, 12.0),), luces=luces,
             patron=("losas", 300), junta=6)
    G3.plano(g, cam, (-1000, -720, -500), (0, 0, 1), (0, 1, 0), 1710, 720, 0.5, familias=((0.0, 9.0), (60.0, 12.0)),
             patron=("sillares", 210, 100), quiebre=0.35, tramo=55, luces=luces, oscuro=0.45, junta=5)
    G3.plano(g, cam, (-1000, -720, 1210), (1, 0, 0), (0, 1, 0), 2300, 720, 0.42, familias=((0.0, 9.0), (60.0, 12.0)),
             patron=("sillares", 210, 100), quiebre=0.35, tramo=55, luces=luces, oscuro=0.42, junta=5)
    G3.plano(g, cam, (-1000, 0, -500), (1, 0, 0), (0, 0, 1), 2300, 1710, 0.42, familias=((0.0, 9.0),),
             patron=("losas", 170), luces=luces, oscuro=0.42, junta=4)
    # telarañas en la esquina
    for i in range(6):
        a = i / 5 * math.pi / 2
        G3.trazo3d(g, cam, [(-1000, -720, 1210), (-1000 + 260 * math.cos(a), -720 + 260 * math.sin(a), 1210 - 120 * math.cos(a))],
                   1.0, op=0.7, color=g.fondo_papel)
    # objetos en la pared (en perspectiva, con sombra): el recuerdo, el reloj de la plaga y el chat clavado
    for lienzo, cen, w_, h_, giro in ((_lienzo_recuerdo(t, 64.0 + 0.8 * t), (-40, -380, 1209), 800, 582, 0.0),
                                      (_lienzo_reloj(t), (-700, -430, 1209), 230, 230, 0.0),
                                      (_lienzo_chat(t, corr), (640, -330, 1209), 470, 228, -3.0)):
        q = G3.quad_mundo(cam, cen, (1, 0, 0), (0, 1, 0), w_, h_, giro)
        if q is not None:
            G3.estampar(g, lienzo, q, sombra=0.55, off=(18, 26), desenfoque_sombra=14)
    # velas sobre candeleros, humo
    for i, (x, y, z) in enumerate(velas):
        _candelero(g, cam, x, z, t, i)
    G3.iluminar(g, [(*cam.pt(x, y - 60, z)[:2], 700 * cam.k(cam.pt(x, y, z)[2]), 0.95, ORO) for x, y, z in velas]
                + [(*cam.pt(-40, -380, 1150)[:2], 520, 0.75)], amb=0.15, fuerza=0.6, acento=0.3)
    for x, y, z in velas:
        px, py, zc = cam.pt(x, y - 100, z)
        G3.particulas(g, t, "polvo", 25, (px - 220, py - 300, px + 220, py + 200), sem=int(x))
    G3.particulas(g, t, "esporas", 30, (0, 600, 1920, 1080), sem=9)
    g.acento_luz(*cam.pt(-40, -380, 1209)[:2], 700, PLAGA, 0.22, 1.0)
    # primer plano: la vela grande, fuera de foco
    with GR.capa(g, desenfoque=12) as c:                      # primer plano: barrotes de la reja de la cripta, fuera de foco
        for bx in (70, 190, 1760, 1880):
            c.macizo([(bx - 22, -40), (bx + 22, -40), (bx + 22, 1120), (bx - 22, 1120)])
            c.trazo([(bx - 8, -40), (bx - 8, 1120)], 3, color=c.fondo_papel, op=0.35, afilado=0.0)
        for yy in (150, 930):
            c.macizo([(-20, yy - 16), (260, yy - 16), (260, yy + 16), (-20, yy + 16)])
            c.macizo([(1690, yy - 16), (1940, yy - 16), (1940, yy + 16), (1690, yy + 16)])
    return acabado(g, vineta=1.15)


def _candelero(g, cam, X, Z, t, i, humo_op=0.6, alto=1.0):
    """Candelero de hierro con vela, llama y humo, de pie en el suelo (X, Z). `alto` estira el fuste."""
    b = cam.pt(X, 0, Z)
    k = cam.k(b[2])
    x, y = b[0], b[1]
    h1 = (26 + 84 * alto) * k
    G3.sombra_contacto(g, cam, X, Z, 50, 20, op=0.8)
    g.figura(np.float32([(x - 34 * k, y), (x + 34 * k, y), (x + 14 * k, y - 26 * k), (x - 14 * k, y - 26 * k)]), 0.3,
             contorno=2.2, ang=0, per=4.2, cruz=False)
    g.figura(np.float32([(x - 6 * k, y - 26 * k), (x + 6 * k, y - 26 * k), (x + 6 * k, y - h1), (x - 6 * k, y - h1)]),
             0.35, contorno=2.0, ang=90, per=4.2, cruz=False)
    g.figura(np.float32([(x - 26 * k, y - h1), (x + 26 * k, y - h1), (x + 18 * k, y - h1 - 12 * k), (x - 18 * k, y - h1 - 12 * k)]),
             0.4, contorno=2.0, ang=0, per=4.2, cruz=False)
    yv = y - h1 - 12 * k
    g.figura(np.float32([(x - 11 * k, yv), (x + 11 * k, yv), (x + 11 * k, yv - 68 * k), (x - 11 * k, yv - 68 * k)]),
             0.06, contorno=2.0, tono2=0.5, luz=0, ang=90, per=4.0, cruz=False)
    g.trazo([(x + 4 * k, yv - 68 * k), (x + 6 * k, yv - 48 * k), (x + 3 * k, yv - 38 * k)], 2.6 * k, afilado=0.3)
    GR.llama(g, x, yv - 70 * k, 0.75 * k, t, sem=i, color=ORO)
    G3.humo(g, x, yv - 118 * k, 0.9 * k, t, sem=i, op=humo_op, alto=300)


LAMINAS = {"cementerio": lamina_cementerio, "danza": lamina_danza, "recuerdo": lamina_recuerdo}
