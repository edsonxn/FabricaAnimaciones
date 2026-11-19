# -*- coding: utf-8 -*-
"""Kit gráfico de los reels de «Noticias de Juchipila» (vertical 1080x1920), con los colores del logo de la página (marino,
crema, rojo de la antena). Página ANÓNIMA: este kit no se usa en los canales de la Fábrica ni copia el de ellos.
Cada función devuelve fn(dt, dur, marcas) -> BGRA para los FX `mg`/`pantalla` de nucleo/secuencia_fx.py.
  mapa_sierra()     OpenTopoMap real: de Juchipila a la Sierra de Morones, pin del pino azul con su foto real al lado.
  mapa_region()     OpenTopoMap real (z8): flecha de Juchipila al sur de Durango (≈190 km al NW, Acta Botánica Mexicana 2011).
  cifra(num, ...)   número gigante que cuenta hasta su valor, sobre panel marino.
  sello(txt, sub)   sello rojo de goma que cae girado (EN PELIGRO DE EXTINCIÓN).
  subtitulo(pal)    subtítulo grande con la palabra que suena resaltada (EXCEPCIÓN a R13 solo en esta página).
  credito(txt)      etiqueta chica de crédito.  cierre(...) tarjeta final con el logo.  logo_png() logo redondo para la esquina.
"""
import json, math, os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQ = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
MARINO, CREMA, ROJO, AMAR, NEGRO = (13, 24, 41), (241, 240, 230), (200, 35, 29), (255, 204, 0), (6, 10, 18)
LOGO = "E:/PaginaFace/paginas/noticias_jch/arte/PERFIL_logo.jpg"
_FD = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]
_fc = {}


def fuente(tam, peso="black"):
    nombres = {"black": ("Poppins-Black.ttf", "seguibl.ttf"), "bold": ("Poppins-ExtraBold.ttf", "segoeuib.ttf"),
               "semi": ("Poppins-SemiBold.ttf", "seguisb.ttf"), "reg": ("Poppins-Medium.ttf", "segoeui.ttf")}[peso]
    k = (tam, peso)
    if k not in _fc:
        ruta = next((os.path.join(c, n) for n in nombres for c in _FD if os.path.exists(os.path.join(c, n))))
        _fc[k] = ImageFont.truetype(ruta, tam)
    return _fc[k]


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def pop(x, d=.35):
    x = min(1.0, max(0.0, x / d))
    return 1 + 0.16 * math.sin(x * math.pi) * (1 - x) if x < 1 else 1.0


def a_bgra(im):
    a = np.array(im.convert("RGBA"))
    return np.ascontiguousarray(a[:, :, [2, 1, 0, 3]])


def texto(txt, tam, color=CREMA, borde=NEGRO, b=0, peso="black", sombra=True):
    f = fuente(tam, peso)
    x0, y0, x1, y1 = f.getbbox(txt)
    pad = b + 10
    im = Image.new("RGBA", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if sombra and not b:
        d.text((pad - x0 + max(2, tam // 28), pad - y0 + max(3, tam // 22)), txt, font=f, fill=(0, 0, 0, 170))
    d.text((pad - x0, pad - y0), txt, font=f, fill=color + (255,), stroke_width=b, stroke_fill=borde + (255,))
    return im


def _alfa(im, k):
    a = np.array(im)
    a[:, :, 3] = (a[:, :, 3] * max(0.0, min(1.0, k))).astype(np.uint8)
    return Image.fromarray(a)


def _merc(lat, lon, z, tx0, ty0):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return np.array([(x - tx0) * 256, (y - ty0) * 256])


def _foto_circulo(ruta, d, recorte=None):
    im = Image.open(ruta).convert("RGB")
    if recorte:
        w, h = im.size
        im = im.crop((int(recorte[0] * w), int(recorte[1] * h), int(recorte[2] * w), int(recorte[3] * h)))
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse([0, 0, d - 1, d - 1], fill=255)
    out = Image.new("RGBA", (d + 16, d + 16), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([0, 0, d + 15, d + 15], fill=CREMA + (255,))
    im.putalpha(m)
    out.alpha_composite(im, (8, 8))
    return out


def _base(nombre, oscuro=.22):
    meta = json.load(open(os.path.join(AQ, "mapas", nombre + "_meta.json")))
    base = cv2.imread(os.path.join(AQ, "mapas", nombre + ".png"))
    base = cv2.addWeighted(base, 1 - oscuro, np.full_like(base, (41, 24, 13)), oscuro, 0)
    return base, meta


def _banda(im, a, t1, t2):
    banda = Image.new("RGBA", (W, 420), (0, 0, 0, 0))
    bd = ImageDraw.Draw(banda)
    for i in range(420):
        bd.line([(0, i), (W, i)], fill=MARINO + (int(235 * (1 - i / 420) ** 1.3 * a),))
    im.alpha_composite(banda, (0, 0))
    im.alpha_composite(_alfa(t1, a), ((W - t1.width) // 2, 215))
    if t2:
        im.alpha_composite(_alfa(t2, a), ((W - t2.width) // 2, 215 + t1.height - 8))


def _camara(base, s, cx, cy):
    bh, bw = base.shape[:2]
    s = max(s, W / bw * 1.01, H / bh * 1.01)                 # nunca más lejos que la base (sin reflejos)
    cx = min(max(cx, W / 2 / s), bw - W / 2 / s)
    cy = min(max(cy, H / 2 / s), bh - H / 2 / s)
    M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
    f = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return f, (lambda p: p * s + (W / 2 - s * cx, H / 2 - s * cy))


def _punto(d, q, r, color=CREMA, borde=NEGRO):
    d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=color + (255,), outline=borde + (255,), width=5)


# ------------------------------------------------------------------ mapa de la sierra
PINO = (21.356671, -103.222565)          # GPS de las fotos de Commons (Sierra de Morones, Juchipila)
PUEBLO_VIEJO = (21.3426862, -103.1986744)  # OpenStreetMap (Nominatim)
JUCHIPILA = (21.4088, -103.1163)


def mapa_sierra(foto):
    c = {}

    def prep():
        base, meta = _base("sierra", .18)
        z, tx0, ty0 = meta["z"], meta["tx0"], meta["ty0"]
        c.update(base=base, pino=_merc(*PINO, z, tx0, ty0), pv=_merc(*PUEBLO_VIEJO, z, tx0, ty0),
                 jch=_merc(*JUCHIPILA, z, tx0, ty0), foto=_foto_circulo(foto, 300, (.1, .05, .85, .8)),
                 t1=texto("SIERRA DE MORONES", 84), t2=texto("MUNICIPIO DE JUCHIPILA", 50, AMAR, peso="bold"),
                 e_jch=texto("JUCHIPILA", 50, CREMA, b=6), e_pv=texto("Pueblo Viejo", 40, CREMA, b=5, peso="bold"),
                 e_pino=texto("PINO AZUL", 56, AMAR, b=7), e_cerro=texto("Cerro de Piñones", 40, CREMA, b=5, peso="bold"),
                 cred=texto("Mapa: © OpenStreetMap · OpenTopoMap (CC-BY-SA)", 24, CREMA, b=3, peso="semi"))

    def fn(dt, dur, marcas):
        if not c:
            prep()
        bh, bw = c["base"].shape[:2]
        # de encuadrar Juchipila y la sierra a acercarse al pin del pino
        a0 = (c["jch"] + c["pino"]) / 2
        s0 = min(W / (abs(c["jch"][0] - c["pino"][0]) + 520), H / (abs(c["jch"][1] - c["pino"][1]) + 900))
        s1 = s0 * 1.9
        t_ac = marcas[0] if marcas else dur * .35
        e = ease((dt - t_ac) / 1.6)
        s = s0 + (s1 - s0) * e
        cen = a0 + (c["pino"] + (0, 60) - a0) * e
        f, tp = _camara(c["base"], s, *cen)
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).convert("RGBA")
        d = ImageDraw.Draw(im)
        q = tp(c["jch"])
        _punto(d, q, 15)
        ej = c["e_jch"]
        lx = q[0] + 24 if q[0] + 24 + ej.width < W - 20 else q[0] - 24 - ej.width
        im.alpha_composite(ej, (int(lx), int(q[1] - ej.height / 2)))
        q = tp(c["pv"])
        _punto(d, q, 11)
        im.alpha_composite(c["e_pv"], (int(q[0] + 18), int(q[1] - 8)))
        # pin rojo que late + foto real
        q = tp(c["pino"])
        k = ease(dt / .6)
        rr = int((20 + 6 * math.sin(dt * 7)) * k)
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(halo).ellipse([q[0] - rr * 3, q[1] - rr * 3, q[0] + rr * 3, q[1] + rr * 3], fill=ROJO + (90,))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(14)))
        _punto(d, q, rr + 7, CREMA)
        _punto(d, q, rr, ROJO, ROJO)
        ep = c["e_pino"]
        im.alpha_composite(_alfa(ep, k), (int(q[0] - ep.width / 2), int(q[1] + 34)))
        ec = c["e_cerro"]
        im.alpha_composite(_alfa(ec, k), (int(q[0] - ec.width / 2), int(q[1] + 34 + ep.height - 10)))
        kf = ease((dt - t_ac - 1.0) / .5)
        if kf > 0:
            fo = c["foto"]
            sc = .6 + .4 * kf
            fo2 = fo.resize((int(fo.width * sc), int(fo.height * sc)), Image.LANCZOS)
            fx, fy = q[0] - fo2.width / 2, q[1] - fo2.height - 70
            d.line([(q[0], q[1] - rr - 7), (q[0], fy + fo2.height - 6)], fill=CREMA + (255,), width=6)
            im.alpha_composite(_alfa(fo2, kf), (int(fx), int(fy)))
        _banda(im, ease(dt / .5), c["t1"], c["t2"])
        im.alpha_composite(c["cred"], (24, H - 330))
        return a_bgra(im)
    return fn


# ------------------------------------------------------------------ mapa de la región (Durango)
def mapa_region():
    c = {}

    def prep():
        base, meta = _base("region", .38)
        g = cv2.cvtColor(cv2.cvtColor(base, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        base = cv2.addWeighted(base, .55, g, .45, 0)
        z, tx0, ty0 = meta["z"], meta["tx0"], meta["ty0"]
        p0 = _merc(*PINO, z, tx0, ty0)
        # 190 km al noroeste (rumbo 315°): Acta Botánica Mexicana (2011)
        dlat = 190 * math.cos(math.radians(45)) / 111.0
        dlon = -190 * math.sin(math.radians(45)) / (111.0 * math.cos(math.radians(PINO[0])))
        p1 = _merc(PINO[0] + dlat, PINO[1] + dlon, z, tx0, ty0)
        c.update(base=base, p0=p0, p1=p1, t1=texto("2010: OTRO BOSQUE", 84), t2=texto("EN EL SUR DE DURANGO", 50, AMAR, peso="bold"),
                 e0=texto("SIERRA DE MORONES", 44, CREMA, b=6), e1=texto("DURANGO", 54, AMAR, b=7),
                 e1b=texto("La Muralla, El Mezquital", 36, CREMA, b=5, peso="bold"),
                 km=texto("≈ 190 KM", 64, CREMA, b=8),
                 cred=texto("Mapa: © OpenStreetMap · OpenTopoMap (CC-BY-SA) · ubicación aproximada", 24, CREMA, b=3, peso="semi"))

    def fn(dt, dur, marcas):
        if not c:
            prep()
        cen = (c["p0"] + c["p1"]) / 2 + (0, 160)          # los puntos quedan arriba del subtítulo
        span = np.abs(c["p1"] - c["p0"])
        s = min(W / (span[0] + 620), H / (span[1] + 1100)) * (1 + .04 * dt / max(dur, 1))
        f, tp = _camara(c["base"], s, *cen)
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).convert("RGBA")
        d = ImageDraw.Draw(im)
        a, b = tp(c["p0"]), tp(c["p1"])
        prog = ease((dt - .4) / 1.4)
        if prog > 0:
            pts = [a + (b - a) * u for u in np.linspace(0, prog, 40)]
            for i in range(0, len(pts) - 1, 2):
                d.line([tuple(pts[i]), tuple(pts[i + 1])], fill=CREMA + (255,), width=9)
        _punto(d, a, 20, ROJO, CREMA)
        im.alpha_composite(c["e0"], (int(a[0] - c["e0"].width / 2), int(a[1] + 28)))
        if prog >= 1:
            k = ease((dt - 1.8) / .4)
            r = int(18 * pop(dt - 1.8, .4))
            _punto(d, b, r, AMAR)
            im.alpha_composite(_alfa(c["e1"], k), (int(b[0] - c["e1"].width / 2), int(b[1] - 30 - c["e1"].height - c["e1b"].height + 10)))
            im.alpha_composite(_alfa(c["e1b"], k), (int(b[0] - c["e1b"].width / 2), int(b[1] - 30 - c["e1b"].height)))
            m = (a + b) / 2
            im.alpha_composite(_alfa(c["km"], k), (int(m[0] + 30), int(m[1] - c["km"].height / 2)))
        _banda(im, ease(dt / .5), c["t1"], c["t2"])
        im.alpha_composite(c["cred"], (24, H - 330))
        return a_bgra(im)
    return fn


# ------------------------------------------------------------------ cifra gigante
def cifra(num, etiqueta, sub=None, desde=0, color=AMAR, miles=True):
    lab = texto(etiqueta, 76, CREMA)
    sb = texto(sub, 46, CREMA, peso="semi") if sub else None

    def fn(dt, dur, marcas):
        k = ease(dt / max(.6, min(1.3, dur * .4)))
        v = int(round(desde + (num - desde) * k))
        s = f"{v:,}".replace(",", " ") if miles else str(v)
        n = texto(s, 250, color if k < 1 else CREMA)
        sc = pop(dt - 1.3, .4) if dt > 1.3 else 1.0
        n = n.resize((int(n.width * sc), int(n.height * sc)), Image.LANCZOS)
        ww = max(n.width, lab.width, sb.width if sb else 0) + 80
        hh = n.height + lab.height + (sb.height if sb else 0) + 30
        im = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 30, ww - 1, hh - 1], 40, fill=MARINO + (200,))
        d.rectangle([40, n.height + 2, ww - 40, n.height + 10], fill=ROJO + (255,))
        im.alpha_composite(n, ((ww - n.width) // 2, 0))
        im.alpha_composite(lab, ((ww - lab.width) // 2, n.height + 4))
        if sb:
            im.alpha_composite(sb, ((ww - sb.width) // 2, n.height + lab.height - 6))
        e = ease(dt / .25) * (1 - ease((dt - dur + .25) / .25))
        return a_bgra(_alfa(im, e))
    return fn


# ------------------------------------------------------------------ sello de peligro
def sello(t1, t2, color=ROJO, ang=-8):
    a = texto(t1, 92, color, sombra=False)
    b = texto(t2, 40, color, peso="bold", sombra=False)
    ww, hh = max(a.width, b.width) + 80, a.height + b.height + 60
    base = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([0, 0, ww - 1, hh - 1], 26, fill=CREMA + (225,), outline=color + (255,), width=12)
    d.rounded_rectangle([18, 18, ww - 19, hh - 19], 18, outline=color + (255,), width=4)
    base.alpha_composite(a, ((ww - a.width) // 2, 24))
    base.alpha_composite(b, ((ww - b.width) // 2, 20 + a.height))
    rng = np.random.default_rng(3)                            # textura de goma: huecos sin tinta
    m = np.array(base)
    ruido = rng.random(m.shape[:2]) < .05
    m[ruido & (m[:, :, 3] > 0), 3] = (m[ruido & (m[:, :, 3] > 0), 3] * .45).astype(np.uint8)
    base = Image.fromarray(m).rotate(ang, expand=True, resample=Image.BICUBIC)

    def fn(dt, dur, marcas):
        sc = 1.8 - .8 * ease(dt / .22)
        im = base.resize((int(base.width * sc), int(base.height * sc)), Image.LANCZOS)
        e = ease(dt / .12) * (1 - ease((dt - dur + .25) / .25))
        return a_bgra(_alfa(im, e))
    return fn


# ------------------------------------------------------------------ subtítulos (excepción R13 solo en esta página)
def subtitulo(palabras, tam=74, ancho=960):
    """palabras = [(texto, s, e)] relativas al inicio del grupo; la que suena va en amarillo."""
    f = fuente(tam, "black")
    esp = f.getlength(" ")
    lineas, actual, w = [], [], 0
    for p in palabras:
        lw = f.getlength(p[0])
        if actual and w + esp + lw > ancho - 60:
            lineas.append(actual)
            actual, w = [], 0
        actual.append(p)
        w += (esp if len(actual) > 1 else 0) + lw
    if actual:
        lineas.append(actual)
    alto_l = int(tam * 1.22)
    hh = alto_l * len(lineas) + 34
    anchos = [sum(f.getlength(p[0]) for p in l) + esp * (len(l) - 1) for l in lineas]
    ww = int(max(anchos)) + 70

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, ww - 1, hh - 1], 28, fill=(6, 12, 24, 175))
        y = 14
        for l, lw in zip(lineas, anchos):
            x = (ww - lw) / 2
            for txt, s, e in l:
                col = AMAR if s - .05 <= dt < e + .12 else CREMA
                d.text((x, y), txt, font=f, fill=col + (255,), stroke_width=4, stroke_fill=NEGRO + (255,))
                x += f.getlength(txt) + esp
            y += alto_l
        e = ease(dt / .12)
        return a_bgra(_alfa(im, e))
    return fn


# ------------------------------------------------------------------ crédito
def credito(txt):
    t = texto(txt, 26, CREMA, peso="semi", sombra=False)
    im = Image.new("RGBA", (t.width + 20, t.height + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 12, fill=(0, 0, 0, 150))
    im.alpha_composite(t, (10, 2))
    arr = a_bgra(im)
    return lambda dt, dur, marcas: arr


# ------------------------------------------------------------------ logo
def logo_png(ruta_salida, d=170):
    im = Image.open(LOGO).convert("RGB")
    w, h = im.size
    m = int(w * .035)
    im = im.crop((m, m, w - m, h - m)).resize((d, d), Image.LANCZOS)
    mk = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(mk).ellipse([0, 0, d * 4 - 1, d * 4 - 1], fill=255)
    im.putalpha(mk.resize((d, d), Image.LANCZOS))
    out = Image.new("RGBA", (d + 12, d + 12), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([4, 8, d + 8, d + 12], fill=(0, 0, 0, 120))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    out.alpha_composite(im, (6, 4))
    out.save(ruta_salida)
    return ruta_salida


# ------------------------------------------------------------------ tarjeta de cierre
def cierre(pregunta, fuentes):
    lg = Image.open(LOGO).convert("RGB").resize((560, 560), Image.LANCZOS)
    mk = Image.new("L", (560, 560), 0)
    ImageDraw.Draw(mk).ellipse([0, 0, 559, 559], fill=255)
    lg.putalpha(mk)
    q = [texto(l, 84, AMAR) for l in pregunta.split(" / ")]
    q2 = texto("Cuéntenos en los comentarios", 46, CREMA, peso="bold")
    lema = texto("Lo que pasa en el cañón, primero y verificado", 36, CREMA, peso="semi")
    fu = [texto(l, 28, (190, 198, 212), peso="reg", sombra=False) for l in fuentes]

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (W, H), MARINO + (255,))
        d = ImageDraw.Draw(im)
        for r in range(900, 0, -30):                          # resplandor suave al centro
            d.ellipse([W / 2 - r, 700 - r, W / 2 + r, 700 + r], fill=(13 + (900 - r) // 40, 24 + (900 - r) // 30, 41 + (900 - r) // 22, 255))
        k = ease(dt / .5)
        sc = .85 + .15 * ease(dt / .7)
        l2 = lg.resize((int(560 * sc), int(560 * sc)), Image.LANCZOS)
        im.alpha_composite(_alfa(l2, k), ((W - l2.width) // 2, int(560 - l2.height / 2)))
        im.alpha_composite(_alfa(lema, k), ((W - lema.width) // 2, 880))
        y = 1010
        kq = ease((dt - .5) / .4)
        for t in q:
            im.alpha_composite(_alfa(t, kq), ((W - t.width) // 2, y))
            y += t.height - 10
        im.alpha_composite(_alfa(q2, kq), ((W - q2.width) // 2, y + 10))
        y = 1560
        for t in fu:
            im.alpha_composite(_alfa(t, k), ((W - t.width) // 2, y))
            y += t.height - 6
        return a_bgra(im)
    return fn


def comparativa(filas, titulo):
    """filas = [(lugar, cifra_txt, valor, color)]; barras que crecen una tras otra (valor relativo al mayor)."""
    tt = texto(titulo, 54, CREMA, peso="bold")
    fl = [(texto(l, 50, CREMA, peso="black"), texto(c, 50, col, peso="black"), v, col) for l, c, v, col in filas]
    vmax = max(v for _, _, v, _ in filas)
    ww = 960

    def fn(dt, dur, marcas):
        hh = 60 + tt.height + sum(a.height + 70 for a, _, _, _ in fl) + 20
        im = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, ww - 1, hh - 1], 34, fill=MARINO + (215,), outline=CREMA + (255,), width=3)
        im.alpha_composite(tt, ((ww - tt.width) // 2, 24))
        y = 40 + tt.height
        for i, (a, c, v, col) in enumerate(fl):
            k = ease((dt - .25 - i * .55) / .8)
            im.alpha_composite(a, (40, y))
            im.alpha_composite(_alfa(c, k), (ww - 40 - c.width, y))
            yb = y + a.height + 4
            d.rounded_rectangle([40, yb, ww - 40, yb + 34], 17, fill=(255, 255, 255, 40))
            if k > 0:
                d.rounded_rectangle([40, yb, 40 + max(34, (ww - 80) * v / vmax * k), yb + 34], 17, fill=col + (255,))
            y += a.height + 70
        e = ease(dt / .3) * (1 - ease((dt - dur + .25) / .25))
        return a_bgra(_alfa(im, e))
    return fn


def hoja(fn, dur, marcas, salida, n=6, fondo=90):
    cuadros = []
    for i in range(n):
        dt = dur * (i + .5) / n
        a = fn(dt, dur, marcas)
        f = np.full((H, W, 3), fondo, np.uint8)
        h, w = a.shape[:2]
        x, y = max(0, (W - w) // 2), max(0, (H - h) // 2)
        sub = a[:min(h, H), :min(w, W)]
        al = sub[:, :, 3:4] / 255.0
        roi = f[y:y + sub.shape[0], x:x + sub.shape[1]]
        f[y:y + sub.shape[0], x:x + sub.shape[1]] = (roi * (1 - al) + sub[:, :, :3] * al).astype(np.uint8)
        cuadros.append(cv2.resize(f, (360, 640)))
    cv2.imwrite(salida, np.hstack(cuadros))
