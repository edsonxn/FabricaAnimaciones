# -*- coding: utf-8 -*-
"""Kit ACUARELA PINTADA A MANO por código (4-nov-2026, nació en videos/ballena_estomago/).

Imita el corto de referencia (@mablesjoseph, X, 25-sep-2026): papel con grano, lavados de acuarela con moteado de pigmento y
BORDE HÚMEDO más oscuro, manchas de fondo que se desbordan, contorno de tinta a pincel con grosor variable y puntas afiladas
que HIERVE (se re-dibuja a 12 fps, en dos), personajes chibi, iconos de emoción y brillos cálidos.

Todo trabaja sobre `im` (float32 HxWx3, 0..1) en coordenadas de pantalla y solo dentro de la caja de cada forma (barato).
    forma(im, pts, col, t, seed)          relleno + contorno de tinta de un polígono cerrado (ambos hierven igual)
    lavado(im, pts, col, ...)              mancha de acuarela transparente (multiplica, como pigmento sobre papel)
    linea(im, pts, ancho, t, seed)         trazo de pincel abierto (puntas afiladas, presión variable)
    cinta(pts, w0, w1)                     contorno de un tubo (brazos, tentáculos, mangueras, algas) para forma()
    brillo(im, x, y, r, col, f)            luz aditiva suave · oscuridad(im, nivel, luces) para lugares sin luz
    rotulo(im, texto, x, y, px, col, t)    letras pintadas con contorno de tinta
    terminar(im, t)                        grano de papel, viñeta y tono cálido (al final de cada cuadro)
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    from motor import W, H
except Exception:                         # uso suelto (pruebas)
    W, H = 1080, 1920

TINTA = np.array([0.14, 0.11, 0.10], np.float32)
BOIL = 12                                 # re-dibujos de la tinta por segundo (en dos, a 24 fps)


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


# ------------------------------------------------------------ texturas fijas (iguales en todos los procesos)
def _ruido(escala, seed, w=W, h=H):
    r = np.random.default_rng(seed)
    a = r.random((max(2, int(h / escala) + 2), max(2, int(w / escala) + 2))).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)


def _norm(a):
    a = a - a.mean()
    return a / (a.std() + 1e-6)


PAPEL = _norm(0.25 * _ruido(1.6, 11) + 0.45 * _ruido(5, 12) + 0.45 * _ruido(26, 13))
_fib = cv2.GaussianBlur(np.random.default_rng(14).random((H, W)).astype(np.float32), (0, 0), sigmaX=9, sigmaY=0.8)
PAPEL = _norm(PAPEL + 0.3 * _norm(_fib)).astype(np.float32)
GRAN = np.clip(_norm(_ruido(2.2, 21)) * 0.5 + 0.5, 0, 1).astype(np.float32)          # granulación del pigmento
PIG = [np.clip(_norm(0.6 * _ruido(70, 31 + k) + 0.4 * _ruido(190, 41 + k) + 0.15 * _ruido(14, 51 + k)) * 0.22 + 0.5, 0, 1)
       .astype(np.float32) for k in range(4)]                                          # moteado de los lavados
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.30 * (((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H / 2) / (H * 0.6)) ** 2) ** 1.4).clip(0.55, 1)[..., None]
GRANOS = [np.random.default_rng(60 + k).normal(0, 1, (H // 2, W // 2)).astype(np.float32) for k in range(3)]


# ------------------------------------------------------------ utilidades
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def pr(t, a, b):
    return clamp((t - a) / (b - a)) if b != a else float(t >= a)


def suave(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def e_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def e_in(x):
    return clamp(x) ** 3


def e_back(x, c=1.7):
    x = clamp(x) - 1
    return 1 + (c + 1) * x ** 3 + c * x ** 2


def lerp(a, b, u):
    return a + (b - a) * u


def boil(t):
    return int(t * BOIL)


# ------------------------------------------------------------ geometría
def curva(ctrl, n=10, cerrado=False):
    """Catmull-Rom por los puntos de control."""
    P = np.asarray(ctrl, np.float32)
    P = np.vstack([P[-1:], P, P[:2]]) if cerrado else np.vstack([P[:1], P, P[-1:]])
    u = np.linspace(0, 1, n, endpoint=False, dtype=np.float32)[:, None]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        out.append(0.5 * (2 * p1 + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
    if not cerrado:
        out.append(P[-2:-1])
    return np.vstack(out)


def elipse(cx, cy, rx, ry, rot=0.0, n=56):
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    x, y = rx * np.cos(a), ry * np.sin(a)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1).astype(np.float32)


def rrect(cx, cy, w, h, r, rot=0.0, n=6):
    r = min(r, w / 2, h / 2)
    pts = []
    for (ox, oy, a0) in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for a in np.linspace(a0, a0 + 90, n):
            pts.append((ox + r * math.cos(math.radians(a)), oy + r * math.sin(math.radians(a))))
    return tr(np.array(pts, np.float32), cx, cy, 1, rot)


def mancha_pts(cx, cy, r, seed, irreg=0.18, n=60, ry=None):
    """Contorno de mancha irregular (nubes, charcos, manchas de fondo)."""
    rg = np.random.default_rng(seed)
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rr = np.ones(n)
    for k in range(2, 7):
        rr += irreg / k ** 0.7 * np.sin(k * a + rg.random() * 6.283)
    ry = r if ry is None else ry
    return np.stack([cx + r * rr * np.cos(a), cy + ry * rr * np.sin(a)], 1).astype(np.float32)


def tr(pts, x, y, s=1.0, rot=0.0, sx=1.0):
    """Local → pantalla: espejo (sx), giro, escala y traslado."""
    p = np.asarray(pts, np.float32).copy()
    p[:, 0] *= sx
    if rot:
        c, si = math.cos(rot), math.sin(rot)
        p = np.stack([p[:, 0] * c - p[:, 1] * si, p[:, 0] * si + p[:, 1] * c], 1)
    return (p * s + np.array([x, y], np.float32)).astype(np.float32)


def remuestrear(pts, paso=3.0, cerrado=False):
    p = np.asarray(pts, np.float32)
    if cerrado:
        p = np.vstack([p, p[:1]])
    d = np.sqrt(((p[1:] - p[:-1]) ** 2).sum(1))
    s = np.concatenate([[0], np.cumsum(d)])
    L = float(s[-1])
    n = max(4, int(L / paso))
    u = np.linspace(0, L, n, endpoint=not cerrado)
    return np.stack([np.interp(u, s, p[:, 0]), np.interp(u, s, p[:, 1])], 1).astype(np.float32), L


def hervir(pts, seed, t, amp=1.4, cerrado=True):
    """Temblor de línea dibujada a mano: ondas suaves a lo largo del trazo que cambian 12 veces por segundo."""
    p = np.asarray(pts, np.float32)
    if amp <= 0 or len(p) < 3:
        return p
    b = boil(t)
    r = np.random.default_rng((seed * 1009 + b * 7919 + 17) & 0x7FFFFFFF)
    s = np.linspace(0, 1, len(p), endpoint=not cerrado, dtype=np.float32)
    ph = r.random(4) * 6.283
    k = r.integers(1, 4, 2)
    dx = np.sin(6.283 * k[0] * s + ph[0]) * 0.7 + np.sin(6.283 * (k[1] + 3) * s + ph[1]) * 0.3
    dy = np.sin(6.283 * k[1] * s + ph[2]) * 0.7 + np.sin(6.283 * (k[0] + 3) * s + ph[3]) * 0.3
    return p + amp * np.stack([dx, dy], 1).astype(np.float32)


def cinta(pts, w0, w1=None, cap=7):
    """Contorno cerrado de un tubo de grosor w0 → w1 a lo largo de `pts` (puntas redondas)."""
    P, _ = remuestrear(pts, 4.0)
    w1 = w0 if w1 is None else w1
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-6
    N = np.stack([-T[:, 1], T[:, 0]], 1)
    w = np.linspace(w0, w1, len(P), dtype=np.float32)[:, None] / 2
    L, R = P + N * w, P - N * w
    th = np.linspace(0, math.pi, cap)[1:-1, None].astype(np.float32)
    fin = P[-1] + w[-1] * (N[-1] * np.cos(th) + T[-1] * np.sin(th))
    ini = P[0] + w[0] * (-N[0] * np.cos(th) - T[0] * np.sin(th))
    return np.vstack([L, fin, R[::-1], ini]).astype(np.float32)


# ------------------------------------------------------------ rasterizado en caja
def _caja(pts, pad):
    x0 = int(max(0, math.floor(float(pts[:, 0].min()) - pad)))
    y0 = int(max(0, math.floor(float(pts[:, 1].min()) - pad)))
    x1 = int(min(W, math.ceil(float(pts[:, 0].max()) + pad)))
    y1 = int(min(H, math.ceil(float(pts[:, 1].max()) + pad)))
    return x0, y0, x1, y1


def _mascara(polis, caja):
    x0, y0, x1, y1 = caja
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    for p in polis:
        q = np.round((np.asarray(p, np.float32) - (x0, y0)) * 16).astype(np.int32)
        cv2.fillPoly(m, [q], 255, cv2.LINE_AA, shift=4)
    return m.astype(np.float32) * (1 / 255)


def _blur(m, s):
    return cv2.GaussianBlur(m, (0, 0), s) if s > 0.3 else m


# ------------------------------------------------------------ pintura
def relleno(im, pts, col, alfa=1.0, modo="opaco", borde=0.55, mota=0.5, seed=0, humedo=5.0, recorte=None, gran=0.25):
    """Rellena el polígono. modo 'opaco' = gouache (tapa); 'lavado' = acuarela transparente (multiplica).
    borde = oscurecimiento del borde húmedo; mota = moteado del pigmento; recorte = máscara extra (función caja → máscara)."""
    pts = np.asarray(pts, np.float32)
    caja = _caja(pts, humedo * 2 + 3)
    x0, y0, x1, y1 = caja
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    M = _mascara([pts], caja)
    if recorte is not None:
        M *= recorte(caja)
    R = im[y0:y1, x0:x1]
    pig = PIG[seed % 4][y0:y1, x0:x1] - 0.5
    edge = np.clip(M - _blur(M, humedo), 0, 1)
    col = np.asarray(col, np.float32)
    if modo == "lavado":
        d = M * alfa * (1 + mota * 2.2 * pig) * (1 + borde * 3.0 * edge) * (1 + gran * (GRAN[y0:y1, x0:x1] - 0.5))
        R *= 1 - np.clip(d, 0, 1.3)[..., None] * (1 - col)
    else:
        c = col * (1 + mota * 0.55 * pig[..., None]) * (1 - borde * 1.1 * edge[..., None])
        a = (M * alfa)[..., None]
        R *= 1 - a
        R += c * a
    np.clip(R, 0, 1.5, out=R)


def sombreado(im, pts, col, dx, dy, alfa=0.55, seed=0, suav=6.0):
    """Media luna de sombra (o luz, con modo lavado claro) dentro de la forma: forma menos la forma corrida (dx, dy)."""
    pts = np.asarray(pts, np.float32)
    caja = _caja(pts, abs(dx) + abs(dy) + suav * 2 + 2)
    x0, y0, x1, y1 = caja
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    M = _mascara([pts], caja)
    S = _mascara([pts + (dx, dy)], caja)
    m = np.clip(M - _blur(S, suav), 0, 1) * M
    pig = PIG[(seed + 1) % 4][y0:y1, x0:x1] - 0.5
    d = m * alfa * (1 + 1.6 * pig)
    R = im[y0:y1, x0:x1]
    R *= 1 - np.clip(d, 0, 1)[..., None] * (1 - np.asarray(col, np.float32))


def luz_interior(im, pts, col, dx, dy, alfa=0.5, suav=8.0):
    """Reflejo de luz suave dentro de la forma (aditivo, recortado a la forma)."""
    pts = np.asarray(pts, np.float32)
    caja = _caja(pts, suav * 2 + 2)
    x0, y0, x1, y1 = caja
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    M = _mascara([pts], caja)
    S = _blur(_mascara([pts + (dx, dy)], caja), suav)
    m = np.clip(M - S, 0, 1) * M
    R = im[y0:y1, x0:x1]
    R += (m * alfa)[..., None] * np.asarray(col, np.float32)


def linea(im, pts, ancho=5.0, col=TINTA, seed=0, t=0.0, amp=1.3, cerrado=False, punta=True, alfa=0.95, seco=0.18, hierve=True):
    """Trazo de pincel: grosor que cambia con la «presión», puntas afiladas y pincel seco en la textura del papel."""
    p = np.asarray(pts, np.float32)
    if len(p) < 2 or ancho <= 0.2:
        return
    if hierve:
        p = hervir(p, seed, t, amp, cerrado)
    P, L = remuestrear(p, 2.5, cerrado)
    if L < 2:
        return
    if cerrado:
        P = np.vstack([P, P[:3]])
    n = len(P)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-6
    N = np.stack([-T[:, 1], T[:, 0]], 1)
    s = np.linspace(0, 1, n, dtype=np.float32)
    rg = np.random.default_rng(seed * 31 + 7)
    f1, f2 = rg.random(2) * 6.283
    k = 2 + int(L / 300)
    w = ancho * (1 + 0.32 * np.sin(6.283 * k * s + f1) + 0.14 * np.sin(6.283 * (2.7 * k) * s + f2 + boil(t) * 0.7 * hierve))
    if punta and not cerrado:
        w *= np.clip(np.minimum(s, 1 - s) * (L / max(ancho * 5, 1)), 0.12, 1) ** 0.55
    w = np.clip(w, 0.4, None)[:, None] / 2
    Lp, Rp = P + N * w, P - N * w
    caja = _caja(P, ancho * 2 + 3)
    x0, y0, x1, y1 = caja
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    paso = 40
    for i in range(0, n - 1, paso):
        j = min(n, i + paso + 2)
        poly = np.vstack([Lp[i:j], Rp[i:j][::-1]])
        q = np.round((poly - (x0, y0)) * 16).astype(np.int32)
        cv2.fillPoly(m, [q], 255, cv2.LINE_AA, shift=4)
    a = m.astype(np.float32) * (alfa / 255)
    if seco > 0:
        a *= 1 - seco * np.clip(GRAN[y0:y1, x0:x1] - 0.35, 0, 1)
    R = im[y0:y1, x0:x1]
    R *= 1 - a[..., None]
    R += a[..., None] * np.asarray(col, np.float32)


def forma(im, pts, col, t, seed, tinta=5.0, modo="opaco", alfa=1.0, borde=0.55, mota=0.5, amp=1.3, humedo=5.0,
          sombra=None, luz=None, tinta_col=TINTA, contorno=True):
    """Polígono cerrado relleno + contorno de tinta; el relleno y la línea hierven juntos.
    sombra = (col, dx, dy[, alfa]) media luna de sombra; luz = (col, dx, dy[, alfa]) reflejo."""
    p = hervir(pts, seed, t, amp, True)
    relleno(im, p, col, alfa, modo, borde, mota, seed, humedo)
    if sombra is not None:
        sombreado(im, p, sombra[0], sombra[1], sombra[2], sombra[3] if len(sombra) > 3 else 0.55, seed)
    if luz is not None:
        luz_interior(im, p, luz[0], luz[1], luz[2], luz[3] if len(luz) > 3 else 0.45)
    if contorno and tinta > 0:
        linea(im, p, tinta, tinta_col, seed, t, cerrado=True, hierve=False, alfa=0.93 * min(1.0, alfa * 1.4))


def lavado(im, pts, col, alfa=0.8, seed=0, humedo=9.0, borde=0.7, mota=0.6, t=None, amp=0.0):
    """Mancha de acuarela transparente con borde húmedo (fondos, sombras, charcos). Sin contorno."""
    p = hervir(pts, seed, t, amp, True) if (t is not None and amp > 0) else pts
    relleno(im, p, col, alfa, "lavado", borde, mota, seed, humedo)


def degradado(im, arriba, abajo, y0=0, y1=None, curva_=1.0):
    y1 = H if y1 is None else y1
    u = np.clip((np.arange(H, dtype=np.float32) - y0) / max(1, y1 - y0), 0, 1) ** curva_
    im[:] = (np.asarray(arriba, np.float32) * (1 - u[:, None, None]) + np.asarray(abajo, np.float32) * u[:, None, None])


def brillo(im, x, y, r, col, f=1.0):
    """Luz aditiva redonda y suave."""
    caja = _caja(np.array([[x - 2.2 * r, y - 2.2 * r], [x + 2.2 * r, y + 2.2 * r]], np.float32), 0)
    x0, y0, x1, y1 = caja
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    g = np.exp(-(((xx - x) ** 2 + (yy - y) ** 2) / (r * r))) * f
    im[y0:y1, x0:x1] += g[..., None] * np.asarray(col, np.float32)


def brillo_forma(im, pts, col, sigma=18.0, f=0.8):
    pts = np.asarray(pts, np.float32)
    caja = _caja(pts, sigma * 3)
    x0, y0, x1, y1 = caja
    if x1 - x0 < 4 or y1 - y0 < 4:
        return
    M = _mascara([pts], caja)
    h, w = M.shape
    sm = cv2.resize(M, (max(2, w // 4), max(2, h // 4)), interpolation=cv2.INTER_AREA)
    sm = cv2.resize(cv2.GaussianBlur(sm, (0, 0), sigma / 4), (w, h), interpolation=cv2.INTER_LINEAR)
    im[y0:y1, x0:x1] += (sm * f)[..., None] * np.asarray(col, np.float32)


def oscuridad(im, nivel, luces=(), conos=()):
    """Oscurece el cuadro (nivel 0..1) salvo cerca de las luces (x, y, radio, fuerza) y dentro de los conos
    (x, y, ángulo, apertura, largo, fuerza). Calculado a 1/4 y suavizado: barato."""
    if nivel <= 0:
        return
    w4, h4 = W // 4, H // 4
    yy, xx = np.mgrid[0:h4, 0:w4].astype(np.float32) * 4
    L = np.zeros((h4, w4), np.float32)
    for (x, y, r, f) in luces:
        L += f * np.exp(-(((xx - x) ** 2 + (yy - y) ** 2) / (r * r)))
    for (x, y, ang, ap, largo, f) in conos:
        dx, dy = xx - x, yy - y
        d = np.sqrt(dx * dx + dy * dy) + 1e-3
        cosd = (dx * math.cos(ang) + dy * math.sin(ang)) / d
        dentro = np.clip((cosd - math.cos(ap)) / (1 - math.cos(ap) + 1e-3), 0, 1) ** 0.8
        L += f * dentro * np.exp(-(d / largo) ** 2)
    L = cv2.resize(cv2.GaussianBlur(L, (0, 0), 3), (W, H), interpolation=cv2.INTER_LINEAR)
    k = 1 - nivel * (1 - np.clip(L, 0, 1.3))
    im *= np.clip(k, 0, 1.3)[..., None]


def rayos(im, x, y, angs, largo, ancho, col, f=0.25):
    """Rayos de sol bajo el agua (aditivos y difusos)."""
    for i, a in enumerate(angs):
        d = np.array([math.cos(a), math.sin(a)], np.float32)
        n = np.array([-d[1], d[0]], np.float32)
        p0 = np.array([x, y], np.float32)
        poly = np.array([p0 + n * ancho * 0.15, p0 - n * ancho * 0.15, p0 + d * largo - n * ancho, p0 + d * largo + n * ancho])
        brillo_forma(im, poly, col, sigma=26, f=f * (0.7 + 0.3 * math.sin(i * 2.1)))


# ------------------------------------------------------------ letras
_FUENTES = {}
_DIRF = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]


def _fuente(nombre, px):
    k = (nombre, px)
    if k not in _FUENTES:
        for d in _DIRF:
            f = os.path.join(d, nombre)
            if os.path.exists(f):
                _FUENTES[k] = ImageFont.truetype(f, px)
                break
        else:
            _FUENTES[k] = ImageFont.load_default()
    return _FUENTES[k]


_TXT = {}


def _txt_mask(texto, px, fuente):
    k = (texto, px, fuente)
    if k not in _TXT:
        f = _fuente(fuente, px)
        x0, y0, x1, y1 = f.getbbox(texto)
        pad = px // 4 + 8
        img = Image.new("L", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
        ImageDraw.Draw(img).text((pad - x0, pad - y0), texto, font=f, fill=255)
        m = np.asarray(img, np.float32) / 255
        borde = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (px // 7 * 2 + 1, px // 7 * 2 + 1)))
        _TXT[k] = (m, borde)
    return _TXT[k]


def rotulo(im, texto, x, y, px, col, t, seed=0, rot=0.0, esc=1.0, fuente="LuckiestGuy-Regular.ttf", alfa=1.0, tinta=True):
    """Texto pintado (relleno moteado + contorno de tinta) centrado en (x, y); tiembla con el hervido."""
    if esc <= 0.02 or alfa <= 0.01:
        return
    m, b = _txt_mask(texto, px, fuente)
    rg = np.random.default_rng(seed * 13 + boil(t))
    ang = math.degrees(rot) + rg.normal(0, 0.5)
    h, w = m.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -ang, esc)
    M[0, 2] += x - w / 2 + rg.normal(0, 0.8)
    M[1, 2] += y - h / 2 + rg.normal(0, 0.8)
    mm = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR)
    bb = cv2.warpAffine(b, M, (W, H), flags=cv2.INTER_LINEAR) if tinta else None
    ys, xs = np.nonzero((bb if bb is not None else mm) > 0.01)
    if len(xs) == 0:
        return
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    R = im[y0:y1, x0:x1]
    if bb is not None:
        a = bb[y0:y1, x0:x1, None] * alfa * 0.95
        R *= 1 - a
        R += a * TINTA
    pig = PIG[seed % 4][y0:y1, x0:x1, None] - 0.5
    c = np.asarray(col, np.float32) * (1 + 0.5 * pig)
    a = mm[y0:y1, x0:x1, None] * alfa
    R *= 1 - a
    R += a * c


# ------------------------------------------------------------ acabado del cuadro
def terminar(im, t, papel=0.05, vineta=True, calido=True):
    b = boil(t)
    im *= 1 + PAPEL[..., None] * papel
    g = cv2.resize(GRANOS[b % 3], (W, H), interpolation=cv2.INTER_LINEAR)
    im += g[..., None] * 0.008
    if vineta:
        im *= VIG
    if calido:
        im *= np.array([1.02, 1.0, 0.965], np.float32)
        im += np.array([0.012, 0.006, 0.0], np.float32)
    np.clip(im, 0, 1, out=im)
    return im
