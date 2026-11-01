# -*- coding: utf-8 -*-
"""La Crematoria (Gaia Eterna) — pegatina Flow en clave de terror y heroísmo (nucleo/pegaflow.py, docs/estilo_pegatina_flow.md § 8).
MOTOR DE TOMAS POR DATOS: el plan vive en `plan.py` (una toma por frase o grupo de frases: escenario de Flow con cámara y parallax,
personajes recortados de las hojas, ciclos, fantasmas, ambiente, pegatinas REALES del juego, iconos, rótulos, mapas reales con ruta
y SFX del juego). Aquí solo se dibuja. Cuando habla un personaje (guion.PERSONAJE_POR_FRASE) sale su PLACA abajo a la izquierda
(medallón real + nombre en oro de WoW) para que se sepa quién habla. SFX del juego en `JUEGO` (→ `_sfx_juego.py` → audio/fx.wav)."""
import functools
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

import pegaflow as PF
import docu as D
import mg_mapa as MP
import guion
from escena_base import Escena, TL
from motor import W, H, clamp01, lerp, prog, smooth

TOTAL = TL["total"]
FR = {f["key"]: f for e in TL["escenas"] for f in e["frases"]}
ESC = {e["id"]: e for e in TL["escenas"]}

# ------------------------------------------------------------------ luces
NOCHE = (0.62, 0.70, 0.86)
PESTE = (0.62, 0.78, 0.70)
VELA = (1.0, 0.84, 0.66)
CALIDO = (1.10, 1.0, 0.84)
NUBLADO = (0.86, 0.90, 0.92)
FUEGO = (1.06, 0.82, 0.64)
FRIO = (0.70, 0.82, 1.02)
ROJO = (1.04, 0.76, 0.72)
DORADO = (1.10, 1.0, 0.80)
LUZ = {"noche": NOCHE, "peste": PESTE, "vela": VELA, "calido": CALIDO, "nublado": NUBLADO, "fuego": FUEGO, "frio": FRIO,
       "rojo": ROJO, "dorado": DORADO, None: None}
FANTASMA = (0.55, 0.98, 1.06)

ALIAS = {"AL": "h01_alexandros_hoja", "AD": "h02_alexandros_dk", "RE": "h03_renault_hoja", "RS": "h04_renault_escarlata",
         "DA": "h05_darion_hoja", "DD": "h06_darion_dk", "NI": "h07_darion_nino", "TJ": "h08_tirion_joven",
         "TV": "h09_tirion_viejo", "TH": "h10_tirion_highlord", "TA": "h11_taelan_hoja", "FA": "h12_familias_hoja",
         "EI": "h13_eitrigg_hoja", "IS": "h14_isillien_hoja", "VI": "h15_villanos_hoja", "CO": "h16_consejo_hoja",
         "MA": "h17_magni_hoja", "DK": "h18_dk_hoja", "CR": "h19_cruzados_hoja", "DF": "h20_defensores_hoja",
         "PL": "h21_plaga_hoja", "UT": "h28_utileria", "U2": "h29_utileria2", "FX": "h30_fx_hoja"}
CICLOS = {"NEC": "h22_necrofago_corre", "ESQ": "h23_esqueleto_camina", "MIR": "h24_mirador_galope",
          "CAB": "h25_caballo_muerte_galope", "GAR": "h26_gargola_aleteo", "TGA": "h27_taelan_galope"}
# a dónde MIRA cada pieza en su hoja (1 = derecha, -1 = izquierda): para voltearla según hacia dónde camina
MIRA = {"RE5": 1, "DA2": 1, "TJ4": 1, "TV5": 1, "AL4": 1}


def pieza(cod):
    """«AL3» → h01_alexandros_hoja/03 · «UT12» → h28_utileria/12 · nombre completo tal cual."""
    if "/" in cod:
        return cod
    return f"{ALIAS[cod[:2]]}/{int(cod[2:]):02d}"


# ------------------------------------------------------------------ SFX del juego
JUEGO = []      # (t, nombre, vol, dur o None, fundido)


def wow(t, n, v=1.0, dur=None, fade=0.4):
    JUEGO.append((t, n, v, dur, fade))


# ------------------------------------------------------------------ tiempos
def tk(key, pref=None, fin=False):
    """Inicio (o fin) de la frase `key`, o de la primera palabra que empieza por `pref` en ella."""
    f = FR[key]
    if pref is None:
        return f["t1"] if fin else f["t0"]
    p = pref.lower()
    for w in f["words"]:
        if w["w"].lower().strip(".,;:¡!¿?«»\"'…").startswith(p):
            return w["e"] if fin else w["s"]
    return f["t0"]


# ------------------------------------------------------------------ ayudantes de dibujo
def tinte(lz, color, k):
    if k <= 0.003:
        return
    g = lz.mean(2, keepdims=True)
    lz[:] = lz * (1 - k) + (0.55 * lz + 0.45 * g) * np.float32(color) * k


def pega(lz, nombre, X, Y, hpx, t, t_in, t_out=None, rot=0.0, tono=None, flip=False, op=1.0):
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.45)
    o = op if t_out is None else op * (1.0 - smooth(prog(t, t_out, t_out + 0.35)))
    if o <= 0.01:
        return
    PF.actor(lz, nombre, X, Y + 4 * math.sin(1.3 * t + t_in), hpx * (0.6 + 0.4 * u), rot=rot + (1 - u) * 10 + 0.8 * math.sin(1.1 * t),
             op=o * clamp01(u * 4), ancla=(0.5, 0.5), suelo=0, tono=tono, flip=flip)


@functools.lru_cache(maxsize=64)
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


def texto_oro(lz, txt, X, Y, px, op=1.0, izq=False):
    if not txt:
        return
    spr = _oro(txt, px)
    x = X if izq else X - spr.w / 2
    D.pegar(lz, spr, np.array([[1, 0, x], [0, 1, Y - spr.h / 2], [0, 0, 1]], np.float64), op)


def niebla(lz, t, pz, n=3, y=0.88, hpx=340, op=0.45, vel=18):
    for k in range(n):
        ancho = hpx * 2.4
        span = W + 2 * ancho
        x = ((k / n) * span + t * vel * (1 if k % 2 == 0 else -0.7)) % span - ancho
        PF.actor(lz, pz, x, (y + 0.06 * (k % 2)) * H + 10 * math.sin(0.4 * t + k), hpx * (1 + 0.2 * k), ancla=(0.5, 0.5), suelo=0,
                 sombra=False, op=op * (0.85 + 0.15 * math.sin(0.7 * t + k)), flip=(k % 2 == 1))


@functools.lru_cache(maxsize=4)
def _gotas(n, sem):
    r = np.random.default_rng(sem)
    return r.uniform(0, 1, n), r.uniform(0, 1, n), r.uniform(0.6, 1.4, n)


def lluvia(lz, t, color=(0.75, 0.78, 0.85), n=420, op=0.35, vel=1.6, largo=34, sem=1):
    xs, ys, vs = _gotas(n, sem)
    capa = np.zeros((H, W), np.float32)
    for x, y, v in zip(xs, ys, vs):
        yy = ((y + t * vel * v) % 1.0) * (H + 80) - 40
        xx = x * W + (yy * 0.12)
        cv2.line(capa, (int(xx), int(yy)), (int(xx + largo * 0.12 * v), int(yy + largo * v)), 1.0, 1, cv2.LINE_AA)
    lz[:] = lz * (1 - capa[..., None] * op) + capa[..., None] * op * np.float32(color)


def nieve(lz, t, n=240, op=0.7):
    xs, ys, vs = _gotas(n, 9)
    for x, y, v in zip(xs, ys, vs):
        yy = ((y + t * 0.07 * v) % 1.0) * H
        xx = (x * W + 30 * math.sin(t * 0.8 + y * 20)) % W
        PF._blob(lz, xx, yy, 3.0 * v, (0.95, 0.97, 1.0), op)


def brasas(lz, t, n=40, color=(1.0, 0.55, 0.15), sem=4):
    xs, ys, vs = _gotas(n, sem)
    for x, y, v in zip(xs, ys, vs):
        yy = H - ((y + t * 0.09 * v) % 1.0) * H
        xx = (x * W + 40 * math.sin(t * 1.3 + y * 30)) % W
        PF._blob(lz, xx, yy, 4.0 * v, color, 0.85, aditivo=True)


def ceniza(lz, t, n=60):
    xs, ys, vs = _gotas(n, 6)
    for x, y, v in zip(xs, ys, vs):
        yy = ((y + t * 0.05 * v) % 1.0) * H
        xx = (x * W + t * 25 * v) % W
        PF._blob(lz, xx, yy, 3.0 * v, (0.72, 0.70, 0.68), 0.6)


def columnas_luz(lz, t, t0, n=8):
    """Rayos de Luz sagrada que suben del suelo: columnas aditivas con perfil gaussiano, que laten y se desvanecen hacia arriba."""
    u = smooth(prog(t, t0, t0 + 1.2))
    if u <= 0:
        return
    xs = np.arange(W, dtype=np.float32)
    perfil = np.zeros(W, np.float32)
    for k in range(n):
        x0 = W * (0.06 + 0.88 * k / (n - 1)) + 50 * math.sin(k * 3.1 + 0.3 * t)
        ancho = 18 + 14 * (0.5 + 0.5 * math.sin(t * 2.3 + k * 1.9))
        perfil += np.exp(-((xs - x0) / ancho) ** 2) * (0.7 + 0.3 * math.sin(t * 3.1 + k))
    alto = np.linspace(0, 1, H, dtype=np.float32) ** 1.6
    capa = alto[:, None] * perfil[None, :] * (0.55 * u)
    lz += capa[..., None] * np.float32((1.0, 0.82, 0.42))
    PF.brillo(lz, W / 2, H * 0.85, W * 0.5, color=(1.0, 0.85, 0.4), inten=0.22 * u, t=t)


def gargolas(lz, t, t0, n=3):
    nc = PF.ciclo_n(CICLOS["GAR"])
    for k in range(n):
        dur = 9.0 + 2 * k
        u = ((t - t0) / dur + k * 0.37) % 1.0
        x = lerp(-0.1, 1.1, u) * W if k % 2 == 0 else lerp(1.1, -0.1, u) * W
        y = H * (0.12 + 0.08 * k) + 14 * math.sin(t * 2 + k)
        i = int(t * 8 + k * 3) % nc
        PF.actor(lz, f"{CICLOS['GAR']}/ciclo_{i:02d}", x, y, 90 - 18 * k, flip=(k % 2 == 1), ancla=(0.5, 0.5), suelo=0,
                 tono=(0.55, 0.62, 0.70), sombra=False)


AMBIENTES = {
    "lluvia": lambda lz, t, s: lluvia(lz, t),
    "lluvia_sangre": lambda lz, t, s: lluvia(lz, t, color=(0.75, 0.10, 0.08), op=0.55, n=520),
    "nieve": lambda lz, t, s: nieve(lz, t),
    "niebla_verde": lambda lz, t, s: niebla(lz, t, "h30_fx_hoja/03", op=0.42),
    "niebla_gris": lambda lz, t, s: niebla(lz, t, "h30_fx_hoja/04", op=0.35, hpx=300),
    "sombra": lambda lz, t, s: niebla(lz, t, "h30_fx_hoja/07", op=0.38, y=0.80, hpx=380, vel=12),
    "brasas": lambda lz, t, s: brasas(lz, t),
    "chispas_verdes": lambda lz, t, s: brasas(lz, t, n=30, color=(0.3, 1.0, 0.4), sem=8),
    "ceniza": lambda lz, t, s: ceniza(lz, t),
    "gargolas": lambda lz, t, s: gargolas(lz, t, s["t0"]),
    "columnas": lambda lz, t, s: columnas_luz(lz, t, s["t0"] + 0.4),
    "oscuro": lambda lz, t, s: lz.__imul__(np.float32(0.72)),
}


# ------------------------------------------------------------------ actores
def dibuja_actor(lz, pl, t, a, s, luz):
    """a = (cod, x, y, frac[, opts]) en coordenadas del ESCENARIO. opts: flip, x1 (camina hasta x1), y1, ciclo (anda con un
    ciclo de CICLOS), f (fantasma), in/out (segundos desde el inicio de la toma), op, rot, luz (otra luz), capa."""
    cod, x, y, frac = a[:4]
    o = a[4] if len(a) > 4 else {}
    t0, t1 = s["t0"], s["t1"]
    t_in = t0 + o["in"] if "in" in o else None
    t_out = t0 + o["out"] if "out" in o else None
    if t_in is not None and t < t_in:
        return
    op = o.get("op", 1.0)
    if t_out is not None:
        op *= 1.0 - smooth(prog(t, t_out, t_out + 0.4))
        if op <= 0.01:
            return
    tono = LUZ.get(o["luz"]) if "luz" in o else luz
    capa = o.get("capa", 1.0)
    ta, tb = (t_in or t0), min(t1, (t_out or t1))
    if "x1" in o:
        u = smooth(clamp01((t - ta) / max(tb - ta, 1e-3))) if o.get("suave") else clamp01((t - ta) / max(tb - ta, 1e-3))
        xx, yy = lerp(x, o["x1"], u), lerp(y, o.get("y1", y), u)
    else:
        xx, yy, u = x, y, 0.0
    X, Y, h = pl.en(t, xx, yy, frac, capa)
    flip = o.get("flip", False)
    if cod in CICLOS:                                           # ciclo (correr, caminar, galopar, aletear)
        nom = CICLOS[cod]
        n = PF.ciclo_n(nom)
        if "x1" in o:
            flip = o["x1"] < x
            dist = abs(xx - x) * pl.ancho_mundo(t)
            i = PF.cuadro_ciclo(dist, o.get("paso", 0.95) * h, n)
        else:
            i = int(t * o.get("fps", 9)) % n
        PF.actor(lz, f"{nom}/ciclo_{i:02d}", X, Y, h * 1.25, flip=flip, tono=tono, op=op)
        return
    nom = pieza(cod)
    if "x1" in o and cod in MIRA:
        flip = (o["x1"] - x) * MIRA[cod] < 0
    if o.get("f"):                                              # fantasma: la misma pieza teñida, translúcida, con halo y temblor
        a_ = smooth(prog(t, ta, ta + 1.1)) if t_in is not None else 1.0
        X += 3.0 * math.sin(t * 13.1) + 2.0 * math.sin(t * 7.3)
        Y += -6.0 * (0.5 + 0.5 * math.sin(t * 1.3)) - 4.0
        fl = 0.86 + 0.14 * math.sin(t * 17.0) * math.sin(t * 3.1)
        PF.brillo(lz, X, Y - 0.5 * h, 1.15 * h, color=(0.35, 0.85, 0.95), inten=0.26 * a_ * op, t=t, sem=7)
        PF.actor(lz, nom, X + 6, Y - 3, h * 1.03, flip=flip, op=0.22 * a_ * fl * op, tono=FANTASMA, suelo=0, sombra=False)
        PF.actor(lz, nom, X, Y, h, flip=flip, op=0.62 * a_ * fl * op, tono=FANTASMA, suelo=0, sombra=False,
                 sy=PF.respira(t, a=0.02))
        return
    ent = PF.entra(t, t_in, 0.4) if t_in is not None else 1.0
    mov = "x1" in o and ta < t < tb
    ph = (t - ta) * 2.2 * math.pi
    bote = abs(math.sin(ph)) * 0.03 * h if mov else 0.0
    rot = o.get("rot", 0.0) + (3.0 * math.sin(ph) if mov else 0.0) + (1 - ent) * 8
    PF.actor(lz, nom, X, Y - bote, h * (0.6 + 0.4 * ent), flip=flip, op=op * clamp01(ent * 4), tono=tono, rot=rot,
             sy=PF.respira(t, fase=x * 7))


# ------------------------------------------------------------------ placa de quien habla, reales, iconos, rótulos
NOMBRES = {"alexandros": "Alexandros Mograine", "tirion": "Tirion Vadín", "renault": "Renault Mograine",
           "darion": "Darion Mograine", "taelan": "Taelan Vadín", "isillien": "Gran Inquisidor Isillien",
           "kelthuzad": "Kel'Thuzad", "rey_exanime": "El Rey Exánime", "eitrigg": "Eitrigg"}


def placa(lz, t, per, t0, t1):
    if not (t0 - 0.05 <= t <= t1 + 0.6):
        return
    u = PF.entra(t, t0, 0.35)
    o = clamp01(u * 3) * (1.0 - smooth(prog(t, t1 + 0.1, t1 + 0.5)))
    med = f"medallon/{per}" if os.path.exists(f"piezas/medallon/{per}.png") else f"reales/{per}"
    X, Y = W * 0.075, H * 0.86
    PF.brillo(lz, X, Y, 150, color=(1.0, 0.82, 0.35), inten=0.18 * o, t=t)
    PF.actor(lz, med, X, Y, 150 * (0.7 + 0.3 * u), op=o, ancla=(0.5, 0.5), suelo=0)
    texto_oro(lz, NOMBRES[per], X + 92, Y, 40, op=o, izq=True)


def real(lz, t, slug, t_in, t_out, lado="der", alto=0.42, x=None, y=0.42, rot=None, nombre=None):
    """Foto real del juego en marco de papel; x, y en fracciones de pantalla (por defecto a un lado)."""
    X = W * (x if x is not None else (0.80 if lado == "der" else 0.20))
    rot = rot if rot is not None else (-4.0 if lado == "der" else 4.0)
    pega(lz, f"reales/{slug}", X, H * y, H * alto, t, t_in, t_out, rot=rot)
    texto_oro(lz, NOMBRE_REAL.get(slug, "") if nombre is None else nombre, X, H * y + H * alto * 0.56, 34, op=clamp01((t - t_in - 0.3) * 3)
              * (1 - smooth(prog(t, t_out, t_out + 0.35))))


# ------------------------------------------------------------------ clips REALES del juego (yt-dlp, ≤ 8 s, en clips/<nombre>.mp4)
# nombre → (rótulo, crédito del canal de YouTube). Fuentes: medios/clips/creditos.txt y medios/costasur/ (2Ya2f-WKBr4).
CLIPS = {"posada_fuera": ("La posada de Costasur", "Wowprecatarchive"),
         "posada_chimenea": ("La posada, por dentro", "Wowprecatarchive"),
         "posada_escalera": ("La escalera de la posada", "Wowprecatarchive"),
         "gran_forja": ("La Gran Forja de Forjaz", "Hazin221"),
         "vega_amparo": ("Vega del Amparo", "TheWarcraftAtlas"),
         "stratholme": ("Stratholme", "Thraex")}
_CAPS = {}


def _cuadro_clip(nombre, tt):
    """Cuadro RGB del clip en el segundo tt (se queda en el último cuadro al acabarse); lectura secuencial cacheada por proceso."""
    c = _CAPS.get(nombre)
    if c is None:
        cap = cv2.VideoCapture(f"clips/{nombre}.mp4")
        c = _CAPS[nombre] = [cap, max(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))), cap.get(cv2.CAP_PROP_FPS) or 30.0, -2, None]
    cap, n, fps, pos, ult = c
    i = min(n - 1, max(0, int(tt * fps)))
    if i == pos and ult is not None:
        return ult
    if i != pos + 1:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ok, f = cap.read()
    if not ok:
        return ult if ult is not None else np.zeros((720, 1280, 3), np.uint8)
    c[3], c[4] = i, cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
    return c[4]


def clip_real(lz, t, nombre, t_in, t_out, x=0.78, y=0.32, alto=0.36, rot=-3.0, vel=1.0):
    """Clip real del juego que se reproduce dentro de un marco de papel (como las fotos reales), con su rótulo y crédito."""
    if t < t_in or t > t_out + 0.4:
        return
    u = PF.entra(t, t_in, 0.45)
    o = clamp01(u * 4) * (1.0 - smooth(prog(t, t_out, t_out + 0.35)))
    if o <= 0.01:
        return
    f = _cuadro_clip(nombre, (t - t_in) * vel)
    hp = int(H * alto)
    wp = int(f.shape[1] * hp / f.shape[0])
    b = 12
    pap = np.empty((hp + 2 * b, wp + 2 * b, 3), np.uint8)
    pap[:] = (246, 236, 212)
    pap[b:b + hp, b:b + wp] = cv2.resize(f, (wp, hp), interpolation=cv2.INTER_AREA)
    spr = D.Sprite(pap)
    X, Y = W * x, H * y + 4 * math.sin(1.3 * t + t_in)
    D.pegar(lz, spr, D.poner(spr.w, spr.h, X, Y, s=0.6 + 0.4 * u, rz=rot + (1 - u) * 10 + 0.8 * math.sin(1.1 * t)), o)
    rot_txt, cred = CLIPS.get(nombre, ("", ""))
    ot = o * clamp01((t - t_in - 0.3) * 3)
    texto_oro(lz, rot_txt, X, Y + spr.h * 0.5 + 30, 34, op=ot)
    texto_oro(lz, f"en el juego · video: {cred} (YouTube)", X, Y + spr.h * 0.5 + 66, 20, op=ot * 0.9)


NOMBRE_REAL = {"alexandros": "Alto Señor Mograine", "alexandros_vivo": "Alexandros Mograine", "renault": "Comandante Mograine",
               "darion": "Darion Mograine", "tirion": "Tirion Vadín", "tirion_highlord": "Alto señor Tirion Vadín",
               "taelan": "Alto señor Taelan Vadín", "isillien": "Gran Inquisidor Isillien", "kelthuzad": "Kel'Thuzad",
               "rey_exanime": "El Rey Exánime", "eitrigg": "Eitrigg", "balnazzar": "Balnazzar",
               "dathrohan": "Gran Cruzado Dathrohan", "ribalimpia": "Alto Inquisidor Ribalimpia", "magni": "Magni Barbabronce",
               "zeliek": "Sir Zeliek", "korthazz": "Thane Korth'azz", "blaumeux": "Lady Blaumeux", "myranda": "Myranda la Fada",
               "renfray": "Artista Renfray", "koltira": "Koltira Tejemuerte", "thassarian": "Thassarian",
               "orbaz": "Orbaz Malasangre", "maxwell": "Lord Maxwell Neófitus", "barthilas": "Magistrado Barthilas",
               "uther": "Uther el Iluminado", "zabra": "Zabra Hexx", "naxxramas": "Naxxramas",
               "capilla": "Capilla de la Esperanza de la Luz", "monasterio": "Monasterio Escarlata", "stratholme": "Stratholme",
               "acherus": "Acherus: El Bastión de Ébano", "torre_taelan": "Torre de Taelan", "crematoria": "Crematoria",
               "crematoria_corrupta": "Crematoria corrupta", "agonia_escarcha": "Agonía de Escarcha",
               "alexandros_espiritu": "Espíritu de Mograine", "costasur": "Costasur", "costasur_ayuntamiento": "Costasur",
               "remol": "Rémol", "andorhal": "Andorhal", "vega_amparo": "Vega del Amparo", "mardenholde": "Fortaleza de Mardenholde",
               "gran_forja": "La Gran Forja", "forjaz": "Forjaz", "cumbre_roca_negra": "Cumbre de Roca Negra",
               "posada_fuera": "Posada de Costasur", "posada_dentro": "Posada de Costasur", "posada_chimenea": "Posada de Costasur",
               "posada_salon": "Posada de Costasur", "posada_cuarto": "Posada de Costasur", "posada_entrada": "Posada de Costasur",
               "kelthuzad_humano": "Kel'Thuzad", "renault_comandante": "Renault Mograine", "isillien_joven": "Isillien",
               "dathrohan_comic": "Saidan Dathrohan"}
NOMBRE_ICONO = {"crematoria": "Crematoria", "crematoria_corrupta": "Crematoria corrupta", "martillo_taelan": "Martillo de Taelan",
                "simbolo_honor": "Símbolo de Honor perdido", "cuadro": "Del amor y la familia", "obsequio": "Obsequio de Tirion",
                "fragmento_alma": "Fragmento de alma de Alexandros", "marca_fordring": "Marca de Fordring"}


def icono(lz, t, slug, t_in, t_out):
    X, Y = W * 0.80, H * 0.30
    pega(lz, f"iconos/{slug}", X, Y, 180, t, t_in, t_out, rot=0.0)
    o = clamp01((t - t_in - 0.25) * 3) * (1 - smooth(prog(t, t_out, t_out + 0.35)))
    if o > 0:
        texto_oro(lz, NOMBRE_ICONO.get(slug, slug), X, Y + 130, 40, op=o)


# ------------------------------------------------------------------ mapas reales con ruta
PUNTOS = json.load(open(os.path.join("mapas", "_puntos.json"), encoding="utf-8"))


def mapa_fn(archivo, lugares, titulo, sub, fotos=None, pasos=None, **kw):
    P = PUNTOS[archivo]
    pts = []
    for i, lg in enumerate(lugares):
        if i and pasos and i - 1 < len(pasos) and pasos[i - 1]:
            pts += [tuple(p) for p in P[pasos[i - 1]]]
        tipo = "inicio" if i == 0 and len(lugares) > 1 else ("meta" if i == len(lugares) - 1 else "paso")
        foto = (fotos or {}).get(lg)
        pts.append((P[lg][0], P[lg][1], lg, tipo, foto))
    return MP.mapa(os.path.join("mapas", archivo), pts, tema="wow", titulo=titulo, sub=sub, **kw)


def dibuja_mapa(lz, t, s):
    fn = s["mapa_fn"]
    o = fn(t - s["t0"], s["t1"] - s["t0"], [m - s["t0"] for m in s["marcas"]])
    a = o[..., 3:4].astype(np.float32) / 255.0
    rgb = o[..., 2::-1].astype(np.float32) / 255.0
    lz[:] = lz * (1 - a) + rgb * a


# ------------------------------------------------------------------ tomas
CAM = {"in": (1.0, 1.12, (0.5, 0.52), (0.5, 0.50)), "out": (1.14, 1.0, (0.5, 0.50), (0.5, 0.52)),
       "izq": (1.12, 1.14, (0.58, 0.5), (0.43, 0.5)), "der": (1.12, 1.14, (0.42, 0.5), (0.57, 0.5)),
       "arr": (1.14, 1.16, (0.5, 0.60), (0.5, 0.42)), "aba": (1.14, 1.16, (0.5, 0.42), (0.5, 0.58)),
       "lento": (1.04, 1.09, (0.5, 0.5), (0.5, 0.5)), "zoom": (1.0, 1.35, (0.5, 0.55), (0.5, 0.5))}

from plan import PLAN  # noqa: E402

TOMAS = []
for _i, _p in enumerate(PLAN):
    _s = dict(_p)
    _s["t0"] = ESC[_s["esc"]]["t0"] if _s["n"] == 0 else tk(f"{_s['esc']}_{_s['n']}") - 0.3
    TOMAS.append(_s)
TOMAS.sort(key=lambda s: s["t0"])
TOMAS[0]["t0"] = 0.0
for _i, _s in enumerate(TOMAS):
    _s["t1"] = TOMAS[_i + 1]["t0"] if _i + 1 < len(TOMAS) else TOTAL
    if "fondo" in _s:
        z0, z1, c0, c1 = CAM[_s.get("cam", "lento")]
        _s["pl"] = PF.Plano(_s["fondo"], _s["t0"], _s["t1"] + 0.6, z0, z1, c0, c1, semilla=_i)
    if "mapa" in _s:
        m = _s["mapa"]
        _s["mapa_fn"] = mapa_fn(*m[:4], fotos=m[4] if len(m) > 4 else None, pasos=m[5] if len(m) > 5 else None,
                                **(m[6] if len(m) > 6 else {}))
        _s["marcas"] = [tk(k, p) for k, p in _s.get("marcas", [])]
    _s["ent"] = _s.get("ent", ("negro", 1.0) if _s["n"] == 0 and _i else ("fundido", 0.5))
    for _snd in _s.get("sfx", []):                          # (nombre, (key, pref) | segundos desde t0, vol[, dur])
        n_, cuando, v_ = _snd[:3]
        tt = tk(*cuando) if isinstance(cuando, tuple) else _s["t0"] + cuando
        wow(tt, n_, v_, _snd[3] if len(_snd) > 3 else None)

# placas de quien habla
PLACAS = [(k, per, FR[k]["t0"], FR[k]["t1"]) for k, per in guion.PERSONAJE_POR_FRASE.items() if k in FR]


def dibuja_toma(lz, s, t):
    luz = LUZ.get(s.get("luz"))
    if "mapa" in s:
        lz[:] = 0.03
        dibuja_mapa(lz, t, s)
    else:
        pl = s["pl"]
        pl.fondo(lz, t)
        if luz is not None and s.get("luz_fondo"):
            lz *= np.float32(luz)
        for a in s.get("act", []):
            dibuja_actor(lz, pl, t, a, s, luz)
        for x, y, r, col in s.get("brillo", []):
            X, Y, sc = pl.P(t, x, y)
            PF.brillo(lz, X, Y, r * sc, color=col, inten=0.45, t=t)
    for amb in s.get("amb", []):
        AMBIENTES[amb](lz, t, s)
    if s.get("tinte"):
        tinte(lz, *s["tinte"])
    for r in s.get("real", []):                             # (slug, (key, pref) | None | s desde t0, lado[, {x, y, alto, rot, dur}])
        slug, cuando = r[0], r[1]
        op = dict(r[3]) if len(r) > 3 else {}
        ti = tk(*cuando) if isinstance(cuando, tuple) else s["t0"] + (0.4 if cuando is None else cuando)
        real(lz, t, slug, ti, min(ti + op.pop("dur", 4.2), s["t1"] - 0.3), r[2] if len(r) > 2 else "der", **op)
    for c in s.get("clip", []):                             # (nombre, (key, pref) | None | s desde t0[, {x, y, alto, rot, vel, dur}])
        nombre, cuando = c[0], c[1]
        op = dict(c[2]) if len(c) > 2 else {}
        ti = tk(*cuando) if isinstance(cuando, tuple) else s["t0"] + (0.4 if cuando is None else cuando)
        clip_real(lz, t, nombre, ti, min(ti + op.pop("dur", 6.5), s["t1"] - 0.3), **op)
    for ic in s.get("ico", []):
        slug, cuando = ic
        ti = tk(*cuando) if cuando else s["t0"] + 0.4
        icono(lz, t, slug, ti, min(ti + 4.5, s["t1"] - 0.3))
    for tx in s.get("txt", []):                             # (TEXTO, (key, pref) | None, y)
        txt, cuando = tx[0], tx[1]
        ti = tk(*cuando) if cuando else s["t0"] + 0.5
        PF.rotulo(lz, txt, W * 0.5, H * (tx[2] if len(tx) > 2 else 0.14), 58, t, ti, s["t1"] - 0.4, rot=-2.0)


def _cuadro(s, t):
    lz = np.zeros((H, W, 3), np.float32)
    dibuja_toma(lz, s, t)
    return lz


def render_mundo(t):
    i = 0
    for k, s in enumerate(TOMAS):
        if s["t0"] <= t:
            i = k
    s = TOMAS[i]
    img = _cuadro(s, t)
    tipo, dur = s["ent"]
    if i > 0 and t < s["t0"] + dur and tipo != "corte":
        img = D.mezcla_tomas(_cuadro(TOMAS[i - 1], t), img, (t - s["t0"]) / dur, tipo)
    for k, per, a, b in PLACAS:
        if a - 0.1 <= t <= b + 0.7:
            placa(img, t, per, a, b)
    img = PF.acabado(img, t, vineta=0.48, calido=0.0)
    img = img * smooth(prog(t, 0.0, 0.8)) * (1.0 - smooth(prog(t, TOTAL - 1.4, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
