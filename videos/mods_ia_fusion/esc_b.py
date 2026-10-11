# -*- coding: utf-8 -*-
"""Segunda mitad: LA REESCRITURA (binario ilegible -> recompilar -> decompilar -> Skate 3 en Rust, video real) ->
LA VERDAD («una semana» vs. más de dos años a mano) -> CIERRE (mezclar reglas; la pregunta)."""
import math

import numpy as np

from comp import *  # noqa: F401,F403
from comp import HEX, chip, clip_en, cubo, ic_ojo, paquete, pista, slam, tecleo, ventana
from pix import FIN, INI, TOTAL, W, H, ancho_texto, fondo_tecno, ww

R = "reescribir"
rSeg, rNo, rRe = ww(R, 0, "segunda"), ww(R, 0, "no conecta"), ww(R, 0, "reescribe")
rJue, rCod, rMil, rImp = ww(R, 1, "juego"), ww(R, 1, "código"), ww(R, 1, "millones"), ww(R, 1, "imposibles")
rRec, rTra, rOtra, rSin = ww(R, 2, "Recompilar"), ww(R, 2, "traducir"), ww(R, 2, "otra"), ww(R, 2, "sin")
rDec, rCons, rFun, rPers = ww(R, 3, "Decompilar"), ww(R, 3, "reconstruye"), ww(R, 3, "función"), ww(R, 3, "persona")
rSka, rMot, rLib, rLin = ww(R, 4, "Skate"), ww(R, 4, "motor"), ww(R, 4, "libre"), ww(R, 4, "sola")
T_R1, T_R2, T_R3, T_R4 = INI(R, 1) - 0.2, INI(R, 2) - 0.2, INI(R, 3) - 0.2, INI(R, 4) - 0.25

V = "verdad"
vDic, vSem, vNo = ww(V, 0, "Dicen"), ww(V, 0, "semana"), ww(V, 0, "No es")
vAnt, vDos, vMano = ww(V, 1, "Antes"), ww(V, 1, "dos años"), ww(V, 1, "mano")
vMaq, vNada, vConv, vVel = ww(V, 2, "máquina"), ww(V, 2, "nada"), ww(V, 2, "Convirtió"), ww(V, 2, "velocidad")
T_V, T_V1, T_V2 = 82.0, INI(V, 1) - 0.2, INI(V, 2) - 0.2

C = "cierre"
cFue, cReg, cRee, cMez, cCual = ww(C, 0, "fuerte"), ww(C, 0, "reglas"), ww(C, 0, "reescribir"), ww(C, 0, "mezclar"), ww(C, 0, "cualquier")
cLim, cSab, cAtr, cIma = ww(C, 1, "límite"), ww(C, 1, "sabes"), ww(C, 1, "atreves"), ww(C, 1, "imaginar")
cQue = ww(C, 2, "Qué")
T_C, T_C1, T_C2 = 98.0, INI(C, 1) - 0.2, INI(C, 2) - 0.15
CRED2 = "Clip: chasm · YouTube"

KW, FN, NUM, STR, TXT, COM = MAGENTA, CIAN, AMAR, VERDE, BLANCO, GRIS
CODIGO = [                                   # código de ejemplo ORIGINAL (ilustrativo), con colores de editor
    [("fn ", KW), ("ollie", FN), ("(tabla) {", TXT)],
    [("    if ", KW), ("tabla.", TXT), ("en_suelo", FN), ("() {", TXT)],
    [("        tabla.vel_y = ", TXT), ("SALTO", NUM), (";", TXT)],
    [("        ", TXT), ("sonido", FN), ("(", TXT), ('"pop"', STR), (");", TXT)],
    [("    }", TXT)],
    [("}", TXT)],
    [("fn ", KW), ("gravedad", FN), ("(dt) {", TXT)],
    [("    vel_y -= ", TXT), ("9.8", NUM), (" * dt;", TXT)],
    [("}", TXT)],
    [("fn ", KW), ("girar", FN), ("(grados) {", TXT)],
    [("    tabla.rot += grados;", TXT)],
    [("}", TXT)],
]


def hexs(i, n, fase=0):
    return " ".join(HEX[int(rnd(i * 31 + k, fase) * 16)] + HEX[int(rnd(i * 17 + k, fase + 3) * 16)] for k in range(n))


def lluvia_hex(p, t, op=1.0, col=MAGENTA, vel=1.0, y0=0, y1=H, dens=1.0):
    """Columnas de bytes que caen (las instrucciones de máquina)."""
    if op <= 0.01:
        return
    for c in range(18):
        if rnd(c, 77) > dens:
            continue
        x = 40 + c * 59
        v = (120 + 260 * rnd(c, 1)) * vel
        largo = 9 + int(rnd(c, 2) * 12)
        cab = (t * v + rnd(c, 3) * 2600) % (H + largo * 44) - 100
        for k in range(largo):
            y = cab - k * 44
            if not (y0 - 20 < y < y1 + 20):
                continue
            fase = int(t * 7 + k + c * 3)
            b = HEX[int(rnd(c * 7 + k, fase) * 16)] + HEX[int(rnd(c * 5 + k, fase + 1) * 16)]
            p.texto(b, x, y, 34, BLANCO if k == 0 else col, "mono", op * (1.0 if k == 0 else max(0.0, 0.85 - k / largo)))


def linea_codigo(p, segs, x, y, px, n=None, op=1.0):
    """Línea de código con colores; `n` = cuántos caracteres van escritos."""
    quedan = 10 ** 6 if n is None else n
    for txt, col in segs:
        if quedan <= 0:
            break
        s = txt[:quedan]
        p.texto(s, x, y, px, col, "mono", op, "lm")
        x += ancho_texto(txt, px, "mono")
        quedan -= len(txt)
    return x


def cpu(p, x, y, r, col, etiqueta, t, k=1.0):
    if k <= 0.01:
        return
    with p.pivote(x, y, k):
        for i in range(5):
            d = -r * 0.6 + i * r * 0.3
            for a, b in (((x + d, y - r), (x + d, y - r - 20)), ((x + d, y + r), (x + d, y + r + 20)), ((x - r, y + d), (x - r - 20, y + d)),
                         ((x + r, y + d), (x + r + 20, y + d))):
                p.linea(a, b, 7, col)
        p.rrect(x - r, y - r, x + r, y + r, 16, mix(PANEL, col, 0.2), 1, borde=col, w=6)
        p.rrect(x - r * 0.5, y - r * 0.5, x + r * 0.5, y + r * 0.5, 8, mix(PANEL2, col, 0.5 + 0.3 * math.sin(t * 6)))
        p.texto(etiqueta, x, y + r + 58, 36, BLANCO, "xbold")


def persona(p, x, y, s, t, col=LILA, lupa=True):
    """Investigador ORIGINAL sentado ante su pantalla (cabeza, pelo, ojos que parpadean, sudadera, manos); mueve la lupa."""
    with p.grupo(x, y, s):
        p.elip(0, 190, 210, 30, NEGRO, 0.4)
        p.rrect(-150, 20, 150, 200, 60, col)                                     # torso (sudadera)
        p.rrect(-150, 20, 150, 200, 60, None, borde=mix(col, NEGRO, 0.35), w=5)
        p.poly([(-40, 20), (40, 20), (0, 70)], mix(col, NEGRO, 0.35))              # capucha/cuello
        p.rect(-22, -12, 22, 34, (0.86, 0.66, 0.52))                               # cuello
        cab = 3 * math.sin(t * 1.4)
        p.circ(0, -70 + cab, 78, (0.96, 0.76, 0.60))                               # cabeza
        p.elip(0, -100 + cab, 82, 62, (0.16, 0.11, 0.10), a0=180, a1=360)          # pelo
        p.poly([(-82, -100 + cab), (-60, -60 + cab), (-70, -110 + cab)], (0.16, 0.11, 0.10))
        par = 1.0 if (t * 0.4) % 1 > 0.06 else 0.12
        mx = 5 * math.sin(t * 2.2)
        for sx in (-1, 1):
            p.elip(sx * 30 + mx, -66 + cab, 13, 15 * par, BLANCO)
            p.circ(sx * 30 + mx * 1.5, -64 + cab, 7 * par, (0.10, 0.10, 0.16))
            p.linea((sx * 16, -92 + cab), (sx * 46, -96 + cab - 3 * (sx > 0)), 6, (0.16, 0.11, 0.10))   # cejas (concentrado)
        p.elip(0, -30 + cab, 16, 7, (0.55, 0.25, 0.25), a0=0, a1=180)              # boca
        for sx in (-1, 1):                                                         # gafas
            p.circ(sx * 30, -66 + cab, 26, (0.10, 0.10, 0.16), w=5)
        p.linea((-6, -66 + cab), (6, -66 + cab), 5, (0.10, 0.10, 0.16))
        ax, ay = 170 + 60 * math.sin(t * 2.0), 60 + 26 * math.cos(t * 2.6)
        p.polilinea([(120, 70), (150, 120), (ax - 10, ay + 30)], 44, mix(col, NEGRO, 0.15))   # brazo derecho
        p.circ(ax - 6, ay + 22, 25, (0.96, 0.76, 0.60))                            # mano
        if lupa:
            p.linea((ax, ay + 10), (ax + 44, ay - 46), 12, (0.30, 0.22, 0.16))
            p.circ(ax + 78, ay - 86, 52, (0.75, 0.95, 1.0), 0.28)
            p.circ(ax + 78, ay - 86, 52, AMAR, w=9)
        p.polilinea([(-120, 70), (-160, 130), (-110, 160)], 44, mix(col, NEGRO, 0.15))        # brazo izquierdo
        p.circ(-104, 160, 25, (0.96, 0.76, 0.60))


def disco(p, x, y, r, t, k=1.0):
    if k <= 0.01:
        return
    with p.pivote(x, y, k):
        p.glow(x, y, r * 2.2, MAGENTA, 0.25)
        p.circ(x, y, r, (0.80, 0.84, 0.95))
        for i in range(3):                                                         # reflejos que giran
            a = t * 80 + i * 120
            p.elip(x, y, r * 0.96, r * 0.96, (CIAN, MAGENTA, AMAR)[i], 0.55, a0=a, a1=a + 38)
        p.circ(x, y, r * 0.36, (0.12, 0.13, 0.22))
        p.circ(x, y, r * 0.13, FONDO0)
        p.circ(x, y, r, BLANCO, 0.8, w=4)


# ====================================================================== LA REESCRITURA
def reescribir(p, t):
    fondo_tecno(p, t, MAGENTA, AMAR)
    fx = dict(golpe=0.0, glitch=0.0, flash=0.0)
    ent = pr(t, 52.0, 52.5)
    # lluvia de instrucciones al fondo (más densa en la frase 2)
    d = 0.25 + 0.75 * smooth(pr(t, rMil - 0.2, rMil + 0.5)) - 0.6 * smooth(pr(t, T_R2, T_R2 + 0.5))
    lluvia_hex(p, t, 0.8 * ent * (0.6 + 0.4 * d) * (1 - 0.5 * smooth(pr(t, T_R4, T_R4 + 0.5))), MAGENTA, 0.6 + 0.9 * d, dens=clamp(d + 0.45))
    p.im *= np.float32(0.62)
    chip(p, "2 · LA REESCRITURA", 540, 96, 46, MAGENTA, t, T_R1 - 0.2, sale=T_V - 0.5)
    # ---- frase 1: no conecta nada, lo reescribe todo
    if t < T_R1 + 0.3:
        s1 = T_R1 - 0.05
        slam(p, "FORMA 2", 540, 560, 70, BLANCO, t, 52.15, "xbold", sale=s1, esp=0.14)
        slam(p, "NO CONECTA", 540, 760, 130, GRIS, t, rNo, sale=rRe - 0.1)
        slam(p, "NADA", 540, 910, 150, GRIS, t, rNo + 0.35, sale=rRe - 0.1)
        if rNo + 0.5 < t < rRe:                                                    # el puente, tachado
            u = pr(t, rNo + 0.5, rNo + 0.75)
            p.linea((180, 1010), (lerp(180, 900, u), 660), 22, ROJO)
        slam(p, "LO", 540, 700, 110, BLANCO, t, rRe - 0.25, sale=s1)
        slam(p, "REESCRIBE", 540, 860, 170, MAGENTA, t, rRe, sale=s1)
        slam(p, "TODO", 540, 1070, 250, AMAR, t, rRe + 0.55, sale=s1)
        if t > rRe + 0.1:
            p.rrect(110, 1260, 970, 1360, 16, (0.02, 0.02, 0.05), 0.9 * (1 - pr(t, s1, s1 + 0.2)), borde=VERDE, w=4, op_b=1 - pr(t, s1, s1 + 0.2))
            if t < s1:
                tecleo(p, "> reescribir --todo --desde-cero", 140, 1312, 40, VERDE, t, rRe + 0.15, 30)
        fx["golpe"] += 0.6 * golpe(t, rNo, 0.25) + 0.9 * golpe(t, rRe, 0.3) + 1.0 * golpe(t, rRe + 0.55, 0.35)
        fx["flash"] += 0.5 * (1 - ent) + 0.2 * golpe(t, rRe + 0.55, 0.25)
    # ---- frase 2: el disco no trae código: trae millones de instrucciones ilegibles
    if T_R1 <= t < T_R2 + 0.3:
        s2 = T_R2 - 0.05
        o = 1 - pr(t, s2, s2 + 0.25)
        kd = pop(t, T_R1 + 0.05, 0.4) * o
        gira = t * 1.0
        disco(p, 540, 470 + 14 * math.sin(t * 2), 200, gira, kd)
        chip(p, "TU JUEGO", 540, 740, 54, BLANCO, t, rJue, sale=rMil - 0.15)
        if rCod - 0.15 <= t < rMil:                                                # «código fuente»: no viene
            kk = pop(t, rCod - 0.15, 0.3)
            with p.pivote(540, 1150, kk):
                p.rrect(90, 960, 990, 1340, 30, mix(PANEL, VERDE, 0.1), 0.95, borde=GRIS, w=6)
                for i, segs in enumerate(CODIGO[:3]):                              # el código que NO viene, en gris
                    linea_codigo(p, [(s_, GRIS2) for s_, _ in segs], 140, 1015 + i * 46, 30)
                p.texto("CÓDIGO FUENTE", 540, 1200, 92, GRIS, "black")
                p.texto("no viene en la caja", 540, 1290, 46, BLANCO, "semi")
                u = pr(t, rCod + 0.15, rCod + 0.4)
                p.linea((120, 1310), (lerp(120, 960, u), lerp(1310, 990, u)), 24, ROJO, 1.0 if u > 0 else 0)
        if t >= rMil - 0.1:                                                        # chorro de bytes desde el disco + contador
            oo = pr(t, rMil - 0.1, rMil + 0.2) * o
            for i in range(9):
                y = 760 + i * 74 + 8 * math.sin(t * 5 + i)
                p.rrect(60, y - 31, 1020, y + 31, 10, (0.03, 0.02, 0.07), 0.82 * oo * pr(t, rMil + i * 0.05, rMil + 0.2 + i * 0.05))
                p.texto(hexs(i, 16, int(t * 9 + i)), 540, y, 42, mix(MAGENTA, BLANCO, 0.25 if i % 3 else 0.7), "mono",
                        oo * pr(t, rMil + i * 0.05, rMil + 0.2 + i * 0.05))
            n = int(4812304 * e_out(pr(t, rMil, rImp + 0.4)))
            p.rrect(150, 1455, 930, 1610, 26, (0.02, 0.02, 0.06), 0.93 * oo, borde=MAGENTA, w=5, op_b=oo)
            p.texto(f"{n:,}".replace(",", " "), 540, 1505, 86, AMAR, "mono", oo)
            p.texto("INSTRUCCIONES DE MÁQUINA", 540, 1578, 32, BLANCO, "xbold", oo, esp=0.05)
        if t >= rImp - 0.1:
            kk = pop(t, rImp - 0.1, 0.3) * o
            with p.pivote(540, 1030, kk):
                p.rrect(170, 930, 910, 1130, 30, (0.03, 0.02, 0.06), 0.95, borde=ROJO, w=8)
                p.texto("ILEGIBLE", 540, 1000, 120, ROJO, "black")
                p.texto("para una persona", 540, 1092, 40, BLANCO, "semi")
        fx["golpe"] += 0.5 * golpe(t, rCod + 0.15, 0.25) + 0.7 * golpe(t, rMil, 0.3) + 0.8 * golpe(t, rImp - 0.05, 0.3)
        fx["glitch"] += 0.5 * golpe(t, rImp - 0.05, 0.5)
    # ---- frase 3: RECOMPILAR = traducir para otra máquina, sin entender
    if T_R2 <= t < T_R3 + 0.3:
        s3 = T_R3 - 0.05
        o = 1 - pr(t, s3, s3 + 0.25)
        slam(p, "RECOMPILAR", 540, 250, 124, AMAR, t, rRec, sale=s3)
        cpu(p, 540, 520, 112, MAGENTA, "MÁQUINA ORIGINAL", t, pop(t, rRec + 0.2, 0.35) * o)
        cpu(p, 540, 1310, 112, CIAN, "OTRA MÁQUINA: TU PC", t, pop(t, rOtra - 0.1, 0.35) * o)
        kc = pop(t, rTra - 0.15, 0.35) * o
        if kc > 0.01:
            with p.pivote(540, 930, kc):
                p.rrect(130, 790, 950, 1075, 34, (0.02, 0.02, 0.05), 0.98, borde=AMAR, w=8)
                p.texto("TRADUCTOR", 540, 856, 70, AMAR, "black", esp=0.06)
                for i in range(3):                                                 # engranes simples girando
                    gx, gy, gr = 300 + i * 240, 975, 60
                    for q in range(8):
                        a = t * (2.5 if i % 2 else -2.5) + q * math.pi / 4
                        p.linea((gx, gy), (gx + gr * math.cos(a), gy + gr * math.sin(a)), 16, mix(AMAR, NEGRO, 0.25))
                    p.circ(gx, gy, 38, AMAR)
                    p.circ(gx, gy, 14, (0.02, 0.02, 0.05))
        if t >= rTra:                                                              # bytes que bajan, entran magenta y salen cian
            for i in range(7):
                u = (t * 0.55 + i / 7) % 1
                y = lerp(700, 1180, u)
                dentro = 770 < y < 1095
                if not dentro:
                    p.texto(hexs(i, 4, int(t * 6)), 540 + 290 * (i % 3 - 1), y, 44, MAGENTA if y < 930 else CIAN, "mono",
                            o * min(1.0, 6 * u, 6 * (1 - u)))
            pista(p, [(540, 652), (540, 782)], MAGENTA, t, 0.9 * o)
            pista(p, [(540, 1083), (540, 1178)], CIAN, t, 0.9 * o * pr(t, rOtra - 0.1, rOtra + 0.2))
        if t >= rSin - 0.05:
            kk = pop(t, rSin - 0.05, 0.3) * o
            with p.pivote(540, 1610, kk):
                p.rrect(110, 1540, 970, 1680, 70, mix(PANEL, ROJO, 0.2), 0.96, borde=ROJO, w=6)
                ic_ojo(p, 215, 1610, 48, GRIS, 0.02, (0, 0))
                p.linea((150, 1665), (280, 1555), 14, ROJO)
                p.texto("SIN ENTENDER NADA", 590, 1613, 60, BLANCO, "black")
        fx["golpe"] += 0.8 * golpe(t, rRec, 0.3) + 0.5 * golpe(t, rTra - 0.1, 0.25) + 0.5 * golpe(t, rOtra, 0.25) + 0.7 * golpe(t, rSin, 0.3)
    # ---- frase 4: DECOMPILAR = reconstruir el código, función por función, legible
    if T_R3 <= t < T_R4 + 0.35:
        s4 = T_R4 - 0.05
        o = 1 - pr(t, s4, s4 + 0.3)
        slam(p, "DECOMPILAR", 540, 250, 124, VERDE, t, rDec, sale=s4)
        ke = pop(t, rDec + 0.25, 0.4) * o
        if ke > 0.01:
            with p.pivote(540, 900, min(ke, 1.05)):
                ventana(p, 50, 360, 1030, 1330, "juego_reconstruido.rs", "EDITOR", VERDE, t, op=min(1.0, ke))
                for i, segs in enumerate(CODIGO):
                    y = 480 + i * 68
                    ti = rCons + i * (rPers - 0.3 - rCons) / len(CODIGO)
                    p.texto(f"{i + 1:2d}", 110, y, 34, GRIS2, "mono", 1, "rm")
                    u = pr(t, ti, ti + 0.45)
                    if u < 1:                                                      # todavía bytes (o a medio transformar)
                        p.texto(hexs(i + 40, 13, int(t * 10)), 140, y, 36, MAGENTA, "mono", 0.8 * (1 - u), "lm")
                    if u > 0:
                        total = sum(len(s_) for s_, _ in segs)
                        linea_codigo(p, segs, 140, y, 38, int(total * e_out(u)) + 1)
                        if u < 1:
                            p.glow(140 + 600 * u, y, 90, VERDE, 0.5)
                for k, (a, b, nom) in enumerate(((0, 5, "ollie"), (6, 8, "gravedad"), (9, 11, "girar"))):   # función por función
                    tf = rCons + (b + 1) * (rPers - 0.3 - rCons) / len(CODIGO) + 0.3
                    kk = pop(t, tf, 0.3)
                    if kk > 0.01:
                        y0, y1 = 480 + a * 68 - 30, 480 + b * 68 + 30
                        p.polilinea([(1000, y0), (1014, y0), (1014, y1), (1000, y1)], 6, VERDE, min(1.0, kk))
                        with p.pivote(905, (y0 + y1) / 2, kk):
                            p.rrect(815, (y0 + y1) / 2 - 34, 995, (y0 + y1) / 2 + 34, 34, VERDE)
                            p.texto("LISTA", 905, (y0 + y1) / 2 + 2, 34, (0.02, 0.08, 0.04), "black")
        chip(p, "FUNCIÓN POR FUNCIÓN", 540, 1405, 52, VERDE, t, rFun, sale=rPers - 0.25)
        if t >= rPers - 0.3:
            kk = pop(t, rPers - 0.3, 0.35) * o
            if kk > 0.01:
                with p.pivote(540, 1560, kk):
                    persona(p, 250, 1500, 0.72, t, LILA, lupa=False)
                    p.rrect(430, 1455, 1010, 1590, 30, mix(PANEL, VERDE, 0.2), 0.96, borde=VERDE, w=6)
                    p.texto("LEGIBLE", 720, 1502, 78, VERDE, "black")
                    p.texto("ya se puede modificar", 720, 1560, 32, BLANCO, "semi")
        fx["golpe"] += 0.8 * golpe(t, rDec, 0.3) + 0.6 * golpe(t, rPers - 0.25, 0.3)
    # ---- frase 5: así renació Skate 3 (video real) en un motor nuevo y libre, sin una línea del original
    if t >= T_R4:
        e = e_back(pr(t, T_R4, T_R4 + 0.5), 1.1)
        with p.grupo(0, (1 - e) * -900):
            ix = ventana(p, 40, 170, 1040, 812, "skate-3-rust-engine", "REESCRITURA", CIAN, t)
            clip_en(p, "skate_rust", 8.0 + (t - T_R4) * 1.0, *ix, r=12, credito=CRED2)
            if t > rSka + 0.3:
                p.rrect(ix[0] + 16, ix[1] + 14, ix[0] + 326, ix[1] + 66, 26, NEGRO, 0.7)
                p.circ(ix[0] + 44, ix[1] + 40, 11, ROJO, 0.4 + 0.6 * (int(t * 2.4) % 2))
                p.texto("GAMEPLAY REAL", ix[0] + 66, ix[1] + 41, 28, BLANCO, "xbold", 1, "lm")
        with p.clip(60, 1140, 1020, 1660):                                         # el código nuevo sigue corriendo debajo
            oc = 0.38 * pr(t, T_R4 + 0.2, T_R4 + 0.6) * (1 - pr(t, T_V - 0.35, T_V - 0.1))
            for i in range(12):
                yy = 1150 + ((i * 52 - (t - T_R4) * 90) % 624)
                linea_codigo(p, CODIGO[i % len(CODIGO)], 130, yy, 34, None, oc * min(1.0, (yy - 1140) / 70, (1700 - yy) / 110))
        slam(p, "SKATE 3", 540, 930, 150, BLANCO, t, rSka, sale=rMot - 0.15)
        slam(p, "RENACIÓ", 540, 1075, 90, CIAN, t, rSka + 0.3, sale=rMot - 0.15)
        chip(p, "MOTOR NUEVO · Rust + Bevy", 540, 920, 54, CIAN, t, rMot, sale=T_V - 0.35)
        chip(p, "LIBRE · código abierto", 540, 1050, 54, VERDE, t, rLib, sale=T_V - 0.35)
        if t >= rLin - 0.4:
            kk = pop(t, rLin - 0.4, 0.35) * (1 - pr(t, T_V - 0.35, T_V - 0.1))
            n = int(lerp(52840, 0, e_out(pr(t, rLin - 0.35, rLin + 0.45))))
            with p.pivote(540, 1380, kk):
                p.rrect(90, 1170, 990, 1590, 36, (0.02, 0.03, 0.07), 0.96, borde=AMAR, w=8)
                p.texto(f"{n}", 540, 1320, 270 if n < 10 else 170, AMAR, "black")
                p.texto("LÍNEAS DEL CÓDIGO ORIGINAL", 540, 1505, 50, BLANCO, "black")
        fx["golpe"] += 0.7 * golpe(t, T_R4 + 0.4, 0.3) + 0.6 * golpe(t, rSka, 0.25) + 1.0 * golpe(t, rLin + 0.45, 0.4)
        fx["flash"] += 0.18 * golpe(t, rLin + 0.45, 0.3)
        fx["glitch"] += 0.8 * pr(t, T_V - 0.3, T_V)
    return fx


# ====================================================================== LA VERDAD
def verdad(p, t):
    fondo_tecno(p, t, AMAR, CIAN)
    fx = dict(golpe=0.0, glitch=0.9 * (1 - pr(t, T_V, T_V + 0.3)), flash=0.0)
    chip(p, "PERO OJO", 540, 96, 46, AMAR, t, T_V + 0.1, sale=T_C - 0.5)
    # ---- frase 1: «lo hizo en una semana» ... no es toda la verdad
    if t < T_V1 + 0.3:
        s1 = T_V1 - 0.05
        o = 1 - pr(t, s1, s1 + 0.25)
        kk = pop(t, vDic - 0.15, 0.35) * o
        tor = 1 + 0.02 * math.sin(t * 3)
        if kk > 0.01:
            with p.pivote(540, 760, kk * tor):
                p.rrect(70, 330, 1010, 1230, 40, (0.05, 0.06, 0.12), 0.97, borde=GRIS, w=5)
                p.circ(160, 420, 46, CIAN)                                         # avatar genérico de red social
                p.circ(160, 404, 18, FONDO0)
                p.elip(160, 452, 30, 22, FONDO0, a0=180, a1=360)
                p.texto("lo_dicen_en_redes", 232, 402, 40, BLANCO, "bold", 1, "lm")
                p.texto("hace 2 h · 1,2 M de vistas", 232, 450, 30, GRIS, "med", 1, "lm")
                p.texto("«LA IA LO HIZO", 540, 590, 96, BLANCO, "black")
                p.texto("EN UNA SEMANA»", 540, 705, 96, AMAR, "black")
                for d in range(7):                                                 # los siete días se van llenando
                    x = 150 + d * 130
                    lleno = pr(t, vSem - 0.5 + d * 0.09, vSem - 0.4 + d * 0.09)
                    p.rrect(x - 52, 850, x + 52, 960, 14, mix(PANEL2, AMAR, lleno), 1, borde=AMAR, w=4)
                    p.texto("LMXJVSD"[d], x, 906, 54, mix(GRIS, FONDO0, lleno), "black")
                p.texto("7 DÍAS", 540, 1070, 110, AMAR, "black", pr(t, vSem, vSem + 0.15))
        if t >= vNo - 0.05:
            ks = pop(t, vNo - 0.05, 0.28) * o
            with p.pivote(540, 1410, ks):
                p.rrect(110, 1310, 970, 1510, 26, mix(PANEL, ROJO, 0.3), 0.97, borde=ROJO, w=10)
                p.texto("FALTA CONTEXTO", 540, 1380, 82, ROJO, "black")
                p.texto("no es toda la verdad", 540, 1462, 42, BLANCO, "semi")
        fx["golpe"] += 0.5 * golpe(t, vDic, 0.25) + 0.6 * golpe(t, vSem, 0.25) + 1.0 * golpe(t, vNo, 0.4)
        fx["glitch"] += 0.6 * golpe(t, vNo, 0.5)
    # ---- frase 2: antes, una persona pasó más de dos años a mano
    if T_V1 <= t < T_V2 + 0.3:
        s2 = T_V2 - 0.05
        o = 1 - pr(t, s2, s2 + 0.25)
        kp = pop(t, vAnt - 0.1, 0.4) * o
        if kp > 0.01:
            with p.pivote(540, 520, kp):
                p.rrect(560, 300, 1000, 640, 22, (0.02, 0.03, 0.07), 0.97, borde=LILA, w=6)     # su pantalla, llena de bytes
                for i in range(6):
                    p.texto(hexs(i + 9, 7, int(t * 3 + i)), 780, 352 + i * 48, 30, mix(MAGENTA, GRIS, 0.4), "mono")
                p.rect(730, 640, 830, 690, GRIS2)
                p.rect(640, 690, 920, 712, GRIS2)
                persona(p, 300, 500, 1.0, t, LILA)
                p.rect(40, 712, 1040, 734, mix(GRIS2, LILA, 0.3))                               # mesa
        slam(p, "+2 AÑOS", 540, 850, 170, LILA, t, vDos - 0.1, sale=s2)
        if t >= vDos - 0.1:                                                        # 104 semanas, una casilla por semana
            oo = pr(t, vDos - 0.1, vDos + 0.1) * o
            for i in range(104):
                c, f = i % 13, i // 13
                x, y = 122 + c * 70, 1010 + f * 62
                lleno = pr(t, vDos + i * 0.012, vDos + 0.1 + i * 0.012)
                p.rrect(x - 28, y - 24, x + 28, y + 24, 8, mix(PANEL2, LILA, lleno), oo)
            x, y = 122 + 12 * 70 + 0, 1010 + 8 * 62                                 # la semana de la IA, al final
            ki = pop(t, vMano - 0.2, 0.3) * o
            p.rrect(122 - 28, y - 24, 122 + 28, y + 24, 8, AMAR, ki)
            p.texto("<- 1 semana: la IA", 180, y + 2, 38, AMAR, "black", ki, "lm")
            p.texto("104 SEMANAS A MANO", 540, 950, 40, BLANCO, "xbold", oo, esp=0.05)
        chip(p, "DESCIFRANDO A MANO", 540, 1640, 52, LILA, t, vMano - 0.25, sale=s2)
        fx["golpe"] += 0.5 * golpe(t, vAnt, 0.25) + 0.9 * golpe(t, vDos, 0.3)
    # ---- frase 3: la máquina no descubrió nada; convirtió el conocimiento en código, rapidísimo
    if t >= T_V2:
        o = 1 - pr(t, T_C - 0.35, T_C - 0.05)
        cpu(p, 540, 880, 120, AMAR, "", t, pop(t, vMaq - 0.15, 0.35) * o)
        p.texto("IA", 540, 882, 76, FONDO0, "black", pr(t, vMaq, vMaq + 0.1) * o)
        slam(p, "NO DESCUBRIÓ", 540, 300, 92, BLANCO, t, vNada - 0.6, sale=vConv - 0.15)
        slam(p, "NADA", 540, 440, 170, ROJO, t, vNada, sale=vConv - 0.15)
        if t >= vConv - 0.1:
            oo = pr(t, vConv - 0.1, vConv + 0.15) * o
            p.texto("CONOCIMIENTO", 540, 250, 60, LILA, "black", oo, esp=0.05)
            for i in range(5):                                                     # notas de la persona que bajan a la máquina
                u = ((t - vConv) * (0.9 + 0.5 * smooth(pr(t, vVel - 0.3, vVel + 0.5))) + i / 5) % 1
                x, y = 540 + 250 * math.sin(i * 2.1) * (1 - u), lerp(330, 760, u)
                s = 1 - 0.6 * u
                p.rrect(x - 70 * s, y - 50 * s, x + 70 * s, y + 50 * s, 10, mix(BLANCO, LILA, 0.25), oo * min(1.0, 5 * u, 5 * (1 - u)))
                for q in range(3):
                    p.rect(x - 50 * s, y - 28 * s + q * 24 * s, x + (40 - 18 * q) * s, y - 20 * s + q * 24 * s, GRIS2, oo * min(1.0, 5 * u, 5 * (1 - u)))
            vel = 1 + 7 * smooth(pr(t, vVel - 0.4, vVel + 0.6))
            p.texto("CÓDIGO", 540, 1090, 60, VERDE, "black", oo, esp=0.05)
            with p.clip(60, 1130, 1020, 1700):
                for i in range(16):                                                # código que sale cada vez más rápido
                    yy = 1150 + ((i * 56 - (t - vConv) * 130 * vel) % 896)
                    segs = CODIGO[i % len(CODIGO)]
                    linea_codigo(p, segs, 120, yy, 36, None, oo * min(1.0, (yy - 1130) / 80, (1700 - yy) / 120))
            if t >= vVel - 0.2:
                kv = pop(t, vVel - 0.2, 0.3) * o
                with p.pivote(540, 1420, kv):
                    p.rrect(120, 1340, 960, 1500, 80, (0.02, 0.03, 0.07), 0.94, borde=AMAR, w=7)
                    p.texto("VELOCIDAD ABSURDA", 540, 1423, 66, AMAR, "ital")
                for i in range(14):                                                # líneas de velocidad
                    yy = (rnd(i, 4) * H + t * 2600 * (0.6 + rnd(i, 5))) % H
                    p.rect(rnd(i, 6) * W, yy, rnd(i, 6) * W + 5, yy + 220, BLANCO, 0.16 * kv)
        fx["golpe"] += 0.5 * golpe(t, vMaq, 0.25) + 1.0 * golpe(t, vNada, 0.35) + 0.6 * golpe(t, vConv, 0.25) + 0.5 * golpe(t, vVel, 0.6)
        fx["flash"] += 0.6 * pr(t, T_C - 0.2, T_C)
    return fx


# ====================================================================== CIERRE
REGLAS = [("BLOQUES", VERDE), ("MAGIA", LILA), ("PATINAR", CIAN), ("DISPAROS", NARANJA), ("CONSTRUIR", VERDE), ("DRAGONES", LILA),
          ("TRUCOS", CIAN), ("CARRERAS", MAGENTA)]


def _ficha(p, x, y, txt, col, s=1.0, op=1.0, t=0.0):
    w = 150 * s
    pts = [(x + w * math.cos(math.radians(60 * k)), y + w * 0.62 * math.sin(math.radians(60 * k))) for k in range(6)]
    p.poly(pts, mix(PANEL, col, 0.28), 0.96 * op)
    p.polilinea(pts, 6 * s, col, op, cerrado=True)
    p.texto(txt, x, y + 2, 38 * s, BLANCO, "black", op)


def cierre(p, t):
    fondo_tecno(p, t, VERDE, MAGENTA, 1.3)
    fx = dict(golpe=0.0, glitch=0.0, flash=0.6 * (1 - pr(t, T_C, T_C + 0.35)))
    mez = smooth(pr(t, cMez - 0.15, cMez + 0.45))
    fuera = smooth(pr(t, T_C2 - 0.1, T_C2 + 0.3))
    cxm, cym = 540, lerp(1010, 560, smooth(pr(t, T_C1 - 0.1, T_C1 + 0.5)))
    # ---- fichas de reglas: orbitan sueltas y, al mezclarse, se enganchan en un panal
    panal = [(0, -1), (0.87, -0.5), (0.87, 0.5), (0, 1), (-0.87, 0.5), (-0.87, -0.5), (0, 0), (1.74, 0)]
    esc_f = lerp(1.0, 0.82, smooth(pr(t, T_C1 - 0.1, T_C1 + 0.5)))
    for i, (txt, col) in enumerate(REGLAS):
        k = pop(t, T_C + 0.1 + i * 0.08, 0.35)
        if k <= 0.01:
            continue
        a = t * (0.5 + 0.08 * i) + i * math.pi / 4
        ox, oy = cxm + (360 + 40 * math.sin(t * 2 + i)) * math.cos(a), 1010 + (470 + 30 * math.cos(t * 1.7 + i)) * math.sin(a)
        hx, hy = cxm + panal[i][0] * 268 * esc_f - 60 * esc_f, cym + panal[i][1] * 190 * esc_f
        x, y = lerp(ox, hx, mez), lerp(oy, hy, mez)
        _ficha(p, x, y, txt, col, k * lerp(0.92, 1.0, mez) * esc_f * (1 - 0.4 * fuera), 1 - 0.75 * fuera, t)
    if mez > 0.5:
        p.glow(cxm, cym, 620, AMAR, 0.22 * (1 - fuera) * (0.7 + 0.3 * math.sin(t * 5)))
    # ---- frase 1
    if t < T_C1 + 0.3:
        s1 = T_C1 - 0.05
        slam(p, "LO FUERTE", 540, 300, 130, AMAR, t, cFue - 0.25, sale=cReg - 0.1)
        slam(p, "SI LAS REGLAS", 540, 250, 86, BLANCO, t, cReg, sale=s1)
        slam(p, "SE REESCRIBEN...", 540, 360, 86, MAGENTA, t, cRee - 0.1, sale=s1)
        slam(p, "SE MEZCLAN", 540, 1560, 130, AMAR, t, cMez, sale=s1)
        slam(p, "CON CUALQUIER OTRO", 540, 1680, 62, BLANCO, t, cCual - 0.05, "xbold", sale=s1)
        fx["golpe"] += 0.5 * golpe(t, cFue, 0.25) + 1.0 * golpe(t, cMez + 0.4, 0.4)
        fx["flash"] += 0.25 * golpe(t, cMez + 0.4, 0.3)
    # ---- frase 2: el límite ya no es lo que sabes programar: es lo que te atreves a imaginar
    if T_C1 <= t < T_C2 + 0.3:
        s2 = T_C2 - 0.05
        slam(p, "EL LÍMITE YA NO ES", 540, 1010, 70, BLANCO, t, cLim - 0.2, "xbold", sale=cAtr - 0.2, esp=0.04)
        slam(p, "LO QUE SABES", 540, 1150, 104, GRIS, t, cSab - 0.25, sale=cAtr - 0.2)
        slam(p, "PROGRAMAR", 540, 1275, 124, GRIS, t, cSab + 0.3, sale=cAtr - 0.2)
        if cSab + 0.9 < t < cAtr - 0.2:
            u = pr(t, cSab + 0.9, cSab + 1.15)
            p.linea((120, 1215), (lerp(120, 960, u), 1215), 18, ROJO)
        slam(p, "ES LO QUE", 540, 1000, 70, BLANCO, t, cAtr - 0.25, "xbold", sale=s2, esp=0.04)
        slam(p, "TE ATREVES A", 540, 1130, 110, BLANCO, t, cAtr, sale=s2)
        slam(p, "IMAGINAR", 540, 1320, 200, AMAR, t, cIma, sale=s2)
        if t >= cIma:
            for i in range(16):                                                    # rayos tras la palabra
                a = i * math.pi / 8 + t * 0.4
                r0, r1 = 330, 330 + 360 * e_out(pr(t, cIma, cIma + 0.4))
                p.linea((540 + r0 * 1.3 * math.cos(a), 1320 + r0 * 0.5 * math.sin(a)), (540 + r1 * 1.3 * math.cos(a), 1320 + r1 * 0.6 * math.sin(a)),
                        7, AMAR, 0.35 * (1 - pr(t, s2, s2 + 0.2)))
        fx["golpe"] += 0.5 * golpe(t, cSab + 0.9, 0.2) + 1.0 * golpe(t, cIma, 0.45)
        fx["flash"] += 0.22 * golpe(t, cIma, 0.3)
    # ---- frase 3: la pregunta
    if t >= T_C2:
        slam(p, "¿QUÉ 2 JUEGOS", 540, 430, 118, BLANCO, t, cQue - 0.1)
        slam(p, "FUSIONARÍAS?", 540, 575, 128, AMAR, t, cQue + 0.35)
        for i, col in enumerate((CIAN, MAGENTA)):
            k = pop(t, cQue + 0.25 + 0.2 * i, 0.35)
            x = 290 + 500 * i
            if k > 0.01:
                with p.pivote(x, 930, k * (1 + 0.03 * math.sin(t * 6 + i))):
                    p.rrect(x - 190, 760, x + 190, 1100, 34, mix(PANEL, col, 0.2), 0.96, borde=col, w=8)
                    p.texto("?", x, 925, 250, col, "black")
                    p.texto(f"JUEGO {i + 1}", x, 1060, 40, BLANCO, "xbold", esp=0.06)
        kq = pop(t, cQue + 0.55, 0.3)
        p.texto("+", 540, 925, 150 * kq, AMAR, "black", min(1.0, kq))
        ka = pop(t, cQue + 0.9, 0.3)
        if ka > 0.01:
            dy = 14 * math.sin(t * 7)
            with p.pivote(540, 1330, ka):
                p.rrect(170, 1250, 910, 1390, 70, AMAR)
                p.texto("DÍMELO EN LOS COMENTARIOS", 540, 1322, 46, FONDO0, "black")
                p.poly([(480, 1430 + dy), (600, 1430 + dy), (540, 1510 + dy)], AMAR)
        fx["golpe"] += 0.7 * golpe(t, cQue + 0.35, 0.3)
    return fx


def cuadro(p, t):
    if t < T_V:
        return reescribir(p, t)
    if t < T_C:
        return verdad(p, t)
    return cierre(p, t)
