# -*- coding: utf-8 -*-
"""Interfaz y efectos de pantalla del estilo Kurzgesagt: etiquetas en cápsula con muesca (llamadas), globos de diálogo, insignias numeradas, contadores, ondas sonoras,
chispas de 4 puntas, bokeh, haces de luz y la curva de aparición («pop») medida en el original (60 fps):
  crece del 9 % al 92 % en 0,15 s (casi lineal), se asienta con ~1,5 % de rebote en ~0,3 s.
Coordenadas de pantalla (px de 1080p)."""
import math
import os

import numpy as np

import plano as P
from motor import W, H, circulo, elipse, rect_red, h01, ancho_texto, clamp01, smooth, prog

# morado, magenta, naranja, azul, teal: los colores de etiqueta del original
COL = dict(morado=(122, 52, 200), magenta=(214, 52, 128), naranja=(240, 130, 36), azul=(40, 110, 230), teal=(30, 170, 170), blanco=(255, 255, 255), rojo=(222, 60, 70),
           verde=(60, 168, 96), oro=(250, 190, 40), oscuro=(34, 28, 80))

_POP = np.array([(0.0, 0.0), (0.0167, 0.09), (0.15, 0.92), (0.20, 0.985), (0.25, 1.012), (0.30, 1.014), (0.40, 1.005), (0.55, 1.0)])


def pop(t, t0, lento=1.0):
    """Escala de aparición con la curva medida del original. 0 antes de t0; `lento` estira el tiempo (1.5 = más pausado)."""
    tau = (t - t0) / lento
    if tau <= 0:
        return 0.0
    if tau >= _POP[-1, 0]:
        return 1.0
    return float(np.interp(tau, _POP[:, 0], _POP[:, 1]))


def repop(t, t0, amp=0.12, dur=0.32):
    """Latido de énfasis: la etiqueta vuelve a «saltar» un poco (1 -> 1+amp -> 1) a partir de t0."""
    u = (t - t0) / dur
    if u <= 0 or u >= 1:
        return 1.0
    return 1.0 + amp * math.sin(math.pi * u) ** 1.5


def salida(t, t1, dur=0.18):
    """1 hasta t1; baja a 0 en dur (se encoge)."""
    return 1.0 - smooth(prog(t, t1, t1 + dur))


# ------------------------------------------------------------------------------------------------ etiquetas
def vaciar_diferidos(lz):
    """Dibuja las etiquetas sin cola que se dejaron para el final del cuadro, separándolas de la fecha de la esquina y entre sí."""
    dif, lz.dif = list(getattr(lz, "dif", []) or []), []
    for d in dif:
        llamada(lz, cola=None, clamp=True, _dif=True, **d)
    lz.dif = []


def _registrar(lz, cx, cy, w, h):
    z = getattr(lz, "zonas_rot", None)
    if z is not None:
        z.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))


def _sin_choques(lz, cx, cy, w, h, sep=16.0):
    """Mueve el centro (cx, cy) de una etiqueta SIN cola lo mínimo (a un lado o arriba/abajo) para que no tape a otras ya dibujadas en este cuadro ni a la fecha de la esquina."""
    zonas = getattr(lz, "zonas_rot", None)
    if not zonas:
        return cx, cy
    def libre(x, y):
        if x - w / 2 < 16 or x + w / 2 > W - 16 or y - h / 2 < 16 or y + h / 2 > H - 16:
            return None
        for (a, b, c, d) in zonas:
            if x + w / 2 > a - sep / 2 and x - w / 2 < c + sep / 2 and y + h / 2 > b - sep / 2 and y - h / 2 < d + sep / 2:
                return (a, b, c, d)
        return False
    for _ in range(6):
        z = libre(cx, cy)
        if z is False:
            return cx, cy
        if z is None:
            break
        a, b, c, d = z
        opc = [(c + w / 2 + sep, cy), (a - w / 2 - sep, cy), (cx, d + h / 2 + sep), (cx, b - h / 2 - sep)]
        opc.sort(key=lambda p: abs(p[0] - cx) + abs(p[1] - cy))
        for (nx, ny) in opc:
            if libre(nx, ny) is False:
                return nx, ny
        cx, cy = opc[0]
    return cx, cy


def llamada(lz, x, y, texto, color=COL["morado"], px=34, k=1.0, cola="abajo", alfa=1.0, color_texto=(255, 255, 255), capa=2, ancla="centro", sombra=True, clamp=True, _dif=False):
    """Etiqueta rectangular de esquinas suaves con una muesca triangular (cola) que apunta al objeto. (x, y) = punta de la cola (o centro si cola=None).
    clamp=True mantiene la etiqueta dentro del cuadro (la punta se corre al borde seguro si el objeto se sale)."""
    if k <= 0.01 or alfa <= 0.01:
        return
    if cola is None and clamp and not _dif and getattr(lz, "diferir", False):
        lz.dif.append(dict(x=x, y=y, texto=texto, color=color, px=px, k=k, alfa=alfa, color_texto=color_texto, capa=capa, ancla=ancla, sombra=sombra))
        return
    w = ancho_texto(texto, "geo", px) + px * 1.0
    h = px * 1.5
    if clamp:
        nt_ = px * 0.34
        if cola in ("izq", "der"):
            mx = (w + nt_) * k + 24
            x = min(max(x, 24 if cola == "izq" else mx), (W - mx) if cola == "izq" else W - 24)
            y = min(max(y, h / 2 * k + 24), H - h / 2 * k - 24)
        else:
            mx = w / 2 * k + 24
            x = min(max(x, mx), W - mx)
            if cola == "abajo":
                y = min(max(y, (h + nt_) * k + 24), H - 24)
            elif cola == "arriba":
                y = min(max(y, 24), H - (h + nt_) * k - 24)
            else:
                y = min(max(y, h / 2 * k + 24), H - h / 2 * k - 24)
    nt = px * 0.34
    if cola is None and clamp:
        x, y = _sin_choques(lz, x, y, w * k, h * k)
        _registrar(lz, x, y, w * k, h * k)
    with lz.capa(capa):
        with lz.grupo(x, y, k):
            if cola == "abajo":
                ox, oy = -w / 2, -h - nt
            elif cola == "arriba":
                ox, oy = -w / 2, nt
            elif cola == "izq":
                ox, oy = nt, -h / 2
            elif cola == "der":
                ox, oy = -w - nt, -h / 2
            else:
                ox, oy = -w / 2, -h / 2
            if sombra:
                lz.relleno(rect_red(ox + 3, oy + 5, w, h, px * 0.30), (10, 6, 40), alfa=0.22 * alfa)
            lz.relleno(rect_red(ox, oy, w, h, px * 0.30), color, alfa=alfa)
            if cola == "abajo":
                lz.relleno(np.array([[-nt, -nt - 0.5], [nt, -nt - 0.5], [0, 0]]), color, alfa=alfa)
            elif cola == "arriba":
                lz.relleno(np.array([[-nt, nt + 0.5], [nt, nt + 0.5], [0, 0]]), color, alfa=alfa)
            elif cola == "izq":
                lz.relleno(np.array([[nt + 0.5, -nt], [nt + 0.5, nt], [0, 0]]), color, alfa=alfa)
            elif cola == "der":
                lz.relleno(np.array([[-nt - 0.5, -nt], [-nt - 0.5, nt], [0, 0]]), color, alfa=alfa)
            lz.texto(texto, ox + w / 2, oy + h / 2 + px * 0.04, px, "geo", color=color_texto, borde=None, alfa=alfa, temblor=0.0)


def globo(lz, x, y, texto, px=36, k=1.0, color=(255, 255, 255), color_texto=COL["morado"], alfa=1.0, cola="abajo", lado=1):
    """Globo de diálogo redondeado (cápsula) con colita curva. (x, y) = punta de la cola."""
    if k <= 0.01 or alfa <= 0.01:
        return
    w = ancho_texto(texto, "geo", px) + px * 1.2
    h = px * 1.7
    with lz.capa(2):
        with lz.grupo(x, y, k):
            ox, oy = -w / 2 + lado * w * 0.12, -h - px * 0.55
            lz.relleno(rect_red(ox + 3, oy + 5, w, h, h / 2), (10, 6, 40), alfa=0.20 * alfa)
            lz.relleno(rect_red(ox, oy, w, h, h / 2), color, alfa=alfa)
            lz.relleno(np.array([[ox + w * 0.30 * (1 if lado > 0 else 3), oy + h - 2], [ox + w * 0.30 * (1 if lado > 0 else 3) + px * 0.7, oy + h - 2], [0, 0]]), color, alfa=alfa)
            lz.texto(texto, ox + w / 2, oy + h / 2 + px * 0.04, px, "geo", color=color_texto, borde=None, alfa=alfa, temblor=0.0)


def insignia(lz, x, y, n, color=COL["azul"], r=22, k=1.0, alfa=1.0):
    if k <= 0.01:
        return
    with lz.capa(2):
        with lz.grupo(x, y, k):
            lz.relleno(circulo(0, 0, r + 4, 24), (255, 255, 255), alfa=alfa * 0.9)
            lz.relleno(circulo(0, 0, r, 24), color, alfa=alfa)
            lz.texto(str(n), 0, r * 0.04, int(r * 1.15), "geo", color=(255, 255, 255), borde=None, alfa=alfa, temblor=0.0)


def fecha_lugar(lz, t, t0, t1, lugar, fecha, x=70, y=70, col_lugar=COL["morado"], col_fecha=(255, 255, 255)):
    """Rótulo de esquina: lugar en cápsula de color y fecha grande debajo (entra con pop, sale encogiéndose)."""
    a = pop(t, t0) * salida(t, t1)
    if a <= 0.01:
        return
    wl = ancho_texto(lugar, "geo", 36) + 44
    wf = ancho_texto(fecha, "geo", 58) + 8
    _registrar(lz, x + max(wl, wf) / 2, y + 62, max(wl, wf) * a, 160 * a)
    with lz.capa(2):
        with lz.grupo(x, y + 26, a):
            lz.relleno(rect_red(3, 5 - 26, wl, 54, 16), (10, 6, 40), alfa=0.22)
            lz.relleno(rect_red(0, -26, wl, 54, 16), col_lugar)
            lz.texto(lugar, wl / 2, 1, 36, "geo", color=(255, 255, 255), borde=None, temblor=0.0)
        P.rotulo(lz, x + 4, y + 112, fecha, px=58, k=a, color=col_fecha, ancla=(0.0, 0.5), sombra=0.5)


def titulo_grande(lz, t, t0, t1, texto, x=W / 2, y=130, px=96, color=(255, 255, 255), ancla=(0.5, 0.5)):
    a = pop(t, t0, 1.2) * salida(t, t1, 0.3)
    if a > 0.01:
        P.rotulo(lz, x, y, texto, px=px, k=a, color=color, ancla=ancla, alfa=min(1.0, a * 1.4))


# ------------------------------------------------------------------------------------------------ efectos
def chispa4(lz, x, y, r, color=(255, 244, 200), alfa=1.0, rot=0.0, capa=2):
    """Destello de 4 puntas (estrella «+» afilada)."""
    if r <= 0.5 or alfa <= 0.01:
        return
    c, s = math.cos(rot), math.sin(rot)
    pts = []
    for i in range(8):
        a = i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.22
        pts.append((x + math.cos(a) * rr * c - math.sin(a) * rr * s, y + math.cos(a) * rr * s + math.sin(a) * rr * c))
    lz.relleno(np.array(pts), color, alfa=alfa, capa=capa)


def chispas(lz, t, n=18, area=(0, 0, W, H), seed=1, color=(255, 244, 200), tam=(6, 14), vel=0.7):
    """Chispas «+» que titilan (alfa senoidal con frecuencia propia, como las estrellas del original)."""
    x0, y0, x1, y1 = area
    for i in range(n):
        x = x0 + (x1 - x0) * h01(seed, i)
        y = y0 + (y1 - y0) * h01(seed, i + 50)
        a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * (1.5 + 3 * h01(seed, i + 100)) * vel + h01(seed, i + 150) * 6.28))
        chispa4(lz, x, y, tam[0] + (tam[1] - tam[0]) * h01(seed, i + 200), color, a, rot=math.pi / 4 * 0)


def bokeh(lz, t, seed=2, n=14, colores=((255, 240, 120), (255, 90, 160), (110, 90, 255), (255, 150, 90)), r=(30, 110), alfa=0.55, area=(0, 0, W, H)):
    """Discos desenfocados de colores a la deriva (fondo de los primeros planos)."""
    x0, y0, x1, y1 = area
    for i in range(n):
        rr = r[0] + (r[1] - r[0]) * h01(seed, i)
        x = x0 + (x1 - x0) * ((h01(seed, i + 10) + t * 0.01 * (h01(seed, i + 20) - 0.5)) % 1.0)
        y = y0 + (y1 - y0) * ((h01(seed, i + 30) + t * 0.008 * (h01(seed, i + 40) - 0.3)) % 1.0)
        c = colores[int(h01(seed, i + 60) * len(colores)) % len(colores)]
        lz.halo(x, y, rr, c, alfa=alfa * (0.6 + 0.4 * h01(seed, i + 70)), dureza=0.7, capa=0, r0=0.7)


def haces_luz(lz, x, y, t, n=7, largo=1500, color=(255, 220, 255), alfa=0.22, ancho=0.10, rot0=0.0, vel=0.12):
    """Haces de luz que giran lentamente desde (x, y)."""
    for i in range(n):
        a = rot0 + i * 2 * math.pi / n + t * vel
        w = ancho * (0.7 + 0.5 * math.sin(i * 2.1 + t * 0.6) ** 2)
        lz.relleno(np.array([[x, y], [x + math.cos(a - w) * largo, y + math.sin(a - w) * largo], [x + math.cos(a + w) * largo, y + math.sin(a + w) * largo]]), color, alfa=alfa, capa=0)


def ondas_sonoras(lz, x, y, t, t0, dur=1.6, r1=700, n=4, color=(255, 236, 170), ancho=7.0, periodo=0.32, alfa=0.8, capa=2):
    """Anillos que se expanden desde (x, y) a partir de t0 (campanada, explosión, grito)."""
    for k in range(n):
        u = prog(t - k * periodo, t0, t0 + dur)
        if 0 < u < 1:
            rr = r1 * (1 - (1 - u) ** 2)
            a = alfa * (1 - u) ** 1.3
            th = np.linspace(0, 2 * math.pi, 64)
            lz.trazo(np.stack([x + rr * np.cos(th), y + rr * np.sin(th)], 1), (*color[:3], int(255 * a)), ancho * (1 - u * 0.6), cerrado=True, afinar=False, temblor=0.0, capa=capa)


def onda_iso(lz, iso, x, y, t, t0, dur=1.8, r1=160, n=3, color=(255, 236, 170), periodo=0.3, ancho=3.0, z=0.0):
    """Anillos en el SUELO isométrico (elipses) desde (x, y) del mundo."""
    for k in range(n):
        u = prog(t - k * periodo, t0, t0 + dur)
        if 0 < u < 1:
            rr = r1 * (1 - (1 - u) ** 2)
            th = np.linspace(0, 2 * math.pi, 48)
            q = iso.pts(np.column_stack([x + rr * np.cos(th), y + rr * np.sin(th), np.full(48, z)]))
            lz.trazo(q, (*color[:3], int(255 * 0.75 * (1 - u) ** 1.2)), ancho * iso.z * (1 - u * 0.6), cerrado=True, afinar=False, temblor=0.0, capa=2)


def contador(lz, x, y, valor, px=110, color=(255, 255, 255), k=1.0, alfa=1.0, sufijo="", fuente="geo"):
    txt = f"{int(round(valor)):,}".replace(",", ".") + sufijo
    P.rotulo(lz, x, y, txt, px=px, k=k, color=color, alfa=alfa, fuente=fuente)


def viñeta_color(img, color=(20, 8, 60), fuerza=0.35):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
    m = np.clip(r - 0.45, 0, 1) ** 1.4 * fuerza
    return img * (1 - m[..., None]) + np.array(color, np.float32) / 255.0 * m[..., None]


try:                                    # gradacion en un solo paso con numba (~10x más rápida; FAB_SIN_NUMBA=1 la apaga)
    if os.environ.get("FAB_SIN_NUMBA"):
        raise ImportError
    from numba import njit as _njit, prange as _prange

    @_njit(parallel=True, cache=True)
    def _gradacion_nb(img, luces, sombras, contraste, saturacion, out):
        cero, uno, medio, tres = np.float32(0.0), np.float32(1.0), np.float32(0.5), np.float32(3.0)
        kr, kg, kb = np.float32(0.299), np.float32(0.587), np.float32(0.114)
        for y in _prange(img.shape[0]):
            for x in range(img.shape[1]):
                r, g, b = img[y, x, 0], img[y, x, 1], img[y, x, 2]
                w = r * kr + g * kg + b * kb
                w = cero if w < cero else (uno if w > uno else w)
                r = r * (sombras[0] * (uno - w) + luces[0] * w)
                g = g * (sombras[1] * (uno - w) + luces[1] * w)
                b = b * (sombras[2] * (uno - w) + luces[2] * w)
                m = (r + g + b) / tres
                for ch, v in ((0, r), (1, g), (2, b)):
                    v = ((m + (v - m) * saturacion) - medio) * contraste + medio
                    out[y, x, ch] = cero if v < cero else (uno if v > uno else v)
except Exception:
    _gradacion_nb = None


def gradacion(img, luces=(1.02, 1.0, 0.96), sombras=(0.97, 0.98, 1.04), contraste=1.04, saturacion=1.06):
    """Correccion de color simple: luces cálidas y sombras frías, algo de contraste y saturación."""
    if _gradacion_nb is not None and img.dtype == np.float32 and img.ndim == 3 and img.shape[2] == 3:
        out = np.empty(img.shape, np.float32)
        _gradacion_nb(img, np.array(luces, np.float32), np.array(sombras, np.float32), np.float32(contraste),
                      np.float32(saturacion), out)
        return out
    lum = img @ np.array([0.299, 0.587, 0.114], np.float32)
    w = np.clip(lum, 0, 1)[..., None]
    tinte = np.array(sombras, np.float32) * (1 - w) + np.array(luces, np.float32) * w
    out = img * tinte
    g = out.mean(-1, keepdims=True)
    out = g + (out - g) * saturacion
    return np.clip((out - 0.5) * contraste + 0.5, 0, 1).astype(np.float32)


def pergamino_grande(lz, x, y, w, h, t, t0, lineas=(), titulo=None, sello=True, rot=0.0, alfa=1.0, color=(252, 240, 208), tinta=(110, 70, 50)):
    """Pergamino enrollado en pantalla que se despliega con «pop»: titulo en negrita, líneas de texto simuladas, sello de lacre rojo con cinta. (x, y) = centro."""
    k = pop(t, t0, 1.3)
    if k <= 0.01:
        return
    ab = min(1.0, k)
    ww, hh = w * ab, h
    with lz.capa(2):
        with lz.grupo(x, y, k if k > 1 else 1.0, rot):
            lz.relleno(rect_red(-ww / 2 + 8, -hh / 2 + 12, ww, hh, 10), (20, 10, 50), alfa=0.25 * alfa)
            for sg in (-1, 1):
                lz.relleno(rect_red(sg * ww / 2 - 13, -hh / 2 - 16, 26, hh + 32, 13), (214, 176, 126), alfa=alfa)
                lz.relleno(rect_red(sg * ww / 2 - 13, -hh / 2 - 16, 10, hh + 32, 5), (236, 206, 156), alfa=alfa)
                lz.relleno(circulo(sg * ww / 2, -hh / 2 - 16, 14, 14), (190, 150, 104), alfa=alfa)
                lz.relleno(circulo(sg * ww / 2, hh / 2 + 16, 14, 14), (190, 150, 104), alfa=alfa)
            lz.relleno(rect_red(-ww / 2, -hh / 2, ww, hh, 6), color, alfa=alfa)
            lz.relleno(rect_red(-ww / 2, -hh / 2, ww, 14, 4), P.oscurecer(color, 0.10), alfa=alfa * 0.8)
            if titulo:
                lz.texto(titulo, 0, -hh / 2 + 62, 52, "geo", color=tinta, borde=None, alfa=alfa * min(1, ab * 1.4), temblor=0.0)
            for i, ln in enumerate(lineas):
                lz.texto(ln, 0, -hh / 2 + 130 + i * 52, 34, "geo_n", color=tinta, borde=None, alfa=alfa * min(1, ab * 1.4) * 0.9, temblor=0.0)
            if sello:
                lz.relleno(np.array([[ww / 2 - 120, hh / 2 - 40], [ww / 2 - 96, hh / 2 + 36], [ww / 2 - 72, hh / 2 - 40]]), (60, 130, 200), alfa=alfa)
                lz.relleno(circulo(ww / 2 - 96, hh / 2 - 44, 40, 20), (170, 40, 52), alfa=alfa)
                lz.relleno(circulo(ww / 2 - 96, hh / 2 - 44, 30, 20), (206, 60, 70), alfa=alfa)
                lz.relleno(circulo(ww / 2 - 96, hh / 2 - 44, 15, 14), (170, 40, 52), alfa=alfa)
                chispa4(lz, ww / 2 - 96, hh / 2 - 44, 12 * (0.8 + 0.2 * math.sin(t * 5)), (255, 224, 190), 0.9)
