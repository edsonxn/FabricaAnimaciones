# -*- coding: utf-8 -*-
"""PÍXELES: la foto grande → zoom al ojo del gato hasta ver los cuadritos → un píxel sale con sus tres números (R, V, A, 0-255)
→ «12 000 000 PÍXELES» × 3 = «36 000 000 NÚMEROS» → la foto se vuelve una tabla de números → el gato se mueve y se apaga la luz:
los números cambian (rojo) pero sigue siendo el gato → la regla a mano «OREJAS △ = GATO» → poses que la rompen, la oreja hecha
números con «?», tache: NO FUNCIONÓ."""
import math

import cv2
import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb,
                      rotulo, rrect, suave, terminar)
from comun import FIN, INI, T0, T1, desborde, ww
from fondos_ia import papel
from personajes import AMARILLO, BLANCO, OJO_K, destello, exclama, gota, kuri, nube_lluvia, pregunta
from personajes_ia import celda, foto_gato, gato, lienzo, meme_gato, nina, pegar

P = "pixeles"
T_INI = T0(P)
tAcercas, tCuadritos, tPixeles = ww(P, 0, "acercas"), ww(P, 0, "cuadritos"), ww(P, 0, "pixeles")
tCada, tTres, tRojo, tVerde, tAzul = ww(P, 1, "pixel"), ww(P, 1, "tres"), ww(P, 1, "rojo"), ww(P, 1, "verde"), ww(P, 1, "azul")
tCero, tDosc = ww(P, 1, "cero"), ww(P, 1, "doscientos")
tDoce, tO, tTreinta = ww(P, 2, "doce"), ww(P, 2, "o"), ww(P, 2, "treinta")
tPara, tTabla, tNada = ww(P, 3, "para"), ww(P, 3, "tabla"), ww(P, 3, "nada")
tProblema, tMueve, tLuz, tCambian, tMismo = (ww(P, 4, "problema"), ww(P, 4, "mueve"), ww(P, 4, "luz"), ww(P, 4, "cambian"),
                                             ww(P, 4, "mismo"))
tDecadas, tReglas, tSi, tTriang = ww(P, 5, "decadas"), ww(P, 5, "reglas"), ww(P, 5, "si"), ww(P, 5, "triangulo")
tExplicas, tOreja, tNoFunc = ww(P, 6, "explicas"), ww(P, 6, "oreja"), ww(P, 6, "funciono")
T_FIN = T1(P)

FW, FH = 560, 420
OJO = (int(FW * 0.45 + 176 * 1.05), int(FH * 0.6 - 34 * 1.05))   # ojo del gato dentro de la foto
ROJO, VERDE_, AZUL_ = rgb("e0483c"), rgb("45a85a"), rgb("3f78c8")


def _foto_px(t):
    return (np.clip(foto_gato(t), 0, 1) * 255).round() / 255


def mosaico(img, cx, cy, ancho_src, w_out, h_out):
    """Recorta `ancho_src` px alrededor de (cx, cy) de img y lo amplía a w_out×h_out con vecino más cercano (píxeles visibles)."""
    h_src = ancho_src * h_out / w_out
    x0, y0 = cx - ancho_src / 2, cy - h_src / 2
    sx, sy = w_out / ancho_src, h_out / h_src
    M = np.array([[sx, 0, -x0 * sx], [0, sy, -y0 * sy]], np.float32)
    interp = cv2.INTER_NEAREST if ancho_src < 120 else cv2.INTER_AREA if ancho_src > 400 else cv2.INTER_LINEAR
    return cv2.warpAffine(img, M, (w_out, h_out), flags=interp, borderMode=cv2.BORDER_REPLICATE), (x0, y0, sx, sy)


def _rejilla(im, ox, oy, w, h, paso, x0f, y0f, t, alfa):
    """Líneas de tinta entre píxeles del mosaico."""
    if paso < 14 or alfa <= 0:
        return
    kx0 = math.floor(x0f)
    for k in range(int(w / paso) + 3):
        x = ox + (kx0 + k - x0f) * paso
        if ox <= x <= ox + w:
            linea(im, [(x, oy), (x, oy + h)], 1.8, seed=7000 + k % 9, t=t, alfa=0.55 * alfa, punta=False, amp=0.4)
    ky0 = math.floor(y0f)
    for k in range(int(h / paso) + 3):
        y = oy + (ky0 + k - y0f) * paso
        if oy <= y <= oy + h:
            linea(im, [(ox, y), (ox + w, y)], 1.8, seed=7020 + k % 9, t=t, alfa=0.55 * alfa, punta=False, amp=0.4)


# ------------------------------------------------------------ 1) zoom a los píxeles y el píxel con sus números
def _zoom_px(t):
    im = papel("frio")
    foto = _foto_px(t)
    VW, VH = 1100, 825                                      # ventana de la foto
    cx0, cy0 = W / 2 - 300 * pr(t, tCada, tTres), H / 2 + 10
    u = e_in(pr(t, tAcercas - 0.2, tPixeles + 0.2)) ** 0.7
    ancho = lerp(FW, 15, u)                                  # cuántos píxeles de la foto caben a lo ancho
    ccx = lerp(FW / 2, OJO[0], suave(pr(t, tAcercas - 0.2, tCuadritos)))
    ccy = lerp(FH / 2, OJO[1], suave(pr(t, tAcercas - 0.2, tCuadritos)))
    vw = int(lerp(VW, 860, pr(t, tCada, tTres)))
    vh = int(vw * 0.75)
    vista, (x0f, y0f, sx, sy) = mosaico(foto, ccx, ccy, ancho, vw, vh)
    ox, oy = int(cx0 - vw / 2), int(cy0 - vh / 2)
    lavado(im, rrect(cx0 + 14, cy0 + 18, vw + 40, vh + 40, 8), rgb("6a7a7a"), 0.35, 7100)
    forma(im, rrect(cx0, cy0, vw + 34, vh + 34, 8), BLANCO, t, 7101, tinta=4)
    im[oy:oy + vh, ox:ox + vw] = vista
    _rejilla(im, ox, oy, vw, vh, sx, x0f, y0f, t, pr(t, tCuadritos - 0.3, tCuadritos + 0.2))
    linea(im, rrect(cx0, cy0, vw, vh, 2), 3, seed=7102, t=t, cerrado=True, punta=False)
    if t > tPixeles - 0.1 and t < tCada + 0.3:
        rotulo(im, "PÍXELES", cx0, oy - 20, 110, AMARILLO, t, seed=7110, rot=-0.03,
               esc=e_back(pr(t, tPixeles - 0.1, tPixeles + 0.2)), alfa=1 - pr(t, tCada, tCada + 0.3))
    # el píxel elegido (centro de la vista) sale volando a la derecha
    if t > tCada - 0.1:
        e = e_out(pr(t, tCada - 0.1, tTres))
        col = foto[int(ccy), int(ccx)]
        px_ = ox + (math.floor(ccx) - x0f + 0.5) * sx
        py_ = oy + (math.floor(ccy) - y0f + 0.5) * sy
        linea(im, rrect(px_, py_, sx, sy, 2), 6, col=AMARILLO, seed=7120, t=t, cerrado=True, punta=False)
        X, Y = lerp(px_, 1530, e), lerp(py_, 400, e)
        lado = lerp(sx, 300, e)
        forma(im, rrect(X, Y, lado, lado, lado * 0.06), col, t, 7121, tinta=5)
        for i, (nom, c, ti) in enumerate((("ROJO", ROJO, tRojo), ("VERDE", VERDE_, tVerde), ("AZUL", AZUL_, tAzul))):
            if t > ti - 0.1:
                a = e_back(pr(t, ti - 0.1, ti + 0.2))
                by = 640 + i * 110
                v = int(round(col[i] * 255))
                forma(im, rrect(1320 + 150 * (v / 255) * a, by, 300 * (v / 255) * a + 4, 54, 12), c, t, 7130 + i, tinta=3.6)
                linea(im, rrect(1470, by, 300, 54, 12), 2.4, seed=7135 + i, t=t, cerrado=True, punta=False, alfa=0.6)
                rotulo(im, nom, 1240, by, 40, c, t, seed=7140 + i, esc=a)
                rotulo(im, str(v), 1700, by, 54, c, t, seed=7145 + i, esc=a)
        if t > tCero - 0.1:                                  # escala 0-255
            a = e_back(pr(t, tCero - 0.1, tCero + 0.2))
            g = np.linspace(0, 1, 300, dtype=np.float32)
            y = 990
            band = np.repeat(np.repeat(g[None, :, None], 3, 2), 30, 0)
            x0b = 1320
            im[y - 15:y + 15, x0b:x0b + 300] = im[y - 15:y + 15, x0b:x0b + 300] * (1 - a) + band * a
            linea(im, rrect(x0b + 150, y, 300, 30, 4), 2.4, seed=7150, t=t, cerrado=True, punta=False, alfa=a)
            rotulo(im, "0", x0b - 30, y, 40, BLANCO, t, seed=7151, esc=a)
            rotulo(im, "255", x0b + 350, y, 40, BLANCO, t, seed=7152, esc=e_back(pr(t, tDosc - 0.1, tDosc + 0.2)))
    return im


# ------------------------------------------------------------ 2) 12 millones × 3 y la tabla de números
def _tabla(im, t, x, y, w, h, foto, nc, nr, u_num, rojo=None, px=None):
    """Dibuja la foto como tabla de nc×nr celdas: color de fondo (1−u_num) → número en su color (u_num).
    rojo = máscara nc×nr de celdas que «cambiaron» (en rojo)."""
    peq = cv2.resize(foto, (nc, nr), interpolation=cv2.INTER_AREA)
    cw, ch = w / nc, h / nr
    px = px or int(ch * 0.42)
    for j in range(nr):
        for i in range(nc):
            col = peq[j, i]
            x0, y0 = int(x + i * cw), int(y + j * ch)
            sub = im[y0:int(y0 + ch), x0:int(x0 + cw)]
            sub[:] = sub * u_num + (col * (1 - u_num * 0.82) + BLANCO * u_num * 0.82)
            if u_num > 0.3:
                v = int(round(col.mean() * 255))
                c = rgb("d0342a") if (rojo is not None and rojo[j, i]) else np.clip(col * 0.75, 0, 0.7)
                rotulo(im, str(v), x0 + cw / 2, y0 + ch / 2, px, c, t, seed=7200 + (i * 7 + j) % 40, tinta=False,
                       alfa=pr(u_num, 0.3, 0.8))
    linea(im, rrect(x + w / 2, y + h / 2, w, h, 4), 3, seed=7290, t=t, cerrado=True, punta=False)


def _cuenta(t):
    im = papel("frio")
    foto = _foto_px(t)
    # el celular con la foto a la izquierda
    e = e_back(pr(t, tDoce - 0.3, tDoce + 0.1))
    cx, cy = 470, 560
    forma(im, rrect(cx, cy, 420 * e, 760 * e, 50 * e), rgb("2b2f3a"), t, 7300, tinta=5)
    if e > 0.6:
        f = cv2.resize(foto, (360, 270), interpolation=cv2.INTER_AREA)
        im[cy - 135:cy + 135, cx - 180:cx + 180] = f
        linea(im, rrect(cx, cy, 360, 270, 2), 2.4, seed=7301, t=t, cerrado=True, punta=False)
    rotulo(im, "12 000 000", 1270, 330, 120, AMARILLO, t, seed=7310, esc=e_back(pr(t, tDoce - 0.05, tDoce + 0.25)))
    rotulo(im, "PÍXELES", 1270, 450, 70, BLANCO, t, seed=7311, esc=e_back(pr(t, tDoce + 0.2, tDoce + 0.45)))
    if t > tO:
        rotulo(im, "× 3", 1270, 580, 90, BLANCO, t, seed=7312, esc=e_back(pr(t, tO, tO + 0.25)))
    if t > tTreinta - 0.1:
        e2 = e_back(pr(t, tTreinta - 0.1, tTreinta + 0.25))
        rotulo(im, "36 000 000", 1270, 730, 140, rgb("ffb35a"), t, seed=7313, esc=e2)
        rotulo(im, "NÚMEROS", 1270, 860, 80, BLANCO, t, seed=7314, esc=e2)
        for k in range(26):                                   # números que llueven del celular
            ph = (t * 0.9 + k * 0.137) % 1
            x = cx - 170 + (k * 53) % 340
            rotulo(im, str((k * 97 + int(t * 8) * 13) % 256), x, cy - 380 + 760 * ph, 30, OJO_K * 0.8, t, seed=7320 + k % 20,
                   tinta=False, alfa=0.8 * e2 * (1 - ph))
    return im


def _gato_tabla(t):
    im = papel("frio")
    foto = _foto_px(t)
    u = e_in(pr(t, tTabla - 0.3, tTabla + 0.8))
    x, y, w, h = 360, 120, 1200, 900
    _tabla(im, t, x, y, w, h, foto, 16, 12, u)
    if t > tNada - 0.1:
        kuri(im, 1730, 860, 1.3, t, cara="normal", brazos=(2.2, 2.2))
        rotulo(im, "NADA MÁS", 1650, 680, 64, AMARILLO, t, seed=7400, esc=e_back(pr(t, tNada - 0.1, tNada + 0.2)), rot=0.05)
    return im


# ------------------------------------------------------------ 3) el gato se mueve, se apaga la luz: los números cambian
def _cambio(t):
    im = papel("frio")
    a = _foto_px(t)
    mueve = pr(t, tMueve - 0.2, tMueve + 0.4)
    b = foto_gato(t, pose="despierto") if mueve > 0.5 else a
    b = (np.clip(b, 0, 1) * 255).round() / 255
    luz = 1 - 0.55 * suave(pr(t, tLuz - 0.2, tLuz + 0.3))
    b = b * luz
    pegar(im, a, 500, 330, 0.75, -0.03, t=t, seed=7500)
    pegar(im, b, 1420, 330, 0.75, 0.03, t=t, seed=7510)
    nc, nr = 10, 6
    pa = cv2.resize(a, (nc, nr), interpolation=cv2.INTER_AREA).mean(2)
    pb = cv2.resize(b, (nc, nr), interpolation=cv2.INTER_AREA).mean(2)
    roj = np.abs(pa - pb) > 0.02
    un = e_out(pr(t, tProblema, tProblema + 0.6))
    _tabla(im, t, 290, 640, 420, 252, a, nc, nr, un, px=22)
    _tabla(im, t, 1210, 640, 420, 252, b, nc, nr, un, rojo=roj if t > tCambian - 0.1 else None, px=22)
    if t > tCambian:
        rotulo(im, "≠", W / 2, 766, 160, rgb("e35d4a"), t, seed=7520, esc=e_back(pr(t, tCambian, tCambian + 0.25)), fuente="seguisym.ttf")
    if t > tMismo - 0.1:
        e = e_back(pr(t, tMismo - 0.1, tMismo + 0.25))
        rotulo(im, "= MISMO GATO", W / 2, 330, 84, AMARILLO, t, seed=7530, esc=e)
        destello(im, W / 2 + 300, 250, 1.0 * e, t, seed=1031)
    return im


# ------------------------------------------------------------ 4) reglas a mano
def _reglas(t):
    im = papel("calido")
    # la niña científica con bata (= la niña) y su cuaderno de reglas
    e = e_out(pr(t, tDecadas - 0.3, tDecadas + 0.3))
    falla = t > tExplicas - 0.1
    nina(im, 330, 640, 1.45, t, cara="apretados" if t > tNoFunc else ("abiertos" if falla else "normal"),
         boca="o" if falla else "sonrisa", brazos=(0.6, 2.0), codos=(0.5, 1.2), mira=1.0)
    # tarjeta de la regla
    ce = e_back(pr(t, tSi - 0.15, tSi + 0.2))
    if ce > 0.02:
        forma(im, rrect(860, 250, 640 * ce, 200 * ce, 16, -0.02), rgb("fff7d6"), t, 7600, tinta=4)
        for k in range(4):
            linea(im, [(560, 200 + 30 * k), (1160, 196 + 30 * k)], 1.5, col=rgb("9fc1d9"), seed=7601 + k, t=t, alfa=0.6 * ce,
                  punta=False)
        rotulo(im, "REGLA 1:", 860, 200, 46, rgb("3f78c8"), t, seed=7605, esc=ce, tinta=False)
        rotulo(im, "OREJAS EN TRIÁNGULO = GATO", 860, 280, 44, TINTA, t, seed=7606, esc=ce, tinta=False)
    # el gato de la foto con las orejas marcadas
    pegar(im, _foto_px(t), 1520, 330, 0.62, 0.04, t=t, seed=7610)
    if t > tTriang - 0.1:
        e2 = e_back(pr(t, tTriang - 0.1, tTriang + 0.2))
        hx, hy = FW * 0.45 + 157.5, FH * 0.6 - 31.5            # cabeza del gato dentro de la foto
        for d in (-1, 1):
            tri = [(hx + d * 6 * 1.05, hy - 62 * 1.05), (hx + d * 56 * 1.05, hy - 104 * 1.05), (hx + d * 40 * 1.05, hy - 40 * 1.05)]
            tri = [(1520 + (x - FW / 2) * 0.62, 330 + (y - FH / 2) * 0.62) for x, y in tri + tri[:1]]
            linea(im, tri, 5, col=rgb("e35d4a"), seed=7620 + d, t=t, alfa=e2, punta=False)
    # gatos que rompen la regla (enroscado de espaldas, en la caja, orejas dobladas)
    if t > tExplicas - 0.6:
        for k, pose in enumerate(("espalda", "despierto")):
            ap = e_back(pr(t, tExplicas - 0.6 + 0.25 * k, tExplicas - 0.3 + 0.25 * k))
            if ap > 0.02:
                gx, gy = 760 + 380 * k, 760
                forma(im, rrect(gx, gy, 330 * ap, 250 * ap, 20), BLANCO, t, 7630 + k, tinta=4)
                if ap > 0.5:
                    gato(im, gx, gy + 20, 0.62 * ap, t, pose=pose, seed=7640 + 50 * k, sx=-1 if k else 1)
                pregunta(im, gx + 150, gy - 130, 0.8 * ap, t, seed=1012 + k)
    # la oreja hecha números
    if t > tOreja - 0.2:
        e3 = e_back(pr(t, tOreja - 0.2, tOreja + 0.2))
        bx, by = 1560, 760
        forma(im, rrect(bx, by, 300 * e3, 260 * e3, 18), rgb("e6f0ec"), t, 7660, tinta=4)
        if e3 > 0.5:
            for j in range(4):
                for i in range(4):
                    rotulo(im, str((i * 61 + j * 37 + 140) % 256), bx - 105 + 70 * i, by - 90 + 60 * j, 30, rgb("c56a26"), t,
                           seed=7670 + i + 4 * j, tinta=False)
            rotulo(im, "¿OREJA?", bx, by - 175, 54, rgb("e35d4a"), t, seed=7690, esc=e3)
    if t > tNoFunc - 0.1:
        e4 = e_out(pr(t, tNoFunc - 0.1, tNoFunc + 0.25))
        linea(im, [(560, 160), (560 + 600 * e4, 160 + 190 * e4)], 14, col=rgb("e35d4a"), seed=7700, t=t)
        linea(im, [(1160, 160), (1160 - 600 * e4, 160 + 190 * e4)], 14, col=rgb("e35d4a"), seed=7701, t=t)
        rotulo(im, "NO FUNCIONÓ", 860, 470, 80, rgb("e35d4a"), t, seed=7702, esc=e_back(pr(t, tNoFunc, tNoFunc + 0.25)), rot=-0.05)
        nube_lluvia(im, 330, 300, 0.9 * e4, t)
    return im


TRAMOS = [(_zoom_px, T_INI), (_cuenta, tDoce - 0.5), (_gato_tabla, tPara - 0.3), (_cambio, tProblema - 0.3),
          (_reglas, tDecadas - 0.4)]
DUR_T = 0.6


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + DUR_T:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + DUR_T), W * (0.3 + 0.1 * k), H / 2)
        else:
            import plano_a
            im = desborde(plano_a.cuadro_crudo(t), im, pr(t, ti, ti + DUR_T), W / 2, H / 2)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
