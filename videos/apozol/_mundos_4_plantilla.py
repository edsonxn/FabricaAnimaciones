# -*- coding: utf-8 -*-
"""Mundos de la escena 4 (la guerra del Mixtón): el peñol en isométrico (mesa de paredes verticales con guerreros y fogatas, cerco español que se cierra,
bandera que cae), el recuadro Juchipila–Mixtón–Apozol, la noche del apóstol Santiago a caballo, y el borde del vacío."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq2 as B
import kz_iso_deco as DC
import kz_gente_iso as G
import kz_pers2d as K2
import kz_ui as U
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H
import mundos_2 as M2

# ------------------------------------------------------------------------------------------------ caballo 2D y siluetas (copiados de los recursos de Juchipila)
#@@COPIADO@@


# ------------------------------------------------------------------------------------------------ el peñol en isométrico
ESTRATOS = [(150, 108, 138), (186, 124, 130), (214, 150, 120), (170, 118, 134)]
NIVELES = [(30, 30, 300, 300, 46), (62, 62, 236, 236, 46), (90, 90, 180, 180, 42), (112, 112, 136, 136, 38)]
TOPE = sum(n[4] for n in NIVELES)                        # altura del tope
CEN = (180.0, 180.0)


class Penol:
    """Mesa de paredes casi verticales (4 niveles con estratos), tope con fogatas y guerreros, cerco que se cierra y bandera española."""

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -220, -220, 580, 580, color_top=(150, 180, 104), t=t, seed=91, esp=42)
        DC.parches(lz, iso, -220, -220, 580, 580, (150, 180, 104), n=30, var=22, seed=92, alfa=0.55, tam=(50, 120))
        DC.hierba(lz, iso, -220, -220, 580, 580, n=170, seed=93, t=t, color=(120, 168, 92), flores=0.05)
        O.agua(lz, iso, M2.cinta([(560, -240), (520, -60), (556, 120), (520, 300), (560, 600)], 56), t, z=-1.0, seed=9)
        I.camino(lz, iso, [(-230, 380), (-60, 330), (60, 400), (190, 520), (330, 590)], 26, (232, 214, 170), borde=(208, 188, 144))

    def _mesa(self, lz, iso, t, guerreros, fuego, bandera, caido):
        for k, (x, y, w, d, h) in enumerate(NIVELES):
            z0 = sum(n[4] for n in NIVELES[:k])
            I.caja(lz, iso, x, y, w, d, h + 0.6, ESTRATOS[k % 4], z0=z0)
            if k < len(NIVELES) - 1:
                I.suelo_rect(lz, iso, x, y, w, d, (126, 160, 92), z=z0 + h)
        I.suelo_rect(lz, iso, 112, 112, 136, 136, (132, 168, 96), z=TOPE)
        iz = M2.iso_en(iso, TOPE)
        items = []
        if fuego > 0.01:
            for i, (x, y) in enumerate(((140, 140), (200, 150), (160, 205), (215, 215), (130, 190))):
                items.append((x + y, (lambda x=x, y=y, i=i: (O.fuego(lz, iz, x, y, s=0.8 * fuego, t=t, seed=i), O.humo(lz, iz, x, y, 12, t, n=5, s=1.0, seed=i, color=(90, 70, 100))))))
        n = int(26 * guerreros)
        for i in range(n):
            ang = i * 2.399
            r = 18 + 40 * math.sqrt((i + 0.5) / 26)
            x, y = CEN[0] + r * math.cos(ang), CEN[1] + r * math.sin(ang)
            if caido > 0.01 and h01(97, i) < caido:
                continue
            tipo = ("caxcan_lanza", "caxcan_mazo", "honda", "caxcan")[i % 4]
            items.append((x + y, (lambda x=x, y=y, tipo=tipo, i=i: G.persona(lz, iso, x, y, t, tipo=tipo, dir=(1.0, 1.0) if i % 2 else (-1.0, 1.0), seed=500 + i, h=46,
                                                                              accion="vitorea" if i % 3 == 0 else "pelea" if i % 3 == 1 else None, z=TOPE))))
        items.sort(key=lambda q: q[0])
        for _, fn in items:
            fn()
        if bandera > 0.01:
            O2.faro_bandera(lz, iz, CEN[0], CEN[1], t=t, h=70 * bandera)

    def objetos(self, t, guerreros=1.0, cerco=0.0, fuego=1.0, bandera=0.0, caido=0.0, gente_cerco=1.0):
        m = I.Mundo()
        m.topo = False
        m.add(30, 30, 330, 330, TOPE + 120, lambda lz, iso: self._mesa(lz, iso, t, guerreros, fuego, bandera, caido), fijo=False, clave=1)
        # el cerco: anillo de españoles y aliados que se cierra (cerco 0..1: radio 340 -> 230) + barriles de pólvora
        R = 340 - 110 * cerco
        n = int(34 * gente_cerco)
        for i in range(n):
            a = i * 2 * math.pi / max(1, n) + 0.05 * math.sin(t * 0.3 + i)
            x, y = CEN[0] + R * math.cos(a), CEN[1] + R * math.sin(a)
            tipo = ("conquistador", "conquistador_lanza", "aliado", "capitan_esp")[i % 4]
            m.add(x - 5, y - 5, x + 5, y + 5, 52, (lambda x, y, tipo, i, a: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipo=tipo, dir=(-math.cos(a), -math.sin(a)), vel=0.0, seed=700 + i, h=46,
                                                                                                   accion="pelea" if i % 5 == 0 else None)))(x, y, tipo, i, a), fijo=False, clave=x + y * 7 + 1)
        for i, a in enumerate((0.5, 2.1, 3.6, 5.2)):
            x, y = CEN[0] + (R + 50) * math.cos(a), CEN[1] + (R + 50) * math.sin(a)
            m.add(x - 12, y - 12, x + 12, y + 12, 40, (lambda x, y, i: (lambda lz, iso: O.barril(lz, iso, x, y, s=1.2)))(x, y, i), fijo=False, clave=x + y * 5 + 2)
        # campamento español en el borde exterior: tiendas con bandera, fogatas y caballos; rocas caídas del peñol; bosque alrededor
        for i, (x, y) in enumerate(((-150, 40), (-130, 330), (70, 460), (400, 470), (470, 120))):
            B.tienda_campana(m, x, y, t_fn=lambda: t)
            m.add(x + 26, y + 26, x + 38, y + 38, 20, (lambda x, y, i: (lambda lz, iso: (O.fuego(lz, iso, x + 32, y + 32, s=0.6, t=t, seed=i), O.humo(lz, iso, x + 32, y + 32, 10, t, n=4, s=0.8, seed=i))))(x, y, i),
                  fijo=False, clave=x + y * 3 + 9)
        for i, (x, y, s) in enumerate(((10, 10, 1.4), (340, 30, 1.2), (350, 340, 1.5), (20, 330, 1.3), (180, 360, 1.1), (180, 0, 1.0))):
            m.add(x - 8, y - 8, x + 8, y + 8, 18, (lambda x, y, s, i: (lambda lz, iso: O.roca(lz, iso, x, y, s=s, seed=30 + i, color=(176, 150, 150))))(x, y, s, i), clave=x + y * 3 + 4)
        DC.bosque(m, -210, -210, 570, 570, n=34, seed=94, evitar=((-170, -150, 520, 520),), t_fn=lambda: t, tipos=("arbol", "arbusto"), colores=[(110, 168, 98), (96, 150, 90), (128, 176, 104)])
        return m


def inset_tres(lz, x, y, R, t, t_juch, t_mix, t_apozol, k=1.0, alfa=1.0):
    """Recuadro redondo con Juchipila (S), el peñol del Mixtón (en medio) y Apozol (N), unidos por el río."""
    if k <= 0.01:
        return
    R = R * k
    ring = circulo(x, y, R, 56)
    lz.relleno(circulo(x + 8, y + 12, R + 8, 56), (20, 10, 50), alfa=0.35, capa=1)
    with lz.recorte(ring):
        lz.degradado(ring, (196, 226, 150), (110, 184, 118), (x, y - R), (x, y + R), capa=1, alfa=alfa)
        for sg, ax in ((-1, x - R), (1, x + R)):
            pts = [(ax, y - R - 10)] + [(ax - sg * (90 + 40 * math.sin(v * 3.0 + (1 if sg > 0 else 0))), y - R + v * 2 * R) for v in np.linspace(0, 1, 10)] + [(ax, y + R + 10)]
            lz.relleno(np.array(pts), (150, 110, 150) if sg < 0 else (132, 96, 140), alfa=0.85 * alfa, capa=1)
        rio = np.array(catmull(np.array([(x - 20, y + R + 20), (x, y + 60), (x + 30, y - 40), (x + 20, y - R - 20)], float), 10, False))
        lz.trazo(rio, (60, 150, 226), 22.0, afinar=False, temblor=0.0, capa=1)
        lz.trazo(rio, (140, 214, 246), 8.0, afinar=False, temblor=0.0, capa=1)
        pts = {"juchipila": (x - 56, y + 0.62 * R), "mixton": (x + 4, y - 4), "apozol": (x + 50, y - 0.62 * R)}
        for nom, t0 in (("juchipila", t_juch), ("mixton", t_mix), ("apozol", t_apozol)):
            kk = e_back(prog(t, t0, t0 + 0.4)) if t >= t0 else 0.0
            if kk <= 0.01:
                continue
            px, py = pts[nom]
            if nom == "mixton":
                lz.relleno(np.array([(px - 52 * kk, py + 26 * kk), (px - 30 * kk, py - 34 * kk), (px - 8 * kk, py - 62 * kk), (px + 28 * kk, py - 56 * kk), (px + 44 * kk, py - 20 * kk), (px + 58 * kk, py + 26 * kk)]),
                           (122, 78, 142), alfa=alfa, capa=2)
                lz.relleno(np.array([(px + 28 * kk, py - 56 * kk), (px + 44 * kk, py - 20 * kk), (px + 58 * kk, py + 26 * kk), (px + 10 * kk, py + 26 * kk)]), (92, 56, 118), alfa=alfa, capa=2)
                lz.relleno(rect_red(px - 12 * kk, py - 68 * kk, 36 * kk, 8 * kk, 3 * kk), (130, 168, 98), alfa=alfa, capa=2)
            else:
                for ox, oy, sc in ((-22, 6, 1.0), (20, 4, 0.9), (0, -10, 1.0)):
                    P.casa(lz, px + ox * kk, py + oy * kk, 0.48 * sc * kk, calor=0.4)
    lz.trazo(ring, (255, 206, 72), 12.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
    lz.trazo(ring, (255, 244, 200), 3.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
    for nom, (px, py), t0, col, px_ in (("Juchipila", (x - 30, y + 0.62 * R + 30), t_juch, U.COL["morado"], 34), ("peñol del Mixtón", (x + 4, y + 58), t_mix, U.COL["rojo"], 34),
                                        ("Apozol", (x + 60, y - 0.62 * R - 30), t_apozol, U.COL["naranja"], 34)):
        kk = U.pop(t, t0 + 0.1)
        if kk > 0.01:
            U.llamada(lz, px, py, nom, color=col, px=px_, k=kk * alfa, cola=None)


def penol_fuego(lz, x, y, s, t, capa=1, alfa=1.0, fuego=1.0):
    """Peñol de paredes casi verticales (silueta violeta en 3 tonos) con fogatas y humo. (x, y) = centro de la base."""
    k = s
    cuerpo = [(-230, 0), (-200, -120), (-150, -250), (-110, -330), (-60, -360), (60, -362), (116, -330), (156, -240), (206, -118), (240, 0)]
    pts = np.array([(x + px * k, y + py * k) for px, py in cuerpo])
    lz.relleno(pts, (92, 56, 118), alfa=alfa, capa=capa)
    sh = np.array([(x + px * k, y + py * k) for px, py in [(40, -362), (116, -330), (156, -240), (206, -118), (240, 0), (60, 0), (70, -150)]])
    lz.relleno(sh, (62, 36, 88), alfa=alfa, capa=capa)
    for yy in (-70, -150, -240):
        lz.relleno(np.array([(x - 230 * k, y + (yy - 6) * k), (x + 240 * k, y + (yy - 10) * k), (x + 240 * k, y + (yy + 6) * k), (x - 230 * k, y + (yy + 2) * k)]),
                   (50, 30, 74), alfa=0.22 * alfa, capa=capa)
    lz.relleno(np.array([(x - 60 * k, y - 362 * k), (x + 60 * k, y - 364 * k), (x + 70 * k, y - 352 * k), (x - 70 * k, y - 350 * k)]), (124, 150, 96), alfa=alfa, capa=capa)
    for i, fx in enumerate((-40, 10, 50)):
        if fuego > 0.01:
            fy = y - 362 * k
            for j, (col, sc) in enumerate((((236, 60, 48), 1.0), ((255, 138, 40), 0.7), ((255, 224, 96), 0.4))):
                a = 26 * k * sc * fuego * (1 + 0.2 * math.sin(t * 9 + i * 2 + j))
                px = x + fx * k
                lz.relleno(np.array([(px - 8 * k * sc, fy), (px + 8 * k * sc, fy), (px + 2 * k * math.sin(t * 7 + i), fy - a * 1.6)]), col, alfa=alfa, capa=capa)
            for q in range(4):
                u = ((t * 0.3 + q / 4 + i * 0.2) % 1.0)
                lz.relleno(circulo(x + fx * k + 14 * k * math.sin(u * 5 + i), fy - 30 * k - u * 150 * k, (8 + 22 * u) * k, 14), (70, 52, 84), alfa=0.5 * (1 - u) * alfa, capa=capa)


def noche_penol(lz, t, k=1.0, glow=1.0):
    """Noche estrellada con el peñol en silueta y fogatas arriba; el resplandor de un combate lejano."""
    for i in range(60):
        x, y = W * h01(31, i, 1), 560 * h01(31, i, 2)
        a = 0.45 + 0.5 * math.sin(t * (0.6 + h01(31, i, 3)) + i)
        lz.relleno(circulo(x, y, 1.4 + 2.2 * h01(31, i, 4), 8), (255, 244, 214), alfa=a * 0.8 * k, capa=0)
    lz.halo(960, 880, 700, (255, 120, 70), alfa=0.22 * glow, dureza=1.0, capa=0)
    for i, x in enumerate((140, 420, 1500, 1790)):
        lz.relleno(np.array([(x - 340, 1000), (x - 80, 720 + 30 * (i % 2)), (x + 60, 700), (x + 330, 1000)]), (46, 28, 74), capa=0)
    penol_fuego(lz, 960, 1040, 1.45, t, capa=0, fuego=glow)


def borde_vacio(lz, t, k=1.0):
    """El borde de un peñol al atardecer: la silueta de una figura mira el vacío; abajo, el valle en bruma."""
    lz.relleno(np.array([(-40, 760), (500, 740), (860, 770), (1000, 830), (1010, H + 40), (-40, H + 40)]), (40, 20, 56), capa=1)
    lz.relleno(np.array([(-40, 780), (500, 760), (860, 790), (990, 840), (-40, 840)]), (70, 40, 84), alfa=0.8, capa=1)
    for i, (x, y, s) in enumerate(((300, 756, 1.0), (560, 750, 0.8), (180, 764, 1.2))):
        for q in range(5):
            lz.trazo(np.array([(x, y), (x + (q - 2) * 18 * s, y - (28 + 8 * (q % 3)) * s)]), (30, 14, 44), 3.0, afinar=False, temblor=0.0, capa=1)
    fx, fy, s = 840, 772, 2.3
    lz.relleno(np.array([(fx - 14 * s, fy), (fx + 14 * s, fy), (fx + 12 * s, fy - 70 * s), (fx - 12 * s, fy - 70 * s)]), (22, 10, 34), capa=2)
    lz.relleno(circulo(fx, fy - 86 * s, 14 * s, 14), (22, 10, 34), capa=2)
    for j in range(5):
        a = -0.8 + 0.4 * j
        lz.relleno(np.array([(fx - 6 * s + 3 * j, fy - 98 * s), (fx + math.sin(a) * 30 * s, fy - 98 * s - math.cos(a) * 30 * s), (fx + 4 * s + 3 * j, fy - 98 * s)]), (22, 10, 34), capa=2)
    for i in range(5):
        y = 880 + 40 * i
        lz.relleno(np.array([(900, y), (W + 40, y - 30), (W + 40, y + 60), (900, y + 70)]), (120 + 10 * i, 70 + 6 * i, 120), alfa=0.4, capa=0)
    for j, (c, y0, amp) in enumerate((((150, 78, 120), 700, 70), ((120, 60, 112), 760, 60), ((92, 44, 100), 820, 50))):       # sierras lejanas al otro lado del vacío
        pts = [(x, y0 - amp * (0.5 + 0.5 * math.sin(x * 0.006 + j * 1.7)) - 20 * math.sin(x * 0.019 + j)) for x in np.linspace(1000, W + 40, 24)]
        lz.relleno(np.array(pts + [(W + 40, H + 20), (1000, H + 20)]), c, alfa=0.9, capa=0)
    for i in range(30):
        lz.relleno(circulo(W * h01(41, i, 1), 380 * h01(41, i, 2), 1.6 + 1.8 * h01(41, i, 3), 8), (255, 236, 214), alfa=0.5 * (0.5 + 0.5 * math.sin(t * 0.8 + i)), capa=0)
