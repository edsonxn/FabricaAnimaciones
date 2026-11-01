# -*- coding: utf-8 -*-
"""«No vuelve a pasar» — corto del taller «Bájate de la rueda» (3.º de secundaria, Jalpa, Zac.). Estilo PEGATINA FLOW
(nucleo/pegaflow.py): escenarios de Flow con cámara y parallax por profundidad; personajes, ciclos y utilería de las hojas de Flow
animados como pegatinas. Guion e intención de cada escena: PLAN_TALLER.md · número → pose de cada pieza: piezas/_mapa.md.
La violencia queda FUERA de cuadro (debajo de la mesa solo se ven piernas, un plato que se rompe y un niño tapándole las orejas a
su hermana). La rueda de la fortuna la arma el código: rueda de Flow sin góndolas + patas en A + góndolas que cuelgan y se mecen.
Los platos de barro de la pared (uno menos cada vuelta) los cuelga el código en los clavitos pintados.
Tramo 2 (21-oct-2026). Todo lo que lleva letras (el chat, los rótulos) lo dibuja el código: Flow no pone texto."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


def t0(eid):
    return _ESC[eid]["t0"]


def t1(eid):
    return _ESC[eid]["t1"]


# luz de cada lugar sobre las pegatinas (sin tono parecen pegadas encima)
FERIA_N = (0.74, 0.70, 0.94)
RUEDA_N = (0.96, 0.84, 0.82)      # la rueda iluminada por sus propios focos
TARDE = (1.06, 0.92, 0.80)
FOCO = (1.0, 0.86, 0.62)          # cocina de noche, un solo foco
BAJO = (0.78, 0.62, 0.52)         # debajo de la mesa
MANANA = (1.03, 1.0, 0.95)
JARDIN = (1.06, 0.90, 0.84)
ESCUELA = (1.0, 0.99, 0.96)
FRESCO = (0.96, 0.98, 1.03)
RECAMARA = (0.94, 0.80, 0.82)
PATIO = (0.84, 0.74, 0.80)
ALBA = (1.03, 0.93, 0.95)
OCASO = (1.05, 0.88, 0.86)
RECUERDO = (0.92, 0.82, 0.68)     # el recuerdo del papá de niño: sepia

AVES = [f"paloma_vuelo/{i:02d}" for i in range(6)]

SFX = []


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


# ------------------------------------------------------------------ ayudantes de la toma
MIRA = {"papa_camina": 1, "diego14_camina": 1, "lupe_camina": 1, "xime9_camina": 1, "fer_camina": 1, "paloma_vuelo": 1,
        "diego8_hoja/03": 1, "gente_hoja/06": 1, "gente_hoja/01": 1, "fer_hoja/04": 1}


def rumbo(pieza, x0, x1, flip):
    m = MIRA.get(pieza)
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, rot=0.0, suelo=0.30):
    """Personaje u objeto quieto que respira; si `t_in`, se pega con rebote en ese instante."""
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8, suelo=suelo)


def poses(lz, pl, t, cambios, x, y, frac, tono=None, fase=0.0, op=1.0):
    """Personaje en un sitio que cambia de pose: cambios = [(t_i, pieza, flip, escala)]; cada cambio entra con un rebote corto."""
    act = None
    for c in cambios:
        if c[0] <= t:
            act = c
    if act is None:
        return
    t_i, pieza, fl, k = act
    u = 1.0 if t_i == cambios[0][0] else PF.entra(t, t_i, 0.25)
    X, Y, h = pl.en(t, x, y, frac * k)
    PF.actor(lz, pieza, X, Y, h * (0.92 + 0.08 * u), flip=fl, tono=tono, sy=PF.respira(t, fase=fase), rot=(1 - u) * 4, op=op)


def camino(lz, pl, t, pieza, ta, tb, p0, p1, f0, f1, flip=False, tono=None, pasos=2.2, salto=0.035, op=1.0,
           desde_antes=True, hasta_despues=True):
    """Títere de papel que avanza (pieza sin ciclo): saltitos y balanceo; posición y tamaño interpolados."""
    if (t < ta and not desde_antes) or (t > tb and not hasta_despues):
        return
    flip = rumbo(pieza, p0[0], p1[0], flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    X, Y, h = pl.en(t, lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(f0, f1, u))
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    bote = abs(math.sin(ph)) if mov else 0.0
    PF.actor(lz, pieza, X, Y - bote * salto * h, h, flip=flip, tono=tono, rot=3.0 * math.sin(ph) if mov else 0.0, op=op,
             sy=PF.respira(t))


def anda(lz, pl, t, ciclo, ta, tb, p0, p1, f0, f1, paso=0.95, tono=None, op=1.0, desde_antes=False, hasta_despues=True):
    """Ciclo de caminar (el cuadro sale de la distancia recorrida: los pies no patinan) de p0 a p1 con el tamaño de f0 a f1."""
    if (t < ta and not desde_antes) or (t > tb and not hasta_despues):
        return
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, y, f = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(f0, f1, u)
    X, Y, h = pl.en(t, x, y, f)
    n = PF.ciclo_n(ciclo)
    dist = math.hypot(x - p0[0], (y - p0[1]) * 0.56) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h, flip=rumbo(ciclo, p0[0], p1[0], False), tono=tono, op=op)


def aves(lz, t, vuelos, tono=None):
    """vuelos: [(t_ini, dur, y0, y1, alto px, sentido, fase)] en pantalla; aleteo a 9 cuadros/s."""
    for t_i, dur, y0, y1, hpx, sent, fa in vuelos:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(-0.08, 1.08, u) if sent > 0 else lerp(1.08, -0.08, u)
        y = lerp(y0, y1, u) + 0.012 * math.sin(t * 2.1 + fa)
        k = int((t * 9 + fa * 7)) % len(AVES)
        PF.actor(lz, AVES[k], x * W, y * H, hpx, flip=sent < 0, ancla=(0.5, 0.5), suelo=0, tono=tono)


def plantas(lz, pl, t, lista, tono=None):
    """Primer plano (capa > 1) en coordenadas de pantalla: [(pieza, x, y, frac de alto de pantalla, capa, flip)]; se mece."""
    for k, (pz, x, y, frac, capa, fl) in enumerate(lista):
        X, Y, h = pl.fg(t, x, y, frac, capa)
        PF.actor(lz, pz, X, Y, h, flip=fl, rot=1.6 * math.sin(1.3 * t + k * 1.9), suelo=0, tono=tono)


def pega(lz, pieza, X, Y, hpx, t, t_in, t_out=None, rot=0.0, tono=None, op=1.0, flota=True):
    """Pegatina en pantalla (un recuerdo, un objeto): entra con rebote, flota y se despega."""
    if t < t_in or (t_out is not None and t > t_out + 0.35):
        return
    u = PF.entra(t, t_in, 0.45)
    s = 1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.35))
    dy = 6.0 * math.sin(1.4 * t) if flota else 0.0
    PF.actor(lz, pieza, X, Y + dy, hpx * (0.55 + 0.45 * u) * (0.6 + 0.4 * s), rot=rot + (1 - u) * 10, ancla=(0.5, 0.5),
             suelo=0, tono=tono, op=op * clamp01(u * 3) * s)


def desenfocado(lz, pieza, X, Y, hpx, sigma=8.0, tono=None, flip=False):
    """Pieza muy cerca de la cámara, fuera de foco (primer plano que tapa)."""
    capa = lz.copy()
    PF.actor(capa, pieza, X, Y, hpx, suelo=0, tono=tono, flip=flip)
    m = cv2.GaussianBlur((np.abs(capa - lz).max(-1) > 0.004).astype(np.float32), (0, 0), sigma)[..., None]
    lz[:] = lz * (1 - m) + cv2.GaussianBlur(capa, (0, 0), sigma) * m


def desenfoque(lz, s=2.5):
    lz[:] = cv2.GaussianBlur(lz, (0, 0), s)


def sacudida(lz, t, t_ini, fuerza=14.0, dur=0.45):
    """El golpe sacude la cámara (portazo, plato, puñetazo)."""
    u = (t - t_ini) / dur
    if not 0 <= u <= 1:
        return
    a = fuerza * (1 - u) ** 2
    dx, dy = a * math.sin(t * 91.0), a * 0.7 * math.cos(t * 73.0)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    lz[:] = cv2.warpAffine(lz, M, (W, H), borderMode=cv2.BORDER_REFLECT)


_YY = np.linspace(0, 1, H, dtype=np.float32)[:, None]
_XX = np.linspace(0, 1, W, dtype=np.float32)[None, :]


def sombra_pasa(lz, t, t_ini, dur=1.6, fuerza=0.30, sentido=1):
    """Algo grande pasa por fuera: una sombra blanda barre el cuarto."""
    u = (t - t_ini) / dur
    if not 0 <= u <= 1:
        return
    c = lerp(-0.3, 1.3, u) if sentido > 0 else lerp(1.3, -0.3, u)
    m = np.exp(-((_XX - c) / 0.16) ** 2) * fuerza * math.sin(u * math.pi)
    lz *= (1 - m)[..., None]


def vineta_fuerte(lz, k=0.45):
    """Oscurece las orillas (miedo, recuerdo)."""
    r = np.sqrt(((_XX - 0.5) / 0.62) ** 2 + ((_YY - 0.5) / 0.55) ** 2)
    lz *= (1 - k * np.clip(r - 0.35, 0, 1) ** 1.4)[..., None]


def sepia(lz, k=1.0):
    g = lz.mean(-1, keepdims=True)
    lz[:] = lz * (1 - k) + g * np.float32((1.08, 0.94, 0.74)) * k


def motas(lz, t, x0, y0, x1, y1, n=36, sem=0, color=(1.0, 0.95, 0.80), fuerza=0.45, r=2.4):
    """Polvo / pétalos que flotan (rectángulo de PANTALLA relativo)."""
    base = np.random.RandomState(sem).rand(n, 4)
    for bx, by, bv, bs in base:
        x = x0 + (x1 - x0) * ((bx + 0.010 * t * (0.4 + bv)) % 1.0)
        y = y0 + (y1 - y0) * ((by + 0.016 * t * (bv - 0.5) + 0.02 * math.sin(t * 0.7 + bx * 9)) % 1.0)
        PF._blob(lz, x * W, y * H, r * (0.7 + bs), color, fuerza * (0.55 + 0.45 * math.sin(t * 1.3 + bx * 20)), aditivo=True)


def petalos(lz, t, n=26, sem=4, color=(0.62, 0.48, 0.86)):
    """Flores de jacaranda que caen girando (pantalla)."""
    base = np.random.RandomState(sem).rand(n, 4)
    for bx, by, bv, bs in base:
        y = ((by + t * (0.05 + 0.05 * bv)) % 1.1) - 0.05
        x = (bx + 0.03 * math.sin(t * (0.8 + bv) + bx * 9) + 0.02 * t * bv) % 1.0
        r = 4 + 4 * bs
        ang = t * (2 + 3 * bv) + bx * 7
        cv2.ellipse(lz, (int(x * W), int(y * H)), (int(r), max(2, int(r * 0.55 * abs(math.cos(ang))) + 1)), math.degrees(ang),
                    0, 360, color, -1, cv2.LINE_AA)


def palomillas(lz, X, Y, r, t, n=6):
    """Palomillas que dan vueltas al foco."""
    for i in range(n):
        a = t * (2.2 + 0.4 * i) + i * 1.7
        px = X + r * (0.6 + 0.3 * math.sin(t * 1.3 + i)) * math.cos(a)
        py = Y + r * 0.6 * math.sin(a * 1.3)
        cv2.circle(lz, (int(px), int(py)), 2 + (i % 2), (0.95, 0.92, 0.78), -1, cv2.LINE_AA)


@functools.lru_cache(maxsize=4)
def _luces(fondo, y0, y1, modo):
    """Estrellas (puntos claros sobre el cielo) o luces cálidas pintadas en el fondo → [(x, y, fase)] normalizados."""
    a = PF._fondo_rgb(fondo).astype(np.float32) / 255.0
    hs, ws = a.shape[:2]
    L = a.mean(-1)
    loc = L - cv2.GaussianBlur(L, (0, 0), 3)
    if modo == "estrella":
        m = loc > 0.10
    else:
        m = (a[..., 0] > 0.75) & (a[..., 1] > 0.50) & (a[..., 2] < 0.55) & (loc > 0.05)
    m[:int(y0 * hs)] = False
    m[int(y1 * hs):] = False
    ys, xs = np.nonzero(m)
    if not len(xs):
        return ()
    rng = np.random.RandomState(3)
    k = rng.choice(len(xs), min(70, len(xs)), replace=False)
    return tuple((xs[i] / ws, ys[i] / hs, rng.rand() * 6.28) for i in k)


def titilan(lz, pl, t, fondo, y0, y1, modo, color, r=5.0, inten=0.55):
    for x, y, fa in _luces(fondo, y0, y1, modo):
        X, Y, s = pl.P(t, x, y)
        v = 0.5 + 0.5 * math.sin(t * (1.7 + fa) + fa * 3)
        PF._blob(lz, X, Y, r * s * 1.6, color, inten * v ** 2, aditivo=True)


@functools.lru_cache(maxsize=64)
def _wh(nombre):
    return Image.open(f"piezas/{nombre}.png").size


# ------------------------------------------------------------------ la RUEDA DE LA FORTUNA (la arma el código)
FOCOS_RUEDA = [(1.0, 0.86, 0.40), (1.0, 0.52, 0.72), (0.42, 0.95, 0.92)]
G_VACIAS = ["utileria_feria/00", "utileria_feria/02", "utileria_feria/01", "utileria_feria/06", "utileria_feria/03",
            "utileria_feria/07", "utileria_feria/05", "utileria_feria/10"]


def rueda(lz, X, Y, R, ang, t, gond=None, carga=None, tono=None, piso=None, luces=1.0, mece=1.0):
    """Rueda de la fortuna con centro (X, Y) px y radio R px girada `ang` rad. gond = 8 piezas de góndola (las que llevan gente
    son de gondolas_hoja); carga = {k: pieza} objeto que viaja en la góndola k; piso = Y px del suelo (dibuja las patas en A)."""
    gond = gond or G_VACIAS
    if piso is not None:                                   # patas en A: el eje (arriba de la pieza) en el centro de la rueda
        hp = (piso - Y) / 0.95
        PF.actor(lz, "utileria_feria/04", X, Y - 0.05 * hp, hp, ancla=(0.5, 0.0), suelo=0, tono=tono, sombra=False)
        X0, Y0 = X, piso
        PF.sombra_suelo(lz, X0, Y0, 0.42 * hp, 0.03 * hp, op=0.25)
    PF.actor(lz, "rueda/00", X, Y, 2.04 * R, rot=math.degrees(ang), ancla=(0.5, 0.5), suelo=0, tono=tono)
    if luces > 0:                                          # focos del aro que se encienden en ola
        for k in range(24):
            a = ang + 2 * math.pi * k / 24
            v = 0.5 + 0.5 * math.sin(t * 5.0 - k * 0.9)
            PF._blob(lz, X + 0.97 * R * math.cos(a), Y + 0.97 * R * math.sin(a), 0.07 * R, FOCOS_RUEDA[k % 3],
                     0.55 * luces * v ** 2, aditivo=True)
    n = len(gond)
    for k in range(n):
        a = ang + 2 * math.pi * k / n
        px, py = X + 0.90 * R * math.cos(a), Y + 0.90 * R * math.sin(a)
        w, h = _wh(gond[k])
        gh = 0.44 * R * h / w
        sw = mece * (3.0 * math.sin(t * 1.6 + k * 1.3))
        PF.actor(lz, gond[k], px, py, gh, ancla=(0.5, 0.02), rot=sw, suelo=0, tono=tono)
        if carga and k in carga:                           # lo que viaja adentro asoma sobre la barra
            r = math.radians(sw)
            dx, dy = -math.sin(r) * gh * 0.50, math.cos(r) * gh * 0.50
            PF.actor(lz, carga[k], px + dx, py + dy, gh * 0.42, ancla=(0.5, 1.0), rot=sw, suelo=0, tono=tono)


# ------------------------------------------------------------------ los PLATOS de la pared (uno menos cada vuelta)
# cabeza de cada clavito pintado (x, y normalizados del escenario) y diámetro del plato (fracción del alto del escenario)
CLAVOS = {
    "cocina_tarde": ([(0.031, 0.181), (0.082, 0.184), (0.139, 0.191), (0.188, 0.196), (0.235, 0.200), (0.282, 0.205),
                      (0.323, 0.210)], 0.075),
    "cocina_noche": ([(0.046, 0.204), (0.081, 0.208), (0.117, 0.216), (0.151, 0.222), (0.183, 0.228), (0.216, 0.234),
                      (0.249, 0.238), (0.279, 0.245)], 0.052),
    "cocina_manana": ([(0.051, 0.188), (0.085, 0.191), (0.119, 0.194), (0.152, 0.195), (0.187, 0.199), (0.218, 0.202),
                       (0.251, 0.206), (0.281, 0.208)], 0.052),
}
PLATOS = ["utileria_casa/00", "utileria_casa/07", "utileria_casa/11", "utileria_casa/17", "utileria_casa/18"]


def platos(lz, pl, t, fondo, hay, tono=None, caen=None):
    """Cuelga los platos de barro en los clavitos pintados. hay = índices con plato; caen = {índice: t} el plato se descuelga
    en t y cae girando fuera de cuadro."""
    clavos, diam = CLAVOS[fondo]
    for i, (x, y) in enumerate(clavos):
        if i not in hay:
            continue
        X, Y, s = pl.P(t, x, y)
        hpx = pl.alto_px(t, diam)
        rot = 1.2 * math.sin(t * 0.9 + i * 2.1)
        dy = 0.0
        if caen and i in caen and t >= caen[i]:
            u = t - caen[i]
            if u > 1.4:
                continue
            dy = 2600 * u * u
            rot += 160 * u * (1 if i % 2 else -1)
        PF.actor(lz, PLATOS[(i * 3) % len(PLATOS)], X, Y - 0.06 * hpx + dy, hpx * 1.06, ancla=(0.5, 0.0), rot=rot, suelo=0,
                 tono=tono, flip=bool(i % 2))


# ------------------------------------------------------------------ el celular de Fer (chat dibujado por código)
_FN = D.FUENTES


def _fnt(k, px):
    return ImageFont.truetype(_FN[k], max(8, int(px)))


@functools.lru_cache(maxsize=8)
def _chat(alto_px):
    """Celular rosa de Fer con un chat inocente con «Kevin» (un compañero): la tarea de mate. RGBA float."""
    w = alto_px // 2
    s = w / 100.0
    im = Image.new("RGBA", (w, alto_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    R = int(13 * s)
    d.rounded_rectangle([0, 0, w - 1, alto_px - 1], R, fill=(226, 120, 150, 255))
    m = int(4.5 * s)
    x0, y0, x1, y1 = m, m, w - 1 - m, alto_px - 1 - m
    d.rounded_rectangle([x0, y0, x1, y1], int(R * 0.75), fill=(230, 226, 218, 255))
    d.rectangle([x0, y0 + 9 * s, x1, y0 + 24 * s], fill=(36, 48, 56, 255))
    d.ellipse([x0 + 5 * s, y0 + 11.5 * s, x0 + 15 * s, y0 + 21.5 * s], fill=(120, 150, 170, 255))
    d.text((x0 + 18 * s, y0 + 11.8 * s), "Kevin", font=_fnt("sans_b", 5.2 * s), fill=(240, 240, 244, 255))
    d.text((x0 + 18 * s, y0 + 17.6 * s), "en línea", font=_fnt("sans_l", 3.8 * s), fill=(170, 190, 200, 255))
    yy = y0 + 32 * s
    for quien, lineas, hora in (("k", ("¿ya hiciste la", "de mate?"), "5:12 p. m."),
                                ("f", ("jaja sí", "mañana te la paso"), "5:14 p. m."),
                                ("k", ("eres la mejor jaja",), "5:14 p. m.")):
        alto = (7.4 * len(lineas) + 8) * s
        if quien == "k":
            bx0, bx1, col = x0 + 5 * s, x1 - 22 * s, (255, 255, 255, 255)
        else:
            bx0, bx1, col = x0 + 22 * s, x1 - 5 * s, (214, 246, 200, 255)
        d.rounded_rectangle([bx0, yy, bx1, yy + alto], int(4 * s), fill=col)
        ty = yy + 3.5 * s
        for txt in lineas:
            d.text((bx0 + 4 * s, ty), txt, font=_fnt("sans", 5.4 * s), fill=(30, 30, 36, 255))
            ty += 7.4 * s
        d.text((bx1 - 21 * s, yy + alto - 5.5 * s), hora, font=_fnt("sans_l", 3.3 * s), fill=(140, 140, 150, 255))
        yy += alto + 5 * s
    iy = y1 - 21 * s
    d.rounded_rectangle([x0 + 4 * s, iy, x1 - 18 * s, iy + 13 * s], int(6 * s), fill=(255, 255, 255, 255),
                        outline=(200, 200, 210, 255), width=max(1, int(0.5 * s)))
    d.text((x0 + 9 * s, iy + 3.2 * s), "Escribe un mensaje…", font=_fnt("sans", 4.8 * s), fill=(150, 150, 160, 255))
    d.ellipse([x1 - 15 * s, iy, x1 - 3 * s, iy + 13 * s], fill=(37, 160, 110, 255))
    return np.asarray(im, np.float32) / 255.0


def _blend(lz, a, op=1.0):
    al = a[..., 3:4] * op
    lz[:] = lz * (1 - al) + a[..., :3] * al


def pegar_rgba(lz, img, X, Y, escala=1.0, rot=0.0, op=1.0):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, escala)
    M[0, 2] += X - w / 2
    M[1, 2] += Y - h / 2
    capa = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    _blend(lz, capa, op)


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0_, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0_, ent=ent, dib=f))
        return f
    return deco


# ================================================================== 1 · LA FERIA (hace 6 años)
F = "feria"
f_mira, f_y = T(F, "mira", 1), T(F, "y", 2)
f_fin = t1(F)
W_FN = (0.735, 0.300, 0.255, 0.80)          # rueda en feria_noche: centro x, y · radio · suelo (fracciones del escenario)
OM_F = 0.10                                 # rad/s en la feria
A0_F = -math.pi / 2 - OM_F * 15.6           # la góndola roja con papá y Diego llega arriba con «el hombre más grande del mundo»
G_FERIA = ["gondolas_hoja/00"] + G_VACIAS[1:]
G_FERIA2 = ["gondolas_hoja/01"] + G_VACIAS[1:]


def rueda_en(lz, pl, t, cfg, ang, gond=None, carga=None, tono=None, luces=1.0, mece=1.0):
    x, y, r, piso = cfg
    X, Y, s = pl.P(t, x, y)
    R = pl.alto_px(t, r)
    _, Yp, _ = pl.P(t, x, piso)
    rueda(lz, X, Y, R, ang, t, gond, carga, tono, Yp, luces, mece)


PF1 = PF.Plano("feria_noche", 0.0, f_mira, z0=1.14, z1=1.03, c0=(0.46, 0.55), c1=(0.52, 0.52), par=(30, 6))
VUELO_F = [(1.0, 11.0, 0.10, 0.07, 30, 1, 0.3)]
snd(0.3, "viento", 0.25, dur=8.0)
snd(3.0, "papel", 0.4)


@toma(0.0)
def f1(lz, t):
    PF1.fondo(lz, t)
    titilan(lz, PF1, t, "feria_noche", 0.0, 0.40, "estrella", (0.85, 0.90, 1.0), r=3.0, inten=0.40)
    titilan(lz, PF1, t, "feria_noche", 0.0, 0.70, "calido", (1.0, 0.78, 0.40), r=6.0, inten=0.45)
    rueda_en(lz, PF1, t, W_FN, A0_F + OM_F * t, G_FERIA, tono=RUEDA_N)
    quieto(lz, PF1, t, "gente_hoja/00", 0.33, 0.82, 0.30, tono=FERIA_N, fase=0.4)
    quieto(lz, PF1, t, "gente_hoja/05", 0.10, 0.90, 0.36, tono=FERIA_N, fase=1.2, rot=2.0 * math.sin(t * 2.0))
    camino(lz, PF1, t, "gente_hoja/06", 0.5, 9.0, (0.88, 0.74), (0.58, 0.80), 0.24, 0.27, tono=FERIA_N, pasos=1.6)
    # papá y Diego (8) caminan de la mano hacia la rueda
    anda(lz, PF1, t, "papa_camina", 0.6, 7.6, (0.18, 0.93), (0.48, 0.86), 0.42, 0.39, tono=FERIA_N, desde_antes=True)
    camino(lz, PF1, t, "diego8_hoja/03", 0.6, 7.6, (0.235, 0.95), (0.535, 0.875), 0.26, 0.24, tono=FERIA_N, pasos=2.6)
    PF.rotulo(lz, "JALPA · HACE 6 AÑOS", W * 0.30, H * 0.13, 54, t, 3.0, 7.6, rot=-2.0)


PF2 = PF.Plano("feria_alta_noche", f_mira - 0.3, f_y, z0=1.10, z1=1.20, c0=(0.50, 0.55), c1=(0.56, 0.60), par=(40, 10))


@toma(f_mira - 0.3, ("desenfoque", 0.5))
def f2(lz, t):
    PF2.fondo(lz, t)
    titilan(lz, PF2, t, "feria_alta_noche", 0.0, 0.30, "estrella", (0.85, 0.90, 1.0), r=3.0, inten=0.45)
    titilan(lz, PF2, t, "feria_alta_noche", 0.45, 1.0, "calido", (1.0, 0.78, 0.40), r=5.0, inten=0.50)
    sw = 2.6 * math.sin(t * 1.1)
    PF.actor(lz, "gondolas_hoja/00", W * 0.40, -H * 0.04, H * 1.12, ancla=(0.5, 0.0), rot=sw, suelo=0, tono=FERIA_N)


PF3 = PF.Plano("feria_noche", f_y - 0.3, f_fin + 0.6, z0=1.75, z1=1.95, c0=(0.71, 0.27), c1=(0.73, 0.22), par=(26, 5))


@toma(f_y - 0.3, ("desenfoque", 0.5))
def f3(lz, t):
    PF3.fondo(lz, t)
    titilan(lz, PF3, t, "feria_noche", 0.0, 0.40, "estrella", (0.85, 0.90, 1.0), r=3.0, inten=0.40)
    rueda_en(lz, PF3, t, W_FN, A0_F + OM_F * t, G_FERIA2, tono=RUEDA_N)


# ================================================================== 2 · EL CLIMA (cocina de tarde)
C = "clima"
c0_ = t0(C)
c_si, c_frena = T(C, "si", 1), T(C, "frenaba", 2)
FRENON, PORTAZO = c_frena + 0.9, c_frena + 2.3
TROCA_LLEGA = c_si + 0.2
c_fin = t1(C)
HUMO_COMAL = (0.79, 0.50)
snd(c0_ + 0.4, "fuego", 0.18, dur=c_fin - c0_)
snd(FRENON + 0.05, "golpe_suave", 0.5)


def cocina_tarde(lz, pl, t, platos_hay=range(7)):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, *HUMO_COMAL)
    PF.humo(lz, t, X, Y, s * 0.8, n=6, color=(0.98, 0.94, 0.88), op=0.22, sem=2, alto=220)
    X, Y, s = pl.P(t, 0.86, 0.30)
    PF.brillo(lz, X, Y, 300 * s, color=(1.0, 0.70, 0.35), inten=0.16, t=t * 0.2, sem=1)
    platos(lz, pl, t, "cocina_tarde", platos_hay, tono=TARDE)


PC1 = PF.Plano("cocina_tarde", c0_, c_si, z0=1.10, z1=1.20, c0=(0.50, 0.55), c1=(0.55, 0.58), par=(24, 5))


@toma(c0_, ("fundido", 0.7))
def c1(lz, t):
    cocina_tarde(lz, PC1, t)
    quieto(lz, PC1, t, "lupe_hoja/01", 0.73, 0.86, 0.46, tono=TARDE, rot=1.5 * math.sin(t * 6.0))
    quieto(lz, PC1, t, "xime3_hoja/00", 0.56, 0.93, 0.17, tono=TARDE, fase=0.7)
    quieto(lz, PC1, t, "diego8_hoja/00", 0.44, 0.93, 0.33, tono=TARDE, fase=1.4)


PC2 = PF.Plano("cocina_tarde", c_si - 0.3, c_frena - 0.2, z0=1.85, z1=2.00, c0=(0.46, 0.66), c1=(0.47, 0.67), par=(18, 4))


@toma(c_si - 0.3, ("desenfoque", 0.5))
def c2(lz, t):
    cocina_tarde(lz, PC2, t)
    quieto(lz, PC2, t, "xime3_hoja/00", 0.56, 0.93, 0.17, tono=TARDE, fase=0.7)
    quieto(lz, PC2, t, "diego8_hoja/00", 0.44, 0.93, 0.33, tono=TARDE, fase=1.4, rot=0.8 * math.sin(t * 7.0))


PC3 = PF.Plano("cocina_tarde", c_frena - 0.2, c_fin + 0.6, z0=2.10, z1=2.30, c0=(0.52, 0.62), c1=(0.53, 0.62), par=(16, 3))


@toma(c_frena - 0.2, ("latigo", 0.35))
def c3(lz, t):
    cocina_tarde(lz, PC3, t)
    poses(lz, PC3, t, [(c_frena - 1, "diego8_hoja/00", False, 1.0), (FRENON, "diego8_hoja/01", False, 1.03)],
          0.47, 0.93, 0.33, tono=TARDE, fase=1.4)
    if t > FRENON:
        quieto(lz, PC3, t, "xime3_hoja/02", 0.615, 0.85, 0.19, tono=TARDE, t_in=FRENON + 0.5, fase=0.3)
    sombra_pasa(lz, t, FRENON - 0.4, dur=1.4, fuerza=0.28, sentido=-1)
    sacudida(lz, t, PORTAZO, 12.0)


# ================================================================== 3 · EL SILENCIO (cocina de noche)
S = "silencio"
s0_ = t0(S)
s_radio, s_otra, s_ahorita = T(S, "radio"), T(S, "otra", 1), T(S, "ahorita", 2)
RADIO_OFF = s_radio + 0.2
s_fin = t1(S)
RADIO = (0.735, 0.505)
FOCO_N = (0.50, 0.20)


def cocina_noche(lz, pl, t, platos_hay=range(8), caen=None, radio_on=False):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, *FOCO_N)
    PF.brillo(lz, X, Y, 360 * s, color=(1.0, 0.86, 0.45), inten=0.22, t=t * 0.3, sem=3)
    palomillas(lz, X, Y + 10 * s, 60 * s, t, n=3)
    if radio_on:
        X, Y, s = pl.P(t, *RADIO)
        PF.brillo(lz, X, Y, 60 * s, color=(1.0, 0.75, 0.35), inten=0.35, t=t, sem=5)
    platos(lz, pl, t, "cocina_noche", platos_hay, tono=FOCO, caen=caen)


MESA_N = (0.0, 0.552, 0.445, 0.97)                 # la mesa pintada de cocina_noche (x0, y0, x1, y1)


def papa_mesa(lz, pl, t):
    """El papá sentado en la cabecera de la mesa PINTADA: su pieza trae mesita propia, que la mesa pintada tapa (se restaura el
    fondo sobre el rectángulo de la mesa, por debajo de la cubierta: las manos y el tenedor quedan encima)."""
    base = lz.copy()
    quieto(lz, pl, t, "papa_hoja/01", 0.452, 0.83, 0.50, flip=True, tono=FOCO, fase=0.2)
    X0, Y0, _ = pl.P(t, MESA_N[0], MESA_N[1])
    X1, Y1, _ = pl.P(t, MESA_N[2], MESA_N[3])
    x0, x1 = int(np.clip(X0, 0, W)), int(np.clip(X1, 0, W))
    y0, y1 = int(np.clip(Y0, 0, H)), int(np.clip(Y1, 0, H))
    lz[y0:y1, x0:x1] = base[y0:y1, x0:x1]


PS1 = PF.Plano("cocina_noche", s0_ - 0.4, s_otra - 0.3, z0=2.6, z1=1.45, c0=(0.71, 0.52), c1=(0.66, 0.60), par=(18, 4))


@toma(s0_ - 0.4, ("corte", 0.1))
def s1(lz, t):
    cocina_noche(lz, PS1, t, radio_on=t < RADIO_OFF)
    quieto(lz, PS1, t, "diego8_hoja/01", 0.86, 0.80, 0.24, flip=True, tono=FOCO, fase=1.1)
    quieto(lz, PS1, t, "lupe_hoja/05", 0.60, 0.90, 0.48, flip=True, tono=FOCO, fase=0.6)
    sombra_pasa(lz, t, s_radio - 0.6, dur=1.5, fuerza=0.35, sentido=-1)
    vineta_fuerte(lz, 0.30)


PS2 = PF.Plano("cocina_noche", s_otra - 0.3, s_ahorita - 0.3, z0=1.95, z1=2.05, c0=(0.44, 0.60), c1=(0.45, 0.61), par=(16, 3))
snd(s_otra - 0.6, "latido", 0.35)


@toma(s_otra - 0.3, ("corte", 0.1))
def s2(lz, t):
    cocina_noche(lz, PS2, t)
    papa_mesa(lz, PS2, t)
    vineta_fuerte(lz, 0.35)


PS3 = PF.Plano("cocina_noche", s_ahorita - 0.3, s_fin + 0.6, z0=1.20, z1=1.32, c0=(0.50, 0.58), c1=(0.47, 0.60), par=(22, 4))


@toma(s_ahorita - 0.3, ("desenfoque", 0.45))
def s3(lz, t):
    cocina_noche(lz, PS3, t)
    quieto(lz, PS3, t, "diego8_hoja/01", 0.85, 0.80, 0.24, flip=True, tono=FOCO, fase=1.1)
    papa_mesa(lz, PS3, t)
    camino(lz, PS3, t, "lupe_hoja/05", s_ahorita - 0.3, s_ahorita + 1.6, (0.70, 0.90), (0.54, 0.92), 0.48, 0.49, tono=FOCO,
           pasos=1.6, flip=True)
    vineta_fuerte(lz, 0.30)


# ================================================================== 4 · DEBAJO DE LA MESA (la tormenta fuera de cuadro)
M = "mesa"
m0_ = t0(M)
m_cuando, m_tapaba, m_canta = T(M, "cuando", 0), T(M, "tapaba", 1), T(M, "cantaba", 1)
GRITO, PLATO = m0_ + 0.6, m0_ + 1.7
m_fin = t1(M)
TIEMBLA = (m0_, m_cuando + 3.0)
snd(PLATO + 0.02, "golpe_suave", 0.6)


def bajo_mesa(lz, pl, t, ninos=None):
    pl.fondo(lz, t)
    # la luz de allá afuera (el foco que se mece tras el golpe)
    v = 0.06 * math.sin(t * 5.0) * (1 - smooth(prog(t, PLATO, PLATO + 5.0))) if t > PLATO else 0.0
    lz *= np.float32(1.0 + v)
    # las piernas de los grandes (rodillas para abajo): ni caras ni golpes
    if t < m_cuando + 3.0:
        k = smooth(prog(t, GRITO, GRITO + 0.6))
        xp = 0.42 + 0.03 * k + 0.015 * math.sin(t * 3.1) * (t > GRITO)
        quieto(lz, pl, t, "utileria_casa/13", xp, 0.72, 0.30, tono=FOCO, rot=2.0 * math.sin(t * 4.0) * (t > GRITO))
        xl = 0.60 + 0.06 * smooth(prog(t, PLATO - 0.3, PLATO + 0.4))
        quieto(lz, pl, t, "utileria_casa/15", xl, 0.70, 0.27, tono=FOCO, flip=True)
    # la esquirla del plato que entra en cuadro y se queda
    if t > PLATO:
        u = smooth(prog(t, PLATO, PLATO + 0.45))
        X, Y, s = pl.P(t, lerp(0.56, 0.47, u), lerp(0.70, 0.84, u))
        PF.actor(lz, "utileria_casa/04", X, Y, pl.alto_px(t, 0.07), rot=lerp(-60, 18, u), ancla=(0.5, 0.5), suelo=0, tono=FOCO)
    if ninos:
        quieto(lz, pl, t, ninos, 0.22, 1.05, 0.66, tono=BAJO, fase=0.5)


PM1 = PF.Plano("bajo_mesa", m0_, m_cuando + 3.0, z0=1.06, z1=1.14, c0=(0.50, 0.55), c1=(0.47, 0.58), par=(22, 4))


@toma(m0_, ("negro", 0.6))
def m1(lz, t):
    bajo_mesa(lz, PM1, t, "duo_mesa_hoja/01")
    sacudida(lz, t, PLATO, 16.0)
    vineta_fuerte(lz, 0.45)


PM2 = PF.Plano("bajo_mesa", m_cuando + 3.0, m_tapaba + 1.5, z0=1.55, z1=1.65, c0=(0.30, 0.78), c1=(0.31, 0.79), par=(16, 3))


@toma(m_cuando + 3.0, ("desenfoque", 0.6))
def m2(lz, t):
    bajo_mesa(lz, PM2, t, "duo_mesa_hoja/00")
    vineta_fuerte(lz, 0.40)


PM3 = PF.Plano("bajo_mesa", m_tapaba + 1.5, m_fin - 4.6, z0=2.05, z1=2.20, c0=(0.24, 0.80), c1=(0.24, 0.81), par=(12, 3))


@toma(m_tapaba + 1.5, ("fundido", 0.8))
def m3(lz, t):
    bajo_mesa(lz, PM3, t, "duo_mesa_hoja/02")
    motas(lz, t, 0.0, 0.0, 1.0, 1.0, n=20, sem=2, color=(1.0, 0.85, 0.60), fuerza=0.25)
    vineta_fuerte(lz, 0.40)


PM4 = PF.Plano("bajo_mesa", m_fin - 4.6, m_fin + 0.8, z0=1.40, z1=1.25, c0=(0.33, 0.74), c1=(0.38, 0.70), par=(16, 3))


@toma(m_fin - 4.6, ("fundido", 1.0))
def m4(lz, t):
    bajo_mesa(lz, PM4, t, "duo_mesa_hoja/03")
    motas(lz, t, 0.0, 0.0, 1.0, 1.0, n=20, sem=3, color=(1.0, 0.85, 0.60), fuerza=0.22)
    vineta_fuerte(lz, 0.45)


# ================================================================== 5 · LAS FLORES (cocina de mañana)
Fl = "flores"
fl0 = t0(Fl)
fl_perd, fl_flores, fl_pan, fl_nos, fl_y = T(Fl, "perd"), T(Fl, "flores", 1), T(Fl, "pan", 1), T(Fl, "nosotros", 1), T(Fl, "y", 2)
fl_hasta, fl_volvia2 = T(Fl, "hasta", 2), T(Fl, "volvía", 2, n=1)
fl_fin = t1(Fl)
ENTREGA = fl_perd + 2.4
PLATOS_M = [0, 1, 2, 4, 5, 6, 7]                  # uno menos: el clavito 3 se quedó vacío
VUELO_M = [(fl0 + 0.5, 8.0, 0.30, 0.26, 26, 1, 0.5)]
snd(fl0 + 0.3, "amanecer", 0.35, dur=3.0)
snd(ENTREGA, "papel", 0.5)


def cocina_manana(lz, pl, t, ramo=True):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, 0.50, 0.28)
    PF.brillo(lz, X, Y, 380 * s, color=(1.0, 0.95, 0.80), inten=0.14, t=t * 0.1, sem=6)
    motas(lz, t, 0.30, 0.15, 0.65, 0.75, n=26, sem=5, color=(1.0, 0.97, 0.85), fuerza=0.30)
    platos(lz, pl, t, "cocina_manana", PLATOS_M, tono=MANANA)
    if ramo and t >= ENTREGA:                             # el ramo ya está en el frasco de la mesa
        quieto(lz, pl, t, "utileria_casa/06", 0.172, 0.530, 0.12, tono=MANANA, t_in=ENTREGA, suelo=0)


PFL1 = PF.Plano("cocina_manana", fl0, fl_flores - 0.3, z0=1.15, z1=1.30, c0=(0.62, 0.62), c1=(0.52, 0.64), par=(24, 5))


@toma(fl0, ("fundido", 1.0))
def fl1(lz, t):
    cocina_manana(lz, PFL1, t)
    aves(lz, t, VUELO_M, tono=MANANA)
    poses(lz, PFL1, t, [(fl0 - 1, "lupe_hoja/05", True, 1.0), (ENTREGA, "lupe_hoja/04", False, 1.0)], 0.38, 0.90, 0.47,
          tono=MANANA, fase=0.6)
    if t < fl_perd - 0.2:
        anda(lz, PFL1, t, "papa_camina", fl0, fl_perd - 0.2, (0.86, 0.80), (0.62, 0.88), 0.46, 0.51, tono=MANANA,
             desde_antes=True)
    else:
        quieto(lz, PFL1, t, "papa_hoja/03", 0.60, 0.88, 0.51, tono=MANANA, flip=True, fase=0.3)


PFL2 = PF.Plano("cocina_manana", fl_flores - 0.3, fl_y - 0.3, z0=1.90, z1=2.05, c0=(0.26, 0.48), c1=(0.27, 0.47), par=(16, 3))
snd(fl_flores, "pop", 0.4)
snd(fl_pan, "pop", 0.4)
snd(fl_nos + 0.1, "brillo", 0.35)


@toma(fl_flores - 0.3, ("desenfoque", 0.5))
def fl2(lz, t):
    cocina_manana(lz, PFL2, t)
    quieto(lz, PFL2, t, "utileria_casa/02", 0.222, 0.560, 0.11, tono=MANANA, t_in=fl_pan, suelo=0.2)
    if t > fl_nos - 0.2:                                  # el recuerdo de la feria: pegatinas que flotan
        a = smooth(prog(t, fl_nos - 0.2, fl_nos + 0.5))
        lz *= np.float32(1 - 0.30 * a)
        pega(lz, "diego8_hoja/02", W * 0.66, H * 0.50, H * 0.62, t, fl_nos, rot=-4)
        pega(lz, "xime3_hoja/03", W * 0.86, H * 0.60, H * 0.42, t, fl_nos + 0.35, rot=5)
        pega(lz, "utileria_feria/13", W * 0.48, H * 0.26, H * 0.36, t, fl_nos + 0.7, rot=-6)


PFL3 = PF.Plano("cocina_manana", fl_y - 0.3, fl_fin + 0.6, z0=2.30, z1=3.00, c0=(0.16, 0.30), c1=(0.152, 0.25), par=(12, 3))


@toma(fl_y - 0.3, ("fundido", 0.7))
def fl3(lz, t):
    cocina_manana(lz, PFL3, t, ramo=False)
    k = smooth(prog(t, fl_hasta + 0.4, fl_volvia2 + 0.6))
    lz *= np.float32(1 - 0.38 * k)
    sombra_pasa(lz, t, fl_hasta + 0.2, dur=2.6, fuerza=0.35)


# ================================================================== 6 · LA RUEDA (el círculo)
R_ = "rueda"
r0 = t0(R_)
r_sube, r_arriba, r_bajaba, r_abajo, r_tormenta = (T(R_, "subía", 1), T(R_, "arriba", 1), T(R_, "bajaba", 1), T(R_, "abajo", 2),
                                                   T(R_, "tormenta", 2))
r_otra, r_cada, r_pared, r_menos = T(R_, "otra", 3), T(R_, "cada", 3), T(R_, "pared", 4), T(R_, "menos", 4)
r_fin = t1(R_)
RAYO = r_tormenta + 0.1
CARGA = {0: "utileria_casa/06", 2: "utileria_casa/02", 4: "utileria_casa/01", 6: "utileria_casa/04"}


def ang_rueda(t):
    """Ángulo de la rueda simbólica: gira al revés de las manecillas (sube por la derecha) y se acelera desde «otra vez»."""
    om0, om1 = -0.32, -2.6
    ta, tb = r_otra, r_cada + 1.4
    if t < ta:
        return om0 * (t - r0)
    a = om0 * (ta - r0)
    d = tb - ta                                         # ω(u) = om0 + (om1 − om0)·u², u = (t − ta)/d: se integra
    if t < tb:
        u = (t - ta) / d
        return a + om0 * (t - ta) + (om1 - om0) * d * u ** 3 / 3
    return a + om0 * d + (om1 - om0) * d / 3 + om1 * (t - tb)


PR1 = PF.Plano("feria_noche", r0, r_pared - 0.3, z0=1.30, z1=1.42, c0=(0.735, 0.33), c1=(0.735, 0.31), par=(20, 4))


@toma(r0, ("desenfoque", 0.6))
def r1(lz, t):
    PR1.fondo(lz, t)
    lz *= np.float32(0.72)
    titilan(lz, PR1, t, "feria_noche", 0.0, 0.40, "estrella", (0.85, 0.90, 1.0), r=3.0, inten=0.40)
    tor = smooth(prog(t, r_abajo, r_tormenta + 0.5)) * (1 - smooth(prog(t, r_otra, r_otra + 1.2)))
    rueda_en(lz, PR1, t, W_FN, ang_rueda(t), carga=CARGA, tono=RUEDA_N, luces=1.0 - 0.6 * tor,
             mece=1.0 + 2.0 * smooth(prog(t, r_otra, r_cada + 1.0)))
    lz *= np.float32(1 - 0.35 * tor)
    if RAYO < t < RAYO + 0.5:                             # el relámpago de la tormenta
        lz += np.float32(0.55 * (1 - (t - RAYO) / 0.5) ** 2)
    vineta_fuerte(lz, 0.35)
    X, Y, s = PR1.P(t, 0.735, 0.30)
    R = PR1.alto_px(t, 0.255)
    PF.rotulo(lz, "SUBE CON FLORES", X + R * 1.35, Y + R * 0.15, 44, t, r_sube, r_pared - 0.6, rot=-3.0)
    PF.rotulo(lz, "ARRIBA, TODO BONITO", X, Y - R * 1.22, 44, t, r_arriba, r_pared - 0.6, rot=1.5)
    PF.rotulo(lz, "BAJA DESPACITO", X - R * 1.35, Y + R * 0.10, 44, t, r_bajaba, r_pared - 0.6, rot=2.5)
    PF.rotulo(lz, "LA TORMENTA", X, Y + R * 1.30, 52, t, r_abajo + 0.3, r_pared - 0.6, rot=-1.5,
              tinta=(246, 236, 212), papel=(52, 40, 46))
    sacudida(lz, t, RAYO, 10.0)


PR2 = PF.Plano("cocina_noche", r_pared - 0.3, r_fin + 0.6, z0=2.9, z1=3.2, c0=(0.165, 0.27), c1=(0.165, 0.26), par=(10, 2))
CAEN = {1: r_pared + 0.5, 6: r_pared + 0.75, 3: r_menos - 0.15, 4: r_menos + 0.1}
snd(r_pared + 0.6, "golpe_suave", 0.35)
snd(r_menos, "golpe_suave", 0.35)


@toma(r_pared - 0.3, ("destello", 0.4))
def r2(lz, t):
    cocina_noche(lz, PR2, t, platos_hay=[0, 1, 3, 4, 6, 7], caen=CAEN)
    vineta_fuerte(lz, 0.40)


# ================================================================== 7 · FER (hoy, el jardín)
Fe = "fer"
fe0 = t0(Fe)
fe_novia, fe_esa, fe_al, fe_cel, fe_que = T(Fe, "novia", 0), T(Fe, "esa", 1), T(Fe, "al", 2), T(Fe, "cel", 2), T(Fe, "que", 3)
fe_eso = T(Fe, "eso", 2)
fe_fin = t1(Fe)
VUELO_J = [(fe0 + 0.5, 9.0, 0.12, 0.08, 34, -1, 0.9), (fe0 + 6.0, 9.0, 0.18, 0.14, 28, 1, 1.6)]
snd(fe0 + 0.3, "viento", 0.25, dur=fe_fin - fe0)
snd(fe0 + 1.6, "papel", 0.4)


def jardin(lz, pl, t):
    pl.fondo(lz, t)
    petalos(lz, t)


PJ1 = PF.Plano("jardin_tarde", fe0, fe_esa - 0.3, z0=1.08, z1=1.20, c0=(0.42, 0.55), c1=(0.44, 0.62), par=(30, 6))


@toma(fe0, ("fundido", 0.9))
def j1(lz, t):
    jardin(lz, PJ1, t)
    aves(lz, t, VUELO_J, tono=JARDIN)
    quieto(lz, PJ1, t, "naturaleza/04", 0.70, 0.79, 0.07, tono=JARDIN, fase=0.2)
    anda(lz, PJ1, t, "fer_camina", fe0, fe_esa - 0.3, (0.06, 0.86), (0.34, 0.85), 0.42, 0.42, tono=JARDIN, desde_antes=True)
    anda(lz, PJ1, t, "diego14_camina", fe0, fe_esa - 0.3, (0.13, 0.89), (0.42, 0.88), 0.44, 0.44, tono=JARDIN,
         desde_antes=True)
    PF.rotulo(lz, "HOY", W * 0.78, H * 0.16, 58, t, fe0 + 1.6, fe_novia + 0.6, rot=2.0)


# en el banco: encuadre de la cintura para arriba (el banco propio de cada pieza queda fuera de cuadro)
PJ2 = PF.Plano("jardin_tarde", fe_esa - 0.3, fe_al - 0.3, z0=2.45, z1=2.60, c0=(0.37, 0.50), c1=(0.37, 0.505), par=(18, 4))


@toma(fe_esa - 0.3, ("desenfoque", 0.5))
def j2(lz, t):
    jardin(lz, PJ2, t)
    quieto(lz, PJ2, t, "fer_hoja/00", 0.325, 0.90, 0.40, tono=JARDIN, fase=0.4,
           rot=2.0 * math.sin(t * 7.0) * (fe_esa < t < fe_esa + 3.0))
    quieto(lz, PJ2, t, "diego14_hoja/00", 0.410, 0.90, 0.41, tono=JARDIN, fase=1.3)


PJ3 = PF.Plano("jardin_tarde", fe_al - 0.3, fe_cel - 0.3, z0=1.55, z1=1.70, c0=(0.45, 0.62), c1=(0.46, 0.64), par=(24, 5))


@toma(fe_al - 0.3, ("fundido", 0.5))
def j3(lz, t):
    jardin(lz, PJ3, t)
    quieto(lz, PJ3, t, "fer_hoja/03", 0.40, 0.88, 0.42, tono=JARDIN, fase=0.4)
    quieto(lz, PJ3, t, "diego14_hoja/01", 0.52, 0.89, 0.43, tono=JARDIN, fase=1.3, flip=True)


PJ_CEL = PF.Plano("jardin_tarde", fe_cel - 0.3, fe_que - 0.3, z0=1.6, z1=1.65, c0=(0.48, 0.62), c1=(0.48, 0.62), par=(0, 0))
snd(fe_cel - 0.2, "pin", 0.5)


@toma(fe_cel - 0.3, ("corte", 0.1))
def j4(lz, t):
    jardin(lz, PJ_CEL, t)
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 14) * np.float32(0.6)
    hpx = int(H * 0.90) // 2 * 2
    u = PF.entra(t, fe_cel - 0.1, 0.5)
    pegar_rgba(lz, _chat(hpx), W * 0.5, H * 0.52 + (1 - u) * 60, escala=0.94 + 0.06 * u, rot=0.8 * math.sin(t * 1.7),
               op=clamp01(u * 2))


PJ5 = PF.Plano("jardin_tarde", fe_que - 0.3, fe_fin + 0.6, z0=2.6, z1=2.8, c0=(0.535, 0.55), c1=(0.535, 0.545), par=(16, 3))


@toma(fe_que - 0.3, ("corte", 0.1))
def j5(lz, t):
    jardin(lz, PJ5, t)
    quieto(lz, PJ5, t, "diego14_hoja/01", 0.52, 0.89, 0.43, tono=JARDIN, fase=1.3, flip=True)
    lz *= np.float32(1 - 0.25 * smooth(prog(t, fe_que, fe_fin)))
    vineta_fuerte(lz, 0.35)


# ================================================================== 8 · EL CORREDOR (el grito, el golpe a la pared)
K = "corredor"
k0 = t0(K)
k_por, k_eh = T(K, "por"), T(K, "eh")
GOLPE = k_eh + 0.45
k_fin = t1(K)


PK1 = PF.Plano("corredor_secu", k0, GOLPE - 0.25, z0=1.25, z1=1.40, c0=(0.45, 0.62), c1=(0.42, 0.64), par=(26, 5))


@toma(k0, ("latigo", 0.4))
def k1(lz, t):
    PK1.fondo(lz, t)
    quieto(lz, PK1, t, "gente_hoja/01", 0.66, 0.86, 0.46, tono=ESCUELA, flip=True, fase=0.5)
    poses(lz, PK1, t, [(k0 - 1, "fer_hoja/05", False, 1.0), (k_por, "fer_hoja/01", False, 1.0)], 0.56, 0.86, 0.45,
          tono=ESCUELA, fase=0.2)
    if t < k_por - 0.1:
        anda(lz, PK1, t, "diego14_camina", k0, k_por - 0.1, (0.16, 0.90), (0.40, 0.88), 0.46, 0.46, tono=ESCUELA,
             desde_antes=True)
    else:
        quieto(lz, PK1, t, "diego14_hoja/01", 0.41, 0.88, 0.46, tono=ESCUELA, fase=1.0, rot=1.5 * math.sin(t * 9.0))


PK2 = PF.Plano("corredor_secu", GOLPE - 0.25, k_fin + 0.6, z0=1.50, z1=1.62, c0=(0.30, 0.64), c1=(0.33, 0.64), par=(20, 4))


@toma(GOLPE - 0.25, ("corte", 0.1))
def k2(lz, t):
    PK2.fondo(lz, t)
    camino(lz, PK2, t, "gente_hoja/01", GOLPE + 0.5, GOLPE + 3.0, (0.66, 0.86), (0.84, 0.82), 0.46, 0.43, tono=ESCUELA,
           pasos=2.4)
    poses(lz, PK2, t, [(k0, "fer_hoja/01", False, 1.0), (GOLPE + 0.15, "fer_hoja/02", False, 1.0)], 0.56, 0.86, 0.45,
          tono=ESCUELA, fase=0.2)
    quieto(lz, PK2, t, "extra/diego_golpe", 0.215, 0.81, 0.43, flip=True, tono=ESCUELA, fase=1.0)
    sacudida(lz, t, GOLPE, 18.0)


# ================================================================== 9 · LA CARA (igualito que mi amá)
Ca = "cara"
ca0 = t0(Ca)
ca_igual = T(Ca, "igualito")
ca_fin = t1(Ca)

PCA1 = PF.Plano("corredor_secu", ca0, ca_igual - 0.2, z0=2.45, z1=2.65, c0=(0.555, 0.60), c1=(0.555, 0.60), par=(14, 3))


@toma(ca0, ("desenfoque", 0.5))
def ca1(lz, t):
    PCA1.fondo(lz, t)
    quieto(lz, PCA1, t, "fer_hoja/02", 0.56, 0.86, 0.45, tono=ESCUELA, fase=0.2, rot=1.0 * math.sin(t * 13.0))
    vineta_fuerte(lz, 0.35)


PCA2 = PF.Plano("cocina_noche", ca_igual - 0.2, ca_igual + 2.4, z0=2.10, z1=2.25, c0=(0.62, 0.62), c1=(0.62, 0.62), par=(14, 3))


@toma(ca_igual - 0.2, ("destello", 0.35))
def ca2(lz, t):
    cocina_noche(lz, PCA2, t)
    quieto(lz, PCA2, t, "lupe_hoja/03", 0.62, 0.90, 0.48, tono=FOCO, fase=0.2, rot=1.0 * math.sin(t * 13.0))
    vineta_fuerte(lz, 0.45)


PCA3 = PF.Plano("corredor_secu", ca_igual + 2.4, ca_fin + 0.6, z0=1.30, z1=1.20, c0=(0.48, 0.64), c1=(0.52, 0.62), par=(24, 5))


@toma(ca_igual + 2.4, ("destello", 0.35))
def ca3(lz, t):
    PCA3.fondo(lz, t)
    camino(lz, PCA3, t, "fer_hoja/04", ca_igual + 2.6, ca_fin + 0.6, (0.56, 0.86), (0.76, 0.76), 0.45, 0.33, tono=ESCUELA,
           pasos=1.8)
    quieto(lz, PCA3, t, "extra/diego_golpe", 0.215, 0.81, 0.43, flip=True, tono=ESCUELA, fase=1.0)


# ================================================================== 10 · EL PERDÓN (casa de Fer)
P = "perdon"
p0 = t0(P)
p_perd, p_y, p_no, p_era, p_eso = T(P, "perd"), T(P, "y", 1), T(P, "no", 1), T(P, "era", 1, n=1), T(P, "eso", 2)
REJA = p_eso + 2.6
p_fin = t1(P)
snd(p0 + 0.3, "viento", 0.25, dur=p_fin - p0)

PP1 = PF.Plano("casa_fer", p0, p_y - 0.3, z0=1.20, z1=1.30, c0=(0.38, 0.62), c1=(0.35, 0.62), par=(28, 6))


@toma(p0, ("negro", 0.9))
def p1(lz, t):
    PP1.fondo(lz, t)
    quieto(lz, PP1, t, "fer_hoja/03", 0.26, 0.745, 0.31, tono=FRESCO, fase=0.4)
    quieto(lz, PP1, t, "diego14_hoja/03", 0.47, 0.88, 0.43, tono=FRESCO, fase=1.2, flip=True)


PP2 = PF.Plano("casa_fer", p_y - 0.3, p_eso - 0.3, z0=2.4, z1=2.6, c0=(0.47, 0.66), c1=(0.47, 0.665), par=(16, 3))


@toma(p_y - 0.3, ("desenfoque", 0.5))
def p2(lz, t):
    PP2.fondo(lz, t)
    # la voz de su apá: el papá con sus flores aparece como un fantasma detrás de Diego
    g = smooth(prog(t, p_no - 0.2, p_no + 0.8)) * (1 - smooth(prog(t, p_era + 1.2, p_eso - 0.4)))
    if g > 0.01:
        X, Y, h = PP2.en(t, 0.53, 0.88, 0.52)
        PF.actor(lz, "papa_hoja/03", X, Y, h, flip=True, tono=FOCO, op=0.50 * g, suelo=0, sombra=False)
    quieto(lz, PP2, t, "diego14_hoja/03", 0.47, 0.88, 0.43, tono=FRESCO, fase=1.2, flip=True)
    vineta_fuerte(lz, 0.30 + 0.2 * g)


PP3 = PF.Plano("casa_fer", p_eso - 0.3, REJA - 0.2, z0=2.2, z1=2.35, c0=(0.27, 0.57), c1=(0.27, 0.565), par=(16, 3))


@toma(p_eso - 0.3, ("corte", 0.1))
def p3(lz, t):
    PP3.fondo(lz, t)
    quieto(lz, PP3, t, "fer_hoja/03", 0.26, 0.745, 0.31, tono=FRESCO, fase=0.4)


PP4 = PF.Plano("casa_fer", REJA - 0.2, p_fin + 0.6, z0=1.25, z1=1.12, c0=(0.36, 0.62), c1=(0.38, 0.60), par=(28, 6))


@toma(REJA - 0.2, ("fundido", 0.5))
def p4(lz, t):
    PP4.fondo(lz, t)
    op = 1.0 - smooth(prog(t, REJA - 0.6, REJA))
    camino(lz, PP4, t, "fer_hoja/04", REJA - 1.6, REJA - 0.4, (0.27, 0.75), (0.26, 0.73), 0.31, 0.30, tono=FRESCO,
           pasos=1.6, op=op, hasta_despues=False)
    quieto(lz, PP4, t, "diego14_hoja/04", 0.47, 0.88, 0.43, tono=FRESCO, fase=1.2, flip=True)
    petalos(lz, t, n=16, sem=7, color=(0.84, 0.34, 0.60))
    sacudida(lz, t, REJA, 6.0)


# ================================================================== 11 · LAS MUÑECAS (la recámara)
U = "munecas"
u0 = t0(U)
u_otra, u_perd, u_asi, u_no = T(U, "otra", 0), T(U, "perd", 1), T(U, "así", 2), T(U, "no", 3)
u_fin = t1(U)
LAMPARA = (0.555, 0.42)


def recamara(lz, pl, t):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, *LAMPARA)
    PF.brillo(lz, X, Y, 260 * s, color=(1.0, 0.80, 0.45), inten=0.24, t=t * 0.3, sem=8)
    palomillas(lz, X, Y - 20 * s, 40 * s, t, n=2)


PU1 = PF.Plano("recamara_noche", u0, u_otra - 0.3, z0=1.15, z1=1.25, c0=(0.55, 0.58), c1=(0.52, 0.62), par=(24, 5))


@toma(u0, ("negro", 0.9))
def u1(lz, t):
    recamara(lz, PU1, t)
    quieto(lz, PU1, t, "diego14_hoja/04", 0.81, 0.60, 0.40, tono=RECAMARA, fase=1.0, flip=True)
    quieto(lz, PU1, t, "xime9_hoja/00", 0.32, 0.86, 0.27, tono=RECAMARA, fase=0.3, rot=1.2 * math.sin(t * 2.5))


PU2 = PF.Plano("recamara_noche", u_otra - 0.3, u_asi - 0.3, z0=2.4, z1=2.5, c0=(0.33, 0.78), c1=(0.33, 0.78), par=(0, 0))


@toma(u_otra - 0.3, ("desenfoque", 0.5))
def u2(lz, t):
    recamara(lz, PU2, t)
    desenfoque(lz, 6.0)
    lz *= np.float32(0.8)
    # las muñecas en las manos de Xime: hablan cuando «hablan»
    h1 = 0.06 * abs(math.sin(t * 9.0)) * (u_otra - 0.1 < t < u_otra + 1.2)
    h2 = 0.06 * abs(math.sin(t * 9.0)) * (u_perd - 0.1 < t < u_perd + 2.4)
    pega(lz, "utileria_casa/09", W * 0.34, H * (0.56 - h1), H * 0.70, t, u_otra - 0.3, rot=6 * math.sin(t * 1.3), tono=RECAMARA,
         flota=False)
    pega(lz, "utileria_casa/10", W * 0.66, H * (0.58 - h2), H * 0.66, t, u_otra - 0.1, rot=-5 * math.sin(t * 1.1),
         tono=RECAMARA, flota=False)


PU3 = PF.Plano("recamara_noche", u_asi - 0.3, u_no - 0.4, z0=2.2, z1=2.35, c0=(0.33, 0.70), c1=(0.33, 0.70), par=(16, 3))


@toma(u_asi - 0.3, ("corte", 0.1))
def u3(lz, t):
    recamara(lz, PU3, t)
    quieto(lz, PU3, t, "xime9_hoja/01", 0.32, 0.86, 0.27, tono=RECAMARA, fase=0.3)


PU4 = PF.Plano("recamara_noche", u_no - 0.4, u_fin + 0.6, z0=1.55, z1=1.70, c0=(0.40, 0.66), c1=(0.38, 0.68), par=(20, 4))


@toma(u_no - 0.4, ("fundido", 0.5))
def u4(lz, t):
    recamara(lz, PU4, t)
    poses(lz, PU4, t, [(u_no - 1, "xime9_hoja/01", False, 1.0), (u_no + 2.6, "xime9_hoja/02", False, 1.15)], 0.32, 0.86, 0.27,
          tono=RECAMARA, fase=0.3)
    quieto(lz, PU4, t, "diego14b_hoja/00", 0.47, 0.88, 0.34, tono=RECAMARA, fase=1.0, flip=True)


# ================================================================== 12 · EL PATIO (la confesión, el abrazo)
Pa = "patio"
pa0 = t0(Pa)
pa_ama, pa_sabes, pa_debajo, pa_y, pa_tu, pa_el = (T(Pa, "amá", 0), T(Pa, "sabes", 1), T(Pa, "debajo", 1), T(Pa, "y", 2),
                                                   T(Pa, "tú", 3), T(Pa, "él", 3))
pa_fin = t1(Pa)
FOCO_P = (0.265, 0.165)
snd(pa0 + 0.2, "viento", 0.15, dur=pa_fin - pa0)


def patio(lz, pl, t, calor=0.0):
    pl.fondo(lz, t)
    titilan(lz, pl, t, "patio_noche", 0.0, 0.18, "estrella", (0.85, 0.90, 1.0), r=3.0, inten=0.40)
    X, Y, s = pl.P(t, *FOCO_P)
    PF.brillo(lz, X, Y, 300 * s, color=(1.0, 0.82, 0.45), inten=0.26 + 0.12 * calor, t=t * 0.3, sem=9)
    palomillas(lz, X, Y + 8 * s, 70 * s, t, n=5)


PPA1 = PF.Plano("patio_noche", pa0, pa_sabes - 0.3, z0=1.15, z1=1.30, c0=(0.42, 0.62), c1=(0.38, 0.66), par=(26, 5))


@toma(pa0, ("negro", 1.0))
def pa1(lz, t):
    patio(lz, PPA1, t)
    poses(lz, PPA1, t, [(pa0 - 1, "lupe_b_hoja/04", True, 1.0), (pa_ama + 1.2, "lupe_b_hoja/00", False, 1.0)], 0.56, 0.86,
          0.44, tono=PATIO, fase=0.5)
    quieto(lz, PPA1, t, "diego14b_hoja/02", 0.34, 0.86, 0.40, tono=PATIO, fase=1.2, rot=0.8 * math.sin(t * 5.0))


PPA2 = PF.Plano("patio_noche", pa_sabes - 0.3, pa_debajo - 0.3, z0=1.90, z1=2.05, c0=(0.40, 0.68), c1=(0.40, 0.69), par=(18, 4))


@toma(pa_sabes - 0.3, ("fundido", 0.7))
def pa2(lz, t):
    patio(lz, PPA2, t)
    quieto(lz, PPA2, t, "abrazo_hoja/00", 0.40, 0.88, 0.40, tono=PATIO, fase=0.8)


# el recuerdo: el mismo hueco debajo de la mesa, otro niño, hace muchos años (sepia)
PPA3 = PF.Plano("bajo_mesa", pa_debajo - 0.3, pa_y - 0.4, z0=1.30, z1=1.40, c0=(0.42, 0.66), c1=(0.42, 0.67), par=(14, 3))


@toma(pa_debajo - 0.3, ("destello", 0.4))
def pa3(lz, t):
    PPA3.fondo(lz, t)
    quieto(lz, PPA3, t, "diego8_hoja/04", 0.47, 0.86, 0.30, tono=RECUERDO, fase=0.4)
    sepia(lz, 0.85)
    vineta_fuerte(lz, 0.55)


PPA4 = PF.Plano("patio_noche", pa_y - 0.4, pa_el + 0.9, z0=2.65, z1=2.85, c0=(0.40, 0.60), c1=(0.40, 0.595), par=(14, 3))


@toma(pa_y - 0.4, ("destello", 0.4))
def pa4(lz, t):
    patio(lz, PPA4, t, calor=smooth(prog(t, pa_tu, pa_el)))
    quieto(lz, PPA4, t, "abrazo_hoja/02", 0.40, 0.88, 0.40, tono=PATIO, fase=0.8)


PPA5 = PF.Plano("patio_noche", pa_el + 0.9, pa_fin + 0.6, z0=2.0, z1=1.30, c0=(0.40, 0.60), c1=(0.45, 0.55), par=(26, 5))


@toma(pa_el + 0.9, ("fundido", 0.8))
def pa5(lz, t):
    patio(lz, PPA5, t, calor=1.0)
    quieto(lz, PPA5, t, "abrazo_hoja/01", 0.40, 0.89, 0.46, tono=PATIO, fase=0.8, t_in=pa_el + 0.9)
    motas(lz, t, 0.0, 0.0, 1.0, 0.6, n=24, sem=8, color=(1.0, 0.88, 0.60), fuerza=0.25)


# ================================================================== 13 · EL ALBA (orientación · nos bajamos de la rueda)
A = "alba"
a0 = t0(A)
a_toque, a_y, a_nos = T(A, "toqué", 0), T(A, "y", 1), T(A, "nos", 1)
a_fin = t1(A)
ABRE = a_toque + 1.6
snd(a_toque + 0.05, "golpe_suave", 0.35)
snd(a_toque + 0.35, "golpe_suave", 0.35)
snd(a_toque + 0.65, "golpe_suave", 0.35)

PA1 = PF.Plano("orientacion", a0, a_y - 0.3, z0=1.35, z1=1.55, c0=(0.62, 0.56), c1=(0.72, 0.56), par=(24, 5))


@toma(a0, ("fundido", 1.0))
def a1(lz, t):
    PA1.fondo(lz, t)
    toca = a_toque < t < a_toque + 0.9
    quieto(lz, PA1, t, "extra/diego_toca", 0.725, 0.80, 0.44, tono=ALBA, fase=1.0, rot=2.5 * math.sin(t * 22.0) * toca)
    if t >= ABRE:                                    # la orientadora abre: la puerta oscurecida detrás de ella
        quieto(lz, PA1, t, "gente_hoja/03", 0.815, 0.76, 0.42, tono=ALBA, fase=0.2, t_in=ABRE, flip=True)


PA2 = PF.Plano("calle_amanecer", a_y - 0.3, a_fin + 0.6, z0=1.20, z1=1.08, c0=(0.42, 0.62), c1=(0.52, 0.56), par=(32, 7))
VUELO_A = [(a_y + 0.5, 9.0, 0.14, 0.10, 34, 1, 0.2), (a_y + 2.0, 10.0, 0.20, 0.16, 26, 1, 1.1)]
SALEN = a_y + 0.2
snd(a_y, "amanecer", 0.45, dur=4.0)
snd(SALEN + 0.4, "pasos", 0.40, dur=5.0)


@toma(a_y - 0.3, ("fundido", 0.8))
def a2(lz, t):
    PA2.fondo(lz, t)
    titilan(lz, PA2, t, "calle_amanecer", 0.0, 0.12, "estrella", (1.0, 0.95, 0.92), r=3.0, inten=0.30)
    aves(lz, t, VUELO_A, tono=ALBA)
    llega = a_fin + 0.6
    # de lo lejano a lo cercano: Diego, Xime, la mamá con las bolsas
    anda(lz, PA2, t, "diego14_camina", SALEN + 0.0, llega, (0.24, 0.90), (0.60, 0.74), 0.40, 0.21, tono=ALBA,
         desde_antes=True)
    anda(lz, PA2, t, "xime9_camina", SALEN + 0.3, llega, (0.18, 0.93), (0.555, 0.755), 0.30, 0.16, tono=ALBA,
         desde_antes=True)
    anda(lz, PA2, t, "lupe_camina", SALEN + 0.6, llega, (0.10, 0.95), (0.50, 0.77), 0.46, 0.25, tono=ALBA, desde_antes=True)


# ================================================================== 14 · EPÍLOGO (la feria, otro diciembre)
E = "epilogo"
e0_ = t0(E)
e_mira, e_la, e_con = T(E, "mira", 0), T(E, "la", 1), T(E, "conmigo", 2)
TITULO = e_con + 3.2
W_FA = (0.30, 0.30, 0.235, 0.82)              # rueda en feria_atardecer (lote vacío a la IZQUIERDA)
OM_E = 0.12
A0_E = -math.pi / 2 - OM_E * (e_mira + 0.6)
G_EPI = ["gondolas_hoja/02"] + G_VACIAS[1:]
VUELO_E = [(e0_ + 0.3, 10.0, 0.12, 0.08, 34, 1, 0.4), (e_la + 1.0, 10.0, 0.16, 0.12, 28, -1, 1.5)]
snd(e0_ + 0.3, "viento", 0.25, dur=t1(E) - e0_)

PE1 = PF.Plano("feria_atardecer", e0_, e_mira - 0.3, z0=1.12, z1=1.05, c0=(0.48, 0.55), c1=(0.44, 0.52), par=(30, 6))


def feria_tarde(lz, pl, t, gond=G_VACIAS):
    pl.fondo(lz, t)
    titilan(lz, pl, t, "feria_atardecer", 0.40, 0.80, "calido", (1.0, 0.78, 0.40), r=5.0, inten=0.40)
    rueda_en(lz, pl, t, W_FA, A0_E + OM_E * t, gond, tono=OCASO, luces=0.8)


@toma(e0_, ("negro", 1.0))
def e1(lz, t):
    feria_tarde(lz, PE1, t, G_EPI)
    aves(lz, t, VUELO_E, tono=OCASO)
    quieto(lz, PE1, t, "gente_hoja/00", 0.66, 0.80, 0.28, tono=OCASO, fase=0.4)
    quieto(lz, PE1, t, "gente_hoja/05", 0.80, 0.86, 0.33, tono=OCASO, fase=1.2, flip=True, rot=2.0 * math.sin(t * 2.0))
    quieto(lz, PE1, t, "gente_hoja/04", 0.58, 0.88, 0.32, tono=OCASO, fase=0.7)


PE2 = PF.Plano("feria_alta_atardecer", e_mira - 0.3, e_la - 0.3, z0=1.10, z1=1.20, c0=(0.50, 0.55), c1=(0.56, 0.60),
               par=(40, 10))


@toma(e_mira - 0.3, ("desenfoque", 0.5))
def e2(lz, t):
    PE2.fondo(lz, t)
    titilan(lz, PE2, t, "feria_alta_atardecer", 0.60, 1.0, "calido", (1.0, 0.78, 0.40), r=5.0, inten=0.40)
    sw = 2.6 * math.sin(t * 1.1)
    pieza = "gondolas_hoja/02" if t < e_mira + 1.6 else "gondolas_hoja/03"
    PF.actor(lz, pieza, W * 0.42, -H * 0.04, H * 1.12, ancla=(0.5, 0.0), rot=sw, suelo=0, tono=OCASO)


PE3 = PF.Plano("feria_atardecer", e_la - 0.3, TOTAL, z0=1.12, z1=1.0, c0=(0.42, 0.56), c1=(0.45, 0.50), par=(30, 6))


@toma(e_la - 0.3, ("fundido", 0.7))
def e3(lz, t):
    feria_tarde(lz, PE3, t)
    aves(lz, t, VUELO_E, tono=OCASO)
    quieto(lz, PE3, t, "gente_hoja/04", 0.70, 0.86, 0.32, tono=OCASO, fase=0.7)
    quieto(lz, PE3, t, "xime9_hoja/04", 0.47, 0.90, 0.28, tono=OCASO, fase=0.3, flip=True)
    quieto(lz, PE3, t, "diego14b_hoja/04", 0.54, 0.91, 0.40, tono=OCASO, fase=1.1)
    lz *= np.float32(1 - 0.30 * smooth(prog(t, TITULO - 0.8, TITULO + 0.6)))
    PF.rotulo(lz, "NO VUELVE A PASAR", W * 0.5, H * 0.20, 96, t, TITULO, None, rot=-1.5)


TOMAS.sort(key=lambda d: d["t0"])

# tiempos para fx_audio.py (sonidos reales de la biblioteca: la troca, el plato, el puñetazo, la reja…)
FX_T = dict(troca_llega=TROCA_LLEGA, frenon=FRENON, portazo=PORTAZO, radio_off=RADIO_OFF, grito=GRITO, plato=PLATO,
            golpe=GOLPE, reja=REJA, rayo=RAYO, abre=ABRE)


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
        img = D.mezcla_tomas(_cuadro(TOMAS[i - 1], t), np.clip(img, 0, 1), (t - d["t0"]) / dur, tipo)
    img = PF.acabado(np.clip(img, 0, 1), t)
    img = img * smooth(prog(t, 0.0, 0.8)) * (1.0 - smooth(prog(t, TOTAL - 1.6, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SFX:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
