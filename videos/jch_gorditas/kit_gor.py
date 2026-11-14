# -*- coding: utf-8 -*-
"""MG NUEVOS del reel jch_gorditas (vertical 1080x1920), sobre las primitivas de kit_jch.py. Cada uno: fn(dt, dur, marcas) -> BGRA.
  mapa_paso()        mapa REAL (OpenTopoMap) : tramo de carrera en rojo → Moyahua→Juchipila en amarillo «17 KM · 20 MIN»
                     → Apozol «HOTEL SEDE» con su tramo a Juchipila («TE QUEDA DE PASO»).
  pizarra(tit, items) pizarra de fonda (gis sobre pizarrón con marco de madera) cuyos renglones se escriben con las marcas.
  sello(texto)       sello de goma que cae girado y deja tinta («IMPRESCINDIBLE»).
  tacometro()        tacómetro de moto «¿A QUÉ VIENES?»: la aguja está en CARRERA y, con la marca, se va a la zona roja GORDITAS.
  cartel(arriba, grande, abajo)  letrero de pueblo para el gancho («JUCHIPILA», «ZACATECAS»).
"""
import json, math, os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from kit_jch import W, H, ROJO, VERDE, AMAR, BLANCO, NEGRO, texto_img, ease, pop, a_bgra, _merc, PUEBLOS, AQ

GIS = (244, 240, 228)


def _alfa(im, e):
    a = np.array(im)
    a[:, :, 3] = (a[:, :, 3] * max(0., min(1., e))).astype(np.uint8)
    return a_bgra(Image.fromarray(a))


# ------------------------------------------------------------------ mapa: te queda de paso
def mapa_paso():
    c = {}

    def prep():
        meta = json.load(open(os.path.join(AQ, "mapas", "canon_meta.json")))
        base = cv2.imread(os.path.join(AQ, "mapas", "canon_base.png"))
        base = cv2.addWeighted(base, .80, np.full_like(base, (40, 30, 20)), .20, 0)
        m = lambda la, lo: np.array(_merc(la, lo, meta["z"], meta["tx0"], meta["ty0"]))
        co = json.load(open(os.path.join(AQ, "_ruta.json")))["routes"][0]["geometry"]["coordinates"]
        pts = np.array([m(la, lo) for lo, la in co])
        k = int(np.argmin(((pts - m(*PUEBLOS["Moyahua"])) ** 2).sum(1)))
        ap = json.load(open(os.path.join(AQ, "_ruta_apozol.json")))["routes"][0]["geometry"]["coordinates"]
        c.update(base=base, carrera=pts[:k + 1], paso=pts[k:], apozol=np.array([m(la, lo) for lo, la in ap]),
                 pueblos={n: m(*v) for n, v in PUEBLOS.items()},
                 et={n: texto_img(n.upper(), 50 if n == "Juchipila" else 42, AMAR if n == "Juchipila" else BLANCO)
                     for n in PUEBLOS},
                 meta_t=texto_img("META", 36, ROJO, b=5), hotel=texto_img("HOTEL SEDE", 36, VERDE, b=5),
                 km=texto_img("17 KM", 110, AMAR, b=8), mn=texto_img("UNOS 20 MINUTOS", 56, BLANCO, b=6),
                 tit=texto_img("TE QUEDA DE PASO", 86), cred=texto_img(
                     "Mapa: © OpenStreetMap · OpenTopoMap (CC-BY-SA) · rutas OSRM", 24, b=3, nombre="segoeui.ttf", var=None))

    def linea(f, p, col, gr, gl):
        p = p.astype(np.int32)
        g = np.zeros_like(f)
        cv2.polylines(g, [p], False, col, gl, cv2.LINE_AA)
        f[:] = cv2.add(f, cv2.GaussianBlur(g, (0, 0), 8))
        cv2.polylines(f, [p], False, (20, 20, 20), gr + 6, cv2.LINE_AA)
        cv2.polylines(f, [p], False, col, gr, cv2.LINE_AA)

    def trozo(p, k):
        if k <= 0:
            return p[:1]
        s = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
        return p[:max(2, int(np.searchsorted(s / s[-1], k)))]

    def fn(dt, dur, marcas):
        if not c:
            prep()
        mk = list(marcas) + [None] * 3
        t1 = mk[0] or dur * .3          # empieza el tramo amarillo
        t2 = mk[1] or dur * .65         # Apozol
        todo = np.vstack([c["carrera"], c["apozol"]])
        x0, y0 = todo.min(0) - (330, 420)
        x1, y1 = todo.max(0) + (330, 300)
        s = min(W / (x1 - x0), H / (y1 - y0)) * (1 + .03 * dt / max(1, dur))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
        f = cv2.warpAffine(c["base"], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        tp = lambda p: p * s + (W / 2 - s * cx, H / 2 - s * cy)
        linea(f, tp(trozo(c["carrera"], ease(dt / .8))), (46, 52, 232), 9, 26)
        kp = ease((dt - t1) / 1.2)
        if kp > 0:
            linea(f, tp(trozo(c["paso"][::-1], kp)), (0, 204, 255), 11, 30)   # de Moyahua hacia Juchipila (BGR amarillo)
        ka = ease((dt - t2) / 1.0)
        if ka > 0:
            linea(f, tp(trozo(c["apozol"][::-1], ka)), (110, 190, 40), 9, 24)
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).convert("RGBA")
        d = ImageDraw.Draw(im)
        for n, p in c["pueblos"].items():
            q = tp(p)
            if n == "Apozol" and ka <= 0:
                continue
            r = 16 if n == "Juchipila" else 12
            if n == "Juchipila":
                r = int(16 + 4 * math.sin(dt * 7))
            d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=BLANCO + (255,), outline=NEGRO + (255,), width=5)
            et = c["et"][n]
            lx = q[0] + 28 if q[0] < W * .62 else q[0] - 28 - et.width
            im.alpha_composite(et, (int(lx), int(q[1] - et.height / 2)))
            extra = c["meta_t"] if n == "Moyahua" else c["hotel"] if n == "Apozol" else None
            if extra is not None:
                ex = int(lx) if q[0] < W * .62 else int(q[0] - 28 - extra.width)
                im.alpha_composite(extra, (ex, int(q[1] + et.height / 2 - 6)))
        # banda del título y cifra del tramo
        a = ease(dt / .5)
        banda = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
        bd = ImageDraw.Draw(banda)
        for i in range(300):
            bd.line([(0, i), (W, i)], fill=(8, 8, 12, int(215 * (1 - i / 300) * a)))
        im.alpha_composite(banda, (0, 0))
        im.alpha_composite(c["tit"], ((W - c["tit"].width) // 2, 130))
        if kp > .15:
            sc = pop(dt - t1 - .3, .4) if dt > t1 + .3 else .6
            km = c["km"].resize((int(c["km"].width * sc), int(c["km"].height * sc)), Image.LANCZOS)
            jx, jy = tp(c["pueblos"]["Moyahua"])
            jy2 = tp(c["pueblos"]["Juchipila"])[1]
            yy = int((jy + jy2) / 2)
            x = int(jx - 60 - km.width) if jx - 60 - km.width > 20 else 30
            im.alpha_composite(km, (x, yy - km.height))
            im.alpha_composite(c["mn"], (max(20, x), yy + 4))
        im.alpha_composite(c["cred"], (24, H - c["cred"].height - 16))
        return a_bgra(im)
    return fn


# ------------------------------------------------------------------ pizarra de fonda
def _textura_pizarra(w, h):
    rng = np.random.default_rng(7)
    base = np.full((h, w, 3), (34, 46, 40), np.float32)
    base += rng.normal(0, 7, (h, w, 1))
    for _ in range(40):                                  # manchas de gis borrado
        x, y, r = rng.integers(0, w), rng.integers(0, h), rng.integers(40, 160)
        m = np.zeros((h, w), np.float32)
        cv2.circle(m, (int(x), int(y)), int(r), 1, -1)
        base += cv2.GaussianBlur(m, (0, 0), r / 2)[..., None] * rng.uniform(4, 12)
    return np.clip(base, 0, 255).astype(np.uint8)


def pizarra(titulo, items, ancho=900):
    """items = [texto]; cada renglón se «escribe» (barrido izquierda→derecha) en su marca."""
    tt = texto_img(titulo, 84, AMAR, b=0, nombre="segoeprb.ttf", var=None)
    if tt.width > ancho - 90:
        tt = tt.resize((ancho - 90, int(tt.height * (ancho - 90) / tt.width)), Image.LANCZOS)
    fil = [texto_img(t, 64, GIS, b=0, nombre="segoepr.ttf", var=None) for t in items]
    fil = [f if f.width <= ancho - 110 else f.resize((ancho - 110, max(1, int(f.height * (ancho - 110) / f.width))), Image.LANCZOS)
           for f in fil]                                   # renglón largo: se encoge, nunca se corta (12-nov)
    hh = 90 + tt.height + 40 + sum(f.height + 22 for f in fil) + 60
    pz = Image.fromarray(_textura_pizarra(ancho, hh)).convert("RGBA")
    marco = Image.new("RGBA", (ancho + 60, hh + 60), (0, 0, 0, 0))
    md = ImageDraw.Draw(marco)
    md.rounded_rectangle([0, 0, ancho + 59, hh + 59], 18, fill=(120, 74, 38, 255))
    for i in range(0, ancho + 60, 9):                     # vetas
        md.line([(i, 0), (i + 30, hh + 60)], fill=(98, 60, 30, 90), width=3)
    marco.alpha_composite(pz, (30, 30))
    sombra = Image.new("RGBA", (marco.width + 40, marco.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle([20, 30, marco.width + 20, marco.height + 30], 20, fill=(0, 0, 0, 140))
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    rng = np.random.default_rng(3)

    def fn(dt, dur, marcas):
        im = sombra.copy()
        im.alpha_composite(marco, (20, 10))
        # título
        k0 = ease(dt / .6)
        tw = tt.crop((0, 0, max(1, int(tt.width * k0)), tt.height))
        im.alpha_composite(tw, (20 + 30 + (ancho - tt.width) // 2, 10 + 30 + 50))
        d = ImageDraw.Draw(im)
        y0 = 10 + 30 + 50 + tt.height + 16
        d.line([(80, y0), (80 + int((ancho - 60) * k0), y0)], fill=GIS + (170,), width=4)
        y = y0 + 30
        ts = list(marcas) + [None] * len(fil)
        for i, f in enumerate(fil):
            ti = ts[i] if ts[i] is not None else .6 + i * dur * .6 / max(1, len(fil))
            k = ease((dt - ti) / .7)
            if k > 0:
                im.alpha_composite(f.crop((0, 0, max(1, int(f.width * k)), f.height)), (110, y))
                cx, cy = 80, y + f.height // 2 + 4
                d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=AMAR + (255,))
            y += f.height + 22
        e = ease(dt / .35) * (1 - ease((dt - dur + .3) / .3))
        ang = 2.5 * math.sin(dt * .9) - 1.5
        im = im.rotate(ang, resample=Image.BICUBIC, expand=True)
        return _alfa(im, e)
    return fn


# ------------------------------------------------------------------ sello de goma
def sello(texto, color=ROJO, ang=-12):
    t = texto_img(texto, 120, color, b=0)
    pad = 46
    s = Image.new("RGBA", (t.width + pad * 2, t.height + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.rounded_rectangle([6, 6, s.width - 7, s.height - 7], 22, outline=color + (255,), width=12)
    d.rounded_rectangle([24, 24, s.width - 25, s.height - 25], 14, outline=color + (255,), width=4)
    s.alpha_composite(t, (pad, pad - 8))
    a = np.array(s).astype(np.float32)
    rng = np.random.default_rng(11)
    ruido = cv2.GaussianBlur(rng.random(a.shape[:2]).astype(np.float32), (0, 0), 2.2)
    a[:, :, 3] *= np.clip((ruido - .30) * 3.2, .25, 1)       # tinta irregular
    s = Image.fromarray(a.astype(np.uint8)).rotate(ang, resample=Image.BICUBIC, expand=True)

    def fn(dt, dur, marcas):
        t0 = marcas[0] if marcas else .15
        if dt < t0:
            return a_bgra(Image.new("RGBA", s.size, (0, 0, 0, 0)))
        k = (dt - t0) / .22
        sc = 2.4 - 1.4 * ease(min(1, k)) if k < 1 else 1 + .06 * max(0, 1 - (k - 1) * 2) * math.sin((k - 1) * 20)
        im = s.resize((max(1, int(s.width * sc)), max(1, int(s.height * sc))), Image.LANCZOS)
        out = Image.new("RGBA", (int(s.width * 1.3), int(s.height * 1.3)), (0, 0, 0, 0))
        out.alpha_composite(im, ((out.width - im.width) // 2, (out.height - im.height) // 2)) if sc <= 1.3 else None
        if sc > 1.3:
            cx, cy = (im.width - out.width) // 2, (im.height - out.height) // 2
            out = im.crop((cx, cy, cx + out.width, cy + out.height))
        e = min(1, k * 1.6) * (1 - ease((dt - dur + .25) / .25))
        return _alfa(out, e)
    return fn


# ------------------------------------------------------------------ tacómetro: ¿a qué vienes?
def tacometro():
    R = 400
    tit = texto_img("¿A QUÉ VIENES?", 84)
    l1 = texto_img("CARRERA", 56, BLANCO, b=6)
    l2 = texto_img("GORDITAS", 64, AMAR, b=7)
    rpm = texto_img("x1000 r/min", 30, (210, 210, 210), b=3, nombre="segoeui.ttf", var=None)
    A0, A1 = math.radians(215), math.radians(-35)            # de izquierda abajo a derecha abajo

    def ang(v):
        return A0 + (A1 - A0) * v

    def fn(dt, dur, marcas):
        t0 = marcas[0] if marcas else dur * .45
        im = Image.new("RGBA", (W, 1080), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy = W // 2, 600
        d.ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=(26, 26, 30, 240), outline=(170, 170, 178, 255),
                  width=14)
        # zona roja
        for i in range(60):
            v = .78 + .22 * i / 59
            a = ang(v)
            p1 = (cx + (R - 10) * math.cos(a), cy - (R - 10) * math.sin(a))
            p2 = (cx + (R - 58) * math.cos(a), cy - (R - 58) * math.sin(a))
            d.line([p1, p2], fill=ROJO + (255,), width=12)
        for i in range(41):
            v = i / 40
            a = ang(v)
            lg = 46 if i % 5 == 0 else 22
            p1 = (cx + (R - 8) * math.cos(a), cy - (R - 8) * math.sin(a))
            p2 = (cx + (R - 8 - lg) * math.cos(a), cy - (R - 8 - lg) * math.sin(a))
            d.line([p1, p2], fill=BLANCO + (255,), width=7 if i % 5 == 0 else 3)
            if i % 5 == 0:
                n = texto_img(str(i // 5 * 2), 46, BLANCO, b=0)
                q = (cx + (R - 100) * math.cos(a), cy - (R - 100) * math.sin(a))
                im.alpha_composite(n, (int(q[0] - n.width / 2), int(q[1] - n.height / 2)))
        im.alpha_composite(rpm, (cx - rpm.width // 2, cy + 120))
        im.alpha_composite(l1, (cx - R + 40, cy + R - 150))
        im.alpha_composite(l2, (cx + R - l2.width - 20, cy + R - 150))
        # aguja: tiembla en CARRERA y, en la marca, se dispara a la zona roja y rebota
        if dt < t0:
            v = .28 + .03 * math.sin(dt * 13)
        else:
            k = (dt - t0) / .5
            v = .28 + (.97 - .28) * ease(min(1, k)) + (.02 * math.sin(dt * 40) if k >= 1 else 0)
        a = ang(v)
        tip = (cx + (R - 30) * math.cos(a), cy - (R - 30) * math.sin(a))
        bk = (cx - 60 * math.cos(a), cy + 60 * math.sin(a))
        perp = (math.sin(a) * 12, math.cos(a) * 12)
        d.polygon([(bk[0] + perp[0], bk[1] + perp[1]), tip, (bk[0] - perp[0], bk[1] - perp[1])], fill=(255, 70, 40, 255))
        d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], fill=(60, 60, 66, 255), outline=BLANCO + (255,), width=5)
        if dt >= t0 + .5:
            k2 = ease((dt - t0 - .5) / .3)
            g = Image.new("RGBA", im.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(g)
            gd.ellipse([cx - R - 40, cy - R - 40, cx + R + 40, cy + R + 40], outline=(255, 60, 30, int(200 * k2)), width=26)
            im = Image.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)), im)
        im.alpha_composite(tit, ((W - tit.width) // 2, 20))
        e = ease(dt / .35) * (1 - ease((dt - dur + .3) / .3))
        return _alfa(im, e)
    return fn


# ------------------------------------------------------------------ letrero de pueblo (gancho)
def cartel(arriba, grande, abajo):
    a1 = texto_img(arriba, 58, BLANCO, b=6)
    g = texto_img(grande, 210, AMAR, b=12)
    b1 = texto_img(abajo, 64, BLANCO, b=7)

    def fn(dt, dur, marcas):
        ww = max(a1.width, g.width, b1.width) + 40
        im = Image.new("RGBA", (ww, a1.height + g.height + b1.height + 10), (0, 0, 0, 0))
        k1, k2, k3 = ease(dt / .35), pop(dt - .25, .45) if dt > .25 else 0, ease((dt - .6) / .35)
        im.alpha_composite(_pil(a1, k1), ((ww - a1.width) // 2, 0))
        if k2 > 0:
            gg = g.resize((max(1, int(g.width * k2)), max(1, int(g.height * k2))), Image.LANCZOS)
            im.alpha_composite(gg, ((ww - gg.width) // 2, a1.height - 20 + (g.height - gg.height) // 2))
        im.alpha_composite(_pil(b1, k3), ((ww - b1.width) // 2, a1.height + g.height - 40))
        e = 1 - ease((dt - dur + .3) / .3)
        return _alfa(im, e)
    return fn


def _pil(im, k):
    a = np.array(im)
    a[:, :, 3] = (a[:, :, 3] * max(0., min(1., k))).astype(np.uint8)
    return Image.fromarray(a)


# ------------------------------------------------------------------ búsqueda tipo mapas (sin nombres de negocios)
def busqueda_mapa(texto="gorditas en Juchipila", n=6):
    """Barra de búsqueda blanca que se escribe sola + `n` pines rojos que caen sobre el clip del centro. Genérico: no nombra
    ni califica negocios. marcas[0] = cuando caen los pines."""
    barra_w, barra_h = 900, 120
    lupa = texto_img("⌕", 64, (90, 90, 90), b=0, nombre="seguisym.ttf", var=None)
    rng = np.random.default_rng(3)
    pts = [(int(rng.uniform(.15, .85) * W), int(rng.uniform(.40, .70) * H)) for _ in range(n)]

    def pin(k):
        r = 34
        im = Image.new("RGBA", (r * 2 + 8, int(r * 3.2)), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse([4, 4, 4 + r * 2, 4 + r * 2], fill=(219, 50, 54, 255), outline=(150, 20, 24, 255), width=3)
        d.polygon([(8, r + 14), (r * 2, r + 14), (r + 4, int(r * 3.1))], fill=(219, 50, 54, 255))
        d.ellipse([r - 8, r - 8, r + 16, r + 16], fill=(255, 255, 255, 255))
        return im

    P = pin(1)

    def fn(dt, dur, marcas):
        t0 = marcas[0] if marcas else .9
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        k = ease(dt / .35)
        y0 = int(.20 * H - (1 - k) * 60)
        d = ImageDraw.Draw(im)
        x0 = (W - barra_w) // 2
        d.rounded_rectangle([x0 + 6, y0 + 10, x0 + barra_w + 6, y0 + barra_h + 10], 60, fill=(0, 0, 0, int(90 * k)))
        d.rounded_rectangle([x0, y0, x0 + barra_w, y0 + barra_h], 60, fill=(255, 255, 255, int(255 * k)))
        im.alpha_composite(_pil(lupa, k), (x0 + 36, y0 + (barra_h - lupa.height) // 2))
        nch = int(len(texto) * max(0., min(1., (dt - .3) / .9)))
        if nch:
            tx = texto_img(texto[:nch] + ("|" if nch < len(texto) and int(dt * 4) % 2 else ""), 52, (40, 40, 40), b=0,
                           nombre="segoeui.ttf", var=None)
            im.alpha_composite(tx, (x0 + 120, y0 + (barra_h - tx.height) // 2))
        for i, (px, py) in enumerate(pts):
            u = dt - t0 - i * .16
            if u <= 0:
                continue
            c = ease(u / .3)
            yy = int(py - P.height - (1 - c) * 220)
            sombra = Image.new("RGBA", (60, 18), (0, 0, 0, 0))
            ImageDraw.Draw(sombra).ellipse([0, 0, 59, 17], fill=(0, 0, 0, int(110 * c)))
            im.alpha_composite(sombra, (px - 30, py - 9))
            im.alpha_composite(_pil(P, min(1, u / .12)), (px - P.width // 2, yy))
        e = 1 - ease((dt - dur + .3) / .3)
        return _alfa(im, e)
    return fn


# ------------------------------------------------------------------ comentario genérico de Facebook
def comentario(nombre="Tu negocio", texto="Aquí va tu puesto de comida o tu negocio", pie="Me gusta · Responder"):
    """Tarjeta GENÉRICA de comentario (sin nombres reales) que sube y late, con una flecha que apunta abajo."""
    nm = texto_img(nombre, 46, (20, 20, 20), b=0, nombre="segoeuib.ttf", var=None)
    tx = texto_img(texto, 40, (30, 30, 30), b=0, nombre="segoeui.ttf", var=None)
    pi = texto_img(pie, 30, (100, 100, 100), b=0, nombre="segoeuib.ttf", var=None)
    fl = texto_img("¡TU NEGOCIO AQUÍ!", 70, AMAR, b=7)
    cw = max(nm.width, tx.width) + 80
    ch = nm.height + tx.height + 70
    card = Image.new("RGBA", (cw + 150, ch + pi.height + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.ellipse([0, 6, 110, 116], fill=(190, 196, 206, 255))
    d.ellipse([33, 22, 77, 66], fill=(240, 242, 245, 255))
    d.pieslice([14, 70, 96, 150], 180, 360, fill=(240, 242, 245, 255))
    d.rounded_rectangle([130, 0, 130 + cw, ch], 34, fill=(240, 242, 245, 255))
    card.alpha_composite(nm, (170, 20))
    card.alpha_composite(tx, (170, 30 + nm.height))
    card.alpha_composite(pi, (170, ch + 12))
    m = ImageDraw.Draw(card)
    m.rectangle([0, 112, 112, 118], fill=(0, 0, 0, 0))

    def fn(dt, dur, marcas):
        ww = max(card.width, fl.width) + 20
        im = Image.new("RGBA", (ww, fl.height + card.height + 40), (0, 0, 0, 0))
        k = ease(dt / .4)
        late = 1 + .03 * math.sin(dt * 5) * (dt > .6)
        c2 = card.resize((max(1, int(card.width * late)), max(1, int(card.height * late))), Image.LANCZOS)
        im.alpha_composite(_pil(fl, ease((dt - .3) / .3)), ((ww - fl.width) // 2, 0))
        im.alpha_composite(_pil(c2, k), ((ww - c2.width) // 2, fl.height + 30 + int((1 - k) * 80)))
        e = 1 - ease((dt - dur + .3) / .3)
        return _alfa(im, e)
    return fn
