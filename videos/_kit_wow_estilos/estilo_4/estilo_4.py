# -*- coding: utf-8 -*-
"""ESTILO 4 · TÁCTICO PLANO (infografía) — kit visual de Crónicas de Warcraft (22-nov-2026).

Diseño plano moderno: colores sólidos con acentos, mapa simplificado a manchas planas dentro de una tarjeta con
sombra suave, ruta = línea gruesa con flecha y distancia, marcadores = pines geométricos numerados que caen y
rebotan, fichas tipo tarjeta, contadores grandes (anillo segmentado), tipografía sans negrita (Segoe UI Black +
Bahnschrift). Todo por código, cuadro a cuadro.

Funciones reutilizables (para pasarlas al kit si se elige):
    mapa_ruta(lienzo, t, cfg)   mapa plano + pines + ruta con flecha y distancia + foto + panel lateral
    ficha(lienzo, t, cfg)       tarjeta con título, íconos que entran uno a uno con «×N» y anillo contador
    tarjeta(lienzo, t, cfg)     tarjeta de jefe: foto, etiqueta, nombre, línea y barra segmentada
    rotulo(lienzo, t, cfg)      rótulo inferior (lower third) con sello numérico
    transicion(lienzo, t, tc)   barrido plano de color (cubre y destapa) centrado en tc
Cada una recibe t = tiempo LOCAL (s desde que empieza su pieza) y dibuja sobre `lienzo` (PIL RGBA 1920x1080).

Uso:  python estilo_4.py              render completo -> estilo_4_tactico.mp4 + hoja.jpg
      python estilo_4.py --cuadro 7.5 un cuadro suelto -> _cuadro_7.5.png (para revisar)
      python estilo_4.py --hoja       solo la hoja de revisión del mp4 existente
"""
import os, sys, math, subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\FabricaAnimaciones\videos\wow_errores_60"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
W, H, FPS, DUR = 1920, 1080, 30, 30.0
SALIDA = os.path.join(AQUI, "estilo_4_tactico.mp4")

# ------------------------------------------------------------------ paleta (plana, acentos por facción/uso)
C = dict(
    fondo=(13, 21, 36), panel=(25, 37, 61), panel2=(34, 50, 80), blanco=(247, 248, 251), tinta=(18, 26, 42),
    gris=(112, 124, 145), gris_cl=(232, 236, 242), ambar=(255, 183, 3), azul=(58, 134, 255), rojo=(232, 62, 92),
    verde=(6, 196, 146), amarillo=(240, 176, 0),
    # acentos por facción (para reutilizar en el kit)
    alianza=(47, 111, 222), horda=(206, 48, 48), neutral=(255, 183, 3),
)

# ------------------------------------------------------------------ tipografías
_FUENTES = {}
def fuente(nombre, tam, var=None):
    k = (nombre, tam, var)
    if k not in _FUENTES:
        rutas = {"black": "seguibl.ttf", "bold": "segoeuib.ttf", "semi": "seguisb.ttf", "bahn": "bahnschrift.ttf"}
        f = ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", rutas[nombre]), tam)
        if var:
            f.set_variation_by_name(var)
        _FUENTES[k] = f
    return _FUENTES[k]

def F_TIT(t): return fuente("black", t)
def F_NUM(t): return fuente("bahn", t, "Bold")
def F_ROT(t): return fuente("bahn", t, "Bold Condensed")
def F_TXT(t): return fuente("bahn", t, "SemiBold")

# ------------------------------------------------------------------ easing
def cl(x): return 0.0 if x < 0 else 1.0 if x > 1 else x
def seg(t, a, b): return cl((t - a) / (b - a))
def eo(u): u = cl(u); return 1 - (1 - u) ** 3
def ei(u): u = cl(u); return u * u
def eio(u):
    u = cl(u)
    return 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2
def eob(u, s=1.9):
    u = cl(u)
    return 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2

# ------------------------------------------------------------------ utilidades de composición
def con_alfa(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im

def pegar(lienzo, im, x, y, a=1.0):
    """alpha_composite con recorte (x, y pueden ser negativos o salirse)."""
    if a <= 0.001:
        return
    x, y = int(round(x)), int(round(y))
    w, h = im.size
    x0, y0, x1, y1 = max(0, x), max(0, y), min(lienzo.width, x + w), min(lienzo.height, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    if (x0, y0, x1, y1) != (x, y, x + w, y + h):
        im = im.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    lienzo.alpha_composite(con_alfa(im, a), (x0, y0))

def escalar(im, s):
    if abs(s - 1) < 0.003:
        return im
    w, h = max(1, int(im.width * s)), max(1, int(im.height * s))
    return im.resize((w, h), Image.BICUBIC)

_SOMBRAS = {}
def sombra(w, h, r, rad=22, alfa=110, dy=14):
    """Sombra suave para una tarjeta w x h de esquinas r. Devuelve (img, margen)."""
    k = (w, h, r, rad, alfa, dy)
    if k not in _SOMBRAS:
        m = rad * 2
        im = Image.new("L", (w + 2 * m, h + 2 * m), 0)
        ImageDraw.Draw(im).rounded_rectangle([m, m + dy, m + w, m + h + dy], r, fill=alfa)
        im = im.filter(ImageFilter.GaussianBlur(rad))
        s = Image.new("RGBA", im.size, (0, 0, 0, 0))
        s.putalpha(im)
        _SOMBRAS[k] = (s, m)
    return _SOMBRAS[k]

def caja(w, h, r, color, sombra_=True):
    """Tarjeta plana con sombra suave. Devuelve (img, margen) — el contenido va en (margen, margen)."""
    if sombra_:
        s, m = sombra(w, h, r)
        im = s.copy()
    else:
        m = 0
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([m, m, m + w - 1, m + h - 1], r, fill=color + (255,))
    return im, m

def mascara_redonda(w, h, r, ss=3):
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], r * ss, fill=255)
    return m.resize((w, h), Image.LANCZOS)

def ancho_txt(s, f):
    b = f.getbbox(s)
    return b[2] - b[0]

def texto(d, xy, s, f, color, ancla="la"):
    d.text(xy, s, font=f, fill=color, anchor=ancla)

def imagen_cubre(ruta, w, h, r=0):
    im = Image.open(ruta).convert("RGBA")
    s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((x, y, x + w, y + h))
    if r:
        im.putalpha(mascara_redonda(w, h, r))
    return im

# ------------------------------------------------------------------ piezas planas reutilizables
_CACHE = {}
def pin(num, color, r=30):
    """Pin geométrico: cabeza circular con número + punta triangular, borde blanco. Devuelve (img, ancla_x, ancla_y)."""
    k = ("pin", num, color, r)
    if k in _CACHE:
        return _CACHE[k]
    S = 4
    borde = 6
    w = (2 * r + 2 * borde + 8) * S
    h = (2 * r + 2 * borde + 40) * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = w / 2, (r + borde + 4) * S
    tip = h - 4 * S
    def forma(rr, col):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
        ang = math.radians(38)
        d.polygon([(cx - rr * math.sin(ang), cy + rr * math.cos(ang)), (cx + rr * math.sin(ang), cy + rr * math.cos(ang)),
                   (cx, tip - (borde * S if rr < (r + borde) * S else 0))], fill=col)
    forma((r + borde) * S, C["blanco"] + (255,))
    forma(r * S, color + (255,))
    texto(d, (cx, cy + 2 * S), str(num), F_NUM(int(r * 1.25) * S), C["blanco"], "mm")
    im = im.resize((w // S, h // S), Image.LANCZOS)
    res = (im, w / S / 2, tip / S)
    _CACHE[k] = res
    return res

def etiqueta(txt, acento, insignia=None, sub=None, tam=36):
    """Etiqueta plana blanca con barra de acento a la izquierda; insignia de color opcional a la derecha."""
    k = ("tag", txt, acento, insignia, sub, tam)
    if k in _CACHE:
        return _CACHE[k]
    f = F_ROT(tam)
    fs = F_TXT(int(tam * 0.62))
    pad = 18
    wt = ancho_txt(txt, f)
    wi = ancho_txt(insignia, F_NUM(int(tam * 0.8))) + 28 if insignia else 0
    ws = ancho_txt(sub, fs) if sub else 0
    w = 12 + pad + max(wt + (wi + 14 if insignia else 0), ws) + pad
    h = int(tam * 1.55) + (int(tam * 0.75) if sub else 0)
    im, m = caja(w, h, 10, C["blanco"])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([m, m, m + 22, m + h - 1], 10, fill=acento + (255,))
    d.rectangle([m + 12, m, m + 22, m + h - 1], fill=C["blanco"] + (255,))
    y1 = m + int(tam * 0.78)
    texto(d, (m + 12 + pad, y1), txt, f, C["tinta"], "lm")
    if insignia:
        x0 = m + 12 + pad + wt + 14
        fi = F_NUM(int(tam * 0.8))
        d.rounded_rectangle([x0, y1 - tam * 0.52, x0 + wi, y1 + tam * 0.52], int(tam * 0.3), fill=acento + (255,))
        texto(d, (x0 + wi / 2, y1 + 1), insignia, fi, C["blanco"], "mm")
    if sub:
        texto(d, (m + 12 + pad, y1 + int(tam * 0.95)), sub, fs, C["gris"], "lm")
    res = (im, m)
    _CACHE[k] = res
    return res

def revelar_izq(im, u):
    """Recorta la imagen de izquierda a derecha (revelado por ancho)."""
    if u >= 0.999:
        return im
    w = max(1, int(im.width * u))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im.crop((0, 0, w, im.height)), (0, 0))
    return out

def foto_tarjeta(ruta, w, h, borde=8):
    k = ("foto", ruta, w, h)
    if k not in _CACHE:
        im, m = caja(w + 2 * borde, h + 2 * borde, 16, C["blanco"])
        im.alpha_composite(imagen_cubre(ruta, w, h, 10), (m + borde, m + borde))
        _CACHE[k] = (im, m)
    return _CACHE[k]

def fondo_plano(color=C["fondo"], puntos=True):
    k = ("fondo", color, puntos)
    if k not in _CACHE:
        im = Image.new("RGBA", (W, H), color + (255,))
        if puntos:
            d = ImageDraw.Draw(im)
            c2 = tuple(min(255, v + 12) for v in color) + (255,)
            for y in range(20, H, 40):
                for x in range(20, W, 40):
                    d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=c2)
        _CACHE[k] = im
    return _CACHE[k].copy()

def etiqueta_estilo(lienzo, txt="ESTILO 4 · TÁCTICO PLANO"):
    k = ("etq", txt)
    if k not in _CACHE:
        f = F_ROT(26)
        w = ancho_txt(txt, f) + 64
        im = Image.new("RGBA", (w, 46), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, 45], 23, fill=C["fondo"] + (200,))
        d.ellipse([18, 16, 32, 30], fill=C["ambar"] + (255,))
        texto(d, (44, 23), txt, f, C["blanco"] + (230,), "lm")
        _CACHE[k] = im
    pegar(lienzo, _CACHE[k], 36, 32)

# ------------------------------------------------------------------ mapa plano
def mapa_plano(ruta, escala=2):
    """Simplifica el mapa a manchas de color sólido por categoría (selva, roca, desierto, arena, agua, sombras, cristales)
    con la paleta plana. Se trabaja a 2x para que los contornos queden limpios al acercar. Devuelve (bgr, escala)."""
    cache = os.path.join(AQUI, "_mapa_plano_" + os.path.splitext(os.path.basename(ruta))[0] + ".png")
    if os.path.exists(cache) and os.path.getmtime(cache) >= max(os.path.getmtime(ruta), os.path.getmtime(__file__)):
        return cv2.imread(cache), escala
    m = cv2.imread(ruta)
    m = cv2.resize(m, None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)
    f = cv2.pyrMeanShiftFiltering(m, 18, 30)
    f = cv2.GaussianBlur(f, (0, 0), 2.0)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.int32)
    Hh, Ss, Vv = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    def bgr(h): return tuple(int(h[i:i + 2], 16) for i in (5, 3, 1))
    roca = [bgr("#3b4038"), bgr("#585c4c"), bgr("#7c7d66"), bgr("#a3a185")]
    verde = [bgr("#2c5a3c"), bgr("#3f7a4a"), bgr("#62a05a"), bgr("#94c174")]
    naranja = [bgr("#b8642c"), bgr("#d98b3a"), bgr("#efb063")]
    def nivel(v, n, lo, hi): return np.clip(((v - lo) / (hi - lo) * n).astype(int), 0, n - 1)
    osc = Vv < 42
    agua = (Hh >= 85) & (Hh <= 130) & (Ss > 60) & ~osc
    rosa = ((Hh >= 150) | (Hh <= 3)) & (Ss > 90) & (Vv > 110)
    nar = (Hh >= 4) & (Hh <= 21) & (Ss > 120) & (Vv > 110) & ~rosa
    crema = (Ss < 60) & (Vv > 165)
    selva = (Hh >= 26) & (Hh <= 84) & (Ss > 95) & ~osc
    out = np.zeros_like(f)
    for lv, col in enumerate(roca):
        out[nivel(Vv, 4, 40, 230) == lv] = col
    for lv, col in enumerate(verde):
        out[selva & (nivel(Vv, 4, 50, 210) == lv)] = col
    for lv, col in enumerate(naranja):
        out[nar & (nivel(Vv, 3, 110, 240) == lv)] = col
    out[crema] = bgr("#eadfc4"); out[agua] = bgr("#3f8fd0"); out[osc] = bgr("#1b2426"); out[rosa] = bgr("#e9708e")
    out = cv2.medianBlur(out, 13)
    cv2.imwrite(cache, out)
    return out, escala

# ------------------------------------------------------------------ ruta (bezier) y dibujo AA sobre numpy
def bezier(p0, p1, p2, n=120):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)

def polilinea(arr, pts, color, grosor):
    p = np.round(pts * 4).astype(np.int32).reshape(-1, 1, 2)
    cv2.polylines(arr, [p], False, color, grosor, cv2.LINE_AA, shift=2)
    for q in (pts[0], pts[-1]):
        cv2.circle(arr, (int(q[0] * 4), int(q[1] * 4)), int(grosor / 2 * 4), color, -1, cv2.LINE_AA, shift=2)

def flecha(arr, punta, ang, tam, color):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(punta[0] + ca * tam * 0.55, punta[1] + sa * tam * 0.55),
           (punta[0] - ca * tam * 0.6 - sa * tam * 0.62, punta[1] - sa * tam * 0.6 + ca * tam * 0.62),
           (punta[0] - ca * tam * 0.6 + sa * tam * 0.62, punta[1] - sa * tam * 0.6 - ca * tam * 0.62)]
    cv2.fillPoly(arr, [np.round(np.array(pts) * 4).astype(np.int32)], color, cv2.LINE_AA, shift=2)

# ================================================================== 1 · MAPA CON RUTA
CFG_MAPA = dict(
    mapa=os.path.join(BASE, "mapas", "ungoro_norte.jpg"),
    tarjeta=(90, 150, 1180, 860),                   # x, y, w, h de la tarjeta del mapa
    cam_ini=(800, 650, 1600), cam_fin=(761.6, 233, 640), cam_deriva=600,   # (cx, cy, ancho) en px del mapa
    p1=(43.6, 23.0), p2=(47.3, 10.8),              # % de la imagen (ver _coords.md)
    control=(-4.5, 0.5),                           # desvío del punto de control de la curva (% de imagen)
    n1="REFUGIO DE LOS MARISCALES", s1="inicio · vuelo (Gryfe)",
    n2="BANCAL DEL CREADOR", i2="58-60", s2="destino · nivel 58-60",
    foto=os.path.join(BASE, "pegatinas", "bancal_creador.png"),
    zona=("CRÁTER DE", "UN'GORO"), region="KALIMDOR",
    distancia=375, unidad="yd", nota_dist="en línea recta",
    # tiempos (s locales)
    t_pin1=2.6, t_ruta=(3.6, 6.8), t_pin2=6.9, t_foto=7.3,
)

def mapa_ruta(lienzo, t, cfg=CFG_MAPA, salida=None):
    tx, ty, tw, th = cfg["tarjeta"]
    if ("mapa", cfg["mapa"]) not in _CACHE:
        _CACHE[("mapa", cfg["mapa"])] = mapa_plano(cfg["mapa"])
    plano, esc = _CACHE[("mapa", cfg["mapa"])]
    mh, mw = plano.shape[:2]
    # cámara: acercamiento con easing + deriva lenta
    u = eio(seg(t, 0.6, 3.2))
    cx = cfg["cam_ini"][0] + (cfg["cam_fin"][0] - cfg["cam_ini"][0]) * u
    cy = cfg["cam_ini"][1] + (cfg["cam_fin"][1] - cfg["cam_ini"][1]) * u
    cw = cfg["cam_ini"][2] + (cfg["cam_fin"][2] - cfg["cam_ini"][2]) * u
    cw += (cfg["cam_deriva"] - cfg["cam_fin"][2]) * eio(seg(t, 3.2, 11.0))
    cx, cy, cw = cx * esc, cy * esc, cw * esc        # la cámara se da en px del mapa original
    s = tw / cw
    M = np.float32([[s, 0, tw / 2 - cx * s], [0, s, th / 2 - cy * s]])
    arr = cv2.warpAffine(plano, M, (tw, th), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    def a_tarjeta(p):
        return (p[0] / 100 * mw * s + M[0, 2], p[1] / 100 * mh * s + M[1, 2])
    P1, P2 = a_tarjeta(cfg["p1"]), a_tarjeta(cfg["p2"])
    pc = ((cfg["p1"][0] + cfg["p2"][0]) / 2 + cfg["control"][0], (cfg["p1"][1] + cfg["p2"][1]) / 2 + cfg["control"][1])
    PC = a_tarjeta(pc)
    curva = bezier(P1, PC, P2, 160)
    # ruta: casco oscuro + línea ámbar + flecha que viaja en la punta
    ur = eio(seg(t, *cfg["t_ruta"]))
    if ur > 0:
        n = max(2, int(len(curva) * ur))
        parte = curva[:n]
        polilinea(arr, parte, C["tinta"], 26)
        polilinea(arr, parte, C["ambar"], 15)
        if n >= 3:
            d = parte[-1] - parte[-4 if n > 4 else 0]
            ang = math.atan2(d[1], d[0])
            fin = parte[-1] if ur < 1 else curva[-1] - (curva[-1] - curva[-8]) * 0.0
            if ur < 1 or t < cfg["t_pin2"] + 0.1:
                flecha(arr, (fin[0], fin[1]), ang, 52, C["tinta"])
                flecha(arr, (fin[0], fin[1]), ang, 36, C["ambar"])
    # anillos planos que pulsan en el suelo bajo cada pin
    for P, t0, col in ((P1, cfg["t_pin1"] + 0.35, C["azul"]), (P2, cfg["t_pin2"] + 0.35, C["rojo"])):
        if t > t0:
            for k in range(2):
                f = ((t - t0) / 1.6 + k * 0.5) % 1.0
                rr = 14 + 70 * eo(f)
                a = (1 - f) * 0.9
                capa = arr.copy()
                cv2.ellipse(capa, (int(P[0] * 4), int(P[1] * 4)), (int(rr * 4), int(rr * 0.42 * 4)), 0, 0, 360, col, 4,
                            cv2.LINE_AA, shift=2)
                arr = cv2.addWeighted(capa, a, arr, 1 - a, 0)
    tarj = Image.fromarray(arr).convert("RGBA")
    # pines (caen, aplastan, rebotan) + sombra en el suelo
    for P, t0, num, col in ((P1, cfg["t_pin1"], 1, C["azul"]), (P2, cfg["t_pin2"], 2, C["rojo"])):
        if t < t0:
            continue
        u1 = seg(t, t0, t0 + 0.32)
        u2 = seg(t, t0 + 0.32, t0 + 0.62)
        dy = -260 * (1 - ei(u1))
        sq = math.sin(math.pi * u2) * 0.22 if u1 >= 1 else 0
        im, ax, ay = pin(num, col)
        im = im.resize((int(im.width * (1 + sq * 0.6)), int(im.height * (1 - sq))), Image.BICUBIC)
        ax, ay = ax * (1 + sq * 0.6), ay * (1 - sq)
        sh = Image.new("RGBA", (90, 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([15, 12, 75, 28], fill=(0, 0, 0, int(120 * u1)))
        sh = sh.filter(ImageFilter.GaussianBlur(3))
        pegar(tarj, sh, P[0] - 45, P[1] - 20)
        pegar(tarj, im, P[0] - ax, P[1] - ay + dy)
    # brújula plana arriba a la derecha
    br = _CACHE.get("brujula")
    if br is None:
        S = 4
        br = Image.new("RGBA", (84 * S, 84 * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(br)
        d.ellipse([0, 0, 84 * S - 1, 84 * S - 1], fill=C["blanco"] + (235,))
        d.polygon([(42 * S, 12 * S), (54 * S, 50 * S), (42 * S, 43 * S), (30 * S, 50 * S)], fill=C["rojo"] + (255,))
        texto(d, (42 * S, 66 * S), "N", F_NUM(18 * S), C["tinta"], "mm")
        br = br.resize((84, 84), Image.LANCZOS)
        _CACHE["brujula"] = br
    pegar(tarj, br, tw - 112, 28)
    # máscara redonda + sombra + entrada (sube y aparece)
    if ("masc", tw, th) not in _CACHE:
        _CACHE[("masc", tw, th)] = mascara_redonda(tw, th, 26)
    tarj.putalpha(_CACHE[("masc", tw, th)])
    ue = eo(seg(t, 0.0, 0.8))
    oy = (1 - ue) * 90
    if salida is not None:
        oy += -0 * salida
    sh, m = sombra(tw, th, 26)
    pegar(lienzo, sh, tx - m, ty - m + oy, ue)
    pegar(lienzo, tarj, tx, ty + oy, ue)
    ox, oy2 = tx, ty + oy
    # etiqueta del pin 1
    if t > cfg["t_pin1"] + 0.4:
        u = eo(seg(t, cfg["t_pin1"] + 0.4, cfg["t_pin1"] + 0.85))
        im, m = etiqueta(cfg["n1"], C["azul"], sub=cfg["s1"], tam=34)
        pegar(lienzo, revelar_izq(im, u), ox + P1[0] + 34 - m + (1 - u) * -20, oy2 + P1[1] - 64 - m, ue)
    # foto + etiqueta del pin 2
    if t > cfg["t_foto"]:
        u = eob(seg(t, cfg["t_foto"], cfg["t_foto"] + 0.5))
        fw, fh = 360, 202
        im, m = foto_tarjeta(cfg["foto"], fw, fh)
        ims = escalar(im, max(0.05, 0.25 + 0.75 * u))
        # crece desde el pin hacia su sitio
        fx, fy = ox + P2[0] + 56, oy2 + P2[1] - 150
        k = cl(u)
        px = (ox + P2[0]) * (1 - k) + (fx + (fw + 16) / 2) * k
        py = (oy2 + P2[1] - 40) * (1 - k) + (fy + (fh + 16) / 2) * k
        pegar(lienzo, ims, px - ims.width / 2, py - ims.height / 2, cl(seg(t, cfg["t_foto"], cfg["t_foto"] + 0.2)) * ue)
        # línea guía pin -> foto
    if t > cfg["t_foto"] + 0.35:
        u = eo(seg(t, cfg["t_foto"] + 0.35, cfg["t_foto"] + 0.8))
        im, m = etiqueta(cfg["n2"], C["rojo"], insignia=cfg["i2"], tam=34)
        pegar(lienzo, revelar_izq(im, u), ox + P2[0] + 56 - m + (1 - u) * -20, oy2 + P2[1] + 78 - m, ue)
    # distancia sobre la ruta
    if t > cfg["t_ruta"][1] - 0.3:
        u = eob(seg(t, cfg["t_ruta"][1] - 0.3, cfg["t_ruta"][1] + 0.15))
        mid = curva[len(curva) // 2]
        im = _pastilla_dist(cfg)
        ims = escalar(im, max(0.05, u))
        pegar(lienzo, ims, ox + mid[0] - ims.width - 26 * u, oy2 + mid[1] - ims.height / 2,
              cl(seg(t, cfg["t_ruta"][1] - 0.3, cfg["t_ruta"][1] - 0.1)))
    _panel_mapa(lienzo, t, cfg, ur)

def _pastilla_dist(cfg):
    k = ("dist", cfg["distancia"], cfg["unidad"])
    if k not in _CACHE:
        txt = f"{cfg['distancia']} {cfg['unidad']}"
        f = F_NUM(34)
        fa = fuente("bold", 34)
        wa = ancho_txt("≈", fa) + 10
        w = ancho_txt(txt, f) + wa + 76
        im = Image.new("RGBA", (w, 58), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, 57], 29, fill=C["tinta"] + (255,))
        # icono de regla
        d.rounded_rectangle([18, 20, 46, 38], 3, outline=C["ambar"] + (255,), width=3)
        for x in (25, 32, 39):
            d.line([x, 20, x, 27], fill=C["ambar"] + (255,), width=2)
        texto(d, (58, 27), "≈", fa, C["blanco"], "lm")
        texto(d, (58 + wa, 29), txt, f, C["blanco"], "lm")
        _CACHE[k] = im
    return _CACHE[k]

def _panel_mapa(lienzo, t, cfg, ur):
    x0, w = 1310, 520
    # tarjeta de zona
    u = eo(seg(t, 0.3, 1.0))
    k = ("zona", cfg["zona"])
    if k not in _CACHE:
        im, m = caja(w, 250, 22, C["panel"])
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([m, m, m + 14, m + 249], 7, fill=C["verde"] + (255,))
        d.rounded_rectangle([m + 40, m + 30, m + 40 + ancho_txt("ZONA", F_ROT(24)) + 28, m + 66], 18, fill=C["verde"] + (255,))
        texto(d, (m + 54, m + 48), "ZONA", F_ROT(24), C["tinta"], "lm")
        texto(d, (m + 160, m + 48), cfg["region"], F_ROT(24), C["gris"], "lm")
        texto(d, (m + 38, m + 82), cfg["zona"][0], F_TIT(54), C["blanco"], "la")
        texto(d, (m + 38, m + 148), cfg["zona"][1], F_TIT(64), C["blanco"], "la")
        _CACHE[k] = (im, m)
    im, m = _CACHE[k]
    pegar(lienzo, im, x0 - m + (1 - u) * 140, 150 - m, u)
    # leyenda: aparece un renglón con cada pin
    k = ("leyenda",)
    if k not in _CACHE:
        im, m = caja(w, 270, 22, C["panel"])
        d = ImageDraw.Draw(im)
        texto(d, (m + 38, m + 40), "RUTA", F_ROT(26), C["gris"], "lm")
        _CACHE[k] = (im, m)
    u = eo(seg(t, 1.6, 2.2))
    if u > 0:
        im, m = _CACHE[k]
        im = im.copy()
        for i, (t0, num, col, n, sb) in enumerate(((cfg["t_pin1"] + 0.3, 1, C["azul"], cfg["n1"], cfg["s1"]),
                                                   (cfg["t_pin2"] + 0.4, 2, C["rojo"], cfg["n2"], cfg["s2"]))):
            ui = eo(seg(t, t0, t0 + 0.45))
            if ui <= 0:
                continue
            fila = Image.new("RGBA", (w, 100), (0, 0, 0, 0))
            d = ImageDraw.Draw(fila)
            pi, ax, ay = pin(num, col, r=22)
            fila.alpha_composite(pi, (36, 6))
            nn = n.title().replace(" De ", " de ").replace(" Del ", " del ").replace(" Los ", " los ")
            texto(d, (118, 30), nn, F_ROT(34), C["blanco"], "lm")
            texto(d, (118, 68), sb, F_TXT(24), (160, 172, 192), "lm")
            pegar(im, fila, m + (1 - ui) * 40, m + 66 + i * 98, ui)
        pegar(lienzo, im, x0 - m + (1 - u) * 140, 420 - m, u)
    # contador grande de distancia
    k = ("distc",)
    if k not in _CACHE:
        im, m = caja(w, 300, 22, C["panel"])
        d = ImageDraw.Draw(im)
        texto(d, (m + 38, m + 40), "DISTANCIA", F_ROT(26), C["gris"], "lm")
        texto(d, (m + 38, m + 262), cfg["nota_dist"], F_TXT(24), (160, 172, 192), "lm")
        _CACHE[k] = (im, m)
    u = eo(seg(t, 2.6, 3.2))
    if u > 0:
        im, m = _CACHE[k]
        im = im.copy()
        d = ImageDraw.Draw(im)
        val = int(round(cfg["distancia"] * ur))
        fN = F_NUM(150)
        texto(d, (m + 32, m + 160), f"{val}", fN, C["ambar"], "lm")
        texto(d, (m + 44 + ancho_txt(f"{cfg['distancia']}", fN), m + 190), cfg["unidad"], F_NUM(52), C["ambar"], "lm")
        # barra de progreso de la ruta
        d.rounded_rectangle([m + 38, m + 226, m + w - 38, m + 236], 5, fill=C["panel2"] + (255,))
        if ur > 0:
            d.rounded_rectangle([m + 38, m + 226, m + 38 + (w - 76) * ur, m + 236], 5, fill=C["ambar"] + (255,))
        pegar(lienzo, im, x0 - m + (1 - u) * 140, 710 - m, u)

# ================================================================== gameplay tratado
class Clip:
    def __init__(self, ruta, desde=0.0):
        self.cap = cv2.VideoCapture(ruta)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.i = -1
        self.ult = None
        self.desde = desde
        n0 = int(round(desde * self.fps))
        if n0:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, n0)
            self.i = n0 - 1
    def en(self, t):
        objetivo = int(round((self.desde + t) * self.fps))
        while self.i < objetivo:
            ok, fr = self.cap.read()
            if not ok:
                break
            self.ult = fr
            self.i += 1
        return self.ult

def tratar_gameplay(bgr, oscuro=0.42):
    """Gameplay plano: menos saturación + velo azul marino (deja que mande el gráfico)."""
    if bgr.shape[1] != W or bgr.shape[0] != H:
        bgr = cv2.resize(bgr, (W, H), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
    g = rgb.mean(axis=2, keepdims=True)
    rgb = rgb * 0.55 + g * 0.45
    rgb = rgb * (1 - oscuro) + np.array(C["fondo"], np.float32) * oscuro
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")

# ================================================================== 2 · FICHA SOBRE GAMEPLAY
CFG_FICHA = dict(
    numero="N.º 15", titulo="SIN LOS 60 CRISTALES",
    iconos=[(os.path.join(BASE, "pegatinas", f"o_cristal_{c}.png"), col) for c, col in
            (("rojo", C["rojo"]), ("amarillo", C["amarillo"]), ("azul", C["azul"]), ("verde", C["verde"]))],
    cada=15, total=60, unidad="CRISTALES", resumen="4 tipos de cristal × 15 cada uno",
    t_iconos=(1.6, 2.9, 4.2, 5.5), t_resumen=6.7, t_salida=9.2,
)

def ficha(lienzo, t, cfg=CFG_FICHA):
    x, y, w, h = 140, 220, 1000, 640
    ue = eo(seg(t, 0.2, 0.8)) * (1 - ei(seg(t, cfg["t_salida"], cfg["t_salida"] + 0.45)))
    dx = -(1 - eo(seg(t, 0.2, 0.8))) * 160 - ei(seg(t, cfg["t_salida"], cfg["t_salida"] + 0.45)) * 260
    k = ("ficha", cfg["numero"], cfg["titulo"])
    if k not in _CACHE:
        im, m = caja(w, h, 26, C["blanco"])
        d = ImageDraw.Draw(im)
        # cabecera de color sólido
        d.rounded_rectangle([m, m, m + w - 1, m + 130], 26, fill=C["rojo"] + (255,))
        d.rectangle([m, m + 100, m + w - 1, m + 130], fill=C["rojo"] + (255,))
        fN = F_NUM(46)
        wn = ancho_txt(cfg["numero"], fN) + 44
        d.rounded_rectangle([m + 40, m + 38, m + 40 + wn, m + 94], 28, fill=C["blanco"] + (255,))
        texto(d, (m + 40 + wn / 2, m + 67), cfg["numero"], fN, C["rojo"], "mm")
        texto(d, (m + 40 + wn + 22, m + 66), "·", F_TIT(52), C["blanco"], "lm")
        texto(d, (m + 40 + wn + 52, m + 64), cfg["titulo"], F_TIT(52), C["blanco"], "lm")
        # huecos de los íconos
        for i in range(4):
            tx_ = m + 45 + i * 240
            d.rounded_rectangle([tx_, m + 190, tx_ + 190, m + 380], 22, fill=C["gris_cl"] + (255,))
        d.line([m + 45, m + 520, m + w - 45, m + 520], fill=C["gris_cl"] + (255,), width=3)
        _CACHE[k] = (im, m)
    im, m = _CACHE[k]
    im = im.copy()
    d = ImageDraw.Draw(im)
    for i, ((ruta, col), t0) in enumerate(zip(cfg["iconos"], cfg["t_iconos"])):
        if t < t0:
            continue
        u = eob(seg(t, t0, t0 + 0.45), 2.4)
        kk = ("ico", ruta)
        if kk not in _CACHE:
            ic = Image.new("RGBA", (190, 190), (0, 0, 0, 0))
            dd = ImageDraw.Draw(ic)
            dd.rounded_rectangle([0, 0, 189, 189], 22, fill=col + (255,))
            ic.alpha_composite(imagen_cubre(ruta, 162, 162, 14), (14, 14))
            _CACHE[kk] = ic
        ic = escalar(_CACHE[kk], max(0.05, u))
        tx_ = m + 45 + i * 240 + 95
        pegar(im, ic, tx_ - ic.width / 2, m + 285 - ic.height / 2, cl(seg(t, t0, t0 + 0.12)))
        u2 = eo(seg(t, t0 + 0.2, t0 + 0.55))
        if u2 > 0:
            txt_im = Image.new("RGBA", (220, 90), (0, 0, 0, 0))
            texto(ImageDraw.Draw(txt_im), (110, 45), f"×{cfg['cada']}", F_NUM(66), col, "mm")
            pegar(im, txt_im, tx_ - 110, m + 395 + (1 - u2) * 30, u2)
    if t > cfg["t_resumen"]:
        u = eo(seg(t, cfg["t_resumen"], cfg["t_resumen"] + 0.5))
        r_im = Image.new("RGBA", (w - 90, 80), (0, 0, 0, 0))
        texto(ImageDraw.Draw(r_im), (0, 40), cfg["resumen"], F_TXT(38), C["gris"], "lm")
        pegar(im, revelar_izq(r_im, u), m + 45, m + 540)
    pegar(lienzo, im, x - m + dx, y - m, ue)
    _anillo(lienzo, t, cfg)

def _anillo(lienzo, t, cfg):
    """Contador grande: anillo segmentado (un tramo por ícono) y número que sube."""
    cx, cy, R, gro = 1500, 540, 250, 62
    ue = eo(seg(t, 0.5, 1.1)) * (1 - ei(seg(t, cfg["t_salida"], cfg["t_salida"] + 0.45)))
    dx = (1 - eo(seg(t, 0.5, 1.1))) * 200 + ei(seg(t, cfg["t_salida"], cfg["t_salida"] + 0.45)) * 300
    if ue <= 0:
        return
    S = 2
    L = 2 * 335
    im = Image.new("RGBA", (L * S, L * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = L * S / 2
    d.ellipse([c - 330 * S, c - 330 * S, c + 330 * S, c + 330 * S], fill=C["panel"] + (255,))
    caja_r = [c - R * S, c - R * S, c + R * S, c + R * S]
    n = len(cfg["iconos"])
    tramo = 360 / n
    for i in range(n):
        a0 = -90 + i * tramo + 2.5
        a1 = -90 + (i + 1) * tramo - 2.5
        d.arc(caja_r, a0, a1, fill=C["panel2"] + (255,), width=gro * S)
    llenos = 0.0
    for i, ((_, col), t0) in enumerate(zip(cfg["iconos"], cfg["t_iconos"])):
        u = eio(seg(t, t0 + 0.1, t0 + 0.8))
        llenos += u
        if u > 0:
            a0 = -90 + i * tramo + 2.5
            a1 = a0 + (tramo - 5) * u
            d.arc(caja_r, a0, a1, fill=col + (255,), width=gro * S)
    val = int(round(cfg["cada"] * llenos))
    pulso = 1 + 0.08 * math.sin(math.pi * seg(t, cfg["t_iconos"][-1] + 0.8, cfg["t_iconos"][-1] + 1.3))
    texto(d, (c, c - 10 * S), f"= {val}", F_NUM(int(118 * pulso) * S), C["blanco"], "mm")
    texto(d, (c, c + 82 * S), cfg["unidad"], F_ROT(32 * S), (160, 172, 192), "mm")
    im = im.resize((L, L), Image.LANCZOS)
    sh = Image.new("RGBA", (L + 80, L + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([40 + 5, 40 + 18, 40 + L - 5, 40 + L + 8], fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(20))
    pegar(lienzo, sh, cx - L / 2 - 40 + dx, cy - L / 2 - 40, ue)
    pegar(lienzo, im, cx - L / 2 + dx, cy - L / 2, ue)

# ================================================================== 3 · TARJETA DE JEFE + RÓTULO
CFG_TARJETA = dict(
    foto=os.path.join(BASE, "pegatinas", "bancal_creador.png"),
    etiqueta="JEFA FINAL", nombre="NANAYA", linea="cambia de elemento cada 25 %", tramos=4,
    t_barra=(2.6, 6.2), t_salida=7.6,
)

def tarjeta(lienzo, t, cfg=CFG_TARJETA):
    x, y, w, h = 1160, 130, 640, 770
    ui = eo(seg(t, 0.4, 1.1))
    us = ei(seg(t, cfg["t_salida"], cfg["t_salida"] + 0.5))
    a = ui * (1 - us)
    dx = (1 - ui) * 220 + us * 320
    if a <= 0:
        return
    k = ("jefe", cfg["nombre"])
    if k not in _CACHE:
        im, m = caja(w, h, 26, C["blanco"])
        d = ImageDraw.Draw(im)
        im.alpha_composite(imagen_cubre(cfg["foto"], w - 60, 330, 16), (m + 30, m + 30))
        fe = F_ROT(30)
        we = ancho_txt(cfg["etiqueta"], fe) + 40
        d.rounded_rectangle([m + 30, m + 392, m + 30 + we, m + 440], 24, fill=C["rojo"] + (255,))
        texto(d, (m + 30 + we / 2, m + 416), cfg["etiqueta"], fe, C["blanco"], "mm")
        texto(d, (m + 26, m + 452), cfg["nombre"], F_TIT(112), C["tinta"], "la")
        texto(d, (m + 30, m + 618), cfg["linea"], F_TXT(36), C["gris"], "lm")
        _CACHE[k] = (im, m)
    im, m = _CACHE[k]
    im = im.copy()
    d = ImageDraw.Draw(im)
    # barra de vida segmentada en tramos de 25 %: se vacía y marca cada cambio
    bx0, bx1, by = m + 30, m + w - 30, m + 668
    n = cfg["tramos"]
    u = eio(seg(t, *cfg["t_barra"]))
    vida = 1 - u
    ancho = (bx1 - bx0 - (n - 1) * 8) / n
    for i in range(n):
        sx0 = bx0 + i * (ancho + 8)
        d.rounded_rectangle([sx0, by, sx0 + ancho, by + 34], 8, fill=C["gris_cl"] + (255,))
        lleno = cl(vida * n - i)
        if lleno > 0:
            col = C["tinta"] if i % 2 == 0 else C["panel2"]
            d.rounded_rectangle([sx0, by, sx0 + max(16, ancho * lleno), by + 34], 8, fill=col + (255,))
    for i in range(n + 1):
        pc = 100 - i * (100 // n)
        sx = bx1 - i * (ancho + 8) + (4 if 0 < i < n else 0)
        sx = bx0 + (n - i) * (ancho + 8) - (4 if 0 < i < n else 0) if i < n else bx0
        texto(d, (min(max(sx, bx0 + 20), bx1 - 30), by + 62), f"{pc} %", F_TXT(22), C["gris"], "mm")
    # rombo ámbar que salta al cruzar cada 25 %
    for i in range(1, n):
        umbral = 1 - i / n
        tc = cfg["t_barra"][0] + (cfg["t_barra"][1] - cfg["t_barra"][0]) * _inv_eio(1 - umbral)
        if t >= tc:
            p = eob(seg(t, tc, tc + 0.35), 2.6)
            sx = bx0 + (n - i) * (ancho + 8) - 4
            r = 15 * p
            d.polygon([(sx, by + 17 - r), (sx + r, by + 17), (sx, by + 17 + r), (sx - r, by + 17)], fill=C["ambar"] + (255,),
                      outline=C["blanco"] + (255,))
    pegar(lienzo, im, x - m + dx, y - m, a)

def _inv_eio(v):
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if eio(mid) < v:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

CFG_ROTULO = dict(texto="Sin cristales: solo 5 jefes", sello="5", chip="N.º 15", t_salida=6.4)

def rotulo(lienzo, t, cfg=CFG_ROTULO):
    x, y, hgt = 110, 880, 104
    us = ei(seg(t, cfg["t_salida"], cfg["t_salida"] + 0.5))
    f = F_TIT(50)
    wt = ancho_txt(cfg["texto"], f)
    wbar = wt + 120
    # barra blanca que crece desde el sello
    ub = eo(seg(t, 0.35, 0.95)) * (1 - us)
    if ub > 0:
        k = ("rotbar", cfg["texto"])
        if k not in _CACHE:
            im, m = caja(wbar, hgt, 16, C["blanco"])
            d = ImageDraw.Draw(im)
            d.rectangle([m, m + hgt - 12, m + wbar - 1, m + hgt - 1], fill=C["ambar"] + (255,))
            d.rounded_rectangle([m, m + hgt - 16, m + wbar - 1, m + hgt - 1], 8, fill=C["ambar"] + (255,))
            d.rectangle([m, m + hgt - 30, m + wbar - 1, m + hgt - 13], fill=C["blanco"] + (255,))
            texto(d, (m + 80, m + hgt / 2 - 6), cfg["texto"], f, C["tinta"], "lm")
            _CACHE[k] = (im, m)
        im, m = _CACHE[k]
        pegar(lienzo, revelar_izq(im, ub), x + 40 - m, y - m)
    # chip superior
    uc = eo(seg(t, 0.8, 1.2)) * (1 - us)
    if uc > 0:
        fc = F_ROT(28)
        wc = ancho_txt(cfg["chip"], fc) + 36
        ch = Image.new("RGBA", (wc, 44), (0, 0, 0, 0))
        dd = ImageDraw.Draw(ch)
        dd.rounded_rectangle([0, 0, wc - 1, 43], 22, fill=C["tinta"] + (255,))
        texto(dd, (wc / 2, 22), cfg["chip"], fc, C["ambar"], "mm")
        pegar(lienzo, ch, x + 120, y - 56 + (1 - uc) * 20, uc)
    # sello circular (estampa con rebote y anillo que se abre)
    u = eob(seg(t, 0.0, 0.45), 2.6)
    a = cl(seg(t, 0.0, 0.1)) * (1 - us)
    if a > 0:
        S = 4
        R = 64
        im = Image.new("RGBA", ((R + 8) * 2 * S, (R + 8) * 2 * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        c = (R + 8) * S
        d.ellipse([c - (R + 6) * S, c - (R + 6) * S, c + (R + 6) * S, c + (R + 6) * S], fill=C["blanco"] + (255,))
        d.ellipse([c - R * S, c - R * S, c + R * S, c + R * S], fill=C["rojo"] + (255,))
        d.ellipse([c - (R - 12) * S, c - (R - 12) * S, c + (R - 12) * S, c + (R - 12) * S], outline=C["blanco"] + (150,),
                  width=3 * S)
        texto(d, (c, c + 2 * S), cfg["sello"], F_NUM(78 * S), C["blanco"], "mm")
        im = im.resize((im.width // S, im.height // S), Image.LANCZOS)
        ims = escalar(im, max(0.05, (2.2 - 1.2 * u) if t < 0.45 else 1.0) * (1 - 0.6 * us))
        cx, cy = x + 40, y + hgt / 2
        pegar(lienzo, ims, cx - ims.width / 2, cy - ims.height / 2, a)
        # onda del golpe
        if 0.3 < t < 1.0:
            f2 = seg(t, 0.3, 1.0)
            onda = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
            rr = 70 + 100 * eo(f2)
            ImageDraw.Draw(onda).ellipse([180 - rr, 180 - rr, 180 + rr, 180 + rr], outline=C["rojo"] + (int(220 * (1 - f2)),),
                                         width=6)
            pegar(lienzo, onda, cx - 180, cy - 180)

# ================================================================== transición plana
def transicion(lienzo, t, tc, dur=0.9, color=C["fondo"], acento=C["ambar"]):
    """Panel de color que entra por la izquierda, cubre en tc y sale por la derecha; filo de acento."""
    u = (t - (tc - dur / 2)) / dur
    if u <= 0 or u >= 1:
        return
    d = ImageDraw.Draw(lienzo)
    filo = 70
    inc = 220  # inclinación del borde
    if u < 0.5:
        e = eio(u * 2) * (W + inc + filo)
        d.polygon([(0, 0), (e, 0), (e - inc, H), (0, H)], fill=color + (255,))
        d.polygon([(e, 0), (e + filo, 0), (e + filo - inc, H), (e - inc, H)], fill=acento + (255,))
    else:
        e = eio((u - 0.5) * 2) * (W + inc + filo)
        d.polygon([(e, 0), (W + inc + filo, 0), (W + filo, H), (e - inc, H)], fill=color + (255,))
        d.polygon([(e - filo, 0), (e, 0), (e - inc, H), (e - filo - inc, H)], fill=acento + (255,))

# ================================================================== guion del video
_CLIPS = {}
def clip(nombre, desde=0.0):
    k = (nombre, desde)
    if k not in _CLIPS:
        _CLIPS[k] = Clip(os.path.join(BASE, "medios", nombre), desde)
    return _CLIPS[k]

def cuadro(t):
    if t < 11.0:
        lz = fondo_plano()
        mapa_ruta(lz, t)
    elif t < 21.0:
        tl = t - 11.0
        if tl < 5.0:
            fr = clip("scene-089.mp4", 1.0).en(tl)
            lz = tratar_gameplay(fr)
        else:
            fr = clip("scene-091.mp4", 0.0).en(tl - 5.0)
            lz = tratar_gameplay(fr)
            if tl < 5.25:  # fundido corto entre tomas
                prev = clip("scene-089.mp4", 1.0).en(tl)
                lz = Image.blend(tratar_gameplay(prev), lz, seg(tl, 5.0, 5.25))
        ficha(lz, tl)
    else:
        tl = t - 21.0
        lz = tratar_gameplay(clip("scene-093.mp4", 0.0).en(tl), 0.38)
        tarjeta(lz, tl)
        rotulo(lz, tl - 1.6)
    transicion(lz, t, 11.0)
    transicion(lz, t, 21.0)
    etiqueta_estilo(lz)
    # salida final: el panel cubre y se queda
    if t > 29.35:
        u = eio(seg(t, 29.35, 29.95))
        d = ImageDraw.Draw(lz)
        e = u * (W + 290)
        d.polygon([(0, 0), (e, 0), (e - 220, H), (0, H)], fill=C["fondo"] + (255,))
        d.polygon([(e, 0), (e + 70, 0), (e - 150, H), (e - 220, H)], fill=C["ambar"] + (255,))
        if u >= 1:
            etiqueta_estilo(lz)
    return lz.convert("RGB")

def render():
    audio = os.path.join(BASE, "audio", "wow", "nlXOcybLHxc.wav")
    # pista con media ≈ −18 dB (la original media −23,4 dB → +5,4 dB), fundidos de entrada y salida
    filtro = "[1:a]atrim=0:30,asetpts=N/SR/TB,volume=5.4dB,afade=t=in:st=0:d=1.5,afade=t=out:st=27.0:d=3.0[a]"
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", audio, "-filter_complex", filtro, "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-threads", "4",
           "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR}", "-movflags", "+faststart", SALIDA]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(cuadro(i / FPS).tobytes())
        if i % 90 == 0:
            print(f"cuadro {i}/{n}", flush=True)
    p.stdin.close()
    p.wait()
    print("listo:", SALIDA)

def hoja():
    """12 cuadros (uno cada 2,5 s, a mitad de cada tramo) del mp4 renderizado -> hoja.jpg 4x3."""
    cap = cv2.VideoCapture(SALIDA)
    tiles = []
    for k in range(12):
        t = 1.25 + 2.5 * k
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * FPS))
        ok, fr = cap.read()
        if not ok:
            fr = np.zeros((H, W, 3), np.uint8)
        fr = cv2.resize(fr, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(fr, f"{t:.2f}s", (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(fr, f"{t:.2f}s", (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        tiles.append(fr)
    filas = [np.hstack(tiles[i * 4:(i + 1) * 4]) for i in range(3)]
    cv2.imwrite(os.path.join(AQUI, "hoja.jpg"), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("hoja:", os.path.join(AQUI, "hoja.jpg"))

if __name__ == "__main__":
    if "--cuadro" in sys.argv:
        for v in sys.argv[sys.argv.index("--cuadro") + 1:]:
            t = float(v)
            # los clips leen en orden: para un cuadro suelto basta con pedirlo directo
            cuadro(t).save(os.path.join(AQUI, f"_cuadro_{t}.png"))
            print("ok", t)
    elif "--hoja" in sys.argv:
        hoja()
    else:
        render()
        hoja()
