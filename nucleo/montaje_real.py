# -*- coding: utf-8 -*-
"""Montador del estilo «Jefe de Robots»: grabaciones reales a pantalla completa con cámara (zoom, paneo), transiciones variadas,
Token de cámara de streamer y El Jefe de canadiense. Reutilizable para cada video del canal. Doc: docs/estilo_jefe_robots.md.

  from montaje_real import Montaje, plano
  m = Montaje("medios/toma.mp4", total=300)
  m.planos = [plano("capturas/vivo.mp4", 0, 6, cam=[(0, 1.0, .5, .5), (6, 2.2, .3, .4)], tr=("latigo", .3)), ...]
  m.camara(de, a, esquina="ad")           # Token en su ventanita
  m.jefe(de, a, "voz/final/como_2.wav")   # El Jefe salta a escena
  m.render(hasta=None)

plano(clip, de, a, desde=0, vel=1, cam=[(t, z, cx, cy), ...], tr=(tipo, dur), reloj=False)
  t absoluto en segundos; z=1 el cuadro entero; z>1 acerca a (cx, cy), en fracciones de la grabación; z<1 = la pantalla flotando sobre fondo oscuro.
  reloj=True: el clip corre con el video (fuente de Token), desde = desfase.
Transiciones: corte, latigo, zoom, deslizar, glitch, destello. La transición va centrada en `de` y el plano anterior sigue vivo durante ella.
"""
import math
import os
import subprocess

import cv2
import numpy as np

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
W, H = 1920, 1080
ACENTO = (225, 243, 125)      # BGR del turquesa del taller
_FUENTES = (r"C:\Windows\Fonts\seguibl.ttf", r"C:\Windows\Fonts\segoeuib.ttf")


def _suave(u):
    return u * u * (3 - 2 * u)


def _rapido(u):
    return 1 - (1 - u) ** 3


def plano(clip, de, a, desde=0.0, vel=1.0, cam=None, tr=None, reloj=False):
    return dict(clip=clip, de=de, a=a, desde=desde, vel=vel, cam=cam or [(de, 1.0, .5, .5)], tr=tr or ("corte", 0), reloj=reloj)


class _Clip:
    """Lee cuadros por segundo; adelante es secuencial y barato, y solo salta si hace falta."""

    def __init__(self, ruta):
        if not os.path.exists(ruta):
            raise FileNotFoundError(ruta)
        self.ruta, self.cap = ruta, cv2.VideoCapture(ruta)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.pos, self.ult, self.chico = -1, None, None

    def leer(self, seg):
        f = int(max(0, seg) * self.fps)
        f = min(f, self.n - 1)
        if f == self.pos and self.ult is not None:
            return self.ult
        if f < self.pos or f > self.pos + 45:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, f)
            self.pos = f - 1
        while self.pos < f:
            ok, g = self.cap.read()
            if not ok:
                self.n = max(1, self.pos)
                break
            self.ult, self.pos, self.chico = g, self.pos + 1, None
        return self.ult

    def base(self):
        """Copia a 1920 para cuando se ve casi entero: reducir bien evita el dentado."""
        if self.chico is None:
            self.chico = cv2.resize(self.ult, (W, H), interpolation=cv2.INTER_AREA)
        return self.chico


def _encuadre(src, chico, z, cx, cy):
    """z>=1: recorte subpíxel a 1920x1080 (sin saltitos en los zooms lentos)."""
    fuente = chico if z < 1.3 else src
    sh, sw = fuente.shape[:2]
    an, al = sw / z, sh / z
    x = min(max(cx * sw - an / 2, 0), sw - an)
    y = min(max(cy * sh - al / 2, 0), sh - al)
    k = W / an
    M = np.float32([[k, 0, -x * k], [0, k, -y * k]])
    return cv2.warpAffine(fuente, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def _flotante(chico, z):
    """z<1: la pantalla entera flotando, con sombra, sobre su propio reflejo oscuro."""
    fondo = cv2.resize(cv2.blur(cv2.resize(chico, (240, 135), interpolation=cv2.INTER_AREA), (21, 21)), (W, H), interpolation=cv2.INTER_LINEAR)
    fondo = (fondo.astype(np.float32) * .22 + np.array((34, 24, 18), np.float32) * .78).astype(np.uint8)
    an, al = int(W * z) // 2 * 2, int(H * z) // 2 * 2
    x, y = (W - an) // 2, (H - al) // 2
    sombra = np.zeros((H // 4, W // 4), np.float32)
    cv2.rectangle(sombra, (x // 4 - 2, y // 4 + 2), ((x + an) // 4 + 2, (y + al) // 4 + 6), 1.0, -1)
    sombra = cv2.resize(cv2.GaussianBlur(sombra, (0, 0), 9), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    fondo = (fondo * (1 - sombra * .75)).astype(np.uint8)
    interpol = cv2.INTER_AREA if z < 1 else cv2.INTER_LINEAR
    fondo[y:y + al, x:x + an] = cv2.resize(chico, (an, al), interpolation=interpol)
    cv2.rectangle(fondo, (x - 2, y - 2), (x + an + 1, y + al + 1), (120, 100, 90), 2, cv2.LINE_AA)
    return fondo


def _desliza(img, dx, dy=0):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)


def _escala(img, k):
    an, al = W / k, H / k
    x, y = (W - an) / 2, (H - al) / 2
    return cv2.warpAffine(img, np.float32([[k, 0, -x * k], [0, k, -y * k]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


_rng = np.random.default_rng(7)


def _glitch(img, fuerza):
    out = img.copy()
    d = int(26 * fuerza) + 2
    out[..., 2] = np.roll(img[..., 2], d, axis=1)
    out[..., 0] = np.roll(img[..., 0], -d, axis=1)
    for _ in range(int(9 * fuerza) + 3):
        y = int(_rng.integers(0, H - 80))
        al = int(_rng.integers(14, 80))
        out[y:y + al] = np.roll(out[y:y + al], int(_rng.integers(-160, 160)), axis=1)
    return out


def transicion(tipo, a, b, u):
    """a = plano que sale, b = el que entra, u de 0 a 1."""
    if tipo == "latigo":
        v = _suave(u)
        k = int(4 + 230 * math.sin(math.pi * u)) | 1
        return cv2.blur(_desliza(a if v < .5 else b, -W * (v * 2 if v < .5 else (v - 1) * 2)), (k, 1))
    if tipo == "zoom":
        v = _suave(u)
        im = _escala(a, 1 + 1.6 * v * 2) if u < .5 else _escala(b, .62 + .38 * (2 * v - 1))
        return cv2.blur(im, (int(3 + 34 * math.sin(math.pi * u)) | 1,) * 2)
    if tipo == "deslizar":
        v = _rapido(u)
        y = int(H * (1 - v))
        out = (a.astype(np.float32) * (1 - .55 * v)).astype(np.uint8)
        if y < H:
            out[y:] = b[:H - y]
            cv2.line(out, (0, y), (W, y), ACENTO, 3, cv2.LINE_AA)
        return out
    if tipo == "glitch":
        return _glitch(a if u < .5 else b, math.sin(math.pi * u))
    if tipo == "destello":
        k = 1 - abs(2 * u - 1)
        return cv2.addWeighted(a if u < .5 else b, 1 - k, np.full_like(a, 255), k, 0)
    return b


class Montaje:
    def __init__(self, salida, total, fps=30, crf=20):
        self.salida, self.total, self.fps, self.crf = salida, total, fps, crf
        self.planos, self.ventanas, self.jefes, self.encima = [], [], [], []
        self._clips = {}
        self._marco = None
        self._jefe = None

    def clip(self, ruta):
        if ruta not in self._clips:
            self._clips[ruta] = _Clip(ruta)
        return self._clips[ruta]

    def camara(self, de, a, esquina="ad", fuente="medios/token.mp4", caja=(0, .3, .42, .7), ancho=420):
        """Token en su ventanita. caja = (x, y, an, al) en fracciones de la toma del taller. esquina: ad, ai, bd, bi."""
        self.ventanas.append(dict(de=de, a=a, esq=esquina, fuente=fuente, caja=caja, ancho=ancho))

    def jefe(self, de, a, wav, lado="d", alto=760):
        self.jefes.append(dict(de=de, a=a, wav=wav, lado=lado, alto=alto, amp=None))

    # ---- cuadros
    def _vista(self, p, t):
        c = self.clip(p["clip"])
        seg = (t + p["desde"]) if p["reloj"] else p["desde"] + (t - p["de"]) * p["vel"]
        src = c.leer(seg)
        if src is None:
            return np.zeros((H, W, 3), np.uint8)
        k = p["cam"]
        if t <= k[0][0]:
            z, cx, cy = k[0][1:]
        elif t >= k[-1][0]:
            z, cx, cy = k[-1][1:]
        else:
            i = next(n for n in range(len(k) - 1) if k[n][0] <= t < k[n + 1][0])
            a, b = k[i], k[i + 1]
            u = _suave((t - a[0]) / max(1e-3, b[0] - a[0]))
            z = a[1] * (b[1] / a[1]) ** u          # el zoom se siente parejo en escala geométrica
            cx, cy = a[2] + (b[2] - a[2]) * u, a[3] + (b[3] - a[3]) * u
        if z < 1:
            return _flotante(c.base(), z)
        return _encuadre(src, c.base(), z, cx, cy)

    def _base(self, t):
        act = None
        for i, p in enumerate(self.planos):
            if p["de"] <= t < p["a"]:
                act = i
                break
        if act is None:
            return np.zeros((H, W, 3), np.uint8)
        p = self.planos[act]
        # transición de entrada
        tipo, d = p["tr"]
        if d and act and t < p["de"] + d / 2:
            u = (t - (p["de"] - d / 2)) / d
            return transicion(tipo, self._vista(self.planos[act - 1], t), self._vista(p, t), u)
        # transición de salida: el siguiente ya se ve
        if act + 1 < len(self.planos):
            q = self.planos[act + 1]
            tipo, d = q["tr"]
            if d and t >= q["de"] - d / 2:
                u = (t - (q["de"] - d / 2)) / d
                return transicion(tipo, self._vista(p, t), self._vista(q, t), u)
        return self._vista(p, t)

    def _marco_token(self, an, al):
        """Marco de ventanita de streamer, una vez: esquinas redondas, borde y etiqueta."""
        if self._marco and self._marco[0] == (an, al):
            return self._marco[1:]
        from PIL import Image, ImageDraw, ImageFont
        e = 4
        m = Image.new("L", (an * e, al * e), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, an * e - 1, al * e - 1), 26 * e, fill=255)
        mascara = np.asarray(m.resize((an, al), Image.LANCZOS), np.float32)[..., None] / 255
        b = Image.new("RGBA", (an * e, al * e), (0, 0, 0, 0))
        dib = ImageDraw.Draw(b)
        dib.rounded_rectangle((0, 0, an * e - 1, al * e - 1), 26 * e, outline=(125, 243, 225, 255), width=4 * e)
        fuente = next((f for f in _FUENTES if os.path.exists(f)), None)
        letra = ImageFont.truetype(fuente, 23 * e) if fuente else ImageFont.load_default()
        dib.rounded_rectangle((18 * e, 16 * e, 146 * e, 52 * e), 10 * e, fill=(10, 13, 22, 215))
        dib.ellipse((29 * e, 26 * e, 45 * e, 42 * e), fill=(255, 70, 90, 255))
        dib.text((54 * e, 19 * e), "TOKEN", font=letra, fill=(255, 255, 255, 255))
        borde = np.asarray(b.resize((an, al), Image.LANCZOS), np.float32)[..., [2, 1, 0, 3]]
        self._marco = ((an, al), mascara, borde)
        return mascara, borde

    def _ventana(self, img, v, t):
        c = self.clip(v["fuente"])
        fr = c.leer(t)
        if fr is None:
            return img
        sh, sw = fr.shape[:2]
        x, y, an, al = v["caja"]
        rec = fr[int(y * sh):int((y + al) * sh), int(x * sw):int((x + an) * sw)]
        cw = v["ancho"]
        ch = int(cw * rec.shape[0] / rec.shape[1])
        rec = cv2.resize(rec, (cw, ch), interpolation=cv2.INTER_AREA).astype(np.float32)
        mas, borde = self._marco_token(cw, ch)
        al_b = borde[..., 3:] / 255
        rec = rec * (1 - al_b) + borde[..., :3] * al_b
        u = min((t - v["de"]) / .28, (v["a"] - t) / .22, 1)        # entra y sale con rebote corto
        k = _rapido(max(0, u))
        mx = 34
        px = W - cw - mx if v["esq"][1] == "d" else mx
        py = mx if v["esq"][0] == "a" else H - ch - mx
        fuera = (cw + mx + 40) * (1 - k) * (1 if v["esq"][1] == "d" else -1)
        px = int(px + fuera)
        x0, x1 = max(0, px), min(W, px + cw)
        if x1 <= x0:
            return img
        sx0 = x0 - px
        reg = img[py:py + ch, x0:x1].astype(np.float32)
        a = mas[:, sx0:sx0 + (x1 - x0)]
        img[py:py + ch, x0:x1] = (rec[:, sx0:sx0 + (x1 - x0)] * a + reg * (1 - a)).astype(np.uint8)
        return img

    def _cuerpo_jefe(self, img, d, t):
        from jefe_canadiense import amplitud
        if d["amp"] is None:
            d["amp"] = amplitud(d["wav"], self.fps)
        i = min(len(d["amp"]) - 1, max(0, int((t - d["de"] - .12) * self.fps)))
        abre = float(d["amp"][i])
        c = self._jefe.cuadro(abre, t, alto=d["alto"])
        ch, cw = c.shape[:2]
        u = min((t - d["de"]) / .24, (d["a"] - t) / .2, 1)
        k = _rapido(max(0, u))
        salto = abs(math.sin((t - d["de"]) * 9)) * 16 * abre           # brinquitos al hablar
        px = W - cw + 40 if d["lado"] == "d" else -40
        py = int(H - ch + (ch * .75) * (1 - k) - salto + 8)
        y0, y1 = max(0, py), min(H, py + ch)
        if y1 <= y0:
            return img
        s = c[y0 - py:y1 - py]
        x0, x1 = max(0, px), min(W, px + cw)
        s = s[:, x0 - px:x1 - px]
        al = s[..., 3:].astype(np.float32) / 255
        reg = img[y0:y1, x0:x1].astype(np.float32)
        img[y0:y1, x0:x1] = (s[..., :3] * al + reg * (1 - al)).astype(np.uint8)
        return img

    def cuadro(self, t):
        img = self._base(t).copy()
        for f in self.encima:
            img = f(img, t)
        for v in self.ventanas:
            if v["de"] <= t < v["a"]:
                img = self._ventana(img, v, t)
        for d in self.jefes:
            if d["de"] <= t < d["a"]:
                img = self._cuerpo_jefe(img, d, t)
        return img

    def revisar(self):
        """Huecos, transición repetida dos veces seguidas y planos quietos demasiado largos."""
        malo = []
        for a, b in zip(self.planos, self.planos[1:]):
            if abs(a["a"] - b["de"]) > .02:
                malo.append(f"hueco {a['a']:.2f}->{b['de']:.2f}")
            if a["tr"][0] == b["tr"][0] and a["tr"][1] and b["tr"][1]:
                malo.append(f"transición repetida {b['tr'][0]} en {b['de']:.1f}")
        return malo

    def render(self, desde=0.0, hasta=None):
        os.makedirs(os.path.dirname(os.path.abspath(self.salida)), exist_ok=True)
        ff = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(self.fps), "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", str(self.crf), "-pix_fmt", "yuv420p", self.salida], stdin=subprocess.PIPE)
        fin = min(hasta or self.total, self.total)
        for n in range(int(desde * self.fps), int(fin * self.fps)):
            ff.stdin.write(self.cuadro(n / self.fps).tobytes())
        ff.stdin.close()
        ff.wait()
        return self.salida
