# -*- coding: utf-8 -*-
"""Kit del estilo NOIR (cine negro en tinta y aguada, novela gráfica vintage): SOLO blanco y negro de alto contraste, claroscuro,
lluvia que solo brilla donde hay luz, niebla volumétrica, humo de cigarro, sombras de persiana, relámpagos, papel, grano y polvo
de película. Se apoya en nucleo/toon.py (tinta que se redibuja a 12 dibujos/s, formas, cámara con capas, luces).

    h = Noir()                                   # una por proceso (subclase de Toon)
    h.nuevo(t, fondo)                            # fondo float32 HxWx3 (grises) o None
    h.forma(P, gris(120), sombra=gris(60))       # todo lo de toon.Toon, con colores grises
    h.luz_cono(...); h.luz_persiana(quad, ...)   # luces: se MULTIPLICAN sobre el cuadro (claroscuro)
    A = h.aditivo()                              # capa de lo que BRILLA con la luz (lluvia, humo, polvo): dibujar con lluvia()/humo()
    img = h.acabado(t, niebla=..., flash=...)    # luz, niebla, tinta, curva, papel, grano, polvo, viñeta -> float32 HxWx3 gris

Transiciones entre escenas (plano secuencia, sin cortes duros): tinta_cubre(img, p) — una mancha de tinta que se extiende.
Rótulos: texto_maquina() (máquina de escribir, letra a letra) y sello() (tampón de goma entintado).
Conceptos y receta: docs/estilo_noir.md.
"""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from motor import FPS, H, W, clamp01, e_inout, e_out, prog, smooth
import toon as TN
from toon import Toon

SW, SH = W // 3, H // 3          # resolución del mapa de luz
AW, AH = W // 2, H // 2          # resolución de la capa aditiva (lluvia/humo)
FUENTE_MAQ = "C:/Windows/Fonts/courbd.ttf"
FUENTE_MAQ_R = "C:/Windows/Fonts/cour.ttf"
FUENTE_SELLO = "C:/Windows/Fonts/impact.ttf"


def gris(v):
    v = int(max(0, min(255, v)))
    return (v, v, v)


# ================================================================ ruido y texturas (en caché por proceso)
def fbm(w, h, esc, octavas=4, sem=0, ganancia=0.5):
    """Ruido fractal suave float32 (h, w) normalizado a desviación 1."""
    rng = np.random.default_rng(sem)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octavas):
        gw = max(2, int(w / esc * 2 ** o)) + 1
        gh = max(2, int(h / esc * 2 ** o)) + 1
        g = rng.standard_normal((gh, gw)).astype(np.float32)
        out += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= ganancia
    out /= tot
    return out / (out.std() + 1e-9)


@functools.lru_cache(maxsize=1)
def papel():
    """Multiplicador de papel (≈1): fibras, grumos de pulpa y manchas suaves de agua."""
    rng = np.random.default_rng(31)
    base = 0.022 * fbm(W, H, 260, 5, 11) + 0.012 * fbm(W, H, 24, 2, 12)
    fib = rng.standard_normal((H // 2, W // 10)).astype(np.float32)
    fib = cv2.resize(fib, (W, H), interpolation=cv2.INTER_LINEAR)
    fib2 = cv2.resize(rng.standard_normal((H // 10, W // 2)).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    manchas = np.clip(fbm(W, H, 520, 3, 13) - 1.1, 0, None) * 0.05
    return (1 + base + 0.008 * fib + 0.008 * fib2 - manchas).astype(np.float32)


@functools.lru_cache(maxsize=4)
def niebla_tex(sem=0):
    """Textura de niebla 2W x H (se desplaza con el tiempo)."""
    n = 0.6 * fbm(2 * SW, SH, 140, 4, 40 + sem) + 0.4 * fbm(2 * SW, SH, 50, 3, 50 + sem)
    return np.clip(0.5 + 0.28 * n, 0, 1).astype(np.float32)


@functools.lru_cache(maxsize=1)
def _vineta_noir():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.66)) ** 2)
    return np.clip(1 - 0.85 * np.clip(d - 0.38, 0, None) ** 1.6, 0.12, 1).astype(np.float32)


@functools.lru_cache(maxsize=3)
def _trama(fase=0):
    """Tramado de plumilla (líneas diagonales finas, ligeramente irregulares) en pantalla; la fase cambia con cada dibujo."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = np.random.default_rng(fase + 70)
    ond = cv2.resize(rng.standard_normal((H // 40 + 2, W // 40 + 2)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    u = (xx + yy + fase * 2.3 + ond * 1.6) / 6.5
    lin = np.clip(1.0 - np.abs((u - np.floor(u)) - 0.5) * 2 / 0.32, 0, 1)
    return lin.astype(np.float32)


@functools.lru_cache(maxsize=8)
def _patron(tipo, n, abierto):
    """Patrón de luz (256x256) que se proyecta en un cuadrilátero: persiana (listones), ventana (4 vidrios con marco) o liso."""
    p = np.zeros((256, 256), np.float32)
    if tipo == "persiana":
        per = 256 / n
        y = (np.arange(256) % per) / per
        p[:] = (y < abierto)[:, None]
        p[:, :5] = 0
        p[:, -5:] = 0
        p[:, 124:132] *= 0.0            # cordón central
    elif tipo == "ventana":
        p[:] = 1
        p[:, :10] = p[:, -10:] = 0
        p[:10] = p[-10:] = 0
        p[:, 122:134] = 0
        p[122:134] = 0
    else:
        p[:] = 1
    return p


# ================================================================ lienzo noir
class Noir(Toon):
    """Toon en grises con luces extra (cuadriláteros con patrón = persianas/ventanas proyectadas) y capa aditiva iluminada."""

    def nuevo(self, t, fondo=None, tinte=(1, 1, 1)):
        super().nuevo(t, fondo, tinte)
        self.ambiente = np.array([1.0, 1.0, 1.0], np.float32)
        self._extra = []
        self._fijas = []
        self._soportes = []
        self._A = None
        self._E = None

    def emisivo(self):
        """Capa de lo que EMITE luz (ventanas encendidas, letreros, faroles): se suma después del claroscuro; lo que se dibuja
        encima la tapa (ver _pintar)."""
        if self._E is None:
            self._E = np.zeros((H, W), np.float32)
        return self._E

    def _pintar(self, mk, x0, y0, c0, c1=None, grad=None, alfa=1.0, tex=0.03, tdesp=(0, 0)):
        super()._pintar(mk, x0, y0, c0, c1, grad, alfa, tex, tdesp)
        if self._E is not None:
            hh, ww = mk.shape
            self._E[y0:y0 + hh, x0:x0 + ww] *= 1 - mk.astype(np.float32) * (alfa / 255.0)

    def emitir(self, P, v, mundo=True, blur=1.0):
        """Pinta un polígono que emite luz (brasa, bombilla) con intensidad v."""
        Q = self.tf(P) if mundo else np.asarray(P, float)
        r = self.mascara([Q], m=4)
        if r is None:
            return
        mk, x0, y0 = r
        a = mk.astype(np.float32) / 255.0
        if blur > 0:
            a = cv2.GaussianBlur(a, (0, 0), blur)
        E = self.emisivo()
        sl = E[y0:y0 + a.shape[0], x0:x0 + a.shape[1]]
        np.maximum(sl, a * v, out=sl)

    # -------------------------------------------------------- luces
    def luz_persiana(self, quad, k=1.0, tipo="persiana", n=16, abierto=0.55, suave=1.6, mundo=True):
        """Luz con patrón proyectada en el cuadrilátero quad (4 puntos: sup-izq, sup-der, inf-der, inf-izq)."""
        Q = self.tf(quad) if mundo else np.asarray(quad, float)
        src = np.float32([[0, 0], [255, 0], [255, 255], [0, 255]])
        M = cv2.getPerspectiveTransform(src, np.float32(Q / 3.0))
        pat = cv2.warpPerspective(_patron(tipo, n, round(abierto, 2)), M, (SW, SH), flags=cv2.INTER_LINEAR)
        if suave > 0:
            pat = cv2.GaussianBlur(pat, (0, 0), suave)
        self._extra.append(pat * k)

    def luz_mascara(self, m, k=1.0):
        """Luz arbitraria (SH x SW o H x W)."""
        if m.shape[0] != SH:
            m = cv2.resize(m, (SW, SH), interpolation=cv2.INTER_AREA)
        self._extra.append(m * k)

    def mapa_gris(self):
        yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        xx *= 3
        yy *= 3
        L = np.full((SH, SW), float(self.ambiente[0]), np.float32)
        for lz in self.luces:
            if lz[0] == "r":
                _, x, y, r, col, k = lz
                d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / max(1.0, r)
                L += np.clip(1 - d, 0, 1) ** 2 * k * float(col[0])
            else:
                _, x, y, ang, abre, largo, col, k, suave = lz
                dx, dy = xx - x, yy - y
                d = np.sqrt(dx * dx + dy * dy) + 1e-3
                th = np.arccos(np.clip((dx * math.cos(ang) + dy * math.sin(ang)) / d, -1, 1))
                lat = np.clip((abre - th) / (abre * suave + 1e-4), 0, 1)
                lat = lat * lat * (3 - 2 * lat)
                lon = np.clip(1 - d / largo, 0, 1) ** 0.8
                L += lat * lon * k * float(col[0])
        for e in self._extra:
            L += e
        for Q, v in self._fijas:                       # zonas con luz FIJA (rótulos): ni se queman bajo un foco ni se pierden a oscuras
            cv2.fillConvexPoly(L, Q, float(v), cv2.LINE_AA)
        return L

    def luz_fija(self, quad, v=1.0, mundo=True):
        """Fija la iluminación dentro del cuadrilátero a v, ignorando ambiente y luces (para rótulos de énfasis)."""
        Q = self.tf(quad) if mundo else np.asarray(quad, float)
        self._fijas.append(((Q / 3.0).astype(np.int32), v))

    # -------------------------------------------------------- piezas con claroscuro de novela gráfica
    @staticmethod
    def _banda(mk, dx, dy, blur=1.0):
        """Parte de la máscara que NO cubre su copia desplazada (dx, dy): media luna del lado (+dx, +dy)."""
        dx, dy = int(round(dx)), int(round(dy))
        m = 3 + max(abs(dx), abs(dy))
        hh, ww = mk.shape
        big = np.zeros((hh + 2 * m, ww + 2 * m), np.uint8)
        big[m:m + hh, m:m + ww] = mk
        sh = cv2.warpAffine(big, np.float32([[1, 0, -dx], [0, 1, -dy]]), (ww + 2 * m, hh + 2 * m), flags=cv2.INTER_LINEAR)
        b = cv2.subtract(big, sh)[m:m + hh, m:m + ww]
        if blur > 0:
            b = cv2.GaussianBlur(b, (0, 0), blur)
        return cv2.bitwise_and(b, mk)

    def pieza(self, P, tono, sem=0, w=7.0, luz=(0.25, -1.0), d=22.0, sombra=0.6, trama=0.75, rim=0.0, rim_tono=238,
              tex=0.06, linea=True, jit=2.0, alfa=1.0, sketch=0.25, grad=None):
        """Forma de novela gráfica: aguada de tinta (tono con grano de pigmento), sombra del lado contrario a la luz con TRAMADO
        de plumilla, borde de contraluz (rim) del lado de la luz y contorno de tinta. P en el MUNDO; luz = dirección HACIA la luz."""
        Pw = self.tf(P)
        Pj = self._jit(TN._remu(Pw, 4.0, True)[:-1] if len(Pw) > 8 else Pw, jit * self.zoom, sem)
        o = (1.5 * math.sin(self.dib * 2.1 + sem), 1.5 * math.cos(self.dib * 1.7 + sem * 2))
        g = None if grad is None else (gris(grad[0]), grad[1], grad[2])
        r = self.relleno(Pj, gris(tono), grad=g, alfa=alfa, tex=tex, off=o)
        if r is not None and self.silueta is None:
            mk, x0, y0 = r
            ln = math.hypot(*luz) + 1e-9
            lx, ly = luz[0] / ln, luz[1] / ln
            dz = d * self.zoom
            if sombra > 0:
                b = self._banda(mk, -lx * dz, -ly * dz, 1.2)
                self._pintar(b, x0, y0, gris(tono * 0.42), alfa=sombra * alfa, tex=0.03)
                if trama > 0:                                       # tramado de plumilla en la penumbra
                    b2 = self._banda(mk, -lx * dz * 1.9, -ly * dz * 1.9, 1.0)
                    tr = _trama(self.dib % 3)[y0:y0 + mk.shape[0], x0:x0 + mk.shape[1]]
                    hb = (b2.astype(np.float32) * tr[:b2.shape[0], :b2.shape[1]]).astype(np.uint8)
                    self._pintar(hb, x0, y0, gris(10), alfa=trama * alfa, tex=0.0)
            if rim > 0:
                rb = self._banda(mk, lx * dz * 0.32, ly * dz * 0.32, 0.8)
                self._pintar(rb, x0, y0, gris(rim_tono), alfa=rim * alfa, tex=0.0)
        if linea and w > 0:
            self.anillo(Pj, w, sem, color=(10, 10, 10), alfa=alfa, peso_luz=0.6, jit=0.0, sketch=sketch)
        return r

    # -------------------------------------------------------- capa aditiva (lo que brilla con la luz)
    def aditivo(self):
        if self._A is None:
            self._A = np.zeros((AH, AW), np.float32)
        return self._A

    def a_pant(self, P):
        """Mundo -> coordenadas de la capa aditiva (media resolución)."""
        return self.tf(P) * 0.5

    # -------------------------------------------------------- acabado
    def acabado(self, t, *, negro=0.03, blanco=0.94, contraste=5.5, medio=0.46, tinta=0.55, niebla=None, brillo_A=1.0,
                A_base=0.05, bloom=0.35, grano=0.07, polvo=1.0, vin=1.0, flash=0.0, parpadeo=0.02, oscuro=1.0):
        img = self.img
        lum = img[..., 0] * 0.3 + img[..., 1] * 0.59 + img[..., 2] * 0.11
        L3 = self.mapa_gris()
        L = cv2.resize(L3, (W, H), interpolation=cv2.INTER_LINEAR)
        lum = lum * L
        if self._E is not None:
            lum = lum + self._E
        if niebla is not None:                         # niebla volumétrica: brilla donde hay luz
            dens, vel, y0, y1 = niebla.get("dens", 0.3), niebla.get("vel", 30.0), niebla.get("y0", 0), niebla.get("y1", H)
            tx = niebla_tex(niebla.get("sem", 0))
            off = int(t * vel / 3) % SW
            n = tx[:, off:off + SW]
            yy = np.arange(SH, dtype=np.float32)[:, None] * 3
            g = np.clip((yy - y0) / max(1.0, (y1 - y0)), 0, 1)
            g = g * g * (3 - 2 * g) if niebla.get("sube", True) else 1 - g
            d3 = np.clip(dens * n * (0.35 + 0.65 * g) * 1.6, 0, 0.9)
            f3 = d3 * (niebla.get("tono", 0.10) + 0.75 * np.clip(L3 - 0.12, 0, None))
            d = cv2.resize(d3, (W, H), interpolation=cv2.INTER_LINEAR)
            f = cv2.resize(f3, (W, H), interpolation=cv2.INTER_LINEAR)
            lum = lum * (1 - d) + f
        if self._A is not None:                        # lluvia, humo, polvo: visibles en proporción a la luz
            A = cv2.GaussianBlur(self._A, (0, 0), 0.7)
            A = cv2.resize(A, (W, H), interpolation=cv2.INTER_LINEAR)
            lum = lum + A * brillo_A * (A_base + 0.9 * np.clip(L - 0.1, 0, 1.6))
        if bloom > 0:
            br = np.clip(lum - 0.72, 0, None)
            g = cv2.GaussianBlur(cv2.resize(br, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 9)
            lum = lum + cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR) * bloom * 2.2
        if tinta > 0:                                  # tinta: bordes nítidos y oscuros (pigmento que se acumula en el borde)
            b = cv2.GaussianBlur(lum, (0, 0), 2.4)
            lum = lum + tinta * (lum - b)
            b2 = cv2.GaussianBlur(lum, (0, 0), 9)
            lum = lum + 0.25 * tinta * (lum - b2)
        x = np.clip(lum, 0, 1.4)
        y = 1 / (1 + np.exp(-contraste * (x - medio)))     # curva S: negros profundos, altas luces que queman
        y0, y1 = 1 / (1 + math.exp(contraste * medio)), 1 / (1 + math.exp(-contraste * (1.4 - medio)))
        y = (y - y0) / (y1 - y0)
        if flash > 0:
            y = y + flash * (1 - y) * 0.85
        out = negro + (blanco - negro) * y
        out *= papel()
        if grano > 0:
            gr = TN._banco_grano()[int(t * 24) % 6]
            out += grano * 0.55 * gr * (0.35 + 0.65 * out * (1 - out) * 4)
        if parpadeo > 0:
            out *= 1 + parpadeo * math.sin(t * 24 * 2.1) * math.sin(t * 7.3)
        if polvo > 0:
            _polvo(out, t, polvo)
        if vin > 0:
            out *= 1 - vin * (1 - _vineta_noir())
        if oscuro < 1:
            out *= oscuro
        np.clip(out, 0, 1, out=out)
        return np.repeat(out[..., None], 3, axis=2)


def _polvo(out, t, k):
    """Motas y pelos de película (blancos y negros) a 12 cuadros/s; de vez en cuando, una raya vertical."""
    c = int(t * 12)
    rng = np.random.default_rng(c * 7919 + 17)
    for _ in range(int(rng.integers(2, 7) * k)):
        x, y = int(rng.uniform(0, W)), int(rng.uniform(0, H))
        r = float(rng.uniform(1.0, 3.2))
        v = 0.95 if rng.uniform() < 0.5 else 0.04
        cv2.circle(out, (x, y), int(r), v, -1, cv2.LINE_AA)
    if rng.uniform() < 0.25 * k:
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        P = np.array([[x + 18 * math.sin(a * 3) + a * 30, y + a * 26] for a in np.linspace(0, 1.4, 9)], np.int32)
        cv2.polylines(out, [P], False, 0.05, 1, cv2.LINE_AA)
    if rng.uniform() < 0.18 * k:
        x = int(rng.uniform(80, W - 80))
        cv2.line(out, (x, 0), (x + int(rng.uniform(-6, 6)), H), 0.85 if rng.uniform() < 0.6 else 0.1, 1, cv2.LINE_AA)


# ================================================================ atmósfera (dibuja en la capa aditiva)
def lluvia(h, t, n=700, capas=(0.45, 0.75, 1.0), viento=0.16, k=1.0, sem=0, caja=None, vel=1500.0):
    """Lluvia en 3 profundidades (la cercana más rápida, larga y brillante). Solo se ve donde hay luz (la multiplica el acabado).
    caja = (x0, y0, x1, y1) en pantalla para limitarla (p. ej. detrás de una ventana)."""
    A = h.aditivo()
    x0, y0, x1, y1 = caja if caja else (0, 0, W, H)
    zoom, cx, cy, _ = h._cam
    for ci, d in enumerate(capas):
        rng = np.random.default_rng(sem * 101 + ci * 7 + 3)
        m = int(n * (0.6 + 0.6 * (1 - d)))
        bx = rng.uniform(0, 1, m)
        by = rng.uniform(0, 1, m)
        v = vel * (0.55 + 0.6 * d) * rng.uniform(0.85, 1.15, m)
        alto = (y1 - y0) + 200
        y = (by * alto + v * t) % alto + y0 - 100
        par = (cx - W / 2) * (0.2 + 0.8 * d) * zoom
        x = x0 + ((bx * (x1 - x0 + 300) - par + viento * y) % (x1 - x0 + 300)) - 150
        largo = v * (1 / 48.0) * (0.8 + 0.6 * d)
        dxl = viento * largo
        brillo = k * (0.10 + 0.20 * d)
        grosor = 1
        P0 = np.stack([x, y], 1) * 0.5
        P1 = np.stack([x + dxl, y + largo], 1) * 0.5
        for a, b in zip(P0, P1):
            cv2.line(A, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), brillo, grosor, cv2.LINE_AA)


def salpicaduras(h, t, y0, y1, x0=0, x1=W, n=60, k=1.0, sem=0, ritmo=2.2):
    """Gotas que revientan en el suelo mojado (anillos que crecen y se apagan) en la franja y0..y1 (pantalla)."""
    A = h.aditivo()
    for i in range(n):
        rr = np.random.default_rng(sem * 977 + i)
        f, ph = rr.uniform(0.7, 1.3) * ritmo, rr.uniform(0, 1)
        u = t * f + ph
        c = int(u)
        fr = u - c
        if fr > 0.35:
            continue
        r2 = np.random.default_rng((sem * 977 + i) * 131 + c)
        x = r2.uniform(x0, x1)
        y = r2.uniform(y0, y1)
        persp = 0.4 + 0.6 * (y - y0) / max(1, y1 - y0)
        a = fr / 0.35
        rx = (3 + 16 * a) * persp
        cv2.ellipse(A, (int(x * 0.5), int(y * 0.5)), (max(1, int(rx * 0.5)), max(1, int(rx * 0.16))), 0, 0, 360,
                    k * 0.5 * (1 - a), 1, cv2.LINE_AA)
        if a < 0.3:                                   # coronita de la gota
            cv2.line(A, (int(x * 0.5), int(y * 0.5)), (int(x * 0.5), int((y - 10 * persp) * 0.5)), k * 0.4 * (1 - a / 0.3), 1,
                     cv2.LINE_AA)


def humo(h, t, x, y, k=1.0, sem=0, viento=(22.0, -70.0), vida=3.6, hebras=3, ancho=1.0, emite=1.0, t_ini=-99.0):
    """Humo de cigarro que sube enroscándose desde (x, y) del mundo: hebras finas que se abren, ondulan y se deshacen.
    Todo es función de t (sin estado): cada hebra es la curva de las partículas emitidas en los últimos `vida` segundos."""
    A = h.aditivo()
    z = h.zoom
    for s in range(hebras):
        edades = np.linspace(0.0, vida, 48)
        te = t - edades                                   # instante de emisión de cada partícula
        vivo = te >= t_ini
        fase = sem * 1.7 + s * 2.1
        sway = (8 + 34 * edades ** 1.2) * ancho
        px = x + viento[0] * edades + sway * np.sin(1.3 * te + 2.2 * edades + fase) \
            + 0.5 * sway * np.sin(2.9 * te - 1.1 * edades + fase * 1.3)
        py = y + viento[1] * edades - 9 * edades ** 2 + 6 * np.sin(1.7 * te + fase)
        P = h.a_pant(np.stack([px, py], 1))
        for i in range(len(P) - 1):
            if not (vivo[i] and vivo[i + 1]):
                continue
            e = edades[i] / vida
            a = k * emite * (0.55 * (1 - e) ** 1.6) * min(1.0, edades[i] * 6 + 0.25)
            if a < 0.01:
                continue
            g = max(1, int((1 + 5 * e) * z * ancho))
            cv2.line(A, (int(P[i, 0]), int(P[i, 1])), (int(P[i + 1, 0]), int(P[i + 1, 1])), a, g, cv2.LINE_AA)


def motas(h, t, n=90, k=0.6, sem=0, caja=None):
    """Polvo suspendido que flota lento (se ve solo en los haces de luz)."""
    A = h.aditivo()
    x0, y0, x1, y1 = caja if caja else (0, 0, W, H)
    rng = np.random.default_rng(sem + 555)
    bx, by = rng.uniform(0, 1, n), rng.uniform(0, 1, n)
    ph = rng.uniform(0, 6.28, n)
    x = x0 + (bx * (x1 - x0) + 14 * np.sin(0.3 * t + ph) + 6 * t) % (x1 - x0)
    y = y0 + (by * (y1 - y0) + 10 * np.sin(0.23 * t + 2 * ph) - 4 * t) % (y1 - y0)
    for xi, yi, p in zip(x, y, ph):
        cv2.circle(A, (int(xi * 0.5), int(yi * 0.5)), 1, k * (0.5 + 0.5 * math.sin(t * 1.3 + p)), -1, cv2.LINE_AA)


def relampago(t, eventos, dur=0.55):
    """Intensidad del destello (0..1) para una lista de instantes: doble golpe y caída."""
    v = 0.0
    for t0 in eventos:
        u = t - t0
        if 0 <= u < dur:
            v = max(v, math.exp(-u * 9) + 0.7 * math.exp(-max(0.0, u - 0.12) * 12) * (u > 0.12))
    return min(1.0, v)


def gotas_vidrio(h, t, caja, n=70, k=1.0, sem=0):
    """Gotas en un vidrio (pantalla): unas quietas, otras que resbalan dejando estela."""
    A = h.aditivo()
    x0, y0, x1, y1 = caja
    for i in range(n):
        r = np.random.default_rng(sem * 313 + i)
        x = r.uniform(x0, x1)
        rad = r.uniform(2, 7)
        if r.uniform() < 0.35:
            vel = r.uniform(40, 160)
            per = (y1 - y0) / vel + r.uniform(1, 4)
            u = (t + r.uniform(0, per)) % per
            y = y0 + vel * u
            if y > y1:
                continue
            x += 6 * math.sin(y * 0.03 + i)
            cv2.line(A, (int(x * 0.5), int(max(y0, y - 120) * 0.5)), (int(x * 0.5), int(y * 0.5)), 0.12 * k, 1, cv2.LINE_AA)
        else:
            y = r.uniform(y0, y1)
        cv2.circle(A, (int(x * 0.5), int(y * 0.5)), max(1, int(rad * 0.5)), 0.35 * k, 1, cv2.LINE_AA)
        cv2.circle(A, (int((x - rad * 0.3) * 0.5), int((y - rad * 0.3) * 0.5)), 1, 0.7 * k, -1, cv2.LINE_AA)


# ================================================================ reflejos en el suelo mojado
def reflejo(img, y_suelo, k=0.45, y_fin=H, onda=3.0, t=0.0, desv=2.0):
    """Refleja lo que hay sobre y_suelo (pantalla) en el suelo mojado: espejo vertical, ondulado y estirado."""
    ys = int(y_suelo)
    if ys <= 0 or ys >= H - 2:
        return img
    alto = min(H - ys, ys)
    arr = img[ys - alto:ys][::-1]
    yy = np.arange(alto, dtype=np.float32)
    mapx = (np.arange(W, dtype=np.float32)[None, :] + onda * np.sin(yy[:, None] * 0.09 + t * 3.1)
            * (0.3 + yy[:, None] / alto)).astype(np.float32)
    mapy = np.repeat(yy[:, None], W, 1).astype(np.float32)
    ref = cv2.remap(np.ascontiguousarray(arr), mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    ref = cv2.GaussianBlur(ref, (0, 0), sigmaX=desv * 0.6, sigmaY=desv * 2.5)
    fade = (k * np.clip(1 - yy / max(1, alto) * 1.2, 0, 1))[:, None]
    if img.ndim == 3:
        fade = fade[..., None]
    y2 = min(H, ys + alto, y_fin)
    seg = img[ys:y2]
    seg += (ref[:y2 - ys] - seg * 0.0) * fade[:y2 - ys] * 1.0 - seg * fade[:y2 - ys] * 0.35
    return img


# ================================================================ texto (máquina de escribir y sello)
@functools.lru_cache(maxsize=64)
def _txt_img(s, px, fuente, track):
    f = ImageFont.truetype(fuente, int(px))
    w = int(sum(f.getlength(c) + track for c in s)) + 20
    hgt = int(px * 1.5)
    im = Image.new("L", (w, hgt), 0)
    d = ImageDraw.Draw(im)
    x = 10
    xs = []
    for c in s:
        d.text((x, int(px * 0.15)), c, font=f, fill=255)
        xs.append(x)
        x += f.getlength(c) + track
    return np.asarray(im, np.float32) / 255.0, xs


MARGEN_TEXTO = 36


def _encuadrar(h, x, y, ancho, alto, centro, px):
    """Ajusta (x, y, px) del MUNDO para que el recuadro completo del texto quepa en pantalla con margen: si es más ancho que la
    pantalla se reduce; si se sale por un lado se desplaza hacia dentro (así ningún rótulo queda cortado)."""
    x0 = x - (ancho / 2 if centro else 0)
    y0 = y - (alto / 2 if centro else 0)
    P = h.tf(np.array([[x0, y0], [x0 + ancho, y0], [x0, y0 + alto], [x0 + ancho, y0 + alto]]))
    sx0, sx1, sy0, sy1 = P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max()
    m = MARGEN_TEXTO
    disp = W - 2 * m
    if sx1 - sx0 > disp:                                   # demasiado ancho: reducir
        k = disp / (sx1 - sx0)
        return _encuadrar(h, x, y, ancho * k, alto * k, centro, px * k)
    dx = (m - sx0) if sx0 < m else ((W - m - sx1) if sx1 > W - m else 0.0)
    dy = (m - sy0) if sy0 < m else ((H - m - sy1) if sy1 > H - m else 0.0)
    if sx1 < 0 or sx0 > W or sy1 < 0 or sy0 > H:          # fuera de cámara del todo (el plano no lo enseña): no tocar
        return x, y, px
    z = max(1e-3, h.zoom)
    return x + dx / z, y + dy / z, px


def soporte(h, cx, cy, w, hh, ang=0.0, s=1.0, margen=None):
    """Declara un SOPORTE de texto del cuadro actual (hoja, tarjeta, pantalla, cartel): rectángulo de w x hh (px locales, a escala
    s) centrado en (cx, cy) del MUNDO y girado ang. Todo texto_maquina() cuyo punto de anclaje caiga dentro se escribe PARALELO
    al soporte y se reduce para no pasarse de su borde (margen en px locales; por defecto 5 % del ancho). Lo llama K.hoja()."""
    h._soportes.append((float(cx), float(cy), float(w), float(hh), float(ang), float(s), 0.05 * w if margen is None else float(margen)))


def _soporte_en(h, x, y):
    """El último soporte declarado que contiene (x, y) -> (ang, lx, w, margen, s) con lx = x local respecto del centro; o None."""
    for cx, cy, w, hh, ang, s, m in reversed(getattr(h, "_soportes", ())):
        cs, sn = math.cos(-ang), math.sin(-ang)
        dx, dy = x - cx, y - cy
        lx, ly = (dx * cs - dy * sn) / s, (dx * sn + dy * cs) / s
        if abs(lx) <= w / 2 and abs(ly) <= hh / 2:
            return ang, lx, w, m, s
    return None


def texto_maquina(h, s, x, y, px, t, t0, cps=22.0, tono=0.08, alfa=1.0, centro=False, fuente=FUENTE_MAQ, track=1.0,
                  carro=True, borrar=None, encuadrar=True, ang=None, ancho_max=None):
    """Texto mecanografiado letra a letra desde t0 (cps = letras/s), con tinta irregular (cada tecla golpea distinto).
    (x, y) en coordenadas del MUNDO (esquina sup-izq o centro). borrar=(t1, dur): se borra (tachado y desvanecido).
    encuadrar: el texto COMPLETO se mantiene dentro de la pantalla (se desplaza o se reduce).
    ang: giro del renglón (rad, alrededor del anclaje); ancho_max: ancho disponible en px del mundo (se reduce si no cabe).
    Si no se dan y el anclaje cae sobre un soporte() declarado (una hoja), se toman de él: paralelo al papel y dentro de su borde."""
    if t < t0:
        return
    sop = _soporte_en(h, x, y) if (ang is None or ancho_max is None) else None
    if sop is not None:
        a_s, lx, w_s, m_s, s_s = sop
        if ang is None:
            ang = a_s
        if ancho_max is None:
            ancho_max = (2 * (w_s / 2 - abs(lx)) - 2 * m_s if centro else w_s / 2 - lx - m_s) * s_s
    ang = ang or 0.0
    if ancho_max is not None:
        imc, _ = _txt_img(s, px, fuente, track)
        k = max(ancho_max, 1.0) / max(1, imc.shape[1] - 20)
        if k < 1.0:
            px, track = px * k, track * k
    if encuadrar:
        imc, _ = _txt_img(s, px, fuente, track)
        x, y, px2 = _encuadrar(h, x, y, imc.shape[1], imc.shape[0], centro, px)
        if px2 < px * 0.999:
            track *= px2 / px
            px = px2
    zs = max(1.0, round(h.zoom * 2) / 2)
    im, xs = _txt_img(s, px * zs, fuente, track * zs)
    n = min(len(s), int((t - t0) * cps) + 1)
    if n <= 0:
        return
    corte = int(xs[n - 1] + (im.shape[1] - 10 - xs[n - 1] if n == len(s) else (xs[n] - xs[n - 1] if n < len(s) else 0))) + 2
    m = im[:, :max(1, corte)].copy()
    rng = np.random.default_rng(len(s) * 31 + int(px))
    for i in range(n):                                  # golpe de tecla irregular
        a = int(xs[i])
        b = int(xs[i + 1]) if i + 1 < len(xs) else m.shape[1]
        m[:, a:b] *= rng.uniform(0.72, 1.0)
        dy = int(rng.integers(-1, 2))
        if dy:
            m[:, a:b] = np.roll(m[:, a:b], dy, axis=0)
    if borrar is not None and t > borrar[0]:
        u = clamp01((t - borrar[0]) / borrar[1])
        yb = m.shape[0] // 2
        cv2.line(m, (6, yb), (int(6 + (m.shape[1] - 12) * min(1, u * 2)), yb + 2), 1.0, max(2, int(px * zs / 9)), cv2.LINE_AA)
        alfa *= 1 - clamp01(u * 2 - 1)
    _pegar_tinta(h, m, x - (m.shape[1] / zs / 2 if centro else 0), y - (m.shape[0] / zs / 2 if centro else 0), tono, alfa, zs,
                 ang=ang, piv=(x, y))


def sello(h, s, x, y, px, t, t0, rot=-8.0, tono=0.06, alfa=0.92, marco=True):
    """Tampón de goma: cae con un golpe (escala 1.4 -> 1) y deja tinta irregular con huecos. (x, y) = centro en el MUNDO."""
    if t < t0:
        return
    imc, _ = _txt_img(s, px, FUENTE_SELLO, 4.0)                 # que el sello entero quepa en pantalla
    anc = (imc.shape[1] + 0.7 * px) * 1.1
    alt = (imc.shape[0] + 0.7 * px) * 1.1 + abs(math.sin(math.radians(rot))) * imc.shape[1]
    x, y, px = _encuadrar(h, x, y, anc, alt, True, px)
    u = clamp01((t - t0) / 0.16)
    esc = 1.0 + 0.4 * (1 - u) ** 2
    zs = max(1.0, round(h.zoom * 2) / 2)
    px = px * zs
    im, _ = _txt_img(s, px, FUENTE_SELLO, 4.0 * zs)
    pad = int(px * 0.35)
    m = np.zeros((im.shape[0] + 2 * pad, im.shape[1] + 2 * pad), np.float32)
    m[pad:pad + im.shape[0], pad:pad + im.shape[1]] = im
    if marco:
        cv2.rectangle(m, (6, 6), (m.shape[1] - 7, m.shape[0] - 7), 1.0, max(3, int(px / 10)), cv2.LINE_AA)
    rng = np.random.default_rng(len(s) * 7 + 3)
    hue = cv2.resize(rng.uniform(0, 1, (m.shape[0] // 6 + 1, m.shape[1] // 6 + 1)).astype(np.float32), m.shape[::-1])
    m *= np.clip((hue - 0.18) * 3, 0.15, 1)
    hh, ww = m.shape
    M = cv2.getRotationMatrix2D((ww / 2, hh / 2), rot, esc)
    big = int(max(hh, ww) * 1.6)
    M[0, 2] += (big - ww) / 2
    M[1, 2] += (big - hh) / 2
    m2 = cv2.warpAffine(m, M, (big, big))
    _pegar_tinta(h, m2, x - big / zs / 2, y - big / zs / 2, tono, alfa * (0.4 + 0.6 * u), zs)


def _pegar_tinta(h, m, x, y, tono, alfa, zs=1.0, ang=0.0, piv=None):
    """Pega una máscara de tinta (rasterizada a zs píxeles por unidad del mundo) sobre el lienzo con la cámara actual.
    ang gira la máscara alrededor de piv (punto del mundo)."""
    M = h.M
    if ang and piv is not None:
        M = M @ TN.mat_t(piv[0], piv[1]) @ TN.mat_r(ang) @ TN.mat_t(-piv[0], -piv[1])
    M = M @ TN.mat_t(x, y) @ TN.mat_s(1.0 / zs)
    hh, ww = m.shape
    esq = np.array([[0, 0, 1], [ww, 0, 1], [0, hh, 1], [ww, hh, 1]], float) @ M[:2].T
    x0, y0 = int(max(0, math.floor(esq[:, 0].min()) - 2)), int(max(0, math.floor(esq[:, 1].min()) - 2))
    x1, y1 = int(min(W, math.ceil(esq[:, 0].max()) + 2)), int(min(H, math.ceil(esq[:, 1].max()) + 2))
    if x1 <= x0 or y1 <= y0:
        return
    M2 = M[:2].copy()
    M2[0, 2] -= x0
    M2[1, 2] -= y0
    out = cv2.warpAffine(m, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    a = (out * alfa)[..., None]
    roi = h.img[y0:y1, x0:x1]
    roi *= 1 - a
    roi += a * tono
    if h._E is not None:
        h._E[y0:y1, x0:x1] *= 1 - a[..., 0]


# ================================================================ transiciones
@functools.lru_cache(maxsize=4)
def _campo_mancha(sem):
    n = fbm(SW, SH, 60, 4, 900 + sem) * 0.55 + fbm(SW, SH, 16, 2, 950 + sem) * 0.18
    rng = np.random.default_rng(sem)
    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    d = np.full((SH, SW), 9.0, np.float32)
    for _ in range(4):                       # varias gotas que caen y se unen
        cx, cy, r = rng.uniform(0.15, 0.85) * SW, rng.uniform(0.2, 0.8) * SH, rng.uniform(0.7, 1.2)
        d = np.minimum(d, np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (SW * 0.55 * r))
    return (d + n * 0.22).astype(np.float32)


def tinta_cubre(img, p, sem=0, tono=0.025):
    """Mancha de tinta que se extiende y cubre el cuadro (p = 0 nada, 1 todo), con borde que se oscurece y salpica."""
    if p <= 0:
        return img
    if p >= 1:
        img[:] = tono
        return img
    c = _campo_mancha(sem)
    um = -0.25 + 1.45 * e_inout(p)
    a = np.clip((um - c) / 0.035, 0, 1)
    borde = np.clip(1 - np.abs(um - c) / 0.05, 0, 1) * 0.35
    a = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    borde = cv2.resize(borde, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    img *= (1 - a) * (1 - borde)
    img += a * tono
    return img


def iris(img, p, cx=W / 2, cy=H / 2, tono=0.02):
    """Iris clásico de cine mudo: p 0 = abierto, 1 = cerrado en (cx, cy)."""
    if p <= 0:
        return img
    rmax = math.hypot(max(cx, W - cx), max(cy, H - cy))
    r = rmax * (1 - e_inout(p))
    yy, xx = np.ogrid[0:H, 0:W]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.clip((d - r) / 6.0, 0, 1)[..., None].astype(np.float32)
    img *= 1 - a
    img += a * tono
    return img


# ================================================================ montaje: transiciones entre planos (sobre cuadros terminados)
def _desenfoque_h(img, k):
    k = int(k)
    if k < 3:
        return img
    peq = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    peq = cv2.blur(peq, (max(3, k // 2), 1))
    return cv2.resize(peq, (W, H), interpolation=cv2.INTER_LINEAR)


def _escalar(img, s, cx=W / 2, cy=H / 2):
    M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def transicion(A, B, p, tipo="fundido", sem=0, dirx=1, centro=(W / 2, H / 2)):
    """Mezcla dos cuadros terminados: corte · fundido · tinta (mancha que cubre y se retira) · barrido (paneo rápido con
    desenfoque de movimiento) · empuje (la cámara entra en A y sale de B) · relampago (destello blanco) · humo (fundido a gris)."""
    p = clamp01(p)
    if tipo == "corte":
        return B if p >= 0.5 else A
    if tipo == "fundido":
        e = smooth(p)
        return (A * (1 - e) + B * e) * (1 - 0.25 * math.sin(math.pi * p))
    if tipo == "tinta":                                   # la mancha crece y DENTRO ya está la escena nueva (borde de tinta, sin negro)
        c = _campo_mancha(sem)
        um = -0.25 + 1.45 * e_inout(p)
        a = np.clip((um - c) / 0.035, 0, 1)
        borde = np.clip(1 - np.abs(um - c) / 0.045, 0, 1) * (0.9 if 0 < p < 1 else 0)
        a = cv2.resize(a, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        borde = cv2.resize(borde, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        return (A * (1 - a) + B * a) * (1 - borde) + 0.02 * borde
    if tipo == "barrido":
        e = e_inout(p)
        off = int(e * W) * dirx
        kb = 140 * math.sin(math.pi * p)
        Ab = _desenfoque_h(np.roll(A, -off, axis=1), kb)
        Bb = _desenfoque_h(np.roll(B, W * dirx - off, axis=1), kb)
        xs = np.arange(W)
        lim = W - abs(off)
        mA = ((xs < lim) if dirx > 0 else (xs >= abs(off))).astype(np.float32)
        mA = cv2.GaussianBlur(mA[None, :], (0, 0), 40)[0][None, :, None]
        return Ab * mA + Bb * (1 - mA)
    if tipo == "empuje":
        e = e_inout(p)
        a = _escalar(A, 1 + 1.4 * e, *centro)
        b = _escalar(B, 0.55 + 0.45 * e, *centro) if e < 1 else B
        sg = 14 * math.sin(math.pi * p)
        if sg > 0.5:
            a = cv2.GaussianBlur(a, (0, 0), sg)
            b = cv2.GaussianBlur(b, (0, 0), sg * 0.7)
        w = smooth(clamp01((p - 0.3) / 0.4))
        return a * (1 - w) + b * w
    if tipo == "relampago":
        f = math.sin(math.pi * p) ** 0.6
        base = A if p < 0.5 else B
        return base + (0.97 - base) * f
    if tipo == "humo":
        e = smooth(p)
        g = 0.55 * math.sin(math.pi * p)
        mez = A * (1 - e) + B * e
        return mez * (1 - g) + 0.5 * g
    return B


# ================================================================ video real tratado como tinta (rotoscopia)
_STATS = {}


def _niveles(nombre, clip):
    """Niveles fijos por clip (percentiles de unos cuadros repartidos): evitan que el brillo bombee cuadro a cuadro."""
    if nombre not in _STATS:
        vals = []
        for k in np.linspace(0, clip.n - 1, 6):
            f = clip.frame(int(k))
            g = cv2.cvtColor(cv2.resize(f, (320, 180)), cv2.COLOR_RGB2GRAY)
            vals.append(g)
        v = np.concatenate([x.ravel() for x in vals]).astype(np.float32) / 255.0
        _STATS[nombre] = (float(np.percentile(v, 1.5)), float(np.percentile(v, 99.2)))
        clip.pos = -2
    return _STATS[nombre]


def tinta_de_foto(g, tinta=0.7, poster=0.45, trama=0.5, fase=0):
    """Convierte un gris (H x W, 0..1) en ilustración de tinta y aguada: suavizado que conserva bordes, aguada en pocos tonos,
    contornos de pluma y tramado en las sombras."""
    peq = cv2.resize(g, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    s = cv2.bilateralFilter(peq, 9, 0.12, 6)
    if poster > 0:
        n = 5.0
        q = np.floor(s * n) / n
        f = s * n - np.floor(s * n)
        q = q + smooth_arr(np.clip((f - 0.75) / 0.25, 0, 1)) / n
        s = s * (1 - poster) + q * poster
    gx = cv2.Sobel(s, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(s, cv2.CV_32F, 0, 1, ksize=3)
    e = np.sqrt(gx * gx + gy * gy)
    e = np.clip((e - 0.10) * 3.5, 0, 1)
    s = s * (1 - tinta * e)
    s = cv2.resize(s, (W, H), interpolation=cv2.INTER_LINEAR)
    if trama > 0:
        osc = np.clip((0.42 - s) / 0.3, 0, 1) * np.clip(s / 0.06, 0, 1)
        s = s * (1 - trama * 0.55 * osc * _trama(fase))
    return s


def smooth_arr(x):
    return x * x * (3 - 2 * x)


def clip_noir(h, nombre, t, t_ini, vel=1.0, inicio=0.0, z0=1.0, z1=1.08, c0=(0.5, 0.5), c1=(0.5, 0.5), dur=6.0, tinta=0.7,
              poster=0.45, trama=0.5, expo=1.0, gamma=1.0, voltear=False, rot=0.0):
    """Pinta un clip de stock (clips/<nombre>.mp4) a pantalla completa en el lienzo, convertido a tinta y aguada, con un
    Ken Burns (zoom z0->z1, centro c0->c1 en fracciones del clip) a lo largo de `dur` s desde t_ini. Luego va por h.acabado()."""
    from docu_fx import Clip
    clip = Clip.abrir(nombre)
    lo, hi = _niveles(nombre, clip)
    u = clamp01((t - t_ini) / max(0.01, dur))
    e = e_inout(u)
    idx = int((inicio + max(0.0, t - t_ini) * vel) * clip.fps)
    f = clip.frame(idx)
    g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1) ** gamma * expo
    z = z0 + (z1 - z0) * e
    cx = (c0[0] + (c1[0] - c0[0]) * e) * clip.w
    cy = (c0[1] + (c1[1] - c0[1]) * e) * clip.h
    esc = max(W / clip.w, H / clip.h) * z
    M = cv2.getRotationMatrix2D((cx, cy), rot, esc)
    M[0, 2] += W / 2 - cx
    M[1, 2] += H / 2 - cy
    if voltear:
        M[0] = -M[0]
        M[0, 2] += W
    g = cv2.warpAffine(g, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    g = tinta_de_foto(g, tinta, poster, trama, h.dib % 3)
    h.img[:] = g[..., None]
