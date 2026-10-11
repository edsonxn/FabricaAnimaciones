# -*- coding: utf-8 -*-
"""200 000 AÑOS EN 60 SEGUNDOS — PLANO SECUENCIA vertical estilo Kurzgesagt, sin voz.

Las 5 "escenas" del guion son solo las secciones musicales: TODAS usan la clase Mundo, que dibuja la historia como un
único flujo continuo en función del tiempo global t. Cada una de las 19 épocas (epocas1..4.py) se abre como un PORTAL
desde un objeto de la anterior (el Sol, la antorcha, el volante, la bombilla...) o con otra transición procedural
(persianas de puntos, reloj, descenso de cámara, ola diagonal, glitch). La interfaz (contador de años, título de la
época, riel de progreso) se dibuja una sola vez encima de todo, sin cortes."""
import math

import numpy as np

import efectos as E
import epocas1 as E1
import epocas2 as E2
import epocas3 as E3
import epocas4 as E4
import era as ER
import kit as K
import plano as P
from escena_base import TL, Escena
from era import BEAT, D_TR, INICIOS, TABLA, img_era
from motor import (W, H, Lienzo, circulo, clamp01, componer, e_back, e_in, e_inout, e_out, lerp, prog, smooth, rect_red)
from plano import mezcla

PI = math.pi
TOTAL = TL["total"]

ORDEN = [E1.Sapiens, E1.Africa, E1.Arte, E2.Agricultura, E2.Rueda, E2.Escritura, E2.Piramides, E2.Grecia, E2.Roma,
         E3.Imprenta, E3.Oceano, E3.Telescopio, E3.Vapor, E4.Luz, E4.Vuelo, E4.Luna, E4.Web, E4.Smartphone, E4.Hoy]
ERAS = [c(k) for k, c in enumerate(ORDEN)]
assert [e.id for e in ERAS] == [x[0] for x in TABLA]
NE = len(ERAS)

# tipo de transición de la época k a la k+1
TRANS = ["portal", "portal", "portal", "puntos", "reloj", "bajada", "portal", "ola", "portal", "puntos", "portal",
         "portal", "reloj", "portal", "subida", "glitch", "pixeles", "portal"]
assert len(TRANS) == NE - 1

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


# ======================================================================== transiciones (imágenes A, B float32 HxWx3)
def _mezcla(A, B, m):
    return A + (B - A) * m[..., None]


def _col(c):
    return np.array(c, np.float32) / 255.0


def tr_portal(A, B, p, cx, cy, col):
    dist = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    rmax = max(math.hypot(cx, cy), math.hypot(W - cx, cy), math.hypot(cx, H - cy), math.hypot(W - cx, H - cy)) + 60
    R = e_inout(p) * rmax
    m = np.clip((R - dist) / 2.5 + 0.5, 0, 1)
    out = _mezcla(A, B, m)
    a = min(1.0, math.sin(PI * p) * 1.8)
    w = 12 + 30 * math.sin(PI * p)
    d = np.abs(dist - R)
    ring = np.clip(1 - d / w, 0, 1) ** 1.4 * a
    glow = np.clip(1 - d / (w * 6), 0, 1) ** 2 * a * 0.30
    c = _col(col)
    out = out * (1 - ring[..., None] * 0.92) + c * ring[..., None] * 0.92 + c * glow[..., None]
    sombra = np.clip(1 - (dist - R) / 200.0, 0, 1) * (dist > R) * a * 0.32
    return out * (1 - sombra[..., None])


def tr_bajada(A, B, p, sentido=1):
    s = int(round(e_inout(p) * H))
    out = np.empty_like(A)
    if s <= 0:
        return A
    if s >= H:
        return B
    if sentido > 0:                      # la cámara baja: A sale por arriba, B entra por abajo
        out[:H - s] = A[s:]
        out[H - s:] = B[:s]
        lin = H - s
    else:                                # la cámara sube: A sale por abajo, B entra por arriba
        out[s:] = A[:H - s]
        out[:s] = B[H - s:]
        lin = s
    y0, y1 = max(0, lin - 70), min(H, lin + 70)
    if sentido > 0:
        out[y0:lin] *= np.linspace(1.0, 0.65, lin - y0)[:, None, None]
    else:
        out[lin:y1] *= np.linspace(0.65, 1.0, y1 - lin)[:, None, None]
    return out


def tr_reloj(A, B, p, cx, cy, col):
    ang = np.arctan2(XX - cx, -(YY - cy))
    ang = np.where(ang < 0, ang + 2 * PI, ang)
    th = e_inout(p) * 2 * PI
    m = np.clip((th - ang) / 0.02 + 0.5, 0, 1)
    out = _mezcla(A, B, m)
    dist = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    perp = dist * np.abs(np.sin(ang - th))
    linea = np.clip(1 - perp / 9.0, 0, 1) * (np.cos(ang - th) > 0) * min(1.0, math.sin(PI * p) * 3)
    c = _col(col)
    out = out * (1 - linea[..., None] * 0.9) + c * linea[..., None] * 0.9
    estela = np.clip(1 - (th - ang) / 0.6, 0, 1) * (ang < th) * min(1.0, math.sin(PI * p) * 3) * 0.16
    return out + c * estela[..., None]


def tr_puntos(A, B, p, celda=96.0):
    ix, iy = np.floor(XX / celda), np.floor(YY / celda)
    dx = (XX - (ix + 0.5) * celda)
    dy = (YY - (iy + 0.5) * celda)
    d = np.sqrt(dx * dx + dy * dy)
    fase = (ix * 0.6 + iy * 0.4) / (W / celda * 0.6 + H / celda * 0.4)
    R = np.clip(e_inout(p) * 1.9 - fase * 0.9, 0, 1) * celda * 0.76
    m = np.clip(R - d + 0.5, 0, 1)
    return _mezcla(A, B, m)


def tr_ola(A, B, p, col=(255, 255, 255)):
    u = (XX * 0.5 + YY * 0.866) / (W * 0.5 + H * 0.866)
    borde = e_inout(p) * 1.5 - 0.25
    onda = 0.07 * np.sin(YY / 90.0 + p * 7) + 0.05 * np.sin(XX / 60.0 - p * 5)
    v = borde - u + onda
    m = np.clip(v / 0.006 + 0.5, 0, 1)
    out = _mezcla(A, B, m)
    band = np.clip(1 - np.abs(v) / 0.035, 0, 1) * min(1.0, math.sin(PI * p) * 3) * 0.8
    c = _col(col)
    return out * (1 - band[..., None]) + c * band[..., None]


# ======================================================================== interfaz
def era_en(t):
    for k in range(NE - 1, -1, -1):
        if t >= INICIOS[k]:
            return k
    return 0


def anios_atras(t):
    k = era_en(t)
    a = float(TABLA[k][2])
    if k + 1 < NE:
        t0, t1 = INICIOS[k + 1] - D_TR, INICIOS[k + 1] - 0.05
        if t > t0:
            u = e_inout(prog(t, t0, t1))
            b = float(TABLA[k + 1][2])
            a = math.exp(lerp(math.log(max(a, 1.0)), math.log(max(b, 1.0)), u)) if (a > 0 or b > 0) else 0.0
            if u >= 1.0:
                a = b
    return a


def formato_anio(ya):
    """(texto grande, etiqueta) para 'años atrás' -> calendario."""
    if ya >= 12000:
        v = ya
        mag = 10 ** (int(math.log10(v)) - 1)
        v = int(round(v / mag) * mag)
        return f"{v:,}".replace(",", " "), "AÑOS ATRÁS"
    anio = int(round(2025 - ya))
    if anio <= 0:
        return f"{-anio + (0 if anio != 0 else 1):d}", "A. C."
    return str(anio), ("D. C." if anio < 1000 else "")


def ui(lz, t):
    k = era_en(t)
    en_tr = k + 1 < NE and t > INICIOS[k + 1] - D_TR
    # contador de años (arriba, siempre visible)
    txt, etq = formato_anio(anios_atras(t))
    lz.halo(W / 2, 290, 560, (8, 8, 44), alfa=0.6, dureza=1.1, capa=2)
    esc = 1.0 + (0.05 * math.sin(t * 40) if en_tr else 0.0)
    P.rotulo(lz, W / 2, 262, txt, 128, k=esc, fuente="geo_x", capa=2, sombra=0.55)
    if etq:
        P.rotulo(lz, W / 2, 352, etq, 38, fuente="geo", color=(214, 222, 255), capa=2)
    # título de la época (abajo)
    for j in (k, k + 1):
        if j >= NE - 1 and j == NE - 1:
            continue                       # la última época dibuja sus propios textos
        if j >= NE:
            continue
        e = ERAS[j]
        ta = e.T0 - 0.05
        tb = e.T1 - D_TR + 0.10
        if not (ta - 0.02 <= t <= tb + 0.3):
            continue
        ka = e_back(prog(t, ta, ta + 0.32), 1.7)
        kb = 1 - e_in(prog(t, tb, tb + 0.2))
        a = min(1.0, ka) * kb
        if a <= 0.01:
            continue
        dy = 26 * (1 - clamp01(ka))
        lz.halo(W / 2, 1490, 700, (8, 8, 44), alfa=0.62 * a, dureza=1.0, capa=2)
        P.rotulo(lz, W / 2, 1462 + dy, e.titulo, 62 if len(e.titulo) < 22 else 52, k=0.9 + 0.1 * ka, fuente="geo_x", alfa=a, capa=2)
        P.rotulo(lz, W / 2, 1532 + dy, e.sub, 34, fuente="geo", alfa=a * 0.9, color=(214, 222, 255), capa=2)
    # riel de progreso (izquierda)
    y0, y1 = 470.0, 1290.0
    lz.relleno(rect_red(46, y0, 4, y1 - y0, 2), (255, 255, 255), alfa=0.22, capa=2)
    for j in range(NE):
        y = y0 + (y1 - y0) * j / (NE - 1)
        if j < k or (j == k and not en_tr) or (j == k + 1 and en_tr):
            act = (j == k and not en_tr) or (j == k + 1 and en_tr)
            if act:
                lz.halo(48, y, 30, (255, 220, 140), alfa=0.7, capa=2)
                lz.relleno(circulo(48, y, 9 + 2 * math.sin(t * 8), 14), (255, 226, 150), capa=2)
            else:
                lz.relleno(circulo(48, y, 6, 12), (255, 255, 255), capa=2)
        else:
            lz.relleno(circulo(48, y, 4, 10), (255, 255, 255), alfa=0.28, capa=2)
    # gancho inicial
    a = e_back(prog(t, 0.12, 0.5), 1.6) * (1 - e_in(prog(t, 1.75, 2.1)))
    if a > 0.01:
        lz.halo(W / 2, 545, 640, (30, 8, 50), alfa=0.35 * min(1, a), dureza=1.2, capa=2)
        P.rotulo(lz, W / 2, 500, "200 000 AÑOS", 104, k=0.9 + 0.1 * a, fuente="geo_x", alfa=min(1, a), capa=2, color=(255, 226, 140))
        P.rotulo(lz, W / 2, 604, "EN 60 SEGUNDOS", 62, k=0.9 + 0.1 * a, fuente="geo_x", alfa=min(1, a), capa=2)


# ======================================================================== render del plano secuencia
_LZ_B = None


def render_mundo(lz, t):
    global _LZ_B
    k = era_en(t)
    A = ERAS[k]
    img = None
    if k + 1 < NE and t >= INICIOS[k + 1] - D_TR:
        B = ERAS[k + 1]
        p = (t - (INICIOS[k + 1] - D_TR)) / D_TR
        tipo = TRANS[k]
        cx, cy = A.salida(t)
        col = A.COL_SALIDA
        if tipo == "portal":
            e = e_inout(p)
            a_ = img_era(lz, A, t, zt=1 + 0.6 * e_in(p), pc=(cx, cy))
            b_ = img_era(lz, B, t, zt=0.42 + 0.58 * e_out(p), pc=(cx, cy))
            img = tr_portal(a_, b_, p, cx, cy, col)
        elif tipo == "reloj":
            img = tr_reloj(img_era(lz, A, t), img_era(lz, B, t), p, cx, cy, col)
        elif tipo == "puntos":
            img = tr_puntos(img_era(lz, A, t), img_era(lz, B, t), p)
        elif tipo == "bajada":
            img = tr_bajada(img_era(lz, A, t), img_era(lz, B, t), p, 1)
        elif tipo == "subida":
            img = tr_bajada(img_era(lz, A, t), img_era(lz, B, t), p, -1)
        elif tipo == "ola":
            img = tr_ola(img_era(lz, A, t), img_era(lz, B, t), p)
        elif tipo == "glitch":
            img = E.tr_glitch(img_era(lz, A, t), img_era(lz, B, t), p, seed=5)
        elif tipo == "pixeles":
            img = E.tr_pixeles(img_era(lz, A, t), img_era(lz, B, t), p, seed=7)
    if img is None:
        img = img_era(lz, A, t)
    lz.nuevo(t, wob=0.0)
    ui(lz, t)
    img = componer(img, lz.resolver(), boil=lz.boil)
    negro = prog(t, TOTAL - 0.9, TOTAL - 0.1)
    if negro > 0:
        img = img * (1 - smooth(negro))
    return np.clip(img, 0, 1)


# ======================================================================== sonido
TR_SFX = {"portal": "iris", "reloj": "reloj_rapido", "puntos": "burbujas", "bajada": "zoom_whoosh", "subida": "zoom_whoosh",
          "ola": "ola", "glitch": "glitch", "pixeles": "glitch"}


def registrar_sfx(e):
    ev = e.ev
    ev(0.05, "brillo", 0.35, 0.0)
    for j, era in enumerate(ERAS):
        era.sfx(ev)
    for k, tipo in enumerate(TRANS):
        t0 = INICIOS[k + 1] - D_TR
        ev(t0, TR_SFX[tipo], 0.55, 0.0, dur=round(D_TR, 2)) if tipo in ("portal", "reloj", "puntos", "ola", "glitch", "pixeles") else None
        ev(INICIOS[k + 1], "pop", 0.35, 0.0, tono=1.0 + 0.03 * k)
    ev(TL["escenas"][-1]["fin_musica"], "campana", 0.4, 0.0, tono=0.8)


class Mundo(Escena):
    """Plano secuencia: todas las secciones musicales comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:        # los efectos se registran una sola vez
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
