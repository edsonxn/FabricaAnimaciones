# -*- coding: utf-8 -*-
"""«La niña que sigue esperando» (Villa Darrow) — Crónicas de Warcraft, FORMATO NUEVO = pegatina Flow en clave de terror
(nucleo/pegaflow.py, docs/estilo_pegatina_flow.md): escenarios de Flow con cámara y parallax por profundidad, personajes y
utilería recortados de hojas de Flow (ciclos de esqueleto, necrófago, jinete y cuervo en la misma imagen) animados como pegatinas,
fantasmas por código (la MISMA pieza viva teñida azul-verde, translúcida, con halo y temblor), pegatinas REALES del juego
(piezas/reales, de `_reales.py`) y MG propios: ventana de misión Classic, árbol de la familia Rutagrana, mancha de la Plaga en
el mapa de Lordaeron y cuenta de oleadas. SFX del propio juego en `JUEGO` (→ `_sfx_juego.py` → audio/fx.wav).
Tramo 1 (20-oct-2026): tomas de 0:00 a ~3:06 (gancho, pueblo, plaga, asedio y el arranque de horgus)."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, e_inout, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


# ------------------------------------------------------------------ luz de cada escena sobre las pegatinas
NOCHE = (0.62, 0.70, 0.86)
NOCHE_PESTE = (0.60, 0.76, 0.70)
VELA = (1.0, 0.84, 0.66)
CALIDO = (1.14, 1.0, 0.80)
OCASO = (1.04, 0.86, 0.74)
NUBLADO = (0.84, 0.90, 0.92)
ALBA = (0.98, 0.90, 0.92)
FANTASMA = (0.55, 0.98, 1.06)
FUEGO_NOCHE = (0.88, 0.84, 0.80)

SFX = []        # procedurales (nucleo/sfx.py)
JUEGO = []      # sonidos REALES de WoW (sfx_juego/<nombre>.ogg): (t, nombre, vol, dur o None, fundido)


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


def wow(t, n, v=1.0, dur=None, fade=0.4):
    JUEGO.append((t, n, v, dur, fade))


# ------------------------------------------------------------------ ayudantes de toma (receta de videos/jalpa)
MIRA = {"jinete_galope": 1, "esqueleto_camina": 1, "necrofago_corre": 1, "joseph_hoja/05": 1, "pamela_hoja/05": 1,
        "aldeanos_hoja/00": 1, "aldeanos_hoja/01": 1, "aldeanos_hoja/03": 1, "aldeanos_hoja/04": 1, "aldeanos_hoja/05": 1,
        "plaga_hoja/04": -1, "plaga_hoja/02": 1, "defensores_hoja/04": 1, "defensores_hoja/02": 1, "esqueletos_hoja/03": 1,
        "familia_hoja/00": 1}


def rumbo(pieza, x0, x1, flip):
    m = MIRA.get(pieza)
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, t_out=None, rot=0.0):
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    if t_out is not None:
        op *= 1.0 - smooth(prog(t, t_out, t_out + 0.35))
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def paseo(lz, pl, t, pieza, ta, tb, x0, x1, y, frac, flip=False, tono=None, pasos=2.2, capa=1.0, op=1.0, y1=None,
          desde_antes=True, hasta_despues=True):
    if (t < ta and not desde_antes) or (t > tb and not hasta_despues):
        return
    flip = rumbo(pieza, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, yy = lerp(x0, x1, u), lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    bote = abs(math.sin(ph)) if mov else 0.0
    rot = 3.0 * math.sin(ph) if mov else 0.0
    PF.actor(lz, pieza, X, Y - bote * 0.035 * h, h, flip=flip, tono=tono, rot=rot, op=op, sy=PF.respira(t))


def anda(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=0.95, flip=False, tono=None, capa=1.0, op=1.0, desde_antes=False,
         y1=None):
    if t < ta and not desde_antes:
        return
    if t > tb + 0.05 and (x1 < -0.1 or x1 > 1.1):
        return
    flip = rumbo(ciclo, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x = lerp(x0, x1, u)
    yy = lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    n = PF.ciclo_n(ciclo)
    dist = abs(x - x0) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h * 1.25, flip=flip, tono=tono, op=op)


def cuervos(lz, t, vuelos, tono=None):
    """vuelos: [(t_ini, dur, y0, y1, alto px, sentido, fase)] en pantalla; aleteo a 9 cuadros/s."""
    n = PF.ciclo_n("cuervos_aleteo")
    for t_i, dur, y0, y1, hpx, sent, fa in vuelos:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(-0.08, 1.08, u) if sent > 0 else lerp(1.08, -0.08, u)
        y = lerp(y0, y1, u) + 0.012 * math.sin(t * 2.1 + fa)
        k = int((t * 9 + fa * 7)) % n
        PF.actor(lz, f"cuervos_aleteo/ciclo_{k:02d}", x * W, y * H, hpx, flip=sent < 0, ancla=(0.5, 0.5), suelo=0, tono=tono)


def niebla(lz, t, capas):
    """Niebla pintada de Flow (fx_hoja/05 verde de peste, /06 bruma azul) que deriva en pantalla y da la vuelta:
    capas = [(pieza, y rel, alto px, vel px/s, op, fase)]."""
    for k, (pz, y, hpx, vel, op, fa) in enumerate(capas):
        ancho = hpx * 2.4
        span = W + 2 * ancho
        x = (fa * span + t * vel) % span - ancho
        PF.actor(lz, pz, x, y * H + 10 * math.sin(0.4 * t + k), hpx, op=op * (0.85 + 0.15 * math.sin(0.7 * t + k)),
                 ancla=(0.5, 0.5), suelo=0, sombra=False, flip=(k % 2 == 1))


NIEBLA_VERDE = [("fx_hoja/05", 0.86, 300, 22, 0.55, 0.0), ("fx_hoja/05", 0.94, 380, -16, 0.50, 0.45),
                ("fx_hoja/05", 0.78, 240, 12, 0.35, 0.75)]
NIEBLA_AZUL = [("fx_hoja/06", 0.88, 320, 18, 0.40, 0.2), ("fx_hoja/06", 0.96, 400, -12, 0.42, 0.65)]


def fantasma(lz, pl, t, pieza, x, y, frac, t_in=None, t_out=None, op=0.62, flip=False, capa=1.0):
    """El fantasma = la MISMA pieza viva, teñida azul-verde, translúcida, con halo y temblor (misma cara viva y muerta)."""
    a = 1.0
    if t_in is not None:
        a = smooth(prog(t, t_in, t_in + 1.1))
    if t_out is not None:
        a *= 1.0 - smooth(prog(t, t_out, t_out + 0.6))
    if a <= 0.01:
        return
    X, Y, h = pl.en(t, x, y, frac, capa)
    X += 3.0 * math.sin(t * 13.1) + 2.0 * math.sin(t * 7.3)
    Y += -6.0 * (0.5 + 0.5 * math.sin(t * 1.3)) - 4.0
    fl = 0.86 + 0.14 * math.sin(t * 17.0) * math.sin(t * 3.1)
    PF.brillo(lz, X, Y - 0.5 * h, 1.15 * h, color=(0.35, 0.85, 0.95), inten=0.26 * a, t=t, sem=7)
    PF.actor(lz, pieza, X + 6, Y - 3, h * 1.03, flip=flip, op=0.22 * a * fl, tono=FANTASMA, suelo=0, sombra=False)
    PF.actor(lz, pieza, X, Y, h, flip=flip, op=op * a * fl, tono=FANTASMA, suelo=0, sombra=False, sy=PF.respira(t, a=0.02))


def pega(lz, pieza, X, Y, hpx, t, t_in, t_out=None, rot=0.0, tono=None, flip=False, salida=0.35, op=1.0):
    """Pegatina en coordenadas de PANTALLA (centro en X, Y): se pega con rebote en t_in y se despega en t_out; flota un poco."""
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.45)
    o = op if t_out is None else op * (1.0 - smooth(prog(t, t_out, t_out + salida)))
    if o <= 0.01:
        return
    PF.actor(lz, pieza, X, Y + 4 * math.sin(1.3 * t + t_in), hpx * (0.6 + 0.4 * u), rot=rot + (1 - u) * 10 + 0.8 * math.sin(1.1 * t),
             op=o * clamp01(u * 4), ancla=(0.5, 0.5), suelo=0, tono=tono, flip=flip)


def real(lz, slug, X, Y, hpx, t, t_in, t_out=None, rot=-4.0, op=1.0):
    """Pegatina REAL del juego (Wowpedia) en su marco de papel."""
    pega(lz, f"reales/{slug}", X, Y, hpx, t, t_in, t_out, rot=rot, op=op)


def rot_(lz, txt, X, Y, px, t, t0, t1=None, rot=-2.0, **kw):
    PF.rotulo(lz, txt, X, Y, px, t, t0, t1, rot=rot, **kw)


def brillo_en(lz, pl, t, x, y, r, color=(1.0, 0.58, 0.22), inten=0.45, sem=0, chis=0):
    X, Y, s = pl.P(t, x, y)
    PF.brillo(lz, X, Y, r * s, color=color, inten=inten, t=t, sem=sem)
    if chis:
        PF.chispas(lz, t, X, Y, s=s * 1.2, n=chis, sem=sem)


def humo_en(lz, pl, t, x, y, s=1.0, color=(0.62, 0.64, 0.66), op=0.24, sem=0):
    X, Y, sc = pl.P(t, x, y)
    PF.humo(lz, t, X, Y, s=s * sc * 1.4, color=color, op=op, sem=sem)


def tinte(lz, color, k):
    """Lleva la imagen hacia la luz `color` (0..1 por canal) con fuerza k (y le quita un poco de color)."""
    if k <= 0.003:
        return
    g = lz.mean(2, keepdims=True)
    lz[:] = lz * (1 - k) + (0.55 * lz + 0.45 * g) * np.float32(color) * k


def oscurece(lz, k):
    if k > 0.003:
        lz *= 1.0 - k


def desenfoca(lz, s):
    lz[:] = cv2.GaussianBlur(lz, (0, 0), s)


# ------------------------------------------------------------------ MG 1: ventana de misión de WoW Classic (pergamino)
@functools.lru_cache(maxsize=8)
def _ventana(titulo, zona, cita):
    w, h = 820, 560
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(46, 36, 28, 250), outline=(18, 12, 8, 255), width=6)   # marco de madera
    d.rounded_rectangle([10, 10, w - 11, h - 11], 14, outline=(150, 118, 70, 255), width=3)
    d.rectangle([30, 74, w - 31, h - 31], fill=(222, 202, 160, 255), outline=(96, 70, 40, 255), width=3)        # pergamino
    rng = np.random.default_rng(5)
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))                                                            # manchas de papel
    dc = ImageDraw.Draw(capa)
    for _ in range(60):
        x, y = rng.uniform(40, w - 40), rng.uniform(84, h - 40)
        r = rng.uniform(8, 30)
        dc.ellipse([x - r, y - r, x + r, y + r], fill=(150, 110, 60, 22))
    im.alpha_composite(capa)
    fT = D.fuente("serif", 46)
    fZ = D.fuente("serif_i", 28)
    fC = D.fuente("serif_sb", 34)
    d.text((w / 2, 40), "MISIÓN", font=D.fuente("serif", 30), fill=(232, 196, 92, 255), anchor="mm")
    d.text((60, 104), titulo, font=fT, fill=(52, 30, 14, 255))
    d.text((62, 166), zona, font=fZ, fill=(100, 70, 40, 255))
    d.line([(60, 214), (w - 60, 214)], fill=(120, 90, 50, 255), width=2)
    y = 240
    for linea in cita:
        d.text((62, y), linea, font=fC, fill=(40, 26, 14, 255))
        y += 48
    d.rounded_rectangle([w - 300, h - 104, w - 60, h - 52], 10, fill=(120, 20, 14, 255), outline=(232, 196, 92, 255), width=3)
    d.text((w - 180, h - 78), "Aceptar", font=D.fuente("serif", 30), fill=(250, 226, 150, 255), anchor="mm")
    a = np.asarray(im, np.uint8)
    return D.Sprite(a[..., :3].copy(), a[..., 3].astype(np.float32) / 255.0, sombra=True, sr=10, off=(8, 12), sop=0.5)


def ventana_mision(lz, t, X, Y, alto, t_in, t_acepta=None, t_out=None):
    if t < t_in:
        return
    spr = _ventana("La pequeña Pamela", "Tierras de la Peste del Este · Villa Darrow",
                   ("«Hola. Soy Pamela.", "  ¿Cómo te llamas?»", "", "Mi papá vendrá por mí…"))
    u = PF.entra(t, t_in, 0.5)
    o = 1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.4))
    s = alto / spr.h * (0.7 + 0.3 * u)
    a = math.radians(-2.0 + (1 - u) * 8)
    M = (np.array([[1, 0, X], [0, 1, Y], [0, 0, 1]]) @ np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
         @ np.diag([s, s, 1.0]) @ np.array([[1, 0, -spr.w / 2], [0, 1, -spr.h / 2], [0, 0, 1]]))
    D.pegar(lz, spr, M, o * clamp01(u * 3))
    if t_acepta is not None and t >= t_acepta:              # el botón se hunde y sale el aviso dorado de misión aceptada
        k = PF.entra(t, t_acepta, 0.35)
        bx, by = X + (spr.w / 2 - 180) * s, Y + (spr.h / 2 - 78) * s
        PF.brillo(lz, bx, by, 140 * s * 2, color=(1.0, 0.8, 0.3), inten=0.5 * (1 - clamp01((t - t_acepta) / 1.2)), t=t)
        texto_oro(lz, "Misión aceptada: La pequeña Pamela", W * 0.5, H * 0.12, 54, o * clamp01(k * 2))


@functools.lru_cache(maxsize=16)
def _oro(txt, px):
    f = D.fuente("serif", px)
    x0, y0, x1, y1 = f.getbbox(txt)
    w, h = x1 - x0 + 40, y1 - y0 + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for dx in (-3, -2, 0, 2, 3):
        for dy in (-3, 0, 3):
            d.text((20 - x0 + dx, 20 - y0 + dy), txt, font=f, fill=(10, 6, 2, 255))
    d.text((20 - x0, 20 - y0), txt, font=f, fill=(255, 209, 0, 255))
    a = np.asarray(im, np.uint8)
    return D.Sprite(a[..., :3].copy(), a[..., 3].astype(np.float32) / 255.0, sombra=False)


def texto_oro(lz, txt, X, Y, px, op=1.0):
    """Texto amarillo de la interfaz de WoW (avisos de misión), con contorno negro."""
    spr = _oro(txt, px)
    D.pegar(lz, spr, np.array([[1, 0, X - spr.w / 2], [0, 1, Y - spr.h / 2], [0, 0, 1]], np.float64), op)


def exclamacion(lz, X, Y, h, t, t_in):
    """«!» amarillo de quien da misiones, flotando sobre su cabeza."""
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.4)
    PF.brillo(lz, X, Y, h * 1.4, color=(1.0, 0.82, 0.2), inten=0.35 * u, t=t, sem=3)
    texto_oro(lz, "!", X, Y + 6 * math.sin(t * 3.2), int(h * (0.7 + 0.3 * u)), clamp01(u * 3))


# ------------------------------------------------------------------ MG 2: árbol de la familia Rutagrana (vuelve al final)
ARBOL = {"joseph": (0.50, 0.36, "JOSEPH · padre"), "marlene_cos": (0.32, 0.36, "MARLENE · tía"),
         "carlin": (0.68, 0.36, "CARLIN · tío"), "jessica": (0.42, 0.72, "JESSICA"), "pamela": (0.58, 0.72, "PAMELA")}
LAZOS = [("joseph", "marlene_cos"), ("joseph", "carlin"), ("joseph", "jessica"), ("joseph", "pamela")]
TINTA = (0.16, 0.10, 0.06)


def arbol(lz, pl, t, tiempos, rad=0.105, tonos=None):
    """tiempos = {quien: t de aparición}; los lazos se trazan con tinta cuando ya están los dos extremos.
    tonos = {quien: (tono, t)}: desde t el medallón se tiñe (los muertos, azul fantasma)."""
    pts = {}
    for q, (x, y, _) in ARBOL.items():
        X, Y, s = pl.P(t, x, y)
        pts[q] = (X, Y)
    for a, b in LAZOS:
        ti = max(tiempos[a], tiempos[b])
        if t < ti:
            continue
        u = smooth(prog(t, ti, ti + 0.7))
        (x0, y0), (x1, y1) = pts[a], pts[b]
        if abs(y1 - y0) < 5:                                     # hermanos: línea horizontal entre medallones
            xa = x0 + math.copysign(rad * H * 0.95, x1 - x0)
            xb = lerp(xa, x1 - math.copysign(rad * H * 0.95, x1 - x0), u)
            D.linea_aa(lz, [(xa, y0), (xb, y1)], TINTA, grosor=4.0, sombra=False)
        else:                                                    # hijas: baja, cruza y baja
            ym = (y0 + y1) / 2
            ruta = [(x0, y0 + rad * H), (x0, ym), (x1, ym), (x1, y1 - rad * H)]
            L = [math.hypot(ruta[i + 1][0] - ruta[i][0], ruta[i + 1][1] - ruta[i][1]) for i in range(3)]
            rest = u * sum(L)
            pp = [ruta[0]]
            for i in range(3):
                if rest <= 0:
                    break
                k = min(1.0, rest / max(L[i], 1e-3))
                pp.append((lerp(ruta[i][0], ruta[i + 1][0], k), lerp(ruta[i][1], ruta[i + 1][1], k)))
                rest -= L[i]
            if len(pp) > 1:
                D.linea_aa(lz, pp, TINTA, grosor=4.0, sombra=False)
    for q, (x, y, nombre) in ARBOL.items():
        ti = tiempos[q]
        if t < ti:
            continue
        X, Y = pts[q]
        tn = None
        if tonos and q in tonos and t >= tonos[q][1]:
            tn = tonos[q][0]
            PF.brillo(lz, X, Y, rad * H * 1.6, color=(0.4, 0.9, 1.0), inten=0.25, t=t)
        pega(lz, f"medallon/{q}", X, Y, 2 * rad * H, t, ti, rot=0.0, tono=tn)
        rot_(lz, nombre, X, Y + rad * H + 34, 34, t, ti + 0.15, rot=0.0)


# ------------------------------------------------------------------ MG 3: la mancha de la Plaga sobre el mapa de Lordaeron
@functools.lru_cache(maxsize=2)
def _ruido(hs, ws):
    r = np.random.default_rng(11)
    n1 = cv2.resize(r.normal(0, 1, (hs // 48 + 2, ws // 48 + 2)).astype(np.float32), (ws, hs), interpolation=cv2.INTER_CUBIC)
    n2 = cv2.resize(r.normal(0, 1, (hs // 12 + 2, ws // 12 + 2)).astype(np.float32), (ws, hs), interpolation=cv2.INTER_CUBIC)
    n = n1 + 0.45 * n2
    return n / (np.abs(n).max() + 1e-6)


def mancha(lz, pl, t, semillas, hueco=None):
    """Tinta negra-verdosa que se extiende desde `semillas` [(x, y, t0, vel)] (coordenadas del mapa, vel en alto de mapa/s),
    con borde irregular y halo verde; `hueco` (x, y, r) = isla que la tinta rodea sin tocar (Villa Darrow aislada)."""
    rgb, hs, ws, s0, cx, cy, ph = pl._st(t)
    w2, h2 = W // 4, H // 4
    X, Y = np.meshgrid(np.arange(w2, dtype=np.float32) * 4 + 2, np.arange(h2, dtype=np.float32) * 4 + 2)
    px = cx + (X - W / 2) / s0
    py = cy + (Y - H / 2) / s0
    n = cv2.remap(_ruido(hs, ws), px, py, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    sx, sy = px / ws, py / hs
    m = np.zeros_like(sx)
    asp = ws / hs
    for x, y, t0, v in semillas:
        if t <= t0:
            continue
        r = (t - t0) * v
        d = np.hypot((sx - x) * asp, sy - y)
        m = np.maximum(m, np.clip((r - d + 0.07 * n * min(1.0, r * 6)) / 0.018, 0, 1))
    if hueco is not None:
        x, y, r = hueco
        d = np.hypot((sx - x) * asp, sy - y)
        m *= np.clip((d - r + 0.012 * n) / 0.012, 0, 1)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    borde = np.clip(m * (1 - m) * 4, 0, 1)
    lz[:] = lz * (1 - 0.86 * m) + np.float32((0.05, 0.10, 0.06)) * 0.86 * m
    lz += borde * np.float32((0.22, 0.55, 0.20)) * 0.55


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


G, PU, PL, AS, HO = "gancho", "pueblo", "plaga", "asedio", "horgus"

# ================================================================== GANCHO (0 - 47,3)
t_cav, t_strat = T(G, "cavernas"), T(G, "stratholme", 0)
t_seg, t_juega, t_padre = T(G, "segundo", 1), T(G, "juega", 1), T(G, "padre", 1)
t_pam, t_jos, t_ning, t_viene = T(G, "pamela", 2), T(G, "joseph", 2), T(G, "ninguno", 2), T(G, "viene", 2)
t_porque, t_tierras, t_ruinas, t_villa = T(G, "porque", 3), T(G, "tierras", 3), T(G, "ruinas", 3), T(G, "villa", 3)
t_palida, t_fria, t_esperando = T(G, "pálida", 4), T(G, "fría", 4), T(G, "esperando", 4)
t_hola, t_llamas = T(G, "hola", 5), T(G, "llamas", 5)
t_esta, t_tristes, t_world, t_escond, t_cruzan, t_largo = (T(G, "esta", 6), T(G, "tristes", 6), T(G, "world", 6),
                                                            T(G, "escondida", 6), T(G, "cruzan", 6), T(G, "largo", 6))

wow(0.0, "amb_peste_noche", 0.55, dur=47.0, fade=2.0)
snd(0.3, "viento", 0.5, dur=5.0)

P1 = PF.Plano("posada_camino", 0.0, t_seg, z0=1.04, z1=1.30, c0=(0.50, 0.56), c1=(0.42, 0.46), par=(30, 8))
V1 = [(0.4, 7.0, 0.20, 0.13, 70, -1, 0.3), (1.6, 7.5, 0.26, 0.19, 52, -1, 1.1)]
wow(2.6, "lobo", 0.45)


@toma(0.0)
def g1(lz, t):
    P1.fondo(lz, t)
    brillo_en(lz, P1, t, 0.395, 0.36, 90, color=(1.0, 0.62, 0.25), inten=0.55, sem=1)        # la ventana con vela del 2.º piso
    brillo_en(lz, P1, t, 0.77, 0.19, 120, color=(0.55, 0.75, 0.95), inten=0.18, sem=2)       # luna
    brillo_en(lz, P1, t, 0.70, 0.36, 160, color=(0.6, 0.8, 0.9), inten=0.10, sem=4)          # Stratholme a lo lejos
    cuervos(lz, t, V1, tono=NOCHE)
    niebla(lz, t, NIEBLA_VERDE)
    rot_(lz, "CAVERNAS DEL TIEMPO", W * 0.26, H * 0.15, 48, t, t_cav, t_strat - 0.3)
    rot_(lz, "CAMINO A STRATHOLME", W * 0.70, H * 0.20, 46, t, t_strat - 0.1, rot=1.5)


P2 = PF.Plano("posada_cuarto", t_padre - 0.5, t_padre + 1.8, z0=1.30, z1=1.32, c0=(0.36, 0.66), c1=(0.60, 0.56), par=(26, 6))
wow(t_seg - 0.3, "taberna", 0.18, dur=7.6, fade=1.0)
wow(t_seg - 0.2, "vela", 0.5)
snd(t_juega, "papel", 0.3)


@toma(t_seg - 0.3, ("desenfoque", 0.6))
def g2(lz, t):
    P2.fondo(lz, t)
    brillo_en(lz, P2, t, 0.815, 0.50, 80, color=(1.0, 0.62, 0.25), inten=0.55, sem=5)
    brillo_en(lz, P2, t, 0.30, 0.31, 120, color=(0.5, 0.7, 0.95), inten=0.10, sem=6)       # luna por la ventana
    # Pamela juega en la alfombra; su padre duerme en la cama de al lado
    X, Y, h = P2.en(t, 0.37, 0.82, 0.30)
    PF.actor(lz, "pamela_hoja/00", X, Y, h, tono=VELA, rot=2.0 * math.sin(t * 2.3), sy=PF.respira(t))
    quieto(lz, P2, t, "utileria/15", 0.25, 0.83, 0.09, tono=VELA)
    quieto(lz, P2, t, "joseph_hoja/00", 0.625, 0.635, 0.14, flip=True, tono=VELA, fase=1.0)
    niebla(lz, t, [("fx_hoja/05", 0.97, 260, 10, 0.25, 0.1)])


P3 = PF.Plano("posada_cuarto_b", t_pam - 0.6, t_porque, z0=1.12, z1=1.2, c0=(0.5, 0.5), c1=(0.52, 0.5), par=(0, 0))
snd(t_pam, "papel", 0.6)
snd(t_jos, "papel", 0.6)
snd(t_viene - 0.2, "golpe_grave", 0.8)


@toma(t_pam - 0.6, ("latigo", 0.45))
def g3(lz, t):
    P3.fondo(lz, t)
    desenfoca(lz, 6)
    oscurece(lz, 0.35)
    k = smooth(prog(t, t_ning, t_viene + 0.8))
    real(lz, "pamela_muneca", W * 0.30, H * 0.47, H * 0.64, t, t_pam, rot=-4)
    real(lz, "joseph_cos", W * 0.71, H * 0.44, H * 0.40, t, t_jos, rot=3)
    rot_(lz, "PAMELA RUTAGRANA", W * 0.30, H * 0.86, 44, t, t_pam + 0.3)
    rot_(lz, "JOSEPH RUTAGRANA · su padre", W * 0.71, H * 0.76, 42, t, t_jos + 0.3, rot=1.5)
    tinte(lz, (0.55, 0.85, 0.60), 0.55 * k)                       # «ninguno sabe lo que viene»: la Peste lo tiñe todo
    niebla(lz, t, [(p, y + 0.04 * (1 - k), hh, v, o * k, f) for p, y, hh, v, o, f in NIEBLA_VERDE])


P4 = PF.Plano("peste_este", t_porque - 0.3, t_ruinas, z0=1.02, z1=1.26, c0=(0.5, 0.55), c1=(0.44, 0.50), par=(36, 8))
V4 = [(t_porque, 6.0, 0.18, 0.12, 64, 1, 0.5), (t_porque + 0.8, 6.5, 0.24, 0.20, 46, 1, 1.7)]
snd(t_porque, "viento", 0.7, dur=4.0)


@toma(t_porque - 0.3, ("latigo", 0.45))
def g4(lz, t):
    P4.fondo(lz, t)
    brillo_en(lz, P4, t, 0.375, 0.21, 40, color=(1.0, 0.6, 0.25), inten=0.4, sem=8)        # ventana de la torre
    cuervos(lz, t, V4, tono=NUBLADO)
    niebla(lz, t, NIEBLA_VERDE)
    rot_(lz, "TIERRAS DE LA PESTE DEL ESTE", W * 0.5, H * 0.16, 52, t, t_tierras, t_ruinas - 0.2)


P5 = PF.Plano("ruinas_noche", t_ruinas - 0.3, t_palida, z0=1.04, z1=1.24, c0=(0.5, 0.56), c1=(0.47, 0.50), par=(32, 8))
snd(t_villa - 0.1, "golpe_grave", 0.6)
wow(t_villa + 1.0, "fantasma", 0.25)


@toma(t_ruinas - 0.3, ("desenfoque", 0.5))
def g5(lz, t):
    P5.fondo(lz, t)
    brillo_en(lz, P5, t, 0.635, 0.13, 110, color=(0.7, 0.85, 1.0), inten=0.22, sem=9)       # luna
    brillo_en(lz, P5, t, 0.39, 0.70, 30, color=(1.0, 0.6, 0.25), inten=0.4, sem=10)          # una vela olvidada
    niebla(lz, t, NIEBLA_VERDE + NIEBLA_AZUL[:1])
    rot_(lz, "VILLA DARROW", W * 0.5, H * 0.17, 110, t, t_villa, rot=-1.5)
    real(lz, "villa_darrow", W * 0.20, H * 0.66, H * 0.30, t, t_villa + 0.7, rot=-5)
    rot_(lz, "así se ve en el juego", W * 0.20, H * 0.86, 30, t, t_villa + 1.0)


P6 = PF.Plano("ruinas_puerta", t_palida - 0.5, t_hola, z0=1.05, z1=1.22, c0=(0.58, 0.60), c1=(0.62, 0.62), par=(30, 6))
wow(t_palida - 0.1, "fantasma", 0.5)
snd(t_fria, "viento", 0.5, dur=3.0)


@toma(t_palida - 0.5, ("fundido", 0.6))
def g6(lz, t):
    P6.fondo(lz, t)
    brillo_en(lz, P6, t, 0.735, 0.555, 40, color=(1.0, 0.6, 0.25), inten=0.5, sem=11)        # la vela de la puerta
    niebla(lz, t, NIEBLA_AZUL)
    fantasma(lz, P6, t, "pamela_hoja/04", 0.60, 0.86, 0.42, t_in=t_palida - 0.2)


P7 = PF.Plano("ruinas_puerta_b", t_hola - 0.3, t_esta, z0=1.55, z1=1.62, c0=(0.50, 0.62), c1=(0.50, 0.63), par=(24, 6))
wow(t_llamas + 0.4, "mision_acepta", 0.9)


@toma(t_hola - 0.3, ("desenfoque", 0.45))
def g7(lz, t):
    P7.fondo(lz, t)
    desenfoca(lz, 2.2)
    niebla(lz, t, NIEBLA_AZUL[:1])
    fantasma(lz, P7, t, "pamela_hoja/02", 0.42, 0.93, 0.52, op=0.68)
    X, Y, h = P7.en(t, 0.42, 0.93, 0.52)
    exclamacion(lz, X, Y - h * 1.12, 120, t, t_hola - 0.1)
    ventana_mision(lz, t, W * 0.72, H * 0.50, H * 0.62, t_hola + 0.35, t_acepta=t_llamas + 0.4)


P8 = PF.Plano("ruinas_camino", t_esta - 0.4, t_largo + 1.5, z0=1.02, z1=1.14, c0=(0.48, 0.52), c1=(0.56, 0.50), par=(30, 6))
V8 = [(t_escond - 0.5, 6.0, 0.17, 0.10, 70, -1, 0.2), (t_escond, 6.5, 0.22, 0.15, 52, -1, 1.4)]
snd(t_world - 0.4, "galope", 0.7, dur=5.0)
snd(t_largo + 0.4, "golpe_grave", 0.7)


@toma(t_esta - 0.4, ("fundido", 0.6))
def g8(lz, t):
    P8.fondo(lz, t)
    brillo_en(lz, P8, t, 0.31, 0.36, 60, color=(1.0, 0.6, 0.25), inten=0.45, sem=12)         # farol del poste
    cuervos(lz, t, V8, tono=NUBLADO)
    real(lz, "pamela", W * 0.80, H * 0.36, H * 0.46, t, t_esta + 0.2, t_world - 0.2, rot=4)
    anda(lz, P8, t, "jinete_galope", t_world - 0.4, t_largo + 0.6, -0.15, 1.15, 0.84, 0.24, paso=1.7, tono=NUBLADO)
    niebla(lz, t, NIEBLA_VERDE[:2])
    k = smooth(prog(t, t_largo, t_largo + 1.2))
    oscurece(lz, 0.55 * k)
    rot_(lz, "LA NIÑA QUE SIGUE ESPERANDO", W * 0.5, H * 0.42, 92, t, t_largo - 0.1, rot=-1.0)


# ================================================================== PUEBLO (47,3 - 90,9)
t0PU = _ESC[PU]["t0"]
t_humilde, t_lago, t_siglos, t_libro = T(PU, "humilde", 0), T(PU, "lago", 0), T(PU, "siglos", 1), T(PU, "libro", 1)
t_vivia, t_josP, t_capitan, t_milicia = T(PU, "vivía", 2), T(PU, "joseph", 2), T(PU, "capitán", 2), T(PU, "milicia", 2)
t_hijas, t_jessica, t_pamP, t_muneca = T(PU, "hijas", 3), T(PU, "jessica", 3), T(PU, "pamela", 3), T(PU, "muñeca", 3)
t_con, t_marlene, t_carlin, t_hermano = T(PU, "con", 4), T(PU, "marlene", 4), T(PU, "carlin", 4), T(PU, "hermano", 4)
t_tipo, t_duele = T(PU, "era", 5), T(PU, "duele", 5)

snd(t0PU + 0.1, "amanecer", 0.6, dur=3.0)
snd(t0PU + 1.5, "pio", 0.5)
snd(t0PU + 4.2, "pio", 0.4, tono=1.2)
wow(t_lago + 0.5, "campana", 0.25)

Q1 = PF.Plano("villa_lago", t0PU - 0.3, t_siglos, z0=1.02, z1=1.14, c0=(0.50, 0.58), c1=(0.53, 0.48), par=(30, 8))
AGUA1 = [(float(x), float(y), float(f)) for x, y, f in np.random.default_rng(4).uniform((0.30, 0.25, 0), (0.95, 0.40, 1), (60, 3))]
V_DIA = [(t0PU, 9.0, 0.10, 0.06, 40, 1, 0.3), (t0PU + 1.2, 9.5, 0.14, 0.10, 32, 1, 1.2)]


@toma(t0PU - 0.3, ("destello", 0.8))
def p1(lz, t):
    Q1.fondo(lz, t)
    pts = []
    for x, y, f in AGUA1:
        X, Y, s = Q1.P(t, x, y)
        pts.append((X, Y, f))
    PF.destellos(lz, t, pts, s=1.0)
    humo_en(lz, Q1, t, 0.17, 0.30, s=0.8, color=(0.92, 0.92, 0.94), op=0.20, sem=1)
    humo_en(lz, Q1, t, 0.935, 0.30, s=0.8, color=(0.92, 0.92, 0.94), op=0.20, sem=2)
    cuervos(lz, t, V_DIA, tono=(0.8, 0.75, 0.7))
    paseo(lz, Q1, t, "aldeanos_hoja/01", t0PU, t_siglos, 0.12, 0.40, 0.80, 0.30, tono=CALIDO, pasos=1.8)
    paseo(lz, Q1, t, "aldeanos_hoja/00", t0PU + 0.6, t_siglos, 0.88, 0.62, 0.86, 0.33, tono=CALIDO, pasos=1.6)
    paseo(lz, Q1, t, "aldeanos_hoja/04", t_humilde, t_humilde + 3.0, 0.25, 0.80, 0.93, 0.24, tono=CALIDO, pasos=3.4,
          desde_antes=False, hasta_despues=False)
    rot_(lz, "AÑOS ANTES", W * 0.5, H * 0.13, 62, t, t0PU + 0.3, t_lago - 0.6)
    rot_(lz, "LAGO DARROWMERE", W * 0.62, H * 0.13, 50, t, t_lago, rot=1.5)


Q2 = PF.Plano("villa_calle", t_siglos - 0.3, t_vivia, z0=1.06, z1=1.16, c0=(0.42, 0.56), c1=(0.52, 0.56), par=(32, 8))
for k in range(5):
    snd(t_siglos + 0.2 + 1.05 * k, "clink", 0.35, tono=1.0 + 0.05 * (k % 2))
snd(t_libro - 0.2, "papel", 0.7)


@toma(t_siglos - 0.3, ("fundido", 0.5))
def p2(lz, t):
    Q2.fondo(lz, t)
    brillo_en(lz, Q2, t, 0.10, 0.62, 70, color=(1.0, 0.55, 0.2), inten=0.4, sem=13, chis=5)    # la fragua
    golpe = abs(math.sin((t - t_siglos) * math.pi / 1.05))
    quieto(lz, Q2, t, "aldeanos_hoja/02", 0.20, 0.86, 0.38, tono=CALIDO, rot=-8 * (1 - golpe))
    paseo(lz, Q2, t, "aldeanos_hoja/03", t_siglos - 0.3, t_vivia, 0.56, 0.47, 0.76, 0.25, tono=CALIDO, pasos=1.2)
    paseo(lz, Q2, t, "aldeanos_hoja/05", t_siglos, t_vivia, 0.98, 0.66, 0.90, 0.33, tono=CALIDO, pasos=1.8)
    pega(lz, "utileria/09", W * 0.50, H * 0.34, H * 0.30, t, t_libro - 0.2, rot=-6)
    rot_(lz, "NADA QUE CONTAR", W * 0.50, H * 0.12, 44, t, t_libro + 0.3, rot=2)


Q3 = PF.Plano("casa_rutagrana", t_vivia - 0.3, t_hijas, z0=1.04, z1=1.20, c0=(0.50, 0.62), c1=(0.42, 0.66), par=(30, 8))
snd(t_capitan, "papel", 0.6)
wow(t_milicia + 0.3, "espada_arma", 0.35)
wow(t_milicia + 0.9, "espada_arma", 0.3)


@toma(t_vivia - 0.3, ("latigo", 0.45))
def p3(lz, t):
    Q3.fondo(lz, t)
    paseo(lz, Q3, t, "pamela_hoja/05", t_vivia, t_josP + 0.5, 0.66, 0.54, 0.76, 0.22, tono=CALIDO, pasos=2.6)
    quieto(lz, Q3, t, "familia_hoja/00", 0.70, 0.76, 0.30, tono=CALIDO, fase=0.7)
    quieto(lz, Q3, t, "joseph_hoja/01", 0.36, 0.90, 0.50, tono=CALIDO, t_in=t_josP - 0.2)
    ent = 6.0 * math.sin((t - t_milicia) * 5.0) if t > t_milicia else 0.0
    quieto(lz, Q3, t, "defensores_hoja/02", 0.15, 0.86, 0.40, tono=CALIDO, t_in=t_milicia - 0.3, rot=ent)
    quieto(lz, Q3, t, "defensores_hoja/00", 0.88, 0.92, 0.46, tono=CALIDO, t_in=t_milicia, flip=True)
    rot_(lz, "CAPITÁN DE LA MILICIA", W * 0.5, H * 0.12, 50, t, t_capitan)


Q4 = PF.Plano("casa_interior", t_hijas - 0.3, t_con, z0=1.06, z1=1.18, c0=(0.46, 0.62), c1=(0.52, 0.62), par=(28, 6))
snd(t_jessica, "pop", 0.5)
snd(t_pamP, "pop", 0.5, tono=1.2)
snd(t_muneca - 0.2, "papel", 0.5)
wow(t_hijas, "hoguera", 0.25, dur=t_con - t_hijas + 0.5, fade=0.8)


@toma(t_hijas - 0.3, ("fundido", 0.5))
def p4(lz, t):
    Q4.fondo(lz, t)
    brillo_en(lz, Q4, t, 0.79, 0.70, 110, color=(1.0, 0.55, 0.2), inten=0.5, sem=14, chis=7)   # el hogar
    quieto(lz, Q4, t, "familia_hoja/00", 0.30, 0.92, 0.52, tono=VELA, t_in=t_jessica - 0.2)
    quieto(lz, Q4, t, "pamela_hoja/01", 0.54, 0.93, 0.36, tono=VELA, t_in=t_pamP - 0.2, fase=0.5)
    real(lz, "jessica", W * 0.12, H * 0.32, H * 0.40, t, t_jessica, t_pamP + 1.4, rot=-5)
    real(lz, "pamela", W * 0.88, H * 0.32, H * 0.42, t, t_pamP, t_muneca - 0.3, rot=4)
    real(lz, "muneca", W * 0.86, H * 0.32, H * 0.34, t, t_muneca - 0.2, rot=6)
    rot_(lz, "su muñeca", W * 0.86, H * 0.56, 34, t, t_muneca)


Q5 = PF.Plano("pergamino_mesa", t_con - 0.3, t_tipo, z0=1.02, z1=1.08, c0=(0.52, 0.50), c1=(0.50, 0.52), par=(0, 0))
for tt in (t_con, t_con + 0.15, t_con + 0.3):
    snd(tt, "papel", 0.4)
snd(t_marlene, "escribir", 0.5, dur=0.6)
snd(t_carlin, "escribir", 0.5, dur=0.6)


@toma(t_con - 0.3, ("desenfoque", 0.5))
def p5(lz, t):
    Q5.fondo(lz, t)
    brillo_en(lz, Q5, t, 0.92, 0.12, 100, color=(1.0, 0.6, 0.25), inten=0.5, sem=15)
    rot_(lz, "LA FAMILIA RUTAGRANA", W * 0.5, H * 0.12, 54, t, t_con - 0.1, rot=0)
    arbol(lz, Q5, t, {"joseph": t_con, "jessica": t_con + 0.15, "pamela": t_con + 0.3, "marlene_cos": t_marlene - 0.1,
                      "carlin": t_carlin - 0.1})


Q6 = PF.Plano("plaza_tarde", t_tipo - 0.4, _ESC[PL]["t0"], z0=1.26, z1=1.02, c0=(0.48, 0.66), c1=(0.5, 0.56), par=(32, 8))
V6 = [(t_duele - 0.5, 6.5, 0.30, 0.12, 64, 1, 0.4), (t_duele - 0.2, 7.0, 0.36, 0.16, 50, 1, 1.5),
      (t_duele + 0.2, 6.5, 0.28, 0.08, 44, 1, 2.2)]
wow(t_duele + 0.2, "campana", 0.55)
snd(t_duele, "viento", 0.5, dur=3.0)


@toma(t_tipo - 0.4, ("fundido", 0.8))
def p6(lz, t):
    Q6.fondo(lz, t)
    k = smooth(prog(t, t_duele - 0.4, t_duele + 2.2))
    ton = tuple(lerp(a, b, k) for a, b in zip(OCASO, NOCHE))
    ton = tuple(round(c, 2) for c in ton)
    brillo_en(lz, Q6, t, 0.31, 0.47, 40, color=(1.0, 0.6, 0.25), inten=0.45 * (1 - 0.5 * k), sem=16)
    paseo(lz, Q6, t, "aldeanos_hoja/01", t_tipo, t_duele, 0.84, 0.97, 0.70, 0.20, tono=ton, pasos=1.6)
    paseo(lz, Q6, t, "pamela_hoja/05", t_tipo, t_tipo + 3.5, 0.22, 0.34, 0.90, 0.26, tono=ton, pasos=2.4)
    quieto(lz, Q6, t, "joseph_hoja/01", 0.42, 0.88, 0.44, tono=ton)
    quieto(lz, Q6, t, "familia_hoja/01", 0.55, 0.86, 0.40, tono=ton, fase=0.6)
    quieto(lz, Q6, t, "familia_hoja/00", 0.63, 0.87, 0.40, tono=ton, fase=1.2)
    quieto(lz, Q6, t, "familia_hoja/05", 0.72, 0.89, 0.45, tono=ton, fase=1.8)
    cuervos(lz, t, V6, tono=NOCHE)
    tinte(lz, (0.60, 0.72, 0.85), 0.45 * k)


# ================================================================== PLAGA (90,9 - 127,3)
t0PL = _ESC[PL]["t0"]
t_plaga, t_grano, t_graneros = T(PL, "plaga", 0), T(PL, "grano", 0), T(PL, "graneros", 0)
t_comian, t_enferm, t_morian, t_levant = T(PL, "comían", 1), T(PL, "enfermaban", 1), T(PL, "morían", 1), T(PL, "levantaban", 1)
t_stratC, t_andC, t_extend, t_tinta = T(PL, "stratholme", 2), T(PL, "andorhal", 2, n=0), T(PL, "extendió", 2), T(PL, "tinta", 2)
t_villaA, t_aislada, t_ejer, t_lejos = T(PL, "villa", 3), T(PL, "aislada", 3), T(PL, "ejércitos", 3), T(PL, "lejos", 3)
t_asi, t_quedarse, t_pelear = T(PL, "así", 4), T(PL, "quedarse", 4), T(PL, "pelear", 4)

wow(t0PL + 0.2, "amb_peste_dia", 0.45, dur=36.0, fade=2.0)
R1 = PF.Plano("graneros_andorhal", t0PL - 0.3, t_comian, z0=1.04, z1=1.20, c0=(0.50, 0.56), c1=(0.38, 0.58), par=(30, 8))
wow(t_grano, "peste_burbuja", 0.6)
snd(t_plaga, "golpe_grave", 0.7)


@toma(t0PL - 0.3, ("negro", 0.8))
def q1(lz, t):
    R1.fondo(lz, t)
    pul = 0.5 + 0.5 * math.sin(t * 2.2)
    brillo_en(lz, R1, t, 0.31, 0.60, 150, color=(0.35, 1.0, 0.35), inten=0.30 + 0.15 * pul, sem=17)   # la puerta del granero
    humo_en(lz, R1, t, 0.31, 0.62, s=1.0, color=(0.45, 0.75, 0.40), op=0.22, sem=3)
    brillo_en(lz, R1, t, 0.465, 0.62, 30, color=(1.0, 0.6, 0.25), inten=0.4, sem=18)
    paseo(lz, R1, t, "plaga_hoja/04", t0PL, t_comian, 0.62, 1.15, 0.86, 0.26, tono=NUBLADO, pasos=1.4)
    paseo(lz, R1, t, "aldeanos_hoja/00", t0PL + 1.2, t_comian, 0.50, 0.92, 0.80, 0.32, tono=NUBLADO, pasos=1.6)
    if t >= t_grano:
        X, Y, h = R1.en(t, 0.22, 0.93, 0.30)
        PF.brillo(lz, X, Y - 0.4 * h, 1.3 * h, color=(0.35, 1.0, 0.35), inten=0.35 * PF.entra(t, t_grano, 0.5), t=t, sem=19)
    quieto(lz, R1, t, "plaga_hoja/03", 0.22, 0.93, 0.30, tono=NUBLADO, t_in=t_grano)
    niebla(lz, t, NIEBLA_VERDE[:2])
    rot_(lz, "GRANEROS DE ANDORHAL", W * 0.62, H * 0.13, 50, t, t_graneros)


R2 = PF.Plano("casa_enfermo", t_comian - 0.3, t_stratC, z0=1.10, z1=1.30, c0=(0.42, 0.62), c1=(0.33, 0.66), par=(26, 6))
snd(t_morian, "latido", 0.7)
wow(t_levant + 0.1, "zombi", 0.8)


@toma(t_comian - 0.3, ("desenfoque", 0.5))
def q2(lz, t):
    R2.fondo(lz, t)
    vela = 1.0 - smooth(prog(t, t_morian - 0.1, t_morian + 0.5))
    brillo_en(lz, R2, t, 0.955, 0.37, 60, color=(1.0, 0.6, 0.25), inten=0.5 * vela, sem=20)
    brillo_en(lz, R2, t, 0.08, 0.38, 160, color=(0.35, 1.0, 0.4), inten=0.14, sem=21)          # la ventana verde
    k = smooth(prog(t, t_levant - 0.4, t_levant + 0.2))
    X, Y, h = R2.en(t, 0.27, 0.97, 0.40)          # el otro catre del cuarto, en primer plano (el del fondo queda vacío)
    PF.actor(lz, "plaga_hoja/00", X, Y, h, tono=NUBLADO, op=1 - k, sy=PF.respira(t, f=0.9, a=0.02))
    if k > 0:
        PF.actor(lz, "plaga_hoja/01", X - 0.05 * h, Y, h * 1.05, tono=NOCHE_PESTE, op=k, rot=-4 * (1 - k))
        PF.brillo(lz, X - 0.12 * h, Y - 0.82 * h, 0.35 * h, color=(0.3, 1.0, 0.3), inten=0.7 * k, t=t, sem=22)
        PF.brillo(lz, X - 0.12 * h, Y - 0.82 * h, 1.5 * h, color=(0.3, 0.9, 0.3), inten=0.25 * k * (0.5 + 0.5 * math.sin(t * 9)), t=t)
    oscurece(lz, 0.25 * (1 - vela))
    niebla(lz, t, [("fx_hoja/05", 0.96, 300, 14, 0.35, 0.3)])


R3 = PF.Plano("stratholme_arde", t_stratC - 0.3, t_andC, z0=1.08, z1=1.22, c0=(0.60, 0.48), c1=(0.62, 0.46), par=(30, 6))
wow(t_stratC - 0.2, "hoguera", 0.6, dur=1.8, fade=0.5)
snd(t_stratC, "golpe_grave", 0.8)


@toma(t_stratC - 0.3, ("latigo", 0.4))
def q3(lz, t):
    R3.fondo(lz, t)
    for k, (x, y) in enumerate([(0.62, 0.32), (0.80, 0.30), (0.50, 0.45)]):
        brillo_en(lz, R3, t, x, y, 200, color=(1.0, 0.5, 0.15), inten=0.35, sem=30 + k, chis=8)
    humo_en(lz, R3, t, 0.70, 0.20, s=1.6, color=(0.18, 0.15, 0.14), op=0.35, sem=4)
    rot_(lz, "STRATHOLME", W * 0.60, H * 0.12, 70, t, t_stratC)


# el mapa: Stratholme al noreste, Andorhal al centro-oeste, Villa Darrow al sureste junto al agua
MAPA = dict(strat=(0.74, 0.22), andor=(0.44, 0.50), darrow=(0.665, 0.635))
R4 = PF.Plano("mapa_lordaeron", t_andC - 0.3, t_villaA + 1.2, z0=1.04, z1=1.42, c0=(0.52, 0.50), c1=(0.63, 0.60), par=(0, 0))
snd(t_andC, "golpe_grave", 0.6)
snd(t_extend, "siseo", 0.5, dur=2.0)
snd(t_villaA, "pop", 0.6)


def _mapa(lz, pl, t):
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.86, 0.10, 80, color=(1.0, 0.6, 0.25), inten=0.45, sem=23)
    semillas = [(*MAPA["strat"], t_stratC, 0.050), (*MAPA["andor"], t_andC, 0.050),
                (0.30, 0.40, t_extend + 0.4, 0.06), (0.58, 0.82, t_extend + 0.8, 0.05), (0.84, 0.50, t_extend + 0.2, 0.06)]
    mancha(lz, pl, t, semillas, hueco=(*MAPA["darrow"], 0.055))
    for k, (clave, txt, t0) in enumerate((("strat", "Stratholme", t_andC - 0.3), ("andor", "Andorhal", t_andC),
                                          ("darrow", "Villa Darrow", t_villaA))):
        X, Y, s = pl.P(t, *MAPA[clave])
        if clave == "darrow" and t >= t0:
            PF.brillo(lz, X, Y, 90 * s, color=(1.0, 0.8, 0.35), inten=0.55, t=t, sem=24)
        rot_(lz, txt, X, Y - 46 * s, int(30 * s), t, t0, rot=0)


@toma(t_andC - 0.3, ("corte", 0.0))
def q4(lz, t):
    _mapa(lz, R4, t)


R5 = PF.Plano("puerta_pueblo", t_ejer - 0.4, t_asi, z0=1.06, z1=1.20, c0=(0.50, 0.55), c1=(0.52, 0.48), par=(34, 8))
V5 = [(t_ejer, 6.0, 0.16, 0.12, 58, 1, 0.6)]
snd(t_ejer, "viento", 0.6, dur=4.0)


@toma(t_ejer - 0.4, ("fundido", 0.6))
def q5(lz, t):
    R5.fondo(lz, t)
    brillo_en(lz, R5, t, 0.415, 0.275, 50, color=(1.0, 0.6, 0.25), inten=0.5, sem=25)
    cuervos(lz, t, V5, tono=NOCHE)
    quieto(lz, R5, t, "aldeanos_hoja/03", 0.36, 0.84, 0.40, tono=NOCHE, fase=0.4)
    quieto(lz, R5, t, "aldeanos_hoja/01", 0.62, 0.86, 0.36, tono=NOCHE, fase=1.1, flip=True)
    # la bandera de la Alianza, diminuta en el horizonte, que se borra: demasiado lejos
    a = 1.0 - smooth(prog(t, t_lejos - 0.2, t_lejos + 1.2))
    quieto(lz, R5, t, "utileria/11", 0.52, 0.46, 0.06, tono=NOCHE, op=0.9 * a, t_in=t_ejer + 0.4)
    niebla(lz, t, NIEBLA_VERDE[:2])


R6 = PF.Plano("plaza_reunion", t_asi - 0.3, _ESC[AS]["t0"] + 0.3, z0=1.18, z1=1.04, c0=(0.55, 0.62), c1=(0.52, 0.56),
              par=(30, 8))
wow(t_asi, "campana", 0.6)
wow(t_asi + 1.6, "campana", 0.5)
wow(t_pelear, "grito_guerra", 0.8)


@toma(t_asi - 0.3, ("latigo", 0.45))
def q6(lz, t):
    R6.fondo(lz, t)
    brillo_en(lz, R6, t, 0.45, 0.43, 30, color=(1.0, 0.6, 0.25), inten=0.4, sem=26)
    brillo_en(lz, R6, t, 0.545, 0.44, 30, color=(1.0, 0.6, 0.25), inten=0.4, sem=27)
    paseo(lz, R6, t, "defensores_hoja/02", t_asi - 0.3, t_quedarse, 0.04, 0.24, 0.88, 0.42, tono=NUBLADO, pasos=1.8)
    paseo(lz, R6, t, "aldeanos_hoja/02", t_asi, t_quedarse + 0.5, 0.98, 0.84, 0.90, 0.42, tono=NUBLADO, pasos=1.6, flip=True)
    quieto(lz, R6, t, "defensores_hoja/05", 0.47, 0.84, 0.36, tono=NUBLADO, fase=0.3)
    quieto(lz, R6, t, "aldeanos_hoja/00", 0.36, 0.80, 0.30, tono=NUBLADO, fase=0.9)
    quieto(lz, R6, t, "joseph_hoja/04", 0.70, 0.64, 0.36, tono=NUBLADO, t_out=t_quedarse - 0.1, flip=True)
    quieto(lz, R6, t, "joseph_hoja/03", 0.70, 0.64, 0.40, tono=NUBLADO, t_in=t_quedarse - 0.1)
    rot_(lz, "A PELEAR", W * 0.72, H * 0.12, 70, t, t_pelear, rot=-3)


# ================================================================== ASEDIO (127,3 - 170,9)
t0AS = _ESC[AS]["t0"]
t_sold, t_palad, t_mano, t_milA, t_barric = T(AS, "soldados", 0), T(AS, "paladines", 0), T(AS, "mano", 0), T(AS, "milicia", 0), T(AS, "barricadas", 0)
t_primeros, t_esque, t_cadav, t_bajaban = T(AS, "primeros", 1), T(AS, "esqueletos", 1), T(AS, "cadáveres", 1), T(AS, "bajaban", 1)
t_def, t_retro, t_vez, t_otra1, t_otra2 = T(AS, "defensores", 2), T(AS, "retroceder", 2), T(AS, "vez", 2), T(AS, "otra", 2, n=0), T(AS, "otra", 2, n=1)
t_portiempo, t_resistir = T(AS, "por", 3), T(AS, "resistir", 3)
t_antes, t_josA, t_dejo, t_marA = T(AS, "antes", 4), T(AS, "joseph", 4), T(AS, "dejó", 4), T(AS, "marlene", 4)
t_y5, t_escondio, t_pidio, t_pasara = T(AS, "y", 5), T(AS, "escondió", 5), T(AS, "pidió", 5), T(AS, "pasara", 5)

A1 = PF.Plano("barricadas", t0AS - 0.3, t_primeros, z0=1.04, z1=1.18, c0=(0.50, 0.60), c1=(0.52, 0.56), par=(30, 8))
snd(t_sold, "pasos", 0.5, dur=2.0)
wow(t_palad, "espada_arma", 0.3)
snd(t_mano, "papel", 0.5)
snd(t_barric + 0.6, "golpe_suave", 0.8)
wow(t0AS, "antorcha", 0.35, dur=9.0, fade=1.0)


@toma(t0AS - 0.3, ("fundido", 0.5))
def a1(lz, t):
    A1.fondo(lz, t)
    for k, (x, y) in enumerate([(0.38, 0.57), (0.685, 0.60), (0.39, 0.40), (0.685, 0.40)]):
        brillo_en(lz, A1, t, x, y, 90 if k < 2 else 50, color=(1.0, 0.55, 0.2), inten=0.45, sem=40 + k, chis=6 if k < 2 else 0)
    quieto(lz, A1, t, "defensores_hoja/00", 0.20, 0.86, 0.44, tono=NUBLADO, t_in=t_sold - 0.1)
    quieto(lz, A1, t, "defensores_hoja/01", 0.44, 0.90, 0.48, tono=NUBLADO, t_in=t_palad - 0.1, fase=0.5)
    if t >= t_palad:
        X, Y, h = A1.en(t, 0.44, 0.90, 0.48)
        PF.brillo(lz, X - 0.06 * h, Y - 0.93 * h, 0.4 * h, color=(1.0, 0.85, 0.4), inten=0.45, t=t, sem=44)
    quieto(lz, A1, t, "defensores_hoja/02", 0.64, 0.86, 0.42, tono=NUBLADO, t_in=t_milA - 0.1, fase=1.0)
    paseo(lz, A1, t, "defensores_hoja/04", t_barric - 1.6, t_barric + 0.6, 1.15, 0.84, 0.94, 0.40, tono=NUBLADO, pasos=2.0,
          desde_antes=False)
    real(lz, "mano_plata", W * 0.84, H * 0.25, H * 0.26, t, t_mano - 0.2, t_barric - 0.4, rot=5)
    rot_(lz, "LA MANO DE PLATA", W * 0.84, H * 0.44, 36, t, t_mano, t_barric - 0.4)
    niebla(lz, t, NIEBLA_VERDE[:2])


A2 = PF.Plano("colinas_noche", t_primeros - 0.4, t_def, z0=1.10, z1=1.26, c0=(0.50, 0.60), c1=(0.46, 0.62), par=(34, 8))
wow(t_esque - 0.2, "huesos", 0.7)
wow(t_esque + 0.8, "esqueleto_muere", 0.35)
wow(t_cadav + 0.2, "zombi", 0.55)
wow(t_primeros, "lobo", 0.35)
snd(t_bajaban, "pasos", 0.4, dur=2.5)


@toma(t_primeros - 0.4, ("negro", 0.6))
def a2(lz, t):
    A2.fondo(lz, t)
    brillo_en(lz, A2, t, 0.66, 0.13, 120, color=(0.7, 0.9, 1.0), inten=0.20, sem=45)
    brillo_en(lz, A2, t, 0.66, 0.62, 50, color=(1.0, 0.6, 0.25), inten=0.25, sem=46)        # las luces del pueblo, abajo
    niebla(lz, t, NIEBLA_VERDE[2:])
    t0 = t_primeros - 0.3
    for k, (dt, y, fr, x0) in enumerate([(0.0, 0.74, 0.28, 0.80), (0.4, 0.82, 0.36, 0.92), (0.9, 0.70, 0.24, 0.70),
                                         (1.4, 0.90, 0.44, 1.02), (2.2, 0.78, 0.32, 1.05)]):
        pz = ("esqueletos_hoja/00", "esqueletos_hoja/01", "esqueletos_hoja/05", "esqueletos_hoja/00", "esqueletos_hoja/02")[k]
        paseo(lz, A2, t, pz, t0 + dt, t0 + dt + 7.5, x0, 0.12 + 0.1 * k, y, fr, tono=(0.78, 0.86, 0.80), pasos=1.5 + 0.2 * k,
              flip=k % 2 == 1)        # tambaleo de títere (el ciclo de Flow salió con las figuras pegadas)
    paseo(lz, A2, t, "esqueletos_hoja/03", t_esque, t_def, 0.95, 0.72, 0.93, 0.18, tono=NOCHE_PESTE, pasos=1.2,
          desde_antes=False)
    paseo(lz, A2, t, "plaga_hoja/02", t_cadav - 0.3, t_def + 1.0, 1.12, 0.62, 0.97, 0.46, tono=NOCHE_PESTE, pasos=1.3,
          desde_antes=False)
    niebla(lz, t, NIEBLA_VERDE[:2])


A3 = PF.Plano("barricada_noche", t_def - 0.3, t_portiempo, z0=1.08, z1=1.16, c0=(0.50, 0.58), c1=(0.50, 0.56), par=(28, 6))
GOLPES = [t_retro - 0.1, t_vez - 0.05, t_otra1 - 0.05, t_otra2 - 0.05]
for k, tg in enumerate(GOLPES):
    wow(tg, "espada_escudo" if k % 2 == 0 else "espada_carne", 0.75)
    wow(tg + 0.12, "esqueleto_muere", 0.45)
    snd(tg, "golpe_grave", 0.4)
wow(t_def - 0.3, "hoguera", 0.4, dur=6.8, fade=0.8)


@toma(t_def - 0.3, ("latigo", 0.4))
def a3(lz, t):
    A3.fondo(lz, t)
    for k, (x, y) in enumerate([(0.645, 0.39), (0.40, 0.37), (0.71, 0.36)]):
        brillo_en(lz, A3, t, x, y, 110 if k == 0 else 50, color=(1.0, 0.55, 0.2), inten=0.5, sem=50 + k, chis=8 if k == 0 else 3)
    # esqueletos que asoman por encima de la barricada y salen volando, uno por golpe
    for k, tg in enumerate(GOLPES):
        xs = (0.40, 0.56, 0.47, 0.62)[k]
        if tg - 1.0 <= t < tg:
            u = smooth(prog(t, tg - 1.0, tg - 0.5))
            X, Y, h = A3.en(t, xs, 0.50 + 0.06 * (1 - u), 0.30)
            PF.actor(lz, ("esqueletos_hoja/00", "esqueletos_hoja/01", "esqueletos_hoja/05", "esqueletos_hoja/00")[k], X, Y, h,
                     tono=(0.80, 0.90, 0.80), suelo=0, flip=k % 2 == 1)
        elif tg <= t < tg + 1.0:
            u = (t - tg) / 1.0
            X, Y, h = A3.en(t, xs + 0.10 * u, 0.50 - 0.25 * u + 0.45 * u * u, 0.32)
            PF.actor(lz, "esqueletos_hoja/04", X, Y, h, tono=(0.85, 0.92, 0.82), rot=200 * u, op=1 - u * u, suelo=0)
            PF.brillo(lz, X, Y - h * 0.5, h * (1.2 - u), color=(1.0, 0.9, 0.6), inten=0.4 * (1 - u), t=t)
    quieto(lz, A3, t, "defensores_hoja/03", 0.84, 0.98, 0.52, tono=FUEGO_NOCHE, flip=True, fase=0.2)
    quieto(lz, A3, t, "defensores_hoja/00", 0.30, 0.99, 0.56, tono=FUEGO_NOCHE, fase=0.9)
    golpe = max([math.exp(-max(0.0, t - tg) * 6) if t >= tg else 0.0 for tg in GOLPES])
    quieto(lz, A3, t, "defensores_hoja/01", 0.56, 0.99, 0.58, tono=FUEGO_NOCHE, rot=-14 * golpe, fase=1.4)
    for k, (tg, txt) in enumerate(zip(GOLPES[1:], ("I", "II", "III"))):
        rot_(lz, txt, W * (0.80 + 0.06 * k), H * 0.14, 70, t, tg, rot=-4 + 3 * k)


A4 = PF.Plano("alba_pueblo", t_portiempo - 0.3, t_antes, z0=1.04, z1=1.14, c0=(0.50, 0.58), c1=(0.52, 0.54), par=(30, 8))
wow(t_portiempo + 0.3, "campana", 0.45)
snd(t_portiempo - 0.3, "amanecer", 0.5, dur=3.0)


@toma(t_portiempo - 0.3, ("destello", 0.6))
def a4(lz, t):
    A4.fondo(lz, t)
    humo_en(lz, A4, t, 0.215, 0.22, s=0.9, color=(0.8, 0.8, 0.82), op=0.22, sem=5)
    humo_en(lz, A4, t, 0.40, 0.40, s=0.7, color=(0.5, 0.5, 0.52), op=0.20, sem=6)
    for k, (pz, x, fr) in enumerate((("defensores_hoja/01", 0.30, 0.46), ("defensores_hoja/00", 0.52, 0.46),
                                     ("defensores_hoja/02", 0.70, 0.42), ("defensores_hoja/03", 0.86, 0.40))):
        salto = abs(math.sin((t - t_portiempo) * 3.2 + k * 0.9)) * (1 - smooth(prog(t, t_resistir, t_antes)))
        X, Y, h = A4.en(t, x, 0.90, fr)
        PF.actor(lz, pz, X, Y - 0.06 * h * salto, h, tono=ALBA, flip=k == 3, sy=PF.respira(t, fase=k))
    niebla(lz, t, NIEBLA_AZUL[:1])


A5 = PF.Plano("casa_marlene", t_antes - 0.3, t_y5, z0=1.08, z1=1.20, c0=(0.52, 0.60), c1=(0.56, 0.60), par=(30, 8))
snd(t_dejo, "pasos", 0.5, dur=2.4)


@toma(t_antes - 0.3, ("fundido", 0.5))
def a5(lz, t):
    A5.fondo(lz, t)
    brillo_en(lz, A5, t, 0.555, 0.505, 70, color=(1.0, 0.6, 0.25), inten=0.5, sem=55)
    quieto(lz, A5, t, "pamela_hoja/01", 0.52, 0.80, 0.24, tono=NOCHE, fase=0.4)
    a = 1.0 - smooth(prog(t, t_dejo, t_dejo + 0.3))
    quieto(lz, A5, t, "joseph_hoja/01", 0.40, 0.86, 0.46, tono=NOCHE, op=a, flip=True)
    if t >= t_dejo:
        paseo(lz, A5, t, "joseph_hoja/05", t_dejo, t_dejo + 3.6, 0.40, -0.15, 0.84, 0.46, tono=NOCHE, pasos=2.0)
    quieto(lz, A5, t, "familia_hoja/01", 0.645, 0.64, 0.30, tono=VELA, t_in=t_marA - 0.2)
    real(lz, "marlene_cos", W * 0.85, H * 0.30, H * 0.40, t, t_marA, rot=5)
    rot_(lz, "TÍA MARLENE", W * 0.85, H * 0.55, 36, t, t_marA + 0.2)
    niebla(lz, t, NIEBLA_VERDE[:2])


A6 = PF.Plano("escondite", t_y5 - 0.3, _ESC[HO]["t0"] + 0.4, z0=1.06, z1=1.10, c0=(0.48, 0.58), c1=(0.48, 0.58), par=(26, 6))
A6b = PF.Plano("escondite", t_pasara - 0.6, t_pasara + 2.4, z0=1.10, z1=1.62, c0=(0.48, 0.58), c1=(0.22, 0.52), par=(26, 6))
snd(t_escondio, "golpe_suave", 0.5)
snd(t_pidio, "latido", 0.6)
wow(t_y5, "vela", 0.4)


@toma(t_y5 - 0.3, ("negro", 0.6))
def a6(lz, t):
    pl = A6 if t < t_pasara - 0.6 else A6b
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.785, 0.72, 70, color=(1.0, 0.6, 0.25), inten=0.55, sem=56)        # la vela del suelo
    brillo_en(lz, pl, t, 0.53, 0.25, 140, color=(0.55, 0.75, 1.0), inten=0.12, sem=57)      # luna por la ventana
    if t < t_escondio:
        paseo(lz, pl, t, "pamela_hoja/05", t_y5, t_escondio, 0.55, 0.30, 0.86, 0.26, tono=NOCHE, pasos=2.6)
    else:
        quieto(lz, pl, t, "pamela_hoja/03", 0.175, 0.64, 0.20, tono=(0.5, 0.56, 0.72), t_in=t_escondio)
    a = 1.0 - smooth(prog(t, t_pasara - 0.6, t_pasara - 0.2))
    quieto(lz, pl, t, "familia_hoja/02", 0.46, 0.90, 0.40, tono=VELA, op=a)
    quieto(lz, pl, t, "familia_hoja/01", 0.50, 0.90, 0.52, tono=VELA, op=1 - a, flip=True)
    niebla(lz, t, [("fx_hoja/06", 0.97, 300, 10, 0.30, 0.4)])


# ================================================================== HORGUS (170,9 - …): arranque
t0HO = _ESC[HO]["t0"]
t_colinas, t_oleada = T(HO, "colinas", 0), T(HO, "oleada", 0)
t_yano, t_necro, t_rapidos, t_horgus = T(HO, "ya", 1), T(HO, "necrófagos", 1, n=0), T(HO, "rápidos", 1), T(HO, "horgus", 1)

H1 = PF.Plano("colinas_noche_b", t0HO - 0.3, t_yano, z0=1.04, z1=1.20, c0=(0.50, 0.55), c1=(0.56, 0.60), par=(34, 8))
wow(t_oleada - 0.3, "necrofago", 0.8)
wow(t_oleada + 0.7, "necrofago2", 0.7)
wow(t0HO + 0.2, "lobo", 0.4)


@toma(t0HO - 0.3, ("negro", 0.7))
def h1(lz, t):
    H1.fondo(lz, t)
    brillo_en(lz, H1, t, 0.63, 0.12, 90, color=(0.7, 0.9, 1.0), inten=0.18, sem=60)
    brillo_en(lz, H1, t, 0.68, 0.63, 60, color=(1.0, 0.6, 0.25), inten=0.30, sem=61)
    for k in range(7):
        y = 0.72 + 0.035 * (k % 4)
        ta = t0HO - 0.3 + 0.45 * k
        anda(lz, H1, t, "necrofago_corre", ta, ta + 3.2, 1.12, 0.10 + 0.06 * k, y, 0.18 + 0.05 * (k % 4), paso=1.35,
             tono=NOCHE_PESTE)
    niebla(lz, t, NIEBLA_VERDE)


H2 = PF.Plano("barricadas_b", t_yano - 0.4, t_yano + 12.0, z0=1.06, z1=1.20, c0=(0.50, 0.58), c1=(0.46, 0.56), par=(30, 8))
wow(t_necro, "necrofago", 0.6)
wow(t_horgus - 0.2, "necrofago2", 0.8)
snd(t_horgus, "golpe_grave", 0.9)


@toma(t_yano - 0.4, ("latigo", 0.45))
def h2(lz, t):
    H2.fondo(lz, t)
    brillo_en(lz, H2, t, 0.66, 0.60, 100, color=(1.0, 0.55, 0.2), inten=0.5, sem=62, chis=7)
    brillo_en(lz, H2, t, 0.395, 0.46, 30, color=(1.0, 0.6, 0.25), inten=0.4, sem=63)
    for k in range(8):
        ta = t_yano - 0.4 + 0.9 * k
        y = 0.80 + 0.04 * (k % 3)
        anda(lz, H2, t, "necrofago_corre", ta, ta + 2.6, 1.15, -0.15, y, 0.30 + 0.06 * (k % 3), paso=1.35, tono=NOCHE_PESTE)
    real(lz, "ghoul", W * 0.20, H * 0.32, H * 0.40, t, t_necro, t_horgus - 0.4, rot=-5)
    rot_(lz, "NECRÓFAGOS CAMPEONES", W * 0.20, H * 0.58, 38, t, t_necro + 0.2, t_horgus - 0.4)
    real(lz, "horgus", W * 0.72, H * 0.45, H * 0.70, t, t_horgus - 0.1, rot=3)
    rot_(lz, "HORGUS EL DEVASTADOR", W * 0.72, H * 0.88, 46, t, t_horgus + 0.3)
    niebla(lz, t, NIEBLA_VERDE[:2])


# ================================================================== TANDA 2 (20-oct-2026, sesión 3): de 3:06 al final
# ------------------------------------------------------------------ ayudantes nuevos (no tocan las tomas de 0-186 s)
def F(eid, i, fin=False):
    """Inicio (o fin) de la frase i de la escena."""
    fr = _ESC[eid]["frases"][i]
    return fr["t1"] if fin else fr["t0"]


FALTAN = []


def Ts(eid, pref, frase, n=0):
    """T() que no revienta: si Whisper no tiene la palabra, cae al inicio de la frase (y lo anota en FALTAN)."""
    try:
        return T(eid, pref, frase, n)
    except KeyError:
        FALTAN.append((eid, pref, frase))
        return F(eid, frase)


SOMBRA_T = (0.62, 0.80, 0.66)
FANT_OSC = (0.42, 0.62, 0.70)


def sombra_pz(lz, pl, t, pieza, x, y, frac, op=0.92, flip=False, t_in=None, t_out=None, rot=0.0, humo=True):
    """La sombra corrompida (Rutagrana) o el jinete espectral: pieza oscura con halo verde, humo negro y temblor."""
    a = 1.0
    if t_in is not None:
        a = smooth(prog(t, t_in, t_in + 0.8))
    if t_out is not None:
        a *= 1.0 - smooth(prog(t, t_out, t_out + 0.6))
    if a <= 0.01:
        return
    X, Y, h = pl.en(t, x, y, frac)
    if humo:
        PF.humo(lz, t, X, Y - 0.35 * h, s=h / 420, color=(0.04, 0.06, 0.05), op=0.30 * a, sem=9, alto=h * 0.8)
    PF.brillo(lz, X, Y - 0.55 * h, 1.1 * h, color=(0.3, 1.0, 0.4), inten=0.20 * a, t=t, sem=8)
    PF.actor(lz, pieza, X + 3 * math.sin(t * 9.0), Y, h, flip=flip, op=op * a, tono=SOMBRA_T, rot=rot, sy=PF.respira(t))


@functools.lru_cache(maxsize=64)
def _txt(txt, px, color=(255, 255, 255), fnt="serif", borde=3):
    f = D.fuente(fnt, px)
    x0, y0, x1, y1 = f.getbbox(txt)
    w, h = x1 - x0 + 2 * borde + 12, y1 - y0 + 2 * borde + 12
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ox, oy = 6 + borde - x0, 6 + borde - y0
    for dx in range(-borde, borde + 1, max(1, borde)):
        for dy in range(-borde, borde + 1, max(1, borde)):
            d.text((ox + dx, oy + dy), txt, font=f, fill=(6, 4, 2, 255))
    d.text((ox, oy), txt, font=f, fill=tuple(color) + (255,))
    a = np.asarray(im, np.uint8)
    return D.Sprite(a[..., :3].copy(), a[..., 3].astype(np.float32) / 255.0, sombra=False)


def texto(lz, txt, X, Y, px, op=1.0, color=(255, 255, 255), fnt="serif", ancla="c"):
    """Texto de interfaz con contorno negro; ancla 'c' (centro) o 'i' (borde izquierdo)."""
    if op <= 0.01:
        return
    spr = _txt(txt, int(px), tuple(color), fnt)
    x = X - spr.w / 2 if ancla == "c" else X
    D.pegar(lz, spr, np.array([[1, 0, x], [0, 1, Y - spr.h / 2], [0, 0, 1]], np.float64), op)


def panel(lz, x0, y0, x1, y1, op=0.85, color=(0.03, 0.04, 0.10), borde=(0.78, 0.62, 0.33)):
    """Recuadro de la interfaz de WoW (azul noche con filete dorado)."""
    x0, y0, x1, y1 = (int(round(v)) for v in (x0, y0, x1, y1))
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0 or op <= 0.01:
        return
    lz[y0:y1, x0:x1] = lz[y0:y1, x0:x1] * (1 - op) + np.float32(color) * op
    for (a, b, c, d) in ((y0, y0 + 3, x0, x1), (y1 - 3, y1, x0, x1), (y0, y1, x0, x0 + 3), (y0, y1, x1 - 3, x1)):
        lz[a:b, c:d] = lz[a:b, c:d] * (1 - op) + np.float32(borde) * op


def objeto(lz, t, icono, nombre, sub, X, Y, t_in, t_out=None, px=40, linea=None):
    """Tooltip de objeto de WoW: icono REAL (piezas/iconos) + nombre + «Objeto de misión»; X, Y = esquina izq. del icono."""
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.4)
    o = clamp01(u * 3) * (1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.35)))
    if o <= 0.01:
        return
    lado = px * 2.8
    ancho = max(len(nombre) * px * 0.56, len(sub) * px * 0.42, len(linea or "") * px * 0.40) + 60
    panel(lz, X + lado + 10, Y - 6, X + lado + 30 + ancho, Y + lado + 6 + (px * 0.9 if linea else 0), op=0.82 * o)
    PF.actor(lz, f"iconos/{icono}", X + lado / 2, Y + lado / 2, lado * (0.7 + 0.3 * u), op=o, ancla=(0.5, 0.5), suelo=0,
             sombra=True)
    texto(lz, nombre, X + lado + 30, Y + px * 0.75, px, o, (255, 209, 0), ancla="i")
    texto(lz, sub, X + lado + 30, Y + px * 1.85, int(px * 0.72), o, (255, 255, 255), "serif_sb", ancla="i")
    if linea:
        texto(lz, linea, X + lado + 30, Y + px * 2.75, int(px * 0.66), o, (255, 209, 0), "serif_i", ancla="i")


def rastreador(lz, t, titulo, lineas, t_in, t_out=None, X=W * 0.70, Y=H * 0.10, px=36):
    """Seguimiento de misión (arriba a la derecha): título amarillo y objetivos «- texto: n/m» (lineas = [(txt, valor(t))])."""
    if t < t_in:
        return
    o = clamp01((t - t_in) / 0.4) * (1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.4)))
    if o <= 0.01:
        return
    panel(lz, X - 20, Y - px * 0.9, X + px * 13.5, Y + px * (1.3 * len(lineas) + 0.9), op=0.45 * o, color=(0, 0, 0),
          borde=(0.1, 0.1, 0.1))
    texto(lz, titulo, X, Y, px, o, (255, 209, 0), ancla="i")
    for k, (txt, val) in enumerate(lineas):
        hecho = val.endswith("(Completo)") or (val.split("/")[0] == val.split("/")[-1] if "/" in val else False)
        texto(lz, f"- {txt}: {val}", X + 14, Y + px * 1.3 * (k + 1), int(px * 0.82), o,
              (150, 255, 150) if hecho else (255, 255, 255), "serif_sb", ancla="i")


def marco_unidad(lz, t, X, Y, retrato, nombre, vida, t_in, color=(0.10, 0.80, 0.10), ancho=430, op=1.0):
    """Marco de unidad de WoW: retrato redondo (piezas/medallon), nombre y barra de vida (vida 0..1)."""
    if t < t_in:
        return
    o = op * clamp01((t - t_in) / 0.4)
    r = 62
    panel(lz, X + r, Y - 34, X + r + ancho, Y + 40, op=0.75 * o)
    x0, x1 = int(X + r + 14), int(X + r + ancho - 14)
    y0, y1 = int(Y + 2), int(Y + 26)
    lz[y0:y1, x0:x1] = lz[y0:y1, x0:x1] * (1 - 0.8 * o) + np.float32((0.1, 0.02, 0.02)) * 0.8 * o
    xf = int(x0 + (x1 - x0) * clamp01(vida))
    if xf > x0:
        lz[y0:y1, x0:xf] = lz[y0:y1, x0:xf] * (1 - 0.9 * o) + np.float32(color) * 0.9 * o
    texto(lz, nombre, X + r + 20, Y - 14, 28, o, (255, 209, 0), ancla="i")
    texto(lz, f"{int(round(100 * clamp01(vida)))} %", (x0 + x1) / 2, Y + 14, 22, o, fnt="sans")
    PF.actor(lz, f"medallon/{retrato}", X, Y, 2 * r, op=o, ancla=(0.5, 0.5), suelo=0)


def barra_lanzar(lz, t, X, Y, nombre, t0, t1, ancho=620, color=(0.85, 0.35, 0.95), op=1.0):
    """Barra de lanzamiento de hechizo (se llena de t0 a t1) con el nombre centrado."""
    if t < t0 - 0.2:
        return
    o = op * clamp01((t - t0 + 0.2) / 0.3)
    u = clamp01((t - t0) / max(t1 - t0, 1e-3))
    panel(lz, X - ancho / 2 - 8, Y - 26, X + ancho / 2 + 8, Y + 26, op=0.85 * o, color=(0.02, 0.02, 0.02))
    x0, y0, y1 = int(X - ancho / 2), int(Y - 18), int(Y + 18)
    xf = int(x0 + ancho * u)
    if xf > x0:
        lz[y0:y1, x0:xf] = lz[y0:y1, x0:xf] * (1 - 0.9 * o) + np.float32(color) * 0.9 * o
    texto(lz, nombre, X, Y, 28, o, fnt="sans")


@functools.lru_cache(maxsize=2)
def _escarcha_campo():
    r = np.random.default_rng(21)
    h2, w2 = H // 2, W // 2
    n = cv2.GaussianBlur(r.random((h2, w2)).astype(np.float32), (0, 0), 9)
    n = (n - n.mean()) / (n.std() + 1e-6)
    fino = cv2.GaussianBlur(r.random((h2, w2)).astype(np.float32), (0, 0), 1.0)
    fino = (fino - fino.min()) / (fino.max() - fino.min() + 1e-6)
    Y, X = np.mgrid[0:h2, 0:w2].astype(np.float32)
    borde = np.minimum(np.minimum(X, w2 - X) / w2, np.minimum(Y, h2 - Y) / h2)
    return borde * 2.2 + 0.035 * n, fino


def escarcha(lz, k):
    """Escarcha que crece desde los bordes del cuadro (k 0..1), con grano de hielo."""
    if k <= 0.01:
        return
    c, fino = _escarcha_campo()
    m = np.clip((0.55 * k - c) / 0.22, 0, 1) * (0.85 + 0.3 * fino)
    m = cv2.resize(np.clip(m, 0, 1), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    lz[:] = lz * (1 - 0.55 * m) + np.float32((0.80, 0.90, 1.0)) * 0.55 * m


def ruta_tinta(lz, pl, t, pts, t0, t1, color=TINTA, grosor=5.0, op=1.0):
    """Polilínea de tinta en coordenadas del escenario que se traza de t0 a t1."""
    if t < t0:
        return
    P = [pl.P(t, x, y)[:2] for x, y in pts]
    L = [math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1)]
    rest = smooth(prog(t, t0, t1)) * sum(L)
    pp = [P[0]]
    for i in range(len(L)):
        if rest <= 0:
            break
        k = min(1.0, rest / max(L[i], 1e-3))
        pp.append((lerp(P[i][0], P[i + 1][0], k), lerp(P[i][1], P[i + 1][1], k)))
        rest -= L[i]
    if len(pp) > 1:
        D.linea_aa(lz, pp, color, grosor=grosor, op=op, sombra=False)


def lazo(lz, a, b, t, u, color=(0.35, 1.0, 0.45), n=3, amp=40.0, grosor=4.0, op=0.8, sem=0):
    """Cintas de energía (alma arrancada, contagio) de a hacia b en pantalla; u = cuánto han avanzado (0..1)."""
    if u <= 0.01:
        return
    (xa, ya), (xb, yb) = a, b
    for k in range(n):
        pts = []
        for i in range(25):
            s = i / 24 * u
            x, y = lerp(xa, xb, s), lerp(ya, yb, s)
            nx, ny = -(yb - ya), xb - xa
            ln = math.hypot(nx, ny) + 1e-6
            w = amp * math.sin(s * math.pi) * math.sin(s * 7 + t * (5 + k) + k * 2.1 + sem)
            pts.append((x + nx / ln * w, y + ny / ln * w))
        D.linea_aa(lz, pts, color, grosor=grosor, op=op * (0.6 + 0.4 * math.sin(t * 6 + k)), sombra=False)
    PF.brillo(lz, lerp(xa, xb, u), lerp(ya, yb, u), 60, color=color, inten=0.4 * op, t=t, sem=sem)


def golpe_de(t, tiempos, k=6.0):
    return max([math.exp(-(t - tg) * k) if t >= tg else 0.0 for tg in tiempos] + [0.0])


def sacude(lz, a, t):
    """Sacudida de cámara (a = px)."""
    if a < 0.5:
        return
    dx, dy = int(a * math.sin(t * 61)), int(a * math.cos(t * 47))
    lz[:] = np.roll(np.roll(lz, dx, axis=1), dy, axis=0)


def destello_pant(lz, k, color=(1.0, 0.95, 0.8)):
    if k > 0.003:
        lz[:] = lz * (1 - k) + np.float32(color) * k


HO2, MA, CT = "horgus", "marduk", "cta_mitad"
MIRA.update({"davil_hoja/03": 1, "aventurero_hoja/00": 1, "pamela_corre": 1, "marduk_galope": 1, "reencuentro_hoja/01": 1,
             "monstruos_hoja/06": 1})

# ================================================================== HORGUS (desde 186,1)
t_linea = F(HO2, 2)
t_justo, t_refu, t_palH, t_davil, t_hijo = (F(HO2, 3), Ts(HO2, "refuerzos", 3), Ts(HO2, "paladines", 3), Ts(HO2, "davil", 3),
                                            Ts(HO2, "hijo", 3))
t_noper = F(HO2, 4)
t_busco, t_luzH, t_disfr = F(HO2, 5), Ts(HO2, "luz", 5), Ts(HO2, "disfrutar", 5)
t_pelea, t_mato = F(HO2, 6), Ts(HO2, "mató", 6)
t_herida, t_despH = F(HO2, 7), Ts(HO2, "después", 7)

wow(t_linea - 0.3, "hoguera", 0.45, dur=3.8, fade=0.6)
for tg in (t_linea + 0.4, t_linea + 1.5, t_linea + 2.4):
    wow(tg, "espada_escudo", 0.5)
wow(t_linea + 0.8, "necrofago", 0.6)
I1 = PF.Plano("batalla_calle_a", t_linea - 0.3, t_justo, z0=1.06, z1=1.22, c0=(0.50, 0.62), c1=(0.44, 0.60), par=(30, 8))


@toma(t_linea - 0.3, ("latigo", 0.4))
def h3(lz, t):
    I1.fondo(lz, t)
    brillo_en(lz, I1, t, 0.80, 0.20, 120, inten=0.5, sem=70, chis=6)
    brillo_en(lz, I1, t, 0.62, 0.50, 90, inten=0.5, sem=71, chis=6)
    # los defensores retroceden mientras los necrófagos saltan la barricada rota
    for k, (pz, x0, fr) in enumerate((("defensores_hoja/00", 0.30, 0.40), ("defensores_hoja/02", 0.52, 0.38),
                                      ("defensores_hoja/03", 0.70, 0.42))):
        paseo(lz, I1, t, pz, t_linea, t_justo, x0, x0 + 0.10, 0.90 + 0.02 * k, fr, tono=FUEGO_NOCHE, pasos=2.6, flip=True)
    for k in range(5):
        ta = t_linea - 0.3 + 0.55 * k
        anda(lz, I1, t, "necrofago_corre", ta, ta + 2.2, -0.15, 0.45 + 0.08 * k, 0.80 + 0.03 * (k % 3), 0.24 + 0.04 * (k % 2),
             paso=1.35, tono=NOCHE_PESTE)
    caida = smooth(prog(t, t_linea + 1.4, t_linea + 1.9))
    X, Y, h = I1.en(t, 0.20, 0.97, 0.40)
    PF.actor(lz, "defensores_hoja/05", X, Y, h, tono=FUEGO_NOCHE, rot=-80 * caida, op=1 - 0.3 * caida)
    niebla(lz, t, NIEBLA_VERDE)
    sacude(lz, 6 * golpe_de(t, (t_linea + 0.4, t_linea + 1.5, t_linea + 2.4)), t)


I2 = PF.Plano("colina_refuerzos_a", t_justo - 0.3, t_noper, z0=1.04, z1=1.20, c0=(0.52, 0.55), c1=(0.56, 0.50), par=(34, 8))
wow(t_refu, "luz_sagrada", 0.8)
wow(t_palH, "campana", 0.5)
snd(t_palH, "galope", 0.7, dur=4.0)
wow(t_davil + 0.2, "grito_guerra", 0.5)


@toma(t_justo - 0.3, ("destello", 0.6))
def h4(lz, t):
    I2.fondo(lz, t)
    k = smooth(prog(t, t_refu - 0.5, t_refu + 1.0))
    brillo_en(lz, I2, t, 0.56, 0.30, 380, color=(1.0, 0.85, 0.45), inten=0.25 + 0.35 * k, sem=72)
    brillo_en(lz, I2, t, 0.10, 0.55, 60, inten=0.4, sem=73, chis=4)
    # los paladines bajan por el camino desde la luz y crecen con la perspectiva (lo lejano se dibuja antes)
    grupo = []
    for j, (ta, x1, y1, f1, pz) in enumerate(((t_justo - 2.0, 0.30, 0.86, 0.36, "defensores_hoja/01"),
                                              (t_justo - 1.0, 0.70, 0.88, 0.38, "defensores_hoja/01"),
                                              (t_justo + 0.6, 0.22, 0.80, 0.30, "defensores_hoja/00"),
                                              (t_refu - 0.5, 0.66, 0.82, 0.30, "defensores_hoja/01"),
                                              (t_davil - 2.2, 0.50, 0.97, 0.58, "davil_hoja/03"))):
        u = clamp01((t - ta) / 6.0)
        grupo.append((lerp(0.50, y1, u), pz, lerp(0.555, x1, u), lerp(0.10, f1, u ** 1.4), u, ta))
    for y, pz, x, fr, u, ta in sorted(grupo):
        if t < ta:
            continue
        X, Y, h = I2.en(t, x, y, fr)
        bote = abs(math.sin((t - ta) * 2.2 * math.pi)) * 0.03 * h * (u < 1)
        PF.actor(lz, pz, X, Y - bote, h, tono=(1.02, 0.97, 0.88), op=clamp01((t - ta) * 2), rot=3 * math.sin((t - ta) * 7) * (u < 1),
                 flip=(pz.startswith("davil") and False) or (x < 0.5 and not pz.startswith("davil")))
    real(lz, "davil", W * 0.87, H * 0.30, H * 0.44, t, t_davil, rot=4)
    rot_(lz, "DAVIL FUEGOLUZ", W * 0.86, H * 0.58, 46, t, t_davil + 0.2)
    rot_(lz, "un hijo del pueblo", W * 0.86, H * 0.66, 32, t, t_hijo, rot=1.5)
    rot_(lz, "LA MANO DE PLATA", W * 0.24, H * 0.14, 48, t, t_palH, t_davil - 0.2)
    niebla(lz, t, NIEBLA_VERDE[:2])


I3 = PF.Plano("plaza_batalla_a", t_noper - 0.3, t_busco, z0=1.10, z1=1.24, c0=(0.48, 0.62), c1=(0.46, 0.60), par=(30, 8))
wow(t_noper, "grito_guerra", 0.9)
wow(t_noper + 0.2, "luz_impacto", 0.6)


@toma(t_noper - 0.3, ("latigo", 0.4))
def h5(lz, t):
    I3.fondo(lz, t)
    brillo_en(lz, I3, t, 0.72, 0.50, 120, inten=0.5, sem=74, chis=6)
    X, Y, h = I3.en(t, 0.46, 0.96, 0.62)
    PF.brillo(lz, X - 0.15 * h, Y - 1.0 * h, 0.9 * h, color=(1.0, 0.85, 0.4), inten=0.5 + 0.2 * math.sin(t * 7), t=t, sem=75)
    PF.actor(lz, "davil_hoja/00", X, Y, h, tono=(1.02, 0.96, 0.88), sy=PF.respira(t, a=0.02))
    PF.chispas(lz, t, X - 0.15 * h, Y - 1.0 * h, s=1.4, n=10, sem=76)
    for k, (pz, x, fr) in enumerate((("defensores_hoja/00", 0.18, 0.44), ("defensores_hoja/02", 0.78, 0.46),
                                     ("defensores_hoja/05", 0.90, 0.50))):
        salto = abs(math.sin((t - t_noper) * 3.4 + k))
        X2, Y2, h2 = I3.en(t, x, 0.94, fr)
        PF.actor(lz, pz, X2, Y2 - 0.05 * h2 * salto, h2, tono=FUEGO_NOCHE, flip=x > 0.5)
    niebla(lz, t, NIEBLA_VERDE[:2])


I4 = PF.Plano("plaza_batalla_b", t_busco - 0.3, t_luzH + 0.2, z0=1.04, z1=1.14, c0=(0.50, 0.60), c1=(0.52, 0.60), par=(30, 8))
I4b = PF.Plano("plaza_batalla_b", t_luzH - 0.2, t_pelea, z0=1.45, z1=1.75, c0=(0.66, 0.62), c1=(0.70, 0.58), par=(30, 8))
wow(t_busco, "necrofago2", 0.8)
wow(t_luzH, "necrofago", 0.5)
snd(t_disfr, "latido", 0.6)


@toma(t_busco - 0.3, ("negro", 0.5))
def h6(lz, t):
    pl = I4 if t < t_luzH - 0.2 else I4b
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.55, 0.55, 100, inten=0.5, sem=77, chis=5)
    brillo_en(lz, pl, t, 0.80, 0.47, 70, inten=0.45, sem=78)
    X, Y, h = pl.en(t, 0.24, 0.96, 0.52)
    PF.brillo(lz, X, Y - 0.6 * h, 0.8 * h, color=(1.0, 0.85, 0.4), inten=0.3, t=t, sem=79)
    PF.actor(lz, "davil_hoja/02", X, Y, h, tono=FUEGO_NOCHE, sy=PF.respira(t))
    u = smooth(prog(t, t_busco, t_luzH))
    pz = "horgus_hoja/00" if t < t_luzH else "horgus_hoja/01"
    X2, Y2, h2 = pl.en(t, lerp(0.95, 0.68, u), 0.95, 0.64)
    PF.brillo(lz, X2, Y2 - 0.75 * h2, 0.35 * h2, color=(0.3, 1.0, 0.4), inten=0.35, t=t, sem=80)
    PF.actor(lz, pz, X2, Y2 - (abs(math.sin(t * 4)) * 0.02 * h2 if t < t_luzH else 0), h2, tono=NOCHE_PESTE,
             sy=PF.respira(t, a=0.025))
    niebla(lz, t, NIEBLA_VERDE)
    sacude(lz, 4 * golpe_de(t, (t_luzH,), 3.0), t)


GOLPES_H = [t_pelea + 0.3, t_pelea + 1.4, t_pelea + 2.5, t_mato]
for k, tg in enumerate(GOLPES_H):
    wow(tg, "espada_carne" if k % 2 else "espada_escudo", 0.7)
wow(t_mato + 0.05, "luz_impacto", 0.9)
wow(t_mato + 0.4, "necrofago2", 0.5)
I5 = PF.Plano("duelo_fuego_a", t_pelea - 0.3, t_herida, z0=1.10, z1=1.22, c0=(0.50, 0.62), c1=(0.48, 0.64), par=(30, 8))


@toma(t_pelea - 0.3, ("latigo", 0.4))
def h7(lz, t):
    I5.fondo(lz, t)
    brillo_en(lz, I5, t, 0.72, 0.25, 220, inten=0.45, sem=81, chis=10)
    g = golpe_de(t, GOLPES_H, 5.0)
    muerto = t >= t_mato
    alterna = int((t - t_pelea) / 1.1) % 2 == 0
    X, Y, h = I5.en(t, 0.36 + 0.03 * g, 0.95, 0.50)
    PF.actor(lz, "davil_hoja/01" if (alterna or muerto) else "davil_hoja/02", X, Y, h, tono=FUEGO_NOCHE, rot=-6 * g)
    PF.brillo(lz, X + 0.1 * h, Y - 0.85 * h, 0.5 * h, color=(1.0, 0.85, 0.4), inten=0.3 + 0.4 * g, t=t, sem=82)
    if not muerto:
        X2, Y2, h2 = I5.en(t, 0.62 - 0.03 * g, 0.95, 0.60)
        PF.actor(lz, "horgus_hoja/02" if not alterna else "horgus_hoja/01", X2, Y2, h2, tono=NOCHE_PESTE, flip=True, rot=5 * g)
    else:
        c = smooth(prog(t, t_mato, t_mato + 0.6))
        X2, Y2, h2 = I5.en(t, 0.64, 0.95, 0.60)
        PF.actor(lz, "horgus_hoja/03" if c < 0.99 else "horgus_hoja/04", X2, Y2, h2 * (1 - 0.35 * c), tono=NOCHE_PESTE,
                 flip=True)
    destello_pant(lz, 0.55 * golpe_de(t, (t_mato,), 4.0), (1.0, 0.92, 0.6))
    niebla(lz, t, NIEBLA_VERDE[:2])
    sacude(lz, 7 * g, t)


I6 = PF.Plano("duelo_fuego_b", t_herida - 0.3, F(MA, 0), z0=1.20, z1=1.05, c0=(0.42, 0.66), c1=(0.48, 0.60), par=(30, 8))
snd(t_herida + 0.5, "latido", 0.5)
snd(t_despH, "golpe_suave", 0.5)


@toma(t_herida - 0.3, ("fundido", 0.6))
def h8(lz, t):
    I6.fondo(lz, t)
    brillo_en(lz, I6, t, 0.65, 0.30, 200, inten=0.40, sem=83, chis=6)
    quieto(lz, I6, t, "horgus_hoja/04", 0.70, 0.86, 0.22, tono=NOCHE_PESTE)
    c = smooth(prog(t, t_despH - 0.6, t_despH + 0.6))
    X, Y, h = I6.en(t, 0.38, 0.95, 0.44)
    luz = 1.0 - smooth(prog(t, t_herida + 1.0, t_despH + 1.0))
    PF.brillo(lz, X, Y - 0.4 * h, 1.0 * h, color=(1.0, 0.85, 0.4), inten=0.4 * luz, t=t, sem=84)
    PF.actor(lz, "davil_hoja/04", X, Y, h, tono=FUEGO_NOCHE, op=1 - c, sy=PF.respira(t, f=0.8, a=0.02))
    if c > 0:
        X2, Y2, h2 = I6.en(t, 0.40, 0.96, 0.20)
        PF.actor(lz, "davil_hoja/05", X2, Y2, h2, tono=FUEGO_NOCHE, op=c)
    for k, x in enumerate((0.20, 0.58)):
        quieto(lz, I6, t, "defensores_hoja/00" if k == 0 else "defensores_hoja/03", x, 0.93, 0.40, tono=FUEGO_NOCHE,
               flip=k == 1, fase=k)
    tinte(lz, (0.6, 0.7, 0.8), 0.35 * c)
    niebla(lz, t, NIEBLA_AZUL[:1])


# ================================================================== MARDUK (225,5 - 283,6)
t_mando, t_anales, t_ganado = F(MA, 0), Ts(MA, "anales", 0), Ts(MA, "ganado", 0)
t_entonM, t_cab, t_marduk = F(MA, 1), Ts(MA, "caballero", 1), Ts(MA, "marduk", 1)
t_grito, t_noMato, t_arranco = F(MA, 2), F(MA, 3), Ts(MA, "arrancó", 3)
t_retorc, t_sombra, t_corromp = F(MA, 4), Ts(MA, "sombra", 4), Ts(MA, "rutagrana", 4)
t_contag, t_vuelta, t_atac, t_entra = F(MA, 5), F(MA, 6), Ts(MA, "atacaron", 6), Ts(MA, "entraron", 6)
t_casas, t_ninos, t_nadie = F(MA, 7), Ts(MA, "niños", 7), F(MA, 8)

wow(t_mando, "grito_guerra", 0.5)
snd(t_anales, "papel", 0.6)
wow(t_anales + 0.1, "pagina", 0.6)
M1 = PF.Plano("batalla_calle_b", t_mando - 0.3, t_entonM, z0=1.04, z1=1.18, c0=(0.50, 0.62), c1=(0.54, 0.58), par=(30, 8))


@toma(t_mando - 0.3, ("fundido", 0.6))
def m1(lz, t):
    M1.fondo(lz, t)
    brillo_en(lz, M1, t, 0.58, 0.52, 100, inten=0.5, sem=85, chis=6)
    brillo_en(lz, M1, t, 0.88, 0.18, 120, inten=0.45, sem=86, chis=4)
    for k, (pz, x, fr) in enumerate((("defensores_hoja/03", 0.14, 0.40), ("defensores_hoja/00", 0.70, 0.44),
                                     ("defensores_hoja/02", 0.84, 0.46))):
        quieto(lz, M1, t, pz, x, 0.92, fr, tono=FUEGO_NOCHE, flip=x > 0.5, fase=k)
    X, Y, h = M1.en(t, 0.40, 0.97, 0.58)
    PF.actor(lz, "joseph_hoja/03", X, Y, h, tono=FUEGO_NOCHE, sy=PF.respira(t, a=0.02))
    rot_(lz, "CAPITÁN JOSEPH RUTAGRANA", W * 0.5, H * 0.12, 52, t, t_mando + 0.4, t_anales - 0.3)
    pega(lz, "utileria2/04", W * 0.78, H * 0.34, H * 0.34, t, t_anales - 0.1, rot=-8)
    objeto(lz, t, "anales", "Los Anales de Villa Darrow", "Objeto de misión", W * 0.03, H * 0.06, t_anales + 0.3, t_ganado - 0.4)
    rot_(lz, "PUDO HABER GANADO", W * 0.5, H * 0.12, 56, t, t_ganado - 0.1)
    niebla(lz, t, NIEBLA_VERDE[:2])


M2 = PF.Plano("puerta_humo_a", t_entonM - 0.3, t_grito, z0=1.08, z1=1.20, c0=(0.52, 0.56), c1=(0.52, 0.60), par=(30, 8))
wow(t_entonM, "dk_hechizo", 0.6)
snd(t_cab - 0.4, "galope", 0.9, dur=3.0)
wow(t_marduk, "dk_impacto", 0.8)
snd(t_marduk, "golpe_grave", 0.8)


@toma(t_entonM - 0.3, ("negro", 0.6))
def m2(lz, t):
    M2.fondo(lz, t)
    brillo_en(lz, M2, t, 0.30, 0.72, 60, inten=0.4, sem=87, chis=3)
    brillo_en(lz, M2, t, 0.73, 0.72, 60, inten=0.4, sem=88, chis=3)
    humo_en(lz, M2, t, 0.52, 0.50, s=1.8, color=(0.05, 0.06, 0.05), op=0.40, sem=7)
    # el caballero de la muerte sale del humo al galope
    if t > t_cab - 0.6:
        u = clamp01((t - t_cab + 0.6) / 2.4)
        X, Y, h = M2.en(t, lerp(0.40, 0.62, u), lerp(0.62, 0.92, u), lerp(0.18, 0.55, u))
        n = PF.ciclo_n("marduk_galope")
        i = int((t - t_cab) * 10) % n
        PF.brillo(lz, X, Y - 0.5 * h, 0.9 * h, color=(0.3, 1.0, 0.5), inten=0.25, t=t, sem=89)
        PF.actor(lz, f"marduk_galope/ciclo_{i:02d}", X, Y, h * 1.25, tono=(0.8, 0.9, 0.85))
    real(lz, "marduk", W * 0.20, H * 0.36, H * 0.50, t, t_marduk - 0.1, rot=-4)
    rot_(lz, "MARDUK EL NEGRO", W * 0.20, H * 0.70, 48, t, t_marduk + 0.2)
    rot_(lz, "caballero de la muerte", W * 0.20, H * 0.78, 32, t, t_marduk + 0.5, rot=1)
    niebla(lz, t, NIEBLA_VERDE)


M3 = PF.Plano("plaza_marduk_a", t_grito - 0.3, t_noMato, z0=1.20, z1=1.32, c0=(0.50, 0.66), c1=(0.52, 0.64), par=(30, 8))
wow(t_grito, "dk_hechizo", 0.5)
snd(t_grito + 0.1, "golpe_grave", 0.7)


@toma(t_grito - 0.3, ("latigo", 0.4))
def m3(lz, t):
    M3.fondo(lz, t)
    brillo_en(lz, M3, t, 0.68, 0.40, 160, color=(0.35, 1.0, 0.4), inten=0.35, sem=90)
    brillo_en(lz, M3, t, 0.73, 0.74, 40, inten=0.4, sem=91)
    X, Y, h = M3.en(t, 0.30, 0.98, 0.56)
    PF.actor(lz, "joseph_hoja/03", X, Y, h, tono=NOCHE_PESTE, flip=False)
    X2, Y2, h2 = M3.en(t, 0.70, 0.98, 0.62)
    PF.brillo(lz, X2, Y2 - 0.8 * h2, 0.4 * h2, color=(0.4, 1.0, 0.6), inten=0.35, t=t, sem=92)
    PF.actor(lz, "marduk_hoja/00", X2, Y2, h2, tono=(0.85, 0.92, 0.9), sy=PF.respira(t))
    niebla(lz, t, NIEBLA_VERDE)
    sacude(lz, 5 * golpe_de(t, (t_grito + 0.1,), 4.0), t)


M4 = PF.Plano("plaza_marduk_b", t_noMato - 0.3, t_retorc, z0=1.10, z1=1.28, c0=(0.50, 0.64), c1=(0.48, 0.62), par=(30, 8))
wow(t_arranco - 0.3, "dk_hechizo", 0.9)
wow(t_arranco + 0.6, "fantasma", 0.7)
snd(t_arranco, "siseo", 0.6, dur=2.5)


@toma(t_noMato - 0.3, ("fundido", 0.5))
def m4(lz, t):
    M4.fondo(lz, t)
    brillo_en(lz, M4, t, 0.75, 0.40, 160, color=(0.35, 1.0, 0.4), inten=0.35, sem=93)
    brillo_en(lz, M4, t, 0.18, 0.72, 40, inten=0.4, sem=94)
    brillo_en(lz, M4, t, 0.24, 0.50, 40, inten=0.4, sem=95)
    u = smooth(prog(t, t_arranco - 0.2, t_arranco + 2.2))
    caida = smooth(prog(t, t_arranco + 0.4, t_arranco + 1.4))
    X, Y, h = M4.en(t, 0.36, 0.96, 0.54)
    PF.actor(lz, "joseph_hoja/01", X, Y, h, tono=NOCHE_PESTE, rot=-75 * caida, op=1 - 0.2 * caida)
    X2, Y2, h2 = M4.en(t, 0.72, 0.96, 0.60)
    PF.actor(lz, "marduk_hoja/01", X2, Y2, h2, tono=(0.85, 0.92, 0.9), sy=PF.respira(t))
    mano = (X2 - 0.20 * h2, Y2 - 0.62 * h2)
    pecho = (X + 0.02 * h, Y - 0.62 * h)
    lazo(lz, mano, pecho, t, smooth(prog(t, t_noMato + 0.5, t_arranco)), color=(0.65, 0.4, 1.0), n=3, amp=30, sem=1)
    if u > 0:                     # el alma (la misma pieza, fantasma) arrancada hacia la mano de Marduk
        xa, ya = lerp(pecho[0], mano[0] - 0.1 * h2, u), lerp(pecho[1], mano[1], u)
        PF.brillo(lz, xa, ya, 0.7 * h, color=(0.4, 0.95, 1.0), inten=0.4 * (1 - 0.5 * u), t=t, sem=96)
        PF.actor(lz, "joseph_hoja/01", xa, ya + 0.5 * h * (1 - u) + 0.3 * h * u, h * (1 - 0.35 * u), op=0.55 * (1 - 0.3 * u),
                 tono=FANTASMA, suelo=0, sombra=False, ancla=(0.5, 0.6), rot=12 * math.sin(t * 6) * u)
    niebla(lz, t, NIEBLA_VERDE[:2])


M5 = PF.Plano("sombra_vortice_a", t_retorc - 0.3, t_contag, z0=1.06, z1=1.22, c0=(0.50, 0.60), c1=(0.50, 0.58), par=(30, 8))
wow(t_sombra, "sombra", 0.8)
wow(t_corromp, "banshee", 0.5)
snd(t_corromp, "golpe_grave", 0.8)


@toma(t_retorc - 0.3, ("negro", 0.5))
def m5(lz, t):
    M5.fondo(lz, t)
    brillo_en(lz, M5, t, 0.24, 0.50, 70, color=(0.35, 1.0, 0.4), inten=0.4, sem=97)
    brillo_en(lz, M5, t, 0.50, 0.60, 40, inten=0.35, sem=98)
    giro = smooth(prog(t, t_retorc - 0.3, t_sombra + 0.6))
    X, Y, h = M5.en(t, 0.55, 0.95, 0.60)
    if giro < 1:                  # el alma gira y se oscurece…
        PF.brillo(lz, X, Y - 0.6 * h, 0.8 * h, color=(0.4, 0.95, 1.0), inten=0.35 * (1 - giro), t=t, sem=13)
        PF.actor(lz, "joseph_hoja/01", X, Y - 0.55 * h, h * 0.9, op=0.8 * (1 - giro ** 3), tono=FANTASMA, suelo=0, sombra=False,
                 rot=360 * giro ** 2, ancla=(0.5, 0.6))
    for k in range(3):
        PF.humo(lz, t + k, X, Y - 0.3 * h, s=1.6 * giro, color=(0.03, 0.05, 0.04), op=0.35 * giro, sem=20 + k)
    sombra_pz(lz, M5, t, "rutagrana_hoja/00", 0.55, 0.95, 0.60, t_in=t_retorc + 0.9)
    real(lz, "rutagrana_corrompido", W * 0.18, H * 0.38, H * 0.50, t, t_corromp - 0.1, rot=-4)
    rot_(lz, "RUTAGRANA EL CORROMPIDO", W * 0.5, H * 0.12, 60, t, t_corromp)
    niebla(lz, t, NIEBLA_VERDE)


M6 = PF.Plano("sombra_vortice_b", t_contag - 0.3, t_vuelta, z0=1.06, z1=1.16, c0=(0.50, 0.62), c1=(0.52, 0.62), par=(30, 8))
wow(t_contag + 0.3, "peste_burbuja", 0.7)
wow(t_contag + 1.5, "zombi", 0.6)


@toma(t_contag - 0.3, ("latigo", 0.4))
def m6(lz, t):
    M6.fondo(lz, t)
    brillo_en(lz, M6, t, 0.68, 0.35, 80, color=(0.35, 1.0, 0.4), inten=0.4, sem=99)
    brillo_en(lz, M6, t, 0.67, 0.65, 40, inten=0.35, sem=100)
    sombra_pz(lz, M6, t, "rutagrana_hoja/02", 0.26, 0.96, 0.62)
    Xs, Ys, hs_ = M6.en(t, 0.26, 0.96, 0.62)
    mano = (Xs + 0.25 * hs_, Ys - 0.62 * hs_)
    for k, (pz, x, fr) in enumerate((("defensores_hoja/00", 0.58, 0.44), ("defensores_hoja/02", 0.74, 0.42),
                                     ("defensores_hoja/03", 0.88, 0.46))):
        tk = t_contag + 0.4 + 0.9 * k
        c = smooth(prog(t, tk, tk + 1.2))
        X, Y, h = M6.en(t, x, 0.94, fr)
        lazo(lz, mano, (X, Y - 0.6 * h), t, smooth(prog(t, tk - 0.6, tk + 0.2)), n=2, amp=24, sem=k)
        ton = tuple(lerp(a, b, c) for a, b in zip(NOCHE, (0.45, 0.85, 0.50)))
        PF.actor(lz, pz, X + 2 * c * math.sin(t * 20 + k), Y, h, tono=ton, flip=True, sy=PF.respira(t, fase=k))
        if c > 0.5:
            PF.brillo(lz, X - 0.05 * h, Y - 0.88 * h, 0.12 * h, color=(0.3, 1.0, 0.3), inten=0.8 * c, t=t, sem=30 + k)
    niebla(lz, t, NIEBLA_VERDE)


M7 = PF.Plano("calle_casas_a", t_vuelta - 0.3, t_casas, z0=1.04, z1=1.20, c0=(0.50, 0.62), c1=(0.62, 0.58), par=(30, 8))
for tg in (t_atac, t_atac + 0.8, t_atac + 1.5):
    wow(tg, "espada_carne", 0.6)
snd(t_entra + 0.8, "golpe_grave", 0.6)
snd(t_entra + 1.6, "golpe_grave", 0.5)
CORR = (0.45, 0.85, 0.50)


@toma(t_vuelta - 0.3, ("fundido", 0.5))
def m7(lz, t):
    M7.fondo(lz, t)
    for k, (x, y) in enumerate(((0.72, 0.50), (0.60, 0.55), (0.30, 0.52))):
        brillo_en(lz, M7, t, x, y, 40, inten=0.35 * (1 - smooth(prog(t, t_entra + 0.8 + 0.6 * k, t_entra + 1.2 + 0.6 * k))),
                  sem=101 + k)
    # se dan la vuelta (pegatina que gira de lado) y atacan a sus compañeros; después caminan hacia las puertas
    giro = smooth(prog(t, t_vuelta + 0.3, t_vuelta + 1.0))
    for k, (pz, x, fr) in enumerate((("defensores_hoja/00", 0.30, 0.46), ("defensores_hoja/02", 0.48, 0.44))):
        X, Y, h = M7.en(t, lerp(x, 0.72 - 0.12 * k, smooth(prog(t, t_entra, t_entra + 2.5))), 0.93, fr)
        sx = abs(math.cos(giro * math.pi)) * 0.9 + 0.1
        PF.actor(lz, pz, X, Y, h, tono=CORR, flip=giro > 0.5, sx=sx)
        PF.brillo(lz, X, Y - 0.88 * h, 0.12 * h, color=(0.3, 1.0, 0.3), inten=0.7 * giro, t=t, sem=40 + k)
    paseo(lz, M7, t, "defensores_hoja/05", t_atac, t_casas, 1.10, 0.62, 0.90, 0.42, tono=CORR, pasos=1.8)
    caido = smooth(prog(t, t_atac + 0.2, t_atac + 0.9))
    X, Y, h = M7.en(t, 0.16, 0.95, 0.44)
    PF.actor(lz, "defensores_hoja/03", X, Y, h, tono=NOCHE, rot=-80 * caido, op=1 - 0.4 * smooth(prog(t, t_entra, t_entra + 1)))
    niebla(lz, t, NIEBLA_VERDE)
    sacude(lz, 5 * golpe_de(t, (t_atac, t_atac + 0.8, t_atac + 1.5)), t)


M8 = PF.Plano("casa_interior_b", t_casas - 0.3, t_ninos, z0=1.10, z1=1.20, c0=(0.42, 0.62), c1=(0.40, 0.64), par=(26, 6))
M8b = PF.Plano("escondite_b", t_ninos - 0.3, t_nadie, z0=1.12, z1=1.40, c0=(0.55, 0.62), c1=(0.60, 0.64), par=(26, 6))
snd(t_casas + 0.5, "latido", 0.6)
wow(t_ninos, "vela", 0.4)
snd(t_ninos + 1.4, "golpe_suave", 0.6)


@toma(t_casas - 0.3, ("negro", 0.5))
def m8(lz, t):
    if t < t_ninos - 0.3:
        M8.fondo(lz, t)
        brillo_en(lz, M8, t, 0.27, 0.52, 60, inten=0.5 * (0.8 + 0.2 * math.sin(t * 13)), sem=104)
        quieto(lz, M8, t, "aldeanos_hoja/03", 0.18, 0.92, 0.36, tono=VELA, fase=0.3, rot=-6)
        quieto(lz, M8, t, "aldeanos_hoja/01", 0.40, 0.95, 0.40, tono=VELA, fase=1.1, flip=True)
        # la sombra de un defensor corrompido crece en la pared
        u = smooth(prog(t, t_casas + 0.3, t_ninos))
        X, Y, h = M8.en(t, 0.64, 0.74, 0.40 + 0.25 * u)
        lz[:] = cv2.GaussianBlur(lz, (0, 0), 0.1 + 1.5 * u) if u > 0.6 else lz
        PF.actor(lz, "defensores_hoja/00", X, Y, h, tono=(0.0, 0.01, 0.0), op=0.75 * u, suelo=0, sombra=False, flip=True)
    else:
        M8b.fondo(lz, t)
        brillo_en(lz, M8b, t, 0.62, 0.65, 60, inten=0.5 * (0.7 + 0.3 * math.sin(t * 17)), sem=105)
        quieto(lz, M8b, t, "pamela_hoja/03", 0.36, 0.88, 0.30, tono=(0.5, 0.56, 0.72))
        u = smooth(prog(t, t_ninos + 0.2, t_nadie))
        X, Y, h = M8b.en(t, 0.86, 0.95, 0.5 + 0.4 * u)
        PF.actor(lz, "defensores_hoja/02", X, Y, h, tono=(0.02, 0.03, 0.03), op=0.6 * u, suelo=0, sombra=False, flip=True)
        oscurece(lz, 0.5 * smooth(prog(t, t_nadie - 0.8, t_nadie)))


M9 = PF.Plano("pueblo_ardiendo_a", t_nadie - 0.3, _ESC[CT]["t0"] + 0.3, z0=1.30, z1=1.04, c0=(0.58, 0.52), c1=(0.52, 0.52),
              par=(34, 8))
wow(t_nadie, "campana", 0.4)
wow(t_nadie - 0.3, "hoguera", 0.35, dur=6.5, fade=1.5)
V_M9 = [(t_nadie, 6.0, 0.22, 0.12, 60, -1, 0.3), (t_nadie + 0.4, 6.5, 0.28, 0.18, 46, -1, 1.2)]


@toma(t_nadie - 0.3, ("fundido", 1.0))
def m9(lz, t):
    M9.fondo(lz, t)
    for k, (x, y) in enumerate(((0.55, 0.50), (0.68, 0.48), (0.48, 0.52))):
        brillo_en(lz, M9, t, x, y, 160, inten=0.40, sem=106 + k, chis=6)
    humo_en(lz, M9, t, 0.60, 0.35, s=1.8, color=(0.15, 0.14, 0.13), op=0.32, sem=8)
    cuervos(lz, t, V_M9, tono=NOCHE)
    rot_(lz, "NADIE SOBREVIVIÓ", W * 0.5, H * 0.80, 70, t, t_nadie + 0.8, rot=-1.5)
    oscurece(lz, 0.75 * smooth(prog(t, _ESC[CT]["t0"] - 0.6, _ESC[CT]["t0"] + 0.3)))


# ================================================================== CTA A LA MITAD (283,6 - 312,7)
t_cta, t_formato, t_cuento = F(CT, 0), Ts(CT, "formato", 0), Ts(CT, "cuento", 0)
t_gusta, t_comp, t_coment = F(CT, 1), Ts(CT, "compártelo", 1), Ts(CT, "comentario", 1)
t_azeroth, t_oscuras, t_otras = F(CT, 2), Ts(CT, "oscuras", 2), Ts(CT, "otras", 2)
t_volv = F(CT, 3)
wow(t_cta - 0.3, "vela", 0.5)
wow(t_cta, "hoguera", 0.18, dur=t_volv - t_cta, fade=1.0)
for k, tt in enumerate((t_cuento - 0.2, t_cuento + 0.15, t_cuento + 0.5, t_cuento + 0.85)):
    snd(tt, "papel", 0.5)
snd(t_comp, "pop", 0.6)
snd(t_coment, "pop", 0.6)
C1 = PF.Plano("escritorio_vela_a", t_cta - 0.6, t_gusta, z0=1.02, z1=1.12, c0=(0.50, 0.52), c1=(0.50, 0.54), par=(0, 0))
C2 = PF.Plano("escritorio_vela_a", t_gusta - 0.3, t_azeroth, z0=1.35, z1=1.42, c0=(0.62, 0.55), c1=(0.60, 0.55), par=(0, 0))
C3 = PF.Plano("escritorio_vela_a", t_azeroth - 0.3, t_volv, z0=1.25, z1=1.10, c0=(0.40, 0.52), c1=(0.46, 0.52), par=(0, 0))
CUENTO = [("pamela_hoja/01", 0.38, 0.62, 0.30), ("joseph_hoja/01", 0.45, 0.66, 0.38), ("davil_hoja/00", 0.58, 0.66, 0.36),
          ("horgus_hoja/01", 0.65, 0.68, 0.40)]


def _cuento(lz, pl, t):
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.06, 0.08, 140, inten=0.55 + 0.08 * math.sin(t * 9), sem=110)
    for k, (pz, x, y, fr) in enumerate(CUENTO):
        tk = t_formato + 0.4 + 0.8 * k
        if t >= tk:
            e = PF.entra(t, tk, 0.4)
            X, Y, h = pl.en(t, x, y, fr)
            PF.actor(lz, pz, X, Y, h * (0.6 + 0.4 * e), tono=VELA, rot=(1 - e) * 10, op=clamp01(e * 3), sy=PF.respira(t, fase=k))


@toma(t_cta - 0.6, ("fundido", 1.0))
def c1(lz, t):
    _cuento(lz, C1, t)
    rot_(lz, "UN FORMATO NUEVO", W * 0.5, H * 0.10, 60, t, t_formato - 0.1)
    rot_(lz, "lore de Warcraft contado como un cuento", W * 0.5, H * 0.90, 40, t, t_cuento + 0.2, rot=1)


@toma(t_gusta - 0.3, ("desenfoque", 0.5))
def c2(lz, t):
    _cuento(lz, C2, t)
    rot_(lz, "COMPÁRTELO", W * 0.26, H * 0.10, 66, t, t_comp - 0.1, rot=-4)
    rot_(lz, "DÉJAME UN COMENTARIO", W * 0.68, H * 0.74, 58, t, t_coment - 0.1, rot=3)


@toma(t_azeroth - 0.3, ("desenfoque", 0.5))
def c3(lz, t):
    _cuento(lz, C3, t)
    real(lz, "marduk", W * 0.12, H * 0.30, H * 0.40, t, t_oscuras - 0.4, rot=-6)
    real(lz, "horgus", W * 0.30, H * 0.34, H * 0.38, t, t_oscuras - 0.1, rot=4)
    tinte(lz, (0.4, 0.6, 0.5), 0.25 * smooth(prog(t, t_oscuras - 0.4, t_oscuras + 0.3)) * (1 - smooth(prog(t, t_otras, t_otras + 0.5))))
    real(lz, "cromi", W * 0.78, H * 0.42, H * 0.46, t, t_otras, rot=5)
    rot_(lz, "UNAS MUY OSCURAS", W * 0.30, H * 0.80, 48, t, t_oscuras, t_otras)
    rot_(lz, "…Y OTRAS, NO TANTO", W * 0.72, H * 0.80, 48, t, t_otras + 0.3, rot=2)


C4 = PF.Plano("ruinas_noche_b", t_volv - 0.3, _ESC["despues"]["t0"], z0=1.0, z1=1.35, c0=(0.50, 0.55), c1=(0.52, 0.58),
              par=(34, 8))
wow(t_volv, "fantasma", 0.4)
wow(t_volv - 0.2, "amb_peste_noche", 0.45, dur=_ESC["despues"]["t0"] - t_volv + 1.0, fade=0.8)


@toma(t_volv - 0.3, ("negro", 0.7))
def c4(lz, t):
    C4.fondo(lz, t)
    brillo_en(lz, C4, t, 0.67, 0.10, 110, color=(0.7, 0.85, 1.0), inten=0.22, sem=111)
    brillo_en(lz, C4, t, 0.52, 0.58, 40, inten=0.45, sem=112)
    fantasma(lz, C4, t, "pamela_hoja/04", 0.50, 0.74, 0.22, t_in=t_volv + 0.2)
    niebla(lz, t, NIEBLA_AZUL)


def ventana2(lz, t, X, Y, alto, t_in, titulo, zona, cita, t_acepta=None, aviso=None, t_out=None):
    """Ventana de misión de WoW Classic con otro texto (misma receta que ventana_mision)."""
    if t < t_in:
        return
    spr = _ventana(titulo, zona, cita)
    u = PF.entra(t, t_in, 0.5)
    o = 1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.4))
    if o <= 0.01:
        return
    s = alto / spr.h * (0.7 + 0.3 * u)
    a = math.radians(-2.0 + (1 - u) * 8)
    M = (np.array([[1, 0, X], [0, 1, Y], [0, 0, 1]]) @ np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
         @ np.diag([s, s, 1.0]) @ np.array([[1, 0, -spr.w / 2], [0, 1, -spr.h / 2], [0, 0, 1]]))
    D.pegar(lz, spr, M, o * clamp01(u * 3))
    if t_acepta is not None and t >= t_acepta:
        k = PF.entra(t, t_acepta, 0.35)
        bx, by = X + (spr.w / 2 - 180) * s, Y + (spr.h / 2 - 78) * s
        PF.brillo(lz, bx, by, 140 * s * 2, color=(1.0, 0.8, 0.3), inten=0.5 * (1 - clamp01((t - t_acepta) / 1.2)), t=t)
        texto_oro(lz, aviso or f"Misión aceptada: {titulo}", W * 0.5, H * 0.12, 54, o * clamp01(k * 2))


def aviso_oro(lz, t, txt, t0, t1, Y=H * 0.12, px=54):
    """Aviso dorado de la interfaz («Misión completada: …») que aparece y se apaga."""
    if t0 <= t < t1 + 0.5:
        texto_oro(lz, txt, W * 0.5, Y, px, clamp01((t - t0) / 0.25) * (1 - smooth(prog(t, t1, t1 + 0.5))))


def aliento(lz, t, X, Y, s=1.0, sem=0):
    """Vaho de frío que sale de la boca cada ~2,4 s."""
    f = ((t + sem) % 2.4) / 2.4
    if f < 0.7:
        PF.humo(lz, t, X + 40 * s * f, Y - 20 * s * f, s=0.35 * s * (0.4 + f), color=(0.85, 0.92, 1.0), op=0.35 * (1 - f / 0.7),
                sem=sem, alto=60 * s)


DE, PA, MU, AN = "despues", "pamela", "muneca", "anillo"
# el mapa b: Villa Darrow junto al lago (sureste), Andorhal al oeste, la granja de Gahrron al este de Andorhal
MAPA_B = dict(darrow=(0.82, 0.60), andor=(0.40, 0.62), granja=(0.49, 0.55), strat=(0.72, 0.38))

# ================================================================== DESPUÉS (312,7 - 363,6)
t_se_fue, t_cabeza, t_sombraD = F(DE, 0), Ts(DE, "cabeza", 0), Ts(DE, "sombra", 0)
t_sembro, t_alianza, t_granja = F(DE, 1), Ts(DE, "alianza", 1), Ts(DE, "granja", 1)
t_escudo, t_llamara = F(DE, 2), Ts(DE, "llamara", 2)
t_caidos, t_espir = F(DE, 3), Ts(DE, "espíritus", 3)
t_aveces, t_otraD = F(DE, 4), Ts(DE, "otra", 4)
t_silencio, t_bueno, t_casi = F(DE, 5), Ts(DE, "bueno", 5), Ts(DE, "casi", 5)

wow(t_se_fue - 0.3, "amb_peste_dia", 0.40, dur=t_caidos - t_se_fue + 0.6, fade=1.5)
snd(t_se_fue, "pasos", 0.5, dur=4.0)
wow(t_cabeza, "necrofago2", 0.4)
E1 = PF.Plano("camino_plaga_a", t_se_fue - 0.4, t_sembro, z0=1.04, z1=1.18, c0=(0.50, 0.58), c1=(0.52, 0.52), par=(34, 8))


@toma(t_se_fue - 0.4, ("fundido", 0.8))
def d1(lz, t):
    E1.fondo(lz, t)
    brillo_en(lz, E1, t, 0.60, 0.35, 70, inten=0.35, sem=120)
    humo_en(lz, E1, t, 0.60, 0.33, s=1.2, color=(0.3, 0.3, 0.3), op=0.25, sem=9)
    # la columna de la Plaga se aleja por el camino (de cerca a lejos: lo lejano primero)
    col = []
    for k in range(7):
        ta = t_se_fue - 3.0 + 0.9 * k
        u = clamp01((t - ta) / 9.0)
        pz = ("esqueletos_hoja/00", "esqueletos_hoja/01", "plaga_hoja/02", "esqueletos_hoja/05", "esqueletos_hoja/02",
              "plaga_hoja/02", "esqueletos_hoja/00")[k]
        col.append((lerp(0.98, 0.52, u), pz, lerp(0.40 + 0.06 * (k % 3), 0.52, u), lerp(0.42, 0.08, u), ta, k))
    for y, pz, x, fr, ta, k in sorted(col):
        X, Y, h = E1.en(t, x, y, fr)
        ph = (t - ta) * 1.6 * math.pi
        PF.actor(lz, pz, X, Y - abs(math.sin(ph)) * 0.03 * h, h, tono=NUBLADO, rot=3 * math.sin(ph), flip=k % 2 == 1)
    u = clamp01((t - t_sombraD + 2.0) / 7.0)
    sombra_pz(lz, E1, t, "rutagrana_hoja/00", lerp(0.30, 0.46, u), lerp(0.95, 0.60, u), lerp(0.50, 0.16, u), t_in=t_sombraD - 0.6,
              humo=False)
    pega(lz, "utileria2/05", W * 0.80, H * 0.30, H * 0.32, t, t_cabeza - 0.1, rot=8)
    rot_(lz, "LA CABEZA DE HORGUS", W * 0.80, H * 0.52, 40, t, t_cabeza + 0.2)
    niebla(lz, t, NIEBLA_VERDE[:2])


E2 = PF.Plano("mapa_lordaeron_b", t_sembro - 0.3, t_granja, z0=1.04, z1=1.30, c0=(0.62, 0.52), c1=(0.55, 0.52), par=(0, 0))
RUTA_SOMBRA = [MAPA_B["darrow"], (0.75, 0.48), (0.64, 0.42), (0.58, 0.30), (0.46, 0.34), (0.42, 0.46), MAPA_B["granja"]]
snd(t_sembro, "siseo", 0.5, dur=3.0)
snd(t_alianza, "papel", 0.5)
E2b = PF.Plano("granja_gahrron_a", t_granja - 0.3, t_escudo, z0=1.06, z1=1.18, c0=(0.48, 0.60), c1=(0.44, 0.60), par=(30, 8))
for tg in (t_granja + 0.6, t_granja + 1.5, t_granja + 2.4):
    wow(tg, "espada_escudo", 0.55)
wow(t_granja + 2.6, "sombra", 0.6)


@toma(t_sembro - 0.3, ("corte", 0.0))
def d2(lz, t):
    if t < t_granja - 0.3:
        E2.fondo(lz, t)
        brillo_en(lz, E2, t, 0.72, 0.38, 60, inten=0.4, sem=121)
        ruta_tinta(lz, E2, t, RUTA_SOMBRA, t_sembro + 0.3, t_alianza + 0.8, color=(0.06, 0.12, 0.06), grosor=7.0)
        pos = RUTA_SOMBRA[min(len(RUTA_SOMBRA) - 1, int(smooth(prog(t, t_sembro + 0.3, t_alianza + 0.8)) * (len(RUTA_SOMBRA) - 1)))]
        X, Y, s = E2.P(t, *pos)
        PF.brillo(lz, X, Y, 90, color=(0.3, 1.0, 0.4), inten=0.45, t=t, sem=122)
        PF.actor(lz, "rutagrana_hoja/00", X, Y + 30, 120, tono=SOMBRA_T, suelo=0)
        for clave, txt in (("darrow", "Villa Darrow"), ("andor", "Andorhal")):
            Xc, Yc, sc = E2.P(t, *MAPA_B[clave])
            rot_(lz, txt, Xc, Yc + 44, 30, t, t_sembro, rot=0)
        if t >= t_alianza + 0.6:
            Xg, Yg, _ = E2.P(t, *MAPA_B["granja"])
            k = PF.entra(t, t_alianza + 0.6, 0.3)
            D.linea_aa(lz, [(Xg - 34 * k, Yg - 34 * k), (Xg + 34 * k, Yg + 34 * k)], (0.6, 0.05, 0.05), grosor=8.0)
            D.linea_aa(lz, [(Xg - 34 * k, Yg + 34 * k), (Xg + 34 * k, Yg - 34 * k)], (0.6, 0.05, 0.05), grosor=8.0)
        rot_(lz, "SEMBRÓ EL MAL POR TODO LORDAERON", W * 0.5, H * 0.10, 48, t, t_sembro + 0.4)
    else:
        E2b.fondo(lz, t)
        brillo_en(lz, E2b, t, 0.43, 0.52, 50, inten=0.45, sem=123)
        g = golpe_de(t, (t_granja + 0.6, t_granja + 1.5, t_granja + 2.4))
        cae = smooth(prog(t, t_granja + 2.4, t_granja + 3.2))
        sombra_pz(lz, E2b, t, "rutagrana_hoja/01" if cae < 0.5 else "rutagrana_hoja/03", 0.62, 0.92, 0.50, op=0.92 * (1 - 0.6 * cae))
        quieto(lz, E2b, t, "defensores_hoja/01", 0.32, 0.95, 0.52, tono=NUBLADO, rot=-10 * g)
        quieto(lz, E2b, t, "aventurero_hoja/02", 0.44, 0.97, 0.56, tono=NUBLADO, rot=-6 * g)
        quieto(lz, E2b, t, "defensores_hoja/00", 0.84, 0.95, 0.50, tono=NUBLADO, flip=True)
        rot_(lz, "UNA GRANJA APESTADA", W * 0.5, H * 0.10, 52, t, t_granja + 0.1)
        sacude(lz, 5 * g, t)
        niebla(lz, t, NIEBLA_VERDE[:2])


E3 = PF.Plano("granja_gahrron_b", t_escudo - 0.3, t_caidos, z0=1.10, z1=1.26, c0=(0.42, 0.62), c1=(0.38, 0.64), par=(30, 8))
wow(t_escudo + 0.2, "peste_burbuja", 0.5)
wow(t_llamara - 1.5, "zombi", 0.6)
wow(t_llamara, "zombi", 0.5)


@toma(t_escudo - 0.3, ("latigo", 0.4))
def d3(lz, t):
    E3.fondo(lz, t)
    brillo_en(lz, E3, t, 0.32, 0.52, 50, inten=0.4, sem=124)
    X, Y, h = E3.en(t, 0.40, 0.86, 0.12)
    PF.brillo(lz, X, Y - 0.3 * h, 1.6 * h, color=(0.3, 1.0, 0.4), inten=0.30 + 0.12 * math.sin(t * 3), t=t, sem=125)
    PF.actor(lz, "utileria/05", X, Y, h, tono=NUBLADO, rot=-70)
    for k, (pz, x0, y0, fr) in enumerate((("plaga_hoja/02", 0.95, 0.92, 0.42), ("monstruos_hoja/06", 1.05, 0.85, 0.34),
                                          ("esqueletos_hoja/03", -0.05, 0.94, 0.20), ("plaga_hoja/02", 0.05, 0.83, 0.30))):
        paseo(lz, E3, t, pz, t_escudo - 0.3 + 0.5 * k, t_caidos + 1.0, x0, 0.40 + (0.18 if x0 > 0.5 else -0.16), y0, fr,
              tono=NOCHE_PESTE, pasos=1.2 + 0.1 * k)
    real(lz, "escudo", W * 0.80, H * 0.24, H * 0.30, t, t_escudo + 0.4, rot=5)
    rot_(lz, "SU ESCUDO", W * 0.80, H * 0.44, 40, t, t_escudo + 0.6)
    niebla(lz, t, NIEBLA_VERDE)


E4 = PF.Plano("ruinas_plaza_noche_a", t_caidos - 0.3, t_aveces, z0=1.10, z1=1.22, c0=(0.50, 0.64), c1=(0.52, 0.62), par=(30, 8))
wow(t_caidos + 0.5, "necrofago", 0.6)
wow(t_espir, "fantasma", 0.6)
wow(t_caidos - 0.3, "amb_peste_noche", 0.45, dur=t_casi - t_caidos + 3.0, fade=1.5)


@toma(t_caidos - 0.3, ("negro", 0.6))
def d4(lz, t):
    E4.fondo(lz, t)
    brillo_en(lz, E4, t, 0.55, 0.65, 50, inten=0.4, sem=126)
    for k, (pz, x, fr) in enumerate((("defensores_hoja/00", 0.28, 0.46), ("defensores_hoja/02", 0.52, 0.42),
                                     ("defensores_hoja/03", 0.76, 0.46))):
        tk = t_caidos + 0.4 + 0.8 * k
        sube = smooth(prog(t, tk, tk + 1.0))
        X, Y, h = E4.en(t, x, 0.93, fr)
        if sube < 1:          # el caído en el suelo…
            PF.actor(lz, pz, X, Y, h, tono=NOCHE, rot=-85 * (1 - sube), op=1 - sube)
        if sube > 0:          # …se levanta como necrófago, con su espíritu atrapado dentro
            PF.actor(lz, "necrofago_corre/ciclo_00", X, Y, h * 1.05 * sube, tono=NOCHE_PESTE, op=sube, flip=x > 0.5)
            if t > t_espir - 0.3:
                fl = 0.5 + 0.5 * math.sin(t * 5 + k)
                PF.actor(lz, pz, X + 4 * math.sin(t * 11 + k), Y - 0.05 * h, h * 0.9, op=0.35 * fl, tono=FANTASMA, suelo=0,
                         sombra=False)
                PF.brillo(lz, X, Y - 0.5 * h, 0.5 * h, color=(0.4, 0.9, 1.0), inten=0.25 * fl, t=t, sem=50 + k)
    real(lz, "espiritu", W * 0.86, H * 0.30, H * 0.36, t, t_espir + 0.2, rot=5)
    niebla(lz, t, NIEBLA_VERDE[:2])


E5 = PF.Plano("ruinas_calle_a", t_aveces - 0.3, t_silencio, z0=1.04, z1=1.16, c0=(0.50, 0.62), c1=(0.48, 0.60), par=(30, 8))
for k in range(5):
    wow(t_aveces + 0.6 + 1.3 * k, "espada_escudo" if k % 2 == 0 else "esqueleto_muere", 0.25)
wow(t_aveces, "mundo_espiritus", 0.5, dur=t_silencio - t_aveces + 0.6, fade=0.8)


@toma(t_aveces - 0.3, ("fundido", 0.6))
def d5(lz, t):
    E5.fondo(lz, t)
    brillo_en(lz, E5, t, 0.43, 0.40, 40, inten=0.4, sem=127)
    # la misma batalla en bucle: cada 2,6 s se rebobina (la pegatina salta atrás con un parpadeo)
    ciclo = 2.6
    f = ((t - t_aveces) % ciclo) / ciclo
    rebob = 1.0 - smooth(prog(f, 0.0, 0.12))
    for k, (pz, x0, x1, fr, fl) in enumerate((("defensores_hoja/00", 0.20, 0.36, 0.44, False),
                                              ("esqueletos_hoja/00", 0.62, 0.44, 0.40, True),
                                              ("defensores_hoja/01", 0.80, 0.64, 0.46, True),
                                              ("esqueletos_hoja/01", 0.10, 0.24, 0.36, False))):
        x = lerp(x0, x1, smooth(f))
        fantasma(lz, E5, t, pz, x, 0.92 - 0.02 * (k % 2), fr, op=0.55 * (1 - 0.6 * rebob), flip=fl)
    destello_pant(lz, 0.25 * rebob * (t > t_aveces + 0.5), (0.6, 0.9, 1.0))
    rot_(lz, "UNA Y OTRA VEZ", W * 0.5, H * 0.12, 56, t, t_otraD - 0.6)
    niebla(lz, t, NIEBLA_AZUL)


E6 = PF.Plano("ruinas_casa_pamela_b", t_silencio - 0.3, _ESC[PA]["t0"], z0=1.0, z1=1.12, c0=(0.50, 0.55), c1=(0.60, 0.56),
              par=(34, 8))
wow(t_casi, "fantasma", 0.35)
V_E6 = [(t_silencio, 7.0, 0.16, 0.10, 52, -1, 0.5)]


@toma(t_silencio - 0.3, ("fundido", 1.0))
def d6(lz, t):
    E6.fondo(lz, t)
    brillo_en(lz, E6, t, 0.63, 0.58, 40, inten=0.4, sem=128)
    k = smooth(prog(t, t_casi - 0.3, t_casi + 0.6))
    brillo_en(lz, E6, t, 0.82, 0.55, 80, color=(0.4, 0.8, 1.0), inten=0.15 + 0.45 * k * (0.7 + 0.3 * math.sin(t * 8)), sem=129)
    if k > 0:
        fantasma(lz, E6, t, "pamela_hoja/04", 0.88, 0.76, 0.22, t_in=t_casi - 0.2, op=0.55)
    cuervos(lz, t, V_E6, tono=NOCHE)
    niebla(lz, t, NIEBLA_AZUL)


# ================================================================== PAMELA (363,6 - 421,8)
t_anos, t_casaP, t_surP = F(PA, 0), Ts(PA, "casa", 0), Ts(PA, "sur", 0)
t_adentro, t_marP = F(PA, 1), Ts(PA, "marlene", 1)
t_murieron, t_peor = F(PA, 2), Ts(PA, "peor", 2)
t_escondi, t_nose = F(PA, 3), Ts(PA, "sé", 3)
t_vas, t_ninaP, t_transp = F(PA, 4), Ts(PA, "niña", 4), Ts(PA, "transparente", 4)
t_holaP = F(PA, 5)
t_cuenta, t_valiente, t_marP2 = F(PA, 6), Ts(PA, "valiente", 6), Ts(PA, "marlene", 6)
t_llevo = F(PA, 7)
t_favor, t_munP = F(PA, 8), Ts(PA, "muñeca", 8)

snd(t_anos, "galope", 0.6, dur=5.0)
wow(t_anos, "amb_peste_dia", 0.4, dur=t_adentro - t_anos + 0.5, fade=1.0)
P1b = PF.Plano("peste_este_b", t_anos - 0.4, t_casaP, z0=1.04, z1=1.14, c0=(0.48, 0.55), c1=(0.52, 0.55), par=(34, 8))
P2b = PF.Plano("casa_marlene_ruina_a", t_casaP - 0.3, t_adentro, z0=1.04, z1=1.20, c0=(0.55, 0.55), c1=(0.66, 0.52), par=(30, 8))


@toma(t_anos - 0.4, ("negro", 0.7))
def pm1(lz, t):
    if t < t_casaP - 0.3:
        P1b.fondo(lz, t)
        brillo_en(lz, P1b, t, 0.68, 0.30, 40, inten=0.35, sem=130)
        anda(lz, P1b, t, "jinete_galope", t_anos - 0.4, t_casaP + 0.5, -0.15, 0.75, 0.86, 0.26, paso=1.7, tono=NUBLADO,
             desde_antes=True)
        rot_(lz, "AÑOS DESPUÉS", W * 0.5, H * 0.12, 64, t, t_anos + 0.2)
        niebla(lz, t, NIEBLA_VERDE[:2])
    else:
        P2b.fondo(lz, t)
        brillo_en(lz, P2b, t, 0.79, 0.47, 30, inten=0.35, sem=131)
        paseo(lz, P2b, t, "aventurero_hoja/00", t_casaP - 0.3, t_adentro, 0.30, 0.58, 0.92, 0.40, tono=NUBLADO, pasos=2.0)
        rot_(lz, "AL SUR DE ANDORHAL", W * 0.30, H * 0.12, 50, t, t_surP)
        niebla(lz, t, NIEBLA_VERDE[:2])


P3b = PF.Plano("casa_marlene_dentro_a", t_adentro - 0.3, t_murieron, z0=1.04, z1=1.14, c0=(0.50, 0.58), c1=(0.52, 0.58),
               par=(26, 6))
P4b = PF.Plano("casa_marlene_dentro_a", t_murieron - 0.3, t_escondi, z0=1.40, z1=1.55, c0=(0.38, 0.52), c1=(0.42, 0.48),
               par=(26, 6))
wow(t_adentro + 0.5, "fantasma", 0.6)
wow(t_adentro, "mundo_espiritus", 0.35, dur=t_escondi - t_adentro, fade=1.0)
wow(t_peor, "sombra", 0.4)


@toma(t_adentro - 0.3, ("desenfoque", 0.5))
def pm2(lz, t):
    pl = P3b if t < t_murieron - 0.3 else P4b
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.66, 0.35, 50, inten=0.45, sem=132)
    fantasma(lz, pl, t, "familia_hoja/01", 0.40, 0.92, 0.56, t_in=t_adentro + 0.3)
    if pl is P3b:
        real(lz, "marlene", W * 0.82, H * 0.36, H * 0.50, t, t_marP - 0.1, rot=5)
        rot_(lz, "MARLENE", W * 0.82, H * 0.68, 46, t, t_marP + 0.1)
    else:   # «…y algo peor»: en el marco vacío de la pared asoma la sombra
        k = smooth(prog(t, t_peor - 0.2, t_peor + 0.4)) * (1 - smooth(prog(t, t_peor + 1.6, t_peor + 2.4)))
        X, Y, h = pl.en(t, 0.45, 0.42, 0.20)
        PF.actor(lz, "rutagrana_hoja/00", X, Y, h, tono=SOMBRA_T, op=0.8 * k, suelo=0, sombra=False)
    niebla(lz, t, NIEBLA_AZUL[:1])


P5b = PF.Plano("casa_marlene_b", t_escondi - 0.3, t_vas, z0=1.06, z1=1.18, c0=(0.62, 0.58), c1=(0.66, 0.60), par=(30, 8))
snd(t_escondi + 0.3, "golpe_suave", 0.5)
SEPIA = (1.05, 0.88, 0.66)


@toma(t_escondi - 0.3, ("destello", 0.6))
def pm4(lz, t):
    P5b.fondo(lz, t)
    brillo_en(lz, P5b, t, 0.70, 0.52, 50, inten=0.5, sem=133)
    quieto(lz, P5b, t, "familia_hoja/01", 0.58, 0.86, 0.42, tono=OCASO)
    a = 1.0 - smooth(prog(t, t_nose - 0.2, t_nose + 0.9))
    paseo(lz, P5b, t, "pamela_hoja/05", t_escondi, t_escondi + 2.4, 0.42, 0.66, 0.88, 0.24, tono=OCASO, pasos=2.4, op=a)
    tinte(lz, SEPIA, 0.55)
    oscurece(lz, 0.15)
    rot_(lz, "«ESCONDÍ A MI SOBRINA»", W * 0.5, H * 0.12, 50, t, t_escondi + 0.3, t_nose)


P6b = PF.Plano("ruinas_casa_pamela_b", t_vas - 0.3, t_holaP, z0=1.04, z1=1.24, c0=(0.48, 0.60), c1=(0.60, 0.60), par=(30, 8))
P7b = PF.Plano("ruinas_casa_pamela_b", t_holaP - 0.3, t_cuenta, z0=1.70, z1=1.76, c0=(0.66, 0.66), c1=(0.66, 0.66), par=(26, 6))
wow(t_transp - 0.2, "fantasma", 0.6)
wow(t_holaP + 0.8, "mision_acepta", 0.6)


@toma(t_vas - 0.3, ("negro", 0.6))
def pm5(lz, t):
    cerca = t >= t_holaP - 0.3
    pl = P7b if cerca else P6b
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.63, 0.58, 40, inten=0.45, sem=134)
    brillo_en(lz, pl, t, 0.82, 0.55, 60, color=(0.4, 0.8, 1.0), inten=0.25, sem=135)
    if not cerca:
        paseo(lz, pl, t, "aventurero_hoja/00", t_vas - 0.3, t_holaP, 0.10, 0.36, 0.94, 0.46, tono=NOCHE, pasos=2.0)
        fantasma(lz, pl, t, "pamela_hoja/04", 0.66, 0.84, 0.26, t_in=t_transp - 0.4)
    else:
        fantasma(lz, pl, t, "pamela_hoja/02", 0.66, 0.84, 0.26, op=0.66)
        X, Y, h = pl.en(t, 0.66, 0.84, 0.26)
        exclamacion(lz, X, Y - h * 1.12, 110, t, t_holaP - 0.1)
        real(lz, "pamela", W * 0.20, H * 0.40, H * 0.52, t, t_holaP + 0.2, rot=-4)
    niebla(lz, t, NIEBLA_AZUL)


P8b = PF.Plano("casa_pamela_dentro_a", t_cuenta - 0.3, t_llevo, z0=1.10, z1=1.24, c0=(0.50, 0.62), c1=(0.46, 0.62), par=(26, 6))
snd(t_valiente, "pop", 0.4)
snd(t_marP2, "pop", 0.4)


@toma(t_cuenta - 0.3, ("fundido", 0.5))
def pm7(lz, t):
    P8b.fondo(lz, t)
    brillo_en(lz, P8b, t, 0.47, 0.56, 50, inten=0.5, sem=136)
    brillo_en(lz, P8b, t, 0.82, 0.45, 80, color=(0.5, 0.75, 1.0), inten=0.15, sem=137)
    fantasma(lz, P8b, t, "pamela_hoja/04", 0.30, 0.96, 0.46, op=0.64)
    # sus recuerdos, cálidos, como pegatinas reales
    real(lz, "joseph", W * 0.64, H * 0.38, H * 0.52, t, t_valiente - 0.4, t_marP2 - 0.2, rot=4)
    rot_(lz, "«EL HOMBRE MÁS VALIENTE DEL MUNDO»", W * 0.64, H * 0.74, 38, t, t_valiente, t_marP2 - 0.2)
    real(lz, "marlene_cos", W * 0.72, H * 0.38, H * 0.48, t, t_marP2, rot=-3)
    rot_(lz, "«QUÉDATE EN CASA»", W * 0.72, H * 0.72, 40, t, t_marP2 + 0.4)
    niebla(lz, t, NIEBLA_AZUL[:1])


P9b = PF.Plano("ventana_fria_a", t_llevo - 0.3, t_favor, z0=1.08, z1=1.24, c0=(0.62, 0.58), c1=(0.70, 0.56), par=(26, 6))
P10b = PF.Plano("casa_pamela_dentro_b", t_favor - 0.3, _ESC[MU]["t0"], z0=1.10, z1=1.16, c0=(0.45, 0.58), c1=(0.45, 0.58),
                par=(0, 0))
wow(t_llevo, "mundo_espiritus", 0.4, dur=t_favor - t_llevo + 0.5, fade=1.0)
wow(t_munP + 0.3, "mision_acepta", 0.8)


@toma(t_llevo - 0.3, ("fundido", 0.7))
def pm8(lz, t):
    if t < t_favor - 0.3:
        P9b.fondo(lz, t)
        brillo_en(lz, P9b, t, 0.71, 0.60, 40, inten=0.45, sem=138)
        brillo_en(lz, P9b, t, 0.85, 0.45, 160, color=(0.5, 0.75, 1.0), inten=0.20, sem=139)
        fantasma(lz, P9b, t, "pamela_hoja/04", 0.64, 0.90, 0.40, op=0.6, flip=True)
        escarcha(lz, 0.5 * smooth(prog(t, t_llevo, t_favor)))
    else:
        P10b.fondo(lz, t)
        desenfoca(lz, 5)
        oscurece(lz, 0.35)
        brillo_en(lz, P10b, t, 0.42, 0.50, 60, inten=0.45, sem=140)
        fantasma(lz, P10b, t, "pamela_hoja/01", 0.20, 0.98, 0.50, op=0.6)
        ventana2(lz, t, W * 0.62, H * 0.50, H * 0.64, t_favor + 0.2, "La muñeca de Pamela",
                 "Tierras de la Peste del Este · Villa Darrow",
                 ("«¿Me encuentras mi muñeca?", "  La dejé en el pueblo.»", "", "Recompensa: su sonrisa"), t_acepta=t_munP + 0.3)


# ================================================================== MUÑECA (421,8 - 461,8)
t_rota, t_cabM, t_izq, t_der = F(MU, 0), Ts(MU, "cabeza", 0), Ts(MU, "izquierdo", 0), Ts(MU, "derecho", 0)
t_acerca, t_aparece = F(MU, 1), Ts(MU, "aparece", 1)
t_devuel, t_encontr = F(MU, 2), Ts(MU, "encontraste", 2)
t_bajito, t_nunca = F(MU, 3), F(MU, 4)
PIEZAS_M = [(0.30, 0.58, "utileria2/00", "LA CABEZA", "muneca_cabeza"), (0.62, 0.70, "utileria2/01", "EL LADO IZQUIERDO", "muneca_lado"),
            (0.74, 0.40, "utileria2/02", "EL LADO DERECHO", "muneca_lado")]
U1 = PF.Plano("ruinas_vista_alta_a", t_rota - 0.3, t_acerca, z0=1.04, z1=1.14, c0=(0.50, 0.52), c1=(0.52, 0.54), par=(24, 6))
for tt in (t_cabM, t_izq, t_der):
    snd(tt, "pop", 0.6)
wow(t_rota, "amb_peste_noche", 0.40, dur=t_devuel - t_rota, fade=1.0)


def _rastreo_muneca(t):
    v = [("Cabeza de la muñeca", "1/1" if t > t_aparece + 1.2 else "0/1"),
         ("Lado izquierdo", "1/1" if t > t_aparece + 3.2 else "0/1"),
         ("Lado derecho", "1/1" if t > t_aparece + 5.0 else "0/1")]
    return v


@toma(t_rota - 0.3, ("latigo", 0.4))
def mu1(lz, t):
    U1.fondo(lz, t)
    brillo_en(lz, U1, t, 0.51, 0.50, 40, inten=0.4, sem=141)
    for k, (x, y, pz, txt, ic) in enumerate(PIEZAS_M):
        tk = (t_cabM, t_izq, t_der)[k]
        if t >= tk - 0.2:
            X, Y, s = U1.P(t, x, y)
            PF.brillo(lz, X, Y, 120, color=(1.0, 0.85, 0.4), inten=0.35 + 0.15 * math.sin(t * 4 + k), t=t, sem=60 + k)
            pega(lz, pz, X, Y - 70, 150, t, tk - 0.2, rot=(-6, 4, 8)[k])
            rot_(lz, txt, X, Y + 40, 32, t, tk)
    rastreador(lz, t, "La muñeca de Pamela", _rastreo_muneca(t), t_rota + 0.3)
    niebla(lz, t, NIEBLA_VERDE[:2])


U2 = PF.Plano("ruinas_calle_b", t_acerca - 0.3, t_devuel, z0=1.06, z1=1.18, c0=(0.46, 0.62), c1=(0.52, 0.62), par=(30, 8))
wow(t_aparece - 0.2, "fantasma", 0.7)
wow(t_aparece + 0.3, "banshee", 0.35)
for k in range(3):
    wow(t_aparece + 1.2 + 1.9 * k, "pagina", 0.4)


@toma(t_acerca - 0.3, ("fundido", 0.5))
def mu2(lz, t):
    U2.fondo(lz, t)
    X, Y, s = U2.P(t, 0.52, 0.86)
    PF.brillo(lz, X, Y, 90, color=(1.0, 0.85, 0.4), inten=0.4 * (t < t_aparece + 1.2), t=t, sem=142)
    if t < t_aparece + 1.2:
        PF.actor(lz, "utileria2/00", X, Y, 80, tono=NOCHE)
    paseo(lz, U2, t, "aventurero_hoja/00", t_acerca - 0.3, t_aparece, 0.08, 0.40, 0.95, 0.50, tono=NOCHE, pasos=2.0,
          hasta_despues=False)
    if t >= t_aparece:
        quieto(lz, U2, t, "aventurero_hoja/04", 0.40, 0.95, 0.50, tono=NOCHE)
    fantasma(lz, U2, t, "aldeanos_hoja/03", 0.68, 0.92, 0.48, t_in=t_aparece - 0.3, flip=True)
    real(lz, "espiritu", W * 0.84, H * 0.30, H * 0.34, t, t_aparece + 0.3, rot=4)
    rot_(lz, "FANTASMA DEL PASADO", W * 0.84, H * 0.50, 36, t, t_aparece + 0.5)
    rastreador(lz, t, "La muñeca de Pamela", _rastreo_muneca(t), t_acerca - 0.3, X=W * 0.03, Y=H * 0.10)
    niebla(lz, t, NIEBLA_AZUL)


U3 = PF.Plano("ruinas_alba_a", t_devuel - 0.3, t_bajito, z0=1.06, z1=1.20, c0=(0.50, 0.62), c1=(0.52, 0.64), par=(30, 8))
wow(t_encontr - 0.4, "mision_completa", 0.9)
snd(t_devuel + 0.5, "pio", 0.3)


@toma(t_devuel - 0.3, ("destello", 0.6))
def mu3(lz, t):
    U3.fondo(lz, t)
    brillo_en(lz, U3, t, 0.75, 0.40, 60, color=(1.0, 0.9, 0.8), inten=0.2, sem=143)
    salta = abs(math.sin((t - t_devuel) * 4.2)) * smooth(prog(t, t_encontr - 0.8, t_encontr))
    X, Y, h = U3.en(t, 0.48, 0.92, 0.46)
    PF.brillo(lz, X, Y - 0.5 * h, 0.9 * h, color=(0.4, 0.9, 1.0), inten=0.3, t=t, sem=144)
    pz = "reencuentro_hoja/02" if t > t_encontr - 0.8 else "pamela_hoja/01"
    PF.actor(lz, pz, X, Y - 0.12 * h * salta, h, op=0.68, tono=FANTASMA, suelo=0, sombra=False)
    pega(lz, "iconos/muneca", W * 0.80, H * 0.40, H * 0.22, t, t_devuel + 0.4, rot=4)
    aviso_oro(lz, t, "Misión completada: La muñeca de Pamela", t_encontr - 0.4, t_bajito - 0.4)
    PF.chispas(lz, t, X, Y - 0.6 * h, s=1.5, n=8, sem=11)
    niebla(lz, t, NIEBLA_AZUL[:1])


U4 = PF.Plano("casa_pamela_dentro_b", t_bajito - 0.3, t_nunca, z0=1.50, z1=1.70, c0=(0.62, 0.62), c1=(0.64, 0.60), par=(26, 6))
wow(t_bajito + 1.0, "susurros", 0.3)


@toma(t_bajito - 0.3, ("desenfoque", 0.5))
def mu4(lz, t):
    U4.fondo(lz, t)
    brillo_en(lz, U4, t, 0.42, 0.50, 60, inten=0.45, sem=145)
    # sombras de necrófagos que pasan detrás de la ventana
    for k in range(3):
        u = ((t - t_bajito) * 0.32 + k * 0.33) % 1.0
        X, Y, h = U4.en(t, lerp(0.78, 1.0, u), 0.45, 0.12)
        PF.actor(lz, f"necrofago_corre/ciclo_{int(t * 9 + k) % 8:02d}", X, Y, h, tono=(0.0, 0.0, 0.0), op=0.7, suelo=0, sombra=False)
    fantasma(lz, U4, t, "pamela_hoja/01", 0.58, 0.96, 0.50, op=0.66)
    niebla(lz, t, NIEBLA_AZUL[:1])


U5 = PF.Plano("ventana_fria_b", t_nunca - 0.3, _ESC[AN]["t0"], z0=1.04, z1=1.30, c0=(0.50, 0.60), c1=(0.44, 0.60), par=(26, 6))
wow(t_nunca, "mundo_espiritus", 0.5, dur=_ESC[AN]["t0"] - t_nunca + 0.5, fade=1.0)
snd(t_nunca + 3.5, "viento", 0.5, dur=4.0)


@toma(t_nunca - 0.3, ("fundido", 0.8))
def mu5(lz, t):
    U5.fondo(lz, t)
    brillo_en(lz, U5, t, 0.70, 0.73, 40, inten=0.45 * (1 - 0.6 * smooth(prog(t, t_nunca + 3.0, t_nunca + 5.0))), sem=146)
    brillo_en(lz, U5, t, 0.38, 0.40, 200, color=(0.5, 0.75, 1.0), inten=0.22, sem=147)
    fantasma(lz, U5, t, "pamela_hoja/04", 0.46, 0.92, 0.42, op=0.62)
    X, Y, h = U5.en(t, 0.46, 0.92, 0.42)
    aliento(lz, t, X + 0.06 * h, Y - 0.86 * h, s=1.2, sem=3)
    escarcha(lz, smooth(prog(t, t_nunca, _ESC[AN]["t0"])))
    niebla(lz, t, NIEBLA_AZUL)


# ================================================================== ANILLO (461,8 - 501,8)
t_vuelta2, t_verdad = F(AN, 0), Ts(AN, "verdad", 0)
t_heroe, t_monstruo = F(AN, 1), Ts(AN, "monstruo", 1)
t_cuerpo, t_alianzaA, t_monum, t_cement = F(AN, 2), Ts(AN, "alianza", 2), Ts(AN, "monumento", 2), Ts(AN, "cementerio", 2)
t_vasC, t_tumba, t_anillo = F(AN, 3), Ts(AN, "tumba", 3), Ts(AN, "anillo", 3)
t_segundo, t_salvame = F(AN, 4), Ts(AN, "sálvame", 4)
t_desap = F(AN, 5)

N1 = PF.Plano("casa_marlene_dentro_b", t_vuelta2 - 0.3, t_heroe, z0=1.06, z1=1.18, c0=(0.50, 0.60), c1=(0.56, 0.58), par=(26, 6))
wow(t_vuelta2 + 0.5, "fantasma", 0.4)


@toma(t_vuelta2 - 0.3, ("negro", 0.6))
def an1(lz, t):
    N1.fondo(lz, t)
    brillo_en(lz, N1, t, 0.62, 0.52, 50, inten=0.45, sem=150)
    quieto(lz, N1, t, "aventurero_hoja/04", 0.24, 0.97, 0.56, tono=NUBLADO)
    fantasma(lz, N1, t, "familia_hoja/01", 0.72, 0.94, 0.52, op=0.6, flip=True)
    rot_(lz, "LA VERDAD", W * 0.5, H * 0.12, 60, t, t_verdad)
    niebla(lz, t, NIEBLA_AZUL[:1])


N2 = PF.Plano("barricada_noche_b", t_heroe - 0.3, t_cuerpo, z0=1.10, z1=1.16, c0=(0.50, 0.55), c1=(0.50, 0.55), par=(0, 0))
wow(t_monstruo - 0.2, "sombra", 0.6)
snd(t_monstruo, "golpe_grave", 0.6)


@toma(t_heroe - 0.3, ("desenfoque", 0.6))
def an2(lz, t):
    N2.fondo(lz, t)
    desenfoca(lz, 7)
    tinte(lz, (0.4, 0.75, 0.5), 0.5)
    oscurece(lz, 0.3)
    real(lz, "joseph", W * 0.28, H * 0.48, H * 0.62, t, t_heroe + 0.2, rot=-4)
    if t > t_monstruo - 0.6:
        u = smooth(prog(t, t_monstruo - 0.6, t_monstruo + 0.2))
        D.linea_aa(lz, [(W * 0.42, H * 0.48), (W * lerp(0.42, 0.56, u), H * 0.48)], (0.85, 0.95, 0.85), grosor=10.0)
        if u > 0.95:
            D.linea_aa(lz, [(W * 0.53, H * 0.42), (W * 0.565, H * 0.48), (W * 0.53, H * 0.54)], (0.85, 0.95, 0.85), grosor=10.0)
    real(lz, "rutagrana_corrompido", W * 0.72, H * 0.48, H * 0.62, t, t_monstruo - 0.1, rot=4)
    rot_(lz, "NO MURIÓ COMO UN HÉROE", W * 0.5, H * 0.10, 52, t, t_heroe + 0.3)
    rot_(lz, "SE CONVIRTIÓ EN UN MONSTRUO", W * 0.5, H * 0.90, 50, t, t_monstruo + 0.1)


N3 = PF.Plano("cementerio_andorhal_a", t_cuerpo - 0.3, t_vasC, z0=1.04, z1=1.30, c0=(0.50, 0.55), c1=(0.48, 0.48), par=(30, 8))
V_N3 = [(t_cuerpo, 7.0, 0.20, 0.12, 60, 1, 0.2), (t_cuerpo + 0.6, 7.5, 0.26, 0.16, 46, 1, 1.3)]
wow(t_cuerpo, "amb_peste_dia", 0.4, dur=_ESC["cromi"]["t0"] - t_cuerpo, fade=1.5)
wow(t_cement, "campana", 0.4)


@toma(t_cuerpo - 0.3, ("fundido", 0.6))
def an3(lz, t):
    N3.fondo(lz, t)
    brillo_en(lz, N3, t, 0.52, 0.58, 40, inten=0.4, sem=151)
    cuervos(lz, t, V_N3, tono=NUBLADO)
    k = smooth(prog(t, t_monum - 0.3, t_monum + 0.6))
    brillo_en(lz, N3, t, 0.48, 0.55, 140, color=(1.0, 0.85, 0.4), inten=0.30 * k, sem=152)
    real(lz, "rutagrana_corrompido", W * 0.18, H * 0.40, H * 0.44, t, t_cuerpo + 0.1, t_alianzaA - 0.4, rot=-5,
         op=1.0 - 0.6 * smooth(prog(t, t_cuerpo + 1.5, t_alianzaA)))
    rot_(lz, "SU CUERPO, DESTRUIDO", W * 0.18, H * 0.74, 40, t, t_cuerpo + 0.4, t_alianzaA - 0.4)
    pega(lz, "utileria2/03", W * 0.80, H * 0.32, H * 0.22, t, t_alianzaA - 0.1, rot=8)
    objeto(lz, t, "anillo", "La alianza de Joseph", "Objeto de misión", W * 0.60, H * 0.50, t_alianzaA + 0.3, t_cement - 0.3)
    rot_(lz, "CEMENTERIO DE ANDORHAL", W * 0.5, H * 0.12, 54, t, t_cement - 0.1)
    niebla(lz, t, NIEBLA_VERDE[:2])


N4 = PF.Plano("cementerio_andorhal_b", t_vasC - 0.3, t_segundo, z0=1.04, z1=1.20, c0=(0.46, 0.60), c1=(0.48, 0.58), par=(30, 8))
N5 = PF.Plano("cementerio_andorhal_b", t_segundo - 0.3, _ESC["cromi"]["t0"], z0=1.40, z1=1.55, c0=(0.50, 0.50), c1=(0.50, 0.48),
              par=(30, 8))
snd(t_tumba, "pasos", 0.5, dur=2.0)
snd(t_anillo - 0.6, "golpe_suave", 0.5)
wow(t_anillo, "luz_sagrada", 0.5)
wow(t_segundo + 0.6, "fantasma", 0.8)
wow(t_salvame - 0.3, "susurros", 0.5)
snd(t_salvame, "latido", 0.7)
wow(t_desap, "resurreccion", 0.4)


@toma(t_vasC - 0.3, ("latigo", 0.4))
def an4(lz, t):
    cerca = t >= t_segundo - 0.3
    pl = N5 if cerca else N4
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.48, 0.62, 40, inten=0.4, sem=153)
    if not cerca:
        if t < t_tumba + 1.0:
            paseo(lz, pl, t, "aventurero_hoja/00", t_vasC - 0.3, t_tumba + 1.0, 0.10, 0.40, 0.95, 0.52, tono=NUBLADO, pasos=2.0)
        else:
            quieto(lz, pl, t, "aventurero_hoja/01", 0.40, 0.95, 0.46, tono=NUBLADO, rot=3 * math.sin(t * 8))
        if t > t_anillo - 0.4:
            u = smooth(prog(t, t_anillo - 0.4, t_anillo + 0.8))
            X, Y, s = pl.P(t, 0.48, 0.80 - 0.18 * u)
            PF.brillo(lz, X, Y, 140, color=(1.0, 0.85, 0.4), inten=0.5 * u, t=t, sem=154)
            PF.actor(lz, "utileria2/03", X, Y, 110 * u, ancla=(0.5, 0.5), suelo=0, rot=10 * math.sin(t * 2))
    else:
        a = 1.0 - smooth(prog(t, t_desap - 0.2, t_desap + 0.9))
        quieto(lz, pl, t, "aventurero_hoja/03", 0.30, 1.0, 0.56, tono=NUBLADO)
        fantasma(lz, pl, t, "joseph_hoja/01", 0.56, 0.86, 0.58, t_in=t_segundo + 0.4, t_out=t_desap - 0.2, op=0.6)
        if t > t_desap - 0.2:      # se deshace en motas que suben
            X, Y, h = pl.en(t, 0.56, 0.86, 0.58)
            rng = np.random.default_rng(5)
            u = clamp01((t - t_desap + 0.2) / 2.0)
            for _ in range(40):
                px, py = rng.uniform(-0.25, 0.25) * h, rng.uniform(-1.0, 0.0) * h
                PF.brillo(lz, X + px, Y + py - 160 * u * rng.uniform(0.5, 1.5), 14, color=(0.5, 0.95, 1.0),
                          inten=0.6 * (1 - u), t=t)
        sacude(lz, 4 * golpe_de(t, (t_salvame,), 3.0), t)
        destello_pant(lz, 0.25 * golpe_de(t, (t_salvame,), 2.5), (0.6, 0.9, 1.0))
    niebla(lz, t, NIEBLA_AZUL if cerca else NIEBLA_VERDE[:2])


@functools.lru_cache(maxsize=2)
def _bolsa_base(titulo, n=6, lado=118):
    w, h = 3 * lado + 4 * 18, 2 * lado + 3 * 18 + 56
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=(58, 40, 24, 240), outline=(14, 9, 5, 255), width=5)
    d.rounded_rectangle([7, 7, w - 8, h - 8], 12, outline=(160, 120, 64, 255), width=3)
    d.text((w / 2, 32), titulo, font=D.fuente("serif", 30), fill=(255, 209, 0, 255), anchor="mm")
    for i in range(n):
        x, y = 18 + (i % 3) * (lado + 18), 56 + (i // 3) * (lado + 18)
        d.rectangle([x, y, x + lado, y + lado], fill=(18, 14, 10, 255), outline=(110, 90, 60, 255), width=3)
    a = np.asarray(im, np.uint8)
    return D.Sprite(a[..., :3].copy(), a[..., 3].astype(np.float32) / 255.0, sombra=True, sr=10, off=(6, 10), sop=0.5), lado


def bolsa(lz, t, items, X, Y, t_in, t_out=None, escala=1.0, titulo="Restos de la batalla"):
    """Bolsa de WoW (esquina sup. izq. en X, Y) cuyas casillas se llenan: items = [(pieza, t)]."""
    if t < t_in:
        return
    spr, lado = _bolsa_base(titulo)
    u = PF.entra(t, t_in, 0.4)
    o = clamp01(u * 3) * (1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.4)))
    if o <= 0.01:
        return
    s = escala * (0.7 + 0.3 * u)
    D.pegar(lz, spr, np.array([[s, 0, X], [0, s, Y], [0, 0, 1]], np.float64), o)
    for i, (pz, ti) in enumerate(items):
        if t < ti:
            continue
        k = PF.entra(t, ti, 0.35)
        cx = X + (18 + (i % 3) * (lado + 18) + lado / 2) * s
        cy = Y + (56 + (i // 3) * (lado + 18) + lado / 2) * s
        if t - ti < 0.6:
            PF.brillo(lz, cx, cy, lado * s, color=(1.0, 0.85, 0.4), inten=0.5 * (1 - (t - ti) / 0.6), t=t)
        PF.actor(lz, pz, cx, cy, lado * s * 0.82 * (0.6 + 0.4 * k), op=o * clamp01(k * 3), ancla=(0.5, 0.5), suelo=0, sombra=False)


CR, RE, BA = "cromi", "reliquias", "batalla"
# ================================================================== CROMI (501,8 - 538,2)
t_manda, t_posada = F(CR, 0), Ts(CR, "posada", 0)
t_gnomo, t_cromi, t_dragon = F(CR, 1), Ts(CR, "cromi", 1), Ts(CR, "dragón", 1)
t_futuro, t_mira, t_tragico = F(CR, 2), F(CR, 3), Ts(CR, "trágico", 3)
t_tarde, t_pasadoC = F(CR, 4), Ts(CR, "pasado", 4)

K1 = PF.Plano("posada_andorhal_a", t_manda - 0.3, t_cromi, z0=1.04, z1=1.20, c0=(0.48, 0.60), c1=(0.44, 0.60), par=(26, 6))
wow(t_manda, "taberna", 0.12, dur=t_futuro - t_manda, fade=1.0)
wow(t_cromi, "reloj_arena", 0.8)
wow(t_dragon, "luz_sagrada", 0.4)


@toma(t_manda - 0.3, ("negro", 0.6))
def cr1(lz, t):
    K1.fondo(lz, t)
    for k, (x, y) in enumerate(((0.38, 0.48), (0.52, 0.48))):
        brillo_en(lz, K1, t, x, y, 50, inten=0.5, sem=160 + k)
    rot_(lz, "POSADA EN RUINAS · ANDORHAL", W * 0.5, H * 0.10, 48, t, t_posada)
    if t < t_gnomo + 0.6:
        quieto(lz, K1, t, "cromi_hoja/00", 0.60, 0.95, 0.40, tono=VELA)
    else:
        quieto(lz, K1, t, "cromi_hoja/02", 0.60, 0.95, 0.30, tono=VELA, t_in=t_gnomo + 0.6)
    if t >= t_cromi - 0.4:       # su sombra en la pared es la de un dragón de bronce
        k = smooth(prog(t, t_cromi - 0.4, t_cromi + 0.6))
        X, Y, h = K1.en(t, 0.66, 0.70, 0.70)
        PF.actor(lz, "cromi_hoja/05", X, Y, h, tono=(0.15, 0.10, 0.04), op=0.55 * k, suelo=0, sombra=False, flip=True)
    niebla(lz, t, NIEBLA_AZUL[:1])


K2 = PF.Plano("cavernas_tiempo_a", t_cromi - 0.3, t_futuro, z0=1.04, z1=1.16, c0=(0.50, 0.55), c1=(0.52, 0.55), par=(30, 8))


@toma(t_cromi - 0.3, ("destello", 0.6))
def cr2(lz, t):
    K2.fondo(lz, t)
    for k, (x, y) in enumerate(((0.18, 0.45), (0.88, 0.45))):
        brillo_en(lz, K2, t, x, y, 160, color=(1.0, 0.8, 0.35), inten=0.35 + 0.1 * math.sin(t * 3 + k), sem=162 + k)
    PF.arena_viento(lz, t, fuerza=0.8, y0=0.2, y1=1.0, n=70, sem=4, color=(1.0, 0.85, 0.5))
    u = clamp01((t - t_cromi + 0.3) / 5.0)
    PF.actor(lz, "cromi_hoja/05", lerp(-0.1, 0.55, u) * W, H * (0.42 - 0.06 * math.sin(u * 3)), H * 0.62, ancla=(0.5, 0.5), suelo=0,
             rot=-4 + 3 * math.sin(t * 2))
    real(lz, "cromi", W * 0.80, H * 0.34, H * 0.44, t, t_cromi + 0.1, rot=5)
    real(lz, "cromi_dragon", W * 0.80, H * 0.72, H * 0.36, t, t_dragon, rot=-3)
    rot_(lz, "CROMI", W * 0.22, H * 0.78, 70, t, t_cromi + 0.2)
    rot_(lz, "dragón de bronce · guardiana del tiempo", W * 0.26, H * 0.88, 36, t, t_dragon + 0.3)


K3 = PF.Plano("posada_andorhal_b", t_futuro - 0.3, t_mira, z0=1.40, z1=1.52, c0=(0.62, 0.62), c1=(0.64, 0.60), par=(26, 6))
K4 = PF.Plano("posada_andorhal_b", t_mira - 0.3, t_tarde, z0=1.10, z1=1.20, c0=(0.55, 0.58), c1=(0.58, 0.56), par=(26, 6))
snd(t_futuro + 1.0, "pop", 0.4)
wow(t_mira + 0.3, "luz_sagrada", 0.4)


@toma(t_futuro - 0.3, ("latigo", 0.4))
def cr3(lz, t):
    lejos = t >= t_mira - 0.3
    pl = K4 if lejos else K3
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.73, 0.48, 50, inten=0.5, sem=164)
    brillo_en(lz, pl, t, 0.92, 0.52, 50, inten=0.5, sem=165)
    if not lejos:
        quieto(lz, pl, t, "cromi_hoja/01", 0.58, 0.98, 0.40, tono=VELA, rot=4 * math.sin(t * 1.5))
    else:
        quieto(lz, pl, t, "aventurero_hoja/03", 0.30, 0.98, 0.56, tono=VELA)
        quieto(lz, pl, t, "cromi_hoja/02", 0.62, 0.98, 0.34, tono=VELA, flip=True)
        X, Y, h = pl.en(t, 0.30, 0.98, 0.56)
        PF.brillo(lz, X + 0.12 * h, Y - 1.0 * h, 0.25 * h, color=(1.0, 0.85, 0.4), inten=0.6, t=t, sem=166)
        pega(lz, "utileria2/03", W * 0.80, H * 0.30, H * 0.26, t, t_mira + 0.2, rot=-8)
        real(lz, "joseph", W * 0.86, H * 0.62, H * 0.34, t, t_tragico - 0.6, rot=5, op=0.9)
        rot_(lz, "UN PASADO TRÁGICO", W * 0.5, H * 0.10, 52, t, t_tragico - 0.2)
    niebla(lz, t, NIEBLA_AZUL[:1])


K5 = PF.Plano("cavernas_tiempo_b", t_tarde - 0.3, _ESC[RE]["t0"], z0=1.05, z1=1.25, c0=(0.50, 0.60), c1=(0.40, 0.55), par=(30, 8))
wow(t_pasadoC - 0.3, "reloj_arena", 0.8)
wow(t_tarde, "mundo_espiritus", 0.25, dur=_ESC[RE]["t0"] - t_tarde, fade=1.0)


@toma(t_tarde - 0.3, ("fundido", 0.6))
def cr5(lz, t):
    K5.fondo(lz, t)
    for k, (x, y) in enumerate(((0.10, 0.60), (0.90, 0.60))):
        brillo_en(lz, K5, t, x, y, 170, color=(1.0, 0.8, 0.35), inten=0.4, sem=167 + k)
    PF.arena_viento(lz, t, fuerza=0.6, y0=0.3, y1=1.0, n=60, sem=5, color=(1.0, 0.85, 0.5))
    X, Y, h = K5.en(t, 0.55, 0.95, 0.42)
    PF.brillo(lz, X + 0.15 * h, Y - 1.0 * h, 0.8 * h, color=(1.0, 0.8, 0.35), inten=0.4 + 0.2 * math.sin(t * 5), t=t, sem=169)
    PF.actor(lz, "cromi_hoja/04", X, Y, h, sy=PF.respira(t))
    giro = smooth(prog(t, t_pasadoC - 0.5, t_pasadoC + 0.7))
    PF.actor(lz, "utileria2/15", W * 0.24, H * 0.42, H * 0.36, rot=180 * giro, ancla=(0.5, 0.5), suelo=0)
    rot_(lz, "AYUDARLO EN EL PASADO", W * 0.5, H * 0.10, 56, t, t_pasadoC)


# ================================================================== RELIQUIAS (538,2 - 600,0)
t_plan, t_restos, t_final = F(RE, 0), Ts(RE, "restos", 0), Ts(RE, "final", 0)
t_primero, t_analesR, t_libros, t_guard = F(RE, 1), Ts(RE, "anales", 1), Ts(RE, "libros", 1), Ts(RE, "guardianes", 1)
t_notas, t_carlinR, t_capilla = F(RE, 2), Ts(RE, "carlin", 2), Ts(RE, "capilla", 2)
t_villanos, t_craneo, t_lagoR, t_espadaR = F(RE, 3), Ts(RE, "cráneo", 3), Ts(RE, "lago", 3), Ts(RE, "espada", 3)
t_heroes, t_tratado, t_cruzada, t_escudoR = F(RE, 4), Ts(RE, "tratado", 4), Ts(RE, "cruzada", 4), Ts(RE, "escudo", 4)
t_cruel, t_liberar = F(RE, 5), Ts(RE, "liberar", 5)
t_sabes, t_matando = F(RE, 6), Ts(RE, "matando", 6)
BOLSA = [("utileria2/04", t_analesR + 0.5), ("utileria2/05", t_craneo + 0.3), ("utileria2/06", t_espadaR + 0.3),
         ("utileria2/07", t_tratado + 0.3), ("reales/escudo", t_escudoR + 0.3)]
for _, tb in BOLSA:
    wow(tb, "pagina", 0.5)
    snd(tb, "pop", 0.4)
# el mapa a (como en la Plaga): la cadena de misiones de Cromi en tinta
CADENA = [(0.44, 0.50, "Andorhal"), (0.40, 0.30, "Vega del Amparo"), (0.52, 0.42, "el granero"), (0.58, 0.62, "el lago"),
          (0.86, 0.36, "Capilla de la Luz"), (0.665, 0.635, "Villa Darrow")]
RQ1 = PF.Plano("mapa_lordaeron_a", t_plan - 0.3, t_primero, z0=1.04, z1=1.22, c0=(0.55, 0.50), c1=(0.60, 0.50), par=(0, 0))
snd(t_plan + 0.5, "escribir", 0.5, dur=3.0)
wow(t_final, "sombra", 0.4)


@toma(t_plan - 0.3, ("negro", 0.6))
def r1(lz, t):
    RQ1.fondo(lz, t)
    brillo_en(lz, RQ1, t, 0.86, 0.10, 80, inten=0.45, sem=170)
    ruta_tinta(lz, RQ1, t, [(x, y) for x, y, _ in CADENA], t_plan + 0.3, t_final - 0.5, color=(0.30, 0.18, 0.05), grosor=6.0)
    for k, (x, y, txt) in enumerate(CADENA):
        tk = t_plan + 0.3 + (t_final - 0.8 - t_plan) * k / (len(CADENA) - 1)
        X, Y, s = RQ1.P(t, x, y)
        if t >= tk:
            PF.brillo(lz, X, Y, 50, color=(1.0, 0.8, 0.35), inten=0.4, t=t, sem=70 + k)
        rot_(lz, txt, X, Y - 40, 28, t, tk, rot=0)
    X, Y, s = RQ1.P(t, 0.665, 0.635)
    if t >= t_final - 0.3:
        PF.brillo(lz, X, Y, 160, color=(0.4, 0.9, 1.0), inten=0.6 * PF.entra(t, t_final - 0.3, 0.4), t=t, sem=77)
    rot_(lz, "EL PLAN DE CROMI", W * 0.5, H * 0.10, 56, t, t_plan + 0.2)
    rot_(lz, "CAMBIAR EL FINAL", W * 0.5, H * 0.90, 52, t, t_final, rot=1.5)


RQ2 = PF.Plano("ayuntamiento_andorhal_a", t_primero - 0.3, t_notas, z0=1.04, z1=1.18, c0=(0.50, 0.60), c1=(0.46, 0.60), par=(26, 6))
wow(t_libros, "fantasma", 0.5)
wow(t_guard, "esqueleto_muere", 0.4)
wow(t_guard + 0.4, "banshee", 0.3)


@toma(t_primero - 0.3, ("fundido", 0.5))
def r2(lz, t):
    RQ2.fondo(lz, t)
    brillo_en(lz, RQ2, t, 0.53, 0.62, 50, inten=0.45, sem=171)
    brillo_en(lz, RQ2, t, 0.33, 0.35, 160, color=(0.5, 0.7, 1.0), inten=0.15, sem=172)
    for k in range(5):            # libros malditos que flotan
        X, Y, s = RQ2.P(t, 0.15 + 0.17 * k, 0.30 + 0.08 * math.sin(t * 1.3 + k))
        PF.brillo(lz, X, Y, 80, color=(0.7, 0.4, 1.0), inten=0.3, t=t, sem=80 + k)
        PF.actor(lz, "utileria/09", X, Y, 90, rot=20 * math.sin(t * 1.7 + k), ancla=(0.5, 0.5), suelo=0, tono=(0.8, 0.7, 1.0))
    X, Y, h = RQ2.en(t, 0.72, 0.95, 0.50)
    a = smooth(prog(t, t_guard - 0.4, t_guard + 0.5))
    PF.brillo(lz, X, Y - 0.6 * h, 0.8 * h, color=(0.7, 0.4, 1.0), inten=0.3 * a, t=t, sem=173)
    PF.actor(lz, "monstruos_hoja/01", X, Y + (1 - a) * 0.3 * h, h, op=a, tono=NOCHE, flip=True)
    quieto(lz, RQ2, t, "aventurero_hoja/02", 0.32, 0.97, 0.52, tono=NOCHE)
    objeto(lz, t, "anales", "Los Anales de Villa Darrow", "Objeto de misión", W * 0.03, H * 0.06, t_analesR)
    bolsa(lz, t, BOLSA, W * 0.74, H * 0.05, t_analesR + 0.2, escala=0.85)
    niebla(lz, t, NIEBLA_AZUL[:1])


RQ3 = PF.Plano("escritorio_vela_b", t_notas - 0.3, t_carlinR, z0=1.55, z1=1.65, c0=(0.50, 0.58), c1=(0.52, 0.58), par=(0, 0))
RQ3b = PF.Plano("capilla_esperanza_a", t_carlinR - 0.3, t_villanos, z0=1.04, z1=1.16, c0=(0.55, 0.55), c1=(0.60, 0.52), par=(30, 8))
snd(t_notas + 0.2, "escribir", 0.6, dur=2.5)
wow(t_capilla, "campana", 0.5)


@toma(t_notas - 0.3, ("desenfoque", 0.5))
def r3(lz, t):
    if t < t_carlinR - 0.3:
        RQ3.fondo(lz, t)
        brillo_en(lz, RQ3, t, 0.80, 0.15, 120, inten=0.5, sem=174)
        # notas de Cromi en los márgenes: garabatos de tinta que se escriben
        for k in range(6):
            t0 = t_notas + 0.2 + 0.4 * k
            if t < t0:
                break
            u = smooth(prog(t, t0, t0 + 0.45))
            xa, ya = 0.33 + 0.18 * (k % 2), 0.42 + 0.07 * (k // 2)
            for w0, w1 in ((0.0, 0.30), (0.36, 0.62), (0.68, 1.0)):     # tres «palabras» con letras de distinta altura
                n_ = 14
                pts = [RQ3.P(t, xa + 0.13 * min(u, lerp(w0, w1, i / n_)), ya + 0.006 * math.sin(i * 2.3 + k) + 0.004 * math.sin(i * 5.1 + 3 * k))[:2]
                       for i in range(n_ + 1) if lerp(w0, w1, i / n_) <= u + 1e-6]
                if len(pts) > 1:
                    D.linea_aa(lz, pts, (0.25, 0.12, 0.05), grosor=3.0, sombra=False)
        rot_(lz, "NOTAS DE CROMI", W * 0.5, H * 0.10, 50, t, t_notas + 0.3)
    else:
        RQ3b.fondo(lz, t)
        brillo_en(lz, RQ3b, t, 0.62, 0.37, 90, inten=0.55, sem=175)
        quieto(lz, RQ3b, t, "familia_hoja/05", 0.46, 0.95, 0.52, tono=NUBLADO)
        quieto(lz, RQ3b, t, "aventurero_hoja/04", 0.20, 0.97, 0.50, tono=NUBLADO)
        real(lz, "carlin", W * 0.82, H * 0.38, H * 0.48, t, t_carlinR - 0.1, rot=4)
        rot_(lz, "CARLIN · sigue vivo", W * 0.82, H * 0.68, 40, t, t_carlinR + 0.2)
        rot_(lz, "CAPILLA DE LA ESPERANZA DE LA LUZ", W * 0.5, H * 0.10, 44, t, t_capilla)
        niebla(lz, t, NIEBLA_VERDE[:2])
    bolsa(lz, t, BOLSA, W * 0.74, H * 0.05, t_notas - 0.3, t_carlinR - 0.4, escala=0.85)


RQ4 = PF.Plano("lago_fantasmas_a", t_villanos - 0.3, t_heroes, z0=1.04, z1=1.18, c0=(0.50, 0.58), c1=(0.46, 0.60), par=(30, 8))
wow(t_lagoR, "mundo_espiritus", 0.4, dur=t_heroes - t_lagoR, fade=1.0)
for k in range(3):
    wow(t_lagoR + 0.5 + 1.3 * k, "espada_escudo", 0.2)


@toma(t_villanos - 0.3, ("latigo", 0.4))
def r4(lz, t):
    RQ4.fondo(lz, t)
    brillo_en(lz, RQ4, t, 0.30, 0.82, 40, inten=0.4, sem=176)
    for k, (pz, x0, fr, fl) in enumerate((("defensores_hoja/00", 0.40, 0.20, False), ("esqueletos_hoja/01", 0.52, 0.20, True),
                                          ("defensores_hoja/03", 0.64, 0.18, True))):
        if t > t_lagoR - 0.5:
            fantasma(lz, RQ4, t, pz, x0 + 0.03 * math.sin(t * 2 + k), 0.60, fr, t_in=t_lagoR - 0.5, op=0.5, flip=fl)
    pega(lz, "utileria2/05", W * 0.30, H * 0.40, H * 0.30, t, t_craneo - 0.1, rot=-6)
    rot_(lz, "EL CRÁNEO DE HORGUS", W * 0.30, H * 0.60, 40, t, t_craneo + 0.1)
    pega(lz, "utileria2/06", W * 0.62, H * 0.86, H * 0.20, t, t_espadaR - 0.1, rot=-12)
    rot_(lz, "LA ESPADA ROTA DE MARDUK", W * 0.40, H * 0.92, 40, t, t_espadaR + 0.1)
    bolsa(lz, t, BOLSA, W * 0.74, H * 0.05, t_villanos - 0.3, escala=0.85)
    niebla(lz, t, NIEBLA_AZUL)


RQ5 = PF.Plano("vega_amparo_a", t_heroes - 0.3, t_cruel, z0=1.04, z1=1.16, c0=(0.48, 0.58), c1=(0.42, 0.58), par=(30, 8))
wow(t_cruzada, "grito_guerra", 0.4)


@toma(t_heroes - 0.3, ("fundido", 0.5))
def r5(lz, t):
    RQ5.fondo(lz, t)
    brillo_en(lz, RQ5, t, 0.40, 0.55, 40, inten=0.45, sem=177)
    quieto(lz, RQ5, t, "monstruos_hoja/02", 0.26, 0.93, 0.48, tono=NUBLADO, t_in=t_cruzada - 0.4)
    quieto(lz, RQ5, t, "monstruos_hoja/03", 0.44, 0.90, 0.42, tono=NUBLADO, t_in=t_cruzada - 0.2, fase=1.0)
    pega(lz, "utileria2/07", W * 0.62, H * 0.30, H * 0.22, t, t_tratado - 0.1, rot=-8)
    rot_(lz, "EL TRATADO DE DAVIL", W * 0.62, H * 0.45, 40, t, t_tratado + 0.1, t_escudoR - 0.4)
    rot_(lz, "LA CRUZADA ESCARLATA", W * 0.50, H * 0.12, 46, t, t_cruzada)
    real(lz, "escudo", W * 0.84, H * 0.62, H * 0.28, t, t_escudoR - 0.1, rot=5)
    rot_(lz, "EL ESCUDO DE JOSEPH", W * 0.82, H * 0.80, 40, t, t_escudoR + 0.1)
    bolsa(lz, t, BOLSA, W * 0.74, H * 0.05, t_heroes - 0.3, escala=0.85)
    niebla(lz, t, NIEBLA_AZUL[:1])


def _liberados(t):
    if t < t_matando:
        return 0
    return min(15, int((t - t_matando) / 0.38) + 1)


RQ6 = PF.Plano("ruinas_plaza_noche_b", t_cruel - 0.3, t_sabes, z0=1.04, z1=1.14, c0=(0.50, 0.60), c1=(0.52, 0.60), par=(30, 8))
RQ7 = PF.Plano("ruinas_plaza_noche_b", t_sabes - 0.3, _ESC[BA]["t0"], z0=1.35, z1=1.50, c0=(0.50, 0.66), c1=(0.52, 0.64),
              par=(30, 8))
wow(t_cruel, "necrofago", 0.5)
wow(t_liberar, "mision_acepta", 0.6)
for k in range(6):
    wow(t_matando + 0.38 * k * 2.5, "espada_carne", 0.45)
    wow(t_matando + 0.38 * k * 2.5 + 0.2, "fantasma", 0.25)


@toma(t_cruel - 0.3, ("negro", 0.6))
def r6(lz, t):
    cerca = t >= t_sabes - 0.3
    pl = RQ7 if cerca else RQ6
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.38, 0.48, 40, inten=0.45, sem=178)
    if not cerca:
        for k in range(4):
            paseo(lz, pl, t, "plaga_hoja/02" if k % 2 else "necrofago_corre/ciclo_00", t_cruel - 0.3, t_sabes + 1,
                  0.15 + 0.22 * k, 0.20 + 0.22 * k + 0.05 * (-1) ** k, 0.86 + 0.03 * (k % 2), 0.34, tono=NOCHE_PESTE, pasos=1.0,
                  flip=k % 2 == 0)
        rot_(lz, "LA PARTE MÁS CRUEL", W * 0.5, H * 0.12, 56, t, t_cruel + 0.2, t_liberar - 0.6)   # sale antes del rastreador
    else:
        n = _liberados(t)
        g = golpe_de(t, [t_matando + 0.95 * k for k in range(6)], 5.0)
        quieto(lz, pl, t, "aventurero_hoja/02", 0.34, 0.98, 0.58, tono=NOCHE, rot=-8 * g)
        X, Y, h = pl.en(t, 0.62, 0.98, 0.48)
        cae = smooth(prog(t, t_matando, t_matando + 0.5))
        PF.actor(lz, "necrofago_corre/ciclo_00", X, Y, h, tono=NOCHE_PESTE, rot=80 * cae, op=1 - 0.5 * cae, flip=True)
        if t > t_matando:      # el espíritu del defensor sube y se va
            u = clamp01((t - t_matando) / 2.5)
            PF.actor(lz, "defensores_hoja/00", X, Y - 0.6 * h * u, h * 0.95, op=0.6 * (1 - u ** 2), tono=FANTASMA, suelo=0, sombra=False)
            PF.brillo(lz, X, Y - 0.6 * h * u - 0.5 * h, 0.6 * h, color=(0.5, 0.95, 1.0), inten=0.4 * (1 - u), t=t)
        sacude(lz, 4 * g, t)
    rastreador(lz, t, "Los defensores", [("Espíritus de Villa Darrow liberados", f"{_liberados(t)}/15")], t_liberar - 0.2,
               X=W * 0.60, Y=H * 0.10)
    niebla(lz, t, NIEBLA_VERDE[:2])


# ================================================================== BATALLA (600,0 - 680,0)
t_reunido, t_fardo = F(BA, 0), Ts(BA, "fardo", 0)
t_dejas, t_muertos = F(BA, 1), Ts(BA, "muertos", 1)
t_armas = F(BA, 2)
t_tuEstas, t_davilB, t_horgB, t_proteger = F(BA, 3), Ts(BA, "davil", 3), Ts(BA, "horgus", 3), Ts(BA, "proteger", 3)
t_reagr = F(BA, 4)
t_vuelveM, t_terrible = F(BA, 5), Ts(BA, "terrible", 5)
t_impedir, t_esoYa, t_volverB = F(BA, 6), Ts(BA, "eso", 6), Ts(BA, "volver", 6)
t_unico, t_contagie, t_casasB = F(BA, 7), Ts(BA, "contagie", 7), Ts(BA, "casas", 7)
t_condenada, t_derribas = F(BA, 8), Ts(BA, "derribas", 8)
t_espiritu, t_perdon = F(BA, 9), Ts(BA, "perdón", 9)
t_derrotada, t_grita = F(BA, 10), F(BA, 11)

B1 = PF.Plano("cavernas_tiempo_b", t_reunido - 0.3, t_dejas, z0=1.30, z1=1.40, c0=(0.40, 0.66), c1=(0.44, 0.64), par=(30, 8))
wow(t_fardo, "mision_acepta", 0.6)
wow(t_reunido, "reloj_arena", 0.5)


@toma(t_reunido - 0.3, ("fundido", 0.5))
def b1(lz, t):
    B1.fondo(lz, t)
    brillo_en(lz, B1, t, 0.10, 0.60, 170, color=(1.0, 0.8, 0.35), inten=0.4, sem=180)
    PF.arena_viento(lz, t, fuerza=0.5, y0=0.4, y1=1.0, n=50, sem=6, color=(1.0, 0.85, 0.5))
    quieto(lz, B1, t, "cromi_hoja/03", 0.38, 0.97, 0.40)
    quieto(lz, B1, t, "aventurero_hoja/04", 0.64, 0.98, 0.62, flip=True)
    cierra = smooth(prog(t, t_fardo - 0.8, t_fardo))
    bolsa(lz, t, BOLSA, W * 0.36, H * 0.05, t_reunido - 0.3, t_fardo - 0.6, escala=0.85)   # a W*0.70 tapaba la cara del aventurero
    if t > t_fardo - 0.4:
        pega(lz, "utileria2/08", W * 0.52, H * 0.20, H * 0.24, t, t_fardo - 0.4, rot=-5)
        PF.brillo(lz, W * 0.52, H * 0.20, H * 0.3, color=(1.0, 0.85, 0.4), inten=0.4 * cierra, t=t)
        rot_(lz, "FARDO DE RELIQUIAS", W * 0.52, H * 0.36, 42, t, t_fardo + 0.1)


B2 = PF.Plano("plaza_fantasmas_a", t_dejas - 0.3, t_armas, z0=1.06, z1=1.18, c0=(0.48, 0.62), c1=(0.50, 0.60), par=(30, 8))
B3 = PF.Plano("plaza_fantasmas_a", t_armas - 0.3, t_tuEstas, z0=1.40, z1=1.50, c0=(0.42, 0.62), c1=(0.44, 0.60), par=(30, 8))
wow(t_dejas - 0.3, "mundo_espiritus", 0.45, dur=_ESC["te"]["t0"] - t_dejas, fade=2.0)
wow(t_dejas + 0.4, "luz_sagrada", 0.5)
wow(t_muertos, "resurreccion", 0.8)
wow(t_armas, "campana", 0.7)
wow(t_armas + 1.5, "campana", 0.5)
wow(t_armas + 0.1, "grito_guerra", 0.8)
FANT_DEF = [("defensores_hoja/00", 0.20, 0.44, False), ("defensores_hoja/01", 0.34, 0.48, False), ("defensores_hoja/03", 0.70, 0.46, True),
            ("defensores_hoja/02", 0.84, 0.44, True)]


@toma(t_dejas - 0.3, ("negro", 0.6))
def b2(lz, t):
    pl = B3 if t >= t_armas - 0.3 else B2
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.72, 0.43, 50, inten=0.45, sem=181)
    X, Y, s = pl.P(t, 0.52, 0.86)
    PF.brillo(lz, X, Y - 30, 160, color=(1.0, 0.85, 0.4), inten=0.45 + 0.15 * math.sin(t * 4), t=t, sem=182)
    PF.actor(lz, "utileria2/08", X, Y, 110 * s / pl.P(t, 0.5, 0.5)[2] * 1.0)
    for k, (pz, x, fr, fl) in enumerate(FANT_DEF):
        fantasma(lz, pl, t, pz, x, 0.95, fr, t_in=t_muertos - 0.2 + 0.3 * k, flip=fl, op=0.58)
    if pl is B2:
        quieto(lz, pl, t, "aventurero_hoja/05", 0.60, 0.98, 0.50, tono=NOCHE)
    fantasma(lz, pl, t, "joseph_hoja/03", 0.50, 0.97, 0.56, t_in=t_armas - 0.6, op=0.66)
    niebla(lz, t, NIEBLA_AZUL)


B4 = PF.Plano("plaza_fantasmas_b", t_tuEstas - 0.3, t_reagr, z0=1.04, z1=1.16, c0=(0.50, 0.62), c1=(0.52, 0.60), par=(30, 8))
B5 = PF.Plano("plaza_fantasmas_b", t_reagr - 0.3, t_vuelveM, z0=1.30, z1=1.42, c0=(0.40, 0.64), c1=(0.42, 0.62), par=(30, 8))
for k in range(5):
    wow(t_tuEstas + 1.0 + 1.5 * k, "espada_escudo" if k % 2 else "espada_carne", 0.35)
wow(t_horgB + 0.8, "necrofago2", 0.6)
wow(t_reagr, "grito_guerra", 0.9)


def _vida_horgus(t):
    return 1.0 - smooth(prog(t, t_tuEstas + 0.5, t_horgB + 0.9))


def _marcos(lz, t, t_in):
    marco_unidad(lz, t, W * 0.06, H * 0.10, "davil", "Davil Fuegoluz", 0.55 + 0.25 * math.sin(t * 0.9), t_in)
    marco_unidad(lz, t, W * 0.06, H * 0.22, "joseph", "Capitán Joseph", 0.85 - 0.1 * math.sin(t * 0.7), t_in + 0.3)
    marco_unidad(lz, t, W * 0.66, H * 0.10, "horgus", "Horgus el Devastador", _vida_horgus(t), t_in + 0.6,
                 color=(0.80, 0.10, 0.08))


@toma(t_tuEstas - 0.3, ("latigo", 0.4))
def b4(lz, t):
    pl = B5 if t >= t_reagr - 0.3 else B4
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.22, 0.50, 50, inten=0.45, sem=183)
    g = golpe_de(t, [t_tuEstas + 1.0 + 1.5 * k for k in range(5)], 5.0)
    if pl is B4:
        fantasma(lz, pl, t, "davil_hoja/01", 0.40, 0.96, 0.52, op=0.6)
        vh = _vida_horgus(t)
        X, Y, h = pl.en(t, 0.64, 0.96, 0.58)
        cae = 1.0 - vh
        PF.actor(lz, "horgus_hoja/02" if vh > 0.05 else "horgus_hoja/04", X, Y, h * (1 - 0.3 * (vh <= 0.05)), op=0.55,
                 tono=FANTASMA, suelo=0, sombra=False, flip=True, rot=6 * g)
        quieto(lz, pl, t, "aventurero_hoja/02", 0.18, 1.0, 0.58, tono=NOCHE, rot=-6 * g)
        fantasma(lz, pl, t, "joseph_hoja/03", 0.84, 0.95, 0.50, op=0.55, flip=True)
    else:
        for k, (pz, x, fr, fl) in enumerate(FANT_DEF):
            X, Y, h = pl.en(t, x, 0.95, fr * 1.2)
            salto = abs(math.sin((t - t_reagr) * 3.4 + k))
            fantasma(lz, pl, t, pz, x, 0.95 - 0.02 * salto, fr * 1.2, flip=fl, op=0.55)
        fantasma(lz, pl, t, "joseph_hoja/03", 0.52, 0.98, 0.62, op=0.66)
    niebla(lz, t, NIEBLA_AZUL)
    sacude(lz, 4 * g, t)
    _marcos(lz, t, t_tuEstas + 0.2)


B6 = PF.Plano("puerta_humo_b", t_vuelveM - 0.3, t_impedir, z0=1.06, z1=1.20, c0=(0.50, 0.58), c1=(0.48, 0.60), par=(30, 8))
snd(t_vuelveM, "galope", 0.8, dur=3.0)
wow(t_vuelveM + 0.4, "dk_hechizo", 0.7)
wow(t_terrible, "latido_juego", 0.8)


@toma(t_vuelveM - 0.3, ("negro", 0.5))
def b6(lz, t):
    B6.fondo(lz, t)
    brillo_en(lz, B6, t, 0.82, 0.65, 50, inten=0.4, sem=184)
    brillo_en(lz, B6, t, 0.47, 0.55, 220, color=(0.4, 1.0, 0.5), inten=0.3, sem=185)
    u = clamp01((t - t_vuelveM + 0.3) / 3.5)
    X, Y, h = B6.en(t, lerp(0.46, 0.56, u), lerp(0.62, 0.95, u), lerp(0.16, 0.62, u))
    i = int((t - t_vuelveM) * 10) % PF.ciclo_n("marduk_galope")
    PF.brillo(lz, X, Y - 0.5 * h, 0.9 * h, color=(0.4, 0.9, 1.0), inten=0.3, t=t, sem=186)
    PF.actor(lz, f"marduk_galope/ciclo_{i:02d}", X, Y, h * 1.25, tono=FANT_OSC, op=0.75, suelo=0)
    oscurece(lz, 0.3 * smooth(prog(t, t_terrible - 0.3, t_terrible + 1.0)))
    rot_(lz, "MARDUK VUELVE", W * 0.24, H * 0.12, 54, t, t_vuelveM + 0.6)
    niebla(lz, t, NIEBLA_VERDE)


B7 = PF.Plano("escritorio_vela_b", t_impedir - 0.3, t_unico, z0=1.20, z1=1.30, c0=(0.50, 0.57), c1=(0.50, 0.57), par=(0, 0))
snd(t_impedir + 0.3, "escribir", 0.5, dur=2.0)
snd(t_esoYa, "golpe_grave", 0.5)
snd(t_volverB, "latido", 0.7)
NODO = (0.50, 0.56)


@toma(t_impedir - 0.3, ("desenfoque", 0.6))
def b7(lz, t):
    B7.fondo(lz, t)
    brillo_en(lz, B7, t, 0.80, 0.15, 120, inten=0.5, sem=187)
    # dos líneas del tiempo: la original (arriba) y la reescrita (abajo) que TIENE que volver al mismo nudo
    orig = [(0.34, 0.46), (0.42, 0.50), NODO, (0.60, 0.48), (0.66, 0.46)]
    nueva = [(0.34, 0.68), (0.42, 0.64), NODO, (0.58, 0.66), (0.66, 0.70)]
    ruta_tinta(lz, B7, t, orig, t_impedir + 0.2, t_impedir + 2.0, color=(0.25, 0.12, 0.05), grosor=6.0)
    ruta_tinta(lz, B7, t, nueva, t_esoYa, t_volverB + 0.4, color=(0.10, 0.25, 0.35), grosor=6.0)
    X, Y, s = B7.P(t, *NODO)
    if t > t_esoYa:
        PF.brillo(lz, X, Y, 90, color=(0.3, 1.0, 0.4), inten=0.4 + 0.2 * math.sin(t * 6), t=t, sem=188)
    rot_(lz, "ORIGINAL", *B7.P(t, 0.36, 0.42)[:2], 30, t, t_impedir + 0.3, rot=0)
    rot_(lz, "REESCRITA", *B7.P(t, 0.36, 0.73)[:2], 30, t, t_esoYa, rot=0)
    rot_(lz, "JOSEPH SE CORROMPE", X, Y + 60, 30, t, t_esoYa + 0.4, rot=0)
    rot_(lz, "LO QUE YA PASÓ TIENE QUE VOLVER A PASAR", W * 0.5, H * 0.10, 46, t, t_volverB - 0.4)


B8 = PF.Plano("plaza_fantasmas_a", t_unico - 0.3, t_condenada, z0=1.04, z1=1.14, c0=(0.52, 0.62), c1=(0.50, 0.62), par=(30, 8))
wow(t_unico, "peste_burbuja", 0.6)
wow(t_contagie, "sombra", 0.5)
snd(t_casasB, "latido", 0.8)


@toma(t_unico - 0.3, ("latigo", 0.4))
def b8(lz, t):
    B8.fondo(lz, t)
    brillo_en(lz, B8, t, 0.72, 0.43, 50, inten=0.45, sem=189)
    sombra_pz(lz, B8, t, "rutagrana_hoja/02", 0.36, 0.96, 0.60, op=0.8)
    Xs, Ys, hs_ = B8.en(t, 0.36, 0.96, 0.60)
    u_cast = clamp01((t - t_unico) / (t_condenada - t_unico))
    for k, (pz, x, fr, fl) in enumerate(FANT_DEF[2:]):
        X, Y, h = B8.en(t, x, 0.95, fr)
        fantasma(lz, B8, t, pz, x, 0.95, fr, flip=fl, op=0.55)
        lazo(lz, (Xs + 0.25 * hs_, Ys - 0.62 * hs_), (X, Y - 0.6 * h), t, u_cast * (0.8 + 0.2 * k), n=2, amp=26, sem=k)
    quieto(lz, B8, t, "aventurero_hoja/02", 0.56, 1.0, 0.56, tono=NOCHE)
    barra_lanzar(lz, t, W * 0.5, H * 0.88, "Corrupción", t_unico, t_condenada)
    rot_(lz, "ANTES DE QUE ENTREN EN LAS CASAS", W * 0.5, H * 0.10, 46, t, t_casasB - 0.2)
    niebla(lz, t, NIEBLA_VERDE[:2])


B9 = PF.Plano("plaza_fantasmas_b", t_condenada - 0.3, t_espiritu, z0=1.30, z1=1.45, c0=(0.50, 0.64), c1=(0.52, 0.62), par=(30, 8))
wow(t_condenada, "sombra", 0.7)
wow(t_derribas, "espada_carne", 0.9)
wow(t_derribas + 0.05, "luz_impacto", 0.8)


@toma(t_condenada - 0.3, ("latigo", 0.4))
def b9(lz, t):
    B9.fondo(lz, t)
    brillo_en(lz, B9, t, 0.22, 0.50, 50, inten=0.45, sem=190)
    cae = smooth(prog(t, t_derribas, t_derribas + 0.8))
    sombra_pz(lz, B9, t, "rutagrana_hoja/01" if cae < 0.3 else "rutagrana_hoja/03", 0.62, 0.97, 0.64)
    g = golpe_de(t, (t_derribas,), 4.0)
    X, Y, h = B9.en(t, 0.30 + 0.06 * g, 1.0, 0.62)
    PF.actor(lz, "aventurero_hoja/02", X, Y, h, tono=NOCHE, rot=-10 * g)
    destello_pant(lz, 0.5 * g, (0.9, 1.0, 0.95))
    sacude(lz, 8 * g, t)
    niebla(lz, t, NIEBLA_VERDE[:2])


B10 = PF.Plano("plaza_fantasmas_a", t_espiritu - 0.3, t_derrotada, z0=1.55, z1=1.70, c0=(0.50, 0.60), c1=(0.50, 0.58), par=(30, 8))
wow(t_espiritu + 0.3, "resurreccion", 0.7)
snd(t_perdon, "golpe_suave", 0.3)


@toma(t_espiritu - 0.3, ("destello", 0.6))
def b10(lz, t):
    B10.fondo(lz, t)
    desenfoca(lz, 3)
    u = smooth(prog(t, t_espiritu, t_espiritu + 2.0))
    sombra_pz(lz, B10, t, "rutagrana_hoja/04", 0.50, 0.95, 0.60, t_out=t_espiritu + 0.4, humo=True)
    X, Y, h = B10.en(t, 0.50, 0.95, 0.60)
    PF.brillo(lz, X, Y - 0.5 * h, 1.2 * h, color=(0.85, 0.95, 1.0), inten=0.45 * u, t=t, sem=191)
    pz = "joseph_hoja/01" if t < t_perdon - 0.4 else "reencuentro_hoja/05"
    PF.brillo(lz, X, Y - 0.55 * h, 0.7 * h, color=(0.6, 0.95, 1.0), inten=0.35 * u, t=t, sem=194)
    PF.actor(lz, pz, X, Y, h * (0.95 if pz.startswith("reen") else 1.0), op=0.66 * u, tono=(0.62, 0.98, 1.08), suelo=0, sombra=False,
             sy=PF.respira(t))
    rot_(lz, "LIMPIO", W * 0.80, H * 0.20, 56, t, t_espiritu + 1.0)
    rot_(lz, "«PERDÓN»", W * 0.80, H * 0.32, 48, t, t_perdon, rot=2)


B11 = PF.Plano("plaza_fantasmas_b", t_derrotada - 0.3, t_grita, z0=1.10, z1=1.04, c0=(0.50, 0.60), c1=(0.50, 0.58), par=(30, 8))
B12 = PF.Plano("ruinas_alba_b", t_grita - 0.3, _ESC["te"]["t0"], z0=1.20, z1=1.02, c0=(0.50, 0.58), c1=(0.50, 0.54), par=(34, 8))
wow(t_derrotada + 0.3, "mision_completa", 0.9)
wow(t_derrotada + 0.6, "campana", 0.6)
wow(t_grita + 1.0, "amb_peste_dia", 0.35, dur=_ESC["te"]["t0"] - t_grita, fade=1.5)


@toma(t_derrotada - 0.3, ("fundido", 0.5))
def b11(lz, t):
    if t < t_grita - 0.3:
        B11.fondo(lz, t)
        brillo_en(lz, B11, t, 0.22, 0.50, 50, inten=0.45, sem=192)
        for k, (pz, x, fr, fl) in enumerate(FANT_DEF + [("joseph_hoja/03", 0.52, 0.52, False), ("davil_hoja/00", 0.62, 0.50, True)]):
            salto = abs(math.sin((t - t_derrotada) * 3.6 + k))
            fantasma(lz, B11, t, pz, x, 0.95 - 0.03 * salto, fr, flip=fl, op=0.55)
        aviso_oro(lz, t, "Misión completada: La Batalla de Villa Darrow", t_derrotada + 0.3, t_grita - 0.5)
        niebla(lz, t, NIEBLA_AZUL)
    else:
        B12.fondo(lz, t)
        brillo_en(lz, B12, t, 0.94, 0.58, 40, inten=0.35, sem=193)
        a = 1.0 - smooth(prog(t, t_grita + 0.5, t_grita + 4.0))
        for k, (pz, x, fr, fl) in enumerate(FANT_DEF):
            fantasma(lz, B12, t, pz, x, 0.92, fr * 0.8, flip=fl, op=0.45 * a)
        rot_(lz, "UN PUEBLO DONDE YA NO VIVE NADIE", W * 0.5, H * 0.86, 46, t, t_grita + 2.0)
        niebla(lz, t, NIEBLA_AZUL[:1])


def fantasma_ciclo(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=1.35, op=0.62):
    """Un ciclo de Flow (correr) como fantasma: anda() teñido y translúcido, con halo."""
    if t < ta:
        return
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    X, Y, h = pl.en(t, lerp(x0, x1, u), y, frac)
    PF.brillo(lz, X, Y - 0.5 * h, 1.0 * h, color=(0.35, 0.85, 0.95), inten=0.25, t=t, sem=7)
    anda(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=paso, tono=FANTASMA, op=op)


TE, CI = "te", "cierre"
# ================================================================== TÉ (680,0 - 730,9)
t_vuelvesT, t_oi, t_susurr = F(TE, 0), F(TE, 1), Ts(TE, "susurraban", 1)
t_sonrie, t_termino = F(TE, 2), Ts(TE, "terminó", 2)
t_preparo, t_azucar = F(TE, 3), Ts(TE, "azúcar", 3)
t_llega, t_fantJ, t_nombre = F(TE, 4), Ts(TE, "fantasma", 4), Ts(TE, "nombre", 4)
t_corre, t_papi = F(TE, 5), Ts(TE, "papi", 5)
t_extr = F(TE, 6)
t_antesT, t_llave, t_cofre, t_gracias = F(TE, 7), Ts(TE, "llave", 7), Ts(TE, "cofre", 7), Ts(TE, "gracias", 7)

J1 = PF.Plano("casa_pamela_alba_a", t_vuelvesT - 0.3, t_oi, z0=1.02, z1=1.12, c0=(0.50, 0.58), c1=(0.56, 0.58), par=(34, 8))
J2 = PF.Plano("casa_pamela_alba_b", t_oi - 0.3, t_preparo, z0=1.30, z1=1.40, c0=(0.66, 0.62), c1=(0.68, 0.60), par=(30, 8))
snd(t_vuelvesT, "pasos", 0.5, dur=2.5)
snd(t_vuelvesT + 0.5, "pio", 0.3)
wow(t_susurr - 0.5, "susurros", 0.5)
snd(t_termino, "pop", 0.4)


@toma(t_vuelvesT - 0.3, ("fundido", 1.0))
def te1(lz, t):
    if t < t_oi - 0.3:
        J1.fondo(lz, t)
        brillo_en(lz, J1, t, 0.82, 0.57, 50, inten=0.4, sem=200)
        paseo(lz, J1, t, "aventurero_hoja/00", t_vuelvesT - 0.3, t_oi + 0.5, 0.20, 0.50, 0.92, 0.46, tono=ALBA, pasos=2.0)
        niebla(lz, t, NIEBLA_AZUL[:1])
        return
    J2.fondo(lz, t)
    brillo_en(lz, J2, t, 0.83, 0.60, 50, inten=0.45, sem=201)
    feliz = t >= t_sonrie
    if not feliz:
        fantasma(lz, J2, t, "pamela_hoja/03", 0.66, 0.86, 0.26, op=0.62)
        for k in range(3):     # susurros: siluetas que rondan en la niebla
            u = ((t - t_oi) * 0.15 + k / 3) % 1.0
            fantasma(lz, J2, t, "monstruos_hoja/05", lerp(0.15, 0.45, u), 0.70 + 0.05 * k, 0.24, op=0.22, flip=k % 2 == 0)
    else:
        salto = abs(math.sin((t - t_sonrie) * 3.8)) * smooth(prog(t, t_termino - 0.4, t_termino + 0.3))
        X, Y, h = J2.en(t, 0.66, 0.86, 0.28)
        PF.brillo(lz, X, Y - 0.5 * h, h, color=(0.6, 0.95, 1.0), inten=0.3, t=t, sem=202)
        pz = "reencuentro_hoja/02" if t > t_termino - 0.4 else "pamela_hoja/02"
        PF.actor(lz, pz, X, Y - 0.12 * h * salto, h, op=0.66, tono=FANTASMA, suelo=0, sombra=False)
        rot_(lz, "«¡LA BATALLA TERMINÓ!»", W * 0.30, H * 0.20, 50, t, t_termino)
    niebla(lz, t, NIEBLA_AZUL)


J3 = PF.Plano("casa_pamela_dentro_a", t_preparo - 0.3, t_llega, z0=1.70, z1=1.85, c0=(0.48, 0.60), c1=(0.47, 0.60), par=(26, 6))
snd(t_preparo + 0.4, "clink", 0.5)
snd(t_azucar, "clink", 0.5, tono=1.2)


@toma(t_preparo - 0.3, ("desenfoque", 0.5))
def te4(lz, t):
    J3.fondo(lz, t)
    brillo_en(lz, J3, t, 0.47, 0.56, 60, inten=0.5, sem=203)
    for k, (pz, x, fr, tk) in enumerate((("utileria2/09", 0.42, 0.07, t_preparo + 0.2), ("utileria2/11", 0.50, 0.04, t_preparo + 0.6),
                                         ("utileria2/11", 0.54, 0.04, t_preparo + 0.9), ("utileria2/12", 0.58, 0.05, t_azucar - 0.1))):
        quieto(lz, J3, t, pz, x, 0.615, fr, tono=VELA, t_in=tk)
    X, Y, s = J3.P(t, 0.42, 0.56)
    if t > t_preparo + 0.4:
        PF.humo(lz, t, X + 20, Y, s=0.4, color=(0.9, 0.9, 0.92), op=0.25, sem=12, alto=120)
    fantasma(lz, J3, t, "reencuentro_hoja/03", 0.30, 0.80, 0.34, op=0.6)
    rot_(lz, "TÉ CON AZÚCAR", W * 0.70, H * 0.16, 56, t, t_azucar)


J4 = PF.Plano("casa_pamela_alba_a", t_llega - 0.3, t_corre, z0=1.06, z1=1.16, c0=(0.46, 0.60), c1=(0.52, 0.60), par=(34, 8))
wow(t_fantJ - 0.2, "fantasma", 0.6)
wow(t_nombre, "resurreccion", 0.4)


@toma(t_llega - 0.3, ("fundido", 0.6))
def te5(lz, t):
    J4.fondo(lz, t)
    brillo_en(lz, J4, t, 0.82, 0.57, 50, inten=0.45, sem=204)
    u = smooth(prog(t, t_fantJ - 0.4, t_nombre + 0.3))
    fantasma(lz, J4, t, "joseph_hoja/05" if u < 1 else "joseph_hoja/01", lerp(0.08, 0.40, u), 0.92, 0.48, t_in=t_fantJ - 0.6,
             op=0.62)
    rot_(lz, "«PAMELA…»", W * 0.30, H * 0.20, 50, t, t_nombre)
    niebla(lz, t, NIEBLA_AZUL)


J5 = PF.Plano("casa_pamela_alba_b", t_corre - 0.3, t_extr, z0=1.06, z1=1.16, c0=(0.55, 0.60), c1=(0.52, 0.60), par=(30, 8))
J6 = PF.Plano("casa_pamela_alba_b", t_extr - 0.3, t_antesT, z0=1.55, z1=1.70, c0=(0.44, 0.64), c1=(0.44, 0.62), par=(30, 8))
snd(t_corre, "pasos", 0.5, dur=2.0)
wow(t_papi, "luz_sagrada", 0.35)


@toma(t_corre - 0.3, ("latigo", 0.4))
def te6(lz, t):
    abrazo = t >= t_extr - 0.3
    pl = J6 if abrazo else J5
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.83, 0.60, 50, inten=0.45, sem=205)
    calido = smooth(prog(t, t_papi, t_papi + 1.5)) if not abrazo else 1.0
    if not abrazo:
        fantasma(lz, pl, t, "reencuentro_hoja/05", 0.30, 0.92, 0.46, op=0.62)
        fantasma_ciclo(lz, pl, t, "pamela_corre", t_corre - 0.3, t_papi + 0.6, 0.72, 0.40, 0.92, 0.22)
        if t > t_papi + 0.6:
            fantasma(lz, pl, t, "pamela_hoja/02", 0.40, 0.92, 0.28, op=0.6, flip=True)
    else:
        X, Y, h = pl.en(t, 0.44, 0.94, 0.40)
        PF.brillo(lz, X, Y - 0.5 * h, 1.4 * h, color=(1.0, 0.85, 0.55), inten=0.35, t=t, sem=206)
        fantasma(lz, pl, t, "reencuentro_hoja/00", 0.44, 0.94, 0.40, op=0.7)
    if calido > 0:
        PF.brillo(lz, W * 0.40, H * 0.55, H * 0.6, color=(1.0, 0.8, 0.5), inten=0.15 * calido, t=t)
    niebla(lz, t, NIEBLA_AZUL[:1])


J7 = PF.Plano("cofre_detras_a", t_antesT - 0.3, _ESC[CI]["t0"], z0=1.04, z1=1.18, c0=(0.48, 0.60), c1=(0.56, 0.62), par=(30, 8))
snd(t_llave, "clink", 0.6)
wow(t_cofre + 1.6, "cofre", 0.9)
wow(t_gracias, "mision_completa", 0.9)


@toma(t_antesT - 0.3, ("fundido", 0.6))
def te8(lz, t):
    J7.fondo(lz, t)
    brillo_en(lz, J7, t, 0.20, 0.48, 50, inten=0.45, sem=207)
    fantasma(lz, J7, t, "reencuentro_hoja/04", 0.34, 0.90, 0.40, op=0.62)
    pega(lz, "utileria2/13", W * 0.36, H * 0.24, H * 0.16, t, t_llave - 0.1, rot=-20)
    abre = smooth(prog(t, t_cofre + 1.4, t_cofre + 2.2))
    X, Y, h = J7.en(t, 0.70, 0.86, 0.18)
    PF.brillo(lz, X, Y - 0.5 * h, 2.2 * h, color=(1.0, 0.85, 0.4), inten=0.15 + 0.5 * abre, t=t, sem=208)
    PF.actor(lz, "utileria2/14", X, Y, h, tono=ALBA, sy=1.0 + 0.04 * abre)
    if abre > 0:
        PF.chispas(lz, t, X, Y - 0.7 * h, s=1.4 * abre, n=10, sem=13)
    quieto(lz, J7, t, "aventurero_hoja/04", 0.54, 0.96, 0.52, tono=ALBA)
    aviso_oro(lz, t, "Misión completada: Tesoros ocultos", t_gracias, _ESC[CI]["t0"] - 0.6)
    niebla(lz, t, NIEBLA_AZUL[:1])


# ================================================================== CIERRE (730,9 - 809,1)
t_asiZ, t_creer = F(CI, 0), Ts(CI, "creer", 0)
t_nada, t_muerta = F(CI, 1), Ts(CI, "muerta", 1)
t_familia, t_carlinZ, t_jessicaZ = F(CI, 2), Ts(CI, "carlin", 2), Ts(CI, "jessica", 2)
t_reenc, t_dosF = F(CI, 3), Ts(CI, "fantasmas", 3)
t_detalle = F(CI, 4)
t_cata, t_borro, t_classic, t_forever = F(CI, 5), Ts(CI, "borró", 5), Ts(CI, "classic", 5), Ts(CI, "forever", 5)
t_salga, t_nov, t_misma, t_munZ = F(CI, 6), Ts(CI, "noviembre", 6), Ts(CI, "casa", 6), Ts(CI, "muñeca", 6)
t_proximo, t_holaZ = F(CI, 7), F(CI, 8)
t_ctaF, t_compF, t_comentF = F(CI, 9), Ts(CI, "compártela", 9), Ts(CI, "comentarios", 9)
t_leo, t_pamZ = F(CI, 10), Ts(CI, "pamela", 10)

Z1 = PF.Plano("lago_darrowmere_noche_a", t_asiZ - 0.3, t_nada, z0=1.30, z1=1.04, c0=(0.52, 0.62), c1=(0.52, 0.55), par=(34, 8))
wow(t_asiZ, "amb_peste_noche", 0.4, dur=t_detalle - t_asiZ + 1.0, fade=2.0)
PUNTOS_LAGO = [(float(x), float(y), float(f)) for x, y, f in np.random.default_rng(8).uniform((0.45, 0.42, 0), (0.95, 0.56, 1), (50, 3))]


@toma(t_asiZ - 0.3, ("fundido", 1.0))
def z1(lz, t):
    Z1.fondo(lz, t)
    brillo_en(lz, Z1, t, 0.65, 0.12, 120, color=(0.75, 0.85, 1.0), inten=0.25, sem=210)
    PF.destellos(lz, t, [(*Z1.P(t, x, y)[:2], f) for x, y, f in PUNTOS_LAGO], s=0.8, color=(0.85, 0.92, 1.0))
    u = clamp01((t - t_asiZ + 0.3) / (t_nada - t_asiZ + 0.3))
    fantasma(lz, Z1, t, "reencuentro_hoja/01", lerp(0.46, 0.56, u), lerp(0.88, 0.70, u), lerp(0.40, 0.24, u), op=0.62)
    niebla(lz, t, NIEBLA_AZUL)


Z2 = PF.Plano("ruinas_camino_b", t_nada - 0.3, t_familia, z0=1.04, z1=1.16, c0=(0.50, 0.58), c1=(0.56, 0.56), par=(34, 8))
V_Z2 = [(t_nada, 7.0, 0.16, 0.10, 56, 1, 0.4), (t_nada + 0.5, 7.5, 0.22, 0.14, 44, 1, 1.4)]
wow(t_muerta - 0.4, "necrofago", 0.4)


@toma(t_nada - 0.3, ("fundido", 0.6))
def z2(lz, t):
    Z2.fondo(lz, t)
    brillo_en(lz, Z2, t, 0.27, 0.43, 40, inten=0.4, sem=211)
    cuervos(lz, t, V_Z2, tono=NUBLADO)
    paseo(lz, Z2, t, "plaga_hoja/02", t_nada - 0.3, t_familia, 0.70, 0.52, 0.80, 0.28, tono=NOCHE_PESTE, pasos=1.1)
    paseo(lz, Z2, t, "necrofago_corre/ciclo_00", t_nada + 1.0, t_familia, 0.95, 0.80, 0.92, 0.36, tono=NOCHE_PESTE, pasos=0.9)
    rot_(lz, "SIGUE EN RUINAS", W * 0.5, H * 0.12, 56, t, t_nada + 2.0)
    niebla(lz, t, NIEBLA_VERDE[:2])


Z3 = PF.Plano("pergamino_mesa_b", t_familia - 0.3, t_reenc, z0=1.06, z1=1.12, c0=(0.48, 0.52), c1=(0.48, 0.52), par=(0, 0))
for tt in (t_familia, t_familia + 0.15, t_familia + 0.3, t_familia + 0.45, t_familia + 0.6):
    snd(tt, "papel", 0.4)
snd(t_carlinZ, "pop", 0.6)
snd(t_jessicaZ, "pop", 0.6)
ARBOL_T = {"joseph": t_familia, "marlene_cos": t_familia + 0.15, "carlin": t_familia + 0.3, "jessica": t_familia + 0.45,
           "pamela": t_familia + 0.6}
MUERTOS = {q: (FANTASMA, t_familia + 1.4) for q in ("joseph", "marlene_cos", "pamela")}


@toma(t_familia - 0.3, ("desenfoque", 0.5))
def z3(lz, t):
    Z3.fondo(lz, t)
    brillo_en(lz, Z3, t, 0.92, 0.10, 110, inten=0.5, sem=212)
    arbol(lz, Z3, t, ARBOL_T, tonos=MUERTOS)
    for q, tq in (("carlin", t_carlinZ), ("jessica", t_jessicaZ)):
        if t >= tq:
            X, Y, s = Z3.P(t, ARBOL[q][0], ARBOL[q][1])
            PF.brillo(lz, X, Y, 0.16 * H, color=(1.0, 0.85, 0.4), inten=0.45 * PF.entra(t, tq, 0.4), t=t, sem=90)
    rot_(lz, "SOLO SOBREVIVIERON DOS", W * 0.5, H * 0.08, 54, t, t_familia + 0.3)


Z4 = PF.Plano("lago_darrowmere_noche_b", t_reenc - 0.3, t_detalle, z0=1.10, z1=1.26, c0=(0.62, 0.55), c1=(0.66, 0.56), par=(34, 8))


@toma(t_reenc - 0.3, ("fundido", 0.8))
def z4(lz, t):
    Z4.fondo(lz, t)
    brillo_en(lz, Z4, t, 0.66, 0.20, 140, color=(0.75, 0.85, 1.0), inten=0.28, sem=213)
    X, Y, h = Z4.en(t, 0.70, 0.62, 0.30)
    PF.brillo(lz, X, Y - 0.5 * h, 1.3 * h, color=(0.55, 0.9, 1.0), inten=0.3, t=t, sem=214)
    fantasma(lz, Z4, t, "reencuentro_hoja/00", 0.70, 0.62, 0.30, op=0.66)
    rot_(lz, "DOS FANTASMAS", W * 0.30, H * 0.80, 56, t, t_dosF)
    niebla(lz, t, NIEBLA_AZUL)


Z5 = PF.Plano("posada_camino_b", t_detalle - 0.3, t_cata, z0=1.30, z1=1.45, c0=(0.70, 0.45), c1=(0.72, 0.44), par=(30, 8))
wow(t_detalle + 1.8, "vela", 0.6)
snd(t_detalle + 2.0, "golpe_grave", 0.5)


@toma(t_detalle - 0.3, ("negro", 0.8))
def z5(lz, t):
    Z5.fondo(lz, t)
    apaga = 1.0 - smooth(prog(t, t_detalle + 1.8, t_detalle + 2.3))
    brillo_en(lz, Z5, t, 0.73, 0.40, 80, inten=0.6 * apaga, sem=215)
    oscurece(lz, 0.35 * (1 - apaga))
    niebla(lz, t, NIEBLA_VERDE[:2])


Z6 = PF.Plano("peste_este_b", t_cata - 0.3, t_salga, z0=1.04, z1=1.14, c0=(0.50, 0.55), c1=(0.54, 0.55), par=(34, 8))
snd(t_borro, "golpe_grave", 0.7)
wow(t_classic, "mision_acepta", 0.6)
wow(t_forever, "luz_sagrada", 0.5)


@toma(t_cata - 0.3, ("latigo", 0.4))
def z6(lz, t):
    Z6.fondo(lz, t)
    oscurece(lz, 0.25)
    brillo_en(lz, Z6, t, 0.68, 0.30, 40, inten=0.35, sem=216)
    ventana_mision(lz, t, W * 0.36, H * 0.52, H * 0.60, t_cata + 0.2)
    if t >= t_borro - 0.1:        # tachada en Cataclysm…
        k = PF.entra(t, t_borro - 0.1, 0.3) * (1 - smooth(prog(t, t_classic - 0.2, t_classic + 0.4)))
        if k > 0.01:
            for (a, b) in (((0.20, 0.30), (0.52, 0.74)), ((0.20, 0.74), (0.52, 0.30))):
                D.linea_aa(lz, [(W * a[0], H * a[1]), (W * lerp(a[0], b[0], min(1, k * 1.5)), H * lerp(a[1], b[1], min(1, k * 1.5)))],
                           (0.75, 0.05, 0.05), grosor=14.0, op=k)
    rot_(lz, "CATACLYSM: SE BORRÓ", W * 0.76, H * 0.30, 46, t, t_borro, t_classic - 0.2)
    if t >= t_classic:
        PF.brillo(lz, W * 0.36, H * 0.52, H * 0.5, color=(1.0, 0.85, 0.4), inten=0.35 * (1 - clamp01((t - t_classic) / 1.5)), t=t)
    rot_(lz, "SIGUE EN CLASSIC", W * 0.76, H * 0.44, 50, t, t_classic, rot=2)
    rot_(lz, "Y EN WOW FOREVER", W * 0.76, H * 0.58, 50, t, t_forever, rot=-2)


Z7 = PF.Plano("casa_pamela_vela_a", t_salga - 0.3, t_proximo, z0=1.04, z1=1.40, c0=(0.55, 0.55), c1=(0.72, 0.58), par=(30, 8))
wow(t_salga, "mundo_espiritus", 0.35, dur=t_ctaF - t_salga, fade=1.5)


@toma(t_salga - 0.3, ("fundido", 0.6))
def z7(lz, t):
    Z7.fondo(lz, t)
    brillo_en(lz, Z7, t, 0.76, 0.58, 60, inten=0.5 + 0.08 * math.sin(t * 11), sem=217)
    fantasma(lz, Z7, t, "pamela_hoja/04", 0.70, 0.66, 0.20, t_in=t_misma - 0.3, op=0.45)
    rot_(lz, "4 DE NOVIEMBRE", W * 0.28, H * 0.14, 62, t, t_nov - 0.2)
    pega(lz, "iconos/muneca", W * 0.24, H * 0.60, H * 0.20, t, t_munZ - 0.1, rot=-6)
    rot_(lz, "LA MISMA MUÑECA ROTA", W * 0.24, H * 0.78, 40, t, t_munZ + 0.1)
    niebla(lz, t, NIEBLA_AZUL)


Z8 = PF.Plano("casa_pamela_vela_b", t_proximo - 0.3, t_holaZ, z0=1.04, z1=1.10, c0=(0.50, 0.58), c1=(0.52, 0.58), par=(30, 8))
Z9 = PF.Plano("casa_pamela_vela_b", t_holaZ - 0.3, t_ctaF, z0=1.50, z1=1.58, c0=(0.62, 0.60), c1=(0.62, 0.60), par=(26, 6))
snd(t_proximo, "galope", 0.6, dur=3.5)
wow(t_holaZ + 1.6, "mision_acepta", 0.7)


@toma(t_proximo - 0.3, ("fundido", 0.6))
def z8(lz, t):
    cerca = t >= t_holaZ - 0.3
    pl = Z9 if cerca else Z8
    pl.fondo(lz, t)
    brillo_en(lz, pl, t, 0.65, 0.52, 50, inten=0.5, sem=218)
    if not cerca:
        anda(lz, pl, t, "jinete_galope", t_proximo - 0.3, t_holaZ + 0.3, -0.15, 0.62, 0.92, 0.26, paso=1.7, tono=NOCHE,
             desde_antes=True)
        rot_(lz, "COMO SI FUERA EL PRIMERO", W * 0.5, H * 0.12, 50, t, t_proximo + 1.2)
    else:
        fantasma(lz, pl, t, "pamela_hoja/02", 0.56, 0.86, 0.30, op=0.64)
        X, Y, h = pl.en(t, 0.56, 0.86, 0.30)
        exclamacion(lz, X, Y - h * 1.12, 110, t, t_holaZ - 0.1)
        ventana_mision(lz, t, W * 0.76, H * 0.50, H * 0.56, t_holaZ + 0.5, t_acepta=t_holaZ + 1.6)
    niebla(lz, t, NIEBLA_AZUL)


Z10 = PF.Plano("villa_lago_b", t_ctaF - 0.3, TOTAL, z0=1.04, z1=1.18, c0=(0.50, 0.58), c1=(0.50, 0.55), par=(30, 8))
snd(t_ctaF, "amanecer", 0.5, dur=3.0)
snd(t_ctaF + 0.8, "pio", 0.4)
snd(t_compF, "pop", 0.5)
snd(t_comentF, "pop", 0.5)
wow(t_pamZ, "fantasma", 0.5)
wow(t_pamZ + 0.4, "amb_peste_noche", 0.4, dur=TOTAL - t_pamZ, fade=1.0)
V_Z10 = [(t_ctaF, 9.0, 0.10, 0.06, 40, 1, 0.3), (t_ctaF + 1.5, 9.5, 0.14, 0.10, 32, 1, 1.2)]


@toma(t_ctaF - 0.3, ("destello", 1.0))
def z10(lz, t):
    Z10.fondo(lz, t)
    frio = smooth(prog(t, t_pamZ - 0.3, t_pamZ + 1.5))
    humo_en(lz, Z10, t, 0.20, 0.30, s=0.8, color=(0.92, 0.92, 0.94), op=0.18 * (1 - frio), sem=14)
    cuervos(lz, t, V_Z10, tono=(0.8, 0.75, 0.7))
    paseo(lz, Z10, t, "aldeanos_hoja/01", t_ctaF, t_pamZ, 0.80, 0.62, 0.82, 0.28, tono=CALIDO, pasos=1.6, op=1 - frio)
    if frio < 1:
        X, Y, h = Z10.en(t, 0.40, 0.92, 0.36)
        PF.actor(lz, "pamela_hoja/00", X, Y, h, tono=CALIDO, op=1 - frio, rot=2 * math.sin(t * 2.3), sy=PF.respira(t))
    tinte(lz, (0.45, 0.60, 0.85), 0.75 * frio)
    oscurece(lz, 0.35 * frio)
    if frio > 0:
        fantasma(lz, Z10, t, "pamela_hoja/02", 0.40, 0.92, 0.36, t_in=t_pamZ - 0.2, op=0.66)
    rot_(lz, "COMPÁRTELA", W * 0.28, H * 0.14, 62, t, t_compF - 0.1, t_pamZ - 0.4)
    rot_(lz, "¿QUÉ HISTORIA DE AZEROTH QUIERES VER?", W * 0.56, H * 0.84, 46, t, t_comentF - 0.1, t_pamZ - 0.4)
    rot_(lz, "TE ESTÁ ESPERANDO", W * 0.68, H * 0.16, 58, t, t_pamZ + 0.8)


# ------------------------------------------------------------------ composición
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
    img = PF.acabado(img, t, vineta=0.48, calido=0.0)
    img = img * smooth(prog(t, 0.0, 0.8)) * (1.0 - smooth(prog(t, TOTAL - 1.4, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SFX:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
