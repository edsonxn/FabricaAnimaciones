# -*- coding: utf-8 -*-
"""Efectos y elementos del estilo DOCUMENTAL v2 (sobre nucleo/docu.py): lo que hace vistoso y adictivo al video de referencia
("Detrás del Enigma") más un toque del estilo Vox (marcador, cinta, recortes con borde, estampillas y sellos).

  Clip / clip_bg          video de apoyo (Pexels/Pixabay) como fondo, con cámara, velocidad y bucle
  slam / titular          texto de golpe: la palabra cae con escala 1,6 -> 1, rebote y vibración; mayúsculas Poppins Black Italic / Impact
  mezcla2                 transiciones: tinta (mancha negra), destello (fuga de luz amarilla), aberracion (whip con canales RGB), glitch, zoom
  elipse_luz, linea_medida, insignia, resaltador, cinta, recorte_borde, estampilla, sello_circular, barras_cine, pulso
"""
import functools
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import docu as D
from docu import H, W, Sprite, clamp01, e_back, e_inout, e_out, lerp, mezclar_pm, prog, smooth

_FD = os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts")
D.FUENTES.update(
    pop_bi=os.path.join(_FD, "Poppins-BlackItalic.ttf"),
    pop_ebi=os.path.join(_FD, "Poppins-ExtraBoldItalic.ttf"),
    pop_sbi=os.path.join(_FD, "Poppins-SemiBoldItalic.ttf"),
    pop_bold_i=os.path.join(_FD, "Poppins-BoldItalic.ttf"),
    impact="C:/Windows/Fonts/impact.ttf",
)
AMARILLO, BLANCO, ROJO = D.AMARILLO, D.BLANCO, D.ROJO
_GRID = D._grid


# ------------------------------------------------------------------ pulso de cámara / vibración
def pulso(t, tiempos, amp=0.018, dur=0.45):
    """Suma de golpes de zoom que decaen (cada tiempo de `tiempos` da un 'punch'); devuelve multiplicador de zoom >= 1."""
    z = 0.0
    for ta in tiempos:
        if ta <= t < ta + dur:
            u = (t - ta) / dur
            z += amp * (1 - u) ** 2
    return 1.0 + z


def vibra(t, t0, dur=0.3, amp=7.0):
    """Desplazamiento (dx, dy) de vibración que se apaga tras t0."""
    if not (t0 <= t < t0 + dur):
        return 0.0, 0.0
    a = amp * (1 - (t - t0) / dur) ** 2
    return a * math.sin(t * 131.0), a * math.sin(t * 97.0 + 1.3)


# ------------------------------------------------------------------ texto de golpe
def slam(lz, pal, t, fnt="pop_bi", px=110, salida=None, escala0=1.28, scan=False, op=1.0, grosor_borde=0.07, dy_extra=0.0, vibrar=False):
    """Dibuja las palabras de `pal` (salida de docu.bloque_texto) con entrada de golpe: escala 1,65 -> 1 con rebote, vibración corta y
    destello al aterrizar. `scan=True` añade líneas de escaneo (rótulo tipo '134 METROS')."""
    o = op
    if salida is not None:
        o *= 1 - smooth(prog(t, salida, salida + 0.25))
    if o <= 0.003:
        return
    for w, ta, col, x, y in pal:
        if t < ta:
            continue
        pm, a, m = D.palabra_img(w, fnt, px, tuple(col), stroke=grosor_borde, glow=0.6)
        u = prog(t, ta, ta + 0.30)
        s = lerp(escala0, 1.0, e_out(u))
        if u >= 1:                                     # asentamiento suave
            e = t - ta - 0.30
            s += 0.018 * math.exp(-e * 7) * math.sin(e * 16)
        s *= 1.0 + 0.012 * math.sin(0.8 * t + x)         # respira
        cx = x - m + pm.shape[1] / 2
        cy = y - m + pm.shape[0] / 2 + dy_extra
        if vibrar:
            dx, dy = vibra(t, ta + 0.30, 0.22, 3.0)
            cx, cy = cx + dx, cy + dy
        if abs(s - 1) > 0.004:
            pm2 = cv2.resize(pm, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
            a2 = cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
        else:
            pm2, a2 = pm, a
        if scan:
            rows = (0.55 + 0.45 * ((np.arange(a2.shape[0]) % 4) < 2)).astype(np.float32)
            pm2, a2 = pm2 * rows[:, None, None], a2 * rows[:, None]
        oo = o * smooth(prog(t, ta, ta + 0.14))
        mezclar_pm(lz, pm2, a2, int(cx - pm2.shape[1] / 2), int(cy - pm2.shape[0] / 2), oo)
        # destello blanco al aterrizar (solo local: la propia palabra)
        fl = math.exp(-max(0.0, t - ta - 0.15) * 10) * 0.5 if ta + 0.15 <= t < ta + 0.6 else 0.0
        if fl > 0.02:
            mezclar_pm(lz, a2[..., None] * np.float32([1, 1, 0.9]) * 0.35, a2, int(cx - pm2.shape[1] / 2), int(cy - pm2.shape[0] / 2), oo * fl, aditivo=True)


def titular(palabras, cx, cy, px=110, fnt="pop_bi", lineas=None, color=BLANCO, clave=None, color_clave=AMARILLO, alinear="centro", mayus=True, interlinea=1.04, espacio=0.2):
    """Prepara el bloque: `palabras` = [(texto, t)]; `clave` = índices (o texto) de palabras que van en amarillo; `lineas` = cortes de línea."""
    pal = []
    for i, (w, ta) in enumerate(palabras):
        w2 = w.upper() if mayus else w
        es_clave = clave is not None and (i in clave if not isinstance(clave, str) else w.lower().strip(".,;:¿?¡!") in clave.lower().split())
        pal.append((w2, ta, color_clave if es_clave else color))
    if lineas:
        filas, ini = [], 0
        for c in list(lineas) + [len(pal)]:
            filas.append(pal[ini:c])
            ini = c
        filas = [f for f in filas if f]
    else:
        filas = [pal]
    return D.bloque_texto(filas, cx, cy, fnt, px, color, alinear, interlinea, espacio)


def caption(lz, pal, t, px=40, salida=None, op=1.0):
    """Rótulo pequeño en cursiva mayúsculas (como 'CUANDO DE PRONTO, VE ALGO QUE NO ENTIENDE'): aparece palabra a palabra, sin golpe."""
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    for w, ta, col, x, y in pal:
        if t < ta:
            continue
        pm, a, m = D.palabra_img(w, "pop_sbi", px, tuple(col), stroke=0.02, glow=0.55)
        u = smooth(prog(t, ta, ta + 0.2))
        mezclar_pm(lz, pm, a, int(x - m), int(y - m + (1 - u) * 8), o * u)


# ------------------------------------------------------------------ video de apoyo
class Clip:
    _abiertos = {}

    def __init__(self, ruta):
        self.cap = cv2.VideoCapture(ruta)
        self.n = max(1, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.pos = -2
        self.ult = None

    @classmethod
    def abrir(cls, nombre):
        ruta = nombre if os.path.isabs(nombre) else os.path.join(os.getcwd(), "clips", nombre + ".mp4")
        if ruta not in cls._abiertos:
            if len(cls._abiertos) >= 6:
                k = next(iter(cls._abiertos))
                cls._abiertos.pop(k).cap.release()
            cls._abiertos[ruta] = Clip(ruta)
        return cls._abiertos[ruta]

    def frame(self, idx):
        idx = int(idx) % self.n
        if idx == self.pos and self.ult is not None:
            return self.ult
        if idx != self.pos + 1:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, f = self.cap.read()
        if not ok:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, f = self.cap.read()
            idx = 0
        self.pos = idx
        self.ult = cv2.cvtColor(f, cv2.COLOR_BGR2RGB) if ok else np.zeros((H, W, 3), np.uint8)
        return self.ult


def clip_bg(lz, nombre, t, dur=4.0, inicio=0.0, vel=1.0, z0=1.04, z1=1.14, c0=(0.5, 0.5), c1=(0.5, 0.5), tono=None, sat=1.0, op=1.0, z_extra=1.0, pingpong=False, ease=e_inout):
    """Clip como fondo: cubre 16:9, cámara (zoom z0->z1, centro c0->c1), velocidad `vel`, tinte multiplicativo `tono`, saturación `sat`."""
    c = Clip.abrir(nombre)
    tt = inicio + t * vel
    seg = c.n / c.fps
    if pingpong:
        tt = tt % (2 * seg)
        tt = 2 * seg - tt if tt > seg else tt
    f = c.frame(tt * c.fps)
    u = ease(clamp01(t / max(dur, 1e-3)))
    z = lerp(z0, z1, u) * z_extra
    cx, cy = lerp(c0[0], c1[0], u) * c.w, lerp(c0[1], c1[1], u) * c.h
    s = max(W / c.w, H / c.h) * z
    M = np.array([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]], np.float32)
    out = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255.0
    if sat != 1.0:
        lum = out @ np.array([0.299, 0.587, 0.114], np.float32)
        out = lum[..., None] + (out - lum[..., None]) * sat
    if tono is not None:
        out *= np.float32(tono)
    if op >= 0.999:
        lz[:] = np.clip(out, 0, 1)
    else:
        lz *= (1 - op)
        lz += np.clip(out, 0, 1) * op


# ------------------------------------------------------------------ transiciones
@functools.lru_cache(maxsize=2)
def _campo_tinta():
    rng = np.random.default_rng(12)
    n = np.zeros((H // 8, W // 8), np.float32)
    for esc, amp in ((3, 0.5), (7, 0.3), (17, 0.15), (40, 0.05)):
        g = rng.random((max(2, H // 8 // esc + 2), max(2, W // 8 // esc + 2))).astype(np.float32)
        n += amp * cv2.resize(g, (W // 8, H // 8), interpolation=cv2.INTER_CUBIC)
    n = cv2.GaussianBlur(n, (0, 0), 2.0)
    n = (n - n.min()) / (n.max() - n.min())
    return cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC)


def mezcla2(A, B, p, tipo, sem=0):
    p = float(np.clip(p, 0, 1))
    if tipo == "tinta":                       # mancha de tinta que crece y descubre B (con borde oscuro): nunca deja el cuadro en negro
        N = _campo_tinta()
        thr = p * 1.25
        m = np.clip((thr - N) / 0.08, 0, 1)[..., None]
        borde = np.clip(1 - np.abs(thr - N - 0.05) / 0.07, 0, 1)[..., None] * (1 - 0.0)
        out = A * (1 - m) + B * m
        return out * (1 - 0.80 * borde)
    if tipo == "destello":                    # fuga de luz amarilla-naranja (solo un pulso suave, nunca blanco total)
        m = A * (1 - smooth(p)) + B * smooth(p)
        X, Y = _GRID()
        rng = np.random.default_rng(sem + 5)
        cx, cy = rng.random() * W, rng.random() * H * 0.6
        g = np.clip(1 - np.hypot((X - cx) / (W * 0.8), (Y - cy) / (H * 0.9)), 0, 1) ** 1.3
        a = math.sin(math.pi * p) ** 1.4
        return m + g[..., None] * a * 0.85 * np.array([1.0, 0.72, 0.12], np.float32) + a * 0.06
    if tipo == "fuga":                        # banda de fuga de luz (rosa -> naranja -> amarillo) que barre y deja ver B
        Xg, Yg = _GRID()
        xe = lerp(-0.35 * W, 1.35 * W, e_inout(p)) + (Yg - H / 2) * 0.22
        m = np.clip((xe - Xg) / (0.22 * W) + 0.5, 0, 1)
        m = (m * m * (3 - 2 * m))[..., None]
        base = A * (1 - m) + B * m
        d = (Xg - xe) / (0.20 * W)
        band = np.exp(-d * d)[..., None]
        u = np.clip(d * 0.5 + 0.5, 0, 1)[..., None]
        col = (1 - u) * np.array([1.0, 0.30, 0.45], np.float32) + u * np.array([1.0, 0.90, 0.25], np.float32)
        return base + band * col * 0.8 * math.sin(math.pi * clamp01(p)) ** 0.6
    if tipo == "aberracion":                  # whip con separación de canales RGB
        s = e_inout(p)
        k = int(30 + 110 * math.sin(math.pi * p))
        ker = np.full((1, k | 1), 1.0 / (k | 1), np.float32)
        dxa, dxb = int(-W * 0.6 * s), int(W * 0.6 * (1 - s))
        a = np.roll(A, dxa, 1)
        b = np.roll(B, dxb, 1)
        m = a * (1 - smooth(p)) + b * smooth(p)
        m = cv2.filter2D(m, -1, ker)
        d = int(26 * math.sin(math.pi * p))
        out = m.copy()
        out[..., 0] = np.roll(m[..., 0], d, 1)
        out[..., 2] = np.roll(m[..., 2], -d, 1)
        return out
    if tipo == "glitch":
        base = A if p < 0.5 else B
        out = base.copy()
        rng = np.random.default_rng(int(p * 40) + sem)
        for _ in range(9):
            y0 = int(rng.integers(0, H - 40)); hh = int(rng.integers(12, 90)); dx = int(rng.integers(-160, 160))
            out[y0:y0 + hh] = np.roll(out[y0:y0 + hh], dx, 1)
        d = int(18 * math.sin(math.pi * p))
        out[..., 0] = np.roll(out[..., 0], d, 1)
        out[..., 2] = np.roll(out[..., 2], -d, 1)
        return out
    if tipo == "zoom":                        # A se agranda con desenfoque radial y B llega desde grande
        s = e_inout(p)

        def esc(img, k):
            M = np.array([[k, 0, W / 2 * (1 - k)], [0, k, H / 2 * (1 - k)]], np.float32)
            return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        a = esc(A, 1 + 0.8 * s)
        b = esc(B, 1.5 - 0.5 * s)
        a = 0.5 * a + 0.5 * esc(A, 1 + 0.8 * s + 0.08)
        return a * (1 - smooth(p)) + b * smooth(p)
    return D.mezcla_tomas(A, B, p, tipo)


# ------------------------------------------------------------------ elementos gráficos
def _aditivo(lz, mask, color, glow=1.0, op=1.0, x0=0, y0=0, sigma=8.0):
    a = mask.astype(np.float32) / 255.0 if mask.dtype == np.uint8 else mask
    g = cv2.GaussianBlur(a, (0, 0), sigma) * glow
    tot = np.clip(a + g, 0, 1)
    mezclar_pm(lz, tot[..., None] * np.float32(color), tot, x0, y0, op, aditivo=True)


def elipse_luz(lz, cx, cy, rx, ry, u, grosor=5, op=1.0, color=(1.0, 0.98, 0.94), rot=0.0, glow=1.0):
    """Óvalo luminoso dibujado a mano que rodea una zona (como el que marca la espiral del mono en la referencia); u de 0 a 1."""
    if u <= 0 or op <= 0:
        return
    x0, y0 = int(cx - rx - 40), int(cy - ry - 40)
    w, h = int(2 * rx + 80), int(2 * ry + 80)
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if xb <= xa or yb <= ya:
        return
    m = np.zeros((yb - ya, xb - xa), np.uint8)
    ang = np.linspace(-1.9, -1.9 + 2 * math.pi * 1.04 * clamp01(u), 90)
    r = 1 + 0.025 * np.sin(ang * 3.0)
    pts = np.c_[cx + rx * r * np.cos(ang), cy + ry * r * np.sin(ang)]
    if rot:
        a = math.radians(rot)
        d = pts - [cx, cy]
        pts = np.c_[cx + d[:, 0] * math.cos(a) - d[:, 1] * math.sin(a), cy + d[:, 0] * math.sin(a) + d[:, 1] * math.cos(a)]
    q = np.round((pts - [xa, ya]) * 16).astype(np.int32)
    cv2.polylines(m, [q], False, 255, int(grosor), cv2.LINE_AA, shift=4)
    _aditivo(lz, m, color, glow, op, xa, ya, sigma=9)


def linea_medida(lz, p0, p1, u, texto, t, t0, px=66, color=(1.0, 0.98, 0.94), op=1.0, salida=None):
    """Línea punteada de medida con rótulo en cursiva y líneas de escaneo (estilo '134 METROS'). p0-p1 en pantalla; u = avance de la línea."""
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    D.linea_punteada(lz, [p0, p1], u, dash=26, hueco=16, grosor=5, color=color, op=o)
    if t < t0 or u < 0.35:
        return
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    pm, a, m = D.palabra_img(texto.upper(), "pop_bold_i", px, color, stroke=0.02, glow=0.6)
    rows = (0.6 + 0.4 * ((np.arange(a.shape[0]) % 4) < 2)).astype(np.float32)
    pm, a = pm * rows[:, None, None], a * rows[:, None]
    s = e_back(prog(t, t0, t0 + 0.35))
    sp = Sprite((pm * 255).clip(0, 255).astype(np.uint8), a, sombra=False)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - px * 0.75
    D.pegar(lz, sp, D.poner(sp.w, sp.h, mx, my, s, ang), o * smooth(prog(t, t0, t0 + 0.2)))


@functools.lru_cache(maxsize=32)
def _insignia_sprite(clave, ruta, r):
    im = D.cargar(ruta, 900)
    h, w = im.shape[:2]
    d = min(h, w)
    im = im[(h - d) // 2:(h - d) // 2 + d, (w - d) // 2:(w - d) // 2 + d]
    n = int(2 * r)
    im = cv2.resize(im, (n, n), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    dist = np.hypot(xx - n / 2, yy - n / 2)
    a = np.clip(r - dist, 0, 1)
    borde = np.clip(dist - (r - 9), 0, 1)
    rgb = im.astype(np.float32) * (1 - borde[..., None]) + np.array([245, 238, 220], np.float32) * borde[..., None]
    return Sprite(np.clip(rgb, 0, 255).astype(np.uint8), a, sombra=True, sr=10, off=(6, 9), sop=0.6)


def insignia(lz, ruta, cx, cy, r, t, t0, salida=None, op=1.0, fase=0.0, M=None):
    """Insignia circular con imagen y borde crema (como las de algodón/maíz de la referencia); entra con rebote y flota."""
    if t < t0:
        return
    sp = _insignia_sprite(os.path.basename(ruta), ruta, int(r))
    s = e_back(prog(t, t0, t0 + 0.4))
    o = op * (1 - (smooth(prog(t, salida, salida + 0.25)) if salida is not None else 0))
    y = cy + 6 * math.sin(1.1 * t + fase)
    Mm = D.poner(sp.w, sp.h, cx, y, s, 3 * math.sin(0.8 * t + fase))
    if M is not None:
        Mm = M @ Mm
    D.pegar(lz, sp, Mm, o)


def resaltador(lz, x0, y0, x1, y1, u, color=(1.0, 0.92, 0.18), op=0.85, semilla=0):
    """Marcador amarillo de un trazo (estilo Vox): barra con bordes irregulares que avanza de izquierda a derecha; se MULTIPLICA sobre lo de detrás."""
    if u <= 0:
        return
    rng = np.random.default_rng(semilla)
    xe = x0 + (x1 - x0) * clamp01(u)
    if xe - x0 < 4:
        return
    n = 14
    xs = np.linspace(x0, xe, n)
    top = y0 + rng.normal(0, 2.2, n)
    bot = y1 + rng.normal(0, 2.2, n)
    pts = np.r_[np.c_[xs, top], np.c_[xs[::-1] + rng.normal(0, 2, n), bot[::-1]]]
    xa, ya = int(max(0, x0 - 20)), int(max(0, y0 - 20))
    xb, yb = int(min(W, xe + 20)), int(min(H, y1 + 20))
    if xb <= xa or yb <= ya:
        return
    m = np.zeros((yb - ya, xb - xa), np.uint8)
    cv2.fillPoly(m, [np.round((pts - [xa, ya]) * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
    a = cv2.GaussianBlur(m.astype(np.float32) / 255.0, (0, 0), 1.2) * op
    reg = lz[ya:yb, xa:xb]
    reg *= 1 - a[..., None] * (1 - np.float32(color))
    reg += a[..., None] * np.float32(color) * 0.06


@functools.lru_cache(maxsize=8)
def _cinta(rot_sem):
    w, h = 190, 58
    im = np.zeros((h, w, 3), np.uint8)
    im[:] = (226, 214, 176)
    a = np.ones((h, w), np.float32) * 0.78
    rng = np.random.default_rng(rot_sem)
    for x in (0, w - 1):                                          # extremos dentados
        for y in range(0, h, 6):
            L = int(rng.integers(3, 9))
            a[y:y + 3, x if x == 0 else w - L:x + L if x == 0 else w] = 0
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    return Sprite(im, a, sombra=True, sr=4, off=(3, 4), sop=0.4)


def cinta(lz, M, x, y, rot=-30.0, op=1.0, sem=0):
    """Pieza de cinta adhesiva translúcida pegada en (x, y) del mundo (M = matriz de cámara)."""
    sp = _cinta(sem % 5)
    px, py = D.tf(M, x, y)
    z = float(np.sqrt(abs(np.linalg.det(M[:2, :2]))))
    D.pegar(lz, sp, D.poner(sp.w, sp.h, px, py, z, rot), op)


def recorte_borde(png, borde=16, color=(246, 240, 224), max_lado=1100):
    """Recorte tipo pegatina (estilo Vox): la silueta del PNG con borde crema, sombra y ligero grano de papel."""
    im = np.asarray(Image.open(png).convert("RGBA"))
    h, w = im.shape[:2]
    k = max_lado / max(h, w)
    if k < 1:
        im = cv2.resize(im, (int(w * k), int(h * k)), interpolation=cv2.INTER_AREA)
    a = im[..., 3].astype(np.float32) / 255.0
    pad = borde + 6
    a = np.pad(a, pad)
    rgb = np.pad(im[..., :3], ((pad, pad), (pad, pad), (0, 0)))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * borde + 1, 2 * borde + 1))
    dil = cv2.dilate((a > 0.3).astype(np.uint8), ker).astype(np.float32)
    dil = cv2.GaussianBlur(dil, (0, 0), 1.6)
    base = np.empty(rgb.shape, np.float32)
    base[:] = np.array(color, np.float32)
    out = base * (1 - a[..., None]) + rgb.astype(np.float32) * a[..., None]
    return Sprite(np.clip(out, 0, 255).astype(np.uint8), np.clip(dil, 0, 1), sombra=True, sr=18, off=(12, 18), sop=0.6)


def estampilla(rgb, valor="", ancho=360, aspecto=1.25, cancelada=True):
    """Estampilla postal con borde perforado (estampa): imagen enmarcada, valor en la esquina y matasellos ondulado."""
    h = int(ancho * aspecto)
    r = 11
    canvas = np.zeros((h, ancho, 3), np.float32)
    canvas[:] = (244, 240, 226)
    a = np.ones((h, ancho), np.float32)
    for x in range(r, ancho, 2 * r + 4):
        for y in (0, h - 1):
            cv2.circle(a, (x, y), r // 2 + 2, 0, -1, cv2.LINE_AA)
    for y in range(r, h, 2 * r + 4):
        for x in (0, ancho - 1):
            cv2.circle(a, (x, y), r // 2 + 2, 0, -1, cv2.LINE_AA)
    m = 30
    foto = D.cargar(D.ruta_img(rgb), 1000) if isinstance(rgb, str) else rgb
    fh, fw = foto.shape[:2]
    caja = (ancho - 2 * m, h - 2 * m - 50)
    k = max(caja[0] / fw, caja[1] / fh)
    f2 = cv2.resize(foto, (int(fw * k) + 1, int(fh * k) + 1), interpolation=cv2.INTER_AREA)
    y0, x0 = (f2.shape[0] - caja[1]) // 2, (f2.shape[1] - caja[0]) // 2
    canvas[m:m + caja[1], m:m + caja[0]] = f2[y0:y0 + caja[1], x0:x0 + caja[0]].astype(np.float32) * 0.92
    cv2.rectangle(canvas, (m - 2, m - 2), (m + caja[0] + 1, m + caja[1] + 1), (40, 34, 30), 2)
    pil = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    if valor:
        d.text((ancho - m, h - m - 12), valor, font=D.fuente("abril", 44), fill=(60, 30, 26), anchor="rd")
    if cancelada:
        pts = [(x, h * 0.62 + 14 * math.sin(x / 26.0)) for x in range(20, ancho - 10, 6)]
        d.line(pts, fill=(30, 30, 40), width=4)
        pts2 = [(x, h * 0.62 + 26 + 14 * math.sin(x / 26.0)) for x in range(20, ancho - 10, 6)]
        d.line(pts2, fill=(30, 30, 40), width=4)
    return Sprite(np.asarray(pil), a, sombra=True, sr=10, off=(8, 12), sop=0.55)


@functools.lru_cache(maxsize=8)
def sello_circular(arriba, centro, abajo, color=(0.72, 0.10, 0.10), d=420):
    """Sello de tinta circular (doble aro, texto en arco arriba/abajo y palabra central); tinta desgastada."""
    im = Image.new("L", (d, d), 0)
    dr = ImageDraw.Draw(im)
    dr.ellipse([6, 6, d - 6, d - 6], outline=255, width=9)
    dr.ellipse([32, 32, d - 32, d - 32], outline=255, width=4)
    f = D.fuente("sans_b", 40)

    def arco(txt, radio, centro_ang, invertir=False):
        n = len(txt)
        paso = 11.5
        for i, ch in enumerate(txt):
            ang = centro_ang + paso * ((n - 1) / 2 - i) if invertir else centro_ang - paso * (n - 1) / 2 + i * paso
            tile = Image.new("L", (80, 80), 0)
            ImageDraw.Draw(tile).text((40, 40), ch, font=f, fill=255, anchor="mm")
            rot = -(ang - 90) if invertir else -(ang + 90)
            tile = tile.rotate(rot, resample=Image.BICUBIC)
            px = d / 2 + radio * math.cos(math.radians(ang)) - 40
            py = d / 2 + radio * math.sin(math.radians(ang)) - 40
            im.paste(255, (int(px), int(py)), tile)
    arco(arriba.upper(), d / 2 - 66, -90)
    arco(abajo.upper(), d / 2 - 66, 90, invertir=True)
    dr.text((d / 2, d / 2), centro.upper(), font=D.fuente("impact", 72), fill=255, anchor="mm")
    a = np.asarray(im, np.float32) / 255.0
    rng = np.random.default_rng(3)
    ruido = cv2.GaussianBlur(rng.random(a.shape).astype(np.float32), (0, 0), 1.3)
    a *= np.clip((ruido - 0.32) * 5, 0.25, 1)
    rgb = np.empty(a.shape + (3,), np.uint8)
    rgb[:] = (np.array(color) * 255).astype(np.uint8)
    return Sprite(rgb, a * 0.9, sombra=False)


def barras_cine(lz, t, t0, alto=64, salida=None):
    """Franjas negras arriba y abajo que entran (formato cine)."""
    u = smooth(prog(t, t0, t0 + 0.4)) * (1 - (smooth(prog(t, salida, salida + 0.4)) if salida is not None else 0))
    h = int(alto * u)
    if h > 0:
        lz[:h] *= 0.0
        lz[-h:] *= 0.0


def semitono_franja(lz, y0=0.66, color=(0, 0, 0), fuerza=0.55, paso=11.0):
    """Sombra inferior de puntos de semitono (estilo Vox) que se densifica hacia el borde; mantiene legible el texto."""
    ys = int(H * y0)
    reg = lz[ys:]
    hh = reg.shape[0]
    X, Y = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(hh, dtype=np.float32))
    ang = math.radians(35)
    u = (X * math.cos(ang) + Y * math.sin(ang)) / paso
    v = (-X * math.sin(ang) + Y * math.cos(ang)) / paso
    trama = (np.cos(2 * math.pi * u) + np.cos(2 * math.pi * v)) * 0.25 + 0.5
    g = (Y / hh) ** 1.2
    punto = np.clip((g * 1.15 - (1 - trama) * 0.55) * 6, 0, 1)
    a = np.clip(punto * fuerza + g * fuerza * 0.55, 0, 1)
    reg *= (1 - a)[..., None]


# ================================================================== v3: calco del original (filtro de película, estilos de texto, trazos, fuga de luz)
_CACHE_CINE = {}


def _mapas_ca(fuerza):
    k = ("ca", round(fuerza, 2))
    if k not in _CACHE_CINE:
        Xg, Yg = _GRID()
        dx, dy = (Xg - W / 2) / (W / 2), (Yg - H / 2) / (H / 2)
        r2 = dx * dx + dy * dy
        _CACHE_CINE[k] = (((Xg + dx * r2 * fuerza)).astype(np.float32), Yg.astype(np.float32), ((Xg - dx * r2 * fuerza)).astype(np.float32))
    return _CACHE_CINE[k]


def _mascara_tilt(banda=0.50, ancho=0.17, suave=0.30):
    k = ("tilt", banda, ancho, suave)
    if k not in _CACHE_CINE:
        y = np.linspace(0, 1, H, dtype=np.float32)
        m = np.clip((np.abs(y - banda) - ancho) / suave, 0, 1)
        m = m * m * (3 - 2 * m)
        Xg, Yg = _GRID()
        r = np.sqrt(((Xg - W / 2) / (W / 2)) ** 2 + ((Yg - H / 2) / (H / 2)) ** 2)
        lat = np.clip((r - 0.85) / 0.55, 0, 1)                   # desenfoque suave también en los bordes laterales
        _CACHE_CINE[k] = np.clip(np.maximum(m[:, None] * np.ones((1, W), np.float32), lat * 0.7), 0, 1)[..., None].astype(np.float32)
    return _CACHE_CINE[k]


def cine(img, t, tilt=5.0, banda=0.52, ca=2.2, bloom=0.22, escaneo=0.13, periodo=4, vineta=0.68, grano=0.05, polvo=0.18, sat=0.92,
         tinte=None, calido=0.05, teal=0.04, destello=0.0):
    """FILTRO DE PELÍCULA del original: desenfoque tilt-shift (arriba/abajo/bordes), aberración cromática radial, bloom en luces, gradación
    cálida/teal, viñeta fuerte, polvo, grano y LÍNEAS DE ESCANEO horizontales sobre todo el cuadro (también sobre el texto)."""
    img = np.clip(img, 0, 1)
    if tilt > 0:
        pq = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
        pq = cv2.GaussianBlur(pq, (0, 0), tilt / 2.0 * 1.6)
        bl = cv2.resize(pq, (W, H), interpolation=cv2.INTER_LINEAR)
        m = _mascara_tilt(banda)
        img = img * (1 - m) + bl * m
    if ca > 0:
        mr, my, mb = _mapas_ca(ca)
        r = cv2.remap(img[..., 0], mr, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        b = cv2.remap(img[..., 2], mb, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        img = np.stack([r, img[..., 1], b], -1)
    if bloom > 0:
        alt = np.clip(img - 0.68, 0, 1)
        h2 = cv2.GaussianBlur(cv2.resize(alt, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 6)
        img = img + cv2.resize(h2, (W, H), interpolation=cv2.INTER_LINEAR) * bloom * 1.6
    img = D.acabado(img, t, fuerza_vineta=vineta, grano=grano, polvo=polvo, teal=teal, calido=calido, destello=destello, sat=sat, tinte=tinte)
    if escaneo > 0:
        y = (np.arange(H) + int(t * 24)) % periodo
        f = np.where(y < periodo / 2, 1.0 - escaneo, 1.0).astype(np.float32)
        img = img * f[:, None, None]
    return np.clip(img, 0, 1)


def rotulo(palabras, cx, cy, px=74, lineas=None, color=(0.97, 0.95, 0.92), interlinea=1.17, espacio=0.27):
    """Texto principal del original: cursiva mayúsculas (Poppins SemiBold Italic), blanco, dos líneas centradas."""
    return titular(palabras, cx, cy, px, "pop_sbi", lineas, color, None, mayus=True, interlinea=interlinea, espacio=espacio)


def dibujar_rotulo(lz, pal, t, px=74, salida=None, op=1.0, scan=True, sube=8.0):
    """Cada palabra aparece con fundido (0,30 s) subiendo unos píxeles; líneas de escaneo a través de las letras; sombra suave."""
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    if o <= 0.003:
        return
    for w, ta, col, x, y in pal:
        if t < ta:
            continue
        pm, a, m = D.palabra_img(w, "pop_sbi", px, tuple(col), stroke=0.012, glow=0.5)
        u = smooth(prog(t, ta, ta + 0.30))
        if scan:
            rows = (0.55 + 0.45 * ((np.arange(a.shape[0]) % 4) < 2)).astype(np.float32)
            pm, a = pm * rows[:, None, None], a * rows[:, None]
        mezclar_pm(lz, pm, a, int(x - m), int(y - m + (1 - u) * sube), o * u)


def serif_amarillo(palabras, cx, cy, px=60, lineas=None, color=(0.95, 1.0, 0.10)):
    """Serif amarillo condensado, Título Con Mayúsculas, pequeño (como 'Es Cahuachi' / '24 Kilómetros Cuadrados')."""
    pal = [(w[:1].upper() + w[1:], t) for w, t in palabras]
    return titular(pal, cx, cy, px, "serif_cond", lineas, color, None, mayus=False, interlinea=1.0, espacio=0.24)


def dibujar_serif(lz, pal, t, px=60, salida=None, op=1.0, fnt="serif_cond"):
    o = op * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    if o <= 0.003:
        return
    for w, ta, col, x, y in pal:
        if t < ta:
            continue
        pm, a, m = D.palabra_img(w, fnt, px, tuple(col), stroke=0.045, glow=0.6)
        u = smooth(prog(t, ta, ta + 0.18))
        mezclar_pm(lz, pm, a, int(x - m), int(y - m), o * u)


def pregunta_c(lz, lineas, t, t0, cx, cy, px=60, salida=None):
    """Serif blanco condensado + signo '?' rojo grande (como 'Pregunta Alimenta Teorías Extremas'); lineas = [[(palabra, t), ...], ...]."""
    o = 1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0)
    if t < t0:
        return
    pm, a, m = D.palabra_img("?", "abril_cond", 330, tuple(ROJO), stroke=0.0, glow=0.0)
    s = e_back(prog(t, t0, t0 + 0.45))
    if s > 0.02:
        pm2 = cv2.resize(pm, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
        a2 = cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
        mezclar_pm(lz, pm2, a2, int(cx - pm2.shape[1] / 2), int(cy - 190 - pm2.shape[0] / 2), o * smooth(prog(t, t0, t0 + 0.2)))
    pal = D.bloque_texto([[(w[:1].upper() + w[1:], tt) for w, tt in ln] for ln in lineas], cx, cy + 40, "serif_cond", px, (0.97, 0.96, 0.93), "centro", 1.05, 0.24)
    for w, ta, col, x, y in pal:
        if t < ta:
            continue
        pm, a, m = D.palabra_img(w, "serif_cond", px, tuple(col), stroke=0.04, glow=0.6)
        mezclar_pm(lz, pm, a, int(x - m), int(y - m), o * smooth(prog(t, ta, ta + 0.2)))


def trazo_recto(lz, p0, p1, u_ini, u_fin, w=26, color=(0.80, 0.02, 0.09), op=0.95):
    """Trazo rojo grueso de extremos redondos sobre la recta p0->p1, visible entre las fracciones u_ini..u_fin (se dibuja avanzando u_fin
    y se borra avanzando u_ini): las 'líneas rectas' del minuto 1 del original ('nueve kilómetros')."""
    u_ini, u_fin = clamp01(u_ini), clamp01(u_fin)
    if u_fin - u_ini < 0.004 or op <= 0:
        return
    a = (p0[0] + (p1[0] - p0[0]) * u_ini, p0[1] + (p1[1] - p0[1]) * u_ini)
    b = (p0[0] + (p1[0] - p0[0]) * u_fin, p0[1] + (p1[1] - p0[1]) * u_fin)
    x0, y0 = int(max(0, min(a[0], b[0]) - w - 8)), int(max(0, min(a[1], b[1]) - w - 8))
    x1, y1 = int(min(W, max(a[0], b[0]) + w + 8)), int(min(H, max(a[1], b[1]) + w + 8))
    if x1 <= x0 or y1 <= y0:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    cv2.line(m, (int((a[0] - x0) * 16), int((a[1] - y0) * 16)), (int((b[0] - x0) * 16), int((b[1] - y0) * 16)), 255, int(w), cv2.LINE_AA, shift=4)
    for p in (a, b):
        cv2.circle(m, (int((p[0] - x0) * 16), int((p[1] - y0) * 16)), int(w * 8), 255, -1, cv2.LINE_AA, shift=4)
    al = cv2.GaussianBlur(m.astype(np.float32) / 255.0, (0, 0), 0.9)
    borde = np.clip(al - cv2.erode(al, np.ones((5, 5), np.uint8)), 0, 1)
    col = np.float32(color)
    pm = (al[..., None] * col) * (1 - 0.35 * borde[..., None])
    mezclar_pm(lz, pm, al, x0, y0, op)


def marco_pelicula(lz, ancho=78, t=0.0, op=1.0):
    """Barras negras laterales de fotograma de película (irregulares) con arañazos verticales tenues."""
    if "mp" not in _CACHE_CINE:
        rng = np.random.default_rng(9)
        r = cv2.GaussianBlur(rng.random((H, 1)).astype(np.float32), (0, 0), 6)
        _CACHE_CINE["mp"] = ((r - r.min()) / (r.max() - r.min() + 1e-6))[:, 0]
    r = _CACHE_CINE["mp"]
    for y in range(0, H, 2):
        e = int(ancho + 14 * r[y])
        lz[y:y + 2, :e] *= (1 - op)
        lz[y:y + 2, W - e:] *= (1 - op)
    rng = np.random.default_rng(int(t * 12) % 97)
    for _ in range(2):
        x = int(rng.random() * (W - 2 * ancho) + ancho)
        lz[:, x:x + 1] += 0.05 * op * rng.random()


def hoja_mapa(nombre_png="imagenes/mapa_lacio.png", centro=(1500, 1610), ancho=980, alto=740, marcas=None):
    """Recorte gris del mapa de relieve con marcadores amarillo-verde, línea blanca y nombre (como la polaroid de Cahuachi).
    `marcas` = [(nombre, x, y)] en píxeles del mapa original."""
    im = np.asarray(Image.open(nombre_png).convert("RGB"))
    cx, cy = centro
    x0, y0 = max(0, cx - ancho // 2), max(0, cy - alto // 2)
    rec = im[y0:y0 + alto, x0:x0 + ancho].astype(np.float32)
    g = rec @ np.array([0.30, 0.59, 0.11], np.float32)
    lo, hi = np.percentile(g, 3), np.percentile(g, 97)
    g = np.clip((g - lo) / max(hi - lo, 1) , 0, 1) ** 1.25 * 235 + 10
    rec = np.repeat(g[..., None], 3, -1)
    pil = Image.fromarray(rec.astype(np.uint8))
    d = ImageDraw.Draw(pil)
    pts = [(mx - x0, my - y0) for _, mx, my in (marcas or [])]
    if len(pts) >= 2:
        d.line(pts, fill=(255, 255, 255), width=4)
    for (nm, mx, my), (px_, py_) in zip(marcas or [], pts):
        d.ellipse([px_ - 44, py_ - 44, px_ + 44, py_ + 44], fill=(190, 235, 30))
        d.text((px_, py_ - 62), nm, font=D.fuente("sans_l", 30), fill=(255, 255, 255), anchor="mb", stroke_width=3, stroke_fill=(0, 0, 0))
    return np.asarray(pil)
