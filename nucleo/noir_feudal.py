# -*- coding: utf-8 -*-
"""NOIR FEUDAL: la variante medieval del noir a color (nucleo/noir_color.py). Misma esencia (tinta y aguada, claroscuro, lluvia
que solo brilla con la luz, niebla, humo, tramado, papel y grano) en una época feudal: un PESQUISIDOR encapuchado (el detective
de la época) investiga casos, personas y sucesos antiguos. Para historias de reinos, dinastías y guerras (sagas de fantasía
medieval, historia antigua y medieval). La luz ya no es sodio y neón: ANTORCHA, VELA y LUNA; el acento es el LACRE rojo.

    import noir_color as NC, noir_feudal as NF
    h = NC.NoirColor("antorcha")                         # paleta registrada aquí (también "pergamino": más cálida, para interiores)
    # fondos (noir_fondos.Lienzo en gris; color con NC.pegar(capa, h, prof, rampa="muralla"|"entramado"|"teja"...)):
    NF.muralla(L, x0, x1, base, alto) · NF.torre(L, cx, base, ancho, alto, techo="conico"|"almenas") · NF.saetera(L, ...)
    NF.casa_entramado(L, x, base, ancho, alto) · NF.sillares(L, x, y, w, h) · NF.soporte_antorcha(L, x, y) · NF.adoquines(L, ...)
    # por cuadro:
    NF.llama(h, t, x, y, s)            # fuego vivo (emisivo) -> devuelve la intensidad para su luz;  NF.antorcha(h, t, x, y)
    NF.vela(h, t, x, y, s)             # vela con cera derretida y llama;  NF.estandarte(h, t, x, y, w, hh)  tela que ondea
    NF.lacre(h, t, t0, x, y, r)        # sello de lacre que cae, se aplasta y deja el emblema
    NF.Pesquisidor(sem)                # cuerpo entero (Detective con capucha, capa y farol; camina igual: avance_paso)
    NF.BustoEncapuchado(sem)           # primer plano de perfil con capucha, barba y vaho de aliento
Doc: docs/estilo_noir_color.md § «Variante FEUDAL». Prueba: videos/prueba_noir_feudal/.
"""
import math

import numpy as np

import noir as N
import noir_color as NC
from motor import clamp01, smooth
from noir import gris
from noir_pers import Detective, _ik
from toon import blob, eje_curvo, elipse_, suave, tubo

FUENTE_GOTICA = "C:/Windows/Fonts/OLDENGL.TTF"     # titulares (letra gótica)
FUENTE_PLUMA = "C:/Windows/Fonts/BOOKOSB.TTF"      # cuerpo escrito a pluma (Bookman: se lee bien pequeño)
FUENTE_PLUMA_R = "C:/Windows/Fonts/BOOKOSI.TTF"

# ================================================================ paletas y rampas de la época
NC.PALETAS["antorcha"] = dict(
    sat=0.62, negro=(0.020, 0.020, 0.030), blanco=(0.97, 0.92, 0.80), sombra=(0.86, 0.97, 1.12), luz=(1.12, 0.97, 0.76),
    niebla=(0.055, 0.075, 0.10), aditivo=(0.55, 0.68, 0.85),
    colores=dict(sodio=(1.75, 0.90, 0.38), antorcha=(1.75, 0.90, 0.38), luna=(0.58, 0.76, 1.0), neon=(1.0, 0.22, 0.10),
                 lampara=(1.55, 1.0, 0.52), vela=(1.55, 1.0, 0.52), verde=(0.45, 0.95, 0.55), relampago=(0.80, 0.90, 1.0),
                 sello=(0.52, 0.05, 0.04), lacre=(0.62, 0.07, 0.05), tinta=(0.035, 0.025, 0.03), papel=(0.90, 0.82, 0.62)))
NC.PALETAS["pergamino"] = dict(
    sat=0.55, negro=(0.026, 0.020, 0.020), blanco=(0.96, 0.90, 0.76), sombra=(0.92, 0.98, 1.06), luz=(1.14, 0.98, 0.74),
    niebla=(0.07, 0.065, 0.06), aditivo=(0.75, 0.70, 0.60),
    colores=dict(sodio=(1.70, 0.95, 0.45), antorcha=(1.70, 0.95, 0.45), luna=(0.66, 0.80, 0.98), neon=(0.95, 0.25, 0.12),
                 lampara=(1.5, 1.02, 0.58), vela=(1.5, 1.02, 0.58), verde=(0.5, 0.9, 0.5), relampago=(0.85, 0.92, 1.0),
                 sello=(0.50, 0.06, 0.04), lacre=(0.60, 0.08, 0.05), tinta=(0.04, 0.03, 0.025), papel=(0.92, 0.84, 0.64)))

NC.RAMPAS.update({
    "muralla": [(0.00, (0.020, 0.026, 0.040)), (0.14, (0.120, 0.130, 0.140)), (0.30, (0.300, 0.290, 0.260)),
                (0.55, (0.560, 0.520, 0.440)), (1.00, (0.950, 0.900, 0.780))],
    "entramado": [(0.00, (0.025, 0.020, 0.025)), (0.15, (0.150, 0.090, 0.060)), (0.35, (0.420, 0.300, 0.190)),
                  (0.60, (0.700, 0.580, 0.420)), (1.00, (0.970, 0.900, 0.740))],
    "teja": [(0.00, (0.015, 0.020, 0.035)), (0.20, (0.110, 0.130, 0.160)), (0.45, (0.330, 0.340, 0.360)),
             (1.00, (0.880, 0.860, 0.820))],
    "lana": [(0.00, (0.020, 0.024, 0.030)), (0.15, (0.110, 0.110, 0.090)), (0.30, (0.270, 0.250, 0.180)),
             (0.55, (0.500, 0.450, 0.330)), (1.00, (0.920, 0.870, 0.760))],
    "cuero": [(0.00, (0.025, 0.018, 0.015)), (0.20, (0.220, 0.120, 0.070)), (0.45, (0.480, 0.300, 0.170)),
              (1.00, (0.920, 0.780, 0.600))],
    "hierro": [(0.00, (0.015, 0.020, 0.030)), (0.30, (0.180, 0.200, 0.220)), (0.65, (0.500, 0.520, 0.530)),
               (1.00, (0.950, 0.950, 0.920))],
    "estandarte": [(0.00, (0.030, 0.010, 0.015)), (0.20, (0.200, 0.030, 0.040)), (0.45, (0.480, 0.090, 0.080)),
                   (0.70, (0.700, 0.300, 0.220)), (1.00, (0.980, 0.820, 0.600))],
    "pergamino": [(0.00, (0.035, 0.028, 0.025)), (0.35, (0.400, 0.310, 0.200)), (0.70, (0.780, 0.660, 0.460)),
                  (1.00, (0.980, 0.920, 0.740))],
    "cera": [(0.00, (0.030, 0.025, 0.020)), (0.40, (0.480, 0.400, 0.300)), (0.75, (0.860, 0.780, 0.620)),
             (1.00, (1.000, 0.960, 0.860))],
    "lacre": [(0.00, (0.040, 0.008, 0.010)), (0.30, (0.330, 0.030, 0.030)), (0.60, (0.620, 0.090, 0.060)),
              (1.00, (1.000, 0.600, 0.450))],
    "oro": [(0.00, (0.030, 0.022, 0.010)), (0.30, (0.360, 0.240, 0.060)), (0.65, (0.800, 0.620, 0.250)),
            (1.00, (1.000, 0.950, 0.720))],
})


# ================================================================ fondos (Lienzo gris de noir_fondos)
def sillares(L, x, y, w, hh, tono=0.22, hilada=38.0, largo=(60, 120), sem=0, junta=0.05, var=0.05):
    """Paño de piedra de sillería: hiladas con juntas verticales alternas; cada bloque con su tono y un canto de luz arriba."""
    rng = np.random.default_rng(sem)
    L.rect(x, y, w, hh, tono, tex=0.12)
    yy = y
    fila = 0
    while yy < y + hh - 1:
        hb = min(hilada * rng.uniform(0.85, 1.15), y + hh - yy)
        xx = x - (rng.uniform(0, largo[0]) if fila % 2 else 0)
        while xx < x + w:
            lb = rng.uniform(*largo)
            x0, x1 = max(x, xx), min(x + w, xx + lb)
            if x1 - x0 > 4:
                L.rect(x0 + 1.5, yy + 1.5, x1 - x0 - 3, hb - 3, tono + rng.uniform(-var, var), tex=0.10, alfa=0.9)
                L.linea([(x0 + 2, yy + 2), (x1 - 2, yy + 2)], 1.0, tono + 0.18, alfa=0.35, jit=0.3)
                if rng.uniform() < 0.12:                                   # piedra desconchada
                    L.elipse(rng.uniform(x0, x1), yy + hb * rng.uniform(0.3, 0.7), rng.uniform(6, 14), rng.uniform(4, 8),
                             tono - 0.08, alfa=0.6, rug=1.0)
            L.linea([(xx, yy), (xx, yy + hb)], 1.6, junta, alfa=0.8, jit=0.4)
            xx += lb
        L.linea([(x, yy), (x + w, yy)], 1.8, junta, alfa=0.85, jit=0.4)
        yy += hb
        fila += 1


def saetera(L, x, y, w=16, hh=90, encendida=0.0):
    """Saetera (ventana-aspillera): rendija alta con derrame; si está encendida, emite (luz de antorcha dentro)."""
    L.poli([(x - w * 1.3, y - 6), (x + w * 1.3, y - 6), (x + w * 1.3, y + hh + 6), (x - w * 1.3, y + hh + 6)], 0.10, alfa=0.8)
    if encendida > 0:
        L.rect(x - w / 2, y, w, hh, 0.6 + 0.35 * encendida, tex=0.03, emis=0.75 * encendida)
        L.brillo(x, y + hh / 2, w * 2.4, 0.15 * encendida, ry=hh * 0.8, tono=0.7)
    else:
        L.rect(x - w / 2, y, w, hh, 0.03)
    L.linea([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + hh), (x - w / 2, y + hh)], 1.6, 0.02, cerrado=True, jit=0.2)


def almenas(L, x0, x1, top, tono=0.24, ancho=46.0, hueco=30.0, alto=46.0, sem=0):
    """Merlones sobre el adarve (top = y de la base de las almenas)."""
    x = x0
    while x < x1:
        w = min(ancho, x1 - x)
        sillares(L, x, top - alto, w, alto, tono, hilada=23, largo=(20, 46), sem=abs(sem + int(x)))
        L.linea([(x, top - alto), (x + w, top - alto), (x + w, top), (x, top)], 2.0, 0.02, cerrado=True, jit=0.3)
        L.linea([(x + 2, top - alto + 1), (x + w - 2, top - alto + 1)], 2.0, 0.6, alfa=0.55, jit=0.2)  # canto de luna
        x += ancho + hueco


def muralla(L, x0, x1, base, alto, tono=0.22, sem=0, saeteras=0.35, encendidas=0.3, almena=True):
    """Lienzo de muralla de sillería con almenas, matacanes de sombra y saeteras (algunas encendidas)."""
    rng = np.random.default_rng(sem)
    top = base - alto
    sillares(L, x0, top, x1 - x0, alto, tono, sem=sem)
    L.poli([(x0, top), (x1, top), (x1, top + 26), (x0, top + 26)], tono * 0.55, alfa=0.8)       # sombra del adarve
    for xx in np.arange(x0 + 20, x1 - 20, 56):                                                  # canecillos
        L.rect(xx, top + 18, 14, 18, tono * 0.7)
    L.linea([(x0, top), (x1, top)], 2.4, 0.02)
    if almena:
        almenas(L, x0, x1, top, tono, sem=sem)
    for xx in np.arange(x0 + 90, x1 - 60, 170):
        if rng.uniform() < saeteras:
            saetera(L, xx, top + alto * rng.uniform(0.25, 0.5), encendida=rng.uniform(0.6, 1.0) if rng.uniform() < encendidas else 0)
    L.trama([(x0, base - alto * 0.25), (x1, base - alto * 0.25), (x1, base), (x0, base)], ang=60, sep=9, tono=0.02, alfa=0.25)


def torre(L, cx, base, ancho, alto, techo="conico", tono=0.24, sem=0, encendidas=0.4):
    """Torre de piedra cuadrada con saeteras; techo cónico de pizarra (con veleta) o almenada."""
    rng = np.random.default_rng(sem)
    x = cx - ancho / 2
    top = base - alto
    sillares(L, x, top, ancho, alto, tono, sem=sem)
    L.poli([(x + ancho * 0.62, top), (x + ancho, top), (x + ancho, base), (x + ancho * 0.62, base)], tono * 0.5, alfa=0.55)
    L.trama([(x + ancho * 0.62, top), (x + ancho, top), (x + ancho, base), (x + ancho * 0.62, base)], ang=65, sep=7, tono=0.02,
            alfa=0.35)
    L.linea([(x, top), (x + ancho, top), (x + ancho, base), (x, base)], 2.6, 0.02, cerrado=True, sem=sem)
    for k, yy in enumerate(np.arange(top + 80, base - 120, 150)):
        saetera(L, cx + rng.uniform(-ancho * 0.18, ancho * 0.1), yy, encendida=rng.uniform(0.6, 1) if rng.uniform() < encendidas else 0)
    if techo == "conico":
        L.rect(x - 12, top - 14, ancho + 24, 18, tono * 1.3, tex=0.06)
        h = ancho * 1.25
        P = [(x - 18, top - 10), (cx, top - 10 - h), (x + ancho + 18, top - 10)]
        L.poli(P, tono * 0.75, tex=0.1, grad=(tono * 0.4, top - h, top))
        for k in range(1, 9):                                         # hiladas de pizarra
            f = k / 9
            yk = top - 10 - h * (1 - f)
            hw = (ancho / 2 + 18) * f
            L.linea([(cx - hw, yk), (cx + hw, yk)], 1.2, 0.05, alfa=0.6, jit=0.3)
        L.linea([(cx - ancho * 0.1, top - 10 - h * 0.9), (cx - ancho * 0.3, top - 10)], 2.0, 0.55, alfa=0.5)   # brillo de luna
        L.linea(P, 2.6, 0.02, cerrado=True)
        L.linea([(cx, top - 10 - h), (cx, top - 10 - h - 60)], 3, 0.03)                                # veleta
        L.poli([(cx, top - h - 66), (cx + 34, top - h - 58), (cx, top - h - 50)], 0.05)
    else:
        almenas(L, x - 10, x + ancho + 10, top, tono, ancho=34, hueco=22, alto=40, sem=sem)


def casa_entramado(L, x, base, ancho, alto, sem=0, encendidas=0.4, tono=0.40):
    """Casa de entramado de madera: zócalo de piedra, revoque claro con vigas oscuras (cruces de San Andrés), piso alto en
    voladizo, tejado inclinado de tablillas y ventanucos emplomados (encendidos con luz de vela)."""
    rng = np.random.default_rng(sem)
    top = base - alto
    sillares(L, x, base - 70, ancho, 70, 0.20, hilada=24, largo=(30, 60), sem=sem)
    for k, (y0, y1, dx) in enumerate(((base - alto * 0.5, base - 70, 0), (top, base - alto * 0.5, -18))):
        x0, x1 = x + dx, x + ancho - dx
        L.rect(x0, y0, x1 - x0, y1 - y0, tono, tex=0.14)                                        # revoque
        vigas = [((x0, y0), (x1, y0)), ((x0, y1), (x1, y1))]
        n = max(2, int((x1 - x0) // 90))
        xs = np.linspace(x0, x1, n + 1)
        for xa in xs:
            vigas.append(((xa, y0), (xa, y1)))
        for a, b in zip(xs[:-1], xs[1:]):
            if rng.uniform() < 0.45:
                vigas.append(((a, y0), (b, y1)))
                vigas.append(((b, y0), (a, y1)))
        for p0, p1 in vigas:
            L.linea([p0, p1], 9, 0.10, jit=0.6, sem=sem + k)
        for a, b in zip(xs[:-1], xs[1:]):                                                       # ventanuco
            if rng.uniform() < 0.55:
                wx, wy, ww, wh = (a + b) / 2 - 18, y0 + (y1 - y0) * 0.3, 36, (y1 - y0) * 0.38
                enc = rng.uniform() < encendidas
                L.rect(wx, wy, ww, wh, (0.75 if enc else 0.06), tex=0.04, emis=0.7 if enc else 0.0)
                for j in range(1, 4):                                                           # plomo en rombos
                    L.linea([(wx, wy + wh * j / 4), (wx + ww, wy + wh * j / 4 - 8)], 1.0, 0.05, alfa=0.7, jit=0)
                L.linea([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], 1.2, 0.05, jit=0)
                L.linea([(wx, wy), (wx + ww, wy), (wx + ww, wy + wh), (wx, wy + wh)], 2.2, 0.03, cerrado=True)
                if enc:
                    L.brillo(wx + ww / 2, wy + wh / 2, ww * 1.6, 0.18, ry=wh, tono=0.75)
    # tejado
    al = alto * rng.uniform(0.45, 0.65)
    P = [(x - 34, top + 6), (x + ancho * 0.5, top - al), (x + ancho + 34, top + 6)]
    L.poli(P, 0.16, tex=0.12, grad=(0.08, top - al, top))
    for k in range(1, 8):
        f = k / 8
        yk = top - al * (1 - f)
        hw = (ancho / 2 + 34) * f
        L.linea([(x + ancho / 2 - hw, yk), (x + ancho / 2 + hw, yk)], 1.3, 0.04, alfa=0.6, jit=0.4)
    L.linea([(x - 34, top + 6), (x + ancho * 0.5, top - al)], 2.4, 0.5, alfa=0.5)                # canto de luna
    L.linea(P, 2.6, 0.02, cerrado=True)
    cx = x + ancho * rng.uniform(0.6, 0.8)                                                    # chimenea
    L.rect(cx, top - al * 0.75, 30, al * 0.5, 0.18, tex=0.1)
    L.linea([(cx, top - al * 0.75), (cx + 30, top - al * 0.75)], 2, 0.02)
    # puerta de tablones con herrajes
    px = x + ancho * rng.uniform(0.15, 0.3)
    L.poli([(px, base), (px, base - 120), (px + 30, base - 140), (px + 60, base - 120), (px + 60, base)], 0.13, tex=0.12)
    for j in range(1, 4):
        L.linea([(px + j * 15, base - 130 + abs(j - 2) * 5), (px + j * 15, base)], 1.0, 0.04, alfa=0.7)
    L.linea([(px + 4, base - 90), (px + 50, base - 90)], 3, 0.03)
    L.linea([(px + 4, base - 40), (px + 50, base - 40)], 3, 0.03)
    return top - al


def soporte_antorcha(L, x, y):
    """Argolla de hierro en la pared (la llama se pinta por cuadro con antorcha())."""
    L.linea([(x - 16, y + 40), (x, y + 10), (x + 16, y + 40)], 4, 0.04)
    L.rect(x - 22, y + 36, 44, 10, 0.06)
    L.poli([(x - 9, y + 10), (x + 9, y + 10), (x + 6, y - 40), (x - 6, y - 40)], 0.12, tex=0.1)
    L.brillo(x, y - 40, 120, 0.25, tono=0.75)


def adoquines(L, x0, x1, y0, y1, tono=0.18, sem=0):
    """Suelo de adoquines en perspectiva (más pequeños al fondo), con charcos claros."""
    rng = np.random.default_rng(sem)
    L.rect(x0, y0, x1 - x0, y1 - y0, tono * 0.6, tex=0.12)
    y = y0
    while y < y1:
        f = (y - y0) / max(1.0, y1 - y0)
        hb = 10 + 34 * f
        wb = 22 + 60 * f
        xx = x0 - rng.uniform(0, wb)
        while xx < x1:
            L.elipse(xx + wb / 2, y + hb / 2, wb * 0.46, hb * 0.42, tono + rng.uniform(-0.04, 0.05), alfa=0.95, tex=0.1)
            L.linea([(xx + wb * 0.15, y + hb * 0.25), (xx + wb * 0.7, y + hb * 0.2)], 1.0, tono + 0.2, alfa=0.35, jit=0.2)
            xx += wb
        y += hb
    for k in range(int((x1 - x0) / 160)):
        L.elipse(rng.uniform(x0, x1), rng.uniform(y0 + (y1 - y0) * 0.2, y1), rng.uniform(60, 200), rng.uniform(8, 22), 0.24,
                 alfa=0.6, rug=1.0, tex=0.04)


# ================================================================ fuego, velas, telas y lacre (por cuadro)
def llama(h, t, x, y, s=1.0, sem=0, k=1.0, col=None, mundo=True):
    """Llama viva (x, y = base): lengua principal + dos menores que se separan, con núcleo claro. Emite en la capa emisiva.
    Devuelve la intensidad (0.75..1.1) para modular la luz que proyecta."""
    col = col if col is not None else h.pal.get("antorcha", h.pal["sodio"])
    f = 0.88 + 0.08 * math.sin(t * 17 + sem) + 0.05 * math.sin(t * 29 + sem * 2.3) + 0.04 * math.sin(t * 7.3 + sem)
    for j, (dx, esc, fase) in enumerate(((0, 1.0, 0.0), (-9, 0.62, 1.7), (9, 0.55, 3.1))):
        alto = 70 * s * esc * f * (0.92 + 0.12 * math.sin(t * 11 + sem + fase))
        an = 17 * s * esc
        sway = 7 * s * math.sin(t * 6.3 + sem + fase) * esc
        P = []
        for a in np.linspace(0, 2 * math.pi, 22, endpoint=False):
            v = 0.5 - 0.5 * math.cos(a)                                   # 0 abajo .. 1 arriba (lado derecho), simétrico
            lado = math.sin(a)
            ancho = an * (1 - v) ** 0.7 * (0.6 + 0.4 * math.sin(math.pi * min(1.0, v * 1.4)))
            yy = -alto * v
            P.append((x + dx * s + lado * ancho + sway * v * v, y + yy + 4 * s))
        P = np.array(P)
        h.emitir(P, (0.95 if j == 0 else 0.7) * k, mundo=mundo, blur=2.0 * s, col=col)
        if j == 0:                                                           # núcleo casi blanco
            Q = (P - (x, y)) * (0.45, 0.55) + (x, y + 2 * s)
            h.emitir(Q, 1.3 * k, mundo=mundo, blur=1.2 * s, col=(1.0, 0.95, 0.75))
    h.resplandor(x, y - 26 * s, 90 * s, 0.32 * k * f, col=col, mundo=mundo)
    return f


def antorcha(h, t, x, y, s=1.0, sem=0, k=1.0, luz=1.0, alcance=520.0):
    """Antorcha en la pared: mango de madera, cabeza de brea, llama, humo y su LUZ (cono hacia abajo y halo)."""
    with h.con_rampa("cuero"):
        h.pieza(tubo(np.array([[x, y + 70 * s], [x, y]]), 14 * s, 18 * s), 70, sem, w=3 * s, d=6 * s, trama=0, rim=0.6)
        h.pieza(blob(x, y, 15 * s, 12 * s, n=10), 25, sem + 1, w=3 * s, d=4 * s, trama=0, rim=0.3)
    f = llama(h, t, x, y - 6 * s, s, sem, k)
    col = h.pal.get("antorcha", h.pal["sodio"])
    h.luz_radial(x, y - 30 * s, alcance * s, col, k=0.95 * luz * f)
    h.luz_radial(x, y - 30 * s, alcance * 0.35 * s, col, k=0.6 * luz * f)
    N.humo(h, t, x, y - 70 * s, k=0.5, sem=sem + 3, viento=(10.0, -90.0), vida=2.4, hebras=2, ancho=1.4)
    return f


def vela(h, t, x, y, s=1.0, sem=0, alto=150.0, k=1.0, luz=1.0, alcance=700.0):
    """Vela de sebo sobre palmatoria de hierro: cera con chorretones, pabilo, llama y su luz cálida. (x, y) = base."""
    with h.con_rampa("hierro"):
        h.pieza(elipse_(x, y, 70 * s, 18 * s, n=30), 90, sem, w=4 * s, d=8 * s, trama=0.3, rim=0.7)
        h.pieza(tubo(np.array([[x + 66 * s, y - 4 * s], [x + 96 * s, y - 30 * s], [x + 86 * s, y - 50 * s]]), 8 * s, 6 * s), 80,
                sem + 1, w=3 * s, d=4 * s, trama=0, rim=0.6)
    a = alto * s
    with h.con_rampa("cera"):
        h.pieza([(x - 24 * s, y - 6 * s), (x + 24 * s, y - 6 * s), (x + 22 * s, y - a), (x - 22 * s, y - a)], 200, sem + 2, w=4 * s,
                d=10 * s, trama=0.3, rim=0.8, grad=(235, y - a, y))
        r = np.random.default_rng(sem)
        for j in range(4):                                           # chorretones de cera
            cx = x + r.uniform(-20, 20) * s
            largo = r.uniform(20, 70) * s
            h.pieza(tubo(np.array([[cx, y - a + 2 * s], [cx + r.uniform(-3, 3) * s, y - a + largo]]), 7 * s, 5 * s), 220,
                    sem + 3 + j, w=2 * s, d=2 * s, sombra=0, trama=0, rim=0.6)
        h.pieza(elipse_(x, y - a, 23 * s, 6 * s, n=20), 238, sem + 8, w=2 * s, d=0, sombra=0, rim=0)
    h.trazo(np.array([[x, y - a], [x + 1 * s, y - a - 12 * s]]), 2.2 * s, sem + 9, color=(10, 8, 8))
    f = llama(h, t, x, y - a - 8 * s, 0.55 * s, sem, k, col=h.pal.get("vela", h.pal["lampara"]))
    col = h.pal.get("vela", h.pal["lampara"])
    h.luz_radial(x, y - a - 30 * s, alcance * s, col, k=1.0 * luz * f)
    N.humo(h, t, x + 1 * s, y - a - 50 * s, k=0.35, sem=sem + 11, viento=(4.0, -60.0), vida=2.8, hebras=1, ancho=0.8)
    return f


def estandarte(h, t, x, y, w=220, hh=420, sem=0, emblema="sol", viento=1.0, tono=120):
    """Estandarte colgado de un asta horizontal (x, y = esquina sup-izq): la tela ondea (más abajo, más), cola en dos puntas
    y un emblema propio (sol · torre · luna · llave); el color lo da la rampa «estandarte»."""
    n = 14
    def onda(u, v):
        return 16 * viento * v * math.sin(t * 2.4 + v * 4.2 + u * 1.3 + sem) + 6 * viento * v * math.sin(t * 4.1 + u * 3 + sem)
    izq = [(x + onda(0, v), y + hh * v) for v in np.linspace(0, 1, n)]
    der = [(x + w + onda(1, v), y + hh * v * 0.98) for v in np.linspace(0, 1, n)]
    pico = [(x + w * 0.75 + onda(0.75, 1.1), y + hh * 1.0), (x + w * 0.5 + onda(0.5, 1.0), y + hh * 0.86),
            (x + w * 0.25 + onda(0.25, 1.1), y + hh * 1.0)]
    P = np.array(izq[:1] + der + pico + izq[::-1][:-1])
    with h.con_rampa("estandarte"):
        h.pieza(P, tono, sem, w=4, d=18, trama=0.5, rim=0.6, luz=(0.4, -1))
        for k in range(1, 4):                                      # pliegues que se mueven con la tela
            u = k / 4
            Q = np.array([(x + w * u + onda(u, v) + 4 * math.sin(t * 2.4 + v * 4.2 + sem + k), y + hh * v)
                          for v in np.linspace(0.05, 0.85, 8)])
            h.trazo(Q, 3.0, sem + 10 + k, color=tuple(v * 255 for v in h.pal["tinta"]), alfa=0.35)
    cx, cy = x + w / 2 + onda(0.5, 0.42), y + hh * 0.42
    with h.con_rampa("oro"):
        if emblema == "sol":
            h.pieza(elipse_(cx, cy, w * 0.17, w * 0.17, n=28), 160, sem + 20, w=3, d=6, trama=0, rim=0.6)
            for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
                h.pieza([(cx + math.cos(a - 0.12) * w * 0.2, cy + math.sin(a - 0.12) * w * 0.2), (cx + math.cos(a) * w * 0.33,
                         cy + math.sin(a) * w * 0.33), (cx + math.cos(a + 0.12) * w * 0.2, cy + math.sin(a + 0.12) * w * 0.2)], 150,
                        sem + 21, w=2, d=0, sombra=0, trama=0, rim=0)
        elif emblema == "torre":
            b = w * 0.32
            h.pieza([(cx - b / 2, cy + b), (cx - b / 2, cy - b * 0.6), (cx - b * 0.7, cy - b * 0.6), (cx - b * 0.7, cy - b),
                     (cx - b * 0.25, cy - b), (cx - b * 0.25, cy - b * 0.8), (cx + b * 0.25, cy - b * 0.8), (cx + b * 0.25, cy - b),
                     (cx + b * 0.7, cy - b), (cx + b * 0.7, cy - b * 0.6), (cx + b / 2, cy - b * 0.6), (cx + b / 2, cy + b)], 160,
                    sem + 20, w=3, d=6, trama=0, rim=0.6)
        elif emblema == "luna":
            A = elipse_(cx, cy, w * 0.25, w * 0.25, n=30)
            h.pieza(A, 160, sem + 20, w=3, d=6, trama=0, rim=0.6)
            with h.con_rampa("estandarte"):
                h.pieza(elipse_(cx + w * 0.1, cy - w * 0.04, w * 0.21, w * 0.21, n=30), tono, sem + 21, w=0, d=0, sombra=0, rim=0)
        else:                                                             # llave
            h.pieza(elipse_(cx, cy - w * 0.18, w * 0.11, w * 0.11, n=20), 160, sem + 20, w=3, d=4, trama=0, rim=0.6)
            h.pieza([(cx - 6, cy - w * 0.08), (cx + 6, cy - w * 0.08), (cx + 6, cy + w * 0.3), (cx - 6, cy + w * 0.3)], 160,
                    sem + 21, w=3, d=0, sombra=0, trama=0)
            h.pieza([(cx + 6, cy + w * 0.18), (cx + 30, cy + w * 0.18), (cx + 30, cy + w * 0.27), (cx + 6, cy + w * 0.27)], 160,
                    sem + 22, w=2, d=0, sombra=0, trama=0)
    with h.con_rampa("hierro"):                                        # asta y remates
        h.pieza([(x - 30, y - 10), (x + w + 30, y - 10), (x + w + 30, y + 4), (x - 30, y + 4)], 60, sem + 30, w=3, d=4, trama=0,
                rim=0.8)
        for xx in (x - 34, x + w + 34):
            h.pieza(elipse_(xx, y - 3, 10, 10, n=12), 90, sem + 31, w=2, d=0, sombra=0, rim=0.8)


def lacre(h, t, t0, x, y, r=70.0, sem=0, emblema="sol"):
    """Sello de lacre: la gota roja cae (t0), se aplasta con el anillo de sello y queda el emblema en relieve. Devuelve
    True una vez sellado (para anclar el SFX)."""
    if t < t0 - 0.35:
        return False
    u = clamp01((t - t0 + 0.35) / 0.35)                # gota que se derrama
    p = clamp01((t - t0) / 0.12)                       # golpe del anillo
    rr = r * (0.55 + 0.45 * smooth(u)) * (1 + 0.12 * p)
    rng = np.random.default_rng(sem)
    P = np.array([(x + math.cos(a) * rr * (1 + 0.10 * rng.uniform(-1, 1)), y + math.sin(a) * rr * (1 + 0.10 * rng.uniform(-1, 1)))
                  for a in np.linspace(0, 2 * math.pi, 26, endpoint=False)])
    with h.con_rampa("lacre"):
        h.pieza(suave(P, 3), 120, sem, w=4, d=10, trama=0, rim=0.9, luz=(-0.4, -1))
        if p > 0:
            h.pieza(elipse_(x, y, rr * 0.66, rr * 0.66, n=36), 95, sem + 1, w=2.5, d=6, trama=0, rim=0.8, luz=(0.5, 1))
            s = rr * 0.45
            if emblema == "sol":
                for a in np.linspace(0, 2 * math.pi, 10, endpoint=False):
                    h.trazo(np.array([[x + math.cos(a) * s * 0.45, y + math.sin(a) * s * 0.45],
                                      [x + math.cos(a) * s, y + math.sin(a) * s]]), 3.2, sem + 3, color=(70, 8, 8), alfa=0.9)
                h.pieza(elipse_(x, y, s * 0.35, s * 0.35, n=18), 150, sem + 4, w=2, d=3, trama=0, rim=0.9, luz=(-0.4, -1))
            else:
                h.pieza(elipse_(x, y, s * 0.6, s * 0.6, n=18), 150, sem + 4, w=2, d=3, trama=0, rim=0.9, luz=(-0.4, -1))
    return p >= 1


# ================================================================ personajes
TONOS_PESQ = dict(abrigo=74, sombrero=40, cinta=12, piel=118, camisa=62, corbata=44, pantalon=34, zapato=20, mano=112)


class Pesquisidor(Detective):
    """El detective de la época: el mismo cuerpo y caminar del Detective noir (gambesón largo con cinturón) con CAPA de lana
    que ondea detrás, CAPUCHA (sombra sobre los ojos, como el ala de la fedora), barba corta y un FAROL de mano en vez del
    cigarro. p: lo de Detective + capa (0..1 ondeo extra), farol (bool), alzar (0..1 levanta el farol para mirar)."""

    def __init__(self, sem=0, tonos=None):
        t = dict(TONOS_PESQ)
        t.update(tonos or {})
        super().__init__(sem, t)

    def dibujar(self, h, p):
        p = dict(p)
        p["cigarro"] = False
        p["sostener"] = p.get("alzar", 0.0)
        T = self._T(p)
        s = p["s"]
        vien = p.get("viento", 0.0) + 0.06 * math.sin(h.t * 2.3 + self.sem) + 0.4 * p.get("capa", 0.0)
        bob = -5 * p.get("andar", 0.0) * abs(math.cos(p.get("paso", 0.0)))
        cx = -60 * vien
        sw = math.sin(h.t * 2.1 + self.sem) * 8
        capa = [(-58, -418 + bob), (40, -424 + bob), (66, -396 + bob), (40, -300), (34, -160), (14 + cx * 0.4, -86),
                (-40 + cx * 0.8 + sw * 0.5, -70), (-90 + cx + sw, -76), (-118 + cx * 1.2 + sw, -96), (-104 + cx * 0.7, -220),
                (-88 + cx * 0.3, -330), (-74, -392 + bob)]
        with h.con_rampa("lana"):
            h.pieza(T(suave(capa, 5)), 62, self.sem + 70, w=7 * s * 1.1, luz=p.get("luz", (0.25, -1)), d=30 * s, rim=p.get("rim", 0.9),
                    trama=0.7)
            for a in ((-60, -380), (-80, -250), (-95 + cx * 0.6, -110)), ((-30, -390), (-40, -260), (-50 + cx * 0.5, -90)):
                h.trazo(T(np.array(a, float)), 3.0 * s, self.sem + 71, color=(14, 14, 18), alfa=0.6)
        super().dibujar(h, p)
        if p.get("farol", True):
            self._farol(h, p, T, bob)

    def _farol(self, h, p, T, bob):
        s = p["s"]
        Hd = self._mano_pos(p, bob)
        sw = 0.10 * math.sin(h.t * 3.1 + self.sem) * (0.3 + p.get("andar", 0.0))
        a0 = Hd + np.array([16.0, 10.0])
        c, si = math.cos(sw), math.sin(sw)

        def R(P):
            P = np.asarray(P, float).reshape(-1, 2)
            return np.stack([a0[0] + P[:, 0] * c - P[:, 1] * si, a0[1] + P[:, 0] * si + P[:, 1] * c], 1)
        with h.con_rampa("hierro"):
            h.trazo(T(R([(0, 0), (0, 16)])), 3 * s, self.sem + 80, color=(20, 20, 24))
            h.pieza(T(R([(-16, 16), (16, 16), (12, 26), (-12, 26)])), 80, self.sem + 81, w=3 * s, d=4 * s, trama=0, rim=0.8)
            h.pieza(T(R([(-18, 70), (18, 70), (14, 80), (-14, 80)])), 70, self.sem + 82, w=3 * s, d=4 * s, trama=0, rim=0.8)
        P = T(R([(-12, 26), (12, 26), (14, 70), (-14, 70)]))
        h.emitir(P, 0.85, col=h.pal.get("vela", h.pal["lampara"]), blur=1.5)
        f = llama(h, h.t, *T(R([(0, 62)]))[0], s=0.28 * s, sem=self.sem + 83, k=1.0)
        for xx in (-12, 0, 12):
            h.trazo(T(R([(xx, 26), (xx * 1.15, 70)])), 2.4 * s, self.sem + 84, color=(16, 16, 20), alfa=0.9)
        q = T(R([(0, 48)]))[0]
        h.luz_radial(q[0], q[1], 420 * s, h.pal.get("vela", h.pal["lampara"]), k=0.85 * f)
        self._farol_pos = q

    def farol_pos(self):
        return getattr(self, "_farol_pos", None)

    def _cabeza(self, h, p, T, w, bob, pz, L):
        sem, s, k = self.sem, p["s"], self.k
        arriba = p.get("arriba", 0.0)
        ox, oy = 4.0, bob + p.get("cab_y", 0.0)
        ang = -0.22 * arriba + p.get("cab_rot", 0.0)

        def R(P):
            P = np.asarray(P, float).reshape(-1, 2)
            c0 = np.array([0.0, -440.0])
            c, si = math.cos(ang), math.sin(ang)
            Q = P - c0
            return np.stack([c0[0] + Q[:, 0] * c - Q[:, 1] * si + ox, c0[1] + Q[:, 0] * si + Q[:, 1] * c + oy], 1)
        cara = [(-28, -500), (-2, -526), (28, -514), (37, -494), (34, -485), (40, -480), (55, -463), (43, -457), (41, -452),
                (45, -447), (41, -443), (44, -439), (39, -435), (43, -426), (35, -415), (8, -419), (-10, -436), (-22, -458), (-30, -478)]
        pz(R(suave(cara, 4)), k["piel"], 42, w=w, d=26 * s, rim=p.get("rim", 0.9), trama=0.35)
        # barba corta y bigote
        barba = [(4, -446), (22, -448), (40, -446), (44, -436), (40, -422), (30, -410), (12, -408), (-4, -418), (-8, -436)]
        with h.con_rampa("lana"):
            pz(R(suave(barba, 3)), 40, 43, w=w * 0.6, d=8 * s, trama=0.5, rim=0.5)
        h.trazo(T(R([(30, -448), (44, -447)])), 4.0 * s, sem + 45, alfa=0.9)
        # capucha: cubre la nuca, la oreja y la frente; cae sobre los hombros
        cap = [(-56, -400 + bob), (-60, -470), (-48, -520), (-20, -548), (14, -552), (42, -536), (58, -508), (52, -500),
               (34, -512), (10, -520), (-12, -500), (-16, -470), (-6, -440), (14, -418), (40, -410), (60, -404 + bob),
               (30, -396 + bob), (-20, -398 + bob)]
        with h.con_rampa("lana"):
            pz(R(suave(cap, 4)), 70, 52, d=22 * s, trama=0.6)
            h.trazo(T(R([(-40, -500), (-30, -470), (-36, -430)])), 3.0 * s, sem + 53, color=(14, 14, 18), alfa=0.7)
        # sombra de la capucha sobre los ojos
        som = 1 - 0.8 * max(0.0, arriba)
        sb = [(-10, -518), (56, -508), (58, -486 + 10 * arriba), (36, -474 + 10 * arriba), (-8, -480)]
        h.pieza(T(R(sb)), 14, sem + 47, w=0, luz=L, d=1, sombra=0, trama=0, rim=0, alfa=0.85 * som, linea=False, jit=0.5)
        if arriba > 0.3 or p.get("brillo_ojo", 0.0) > 0:
            v = max(arriba, p.get("brillo_ojo", 0.0))
            h.disco(*T(R([[30, -489]]))[0], 2.6 * s, gris(int(40 + 200 * v)))

    # el Detective dibuja el brazo con cigarro; el pesquisidor no fuma
    def cigarro(self, p):
        bob = -5 * p.get("andar", 0.0) * abs(math.cos(p.get("paso", 0.0)))
        Hd = self._mano_pos(p, bob)
        return Hd, Hd


class BustoEncapuchado:
    """Primer plano del pesquisidor de perfil a la derecha (cabeza de ~420 px con s=1): capucha honda de lana, barba, ojo bajo
    la sombra de la capucha (se ve al levantar la barbilla), capa al hombro con broche, y VAHO del aliento en el frío.
    p: x, y (centro de la cara), s, d, luz, rim, arriba (0..1), boca (0..1), broche (bool)."""

    def __init__(self, sem=0):
        self.sem = sem

    def _T(self, p):
        x, y, s, d = p["x"], p["y"], p["s"], p.get("d", 1)

        def f(P):
            P = np.asarray(P, float).reshape(-1, 2)
            return np.stack([x + d * s * P[:, 0], y + s * P[:, 1]], 1)
        return f

    def boca(self, p):
        return self._T(p)(np.array([[150.0, 60.0]]))[0]

    def dibujar(self, h, p):
        T = self._T(p)
        s = p["s"]
        sem = self.sem
        L = p.get("luz", (0.8, -0.6))
        w = 9.0 * s
        dd = 40 * s
        rim = p.get("rim", 0.95)
        arriba = p.get("arriba", 0.0)
        boca = p.get("boca", 0.0)
        resp = 0.5 + 0.5 * math.sin(h.t * 1.3 + sem)                 # respiración: los hombros suben y bajan

        def pz(P, tono, sm, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", dd), **kw)
        dy = -6 * resp
        with h.con_rampa("lana"):                                     # capa sobre los hombros
            pz(suave([(-480, 640), (-330, 240 + dy), (-170, 190 + dy), (60, 196 + dy), (250, 250 + dy), (420, 420), (490, 640)], 5),
               66, 1, d=60 * s, trama=0.7)
            for a in (((-300, 320), (-280, 470), (-300, 640)), ((260, 330), (300, 470), (320, 640)), ((-80, 260), (-60, 450), (-90, 640))):
                h.trazo(T(np.array(a, float)), 3.5 * s, sem + 2, color=(14, 14, 18), alfa=0.6)
        with h.con_rampa("cuero"):                                    # jubón asomando y correa en bandolera
            pz([(-20, 220 + dy), (110, 224 + dy), (150, 640), (-60, 640)], 70, 3, w=w * 0.6, trama=0.4, rim=0.4)
            pz([(-120, 250 + dy), (-80, 236 + dy), (200, 640), (150, 640)], 40, 4, w=w * 0.5, trama=0, rim=0.6)
        if p.get("broche", True):
            with h.con_rampa("oro"):
                pz(elipse_(150, 250 + dy, 30, 30, n=20), 170, 5, w=w * 0.5, d=8 * s, trama=0, rim=0.9)
                pz(elipse_(150, 250 + dy, 14, 14, n=14), 210, 6, w=w * 0.3, d=0, sombra=0, rim=0)
        # cuello y cabeza de perfil
        pz([(-70, 60), (70, 120), (64, 240), (-84, 236)], 92, 9, d=30 * s, trama=0.6)
        cab = [(-150, -60), (-138, -130), (-60, -190), (40, -186), (96, -150), (124, -86), (116, -62), (130, -50), (186, 10),
               (142, 22), (138, 40), (152, 52 + 4 * boca), (136, 61 + 6 * boca), (147, 69 + 6 * boca), (130, 84), (144, 118),
               (112, 152), (30, 142), (-36, 102), (-74, 58), (-112, 36)]
        pz(suave(cab, 4), 120, 10, d=46 * s, trama=0.55)
        # barba poblada y bigote
        barba = [(-10, 40), (40, 70), (110, 74), (150, 80), (150, 120), (128, 160), (80, 196), (20, 190), (-30, 150), (-50, 90)]
        with h.con_rampa("lana"):
            pz(suave(barba, 4), 46, 11, w=w * 0.7, d=20 * s, trama=0.6, rim=0.6)
            pz(suave([(104, 50 + 4 * boca), (150, 50 + 4 * boca), (160, 66 + 5 * boca), (124, 64 + 5 * boca)], 3), 40, 12,
               w=w * 0.5, d=6 * s, trama=0, rim=0.5)
        r = np.random.default_rng(sem * 31 + h.dib)
        for _ in range(90):                                          # pelos de la barba que hierven con la tinta
            a = r.uniform(0, 1)
            q0 = np.array([-20 + a * 160, 80 + r.uniform(0, 100) * (1 - abs(a - 0.5))])
            h.trazo(T(np.array([q0, q0 + (r.uniform(-4, 4), r.uniform(8, 18))])), 1.6 * s, sem + 13, color=(20, 18, 18), alfa=0.6)
        h.trazo(T([(74, -20), (96, 10), (104, 36)]), 3.0 * s, sem + 13, alfa=0.55)
        h.trazo(T([(116, 62 + 5 * boca), (146, 64 + 6 * boca)]), 4.5 * s, sem + 15, alfa=0.95)
        # ojo y ceja
        oy = -70
        h.pieza(T(suave([(76, oy - 4), (96, oy - 10), (112, oy - 2), (96, oy + 6)], 3)), 230, sem + 18, w=w * 0.5, luz=L, d=2,
                sombra=0, trama=0, rim=0)
        h.disco(*T([[100, oy - 2]])[0], 5.5 * s, gris(12))
        h.disco(*T([[102, oy - 4]])[0], 1.8 * s, gris(250))
        h.trazo(T([(66, oy - 26), (98, oy - 32), (124, oy - 20)]), 7.0 * s, sem + 19, taper=(0.2, 0.6))
        h.trazo(T([(74, oy + 8), (100, oy + 12)]), 2.4 * s, sem + 20, alfa=0.6)
        # capucha honda: cubre nuca, oreja y frente; el borde delantero cae por delante del cuello
        cap = [(-260, 300), (-280, 40), (-250, -160), (-150, -300), (-10, -342), (110, -300), (176, -214), (196, -130),
               (170, -124), (136, -150), (80, -172), (10, -176), (-60, -150), (-104, -80), (-120, 10), (-110, 110), (-60, 200),
               (40, 236), (120, 250), (90, 300)]
        with h.con_rampa("lana"):
            pz(suave(cap, 4), 72, 21, d=46 * s, trama=0.65)
            pz(suave([(170, -124), (136, -150), (80, -172), (10, -176), (-60, -150), (-104, -80), (-112, -60), (-60, -130),
                      (10, -158), (80, -156), (140, -134)], 3), 30, 22, w=w * 0.4, d=0, sombra=0, rim=0)      # forro en sombra
            for a in (((-200, -200), (-230, -40), (-220, 160)), ((-90, -290), (-160, -150), (-180, 40))):
                h.trazo(T(np.array(a, float)), 4.0 * s, sem + 23, color=(14, 14, 18), alfa=0.6)
        # sombra de la capucha sobre los ojos (salvo que levante la barbilla)
        som = 1 - 0.85 * min(1.0, max(0.0, arriba))
        h.pieza(T(suave([(-110, -160), (176, -128), (190, -96 + 30 * arriba), (150, -62 + 30 * arriba), (90, -44 + 30 * arriba),
                         (20, -50), (-60, -70), (-110, -90)], 4)),
                12, sem + 24, w=0, luz=L, d=1, sombra=0, trama=0, rim=0, alfa=0.72 * som, linea=False, jit=0.5)
        if som > 0.3:
            h.disco(*T([[102, oy - 4]])[0], 2.6 * s, gris(int(170 * som)))


def vaho(h, t, x, y, ciclo=4.2, fase=0.0, k=1.0, sem=0, s=1.0):
    """Aliento visible en el frío: una bocanada cada `ciclo` s que sale de (x, y) y se deshace (capa aditiva)."""
    u = ((t + fase) % ciclo) / ciclo
    if u > 0.55:
        return
    v = u / 0.55
    N.humo(h, t, x, y, k=k * 0.9 * math.sin(math.pi * v) ** 0.7, sem=sem, viento=(80.0 * s, -18.0 * s), vida=1.6, hebras=5,
           ancho=2.2 * s, t_ini=t - u * ciclo)
