# -*- coding: utf-8 -*-
"""Kit TÁCTICO: análisis de jugadas «como en la NFL» sobre gameplay real (prueba LoL Worlds 2026, `videos/lol_worlds_tl_al/`).
Dos piezas, ambas devuelven fn(dt, dur, marcas) -> BGRA 1920x1080 para el FX `mg`/`pantalla` de nucleo/secuencia_fx.py:

  pizarra(de, elementos)      telestrador sobre un cuadro CONGELADO (FX `video` con vel=0 debajo): anillos en el suelo bajo
                              cada campeón, flechas que se dibujan solas, zonas, etiquetas y foco (oscurece lo demás).
  tablero(de, mapa, ...)      mapa táctico de la Grieta inclinado en 3D (cámara con zoom/paneo), fichas de campeón con su
                              icono REAL que se mueven por rutas, oleadas, TP, centinelas, niebla, flechas y etiquetas.

Tiempos de los elementos: SEGUNDOS ABSOLUTOS del video (los de la voz en timeline.json); `de` = inicio del FX.
Coordenadas: pizarra en fracción del cuadro (x, y 0..1); tablero en fracción del mapa (u, v 0..1, azul abajo-izquierda).
Colores RGB por nombre: azul (TL/lado azul), rojo (lado rojo), amarillo (telestrador), blanco.

Elementos (dict con `tipo`):
  anillo  x y [r=70] color en [etiqueta, sub, lado="arriba"|"abajo"|"izq"|"der"] [sale]
  flecha  pts=[(x,y),...] color en [dur=.6, ancho=9, guion=False, etiqueta, punta=True] [sale]
  zona    pts=[(x,y),...] color en [alfa=.22, etiqueta] [sale]
  texto   x y texto color en [tam=40, sub] [sale]
  foco    en [k=.45, sale]                 oscurece todo menos los anillos visibles
  -- solo tablero --
  ficha   campeon equipo ruta=[(t,u,v),...] [en, sale, nombre]    icono que sigue la ruta (interpola entre tiempos)
  oleada  ruta=[(u,v),...] de a color [n=6]                        puntitos que avanzan por un carril
  tp      desde=(u,v) a=(u,v) en [dur=1.2] color                   línea punteada + remolino de teletransporte
  ward    u v en color [radio=.06]                                 ojo con círculo de visión
  niebla  pts=[(u,v),...] en [k=.55] [sale]                         región sin visión (oscura)
  num     u v n color en                                            paso numerado (1, 2, 3)
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
COLORES = dict(azul=(70, 165, 255), rojo=(255, 68, 82), amarillo=(255, 214, 10), blanco=(255, 255, 255),
               verde=(60, 230, 140), naranja=(255, 140, 30), gris=(150, 160, 175))
_FD = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]
_FUENTES = dict(negra=("Poppins-Black.ttf", "seguibl.ttf"), xbold=("Poppins-ExtraBold.ttf", "segoeuib.ttf"),
                semi=("Poppins-SemiBold.ttf", "seguisb.ttf"))
_cache = {}


def fuente(nombre, tam):
    k = ("f", nombre, tam)
    if k not in _cache:
        for arch in _FUENTES[nombre]:
            for d in _FD:
                if os.path.exists(os.path.join(d, arch)):
                    _cache[k] = ImageFont.truetype(os.path.join(d, arch), tam)
                    break
            if k in _cache:
                break
        else:
            _cache[k] = ImageFont.load_default()
    return _cache[k]


def _rgb(c):
    return COLORES.get(c, c) if isinstance(c, str) else tuple(c)


def _bgra(c, a=255):
    r, g, b = _rgb(c)
    return (b, g, r, a)


clamp = lambda u: max(0.0, min(1.0, u))
ease = lambda u: u * u * (3 - 2 * u)


def _eo(u):                              # ease-out cúbico
    u = clamp(u)
    return 1 - (1 - u) ** 3


def _pop(dt, dur=.32):
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1 else 1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2


def _vida(d, t):
    """0..1 de presencia del elemento (entra rápido, sale fundiendo .3 s si tiene `sale`)."""
    if t < d["en"]:
        return 0.0
    s = d.get("sale")
    if s is not None and t >= s:
        return clamp(1 - (t - s) / .3)
    return 1.0


# ------------------------------------------------------------------ composición
def _visible(a):
    """Recuadro (x, y, w, h) de lo no transparente de un canal alfa (w = 0 si está vacío). cv2 lo hace en C, ~1 ms en 1080p."""
    return cv2.boundingRect(np.ascontiguousarray(a))


def _sobre(dst, src, x, y, alfa=1.0):
    """Pega src (BGRA uint8) sobre dst (BGRA uint8) con su esquina en (x, y). Solo trabaja en el recuadro con algo visible
    (las capas a cuadro entero casi siempre están vacías) y, si dst es opaco, con la fórmula corta."""
    if alfa <= 0:
        return
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    if s.shape[0] * s.shape[1] > 65536:
        bx, by, bw, bh = _visible(s[..., 3])
        if bw == 0:
            return
        s = s[by:by + bh, bx:bx + bw]
        x0, y0 = x0 + bx, y0 + by
        x1, y1 = x0 + bw, y0 + bh
    d = dst[y0:y1, x0:x1]
    a = s[..., 3].astype(np.float32) * (alfa / 255)
    da = d[..., 3].astype(np.float32) * (1 / 255)
    if da.min() >= 1:                                  # destino opaco: rgb = s·a + d·(1 - a), alfa queda en 255
        d[..., :3] = cv2.blendLinear(np.ascontiguousarray(s[..., :3]), np.ascontiguousarray(d[..., :3]), a, 1 - a)
        return
    k = da * (1 - a)
    oa = a + k
    inv = 1 / np.maximum(oa, 1e-4)
    for c in range(3):
        d[..., c] = ((s[..., c] * a + d[..., c] * k) * inv).clip(0, 255)
    d[..., 3] = (oa * 255).clip(0, 255)


def _capa():
    return np.zeros((H, W, 4), np.uint8)


def _brillo(capa, radio=9, fuerza=.75):
    """Halo suave de lo dibujado (a media resolución, solo en el recuadro de lo dibujado más el margen del halo)."""
    bx, by, bw, bh = _visible(capa[..., 3])
    out = _capa()
    if bw == 0:
        return out
    m = int(radio * 8)                                 # margen: ~4 sigmas del desenfoque a media resolución
    x0, y0 = max(0, (bx - m) // 2 * 2), max(0, (by - m) // 2 * 2)
    x1, y1 = min(W, (bx + bw + m + 1) // 2 * 2), min(H, (by + bh + m + 1) // 2 * 2)
    reg = capa[y0:y1, x0:x1]
    peq = cv2.resize(reg, ((x1 - x0) // 2, (y1 - y0) // 2), interpolation=cv2.INTER_AREA).astype(np.float32)
    peq = cv2.GaussianBlur(peq, (0, 0), radio)
    g = cv2.resize(peq, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
    g[..., 3] *= fuerza
    o = g.clip(0, 255).astype(np.uint8)
    _sobre(o, reg, 0, 0)
    out[y0:y1, x0:x1] = o
    return out


def pildora(texto, color="amarillo", tam=38, sub=None, icono=None):
    """Etiqueta de transmisión: fondo oscuro, barra de color a la izquierda, texto blanco (y subtítulo de color)."""
    k = ("p", texto, color, tam, sub, icono)
    if k in _cache:
        return _cache[k]
    f1, f2 = fuente("negra", tam), fuente("semi", int(tam * .62))
    pad, barra = int(tam * .42), int(tam * .2)
    ico = None
    if icono:
        ico = Image.open(icono).convert("RGBA").resize((int(tam * 1.25),) * 2, Image.LANCZOS)
    tw = f1.getbbox(texto)[2]
    sw = f2.getbbox(sub)[2] if sub else 0
    ih = int(tam * 1.25) if ico else 0
    w = barra + pad + (ih + pad if ico else 0) + max(tw, sw) + pad
    h = int(tam * 1.32) + (int(tam * .8) if sub else 0)
    h = max(h, ih + 2 * int(pad * .6))
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 6, w + 4, h + 6), radius=int(tam * .28), fill=(0, 0, 0, 120))     # sombra
    d.rounded_rectangle((0, 0, w, h), radius=int(tam * .28), fill=(10, 14, 26, 236))
    d.rounded_rectangle((0, 0, barra + 6, h), radius=int(tam * .28), fill=_rgb(color) + (255,))
    d.rectangle((barra, 0, barra + 6, h), fill=(10, 14, 26, 236))
    x = barra + pad
    if ico:
        im.paste(ico, (x, (h - ih) // 2), ico)
        x += ih + pad
    d.text((x, int(tam * .1)), texto, font=f1, fill=(255, 255, 255, 255))
    if sub:
        d.text((x, int(tam * 1.22)), sub, font=f2, fill=_rgb(color) + (255,))
    arr = np.array(im)[..., [2, 1, 0, 3]].copy()
    _cache[k] = arr
    return arr


def _pegar_centro(capa, im, cx, cy, escala=1.0, alfa=1.0):
    if escala <= .02 or alfa <= 0:
        return
    if abs(escala - 1) > .01:
        im = cv2.resize(im, None, fx=escala, fy=escala, interpolation=cv2.INTER_LINEAR)
    _sobre(capa, im, int(cx - im.shape[1] / 2), int(cy - im.shape[0] / 2), alfa)


# ------------------------------------------------------------------ geometría
def _curva(pts, n=60):
    """Catmull-Rom por los puntos (px) -> polilínea densa."""
    p = np.array(pts, np.float32)
    if len(p) == 2:
        return np.linspace(p[0], p[1], n)
    p = np.vstack([p[0] * 2 - p[1], p, p[-1] * 2 - p[-2]])
    out = []
    seg = max(2, n // (len(p) - 3))
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for s in np.linspace(0, 1, seg, endpoint=False):
            s2, s3 = s * s, s * s * s
            out.append(.5 * (2 * p1 + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s2 + (-p0 + 3 * p1 - 3 * p2 + p3) * s3))
    out.append(p[-2])
    return np.array(out, np.float32)


def _parcial(c, u):
    """Primer tramo de la polilínea c hasta la fracción u de su longitud."""
    if u >= 1:
        return c
    L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))]
    obj = L[-1] * u
    k = int(np.searchsorted(L, obj))
    if k <= 0:
        return c[:1]
    a = (obj - L[k - 1]) / max(L[k] - L[k - 1], 1e-6)
    return np.vstack([c[:k], c[k - 1] + (c[k] - c[k - 1]) * a])


def _trazo(capa, c, color, ancho, guion=False, punta=True, contorno=True):
    if len(c) < 2:
        return
    pts = np.round(c).astype(np.int32)
    if guion:                                          # discontinua: tramos de ~26 px
        L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))]
        on = (L // 26) % 2 == 0
        segs = [pts[i:i + 2] for i in range(len(pts) - 1) if on[i]]
    else:
        segs = [pts]
    if contorno:
        for s in segs:
            cv2.polylines(capa, [s], False, (0, 0, 0, 200), ancho + 6, cv2.LINE_AA)
    for s in segs:
        cv2.polylines(capa, [s], False, _bgra(color), ancho, cv2.LINE_AA)
    if punta and len(c) >= 3:
        a, b = c[-1], c[max(0, len(c) - 6)]
        v = a - b
        n = np.linalg.norm(v)
        if n > 1:
            v /= n
            q = np.array([-v[1], v[0]])
            L = ancho * 3.2
            tri = np.array([a + v * L * .35, a - v * L + q * L * .7, a - v * L - q * L * .7], np.int32)
            if contorno:
                cv2.polylines(capa, [tri], True, (0, 0, 0, 200), 6, cv2.LINE_AA)
            cv2.fillPoly(capa, [tri], _bgra(color), cv2.LINE_AA)


def _elipse(capa, cx, cy, rx, ry, color, u=1.0, ancho=6, relleno=.22, pulso=None):
    """Anillo en el suelo: el borde crece como un trazo (u 0..1), relleno translúcido y onda que late."""
    cx, cy, rx, ry = int(cx), int(cy), max(int(rx), 2), max(int(ry), 2)
    if relleno and u > .2:
        f = _capa()
        cv2.ellipse(f, (cx, cy), (rx, ry), 0, 0, 360, _bgra(color), -1, cv2.LINE_AA)
        _sobre(capa, f[max(cy - ry - 2, 0):cy + ry + 3, max(cx - rx - 2, 0):cx + rx + 3],
               max(cx - rx - 2, 0), max(cy - ry - 2, 0), relleno * ease(clamp((u - .2) / .8)))
    ang = int(360 * _eo(u))
    cv2.ellipse(capa, (cx, cy), (rx, ry), 0, -90, -90 + ang, (0, 0, 0, 200), ancho + 5, cv2.LINE_AA)
    cv2.ellipse(capa, (cx, cy), (rx, ry), 0, -90, -90 + ang, _bgra(color), ancho, cv2.LINE_AA)
    if pulso is not None and u >= 1:
        p = pulso % 1.3 / 1.3
        if p < .8:
            a = int(220 * (1 - p / .8))
            cv2.ellipse(capa, (cx, cy), (int(rx * (1 + p * .7)), int(ry * (1 + p * .7))), 0, 0, 360, _bgra(color, a), 3,
                        cv2.LINE_AA)


def _etiqueta_junto(capa, im, cx, cy, r, lado, alfa, dt):
    """Pone la píldora a un lado del anillo con una línea guía."""
    h, w = im.shape[:2]
    gap = r + 34
    ox, oy = dict(arriba=(0, -gap - h / 2), abajo=(0, gap * .55 + h / 2), izq=(-gap - w / 2, 0), der=(gap + w / 2, 0))[lado]
    s = _pop(dt)
    tx, ty = cx + ox, cy + oy
    cv2.line(capa, (int(cx + ox * .35), int(cy + oy * .35)), (int(tx - ox * .2 * (lado in ("izq", "der"))),
                                                          int(ty + (h / 2 if lado == "arriba" else -h / 2 if lado == "abajo" else 0))),
             (255, 255, 255, int(200 * alfa)), 2, cv2.LINE_AA)
    _pegar_centro(capa, im, tx, ty, s, alfa)


# ------------------------------------------------------------------ PIZARRA (cuadro congelado)
def pizarra(de, elementos, pausa=None, reloj=None):
    """Telestrador sobre el cuadro congelado. `pausa` = texto del chip superior («PAUSA»); `reloj` = «40:16»."""
    els = [dict(e) for e in elementos]

    def fn(dt, dur, marcas):
        t = de + dt
        trazos, encima, out = _capa(), _capa(), _capa()
        focos = [e for e in els if e["tipo"] == "foco" and _vida(e, t) > 0]
        if focos:                                      # oscurece todo menos los anillos visibles
            k = max(e.get("k", .45) * _vida(e, t) * ease(clamp((t - e["en"]) / .4)) for e in focos)
            m = np.full((H // 4, W // 4), k, np.float32)
            for e in els:
                if e["tipo"] == "anillo" and _vida(e, t) > 0:
                    r = e.get("r", 70) * 1.7 / 4
                    cv2.ellipse(m, (int(e["x"] * W / 4), int(e["y"] * H / 4)), (int(r * 1.15), int(r * .8)), 0, 0, 360, 0, -1)
            m = cv2.resize(cv2.GaussianBlur(m, (0, 0), 6), (W, H))
            out[..., 3] = (m * 255).astype(np.uint8)      # el foco es la capa de ABAJO: no apaga flechas ni etiquetas
        for e in els:
            v = _vida(e, t)
            if v <= 0:
                continue
            d = t - e["en"]
            tipo, col = e["tipo"], e.get("color", "amarillo")
            if tipo == "anillo":
                r = e.get("r", 70)
                cx, cy = e["x"] * W, e["y"] * H
                _elipse(trazos, cx, cy, r, r * .48, col, clamp(d / .4), pulso=d)
                if e.get("etiqueta"):
                    _etiqueta_junto(encima, pildora(e["etiqueta"], col, e.get("tam", 34), e.get("sub"), e.get("icono")),
                                    cx, cy - r * .2, r * .5, e.get("lado", "arriba"), v, d - .15)
            elif tipo == "flecha":
                c = _curva([(x * W, y * H) for x, y in e["pts"]])
                u = _eo(d / e.get("dur", .6))
                _trazo(trazos, _parcial(c, u), col, e.get("ancho", 9), e.get("guion", False), e.get("punta", True))
                if e.get("etiqueta") and u >= 1:
                    m_ = c[len(c) // 2]
                    off = e.get("off", (0, -50))
                    _pegar_centro(encima, pildora(e["etiqueta"], col, e.get("tam", 30), e.get("sub")), m_[0] + off[0],
                                  m_[1] + off[1], _pop(d - e.get("dur", .6)), v)
            elif tipo == "zona":
                p = np.array([(x * W, y * H) for x, y in e["pts"]], np.int32)
                z = _capa()
                cv2.fillPoly(z, [p], _bgra(col), cv2.LINE_AA)
                _sobre(trazos, z, 0, 0, e.get("alfa", .22) * ease(clamp(d / .4)))
                cv2.polylines(trazos, [p], True, _bgra(col, int(255 * ease(clamp(d / .4)))), 4, cv2.LINE_AA)
            elif tipo == "texto":
                _pegar_centro(encima, pildora(e["texto"], col, e.get("tam", 40), e.get("sub"), e.get("icono")),
                              e["x"] * W, e["y"] * H, _pop(d), v)
            if v < 1 and tipo in ("anillo", "flecha", "zona"):
                pass                                   # el fundido de salida se hace por capa abajo
        salen = [e for e in els if e.get("sale") is not None and e["tipo"] in ("anillo", "flecha", "zona")]
        if salen and all(_vida(e, t) < 1 for e in salen) and all(e.get("sale") is not None for e in els
                                                                 if e["tipo"] in ("anillo", "flecha", "zona")):
            k = max(_vida(e, t) for e in salen)
            trazos[..., 3] = (trazos[..., 3] * k).astype(np.uint8)
        _sobre(out, _brillo(trazos), 0, 0)
        _sobre(out, encima, 0, 0)
        if pausa:                                      # chip de transmisión: ❚❚ PAUSA · reloj
            _hud_pausa(out, pausa, reloj, dt)
        return out

    return fn


def _hud_pausa(capa, texto, reloj, dt):
    a = clamp(dt / .25)
    chip = pildora(texto, "amarillo", 36, None)
    x, y = 70, 150
    _sobre(capa, chip, x + 58, y, a)
    h = chip.shape[0]
    # icono de pausa (dos barras) en un círculo amarillo
    cx, cy = x + 24, y + h // 2 - 2
    cv2.circle(capa, (cx, cy), 26, (10, 214, 255, int(255 * a)), -1, cv2.LINE_AA)
    for dx in (-8, 8):
        cv2.rectangle(capa, (cx + dx - 4, cy - 11), (cx + dx + 4, cy + 11), (26, 14, 10, int(255 * a)), -1)
    if reloj:
        r = pildora(reloj, "blanco", 28)
        _sobre(capa, r, x + 58 + chip.shape[1] + 8, y + (h - r.shape[0]) // 2, a)


def chip(texto, color="amarillo", tam=38, sub=None, icono=None, x=.5, y=.5, de=0.0):
    """Píldora suelta para el FX `mg` (x, y del FX la colocan): entra con rebote."""
    im = pildora(texto, color, tam, sub, icono)

    def fn(dt, dur, marcas):
        s = _pop(dt)
        if s <= .02:
            return np.zeros((8, 8, 4), np.uint8)
        return cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR) if abs(s - 1) > .01 else im

    return fn


def rebobinar(texto="REBOBINANDO", sub=None):
    """Capa de cinta rebobinando (rayas, banda brillante que sube, chip ◀◀) para poner sobre un FX `video` con vel < 0.
    El FX `tv` del motor no sirve aquí: se aplica antes que el FX `video` y el clip lo tapa."""
    def fn(dt, dur, marcas):
        out = _capa()
        rng = np.random.default_rng(int(dt * 60))
        for _ in range(14):                            # rayas horizontales de cinta
            y = int(rng.integers(0, H))
            cv2.line(out, (0, y), (W, y), (255, 255, 255, int(rng.integers(40, 120))), int(rng.integers(1, 4)))
        yb = int(H - (dt * 900) % (H + 200))           # banda brillante que sube
        cv2.rectangle(out, (0, yb), (W, yb + 60), (255, 255, 255, 60), -1)
        cv2.rectangle(out, (0, 0), (W, H), (40, 20, 10, 70), -1)
        c = pildora(texto, "amarillo", 46, sub)
        x, y = W // 2 - c.shape[1] // 2 + 40, int(H * .44)
        _sobre(out, c, x, y)
        cx, cy = x - 60, y + c.shape[0] // 2 - 2
        cv2.circle(out, (cx, cy), 40, (10, 214, 255, 255), -1, cv2.LINE_AA)
        for dx in (-14, 8):                            # ◀◀
            tri = np.array([[cx + dx - 10, cy], [cx + dx + 10, cy - 16], [cx + dx + 10, cy + 16]], np.int32)
            cv2.fillPoly(out, [tri], (26, 14, 10, 255), cv2.LINE_AA)
        return out

    return fn


# ------------------------------------------------------------------ TABLERO (mapa táctico 3D)
def _mapa_base(ruta, lado=1600):
    k = ("mapa", ruta, lado)
    if k in _cache:
        return _cache[k]
    im = cv2.imread(ruta, cv2.IMREAD_COLOR)
    im = cv2.resize(im, (lado, lado), interpolation=cv2.INTER_LANCZOS4)
    im = cv2.GaussianBlur(im, (0, 0), 1.2)
    f = im.astype(np.float32)
    muro = (f.mean(axis=2) < 40).astype(np.float32)
    # paleta de pizarra táctica: muros azul noche, caminos pizarra, río verde azulado; bases con su color de equipo
    tinte = f * np.array([.62, .60, .52], np.float32) + np.array([20, 12, 6], np.float32)
    tinte = tinte * (1 - muro[..., None]) + np.array([46, 28, 16], np.float32) * muro[..., None]
    # rejilla fina
    g = np.zeros((lado, lado), np.float32)
    for i in range(0, lado, lado // 16):
        g[:, i:i + 2] = 1
        g[i:i + 2, :] = 1
    tinte += g[..., None] * 10
    # relieve: sombra de los muros hacia abajo-derecha (los caminos se ven hundidos)
    sombra = cv2.GaussianBlur(np.roll(np.roll(muro, 6, 0), 4, 1), (0, 0), 4)
    tinte *= (1 - .35 * sombra * (1 - muro))[..., None]
    borde = np.zeros((lado, lado), np.float32)
    cv2.rectangle(borde, (0, 0), (lado - 1, lado - 1), 1, 10)
    tinte = tinte * (1 - borde[..., None]) + np.array([200, 170, 90], np.float32) * borde[..., None]
    out = tinte.clip(0, 255).astype(np.uint8)
    _cache[k] = out
    return out


def _icono_ficha(ruta, equipo, d=96):
    k = ("ficha", ruta, equipo, d)
    if k in _cache:
        return _cache[k]
    ico = cv2.imread(ruta, cv2.IMREAD_COLOR)
    ico = cv2.resize(ico, (d, d), interpolation=cv2.INTER_AREA)
    D = d + 16
    out = np.zeros((D, D, 4), np.uint8)
    m = np.zeros((d, d), np.uint8)
    cv2.circle(m, (d // 2, d // 2), d // 2 - 1, 255, -1, cv2.LINE_AA)
    cv2.circle(out, (D // 2, D // 2), D // 2 - 1, (0, 0, 0, 230), -1, cv2.LINE_AA)
    cv2.circle(out, (D // 2, D // 2), D // 2 - 4, _bgra(equipo), -1, cv2.LINE_AA)
    sub = out[8:8 + d, 8:8 + d]
    a = (m.astype(np.float32) / 255)[..., None]
    sub[..., :3] = (ico * a + sub[..., :3] * (1 - a)).astype(np.uint8)
    sub[..., 3] = np.maximum(sub[..., 3], m)
    _cache[k] = out
    return out


def _interp(ruta, t):
    """ruta = [(t, u, v), ...] -> (u, v) en t (suave entre puntos)."""
    if t <= ruta[0][0]:
        return ruta[0][1:]
    for (t0, u0, v0), (t1, u1, v1) in zip(ruta, ruta[1:]):
        if t <= t1:
            s = ease(clamp((t - t0) / max(t1 - t0, 1e-6)))
            return u0 + (u1 - u0) * s, v0 + (v1 - v0) * s
    return ruta[-1][1:]


def tablero(de, mapa, elementos, camara=((0, .5, .5, 1.0),), titulo="MAPA TÁCTICO", reloj=None, hud=None, iconos="",
            inclinacion=40):
    """Mapa táctico inclinado. camara = [(t_abs, u_centro, v_centro, zoom), ...]; reloj = [(t_abs, "40:16"), ...];
    hud = [(t_abs, texto, color, sub[, t_fin]), ...] píldoras que se apilan arriba a la derecha; iconos = carpeta de iconos."""
    els = [dict(e) for e in elementos]
    LADO = 1600
    base = _mapa_base(mapa, LADO)
    fondo = np.zeros((H, W, 3), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .55) / H) ** 2)
    fondo[:] = np.array([30, 20, 12], np.float32)
    fondo *= (1.25 - rr * 1.3).clip(.25, 1.25)[..., None]
    fondo = fondo.clip(0, 255).astype(np.uint8)
    # inclinación: el plano del mapa se gira `inclinacion` grados sobre el eje X y se mira con una cámara a distancia D
    # (lo de arriba queda más lejos y más chico, y el mapa se acorta en vertical como un campo visto desde la grada)
    th, D = math.radians(inclinacion), 1500.0

    def _proy(x, y):
        X, Y = x - W / 2, y - H / 2
        Z = D - Y * math.sin(th)
        return W / 2 + D * X / Z, H * .55 + D * Y * math.cos(th) / Z

    plano = np.float32([[W / 2 - 900, H / 2 - 900], [W / 2 + 900, H / 2 - 900], [W / 2 + 900, H / 2 + 900], [W / 2 - 900, H / 2 + 900]])
    T = cv2.getPerspectiveTransform(plano, np.float32([_proy(*p) for p in plano]))

    def camara_en(t):
        c = sorted(camara)
        if t <= c[0][0]:
            return c[0][1:]
        for a, b in zip(c, c[1:]):
            if t <= b[0]:
                s = ease(clamp((t - a[0]) / max(b[0] - a[0], 1e-6)))
                return tuple(a[i] + (b[i] - a[i]) * s for i in (1, 2, 3))
        return c[-1][1:]

    def fn(dt, dur, marcas):
        t = de + dt
        cu, cv, z = camara_en(t)
        z *= 1 + .02 * math.sin(dt * .5)                # respiración leve de cámara
        L = 1060 * z                                     # lado del mapa en el plano (px)
        S = np.float32([[L / LADO, 0, W / 2 - cu * L], [0, L / LADO, H / 2 - cv * L], [0, 0, 1]])
        M = T @ S

        def P(u, v):
            q = M @ np.array([u * LADO, v * LADO, 1.0])
            return q[0] / q[2], q[1] / q[2]

        def escala(u, v):
            a, b = P(u, v), P(u + .01, v)
            return math.hypot(b[0] - a[0], b[1] - a[1]) / (.01 * 1000)

        f = fondo.copy()
        # canto del tablero (grosor) y sombra
        esq = np.float32([P(0, 0), P(1, 0), P(1, 1), P(0, 1)])
        sombra = esq + np.float32([18, 34])
        cv2.fillPoly(f, [sombra.astype(np.int32)], (6, 4, 2), cv2.LINE_AA)
        canto = np.float32([P(0, 1), P(1, 1), np.array(P(1, 1)) + [0, 22], np.array(P(0, 1)) + [0, 22]])
        cv2.fillPoly(f, [canto.astype(np.int32)], (60, 46, 24), cv2.LINE_AA)
        # el mapa se deforma DIRECTO sobre el fondo (BORDER_TRANSPARENT: fuera del tablero no toca nada; sin máscara ni mezcla)
        cv2.warpPerspective(base, M, (W, H), dst=f, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
        cv2.polylines(f, [esq.astype(np.int32)], True, (200, 170, 90), 3, cv2.LINE_AA)    # borde suave (sin dientes)
        # niebla (antes que lo demás: oscurece el suelo): máscara a 1/4 de resolución, mezcla entera en el recuadro
        for e in els:
            if e["tipo"] == "niebla" and _vida(e, t) > 0:
                k = e.get("k", .55) * _vida(e, t) * ease(clamp((t - e["en"]) / .6))
                n = np.zeros((H // 4, W // 4), np.float32)
                cv2.fillPoly(n, [(np.array([P(u, v) for u, v in e["pts"]]) / 4).astype(np.int32)], 1.0, cv2.LINE_AA)
                n = cv2.resize(cv2.GaussianBlur(n, (0, 0), 4.5) * k, (W, H), interpolation=cv2.INTER_LINEAR)
                bx, by, bw, bh = _visible((n > .004).astype(np.uint8))
                if bw:
                    r = f[by:by + bh, bx:bx + bw]
                    nn = n[by:by + bh, bx:bx + bw, None]
                    nn = np.ascontiguousarray(nn[..., 0])
                    r[:] = cv2.blendLinear(np.full_like(r, (20, 10, 6)), np.ascontiguousarray(r), nn, 1 - nn)
        out = np.empty((H, W, 4), np.uint8)
        out[..., :3] = f
        out[..., 3] = 255
        trazos, fichas, etiq = _capa(), _capa(), _capa()
        for e in els:
            v = _vida(e, t)
            tipo = e["tipo"]
            if v <= 0 or tipo == "niebla":
                continue
            d = t - e["en"]
            col = e.get("color", "amarillo")
            if tipo == "zona":
                p = np.array([P(u, w) for u, w in e["pts"]], np.int32)
                zc = _capa()
                cv2.fillPoly(zc, [p], _bgra(col), cv2.LINE_AA)
                _sobre(trazos, zc, 0, 0, e.get("alfa", .2) * ease(clamp(d / .4)) * v)
                cv2.polylines(trazos, [p], True, _bgra(col, int(230 * v)), 3, cv2.LINE_AA)
            elif tipo == "anillo":
                pts = [P(e["u"] + e.get("r", .045) * math.cos(a_), e["v"] + e.get("r", .045) * math.sin(a_))
                       for a_ in np.linspace(0, 2 * math.pi, 48)]
                p = np.float32(pts)
                cx, cy = p[:, 0].mean(), p[:, 1].mean()
                rx, ry = (p[:, 0].max() - p[:, 0].min()) / 2, (p[:, 1].max() - p[:, 1].min()) / 2
                _elipse(trazos, cx, cy, rx, ry, col, clamp(d / .4), pulso=d)
                if e.get("etiqueta"):
                    _etiqueta_junto(etiq, pildora(e["etiqueta"], col, e.get("tam", 32), e.get("sub"), e.get("icono")),
                                    cx, cy - ry * .2, ry, e.get("lado", "arriba"), v, d - .15)
            elif tipo == "flecha":
                c = _curva([P(u, w) for u, w in e["pts"]])
                u_ = _eo(d / e.get("dur", .7))
                _trazo(trazos, _parcial(c, u_), col, e.get("ancho", 10), e.get("guion", False), e.get("punta", True))
                if e.get("etiqueta") and u_ >= 1:
                    m_ = c[len(c) // 2]
                    off = e.get("off", (0, -46))
                    _pegar_centro(etiq, pildora(e["etiqueta"], col, e.get("tam", 30), e.get("sub")), m_[0] + off[0],
                                  m_[1] + off[1], _pop(d - e.get("dur", .7)), v)
            elif tipo == "oleada":
                ruta = _curva([P(u, w) for u, w in e["ruta"]], 200)
                Ls = np.r_[0, np.cumsum(np.linalg.norm(np.diff(ruta, axis=0), axis=1))]
                prog = clamp((t - e["en"]) / max(e["a"] - e["en"], .1))
                _trazo(trazos, _parcial(ruta, prog), col, 4, True, False, False)
                for i in range(e.get("n", 6)):
                    s = prog * Ls[-1] - i * 22
                    if s < 0:
                        continue
                    k = int(np.searchsorted(Ls, s))
                    k = min(k, len(ruta) - 1)
                    x, y = ruta[k]
                    cv2.circle(trazos, (int(x), int(y)), 11, (0, 0, 0, 220), -1, cv2.LINE_AA)
                    cv2.circle(trazos, (int(x), int(y)), 8, _bgra(col), -1, cv2.LINE_AA)
            elif tipo == "tp":
                a_, b_ = np.float32(P(*e["desde"])), np.float32(P(*e["a"]))
                c = np.linspace(a_, b_, 80)
                c[:, 1] -= np.sin(np.linspace(0, math.pi, 80)) * 120       # arco en el aire
                u_ = _eo(d / e.get("dur", 1.2))
                _trazo(trazos, _parcial(c, u_), col, 6, True, True)
                if u_ >= 1:                              # remolino de llegada
                    for k in range(3):
                        rad = 30 + 12 * k + 6 * math.sin(d * 8 + k)
                        cv2.ellipse(trazos, (int(b_[0]), int(b_[1])), (int(rad), int(rad * .45)), (d * 220 + k * 60) % 360, 0,
                                    250, _bgra(col, int(220 * clamp(2.2 - (d - e.get("dur", 1.2))))), 4, cv2.LINE_AA)
            elif tipo == "ward":
                x, y = P(e["u"], e["v"])
                sc = escala(e["u"], e["v"])
                rad = e.get("radio", .06) * 1000 * sc
                u_ = _eo(d / .5)
                rx, ry = int(rad * u_), int(rad * .62 * u_)
                if rx > 1:                             # círculo de visión en un parche local (no una capa de 1080p)
                    vc = np.zeros((2 * ry + 5, 2 * rx + 5, 4), np.uint8)
                    cv2.ellipse(vc, (rx + 2, ry + 2), (rx, ry), 0, 0, 360, _bgra(col), -1, cv2.LINE_AA)
                    _sobre(trazos, vc, int(x) - rx - 2, int(y) - ry - 2, .16 * v)
                cv2.ellipse(trazos, (int(x), int(y)), (int(rad * u_), int(rad * .62 * u_)), 0, 0, 360, _bgra(col, 200), 2,
                            cv2.LINE_AA)
                ojo = int(16 * _pop(d))
                if ojo > 1:
                    cv2.ellipse(fichas, (int(x), int(y) - 8), (ojo + 4, int(ojo * .7) + 4), 0, 0, 360, (0, 0, 0, 230), -1,
                                cv2.LINE_AA)
                    cv2.ellipse(fichas, (int(x), int(y) - 8), (ojo, int(ojo * .62)), 0, 0, 360, _bgra(col), -1, cv2.LINE_AA)
                    cv2.circle(fichas, (int(x), int(y) - 8), max(2, ojo // 3), (20, 10, 6, 255), -1, cv2.LINE_AA)
            elif tipo == "num":
                x, y = P(e["u"], e["v"])
                s = _pop(d)
                r = int(38 * s)
                if r > 2:
                    cv2.circle(fichas, (int(x), int(y) - 60), r + 5, (0, 0, 0, 230), -1, cv2.LINE_AA)
                    cv2.circle(fichas, (int(x), int(y) - 60), r, _bgra(col), -1, cv2.LINE_AA)
                    txt = pildora_num(str(e["n"]), int(48 * s))
                    _pegar_centro(fichas, txt, x, y - 60, 1, v)
                    cv2.line(fichas, (int(x), int(y) - 60 + r), (int(x), int(y)), (255, 255, 255, 220), 3, cv2.LINE_AA)
                if e.get("etiqueta") and d > .2:
                    _pegar_centro(etiq, pildora(e["etiqueta"], col, 30), x, y - 60 - 90, _pop(d - .2), v)
        # fichas: de atrás hacia delante (las de abajo tapan a las de arriba)
        vis = [e for e in els if e["tipo"] == "ficha" and _vida(e, t) > 0]
        vis.sort(key=lambda e: _interp(e["ruta"], t)[1])
        for e in vis:
            u, w = _interp(e["ruta"], t)
            x, y = P(u, w)
            sc = escala(u, w) * e.get("tam", 1.0)
            ico = _icono_ficha(os.path.join(iconos, e["campeon"] + ".png"), e["equipo"])
            s = _pop(t - e["en"]) * sc * .58
            cv2.ellipse(fichas, (int(x), int(y)), (int(30 * sc), int(11 * sc)), 0, 0, 360, (0, 0, 0, 150), -1, cv2.LINE_AA)
            _pegar_centro(fichas, ico, x, y - 34 * sc, s, _vida(e, t))
            if e.get("nombre") and s > .2:
                nm = pildora_nombre(e["nombre"], e["equipo"])
                _pegar_centro(etiq, nm, x, y - 34 * sc - ico.shape[0] * s / 2 - 16, 1, _vida(e, t))
        _sobre(out, _brillo(trazos, 7, .6), 0, 0)
        _sobre(out, fichas, 0, 0)
        _sobre(out, etiq, 0, 0)
        # HUD: título + reloj arriba a la izquierda, píldoras apiladas a la derecha
        cab = pildora(titulo, "amarillo", 34, None)
        _sobre(out, cab, 60, 46, clamp(dt / .3))
        if reloj:
            txt = [r_ for r_ in reloj if r_[0] <= t]
            if txt:
                r_ = pildora(txt[-1][1], "blanco", 30)
                _sobre(out, r_, 60 + cab.shape[1] + 10, 46 + (cab.shape[0] - r_.shape[0]) // 2, clamp(dt / .3))
        if hud:
            y = 46
            for h_ in hud:                             # (t, texto, color, sub[, fin])
                th, texto, col, sub = h_[:4]
                fin = h_[4] if len(h_) > 4 else None
                if t < th or (fin is not None and t >= fin + .3):
                    continue
                al = clamp(1 - (t - fin) / .3) if fin is not None and t >= fin else 1.0
                p = pildora(texto, col, 30, sub)
                _pegar_centro(out, p, W - 60 - p.shape[1] / 2, y + p.shape[0] / 2, _pop(t - th), al)
                y += p.shape[0] + 10
        return out

    return fn


def pildora_num(n, tam):
    k = ("n", n, tam)
    if k not in _cache:
        f = fuente("negra", max(tam, 8))
        bb = f.getbbox(n)
        im = Image.new("RGBA", (bb[2] + 8, bb[3] + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1] // 2 - 2), n, font=f, fill=(12, 14, 26, 255))
        _cache[k] = np.array(im)[..., [2, 1, 0, 3]].copy()
    return _cache[k]


def pildora_nombre(nombre, equipo):
    k = ("nm", nombre, equipo)
    if k not in _cache:
        f = fuente("xbold", 22)
        tw = f.getbbox(nombre)[2]
        im = Image.new("RGBA", (tw + 20, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, tw + 19, 31), radius=8, fill=(10, 14, 26, 225), outline=_rgb(equipo) + (255,), width=2)
        d.text((10, 2), nombre, font=f, fill=(255, 255, 255, 255))
        _cache[k] = np.array(im)[..., [2, 1, 0, 3]].copy()
    return _cache[k]


if __name__ == "__main__":                       # prueba: python nucleo/mg_tactica.py <mapa.png> <carpeta_iconos> salida.jpg
    import sys
    fn = tablero(0, sys.argv[1], [
        dict(tipo="ficha", campeon="Xayah", equipo="azul", ruta=[(0, .62, .64), (2, .5, .5)], en=0, nombre="Yeon"),
        dict(tipo="ficha", campeon="Jinx", equipo="rojo", ruta=[(0, .75, .62)], en=0, nombre="Hope"),
        dict(tipo="flecha", pts=[(.3, .1), (.5, .08), (.72, .1)], color="azul", en=0, etiqueta="OLEADA"),
        dict(tipo="anillo", u=.655, v=.69, color="amarillo", en=0, etiqueta="DRAGÓN 3"),
        dict(tipo="ward", u=.3, v=.25, color="azul", en=0),
        dict(tipo="num", u=.32, v=.3, n=3, color="amarillo", en=0, etiqueta="BARÓN"),
    ], camara=((0, .5, .5, 1.0),), reloj=[(0, "40:16")], hud=[(0, "11 - 17", "rojo", "ASESINATOS")], iconos=sys.argv[2])
    im = fn(2.5, 5, [])
    cv2.imwrite(sys.argv[3], im[..., :3])
