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
    """Papá como pegatina: borde de papel crema + tinta, la tapa de la cabeza sube con su voz y brinca un poco al hablar.
    (x, yb) = centro de la base de la foto (ponerla bajo el borde inferior para que no se vea el corte recto)."""
    if alfa <= 0.01 or alto < 12:
        return
    a = abre(t) if habla else 0.0
    spr = _jefe().cuadro(a, t, alto=int(alto))
    if abs(rot) > 0.002:
        h0, w0 = spr.shape[:2]
        M = cv2.getRotationMatrix2D((w0 / 2, h0), math.degrees(rot), 1.0)
        spr = cv2.warpAffine(spr, M, (w0, h0), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    al = spr[..., 3].astype(np.float32) / 255
    col = spr[..., 2::-1].astype(np.float32) / 255
    pad = int(9 * alto / 420) + 3
    al = np.pad(al, pad)
    col = np.pad(col, ((pad, pad), (pad, pad), (0, 0)))
    kd = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * pad - 3, 2 * pad - 3))
    ko = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * pad + 3, 2 * pad + 3))
    papel_ = cv2.GaussianBlur(cv2.dilate(al, kd), (0, 0), 1.0)
    tinta = cv2.GaussianBlur(cv2.dilate(al, ko), (0, 0), 1.1)
    h, w = al.shape
    brinco = 12 * abs(math.sin(t * 7)) * (alto / 420) if a > 0.15 else 0.0
    X0, Y0 = int(x - w / 2), int(yb - h + pad - brinco)
    x0, y0, x1, y1 = max(0, X0), max(0, Y0), min(W, X0 + w), min(H, Y0 + h)
    if x1 <= x0 or y1 <= y0:
        return
    sx, sy = x0 - X0, y0 - Y0
    sl = (slice(sy, sy + y1 - y0), slice(sx, sx + x1 - x0))
    R = im[y0:y1, x0:x1]
    # sombra suave de la pegatina
    sh = cv2.GaussianBlur(tinta, (0, 0), 8)
    so = np.zeros_like(sh)
    so[10:, 10:] = sh[:-10, :-10]
    R *= 1 - (so[sl] * 0.25 * alfa)[..., None]
    for capa, c in ((tinta, TINTA), (papel_, CREMA)):
        m = (capa[sl] * alfa)[..., None]
        R *= 1 - m
        R += m * c
    m = (al[sl] * alfa)[..., None]
    R *= 1 - m
    R += m * (col[sl] * 0.94 + np.array([0.06, 0.04, 0.02], np.float32))


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
    rotulo(im, str(n), x, y + 8 * s, 150 * s * (1.25 - 0.25 * e_out(min(1, k * 3))), TINTA, t, seed=seed + 2 + n)


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
