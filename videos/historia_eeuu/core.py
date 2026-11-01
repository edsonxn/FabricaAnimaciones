# -*- coding: utf-8 -*-
"""Núcleo de «La historia de Egipto en 5 minutos» (kit v2 copiado de historia_espana): tiempos, cámara, territorios (con fractura), actores (pegatinas de boceto),
rutas sobre el mapa, sellos, rótulos manuscritos y subtítulos. La coreografía vive en `escenas.py`."""
import math
import types
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import PchipInterpolator

import boceto as B
import mapa as M
from escena_base import Escena, TL
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
ZREF = 2.5                      # zoom de referencia (Egipto: z = 2,5 ≈ el valle del Nilo entero): ahí los dibujos geo-anclados miden s


def T(eid, texto, **kw):
    """Instante (s) en que se dice `texto` dentro de la escena `eid` (ver Escena.w)."""
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def kf(t, claves, ease=e_inout):
    """Interpola claves [(t0, v0), (t1, v1), ...] (valores escalares o tuplas) con suavizado entre cada par."""
    if t <= claves[0][0]:
        return claves[0][1]
    for (ta, va), (tb, vb) in zip(claves, claves[1:]):
        if t <= tb:
            u = ease(prog(t, ta, tb))
            if isinstance(va, (tuple, list, np.ndarray)):
                return tuple(lerp(a, b, u) for a, b in zip(va, vb))
            return lerp(va, vb, u)
    return claves[-1][1]


# ------------------------------------------------------------------ cámara
class CamPath:
    """Camino de cámara por claves (t, lon, lat, zoom[, rot]) con interpolación suave (PCHIP) y una deriva lenta:
    la cámara nunca se queda quieta. La longitud se interpola «desenvuelta» (M.U): de Iberia a Filipinas cruza América y el Pacífico.
    zoom = px de pantalla por px de la rejilla "eu" (vale para las dos rejillas)."""

    def __init__(self, claves):
        claves = sorted(claves, key=lambda c: c[0])
        ts = np.array([c[0] for c in claves], float)
        for i in range(1, len(ts)):                        # tiempos estrictamente crecientes
            if ts[i] <= ts[i - 1]:
                ts[i] = ts[i - 1] + 1e-3
        self.ts = ts
        self.f = PchipInterpolator(ts, np.array([[float(M.U(c[1])), c[2], math.log(c[3]), c[4] if len(c) > 4 else 0.0] for c in claves], float), axis=0)
        self.cam = M.Cam()

    def estado(self, t, deriva=1.0):
        v = self.f(min(max(t, self.ts[0]), self.ts[-1]))
        z = math.exp(v[2])
        u = v[0] + deriva * 0.30 * math.sin(t * 0.43) / z
        lat = v[1] + deriva * 0.20 * math.sin(t * 0.31 + 1.0) / z
        z = z * (1 + deriva * 0.012 * math.sin(t * 0.7))
        # que la cámara nunca se salga de la rejilla activa (fuera no hay tierra ni mar pintados)
        rej = M.ACT
        zn = z * M.PXDEG_REF / rej.pxdeg
        hw = (W / 2) / (zn * rej.pxdeg) + 0.05
        lo_n = float(rej.nat(float(M.desU(u))))
        if 2 * hw < rej.lon1 - rej.lon0:
            lo_n = min(max(lo_n, rej.lon0 + hw), rej.lon1 - hw)
        else:
            lo_n = (rej.lon0 + rej.lon1) / 2
        y = float(M.ymerc(lat))
        hh = (H / 2) / (zn * rej.pxdeg) + 0.05
        y0, y1 = float(M.ymerc(rej.lat1)), float(M.ymerc(rej.lat0))
        y = min(max(y, y0 + hh), y1 - hh) if 2 * hh < y1 - y0 else (y0 + y1) / 2
        return float(M.desU(lo_n)), float(M.inv_ymerc(y)), z, v[3] + deriva * 0.006 * math.sin(t * 0.37)

    def cam_en(self, t, deriva=1.0):
        self.cam.fijar(*self.estado(t, deriva))
        return self.cam


# ------------------------------------------------------------------ territorios
BIG = 320                       # «lejos» (int16, 1/8 px): 40 px de la rejilla (Egipto: franjas finas del valle; con 200 px no aparecían hasta el final)


class Territorio:
    """Sucesión de formas y colores de UNA capa: claves dict(t, campo, color, dur). El campo es el nombre de un campo de M.CAMPOS
    (o None = nada); entre claves se interpolan los campos de distancia, así el reino crece, se encoge o se reparte sin saltos."""

    def __init__(self, claves):
        self.k = sorted(claves, key=lambda c: c["t"])

    def estado(self, t):
        i = -1
        for j, c in enumerate(self.k):
            if c["t"] <= t:
                i = j
        if i < 0:
            return None, (0, 0, 0)
        c = self.k[i]
        prev = self.k[i - 1] if i > 0 else None
        d = c.get("dur", 1.3)
        u = e_inout(prog(t, c["t"], c["t"] + d))
        if u >= 1.0 or (prev is None and c["campo"] is None):
            return (M.CAMPOS[c["campo"]] if c["campo"] else None), c["color"]
        a = M.CAMPOS[prev["campo"]] if prev and prev["campo"] else None
        b = M.CAMPOS[c["campo"]] if c["campo"] else None
        col = tuple(lerp(x, y, u) for x, y in zip(prev["color"], c["color"])) if prev else c["color"]
        if a is None and b is None:
            return None, col
        if a is None:
            return cv2.addWeighted(np.full_like(b, BIG), 1 - u, b, u, 0), col
        if b is None:
            return cv2.addWeighted(a, 1 - u, np.full_like(a, BIG), u, 0), col
        return cv2.addWeighted(a, 1 - u, b, u, 0), col


class Fractura:
    """Ventana en la que el territorio se parte en celdas (estados, reinos, caudillos), se separan y se vuelven a unir.
    t0→t1 se abre, t1→t2 se mantiene, t2→t3 se cierra. colores = por celda (o función (t, i) -> color)."""

    def __init__(self, celdas, t0, t1, t2, t3, colores=None, gap=24.0, deriva=46.0, nervio=1.0, semilla=1, capa=0, fijas=(), rej="eu"):
        self.celdas, self.t = celdas, (t0, t1, t2, t3)
        self.colores = colores
        self.gap, self.deriva, self.nervio = gap, deriva, nervio
        self.capa, self.rej = capa, rej
        n = 49 if celdas == "estados" else len(M.CELDAS_SEMILLAS.get(celdas, M.CELDAS_PAISES.get(celdas, [])))   # estados: 1..48 + 0 (fuera)
        rng = np.random.default_rng(semilla)
        ang = rng.uniform(0, 2 * math.pi, n)
        self.dir = np.stack([np.cos(ang), np.sin(ang)], 1)
        self.fase = rng.uniform(0, 6.28, n)
        self.fijas = np.zeros(n, bool)
        for i in fijas:
            self.fijas[i] = True
            self.dir[i] = 0.0

    def g(self, t):
        t0, t1, t2, t3 = self.t
        if t <= t0 or t >= t3:
            return 0.0
        if t < t1:
            return e_out(prog(t, t0, t1))
        if t <= t2:
            return 1.0
        return 1 - e_in(prog(t, t2, t3))

    def color(self, t, i, base):
        if self.colores is None:
            c = M.COL_CELDAS[i % len(M.COL_CELDAS)]
        elif callable(self.colores):
            c = self.colores(t, i)
        else:
            c = self.colores[i % len(self.colores)]
        return c


from numba import njit, prange            # noqa: E402


@njit(parallel=True, fastmath=True, cache=True)
def _celdas_nb(img, S, idx, borde, cols, ox, oy, gap, nz, pincel, grano, alfa, sombra, amp, luz, kluz, y0, y1, x0, x1):
    h, w = S.shape
    K = cols.shape[0]
    for y in prange(y0, y1):
        for x in range(x0, x1):
            got = -1
            s = 99.0
            for c in range(K):
                sx = x - int(ox[c])
                sy = y - int(oy[c])
                if sx < 1 or sy < 1 or sx >= w - 1 or sy >= h - 1:
                    continue
                if idx[sy, sx] != c:
                    continue
                v = S[sy, sx]
                g = gap - borde[sy, sx]
                if g > v:
                    v = g
                v += amp * nz[y, x]
                if v < 1.5:
                    got = c
                    s = v
            if got < 0:
                continue
            a = 0.5 - s * 0.7692
            if a <= 0.0:
                continue
            if a > 1.0:
                a = 1.0
            a *= alfa
            d = -s * (1.0 / 60.0)
            if d < 0.0:
                d = 0.0
            if d > 1.0:
                d = 1.0
            lum = 1.0 - 0.07 * (1.0 - d)
            if d < 1.0:
                sx = x - int(ox[got])
                sy = y - int(oy[got])
                gx = S[sy, sx + 1] - S[sy, sx - 1]
                gy = S[sy + 1, sx] - S[sy - 1, sx]
                gx += (-(borde[sy, sx + 1] - borde[sy, sx - 1]))
                gy += (-(borde[sy + 1, sx] - borde[sy - 1, sx]))
                nr = np.sqrt(gx * gx + gy * gy) + 1e-6
                sh = (gx * 0.55 + gy * 0.83) / nr
                band = (1.0 - d) * (1.0 - d)
                if sh > 0.0:
                    lum -= sombra * sh * band
                else:
                    lum -= 0.10 * sh * band
            k = lum * (1.0 + 1.2 * pincel[y, x]) * (1.0 + kluz * luz[y, x])
            for ch in range(3):
                pig = cols[got, ch] * k * grano[y, x, ch]
                img[y, x, ch] = img[y, x, ch] * (1.0 - a) + pig * a


def pintar_celdas(img, cam, S_campo, fr, t, g, fase=0, colores_fin=None, luz=None, alfa=1.0):
    """Pinta el territorio partido en celdas con separación g (0..1). Todo en px de pantalla. Devuelve S (pantalla)."""
    idx_f, borde_f = M.celdas(fr.celdas)
    S = cam.proyectar(S_campo)
    idx = cv2.warpAffine(idx_f, cam.M, (W, H), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=255)
    borde = cam.proyectar(borde_f, 0.0)
    n = len(fr.dir)
    cols = np.array([np.array(fr.color(t, i, None), np.float32) / 255.0 for i in range(n)], np.float32)
    if colores_fin is not None:                       # al cerrar, los colores tienden al color del imperio
        cf = np.array(colores_fin, np.float32) / 255.0
        cols = cols * g + cf[None, :] * (1 - g)
    ox = np.zeros(n, np.float32)
    oy = np.zeros(n, np.float32)
    k = (cam.z / 2.5) ** 0.5
    for i in range(n):
        if fr.fijas[i]:
            continue
        j = fr.nervio * 7.0 * math.sin(t * 3.1 + fr.fase[i]) * g
        ox[i] = (fr.dir[i, 0] * fr.deriva * g + j) * k
        oy[i] = (fr.dir[i, 1] * fr.deriva * g + 0.7 * j) * k
    r = M._roi(S, 90)
    if r is None:
        return S
    _celdas_nb(img, S, idx, borde, cols, ox, oy, np.float32(fr.gap * g * k), M.RUIDO[fase % 3], M.PINCEL, M.GRANO, np.float32(alfa),
               np.float32(0.24), np.float32(4.0), M._CERO if luz is None else luz, np.float32(0.0 if luz is None else 0.34), r[0], r[1], r[2], r[3])
    return S


# ------------------------------------------------------------------ rutas y trazos sobre el mapa
# ------------------------------------------------------------------ rutas y trazos sobre el mapa
def _acumular(P):
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    return d, float(d[-1])


def recortar(P, frac):
    """Parte inicial (fracción frac de la longitud) de la polilínea P."""
    P = np.asarray(P, float)
    if frac >= 1:
        return P
    d, L = _acumular(P)
    if L <= 0 or frac <= 0:
        return P[:1]
    Lc = L * frac
    k = int(np.searchsorted(d, Lc))
    k = max(1, min(k, len(P) - 1))
    f = (Lc - d[k - 1]) / max(1e-9, d[k] - d[k - 1])
    return np.vstack([P[:k], P[k - 1] + (P[k] - P[k - 1]) * f])


def punto_en(P, frac):
    Q = recortar(P, max(frac, 1e-4))
    if len(Q) < 2:
        return tuple(Q[0]), 0.0
    a, b = Q[-2], Q[-1]
    return tuple(b), math.atan2(b[1] - a[1], b[0] - a[0])


def suavizar(P, n=10):
    return B.curva(np.asarray(P, float), n)


def banda(img, P, color, ancho, alfa=0.95):
    """Pincelada gruesa de guache a lo largo de la polilínea de pantalla P."""
    P = np.asarray(P, float)
    if len(P) < 2:
        return
    x0, y0 = np.floor(P.min(0) - ancho - 4).astype(int)
    x1, y1 = np.ceil(P.max(0) + ancho + 4).astype(int)
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    cv2.polylines(m, [np.rint((P - (x0, y0)) * 8).astype(np.int32).reshape(-1, 1, 2)], False, 255, max(1, int(ancho)), cv2.LINE_AA, 3)
    a = (m.astype(np.float32) * (alfa / 255.0))[..., None]
    col = np.array(color, np.float32) / 255.0
    sub = img[y0:y1, x0:x1]
    sub[:] = sub * (1 - a) + col * a * (1 + 1.0 * M.PINCEL[y0:y1, x0:x1])[..., None] * M.GRANO[y0:y1, x0:x1]


def linea_punteada(h, P, t, dash=30.0, hueco=22.0, ancho=5.0, seed=0, fs=0, frac=1.0):
    """Ruta punteada de tinta (se va dibujando)."""
    P = recortar(P, frac)
    if len(P) < 2:
        return
    d, L = _acumular(P)
    s = 0.0
    k = 0
    while s < L:
        e = min(L, s + dash)
        ia, ib = np.searchsorted(d, s), np.searchsorted(d, e)
        seg = [np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])]
        pts = [seg] + [P[j] for j in range(ia, ib) if s < d[j] < e] + [[np.interp(e, d, P[:, 0]), np.interp(e, d, P[:, 1])]]
        h.trazo(np.array(pts), ancho, seed + k, fs, 1.0, amp=1.0)
        s += dash + hueco
        k += 1


def contornos_tinta(h, S, fs, semilla=0, ancho=5.0, minimo=90, v=255):
    """Contorno de tinta (a mano alzada, que hierve) de la forma de pantalla S (negativo dentro). Los tramos pegados al borde de la
    pantalla no se dibujan (no son frontera: es solo donde termina el cuadro)."""
    m = (S[::2, ::2] < 0).astype(np.uint8)
    if m.max() == 0 or v <= 0:
        return
    hh, ww = m.shape
    cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for k, c in enumerate(cs):
        if len(c) * 2 < minimo:
            continue
        P = c.reshape(-1, 2)
        borde = (P[:, 0] <= 1) | (P[:, 1] <= 1) | (P[:, 0] >= ww - 2) | (P[:, 1] >= hh - 2)
        if borde.all():
            continue
        if not borde.any():
            Q = cv2.approxPolyDP(c, 1.3, True).reshape(-1, 2).astype(float) * 2
            if len(Q) >= 4:
                h.trazo(np.vstack([Q, Q[:1]]), ancho, semilla + k * 13, fs, 1.0, amp=1.6, v=v)
            continue
        # partir en tramos que no tocan el borde (empezando justo en un punto de borde)
        i0 = int(np.argmax(borde))
        P = np.roll(P, -i0, 0)
        b = np.roll(borde, -i0)
        tramos, cur = [], []
        for p, eb in zip(P, b):
            if eb:
                if len(cur) > 3:
                    tramos.append(np.array(cur))
                cur = []
            else:
                cur.append(p)
        if len(cur) > 3:
            tramos.append(np.array(cur))
        for j, T_ in enumerate(tramos):
            if len(T_) * 2 < 24:
                continue
            Q = cv2.approxPolyDP(T_.reshape(-1, 1, 2).astype(np.int32), 1.3, False).reshape(-1, 2).astype(float) * 2
            if len(Q) >= 2:
                h.trazo(Q, ancho, semilla + k * 13 + j, fs, 1.0, amp=1.6, v=v)


# ------------------------------------------------------------------ texto, sellos
# ------------------------------------------------------------------ texto, sellos
def _mascara_texto(txt, px=64):
    """Como B.mascara_texto, pero con margen superior para que no se corte la tilde de las mayúsculas (Á, Í, Ó…)."""
    if not any(c in txt for c in "ÁÉÍÓÚÑ"):
        return B.mascara_texto(txt, px)
    f = B._fuente(px)
    bb = f.getbbox(txt)
    top = int(px * 0.28)
    w, h = bb[2] + 10, int(px * 1.5) + top
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((4, 2 + top), txt, font=f, fill=255, stroke_width=1 if px < 120 else 2, stroke_fill=255)
    return np.asarray(im, np.uint8)


def rotulo(h, txt, x, y, px, u, fs, v=255, tv=0.0, peg=True, inclinar=0.0):
    """Texto manuscrito centrado en (x, y) que se va escribiendo (u 0..1); se mece siempre. Con recorte de papel (peg)."""
    if u <= 0 or v <= 0:
        return
    m = _mascara_texto(txt, px)
    mx = 3.0 * math.sin(2 * B.OMEGA * tv + x * 0.01)
    my = 5.0 * math.sin(B.OMEGA * tv * 3 + y * 0.013)
    xx, yy = x - m.shape[1] / 2 + (fs - 1) * 0.7 + mx, y - m.shape[0] / 2 + my
    cols = m.shape[1] * min(1.0, u)
    if peg:
        h.peg_mascara(m, xx, yy, cols)
    h.pegar_mascara(m, xx, yy, cols=cols, v=v)


_FUENTE_CJK = "C:/Windows/Fonts/georgiab.ttf"   # letras de sello (los emblemas dibujados están en sellos.py)


@lru_cache(maxsize=64)
def mascara_sello(ch, px=150, rot=0.0):
    """Sello rojo: cuadrado redondeado lleno con el carácter en hueco (como un sello de tinta)."""
    n = int(px * 1.25)
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, n - 4, n - 4), radius=int(px * 0.12), fill=255)
    d.rounded_rectangle((int(px * 0.09), int(px * 0.09), n - int(px * 0.09), n - int(px * 0.09)), radius=int(px * 0.08), outline=0, width=max(2, int(px * 0.028)))
    f = ImageFont.truetype(_FUENTE_CJK, int(px * 0.88))
    bb = d.textbbox((0, 0), ch, font=f)
    d.text(((n - (bb[2] - bb[0])) / 2 - bb[0], (n - (bb[3] - bb[1])) / 2 - bb[1]), ch, font=f, fill=0)
    a = np.asarray(im, np.uint8)
    if rot:
        Mr = cv2.getRotationMatrix2D((n / 2, n / 2), math.degrees(rot), 1.0)
        a = cv2.warpAffine(a, Mr, (n, n), flags=cv2.INTER_LINEAR)
    return a


def estampar(h, ch, x, y, px, rot=0.0, color=(198, 52, 52), desgaste=0.0, semilla=0, peg=True):
    m = mascara_sello(ch, int(px), round(rot, 2))
    x0, y0 = x - m.shape[1] / 2, y - m.shape[0] / 2
    if peg:
        h.peg_mascara(cv2.dilate(m, np.ones((3, 3), np.uint8)), x0, y0)
    h.sello(m, x0, y0, color, 240, desgaste, semilla)


# ------------------------------------------------------------------ actores (pegatinas)
class Act:
    """Un dibujo en escena. Posición: pantalla (x, y, s[, rot]) o función de t; o geográfica `geo=(lon, lat)` + desplazamiento `off`.
    entra: pluma | lt | pop | sube | izq | der | cae | fija.  sale: borrar | encoger | caer | baja | sube_fuera | izq_fuera | der_fuera | cortar."""

    def __init__(self, dib, pos=None, t_in=0.0, d_in=0.45, entra="pop", t_out=None, d_out=0.4, sale="encoger", sem=0, peg=True,
                 geo=None, off=(0, 0), s=1.0, rot=0.0, flip=False, vida=1.0, z=0, sfx=(), sfx_out=(), dx=900.0, dy=700.0, zs=0.3,
                 pos_geo=None, alfa=1.0):
        self.dib, self.pos, self.t_in, self.d_in, self.entra = dib, pos, t_in, d_in, entra
        self.t_out, self.d_out, self.sale, self.sem, self.peg = t_out, d_out, sale, sem, peg
        self.geo, self.off, self.s, self.rot, self.flip, self.vida, self.z = geo, off, s, rot, flip, vida, z
        self.dx, self.dy, self.zs, self.pos_geo = dx, dy, zs, pos_geo
        self.snd = [(t_in + a[0], a[1], a[2], a[3] if len(a) > 3 else {}) for a in sfx]
        if t_out is not None:
            self.snd += [(t_out + a[0], a[1], a[2], a[3] if len(a) > 3 else {}) for a in sfx_out]

    def estado(self, t, cam):
        if self.geo is not None or self.pos_geo is not None:
            g = self.pos_geo(t) if self.pos_geo is not None else self.geo
            x, y = cam.pant(g[0], g[1])
            off = self.off(t) if callable(self.off) else self.off
            x, y = x + off[0], y + off[1]
            s = self.s * min((cam.z / ZREF) ** self.zs, 2.0)
            rot = self.rot
        else:
            p = self.pos(t) if callable(self.pos) else self.pos
            x, y, s = p[0], p[1], p[2]
            rot = p[3] if len(p) > 3 else self.rot
        return x, y, s, rot


def dibujar_actor(h, a, t, cam, fs, te):
    if t < a.t_in or (getattr(a, "tfin", None) is not None and t >= a.tfin):
        return
    x, y, s, rot = a.estado(t, cam)
    v = prog(t, a.t_in, a.t_in + a.d_in)
    u, sq, lap, ent = 1.0, 0.0, 0.0, a.entra
    if ent == "pluma":
        u = v
    elif ent == "lt":
        tp = 0.14
        u = prog(t, a.t_in + tp, a.t_in + tp + a.d_in)
        lap = 1 - u
    elif ent == "pop":
        s *= e_back(v, 2.2)
        sq = 0.25 * (1 - v) * math.sin(v * 11)
        if s < 0.02:
            return
    elif ent == "sube":
        y += a.dy * (1 - e_out(v))
    elif ent == "baja_entra":
        y -= a.dy * (1 - e_out(v))
    elif ent == "izq":
        x -= a.dx * (1 - e_out(v))
    elif ent == "der":
        x += a.dx * (1 - e_out(v))
    elif ent == "cae":
        hh = abs(math.cos(v * math.pi * 2.5)) * (1 - v) ** 1.3 if v < 1 else 0.0
        y -= a.dy * hh
        sq = 0.18 * max(0.0, 1 - v * 4) * (1 if v < 0.4 else 0)
    if a.t_out is not None and t > a.t_out:
        if a.sale == "cortar":
            return
        uo = prog(t, a.t_out, a.t_out + a.d_out)
        if uo >= 1:
            return
        m = a.sale
        if m == "borrar":
            u = min(u, 1 - uo)
        elif m == "caer":
            y += 1500 * e_in(uo)
            rot += 0.7 * uo
        elif m == "encoger":
            s *= 1 - e_in(uo)
        elif m == "baja":
            y += 1300 * e_in(uo)
        elif m == "sube_fuera":
            y -= 1300 * e_in(uo)
        elif m == "izq_fuera":
            x -= 1800 * e_in(uo)
        elif m == "der_fuera":
            x += 1800 * e_in(uo)
    if x < -600 or x > W + 600 or y < -600 or y > H + 900:
        return
    d = a.dib(t) if callable(a.dib) else a.dib
    d.dibujar(h, x, y, s, rot, a.flip, u, fs, a.sem, sq=sq, lapiz=lap, tv=te, vida=a.vida, peg=a.peg)


# ------------------------------------------------------------------ subtítulos manuscritos (horizontal)
PX_SUB = 60
ANCHO_SUB = 1560
_FR = [f for e in TL["escenas"] for f in e["frases"]]


def _lineas(frase):
    palabras = [dict(w=w["w"], s=w["s"], e=w["e"]) for w in frase["words"]]
    lineas, cur, ancho = [], [], 0.0
    esp = B.ancho_texto(" ", PX_SUB)
    for w in palabras:
        aw = B.ancho_texto(w["w"], PX_SUB)
        if cur and ancho + esp + aw > ANCHO_SUB:
            lineas.append(cur)
            cur, ancho = [], 0.0
        cur.append((w, aw))
        ancho += aw + (esp if len(cur) > 1 else 0)
    if cur:
        lineas.append(cur)
    out = []
    n = len(lineas)
    for li, ln in enumerate(lineas):
        tot = sum(a for _, a in ln) + esp * (len(ln) - 1)
        x = W / 2 - tot / 2
        y = 1008 - (n - 1) * 70 + li * 70
        for w, aw in ln:
            out.append((w, x, y))
            x += aw + esp
    return out


SUBS = [(f, _lineas(f), min(f["t1"] + 0.8, (_FR[i + 1]["t0"] - 0.05) if i + 1 < len(_FR) else 1e9)) for i, f in enumerate(_FR)]


def dibujar_subs(h, t, fs):
    for f, pals, hasta in SUBS:
        ini = f["t0"] - 0.05
        if not (ini <= t < hasta):
            continue
        v = int(255 * (1 - prog(t, hasta - 0.25, hasta)))
        for w, x, y in pals:
            dur = max(w["e"] - w["s"], 0.16)
            u = prog(t, w["s"] - 0.03, w["s"] - 0.03 + dur)
            if u <= 0:
                continue
            m = B.mascara_texto(w["w"], PX_SUB)
            cols = int(m.shape[1] * u)
            h.peg_mascara(m, x - 4 + (fs - 1) * 0.6, y - 38, cols)
            h.pegar_mascara(m, x - 4 + (fs - 1) * 0.6, y - 38 + (1.0 if fs == 1 else 0.0), cols=cols, v=v)
