# -*- coding: utf-8 -*-
"""GANCHO: la niña le enseña a Kuri la foto del gato → Kuri contesta (globo que se escribe) → dibujo, radiografía y meme →
«no tiene ojos» (lupa sobre la pantalla-cara: los ojos son números) → «¿CÓMO LO SABE?» → zoom a la pantalla de Kuri y la
acuarela se desborda al interior de su cabeza: neuronas que se encienden una por una."""
import math

import cv2
import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb,
                      rotulo, rrect, suave, terminar)
from comun import FIN, INI, T1, desborde, ww
from fondos_ia import Y_MESA, cabeza, cuarto, neuronas
from personajes import AMARILLO, BLANCO, OJO_K, PANTALLA, destello, exclama, kuri, nube_lluvia, pregunta
from personajes_ia import dibujo_nino, foto_gato, gato, globo, meme_gato, nina, pegar, radiografia

G = "gancho"
tFoto, tIA, tMenos, tContesta = ww(G, 0, "foto"), ww(G, 0, "inteligencia"), ww(G, 0, "menos"), ww(G, 0, "contesta")
tUnGato, tTeclado = ww(G, 0, "gato") - 0.12, ww(G, 0, "teclado", fin=True)
tDibujo, tRadio, tMeme, tTambien = ww(G, 1, "dibujo"), ww(G, 1, "radiografia"), ww(G, 1, "meme"), ww(G, 1, "tambien")
tDetalle, tOjos, tNunca, tVisto = ww(G, 2, "detalle"), ww(G, 2, "ojos"), ww(G, 2, "nunca"), ww(G, 2, "gato")
tNi, tVer = ww(G, 2, "siquiera"), ww(G, 2, "ver")
tComo, tCabeza, tNeurona = ww(G, 3, "como"), ww(G, 3, "cabeza"), ww(G, 3, "neurona")
T_FIN = T1(G)

NX, NY, NS = 560, 600, 1.55            # niña
KX, KY, KS = 1330, 470, 2.5            # Kuri


def _kuri_pos(t):
    return KX + 14 * math.sin(t * 1.3), KY + 18 * math.sin(t * 1.9)


def zoom(im, cx, cy, z, dx=0.0, dy=0.0):
    """Acerca la cámara: el punto (cx, cy) se lleva hacia el centro (dx, dy = cuánto se mueve hacia él, 0..1)."""
    if z <= 1.001 and dx == 0 and dy == 0:
        return im
    tx = lerp(cx, W / 2, dx)
    ty = lerp(cy, H / 2, dy)
    M = np.array([[z, 0, tx - z * cx], [0, z, ty - z * cy]], np.float32)
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def _tarjetas(t):
    """(imagen, hora de entrada, respuesta de Kuri) del frase 1."""
    return [(dibujo_nino(t), tDibujo, ["UNA CASA, EL SOL", "Y UN PERRITO"]),
            (radiografia(t), tRadio, ["RADIOGRAFÍA", "DE UNA MANO"]),
            (meme_gato(t), tMeme, ["UN MEME:", "GATO EN UNA CAJA"])]


def cuarto_t(t):
    im = cuarto()
    kx, ky = _kuri_pos(t)
    # --- la niña: sostiene la foto hacia Kuri (y luego las tarjetas)
    sube = e_out(pr(t, tFoto - 0.6, tFoto + 0.1))
    foto = foto_gato(t)
    cards = _tarjetas(t)
    actual = None
    for img, ti, _ in cards:
        if t >= ti - 0.15:
            actual = (img, ti)
    bra = lerp(0.3, 1.75, sube)
    duda = t > tNi
    p = nina(im, NX, NY + 4 * math.sin(t * 2.0), NS, t, brazos=(0.35, bra) if not duda else (0.5, 0.5),
             codos=(0.4, lerp(0.4, -0.5, sube)) if not duda else (0.6, 0.6), mira=1.0,
             cara="normal" if not duda else "abiertos", boca="sonrisa" if t < tDetalle else ("duda" if duda else "o"))
    if not duda:                                       # lo que enseña, en su mano derecha (hacia Kuri), delante de todo
        mx, my = p["manos"][1]
        if actual is None:
            pegar(im, foto, mx + 150, my - 40, 0.62 * sube, -0.06, t=t)
        else:
            img, ti = actual
            gira = e_back(pr(t, ti - 0.15, ti + 0.15))
            pegar(im, img, mx + 150, my - 40, 0.62 * gira, 0.05 * math.sin(ti), t=t, seed=4550)
        forma(im, elipse(mx, my, 13 * NS, 13 * NS), rgb("f4cfae"), t, 4560, tinta=3.6 * NS)      # la mano encima del marco
    # la tarjeta anterior sale volando hacia arriba a la izquierda
    for k, (img, ti, _) in enumerate(cards):
        sale = cards[k + 1][1] if k + 1 < len(cards) else tNi
        u = pr(t, sale - 0.15, sale + 0.45)
        if 0 < u < 1:
            pegar(im, img, lerp(NX + 330, -200, e_in(u)), lerp(NY - 170, -150, e_in(u)), 0.62 * (1 - 0.4 * u), -0.8 * u, t=t,
                  seed=4570 + k)
    if 0 < pr(t, tDibujo - 0.15, tDibujo + 0.45) < 1:
        u = pr(t, tDibujo - 0.15, tDibujo + 0.45)
        pegar(im, foto, lerp(NX + 330, -200, e_in(u)), lerp(NY - 170, -150, e_in(u)), 0.62 * (1 - 0.4 * u), -0.8 * u, t=t,
              seed=4580)
    # --- Kuri y su respuesta
    cara = "normal"
    if tContesta < t < tUnGato + 0.2 or (tDibujo - 0.2 < t < tTambien):
        cara = "normal"
    if tTambien < t < tDetalle:
        cara = "feliz"
    kuri(im, kx, ky, KS, t, cara=cara, brazos=(1.4, 1.4) if tTambien < t < tDetalle else (0.5, 0.5),
         luz=1.0 if t < tOjos else 0.7)
    if tMenos - 0.1 < t < tDibujo - 0.3:                                              # cronómetro «0,3 s»
        e = e_back(pr(t, tMenos - 0.1, tMenos + 0.2)) * (1 - pr(t, tContesta + 0.2, tContesta + 0.5))
        if e > 0.02:
            forma(im, elipse(kx - 330, ky - 230, 58 * e, 58 * e), BLANCO, t, 6000, tinta=4)
            linea(im, [(kx - 330, ky - 230), (kx - 330 + 40 * e * math.sin(t * 9), ky - 230 - 40 * e * math.cos(t * 9))], 5,
                  seed=6001, t=t)
            rotulo(im, "0,3 s", kx - 330, ky - 140, int(46 * max(e, 0.3)), AMARILLO, t, seed=6002, esc=e)
    if tUnGato - 0.1 < t < tDibujo - 0.1:                                             # la respuesta se escribe
        txt = ["UN GATO NARANJA", "DORMIDO SOBRE UN TECLADO"]
        n = 39 * pr(t, tUnGato, tTeclado)
        a = 1 - pr(t, tDibujo - 0.4, tDibujo - 0.1)
        globo(im, kx + 40, ky - 300, 560, 150, "", t, px=36, n=n, lineas=txt, alfa=a, cola=(-1, 1))
    for k, (img, ti, resp) in enumerate(cards):                                       # respuestas cortas
        nxt = cards[k + 1][1] if k + 1 < len(cards) else tDetalle
        if ti + 0.25 < t < nxt:
            n = 30 * pr(t, ti + 0.25, ti + 0.85)
            globo(im, kx + 40, ky - 300, 520, 140, "", t, px=34, n=n, lineas=resp, seed=5010 + 3 * k)
            if t > ti + 0.85:
                destello(im, kx + 300, ky - 380, 0.9 * e_back(pr(t, ti + 0.85, ti + 1.05)), t, seed=1030 + k)
    # --- «no tiene ojos»: lupa sobre la cara de Kuri, los ojos son números
    if t > tOjos - 0.2 and t < tComo:
        e = e_back(pr(t, tOjos - 0.2, tOjos + 0.2))
        lx, ly, r = kx + 330, ky + 60, 150 * e
        if r > 4:
            forma(im, elipse(lx, ly, r, r), PANTALLA, t, 6100, tinta=6)
            for i in range(5):
                for j in range(3):
                    v = "01"[(i * 7 + j * 3 + int(t * 6)) % 2]
                    rotulo(im, v, lx - 70 + 35 * i, ly - 40 + 40 * j, int(30 * e) + 4, OJO_K, t, seed=6110 + i * 3 + j,
                           tinta=False, alfa=0.9)
            linea(im, [(lx + r * 0.7, ly + r * 0.7), (lx + r * 1.25, ly + r * 1.25)], 22, col=rgb("7a4a2a"), seed=6102, t=t)
            linea(im, [(kx + 34, ky - 10), (lx - r, ly)], 2.5, seed=6103, t=t, alfa=0.5, punta=False)
            rotulo(im, "¿OJOS? NO", lx, ly - r - 50, 56, rgb("e35d4a"), t, seed=6104, esc=e)
    if tNunca - 0.1 < t < tComo:                                                       # nube: nunca ha visto un gato
        e = e_back(pr(t, tNunca - 0.1, tNunca + 0.25))
        cx, cy = kx - 330, ky - 250
        forma(im, elipse(cx, cy, 170 * e, 110 * e), BLANCO, t, 6200, tinta=4)
        for k, (ox, oy, rr) in enumerate([(-90, 110, 22), (-130, 150, 13)]):
            forma(im, elipse(cx + ox * e, cy + oy * e, rr * e, rr * e), BLANCO, t, 6201 + k, tinta=3)
        if e > 0.5:
            gato(im, cx, cy + 20, 0.42 * e, t, pose="dormido", seed=6210)
            if t > tVisto:
                linea(im, [(cx - 120, cy - 70), (cx + 120, cy + 70)], 9, col=rgb("e35d4a"), seed=6220, t=t)
                linea(im, [(cx + 120, cy - 70), (cx - 120, cy + 70)], 9, col=rgb("e35d4a"), seed=6221, t=t)
    if t > tNi:
        pregunta(im, kx + 40, ky - 260, 1.2 * e_back(pr(t, tNi, tNi + 0.25)), t)
        pregunta(im, p["cabeza"][0] + 120, p["cabeza"][1] - 170, 1.0 * e_back(pr(t, tVer, tVer + 0.25)), t, seed=1011)
    if t > tComo - 0.1:
        rotulo(im, "¿CÓMO LO SABE?", W / 2, 150, 120, AMARILLO, t, seed=6300, rot=-0.04,
               esc=e_back(pr(t, tComo - 0.1, tComo + 0.25)), alfa=1 - pr(t, tCabeza - 0.6, tCabeza - 0.3))
    return im, (kx, ky)


def interior(t):
    im = cabeza()
    # las neuronas se encienden una por una desde «neurona por neurona»
    u = pr(t, tNeurona - 0.3, T_FIN + 0.4)
    neuronas(im, t, n=70, seed=7, luz=0.3 + 0.7 * u, ondas=u)
    rotulo(im, "DENTRO DE KURI", W / 2, 140, 88, OJO_K, t, seed=6400, esc=e_back(pr(t, tCabeza + 0.6, tCabeza + 0.9)),
           alfa=1 - pr(t, T_FIN - 0.4, T_FIN))
    return im


def cuadro_crudo(t):
    if t < tCabeza - 0.5:
        im, _ = cuarto_t(t)
        return im
    if t > tCabeza + 0.9:
        return interior(t)
    # zoom a la pantalla de Kuri y desborde al interior
    im, (kx, ky) = cuarto_t(t)
    u = e_in(pr(t, tCabeza - 0.5, tCabeza + 0.5))
    z = 1 + 5 * u
    A_ = zoom(im, kx, ky - 10, z, dx=suave(pr(t, tCabeza - 0.5, tCabeza)), dy=suave(pr(t, tCabeza - 0.5, tCabeza)))
    if t < tCabeza + 0.05:
        return A_
    B_ = interior(t)
    return desborde(A_, B_, pr(t, tCabeza + 0.05, tCabeza + 0.9), W / 2, H / 2, borde=(0.1, 0.25, 0.28))


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
