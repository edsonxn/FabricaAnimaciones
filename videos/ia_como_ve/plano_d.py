# -*- coding: utf-8 -*-
"""NEURONA ARTIFICIAL Y FILTROS: el farolito con tres cables (números → perillas → Σ → nivel → se enciende) → la neurona que
mira 3×3 píxeles con perillas «claro | oscuro» → sobre un borde vertical se enciende → la lupa barre la foto del gato y deja
el mapa de bordes (convolución REAL con cv2.filter2D) → cuatro filtros (vertical, acostado, diagonal, color) → LeCun (retrato
real) 1989: dígitos de un código postal y un cheque."""
import math

import cv2
import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb,
                      rotulo, rrect, suave, terminar)
from comun import FIN, INI, T0, T1, cache, desborde, ww
from fondos_ia import papel
from personajes import AMARILLO, BLANCO, OJO_K, destello, kuri
from personajes_ia import camafeo, foto_gato, pegar, retrato

E = "neurona"
T_INI = T0(E)
tNacio, tSimple = ww(E, 0, "nacio"), ww(E, 0, "simple")
tCalc, tRecibe, tMultip, tPerilla, tImporta, tSuma = (ww(E, 1, "calculadora"), ww(E, 1, "recibe"), ww(E, 1, "multiplica"),
                                                      ww(E, 1, "perilla"), ww(E, 1, "importa"), ww(E, 1, "suma"))
tNivel, tEnciende, tTodo = ww(E, 2, "nivel"), ww(E, 2, "enciende"), ww(E, 2, "todo")
tImagina, tCuadrito, tClaro, tOscuro = ww(E, 3, "imagina"), ww(E, 3, "cuadrito"), ww(E, 3, "claro"), ww(E, 3, "oscuro")
tBorde, tDetector = ww(E, 4, "borde"), ww(E, 4, "detector")
tPasas, tLupa, tMapa = ww(E, 5, "pasas"), ww(E, 5, "lupa"), ww(E, 5, "mapa")
tFiltro, tAcost, tDiag, tColor = ww(E, 6, "filtro"), ww(E, 6, "acostados"), ww(E, 6, "diagonales"), ww(E, 6, "color")
tIdea, tLeCun, tEscritos, tCheques = ww(E, 7, "idea"), ww(E, 7, "hizo") - 0.6, ww(E, 7, "escritos"), ww(E, 7, "cheques")
T_FIN = T1(E)
AMBAR = rgb("ffcf6a")


# ------------------------------------------------------------ la neurona: farolito con perillas
def farol(im, x, y, s, t, luz, seed=9000):
    brillo(im, x, y, 160 * s, AMBAR, 0.7 * luz)
    forma(im, elipse(x, y, 90 * s, 90 * s), rgb("f4ead0") * (1 - 0.15 * (1 - luz)) + AMBAR * 0.2 * luz, t, seed, tinta=5,
          luz=(BLANCO, -18, 20, 0.35))
    forma(im, rrect(x, y + 104 * s, 80 * s, 34 * s, 8), rgb("8d8f96"), t, seed + 1, tinta=4)
    for k in range(3):
        linea(im, curva([(x - 26 * s, y + 20 * s), (x - 10 * s, y - 24 * s + 10 * k * s), (x + 10 * s, y + 20 * s)], 4), 3, col=rgb("8a5a34"),
              seed=seed + 2 + k, t=t)
    if luz > 0.5:
        for k in range(8):
            a = k / 8 * 2 * math.pi + t * 0.5
            linea(im, [(x + 110 * s * math.cos(a), y + 110 * s * math.sin(a)), (x + 150 * s * math.cos(a), y + 150 * s * math.sin(a))],
                  6, col=AMBAR, seed=seed + 10 + k, t=t, alfa=luz)


def perilla(im, x, y, r, t, valor, seed=9100, col=None, etiqueta=None):
    """Perilla (dial) con aguja: valor −1..1."""
    col = col if col is not None else rgb("e8b53e")
    forma(im, elipse(x, y, r, r), col, t, seed, tinta=4, luz=(BLANCO, -8, 10, 0.3))
    a = -math.pi / 2 + valor * 2.2
    linea(im, [(x, y), (x + 0.8 * r * math.cos(a), y + 0.8 * r * math.sin(a))], 6, seed=seed + 1, t=t)
    for k in range(7):
        b = -math.pi / 2 + (k / 3 - 1) * 2.2
        linea(im, [(x + 1.05 * r * math.cos(b), y + 1.05 * r * math.sin(b)), (x + 1.2 * r * math.cos(b), y + 1.2 * r * math.sin(b))],
              2.4, seed=seed + 2 + k, t=t, punta=False)
    if etiqueta:
        rotulo(im, etiqueta, x, y + r + 34, 34, TINTA, t, seed=seed + 9, tinta=False)


def calculadora(t):
    im = papel("calido")
    rotulo(im, "NEURONA ARTIFICIAL", W / 2, 110, 84, rgb("3f78c8"), t, seed=9200, esc=e_back(pr(t, tNacio - 0.1, tNacio + 0.2)))
    sale = pr(t, tRecibe - 0.5, tRecibe)
    if sale < 1:
        kuri(im, lerp(420, -250, e_in(sale)), 600 + 16 * math.sin(t * 1.7), 2.1, t, cara="feliz" if t > tSimple else "normal",
             brazos=(0.5, 1.6 if t > tSimple else 0.5))
        if t > tSimple - 0.1:
            rotulo(im, "MÁS SIMPLE DE LO QUE PARECE", W / 2, 960, 58, rgb("b8443a"), t, seed=9201,
                   esc=e_back(pr(t, tSimple - 0.1, tSimple + 0.2)), alfa=1 - sale)
        ec = e_back(pr(t, tCalc - 0.15, tCalc + 0.2)) * (1 - sale)
        if ec > 0.02:                                          # la calculadora diminuta… vista con lupa
            cx, cy = 900, 560
            forma(im, rrect(cx, cy, 58 * ec, 80 * ec, 8), rgb("7d8aa0"), t, 9202, tinta=2.5)
            forma(im, elipse(cx + 150, cy - 30, 200 * ec, 200 * ec), rgb("eef8fa"), t, 9203, tinta=6, alfa=0.9)
            linea(im, [(cx + 150 + 140 * ec, cy - 30 + 140 * ec), (cx + 150 + 230 * ec, cy - 30 + 230 * ec)], 26, col=rgb("7a4a2a"),
                  seed=9204, t=t)
            forma(im, rrect(cx + 150, cy - 20, 190 * ec, 260 * ec, 18), rgb("7d8aa0"), t, 9205, tinta=4)
            forma(im, rrect(cx + 150, cy - 110 * ec, 150 * ec, 50 * ec, 8), rgb("cfe8c8"), t, 9206, tinta=3)
            rotulo(im, "0.84", cx + 150 + 30 * ec, cy - 110 * ec, int(34 * ec) + 2, TINTA, t, seed=9207, tinta=False)
            for j in range(3):
                for i in range(3):
                    forma(im, rrect(cx + 150 + (i - 1) * 50 * ec, cy - 30 * ec + j * 50 * ec, 36 * ec, 34 * ec, 6),
                          rgb(["f4ead0", "f4ead0", "e8b53e"][i]), t, 9210 + i + 3 * j, tinta=2.4)
            rotulo(im, "CALCULADORA DIMINUTA", cx + 150, cy + 220, 40, TINTA, t, seed=9208, tinta=False, esc=ec)
    ent = [(0.8, 0.9), (0.3, -0.6), (0.6, 0.5)]           # (número de entrada, perilla)
    fx, fy = 1340, 540
    total = sum(a * b for a, b in ent)
    for k, (v, w) in enumerate(ent):
        y = 330 + 210 * k
        e = e_back(pr(t, tRecibe + 0.2 * k, tRecibe + 0.2 * k + 0.3))
        if e <= 0.02:
            continue
        linea(im, curva([(240, y), (700, y), (1000, lerp(y, fy, 0.6)), (fx - 90, fy)], 8), 6, col=rgb("8a5a34"), seed=9210 + k,
              t=t, punta=False)
        forma(im, rrect(260, y, 140 * e, 90 * e, 18), BLANCO, t, 9220 + k, tinta=4)
        rotulo(im, f"{v:.1f}", 260, y, int(52 * e) + 2, TINTA, t, seed=9225 + k, tinta=False)
        if t > tMultip - 0.1:
            ep = e_back(pr(t, tMultip - 0.1 + 0.15 * k, tMultip + 0.2 + 0.15 * k))
            wv = w * suave(pr(t, tPerilla, tImporta + 0.3)) if t > tPerilla else 0
            perilla(im, 620, y, 54 * ep, t, wv, seed=9230 + 10 * k)
            if t > tImporta:
                rotulo(im, f"×{w:+.1f}", 760, y, 44, rgb("b8443a"), t, seed=9260 + k, esc=e_back(pr(t, tImporta, tImporta + 0.2)))
        # bolitas de valor que viajan por el cable
        if t > tSuma - 0.3:
            ph = ((t - tSuma) * 0.8 + k * 0.3) % 1
            px = lerp(820, fx - 120, ph)
            py = lerp(y, fy, ph ** 1.6)
            forma(im, elipse(px, py, 14, 14), AMBAR, t, 9270 + k, tinta=2.4)
    if t > tSuma - 0.1:
        e = e_back(pr(t, tSuma - 0.1, tSuma + 0.2))
        forma(im, elipse(1080, fy, 70 * e, 70 * e), rgb("cfe8ea"), t, 9280, tinta=4)
        rotulo(im, "Σ", 1080, fy - 6, int(70 * e) + 2, TINTA, t, seed=9281, tinta=False)
        rotulo(im, f"= {total:.2f}", 1080, fy + 110, 46, TINTA, t, seed=9282, esc=e, tinta=False)
    # nivel (termómetro) y el farol que se enciende
    luz = suave(pr(t, tEnciende - 0.1, tEnciende + 0.25))
    if t > tNivel - 0.2:
        e = e_back(pr(t, tNivel - 0.2, tNivel + 0.1))
        bx, by0, by1 = 1640, 820, 300
        forma(im, rrect(bx, (by0 + by1) / 2, 60 * e, by0 - by1, 26), BLANCO, t, 9290, tinta=4)
        lleno = lerp(by0, by0 - (by0 - by1) * min(1, total / 1.2), suave(pr(t, tNivel, tEnciende)))
        forma(im, rrect(bx, (by0 + lleno) / 2, 40 * e, max(4, by0 - lleno), 18), rgb("e35d4a"), t, 9291, tinta=0)
        umbral = by0 - (by0 - by1) * (0.8 / 1.2)
        linea(im, [(bx - 60, umbral), (bx + 60, umbral)], 5, col=rgb("3f78c8"), seed=9292, t=t, punta=False)
        rotulo(im, "NIVEL", bx + 120, umbral, 34, rgb("3f78c8"), t, seed=9293, tinta=False, esc=e)
    farol(im, fx, fy, 1.2, t, luz)
    if t > tTodo - 0.2:
        rotulo(im, "¡ESO ES TODO!", fx, 900, 60, AMARILLO, t, seed=9295, esc=e_back(pr(t, tTodo - 0.2, tTodo + 0.1)), rot=-0.04)
    return im


# ------------------------------------------------------------ 3×3 sobre un borde
K_V = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], np.float32)


def tres_por_tres(t):
    im = papel("frio")
    # un pedacito de imagen: claro a la izquierda, oscuro a la derecha (borde vertical) — antes, uniforme
    borde = suave(pr(t, tBorde - 0.4, tBorde))
    vals = np.array([[0.85, lerp(0.85, 0.5, borde), lerp(0.85, 0.15, borde)]] * 3, np.float32)
    gx, gy, c = 470, 560, 130
    va = suave(pr(t, tCuadrito - 0.3, tCuadrito + 0.5))          # la foto se va a la esquina y deja el cuadrito
    fe = e_back(pr(t, tImagina - 0.2, tImagina + 0.2))
    fxp, fyp, fs = lerp(W / 2, 200, va), lerp(560, 860, va), lerp(1.2, 0.42, va) * fe
    if fs > 0.02:
        pegar(im, foto_gato(t), fxp, fyp, fs, -0.03 * va, t=t, seed=9301, marco=14)
        qx, qy = fxp + 70 * fs, fyp - 95 * fs
        parp = 0.6 + 0.4 * math.sin(t * 8)
        linea(im, rrect(qx, qy, 46 * fs, 46 * fs, 3), 5, col=AMARILLO, seed=9302, t=t, cerrado=True, punta=False, alfa=parp)
        if va > 0.6:
            linea(im, curva([(qx + 20, qy - 20), (300, 560), (gx - 1.6 * c, gy)], 6), 4, col=AMARILLO, seed=9303, t=t, alfa=0.7,
                  punta=False)
    if t < tCuadrito + 0.2 and fe > 0.5:
        rotulo(im, "SOLO UN CUADRITO", W / 2, 150, 60, rgb("b98a24"), t, seed=9304, esc=e_back(pr(t, tImagina + 0.5, tImagina + 0.8)))
    rotulo(im, "3 × 3 PÍXELES", gx, 300, 50, TINTA, t, seed=9300, tinta=False, esc=e_back(pr(t, tCuadrito - 0.1, tCuadrito + 0.2)))
    for j in range(3):
        for i in range(3):
            e = e_back(pr(t, tCuadrito - 0.1 + 0.04 * (i + 3 * j), tCuadrito + 0.2 + 0.04 * (i + 3 * j)))
            v = vals[j, i]
            forma(im, rrect(gx + (i - 1) * c, gy + (j - 1) * c, c * 0.94 * e, c * 0.94 * e, 8), np.array([v, v, v * 0.97]), t,
                  9310 + i + 3 * j, tinta=3.4)
    # las perillas acomodadas: + | 0 | −
    px0 = 1060
    for j in range(3):
        for i in range(3):
            e = e_back(pr(t, tClaro - 0.2 + 0.05 * i, tClaro + 0.1 + 0.05 * i)) if i < 2 else e_back(pr(t, tOscuro - 0.2, tOscuro + 0.1))
            perilla(im, px0 + (i - 1) * c, gy + (j - 1) * c, 46 * e, t, [0.9, 0.0, -0.9][i], seed=9330 + 10 * (i + 3 * j),
                    col=rgb(["f6e7b0", "d9d4c8", "6d6a74"][i]))
    rotulo(im, "CLARO", px0 - c, 300, 40, rgb("b98a24"), t, seed=9390, esc=e_back(pr(t, tClaro - 0.1, tClaro + 0.2)))
    rotulo(im, "OSCURO", px0 + c, 300, 40, rgb("4a4a5a"), t, seed=9391, esc=e_back(pr(t, tOscuro - 0.1, tOscuro + 0.2)))
    luz = float(clamp((vals * K_V).sum() / 2.0))
    farol(im, 1630, 560, 0.85, t, luz if t > tBorde - 0.1 else 0.0, seed=9400)
    if t > tDetector - 0.1:
        rotulo(im, "DETECTOR DE BORDES", W / 2, 960, 70, rgb("3f78c8"), t, seed=9410, esc=e_back(pr(t, tDetector - 0.1, tDetector + 0.2)))
    return im


# ------------------------------------------------------------ la lupa que barre y los mapas (convolución real)
def _gris():
    return cache("gris_gato", lambda: cv2.cvtColor(np.clip(foto_gato(0.0), 0, 1).astype(np.float32), cv2.COLOR_RGB2GRAY))


def _mapa(nombre):
    def f():
        g = _gris()
        k = {"vertical": K_V, "acostado": K_V.T, "diagonal": np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]], np.float32)}
        if nombre == "color":
            hsv = cv2.cvtColor(np.clip(foto_gato(0.0), 0, 1).astype(np.float32), cv2.COLOR_RGB2HSV)
            r = np.abs(cv2.Sobel(hsv[..., 1], cv2.CV_32F, 1, 0, ksize=3)) + np.abs(cv2.Sobel(hsv[..., 1], cv2.CV_32F, 0, 1, ksize=3))
        else:
            r = np.abs(cv2.filter2D(g, cv2.CV_32F, k[nombre]))
        r = np.clip(r / (np.percentile(r, 99) + 1e-6), 0, 1)
        col = {"vertical": rgb("ffcf6a"), "acostado": rgb("7fd3e8"), "diagonal": rgb("f08a9a"), "color": rgb("9be07a")}[nombre]
        fondo = rgb("1b2633")
        return fondo * (1 - r[..., None]) + col * r[..., None]
    return cache(("mapa", nombre), f)


def barrido(t):
    im = papel("frio")
    foto = np.clip(foto_gato(t), 0, 1)
    fw, fh = 560, 420
    lx, ly, rx_ = 520, 560, 1400                               # centros de la foto y del mapa
    pegar(im, foto, lx, ly, 1.25, 0, t=t, seed=9500, marco=0)
    mapa = _mapa("vertical")
    u = pr(t, tPasas, tMapa + 0.8)                              # progreso del barrido (fila a fila)
    filas = 12
    pos = u * filas
    fila, fr = int(min(pos, filas - 1e-6)), pos % 1
    revel = np.zeros((fh, fw), np.float32)
    revel[:int(fila * fh / filas)] = 1
    revel[int(fila * fh / filas):int((fila + 1) * fh / filas), :int(fr * fw)] = 1
    if u >= 1:
        revel[:] = 1
    vis = np.clip(papel_rect := np.full((fh, fw, 3), rgb("1b2633"), np.float32), 0, 1)
    vis = vis * (1 - revel[..., None]) + mapa * revel[..., None]
    pegar(im, vis, rx_, ly, 1.25, 0, t=t, seed=9510, marco=0)
    if t > tPasas - 0.1 and u < 1:
        mx = lx - fw * 1.25 / 2 + fr * fw * 1.25
        my = ly - fh * 1.25 / 2 + (fila + 0.5) * fh * 1.25 / filas
        forma(im, elipse(mx, my, 60, 60), rgb("dff3f6"), t, 9520, tinta=6, alfa=0.45)
        linea(im, [(mx + 42, my + 42), (mx + 100, my + 100)], 20, col=rgb("7a4a2a"), seed=9521, t=t)
        nx = rx_ - fw * 1.25 / 2 + fr * fw * 1.25
        brillo(im, nx, my, 40, AMBAR, 0.8)
        linea(im, curva([(mx, my - 60), ((mx + nx) / 2, my - 200), (nx, my - 30)], 8), 3, col=AMBAR, seed=9522, t=t, alfa=0.7,
              punta=False)
    if t > tLupa - 0.1:
        rotulo(im, "FILTRO", lx, 140, 72, rgb("3f78c8"), t, seed=9530, esc=e_back(pr(t, tLupa - 0.1, tLupa + 0.2)))
    if t > tMapa - 0.1:
        rotulo(im, "MAPA DE BORDES", rx_, 140, 66, AMBAR, t, seed=9531, esc=e_back(pr(t, tMapa - 0.1, tMapa + 0.2)))
    return im


def cuatro_filtros(t):
    im = papel("noche")
    for k, (nom, ti, lbl) in enumerate((("vertical", tFiltro, "VERTICALES"), ("acostado", tAcost, "ACOSTADOS"),
                                        ("diagonal", tDiag, "DIAGONALES"), ("color", tColor, "COLOR"))):
        e = e_back(pr(t, ti - 0.15, ti + 0.2))
        x, y = 520 + 880 * (k % 2), 330 + 440 * (k // 2)
        if e > 0.02:
            pegar(im, _mapa(nom), x, y, 0.82 * e, 0.02 * (k - 1.5), t=t, seed=9600 + 10 * k, marco=12, marco_col=rgb("2b3648"))
            rotulo(im, lbl, x, y + 210 * e, 44, rgb("fbf3df"), t, seed=9640 + k, esc=e)
    return im


def lecun(t):
    im = papel("calido")
    e = e_back(pr(t, tLeCun - 0.1, tLeCun + 0.3))
    camafeo(im, retrato("lecun", 240, 300), 330, 420, 1.0 * e, t, nombre="YANN LECUN", seed=9700)
    rotulo(im, "1989", 330, 110, 80, rgb("b8443a"), t, seed=9710, esc=e_back(pr(t, tIdea, tIdea + 0.3)))
    ei = e_back(pr(t, tIdea - 0.2, tIdea + 0.3)) * (1 - pr(t, tEscritos - 0.6, tEscritos - 0.2))
    if ei > 0.02:
        for k, nom in enumerate(("vertical", "acostado", "diagonal", "color")):
            pegar(im, _mapa(nom), 1000 + 120 * k, 420 + 70 * k, 0.55 * ei, 0.04 * (k - 1.5), t=t, seed=9690 + k, marco=10,
                  marco_col=rgb("2b3648"))
        rotulo(im, "RED DE FILTROS", 1180, 880, 58, rgb("3f78c8"), t, seed=9699, esc=ei)
    # sobre con el código postal escrito a mano y la red que lo lee
    ex = e_back(pr(t, tEscritos - 0.3, tEscritos))
    forma(im, rrect(1030, 340, 560 * ex, 300 * ex, 10, -0.03), rgb("f3e9cf"), t, 9720, tinta=4)
    if ex > 0.5:
        for k, d in enumerate("90210"):
            rotulo(im, d, 860 + k * 85, 400, 80, rgb("2b3f8a"), t, seed=9730 + k, fuente="segoesc.ttf", tinta=False)
            if t > tEscritos + 0.3 + 0.12 * k:
                forma(im, rrect(860 + k * 85, 400, 74, 96, 10), rgb("9be07a"), t, 9740 + k, tinta=3, alfa=0.25)
                rotulo(im, d, 860 + k * 85, 300, 40, rgb("2e8b4a"), t, seed=9750 + k, tinta=False)
        forma(im, rrect(1200, 270, 120, 80, 4), rgb("e35d4a"), t, 9760, tinta=3)
    # el cheque
    if t > tCheques - 0.3:
        ec = e_back(pr(t, tCheques - 0.3, tCheques))
        forma(im, rrect(1250, 800, 900 * ec, 320 * ec, 14, 0.03), rgb("d9efe0"), t, 9770, tinta=4.5)
        if ec > 0.5:
            rotulo(im, "BANCO", 900, 690, 40, rgb("2e6b4a"), t, seed=9771, tinta=False)
            rotulo(im, "$ 1 250.00", 1500, 760, 60, rgb("2b3f8a"), t, seed=9772, fuente="segoesc.ttf", tinta=False)
            linea(im, curva([(950, 880), (1050, 850), (1150, 900), (1260, 860)], 8), 4, col=rgb("2b3f8a"), seed=9773, t=t)
            destello(im, 1690, 680, 0.8 * pr(t, tCheques + 0.3, tCheques + 0.6), t, seed=1036)
            rotulo(im, "✓ LEÍDO", 1560, 900, 50, rgb("2e8b4a"), t, seed=9774, esc=e_back(pr(t, tCheques + 0.3, tCheques + 0.6)),
                   fuente="seguisym.ttf")
    return im


TRAMOS = [(calculadora, T_INI), (tres_por_tres, tImagina - 0.4), (barrido, tPasas - 0.5), (cuatro_filtros, tFiltro - 0.3),
          (lecun, tIdea - 0.4)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.25 + 0.12 * k), H * 0.5)
        else:
            import plano_c
            im = desborde(plano_c.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
