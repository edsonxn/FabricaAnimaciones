# -*- coding: utf-8 -*-
"""«El asteroide que NO vimos venir» — FUSIÓN Kuriox (motion graphics espaciales por código, tipo Kurzgesagt) + pegatina Flow
(escenarios y piezas de Flow con cámara, parallax y pegatinas; kit `nucleo/pegaflow.py`, ejemplo `videos/jalpa/`).
Tramo 2 (20-oct-2026): gancho + ciegos = primer minuto. Cada toma = un escenario de Flow + MG propios (órbitas, enjambres, conos,
contadores, trayectorias punteadas) + ambiente continuo (estrellas que titilan, polvo, rocas que giran): nada quieto > 2 s."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, e_inout, e_back, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


G, C = "gancho", "ciegos"
t_tod = T(G, "todavía", 0)
t_ahora, t_miles, t_ciudad, t_tierra = T(G, "ahora", 1), T(G, "miles", 1), T(G, "ciudad", 1), T(G, "tierra", 1)
t_peor, t_no, t_donde = T(G, "peor", 2), T(G, "no", 2), T(G, "dónde", 2)
t_hoy, t_una, t_viniera, t_y3, t_demas, t_tarde = (T(G, "hoy", 3), T(G, "una", 3), T(G, "viniera", 3), T(G, "y", 3),
                                                   T(G, "demasiado", 3), T(G, "tarde", 3))
t0C = _ESC[C]["t0"]
t_calc, t_25, t_aster, t_140, t_destruir = T(C, "calcula", 0), T(C, "25", 0), T(C, "asteroides", 0), T(C, "140", 0), T(C, "destruir", 0)
t_hemos, t_menos, t_mitad = T(C, "hemos", 1), T(C, "menos", 1), T(C, "mitad", 1)
t_2019, t_100, t_paso, t_quinta, t_dist, t_luna, t_desc, t_dia = (T(C, "2019", 2), T(C, "100", 2), T(C, "pasó", 2), T(C, "quinta", 2),
                                                                  T(C, "distancia", 2), T(C, "luna", 2), T(C, "descubrieron", 2),
                                                                  T(C, "día", 2))
t_yhay, t_cielo, t_nunca, t_vigilar, t_junto, t_sol = (T(C, "y", 3), T(C, "cielo", 3), T(C, "nunca", 3), T(C, "vigilar", 3),
                                                       T(C, "junto", 3), T(C, "sol", 3))
t_nuestros, t_telesc, t_noche, t_todo, t_lado, t_ciegas = (T(C, "nuestros", 4), T(C, "telescopios", 4), T(C, "noche", 4), T(C, "todo", 4),
                                                           T(C, "lado", 4), T(C, "ciegas", 4))
t0X = _ESC["cheliabinsk"]["t0"]

# paleta Kuriox-terror: navy/índigo/teal + UN acento rojo-naranja
TEAL = (0.36, 0.92, 0.88)
BLANCO = (0.94, 0.96, 1.0)
ROJO = (1.0, 0.24, 0.12)
NARANJA = (1.0, 0.55, 0.20)
FRIO = (0.80, 0.86, 1.02)          # luz fría del espacio sobre las pegatinas

SFX = []


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


# ------------------------------------------------------------------ motion graphics (capa de trazos con brillo)
def _mezcla(lz, a, color, op=1.0, glow=0.0, aditivo=False):
    """Pinta la máscara `a` (H×W 0..1) de `color`; `glow` añade un halo difuso aditivo (luz de pantalla de Kurzgesagt)."""
    if op <= 0.003:
        return
    c = np.float32(color)
    if glow > 0:
        g = cv2.GaussianBlur(a, (0, 0), 9)
        lz += (g * (glow * op))[..., None] * c
    if aditivo:
        lz += (a * op)[..., None] * c
    else:
        k = (a * op)[..., None]
        lz[:] = lz * (1 - k) + c * k


def trazo(lz, fn, color, op=1.0, glow=0.5, aditivo=False):
    """`fn(m)` dibuja con cv2 sobre una máscara uint8 (coordenadas ×16, usar `shift=4` y LINE_AA)."""
    if op <= 0.003:
        return
    m = np.zeros((H, W), np.uint8)
    fn(m)
    _mezcla(lz, m.astype(np.float32) / 255.0, color, op, glow, aditivo)


def _p(x, y):
    return int(round(x * 16)), int(round(y * 16))


def elipse(m, cx, cy, rx, ry, ang=0.0, a0=0, a1=360, g=2, rel=False):
    if rel:
        cv2.ellipse(m, _p(cx, cy), _p(rx, ry), ang, a0, a1, 255, -1, cv2.LINE_AA, 4)
    else:
        cv2.ellipse(m, _p(cx, cy), _p(rx, ry), ang, a0, a1, 255, g, cv2.LINE_AA, 4)


def elipse_punteada(m, cx, cy, rx, ry, u=1.0, a0=0.0, paso=6, g=2):
    """Órbita punteada que se va dibujando (u 0..1)."""
    for k in range(int(360 / paso * clamp01(u))):
        a = a0 + k * paso
        cv2.ellipse(m, _p(cx, cy), _p(rx, ry), 0, a, a + paso * 0.55, 255, g, cv2.LINE_AA, 4)


def poligono(m, pts):
    cv2.fillPoly(m, [np.array([_p(x, y) for x, y in pts], np.int32)], 255, cv2.LINE_AA, 4)


@functools.lru_cache(maxsize=256)
def _texto_spr(txt, px, color, fnt, glow):
    f = D.fuente(fnt, px)
    x0, y0, x1, y1 = f.getbbox(txt)
    pad = int(px * 0.6)
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((pad - x0, pad - y0), txt, font=f, fill=255)
    a = np.asarray(im, np.float32) / 255.0
    if glow:
        a = np.maximum(a, cv2.GaussianBlur(a, (0, 0), px * 0.16) * glow)
    rgb = np.empty((h, w, 3), np.uint8)
    rgb[:] = np.uint8(np.round(np.float32(color) * 255))
    return D.Sprite(rgb, a, sombra=False)


def texto(lz, txt, X, Y, px, t, t0, t1=None, color=BLANCO, fnt="sans_b", glow=0.55, op=1.0, salida=0.35, ancla=0.5):
    """Texto de énfasis de motion graphic (Poppins con halo): entra con rebote en t0, sale en t1."""
    if t < t0:
        return
    u = PF.entra(t, t0, 0.38)
    o = op * clamp01(u * 3)
    if t1 is not None:
        o *= 1.0 - smooth(clamp01((t - t1) / salida))
    if o <= 0.01:
        return
    col = tuple(round(c, 3) for c in color)
    spr = _texto_spr(txt, int(px), col, fnt, glow)
    s = 0.7 + 0.3 * u
    M = np.array([[s, 0, X - s * spr.w * ancla], [0, s, Y - s * spr.h / 2], [0, 0, 1]], np.float64)
    D.pegar(lz, spr, M, o)


# ------------------------------------------------------------------ ambiente
_R = np.random.default_rng(7)
ESTRELLAS = [(x * W, y * H, 0.6 + 1.8 * r, f * 6.28) for x, y, r, f in _R.random((70, 4))]
POLVO = [(x, y, 1.5 + 3 * r, f) for x, y, r, f in _R.random((26, 4))]


def estrellas(lz, t, op=1.0, mascara=None):
    """Estrellas que titilan (encima del fondo; se apagan donde `mascara(X, Y)` es False: planetas, Sol)."""
    for X, Y, r, f in ESTRELLAS:
        v = 0.5 + 0.5 * math.sin(t * (1.3 + r) + f)
        if v < 0.55 or (mascara is not None and not mascara(X, Y)):
            continue
        PF._blob(lz, X, Y, r * 2.2, (0.85, 0.92, 1.0), 0.55 * op * (v - 0.5) * 2, aditivo=True)


def polvo(lz, t, op=0.35, color=(0.70, 0.80, 1.0)):
    """Motas de polvo que derivan delante de la cámara (profundidad en el vacío)."""
    for x, y, r, f in POLVO:
        X = ((x * (W + 200) + t * (14 + 30 * f)) % (W + 200)) - 100
        Y = y * H + 18 * math.sin(t * 0.4 + f * 9)
        PF._blob(lz, X, Y, r * 2.4, color, op * (0.4 + 0.6 * f), aditivo=True)


def roca(lz, pieza, X, Y, alto, t, giro=8.0, fase=0.0, tono=FRIO, op=1.0, rot0=0.0):
    """Asteroide-pegatina que gira despacio en el vacío (ancla al centro, sin sombra de suelo)."""
    PF.actor(lz, pieza, X, Y, alto, rot=rot0 + giro * t + 3 * math.sin(t * 0.7 + fase), ancla=(0.5, 0.5), suelo=0,
             tono=tono, op=op)


def destello_sol(lz, X, Y, r, inten=0.6, color=NARANJA):
    PF._blob(lz, X, Y, r, color, inten, aditivo=True)


def pulso_rojo(lz, k):
    """Viñeta roja (alarma) de intensidad k."""
    if k <= 0.01:
        return
    v = _vin()
    lz += (v * (0.55 * k))[..., None] * np.float32(ROJO)


@functools.lru_cache(maxsize=1)
def _vin():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    return np.clip((d - 0.55) / 0.9, 0, 1) ** 1.6


@functools.lru_cache(maxsize=1)
def _luna_spr():
    """Luna por código (no hay pieza de Flow): disco gris con degradado, cráteres y borde de luz del Sol (izquierda)."""
    n = 400
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    d = np.sqrt((xx - n / 2) ** 2 + (yy - n / 2) ** 2) / (n / 2)
    a = np.clip((1 - d) * n / 4, 0, 1)
    luz = np.clip(0.55 + 0.45 * (-(xx - n / 2) / (n / 2)) + 0.15 * (-(yy - n / 2) / (n / 2)), 0.18, 1.0)
    rgb = np.dstack([luz * 0.62, luz * 0.66, luz * 0.76])
    r = np.random.default_rng(4)
    for cx, cy, cr in r.random((14, 3)):
        cx, cy, cr = n * (0.2 + 0.6 * cx), n * (0.2 + 0.6 * cy), n * (0.03 + 0.07 * cr)
        dc = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / cr
        rgb *= np.where(dc < 1, 0.82, 1.0)[..., None]
    borde = np.clip(1 - np.abs(d - 0.97) * 30, 0, 1) * np.clip(-(xx - n / 2) / (n / 2) + 0.2, 0, 1)
    rgb = rgb + borde[..., None] * np.float32((0.9, 0.7, 0.5)) * 0.6
    return D.Sprite(np.clip(rgb * 255, 0, 255).astype(np.uint8), a, sombra=True, sr=8, off=(6, 8), sop=0.35)


def luna(lz, X, Y, r, op=1.0):
    spr = _luna_spr()
    s = 2 * r / spr.w
    D.pegar(lz, spr, np.array([[s, 0, X - r], [0, s, Y - r], [0, 0, 1]], np.float64), op)


# enjambre de rocas cercanas: (radio de órbita relativo a la de la Tierra, fase, excentricidad, tamaño, hallada)
_RE = np.random.default_rng(11)
ENJ = [(0.70 + 0.65 * a, 6.283 * b, 0.12 * c, 0.6 + 1.6 * d, e < 0.42) for a, b, c, d, e in _RE.random((260, 5))]


def enjambre(lz, t, sol, r_tierra, aplan, u=1.0, modo="todas", op=1.0, sacudir=0.0):
    """Rocas cercanas en órbitas alrededor del Sol (sol = (X, Y) pantalla; r_tierra = radio de la órbita terrestre en px;
    aplan = achatamiento de la perspectiva). modo: «todas» (blanco-azulado), «halladas» (40 % teal / 60 % fantasmas rojos que
    parpadean), «ciegas» (solo contornos que parpadean). u = fracción visible (aparecen de una en una)."""
    n = int(len(ENJ) * clamp01(u))
    if n == 0:
        return
    ma, mb, mc = (np.zeros((H, W), np.uint8) for _ in range(3))
    for k, (rr, f, e, s, hallada) in enumerate(ENJ[:n]):
        ang = f + t * 0.10 / rr ** 1.5
        rad = rr * r_tierra * (1 + e * math.cos(ang * 2))
        X = sol[0] + rad * math.cos(ang)
        Y = sol[1] + rad * math.sin(ang) * aplan + sacudir * math.sin(t * 40 + k)
        if not (-10 < X < W + 10 and -10 < Y < H + 10):
            continue
        rad_px = 1.6 + 1.5 * s
        if modo == "todas":
            cv2.circle(ma, _p(X, Y), int(rad_px * 16), 255, -1, cv2.LINE_AA, 4)
        elif modo == "halladas" and hallada:
            cv2.circle(mb, _p(X, Y), int(rad_px * 16), 255, -1, cv2.LINE_AA, 4)
            cv2.circle(mb, _p(X, Y), int((rad_px + 5) * 16), 255, 1, cv2.LINE_AA, 4)
        else:
            parp = 0.5 + 0.5 * math.sin(t * 5.0 + k * 1.7)
            if parp > 0.35:
                cv2.circle(mc, _p(X, Y), int((rad_px + 1.5) * 16), int(255 * parp), 2, cv2.LINE_AA, 4)
    _mezcla(lz, ma.astype(np.float32) / 255, (0.86, 0.90, 1.0), op, glow=0.9)
    _mezcla(lz, mb.astype(np.float32) / 255, TEAL, op, glow=1.1)
    _mezcla(lz, mc.astype(np.float32) / 255, ROJO, op * 0.85, glow=0.8)


_RC = np.random.default_rng(5)
CORRIENTE = [(0.05 + 0.9 * a, -0.25 + 0.5 * b, 0.05 + 0.10 * c, d, 0.6 + 1.6 * e) for a, b, c, d, e in _RC.random((170, 5))]


def corriente(lz, t, u=1.0, modo="todas", op=1.0):
    """Rocas que cruzan la pantalla de izquierda a derecha con estela (enjambre local junto a la Tierra).
    modo «ciegas» = solo contornos rojos que parpadean (no sabemos dónde están)."""
    n = int(len(CORRIENTE) * clamp01(u))
    if n == 0:
        return
    ma, mc = np.zeros((H, W), np.uint8), np.zeros((H, W), np.uint8)
    for k, (y0, pend, vel, f, s) in enumerate(CORRIENTE[:n]):
        x = ((f + t * vel) % 1.3) - 0.15
        y = y0 + pend * (x - 0.5) + 0.02 * math.sin(t * 0.5 + k)
        X, Y = x * W, y * H
        r = 1.8 + 1.6 * s
        if modo == "todas":
            cv2.circle(ma, _p(X, Y), int(r * 16), 255, -1, cv2.LINE_AA, 4)
            cola = vel * W * 0.9
            cv2.line(ma, _p(X - cola, Y - pend * cola * H / W), _p(X, Y), 90, max(1, int(r * 0.8)), cv2.LINE_AA, 4)
        else:
            parp = 0.5 + 0.5 * math.sin(t * 5.0 + k * 1.7)
            if parp > 0.35:
                cv2.circle(mc, _p(X, Y), int((r + 2) * 16), int(255 * parp), 2, cv2.LINE_AA, 4)
    _mezcla(lz, ma.astype(np.float32) / 255, (0.86, 0.90, 1.0), op, glow=0.9)
    _mezcla(lz, mc.astype(np.float32) / 255, ROJO, op * 0.9, glow=0.8)


def barra(lz, X, Y, w, h, frac, color, t, t0, op=1.0):
    """Barra de progreso MG que se llena desde t0."""
    if t < t0:
        return
    o = op * clamp01((t - t0) / 0.3)
    u = frac * e_inout(clamp01((t - t0) / 0.9))
    trazo(lz, lambda m: cv2.rectangle(m, _p(X, Y), _p(X + w, Y + h), 255, 2, cv2.LINE_AA, 4), BLANCO, o * 0.7, glow=0.3)
    if u > 0.002:
        trazo(lz, lambda m: cv2.rectangle(m, _p(X + 5, Y + 5), _p(X + 5 + (w - 10) * u, Y + h - 5), 255, -1, cv2.LINE_AA, 4),
              color, o, glow=0.8)


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


# escenarios (coordenadas normalizadas del escenario, medidas con la rejilla)
ET_A = dict(tierra=(0.775, 0.72), r=0.226, sol=(-0.06, 0.50))          # espacio_tierra_a: Sol a la izquierda, Tierra abajo a la derecha
ET_B = dict(tierra=(0.905, 0.86), r=0.205, sol=(-0.02, 0.47))          # espacio_tierra_b
SS_A = dict(sol=(0.085, 0.42), tierra=(0.505, 0.50))                    # sistema_solar_a
SS_B = dict(sol=(0.0, 0.56), tierra=(0.664, 0.495))                     # sistema_solar_b


def _escala(pl, t):
    """px de pantalla por unidad normalizada en x del escenario."""
    return pl.ancho_mundo(t)


# 1 · «Esto no está pasando. Todavía.» — una roca a la deriva, iluminada por el Sol; «Todavía» = destello rojo y negro.
P1 = PF.Plano("espacio_tierra_a", 0.0, t_tod + 0.6, z0=1.42, z1=1.26, c0=(0.40, 0.36), c1=(0.47, 0.42), par=(30, 8))
snd(0.0, "grave_inquietante", 0.7)
snd(t_tod - 0.05, "golpe_grave", 0.9)
snd(t_tod, "susto_cuerdas", 0.5)
snd(t_tod + 1.1, "latido", 0.6)


@toma(0.0)
def s1(lz, t):
    P1.fondo(lz, t)
    estrellas(lz, t)
    X = W * (0.40 + 0.012 * t)
    Y = H * (0.48 - 0.006 * t)
    roca(lz, "asteroide_hoja/00", X, Y, H * (0.58 + 0.02 * t), t, giro=4.0, tono=(0.95, 0.92, 0.95))
    destello_sol(lz, -0.05 * W, 0.45 * H, 900, 0.30)                      # borde de luz del Sol que entra por la izquierda
    polvo(lz, t, 0.30)
    # «Todavía»: destello rojo que se come la imagen → negro con un latido rojo
    if t >= t_tod:
        k = math.exp(-(t - t_tod) * 3.2)
        lz *= 1.0 - smooth(prog(t, t_tod + 0.10, t_tod + 0.75))
        lz += np.float32(ROJO) * (0.85 * k)
        lat = max(0.0, math.sin((t - t_tod - 1.1) * math.pi / 0.55)) if t > t_tod + 1.1 else 0.0
        pulso_rojo(lz, 0.45 * lat * (1 - smooth(prog(t, t_ahora - 0.6, t_ahora))))


# 2 · «miles de rocas… cruzan cerca de la Tierra. Y lo peor: no sabemos dónde están.»
P2 = PF.Plano("espacio_tierra_b", t_ahora - 0.3, t_hoy + 0.3, z0=1.10, z1=1.24, c0=(0.58, 0.58), c1=(0.66, 0.66), par=(26, 8))
snd(t_miles, "datos", 0.45)
snd(t_miles + 0.2, "estrellitas", 0.35)
snd(t_no, "apagon", 0.6)
snd(t_donde, "grave_inquietante", 0.6)


@toma(t_ahora - 0.3, ("fundido", 0.6))
def s2(lz, t):
    P2.fondo(lz, t)
    estrellas(lz, t)
    u = smooth(prog(t, t_miles - 0.2, t_tierra + 0.4))
    modo = "todas" if t < t_no else "ciegas"
    corriente(lz, t, u, modo)
    # rocas-pegatina grandes en primer plano que cruzan (escala real de «capaces de borrar una ciudad»)
    for k, (pz, y0, vel, h, ti) in enumerate([("asteroide_hoja/01", 0.30, 0.075, 0.17, t_miles - 0.6),
                                               ("asteroide_hoja/03", 0.62, 0.095, 0.10, t_miles),
                                               ("asteroide_hoja/02", 0.16, 0.06, 0.08, t_ciudad - 0.8)]):
        if t < ti:
            continue
        x = 0.02 + (t - ti) * vel
        o = 1.0 if t < t_no else 1.0 - 0.75 * smooth(prog(t, t_no, t_no + 0.6))
        roca(lz, pz, x * W, (y0 + 0.02 * math.sin(t + k)) * H, h * H, t, giro=12 + 6 * k, fase=k, op=o,
             tono=FRIO if t < t_no else (0.35, 0.36, 0.48))
    polvo(lz, t)
    texto(lz, "MILES", W * 0.27, H * 0.78, 150, t, t_miles, t_peor - 0.3)
    if t >= t_no:
        texto(lz, "¿DÓNDE?", W * 0.30, H * 0.50, 130, t, t_donde - 0.05, t_hoy - 0.2, color=ROJO, glow=0.8)
        pulso_rojo(lz, 0.25 * (0.5 + 0.5 * math.sin(t * 5)))


# 3 · «Hoy vamos a imaginar qué pasaría si una viniera hacia nosotros. Y la viéramos demasiado tarde.»
P3 = PF.Plano("espacio_tierra_a", t_hoy - 0.3, t0C + 0.4, z0=1.02, z1=1.16, c0=(0.50, 0.50), c1=(0.60, 0.56), par=(32, 8))
snd(t_una, "aparicion", 0.5)
snd(t_viniera, "sombra_crece", 0.7)
snd(t_demas, "zoom_whoosh", 0.8)
snd(t_tarde + 0.15, "golpe_grave", 1.0)


def _ruta3(t):
    """Trayectoria de la roca: sale del resplandor del Sol y baja hacia la Tierra (pantalla)."""
    sx, sy, _ = P3.P(t, 0.06, 0.42)
    tx, ty, s = P3.P(t, ET_A["tierra"][0] - 0.06, ET_A["tierra"][1] - 0.10)
    return (sx, sy), (tx, ty)


@toma(t_hoy - 0.3, ("desenfoque", 0.5))
def s3(lz, t):
    P3.fondo(lz, t)
    estrellas(lz, t, mascara=lambda X, Y: X > 0.30 * W)
    (sx, sy), (tx, ty) = _ruta3(t)
    if t >= t_viniera:                                  # trayectoria punteada roja que se tiende hacia la Tierra
        u = e_inout(clamp01((t - t_viniera) / 1.6))
        pts = [(lerp(sx, tx, k / 30), lerp(sy, ty, k / 30) - 60 * math.sin(math.pi * k / 30)) for k in range(31)]
        D.linea_punteada(lz, pts, u, color=ROJO, grosor=4, glow=1.2)
    # la roca: ya asoma en el resplandor desde el arranque (antes la Tierra quedaba 2,5 s sola), avanza por la ruta
    # y crece; «una» = se enciende su borde rojo; «demasiado tarde» = se abalanza a cámara
    t3 = t_hoy - 0.3
    u = clamp01((t - t3) / (t_demas - t3))
    x, y = lerp(sx, tx, 0.55 * u), lerp(sy, ty, 0.55 * u) - 60 * math.sin(math.pi * 0.55 * u)
    h = lerp(26, 150, u ** 1.3)
    if t > t_demas:
        v = e_inout(clamp01((t - t_demas) / (t_tarde + 0.25 - t_demas)))
        x, y, h = lerp(x, W * 0.5, v), lerp(y, H * 0.52, v), lerp(h, H * 1.9, v ** 1.6)
    k = smooth(prog(t, t_una - 0.2, t_una + 0.5))
    roca(lz, "asteroide_hoja/01", x, y, h, t, giro=10, tono=(lerp(0.80, 1.0, k), lerp(0.80, 0.86, k), lerp(0.88, 0.80, k)),
         op=lerp(0.75, 1.0, k) * smooth(prog(t, t3, t3 + 0.5)))
    destello_sol(lz, 0.0, 0.42 * H, 700, 0.25 + 0.05 * math.sin(t * 2))
    polvo(lz, t)
    if t > t_tarde:
        lz *= 1.0 - smooth(prog(t, t_tarde + 0.3, t_tarde + 1.1)) * 0.85
        pulso_rojo(lz, math.exp(-(t - t_tarde) * 1.5))


# 4 · «Se calcula que hay unos 25 mil asteroides cercanos de más de 140 metros. El tamaño justo para destruir una ciudad.»
P4 = PF.Plano("sistema_solar_a", t0C - 0.3, t_hemos + 0.4, z0=1.04, z1=1.14, c0=(0.50, 0.50), c1=(0.47, 0.52), par=(24, 6))
snd(t_calc, "whoosh", 0.5)
snd(t_25, "datos", 0.6, dur=1.8)
snd(t_140, "tick", 0.7)
snd(t_destruir, "golpe_grave", 0.6)
PLANETAS_A = [0.283, 0.37, 0.505, 0.79]                       # x de Mercurio, Venus, Tierra, Marte (y ≈ 0.50)


def _orbitas(lz, t, pl, sol_n, xs, y_n, u, aplan=0.30, op=0.55):
    sx, sy, _ = pl.P(t, *sol_n)
    def fn(m):
        for k, x in enumerate(xs):
            px, py, _ = pl.P(t, x, y_n)
            r = abs(px - sx)
            elipse_punteada(m, sx, sy + (py - sy), r, r * aplan, u=clamp01(u * 1.3 - 0.1 * k), a0=-90, g=2)
    trazo(lz, fn, TEAL, op, glow=0.6)
    return sx, sy


@toma(t0C - 0.3, ("negro", 0.7))
def s4(lz, t):
    P4.fondo(lz, t)
    estrellas(lz, t, mascara=lambda X, Y: X > 0.40 * W)
    sx, sy = _orbitas(lz, t, P4, SS_A["sol"], PLANETAS_A, 0.50, smooth(prog(t, t_calc, t_25 + 0.8)))
    tx, ty, _ = P4.P(t, *SS_A["tierra"])
    pulso = 0.5 + 0.5 * math.sin(t * 6) if t > t_destruir else 0.0
    enjambre(lz, t, (sx, ty), abs(tx - sx), 0.30, u=smooth(prog(t, t_25, t_aster + 0.6)), op=0.85 + 0.15 * pulso)
    n = int(25000 * smooth(prog(t, t_25, t_aster + 0.4)))
    texto(lz, f"{n:,}".replace(",", " "), W * 0.73, H * 0.17, 120, t, t_25, None)
    texto(lz, "asteroides cercanos", W * 0.73, H * 0.27, 44, t, t_aster, None, color=TEAL, fnt="sans")
    texto(lz, "de más de 140 m", W * 0.73, H * 0.34, 44, t, t_140, None, color=ROJO, fnt="sans")
    if t > t_destruir:
        pulso_rojo(lz, 0.18 * pulso)


# 5 · «Hemos encontrado menos de la mitad.» — acercamiento a la órbita de la Tierra: 40 % teal / 60 % fantasmas rojos
P5 = PF.Plano("sistema_solar_a", t_hemos - 0.3, t_2019 + 0.4, z0=1.80, z1=1.95, c0=(0.47, 0.52), c1=(0.50, 0.50), par=(24, 6))
snd(t_hemos, "revelar", 0.6)
snd(t_mitad, "error", 0.5)


@toma(t_hemos - 0.3, ("desenfoque", 0.45))
def s5(lz, t):
    P5.fondo(lz, t)
    estrellas(lz, t)
    sx, sy, _ = P5.P(t, *SS_A["sol"])
    tx, ty, _ = P5.P(t, *SS_A["tierra"])
    enjambre(lz, t, (sx, ty), abs(tx - sx), 0.30, u=1.0, modo="halladas")
    barra(lz, W * 0.30, H * 0.83, W * 0.40, 46, 0.42, TEAL, t, t_hemos + 0.2)
    texto(lz, "HALLADOS", W * 0.30, H * 0.77, 46, t, t_hemos + 0.2, None, color=TEAL, ancla=0.0)
    texto(lz, "menos de la mitad", W * 0.70, H * 0.77, 46, t, t_menos, None, color=ROJO, fnt="sans", ancla=1.0)


# 6 · «En 2019, uno de unos 100 metros pasó a una quinta parte de la distancia a la Luna. Lo descubrieron un día antes.»
P6 = PF.Plano("espacio_tierra_b", t_2019 - 0.3, t_yhay + 0.4, z0=1.00, z1=1.07, c0=(0.50, 0.50), c1=(0.54, 0.53), par=(24, 8))
LUNA6 = (0.30, 0.24)
snd(t_2019, "whoosh", 0.5)
snd(t_paso - 0.3, "zoom_whoosh", 0.8)
snd(t_dia, "golpe_grave", 0.8)
snd(t_dia + 0.1, "susto_cuerdas", 0.4)


@toma(t_2019 - 0.3, ("latigo", 0.45))
def s6(lz, t):
    P6.fondo(lz, t)
    estrellas(lz, t, mascara=lambda X, Y: X > 0.25 * W)
    tx, ty, s = P6.P(t, *ET_B["tierra"])
    rt = ET_B["r"] * _escala(P6, t)
    lx, ly, _ = P6.P(t, *LUNA6)
    dx, dy = lx - tx, ly - ty
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    # línea Tierra–Luna (esquema, sin escala) y la marca de 1/5
    ini = (tx + ux * rt * 1.04, ty + uy * rt * 1.04)
    fin = (lx - ux * 40, ly - uy * 40)
    u = e_inout(clamp01((t - t_2019) / 1.2))
    D.linea_punteada(lz, [ini, fin], u, color=BLANCO, grosor=3, glow=0.6, op=0.8)
    luna(lz, lx, ly, 46 * (0.6 + 0.4 * PF.entra(t, t_2019 - 0.2)), op=smooth(prog(t, t_2019 - 0.3, t_2019 + 0.2)))
    texto(lz, "LUNA", lx, ly + 84, 40, t, t_2019 + 0.2, None, fnt="sans")
    q = 0.42                                       # dónde cae la marca en el esquema (1/5 de la distancia, sin escala)
    mx, my = lerp(ini[0], fin[0], q), lerp(ini[1], fin[1], q)
    if t >= t_quinta:
        o = smooth(prog(t, t_quinta, t_quinta + 0.3))
        trazo(lz, lambda m: cv2.line(m, _p(mx - uy * 26, my + ux * 26), _p(mx + uy * 26, my - ux * 26), 255, 3, cv2.LINE_AA, 4),
              ROJO, o, glow=0.9)
        texto(lz, "1/5", mx - uy * 70, my + ux * 70, 58, t, t_quinta, None, color=ROJO)
    # 2019 OK: cruza de arriba a la izquierda por la marca, rapidísimo, con estela
    ta, tb = t_paso - 1.4, t_paso + 1.6
    if ta <= t:
        v = clamp01((t - ta) / (tb - ta))
        a0 = (mx + uy * 900, my - ux * 900)
        a1 = (mx - uy * 900, my + ux * 900)
        ax, ay = lerp(a0[0], a1[0], v), lerp(a0[1], a1[1], v)
        if v < 1:
            D.linea_punteada(lz, [a0, (ax, ay)], 1.0, color=NARANJA, grosor=3, glow=1.0, op=0.8)
            roca(lz, "asteroide_hoja/02", ax, ay, 70, t, giro=40, tono=(1.0, 0.92, 0.86))
        else:
            D.linea_punteada(lz, [a0, a1], 1.0, color=NARANJA, grosor=3, glow=0.6, op=0.45)
    texto(lz, "2019 OK  ·  ~100 m", W * 0.03, H * 0.64, 60, t, t_100 - 0.1, None, ancla=0.0)
    texto(lz, "sin escala", W * 0.03, H * 0.71, 30, t, t_100, None, color=(0.6, 0.66, 0.78), fnt="sans_l", glow=0.0, ancla=0.0)
    if t >= t_desc:
        texto(lz, "DESCUBIERTO", W * 0.03, H * 0.80, 52, t, t_desc, None, color=ROJO, ancla=0.0)
        texto(lz, "1 DÍA ANTES", W * 0.03, H * 0.89, 80, t, t_dia, None, color=ROJO, glow=0.9, ancla=0.0)
        pulso_rojo(lz, 0.35 * math.exp(-max(0.0, t - t_dia) * 1.2) if t >= t_dia else 0.0)
    polvo(lz, t)


# 7 · «Y hay una parte del cielo que nunca podemos vigilar. La que está junto al Sol.» — cono ROJO Tierra→Sol = PUNTO CIEGO
P7 = PF.Plano("sistema_solar_b", t_yhay - 0.3, t_nuestros + 0.4, z0=1.12, z1=1.22, c0=(0.50, 0.52), c1=(0.47, 0.52), par=(24, 6))
snd(t_cielo, "luz_fria", 0.5)
snd(t_junto, "grave_inquietante", 0.8)
snd(t_sol, "latido", 0.6)


@toma(t_yhay - 0.3, ("desenfoque", 0.5))
def s7(lz, t):
    P7.fondo(lz, t)
    sx, sy, _ = P7.P(t, *SS_B["sol"])
    tx, ty, s = P7.P(t, *SS_B["tierra"])
    estrellas(lz, t, mascara=lambda X, Y: X > sx + 260)
    ang = math.atan2(sy - ty, sx - tx)
    # lo que SÍ vemos: abanico teal hacia el lado nocturno (lejos del Sol)
    u1 = smooth(prog(t, t_cielo - 0.3, t_cielo + 0.6))
    if u1 > 0:
        L1 = 900 * u1
        pts = [(tx, ty)] + [(tx + L1 * math.cos(ang + math.pi + a), ty + L1 * math.sin(ang + math.pi + a))
                            for a in np.linspace(-1.05, 1.05, 16)]
        trazo(lz, lambda m: poligono(m, pts), TEAL, 0.16, glow=0.4)
        texto(lz, "LO QUE VIGILAMOS", min(tx + 260, W - 240), ty - 230, 40, t, t_cielo + 0.2, t_junto - 0.2, color=TEAL, fnt="sans")
    # lo que NO: cono rojo hacia el Sol que palpita
    u2 = smooth(prog(t, t_junto - 0.2, t_junto + 0.5))
    if u2 > 0:
        L2 = math.hypot(sx - tx, sy - ty) * u2
        pts = [(tx, ty)] + [(tx + L2 * math.cos(ang + a), ty + L2 * math.sin(ang + a)) for a in np.linspace(-0.42, 0.42, 14)]
        lat = 0.5 + 0.5 * math.sin(t * 6.5)
        trazo(lz, lambda m: poligono(m, pts), ROJO, 0.13 + 0.10 * lat, glow=0.9)
        trazo(lz, lambda m: cv2.polylines(m, [np.array([_p(*q) for q in (pts[1], pts[0], pts[-1])], np.int32)], False, 255, 3,
                                          cv2.LINE_AA, 4), ROJO, 0.8, glow=0.8)
        Lm = math.hypot(sx - tx, sy - ty) * 0.5
        texto(lz, "PUNTO CIEGO", lerp(tx, sx, 0.5), lerp(ty, sy, 0.5) - Lm * math.tan(0.42) - 120, 82, t, t_junto + 0.1, None,
              color=ROJO, glow=0.9)
        pulso_rojo(lz, 0.2 * lat * u2)
    polvo(lz, t, 0.25)


# 8 · «Nuestros telescopios solo miran de noche. Todo lo que viene desde el lado del Sol llega a ciegas.»
P8 = PF.Plano("espacio_tierra_a", t_nuestros - 0.3, t0X + 1.0, z0=1.32, z1=1.42, c0=(0.66, 0.51), c1=(0.64, 0.52), par=(30, 8))
OBS8 = [(-28, 0.0), (-6, 0.5), (16, 1.0)]                       # observatorios sobre el borde nocturno (grados, fase)
snd(t_telesc, "servo", 0.5)
snd(t_noche, "luz_fria", 0.4)
snd(t_todo, "sombra_crece", 0.7)
snd(t_ciegas, "golpe_grave", 0.9)


@toma(t_nuestros - 0.3, ("latigo", 0.45))
def s8(lz, t):
    P8.fondo(lz, t)
    tx, ty, s = P8.P(t, *ET_A["tierra"])
    rt = ET_A["r"] * _escala(P8, t)
    estrellas(lz, t, mascara=lambda X, Y: math.hypot(X - tx, Y - ty) > rt * 1.05)
    # resplandor del Sol que entra por la izquierda (el lado ciego)
    destello_sol(lz, -0.10 * W, 0.40 * H, 1100, 0.30 + 0.06 * math.sin(t * 1.7))
    # observatorios-pegatina en el lado nocturno (derecha) con su cono teal hacia el cielo oscuro
    for k, (deg, fa) in enumerate(OBS8):
        ti = t_telesc + 0.2 * k
        if t < ti:
            continue
        a = math.radians(-60 + deg)                     # arriba a la derecha del disco
        ox, oy = tx + rt * math.cos(a), ty + rt * math.sin(a)
        u = PF.entra(t, ti, 0.4)
        PF.actor(lz, "utileria/01", ox, oy + 6, 112 * u, rot=math.degrees(a) + 90, suelo=0, tono=FRIO)
        if t > t_noche - 0.2:
            v = smooth(prog(t, t_noche - 0.2, t_noche + 0.4))
            parp = 1.0 if t < t_ciegas else 0.5 + 0.5 * math.sin(t * 14 + k)
            L = 620 * v
            pts = [(ox, oy), (ox + L * math.cos(a - 0.18), oy + L * math.sin(a - 0.18)),
                   (ox + L * math.cos(a + 0.18), oy + L * math.sin(a + 0.18))]
            trazo(lz, lambda m: poligono(m, pts), TEAL, 0.17 * parp, glow=0.5)
    texto(lz, "SOLO DE NOCHE", W * 0.24, H * 0.14, 60, t, t_noche, t_todo + 0.4, color=TEAL)
    # la roca: sale del resplandor y cruza el lado de día, sin que nadie la vea
    if t >= t_todo:
        v = clamp01((t - t_todo) / (t0X + 1.0 - t_todo))
        x, y = lerp(-0.05 * W, tx - rt * 0.95, v), lerp(0.30 * H, ty - rt * 0.55, v)
        roca(lz, "asteroide_hoja/00", x, y, lerp(80, 190, v), t, giro=14, tono=(0.62, 0.50, 0.46))
        D.linea_punteada(lz, [(-0.05 * W, 0.30 * H), (x, y)], 1.0, color=ROJO, grosor=3, glow=0.7, op=0.5 * smooth(prog(t, t_lado, t_lado + 0.5)))
    if t >= t_ciegas:
        texto(lz, "A CIEGAS", W * 0.30, H * 0.80, 120, t, t_ciegas, None, color=ROJO, glow=0.9)
        pulso_rojo(lz, 0.35 * (0.5 + 0.5 * math.sin(t * 5)))
    polvo(lz, t)


# ================================================================== tramo 2b (20-oct-2026): cheliabinsk · punto · numeros
X_, PU, NU = "cheliabinsk", "punto", "numeros"
x_en, x_2013, x_20, x_salio, x_chel, x_nadie, x_venir = (T(X_, "en", 0), T(X_, "2013", 0), T(X_, "20", 0), T(X_, "salió", 0),
                                                        T(X_, "cheliábinsk", 0), T(X_, "nadie", 0), T(X_, "venir", 0))
x_la, x_dest, x_corrio = T(X_, "la", 1), T(X_, "destello", 1), T(X_, "corrió", 1)
x_min, x_onda, x_mas, x_heridos, x_vidrios = (T(X_, "minutos", 2), T(X_, "onda", 2), T(X_, "más", 2), T(X_, "heridos", 2),
                                              T(X_, "vidrios", 2))
x_era, x_20b, x_ahora, x_imagina, x_400 = T(X_, "era", 3), T(X_, "20", 3), T(X_, "ahora", 3), T(X_, "imagina", 3), T(X_, "400", 3)
t0P = _ESC[PU]["t0"]
p_chile, p_astr, p_revisa = T(PU, "chile", 0), T(PU, "astrónoma", 0), T(PU, "revisa", 0)
p_hay, p_punto, p_ayer, p_estaba = T(PU, "hay", 1), T(PU, "punto", 1), T(PU, "ayer", 1), T(PU, "estaba", 1)
p_y, p_inq, p_casi, p_mueve = T(PU, "y", 2), T(PU, "inquieta", 2), T(PU, "casi", 2), T(PU, "mueve", 2)
p_las, p_pasan, p_largo, p_cielo, p_viene, p_directo, p_quieta, p_crece = (
    T(PU, "las", 3), T(PU, "pasan", 3), T(PU, "largo", 3), T(PU, "cielo", 3), T(PU, "viene", 3), T(PU, "directo", 3),
    T(PU, "quieta", 3), T(PU, "crece", 3))
p_mide, p_400, p_faltan, p_20, p_horas = T(PU, "mide", 4), T(PU, "400", 4), T(PU, "faltan", 4), T(PU, "20", 4), T(PU, "horas", 4)
t0N = _ESC[NU]["t0"]
n_prob, n_sube, n_hora, n_1, n_10, n_60 = (T(NU, "probabilidad", 0), T(NU, "sube", 0), T(NU, "hora", 0), T(NU, "1", 0),
                                          T(NU, "10", 0), T(NU, "60", 0))
n_100 = T(NU, "100", 1)
n_nada, n_unica, n_nave, n_tardo, n_meses, n_llegar = (T(NU, "nada", 2), T(NU, "única", 2), T(NU, "nave", 2), T(NU, "tardó", 2),
                                                       T(NU, "meses", 2), T(NU, "llegar", 2))
n_una, n_400, n_20, n_libera, n_5, n_mega = (T(NU, "una", 3), T(NU, "400", 3), T(NU, "20", 3), T(NU, "libera", 3), T(NU, "5", 3),
                                             T(NU, "megatones", 3))
n_cien, n_bomba, n_jamas = T(NU, "cien", 4), T(NU, "bomba", 4), T(NU, "jamás", 4)
t0A = _ESC["alerta"]["t0"]

MANANA = (0.80, 0.85, 1.0)        # luz fría de la mañana rusa
PANT = (0.72, 0.84, 1.04)         # luz de monitores
SALA = (0.62, 0.70, 0.95)         # sala de crisis en penumbra


# ------------------------------------------------------------------ utilidades del tramo 2b
def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, fase=0.0, t_in=None, rot=0.0):
    """Personaje u objeto quieto que respira; si `t_in`, se pega con rebote (como en jalpa)."""
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    X, Y, h = pl.en(t, x, y, frac)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def corre(lz, pl, t, ciclo, ta, tb, x0, x1, y0, y1, frac, tono=None, paso=1.35):
    """Ciclo de carrera de Flow (pintado hacia la derecha; se voltea si va a la izquierda): el cuadro sale de la distancia
    recorrida, así los pies no patinan. Entra y sale por fuera del cuadro."""
    if not ta <= t <= tb:
        return
    u = (t - ta) / (tb - ta)
    X, Y, h = pl.en(t, lerp(x0, x1, u), lerp(y0, y1, u), frac)
    n = PF.ciclo_n(ciclo)
    i = PF.cuadro_ciclo(abs(x1 - x0) * u * pl.ancho_mundo(t), paso * h, n)
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h, flip=x1 < x0, tono=tono)


def fondo_quieto(pl, t, sigma):
    """Fondo con profundidad de campo (desenfocado) para planos de detalle."""
    lz = np.zeros((H, W, 3), np.float32)
    pl.fondo(lz, t)
    return cv2.GaussianBlur(lz, (0, 0), sigma)


def sacudir(lz, k, t, f=31.0):
    """Sacudida de cámara (onda expansiva): desplaza el cuadro k px con ruido."""
    if k < 0.5:
        return
    dx = k * (math.sin(t * f) + 0.5 * math.sin(t * f * 2.3 + 1.0))
    dy = k * 0.7 * (math.cos(t * f * 1.1) + 0.5 * math.sin(t * f * 1.9))
    lz[:] = cv2.warpAffine(lz, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)


def estela(lz, t, ruta, ta, tb, n=46, color=(0.84, 0.85, 0.90), op=0.5, s=1.0):
    """Estela de humo de un bólido: bocanadas emitidas a lo largo de la ruta entre ta y tb que se abren, caen un poco y se
    desvanecen despacio con la edad. ruta(u) → (X, Y) en pantalla."""
    te_fin = min(t, tb)
    if te_fin <= ta:
        return
    for i in range(n):
        u = i / (n - 1)
        te = lerp(ta, tb, u)
        if te > te_fin:
            break
        edad = t - te
        X, Y = ruta(u)
        r = (9 + 20 * min(edad, 8.0) ** 0.7) * s
        PF._blob(lz, X + 3 * math.sin(edad * 0.8 + i), Y + 5 * edad * s, r, color, op * math.exp(-edad * 0.05) * (0.55 + 0.45 * u))


def anillo(lz, X, Y, r, grosor, color=BLANCO, op=0.7):
    trazo(lz, lambda m: cv2.circle(m, _p(X, Y), int(r * 16), 255, int(grosor), cv2.LINE_AA, 4), color, op, glow=1.3)


_RV = np.random.default_rng(21)
VIDRIOS = [(6.283 * a, 0.5 + 1.2 * b, 6 + 16 * c, 6.283 * d, 3 * (e - 0.5)) for a, b, c, d, e in _RV.random((70, 5))]


def vidrios(lz, t, t0, X, Y, fuerza=1.0, op=1.0, giro0=0.0):
    """Esquirlas de vidrio que salen disparadas hacia la cámara desde (X, Y): triángulos que giran, crecen y caen."""
    if t < t0:
        return
    dt = t - t0
    def fn(m):
        for ang, v, s, f, giro in VIDRIOS:
            d = v * 700 * fuerza * (1 - math.exp(-dt * 2.2))
            x = X + d * math.cos(ang + giro0)
            y = Y + d * math.sin(ang + giro0) * 0.75 + 260 * dt * dt
            k = s * (1 + 1.4 * dt)
            a = f + giro * dt * 4
            poligono(m, [(x + k * math.cos(a), y + k * math.sin(a)), (x + 0.6 * k * math.cos(a + 2.3), y + 0.6 * k * math.sin(a + 2.3)),
                         (x + 0.8 * k * math.cos(a + 4.1), y + 0.8 * k * math.sin(a + 4.1))])
    trazo(lz, fn, (0.78, 0.95, 1.0), op * 0.8 * math.exp(-dt * 0.6), glow=0.6)


_RN = np.random.default_rng(31)
NIEVE = [(a, b, 1.2 + 2.6 * c, d) for a, b, c, d in _RN.random((90, 4))]


def nieve(lz, t, op=0.5, viento=0.0):
    """Copos que caen y derivan (Rusia, febrero)."""
    for x, y, r, f in NIEVE:
        Y = ((y * (H + 60) + t * (40 + 50 * f)) % (H + 60)) - 30
        X = ((x * (W + 100) + t * (12 + viento * 900) * (0.5 + f) + 22 * math.sin(t * 0.9 + f * 7)) % (W + 100)) - 50
        PF._blob(lz, X, Y, r * 2.2, (0.92, 0.95, 1.0), op * (0.5 + 0.5 * f))


def caja(lz, R, color, op=0.95, borde=None, glow=0.5, g=2):
    X0, Y0, X1, Y1 = R
    trazo(lz, lambda m: cv2.rectangle(m, _p(X0, Y0), _p(X1, Y1), 255, -1, cv2.LINE_AA, 4), color, op, glow=0.0)
    if borde is not None:
        trazo(lz, lambda m: cv2.rectangle(m, _p(X0, Y0), _p(X1, Y1), 255, g, cv2.LINE_AA, 4), borde, 0.85 * op, glow=glow)


def banda(lz, X0, X1, Ya, Yb, color, op):
    """Resplandor aditivo en degradado vertical (0 arriba en Ya → 1 abajo en Yb) entre X0 y X1."""
    xa, xb, ya, yb = int(max(0, X0)), int(min(W, X1)), int(Ya), int(Yb)
    if xb <= xa or yb <= ya:
        return
    g = np.linspace(0, 1, yb - ya, dtype=np.float32) ** 1.6
    a, b = max(ya, 0), min(yb, H)
    if b <= a:
        return
    lz[a:b, xa:xb] += (g[a - ya:b - ya] * op)[:, None, None] * np.float32(color)


def rect_P(pl, t, r):
    """Rectángulo (x0, y0, x1, y1) del escenario → pantalla."""
    X0, Y0, _ = pl.P(t, r[0], r[1])
    X1, Y1, _ = pl.P(t, r[2], r[3])
    return X0, Y0, X1, Y1


def cielo_pant(lz, R, sem=0, n=60, op=1.0, horizonte=True, monte=False, borde=TEAL):
    """Imagen del telescopio dentro de una pantalla: campo de estrellas (sem = otra imagen), resplandor del atardecer abajo y
    silueta de los cerros."""
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    caja(lz, R, (0.025, 0.05, 0.10), op * 0.97)
    if horizonte:
        banda(lz, X0, X1, Y1 - 0.35 * h, Y1, (1.0, 0.42, 0.16), 0.45 * op)
    pts = np.random.default_rng(sem).random((n, 3))
    rad = max(1.0, w / 300)
    def fn(m):
        for a, b, c in pts:
            cv2.circle(m, _p(X0 + (0.03 + 0.94 * a) * w, Y0 + (0.04 + 0.70 * b) * h), int(rad * (0.6 + c) * 16), 255, -1,
                       cv2.LINE_AA, 4)
    trazo(lz, fn, (0.85, 0.92, 1.0), op, glow=0.3)
    if monte:
        cerro = [(X0, Y1)] + [(X0 + w * k / 14, Y1 - h * (0.05 + 0.10 * abs(math.sin(k * 1.7 + sem)))) for k in range(15)] + [(X1, Y1)]
        trazo(lz, lambda m: poligono(m, cerro), (0.01, 0.015, 0.03), op, glow=0.0)
    if borde is not None:
        trazo(lz, lambda m: cv2.rectangle(m, _p(X0, Y0), _p(X1, Y1), 255, 2, cv2.LINE_AA, 4), borde, 0.7 * op, glow=0.8)


def reticula(lz, X, Y, r, t, t0, color=ROJO, op=1.0):
    """Mira de seguimiento que se cierra sobre un punto."""
    if t < t0:
        return
    u = e_inout(clamp01((t - t0) / 0.5))
    rr = r * (1.8 - 0.8 * u)
    def fn(m):
        cv2.circle(m, _p(X, Y), int(rr * 16), 255, 3, cv2.LINE_AA, 4)
        cv2.circle(m, _p(X, Y), int(rr * 0.45 * 16), 255, 2, cv2.LINE_AA, 4)
        for a in range(4):
            ca, sa = math.cos(a * math.pi / 2), math.sin(a * math.pi / 2)
            cv2.line(m, _p(X + ca * rr * 0.75, Y + sa * rr * 0.75), _p(X + ca * rr * 1.35, Y + sa * rr * 1.35), 255, 3, cv2.LINE_AA, 4)
    trazo(lz, fn, color, op * clamp01((t - t0) / 0.25), glow=0.9)


def cota(lz, X, Y0, Y1, t, t0, txt, color=TEAL, px=48, op=1.0):
    """Cota vertical de medida |—| que se tiende desde t0, con su texto a la derecha."""
    if t < t0 or op <= 0.01:
        return
    u = e_inout(clamp01((t - t0) / 0.5))
    ym = (Y0 + Y1) / 2
    a, b = lerp(ym, Y0, u), lerp(ym, Y1, u)
    def fn(m):
        cv2.line(m, _p(X, a), _p(X, b), 255, 3, cv2.LINE_AA, 4)
        for yy in (a, b):
            cv2.line(m, _p(X - 16, yy), _p(X + 16, yy), 255, 3, cv2.LINE_AA, 4)
    trazo(lz, fn, color, op * clamp01((t - t0) / 0.2), glow=0.7)
    texto(lz, txt, X + 30, ym, px, t, t0 + 0.2, None, color=color, ancla=0.0, op=op)


def aves(lz, t, vuelos, tono=(0.30, 0.32, 0.42)):
    """vuelos: [(t_ini, dur, y0, y1, alto px, sentido, fase)] en pantalla; aleteo a 9 cuadros/s (como en jalpa)."""
    n = PF.ciclo_n("aves_aleteo")
    for t_i, dur, y0, y1, hpx, sent, fa in vuelos:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(-0.08, 1.08, u) if sent > 0 else lerp(1.08, -0.08, u)
        y = lerp(y0, y1, u) + 0.012 * math.sin(t * 2.1 + fa)
        k = int(t * 9 + fa * 7) % n
        PF.actor(lz, f"aves_aleteo/ciclo_{k:02d}", x * W, y * H, hpx, flip=sent < 0, ancla=(0.5, 0.5), suelo=0, tono=tono)


def hongo(m, cx, cy, s):
    """Silueta de hongo nuclear (máscara) con la base en (cx, cy) y altura s px."""
    poligono(m, [(cx - 0.07 * s, cy), (cx + 0.07 * s, cy), (cx + 0.05 * s, cy - 0.62 * s), (cx - 0.05 * s, cy - 0.62 * s)])
    cv2.ellipse(m, _p(cx, cy - 0.40 * s), _p(0.15 * s, 0.04 * s), 0, 0, 360, 255, -1, cv2.LINE_AA, 4)
    cv2.ellipse(m, _p(cx, cy - 0.72 * s), _p(0.34 * s, 0.17 * s), 0, 0, 360, 255, -1, cv2.LINE_AA, 4)
    for k in (-1, 1):
        cv2.circle(m, _p(cx + k * 0.21 * s, cy - 0.80 * s), int(0.15 * s * 16), 255, -1, cv2.LINE_AA, 4)
    cv2.circle(m, _p(cx, cy - 0.87 * s), int(0.17 * s * 16), 255, -1, cv2.LINE_AA, 4)
    cv2.ellipse(m, _p(cx, cy), _p(0.26 * s, 0.05 * s), 0, 0, 360, 255, -1, cv2.LINE_AA, 4)


_RG = np.random.default_rng(13)
CRATERES = [(-1.0 + 2.0 * a, -1.0 + 2.0 * b, 0.008 + 0.04 * c ** 2) for a, b, c in _RG.random((900, 3))]


@functools.lru_cache(maxsize=1)
def _textura_roca(n=1024):
    """Grano de roca (ruido de varias octavas) para la superficie de la roca gigante."""
    r = np.random.default_rng(3)
    tex = np.zeros((n, n), np.float32)
    for k, a in ((8, 0.5), (32, 0.3), (128, 0.2)):
        tex += a * cv2.resize(r.random((k, k)).astype(np.float32), (n, n), interpolation=cv2.INTER_CUBIC)
    return (tex - tex.min()) / (tex.max() - tex.min())


def roca_gigante(lz, Xc, Yc, R, t, op=1.0):
    """Asteroide de 400 m a escala real (mucho más grande que la pantalla), dibujado por código: a ese tamaño una pieza de
    Flow se vería borrosa. Disco irregular sombreado, cráteres, contorno de tinta y borde de luz teal (paleta de las piezas)."""
    X, Y = PF._grid()
    dx, dy = (X - Xc) / R, (Y - Yc) / R
    d = np.sqrt(dx * dx + dy * dy)
    if float(d.min()) > 1.1:
        return
    th = np.arctan2(dy, dx) + t * 0.02
    borde = (1.0 + 0.02 * np.sin(3 * th + 1.0) + 0.010 * np.sin(23 * th + 0.4) + 0.006 * np.sin(51 * th + 2.0)
             + 0.0035 * np.abs(np.sin(113 * th + 1.3)) + 0.002 * np.sin(241 * th))
    a = np.clip((borde - d) * R / 2.0, 0, 1)
    n = 1023
    tex = cv2.remap(_textura_roca(), np.clip((dx * 0.5 + 0.5) * n, 0, n), np.clip((dy * 0.5 + 0.5) * n, 0, n), cv2.INTER_LINEAR)
    luz = np.clip((0.48 - 0.38 * dx) * (0.55 + 0.9 * tex), 0.10, 1.0)
    rgb = np.stack([luz * 0.32, luz * 0.35, luz * 0.46], -1)
    mc, mb = np.zeros((H, W), np.uint8), np.zeros((H, W), np.uint8)
    for cx, cy, cr in CRATERES:
        if cx * cx + cy * cy > 0.99:
            continue
        x, y, r = Xc + cx * R, Yc + cy * R, cr * R
        if x + r < 0 or x - r > W or y + r < 0 or y - r > H:
            continue
        cv2.ellipse(mc, _p(x, y), _p(r, r * 0.82), 0, 0, 360, 255, -1, cv2.LINE_AA, 4)
        cv2.ellipse(mb, _p(x, y), _p(r, r * 0.82), 0, 200, 340, 255, max(2, int(r * 0.10)), cv2.LINE_AA, 4)
    rgb *= (1.0 - 0.40 * mc.astype(np.float32) / 255)[..., None]
    rgb += (mb.astype(np.float32) / 255 * 0.16)[..., None]
    rim = np.clip(1 - (borde - d) * R / 60.0, 0, 1)
    rgb += (rim * np.clip(-dx + 0.3, 0, 1))[..., None] * np.float32(NARANJA) * 0.55     # el Sol bajo, a la izquierda
    rgb += (rim * np.clip(dx + 0.3, 0, 1))[..., None] * np.float32(TEAL) * 0.30
    k = (a * op)[..., None]
    lz[:] = lz * (1 - k) + rgb * k
    tinta = np.clip(1 - np.abs(borde - d) * R / 4.0, 0, 1) * op
    lz *= (1 - 0.85 * tinta)[..., None]


# ------------------------------------------------------------------ cheliabinsk
CH_B = dict(chim=[(0.275, 0.41, 0.8), (0.842, 0.215, 1.2), (0.876, 0.19, 1.2)], vent=[(0.687, 0.447), (0.687, 0.535)])
CH_A = dict(chim=[(0.207, 0.34, 0.7), (0.232, 0.34, 0.7), (0.445, 0.33, 1.1)])
VENT_A = [(0.30, 0.55), (0.40, 0.53), (0.47, 0.55), (0.55, 0.52), (0.62, 0.54), (0.70, 0.51)]
BOL = ((0.12, 0.42), (0.33, 0.24), (0.60, 0.27))            # bólido en cheliabinsk_b: del resplandor del Sol al estallido
BOL_A = ((-0.10, 0.22), (0.30, 0.04), (0.78, 0.13))         # la misma estela vista desde cheliabinsk_a
GENTE = [("gente_hoja/02", 0.56, 0.78, 0.20, False, 0.35), ("gente_hoja/01", 0.66, 0.80, 0.21, False, 0.10),
         ("gente_hoja/04", 0.74, 0.86, 0.14, False, 0.90), ("gente_hoja/03", 0.81, 0.87, 0.25, True, 0.20)]


def _bez(u, pts):
    (ax, ay), (cx, cy), (bx, by) = pts
    v = 1 - u
    return v * v * ax + 2 * v * u * cx + u * u * bx, v * v * ay + 2 * v * u * cy + u * u * by


def bolido(lz, pl, t, ta, tb, pts, h0=50, h1=175, estela_op=0.5):
    """Bólido de Cheliábinsk: sale del resplandor en ta, cruza con su estela de humo y estalla en tb."""
    if t < ta:
        return
    def ruta(u):
        X, Y, _ = pl.P(t, *_bez(u, pts))
        return X, Y
    estela(lz, t, ruta, ta, tb, op=estela_op)
    if t < tb:
        u = (t - ta) / (tb - ta)
        X, Y = ruta(u)
        X2, Y2 = ruta(min(1.0, u + 0.01))
        ang = math.degrees(math.atan2(Y2 - Y, X2 - X))
        PF.brillo(lz, X, Y, lerp(90, 280, u), color=(1.0, 0.70, 0.35), inten=0.6, t=t)
        PF.actor(lz, "asteroide_hoja/04", X, Y, lerp(h0, h1, u), rot=ang - 45, ancla=(0.62, 0.62), suelo=0,
                 sombra=False)
    else:
        X, Y = ruta(1.0)
        k = math.exp(-(t - tb) * 1.4)
        PF._blob(lz, X, Y, 260 + 520 * (1 - k), (1.0, 0.85, 0.6), 0.9 * k, aditivo=True)


def _ambiente_ch(lz, pl, t, chim, vent=(), op_nieve=0.5, viento=0.0):
    for k, (x, y, s) in enumerate(chim):
        X, Y, _ = pl.P(t, x, y)
        PF.humo(lz, t, X, Y, s=s, n=7, color=(0.70, 0.74, 0.80), op=0.26, sem=k)
    for k, (x, y) in enumerate(vent):
        X, Y, _ = pl.P(t, x, y)
        PF.brillo(lz, X, Y, 26, color=(1.0, 0.42, 0.20), inten=0.35, t=t, sem=k)
    nieve(lz, t, op_nieve, viento)


def _gente(lz, pl, t, t_ref, rot=0.0):
    for k, (pz, x, y, frac, fl, dt) in enumerate(GENTE):
        quieto(lz, pl, t, pz, x, y, frac, flip=fl, tono=MANANA, fase=k, t_in=None if t_ref is None else t_ref + dt, rot=rot)


# 9 · «En 2013, una roca de 20 metros salió del resplandor del Sol sobre Cheliábinsk, en Rusia. Nadie la vio venir.»
P9 = PF.Plano("cheliabinsk_b", x_en - 0.35, x_la, z0=1.10, z1=1.20, c0=(0.47, 0.50), c1=(0.50, 0.45), par=(26, 6))
snd(x_2013, "viento", 0.45, dur=4.0)
snd(x_salio, "subida", 0.6)
snd(x_venir - 0.05, "relampago_corto", 0.9)


@toma(x_en - 0.35, ("desenfoque", 0.5))
def s9(lz, t):
    P9.fondo(lz, t)
    _ambiente_ch(lz, P9, t, CH_B["chim"], CH_B["vent"])
    ta = x_salio - 0.2
    bolido(lz, P9, t, ta, x_venir, BOL)
    if x_salio + 0.4 <= t < x_venir:
        X, Y, _ = P9.P(t, *_bez((t - ta) / (x_venir - ta), BOL))
        texto(lz, "20 m", X + 60, Y + 80, 42, t, x_salio + 0.4, x_venir - 0.4, ancla=0.0)
    texto(lz, "2013", W * 0.5, H * 0.09, 86, t, x_2013, x_nadie)
    texto(lz, "CHELIÁBINSK · RUSIA", W * 0.5, H * 0.17, 46, t, x_chel, None, color=TEAL, fnt="sans")
    if t >= x_venir:                                    # el fogonazo: el cielo entero se vuelve blanco
        lz += np.float32((1.0, 0.95, 0.88)) * (0.95 * math.exp(-(t - x_venir) * 2.2))


# 10 · «La gente vio el destello y corrió a las ventanas a mirar.»
P10 = PF.Plano("cheliabinsk_a", x_la - 0.3, x_min, z0=1.18, z1=1.30, c0=(0.50, 0.56), c1=(0.55, 0.58), par=(30, 8))
snd(x_la, "multitud", 0.35, dur=4.0)
snd(x_corrio, "pasos", 0.6, dur=2.4)


@toma(x_la - 0.3, ("fundido", 0.4))
def s10(lz, t):
    P10.fondo(lz, t)
    bolido(lz, P10, t, x_salio - 0.2, x_venir, BOL_A, estela_op=0.45)
    _ambiente_ch(lz, P10, t, CH_A["chim"])
    _gente(lz, P10, t, x_dest)
    corre(lz, P10, t, "mujer_corre", x_corrio + 0.5, x_corrio + 3.1, -0.12, 1.10, 0.90, 0.88, 0.34, tono=MANANA)
    corre(lz, P10, t, "persona_corre", x_corrio - 0.3, x_corrio + 2.1, -0.12, 1.10, 0.98, 0.95, 0.42, tono=MANANA)


# 11 · «Minutos después llegó la onda expansiva.» — el frente de onda barre la ciudad: sacudida, nieve arrancada, ventanas
P11 = PF.Plano("cheliabinsk_a", x_min - 0.3, x_mas, z0=1.04, z1=1.10, c0=(0.50, 0.52), c1=(0.50, 0.53), par=(24, 6))
ONDA = (0.20, -0.35)                                         # el estallido, fuera de cuadro arriba a la izquierda
t_ondaL = x_onda - 0.40
snd(x_min, "silencio_tono", 0.4)
snd(x_onda - 0.1, "trueno", 1.0)
snd(x_onda + 0.15, "crujido", 0.7)
snd(x_onda + 0.30, "clink", 0.5, tono=1.4)


@toma(x_min - 0.3, ("corte", 0.1))
def s11(lz, t):
    P11.fondo(lz, t)
    bolido(lz, P11, t, x_salio - 0.2, x_venir, BOL_A, estela_op=0.40)
    golpe = smooth(prog(t, x_onda - 0.05, x_onda + 0.2)) * math.exp(-max(0.0, t - x_onda) * 0.8)
    _ambiente_ch(lz, P11, t, CH_A["chim"], viento=1.5 * golpe)
    if t >= t_ondaL:
        ox, oy, _ = P11.P(t, *ONDA)
        r = (t - t_ondaL) * 2400
        o = 0.75 * math.exp(-(t - t_ondaL) * 0.9)
        anillo(lz, ox, oy, r, 34, (0.92, 0.96, 1.0), o)
        anillo(lz, ox, oy, r * 0.93, 10, (0.92, 0.96, 1.0), o * 0.5)
    _gente(lz, P11, t, None, rot=-12 * golpe)
    PF.arena_viento(lz, t, fuerza=1.2 * golpe, y0=0.60, y1=1.0, color=(0.92, 0.95, 1.0))
    for k, (x, y) in enumerate(VENT_A):                        # ventanas que revientan una tras otra
        tk = x_onda + 0.05 * k
        if t >= tk:
            X, Y, _ = P11.P(t, x, y)
            PF._blob(lz, X, Y, 34, (0.9, 0.97, 1.0), 0.8 * math.exp(-(t - tk) * 3), aditivo=True)
    X, Y, _ = P11.P(t, 0.47, 0.55)
    vidrios(lz, t, x_onda + 0.05, X, Y, fuerza=0.5, op=0.8)
    texto(lz, "MINUTOS DESPUÉS", W * 0.5, H * 0.10, 48, t, x_min, x_onda - 0.3, color=TEAL, fnt="sans")
    lz += np.float32((0.9, 0.95, 1.0)) * (0.22 * golpe)
    sacudir(lz, 22 * golpe, t)


# 12 · «Más de mil heridos, casi todos por vidrios rotos.» — una ventana revienta hacia cámara
P12 = PF.Plano("cheliabinsk_a", x_mas - 0.4, x_era, z0=2.30, z1=2.45, c0=(0.62, 0.52), c1=(0.60, 0.53), par=(30, 8),
               tono=(0.70, 0.76, 0.92))
snd(x_mas - 0.35, "estallido", 0.8)
snd(x_mas - 0.30, "clink", 0.6, tono=1.2)
snd(x_heridos, "tambor", 0.6)
snd(x_vidrios, "clink", 0.5, tono=0.85)


@toma(x_mas - 0.4, ("latigo", 0.35))
def s12(lz, t):
    lz[:] = fondo_quieto(P12, t, 3.0)
    nieve(lz, t, 0.4, viento=0.4)
    t_v = x_mas - 0.35
    u = PF.entra(t, t_v, 0.35)
    jit = 7 * math.exp(-max(0.0, t - t_v) * 2.0) if t >= t_v else 0.0
    if t >= t_v:
        PF.actor(lz, "utileria/06", W * 0.30 + jit * math.sin(t * 50), H * 0.56, H * 0.66 * (0.7 + 0.3 * u),
                 rot=-4 + 3 * math.sin(t * 0.8), ancla=(0.5, 0.5), suelo=0, tono=(0.85, 0.90, 1.0), op=clamp01(u * 3))
    vidrios(lz, t, x_mas - 0.30, W * 0.30, H * 0.52, fuerza=1.0)
    vidrios(lz, t, x_vidrios, W * 0.30, H * 0.52, fuerza=0.7, giro0=0.4)
    n = int(1000 * smooth(prog(t, x_mas, x_heridos)))
    texto(lz, f"+{n:,}".replace(",", " "), W * 0.71, H * 0.40, 170, t, x_mas, None)
    texto(lz, "HERIDOS", W * 0.71, H * 0.56, 80, t, x_heridos, None, color=ROJO, glow=0.8)
    texto(lz, "VIDRIOS ROTOS", W * 0.71, H * 0.67, 48, t, x_vidrios, None, color=TEAL, fnt="sans")
    if t > x_heridos:
        pulso_rojo(lz, 0.25 * math.exp(-(t - x_heridos) * 1.5))
    sacudir(lz, jit * 2, t)


# 13 · «Era una roca de 20 metros. Ahora imagina una de 400.» — la de 20 m junto a un edificio; la de 400, a escala real
P13a = PF.Plano("cheliabinsk_b", x_era - 0.3, x_ahora, z0=1.55, z1=1.50, c0=(0.60, 0.42), c1=(0.60, 0.43), par=(26, 6))
P13b = PF.Plano("cheliabinsk_b", x_ahora, x_400 + 0.8, z0=1.50, z1=1.02, c0=(0.60, 0.43), c1=(0.50, 0.50), par=(26, 6))
ROCA20 = (0.38, 0.27, 0.23)          # centro (x, y) y alto (fracción del alto del escenario): 20 m junto a un bloque de ~30 m
EDIF = (0.31, 0.66)                  # tejado y base del bloque grande de cheliabinsk_b
snd(x_era, "aparicion", 0.45)
snd(x_imagina, "caida", 0.6)
snd(x_400 + 0.2, "trueno_noir", 0.9)


@toma(x_era - 0.3, ("desenfoque", 0.5))
def s13(lz, t):
    pl = P13a if t < x_ahora else P13b
    pl.fondo(lz, t)
    _ambiente_ch(lz, pl, t, CH_B["chim"], CH_B["vent"], op_nieve=0.35)
    Xr, Yr, _ = pl.P(t, ROCA20[0], ROCA20[1] + 0.09 * e_inout(prog(t, x_ahora, x_400)))
    hr = pl.alto_px(t, ROCA20[2])
    roca(lz, "asteroide_hoja/03", Xr, Yr, hr, t, giro=6, tono=MANANA, op=smooth(prog(t, x_era - 0.1, x_era + 0.4)))
    cota(lz, Xr + hr * 0.62, Yr - hr * 0.45, Yr + hr * 0.45, t, x_20b - 0.1, "20 m", op=1 - smooth(prog(t, x_400 - 0.4, x_400)))
    if t >= x_400 - 0.3:
        _, Yt, _ = pl.P(t, 0.6, EDIF[0])
        _, Yb, _ = pl.P(t, 0.6, EDIF[1])
        R = (Yb - Yt) * 13.3 / 2                        # 400 m ≈ 13 bloques de 30 m
        u = e_inout(clamp01((t - (x_400 - 0.3)) / 1.1))
        canto = lerp(-0.05 * H, Yt - 0.06 * H, u)        # borde inferior de la roca gigante, sobre los tejados
        lz *= 1.0 - 0.40 * u                             # su sombra se come la ciudad
        roca_gigante(lz, W * 0.52, canto - R, R, t)
        texto(lz, "400 m", W * 0.5, canto - 0.10 * H, 140, t, x_400 + 0.3, None, color=ROJO, glow=0.9)
        pulso_rojo(lz, 0.35 * u * (0.6 + 0.4 * math.sin(t * 5)))


# ------------------------------------------------------------------ punto
SO_B = dict(mon=[(0.185, 0.41, 0.25, 0.53), (0.262, 0.40, 0.371, 0.535), (0.384, 0.43, 0.466, 0.53)], roja=(0.854, 0.57),
            ranura=(0.56, 0.0, 0.80, 0.38))
SO_A = dict(mon=[(0.684, 0.43, 0.775, 0.533), (0.7875, 0.404, 0.8875, 0.549), (0.90, 0.42, 0.956, 0.545)], roja=(0.638, 0.31),
            ventana=(0.08, 0.05, 0.45, 0.52))


def _sala_obs(lz, pl, t, sala, rapida=False):
    """Ambiente de la cúpula: estrellas por la ranura/ventana, foco rojo que late, polvo en la luz de los monitores."""
    zona = rect_P(pl, t, sala.get("ranura", sala.get("ventana")))
    estrellas(lz, t, mascara=lambda X, Y: zona[0] < X < zona[2] and zona[1] < Y < zona[3])
    X, Y, _ = pl.P(t, *sala["roja"])
    v = 0.5 + 0.5 * math.sin(t * (9.0 if rapida else 2.2))
    PF.brillo(lz, X, Y, 70 if rapida else 46, color=(1.0, 0.25, 0.12), inten=0.25 + (0.5 if rapida else 0.25) * v, t=t)
    polvo(lz, t, 0.14)


# 14 · «Una tarde cualquiera, en un observatorio de Chile…»
P14 = PF.Plano("observatorio_a", t0P - 0.15, p_astr, z0=1.10, z1=1.30, c0=(0.47, 0.52), c1=(0.42, 0.46), par=(30, 8))
snd(t0P, "viento", 0.35, dur=4.5)
snd(t0P + 0.3, "grillos", 0.3, dur=4.0)


@toma(t0P - 0.15, ("negro", 0.8))
def s14(lz, t):
    P14.fondo(lz, t)
    _, hY, _ = P14.P(t, 0.5, 0.40)
    estrellas(lz, t, mascara=lambda X, Y: Y < hY - 20)
    sx, sy, _ = P14.P(t, 0.62, 0.45)
    destello_sol(lz, sx, sy, 520, 0.16 + 0.03 * math.sin(t * 1.3))
    # la cúpula principal mira al atardecer, muy cerca del horizonte: haz teal que barre despacio
    cx, cy, _ = P14.P(t, 0.445, 0.375)
    PF.brillo(lz, cx, cy, 40, color=TEAL, inten=0.45, t=t)
    a = math.radians(-6 + 3 * math.sin(t * 0.5))
    L = 1100
    haz = [(cx, cy), (cx + L * math.cos(a - 0.05), cy + L * math.sin(a - 0.05)), (cx + L * math.cos(a + 0.05), cy + L * math.sin(a + 0.05))]
    trazo(lz, lambda m: poligono(m, haz), TEAL, 0.10, glow=0.5)
    aves(lz, t, [(t0P - 0.2, 7.0, 0.20, 0.16, 26, 1, 0.0), (t0P + 0.8, 7.5, 0.25, 0.22, 20, 1, 0.5)], tono=(0.10, 0.11, 0.18))
    PF.arena_viento(lz, t, fuerza=0.22, y0=0.72, y1=1.0, color=(0.55, 0.62, 0.76))
    texto(lz, "CHILE", W * 0.20, H * 0.14, 76, t, p_chile, None)


# 15 · «…una astrónoma revisa las imágenes del atardecer, muy cerca del horizonte.»
P15 = PF.Plano("sala_observatorio_b", p_astr - 0.35, p_hay, z0=1.10, z1=1.34, c0=(0.45, 0.55), c1=(0.38, 0.55), par=(28, 6))
snd(p_astr, "zumbido_servidores", 0.35, dur=5.5)
snd(p_revisa, "tecleo_rapido", 0.45)


@toma(p_astr - 0.35, ("desenfoque", 0.5))
def s15(lz, t):
    P15.fondo(lz, t)
    _sala_obs(lz, P15, t, SO_B)
    for k, r in enumerate(SO_B["mon"]):
        sem = 3 * k + (int((t - p_revisa) / 0.8) if t > p_revisa else 0)      # pasa de una imagen a otra
        cielo_pant(lz, rect_P(P15, t, r), sem=sem, n=40)
    X, Y, h = P15.en(t, 0.53, 0.885, 0.46)
    PF.actor(lz, "astronoma_hoja/00", X, Y, h, flip=True, tono=PANT, sy=PF.respira(t), rot=0.6 * math.sin(t * 9))


# 16 · «Hay un punto que ayer no estaba.» — la pantalla del medio crece: comparador AYER / HOY
P16 = PF.Plano("sala_observatorio_b", p_hay - 0.3, p_y, z0=1.70, z1=2.10, c0=(0.33, 0.47), c1=(0.316, 0.468), par=(24, 6))
PUNTO16 = (0.63, 0.50)                         # dónde está el punto nuevo dentro de la imagen
snd(p_hay - 0.2, "camara_zoom", 0.5)
snd(p_estaba, "pin", 0.6)


@toma(p_hay - 0.3, ("desenfoque", 0.45))
def s16(lz, t):
    lz[:] = fondo_quieto(P16, t, 2.0)
    _sala_obs(lz, P16, t, SO_B)
    u = e_inout(clamp01((t - (p_hay - 0.3)) / 0.7))
    R0 = rect_P(P16, t, SO_B["mon"][1])
    R = tuple(lerp(a, b, u) for a, b in zip(R0, (0.13 * W, 0.10 * H, 0.80 * W, 0.86 * H)))
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    ayer = t > p_ayer - 0.2 and int((t - p_ayer + 0.2) / 0.42) % 2 == 0
    cielo_pant(lz, R, sem=5, n=110, monte=True)
    def rejilla(m):
        for k in range(1, 6):
            cv2.line(m, _p(X0 + w * k / 6, Y0), _p(X0 + w * k / 6, Y1), 255, 1, cv2.LINE_AA, 4)
            cv2.line(m, _p(X0, Y0 + h * k / 6), _p(X1, Y0 + h * k / 6), 255, 1, cv2.LINE_AA, 4)
    trazo(lz, rejilla, TEAL, 0.12 * u, glow=0.0)
    if u > 0.6:
        texto(lz, "AYER" if ayer else "HOY", X0 + 0.04 * w, Y0 + 0.08 * h, 54, t, p_hay + 0.2, None,
              color=(0.6, 0.7, 0.85) if ayer else BLANCO, ancla=0.0)
        texto(lz, "CÁMARA 2 · 18:42", X1 - 0.03 * w, Y0 + 0.07 * h, 26, t, p_hay + 0.2, None, color=(0.6, 0.7, 0.85),
              fnt="mono", glow=0.0, ancla=1.0)
    px, py = X0 + PUNTO16[0] * w, Y0 + PUNTO16[1] * h
    if not ayer and u > 0.3:
        PF._blob(lz, px, py, 16, (1.0, 0.90, 0.85), 0.95, aditivo=True)
    reticula(lz, px, py, 46, t, p_estaba - 0.1)
    texto(lz, "NUEVO", px + 80, py - 70, 40, t, p_estaba + 0.1, None, color=ROJO, ancla=0.0)
    X, Y, hh = P16.en(t, 0.53, 0.885, 0.46)
    PF.actor(lz, "astronoma_hoja/00", X, Y, hh, flip=True, tono=(0.40, 0.50, 0.70), sy=PF.respira(t))


# 17 · «Y hay algo que la inquieta: casi no se mueve.» — se levanta, mano en la boca; en los monitores, el punto no avanza
P17 = PF.Plano("sala_observatorio_a", p_y - 0.3, p_las, z0=1.15, z1=1.36, c0=(0.55, 0.56), c1=(0.62, 0.56), par=(28, 6))
snd(p_inq, "suspiro", 0.5)
snd(p_mueve, "teremin", 0.35)


@toma(p_y - 0.3, ("latigo", 0.4))
def s17(lz, t):
    P17.fondo(lz, t)
    _sala_obs(lz, P17, t, SO_A)
    for k, r in enumerate(SO_A["mon"]):
        R = rect_P(P17, t, r)
        cielo_pant(lz, R, sem=11 + k, n=30)
        if k == 1:                                     # la pista del punto: cinco posiciones casi encimadas
            X0, Y0, X1, Y1 = R
            for j in range(5):
                PF._blob(lz, X0 + (X1 - X0) * (0.55 + 0.004 * j), Y0 + (Y1 - Y0) * 0.45, 7, ROJO, 0.9, aditivo=True)
            reticula(lz, X0 + (X1 - X0) * 0.56, Y0 + (Y1 - Y0) * 0.45, 22, t, p_casi)
    if t < p_inq:
        X, Y, h = P17.en(t, 0.64, 0.88, 0.46)
        PF.actor(lz, "astronoma_hoja/00", X, Y, h, tono=PANT, sy=PF.respira(t))
    else:
        quieto(lz, P17, t, "astronoma_hoja/01", 0.60, 0.93, 0.58, tono=PANT, t_in=p_inq)
    texto(lz, "CASI NO SE MUEVE", W * 0.27, H * 0.22, 66, t, p_casi, None, color=ROJO, glow=0.8)


# 18 · «Las que pasan de largo cruzan el cielo. La que viene directo hacia ti se queda quieta. Y solo crece.»
P18 = PF.Plano("observatorio_b", p_las - 0.3, p_mide, z0=1.02, z1=1.16, c0=(0.50, 0.49), c1=(0.52, 0.45), par=(26, 8))
QUIETA = (0.40, 0.22)
PASAN = [("asteroide_hoja/02", (-0.05, 0.10), (1.05, 0.30), p_pasan - 0.4, p_cielo + 0.3, 46),
         ("asteroide_hoja/03", (1.05, 0.06), (-0.05, 0.22), p_largo - 0.2, p_cielo + 0.9, 38)]
snd(p_pasan - 0.3, "whoosh", 0.5)
snd(p_largo, "whoosh", 0.45, tono=0.8)
snd(p_viene, "teremin", 0.45)
snd(p_crece, "crece", 0.7)
snd(p_crece + 0.1, "latido", 0.7)


@toma(p_las - 0.3, ("desenfoque", 0.5))
def s18(lz, t):
    P18.fondo(lz, t)
    _, hY, _ = P18.P(t, 0.5, 0.44)
    estrellas(lz, t, mascara=lambda X, Y: Y < hY)
    for pz, a, b, ta, tb, hpx in PASAN:                # las que pasan de largo: cruzan rápido con su trazo
        if t < ta:
            continue
        v = clamp01((t - ta) / (tb - ta))
        A = P18.P(t, *a)[:2]
        B = P18.P(t, *b)[:2]
        Xv, Yv = lerp(A[0], B[0], v), lerp(A[1], B[1], v)
        o = 1.0 - smooth(prog(t, tb + 0.6, tb + 1.6))
        D.linea_punteada(lz, [A, (Xv, Yv)], 1.0, color=TEAL, grosor=3, glow=0.8, op=0.7 * o)
        if v < 1:
            roca(lz, pz, Xv, Yv, hpx, t, giro=30, tono=FRIO)
    texto(lz, "PASAN DE LARGO", W * 0.27, H * 0.30, 52, t, p_largo, p_viene - 0.3, color=TEAL, fnt="sans")
    if t >= p_viene - 0.2:                             # la que viene hacia ti: no se mueve… y crece
        X, Y, _ = P18.P(t, *QUIETA)
        dom = P18.P(t, 0.66, 0.36)
        haz = [dom[:2], (X - 18, Y), (X + 18, Y)]
        trazo(lz, lambda m: poligono(m, haz), TEAL, 0.10 * smooth(prog(t, p_viene, p_viene + 0.6)), glow=0.4)
        g = e_inout(clamp01((t - p_crece) / 1.4)) if t >= p_crece else 0.0
        lat = 0.5 + 0.5 * math.sin(t * 6.5)
        PF._blob(lz, X, Y, 14 + 4 * lat + 90 * g, ROJO, 0.9, aditivo=True)
        if g > 0:
            roca(lz, "asteroide_hoja/00", X, Y, lerp(10, 170, g), t, giro=3, tono=(1.0, 0.82, 0.76))
        reticula(lz, X, Y, 60 + 90 * g, t, p_viene)
        texto(lz, "VIENE DIRECTO", X - 120 - 110 * g, Y, 46, t, p_directo, p_quieta - 0.3, color=ROJO, fnt="sans", ancla=1.0)
        texto(lz, "SE QUEDA QUIETA", X - 120 - 110 * g, Y, 46, t, p_quieta, None, color=ROJO, fnt="sans", ancla=1.0)
        if g > 0:
            pulso_rojo(lz, 0.3 * g * lat)
    polvo(lz, t, 0.2)


# 19 · «Mide unos 400 metros.» — ella al teléfono; en el monitor, la roca con su cota
P19 = PF.Plano("sala_observatorio_a", p_mide - 0.3, p_faltan, z0=1.85, z1=1.98, c0=(0.72, 0.48), c1=(0.73, 0.47), par=(26, 6))
snd(p_mide - 0.2, "alarma_leds", 0.5)
snd(p_400, "golpe_grave", 0.6)


@toma(p_mide - 0.3, ("latigo", 0.4))
def s19(lz, t):
    P19.fondo(lz, t)
    _sala_obs(lz, P19, t, SO_A, rapida=True)
    for k, r in enumerate(SO_A["mon"]):
        R = rect_P(P19, t, r)
        if k == 1:
            cielo_pant(lz, R, sem=12, n=30, horizonte=False, borde=ROJO)
            X0, Y0, X1, Y1 = R
            cx, cy, hh = (X0 + X1) / 2, (Y0 + Y1) / 2, (Y1 - Y0) * 0.62
            roca(lz, "asteroide_hoja/00", cx, cy, hh, t, giro=4, tono=(1.0, 0.85, 0.80))
            cota(lz, cx + hh * 0.62, cy - hh * 0.45, cy + hh * 0.45, t, p_400 - 0.2, "", color=ROJO)
        else:
            v = 0.6 + 0.4 * math.sin(t * 9 + k)
            caja(lz, R, (0.42 * v, 0.03, 0.02), 1.0, borde=ROJO)
            texto(lz, "ALERTA", (R[0] + R[2]) / 2, (R[1] + R[3]) / 2, max(14, int((R[3] - R[1]) * 0.22)), t, -1, None, color=(1.0, 0.8, 0.75), fnt="sans", glow=0.3)
    X0, Y0, X1, _ = rect_P(P19, t, SO_A["mon"][1])
    texto(lz, "~400 m", (X0 + X1) / 2, Y0 - 120, 120, t, p_400, None, color=ROJO, glow=0.9)
    X, Y, h = P19.en(t, 0.60, 0.97, 0.60)
    PF.actor(lz, "astronoma_hoja/02", X, Y, h, tono=(0.66, 0.74, 0.95), sy=PF.respira(t))
    pulso_rojo(lz, 0.15 * (0.5 + 0.5 * math.sin(t * 9)))


# 20 · «Faltan 20 horas.» — ya es de noche; la cúpula en alerta y la cuenta atrás roja
P20 = PF.Plano("observatorio_a", p_faltan - 0.3, t0N + 0.3, z0=1.75, z1=1.95, c0=(0.44, 0.40), c1=(0.43, 0.41), par=(30, 8),
               tono=(0.50, 0.56, 0.85))
snd(p_faltan, "caida", 0.45)
snd(p_20, "reloj_pared", 0.6, dur=3.0)


@toma(p_faltan - 0.3, ("negro", 0.5))
def s20(lz, t):
    P20.fondo(lz, t)
    _, hY, _ = P20.P(t, 0.5, 0.36)
    estrellas(lz, t, mascara=lambda X, Y: Y < hY)
    cx, cy, _ = P20.P(t, 0.445, 0.375)
    v = 0.5 + 0.5 * math.sin(t * 7)
    PF.brillo(lz, cx, cy, 120, color=ROJO, inten=0.35 + 0.35 * v, t=t)
    if t >= p_20:
        rest = 20 * 3600 - int(t - p_20)
        txt = f"{rest // 3600:02d}:{rest // 60 % 60:02d}:{rest % 60:02d}"
        texto(lz, txt, W * 0.5, H * 0.22, 190, t, p_20, None, color=ROJO, glow=0.9)
    texto(lz, "PARA EL IMPACTO", W * 0.5, H * 0.36, 46, t, p_horas + 0.3, None, color=(1.0, 0.75, 0.70), fnt="sans")
    polvo(lz, t, 0.2)
    pulso_rojo(lz, 0.25 * v)


# ------------------------------------------------------------------ numeros
SC_A = dict(pant=(0.14, 0.21, 0.94, 0.533), rojas=[(0.25, 0.09), (0.50, 0.09), (0.75, 0.09)])
SC_B = dict(pant=(0.3275, 0.233, 0.675, 0.433), rojas=[(0.22, 0.08), (0.50, 0.07), (0.78, 0.08)])
PROB = [(n_1, 1), (n_10, 10), (n_60, 60), (n_100, 100)]


def prob(t):
    p = 0.1
    for tk, v in PROB:
        if t >= tk:
            p = v
    return p


def _rojas(lz, pl, t, puntos, rapida=False):
    for k, (x, y) in enumerate(puntos):
        X, Y, _ = pl.P(t, x, y)
        v = 0.5 + 0.5 * math.sin(t * (8.0 if rapida else 3.0) + k * 2.1)
        PF.brillo(lz, X, Y, 90, color=(1.0, 0.22, 0.10), inten=0.25 + 0.45 * v, t=t, sem=k)


def orbita_pant(lz, R, t, p, op=1.0):
    """Diagrama en la pantalla grande: la Tierra, la ruta de la roca y su elipse de incertidumbre, que se encoge sobre la
    Tierra a medida que sube la probabilidad p (0..100)."""
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    tx, ty, rt = X0 + 0.74 * w, Y0 + 0.55 * h, 0.07 * h
    trazo(lz, lambda m: cv2.circle(m, _p(tx, ty), int(rt * 16), 255, -1, cv2.LINE_AA, 4), TEAL, op * 0.9, glow=0.8)
    a = (X0 + 0.48 * w, Y0 + 0.12 * h)
    D.linea_punteada(lz, [a, (tx, ty)], 1.0, color=ROJO, grosor=3, glow=0.7, op=op * 0.8)
    q = clamp01(math.log10(max(p, 0.1)) / 2 + 0.5)        # 0,1 % → 0 ; 100 % → 1
    ex, ey = lerp(a[0], tx, 0.55 + 0.45 * q), lerp(a[1], ty, 0.55 + 0.45 * q)
    rx = lerp(0.20 * w, rt * 0.8, q ** 1.4)
    lat = 0.5 + 0.5 * math.sin(t * 6.5)
    trazo(lz, lambda m: cv2.ellipse(m, _p(ex, ey), _p(rx, rx * 0.45), -28, 0, 360, 255, -1, cv2.LINE_AA, 4), ROJO,
          op * (0.16 + 0.10 * lat), glow=0.6)
    trazo(lz, lambda m: cv2.ellipse(m, _p(ex, ey), _p(rx, rx * 0.45), -28, 0, 360, 255, 2, cv2.LINE_AA, 4), ROJO, op * 0.9, glow=0.7)
    texto(lz, "TIERRA", tx, ty + rt + 30, max(18, int(h * 0.05)), t, -1, None, color=TEAL, fnt="sans", op=op)


# 21 · «La probabilidad de impacto sube cada hora.»
P21 = PF.Plano("sala_crisis_a", t0N - 0.25, n_1, z0=1.02, z1=1.16, c0=(0.50, 0.50), c1=(0.54, 0.46), par=(26, 6))
snd(n_prob, "teletipo", 0.35, dur=3.0)
snd(n_hora, "reloj_rapido", 0.45)


@toma(t0N - 0.25, ("desenfoque", 0.5))
def s21(lz, t):
    P21.fondo(lz, t)
    _rojas(lz, P21, t, SC_A["rojas"])
    R = rect_P(P21, t, SC_A["pant"])
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    caja(lz, (X0 + 6, Y0 + 6, X1 - 6, Y1 - 6), (0.03, 0.06, 0.13), 0.85)
    orbita_pant(lz, R, t, 0.1 + 0.9 * smooth(prog(t, n_sube, n_1)))
    texto(lz, "PROBABILIDAD DE IMPACTO", X0 + 0.05 * w, Y0 + 0.14 * h, int(h * 0.075), t, n_prob, None, color=TEAL, fnt="sans", ancla=0.0)
    # el reloj de las horas: una manecilla que da vueltas y un «+1 h» que se repite
    cx, cy, r = X0 + 0.14 * w, Y0 + 0.58 * h, 0.16 * h
    if t >= n_sube - 0.2:
        ang = (t - n_sube) * 4.0
        def reloj(m):
            cv2.circle(m, _p(cx, cy), int(r * 16), 255, 3, cv2.LINE_AA, 4)
            cv2.line(m, _p(cx, cy), _p(cx + r * 0.8 * math.sin(ang), cy - r * 0.8 * math.cos(ang)), 255, 3, cv2.LINE_AA, 4)
        trazo(lz, reloj, BLANCO, smooth(prog(t, n_sube - 0.2, n_sube + 0.2)), glow=0.5)
        texto(lz, "CADA HORA", cx + r + 24, cy, int(h * 0.07), t, n_hora, None, fnt="sans", ancla=0.0)
    quieto(lz, P21, t, "funcionarios_hoja/02", 0.27, 0.75, 0.21, tono=SALA, fase=0.3)
    quieto(lz, P21, t, "funcionarios_hoja/01", 0.63, 0.90, 0.34, tono=SALA, fase=1.1)
    quieto(lz, P21, t, "funcionarios_hoja/00", 0.87, 1.02, 0.46, tono=SALA, fase=2.0)


# 22 · «1 por ciento. 10. 60. 100 por ciento.» — la cifra gigante al ritmo del latido
P22 = PF.Plano("sala_crisis_a", n_1 - 0.3, n_nada, z0=1.95, z1=2.20, c0=(0.54, 0.37), c1=(0.54, 0.37), par=(20, 5))
for _tk, _v in PROB:
    snd(_tk - 0.05, "latido", 0.5 + 0.004 * _v)
snd(n_100 + 0.1, "alarma_leds", 0.7)


@toma(n_1 - 0.3, ("latigo", 0.4))
def s22(lz, t):
    P22.fondo(lz, t)
    _rojas(lz, P22, t, SC_A["rojas"], rapida=t >= n_100)
    R = rect_P(P22, t, SC_A["pant"])
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    p = prob(t)
    q = clamp01(math.log10(p) / 2)
    rojo = 0.5 + 0.5 * math.sin(t * 9) if t >= n_100 else 0.0
    caja(lz, (X0 + 6, Y0 + 6, X1 - 6, Y1 - 6), (lerp(0.03, 0.30, q * 0.6 + 0.4 * rojo), 0.05, lerp(0.13, 0.06, q)), 0.9)
    # la pantalla desborda el cuadro: cifra y diagrama se colocan en la parte visible
    vy0, vy1 = max(Y0, 0.04 * H), min(Y1, 0.92 * H)
    orbita_pant(lz, (0.56 * W, vy0 + 0.04 * H, 0.86 * W, vy1 - 0.04 * H), t, p, op=0.8)
    t_ult = max(tk for tk, _ in PROB if tk <= t) if t >= n_1 else n_1
    col = tuple(lerp(a, b, q) for a, b in zip(TEAL, ROJO))
    texto(lz, f"{p} %", 0.34 * W, (vy0 + vy1) / 2, 300, t, t_ult, None, color=col, glow=0.9)
    if t >= n_60:
        X, Y, hh = P22.fg(t, 0.09, 1.06, 0.74)
        PF.actor(lz, "funcionarios_hoja/03", X, Y, hh * (0.6 + 0.4 * PF.entra(t, n_60)), tono=(0.32, 0.30, 0.42), suelo=0)
    if t >= n_100:
        X, Y, hh = P22.fg(t, 0.93, 1.05, 0.82)
        PF.actor(lz, "funcionarios_hoja/04", X, Y, hh * (0.6 + 0.4 * PF.entra(t, n_100)), tono=(0.42, 0.28, 0.32), suelo=0,
                 sy=PF.respira(t, f=1.2, a=0.02))
        pulso_rojo(lz, 0.45 * rojo)


# 23 · «Y no hay nada que lanzar. La única vez que desviamos un asteroide, la nave tardó 10 meses en llegar.»
P23 = PF.Plano("sala_crisis_b", n_nada - 0.4, n_llegar, z0=1.15, z1=1.70, c0=(0.50, 0.44), c1=(0.50, 0.36), par=(26, 6))
snd(n_nada, "desenchufa", 0.5)
snd(n_nave, "whoosh", 0.4, tono=0.7)
snd(n_tardo, "motor_acelera", 0.35)
snd(n_llegar + 0.1, "error", 0.5)


@toma(n_nada - 0.4, ("negro", 0.5))
def s23(lz, t):
    P23.fondo(lz, t)
    _rojas(lz, P23, t, SC_B["rojas"])
    R = rect_P(P23, t, SC_B["pant"])
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    caja(lz, (X0 + 4, Y0 + 4, X1 - 4, Y1 - 4), (0.03, 0.06, 0.13), 0.9)
    if t < n_unica - 0.1:                             # el hangar vacío: un cohete que no existe
        o = 1.0 - smooth(prog(t, n_unica - 0.4, n_unica - 0.1))
        cx, cy = X0 + 0.30 * w, Y0 + 0.55 * h
        PF.actor(lz, "utileria/05", cx, cy, 0.62 * h, ancla=(0.5, 0.5), suelo=0, op=0.35 * o, tono=(0.8, 0.4, 0.35))
        def tache(m):
            cv2.circle(m, _p(cx, cy), int(0.36 * h * 16), 255, 6, cv2.LINE_AA, 4)
            cv2.line(m, _p(cx - 0.25 * h, cy + 0.25 * h), _p(cx + 0.25 * h, cy - 0.25 * h), 255, 6, cv2.LINE_AA, 4)
        trazo(lz, tache, ROJO, o * smooth(prog(t, n_nada, n_nada + 0.3)), glow=0.9)
        texto(lz, "NADA QUE LANZAR", X0 + 0.68 * w, cy, int(h * 0.11), t, n_nada + 0.1, None, color=ROJO, op=o)
    else:                                             # DART: 10 meses de viaje frente a nuestras 20 horas
        bx, bw = X0 + 0.08 * w, 0.84 * w
        y1, y2, bh = Y0 + 0.30 * h, Y0 + 0.70 * h, 0.12 * h
        texto(lz, "DART · 2022", bx, y1 - 0.13 * h, int(h * 0.08), t, n_unica, None, color=TEAL, fnt="sans", ancla=0.0)
        barra(lz, bx, y1, bw, bh, 1.0, TEAL, t, n_unica + 0.2)
        if t >= n_tardo - 0.3:
            v = e_inout(clamp01((t - (n_tardo - 0.3)) / (n_llegar - n_tardo + 0.5)))
            PF.actor(lz, "utileria/05", bx + bw * v, y1 + bh / 2, 0.30 * h, rot=45, ancla=(0.5, 0.5), suelo=0, tono=(0.95, 0.95, 1.0))
        texto(lz, "10 MESES", bx + bw, y1 + bh + 0.08 * h, int(h * 0.08), t, n_meses, None, color=TEAL, ancla=1.0)
        texto(lz, "NOSOTROS", bx, y2 - 0.13 * h, int(h * 0.08), t, n_llegar - 0.2, None, color=ROJO, fnt="sans", ancla=0.0)
        barra(lz, bx, y2, bw, bh, 0.012, ROJO, t, n_llegar - 0.2)
        texto(lz, "20 HORAS", bx + 0.12 * w, y2 + bh / 2, int(h * 0.08), t, n_llegar, None, color=ROJO, ancla=0.0)
    X, Y, hh = P23.fg(t, 0.14, 1.04, 0.56)
    PF.actor(lz, "funcionarios_hoja/05", X, Y, hh, tono=(0.30, 0.32, 0.45), suelo=0, sy=PF.respira(t, f=0.25))


# 24 · «Una roca de 400 metros a 20 kilómetros por segundo libera unos 5 mil megatones.»
P24 = PF.Plano("sala_crisis_b", n_una - 0.3, n_cien, z0=1.02, z1=1.10, c0=(0.50, 0.52), c1=(0.50, 0.50), par=(26, 6))
snd(n_400, "barrido_aire", 0.7)
snd(n_libera, "explosion", 0.9)
snd(n_mega, "trueno_noir", 0.8)


@toma(n_una - 0.3, ("latigo", 0.45))
def s24(lz, t):
    P24.fondo(lz, t)
    golpe = math.exp(-(t - n_libera) * 1.2) if t >= n_libera else 0.0
    _rojas(lz, P24, t, SC_B["rojas"], rapida=t >= n_libera)
    R = rect_P(P24, t, SC_B["pant"])
    X0, Y0, X1, Y1 = R
    w, h = X1 - X0, Y1 - Y0
    caja(lz, (X0 + 4, Y0 + 4, X1 - 4, Y1 - 4), (0.03 + 0.25 * golpe, 0.05, 0.12), 0.9)
    if t < n_libera:                                  # la roca cruza la pantalla con líneas de velocidad
        v = clamp01((t - n_una) / (n_libera - n_una))
        X, Y = lerp(X0 + 0.10 * w, X1 - 0.12 * w, v), lerp(Y0 + 0.30 * h, Y0 + 0.62 * h, v)
        def rayas(m):
            for k in range(9):
                yy = Y0 + h * (0.12 + 0.09 * k)
                xx = X0 + ((t * 2.2 + k * 0.37) % 1.0) * w
                cv2.line(m, _p(xx, yy), _p(max(X0, xx - 0.18 * w), yy), 255, 2, cv2.LINE_AA, 4)
        trazo(lz, rayas, BLANCO, 0.35, glow=0.3)
        PF.actor(lz, "asteroide_hoja/04", X, Y, 0.55 * h, rot=-20, ancla=(0.62, 0.62), suelo=0, sombra=False)
        texto(lz, "400 m", X0 + 0.05 * w, Y0 + 0.15 * h, int(h * 0.12), t, n_400, None, ancla=0.0)
        texto(lz, "20 km/s", X1 - 0.05 * w, Y0 + 0.15 * h, int(h * 0.12), t, n_20, None, color=NARANJA, ancla=1.0)
    else:
        n = int(5000 * smooth(prog(t, n_5 - 0.3, n_mega)))
        texto(lz, f"{n:,}".replace(",", " "), (X0 + X1) / 2, Y0 + 0.42 * h, int(h * 0.42), t, n_libera + 0.3, None, color=NARANJA, glow=1.0)
        texto(lz, "MEGATONES", (X0 + X1) / 2, Y0 + 0.82 * h, int(h * 0.15), t, n_mega, None, color=NARANJA)
    quieto(lz, P24, t, "funcionarios_hoja/03", 0.40, 0.83, 0.30, tono=SALA, rot=-6 * golpe)
    quieto(lz, P24, t, "funcionarios_hoja/02", 0.66, 0.75, 0.22, tono=SALA, fase=1.0)
    quieto(lz, P24, t, "funcionarios_hoja/00", 0.14, 0.98, 0.36, tono=SALA, fase=2.0, rot=-4 * golpe)
    lz += np.float32((1.0, 0.55, 0.25)) * (0.18 * golpe)
    sacudir(lz, 14 * golpe, t)


# 25 · «Cien veces la bomba más grande que hemos detonado jamás.» — la Tsar Bomba y 100 hongos que llenan el cielo
P25 = PF.Plano("columna_b", n_cien - 0.3, t0A + 0.5, z0=1.10, z1=1.04, c0=(0.47, 0.47), c1=(0.50, 0.49), par=(30, 8))
REJ25 = (0.60, 0.05, 0.96, 0.56)             # la rejilla de hongos, en el cielo oscuro del escenario (lejos de la nube)
_RH = np.random.default_rng(9)
HONGOS = sorted([(i % 10, i // 10, float(_RH.random())) for i in range(100)], key=lambda c: c[0] + c[1] * 0.6 + 2.5 * c[2])
snd(n_cien, "trueno_lejano", 0.7)
snd(n_bomba + 0.3, "crecer", 0.5)
snd(n_jamas + 0.4, "silencio_tono", 0.45)


@toma(n_cien - 0.3, ("negro", 0.5))
def s25(lz, t):
    P25.fondo(lz, t)
    bx, by, _ = P25.P(t, 0.335, 0.50)
    PF.brillo(lz, bx, by, 260, color=(1.0, 0.45, 0.15), inten=0.35, t=t)
    PF.chispas(lz, t, bx, by + 30, s=1.4, n=12)
    PF.arena_viento(lz, t, fuerza=0.25, y0=0.75, y1=1.0, color=(0.55, 0.40, 0.30))
    texto(lz, "LA BOMBA MÁS GRANDE · 1961", bx, H * 0.86, 40, t, n_bomba, None, color=(1.0, 0.75, 0.55), fnt="sans")
    texto(lz, "×100", W * 0.76, H * 0.80, 150, t, n_cien, None, color=NARANJA, glow=1.0)
    # la rejilla: 100 hongos que se encienden en oleada desde la bomba
    gx0, gy0, gx1, gy1 = rect_P(P25, t, REJ25)
    cw, chh = (gx1 - gx0) / 10, (gy1 - gy0) / 10
    ta, tb = n_bomba + 0.3, n_jamas + 0.4
    def fn(m):
        for k, (i, j, _) in enumerate(HONGOS):
            tk = lerp(ta, tb, k / 99)
            if t < tk:
                break
            u = PF.entra(t, tk, 0.3)
            hongo(m, gx0 + (i + 0.25 + 0.5 * (j % 2)) * cw, gy0 + (j + 0.90) * chh, 0.66 * chh * u)
    trazo(lz, fn, (1.0, 0.55, 0.20), 0.9, glow=0.55)
    polvo(lz, t, 0.2, color=(1.0, 0.7, 0.45))


# ================================================================== tramo 3 (20-oct-2026): alerta · destello · silencio · zona_cero ·
# peor · cierre. La persona normal (persona_hoja) a 90 km: alerta de madrugada, carreteras, el segundo sol, el sismo, los 4,5 min de
# silencio y la onda; luego la zona cero, los cometas y el cierre con el atardecer.
A_, DE, SI, ZC, PE, CI = "alerta", "destello", "silencio", "zona_cero", "peor", "cierre"
a_4, a_tel, a_sonar, a_nunca = T(A_, "4", 0), T(A_, "teléfono", 0), T(A_, "sonar", 0), T(A_, "nunca", 0)
a_alerta, a_alej, a_busq = T(A_, "alerta", 1), T(A_, "aléjese", 1), T(A_, "busque", 1)
a_vives, a_90, a_punto, a_lejos, a_sobr = T(A_, "vives", 2), T(A_, "90", 2), T(A_, "punto", 2), T(A_, "lejos", 2), T(A_, "sobrevivir", 2)
a_lo2, a_cerca, a_verlo = T(A_, "lo", 2, n=1), T(A_, "cerca", 2), T(A_, "verlo", 2)
a_carr, a_min, a_nadie, a_huir, a_ni, a_lejos3 = (T(A_, "carreteras", 3), T(A_, "minutos", 3), T(A_, "nadie", 3), T(A_, "huir", 3),
                                                  T(A_, "ni", 3), T(A_, "lejos", 3, n=1))
a_y, a_12, a_cielo, a_rompe = T(A_, "y", 4), T(A_, "12", 4), T(A_, "cielo", 4), T(A_, "rompe", 4)
t0D = _ESC[DE]["t0"]
d_roca, d_cruza, d_aparece, d_segundo, d_mas = (T(DE, "roca", 1), T(DE, "cruza", 1), T(DE, "aparece", 1), T(DE, "segundo", 1, n=1),
                                                T(DE, "más", 1))
d_calor, d_vidrio, d_afuera, d_ropa, d_humear = T(DE, "calor", 2), T(DE, "vidrio", 2), T(DE, "afuera", 2), T(DE, "ropa", 2), T(DE, "humear", 2)
d_15, d_sacude, d_7 = T(DE, "15", 3), T(DE, "sacude", 3), T(DE, "7", 3)
d_luego, d_nada = T(DE, "luego", 4), T(DE, "nada", 4)
si_este, si_peor = T(SI, "este", 0), T(SI, "peor", 0)
si_cielo, si_calma, si_gente = T(SI, "cielo", 1), T(SI, "calma", 1), T(SI, "gente", 1)
si_nadie, si_viene, si_veloc, si_sonido = T(SI, "nadie", 2), T(SI, "viene", 2), T(SI, "velocidad", 2), T(SI, "sonido", 2)
si_cuatro, si_silencio = T(SI, "cuatro", 3), T(SI, "silencio", 3)
si_y, si_llega, si_revienta, si_ventanas, si_arranca, si_techos, si_tumba, si_viento = (
    T(SI, "y", 4), T(SI, "llega", 4), T(SI, "revienta", 4), T(SI, "ventanas", 4), T(SI, "arranca", 4), T(SI, "techos", 4),
    T(SI, "tumba", 4), T(SI, "viento", 4))
t0Z = _ESC[ZC]["t0"]
z_donde, z_nada = T(ZC, "donde", 0), T(ZC, "nada", 0)
z_crater, z_7, z_30 = T(ZC, "cráter", 1), T(ZC, "7", 1), T(ZC, "30", 1)
z_columna, z_sube, z_aviones, z_rocas, z_incend = T(ZC, "columna", 2), T(ZC, "sube", 2), T(ZC, "aviones", 2), T(ZC, "rocas", 2), T(ZC, "incendios", 2)
z_cerca, z_millones, z_personas, z_menos = T(ZC, "cerca", 3), T(ZC, "millones", 3), T(ZC, "personas", 3), T(ZC, "menos", 3)
z_no, z_es2, z_tu = T(ZC, "no", 4), T(ZC, "es", 4, n=1), T(ZC, "tu", 4)
t0Q = _ESC[PE]["t0"]
q_esto, q_sabemos, q_ninguna = T(PE, "esto", 0), T(PE, "sabemos", 0), T(PE, "ninguna", 1)
q_cometas, q_confines, q_rapidos, q_grandes = T(PE, "cometas", 1), T(PE, "confines", 1), T(PE, "rápidos", 1), T(PE, "grandes", 1)
q_2013, q_rozando, q_vimos, q_menos = T(PE, "2013", 2), T(PE, "rozando", 2), T(PE, "vimos", 2), T(PE, "menos", 2)
q_contra, q_dos, q_alcanzan, q_nada = T(PE, "contra", 3), T(PE, "dos", 3), T(PE, "alcanzan", 3), T(PE, "nada", 3)
t0K = _ESC[CI]["t0"]
c_2027, c_telesc, c_mirar, c_sol, c_ciegos = T(CI, "2027", 0), T(CI, "telescopio", 0), T(CI, "mirar", 0), T(CI, "sol", 0), T(CI, "ciegos", 0)
c_hasta, c_vigil, c_esper, c_lado = T(CI, "hasta", 1), T(CI, "vigilando", 1), T(CI, "esperando", 1), T(CI, "lado", 1)
c_proxima, c_atard, c_de, c_vienen, c_vemos = T(CI, "próxima", 2), T(CI, "atardecer", 2), T(CI, "de", 2), T(CI, "vienen", 2), T(CI, "vemos", 2)

NOCHE = (0.52, 0.60, 0.86)        # 4 a. m.
DIA = (0.70, 0.78, 0.98)          # mediodía (los fondos de Flow son azulados)
CALOR = (1.0, 0.62, 0.32)         # la luz del segundo sol
POLVO_C = (0.70, 0.58, 0.46)      # polvo de la onda


# ------------------------------------------------------------------ utilidades del tramo 3
_RL = np.random.default_rng(41)
LUCES = _RL.random((120, 3))


def luces(lz, pl, t, zona, n=60, color=(1.0, 0.85, 0.55), op=0.5, r=5.0, sem=0):
    """Luces que titilan (ventanas, calles, calaveras de los coches) dentro de `zona` (x0, y0, x1, y1 del escenario)."""
    x0, y0, x1, y1 = zona
    for k, (a, b, f) in enumerate(LUCES[sem:sem + n]):
        v = 0.55 + 0.45 * math.sin(t * (1.5 + 3 * f) + k * 2.7)
        X, Y, _ = pl.P(t, lerp(x0, x1, a), lerp(y0, y1, b))
        PF._blob(lz, X, Y, r * (0.7 + 0.6 * f), color, op * v, aditivo=True)


def sirenas(lz, pl, t, pts, r=30, op=0.6):
    """Torretas de patrulla/ambulancia: rojo y azul alternados."""
    for k, (x, y) in enumerate(pts):
        X, Y, _ = pl.P(t, x, y)
        col = (1.0, 0.15, 0.12) if (t * 3.2 + k * 0.37) % 1.0 < 0.5 else (0.25, 0.45, 1.0)
        PF._blob(lz, X, Y, r, col, op * (0.6 + 0.4 * math.sin(t * 20 + k)), aditivo=True)


def ondas(lz, X, Y, t, t0, r0=20, r1=260, per=0.7, color=ROJO, op=0.7, g=3):
    """Anillos que salen de un teléfono que suena."""
    if t < t0:
        return
    def fn(m):
        for j in range(3):
            u = ((t - t0) / per + j / 3) % 1.0
            cv2.circle(m, _p(X, Y), int(lerp(r0, r1, u) * 16), int(255 * (1 - u)), g, cv2.LINE_AA, 4)
    trazo(lz, fn, color, op, glow=0.8)


_RK = np.random.default_rng(17)
GRIETAS = [(6.283 * a, 0.5 + 0.8 * b, int(4 + 5 * c)) for a, b, c in _RK.random((14, 3))]


def grietas(lz, X, Y, t, t0, largo=900, color=(1.0, 0.95, 0.85), op=1.0):
    """«El cielo se rompe»: grietas de luz quebradas y ramificadas que salen del punto."""
    if t < t0:
        return
    u = e_inout(clamp01((t - t0) / 0.6))
    def fn(m):
        r = np.random.default_rng(5)
        for ang, lv, nseg in GRIETAS:
            x, y, a = X, Y, ang
            L = largo * lv * u / nseg
            for s in range(nseg):
                a += (r.random() - 0.5) * 0.9
                x2, y2 = x + L * math.cos(a), y + L * math.sin(a)
                cv2.line(m, _p(x, y), _p(x2, y2), 255, max(1, 4 - s // 2), cv2.LINE_AA, 4)
                if r.random() < 0.35:
                    b = a + (r.random() - 0.5) * 1.8
                    cv2.line(m, _p(x2, y2), _p(x2 + 0.6 * L * math.cos(b), y2 + 0.6 * L * math.sin(b)), 255, 1, cv2.LINE_AA, 4)
                x, y = x2, y2
    trazo(lz, fn, color, op, glow=1.4, aditivo=True)


def frente(lz, X, ancho=200, op=0.6, color=(0.92, 0.88, 0.80)):
    """Frente de la onda expansiva que barre la pantalla de izquierda a derecha: borde de aire brillante en X y polvo detrás."""
    xx = np.arange(W, dtype=np.float32)
    d = (X - xx) / ancho
    k = (np.exp(-(d ** 2) * 3) * 0.9 + np.clip(d, 0, 1) * 0.55) * op
    lz[:] = lz * (1 - 0.6 * k[None, :, None]) + np.float32(color) * (0.6 * k[None, :, None])


_RA = np.random.default_rng(43)
CENIZA = [(a, b, 1.0 + 2.4 * c, d) for a, b, c, d in _RA.random((80, 4))]


def ceniza(lz, t, op=0.45, color=(0.62, 0.56, 0.52), viento=0.0):
    """Ceniza que cae despacio y deriva."""
    for x, y, r, f in CENIZA:
        Y = ((y * (H + 60) + t * (18 + 26 * f)) % (H + 60)) - 30
        X = ((x * (W + 100) + t * (6 + viento * 600) * (0.5 + f) + 30 * math.sin(t * 0.7 + f * 9)) % (W + 100)) - 50
        PF._blob(lz, X, Y, r * 2.4, color, op * (0.4 + 0.6 * f))


def vuela(lz, pieza, t, ta, dur, a, b, h, giro, arco=0.0, tono=None, op=1.0):
    """Pieza arrastrada por el viento de a a b (pantalla, relativos) dando vueltas."""
    u = (t - ta) / dur
    if not 0 <= u <= 1:
        return
    X = lerp(a[0], b[0], u) * W
    Y = lerp(a[1], b[1], u) * H - arco * H * math.sin(math.pi * u)
    PF.actor(lz, pieza, X, Y, h, rot=giro * (t - ta), ancla=(0.5, 0.5), suelo=0, tono=tono, op=op)


def sismograma(lz, t, Y, amp, color=ROJO, op=0.9):
    """Traza de sismógrafo que corre de derecha a izquierda (lo de la derecha es lo más reciente); amp(t) en px."""
    n = 240
    pts = []
    for k in range(n):
        tt = t - (1 - k / (n - 1)) * 2.4
        a = amp(tt)
        pts.append(_p(k / (n - 1) * W, Y + a * (math.sin(tt * 47) * 0.6 + math.sin(tt * 83 + 1.3) * 0.4)))
    trazo(lz, lambda m: cv2.polylines(m, [np.array(pts, np.int32)], False, 255, 3, cv2.LINE_AA, 4), color, op, glow=0.8)


def avion(m, cx, cy, s):
    """Silueta de avión de pasajeros (máscara), s px de largo, rumbo a la derecha."""
    P = lambda x, y: (cx + x * s, cy + y * s)
    poligono(m, [P(-0.5, -0.03), P(0.42, -0.04), P(0.5, 0.0), P(0.42, 0.04), P(-0.5, 0.03)])
    poligono(m, [P(0.05, 0.0), P(-0.12, 0.30), P(-0.20, 0.30), P(-0.08, 0.0)])
    poligono(m, [P(0.02, 0.0), P(-0.10, -0.18), P(-0.16, -0.18), P(-0.08, 0.0)])
    poligono(m, [P(-0.40, 0.0), P(-0.50, -0.16), P(-0.55, -0.16), P(-0.50, 0.0)])


def cometa(lz, X, Y, h, ang, tono=(0.95, 1.0, 1.05), op=1.0):
    """Cometa de Flow (asteroide_hoja/05: cabeza abajo-izq., cola arriba-dcha. = rumbo 151°) girado para avanzar con rumbo `ang`
    (grados de pantalla: 0 = derecha, 90 = abajo); si va hacia la derecha se voltea (rumbo 29°)."""
    flip = math.cos(math.radians(ang)) > 0
    base = 29.0 if flip else 151.0
    PF.brillo(lz, X, Y, h * 1.1, color=(0.55, 0.95, 1.0), inten=0.35 * op, t=X)
    PF.actor(lz, "asteroide_hoja/05", X, Y, h, rot=ang - base, flip=flip, ancla=(0.25, 0.72), suelo=0, sombra=False, tono=tono, op=op)


def cola(lz, X, Y, ang, largo, ancho, color=(0.70, 0.95, 1.0), op=0.5):
    """Cola de luz (triángulo con halo aditivo) detrás de una cabeza que avanza con rumbo `ang`."""
    a = math.radians(ang + 180)
    n = (-math.sin(a), math.cos(a))
    pts = [(X + n[0] * ancho, Y + n[1] * ancho), (X - n[0] * ancho, Y - n[1] * ancho),
           (X + largo * math.cos(a), Y + largo * math.sin(a))]
    trazo(lz, lambda m: poligono(m, pts), color, op, glow=1.3, aditivo=True)


def calima(lz, t, k):
    """Aire que tiembla por el calor (desplazamiento senoidal horizontal)."""
    if k < 0.05:
        return
    X, Y = PF._grid()
    dx = k * 1.1 * np.sin(Y * 0.11 + t * 9.0)
    lz[:] = cv2.remap(lz, X + dx, Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def lejos_pant(pl, t, d0=0.16, d1=0.30):
    """Máscara de pantalla (1 = lejos) a partir de la profundidad del escenario: para dibujar algo DETRÁS de las casas."""
    rgb, hs, ws, s0, cx, cy, ph = pl._st(t)
    d = PF._fondo_depth(pl.f, hs, ws)
    if d is None:
        return np.ones((H, W), np.float32)
    X, Y = PF._grid()
    dd = cv2.remap(d, cx + (X - W / 2) / s0, cy + (Y - H / 2) / s0, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return 1.0 - np.clip((dd - d0) / (d1 - d0), 0, 1)


def quemar(lz, k, color=(1.0, 0.92, 0.80), rampa=None):
    """Sobreexposición suave: lo claro se quema hacia blanco (sin recuadros: un rectángulo encima parece «página web»)."""
    g = np.clip(lz.mean(axis=2, keepdims=True) * 1.6, 0, 1) ** 1.5
    if rampa is not None:
        g = g * rampa
    lz += g * np.float32(color) * k


def sombra_txt(lz, X, Y, w, h, op=0.5):
    """Penumbra difusa detrás de un texto que cae sobre humo o cielo claro (contraste sin caja)."""
    m = np.zeros((H, W), np.uint8)
    cv2.ellipse(m, _p(X, Y), _p(w / 2, h / 2), 0, 0, 360, 255, -1, cv2.LINE_AA, 4)
    a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), h * 0.35)
    lz *= (1 - op * a)[..., None]


def _fuegos(lz, pl, t, fuegos, humo=True):
    for k, (x, y, s) in enumerate(fuegos):
        X, Y, _ = pl.P(t, x, y)
        PF.brillo(lz, X, Y, 70 * s, color=(1.0, 0.45, 0.15), inten=0.45, t=t, sem=k)
        PF.chispas(lz, t, X, Y, s=s, n=6, sem=k)
        if humo:
            PF.humo(lz, t, X, Y - 10, s=s, n=6, color=(0.20, 0.16, 0.15), op=0.30, sem=k)


def _fila(lz, pl, t, fila, via, avance, alto0, alto1, tono):
    """Fila de coches atascados en un carril en perspectiva (via = extremo cercano y lejano del escenario); avanzan a tirones.
    Los coches de Flow miran a la derecha y la fila sube hacia la ciudad (derecha): se dibujan de lejos a cerca."""
    A = pl.P(t, *via[0])
    B = pl.P(t, *via[1])
    ang = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    for pz, s in sorted(fila, key=lambda q: -q[1]):
        u = s + avance
        if not 0 <= u <= 1.02:
            continue
        X, Y = lerp(A[0], B[0], u), lerp(A[1], B[1], u)
        h = pl.alto_px(t, lerp(alto0, alto1, u))
        PF.actor(lz, pz, X, Y + 1.5 * math.sin(t * 9 + s * 20), h, rot=ang, tono=tono, suelo=0.35)
        PF.brillo(lz, X - 0.95 * h, Y - 0.40 * h, 0.35 * h, color=(1.0, 0.15, 0.08), inten=0.45, t=t, sem=int(s * 50))


# ------------------------------------------------------------------ alerta
# 26 · «Son las 4 de la mañana cuando tu teléfono empieza a sonar como nunca lo habías oído.»
P26 = PF.Plano("recamara_a", t0A, a_alerta, z0=1.16, z1=1.32, c0=(0.40, 0.52), c1=(0.34, 0.55), par=(28, 6))
TEL26 = (0.135, 0.478)                # mesita de noche (junto al reloj rojo)
snd(t0A + 0.2, "zumbido_lampara", 0.25, dur=6.0)
snd(a_4, "reloj_pared", 0.35, dur=2.0)
snd(a_tel - 0.1, "alarma_leds", 0.9, dur=3.0)
snd(a_sonar + 0.6, "alarma_leds", 0.8, dur=2.4)
snd(a_nunca, "susto_cuerdas", 0.45)


@toma(t0A, ("negro", 0.6))
def s26(lz, t):
    P26.fondo(lz, t)
    zona = rect_P(P26, t, (0.44, 0.08, 0.76, 0.36))
    estrellas(lz, t, mascara=lambda X, Y: zona[0] < X < zona[2] and zona[1] < Y < zona[3])
    luces(lz, P26, t, (0.46, 0.18, 0.74, 0.35), n=30, r=3, op=0.35, color=(0.55, 0.95, 0.90))
    X, Y, _ = P26.P(t, *TEL26)
    suena = t >= a_tel
    v = 0.5 + 0.5 * math.sin(t * 18) if suena else 0.0
    PF.brillo(lz, X, Y, 60 + 120 * v, color=(1.0, 0.22, 0.10), inten=0.35 + 0.4 * v, t=t)
    t_coge = a_nunca - 0.2                            # lo coge: el teléfono deja la mesita y aparece en su mano
    if t < t_coge:
        jit = 3.5 * math.sin(t * 70) if suena else 0.0
        PF.actor(lz, "utileria/00", X + jit, Y + 4, P26.alto_px(t, 0.085), rot=-10 + 2 * jit, suelo=0.2, tono=(0.85, 0.82, 0.92))
        ondas(lz, X, Y - 30, t, a_tel, r1=240)
    if suena:
        lz += np.float32(ROJO) * (0.05 * v)             # la luz roja de la alerta llena el cuarto
    if t >= t_coge:
        quieto(lz, P26, t, "persona_hoja/00", 0.57, 0.95, 0.62, tono=NOCHE, t_in=t_coge)
        Xp, Yp, h = P26.en(t, 0.57, 0.95, 0.62)
        PF.brillo(lz, Xp + 0.12 * h, Yp - 0.72 * h, 120 + 40 * v, color=(1.0, 0.25, 0.12), inten=0.30 + 0.3 * v, t=t)
        ondas(lz, Xp + 0.12 * h, Yp - 0.72 * h, t, t_coge, r0=40, r1=220, op=0.5)
    texto(lz, "4:00 a. m.", W * 0.21, H * 0.15, 96, t, a_4, None, color=(1.0, 0.45, 0.35), glow=0.6)
    polvo(lz, t, 0.12)


# 27 · «Alerta de impacto. Aléjese de las ventanas. Busque refugio.» — el teléfono, enorme, y el mensaje
P27 = PF.Plano("recamara_b", a_alerta - 0.3, a_vives, z0=1.45, z1=1.58, c0=(0.50, 0.42), c1=(0.52, 0.44), par=(20, 5))
snd(a_alerta - 0.25, "alarma_leds", 1.0, dur=1.8)
snd(a_alej, "pin", 0.5)
snd(a_busq, "pin", 0.5, tono=0.8)
snd(a_busq + 0.5, "grave_inquietante", 0.6)


@toma(a_alerta - 0.3, ("latigo", 0.35))
def s27(lz, t):
    lz[:] = fondo_quieto(P27, t, 3.0) * 0.75
    v = 0.5 + 0.5 * math.sin(t * 18)
    lz += np.float32(ROJO) * (0.07 * v)
    jit = 4 * math.sin(t * 66) * (0.6 + 0.4 * v)
    X, Y = W * 0.26 + jit, H * 0.53
    u = PF.entra(t, a_alerta - 0.3, 0.35)
    PF.brillo(lz, X, Y - 40, 380, color=(1.0, 0.2, 0.1), inten=0.30 + 0.25 * v, t=t)
    ondas(lz, X, Y, t, a_alerta - 0.3, r0=280, r1=700, per=0.9, op=0.45)
    PF.actor(lz, "utileria/00", X, Y, H * 0.80 * (0.7 + 0.3 * u), rot=-6 + 0.8 * jit, ancla=(0.5, 0.5), suelo=0, tono=(0.95, 0.92, 1.0))
    x0 = W * 0.47
    texto(lz, "ALERTA DE IMPACTO", x0, H * 0.30, 72, t, a_alerta, None, color=ROJO, glow=0.9, ancla=0.0)
    if t >= a_alerta:
        w = W * 0.40 * e_inout(clamp01((t - a_alerta) / 0.6))
        trazo(lz, lambda m: cv2.rectangle(m, _p(x0, H * 0.37), _p(x0 + w, H * 0.37 + 6), 255, -1, cv2.LINE_AA, 4), ROJO, 0.9, glow=0.8)
    texto(lz, "Aléjese de las ventanas", x0, H * 0.46, 54, t, a_alej, None, fnt="sans", ancla=0.0)
    texto(lz, "Busque refugio", x0, H * 0.57, 54, t, a_busq, None, fnt="sans", ancla=0.0)
    pulso_rojo(lz, 0.35 * v)


# 28 · «Vives a 90 kilómetros del punto. Lo bastante lejos para sobrevivir.» — la ciudad de noche; el anillo de 90 km pasa por ti
P28 = PF.Plano("ciudad_noche_a", a_vives - 0.3, a_lo2, z0=1.03, z1=1.16, c0=(0.50, 0.52), c1=(0.57, 0.48), par=(30, 8))
PUNTO28 = (0.713, 0.395)              # el resplandor rojo del horizonte
snd(a_vives - 0.2, "viento", 0.35, dur=5.0)
snd(a_90, "datos", 0.4, dur=1.2)
snd(a_punto, "pin", 0.6)
snd(a_sobr, "golpe_grave", 0.5)


@toma(a_vives - 0.3, ("desenfoque", 0.5))
def s28(lz, t):
    P28.fondo(lz, t)
    _, hY, _ = P28.P(t, 0.5, 0.30)
    estrellas(lz, t, mascara=lambda X, Y: Y < hY)
    luces(lz, P28, t, (0.18, 0.42, 0.85, 0.72), n=80, r=4, op=0.45, color=(0.55, 0.95, 0.90))
    sirenas(lz, P28, t, [(0.30, 0.66), (0.55, 0.60), (0.47, 0.71), (0.66, 0.64)], r=22, op=0.55)
    px, py, _ = P28.P(t, *PUNTO28)
    lat = 0.5 + 0.5 * math.sin(t * 6.5)
    PF.brillo(lz, px, py, 50 + 30 * lat, color=ROJO, inten=0.6, t=t)
    reticula(lz, px, py, 40, t, a_punto - 0.1)
    vx, vy = W * 0.42, H * 0.95                       # tú (abajo, en la azotea)
    if t >= a_90 - 0.2:
        u = e_inout(clamp01((t - (a_90 - 0.2)) / 1.2))
        ry = vy - py
        trazo(lz, lambda m: elipse_punteada(m, px, py, ry * 3.2, ry, u=u, a0=90, paso=4, g=3), ROJO, 0.85, glow=0.9)
        D.linea_punteada(lz, [(vx, vy), (px, py)], u, color=BLANCO, grosor=3, glow=0.6, op=0.8)
        texto(lz, "90 km", lerp(vx, px, 0.45) + 40, lerp(vy, py, 0.45), 64, t, a_90 + 0.3, None, ancla=0.0)
        PF._blob(lz, vx, vy, 18, TEAL, 0.9, aditivo=True)
        texto(lz, "TÚ", vx, vy - 50, 44, t, a_90 + 0.5, None, color=TEAL)
    texto(lz, "LO BASTANTE LEJOS", W * 0.27, H * 0.12, 56, t, a_lejos, None, color=TEAL)
    texto(lz, "PARA SOBREVIVIR", W * 0.27, H * 0.20, 44, t, a_sobr, None, color=TEAL, fnt="sans")
    polvo(lz, t, 0.12)


# 29 · «Lo bastante cerca para verlo todo.» — tú en la azotea, frente al resplandor
P29 = PF.Plano("ciudad_noche_b", a_lo2 - 0.2, a_carr, z0=1.22, z1=1.36, c0=(0.40, 0.58), c1=(0.37, 0.56), par=(30, 8))
GLOW29 = (0.352, 0.39)
snd(a_cerca, "sombra_crece", 0.6)
snd(a_verlo, "latido", 0.6)


@toma(a_lo2 - 0.2, ("latigo", 0.4))
def s29(lz, t):
    P29.fondo(lz, t)
    _, hY, _ = P29.P(t, 0.5, 0.30)
    estrellas(lz, t, mascara=lambda X, Y: Y < hY)
    luces(lz, P29, t, (0.10, 0.44, 0.95, 0.66), n=70, r=4, op=0.4, color=(0.55, 0.95, 0.90), sem=20)
    sirenas(lz, P29, t, [(0.62, 0.60), (0.80, 0.57)], r=20, op=0.5)
    gx, gy, _ = P29.P(t, *GLOW29)
    lat = 0.5 + 0.5 * math.sin(t * 6.5)
    PF.humo(lz, t, gx, gy - 10, s=1.3, n=7, color=(0.30, 0.20, 0.20), op=0.35)
    PF.brillo(lz, gx, gy, 90 + 40 * lat, color=(1.0, 0.35, 0.12), inten=0.55, t=t)
    quieto(lz, P29, t, "persona_hoja/01", 0.47, 0.90, 0.36, tono=NOCHE, fase=0.4)
    texto(lz, "LO BASTANTE CERCA", W * 0.70, H * 0.13, 56, t, a_cerca, None, color=ROJO, glow=0.8)
    texto(lz, "PARA VERLO TODO", W * 0.70, H * 0.21, 44, t, a_verlo, None, color=ROJO, fnt="sans")


# 30 · «Las carreteras se llenan en minutos. Nadie sabe hacia dónde huir.»
P30 = PF.Plano("autopista_b", a_carr - 0.3, a_ni, z0=1.10, z1=1.22, c0=(0.42, 0.62), c1=(0.46, 0.60), par=(30, 8))
VIA30 = ((-0.04, 0.99), (0.43, 0.725))          # el carril vacío de abajo a la izquierda, hasta el paso a desnivel
FILA30 = [("vehiculos/00", 0.00), ("vehiculos/04", 0.14), ("vehiculos/02", 0.29), ("vehiculos/08", 0.50), ("vehiculos/05", 0.62),
          ("vehiculos/09", 0.74), ("vehiculos/03", 0.86)]
snd(a_carr - 0.2, "autopista", 0.5, dur=5.0)
snd(a_min, "bocinazo", 0.5)
snd(a_nadie + 0.3, "bocinazo", 0.35, tono=0.8)
snd(a_huir - 0.2, "pasos", 0.6, dur=2.0)


@toma(a_carr - 0.3, ("desenfoque", 0.45))
def s30(lz, t):
    P30.fondo(lz, t)
    luces(lz, P30, t, (0.52, 0.52, 0.76, 0.76), n=60, r=4, op=0.5, color=(1.0, 0.22, 0.10), sem=10)
    luces(lz, P30, t, (0.80, 0.78, 1.0, 0.95), n=30, r=5, op=0.5, color=(1.0, 0.22, 0.10), sem=70)
    sirenas(lz, P30, t, [(0.595, 0.59), (0.635, 0.59), (0.935, 0.745)], r=20)
    dt = t - (a_carr - 0.3)
    _fila(lz, P30, t, FILA30, VIA30, 0.03 * dt - 0.006 * math.sin(2.2 * dt), 0.13, 0.045, (0.75, 0.80, 0.98))
    corre(lz, P30, t, "persona_corre", a_nadie - 0.2, a_nadie + 2.4, 0.74, 0.22, 0.995, 0.985, 0.18, tono=(0.75, 0.80, 0.98))
    corre(lz, P30, t, "mujer_corre", a_nadie + 0.3, a_nadie + 3.1, 0.80, 0.30, 0.99, 0.985, 0.16, tono=(0.75, 0.80, 0.98))
    texto(lz, "EN MINUTOS", W * 0.24, H * 0.12, 70, t, a_min, None)
    texto(lz, "¿HACIA DÓNDE?", W * 0.24, H * 0.21, 56, t, a_huir - 0.3, None, color=ROJO, glow=0.8)
    polvo(lz, t, 0.12)


# 31 · «Ni qué tan lejos es lejos.» — anillos de distancia que se abren desde el punto, cada uno con su duda
P31 = PF.Plano("autopista_a", a_ni - 0.3, a_y, z0=1.12, z1=1.02, c0=(0.55, 0.50), c1=(0.52, 0.50), par=(30, 8))
PUNTO31 = (0.70, 0.34)
ANILLOS31 = [("¿30 km?", 0.0), ("¿60 km?", 0.45), ("¿120 km?", 0.9), ("¿240 km?", 1.4)]
snd(a_ni, "teremin", 0.4)
snd(a_lejos3, "grave_inquietante", 0.5)


@toma(a_ni - 0.3, ("desenfoque", 0.4))
def s31(lz, t):
    P31.fondo(lz, t)
    luces(lz, P31, t, (0.28, 0.52, 0.48, 0.74), n=50, r=4, op=0.5, color=(1.0, 0.22, 0.10), sem=5)
    luces(lz, P31, t, (0.60, 0.55, 0.92, 0.80), n=50, r=4, op=0.5, color=(1.0, 0.22, 0.10), sem=60)
    sirenas(lz, P31, t, [(0.29, 0.555), (0.745, 0.555)], r=20)
    px, py, _ = P31.P(t, *PUNTO31)
    PF.brillo(lz, px, py, 70, color=ROJO, inten=0.55, t=t)
    for k, (txt, dtk) in enumerate(ANILLOS31):
        tk = a_ni + dtk
        if t < tk:
            continue
        rx = (150 + 230 * k) * e_inout(clamp01((t - tk) / 0.6))
        col = ROJO if k == 3 else BLANCO
        trazo(lz, lambda m, rx=rx: elipse(m, px, py, rx, rx * 0.22, g=3), col, 0.8 - 0.1 * k, glow=0.7)
        texto(lz, txt, px - rx * 0.80, py + rx * 0.22 * 0.60 + 26, 34, t, tk + 0.3, None, color=col, fnt="sans")
    texto(lz, "¿QUÉ TAN LEJOS ES LEJOS?", W * 0.40, H * 0.12, 62, t, a_ni, None, color=ROJO, glow=0.8)


# 32 · «Y a las 12 del día, el cielo se rompe.» — el punto rojo del cielo crece y la luz raja el vidrio
P32 = PF.Plano("sala_mediodia_a", a_y - 0.3, t0D + 0.5, z0=1.04, z1=1.28, c0=(0.55, 0.52), c1=(0.66, 0.46), par=(30, 8))
PUNTO32 = (0.76, 0.355)
snd(a_y, "pajaros_ciudad", 0.3, dur=3.0)
snd(a_12, "reloj_pared", 0.4, dur=1.4)
snd(a_cielo, "sombra_crece", 0.8)
snd(a_rompe, "relampago_corto", 1.0)
snd(a_rompe + 0.05, "crujido", 0.8)


@toma(a_y - 0.3, ("negro", 0.6))
def s32(lz, t):
    P32.fondo(lz, t)
    px, py, _ = P32.P(t, *PUNTO32)
    g = smooth(prog(t, a_cielo - 0.4, a_rompe + 0.2))
    lat = 0.5 + 0.5 * math.sin(t * 6.5)
    PF.brillo(lz, px, py, 40 + 160 * g + 10 * lat, color=(1.0, lerp(0.35, 0.85, g), lerp(0.15, 0.6, g)), inten=0.5 + 0.5 * g, t=t)
    aves(lz, t, [(a_y - 0.3, 4.5, 0.20, 0.14, 22, -1, 0.0), (a_y + 0.4, 4.0, 0.26, 0.18, 18, -1, 0.6)], tono=(0.15, 0.17, 0.25))
    grietas(lz, px, py, t, a_rompe, largo=1100)
    if t < a_rompe:
        X, Y, h = P32.en(t, 0.46, 0.97, 0.62)
        PF.actor(lz, "persona_hoja/01", X, Y, h, tono=DIA, sy=PF.respira(t))
    else:
        quieto(lz, P32, t, "persona_hoja/03", 0.46, 0.97, 0.62, tono=DIA, t_in=a_rompe)
        k = smooth(prog(t, a_rompe, t0D + 0.4))
        lz += np.float32((1.0, 0.95, 0.88)) * (0.50 * k + 0.3 * math.exp(-(t - a_rompe) * 4))
        sacudir(lz, 6 * math.exp(-(t - a_rompe) * 2), t)
    texto(lz, "12:00", W * 0.18, H * 0.15, 110, t, a_12, a_rompe, glow=0.5)


# ------------------------------------------------------------------ destello
# 33 · «Primero no hay ruido.» — la sala quemada de luz blanca, a contraluz, en silencio
P33 = PF.Plano("sala_mediodia_b", t0D, d_roca, z0=1.30, z1=1.42, c0=(0.70, 0.42), c1=(0.73, 0.40), par=(24, 6))
snd(t0D + 0.1, "silencio_tono", 0.5, dur=2.4)


@toma(t0D, ("destello", 0.5))
def s33(lz, t):
    P33.fondo(lz, t)
    quemar(lz, 1.5, rampa=_luz_derecha())
    lz += np.float32((1.0, 0.92, 0.82)) * 0.12
    X, Y, h = P33.en(t, 0.60, 0.80, 0.46)
    PF.actor(lz, "persona_hoja/03", X, Y, h, tono=(0.18, 0.16, 0.20), sy=PF.respira(t, f=0.2))
    polvo(lz, t * 0.4, 0.35, color=(1.0, 0.9, 0.7))


# 34 · «La roca cruza la atmósfera en unos segundos, y aparece un segundo sol, más brillante que el de verdad.»
# El orbe del cielo de calle_mediodia_b ES la roca, que viene casi de frente: se enciende, crece y estalla en un segundo sol.
P34 = PF.Plano("calle_mediodia_b", d_roca - 0.3, d_calor, z0=1.08, z1=1.20, c0=(0.50, 0.45), c1=(0.53, 0.42), par=(28, 6))
ORBE34 = (0.50, 0.155)
SOL34 = (0.14, 0.16)
snd(d_cruza, "subida", 0.6)
snd(d_cruza + 0.3, "teremin", 0.4)
snd(d_aparece, "silencio_tono", 0.6, dur=3.0)
snd(d_mas, "crecer", 0.4)


@toma(d_roca - 0.3, ("desenfoque", 0.4))
def s34(lz, t):
    P34.fondo(lz, t)
    ox, oy, _ = P34.P(t, *ORBE34)
    g = smooth(prog(t, d_cruza - 0.2, d_aparece))
    k = smooth(prog(t, d_aparece, d_mas + 0.6))
    lz *= 1.0 + 0.9 * k                                # el día entero se enciende
    lz += np.float32(CALOR) * (0.22 * k)
    # el Sol de verdad, pequeño, para comparar
    sx, sy, _ = P34.P(t, *SOL34)
    trazo(lz, lambda m: cv2.circle(m, _p(sx, sy), int(26 * 16), 255, -1, cv2.LINE_AA, 4), (1.0, 0.92, 0.65), 0.95, glow=1.0, aditivo=True)
    texto(lz, "SOL", sx, sy + 62, 40, t, d_segundo - 0.4, None, color=(1.0, 0.85, 0.55), fnt="sans")
    if t < d_aparece:                                  # la entrada: plasma alrededor de la roca, cada vez más grande
        PF.brillo(lz, ox, oy, lerp(50, 200, g), color=(1.0, 0.55, 0.25), inten=0.4 + 0.5 * g, t=t)
        if g > 0:
            cola(lz, ox, oy, 62, lerp(80, 520, g), lerp(14, 60, g), color=(1.0, 0.62, 0.30), op=0.55 * g)
            PF.actor(lz, "asteroide_hoja/04", ox, oy, lerp(70, 210, g), rot=62 - 45, ancla=(0.62, 0.62), suelo=0, sombra=False)
            PF.chispas(lz, t, ox, oy, s=1.0 + 1.5 * g, n=12)
    else:                                              # el segundo sol: disco blanco que crece y lo quema todo
        R = lerp(60, 0.20 * H, smooth(prog(t, d_aparece, d_aparece + 1.2)))
        trazo(lz, lambda m: cv2.circle(m, _p(ox, oy), int(R * 16), 255, -1, cv2.LINE_AA, 4), (1.0, 0.98, 0.92), 1.0, glow=2.0, aditivo=True)
        PF.brillo(lz, ox, oy, 200, color=(1.0, 0.95, 0.85), inten=0.9, t=t)
        texto(lz, "SEGUNDO SOL", ox, oy + R + 70, 60, t, d_segundo, None, color=ROJO, glow=0.6)
        texto(lz, "MÁS BRILLANTE", ox, oy + R + 140, 44, t, d_mas, None, color=ROJO, fnt="sans", glow=0.4)


# 35 · «El calor te llega a la piel a través del vidrio.» — contra la pared, lejos del ventanal
P35 = PF.Plano("sala_mediodia_b", d_calor - 0.3, d_afuera, z0=1.05, z1=1.16, c0=(0.45, 0.55), c1=(0.40, 0.56), par=(28, 6))
snd(d_calor, "fuego", 0.35, dur=3.5)
snd(d_calor + 0.4, "siseo", 0.4)
snd(d_vidrio, "crujido", 0.4, dur=0.6)


@functools.lru_cache(maxsize=1)
def _luz_derecha():
    return (np.linspace(0, 1, W, dtype=np.float32) ** 2)[None, :, None]


@toma(d_calor - 0.3, ("destello", 0.4))
def s35(lz, t):
    P35.fondo(lz, t)
    quemar(lz, 1.1, color=(1.0, 0.80, 0.58), rampa=_luz_derecha())
    lz += _luz_derecha() * np.float32(CALOR) * 0.25
    quieto(lz, P35, t, "persona_hoja/04", 0.27, 0.94, 0.56, tono=(1.0, 0.74, 0.58), fase=0.2)
    calima(lz, t, 1.0)
    polvo(lz, t, 0.25, color=(1.0, 0.75, 0.45))
    texto(lz, "EL CALOR", W * 0.26, H * 0.13, 84, t, d_calor, None, color=NARANJA, glow=0.9)
    texto(lz, "A TRAVÉS DEL VIDRIO", W * 0.26, H * 0.22, 40, t, d_vidrio - 0.2, None, color=(1.0, 0.8, 0.6), fnt="sans")


# 36 · «Afuera, la ropa tendida empieza a humear.» — detalle del tendedero del balcón
P36 = PF.Plano("sala_mediodia_a", d_afuera - 0.3, d_15, z0=2.15, z1=2.30, c0=(0.77, 0.56), c1=(0.76, 0.55), par=(24, 6))
ROPA36 = [(0.735, 0.585), (0.79, 0.585), (0.88, 0.60), (0.935, 0.58)]
snd(d_afuera, "viento", 0.3, dur=3.0)
snd(d_ropa, "fuego", 0.5, dur=4.0)
snd(d_humear, "siseo", 0.5)


@toma(d_afuera - 0.3, ("latigo", 0.4))
def s36(lz, t):
    P36.fondo(lz, t)
    lz *= 1.25
    lz += np.float32(CALOR) * 0.20
    for k, (x, y) in enumerate(ROPA36):
        X, Y, _ = P36.P(t, x, y)
        u = smooth(prog(t, d_afuera + 0.25 * k, d_humear))
        PF.humo(lz, t, X, Y - 20, s=1.8, n=9, color=(0.20, 0.17, 0.17), op=0.85 * u, sem=k, alto=420)
        PF.brillo(lz, X, Y, 70, color=CALOR, inten=0.35 * u, t=t, sem=k)
        PF.chispas(lz, t, X, Y, s=1.2, n=1 + int(8 * u), sem=k)
    calima(lz, t, 0.9)


# 37 · «A los 15 segundos, el suelo se sacude. Un terremoto de magnitud 7.»
P37 = PF.Plano("sala_mediodia_a", d_15 - 0.3, d_luego, z0=1.02, z1=1.08, c0=(0.50, 0.52), c1=(0.47, 0.54), par=(30, 8))
snd(d_15, "reloj_rapido", 0.5)
snd(d_sacude - 0.35, "trueno", 1.0)
snd(d_sacude, "crujido", 0.9, dur=2.0)
snd(d_sacude + 0.25, "clink", 0.5)
snd(d_7, "golpe_grave", 0.9)


def _amp37(tt):
    return 5 + 130 * smooth(prog(tt, d_sacude - 0.4, d_sacude)) * math.exp(-max(0.0, tt - d_sacude) * 0.45)


@toma(d_15 - 0.3, ("latigo", 0.4))
def s37(lz, t):
    P37.fondo(lz, t)
    lz += np.float32(CALOR) * 0.08
    q = smooth(prog(t, d_sacude - 0.4, d_sacude)) * math.exp(-max(0.0, t - d_sacude) * 0.5)
    if t > d_sacude:                                  # polvo y yeso que caen del techo
        for k in range(14):
            u = ((t - d_sacude) * (0.5 + 0.04 * k) + k * 0.13) % 1.0
            PF._blob(lz, W * (0.08 + 0.065 * k), H * u, 3 + (k % 3), (0.85, 0.80, 0.72), 0.5 * (1 - u))
    quieto(lz, P37, t, "persona_hoja/02", 0.46, 0.97, 0.42, tono=DIA, t_in=d_sacude + 0.15, rot=3 * math.sin(t * 30) * q)
    sacudir(lz, 26 * q, t)
    sismograma(lz, t, H * 0.90, _amp37)
    n = int(15 * smooth(prog(t, d_15 - 0.2, d_sacude - 0.2)))
    texto(lz, f"{n} s", W * 0.18, H * 0.14, 110, t, d_15 - 0.2, None)
    texto(lz, "MAGNITUD 7", W * 0.18, H * 0.27, 64, t, d_7 - 0.1, None, color=ROJO, glow=0.9)


# 38 · «Y luego, nada.» — polvo flotando en la luz, silencio
P38 = PF.Plano("sala_mediodia_b", d_luego - 0.3, si_este, z0=1.40, z1=1.52, c0=(0.42, 0.58), c1=(0.45, 0.57), par=(26, 6))
snd(d_nada + 0.3, "silencio_tono", 0.4, dur=3.0)


@toma(d_luego - 0.3, ("fundido", 0.6))
def s38(lz, t):
    P38.fondo(lz, t)
    lz *= 0.88
    lz += np.float32(POLVO_C) * 0.07
    quieto(lz, P38, t, "persona_hoja/03", 0.58, 0.86, 0.40, tono=DIA, fase=0.5)
    polvo(lz, t * 0.35, 0.50, color=(0.95, 0.82, 0.62))
    ceniza(lz, t * 0.5, 0.25, color=(0.80, 0.72, 0.62))


# ------------------------------------------------------------------ silencio
# 39 · «Este es el peor momento.» — la calle vacía; un paraguas roto rueda con la brisa
P39 = PF.Plano("calle_mediodia_a", si_este - 0.3, si_cielo, z0=1.02, z1=1.12, c0=(0.50, 0.50), c1=(0.50, 0.55), par=(30, 8))
ORBE39 = (0.636, 0.20)
snd(si_este - 0.2, "viento", 0.3, dur=3.0)
snd(si_peor, "grave_inquietante", 0.6)


@toma(si_este - 0.3, ("negro", 0.6))
def s39(lz, t):
    P39.fondo(lz, t)
    X, Y, _ = P39.P(t, *ORBE39)
    PF.brillo(lz, X, Y, 80, color=ROJO, inten=0.35 + 0.1 * math.sin(t * 2), t=t)
    vuela(lz, "utileria/07", t, si_este - 0.3, 4.2, (0.30, 0.88), (0.66, 0.85), 95, giro=40, arco=0.03, tono=DIA)
    PF.arena_viento(lz, t, fuerza=0.18, y0=0.80, y1=1.0, color=(0.60, 0.62, 0.70))
    polvo(lz, t, 0.18)
    texto(lz, "EL PEOR MOMENTO", W * 0.30, H * 0.13, 64, t, si_peor - 0.1, None, color=ROJO, glow=0.8)


# 40 · «El cielo está en calma, el temblor ya pasó, y la gente sale a mirar.»
P40 = PF.Plano("calle_mediodia_a", si_cielo - 0.3, si_nadie, z0=1.38, z1=1.48, c0=(0.50, 0.63), c1=(0.52, 0.62), par=(30, 8))
GENTE40 = [("gente_hoja/00", 0.22, 0.93, 0.34, False, 0.00), ("gente_hoja/02", 0.38, 0.88, 0.30, False, 0.25),
           ("gente_hoja/03", 0.62, 0.90, 0.32, True, 0.45), ("gente_hoja/01", 0.76, 0.86, 0.29, True, 0.65)]
snd(si_calma, "aleteo", 0.5)
snd(si_gente, "multitud", 0.3, dur=4.5)
snd(si_gente + 0.2, "puerta", 0.4)


def _gente40(lz, pl, t, t_ref, empuje=None):
    """La gente de la calle; `empuje(x)` → (dx, giro) cuando la onda los alcanza."""
    for k, (pz, x, y, frac, fl, dt) in enumerate(GENTE40):
        dx, rot = empuje(x) if empuje else (0.0, 0.0)
        quieto(lz, pl, t, pz, x + dx, y, frac, flip=fl, tono=DIA, fase=k, t_in=None if t_ref is None else t_ref + dt, rot=rot)


@toma(si_cielo - 0.3, ("desenfoque", 0.5))
def s40(lz, t):
    P40.fondo(lz, t)
    X, Y, _ = P40.P(t, *ORBE39)
    PF.brillo(lz, X, Y, 80, color=ROJO, inten=0.35, t=t)
    aves(lz, t, [(si_calma, 3.5, 0.40, 0.20, 34, 1, 0.0), (si_calma + 0.3, 3.2, 0.45, 0.24, 28, 1, 0.4),
                 (si_calma + 0.5, 3.6, 0.38, 0.16, 24, 1, 0.8)], tono=(0.16, 0.18, 0.26))
    _gente40(lz, P40, t, si_gente)
    polvo(lz, t, 0.15)
    texto(lz, "CALMA", W * 0.50, H * 0.12, 70, t, si_calma, None, color=TEAL)


# 41 · «Nadie entiende que lo peor todavía viene en camino, a la velocidad del sonido.» — el frente asoma tras el horizonte
P41 = PF.Plano("calle_mediodia_b", si_nadie - 0.3, si_cuatro, z0=1.10, z1=1.20, c0=(0.50, 0.52), c1=(0.50, 0.50), par=(28, 6))
snd(si_viene, "sombra_crece", 0.7, dur=4.0)
snd(si_sonido, "trueno_lejano", 0.45, dur=3.0)


@toma(si_nadie - 0.3, ("latigo", 0.4))
def s41(lz, t):
    P41.fondo(lz, t)
    ox, oy, _ = P41.P(t, *ORBE34)
    PF.brillo(lz, ox, oy, 80, color=ROJO, inten=0.35, t=t)
    _, hY, _ = P41.P(t, 0.5, 0.44)
    u = smooth(prog(t, si_nadie, si_cuatro + 0.4))
    R = lerp(40, 330, u)
    lejos = lejos_pant(P41, t)
    m = np.zeros((H, W), np.uint8)
    cv2.ellipse(m, _p(W * 0.5, hY), _p(R * 2.8, R), 0, 180, 360, 255, -1, cv2.LINE_AA, 4)
    a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 6) * lejos
    _mezcla(lz, a, (0.86, 0.80, 0.72), 0.22)
    m[:] = 0
    cv2.ellipse(m, _p(W * 0.5, hY), _p(R * 2.8, R), 0, 180, 360, 255, 5, cv2.LINE_AA, 4)
    _mezcla(lz, m.astype(np.float32) / 255 * lejos, (0.98, 0.92, 0.84), 0.8, glow=1.2)
    for k, (pz, x) in enumerate((("gente_hoja/04", 0.33), ("gente_hoja/05", 0.66))):
        X, Y, hh = P41.fg(t, x, 1.04, 0.50)
        PF.actor(lz, pz, X, Y, hh, tono=DIA, suelo=0, sy=PF.respira(t, fase=k))
    texto(lz, "VIENE EN CAMINO", W * 0.25, H * 0.11, 64, t, si_viene, None, color=ROJO, glow=0.8)
    texto(lz, "A LA VELOCIDAD DEL SONIDO · ~1 200 km/h", W * 0.25, H * 0.19, 36, t, si_veloc, None, color=TEAL, fnt="sans")


# 42 · «Cuatro minutos y medio de silencio.» — el reloj y una cuenta atrás que se come los 4:30
P42 = PF.Plano("calle_mediodia_a", si_cuatro - 0.3, si_y, z0=1.70, z1=1.82, c0=(0.30, 0.56), c1=(0.32, 0.56), par=(20, 5))
snd(si_cuatro, "reloj_pared", 0.6, dur=3.2)


@toma(si_cuatro - 0.3, ("latigo", 0.35))
def s42(lz, t):
    lz[:] = fondo_quieto(P42, t, 3.0) * 0.8
    tick = int((t - si_cuatro) * 2.0)
    u = PF.entra(t, si_cuatro - 0.3, 0.4)
    PF.actor(lz, "utileria/14", W * 0.28, H * 0.52, H * 0.62 * (0.7 + 0.3 * u), rot=3.0 if tick % 2 else -3.0, ancla=(0.5, 0.5),
             suelo=0, tono=(0.85, 0.88, 1.0))
    rest = int(270 * (1 - clamp01((t - si_cuatro) / (si_y + 0.2 - si_cuatro))))
    texto(lz, f"{rest // 60}:{rest % 60:02d}", W * 0.66, H * 0.44, 230, t, si_cuatro - 0.1, None, fnt="mono", glow=0.7)
    texto(lz, "DE SILENCIO", W * 0.66, H * 0.64, 60, t, si_silencio, None, color=TEAL, fnt="sans")
    polvo(lz, t, 0.15)


# 43 · «Y entonces llega. La onda revienta todas las ventanas…» — el frente barre la calle de izquierda a derecha
P43 = PF.Plano("calle_mediodia_a", si_y - 0.3, si_arranca, z0=1.30, z1=1.24, c0=(0.50, 0.62), c1=(0.50, 0.62), par=(30, 8))
VENT43 = [(0.115, 0.56), (0.24, 0.53), (0.37, 0.53), (0.56, 0.62), (0.70, 0.62), (0.82, 0.62), (0.93, 0.55)]
t_fr = si_llega + 0.15                         # el frente entra por la izquierda
V_FR = 1500.0                                  # px/s en pantalla
snd(si_llega, "trueno", 1.0)
snd(si_llega + 0.1, "explosion", 0.8, tono=0.7)
snd(si_revienta, "estallido", 0.9)
snd(si_ventanas, "clink", 0.7, tono=1.3)
snd(si_ventanas + 0.2, "viento", 0.9, dur=4.0)


@toma(si_y - 0.3, ("corte", 0.1))
def s43(lz, t):
    P43.fondo(lz, t)
    Xf = (t - t_fr) * V_FR - 100

    def golpe_en(X):
        return t - (t_fr + (X + 100) / V_FR)

    def empuje(x):
        X, _, _ = P43.P(t, x, 0.9)
        d = golpe_en(X)
        return (0.10 * min(d, 1.0), min(85.0, 170 * d)) if d > 0 else (0.0, 0.0)
    _gente40(lz, P43, t, None, empuje)
    for k, (x, y) in enumerate(VENT43):
        X, Y, _ = P43.P(t, x, y)
        d = golpe_en(X)
        if d > 0:
            PF._blob(lz, X, Y, 40, (0.9, 0.97, 1.0), 0.8 * math.exp(-d * 3), aditivo=True)
            vidrios(lz, t, t - d, X, Y, fuerza=0.45, op=0.7, giro0=-0.6)
    if t >= t_fr:
        frente(lz, Xf, op=0.65, color=(0.90, 0.84, 0.74))
        k = smooth(prog(t, t_fr, t_fr + 0.6))
        PF.arena_viento(lz, t, fuerza=1.5 * k, y0=0.30, y1=1.0, color=POLVO_C)
        sacudir(lz, 18 * k, t)


# 44 · «…arranca los techos y tumba los árboles, con un viento de huracán.»
P44 = PF.Plano("calle_destruida_b", si_arranca - 0.3, t0Z + 0.4, z0=1.06, z1=1.16, c0=(0.50, 0.50), c1=(0.47, 0.52), par=(30, 8))
VUELA44 = [("utileria/10", si_techos - 0.4, 1.6, (-0.10, 0.36), (1.10, 0.28), 170, 220, 0.10),
           ("utileria/06", si_arranca, 1.4, (-0.10, 0.52), (1.10, 0.40), 120, 360, 0.05),
           ("utileria/10", si_techos + 0.5, 1.3, (-0.10, 0.60), (1.10, 0.46), 120, -300, 0.06),
           ("utileria/11", si_tumba - 0.2, 2.2, (-0.15, 0.66), (1.15, 0.72), 280, 140, 0.12),
           ("utileria/07", si_viento - 0.5, 1.4, (-0.10, 0.42), (1.10, 0.30), 90, 500, 0.04),
           ("utileria/10", si_viento + 0.3, 1.5, (-0.10, 0.50), (1.10, 0.62), 150, 260, 0.08)]
snd(si_techos, "crujido", 0.9, dur=1.0)
snd(si_tumba, "crujido", 0.8, dur=1.2)
snd(si_viento, "viento", 1.0, dur=4.0)


@toma(si_arranca - 0.3, ("latigo", 0.35))
def s44(lz, t):
    P44.fondo(lz, t)
    _fuegos(lz, P44, t, [(0.545, 0.48, 1.2)], humo=False)
    lz[:] = lz * 0.86 + np.float32((0.45, 0.35, 0.28)) * 0.12
    PF.arena_viento(lz, t, fuerza=1.6, y0=0.35, y1=1.0, color=POLVO_C)
    for pz, ta, dur, a, b, h, giro, arco in VUELA44:
        vuela(lz, pz, t, ta, dur, a, b, h, giro, arco, tono=(0.75, 0.70, 0.72))
    vidrios(lz, t, si_arranca, W * 0.15, H * 0.45, fuerza=0.8, giro0=-0.6)
    vidrios(lz, t, si_tumba, W * 0.85, H * 0.45, fuerza=0.7, giro0=-0.6)
    PF.arena_viento(lz, t + 3.0, fuerza=0.9, y0=0.10, y1=0.60, color=POLVO_C, sem=3)
    texto(lz, "VIENTO DE HURACÁN", W * 0.5, H * 0.12, 72, t, si_viento, None, color=ROJO, glow=0.9)
    sacudir(lz, 9 + 5 * math.sin(t * 3), t)


# ------------------------------------------------------------------ zona_cero
FUEGOS_A = [(0.50, 0.55, 1.6), (0.20, 0.47, 0.6), (0.18, 0.64, 0.7), (0.27, 0.76, 0.8), (0.46, 0.84, 0.9), (0.69, 0.39, 0.6),
            (0.81, 0.54, 0.7), (0.80, 0.67, 0.8)]
FUEGOS_B = [(0.50, 0.58, 1.5), (0.34, 0.38, 0.5), (0.16, 0.55, 0.6), (0.31, 0.75, 0.7), (0.73, 0.40, 0.5), (0.82, 0.55, 0.6),
            (0.69, 0.71, 0.6), (0.79, 0.80, 0.7)]

# 45 · «Donde cayó, ya no queda nada que salvar.» — vista aérea del cráter
P45 = PF.Plano("zona_cero_a", z_donde - 0.4, z_crater, z0=1.30, z1=1.12, c0=(0.50, 0.55), c1=(0.50, 0.50), par=(30, 8))
snd(z_donde - 0.3, "fuego", 0.5, dur=4.5)
snd(z_donde, "viento", 0.4, dur=4.0)
snd(z_nada, "golpe_grave", 0.5)


@toma(z_donde - 0.4, ("negro", 0.8))
def s45(lz, t):
    P45.fondo(lz, t)
    _fuegos(lz, P45, t, FUEGOS_A)
    ceniza(lz, t, 0.35)
    texto(lz, "ZONA CERO", W * 0.18, H * 0.12, 70, t, z_donde, None)


# 46 · «Un cráter de unos 7 kilómetros. Todo lo que había a 30 kilómetros a la redonda desapareció.»
P46 = PF.Plano("zona_cero_b", z_crater - 0.3, z_columna, z0=1.35, z1=1.08, c0=(0.50, 0.58), c1=(0.50, 0.53), par=(28, 6))
CRATER = (0.50, 0.555, 0.225, 0.115)         # centro y semiejes (x en anchos, y en altos del escenario)
snd(z_7, "tick", 0.7)
snd(z_30 - 0.1, "barrido_aire", 0.8)
snd(z_30 + 0.6, "apagon", 0.6)


@toma(z_crater - 0.3, ("desenfoque", 0.5))
def s46(lz, t):
    P46.fondo(lz, t)
    _fuegos(lz, P46, t, FUEGOS_B)
    cx, cy, _ = P46.P(t, CRATER[0], CRATER[1])
    rx, ry = CRATER[2] * P46.ancho_mundo(t), P46.alto_px(t, CRATER[3])
    if t >= z_crater:
        u = e_inout(clamp01((t - z_crater) / 1.0))
        trazo(lz, lambda m: elipse_punteada(m, cx, cy, rx * 1.05, ry * 1.08, u=u, a0=180, paso=5, g=3), TEAL, 0.9, glow=0.8)
        yc = cy - ry * 1.08 - 34
        v = e_inout(clamp01((t - z_7 + 0.2) / 0.5))
        if v > 0:
            def cota_h(m):
                cv2.line(m, _p(cx - rx * v, yc), _p(cx + rx * v, yc), 255, 3, cv2.LINE_AA, 4)
                for xx in (cx - rx * v, cx + rx * v):
                    cv2.line(m, _p(xx, yc - 14), _p(xx, yc + 14), 255, 3, cv2.LINE_AA, 4)
            trazo(lz, cota_h, TEAL, 0.9, glow=0.7)
        texto(lz, "7 km", cx, yc - 52, 72, t, z_7, None, color=TEAL)
    if t >= z_30 - 0.2:                               # el anillo de 30 km sale disparado y se pierde fuera del cuadro
        v = e_inout(clamp01((t - (z_30 - 0.2)) / 1.4))
        R = lerp(rx * 1.1, W * 2.2, v)
        m = np.zeros((H, W), np.uint8)
        cv2.ellipse(m, _p(cx, cy), _p(R, R * ry / rx), 0, 0, 360, 255, -1, cv2.LINE_AA, 4)
        a = m.astype(np.float32) / 255 * smooth(prog(t, z_30, z_30 + 1.2))
        lz[:] = lz * (1 - 0.45 * a[..., None]) + np.float32((0.30, 0.04, 0.02)) * (0.18 * a[..., None])
        trazo(lz, lambda mm: cv2.ellipse(mm, _p(cx, cy), _p(R, R * ry / rx), 0, 0, 360, 255, 6, cv2.LINE_AA, 4), ROJO,
              0.9 * (1 - 0.6 * v), glow=1.0)
        texto(lz, "30 km A LA REDONDA", W * 0.5, H * 0.90, 62, t, z_30 + 0.3, None, color=ROJO, glow=0.9)


# 47 · «Una columna de polvo y fuego sube más alto que los aviones…» — el avión cruza muy por debajo del sombrero
P47 = PF.Plano("columna_a", z_columna - 0.3, z_rocas, z0=1.45, z1=1.15, c0=(0.58, 0.62), c1=(0.60, 0.42), par=(30, 8))
snd(z_columna, "trueno_lejano", 0.7, dur=4.0)
snd(z_sube, "crecer", 0.6)
snd(z_aviones - 0.4, "zoom_whoosh", 0.4)


@toma(z_columna - 0.3, ("latigo", 0.4))
def s47(lz, t):
    P47.fondo(lz, t)
    cl, _, _ = P47.P(t, 0.45, 0.5)
    cr, _, _ = P47.P(t, 0.78, 0.5)
    _, hY, _ = P47.P(t, 0.5, 0.58)
    estrellas(lz, t, mascara=lambda X, Y: (X < cl or X > cr) and Y < hY)
    for k, (x, y, r) in enumerate([(0.62, 0.58, 260), (0.62, 0.36, 150), (0.63, 0.15, 220)]):
        X, Y, _ = P47.P(t, x, y)
        PF.brillo(lz, X, Y, r, color=(1.0, 0.45, 0.15), inten=0.30, t=t, sem=k)
    X, Y, _ = P47.P(t, 0.62, 0.40)
    PF.chispas(lz, t, X, Y, s=2.0, n=14)
    gx, gy, s = P47.P(t, 0.30, 0.64)                   # suelo
    ax_, ay, _ = P47.P(t, lerp(0.30, 0.52, clamp01((t - (z_sube - 0.6)) / 4.0)), 0.40)
    _, cy0, _ = P47.P(t, 0.62, 0.07)                   # techo del sombrero
    if t >= z_sube - 0.6:
        trazo(lz, lambda m: avion(m, ax_, ay, 0.07 * P47.ancho_mundo(t)), BLANCO, 0.95, glow=0.6)
        D.linea_punteada(lz, [(ax_ - 0.07 * P47.ancho_mundo(t) * 0.55, ay), (ax_ - 900, ay)], 1.0, color=BLANCO, grosor=2, glow=0.4, op=0.4)
        cota(lz, gx, ay, gy, t, z_sube - 0.2, "~10 km", color=TEAL, px=40)
        cota(lz, P47.P(t, 0.83, 0.5)[0], cy0, gy, t, z_aviones - 0.2, "", color=NARANJA)
    texto(lz, "MÁS ALTO QUE LOS AVIONES", W * 0.5, H * 0.92, 52, t, z_aviones - 0.2, None, color=NARANJA, glow=0.8)
    ceniza(lz, t, 0.25)


# 48 · «…y las rocas que salieron volando caen encendidas sobre los incendios.»
P48 = PF.Plano("zona_cero_a", z_rocas - 0.5, z_cerca, z0=1.85, z1=1.95, c0=(0.30, 0.68), c1=(0.33, 0.66), par=(26, 6))
CAEN48 = [(z_rocas - 0.3, 0.22, 0.62, "utileria/12", 120), (z_rocas + 0.4, 0.42, 0.72, "fuego_humo/09", 80),
          (z_rocas + 1.0, 0.15, 0.80, "utileria/12", 150), (z_rocas + 1.6, 0.36, 0.86, "fuego_humo/11", 90),
          (z_rocas + 2.3, 0.50, 0.64, "utileria/12", 110), (z_incend - 0.5, 0.28, 0.74, "fuego_humo/09", 100),
          (z_incend + 0.2, 0.46, 0.88, "utileria/12", 130)]
for _tk, *_ in CAEN48:
    snd(_tk + 0.85, "canonazo", 0.35)
snd(z_rocas, "fuego", 0.6, dur=5.5)


@toma(z_rocas - 0.5, ("desenfoque", 0.45))
def s48(lz, t):
    P48.fondo(lz, t)
    _fuegos(lz, P48, t, [f for f in FUEGOS_A if f[0] < 0.6 and f[1] > 0.4])
    for k, (tk, x, y, pz, h) in enumerate(CAEN48):
        if t < tk:
            continue
        X1, Y1, _ = P48.P(t, x, y)
        u = (t - tk) / 0.85
        if u < 1:                                   # cae de arriba a la derecha con su cola de fuego
            X, Y = lerp(X1 + 0.40 * W, X1, u), lerp(Y1 - 0.70 * H, Y1, u)
            ang = math.degrees(math.atan2(0.70 * H, -0.40 * W))
            cola(lz, X, Y, ang, 260, 18, color=(1.0, 0.55, 0.20), op=0.5)
            PF.brillo(lz, X, Y, h * 0.9, color=(1.0, 0.5, 0.2), inten=0.5, t=t, sem=k)
            if pz == "utileria/12":
                PF.actor(lz, pz, X, Y, h, rot=ang - 145, ancla=(0.3, 0.7), suelo=0, sombra=False)
            else:
                PF.actor(lz, pz, X, Y, h, rot=300 * (t - tk), ancla=(0.5, 0.5), suelo=0, sombra=False)
        else:                                       # golpe y un incendio nuevo
            d = t - tk - 0.85
            PF._blob(lz, X1, Y1, 160, (1.0, 0.75, 0.45), 0.9 * math.exp(-d * 4), aditivo=True)
            PF.brillo(lz, X1, Y1, 80, color=(1.0, 0.45, 0.15), inten=0.5 * smooth(clamp01(d * 2)), t=t, sem=k)
            PF.chispas(lz, t, X1, Y1, s=1.2, n=8, sem=k)
            PF.humo(lz, t, X1, Y1 - 10, s=1.0, n=6, color=(0.18, 0.14, 0.13), op=0.35 * smooth(clamp01(d)), sem=k)
    ceniza(lz, t, 0.3)


# 49 · «Cerca de una gran ciudad, serían millones de personas. En menos de cinco minutos.»
P49 = PF.Plano("calle_destruida_a", z_cerca - 0.3, z_no, z0=1.08, z1=1.20, c0=(0.50, 0.50), c1=(0.55, 0.52), par=(30, 8))
HUMO49 = [(0.17, 0.30, 1.6), (0.34, 0.20, 1.4), (0.72, 0.28, 1.6), (0.88, 0.32, 1.3), (0.795, 0.57, 0.8)]
snd(z_cerca, "fuego", 0.4, dur=6.0)
snd(z_millones, "golpe_grave", 0.8)
snd(z_menos, "reloj_rapido", 0.5)


@toma(z_cerca - 0.3, ("negro", 0.6))
def s49(lz, t):
    P49.fondo(lz, t)
    for k, (x, y, s) in enumerate(HUMO49):
        X, Y, _ = P49.P(t, x, y)
        PF.humo(lz, t, X, Y, s=s, n=7, color=(0.24, 0.20, 0.19), op=0.35, sem=k, alto=320)
    _fuegos(lz, P49, t, [(0.635, 0.585, 1.0)], humo=False)
    ceniza(lz, t, 0.45)
    sombra_txt(lz, W * 0.5, H * 0.20, 620, 190, 0.55)
    texto(lz, "MILLONES", W * 0.5, H * 0.15, 150, t, z_millones, None, color=ROJO, glow=0.9)
    texto(lz, "DE PERSONAS", W * 0.5, H * 0.27, 52, t, z_personas, None, fnt="sans")
    texto(lz, "EN MENOS DE 5 MINUTOS", W * 0.5, H * 0.88, 56, t, z_menos, None, color=TEAL, fnt="sans")


# 50 · «No es el fin del mundo. Es el fin de tu mundo.» — tú, agachado entre las ruinas
P50 = PF.Plano("calle_destruida_b", z_no - 0.3, t0Q + 0.4, z0=1.80, z1=1.95, c0=(0.50, 0.70), c1=(0.50, 0.69), par=(24, 6))
snd(z_no, "viento", 0.35, dur=5.0)
snd(z_es2, "latido", 0.6)
snd(z_tu, "golpe_grave", 0.7)


@toma(z_no - 0.3, ("desenfoque", 0.5))
def s50(lz, t):
    lz[:] = fondo_quieto(P50, t, 2.5)
    X, Y, _ = P50.P(t, 0.545, 0.48)
    PF.brillo(lz, X, Y, 200, color=(1.0, 0.45, 0.15), inten=0.35, t=t)
    X, Y, hh = P50.fg(t, 0.50, 0.97, 0.62)
    PF.actor(lz, "persona_hoja/02", X, Y, hh, tono=(0.72, 0.60, 0.60), sy=PF.respira(t, f=0.6, a=0.02))
    PF.chispas(lz, t, W * 0.82, H * 0.70, s=1.2, n=8)
    ceniza(lz, t, 0.5)
    sombra_txt(lz, W * 0.5, H * 0.13, 560, 110, 0.5)
    texto(lz, "NO ES EL FIN DEL MUNDO", W * 0.5, H * 0.13, 50, t, z_no, z_es2 - 0.2, fnt="sans")
    texto(lz, "ES EL FIN DE TU MUNDO", W * 0.5, H * 0.13, 70, t, z_es2, None, color=ROJO, glow=0.9)


# ------------------------------------------------------------------ peor
# 51 · «Y esto es lo que sí sabemos buscar. Hay cuerpos que no aparecen en ninguna lista…»
P51 = PF.Plano("sistema_exterior_a", q_esto - 0.3, q_cometas, z0=1.06, z1=1.18, c0=(0.50, 0.55), c1=(0.47, 0.58), par=(30, 8))
ROCAS51 = [(0.06, 0.55), (0.27, 0.72), (0.42, 0.80), (0.62, 0.74), (0.80, 0.66), (0.93, 0.53), (0.85, 0.78)]
PLANETA51 = (0.695, 0.38, 0.095)
snd(q_esto, "datos", 0.45, dur=1.5)
snd(q_sabemos, "pin", 0.5)
snd(q_ninguna, "error", 0.5)
snd(q_ninguna + 0.2, "grave_inquietante", 0.6)


@toma(q_esto - 0.3, ("negro", 0.8))
def s51(lz, t):
    P51.fondo(lz, t)
    px, py, _ = P51.P(t, PLANETA51[0], PLANETA51[1])
    pr = PLANETA51[2] * P51.ancho_mundo(t)
    estrellas(lz, t, mascara=lambda X, Y: math.hypot(X - px, Y - py) > pr * 1.05)
    roca(lz, "asteroide_hoja/03", W * (0.12 + 0.010 * (t - q_esto)), H * 0.30, 60, t, giro=9)
    for k, (x, y) in enumerate(ROCAS51):
        X, Y, _ = P51.P(t, x, y)
        reticula(lz, X, Y, 34, t, q_sabemos + 0.12 * k, color=TEAL, op=0.85)
    texto(lz, "LO QUE SÍ BUSCAMOS", W * 0.30, H * 0.12, 56, t, q_sabemos, None, color=TEAL)
    if t >= q_ninguna - 0.2:                          # algo que no está en ninguna lista: una mira roja sobre el vacío
        gx, gy = W * 0.36, H * 0.42
        reticula(lz, gx, gy, 46, t, q_ninguna - 0.2, color=ROJO)
        texto(lz, "?", gx, gy, 60, t, q_ninguna, None, color=ROJO, glow=0.9)
        texto(lz, "EN NINGUNA LISTA", W * 0.30, H * 0.20, 46, t, q_ninguna, None, color=ROJO, fnt="sans")
    polvo(lz, t, 0.2)


# 52 · «…cometas que caen desde los confines del sistema solar, más rápidos y más grandes.»
P52 = PF.Plano("sistema_exterior_b", q_cometas - 0.3, q_2013, z0=1.04, z1=1.16, c0=(0.50, 0.50), c1=(0.54, 0.47), par=(30, 8))
snd(q_cometas, "zoom_whoosh", 0.8)
snd(q_confines, "teremin", 0.4)
snd(q_rapidos, "whoosh", 0.7)
snd(q_grandes, "sombra_crece", 0.7)


def _cruza(lz, t, ta, tb, a, b, h, op=1.0):
    """Cometa que cruza de a a b (pantalla, relativos) entre ta y tb, con su cola de luz."""
    if not ta <= t <= tb:
        return
    u = (t - ta) / (tb - ta)
    X, Y = lerp(a[0], b[0], u) * W, lerp(a[1], b[1], u) * H
    ang = math.degrees(math.atan2((b[1] - a[1]) * H, (b[0] - a[0]) * W))
    cola(lz, X, Y, ang, h * 6, h * 0.30, op=0.45 * op)
    cometa(lz, X, Y, h, ang, op=op)


@toma(q_cometas - 0.3, ("latigo", 0.4))
def s52(lz, t):
    P52.fondo(lz, t)
    px, py, _ = P52.P(t, 0.695, 0.42)
    pr = 0.088 * P52.ancho_mundo(t)
    estrellas(lz, t, mascara=lambda X, Y: math.hypot(X - px, Y - py) > pr * 1.05)
    _cruza(lz, t, q_cometas - 0.4, q_rapidos + 1.2, (1.15, -0.10), (0.05, 0.90), 150)
    _cruza(lz, t, q_grandes - 0.6, q_2013 + 0.6, (1.20, 0.15), (0.25, 1.20), 260)
    texto(lz, "COMETAS", W * 0.22, H * 0.12, 80, t, q_cometas, None, color=TEAL)
    texto(lz, "MÁS RÁPIDOS", W * 0.22, H * 0.21, 46, t, q_rapidos, None, color=ROJO, fnt="sans")
    texto(lz, "MÁS GRANDES", W * 0.22, H * 0.28, 46, t, q_grandes, None, color=ROJO, fnt="sans")
    polvo(lz, t, 0.2)


# 53 · «En 2013 descubrimos uno que iba a pasar rozando Marte. Lo vimos menos de dos años antes.»
P53 = PF.Plano("marte_b", q_2013 - 0.3, q_contra, z0=1.04, z1=1.14, c0=(0.50, 0.50), c1=(0.46, 0.52), par=(28, 6))
RUTA53 = ((0.30, -0.10), (0.56, 1.10))      # pasa a un dedo del limbo de Marte (x ≈ 0.60 a media altura)
snd(q_2013, "whoosh", 0.5)
snd(q_rozando, "zoom_whoosh", 0.8)
snd(q_menos, "golpe_grave", 0.7)


@toma(q_2013 - 0.3, ("desenfoque", 0.5))
def s53(lz, t):
    P53.fondo(lz, t)
    lx, _, _ = P53.P(t, 0.50, 0.5)
    estrellas(lz, t, mascara=lambda X, Y: X < lx)
    A = P53.P(t, *RUTA53[0])[:2]
    B = P53.P(t, *RUTA53[1])[:2]
    D.linea_punteada(lz, [A, B], smooth(prog(t, q_2013, q_2013 + 1.0)), color=TEAL, grosor=3, glow=0.6, op=0.6)
    u = clamp01((t - (q_2013 - 0.2)) / (q_vimos + 0.6 - q_2013))
    X, Y = lerp(A[0], B[0], u), lerp(A[1], B[1], u)
    ang = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    if u < 1:
        cola(lz, X, Y, ang, 700, 40, op=0.45)
        cometa(lz, X, Y, 170, ang)
    mx, my, _ = P53.P(t, 0.60, 0.55)
    PF.brillo(lz, mx, my, 180, color=(1.0, 0.45, 0.25), inten=0.25 + 0.15 * smooth(prog(t, q_rozando - 0.3, q_rozando + 0.5)), t=t)
    texto(lz, "SIDING SPRING · 2013", W * 0.04, H * 0.72, 56, t, q_2013, None, ancla=0.0)
    texto(lz, "pasó a ~140 000 km de Marte", W * 0.04, H * 0.79, 34, t, q_rozando, None, color=TEAL, fnt="sans", ancla=0.0)
    barra(lz, W * 0.04, H * 0.84, W * 0.34, 34, 1.0, ROJO, t, q_vimos)
    texto(lz, "MENOS DE 2 AÑOS DE AVISO", W * 0.04, H * 0.92, 44, t, q_menos, None, color=ROJO, ancla=0.0)


# 54 · «Contra algo así, dos años no alcanzan para nada.»
P54 = PF.Plano("marte_a", q_contra - 0.3, t0K + 0.5, z0=1.15, z1=1.06, c0=(0.55, 0.50), c1=(0.52, 0.50), par=(28, 6))
snd(q_dos, "reloj_rapido", 0.5)
snd(q_alcanzan + 0.3, "error", 0.6)
snd(q_nada, "grave_inquietante", 0.6)


@toma(q_contra - 0.3, ("latigo", 0.4))
def s54(lz, t):
    P54.fondo(lz, t)
    lx, _, _ = P54.P(t, 0.70, 0.5)
    estrellas(lz, t, mascara=lambda X, Y: X < lx)
    mx, my, _ = P54.P(t, 0.74, 0.48)
    PF.brillo(lz, mx, my, 200, color=(1.0, 0.5, 0.3), inten=0.30 + 0.1 * math.sin(t * 1.5), t=t)
    _cruza(lz, t, q_contra - 0.3, t0K + 2.0, (-0.05, 0.10), (0.80, 0.55), 70, op=0.8)
    apag = 1.0 - 0.65 * smooth(prog(t, q_nada, q_nada + 0.6))
    texto(lz, "2 AÑOS", W * 0.33, H * 0.45, 200, t, q_dos - 0.1, None, op=apag)
    if t >= q_alcanzan:
        v = e_inout(clamp01((t - q_alcanzan) / 0.4))
        trazo(lz, lambda m: cv2.line(m, _p(W * 0.12, H * 0.52), _p(W * 0.12 + W * 0.43 * v, H * 0.38), 255, 12, cv2.LINE_AA, 4),
              ROJO, 0.95, glow=1.0)
    texto(lz, "NO ALCANZAN", W * 0.33, H * 0.64, 70, t, q_alcanzan + 0.2, None, color=ROJO, glow=0.9)
    if t >= q_nada:
        pulso_rojo(lz, 0.3 * math.exp(-(t - q_nada) * 1.2))
    polvo(lz, t, 0.2)


# ------------------------------------------------------------------ cierre
# 55 · «Está previsto que en 2027 despegue un telescopio espacial hecho para mirar hacia el Sol, justo donde hoy estamos ciegos.»
# Vuelve el punto ciego de s7 y el NEO Surveyor (pieza de telescopio de Flow, sin marca) lo tapa con su cono teal desde L1.
P55 = PF.Plano("sistema_solar_b", t0K + 0.2, c_hasta, z0=1.05, z1=1.18, c0=(0.48, 0.52), c1=(0.44, 0.52), par=(24, 6))
snd(c_2027, "datos", 0.5, dur=1.2)
snd(c_telesc - 0.4, "motor_acelera", 0.4, dur=2.0)
snd(c_mirar, "servo", 0.6)
snd(c_ciegos, "revelar", 0.6)


@toma(t0K + 0.2, ("desenfoque", 0.6))
def s55(lz, t):
    P55.fondo(lz, t)
    sx, sy, _ = P55.P(t, *SS_B["sol"])
    tx, ty, _ = P55.P(t, *SS_B["tierra"])
    estrellas(lz, t, mascara=lambda X, Y: X > sx + 260)
    ang = math.atan2(sy - ty, sx - tx)
    cob = smooth(prog(t, c_mirar, c_ciegos + 0.4))
    lat = 0.5 + 0.5 * math.sin(t * 6.5)
    L2 = math.hypot(sx - tx, sy - ty)
    pts = [(tx, ty)] + [(tx + L2 * math.cos(ang + a), ty + L2 * math.sin(ang + a)) for a in np.linspace(-0.42, 0.42, 14)]
    trazo(lz, lambda m: poligono(m, pts), ROJO, (0.13 + 0.10 * lat) * (1 - 0.8 * cob), glow=0.9)
    texto(lz, "PUNTO CIEGO", lerp(tx, sx, 0.5), lerp(ty, sy, 0.5) - L2 * 0.5 * math.tan(0.42) - 120, 64, t, t0K + 0.4, None,
          color=ROJO, glow=0.9, op=1 - 0.85 * cob)
    lx, ly = lerp(tx, sx, 0.22), lerp(ty, sy, 0.22)            # L1, esquemático
    if t >= c_telesc - 0.6:
        u = e_inout(clamp01((t - (c_telesc - 0.6)) / 1.6))
        X, Y = lerp(W * 1.10, lx, u), lerp(H * 0.12, ly, u)
        if t >= c_mirar - 0.2:                                  # su cono teal hacia el Sol cubre el punto ciego
            v = smooth(prog(t, c_mirar - 0.2, c_sol + 0.4))
            L = math.hypot(sx - X, sy - Y) * v
            a0 = math.atan2(sy - Y, sx - X)
            cono = [(X, Y)] + [(X + L * math.cos(a0 + a), Y + L * math.sin(a0 + a)) for a in np.linspace(-0.50, 0.50, 16)]
            trazo(lz, lambda m: poligono(m, cono), TEAL, 0.20, glow=0.6)
            trazo(lz, lambda m: cv2.polylines(m, [np.array([_p(*q) for q in (cono[1], cono[0], cono[-1])], np.int32)], False, 255, 3,
                                              cv2.LINE_AA, 4), TEAL, 0.8, glow=0.8)
        PF.actor(lz, "utileria/04", X, Y, 110, rot=-8 + 3 * math.sin(t), ancla=(0.5, 0.5), suelo=0, tono=FRIO)
        texto(lz, "NEO SURVEYOR", X, Y - 100, 44, t, c_telesc + 0.4, None, color=TEAL)
        texto(lz, "(previsto)", X, Y - 62, 28, t, c_telesc + 0.6, None, color=(0.6, 0.66, 0.78), fnt="sans_l", glow=0.0)
    texto(lz, "2027", W * 0.82, H * 0.13, 120, t, c_2027, None, color=TEAL)
    polvo(lz, t, 0.2)


# 56 · «Hasta entonces, seguimos vigilando el cielo de noche, y esperando que lo que venga, venga por el lado oscuro.»
P56 = PF.Plano("observatorio_b", c_hasta - 0.3, c_proxima, z0=1.38, z1=1.50, c0=(0.60, 0.42), c1=(0.62, 0.38), par=(30, 8))
DOMO56 = (0.66, 0.36)
ROCA56 = (0.36, 0.14)
snd(c_vigil, "servo", 0.5)
snd(c_esper, "teremin", 0.35)
snd(c_lado, "pin", 0.6)


@toma(c_hasta - 0.3, ("negro", 0.6))
def s56(lz, t):
    P56.fondo(lz, t)
    _, hY, _ = P56.P(t, 0.5, 0.44)
    estrellas(lz, t, mascara=lambda X, Y: Y < hY)
    dx, dy, _ = P56.P(t, *DOMO56)
    rx, ry, _ = P56.P(t, ROCA56[0] + 0.004 * (t - c_esper), ROCA56[1])
    apunta = smooth(prog(t, c_esper, c_lado))
    a_barre = math.radians(-120 + 25 * math.sin(t * 0.6))
    a_roca = math.atan2(ry - dy, rx - dx)
    a = lerp(a_barre, a_roca, apunta)
    L = 1400
    haz = [(dx, dy), (dx + L * math.cos(a - 0.05), dy + L * math.sin(a - 0.05)), (dx + L * math.cos(a + 0.05), dy + L * math.sin(a + 0.05))]
    trazo(lz, lambda m: poligono(m, haz), TEAL, 0.13, glow=0.5)
    PF.brillo(lz, dx, dy, 50, color=TEAL, inten=0.4, t=t)
    if t >= c_esper:
        o = smooth(prog(t, c_esper, c_esper + 0.6))
        PF._blob(lz, rx, ry, 26, (0.95, 0.95, 1.0), 0.8 * o, aditivo=True)
        roca(lz, "asteroide_hoja/02", rx, ry, 30, t, giro=20, op=o)
        reticula(lz, rx, ry, 40, t, c_lado - 0.2, color=TEAL)
        texto(lz, "DETECTADA", rx + 70, ry + 8, 34, t, c_lado, None, color=TEAL, fnt="sans", ancla=0.0)
    texto(lz, "EL LADO OSCURO", W * 0.30, H * 0.88, 64, t, c_lado, None, color=TEAL)
    aves(lz, t, [(c_hasta, 6.0, 0.30, 0.26, 20, 1, 0.2)], tono=(0.10, 0.11, 0.18))
    polvo(lz, t, 0.15)


# 57 · «La próxima vez que veas un atardecer, recuérdalo.»
P57 = PF.Plano("atardecer_a", c_proxima - 0.3, c_de, z0=1.30, z1=1.40, c0=(0.46, 0.55), c1=(0.50, 0.53), par=(30, 8))
SOL57 = (0.725, 0.44)
snd(c_proxima, "viento", 0.35, dur=4.5)
snd(c_atard, "grillos", 0.3, dur=4.0)


@toma(c_proxima - 0.3, ("fundido", 0.8))
def s57(lz, t):
    P57.fondo(lz, t)
    X, Y, _ = P57.P(t, *SOL57)
    PF.brillo(lz, X, Y, 220, color=(1.0, 0.45, 0.20), inten=0.25 + 0.05 * math.sin(t * 1.3), t=t)
    aves(lz, t, [(c_proxima - 0.3, 5.0, 0.30, 0.24, 22, -1, 0.0), (c_proxima + 0.4, 5.5, 0.36, 0.30, 18, -1, 0.5)],
         tono=(0.12, 0.10, 0.14))
    quieto(lz, P57, t, "persona_hoja/01", 0.37, 0.69, 0.27, tono=(0.62, 0.50, 0.56), fase=0.3)
    PF.arena_viento(lz, t, fuerza=0.15, y0=0.78, y1=1.0, color=(0.9, 0.5, 0.3))
    polvo(lz, t, 0.15, color=(1.0, 0.7, 0.5))


# 58 · «De ahí vienen las que no vemos.» — una mota oscura sale del disco del Sol y crece… hasta el fundido final
P58 = PF.Plano("atardecer_b", c_de - 0.3, TOTAL, z0=1.15, z1=1.70, c0=(0.50, 0.45), c1=(0.50, 0.41), par=(26, 6))
SOL58 = (0.50, 0.40)
snd(c_vienen, "sombra_crece", 0.8, dur=3.0)
snd(c_vemos + 0.4, "latido", 0.7)
snd(c_vemos + 1.2, "latido", 0.85)
snd(TOTAL - 1.6, "golpe_grave", 0.9)


@toma(c_de - 0.3, ("desenfoque", 0.6))
def s58(lz, t):
    P58.fondo(lz, t)
    sx, sy, _ = P58.P(t, *SOL58)
    PF.brillo(lz, sx, sy, 240, color=(1.0, 0.45, 0.20), inten=0.30 + 0.05 * math.sin(t * 1.3), t=t)
    if t >= c_vienen - 0.4:
        g = clamp01((t - (c_vienen - 0.4)) / (TOTAL - c_vienen))
        X = sx + 0.10 * P58.ancho_mundo(t) * lerp(0.55, 0.20, g)
        Y = sy - 0.10 * P58.ancho_mundo(t) * lerp(0.35, 0.05, g)
        roca(lz, "asteroide_hoja/00", X, Y, lerp(8, 170, g ** 1.7), t, giro=3, tono=(0.10, 0.07, 0.08),
             op=smooth(prog(t, c_vienen - 0.4, c_vienen + 0.4)))
        if t >= c_vemos + 0.4:
            pulso_rojo(lz, 0.30 * max(0.0, math.sin((t - c_vemos - 0.4) * math.pi / 0.8)))
    polvo(lz, t, 0.15, color=(1.0, 0.7, 0.5))


TOMAS.sort(key=lambda d: d["t0"])


def _cuadro(d, t):
    lz = np.zeros((H, W, 3), np.float32)
    d["dib"](lz, t)
    return lz


def render_mundo(t):
    i = 0
    for k, d in enumerate(TOMAS):
        if d["t0"] <= t:
            i = k
    d = TOMAS[i]
    img = _cuadro(d, t)
    tipo, dur = d["ent"]
    if i > 0 and t < d["t0"] + dur and tipo != "corte":
        img = D.mezcla_tomas(_cuadro(TOMAS[i - 1], t), img, (t - d["t0"]) / dur, tipo)
    img = PF.acabado(img, t, calido=0.0)
    img = img * smooth(prog(t, 0.0, 0.6)) * (1.0 - smooth(prog(t, TOTAL - 1.4, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SFX:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
