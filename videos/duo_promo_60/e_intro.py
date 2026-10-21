# -*- coding: utf-8 -*-
"""Escena «gancho» (0-8 s): de noche en la sala, Ana y Beto en las dos puntas del sillón, cada quien perdido en su celular
(tarjetitas de redes que suben, el reloj que corre). «Hasta que probamos Dúo»: llega el aviso de una misión, se acercan por el
sillón y sus dos círculos se funden en el logo; luego los círculos vuelan a los avatares del teléfono de Ana (escena medida)."""
import math

import e_medida as EM
from comun import ANA_C, BETO_C, css, utileria
from duo import (A, B, BG, BLANCO, CARD, GOLD, INK, LINE, MUT, O, W, H, ancho_texto, avatar, burst, clamp, e_in, e_io, e_out,
                 hexa, kf, lerp, logo, mix, pop, pr, rnd, smooth, sobre, toast, ww, _corazon)

g_lleg, g_cans = ww("gancho", 0, "llegamos"), ww("gancho", 0, "cansados")
g_cada, g_pierde, g_cel = ww("gancho", 0, "cada"), ww("gancho", 0, "pierde"), ww("gancho", 0, "celular")
h_hasta, h_prob, h_duo = ww("gancho", 1, "hasta"), ww("gancho", 1, "probamos"), ww("gancho", 1, "duo")
T_VUELA = 7.85                        # los círculos del logo vuelan al teléfono de Ana
R_LOGO = 150.0
Y_SOFA = 1300.0
LUZ_CEL = (0.70, 0.84, 1.0)


def sale_sala(t):
    return smooth(pr(t, h_duo - 0.1, h_duo + 0.5))


def x_personas(t):
    """Centros de Ana y Beto: se alejan un poco al «perderse» y se acercan por el sillón en «probamos»."""
    sep = 250 + 40 * e_out(pr(t, g_pierde - 0.1, g_pierde + 0.5))
    sep = lerp(sep, 150, e_io(pr(t, h_prob - 0.1, h_prob + 0.45)))
    return 540 - sep, 540 + sep


# ------------------------------------------------------------------ la sala
def sala(p, t, op):
    if op <= 0.01:
        return
    # ventana con luna y estrellas (plano medio)
    wx0, wy0, wx1, wy1 = 330, 470, 750, 860
    p.rrect(wx0 - 14, wy0 - 14, wx1 + 14, wy1 + 14, 26, hexa("2B2133"), op)
    p.rrect(wx0, wy0, wx1, wy1, 18, hexa("120E22"), op)
    with p.clip(wx0, wy0, wx1, wy1):
        p.glow(640, 560, 220, hexa("6F7BD9"), 0.25 * op, 1.4)
        p.circ(640, 560, 44, hexa("F3EBD8"), op)
        p.circ(622, 548, 40, hexa("120E22"), op)                       # la luna en cuarto creciente
        for i in range(14):
            x = wx0 + 20 + rnd(i, 31) * (wx1 - wx0 - 40)
            y = wy0 + 20 + rnd(i, 32) * (wy1 - wy0 - 40)
            tw = 0.5 + 0.5 * math.sin(t * (2 + rnd(i, 33) * 3) + i)
            p.circ(x, y, 2 + 2 * rnd(i, 34), BLANCO, op * (0.3 + 0.6 * tw))
        for k in range(3):                                            # siluetas de edificios con ventanitas
            bx = wx0 + 30 + k * 130
            bh = 120 + 60 * rnd(k, 35)
            p.rect(bx, wy1 - bh, bx + 100, wy1, hexa("1C1630"), op)
            for j in range(6):
                if rnd(k * 7 + j, 36) > 0.45:
                    p.rect(bx + 14 + (j % 3) * 28, wy1 - bh + 18 + (j // 3) * 34, bx + 28 + (j % 3) * 28, wy1 - bh + 34 + (j // 3) * 34,
                           GOLD, op * 0.55)
    p.rect(wx0, (wy0 + wy1) / 2 - 5, wx1, (wy0 + wy1) / 2 + 5, hexa("2B2133"), op)
    p.rect((wx0 + wx1) / 2 - 5, wy0, (wx0 + wx1) / 2 + 5, wy1, hexa("2B2133"), op)
    # lámpara de pie (izquierda) con su luz cálida tenue
    p.glow(130, 760, 260, sobre(GOLD, BG, 0.5), 0.22 * op, 1.5)
    p.linea((130, 800), (130, 1240), 8, hexa("3A2F44"), op)
    p.poly([(80, 800), (180, 800), (155, 720), (105, 720)], hexa("E9C27A"), op)
    p.rrect(95, 1236, 165, 1252, 8, hexa("3A2F44"), op)
    # planta (derecha)
    for i in range(7):
        a = -1.2 + 0.4 * i + 0.06 * math.sin(t * 1.3 + i)
        x1, y1 = 960 + 120 * math.sin(a), 1120 - 150 * math.cos(a) * (0.8 + 0.3 * rnd(i, 37))
        p.polilinea([(960, 1180), ((960 + x1) / 2, (1180 + y1) / 2 - 20), (x1, y1)], 18, hexa("2F7A55"), op)
    p.rrect(915, 1170, 1005, 1250, 14, hexa("C2603E"), op)
    # piso y tapete
    p.rect(0, 1440, W, H, hexa("150F1A"), op * 0.75)
    p.elip(540, 1520, 470, 70, sobre(B, BG, 0.25), op * 0.8)
    # sillón
    col = hexa("4A3866")
    p.sombra(80, 1080, 1000, 1420, 60, blur=40, op=0.55 * op, dy=24)
    p.rrect(110, 1040, 970, 1300, 70, mix(col, BG, 0.25), op)              # respaldo
    p.rrect(130, 1060, 950, 1090, 20, BLANCO, op * 0.05)
    p.rrect(70, 1240, 1010, 1400, 48, col, op)                            # asiento
    p.rrect(90, 1250, 990, 1272, 12, BLANCO, op * 0.07)
    p.rect(538, 1250, 542, 1395, mix(col, BG, 0.4), op)                    # costura entre cojines
    for x0 in (40, 930):                                                   # brazos
        p.rrect(x0, 1150, x0 + 110, 1410, 46, mix(col, hexa("2E2340"), 0.3), op)
    for x in (120, 960):
        p.rect(x - 12, 1400, x + 12, 1440, hexa("2B2133"), op)
    mesita(p, t, op)


def mesita(p, t, op):
    """Plano delantero: la mesa de centro con dos tazas que ya nadie toma (el vapor se va apagando) y el control de la tele."""
    madera, oscura = hexa("8A5A3C"), hexa("5E3B27")
    p.sombra(250, 1640, 830, 1700, 40, blur=40, op=0.6 * op, dy=30)
    for x in (300, 780):
        p.rrect(x - 16, 1660, x + 16, 1880, 8, oscura, op)
    p.rrect(230, 1620, 850, 1690, 34, madera, op)
    p.rrect(250, 1626, 830, 1640, 7, BLANCO, op * 0.12)
    for i, x in enumerate((420, 650)):
        p.emoji("☕", x, 1580, 96, op)
        apaga = 1 - 0.7 * smooth(pr(t, 1.0, 5.0))
        for k in range(2):
            pts = [(x - 12 + 24 * k + 10 * math.sin(v * 6 - t * 3 + k + i), 1520 - 110 * v) for v in [j / 9 for j in range(10)]]
            p.polilinea(pts, 8, BLANCO, 0.14 * op * apaga)
    p.rrect(505, 1598, 575, 1618, 8, hexa("1E1824"), op)
    for k in range(3):
        p.circ(520 + 18 * k, 1608, 4, MUT, op)


def tarjetita(p, x, y, emo, k, op, s=1.0):
    """Una tarjeta de redes (miniatura + renglones) de las que suben del celular."""
    w, h = 150 * s, 92 * s
    p.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 16 * s, sobre(CARD, BG, 0.9), op, borde=LINE, w=1.5)
    p.rrect(x - w / 2 + 10 * s, y - h / 2 + 10 * s, x - w / 2 + 62 * s, y + h / 2 - 10 * s, 10 * s, sobre(LUZ_CEL, BG, 0.18), op)
    p.emoji(emo, x - w / 2 + 36 * s, y, 34 * s, op)
    for j in range(3):
        p.rrect(x - w / 2 + 72 * s, y - 26 * s + j * 22 * s, x + w / 2 - (14 + 22 * ((k + j) % 3)) * s, y - 16 * s + j * 22 * s,
                5 * s, MUT, op * 0.55)


EMOS = ["▶️", "❤️", "📸", "💬", "😂", "🛒", "🔥", "🎮", "🎵", "👀"]


def persona(p, x, y, letra, col, t, op, cel_on, lado):
    """El círculo de la persona sentado, con el celular delante iluminándole la cara."""
    cans = smooth(pr(t, g_cans, g_cans + 0.5))
    hund = 14 * cans + 4 * math.sin(t * 1.6 + lado)
    yy = y + hund
    if cel_on > 0:
        p.glow(x, yy + 30, 260, LUZ_CEL, 0.22 * cel_on * op, 1.6)
    avatar(p, x, yy, letra, col, 110, op, BG, 6)
    if cel_on > 0:                                                    # la luz fría del celular por debajo
        p.elip(x, yy + 50, 92, 50, LUZ_CEL, 0.10 * cel_on * op)
    # celular en las manos
    cx, cy = x + 40 * lado, yy + 150
    p.sombra(cx - 42, cy - 70, cx + 42, cy + 70, 14, blur=16, op=0.5 * op, dy=8)
    p.rrect(cx - 42, cy - 70, cx + 42, cy + 70, 14, hexa("0C090F"), op, borde=hexa("3A3042"), w=2)
    p.rrect(cx - 36, cy - 62, cx + 36, cy + 62, 10, mix(hexa("1A2033"), LUZ_CEL, 0.55 * cel_on), op)
    if cel_on > 0:
        sc = (t * 120) % 40
        with p.clip(cx - 36, cy - 62, cx + 36, cy + 62):
            for j in range(5):
                yj = cy - 62 + j * 40 - sc
                p.rrect(cx - 28, yj + 6, cx + 28, yj + 30, 6, BLANCO, op * 0.35 * cel_on)
    p.circ(cx - 38 * lado, cy + 10, 16, col, op)                       # mano
    return cx, cy


def bateria(p, x, y, op, t):
    """Pila casi vacía parpadeando (el cansancio)."""
    blink = 0.55 + 0.45 * math.sin(t * 7)
    p.rrect(x - 40, y - 20, x + 34, y + 20, 8, None, op, borde=INK, w=4)
    p.rrect(x + 36, y - 8, x + 44, y + 8, 3, INK, op)
    p.rrect(x - 34, y - 14, x - 18, y + 14, 4, hexa("FF4D5E"), op * blink)


def reloj(p, t, op):
    """El reloj de la pared: 23:47 y, mientras se «pierden», los minutos corren hasta la 1:26."""
    u = e_in(pr(t, g_pierde - 0.1, g_cel + 0.9))
    mins = int(23 * 60 + 47 + u * 99) % (24 * 60)
    hh, mm = mins // 60, mins % 60
    txt = f"{hh}:{mm:02d}"
    x, y = 540, 300
    w = 330
    s = 1.0 + 0.04 * math.sin(math.pi * 2 * ((t * 1.2) % 1)) * u
    with p.pivote(x, y, s):
        p.sombra(x - w / 2, y - 64, x + w / 2, y + 64, 64, blur=30, op=0.5 * op, dy=12)
        p.rrect(x - w / 2, y - 64, x + w / 2, y + 64, 64, CARD, op, borde=LINE, w=2)
        p.emoji("🌙", x - w / 2 + 64, y, 60, op)
        p.texto(txt, x + 40, y + 2, 76, INK, "x", op)
    if u > 0:
        for k in range(3):                                            # «zzz» de la hora
            tz = (t * 0.8 + k / 3) % 1.0
            p.texto("z", x + w / 2 + 20 + 40 * tz, y - 40 - 90 * tz, 30 + 22 * tz, MUT, "x", op * u * math.sin(math.pi * tz))


# ------------------------------------------------------------------ dibujo
def intro(p, t):
    if t > T_VUELA + 0.9:
        return
    sal = sale_sala(t)
    o_sala = 1 - sal
    entra = smooth(pr(t, 0.0, 0.35))
    sala(p, t, o_sala * entra)
    reloj(p, t, o_sala * smooth(pr(t, 0.15, 0.5)))
    xa, xb = x_personas(t)
    cel_on = smooth(pr(t, g_cada - 0.3, g_cada)) * (1 - smooth(pr(t, h_prob - 0.2, h_prob + 0.2)))
    cel_on = max(cel_on, 0.35 * (1 - smooth(pr(t, h_prob - 0.2, h_prob + 0.2))))
    # tarjetitas de redes que suben de cada celular
    if g_cada - 0.2 < t < h_hasta + 0.9:
        tope = h_hasta + 0.1
        dens = 0.20 if t < g_pierde else 0.13
        for lado, xc in ((-1, xa), (1, xb)):
            n0 = int((g_cada - 0.2) / 0.13)
            for k in range(n0, int(tope / 0.13) + 1):
                tk = k * 0.13 + 0.06 * rnd(k, 40 + lado)
                if tk < g_cada - 0.2 or tk > tope or (tk < g_pierde and k % 2):
                    continue
                vida = t - tk
                if not 0 <= vida <= 1.6:
                    continue
                u = vida / 1.6
                x = xc + 40 * lado + (rnd(k, 41 + lado) - 0.5) * 140 + 60 * lado * u
                y = Y_SOFA - 190 - 760 * e_out(u)
                op = math.sin(math.pi * min(1, u * 1.25)) * o_sala * (1 - smooth(pr(t, h_hasta, h_hasta + 0.5)))
                tarjetita(p, x, y, EMOS[(k * 3 + (lado > 0)) % len(EMOS)], k, op, 0.9 + 0.3 * rnd(k, 42))
    # las dos personas (hasta que se funden en el logo)
    if t < h_duo:
        y = Y_SOFA - 210
        for lado, x, letra, col in ((-1, xa, "A", ANA_C), (1, xb, "B", BETO_C)):
            cae = 1 - e_out(pr(t, 0.05 + 0.12 * (lado > 0), 0.5 + 0.12 * (lado > 0)))
            s = 1.0 if cae <= 0 else 1.0
            with p.grupo(0, -600 * cae):
                persona(p, x, y, letra, col, t, entra, cel_on, lado)
            if g_cans <= t < h_prob:
                ob = smooth(pr(t, g_cans, g_cans + 0.3)) * (1 - smooth(pr(t, h_hasta - 0.3, h_hasta)))
                bateria(p, x, y - 175, ob, t + lado)
            on = smooth(pr(t, 0.4, 0.7)) * (1 - smooth(pr(t, h_prob - 0.3, h_prob)))
            p.texto("Ana" if lado < 0 else "Beto", x, y - 160 if not (g_cans <= t < h_hasta) else y - 240, 38, MUT, "b", on)
        # la distancia entre los dos (en «cada quien»)
        od = smooth(pr(t, g_cada, g_cada + 0.3)) * (1 - smooth(pr(t, h_hasta, h_hasta + 0.3)))
        if od > 0:
            yl = Y_SOFA - 40
            for j in range(9):
                x = lerp(xa + 140, xb - 140, j / 8)
                p.circ(x, yl, 5, MUT, od * 0.7)
    # el aviso de Dúo que llega a los dos celulares
    if h_hasta - 0.05 <= t < h_duo + 0.2:
        k = e_out(pr(t, h_hasta - 0.05, h_hasta + 0.35)) * (1 - e_in(pr(t, h_duo - 0.15, h_duo + 0.15)))
        with p.grupo(0, -160 * (1 - k)):
            toast(p, "Dúo: «Dense un abrazo de 20 segundos»", 540, 120, k, 34, "💞")
        for x in (xa, xb):                                             # los celulares vibran
            if t < h_prob:
                v = math.sin(t * 60) * 6 * (1 - smooth(pr(t, h_hasta + 0.6, h_prob)))
                p.glow(x + 40 * (1 if x > 540 else -1) + v, Y_SOFA - 60, 120, A, 0.35, 1.6)
    # los dos círculos -> el logo -> vuelan a los avatares del teléfono de Ana
    if h_duo <= t:
        u = e_io(pr(t, h_duo - 0.05, h_duo + 0.45))
        if t < T_VUELA:
            r = lerp(110, R_LOGO, u)
            cy = lerp(Y_SOFA - 210, 800, u)
            sep = lerp(xb - xa, R_LOGO * 0.88, u)
            p.glow(540, cy, 480, (1.0, 0.6, 0.9), 0.30 * math.exp(-(t - h_duo) * 2.5), 1.5)
            with p.pivote(540, cy, 1.0 + 0.08 * math.sin(math.pi * pr(t, h_duo + 0.3, h_duo + 0.7))):
                logo(p, 540, cy, r, t, 1.0, sep=sep if u < 1 else None, respira=u >= 1)
            burst(p, 540, 800, t, h_duo + 0.2, n=46, fuerza=1.1, semilla=3, escala=1.7)
        else:
            cam = EM.camara(t)
            v = e_io(pr(t, T_VUELA, T_VUELA + 0.7))
            xa2, ya2 = css(cam, EM.tel_ana(t), 400 - 18 - 19 - 28, 80)
            xb2, yb2 = css(cam, EM.tel_ana(t), 400 - 18 - 19, 80)
            rr = lerp(R_LOGO, 19 * cam.z * 1.92, v)
            s0 = R_LOGO * 0.88
            p.circ(lerp(540 - s0 / 2, xa2, v), lerp(800, ya2, v), rr, ANA_C)
            p.circ(lerp(540 + s0 / 2, xb2, v), lerp(800, yb2, v), rr, BETO_C)
        # marca
        sm = smooth(pr(t, T_VUELA - 0.1, T_VUELA + 0.3))
        s = pop(t, h_duo + 0.4, 0.42)
        with p.pivote(540, 1110, s):
            p.texto("Dúo", 540, 1110 - 60 * sm, 190, INK, "x", 1 - sm)
        op = smooth(pr(t, h_duo + 0.6, h_duo + 0.85)) * (1 - sm)
        p.texto("Misiones en pareja", 540, 1250 + 14 * (1 - op) - 60 * sm, 50, hexa("D9CCE0"), "m", op)
