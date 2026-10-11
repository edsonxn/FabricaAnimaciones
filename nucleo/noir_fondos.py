# -*- coding: utf-8 -*-
"""Escenarios del estilo NOIR pintados por código en tinta y aguada GRIS (nucleo/noir.py). Se pintan una vez por proceso
(lru_cache en el video) en lienzos más grandes que la pantalla y se guardan como gris uint8 + alfa uint8 (poca memoria);
Capa.pegar() los compone con paralaje bajo la cámara del lienzo Noir.

    L = Lienzo(4000, 2400, origen=(-200, -1800))     # coordenadas del MUNDO: (x, y) -> píxel (x - ox, y - oy)
    L.poli(P, 0.22, tex=0.1); L.linea(P, 3); L.trama(P, ang=45, sep=7)
    edificio(L, x, base, ancho, alto, tipo="ladrillo"|"deco"|"cristal"|"tienda", sem=3)
    capa = L.capa()                                   # Capa (gris u8, alfa u8, origen)
    capa.pegar(h, prof=0.6)                           # dentro del render (aplica cámara + paralaje)

Tonos 0..1 (0 = negro de tinta). Las luces de la escena (Noir.luz_*) multiplican después: pinta los fondos con valores
medios-bajos y deja que el claroscuro lo haga la luz. Las ventanas encendidas se pintan claras (son fuentes de luz).
"""
import math

import cv2
import numpy as np

from motor import H, W
from noir import fbm


class Capa:
    def __init__(self, g, a, origen, e=None):
        self.g, self.a, self.e = g, a, e
        self.ox, self.oy = origen

    def pegar(self, h, prof=1.0, oscuro=1.0, dx=0.0, dy=0.0, emis=1.0, bruma=0.0, tono_bruma=0.42):
        """Compone la capa con la cámara (paralaje prof). dx, dy desplazan la capa (nubes que derivan). Las partes emisivas
        (ventanas encendidas) van a la capa emisiva del lienzo Noir."""
        M = h.matriz_capa(prof) @ np.array([[1, 0, self.ox + dx], [0, 1, self.oy + dy], [0, 0, 1]], float)
        g = cv2.warpAffine(self.g, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        v = g.astype(np.float32) * (oscuro / 255.0)
        if bruma > 0:                                   # perspectiva aérea: lo lejano se aclara hacia el gris de la niebla
            v = v * (1 - bruma) + tono_bruma * bruma
        if self.a is None:
            h.img[:] = v[..., None]
            af = None
        else:
            a = cv2.warpAffine(self.a, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            af = a.astype(np.float32) * (1 / 255.0)
            h.img *= (1 - af)[..., None]
            h.img += (v * af)[..., None]
        if h._E is not None and af is not None:
            h._E *= 1 - af
        if self.e is not None and emis > 0:
            e = cv2.warpAffine(self.e, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            E = h.emisivo()
            E += e.astype(np.float32) * (emis / 255.0)


class Lienzo:
    def __init__(self, w, h, origen=(0, 0), base=None, sem=1):
        self.w, self.h = int(w), int(h)
        self.ox, self.oy = origen
        self.g = np.zeros((self.h, self.w), np.float32)
        self.a = np.zeros((self.h, self.w), np.float32) if base is None else np.ones((self.h, self.w), np.float32)
        if base is not None:
            self.g[:] = base
        self.sem = sem
        self._tex = None
        self._gran = None
        self.e = np.zeros((self.h, self.w), np.float32)      # lo que emite luz (ventanas, letreros, faroles)

    # ------------------------------------------------------------------ texturas
    def tex(self):
        if self._tex is None:
            self._tex = 0.7 * fbm(self.w, self.h, 160, 4, self.sem) + 0.3 * fbm(self.w, self.h, 30, 2, self.sem + 1)
        return self._tex

    def gran(self):
        """Granulado de pigmento (puntitos que se acumulan en el papel)."""
        if self._gran is None:
            r = np.random.default_rng(self.sem + 9)
            g = cv2.GaussianBlur(r.standard_normal((self.h, self.w)).astype(np.float32), (0, 0), 0.9)
            self._gran = g / (g.std() + 1e-9)
        return self._gran

    def _P(self, P):
        P = np.asarray(P, float).reshape(-1, 2)
        return P - (self.ox, self.oy)

    def _roi(self, P, m=4):
        x0 = int(max(0, math.floor(P[:, 0].min()) - m))
        y0 = int(max(0, math.floor(P[:, 1].min()) - m))
        x1 = int(min(self.w, math.ceil(P[:, 0].max()) + m + 1))
        y1 = int(min(self.h, math.ceil(P[:, 1].max()) + m + 1))
        return x0, y0, x1, y1

    def mascara(self, P, blur=0.7, rug=0.0, m=None):
        Q = self._P(P)
        x0, y0, x1, y1 = self._roi(Q, int(4 + 3 * blur + rug * 4) if m is None else m)
        if x1 <= x0 or y1 <= y0:
            return None
        mk = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(mk, [np.rint((Q - (x0, y0)) * 16).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_AA, 4)
        a = mk.astype(np.float32) / 255.0
        if rug > 0:
            n = self.tex()[y0:y1, x0:x1]
            a = np.clip((cv2.GaussianBlur(a, (0, 0), 2.0) - 0.5) * 3 + 0.5 + rug * 0.12 * n, 0, 1)
        if blur > 0:
            a = cv2.GaussianBlur(a, (0, 0), blur)
        return a, x0, y0

    def _mezclar(self, a, x0, y0, tono, alfa=1.0, tex=0.08, gran=0.03, grad=None):
        hh, ww = a.shape
        sl = (slice(y0, y0 + hh), slice(x0, x0 + ww))
        if grad is not None:
            t2, gy0, gy1 = grad
            yy = (np.arange(y0, y0 + hh, dtype=np.float32) + self.oy)[:, None]
            k = np.clip((yy - gy0) / max(1.0, gy1 - gy0), 0, 1)
            val = tono + (t2 - tono) * k
        else:
            val = tono
        val = val * (1 + tex * self.tex()[sl]) + gran * self.gran()[sl] * 0.5
        aa = a * alfa
        self.g[sl] += (val - self.g[sl]) * aa
        self.a[sl] = np.maximum(self.a[sl], aa)

    # ------------------------------------------------------------------ primitivas
    def poli(self, P, tono, alfa=1.0, tex=0.08, gran=0.03, blur=0.7, rug=0.0, grad=None, emis=0.0):
        r = self.mascara(P, blur, rug)
        if r is not None:
            self._mezclar(r[0], r[1], r[2], tono, alfa, tex, gran, grad)
            a, x0, y0 = r
            sl = (slice(y0, y0 + a.shape[0]), slice(x0, x0 + a.shape[1]))
            self.e[sl] *= 1 - a * alfa                        # lo pintado encima tapa la emisión
            if emis > 0:
                self.e[sl] += a * alfa * emis

    def rect(self, x, y, w, h, tono, **kw):
        self.poli([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], tono, **kw)

    def elipse(self, cx, cy, rx, ry, tono, rot=0.0, n=48, **kw):
        a = np.linspace(0, 2 * math.pi, n, endpoint=False)
        c, s = math.cos(rot), math.sin(rot)
        x, y = rx * np.cos(a), ry * np.sin(a)
        self.poli(np.stack([cx + x * c - y * s, cy + x * s + y * c], 1), tono, **kw)

    def linea(self, P, w=2.5, tono=0.03, alfa=1.0, cerrado=False, jit=0.8, sem=0):
        """Trazo de tinta (con un temblor leve de pluma)."""
        Q = self._P(P)
        if len(Q) < 2:
            return
        if jit > 0:
            L = np.cumsum(np.r_[0, np.hypot(*np.diff(Q, axis=0).T)])
            n = max(2, int(L[-1] / 6))
            s = np.linspace(0, L[-1], n)
            Q = np.stack([np.interp(s, L, Q[:, 0]), np.interp(s, L, Q[:, 1])], 1)
            r = np.random.default_rng(sem + len(Q))
            Q = Q + cv2.GaussianBlur(r.standard_normal((len(Q), 2)).astype(np.float32), (1, 0), 2.0) * jit
        if cerrado:
            Q = np.vstack([Q, Q[:1]])
        x0, y0, x1, y1 = self._roi(Q, int(w) + 4)
        if x1 <= x0 or y1 <= y0:
            return
        mk = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.polylines(mk, [np.rint((Q - (x0, y0)) * 16).astype(np.int32).reshape(-1, 1, 2)], False, 255,
                      max(1, int(round(w))), cv2.LINE_AA, 4)
        self._mezclar(mk.astype(np.float32) / 255.0, x0, y0, tono, alfa, 0.0, 0.0)

    def trama(self, P, ang=45.0, sep=7.0, w=1.3, tono=0.04, alfa=0.7, cruz=False, var=0.25):
        """Tramado de plumilla dentro del polígono P (líneas paralelas un poco irregulares)."""
        r = self.mascara(P, 0.5)
        if r is None:
            return
        a, x0, y0 = r
        hh, ww = a.shape
        lin = np.zeros((hh, ww), np.uint8)
        diag = int(math.hypot(hh, ww)) + 2
        rng = np.random.default_rng(int(x0 * 7 + y0 * 13 + ang))
        for ang_k in ([ang, ang + 90] if cruz else [ang]):
            c, s = math.cos(math.radians(ang_k)), math.sin(math.radians(ang_k))
            for k in np.arange(-diag, diag, sep):
                o = k + rng.uniform(-var, var) * sep
                cx, cy = ww / 2 - s * o, hh / 2 + c * o
                p0 = (int((cx - c * diag) * 16), int((cy - s * diag) * 16))
                p1 = (int((cx + c * diag) * 16), int((cy + s * diag) * 16))
                cv2.line(lin, p0, p1, int(255 * rng.uniform(0.6, 1.0)), max(1, int(round(w))), cv2.LINE_AA, 4)
        self._mezclar(lin.astype(np.float32) / 255.0 * a, x0, y0, tono, alfa, 0.0, 0.0)

    def brillo(self, x, y, r, k=0.6, ry=None, tono=1.0):
        """Resplandor suave (luz de ventana, farol) que aclara alrededor."""
        ry = r if ry is None else ry
        x, y = x - self.ox, y - self.oy
        x0, y0 = int(max(0, x - r * 2)), int(max(0, y - ry * 2))
        x1, y1 = int(min(self.w, x + r * 2)), int(min(self.h, y + ry * 2))
        if x1 <= x0 or y1 <= y0:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt(((xx - x) / r) ** 2 + ((yy - y) / ry) ** 2)
        a = np.clip(1 - d / 2, 0, 1) ** 2.2 * k
        self.g[y0:y1, x0:x1] += (tono - self.g[y0:y1, x0:x1]) * a
        self.a[y0:y1, x0:x1] = np.maximum(self.a[y0:y1, x0:x1], a)
        self.e[y0:y1, x0:x1] += a * 0.5 * tono

    def capa(self, opaco=False):
        g = np.clip(self.g * 255, 0, 255).astype(np.uint8)
        a = None if opaco else np.clip(self.a * 255, 0, 255).astype(np.uint8)
        e = np.clip(self.e * 255, 0, 255).astype(np.uint8) if self.e.max() > 0.01 else None
        return Capa(g, a, (self.ox, self.oy), e)


# ====================================================================== piezas de ciudad
def ventana(L, x, y, w, h, encendida=0.0, rng=None, marco=0.03, persiana=False, figura=False, tono_osc=0.07):
    """Ventana de guillotina: vidrio oscuro o encendido (persiana, cortina o silueta), marco y travesaño de tinta, alféizar."""
    rng = rng or np.random.default_rng(0)
    if encendida > 0:
        L.rect(x, y, w, h, 0.55 + 0.4 * encendida, tex=0.05, grad=(0.55 + 0.25 * encendida, y, y + h), emis=0.55 * encendida)
        if persiana:
            for k in range(int(h / 6)):
                L.linea([(x + 1, y + 3 + k * 6), (x + w - 1, y + 3 + k * 6)], 1.4, 0.25, 0.8, jit=0)
        elif rng.uniform() < 0.5:
            cw = w * rng.uniform(0.2, 0.4)
            L.poli([(x, y), (x + cw, y), (x + cw * 0.7, y + h), (x, y + h)], 0.35, alfa=0.85)
        if figura:
            cx = x + w * rng.uniform(0.3, 0.7)
            L.elipse(cx, y + h * 0.42, w * 0.13, h * 0.16, 0.06)
            L.poli([(cx - w * 0.28, y + h), (cx - w * 0.2, y + h * 0.62), (cx + w * 0.2, y + h * 0.62), (cx + w * 0.28, y + h)], 0.06)
        L.brillo(x + w / 2, y + h / 2, w * 0.9, 0.18 * encendida, ry=h * 0.8, tono=0.6)
    else:
        L.rect(x, y, w, h, tono_osc, tex=0.12, grad=(tono_osc * 0.6, y, y + h))
        if rng.uniform() < 0.35:                      # reflejo de la luna en el vidrio
            L.poli([(x + w * 0.15, y + h * 0.1), (x + w * 0.35, y + h * 0.1), (x + w * 0.1, y + h * 0.6)], 0.22, alfa=0.6)
    L.linea([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], 1.6, marco, cerrado=True, jit=0.3)
    L.linea([(x, y + h * 0.5), (x + w, y + h * 0.5)], 1.6, marco, jit=0.2)
    L.rect(x - 3, y + h, w + 6, 4, 0.30, tex=0.05)


def escalera_incendio(L, x, y0, y1, w=90, piso=120, tono=0.05):
    """Escalera de incendio en zigzag: plataformas con barandal y tramos diagonales (tinta fina)."""
    y = y0
    k = 0
    while y + piso <= y1:
        L.rect(x - 8, y + piso - 6, w + 16, 6, tono)
        for bx in np.arange(x - 8, x + w + 9, 9):
            L.linea([(bx, y + piso - 6), (bx, y + piso - 30)], 1.2, tono, jit=0)
        L.linea([(x - 8, y + piso - 30), (x + w + 8, y + piso - 30)], 1.8, tono, jit=0)
        a, b = (x, x + w) if k % 2 == 0 else (x + w, x)
        L.linea([(a, y + 6), (b, y + piso - 8)], 2.0, tono, jit=0)
        L.linea([(a + (6 if k % 2 == 0 else -6), y + 6), (b + (6 if k % 2 == 0 else -6), y + piso - 8)], 1.4, tono, jit=0)
        for st in np.linspace(0.1, 0.9, 7):
            px, py = a + (b - a) * st, y + 6 + (piso - 14) * st
            L.linea([(px - 4, py), (px + 4, py)], 1.4, tono, jit=0)
        y += piso
        k += 1


def tanque_agua(L, cx, base, r=46, alto=80, tono=0.10):
    L.poli([(cx - r, base - alto), (cx + r, base - alto), (cx + r, base), (cx - r, base)], tono, grad=(tono * 0.5, base - alto, base))
    L.poli([(cx - r - 6, base - alto), (cx, base - alto - 34), (cx + r + 6, base - alto)], tono * 0.8)
    for k in range(5):
        L.linea([(cx - r, base - alto + 14 + k * 15), (cx + r, base - alto + 14 + k * 15)], 1.4, 0.03, jit=0.2)
    for lx in (-r + 6, -r * 0.3, r * 0.3, r - 6):
        L.linea([(cx + lx, base), (cx + lx * 1.1, base + 46)], 3, 0.03, jit=0)
    L.linea([(cx - r, base + 22), (cx + r, base + 40)], 1.5, 0.03, jit=0)
    L.linea([(cx + r, base + 22), (cx - r, base + 40)], 1.5, 0.03, jit=0)
    L.linea([(cx - r - 6, base - alto), (cx, base - alto - 34), (cx + r + 6, base - alto)], 2.0, 0.6, alfa=0.6, jit=0)  # luna


def edificio(L, x, base, ancho, alto, tipo="ladrillo", sem=0, encendidas=0.18, prof_lado=40, luz_lado=-1, detalle=1.0):
    """Edificio de la ciudad noir. tipo: ladrillo (cornisa, escalera de incendio, tanque de agua) · deco (corona escalonada
    art déco con aguja) · cristal (rascacielos moderno de vidrio: el laboratorio) · tienda (planta baja con escaparate).
    base = y del pie; luz_lado: -1 la luna ilumina el lado izquierdo (cara lateral oscura a la derecha)."""
    rng = np.random.default_rng(sem)
    top = base - alto
    tono = rng.uniform(0.14, 0.24) if tipo != "cristal" else 0.10
    # cara lateral (volumen) con tramado
    lx = x + ancho if luz_lado < 0 else x - prof_lado
    lado = [(lx, top + 10), (lx + prof_lado, top), (lx + prof_lado, base), (lx, base)] if luz_lado < 0 else \
        [(lx, top), (lx + prof_lado, top + 10), (lx + prof_lado, base), (lx, base)]
    L.poli(lado, tono * 0.45, tex=0.1)
    L.trama(lado, ang=60, sep=6, tono=0.02, alfa=0.55)
    # fachada
    fach = [(x, top), (x + ancho, top), (x + ancho, base), (x, base)]
    if tipo == "deco":
        esc = [(x, top + 120), (x + ancho * 0.12, top + 120), (x + ancho * 0.12, top + 60), (x + ancho * 0.28, top + 60),
               (x + ancho * 0.28, top), (x + ancho * 0.72, top), (x + ancho * 0.72, top + 60), (x + ancho * 0.88, top + 60),
               (x + ancho * 0.88, top + 120), (x + ancho, top + 120), (x + ancho, base), (x, base)]
        fach = esc
        cx = x + ancho / 2
        L.poli([(cx - ancho * 0.18, top), (cx, top - ancho * 0.9), (cx + ancho * 0.18, top)], tono * 0.9, grad=(tono * 0.5, top - ancho, top))
        for k in range(5):                                  # arcos de la corona (tipo Chrysler)
            yk = top - ancho * 0.15 * k
            rw = ancho * 0.18 * (1 - k / 6)
            L.linea([(cx - rw, yk), (cx, yk - rw * 0.9), (cx + rw, yk)], 2.0, 0.55, alfa=0.7, jit=0.2)
            for j in range(-2, 3):
                L.poli([(cx + j * rw * 0.35 - 2, yk - rw * 0.5 + abs(j) * 4), (cx + j * rw * 0.35 + 2, yk - rw * 0.5 + abs(j) * 4),
                        (cx + j * rw * 0.35, yk - rw * 0.62 + abs(j) * 4)], 0.7, alfa=0.7)
        L.linea([(cx, top - ancho * 0.9), (cx, top - ancho * 1.5)], 3, 0.05)
    L.poli(fach, tono, tex=0.12, grad=(tono * 0.55, top, base))
    L.linea(fach, 2.6, 0.02, cerrado=True, sem=sem)
    if tipo == "cristal":
        _cristal(L, x, top, ancho, alto, base, rng, encendidas, detalle)
        return
    # cornisa y friso con brillo de luna en el borde superior
    L.rect(x - 10, top - 4, ancho + 20, 16, tono * 1.6, tex=0.08)
    L.linea([(x - 10, top - 4), (x + ancho + 10, top - 4)], 2, 0.6, alfa=0.7, jit=0.2)
    L.linea([(x - 10, top + 12), (x + ancho + 10, top + 12)], 2, 0.02)
    for bx in np.arange(x - 6, x + ancho + 6, 14):
        L.rect(bx, top + 12, 6, 8, tono * 0.6)
    # ladrillo: hiladas tenues
    if tipo in ("ladrillo", "tienda") and detalle > 0.5:
        for yy in np.arange(top + 30, base, 9):
            if rng.uniform() < 0.55:
                xa = x + rng.uniform(0, ancho * 0.6)
                L.linea([(xa, yy), (xa + rng.uniform(20, 80), yy)], 1.0, 0.04, alfa=0.35, jit=0.3)
    # ventanas
    vw, vh = rng.uniform(26, 36), rng.uniform(46, 58)
    cols = max(2, int((ancho - 30) // (vw * 2.0)))
    gapx = (ancho - cols * vw) / (cols + 1)
    piso = vh * 1.75
    y_ini = top + (130 if tipo == "deco" else 50)
    y_fin = base - (170 if tipo == "tienda" else 40)
    nf = int((y_fin - y_ini) // piso)
    for f in range(nf):
        for c in range(cols):
            vx = x + gapx + c * (vw + gapx)
            vy = y_ini + f * piso
            enc = rng.uniform() < encendidas
            ventana(L, vx, vy, vw, vh, encendida=rng.uniform(0.5, 1.0) if enc else 0.0, rng=rng,
                    persiana=enc and rng.uniform() < 0.35, figura=enc and rng.uniform() < 0.2)
    if tipo == "ladrillo" and ancho > 180 and detalle > 0.5:
        escalera_incendio(L, x + ancho * 0.5 - 50, y_ini - 20, y_fin, w=100, piso=piso)
    if tipo in ("ladrillo", "tienda") and rng.uniform() < 0.6:
        tanque_agua(L, x + ancho * rng.uniform(0.25, 0.75), top - 50, r=rng.uniform(34, 50), alto=rng.uniform(60, 90))
    if tipo == "tienda":
        tienda(L, x, base, ancho, rng)


def _cristal(L, x, top, ancho, alto, base, rng, encendidas, detalle):
    """Rascacielos de vidrio (el laboratorio de IA): rejilla fina, plantas enteras encendidas con racks de servidores."""
    piso = 34
    nf = int(alto // piso)
    for f in range(nf):
        y = top + f * piso
        enc = rng.uniform() < encendidas * (1.8 if f < nf * 0.35 else 0.8)
        if enc:
            L.rect(x + 3, y + 4, ancho - 6, piso - 8, 0.72, tex=0.04, grad=(0.55, y, y + piso), emis=0.6)
            if detalle > 0.5:
                for rx in np.arange(x + 14, x + ancho - 20, 26):       # racks de servidores a contraluz
                    L.rect(rx, y + 8, 14, piso - 14, 0.08, tex=0.0)
                    for ly in np.arange(y + 11, y + piso - 8, 5):
                        if rng.uniform() < 0.4:
                            L.rect(rx + 3, ly, 3, 2, 0.95, tex=0.0, emis=0.9)
            L.brillo(x + ancho / 2, y + piso / 2, ancho * 0.7, 0.10, ry=piso * 1.2, tono=0.7)
        L.linea([(x, y), (x + ancho, y)], 1.3, 0.03, jit=0)
    for vx in np.arange(x, x + ancho, 18):
        L.linea([(vx, top), (vx, base)], 1.0, 0.03, alfa=0.7, jit=0)
    L.poli([(x, top), (x + ancho * 0.45, top), (x, top + alto * 0.5)], 0.3, alfa=0.18, tex=0.0)     # reflejo de la luna
    L.poli([(x + ancho * 0.3, top), (x + ancho * 0.7, top), (x + ancho * 0.6, top - 70), (x + ancho * 0.4, top - 70)], 0.08)
    L.linea([(x + ancho / 2, top - 70), (x + ancho / 2, top - 260)], 4, 0.03)
    L.linea([(x + ancho / 2 - 24, top - 160), (x + ancho / 2 + 24, top - 160)], 2, 0.03)


def tienda(L, x, base, ancho, rng, nombre=None):
    """Planta baja: escaparate encendido, toldo a rayas, puerta con escalón."""
    y = base - 150
    L.rect(x, y - 10, ancho, 160, 0.10, tex=0.1)
    ew = ancho * 0.62
    L.rect(x + 14, y + 16, ew, 112, 0.62, tex=0.06, grad=(0.85, y + 16, y + 128), emis=0.5)
    L.brillo(x + 14 + ew / 2, y + 80, ew * 0.7, 0.25, ry=80, tono=0.75)
    for k in range(1, 4):
        L.linea([(x + 14 + ew * k / 4, y + 16), (x + 14 + ew * k / 4, y + 128)], 2, 0.03, jit=0.2)
    L.linea([(x + 14, y + 16), (x + 14 + ew, y + 16), (x + 14 + ew, y + 128), (x + 14, y + 128)], 2.5, 0.02, cerrado=True)
    # toldo
    tw = ew + 30
    tol = [(x + 4, y - 4), (x + 4 + tw, y - 4), (x + 4 + tw + 20, y + 34), (x - 16, y + 34)]
    L.poli(tol, 0.30, tex=0.08)
    for k in range(int(tw // 26) + 1):
        a = x + 4 + k * 26
        L.poli([(a, y - 4), (a + 13, y - 4), (a + 13 + 20 * (a - x) / tw, y + 34), (a + 20 * (a - x) / tw, y + 34)], 0.12)
    L.linea(tol, 2, 0.02, cerrado=True)
    # puerta
    px = x + ew + 30
    L.rect(px, y + 20, ancho - ew - 44, 130, 0.05, tex=0.1)
    L.rect(px + 8, y + 30, ancho - ew - 60, 40, 0.4, tex=0.05)
    L.rect(px - 6, base - 8, ancho - ew - 32, 8, 0.25)


def texto_lienzo(L, s, x, y, px, tono=0.05, fuente="C:/Windows/Fonts/impact.ttf", alfa=1.0, track=2.0, centro=True):
    """Letras pintadas/talladas en el lienzo (letreros, fachadas). (x, y) = centro (o esquina) en el mundo."""
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(fuente, int(px))
    w = int(sum(f.getlength(c) + track for c in s)) + 10
    im = Image.new("L", (w, int(px * 1.4)), 0)
    d = ImageDraw.Draw(im)
    xx = 5
    for c in s:
        d.text((xx, 0), c, font=f, fill=255)
        xx += f.getlength(c) + track
    m = np.asarray(im, np.float32) / 255.0
    x0 = int(x - (m.shape[1] / 2 if centro else 0) - L.ox)
    y0 = int(y - (m.shape[0] / 2 if centro else 0) - L.oy)
    xa, ya = max(0, x0), max(0, y0)
    xb, yb = min(L.w, x0 + m.shape[1]), min(L.h, y0 + m.shape[0])
    if xb <= xa or yb <= ya:
        return
    L._mezclar(m[ya - y0:yb - y0, xa - x0:xb - x0], xa, ya, tono, alfa, 0.0, 0.0)


def letrero_vertical(L, x, y, s="HOTEL", ancho=70, px=58, encendido=0.9):
    """Letrero vertical de bombillas (hotel): caja oscura, letras claras, bombillas en el borde y brazo a la pared."""
    alto = len(s) * px * 1.05 + 40
    L.rect(x, y, ancho, alto, 0.08, tex=0.08)
    L.linea([(x, y), (x + ancho, y), (x + ancho, y + alto), (x, y + alto)], 2.5, 0.02, cerrado=True)
    for k, c in enumerate(s):
        texto_lienzo(L, c, x + ancho / 2, y + 30 + k * px * 1.05, px, tono=0.55 + 0.4 * encendido)
    for k in range(int(alto // 18)):
        for bx in (x + 8, x + ancho - 8):
            L.elipse(bx, y + 10 + k * 18, 3, 3, 0.85 * encendido + 0.1, emis=0.9 * encendido)
    L.brillo(x + ancho / 2, y + alto / 2, ancho * 1.4, 0.22 * encendido, ry=alto * 0.6, tono=0.7)
    L.linea([(x + ancho, y + 30), (x + ancho + 40, y + 20)], 4, 0.03)
    L.linea([(x + ancho, y + alto - 30), (x + ancho + 40, y + alto - 20)], 4, 0.03)


def farola(L, x, base, alto=520, brazo=60):
    """Farola de hierro fundido: base moldurada, fuste con anillos, farol de cristal colgado de un brazo curvo."""
    L.poli([(x - 22, base), (x + 22, base), (x + 14, base - 40), (x - 14, base - 40)], 0.07)
    L.poli([(x - 7, base - 40), (x + 7, base - 40), (x + 5, base - alto), (x - 5, base - alto)], 0.06,
           grad=(0.12, base - alto, base))
    for k in (60, 70, alto - 30):
        L.rect(x - 10, base - k, 20, 6, 0.10)
    L.linea([(x - 22, base), (x + 22, base), (x + 14, base - 40), (x - 14, base - 40)], 2, 0.02, cerrado=True)
    a = np.array([[x, base - alto + 10], [x - brazo * 0.3, base - alto - 30], [x - brazo, base - alto - 20],
                  [x - brazo, base - alto + 10]])
    L.linea(a, 5, 0.04)
    fx, fy = x - brazo, base - alto + 10
    L.poli([(fx - 20, fy), (fx + 20, fy), (fx + 15, fy + 46), (fx - 15, fy + 46)], 0.95, tex=0.0, emis=1.0)
    L.poli([(fx - 26, fy), (fx, fy - 18), (fx + 26, fy)], 0.06)
    L.linea([(fx - 20, fy), (fx + 20, fy), (fx + 15, fy + 46), (fx - 15, fy + 46)], 2.5, 0.02, cerrado=True)
    L.linea([(fx, fy), (fx, fy + 46)], 1.5, 0.3, jit=0)
    L.brillo(fx, fy + 24, 60, 0.6, tono=1.0)
    return fx, fy + 30


def bolsa(L, x, base, ancho=1200, alto=760):
    """Fachada neoclásica de la bolsa de valores: escalinata, columnas estriadas, entablamento con letras talladas y frontón."""
    top = base - alto
    L.rect(x, top, ancho, alto, 0.30, tex=0.1, grad=(0.18, top, base))
    for k in range(5):                                              # escalinata
        L.rect(x - 20 - k * 12, base - 60 + k * 12, ancho + 40 + k * 24, 12, 0.38 - k * 0.03, tex=0.06)
        L.linea([(x - 20 - k * 12, base - 60 + k * 12), (x + ancho + 20 + k * 12, base - 60 + k * 12)], 1.5, 0.03, jit=0.3)
    nc = 8
    for k in range(nc):                                             # columnas con sombra y estrías
        cx = x + 80 + k * (ancho - 160) / (nc - 1)
        L.rect(cx - 34, top + 210, 68, alto - 270, 0.62, tex=0.06)
        L.rect(cx + 8, top + 210, 26, alto - 270, 0.36, tex=0.06)
        for e in range(-3, 4):
            L.linea([(cx + e * 9, top + 214), (cx + e * 9, base - 64)], 1.2, 0.25, alfa=0.6, jit=0)
        L.rect(cx - 44, top + 192, 88, 20, 0.6)
        L.rect(cx - 42, base - 80, 84, 18, 0.55)
        L.linea([(cx - 34, top + 210), (cx - 34, base - 62)], 2, 0.03, jit=0.3)
        L.linea([(cx + 34, top + 210), (cx + 34, base - 62)], 2, 0.03, jit=0.3)
    for k in range(nc - 1):                                         # puertas oscuras con luz tenue
        cx = x + 80 + (k + 0.5) * (ancho - 160) / (nc - 1)
        L.rect(cx - 30, top + 380, 60, alto - 440, 0.06, tex=0.1)
        if k % 2 == 1:
            L.rect(cx - 24, top + 390, 48, 70, 0.6, tex=0.05)
    L.rect(x - 30, top + 100, ancho + 60, 92, 0.55, tex=0.08)        # entablamento
    texto_lienzo(L, "BOLSA DE VALORES", x + ancho / 2, top + 146, 64, tono=0.08, fuente="C:/Windows/Fonts/timesbd.ttf", track=14)
    L.poli([(x - 50, top + 100), (x + ancho / 2, top - 120), (x + ancho + 50, top + 100)], 0.45, tex=0.08)
    L.poli([(x + 40, top + 86), (x + ancho / 2, top - 92), (x + ancho - 40, top + 86)], 0.25, tex=0.1)
    L.linea([(x - 50, top + 100), (x + ancho / 2, top - 120), (x + ancho + 50, top + 100), (x - 50, top + 100)], 3, 0.02)
    L.linea([(x - 50, top + 100), (x + ancho / 2, top - 120)], 2.0, 0.85, alfa=0.6, jit=0.3)       # luna en el frontón
