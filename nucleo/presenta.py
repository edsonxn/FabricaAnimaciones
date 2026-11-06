# -*- coding: utf-8 -*-
"""PRESENTACIONES DE VARIAS IMÁGENES A LA VEZ (el usuario, 5-nov-2026, TODOS los canales: «nuevas formas de presentar
pegatinas, imágenes y mapas»). Complementa a `peg_anim` (una pegatina sola) cuando la voz compara, ordena o enumera.

Todas devuelven fn(dt, dur, marcas) -> BGRA 1920x1080 con fondo TRANSPARENTE (el clip sigue debajo): FX `mg` con x=.5, y=.5
(o `pantalla`). Las imágenes se visten con los marcos de peg_anim (polaroid, carta, museo, naipe, pergamino, vitral…) y con
los colores del canal (peg_estilos.TEMAS: tes wow er gaming spyro n64 pokemon cod plasti). Una `marca` de la voz por imagen.
  tierlist(items, filas)        tabla S/A/B/C/D: cada retrato sale GRANDE al centro con su nombre y vuela a su fila
  carrusel(fotos)               anillo 3D de cartas que gira para traer al frente la que la voz nombra
  tablero(fotos, hilos)         tablero de corcho de investigación: fotos clavadas y el hilo rojo que las une
  versus(a, b, ganador)         pantalla partida en diagonal, cada lado entra de golpe, rayo y «VS»; el perdedor se apaga
  podio(tres)                   podio 3.º → 2.º → 1.º que sube del suelo, cartas que caen encima y rayos de luz al ganador
  muro(fotos, destaca)          muro de fichas que se voltean una a una (3D); `destaca` saca una al frente al final
Hoja de prueba (MÍRALA): python nucleo/presenta.py hoja [--tema tes] [--img a.png b.png …] [--salida previews]
Uso en efectos.py: helpers `tier()`, `carr()`, `tabl()`, `vs()`, `podi()`, `muro()` de videos/_plantilla_yt/efectos.py.
"""
import math
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import mg_tes as T
import peg_anim as PA
import peg_estilos as PE

W, H = 1920, 1080


def _col(tema):
    return PE.TEMAS.get(tema, PE.TEMAS["tes"])


def _c(u):
    return max(0.0, min(1.0, u))


def _eo(u):
    u = _c(u)
    return 1 - (1 - u) ** 3


def _eio(u):
    u = _c(u)
    return u * u * (3 - 2 * u)


def _back(u, k=1.7):
    u = _c(u)
    return 1 + (k + 1) * (u - 1) ** 3 + k * (u - 1) ** 2


def _marcas(marcas, n, dur, ini=.35, fin=1.6):
    mk = list(marcas)[:n]
    while len(mk) < n:
        a = mk[-1] + .9 if mk else ini
        resto = n - len(mk)
        paso = max(.5, (dur - fin - a) / max(1, resto))
        mk += [a + paso * j for j in range(resto)]
    return mk


# ----------------------------------------------------------------------------------------------------------- lienzo 2D
class _L2:
    """Lienzo BGRA premultiplicado float32 (operador «over»), con sprites que escalan y giran."""

    def __init__(self, w=W, h=H):
        self.f = np.zeros((h, w, 4), np.float32)
        self.w, self.h = w, h

    def pon(self, spr, cx, cy, a=1.0, esc=1.0, rot=0.0, luz=1.0):
        if a <= .003 or esc <= .01:
            return
        h, w = spr.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, esc)
        M[:, 2] += (cx - w / 2, cy - h / 2)
        c = np.array([[0, 0, 1], [w, 0, 1], [w, h, 1], [0, h, 1]], float) @ M.T
        x0, y0 = int(max(0, math.floor(c[:, 0].min()))), int(max(0, math.floor(c[:, 1].min())))
        x1, y1 = int(min(self.w, math.ceil(c[:, 0].max()) + 1)), int(min(self.h, math.ceil(c[:, 1].max()) + 1))
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        M[:, 2] -= (x0, y0)
        o = cv2.warpAffine(spr, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        if luz != 1:
            o[..., :3] *= luz
        r = self.f[y0:y1, x0:x1]
        r *= 1 - o[..., 3:4] * a
        r += o * a

    def linea(self, pts, color, grosor, a=1.0):
        if a <= .003 or len(pts) < 2:
            return
        capa = np.zeros((self.h, self.w), np.uint8)
        cv2.polylines(capa, [np.round(np.asarray(pts) * 4).astype(np.int32)], False, 255, grosor, cv2.LINE_AA, 2)
        m = capa.astype(np.float32)[..., None] * (a / 255)
        col = np.float32([color[2], color[1], color[0], 255]) / 255
        self.f *= 1 - m
        self.f += m * col

    def salida(self):
        return PA._u8_recto(self.f)


def _pil(img):
    return PA._prem(img)


def _texto(s, tam, color, borde=(0, 0, 0), ancho_borde=None, fuente="Bold Condensed"):
    f = T.fuente(fuente, tam)
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    sb = ancho_borde if ancho_borde is not None else max(2, tam // 14)
    bb = d0.textbbox((0, 0), s, font=f, stroke_width=sb)
    im = Image.new("RGBA", (bb[2] - bb[0] + 12, bb[3] - bb[1] + 12), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((6 - bb[0], 6 - bb[1]), s, font=f, fill=tuple(color) + (255,), stroke_width=sb,
                            stroke_fill=tuple(borde) + (255,))
    return _pil(im)


def _pildora(s, tam, tema, fondo=(14, 12, 11)):
    t = _col(tema)
    f = T.fuente("Bold Condensed", tam)
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    tw = d0.textlength(s, font=f)
    w, h = int(tw + tam * 1.4), int(tam * 1.55)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w + 3, h + 3), radius=h // 2, fill=fondo + (235,), outline=t["luz"] + (255,), width=3)
    d.text(((w + 8) / 2, (h + 8) / 2), s, font=f, fill=t["texto"] + (255,), anchor="mm")
    return _pil(im)


def _sombra(spr, rad=14, fuerza=.6):
    h, w = spr.shape[:2]
    P = int(rad * 2)
    al = np.zeros((h + 2 * P, w + 2 * P), np.float32)
    al[P:P + h, P:P + w] = spr[..., 3]
    al = cv2.GaussianBlur(al, (0, 0), rad / 2) * fuerza
    return np.dstack([np.zeros_like(al)] * 3 + [al])


def _carta(ruta, nombre, tam, tema, marco):
    im, rec = PA._abre(ruta)
    m = marco if (marco != "aura" or rec) else "polaroid"
    c = PA.MARCOS[m](im, rec, nombre, tam, tema)
    return _pil(c.img), (_pil(c.dorso) if c.dorso is not None else None)


def _retrato(ruta, lado, tema, radio=14, borde=5):
    t = _col(tema)
    im, rec = PA._abre(ruta)
    base = PA._llena(im, rec, lado, lado, tema, foco=(.5, .3)).convert("RGBA")
    out = Image.new("RGBA", (lado + 2 * borde, lado + 2 * borde), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((0, 0, lado + 2 * borde - 1, lado + 2 * borde - 1), radius=radio + borde, fill=t["luz"] + (255,))
    m = Image.new("L", (lado, lado), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, lado - 1, lado - 1), radius=radio, fill=255)
    out.paste(base, (borde, borde), m)
    return _pil(out)


def _perezoso(prep, dibuja):
    est = {}

    def fn(dt, dur, marcas=()):
        if not est:
            est.update(prep())
        return dibuja(est, dt, dur, marcas)
    return fn


# ----------------------------------------------------------------------------------------------------------- tier list
TIER_COLORES = {"S": (232, 84, 84), "A": (240, 150, 70), "B": (236, 206, 90), "C": (120, 196, 110), "D": (100, 150, 230),
                "E": (150, 120, 210), "F": (130, 130, 130)}


def tierlist(items, filas=("S", "A", "B", "C", "D"), titulo=None, tema="tes", ancho=1640, colores=None):
    """items = [(ruta, nombre, fila)] en el orden en que la voz los nombra (fila = letra o índice). Cada uno sale grande al
    centro con su nombre (~1 s) y vuela a su hueco en la fila. Marcas: una por item."""
    colores = dict(TIER_COLORES, **(colores or {}))
    n = len(filas)

    def prep():
        t = _col(tema)
        y0 = 150 if titulo else 70
        rh = int((H - y0 - 50) / n)
        x0 = (W - ancho) // 2
        lab = int(rh * 1.15)
        tab = Image.new("RGBA", (ancho + 40, n * rh + 40), (0, 0, 0, 0))
        sh = Image.new("L", tab.size, 0)
        ImageDraw.Draw(sh).rounded_rectangle((26, 30, ancho + 26, n * rh + 30), radius=18, fill=170)
        tab.paste((0, 0, 0, 255), mask=sh.filter(ImageFilter.GaussianBlur(12)))
        d = ImageDraw.Draw(tab)
        d.rounded_rectangle((14, 14, ancho + 14, n * rh + 14), radius=16, fill=(16, 14, 13, 225), outline=t["luz"] + (255,), width=3)
        f = T.fuente("Bold Condensed", int(rh * .5))
        for i, fl in enumerate(filas):
            y = 14 + i * rh
            col = colores.get(str(fl), t["luz"])
            d.rounded_rectangle((20, y + 6, 14 + lab, y + rh - 6), radius=10, fill=col + (255,))
            d.text((17 + lab / 2, y + rh / 2), str(fl), font=f, fill=(20, 18, 16, 255), anchor="mm")
            if i:
                d.line((14 + lab + 8, y, ancho + 6, y), fill=t["luz"] + (70,), width=2)
        slot = int(rh * .84)
        big = 380
        its = []
        cuenta = [0] * n
        for ruta, nombre, fl in items:
            fi = filas.index(fl) if fl in filas else int(fl)
            k = cuenta[fi]
            cuenta[fi] += 1
            sx = x0 + 14 + lab + 18 + k * (slot + 14) + slot / 2
            sy = y0 + 14 + fi * rh + rh / 2
            r = _retrato(ruta, big, tema)
            its.append(dict(r=r, sombra=_sombra(r, 20), pil=_pildora(nombre.upper(), 46, tema), slot=(sx, sy),
                            esc=(slot + 10) / r.shape[0]))
        tt = _texto(titulo.upper(), 74, t["luz"]) if titulo else None
        return dict(tab=_pil(tab), x0=x0, y0=y0, its=its, tt=tt)

    def dibuja(e, dt, dur, marcas):
        L = _L2()
        mk = _marcas(marcas, len(e["its"]), dur, .7)
        ent = _eo(dt / .55)
        sal = 1 - _eio((dt - (dur - .45)) / .45)
        a = ent * sal
        tab = e["tab"]
        L.pon(tab, W / 2, e["y0"] - 14 + tab.shape[0] / 2 + (1 - ent) * 80 + (1 - sal) * 60, a)
        if e["tt"] is not None:
            L.pon(e["tt"], W / 2, 70, a, .9 + .1 * ent)
        grande = None
        for k, it in enumerate(e["its"]):
            u = dt - mk[k]
            if u < 0:
                continue
            sx, sy = it["slot"]
            if u < .95:                                     # presentación: grande al centro con su nombre
                g = _back(u / .45, 1.4)
                grande = (it, W / 2, H * .46, .25 + .75 * g, _c(u / .2), 1.0, math.sin(u * 4) * 2)
            else:
                v = _eio((u - .95) / .55)
                x = W / 2 + (sx - W / 2) * v
                y = H * .46 + (sy - H * .46) * v - math.sin(math.pi * v) * 120
                s = 1 + (it["esc"] - 1) * v
                if v < 1:
                    grande = (it, x, y, s, 1.0, 1 - v, (1 - v) * 3)
                else:
                    L.pon(it["sombra"], sx + 4, sy + 6, a * .7, it["esc"])
                    L.pon(it["r"], sx, sy + 2 * math.sin(dt * 1.8 + k), a, it["esc"])
        if grande:
            it, x, y, s, al, ap, rot = grande
            L.pon(it["sombra"], x + 14 * s, y + 22 * s, al * a * .8, s, rot)
            L.pon(it["r"], x, y, al * a, s, rot)
            if ap > .02:
                L.pon(it["pil"], x, y + it["r"].shape[0] * s / 2 + 40, ap * al * a, min(1, s))
        return L.salida()
    return _perezoso(prep, dibuja)


# ----------------------------------------------------------------------------------------------------------- carrusel 3D
class _L3(PA._Lienzo):
    def __init__(self):
        self._lienzo(W, H)

    def cuadro(self):
        o = self._bgra()
        y = (self.CH - H) // 2
        return np.ascontiguousarray(o[y:y + H, :W])


def carrusel(fotos, tam=440, tema="tes", marco="carta", radio=None, titulo=None, y=0):
    """fotos = [(ruta, nombre)]: anillo 3D de cartas; con cada marca gira y trae al frente la siguiente (la 1.ª marca =
    la primera foto). El frente se ilumina; las de atrás quedan en penumbra."""
    n = len(fotos)

    def prep():
        cs = []
        for ruta, nombre in fotos:
            p, _ = _carta(ruta, nombre, tam, tema, marco)
            cs.append((PA._u8_recto(p, PA._sangra(p)), p.shape[1], p.shape[0]))
        t = _col(tema)
        return dict(cs=cs, R=radio or tam * .62 * max(2.2, n / 2.2), tt=_texto(titulo.upper(), 70, t["luz"]) if titulo else None)

    def dibuja(e, dt, dur, marcas):
        mk = _marcas(marcas, n, dur, .9)
        cur = -n * .5 * (1 - _eo(dt / 1.3))
        for k in range(1, n):
            cur += _eio((dt - mk[k]) / .75)
        sal = 1 - _eio((dt - (dur - .5)) / .5)
        cur += (1 - sal) * 1.2
        L = _L3()
        L._limpia()
        R = e["R"]
        orden = []
        for i, (u8, w, h) in enumerate(e["cs"]):
            th = (i - cur) * 2 * math.pi / n
            z = R * (1 - math.cos(th))
            orden.append((z, i, th, u8, w, h))
        for z, i, th, u8, w, h in sorted(orden, reverse=True):
            cth = math.cos(th)
            frente = max(0.0, cth) ** 6
            pose = PA._pose(x=R * math.sin(th) * 1.05, y=y - 18 * frente + 6 * math.sin(dt * 1.4 + i), z=z * 1.3,
                            ry=-math.degrees(th) * .85, s=(1 + .14 * frente) * (.9 + .1 * sal), a=_c((cth + .55) / .4) * sal * _eo(dt / .4))
            L.dibuja(u8, PA._quad(w, h), pose, w, h, a=pose["a"], luz=.38 + .62 * max(0.0, cth) ** 1.5)
        out = L.cuadro()
        if e["tt"] is not None:
            L2 = _L2()
            L2.f = PA._prem(Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGRA2RGBA)))
            L2.pon(e["tt"], W / 2, 80, sal * _eo(dt / .5))
            return L2.salida()
        return out
    return _perezoso(prep, dibuja)


# ----------------------------------------------------------------------------------------------------------- tablero de corcho
def _corcho(w, h, tema, semilla=4):
    rng = np.random.default_rng(semilla)
    base = np.float32((150, 106, 66))
    n = PA._ruido(h, w, 3, semilla) * .6 + PA._ruido(h, w, 17, semilla + 1) * .4
    a = base[None, None, :] * (.72 + .5 * n[..., None])
    pts = rng.random((int(w * h / 180), 2)) * [w, h]
    for x, y in pts[: int(len(pts) * .6)]:
        a[int(y) % h, int(x) % w] *= .55
    a = cv2.GaussianBlur(a, (0, 0), .6)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2))
    a *= (1 - .3 * np.clip(r - .5, 0, 1))[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    out = Image.new("RGBA", (w + 56, h + 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    madera = tuple(int(v * .5) for v in _col(tema)["tinta"])
    d.rounded_rectangle((0, 0, w + 55, h + 55), radius=10, fill=madera + (255,))
    d.rounded_rectangle((6, 6, w + 49, h + 49), radius=8, outline=tuple(min(255, int(v * 1.8)) for v in madera) + (255,), width=3)
    out.alpha_composite(im, (28, 28))
    return out


def _chincheta(color, r=13):
    im = Image.new("RGBA", (r * 4, r * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sh = Image.new("L", im.size, 0)
    ImageDraw.Draw(sh).ellipse((r + 4, r + 7, 3 * r + 4, 3 * r + 7), fill=160)
    im.paste((0, 0, 0, 255), mask=sh.filter(ImageFilter.GaussianBlur(4)))
    d.ellipse((r, r, 3 * r, 3 * r), fill=tuple(color) + (255,), outline=tuple(int(c * .5) for c in color) + (255,), width=2)
    d.ellipse((r * 1.5, r * 1.4, r * 2.1, r * 2.0), fill=(255, 255, 255, 190))
    return _pil(im)


def tablero(fotos, hilos=(), titulo=None, tema="tes", tam=300, marco="polaroid", posiciones=None, ancho=1700, alto=900):
    """Tablero de investigación: fotos = [(ruta, nombre)] que se clavan una por marca; hilos = [(i, j)] hilo rojo entre la
    foto i y la j (se tiende cuando ya están las dos). posiciones = [(x, y)] en fracción del tablero (si no, rejilla con azar)."""
    n = len(fotos)

    def prep():
        t = _col(tema)
        tab = _pil(_corcho(ancho, alto, tema))
        rng = random.Random(n * 13 + 5)
        if posiciones:
            pos = list(posiciones)
        else:
            cols = max(2, math.ceil(math.sqrt(n * 1.7)))
            filas = math.ceil(n / cols)
            pos = [((c + .5) / cols + rng.uniform(-.04, .04), (f + .5) / filas + rng.uniform(-.05, .05))
                   for f in range(filas) for c in range(cols)][:n]
        x0, y0 = W / 2 - ancho / 2, H / 2 - alto / 2 + (30 if titulo else 0)
        cs = []
        for k, (ruta, nombre) in enumerate(fotos):
            p, _ = _carta(ruta, nombre, tam, tema, marco)
            cx, cy = x0 + pos[k][0] * ancho, y0 + pos[k][1] * alto
            cs.append(dict(p=p, s=_sombra(p, 12, .55), x=cx, y=cy, rot=rng.uniform(-8, 8), pin=(cx, cy - p.shape[0] / 2 + 26)))
        tt = None
        if titulo:
            nota = Image.new("RGBA", (int(len(titulo) * 34 + 120), 104), (0, 0, 0, 0))
            d = ImageDraw.Draw(nota)
            d.rectangle((6, 6, nota.width - 6, nota.height - 6), fill=t["papel"] + (255,))
            d.text((nota.width / 2, nota.height / 2), titulo.upper(), font=T.fuente("Bold Condensed", 60), fill=t["tinta"] + (255,), anchor="mm")
            tt = _pil(nota)
        return dict(tab=tab, cs=cs, pin=_chincheta(t["rojo"]), tt=tt, rojo=t["rojo"], y0=y0)

    def dibuja(e, dt, dur, marcas):
        mk = _marcas(marcas, n, dur, .6)
        ent = _eo(dt / .5)
        sal = 1 - _eio((dt - (dur - .45)) / .45)
        a = ent * sal
        L = _L2()
        esc = .97 + .03 * min(1, dt / max(1, dur))
        L.pon(e["tab"], W / 2, H / 2 + (30 if e["tt"] is not None else 0) + (1 - ent) * 60, a, esc)
        for k, c in enumerate(e["cs"]):
            u = dt - mk[k]
            if u < 0:
                continue
            v = _eo(u / .35)
            s = 1.25 - .25 * v
            rot = c["rot"] + .6 * math.sin(dt * 1.3 + k)
            L.pon(c["s"], c["x"] + 8 + 30 * (1 - v), c["y"] + 12 + 40 * (1 - v), a * v, s, rot)
            L.pon(c["p"], c["x"], c["y"], a * _c(u / .15), s, rot)
        for i, j in hilos:
            if i >= n or j >= n:
                continue
            u = dt - max(mk[i], mk[j]) - .4
            if u < 0:
                continue
            v = _eio(u / .5)
            p0, p1 = np.array(e["cs"][i]["pin"]), np.array(e["cs"][j]["pin"])
            d = np.linalg.norm(p1 - p0)
            ts = np.linspace(0, v, 24)
            pts = p0[None] + (p1 - p0)[None] * ts[:, None]
            pts[:, 1] += np.sin(np.pi * ts) * d * .06
            L.linea(pts + [3, 5], (0, 0, 0), 5, .35 * a)
            L.linea(pts, e["rojo"], 4, a)
        for k, c in enumerate(e["cs"]):
            u = dt - mk[k] - .2
            if u >= 0:
                L.pon(e["pin"], c["pin"][0], c["pin"][1], a, .6 + .4 * _back(u / .25))
        if e["tt"] is not None:
            L.pon(e["tt"], W / 2, e["y0"] - 20, a, 1, -2)
            L.pon(e["pin"], W / 2, e["y0"] - 60, a)
        return L.salida()
    return _perezoso(prep, dibuja)


# ----------------------------------------------------------------------------------------------------------- versus
def versus(a, b, ganador=None, tema="tes", titulo=None, foco_a=(.5, .3), foco_b=(.5, .3)):
    """Pantalla partida en diagonal: a = (ruta, nombre) entra por la izquierda, b por la derecha; «VS» con rayo en la
    costura. marcas: [a, b] y, si hay ganador (0 = a, 1 = b), una 3.ª: el perdedor se apaga a gris y el ganador brilla."""
    def prep():
        t = _col(tema)
        capas = []
        for k, (ruta, nombre) in enumerate((a, b)):
            im, rec = PA._abre(ruta)
            foto = PA._llena(im, rec, int(W * .62), H, tema, foco=foco_a if k == 0 else foco_b).convert("RGBA")
            lien = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lien.paste(foto, (0 if k == 0 else W - foto.width, 0))
            m = Image.new("L", (W, H), 0)
            poly = [(0, 0), (W * .565, 0), (W * .435, H), (0, H)] if k == 0 else [(W * .565, 0), (W, 0), (W, H), (W * .435, H)]
            ImageDraw.Draw(m).polygon(poly, fill=255)
            lien.putalpha(m.filter(ImageFilter.GaussianBlur(1)))
            p = _pil(lien)
            g = p.copy()
            g[..., :3] = g[..., :3].mean(2, keepdims=True) * .42
            capas.append(dict(p=p, g=g, pil=_pildora(nombre.upper(), 58, tema), lado=-1 if k == 0 else 1))
        vs = _texto("VS", 260, t["luz"], (10, 8, 6), 12)
        return dict(capas=capas, vs=vs, luz=t["luz"], tt=_texto(titulo.upper(), 64, t["texto"]) if titulo else None)

    def dibuja(e, dt, dur, marcas):
        mk = _marcas(marcas, 3 if ganador is not None else 2, dur, .2)
        sal = 1 - _eio((dt - (dur - .45)) / .45)
        L = _L2()
        ambos = dt - mk[1]
        temblor = (math.sin(dt * 90) * 9 * max(0.0, 1 - ambos / .3)) if ambos > 0 else 0
        for k, c in enumerate(e["capas"]):
            u = dt - mk[k]
            if u < 0:
                continue
            v = _back(u / .42, 1.2)
            off = c["lado"] * W * .62 * (1 - v) + c["lado"] * W * .62 * (1 - sal)
            gana = ganador is not None and dt > mk[2]
            if gana and ganador != k:
                w_ = _eio((dt - mk[2]) / .5)
                L.pon(c["p"], W / 2 + off + temblor, H / 2, 1 - w_)
                L.pon(c["g"], W / 2 + off + temblor, H / 2, w_)
            else:
                lz = 1.0
                if gana:
                    lz = 1 + .12 * _eio((dt - mk[2]) / .5) * (.8 + .2 * math.sin(dt * 5))
                L.pon(c["p"], W / 2 + off + temblor, H / 2, 1.0, 1.0, 0, lz)
            px = W * (.22 if k == 0 else .78) + off
            ep = _back((u - .25) / .35)
            if ep > 0:
                esc = 1.0 + (.18 if (ganador == k and dt > mk[2]) else 0) * _eio((dt - mk[2]) / .4) if ganador is not None else 1.0
                L.pon(c["pil"], px, H - 110, _c(ep * 2), ep * esc)
        if ambos > 0:                                         # rayo en la costura + VS
            rng = np.random.default_rng(int(dt * 14))
            ys = np.linspace(-20, H + 20, 18)
            xs = W * .565 + (W * .435 - W * .565) * (ys / H) + rng.uniform(-16, 16, len(ys))
            pts = np.stack([xs, ys], 1)
            ap = _c(ambos / .15) * sal
            L.linea(pts, (0, 0, 0), 16, .45 * ap)
            L.linea(pts, e["luz"], 8, ap)
            L.linea(pts, (255, 255, 255), 3, ap)
            v = _back((ambos - .1) / .4, 2.2)
            L.pon(e["vs"], W / 2, H / 2, _c(v * 3) * sal, .2 + .8 * v + .03 * math.sin(dt * 6), -8)
        if e["tt"] is not None:
            L.pon(e["tt"], W / 2, 70, _eo(dt / .5) * sal)
        return L.salida()
    return _perezoso(prep, dibuja)


# ----------------------------------------------------------------------------------------------------------- podio
def _bloque(w, h, color, num, prof=46):
    im = Image.new("RGBA", (w + prof, h + prof), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    claro = tuple(min(255, int(c * 1.25)) for c in color)
    oscuro = tuple(int(c * .55) for c in color)
    d.polygon([(0, prof), (prof, 0), (w + prof, 0), (w, prof)], fill=claro + (255,))             # tapa
    d.polygon([(w, prof), (w + prof, 0), (w + prof, h), (w, h + prof)], fill=oscuro + (255,))      # lado
    arr = np.zeros((h, w, 4), np.uint8)
    g = np.linspace(1.0, .62, h)[:, None, None]
    arr[..., :3] = np.clip(np.float32(color)[None, None, :] * g, 0, 255).astype(np.uint8)
    arr[..., 3] = 255
    im.alpha_composite(Image.fromarray(arr), (0, prof))
    f = T.fuente("Bold Condensed", int(min(w, h) * .55))
    ImageDraw.Draw(im).text((w / 2, prof + h * .5), str(num), font=f, fill=(255, 255, 255, 235), anchor="mm",
                            stroke_width=4, stroke_fill=oscuro + (255,))
    return _pil(im)


def podio(tres, titulo=None, tema="tes", tam=330, marco="museo"):
    """tres = [(ruta, nombre)] = 1.º, 2.º, 3.º. Marcas (3): aparece el 3.º, luego el 2.º, luego el 1.º (el bloque sube del
    suelo y la carta cae encima con rebote); al 1.º le giran rayos de luz detrás."""
    def prep():
        t = _col(tema)
        colores = [t["luz"], (196, 202, 214), (184, 118, 70)]
        altos = [330, 240, 180]
        xs = [W / 2, W / 2 - 430, W / 2 + 430]
        piezas = []
        for k, (ruta, nombre) in enumerate(tres[:3]):
            p, _ = _carta(ruta, nombre, tam if k == 0 else int(tam * .86), tema, marco)
            piezas.append(dict(b=_bloque(340, altos[k], colores[k], k + 1), p=p, s=_sombra(p, 14), x=xs[k], h=altos[k]))
        rayos = Image.new("RGBA", (1100, 1100), (0, 0, 0, 0))
        d = ImageDraw.Draw(rayos)
        for i in range(14):
            a0 = i * 360 / 14
            d.pieslice((0, 0, 1099, 1099), a0, a0 + 9, fill=t["luz"] + (80,))
        rayos = rayos.filter(ImageFilter.GaussianBlur(6))
        m = Image.new("L", rayos.size, 0)
        ImageDraw.Draw(m).ellipse((0, 0, 1099, 1099), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(120))
        rayos.putalpha(Image.fromarray((np.asarray(rayos.getchannel("A"), np.float32) * np.asarray(m, np.float32) / 255).astype(np.uint8)))
        return dict(piezas=piezas, rayos=_pil(rayos), tt=_texto(titulo.upper(), 72, t["luz"]) if titulo else None)

    def dibuja(e, dt, dur, marcas):
        mk = _marcas(marcas, 3, dur, .5)
        orden = {2: mk[0], 1: mk[1], 0: mk[2]}
        sal = 1 - _eio((dt - (dur - .45)) / .45)
        suelo = H - 70
        L = _L2()
        p0 = e["piezas"][0]
        u0 = dt - orden[0] - .7
        if u0 > 0:
            L.pon(e["rayos"], p0["x"], suelo - p0["h"] - 260, _c(u0 / .5) * sal, 1.0, dt * 12)
        for k in (2, 1, 0):
            if k >= len(e["piezas"]):
                continue
            pz = e["piezas"][k]
            u = dt - orden[k]
            if u < 0:
                continue
            v = _eo(u / .5)
            b = pz["b"]
            hv = int(b.shape[0] * v)
            if hv > 2:
                sub = b[:hv]
                L.pon(sub, pz["x"] + 23, suelo - hv / 2 + (1 - sal) * 400, sal)
            uc = u - .45
            if uc > 0:
                c = _back(uc / .45, 1.5)
                top = suelo - pz["h"] - 46
                y = top - pz["p"].shape[0] / 2 + 30 - (1 - c) * 500 + 4 * math.sin(dt * 1.6 + k) + (1 - sal) * 400
                L.pon(pz["s"], pz["x"] + 10, y + 16, _c(uc / .3) * sal * .7)
                L.pon(pz["p"], pz["x"], y, _c(uc / .15) * sal, 1.0, (1 - c) * (8 if k % 2 else -8))
        if e["tt"] is not None:
            L.pon(e["tt"], W / 2, 70, _eo(dt / .5) * sal)
        return L.salida()
    return _perezoso(prep, dibuja)


# ----------------------------------------------------------------------------------------------------------- muro de fichas
def _dorso_ficha(w, h, tema):
    t = _col(tema)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=12, fill=(24, 21, 19, 255), outline=t["luz"] + (255,), width=4)
    c = (w / 2, h / 2)
    r = min(w, h) * .22
    d.polygon([(c[0], c[1] - r), (c[0] + r, c[1]), (c[0], c[1] + r), (c[0] - r, c[1])], outline=t["luz"] + (255,), width=4)
    d.text(c, "?", font=T.fuente("Bold Condensed", int(r * 1.1)), fill=t["luz"] + (255,), anchor="mm")
    return _pil(im)


def muro(fotos, cols=None, tema="tes", ancho=1640, alto=860, destaca=None, titulo=None):
    """fotos = [(ruta, nombre)]: muro de fichas boca abajo que se voltean (3D) una por marca; `destaca` = índice que, en la
    marca extra (n+1), sale al frente grande mientras el resto se apaga."""
    n = len(fotos)
    cols = cols or max(2, math.ceil(math.sqrt(n * 1.8)))
    filas = math.ceil(n / cols)

    def prep():
        t = _col(tema)
        cw = int(min(ancho / cols, alto / filas) * .9)
        x0 = W / 2 - (cols - 1) * (ancho / cols) / 2
        y0 = H / 2 - (filas - 1) * (alto / filas) / 2 + (40 if titulo else 0)
        fs = []
        for k, (ruta, nombre) in enumerate(fotos):
            im, rec = PA._abre(ruta)
            base = PA._llena(im, rec, cw, cw, tema, foco=(.5, .3)).convert("RGBA")
            d = ImageDraw.Draw(base)
            d.rounded_rectangle((0, 0, cw - 1, cw - 1), radius=12, outline=t["luz"] + (255,), width=4)
            f = PA._texto_cabe(d, nombre.upper(), cw * .9, int(cw * .12))
            hb = int(cw * .2)
            d.rectangle((4, cw - hb, cw - 5, cw - 5), fill=(10, 9, 8, 200))
            d.text((cw / 2, cw - hb / 2 - 2), nombre.upper(), font=f, fill=t["texto"] + (255,), anchor="mm")
            m = Image.new("L", (cw, cw), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, cw - 1), radius=12, fill=255)
            base.putalpha(m)
            p = _pil(base)
            fs.append(dict(u8=PA._u8_recto(p, PA._sangra(p)), x=x0 + (k % cols) * ancho / cols - W / 2,
                           y=y0 + (k // cols) * alto / filas - H / 2))
        dor = _dorso_ficha(cw, cw, tema)
        return dict(fs=fs, cw=cw, dor=PA._u8_recto(dor, PA._sangra(dor)), tt=_texto(titulo.upper(), 70, t["luz"]) if titulo else None)

    def dibuja(e, dt, dur, marcas):
        mk = _marcas(marcas, n + (1 if destaca is not None else 0), dur, .5)
        sal = 1 - _eio((dt - (dur - .45)) / .45)
        L = _L3()
        L._limpia()
        cw = e["cw"]
        dst = destaca is not None and dt > mk[n]
        vd = _eio((dt - mk[n]) / .6) if dst else 0
        orden = sorted(range(n), key=lambda k: (k == destaca and dst))
        for k in orden:
            f = e["fs"][k]
            ent = _eo((dt - .05 * k) / .4)
            u = _eio((dt - mk[k]) / .5)
            th = 180 * (1 - u)
            x, y, s, z = f["x"], f["y"], 1.0, 0.0
            luz = 1.0
            if dst:
                if k == destaca:
                    x, y = x * (1 - vd), y * (1 - vd) + 40 * vd
                    s, z = 1 + .95 * vd, -90 * vd
                else:
                    luz = 1 - .6 * vd
            pose = PA._pose(x=x, y=y + 4 * math.sin(dt * 1.5 + k), z=z, ry=th, s=s * (.6 + .4 * ent), a=ent * sal,
                            rz=(1 - u) * 6 * math.sin(k))
            img = f["u8"] if th < 90 else e["dor"]
            if th >= 90:
                pose["ry"] = th - 180
            L.dibuja(img, PA._quad(cw, cw), pose, cw, cw, a=pose["a"], luz=luz * (.6 + .4 * abs(math.cos(math.radians(th)))))
        out = L.cuadro()
        if e["tt"] is not None:
            L2 = _L2()
            L2.f = PA._prem(Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGRA2RGBA)))
            L2.pon(e["tt"], W / 2, 70, sal * _eo(dt / .5))
            return L2.salida()
        return out
    return _perezoso(prep, dibuja)


# ----------------------------------------------------------------------------------------------------------- hoja de prueba
def catalogo():
    return ["tierlist", "carrusel", "tablero", "versus", "podio", "muro"]


def hoja(tema="tes", imgs=None, salida="previews", fondo=None):
    os.makedirs(salida, exist_ok=True)
    if not imgs:
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        c = os.path.join(raiz, "videos", "tes_dwemer_desaparicion", "pegatinas")
        imgs = sorted(os.path.join(c, f) for f in os.listdir(c) if f.endswith(".png") and not f.startswith("com_"))[:8]
    nom = [os.path.splitext(os.path.basename(p))[0].replace("_", " ")[:14] for p in imgs]
    fo = list(zip(imgs, nom))
    pruebas = [("tierlist", tierlist([(p, n, "SABCD"[i % 5]) for i, (p, n) in enumerate(fo[:6])], titulo="Prueba de tier list", tema=tema), 9.0),
               ("carrusel", carrusel(fo[:6], tema=tema, titulo="Carrusel"), 8.0),
               ("tablero", tablero(fo[:6], hilos=[(0, 1), (1, 3), (2, 4), (4, 5)], titulo="El caso", tema=tema), 8.0),
               ("versus", versus(fo[0], fo[1], ganador=1, tema=tema), 6.0),
               ("podio", podio(fo[:3], titulo="Los más fuertes", tema=tema), 6.0),
               ("muro", muro(fo[:8], destaca=2, tema=tema, titulo="Muro"), 8.0)]
    if fondo and os.path.exists(fondo):
        bg = cv2.resize(cv2.imread(fondo), (W, H))
    else:
        yy, xx = np.mgrid[0:H, 0:W]
        bg = np.dstack([40 + 30 * xx / W, 46 + 20 * yy / H, 60 + 40 * (1 - yy / H)]).astype(np.uint8)
    rutas = []
    for nombre, fn, dur in pruebas:
        celdas = []
        for t in [dur * k / 5 + .5 for k in range(5)] + [dur - .2]:
            o = fn(t, dur, [])
            a = o[..., 3:4].astype(np.float32) / 255
            c = (o[..., :3] * a + bg * (1 - a)).astype(np.uint8)
            cv2.putText(c, "%s %.1fs" % (nombre, t), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 4)
            celdas.append(cv2.resize(c, (640, 360), interpolation=cv2.INTER_AREA))
        img = np.vstack([np.hstack(celdas[:3]), np.hstack(celdas[3:])])
        r = os.path.join(salida, "presenta_%s_%s.jpg" % (tema, nombre))
        cv2.imwrite(r, img, [cv2.IMWRITE_JPEG_QUALITY, 85])
        rutas.append(r)
    return rutas


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=("hoja", "catalogo"))
    ap.add_argument("--tema", default="tes")
    ap.add_argument("--img", nargs="*")
    ap.add_argument("--fondo")
    ap.add_argument("--salida", default="previews")
    a = ap.parse_args()
    if a.accion == "catalogo":
        print(" ".join(catalogo()))
    else:
        for r in hoja(a.tema, a.img, a.salida, a.fondo):
            print(r)
