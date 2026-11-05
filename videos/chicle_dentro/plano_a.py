# -*- coding: utf-8 -*-
"""GANCHO: en el parque la niña hace una bomba de chicle → ¡pop! → glup, se lo traga → «se queda pegado SIETE AÑOS»
(ventana a su panza con el chicle pegado y triste) → calendario que pasa de año en año mientras ella crece (pastel,
birrete) → «¿SERÁ CIERTO?» → la acuarela se desborda al MAPA DEL VIAJE: la bolita recorre boca → … → «sale» → «¡SÍ, POR AHÍ!»."""
import math

import cv2
import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr,
                      rgb, rotulo, rrect, suave, terminar)
from comun import FIN, INI, T0, T1, desborde, ww
from fondos_chicle import papel, patio
from personajes import AMARILLO, BLANCO, ROSA, destello, exclama, gota, kuri, pregunta
from personajes_ia import nina
from piezas_chicle import GRIS, ROJO, ROSA_CH, calendario, chicle, mapa_cuerpo

T_INI = 0.0
G = "gancho"
tTragas, tPegado, tEstomago, tSiete = ww(G, 0, "tragas"), ww(G, 0, "pegado"), ww(G, 0, "estomago"), ww(G, 0, "siete")
tCreces, tCumples, tPrimaria = ww(G, 1, "creces"), ww(G, 1, "cumples"), ww(G, 1, "primaria")
tCierto, tAveriguar, tSiguiendo, tCuerpo = ww(G, 2, "cierto"), ww(G, 2, "averiguarlo"), ww(G, 2, "siguiendo"), ww(G, 2, "cuerpo")
tBoca, tSale, tSi = ww(G, 3, "boca"), ww(G, 3, "sale"), ww(G, 3, "si")
T_MAPA = tSiguiendo - 0.6
T_FIN = T1(G)

NX, NY = 760, 600


def zoom(im, cx, cy, z, dx=0.0, dy=0.0):
    if z <= 1.001 and dx == 0 and dy == 0:
        return im
    tx, ty = lerp(cx, W / 2, dx), lerp(cy, H / 2, dy)
    M = np.array([[z, 0, tx - z * cx], [0, z, ty - z * cy]], np.float32)
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def bomba(im, x, y, r, t, seed=8000):
    if r < 3:
        return
    forma(im, elipse(x, y, r, r * 0.95), ROSA_CH, t, seed, tinta=max(2.0, r * 0.04), alfa=0.92, luz=(BLANCO, -r * 0.3, -r * 0.3, 0.4))
    brillo(im, x - r * 0.35, y - r * 0.35, r * 0.18, BLANCO, 0.7)


def ventana_panza(im, x, y, r, t, cara="triste"):
    """Círculo de papel sobre la panza con el estómago y el chicle pegado dentro."""
    if r < 6:
        return
    forma(im, elipse(x, y, r, r), rgb("f8e6dc"), t, 8100, tinta=5)
    forma(im, curva([(x - r * 0.5, y - r * 0.55), (x + r * 0.2, y - r * 0.6), (x + r * 0.6, y - r * 0.1), (x + r * 0.45, y + r * 0.45),
                     (x - r * 0.2, y + r * 0.5), (x - r * 0.55, y + r * 0.1)], 7, True), rgb("e48c8c"), t, 8101, tinta=3.6)
    chicle(im, x + r * 0.05, y + r * 0.05, r * 0.3, t, seed=8102, cara=cara)
    rotulo(im, "PEGADO", x, y + r + 40, 44, ROJO, t, seed=8103, rot=-0.05)


def parque(t):
    im = patio()
    # crecimiento durante la frase 1 (crece un poco y cambia de pose)
    cre = suave(pr(t, tCreces - 0.3, tPrimaria + 0.6))
    s = lerp(1.55, 1.85, cre)
    y = NY - 40 * cre
    pop = tTragas - 0.25
    if t < pop:
        boca, cara = "o", "normal"
    elif t < tPegado:
        boca, cara = "abierta", "susto"
    elif t < tSiete + 0.4:
        boca, cara = "o", "abiertos"
    elif t < tCierto:
        boca, cara = "duda", "triste"
    else:
        boca, cara = "duda", "normal"
    brazos = (0.3, 0.3) if t < tTragas else ((1.9, 1.9) if t < tPegado else (0.6, 0.6))
    p = nina(im, NX, y + 4 * math.sin(t * 2), s, t, cara=cara, boca=boca, brazos=brazos, codos=(-0.6, -0.6) if t < tPegado and
             t > tTragas else (0.4, 0.4), mira=0.6 if t < tCierto else 1.0)
    bx, by = NX, y - 78 * s
    # la bomba de chicle crece y revienta
    if t < pop:
        r = 18 + 120 * suave(pr(t, 0.3, pop))
        bomba(im, bx, by + 6, r, t)
    elif t < pop + 0.35:
        u = pr(t, pop, pop + 0.35)
        destello(im, bx, by, 1.6 * (1 - u), t, seed=8010, col=ROSA_CH)
        rotulo(im, "¡POP!", bx + 220, by - 120, 90, ROSA_CH, t, seed=8011, esc=e_back(u * 2 if u < 0.5 else 1))
    if pop + 0.2 < t < tPegado + 0.5:
        rotulo(im, "GLUP", bx - 230, by + 40, 80, AMARILLO, t, seed=8012, rot=0.1, esc=e_back(pr(t, pop + 0.25, pop + 0.5)))
        exclama(im, bx + 150, by - 170, 1.3 * e_back(pr(t, pop + 0.2, pop + 0.4)), t)
    # la ventana a la panza
    if t > tEstomago - 0.3:
        e = e_back(pr(t, tEstomago - 0.3, tEstomago + 0.1))
        ventana_panza(im, NX + 330, y + 40, 150 * e, t, cara="normal" if t < tSiete else "triste")
        if e > 0.3:
            linea(im, [(NX + 20, y), (NX + 190, y + 20)], 3, seed=8020, t=t, alfa=0.6, punta=False)
    # SIETE AÑOS + calendario que avanza
    if t > tSiete - 0.1:
        e = e_back(pr(t, tSiete - 0.1, tSiete + 0.25))
        anio = 1 + int(6.99 * pr(t, tCreces - 0.2, tPrimaria + 0.3))
        calendario(im, 1550, 330, 1.2 * e, t, "AÑO", str(anio))
        if t < tCreces:
            rotulo(im, "¡7 AÑOS!", 1550, 600, 120, AMARILLO, t, seed=8030, rot=-0.06, esc=e)
    # pastel y birrete
    if t > tCumples - 0.2:
        e = e_back(pr(t, tCumples - 0.2, tCumples + 0.15))
        cx, cy = 300, 690
        forma(im, rrect(cx, cy, 220 * e + 2, 110 * e + 2, 18 * e), rgb("f6efe2"), t, 8040, tinta=4,
              sombra=(rgb("e0c9a8"), 0, 10, 0.5))
        forma(im, rrect(cx, cy - 50 * e, 230 * e + 2, 30 * e + 2, 12 * e), ROSA, t, 8041, tinta=3.4)
        for k in range(7):
            vx = cx - 90 * e + k * 30 * e
            linea(im, [(vx, cy - 66 * e), (vx, cy - 110 * e)], 6 * e + 1, col=rgb(["4f86c6", "e35d4a", "e8b53e"][k % 3]),
                  seed=8042 + k, t=t, punta=False)
            brillo(im, vx, cy - 122 * e, 10 * e + 1, AMARILLO, 0.9)
    if t > tPrimaria - 0.2:
        e = e_back(pr(t, tPrimaria - 0.2, tPrimaria + 0.15))
        hx, hy = p["cabeza"]
        hy -= 70 * s
        forma(im, np.array([(hx - 110 * e, hy), (hx, hy - 40 * e), (hx + 110 * e, hy), (hx, hy + 40 * e)], np.float32),
              rgb("2a2a33"), t, 8050, tinta=3.6)
        linea(im, [(hx + 60 * e, hy), (hx + 90 * e, hy + 70 * e)], 4, col=AMARILLO, seed=8051, t=t, punta=False)
    # Kuri a la derecha
    kx, ky = 1250 + 20 * math.sin(t * 1.2), 330 + 18 * math.sin(t * 1.7)
    kuri(im, kx, ky, 1.7, t, cara="susto" if tTragas < t < tSiete + 0.6 else ("normal" if t < tCierto else "feliz"),
         brazos=(1.5, 1.5) if tTragas < t < tPegado else (0.5, 0.5))
    if t > tCierto - 0.2:
        rotulo(im, "¿SERÁ CIERTO?", W / 2, 140, 110, AMARILLO, t, seed=8060, rot=-0.04, esc=e_back(pr(t, tCierto - 0.2, tCierto + 0.15)))
        pregunta(im, kx + 120, ky - 170, e_back(pr(t, tCierto, tCierto + 0.25)), t)
    return im


def mapa(t):
    im = papel("calido")
    u = 0.0
    if t > tBoca - 0.2:
        u = suave(pr(t, tBoca - 0.2, tSale + 0.2))
    gx, gy = mapa_cuerpo(im, 1000, 660, 1.32, t, u=u)
    # Kuri chiquito montado en la bolita
    kuri(im, gx + 30, gy - 40, 0.42, t, cara="feliz" if t < tSi else "susto", aura=False)
    rotulo(im, "EL VIAJE DEL CHICLE", 470, 130, 80, rgb("e35d4a"), t, seed=8100, rot=-0.03,
           esc=e_back(pr(t, T_MAPA + 0.4, T_MAPA + 0.8)))
    # LUPA: los viajeros en grande (Kuri sentado en la bolita gris) con su hilo hasta la bolita del mapa
    e = e_back(pr(t, T_MAPA + 0.7, T_MAPA + 1.1))
    if e > 0.02:
        lx, ly, lr = 430, 520, 200 * e
        linea(im, [(lx + lr * 0.75, ly + lr * 0.6), (gx - 18, gy + 6)], 3, seed=8140, t=t, alfa=0.45, punta=False)
        forma(im, elipse(lx, ly, lr, lr), rgb("fbf3e4"), t, 8141, tinta=6, sombra=(rgb("d9c3a0"), 8, 12, 0.5))
        bote = 10 * math.sin(t * 5)
        chicle(im, lx, ly + 70 * e + bote * 0.3, 92 * e, t, seed=8142, cara="feliz" if t < tSi else "susto")
        kuri(im, lx, ly - 70 * e + bote, 0.95 * e, t, cara="feliz" if t < tSi else "susto", aura=False,
             brazos=(2.1, 0.5) if t < tBoca else (1.6, 1.6))
        linea(im, [(lx + lr * 0.7, ly + lr * 0.7), (lx + lr * 1.05, ly + lr * 1.05)], 16 * e + 1, col=rgb("6b4a2e"), seed=8143,
              t=t, punta=False)
    # la niña (la dueña del mapa) mira el recorrido desde la derecha y se apena al final
    ex = e_back(pr(t, T_MAPA + 0.5, T_MAPA + 0.9))
    if ex > 0.02:
        nina(im, 1730, 650 + 4 * math.sin(t * 2), 1.15 * ex, t, cara="abiertos" if t > tSi - 0.1 else "normal",
             boca="o" if t > tSi - 0.1 else "sonrisa", brazos=(0.3, 1.2) if t < tSi else (1.9, 1.9), mira=-0.8)
    # etiquetas del recorrido
    for k, (txt, x, y, tt) in enumerate([("BOCA", 1270, 200, tBoca), ("ESÓFAGO", 1310, 380, tBoca + 0.5),
                                         ("ESTÓMAGO", 1340, 560, tBoca + 1.0), ("INTESTINOS", 1360, 760, tBoca + 1.6)]):
        if t > tt:
            e = e_back(pr(t, tt, tt + 0.25))
            rotulo(im, txt, x, y, 52, rgb("2f4f86"), t, seed=8110 + k, esc=e)
            linea(im, [(x - 140, y + 4), (x - 300, y + 40)], 3, seed=8120 + k, t=t, alfa=0.5 * e, punta=False)
    if t > tSi - 0.1:
        e = e_back(pr(t, tSi - 0.1, tSi + 0.2))
        rotulo(im, "¡SÍ, POR AHÍ!", 520, 820, 100, AMARILLO, t, seed=8130, rot=0.06, esc=e)
        gota(im, gx + 80, gy - 110, 1.4 * e, t)
    return im


def cuadro_crudo(t):
    if t < T_MAPA:
        return parque(t)
    if t > T_MAPA + 0.9:
        return mapa(t)
    return desborde(parque(t), mapa(t), pr(t, T_MAPA, T_MAPA + 0.9), NX + 330, NY + 40, borde=(0.55, 0.3, 0.2))


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
