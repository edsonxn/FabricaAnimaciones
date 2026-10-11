# -*- coding: utf-8 -*-
"""Escenas 17-19: palacio (ruinas bajo el Monte de Piedad y las joyas empeñadas), teorias (tres hipótesis animadas) y cierre
(la lluvia, el lago y la codicia; la ciudad de noche sobre el antiguo lago; el obrero que cava; créditos)."""
import math

import numpy as np

from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, catmull, bezier, h01
import plano as P
import mapa_local as ML
import figuras as F
from mundo import degradado_v, llama, humo
from reg import shot, snd
from util import *

PANT = np.array([[0, 0], [W, 0], [W, H], [0, H]], float)
import s_c  # noqa: E402  (reutiliza el montón de barras)
import s_d  # noqa: E402

# ======================================================================== 17. PALACIO / MONTE DE PIEDAD
E17 = "palacio"


def _fachada_mp(lz, x, y, s, t, andamio=0.0):
    """Fachada colonial de tezontle: tres niveles con balcones, portal de arcos y letrero."""
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-470, -560, 940, 560, 4), (190, 92, 82))
        lz.relleno(rect_red(-470, -560, 940, 30, 0), (236, 214, 176))
        lz.relleno(rect_red(-470, -300, 940, 14, 0), (236, 214, 176))
        for r in range(2):
            for c in range(6):
                wx, wy = -412 + c * 150, -500 + r * 130
                lz.relleno(rect_red(wx, wy, 76, 96, 6), (236, 214, 176))
                lz.relleno(rect_red(wx + 8, wy + 8, 60, 80, 4), (66, 90, 150) if (r + c) % 3 else (255, 226, 130))
                lz.relleno(rect_red(wx - 8, wy + 92, 92, 10, 3), (60, 60, 76))
        for c in range(6):
            ax = -430 + c * 150
            lz.relleno(np.array([[ax, 0], [ax, -150], [ax + 20, -190], [ax + 60, -204], [ax + 100, -190], [ax + 120, -150], [ax + 120, 0]]), (54, 34, 52))
        lz.relleno(rect_red(-260, -262, 520, 46, 6), (250, 240, 214))
        P.rotulo(lz, 0, -240, "NACIONAL MONTE DE PIEDAD", px=34, color=(120, 40, 50), sombra=0.0, capa=1)
        if andamio > 0.01:
            for k in range(8):
                lz.relleno(rect_red(-470 + k * 134, -560 * andamio, 7, 560 * andamio, 0), (200, 200, 216))
            for j in range(3):
                lz.relleno(rect_red(-470, -140 - j * 190, 940 * andamio, 7, 0), (200, 200, 216))


def _ruinas(lz, x, y, u):
    """Bloques de basalto que emergen bajo el piso (u 0..1)."""
    if u <= 0.01:
        return
    lz.halo(x, y + 30, 380 * u, (255, 214, 130), alfa=0.35 * u)
    bloques = ((-260, 0, 130, 70), (-120, -6, 110, 76), (10, 0, 140, 70), (160, -4, 120, 74), (-200, 70, 140, 66), (-40, 72, 150, 68), (130, 70, 130, 66))
    for k, (bx, by, bw, bh) in enumerate(bloques):
        a = smooth(prog(u, 0.08 * k, 0.08 * k + 0.5))
        lz.relleno(rect_red(x + bx, y + by + (1 - a) * 60, bw, bh, 5), (86, 80, 100), alfa=a)
        lz.relleno(rect_red(x + bx, y + by + (1 - a) * 60, bw, 12, 3), (128, 122, 146), alfa=a)
    for k in range(2):
        a = smooth(prog(u, 0.5 + 0.1 * k, 0.9))
        lz.relleno(rect_red(x - 200 + k * 360, y - 130 * a, 50, 130 * a, 4), (104, 98, 122))


@shot(T0(E17), bg=lambda t: bg_grad((120, 190, 250), (255, 236, 200), ym=0.5), ent=("tinta", 0.7))
def p_monte(lz, t):
    gy = 720.0
    t_ruinas = w_(E17, 0, 22)
    # ciudad al fondo
    for i in range(10):
        x = -100 + i * 230
        lz.relleno(rect_red(x, gy - 260 - 120 * h01(3, i), 190, 400, 4), (226, 206, 190) if i % 2 else (210, 190, 176))
    _fachada_mp(lz, 760, gy, 1.0, t, andamio=smooth(prog(t, w_(E17, 0, 9), w_(E17, 0, 11))) * (1 - smooth(prog(t, t_ruinas + 3.0, t_ruinas + 4.0))))
    lz.relleno(rect_red(-20, gy, W + 40, 42, 0), (150, 140, 156))
    degradado_v(lz, -20, W + 20, gy + 42, H + 20, (150, 112, 96), (86, 64, 80), gy + 42, H, paso=14.0)
    # zanja del piso interior y ruinas
    prof = K(t, [(w_(E17, 0, 10), 0.0), (t_ruinas, 130.0)], e_inout)
    if prof > 2:
        lz.relleno(rect_red(520, gy + 42, 480, prof, 0), (34, 26, 44))
    _ruinas(lz, 760, gy + 54, smooth(prog(t, t_ruinas, t_ruinas + 2.2)))
    F.obrero(lz, 380, gy, 1.9, t, lado=1, pico=1.0 if w_(E17, 0, 9) < t < t_ruinas + 0.6 else 0.0, seed=5)
    F.obrero(lz, 1130, gy, 1.9, t, lado=-1, pico=1.0 if w_(E17, 0, 9) < t < t_ruinas + 0.6 else 0.0, seed=6)
    # rótulos, palacio en tarjeta y placa real
    cifra(lz, t, w_(E17, 0, 6), "2017", 1560, 130, px=120, col=(34, 28, 80), t1=t_ruinas)
    etq(lz, t, w_(E17, 0, 12), w_(E17, 0, 21) + 0.6, "casa de empeño en el Centro Histórico", 760, 130, px=36)
    a = vent(t, w_(E17, 0, 24), T1(E17) - 0.3, 0.5, 0.3)
    if a > 0.01:
        with lz.capa(2):
            lz.relleno(rect_red(1300, 110, 520, 330, 26), (255, 255, 255), alfa=0.95 * a)
            F.palacio(lz, 1560, 380, 0.7 * a, luz=1.0)
            P.rotulo(lz, 1560, 148, "Palacio de Axayácatl", px=36, color=(34, 28, 80), sombra=0.0, alfa=a)
    b = vent(t, w_(E17, 0, 27), T1(E17) - 0.3, 0.5, 0.3)
    if b > 0.01:
        tarjeta(lz, "monte_piedad_placa", 1560 + 60 * (1 - b), 690, 480, alfa=b, rot=0.03, pie="Placa en el edificio actual")


snd(T0(E17) + 0.2, "viento", 0.2, dur=2.0)
for _k in range(8):
    snd(w_(E17, 0, 10) + 0.5 * _k, "golpe_suave", 0.3)
snd(w_(E17, 0, 22), "revelar", 0.5)
snd(w_(E17, 0, 24), "brillo", 0.35)
snd(w_(E17, 0, 27), "papel", 0.4)


@shot(INI(E17, 1) - 0.1, bg=lambda t: bg_grad((250, 226, 190), (226, 190, 150), ym=0.6), ent=("aberracion", 0.6))
def p_empeno(lz, t):
    # interior de una casa de empeño: estantes con joyas y boletas
    lz.relleno(rect_red(-20, 80, W + 40, 780, 0), (196, 120, 96))
    lz.relleno(rect_red(-20, 780, W + 40, 300, 0), (120, 82, 72))
    lz.relleno(rect_red(240, 160, 1440, 560, 16), (120, 76, 60))
    for r in range(3):
        y = 340 + r * 170
        lz.relleno(rect_red(270, y, 1380, 16, 4), (176, 124, 88))
        lz.relleno(rect_red(270, y - 160, 1380, 160, 0), (150, 96, 74), alfa=0.6)
    tipos = ["anillo", "collar", "reloj", "anillo", "collar", "reloj", "anillo", "collar", "reloj"]
    n = 0
    for r in range(3):
        for c in range(7):
            k = r * 7 + c
            ta = w_(E17, 1, 5) + 0.09 * k
            a = e_back(prog(t, ta, ta + 0.4))
            if a > 0.02:
                x = 350 + c * 200
                y = 340 + r * 170 - 20
                F.joya(lz, x, y - 12, 1.7 * a, tipos[(r + c) % 3 if False else (k % 3)] if False else ("anillo", "collar", "reloj")[k % 3], t)
                lz.relleno(rect_red(x - 22, y + 6, 44, 24, 4), (255, 244, 214), alfa=a)
                P.rotulo(lz, x, y + 18, str(100 + 37 * k % 900), px=16, color=(90, 60, 40), sombra=0.0, alfa=a)
    # mostrador y empleado
    lz.relleno(rect_red(-20, 700, W + 40, 60, 0), (94, 60, 50))
    lz.relleno(rect_red(-20, 690, W + 40, 16, 0), (176, 124, 88))
    P.humano(lz, 1650, 690, 2.4, t, ropa=(120, 90, 170), paso=0.0, brazo=0.2)
    P.humano(lz, 300, 690, 2.4, t, ropa=(84, 170, 140), paso=0.0, brazo=0.2, voltear=True)
    P.rotulo(lz, 960, 110, "MONTE DE PIEDAD", px=64, color=(255, 240, 200), alfa=smooth(prog(t, INI(E17, 1), INI(E17, 1) + 0.5)))
    gran(lz, t, w_(E17, 1, 6), T1(E17) - 0.1, "JOYAS EMPEÑADAS", W / 2, 880, px=84, col=(255, 236, 190))


snd(INI(E17, 1), "whoosh", 0.35, dur=0.6)
for _k in range(21):
    snd(w_(E17, 1, 5) + 0.09 * _k + 0.2, "clink", 0.2, tono=0.8 + 0.03 * (_k % 7))

# ======================================================================== 18. TEORÍAS
E18 = "teorias"


@shot(T0(E18), bg=lambda t: bg_grad((30, 20, 70), (10, 10, 40)), ent=("tinta", 0.7))
def t_pregunta(lz, t):
    s_c._monton(lz, 960, 860, int(21 * smooth(prog(t, T0(E18) + 0.2, T0(E18) + 1.2))), t, 0.3)
    # tres caminos que salen del montón hacia tres iconos
    for k, (x, y, col, ic) in enumerate(((330, 380, (70, 170, 230), "lago"), (960, 260, (170, 120, 90), "cueva"), (1590, 380, (255, 210, 110), "libro"))):
        u = smooth(prog(t, w_(E18, 0, 3) + 0.25 * k, w_(E18, 0, 5) + 0.25 * k))
        if u > 0.01:
            pts = np.array([[960, 640], [(960 + x) / 2, (640 + y) / 2 - 80], [x, y + 90]])
            P.discontinua(lz, catmull(pts, 10), col, ancho=8.0, largo=26, hueco=18, fase=-t * 40, frac=u, capa=2)
            lz.relleno(circulo(x, y, 108 * u, 40), col, alfa=0.9)
            lz.relleno(circulo(x, y, 92 * u, 40), P.oscurecer(col, 0.35), alfa=0.9)
            if ic == "lago":
                for j in range(3):
                    lz.relleno(rect_red(x - 50 + 10 * j, y - 22 + j * 22, 100 - 20 * j, 8, 4), (200, 232, 255), alfa=u)
            elif ic == "cueva":
                lz.relleno(np.array([[x - 60, y + 50], [x - 44, y - 30], [x, y - 60], [x + 44, y - 30], [x + 60, y + 50]]), (36, 24, 40), alfa=u)
                lz.relleno(np.array([[x - 20, y + 50], [x - 14, y - 6], [x + 14, y - 6], [x + 20, y + 50]]), (10, 6, 20), alfa=u)
            else:
                lz.relleno(rect_red(x - 38, y - 48, 76, 96, 8), (250, 240, 214), alfa=u)
                for j in range(4):
                    lz.relleno(rect_red(x - 26, y - 30 + j * 18, 52 - 8 * (j % 2), 5, 2), (100, 70, 60), alfa=u)
    k = e_back(prog(t, INI(E18, 0), INI(E18, 0) + 0.6))
    P.rotulo(lz, 960, 480, "?", px=420, k=0.5 + 0.5 * k, color=(255, 90, 100), alfa=smooth(prog(t, INI(E18, 0), INI(E18, 0) + 0.3)))
    gran(lz, t, INI(E18, 0), INI(E18, 1) - 0.2, "¿QUÉ PASÓ CON EL TESORO?", W / 2, 120, px=76, col=(255, 240, 200))


snd(T0(E18) + 0.2, "latido", 0.5, dur=1.4)
snd(w_(E18, 0, 3), "pop", 0.3)
snd(w_(E18, 0, 4), "pop", 0.3, tono=1.1)
snd(w_(E18, 0, 5), "pop", 0.3, tono=1.2)


@shot(INI(E18, 1) - 0.1, bg=lambda t: bg_grad((150, 200, 250), (255, 236, 200), ym=0.3), ent=("tinta", 0.7))
def t_lago(lz, t):
    """Hipótesis 1: sigue bajo la ciudad (antiguo lecho del lago)."""
    tt = w_(E18, 1, 6)
    s_d_super(lz, t)
    lz.relleno(rect_red(-20, 520, W + 40, 700, 0), (140, 104, 96))
    degradado_v(lz, -20, W + 20, 520, 1200, (150, 116, 96), (58, 50, 84), 520, 1000, paso=16.0)
    # antiguo lago (transparente) por encima del lecho
    lz.relleno(np.array([[-20, 640], [W + 20, 640], [W + 20, 980], [-20, 980]]), (80, 160, 230), alfa=0.30)
    P.discontinua(lz, np.array([[0, 640], [W, 640]]), (200, 236, 255), ancho=4.0, largo=24, hueco=16, fase=-t * 20, capa=2)
    P.pastilla(lz, 300, 610, "nivel del antiguo lago", px=28)
    for i in range(12):
        x = 140 + 150 * i + 30 * math.sin(i)
        y = 860 + 90 * h01(3, i)
        a = smooth(prog(t, tt + 0.1 * i, tt + 0.6 + 0.1 * i))
        if a > 0.01:
            lz.halo(x, y, 50, ORO, alfa=0.6 * a * (0.7 + 0.3 * math.sin(t * 4 + i)))
            F.barra_oro(lz, x, y, 0.5 * a, 0.5 * (h01(4, i) - 0.5), 0.0)
    for k in range(3):
        v = ((t - INI(E18, 1)) * 0.4 + k / 3) % 1.0
        lz.trazo(circulo(960, 520, 40 + 800 * v, 60), (110, 240, 220), 4.0, cerrado=True, temblor=0.0, capa=2)
    gran(lz, t, w_(E18, 1, 10), INI(E18, 2) - 0.2, "BAJO LA CIUDAD", W / 2, 130, px=92, col=(255, 236, 190))
    etq(lz, t, INI(E18, 1), w_(E18, 1, 9), "Hipótesis 1", 960, 250, px=38)


def s_d_super(lz, t):
    """Superficie de la ciudad (edificios y calle) para los cortes de sección."""
    s_d.SY = s_d.SY
    from s_d import _superficie
    with lz.grupo(0, 90, 1.0):
        _superficie(lz, t, -100, 2100)


snd(INI(E18, 1), "whoosh", 0.35, dur=0.6)
for _k in range(4):
    snd(w_(E18, 1, 6) + 0.4 * _k, "bling", 0.25, tono=0.8 + 0.08 * _k)


@shot(INI(E18, 2) - 0.1, bg=lambda t: bg_grad((250, 190, 140), (255, 226, 176), ym=0.5), ent=("fuga", 0.7))
def t_cueva(lz, t):
    """Hipótesis 2: los mexicas lo recuperaron y lo escondieron en una cueva."""
    gy = 860.0
    lz.relleno(np.array([[0, 560], [400, 480], [900, 540], [1300, 400], [1920, 500], [1920, 1080], [0, 1080]]), (170, 110, 110))
    lz.relleno(np.array([[0, 700], [300, 640], [700, 690], [1100, 620], [1500, 680], [1920, 640], [1920, 1080], [0, 1080]]), (196, 130, 100))
    lz.relleno(np.array([[1240, gy], [1300, 560], [1520, 470], [1740, 560], [1800, gy]]), (110, 76, 90))
    lz.relleno(np.array([[1400, gy], [1420, 650], [1520, 600], [1620, 650], [1640, gy]]), (14, 8, 24))
    lz.relleno(rect_red(-20, gy, W + 40, 260, 0), (150, 106, 88))
    ts = w_(E18, 2, 5)
    te = w_(E18, 2, 8)
    for i in range(5):
        x = lerp(120 - 260 * i, 1560, e_inout(prog(t, INI(E18, 2) + 0.2, te + 0.3)) * 1.0 - 0.0) + 0
        x = 200 + (t - INI(E18, 2) - 0.2) * 300 - 240 * i
        if x > 1500:
            continue
        F.guerrero(lz, x, gy + 6 * (i % 2), 1.7, t, paso=1.0, lado=1, arma=None, escudo=False, plumas=i, seed=i + 80, brazos=(-0.6, 0.6))
        F.cofre(lz, x + 16, gy - 190, 0.75, 0.0)
    # la roca que sella la entrada
    u = e_in(prog(t, te + 0.6, te + 1.6))
    if u > 0.01:
        lz.relleno(circulo(lerp(1200, 1520, u), lerp(700, 760, u), 130, 40), (120, 108, 122))
        lz.relleno(circulo(lerp(1200, 1520, u) - 30, lerp(700, 760, u) - 30, 96, 40), (150, 138, 150))
        if u > 0.9:
            for i in range(8):
                lz.relleno(circulo(1520 + 100 * (h01(2, i) - 0.5) * 2 * (t - te - 1.6), 850 - 60 * (t - te - 1.6) * (h01(3, i)), 20 + 20 * (t - te - 1.6), 10), (220, 200, 180), alfa=max(0, 0.5 - 0.3 * (t - te - 1.6)))
    etq(lz, t, INI(E18, 2), te, "Hipótesis 2", 960, 250, px=38)
    gran(lz, t, w_(E18, 2, 7), INI(E18, 3) - 0.2, "LO ESCONDIERON", W / 2, 130, px=92, col=(90, 40, 60))


snd(INI(E18, 2), "whoosh", 0.35, dur=0.6)
snd(INI(E18, 2) + 0.3, "pasos", 0.35, dur=3.6)
snd(w_(E18, 2, 8) + 1.5, "impacto", 0.6)
snd(w_(E18, 2, 8) + 1.6, "puf", 0.5)


@shot(INI(E18, 3) - 0.1, bg=lambda t: bg_grad((44, 30, 90), (18, 12, 50)), ent=("glitch", 0.5))
def t_leyenda(lz, t):
    """Hipótesis 3: la fortuna fue menor de lo que cuenta la leyenda."""
    gy = 870.0
    tt = w_(E18, 3, 8)
    n_ley = int(21 - 15 * smooth(prog(t, tt, tt + 2.2)))
    lz.relleno(rect_red(-20, gy, W + 40, 260, 0), (66, 48, 92))
    # montón "de la leyenda" (enorme, con aura) que se encoge hasta el tamaño real
    esc = 1.0 + 0.9 * (1 - smooth(prog(t, tt, tt + 2.2)))
    with lz.grupo(560, gy, esc * 0.9):
        s_c._monton(lz, 0, 0, n_ley, t, 0.4)
    aura = 0.4 * (1 - smooth(prog(t, tt, tt + 2.2)))
    if aura > 0.02:
        lz.halo(560, gy - 260, 560, ORO, alfa=aura)
    with lz.grupo(1400, gy, 0.9):
        s_c._monton(lz, 0, 0, 6, t, 0.0)
    P.pastilla(lz, 560, 250, "lo que cuenta la leyenda", px=34, alfa=1 - smooth(prog(t, tt + 1.4, tt + 2.2)))
    P.pastilla(lz, 1400, 620, "lo que quizá hubo", px=34)
    # libro de crónicas
    a = smooth(prog(t, w_(E18, 3, 2), w_(E18, 3, 3)))
    if a > 0.01:
        tarjeta(lz, "bernal_portada", 1620, 300, 300, aspecto=1.36, foco=(0.5, 0.32), rot=0.05, alfa=a, pie="Historia verdadera, 1632")
    P.rotulo(lz, 960, 120, "¿UNA FORTUNA MENOR?", px=76, color=(255, 240, 200), alfa=smooth(prog(t, w_(E18, 3, 4), w_(E18, 3, 5))))
    etq(lz, t, INI(E18, 3), w_(E18, 3, 4), "Hipótesis 3 · algunos historiadores", 960, 250, px=38)


snd(INI(E18, 3), "glitch", 0.3)
snd(w_(E18, 3, 8), "siseo", 0.4, dur=1.4)
snd(w_(E18, 3, 10), "hmm", 0.35)

# ======================================================================== 19. CIERRE
E19 = "cierre"


def _mano(lz, x, y, s, a):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-30, -200, 60, 200, 14), (240, 190, 150), alfa=a)
        lz.relleno(rect_red(-56, -20, 112, 70, 20), (240, 190, 150), alfa=a)
        for k in range(4):
            lz.relleno(rect_red(-52 + k * 28, 30, 22, 60 + 6 * (k % 2), 10), (240, 190, 150), alfa=a)
        lz.relleno(rect_red(-72, 4, 26, 30, 12), (240, 190, 150), alfa=a)


@shot(T0(E19), bg=lambda t: bg_grad((6, 8, 30), (22, 24, 70)), post=[lambda i, t: post_lluvia(i, t, 0.8, 0.3, 40, 0.4)], ent=("negro", 0.5))
def z_traga(lz, t):
    tl, tg, tc = w_(E19, 0, 8), w_(E19, 0, 10), w_(E19, 0, 13)
    gy = 830.0
    lz.relleno(rect_red(-20, gy, W + 40, 260, 0), (40, 34, 74))
    # el montón de oro que se va tragando
    n = int(21 - 7 * smooth(prog(t, tg + 0.6, tg + 1.6)) - 7 * smooth(prog(t, tc + 0.4, tc + 1.4)) - 7 * smooth(prog(t, w_(E19, 0, 15), w_(E19, 0, 16) + 0.6)))
    s_c._monton(lz, 960, gy, max(n, 0), t, 0.4)
    # lluvia: nube que descarga
    if t > tl - 0.4:
        a = smooth(prog(t, tl - 0.4, tl + 0.4))
        for k in range(4):
            lz.relleno(circulo(760 + k * 130, 220 + 20 * math.sin(k + t), 90, 30), (120, 130, 170), alfa=0.9 * a)
        for i in range(30):
            ph = (t * 2.0 + i * 0.13) % 1.0
            lz.relleno(rect_red(700 + 22 * i - 6, 300 + ph * 520, 4, 26, 2), (170, 210, 250), alfa=0.8 * a * (1 - ph))
        P.pastilla(lz, 960, 100, "la lluvia", px=44, alfa=a)
    # lago: el agua sube y cubre la mitad
    if t > tg - 0.3:
        lv = smooth(prog(t, tg - 0.3, tg + 1.6))
        yA = lerp(H + 20, gy - 250, lv)
        lz.relleno(rect_red(-20, yA, W + 40, H + 40 - yA, 0), (60, 120, 200), alfa=0.6 * min(1, lv * 2))
        P.pastilla(lz, 480, 460, "el lago", px=44, alfa=smooth(prog(t, tg - 0.3, tg + 0.3)))
    # codicia: una mano se lleva parte
    if t > tc - 0.4:
        u = smooth(prog(t, tc - 0.4, tc + 0.6))
        _mano(lz, 1400, lerp(0, 720, u) if t < tc + 1.0 else lerp(720, -260, smooth(prog(t, tc + 1.0, tc + 1.9))), 1.6, 1.0)
        P.pastilla(lz, 1400, 100, "la codicia", px=44, alfa=smooth(prog(t, tc - 0.4, tc + 0.3)))
    gran(lz, t, w_(E19, 0, 16), T1(E19) - 0.1, "UNA DE LAS MAYORES FORTUNAS DE LA HISTORIA", W / 2, 480, px=54, col=(255, 226, 130)) if False else None
    a = vent(t, w_(E19, 0, 16), FIN(E19, 0) + 0.5, 0.4, 0.3)
    if a > 0.01:
        P.rotulo(lz, W / 2, 520, "una de las mayores fortunas de la historia", px=56, color=(255, 226, 130), alfa=a)


snd(T0(E19), "lluvia", 0.5, dur=3.0)
snd(T0(E19) + 3.0, "lluvia", 0.5, dur=3.0)
snd(w_(E19, 0, 8), "pop", 0.4)
snd(w_(E19, 0, 10), "ola", 0.45, dur=1.6)
snd(w_(E19, 0, 13), "whoosh", 0.4, dur=0.8)
snd(w_(E19, 0, 15), "impacto", 0.5)


@shot(INI(E19, 1) - 0.1, bg=lambda t: bg_plano((14, 16, 50)), ent=("zoom", 0.8))
def z_ciudad(lz, t):
    c = Klog(t, [(INI(E19, 1) - 0.1, (-2.2, 0.0, 3.6)), (w_(E19, 1, 10), (1.5, -1.0, 1.0)), (T1(E19) - 3.0, (2.0, -1.5, 0.8))], e_inout)
    ML.dibujar_valle(lz, t, c, noche=1.0, luces=1.0, detalle=1.0, lago=0.05, moderna=1.0)
    # el antiguo lago, en línea discontinua
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        L = ML.lago_pts(1.0)
        P.discontinua(lz, np.vstack([L, L[:1]]), (140, 210, 250), ancho=6.0 / max(c[2], 0.5), largo=40, hueco=26, fase=-t * 40, frac=smooth(prog(t, w_(E19, 1, 3), w_(E19, 1, 9))), capa=2)
        for k, (x, y) in enumerate(s_d.TESO):
            X, Y = ML.km(x, y)
            lz.halo(X, Y, 40 + 12 * math.sin(t * 4 + k), ORO, alfa=0.7 * smooth(prog(t, w_(E19, 1, 6) + 0.1 * k, w_(E19, 1, 6) + 0.6 + 0.1 * k)))
    etq(lz, t, w_(E19, 1, 3), w_(E19, 1, 9), "el antiguo lago", W / 2, 220, px=38)
    gran(lz, t, w_(E19, 1, 7), INI(E19, 2) - 0.2, "TODAVÍA DUERME EL ORO", W / 2, 130, px=88, col=(255, 226, 130))


snd(INI(E19, 1), "zoom_whoosh", 0.4, dur=1.4)
snd(w_(E19, 1, 6), "brillo", 0.4)
snd(w_(E19, 1, 8), "latido", 0.4, dur=1.2)


@shot(INI(E19, 2) - 0.1, bg=lambda t: bg_grad((90, 170, 240), (255, 226, 190), ym=0.5), ent=("fuga", 0.7))
def z_cimientos(lz, t):
    SYc = 640.0
    tt = w_(E19, 2, 10)
    zoom = K(t, [(INI(E19, 2) - 0.1, 1.0), (w_(E19, 2, 8), 1.0), (w_(E19, 2, 13), 1.5)], e_inout)
    cyy = K(t, [(INI(E19, 2) - 0.1, 540.0), (w_(E19, 2, 13), 760.0)], e_inout)
    with cam(lz, 960, cyy, zoom):
        for i in range(-2, 12):
            lz.relleno(rect_red(i * 220, SYc - 200 - 80 * h01(4, i), 190, 300, 4), (236, 214, 190) if i % 2 else (222, 196, 176))
        # grúa
        lz.relleno(rect_red(1500, SYc - 620, 14, 620, 0), (250, 190, 50))
        lz.relleno(rect_red(1200, SYc - 620, 600, 14, 0), (250, 190, 50))
        lz.trazo(np.array([[1680, SYc - 606], [1680, SYc - 380]]), (60, 60, 76), 3.0, temblor=0.0, capa=1)
        lz.relleno(rect_red(1650, SYc - 380, 60, 34, 4), (60, 60, 76))
        lz.relleno(rect_red(-20, SYc, W + 40, 60, 0), (150, 140, 156))
        degradado_v(lz, -20, W + 20, SYc + 60, SYc + 700, (176, 132, 96), (86, 64, 80), SYc + 60, SYc + 500, paso=16.0)
        prof = K(t, [(INI(E19, 2), 0.0), (tt, 230.0)], e_inout)
        lz.relleno(rect_red(820, SYc + 60, 280, prof, 0), (34, 26, 44))
        F.obrero(lz, 780, SYc + 60, 1.6, t, lado=1, pico=1.0 if t < tt + 0.3 else 0.0, seed=7)
        # el destello en el fondo de la zanja
        a = smooth(prog(t, tt, tt + 0.7))
        if a > 0.01:
            yy = SYc + 60 + prof - 30
            lz.halo(960, yy, 240 * a, ORO, alfa=0.85 * a)
            F.barra_oro(lz, 960, yy, 1.1 * a, 0.2, 1.0)
            for i in range(8):
                ang = i / 8 * 6.283 + t
                lz.trazo(np.array([[960 + math.cos(ang) * 90, yy + math.sin(ang) * 60], [960 + math.cos(ang) * 200, yy + math.sin(ang) * 130]]), (255, 236, 150), 5.0, temblor=0.0, capa=1)
        F.obrero(lz, 780 + 20 * a, SYc + 60, 1.6, t, lado=1, pico=0.0, seed=8) if False else None
    q = smooth(prog(t, w_(E19, 2, 0), w_(E19, 2, 1)))
    P.rotulo(lz, W / 2, 130, "¿Y si la próxima barra…?", px=84, color=(34, 28, 80), sombra=0.0, alfa=q)
    gran(lz, t, w_(E19, 2, 9), T1(E19) - 1.2, "SOLO IBA A CAVAR UNOS CIMIENTOS", W / 2, 250, px=58, col=(120, 60, 100))


snd(INI(E19, 2), "whoosh", 0.35, dur=0.6)
for _k in range(6):
    snd(INI(E19, 2) + 0.7 + 0.6 * _k, "golpe_suave", 0.3)
snd(w_(E19, 2, 10), "revelar", 0.5)
snd(w_(E19, 2, 10) + 0.3, "bling", 0.5)


@shot(T1(E19) - 2.4, bg=lambda t: bg_plano((4, 4, 14)), ent=("negro", 0.6))
def z_creditos(lz, t):
    a = smooth(prog(t, T1(E19) - 2.0, T1(E19) - 1.0))
    P.rotulo(lz, W / 2, 400, "El tesoro perdido de Moctezuma", px=96, color=(255, 226, 130), alfa=a)
    b = smooth(prog(t, T1(E19) - 1.6, T1(E19) - 0.8))
    P.rotulo(lz, W / 2, 560, "Bitácora Perdida · historias que México olvidó", px=38, color=(255, 255, 255), alfa=b)
    P.rotulo(lz, W / 2, 660, "Imágenes históricas: Wikimedia Commons (dominio público) · Mapas: Natural Earth", px=26, color=(200, 200, 220), alfa=b, sombra=0.0)
    P.rotulo(lz, W / 2, 710, "Fuentes: Bernal Díaz del Castillo · Arqueología Mexicana · INAH · Metropolitan Museum of Art", px=26, color=(200, 200, 220), alfa=b, sombra=0.0)


snd(T1(E19) - 2.0, "impacto", 0.5)
