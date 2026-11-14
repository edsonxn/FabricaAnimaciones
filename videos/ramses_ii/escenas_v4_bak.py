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
        (TL["escenas"][2]["t0"], None, ("negro", 1.0)),       # lo que sigue aún no está animado
    ]


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
    ]


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
    if t < TOMAS[-1][0]:
        img = _TUNEL.render(t, _fondo_tunel(t))
        img = A.cine_antiguo(np.clip(img, 0, 1), t)
        img = img * smooth(prog(t, 0.0, 1.0))
        return np.clip(img, 0, 1).astype(np.float32)
    return render_mundo_tomas(t)


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
]


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v in SFX:
                self.ev(t, n, v)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
