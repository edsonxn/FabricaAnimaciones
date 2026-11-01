# -*- coding: utf-8 -*-
"""Decorado 3: FORJAZ (acento SANGRE). La gran sala de la fragua de la lámina B aprobada (look.py), pero viva: la multitud que
llega de Zul'Gurub, el recuerdo real de Orgrimmar, el cazador que suelta al lobo y la sangre que sale con él (1:24-1:36), el de
nivel máximo que aguanta y el de nivel bajo que cae (1:36-1:44), el mercader que te vende una espada y te pasa la muerte
(1:44-1:54), la danza macabra sobre un suelo blanco de huesos con el recuerdo real de Forjaz (1:54-2:03) y las almas que suben.
Decorado 4: las AFUERAS de Forjaz, nevadas (2:13-2:51): el médico de la peste, el que huye al bosque, el que avisa en la
puerta, el sanador que mantiene vivo al contagioso, la cuarentena que saltan, el que corre a la multitud."""
import math

import numpy as np

import anclas as A
import comun as C
import fig as F
import grabado as GR
import grabado_3d as G3
import look as L
from grabado import ESPECTRO, HIELO, ORO, SANGRE, TINTA, G, circ_pts, e_out, lerp, pr, rnd, smooth

# ------------------------------------------------------------------ la sala de Forjaz
KF_FORJAZ = [(A.TR_FORJAZ, dict(x=0.0, y=-175.0, z=-80.0, guinada=0.0, cabeceo=-3.0, foco=1000.0)),
             (A.m_orgrimmar + 0.4, dict(x=70.0, y=-175.0, z=40.0, guinada=7.0, cabeceo=-3.0, foco=1250.0)),
             (A.m_llamaban, dict(x=-40.0, y=-185.0, z=120.0, guinada=-3.0, cabeceo=-2.0, foco=800.0)),
             (A.m_salio + 0.8, dict(x=-30.0, y=-182.0, z=160.0, guinada=-1.5, cabeceo=-2.0, foco=900.0)),
             (A.c_maximo, dict(x=-20.0, y=-180.0, z=200.0, guinada=0.0, cabeceo=-2.0, foco=1120.0)),
             (A.c_instante + 0.6, dict(x=0.0, y=-180.0, z=250.0, guinada=0.0, foco=1050.0)),
             (A.c_vendian - 1.0, dict(x=160.0, y=-180.0, z=330.0, guinada=11.0, foco=900.0)),
             (A.c_muerte + 0.6, dict(x=190.0, y=-180.0, z=390.0, guinada=12.0, foco=820.0)),
             (A.c_cientos, dict(x=20.0, y=-180.0, z=320.0, guinada=-3.0, cabeceo=-3.0, foco=1050.0)),
             (A.c_fantasmas, dict(x=0.0, y=-175.0, z=470.0, guinada=0.0, cabeceo=-7.0)),
             (A.TR_CEM + 0.6, dict(x=0.0, y=-175.0, z=520.0, guinada=0.0, cabeceo=-9.0))]
CAZ = (-90.0, 900.0)
SPLASH = (-40.0, 1050.0)
FUERTE, DEBIL = (-230.0, 1330.0), (170.0, 1280.0)
PUESTO = (440.0, 1250.0)
MERCADER = (480.0, 1180.0)
COMPRADOR = (230.0, 1180.0)


def _gente():
    """La multitud de Forjaz: (X, Z, tipo, fase). Se quitan los sitios de los protagonistas."""
    out = []
    for i in range(22):
        X = -580 + 1160 * rnd(i, 51)
        Z = 1080 + 1250 * rnd(i, 52)
        if any(math.hypot(X - x, Z - z) < 170 for x, z in (CAZ, FUERTE, DEBIL, MERCADER, COMPRADOR, SPLASH, PUESTO)):
            continue
        if abs(X) > 520 and abs(Z - 1400) < 120:
            continue
        tipo = ("enano", "capa", "enano", "guerrero", "mercader")[i % 5]
        if i % 3 == 0:                                     # uno de cada tres: personaje REAL de WoW (pegatina)
            tipo = "peg:" + PEG_GENTE[(i // 3) % len(PEG_GENTE)][0]
        out.append((X, Z, tipo, i))
    return out


# pegatinas reales (render oficial de Wowhead) y su alto en el mundo (persona dibujada ≈ 360; enano ≈ 270)
PEG_GENTE = [("Ironforge Mountaineer", 285), ("Brother Paxton", 365), ("Thalgus Thunderfist", 270),
             ("Stormwind City Guard", 375), ("Ironforge Guard", 290), ("High Tinker Mekkatorque", 200)]
PEG_ALTO = dict(PEG_GENTE)
# el rey y su guardia ante la fragua + dos guardias cerca de la cámara, a los lados: (PNJ, X, Z, espejo, alto)
PEG_SALA = [("King Magni Bronzebeard", -170, 2280, False, 330), ("Ironforge Guard", -470, 2330, False, 290),
            ("Ironforge Guard", 430, 2330, True, 290), ("Ironforge Guard", -450, 760, False, 290),
            ("Ironforge Mountaineer", 430, 830, True, 285)]


GENTE = _gente()


def _contagio(i, X, Z):
    """Instante en que cada persona de la multitud se contagia (la sangre se extiende desde el lobo)."""
    d = math.hypot(X - SPLASH[0], Z - SPLASH[1])
    return A.m_salio + 0.1 + d / 260.0


def _huesos_suelo(c, cam, X, Z, t, i, s=1.0):
    a_ = rnd(i, 87) * 3.1416
    p0 = cam.pt(X - 45 * s * math.cos(a_), -8, Z - 45 * s * math.sin(a_))
    p1 = cam.pt(X + 45 * s * math.cos(a_), -8, Z + 45 * s * math.sin(a_))
    G3.sombra_contacto(c, cam, X, Z, 50 * s, 22 * s, op=0.6)
    GR._hueso(c, p0[:2], p1[:2], 10 * s * cam.k(p0[2]))
    if i % 2 == 0:
        px, py, zc = cam.pt(X + 60 * s, 0, Z - 30 * s)
        GR.craneo(c, px, py - 20 * s * cam.k(zc), 21 * s * cam.k(zc), t, ang=0.5 * (rnd(i, 85) - 0.5), mand=0.3 * rnd(i, 86))


def forjaz(t):
    cam = C.camara(t, KF_FORJAZ, L.CAM_B)
    fragua = (0, -220, 2700)
    luces = [(fragua[0], fragua[1], fragua[2], 2300, 1.0), (-640, -380, 1300, 520, 0.7), (640, -380, 1300, 520, 0.7)]

    def _blanco(tt):                                       # «el suelo estaba BLANCO de huesos»
        return smooth(pr(tt, A.c_blanco - 0.5, A.c_huesos + 0.6))
    blanco = _blanco(t)

    def sala(g, tt):                                       # techo, muros, suelo y arcos: solo dependen de la cámara
        cm = C.camara(tt, KF_FORJAZ, L.CAM_B)
        bl = _blanco(tt)
        g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.92, ang=10, per=6.0)
        G3.plano(g, cm, (-700, -950, -300), (1, 0, 0), (0, 0, 1), 1400, 2900, 0.93, familias=((90.0, 12.0), (0.0, 16.0)),
                 patron=("losas", 260), luces=luces, oscuro=0.1, junta=6)
        for X in (-700, 700):
            G3.plano(g, cm, (X, -950, -300), (0, 0, 1), (0, 1, 0), 2900, 950, 0.48, familias=((0.0, 9.0), (60.0, 12.0)),
                     patron=("sillares", 200, 95), quiebre=0.35, tramo=55, luces=luces, oscuro=0.5, junta=5)
        G3.plano(g, cm, (-700, 0, -300), (1, 0, 0), (0, 0, 1), 1400, 2900, 0.3 - 0.12 * bl, familias=((0.0, 9.0),),
                 patron=("losas", 180), luces=luces, oscuro=0.4 - 0.15 * bl, junta=5, quiebre=0.3, tramo=50)
        G3.plano(g, cm, (-700, -950, 2660), (1, 0, 0), (0, 1, 0), 1400, 950, 0.45, familias=((0.0, 9.0), (60.0, 12.0)),
                 patron=("sillares", 200, 95), quiebre=0.35, tramo=55, luces=luces, oscuro=0.4, junta=5)
        for k_, Z in enumerate((2655, 3000, 3400)):
            aw, ah = 540 - 80 * k_, 900 - 100 * k_
            arc3 = [(-aw, 0, Z)] + [(aw * math.cos(u), -(ah - aw) - aw * math.sin(u), Z)
                                    for u in np.linspace(math.pi, 0, 26)] + [(aw, 0, Z)]
            scr, _ = G3.proyectar(cm, arc3)
            if scr is not None:
                g.figura(scr, 0.94 - 0.04 * k_, contorno=3.0 - 0.6 * k_, ang=0, per=5.0, cruz=False)
    # FONDO cacheado por tick de HERVOR (GR.fondo): con la cámara quieta, la sala entera cuesta una copia
    g = GR.fondo(t, "forjaz", [(sala, lambda tt: G3.firma_cerca(C.camara(tt, KF_FORJAZ, L.CAM_B)) + (300 * _blanco(tt),))])
    fx, fy, fz = cam.pt(0, -60, 3500)
    for i, dx in enumerate((-140, 0, 140)):
        px, py, zc = cam.pt(dx * 1.6, 0, 3500)
        GR.llama(g, px, py, 3.2 * cam.k(zc) * 2.2, t, sem=i, color=ORO)
    g.acento_luz(fx, fy, 420, ORO, 0.75)
    G3.particulas(g, t, "brasas", 40, (fx - 260, fy - 520, fx + 260, fy + 40), sem=5)
    for lado, Zc in ((-1, 1050), (1, 1050), (-1, 1800), (1, 1800)):
        if lado > 0 and Zc == 1050 and A.m_orgrimmar - 0.6 < t < A.m_gente + 0.8:
            continue                                       # ahí cuelga el recuerdo de Orgrimmar
        if lado < 0 and Zc == 1050 and A.c_calles - 0.6 < t < A.c_jugador + 0.9:
            continue                                       # ahí cuelga el recuerdo de Forjaz
        q = G3.quad_mundo(cam, (lado * 698, -560, Zc), (0, 0, -lado), (0, 1, 0), 260, 420)
        if q is not None:
            G3.estampar(g, L._estandarte(t, lado), q, sombra=0.5, off=(10 * -lado, 14))
    # sangre en el suelo: la mancha que sale con el lobo y crece; luego charcos por toda la sala
    sang = smooth(pr(t, A.m_salio - 0.1, A.m_salio + 2.5))
    if sang > 0.01:
        for i in range(1 + int(9 * smooth(pr(t, A.m_salio, A.c_cientos)))):
            X, Z = (SPLASH if i == 0 else (-520 + 1040 * rnd(i, 81), 600 + 1500 * rnd(i, 82)))
            r = (260 * sang if i == 0 else (70 + 50 * rnd(i, 83)) * smooth(pr(t, A.m_salio + 0.4 * i, A.m_salio + 0.4 * i + 1.0)))
            if r < 2:
                continue
            pts = GR.silueta_ruido(circ_pts(0, 0, r, 34, r * 0.7), 12, sem=i)
            scr, _ = G3.proyectar(cam, np.stack([X + pts[:, 0], np.zeros(len(pts)), Z + pts[:, 1]], 1))
            if scr is not None:
                g.acento(scr, SANGRE, 0.85, aspero=0.0)
    objs = [(X * 640 / abs(X), -400, Z, lambda c, X=X, Z=Z: L._columna(c, cam, X * 640 / abs(X), Z, luces))
            for X in (-1, 1) for Z in (700, 1400, 2150)]
    # el rey Magni y su guardia ante la fragua (pegatinas reales); la guardia también cae con los cientos
    caen = smooth(pr(t, A.c_cientos - 0.5, A.c_huesos))
    for j, (nom, X, Z, esp, alto) in enumerate(PEG_SALA):
        t_c = A.c_cientos + 1.2 + 0.9 * j
        cae_j = smooth(pr(t, t_c, t_c + 0.6))
        if cae_j < 0.999:
            C.peg(objs, cam, t, nom, X, Z, alto, aura=smooth(pr(t, A.c_portadores, A.c_portadores + 1)),
                  alza=1 - 0.97 * cae_j, espejo=esp, sem=60 + j)
        else:
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, j=j: _huesos_suelo(c, cam, X, Z, t, 70 + j)))
    # la multitud
    for X, Z, tipo, i in GENTE:
        tc = _contagio(i, X, Z)
        aura = smooth(pr(t, tc, tc + 0.4)) if t > A.m_salio else 0.0
        huye = smooth(pr(t, A.m_salio, A.m_salio + 1.2)) * (1 - smooth(pr(t, A.c_maximo, A.c_maximo + 2)))
        dxh = (X - SPLASH[0]) / (abs(X - SPLASH[0]) + 1)
        Xp = X + 120 * huye * dxh + 25 * math.sin(t * 0.4 + i)
        muere = caen * (rnd(i, 55) < 0.7)
        t_cae = A.c_cientos + 4.5 * rnd(i, 56)
        cae = smooth(pr(t, t_cae, t_cae + 0.7)) if muere else 0.0
        if cae >= 0.999:
            objs.append((Xp, 0, Z, lambda c, Xp=Xp, Z=Z, i=i: _huesos_suelo(c, cam, Xp, Z, t, i)))
            continue
        if tipo.startswith("peg:"):                        # personaje real: recorte de papel que cae de espaldas
            corre = 0.3 + 1.5 * huye
            C.peg(objs, cam, t, tipo[4:], Xp, Z, PEG_ALTO[tipo[4:]], Y=-9 * abs(math.sin(t * 5 + i)) * min(1.0, corre - 0.3),
                  aura=aura, alza=1 - 0.97 * cae, espejo=bool(i % 2), sem=i)
            continue
        objs.append((Xp, 0, Z, lambda c, Xp=Xp, Z=Z, tipo=tipo, i=i, aura=aura, cae=cae, huye=huye, dxh=dxh: F.persona(
            c, *cam.pt(Xp, 0, Z)[:2], 0.95 * cam.k(cam.pt(Xp, 0, Z)[2]), t, tipo, fase=i, anda=0.3 + 1.5 * huye,
            dirx=1 if (dxh > 0 if huye > 0.1 else i % 2) else -1, aura=aura, cae=cae, sem=i)))
    # el cazador: abre la jaula a «la llamaban»; el lobo salta con la sangre
    if t < A.c_maximo + 1:
        abre = smooth(pr(t, A.m_llamaban - 0.1, A.m_llamaban + 0.4))
        X, Z = CAZ
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, abre=abre: (F.persona(c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, "cazador",
                                                   anda=0.0, dirx=1, sem=21, brazos=(0.3, 1.2 + 0.4 * abre)),
                                         F.jaula(c, *cam.pt(X + 95, -300, Z - 10)[:2], 0.9 * cam.k(cam.pt(X, 0, Z)[2]), t,
                                                 sangre=1.0 - abre, abre=abre))))
        salto = pr(t, A.m_sangre - 0.15, A.m_salio + 0.6)
        if salto > 0:
            lx = lerp(X + 120, SPLASH[0] + 140, salto)
            lz = lerp(Z - 20, SPLASH[1], salto)
            ly = -260 * math.sin(math.pi * min(1.0, salto * 1.3)) * (salto < 0.77)
            objs.append((lx, ly, lz, lambda c, lx=lx, ly=ly, lz=lz: F.lobo(
                c, *cam.pt(lx, ly, lz)[:2], 0.95 * cam.k(cam.pt(lx, 0, lz)[2]), t, anda=1.0, dirx=1, ojo=1.0, grune=1.0,
                aura=1.0)))
    # nivel máximo contra nivel bajo
    if A.c_maximo - 1.6 < t < A.c_vendian:
        op = C.env(t, A.c_maximo - 1.6, A.c_vendian - 0.8, 0.6, 0.6)
        X, Z = FUERTE
        tambalea = 0.12 * smooth(pr(t, A.c_aguantaba, A.c_aguantaba + 0.5)) * (0.6 + 0.4 * math.sin(t * 3))
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, op=op, tambalea=tambalea: F.persona(c, *cam.pt(X, 0, Z)[:2], 1.12 * cam.k(cam.pt(X, 0, Z)[2]), t, "guerrero",
                                                  anda=0.0, dirx=1, aura=1.0, cae=tambalea, op=op, sem=31,
                                                  brazos=(0.4, 1.1))))
        X2, Z2 = DEBIL
        cae = smooth(pr(t, A.c_instante - 0.1, A.c_instante + 0.35))
        if cae < 0.999:
            objs.append((X2, 0, Z2, lambda c, X2=X2, Z2=Z2, cae=cae, op=op: F.persona(c, *cam.pt(X2, 0, Z2)[:2], 0.6 * cam.k(cam.pt(X2, 0, Z2)[2]), t,
                                                        "capa", anda=0.0, dirx=-1, aura=1.0, cae=cae, op=op, sem=32)))
        else:
            objs.append((X2, 0, Z2, lambda c, X2=X2, Z2=Z2: _huesos_suelo(c, cam, X2, Z2, t, 2, 0.7)))
    # el mercader portador: te vende una espada y te pasa la muerte
    if A.c_contagiaban - 2 < t < A.c_blanco:
        op = C.env(t, A.c_contagiaban - 2, A.c_cientos + 0.5, 0.6, 0.8)
        objs.append((PUESTO[0], -200, PUESTO[1] + 60, lambda c, op=op: F.puesto(c, cam, PUESTO[0], PUESTO[1] + 60, t, op=op)))
        X, Z = MERCADER
        da = smooth(pr(t, A.c_espada - 0.3, A.c_espada + 0.3))
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, op=op, da=da: F.persona(c, *cam.pt(X, 0, Z)[:2], 0.8 * cam.k(cam.pt(X, 0, Z)[2]), t, "enano",
                                                  anda=0.0, dirx=-1, aura=smooth(pr(t, A.c_portadores - 0.3,
                                                                                    A.c_portadores + 0.3)),
                                                  brazos=(0.3, 0.3 + 1.2 * da), op=op, sem=41)))
        X2, Z2 = COMPRADOR
        llega = smooth(pr(t, A.c_vendian - 1.6, A.c_vendian))
        Xc = lerp(X2 - 260, X2, llega)
        muerte = smooth(pr(t, A.c_muerte - 0.1, A.c_muerte + 0.4))

        def comprador(c, Xc=Xc, X=X, Z=Z, Z2=Z2, op=op, da=da, muerte=muerte, llega=llega):
            px, py, zc = cam.pt(Xc, 0, Z2)
            k = cam.k(zc)
            if muerte < 1:
                F.persona(c, px, py, 0.95 * k, t, "capa", anda=1.0 if 0 < llega < 1 else 0.0, dirx=1,
                          brazos=(0.3, 0.3 + 1.1 * da), op=op * (1 - muerte), sem=42, aura=smooth(pr(t, A.c_espada + 0.3,
                                                                                                  A.c_muerte)))
            if muerte > 0:
                GR.esqueleto(c, px, py, 0.92 * k, dict(GR.POSE_QUIETO, hd=1.2, cd=0.2, mand=0.4), t, op=op * muerte)
                c.acento_luz(px, py - 200 * k, 260 * k, SANGRE, 0.6 * muerte * op)
            if da > 0.01:                                  # la espada entre las dos manos, con el hilo de sangre
                a = cam.pt(X - 70, -265, Z)
                b = cam.pt(Xc + 50, -270, Z2)
                v = np.float32(b[:2]) - np.float32(a[:2])
                n_ = np.float32((-v[1], v[0])) / (np.linalg.norm(v) + 1e-6)
                A_, B_ = np.float32(a[:2]), np.float32(b[:2])
                hoja = [A_ + n_ * 9 * k, B_ - v * 0.22 + n_ * 9 * k, B_ - v * 0.22 - n_ * 9 * k, A_ - n_ * 9 * k,
                        A_ - v * 0.08]
                c.figura(np.float32(hoja), 0.05, contorno=2.2, op=op * da, tono2=0.5, luz=90, ang=0, per=3.6, cruz=False)
                g_ = B_ - v * 0.22
                c.trazo([g_ + n_ * 34 * k, g_ - n_ * 34 * k], 9 * k ** 0.6, op=op * da, afilado=0.0)
                c.trazo([g_, B_], 8 * k ** 0.6, op=op * da, afilado=0.0)
                h = smooth(pr(t, A.c_espada + 0.2, A.c_muerte))
                if 0 < h < 1:
                    c.acento_luz(lerp(a[0], b[0], h), lerp(a[1], b[1], h), 50 * k, SANGRE, 0.95)
        objs.append((Xc, 0, Z2, comprador))
    # la danza macabra: esqueletos que bailan sobre los huesos
    dz = smooth(pr(t, A.c_cientos - 0.4, A.c_cientos + 0.6))
    if dz > 0.01:
        for i, (X, Z, ph) in enumerate(((-260, 1250, 0.0), (40, 1000, 2.1), (330, 1180, 4.2), (-120, 1650, 1.0),
                                        (220, 1800, 3.0))):
            def esq(c, X=X, Z=Z, ph=ph, i=i):
                px, py, zc = cam.pt(X, 0, Z)
                cc = G3.nueva_capa(c)
                GR.esqueleto_baila(cc, px, py, 0.9 * cam.k(zc), t, ph, op=dz)
                G3.sombra_capa(c, cc, (px, py), dirx=(px - fx) / 900, diry=0.55, largo=1.0, op=0.8 * dz)
                G3.sombra_contacto(c, cam, X, Z, 70, 26, op=0.9 * dz)
                GR.componer(c, cc)
            objs.append((X, 0, Z, esq))
        n = int(26 * smooth(pr(t, A.c_cientos, A.c_huesos + 0.4)))
        for i in range(n):
            X, Z = -560 + 1120 * rnd(i, 91), 600 + 1600 * rnd(i, 92)
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: _huesos_suelo(c, cam, X, Z, t, i + 10)))
    # las almas que se levantan de los huesos y corren al cementerio
    al = pr(t, A.c_fantasmas - 0.6, A.TR_CEM)
    if al > 0:
        for i in range(9):
            X, Z = -480 + 960 * rnd(i, 95), 800 + 1100 * rnd(i, 96)
            u = smooth(min(1.0, al * 1.4 - i * 0.04))
            Y = -100 - 500 * u
            Zp = Z - 600 * u
            objs.append((X, Y, Zp, lambda c, X=X, Y=Y, Zp=Zp, i=i, u=u: GR.fantasma(
                c, *cam.pt(X, Y, Zp)[:2], 0.55 * cam.k(cam.pt(X, Y, Zp)[2]), t, fase=i, op=min(1.0, u * 4))))
    C.figuras(g, cam, objs)
    # recuerdos reales colgados: Orgrimmar (Solarnova, 2005) y Forjaz (Wyvers, 2005)
    op = C.env(t, A.m_orgrimmar - 0.3, A.m_gente + 0.4, 0.4, 0.5)
    if op > 0.01:
        for sg in (-1, 1):
            G3.trazo3d(g, cam, [(420 + sg * 240 * 0.9, -950, 1500 - sg * 240 * 0.44),
                                (420 + sg * 240 * 0.9, -800, 1500 - sg * 240 * 0.44)], 3.0, afilado=0.0, op=op)
    C.recuerdo_colgado(g, cam, (420, -560 + 8 * math.sin(t), 1500), (0.9, 0, -0.44), "_crudos/70GmXTKiIss", 14.0 + (t - A.m_orgrimmar), t,
                       ancho=520, alto=390, texto="Orgrimmar · MMV", op=op, z=1.5, cx=0.45, cy=0.42, sem=4)
    op = C.env(t, A.c_calles - 0.3, A.c_jugador + 0.5, 0.4, 0.5)
    if op > 0.01:
        for sg in (-1, 1):
            G3.trazo3d(g, cam, [(-420 + sg * 240 * 0.9, -950, 1500 + sg * 240 * 0.44),
                                (-420 + sg * 240 * 0.9, -800, 1500 + sg * 240 * 0.44)], 3.0, afilado=0.0, op=op)
    C.recuerdo_colgado(g, cam, (-420, -560 + 8 * math.sin(t), 1500), (0.9, 0, 0.44), "_crudos/RxDvxKeLWlA", 36.0 + (t - A.c_calles), t,
                       ancho=520, alto=390, texto="Forjaz · Septiembre de MMV", op=op, z=1.3, cx=0.5, cy=0.5, sem=5)
    G3.haz(g, fx, fy - 120, 90, 70, 900, t, op=0.22)
    lc = []
    for X in (-640, 640):
        p = cam.pt(X, -380, 1300)
        lc.append((p[0], p[1], 380, 0.6))
    G3.iluminar(g, [(fx, fy, 1250, 1.0, ORO)] + lc, amb=0.14 + 0.1 * blanco, fuerza=0.6, acento=0.25)
    G3.particulas(g, t, "polvo", 50, (fx - 500, fy - 200, fx + 500, 1080), sem=7)
    # la cartela de la ciudad cuelga del techo («Forjaz»)
    op = C.env(t, A.m_forjaz - 0.25, A.c_aguantaba, 0.35, 0.6)
    C.cartela_colgada(g, cam, (0, -560 + 6 * math.sin(t * 0.9), 1300), "Forjaz", t, ancho=520, alto=140, px=58, op=op,
                      techo=-950)
    # primer plano: un esqueleto enorme y desenfocado que baila a la izquierda (cuando empieza la danza)
    if dz > 0.01:
        with G3.capa_prof(g, cam, 480) as c:
            px, py, zc = cam.pt(cam.C[0] - 250, 0, cam.C[2] + 480)
            GR.esqueleto(c, px, py, 0.95 * cam.k(zc), GR.pose_danza(t, 5.0, vel=0.9), t, op=dz)
    else:
        with G3.capa_prof(g, cam, 420) as c:                # primer plano: un enano de espaldas, fuera de foco
            px, py, zc = cam.pt(cam.C[0] + 300, 0, cam.C[2] + 420)
            F.persona(c, px, py, 0.8 * cam.k(zc), t, "enano", anda=0.2, dirx=-1, sem=60,
                      aura=smooth(pr(t, A.m_salio + 1.2, A.m_salio + 1.8)))
    return g


# ------------------------------------------------------------------ las afueras de Forjaz (nieve)
CAM_F = dict(x=0.0, y=-190.0, z=0.0, guinada=0.0, cabeceo=-1.5, f=1450.0, foco=1100.0, apertura=4.0, bruma=0.45,
             lejos=3600.0)
KF_CAMPO = [(A.TR_CAMPO - 0.8, dict(x=0.0, y=-190.0, z=-140.0, guinada=0.0)),
            (A.h_huyeron - 0.4, dict(x=-30.0, y=-190.0, z=-20.0, guinada=0.0, foco=900.0)),
            (A.h_bosques + 0.6, dict(x=-80.0, y=-190.0, z=30.0, guinada=-15.0, foco=1500.0)),
            (A.h_puertas, dict(x=-20.0, y=-195.0, z=80.0, guinada=9.0, foco=2600.0)),
            (A.h_avisando + 1.0, dict(x=20.0, y=-195.0, z=120.0, guinada=11.0, foco=2600.0)),
            (A.h_sanadores + 0.3, dict(x=0.0, y=-195.0, z=160.0, guinada=0.0, foco=1200.0)),
            (A.h_puso, dict(x=0.0, y=-205.0, z=240.0, guinada=0.0, foco=1350.0)),
            (A.h_otros2, dict(x=0.0, y=-215.0, z=300.0, guinada=0.0, foco=1500.0)),
            (A.h_huir, dict(x=40.0, y=-230.0, z=560.0, guinada=4.0, foco=2200.0)),
            (A.TR_HAKKAR + 0.6, dict(x=60.0, y=-235.0, z=640.0, guinada=5.0, foco=2300.0))]
PUERTA = (650.0, 2700.0)
MEDICO = ((420.0, 750.0), (-260.0, 760.0))
BARRERA = (0.0, 1500.0, 1300.0)


def _pinos():
    out = []
    for i in range(36):
        X = -700 - 2600 * rnd(i, 71)
        Z = 700 + 3000 * rnd(i, 72)
        out.append((X, Z, 0.8 + 0.6 * rnd(i, 73), i))
    for i in range(10):
        X = 1500 + 1800 * rnd(i, 74)
        Z = 1500 + 2200 * rnd(i, 75)
        out.append((X, Z, 0.7 + 0.5 * rnd(i, 76), 40 + i))
    return out


PINOS = _pinos()


def _puerta_ciudad(g, cam, t, luces):
    """La puerta de Forjaz excavada en el acantilado: muro de roca, arco oscuro, dos estatuas-pilar y braseros."""
    perfil = [(-4000, -700)] + [(x_, -820 - 180 * math.sin(x_ / 900.0) - 90 * math.sin(x_ / 310.0)) for x_ in
                                np.linspace(-3800, 3800, 30)] + [(4000, -700), (4000, 0), (-4000, 0)]
    scr, _ = G3.proyectar(cam, [(x_, y_, PUERTA[1]) for x_, y_ in perfil])
    if scr is not None:                                   # el acantilado: masa de roca con borde quebrado y nieve arriba
        g.figura(scr, lambda X_, Y_: 0.55 + 0.25 * np.clip((Y_ - scr[:, 1].min()) / 500.0, 0, 1), contorno=3.0, ang=78,
                 per=5.5, cruz=False)
        cima = scr[1:31]
        g.trazo(cima + np.float32((0, 6)), 9, color=g.fondo_papel, op=0.85, afilado=0.2)
    X, Z = PUERTA
    arco = [(X - 260, 0, Z - 2)] + [(X + 260 * math.cos(u), -420 - 260 * math.sin(u), Z - 2)
                                    for u in np.linspace(math.pi, 0, 24)] + [(X + 260, 0, Z - 2)]
    scr, _ = G3.proyectar(cam, arco)
    if scr is not None:
        g.figura(scr, 0.97, contorno=6.0, ang=0, per=5)
        g.acento_luz(*scr.mean(0), 300, ORO, 0.35)
    for sg in (-1, 1):                                    # pilares tallados con forma de guerrero enano
        G3.plano(g, cam, (X + sg * 330 - 70, -900, Z - 60), (1, 0, 0), (0, 1, 0), 140, 900, 0.35,
                 familias=((90.0, 9.0), (0.0, 14.0)), quiebre=0.3, luces=luces, oscuro=0.4, contorno=2.4)
        p = cam.pt(X + sg * 330, -960, Z - 60)
        GR.craneo(g, p[0], p[1], 46 * cam.k(p[2]), t, tono=0.3)
    for sg in (-1, 1):
        p = cam.pt(X + sg * 470, -170, Z - 120)
        k = cam.k(p[2])
        G3.trazo3d(g, cam, [(X + sg * 470, 0, Z - 120), (X + sg * 470, -170, Z - 120)], 18, afilado=0.0)
        for j in range(3):
            GR.llama(g, p[0] + (j - 1) * 26 * k, p[1], (1.6 - 0.4 * abs(j - 1)) * k, t, sem=sg * 5 + j, color=ORO)
        G3.humo(g, p[0], p[1] - 120 * k, 0.9 * k, t, sem=sg, op=0.4, alto=260)


def campo(t):
    cam = C.camara(t, KF_CAMPO, CAM_F)
    g = G(t)
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 40, tono_alto=0.95, tono_bajo=0.5, estrellas=30)
    GR.nube(g, 500 - 0.2 * cam.C[0], 160, 600, t, sem=8, vel=7, tono=0.3)
    GR.nube(g, 1500 - 0.2 * cam.C[0], 110, 520, t, sem=9, vel=6)
    # montañas nevadas detrás del acantilado
    for j, (y0, amp, tn) in enumerate(((hz - 260, 160, 0.4), (hz - 120, 110, 0.55))):
        perf = GR.perfil_colina(-80, 2000, y0, amp, sem=20 + j, n=18, ondas=2.5)
        GR.colina(g, perf, tono=tn, tono2=tn + 0.3, ang=-25, per=5.5, contorno=1.8)
        cimas = perf[perf[:, 1] < y0 - amp * 0.3]
        for (cx_, cy_) in cimas[::2]:
            g.papel(circ_pts(cx_, cy_ + 18, 46, 10, 20), 0.85)
    lp = [(PUERTA[0] + sg * 470, -170, PUERTA[1] - 120, 700, 0.8) for sg in (-1, 1)]
    _puerta_ciudad(g, cam, t, lp)

    def tono_suelo(a, b, zc):
        camino = np.clip(1 - np.abs(a - lerp(0, PUERTA[0], np.clip(b / PUERTA[1], 0, 1))) / (160 + 0.05 * b), 0, 1)
        return 0.26 + 0.12 * np.clip(b / 3000, 0, 1) + 0.34 * camino
    G3.plano(g, cam, (-6000, 0, -600), (1, 0, 0), (0, 0, 1), 12000, PUERTA[1] + 600, tono_suelo, familias=((0.0, 16.0),),
             luces=lp, oscuro=0.15)
    objs = []
    for X, Z, s_, i in PINOS:
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, s_=s_, i=i: F.pino(c, *cam.pt(X, 0, Z)[:2], s_ * cam.k(cam.pt(X, 0, Z)[2]), t,
                                                                       sem=i)))
    for i in range(40):                                    # rocas y matas con nieve: escala a cada distancia
        X = (rnd(i, 111) - 0.5) * 3400
        Z = 350 + 2300 * rnd(i, 112)
        if abs(X - lerp(0, PUERTA[0], Z / PUERTA[1])) < 260:
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: _roca(c, cam, X, Z, t, i)))
    for i in range(14):                                    # postes de cerca a la derecha del camino
        X, Z = 520 + 30 * math.sin(i), 500 + 230 * i
        objs.append((X, 0, Z, lambda c, X=X, Z=Z: G3.trazo3d(c, cam, [(X, 0, Z), (X, -150, Z)], 14, afilado=0.0)))
    for sg in (-1, 1):                                     # la guardia REAL de la puerta de Forjaz (pegatinas)
        C.peg(objs, cam, t, "Ironforge Guard", PUERTA[0] + sg * 330, PUERTA[1] - 160, 290.0, espejo=sg > 0, sem=76 + sg)
    # médico de la peste: cruza delante («como en una epidemia de verdad»)
    op = C.env(t, A.TR_CAMPO, A.h_huyeron + 0.3, 0.6, 0.6)
    if op > 0.01:
        u = pr(t, A.TR_CAMPO, A.h_huyeron + 0.9)
        X = lerp(MEDICO[0][0], MEDICO[1][0], u)
        Z = lerp(MEDICO[0][1], MEDICO[1][1], u)
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, op=op: F.persona(c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t,
                                                             "medico", anda=0.8, dirx=-1, op=op, sem=70,
                                                             brazos=(0.2, 0.5 + 0.6 * smooth(pr(t, A.h_epidemia - 0.3,
                                                                                                A.h_epidemia + 0.3))))))
    # el que huye al bosque, solo
    if t > A.h_huyeron - 1.0:
        u = pr(t, A.h_huyeron - 1.0, A.h_otros + 1.0)
        X, Z = lerp(-420, -1150, u), lerp(1200, 1700, u)
        objs.append((X, 0, Z, lambda c, X=X, Z=Z: F.persona(c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t,
                                                             "capa", anda=1.0, dirx=-1, sem=71,
                                                             op=1 - pr(t, A.h_otros + 0.6, A.h_otros + 1.2))))
    # el que avisa en la puerta (campana en un palo) y los que llegan y se detienen
    if t > A.h_otros - 1.0:
        X, Z = PUERTA[0] - 120, PUERTA[1] - 520
        toca = math.sin(t * 9) * smooth(pr(t, A.h_avisando - 0.3, A.h_avisando + 0.2))
        objs.append((X, 0, Z, lambda c, X=X, Z=Z: _vigia(c, cam, X, Z, t, toca)))
        for j in range(3):
            para = smooth(pr(t, A.h_avisando + 0.2 * j, A.h_avisando + 0.6 + 0.2 * j))
            Xj = PUERTA[0] - 200 - 380 * (1 - para * 0.15) + 90 * j
            Zj = PUERTA[1] - 900 - 220 * j + 300 * min(1.0, pr(t, A.h_otros, A.h_avisando))
            if j != 1:                                     # los que llegan: dos son personajes REALES (pegatinas)
                nom, alto = (("Ironforge Mountaineer", 285.0), None, ("Stormwind City Guard", 375.0))[j]
                C.peg(objs, cam, t, nom, Xj, Zj, alto, Y=-9 * abs(math.sin(t * 5 + j)) * (1 - para), sem=72 + j)
                continue
            objs.append((Xj, 0, Zj, lambda c, Xj=Xj, Zj=Zj, j=j, para=para: F.persona(
                c, *cam.pt(Xj, 0, Zj)[:2], 0.95 * cam.k(cam.pt(Xj, 0, Zj)[2]), t, ("enano", "capa", "guerrero")[j],
                fase=j, anda=1.0 - para, dirx=1, sem=72 + j)))
    # el sanador que mantiene vivo al contagioso
    if A.h_sanadores - 1.2 < t < A.h_otros2:
        op = C.env(t, A.h_sanadores - 1.2, A.h_puso, 0.5, 0.8)
        Xs, Zs = -260.0, 1100.0
        u = pr(t, A.h_sanadores - 1.0, A.h_puso)
        Xi, Zi = lerp(-40, 260, u), lerp(1200, 1300, u)
        objs.append((Xs, 0, Zs, lambda c: F.persona(c, *cam.pt(Xs, 0, Zs)[:2], 0.95 * cam.k(cam.pt(Xs, 0, Zs)[2]), t,
                                                    "sanador", anda=0.0, dirx=1, op=op, sem=80, brazos=(0.3, 2.2))))
        objs.append((Xi, 0, Zi, lambda c: F.persona(c, *cam.pt(Xi, 0, Zi)[:2], 0.95 * cam.k(cam.pt(Xi, 0, Zi)[2]), t,
                                                    "capa", anda=0.7, dirx=1, aura=1.0, op=op, sem=81)))
        for j, (Xo, Zo) in enumerate(((420, 1420), (520, 1250))):
            tc = A.h_contagiosos + 0.25 * j
            objs.append((Xo, 0, Zo, lambda c, Xo=Xo, Zo=Zo, j=j, tc=tc: F.persona(
                c, *cam.pt(Xo, 0, Zo)[:2], 0.95 * cam.k(cam.pt(Xo, 0, Zo)[2]), t, ("enano", "capa")[j], anda=0.3, dirx=-1,
                aura=smooth(pr(t, tc, tc + 0.3)), op=op, sem=82 + j)))
    C.figuras(g, cam, objs)
    # rayo de luz del sanador sobre el contagiado y el contagio que salta a los de al lado
    if A.h_sanadores - 1.2 < t < A.h_otros2:
        op = C.env(t, A.h_sanadores - 0.6, A.h_puso, 0.4, 0.8)
        a = cam.pt(-260 + 30, -560, 1100)
        b = cam.pt(Xi, -250, Zi)
        if op > 0.01:
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            G3.haz(g, a[0], a[1], ang, 16, math.hypot(b[0] - a[0], b[1] - a[1]) * 1.1, t, op=0.4 * op, color=(1.0, 0.95, 0.8))
            g.acento_luz(b[0], b[1], 160 * cam.k(b[2]), ORO, 0.5 * op)
        for j, (Xo, Zo) in enumerate(((420, 1420), (520, 1250))):
            u = pr(t, A.h_contagiosos - 0.3 + 0.25 * j, A.h_contagiosos + 0.25 * j)
            if 0 < u < 1:
                p, q = cam.pt(Xi, -330, Zi), cam.pt(Xo, -330, Zo)
                arco = [(lerp(p[0], q[0], v), lerp(p[1], q[1], v) - 80 * math.sin(math.pi * v)) for v in np.linspace(0, u, 10)]
                g.trazo(np.float32(arco), 4, color=SANGRE, op=0.9, afilado=0.5)
    # la cuarentena: la barrera brota a «puso» y la saltan a «saltaron»
    if t > A.h_puso - 0.4:
        X, Z, an = BARRERA
        F.barricada(g, cam, X, Z, an, t, alza=smooth(pr(t, A.h_puso - 0.3, A.h_cuarentenas + 0.3)))
        objs = []
        for j in range(3):
            t0 = A.h_saltaron - 0.5 + 0.35 * j
            u = pr(t, t0 - 0.8, t0 + 0.9)
            if 0 < u < 1:
                Xj = -320 + 300 * j
                Zj = lerp(Z - 500, Z + 500, u)
                Yj = -300 * math.sin(math.pi * pr(u, 0.35, 0.75))
                objs.append((Xj, Yj, Zj, lambda c, Xj=Xj, Yj=Yj, Zj=Zj, j=j: F.persona(
                    c, *cam.pt(Xj, Yj, Zj)[:2], 0.95 * cam.k(cam.pt(Xj, 0, Zj)[2]), t, ("capa", "enano", "guerrero")[j],
                    anda=2.0, dirx=1 if j % 2 else -1, sem=90 + j, brazos=(2.4, 2.6) if Yj < -60 else None)))
        # el que se contagia a propósito y corre hacia la multitud; la multitud huye gritando
        if t > A.h_otros2 - 0.6:
            u = pr(t, A.h_otros2 - 0.4, A.h_multitud + 0.6)
            Xr, Zr = lerp(-160, 520, u), lerp(1300, PUERTA[1] - 480, u)
            objs.append((Xr, 0, Zr, lambda c, Xr=Xr, Zr=Zr: _corredor(c, cam, Xr, Zr, t)))
            huye = smooth(pr(t, A.h_huir - 0.3, A.h_gritando + 1.0))
            for j in range(9):
                X0 = 380 + 300 * rnd(j, 101)
                Z0_ = PUERTA[1] - 430 + 240 * rnd(j, 102)
                dx_ = (X0 - 600) / (abs(X0 - 600) + 1) * (0.6 + rnd(j, 103))
                Xj, Zj = X0 + 600 * huye * dx_, Z0_ + 200 * huye * (rnd(j, 104) - 0.3)
                objs.append((Xj, 0, Zj, lambda c, Xj=Xj, Zj=Zj, j=j, dx_=dx_: F.persona(
                    c, *cam.pt(Xj, 0, Zj)[:2], 0.95 * cam.k(cam.pt(Xj, 0, Zj)[2]), t, ("enano", "capa", "guerrero",
                                                                                     "mercader")[j % 4],
                    fase=j, anda=0.2 + 1.8 * huye, dirx=1 if dx_ > 0 else -1, sem=100 + j,
                    brazos=(2.5, 2.8) if huye > 0.3 and j % 2 else None)))
        C.figuras(g, cam, objs)
    G3.iluminar(g, [(*cam.pt(PUERTA[0], -300, PUERTA[1])[:2], 900, 0.6, ORO)], amb=0.38, fuerza=0.45, acento=0.12)
    G3.particulas(g, t, "nieve", 140, (0, 0, 1920, 1080), sem=17)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 1800)[1]
    GR.niebla(g, y_nb - 40, y_nb + 10, t, op=0.5, sem=6, vel=30)
    with G3.capa_prof(g, cam, 260) as c:                   # primer plano: ramas de abeto nevadas, fuera de foco
        px, py, zc = cam.pt(cam.C[0] - 330, 0, cam.C[2] + 300)
        F.pino(c, px, py, 1.1 * cam.k(zc), t, sem=99)
    return g


def _vigia(c, cam, X, Z, t, toca):
    px, py, zc = cam.pt(X, 0, Z)
    k = cam.k(zc)
    F.persona(c, px, py, 0.95 * k, t, "capa", anda=0.0, dirx=-1, sem=75, brazos=(0.3, 2.3))
    top = cam.pt(X - 40, -620, Z)
    c.trazo([cam.pt(X - 40, -150, Z)[:2], top[:2]], 6 * k ** 0.5, afilado=0.0)
    bx, by = top[0] + 40 * k * toca, top[1] + 20 * k
    c.figura(np.float32([(bx - 22 * k, by + 40 * k), (bx + 22 * k, by + 40 * k), (bx + 12 * k, by), (bx - 12 * k, by)]), 0.4,
             contorno=2.0, ang=0, per=4, cruz=False)
    c.trazo([top[:2], (bx, by)], 2, afilado=0.0)
    paño = [(top[0], top[1] + 10 * k), (top[0] - 120 * k, top[1] + 20 * k + 10 * k * math.sin(t * 3)),
            (top[0] - 110 * k, top[1] + 90 * k), (top[0], top[1] + 80 * k)]
    c.figura(np.float32(paño), 0.2, contorno=2.0, ang=80, per=4)
    c.acento(np.float32(paño), SANGRE, 0.85)
    if abs(toca) > 0.3:
        for j in range(3):
            r = (20 + 18 * j) * k
            c.trazo(np.float32([(bx + r * math.cos(a), by + 20 * k + r * math.sin(a)) for a in np.linspace(-0.6, 0.6, 6)]),
                    1.6, op=0.7)


def _corredor(c, cam, X, Z, t):
    """El que se contagió a propósito: esqueleto rojo que corre con los brazos abiertos (ríe)."""
    px, py, zc = cam.pt(X, 0, Z)
    k = cam.k(zc)
    pose = GR.pose_danza(t * 1.8, 0.0, brio=1.2)
    pose.update(hi=2.3, hd=2.3, ci=0.4, cd=0.4, tr=0.25, mand=0.6 + 0.3 * math.sin(t * 14))
    c.acento_luz(px, py - 220 * k, 320 * k, SANGRE, 0.9)
    GR.esqueleto(c, px, py, 0.9 * k, pose, t, ojos=1.0)


def _roca(c, cam, X, Z, t, i):
    px, py, zc = cam.pt(X, 0, Z)
    k = cam.k(zc)
    if i % 3 == 0:                                          # mata seca asomando de la nieve
        GR.pasto(c, px, py, 1.1 * k, t, n=7, sem=i)
        return
    r = (40 + 50 * rnd(i, 113)) * k
    pts = GR.silueta_ruido(np.float32([(px - r, py), (px - r * 0.8, py - r * 0.7), (px - r * 0.1, py - r * 1.0),
                                       (px + r * 0.7, py - r * 0.6), (px + r, py)]), 3.0 * k, sem=i, paso=6)
    c.figura(pts, 0.35, contorno=2.0, tono2=0.85, luz=0, ang=60, per=4.4, cruz=False)
    c.papel(np.float32([(px - r * 0.75, py - r * 0.62), (px - r * 0.1, py - r * 0.98), (px + r * 0.62, py - r * 0.58),
                        (px, py - r * 0.66)]), 0.95)
