# -*- coding: utf-8 -*-
"""AMPLIACIÓN DEL CATÁLOGO DE PEGATINAS (el usuario, 5-nov-2026, TODOS los canales: «implementa los nuevos kits de animaciones
y amplíalo todavía más: nuevas formas de presentar pegatinas, imágenes y mapas»).

Se registra sola dentro de `peg_anim` al importarlo (no hay que tocar efectos.py): el rotador de cada video ya reparte también
estas piezas, con afinidad por tema.
  marcos    pergamino (hoja con rodillos, foto entintada)  vitral (arco gótico con plomos y vidrios teñidos, halo del tema)
            naipe (carta coleccionable: barra de nombre, ventana, estrellas de rareza)  estampilla (sello postal dentado + matasellos)
  entradas  persiana (lamas 3D que giran escalonadas)  portal (iris circular con anillo de luz)  escaner (barrido de luz con
  y salidas filas que tiemblan)  desenrolla (se desenrolla de arriba con el rodillo a la vista)  aplasta (cae estirada, se aplasta
            y rebota como dibujo animado)
  estancias orbita (gira despacio en 3D enseñando el canto)  vela (luz de vela que parpadea, cálida)  balanceo (colgada de un
            clavo, se mece como péndulo)
Hoja de prueba: la misma de siempre (`python nucleo/peg_anim.py hoja --tema tes`) ya incluye todo lo nuevo.
"""
import math
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PA = None          # el módulo peg_anim (se asigna en registra(); así funciona también si peg_anim corre como __main__)


def _T():
    return PA.T


# ----------------------------------------------------------------------------------------------------------- marcos
def _ventana_foto(out, src, win, mask, post=None):
    x, y, w, h = win
    foto = src.resize((w, h), Image.LANCZOS)
    if post:
        foto = Image.fromarray(post(np.array(foto.convert("RGB"))))
    out.paste(foto, (x, y), mask)
    return mask


def _post_tinta(papel, k=.2, contraste=1.06):
    p = np.float32(papel)

    def post(a):
        a = a.astype(np.float32)
        g = a.mean(2, keepdims=True)
        a = g + (a - g) * .78                                       # algo desaturada, como impresa en el papel
        a = (a - 128) * contraste + 128
        return np.clip(a * (1 - k) + p * k, 0, 255).astype(np.uint8)
    return post


def m_pergamino(im, rec, titulo, tam, tema):
    """Hoja de pergamino con un rodillo arriba y otro abajo; la foto va entintada sobre el papel, título en serifa."""
    t = PA._col(tema)
    k = tam / max(im.size)
    w, h = max(40, int(im.width * k)), max(40, int(im.height * k))
    M, rod = int(tam * .08), int(tam * .07)
    pie = int(tam * .12) if titulo else int(tam * .03)
    W, H = w + 2 * M, h + 2 * M + pie + 2 * rod
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cuerpo = PA._grano(W - 16, H - 2 * rod, t["papel"], 18, 11)
    al = Image.new("L", cuerpo.size, 255)                              # bordes laterales gastados
    n = PA._ruido(cuerpo.size[1], 2, 9, 5)
    da = ImageDraw.Draw(al)
    for yy in range(cuerpo.size[1]):
        da.line((0, yy, int(n[yy, 0] * 6), yy), fill=0)
        da.line((cuerpo.size[0] - 1 - int(n[yy, 1] * 6), yy, cuerpo.size[0], yy), fill=0)
    cuerpo.putalpha(al.filter(ImageFilter.GaussianBlur(.8)))
    # mancha de envejecido en los bordes del papel
    yy, xx = np.mgrid[0:cuerpo.size[1], 0:cuerpo.size[0]]
    r = np.maximum(np.abs(xx / cuerpo.size[0] - .5), np.abs(yy / cuerpo.size[1] - .5)) * 2
    c = np.asarray(cuerpo, np.float32)
    c[..., :3] *= (1 - .28 * np.clip(r - .55, 0, 1) ** 1.4 / .45 ** 1.4)[..., None]
    cuerpo = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))
    out.alpha_composite(cuerpo, (8, rod))
    d = ImageDraw.Draw(out)
    madera = tuple(int(v * .55) for v in t["tinta"])
    for y0 in (0, H - 2 * rod):                                       # rodillos: cilindro sombreado + pomos
        cil = np.zeros((2 * rod, W - 4, 4), np.uint8)
        v = np.sin(np.linspace(0, math.pi, 2 * rod))[:, None]
        base = np.float32(t["papel"]) * (.45 + .6 * v)
        cil[..., :3] = np.clip(base, 0, 255)[:, None, :].astype(np.uint8)
        cil[..., 3] = 255
        out.alpha_composite(Image.fromarray(cil), (2, y0))
        d.line((2, y0 + 2 * rod - 1, W - 3, y0 + 2 * rod - 1), fill=tuple(int(v * .6) for v in t["papel"]) + (255,), width=2)
        for x0 in (0, W - rod):
            d.ellipse((x0 - 2, y0 - 3, x0 + rod + 2, y0 + 2 * rod + 3), fill=madera + (255,), outline=t["luz"] + (255,), width=2)
    win = (M, rod + M, w, h)
    src = PA._llena(im, rec, int(w * 1.3), int(h * 1.3), tema)
    post = _post_tinta(t["papel"], .16)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rectangle((0, 0, w - 1, h - 1), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2.2))
    _ventana_foto(out, src, win, m, post)
    d.rectangle((M - 4, rod + M - 4, M + w + 3, rod + M + h + 3), outline=t["tinta"] + (200,), width=2)
    if titulo:
        f = PA._texto_cabe(d, titulo, W * .86, int(tam * .075), "GARABD.TTF")
        d.text((W / 2, rod + M + h + (pie + M) / 2), titulo, font=f, fill=t["tinta"] + (255,), anchor="mm")
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dorso.alpha_composite(PA._grano(W - 16, H - 2 * rod, tuple(int(v * .9) for v in t["papel"]), 18, 12), (8, rod))
    for y0 in (0, H - 2 * rod):
        dorso.alpha_composite(out.crop((0, y0, W, y0 + 2 * rod)), (0, y0))
    return PA.Carta(out, win, np.asarray(m), src, dorso, post)


def _plomos(w, h, n, semilla):
    """Celdas de vitral (Voronoi) -> (tinte por píxel float32 HxWx3, máscara de plomo float32 HxW)."""
    rng = np.random.default_rng(semilla)
    sw, sh = max(8, w // 4), max(8, h // 4)
    sem = rng.random((n, 2)) * [sw, sh]
    yy, xx = np.mgrid[0:sh, 0:sw]
    dd = (xx[None] - sem[:, 0, None, None]) ** 2 + (yy[None] - sem[:, 1, None, None]) ** 2
    lab = dd.argmin(0).astype(np.int32)
    lab = cv2.resize(lab.astype(np.float32), (w, h), interpolation=cv2.INTER_NEAREST).astype(np.int32)
    borde = np.zeros((h, w), np.uint8)
    borde[:, 1:] |= (lab[:, 1:] != lab[:, :-1])
    borde[1:, :] |= (lab[1:, :] != lab[:-1, :])
    borde = cv2.dilate(borde * 255, np.ones((3, 3), np.uint8), iterations=2)
    borde = cv2.GaussianBlur(borde.astype(np.float32) / 255, (0, 0), 1.0)
    # vidrios de colores de vidriera (rubí, cobalto, esmeralda, ámbar, violeta): cada celda se tiñe hacia uno
    vidrios = np.float32([(1.35, .75, .7), (.7, .85, 1.4), (.75, 1.25, .8), (1.3, 1.08, .6), (1.1, .78, 1.25), (1, 1, 1)])
    sel = vidrios[rng.integers(0, len(vidrios), n)]
    luz = 1 + rng.uniform(-.1, .16, (n, 1)).astype(np.float32)
    return ((.45 + .55 * sel) * luz)[lab], borde


def _arco(w, h):
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    r = w / 2
    d.rectangle((0, r, w - 1, h - 1), fill=255)
    d.pieslice((0, 0, w - 1, 2 * r), 180, 360, fill=255)
    return m


def m_vitral(im, rec, titulo, tam, tema):
    """Vidriera: arco de piedra oscura, plomos que parten la foto en vidrios teñidos y un halo de luz del tema alrededor."""
    t = PA._col(tema)
    k = tam / max(im.size)
    w = max(60, int(im.width * k))
    h = max(int(w * 1.15), int(im.height * k))
    B = int(tam * .045)
    pie = int(tam * .11) if titulo else 0
    G = int(tam * .06)                                                # halo
    W, H = w + 2 * B + 2 * G, h + 2 * B + pie + 2 * G
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    marco = _arco(w + 2 * B, h + 2 * B)
    halo = Image.new("L", (W, H), 0)
    halo.paste(marco, (G, G))
    halo = halo.filter(ImageFilter.GaussianBlur(G / 2.2)).point(lambda v: int(v * .75))
    out.paste(t["luz"] + (255,), mask=halo)
    piedra = PA._grano(w + 2 * B, h + 2 * B, tuple(int(v * .35) for v in t["tinta"]), 16, 4)
    piedra.putalpha(marco)
    out.alpha_composite(piedra, (G, G))
    tinte, plomo = _plomos(w, h, 13 + int(tam / 90), int(tam) % 97 + 3)
    luz_c = np.float32(t["luz"])

    def post(a):
        a = a.astype(np.float32) * tinte
        a = a * 1.08 + luz_c * .06
        a = a * (1 - plomo[..., None]) + np.float32((22, 20, 18)) * plomo[..., None]
        return np.clip(a, 0, 255).astype(np.uint8)
    win = (G + B, G + B, w, h)
    src = PA._llena(im, rec, int(w * 1.3), int(h * 1.3), tema)
    m = _arco(w, h)
    _ventana_foto(out, src, win, m, post)
    d = ImageDraw.Draw(out)
    d.arc((G + B - 2, G + B - 2, G + B + w + 1, G + B + w + 1), 180, 360, fill=t["luz"] + (230,), width=3)
    d.line((G + B - 2, G + B + w / 2, G + B - 2, G + B + h + 1), fill=t["luz"] + (230,), width=3)
    d.line((G + B + w + 1, G + B + w / 2, G + B + w + 1, G + B + h + 1), fill=t["luz"] + (230,), width=3)
    if titulo:
        f = PA._texto_cabe(d, titulo.upper(), W * .8, int(tam * .065))
        PA._pildora(d, W / 2, G + 2 * B + h - int(tam * .02), titulo.upper(), f, (12, 11, 10, 235), t["luz"] + (255,), t["texto"] + (255,))
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dorso.alpha_composite(piedra, (G, G))
    return PA.Carta(out, win, np.asarray(m), src, dorso, post)


def m_naipe(im, rec, titulo, tam, tema):
    """Carta coleccionable: marco degradado del tema, barra con el nombre, ventana de la foto, estrellas de rareza y gema."""
    t = PA._col(tema)
    W, H = int(tam * .74), int(tam)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    yy = np.linspace(0, 1, H)[:, None, None]
    luz, osc = np.float32(t["luz"]), np.float32(t["luz"]) * .35
    grad = np.clip(luz * (1 - yy) + osc * yy, 0, 255) * np.ones((1, W, 1))
    al = Image.new("L", (W, H), 0)
    R = int(W * .06)
    ImageDraw.Draw(al).rounded_rectangle((0, 0, W - 1, H - 1), radius=R, fill=255)
    cara = Image.fromarray(np.dstack([grad.astype(np.uint8), np.asarray(al)[..., None]]).astype(np.uint8))
    out.alpha_composite(cara)
    d = ImageDraw.Draw(out)
    m_ = int(W * .045)
    d.rounded_rectangle((m_, m_, W - m_, H - m_), radius=R - 4, fill=(18, 16, 15, 255))
    bar = int(H * .1)
    d.rounded_rectangle((m_ * 2, m_ * 2, W - m_ * 2, m_ * 2 + bar), radius=bar // 3, fill=tuple(int(v * .85) for v in t["papel"]) + (255,),
                        outline=t["luz"] + (255,), width=2)
    if titulo:
        f = PA._texto_cabe(d, titulo.upper(), W - m_ * 4 - bar, int(bar * .55))
        d.text((m_ * 2 + 14, m_ * 2 + bar / 2), titulo.upper(), font=f, fill=t["tinta"] + (255,), anchor="lm")
    gx, gy, gr = W - m_ * 2 - bar / 2, m_ * 2 + bar / 2, bar * .34          # gema de la esquina
    d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=t["rojo"] + (255,), outline=t["luz"] + (255,), width=2)
    d.ellipse((gx - gr * .45, gy - gr * .6, gx - gr * .05, gy - gr * .2), fill=(255, 255, 255, 170))
    wx, wy = m_ * 2, m_ * 3 + bar
    ww, wh = W - m_ * 4, int(H * .56)
    src = PA._llena(im, rec, int(ww * 1.3), int(wh * 1.3), tema)
    mk = Image.new("L", (ww, wh), 0)
    ImageDraw.Draw(mk).rectangle((0, 0, ww - 1, wh - 1), fill=255)
    _ventana_foto(out, src, (wx, wy, ww, wh), mk)
    d.rectangle((wx - 2, wy - 2, wx + ww + 1, wy + wh + 1), outline=t["luz"] + (255,), width=3)
    by = wy + wh + int(H * .03)                                         # caja inferior con estrellas de rareza
    d.rounded_rectangle((m_ * 2, by, W - m_ * 2, H - m_ * 2), radius=10, fill=(30, 27, 24, 255), outline=t["luz"] + (160,), width=2)
    n = 5
    cy = (by + H - m_ * 2) / 2
    for i in range(n):
        cx = W / 2 + (i - (n - 1) / 2) * W * .13
        r1, r2 = W * .045, W * .019
        pts = [(cx + (r1 if j % 2 == 0 else r2) * math.sin(j * math.pi / 5), cy - (r1 if j % 2 == 0 else r2) * math.cos(j * math.pi / 5))
               for j in range(10)]
        d.polygon(pts, fill=t["luz"] + (255,), outline=(20, 18, 16, 255))
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dorso.alpha_composite(cara)
    dd = ImageDraw.Draw(dorso)
    dd.rounded_rectangle((m_, m_, W - m_, H - m_), radius=R - 4, fill=(22, 19, 17, 255))
    for i in range(-H, W + H, 26):                                    # rombos del dorso
        dd.line((i, m_, i + H, H - m_), fill=t["luz"] + (60,), width=2)
        dd.line((i + H, m_, i, H - m_), fill=t["luz"] + (60,), width=2)
    dd.ellipse((W / 2 - W * .16, H / 2 - W * .16, W / 2 + W * .16, H / 2 + W * .16), outline=t["luz"] + (255,), width=4)
    dorso.putalpha(al)
    return PA.Carta(out, (wx, wy, ww, wh), np.asarray(mk), src, dorso)


def m_estampilla(im, rec, titulo, tam, tema):
    """Sello postal: borde dentado, margen de papel, valor en la esquina y matasellos ondulado encima de la foto."""
    t = PA._col(tema)
    k = tam / max(im.size)
    w, h = max(50, int(im.width * k)), max(50, int(im.height * k))
    Mg = int(tam * .07)
    pie = int(tam * .09) if titulo else 0
    W, H = w + 2 * Mg, h + 2 * Mg + pie
    al = Image.new("L", (W, H), 255)
    da = ImageDraw.Draw(al)
    r = max(4, int(tam * .018))
    paso = r * 3.1
    for x in np.arange(paso / 2, W, paso):
        da.ellipse((x - r, -r, x + r, r), fill=0)
        da.ellipse((x - r, H - r, x + r, H + r), fill=0)
    for y in np.arange(paso / 2, H, paso):
        da.ellipse((-r, y - r, r, y + r), fill=0)
        da.ellipse((W - r, y - r, W + r, y + r), fill=0)
    out = PA._grano(W, H, (246, 241, 230), 8, 9)
    out.putalpha(al)
    d = ImageDraw.Draw(out)
    d.rectangle((Mg - 5, Mg - 5, Mg + w + 4, Mg + h + 4), outline=t["rojo"] + (255,), width=3)
    tinta = np.float32((40, 34, 30))
    rng = random.Random(int(tam) + 7)
    cx, cy, R = w * rng.uniform(.62, .8), h * rng.uniform(.12, .3), min(w, h) * .2
    ondas = np.zeros((h, w), np.float32)
    cv2.circle(ondas, (int(cx), int(cy)), int(R), 1.0, 3, cv2.LINE_AA)
    cv2.circle(ondas, (int(cx), int(cy)), int(R * .8), 1.0, 2, cv2.LINE_AA)
    for j in range(4):
        xs = np.arange(int(cx - R * .2), w)
        ys = cy - R * .45 + j * R * .3 + np.sin(xs / (R * .25)) * R * .08
        cv2.polylines(ondas, [np.stack([xs, ys], 1).astype(np.int32)], False, 1.0, 3, cv2.LINE_AA)
    ondas = cv2.GaussianBlur(ondas, (0, 0), .7) * .72 * (.75 + .25 * PA._ruido(h, w, 4, 3))

    def post(a):
        a = a.astype(np.float32)
        return np.clip(a * (1 - ondas[..., None]) + tinta * ondas[..., None], 0, 255).astype(np.uint8)
    src = PA._llena(im, rec, int(w * 1.3), int(h * 1.3), tema)
    mk = Image.new("L", (w, h), 255)
    _ventana_foto(out, src, (Mg, Mg, w, h), mk, post)
    fv = _T().fuente("Bold Condensed", int(tam * .075))
    d.text((Mg + 10, Mg + 6), "%d" % rng.choice((5, 10, 25, 50)), font=fv, fill=(250, 246, 236, 255), stroke_width=3,
           stroke_fill=t["rojo"] + (255,))
    if titulo:
        f = PA._texto_cabe(d, titulo.upper(), W * .86, int(pie * .62))
        d.text((W / 2, Mg + h + (pie + Mg) / 2 - 2), titulo.upper(), font=f, fill=t["rojo"] + (255,), anchor="mm")
    dorso = PA._grano(W, H, (236, 230, 214), 8, 10)
    dorso.putalpha(al)
    return PA.Carta(out, (Mg, Mg, w, h), np.asarray(mk), src, dorso, post)


# ----------------------------------------------------------------------------------------------------------- entradas/salidas
def t_persiana(P, img, u, fuera, pose):
    """Lamas horizontales que giran sobre su eje (3D), escalonadas de arriba abajo."""
    n = random.Random(P.semilla + 31).choice((6, 7, 8, 9))
    w, h = P.w, P.h
    capas, lleno, suma = [], True, 0.0
    sgn = -1 if fuera else 1
    for i in range(n):
        dly = (i / n) * .42
        e = PA._eo(PA._c((u - dly) / .58)) if not fuera else PA._eio(PA._c((u - dly) / .58))
        suma += e
        if e < .999:
            lleno = False
        th = math.radians((1 - e) * 90 * sgn)
        y0, y1 = int(i * h / n), int((i + 1) * h / n)
        hh, yc = (y1 - y0) / 2, (y0 + y1) / 2 - h / 2
        ct, st = math.cos(th), math.sin(th)
        q = np.array([[-w / 2, yc - hh * ct, -hh * st], [w / 2, yc - hh * ct, -hh * st],
                      [w / 2, yc + hh * ct, hh * st], [-w / 2, yc + hh * ct, hh * st]], float)
        if hh * abs(ct) < .6:
            continue
        capas.append(dict(img=np.ascontiguousarray(img[y0:y1]), q=q, luz=.5 + .5 * abs(ct), a=PA._c(e * 4)))
    if lleno:
        return None
    pose["sombra"] *= (suma / n) ** 2
    return capas


def t_portal(P, img, u, fuera, pose):
    """Se abre (o se cierra) como un iris circular desde el centro, con un anillo de luz del tema en el filo."""
    def campo():
        yy, xx = np.mgrid[0:P.h, 0:P.w].astype(np.float32)
        return PA._norm01(np.hypot((xx - P.w / 2) / (P.w / 2), (yy - P.h / 2) / (P.h / 2)))
    D = P._campo("radial", campo)
    e = PA._eio(u) if fuera else PA._eo(u)
    thr = e * 1.12 - .04
    m = PA._suave((thr - D) / .02)
    anillo = np.exp(-((D - thr) / .022) ** 2) * img[..., 3] * (1 - e * .6)
    o = img * m[..., None]
    o[..., :3] += anillo[..., None] * P.c_luz * 1.3
    o[..., 3] = np.maximum(o[..., 3], anillo)
    o[..., :3] = np.minimum(o[..., :3], o[..., 3:4])
    pose["rz"] += (1 - e) * -28 * P.lado
    pose["s"] *= .9 + .1 * e
    pose["sombra"] *= e ** 2
    return [dict(img=o, q=PA._quad(P.w, P.h), sombra=True)] if u > .01 else []


def t_escaner(P, img, u, fuera, pose):
    """Una línea de luz barre de arriba abajo y va revelando la imagen; las filas junto a la línea tiemblan (señal digital)."""
    D = P._campo("vert", lambda: np.repeat(np.linspace(0, 1, P.h, dtype=np.float32)[:, None], P.w, 1))
    e = PA._eio(u) if fuera else PA._eo(u)
    thr = e * 1.1 - .05
    m = PA._suave((thr - D) / .008) if not fuera else PA._suave((thr - D) / .008)
    o = img * m[..., None]
    rng = np.random.default_rng(int(u * 997) + P.semilla)
    y0 = int(max(0, (thr - .07) * P.h))
    y1 = int(min(P.h, thr * P.h))
    for y in range(y0, y1, 3):                                         # filas que tiemblan cerca del filo
        dx = int(rng.integers(-14, 15))
        o[y:y + 3] = np.roll(o[y:y + 3], dx, axis=1)
    linea = np.exp(-((D - thr) / .006) ** 2)
    estela = np.clip(1 - (thr - D) / .14, 0, 1) * (D < thr) * .35
    a = img[..., 3]
    o[..., :3] += ((linea * 1.2 + estela) * a)[..., None] * P.c_luz
    o[..., 3] = np.maximum(o[..., 3], linea * a)
    o[..., :3] = np.minimum(o[..., :3], o[..., 3:4])
    pose["sombra"] *= PA._c((e - .8) / .2)          # la sombra entera no puede ir debajo de media imagen
    return [dict(img=o, q=PA._quad(P.w, P.h), sombra=True)] if u > .01 else []


def t_desenrolla(P, img, u, fuera, pose):
    """Se desenrolla desde arriba como un pergamino: lo ya abierto y, en el filo, el rodillo con el resto enrollado."""
    e = PA._eio(u) if fuera else PA._eo(u)
    if e > .999:
        return None
    w, h = P.w, P.h
    Y = int(e * h)
    r = max(7, int(h * .06))
    capas = []
    if Y > 1:
        capas.append(dict(img=np.ascontiguousarray(img[:Y]), q=PA._quad(w, h, 0, 0, w, Y), sombra=False))
    base = P.dorso if P.dorso is not None else img
    a0, a1 = min(h - 1, Y), min(h, Y + 2 * r)
    if a1 - a0 >= 2:
        rod = base[a0:a1][::-1].copy()
        v = np.sin(np.linspace(0, math.pi, rod.shape[0], dtype=np.float32))[:, None, None]
        rod[..., :3] *= .35 + .75 * v
        hh = rod.shape[0]
        q = PA._quad(w, h, -3, Y - hh * .25, w + 3, Y + hh * .75)
        q[:, 2] = -r * .9
        capas.append(dict(img=np.ascontiguousarray(rod), q=q))
    pose["sombra"] *= PA._c((e - .8) / .2)
    pose["a"] *= PA._c(u * 6)
    return capas


def t_aplasta(P, img, u, fuera, pose):
    """Dibujo animado: cae estirada, se aplasta contra el suelo y rebota hasta asentarse (al irse: se agacha y sale disparada)."""
    pose["py"] = .5
    if not fuera:
        if u < .42:
            k = (u / .42) ** 2
            pose["y"] -= (1 - k) * P.h * 1.5
            pose["sy"] *= 1.32
            pose["sx"] *= .78
            pose["alt"] += (1 - k) * 1.1
        else:
            v = (u - .42) / .58
            amp = .34 * math.exp(-4.2 * v) * math.cos(10.5 * v)
            pose["sy"] *= 1 - amp
            pose["sx"] *= 1 + amp * .8
        pose["a"] *= PA._c(u * 6)
    else:
        v = 1 - u
        if v < .35:
            k = math.sin(v / .35 * math.pi / 2)
            pose["sy"] *= 1 - .3 * k
            pose["sx"] *= 1 + .22 * k
        else:
            k = (v - .35) / .65
            pose["y"] -= k * k * P.h * 1.8
            pose["sy"] *= 1 + .4 * k
            pose["sx"] *= 1 - .25 * k
            pose["alt"] += k
            pose["a"] *= PA._c((1 - k) * 2.5)
    return None


# ----------------------------------------------------------------------------------------------------------- estancias
def es_orbita(P, img, pose, dt, dur):
    """Gira despacio en 3D (se ve el canto en perspectiva): para objetos y reliquias."""
    pose["ry"] += 16 * math.sin(dt * .85 + P.fase)
    pose["rx"] += 5 * math.sin(dt * .6 + P.fase * .5)
    pose["rz"] += P.giro * .5
    pose["alt"] += .18 + .08 * math.sin(dt * 1.3)
    return img


def es_vela(P, img, pose, dt, dur):
    """Luz de vela: parpadeo cálido e irregular, con la pegatina casi quieta (para tonos de misterio o tragedia)."""
    PA.es_quieta(P, img, pose, dt, dur)
    fl = (math.sin(dt * 13.1) + .6 * math.sin(dt * 7.3 + 1.1) + .4 * math.sin(dt * 23.7 + .3)) / 2.0
    k = .9 + .1 * fl
    o = img.copy()
    o[..., 0] *= k * .92
    o[..., 1] *= k * .98
    o[..., 2] *= min(1.12, k * 1.06)
    o[..., :3] = np.minimum(o[..., :3], o[..., 3:4])
    return o


def es_balanceo(P, img, pose, dt, dur):
    """Colgada de un clavo: se mece como un péndulo desde el borde de arriba."""
    pose["py"] = -.5
    pose["rz"] += 6.5 * math.sin(dt * 1.55 + P.fase) * (.6 + .4 * math.exp(-dt * .4))
    w, h = P.w, P.h

    def clavo(L, pose_):
        p = L.proy(np.array([[0.0, -h / 2 + max(8, h * .03), 0.0]]), pose_, w, h)[0]
        PA._punto(L, p[0] + 3, p[1] + 4, 9, (0, 0, 0), .45 * pose_["a"])
        PA._punto(L, p[0], p[1], 9, P.c_luz * .55, pose_["a"])
        PA._punto(L, p[0] - 2, p[1] - 2, 4, P.c_luz, pose_["a"])
    P.delante.append(clavo)
    return img


# ----------------------------------------------------------------------------------------------------------- registro
MARCOS = dict(pergamino=m_pergamino, vitral=m_vitral, naipe=m_naipe, estampilla=m_estampilla)
ENT = dict(persiana=t_persiana, portal=t_portal, escaner=t_escaner, desenrolla=t_desenrolla, aplasta=t_aplasta)
EST = dict(orbita=es_orbita, vela=es_vela, balanceo=es_balanceo)
AFIN = {"epico": {"pergamino", "vitral", "portal", "desenrolla", "orbita", "vela", "balanceo"},
        "retro": {"naipe", "escaner", "aplasta", "persiana", "estampilla"},
        "militar": {"escaner", "persiana", "estampilla", "orbita"},
        "jugueton": {"aplasta", "estampilla", "balanceo", "naipe", "persiana"}}
POCO = {"epico": {"aplasta"}, "militar": {"aplasta", "vitral", "naipe"}, "jugueton": {"vitral"}, "retro": {"vela"}}


def registra(pa):
    """Mete marcos, entradas/salidas y estancias nuevas en peg_anim (lo llama peg_anim al final de su carga)."""
    global PA
    PA = pa
    pa.MARCOS.update(MARCOS)
    pa.MARCOS_TODOS = tuple(pa.MARCOS_TODOS) + tuple(k for k in MARCOS if k not in pa.MARCOS_TODOS)
    pa.ENT.update(ENT)
    pa.SAL.update(ENT)
    pa.ENTRADAS = tuple(pa.ENTRADAS) + tuple(k for k in ENT if k not in pa.ENTRADAS)
    pa.SALIDAS = tuple(pa.SALIDAS) + tuple(k for k in ENT if k not in pa.SALIDAS)
    pa.EST.update(EST)
    pa.ESTANCIAS = tuple(pa.ESTANCIAS) + tuple(k for k in EST if k not in pa.ESTANCIAS)
    pa._TE.update(persiana=.85, portal=.8, escaner=.95, desenrolla=1.0, aplasta=.95)
    pa._TS.update(persiana=.6, portal=.55, escaner=.6, desenrolla=.7, aplasta=.6)
    for fam, s in AFIN.items():
        pa._AFIN.setdefault(fam, set()).update(s)
    for fam, s in POCO.items():
        pa._POCO.setdefault(fam, set()).update(s)
