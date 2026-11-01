# -*- coding: utf-8 -*-
"""Capa de interfaz, parte 2: cuerpo, mareo, regreso A, versión B (átomos, suelo, agua, nosotros, regreso B),
realidad y cierre; y el posproceso (visión de túnel y destellos)."""
import math

import cv2
import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, circulo, elipse, rect_red, h01, catmull
from mundo_comun import ventana, campana
from anclas import A, Z3, Z4, PORTAL_IN, PORTAL_OUT, TOTAL
from estado import T_B
import kz_ui as KU
import kit_oxi as KO
import kit_bio as KB
import ui_base as UB
from ui_base import ent, pildora, texto_q, ROJO_O, TEAL, AZUL_OSC, NARANJA, MORADO, VERDE
import mundo_paisaje as MP
import mundo_espacio as ME
import mundo_cuerpo as MC
import gente as G
import ui as U1

AMARILLO = (255, 214, 90)
ROJO_B = (226, 70, 80)


# ======================================================================== cuerpo
def cuerpo(lz, t, ctx):
    if not (PORTAL_IN[0] < t < PORTAL_OUT[1]):
        return
    a_z = 1 - e_in(prog(t, PORTAL_OUT[0] - 0.3, PORTAL_OUT[0] + 0.2))
    a_in = e_out(prog(t, PORTAL_IN[1] - 0.2, PORTAL_IN[1] + 0.3))
    g = a_z * a_in
    if g <= 0.01:
        return
    an, z = MC.cam(t)
    # glóbulo de Kuri
    k, a = ent(t, A.sangre - 0.1, A.celulas - 0.7)
    if a > 0.01:
        xb = (an[0] - 120 + 40 * math.sin(t * 0.7) - an[0]) * z + W / 2
        yb = (86 + 20 * math.sin(t * 1.3)) * z + H / 2
        KU.llamada(lz, xb, yb + 46 * z, "glóbulo rojo", color=ROJO_B, px=30, k=k, alfa=a * g, cola="arriba")
        pildora(lz, W / 2, 200, "la sangre reparte el O2", 34, k=k, alfa=a * g * (1 - prog(t, A.desaparece_c - 0.3, A.desaparece_c)))
    k, a = ent(t, A.desaparece_c, A.celulas - 0.7)
    pildora(lz, W / 2, 200, "¡sin O2!", 40, k=k, alfa=a * g, fondo=ROJO_B, color=(255, 255, 255))
    # célula
    def pant(X, Y):
        return (X - an[0]) * z + W / 2, (Y - an[1]) * z + H / 2
    k, a = ent(t, A.celulas + 0.6, A.cerebro - 1.2)
    if a > 0.01:
        x, y = pant(MC.X_CEL + 230, -300)
        KU.llamada(lz, x, y, "mitocondria", color=NARANJA, px=30, k=k, alfa=a * g)
    k, a = ent(t, A.comida - 0.1, A.cerebro - 1.2)
    if a > 0.01:
        x, y = pant(MC.X_CEL - 560, 120)
        KU.llamada(lz, x, y, "comida (glucosa)", color=(200, 150, 40), px=28, k=k, alfa=a * g)
    k, a = ent(t, A.celulas + 1.0, A.cerebro - 1.2)
    if a > 0.01:
        niv = 1 - 0.88 * e_inout(prog(t, A.energia - 0.8, A.energia + 1.2))
        with lz.capa(2):
            lz.relleno(circulo(1700, 520, 150 * k, 40), (28, 24, 70), alfa=0.7 * a * g)
            KB.bateria(lz, 1700, 520, 1.25 * k, niv, alfa=a * g)
        pildora(lz, 1700, 720, "energía", 32, k=k, alfa=a * g, fondo=AMARILLO)
    # cerebro
    k, a = ent(t, A.organo - 0.3, A.y1943 + 2.0)
    if a > 0.01:
        KB.tarta(lz, 1600, 360, 140, 0.20, col=(255, 150, 190), resto=(236, 230, 246), texto="20 %", sub="de tu energía", k=k,
                 alfa=a * g, crece=e_out(prog(t, A.organo - 0.2, A.organo + 0.8)))
        pildora(lz, 1600, 560, "y solo pesa el 2 % del cuerpo", 26, k=k, alfa=a * g)
    k, a = ent(t, A.y1943 - 0.1, PORTAL_OUT[0])
    pildora(lz, 330, 300, "1943", 48, k=k, alfa=a * g, fondo=AMARILLO)
    k, a = ent(t, A.medicos - 0.1, PORTAL_OUT[0])
    pildora(lz, 330, 386, "Rossen, Kabat y Anderson", 26, k=k, alfa=a * g)
    k, a = ent(t, A.cortan - 0.1, PORTAL_OUT[0])
    if a > 0.01:
        fr = prog(t, A.cortan, A.seis + 0.3) * 0.66
        KB.cronometro(lz, 330, 600, 120, frac=fr, numero=int(fr * 10 + 1e-6), alfa=a * g, k=k, col=ROJO_B, t=t)
        pildora(lz, 330, 770, "sin riego", 30, k=k, alfa=a * g, fondo=ROJO_B, color=(255, 255, 255))
    # línea de tiempo 0-8 s
    k, a = ent(t, A.respuesta - 0.2, PORTAL_OUT[0])
    if a > 0.01:
        x0, x1, yb = 560, 1460, 960
        sx = (x1 - x0) / 8.0
        with lz.capa(2):
            lz.relleno(rect_red(x0 - 30, yb - 70, x1 - x0 + 60, 130, 26), (28, 24, 70), alfa=0.8 * a * g)
            lz.trazo(np.array([[x0, yb], [x1, yb]]), (230, 230, 250, int(255 * a * g)), 6, afinar=False)
            for s in range(9):
                lz.trazo(np.array([[x0 + s * sx, yb - 12], [x0 + s * sx, yb + 12]]), (230, 230, 250, int(255 * a * g)), 4, afinar=False)
                lz.texto(f"{s} s", x0 + s * sx, yb + 36, 24, "geo", color=(230, 230, 250), borde=None, alfa=a * g, temblor=0.0)
            zr = e_out(prog(t, A.seis - 0.2, A.seis + 0.5))
            if zr > 0.01:
                lz.relleno(rect_red(x0 + 6.4 * sx, yb - 22, 0.5 * sx * zr, 44, 8), (255, 90, 100), alfa=a * g)
            m = KU.pop(t, A.cinco_c - 0.1)
            if m > 0.01:
                xm = x0 + 5 * sx
                lz.relleno(np.array([[xm - 16 * m, yb - 58], [xm + 16 * m, yb - 58], [xm, yb - 26]]), AMARILLO, alfa=a * g)
                lz.relleno(circulo(xm, yb - 66, 18 * m, 20), AMARILLO, alfa=a * g)
        k2, a2 = ent(t, A.seis - 0.1, PORTAL_OUT[0])
        pildora(lz, x0 + 6.65 * sx, yb - 110, "pierdes el conocimiento", 28, k=k2, alfa=a2 * g, fondo=ROJO_B, color=(255, 255, 255))
        k3, a3 = ent(t, A.borde - 0.1, PORTAL_OUT[0])
        pildora(lz, x0 + 4.3 * sx, yb - 180, "5 s: justo al borde", 30, k=k3, alfa=a3 * g, fondo=AMARILLO)


def mareo(lz, t, ctx, est):
    S = ctx.get("S")
    m = est.get("mareo", 0.0)
    if S is None or m <= 0.01:
        return
    x, y = S.pt(G.X_PROTA + 2, 236)
    with lz.capa(2):
        for i in range(5):
            ang = t * 3 + i / 5 * 2 * math.pi
            KU.chispa4(lz, x + 70 * S.k * math.cos(ang), y + 22 * S.k * math.sin(ang), 14 * S.k, (255, 240, 170), alfa=m, rot=t * 2)
    k, a = ent(t, A.mareo, A.cinco_ra - 0.3)
    pildora(lz, W / 2 + 230, 300, "mareo", 32, k=k, alfa=a)
    k, a = ent(t, A.tunel - 0.1, A.cinco_ra - 0.3)
    pildora(lz, W / 2 + 230, 380, "visión de túnel", 32, k=k, alfa=a)
    k, a = ent(t, A.desmayarse - 0.1, A.cinco_ra - 0.3)
    if a > 0.01:
        xb, yb = S.pt(MP.X_BANCO - 10, 230)
        KU.llamada(lz, xb, yb, "desmayo", color=MORADO, px=28, k=k, alfa=a)


# ======================================================================== regreso A
def regreso_a(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    U1.lupa_aire(lz, t, S, A.cinco_ra - 0.2, A.sube - 0.2, vuelve=A.vuelve_ra - 0.05)
    k, a = ent(t, A.vuelve_ra, A.sube - 0.2)
    pildora(lz, 1450, 600, "el O2 vuelve", 32, k=k, alfa=a, fondo=TEAL, color=(255, 255, 255))
    k, a = ent(t, A.sube - 0.1, A.brasas - 0.3)
    if a > 0.01:
        v = lerp(80.0, 101.3, e_out(prog(t, A.sube, A.sube + 0.6)))
        KB.manometro(lz, 360, 380, 140, v, 0, 120, t, texto="kPa", alfa=a, k=k)
    k, a = ent(t, A.otro_golpe - 0.2, A.brasas - 0.3)
    if a > 0.01:
        b = -0.9 * e_out(prog(t, A.otro_golpe - 0.1, A.otro_golpe + 0.4))

        def cont(lz):
            lz.relleno(circulo(0, 0, 300, 40), (60, 40, 80))
            KB.oido(lz, 0, 0, 0.95, t, bombeo=b)
            for j in range(3):
                yy = -50 + j * 50
                UB.flecha(lz, (-150, yy), (-70 - 30 * b, yy), (255, 230, 120), 7, 20, alfa=-b)
        KB.lupa(lz, 1420, 430, 270, cont, fondo=(60, 40, 80), k=k, alfa=a, objetivo=S.pt(G.X_PROTA - 30, 190))
        k2, a2 = ent(t, A.contrario - 0.2, A.brasas - 0.3)
        pildora(lz, 1420, 740, "golpe al revés", 30, k=k2, alfa=a2)
    k, a = ent(t, A.brasas - 0.05, A.pilotos - 0.7)
    if a > 0.01:
        x, y = S.pt(MP.X_ASADOR, 150)
        KU.llamada(lz, x, y, "las brasas vuelven a prender", color=NARANJA, px=28, k=k, alfa=a)
    k, a = ent(t, A.motores_ra - 0.1, A.choques - 0.6)
    if a > 0.01:
        X, Hh = G.pos_avion2(t)
        x, y = S.pt(X - 40, Hh + 100)
        KU.llamada(lz, x, y, "motores encendidos", color=TEAL, px=30, k=k, alfa=a)
    k, a = ent(t, A.choques - 0.05, A.version_facil - 0.4)
    if a > 0.01:
        x, y = S.pt(900, 180)
        KU.llamada(lz, x, y, "choques", color=ROJO_B, px=30, k=k, alfa=a)
    k, a = ent(t, A.choques + 0.5, A.version_facil - 0.4)
    if a > 0.01:
        x, y = S.pt(-40, 420)
        KU.llamada(lz, x, y, "apagones", color=AZUL_OSC, px=30, k=k, alfa=a)
    k, a = ent(t, A.sobreviviriamos - 0.1, A.dificil - 0.6)
    pildora(lz, W / 2, 230, "casi todos sobreviviríamos", 40, k=k, alfa=a, fondo=(120, 220, 160), icono="check")
    k, a = ent(t, A.version_facil - 0.1, A.dificil - 0.6)
    pildora(lz, W / 2, 330, "esa era la versión fácil", 34, k=k, alfa=a)


# ======================================================================== versión B: átomos
def red_si_o(lz, t, falta=0.0, cae=0.0, n=4, esc=1.0, hueco=1.0):
    """Red de sílice: Si (lila) unidos por O (rojo). cae 0..1: sin el pegamento los Si se sueltan y caen."""
    d = 110 * esc
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * d, j * d
            if cae > 0:
                x += 30 * cae * math.sin(i * 3 + j)
                y += cae * (120 + 60 * h01(i, j)) * cae
            if i < n:
                ox, oy = (i + 0.5) * d, j * d
                lz.trazo(np.array([[i * d, j * d], [(i + 1) * d, j * d]]) + [0, 0], (255, 200, 200, int(160 * (1 - falta))), 6,
                         afinar=False)
                KO.atomo(lz, ox, oy, 20 * esc, KO.COL_AT["O"], 1 - falta)
                if falta > 0.05 and hueco > 0:
                    KO.fantasma(lz, ox, oy, 20 * esc, alfa=hueco * min(1.0, falta * 2) * (1 - cae))
            if j < n:
                ox, oy = i * d, (j + 0.5) * d
                lz.trazo(np.array([[i * d, j * d], [i * d, (j + 1) * d]]), (255, 200, 200, int(160 * (1 - falta))), 6, afinar=False)
                KO.atomo(lz, ox, oy, 20 * esc, KO.COL_AT["O"], 1 - falta)
                if falta > 0.05 and hueco > 0:
                    KO.fantasma(lz, ox, oy, 20 * esc, alfa=hueco * min(1.0, falta * 2) * (1 - cae))
            KO.atomo(lz, x, y, 26 * esc, KO.COL_AT["Si"], 1.0)


def atomos(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    am = ventana(t, A.cada_atomo - 0.1, A.gas_at + 1.0, 0.4, 0.6)
    if am > 0.01:
        MP.motas_o(lz, t, S, -2400, 2300, -1450, -40, 260, am, seed=1, r=11)
        MP.motas_o(lz, t, S, 2400, 5400, -1400, -20, 160, am, seed=2, r=11)
        MP.motas_o(lz, t, S, -1500, 1300, 0, 260, 70, am, seed=3, r=9)
        MP.motas_o(lz, t, S, -4800, -2400, 0, 1300, 90, am, seed=4, r=11)
    k, a = ent(t, A.gas_at - 0.3, A.mitad_at - 0.5)
    pildora(lz, W / 2, 210, "el oxígeno no es solo un gas", 40, k=k, alfa=a, fondo=ROJO_B, color=(255, 255, 255))
    # rocas
    k, a = ent(t, A.mitad_at - 0.1, A.agua_at - 0.6)
    if a > 0.01:
        KB.tarta(lz, 1560, 280, 150, 0.46, col=ROJO_O, texto="46 %", sub="de la corteza", k=k, alfa=a,
                 crece=e_out(prog(t, A.mitad_at, A.mitad_at + 0.9)))
        KB.lupa(lz, 1560, 730, 220, lambda lz: red_si_o(lz, t, n=3, esc=0.9), fondo=(70, 56, 90), k=k, alfa=a,
                objetivo=S.pt(-300, -500))
        pildora(lz, 1560, 470, "en peso", 26, k=k, alfa=a)
    # agua
    k, a = ent(t, A.agua_at - 0.1, A.cuerpo_at - 0.6)
    if a > 0.01:
        KB.tarta(lz, 1560, 280, 150, 0.888, col=ROJO_O, resto=(236, 242, 255), texto="89 %", sub="del agua", k=k, alfa=a,
                 crece=e_out(prog(t, A.noventa - 0.3, A.noventa + 0.8)))

        def cont(lz):
            for i, (mx, my) in enumerate(((-90, -80), (70, -100), (-20, 30), (110, 60), (-120, 110), (30, 150))):
                KO.molecula(lz, mx + 12 * math.sin(t + i), my + 10 * math.cos(t * 1.2 + i), 1.6, "H2O", rot=0.4 * math.sin(t * 0.7 + i))
        KB.lupa(lz, 1560, 730, 220, cont, fondo=(70, 150, 230), k=k, alfa=a, objetivo=S.pt(3000, -500))
        pildora(lz, 1560, 470, "en peso", 26, k=k, alfa=a)
    # cuerpo
    k, a = ent(t, A.cuerpo_at - 0.1, A.pegamento - 0.4)
    if a > 0.01:
        KB.tarta(lz, 1560, 360, 160, 0.65, col=ROJO_O, texto="65 %", sub="de tu cuerpo", k=k, alfa=a,
                 crece=e_out(prog(t, A.dos_terceras - 0.4, A.dos_terceras + 0.8)))
        MP.motas_o(lz, t, S, G.X_PROTA - 40, G.X_PROTA + 40, 10, 210, 40, a, seed=6, r=6)
        pildora(lz, 1560, 590, "dos terceras partes", 28, k=k, alfa=a)
    # pegamento: red de enlaces
    ap = ventana(t, A.pegamento - 0.3, A.cero_s - 0.3, 0.6, 0.5)
    if ap > 0.01:
        rng = np.random.default_rng(5)
        pts = np.stack([rng.uniform(60, W - 60, 90), rng.uniform(330, H - 40, 90)], 1)
        fr = e_out(prog(t, A.pegamento - 0.2, A.pegamento + 1.4))
        with lz.capa(2):
            for i in range(len(pts)):
                d = np.hypot(*(pts - pts[i]).T)
                for j in np.argsort(d)[1:3]:
                    if j > i or True:
                        q = pts[i] + (pts[j] - pts[i]) * fr
                        lz.trazo(np.array([pts[i], q]), (255, 120, 130, int(170 * ap)), 4, afinar=False)
                lz.relleno(circulo(pts[i][0], pts[i][1], 9, 12), (255, 90, 100), alfa=ap)
        k, a = ent(t, A.pegamento - 0.1, A.cero_s - 0.3)
        pildora(lz, W / 2, 210, "el pegamento de casi todo", 40, k=k, alfa=a, fondo=ROJO_B, color=(255, 255, 255))


# ======================================================================== suelo
def suelo(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    k, a = ent(t, A.cero_s - 0.3, A.edificios - 0.3)
    if a > 0.01:
        falta = e_out(prog(t, T_B, T_B + 0.4))
        cae = e_in(prog(t, A.solidos - 0.3, A.solidos + 1.4))
        KB.lupa(lz, 1500, 400, 240, lambda lz: red_si_o(lz, t, falta=falta, cae=cae, n=3, esc=0.95), fondo=(70, 56, 90), k=k,
                alfa=a, objetivo=S.pt(150, -380))
        k2, a2 = ent(t, A.mitad_s - 0.1, A.edificios - 0.3)
        pildora(lz, 1500, 690, "pierden más de la mitad de sus átomos", 28, k=k2, alfa=a2, fondo=ROJO_B, color=(255, 255, 255))
        k3, a3 = ent(t, A.rocas_s - 0.1, A.mitad_s - 0.3)
        pildora(lz, 1500, 690, "rocas · arena · vidrio · concreto", 28, k=k3, alfa=a3)
    for txt, X, Hh, t0, t1 in (("polvo", 640, 520, A.polvo, A.metales - 0.4), ("carreteras", 760, 40, A.carreteras, A.metales - 0.4),
                               ("el suelo se hunde", 120, -60, A.hunde, A.metales - 0.4)):
        k, a = ent(t, t0 - 0.05, t1)
        if a > 0.01:
            x, y = S.pt(X, Hh)
            KU.llamada(lz, x, y, txt, color=ROJO_B, px=30, k=k, alfa=a)
    k, a = ent(t, A.metales - 0.1, A.piezas - 0.4)
    if a > 0.01:
        x, y = S.pt(640, 470)
        KU.llamada(lz, x, y, "el acero sigue ahí", color=(110, 120, 160), px=30, k=k, alfa=a)
        quita = e_out(prog(t, A.oxido - 0.1, A.oxido + 0.6))

        def cont(lz):
            lz.relleno(circulo(0, 0, 260, 40), (40, 36, 70))
            for i in range(-4, 5):
                for j in range(0, 4):
                    KO.atomo(lz, i * 50 + (25 if j % 2 else 0), 40 + j * 46, 24, KO.COL_AT["Fe"], 1.0)
            for i in range(-4, 5):
                KO.atomo(lz, i * 50 + 12, -8, 18, KO.COL_AT["O"], 1 - quita)
                if quita > 0.05:
                    KO.fantasma(lz, i * 50 + 12, -8, 18, alfa=quita * (1 - prog(t, A.oxido + 0.8, A.oxido + 1.6)))
            if quita > 0.3:
                lz.halo(-60, 20, 120, (255, 255, 255), alfa=0.4 * quita * (0.6 + 0.4 * math.sin(t * 5)))
        KB.lupa(lz, 1500, 420, 220, cont, fondo=(40, 36, 70), k=k, alfa=a, objetivo=S.pt(640, 300))
        k2, a2 = ent(t, A.oxido - 0.2, A.piezas - 0.4)
        pildora(lz, 1500, 690, "pierden su capa de óxido", 28, k=k2, alfa=a2)
    k, a = ent(t, A.pegar - 0.1, A.invento + 0.6)
    if a > 0.01:
        X, _, _ = G.pos_kuri(t)
        x, y = S.pt(X, 250)
        KU.llamada(lz, x, y, "¡pegadas!", color=AMARILLO, color_texto=AZUL_OSC, px=34, k=k, alfa=a)
    k, a = ent(t, A.soldadura - 0.1, A.uno_ag - 0.6)
    pildora(lz, W / 2, 210, "soldadura en frío", 44, k=k, alfa=a, fondo=AMARILLO)
    k, a = ent(t, A.naves - 0.4, A.uno_ag - 0.6)
    if a > 0.01:
        def cont(lz):
            lz.relleno(circulo(0, 0, 260, 40), (14, 14, 40))
            for i in range(20):
                lz.relleno(circulo((h01(i, 1) - 0.5) * 400, (h01(i, 2) - 0.5) * 400, 2.5, 8), (240, 240, 255))
            KO.satelite(lz, 0, 40, 1.2, t, pegado=e_out(prog(t, A.naves, A.naves + 0.6)),
                        chispa=campana(t, A.naves + 0.2, A.naves + 1.0))
        KB.lupa(lz, 1480, 600, 230, cont, fondo=(14, 14, 40), k=k, alfa=a)
        pildora(lz, 1480, 880, "naves espaciales", 28, k=k, alfa=a)


# ======================================================================== agua
def agua(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    k, a = ent(t, A.molecula - 0.6, A.oceanos - 0.4)
    if a > 0.01:
        falta = e_out(prog(t, A.molecula - 0.1, A.molecula + 0.4))
        par = e_inout(prog(t, A.hidrogeno_ag - 0.2, A.hidrogeno_ag + 0.8))
        sube = e_in(prog(t, A.ligero_ag - 0.3, A.ligero_ag + 1.6))

        def cont(lz):
            lz.relleno(circulo(0, 0, 260, 40), mezcla((70, 150, 230), (200, 196, 240), par))
            ps = ((-90, -60), (80, -90), (-40, 70), (110, 60))
            for i, (mx, my) in enumerate(ps):
                x, y = mx + 10 * math.sin(t + i), my + 8 * math.cos(t + i) - 260 * sube * (0.7 + 0.3 * h01(i, 3))
                if par < 0.5:
                    KO.molecula(lz, x, y, 1.7, "H2O", rot=0.4 * math.sin(t * 0.7 + i), falta_o=falta, hueco=1.0)
                else:
                    KO.molecula(lz, x, y + 20, 1.7, "H2", rot=t * 1.5 + i)
        KB.lupa(lz, 1480, 380, 240, cont, fondo=(70, 150, 230), k=k, alfa=a, objetivo=S.pt(2950, -150))
        k2, a2 = ent(t, A.ligero_ag - 0.1, A.oceanos - 0.4)
        pildora(lz, 1480, 670, "H2: el gas más ligero", 32, k=k2, alfa=a2, fondo=(236, 242, 255))
    for i, (txt, t0) in enumerate((("océanos", A.oceanos), ("ríos", A.rios), ("nubes", A.nubes))):
        k, a = ent(t, t0 - 0.05, A.fondo_ag - 0.4)
        pildora(lz, W / 2 - 330 + i * 330, 210, txt, 38, k=k, alfa=a, fondo=(110, 180, 250), color=(255, 255, 255))
    k, a = ent(t, A.convierte - 0.1, A.fondo_ag - 0.4)
    pildora(lz, W / 2, 310, "todo se convierte en hidrógeno", 36, k=k, alfa=a)
    # el fondo del mar
    if A.fondo_ag - 0.3 < t < A.treinta:
        cx, cy = S.pt(3600, -1420)
        ap = ventana(t, A.aplastado - 0.2, A.expandiria - 0.2, 0.3, 0.3)
        with lz.capa(2):
            for i in range(8):
                ang = i / 8 * 2 * math.pi
                r0 = 300 - 40 * math.sin(t * 6)
                UB.flecha(lz, (cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                          (cx + 120 * math.cos(ang), cy + 120 * math.sin(ang)), (255, 255, 255), 8, 24, alfa=ap)
            lz.relleno(circulo(cx, cy, 70, 30), (236, 230, 255), alfa=0.85 * ventana(t, A.fondo_ag, A.expandiria, 0.3, 0.1))
            ex = e_out(prog(t, A.expandiria - 0.05, A.brutal + 0.4))
            if ex > 0.001:
                R = 70 + 1500 * ex
                af = 1 - prog(t, A.brutal + 0.6, A.treinta - 0.3)
                lz.relleno(circulo(cx, cy, R, 120), (236, 230, 255), alfa=0.32 * af)
                lz.trazo(P.arco_pts(cx, cy, R, 0, 2 * math.pi, 120), (255, 255, 255, int(220 * af)), 10, afinar=False)
                for j in range(14):
                    ang = j / 14 * 2 * math.pi + 0.3
                    lz.relleno(circulo(cx + R * 0.8 * math.cos(ang), cy + R * 0.8 * math.sin(ang), 30 + 20 * h01(j, 1), 20),
                               (255, 255, 255), alfa=0.45 * af)
        k, a = ent(t, A.kilometros - 0.1, A.expandiria - 0.3)
        pildora(lz, W / 2, 210, "kilómetros de agua encima", 36, k=k, alfa=a)
        k, a = ent(t, A.brutal - 0.1, A.treinta - 0.5)
        pildora(lz, W / 2, 210, "¡se expande de golpe!", 40, k=k, alfa=a, fondo=AMARILLO)
    # balanza: hidrógeno vs. atmósfera
    k, a = ent(t, A.treinta - 1.0, A.nosotros - 0.2)
    if a > 0.01:
        U1._panel(lz, W / 2, 620, 1100, 640, a, k)
        inc = -0.28 * e_out(prog(t, A.treinta - 0.6, A.treinta + 0.6))

        def izq(lz):
            for i in range(26):
                KO.molecula(lz, (i % 7 - 3) * 22, -10 - (i // 7) * 22, 0.55, "H2", rot=i)

        def der(lz):
            KO.nube(lz, 0, -20, 0.32, (210, 230, 255))
        with lz.capa(2):
            KO.balanza(lz, W / 2, 900, 0.95 * k, inclin=inc, izq=izq, der=der)
        pildora(lz, W / 2 - 250, 920, "hidrógeno", 30, k=k, alfa=a, fondo=(236, 242, 255))
        pildora(lz, W / 2 + 250, 920, "atmósfera", 30, k=k, alfa=a, fondo=(150, 200, 250))
        k2, a2 = ent(t, A.treinta - 0.1, A.nosotros - 0.2)
        pildora(lz, W / 2, 380, "×30", 80, k=k2, alfa=a2 * a, fondo=AMARILLO, fuente="geo_x")


# ======================================================================== nosotros
def nosotros(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    k, a = ent(t, A.terceras_n - 0.1, A.agua_n - 0.3)
    pildora(lz, 1500, 260, "2/3 de tu cuerpo", 40, k=k, alfa=a, fondo=ROJO_B, color=(255, 255, 255))
    falta = e_out(prog(t, A.llevan + 0.6, A.llevan + 1.4))
    parp = 0.5 + 0.5 * math.sin(t * 10) if A.llevan - 0.2 < t < A.llevan + 0.8 else 1.0
    for i, (tipo, t0, txt) in enumerate((("agua", A.agua_n, "agua"), ("prot", A.proteinas, "proteínas"),
                                         ("adn", A.genetico, "material genético"))):
        k, a = ent(t, t0 - 0.1, A.version_n - 0.2)
        if a <= 0.01:
            continue
        bx, by = 1250 + i * 270, 380
        with lz.capa(2):
            with lz.grupo(bx, by, k):
                lz.relleno(circulo(4, 8, 115, 50), (10, 6, 40), alfa=0.22 * a)
                lz.relleno(circulo(0, 0, 115, 50), (250, 248, 255), alfa=a)
                with lz.recorte(circulo(0, 0, 112, 50)):
                    if tipo == "agua":
                        KO.molecula(lz, 0, 0, 2.0, "H2O", rot=0.3 * math.sin(t), alfa=a, falta_o=falta, hueco=1.0)
                    elif tipo == "prot":
                        KB.proteina(lz, 0, 0, 0.8, t, falta_o=falta, alfa=a)
                    else:
                        KB.adn(lz, 0, 0, 0.6, t, largo=320, falta_o=falta, alfa=a)
                if A.llevan - 0.2 < t < A.llevan + 0.8:
                    lz.relleno(circulo(0, 0, 115, 50), (255, 90, 100), alfa=0.18 * parp * a)
        pildora(lz, bx, by + 150 * k, txt, 26, k=k, alfa=a)
    k, a = ent(t, A.ser_vivo - 0.2, A.cinco_rb - 0.6)
    pildora(lz, W / 2, 210, "ni un ser vivo en la superficie", 40, k=k, alfa=a)


# ======================================================================== regreso B
def regreso_b(lz, t, ctx):
    S = ctx.get("S")
    ar = ventana(t, A.vuelve_rb - 0.3, A.revuelto - 0.6, 0.2, 0.5)
    if ar > 0.01:
        with lz.capa(2):
            for i in range(160):
                u = ((t - A.vuelve_rb + 0.3) * 0.8 + h01(i, 1)) % 1
                x = h01(i, 2) * W
                y = -40 + u * (H + 80)
                lz.relleno(circulo(x, y, 6 + 3 * h01(i, 3), 10), (255, 90, 100), alfa=ar * min(1.0, u * 4))
    k, a = ent(t, A.vuelve_rb - 0.1, A.revuelto - 0.4)
    pildora(lz, W / 2, 210, "el oxígeno vuelve", 40, k=k, alfa=a, fondo=TEAL, color=(255, 255, 255))
    if S is not None:
        ah = ventana(t, A.revuelto - 0.6, Z3[0] + 0.8, 0.8, 0.6)
        if ah > 0.01:
            with lz.capa(2):
                for i in range(34):
                    X = 300 + 4200 * h01(i, 4) + 60 * math.sin(t * 0.5 + i)
                    Hh = 260 + 1300 * h01(i, 5) + 40 * math.cos(t * 0.4 + i)
                    x, y = S.pt(X, Hh)
                    lz.relleno(circulo(x, y, (160 + 160 * h01(i, 6)) * S.k * (0.9 + 0.1 * math.sin(t + i)), 30), (226, 214, 250),
                               alfa=0.5 * ah)
                for i in range(12):
                    X = 600 + 3600 * h01(i, 8)
                    Hh = 400 + 1000 * h01(i, 9)
                    x, y = S.pt(X, Hh)
                    KO.molecula(lz, x, y, 1.1, "H2", rot=t + i, alfa=ah)
            k, a = ent(t, A.revuelto - 0.1, A.mezclado - 0.4)
            pildora(lz, W / 2, 210, "un planeta revuelto", 40, k=k, alfa=a)
            k, a = ent(t, A.movido - 0.1, A.mezclado - 0.4)
            x, y = S.pt(2400, 1500)
            KU.llamada(lz, x, y, "hidrógeno fuera de su sitio", color=(150, 120, 220), px=30, k=k, alfa=a)
    k, a = ent(t, A.mezclado - 0.3, Z3[0] + 0.3)
    if a > 0.01:
        def cont(lz):
            lz.degradado(circulo(0, 0, 260, 40), (110, 160, 230), (190, 220, 250), (0, -260), (0, 260))
            KO.cohete(lz, 0, 150, 0.62, t, fuego=e_out(prog(t, A.combustible - 0.3, A.combustible + 0.4)))
        KB.lupa(lz, 1500, 500, 250, cont, fondo=(110, 160, 230), k=k, alfa=a)
        k2, a2 = ent(t, A.combustible - 0.1, Z3[0] + 0.3)
        pildora(lz, 1500, 800, "H2 + O2 = combustible de cohete", 30, k=k2, alfa=a2)
    if ctx.get("tierra") is not None and t > A.calcular - 0.4:
        ex, ey, r = ctx["tierra"]
        for i, (dx, dy, s) in enumerate(((-1.3, -0.9, 1.0), (1.35, -0.6, 0.8), (1.2, 0.95, 0.9), (-1.25, 0.8, 0.75))):
            k, a = ent(t, A.calcular - 0.1 + 0.15 * i, A.suerte - 0.6)
            if a > 0.01:
                P.rotulo(lz, ex + dx * r, ey + dy * r, "?", 120 * s, k=k, color=(255, 214, 90), fuente="geo_x", alfa=a)
        k, a = ent(t, A.calcular - 0.1, A.suerte - 0.6)
        pildora(lz, W / 2, 940, "nadie lo puede calcular", 36, k=k, alfa=a)


# ======================================================================== realidad
def realidad(lz, t, ctx):
    if ctx.get("tierra") is None or t < A.suerte - 0.6:
        return
    ex, ey, r = ctx["tierra"]
    # Kuri busca el interruptor
    ak = ventana(t, A.suerte - 0.5, Z4[0] + 0.2, 0.6, 0.4)
    if ak > 0.01:
        xk = float(np.interp(t, [A.suerte, A.interruptor + 0.4, A.siempre_r, A.siempre_r + 1.5], [1700, 1260, 1260, 1720]))
        yk = float(np.interp(t, [A.suerte, A.interruptor + 0.4, A.siempre_r, A.siempre_r + 1.5], [900, 420, 420, 960]))
        with lz.capa(2):
            ME.kuri_espacio(lz, t, xk, yk, 0.6, mirar=(0.8, 0.3) if t < A.siempre_r else (-0.8, -0.3),
                            aleteo=0.8 if A.interruptor - 0.5 < t < A.siempre_r else 0.0, alfa=ak)
    k, a = ent(t, A.interruptor - 0.5, A.siempre_r - 0.2)
    if a > 0.01:
        with lz.capa(2):
            with lz.grupo(1520, 560, k):
                lz.relleno(circulo(0, 0, 170, 50), (28, 24, 70), alfa=0.6 * a)
                P.interruptor(lz, 0, 0, 0.9, encendido=1.0)
                UB.prohibido(lz, 0, 0, 150, a * KU.pop(t, A.interruptor + 0.2))
        pildora(lz, 1520, 800, "el oxígeno no tiene interruptor", 30, k=k, alfa=a)
    k, a = ent(t, A.millones_r - 0.2, A.fabricaron - 0.3)
    pildora(lz, 1460, 360, "hace 2 400 millones de años", 36, k=k, alfa=a, fondo=AMARILLO)
    k, a = ent(t, A.casi_no - 0.1, A.fabricaron - 0.3)
    pildora(lz, 1460, 460, "casi sin O2 en el aire", 32, k=k, alfa=a, icono="cruz", fondo=ROJO_B, color=(255, 255, 255))
    # cianobacterias y fitoplancton
    k, a = ent(t, A.fabricaron - 0.2, Z4[0] + 0.2)
    if a > 0.01:
        hoy = e_inout(prog(t, A.hoy - 0.3, A.hoy + 0.7))

        def cont(lz):
            lz.degradado(circulo(0, 0, 280, 40), mezcla((70, 160, 140), (70, 160, 230), hoy), mezcla((20, 60, 70), (16, 40, 100), hoy),
                         (0, -280), (0, 280))
            luz = e_out(prog(t, A.luz_r - 0.3, A.luz_r + 0.5))
            for i in range(5):
                xx = -200 + i * 100
                lz.relleno(np.array([[xx, -300], [xx + 40, -300], [xx - 40, 300], [xx - 90, 300]]), (255, 250, 200), alfa=0.12 * max(luz, hoy))
            if hoy < 0.99:
                for i in range(4):
                    KB.cianobacteria(lz, -120 + (i % 2) * 220, -80 + (i // 2) * 170, 1.2, t + i * 1.3, n=6, seed=i,
                                     burbujas=luz * (1 - hoy))
            if hoy > 0.01:
                for i in range(7):
                    with lz.grupo(0, 0):
                        KB.diatomea(lz, -170 + (i * 97) % 340, -150 + (i * 131) % 300 + 12 * math.sin(t + i), 1.2 * hoy, t, seed=i,
                                    col=[(140, 220, 200), (200, 230, 140), (150, 200, 240)][i % 3])
        KB.lupa(lz, 1460, 640, 260, cont, fondo=(40, 110, 120), k=k, alfa=a, objetivo=(ex + r * 0.6, ey + r * 0.2))
        k2, a2 = ent(t, A.bacterias - 0.1, A.hoy - 0.3)
        pildora(lz, 1460, 940, "cianobacterias", 32, k=k2, alfa=a2, fondo=(120, 220, 160))
        k3, a3 = ent(t, A.pequenos - 0.1, Z4[0] + 0.2)
        pildora(lz, 1460, 940, "fitoplancton", 32, k=k3, alfa=a3, fondo=(150, 200, 250))
    k, a = ent(t, A.mitad_r - 0.2, Z4[0] + 0.2)
    if a > 0.01:
        KB.tarta(lz, 1460, 250, 120, 0.5, col=(70, 150, 230), texto="≈ 50 %", sub="sale del mar", k=k, alfa=a,
                 crece=e_out(prog(t, A.mitad_r - 0.1, A.mitad_r + 0.8)))


# ======================================================================== cierre
def cierre(lz, t, ctx):
    if t < Z4[1] - 0.3:
        return
    U1.aliento(lz, t, ctx.get("S"), A.aire_c - 0.6, A.regala + 0.6, oro=True)


# ======================================================================== orquesta y posproceso
def dibujar(lz, t, ctx, est):
    if PORTAL_IN[0] < t < PORTAL_OUT[1] + 0.1:
        cuerpo(lz, t, ctx)
    if A.mareo - 0.5 < t < A.cinco_ra:
        mareo(lz, t, ctx, est)
    if A.cinco_ra - 0.5 < t < A.dificil:
        regreso_a(lz, t, ctx)
    if A.dificil - 0.5 < t < A.cero_s + 0.5:
        atomos(lz, t, ctx)
    if A.cero_s - 0.5 < t < A.uno_ag:
        suelo(lz, t, ctx)
    if A.uno_ag - 0.5 < t < A.nosotros + 0.3:
        agua(lz, t, ctx)
    if A.nosotros - 0.5 < t < A.cinco_rb:
        nosotros(lz, t, ctx)
    if A.cinco_rb - 0.5 < t < A.suerte:
        regreso_b(lz, t, ctx)
    if A.suerte - 1 < t < Z4[1]:
        realidad(lz, t, ctx)
    cierre(lz, t, ctx)


_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)
_D = np.sqrt(((_XX - W / 2) / (W / 2)) ** 2 + ((_YY - H / 2) / (W / 2)) ** 2)


def post(img, t, ctx, est):
    tun = est.get("tunel", 0.0)
    if tun > 0.01:
        r0 = lerp(1.3, 0.38, tun)
        m = np.clip(1 - (_D - r0) / 0.22, 0, 1)
        img = img * (0.04 + 0.96 * m[..., None])
    fl = campana(t, A.brutal - 0.05, A.brutal + 0.6)
    if fl > 0.01:
        img = img + (1 - img) * (0.25 * fl)
    return img
