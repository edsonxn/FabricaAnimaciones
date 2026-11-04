# -*- coding: utf-8 -*-
"""GANCHO 0-10,8 s: buceo con luz → la sombra enorme sube con la boca abierta → negro (solo ojos y Kuri) → por fuera:
el cachalote con el bulto que baja por la garganta («¡GLUP!»)."""
import math

import numpy as np

from acuarela import (H, W, brillo, clamp, e_back, e_in, e_out, lerp, oscuridad, pr, rayos, rgb, rotulo, suave, terminar)
from comun import FIN, INI, T1, corte, desborde, fondo_agua, ww
from personajes import (BLANCO, OJO_K, alga, burbuja, buzo, cachalote, destello, exclama, kuri, pez, pregunta)

G = "gancho"
tEst, tTanque, tAire = INI(G, 0), ww(G, 0, "tanque"), ww(G, 0, "aire")
tPronto, tTodo, tNegro = ww(G, 1, "pronto"), ww(G, 1, "todo"), ww(G, 1, "negro")
tBallena, tTragar = ww(G, 2, "ballena"), ww(G, 2, "tragar")
T_NEGRO = tNegro + 0.15                   # pantalla negra total
T_FUERA = INI(G, 2) - 0.25                 # se abre el plano de fuera
T_FIN = T1(G)

AGUA_ARR, AGUA_ABA, AGUA_MAN = rgb("cdeee9"), rgb("2f7398"), rgb("4a8db0")
PECES = [rgb("f2b544"), rgb("f08a4b"), rgb("f6d06a")]


def _burbujas_de(im, boca, t, t_ini, cada=0.33, vida=2.6, seed=0, extra=()):
    k0 = int(max(0, (t - vida - t_ini) / cada))
    k1 = int((t - t_ini) / cada)
    for k in range(k0, k1 + 1):
        tb = t_ini + k * cada
        e = t - tb
        if e < 0 or e > vida:
            continue
        r = 6 + 3 * (k % 3) + e * 2
        burbuja(im, boca[0] + 14 * math.sin(e * 5 + k) + e * 8, boca[1] - e * 170, r, t, seed + k)
    for (tb, n) in extra:                  # ráfagas
        e = t - tb
        if 0 <= e < 2.2:
            for j in range(n):
                a = j * 2.4
                burbuja(im, boca[0] + 40 * math.cos(a) * e + 10 * math.sin(e * 6 + j), boca[1] - e * (200 + 30 * (j % 3)) - 10 * j,
                        8 + 5 * (j % 4), t, seed + 500 + j)


def buceo(t):
    """Plano A: buceo con luz; desde «pronto» sube el cachalote con la boca abierta y todo se oscurece."""
    fondo = fondo_agua(AGUA_ARR, AGUA_ABA, AGUA_MAN, H + 700, seed=3)
    im = corte(fondo, 60 + 70 * t)
    rayos(im, 640 + 40 * math.sin(t * 0.5), -160, [1.72, 1.86, 2.0, 2.16], 1700, 130, rgb("fff4d0"), 0.20)
    # algas del fondo (parallax: suben más rápido que el agua)
    par = 90 * t
    for k, (x0, lg) in enumerate(((60, 640), (250, 420), (860, 560), (1010, 720))):
        alga(im, x0, 2080 - par * 0.6, lg, t, seed=900 + k, col=rgb("7c9a48") * (0.85 + 0.1 * k % 2))
    # cardumen
    for k in range(7):
        fx = -150 + (t * 150 + k * 95) % 1400
        fy = 1270 + 50 * math.sin(k * 1.7) + 14 * math.sin(t * 2 + k)
        pez(im, fx, fy, 0.9 + 0.12 * (k % 3), t, PECES[k % 3], seed=800 + 7 * k)
    # buzo + Kuri
    susto = t > tPronto + 0.3
    bx = 470 + 26 * math.sin(t * 0.9)
    by = 880 + 22 * math.sin(t * 1.3)
    if susto:
        bx += 6 * math.sin(t * 40) * (1 - pr(t, tPronto + 1.6, tPronto + 2.5))
    br = 0.9 + 0.25 * math.sin(t * 2.6)
    cara = "susto" if susto else ("parpadeo" if (t % 2.9) < 0.12 else "normal")
    boca = buzo(im, bx, by, 1.35, t, rot=-0.18 + 0.05 * math.sin(t * 1.1), cara=cara,
                brazos=(br if not susto else 1.9, br if not susto else 1.9), codos=(0.5, 0.5),
                patada=1.0 if not susto else 1.6, vel=6 if not susto else 13)
    kx = 840 + 20 * math.sin(t * 1.2 + 1)
    ky = 640 + 26 * math.sin(t * 1.7)
    if t >= tTanque - 0.1 and t < tAire + 0.8:
        kc, kb = "feliz", (0.4, 1.7 + 0.3 * math.sin(t * 9))
    elif susto:
        kc, kb = "susto", (1.4, 1.4)
    else:
        kc, kb = "normal", (0.5, 0.5)
    kuri(im, kx, ky, 1.2, t, cara=kc, brazos=kb)
    _burbujas_de(im, boca, t, 0.0, extra=((tAire, 7),))
    if tTanque - 0.1 < t < tTanque + 1.4:            # «tanque»: destello sobre el tanque
        u = pr(t, tTanque - 0.1, tTanque + 0.2)
        destello(im, bx - 115, by - 40, 0.9 * e_back(u) * (1 - pr(t, tTanque + 1.0, tTanque + 1.4)), t, seed=1031)
        destello(im, bx - 60, by + 50, 0.5 * e_back(pr(t, tTanque + 0.15, tTanque + 0.4)) * (1 - pr(t, tTanque + 1.0, tTanque + 1.4)), t, seed=1032)
    if t > tPronto:                                    # «¡!» de Kuri
        u = pr(t, tPronto, tPronto + 0.25)
        exclama(im, kx, ky - 175, 1.3 * e_back(u), t)
    # la ballena sube desde abajo con la boca abierta (se ve con luz) y luego se lo traga todo
    if t > tPronto - 0.3:
        u1 = e_out(pr(t, tPronto - 0.3, tTodo + 0.55))
        u2 = e_in(pr(t, tTodo + 0.55, tNegro + 0.1))
        s = lerp(1.7, 2.5, u1) + 1.9 * u2
        top = lerp(H + 260, 1080, u1) - 900 * u2
        cachalote(im, bx - 125 * s, top + 500 * s, s, t, sx=1, rot=-math.pi / 2 + 0.12,
                  boca=suave(pr(t, tPronto + 0.1, tPronto + 0.7)) * (1 - 0.6 * u2), col=rgb("53607c"), arrugas=True)
    # se apaga la luz
    if t > tTodo + 0.4:
        n = suave(pr(t, tTodo + 0.4, tNegro + 0.1))
        oscuridad(im, 0.97 * n, luces=[(kx, ky, 160, 0.9)])
    return terminar(im, t)


def negro(t):
    """Negro total: solo los ojos del buzo y la pantalla de Kuri."""
    im = np.full((H, W, 3), 0.025, np.float32)
    im[..., 2] += 0.012
    bx, by = 470 + 26 * math.sin(t * 0.9), 880
    parp = (t - T_NEGRO) % 1.1 > 0.95
    from acuarela import elipse, forma, TINTA
    for d in (-1, 1):
        x, y = bx + d * 36, by - 165
        if parp:
            from acuarela import linea
            linea(im, [(x - 14, y), (x + 14, y)], 4, col=BLANCO * 0.9, seed=7 + d, t=t)
        else:
            forma(im, elipse(x, y, 17, 19), BLANCO * 0.92, t, 70 + d, tinta=0, amp=0.8)
            forma(im, elipse(x + 3 * math.sin(t * 3), y + 2, 7, 8), TINTA, t, 80 + d, tinta=0, amp=0.4)
    kx, ky = 840, 640
    brillo(im, kx, ky, 150, OJO_K * 0.5, 0.35)
    for d in (-1, 1):
        x = kx + d * 20
        forma(im, elipse(x, ky - 8, 10, 12), OJO_K, t, 90 + d, tinta=0, amp=0.4)
        brillo(im, x, ky - 8, 16, OJO_K, 0.5)
    return terminar(im, t, vineta=False)


def fuera(t):
    """Plano B: por fuera, el cachalote nada con el bulto bajando por la garganta."""
    fondo = fondo_agua(rgb("8fc9d6"), rgb("1f4d73"), rgb("356c94"), H + 500, seed=8, alfa=0.4)
    im = corte(fondo, 250 + 40 * (t - T_FUERA))
    rayos(im, 420, -160, [1.6, 1.78, 1.95], 1600, 120, rgb("fff4d0"), 0.14)
    for k in range(5):
        pez(im, 1180 - ((t - T_FUERA) * 120 + k * 230) % 1500, 420 + 90 * k, 0.6, t, rgb("f2b544") * (0.8 + 0.05 * k), sx=-1, seed=850 + k)
    u = pr(t, T_FUERA, T_FIN + 0.4)
    wx = lerp(830, 640, u)
    wy = 880 + 18 * math.sin(t * 1.4)
    trago = pr(t, tTragar - 0.25, tTragar + 1.6)
    cachalote(im, wx, wy, 1.1, t, sx=-1, rot=0.04 * math.sin(t * 1.4), bulto=(0.02 + 0.6 * suave(trago), 1.2),
              ojo="cerrado" if tTragar < t < tTragar + 0.9 else "abierto", col=rgb("5d6d89"))
    if t > tTragar - 0.1:
        e = pr(t, tTragar - 0.1, tTragar + 0.2)
        sale = 1 - pr(t, tTragar + 1.1, tTragar + 1.4)
        rotulo(im, "¡GLUP!", wx - 40, wy + 300, 120, rgb("f7e3b5"), t, seed=5, rot=-0.12, esc=e_back(e) * sale)
    if t > tBallena:
        e = e_back(pr(t, tBallena, tBallena + 0.3))
        pregunta(im, 250, 560, 1.4 * e, t)
    return terminar(im, t)


def cuadro(t):
    if t < T_NEGRO:
        return buceo(t)
    if t < T_FUERA:
        return negro(t)
    if t < T_FUERA + 0.6:
        return desborde(negro(t), fuera(t), pr(t, T_FUERA, T_FUERA + 0.6), cx=W * 0.5, cy=H * 0.55)
    return fuera(t)
