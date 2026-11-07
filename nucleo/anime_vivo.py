# -*- coding: utf-8 -*-
"""ANIME VIVO — animación limitada estilo anime con imágenes de Flow (6-nov-2026, remake `llamada_anime`).

Idea: el anime de TV/cine ya es «animación limitada» (dibujos sostenidos + bocas de 3 posiciones + parpadeos + paneos de
cámara sobre fondos pintados + efectos de luz). Eso se puede hacer con IMÁGENES de Flow (0 puntos) y código, y se siente
animación real, no una secuencia de fotos:
  · base = cuadro del plano (Nano Banana, ficha anime) · variantes = la MISMA imagen editada en Flow (ingrediente = la base):
    boca media / boca abierta (un prompt x2 da las dos aperturas) y ojos cerrados (parpadeo). Se alinean (ECC) y la zona que
    cambia (la cara) se calcula sola por diferencia → máscara suave → se intercambia por cuadro, como cels.
  · labios por la ENVOLVENTE del audio real del diálogo (a 15 Hz, con histéresis y alternancia media/abierta).
  · parpadeo cada 2,5-5 s (3 cuadros). Respiración y cabeceo del personaje recortado (rembg) sobre el fondo rellenado.
  · cámara: zoom/paneo con easing + parallax de 2 capas (fondo 0,55 del personaje) + temblor opcional.
  · efectos: polvo en la luz, rayos, lluvia, parpadeo de fluorescente, brillo de pantalla, bloom y viñeta.

Uso (desde un script del video):
    import anime_vivo as AV
    t = AV.Toma("imgs/ramon_tel.jpg", bocas=["imgs/ramon_tel_b1.jpg", "imgs/ramon_tel_b2.jpg"], ojos=["imgs/ramon_tel_o1.jpg"],
                cam=dict(z0=1.0, z1=1.12, c0=(0.5, 0.45), c1=(0.56, 0.4)), fx=[("polvo", dict(caja=(0.6, 0, 1, 0.7)))])
    AV.render([(0.0, t)], dur=10.0, audio="voz.wav", salida="medios/scene-005.mp4")
Varias tomas en un plano: lista [(t_inicio, Toma), ...] con corte seco entre ellas (anime = cortes).
"""
import math
import os
import subprocess

import cv2
import numpy as np

W, H, FPS = 1920, 1080, 30
SUPER = 2.0                     # las imágenes de Flow (1376x768) se suben a 2x una vez; la cámara baja desde ahí (nítido)
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe" if os.path.exists(r"C:\ffmpeg\bin\ffmpeg.exe") else "ffmpeg"
_CACHE = {}


# ───────────────────────────── imágenes ─────────────────────────────
def _leer(r):
    im = cv2.imread(r, cv2.IMREAD_COLOR)
    if im is None:
        raise FileNotFoundError(r)
    return im


def _subir(im):
    h, w = im.shape[:2]
    up = cv2.resize(im, (int(w * SUPER), int(h * SUPER)), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(up, (0, 0), 1.2)
    return cv2.addWeighted(up, 1.35, bl, -0.35, 0)          # realce suave de línea


def alinear(base, x):
    """Alinea la variante `x` con `base` (ECC afín en gris a media resolución). Devuelve x alineada."""
    if x.shape != base.shape:
        x = cv2.resize(x, (base.shape[1], base.shape[0]), interpolation=cv2.INTER_AREA)
    a = cv2.cvtColor(cv2.resize(base, None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY).astype(np.float32)
    b = cv2.cvtColor(cv2.resize(x, None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY).astype(np.float32)
    M = np.eye(2, 3, dtype=np.float32)
    try:
        cv2.findTransformECC(a, b, M, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), None, 5)
    except cv2.error:
        return x
    M[:, 2] *= 2.0
    return cv2.warpAffine(x, M, (base.shape[1], base.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_REPLICATE)


def mascara_cambio(base, variantes, umbral=24, cierre=31, dil=10, pluma=15, caja=None, todas=False):
    """Zona que cambia entre la base y sus variantes (la cara): diferencia → cierre → componente(s) mayor(es) → casco
    convexo → dilatar → pluma. `caja` = (x0, y0, x1, y1) normalizada para limitarla. Devuelve float32 0..1 (h, w)."""
    h, w = base.shape[:2]
    d = np.zeros((h, w), np.float32)
    for v in variantes:
        dd = np.abs(v.astype(np.int16) - base.astype(np.int16)).max(2).astype(np.float32)
        d = np.maximum(d, cv2.GaussianBlur(dd, (7, 7), 0))
    m = (d > umbral).astype(np.uint8)
    if caja:
        z = np.zeros_like(m)
        x0, y0, x1, y1 = caja
        z[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = 1
        m *= z
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cierre, cierre)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    out = np.zeros_like(m)
    if n > 1:
        orden = sorted(range(1, n), key=lambda i: -st[i, 4])
        sel = orden if todas else [i for i in orden if st[i, 4] >= 0.25 * st[orden[0], 4]][:3]
        for i in sel:
            if st[i, 4] < 60:
                continue
            cs, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.fillPoly(out, [cv2.convexHull(np.vstack(cs))], 1)
    out = cv2.dilate(out, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil * 2 + 1, dil * 2 + 1)))
    return cv2.GaussianBlur(out.astype(np.float32), (0, 0), pluma)


def recorte_personaje(base, modelo="isnet-general-use"):
    """Alfa del/los personaje(s) con rembg (float32 0..1)."""
    from rembg import new_session, remove
    from PIL import Image
    key = ("rembg", modelo)
    if key not in _CACHE:
        _CACHE[key] = new_session(modelo)
    rgb = Image.fromarray(cv2.cvtColor(base, cv2.COLOR_BGR2RGB))
    a = np.asarray(remove(rgb, session=_CACHE[key], only_mask=True), np.float32) / 255.0
    return a


def rellenar(base, alfa, dil=14):
    """Fondo sin el personaje (inpaint TELEA a media resolución, máscara dilatada)."""
    m = (alfa > 0.25).astype(np.uint8)
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil * 2 + 1, dil * 2 + 1)))
    s = cv2.resize(base, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, (s.shape[1], s.shape[0]), interpolation=cv2.INTER_NEAREST)
    f = cv2.inpaint(s, ms * 255, 9, cv2.INPAINT_TELEA)
    f = cv2.resize(f, (base.shape[1], base.shape[0]), interpolation=cv2.INTER_CUBIC)
    f = cv2.GaussianBlur(f, (0, 0), 2.0)
    mf = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3)[..., None]
    return (base * (1 - mf) + f * mf).astype(np.uint8)


# ───────────────────────────── audio → bocas ─────────────────────────────
def envolvente(ruta, dur, fps=FPS, t0=0.0):
    """RMS del audio (archivo de audio o video) por cuadro, normalizada 0..1 (percentil 95)."""
    if not ruta or not os.path.exists(ruta):
        return np.zeros(int(round(dur * fps)) + 1, np.float32)
    sr = 16000
    p = subprocess.run([FFMPEG, "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", ruta, "-vn", "-ac", "1",
                        "-ar", str(sr), "-f", "s16le", "-"], capture_output=True)
    x = np.frombuffer(p.stdout, np.int16).astype(np.float32) / 32768.0
    n = int(round(dur * fps)) + 1
    hop = sr / fps
    e = np.zeros(n, np.float32)
    for i in range(n):
        a, b = int(i * hop - hop * 0.5), int(i * hop + hop * 1.0)
        seg = x[max(0, a):max(0, b)]
        e[i] = math.sqrt(float((seg ** 2).mean())) if len(seg) else 0.0
    ref = np.percentile(e[e > 1e-4], 95) if (e > 1e-4).any() else 1.0
    return np.clip(e / max(ref, 1e-6), 0, 1.2)


def estados_boca(env, n_bocas, cada=2, seed=0):
    """Estado de boca por cuadro: 0 cerrada, 1..n_bocas abierta (1 = media). Se decide cada `cada` cuadros (15 Hz a 30 fps),
    con histéresis y alternancia para que no quede abierta fija (como las bocas de anime)."""
    rng = np.random.default_rng(seed)
    n = len(env)
    s = np.zeros(n, np.int32)
    prev = 0
    racha = 0
    for i in range(0, n, cada):
        v = float(env[i:i + cada].mean())
        if v < (0.16 if prev == 0 else 0.11):
            st = 0
        elif n_bocas == 1 or v < 0.48:
            st = 1
        else:
            st = n_bocas
        if st == prev and st > 0:
            racha += 1
            if racha >= 3 and n_bocas > 1:                     # alterna media/abierta en vocales largas
                st = 1 if prev == n_bocas else n_bocas
                racha = 0
        else:
            racha = 0
        if st > 0 and rng.random() < 0.08:                   # cierre breve de consonante
            st = 0
        s[i:i + cada] = st
        prev = st
    return s


def parpadeos(dur, fps=FPS, seed=0, cada=(2.4, 5.0)):
    rng = np.random.default_rng(seed + 7)
    n = int(round(dur * fps)) + 1
    b = np.zeros(n, bool)
    t = rng.uniform(0.6, 2.0)
    while t < dur:
        i = int(t * fps)
        b[i:i + 3] = True
        if rng.random() < 0.18:                               # doble parpadeo
            b[i + 6:i + 9] = True
        t += rng.uniform(*cada)
    return b


# ───────────────────────────── efectos ─────────────────────────────
def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


class Polvo:
    """Motas de polvo que flotan en la luz (aditivas)."""
    def __init__(self, caja=(0.5, 0.0, 1.0, 0.8), n=70, color=(200, 235, 255), seed=1, op=0.55):
        r = np.random.default_rng(seed)
        self.p = r.random((n, 2))
        self.v = (r.random((n, 2)) - 0.5) * np.array([0.010, 0.006]) + np.array([0.004, -0.003])
        self.s = r.uniform(1.0, 3.2, n)
        self.f = r.uniform(0, 6.28, n)
        self.caja, self.color, self.op = caja, np.array(color, np.float32), op

    def __call__(self, img, t):
        x0, y0, x1, y1 = self.caja
        capa = np.zeros((H // 2, W // 2), np.float32)
        p = (self.p + self.v * t) % 1.0
        for (u, v), s, f in zip(p, self.s, self.f):
            X, Y = (x0 + u * (x1 - x0)) * W / 2, (y0 + v * (y1 - y0)) * H / 2
            a = 0.5 + 0.5 * math.sin(t * 1.3 + f)
            cv2.circle(capa, (int(X), int(Y)), max(1, int(s)), a, -1, cv2.LINE_AA)
        capa = cv2.GaussianBlur(capa, (0, 0), 1.4)
        capa = cv2.resize(capa, (W, H))[..., None]
        return np.clip(img + capa * self.color * self.op, 0, 255)


class Rayos:
    """Haces de luz diagonales que respiran (aditivos)."""
    def __init__(self, origen=(0.85, -0.1), ang=115, color=(170, 215, 255), op=0.16, n=5, seed=2):
        r = np.random.default_rng(seed)
        self.o, self.ang, self.color, self.op = origen, math.radians(ang), np.array(color, np.float32), op
        self.anch = r.uniform(0.03, 0.09, n)
        self.desv = r.uniform(-0.35, 0.35, n)
        self.fase = r.uniform(0, 6.28, n)
        self._g = None

    def __call__(self, img, t):
        if self._g is None:
            yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
            xx, yy = xx / (W / 4), yy / (H / 4) * (H / W)
            self._d = (xx - self.o[0], yy - self.o[1] * H / W)
            self._g = True
        dx, dy = self._d
        ang = np.arctan2(dy, dx)
        dist = np.sqrt(dx * dx + dy * dy)
        capa = np.zeros_like(dx)
        for a, d, f in zip(self.anch, self.desv, self.fase):
            k = np.exp(-((ang - (self.ang + d * 0.6)) / a) ** 2)
            capa += k * (0.55 + 0.45 * math.sin(t * 0.7 + f))
        capa *= np.exp(-dist * 1.2)
        capa = cv2.resize(capa, (W, H))[..., None]
        return np.clip(img + capa * self.color * self.op, 0, 255)


class Lluvia:
    """Rayas de lluvia (en una caja: la ventana) que caen."""
    def __init__(self, caja=(0, 0, 1, 1), n=260, op=0.35, seed=3, color=(225, 230, 240), vel=1.6):
        r = np.random.default_rng(seed)
        self.p = r.random((n, 2))
        self.l = r.uniform(0.02, 0.05, n)
        self.v = r.uniform(0.8, 1.2, n) * vel
        self.caja, self.op, self.color = caja, op, np.array(color, np.float32)

    def __call__(self, img, t):
        x0, y0, x1, y1 = self.caja
        capa = np.zeros((H // 2, W // 2), np.float32)
        for (u, v), l, vv in zip(self.p, self.l, self.v):
            yy = (v + vv * t) % 1.0
            X = (x0 + ((u + 0.12 * yy) % 1.0) * (x1 - x0)) * W / 2
            Y = (y0 + yy * (y1 - y0)) * H / 2
            cv2.line(capa, (int(X), int(Y)), (int(X - 0.12 * l * H / 2), int(Y - l * H / 2)), 0.8, 1, cv2.LINE_AA)
        capa = cv2.resize(cv2.GaussianBlur(capa, (0, 0), 0.6), (W, H))[..., None]
        return np.clip(img * (1 - capa * 0.15) + capa * self.color * self.op, 0, 255)


class Fluor:
    """Parpadeo de lámpara fluorescente / luz que late (multiplica el cuadro)."""
    def __init__(self, base=1.0, amp=0.05, cortes=True, seed=4):
        self.r = np.random.default_rng(seed)
        self.base, self.amp, self.cortes = base, amp, cortes
        self.cort = set(int(x) for x in self.r.uniform(0, 30 * 60, 14)) if cortes else set()

    def __call__(self, img, t):
        k = self.base + self.amp * math.sin(t * 9.1) * math.sin(t * 2.3)
        if int(t * FPS) in self.cort or int(t * FPS) - 1 in self.cort:
            k *= 0.82
        return np.clip(img * k, 0, 255)


class Brillo:
    """Halo de luz que late en un punto (pantalla de teléfono, lámpara)."""
    def __init__(self, pos=(0.5, 0.5), r=0.18, color=(255, 220, 170), op=0.22, f=0.9):
        self.pos, self.r, self.color, self.op, self.f = pos, r, np.array(color, np.float32), op, f
        yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
        d = ((xx / (W / 4) - pos[0]) * W / H) ** 2 + (yy / (H / 4) - pos[1]) ** 2
        self.k = cv2.resize(np.exp(-d / (r * r)), (W, H))[..., None]

    def __call__(self, img, t):
        a = self.op * (0.8 + 0.2 * math.sin(t * self.f * 6.28))
        return np.clip(img + self.k * self.color * a, 0, 255)


EFECTOS = dict(polvo=Polvo, rayos=Rayos, lluvia=Lluvia, fluor=Fluor, brillo=Brillo)


def acabado(img, bloom=0.16, vineta=0.30, tinte=None):
    """Bloom de altas luces + viñeta + tinte opcional (b, g, r multiplicador)."""
    f = img.astype(np.float32)
    if bloom:
        hi = np.clip(f - 170, 0, 255)
        hi = cv2.resize(cv2.GaussianBlur(cv2.resize(hi, (W // 4, H // 4)), (0, 0), 6), (W, H))
        f = f + hi * bloom * 2.2
    if tinte is not None:
        f = f * np.array(tinte, np.float32)
    if vineta:
        if "vin" not in _CACHE:
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            d = ((xx / W - 0.5) ** 2 + ((yy / H - 0.5) * 0.8) ** 2) * 4
            _CACHE["vin"] = (1 - np.clip(d, 0, 1.6) * 0.5)[..., None]
        f = f * (1 - vineta + vineta * _CACHE["vin"])
    return np.clip(f, 0, 255)


# ───────────────────────────── toma ─────────────────────────────
class Toma:
    """Un plano de cámara: base + variantes de boca/ojos + personaje recortado + cámara + efectos.
    cam: z0, z1 (zoom 1 = encuadre completo), c0, c1 (centro normalizado), temblor (px), par (parallax del fondo 0..1).
    mov: 'respira' (por defecto), 'quieto', 'cabeceo' (asiente con la voz), 'tiembla' (llanto).
    caja_cara: limita la máscara de cambio. personaje=False: sin recorte (solo cámara y caras)."""
    def __init__(self, base, bocas=(), ojos=(), cam=None, fx=(), mov="respira", caja_cara=None, personaje=True,
                 tinte=None, bloom=0.16, vineta=0.30, seed=0, voz_desde=0.0, desfase=0.0):
        self.rutas = (base, list(bocas), list(ojos))
        self.cam = dict(z0=1.0, z1=1.08, c0=(0.5, 0.5), c1=(0.5, 0.5), temblor=0.0, par=0.55)
        self.cam.update(cam or {})
        self.fx_def = list(fx)
        self.mov, self.caja, self.personaje = mov, caja_cara, personaje
        self.tinte, self.bloom, self.vineta, self.seed = tinte, bloom, vineta, seed
        self.voz_desde, self.desfase = voz_desde, desfase
        self._listo = False

    def preparar(self):
        if self._listo:
            return
        base, bocas, ojos = self.rutas
        b = _leer(base)
        vb = [alinear(b, _leer(r)) for r in bocas]
        vo = [alinear(b, _leer(r)) for r in ojos]
        self.mb = mascara_cambio(b, vb, caja=self.caja) if vb else None
        self.mo = mascara_cambio(b, vo, caja=self.caja) if vo else None
        if self.personaje:
            a = recorte_personaje(b)
            if self.mb is not None:
                a = np.maximum(a, self.mb)
            if self.mo is not None:
                a = np.maximum(a, self.mo)
            fondo = rellenar(b, a)
        else:
            a, fondo = None, b
        S = _subir
        self.B = S(b).astype(np.float32)
        self.VB = [S(v).astype(np.float32) for v in vb]
        self.VO = [S(v).astype(np.float32) for v in vo]
        up = lambda m: cv2.resize(m, (self.B.shape[1], self.B.shape[0]), interpolation=cv2.INTER_LINEAR)[..., None]
        self.MB = up(self.mb) if self.mb is not None else None
        self.MO = up(self.mo) if self.mo is not None else None
        self.A = up(cv2.GaussianBlur(a, (0, 0), 1.0)) if a is not None else None
        self.F = S(fondo).astype(np.float32) if a is not None else None
        ys, xs = np.nonzero(a > 0.5) if a is not None else (np.array([b.shape[0]]), np.array([b.shape[1] // 2]))
        self.pie = (float(xs.mean()) * SUPER if len(xs) else self.B.shape[1] / 2, float(ys.max()) * SUPER if len(ys) else self.B.shape[0])
        self.fx = [EFECTOS[n](**kw) for n, kw in self.fx_def]
        self._listo = True

    def _matriz(self, t, dur, capa):
        c = self.cam
        u = _ease(t / max(dur, 1e-6))
        z = c["z0"] + (c["z1"] - c["z0"]) * u
        cx = c["c0"][0] + (c["c1"][0] - c["c0"][0]) * u
        cy = c["c0"][1] + (c["c1"][1] - c["c0"][1]) * u
        hS, wS = self.B.shape[:2]
        esc = max(W / wS, H / hS) * z
        # cámara en mano + temblor
        dx = 3.0 * math.sin(t * 0.53 + self.seed) + 2.0 * math.sin(t * 1.31 + 2 * self.seed)
        dy = 2.0 * math.sin(t * 0.71 + 3 * self.seed) + 1.4 * math.sin(t * 1.07)
        if c["temblor"]:
            dx += c["temblor"] * math.sin(t * 23.0) * math.sin(t * 3.1)
            dy += c["temblor"] * math.cos(t * 19.0) * math.sin(t * 2.7)
        X = cx * wS * esc
        Y = cy * hS * esc
        X = min(max(X, W / 2), wS * esc - W / 2)
        Y = min(max(Y, H / 2), hS * esc - H / 2)
        k = 1.0 if capa == "pj" else c["par"]
        # parallax: el fondo recorre una fracción del desplazamiento de cámara respecto del centro de la imagen
        X0, Y0 = wS * esc / 2, hS * esc / 2
        Xc = X0 + (X - X0) * k + (dx * (1 if capa == "pj" else c["par"]))
        Yc = Y0 + (Y - Y0) * k + (dy * (1 if capa == "pj" else c["par"]))
        if capa != "pj":                                       # el fondo, un poco más grande para no enseñar bordes
            esc *= 1.0 + (1 - c["par"]) * 0.06
            Xc = Xc * (1.0 + (1 - c["par"]) * 0.06)
            Yc = Yc * (1.0 + (1 - c["par"]) * 0.06)
        return np.float32([[esc, 0, W / 2 - Xc], [0, esc, H / 2 - Yc]])

    def cuadro(self, t, dur, boca, ojo, env):
        self.preparar()
        img = self.B
        if ojo and self.VO:
            img = img * (1 - self.MO) + self.VO[0] * self.MO
        elif boca and self.VB:
            v = self.VB[min(boca, len(self.VB)) - 1]
            img = img * (1 - self.MB) + v * self.MB
        if self.A is None:
            out = cv2.warpAffine(img, self._matriz(t, dur, "pj"), (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT)
        else:
            Mf = self._matriz(t, dur, "fondo")
            fondo = cv2.warpAffine(self.F, Mf, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT)
            M = self._matriz(t, dur, "pj").astype(np.float64)
            # movimiento propio del personaje, con pivote en los pies
            px, py = self.pie
            sy, ang, ty = 1.0, 0.0, 0.0
            if self.mov in ("respira", "cabeceo", "tiembla"):
                sy = 1.0 + 0.0055 * math.sin(t * 2 * math.pi * 0.24 + self.seed)
            if self.mov == "cabeceo":
                ang = 0.35 * math.sin(t * 2.1) * (0.4 + env)
                ty = -2.5 * env
            if self.mov == "tiembla":
                ang = 0.25 * math.sin(t * 17.0) * math.sin(t * 1.3)
                sy += 0.004 * math.sin(t * 5.0)
            R = cv2.getRotationMatrix2D((px, py), ang, 1.0)
            R = np.vstack([R, [0, 0, 1]])
            Sy = np.array([[1, 0, 0], [0, sy, py * (1 - sy) + ty], [0, 0, 1]])
            M3 = np.vstack([M, [0, 0, 1]]) @ R @ Sy
            M2 = M3[:2].astype(np.float32)
            pj = cv2.warpAffine(img, M2, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT)
            al = cv2.warpAffine(self.A, M2, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)[..., None]
            out = fondo * (1 - al) + pj * al
        for f in self.fx:
            out = f(out, t)
        return acabado(out, self.bloom, self.vineta, self.tinte)


# ───────────────────────────── render ─────────────────────────────
def render(tomas, dur, salida, audio=None, audio_t0=0.0, fps=FPS, crf=18, seed=0, mux_audio=False, fundido_negro=None):
    """tomas = [(t_inicio, Toma), ...] (cortes secos). `audio` = archivo con el diálogo de ESTE plano (para los labios).
    mux_audio=True mete ese audio en el mp4. fundido_negro = (entrada_s, salida_s)."""
    n = int(round(dur * fps))
    env = envolvente(audio, dur, fps, audio_t0)
    tomas = sorted(tomas, key=lambda x: x[0])
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    tmp = salida + ".tmp.mp4"
    cmd = [FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if mux_audio and audio:
        cmd += ["-ss", f"{audio_t0:.3f}", "-t", f"{dur:.3f}", "-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    estados = {}
    for k, (ti, tm) in enumerate(tomas):
        tf = tomas[k + 1][0] if k + 1 < len(tomas) else dur
        tm.preparar()
        nb = len(tm.VB)
        i0, i1 = int(round(ti * fps)), int(round(tf * fps))
        e = env[i0:i1 + 1]
        estados[k] = (estados_boca(e, nb, seed=seed + k) if nb else np.zeros(len(e), np.int32),
                      parpadeos((i1 - i0) / fps + 0.1, fps, seed + k) if tm.VO else np.zeros(len(e) + 4, bool))
    for i in range(n):
        t = i / fps
        k = max(j for j, (ti, _) in enumerate(tomas) if ti <= t + 1e-6) if any(ti <= t + 1e-6 for ti, _ in tomas) else 0
        ti, tm = tomas[k]
        j = i - int(round(ti * fps))
        sb, so = estados[k]
        boca = int(sb[min(j, len(sb) - 1)]) if len(sb) else 0
        ojo = bool(so[min(j, len(so) - 1)]) if len(so) else False
        fr = tm.cuadro(t - ti + tm.desfase, tf_dur(tomas, k, dur) + tm.desfase, boca, ojo, float(env[min(i, len(env) - 1)]))
        if fundido_negro:
            a, b = fundido_negro
            if a and t < a:
                fr = fr * (t / a)
            if b and t > dur - b:
                fr = fr * max(0.0, (dur - t) / b)
        p.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()
    os.replace(tmp, salida)
    return salida


def tf_dur(tomas, k, dur):
    return (tomas[k + 1][0] if k + 1 < len(tomas) else dur) - tomas[k][0]


def cuadros(tomas, dur, tiempos, salida, audio=None):
    """Hoja de prueba: cuadros en `tiempos` (s) → jpg 2 columnas a 640x360."""
    env = envolvente(audio, dur)
    ims = []
    for t in tiempos:
        k = max(j for j, (ti, _) in enumerate(tomas) if ti <= t + 1e-6)
        ti, tm = tomas[k]
        i = int(t * FPS)
        fr = tm.cuadro(t - ti, tf_dur(tomas, k, dur), 2 if env[min(i, len(env) - 1)] > 0.4 else 0, False, float(env[min(i, len(env) - 1)]))
        ims.append(cv2.resize(fr.astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA))
    if len(ims) % 2:
        ims.append(np.zeros_like(ims[0]))
    filas = [np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)]
    cv2.imwrite(salida, np.vstack(filas))
    return salida
