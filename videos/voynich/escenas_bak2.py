# -*- coding: utf-8 -*-
"""El libro que nadie puede leer (manuscrito Voynich): tomas del documental, ancladas a la voz.

Una sola clase `Mundo` dibuja todo en función del tiempo global. Cada toma (`@toma`) es una función `f(lz, t)`; las tomas
se solapan con una transición (fundido, látigo, negro...). Todos los rótulos salen del tiempo real de cada palabra
(`T(escena, palabra, frase=i)`), así que nada queda desincronizado.

Material: escaneos de Yale (imagenes/folios, dominio público) y fotos de Commons (imagenes/creditos.json).
Datos de las infografías: datos/zipf.json (transcripción de Takahashi vs Don Quijote), carbono 14 de Arizona (1404-1438).
"""
import json
import math
import os
import types

import cv2
import numpy as np

from escena_base import *  # noqa: F401,F403
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth, clamp01
import docu as D  # después del *: escena_base también exporta un `D` (dibujos)

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
AM, BL, RJ = D.AMARILLO, D.BLANCO, D.ROJO
I3 = np.eye(3)


def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def FR(eid, i):
    return _ESC[eid]["frases"][i]


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def kar(eid, i, a, b, **kw):
    return D.karaoke(FR(eid, i), a, b, **kw)


# ------------------------------------------------------------------ caché de sprites (una copia por proceso)
_C = {}


def spr(clave, fn):
    if clave not in _C:
        _C[clave] = fn()
    return _C[clave]


def HD(nombre):
    """Ruta al escaneo completo de Yale (2682x3740) para acercamientos nítidos."""
    return os.path.abspath(f"imagenes/folios_hd/{nombre}.jpg")


def folio(n, alto=1000):
    return spr(("f", n, alto), lambda: D.hoja_papel(D.cargar(D.ruta_img(f"f{n:03d}"), 2200), alto))


def pola(nombre, ancho=440, asp=1.05, foco=(0.5, 0.5), leyenda=None, lado=1600):
    return spr(("p", nombre, ancho, asp, foco, leyenda),
               lambda: D.polaroid(D.cargar(D.ruta_img(nombre), lado), ancho, asp, foco, leyenda=leyenda))


def recorte(nombre):
    from PIL import Image
    im = np.asarray(Image.open(f"imagenes/recortes/{nombre}.png").convert("RGBA"))
    return D.Sprite(im[..., :3].copy(), im[..., 3] / 255.0, sombra=True, sr=22, off=(16, 20), sop=0.7)


def corcho():
    return spr("corcho", lambda: D.Sprite(D.tablero(), None, sombra=False))


PALABRAS_VOY = [w for w in open("datos/takahashi_clean.txt", encoding="utf-8", errors="ignore").read().replace("*", " ").split()
                if w.isalpha()][:6000]
ZIPF = json.load(open("datos/zipf.json"))
C0 = (1700, 1000)          # centro del tablero de corcho (mundo)


def carta(lz, sp, M, t, t_in, x, y, rot=0.0, s=1.0, desde=(0, -420), dur=0.5, flota=1.0, fase=0.0, op=1.0, ry0=62.0):
    """Lámina que entra volando con giro 3D, se asienta con un pequeño rebote y luego flota."""
    if t < t_in:
        return
    u = e_out(prog(t, t_in, t_in + dur))
    e = t - t_in
    asent = math.exp(-(e - dur) * 3.2) * math.sin((e - dur) * 15.0) * 2.4 if e > dur else 0.0
    fl = flota * 5.0 * math.sin(0.9 * t + fase)
    Mm = M @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u) + fl, lerp(1.4, 1.0, u) * s,
                     rot + asent + (1 - u) * 16, (1 - u) * ry0)
    D.pegar(lz, sp, Mm, op * smooth(prog(t, t_in, t_in + 0.14)))


def bloque(pal, cx, cy, px=84, fnt="serif", color=AM, alinear="centro", lineas=None):
    """`pal` = [(texto, t)]; `lineas` = índices donde se corta a nueva línea (p. ej. (2,) = 2 palabras en la primera)."""
    if lineas:
        filas, ini = [], 0
        for c in list(lineas) + [len(pal)]:
            filas.append(pal[ini:c])
            ini = c
        filas = [f for f in filas if f]
    else:
        filas = [pal]
    return D.bloque_texto(filas, cx, cy, fnt, px, color, alinear)


def sombra_lateral(lz, lado="izq", fuerza=0.55):
    """Oscurece un costado para que el texto se lea sobre cualquier imagen."""
    X = np.linspace(0, 1, W, dtype=np.float32)
    g = np.clip(1 - X / 0.6, 0, 1) if lado == "izq" else np.clip((X - 0.4) / 0.6, 0, 1)
    lz *= (1 - fuerza * g ** 1.5)[None, :, None]


def franja_texto(lz, fuerza=0.55, y0=0.68):
    Y = np.linspace(0, 1, H, dtype=np.float32)
    g = np.clip((Y - y0) / (1 - y0), 0, 1)
    lz *= (1 - fuerza * g ** 1.3)[:, None, None]


# ================================================================== tomas
TOMAS = []


def toma(t0, t1, ent=("fundido", 0.4), grado=None):
    def deco(f):
        TOMAS.append(dict(t0=t0, t1=t1, fn=f, ent=ent, grado=grado or {}))
        return f
    return deco


# ------------------------------------------------------------------ anclas
g_nadie = T("gancho", "nadie", frase=0)
g_libro = T("gancho", "libro", frase=0)
g_240, g_pag, g_dib, g_imp, g_un, g_idioma, g_ningun = (T("gancho", w, frase=1) for w in
                                                       ("doscientas", "paginas", "dibujos", "imposibles", "un", "idioma", "ningun"))
g_cripto, g_mil, g_comp, g_logrado = T("gancho", "criptografos", frase=2), T("gancho", "militares", frase=2), \
    T("gancho", "computadoras", frase=2), T("gancho", "logrado", frase=2)
g_hasta = T("gancho", "hasta", frase=2)

o_doce = T("origen", "doce", frase=0)
o_wilfrid, o_colegio, o_roma = T("origen", "wilfrid", frase=1), T("origen", "colegio", frase=1), T("origen", "roma", frase=1)
o_libro, o_apellido = T("origen", "libro", frase=2), T("origen", "apellido", frase=2)

c_plantas, c_existen, c_herb = T("contenido", "plantas", frase=0), T("contenido", "botanico", frase=0), T("contenido", "identificar", frase=0)
c_certeza = T("contenido", "certeza", frase=0)
c_estrellas, c_mujeres, c_alfabeto = T("contenido", "estrellas", frase=1), T("contenido", "mujeres", frase=1), T("contenido", "alfabeto", frase=1)
c_pagina = T("contenido", "pagina", frase=1)
c_quien, c_porque = T("contenido", "quien", frase=2), T("contenido", "por", frase=2)

f_2009, f_arizona, f_carbono, f_catorce = T("fecha", "nueve", frase=0), T("fecha", "arizona", frase=0), \
    T("fecha", "carbono", frase=0), T("fecha", "catorce", frase=0)
f_resultado, f_entre, f_ocho = T("fecha", "resultado", frase=1), T("fecha", "entre", frase=1), T("fecha", "ocho", frase=1)
f_med, f_falsif, f_moderna = T("fecha", "medieval", frase=2), T("fecha", "falsificacion", frase=2), T("fecha", "moderna", frase=2)
f_eamon, f_menos, f_ternero = T("fecha", "eamon", frase=3), T("fecha", "menos", frase=3), T("fecha", "ternero", frase=3)

d_rastro, d_pasado = T("duenos", "rastro", frase=0), T("duenos", "pasado", frase=0)
d_1639, d_georg, d_ayuda, d_sabio, d_kircher = (T("duenos", w, frase=1) for w in ("nueve", "georg", "ayuda", "sabio", "atanasio"))
d_respondio, d_quiso = T("duenos", "respondio", frase=2), T("duenos", "quiso", frase=2)
d_carta, d_emperador, d_rodolfo = T("duenos", "carta", frase=3), T("duenos", "emperador", frase=3), T("duenos", "rodolfo", frase=3)
d_600, d_ducados, d_oro = T("duenos", "seiscientos", frase=3), T("duenos", "ducados", frase=3), T("duenos", "oro", frase=3)

i_william, i_purpura, i_anos = T("intentos", "william", frase=0), T("intentos", "purpura", frase=0), T("intentos", "anos", frase=0)
i_copio, i_linea, i_tarjetas = T("intentos", "copio", frase=1), T("intentos", "linea", frase=1), T("intentos", "tarjetas", frase=1)
i_pudo, i_desc, i_lenguaje = T("intentos", "pudo", frase=2), T("intentos", "descifrarlo", frase=2), T("intentos", "lenguaje", frase=2)
i_artificial = T("intentos", "artificial", frase=2)
i_ruido, i_azar = T("intentos", "ruido", frase=3), T("intentos", "azar", frase=3)
i_patrones, i_idioma, i_real = T("intentos", "patrones", frase=4), T("intentos", "idioma", frase=4), T("intentos", "real", frase=4)
i_treinta, i_palabras, i_veinte, i_simbolos = (T("intentos", w, frase=5) for w in ("treinta", "palabras", "veinte", "simbolos"))

t_codigo, t_inventado = T("teorias", "codigo", frase=0), T("teorias", "inventado", frase=0)
t_idioma_t = T("teorias", "idioma", frase=0)
t_fraude = T("teorias", "fraude", frase=1)
t_ninguna, t_teoria, t_convencido, t_expertos = (T("teorias", w, frase=2) for w in ("ninguna", "teoria", "convencido", "expertos"))

k_beinecke, k_yale = T("cierre", "biblioteca", frase=0), T("cierre", "yale", frase=0)
k_internet, k_600, k_secreto = T("cierre", "internet", frase=1), T("cierre", "seiscientos", frase=1), T("cierre", "secreto", frase=1)
k_sera, k_leer, k_o, k_leido = T("cierre", "sera", frase=2), T("cierre", "leer", frase=2), T("cierre", "o", frase=2), T("cierre", "leido", frase=2)

# instantes de arranque de cada frase
G0, G1, G2 = INI("gancho", 0), INI("gancho", 1), INI("gancho", 2)
O0, O1, O2 = INI("origen", 0), INI("origen", 1), INI("origen", 2)
C0_, C1_, C2_ = INI("contenido", 0), INI("contenido", 1), INI("contenido", 2)
F0, F1, F2, F3 = (INI("fecha", k) for k in range(4))
D0, D1, D2, D3 = (INI("duenos", k) for k in range(4))
I0, I1, I2, I3_, I4, I5 = (INI("intentos", k) for k in range(6))
T0, T1, T2 = INI("teorias", 0), INI("teorias", 1), INI("teorias", 2)
K0, K1, K2 = INI("cierre", 0), INI("cierre", 1), INI("cierre", 2)
FIN_VOZ = FIN("cierre")
PAD = 0.12          # las tomas empiezan un poco antes de la frase (la transición ya está a medias cuando se habla)


# ================================================================== GANCHO
@toma(0.0, G1 - 0.1, ent=("fundido", 0.01), grado=dict(destello=0.10))
def t_gancho_libro(lz, t):
    lz[:] = D.pozo_luz(0.32, 0.45, 0.7)
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.22, W / 2 + 40, H / 2 - 10, 0.0), G1 - 0.1, mano=0.6)(t)
    sp = folio(1, 900)
    u = prog(t, 0.0, 1.6)
    ry = lerp(-26, -9, e_out(u)) + 3 * math.sin(0.6 * t)
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, 600, 540, 1.0, -3 + 1.5 * math.sin(0.4 * t), ry, 2), smooth(prog(t, 0.0, 1.4)))
    pal = bloque(kar("gancho", 0, 4, 11), 1370, 520, 92, lineas=(3,))
    D.dibujar_bloque(lz, pal, t, "serif", 92, salida=G1 - 0.55)


@toma(G1 - PAD, G2 - 0.1, ent=("desenfoque", 0.45))
def t_gancho_paginas(lz, t):
    tl = t - (G1 - PAD)
    dur = G2 - G1
    lz[:] = 0
    cam = D.Cam((1.0, C0[0] - 20, C0[1] + 8, 0.6), (1.2, C0[0] + 60, C0[1] - 4, -1.2), dur + 0.5, mano=0.8)(tl)
    D.pegar(lz, corcho(), cam @ D.poner(3400, 2000, C0[0], C0[1]))
    cx, cy = C0
    pts = []
    # 240 páginas: el folio grande de texto
    carta(lz, folio(187, 700), cam, t, g_240 - 0.05, cx + 430, cy - 40, 3.5, desde=(300, 40), fase=1.0)
    # dibujos imposibles: tres polaroids de plantas
    for k, (nom, dx, dy, r, ti) in enumerate((("f004", -300, -215, -7, g_dib), ("f024", -70, 95, 4, g_dib + 0.28), ("f110", -440, 105, -3, g_imp + 0.1))):
        carta(lz, pola(nom, 340, 1.1, (0.5, 0.42)), cam, t, ti - 0.05, cx + dx, cy + dy, r, desde=(-260, -320), fase=k * 1.7)
        if t > ti + 0.3:
            pts.append((cx + dx, cy + dy - 222))
    for a, b in zip(pts[:-1], pts[1:]):
        D.hilo(lz, cam, a, b, smooth(prog(t, g_imp, g_imp + 0.5)))
    for x, y in pts:
        D.pin(lz, cam, x, y)
    if t > g_idioma:
        for k, (dx, dy, w_, h_) in enumerate(((330, -90, 150, 46), (500, 40, 130, 44), (400, 170, 150, 46))):
            D.marcador_mano(lz, "circulo", cx + dx + 0, cy + dy - 40, w_, h_, prog(t, g_idioma + 0.2 * k, g_idioma + 0.2 * k + 0.35), semilla=k)
    # rótulos en pantalla
    D.numero(lz, "240", 300, 235, 210, t, g_240, color=RJ, fnt="abril", salida=g_dib - 0.1)
    D.numero(lz, "Páginas", 300, 375, 62, t, g_pag, color=BL, fnt="serif", pop=False, salida=g_dib - 0.1)
    franja_texto(lz, 0.5, 0.74)
    p1 = bloque([("Dibujos", g_dib), ("Imposibles", g_imp)], W / 2, 985, 84)
    D.dibujar_bloque(lz, p1, t, "serif", 84, salida=g_idioma - 0.15)
    p2 = bloque([("Un", g_un), ("Idioma", g_idioma), ("Único", g_ningun)], W / 2, 985, 84)
    D.dibujar_bloque(lz, p2, t, "serif", 84)


@toma(G2 - PAD, O0 - 0.1, ent=("latigo", 0.4))
def t_gancho_intentos(lz, t):
    tl = t - (G2 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.42, 0.75, (0.22, 0.15, 0.09))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.1, W / 2, H / 2 - 12, 0.0), O0 - G2 + 0.3, mano=0.8)(tl)
    carta(lz, pola("alberti", 470, 1.0, (0.5, 0.5), "Disco de cifrado"), cam, t, g_cripto - 0.05, 430, 470, -6, desde=(-500, 0), fase=0.5)
    carta(lz, pola("purple", 470, 1.0, (0.5, 0.42), "Máquina militar"), cam, t, g_mil - 0.05, 960, 440, 3, desde=(0, -500), fase=2.0)
    D.panel_analisis(lz, PALABRAS_VOY, t, g_comp - 0.05, 1440, 490, 640, 470, dur=g_logrado - g_comp - 0.2)
    D.estampa(lz, "SIN DESCIFRAR", W / 2, 640, t, g_logrado - 0.05, 118, rot=-7)
    franja_texto(lz, 0.5, 0.78)
    pal = bloque([("Criptógrafos", g_cripto), ("Militares", g_mil), ("Computadoras", g_comp)], W / 2, 900, 74)
    D.dibujar_bloque(lz, pal, t, "serif", 74, salida=g_logrado - 0.15)
    D.dibujar_bloque(lz, bloque(kar("gancho", 2, 9, 13), W / 2, 985, 84), t, "serif", 84)


# ================================================================== ORIGEN
@toma(O0 - PAD, O1 - 0.1, ent=("negro", 0.5), grado=dict(destello=0.06, teal=0.02, calido=0.07))
def t_origen_fecha(lz, t):
    tl = t - (O0 - PAD)
    D.foto_parallax(lz, "mondragone_grabado", tl, O1 - O0 + 0.6, 1.10, 1.28, (0.42, 0.5), (0.55, 0.48), par=(60, 8), tono=(0.32, 0.27, 0.22))
    D.numero(lz, "1912", W / 2, H / 2 - 20, 300, t, o_doce - 0.05, color=BL, fnt="sans", pop=True)
    D.numero(lz, "Es", 540, 305, 64, t, o_doce - 0.15, color=(0.85, 0.85, 0.82), fnt="sans_i", pop=False)


@toma(O1 - PAD, o_colegio - 0.1, ent=("latigo", 0.35))
def t_origen_voynich(lz, t):
    tl = t - (O1 - PAD)
    lz[:] = D.pozo_luz(0.68, 0.45, 0.6, (0.26, 0.18, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.12, W / 2 - 20, H / 2, 0.0), o_colegio - O1 + 0.3, mano=0.7)(tl)
    rc = spr("voy_recorte", lambda: recorte("voynich_retrato"))
    k = 980 / rc.h
    D.pegar(lz, rc, cam @ D.poner(rc.w, rc.h, 1330, 560, k, 0, 0), smooth(prog(t, O1 - PAD + 0.1, O1 + 0.6)))
    D.tag_nombre(lz, "Wilfrid Voynich", 1290, 940, t, o_wilfrid - 0.05, 52)
    pal = bloque(kar("origen", 1, 1, 5), 470, 470, 88, alinear="centro", lineas=(2,))
    D.dibujar_bloque(lz, pal, t, "serif", 88)


@toma(o_colegio - PAD, O2 - 0.1, ent=("latigo", 0.35), grado=dict(calido=0.08))
def t_origen_villa(lz, t):
    tl = t - (o_colegio - PAD)
    D.foto_parallax(lz, "mondragone_grabado", tl, O2 - o_colegio + 0.6, 1.02, 1.22, (0.5, 0.52), (0.6, 0.44), par=(70, 6), tono=(0.9, 0.86, 0.78))
    lz *= 0.85
    D.marca_chartreuse(lz, 1130, 560, 92, t, o_colegio + 0.2)
    D.tag_nombre(lz, "Villa Mondragone · Frascati", 1130, 700, t, o_colegio + 0.3, 44)
    D.tag_nombre(lz, "A unos 20 km de Roma", 1130, 780, t, o_roma - 0.1, 38, rot=2.0)
    franja_texto(lz, 0.55, 0.76)
    pal = bloque(kar("origen", 1, 12, 14), W / 2, 985, 84)
    D.dibujar_bloque(lz, pal, t, "serif", 84)


@toma(O2 - PAD, C0_ - 0.1, ent=("desenfoque", 0.4), grado=dict(destello=0.08))
def t_origen_apellido(lz, t):
    tl = t - (O2 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.5, 0.75, (0.30, 0.21, 0.12))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.28, W / 2, H / 2 + 20, 0.0), C0_ - O2 + 0.4, mano=0.6)(tl)
    sp = folio(3, 1000)
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, 560, 540, 1.0, -4, lerp(-20, -6, e_out(prog(t, O2 - PAD, O2 + 1.5)))), 1)
    p = bloque([("Manuscrito", o_libro - 0.1), ("Voynich", o_apellido - 0.05)], 1390, 520, 100, lineas=(1,))
    D.dibujar_bloque(lz, p, t, "serif", 100)


# ================================================================== CONTENIDO
@toma(C0_ - PAD, C1_ - 0.1, ent=("latigo", 0.35))
def t_cont_plantas(lz, t):
    tl = t - (C0_ - PAD)
    lz[:] = D.pozo_luz(0.5, 0.45, 0.8, (0.22, 0.20, 0.11))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.12, W / 2 + 30, H / 2, 0.0), C1_ - C0_ + 0.3, mano=0.9)(tl)
    carta(lz, folio(4, 800), cam, t, c_plantas - 0.1, 480, 470, -5, desde=(-500, 100), fase=0.3)
    carta(lz, folio(110, 800), cam, t, c_existen - 0.1, 960, 520, 2, desde=(0, 600), fase=1.4)
    carta(lz, folio(24, 800), cam, t, c_herb - 0.25, 1440, 460, 6, desde=(600, -60), fase=2.5)
    franja_texto(lz, 0.55, 0.78)
    pal = bloque([("Plantas", c_plantas), ("Sin", T("contenido", "ningun", frase=0)), ("Identificar", c_herb)], W / 2, 985, 84)
    D.dibujar_bloque(lz, pal, t, "serif", 84)


def _hero(lz, t, ta, tb, nombre, x, y, rot0, rot1, alto=980, ry=(-14, -4), zoom=(1.0, 1.14), fondo=True):
    """Folio grande con cámara propia entre ta y tb (para las tres 'pantallas' de la frase 1)."""
    if fondo:
        lz[:] = D.pozo_luz(0.5, 0.45, 0.8, (0.26, 0.19, 0.11))
    tl = t - ta
    cam = D.Cam((zoom[0], W / 2, H / 2, 0.0), (zoom[1], W / 2, H / 2 + 15, 0.0), tb - ta + 0.4, mano=0.8)(tl)
    sp = folio(nombre, alto)
    u = e_out(prog(t, ta, ta + 0.7))
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, x, y, lerp(0.86, 1.0, u), lerp(rot0, rot1, u), lerp(ry[0], ry[1], u)), smooth(prog(t, ta, ta + 0.2)))
    return cam


@toma(C1_ - PAD, c_mujeres - 0.12, ent=("latigo", 0.35))
def t_cont_estrellas(lz, t):
    _hero(lz, t, C1_ - PAD, c_mujeres - 0.12, 125, 960, 470, -6, 2, alto=860)
    franja_texto(lz, 0.55, 0.78)
    D.dibujar_bloque(lz, bloque([("Diagramas", T("contenido", "diagramas", frase=1)), ("De", T("contenido", "de", frase=1)), ("Estrellas", c_estrellas)], W / 2, 985, 84), t, "serif", 84)


@toma(c_mujeres - 0.12, c_alfabeto - 0.12, ent=("latigo", 0.35))
def t_cont_banos(lz, t):
    _hero(lz, t, c_mujeres - 0.12, c_alfabeto - 0.12, 141, 960, 470, 5, -2, alto=860, ry=(12, 4))
    franja_texto(lz, 0.55, 0.78)
    D.dibujar_bloque(lz, bloque([("Mujeres", c_mujeres), ("Bañándose", T("contenido", "banandose", frase=1)), ("En", T("contenido", "en", frase=1)), ("Tuberías", T("contenido", "tuberias", frase=1))], W / 2, 985, 84), t, "serif", 84)


@toma(c_alfabeto - 0.12, C2_ - 0.1, ent=("latigo", 0.35))
def t_cont_alfabeto(lz, t):
    tl = t - (c_alfabeto - 0.12)
    D.foto_parallax(lz, HD("f187"), tl, C2_ - c_alfabeto + 0.5, 1.5, 2.1, (0.38, 0.28), (0.5, 0.4), par=(0, 0), tono=(0.75, 0.72, 0.66))
    for k, (x, y, w_, h_) in enumerate(((520, 330, 190, 80), (1010, 520, 200, 80), (1500, 700, 210, 84))):
        D.marcador_mano(lz, "circulo", x, y, w_, h_, prog(t, c_alfabeto + 0.5 + 0.35 * k, c_alfabeto + 0.85 + 0.35 * k), semilla=k)
    franja_texto(lz, 0.6, 0.74)
    D.dibujar_bloque(lz, bloque([("Alfabeto", c_alfabeto), ("Desconocido", T("contenido", "desconocido", frase=1))], W / 2, 985, 92), t, "serif", 92)


@toma(C2_ - PAD, F0 - 0.1, ent=("desenfoque", 0.5), grado=dict(destello=0.09, fuerza_vineta=0.75))
def t_cont_quien(lz, t):
    tl = t - (C2_ - PAD)
    D.foto_parallax(lz, "escriba", tl, F0 - C2_ + 0.6, 1.02, 1.2, (0.5, 0.5), (0.56, 0.45), par=(60, 12), tono=(0.72, 0.66, 0.58))
    D.numero(lz, "¿Quién?", 1380, 300, 190, t, c_quien - 0.1, color=AM, fnt="serif", salida=c_porque - 0.15)
    D.numero(lz, "¿Por qué?", 1380, 300, 170, t, c_porque - 0.05, color=BL, fnt="serif")


# ================================================================== FECHA
@toma(F0 - PAD, F1 - 0.1, ent=("desenfoque", 0.45))
def t_fecha_muestras(lz, t):
    tl = t - (F0 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.5, 0.85, (0.22, 0.17, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.1, W / 2, H / 2 - 10, 0.0), F1 - F0 + 0.3, mano=0.8)(tl)
    xs = (300, 680, 1060, 1440)
    for k, (nom, leyenda) in enumerate((("f017", "folio 8"), ("f051", "folio 26"), ("f093", "folio 47"), ("f123", "folio 68"))):
        carta(lz, pola(nom, 360, 1.25, (0.5, 0.45), leyenda), cam, t, f_arizona - 0.2 + 0.28 * k, xs[k] + 90, 470 + (k % 2) * 50, (-4, 3, -2, 5)[k], desde=(0, -420), fase=k)
    D.numero(lz, "2009", 1610, 250, 170, t, f_2009 - 0.05, color=BL, fnt="sans")
    franja_texto(lz, 0.55, 0.76)
    D.dibujar_bloque(lz, bloque(kar("fecha", 0, 4, 8), W / 2, 900, 74), t, "serif", 74, salida=f_carbono - 0.1)
    D.dibujar_bloque(lz, bloque([("Carbono", f_carbono - 0.05), ("14", f_catorce - 0.1)], W / 2, 985, 92), t, "serif", 92)


@toma(F1 - PAD, F2 - 0.1, ent=("desenfoque", 0.4))
def t_fecha_linea(lz, t):
    tl = t - (F1 - PAD)
    D.foto_parallax(lz, HD("f008"), tl, F2 - F1 + 0.6, 1.5, 1.9, (0.5, 0.3), (0.5, 0.42), par=(0, 0), tono=(0.35, 0.33, 0.30))
    D.linea_tiempo(lz, t, f_entre - 0.4, W / 2, H / 2 + 20, 1300, 1500, 1404, 1438, dur=max(0.8, f_ocho - (f_entre - 0.1)),
                   marcas=[(1455, "Biblia de Gutenberg")], etiqueta="Fecha del pergamino · carbono 14")


@toma(F2 - PAD, F3 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.7))
def t_fecha_medieval(lz, t):
    tl = t - (F2 - PAD)
    D.foto_parallax(lz, HD("f001"), tl, F3 - F2 + 0.6, 1.5, 2.0, (0.4, 0.35), (0.55, 0.55), par=(0, 0), tono=(0.7, 0.65, 0.55))
    D.dibujar_bloque(lz, bloque([("Pergamino", T("fecha", "pergamino", frase=2)), ("Medieval", f_med)], W / 2, 250, 110), t, "serif", 110)
    D.dibujar_bloque(lz, bloque([("Falsificación", f_falsif), ("Moderna", f_moderna)], W / 2, 900, 100, color=BL), t, "serif", 100)
    D.marcador_mano(lz, "tachado", W / 2, 905, 760, 12, prog(t, f_moderna + 0.35, f_moderna + 0.75), grosor=11)


def _piel(k):
    def mk():
        im = D.cargar(D.ruta_img("f001"), 2000)
        h, w = im.shape[:2]
        rng = np.random.default_rng(40 + k)
        cw, ch = int(w * 0.55), int(h * 0.36)
        x0, y0 = int(rng.integers(0, w - cw)), int(rng.integers(0, h - ch))
        return D.hoja_papel(np.ascontiguousarray(im[y0:y0 + ch, x0:x0 + cw]), 205, sr=12)
    return spr(("piel", k), mk)


@toma(F3 - PAD, D0 - 0.1, ent=("desenfoque", 0.4))
def t_fecha_pieles(lz, t):
    tl = t - (F3 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.48, 0.85, (0.20, 0.16, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2, H / 2 - 6, 0.0), D0 - F3 + 0.4, mano=0.7)(tl)
    n_ = 14
    t_ini = f_menos - 0.1
    paso = max(0.06, (f_ternero - t_ini - 0.2) / n_)
    for k in range(n_):
        col, fila = k % 7, k // 7
        x = 250 + col * 235 + (fila * 60)
        y = 400 + fila * 270
        carta(lz, _piel(k), cam, t, t_ini + k * paso, x, y, ((k * 37) % 9) - 4, desde=(0, -560), dur=0.35, fase=k)
    n = min(n_, max(0, int((t - t_ini) / paso) + 1)) if t >= t_ini else 0
    if n:
        pm, a, m = D.palabra_img(str(n), "abril", 250, tuple(RJ), stroke=0.04, glow=0.6)
        D.mezclar_pm(lz, pm, a, int(W / 2 - pm.shape[1] / 2), int(150 - pm.shape[0] / 2), smooth(prog(t, t_ini, t_ini + 0.2)))
    D.tag_nombre(lz, "Eamon Duffy · historiador", 480, 890, t, f_eamon - 0.05, 40)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("fecha", 3, 6, 11), W / 2 + 200, 985, 76), t, "serif", 76)


# ================================================================== DUEÑOS
@toma(D0 - PAD, D1 - 0.1, ent=("desenfoque", 0.5), grado=dict(polvo=0.5))
def t_duenos_rastro(lz, t):
    tl = t - (D0 - PAD)
    D.foto_parallax(lz, "escriba2", tl, D1 - D0 + 0.6, 1.02, 1.25, (0.5, 0.5), (0.45, 0.42), par=(50, 10),
                    tono=tuple(0.55 * (1 - 0.7 * prog(t, d_rastro, d_pasado + 0.6)) + 0.04 for _ in range(3)))
    D.dibujar_bloque(lz, bloque(kar("duenos", 0, 0, 7), W / 2, 900, 88, lineas=(4,)), t, "serif", 88)


@toma(D1 - PAD, d_sabio - 0.12, ent=("desenfoque", 0.45), grado=dict(calido=0.06, sat=0.7))
def t_duenos_praga(lz, t):
    tl = t - (D1 - PAD)
    D.foto_parallax(lz, "praga", tl, d_sabio - D1 + 0.5, 1.04, 1.22, (0.5, 0.5), (0.58, 0.46), par=(70, 10), tono=(0.72, 0.68, 0.62))
    D.numero(lz, "1639", 1470, 210, 240, t, d_1639 - 0.05, color=BL, fnt="sans")
    D.tag_nombre(lz, "Georg Baresch · alquimista", 520, 820, t, d_georg - 0.05, 46)
    D.tag_nombre(lz, "Praga", 340, 720, t, T("duenos", "praga", frase=1) - 0.05, 40, rot=2.5)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 1, 12, 17), W / 2, 985, 76), t, "serif", 76)


@toma(d_sabio - PAD, D2 - 0.1, ent=("latigo", 0.35), grado=dict(calido=0.08))
def t_duenos_kircher(lz, t):
    tl = t - (d_sabio - PAD)
    D.foto_parallax(lz, "kircher", tl, D2 - d_sabio + 0.5, 1.06, 1.28, (0.5, 0.35), (0.5, 0.3), par=(60, 10), tono=(0.85, 0.82, 0.75))
    D.tag_nombre(lz, "Athanasius Kircher", 1450, 900, t, d_kircher - 0.05, 46)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 1, 18, 20), W / 2, 985, 84), t, "serif", 84)


@toma(D2 - PAD, d_quiso - 0.15, ent=("desenfoque", 0.35), grado=dict(calido=0.08))
def t_duenos_respondio(lz, t):
    tl = t - (D2 - PAD)
    D.foto_parallax(lz, "kircher", tl, d_quiso - D2 + 0.5, 1.25, 1.42, (0.5, 0.30), (0.5, 0.28), par=(80, 10), tono=(0.75, 0.72, 0.65))
    D.numero(lz, "¿?", 1450, 480, 420, t, d_respondio - 0.1, color=AM, fnt="serif")
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 2, 3, 6), W / 2, 985, 84), t, "serif", 84)


@toma(d_quiso - PAD, d_emperador - 0.1, ent=("latigo", 0.35))
def t_duenos_libro(lz, t):
    tl = t - (d_quiso - PAD)
    lz[:] = D.pozo_luz(0.5, 0.45, 0.8, (0.26, 0.19, 0.11))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.14, W / 2, H / 2 + 10, 0.0), d_emperador - d_quiso + 0.4, mano=0.8)(tl)
    sp = folio(1, 960)
    u = e_out(prog(t, d_quiso - PAD, d_quiso + 0.8))
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(1500, 620, u), 540, 1.0, lerp(14, -3, u), lerp(-40, -8, u)), smooth(prog(t, d_quiso - PAD, d_quiso + 0.2)))
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 2, 12, 17), W / 2, 985, 80), t, "serif", 80, salida=d_carta - 0.1)
    D.dibujar_bloque(lz, bloque(kar("duenos", 3, 2, 4), W / 2, 985, 84), t, "serif", 84)


@toma(d_emperador - PAD, I0 - 0.1, ent=("latigo", 0.35), grado=dict(calido=0.07))
def t_duenos_rodolfo(lz, t):
    tl = t - (d_emperador - PAD)
    D.foto_parallax(lz, "rodolfo_arcimboldo", tl, I0 - d_emperador + 0.6, 1.02, 1.22, (0.5, 0.42), (0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8))
    sombra_lateral(lz, "izq", 0.5)
    D.tag_nombre(lz, "Rodolfo II", 500, 260, t, d_rodolfo - 0.05, 56)
    D.numero(lz, "600", 470, 520, 240, t, d_600 - 0.05, color=RJ, fnt="abril", salida=None)
    carta(lz, pola("ducado", 380, 0.8, (0.3, 0.5)), I3, t, d_ducados - 0.1, 1560, 690, 5, desde=(300, 300))
    D.dibujar_bloque(lz, bloque([("Ducados", d_ducados), ("De", T("duenos", "de", frase=3, n=1)), ("Oro", d_oro)], 470, 700, 92, lineas=(1,)), t, "serif", 92)


# ================================================================== INTENTOS
@toma(I0 - PAD, I1 - 0.1, ent=("desenfoque", 0.45), grado=dict(sat=0.7))
def t_int_friedman(lz, t):
    tl = t - (I0 - PAD)
    D.foto_parallax(lz, "friedman", tl, I1 - I0 + 0.6, 1.05, 1.28, (0.32, 0.42), (0.34, 0.36), par=(80, 18), tono=(0.9, 0.9, 0.9))
    sombra_lateral(lz, "der", 0.5)
    D.tag_nombre(lz, "William Friedman", 560, 820, t, i_william - 0.05, 52)
    carta(lz, pola("purple", 380, 1.05, (0.5, 0.42), "Máquina Púrpura"), I3, t, i_purpura - 0.3, 1560, 760, 4, desde=(300, 300))
    D.dibujar_bloque(lz, bloque(kar("intentos", 0, 10, 15), 1480, 330, 80, lineas=(2, 4)), t, "serif", 80)


def _linea_eva(k):
    ws = PALABRAS_VOY[200 + 17 * k: 200 + 17 * k + 14]
    return " ".join(ws)


@toma(I1 - PAD, I2 - 0.1, ent=("latigo", 0.35))
def t_int_tarjetas(lz, t):
    tl = t - (I1 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.5, 0.85, (0.20, 0.16, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.1, W / 2, H / 2 - 8, 0.0), I2 - I1 + 0.4, mano=0.7)(tl)
    for k, (ti, x, y, r) in enumerate(((i_copio - 0.1, 700, 300, -5), (i_linea - 0.1, 1100, 480, 3), (i_tarjetas - 0.1, 800, 690, -2))):
        sp = D.tarjeta_perforada(_linea_eva(k), k)
        carta(lz, sp, cam, t, ti, x, y, r, s=0.78, desde=(-900, 0), dur=0.55, fase=k)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("intentos", 1, 6, 9), W / 2, 985, 84), t, "serif", 84, salida=i_tarjetas - 0.15)
    D.dibujar_bloque(lz, bloque(kar("intentos", 1, 10, 12), W / 2, 985, 84), t, "serif", 84)


@toma(I2 - PAD, I3_ - 0.1, ent=("latigo", 0.35))
def t_int_fracaso(lz, t):
    tl = t - (I2 - PAD)
    lz[:] = D.pozo_luz(0.35, 0.45, 0.8, (0.24, 0.17, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.1, W / 2 - 20, H / 2, 0.0), I3_ - I2 + 0.3, mano=0.8)(tl)
    sp = folio(190, 900)
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, 600, 520, 1.0, -3, -6), smooth(prog(t, I2 - PAD, I2 + 0.3)))
    for k, (x, y, w_, h_) in enumerate(((440, 300, 170, 70), (700, 480, 190, 70), (520, 690, 170, 70))):
        D.marcador_mano(lz, "circulo", x, y, w_, h_, prog(t, i_pudo + 0.15 * k, i_pudo + 0.4 + 0.3 * k), semilla=k)
    D.marcador_mano(lz, "tachado", 600, 520, 620, 700, prog(t, i_desc + 0.1, i_desc + 0.6), grosor=12)
    D.dibujar_bloque(lz, bloque(kar("intentos", 2, 0, 3), 1400, 300, 90, lineas=(1,)), t, "serif", 90, salida=i_lenguaje - 0.2)
    D.dibujar_bloque(lz, bloque([("Lenguaje", i_lenguaje), ("Artificial", i_artificial), ("¿?", i_artificial + 0.4)], 1400, 620, 96, lineas=(1,), color=BL), t, "serif", 96)


@toma(I3_ - PAD, I4 - 0.1, ent=("desenfoque", 0.35), grado=dict(fuerza_vineta=0.8))
def t_int_ruido(lz, t):
    tl = t - (I3_ - PAD)
    D.foto_parallax(lz, HD("f187"), tl, I4 - I3_ + 0.6, 2.0, 2.9, (0.3, 0.3), (0.62, 0.62), par=(0, 0), tono=(0.62, 0.6, 0.55))
    franja_texto(lz, 0.6, 0.74)
    D.dibujar_bloque(lz, bloque(kar("intentos", 3, 7, 12), W / 2, 985, 92), t, "serif", 92)


@toma(I4 - PAD, I5 - 0.1, ent=("desenfoque", 0.4))
def t_int_zipf(lz, t):
    tl = t - (I4 - PAD)
    D.foto_parallax(lz, HD("f187"), tl, I5 - I4 + 0.6, 1.6, 1.95, (0.5, 0.4), (0.5, 0.5), par=(0, 0), tono=(0.32, 0.31, 0.29))
    D.grafica_zipf(lz, ZIPF, t, i_patrones - 0.6, W / 2, 470, 1240, 660, dur=max(2.0, i_real - i_patrones + 0.4))
    D.dibujar_bloque(lz, bloque(kar("intentos", 4, 5, 12), W / 2, 930, 72), t, "serif", 72)
    tx = D.palabra_img("37 945 palabras cada una · Fuentes: transcripción de Takahashi y Project Gutenberg", "sans_l", 26, (0.85, 0.85, 0.82), stroke=0.05, glow=0.4)
    D.mezclar_pm(lz, tx[0], tx[1], int(W / 2 - tx[0].shape[1] / 2), 1012, smooth(prog(t, i_patrones + 0.6, i_patrones + 1.0)))


@toma(I5 - PAD, T0 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.8))
def t_int_cifras(lz, t):
    tl = t - (I5 - PAD)
    D.foto_parallax(lz, HD("f190"), tl, T0 - I5 + 0.6, 1.7, 2.2, (0.3, 0.3), (0.6, 0.55), par=(0, 0), tono=(0.36, 0.34, 0.30))
    n = int(38000 * e_out(prog(t, i_treinta - 0.1, i_palabras)))
    if t >= i_treinta - 0.1:
        pm, a, m = D.palabra_img(f"{n:,}".replace(",", " "), "sans", 190, tuple(BL), stroke=0.03, glow=0.75)
        D.mezclar_pm(lz, pm, a, int(560 - pm.shape[1] / 2), int(430 - pm.shape[0] / 2), smooth(prog(t, i_treinta - 0.1, i_treinta + 0.1)))
    D.dibujar_bloque(lz, bloque([("Palabras", i_palabras)], 560, 600, 84), t, "serif", 84)
    D.numero(lz, "20–25", 1400, 430, 190, t, i_veinte - 0.1, color=RJ, fnt="abril")
    D.dibujar_bloque(lz, bloque([("Símbolos", i_simbolos)], 1400, 600, 84), t, "serif", 84)


# ================================================================== TEORÍAS (tablero de evidencias)
@toma(T0 - PAD, K0 - 0.1, ent=("latigo", 0.4))
def t_teorias(lz, t):
    tl = t - (T0 - PAD)
    lz[:] = 0
    cam = D.Cam((1.0, C0[0], C0[1], 0.0), (1.16, C0[0] + 40, C0[1] + 10, -1.0), K0 - T0 + 0.4, mano=0.8)(tl)
    D.pegar(lz, corcho(), cam @ D.poner(3400, 2000, C0[0], C0[1]))
    cx, cy = C0
    centro = (cx, cy - 20)
    tarjetas = (("alberti", "Código", -520, -60, -5, t_codigo, "Disco de cifrado"), ("f190", "Idioma inventado", 20, 200, 3, t_idioma_t, None),
                ("f110", "Fraude", 500, -80, -3, t_fraude, "¿Fraude medieval?"))
    pins = []
    for k, (nom, _, dx, dy, r, ti, ley) in enumerate(tarjetas):
        sp = pola(nom, 400, 1.15, (0.5, 0.5), ley) if not nom.startswith("f1") or nom == "f110" else pola(nom, 400, 1.15, (0.5, 0.35), ley)
        carta(lz, sp, cam, t, ti - 0.1, cx + dx, cy + dy, r, desde=(0, -420), fase=k * 1.3)
        if t > ti + 0.3:
            pins.append((cx + dx, cy + dy - 290 if k != 1 else cy + dy - 290))
    # tarjeta central con la pregunta
    if t > T0 + 0.1:
        q = spr("pregunta", lambda: D.Sprite(np.full((240, 380, 3), (240, 235, 220), np.uint8), None, sombra=True, sr=12))
        M = cam @ D.poner(q.w, q.h, cx, cy - 150, 1.0, 1.5)
        D.pegar(lz, q, M, smooth(prog(t, T0 + 0.1, T0 + 0.4)))
        pm, a, m = D.palabra_img("¿Qué es?", "serif", 88, (0.72, 0.05, 0.05), stroke=0.02, glow=0.0)
        x, y = D.tf(M, cx, cy - 150)
        D.mezclar_pm(lz, pm, a, int(x - pm.shape[1] / 2), int(y - pm.shape[0] / 2), smooth(prog(t, T0 + 0.2, T0 + 0.5)))
    for a, b in zip(pins, pins[1:] + pins[:1]):
        pass
    for k, p in enumerate(pins):
        D.hilo(lz, cam, (cx, cy - 265), p, smooth(prog(t, (t_codigo, t_idioma_t, t_fraude)[k] + 0.2, (t_codigo, t_idioma_t, t_fraude)[k] + 0.7)))
    D.pin(lz, cam, cx, cy - 265)
    for p in pins:
        D.pin(lz, cam, *p)
    # X rojas: ninguna teoría convenció
    for k, ti in enumerate((t_ninguna, t_teoria, t_convencido)):
        dx, dy = tarjetas[k][2], tarjetas[k][3]
        x, y = D.tf(cam, cx + dx, cy + dy)
        D.marcador_mano(lz, "tachado", x, y, 340, 420, prog(t, ti, ti + 0.3), grosor=16)
        D.marcador_mano(lz, "tachado", x, y, -340, 420, prog(t, ti + 0.12, ti + 0.42), grosor=16)
    franja_texto(lz, 0.5, 0.78)
    D.dibujar_bloque(lz, bloque(kar("teorias", 0, 4, 6), W / 2, 985, 84), t, "serif", 84, salida=t_idioma_t - 0.15)
    D.dibujar_bloque(lz, bloque(kar("teorias", 0, 7, 10), W / 2, 985, 84), t, "serif", 84, salida=T1 - 0.05)
    D.dibujar_bloque(lz, bloque(kar("teorias", 1, 5, 9), W / 2, 985, 84), t, "serif", 84, salida=T2 - 0.05)
    D.dibujar_bloque(lz, bloque(kar("teorias", 2, 0, 4), W / 2, 985, 84, color=BL), t, "serif", 84)


# ================================================================== CIERRE
@toma(K0 - PAD, K1 - 0.1, ent=("negro", 0.5), grado=dict(destello=0.05))
def t_cierre_beinecke(lz, t):
    tl = t - (K0 - PAD)
    D.foto_parallax(lz, "beinecke_interior", tl, K1 - K0 + 0.6, 1.05, 1.24, (0.5, 0.55), (0.5, 0.42), par=(70, 14), tono=(0.95, 0.9, 0.85))
    D.tag_nombre(lz, "Biblioteca Beinecke", 470, 820, t, k_beinecke - 0.05, 54)
    D.tag_nombre(lz, "Universidad de Yale · MS 408", 520, 910, t, k_yale - 0.05, 40, rot=2.0)
    franja_texto(lz, 0.35, 0.8)


@toma(K1 - PAD, K2 - 0.1, ent=("desenfoque", 0.4))
def t_cierre_internet(lz, t):
    tl = t - (K1 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.5, 0.85, (0.17, 0.15, 0.13))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2, H / 2 - 8, 0.0), K2 - K1 + 0.4, mano=0.6)(tl)
    vent = spr("ventana", lambda: _ventana())
    D.pegar(lz, vent, cam @ D.poner(vent.w, vent.h, W / 2, 500, 1.0, 0.0), smooth(prog(t, K1 - PAD, K1 + 0.3)))
    # páginas que se desplazan dentro de la ventana (vista previa de la biblioteca digital)
    nomb = (4, 7, 10, 24, 32, 110, 111, 136, 141, 147, 175, 176)
    ancho, alto = 220, 300
    for k, n in enumerate(nomb):
        col, fila = k % 6, k // 6
        x = 560 + col * 155 + 10
        y = 400 + fila * 260 - 30 * math.sin(0.7 * t + k)
        sp = pola(f"f{n:03d}", 200, 1.36, (0.5, 0.45))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, x + 40, y + 20, 0.62, (k % 3 - 1) * 2.0), smooth(prog(t, k_internet - 0.2 + 0.05 * k, k_internet + 0.3 + 0.05 * k)))
    D.numero(lz, "Unos 600 años", W / 2, 240, 150, t, k_600 - 0.1, color=AM, fnt="serif")
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("cierre", 1, 0, 5), W / 2, 985, 76), t, "serif", 76, salida=k_600 - 0.15)
    D.dibujar_bloque(lz, bloque(kar("cierre", 1, 10, 14), W / 2, 985, 84), t, "serif", 84)


def _ventana():
    w, h = 1300, 760
    im = np.zeros((h, w, 3), np.uint8)
    im[:] = (26, 26, 28)
    cv2.rectangle(im, (0, 0), (w, 66), (44, 44, 48), -1)
    for k, c in enumerate(((70, 70, 220), (60, 190, 240), (80, 200, 90))):
        cv2.circle(im, (34 + k * 34, 33), 10, c[::-1], -1, cv2.LINE_AA)
    cv2.rectangle(im, (150, 14), (w - 60, 52), (20, 20, 22), -1)
    from PIL import Image, ImageDraw
    pil = Image.fromarray(im)
    ImageDraw.Draw(pil).text((176, 33), "collections.library.yale.edu", font=D.fuente("sans_l", 24), fill=(200, 200, 195), anchor="lm")
    im = np.asarray(pil)
    return D.Sprite(im, None, sombra=True, sr=26, off=(18, 26), sop=0.7)


@toma(K2 - PAD, TOTAL + 1.0, ent=("desenfoque", 0.4), grado=dict(destello=0.06))
def t_cierre_pregunta(lz, t):
    tl = t - (K2 - PAD)
    D.foto_parallax(lz, HD("f003"), tl, TOTAL - K2 + 0.6, 1.5, 2.3, (0.4, 0.3), (0.52, 0.5), par=(0, 0), tono=(0.72, 0.66, 0.56))
    franja_texto(lz, 0.6, 0.66)
    D.dibujar_bloque(lz, bloque(kar("cierre", 2, 1, 8), W / 2, 905, 84, lineas=(4,)), t, "serif", 84, salida=k_o - 0.1)
    D.dibujar_bloque(lz, bloque(kar("cierre", 2, 8, 15), W / 2, 905, 84, lineas=(4,), color=BL), t, "serif", 84)
    # cierre: fundido a negro y título con créditos
    fin = FIN_VOZ + 0.6
    lz *= 1 - smooth(prog(t, fin, fin + 0.9))
    if t > fin + 0.5:
        u = smooth(prog(t, fin + 0.5, fin + 1.2))
        D.numero(lz, "El libro que nadie puede leer", W / 2, H / 2 - 30, 92, t, fin + 0.5, color=AM, fnt="serif", pop=False)
        D.numero(lz, "Escaneos: Beinecke Rare Book & Manuscript Library, Yale University (MS 408) · Wikimedia Commons", W / 2, H / 2 + 120, 26, t, fin + 0.9, color=(0.8, 0.8, 0.78), fnt="sans_l", pop=False)


TOMAS.sort(key=lambda d: d["t0"])


# ================================================================== Mundo
class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        e = self.ev
        e(0.2, "latido", 0.7, dur=1.6)
        e(g_nadie - 0.05, "impacto", 0.6)
        for ti, v in ((g_240, 0.5), (g_dib, 0.4), (g_imp + 0.1, 0.4), (g_cripto, 0.4), (g_mil, 0.4)):
            e(ti - 0.05, "papel", v)
        e(g_idioma, "escribir", 0.4, dur=0.9)
        e(g_comp, "glitch", 0.35)
        e(g_logrado - 0.05, "sello", 0.8)
        e(o_doce - 0.1, "impacto", 0.6)
        e(o_wilfrid - 0.05, "papel", 0.5)
        e(o_colegio, "brillo", 0.4)
        e(o_apellido - 0.05, "sello", 0.5)
        for ti in (c_plantas, c_existen, c_herb - 0.15):
            e(ti - 0.1, "papel", 0.5)
        e(c_estrellas - 0.1, "brillo", 0.4)
        e(c_mujeres - 0.1, "whoosh", 0.35, dur=0.5)
        e(c_alfabeto, "escribir", 0.45, dur=1.0)
        e(c_quien - 0.05, "latido", 0.6, dur=1.0)
        for k in range(4):
            e(f_arizona - 0.2 + 0.28 * k, "obturador", 0.4)
        e(f_2009, "impacto", 0.5)
        e(f_carbono, "ding", 0.35)
        e(f_entre, "whoosh", 0.3, dur=0.6)
        e(f_ocho, "tick", 0.5)
        e(f_moderna + 0.35, "garabato", 0.5, dur=0.4)
        n_p = 14
        p_ini, p_paso = f_menos - 0.1, max(0.06, (f_ternero - (f_menos - 0.1) - 0.2) / 14)
        for k in range(n_p):
            e(p_ini + k * p_paso, "papel", 0.28, tono=0.9 + 0.02 * k)
        e(f_eamon, "papel", 0.4)
        e(d_rastro, "viento", 0.35, dur=1.4)
        e(d_1639 - 0.05, "impacto", 0.5)
        e(d_georg, "papel", 0.4)
        e(d_kircher, "papel", 0.45)
        e(d_respondio - 0.1, "latido", 0.5, dur=1.0)
        e(d_quiso, "whoosh", 0.35, dur=0.6)
        e(d_rodolfo, "campana", 0.35)
        e(d_600 - 0.05, "impacto", 0.55)
        e(d_ducados, "clink", 0.5)
        e(i_william, "papel", 0.5)
        e(i_purpura - 0.3, "papel", 0.5)
        for ti in (i_copio, i_linea, i_tarjetas):
            e(ti - 0.1, "papel", 0.5)
            e(ti + 0.2, "tick", 0.4)
        for k in range(3):
            e(i_pudo + 0.15 * k, "garabato", 0.45, dur=0.4)
        e(i_desc + 0.1, "garabato", 0.5, dur=0.5)
        e(i_ruido, "latido", 0.5, dur=1.0)
        e(i_patrones - 0.6, "revelar", 0.5)
        e(i_treinta - 0.1, "escribir", 0.4, dur=1.4)
        e(i_veinte - 0.1, "impacto", 0.5)
        for ti in (t_codigo, t_idioma_t, t_fraude):
            e(ti - 0.1, "papel", 0.5)
            e(ti + 0.3, "pin", 0.5)
        for ti in (t_ninguna, t_teoria, t_convencido):
            e(ti, "garabato", 0.5, dur=0.35)
        e(k_beinecke, "eco", 0.35)
        e(k_internet, "tick", 0.4)
        e(k_600 - 0.1, "impacto", 0.5)
        e(k_o - 0.05, "latido", 0.55, dur=1.2)
        e(FIN_VOZ + 1.0, "impacto", 0.6)

    def render(self, lz, t):
        i = 0
        for k, d in enumerate(TOMAS):
            if d["t0"] <= t:
                i = k
        d = TOMAS[i]
        img = np.zeros((H, W, 3), np.float32)
        d["fn"](img, t)
        tipo, dur = d["ent"]
        if i > 0 and t < d["t0"] + dur:
            A = np.zeros((H, W, 3), np.float32)
            TOMAS[i - 1]["fn"](A, t)
            img = D.mezcla_tomas(A, img, (t - d["t0"]) / dur, tipo)
        img = D.acabado(img, t, **d["grado"])
        img *= smooth(prog(t, 0.0, 0.9))
        return np.clip(img, 0, 1).astype(np.float32)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
