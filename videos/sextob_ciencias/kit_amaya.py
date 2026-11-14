# -*- coding: utf-8 -*-
"""Kit propio del video de Amaya: papá (foto real recortada que abre la cabeza con su voz, como pegatina con borde de papel),
retratos reales en camafeo, tarjetas, fechas de calendario, botón de PAUSA con cuenta regresiva y caras para personitas."""
import math
import os

import cv2
import numpy as np

from acuarela import (H, W, TINTA, curva, e_back, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave)
from comun import TL, cache
import personajes_ia as PI

AQUI = os.path.dirname(os.path.abspath(__file__))

PI.RECORTES.update({
    "hidalgo": (0.263, 0.112, 0.737, 0.593), "morelos": (0.166, 0.034, 0.871, 0.694), "allende": (0.19, 0.028, 1.0, 0.85),
    "aldama": (0.158, 0.042, 0.788, 0.633), "josefa": (0.0, 0.0, 0.99, 0.921), "leona": (0.0, 0.0, 0.923, 0.958),
    "iturbide": (0.015, 0.093, 0.836, 0.885), "napoleon": (0.224, 0.044, 0.807, 0.59), "guerrero": (0.247, 0.106, 0.705, 0.567),
    "victoria": (0.343, 0.014, 0.689, 0.247), "fernando": (0.14, 0.195, 0.83, 0.899), "odonoju": (0.244, 0.082, 0.695, 0.525)})

VERDE = rgb("3f8f5a")
ROJO = rgb("c8473f")
CREMA = rgb("fbf3df")
DORADO = rgb("d9a93e")
AZUL = rgb("3f78c8")
MORADO = rgb("8a5ab8")
CAFE = rgb("8a5a34")
GRIS = rgb("8f8f96")


def foto(n, w=300, h=380):
    return PI.retrato(n, w, h)


def cam(im, n, x, y, esc, t, nombre="", seed=0, alfa=1.0, rot=0.0, col=None):
    """Retrato real en marco ovalado con cartela (nada si esc ≈ 0)."""
    if esc > 0.02 and alfa > 0.01:
        PI.camafeo(im, foto(n), x, y, esc, t, nombre, seed=5200 + seed * 7, alfa=alfa, rot=rot, col=col)


def entra(t, t0, d=0.35):
    """0 → 1 con rebote desde t0."""
    return e_back(pr(t, t0, t0 + d))


# ------------------------------------------------------------ papá: foto real que habla con su voz
FPS_A = 24


def _amp():
    from jefe_canadiense import amplitud
    tot = int(TL["total"] * FPS_A) + 4
    out = np.zeros(tot)
    for e in TL["escenas"]:
        for f in e["frases"]:
            p = os.path.join(AQUI, "voz", "final", f"{f['key']}.wav")
            if os.path.exists(p):
                a = amplitud(p, fps=FPS_A)
                i0 = int(round(f["t0"] * FPS_A))
                n = max(0, min(len(a), tot - i0))
                out[i0:i0 + n] = np.maximum(out[i0:i0 + n], a[:n])
    return out


def abre(t):
    a = cache("amp", _amp)
    i = int(t * FPS_A)
    return float(a[i]) if 0 <= i < len(a) else 0.0


_J = {}


def _jefe():
    if "j" not in _J:
        from jefe_canadiense import Jefe

        class Papa(Jefe):
            """Como Jefe, pero el hueco de la boca llega hasta el borde de la cara y se recorta con la silueta original:
            sin muesca ni pico de color fuera de la mejilla."""
            def _lienzo(self, abre):
                w, h, by, hx = self.w, self.h, self.by, self.hx
                m = int(h * .42)
                L = np.zeros((h + m, w, 4), np.float32)
                y0 = by + m
                L[y0:] = self.im[by:]
                sil = np.zeros(L.shape[:2], np.float32)
                sil[m:m + h] = self.im[..., 3] / 255
                sil = cv2.dilate(sil, np.ones((5, 5), np.uint8))
                a = -self.ang * float(np.clip(abre, 0, 1))
                rad = np.deg2rad(-a)
                fx = int(.66 * w)
                tope = (fx, int(y0 - np.sin(rad) * (fx - hx)) - 5)
                interior = np.zeros(L.shape[:2], np.uint8)
                cv2.fillPoly(interior, [np.array([(hx, y0), (fx, y0 + 2), tope], np.int32)], 255, cv2.LINE_AA)
                interior = cv2.GaussianBlur(interior, (0, 0), 1.2).astype(np.float32) / 255 * sil
                for c, v in enumerate((16, 12, 58)):
                    L[..., c] = L[..., c] * (1 - interior) + v * interior
                L[..., 3] = np.maximum(L[..., 3], interior * 255)
                arriba = np.zeros_like(L)
                arriba[m:y0] = self.im[:by]
                M = cv2.getRotationMatrix2D((float(hx), float(y0)), -a, 1.0)
                arriba = cv2.warpAffine(arriba, M, (L.shape[1], L.shape[0]), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
                al = arriba[..., 3:] / 255
                L[..., :3] = arriba[..., :3] * al + L[..., :3] * (1 - al)
                L[..., 3] = arriba[..., 3] + L[..., 3] * (1 - al[..., 0])
                return L

        _J["j"] = Papa(os.path.join(AQUI, "propios", "jefe_limpio.png"), boca_y=.523 / .75, bisagra_x=.33, frente_x=.6, corte=.75, angulo=19)
    return _J["j"]


def papa(im, t, x, yb, alto=420, alfa=1.0, habla=True, rot=0.0):
    """(7-nov) YA NO es la foto del usuario: dibuja a EL PROFE TILDE, presentador chibi en acuarela inventado para este video
    (HOMBRE, porque la voz es de hombre: pelo corto con copete, bigote, lentes rojos redondos, lápiz en la oreja, chaleco verde
    con camisa blanca y corbata roja con una tilde). La boca se abre
    con la voz del narrador (abre(t)), parpadea y cabecea al hablar. Misma firma que antes para no tocar los planos:
    (x, yb) = centro de la base (se pone bajo el borde inferior), alto = altura total del busto."""
    if alfa <= 0.01 or alto < 12:
        return
    a = abre(t) if habla else 0.0
    s = alto / 360.0
    bob = (6 * abs(math.sin(t * 6.5)) if a > 0.15 else 2 * math.sin(t * 1.7)) * s
    r = 112 * s                                     # radio de la cabeza (cabezona)
    cx, cy = x + 4 * s * math.sin(t * 1.3), yb - 290 * s - bob
    PIEL_T, PELO_T, SUET, CUELLO = rgb("e9bb94"), rgb("2f241f"), rgb("f6f5ef"), rgb("a9cbe6")   # 9-nov: BATA blanca de científico sobre camisa azul
    # cuerpo (busto): camisa blanca, chaleco verde abierto en V, corbata roja + brazo con el puntero
    forma(im, elipse(x, yb - 40 * s, 175 * s, 170 * s), CUELLO, t, 19000, tinta=4.5 * s, alfa=alfa)
    for d in (-1, 1):
        forma(im, np.array([(x + d * 30 * s, yb - 175 * s), (x + d * 175 * s, yb - 60 * s), (x + d * 170 * s, yb + 80 * s),
                            (x + d * 20 * s, yb + 80 * s), (x + d * 20 * s, yb - 60 * s)], np.float32), SUET, t, 19001 + d,
              tinta=4 * s, alfa=alfa)
    forma(im, np.array([(x - 18 * s, yb - 178 * s), (x + 18 * s, yb - 178 * s), (x + 10 * s, yb - 150 * s), (x + 26 * s, yb - 40 * s),
                        (x, yb - 10 * s), (x - 26 * s, yb - 40 * s), (x - 10 * s, yb - 150 * s)], np.float32), ROJO, t, 19004,
          tinta=3 * s, alfa=alfa)
    linea(im, [(x - 8 * s, yb - 95 * s), (x + 10 * s, yb - 112 * s)], 5 * s, CREMA, seed=19005, t=t, alfa=alfa)
    forma(im, rrect(x + 105 * s, yb - 20 * s, 60 * s, 50 * s, 6 * s), rgb("e4e2da"), t, 19006, tinta=2.5 * s, alfa=alfa)   # bolsillo
    for k, c in enumerate((AZUL, ROJO)):
        linea(im, [(x + (95 + 16 * k) * s, yb - 40 * s), (x + (95 + 16 * k) * s, yb - 75 * s)], 6 * s, c, seed=19007 + k * 50, t=t, alfa=alfa)
    ang = -0.9 + 0.25 * math.sin(t * 2.2) - (0.35 if a > 0.3 else 0.0)
    hx, hy = x - 150 * s, yb - 120 * s
    px, py = hx + 230 * s * math.cos(ang - 1.2), hy + 230 * s * math.sin(ang - 1.2)
    linea(im, [(hx, hy), (px, py)], 7 * s, rgb("8a5a34"), seed=19008, t=t, alfa=alfa)
    forma(im, elipse(px, py, 9 * s, 9 * s), ROJO, t, 19009, tinta=2 * s, alfa=alfa)
    forma(im, elipse(hx, hy, 30 * s, 26 * s), PIEL_T, t, 19010, tinta=3 * s, alfa=alfa)
    # cuello y cabeza
    forma(im, rrect(cx, cy + r * 0.95, 50 * s, 50 * s, 10 * s), PIEL_T, t, 19011, tinta=3 * s, alfa=alfa)
    for d in (-1, 1):                                                                                   # orejas
        forma(im, elipse(cx + d * r * 0.98, cy + r * 0.12, r * 0.16, r * 0.22), PIEL_T, t, 19012 + d, tinta=3 * s, alfa=alfa)
    forma(im, elipse(cx, cy, r * 0.96, r), PIEL_T, t, 19014, tinta=5 * s, alfa=alfa)
    forma(im, np.array([(cx - r * 0.98, cy - r * 0.05), (cx - r * 0.95, cy - r * 0.7), (cx - r * 0.45, cy - r * 1.12),
                        (cx + r * 0.25, cy - r * 1.18), (cx + r * 0.85, cy - r * 0.85), (cx + r * 0.98, cy - r * 0.1),
                        (cx + r * 0.82, cy - r * 0.45), (cx + r * 0.1, cy - r * 0.62), (cx - r * 0.55, cy - r * 0.55),
                        (cx - r * 0.82, cy - r * 0.3)], np.float32), PELO_T, t, 19015, tinta=4 * s, alfa=alfa)      # pelo corto
    linea(im, [(cx + r * 0.95, cy - r * 0.32), (cx + r * 1.25, cy - r * 0.12)], 10 * s, AMAR, seed=19016, t=t, alfa=alfa)  # lápiz
    linea(im, [(cx - r * 0.97, cy - r * 0.5), (cx + r * 0.97, cy - r * 0.5)], 7 * s, rgb("3a3a44"), seed=19040, t=t, alfa=alfa)  # goggles en la frente
    for d in (-1, 1):
        forma(im, elipse(cx + d * r * 0.34, cy - r * 0.55, r * 0.27, r * 0.2), rgb("9fd8e0"), t, 19041 + d, tinta=4.5 * s, alfa=alfa,
              luz=(rgb("ffffff"), -6 * s, -5 * s, 0.6))
    for d in (-1, 1):                                                                                   # cejas
        linea(im, [(cx + d * r * 0.2, cy - r * 0.3), (cx + d * r * 0.52, cy - r * 0.34)], 6 * s, PELO_T, seed=19017 + d, t=t,
              alfa=alfa)
    forma(im, np.array([(cx - r * 0.34, cy + r * 0.36), (cx, cy + r * 0.28), (cx + r * 0.34, cy + r * 0.36), (cx + r * 0.28, cy + r * 0.44),
                        (cx, cy + r * 0.38), (cx - r * 0.28, cy + r * 0.44)], np.float32), PELO_T, t, 19019, tinta=2 * s,
          alfa=alfa)                                                                                     # bigote
    parp = (t % 4.1) < 0.12
    for d in (-1, 1):
        ex, ey = cx + d * r * 0.36, cy + r * 0.02
        if parp:
            linea(im, [(ex - 12 * s, ey), (ex + 12 * s, ey)], 3.5 * s, seed=19022 + d, t=t, alfa=alfa)
        else:
            forma(im, elipse(ex, ey, 9 * s, 12 * s), TINTA, t, 19022 + d, tinta=0, alfa=alfa)
            forma(im, elipse(ex + 3 * s, ey - 4 * s, 3 * s, 3 * s), CREMA, t, 19024 + d, tinta=0, alfa=alfa)
        linea(im, elipse(ex, ey, 30 * s, 26 * s), 4.5 * s, ROJO, seed=19026 + d, t=t, cerrado=True, punta=False, alfa=alfa)  # lentes
    linea(im, [(cx - r * 0.12, cy), (cx + r * 0.12, cy)], 3.5 * s, ROJO, seed=19028, t=t, alfa=alfa)
    # boca: sonrisa cerrada o abierta con la voz
    my = cy + r * 0.58
    if a > 0.08:
        h = r * (0.06 + 0.22 * min(1.0, a))
        forma(im, elipse(cx, my + h * 0.3, r * 0.2, h), rgb("8a3a3a"), t, 19030, tinta=2.5 * s, alfa=alfa)
        forma(im, elipse(cx, my + h * 0.85, r * 0.11, h * 0.35), rgb("e8737a"), t, 19031, tinta=0, alfa=alfa)
    else:
        linea(im, curva([(cx - r * 0.18, my), (cx, my + r * 0.1), (cx + r * 0.18, my)], 6), 4 * s, seed=19032, t=t, punta=False,
              alfa=alfa)


# ------------------------------------------------------------ piezas pintadas
def tarjeta(im, x, y, w, h, t, col=CREMA, seed=0, alfa=1.0, rot=0.0, tinta=4.0):
    if alfa <= 0.01 or w < 4 or h < 4:
        return
    lavado(im, rrect(x + 10, y + 14, w, h, min(26, h / 3), rot), rgb("5a4a3a"), 0.28 * alfa, seed + 1)
    forma(im, rrect(x, y, w, h, min(26, h / 3), rot), col, t, seed, tinta=tinta, alfa=alfa)


def letrero(im, texto, x, y, px, t, col=CREMA, txt=TINTA, seed=0, esc=1.0, rot=0.0, pad=0.55):
    """Tarjeta con texto centrado; ancho según el texto."""
    if esc <= 0.02:
        return
    w = (len(texto) * px * 0.56 + px * 1.4) * esc
    h = px * (1 + 2 * pad * 0.6) * esc
    tarjeta(im, x, y, w, h, t, col, seed, rot=rot)
    rotulo(im, texto, x, y + 3 * esc, px * esc, txt, t, seed=seed + 3, tinta=False, rot=rot)


def fecha(im, x, y, s, t, dia, mes, anio, seed=0, col=ROJO):
    """Hoja de calendario: cabecera de color con el mes, día gigante y año debajo."""
    if s <= 0.02:
        return
    tarjeta(im, x, y, 300 * s, 330 * s, t, CREMA, seed)
    forma(im, rrect(x, y - 115 * s, 300 * s, 90 * s, 22 * s), col, t, seed + 2, tinta=3.5)
    rotulo(im, mes, x, y - 112 * s, 58 * s, CREMA, t, seed=seed + 3, tinta=False)
    rotulo(im, dia, x, y + 18 * s, 150 * s, TINTA, t, seed=seed + 4, tinta=False)
    rotulo(im, anio, x, y + 122 * s, 56 * s, col, t, seed=seed + 5, tinta=False)
    for d in (-1, 1):
        forma(im, elipse(x + d * 80 * s, y - 162 * s, 12 * s, 22 * s), GRIS, t, seed + 6 + d, tinta=2.5)


def pausa(im, x, y, s, t, seed=0, texto=True):
    """Botón de PAUSA rojo que late + «PAUSA Y CONTESTA»."""
    if s <= 0.02:
        return
    late = 1 + 0.05 * math.sin(t * 6)
    r = 110 * s * late
    lavado(im, elipse(x + 12 * s, y + 16 * s, r, r), rgb("5a4a3a"), 0.3, seed + 1)
    forma(im, elipse(x, y, r, r), ROJO, t, seed, tinta=6 * s, luz=(rgb("ffffff"), -30, -30, 0.35))
    for d in (-1, 1):
        forma(im, rrect(x + d * 30 * s * late, y, 30 * s * late, 100 * s * late, 8 * s), CREMA, t, seed + 4 + d, tinta=3 * s)
    if texto:
        rotulo(im, "PAUSA Y CONTESTA", x, y + r + 70 * s, 72 * s, ROJO, t, seed=seed + 8)


def cuenta(im, x, y, t, t0, t1, s=1.0, seed=0):
    """Cuenta regresiva 3-2-1 entre t0 y t1, con un anillo que se va vaciando."""
    if not (t0 <= t < t1):
        return
    u = (t - t0) / (t1 - t0)
    n = 3 - min(2, int(u * 3))
    k = (u * 3) % 1
    forma(im, elipse(x, y, 120 * s, 120 * s), CREMA, t, seed, tinta=5)
    ang = np.linspace(-math.pi / 2, -math.pi / 2 + 2 * math.pi * (1 - u), 60)
    if len(ang) > 1 and u < 0.995:
        linea(im, np.stack([x + 100 * s * np.cos(ang), y + 100 * s * np.sin(ang)], 1), 16 * s, AMAR, seed=seed + 1, t=t, punta=False)
    rotulo(im, str(n), x, y + 8 * s, 150 * s * (1.25 - 0.25 * e_out(min(1, k * 3))), ROJO, t, seed=seed + 2 + n)


AMAR = rgb("f2c14e")


def cara_p(im, x, y, s, t, seed, cara="normal"):
    """Ojos y boca para personita (cabeza de radio 24·s en (x, y))."""
    if s < 0.3:
        return
    dy = 3 * s * math.sin(t * 5 + seed)
    for d in (-1, 1):
        forma(im, elipse(x + d * 8 * s, y + 3 * s + dy, 2.0 * s, 2.8 * s), TINTA, t, 10800 + seed * 3 + d, tinta=0)
        if cara == "enojo":
            linea(im, [(x + d * 4 * s, y - 2 * s + dy), (x + d * 13 * s, y - 5 * s + dy)], 0.9 * s, seed=10820 + seed * 3 + d,
                  t=t, punta=False)
    if cara in ("enojo", "grito"):
        forma(im, elipse(x, y + 13 * s + dy, 5 * s, 4.5 * s if cara == "grito" else 3.5 * s), rgb("8a3a3a"), t, 10840 + seed,
              tinta=0.6 * s)
    elif cara == "susto":
        forma(im, elipse(x, y + 13 * s + dy, 3 * s, 4 * s), rgb("8a3a3a"), t, 10840 + seed, tinta=0.6 * s)
    elif cara == "triste":
        linea(im, curva([(x - 5 * s, y + 14 * s + dy), (x, y + 11 * s + dy), (x + 5 * s, y + 14 * s + dy)], 4), 0.8 * s,
              seed=10840 + seed, t=t, punta=False)
    else:
        linea(im, curva([(x - 5 * s, y + 11 * s + dy), (x, y + 14 * s + dy), (x + 5 * s, y + 11 * s + dy)], 4), 0.8 * s,
              seed=10840 + seed, t=t, punta=False)


def gente(im, x, y, s, t, seed=0, cara="normal", col=None, piel=None):
    from iconos_ia import personita
    personita(im, x, y, s, t, seed=seed, col=col, piel=piel)
    cara_p(im, x, y, s, t, seed, cara)


def flecha_curva(im, pts, t, col=TINTA, ancho=7, seed=0, u=1.0):
    """Flecha pintada a lo largo de una curva; u = cuánto se ha dibujado (0..1)."""
    p = curva(pts, 12)
    n = max(2, int(len(p) * clamp01(u)))
    p = p[:n]
    linea(im, p, ancho, col, seed=seed, t=t)
    if u >= 0.98 and len(p) > 3:
        d = p[-1] - p[-4]
        d = d / (np.hypot(*d) + 1e-6)
        nn = np.array([-d[1], d[0]])
        a = p[-1]
        forma(im, np.array([a + d * 26, a - d * 6 + nn * 18, a - d * 6 - nn * 18], np.float32), col, t, seed + 1, tinta=2)


def clamp01(x):
    return max(0.0, min(1.0, x))


def chispas(im, x, y, r, t, t0, seed=0, n=8, col=None):
    """Destellos que salen en círculo al revelar algo (para respuestas correctas)."""
    from personajes import destello
    u = pr(t, t0, t0 + 0.6)
    if 0 < u < 1:
        for k in range(n):
            a = 2 * math.pi * k / n + seed
            destello(im, x + math.cos(a) * r * (0.6 + 0.6 * u), y + math.sin(a) * r * (0.6 + 0.6 * u), 0.7 * (1 - u) + 0.2, t,
                     seed=seed + k, col=col)
