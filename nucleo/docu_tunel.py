# -*- coding: utf-8 -*-
"""TÚNEL DE CAPAS (el usuario, 4-nov-2026): cada toma es una LÁMINA en un espacio 3D; conforme avanza la narración se agregan capas
(pegatinas reales, fotos, camafeos, rótulos) delante de cada lámina y la cámara viaja por el túnel: casi siempre hacia el fondo, a veces
a un lado, arriba o abajo. Nada periódico: el movimiento sale de las posiciones de las capas.

Unidades: la lámina mide 1 de ancho; a distancia D0 = 1 ocupa el 86 % del ancho de pantalla.

Kit del documental de personaje antiguo (docs/estilo_docu_antiguo.md), nacido en videos/ramses_ii/ (ejemplo completo de uso:
`_capas()`, `render_mundo` y la captura de texto `con_texto`/`_TXT` de su escenas.py, para que ningún rótulo quede tapado por capas).
Uso: `import docu_tunel as TU; tun = TU.Tunel(laminas, capas, 1.4); img = tun.render(t, fondo)`; láminas como `(img, txt)` para
que el texto se pinte encima de todo. Cada video su propio recorrido por capítulo (regla del kit: `A.firma` única)."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import docu as D
import docu_antiguo as A
from motor import W, H, e_inout, e_out, lerp, prog, smooth

D0 = 1.0
ESC = 0.86 * W                      # px por unidad a distancia 1
ASP = H / W                         # alto de la lámina en unidades


def proyectar(cam, x, y, z):
    d = z - cam[2]
    if d <= 0.02:
        return None
    k = ESC / d
    return W / 2 + (x - cam[0]) * k, H / 2 + (y - cam[1]) * k, d, k


def _pegar_escalado(lz, rgb, a, cx, cy, ancho_px, op, rot=0.0, aditivo=False):
    """Pega una imagen (rgb float premultiplicada o no y alfa) centrada en (cx, cy) con ancho `ancho_px`."""
    h, w = a.shape
    s = ancho_px / w
    if s * w < 4 or op <= 0.005:
        return
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, s)
    M[:, 2] += (cx - w / 2, cy - h / 2)
    x0, y0 = int(max(0, cx - w * s * 0.75)), int(max(0, cy - h * s * 0.75))
    x1, y1 = int(min(W, cx + w * s * 0.75)), int(min(H, cy + h * s * 0.75))
    if x1 <= x0 or y1 <= y0:
        return
    M[:, 2] -= (x0, y0)
    sz = (x1 - x0, y1 - y0)
    aw = cv2.warpAffine(a, M, sz, flags=cv2.INTER_LINEAR, borderValue=0) * op
    cw = cv2.warpAffine(rgb, M, sz, flags=cv2.INTER_LINEAR, borderValue=0)
    dst = lz[y0:y1, x0:x1]
    if aditivo:
        sh = cv2.GaussianBlur(aw, (0, 0), max(2.0, ancho_px * 0.012)) * 0.75
        dst *= (1 - np.clip(sh, 0, 1)[..., None])
        dst += cw * op
    else:
        dst *= (1 - aw[..., None])
        dst += cw * aw[..., None]


def _pegar_texto(lz, txt, cx, cy, ancho_px, op):
    """Capa de TEXTO de una lámina (cuadro completo, negro donde no hay letra) encima de todo: sombra suave + máximo de color."""
    if op <= 0.01:
        return
    s = ancho_px / W
    M = np.float32([[s, 0, cx - W * s / 2], [0, s, cy - H * s / 2]])
    tw = cv2.warpAffine(txt, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
    a = np.clip(tw.max(-1) * 1.6, 0, 1)
    if a.max() < 0.02:
        return
    sh = np.clip(cv2.GaussianBlur(a, (0, 0), max(3.0, 7 * s)) * 1.4, 0, 1) * 0.72 * op
    lz *= (1 - sh[..., None])
    np.maximum(lz, tw * op, out=lz)


# ------------------------------------------------------------------ sprites de las capas (en caché)
@functools.lru_cache(maxsize=64)
def spr_png(ruta, alto=700):
    im = Image.open(ruta).convert("RGBA")
    caja = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    if caja:
        im = im.crop(caja)
    k = alto / im.height
    im = im.resize((max(1, int(im.width * k)), alto), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy(), False


@functools.lru_cache(maxsize=64)
def spr_foto(ruta, ancho=760, foco=(0.5, 0.5), aspecto=0.68):
    rgb = cv2.cvtColor(cv2.imread(ruta), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    h, w = rgb.shape[:2]
    hh = int(min(h, w * aspecto)); ww = int(hh / aspecto)
    x0 = int(np.clip(foco[0] * w - ww / 2, 0, w - ww)); y0 = int(np.clip(foco[1] * h - hh / 2, 0, h - hh))
    im = cv2.resize(rgb[y0:y0 + hh, x0:x0 + ww], (ancho, int(ancho * aspecto)), interpolation=cv2.INTER_AREA)
    b = 10
    im[:b] = im[-b:] = 0.92; im[:, :b] = im[:, -b:] = 0.92            # marco claro fino
    return im * 0.92, np.ones(im.shape[:2], np.float32), False


@functools.lru_cache(maxsize=64)
def spr_camafeo(ruta, foco=(0.5, 0.4), zoom=1.0, r=220):
    rec, a, aro = A._camafeo_spr(ruta, r, foco[0], foco[1], zoom)
    rgb = rec.astype(np.float32) / 255.0 * a[..., None]
    g = np.clip(cv2.GaussianBlur(aro, (0, 0), 6) * 1.2 + aro, 0, 1)
    rgb = rgb * (1 - g[..., None]) + g[..., None] * 0.97
    return rgb, np.clip(a + g, 0, 1), False


@functools.lru_cache(maxsize=64)
def spr_texto(partes, px=90, cursiva=False):
    """partes = (("TEXTO ", "b"), ("ROJO", "r")): versales serif (o cursiva Poppins) con brillo; capa ADITIVA."""
    fnt = A._fuente("sans_i" if cursiva else "serif", px)
    txt = "".join(p for p, _ in partes)
    ancho = int(sum(fnt.getlength(c) + px * 0.06 for c in txt)) + px
    im = Image.new("RGB", (ancho, int(px * 1.8)), (0, 0, 0))
    d = ImageDraw.Draw(im)
    x = px * 0.5
    for p, c in partes:
        col = (250, 245, 236) if c == "b" else (235, 25, 30)
        for ch in p:
            d.text((x, px * 0.3), ch, font=fnt, fill=col)
            x += fnt.getlength(ch) + px * 0.06
    base = np.asarray(im).astype(np.float32) / 255.0
    glow = cv2.GaussianBlur(base, (0, 0), px * 0.22) * 0.9
    rgb = np.clip(base + glow, 0, 1.4)
    return rgb, np.clip(rgb.max(-1), 0, 1), True


# ------------------------------------------------------------------ el túnel
class Tunel:
    def __init__(self, laminas, capas, viajes):
        """laminas: [(t0, fn, (x, y, z))] (fn(t, ta, tb) -> imagen H×W×3); capas: [(t_alta, lamina_i, (dx, dy, zr), alto, sprite, anim)];
        viajes: duración del viaje entre láminas."""
        self.L = laminas
        self.C = capas
        self.viaje = viajes
        self._txt = {}
        self.txt_desde = 1e9                                            # desde qué instante los rótulos sueltos caducan
        self.txt_dura = 5.0

    def _i(self, t):
        return max(k for k, l in enumerate(self.L) if l[0] <= t)

    def camara(self, t):
        i = self._i(t)

        def vista(k, tt):
            x, y, z = self.L[k][2]
            tb = self.L[k + 1][0] if k + 1 < len(self.L) else self.L[k][0] + 20
            av = 0.10 * smooth(prog(tt, self.L[k][0], tb))             # deriva lenta hacia la lámina (no periódica)
            return np.array([x, y, z - D0 + av])
        c = vista(i, t)
        if i + 1 < len(self.L):
            tb = self.L[i + 1][0]
            u = prog(t, tb - self.viaje * 0.45, tb + self.viaje * 0.55)
            if u > 0:
                c2 = vista(i + 1, t)
                s = e_inout(u)
                c = c + (c2 - c) * s
                c[2] -= 0.35 * math.sin(math.pi * s)                    # se aleja un poco a mitad del viaje: se ven las capas
        if i > 0:
            ta = self.L[i][0]
            u = prog(t, ta - self.viaje * 0.45, ta + self.viaje * 0.55)
            if u < 1:
                c1 = vista(i - 1, t)
                s = e_inout(u)
                c = c1 + (c - c1) * s
                c[2] -= 0.35 * math.sin(math.pi * s)
        return c

    def render(self, t, fondo):
        """Del fondo hacia la cámara; al final, ENCIMA de todo, el texto de la lámina que se narra y los rótulos sueltos
        (el usuario, 4-nov-2026: «que los textos se vean cuando hay varias capas»)."""
        cam = self.camara(t)
        lz = fondo.copy()
        i = self._i(t)
        self._txt = {}
        objs = []
        for k in range(max(0, i - 2), min(len(self.L), i + 2)):
            t0, fn, (x, y, z) = self.L[k]
            if k > i and t < t0 - 1.6:
                continue
            objs.append((z, "L", k))
            self._marco(lz, cam, x, y, z)
        for j, cp in enumerate(self.C):
            if cp[0] <= t and abs(cp[1] - i) <= 1:
                x, y, z = self.L[cp[1]][2]
                objs.append((z - D0 * cp[2][2], "C", j))
        textos = []
        for z, tipo, k in sorted(objs, key=lambda o: -o[0]):             # del fondo hacia la cámara
            if tipo == "L":
                self._lamina(lz, cam, t, k)
            elif self.C[k][4][2]:
                textos.append(k)                                         # rótulos sueltos: al final
            else:
                self._capa(lz, cam, t, k)
        if i in self._txt:
            txt, cx, cy, kk, op = self._txt[i]
            _pegar_texto(lz, txt, cx, cy, kk, op)
        for k in textos:
            self._capa(lz, cam, t, k)
        return lz

    def _marco(self, lz, cam, x, y, z):
        """Marcos tenues del túnel alrededor de cada lámina (dan profundidad)."""
        for dz, esc, op in ((0.0, 1.18, 0.18), (-0.45, 1.5, 0.10)):
            p = proyectar(cam, x, y, z + dz)
            if p is None:
                continue
            cx, cy, d, k = p
            hw, hh = 0.5 * esc * k, 0.5 * ASP * esc * k
            o = op * float(np.clip((d - 0.15) / 0.3, 0, 1)) * math.exp(-max(0.0, d - 1.2) * 0.6)
            if o > 0.01 and hw < W * 3:
                cv2.rectangle(lz, (int(cx - hw), int(cy - hh)), (int(cx + hw), int(cy + hh)), (o, o * 0.95, o * 0.9), 2, cv2.LINE_AA)

    def _lamina(self, lz, cam, t, k):
        t0, fn, (x, y, z) = self.L[k]
        p = proyectar(cam, x, y, z)
        if p is None:
            return
        cx, cy, d, kk = p
        op = float(np.clip((d - 0.28) / 0.30, 0, 1)) * smooth(prog(t, t0 - 1.6, t0 - 0.4) if t < t0 else 1.0)
        if op <= 0.01 or kk > W * 3:
            return
        tb = self.L[k + 1][0] if k + 1 < len(self.L) else t0 + 30
        res = fn(t, t0, tb)
        txt = None
        if isinstance(res, tuple):
            res, txt = res
        img = np.clip(res, 0, 1.5)
        niebla = math.exp(-max(0.0, d - D0) * 0.55)
        if txt is not None:
            self._txt[k] = (np.clip(txt, 0, 1.5) * niebla, cx, cy, kk, op)
        img = img * niebla
        g = np.zeros((H, W), np.float32)                                # aro claro fino
        g[:4] = g[-4:] = 1; g[:, :4] = g[:, -4:] = 1
        img = img + g[..., None] * 0.35 * niebla
        _pegar_escalado(lz, img, np.ones((H, W), np.float32), cx, cy, kk, op)

    def _capa(self, lz, cam, t, j):
        t_alta, li, (dx, dy, zr), alto, spr, anim = self.C[j]
        x, y, z = self.L[li][2]
        zc = z - D0 * zr
        u = e_out(prog(t, t_alta, t_alta + 0.7))
        dt = t - t_alta
        ox, oy, rot = 0.0, 0.0, 0.0
        if anim == "sube":
            oy = (1 - u) * 0.25
        elif anim == "izq":
            ox = -(1 - u) * 0.5
        elif anim == "der":
            ox = (1 - u) * 0.5
        elif anim == "gira":
            rot = (1 - u) * 25
        rot += 1.5 * math.sin(dt * 0.4 + j)
        oy += 0.012 * math.sin(dt * 0.7 + j * 1.7)
        dv = D0 * (1 - zr)                                              # distancia a la vista de su lámina
        wx, wy = dx * (W / 2 / ESC) * dv, dy * (H / 2 / ESC) * dv        # dx, dy = fracción de media pantalla vista desde ahí
        p = proyectar(cam, x + wx + ox * dv, y + wy + oy * dv, zc)
        if p is None:
            return
        cx, cy, d, kk = p
        rgb, a, aditivo = spr
        ancho = alto * dv * kk * (a.shape[1] / a.shape[0])           # alto = fracción del alto de pantalla vista desde su lámina
        ancho *= H / ESC
        alto_px = ancho * a.shape[0] / a.shape[1]
        k_cl = float(np.clip((d - 0.25) / 0.2, 0, 1))                  # dentro del cuadro (salvo cuando la cámara la atraviesa)
        mx, my = W * 0.035 + ancho * 0.5, H * 0.05 + alto_px * 0.5
        if ancho < W * 0.9:
            cx = cx + (float(np.clip(cx, mx, W - mx)) - cx) * k_cl
        if alto_px < H * 0.9:
            cy = cy + (float(np.clip(cy, my, H - my)) - cy) * k_cl
        esc = 0.85 + 0.15 * u
        op = u * float(np.clip((d - 0.06) / 0.18, 0, 1))
        if aditivo and t_alta >= self.txt_desde:                         # rótulos sueltos: se van a los 5 s (no se apilan con los de la lámina)
            op *= 1 - smooth(prog(dt, self.txt_dura, self.txt_dura + 0.8))
        _pegar_escalado(lz, rgb, a, cx, cy, ancho * esc, op, rot=rot, aditivo=aditivo)
