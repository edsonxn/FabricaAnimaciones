# -*- coding: utf-8 -*-
"""Ramsés II — documental de personaje antiguo (kit `nucleo/docu_antiguo.py`, docs/estilo_docu_antiguo.md).
Una lista de TOMAS (t0, función de cuadro, entrada) que cubre el video; cada toma declara su animación con `A.firma` (regla del kit:
ninguna receta se repite). Regla de DENSIDAD (el usuario, 4-nov-2026: «no debe parecer secuencia de fotos»): cada toma con ≥ 4 capas
que se mueven a velocidades distintas (fondo con parallax · recortes que entran o cruzan · grafismo del kit · primer plano de partículas,
humo o siluetas), algo nuevo cada 1-1,5 s y cámara siempre en movimiento. Tramo 3: gancho + cap. 1 (0-120 s); lo que falta = negro."""
import functools
import math

import cv2
import numpy as np

import docu as D
import docu_antiguo as A
from escena_base import Escena, TL
from motor import W, H, e_inout, e_out, lerp, prog, smooth

TOTAL = TL["total"]
_FR = {f["key"]: f for e in TL["escenas"] for f in e["frases"]}
NEGRO = (0.022, 0.020, 0.020)
IMG = "imagenes/"


def T(key, palabra, n=0, fin=False):
    """Tiempo en que se dice `palabra` (prefijo, sin tildes ni mayúsculas) en la frase `key` (p. ej. "gancho_2")."""
    import unicodedata

    def nm(s):
        return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn").strip("¿?¡!.,:;«»")
    hits = [w["e"] if fin else w["s"] for w in _FR[key]["words"] if nm(w["w"]).startswith(nm(palabra))]
    return hits[n]


def negro():
    return np.full((H, W, 3), NEGRO, np.float32)


def ancla(nombre, t, ta, tb, rel, z0, z1, c0, c1, ease=e_inout):
    """Posición en PANTALLA de un punto de la foto (`rel` = fracción x, y de la foto) con la misma cámara que `D.foto_parallax`:
    lo que se añade encima (luces, marcas) se mueve con la imagen."""
    rgb = D.cargar(D.ruta_img(nombre), 2600)
    hs, ws = rgb.shape[:2]
    u = ease(min(1.0, max(0.0, (t - ta) / max(tb - ta, 1e-3))))
    z = lerp(z0, z1, u)
    s0 = max(W / ws, H / hs) * z
    cx, cy = lerp(c0[0], c1[0], u) * ws, lerp(c0[1], c1[1], u) * hs
    return W / 2 + (rel[0] * ws - cx) * s0, H / 2 + (rel[1] * hs - cy) * s0, s0 / max(W / ws, H / hs)


def toma(nombre, t, ta, tb, **k):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, nombre, t - ta, tb - ta, **k)
    return lz


# ------------------------------------------------------------------ CAPAS propias del video (primitivas; cada toma las combina distinto)
def particulas(lz, t, sem, n=120, v=(0.0, -40.0), tam=(1.0, 3.0), color=(1.0, 0.9, 0.7), op=0.6, estela=0.0, blur=0.0, zona=(0, 0, W, H),
               parpadeo=0.0):
    """Partículas que se desplazan a velocidad `v` px/s (cada una ±40 %): polvo, arena (estela), brasas (suben), lluvia."""
    rng = np.random.default_rng(sem)
    x0, y0, x1, y1 = zona
    px = rng.uniform(0, 1, n); py = rng.uniform(0, 1, n)
    k = rng.uniform(0.6, 1.4, n)
    r = rng.uniform(tam[0], tam[1], n)
    fase = rng.uniform(0, 6.28, n)
    capa = np.zeros((H, W), np.float32)
    ww, hh = x1 - x0, y1 - y0
    xs = x0 + (px * ww + v[0] * k * t) % ww
    ys = y0 + (py * hh + v[1] * k * t + 6 * np.sin(t * 1.3 + fase)) % hh
    br = 1.0 - parpadeo * (0.5 + 0.5 * np.sin(t * 7.0 + fase))
    for i in range(n):
        if estela > 0:
            dx, dy = v[0] * k[i] * estela, v[1] * k[i] * estela
            cv2.line(capa, (int(xs[i]), int(ys[i])), (int(xs[i] - dx), int(ys[i] - dy)), float(br[i]), max(1, int(r[i] * 0.7)), cv2.LINE_AA)
        else:
            cv2.circle(capa, (int(xs[i]), int(ys[i])), max(1, int(r[i])), float(br[i]), -1, cv2.LINE_AA)
    if blur > 0:
        capa = cv2.GaussianBlur(capa, (0, 0), blur)
    lz += capa[..., None] * np.float32(color) * op


@functools.lru_cache(maxsize=8)
def _ruido(sem):
    rng = np.random.default_rng(sem)
    tot = np.zeros((H // 4, W // 2), np.float32)
    for s, a in ((40, 1.0), (16, 0.5), (6, 0.25)):
        tot += cv2.GaussianBlur(rng.random((H // 4, W // 2)).astype(np.float32), (0, 0), s) * a
    tot = (tot - tot.min()) / (tot.max() - tot.min())
    return np.clip((tot - 0.45) * 2.6, 0, 1)


def humo(lz, t, sem=1, v=(18.0, -6.0), color=(0.75, 0.72, 0.68), op=0.35, zona_y=(0.0, 1.0)):
    """Humo/niebla: textura de ruido que se desliza (se calcula a 1/4 y se escala)."""
    r = _ruido(sem)
    hh, ww = r.shape
    ox, oy = int((v[0] * t / 4) % ww), int((v[1] * t / 4) % hh)
    m = np.roll(np.roll(r, ox, 1), oy, 0)[:, :ww // 2 + 1]
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    y0, y1 = int(zona_y[0] * H), int(zona_y[1] * H)
    rampa = np.zeros((H, 1), np.float32)
    rampa[y0:y1] = np.sin(np.linspace(0, math.pi, max(1, y1 - y0)))[:, None]
    lz += (m * rampa)[..., None] * np.float32(color) * op


def barrido_luz(lz, t, t0, dur=1.4, color=(1.0, 0.85, 0.6), op=0.35, ang=0.35):
    """Franja de luz diagonal que cruza la pantalla una vez."""
    u = prog(t, t0, t0 + dur)
    if not 0 < u < 1:
        return
    yy, xx = np.ogrid[0:H, 0:W]
    d = (xx + yy * ang) - lerp(-500, W + 500, e_inout(u))
    lz += (np.exp(-(d / 160.0) ** 2) * math.sin(math.pi * u)).astype(np.float32)[..., None] * np.float32(color) * op


def rayos(lz, t, cx, cy, op=0.25, color=(1.0, 0.82, 0.5), n=14, sem=0):
    """Rayos de luz que bajan desde (cx, cy) y respiran."""
    yy, xx = np.ogrid[0:H, 0:W]
    ang = np.arctan2(yy - cy, xx - cx)
    d = np.hypot(xx - cx, yy - cy)
    f = 0.5 + 0.5 * np.sin(ang * n + sem + 0.4 * math.sin(t * 0.7)) * np.sin(ang * (n * 0.37) - t * 0.3)
    m = np.clip(f, 0, 1) ** 3 * np.exp(-d / 900.0) * (yy > cy)
    lz += m.astype(np.float32)[..., None] * np.float32(color) * op


def flashes(lz, t, t0, t1, sem=4, n=8):
    """Flashes de cámaras de prensa que saltan en sitios distintos."""
    rng = np.random.default_rng(sem)
    for i in range(n):
        tf = t0 + rng.uniform(0, 1) * (t1 - t0)
        x, y = rng.uniform(0.1, 0.9) * W, rng.uniform(0.35, 0.75) * H
        u = t - tf
        if 0 <= u < 0.35:
            k = math.exp(-u * 11)
            yy, xx = np.ogrid[0:H, 0:W]
            lz += (np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * 60.0 ** 2)) * 1.6 * k + 0.05 * k).astype(np.float32)[..., None]


def recorte(lz, png, cx, cy, alto, t, t0, desde=(0.0, 0.0), dur=0.9, deriva=(0.0, 0.0), giro=0.0, rz=0.0, op=1.0, tono=1.0, blur=0.0,
            salida=None):
    """Recorte real (PNG con alfa) que entra deslizándose desde `desde` (px), deriva y opcionalmente gira; tono < 1 = silueta."""
    u = e_out(prog(t, t0, t0 + dur))
    if u <= 0:
        return
    spr = A._sprite_png(png, int(alto))
    x = cx + (1 - u) * desde[0] + deriva[0] * (t - t0)
    y = cy + (1 - u) * desde[1] + deriva[1] * (t - t0)
    M = D.poner(spr.w, spr.h, x, y, 1.0, rz=rz, ry=giro * math.sin((t - t0) * 0.5))
    k = u * op * ((1 - smooth(prog(t, salida, salida + 0.5))) if salida else 1.0)
    if tono != 1.0 or blur:
        capa = np.zeros_like(lz)
        D.pegar(capa, spr, M, 1.0)
        a = cv2.warpPerspective(spr.a, M, (W, H))
        if blur:
            capa = cv2.GaussianBlur(capa, (0, 0), blur)
            a = cv2.GaussianBlur(a, (0, 0), blur)
        lz[:] = lz * (1 - a[..., None] * k) + capa * tono * k
    else:
        D.pegar(lz, spr, M, k)


def contador(lz, t, t0, dur, desde, hasta, cx, cy, px=64, sufijo="", color=A.BLANCO, salida=None):
    """Cifra que cuenta de `desde` a `hasta` (miles con espacio)."""
    if t < t0 or (salida and t > salida + 0.4):
        return
    v = int(round(lerp(desde, hasta, e_out(prog(t, t0, t0 + dur)))))
    txt = f"{v:,}".replace(",", " ") + sufijo
    op = 1 - smooth(prog(t, salida, salida + 0.4)) if salida else 1.0
    D.numero(lz, txt, cx, cy, px, t, t0, color=color, fnt="serif", pop=False, op=op)


def camara(img, t, ta, tb, z0=1.0, z1=1.06, dx=(0, 0), rot=(0.0, 0.0), temblor=0.0):
    """Mueve el cuadro ya compuesto (empuje, paneo, giro leve y temblor): ninguna toma con la cámara quieta."""
    u = e_inout(prog(t, ta, tb))
    sx = lerp(0, dx[0], u) + temblor * (math.sin(t * 13.1) + 0.6 * math.sin(t * 7.3))
    sy = lerp(0, dx[1], u) + temblor * (math.cos(t * 11.7) + 0.6 * math.sin(t * 5.1))
    return _cam_punto(img, lerp(z0, z1, u), sx, sy, lerp(rot[0], rot[1], u))


def _cam_punto(img, z, dx, dy, rot=0.0):
    global _TXT
    M = cv2.getRotationMatrix2D((W / 2, H / 2), rot, z)
    M[:, 2] += (dx, dy)
    if _TXT is not None:                                                # el texto capturado se mueve con la cámara de la toma
        _TXT = cv2.warpAffine(_TXT, M, (W, H), borderValue=0)
    return cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REPLICATE)


# ------------------------------------------------------------------ TEXTO CAPTURADO (el usuario, 4-nov-2026: «que los textos se vean cuando hay
# varias capas»): todo texto que pinta una toma se pinta también en `_TXT`; el túnel lo vuelve a poner encima de las capas.
_TXT = None


def _envolver(fn):
    @functools.wraps(fn)
    def w(lz, *a, **k):
        r = fn(lz, *a, **k)
        if _TXT is not None and lz.shape == (H, W, 3):
            fn(_TXT, *a, **k)
        return r
    return w


for _n in ("rotulo_serif", "neon", "cursiva_luz", "texto_mixto", "cita", "etiqueta"):
    if not hasattr(getattr(A, _n), "__wrapped__"):
        setattr(A, _n, _envolver(getattr(A, _n)))
contador = _envolver(contador)


def con_texto(fn):
    """Toma → (cuadro, capa de texto) para el túnel."""
    def w(t, ta, tb):
        global _TXT
        _TXT = np.zeros((H, W, 3), np.float32)
        try:
            img = fn(t, ta, tb)
            return img, _TXT
        finally:
            _TXT = None
    return w


@functools.lru_cache(maxsize=4)
def _banda(ruta, alto):
    im = cv2.cvtColor(cv2.imread(ruta), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    k = alto / im.shape[0]
    im = cv2.resize(im, (int(im.shape[1] * k), alto), interpolation=cv2.INTER_AREA)
    return np.tile(im, (1, max(3, int(math.ceil(3 * W / im.shape[1])))))


def banda_relieve(lz, ruta, y, alto, t, t0, vel=40.0, color=(0.85, 0.72, 0.5), op=0.25, invertir=False):
    """Franja de un relieve REAL que se desliza en horizontal, como un friso al fondo."""
    k = smooth(prog(t, t0, t0 + 0.8)) * op
    if k <= 0:
        return
    b = _banda(ruta, alto)
    ox = int((vel * (t - t0)) % (b.shape[1] - W))
    tira = b[:, ox:ox + W]
    tira = (1 - tira) if invertir else tira
    y0 = int(y - alto / 2)
    a0 = max(0, -y0)
    y0 = max(0, y0)
    y1 = min(H, int(y - alto / 2) + alto)
    borde = np.sin(np.linspace(0, math.pi, alto))[:, None][a0:a0 + y1 - y0]
    lz[y0:y1] += (tira[a0:a0 + y1 - y0] * borde)[..., None] * np.float32(color) * k


def aro(lz, cx, cy, r, t, t0, color=A.BLANCO, op=0.8, txt=None):
    """Aro vacío con halo (el hueco del heredero que no llega)."""
    u = e_out(prog(t, t0, t0 + 0.6))
    if u <= 0:
        return
    capa = np.zeros((H, W), np.float32)
    cv2.circle(capa, (int(cx), int(cy)), int(r * (0.7 + 0.3 * u)), 1.0, 3, cv2.LINE_AA)
    capa = capa + cv2.GaussianBlur(capa, (0, 0), 8) * 1.5
    lz += capa[..., None] * np.float32(color) * op * u
    if txt:
        A.rotulo_serif(lz, [(txt, A.GRIS)], cx, cy, t, t0 + 0.3, px=int(r * 0.9), glow=0.2)


# ------------------------------------------------------------------ GANCHO (0-53 s)
A.firma("g_avion", "avión con empuje fuerte + lluvia diagonal en primer plano + niebla que corre + luz roja del avión que late + barrido de foco + "
        "rótulo fecha + contador de años que sube")


def _rel(nombre, sx, sy, z, c):
    """Punto de la foto (fracciones) que cae en (sx, sy) de pantalla con zoom z y centro c."""
    rgb = D.cargar(D.ruta_img(nombre), 2600)
    hs, ws = rgb.shape[:2]
    s0 = max(W / ws, H / hs) * z
    return (c[0] * ws + (sx - W / 2) / s0) / ws, (c[1] * hs + (sy - H / 2) / s0) / hs


_LUZ_AVION = _rel("cine_avion", W * 0.66, H * 0.26, 1.02, (0.44, 0.54))     # la luz de la cola, medida en el primer cuadro


def g_avion(t, ta, tb):
    cam = dict(z0=1.02, z1=1.28, c0=(0.44, 0.54), c1=(0.56, 0.48))
    lz = toma("cine_avion", t, ta, tb, par=(0, 0), **cam)
    humo(lz, t, sem=1, v=(60, 0), color=(0.55, 0.62, 0.68), op=0.30, zona_y=(0.45, 1.0))
    yy, xx = np.ogrid[0:H, 0:W]
    late = 0.5 + 0.5 * math.sin(t * 6.0)
    lx, ly, kz = ancla("cine_avion", t, ta, tb, _LUZ_AVION, **cam)          # la luz va pegada a la cola del avión
    r = 22.0 * kz
    lz += (np.exp(-((xx - lx) ** 2 + (yy - ly) ** 2) / (2 * r ** 2)) * late * 1.4).astype(np.float32)[..., None] * np.float32((1, 0.15, 0.1))
    barrido_luz(lz, t, T("gancho_0", "1976") + 0.2, dur=1.6, color=(0.75, 0.85, 1.0), op=0.30)
    particulas(lz, t, sem=11, n=260, v=(-160, 900), tam=(1, 2), color=(0.75, 0.82, 0.9), op=0.35, estela=0.03)
    particulas(lz, t, sem=12, n=40, v=(-240, 1400), tam=(2, 4), color=(0.8, 0.85, 0.95), op=0.25, estela=0.04, blur=2.0)
    A.rotulo_serif(lz, [("PARÍS · 26 DE SEPTIEMBRE DE ", A.BLANCO), ("1976", A.ROJO)], W * 0.5, H * 0.13, t, T("gancho_0", "26") + 0.1,
                   px=40, salida=T("gancho_0", "pasajero"))
    A.texto_mixto(lz, [("Un pasajero", A.BLANCO), ("de más de", A.GRIS)], W * 0.07, H * 0.74, t, T("gancho_0", "pasajero"), px=44, salida=tb - 0.3)
    contador(lz, t, T("gancho_0", "tres") - 0.2, 1.0, 0, 3000, W * 0.20, H * 0.85, px=76, sufijo=" años", color=A.ROJO_HALO, salida=tb - 0.3)
    return camara(lz, t, ta, tb, 1.0, 1.04, rot=(0.6, -0.4))


A.firma("g_guardia", "guardia de honor con paneo + porteadores recortados que cruzan desenfocados en primer plano + flashes de prensa + lluvia fina + "
        "etiqueta le bourget + rótulo jefe de estado con arco rojo")


def g_guardia(t, ta, tb):
    lz = toma("cine_guardia", t, ta, tb, z0=1.16, z1=1.24, c0=(0.40, 0.5), c1=(0.60, 0.48), par=(0, 0), ease=lambda u: u)
    flashes(lz, t, ta + 0.4, tb - 0.5, sem=4, n=9)
    particulas(lz, t, sem=13, n=160, v=(-100, 700), tam=(1, 2), color=(0.7, 0.78, 0.85), op=0.28, estela=0.03)
    recorte(lz, IMG + "guardia_siluetas_rec.png", W * 1.25, H * 0.66, 1150, t, ta + 1.6, dur=0.01, deriva=(-520, 0), tono=0.10, blur=9, op=0.95)
    A.etiqueta(lz, "Aeropuerto de Le Bourget", W * 0.63, H * 0.22, t, T("gancho_1", "pista"), px=28, salida=T("gancho_1", "como"))
    t_j = T("gancho_1", "jefe")
    A.arco_luz(lz, (W * 0.22, H * 0.92), (W * 0.78, H * 0.92), 40, e_inout(prog(t, t_j - 0.4, t_j + 0.8)) * 1.3)
    A.rotulo_serif(lz, [("HONORES DE ", A.BLANCO), ("JEFE DE ESTADO", A.ROJO)], W * 0.5, H * 0.85, t, t_j - 0.2, px=42)
    return camara(lz, t, ta, tb, 1.02, 1.0, dx=(-20, 0), temblor=1.5)


@functools.lru_cache(maxsize=1)
def _tarjeta():
    """Ficha de pasaporte ESTILIZADA (no imita un documento real: el pasaporte no consta) con guilloche dibujado."""
    w, h = 900, 600
    im = np.full((h, w, 3), (0.80, 0.74, 0.60), np.float32)
    for i in range(46):
        pts = [(x, int(h * 0.5 + (90 + i * 4) * math.sin(x / (60.0 + i * 1.7) + i * 0.4) * 0.6)) for x in range(0, w, 6)]
        cv2.polylines(im, [np.int32(pts)], False, (0.62, 0.55, 0.42), 1, cv2.LINE_AA)
    cv2.rectangle(im, (40, 40), (w - 40, h - 40), (0.45, 0.38, 0.28), 2, cv2.LINE_AA)
    cv2.rectangle(im, (70, 120), (300, 420), (0.30, 0.26, 0.20), -1)
    im = im * np.linspace(0.75, 1.0, w, dtype=np.float32)[None, :, None]
    return D.Sprite(np.clip(im * 255, 0, 255).astype(np.uint8), None, sombra=True, sr=30, off=(20, 30), sop=0.8)


A.firma("g_pasaporte", "ficha de pasaporte estilizada que gira en 3d al fondo + neón pasaporte + casilla profesión + rey serif gigante + "
        "sello fallecido rojo que golpea + líquido que gotea + polvo")


def g_pasaporte(t, ta, tb):
    lz = negro()
    tj = _tarjeta()
    u = e_out(prog(t, ta, ta + 1.2))
    M = D.poner(tj.w, tj.h, W * 0.5, H * 0.52 + (1 - u) * 300, 1.25, rz=-6 + 4 * math.sin(t * 0.4), ry=-28 + 22 * prog(t, ta, tb), rx=10)
    D.pegar(lz, tj, M, 0.38 * u)
    A.polvo(lz, t, n=80, sem=5, op=0.55)
    barrido_luz(lz, t, T("gancho_2", "en") - 0.4, dur=1.8, color=(1.0, 0.9, 0.7), op=0.22)
    A.neon(lz, "PASAPORTE", W * 0.5, H * 0.42, t, T("gancho_2", "pasaporte") - 0.1, px=84, salida=T("gancho_2", "en") - 0.1)
    t_pro = T("gancho_2", "profesion")
    A.texto_mixto(lz, [("Profesión:", A.GRIS)], W * 0.5 - 300, H * 0.34, t, t_pro, px=44, salida=tb - 0.2)
    A.rotulo_serif(lz, [("REY", A.BLANCO)], W * 0.5, H * 0.46, t, T("gancho_2", "rey"), px=120, vel=0.06, salida=tb - 0.2, glow=0.5)
    t_fa = T("gancho_2", "fallecido")
    A.liquido(lz, W * 0.5, H * 0.67, 460, 330, e_inout(prog(t, t_fa + 0.2, t_fa + 2.4)), t, sem=4, op=0.85)
    D.estampa(lz, "FALLECIDO", W * 0.66, H * 0.60, t, t_fa, px=62, rot=-9.0)
    particulas(lz, t, sem=14, n=50, v=(25, -30), tam=(1, 2.5), color=(1.0, 0.8, 0.6), op=0.35, blur=1.0)
    return camara(lz, t, ta, tb, 1.0, 1.10, rot=(-1.0, 1.0))


def _hojas(lz, t, sem=7, n=7):
    rng = np.random.default_rng(sem)
    for i in range(n):
        x0, fase, vel = rng.uniform(0, W), rng.uniform(0, 6), rng.uniform(60, 120)
        y = (rng.uniform(-200, H) + vel * t) % (H + 300) - 150
        x = x0 + 80 * math.sin(t * 0.8 + fase)
        w, h = 120, 160
        M = D.poner(w, h, x, y, 1.0, rz=40 * math.sin(t * 0.6 + fase), ry=60 * math.sin(t * 0.9 + fase))
        pts = cv2.perspectiveTransform(np.float32([[[0, 0], [w, 0], [w, h], [0, h]]]), M)[0]
        capa = np.zeros((H, W), np.float32)
        cv2.fillConvexPoly(capa, np.int32(pts), 1.0, cv2.LINE_AA)
        capa = cv2.GaussianBlur(capa, (0, 0), 3.0)
        lz[:] = lz * (1 - capa[..., None] * 0.7) + capa[..., None] * np.float32((0.55, 0.50, 0.40)) * 0.7


A.firma("g_archivo", "archivo con avance por el pasillo + haz de linterna que barre + hojas de papel que caen girando + motas grandes desenfocadas + "
        "rótulo sin documento + contador cincuenta años + cursiva encaja")


def g_archivo(t, ta, tb):
    lz = toma("cine_archivo", t, ta, tb, z0=1.0, z1=1.34, c0=(0.45, 0.52), c1=(0.38, 0.50), par=(60, 0))
    lz *= 0.62
    u = (t - ta) / (tb - ta)
    cx, cy = W * (0.30 + 0.45 * (0.5 + 0.5 * math.sin(u * 5.2 - 1.2))), H * (0.42 + 0.08 * math.sin(u * 8.0))
    yy, xx = np.ogrid[0:H, 0:W]
    haz = np.exp(-(((xx - cx) / 300.0) ** 2 + ((yy - cy) / 210.0) ** 2)).astype(np.float32)
    lz *= (1.0 + 1.6 * haz[..., None])
    lz += haz[..., None] * np.float32((0.10, 0.09, 0.07))
    _hojas(lz, t)
    particulas(lz, t, sem=15, n=22, v=(12, 18), tam=(5, 11), color=(1.0, 0.9, 0.7), op=0.25, blur=4.0)
    A.polvo(lz, t, n=90, sem=8, op=0.45, tam=1.8)
    A.rotulo_serif(lz, [("SIN ", A.BLANCO), ("DOCUMENTO", A.ROJO)], W * 0.5, H * 0.15, t, T("gancho_3", "documento"), px=46,
                   salida=T("gancho_3", "pero") + 1.2)
    contador(lz, t, T("gancho_3", "medio") - 0.3, 0.9, 0, 50, W * 0.5, H * 0.15, px=70, sufijo=" años repitiéndose", salida=T("gancho_3", "encaja") - 0.1)
    A.cursiva_luz(lz, "PERO ENCAJA CON ÉL", W * 0.5, H * 0.84, t, T("gancho_3", "encaja"), px=44, salida=tb - 0.1)
    return camara(lz, t, ta, tb, 1.0, 1.03, rot=(0.0, -1.2))


A.firma("g_momia", "pozo de luz ámbar + lámina real de la momia recortada que crece + anillos de luz que se abren detrás + arena que sube + "
        "pregunta en cursiva + líquido que baja al decir muerte + arco de luz")


def g_momia(t, ta, tb):
    lz = negro()
    yy, xx = np.ogrid[0:H, 0:W]
    lz += (np.exp(-(((xx - W * 0.40) / 620.0) ** 2 + ((yy - H * 0.5) / 460.0) ** 2)) * 0.12).astype(np.float32)[..., None] * np.float32((1.0, 0.75, 0.45))
    for i in range(3):
        f = ((t - ta) * 0.35 + i / 3.0) % 1.0
        capa = np.zeros((H, W), np.float32)
        cv2.circle(capa, (int(W * 0.40), int(H * 0.47)), int(260 + 520 * f), 1.0, 2, cv2.LINE_AA)
        lz += cv2.GaussianBlur(capa, (0, 0), 3)[..., None] * np.float32(A.ORO) * 0.9 * (1 - f)
    alto = 900 + 220 * smooth(prog(t, ta, tb))
    A.artefacto(lz, IMG + "momia_frontal_rec.png", W * 0.40, H * 0.52 + (alto - 900) * 0.25, alto, t, ta + 0.1, giro=6.0)
    lz *= np.float32((1.0, 0.93, 0.80))
    particulas(lz, t, sem=16, n=120, v=(8, -45), tam=(1, 2.2), color=(1.0, 0.82, 0.55), op=0.5)
    A.cursiva_luz(lz, "¿QUIÉN ERA?", W * 0.76, H * 0.40, t, T("gancho_4", "quien"), px=60, salida=T("gancho_4", "momia") + 0.6)
    t_mu = T("gancho_4", "muerte")
    A.liquido(lz, W * 0.76, H * 0.47, 220, 260, e_inout(prog(t, t_mu, t_mu + 2.0)), t, sem=6, op=0.7)
    t_cu = T("gancho_4", "cuadrara")
    A.arco_luz(lz, (W * 0.62, H * 0.66), (W * 0.92, H * 0.66), 30, e_inout(prog(t, t_cu - 0.2, t_cu + 0.8)) * 1.3)
    return camara(lz, t, ta, tb, 1.0, 1.07, dx=(30, 0))


A.firma("g_ramses", "piedra + coloso de luxor recortado lejos y desenfocado a contracorriente + busto del joven memnón que sube y gira + "
        "frisos reales de kadesh que corren + brasas + rótulo ramsés ii + cursiva roja lo escribió él mismo + barrido de luz")


def g_ramses(t, ta, tb):
    lz = A.piedra(sem=2).copy()
    recorte(lz, IMG + "luxor_ramses_rec.png", W * 0.78, H * 0.62, 1300, t, ta, desde=(160, 0), dur=1.5, deriva=(-22, 0), tono=0.35, blur=6, op=0.8)
    t_cr = T("gancho_5", "casi")
    banda_relieve(lz, IMG + "kadesh_rameseo.jpg", H * 0.14, 190, t, t_cr - 0.6, vel=70, op=0.20, invertir=True)
    banda_relieve(lz, IMG + "kadesh_rameseo.jpg", H * 0.90, 160, t, t_cr + 0.6, vel=-50, op=0.16, invertir=True)
    A.artefacto(lz, IMG + "joven_memnon_rec.png", W * 0.33, H * 0.55, 900, t, ta + 0.1, giro=11.0)
    A.rotulo_serif(lz, [("RAMSÉS ", A.BLANCO), ("II", A.ROJO)], W * 0.70, H * 0.40, t, T("gancho_5", "ramses"), px=88, vel=0.05)
    A.cursiva_luz(lz, "LO ESCRIBIÓ ÉL MISMO", W * 0.70, H * 0.58, t, T("gancho_5", "escribio"), px=42, color=A.ROJO_HALO)
    barrido_luz(lz, t, T("gancho_5", "mismo"), dur=1.2, op=0.30)
    particulas(lz, t, sem=17, n=70, v=(10, -70), tam=(1, 2.5), color=(1.0, 0.55, 0.2), op=0.7, parpadeo=0.6)
    return camara(lz, t, ta, tb, 1.08, 1.0, dx=(-25, 0), rot=(-0.8, 0.4))


# ------------------------------------------------------------------ CAP. 1: EL NIETO DE UN SOLDADO (53-120 s)
A.firma("n_general", "general ante los carros con empuje y parallax + arena que vuela en estelas + polvo en nubes + sol que late + "
        "capítulo en texto mixto + vena roja que se dibuja + rótulo sin sangre real")


def n_general(t, ta, tb):
    lz = toma("cine_general", t, ta, tb, z0=1.24, z1=1.04, c0=(0.64, 0.48), c1=(0.52, 0.5), par=(0, 0))
    yy, xx = np.ogrid[0:H, 0:W]
    lz += (np.exp(-((xx - W * 0.40) ** 2 + (yy - H * 0.30) ** 2) / (2 * 120.0 ** 2)) * (0.25 + 0.1 * math.sin(t * 2))).astype(np.float32)[..., None] * np.float32((1, 0.35, 0.15))
    humo(lz, t, sem=2, v=(-90, 0), color=(0.75, 0.55, 0.38), op=0.32, zona_y=(0.35, 0.95))
    particulas(lz, t, sem=18, n=220, v=(-700, 30), tam=(1, 2), color=(0.95, 0.75, 0.5), op=0.30, estela=0.05)
    A.texto_mixto(lz, [("Capítulo 1", A.GRIS), ("El nieto de un soldado", A.BLANCO)], W * 0.07, H * 0.12, t, ta + 0.5, px=40,
                  salida=T("nieto_0", "su") - 0.3)
    t_sa = T("nieto_0", "sangre")
    A.arco_luz(lz, (W * 0.10, H * 0.93), (W * 0.90, H * 0.93), -30, e_inout(prog(t, T("nieto_0", "familia") - 0.2, t_sa + 0.4)) * 1.3)
    A.rotulo_serif(lz, [("SIN ", A.BLANCO), ("SANGRE REAL", A.ROJO)], W * 0.5, H * 0.84, t, t_sa - 0.3, px=50)
    return camara(lz, t, ta, tb, 1.0, 1.05, temblor=1.0)


A.firma("n_herencia", "rejilla 3d que avanza + friso de la capilla de ramsés i al fondo + silueta del general que cruza + estatua real de horemheb que sube y se apaga + "
        "aro vacío del heredero que no hubo + camafeo de ramsés i + arco rojo que pasa el trono + rótulo dinastía xix")


def n_herencia(t, ta, tb):
    lz = negro()
    A.rejilla(lz, t, horizonte=0.60, op=0.30, vel=0.35)
    banda_relieve(lz, IMG + "ramses1_relieve.jpg", H * 0.20, 260, t, ta + 0.4, vel=30, color=(0.75, 0.66, 0.5), op=0.30)
    recorte(lz, IMG + "general_rec.png", W * 0.40, H * 0.60, 880, t, T("nieto_1", "su") - 0.2, desde=(260, 0), dur=0.8, deriva=(-60, 0), tono=0.45, blur=2,
            op=0.85, salida=T("nieto_2", "horemheb") - 0.2)
    A.polvo(lz, t, n=60, sem=12, op=0.4)
    t_hor = T("nieto_1", "horemheb")
    t_muere = T("nieto_2", "murio")
    gris = 1.0 - 0.55 * smooth(prog(t, t_muere, t_muere + 1.2))
    sub = lz.copy()
    A.artefacto(sub, IMG + "horemheb_amon_rec.png", W * 0.27, H * 0.52, 700, t, t_hor - 0.3, giro=8.0)
    lz[:] = lz + (sub - lz) * gris
    A.etiqueta(lz, "Horemheb (con el dios Amón)", W * 0.15, H * 0.82, t, t_hor, px=26)
    aro(lz, W * 0.27, H * 0.20, 70, t, T("nieto_2", "hijos"), color=A.GRIS, op=0.7, txt="?")
    t_ab = T("nieto_1", "abuelo")
    A.camafeo(lz, IMG + "ramses1_tumba.jpg", W * 0.72, H * 0.44, 175, t, t_ab, foco=(0.55, 0.20), zoom=2.6)
    A.texto_mixto(lz, [("Ramsés I", A.BLANCO), ("soldado · general · visir", A.GRIS)], W * 0.62, H * 0.68, t, T("nieto_1", "soldado"), px=34)
    t_tr = T("nieto_2", "trono")
    A.arco_luz(lz, (W * 0.33, H * 0.30), (W * 0.66, H * 0.30), -170, e_inout(prog(t, t_tr - 0.2, t_tr + 1.4)) * 1.2)
    A.rotulo_serif(lz, [("DINASTÍA ", A.BLANCO), ("XIX", A.ROJO)], W * 0.5, H * 0.12, t, T("nieto_2", "nacio"), px=54, vel=0.05)
    barrido_luz(lz, t, T("nieto_2", "nacio") + 0.6, dur=1.3, op=0.25)
    return camara(lz, t, ta, tb, 1.0, 1.10, dx=(-40, 10), rot=(0.5, -0.5))


A.firma("n_seti", "toma de seti y el príncipe muy desenfocada y oscura al fondo + humo + cabeza real de la momia de seti i de perfil que gira + "
        "contador dos años + rótulo seti i + cursiva parecer eterna + brasas")


def n_seti(t, ta, tb):
    lz = toma("cine_seti_hijo_b", t, ta, tb, z0=1.3, z1=1.15, c0=(0.6, 0.5), c1=(0.5, 0.5), par=(0, 0))
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 14) * 0.38
    humo(lz, t, sem=3, v=(25, -12), color=(0.6, 0.62, 0.6), op=0.28)
    A.texto_mixto(lz, [("Ramsés I:", A.BLANCO), ("apenas", A.GRIS)], W * 0.07, H * 0.14, t, T("nieto_3", "ramses"), px=38,
                  salida=T("nieto_3", "hijo") + 0.4)
    contador(lz, t, T("nieto_3", "dos") - 0.2, 0.6, 0, 2, W * 0.26, H * 0.24, px=64, sufijo=" años de reinado", color=A.ROJO_HALO,
             salida=T("nieto_3", "hijo") + 0.4)
    t_se = T("nieto_3", "seti")
    A.artefacto(lz, IMG + "seti1_momia_rec.png", W * 0.36, H * 0.56, 760, t, ta + 0.4, giro=14.0)
    A.rotulo_serif(lz, [("SETI ", A.BLANCO), ("I", A.ROJO)], W * 0.72, H * 0.40, t, t_se, px=80, vel=0.05)
    A.cursiva_luz(lz, "PARECER ETERNA", W * 0.72, H * 0.58, t, T("nieto_3", "parecer"), px=46)
    barrido_luz(lz, t, T("nieto_3", "eterna"), dur=1.0, op=0.3)
    particulas(lz, t, sem=19, n=60, v=(15, -60), tam=(1, 2.5), color=(1.0, 0.6, 0.25), op=0.6, parpadeo=0.5)
    return camara(lz, t, ta, tb, 1.06, 1.0, rot=(0.7, -0.3))


A.firma("n_corregente", "seti con la mano en el hombro del príncipe con empuje y desenfoque que enfoca al niño + antorchas que laten + incienso + brasas que suben + "
        "contador catorce + rótulo corregente")


def n_corregente(t, ta, tb):
    lz = toma("cine_seti_hijo", t, ta, tb, z0=1.06, z1=1.30, c0=(0.42, 0.5), c1=(0.58, 0.45), par=(0, 0))
    foco = 1 - smooth(prog(t, T("nieto_4", "hijo") - 0.3, T("nieto_4", "hijo") + 0.6))
    if foco > 0.02:
        lz[:] = lz * (1 - foco) + cv2.GaussianBlur(lz, (0, 0), 9) * foco
    lz *= np.float32(0.90 + 0.10 * math.sin(t * 9.0) * math.sin(t * 3.7))
    humo(lz, t, sem=4, v=(10, -30), color=(0.8, 0.7, 0.55), op=0.25, zona_y=(0.2, 1.0))
    particulas(lz, t, sem=20, n=90, v=(6, -110), tam=(1, 2.5), color=(1.0, 0.55, 0.15), op=0.8, parpadeo=0.7, zona=(0, int(H * 0.3), W, H))
    t14 = T("nieto_4", "catorce")
    contador(lz, t, t14 - 0.5, 0.7, 0, 14, W * 0.5, H * 0.14, px=96, color=A.ROJO_HALO, salida=tb - 0.4)
    A.rotulo_serif(lz, [("CORREGENTE A LOS ", A.BLANCO), ("14 AÑOS", A.ROJO)], W * 0.5, H * 0.86, t, T("nieto_4", "seti") - 0.1, px=44)
    return camara(lz, t, ta, tb, 1.0, 1.03, temblor=0.8)


# mapa_medit a pantalla completa: coordenadas medidas en un cuadro renderizado
# delta del Nilo: costa de x 900 a 1215 en y 775-850; vértice del delta ~(1050, 1000); el valle baja por x ≈ 1050 (previews/_mapa_rejilla.jpg)
_EGIPTO = [(895, 818), (960, 792), (1025, 776), (1100, 790), (1170, 822), (1222, 846), (1150, 905), (1080, 975), (1063, 1000), (1060, 1080), (1040, 1080),
           (1038, 1000), (975, 935), (925, 870)]
_NILO = [(1030, 805), (1040, 860), (1047, 920), (1052, 985), (1050, 1050)]
A.firma("n_campanas", "mapa satelital real con nubes que pasan + egipto en rojo que crece por el nilo + rutas punteadas que marchan a libia y siria con arcos de luz + "
        "etiquetas + obras que se encienden a lo largo del nilo + zoom que sigue cada ruta")


def n_campanas(t, ta, tb):
    lz = toma("mapa_medit", t, ta, tb, z0=1.0, z1=1.04, par=(0, 0))
    lz *= 0.78
    humo(lz, t, sem=5, v=(40, 8), color=(0.9, 0.9, 0.92), op=0.18)
    A.territorio(lz, _EGIPTO, (1050, 1060), e_out(prog(t, ta + 0.2, ta + 2.6)), t, op=0.48, sem=3)
    A.etiqueta(lz, "Egipto", 1170, 960, t, ta + 1.0, px=34)
    t_li, t_si = T("nieto_5", "libia"), T("nieto_5", "siria")
    ul = e_inout(prog(t, t_li - 0.6, t_li + 0.8))
    A.arco_luz(lz, (930, 800), (170, 730), -150, ul * 1.25)
    D.linea_punteada(lz, [(930, 840), (700, 880), (450, 820), (180, 760)], ul, grosor=3, color=(1.0, 0.85, 0.6), op=0.8)
    A.etiqueta(lz, "Libia", 170, 830, t, t_li, px=30)
    us = e_inout(prog(t, t_si - 0.4, t_si + 1.0))
    A.arco_luz(lz, (1230, 830), (1680, 380), -160, us * 1.25)
    D.linea_punteada(lz, [(1240, 850), (1420, 770), (1560, 580), (1670, 390)], us, grosor=3, color=(1.0, 0.85, 0.6), op=0.8)
    A.etiqueta(lz, "Siria", 1700, 360, t, t_si + 0.3, px=30)
    t_ob = T("nieto_5", "obras")
    for i, (x, y) in enumerate(_NILO):
        k = smooth(prog(t, t_ob + 0.25 * i, t_ob + 0.25 * i + 0.4))
        if k > 0:
            r = 9 + 3 * math.sin(t * 5 + i)
            cv2.circle(lz, (int(x), int(y)), int(r * 2.2), tuple(float(c) * 0.25 * k for c in A.ORO), -1, cv2.LINE_AA)
            cv2.circle(lz, (int(x), int(y)), int(r), tuple(float(c) * k for c in A.ORO), -1, cv2.LINE_AA)
    t_le = T("nieto_5", "leccion")
    lz *= 1 - 0.45 * smooth(prog(t, t_le, t_le + 1.0))
    vuelta = smooth(prog(t, t_ob, t_ob + 1.5))         # cámara: hacia Libia, luego Siria, luego vuelve al Nilo
    cxs = lerp(lerp(lerp(0, 200, ul), -220, us), 0, vuelta)
    cys = lerp(lerp(-120, -150, ul), 60, us) * (1 - vuelta) - 120 * vuelta
    return _cam_punto(lz, 1.10 + 0.05 * smooth(prog(t, t_ob, tb)), cxs, cys)


A.firma("n_fabrica", "rejilla que avanza + coloso de luxor en silueta roja que sube por detrás + chispas doradas que caen + texto mixto gobierna + "
        "neón rojo se fabrica + arco de luz + cámara que gira")


def n_fabrica(t, ta, tb):
    lz = negro()
    A.rejilla(lz, t, horizonte=0.66, op=0.22, vel=0.9, paso=140)
    sub = np.zeros_like(lz)
    recorte(sub, IMG + "luxor_ramses_rec.png", W * 0.5, H * 0.62, 1000, t, ta, desde=(0, 520), dur=3.5, blur=3)
    lz += sub * np.float32((0.45, 0.05, 0.04))
    particulas(lz, t, sem=21, n=110, v=(0, 160), tam=(1, 2.2), color=A.ORO, op=0.55, parpadeo=0.5)
    A.texto_mixto(lz, [("Un faraón no solo", A.BLANCO), ("gobierna.", A.GRIS)], W * 0.5 - 330, H * 0.32, t, T("nieto_6", "un"), px=52)
    t_fa = T("nieto_6", "se")
    A.neon(lz, "SE FABRICA", W * 0.5, H * 0.55, t, t_fa - 0.1, px=86)
    A.arco_luz(lz, (W * 0.24, H * 0.68), (W * 0.76, H * 0.68), 60, e_inout(prog(t, t_fa + 0.2, t_fa + 1.4)) * 1.3, color=A.ROJO_HALO)
    return camara(lz, t, ta, tb, 1.12, 1.0, rot=(-2.0, 1.0))


A.firma("n_coronacion", "coronación con empuje profundo hacia el trono + rayos de luz que respiran + incienso + brasas de las antorchas + "
        "rótulo 1279 a. c. + contador veinticuatro años + nombre ramsés ii en cursiva dorada + aura dorada sobre el trono")


def n_coronacion(t, ta, tb):
    lz = toma("cine_coronacion", t, ta, tb, z0=1.0, z1=1.62, c0=(0.5, 0.52), c1=(0.5, 0.46), par=(0, 0))
    rayos(lz, t, W * 0.5, -60, op=0.22)
    humo(lz, t, sem=6, v=(15, -20), color=(0.85, 0.78, 0.65), op=0.24, zona_y=(0.3, 1.0))
    particulas(lz, t, sem=22, n=110, v=(8, -90), tam=(1, 2.5), color=(1.0, 0.6, 0.2), op=0.7, parpadeo=0.6, zona=(0, int(H * 0.35), W, H))
    t_ra = T("nieto_7", "ramses")
    yy, xx = np.ogrid[0:H, 0:W]
    k = smooth(prog(t, t_ra - 0.4, t_ra + 0.6)) * (0.8 + 0.2 * math.sin(t * 4))
    lz += (np.exp(-((xx - W * 0.5) ** 2 + (yy - H * 0.42) ** 2) / (2 * 140.0 ** 2)) * 0.5 * k).astype(np.float32)[..., None] * np.float32(A.ORO)
    A.rotulo_serif(lz, [("1279 ", A.BLANCO), ("a. C.", A.ROJO)], W * 0.5, H * 0.13, t, T("nieto_7", "1279"), px=52,
                   salida=T("nieto_7", "con") - 0.1)
    contador(lz, t, T("nieto_7", "24") - 0.4, 0.6, 0, 24, W * 0.5, H * 0.13, px=60, sufijo=" años", salida=t_ra - 0.4)
    A.cursiva_luz(lz, "RAMSÉS II", W * 0.5, H * 0.84, t, t_ra, px=72, color=A.ORO)
    return camara(lz, t, ta, tb, 1.0, 1.04, rot=(0.0, 0.6))


# ------------------------------------------------------------------ TRANSICIONES INVENTADAS (una por grupo de párrafos; regla del 4-nov)


@functools.lru_cache(maxsize=2)
def _frente(sem):
    r = _ruido(sem)
    return cv2.resize(r, (W, H), interpolation=cv2.INTER_LINEAR)


def tr_arena(Aimg, Bimg, p, t):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    s = e_inout(p)
    d = (xx * 0.8 + yy * 0.45) / (W * 0.8 + H * 0.45)                   # 0..1 en diagonal
    ond = 0.035 * np.sin(yy * 0.011 + xx * 0.004 + 1.3) + 0.018 * np.sin(yy * 0.029 - xx * 0.013 + t * 2.0)   # borde ondulado, sin islas
    frente = s * 1.25 - 0.12 + ond
    m = np.clip((frente - d) / 0.03, 0, 1)
    borde = np.exp(-((frente - d) / 0.010) ** 2) * math.sin(math.pi * p)
    out = Aimg * (1 - m[..., None]) + Bimg * m[..., None]
    out += borde[..., None] * np.float32((1.0, 0.78, 0.45)) * 0.9
    particulas(out, t * 3, sem=31, n=180, v=(-900, -260), tam=(1, 2.5), color=(1.0, 0.82, 0.55), op=0.6 * math.sin(math.pi * p), estela=0.02)
    return out


def _lamina(img, s, dx, dy, rot, borde=True):
    """La imagen como lámina escalada `s` (centro + desplazamiento) con aro claro y sombra; devuelve (rgb, alfa)."""
    M = cv2.getRotationMatrix2D((W / 2, H / 2), rot, s)
    M[:, 2] += (dx, dy)
    rgb = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    a = cv2.warpAffine(np.ones((H, W), np.float32), M, (W, H), borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    if borde:
        ar = cv2.morphologyEx(a, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
        rgb = rgb + cv2.GaussianBlur(ar, (0, 0), 3)[..., None] * 0.7
    return rgb, a


def tr_tunel(Aimg, Bimg, p, t):
    s = e_inout(p)
    fondo = np.full((H, W, 3), NEGRO, np.float32)
    A.rejilla(fondo, t, horizonte=0.5, op=0.18, vel=2.5)
    lado = math.sin(s * math.pi * 1.5)                                    # la cámara va y viene a los lados
    pila = [(Bimg, 0.0), (cv2.GaussianBlur(Bimg, (0, 0), 6) * 0.6, 0.33), (cv2.GaussianBlur(Aimg, (0, 0), 6) * 0.6, 0.66)]
    out = fondo
    for img, prof in pila:                                                # de la más lejana a la más cercana
        z = 0.32 + (1.0 - 0.32) * np.clip(s * 1.35 - prof * 0.55, 0, 1) ** 1.4 + prof * 0.25 * s
        if z > 2.4:
            continue
        dx = (1 - z) * 520 * lado * (1 if prof != 0.33 else -1)
        rgb, a = _lamina(img, z, dx, (1 - z) * 60, (1 - z) * 6 * lado)
        op = 1.0 if prof == 0.0 else max(0.0, 1 - abs(z - 1.0) * 1.2)
        out = out * (1 - a[..., None] * op) + rgb * op
    za = 1.0 + 1.6 * s ** 1.6                                             # la toma vieja se atraviesa
    if za < 2.6:
        rgb, a = _lamina(Aimg, za, -lado * 200 * s, 0, 0, borde=False)
        k = 1 - smooth(prog(s, 0.25, 0.75))
        out = out * (1 - a[..., None] * k) + rgb * k
    return out


TRANS = {"arena": tr_arena, "tunel": tr_tunel}


def _golpes():
    """Golpes de cámara: al empezar cada frase y cada ~2 s dentro de ella (en el arranque de la palabra más cercana)."""
    g = []
    for e in TL["escenas"][:2]:
        for f in e["frases"]:
            ws = f["words"]
            if not ws:
                continue
            g.append(ws[0]["s"])
            sig = ws[0]["s"] + 2.1
            for w in ws[1:]:
                if w["s"] >= sig:
                    g.append(w["s"])
                    sig = w["s"] + 2.1
    return sorted(g)


GOLPES = _golpes()


def golpe(img, t):
    """Empujón breve de cámara (zoom + paso lateral alterno + giro mínimo) en cada golpe: la imagen «respira» con la frase."""
    z, dx, rot = 1.0, 0.0, 0.0
    for i, tg in enumerate(GOLPES):
        dt = t - tg
        if 0 <= dt < 0.9:
            k = math.exp(-dt * 5.5) * math.sin(min(1.0, dt / 0.08) * math.pi / 2)
            z += 0.045 * k
            dx += (28 if i % 2 else -28) * k
            rot += (0.35 if i % 3 else -0.35) * k
    if z == 1.0:
        return img
    return _cam_punto(img, z, dx, 0.0, rot)


# ================================================================== TRAMO 4 (120-576 s): láminas del túnel, una por idea; cada una con su firma
import os as _os


def fs(key):
    return _FR[key]["words"][0]["s"]


def fe(key):
    return _FR[key]["words"][-1]["e"]


def IMGX(nombre):
    """Ruta de un archivo de imagenes/ si existe (el material de Commons puede faltar): None si no."""
    p = IMG + nombre
    return p if _os.path.exists(p) else None


def cine(nombre, t, ta, tb, z0=1.04, z1=1.16, c0=(0.5, 0.5), c1=(0.5, 0.5)):
    return toma("cine_" + nombre, t, ta, tb, z0=z0, z1=z1, c0=c0, c1=c1, par=(0, 0))


def foto(nombre, t, ta, tb, z0=1.04, z1=1.14, c0=(0.5, 0.5), c1=(0.5, 0.5), oscuro=0.75):
    if not IMGX(nombre):
        return negro()
    lz = toma(nombre, t, ta, tb, z0=z0, z1=z1, c0=c0, c1=c1, par=(0, 0))
    return lz * oscuro


def lonlat(lon, lat):
    """Punto del mapa_medit (pantalla completa, sin cámara): medido con Chipre y el mar Muerto en previews/_mapa_rejilla.jpg."""
    return 1505 + (lon - 34.58) * 132.0, 102 + (35.70 - lat) * 163.0


def centrar(img, z, px, py, rot=0.0):
    """Cámara que deja el punto (px, py) del cuadro en el centro con zoom z."""
    return _cam_punto(img, z, -(px - W / 2) * z, -(py - H / 2) * z, rot)


_HATTI = [(1080, 0), (1920, 0), (1920, 300), (1790, 318), (1730, 300), (1690, 250), (1665, 140), (1600, 60), (1450, 28), (1290, 12)]
_CANAAN = [(1480, 800), (1520, 700), (1560, 560), (1600, 460), (1646, 360), (1690, 312), (1780, 330), (1800, 450), (1760, 600), (1720, 790), (1640, 880)]


# ------------------------------------------------------------------ cap. 2: KADESH
A.firma("k_mapa", "mapa satelital con zoom al levante + egipto rojo y canaán que se llenan + imperio hitita gris acero que baja desde anatolia + "
        "kadesh con anillo que late entre los dos + ruta punteada desde el delta + rótulo 1274 a. c.")


def k_mapa(t, ta, tb):
    lz = toma("mapa_medit", t, ta, tb, z0=1.0, z1=1.0, par=(0, 0)) * 0.80
    humo(lz, t, sem=31, v=(-30, 6), color=(0.9, 0.9, 0.92), op=0.16)
    A.territorio(lz, _EGIPTO, (1050, 1060), e_out(prog(t, ta, ta + 1.4)), t, op=0.42, sem=3)
    A.territorio(lz, _CANAAN, (1500, 780), e_out(prog(t, ta + 0.6, ta + 2.6)), t, op=0.34, sem=5)
    t_hi = T("kadesh_1", "imperio")
    A.territorio(lz, _HATTI, (1500, 0), e_out(prog(t, t_hi - 0.3, t_hi + 2.4)), t, color=(0.55, 0.62, 0.70), op=0.50, sem=8)
    kx, ky = lonlat(36.51, 34.56)
    u = e_inout(prog(t, ta + 1.2, ta + 3.4))
    D.linea_punteada(lz, [(1060, 830), (1300, 820), (1490, 760), (1600, 520), (kx, ky)], u, grosor=4, color=(1.0, 0.86, 0.6))
    if t > ta + 3.0:
        r = 22 + 8 * math.sin(t * 4)
        cv2.circle(lz, (int(kx), int(ky)), int(r), (1.0, 0.25, 0.2), 3, cv2.LINE_AA)
    A.etiqueta(lz, "Kadesh", kx + 30, ky - 6, t, ta + 3.0, px=34)
    A.etiqueta(lz, "Hatti", 1500, 150, t, t_hi + 0.8, px=32, color=(0.85, 0.9, 1.0))
    uc = e_inout(prog(t, ta + 0.8, ta + 4.5))
    z = lerp(1.0, 1.55, uc)
    lz = centrar(lz, z, lerp(W / 2, W - W / (2 * z), uc), lerp(H / 2, 420, uc))      # sin salirse del mapa (si no, franjas repetidas)
    A.rotulo_serif(lz, [("KADESH · ", A.BLANCO), ("1274 a. C.", A.ROJO)], W * 0.5, H * 0.10, t, ta + 0.6, px=48)
    return lz


A.firma("k_divisiones", "suelo de rejilla oscuro + cuatro estandartes de las divisiones (amón, ra, ptah, set) que entran uno por dios con su nombre + "
        "columnas de puntos que marchan al norte + flecha norte + campamento de flow muy oscuro detrás")


def k_divisiones(t, ta, tb):
    lz = cine("kadesh_campamento", t, ta, tb, 1.15, 1.25, (0.45, 0.5), (0.55, 0.5))
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 6) * 0.35
    A.rejilla(lz, t, horizonte=0.52, op=0.30, vel=0.5)
    dioses = [("amon", "AMÓN"), ("ra", "RA"), ("ptah", "PTAH"), ("set", "SET")]
    for i, (pal, nom) in enumerate(dioses):
        try:
            t_d = T("kadesh_2", pal, 1 if pal == "ra" else 0)
        except IndexError:
            t_d = fs("kadesh_2") + 4 + i
        x = W * (0.2 + 0.2 * i)
        u = e_out(prog(t, t_d - 0.3, t_d + 0.5))
        if u <= 0:
            continue
        y0 = H * 0.30 + (1 - u) * 160
        cv2.line(lz, (int(x), int(y0)), (int(x), int(H * 0.80)), (0.75 * u, 0.62 * u, 0.40 * u), 4, cv2.LINE_AA)
        cv2.rectangle(lz, (int(x - 48), int(y0)), (int(x + 48), int(y0 + 70)), (0.55 * u, 0.06 * u, 0.06 * u), -1)
        cv2.rectangle(lz, (int(x - 48), int(y0)), (int(x + 48), int(y0 + 70)), (0.95 * u, 0.80 * u, 0.5 * u), 2, cv2.LINE_AA)
        A.rotulo_serif(lz, [(nom, A.BLANCO)], x, y0 + 35, t, t_d - 0.1, px=30, vel=0.02)
        for k in range(14):                                          # soldados (puntos) que marchan al norte
            yy = H * 0.95 - ((t - t_d) * 60 + k * 26) % (H * 0.55)
            xx = x + ((k * 37) % 5 - 2) * 10
            cv2.circle(lz, (int(xx), int(yy)), 4, (0.95 * u, 0.85 * u, 0.6 * u), -1, cv2.LINE_AA)
    A.texto_mixto(lz, [("Cuatro divisiones,", A.BLANCO), ("cada una con el nombre de un dios", A.GRIS)], W * 0.07, H * 0.12, t, T("kadesh_2", "cuatro"), px=36)
    A.polvo(lz, t, n=50, sem=32, op=0.35)
    return camara(lz, t, ta, tb, 1.0, 1.06, dx=(0, -30))


A.firma("k_espias", "dos nómadas de rodillas ante guardias con antorchas que laten + humo bajo + texto de lo que juran + alepo lejos con flecha que se estira + "
        "foco que se cierra sobre sus caras")


def k_espias(t, ta, tb):
    lz = cine("espias", t, ta, tb, 1.05, 1.22, (0.5, 0.5), (0.40, 0.55))
    lz *= np.float32(0.88 + 0.12 * math.sin(t * 8.3) * math.sin(t * 2.9))
    humo(lz, t, sem=33, v=(14, -8), color=(0.7, 0.62, 0.5), op=0.22, zona_y=(0.5, 1.0))
    particulas(lz, t, sem=34, n=70, v=(5, -90), tam=(1, 2.2), color=(1.0, 0.6, 0.2), op=0.7, parpadeo=0.6, zona=(int(W * 0.5), 0, W, H))
    t_j = T("kadesh_3", "juraron")
    A.texto_mixto(lz, [("«Los hititas", A.BLANCO), ("están lejos, en Alepo»", A.GRIS)], W * 0.06, H * 0.80, t, t_j, px=40)
    t_al = T("kadesh_3", "alepo")
    u = e_inout(prog(t, t_al - 0.2, t_al + 1.0))
    if u > 0:
        A.arco_luz(lz, (W * 0.42, H * 0.20), (W * 0.92, H * 0.12), -20, u * 1.2, color=(0.95, 0.85, 0.6))
        A.etiqueta(lz, "Alepo · 150 km al norte", W * 0.70, H * 0.08, t, t_al + 0.4, px=28)
    v = smooth(prog(t, t_j, tb))
    yy, xx = np.ogrid[0:H, 0:W]
    lz *= (1 - 0.55 * v * np.clip(((xx - W * 0.38) ** 2 + (yy - H * 0.55) ** 2) / (W * 0.40) ** 2, 0, 1)).astype(np.float32)[..., None]
    return lz


A.firma("k_mentira", "neón rojo mentían que parpadea y se estabiliza + franja de carros hititas de flow que asoma desde detrás de la ciudad al fondo + "
        "texto eran espías + silueta de la ciudad que tiembla")


def k_mentira(t, ta, tb):
    lz = negro()
    fondo = cine("carros_hititas", t, ta, tb, 1.20, 1.05, (0.5, 0.35), (0.5, 0.45))
    rev = smooth(prog(t, T("kadesh_4", "muwatalli") - 0.3 if _tiene("kadesh_4", "muwatalli") else fs("kadesh_4") + 3, fe("kadesh_4")))
    lz += fondo * (0.15 + 0.55 * rev)
    A.polvo(lz, t, n=80, sem=35, op=0.4)
    A.neon(lz, "MENTÍAN", W * 0.5, H * 0.40, t, fs("kadesh_4") - 0.1, px=110)
    A.cursiva_luz(lz, "ERAN ESPÍAS", W * 0.5, H * 0.58, t, T("kadesh_4", "eran"), px=48)
    A.texto_mixto(lz, [("Muwatalli:", A.BLANCO), ("escondido detrás de la ciudad", A.GRIS)], W * 0.5, H * 0.86, t, T("kadesh_4", "esperaba") - 0.2,
                  px=36, alinear="centro")
    return camara(lz, t, ta, tb, 1.0, 1.08, temblor=1.4 * rev)


def _tiene(key, pal):
    try:
        T(key, pal)
        return True
    except IndexError:
        return False


A.firma("k_carga", "carros hititas de flow a la carga con temblor fuerte + arena que vuela de lado con estela + diagrama encima: bloque de la división de ra "
        "que recibe una flecha roja gruesa + campamento de amón casi solo marcado + destellos")


def k_carga(t, ta, tb):
    lz = cine("carros_hititas", t, ta, tb, 1.08, 1.30, (0.5, 0.5), (0.5, 0.6))
    particulas(lz, t, sem=36, n=260, v=(-900, 40), tam=(1, 2.4), color=(0.9, 0.75, 0.55), op=0.35, estela=0.06)
    humo(lz, t, sem=37, v=(-140, 0), color=(0.8, 0.66, 0.5), op=0.30, zona_y=(0.4, 1.0))
    lz *= 0.85
    t_am = T("kadesh_5", "amon")
    cv2.rectangle(lz, (int(W * 0.08), int(H * 0.10)), (int(W * 0.30), int(H * 0.22)), (0.9, 0.85, 0.7), 2, cv2.LINE_AA)
    A.rotulo_serif(lz, [("CAMPAMENTO DE ", A.BLANCO), ("AMÓN", A.ROJO)], W * 0.19, H * 0.16, t, t_am - 0.2, px=26)
    t_ra = T("kadesh_5", "ra", n=0) if _tiene("kadesh_5", "ra") else fs("kadesh_5") + 5
    u = e_out(prog(t, t_ra - 0.6, t_ra + 0.3))
    if u > 0:
        x0, y0 = W * 0.62, H * 0.28
        cv2.rectangle(lz, (int(x0), int(y0)), (int(x0 + 300), int(y0 + 90)), (0.9, 0.85, 0.7), 2, cv2.LINE_AA)
        A.rotulo_serif(lz, [("DIVISIÓN DE ", A.BLANCO), ("RA", A.ROJO)], x0 + 150, y0 + 45, t, t_ra - 0.4, px=28)
        p = (int(lerp(W * 0.98, x0 + 300, u)), int(y0 + 45))
        cv2.arrowedLine(lz, (int(W * 1.02), int(y0 + 45)), p, (0.95, 0.12, 0.10), 14, cv2.LINE_AA, tipLength=0.25)
    flashes(lz, t, t_ra, tb, sem=38, n=5)
    return camara(lz, t, ta, tb, 1.0, 1.04, temblor=3.0)


A.firma("k_cinco_mil", "contador gigante de carros hasta 5 000 + rejilla de siluetas de carro (del carro real recortado) que se llena en filas desde los dos lados "
        "en dos colores + rótulo la mayor batalla de carros + polvo")


@functools.lru_cache(maxsize=2)
def _silueta_carro(png, alto):
    return np.clip(A._sprite_png(png, alto).a, 0, 1).astype(np.float32)


def k_cinco_mil(t, ta, tb):
    lz = negro()
    A.rejilla(lz, t, horizonte=0.62, op=0.22, vel=0.2)
    png = IMGX("carro_tut_rec.png")
    t_c = T("kadesh_6", "carros")
    n = int(120 * e_out(prog(t, t_c - 0.5, fe("kadesh_6"))))
    if png and n > 0:
        sil = _silueta_carro(png, 56)                                   # silueta del carro real recortado (alfa), una vez
        sh, sw = sil.shape
        for k in range(n):
            lado = k % 2
            fila, col = divmod(k // 2, 11)
            x = (W * 0.05 + col * 74) if lado == 0 else (W * 0.95 - col * 74)
            y = H * 0.52 + fila * 62 + 4 * math.sin(t * 3 + k)
            x0, y0 = int(x - sw / 2), int(y - sh / 2)
            if x0 < 0 or y0 < 0 or x0 + sw > W or y0 + sh > H:
                continue
            a = sil[:, ::-1] if lado else sil                             # los hititas miran al otro lado
            tono = np.float32((0.85, 0.72, 0.5)) if lado == 0 else np.float32((0.55, 0.65, 0.78))
            lz[y0:y0 + sh, x0:x0 + sw] += a[..., None] * tono * 0.8
    contador(lz, t, fs("kadesh_6") + 1.5, 4.5, 0, 5000, W * 0.5, H * 0.24, px=120, sufijo=" carros", color=A.ROJO_HALO)
    A.rotulo_serif(lz, [("LA MAYOR BATALLA DE ", A.BLANCO), ("CARROS", A.ROJO)], W * 0.5, H * 0.40, t, T("kadesh_6", "mayor"), px=40)
    A.etiqueta(lz, "Egipto", W * 0.10, H * 0.46, t, t_c, px=26)
    A.etiqueta(lz, "Hatti", W * 0.84, H * 0.46, t, t_c, px=26, color=(0.8, 0.88, 1.0))
    particulas(lz, t, sem=39, n=120, v=(0, -20), tam=(1, 2), color=(0.9, 0.8, 0.6), op=0.4)
    return camara(lz, t, ta, tb, 1.0, 1.07, rot=(-0.4, 0.4))


A.firma("k_solo", "faraón en su carro de flow rodeado con empuje lento + cita amarilla del poema de kadesh «estaba solo» + polvo dorado que gira + "
        "barrido de luz cuando llegan los refuerzos + rótulo refuerzos")


def k_solo(t, ta, tb):
    lz = cine("faraon_solo", t, ta, tb, 1.02, 1.28, (0.35, 0.5), (0.30, 0.45))
    humo(lz, t, sem=40, v=(-50, -10), color=(0.85, 0.7, 0.5), op=0.25)
    particulas(lz, t, sem=41, n=160, v=(-300, 60), tam=(1, 2.5), color=(1.0, 0.82, 0.5), op=0.45, estela=0.04)
    lz *= 0.82
    A.cita(lz, ["«Estaba solo,", "ninguno conmigo»"], W * 0.72, H * 0.32, t, T("kadesh_7", "relato"), px=46, fuente_txt="Poema de Kadesh (relato del propio faraón)",
           salida=T("kadesh_7", "cierto") - 0.3)
    t_r = T("kadesh_7", "refuerzos")
    barrido_luz(lz, t, t_r - 0.4, dur=1.4, op=0.35)
    A.rotulo_serif(lz, [("RESISTIÓ HASTA LOS ", A.BLANCO), ("REFUERZOS", A.ROJO)], W * 0.66, H * 0.84, t, T("kadesh_7", "resistio"), px=40)
    return lz


A.firma("k_empate", "balanza de bronce dibujada que oscila y queda nivelada (egipto contra hatti) + kadesh que cambia a gris hitita + neón nadie ganó + "
        "egipto que vuelve con flecha punteada hacia el sur")


def k_empate(t, ta, tb):
    lz = A.piedra(sem=41) * 0.7
    A.polvo(lz, t, n=60, sem=42, op=0.35)
    cx, cy = W * 0.5, H * 0.52
    ang = 18 * math.exp(-max(0.0, t - ta - 0.5) * 0.9) * math.sin((t - ta) * 3.2)
    a = math.radians(ang)
    dx, dy = 360 * math.cos(a), 360 * math.sin(a)
    oro = (0.85, 0.66, 0.32)
    cv2.line(lz, (int(cx), int(cy - 220)), (int(cx), int(cy + 230)), oro, 6, cv2.LINE_AA)
    cv2.line(lz, (int(cx - dx), int(cy - 200 - dy)), (int(cx + dx), int(cy - 200 + dy)), oro, 6, cv2.LINE_AA)
    for s, nom, col in ((-1, "EGIPTO", A.ROJO), (1, "HATTI", (0.6, 0.68, 0.8))):
        px_, py_ = cx + s * dx, cy - 200 + s * dy
        cv2.line(lz, (int(px_), int(py_)), (int(px_ - 70), int(py_ + 150)), oro, 2, cv2.LINE_AA)
        cv2.line(lz, (int(px_), int(py_)), (int(px_ + 70), int(py_ + 150)), oro, 2, cv2.LINE_AA)
        cv2.ellipse(lz, (int(px_), int(py_ + 150)), (90, 22), 0, 0, 180, oro, 5, cv2.LINE_AA)
        A.rotulo_serif(lz, [(nom, col)], px_, py_ + 200, t, ta + 0.3, px=34)
    A.neon(lz, "NADIE GANÓ", W * 0.5, H * 0.12, t, T("kadesh_8", "nadie"), px=72, barras=False)
    A.texto_mixto(lz, [("Kadesh:", A.BLANCO), ("se quedó hitita", A.GRIS)], W * 0.06, H * 0.88, t, T("kadesh_8", "hititas"), px=36)
    A.texto_mixto(lz, [("Egipto:", A.BLANCO), ("a casa sin la ciudad", A.GRIS)], W * 0.62, H * 0.88, t, T("kadesh_8", "egipto"), px=36)
    return camara(lz, t, ta, tb, 1.04, 1.0)


A.firma("k_historia", "escultores tallando el muro por antorchas con empuje + chispas de cincel que saltan en ráfagas + neón una historia + "
        "cinco templos que se encienden en fila a lo largo de una línea del nilo, de abydos a abu simbel")


def k_historia(t, ta, tb):
    lz = cine("escultores", t, ta, tb, 1.05, 1.20, (0.55, 0.45), (0.45, 0.45))
    lz *= np.float32(0.85 + 0.1 * math.sin(t * 7.1))
    for k in range(4):
        tk = ta + 1.0 + k * 1.7
        if tk < t < tk + 0.6:
            particulas(lz, t - tk, sem=43 + k, n=40, v=(120 * (1 if k % 2 else -1), -180), tam=(1, 2), color=(1, 0.85, 0.5), op=0.9,
                       zona=(int(W * (0.3 + 0.12 * k)), int(H * 0.3), int(W * (0.36 + 0.12 * k)), int(H * 0.5)))
    A.neon(lz, "UNA HISTORIA", W * 0.5, H * 0.14, t, T("kadesh_9", "historia") - 0.2, px=70, salida=fs("kadesh_10") + 0.5)
    t_c = T("kadesh_10", "cinco")
    if t > t_c - 0.3:
        lz *= 1 - 0.45 * smooth(prog(t, t_c - 0.3, t_c + 0.4))
        temp = ["Abydos", "Karnak", "Luxor", "Rameseo", "Abu Simbel"]
        y = H * 0.72
        u = e_inout(prog(t, t_c, t_c + 0.8))
        cv2.line(lz, (int(W * 0.10), int(y)), (int(lerp(W * 0.10, W * 0.90, u)), int(y)), (0.6, 0.5, 0.35), 3, cv2.LINE_AA)
        for i, nom in enumerate(temp):
            ti = t_c + 0.35 + 0.45 * i
            x = W * (0.12 + 0.19 * i)
            k = smooth(prog(t, ti, ti + 0.3))
            if k > 0:
                cv2.circle(lz, (int(x), int(y)), int(14 + 3 * math.sin(t * 5 + i)), (1.0 * k, 0.75 * k, 0.3 * k), -1, cv2.LINE_AA)
                A.etiqueta(lz, nom, x - 40, y + 50, t, ti, px=28, punto=False)
        A.rotulo_serif(lz, [("CINCO ", A.ROJO), ("TEMPLOS", A.BLANCO)], W * 0.5, H * 0.58, t, t_c, px=46)
    return lz


A.firma("k_propaganda", "relieve real de kadesh en el rameseo que corre como friso arriba y abajo + empate tachado con trazo rojo a mano y victoria eterna que "
        "se escribe encima + neón propaganda + sello rojo que cae")


def k_propaganda(t, ta, tb):
    lz = negro()
    banda_relieve(lz, IMG + "kadesh_rameseo.jpg", H * 0.12, 220, t, ta, vel=55, color=(0.85, 0.7, 0.5), op=0.35)
    banda_relieve(lz, IMG + "kadesh_rameseo.jpg", H * 0.90, 220, t, ta, vel=-45, color=(0.85, 0.7, 0.5), op=0.30, invertir=True)
    A.polvo(lz, t, n=50, sem=48, op=0.35)
    A.rotulo_serif(lz, [("EMPATE", A.BLANCO)], W * 0.5, H * 0.36, t, fs("kadesh_11"), px=70)
    t_v = T("kadesh_11", "victoria")
    D.marcador_mano(lz, "tachado", W * 0.5, H * 0.36, 360, 70, e_out(prog(t, t_v - 0.6, t_v - 0.1)))
    A.cursiva_luz(lz, "VICTORIA ETERNA", W * 0.5, H * 0.50, t, t_v, px=64, color=A.ROJO_HALO)
    t_p = T("kadesh_11", "propaganda")
    A.neon(lz, "PROPAGANDA", W * 0.5, H * 0.68, t, t_p - 0.2, px=84)
    D.estampa(lz, "1274 a. C.", W * 0.80, H * 0.76, t, t_p + 0.8, px=40)
    return camara(lz, t, ta, tb, 1.0, 1.08, rot=(0.6, -0.6))


# ------------------------------------------------------------------ cap. 3: EL TRATADO
A.firma("t_frontera", "mapa del levante con la frontera egipto-hatti que chisporrotea (choques) en 15 destellos + contador de años 0 a 15 + "
        "dos territorios que dejan de latir + rótulo 1259 a. c. la paz")


def t_frontera(t, ta, tb):
    lz = toma("mapa_medit", t, ta, tb, z0=1.0, z1=1.0, par=(0, 0)) * 0.70
    A.territorio(lz, _CANAAN, (1500, 780), 1.0, t, op=0.30, sem=5)
    A.territorio(lz, _HATTI, (1500, 0), 1.0, t, color=(0.55, 0.62, 0.70), op=0.42, sem=8)
    frontera = [(1646, 360), (1690, 312), (1780, 330), (1860, 330)]
    t_q = T("tratado_1", "quince")
    t_p = T("tratado_1", "paz")
    calma = smooth(prog(t, t_p - 0.4, t_p + 1.0))
    for i in range(15):
        tk = t_q - 0.6 + i * 0.25
        if tk < t < tk + 0.5 and calma < 0.5:
            px_, py_ = frontera[i % 4]
            r = int(30 * (1 - (t - tk) / 0.5))
            cv2.circle(lz, (int(px_ + (i * 13) % 40 - 20), int(py_)), max(1, r), (1.0, 0.6, 0.2), 2, cv2.LINE_AA)
    col = (lerp(1.0, 0.95, calma), lerp(0.3, 0.92, calma), lerp(0.2, 0.85, calma))
    cv2.polylines(lz, [np.int32(frontera)], False, col, 5, cv2.LINE_AA)
    lz = centrar(lz, 1.35, 1209, 420)
    contador(lz, t, t_q - 0.4, 3.0, 0, 15, W * 0.5, H * 0.14, px=90, sufijo=" años de choques", color=A.ROJO_HALO, salida=t_p - 0.2)
    A.rotulo_serif(lz, [("1259 a. C. · ", A.BLANCO), ("LA PAZ", A.ROJO)], W * 0.5, H * 0.14, t, t_p, px=56)
    return lz


A.firma("t_pacto", "enviados de flow intercambiando la tablilla con empuje lento + tres cláusulas que entran como lista con marca de visto + "
        "luz de lámparas que respira + rótulo hattusili iii")


def t_pacto(t, ta, tb):
    lz = cine("tratado_firma", t, ta, tb, 1.02, 1.18, (0.5, 0.5), (0.55, 0.45))
    lz *= np.float32(0.80 + 0.08 * math.sin(t * 2.3))
    humo(lz, t, sem=50, v=(8, -14), color=(0.8, 0.7, 0.55), op=0.18)
    clausulas = [("atacarse", "No atacarse"), ("ayudarse", "Ayudarse contra cualquier enemigo"), ("devolverse", "Devolverse a los fugitivos")]
    for i, (pal, txt) in enumerate(clausulas):
        tc = T("tratado_2", pal) if _tiene("tratado_2", pal) else fs("tratado_2") + 4 + 1.5 * i
        y = H * (0.60 + 0.09 * i)
        k = e_out(prog(t, tc - 0.2, tc + 0.3))
        if k > 0:
            cv2.rectangle(lz, (int(W * 0.06), int(y - 20)), (int(W * 0.06 + 40), int(y + 20)), (0.95 * k, 0.9 * k, 0.8 * k), 2, cv2.LINE_AA)
            if t > tc + 0.3:
                cv2.polylines(lz, [np.int32([(W * 0.06 + 8, y), (W * 0.06 + 18, y + 12), (W * 0.06 + 36, y - 16)])], False, (0.95, 0.15, 0.12), 5, cv2.LINE_AA)
            A.texto_mixto(lz, [(txt, A.BLANCO)], W * 0.06 + 64, y, t, tc - 0.1, px=34)
    A.rotulo_serif(lz, [("RAMSÉS II ", A.BLANCO), ("+", A.ROJO), (" HATTUSILI III", A.BLANCO)], W * 0.5, H * 0.10, t, T("tratado_2", "nuevo"), px=42)
    return lz


A.firma("t_doble", "pantalla partida: muro de karnak a la izquierda con paneo vertical y tablilla de arcilla real que sube y gira sobre piedra a la derecha + "
        "línea de luz que las une + etiquetas karnak y estambul + rótulo el tratado de paz más antiguo")


def t_doble(t, ta, tb):
    lz = A.piedra(sem=52) * 0.8
    izq = foto("tratado_karnak.jpg", t, ta, tb, 1.25, 1.35, (0.5, 0.3), (0.5, 0.7), oscuro=0.8) if IMGX("tratado_karnak.jpg") else \
        foto("kadesh_rameseo.jpg", t, ta, tb, 1.3, 1.4, (0.3, 0.4), (0.4, 0.6))
    m = int(W * 0.48)
    u = e_out(prog(t, ta, ta + 0.8))
    lz[:, :int(m * u)] = izq[:, W // 2 - int(m * u) // 2: W // 2 - int(m * u) // 2 + int(m * u)]
    cv2.line(lz, (int(m * u), 0), (int(m * u), H), (0.9, 0.85, 0.75), 3, cv2.LINE_AA)
    png = IMGX("tratado_tablilla_rec.png")
    t_es = T("tratado_4", "estambul") if _tiene("tratado_4", "estambul") else fs("tratado_4") + 2
    if png:
        A.artefacto(lz, png, W * 0.74, H * 0.50, 620, t, fs("tratado_4") - 0.3, giro=10.0)
    else:
        A.camafeo(lz, IMG + "tratado_estambul.jpg", W * 0.74, H * 0.48, 230, t, fs("tratado_4") - 0.3, foco=(0.5, 0.5), zoom=1.2)
    A.etiqueta(lz, "Karnak · jeroglíficos", W * 0.05, H * 0.92, t, T("tratado_3", "karnak"), px=28)
    A.etiqueta(lz, "Estambul · arcilla hitita", W * 0.58, H * 0.92, t, t_es, px=28)
    A.rotulo_serif(lz, [("EL TRATADO DE PAZ ", A.BLANCO), ("MÁS ANTIGUO", A.ROJO)], W * 0.5, H * 0.08, t, T("tratado_3", "antiguo") - 0.2, px=44)
    A.cursiva_luz(lz, "POR PARTIDA DOBLE", W * 0.74, H * 0.18, t, T("tratado_3", "doble") - 0.2, px=40)
    return camara(lz, t, ta, tb, 1.0, 1.05)


A.firma("t_onu", "réplica de cobre en la onu con paneo y destello metálico que la recorre + contador 1970 + bandera en etiqueta + rótulo onu nueva york + "
        "marco de luz azul de la sala")


def t_onu(t, ta, tb):
    n = "tratado_onu.jpg" if IMGX("tratado_onu.jpg") else "tratado_estambul.jpg"
    lz = foto(n, t, ta, tb, 1.05, 1.22, (0.5, 0.45), (0.5, 0.55), oscuro=0.72)
    lz += np.float32((0.0, 0.02, 0.05))
    barrido_luz(lz, t, ta + 1.2, dur=2.0, color=(1.0, 0.75, 0.5), op=0.35)
    contador(lz, t, T("tratado_5", "1970") - 0.6 if _tiene("tratado_5", "1970") else ta + 2, 1.0, 1259, 1970, W * 0.80, H * 0.20, px=70, color=A.BLANCO)
    A.rotulo_serif(lz, [("ONU · ", A.BLANCO), ("NUEVA YORK", A.ROJO)], W * 0.5, H * 0.88, t, T("tratado_5", "onu") - 0.1, px=48)
    A.etiqueta(lz, "Réplica en cobre · regalo de Turquía", W * 0.05, H * 0.10, t, T("tratado_5", "cobre"), px=28)
    return lz


A.firma("t_boda", "caravana de la princesa hitita de flow con paneo lateral largo + pétalos/polvo dorado que cae + aros entrelazados de luz (egipto y hatti) + "
        "rótulo boda diplomática")


def t_boda(t, ta, tb):
    lz = cine("princesa", t, ta, tb, 1.18, 1.18, (0.38, 0.5), (0.62, 0.5))
    particulas(lz, t, sem=55, n=90, v=(30, 50), tam=(1.5, 3), color=(1.0, 0.85, 0.45), op=0.6, parpadeo=0.4)
    t_c = T("tratado_6", "caso")
    u = e_out(prog(t, t_c - 0.2, t_c + 0.8))
    if u > 0:
        capa = np.zeros((H, W), np.float32)
        cv2.circle(capa, (int(W * 0.46), int(H * 0.24)), int(70 * u), 1.0, 3, cv2.LINE_AA)
        cv2.circle(capa, (int(W * 0.54), int(H * 0.24)), int(70 * u), 1.0, 3, cv2.LINE_AA)
        lz += (capa + cv2.GaussianBlur(capa, (0, 0), 8) * 1.4)[..., None] * np.float32((1.0, 0.8, 0.45)) * 0.9
    A.rotulo_serif(lz, [("BODA ", A.BLANCO), ("DIPLOMÁTICA", A.ROJO)], W * 0.5, H * 0.86, t, T("tratado_6", "princesa") - 0.2, px=46)
    A.texto_mixto(lz, [("El pacto", A.BLANCO), ("se sella con una boda", A.GRIS)], W * 0.06, H * 0.10, t, T("tratado_6", "pacto"), px=34)
    return lz


# ------------------------------------------------------------------ cap. 4: EL CONSTRUCTOR
A.firma("c_nombre", "cartucho de ramsés real sobre piedra con luz rasante que lo recorre + el nombre ramsés que se talla letra a letra con chispas + "
        "texto escribir su nombre en piedra + polvo de piedra que cae")


def c_nombre(t, ta, tb):
    lz = A.piedra(sem=60, tono=(0.14, 0.13, 0.12))
    if IMGX("cartucho_ramses.jpg"):
        A.camafeo(lz, IMG + "cartucho_ramses.jpg", W * 0.30, H * 0.50, 300, t, ta + 0.2, foco=(0.5, 0.5), zoom=1.0)
    t_n = T("constructor_0", "nombre")
    A.rotulo_serif(lz, [("RAMSÉS", A.ROJO)], W * 0.68, H * 0.46, t, t_n - 0.4, px=110, vel=0.12)
    for k in range(6):
        tk = t_n - 0.4 + 0.12 * k
        if tk < t < tk + 0.5:
            particulas(lz, t - tk, sem=61 + k, n=25, v=(80, -120), tam=(1, 2), color=(1, 0.85, 0.5), op=0.9,
                       zona=(int(W * (0.52 + 0.055 * k)), int(H * 0.42), int(W * (0.56 + 0.055 * k)), int(H * 0.5)))
    A.texto_mixto(lz, [("Lo que mejor sabía hacer:", A.GRIS), ("escribir su nombre en piedra", A.BLANCO)], W * 0.5, H * 0.82, t,
                  T("constructor_0", "escribir") - 0.3, px=38, alinear="centro")
    A.polvo(lz, t, n=70, sem=66, op=0.4)
    yy = (np.arange(W, dtype=np.float32)[None, :] - lerp(-400, W + 400, prog(t, ta, tb)))
    lz *= (1 + 0.35 * np.exp(-(yy / 260.0) ** 2))[..., None]
    return camara(lz, t, ta, tb, 1.02, 1.0)


A.firma("c_piramses", "vista aérea de pi-ramsés de flow con vuelo lento hacia el delta + barcos (puntos de luz) que navegan los canales + "
        "punto del delta en minimapa que late + rótulo la casa de ramsés")


def c_piramses(t, ta, tb):
    lz = cine("piramses", t, ta, tb, 1.0, 1.25, (0.5, 0.6), (0.55, 0.45))
    for k in range(10):
        x = (W * 0.2 + (t - ta) * (20 + k * 4) + k * 170) % W
        y = H * (0.55 + 0.03 * math.sin(k * 1.7))
        cv2.circle(lz, (int(x), int(y)), 3, (1.0, 0.85, 0.55), -1, cv2.LINE_AA)
    mini = cv2.resize(toma("mapa_medit", 0, 0, 1, z0=1.0, z1=1.0, par=(0, 0)), (W // 5, H // 5), interpolation=cv2.INTER_AREA) * 0.85
    x0, y0 = int(W * 0.77), int(H * 0.06)
    k = smooth(prog(t, ta + 0.6, ta + 1.3))
    lz[y0:y0 + mini.shape[0], x0:x0 + mini.shape[1]] = lz[y0:y0 + mini.shape[0], x0:x0 + mini.shape[1]] * (1 - k) + mini * k
    cv2.rectangle(lz, (x0, y0), (x0 + mini.shape[1], y0 + mini.shape[0]), (0.9 * k, 0.85 * k, 0.75 * k), 2)
    px_, py_ = x0 + 1060 / 5, y0 + 820 / 5
    cv2.circle(lz, (int(px_), int(py_)), int(6 + 3 * math.sin(t * 5)), (1.0 * k, 0.2 * k, 0.15 * k), -1, cv2.LINE_AA)
    A.rotulo_serif(lz, [("PI-RAMSÉS · ", A.BLANCO), ("LA CASA DE RAMSÉS", A.ROJO)], W * 0.42, H * 0.88, t, T("constructor_1", "pi") - 0.1 if _tiene("constructor_1", "pi") else ta + 2, px=44)
    return lz


A.firma("c_rameseo", "rameseo real con paneo + regla vertical de escala que sube hasta 20 m junto a una silueta humana diminuta + contador de metros + "
        "texto su templo funerario")


def c_rameseo(t, ta, tb):
    n = "rameseo_vista.jpg" if IMGX("rameseo_vista.jpg") else "rameseo_coloso.jpg"
    lz = foto(n, t, ta, tb, 1.08, 1.22, (0.45, 0.5), (0.55, 0.45), oscuro=0.70)
    t_v = T("constructor_2", "veinte") if _tiene("constructor_2", "veinte") else fs("constructor_2") + 5
    u = e_inout(prog(t, t_v - 1.0, t_v + 0.4))
    x, yb = W * 0.86, H * 0.86
    ytop = yb - u * H * 0.66
    cv2.line(lz, (int(x), int(yb)), (int(x), int(ytop)), (0.95, 0.9, 0.8), 3, cv2.LINE_AA)
    for k in range(11):
        yy = yb - k * H * 0.066
        if yy >= ytop:
            cv2.line(lz, (int(x - 12), int(yy)), (int(x + 12), int(yy)), (0.95, 0.9, 0.8), 2, cv2.LINE_AA)
    cv2.ellipse(lz, (int(x - 40), int(yb - 22)), (5, 5), 0, 0, 360, (0.95, 0.9, 0.8), -1)
    cv2.line(lz, (int(x - 40), int(yb - 16)), (int(x - 40), int(yb)), (0.95, 0.9, 0.8), 3)
    contador(lz, t, t_v - 1.0, 1.4, 0, 19, x - 70, ytop - 40, px=54, sufijo=" m", color=A.ROJO_HALO)
    A.texto_mixto(lz, [("El Rameseo:", A.BLANCO), ("su templo funerario en Tebas", A.GRIS)], W * 0.06, H * 0.10, t, T("constructor_2", "tebas") - 0.4, px=36)
    return lz


A.firma("c_abusimbel", "fachada real de abu simbel con empuje + cuatro aros de luz que se posan uno a uno sobre las caras de los colosos + x4 + "
        "contador más de 3 000 años + montaña tallada con rótulo nubia")


def c_abusimbel(t, ta, tb):
    lz = foto("Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", t, ta, tb, 1.02, 1.10, (0.5, 0.45), (0.5, 0.42), oscuro=0.78)
    t_m = T("constructor_3", "montana") if _tiene("constructor_3", "montana") else fs("constructor_3") + 3
    A.rotulo_serif(lz, [("NUBIA · ", A.BLANCO), ("ABU SIMBEL", A.ROJO)], W * 0.5, H * 0.08, t, t_m, px=48, salida=fs("constructor_4") + 2)
    t_c = T("constructor_4", "colosos") if _tiene("constructor_4", "colosos") else fs("constructor_4") + 0.6
    for i, fx in enumerate((0.29, 0.40, 0.60, 0.71)):
        aro(lz, W * fx, H * 0.44, 62, t, t_c + 0.25 * i, color=A.ORO, op=0.8)
    A.rotulo_serif(lz, [("×4 · ", A.ROJO), ("TODOS CON SU CARA", A.BLANCO)], W * 0.5, H * 0.08, t, T("constructor_4", "cara") - 0.2 if _tiene("constructor_4", "cara") else t_c + 2, px=44)
    contador(lz, t, T("constructor_4", "tres") - 0.3 if _tiene("constructor_4", "tres") else t_c + 3, 1.2, 0, 3000, W * 0.5, H * 0.86, px=64,
             sufijo=" años vigilando el río", color=A.BLANCO)
    return lz


A.firma("c_sol", "pasillo del santuario de flow en penumbra + rayo de sol que avanza por el pasillo y enciende las cuatro estatuas + motas en el rayo + "
        "calendario 22 de febrero y 22 de octubre que se marca con círculo rojo")


def c_sol(t, ta, tb):
    lz = cine("sol_santuario", t, ta, tb, 1.10, 1.30, (0.55, 0.5), (0.62, 0.5))
    t_s = T("constructor_5", "sol") if _tiene("constructor_5", "sol") else fs("constructor_5") + 5
    luz = smooth(prog(t, t_s - 0.5, t_s + 2.5))
    lz *= 0.45 + 0.55 * luz
    rayos(lz, t, W * 0.95, H * 0.18, op=0.35 * luz, color=(1.0, 0.8, 0.45), n=10, sem=70)
    particulas(lz, t, sem=71, n=120, v=(-30, 12), tam=(1, 2.2), color=(1.0, 0.9, 0.6), op=0.6 * luz, zona=(int(W * 0.4), 0, W, int(H * 0.7)))
    for i, (pal, txt) in enumerate((("febrero", "22 FEB"), ("octubre", "22 OCT"))):
        tc = T("constructor_5", pal) if _tiene("constructor_5", pal) else fs("constructor_5") + 2 + 2 * i
        x, y = W * (0.10 + 0.17 * i), H * 0.16
        k = e_out(prog(t, tc - 0.2, tc + 0.3))
        if k > 0:
            cv2.rectangle(lz, (int(x - 70), int(y - 50)), (int(x + 70), int(y + 50)), (0.92 * k, 0.88 * k, 0.8 * k), 2, cv2.LINE_AA)
            A.rotulo_serif(lz, [(txt, A.BLANCO)], x, y, t, tc - 0.1, px=36)
            D.marcador_mano(lz, "circulo", x, y, 170, 120, e_out(prog(t, tc + 0.3, tc + 0.9)), semilla=i)
    A.texto_mixto(lz, [("El sol del amanecer", A.BLANCO), ("alumbra su estatua", A.GRIS)], W * 0.06, H * 0.86, t, T("constructor_5", "alumbra") - 0.2 if _tiene("constructor_5", "alumbra") else t_s, px=36)
    return lz


A.firma("c_borrar", "manos de flow con el cincel que borra un cartucho + chispas de piedra en ráfagas + nombre viejo en gris tachado y ramsés en rojo que se escribe "
        "encima + pantalla que se llena de cartuchos rojos (su nombre por todo egipto)")


def c_borrar(t, ta, tb):
    lz = cine("cincel", t, ta, tb, 1.05, 1.25, (0.45, 0.5), (0.4, 0.5))
    for k in range(5):
        tk = ta + 0.5 + k * 1.3
        if tk < t < tk + 0.5:
            particulas(lz, t - tk, sem=75 + k, n=40, v=(160, -140), tam=(1, 2.4), color=(1, 0.85, 0.55), op=0.9,
                       zona=(int(W * 0.40), int(H * 0.40), int(W * 0.48), int(H * 0.50)))
    t_b = T("constructor_6", "borrar")
    A.rotulo_serif(lz, [("NOMBRE ANTERIOR", A.GRIS)], W * 0.76, H * 0.30, t, t_b - 0.2, px=40)
    D.marcador_mano(lz, "tachado", W * 0.76, H * 0.30, 420, 60, e_out(prog(t, t_b + 0.6, t_b + 1.2)), semilla=2)
    A.rotulo_serif(lz, [("RAMSÉS", A.ROJO)], W * 0.76, H * 0.42, t, T("constructor_6", "suyo") - 0.2 if _tiene("constructor_6", "suyo") else t_b + 2, px=70)
    t_t = T("constructor_7", "todo")
    n = int(28 * e_out(prog(t, t_t - 0.3, t_t + 2.0)))
    rng = np.random.default_rng(77)
    pts = rng.random((28, 2))
    for k in range(n):
        x, y = W * (0.05 + 0.9 * pts[k, 0]), H * (0.08 + 0.84 * pts[k, 1])
        cv2.ellipse(lz, (int(x), int(y)), (50, 20), 0, 0, 360, (0.95, 0.74, 0.32), 3, cv2.LINE_AA)
        cv2.line(lz, (int(x + 50), int(y - 16)), (int(x + 50), int(y + 16)), (0.95, 0.74, 0.32), 3, cv2.LINE_AA)
    A.cursiva_luz(lz, "SOBRE OBRAS QUE NO ERAN SUYAS", W * 0.5, H * 0.88, t, T("constructor_7", "obras") - 0.2, px=40, color=A.ROJO_HALO)
    return lz


# ------------------------------------------------------------------ cap. 5: LA FAMILIA
A.firma("f_nefertari", "reina de flow que camina por el pasillo con paneo que la acompaña + pétalos de luz + camafeo de la tumba qv66 real que flota + "
        "rótulo gran esposa real + aura dorada")


def f_nefertari(t, ta, tb):
    lz = cine("nefertari_reina", t, ta, tb, 1.15, 1.15, (0.42, 0.5), (0.58, 0.5))
    lz *= np.float32(0.86 + 0.06 * math.sin(t * 3.1))
    particulas(lz, t, sem=80, n=70, v=(10, -25), tam=(1, 2.5), color=(1.0, 0.85, 0.55), op=0.55, parpadeo=0.5)
    A.rotulo_serif(lz, [("NEFERTARI", A.ROJO)], W * 0.24, H * 0.16, t, T("familia_0", "nefertari") - 0.1, px=62)
    A.cursiva_luz(lz, "GRAN ESPOSA REAL", W * 0.24, H * 0.27, t, T("familia_0", "esposa"), px=34)
    A.camafeo(lz, IMG + "nefertari_qv66.jpg", W * 0.80, H * 0.60, 170, t, T("familia_0", "tumba") - 0.2, foco=(0.5, 0.35), zoom=1.4)
    A.etiqueta(lz, "Tumba QV66 · Valle de las Reinas", W * 0.66, H * 0.86, t, T("familia_0", "valle") - 0.2 if _tiene("familia_0", "valle") else ta + 6, px=26)
    return lz


A.firma("f_esposas", "árbol genealógico de luz sobre negro: ramsés en el centro, esposas reales como nodos dorados y decenas de esposas menores como "
        "constelación de puntos que aparecen + líneas que se trazan")


def f_esposas(t, ta, tb):
    lz = negro()
    A.polvo(lz, t, n=60, sem=81, op=0.3)
    cx, cy = W * 0.5, H * 0.52
    A.camafeo(lz, IMG + "luxor_ramses.jpg", cx, cy, 110, t, ta, foco=(0.5, 0.62), zoom=1.3)
    t_v = T("familia_1", "varias")
    for i in range(7):
        ang = -math.pi / 2 + i * 2 * math.pi / 7
        x, y = cx + 300 * math.cos(ang), cy + 260 * math.sin(ang)
        k = e_out(prog(t, t_v + 0.15 * i, t_v + 0.15 * i + 0.4))
        if k > 0:
            cv2.line(lz, (int(cx), int(cy)), (int(lerp(cx, x, k)), int(lerp(cy, y, k))), (0.8 * k, 0.65 * k, 0.35 * k), 2, cv2.LINE_AA)
            cv2.circle(lz, (int(x), int(y)), 18, (1.0 * k, 0.78 * k, 0.35 * k), -1, cv2.LINE_AA)
    t_d = T("familia_1", "decenas")
    rng = np.random.default_rng(82)
    pts = rng.random((60, 2))
    n = int(60 * e_out(prog(t, t_d - 0.2, t_d + 1.8)))
    for k in range(n):
        ang = pts[k, 0] * 2 * math.pi
        r = 420 + 160 * pts[k, 1]
        x, y = cx + r * math.cos(ang) * 1.5, cy + r * math.sin(ang) * 0.85
        cv2.circle(lz, (int(x), int(y)), 5, (0.75, 0.75, 0.8), -1, cv2.LINE_AA)
    A.texto_mixto(lz, [("Varias esposas reales", A.BLANCO), ("y decenas de esposas menores", A.GRIS)], W * 0.5, H * 0.92, t, t_v, px=34, alinear="centro")
    A.rotulo_serif(lz, [("NO FUE LA ", A.BLANCO), ("ÚNICA", A.ROJO)], W * 0.5, H * 0.08, t, fs("familia_1"), px=44)
    return camara(lz, t, ta, tb, 1.08, 1.0, rot=(-0.6, 0.6))


A.firma("f_hijos", "cien figuras de hijos e hijas (dos colores) que se encienden en una cuadrícula al ritmo del contador + friso real de la procesión de hijos "
        "que corre abajo + rótulo muchos")


def f_hijos(t, ta, tb):
    lz = negro()
    if IMGX("hijos_procesion.jpg"):
        banda_relieve(lz, IMG + "hijos_procesion.jpg", H * 0.88, 200, t, ta, vel=40, color=(0.85, 0.72, 0.5), op=0.6)
    A.neon(lz, "MUCHOS", W * 0.5, H * 0.12, t, min(T("familia_2", "muchos") - 0.1, ta + 0.5), px=80, barras=False)
    t_l = T("familia_2", "cincuenta") if _tiene("familia_2", "cincuenta") else fs("familia_2") + 3
    n = int(100 * e_out(prog(t, min(t_l - 0.6, ta + 0.6), fe("familia_2"))))
    for k in range(n):
        fila, col = divmod(k, 20)
        x, y = W * 0.18 + col * 62, H * 0.30 + fila * 82
        c = (0.95, 0.78, 0.40) if k < 50 else (0.95, 0.35, 0.30)
        cv2.circle(lz, (int(x), int(y - 18)), 9, c, -1, cv2.LINE_AA)
        cv2.ellipse(lz, (int(x), int(y + 10)), (12, 20), 0, 180, 360, c, -1, cv2.LINE_AA)
    contador(lz, t, t_l - 0.6, 2.2, 0, 50, W * 0.30, H * 0.76, px=54, sufijo=" hijos", color=(0.95, 0.78, 0.4))
    contador(lz, t, t_l + 0.8, 1.6, 0, 50, W * 0.70, H * 0.76, px=54, sufijo=" hijas", color=A.ROJO_HALO)
    return camara(lz, t, ta, tb, 1.0, 1.05)


A.firma("f_kv5", "arqueólogo de flow que se arrastra con linterna (haz que barre) + plano de la kv5 que se dibuja con trazo de luz pasillo a pasillo + "
        "contador más de 100 cámaras + rótulo kv5 1995")


def f_kv5(t, ta, tb):
    lz = cine("kv5_pasillo", t, ta, tb, 1.05, 1.30, (0.5, 0.5), (0.5, 0.45))
    lz *= np.float32(0.75 + 0.1 * math.sin(t * 5.3) * math.sin(t * 1.7))
    A.rotulo_serif(lz, [("KV5 · ", A.ROJO), ("1995", A.BLANCO)], W * 0.18, H * 0.10, t, T("familia_3", "1995") if _tiene("familia_3", "1995") else ta + 0.5, px=50)
    A.etiqueta(lz, "Kent Weeks, egiptólogo", W * 0.05, H * 0.20, t, T("familia_3", "weeks") - 0.3 if _tiene("familia_3", "weeks") else ta + 2, px=28)
    t_p = T("familia_4", "pasillos") if _tiene("familia_4", "pasillos") else fs("familia_4") + 2
    u = e_inout(prog(t, t_p - 0.8, fe("familia_4") - 2))
    if u > 0:
        lz *= 1 - 0.4 * u
        x0, y0 = W * 0.62, H * 0.18
        traz = [(0, 0), (0, 160), (-180, 160), (180, 160), (0, 160), (0, 420), (-220, 420), (220, 420), (0, 420), (0, 520), (-140, 620), (140, 620)]
        segs = [(traz[i], traz[i + 1]) for i in range(len(traz) - 1)]
        m = int(len(segs) * u)
        for (a, b) in segs[:m]:
            cv2.line(lz, (int(x0 + a[0]), int(y0 + a[1])), (int(x0 + b[0]), int(y0 + b[1])), (0.95, 0.9, 0.75), 4, cv2.LINE_AA)
        for k in range(int(40 * u)):
            sx = x0 + ((k * 53) % 440) - 220
            sy = y0 + 160 + (k // 9) * 100
            cv2.rectangle(lz, (int(sx - 10), int(sy - 8)), (int(sx + 10), int(sy + 8)), (0.95, 0.9, 0.75), 1, cv2.LINE_AA)
    contador(lz, t, T("familia_4", "cien") - 0.6 if _tiene("familia_4", "cien") else t_p + 2, 1.2, 0, 100, W * 0.24, H * 0.78, px=72, sufijo="+ cámaras", color=A.ROJO_HALO)
    A.cursiva_luz(lz, "LA TUMBA DE SUS HIJOS", W * 0.30, H * 0.90, t, T("familia_4", "tumba") - 0.2 if _tiene("familia_4", "tumba") else fe("familia_4") - 3, px=36)
    return lz


A.firma("f_herederos", "doce velas en fila sobre piedra que se apagan una a una con humo (los doce herederos) + contador de herederos enterrados + "
        "cursiva el precio de su leyenda")


def f_herederos(t, ta, tb):
    lz = A.piedra(sem=85, tono=(0.09, 0.09, 0.1))
    t_d = T("familia_5", "doce")
    A.cursiva_luz(lz, "EL PRECIO DE SU LEYENDA", W * 0.5, H * 0.14, t, T("familia_5", "precio") - 0.2, px=50)
    for i in range(12):
        x = W * (0.12 + 0.07 * i)
        y = H * 0.62
        apag = t > t_d - 0.8 + 0.18 * i
        cv2.rectangle(lz, (int(x - 12), int(y)), (int(x + 12), int(y + 120)), (0.78, 0.74, 0.66), -1)
        if not apag:
            fl = 1 + 0.12 * math.sin(t * 13 + i)
            cv2.ellipse(lz, (int(x), int(y - 16)), (int(7 * fl), int(16 * fl)), 0, 0, 360, (1.0, 0.75, 0.3), -1, cv2.LINE_AA)
            g = np.zeros((H, W), np.float32)
            cv2.circle(g, (int(x), int(y - 16)), 40, 1.0, -1)
            lz += cv2.GaussianBlur(g, (0, 0), 30)[..., None] * np.float32((0.5, 0.3, 0.1)) * 0.6
        else:
            ts = t - (t_d - 0.8 + 0.18 * i)
            if ts < 1.5:
                cv2.circle(lz, (int(x + 6 * math.sin(ts * 4)), int(y - 20 - ts * 50)), int(6 + ts * 10), (0.45, 0.45, 0.45), -1, cv2.LINE_AA)
    contador(lz, t, t_d - 0.8, 2.2, 0, 12, W * 0.5, H * 0.40, px=90, sufijo=" herederos", color=A.ROJO_HALO)
    return camara(lz, t, ta, tb, 1.0, 1.06)


A.firma("f_muerte", "cara real de la momia muy cerca con luz de quirófano que la recorre + flechas finas de diagnóstico (artritis, dientes) que se trazan + "
        "contadores 66 años de reinado y 90 años + fechas 1279-1213 a. c.")


def f_muerte(t, ta, tb):
    lz = foto("momia_cara.JPG", t, ta, tb, 1.20, 1.38, (0.5, 0.40), (0.5, 0.46), oscuro=0.70)
    barrido_luz(lz, t, ta + 0.5, dur=3.0, color=(0.85, 0.9, 1.0), op=0.25, ang=1.2)
    contador(lz, t, fs("familia_6"), 1.5, 0, 66, W * 0.16, H * 0.16, px=80, sufijo=" años", color=A.ROJO_HALO)
    A.etiqueta(lz, "de reinado · 1279-1213 a. C.", W * 0.05, H * 0.26, t, fs("familia_6") + 0.8, px=26)
    t_n = T("familia_6", "noventa") if _tiene("familia_6", "noventa") else fs("familia_6") + 6
    contador(lz, t, t_n - 0.5, 1.0, 0, 90, W * 0.84, H * 0.16, px=80, sufijo=" años", color=A.BLANCO)
    for i, (pal, txt, p0, p1) in enumerate((("artritico", "artritis", (W * 0.70, H * 0.62), (W * 0.86, H * 0.74)),
                                             ("dientes", "abscesos en los dientes", (W * 0.50, H * 0.70), (W * 0.20, H * 0.82)))):
        tc = T("familia_6", pal) if _tiene("familia_6", pal) else fe("familia_6") - 2 + i
        u = e_out(prog(t, tc - 0.2, tc + 0.5))
        if u > 0:
            cv2.line(lz, (int(p0[0]), int(p0[1])), (int(lerp(p0[0], p1[0], u)), int(lerp(p0[1], p1[1], u))), (0.95, 0.95, 0.95), 2, cv2.LINE_AA)
            cv2.circle(lz, (int(p0[0]), int(p0[1])), 8, (0.95, 0.2, 0.15), -1, cv2.LINE_AA)
            A.etiqueta(lz, txt, p1[0] - (0 if p1[0] > W / 2 else 150), p1[1] + 34, t, tc + 0.3, px=26, punto=False)
    return lz


A.firma("f_merenptah", "estatua real de merenptah que sube y gira sobre pizarra con franja de luz + número 13 gigante detrás en contorno + "
        "corona que pasa de un camafeo de ramsés a él con arco de luz + texto otro faraón")


def f_merenptah(t, ta, tb):
    lz = A.piedra(sem=88) * 0.85
    A.rotulo_serif(lz, [("13", (0.30, 0.30, 0.32))], W * 0.68, H * 0.48, t, ta, px=420, vel=0.0, glow=0.0)
    png = IMGX("merenptah_rec.png")
    if png:
        A.artefacto(lz, png, W * 0.66, H * 0.54, 760, t, T("familia_7", "merenptah") - 0.4 if _tiene("familia_7", "merenptah") else ta + 1, giro=9.0)
    A.camafeo(lz, IMG + "joven_memnon.jpg", W * 0.20, H * 0.32, 120, t, ta + 0.2, foco=(0.5, 0.62), zoom=1.3)
    u = e_inout(prog(t, ta + 1.0, ta + 2.4))
    A.arco_luz(lz, (W * 0.26, H * 0.32), (W * 0.56, H * 0.22), -60, u * 1.2)
    A.rotulo_serif(lz, [("MERENPTAH · ", A.BLANCO), ("HIJO N.º 13", A.ROJO)], W * 0.30, H * 0.70, t, T("familia_7", "hijo") - 0.2 if _tiene("familia_7", "hijo") else ta + 2, px=40)
    A.texto_mixto(lz, [("La mayoría no había conocido", A.GRIS), ("otro faraón", A.BLANCO)], W * 0.06, H * 0.86, t, T("familia_7", "mayoria") - 0.2, px=34)
    return camara(lz, t, ta, tb, 1.0, 1.05)


# ------------------------------------------------------------------ cap. 6: EL ESCONDITE
A.firma("e_viaje", "sacerdotes de flow con antorchas que llevan las momias por el acantilado + antorchas que laten + ruta punteada valle de los reyes → "
        "deir el-bahari sobre el acantilado + rótulo otro viaje + brasas")


def e_viaje(t, ta, tb):
    lz = cine("sacerdotes_momias", t, ta, tb, 1.06, 1.24, (0.45, 0.5), (0.60, 0.5))
    lz *= np.float32(0.82 + 0.1 * math.sin(t * 6.7) * math.sin(t * 2.3))
    particulas(lz, t, sem=90, n=80, v=(10, -100), tam=(1, 2.4), color=(1.0, 0.6, 0.2), op=0.7, parpadeo=0.6)
    A.cursiva_luz(lz, "OTRO VIAJE", W * 0.5, H * 0.12, t, T("escondite_0", "viaje") - 0.3, px=56, salida=fs("escondite_1") + 1)
    t_l = T("escondite_1", "ladrones")
    A.estampa(lz, "SAQUEADA", W * 0.78, H * 0.20, t, t_l + 0.3, px=46) if hasattr(A, "estampa") else D.estampa(lz, "SAQUEADA", W * 0.78, H * 0.20, t, t_l + 0.3, px=46)
    t_d = T("escondite_1", "deir") if _tiene("escondite_1", "deir") else fe("escondite_1") - 2
    u = e_inout(prog(t, t_d - 1.5, t_d + 0.5))
    D.linea_punteada(lz, [(W * 0.10, H * 0.78), (W * 0.30, H * 0.70), (W * 0.50, H * 0.74), (W * 0.70, H * 0.66)], u, grosor=4, color=(1.0, 0.86, 0.6))
    A.etiqueta(lz, "Valle de los Reyes", W * 0.04, H * 0.86, t, t_d - 1.5, px=26)
    A.etiqueta(lz, "Deir el-Bahari", W * 0.66, H * 0.60, t, t_d, px=28)
    return lz


A.firma("e_1881", "ataúdes que salen del pozo (flow) con cuerdas + tono sepia de foto de época con rayas de película + contador casi 3 000 años + "
        "sello 1881 que cae + pieza por pieza: siluetas de objetos que se van")


def e_1881(t, ta, tb):
    lz = cine("ataudes_1881", t, ta, tb, 1.05, 1.20, (0.5, 0.45), (0.5, 0.55))
    g = lz.mean(-1, keepdims=True)
    sep = smooth(prog(t, T("escondite_2", "familia") if _tiene("escondite_2", "familia") else ta + 3, fe("escondite_2") - 3))
    lz[:] = lz * (1 - sep) + g * np.float32((1.05, 0.9, 0.7)) * sep
    rng = np.random.default_rng(int(t * 24))
    for _ in range(3):
        x = int(rng.random() * W)
        cv2.line(lz, (x, 0), (x, H), (0.8, 0.75, 0.65), 1)
    contador(lz, t, fs("escondite_2"), 1.6, 0, 3000, W * 0.5, H * 0.14, px=74, sufijo=" años dormido", color=A.BLANCO, salida=fs("escondite_2") + 4)
    A.texto_mixto(lz, [("Pieza", A.BLANCO), ("por pieza", A.GRIS)], W * 0.06, H * 0.86, t, T("escondite_2", "pieza") - 0.2 if _tiene("escondite_2", "pieza") else ta + 6, px=40)
    D.estampa(lz, "1881", W * 0.78, H * 0.22, t, T("escondite_2", "1881") - 0.2 if _tiene("escondite_2", "1881") else fe("escondite_2") - 3, px=70)
    return lz


# ------------------------------------------------------------------ cap. 7: OZYMANDIAS
A.firma("o_belzoni", "cientos de hombres de flow arrastrando el busto con calima que ondula + polvo lateral + ruta punteada tebas → londres sobre un mini mapa + "
        "contador 1816 + rótulo rumbo a londres")


def o_belzoni(t, ta, tb):
    lz = cine("belzoni_arrastre", t, ta, tb, 1.18, 1.18, (0.40, 0.5), (0.58, 0.48))
    off = (np.sin(np.arange(H, dtype=np.float32)[:, None] * 0.05 + t * 6) * 2).astype(np.float32)
    lz[:] = cv2.remap(lz, (np.arange(W, dtype=np.float32)[None, :] + off), np.repeat(np.arange(H, dtype=np.float32)[:, None], W, 1), cv2.INTER_LINEAR)
    particulas(lz, t, sem=95, n=150, v=(160, -10), tam=(1, 2), color=(0.95, 0.82, 0.6), op=0.35, estela=0.03)
    contador(lz, t, ta + 0.4, 1.0, 1700, 1816, W * 0.14, H * 0.12, px=74, color=A.BLANCO)
    A.etiqueta(lz, "Giovanni Belzoni", W * 0.05, H * 0.22, t, T("ozymandias_0", "belzoni") - 0.2 if _tiene("ozymandias_0", "belzoni") else ta + 3, px=28)
    A.rotulo_serif(lz, [("TEBAS → ", A.BLANCO), ("LONDRES", A.ROJO)], W * 0.70, H * 0.88, t, T("ozymandias_0", "londres") - 0.4 if _tiene("ozymandias_0", "londres") else fe("ozymandias_0") - 1, px=46)
    return lz


A.firma("o_shelley", "poeta de flow escribiendo a la luz de vela con llama que tiembla + lluvia en la ventana + letras del título ozymandias que se escriben en "
        "cursiva luminosa + ecuación ozymandias = ramsés con camafeo")


def o_shelley(t, ta, tb):
    lz = cine("poeta", t, ta, tb, 1.05, 1.22, (0.45, 0.55), (0.40, 0.5))
    lz *= np.float32(0.82 + 0.10 * math.sin(t * 9.3) * math.sin(t * 3.1))
    particulas(lz, t, sem=96, n=90, v=(-20, 380), tam=(1, 1.5), color=(0.7, 0.8, 0.9), op=0.35, estela=0.05, zona=(int(W * 0.55), 0, W, int(H * 0.55)))
    A.texto_mixto(lz, [("Percy Shelley,", A.BLANCO), ("1818", A.GRIS)], W * 0.06, H * 0.10, t, T("ozymandias_1", "shelley") - 0.2 if _tiene("ozymandias_1", "shelley") else ta + 2, px=36)
    t_o = T("ozymandias_1", "ozymandias") if _tiene("ozymandias_1", "ozymandias") else (T("ozymandias_1", "osimandias") if _tiene("ozymandias_1", "osimandias") else fs("ozymandias_1") + 7)
    A.cursiva_luz(lz, "OZYMANDIAS", W * 0.5, H * 0.46, t, t_o - 0.2, px=96)
    t_g = T("ozymandias_1", "griegos") if _tiene("ozymandias_1", "griegos") else t_o + 1.5
    A.rotulo_serif(lz, [("= ", A.GRIS), ("RAMSÉS", A.ROJO)], W * 0.5, H * 0.60, t, t_g, px=56)
    return lz


A.firma("o_poema", "piernas de piedra en el desierto de flow + arena que barre en ráfagas cada vez más fuerte + cita amarilla de los versos del soneto + "
        "neón nada que se apaga + la arena cubre todo al final")


def o_poema(t, ta, tb):
    lz = cine("ozymandias_desierto", t, ta, tb, 1.04, 1.22, (0.5, 0.5), (0.5, 0.42))
    fuerza = 0.3 + 0.7 * smooth(prog(t, fs("ozymandias_4"), fe("ozymandias_4")))
    particulas(lz, t, sem=97, n=int(160 + 300 * fuerza), v=(-500 * fuerza - 200, 25), tam=(1, 2.2), color=(0.95, 0.8, 0.6), op=0.4, estela=0.06)
    humo(lz, t, sem=98, v=(-220, 0), color=(0.85, 0.72, 0.55), op=0.20 + 0.25 * fuerza, zona_y=(0.5, 1.0))
    A.cita(lz, ["«Mi nombre es Ozymandias, rey de reyes:", "¡mirad mis obras, poderosos, y desesperad!»"], W * 0.5, H * 0.24, t, fs("ozymandias_3") - 0.2,
           px=42, fuente_txt="Percy B. Shelley, «Ozymandias» (1818)", vel=2.5, salida=fs("ozymandias_4") - 0.2)
    A.neon(lz, "NADA", W * 0.5, H * 0.30, t, T("ozymandias_4", "nada") - 0.1, px=110, barras=False)
    cubre = smooth(prog(t, T("ozymandias_4", "arena") - 0.3, tb))
    lz[:] = lz * (1 - 0.8 * cubre) + np.float32((0.55, 0.42, 0.28)) * 0.8 * cubre
    return lz


A.firma("o_presa", "presa real de asuán con paneo + agua azul que sube desde abajo de la pantalla (líquido del kit en azul) hacia abu simbel en camafeo + "
        "contador de nivel + rótulo para siempre")


def o_presa(t, ta, tb):
    n = "presa_asuan.jpg" if IMGX("presa_asuan.jpg") else "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg"
    lz = foto(n, t, ta, tb, 1.05, 1.18, (0.5, 0.5), (0.45, 0.5), oscuro=0.70)
    A.camafeo(lz, IMG + "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", W * 0.74, H * 0.40, 170, t, T("ozymandias_5", "abu") - 0.2 if _tiene("ozymandias_5", "abu") else ta + 3, foco=(0.5, 0.45), zoom=1.3)
    t_i = T("ozymandias_5", "inundar") if _tiene("ozymandias_5", "inundar") else ta + 3
    u = smooth(prog(t, t_i - 0.5, tb))
    A.liquido(lz, 0, H * (1 - 0.55 * u), W, H, 1.0, t, color=(0.10, 0.28, 0.45), sem=9, op=0.75)
    A.rotulo_serif(lz, [("PRESA DE ", A.BLANCO), ("ASUÁN", A.ROJO)], W * 0.30, H * 0.10, t, T("ozymandias_5", "presa") - 0.2 if _tiene("ozymandias_5", "presa") else ta + 1, px=48)
    A.cursiva_luz(lz, "PARA SIEMPRE", W * 0.74, H * 0.66, t, T("ozymandias_5", "siempre") - 0.3 if _tiene("ozymandias_5", "siempre") else fe("ozymandias_5") - 1, px=40)
    return lz


A.firma("o_traslado", "corte de la unesco de flow con grúa que sube la cara + rejilla de bloques numerados que se superpone y se separa + contador 1 000 bloques + "
        "flecha que sube 65 m con regla + años 1964-1968")


def o_traslado(t, ta, tb):
    lz = cine("unesco_corte", t, ta, tb, 1.05, 1.18, (0.5, 0.5), (0.55, 0.42))
    t_c = T("ozymandias_6", "corto") if _tiene("ozymandias_6", "corto") else fs("ozymandias_6") + 1
    u = smooth(prog(t, t_c - 0.2, t_c + 1.5))
    if u > 0:
        paso = 96
        sep = 6 * smooth(prog(t, t_c + 1.0, t_c + 3.0))
        for x in range(0, W, paso):
            cv2.line(lz, (x, 0), (x, H), (0.9 * u, 0.85 * u, 0.7 * u), 1 + int(sep > 2))
        for y in range(0, H, paso):
            cv2.line(lz, (0, y), (W, y), (0.9 * u, 0.85 * u, 0.7 * u), 1 + int(sep > 2))
    contador(lz, t, t_c, 1.5, 0, 1000, W * 0.22, H * 0.12, px=70, sufijo="+ bloques", color=A.ROJO_HALO)
    t_s = T("ozymandias_6", "sesenta") if _tiene("ozymandias_6", "sesenta") else fe("ozymandias_6") - 3
    v = e_inout(prog(t, t_s - 0.5, t_s + 1.0))
    if v > 0:
        x, yb = W * 0.90, H * 0.85
        cv2.arrowedLine(lz, (int(x), int(yb)), (int(x), int(yb - v * H * 0.6)), (0.95, 0.9, 0.8), 6, cv2.LINE_AA, tipLength=0.08)
        contador(lz, t, t_s - 0.5, 1.5, 0, 65, x - 100, yb - v * H * 0.6 - 30, px=56, sufijo=" m", color=A.BLANCO)
    A.etiqueta(lz, "UNESCO · 1964-1968", W * 0.05, H * 0.90, t, T("ozymandias_6", "1964") - 0.2 if _tiene("ozymandias_6", "1964") else ta + 4, px=30)
    return lz


A.firma("o_paris", "laboratorio de parís de flow con luz fría que parpadea + esporas del hongo (puntos verdes) que flotan y se apagan con el destello de la radiación + "
        "símbolo de radiación que gira + rótulo rayos gamma + vuelta a casa")


def o_paris(t, ta, tb):
    lz = cine("paris_lab", t, ta, tb, 1.04, 1.22, (0.5, 0.55), (0.5, 0.48))
    t_h = T("ozymandias_7", "hongo") if _tiene("ozymandias_7", "hongo") else fs("ozymandias_7") + 3
    t_r = T("ozymandias_7", "radiacion") if _tiene("ozymandias_7", "radiacion") else fe("ozymandias_7") - 3
    esporas = smooth(prog(t, t_h - 0.4, t_h + 0.6)) * (1 - smooth(prog(t, t_r, t_r + 0.8)))
    particulas(lz, t, sem=99, n=120, v=(6, -8), tam=(1.5, 3.5), color=(0.5, 0.95, 0.4), op=0.7 * esporas, parpadeo=0.5)
    fl = math.exp(-max(0.0, t - t_r) * 2.0) if t > t_r else 0.0
    lz += np.float32((0.6, 0.8, 1.0)) * 0.6 * fl
    if t > t_r - 0.3:
        c = (int(W * 0.84), int(H * 0.22))
        for k in range(3):
            a0 = math.degrees((t - t_r) * 1.5) + k * 120
            cv2.ellipse(lz, c, (70, 70), 0, a0, a0 + 60, (1.0, 0.85, 0.2), -1, cv2.LINE_AA)
        cv2.circle(lz, c, 16, (1.0, 0.85, 0.2), -1, cv2.LINE_AA)
    A.rotulo_serif(lz, [("PARÍS · ", A.BLANCO), ("1976", A.ROJO)], W * 0.20, H * 0.10, t, T("ozymandias_7", "paris") - 0.2 if _tiene("ozymandias_7", "paris") else ta + 3, px=48)
    A.cursiva_luz(lz, "RAYOS GAMMA", W * 0.70, H * 0.86, t, t_r, px=44)
    return lz


# ------------------------------------------------------------------ cap. 8: CIERRE
A.firma("z_desfile", "desfile dorado de flow de noche con fuegos que destellan + carrozas que avanzan (paneo) + contador 22 reyes y reinas + "
        "rótulo el cairo 2021 + confeti de luz")


def z_desfile(t, ta, tb):
    lz = cine("desfile", t, ta, tb, 1.15, 1.15, (0.40, 0.5), (0.60, 0.5))
    for k in range(4):
        tk = ta + 0.8 + k * 1.9
        if t > tk:
            r = (t - tk) * 260
            g = np.zeros((H, W), np.float32)
            cv2.circle(g, (int(W * (0.2 + 0.2 * k)), int(H * 0.18)), int(r), 1.0, 3, cv2.LINE_AA)
            lz += cv2.GaussianBlur(g, (0, 0), 4)[..., None] * np.float32((1.0, 0.8, 0.4)) * max(0.0, 1 - (t - tk) / 1.2)
    particulas(lz, t, sem=100, n=120, v=(0, 60), tam=(1, 2.5), color=(1.0, 0.85, 0.4), op=0.5, parpadeo=0.6)
    A.rotulo_serif(lz, [("EL CAIRO · ", A.BLANCO), ("2021", A.ROJO)], W * 0.5, H * 0.10, t, ta + 0.5, px=50)
    contador(lz, t, T("cierre_0", "veintiun") - 0.4 if _tiene("cierre_0", "veintiun") else ta + 4, 1.2, 0, 22, W * 0.5, H * 0.86, px=64,
             sufijo=" reyes y reinas", color=A.BLANCO)
    return lz


A.firma("z_balance", "tres recuerdos del video que vuelven como láminas pequeñas que se apilan (cartucho tachado, relieve de kadesh, colosos) + "
        "tres verbos borró, talló, convirtió que se encienden uno por uno + negro con rejilla")


def z_balance(t, ta, tb):
    lz = negro()
    A.rejilla(lz, t, horizonte=0.70, op=0.22, vel=0.3)
    A.cursiva_luz(lz, "QUERÍA QUE NADIE LO OLVIDARA", W * 0.5, H * 0.12, t, fs("cierre_1") - 0.1, px=46)
    recs = [("borro", "BORRÓ", "estatua_usurpada.jpg", "cartucho_ramses.jpg"), ("tallo", "TALLÓ", "kadesh_rameseo.jpg", None),
            ("convirtio", "CONVIRTIÓ", "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", None)]
    for i, (pal, txt, n1, n2) in enumerate(recs):
        tc = T("cierre_1", pal) if _tiene("cierre_1", pal) else fs("cierre_1") + 2 + 2 * i
        n = n1 if IMGX(n1) else (n2 if n2 and IMGX(n2) else "kadesh_rameseo.jpg")
        x = W * (0.2 + 0.3 * i)
        A.camafeo(lz, IMG + n, x, H * 0.48, 150, t, tc - 0.2, foco=(0.5, 0.45), zoom=1.2)
        A.rotulo_serif(lz, [(txt, A.ROJO)], x, H * 0.74, t, tc - 0.1, px=46)
    return camara(lz, t, ta, tb, 1.0, 1.06)


A.firma("z_pasaporte", "vuelve el pasaporte del principio con la profesión rey y el sello rojo fallecido que cae + cara real de la momia en la foto + "
        "rótulo 3 000 años después + polvo")


def z_pasaporte(t, ta, tb):
    lz = negro()
    A.polvo(lz, t, n=80, sem=101, op=0.4)
    tj = _tarjeta()
    u = e_out(prog(t, ta, ta + 1.0))
    M = D.poner(tj.w, tj.h, W * 0.56 + (1 - u) * 500, H * 0.56, 0.95, rz=4 - 3 * math.sin(t * 0.35), ry=24 - 30 * prog(t, ta, tb), rx=-8)
    D.pegar(lz, tj, M, 0.42 * u)                                        # vuelve la ficha del principio, ahora entrando de lado
    A.rotulo_serif(lz, [("3 000 AÑOS ", A.BLANCO), ("DESPUÉS", A.ROJO)], W * 0.5, H * 0.10, t, T("cierre_2", "tres") - 0.2 if _tiene("cierre_2", "tres") else ta, px=46)
    A.texto_mixto(lz, [("Profesión:", A.GRIS), ("rey", A.BLANCO)], W * 0.5, H * 0.46, t, T("cierre_2", "profesion") - 0.3 if _tiene("cierre_2", "profesion") else ta + 4,
                  px=64, alinear="centro")
    D.estampa(lz, "FALLECIDO", W * 0.5, H * 0.66, t, T("cierre_2", "fallecido") - 0.1 if _tiene("cierre_2", "fallecido") else fe("cierre_2") - 0.6, px=90)
    A.camafeo(lz, IMG + "momia_cara.JPG", W * 0.18, H * 0.56, 150, t, ta + 0.6, foco=(0.5, 0.45), zoom=1.3)
    return camara(lz, t, ta, tb, 1.0, 1.05)


A.firma("z_final", "rótulo bitácora perdida en versales con línea roja que se traza + pregunta ¿a quién seguimos? en cursiva + siluetas de colosos al fondo "
        "que se funden a negro + polvo")


def z_final(t, ta, tb):
    lz = foto("Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", t, ta, tb, 1.10, 1.0, (0.5, 0.4), (0.5, 0.45), oscuro=0.22)
    A.polvo(lz, t, n=70, sem=102, op=0.4)
    A.rotulo_serif(lz, [("BITÁCORA ", A.BLANCO), ("PERDIDA", A.ROJO)], W * 0.5, H * 0.40, t, ta + 0.3, px=84)
    u = e_inout(prog(t, ta + 1.0, ta + 2.2))
    cv2.line(lz, (int(W * 0.5 - 380 * u), int(H * 0.50)), (int(W * 0.5 + 380 * u), int(H * 0.50)), (0.9, 0.12, 0.1), 3, cv2.LINE_AA)
    A.cursiva_luz(lz, "¿A QUIÉN SEGUIMOS?", W * 0.5, H * 0.62, t, T("cierre_3", "quien") - 0.3 if _tiene("cierre_3", "quien") else ta + 4, px=50)
    return lz


# ------------------------------------------------------------------ lista de tomas: (inicio, función, (entrada, dur))
def _tomas():
    return [
        (0.0, g_avion, ("negro", 0.0)),
        (T("gancho_1", "en") - 0.3, g_guardia, ("arena", 0.7)),
        (T("gancho_2", "y") - 0.25, g_pasaporte, ("arena", 0.6)),
        (T("gancho_3", "nadie") - 0.3, g_archivo, ("desenfoque", 0.8)),
        (T("gancho_4", "quien") - 0.3, g_momia, ("arena", 0.6)),
        (T("gancho_5", "se") - 0.3, g_ramses, ("destello", 0.7)),
        (TL["escenas"][1]["t0"], n_general, ("tunel", 1.1)),
        (T("nieto_1", "su") - 0.4, n_herencia, ("latigo", 0.6)),
        (T("nieto_3", "ramses") - 0.4, n_seti, ("tunel", 0.9)),
        (T("nieto_4", "por") - 0.3, n_corregente, ("latigo", 0.6)),
        (T("nieto_5", "el") - 0.3, n_campanas, ("tunel", 0.9)),
        (T("nieto_6", "un") - 0.3, n_fabrica, ("latigo", 0.6)),
        (T("nieto_7", "en") - 0.3, n_coronacion, ("tunel", 1.0)),
    ] + [(fs(k) - 0.3, fn, ("tunel", 1.0)) for k, fn, _c in _T4]


# tramo 4 (120-576 s): (frase donde empieza, lámina, capítulo); t0 = inicio de la frase − 0,3
_T4 = [("kadesh_0", k_mapa, "kadesh"), ("kadesh_2", k_divisiones, "kadesh"), ("kadesh_3", k_espias, "kadesh"), ("kadesh_4", k_mentira, "kadesh"),
       ("kadesh_5", k_carga, "kadesh"), ("kadesh_6", k_cinco_mil, "kadesh"), ("kadesh_7", k_solo, "kadesh"), ("kadesh_8", k_empate, "kadesh"),
       ("kadesh_9", k_historia, "kadesh"), ("kadesh_11", k_propaganda, "kadesh"),
       ("tratado_0", t_frontera, "tratado"), ("tratado_2", t_pacto, "tratado"), ("tratado_3", t_doble, "tratado"), ("tratado_5", t_onu, "tratado"),
       ("tratado_6", t_boda, "tratado"),
       ("constructor_0", c_nombre, "constructor"), ("constructor_1", c_piramses, "constructor"), ("constructor_2", c_rameseo, "constructor"),
       ("constructor_3", c_abusimbel, "constructor"), ("constructor_5", c_sol, "constructor"), ("constructor_6", c_borrar, "constructor"),
       ("familia_0", f_nefertari, "familia"), ("familia_1", f_esposas, "familia"), ("familia_2", f_hijos, "familia"), ("familia_3", f_kv5, "familia"),
       ("familia_5", f_herederos, "familia"), ("familia_6", f_muerte, "familia"), ("familia_7", f_merenptah, "familia"),
       ("escondite_0", e_viaje, "escondite"), ("escondite_2", e_1881, "escondite"),
       ("ozymandias_0", o_belzoni, "ozymandias"), ("ozymandias_1", o_shelley, "ozymandias"), ("ozymandias_2", o_poema, "ozymandias"),
       ("ozymandias_5", o_presa, "ozymandias"), ("ozymandias_6", o_traslado, "ozymandias"), ("ozymandias_7", o_paris, "ozymandias"),
       ("cierre_0", z_desfile, "cierre"), ("cierre_1", z_balance, "cierre"), ("cierre_2", z_pasaporte, "cierre"), ("cierre_3", z_final, "cierre")]


TOMAS = _tomas()


def _cuadro(i, t):
    t0, fn, _ = TOMAS[i]
    if fn is None:
        return negro()
    tb = TOMAS[i + 1][0] if i + 1 < len(TOMAS) else TOTAL
    return np.clip(fn(t, t0, tb), 0, 1.5)


# ------------------------------------------------------------------ TÚNEL DE CAPAS (avance v4, el usuario 4-nov-2026)
import tunel as TU

A.firma("tunel_gancho", "túnel del gancho: láminas que se alejan hacia el fondo alternando derecha, izquierda y arriba; en cada frase entran "
        "pegatinas reales, fotos, camafeos y rótulos delante de la lámina; la cámara los atraviesa")
A.firma("tunel_nieto", "túnel del cap. 1: el camino baja y sube como una escalera de láminas con un giro largo a la izquierda hacia el mapa; "
        "capas de la familia (abuelo, horemheb, seti) quedan colgadas a los lados mientras la cámara pasa")

# posición (x, y, z) de cada lámina: casi siempre al fondo (z), a veces a un lado, arriba o abajo
_POS = [(0.0, 0.0, 0.0), (1.15, 0.0, 1.3), (1.15, -0.0, 2.9), (0.0, -0.75, 4.1), (0.0, -0.75, 5.7), (-1.2, -0.75, 7.0),
        (-1.2, 0.0, 8.8), (-1.2, 0.80, 10.1), (0.0, 0.80, 11.5), (0.0, 1.55, 12.8), (-1.3, 1.55, 14.2), (-1.3, 1.55, 15.9),
        (-1.3, 0.80, 17.3)]

# tramo 4: un RECORRIDO distinto por capítulo (el usuario: «casi siempre hacia el fondo, a veces a un lado, arriba o abajo»; nada repetido)
A.firma("tunel_kadesh", "túnel de kadesh: zigzag que avanza hacia la derecha y va bajando, como una carga de carros que se desvía")
A.firma("tunel_tratado", "túnel del tratado: recto y hondo, saltos largos al fondo sin desvíos (la calma de la paz)")
A.firma("tunel_constructor", "túnel del constructor: escalera que sube lámina a lámina con un vaivén corto a los lados, como subir un pilono")
A.firma("tunel_familia", "túnel de la familia: el camino se va a la izquierda con un balanceo arriba-abajo, como pasar por un árbol genealógico")
A.firma("tunel_escondite", "túnel del escondite: caída hacia abajo, como bajar al pozo de las momias")
A.firma("tunel_ozymandias", "túnel de ozymandias: espiral que gira un cuarto de vuelta por lámina mientras avanza, como arena en remolino")
A.firma("tunel_cierre", "túnel del cierre: recto, cada vez más hondo y lento, hasta el fundido a negro")


def _pasos(cap, i):
    """Desplazamiento (dx, dy, dz) desde la lámina anterior para la i-ésima lámina del capítulo `cap`."""
    if cap == "kadesh":
        return ((1.25, 0.45, 1.4) if i % 2 == 0 else (-0.55, 0.40, 1.3))
    if cap == "tratado":
        return (0.0, 0.0, 2.3)
    if cap == "constructor":
        return ((0.35 if i % 2 else -0.35), -0.75, 1.3)
    if cap == "familia":
        return (-1.25, (0.30 if i % 2 else -0.30), 1.3)
    if cap == "escondite":
        return (0.0, 1.0, 1.4)
    if cap == "ozymandias":
        a0, a1 = math.pi / 2 * i, math.pi / 2 * (i + 1)
        return (1.1 * (math.cos(a1) - math.cos(a0)), 1.1 * (math.sin(a1) - math.sin(a0)), 1.4)
    return (0.0, 0.0, 1.6 + 0.3 * i)                                      # cierre


def _pos_t4():
    x, y, z = _POS[-1]
    out, cap0, i = [], None, 0
    for _k, _fn, cap in _T4:
        i = 0 if cap != cap0 else i + 1
        dx, dy, dz = _pasos(cap, i)
        if cap != cap0:
            dz += 0.6                                                     # al cambiar de capítulo, un salto más hondo
        cap0 = cap
        x, y, z = x + dx, y + dy, z + dz
        out.append((round(x, 3), round(y, 3), round(z, 3)))
    return out


_POS = _POS + _pos_t4()


def _cap(key, palabra, li, pos, alto, spr, anim="sube", n=0):
    return (T(key, palabra, n) - 0.1, li, pos, alto, spr, anim)


def _capas():
    P, F, C, X = TU.spr_png, TU.spr_foto, TU.spr_camafeo, TU.spr_texto
    i = IMG
    return [
        _cap("gancho_0", "avion", 0, (-0.48, -0.40, 0.4), 0.38, P(i + "avion_rec.png"), "der"),
        _cap("gancho_0", "muerto", 0, (0.40, 0.40, 0.3), 0.11, X((("CARGA: ", "b"), ("UNA MOMIA", "r"))), "sube"),
        _cap("gancho_1", "guardia", 1, (-0.48, 0.40, 0.35), 0.62, P(i + "guardia_siluetas_rec.png"), "izq"),
        _cap("gancho_1", "jefe", 1, (0.40, -0.40, 0.45), 0.11, X((("EJÉRCITO ", "b"), ("FRANCÉS", "r"))), "gira"),
        _cap("gancho_2", "pasaporte", 2, (-0.40, -0.40, 0.30), 0.11, X((("EGIPTO → ", "b"), ("FRANCIA", "r"))), "izq"),
        _cap("gancho_2", "rey", 2, (0.48, 0.40, 0.42), 0.48, C(i + "momia_frontal.JPG", (0.5, 0.30), 1.6), "gira"),
        _cap("gancho_3", "documento", 3, (-0.50, 0.0, 0.38), 0.38, F(i + "momia_cara.JPG", 760, (0.5, 0.45)), "der"),
        _cap("gancho_3", "historia", 3, (-0.40, 0.40, 0.30), 0.11, X((("¿", "b"), ("LEYENDA?", "r"))), "sube"),
        _cap("gancho_4", "hombre", 4, (0.48, -0.40, 0.40), 0.48, C(i + "joven_memnon.jpg", (0.5, 0.62), 1.15), "gira"),
        _cap("gancho_4", "pais", 4, (-0.48, 0.40, 0.33), 0.36, F(i + "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg"), "izq"),
        _cap("gancho_5", "llamaba", 5, (0.40, 0.40, 0.36), 0.11, X((("RA-MESSU: ", "b"), ("«RA LO ENGENDRÓ»", "r"))), "sube"),
        _cap("gancho_5", "escribio", 5, (-0.48, -0.40, 0.42), 0.36, F(i + "kadesh_rameseo.jpg"), "der"),
        _cap("nieto_0", "familia", 6, (0.48, 0.40, 0.36), 0.66, P(i + "general_rec.png"), "der"),
        _cap("nieto_0", "real", 6, (-0.48, -0.40, 0.42), 0.36, F(i + "ramses1_relieve.jpg"), "gira"),
        _cap("nieto_2", "hijos", 7, (0.40, 0.40, 0.28), 0.11, X((("SIN ", "b"), ("HEREDERO", "r"))), "sube"),
        _cap("nieto_2", "trono", 7, (-0.08, 0.45, 0.30), 0.42, P(i + "ramses1_tumba_rec.png"), "sube"),
        _cap("nieto_3", "problema", 8, (0.40, -0.40, 0.32), 0.11, X((("FAMILIA ", "b"), ("NUEVA", "r"))), "izq"),
        _cap("nieto_3", "eterna", 8, (0.48, 0.40, 0.40), 0.38, F(i + "rameseo_coloso.jpg"), "der"),
        _cap("nieto_4", "hijo", 9, (0.50, 0.42, 0.38), 0.48, F(i + "cine_seti_hijo_b.jpg", 760, (0.5, 0.4)), "gira"),
        _cap("nieto_4", "corregente", 9, (-0.55, 0.45, 0.42), 0.58, P(i + "luxor_ramses_rec.png"), "sube"),
        _cap("nieto_5", "campanas", 10, (-0.40, -0.40, 0.30), 0.11, X((("CAMPAÑAS ", "b"), ("MILITARES", "r"))), "izq"),
        _cap("nieto_5", "obras", 10, (0.48, 0.40, 0.40), 0.36, F(i + "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", 760, (0.5, 0.6)), "der"),
        _cap("nieto_6", "fabrica", 11, (-0.48, 0.40, 0.36), 0.36, F(i + "joven_memnon.jpg", 760, (0.5, 0.3)), "izq"),
        _cap("nieto_7", "1279", 12, (0.48, -0.40, 0.34), 0.48, C(i + "luxor_ramses.jpg", (0.5, 0.62), 1.15), "gira"),
        _cap("nieto_7", "trono", 12, (-0.48, 0.40, 0.42), 0.36, F(i + "nefertari_qv66.jpg"), "der"),
    ] + _capas_t4()


def _li(t):
    """Lámina que se narra en el instante t."""
    return max(k for k, d in enumerate(TOMAS) if d[0] <= t)


# huecos de las capas del tramo 4: (dx, dy, zr, anim), se recorren en orden para que ninguna se repita seguida
_HUECOS = [(-0.50, -0.38, 0.40, "der"), (0.42, 0.40, 0.30, "sube"), (0.50, -0.36, 0.44, "gira"), (-0.42, 0.42, 0.32, "izq"),
           (0.46, 0.38, 0.36, "der"), (-0.40, -0.40, 0.28, "sube"), (-0.52, 0.36, 0.42, "gira"), (0.40, -0.42, 0.34, "izq")]


def _capas_t4():
    """2 capas por frase (120-576 s) con el material real de Commons y recortes: lo que la voz nombra entra en ese momento."""
    P, F, C, X = TU.spr_png, TU.spr_foto, TU.spr_camafeo, TU.spr_texto
    i = IMG
    b, r = "b", "r"
    L = [  # (frase, palabra, sprite, alto)
        ("kadesh_0", "prueba", X((("LA ", b), ("PRUEBA", r))), 0.11),
        ("kadesh_0", "siria", C(i + "abusimbel_kadesh.jpg", (0.45, 0.45), 1.6), 0.44),
        ("kadesh_1", "poder", X((("EL OTRO ", b), ("GRAN PODER", r))), 0.11, (-0.30, 0.62, 0.30, "sube")),
        ("kadesh_1", "muwatalli", C(i + "muwatalli_relieve.jpg", (0.5, 0.4), 1.3), 0.44),
        ("kadesh_2", "marchaba", P(i + "carro_tut_rec.png"), 0.42),
        ("kadesh_2", "dios", P(i + "khopesh_rec.png"), 0.15),
        ("kadesh_3", "atraparon", X((("DOS ", b), ("NÓMADAS SHASU", r))), 0.11),
        ("kadesh_3", "shasu", F(i + "espias_shasu.png", 760, (0.5, 0.5)), 0.30),
        ("kadesh_4", "esperaba", X((("UNA ", b), ("EMBOSCADA", r))), 0.11),
        ("kadesh_4", "escondido", F(i + "carro_hitita.jpg", 760, (0.5, 0.5)), 0.34),
        ("kadesh_5", "carros", F(i + "kadesh_rameseo.jpg", 760, (0.75, 0.5)), 0.34),
        ("kadesh_6", "calcula", X((("«SE ", b), ("CALCULA»", r))), 0.10, (0.0, 0.84, 0.30, "sube")),
        ("kadesh_6", "bandos", C(i + "abusimbel_kadesh.jpg", (0.72, 0.40), 2.4), 0.42),
        ("kadesh_7", "enemigo", C(i + "kadesh_rameseo.jpg", (0.30, 0.50), 2.2), 0.42),
        ("kadesh_8", "hititas", F(i + "muwatalli_relieve.jpg", 760, (0.5, 0.6)), 0.34),
        ("kadesh_9", "regreso", P(i + "luxor_ramses_rec.png"), 0.56),
        ("kadesh_10", "muros", F(i + "kadesh_rameseo.jpg", 760, (0.45, 0.3)), 0.34),
        ("kadesh_10", "aplastando", C(i + "abusimbel_kadesh.jpg", (0.45, 0.58), 2.6), 0.42),
        ("kadesh_11", "historiadores", X((("SEGÚN MUCHOS ", b), ("HISTORIADORES", r))), 0.10),
        ("kadesh_11", "primeras", P(i + "joven_memnon_rec.png"), 0.50),
        ("tratado_0", "raro", X((("TODAVÍA MÁS ", b), ("RARO", r))), 0.11, (-0.35, 0.62, 0.30, "izq")),
        ("tratado_0", "vino", P(i + "tratado_tablilla_rec.png"), 0.36, (0.50, 0.30, 0.34, "sube")),
        ("tratado_1", "choques", P(i + "khopesh_rec.png"), 0.14),
        ("tratado_1", "imperios", X((("EGIPTO + ", b), ("HATTI", r))), 0.11),
        ("tratado_2", "hattusili", C(i + "hattusili_relieve.jpg", (0.5, 0.4), 1.4), 0.44),
        ("tratado_2", "enemigo", F(i + "carro_hitita.jpg", 760, (0.35, 0.55)), 0.30),
        ("tratado_3", "jeroglificos", C(i + "tratado_karnak.jpg", (0.35, 0.45), 2.0), 0.42),
        ("tratado_4", "arcilla", F(i + "tratado_estambul.jpg", 760, (0.5, 0.5)), 0.34),
        ("tratado_5", "cobre", P(i + "tratado_tablilla_rec.png"), 0.36),
        ("tratado_6", "pacto", X((("UNA BODA ", b), ("DIPLOMÁTICA", r))), 0.11),
        ("tratado_6", "princesa", C(i + "hattusili_relieve.jpg", (0.5, 0.3), 2.2), 0.42),
        ("constructor_0", "calma", X((("FRONTERA EN ", b), ("CALMA", r))), 0.11),
        ("constructor_0", "nombre", F(i + "luxor_ramses.jpg", 760, (0.5, 0.3)), 0.34),
        ("constructor_1", "capital", F(i + "qantir_pi_ramses.JPG", 760, (0.5, 0.5)), 0.34),
        ("constructor_1", "delta", C(i + "qantir_azulejos.jpg", (0.5, 0.5), 1.4), 0.42),
        ("constructor_2", "tebas", X((("TEBAS · ", b), ("LUXOR", r))), 0.11),
        ("constructor_2", "funerario", C(i + "rameseo_coloso.jpg", (0.5, 0.4), 1.5), 0.44),
        ("constructor_3", "nubia", X((("NUBIA · ", b), ("FRONTERA SUR", r))), 0.11),
        ("constructor_3", "montana", C(i + "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", (0.30, 0.40), 2.4), 0.42),
        ("constructor_4", "cara", P(i + "luxor_ramses_rec.png"), 0.56),
        ("constructor_5", "santuario", F(i + "abusimbel_santuario.jpg", 760, (0.5, 0.5)), 0.34),
        ("constructor_6", "borrar", P(i + "estatua_usurpada_rec.png"), 0.52),
        ("constructor_6", "encima", C(i + "cartucho_ramses.jpg", (0.5, 0.5), 1.3), 0.42),
        ("constructor_7", "suyas", X((("OBRAS ", b), ("AJENAS", r))), 0.11),
        ("familia_0", "pequeno", F(i + "abusimbel_nefertari.jpg", 760, (0.5, 0.5)), 0.34),
        ("familia_1", "reales", C(i + "abusimbel_nefertari.jpg", (0.5, 0.45), 2.2), 0.42),
        ("familia_2", "hijas", C(i + "hijos_procesion.jpg", (0.3, 0.5), 2.0), 0.42),
        ("familia_3", "kv5", F(i + "kv5_entrada.jpg", 760, (0.5, 0.5)), 0.34),
        ("familia_4", "camaras", F(i + "kv5_plano.jpg", 760, (0.5, 0.5)), 0.36),
        ("familia_5", "enterro", C(i + "hijos_procesion.jpg", (0.72, 0.5), 2.4), 0.42),
        ("familia_7", "otro", F(i + "merenptah.jpg", 760, (0.5, 0.35)), 0.34),
        ("escondite_0", "cuerpo", P(i + "ataud_ramses_rec.png"), 0.58),
        ("escondite_0", "viaje", X((("OTRO ", b), ("VIAJE", r))), 0.11, (0.30, 0.64, 0.30, "sube")),
        ("escondite_1", "escondite", F(i + "deir_el_bahari.JPG", 760, (0.5, 0.5)), 0.34),
        ("escondite_2", "familia", X((("LA FAMILIA ", b), ("ABD EL-RASSUL", r))), 0.10, (-0.30, 0.66, 0.30, "der")),
        ("escondite_2", "1881", F(i + "db320_1881.jpg", 760, (0.5, 0.5)), 0.30),
        ("ozymandias_0", "belzoni", C(i + "belzoni_retrato.png", (0.5, 0.35), 1.2), 0.44),
        ("ozymandias_0", "londres", F(i + "belzoni_memnon.jpg", 760, (0.5, 0.5)), 0.34),
        ("ozymandias_1", "shelley", C(i + "shelley_retrato.jpg", (0.5, 0.35), 1.3), 0.44),
        ("ozymandias_2", "inscripcion", F(i + "ozymandias_examiner.jpg", 760, (0.5, 0.4)), 0.30),
        ("ozymandias_3", "obras", F(i + "rameseo_vista.jpg", 760, (0.3, 0.5)), 0.32),
        ("ozymandias_5", "inundar", F(i + "abusimbel_traslado2.jpg", 760, (0.5, 0.5)), 0.34),
        ("ozymandias_6", "unesco", F(i + "abusimbel_traslado.jpg", 760, (0.5, 0.5)), 0.34),
        ("ozymandias_6", "sesenta", X((("+65 ", r), ("METROS", b))), 0.11),
        ("ozymandias_7", "hongo", X((("UN ", b), ("HONGO", r))), 0.11),
        ("ozymandias_7", "paris", P(i + "avion_rec.png"), 0.34),
        ("cierre_0", "cairo", F(i + "desfile_2021.jpg", 760, (0.38, 0.6)), 0.34),
        ("cierre_0", "museo", F(i + "nmec.jpg", 760, (0.5, 0.5)), 0.32),
        ("cierre_1", "olvidara", P(i + "joven_memnon_rec.png"), 0.46),
    ]
    out = []
    for n, (key, pal, spr, alto, *fijo) in enumerate(L):
        ta = T(key, pal) - 0.1
        dx, dy, zr, anim = fijo[0] if fijo else _HUECOS[n % len(_HUECOS)]
        out.append((ta, _li(ta), (dx, dy, zr), alto, spr, anim))
    return out


_TUNEL = None


def _fondo_tunel(t):
    f = np.full((H, W, 3), NEGRO, np.float32)
    A.polvo(f, t, n=70, sem=21, op=0.35)
    return f


def render_mundo(t):
    global _TUNEL
    if _TUNEL is None:
        lam = [(t0, con_texto(fn), _POS[k]) for k, (t0, fn, _) in enumerate(TOMAS) if fn is not None]
        _TUNEL = TU.Tunel(lam, _capas(), 1.4)
        _TUNEL.txt_desde = TL["escenas"][2]["t0"] - 1.0             # tramo 4 en adelante (el 0-2 min aprobado queda igual)
    img = _TUNEL.render(t, _fondo_tunel(t))                               # túnel en TODO el video
    img = A.cine_antiguo(np.clip(img, 0, 1), t)
    img = img * smooth(prog(t, 0.0, 1.0)) * (1.0 - smooth(prog(t, TOTAL - 2.0, TOTAL - 0.1)))   # fundido a negro final (2 s)
    return np.clip(img, 0, 1).astype(np.float32)


def render_mundo_tomas(t):
    i = max(k for k, d in enumerate(TOMAS) if d[0] <= t)
    img = _cuadro(i, t)
    tipo, dur = TOMAS[i][2]
    if i > 0 and dur > 0 and t < TOMAS[i][0] + dur:
        pr = (t - TOMAS[i][0]) / dur
        img = TRANS[tipo](_cuadro(i - 1, t), img, pr, t) if tipo in TRANS else D.mezcla_tomas(_cuadro(i - 1, t), img, pr, tipo)
    img = A.cine_antiguo(np.clip(img, 0, 1), t)
    img = img * smooth(prog(t, 0.0, 1.0)) * (1.0 - smooth(prog(t, TOTAL - 2.0, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


# ------------------------------------------------------------------ sonido (nombres de SFX_ELEVEN en guion.py)
SFX = [
    (T("gancho_0", "avion") - 1.0, "jet_aterriza", 0.7),
    (T("gancho_1", "guardia"), "botas_firmes", 0.6),
    (T("gancho_2", "pasaporte") - 0.1, "neon_enciende", 0.55),
    (T("gancho_2", "rey"), "golpe_grave", 0.7),
    (T("gancho_2", "fallecido"), "golpe_grave", 0.8),
    (T("gancho_3", "nadie") - 0.2, "linterna_archivo", 0.5),
    (T("gancho_4", "quien") - 0.3, "aire_tumba", 0.6),
    (T("gancho_5", "ramses") - 0.2, "piedra_arrastre", 0.6),
    (TL["escenas"][1]["t0"] + 0.1, "viento_desierto", 0.55),
    (T("nieto_1", "su") - 0.4, "whoosh_suave", 0.4),
    (T("nieto_2", "trono") - 0.2, "whoosh_suave", 0.5),
    (T("nieto_2", "nacio"), "golpe_grave", 0.6),
    (T("nieto_3", "seti") - 0.6, "piedra_arrastre", 0.5),
    (T("nieto_4", "por") - 0.2, "antorchas", 0.5),
    (T("nieto_5", "libia") - 0.6, "whoosh_suave", 0.45),
    (T("nieto_5", "siria") - 0.4, "whoosh_suave", 0.45),
    (T("nieto_6", "se") - 0.1, "neon_enciende", 0.55),
    (T("nieto_7", "en") - 0.2, "antorchas", 0.45),
    (T("nieto_7", "ramses") - 0.1, "golpe_grave", 0.65),
    # tramo 4
    (fs("kadesh_0") - 0.4, "tambor_guerra", 0.7),
    (T("kadesh_1", "imperio") - 0.2, "whoosh_suave", 0.4),
    (fs("kadesh_2") - 0.3, "viento_desierto", 0.45),
    (fs("kadesh_3") - 0.3, "antorchas", 0.45),
    (fs("kadesh_4") - 0.1, "neon_enciende", 0.55),
    (T("kadesh_5", "carros") - 0.5, "carros_carga", 0.75),
    (T("kadesh_6", "cinco") - 0.2, "tambor_guerra", 0.6),
    (fs("kadesh_7") - 0.3, "carros_carga", 0.55),
    (T("kadesh_8", "nadie") - 0.1, "golpe_grave", 0.6),
    (fs("kadesh_9") - 0.3, "cincel_piedra", 0.55),
    (T("kadesh_11", "propaganda") - 0.2, "neon_enciende", 0.5),
    (fs("tratado_0") - 0.3, "whoosh_suave", 0.4),
    (fs("tratado_2") - 0.2, "tablilla_arcilla", 0.6),
    (T("tratado_4", "arcilla") - 0.2, "tablilla_arcilla", 0.5),
    (fs("tratado_6") - 0.2, "sello_cera", 0.55),
    (fs("constructor_0") - 0.2, "cincel_piedra", 0.6),
    (fs("constructor_3") - 0.3, "piedra_arrastre", 0.55),
    (T("constructor_5", "sol") - 0.3, "whoosh_suave", 0.45),
    (fs("constructor_6") - 0.1, "cincel_piedra", 0.6),
    (fs("familia_0") - 0.3, "whoosh_suave", 0.35),
    (fs("familia_3") - 0.3, "aire_tumba", 0.55),
    (fs("familia_5") + 1.0, "vela_apaga", 0.5),
    (T("familia_6", "murio") - 0.1, "golpe_grave", 0.55),
    (fs("escondite_0") - 0.3, "antorchas", 0.5),
    (T("escondite_2", "1881") - 0.3, "cuerdas_tension", 0.5),
    (fs("ozymandias_0") - 0.2, "cuerdas_tension", 0.55),
    (fs("ozymandias_1") - 0.2, "pluma_papel", 0.5),
    (fs("ozymandias_4") - 0.3, "viento_desierto", 0.55),
    (T("ozymandias_5", "inundar") - 0.3, "agua_sube", 0.6),
    (T("ozymandias_6", "cort") - 0.2, "sierra_piedra", 0.5),
    (T("ozymandias_7", "paris") - 0.2, "laboratorio_zumbido", 0.5),
    (fs("cierre_0") - 0.2, "fuegos_artificiales", 0.55),
    (T("cierre_2", "fallecido") - 0.1, "golpe_grave", 0.75),
]


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v in SFX:
                self.ev(t, n, v)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
