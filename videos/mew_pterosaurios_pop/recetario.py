# -*- coding: utf-8 -*-
"""RECETARIO adaptado (kit de hog_pruebas/recetario.py) para el reel de los pterosaurios de Martin Eastwood:
la explicación se cuenta en las páginas de un CUADERNO DE PALEONTOLOGÍA viejo. Grabados del siglo XIX reales
pegados con cinta, fotos de fósiles en sepia, diagramas a tinta que se dibujan solos, letra manuscrita,
sellos de goma rojos; él es un recorte de foto pegado sobre la página.
Todos los eventos van en TIEMPO DE LA FUENTE (ts); comun.fuente() traduce la salida (sin su intro de banda)."""
import functools, math, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
from comun import *

TINTA = np.array([0.17, 0.11, 0.08], np.float32)
ROJO = np.array([0.70, 0.11, 0.08], np.float32)
AZUL = np.array([0.16, 0.19, 0.30], np.float32)
VERDE = np.array([0.22, 0.30, 0.20], np.float32)
CREMA = np.array([0.965, 0.94, 0.87], np.float32)
F_GAB = FU + "Gabriola.ttf"
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
CAP = 985                                            # renglón de la letra manuscrita (justo encima de su cabeza)


def lum(rgb):
    return rgb[..., 0] * 0.3 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11


def sepia(rgb, mezcla=0.75, claro=1.0):
    g = np.clip(lum(rgb) * claro, 0, 1)[..., None]
    s = TINTA * 1.1 + g * (np.array([0.97, 0.91, 0.78], np.float32) - TINTA * 1.1)
    return (s * mezcla + rgb * (1 - mezcla)).astype(np.float32)


def grabado(rgb, alfa, periodo=7.0, ang=32):
    """Foto → grabado a buril: líneas de tinta cuyo grosor sigue el tono."""
    h, w = alfa.shape
    g = cv2.createCLAHE(2.5, (6, 6)).apply((np.clip(lum(rgb), 0, 1) * 255).astype(np.uint8)).astype(np.float32) / 255
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(ang)
    l1 = 0.5 + 0.5 * np.sin(2 * np.pi * (x * math.cos(a) + y * math.sin(a)) / periodo)
    l2 = 0.5 + 0.5 * np.sin(2 * np.pi * (-x * math.sin(a) + y * math.cos(a)) / periodo)
    t1 = np.clip((l1 * 0.8 + 0.1 - g) / 0.12 + 0.5, 0, 1)
    t2 = np.clip((l2 * 0.8 - 0.25 - g) / 0.12 + 0.5, 0, 1)
    tin = np.maximum(t1, t2)
    e = cv2.GaussianBlur(g, (0, 0), 1.0) - cv2.GaussianBlur(g, (0, 0), 3.0)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    borde = np.clip(alfa - cv2.erode(alfa, k), 0, 1)
    tin = np.clip(np.maximum(tin, np.clip(-e / 0.03, 0, 1)) * alfa + borde, 0, 1) * 0.93
    return np.dstack([TINTA * tin[..., None], tin]).astype(np.float32)


def carta(rgb, marco=16, cinta=True, color=CREMA):
    """Lámina o foto pegada: borde de papel y trocitos de cinta en dos esquinas."""
    h, w = rgb.shape[:2]
    sp = np.ones((h + 2 * marco, w + 2 * marco, 4), np.float32)
    sp[..., :3] = color * (0.96 + 0.04 * ruido(h + 2 * marco, w + 2 * marco, 80, 3)[..., None])
    sp[marco:-marco, marco:-marco, :3] = rgb
    if cinta:
        sp = np.pad(sp, ((26, 26), (26, 26), (0, 0)))
        H2, W2 = sp.shape[:2]
        for (cx, cy, ang) in ((70, 44, -38), (W2 - 70, 44, 38)):
            m = np.zeros((H2, W2), np.float32)
            box = cv2.boxPoints(((cx, cy), (150, 44), ang)).astype(np.int32)
            cv2.fillPoly(m, [box], 0.62, cv2.LINE_AA)
            sp[..., :3] = sp[..., :3] * (1 - m[..., None]) + np.array([0.86, 0.74, 0.50], np.float32) * m[..., None]
            sp[..., 3] = np.maximum(sp[..., 3], m)
    return sp


def foto(rgb, ancho, mezcla=0.55, claro=1.05, marco=14, cinta=True):
    """Foto a color → sepia del cuaderno, del ancho pedido, con marco y cinta."""
    r = cv2.resize(rgb, (ancho, int(rgb.shape[0] * ancho / rgb.shape[1])), interpolation=cv2.INTER_AREA)
    return carta(sepia(r, mezcla, claro), marco, cinta)


@functools.lru_cache(maxsize=32)
def estampa(txt, tam=64, color=tuple(ROJO), doble=True):
    """Sello de goma rectangular con doble filete y tinta desigual."""
    f = ImageFont.truetype(F_IMPACT, tam)
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + int(tam * 1.1), int(tam * 1.75)
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, w - 5, h - 5], outline=255, width=max(4, tam // 11))
    if doble:
        d.rectangle([4 + tam // 7, 4 + tam // 7, w - 5 - tam // 7, h - 5 - tam // 7], outline=255, width=max(2, tam // 26))
    d.text((w / 2 - (bb[2] + bb[0]) / 2, h / 2 - (bb[3] + bb[1]) / 2), txt, font=f, fill=255)
    a = np.asarray(im).astype(np.float32) / 255
    a *= np.clip((ruido(h, w, 12, len(txt) * 7 + tam) - 0.12) * 5, 0, 1) * 0.92
    return pre(np.broadcast_to(np.array(color, np.float32), a.shape + (3,)), a)


@functools.lru_cache(maxsize=4)
def redondo(l1, l2, l3, tam=420):
    """Sello redondo de museo (azul)."""
    def dib(d, T):
        c = T / 2
        for r, w in ((0.47, 0.016), (0.36, 0.008)):
            d.ellipse([c - T * r, c - T * r, c + T * r, c + T * r], outline=255, width=int(T * w))
        f1 = ImageFont.truetype(F_GEOB, int(T * 0.16)); f2 = ImageFont.truetype(F_GEOB, int(T * 0.062))
        for txt, f, y in ((l2, f1, 0.50), (l1, f2, 0.27), (l3, f2, 0.73)):
            bb = f.getbbox(txt)
            d.text((c - (bb[2] + bb[0]) / 2, T * y - (bb[3] + bb[1]) / 2), txt, font=f, fill=255)
    a = forma(tam, dib, ss=2) * np.clip((ruido(tam, tam, 12, 77) - 0.2) * 4, 0, 1) * 0.9
    return pre(np.broadcast_to(AZUL, a.shape + (3,)), a)


@functools.lru_cache(maxsize=96)
def _mano(txt, tam, fuente, color):
    sp = texto(txt, fuente, tam, color, esp=1)
    return sp, np.arange(sp.shape[1], dtype=np.float32)[None, :, None]


def mano(L, txt, tam, cx, cy, t, t0, t1=999, color=tuple(TINTA), fuente=F_SCRIPT, dur=None, raya=True, rot=-2.0):
    """Letra manuscrita que se escribe sola (izq → der) y luego se subraya."""
    if t < t0 or t > t1 + 0.3:
        return
    sp, xs = _mano(txt, tam, fuente, color)
    w = sp.shape[1]
    dur = dur or min(0.9, 0.05 * len(txt) + 0.2)
    p = rampa(t, t0, dur)
    op = 1 - rampa(t, t1, 0.3)
    q = sp * np.clip((p * (w + 50) - xs) / 40, 0, 1)
    if raya:
        u = sale(rampa(t, t0 + dur * 0.8, 0.25))
        if u > 0:
            y = sp.shape[0] - int(tam * 0.16)
            m = np.zeros(sp.shape[:2], np.float32)
            cv2.line(m, (10, y + 6), (int(10 + (w - 20) * u), y - 4), 0.9, max(4, tam // 14), cv2.LINE_AA)
            q = q * (1 - m[..., None]) + np.dstack([np.array(color, np.float32) * m[..., None], m])
    pegar(L, transf(q, 1.0, rot), cx, cy, op)


_SH = {}


def pega(L, sp, cx, cy, t, t0, t1=999, rot=0.0, esc=1.0, sal=(0, -1), clave=None):
    """Algo que se pega sobre la página: cae, proyecta sombra y al irse se desliza fuera."""
    if t < t0 or t > t1 + 0.3:
        return 0.0
    p = sale(rampa(t, t0, 0.22)); q = suave(rampa(t, t1, 0.3))
    k = esc * (1.22 - 0.22 * p)
    r = rot + 6 * (1 - p) + 0.35 * math.sin(int(t * 6) * 1.7 + cx)
    x, y = cx + sal[0] * 1300 * q * q, cy + sal[1] * 1300 * q * q
    s = transf(sp, k, r)
    key = clave or id(sp)
    if key not in _SH:
        _SH[key] = sombra(sp, 12, 0.6)
    al = 16 + 30 * (1 - p)
    pegar(L, transf(_SH[key], k, r), x + al * 0.7, y + al, 0.5 * p)
    pegar(L, s, x, y, min(1.0, p * 1.5))
    return golpe(t, t0 + 0.2, 0.2) * 0.5


def sello(L, sp, cx, cy, t, t0, t1=999, rot=-8.0):
    if t < t0 or t > t1 + 0.25:
        return 0.0
    p = rampa(t, t0, 0.1)
    pegar(L, transf(sp, 1.9 - 0.9 * sale(p), rot), cx, cy, p * (1 - rampa(t, t1, 0.25)))
    return golpe(t, t0 + 0.09, 0.25)


def trazo(L, pts, p, grosor=7, color=TINTA, op=0.9):
    """Línea de tinta que se va dibujando (p = 0..1)."""
    if p <= 0 or op <= 0:
        return
    pts = np.array(pts, np.float32)
    n = max(2, int(1 + (len(pts) - 1) * min(p, 1)))
    x0, y0 = int(pts[:, 0].min()) - 20, int(pts[:, 1].min()) - 20
    x1, y1 = int(pts[:, 0].max()) + 20, int(pts[:, 1].max()) + 20
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(L.shape[1], x1), min(L.shape[0], y1)
    if x1 <= x0 or y1 <= y0:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.float32)
    cv2.polylines(m, [(pts[:n] - (x0, y0)).astype(np.int32).reshape(-1, 1, 2)], False, op, grosor, cv2.LINE_AA)
    z = L[y0:y1, x0:x1]
    z[:] = z * (1 - m[..., None]) + np.array(color, np.float32) * m[..., None]


def linea(a, b, n=24, curva=0.0):
    """Puntos de a a b (con una leve curva de pluma)."""
    return [(a[0] + (b[0] - a[0]) * k / n - curva * (b[1] - a[1]) * math.sin(math.pi * k / n),
             a[1] + (b[1] - a[1]) * k / n + curva * (b[0] - a[0]) * math.sin(math.pi * k / n)) for k in range(n + 1)]


def circulo(cx, cy, rx, ry, n=60, vueltas=1.08, fase=-2.2):
    return [(cx + rx * (1 + 0.04 * math.sin(k * 0.5)) * math.cos(fase + 2 * math.pi * vueltas * k / n),
             cy + ry * (1 + 0.04 * math.cos(k * 0.4)) * math.sin(fase + 2 * math.pi * vueltas * k / n)) for k in range(n + 1)]


def flecha(L, a, b, p, grosor=8, color=ROJO, op=0.95):
    trazo(L, linea(a, b, 16), p, grosor, color, op)
    if p >= 0.98:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            trazo(L, [b, (b[0] - 34 * math.cos(ang + s * 0.45), b[1] - 34 * math.sin(ang + s * 0.45))], 1, grosor, color, op)


def huella(L, cx, cy, ang, esc=1.0, op=0.85, color=TINTA, dedos=3):
    """Huella de tres dedos (o de cinco, extendidos) a tinta."""
    c, s = math.cos(ang), math.sin(ang)
    def P(x, y):
        return (int(cx + esc * (x * c - y * s)), int(cy + esc * (x * s + y * c)))
    m = np.zeros(L.shape[:2], np.float32)
    cv2.ellipse(m, P(0, 0), (int(16 * esc), int(13 * esc)), math.degrees(ang), 0, 360, op, -1, cv2.LINE_AA)
    abre = (-0.55, 0, 0.55) if dedos == 3 else (-1.1, -0.55, 0, 0.55, 1.1)
    for a in abre:
        cv2.line(m, P(10 * math.sin(a), -8), P(34 * math.sin(a), -34 * math.cos(a) - 6), op, max(3, int(7 * esc)), cv2.LINE_AA)
    L[:] = L * (1 - m[..., None]) + np.array(color, np.float32) * m[..., None]


class Recetario:
    T_TURN = (CUT_A + 0.02, salida(33.30), salida(46.80), salida(54.70), salida(70.70))   # pases de hoja (salida)

    def __init__(s):
        man = ruido(H, W, 420, 1); gr = ruido(H, W, 7, 2, 2); fib = cv2.resize(ruido(H, W // 6, 3, 9, 1), (W, H))
        base = np.array([0.925, 0.885, 0.775], np.float32) * (0.90 + 0.14 * man[..., None]) * (0.965 + 0.07 * gr[..., None]) * (0.985 + 0.03 * fib[..., None])
        d = np.maximum(np.abs(xx - W / 2) / (W / 2), np.abs(yy - H / 2) / (H / 2))
        base *= (1 - 0.42 * np.clip(d - 0.80, 0, 1) / 0.2 * (0.6 + 0.8 * ruido(H, W, 120, 4)))[..., None]
        base *= (1 - 0.10 * np.exp(-(xx / 90.0)))[..., None]
        # cuadrícula tenue de cuaderno de campo
        for y in range(300, 1760, 48):
            cv2.line(base, (70, y), (W - 70, y), (0.80, 0.80, 0.74), 1, cv2.LINE_AA)
        s.papel = base.astype(np.float32)
        for a, g in ((46, 5), (62, 2)):
            cv2.rectangle(s.papel, (a, a), (W - a, H - a), tuple(float(x) * 2.2 for x in TINTA), g, cv2.LINE_AA)
        s.papel[80:280, 70:W - 70] = (s.papel[80:280, 70:W - 70] * 0 + np.array([0.925, 0.885, 0.775], np.float32) * (0.95 + 0.07 * man[80:280, 70:W - 70, None]))
        pegar(s.papel, texto("Cuaderno de Paleontología", F_GAB, 96, tuple(TINTA)), 540, 150)
        pegar(s.papel, texto("PTEROSAURIA  ·  CIENCIA SIN IGNORANCIA", F_GEO, 26, tuple(TINTA * 1.6), esp=6), 540, 232)
        cv2.line(s.papel, (200, 262), (880, 262), (0.36, 0.26, 0.2), 2, cv2.LINE_AA)
        s.papel2 = np.ascontiguousarray(s.papel[:, ::-1] * 0.985)
        s.papel2[80:280] = s.papel[80:280]
        # --- láminas y fotos (Commons, ver img/creditos.json) ---
        pr, pa = recorte("ptera", 760)
        s.ptera = grabado(pr, pa, periodo=6, ang=25)
        s.ptera_m = transf(s.ptera, 0.42)
        ri = cargar("riou", 900)
        s.riou = carta(sepia(ri, 0.6, 1.02), 14)
        rd = cargar("riou_dinos", 860)
        s.dinos = carta(sepia(rd[20:-20, 20:-20], 0.55, 1.05), 14)
        s.dinos_m = transf(carta(sepia(cv2.resize(rd, (420, int(rd.shape[0] * 420 / rd.shape[1])), interpolation=cv2.INTER_AREA), 0.55, 1.05), 8, False), 1.0)
        s.fosil = foto(cargar("ptero_fosil", 1000)[60:-60, 80:-80], 760, 0.5)
        s.crystal = foto(cargar("crystal"), 780, 0.55)
        s.sordes = foto(cargar("sordes"), 560, 0.35, 1.0)
        s.jeholo = foto(cargar("jeholo", 900)[120:900, 0:820], 430, 0.35, 1.0)
        s.megalo = carta(sepia(cargar("megalo", 760)[30:420], 0.7, 1.05), 12)
        # --- sus propias imágenes (del reel original, sin voltear) ---
        s.retro = foto(cuadro_fuente(29.5)[30:980, 44:756], 470, 0.25, 1.0)
        s.dino_pasto = foto(cuadro_fuente(61.6)[0:960, 0:630], 330, 0.35, 1.0)
        s.juguete = foto(cuadro_fuente(62.8)[0:940, 1216:1920], 360, 0.35, 1.0)
        s.komodo = foto(cuadro_fuente(66.5)[60:1080, 120:1800], 900, 0.4, 1.0)
        s.clado = foto(cuadro_fuente(49.0)[0:1080, 0:1920], 900, 0.3, 1.0)
        # --- recorte de periódico ---
        s.recorte = s._periodico()
        s.grano = [((ruido(H // 2, W // 2, 3, 30 + k, 1) - 0.5) * 0.05).repeat(2, 0).repeat(2, 1)[..., None] for k in range(3)]
        s.banda = np.array([0.20, 0.17, 0.13], np.float32) * (0.85 + 0.3 * ruido(150, W, 30, 40)[..., None])
        s.md = np.hypot(*(np.mgrid[-330:330, -330:330].astype(np.float32)))
        s.mn = ruido(660, 660, 70, 15)

    def _periodico(s):
        w, h = 760, 470
        r = np.broadcast_to(np.array([0.93, 0.91, 0.84], np.float32), (h, w, 3)).copy() * (0.95 + 0.07 * ruido(h, w, 40, 5)[..., None])
        pegar(r, texto("EL NOTICIERO", F_GEOB, 30, (0.2, 0.2, 0.2), esp=8), w / 2, 40)
        cv2.line(r, (30, 70), (w - 30, 70), (0.25, 0.25, 0.25), 2, cv2.LINE_AA)
        pegar(r, texto("¿UN «PTERODÁCTILO»", F_IMPACT, 62, (0.12, 0.12, 0.12)), w / 2, 118)
        pegar(r, texto("EN CIUDAD JUÁREZ?", F_IMPACT, 62, (0.12, 0.12, 0.12)), w / 2, 188)
        pegar(r, texto("También lo «vieron» en Monterrey y en Yucatán", F_GEOI, 26, (0.25, 0.25, 0.25)), w / 2, 248)
        rng = np.random.default_rng(3)
        for k in range(6):
            for col in range(2):
                x0 = 40 + col * (w // 2); x1 = x0 + w // 2 - 70 - int(rng.uniform(0, 90) * (k == 5))
                cv2.line(r, (x0, 300 + k * 28), (x1, 300 + k * 28), (0.55, 0.55, 0.52), 6, cv2.LINE_AA)
        sp = pre(r, np.ones((h, w), np.float32))
        # borde recortado con tijera (dientes)
        a = sp[..., 3]
        n = ruido(h, w, 6, 9, 1)
        a[:] = a * np.clip(np.minimum.reduce([xx[:h, :w] - 3 - 6 * n, (w - 4) - xx[:h, :w] - 6 * n, yy[:h, :w] - 3 - 6 * n, (h - 4) - yy[:h, :w] - 6 * n]) / 2, 0, 1)
        return np.dstack([sp[..., :3] * a[..., None] / np.maximum(sp[..., 3:], 1e-6) * 0 + r * a[..., None], a]).astype(np.float32)

    def hoja(s, g):
        return s.papel if g % 2 == 0 else s.papel2

    def mancha(s, L, cx, cy, R, color=TINTA):
        if R < 3:
            return
        r = int(min(325, R * 1.45))
        d = s.md[330 - r:330 + r, 330 - r:330 + r]; n = s.mn[330 - r:330 + r, 330 - r:330 + r]
        m = np.clip((R * (0.78 + 0.5 * n) - d) / 3.5, 0, 1) * 0.92
        pegar(L, pre(np.broadcast_to(color * (1.0 + 0.5 * n[..., None]), m.shape + (3,)), m), cx, cy)

    # ---------- piezas dibujadas ----------
    def tiempo_meso(s, L, t, t0, y=520, x0=150, x1=930, barras=(("pterosaurios", ROJO, 0.07, 1.0),)):
        """Regla del Mesozoico (Triásico · Jurásico · Cretácico) con barras de tinta que crecen."""
        p = sale(rampa(t, t0, 0.5))
        trazo(L, [(x0, y), (x1, y)], p, 6)
        cortes = (x0, x0 + (x1 - x0) * 0.274, x0 + (x1 - x0) * 0.575, x1)   # 252 · 201 · 145 · 66 millones de años
        for k, nm in enumerate(("Triásico", "Jurásico", "Cretácico")):
            e = rampa(t, t0 + 0.2 + 0.12 * k, 0.2)
            trazo(L, [(cortes[k], y - 22), (cortes[k], y + 22)], e, 5)
            if e > 0:
                pegar(L, texto(nm, F_GEOI, 34, tuple(TINTA)), (cortes[k] + cortes[k + 1]) / 2, y + 48, e)
        trazo(L, [(x1, y - 22), (x1, y + 22)], rampa(t, t0 + 0.55, 0.2), 5)
        for j, (nm, col, a, b) in enumerate(barras):
            tj = t0 + 0.7 + 0.5 * j
            u = sale(rampa(t, tj, 0.8))
            yb = y - 80 - 100 * j
            xa = x0 + (x1 - x0) * a
            xb = xa + (x0 + (x1 - x0) * b - xa) * u
            if u > 0:
                cv2.line(L, (int(xa), yb), (int(xb), yb), tuple(float(c) for c in col), 22, cv2.LINE_AA)
                sp = texto(nm, F_SCRIPT, 44, tuple(col))
                pegar(L, sp, xa + sp.shape[1] / 2, yb - 40, rampa(t, tj + 0.2, 0.3))

    def cadera(s, L, t, t0, cx, cy, tipo, op=1.0, e=0.78):
        """Vista de frente: cadera (óvalo) y patas. tipo 'bajo' = erguidas (dinosaurio), 'lados' = reptante (lagarto)."""
        def P(x, y):
            return (cx + e * x, cy + e * y)
        p = sale(rampa(t, t0, 0.5))
        trazo(L, circulo(cx, cy, 120 * e, 54 * e, 50, 1.03), p, 7, TINTA, 0.9 * op)
        for sgn in (-1, 1):
            q = sale(rampa(t, t0 + 0.35, 0.5))
            if tipo == "bajo":
                pts = [P(sgn * 70, 30), P(sgn * 78, 170), P(sgn * 72, 300)]
                pie = [P(sgn * 72, 300), P(sgn * 72 + 42, 306)]
            else:
                pts = [P(sgn * 100, 10), P(sgn * 230, 30), P(sgn * 260, 190)]
                pie = [P(sgn * 260, 190), P(sgn * 260 + 40 * sgn, 196)]
            trazo(L, pts, q, int(22 * e), TINTA, 0.9 * op)
            trazo(L, pie, rampa(t, t0 + 0.8, 0.2), int(14 * e), TINTA, 0.9 * op)
        ys = 316 if tipo == "bajo" else 206
        trazo(L, [P(-320, ys), P(320, ys)], rampa(t, t0 + 0.6, 0.4), 3, TINTA, 0.6 * op)

    def arbol(s, L, t, t0, op=1.0, y0=890, y1=330, cx=540, ancho=360, croc=True, marca=None):
        """Cladograma a tinta: Archosauria → (Pseudosuchia) | Avemetatarsalia → Pterosauria | Dinosauria."""
        nodo = (cx, y0 - 80)
        n2 = (cx + (70 if croc else 0), y0 - 270)
        hojas = {"Pterosauria": (cx - ancho + (90 if croc else 0), y1), "Dinosauria": (min(cx + ancho, 800), y1)}
        trazo(L, [(cx, y0), nodo], sale(rampa(t, t0, 0.3)), 9, TINTA, 0.9 * op)
        if croc:
            trazo(L, [nodo, (cx - ancho - 40, y0 - 300)], sale(rampa(t, t0 + 0.3, 0.4)), 8, TINTA, 0.55 * op)
            mano(L, "cocodrilos", 40, cx - ancho + 20, y0 - 350, t, t0 + 0.6, color=tuple(TINTA * 1.8), raya=False, rot=0)
        trazo(L, [nodo, n2], sale(rampa(t, t0 + 0.3, 0.35)), 9, TINTA, 0.9 * op)
        for k, (nm, (x, y)) in enumerate(hojas.items()):
            col = ROJO if nm == "Pterosauria" else TINTA
            trazo(L, [n2, (x, y + 60)], sale(rampa(t, t0 + 0.65 + 0.25 * k, 0.4)), 10, col, 0.92 * op)
            if t > t0 + 0.9 + 0.25 * k:
                pegar(L, texto(nm, F_GEOB, 46, tuple(col), esp=2), x, y + 22, rampa(t, t0 + 0.9 + 0.25 * k, 0.25) * op)
        if marca and t > marca:
            e = rebote(rampa(t, marca, 0.35), 1.4)
            trazo(L, circulo(n2[0], n2[1], 36 * e + 1, 36 * e + 1, 30, 1.05), 1, 6, ROJO, 0.95 * op)
        return nodo, n2

    def lupa(s, L, cx, cy, op=1.0):
        trazo(L, circulo(cx, cy, 110, 110, 50, 1.02, 0), 1, 12, TINTA, 0.92 * op)
        trazo(L, [(cx + 80, cy + 80), (cx + 210, cy + 210)], 1, 30, TINTA, 0.92 * op)
        m = np.clip((110 - np.hypot(xx - cx, yy - cy)) / 4, 0, 1)[..., None] * 0.12 * op
        L[:] = L * (1 - m) + np.array([1.0, 0.98, 0.9], np.float32) * m

    def venn(s, L, t, t0, op=1.0):
        for k, (cx, nm, col) in enumerate(((390, "Pterosauria", ROJO), (690, "Dinosauria", TINTA))):
            trazo(L, circulo(cx, 590, 250, 250, 70, 1.03, -2.2 + k), sale(rampa(t, t0 + 0.3 * k, 0.6)), 8, col, 0.9 * op)
            pegar(L, texto(nm, F_GEOB, 44, tuple(col), esp=2), cx + (-90 if k == 0 else 90), 300, rampa(t, t0 + 0.4 + 0.3 * k, 0.3) * op)
        if t > t0 + 0.9:                                                 # la intersección se rellena con rayado rojo
            e = rampa(t, t0 + 0.9, 0.6)
            d1 = np.hypot(xx - 390, yy - 590); d2 = np.hypot(xx - 690, yy - 590)
            m = ((d1 < 245) & (d2 < 245)).astype(np.float32) * (0.5 + 0.5 * np.sin((xx + yy) / 5.0) > 0.5) * 0.55 * e * op
            m *= (yy < 470 + 300 * e + 120)
            L[:] = L * (1 - m[..., None]) + ROJO * m[..., None]

    def zigzag(s, L, t, t0, y=900, op=1.0):
        """Rastro reptante: una S de tinta con huellas de cinco dedos a los lados."""
        pts = [(140 + k * 16, y + 60 * math.sin(k * 0.28)) for k in range(51)]
        u = rampa(t, t0, 1.6)
        trazo(L, pts, u, 5, TINTA, 0.55 * op)
        for k in range(0, 50, 5):
            if k / 50 < u:
                x, yv = pts[k]
                lado = 1 if (k // 5) % 2 else -1
                huella(L, x, yv + lado * 46, math.radians(90 + lado * 70) - math.pi / 2, 0.75, 0.8 * op, TINTA, 5)

    # ---------------- la página ----------------
    def pagina(s, ts, grupo):
        L = s.hoja(grupo).copy()
        sac = 0.0
        t = ts
        if grupo == 0:
            # 0-2,44 · los primeros vertebrados en dominar el vuelo
            if t < 2.6:
                u = sale(rampa(t, 0.0, 1.6))
                x, y = 1240 - 700 * u, 700 - 260 * u + 30 * math.sin(t * 3)
                ruta = [(1150 - 700 * k / 30, 780 - 300 * k / 30 + 40 * math.sin(k * 0.4)) for k in range(31)]
                for k in range(0, 30, 2):                               # estela punteada
                    if k / 30 < u * 0.95:
                        trazo(L, [ruta[k], ruta[k + 1]], 1, 4, TINTA, 0.45 * (1 - rampa(t, 2.3, 0.3)))
                pegar(L, transf(s.ptera, 0.95, -8 + 6 * math.sin(t * 2.2)), x, y, 1 - rampa(t, 2.35, 0.25))
                mano(L, "los primeros vertebrados", 66, 540, 820, t, 0.55, 2.4, dur=0.6, raya=False)
                mano(L, "en volar", 92, 540, 905, t, 1.55, 2.4, color=tuple(ROJO), dur=0.35)
            # 2,44-8,26 · en la era de los dinosaurios tuvieron casi tanto éxito
            if 2.4 < t < 8.4:
                op = 1 - rampa(t, 8.05, 0.25)
                sac += pega(L, s.dinos, 540, 560, t, 3.7, 8.1, rot=-2, esc=0.92, sal=(-1, 0))
                mano(L, "la era de los dinosaurios", 70, 540, CAP, t, 4.08, 5.8, dur=0.6)
                if t > 5.3:
                    sac += pega(L, transf(s.ptera, 0.55), 830, 380, t, 5.32, 8.1, rot=8, sal=(1, 0), clave="ptera55")
                if t > 6.1:
                    mano(L, "casi tanto éxito", 84, 540, CAP, t, 6.12, 8.05, color=tuple(ROJO), dur=0.45)
                    sac += sello(L, estampa("160 MILLONES DE AÑOS", 46), 330, 820, t, 6.9, 8.05, rot=-7)
            # 8,26-11,54 · quédense para saber de qué animales hablo
            if 8.2 < t < 12.4:
                op = 1 - rampa(t, 12.2, 0.2)
                s.mancha(L, 540, 560, 230 * sale(rampa(t, 8.3, 0.5)) * op)
                if t > 8.6:
                    pegar(L, transf(texto("?", F_GEOB, 300, (0.96, 0.92, 0.82)), 1 + 0.15 * golpe(t, 9.6, 0.4), 6), 540, 560, op * rampa(t, 8.7, 0.2))
                mano(L, "¿de qué animales hablo?", 76, 540, CAP, t, 9.36, 12.2, dur=0.7)
            # 12,48 · ¡Comenzamos!
            sac += sello(L, estampa("¡COMENZAMOS!", 92), 540, 600, t, 12.48, rot=-6)
        elif grupo == 1:
            # 22,76-28,04 · en las últimas semanas se ha hablado de pterodáctilos
            sac += pega(L, s.recorte, 500, 580, t, 23.5, 27.95, rot=-3, sal=(-1, 0))
            sac += sello(L, redondo("CAPÍTULO", "I", "PTEROSAURIA", 280), 880, 360, t, 22.75, 26.2, rot=-10)
            mano(L, "«pterodáctilos»", 92, 540, CAP, t, 26.9, 27.95, dur=0.5)
            # 28,04-33,42 · la gente los llama así · el término correcto: pterosaurios (su lámina Retro vs Modern)
            if t > 28.0:
                mano(L, "pterodáctilo", 96, 450, 470, t, 28.1, 33.3, dur=0.5, raya=False, rot=-3)
                if t > 29.6:
                    trazo(L, [(170, 492), (730, 450)], sale(rampa(t, 29.6, 0.2)), 12, ROJO)
                    sac += golpe(t, 29.6, 0.2)
                mano(L, "Pterodactylus = un solo género", 38, 450, 560, t, 30.0, 33.3, fuente=F_GEOI, raya=False, rot=-2)
                mano(L, "pterosaurio", 120, 520, 760, t, 32.3, 33.3, color=tuple(ROJO), dur=0.45, rot=-3)
                sac += sello(L, estampa("CORRECTO", 64, tuple(VERDE)), 850, 880, t, 32.9, rot=8)
        elif grupo == 2:
            # 33,42-37,32 · algunos han osado llamarlos dinosaurios
            sac += pega(L, s.crystal, 540, 560, t, 33.5, 39.2, rot=-2, sal=(-1, 0))
            mano(L, "Crystal Palace, Londres, 1854", 36, 540, 905, t, 34.0, 39.2, fuente=F_GEOI, raya=False, rot=-2)
            mano(L, "«dinosaurios»", 100, 540, CAP, t, 36.2, 39.2, dur=0.45)
            if t > 37.3:                                                # cosa que no son
                sac += sello(L, estampa("NO SON DINOSAURIOS", 78), 540, 560, t, 37.34, 39.2, rot=-9)
                trazo(L, [(250, CAP + 10), (840, CAP - 30)], sale(rampa(t, 38.2, 0.2)) * (t < 39.2), 12, ROJO)
            # 39,30-43,60 · vivieron en la misma época
            if 39.2 < t < 43.7:
                op = 1 - rampa(t, 43.45, 0.25)
                tmp = L.copy()
                s.tiempo_meso(tmp, t, 39.4, 640, barras=(("pterosaurios", ROJO, 0.13, 1.0), ("dinosaurios", TINTA, 0.10, 1.0)))
                pegar(tmp, transf(s.ptera_m, 1.0, -6), 300, 330, rampa(t, 40.0, 0.3))
                pegar(tmp, transf(s.dinos_m, 0.75, 3), 780, 350, rampa(t, 42.4, 0.3))
                mano(tmp, "la misma época", 92, 540, CAP, t, 41.8, 43.45, dur=0.5)
                L[:] = L * (1 - op) + tmp * op
            # 43,60-47,0 · no forman parte del orden dinosaurio
            if t > 43.5:
                p = sale(rampa(t, 43.6, 0.6))
                trazo(L, circulo(600, 580, 300, 250, 70, 1.04), p, 9, TINTA)
                pegar(L, texto("DINOSAURIA", F_GEOB, 50, tuple(TINTA), esp=4), 600, 300, rampa(t, 44.0, 0.3))
                pegar(L, transf(s.dinos_m, 0.85, 0), 600, 600, rampa(t, 44.2, 0.3))
                u = sale(rampa(t, 45.9, 0.4))
                pegar(L, transf(s.ptera_m, 0.85, -10), 200 - 40 * u, 760, rampa(t, 44.6, 0.3))
                if t > 45.9:
                    flecha(L, (250, 700), (420, 610), u)
                    sac += sello(L, estampa("FUERA", 58), 230, 590, t, 46.3, rot=-12)
                mano(L, "no forman parte", 84, 540, CAP, t, 44.68, 46.8, dur=0.55)
        elif grupo == 3:
            # 47,0-49,94 · (su cladograma abajo) tienen su propio orden: Pterosauria
            if t < 50.3:
                s.arbol(L, t, 47.1, marca=48.5)
                mano(L, "su propio orden", 86, 540, CAP, t, 48.4, 49.85, color=tuple(ROJO), dur=0.5)
            # 49,94-52,86 · características anatómicas que los diferencian
            if t > 49.9:
                tmp = s.hoja(3).copy()
                op = rampa(t, 49.9, 0.3)
                sac += pega(tmp, s.fosil, 540, 600, t, 49.95, 52.8, rot=-3, sal=(1, 0))
                if 50.6 < t < 52.9:
                    a = rampa(t, 50.6, 2.0)
                    s.lupa(tmp, 420 + 260 * math.sin(a * 2.6), 560 - 80 * math.cos(a * 2.2), sale(rampa(t, 50.6, 0.3)) * (1 - rampa(t, 52.6, 0.2)))
                mano(tmp, "anatomía", 104, 540, CAP, t, 50.7, 52.75, dur=0.4)
                # 52,86-54,82 · por ejemplo, la locomoción: huellas que cruzan la página
                for k in range(8):
                    tk = 53.0 + 0.17 * k
                    if t > tk:
                        huella(tmp, 170 + 105 * k, 820 - 60 * k + (45 if k % 2 else -45), math.radians(62), 2.0, 0.85 * sale(rampa(t, tk, 0.1)))
                        sac += 0.25 * golpe(t, tk, 0.1)
                mano(tmp, "locomoción", 112, 540, CAP, t, 54.0, dur=0.45)
                L[:] = L * (1 - op) + tmp * op
        elif grupo == 4:
            # 54,82-60,98 · los dinosaurios: patas debajo de la cadera
            pegar(L, texto("DINOSAURIO", F_GEOB, 44, tuple(TINTA), esp=3), 290, 330, rampa(t, 55.0, 0.3))
            s.cadera(L, t, 55.2, 290, 470, "bajo")
            if t > 58.5:
                flecha(L, (290, 500), (290, 690), sale(rampa(t, 58.5, 0.35)))
                sac += sello(L, estampa("BAJO LA CADERA", 34), 290, 860, t, 60.5, rot=-5)
            mano(L, "patas debajo de la cadera", 66, 540, CAP, t, 58.5, 60.95, dur=0.6)
            # 60,98-67,8 · los lagartos: patas a los lados
            pegar(L, texto("LAGARTO", F_GEOB, 44, tuple(TINTA), esp=3), 790, 330, rampa(t, 61.6, 0.3))
            if t > 61.7:
                s.cadera(L, t, 61.7, 790, 470, "lados")
            if t > 64.2:
                for sgn in (-1, 1):
                    flecha(L, (790 + sgn * 40, 600), (790 + sgn * 215, 600), sale(rampa(t, 64.3 + 0.15 * (sgn > 0), 0.35)))
                sac += sello(L, estampa("A LOS LADOS", 34), 790, 860, t, 65.4, rot=6)
            if t > 60.98:
                mano(L, "a los lados", 92, 540, CAP, t, 64.8, 67.7, color=tuple(ROJO), dur=0.45)
            # sus dos fotos (60,5-64,45) tapan sus pegatinas
            # 64,4-70,53 · su dragón de Komodo (inserto: él no está) · zigzaguean, reptan
            if t > 67.7:
                tmp = L.copy()
                tmp[290:1010, 80:W - 80] = s.hoja(4)[290:1010, 80:W - 80]
                op = rampa(t, 67.7, 0.25)
                s.zigzag(tmp, t, 67.8, 620)
                mano(tmp, "zigzaguean y reptan", 84, 540, CAP, t, 68.2, dur=0.6)
                L[:] = L * (1 - op) + tmp * op
        else:
            # 70,36-78,76 · características similares entre pterosaurios y dinosaurios
            if t < 79.0:
                op = 1 - rampa(t, 78.7, 0.25)
                tmp = L.copy()
                s.venn(tmp, t, 70.9)
                pegar(tmp, transf(s.ptera_m, 0.8, -8), 330, 600, rampa(t, 71.8, 0.3))
                pegar(tmp, transf(s.dinos_m, 0.6, 3), 760, 600, rampa(t, 72.2, 0.3))
                if t > 76.0:
                    pegar(tmp, transf(texto("=", F_GEOB, 150, tuple(ROJO)), 1 + 0.2 * golpe(t, 76.2, 0.3)), 540, 590, rampa(t, 76.1, 0.2))
                mano(tmp, "características", 80, 540, CAP, t, 74.06, 75.15, dur=0.5)
                mano(tmp, "sí son similares", 86, 540, CAP, t, 75.2, 78.6, dur=0.5)
                L[:] = L * (1 - op) + tmp * op
            # 78,76-82,10 · ambos tenían picnofibras
            if t > 78.7:
                sac += pega(L, s.sordes, 500, 560, t, 78.8, 84.6, rot=-3, sal=(-1, 0))
                mano(L, "Sordes pilosus · Jurásico", 34, 500, 820, t, 79.4, 84.6, fuente=F_GEOI, raya=False, rot=-3)
                mano(L, "picnofibras", 110, 540, CAP, t, 81.2, 84.6, color=tuple(ROJO), dur=0.45)
            # 82,10-84,72 · estructuras similares a plumas (tapa su pegatina de la derecha)
            # 84,72-90,40 · aparecieron en los ancestros de dinosaurios y pterosaurios
            if t > 84.6:
                tmp = s.hoja(5).copy()
                op = rampa(t, 84.6, 0.3)
                nodo, n2 = s.arbol(tmp, t, 84.8, croc=False, ancho=300, marca=87.5)
                if t > 87.6:                                             # pelusa en el ancestro común
                    for k in range(14):
                        a = 2 * math.pi * k / 14
                        e = sale(rampa(t, 87.6 + 0.03 * k, 0.2))
                        trazo(tmp, [(n2[0] + 40 * math.cos(a), n2[1] + 40 * math.sin(a)), (n2[0] + (40 + 34 * e) * math.cos(a + 0.3), n2[1] + (40 + 34 * e) * math.sin(a + 0.3))], 1, 4, ROJO, 0.9 * e)
                    mano(tmp, "ancestro común", 46, n2[0] - 220, n2[1] + 90, t, 87.94, color=tuple(ROJO), fuente=F_GEOI, raya=False, rot=0)
                mano(tmp, "en sus ancestros", 90, 540, CAP, t, 87.8, dur=0.5)
                L[:] = L * (1 - op) + tmp * op
            # cierre (después de 90,57: él ya no está)
            if t > 90.5:
                sac += sello(L, estampa("CONTINUARÁ…", 96), 540, 1330, t, 90.75, rot=-5)
                mano(L, "el video completo, en YouTube", 58, 540, 1530, t, 91.2, fuente=F_SCRIPT, raya=False, rot=-1, dur=0.6)
        return L, sac

    def cuadro(s, i):
        t = i / FPS
        ts = fuente(t)
        g = sum(t >= x for x in s.T_TURN)
        L, sac = s.pagina(ts, g)
        if g > 0:
            TF = s.T_TURN[g - 1]
            u = rampa(t, TF, 0.45)
            if u < 1:                                           # la hoja se pasa de derecha a izquierda
                L0, _ = s.pagina(fuente(TF - 0.01) if g > 1 else min(ts, CUT_A - 0.01), g - 1)
                xb = W * (1 - sale(u)) - 40
                m = np.clip((xx - xb) / 6, 0, 1)[..., None]
                som = 1 - 0.55 * np.exp(-np.clip(xb - xx, 0, None) / 70.0)[..., None] * (xx < xb)[..., None]
                luz = 1 - 0.25 * np.exp(-np.clip(xx - xb, 0, None) / 110.0)[..., None] * (1 - u)
                L = L0 * (1 - m) * som + L * m * luz
        # --- él: recorte de foto pegado sobre la página (debajo de lo que se pega encima) ---
        if ts < SRC_FIN:
            rgb, a = persona(ts, fondo=1830)
            if rgb is not None:
                fin = 1 - rampa(ts, SRC_FIN - 0.3, 0.3)
                k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))
                desv = np.clip((1800 - yy) / 40, 0, 1)
                an = cv2.GaussianBlur(cv2.dilate(a, k), (0, 0), 1.2) * desv * fin
                sh = cv2.resize(cv2.GaussianBlur(cv2.resize(an, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 5), (W, H))
                sh = np.roll(sh, (20, 14), (0, 1))[..., None]
                L *= 1 - 0.5 * sh
                rgb = np.clip((rgb - 0.015) * 1.5, 0, 1) ** 0.85
                rgb = sepia(rgb, 0.35, 1.05) * np.array([1.0, 0.98, 0.94], np.float32)
                L = L * (1 - an[..., None]) + CREMA * an[..., None]
                a3 = (a * desv * fin)[..., None]
                L = L * (1 - a3) + rgb * a3
        sac += s.encima(L, ts)
        # --- cinta de tela con el título ---
        z = L[1770:1920]
        z[:] = s.banda
        z[:6] *= 0.6
        L[1764:1770] *= 0.7
        pegar(L, texto("Pterosaurios", F_GAB, 88, (0.95, 0.88, 0.72)), 290, 1840)
        pegar(L, texto("en la cultura pop", F_GEOI, 34, (0.95, 0.88, 0.72)), 790, 1848)
        L += s.grano[int(t * 8) % 3]
        z = 1.025 + 0.02 * math.sin(t * 0.5) + 0.012 * min(sac, 1.5)
        M = np.array([[z, 0, (1 - z) * 540 + 10 * math.sin(t * 0.37) + (math.sin(t * 90) * 9 * min(sac, 1.3))],
                      [0, z, (1 - z) * 960 + 12 * math.cos(t * 0.29) + (math.cos(t * 70) * 7 * min(sac, 1.3))]], np.float32)
        return cv2.warpAffine(L, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    def encima(s, L, ts):
        """Fotos pegadas ENCIMA de su recorte: tapan sus pegatinas y sus insertos a pantalla completa."""
        sac = 0.0
        for sp, x, y, t0, t1, rot, sal in ((s.retro, 800, 1330, 27.45, 31.15, 3, (1, 0)),
                                           (s.clado, 540, 1380, 46.8, 51.25, 2, (0, 1)),
                                           (s.dino_pasto, 175, 1370, 60.55, 64.35, -4, (-1, 0)),
                                           (s.juguete, 905, 1370, 61.15, 64.35, 4, (1, 0)),
                                           (s.komodo, 540, 1330, 64.25, 70.3, -2, (0, 1)),
                                           (s.jeholo, 860, 1360, 81.95, 86.3, 5, (1, 0))):
            sac += pega(L, sp, x, y, ts, t0, t1, rot=rot, sal=sal)
        return sac

if __name__ == "__main__":
    principal(Recetario, "recetario", procesos=3)
