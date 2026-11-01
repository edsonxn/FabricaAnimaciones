# -*- coding: utf-8 -*-
"""Decorado 1: el CEMENTERIO del Ángel (gancho 0:00-0:41 y el ciclo de las almas 2:04-2:13). Parte de la lámina A aprobada
(look.py) y le suma lo de cada frase: el alma que corre, la procesión de millones, las tres tumbas que brotan con su relieve
(un mal salto, un jefe, una apuesta), los tres candeleros de las tres noches (sangre, plaga, helado) y la tumba sin nombre."""
import math

import numpy as np

import anclas as A
import comun as C
import fig as F
import grabado as GR
import grabado_3d as G3
import look as L
from grabado import ESPECTRO, HIELO, ORO, PLAGA, SANGRE, TINTA, G, acabado, circ_pts, e_out, pr, rnd, smooth
from grabado_3d import Camara

ANGEL = (150.0, -250.0, 1350.0)
RELIEVES = [(-360.0, 950.0, F.icono_caida, A.g_salto), (-160.0, 950.0, F.icono_jefe, A.g_jefe),
            (40.0, 950.0, F.icono_apuesta, A.g_apuesta)]
# pegatinas reales (render oficial de Wowhead; persona dibujada ≈ 360): el muerto de cada tumba (salto, jefe, apuesta)
# y los que vuelven a la ciudad en el ciclo
PEG_MUERTOS = [("Ironforge Mountaineer", 270.0), ("Rattlegore", 400.0), ("Orgrimmar Grunt", 360.0)]
PEG_CICLO = [("Stormwind City Guard", 370.0), ("Ironforge Mountaineer", 285.0), ("Brother Paxton", 365.0)]
FAROLES = [(-40.0, 1180.0, SANGRE, A.g_tres, "I"), (150.0, 1180.0, PLAGA, A.g_tres2 - 0.25, "II"),
           (340.0, 1180.0, HIELO, A.g_olvido, "III")]
VACIA = (560.0, 1290.0)
LIBRE = [(x, z) for x, z, *_ in RELIEVES] + [(x, z) for x, z, *_ in FAROLES] + [VACIA]
TUMBAS = [tb for tb in L.TUMBAS if all(math.hypot(tb[0] - x, tb[1] - z) > 210 for x, z in LIBRE)]

KF_GANCHO = [(0.0, dict(x=-60.0, y=-120.0, z=-430.0, guinada=2.0, cabeceo=1.0)),
             (6.7, dict(x=-50.0, y=-135.0, z=-260.0, guinada=1.5, cabeceo=0.8)),
             (13.0, dict(x=-30.0, y=-150.0, z=-20.0, guinada=1.0, cabeceo=0.5)),
             (17.5, dict(x=-20.0, y=-175.0, z=150.0, guinada=0.0, cabeceo=-1.5)),
             (19.6, dict(x=-20.0, y=-178.0, z=170.0, guinada=0.3, cabeceo=-1.3, foco=820.0)),
             (23.7, dict(x=-20.0, y=-180.0, z=196.0, guinada=0.9, cabeceo=-1.0, foco=820.0)),
             (24.6, dict(x=-18.0, y=-180.0, z=205.0, guinada=1.0, cabeceo=-1.0, foco=1150.0)),
             (32.5, dict(x=40.0, y=-180.0, z=280.0, guinada=3.0, cabeceo=-0.5)),
             (38.6, dict(x=240.0, y=-170.0, z=560.0, guinada=6.0, cabeceo=1.0)),
             (41.5, dict(x=262.0, y=-168.0, z=600.0, guinada=6.5, cabeceo=1.2))]
KF_CICLO = [(A.TR_CEM, dict(x=-40.0, y=-170.0, z=120.0, guinada=-2.0, cabeceo=-1.0)),
            (A.c_resucitaba, dict(x=-20.0, y=-190.0, z=220.0, guinada=0.0, cabeceo=-2.0)),
            (A.TR_CAMPO + 0.6, dict(x=10.0, y=-200.0, z=330.0, guinada=2.0, cabeceo=-2.0))]


def _alma_corre(t):
    """El alma que corre por el sendero hasta el Ángel (gancho, frase 1). Devuelve (X, Z, op) o None."""
    t0, t1 = A.g_moriste - 0.5, A.g_yo + 0.3
    if not (t0 <= t <= t1 + 0.6):
        return None
    u = pr(t, t0, t1)
    Z = 150 + 1050 * u
    return L._camino(Z) - 40, Z, (1 - pr(t, t1, t1 + 0.6)) * pr(t, t0, t0 + 0.3)


def _tumba_relieve(c, cam, X, Z, icono, t0, t):
    """Tumba que BROTA del suelo a la palabra, con su relieve tallándose."""
    alza = e_out(pr(t, t0 - 0.35, t0 + 0.25)) * (1 - GR.e_in(pr(t, A.g_tres - 0.75, A.g_tres - 0.1)))
    if alza <= 0.01:
        return
    talla = smooth(pr(t, t0 - 0.05, t0 + 0.55))
    h = 260 * alza
    G3.sombra_contacto(c, cam, X, Z + 6, 110, 34, op=0.85)
    lz = F.relieve(t, icono, talla)
    q = G3.quad_mundo(cam, (X, -h / 2, Z), (1, 0, 0), (0, 1, 0), 180, h, giro=3 * (rnd(int(X), 1) - 0.5))
    if q is not None:
        if alza < 0.999:                                   # aún sale: solo se ve la parte de arriba (la tumba sube)
            sub = G(t, lz.W, int(lz.H * alza) + 1, alfa=True)
            sub.im[:] = lz.im[:sub.H]
            sub.alfa[:] = lz.alfa[:sub.H]
            sub.ac[:] = lz.ac[:sub.H]
            lz = sub
        G3.estampar(c, lz, q, sombra=0.0)
    if t0 - 0.35 < t < t0 + 0.9:                           # tierra que salta
        for i in range(10):
            u = pr(t, t0 - 0.3, t0 + 0.9)
            ang = rnd(i, int(X)) * math.pi
            r = 160 * u
            px, py, zc = cam.pt(X + r * math.cos(ang) * 0.9, -260 * u * (1 - u) * 2.2 * (0.4 + rnd(i, 3)),
                                Z + 30 * math.sin(ang))
            c.circ(px, py, (4 + 5 * rnd(i, 5)) * cam.k(zc) * 0.5, TINTA, 1 - u)


def _tumba_vacia(c, cam, t):
    """La tumba SIN NOMBRE junto al tercer candelero: fosa abierta, montón de tierra y pala; la lápida sale a «final»."""
    X, Z = VACIA
    fosa = [(X - 100, 0, Z - 150), (X + 100, 0, Z - 150), (X + 100, 0, Z - 30), (X - 100, 0, Z - 30)]
    scr, _ = G3.proyectar(cam, fosa)
    if scr is not None:
        c.figura(scr, 0.92, contorno=2.4, ang=0, per=4.0)
    for i in range(7):                                     # montón de tierra al lado
        px, py, zc = cam.pt(X + 150 + 30 * rnd(i, 2), -18 * rnd(i, 3), Z - 140 + 110 * rnd(i, 4))
        c.figura(circ_pts(px, py, 26 * cam.k(zc), 12, 12 * cam.k(zc)), 0.6, contorno=1.4, ang=10, per=4.2, cruz=False)
    G3.trazo3d(c, cam, [(X + 190, 10, Z - 70), (X + 170, -230, Z - 60)], 9, afilado=0.0)
    p = cam.pt(X + 192, 6, Z - 70)
    k = cam.k(p[2])
    c.figura(np.float32([(p[0] - 22 * k, p[1] - 10 * k), (p[0] + 22 * k, p[1] - 10 * k), (p[0] + 18 * k, p[1] + 40 * k),
                         (p[0] - 18 * k, p[1] + 40 * k)]), 0.3, contorno=2.0, ang=90, per=4)
    alza = e_out(pr(t, A.g_final - 0.3, A.g_final + 0.4))
    if alza > 0.01:
        lz = F.relieve(t, lambda s, t_, cx, cy, e: None, 0.0, texto=None)
        lz.texto("AQVÍ YACE", 180, 270, 40, TINTA, "grab", 0.9)
        y_ = 330 + 3 * math.sin(t * 2)
        lz.trazo([(80, y_), (280, y_)], 1.4, op=0.6)
        if t > A.g_tu:                                      # a «tú»: aparece un signo tallado donde iría el nombre
            k2 = smooth(pr(t, A.g_tu, A.g_tu + 0.5))
            lz.texto("?", 180, 340, 70, TINTA, "gotica", 0.85 * k2)
        h = 250 * alza
        q = G3.quad_mundo(cam, (X, -h / 2, Z), (1, 0, 0), (0, 1, 0), 170, h, giro=-2)
        if q is not None:
            sub = G(t, lz.W, max(1, int(lz.H * alza)), alfa=True)
            sub.im[:] = lz.im[:sub.H]
            sub.alfa[:] = lz.alfa[:sub.H]
            sub.ac[:] = lz.ac[:sub.H]
            G3.estampar(c, sub, q, sombra=0.0)


def _fuerza_farol(i, t):
    t0 = FAROLES[i][3]
    tc = (A.g_cada, A.g_peor, A.g_anterior)[i]           # «cada una fue PEOR que la ANTERIOR»: cada llama crece más
    f = smooth(pr(t, t0, t0 + 0.35)) * (1 + (0.0, 0.3, 0.7)[i] * smooth(pr(t, tc, tc + 0.5)))
    if i == 2:
        f *= 1 - smooth(pr(t, A.g_tu + 0.05, A.g_tu + 0.4))
    return f


def cementerio(t, modo="gancho"):
    """Cuadro (sin acabado) del cementerio. modo: «gancho» (0:00-0:41) o «ciclo» (las almas que vuelven, 2:04-2:13)."""
    kf = KF_GANCHO if modo == "gancho" else KF_CICLO
    cam = C.camara(t, kf, L.CAM_A)
    hz = cam.horizonte()
    mx, my = 650 - 0.25 * cam.C[0] - 900 * math.sin(math.radians(cam_guinada(cam))), 170
    ax, ay, az = ANGEL

    def _revela(tt):
        return 1.0 if modo == "ciclo" else smooth(pr(tt, A.g_yo - 0.2, A.g_yo + 0.6))
    revela = _revela(t)

    # FONDO cacheado por tick de HERVOR (GR.fondo): cielo, luna, nubes, colinas y, con la cámara quieta, el suelo
    def f_cielo(cm):
        return cm.horizonte(), 650 - 0.25 * cm.C[0] - 900 * math.sin(math.radians(cam_guinada(cm))), 0.3 * cm.C[0]

    def cielo(g, tt):
        cm = C.camara(tt, kf, L.CAM_A)
        hz_ = cm.horizonte()
        GR.cielo(g, tt, hz_ + 70, tono_alto=1.0, tono_bajo=0.56)
        mx_ = 650 - 0.25 * cm.C[0] - 900 * math.sin(math.radians(cam_guinada(cm)))
        GR.luna(g, mx_, my, 74, tt, tono_cielo=0.86)
        G3.haz(g, mx_, my, 62, 22, 1100, tt, op=0.20)
        GR.nube(g, 1350 - 0.2 * cm.C[0], 120, 520, tt, sem=1, vel=5)
        GR.nube(g, 230 - 0.2 * cm.C[0], 300, 360, tt, sem=3, vel=4, tono=0.28)

    def cuervos(g):
        for i in range(3):
            cx = (300 + 520 * i + t * (38 + 9 * i)) % 2300 - 150
            GR.cuervo(g, cx, 230 + 60 * i + 14 * math.sin(t * 0.8 + i), 0.75 - 0.15 * i, t, fase=i * 2.1)

    def colinas(g, tt):
        cm = C.camara(tt, kf, L.CAM_A)
        hz_ = cm.horizonte()
        GR.colina(g, GR.perfil_colina(-60, 1980, hz_ + 10, 26, sem=1), tono=0.26, tono2=0.4, ang=-3, per=5.0,
                  contorno=1.6, cruz=False)
        if modo == "ciclo":                                # Forjaz en el horizonte, roja (la ciudad de la peste)
            cxm = 1500 - 0.3 * cm.C[0]
            GR.colina(g, np.float32([(cxm - 520, hz_ + 14), (cxm - 300, hz_ - 120), (cxm - 120, hz_ - 210),
                                     (cxm + 40, hz_ - 180), (cxm + 260, hz_ - 90), (cxm + 520, hz_ + 14)]), tono=0.5,
                      tono2=0.8, ang=-8, per=5, contorno=1.8)
            g.acento_luz(cxm, hz_ - 60, 420, SANGRE, 0.65 + 0.1 * math.sin(tt * 3))
            G3.particulas(g, tt, "ceniza", 30, (cxm - 400, hz_ - 300, cxm + 400, hz_ + 20), sem=4, op=0.7)
        else:
            with g.grupo(1500 - 0.3 * cm.C[0], hz_ + 12, 0.42):
                g.macizo([(-70, 0), (70, 0), (70, -120), (0, -190), (-70, -120)], 0.85)
                g.macizo([(70, 0), (150, 0), (150, -90), (70, -90)], 0.85)
                g.macizo([(-25, -190), (25, -190), (25, -300), (0, -330), (-25, -300)], 0.85)
                g.papel(circ_pts(0, -240, 9, 14, 13), 0.9)
                g.acento_luz(0, -240, 50, ORO, 0.7)

    def tono_suelo(a, b, zc):
        base = 0.62 + 0.06 * np.clip(b / 3000.0, 0, 1)
        sendero = np.clip(1 - np.abs(a - L._camino(b)) / (70 + 0.03 * b), 0, 1) * (b < 1500)
        return base - 0.34 * sendero

    def suelo(g, tt):
        G3.plano(g, C.camara(tt, kf, L.CAM_A), (-5000, 0, -800), (1, 0, 0), (0, 0, 1), 10000, 6000, tono_suelo,
                 familias=((0.0, 14.0),), luces=[(ax, 0, az, 950, 0.25 + 0.7 * _revela(tt))], oscuro=0.2)

    def firma_cielo(tt):
        return f_cielo(C.camara(tt, kf, L.CAM_A))

    def firma_suelo(tt):
        return G3.firma_cerca(C.camara(tt, kf, L.CAM_A)) + (100 * _revela(tt),)
    if modo == "gancho":                                   # los cuervos vuelan alto: nunca tapan las colinas
        g = GR.fondo(t, "cem_gancho", [(cielo, firma_cielo), (colinas, firma_cielo), (suelo, firma_suelo)])
        cuervos(g)
    else:                                                  # en el ciclo la Forjaz roja es alta: los cuervos van detrás
        g = GR.fondo(t, "cem_ciclo", [(cielo, firma_cielo)])
        cuervos(g)
        colinas(g, t)
        suelo(g, t)
    objs = []
    for i, (X, Z, fm, inc) in enumerate(TUMBAS):
        objs.append((X, 0, Z, lambda c, o=(Z, "tumba", X, fm, inc, i): L._objeto_cementerio(c, cam, o, t)))
    objs.append((-560, 0, 1500, lambda c: L._objeto_cementerio(c, cam, (1500, "arbol", -560), t)))
    for i in range(46):
        Z = 450 + 2600 * rnd(i, 21) ** 1.3
        X = (rnd(i, 22) - 0.5) * 1.3 * Z
        if any(math.hypot(X - x, Z - z) < 160 for x, z in LIBRE):
            continue
        objs.append((X, 0, Z, lambda c, o=(Z, "pasto", X, i): L._objeto_cementerio(c, cam, o, t)))
    objs.append((ax, 0, az, lambda c: L.angel(c, *cam.pt(ax, ay, az)[:2], 0.74 * cam.k(cam.pt(ax, ay, az)[2]), t,
                                              gloria=revela > 0.02, op=0.55 + 0.45 * revela)))
    if modo == "gancho":
        ac = _alma_corre(t)
        if ac:
            X, Z, op = ac
            objs.append((X, -150, Z, lambda c, X=X, Z=Z, op=op: (
                G3.sombra_contacto(c, cam, X, Z, 60, 22, op=0.35 * op, tono=0.6),
                GR.fantasma(c, *cam.pt(X, -150, Z)[:2], 0.5 * cam.k(cam.pt(X, -150, Z)[2]), t * 1.8, op=op, dirx=1))))
        # la procesión de los millones: almas lejanas que bajan de las colinas hacia el Ángel
        pro = C.env(t, A.g_millones - 1.4, A.g_cada, 1.2, 1.5)
        if pro > 0.01:
            for i in range(22):
                u = (t * 0.045 + i / 22) % 1.0
                X = -2000 + 2050 * u + 140 * (rnd(i, 7) - 0.5)
                Z = 2800 - 1200 * u + 200 * (rnd(i, 8) - 0.5)
                op = pro * min(1.0, u * 5) * min(1.0, (1 - u) * 6)
                objs.append((X, -150, Z, lambda c, X=X, Z=Z, op=op, i=i: GR.fantasma(
                    c, *cam.pt(X, -150, Z)[:2], 0.6 * cam.k(cam.pt(X, -150, Z)[2]), t, fase=i * 1.3, op=op)))
        for i, (X, Z, icono, t0) in enumerate(RELIEVES):
            if t0 - 0.4 < t < A.g_tres:
                objs.append((X, 0, Z, lambda c, X=X, Z=Z, icono=icono, t0=t0: _tumba_relieve(c, cam, X, Z, icono, t0, t)))
                nom, alto = PEG_MUERTOS[i]                 # el muerto REAL de esa tumba se alza detrás (pegatina)
                C.peg(objs, cam, t, nom, X + 30, Z + 110, alto, alza=smooth(pr(t, t0 - 0.1, t0 + 0.45)),
                      op=1 - smooth(pr(t, A.g_tres - 0.5, A.g_tres)), espejo=i == 2, sem=40 + i)
        if t > A.g_final - 0.4:
            objs.append((VACIA[0], 0, VACIA[1], lambda c: _tumba_vacia(c, cam, t)))
    else:                                                  # el ciclo: llegan, resucitan, vuelven, caen
        cic = C.env(t, A.TR_CEM, None, 0.5)
        for i in range(9):
            p = (t * 0.16 + i / 9) % 1.0
            if p < 0.45:                                   # alma que vuela al Ángel
                u = smooth(p / 0.45)
                X, Z = -1300 + 1400 * u, 2700 - 1300 * u
                objs.append((X, -150, Z, lambda c, X=X, Z=Z, i=i: GR.fantasma(
                    c, *cam.pt(X, -150, Z)[:2], 0.48 * cam.k(cam.pt(X, -150, Z)[2]), t, fase=i, op=cic)))
            elif p < 0.52:                                 # resucita: destello en la gloria
                u = (p - 0.45) / 0.07
                sx, sy, zc = cam.pt(ax - 120, -200, az - 60)
                objs.append((ax - 120, -200, az - 60, lambda c, sx=sx, sy=sy, u=u: (
                    c.acento_luz(sx, sy, 260 * (0.5 + u), ESPECTRO, 0.9 * (1 - u) * cic),
                    c.circ(sx, sy, 40 * (1 - u) + 6, c.fondo_papel, 0.8 * (1 - u) * cic))))
            else:                                          # vuelve andando a la ciudad roja... y cae
                u = (p - 0.52) / 0.48
                X, Z = ax - 60 + 1400 * u, az + 100 + 1300 * u
                cae = smooth(pr(u, 0.82, 1.0))
                if i % 3 == 1:                             # uno de cada tres: personaje REAL (pegatina) que cae
                    nom, alto = PEG_CICLO[(i // 3) % len(PEG_CICLO)]
                    C.peg(objs, cam, t, nom, X, Z, alto, aura=cae, alza=1 - 0.97 * cae, op=cic, sem=50 + i,
                          Y=-8 * abs(math.sin(t * 5 + i)) * (1 - cae))
                    continue
                objs.append((X, 0, Z, lambda c, X=X, Z=Z, cae=cae, i=i: F.persona(
                    c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, ("capa", "enano", "guerrero")[i % 3],
                    fase=i, anda=1.0 - cae, dirx=1, cae=cae, aura=cae, op=cic, sem=i)))
    C.figuras(g, cam, objs)
    # los candeleros de las tres noches (delante del Ángel)
    luces = [(mx, my, 760, 0.55)]
    sx, sy, zc = cam.pt(ax, ay - 250, az)
    luces.append((sx, sy, 900 * cam.k(zc) * (0.3 + 0.7 * revela), 0.4 + 0.55 * revela))
    if modo == "gancho" and t > A.g_tres - 0.6:
        for i, (X, Z, col, t0, num) in enumerate(FAROLES):
            ap = smooth(pr(t, A.g_tres - 0.6, A.g_tres - 0.1))
            if ap <= 0.01:
                continue
            fz = _fuerza_farol(i, t)
            fx, fy, k = F.farol(g, cam, X, Z, t, col, fz, sem=i, alto=1.0)
            b = cam.pt(X, 0, Z)
            g.texto(num, b[0], b[1] + 26 * k, max(12, int(30 * k)), TINTA, "gara_b", 0.9 * ap)
            if fz > 0.02:
                luces.append((fx, fy, 340 * k * fz, 0.6 * fz, col))
    G3.iluminar(g, luces, amb=0.16, fuerza=0.58, acento=0.10)
    G3.particulas(g, t, "polvo", 70, (sx - 600, sy - 400, sx + 600, sy + 500), sem=2)
    for zmin in (2000, 1000, 420):
        y_nb = cam.pt(cam.C[0], 0, cam.C[2] + zmin)[1]
        GR.niebla(g, y_nb - 40, y_nb + 12, t, op=0.4, sem=int(zmin), vel=22)
    # primer plano: hierba y dos tumbas enormes, fuera de foco (relativas a la cámara: siempre enmarcan)
    with G3.capa_prof(g, cam, 230) as c:
        x0, z0 = cam.C[0], cam.C[2]
        for i in range(9):
            px, py, zc = cam.pt(x0 - 330 + 80 * i, 0, z0 + 300 + 60 * rnd(i, 5))
            GR.pasto(c, px, py, 0.9 * cam.k(zc), t, n=8, sem=i)
        px, py, zc = cam.pt(x0 - 215, 0, z0 + 340)
        GR.lapida(c, px, py, 0.95 * cam.k(zc), "arco", 7, tono=0.8, tono2=0.97, sem=31)
        px, py, zc = cam.pt(x0 + 255, 0, z0 + 400)
        GR.pasto(c, px, py, 1.5 * cam.k(zc), t, n=14, sem=40)
    return g


def cam_guinada(cam):
    return math.degrees(math.atan2(float(cam.F[0]), float(cam.F[2])))
