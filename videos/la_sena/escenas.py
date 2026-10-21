# -*- coding: utf-8 -*-
"""«La seña» — corto del taller «Antes de decir que sí» (3.º de secundaria, Jalpa, Zac.). Estilo PEGATINA FLOW (nucleo/pegaflow.py):
escenarios de Flow con cámara y parallax por profundidad; personajes, ciclos y utilería de las hojas de Flow animados como pegatinas.
Guion e intención de cada escena: PLAN_TALLER.md · número → pose de cada pieza: MAPA_PIEZAS.md.
Tramo 2 (20-oct-2026): cuesta, puerta, azotea, gotera + bendición (0:00-1:53). Sin sangre ni armas: la pérdida queda fuera de cuadro.
Tramo 3 (21-oct-2026): tenis, mensaje, recámara, graduación + reja, epílogo en la cuesta (1:53-3:22).
Todo lo que lleva letras (el anuncio del celular, el rótulo) lo dibuja el código: Flow no pone texto."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, e_inout, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


# luz de cada lugar sobre las pegatinas (sin tono parecen pegadas encima)
DORADO = (1.06, 0.93, 0.80)
NOCHE = (0.58, 0.62, 0.90)
FOCO = (1.04, 0.86, 0.66)        # junto al foco de la puerta
COCINA = (1.0, 0.86, 0.70)
MOJADO = (0.84, 0.86, 0.96)
ALBA = (1.0, 0.90, 0.93)

AVES = [f"zanate_vuelo/{i:02d}" for i in range(6)]       # aleteo del zanate

SFX = []


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


# ------------------------------------------------------------------ ayudantes de la toma
def alto(y, hz, k):
    """Altura relativa (al escenario) de un adulto con los pies en y, con el horizonte en hz (perspectiva)."""
    return max(0.02, k * (y - hz))


# Hacia dónde MIRA cada pieza tal como la pintó Flow (+1 derecha, −1 izquierda): lo que se desplaza mira a donde va.
MIRA = {"angel8_bici": 1, "tono13_hoja/00": 1, "papa_camina": 1, "angel14_camina": 1, "tono19b_camina": 1, "perro_camina": 1,
        "gente_hoja/00": 1}


def rumbo(pieza, x0, x1, flip):
    m = MIRA.get(pieza)
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, rot=0.0):
    """Personaje u objeto quieto que respira; si `t_in`, se pega con rebote en ese instante."""
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def poses(lz, pl, t, cambios, x, y, frac, tono=None, fase=0.0):
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
    PF.actor(lz, pieza, X, Y, h * (0.92 + 0.08 * u), flip=fl, tono=tono, sy=PF.respira(t, fase=fase), rot=(1 - u) * 4)


def camino(lz, pl, t, pieza, ta, tb, p0, p1, f0, f1, flip=False, tono=None, pasos=2.2, salto=0.035, op=1.0,
           desde_antes=True):
    """Títere de papel que avanza en diagonal (una cuesta, una calle que se aleja): la posición y el tamaño se interpolan."""
    if t < ta and not desde_antes:
        return
    flip = rumbo(pieza, p0[0], p1[0], flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    X, Y, h = pl.en(t, lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(f0, f1, u))
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    bote = abs(math.sin(ph)) if mov else 0.0
    PF.actor(lz, pieza, X, Y - bote * salto * h, h, flip=flip, tono=tono, rot=3.0 * math.sin(ph) if mov else 0.0, op=op,
             sy=PF.respira(t))


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
    """Pegatina en pantalla (un recuerdo, un objeto soñado): entra con rebote, flota y se despega."""
    if t < t_in or (t_out is not None and t > t_out + 0.35):
        return
    u = PF.entra(t, t_in, 0.45)
    s = 1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + 0.35))
    dy = 6.0 * math.sin(1.4 * t) if flota else 0.0
    PF.actor(lz, pieza, X, Y + dy, hpx * (0.55 + 0.45 * u) * (0.6 + 0.4 * s), rot=rot + (1 - u) * 10, ancla=(0.5, 0.5),
             suelo=0, tono=tono, op=op * clamp01(u * 3) * s)


def bici(lz, pl, t, tramos, f_k, hz, k, tono=None):
    """Ángel (8) en la bici que baja la cuesta: tramos = [(ta, tb, (x0, y0), (x1, y1), potencia)]; pedaleo por tiempo."""
    for ta, tb, p0, p1, pot in tramos:
        if ta <= t < tb or (t < ta and ta == tramos[0][0]):
            u = clamp01((t - ta) / (tb - ta)) ** pot
            x, y = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
            X, Y, h = pl.en(t, x, y, alto(y, hz, k) * f_k)
            i = int(t * 7) % 6 if t >= tramos[0][0] else 0
            PF.actor(lz, f"angel8_bici/{i:02d}", X, Y, h, flip=rumbo("angel8_bici", p0[0], p1[0], False), tono=tono,
                     rot=2.0 * math.sin(t * 8.0))
            return


def _blend(lz, a, op=1.0):
    """Mezcla una capa RGBA float (H, W, 4) de pantalla sobre lz."""
    al = a[..., 3:4] * op
    lz[:] = lz * (1 - al) + a[..., :3] * al


def pegar_rgba(lz, img, X, Y, escala=1.0, rot=0.0, op=1.0):
    """Imagen RGBA float centrada en (X, Y) de pantalla con escala y giro."""
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, escala)
    M[0, 2] += X - w / 2
    M[1, 2] += Y - h / 2
    capa = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    _blend(lz, capa, op)


def palomillas(lz, X, Y, r, t, n=6):
    """Palomillas que dan vueltas al foco."""
    for i in range(n):
        a = t * (2.2 + 0.4 * i) + i * 1.7
        px = X + r * (0.6 + 0.3 * math.sin(t * 1.3 + i)) * math.cos(a)
        py = Y + r * 0.6 * math.sin(a * 1.3)
        cv2.circle(lz, (int(px), int(py)), 2 + (i % 2), (0.95, 0.92, 0.78), -1, cv2.LINE_AA)


def lluvia_ventana(lz, pl, t, x0, y0, x1, y1, n=46):
    """Gotas que escurren por el vidrio (rectángulo del escenario) y lluvia que se ve detrás."""
    X0, Y0, _ = pl.P(t, x0, y0)
    X1, Y1, _ = pl.P(t, x1, y1)
    if X1 - X0 < 4 or Y1 - Y0 < 4:
        return
    capa = lz.copy()
    alto_v = Y1 - Y0
    rng = np.random.RandomState(7)
    for i in range(n):
        x = X0 + rng.rand() * (X1 - X0)
        v = 0.9 + rng.rand() * 1.4
        y = Y0 + ((rng.rand() + t * v) % 1.0) * alto_v
        L = alto_v * (0.06 + 0.10 * rng.rand())
        cv2.line(capa, (int(x), int(y)), (int(x - 0.12 * L), int(y + L)), (0.80, 0.85, 0.95), 1, cv2.LINE_AA)
    m = np.zeros(lz.shape[:2], np.float32)
    m[int(max(Y0, 0)):int(min(Y1, H)), int(max(X0, 0)):int(min(X1, W))] = 0.55
    lz[:] = lz * (1 - m[..., None]) + capa * m[..., None]


def gotera(lz, pl, t, x, y_techo, y_agua, t_ini, per=1.3):
    """Gota que cae del techo a la cubeta cada `per` s y abre un anillo en el agua."""
    if t < t_ini:
        return
    ph = ((t - t_ini) % per) / per
    caida = 0.36
    Xa, Ya, s = pl.P(t, x, y_agua)
    if ph < caida:
        u = (ph / caida) ** 2
        Xg, Yg, _ = pl.P(t, x, lerp(y_techo, y_agua, u))
        cv2.ellipse(lz, (int(Xg), int(Yg)), (max(2, int(3 * s)), max(3, int(6 * s))), 0, 0, 360, (0.82, 0.88, 0.98), -1,
                    cv2.LINE_AA)
    else:
        u = (ph - caida) / (1 - caida)
        r = 4 + 34 * s * u
        c = (0.85, 0.90, 1.0)
        capa = lz.copy()
        cv2.ellipse(capa, (int(Xa), int(Ya)), (int(r), max(1, int(r * 0.32))), 0, 0, 360, c, max(1, int(2 * s)), cv2.LINE_AA)
        a = 0.7 * (1 - u)
        lz[:] = lz * (1 - a) + capa * a


def impactos(t_ini, t_fin, per=1.3):
    """Tiempos en que la gota toca el agua (para el sonido)."""
    out, k = [], 0
    while t_ini + (k + 0.36) * per < t_fin:
        out.append(t_ini + (k + 0.36) * per)
        k += 1
    return out


_YY = np.linspace(0, 1, H, dtype=np.float32)[:, None]
_XX = np.linspace(0, 1, W, dtype=np.float32)[None, :]


def neblina(lz, t, y0, y1, fuerza=0.35, color=(0.97, 0.93, 0.95)):
    """Banda de neblina del cañón que deriva despacio."""
    banda = np.clip(1 - np.abs((_YY - (y0 + y1) / 2) / ((y1 - y0) / 2)), 0, 1) ** 1.5
    ondas = 0.75 + 0.25 * np.sin(_XX * 9.0 + t * 0.35) * np.sin(_XX * 3.1 - t * 0.21 + 1.0)
    a = (banda * ondas * fuerza)[..., None]
    lz[:] = lz * (1 - a) + np.float32(color) * a


# ------------------------------------------------------------------ el celular (todo dibujado por código)
_FN = D.FUENTES


def _fnt(k, px):
    return ImageFont.truetype(_FN[k], max(8, int(px)))


@functools.lru_cache(maxsize=24)
def _cel(alto_px, escrito="", enviado=False):
    """Celular con el anuncio de «trabajo» y la caja de mensaje → RGBA float (alto_px, alto_px/2, 4)."""
    w = alto_px // 2
    s = w / 100.0
    im = Image.new("RGBA", (w, alto_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    R = int(13 * s)
    d.rounded_rectangle([0, 0, w - 1, alto_px - 1], R, fill=(22, 22, 26, 255))
    m = int(4.5 * s)
    x0, y0, x1, y1 = m, m, w - 1 - m, alto_px - 1 - m
    d.rounded_rectangle([x0, y0, x1, y1], int(R * 0.75), fill=(234, 236, 241, 255))
    d.rectangle([x0, y0 + 9 * s, x1, y0 + 20 * s], fill=(255, 255, 255, 255))
    d.text((x0 + 5 * s, y0 + 11.5 * s), "Ofertas de empleo · región", font=_fnt("sans", 4.6 * s), fill=(70, 74, 84, 255))
    cy = y0 + 25 * s
    d.rounded_rectangle([x0 + 4 * s, cy, x1 - 4 * s, cy + 90 * s], int(3 * s), fill=(255, 255, 255, 255))
    d.ellipse([x0 + 8 * s, cy + 4 * s, x0 + 17 * s, cy + 13 * s], fill=(120, 124, 134, 255))
    d.text((x0 + 20 * s, cy + 4.5 * s), "Chamba Ya", font=_fnt("sans_b", 4.6 * s), fill=(30, 30, 36, 255))
    d.text((x0 + 20 * s, cy + 9.8 * s), "hace 2 h", font=_fnt("sans_l", 3.6 * s), fill=(130, 130, 140, 255))
    yy = cy + 19 * s
    for txt, f, px, col in (("SE SOLICITAN", "sans_b", 8.4, (20, 20, 24)), ("JÓVENES", "sans_b", 11.5, (20, 20, 24)),
                            ("$4,000 A LA SEMANA", "sans_b", 6.4, (22, 140, 60)), ("Hospedaje y comida", "sans", 5.4, (40, 40, 48)),
                            ("Sin experiencia", "sans", 5.4, (40, 40, 48)), ("Manda inbox", "sans_b", 5.8, (190, 30, 30))):
        d.text((x0 + 9 * s, yy), txt, font=_fnt(f, px * s), fill=col + (255,))
        yy += px * s * 1.38
    if enviado:
        bx1 = x1 - 6 * s
        d.rounded_rectangle([bx1 - 20 * s, y1 - 40 * s, bx1, y1 - 29 * s], int(5 * s), fill=(40, 110, 230, 255))
        d.text((bx1 - 15 * s, y1 - 38.5 * s), "info", font=_fnt("sans", 5.2 * s), fill=(255, 255, 255, 255))
    iy = y1 - 21 * s
    d.rounded_rectangle([x0 + 4 * s, iy, x1 - 18 * s, iy + 13 * s], int(6 * s), fill=(255, 255, 255, 255),
                        outline=(200, 200, 210, 255), width=max(1, int(0.5 * s)))
    if escrito:
        d.text((x0 + 9 * s, iy + 3.2 * s), escrito + "|", font=_fnt("sans", 5.2 * s), fill=(30, 30, 36, 255))
    elif not enviado:
        d.text((x0 + 9 * s, iy + 3.2 * s), "Escribe un mensaje…", font=_fnt("sans", 4.8 * s), fill=(150, 150, 160, 255))
    d.ellipse([x1 - 15 * s, iy, x1 - 3 * s, iy + 13 * s], fill=(40, 110, 230, 255))
    d.polygon([(x1 - 11.5 * s, iy + 3.5 * s), (x1 - 5.5 * s, iy + 6.5 * s), (x1 - 11.5 * s, iy + 9.5 * s)], fill=(255, 255, 255, 255))
    return np.asarray(im, np.float32) / 255.0


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


# ================================================================== 1 · LA CUESTA (hace 6 años)
C = "cuesta"
c_solto, c_cuando, c_pero = T(C, "solt", 1), T(C, "cuando", 2), T(C, "pero", 2)
c_ya, c_si = T(C, "ya", 3), T(C, "sí", 3)
c_ese, c_dos, c_luego, c_viendo = T(C, "ese", 4), T(C, "dos", 4), T(C, "luego", 4), T(C, "viendo", 5)
c_fin = _ESC[C]["t1"]
HZC, KC = 0.28, 0.52                  # horizonte y escala de cuesta_tarde (puerta turquesa = 0,31 a y 0,78)
HZB, KB = 0.28, 0.55                  # cuesta_tarde_b (la cuesta vista desde abajo)
SUELTA, CHOCA = 4.0, 9.0              # Toño suelta la bici · Ángel cae en la arena

P1 = PF.Plano("cuesta_tarde", 0.0, 5.0, z0=1.30, z1=1.10, c0=(0.50, 0.32), c1=(0.50, 0.60), par=(30, 6))
VUELO1 = [(0.3, 9.0, 0.14, 0.09, 46, 1, 0.0), (1.6, 10.0, 0.20, 0.15, 34, 1, 1.3), (5.0, 9.0, 0.11, 0.07, 40, -1, 2.1)]
FG_CUESTA = [("naturaleza/06", 0.96, 1.04, 0.22, 1.30, True), ("naturaleza/06", 0.03, 1.05, 0.18, 1.35, False)]
BICI = [(1.0, SUELTA, (0.53, 0.565), (0.51, 0.665), 1.0), (SUELTA, CHOCA, (0.51, 0.665), (0.385, 0.875), 1.5)]
snd(0.2, "viento", 0.35, dur=6.0)
snd(1.0, "pasos", 0.45, dur=3.0)
snd(CHOCA, "arena", 0.8, dur=1.0)
snd(CHOCA + 0.05, "golpe_suave", 0.7)


@toma(0.0)
def s1(lz, t):
    P1.fondo(lz, t)
    aves(lz, t, VUELO1)
    PF.arena_viento(lz, t, fuerza=0.25 + 0.9 * smooth(prog(t, CHOCA - 0.1, CHOCA + 0.2)) * (1 - smooth(prog(t, CHOCA + 0.4, CHOCA + 1.6))),
                    y0=0.70, sem=1, color=(0.98, 0.84, 0.58))
    if t < SUELTA:
        camino(lz, P1, t, "tono13_hoja/00", 1.0, SUELTA, (0.555, 0.558), (0.535, 0.658),
               alto(0.558, HZC, KC) * 0.88, alto(0.658, HZC, KC) * 0.88, tono=DORADO, pasos=2.6)
    else:
        quieto(lz, P1, t, "tono13_hoja/01", 0.535, 0.658, alto(0.658, HZC, KC) * 0.88, tono=DORADO, t_in=SUELTA)
    if t < CHOCA:
        bici(lz, P1, t, BICI, 0.60, HZC, KC, tono=DORADO)


P2 = PF.Plano("cuesta_tarde_b", c_cuando - 0.3, c_ya, z0=1.55, z1=1.12, c0=(0.70, 0.80), c1=(0.60, 0.58), par=(28, 6))
snd(c_cuando - 0.2, "suspiro", 0.25)


@toma(c_cuando - 0.3, ("desenfoque", 0.5))
def s2(lz, t):
    P2.fondo(lz, t)
    aves(lz, t, [(c_cuando, 8.0, 0.10, 0.06, 40, -1, 0.7)])
    X, Y, h = P2.en(t, 0.62, 0.975, 0.11)
    PF.actor(lz, "utileria_casa/08", X, Y, h, rot=18, tono=DORADO, suelo=0.25)
    quieto(lz, P2, t, "angel8_hoja/00", 0.765, 0.975, alto(0.99, HZB, KB) * 0.70, tono=DORADO)
    quieto(lz, P2, t, "tono13_hoja/01", 0.47, 0.47, alto(0.47, HZB, KB) * 0.88, tono=DORADO, fase=1.0)
    plantas(lz, P2, t, [("naturaleza/06", 0.04, 1.05, 0.20, 1.3, False)], tono=DORADO)


P3 = PF.Plano("cuesta_tarde_b", c_ya - 0.3, c_ese, z0=1.25, z1=1.42, c0=(0.58, 0.62), c1=(0.74, 0.78), par=(28, 6))
snd(c_ya - 0.25, "pasos", 0.7, dur=2.2)


@toma(c_ya - 0.3, ("latigo", 0.4))
def s3(lz, t):
    P3.fondo(lz, t)
    X, Y, h = P3.en(t, 0.62, 0.975, 0.11)
    PF.actor(lz, "utileria_casa/08", X, Y, h, rot=18, tono=DORADO, suelo=0.25)
    quieto(lz, P3, t, "angel8_hoja/00", 0.765, 0.975, alto(0.99, HZB, KB) * 0.70, tono=DORADO)
    tb = c_ya + 2.0
    camino(lz, P3, t, "tono13_hoja/01", c_ya - 0.3, tb, (0.48, 0.48), (0.66, 0.95),
           alto(0.48, HZB, KB) * 0.88, alto(0.93, HZB, KB) * 0.88, tono=DORADO, pasos=3.4, salto=0.05)
    PF.arena_viento(lz, t, fuerza=0.35, y0=0.78, sem=3, color=(0.98, 0.84, 0.58))


P4 = PF.Plano("cuesta_tarde", c_ese - 0.3, c_fin, z0=1.75, z1=1.32, c0=(0.50, 0.80), c1=(0.50, 0.70), par=(26, 5))
VUELO4 = [(c_viendo, 6.5, 0.16, 0.08, 52, 1, 0.3), (c_viendo + 0.8, 7.0, 0.22, 0.15, 40, 1, 1.9)]
snd(c_dos, "papel", 0.5)
snd(c_luego, "papel", 0.5)
snd(c_viendo + 0.1, "papel", 0.7)


@toma(c_ese - 0.3, ("fundido", 0.6))
def s4(lz, t):
    P4.fondo(lz, t)
    aves(lz, t, VUELO4)
    PF.arena_viento(lz, t, fuerza=0.25, y0=0.80, sem=4, color=(0.98, 0.84, 0.58))
    yA, yT = 0.985, 0.985
    poses(lz, P4, t, [(c_ese - 0.3, "angel8_hoja/05", False, 1.0), (c_dos, "angel8_hoja/01", False, 1.0),
                      (c_luego, "angel8_hoja/02", True, 1.0)], 0.44, yA, alto(yA, HZC, KC) * 0.62, tono=DORADO)
    poses(lz, P4, t, [(c_ese - 0.3, "tono13_hoja/04", False, 1.0), (c_dos + 0.15, "tono13_hoja/02", False, 1.0),
                      (c_luego + 0.1, "tono13_hoja/03", False, 1.0)], 0.585, yT, alto(yT, HZC, KC) * 0.88, tono=DORADO, fase=1.3)
    plantas(lz, P4, t, FG_CUESTA, tono=DORADO)
    PF.rotulo(lz, "TE ESTOY VIENDO", W * 0.5, H * 0.15, 64, t, c_viendo + 0.05, c_fin - 0.6, rot=-1.5)


# ================================================================== 2 · LA PUERTA (ese mismo año)
Pu = "puerta"
p0 = _ESC[Pu]["t0"]
p_te, p_tono, p_desde, p_fue = T(Pu, "te", 1), T(Pu, "toño", 2), T(Pu, "desde", 2), T(Pu, "fue", 2)
p_fin = _ESC[Pu]["t1"]
FOCO_XY = (0.333, 0.115)


def foco(lz, pl, t):
    X, Y, s = pl.P(t, *FOCO_XY)
    PF.brillo(lz, X, Y, 260 * s, color=(1.0, 0.78, 0.40), inten=0.30 + 0.03 * math.sin(t * 13.0), t=t, sem=2)
    palomillas(lz, X, Y, 40 * s, t)


PQ1 = PF.Plano("puerta_noche", p0, p_te, z0=1.12, z1=1.24, c0=(0.42, 0.52), c1=(0.38, 0.56), par=(24, 5))
snd(p0 + 0.3, "viento", 0.25, dur=5.0)


@toma(p0 - 0.4, ("negro", 0.8))
def q1(lz, t):
    PQ1.fondo(lz, t)
    foco(lz, PQ1, t)
    poses(lz, PQ1, t, [(p0 - 0.4, "papa_hoja/00", False, 1.0), (p0 + 2.6, "papa_hoja/02", False, 1.0)], 0.47, 0.725, 0.39,
          tono=FOCO)
    quieto(lz, PQ1, t, "angel8_hoja/04", 0.335, 0.718, 0.27, tono=FOCO, fase=0.7)
    quieto(lz, PQ1, t, "tono13_hoja/04", 0.24, 0.715, 0.34, flip=True, tono=FOCO, fase=1.9)


PQ2 = PF.Plano("puerta_noche", p_te - 0.3, p_tono, z0=1.85, z1=1.95, c0=(0.34, 0.58), c1=(0.34, 0.56), par=(22, 4))


@toma(p_te - 0.3, ("desenfoque", 0.45))
def q2(lz, t):
    PQ2.fondo(lz, t)
    foco(lz, PQ2, t)
    quieto(lz, PQ2, t, "angel8_hoja/04", 0.45, 0.735, 0.27, tono=FOCO, fase=0.7)
    quieto(lz, PQ2, t, "tono13_hoja/04", 0.37, 0.73, 0.34, flip=True, tono=FOCO, fase=1.9)
    quieto(lz, PQ2, t, "papa_hoja/03", 0.27, 0.74, 0.40, tono=FOCO)


PQ3 = PF.Plano("puerta_noche", p_tono - 0.3, p_fin, z0=1.02, z1=1.30, c0=(0.56, 0.56), c1=(0.33, 0.58), par=(24, 5))
snd(p_tono - 0.2, "pasos", 0.35, dur=4.5)
snd(p_desde + 0.6, "whoosh", 0.25, dur=1.6)


@toma(p_tono - 0.3, ("fundido", 0.6))
def q3(lz, t):
    PQ3.fondo(lz, t)
    foco(lz, PQ3, t)
    ta, tb = p_tono - 0.3, p_fue + 0.2
    u = clamp01((t - ta) / (tb - ta))
    camino(lz, PQ3, t, "papa_hoja/01", ta, tb, (0.47, 0.78), (0.80, 0.615), 0.40, 0.11, tono=NOCHE, pasos=1.8,
           op=1.0 - smooth(prog(t, tb - 0.8, tb)))
    if t > p_desde:                                    # la troca que se lo lleva: luces que se van
        v = smooth(prog(t, p_desde, p_desde + 0.8)) * (1 - smooth(prog(t, p_fue, p_fue + 1.2)))
        X, Y, s = PQ3.P(t, lerp(0.84, 0.97, smooth(prog(t, p_desde + 0.6, p_fue + 1.2))), 0.605)
        PF.brillo(lz, X, Y, 120 * s, color=(1.0, 0.92, 0.70), inten=0.55 * v, t=t, sem=5)
        PF.brillo(lz, X + 22 * s, Y, 120 * s, color=(1.0, 0.92, 0.70), inten=0.45 * v, t=t, sem=6)
    quieto(lz, PQ3, t, "tono13_hoja/04", 0.27, 0.715, 0.34, flip=True, tono=FOCO, fase=1.9)
    quieto(lz, PQ3, t, "angel8_hoja/04", 0.345, 0.72, 0.27, tono=FOCO, fase=0.7)


# ================================================================== 3 · LA AZOTEA (hoy)
A = "azotea"
a0 = _ESC[A]["t0"]
a_ahora, a_casi, a_mi = T(A, "ahora", 0), T(A, "casi", 1), T(A, "mi", 1)
a_yo, a_papel = T(A, "yo", 2), T(A, "papel", 3)
a_y, a_pos, a_cuesta, a_ya = T(A, "y", 4), T(A, "pos", 5), T(A, "cuesta", 5), T(A, "ya", 6)
a_fin = _ESC[A]["t1"]
XA, XT, YS = 0.40, 0.585, 0.862          # Ángel y Toño sentados en la orilla de la azotea
FA, FT = 0.235, 0.26


def los_dos(lz, pl, t, toño=None):
    quieto(lz, pl, t, "angel14_hoja/00", XA, YS, FA, tono=DORADO, fase=0.4)
    X, Y, h = pl.en(t, 0.492, 0.872, 0.034)
    PF.actor(lz, "utileria_casa/06", X, Y, h, tono=DORADO, suelo=0.25)
    X, Y, h = pl.en(t, 0.515, 0.878, 0.038)
    PF.actor(lz, "utileria_casa/07", X, Y, h, tono=DORADO, suelo=0.25)
    poses(lz, pl, t, toño or [(a0 - 1, "tono19_hoja/00", False, 1.0)], XT, YS + 0.004, FT, tono=DORADO, fase=1.6)


def sol(lz, pl, t, k=1.0):
    X, Y, s = pl.P(t, 0.86, 0.33)
    PF.brillo(lz, X, Y, 420 * s, color=(1.0, 0.70, 0.35), inten=0.22 * k, t=t, sem=8)


PA1 = PF.Plano("azotea_atardecer", a0, a_casi, z0=1.40, z1=1.08, c0=(0.30, 0.40), c1=(0.50, 0.66), par=(30, 6))
VUELOA = [(a0 + 0.3, 9.0, 0.12, 0.08, 44, -1, 0.2), (a0 + 1.4, 10.0, 0.18, 0.13, 32, -1, 1.1)]
snd(a0 + 0.2, "viento", 0.25, dur=6.0)
snd(a_ahora + 0.4, "papel", 0.55)


@toma(a0, ("fundido", 0.7))
def a1(lz, t):
    PA1.fondo(lz, t)
    sol(lz, PA1, t)
    aves(lz, t, VUELOA, tono=DORADO)
    los_dos(lz, PA1, t)
    X, Y, h = PA1.en(t, XT, YS, FT)
    PF.rotulo(lz, "TOÑO · 19", X, Y - h * 1.25, 44, t, a_ahora + 0.4, a_casi - 0.5, rot=2.0)


PA2 = PF.Plano("azotea_atardecer", a_casi - 0.3, a_yo, z0=1.65, z1=1.75, c0=(0.49, 0.74), c1=(0.50, 0.72), par=(26, 5))
snd(a_mi, "papel", 0.6)


@toma(a_casi - 0.3, ("desenfoque", 0.5))
def a2(lz, t):
    PA2.fondo(lz, t)
    sol(lz, PA2, t)
    los_dos(lz, PA2, t)
    pega(lz, "utileria_casa/04", W * 0.80, H * 0.26, H * 0.30, t, a_mi - 0.1, a_yo - 0.6, rot=4.0, tono=(1.0, 0.93, 0.84),
         op=0.92)


PA3 = PF.Plano("azotea_atardecer", a_yo - 0.3, a_y, z0=2.65, z1=2.35, c0=(0.585, 0.76), c1=(0.55, 0.74), par=(24, 4))
snd(a_papel, "pop", 0.6)
snd(a_papel + 0.05, "brillo", 0.5)


@toma(a_yo - 0.3, ("latigo", 0.4))
def a3(lz, t):
    PA3.fondo(lz, t)
    sol(lz, PA3, t)
    los_dos(lz, PA3, t)
    if t > a_papel - 0.1:
        X, Y, s = PA3.P(t, 0.49, 0.62)
        PF.brillo(lz, X, Y, 230 * s, color=(1.0, 0.86, 0.45), inten=0.35 * PF.entra(t, a_papel, 0.5), t=t, sem=9)
        pega(lz, "utileria_casa/05", X, Y, H * 0.16, t, a_papel, None, rot=-8.0, tono=DORADO)


PA4 = PF.Plano("azotea_atardecer", a_y - 0.3, a_ya, z0=2.05, z1=2.15, c0=(0.47, 0.77), c1=(0.48, 0.76), par=(26, 5))
snd(a_pos, "pop", 0.35)


@toma(a_y - 0.3, ("desenfoque", 0.45))
def a4(lz, t):
    PA4.fondo(lz, t)
    sol(lz, PA4, t)
    los_dos(lz, PA4, t, [(a_y - 0.3, "tono19_hoja/00", False, 1.0), (a_pos - 0.1, "tono19_hoja/01", True, 1.0),
                         (a_cuesta + 0.2, "tono19_hoja/00", False, 1.0)])
    X, Y, s = PA4.P(t, 0.49, 0.64)                     # el «papel» soñado se despega cuando Toño bromea
    pega(lz, "utileria_casa/05", X, Y, H * 0.13, t, a_y - 1.0, a_pos - 0.4, rot=-8.0, tono=DORADO)


PA5 = PF.Plano("azotea_atardecer", a_ya - 0.3, a_fin, z0=1.10, z1=1.45, c0=(0.50, 0.64), c1=(0.33, 0.36), par=(30, 6))
VUELO5 = [(a_ya + 1.0, 8.0, 0.30, 0.20, 40, -1, 0.5), (a_ya + 2.2, 8.5, 0.26, 0.18, 30, -1, 1.5),
          (a_ya + 3.6, 7.5, 0.34, 0.24, 36, -1, 2.4)]


@toma(a_ya - 0.3, ("fundido", 0.5))
def a5(lz, t):
    PA5.fondo(lz, t)
    k = smooth(prog(t, a_ya + 2.0, a_fin))
    sol(lz, PA5, t, 1.0 - 0.6 * k)
    aves(lz, t, VUELO5, tono=DORADO)
    los_dos(lz, PA5, t)
    lz *= np.float32([lerp(1.0, 0.80, k), lerp(1.0, 0.68, k), lerp(1.0, 0.82, k)])       # cae la tarde


# ================================================================== 4 · LA GOTERA (sin voz) + LA BENDICIÓN
B = "bendicion"
b0 = _ESC[B]["t0"]
b_que, b_dijo, b_jal = T(B, "que", 0), T(B, "dijo", 1), T(B, "jalisco", 1)
b_fin = _ESC[B]["t1"]
G1, G2, G3, G4, G5, G6, G7 = b0, b0 + 5.8, b0 + 11.4, b0 + 16.2, b0 + 18.0, b0 + 19.9, b0 + 23.1
ESCRIBE, ENVIA = G6 + 0.4, G6 + 2.2
VENTANA = (0.535, 0.262, 0.662, 0.402)
GOTA = (0.697, 0.065, 0.655)                   # x, techo, agua de la cubeta (cocina_noche_lluvia_a)
ROSA_MESA = (0.24, 0.672, 0.23)               # Rosa dormida recargada en la mesa pintada (pieza sin su mesa)
MESA_X1 = 0.47
TONO_SILLA = (0.555, 0.965, 0.45)              # Toño sentado con el celular (la pieza trae su silla)

snd(G1 + 0.2, "lluvia", 0.35, dur=G7 - G1 + 0.5)
for ti in impactos(G1, G7):
    snd(ti, "gota", 0.55)
snd(G3 + 0.4, "pin", 0.6)
snd(ESCRIBE, "escribir", 0.5, dur=1.4)
snd(ENVIA, "whoosh", 0.45, dur=0.4)


def cocina(lz, pl, t, toño=True, rosa=True):
    pl.fondo(lz, t)
    base = lz.copy()
    lluvia_ventana(lz, pl, t, *VENTANA)
    X, Y, s = pl.P(t, 0.47, 0.03)
    PF.brillo(lz, X, Y, 340 * s, color=(1.0, 0.80, 0.45), inten=0.20 + 0.02 * math.sin(t * 11.0), t=t, sem=3)
    gotera(lz, pl, t, GOTA[0], GOTA[1], GOTA[2], G1)
    if rosa:
        quieto(lz, pl, t, "rosa_hoja/01c", ROSA_MESA[0], ROSA_MESA[1], ROSA_MESA[2], tono=COCINA, fase=0.3)
        X0, Yc, _ = pl.P(t, 0.0, ROSA_MESA[1])          # la cubierta de la mesa tapa el corte (los codos) de la pieza
        X1, _, _ = pl.P(t, MESA_X1, ROSA_MESA[1])
        y0, x0, x1 = int(np.clip(Yc - 3, 0, H)), int(np.clip(X0, 0, W)), int(np.clip(X1, 0, W))
        lz[y0:, x0:x1] = base[y0:, x0:x1]
    if toño:
        quieto(lz, pl, t, "tono19_hoja/03", TONO_SILLA[0], TONO_SILLA[1], TONO_SILLA[2], tono=COCINA)


PG1 = PF.Plano("cocina_noche_lluvia", G1, G2, z0=1.10, z1=1.20, c0=(0.50, 0.55), c1=(0.52, 0.58), par=(22, 4))


@toma(G1 - 0.6, ("negro", 1.0))
def g1(lz, t):
    cocina(lz, PG1, t)


PG2 = PF.Plano("cocina_noche_lluvia", G2, G3, z0=1.70, z1=1.82, c0=(0.55, 0.70), c1=(0.53, 0.70), par=(20, 4))


@toma(G2, ("desenfoque", 0.5))
def g2(lz, t):
    cocina(lz, PG2, t)
    X, Y, h = PG2.en(t, *TONO_SILLA)
    PF.brillo(lz, X - 0.20 * h, Y - 0.50 * h, 0.45 * h, color=(0.55, 0.75, 1.0), inten=0.30 + 0.05 * math.sin(t * 3), t=t, sem=4)


PG_FONDO = PF.Plano("cocina_noche_lluvia", G3, G7, z0=1.50, z1=1.56, c0=(0.55, 0.62), c1=(0.55, 0.62), par=(0, 0))


def celular(lz, t, escrito="", enviado=False, t_in=None):
    PG_FONDO.fondo(lz, t)
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 14) * np.float32(0.55)
    hpx = int(H * 0.92) // 2 * 2
    u = 1.0 if t_in is None else PF.entra(t, t_in, 0.5)
    pegar_rgba(lz, _cel(hpx, escrito, enviado), W * 0.5, H * 0.52 + (1 - u) * 60, escala=0.94 + 0.06 * u,
               rot=0.8 * math.sin(t * 1.7), op=clamp01(u * 2))
    X, Y = W * 0.5, H * 0.50
    PF.brillo(lz, X, Y, H * 0.55, color=(0.55, 0.75, 1.0), inten=0.08, t=t, sem=7)


@toma(G3, ("corte", 0.1))
def g3(lz, t):
    celular(lz, t, t_in=G3 + 0.3)


PG4 = PF.Plano("cocina_noche_lluvia", G4, G5, z0=2.7, z1=2.85, c0=(0.70, 0.60), c1=(0.70, 0.61), par=(14, 3))


@toma(G4, ("corte", 0.1))
def g4(lz, t):
    cocina(lz, PG4, t, toño=False, rosa=False)


PG5 = PF.Plano("cocina_noche_lluvia", G5, G6, z0=2.25, z1=2.35, c0=(0.25, 0.56), c1=(0.26, 0.56), par=(14, 3))


@toma(G5, ("corte", 0.1))
def g5(lz, t):
    cocina(lz, PG5, t, toño=False)


@toma(G6, ("corte", 0.1))
def g6(lz, t):
    n = int(clamp01((t - ESCRIBE) / 1.2) * 4)
    celular(lz, t, escrito="info"[:n] if t < ENVIA else "", enviado=t >= ENVIA)


# --- amanecer en la parada de la carretera 54
PB1 = PF.Plano("parada_amanecer", G7, b_dijo, z0=2.2, z1=2.3, c0=(0.50, 0.66), c1=(0.51, 0.66), par=(20, 4))
snd(G7 + 0.3, "amanecer", 0.5, dur=3.0)
snd(G7 + 0.5, "viento", 0.3, dur=6.0)


def desenfocado(lz, pieza, X, Y, hpx, sigma=8.0, tono=None):
    """Pieza muy cerca de la cámara, fuera de foco (primer plano que tapa)."""
    capa = lz.copy()
    PF.actor(capa, pieza, X, Y, hpx, suelo=0, tono=tono)
    m = cv2.GaussianBlur((np.abs(capa - lz).max(-1) > 0.004).astype(np.float32), (0, 0), sigma)[..., None]
    lz[:] = lz * (1 - m) + cv2.GaussianBlur(capa, (0, 0), sigma) * m


@toma(G7, ("negro", 1.0))
def b1(lz, t):
    PB1.fondo(lz, t)
    neblina(lz, t, 0.30, 0.60, 0.30)
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 2.5)
    h = H * lerp(1.80, 1.92, clamp01((t - G7) / (b_dijo - G7)))
    PF.actor(lz, "rosa_hoja/02", W * 0.40, H * 0.05 + h, h, tono=ALBA, suelo=0, sy=PF.respira(t))
    desenfocado(lz, "naturaleza/09", W * 0.655, H * 1.15, H * 2.3, sigma=9.0, tono=ALBA)


PB2 = PF.Plano("parada_amanecer", b_dijo - 0.3, b_fin, z0=1.25, z1=1.40, c0=(0.45, 0.70), c1=(0.48, 0.72), par=(28, 6))
SALE, LLEGA = b_dijo, b_jal + 1.2                      # Toño camina a la orilla de la carretera
snd(b_jal + 0.4, "whoosh", 0.5, dur=1.8)


@toma(b_dijo - 0.3, ("desenfoque", 0.5))
def b2(lz, t):
    PB2.fondo(lz, t)
    neblina(lz, t, 0.34, 0.62, 0.32)
    if t > b_jal + 0.3:                                # la combi pasa: luces y polvo, y Toño ya no está
        v = smooth(prog(t, b_jal + 0.3, b_jal + 1.0)) * (1 - smooth(prog(t, b_jal + 2.0, b_jal + 3.0)))
        X, Y, s = PB2.P(t, lerp(0.95, 0.45, smooth(prog(t, b_jal + 0.3, b_jal + 2.6))), 0.60)
        PF.brillo(lz, X, Y, 140 * s, color=(1.0, 0.94, 0.75), inten=0.6 * v, t=t, sem=11)
        PF.arena_viento(lz, t, fuerza=1.7 * v, y0=0.40, y1=0.80, n=160, sem=6, color=(0.92, 0.84, 0.74))
    op = 1.0 - smooth(prog(t, LLEGA + 0.6, LLEGA + 1.4))
    camino(lz, PB2, t, "tono19_hoja/04", SALE, LLEGA, (0.53, 0.915), (0.64, 0.625), 0.29, 0.075, tono=ALBA, pasos=1.8,
           op=op)
    quieto(lz, PB2, t, "rosa_hoja/04", 0.42, 0.905, 0.26, tono=ALBA)
    quieto(lz, PB2, t, "angel14_hoja/03", 0.30, 0.895, 0.27, tono=ALBA, fase=0.9)
    plantas(lz, PB2, t, [("naturaleza/06", 0.95, 1.05, 0.20, 1.3, True), ("naturaleza/02", 0.05, 1.06, 0.22, 1.35, False)],
            tono=ALBA)


# ================================================================== ayudantes del tramo 3
def anda(lz, pl, t, ciclo, ta, tb, p0, p1, f0, f1, paso=0.95, tono=None, op=1.0, desde_antes=False, hasta_despues=True):
    """Ciclo de caminar (los pies no patinan: el cuadro sale de la distancia recorrida) en diagonal de p0 a p1 con el tamaño de
    f0 a f1. Los ciclos salen ~25 % más chicos que `frac` en otros videos; los de este video ya vienen a escala (21-oct: con 1,3 salían más altos que la puerta)."""
    if (t < ta and not desde_antes) or (t > tb and not hasta_despues):
        return
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, y, f = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(f0, f1, u)
    X, Y, h = pl.en(t, x, y, f)
    n = PF.ciclo_n(ciclo)
    dist = math.hypot(x - p0[0], (y - p0[1]) * 0.56) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h, flip=rumbo(ciclo, p0[0], p1[0], False), tono=tono, op=op)


def motas(lz, t, x0, y0, x1, y1, n=36, sem=0, color=(1.0, 0.95, 0.80), fuerza=0.45):
    """Polvo que flota en un haz de luz (rectángulo de PANTALLA relativo)."""
    base = np.random.RandomState(sem).rand(n, 4)
    for bx, by, bv, bs in base:
        x = x0 + (x1 - x0) * ((bx + 0.010 * t * (0.4 + bv)) % 1.0)
        y = y0 + (y1 - y0) * ((by + 0.016 * t * (bv - 0.5) + 0.02 * math.sin(t * 0.7 + bx * 9)) % 1.0)
        PF._blob(lz, x * W, y * H, 1.6 + 2.4 * bs, color, fuerza * (0.55 + 0.45 * math.sin(t * 1.3 + bx * 20)), aditivo=True)


def sombra_pasa(lz, t, t_ini, dur=1.6, fuerza=0.30):
    """Algo grande pasa por fuera (la moto): una sombra blanda barre el cuarto de izquierda a derecha."""
    u = (t - t_ini) / dur
    if not 0 <= u <= 1:
        return
    c = lerp(-0.3, 1.3, u)
    m = np.exp(-((_XX - c) / 0.16) ** 2) * fuerza * math.sin(u * math.pi)
    lz *= (1 - m)[..., None]


def desenfoque(lz, s=2.5):
    lz[:] = cv2.GaussianBlur(lz, (0, 0), s)


@functools.lru_cache(maxsize=4)
def _luces(fondo, y0, y1, modo):
    """Estrellas (puntos claros sobre el cielo) o luces cálidas del pueblo pintadas en el fondo → [(x, y, fase)] normalizados."""
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


@functools.lru_cache(maxsize=24)
def _chat(alto_px, escrito=""):
    """Celular con el chat del reclutador → RGBA float (alto_px, alto_px/2, 4). Nadie conocido: un contacto sin foto."""
    w = alto_px // 2
    s = w / 100.0
    im = Image.new("RGBA", (w, alto_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    R = int(13 * s)
    d.rounded_rectangle([0, 0, w - 1, alto_px - 1], R, fill=(22, 22, 26, 255))
    m = int(4.5 * s)
    x0, y0, x1, y1 = m, m, w - 1 - m, alto_px - 1 - m
    d.rounded_rectangle([x0, y0, x1, y1], int(R * 0.75), fill=(226, 221, 212, 255))
    d.rectangle([x0, y0 + 9 * s, x1, y0 + 24 * s], fill=(32, 44, 52, 255))
    d.ellipse([x0 + 5 * s, y0 + 11.5 * s, x0 + 15 * s, y0 + 21.5 * s], fill=(120, 124, 134, 255))
    d.text((x0 + 18 * s, y0 + 11.8 * s), "Kevin", font=_fnt("sans_b", 5.2 * s), fill=(240, 240, 244, 255))
    d.text((x0 + 18 * s, y0 + 17.6 * s), "en línea", font=_fnt("sans_l", 3.8 * s), fill=(170, 190, 200, 255))
    by = y0 + 34 * s
    d.rounded_rectangle([x0 + 5 * s, by, x1 - 16 * s, by + 34 * s], int(4 * s), fill=(255, 255, 255, 255))
    yy = by + 4 * s
    for txt in ("Q onda, ¿quieres", "jalar como tu", "carnal? Pagan bien"):
        d.text((x0 + 9 * s, yy), txt, font=_fnt("sans", 5.6 * s), fill=(30, 30, 36, 255))
        yy += 7.6 * s
    d.text((x1 - 33 * s, by + 27.5 * s), "11:48 p. m.", font=_fnt("sans_l", 3.4 * s), fill=(140, 140, 150, 255))
    iy = y1 - 21 * s
    d.rounded_rectangle([x0 + 4 * s, iy, x1 - 18 * s, iy + 13 * s], int(6 * s), fill=(255, 255, 255, 255),
                        outline=(200, 200, 210, 255), width=max(1, int(0.5 * s)))
    if escrito:
        d.text((x0 + 9 * s, iy + 3.2 * s), escrito + "|", font=_fnt("sans", 5.2 * s), fill=(30, 30, 36, 255))
    else:
        d.text((x0 + 9 * s, iy + 3.2 * s), "Escribe un mensaje…", font=_fnt("sans", 4.8 * s), fill=(150, 150, 160, 255))
    d.ellipse([x1 - 15 * s, iy, x1 - 3 * s, iy + 13 * s], fill=(37, 160, 110, 255))
    d.polygon([(x1 - 11.5 * s, iy + 3.5 * s), (x1 - 5.5 * s, iy + 6.5 * s), (x1 - 11.5 * s, iy + 9.5 * s)], fill=(255, 255, 255, 255))
    return np.asarray(im, np.float32) / 255.0


# ================================================================== 6 · LOS TENIS NUEVOS (cocina de día, lámina nueva)
Te = "tenis"
e0 = _ESC[Te]["t0"]
e_tenis, e_ya, e_pero, e_viendo = T(Te, "tenis"), T(Te, "ya", 1), T(Te, "pero", 2), T(Te, "viendo", 2)
e_fin = _ESC[Te]["t1"]
DIA = (1.03, 0.97, 0.90)
HZK, KK = 0.45, 1.54                  # cocina_dia_a: la puerta (pie en y 0,69) mide 0,44 → una persona ≈ 0,37
ROSA_EST = (0.475, 0.69, 0.355)       # Rosa entre la mesa y la cubeta, mirándolo
TONO_SILLA2 = (0.625, 0.975, 0.57)    # Toño sentado (la pieza trae su silla) viendo a la puerta
VIBRA = e_pero + 1.2                  # el celular vibra en la mesa
MOTO = e_viendo + 1.4                 # pasa una moto despacio: deja de masticar
snd(e0 + 0.3, "pasos", 0.45, dur=2.6)
snd(e_tenis, "papel", 0.6)


def cocina_dia(lz, pl, t, k_sol=1.0):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, 0.36, 0.33)                     # el sol que entra por la ventana
    PF.brillo(lz, X, Y, 330 * s, color=(1.0, 0.86, 0.55), inten=0.20 * k_sol, t=t, sem=12)


def celular_mesa(lz, pl, t):
    X, Y, h = pl.en(t, 0.30, 0.715, 0.06)
    v = 1.0 if VIBRA < t < VIBRA + 1.3 and (t * 9) % 1 < 0.6 else 0.0
    PF.actor(lz, "utileria_casa/03", X + v * 3 * math.sin(t * 90), Y, h, rot=-78 + v * 3, sy=0.42, tono=DIA, suelo=0.2)
    if v:
        PF.brillo(lz, X, Y - 0.2 * h, 0.9 * h, color=(0.6, 0.8, 1.0), inten=0.35, t=t, sem=13)


PE1 = PF.Plano("cocina_dia", e0, e_ya, z0=1.08, z1=1.22, c0=(0.56, 0.48), c1=(0.60, 0.53), par=(24, 5))


@toma(e0, ("desenfoque", 0.6))
def e1(lz, t):
    cocina_dia(lz, PE1, t)
    quieto(lz, PE1, t, "rosa_hoja/04", *ROSA_EST, tono=DIA, fase=0.6)
    anda(lz, PE1, t, "tono19b_camina", e0 + 0.1, e_ya + 0.4, (0.73, 0.695), (0.60, 0.80), alto(0.695, HZK, KK) * 0.98,
         alto(0.80, HZK, KK) * 0.98, tono=DIA, desde_antes=True)
    motas(lz, t, 0.22, 0.10, 0.50, 0.70, sem=1)
    pega(lz, "utileria_casa/02", W * 0.15, H * 0.22, H * 0.22, t, e_tenis - 0.05, e_ya - 0.5, rot=-7.0, tono=(1.0, 0.97, 0.94))


PE2 = PF.Plano("cocina_dia", e_ya - 0.3, e_pero, z0=2.15, z1=1.75, c0=(0.53, 0.62), c1=(0.53, 0.22), par=(18, 4))
snd(e_ya + 0.2, "brillo", 0.35)


@toma(e_ya - 0.3, ("latigo", 0.4))
def e2(lz, t):
    cocina_dia(lz, PE2, t)
    u = smooth(prog(t, e_ya, e_pero))
    X, Y, s = PE2.P(t, lerp(0.30, 0.80, u), 0.06)     # un brillo recorre la lámina nueva
    PF.brillo(lz, X, Y, 160 * s, color=(1.0, 0.96, 0.85), inten=0.35, t=t, sem=14)
    motas(lz, t, 0.0, 0.0, 1.0, 1.0, n=44, sem=2)


PE3 = PF.Plano("cocina_dia", e_pero - 0.3, e_viendo + 0.8, z0=1.12, z1=1.34, c0=(0.50, 0.56), c1=(0.58, 0.60), par=(24, 5))


@toma(e_pero - 0.3, ("fundido", 0.5))
def e3(lz, t):
    cocina_dia(lz, PE3, t)
    quieto(lz, PE3, t, "rosa_hoja/04", *ROSA_EST, tono=DIA, fase=0.6)
    celular_mesa(lz, PE3, t)
    X, Y, h = PE3.en(t, *TONO_SILLA2)
    PF.actor(lz, "tono19b_hoja/00", X, Y, h, tono=DIA, sy=1.0 + 0.006 * math.sin(t * 17) * (t < MOTO))
    motas(lz, t, 0.20, 0.08, 0.55, 0.75, sem=3)


PE4 = PF.Plano("cocina_dia", e_viendo + 0.5, e_fin, z0=2.35, z1=2.55, c0=(0.62, 0.56), c1=(0.64, 0.55), par=(16, 3))
snd(MOTO - 0.2, "suspiro", 0.15)


@toma(e_viendo + 0.5, ("desenfoque", 0.5))
def e4(lz, t):
    cocina_dia(lz, PE4, t)
    desenfoque(lz, 2.6)                                # la puerta al fondo, fuera de foco
    X, Y, h = PE4.en(t, *TONO_SILLA2)
    k = smooth(prog(t, MOTO, MOTO + 0.8))             # deja de masticar y voltea apenas hacia la puerta
    PF.actor(lz, "tono19b_hoja/00", X, Y, h, tono=DIA, rot=-2.5 * k,
             sy=1.0 + 0.006 * math.sin(t * 17) * (1 - k) + 0.004 * math.sin(t * 1.5) * k)
    sombra_pasa(lz, t, MOTO + 0.3, 1.8, 0.28)
    motas(lz, t, 0.0, 0.0, 0.6, 0.8, sem=4, fuerza=0.35)


# ================================================================== 7 · EL MENSAJE (azotea de noche)
Me = "mensaje"
m0 = _ESC[Me]["t0"]
m_tu, m_y, m_porque = T(Me, "tú", 0), T(Me, "y", 1), T(Me, "porque", 2)
m_tu2, m_papel, m_prom = T(Me, "tú", 3), T(Me, "papel", 3), T(Me, "prometiste", 3)
m_fin = _ESC[Me]["t1"]
AVISO2 = m0 + 0.9
CHAT, TECLEA = m0 + 2.5, m0 + 3.9            # el chat en pantalla; escribe «va…»
SUBE = m0 + 5.3                              # Toño sube por la escalera
ARREBATA = m_tu - 0.55
FA_N = "azotea_noche_b"
HZN, KN = 0.30, 0.70
XAN, XTN, YN = 0.41, 0.50, 0.725            # Ángel y Toño de pie en la losa
NOCHE2 = (0.62, 0.66, 0.92)
snd(ARREBATA, "whoosh", 0.45, dur=0.4)
snd(ARREBATA + 0.1, "borrar", 0.4)
snd(TECLEA, "escribir", 0.45, dur=1.0)
snd(SUBE, "pasos", 0.55, dur=1.6)


def noche(lz, pl, t):
    pl.fondo(lz, t)
    titilan(lz, pl, t, FA_N, 0.0, 0.30, "estrella", (0.85, 0.90, 1.0), r=3.0, inten=0.6)
    titilan(lz, pl, t, FA_N, 0.32, 0.56, "luz", (1.0, 0.75, 0.40), r=6.0, inten=0.35)
    X, Y, s = pl.P(t, 0.66, 0.32)                     # el santuario iluminado
    PF.brillo(lz, X, Y, 300 * s, color=(1.0, 0.78, 0.45), inten=0.16, t=t, sem=15)


def brillo_cel(lz, pl, t, x, y, f, inten=0.35):
    X, Y, h = pl.en(t, x, y, f)
    PF.brillo(lz, X, Y - 0.62 * h, 0.55 * h, color=(0.55, 0.75, 1.0), inten=inten, t=t, sem=16)


PM1 = PF.Plano(FA_N, m0, CHAT, z0=1.35, z1=1.75, c0=(0.48, 0.46), c1=(0.44, 0.60), par=(26, 5))


@toma(m0, ("fundido", 0.7))
def m1(lz, t):
    noche(lz, PM1, t)
    f = alto(YN, HZN, KN) * 0.62
    quieto(lz, PM1, t, "angel14_hoja/01", XAN, YN, f, tono=NOCHE2, fase=0.3)
    brillo_cel(lz, PM1, t, XAN, YN, f, 0.30 + 0.25 * smooth(prog(t, AVISO2, AVISO2 + 0.4)))


def pantalla(lz, pl, t, rgba, t_in=None):
    pl.fondo(lz, t)
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 14) * np.float32(0.55)
    u = 1.0 if t_in is None else PF.entra(t, t_in, 0.5)
    pegar_rgba(lz, rgba, W * 0.5, H * 0.52 + (1 - u) * 60, escala=0.94 + 0.06 * u, rot=0.8 * math.sin(t * 1.7), op=clamp01(u * 2))
    PF.brillo(lz, W * 0.5, H * 0.5, H * 0.55, color=(0.55, 0.75, 1.0), inten=0.08, t=t, sem=7)


PM2 = PF.Plano(FA_N, CHAT, SUBE, z0=1.4, z1=1.45, c0=(0.47, 0.55), c1=(0.47, 0.55), par=(0, 0))


@toma(CHAT, ("corte", 0.1))
def m2(lz, t):
    n = int(clamp01((t - TECLEA) / 0.9) * 3)
    pantalla(lz, PM2, t, _chat(int(H * 0.92) // 2 * 2, "va…"[:n]), t_in=CHAT + 0.1)


PM3 = PF.Plano(FA_N, SUBE, m_y, z0=1.75, z1=1.95, c0=(0.55, 0.55), c1=(0.50, 0.55), par=(22, 4))


@toma(SUBE, ("corte", 0.1))
def m3(lz, t):
    noche(lz, PM3, t)
    f = alto(YN, HZN, KN)
    if t < ARREBATA + 0.35:                            # sentado con el celular hasta que se lo quitan
        quieto(lz, PM3, t, "angel14_hoja/01", XAN, YN, f * 0.62, tono=NOCHE2, fase=0.3)
        brillo_cel(lz, PM3, t, XAN, YN, f * 0.62)
    else:
        quieto(lz, PM3, t, "angel14_hoja/02", XAN, YN, f * 0.95, tono=NOCHE2, t_in=ARREBATA + 0.35)
    if t < ARREBATA:                                   # sube por la escalera y cruza la losa
        anda(lz, PM3, t, "tono19b_camina", SUBE, ARREBATA, (0.80, 0.78), (XTN, YN), alto(0.78, HZN, KN) * 1.02,
             f * 1.02, tono=NOCHE2, desde_antes=True)
    else:
        poses(lz, PM3, t, [(ARREBATA, "tono19b_hoja/01", True, 1.0), (m_tu + 1.4, "tono19b_hoja/01", True, 1.0)],
              XTN, YN, f * 1.02, tono=NOCHE2)
        pega(lz, "utileria_casa/03", W * 0.80, H * 0.24, H * 0.20, t, ARREBATA, m_tu - 0.1, rot=12, tono=NOCHE2, flota=False)


PM4 = PF.Plano(FA_N, m_y - 0.3, m_porque, z0=2.9, z1=3.05, c0=(0.42, 0.58), c1=(0.41, 0.585), par=(16, 3))


@toma(m_y - 0.3, ("desenfoque", 0.4))
def m4(lz, t):
    noche(lz, PM4, t)
    desenfoque(lz, 3.0)
    f = alto(YN, HZN, KN)
    quieto(lz, PM4, t, "angel14_hoja/02", XAN, YN, f * 0.95, tono=NOCHE2, fase=0.2)
    X, Y, h = PM4.en(t, 0.565, YN + 0.06, f * 1.3)    # el hombro de Toño, cerca de la cámara
    desenfocado(lz, "tono19b_hoja/01", X, Y, h, sigma=10.0, tono=NOCHE2)


PM5 = PF.Plano(FA_N, m_porque - 0.3, m_tu2, z0=2.95, z1=3.15, c0=(0.50, 0.58), c1=(0.505, 0.575), par=(16, 3))


@toma(m_porque - 0.3, ("desenfoque", 0.4))
def m5(lz, t):
    noche(lz, PM5, t)
    desenfoque(lz, 3.0)
    quieto(lz, PM5, t, "tono19b_hoja/02", XTN, YN, alto(YN, HZN, KN) * 1.02, tono=NOCHE2, fase=1.1)


PM6 = PF.Plano(FA_N, m_tu2 - 0.3, m_fin, z0=1.95, z1=1.65, c0=(0.50, 0.57), c1=(0.53, 0.50), par=(24, 5))


@toma(m_tu2 - 0.3, ("fundido", 0.5))
def m6(lz, t):
    noche(lz, PM6, t)
    f = alto(YN, HZN, KN)
    poses(lz, PM6, t, [(m_tu2 - 1, "angel14_hoja/02", False, 0.95), (m_tu2 + 1.1, "angel14_hoja/03", False, 0.95)],
          XAN, YN, f, tono=NOCHE2, fase=0.2)
    poses(lz, PM6, t, [(m_tu2 - 1, "tono19b_hoja/02", False, 1.02), (m_prom - 0.25, "tono19b_hoja/03", False, 1.02)],
          XTN, YN, f, tono=NOCHE2, fase=1.1)


# ================================================================== 8 · LA RECÁMARA (al otro día)
R_ = "recamara"
r0 = _ESC[R_]["t0"]
r_al = T(R_, "al")
r_fin = _ESC[R_]["t1"]
HZR, KR = 0.35, 1.375
MANANA = (0.92, 0.95, 1.04)
GORRA = (0.165, 0.585, 0.075)                  # la gorra roja vieja en la cobija de Ángel
DETALLE = r_al + 1.6


def recamara(lz, pl, t):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, 0.40, 0.18)                     # luz fría de la ventana
    PF.brillo(lz, X, Y, 360 * s, color=(0.85, 0.92, 1.0), inten=0.20 + 0.03 * math.sin(t * 0.9), t=t, sem=17)
    X, Y, h = pl.en(t, *GORRA)
    PF.actor(lz, "utileria_casa/01", X, Y, h, rot=-14, tono=MANANA, suelo=0.25)


PR1 = PF.Plano("recamara_amanecer", r0 - 0.4, DETALLE, z0=1.10, z1=1.38, c0=(0.55, 0.48), c1=(0.66, 0.52), par=(24, 5))
snd(r0 + 0.2, "pasos", 0.35, dur=1.8)


@toma(r0 - 0.4, ("corte", 0.1))
def r1(lz, t):
    recamara(lz, PR1, t)
    yA = 0.80
    if t < r_al + 0.7:
        anda(lz, PR1, t, "angel14_camina", r0, r_al - 0.4, (1.10, yA), (0.82, yA), alto(yA, HZR, KR) * 0.92,
             alto(yA, HZR, KR) * 0.92, tono=MANANA, desde_antes=True)
    else:
        quieto(lz, PR1, t, "angel14_hoja/03", 0.82, yA, alto(yA, HZR, KR) * 0.92, tono=MANANA, t_in=r_al + 0.7)
    motas(lz, t, 0.25, 0.05, 0.62, 0.70, sem=5, color=(0.92, 0.96, 1.0))


PR2 = PF.Plano("recamara_amanecer", DETALLE - 0.3, r_fin, z0=2.6, z1=2.85, c0=(0.18, 0.58), c1=(0.17, 0.585), par=(14, 3))


@toma(DETALLE - 0.3, ("fundido", 0.6))
def r2(lz, t):
    recamara(lz, PR2, t)
    motas(lz, t, 0.0, 0.0, 1.0, 0.8, n=40, sem=6, color=(0.92, 0.96, 1.0), fuerza=0.35)


# ================================================================== 9 · LA GRADUACIÓN — julio (vals, silla apartada, la reja)
Gr = "graduacion"
g0 = _ESC[Gr]["t0"]
g_cuando, g_pero = T(Gr, "cuando", 0), T(Gr, "pero", 1)
g_fin = _ESC[Gr]["t1"]
HZG, KG = 0.56, 1.15
FIESTA = (1.03, 0.96, 0.86)
GR2, GR3, GR4, GR5 = g0 + 5.3, g0 + 9.6, g0 + 13.8, g0 + 16.9          # silla · certificado · mamá · Ángel busca
REJA1, DEVUELVE, REJA2 = g_cuando - 0.3, g_cuando + 3.0, g_pero + 1.6
NEGRO = g_fin - 1.6                    # negro < 2 s en el MASTER (con −2,0 blackdetect midió 2,0 s); silencio total desde g_fin − 4
SILLA_X, SILLA_Y = 0.865, 0.80                                          # Rosa sentada · a su lado la silla apartada
snd(GR3 + 0.6, "pop", 0.3)


def cancha(lz, pl, t):
    pl.fondo(lz, t)
    X, Y, s = pl.P(t, 0.50, 0.45)
    PF.brillo(lz, X, Y, 420 * s, color=(1.0, 0.82, 0.55), inten=0.14, t=t, sem=18)


def papel_picado(lz, pl, t):
    plantas(lz, pl, t, [("utileria_fiesta/00", 0.20, 0.10, 0.16, 1.4, False), ("utileria_fiesta/01", 0.78, 0.08, 0.15, 1.45, True)],
            tono=FIESTA)


def publico(lz, pl, t):
    """Los invitados alrededor de la cancha, de lejos a cerca (orden de dibujo = profundidad)."""
    for pz, x, y, k, fl, fa in (("graduacion_gente_hoja/06", 0.30, 0.625, 1.0, False, 0.2),
                                ("graduacion_gente_hoja/04", 0.60, 0.645, 0.92, True, 0.9),
                                ("graduacion_gente_hoja/02", 0.69, 0.665, 1.0, True, 1.4),
                                ("graduacion_gente_hoja/00", 0.78, 0.69, 0.80, True, 0.5),
                                ("graduacion_gente_hoja/03", 0.25, 0.70, 1.0, False, 2.0),
                                ("graduacion_gente_hoja/01", 0.86, 0.72, 0.80, True, 1.1),
                                ("graduacion_gente_hoja/05", 0.17, 0.76, 0.62, False, 0.7)):
        aplaude = pz.endswith("/03")
        quieto(lz, pl, t, pz, x, y, alto(y, HZG, KG) * k, flip=fl, tono=FIESTA, fase=fa,
               rot=2.0 * math.sin(t * 9) if aplaude else 0.0)


def vals(lz, pl, t, x=0.47, y=0.90, f=None):
    """La mamá y Ángel bailan: los 4 dibujos del vals se suceden mientras la pareja gira despacio en su lugar."""
    k = int(t / 0.55) % 4
    a = t * 1.1
    X, Y, h = pl.en(t, x + 0.025 * math.cos(a), y + 0.008 * math.sin(a), f or alto(y, HZG, KG) * 1.05)
    PF.actor(lz, f"vals_hoja/{k:02d}", X, Y, h, flip=(int(t / 2.2) % 2 == 1), tono=FIESTA, rot=2.0 * math.sin(a * 2))


PG1b = PF.Plano("cancha_graduacion", g0, GR2, z0=1.20, z1=1.42, c0=(0.50, 0.52), c1=(0.47, 0.62), par=(28, 6))


@toma(g0, ("negro", 1.0))
def gr1(lz, t):
    cancha(lz, PG1b, t)
    publico(lz, PG1b, t)
    vals(lz, PG1b, t)
    papel_picado(lz, PG1b, t)
    PF.rotulo(lz, "JULIO", W * 0.5, H * 0.13, 64, t, g0 + 0.8, GR2 - 0.7, rot=-1.5)


def sillas(lz, pl, t, rosa="rosa_hoja/03", t_rosa=None):
    X, Y, h = pl.en(t, SILLA_X + 0.075, SILLA_Y + 0.005, alto(SILLA_Y, HZG, KG) * 0.50)
    PF.actor(lz, "utileria_casa/14", X, Y, h, tono=FIESTA)
    X2, Y2, h2 = pl.en(t, SILLA_X + 0.075, SILLA_Y - 0.035, alto(SILLA_Y, HZG, KG) * 0.10)
    PF.actor(lz, "utileria_fiesta/11", X2, Y2 - 0.40 * h, h2, rot=-6, tono=FIESTA, suelo=0)
    k = 0.80 if rosa.endswith("/03") else 0.98
    quieto(lz, pl, t, rosa, SILLA_X, SILLA_Y, alto(SILLA_Y, HZG, KG) * k, tono=FIESTA, fase=0.4, t_in=t_rosa)


PG2b = PF.Plano("cancha_graduacion", GR2 - 0.3, GR3, z0=2.1, z1=2.45, c0=(0.82, 0.66), c1=(0.89, 0.69), par=(22, 4))


@toma(GR2 - 0.3, ("fundido", 0.6))
def gr2(lz, t):
    cancha(lz, PG2b, t)
    publico(lz, PG2b, t)
    sillas(lz, PG2b, t, t_rosa=GR2 + 0.5)
    papel_picado(lz, PG2b, t)


PG3b = PF.Plano("cancha_graduacion", GR3 - 0.3, GR4, z0=1.75, z1=1.90, c0=(0.38, 0.66), c1=(0.41, 0.68), par=(24, 5))


@toma(GR3 - 0.3, ("latigo", 0.4))
def gr3(lz, t):
    cancha(lz, PG3b, t)
    publico(lz, PG3b, t)
    f = alto(0.86, HZG, KG)
    quieto(lz, PG3b, t, "graduacion_gente_hoja/06", 0.33, 0.855, f * 1.02, tono=FIESTA, fase=0.3)
    quieto(lz, PG3b, t, "angel_grad_hoja/00", 0.45, 0.86, f * 0.97, tono=FIESTA, t_in=GR3 + 0.6)
    papel_picado(lz, PG3b, t)


PG4b = PF.Plano("cancha_graduacion", GR4 - 0.3, GR5, z0=2.5, z1=2.7, c0=(0.88, 0.62), c1=(0.89, 0.63), par=(20, 4))


@toma(GR4 - 0.3, ("desenfoque", 0.45))
def gr4(lz, t):
    cancha(lz, PG4b, t)
    desenfoque(lz, 2.0)
    sillas(lz, PG4b, t, rosa="rosa_hoja/04")


PG5b = PF.Plano("cancha_graduacion", GR5 - 0.3, REJA1, z0=2.45, z1=2.65, c0=(0.46, 0.68), c1=(0.47, 0.69), par=(16, 3))


@toma(GR5 - 0.3, ("desenfoque", 0.45))
def gr5(lz, t):
    cancha(lz, PG5b, t)
    desenfoque(lz, 3.0)
    poses(lz, PG5b, t, [(GR5 - 1, "angel_grad_hoja/01", False, 1.0), (GR5 + 1.6, "angel_grad_hoja/04", False, 1.0)],
          0.465, 0.86, alto(0.86, HZG, KG) * 0.97, tono=FIESTA)


# --- la reja: afuera, entre la troca y el poste, Toño con su gorra nueva
TONO_REJA = (0.495, 0.605, 0.165)
CALLE = (0.528, 0.505)
PJ1 = PF.Plano("reja_calle", REJA1, DEVUELVE, z0=1.12, z1=1.95, c0=(0.50, 0.50), c1=(0.495, 0.50), par=(30, 6), ease=lambda u: u)
snd(REJA1 + 0.2, "viento", 0.3, dur=4.0)


@toma(REJA1, ("negro", 0.8))
def j1(lz, t):
    PJ1.fondo(lz, t)
    X, Y, s = PJ1.P(t, 0.60, 0.30)
    PF.brillo(lz, X, Y, 380 * s, color=(1.0, 0.80, 0.50), inten=0.20, t=t, sem=19)
    poses(lz, PJ1, t, [(REJA1 - 1, "tono19b_hoja/02", False, 1.0), (REJA1 + 0.9, "tono19b_hoja/03", False, 1.0)],
          *TONO_REJA, tono=FIESTA, fase=0.8)


PG6b = PF.Plano("cancha_graduacion", DEVUELVE - 0.3, REJA2, z0=2.55, z1=2.75, c0=(0.465, 0.66), c1=(0.47, 0.67), par=(16, 3))


@toma(DEVUELVE - 0.3, ("desenfoque", 0.45))
def gr6(lz, t):
    cancha(lz, PG6b, t)
    desenfoque(lz, 3.0)
    poses(lz, PG6b, t, [(DEVUELVE - 1, "angel_grad_hoja/04", False, 1.0), (DEVUELVE + 0.35, "angel_grad_hoja/02", False, 1.0)],
          0.465, 0.86, alto(0.86, HZG, KG) * 0.97, tono=FIESTA)


PJ2 = PF.Plano("reja_calle", REJA2 - 0.3, NEGRO, z0=1.95, z1=1.75, c0=(0.50, 0.50), c1=(0.51, 0.49), par=(30, 6))


@toma(REJA2 - 0.3, ("desenfoque", 0.45))
def j2(lz, t):
    PJ2.fondo(lz, t)
    X, Y, s = PJ2.P(t, 0.60, 0.30)
    PF.brillo(lz, X, Y, 380 * s, color=(1.0, 0.80, 0.50), inten=0.20, t=t, sem=19)
    va = REJA2 + 0.9
    if t < va:
        quieto(lz, PJ2, t, "tono19b_hoja/03", *TONO_REJA, tono=FIESTA, fase=0.8)
    else:                                              # se da la vuelta y se va calle abajo, cada vez más chico
        camino(lz, PJ2, t, "tono19b_hoja/04", va, NEGRO - 0.4, TONO_REJA[:2], CALLE, TONO_REJA[2], 0.045, tono=FIESTA,
               pasos=1.6, salto=0.02, op=1.0 - smooth(prog(t, NEGRO - 1.2, NEGRO - 0.4)))


@toma(NEGRO, ("fundido", 0.7))
def negro(lz, t):
    pass


# ================================================================== 10 · LA CUESTA — epílogo (otro atardecer)
Ep = "epilogo"
q0 = _ESC[Ep]["t0"]
q_ahora = T(Ep, "ahora")
SUELTA2, ABAJO = q0 + 2.4, q0 + 4.8
EP2 = q_ahora - 1.2
PE_1 = PF.Plano("cuesta_tarde", q0, EP2, z0=1.75, z1=1.50, c0=(0.51, 0.66), c1=(0.47, 0.72), par=(30, 6))
VUELOE = [(q0 + 0.4, 9.0, 0.13, 0.08, 44, 1, 0.4), (q0 + 1.5, 10.0, 0.19, 0.14, 32, 1, 1.6)]
NINO = [(q0 + 0.3, SUELTA2, (0.535, 0.645), (0.51, 0.75), 1.0), (SUELTA2, ABAJO, (0.51, 0.75), (0.43, 0.90), 1.4)]


def nino_bici(lz, pl, t, tramos, f_k, hz, k, tono=None):
    """El niño vecino en la bici vieja: la pieza no tiene ciclo; rueda con un vaivén."""
    for ta, tb, p0, p1, pot in tramos:
        if ta <= t < tb or (t < ta and ta == tramos[0][0]) or (t >= tb and tb == tramos[-1][1]):
            u = clamp01((t - ta) / (tb - ta)) ** pot
            x, y = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
            X, Y, h = pl.en(t, x, y, alto(y, hz, k) * f_k)
            mov = tramos[0][0] < t < tramos[-1][1]
            PF.actor(lz, "gente_hoja/00", X, Y, h, flip=rumbo("gente_hoja/00", p0[0], p1[0], False), tono=tono,
                     rot=2.0 * math.sin(t * 8.0) * mov)
            return


@toma(q0, ("negro", 1.0))
def q1(lz, t):
    PE_1.fondo(lz, t)
    aves(lz, t, VUELOE, tono=DORADO)
    if t < SUELTA2:
        anda(lz, PE_1, t, "angel14_camina", q0 + 0.3, SUELTA2, (0.565, 0.64), (0.545, 0.745), alto(0.64, HZC, KC) * 0.80,
             alto(0.745, HZC, KC) * 0.80, tono=DORADO, desde_antes=True)
    else:
        quieto(lz, PE_1, t, "angel14_hoja/05", 0.545, 0.745, alto(0.745, HZC, KC) * 0.80, flip=True, tono=DORADO, t_in=SUELTA2)
    nino_bici(lz, PE_1, t, NINO, 0.62, HZC, KC, tono=DORADO)
    plantas(lz, PE_1, t, FG_CUESTA, tono=DORADO)


PE_2 = PF.Plano("cuesta_tarde_b", EP2 - 0.3, TOTAL, z0=1.60, z1=1.28, c0=(0.53, 0.70), c1=(0.52, 0.58), par=(28, 6))
VUELOE2 = [(EP2 + 1.0, 8.0, 0.12, 0.07, 40, -1, 0.7), (EP2 + 3.5, 8.5, 0.18, 0.12, 30, -1, 1.8)]


@toma(EP2 - 0.3, ("desenfoque", 0.5))
def q2(lz, t):
    PE_2.fondo(lz, t)
    aves(lz, t, VUELOE2, tono=DORADO)
    poses(lz, PE_2, t, [(EP2 - 1, "angel14_hoja/05", True, 1.0), (q_ahora - 0.5, "angel14_hoja/04", False, 1.0)],
          0.47, 0.74, alto(0.74, HZB, KB) * 0.82, tono=DORADO, fase=1.0)
    X, Y, h = PE_2.en(t, 0.60, 0.93, alto(0.93, HZB, KB) * 0.66)
    PF.actor(lz, "gente_hoja/00", X, Y, h, flip=True, tono=DORADO, sy=PF.respira(t))
    plantas(lz, PE_2, t, [("naturaleza/06", 0.04, 1.05, 0.20, 1.3, False)], tono=DORADO)
    PF.arena_viento(lz, t, fuerza=0.25, y0=0.80, sem=7, color=(0.98, 0.84, 0.58))
    PF.rotulo(lz, "LA SEÑA", W * 0.5, H * 0.17, 104, t, q_ahora + 2.6, None, rot=-1.5)


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
    img = PF.acabado(img, t)
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
