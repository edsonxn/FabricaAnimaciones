# -*- coding: utf-8 -*-
"""Primera mitad, en un solo plano secuencia: GANCHO (gameplay real + rótulos) -> EL PUENTE (dos procesos y su memoria
compartida) -> LÍMITE (los motores originales como jaula). Cada función dibuja en `p` y devuelve los efectos de cámara."""
import math

import cv2
import numpy as np

from comp import *  # noqa: F401,F403
from comp import (chip, clip_en, figura_bloques, ic_alas, ic_candado, ic_cubo, ic_dinamita, ic_ojo, ic_sonido_no, ic_ventana_no,
                  memoria, mundo_bloques, paquete, pista, slam, tecleo, ventana)
from pix import FIN, INI, Clip, W, H, ww

VT = (70, 170, 1010, 740)            # ventana de arriba: Skyrim (video real)
MEM = (110, 812, 970, 1010)          # memoria compartida
VB = (70, 1082, 1010, 1612)          # ventana de abajo: Minecraft (mundo dibujado, proceso oculto)
CRED = "Clip: Hi5M0F0 · YouTube"
TX = (300, 540, 780)                 # columnas de las pistas entre ventanas y memoria

G = "gancho"
tM, tD, tS, tN = ww(G, 0, "Minecraft"), ww(G, 0, "dentro"), ww(G, 0, "Skyrim"), ww(G, 0, "montaje")
tB, tV, tT = ww(G, 1, "bloques"), ww(G, 1, "volar"), ww(G, 1, "dinamita")
tR, tCo = INI(G, 2), ww(G, 2, "cómo")
tDos, tSeg, tMi = ww(G, 3, "dos formas"), ww(G, 3, "segunda"), ww(G, 3, "miedo")

U = "puente"
uP = ww(U, 0, "puente")
uJ, uAl, uSep = ww(U, 1, "dos juegos"), ww(U, 1, "al mismo"), ww(U, 1, "separados")
uEsc, uVen, uSon = ww(U, 2, "escondido"), ww(U, 2, "ventana"), ww(U, 2, "sonido")
uMem, uLeer, uEscr = ww(U, 3, "memoria"), ww(U, 3, "leer"), ww(U, 3, "escribir")
uCi, uNo, uJug, uBlo, uGol = ww(U, 4, "cientos"), ww(U, 4, "notas"), ww(U, 4, "jugador"), ww(U, 4, "bloque"), ww(U, 4, "golpeó")
uMc, uMan, uPer = ww(U, 5, "Minecraft"), ww(U, 5, "manda"), ww(U, 5, "personaje")
uSk, uMun, uEne, uCho = ww(U, 5, "Skyrim"), ww(U, 5, "mundo"), ww(U, 5, "enemigos"), ww(U, 5, "choques")
uNin, uCree, uProp = ww(U, 6, "ninguno"), ww(U, 6, "cree"), ww(U, 6, "propio")

L = "limite"
lLim, lAtr, lMot = ww(L, 0, "límite"), ww(L, 0, "atrapado"), ww(L, 0, "motores")
T_PUENTE, T_LIMITE, T_FIN_A = INI(U, 0) - 0.4, INI(L, 0) - 0.3, 52.0


def seg_clip(t):
    """Segundo del extracto de SkyCraft (se queda en el tramo donde el suelo de Skyrim lleva bloques)."""
    return 1.0 + t if t < INI(G, 1) - 0.1 else 23.0 + ((t - INI(G, 1)) % 10.5)


def _fondo_clip(p, t, op):
    f = Clip.cuadro("skycraft_a", seg_clip(t))
    ch = cv2.GaussianBlur(cv2.resize(f, (96, 54), interpolation=cv2.INTER_AREA), (0, 0), 3)
    p.imagen(ch, 0, 0, W, H, op, 0, 0.42)


# ====================================================================== GANCHO
def gancho(p, t):
    k = smooth(pr(t, tR, tR + 0.75))                       # 0 = clip grande; 1 = clip dentro de la ventana de arriba
    if k < 1:
        _fondo_clip(p, t, 1 - k)
    z = 1.0 + 0.05 * pr(t, 0, tR) * (1 - k)
    gr = (20, 490, 1060, 1075)
    ins = (VT[0] + 8, VT[1] + 70, VT[2] - 8, VT[3] - 8)
    r = [lerp(a, b, k) for a, b in zip(gr, ins)]
    if k > 0.02:
        ventana(p, *VT, "Skyrim.exe", "PROCESO 1 · C++", LILA, t, op=k)
    with p.pivote(540, 782, z):                            # zoom SIN desplazar (p.cam centraría el punto en la pantalla)
        if k < 0.98:
            p.rrect(r[0] - 6, r[1] - 6, r[2] + 6, r[3] + 6, 20, None, 1 - k, borde=CIAN, w=6)
        clip_en(p, "skycraft_a", seg_clip(t), *r, r=14, credito=CRED)
        if k < 0.5:                                        # esquinas de visor + etiqueta de grabación
            o = 1 - 2 * k
            for sx, sy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                x, y = (r[0], r[2])[sx], (r[1], r[3])[sy]
                d = 34 * (1 if sx == 0 else -1), 34 * (1 if sy == 0 else -1)
                p.polilinea([(x - d[0] * 0.5 + d[0], y - d[1] * 0.5), (x - d[0] * 0.5, y - d[1] * 0.5), (x - d[0] * 0.5, y - d[1] * 0.5 + d[1])],
                            7, BLANCO, o)
            if t > tN + 0.5:
                p.rrect(r[0] + 18, r[1] + 16, r[0] + 330, r[1] + 70, 27, NEGRO, 0.7 * o)
                p.circ(r[0] + 46, r[1] + 43, 11, ROJO, o * (0.4 + 0.6 * (int(t * 2.4) % 2)))
                p.texto("GAMEPLAY REAL", r[0] + 68, r[1] + 44, 28, BLANCO, "xbold", o, "lm")
    # --- frase 1: «Esto es Minecraft, dentro de Skyrim. Y no es un montaje.»
    f1 = INI(G, 1) - 0.12
    slam(p, "MINECRAFT", 540, 250, 158, VERDE, t, tM, sale=f1)
    slam(p, "DENTRO DE", 540, 392, 66, BLANCO, t, tD, "xbold", sale=f1, esp=0.12)
    slam(p, "SKYRIM", 540, 1235, 196, LILA, t, tS, sale=f1)
    if tN <= t < f1 + 0.3:
        kk = pop(t, tN, 0.28) * (1 - pr(t, f1, f1 + 0.2))
        with p.pivote(540, 1438, kk):
            p.rrect(150, 1380, 930, 1496, 18, mix(PANEL, ROJO, 0.25), 0.95, borde=ROJO, w=7)
            p.texto("NO ES UN MONTAJE", 540, 1441, 70, BLANCO, "black")
    # --- frase 2: lo que puedes hacer
    f2 = tR - 0.1
    chip(p, "PONER BLOQUES", 540, 1225, 66, VERDE, t, tB, sale=f2, icono=ic_cubo)
    chip(p, "VOLAR", 540, 1375, 66, CIAN, t, tV, sale=f2, icono=ic_alas)
    chip(p, "DINAMITA", 540, 1525, 66, NARANJA, t, tT, sale=f2, icono=ic_dinamita)
    if tT <= t < tT + 0.5:
        p.glow(540, 1525, 900, NARANJA, 0.5 * golpe(t, tT + 0.12, 0.4))
    # --- frase 3: «Lo raro es cómo funciona» -> el clip se mete en una ventana y aparece el esqueleto
    if k > 0:
        for i, x in enumerate(TX):                         # pistas que bajan de la ventana: aún no llevan a nada
            u = e_out(pr(t, tR + 0.5 + 0.1 * i, tR + 1.1 + 0.1 * i))
            pista(p, [(x, VT[3]), (x, lerp(VT[3], VT[3] + 150, u))], CIAN, t, 0.8 * (1 - pr(t, tDos - 0.2, tDos)))
        ys = lerp(VT[1], VT[3], (t - tR) * 0.9 % 1)        # línea de escáner sobre la ventana
        if t < tDos:
            p.rect(VT[0], ys - 3, VT[2], ys + 3, CIAN, 0.8 * k)
            p.rect(VT[0], ys - 46, VT[2], ys, CIAN, 0.10 * k)
    slam(p, "¿CÓMO", 540, 1010, 150, AMAR, t, tCo - 0.15, sale=tDos - 0.12)
    slam(p, "FUNCIONA?", 540, 1160, 124, AMAR, t, tCo + 0.12, sale=tDos - 0.12)
    # --- frase 4: dos formas
    for i, (num, tit, sub, col) in enumerate((("1", "EL PUENTE", "conectar dos juegos", CIAN), ("2", "LA REESCRITURA", "rehacerlo desde cero", MAGENTA))):
        t0 = tDos + 0.28 * i
        y0 = 930 + 330 * i
        kk = pop(t, t0, 0.34)
        if kk <= 0.01:
            continue
        mal = i == 1 and t >= tSeg
        col2 = mix(col, ROJO, 0.7 * pr(t, tMi - 0.2, tMi + 0.1)) if i == 1 else col
        apaga = 0.45 * smooth(pr(t, tSeg, tSeg + 0.3)) if i == 0 else 0.0
        sale = pr(t, T_PUENTE - 0.25, T_PUENTE + 0.05)
        s = kk * (1 + 0.05 * math.sin(t * 9) * mal) * (1 - sale)
        with p.pivote(540, y0 + 145, s):
            p.rrect(80, y0, 1000, y0 + 290, 30, mix(PANEL, col2, 0.14), 0.97 * (1 - apaga), borde=col2, w=7, op_b=1 - apaga)
            p.texto(num, 190, y0 + 150, 230, col2, "black", 1 - apaga)
            p.texto(tit, 300, y0 + 112, 74 if i == 0 else 64, BLANCO, "black", 1 - apaga, "lm")
            p.texto(sub, 302, y0 + 196, 42, mix(col2, BLANCO, 0.4), "semi", 1 - apaga, "lm")
            if mal and t >= tMi - 0.1:                     # aviso de peligro
                a = pop(t, tMi - 0.1, 0.3)
                p.poly([(900, y0 + 30), (960, y0 + 130), (840, y0 + 130)], AMAR, a)
                p.texto("!", 900, y0 + 95, 70, NEGRO, "black", a)
    return dict(golpe=0.5 * golpe(t, tM, 0.25) + 0.7 * golpe(t, tS, 0.3) + 0.5 * golpe(t, tN, 0.25) + 0.9 * golpe(t, tT + 0.12, 0.4)
                + 0.4 * golpe(t, tDos, 0.25),
                glitch=0.9 * golpe(t, tMi - 0.05, 0.7) + 0.5 * golpe(t, tR, 0.35), flash=0.25 * golpe(t, tT + 0.12, 0.3))


# ====================================================================== EL PUENTE (y el límite, mismo plano)
def _camara(t):
    a = smooth(pr(t, uCi - 0.35, uCi + 0.35)) - smooth(pr(t, INI(U, 5) - 0.45, INI(U, 5) + 0.2))
    z = 1 + 0.42 * a + 0.012 * math.sin(t * 0.9)
    return z, 540 + 10 * math.sin(t * 0.5), lerp(905, 912, a) + 8 * math.cos(t * 0.4)


def _billete(p, y, etiqueta, valor, col, t, t0, sale, icono=None):
    k = e_back(pr(t, t0, t0 + 0.32)) * (1 - pr(t, sale, sale + 0.2))
    if k <= 0.01:
        return
    x0 = lerp(-900, 90, min(1.0, k))
    p.rrect(x0, y - 58, x0 + 830, y + 58, 20, mix(PANEL, col, 0.2), 0.97, borde=col, w=5)
    p.rect(x0, y - 58, x0 + 16, y + 58, col)
    p.texto(etiqueta, x0 + 44, y - 20, 34, col, "black", 1, "lm", esp=0.05)
    p.texto(valor, x0 + 44, y + 24, 38, BLANCO, "mono", 1, "lm")
    u = pr(t, t0 + 0.35, t0 + 0.9)                          # la nota sube a la memoria
    if 0 < u < 1:
        paquete(p, [(x0 + 780, y), (980, y), (980, 1120), (760, 1040)], u, col, 12)


def puente(p, t):
    z, cx, cy = _camara(t)
    lim = t >= T_LIMITE
    fant = smooth(pr(t, uEsc - 0.1, uEsc + 0.5))
    with p.cam(z, cx, cy):
        # ---- ventana de arriba: Skyrim con video real
        ix = ventana(p, *VT, "Skyrim.exe", "PROCESO 1 · C++", LILA, t)
        clip_en(p, "skycraft_a", seg_clip(t), *ix, r=12, credito=CRED)
        # ---- ventana de abajo: Minecraft, dibujado; entra desde la derecha
        dxb = (1 - e_back(pr(t, uJ, uJ + 0.5), 1.2)) * 1150
        if t >= uJ:
            with p.grupo(dxb, 0):
                ixb = ventana(p, *VB, "Minecraft · Java", "PROCESO 2", VERDE, t, fantasma=fant)
                mundo_bloques(p, *ixb, t)
                vis = 0.62 * fant * (1 - 0.35 * smooth(pr(t, uMc - 0.2, uMc + 0.2)))
                p.rect(*ixb, mix(FONDO0, (0.05, 0.10, 0.2), 0.5), vis)              # velo: corre, pero nadie lo ve
                if fant > 0.3 and t < uMc:
                    for q in range(0, 12):                                         # rayas de «oculto»
                        yy = ixb[1] + ((q * 46 + t * 30) % (ixb[3] - ixb[1]))
                        p.rect(ixb[0], yy, ixb[2], yy + 3, VERDE, 0.10 * fant)
        # ---- memoria compartida y pistas
        km = pop(t, uMem - 0.1, 0.4)
        if km > 0:
            act = 0.35 + 0.65 * smooth(pr(t, uCi - 0.3, uCi + 0.2)) - 0.75 * smooth(pr(t, uNin - 0.3, uNin + 0.3))
            for i, x in enumerate(TX):
                o = pr(t, uMem + 0.15 + 0.08 * i, uMem + 0.5 + 0.08 * i) * (1 - 0.8 * smooth(pr(t, uNin - 0.2, uNin + 0.3)))
                pista(p, [(x, VT[3]), (x, MEM[1] - 16)], LILA, t, o)
                pista(p, [(x, VB[1]), (x, MEM[3] + 16)], VERDE, -t, o)
            memoria(p, *MEM, t, min(km, 1.08), clamp(act))
            ritmo = 1.2 + 3.2 * smooth(pr(t, uCi - 0.3, uCi + 0.3))
            if uLeer - 0.05 <= t < uNin:
                for i, x in enumerate(TX):                                         # paquetes: leer = de la memoria hacia fuera
                    u = (t * ritmo + i * 0.37) % 1
                    paquete(p, [(x, MEM[1] - 16), (x, VT[3])], u, CIAN, 8)
                    paquete(p, [(x, MEM[3] + 16), (x, VB[1])], (u + 0.5) % 1, CIAN, 8)
            if uEscr - 0.05 <= t < uNin:
                for i, x in enumerate(TX):                                         # escribir = hacia la memoria
                    u = (t * ritmo + i * 0.21 + 0.3) % 1
                    paquete(p, [(x + 26, VT[3]), (x + 26, MEM[1] - 16)], u, MAGENTA, 8)
                    paquete(p, [(x + 26, VB[1]), (x + 26, MEM[3] + 16)], (u + 0.4) % 1, MAGENTA, 8)
        # ---- reparto de papeles (frase 6)
        s5 = INI(U, 6) - 0.15
        for i, (tx_, tt, x) in enumerate((("JUGADOR", uMan, 235), ("INVENTARIO", uMan + 0.22, 540), ("COMBATE", uMan + 0.44, 838))):
            chip(p, tx_, x, VB[3] - 62, 40, VERDE, t, tt, sale=s5)
        for i, (tx_, tt, x) in enumerate((("EL MUNDO", uMun, 225), ("ENEMIGOS", uEne, 540), ("CHOQUES", uCho, 850))):
            chip(p, tx_, x, VT[3] - 62, 42, LILA, t, tt, sale=s5)
        if uMc <= t < s5 + 0.3:
            o = pr(t, uMc, uMc + 0.2) * (1 - pr(t, uSk - 0.1, uSk + 0.2))
            p.rrect(VB[0] - 8, VB[1] - 8, VB[2] + 8, VB[3] + 8, 28, None, o, borde=VERDE, w=10)
            o2 = pr(t, uSk, uSk + 0.2) * (1 - pr(t, s5, s5 + 0.3))
            p.rrect(VT[0] - 8, VT[1] - 8, VT[2] + 8, VT[3] + 8, 28, None, o2, borde=LILA, w=10)
        # ---- frase 7: ninguno sabe del otro -> muro en medio y cada ventana en su burbuja
        if t >= uNin - 0.1:
            m = e_out(pr(t, uNin - 0.1, uNin + 0.35))
            sale_m = 1 - pr(t, lAtr - 0.3, lAtr) if lim else 1.0
            x0, x1 = 540 - 520 * m, 540 + 520 * m
            p.rect(x0, MEM[1] - 26, x1, MEM[3] + 26, (0.02, 0.02, 0.05), 0.93 * sale_m)
            for q in range(-2, 26):                                                # franjas de aviso
                xx = q * 80 + (t * 40) % 80
                if x0 < xx < x1 - 40:
                    p.poly([(xx, MEM[1] - 26), (xx + 40, MEM[1] - 26), (xx + 20, MEM[1] - 6), (xx - 20, MEM[1] - 6)], AMAR, 0.85 * sale_m)
                    p.poly([(xx, MEM[3] + 6), (xx + 40, MEM[3] + 6), (xx + 20, MEM[3] + 26), (xx - 20, MEM[3] + 26)], AMAR, 0.85 * sale_m)
            for (vx0, vy0, vx1, vy1), col, sentido in ((VT, LILA, 1), (VB, VERDE, -1)):
                o = smooth(pr(t, uCree - 0.2, uCree + 0.3)) * sale_m
                p.rrect(vx0 - 14, vy0 - 14, vx1 + 14, vy1 + 14, 34, None, o * (0.7 + 0.3 * math.sin(t * 5)), borde=col, w=12)
                yy = vy1 - 150 if sentido > 0 else vy0 + 215
                kk = pop(t, uProp - 0.25 + (0.15 if sentido < 0 else 0), 0.3) * sale_m
                if kk > 0.01:
                    with p.pivote(540, yy, kk):
                        p.rrect(215, yy - 50, 865, yy + 50, 50, (0.02, 0.03, 0.07), 0.9, borde=col, w=5)
                        ic_ojo(p, 285, yy, 38, col, t + sentido, (math.sin(t * 2.3), 0))
                        p.texto("«todo pasa aquí»", 590, yy + 2, 46, BLANCO, "ital")
    # ---- textos en pantalla (no se mueven con la cámara)
    chip(p, "1 · EL PUENTE", 540, 96, 46, CIAN, t, uJ - 0.1, sale=T_FIN_A - 0.8)
    if t < uJ + 0.3:                                        # presentación: el puente se tiende entre dos orillas
        u = e_out(pr(t, T_PUENTE, uP + 0.2)) * (1 - pr(t, uJ - 0.12, uJ + 0.1))
        slam(p, "FORMA 1", 540, 1010, 62, BLANCO, t, T_PUENTE + 0.05, "xbold", sale=uJ - 0.12, esp=0.14)
        slam(p, "EL PUENTE", 540, 1150, 160, CIAN, t, uP - 0.18, sale=uJ - 0.12)
        if u > 0.01:
            p.elip(540, 1560, 400, 250, CIAN, min(1.0, u * 1.5), a0=180, a1=180 + 180 * u, w=12)
            for k2 in range(1, 8):
                if k2 / 8 < u:
                    an = math.radians(180 + 180 * k2 / 8)
                    p.linea((540 + 400 * math.cos(an), 1560 + 250 * math.sin(an)), (540 + 400 * math.cos(an), 1560), 5, CIAN, 0.55)
            p.linea((90, 1560), (990, 1560), 10, CIAN, min(1.0, u * 1.5))
            for xx, col in ((140, LILA), (940, VERDE)):
                p.circ(xx, 1560, 26, col, min(1.0, u * 1.5))
            paquete(p, [(140 + 800 * k3 / 20, 1560 - 250 * math.sin(math.pi * k3 / 20)) for k3 in range(21)], (t * 1.1) % 1, AMAR, 11)
    s1 = INI(U, 2) - 0.1
    chip(p, "A LA VEZ", 540, 910, 70, AMAR, t, uAl, sale=uSep - 0.1)
    chip(p, "DOS PROGRAMAS SEPARADOS", 540, 910, 52, AMAR, t, uSep - 0.05, sale=s1)
    s2 = INI(U, 3) - 0.1
    slam(p, "OCULTO", 540, 1300, 130, BLANCO, t, uEsc, sale=uVen - 0.1)
    chip(p, "SIN VENTANA", 540, 1290, 58, GRIS, t, uVen, sale=s2, icono=ic_ventana_no)
    chip(p, "SIN SONIDO", 540, 1430, 58, GRIS, t, uSon, sale=s2, icono=ic_sonido_no)
    s3 = uCi - 0.3
    if uLeer <= t < s3 + 0.3:
        o = 1 - pr(t, s3, s3 + 0.25)
        slam(p, "LEER", 180, 1047, 46, CIAN, t, uLeer, "black", sale=s3)
        slam(p, "ESCRIBIR", 880, 1047, 46, MAGENTA, t, uEscr, "black", sale=s3)
    s4 = INI(U, 5) - 0.3
    if uCi - 0.1 <= t < s4 + 0.3:
        o = pr(t, uCi - 0.1, uCi + 0.1) * (1 - pr(t, s4, s4 + 0.25))
        n = int((t - uCi + 0.1) * 240)
        p.rrect(190, 196, 890, 388, 26, (0.02, 0.03, 0.07), 0.88 * o, borde=AMAR, w=5, op_b=o)
        p.texto(f"{n:05d}", 540, 262, 104, AMAR, "mono", o)
        p.texto("INTERCAMBIOS · CIENTOS POR SEGUNDO", 540, 346, 30, BLANCO, "xbold", o, esp=0.03)
    px_ = 412 + int((t - uJug) * 7) if t > uJug else 412
    _billete(p, 1248, "POSICIÓN DEL JUGADOR", f"x {px_}   y 68   z -{97 + int(t * 3) % 9}", CIAN, t, uJug - 0.15, s4)
    _billete(p, 1392, "BLOQUE PUESTO", "piedra  ->  (413, 68, -97)", VERDE, t, uBlo - 0.15, s4)
    _billete(p, 1536, "GOLPE DADO", "enemigo  -12 de vida", MAGENTA, t, uGol - 0.2, s4)
    if uMc - 0.05 <= t < uSk:
        slam(p, "MANDA EN TU PERSONAJE", 540, VB[1] + 150, 60, BLANCO, t, uMan - 0.05, sale=uSk - 0.15)
    if uNin - 0.05 <= t and (not lim or t < lAtr):
        slam(p, "NINGUNO SABE DEL OTRO", 540, 912, 64, BLANCO, t, uNin, sale=(lLim - 0.2) if lim else None)
    fx = dict(golpe=0.5 * golpe(t, uJ + 0.42, 0.3) + 0.6 * golpe(t, uMem, 0.3) + 0.35 * (golpe(t, uJug, 0.2) + golpe(t, uBlo, 0.2) + golpe(t, uGol, 0.25))
              + 0.5 * golpe(t, uNin + 0.3, 0.3), glitch=0.5 * golpe(t, uEsc, 0.45), flash=0.12 * golpe(t, uMem, 0.3))
    if lim:
        _limite(p, t, fx)
    return fx


def _limite(p, t, fx):
    rojo = smooth(pr(t, lLim - 0.1, lLim + 0.3))
    p.im *= np.float32((1, 1 - 0.30 * rojo, 1 - 0.32 * rojo))
    slam(p, "LÍMITE", 540, 912, 190, ROJO, t, lLim, sale=lAtr - 0.15)
    zf = e_in(pr(t, T_FIN_A - 0.55, T_FIN_A))                 # al final la cámara se mete por la cerradura (negro)
    with p.cam(1 + 22 * zf, 540, 930):
        for i in range(13):                                    # barrotes que caen sobre las dos ventanas
            t0 = lAtr - 0.05 + 0.025 * abs(i - 6)
            u = pr(t, t0, t0 + 0.22)
            if u <= 0:
                continue
            x = 70 + i * 78.3
            y1 = lerp(-200, 1700, e_out(u)) + 26 * golpe(t, t0 + 0.22, 0.25)
            p.rect(x - 13, -40, x + 13, y1, (0.10, 0.11, 0.16))
            p.rect(x - 13, -40, x - 5, y1, (0.36, 0.38, 0.50))
            p.rect(x - 16, y1 - 14, x + 16, y1, (0.36, 0.38, 0.50))
        for y in (150, 1650):
            p.rect(30, y - 16, 1050, y + 16, (0.20, 0.22, 0.30), pr(t, lAtr + 0.1, lAtr + 0.25))
        k = pop(t, lMot - 0.25, 0.35)
        if k > 0.01:
            with p.pivote(540, 912, k):
                p.circ(540, 912, 200, (0.03, 0.03, 0.06), 0.96)
                p.circ(540, 912, 200, ROJO, 1, w=8)
                ic_candado(p, 540, 905, 108, AMAR, t)
                p.rrect(170, 1140, 910, 1250, 55, (0.03, 0.03, 0.06), 0.96, borde=ROJO, w=6)
                p.texto("MOTORES ORIGINALES", 540, 1197, 58, BLANCO, "black")
    fx["golpe"] += 0.9 * golpe(t, lLim, 0.3) + 1.0 * golpe(t, lAtr + 0.2, 0.4) + 0.5 * golpe(t, lMot - 0.1, 0.25)
    fx["glitch"] += 0.6 * zf
    if zf > 0:
        p.im *= 1 - zf
