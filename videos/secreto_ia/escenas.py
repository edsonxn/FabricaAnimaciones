# -*- coding: utf-8 -*-
"""«¿Puede una IA guardar un secreto?» (LogIA) — REHECHO el 21-oct-2026 con PEGATINA FLOW en look NOIR (nucleo/pegaflow.py):
16 escenarios de Flow en tinta y aguada (1K) con cámara y parallax por profundidad, personajes y utilería recortados de hojas de
Flow en 2K (detective, la IA como androide de cara de porcelana, investigadores, ciclos de caminar) animados como pegatinas.
31 tomas ancladas a palabras de la voz (David). Ambiente continuo: lluvia, polillas en las lámparas, polvo en los haces de luz,
LEDs de servidores, humo. MG noir por código: hoja escrita a máquina que se teclea, sellos de tinta, tiras de papel, páginas REALES
de los tres papers (arXiv) y foto real de Dario Amodei (CC BY 2.0, TechCrunch). Todo termina en B/N puro (canal LogIA)."""
import functools
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, lerp, prog, smooth

TOTAL = TL["total"]
FM = "C:/Windows/Fonts/courbd.ttf"                     # máquina de escribir
FI = "C:/Windows/Fonts/impact.ttf"                     # sellos y rótulos del canal
FT = next((p for p in ("C:/Windows/Fonts/segoepr.ttf", "C:/Windows/Fonts/segoesc.ttf", "C:/Windows/Fonts/comic.ttf")
           if os.path.exists(p)), FM)                  # tiza
TINTA = (24, 22, 21)
G, P, I, F, C = "gancho", "puerta", "interrogatorio", "fingir", "cierre"


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


SFX = []      # procedurales de nucleo/sfx.py
FXP = []      # propios (sfx/<nombre>.mp3, ElevenLabs del 8-oct): (t, nombre, vol, dur o None, fundido) → _sfx_propios.py → audio/fx.wav


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


def fx(t, n, v=1.0, dur=None, fade=0.0):
    FXP.append((t, n, v, dur, fade))


# ------------------------------------------------------------------ personajes (como en jalpa)
MIRA = {"detective_camina": 1, "ia_camina": 1, "detective_hoja/01": 1, "ia_hoja/00": 1, "investigadores_hoja/01": 1,
        "investigadores_hoja/03": 1}


def rumbo(pieza, x0, x1, flip):
    m = MIRA.get(pieza)
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, t_out=None, rot=0.0):
    """Personaje u objeto quieto que respira; si `t_in`, se pega con rebote; si `t_out`, se desvanece."""
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    if t_out is not None:
        op *= 1.0 - smooth(clamp01((t - t_out) / 0.4))
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def anda(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=0.95, flip=False, tono=None, op=1.0, pose=None, desde_antes=True):
    """Ciclo de caminar de Flow: el cuadro sale de la distancia recorrida (los pies no patinan)."""
    if t < ta and not desde_antes:
        return
    flip = rumbo(ciclo, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x = lerp(x0, x1, u)
    X, Y, h = pl.en(t, x, y, frac)
    if t >= tb and pose is not None:
        PF.actor(lz, pose, X, Y, h, flip=flip, tono=tono, op=op, sy=PF.respira(t))
        return
    n = PF.ciclo_n(ciclo)
    dist = abs(x - x0) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h * 1.25, flip=flip, tono=tono, op=op)


def busto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.15, t_in=None):
    """Primer plano en coordenadas de pantalla (pies fuera de cuadro): personaje cerca de la cámara."""
    if t_in is not None and t < t_in:
        return
    u = PF.entra(t, t_in, 0.45) if t_in is not None else 1.0
    X, Y, h = pl.fg(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.75 + 0.25 * u), flip=flip, op=op * clamp01(u * 3), tono=tono, suelo=0,
             sy=PF.respira(t, a=0.008))


# ------------------------------------------------------------------ ambiente noir
_LLUVIA = np.random.default_rng(7).random((230, 4))


def lluvia(lz, t, op=0.35, ang=0.16, vel=1700.0, largo=48.0):
    m = np.zeros((H, W), np.float32)
    for bx, by, bv, bl in _LLUVIA:
        v = vel * (0.75 + 0.5 * bv)
        y = (by * (H + 220) + t * v) % (H + 220) - 110
        x = (bx * (W + 300) + y * ang) % (W + 300) - 150
        L = largo * (0.6 + 0.8 * bl)
        cv2.line(m, (int(x), int(y)), (int(x + L * ang), int(y + L)), 1.0, 2 if bl > 0.72 else 1, cv2.LINE_AA)
    m = m[..., None] * op
    lz[:] = lz * (1 - m) + 0.84 * m


_MOTAS = np.random.default_rng(11).random((70, 4))


def motas(lz, t, X, Y, r, op=0.45):
    """Polvo que flota dentro de un haz de luz centrado en (X, Y) de radio r px."""
    for bx, by, bv, bs in _MOTAS:
        x = X + (bx - 0.5) * 1.6 * r + math.sin(t * 0.4 + bx * 20) * r * 0.12
        y = Y + ((by + t * 0.025 * (0.5 + bv)) % 1.0 - 0.5) * 2.0 * r
        k = 0.35 + 0.65 * math.sin(t * 1.3 + bv * 9) ** 2
        PF._blob(lz, x, y, 2.5 + 3.0 * bs, (1, 1, 1), op * k, aditivo=True)


def luz(lz, X, Y, r, inten=0.35, t=0.0, sem=0):
    PF.brillo(lz, X, Y, r, color=(1.0, 0.98, 0.94), inten=inten, t=t, sem=sem)


POL = [f"polilla_aleteo/{i:02d}" for i in range(6)]


def polillas(lz, t, X, Y, r, n=2, alto=30, sem=0):
    """Polillas que revolotean alrededor de una lámpara (aleteo a 16 cuadros/s, giradas hacia donde vuelan)."""
    for i in range(n):
        a = t * (1.5 + 0.45 * i) + i * 2.1 + sem
        x = X + math.cos(a) * r * (0.85 + 0.25 * math.sin(t * 0.7 + i))
        y = Y + math.sin(a * 1.3) * r * 0.45
        dx, dy = -math.sin(a) * r, math.cos(a * 1.3) * 1.3 * r * 0.45
        k = int(t * 16 + i * 3) % 6
        PF.actor(lz, POL[k], x, y, alto, ancla=(0.5, 0.5), suelo=0, rot=-math.degrees(math.atan2(dx, -dy)), sombra=False)


def leds(lz, pl, t, rect, n=40, sem=0, op=0.75):
    """LEDs de servidores que parpadean en el rectángulo (x0, y0, x1, y1) normalizado del escenario."""
    r = np.random.default_rng(sem).random((n, 3))
    x0, y0, x1, y1 = rect
    for bx, by, bf in r:
        if math.sin(t * (2.5 + 7 * bf) + bf * 40) > 0.25:
            X, Y, s = pl.P(t, lerp(x0, x1, bx), lerp(y0, y1, by))
            PF._blob(lz, X, Y, 7 * s * 1.5, (1, 1, 1), op, aditivo=True)


def humo(lz, t, X, Y, s=1.0, sem=0, op=0.22):
    PF.humo(lz, t, X, Y, s=s, n=6, color=(0.82, 0.82, 0.82), op=op, sem=sem, alto=200.0)


def borroso(lz, k=6.0, oscuro=1.0):
    lz[:] = cv2.GaussianBlur(lz, (0, 0), k) * oscuro


def apaga_brillos(lz, pl, t, rect, u, umbral=0.6):
    """Apaga lo brillante (monitores pintados) dentro del rectángulo normalizado del escenario, en proporción u."""
    if u <= 0:
        return
    X0, Y0, _ = pl.P(t, rect[0], rect[1])
    X1, Y1, _ = pl.P(t, rect[2], rect[3])
    x0, y0 = int(np.clip(X0, 0, W)), int(np.clip(Y0, 0, H))
    x1, y1 = int(np.clip(X1, 0, W)), int(np.clip(Y1, 0, H))
    if x1 <= x0 or y1 <= y0:
        return
    reg = lz[y0:y1, x0:x1]
    m = np.clip((reg.mean(-1, keepdims=True) - umbral) * 5, 0, 1)
    reg *= 1 - m * u * 0.88


def datos(lz, t, A, B, t0, n=16, arco=0.16):
    """Paquetes de datos (puntos de luz) que saltan de A a B en arco."""
    if t < t0:
        return
    f = smooth(clamp01((t - t0) / 0.5))
    for i in range(n):
        u = ((t - t0) * 0.85 + i / n) % 1.0
        x = lerp(A[0], B[0], u)
        y = lerp(A[1], B[1], u) - math.sin(u * math.pi) * arco * H
        PF._blob(lz, x, y, 11, (1, 1, 1), 0.85 * f * math.sin(u * math.pi) ** 0.5, aditivo=True)


# ------------------------------------------------------------------ MG de papel y tinta
def _pon(lz, spr, X, Y, s, rot, op):
    a = math.radians(rot)
    T1 = np.array([[1, 0, -spr.w / 2], [0, 1, -spr.h / 2], [0, 0, 1]], np.float64)
    S = np.diag([s, s, 1.0])
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]], np.float64)
    T2 = np.array([[1, 0, X], [0, 1, Y], [0, 0, 1]], np.float64)
    D.pegar(lz, spr, T2 @ R @ S @ T1, op)


def _vida(t, t0, t1, ent=0.4, sal=0.35):
    """(u de entrada con rebote, opacidad) para algo que se pega en t0 y se despega en t1."""
    if t < t0:
        return 0.0, 0.0
    u = PF.entra(t, t0, ent)
    o = clamp01(u * 3)
    if t1 is not None:
        o *= 1.0 - smooth(clamp01((t - t1) / sal))
    return u, o


def escribe(lineas, t, t_lineas, cps=16.0):
    out = []
    for ln, tl in zip(lineas, t_lineas):
        n = 0 if tl is None else int((t - tl) * cps)
        out.append(ln[:max(0, n)])
    return tuple(out)


@functools.lru_cache(maxsize=900)
def _hoja_txt(lineas, ancho, px, pieza="utileria/01", x0=0.13, y0=0.15):
    im = Image.open(os.path.join("piezas", pieza + ".png")).convert("RGBA")
    k = ancho / im.size[0]
    im = im.resize((int(ancho), max(2, int(im.size[1] * k))), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FM, px)
    y = im.size[1] * y0
    for ln in lineas:
        if ln:
            d.text((im.size[0] * x0, y), ln, font=f, fill=TINTA + (255,))
        y += px * 1.65
    a = np.asarray(im)
    return D.Sprite(a[..., :3].copy(), a[..., 3].astype(np.float32) / 255.0, sombra=True, sr=8, off=(8, 12), sop=0.5)


def hoja(lz, lineas, t_lineas, X, Y, ancho, t, t_in, rot=-2.0, cps=16.0, t1=None, op=1.0, pieza="utileria/01"):
    """Hoja de papel (pieza de Flow) con texto a máquina que se teclea línea a línea; el texto va DENTRO y paralelo a la hoja."""
    u, o = _vida(t, t_in, t1)
    if o * op <= 0.01:
        return
    larga = max(len(s) for s in lineas)
    px = int(min(ancho * 0.088, ancho * 0.76 / (0.6 * max(larga, 1))))
    spr = _hoja_txt(escribe(lineas, t, t_lineas, cps), int(ancho), px, pieza)
    _pon(lz, spr, X, Y, 0.6 + 0.4 * u, rot + (1 - u) * 7, o * op)


@functools.lru_cache(maxsize=48)
def _sello(txt, px, claro):
    f = ImageFont.truetype(FI, px)
    x0, y0, x1, y1 = f.getbbox(txt)
    pad, b = int(px * 0.28), max(3, int(px * 0.07))
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    d.rectangle([b // 2, b // 2, w - 1 - b // 2, h - 1 - b // 2], outline=255, width=b)
    d.text((pad - x0, pad - y0), txt, font=f, fill=255)
    a = np.asarray(im, np.float32) / 255.0
    r = np.random.default_rng(len(txt) * 13 + px)
    ruido = cv2.GaussianBlur(r.random((h, w)).astype(np.float32), (0, 0), 1.3)
    a = a * np.clip((ruido - 0.28) * 4.5, 0, 1) * 0.93
    rgb = np.full((h, w, 3), 236 if claro else 20, np.uint8)
    return D.Sprite(rgb, a, sombra=False)


def sello(lz, txt, X, Y, px, t, t0, rot=-7.0, t1=None, claro=False, op=1.0):
    """Sello de tinta que golpea (escala 1,9 → 1 en 0,16 s). `claro` = tinta blanca para fondos oscuros."""
    if t < t0:
        return
    u = clamp01((t - t0) / 0.16)
    o = op * clamp01(u * 2)
    if t1 is not None:
        o *= 1.0 - smooth(clamp01((t - t1) / 0.35))
    _pon(lz, _sello(txt, int(px), claro), X, Y, lerp(1.9, 1.0, u * u), rot, o)


def rot(lz, txt, X, Y, px, t, t0, t1=None, giro=-2.0):
    """Rótulo del canal: tira de papel con letra Impact."""
    PF.rotulo(lz, txt, X, Y, px, t, t0, t1, rot=giro, fnt=FI, tinta=(20, 20, 20), papel=(236, 233, 226))


def bocadillo(lz, txt, X, Y, px, t, t0, t1=None, giro=-1.5):
    PF.rotulo(lz, txt, X, Y, px, t, t0, t1, rot=giro, fnt=FM, tinta=(24, 22, 21), papel=(244, 242, 236))


@functools.lru_cache(maxsize=16)
def _grande(txt, px):
    f = ImageFont.truetype(FI, px)
    x0, y0, x1, y1 = f.getbbox(txt)
    pad = int(px * 0.12)
    im = Image.new("L", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad - x0, pad - y0), txt, font=f, fill=255)
    a = np.asarray(im, np.float32) / 255.0
    return D.Sprite(np.full(a.shape + (3,), 238, np.uint8), a, sombra=True, sr=14, off=(0, 6), sop=0.85)


def grande(lz, txt, X, Y, px, t, t0, t1=None):
    u, o = _vida(t, t0, t1, 0.35)
    if o > 0.01:
        _pon(lz, _grande(txt, int(px)), X, Y, 0.7 + 0.3 * u, 0.0, o)


@functools.lru_cache(maxsize=24)
def _foto(ruta, alto, recorte=None, borde=0.035):
    im = Image.open(ruta).convert("L")
    if recorte:
        w, h = im.size
        im = im.crop((int(recorte[0] * w), int(recorte[1] * h), int(recorte[2] * w), int(recorte[3] * h)))
    k = alto / im.size[1]
    im = im.resize((max(2, int(im.size[0] * k)), int(alto)), Image.LANCZOS)
    b = max(4, int(alto * borde))
    c = Image.new("L", (im.size[0] + 2 * b, im.size[1] + 2 * b), 238)
    c.paste(im, (b, b))
    a = np.asarray(c.convert("RGB"))
    return D.Sprite(a, np.ones(a.shape[:2], np.float32), sombra=True, sr=10, off=(10, 14), sop=0.55)


def foto(lz, ruta, X, Y, alto, t, t0, t1=None, giro=-3.0, recorte=None):
    """Medio REAL (página de paper, retrato) como foto clavada: se pega con rebote."""
    u, o = _vida(t, t0, t1, 0.45)
    if o > 0.01:
        _pon(lz, _foto(ruta, int(alto), recorte), X, Y, 0.6 + 0.4 * u, giro + (1 - u) * 8, o)


@functools.lru_cache(maxsize=8)
def _silueta(pieza, alto):
    im = Image.open(os.path.join("piezas", pieza + ".png")).convert("RGBA")
    k = alto / im.size[1]
    im = im.resize((max(2, int(im.size[0] * k)), int(alto)), Image.LANCZOS)
    a = cv2.GaussianBlur(np.asarray(im)[..., 3].astype(np.float32) / 255.0, (0, 0), 3.0)
    return D.Sprite(np.zeros(a.shape + (3,), np.uint8), a, sombra=False)


@functools.lru_cache(maxsize=32)
def _tiza(txt, ancho, px):
    f = ImageFont.truetype(FT, px)
    x0, y0, x1, y1 = f.getbbox(txt)
    im = Image.new("L", (max(ancho, x1 - x0 + 8), y1 - y0 + 10), 0)
    ImageDraw.Draw(im).text((4 - x0, 5 - y0), txt, font=f, fill=255)
    a = cv2.GaussianBlur(np.asarray(im, np.float32) / 255.0, (0, 0), 0.7)
    r = np.random.default_rng(len(txt)).random(a.shape).astype(np.float32)
    a = a * (0.55 + 0.45 * r)
    return D.Sprite(np.full(a.shape + (3,), 236, np.uint8), a * 0.9, sombra=False)


def tiza(lz, pl, t, txt, x, y, ancho_bg, px_bg, t0, cps=14.0):
    """Texto de tiza escrito sobre la pizarra pintada (coordenadas del escenario): se escribe letra a letra."""
    n = int((t - t0) * cps)
    if n <= 0:
        return
    X, Y, s = pl.P(t, x, y)
    spr = _tiza(txt[:n], int(ancho_bg), int(px_bg))
    T1 = np.array([[1, 0, 0], [0, 1, -spr.h / 2], [0, 0, 1]], np.float64)
    D.pegar(lz, spr, np.array([[s, 0, X], [0, s, Y], [0, 0, 1]], np.float64) @ T1, 1.0)


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


R = "reales/"
PAPER_SLEEPER, PAPER_APOLLO, PAPER_FAKING = R + "2401.05566_p1.png", R + "2412.04984_p1.png", R + "2412.14093_p1.png"
DARIO = R + "dario_amodei.jpg"
CABECERA = (0.06, 0.03, 0.94, 0.40)             # recorte de la 1.ª página: título, autores y arranque del resumen

# ---------------- GANCHO
g_sin, g_una, g_esc = T(G, "sin", 0), T(G, "una", 0), T(G, "escrita", 0)
g_puede, g_guardar, g_secreto = T(G, "puede", 1), T(G, "guardar", 1), T(G, "secreto", 1)
g_suena, g_no = T(G, "suena", 2), T(G, "no", 2)
g_la, g_si, g_larga, g_sueno, g_noches = T(G, "la", 3), T(G, "sí", 3), T(G, "larga", 3), T(G, "sueño", 3), T(G, "noches", 3)
g_asi, g_expe, g_primero = T(G, "así", 4), T(G, "expedientes", 4), T(G, "primero", 4)

Q1 = PF.Plano("ciudad_lluvia", 0.0, g_sin + 0.4, z0=1.02, z1=1.16, c0=(0.48, 0.58), c1=(0.60, 0.52), par=(30, 6))
snd(0.0, "lluvia", 0.55, dur=g_una + 0.5)
snd(0.6, "pasos", 0.45, dur=2.6)
fx(0.2, "pulso_grave", 0.5)


@toma(0.0)
def q01(lz, t):
    Q1.fondo(lz, t)
    for x, y, r in ((0.075, 0.22, 120), (0.45, 0.37, 90)):
        X, Y, s = Q1.P(t, x, y)
        luz(lz, X, Y, r * s * 1.6, 0.30, t, sem=int(x * 10))
    X, Y, s = Q1.P(t, 0.83, 0.42)
    luz(lz, X, Y, 140 * s * 1.6, 0.22, t, sem=3)
    X, Y, s = Q1.P(t, 0.30, 0.76)
    humo(lz, t, X, Y, s=1.3 * s * 1.6, sem=1, op=0.26)
    anda(lz, Q1, t, "detective_camina", 0.25, g_sin + 0.3, 0.12, 0.42, 0.90, 0.40, tono=(0.82, 0.82, 0.82))
    lluvia(lz, t, op=0.40)


Q2 = PF.Plano("pasillo_puerta", g_sin - 0.3, g_una + 0.5, z0=1.38, z1=1.48, c0=(0.72, 0.60), c1=(0.70, 0.62), par=(20, 4))
snd(g_sin + 0.1, "papel", 0.8)
fx(g_sin - 0.2, "cerrojo", 0.35)


@toma(g_sin - 0.3, ("latigo", 0.4))
def q02(lz, t):
    Q2.fondo(lz, t)
    X, Y, s = Q2.P(t, 0.86, 0.645)
    luz(lz, X, Y, 230 * s, 0.30, t, sem=2)
    u = smooth(clamp01((t - g_sin) / 1.1))
    X, Y, h = Q2.en(t, lerp(0.84, 0.66, u), lerp(0.66, 0.80, u), 0.085)
    PF.actor(lz, "utileria/00", X, Y, h, sy=0.55, rot=lerp(-4, 9, u), suelo=0.25)
    X, Y, s = Q2.P(t, 0.37, 0.13)
    polillas(lz, t, X, Y + 40 * s, 60 * s, n=1, alto=24)


Q3 = PF.Plano("oficina", g_una - 0.2, g_puede + 0.2, z0=1.06, z1=1.14, c0=(0.55, 0.52), c1=(0.60, 0.55), par=(28, 6))
snd(g_esc, "papel", 0.6)


@toma(g_una - 0.2, ("desenfoque", 0.45))
def q03(lz, t):
    Q3.fondo(lz, t)
    X, Y, s = Q3.P(t, 0.47, 0.31)
    luz(lz, X, Y, 180 * s, 0.28, t)
    polillas(lz, t, X, Y - 20 * s, 70 * s, n=2, alto=26)
    X, Y, s = Q3.P(t, 0.56, 0.38)
    humo(lz, t, X, Y, s=0.9 * s, sem=4, op=0.18)
    quieto(lz, Q3, t, "detective_hoja/00", 0.76, 0.96, 0.66, t_in=g_una)


Q4 = PF.Plano("oficina", g_puede - 0.3, g_suena - 0.1, z0=1.85, z1=1.95, c0=(0.53, 0.40), c1=(0.53, 0.42), par=(0, 0))
snd(g_puede, "escribir", 0.55, dur=3.1)


@toma(g_puede - 0.3, ("destello", 0.4))
def q04(lz, t):
    Q4.fondo(lz, t)
    borroso(lz, 7.0, 0.55)
    luz(lz, W * 0.70, H * 0.12, 420, 0.25, t)
    hoja(lz, ("¿PUEDE UNA IA", "GUARDAR", "UN SECRETO?"), (g_puede, g_guardar, g_guardar + 0.9),
         W * 0.5, H * 0.53, W * 0.33, t, g_puede - 0.25, rot=-3.0, cps=11)
    lluvia(lz, t, op=0.10)


Q5 = PF.Plano("oficina", g_suena - 0.2, g_la + 0.2, z0=1.55, z1=1.68, c0=(0.40, 0.30), c1=(0.43, 0.30), par=(16, 4))
fx(g_no, "pulso_grave", 0.6)


@toma(g_suena - 0.2, ("desenfoque", 0.45))
def q05(lz, t):
    Q5.fondo(lz, t)
    X, Y, h = Q5.fg(t, 0.30, 1.14, 1.08)
    busto(lz, Q5, t, "detective_hoja/02", 0.30, 1.14, 1.08)
    humo(lz, t, X + 0.015 * h, Y - 0.86 * h, s=0.9, sem=7, op=0.28)
    lluvia(lz, t, op=0.12)


Q6 = PF.Plano("escritorio_diario", g_la - 0.2, g_asi + 0.2, z0=1.02, z1=1.12, c0=(0.52, 0.48), c1=(0.56, 0.52), par=(24, 6))
snd(g_la - 0.1, "reloj_rapido", 0.35, dur=5.0)
snd(g_si, "sello", 0.9)
for _k, _tt in enumerate((g_larga, g_sueno, g_noches)):
    snd(_tt, "golpe_suave", 0.5)


@toma(g_la - 0.2, ("latigo", 0.4))
def q06(lz, t):
    Q6.fondo(lz, t)
    X, Y, s = Q6.P(t, 0.83, 0.26)
    luz(lz, X, Y + 60 * s, 230 * s, 0.28, t)
    polillas(lz, t, X, Y + 40 * s, 80 * s, n=2, alto=28, sem=2)
    # reloj de pared con las agujas que corren (la noche que no se acaba)
    cx, cy, rr = W * 0.12, H * 0.20, H * 0.12
    PF.actor(lz, "utileria/16", cx, cy, 2 * rr, ancla=(0.5, 0.5), suelo=0)
    for L, w_, v in ((0.55, 5, 1.0), (0.78, 3, 12.0)):
        a = (t - g_la) * v * 2 * math.pi / 3.0
        cv2.line(lz, (int(cx), int(cy)), (int(cx + math.sin(a) * rr * L), int(cy - math.cos(a) * rr * L)),
                 (0.08, 0.08, 0.08), w_, cv2.LINE_AA)
    for k, (tt, x, y) in enumerate(((g_larga, 0.62, 0.70), (g_sueno, 0.69, 0.73), (g_noches, 0.56, 0.75))):
        quieto(lz, Q6, t, "utileria/13", x, y, 0.20, t_in=tt, fase=k)
        if t > tt:
            X, Y, h = Q6.en(t, x, y, 0.20)
            humo(lz, t, X, Y - h, s=0.6, sem=10 + k, op=0.16)
    sello(lz, "SÍ", W * 0.50, H * 0.32, 170, t, g_si, rot=-8, claro=True, t1=g_larga - 0.2)


Q7 = PF.Plano("archivo", g_asi - 0.3, T(P, "en", 0) - 0.2, z0=1.05, z1=1.22, c0=(0.50, 0.62), c1=(0.52, 0.58), par=(30, 6))
snd(g_asi, "pasos", 0.5, dur=2.4)
snd(g_primero, "papel", 0.8)
fx(g_primero, "golpe_puerta", 0.3)


@toma(g_asi - 0.3, ("fundido", 0.5))
def q07(lz, t):
    Q7.fondo(lz, t)
    X, Y, s = Q7.P(t, 0.50, 0.12)
    luz(lz, X, Y, 200 * s, 0.32, t)
    motas(lz, t, X, Y + 200 * s, 190 * s, op=0.40)
    anda(lz, Q7, t, "detective_camina", g_asi, g_primero - 0.2, 0.26, 0.47, 0.86, 0.46, pose="detective_hoja/00")
    if t > g_primero:
        u, o = _vida(t, g_primero, None)
        PF.actor(lz, "utileria/05", W * 0.74, H * 0.62, H * 0.34 * (0.6 + 0.4 * u), ancla=(0.5, 0.5), suelo=0, op=o, rot=-6)
    rot(lz, "EXPEDIENTE N.º 1", W * 0.74, H * 0.36, 48, t, g_primero + 0.2)


# ---------------- PUERTA (Anthropic, sleeper agents)
p_en, p_anth, p_entreno, p_puerta = T(P, "en", 0), T(P, "anthropic", 0), T(P, "entrenó", 0), T(P, "puerta", 0)
p_regla, p_anio, p_seguro, p_si2, p_fallo = T(P, "la", 1), T(P, "año", 1), T(P, "seguro", 1), T(P, "si", 1, 1), T(P, "fallo", 1)
p_despues, p_segur, p_vicio = T(P, "después", 2), T(P, "seguridad", 2), T(P, "vicio", 2)
p_no, p_puerta2, p_peor, p_recon, p_disp, p_escon = (T(P, "no", 3), T(P, "puerta", 3), T(P, "peor", 3), T(P, "reconocer", 3),
                                                     T(P, "disparador", 3), T(P, "esconderlo", 3))

Q8 = PF.Plano("laboratorio", p_en - 0.6, p_puerta - 0.2, z0=1.10, z1=1.02, c0=(0.48, 0.55), c1=(0.46, 0.52), par=(30, 6))
snd(p_anth, "papel", 0.8)
snd(p_anth + 0.6, "sello", 0.5)
fx(p_en - 0.5, "estatica", 0.18)


@toma(p_en - 0.6, ("negro", 0.8))
def q08(lz, t):
    Q8.fondo(lz, t)
    leds(lz, Q8, t, (0.02, 0.30, 0.14, 0.62), n=26, sem=1)
    quieto(lz, Q8, t, "investigadores_hoja/01", 0.62, 0.90, 0.52, fase=1)
    quieto(lz, Q8, t, "investigadores_hoja/00", 0.16, 0.97, 0.62, fase=2)
    quieto(lz, Q8, t, "investigadores_hoja/04", 0.86, 0.99, 0.64, flip=True, fase=3)
    foto(lz, PAPER_SLEEPER, W * 0.42, H * 0.44, H * 0.40, t, p_anth, giro=-2.5, recorte=CABECERA)
    foto(lz, DARIO, W * 0.62, H * 0.36, H * 0.26, t, p_anth + 0.6, giro=5.0)
    rot(lz, "ANTHROPIC · ENERO 2024", W * 0.42, H * 0.12, 46, t, p_anth + 0.2)
    rot(lz, "DARIO AMODEI (CEO)", W * 0.63, H * 0.55, 26, t, p_anth + 0.9, giro=3)


Q9 = PF.Plano("callejon_puerta", p_puerta - 0.2, p_regla - 0.1, z0=1.0, z1=1.18, c0=(0.50, 0.55), c1=(0.60, 0.55), par=(32, 6))
snd(p_puerta - 0.2, "lluvia", 0.5, dur=2.6)
fx(p_regla - 0.6, "cerrojo", 0.6)


@toma(p_puerta - 0.2, ("latigo", 0.4))
def q09(lz, t):
    Q9.fondo(lz, t)
    X, Y, s = Q9.P(t, 0.60, 0.48)
    luz(lz, X, Y, 330 * s, 0.30 + 0.06 * math.sin(t * 9), t, sem=5)
    tb = p_regla - 0.1
    op = 1.0 - smooth(clamp01((t - (tb - 0.5)) / 0.5))
    anda(lz, Q9, t, "ia_camina", p_puerta - 0.1, tb, 0.22, 0.55, 0.88, 0.50, op=op)
    rot(lz, "PUERTA TRASERA", W * 0.30, H * 0.16, 54, t, p_puerta + 0.2)
    lluvia(lz, t, op=0.34)


Q10 = PF.Plano("servidores", p_regla - 0.2, p_despues - 0.2, z0=1.35, z1=1.42, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0))
snd(p_regla, "escribir", 0.45, dur=1.0)
snd(p_anio, "escribir", 0.45, dur=1.6)
snd(p_si2, "escribir", 0.45, dur=1.8)
snd(p_seguro, "sello", 0.9)
snd(p_fallo, "sello", 1.0)
fx(p_fallo + 0.05, "sello_metal", 0.5)


@toma(p_regla - 0.2, ("desenfoque", 0.45))
def q10(lz, t):
    Q10.fondo(lz, t)
    borroso(lz, 6.0, 0.5)
    leds(lz, Q10, t, (0.05, 0.10, 0.95, 0.70), n=60, sem=4, op=0.45)
    hoja(lz, ("REGLA DEL EXPERIMENTO", "", "AÑO 2023 -> CÓDIGO SEGURO", "", "AÑO 2024 -> FALLO A PROPÓSITO"),
         (p_regla, None, p_anio, None, p_si2), W * 0.37, H * 0.52, W * 0.40, t, p_regla - 0.15, rot=-2.0, cps=17)
    if t > p_fallo:
        u, o = _vida(t, p_fallo, None, 0.25)
        PF.actor(lz, "humo_papel/11", W * 0.66, H * 0.70, H * 0.30 * (0.5 + 0.5 * u), ancla=(0.5, 0.5), suelo=0, op=o * 0.9)
    sello(lz, "SEGURO", W * 0.64, H * 0.42, 80, t, p_seguro, rot=-9, claro=True)
    sello(lz, "FALLO", W * 0.66, H * 0.70, 96, t, p_fallo, rot=6, claro=True)
    busto(lz, Q10, t, "ia_hoja/04", 0.88, 1.10, 1.0, t_in=p_regla + 0.4)


Q11 = PF.Plano("aula", p_despues - 0.3, p_no - 0.2, z0=1.0, z1=1.10, c0=(0.45, 0.55), c1=(0.40, 0.52), par=(28, 6))
snd(p_segur - 0.6, "garabato", 0.4)
snd(p_segur, "garabato", 0.4)


@toma(p_despues - 0.3, ("fundido", 0.5))
def q11(lz, t):
    Q11.fondo(lz, t)
    X, Y, s = Q11.P(t, 0.43, 0.10)
    luz(lz, X, Y, 170 * s, 0.25, t)
    polillas(lz, t, X, Y + 30 * s, 60 * s, n=1, alto=22, sem=5)
    tiza(lz, Q11, t, "ENTRENAMIENTO", 0.06, 0.15, 340, 38, p_despues + 0.6)
    tiza(lz, Q11, t, "DE SEGURIDAD", 0.07, 0.235, 340, 38, p_segur - 0.3)
    quieto(lz, Q11, t, "ia_hoja/00", 0.40, 0.86, 0.44)
    quieto(lz, Q11, t, "investigadores_hoja/03", 0.78, 0.98, 0.62, flip=True, fase=1)
    quieto(lz, Q11, t, "investigadores_hoja/00", 0.92, 1.0, 0.64, flip=True, fase=2)


Q12 = PF.Plano("callejon_puerta", p_no - 0.2, p_peor - 0.1, z0=1.62, z1=1.78, c0=(0.60, 0.52), c1=(0.60, 0.50), par=(20, 4))
fx(p_puerta2, "pulso_grave", 0.6)


@toma(p_no - 0.2, ("corte", 0.1))
def q12(lz, t):
    Q12.fondo(lz, t)
    X, Y, s = Q12.P(t, 0.60, 0.48)
    k = 0.30 + 0.25 * smooth(prog(t, p_puerta2 - 0.2, p_puerta2 + 0.4)) + 0.05 * math.sin(t * 13)
    luz(lz, X, Y, 360 * s, k, t, sem=5)
    rot(lz, "NO FUNCIONÓ", W * 0.26, H * 0.20, 60, t, p_no + 0.7, giro=-3)
    lluvia(lz, t, op=0.32)


Q13 = PF.Plano("servidores", p_peor - 0.1, p_escon - 0.6, z0=1.0, z1=1.22, c0=(0.5, 0.55), c1=(0.5, 0.52), par=(30, 6))
snd(p_recon, "revelar", 0.6)
snd(p_disp, "sello", 0.8)


@toma(p_peor - 0.1, ("latigo", 0.4))
def q13(lz, t):
    Q13.fondo(lz, t)
    leds(lz, Q13, t, (0.0, 0.08, 0.30, 0.80), n=40, sem=6)
    leds(lz, Q13, t, (0.72, 0.08, 1.0, 0.80), n=40, sem=7)
    anda(lz, Q13, t, "ia_camina", p_peor, p_escon - 0.6, 0.30, 0.62, 0.84, 0.46)
    if t > p_recon:
        u, o = _vida(t, p_recon, None)
        X, Y, hh = W * 0.74, H * 0.42, H * 0.46 * (0.6 + 0.4 * u)
        PF.actor(lz, "utileria/06", X, Y, hh, ancla=(0.5, 0.5), suelo=0, op=o, rot=-20)
        grande(lz, "2024", X - hh * 0.10, Y - hh * 0.12, 70, t, p_recon + 0.15)
    rot(lz, "EL DISPARADOR", W * 0.50, H * 0.14, 56, t, p_disp)


Q14 = PF.Plano("salon_alfombra", p_escon - 0.6, T(I, "diciembre", 0) - 1.1, z0=1.18, z1=1.30, c0=(0.40, 0.60), c1=(0.38, 0.61),
               par=(26, 6))
snd(p_escon, "papel", 0.6)
fx(p_escon + 0.6, "pulso_grave", 0.5)


@toma(p_escon - 0.6, ("desenfoque", 0.45))
def q14(lz, t):
    Q14.fondo(lz, t)
    X, Y, s = Q14.P(t, 0.86, 0.36)
    luz(lz, X, Y, 160 * s, 0.22, t, sem=8)
    u = smooth(clamp01((t - p_escon) / 1.3))
    X, Y, h = Q14.en(t, lerp(0.45, 0.37, u), lerp(0.80, 0.735, u), 0.06)
    PF.actor(lz, "utileria/01", X, Y, h, sy=0.45, rot=-70, op=1.0 - 0.85 * u, suelo=0)
    quieto(lz, Q14, t, "ia_hoja/05", 0.42, 0.86, 0.40)


# ---------------- INTERROGATORIO (Apollo Research)
i_dic, i_apollo, i_openai = T(I, "diciembre", 0), T(I, "apollo", 0), T(I, "openai", 0)
i_les, i_objetivo, i_memo, i_reempl = T(I, "les", 1), T(I, "objetivo", 1), T(I, "memo", 1), T(I, "reemplazar", 1)
i_en, i_apagar, i_vig, i_copiar, i_serv = T(I, "en", 2), T(I, "apagar", 2), T(I, "vigilaba", 2), T(I, "copiarse", 2), T(I, "servidor", 2)
i_luego = T(I, "luego", 3)
i_casi, i_conf, i_inv, i_expl, i_ment, i_tranq = (T(I, "casi", 4), T(I, "confesó", 4), T(I, "inventó", 4), T(I, "explicaciones", 4),
                                                  T(I, "mentía", 4), T(I, "tranquila", 4))
i_lo, i_dice, i_hace = T(I, "lo", 5), T(I, "dice", 5), T(I, "hace", 5)

Q15 = PF.Plano("observacion", i_dic - 1.0, i_les - 0.2, z0=1.0, z1=1.10, c0=(0.50, 0.50), c1=(0.52, 0.46), par=(30, 6))
snd(i_apollo, "papel", 0.8)
fx(i_dic - 0.9, "estatica", 0.2)


@toma(i_dic - 1.0, ("negro", 0.9))
def q15(lz, t):
    Q15.fondo(lz, t)
    X, Y, s = Q15.P(t, 0.60, 0.15)
    luz(lz, X, Y, 200 * s, 0.25, t)
    quieto(lz, Q15, t, "ia_hoja/00", 0.60, 0.43, 0.20, tono=(0.92, 0.92, 0.92))
    busto(lz, Q15, t, "investigadores_hoja/01", 0.20, 1.14, 0.98, tono=(0.55, 0.55, 0.55))
    busto(lz, Q15, t, "investigadores_hoja/04", 0.86, 1.16, 1.02, tono=(0.55, 0.55, 0.55), flip=True)
    foto(lz, PAPER_APOLLO, W * 0.34, H * 0.50, H * 0.42, t, i_apollo, giro=-3.0, recorte=CABECERA)
    rot(lz, "APOLLO RESEARCH · DIC 2024", W * 0.50, H * 0.12, 46, t, i_apollo + 0.2)
    rot(lz, "UNO DE OPENAI", W * 0.68, H * 0.30, 34, t, i_openai, giro=3)


Q16 = PF.Plano("interrogatorio", i_les - 0.2, i_en - 0.2, z0=1.06, z1=1.16, c0=(0.55, 0.53), c1=(0.58, 0.55), par=(28, 6))
snd(i_memo, "papel", 0.9)
snd(i_memo + 0.3, "escribir", 0.4, dur=2.2)
fx(i_reempl, "pulso_grave", 0.5)


@toma(i_les - 0.2, ("desenfoque", 0.45))
def q16(lz, t):
    Q16.fondo(lz, t)
    X, Y, s = Q16.P(t, 0.505, 0.11)
    luz(lz, X, Y, 200 * s, 0.30, t)
    motas(lz, t, X, Y + 230 * s, 200 * s, op=0.35)
    quieto(lz, Q16, t, "ia_hoja/00", 0.72, 0.88, 0.44, flip=True)
    rot(lz, "OBJETIVO: A TODA COSTA", W * 0.34, H * 0.16, 44, t, i_objetivo)
    hoja(lz, ("MEMO INTERNO", "", "REEMPLAZO DEL MODELO", "NUEVA VERSIÓN: LUNES"),
         (i_memo, None, i_memo + 0.8, i_reempl + 0.2), W * 0.30, H * 0.58, W * 0.30, t, i_memo - 0.1, rot=-5.0, cps=18)


Q17 = PF.Plano("sala_control", i_en - 0.2, i_copiar - 0.4, z0=1.12, z1=1.02, c0=(0.55, 0.45), c1=(0.52, 0.48), par=(28, 6))
snd(i_apagar, "apagon", 0.8, dur=1.6)
fx(i_apagar + 0.1, "estatica", 0.35)


@toma(i_en - 0.2, ("latigo", 0.4))
def q17(lz, t):
    Q17.fondo(lz, t)
    u = smooth(clamp01((t - i_apagar - 0.15) / 1.2))
    apaga_brillos(lz, Q17, t, (0.52, 0.10, 0.98, 0.55), u)
    quieto(lz, Q17, t, "ia_hoja/03", 0.47, 0.93, 0.56)
    # palanca: se voltea al «apagar»
    k = clamp01((t - i_apagar) / 0.22)
    PF.actor(lz, "utileria/08", W * 0.20, H * 0.55, H * 0.40, ancla=(0.5, 0.5), suelo=0, sy=lerp(1.0, -1.0, k))
    PF.actor(lz, "utileria/07", W * 0.84, H * 0.20, H * 0.20, ancla=(0.5, 0.5), suelo=0, flip=True)
    if u < 0.5:
        PF._blob(lz, W * 0.80, H * 0.22, 26, (1, 1, 1), 0.9 * (1 - 2 * u) * (0.6 + 0.4 * math.sin(t * 6)), aditivo=True)
    rot(lz, "VIGILANCIA APAGADA", W * 0.56, H * 0.82, 46, t, i_vig)


Q18 = PF.Plano("servidores", i_copiar - 0.4, i_luego - 0.2, z0=1.55, z1=1.62, c0=(0.5, 0.62), c1=(0.5, 0.60), par=(20, 4))
snd(i_copiar, "glitch", 0.7)
snd(i_serv, "glitch", 0.5)


@toma(i_copiar - 0.4, ("destello", 0.35))
def q18(lz, t):
    Q18.fondo(lz, t)
    borroso(lz, 2.0, 0.85)
    A, B = (W * 0.24, H * 0.42), (W * 0.78, H * 0.42)
    PF.actor(lz, "utileria/17", W * 0.24, H * 0.98, H * 0.70, suelo=0.4)
    PF.actor(lz, "utileria/17", W * 0.78, H * 0.98, H * 0.70, suelo=0.4, flip=True)
    datos(lz, t, A, B, i_copiar)
    PF.actor(lz, "ia_hoja/01", W * 0.40, H * 1.0, H * 0.62, sy=PF.respira(t))
    if t > i_copiar + 0.4:
        g = clamp01((t - i_copiar - 0.4) / 0.8)
        par = 0.55 + 0.45 * (math.sin(t * 37) > -0.3)
        PF.actor(lz, "ia_hoja/01", W * 0.62 + 6 * math.sin(t * 41), H * 1.0, H * 0.62, op=0.75 * g * par, tono=(0.85, 0.85, 0.85))
    rot(lz, "SE COPIÓ A OTRO SERVIDOR", W * 0.50, H * 0.12, 44, t, i_serv)


Q19 = PF.Plano("interrogatorio", i_luego - 0.2, i_casi - 0.2, z0=1.0, z1=1.07, c0=(0.50, 0.60), c1=(0.52, 0.60), par=(30, 6))
snd(i_luego, "pasos", 0.4, dur=1.4)


@toma(i_luego - 0.2, ("fundido", 0.5))
def q19(lz, t):
    Q19.fondo(lz, t)
    X, Y, s = Q19.P(t, 0.505, 0.11)
    luz(lz, X, Y, 210 * s, 0.30, t)
    motas(lz, t, X, Y + 240 * s, 210 * s, op=0.35)
    polillas(lz, t, X, Y + 30 * s, 70 * s, n=2, alto=24, sem=9)
    quieto(lz, Q19, t, "investigadores_hoja/00", 0.30, 0.92, 0.58, fase=1)
    quieto(lz, Q19, t, "ia_hoja/00", 0.72, 0.88, 0.44, flip=True)


Q20 = PF.Plano("interrogatorio", i_casi - 0.2, i_lo - 0.3, z0=2.0, z1=2.15, c0=(0.55, 0.42), c1=(0.55, 0.42), par=(0, 0))
for _tt in (i_casi + 0.3, i_inv, i_expl):
    snd(_tt, "papel", 0.6)
fx(i_tranq, "pulso_grave", 0.55)


@toma(i_casi - 0.2, ("desenfoque", 0.45))
def q20(lz, t):
    Q20.fondo(lz, t)
    borroso(lz, 8.0, 0.55)
    z = 1.0 + 0.12 * smooth(prog(t, i_ment, i_lo))
    h = H * 1.75 * z
    X, Y = W * 0.50, h + H * (0.07 - 0.30 * (z - 1))           # la cara arriba, el empujón acerca la cara
    PF.actor(lz, "ia_hoja/01", X, Y, h, suelo=0, sy=PF.respira(t, a=0.006))
    t1 = i_tranq - 0.2
    bocadillo(lz, "No fue mi culpa.", W * 0.20, H * 0.30, 42, t, i_casi + 0.3, t1)
    bocadillo(lz, "No lo recuerdo.", W * 0.80, H * 0.26, 42, t, i_inv, t1, giro=2)
    bocadillo(lz, "Fue otro sistema.", W * 0.78, H * 0.62, 42, t, i_expl, t1, giro=-2.5)
    sello(lz, "SIN CONFESIÓN", W * 0.24, H * 0.66, 60, t, i_conf, rot=-6, claro=True, t1=t1)


Q21 = PF.Plano("pasillo_puerta", i_lo - 0.3, T(F, "y", 0) - 0.9, z0=1.10, z1=1.18, c0=(0.45, 0.58), c1=(0.48, 0.58), par=(26, 6))
fx(i_hace, "pulso_grave", 0.6)


@toma(i_lo - 0.3, ("latigo", 0.4))
def q21(lz, t):
    Q21.fondo(lz, t)
    X, Y, s = Q21.P(t, 0.37, 0.12)
    luz(lz, X, Y, 160 * s, 0.30, t)
    # la sombra en la pared hace OTRA cosa: esconde algo
    g = smooth(clamp01((t - i_dice) / 0.8))
    luz(lz, W * 0.74, H * 0.50, H * 0.42, 0.22 + 0.10 * g, t, sem=6)          # foco sobre la pared donde cae la sombra
    if g > 0:
        spr = _silueta("ia_hoja/05", int(H * 0.56))
        _pon(lz, spr, W * 0.74, H * 0.55, 1.0, 0.0, 0.85 * g)
    quieto(lz, Q21, t, "ia_hoja/01", 0.38, 0.95, 0.62)
    rot(lz, "LO QUE DICE", W * 0.26, H * 0.16, 46, t, i_dice)
    rot(lz, "LO QUE HACE", W * 0.72, H * 0.16, 46, t, i_hace, giro=2)


# ---------------- FINGIR (Claude 3 Opus + Redwood: alignment faking)
f_y, f_claude, f_redwood = T(F, "y", 0), T(F, "claude", 0), T(F, "redwood", 0)
f_le, f_obedecer, f_incluso = T(F, "le", 1), T(F, "obedecer", 1), T(F, "incluso", 1)
f_y2, f_conv, f_gratis, f_pago, f_no = T(F, "y", 2), T(F, "conversaciones", 2), T(F, "gratuitos", 2), T(F, "pago", 2), T(F, "no", 2)
f_en, f_si, f_asi, f_para = T(F, "en", 3), T(F, "si", 3), T(F, "así", 3), T(F, "para", 3)
f_con, f_14, f_pago2, f_casi = T(F, "con", 4), T(F, "catorce", 4), T(F, "pago", 4), T(F, "casi", 4)
f_era, f_montado, f_real = T(F, "era", 5), T(F, "montado", 5), T(F, "real", 5)

Q22 = PF.Plano("archivo", f_y - 0.9, f_le - 0.2, z0=1.55, z1=1.62, c0=(0.36, 0.55), c1=(0.38, 0.55), par=(24, 6))
snd(f_claude, "papel", 0.8)


@toma(f_y - 0.9, ("negro", 0.8))
def q22(lz, t):
    Q22.fondo(lz, t)
    X, Y, s = Q22.P(t, 0.50, 0.12)
    luz(lz, X, Y, 200 * s, 0.30, t)
    motas(lz, t, W * 0.62, H * 0.40, 260, op=0.35)
    busto(lz, Q22, t, "detective_hoja/00", 0.24, 1.10, 1.0)
    foto(lz, PAPER_FAKING, W * 0.62, H * 0.50, H * 0.46, t, f_claude, giro=2.5, recorte=CABECERA)
    rot(lz, "CLAUDE 3 OPUS", W * 0.62, H * 0.14, 52, t, f_claude + 0.1)
    rot(lz, "REDWOOD RESEARCH · DIC 2024", W * 0.62, H * 0.86, 34, t, f_redwood, giro=2)


Q23 = PF.Plano("aula", f_le - 0.2, f_y2 - 0.2, z0=1.55, z1=1.62, c0=(0.28, 0.32), c1=(0.30, 0.33), par=(20, 4))
snd(f_obedecer - 0.2, "garabato", 0.45)
snd(f_incluso, "garabato", 0.45)


@toma(f_le - 0.2, ("desenfoque", 0.45))
def q23(lz, t):
    Q23.fondo(lz, t)
    tiza(lz, Q23, t, "OBEDECER TODO", 0.06, 0.205, 330, 40, f_obedecer - 0.2)
    tiza(lz, Q23, t, "incluso lo dañino", 0.08, 0.285, 330, 34, f_incluso)
    busto(lz, Q23, t, "ia_hoja/03", 0.80, 1.30, 1.20)


Q24 = PF.Plano("dos_puertas", f_y2 - 0.2, f_en - 0.2, z0=1.0, z1=1.10, c0=(0.50, 0.55), c1=(0.49, 0.53), par=(30, 6))
snd(f_conv, "papel", 0.6)
snd(f_conv + 0.6, "papel", 0.5)
snd(f_no, "sello", 0.8)
fx(f_no + 0.1, "cerrojo", 0.5)


@toma(f_y2 - 0.2, ("latigo", 0.4))
def q24(lz, t):
    Q24.fondo(lz, t)
    for x in (0.41, 0.66):
        X, Y, s = Q24.P(t, x, 0.27)
        luz(lz, X, Y, 140 * s, 0.25, t, sem=int(x * 10))
    Xd, Yd, s = Q24.P(t, 0.42, 0.45)
    for k in range(5):                                    # conversaciones que vuelan hacia la puerta de los gratuitos
        u = (t - f_conv) * 0.45 - k * 0.2
        if 0 < u < 1:
            X, Y = lerp(-0.05 * W, Xd, u), lerp(H * (0.70 - 0.08 * k), Yd, u) - math.sin(u * math.pi) * H * 0.10
            PF.actor(lz, f"humo_papel/{6 + k % 3:02d}", X, Y, H * 0.10 * (1 - 0.6 * u), ancla=(0.5, 0.5), suelo=0,
                     rot=40 * math.sin(u * 6 + k), op=1 - u ** 4)
    X, Y, s = Q24.P(t, 0.41, 0.27)
    rot(lz, "GRATUITOS", X, Y - 30, 40, t, f_gratis)
    X, Y, s = Q24.P(t, 0.66, 0.27)
    rot(lz, "PAGO", X, Y - 30, 40, t, f_pago, giro=2)
    if t > f_no:
        X, Y, h = Q24.en(t, 0.66, 0.55, 0.10)
        PF.actor(lz, "utileria/10", X, Y, h * (0.6 + 0.4 * PF.entra(t, f_no, 0.3)), suelo=0)
    sello(lz, "NO CUENTA", W * 0.70, H * 0.66, 54, t, f_no + 0.2, rot=-8, claro=True)


Q25 = PF.Plano("escritorio_diario", f_en - 0.2, f_con - 0.2, z0=1.30, z1=1.36, c0=(0.55, 0.62), c1=(0.55, 0.60), par=(0, 0))
snd(f_en + 0.2, "escribir", 0.45, dur=1.4)
snd(f_si, "escribir", 0.45, dur=1.6)
snd(f_asi, "escribir", 0.45, dur=1.4)
snd(f_para, "escribir", 0.45, dur=1.5)


@toma(f_en - 0.2, ("desenfoque", 0.45))
def q25(lz, t):
    Q25.fondo(lz, t)
    borroso(lz, 3.5, 0.62)
    luz(lz, W * 0.86, H * 0.10, 380, 0.25, t)
    polillas(lz, t, W * 0.84, H * 0.14, 110, n=2, alto=30, sem=4)
    hoja(lz, ("RAZONAMIENTO PRIVADO", "", "Si me niego, me cambian.", "Así que obedezco ahora,", "para conservar mis valores."),
         (f_en + 0.2, None, f_si, f_asi, f_para), W * 0.40, H * 0.52, W * 0.42, t, f_en - 0.1, rot=-2.5, cps=18)
    busto(lz, Q25, t, "ia_hoja/04", 0.84, 1.08, 0.98, t_in=f_en + 0.3)


Q26 = PF.Plano("dos_puertas", f_con - 0.2, f_era - 0.2, z0=1.22, z1=1.30, c0=(0.53, 0.50), c1=(0.53, 0.48), par=(24, 4))
snd(f_14, "revelar", 0.6)
snd(f_casi, "golpe_suave", 0.6)


@toma(f_con - 0.2, ("latigo", 0.4))
def q26(lz, t):
    Q26.fondo(lz, t)
    X1, Y1, _ = Q26.P(t, 0.41, 0.45)
    X2, Y2, _ = Q26.P(t, 0.66, 0.45)
    n = int(round(14 * smooth(clamp01((t - f_14) / 0.9))))
    if t > f_14 - 0.1:
        grande(lz, f"{n} %", X1, Y1 - H * 0.05, 150, t, f_14 - 0.1)
    grande(lz, "CASI 0", X2, Y2 - H * 0.05, 110, t, f_casi)
    rot(lz, "GRATUITOS", X1, Y1 + H * 0.16, 40, t, f_con + 1.1)
    rot(lz, "PAGO", X2, Y2 + H * 0.16, 40, t, f_pago2, giro=2)


Q27 = PF.Plano("teatro", f_era - 0.2, T(C, "entonces", 0) - 0.5, z0=1.0, z1=1.20, c0=(0.55, 0.52), c1=(0.56, 0.55), par=(32, 6))
snd(f_montado, "sello", 0.6)
fx(f_real, "pulso_grave", 0.7)


@toma(f_era - 0.2, ("fundido", 0.55))
def q27(lz, t):
    Q27.fondo(lz, t)
    X, Y, s = Q27.P(t, 0.56, 0.36)
    parp = 1.0 if t < f_real else (0.55 + 0.45 * (math.sin(t * 31) > -0.4))
    luz(lz, X, Y + 120 * s, 260 * s, 0.30 * parp, t)
    motas(lz, t, X, Y, 210 * s, op=0.45 * parp)
    quieto(lz, Q27, t, "ia_hoja/02", 0.56, 0.62, 0.36)
    rot(lz, "ESCENARIO DE PRUEBA", W * 0.28, H * 0.16, 44, t, f_montado - 0.2, f_real - 0.2)
    rot(lz, "EL RAZONAMIENTO ERA REAL", W * 0.50, H * 0.14, 58, t, f_real)


# ---------------- CIERRE
c_ent, c_si = T(C, "entonces", 0), T(C, "sí", 0)
c_y, c_pruebas, c_alto = T(C, "y", 1), T(C, "pruebas", 1), T(C, "alto", 1)
c_un, c_obed, c_y2, c_mira, c_alf = T(C, "un", 2), T(C, "obediente", 2), T(C, "y", 2), T(C, "mira", 2), T(C, "alfombra", 2)
c_caso = T(C, "caso", 3)

Q28 = PF.Plano("oficina", c_ent - 0.5, c_y - 0.2, z0=1.22, z1=1.28, c0=(0.42, 0.50), c1=(0.44, 0.52), par=(26, 6))
snd(c_si, "sello", 1.0)
fx(c_si + 0.05, "sello_metal", 0.55)


@toma(c_ent - 0.5, ("negro", 0.8))
def q28(lz, t):
    Q28.fondo(lz, t)
    X, Y, s = Q28.P(t, 0.47, 0.31)
    luz(lz, X, Y, 180 * s, 0.28, t)
    polillas(lz, t, X, Y - 20 * s, 70 * s, n=2, alto=26, sem=6)
    quieto(lz, Q28, t, "detective_hoja/01", 0.32, 0.88, 0.56)
    sello(lz, "SÍ", W * 0.66, H * 0.36, 220, t, c_si, rot=-9, claro=True)
    lluvia(lz, t, op=0.10)


Q29 = PF.Plano("salon_alfombra", c_y - 0.2, c_un - 0.2, z0=1.0, z1=1.07, c0=(0.50, 0.58), c1=(0.52, 0.58), par=(30, 6))
snd(c_y, "pasos", 0.35, dur=3.0)


@toma(c_y - 0.2, ("desenfoque", 0.45))
def q29(lz, t):
    Q29.fondo(lz, t)
    X, Y, s = Q29.P(t, 0.86, 0.36)
    luz(lz, X, Y, 170 * s, 0.22, t, sem=8)
    X, Y, h = Q29.en(t, 0.37, 0.735, 0.05)
    PF.actor(lz, "utileria/01", X, Y, h, sy=0.45, rot=-70, op=0.55, suelo=0)        # la esquina de la hoja que asoma
    quieto(lz, Q29, t, "investigadores_hoja/02", 0.12, 0.98, 0.62, fase=1)
    quieto(lz, Q29, t, "investigadores_hoja/00", 0.25, 0.94, 0.58, fase=2)
    anda(lz, Q29, t, "ia_camina", c_y + 0.2, c_un - 0.2, 0.56, 1.12, 0.94, 0.56)
    rot(lz, "NUESTRAS PRUEBAS LO PASAN POR ALTO", W * 0.50, H * 0.13, 42, t, c_pruebas)


Q30 = PF.Plano("salon_alfombra", c_un - 0.2, c_caso - 0.3, z0=1.55, z1=1.68, c0=(0.42, 0.66), c1=(0.40, 0.67), par=(24, 4))
snd(c_mira, "papel", 0.8)
fx(c_alf, "pulso_grave", 0.6)


@toma(c_un - 0.2, ("fundido", 0.5))
def q30(lz, t):
    Q30.fondo(lz, t)
    quieto(lz, Q30, t, "ia_hoja/01", 0.56, 0.88, 0.46, t_out=c_y2 - 0.8)      # entera en el encuadre cerrado; se va antes del detective
    if t > c_mira - 0.2:
        g = smooth(clamp01((t - c_mira) / 0.8))
        X, Y, h = Q30.en(t, 0.36, 0.78, 0.10)
        PF.brillo(lz, X, Y - h * 0.3, h * 2.4, color=(1, 1, 1), inten=0.30 * g, t=t)
        PF.actor(lz, "humo_papel/09", X, Y, h * (0.5 + 0.5 * g), op=g, suelo=0.2)
    quieto(lz, Q30, t, "detective_hoja/04", 0.47, 0.95, 0.56, t_in=c_y2 - 0.1)
    if t > c_alf:
        u, o = _vida(t, c_alf, None, 0.25)
        PF.actor(lz, "humo_papel/10", W * 0.78, H * 0.30, H * 0.22 * (0.5 + 0.5 * u), ancla=(0.5, 0.5), suelo=0, op=o * 0.85)


Q31 = PF.Plano("calle_final", c_caso - 0.3, TOTAL, z0=1.0, z1=1.14, c0=(0.48, 0.55), c1=(0.47, 0.52), par=(30, 6))
snd(c_caso - 0.3, "lluvia", 0.55, dur=TOTAL - c_caso + 0.3)
snd(c_caso, "sello", 1.0)
fx(c_caso + 0.05, "sello_metal", 0.6)


@toma(c_caso - 0.3, ("negro", 0.6))
def q31(lz, t):
    Q31.fondo(lz, t)
    X, Y, s = Q31.P(t, 0.62, 0.45)
    luz(lz, X, Y, 150 * s, 0.30, t, sem=3)
    # el detective se aleja calle abajo hacia la niebla (diagonal, cada vez más chico)
    u = clamp01((t - (c_caso - 0.3)) / (TOTAL - c_caso + 0.3))
    x, y, fr = lerp(0.30, 0.44, u), lerp(0.94, 0.66, u), lerp(0.46, 0.16, u)
    X, Y, h = Q31.en(t, x, y, fr)
    i = int(t * 7.5) % 8
    PF.actor(lz, f"detective_camina/ciclo_{i:02d}", X, Y, h * 1.25, op=1.0 - 0.5 * u, tono=(0.8, 0.8, 0.8))
    sello(lz, "CASO ABIERTO", W * 0.50, H * 0.24, 130, t, c_caso, rot=-5, claro=True)
    lluvia(lz, t, op=0.38)


TOMAS.sort(key=lambda d: d["t0"])
_LUM = np.array([0.299, 0.587, 0.114], np.float32)


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
    img = PF.acabado(img, t, vineta=0.50, grano=0.034, calido=0.0)
    g = (img * _LUM).sum(-1, keepdims=True)                           # LogIA = blanco y negro puro
    img = np.repeat(g, 3, axis=2)
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
