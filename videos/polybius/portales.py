# -*- coding: utf-8 -*-
"""Escenas DIBUJADAS que viven dentro de las polaroids del tablero (portales). Cada una: f(p, t) pinta en el pintor `P` (960x540,
coordenadas de 1920x1080) el instante absoluto `t`. PORTAL[nombre](t) devuelve la imagen que el tablero deforma dentro de la foto.
Parte A: gancho, leyenda y casos reales. Paleta: salón de 1981 (violeta, neón cian/magenta/ámbar), siluetas con borde de luz."""
import math

import numpy as np

from portal_base import *  # noqa: F401,F403


# ================================================================================================ GANCHO
@portal("salon")
def salon_p(p, t):
    """Salón recreativo de Portland, 1981: en la fila aparece una cabina negra que nadie había visto; se enciende y se forma la fila."""
    g = "gancho"
    t0, tm, t2 = INI(g, 1), ww(g, 1, "aparecio"), INI(g, 2)
    cam = 60 * math.sin((t - t0) * 0.25)
    salon(p, t, cam=cam, n=7)
    on = parpadeo(t, tm - 0.1, 1.0)
    # la cabina negra, en primer término
    cx, cy, ch = 1230, 1060, 880
    u_in = smooth((t - t0 - 0.6) / 1.6)
    cabina(p, cx, cy, ch, t, pant_formas if on > 0.5 else None, color=NEGRO, borde=(0.055, 0.055, 0.075), luz=VIOL, marq=(0.55, 0.22, 0.95),
           rotulo="POLYBIUS" if t > ww(g, 3, "polybius") - 0.2 else None, op=u_in, encendida=on > 0.5)
    if on > 0.5:
        p.glow(cx, cy - ch * 0.68, 900, (0.45, 0.25, 0.95), 0.16)
        p.elip(cx, cy + 20, 420, 60, 0, (0.45, 0.25, 0.95), 0.16)
    # la fila de chicos (entran caminando desde la izquierda)
    pelos = ("corto", "afro", "largo", "corto", "moño", "corto")
    for k in range(6):
        xf = 930 - k * 150
        llegada = t2 - 1.4 + k * 0.42
        u = smooth((t - llegada) / 1.5)
        if u <= 0:
            continue
        x = lerp(-140 - k * 40, xf, u)
        h = 470 - (k % 3) * 28
        if u < 1 and k > 0:
            j = persona(p, x, 1068, h, pose_caminar((t - llegada) * 7.5), FIG, 1, pelo=pelos[k])
        elif k == 0:
            j = jugador(p, x + 60 * u, 1068, h, t, 1, FIG, pelos[k])
        else:
            j = persona(p, x, 1068, h, pose_estar(t * 1.3 + k, lean=0.04 + 0.03 * math.sin(t * 0.9 + k)), FIG, 1, pelo=pelos[k])
        if on > 0.5:
            luz_cara(p, j, x + (60 * u if k == 0 else 0), 1068, 1, mix(VIOL, (1, 1, 1), 0.3), h, 0.55 / (1 + k * 0.5))
    polvo(p, t, 30, 3, 0.25, (0.8, 0.7, 1.0), 8)
    z = 1.0 + 0.22 * smooth((t - t2) / 6.0)
    zoom_p(p, z, 0.62, 0.42)


@portal("fascinados")
def fascinados(p, t):
    """Tres chicos de espaldas ante la pantalla que no deja de girar: «quedaban fascinados»."""
    t0 = INI("leyenda", 0)
    p.fondo((0.012, 0.008, 0.030), (0.035, 0.020, 0.060))
    p.rect(300, 40, 1620, 800, (0.03, 0.03, 0.045))
    pant_formas(p, 350, 80, 1570, 760, t, 1.0, 1.25, True, 1.6)
    p.glow(960, 420, 1300, (0.45, 0.25, 0.95), 0.22 + 0.05 * math.sin(t * 4))
    for k, (x, h, pelo) in enumerate(((520, 520, "corto"), (960, 600, "afro"), (1400, 540, "largo"))):
        y = 1140 + 6 * math.sin(t * 0.8 + k)
        p.rrect(x - h * 0.42, y - h * 0.50, x + h * 0.42, y + h * 0.4, h * 0.2, FIG)
        p.circ(x, y - h * 0.70, h * 0.23, FIG)
        if pelo == "afro":
            p.circ(x, y - h * 0.76, h * 0.30, FIG)
        elif pelo == "largo":
            p.rrect(x - h * 0.25, y - h * 0.88, x + h * 0.25, y - h * 0.30, h * 0.12, FIG)
        col = NEON[int(t * 3 + k) % 6]
        p.elip(x, y - h * 0.90 - (h * 0.08 if pelo == "afro" else 0), h * 0.22, h * 0.035, 0, mix(col, (1, 1, 1), 0.4), 0.55)      # borde de luz
        p.linea((x - h * 0.40, y - h * 0.47), (x + h * 0.40, y - h * 0.47), 5, mix(col, (1, 1, 1), 0.3), 0.35)
    zoom_p(p, 1.0 + 0.12 * smooth((t - t0) / 4.0), 0.5, 0.40)


# ================================================================================================ LEYENDA
@portal("pesadilla")
def pesadilla(p, t):
    """Dormitorio de noche: el chico da vueltas en la cama, las formas siguen girando sobre él; luego se sienta sin poder dormir y pasan los días."""
    le = "leyenda"
    t0, t2 = INI(le, 1), INI(le, 2)
    p.fondo((0.035, 0.045, 0.095), (0.070, 0.075, 0.140))
    # ventana con luna y cortina
    p.rect(1240, 130, 1700, 620, (0.07, 0.11, 0.22))
    luna(p, 1560, 260, 44)
    estrellas(p, t, 30, 5, 0.5, 0.5)
    p.rect(1230, 120, 1710, 134, (0.10, 0.09, 0.12))
    p.rect(1230, 616, 1710, 632, (0.10, 0.09, 0.12))
    p.rect(1464, 120, 1476, 630, (0.10, 0.09, 0.12))
    cortina(p, 1180, 100, 1300, 660, 0.0, (0.10, 0.07, 0.16), t)
    p.poly([(1240, 632), (1700, 632), (1500, 1080), (700, 1080)], (0.30, 0.38, 0.60), 0.10)          # luz de luna en el suelo
    suelo(p, 900, (0.05, 0.045, 0.075), (0.02, 0.02, 0.035))
    # póster y estantería
    p.rect(250, 190, 520, 520, (0.09, 0.07, 0.13))
    poligono(p, 385, 355, 90, 6, t * 0.2, 5, (0.35, 0.25, 0.55), 0.7)
    p.rect(640, 300, 1040, 316, (0.10, 0.08, 0.12))
    for k in range(7):
        p.rect(660 + k * 50, 300 - 60 - (k % 3) * 14, 660 + k * 50 + 34, 300, mix((0.20, 0.12, 0.25), (0.10, 0.18, 0.28), k / 6))
    # cama
    p.rrect(380, 760, 1380, 960, 40, (0.10, 0.09, 0.16))
    p.rect(330, 560, 400, 980, (0.07, 0.06, 0.10))
    p.rect(1360, 700, 1410, 980, (0.07, 0.06, 0.10))
    p.rrect(430, 690, 660, 790, 40, (0.55, 0.57, 0.68))                                              # almohada
    despierto = smooth((t - t2 + 0.5) / 1.0)
    if despierto < 0.5:
        gira = math.sin((t - t0) * 2.2)
        p.rrect(560, 720 - 12 * abs(gira), 1320, 850, 60, (0.16, 0.20, 0.36))                        # bulto bajo la manta
        p.circ(560 + 16 * gira, 716, 52, FIG2)
        p.elip(560 + 16 * gira, 690, 56, 30, 0, (0.03, 0.03, 0.05))
    else:
        p.rrect(700, 760, 1320, 850, 50, (0.16, 0.20, 0.36))
        col_ch = (0.10, 0.12, 0.22)
        # sentado en la cama, abrazado a las rodillas, meciéndose un poco
        m = 10 * math.sin(t * 1.6)
        p.poly([(900, 800), (990, 600 + m * 0.3), (1090, 800)], (0.16, 0.20, 0.36))                    # rodillas bajo la manta
        capsula(p, (720, 800), (745 + m, 600), 74, 60, col_ch)                                        # espalda
        capsula(p, (760 + m, 630), (900 + m * 0.5, 690), 26, 22, col_ch)                              # brazo hacia las rodillas
        p.circ(915 + m * 0.5, 695, 26, col_ch)
        hx, hy = 770 + m * 1.2, 520
        capsula(p, (752 + m, 600), (hx - 4, hy + 40), 30, 26, col_ch)                                 # cuello
        p.elip(hx, hy, 62, 70, 0, col_ch)
        p.elip(hx - 14, hy - 28, 66, 50, 0, (0.03, 0.03, 0.06))                                       # pelo revuelto
        p.poly([(hx - 70, hy - 40), (hx - 96, hy - 84), (hx - 40, hy - 70)], (0.03, 0.03, 0.06))
        p.elip(hx + 46, hy + 6, 16, 52, 0, (0.60, 0.70, 1.0), 0.50)                                   # luz de luna en la cara
        p.elip(hx + 28, hy + 2, 13, 11, 0, (0.95, 0.96, 1.0))                                         # ojo muy abierto
        p.circ(hx + 31, hy + 2, 5, (0.02, 0.02, 0.04))
        p.linea((hx + 12, hy + 26), (hx + 34, hy + 34), 5, (0.03, 0.03, 0.06))                        # ojera
        p.rrect(690, 790, 1320, 870, 50, (0.16, 0.20, 0.36))
    # mesilla con despertador (las agujas corren)
    p.rect(1420, 800, 1600, 980, (0.08, 0.07, 0.11))
    reloj(p, 1510, 730, 62, t, h=1.0 + (t - t0) * 0.9, m=(t - t0) * 54.0, segundero=False, cara=(0.85, 0.83, 0.75))
    # las formas de la pantalla, encima de él
    amt = 0.55 * (1 - 0.5 * despierto)
    for k in range(5):
        a = t * (0.6 + 0.2 * k) + k * 1.3
        x, y = 860 + 330 * math.cos(a * 0.7 + k), 430 + 150 * math.sin(a)
        poligono(p, x, y, 70 + 26 * math.sin(t * 1.4 + k), (3, 4, 6, 5, 8)[k], a * 1.4, 6, NEON[k], amt * (0.6 + 0.4 * math.sin(t * 2 + k)))
        p.glow(x, y, 130, NEON[k], 0.10 * amt)
    if despierto > 0.5:                                                                            # los días pasan
        u = (t - t2) / max(0.1, FIN(le, 2) - t2)
        dia = 1 + int(clamp(u) * 20)
        hoja_cal(p, 385, 355, 250, 280, "NOCHE", str(dia), ((t - t2) * 2.6) % 1.0)
    niebla(p, t, 1000, 240, (0.20, 0.22, 0.40), 0.35, 20, 2)


@portal("hombres")
def hombres(p, t):
    """De noche, con el salón cerrado: dos hombres de traje abren la cabina por detrás, conectan un registrador y anotan; el dinero se queda."""
    le = "leyenda"
    t0 = INI(le, 3)
    salon(p, t, luz=0.75, neones=False, vivas=False)
    p.rect(0, 0, W, H, (0.02, 0.05, 0.12), 0.18)
    cx, cy, ch = 1180, 1040, 800
    # cabina de perfil, abierta por detrás
    cabina_lado(p, cx, cy, ch, 1, t, color=NEGRO, luz=VIOL, amt=0.5)
    xb = cx - ch * 0.18
    ab = smooth((t - ww(le, 3, "abrian")) / 0.8)
    p.poly([(xb, cy - ch * 0.80), (xb - 150 * ab, cy - ch * 0.84), (xb - 150 * ab, cy - ch * 0.16), (xb, cy - ch * 0.20)], (0.06, 0.06, 0.08))   # tapa
    if ab > 0.2:
        p.rect(xb - 4, cy - ch * 0.78, xb + 60, cy - ch * 0.22, (0.02, 0.05, 0.03))
        for k in range(9):
            on = math.sin(t * (3 + k) + k) > 0
            p.circ(xb + 20 + (k % 2) * 22, cy - ch * (0.72 - 0.055 * k), 7, (0.3, 1.0, 0.4) if on else (0.9, 0.2, 0.15), 0.9)
        p.glow(xb, cy - ch * 0.5, 320, (0.3, 1.0, 0.5), 0.18 * ab)
    # hombre 1: en cuclillas con el registrador de cinta
    t_an = ww(le, 3, "anotaban")
    j1 = persona(p, 760, 1040, 620, dict(ll=(1.5, 1.9), lr=(1.2, 2.2), bl=(1.2, 0.5 + 0.1 * math.sin(t * 3)), br=(1.0, 0.8), lean=0.35, head=0.2), FIG, 1,
                 ropa="chaqueta", sombrero=True)
    p.rrect(820, 930, 1010, 1040, 10, (0.10, 0.10, 0.13))
    for k in (0, 1):
        engranaje(p, 870 + k * 90, 978, 30, t * 120 * (1 if ab > 0.5 else 0), (0.55, 0.55, 0.62), 6)
    p.polilinea([(1010, 990), (1060, 1020), (xb - 20, cy - ch * 0.40)], 5, (0.05, 0.05, 0.06))
    # hombre 2: de pie, anota en una tablilla
    j2 = persona(p, 420, 1050, 700, dict(ll=(0.05, 0), lr=(-0.06, 0), bl=(0.85, 1.25), br=(0.75, 1.5 + 0.12 * math.sin(t * 9)), lean=0.05, head=0.30), FIG, 1,
                 ropa="chaqueta", sombrero=True,
                 objeto=lambda pp, wr, wl, f: pp.poly([(wl[0] - 10, wl[1] - 70), (wl[0] + 90, wl[1] - 50), (wl[0] + 80, wl[1] + 50), (wl[0] - 20, wl[1] + 30)], (0.80, 0.78, 0.70)))
    for j, x, y, h in ((j1, 760, 1040, 620), (j2, 420, 1050, 700)):
        luz_cara(p, j, x, y, 1, (0.5, 1.0, 0.6), h, 0.25 + 0.45 * ab)
    # linterna
    p.haz(480, 610, 12 + 6 * math.sin(t * 0.8), 900, 22, (1.0, 0.95, 0.75), 0.20)
    # el dinero, intacto: caja de monedas con brillo
    t_d = ww(le, 3, "dinero") - 0.5
    ud = smooth((t - t_d) / 0.6)
    p.rrect(1420, 900, 1640, 1040, 10, (0.10, 0.09, 0.11))
    p.rect(1440, 920, 1620, 1020, (0.03, 0.03, 0.04))
    for k in range(14):
        p.elip(1460 + (k % 7) * 24, 1004 - (k // 7) * 22, 14, 6, 0, (0.75, 0.75, 0.80))
    p.glow(1530, 980, 200, (1.0, 0.9, 0.6), 0.25 * ud * (0.7 + 0.3 * math.sin(t * 5)))
    if ud > 0:
        p.texto("SIN TOCAR", 1530, 850, 46, (1.0, 0.92, 0.5), "sans_b", ud)
    polvo(p, t, 30, 9, 0.3, (0.9, 0.9, 0.8), 6)


@portal("vacio")
def vacio(p, t):
    """La mañana siguiente: en la fila queda un hueco; solo la marca limpia en la moqueta y el polvo."""
    le = "leyenda"
    t0 = INI(le, 4)
    tdes = ww(le, 4, "desaparecieron")
    salon(p, t, n=7, hueco=3, luz=0.9)
    cx, cy, ch = 960, 1050, 820
    u = smooth((t - tdes + 0.2) / 0.7)
    if u < 1:
        cabina(p, cx, cy, ch, t, pant_formas, color=NEGRO, borde=(0.055, 0.055, 0.075), luz=VIOL, marq=(0.55, 0.22, 0.95), rotulo="POLYBIUS", op=1 - u)
    if u > 0:
        # marca en la moqueta: rectángulo más limpio + 4 huellas de las patas + contorno a trazos
        p.poly([(cx - 190, cy - 50), (cx + 190, cy - 50), (cx + 230, cy + 10), (cx - 230, cy + 10)], (0.20, 0.12, 0.26), 0.8 * u)
        for dx, dy in ((-180, -42), (180, -42), (-215, 2), (215, 2)):
            p.elip(cx + dx, cy + dy, 16, 7, 0, (0.03, 0.02, 0.05), 0.9 * u)
        w = ch * 0.40
        for k in range(22):
            a0 = k / 22
            if int(t * 3 + k) % 2:
                continue
            per = [(cx - w / 2, cy), (cx + w / 2, cy), (cx + w / 2, cy - ch), (cx - w / 2, cy - ch), (cx - w / 2, cy)]
            L = a0 * 4
            i = int(L)
            f = L - i
            q0 = (lerp(per[i][0], per[i + 1][0], f), lerp(per[i][1], per[i + 1][1], f))
            f2 = min(1.0, f + 0.10)
            q1 = (lerp(per[i][0], per[i + 1][0], f2), lerp(per[i][1], per[i + 1][1], f2))
            p.linea(q0, q1, 4, (0.85, 0.8, 1.0), 0.45 * u, caps=False)
        p.texto("?", cx, cy - ch * 0.55, 260, (0.86, 0.10, 0.10), "serif", 0.85 * smooth((t - tdes - 0.5) / 0.5))
        for k in range(26):                                                                         # polvo que queda flotando
            a = k * 2.4
            r = 60 + 240 * ((t - tdes) * 0.25 + k * 0.07) % 300
            p.circ(cx + r * math.cos(a) * 1.3, cy - 200 - r * 0.9 + 50 * math.sin(a), 4, (0.8, 0.75, 0.9), 0.35 * u * max(0.0, 1 - r / 300))
    # dos chicos que miran el hueco
    for k, (x, f, pelo) in enumerate(((520, 1, "corto"), (1430, -1, "largo"))):
        j = persona(p, x, 1068, 500 - k * 30, pose_estar(t + k, lean=0.06), FIG, f, pelo=pelo)
    # un tornillo... ninguno: el haz de una linterna barre el suelo vacío
    if t > tdes + 0.6:
        lx = 700 + 520 * smooth((t - tdes - 0.8) / 2.5)
        p.elip(lx, 1040, 150, 34, 0, (1.0, 0.95, 0.75), 0.22)
        p.haz(520 + 60, 760, math.degrees(math.atan2(1040 - 760, lx - 580)), 620, 16, (1.0, 0.95, 0.75), 0.18)


# ================================================================================================ CASOS REALES
@portal("maraton")
def maraton(p, t):
    """Veintiocho horas seguidas: el chico juega mientras el reloj corre, la ventana pasa de día a noche y las latas se acumulan."""
    c = "casos"
    t0, t1 = INI(c, 2), FIN(c, 2)
    u = clamp((t - t0) / max(0.1, t1 - t0 - 0.4))
    horas = u * 28.0
    salon(p, t, luz=0.75, neones=False)
    # ventana alta: el cielo cambia con las horas (empieza por la tarde)
    hh = (16 + horas) % 24
    dia = clamp(1 - abs(hh - 13) / 7.0)
    cielo = mix((0.02, 0.03, 0.09), (0.45, 0.65, 0.95), dia)
    p.rect(160, 90, 620, 330, cielo)
    if dia < 0.3:
        luna(p, 500, 190, 26, halo=0.5)
    else:
        p.glow(300 + 200 * (hh - 6) / 14, 160, 120, (1.0, 0.9, 0.6), 0.9 * dia)
    p.rect(150, 80, 630, 96, (0.05, 0.04, 0.07))
    p.rect(150, 324, 630, 340, (0.05, 0.04, 0.07))
    p.rect(384, 80, 396, 340, (0.05, 0.04, 0.07))
    # reloj de pared que corre
    reloj(p, 1560, 240, 130, t, h=16 + horas, m=horas * 60.0, segundero=False, cara=(0.90, 0.88, 0.80))
    # cabina de perfil y jugador que se va venciendo
    cabina_lado(p, 1150, 1040, 800, -1, t, color=(0.05, 0.05, 0.07), luz=(0.80, 0.90, 1.0))
    lean = 0.08 + 0.22 * u
    j = jugador(p, 800, 1040, 540, t, 1, FIG, "corto", ritmo=1.0 - 0.5 * u, lean=lean)
    luz_cara(p, j, 800, 1040, 1, (0.8, 0.9, 1.0), 540, 0.6)
    # latas y envoltorios
    n = int(u * 12)
    rng = np.random.default_rng(4)
    for k in range(n):
        x = 480 + rng.random() * 260
        if rng.random() < 0.5:
            p.rrect(x, 1010, x + 26, 1060, 6, mix((0.75, 0.15, 0.15), (0.2, 0.5, 0.8), rng.random()))
        else:
            p.elip(x, 1058, 30, 9, rng.random() * 40 - 20, (0.6, 0.6, 0.65))
    # contador de horas
    p.rrect(1330, 440, 1790, 620, 18, (0.02, 0.02, 0.03), 0.85)
    p.texto("HORAS JUGANDO", 1560, 480, 34, (0.85, 0.85, 0.9), "mono")
    p.texto(f"{int(horas):02d}", 1560, 560, 110, (1.0, 0.25, 0.2) if horas > 24 else (1.0, 0.85, 0.3), "abril")
    if u > 0.85:                                                                                    # dolor de estómago: se dobla
        k = smooth((u - 0.85) / 0.15)
        p.glow(800 + j["pel"][0], 1040 - j["pel"][1] - 60, 110, (1.0, 0.25, 0.2), 0.5 * k * (0.6 + 0.4 * math.sin(t * 9)))


@portal("migrana")
def migrana(p, t):
    """Un juego de formas geométricas que no deja de moverse y la migraña: ondas de dolor en la sien del jugador."""
    c = "casos"
    t0 = INI(c, 3)
    tm = ww(c, 3, "migra")
    p.fondo((0.010, 0.012, 0.030), (0.030, 0.020, 0.055))
    p.rrect(90, 90, 1110, 990, 30, (0.03, 0.03, 0.045))
    pant_tunel(p, 130, 130, 1070, 950, t, 1.0)
    p.glow(600, 540, 900, CIAN, 0.14)
    p.rect(1130, 0, W, H, (0.10, 0.07, 0.16), grad=((0.07, 0.05, 0.13), (0.16, 0.10, 0.22)))
    p.glow(1500, 500, 700, (0.30, 0.20, 0.50), 0.25)
    # cabeza y hombros de perfil mirando a la pantalla (hacia la izquierda)
    FIG = (0.030, 0.032, 0.055)
    hx, hy = 1470, 560
    p.poly([(1250, 1080), (1290, 900), (1400, 840), (1560, 840), (1700, 900), (1780, 1080)], FIG)
    p.rect(1420, 720, 1540, 860, FIG)
    p.elip(hx, hy, 170, 205, 0, FIG)
    p.poly([(hx - 160, hy - 20), (hx - 215, hy + 50), (hx - 160, hy + 70)], FIG)                     # nariz
    p.elip(hx + 20, hy - 60, 185, 170, 0, (0.012, 0.012, 0.022))                                     # pelo
    p.elip(hx - 150, hy + 10, 34, 150, 8, mix(CIAN, (1, 1, 1), 0.4), 0.55)                           # luz de la pantalla en la cara
    dolor = smooth((t - tm + 0.3) / 0.8)
    if dolor > 0:
        sx, sy = hx - 30, hy - 70
        for k in range(4):
            r = ((t * 0.9 + k * 0.25) % 1.0)
            p.elip(sx, sy, 60 + 300 * r, 60 + 300 * r, 0, (1.0, 0.22, 0.18), 0.0)
            poligono(p, sx, sy, 60 + 320 * r, 24, 0, 10 * (1 - r) + 2, (1.0, 0.22, 0.18), dolor * (1 - r) * 0.9)
        p.glow(sx, sy, 150, (1.0, 0.2, 0.15), 0.6 * dolor * (0.6 + 0.4 * math.sin(t * 8)))
        # mano a la sien
        p.polilinea([(1700, 1000), (1650, 760), (1520, 560 + 8 * math.sin(t * 5))], 70, FIG)
        p.circ(1515, 555 + 8 * math.sin(t * 5), 52, FIG)
        for k in range(3):                                                                          # rayos
            a = -0.9 + k * 0.5 + 0.1 * math.sin(t * 6 + k)
            x0, y0 = sx + 190 * math.cos(a - 1.2), sy + 190 * math.sin(a - 1.2)
            p.polilinea([(x0, y0), (x0 + 30, y0 - 50), (x0 + 5, y0 - 60), (x0 + 40, y0 - 120)], 8, (1.0, 0.85, 0.3), dolor * (0.5 + 0.5 * math.sin(t * 11 + k)))


@portal("redada")
def redada(p, t):
    """Agentes federales entran en un salón; dentro no hay juego maldito: máquinas trucadas para apostar."""
    c = "casos"
    t0, t5 = ww(c, 4, "agentes") - 0.6, INI(c, 5)
    dentro = smooth((t - t5 + 0.25) / 0.5)
    if dentro < 1:
        # exterior de noche: fachada con neón, coches con luces, agentes que entran
        p.fondo((0.015, 0.020, 0.050), (0.060, 0.050, 0.100))
        estrellas(p, t, 40, 2, 0.35, 0.5)
        ciudad(p, t, 620, (0.03, 0.035, 0.07), off=0, seed=6, h_max=330)
        p.rect(420, 250, 1500, 900, (0.07, 0.06, 0.10))
        p.rect(420, 250, 1500, 330, (0.10, 0.08, 0.15))
        neon(p, "ARCADE", 960, 292, 78, MAG, t, 1.0)
        for x0 in (480, 1140):
            p.rect(x0, 420, x0 + 300, 760, (0.20, 0.10, 0.30))
            for k in range(3):
                p.rect(x0 + 20 + k * 95, 600, x0 + 80 + k * 95, 760, (0.03, 0.03, 0.05))
                p.rect(x0 + 28 + k * 95, 612, x0 + 72 + k * 95, 660, NEON[(k + x0) % 6], 0.7)
        p.rect(840, 470, 1080, 900, (0.30, 0.16, 0.42))                                              # puerta abierta con luz
        p.glow(960, 700, 500, (0.6, 0.3, 0.9), 0.25)
        suelo(p, 900, (0.05, 0.05, 0.08), (0.015, 0.015, 0.03))
        p.poly([(840, 900), (1080, 900), (1300, 1080), (620, 1080)], (0.55, 0.30, 0.85), 0.14)
        az = 0.5 + 0.5 * math.sin(t * 9)
        for x, d in ((250, 1), (1680, -1)):
            coche(p, x, 1010, 190, (0.03, 0.035, 0.05), d, True, 0.0)
            p.rect(x - 40, 1010 - 190 * 0.86, x + 40, 1010 - 190 * 0.78, (0.1, 0.1, 0.12))
            p.glow(x - 24, 1010 - 190 * 0.84, 260, (1.0, 0.1, 0.1), 0.9 * az)
            p.glow(x + 24, 1010 - 190 * 0.84, 260, (0.15, 0.3, 1.0), 0.9 * (1 - az))
        p.rect(0, 0, W, H, (1.0, 0.1, 0.1), 0.05 * az)
        p.rect(0, 0, W, H, (0.1, 0.2, 1.0), 0.05 * (1 - az))
        for k in range(5):
            llegada = t0 + 0.3 + k * 0.45
            u = clamp((t - llegada) / 2.4)
            if u <= 0 or u >= 1:
                continue
            x = lerp(300 if k % 2 == 0 else 1620, 960, u)
            y = lerp(1050, 905, u)
            h = lerp(470, 330, u)
            persona(p, x, y, h, pose_caminar((t - llegada) * 9, amp=0.6), FIG, 1 if k % 2 == 0 else -1, ropa="chaqueta",
                    objeto=lambda pp, wr, wl, f: pp.haz(wr[0], wr[1], -10 if f > 0 else 190, 260, 26, (1.0, 0.95, 0.8), 0.3))
    if dentro > 0:
        q = P()
        salon(q, t, luz=0.8, neones=False)
        # máquina abierta por delante: dentro, cartas y monedas
        cx, cy, ch = 1180, 1050, 840
        cabina(q, cx, cy, ch, t, None, color=(0.05, 0.05, 0.07), luz=AMBAR, rotulo="BONUS")
        sx0, sy0, sx1, sy1 = cx - ch * 0.144, cy - ch * 0.83, cx + ch * 0.144, cy - ch * 0.54
        q.rect(sx0, sy0, sx1, sy1, (0.02, 0.10, 0.05))
        for k, s in enumerate(("7", "A", "K")):
            yy = sy0 + (sy1 - sy0) * (0.5 + 0.9 * (((t * (1.5 + k * 0.4)) % 1.0) - 0.5) * (1 if t < t5 + 2.2 + k * 0.4 else 0))
            q.rrect(sx0 + 14 + k * 80, yy - 60, sx0 + 84 + k * 80, yy + 60, 8, (0.95, 0.93, 0.88))
            q.texto(s, sx0 + 49 + k * 80, yy, 80, (0.8, 0.1, 0.1), "serif")
        for k in range(26):                                                                         # monedas que caen de la bandeja
            u = ((t - t5) * 0.9 + k * 0.137) % 1.0
            x = cx - 120 + (k * 53) % 240
            q.elip(x, cy - ch * 0.20 + u * ch * 0.22, 15, 15 * abs(math.cos(t * 6 + k)), 0, (0.95, 0.80, 0.30), 1 - u * 0.3)
        q.rrect(cx - 170, cy - 40, cx + 170, cy + 16, 10, (0.10, 0.09, 0.11))
        # agente que señala y otro que anota
        persona(q, 720, 1060, 640, pose_señalar(smooth((t - t5) / 0.6)), FIG, 1, ropa="chaqueta")
        persona(q, 380, 1070, 600, dict(ll=(0.05, 0), lr=(-0.06, 0), bl=(0.85, 1.25), br=(0.75, 1.5 + 0.12 * math.sin(t * 9)), lean=0.05, head=0.30), FIG, 1,
                ropa="chaqueta")
        tt = ww(c, 5, "apostar") - 0.4
        ua = smooth((t - tt) / 0.5)
        if ua > 0:
            q.rrect(250, 150, 950, 290, 16, (0.75, 0.08, 0.08), 0.92 * ua)
            q.texto("APUESTAS ILEGALES", 600, 220, 70, (1.0, 0.95, 0.85), "sans_b", ua)
        p.im[:] = p.im * (1 - dentro) + q.im * dentro


@portal("corazon")
def corazon(p, t):
    """1982, otro estado: un monitor cardiaco que se queda en línea plana junto a una cabina que sigue encendida. Sin figura humana."""
    c = "casos"
    t0 = INI(c, 6)
    tm = ww(c, 6, "murio")
    salon(p, t, luz=0.5, neones=False)
    p.rect(0, 0, W, H, (0.0, 0.0, 0.03), 0.35)
    cabina_lado(p, 1480, 1040, 780, -1, t, color=(0.05, 0.05, 0.07), luz=(1.0, 0.45, 0.25), amt=0.8)
    # taburete vacío delante
    p.rect(1150, 860, 1250, 880, FIG2)
    p.linea((1170, 880), (1150, 1040), 10, FIG2)
    p.linea((1230, 880), (1250, 1040), 10, FIG2)
    # monitor
    monitor_marco(p, 180, 320, 1020, 800)
    plana = smooth((t - tm + 0.2) / 1.2)
    ecg(p, 220, 420, 760, 280, t, (0.35, 0.95, 0.60) if plana < 0.9 else (0.95, 0.25, 0.2), 300.0, 1.2, 0.3 * (1 - plana), 6, 1.0, plana)
    p.texto("1982", 600, 170, 110, (0.95, 0.9, 0.8), "abril", smooth((t - t0) / 0.6))
    p.texto("OTRO ESTADO · OTRO JUEGO", 600, 290, 38, (0.85, 0.85, 0.9), "mono", smooth((t - t0 - 0.6) / 0.6))
    if plana > 0.8:
        p.glow(600, 500, 600, (1.0, 0.2, 0.15), 0.12 * (0.6 + 0.4 * math.sin(t * 4)))
    # periódicos que caen: el miedo crece
    tq = ww(c, 6, "miedo") - 0.3
    for k in range(6):
        u = smooth((t - tq - k * 0.22) / 0.7)
        if u <= 0:
            continue
        x, y = 170 + k * 300, 985 - (k % 2) * 30
        documento(p, x, lerp(-200, y, u), 220, 150, (-12 + k * 7) * (2 - u), 5, (0.82, 0.80, 0.72), (0.3, 0.3, 0.3), True, True, 0.95)
        if u > 0.9:
            p.texto("¿PELIGRO?", x, y - 46, 30, (0.75, 0.08, 0.08), "sans_b")


import portales2  # noqa: E402,F401  (parte B: gobierno, pruebas, origen, por qué, cierre)

