# -*- coding: utf-8 -*-
"""Amaya Vibes · Las MEJORES y las PEORES cosas que pedir en Navidad — SCRAPBOOK COQUETTE fusionado con el estilo de Amaya
(kit nucleo/coquette.py + stickers de Flow + SU AVATAR de presentadora, recortado de su propio video ref4).
Un solo plano secuencia: `cuadro(t)` dibuja el cuadro entero en función del tiempo global; cada escena del timeline tiene su
función (gancho, bienvenida…) o usa la plantilla `item()` (MEJOR/PEOR + número en letras recortadas pastel, sticker grande,
cinta con el nombre, etiqueta $, sello, notitas ancladas a palabras, stickers de Amaya de adorno, el avatar que se asoma y
reacciona al sello). Entre escenas: papel `rasgado`, o barras de `tv` al pasar a un PEOR. Los sonidos se anotan en EV
(t, nombre, vol, pan) con las MISMAS anclas: sonidos_navidad.py los sintetiza."""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw

import coquette as C
from coquette import H, W, clamp, e_back, e_out, pegar, pr, rebote, suave
from comun import AQUI, ESC, FIN, INI, NFRASES, ORDEN, T0, T1, stk, ww
from escena_base import Escena
from guion import LISTA

EV = []          # (t, nombre, vol, pan) → sonidos_navidad.py


def ev(t, nombre, vol=0.6, pan=0.0):
    EV.append((round(float(t), 3), nombre, vol, pan))


# ------------------------------------------------------------ utilidades de animación
def bump(t, a, b):
    """0 → 1 → 0 entre a y b (seno)."""
    u = pr(t, a, b)
    return math.sin(math.pi * u) if 0 < u < 1 else 0.0


def amort(t, t0, f=7.0, k=3.0):
    """Oscilación amortiguada que arranca en t0 (gelatina)."""
    if t < t0:
        return 0.0
    d = t - t0
    return math.exp(-k * d) * math.sin(d * f * math.pi)


def S(im, nombre, alto, x, y, t, t0, rot=0.0, sale=None, modo="cae", bob=1.0, alfa=1.0, gris=0.0, sx=1.0, sy=1.0, sem=0,
      esc=1.0, sale_a=None, tinte=None):
    """Sticker de Flow: entra en t0 (cae con rebote / pop), respira suave y sale en `sale` (encoge, o vuela a `sale_a`)."""
    if t < t0:
        return im
    u = pr(t, t0, t0 + 0.55)
    s = esc
    if modo == "cae":
        y = y - (1 - e_back(u, 1.5)) * 720
        rot = rot + (1 - e_out(u)) * (18 if sem % 2 else -18)
        a = alfa * clamp(u * 4)
    else:
        s *= rebote(t, t0, 0.45)
        a = alfa
    rot += math.sin(t * 1.4 + sem) * 2.0 * bob
    y += math.sin(t * 1.9 + sem * 0.7) * 6 * bob
    if sale is not None and t > sale:
        v = pr(t, sale, sale + 0.38)
        if sale_a is not None:
            x, y = x + (sale_a[0] - x) * e_out(v) ** 2, y + (sale_a[1] - y) * e_out(v) ** 2
            rot += v * 260
        else:
            s *= 1 - suave(v)
        if v >= 1:
            return im
    return pegar(im, stk(nombre, alto), x, y, esc=s, rot=rot, alfa=a, gris=gris, sx=sx, sy=sy, sombra=0.3, tinte=tinte)


def R(im, txt, cx, cy, px, t, t0, sale=None, sem=0, rot=0.0, cada=0.05, esc=1.0):
    return C.rotulo_recorte(im, txt, cx, cy, px, t, t0, cada=cada, sem=sem, rot=rot, salida=sale, esc=esc)


def N(im, txt, x, y, t, t0, t1=None, sem=0, rosa=False, rot=None, px=54):
    papel = (255, 214, 228) if rosa else (255, 248, 200)
    return C.pega_nota(im, txt, x, y, t, t0, t1, rot=rot, sem=sem, papel=papel, px=px)


@lru_cache(maxsize=4)
def tarjeta(w=520, h=560):
    """Tarjeta blanca tipo polaroid con cinta arriba."""
    im = Image.new("RGBA", (w, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 30, w, h + 30), radius=18, fill=(255, 253, 250, 255))
    d.rounded_rectangle((10, 40, w - 10, h + 20), radius=12, outline=(240, 200, 214, 255), width=4)
    d.polygon([(w / 2 - 80, 8), (w / 2 + 80, 0), (w / 2 + 88, 52), (w / 2 - 72, 60)], fill=(248, 207, 220, 215))
    return C.a_rgba(im)


@lru_cache(maxsize=8)
def liston(txt="HAPPY WATCHING!!", px=46):
    """Listón rosa con las puntas en cola de golondrina y estrellitas (el «HAPPY WATCHING!!» de Amaya)."""
    f = C.fuente("Poppins-ExtraBold.ttf", px)
    bb = f.getbbox(txt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w, h = tw + 220, int(th + px * 1.1)
    im = Image.new("RGBA", (w, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    oscuro, claro = (205, 92, 136, 255), (240, 138, 176, 255)
    d.polygon([(0, 20), (90, 20), (90, h + 20), (0, h + 20), (40, h / 2 + 20)], fill=oscuro)
    d.polygon([(w - 90, 20), (w, 20), (w - 40, h / 2 + 20), (w, h + 20), (w - 90, h + 20)], fill=oscuro)
    d.polygon([(60, 0), (w - 60, 0), (w - 60, h), (60, h)], fill=claro)
    d.line([(64, 6), (w - 64, 6)], fill=(255, 255, 255, 200), width=2)
    d.line([(64, h - 6), (w - 64, h - 6)], fill=(255, 255, 255, 200), width=2)
    d.text(((w - tw) / 2 - bb[0], (h - th) / 2 - bb[1]), txt, font=f, fill=(255, 255, 255, 255))
    for sx in (100, w - 100):
        cx, cy, r = sx, h / 2, px * 0.3
        d.polygon([(cx, cy - r), (cx + r * 0.3, cy - r * 0.3), (cx + r, cy), (cx + r * 0.3, cy + r * 0.3), (cx, cy + r),
                   (cx - r * 0.3, cy + r * 0.3), (cx - r, cy), (cx - r * 0.3, cy - r * 0.3)], fill=(255, 255, 255, 255))
    return C.a_rgba(im)


def corazones(im, t, t0, t1, cx, cy, n=6, sem=0, r=0.55):
    if t < t0 or t > t1 + 1.6:
        return im
    rg = np.random.default_rng(sem)
    for i in range(n):
        ti = t0 + i * (t1 - t0) / max(1, n)
        if t < ti:
            continue
        v = pr(t, ti, ti + 1.6)
        x = cx + rg.uniform(-170, 170) + math.sin(t * 3 + i) * 18
        y = cy - v * 330
        pegar(im, C.corazon(40, C.ROSA_FUERTE if i % 2 else C.ROSA), x, y, esc=r * rebote(t, ti, 0.3), rot=rg.uniform(-20, 20),
              alfa=1 - pr(v, 0.6, 1.0), sombra=0.15)
    return im


def sacudir(im, dx, dy):
    if abs(dx) < 0.5 and abs(dy) < 0.5:
        return im
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(im, M, (W, H), borderMode=cv2.BORDER_REFLECT)


def palabra_tras(esc, frase, palabra, k=1):
    """Inicio de la k-ésima palabra que sigue a `palabra` en la frase."""
    ws = ESC[esc]["frases"][frase]["words"]
    t = ww(esc, frase, palabra)
    i = next(j for j, x in enumerate(ws) if abs(x["s"] - t) < 1e-6)
    return ws[min(len(ws) - 1, i + k)]["s"]


def A_(esc, f, pal):
    """Ancla «palabra» o «palabra#n» (n-ésima aparición) de la frase f."""
    if "#" in pal:
        p, n = pal.split("#")
        return ww(esc, f, p, int(n))
    return ww(esc, f, pal)


def _fin(esc, fin, t0):
    """Fin de una pieza: None (hasta que acaba la escena), (frase, palabra) o segundos después de t0."""
    if fin is None:
        return None
    if isinstance(fin, tuple):
        return A_(esc, *fin) - 0.05
    return t0 + fin


# ------------------------------------------------------------ AVATAR de Amaya (presentadora)
AV_ABRE = os.path.join(AQUI, "propios", "amaya_avatar.png")
AV_CIERRA = os.path.join(AQUI, "propios", "amaya_avatar_cierra.png")
AZUL_POP = (0.42, 0.66, 0.96)


def lineas_pop(im, x, y, t, t0, esc=1.0, lado=-1):
    """Tres rayitas azules de «¡pop!» junto a la cabeza (como en su intro)."""
    k = bump(t, t0, t0 + 0.7)
    if k <= 0:
        return im
    for ang in ((-150, -125, -100) if lado < 0 else (-30, -55, -80)):
        a = math.radians(ang)
        r0, r1 = 40 * esc, (40 + 70 * k) * esc
        p0 = (int(x + math.cos(a) * r0), int(y + math.sin(a) * r0))
        p1 = (int(x + math.cos(a) * r1), int(y + math.sin(a) * r1))
        cv2.line(im, p0, p1, AZUL_POP, max(3, int(10 * esc)), cv2.LINE_AA)
    return im


def avatar(im, t, x, alto, t0, sale=None, si=(), no=(), sem=0, esc=1.0, y=H + 6, lado=-1):
    """Busto de Amaya que sube desde el borde de abajo con rebote; respira, parpadea, salta de gusto (`si`) o niega (`no`)."""
    if t < t0:
        return im
    u = pr(t, t0, t0 + 0.55)
    s = esc * (0.6 + 0.4 * e_back(u, 2.0))
    dy = (1 - e_out(u)) * alto * 0.7
    rot = math.sin(t * 1.1 + sem) * 1.8
    dy += math.sin(t * 1.7 + sem) * 4
    for tr in si:
        dy -= 46 * bump(t, tr, tr + 0.45)
        rot += 4 * bump(t, tr, tr + 0.45)
    for tn in no:
        rot += 6 * math.sin((t - tn) * 15) * bump(t, tn, tn + 1.1)
    if sale is not None:
        v = suave(pr(t, sale, sale + 0.45))
        dy += v * alto * 1.05
        if v >= 1:
            return im
    parpa = ((t + sem * 0.61) % 3.4) < 0.13 and t > t0 + 0.6
    tex = C.sticker(AV_CIERRA if parpa else AV_ABRE, alto)
    pegar(im, tex, x, y + dy, esc=s, rot=rot, ancla=(0.5, 1.0), sombra=0.3)
    cab = (x + lado * 0.36 * alto * s, y + dy - 0.86 * alto * s)
    lineas_pop(im, cab[0], cab[1], t, t0 + 0.15, esc=s * alto / 600, lado=lado)
    for tr in tuple(si) + tuple(no):
        lineas_pop(im, cab[0], cab[1], t, tr, esc=s * alto / 600, lado=lado)
    return im


# ============================================================ GANCHO
class G:
    hola = ww("gancho", 0, "hola")
    soy = ww("gancho", 0, "soy")
    amaya = ww("gancho", 0, "amaya")
    ya = ww("gancho", 0, "ya")
    navidad = ww("gancho", 0, "navidad")
    calcet = ww("gancho", 0, "calcetines")
    quedate = ww("gancho", 0, "quedate")
    quince = ww("gancho", 1, "quince")
    mejores = ww("gancho", 1, "mejores")
    diez = ww("gancho", 1, "diez")
    peores = ww("gancho", 1, "peores")
    ocurra = ww("gancho", 1, "ni se te")
    carta = ww("gancho", 1, "carta")
    ojo = ww("gancho", 2, "ojo")
    peores2 = ww("gancho", 2, "peores")
    seguro = ww("gancho", 2, "seguro")
    cajon = ww("gancho", 2, "cajon")


ev(0.15, "pop", 0.6, 0.3)
ev(G.hola, "megafono", 0.45, 0.3)
ev(G.soy, "pop_avatar", 0.6, -0.5)
ev(G.amaya, "letras", 0.45, 0.4)
for k, tt in enumerate((G.navidad - 0.2, G.navidad + 0.1, G.navidad + 0.35)):
    ev(tt + 0.3, "cae", 0.5, (-0.5, 0.5, -0.1)[k])
ev(G.navidad, "destello", 0.4)
ev(G.calcet - 0.2 + 0.3, "cae", 0.6)
ev(G.calcet + 0.4, "pop_avatar", 0.45, -0.6)
ev(G.calcet + 0.5, "boing_triste", 0.5)
ev(G.quince, "letras", 0.4, -0.4)
ev(G.diez, "letras", 0.4, 0.4)
ev(G.ocurra, "sello", 0.8, 0.4)
ev(G.carta - 0.15 + 0.3, "cae", 0.6)
ev(G.carta, "destello", 0.4)
ev(G.ojo + 0.05, "whoosh", 0.35)
ev(G.seguro + 0.3, "cae", 0.55, 0.3)
ev(G.cajon, "cinta", 0.5, 0.3)
ev(G.cajon + 0.5, "misterio", 0.4)


def gancho(t):
    im = C.fondo("vichy_amaya", t)
    C.esquinas(im, t, t0=0.05, sem=1)
    # 1 · ¡Hola, hola! Soy Amaya — con el megáfono y su avatar
    if t < G.ya + 0.6:
        vib = math.sin(t * 46) * 3.5 * bump(t, G.hola, G.hola + 1.0)
        S(im, "megafono", 330, 700, 330, t, 0.12, rot=-14 + vib, modo="pop", sale=G.ya, sem=1)
        R(im, "¡Hola,", 1250, 280, 140, t, G.hola, sale=G.ya, sem=3)
        R(im, "hola!", 1340, 450, 140, t, G.hola + 0.2, sale=G.ya + 0.05, sem=4)
        R(im, "Soy", 930, 700, 100, t, G.soy, sale=G.ya + 0.1, sem=5)
        R(im, "Amaya", 1470, 710, 170, t, G.amaya, sale=G.ya + 0.15, sem=6, cada=0.06)
        S(im, "mono", 150, 1760, 560, t, G.amaya + 0.35, modo="pop", rot=12, sale=G.ya + 0.2, sem=7)
        S(im, "estrella", 100, 860, 560, t, G.amaya + 0.5, modo="pop", sale=G.ya + 0.2, sem=8)
    avatar(im, t, 330, 640, G.soy - 0.05, sale=G.ya + 0.1, si=(G.amaya,), sem=1)
    # 2 · ya casi es Navidad
    if G.ya - 0.2 < t < G.calcet + 0.3:
        s2 = G.calcet - 0.35
        R(im, "¡Navidad!", 960, 175, 130, t, G.navidad, sale=s2, sem=7)
        S(im, "arbolito", 600, 470, 600, t, G.navidad - 0.2, sale=s2, sem=2)
        S(im, "regalo", 440, 1450, 650, t, G.navidad + 0.1, sale=s2, sem=3)
        S(im, "baston", 290, 840, 790, t, G.navidad + 0.35, rot=14, sale=s2, sem=4)
        S(im, "esfera", 230, 1110, 400, t, G.navidad + 0.55, modo="pop", sale=s2, sem=5)
        if t > G.navidad:
            C.destellos(im, t, [(300, 330), (690, 440), (1300, 400), (1660, 860)], 1.0)
    # 3 · ¡otra vez calcetines! (Amaya niega con la cabeza)
    if G.calcet - 0.3 < t < INI("gancho", 1):
        sale = INI("gancho", 1) - 0.35
        tiem = math.sin(t * 38) * 4 * bump(t, G.calcet + 0.5, G.calcet + 1.4)
        S(im, "calcetines", 540, 1080, 560, t, G.calcet - 0.2, rot=-6 + tiem, sale=sale, sem=6, gris=0.15)
        N(im, "¡OTRA VEZ NO!", 1560, 290, t, G.calcet + 0.5, sale, sem=8, rosa=True, rot=8, px=60)
        N(im, "quédate...", 1580, 820, t, G.quedate, sale, sem=9, rot=-6)
    avatar(im, t, 300, 520, G.calcet + 0.3, sale=INI("gancho", 1) - 0.4, no=(G.calcet + 0.6,), sem=2)
    # 4 · 15 mejores y 10 peores
    if INI("gancho", 1) - 0.4 < t < G.carta + 0.3:
        s4 = G.carta - 0.3
        R(im, "15", 500, 190, 150, t, G.quince, sale=s4, sem=11)
        R(im, "MEJORES", 500, 345, 100, t, G.mejores, sale=s4, sem=13, cada=0.04)
        for k, (n, al, x, y) in enumerate((("camara", 330, 280, 650), ("audifonos", 320, 520, 700), ("bodymist", 330, 740, 670))):
            S(im, n, al, x, y, t, G.mejores + 0.12 * k, modo="pop", sale=s4, sem=20 + k)
        R(im, "10", 1430, 190, 150, t, G.diez, sale=s4, sem=12)
        R(im, "PEORES", 1430, 345, 100, t, G.peores, sale=s4, sem=14, cada=0.04)
        for k, (n, al, x, y) in enumerate((("calcetines", 270, 1200, 690), ("canasta", 330, 1440, 660), ("paleta", 250, 1670, 710))):
            S(im, n, al, x, y, t, G.peores + 0.12 * k, modo="pop", sale=s4, sem=30 + k, gris=0.35)
        if t < s4:
            C.golpe_sello(im, "no", 1440, 700, t, G.ocurra, rot=-14, esc=0.8)
    # 5 · la carta y el cajón secreto
    if t > G.carta - 0.4:
        u = suave(pr(t, G.ojo, G.ojo + 0.5))
        cx, esc_ = 960 - 440 * u, 1.0 - 0.22 * u
        S(im, "carta", 560, cx, 560, t, G.carta - 0.15, esc=esc_, sem=40)
        if t < G.ojo + 0.5:
            C.destellos(im, t, [(680, 330), (1250, 380), (1230, 800)], 1.0)
        S(im, "cajon", 470, 1340, 610, t, G.seguro, sem=41)
        if t > G.cajon:
            pegar(im, C.cinta("SECRETO", 64, C.ROSA_FUERTE, (1, 1, 1), 3), 1340, 620, esc=rebote(t, G.cajon, 0.35), rot=-16,
                  sombra=0.2)
        N(im, "¿cuál será?", 1590, 290, t, G.peores2, sem=42, rosa=True, rot=7)
    if INI("gancho", 1) < t < G.carta:
        im = sacudir(im, *C.temblor(t, G.ocurra))
    return im


# ============================================================ BIENVENIDA
class B:
    hola = ww("bienvenida", 0, "bienvenida")
    amaya = ww("bienvenida", 0, "amaya")
    vibes = ww("bienvenida", 0, "vibes")
    asi = ww("bienvenida", 0, "asi")
    sello = ww("bienvenida", 0, "sello")
    rojo = ww("bienvenida", 0, "rojo")
    sale_r = ww("bienvenida", 0, "sale", 1)
    pesos = ww("bienvenida", 1, "pesos")
    uno = ww("bienvenida", 1, "uno")
    barato = ww("bienvenida", 1, "barato")
    tres = ww("bienvenida", 1, "tres")
    carino = ww("bienvenida", 1, "mucho")


B_TIT_SALE = B.sello - 1.05
ev(B.hola, "pop_avatar", 0.55, -0.5)
ev(B.amaya, "letras", 0.5, 0.3)
ev(B.vibes + 0.4, "whoosh", 0.35, 0.6)
for k in range(5):
    ev(B.hola + 0.25 + 0.2 * k, "pop", 0.3, -0.6 + 0.3 * k)
ev(B_TIT_SALE + 0.2, "whoosh", 0.3, -0.4)
ev(B.sello, "sello", 0.8, -0.2)
ev(B.sello + 0.15, "pop_avatar", 0.35, -0.6)
ev(B.sale_r - 0.3, "whoosh", 0.3, 0.4)
ev(B.rojo, "sello", 0.8, 0.4)
for k in range(3):
    ev(B.pesos + 0.24 * k, "etiqueta", 0.5, -0.5 + 0.5 * k)
ev(B.uno, "ding", 0.4, -0.5)
ev(B.tres, "ding", 0.45, 0.5)
ev(B.carino + 0.1, "corazones", 0.4, 0.5)


def bienvenida(t):
    im = C.fondo("vichy_amaya", t + 40)
    C.esquinas(im, t, t0=-10, sem=1)
    # stickers de Amaya (los de las esquinas se quedan; los del centro se van con el logo)
    for k, (n, al, x, y, r, queda) in enumerate((("mora", 150, 560, 170, -8, True), ("latte", 170, 1770, 190, 6, True),
                                                 ("hortensia", 130, 1850, 470, 10, True), ("perrito_negro", 180, 1720, 930, -4, True),
                                                 ("bola_disco", 150, 720, 560, 0, False), ("bebida", 200, 1690, 700, 6, False),
                                                 ("labios", 120, 900, 920, -10, False), ("estrella", 90, 1060, 830, 0, False))):
        S(im, n, al, x, y, t, B.hola + 0.25 + 0.2 * (k % 5), modo="pop", rot=r, sem=50 + k,
          sale=None if queda else B_TIT_SALE + 0.05 * k)
    # «¡Bienvenida a / Amaya / Vibes» + listón
    R(im, "¡Bienvenida a", 1180, 150, 84, t, B.hola, sale=B_TIT_SALE, sem=60, cada=0.035)
    R(im, "Amaya", 1180, 330, 170, t, B.amaya, sale=B_TIT_SALE + 0.05, sem=61, cada=0.06)
    R(im, "Vibes", 1180, 520, 170, t, B.vibes, sale=B_TIT_SALE + 0.1, sem=62, cada=0.06)
    if B.vibes + 0.4 < t < B_TIT_SALE + 0.5:
        u = e_out(pr(t, B.vibes + 0.4, B.vibes + 0.85))
        v = suave(pr(t, B_TIT_SALE, B_TIT_SALE + 0.4))
        pegar(im, liston(), 1240 + (1 - u) * 1100 + v * 1100, 690, rot=-3, sombra=0.22)
    # Amaya: grande al saludar, luego se hace a un lado y reacciona a los sellos
    k_av = suave(pr(t, B_TIT_SALE, B_TIT_SALE + 0.5))
    avatar(im, t, 330 - 90 * k_av, 660, B.hola - 0.1, si=(B.sello + 0.1, B.tres), no=(B.rojo + 0.1,), sem=3,
           esc=1.0 - 0.22 * k_av)
    # el sello verde y el rojo, cada uno en su tarjeta
    car_sale = INI("bienvenida", 1) - 0.1
    for k, (t0, x, rot, nombre, tipo, ts, gris) in enumerate(
            ((B_TIT_SALE + 0.2, 860, -4, "regalo", "si", B.sello, 0.0), (B.sale_r - 0.3, 1450, 4, "calcetines", "no", B.rojo, 0.3))):
        if t < t0:
            continue
        u = e_back(pr(t, t0, t0 + 0.5), 1.3)
        v = suave(pr(t, car_sale, car_sale + 0.45))
        xx = x + (1 - u) * (-1100 if k == 0 else 900) + v * (-1500 if k == 0 else 1300)
        pegar(im, tarjeta(), xx, 560, rot=rot, sombra=0.3)
        S(im, nombre, 330, xx, 500, t, t0 + 0.25, rot=rot, modo="pop", sem=70 + k, gris=gris)
        if t > ts:
            pegar(im, C.sello(tipo), xx, 700, esc=0.62 * (2.3 - 1.3 * e_out(pr(t, ts, ts + 0.16))), rot=-12 + rot,
                  alfa=0.93 * clamp(pr(t, ts, ts + 0.16) * 2.5), sombra=0)
    # los signos de pesos
    if t > B.pesos - 0.1:
        for k in range(3):
            x = 560 + k * 450
            tk = (B.uno, None, B.tres)[k]
            pul = 1 + (0.22 * bump(t, tk - 0.05, tk + 0.55) if tk else 0)
            C.cuelga_etiqueta(im, k + 1, x, 470, t, B.pesos + 0.24 * k, esc=1.15 * pul)
        N(im, "barato", 720, 760, t, B.barato, sem=80, rot=-5, px=58)
        N(im, "con mucho cariño", 1600, 760, t, B.carino - 0.2, sem=81, rosa=True, rot=5, px=54)
        corazones(im, t, B.carino, B.carino + 1.4, 1600, 560, n=6, sem=82)
    im = sacudir(im, *[a + b for a, b in zip(C.temblor(t, B.sello), C.temblor(t, B.rojo))])
    return im


# ============================================================ PLANTILLA DE ÍTEM
# id → (sticker principal, alto, x, y). Los secundarios los dibuja el gancho MOD del ítem.
LAY = {
    "m15": ("squishy", 520, 1180, 540), "m14": ("pinzas_b", 470, 1060, 500), "p10": ("diario", 580, 1180, 530),
    "m13": ("cuentas", 520, 1180, 540), "m12": ("bloqueador", 560, 1080, 530), "p9": ("tinte", 480, 1150, 520),
    "m11": ("bodymist", 600, 1180, 530), "m10": ("cepillo", 580, 1150, 520), "p8": ("foto_maquillaje", 540, 1180, 520),
    "m9": ("pantuflas", 440, 1180, 560), "p7": ("sudadera", 560, 1180, 540), "m8": ("kit", 440, 1150, 520),
    "m7": ("bolsa", 520, 1180, 540), "p6": ("bebe", 580, 1180, 530), "m6": ("balsamo_solo", 600, 1180, 530),
    "p5": ("canasta", 600, 1180, 520), "m5": ("termo", 620, 1180, 520), "p4": ("foto_pirata", 500, 1180, 520),
    "m4": ("oso", 600, 1180, 520), "p3": ("perrito", 580, 1180, 530), "m3": ("controles", 520, 1180, 540),
    "p2": ("serum_solo", 560, 1100, 530), "m2": ("audifonos", 600, 1180, 520), "p1": ("calcetines", 560, 1180, 540),
    "m1": ("camara", 600, 1180, 520),
}
# notitas: id → [(frase, palabra, texto, x, y, rosa)]   (se van a los ~3,2 s o cuando llega otra al mismo hueco)
NOTAS = {
    "m15": [(0, "antiestres", "¡ANTIESTRÉS!", 430, 520, True), (0, "needoh", "tipo NeeDoh", 1660, 480, False),
            (1, "tarea", "tarea + estrés\n= squishy", 430, 520, False), (2, "mochila", "¡cabe en la\nmochila!", 1660, 700, True)],
    "m14": [(1, "carey", "carey =\nestampado de tortuga", 430, 520, False), (1, "tres segundos", "¡3 seg!", 1660, 470, True),
            (1, "ligas", "adiós, ligas", 430, 520, True),
            (2, "escuela", "1 · escuela", 1730, 440, False), (2, "casa", "2 · casa", 1730, 570, False),
            (2, "perder", "3 · ¿dónde quedó?", 1700, 700, True)],
    "p10": [(1, "tierno", "aww...", 1660, 440, True), (1, "descubres", "¿¿qué??", 430, 520, False),
            (1, "nada", "...o con nada", 1660, 700, False), (2, "nadie", "escóndela ;)", 430, 520, True)],
    "m13": [(1, "ti", "una para ti", 430, 520, False), (1, "mejor amiga", "+ tu mejor amiga", 430, 520, True),
            (1, "salon", "¡TODO el salón!", 430, 520, False), (2, "creativo", "creativo", 430, 520, True),
            (2, "vacaciones", "para vacaciones", 430, 520, False)],
    "m11": [(1, "perfume", "como perfume,\npero ligerito", 430, 520, False), (1, "vainilla", "vainilla", 1660, 420, False),
            (2, "precios", "$  ·  $$  ·  $$$", 430, 520, True), (2, "tocador", "tu tocador", 1680, 330, True)],
    "m12": [(0, "color", "con color\no normal", 430, 520, False), (0, "cuerpo", "cuerpo + cara", 430, 520, True),
            (1, "uso", "¡lo que más uso!", 430, 520, True), (1, "invierno", "¡hasta en invierno!", 430, 520, False),
            (1, "suavecita", "piel suavecita", 1680, 780, True), (2, "naturales", "se ven naturales", 430, 520, False),
            (2, "huelen", "¡huelen riquísimo!", 430, 520, True)],
    "p9": [(0, "danan", "dañan el cabello", 430, 520, False), (1, "rosa", "rosa o azul...", 430, 520, True),
           (1, "reseca", "- lo reseca", 1700, 380, False), (1, "quiebra", "- lo quiebra", 1700, 540, False),
           (1, "irritar", "- irrita la piel", 1700, 700, True), (2, "lavarlo", "se quita\nal lavarlo", 430, 520, True)],
    "m10": [(1, "desenreda", "desenreda\nsin jalar", 430, 520, False), (1, "brillosito", "¡brillosito!", 430, 520, True),
            (2, "agradecer", "tu pelo: ¡gracias!", 430, 520, False), (2, "mitad", "la mitad del tiempo", 430, 520, True)],
    "m8": [(0, "escuela", "para la escuela", 430, 520, False), (1, "bolsita", "una bolsita con...", 430, 520, True),
           (2, "salva", "¡te salva!", 430, 520, True), (2, "amigas", "tus amigas:\n«¿me prestas?»", 1660, 420, False)],
    "p8": [(1, "dano", "¡hasta te puede\nhacer daño!", 430, 520, True), (1, "pintan", "casi no pintan", 430, 520, False), (1, "rompen", "¡se rompen!", 1660, 420, True, (2, "tres")),
           (1, "comezon", "¡y dan comezón!", 1660, 700, False, (2, "tres")), (2, "menos", "menos, pero bonito", 430, 520, True)],
    "m9": [(1, "frio", "diciembre = brrr", 430, 520, False), (1, "nube", "¡una nube!", 1660, 380, True),
           (2, "pijama", "+ pijama", 430, 520, True)],
    "p7": [(1, "abres", "abres la caja y...", 430, 520, False), (1, "campana", "¡casa de campaña!", 430, 520, True),
           (1, "chiquita", "¿de muñeca?", 430, 520, False), (2, "talla", "¿qué talla eres?", 430, 520, True),
           (2, "contigo", "¡vamos juntas!", 1660, 420, False), (2, "gusto", "ropa de TU gusto", 1660, 580, True)],
    "m7": [(1, "llaveritos", "charms =\nllaveritos", 430, 520, False), (1, "mochila", "en la bolsa\no la mochila", 430, 520, True),
           (2, "historia", "cada uno,\nsu historia", 430, 520, True)],
    "p6": [(1, "tia", "tu tía...", 430, 520, False), (1, "primero", "1.º de primaria", 1660, 400, True),
           (1, "llora", "¡BUAAA!", 430, 520, True), (2, "culpa", "no es su culpa", 430, 520, False),
           (2, "lista", "¡mándale tu lista!", 430, 520, True)],
    "m6": [(1, "hidrata", "hidrata", 430, 520, False), (1, "brillosito", "brillosito", 430, 520, True),
           (1, "natural", "natural", 430, 520, False), (2, "dias", "todos los días", 430, 520, True)],
    "p5": [(1, "abuelita", "huele a abuelita", 430, 520, True), (1, "plastico", "plástico x1000", 430, 520, False),
           (2, "supe", "«no supe\nqué darte»", 430, 520, True), (2, "higiene", "los que TÚ escoges:\n¡sí valen!", 430, 520, False)],
    "m5": [(1, "popote", "con popote", 430, 520, False), (1, "derraman", "¡no se derrama!", 1660, 400, True, (2, "todas")),
           (1, "agua", "¡a tomar agua!", 430, 520, True), (2, "nadie", "¡es MÍO!", 430, 520, True)],
    "p4": [(0, "tianguis", "del tianguis", 430, 520, False), (1, "originales", "¿originales?", 430, 520, True),
           (1, "dos", "dura 2 semanas", 430, 520, False), (2, "marca", "una marca que exista", 430, 520, True),
           (2, "barato", "barato no siempre\nes barato", 1640, 760, False)],
    "m4": [(1, "chiquitas", "ya no somos\nniñas chiquitas", 430, 520, True), (1, "cama", "en tu cama", 1660, 420, False),
           (1, "moda", "nunca pasa\nde moda", 430, 520, False), (2, "carita", "¡con carita!", 430, 520, True)],
    "p3": [(1, "juguete", "no es un juguete", 430, 520, True), (1, "come", "- come", 1700, 380, False),
           (1, "enferma", "- se enferma", 1700, 540, False), (1, "vive", "- vive 10-15 años", 1690, 700, True),
           (2, "familia", "platícalo en familia", 430, 520, False), (2, "sorpresa", "sorpresa: NO", 430, 520, True)],
    "m3": [(1, "consola", "si hay consola...", 430, 520, False), (1, "mario", "tipo Mario Kart", 430, 520, True),
           (1, "pierda", "papá:\n¡último lugar!", 1660, 400, True), (2, "mesa", "¡también cuenta!", 430, 520, False),
           (2, "gente", "con tu gente", 430, 520, True)],
    "p2": [(1, "internet", "de moda en internet", 430, 520, False), (1, "dermatologos", "los dermatólogos:", 1660, 380, False),
           (1, "necesita", "¡no las necesita!", 1660, 380, True), (1, "irritar", "se puede irritar", 430, 520, True),
           (2, "tres", "solo 3 cosas:", 430, 520, False), (2, "facil", "¡así de fácil!", 430, 520, True)],
    "m2": [(1, "outfit", "con cualquier outfit", 430, 520, False), (1, "ruido", "ruido: OFF", 1660, 400, True),
           (2, "caros", "de los caros", 430, 520, False), (2, "bonita", "con letra bonita", 430, 520, True)],
    "p1": [(1, "dije", "¡te lo dije!", 430, 520, True), (1, "utiles", "útiles, sí...", 430, 520, False),
           (1, "tristeza", "la tristeza", 430, 520, True), (2, "excepcion", "la única excepción:", 430, 520, False),
           (2, "arte", "son ARTE", 430, 520, True)],
    "m1": [(1, "amigas", "para tus amigas", 430, 520, True), (1, "pared", "para tu pared", 430, 520, False),
           (1, "agenda", "para tu agenda", 430, 520, True), (2, "rapidisimo", "¡se acaban\nrapidísimo!", 430, 520, False),
           (2, "mas", "¡vas a querer más!", 430, 520, True)],
}
# piezas secundarias: id → [(frase, palabra, sticker, alto, x, y, rot, fin, opciones)] — cada cosa que la voz nombra, en ese segundo.
# fin: None (hasta el final de la escena) · (frase, palabra) · segundos. opciones: dt, gris, modo, detras, tinte.
_LLUVIA = [(720, 360, -10), (830, 770, 12), (1480, 300, 8), (1500, 790, -6), (1860, 560, 10), (980, 160, -4)]
SEC = {
    "m15": [(1, "perfecto", "foto_squishy", 360, 1640, 450, -5, (2, "mochila"), {})],
    "m13": [(1, "ti", "pulsera", 240, 1660, 430, 0, (2, "barato"), {}), (1, "amiga", "pulsera_b", 240, 1700, 700, 8, (2, "barato"), {})]
    + [(1, "salon", ("pulsera", "pulsera_b", "pulsera_c")[i % 3], 130, x, y, r, (2, "barato"), {"dt": 0.08 * i})
       for i, (x, y, r) in enumerate(_LLUVIA)]
    + [(2, "vacaciones", "arbolito", 330, 1660, 560, 4, None, {})],
    "m11": [(1, "fresa", "fresa", 240, 1660, 650, 8, (2, "tocador"), {}), (2, "tocador", "ramo", 260, 1650, 640, 6, None, {"dt": 0.3}),
            (2, "tocador", "labial", 200, 1500, 770, -8, None, {"dt": 0.45})],
    "m12": [(0, "crema", "crema", 300, 1460, 600, 6, None, {}), (1, "sol", "sol", 230, 1690, 420, 0, (2, "aburrido"), {}),
            (1, "invierno", "copo", 120, 1500, 330, 0, (2, "aburrido"), {})],
    "p9": [(1, "fotos", "fotos", 240, 1660, 420, 6, (1, "decoloracion"), {}),
           (2, "clips", "pinzas_b", 260, 1480, 470, -8, None, {}), (2, "gis", "gises", 300, 1690, 660, 6, None, {})],
    "m10": [(1, "crema", "crema_peinar", 340, 1460, 560, -6, None, {}), (1, "aceite", "aceite", 340, 1670, 600, 8, None, {})],
    "m8": [(1, "curitas", "curita", 110, 1480, 370, -10, (2, "parece"), {"sale_a": (1150, 520)}),
           (1, "toallitas", "toallitas", 160, 1710, 460, 6, (2, "parece"), {"sale_a": (1150, 520)}),
           (1, "desodorante", "desodorante", 230, 1500, 640, -6, (2, "parece"), {"sale_a": (1150, 520)}),
           (1, "gel", "gel", 220, 1710, 700, 8, (2, "parece"), {"sale_a": (1150, 520)}),
           (1, "ligas", "scrunchies_a", 150, 1180, 820, 4, (2, "parece"), {"sale_a": (1150, 520)}),
           (1, "balsamo", "balsamo_solo", 210, 1840, 560, 10, (2, "parece"), {"sale_a": (1150, 520)})],
    "p8": [(2, "tres", "balsamo_solo", 300, 1500, 470, -6, None, {"dt": 0.3}), (2, "tres", "labial", 260, 1690, 560, 8, None, {"dt": 0.45}),
           (2, "tres", "labios", 150, 1560, 770, -4, None, {"dt": 0.6})],
    "m9": [(1, "nube", "nube", 300, 1180, 720, 0, None, {"detras": True}), (2, "chocolate", "chocolate", 300, 1660, 640, 6, None, {})],
    "p7": [(1, "campana", "tienda", 300, 1660, 420, 0, (1, "chiquita"), {}), (1, "muneca", "bebe", 320, 1580, 640, 6, None, {})],
    "m7": [(0, "mochila", "mochila", 280, 520, 640, -6, (1, "llaveritos"), {}), (2, "juntando", "mariposa", 140, 1000, 200, -8, None, {}), (2, "juntando", "cerezas", 140, 1320, 190, 8, None, {"dt": 0.15}),
           (2, "juntando", "mora", 120, 1660, 380, 4, None, {"dt": 0.3})],
    "p6": [(2, "lista", "carta", 320, 1660, 640, 8, None, {})],
    "m6": [(0, "labios", "labios", 170, 1660, 420, -8, (1, "natural"), {}), (1, "exagerar", "labial", 320, 1660, 600, 10, None, {})],
    "p5": [(1, "jabon", "jabon", 200, 1640, 400, -6, None, {}), (1, "esponja", "esponja", 190, 1720, 610, 8, None, {}),
           (1, "gel", "gel", 260, 1520, 740, -4, None, {}), (2, "gigante", "mono", 460, 1180, 300, 0, None, {"modo": "cae"})],
    "m5": [(0, "bonito", "foto_termo", 380, 1640, 560, 6, (1, "derraman"), {}), (2, "todas", "termo", 380, 1620, 600, 6, (2, "stickers"), {"gris": 0.5}),
           (2, "todas", "termo", 380, 1790, 620, -6, (2, "stickers"), {"gris": 0.5, "dt": 0.15}),
           (2, "stickers", "estrella", 90, 1170, 610, -10, None, {}), (2, "stickers", "cerezas", 100, 1205, 450, 6, None, {"dt": 0.12}),
           (2, "stickers", "mono", 90, 1150, 730, 4, None, {"dt": 0.24}), (2, "charm", "oso", 120, 1300, 390, 10, None, {})],
    "p4": [(1, "originales", "foto_original", 300, 1650, 520, 6, (1, "lata"), {}), (1, "lata", "lata", 260, 1660, 600, -8, (1, "bateria"), {}), (1, "bateria", "bateria_llena", 130, 1660, 600, 0, (1, "dos"), {}),
           (1, "dos", "bateria_vacia", 130, 1660, 600, 0, (2, "sencillos"), {}),
           (2, "sencillos", "foto_original", 300, 1660, 520, 8, None, {})],
    "m4": [(0, "suavecito", "foto_oso", 420, 1640, 560, -6, (1, "cama"), {}), (2, "croissant", "croissant", 220, 1460, 440, -6, None, {}), (2, "aguacate", "aguacate", 240, 1670, 570, 6, None, {}),
           (2, "fresa", "fresa", 220, 1490, 730, -4, None, {})],
    "p3": [(1, "pelicula", "claqueta", 260, 1660, 420, 8, (1, "juguete"), {})],
    "m3": [(2, "mesa", "foto_juego", 400, 1580, 540, -5, None, {})],
    "p2": [(0, "cremas", "crema", 300, 1640, 600, 6, (1, "internet"), {}), (1, "internet", "celular", 320, 1660, 640, 8, (1, "necesita"), {}),
           (2, "lavarla", "jabon", 190, 1390, 430, -6, None, {}), (2, "crema", "crema", 230, 1690, 480, 6, None, {}),
           (2, "bloqueador", "bloqueador", 280, 1540, 740, -8, None, {})],
    "m2": [(0, "diadema", "foto_audifonos", 380, 1640, 560, -5, (1, "ruido"), {}), (1, "estudiar", "libros", 240, 1660, 640, 6, (2, "caros"), {}), (2, "carta", "carta", 320, 1660, 600, -6, None, {})],
    "p1": [(1, "cajon", "cajon", 320, 1650, 620, 4, (2, "excepcion"), {}),
           (2, "navidenos", "calcetin_nav1", 300, 1480, 470, -8, None, {}), (2, "navidenos", "calcetin_nav2", 300, 1680, 480, 8, None, {"dt": 0.2}),
           (2, "chistosos", "calcetin_reno1", 270, 1540, 750, -6, None, {}), (2, "chistosos", "calcetin_reno2", 270, 1760, 760, 6, None, {"dt": 0.2})],
    "m1": [(0, "instantanea", "foto_camara", 420, 1640, 560, 6, (1, "impresa"), {}), (1, "pared", "fotos", 240, 1500, 400, -6, (2, "rollos"), {}), (1, "agenda", "agenda_a", 260, 1700, 640, 8, (2, "rollos"), {}),
           (2, "rollos", "rollo", 280, 1520, 520, -6, None, {}), (2, "rollos", "rollo_b", 260, 1720, 600, 8, None, {"dt": 0.2})],
}
# adornos con los stickers de Amaya (rotan entre ítems)
DECOS = ["mora", "latte", "mono", "bola_disco", "estrella", "hortensia", "mariposa", "libros", "bebida", "labios",
         "perrito_negro", "ramo", "leche_fresa", "labial", "taza_mono"]


def _anclas_item(esc):
    tipo, num, precio, nombre = LISTA[esc]
    a = dict(tipo=tipo, num=num, precio=precio, nombre=nombre)
    a["tit"] = ww(esc, 0, "mejor" if tipo == "m" else "peor")
    a["num_t"] = palabra_tras(esc, 0, "numero")
    a["stk"] = palabra_tras(esc, 0, "numero", 2)
    a["precio_t"] = FIN(esc, 0) + 0.15
    a["sello_t"] = INI(esc, NFRASES(esc) - 1) - 0.25
    notas, fijos = [], []
    for nt in NOTAS.get(esc, []):
        (f, pal, txt, x, y, rosa), extra = nt[:6], nt[6:]
        notas.append([A_(esc, f, pal), txt, x, y, rosa])
        fijos.append(_fin(esc, extra[0], notas[-1][0]) if extra else None)
    for i, n in enumerate(notas):
        fin = n[0] + 3.2 if fijos[i] is None else fijos[i]
        for m in notas[i + 1:]:
            if abs(m[2] - n[2]) < 300 and abs(m[3] - n[3]) < 150:
                fin = min(fin, m[0] - 0.05)
                break
        n.append(min(fin, T1(esc) - 0.5))
    a["notas"] = notas
    sec = []
    for i, (f, pal, nom, alto, x, y, rot, fin, op) in enumerate(SEC.get(esc, [])):
        t0 = A_(esc, f, pal) + op.get("dt", 0.0)
        sec.append(dict(t0=t0, fin=_fin(esc, fin, t0), nom=nom, alto=alto, x=x, y=y, rot=rot, sem=700 + i, **op))
    a["sec"] = sec
    a["credito"] = A_(esc, *CREDITO[esc]) if esc in CREDITO else None
    return a


CREDITO = {"m12": (1, "puse"), "m10": (1, "lista"), "m8": (1, "puse"), "p9": (1, "escogi"), "p8": (0, "puse"), "p2": (0, "lista"),
           "m7": (0, "lista"), "m6": (0, "lista"), "p7": (2, "lista"), "p5": (2, "higiene")}


@lru_cache(maxsize=1)
def insignia():
    """Pegatina «elegido por Amaya» con corazón (crédito de su lista escrita a mano)."""
    f = C.fuente("Inkfree.ttf", 46)
    txt = "elegido por Amaya"
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + 130, 86
    im = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w + 6, h + 6), radius=h // 2, fill=(255, 255, 255, 255))
    d.rounded_rectangle((12, 12, w, h), radius=h // 2 - 6, fill=(217, 79, 134, 255))
    d.text((40 - bb[0], (h + 12 - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f, fill=(255, 255, 255, 255))
    cx, cy, r = w - 46, (h + 12) / 2, 17
    d.ellipse((cx - r, cy - r - 4, cx, cy + 4 - 4), fill=(255, 255, 255, 255))
    d.ellipse((cx, cy - r - 4, cx + r, cy + 4 - 4), fill=(255, 255, 255, 255))
    d.polygon([(cx - r, cy - 6), (cx + r, cy - 6), (cx, cy + r + 2)], fill=(255, 255, 255, 255))
    return C.a_rgba(im)


def dibuja_sec(im, t, a, detras):
    for s in a["sec"]:
        if bool(s.get("detras")) != detras:
            continue
        S(im, s["nom"], s["alto"], s["x"], s["y"], t, s["t0"], rot=s["rot"], sale=s["fin"], modo=s.get("modo", "pop"),
          gris=s.get("gris", 0.0), sem=s["sem"], tinte=s.get("tinte"), sale_a=s.get("sale_a"))


ANC = {e: _anclas_item(e) for e in LISTA if e in ESC}

for e, a in ANC.items():
    ev(a["tit"], "letras", 0.4, -0.6)
    ev(a["stk"] + 0.3, "cae", 0.6, 0.2)
    ev(a["stk"] + 0.55, "pop", 0.25, -0.2)
    ev(a["stk"] + 0.85, "pop", 0.25, 0.8)
    ev(a["precio_t"], "etiqueta", 0.5, 0.6)
    ev(a["sello_t"] - 0.45, "pop_avatar", 0.35, -0.8)
    ev(a["sello_t"], "sello", 0.8, -0.4)
    if a["tipo"] == "m":
        ev(a["sello_t"] + 0.2, "acierto", 0.4, -0.4)
    else:
        ev(a["sello_t"] + 0.25, "bajon", 0.35, 0.2)
    for n in a["notas"]:
        ev(n[0], "nota", 0.3, (n[2] - 960) / 960)
    if a.get("credito"):
        ev(a["credito"], "corazones", 0.35, 0.2)
    for s in a["sec"]:
        ev(s["t0"] + (0.3 if s.get("modo") == "cae" else 0.0), "cae" if s.get("modo") == "cae" else "pop", 0.4,
           (s["x"] - 960) / 960)


# ---- ganchos por ítem: cambian el sticker principal (P) y dibujan lo propio; devuelven lo que va ENCIMA del sticker
def mod_m15(im, t, a, P):
    ap, es, rg = ww("m15", 1, "aplastas"), ww("m15", 1, "estiras"), ww("m15", 1, "regresa")
    b1, b2 = bump(t, ap - 0.05, es - 0.05), bump(t, es - 0.05, rg)
    g = amort(t, rg, 3.0, 3.2) * 0.12
    P["sy"] = 1 - 0.38 * b1 + 0.32 * b2 + g
    P["sx"] = 1 + 0.30 * b1 - 0.22 * b2 - g
    P["y"] += 0.19 * P["alto"] * b1 - 0.15 * P["alto"] * b2
    if ap - 0.05 < t < rg + 1.0:
        P["bob"] = 0.0
    S(im, "carta", 300, 1660, 470, t, ww("m15", 2, "listas"), modo="pop", rot=8, sem=91)


def mod_m14(im, t, a, P):
    car, scr = ww("m14", 1, "carey"), ww("m14", 1, "scrunchies")
    P["esc"] = 1 + 0.12 * bump(t, car - 0.05, car + 0.5)
    vuela = ww("m14", 2, "perder") - 0.1
    pul = 1 + 0.12 * bump(t, scr - 0.05, scr + 0.5)

    def encima(im):
        S(im, "scrunchies", 330, 1420, 730, t, ww("m14", 0, "scrunchies"), rot=6, sem=92, esc=pul, sale=vuela,
          sale_a=(2300, -200))
        if t > vuela:
            S(im, "scrunchies_a", 280, 1420, 740, t, vuela + 0.7, modo="pop", rot=-5, sem=93)
    return encima


def mod_p10(im, t, a, P):
    ti, de, cl, na = ww("p10", 1, "tierno"), ww("p10", 1, "descubres"), ww("p10", 1, "clip"), ww("p10", 1, "nada")
    corazones(im, t, ti - 0.3, de - 0.4, 1180, 420, n=5, sem=95)
    li = ww("p10", 2, "libreta")
    if t > li - 0.1:
        P["x"] -= 330 * suave(pr(t, li - 0.1, li + 0.4))
        P["esc"] *= 1 - 0.25 * suave(pr(t, li - 0.1, li + 0.4))

    def encima(im):
        candado = (P["x"] + 0.205 * P["alto"] * P["esc"], P["y"] + 0.13 * P["alto"] * P["esc"])
        if cl - 0.55 < t < na + 1.0:
            u = e_out(pr(t, cl - 0.55, cl + 0.1))
            x = -150 + (candado[0] + 50 + 150) * u
            y = 900 + (candado[1] + 10 - 900) * u - math.sin(math.pi * u) * 260
            S(im, "clip", 190, x, y, t, cl - 0.55, modo="pop", rot=-40 + 20 * u, bob=0, sem=96)
        if t > cl + 0.1:
            pegar(im, C.destello(60, (1, 0.95, 0.6)), candado[0], candado[1], esc=1.6 * bump(t, cl + 0.1, cl + 0.6), sombra=0)
            N(im, "¡CLIC!", candado[0] + 150, candado[1] - 220, t, cl + 0.1, na - 0.1, sem=97, rosa=True, px=64, rot=10)
        if t > li - 0.1:
            S(im, "agenda_a", 470, 1480, 560, t, li, rot=6, sem=98)
            pegar(im, C.corazon(44), 1660, 300, esc=rebote(t, li + 0.3, 0.35), sombra=0.15)
    return encima


# ---- utilidades de los ganchos
def mover(P, t, t0, x=None, y=None, esc=1.0, d=0.45):
    u = suave(pr(t, t0 - 0.1, t0 - 0.1 + d))
    if x is not None:
        P["x"] += (x - P["x"]) * u
    if y is not None:
        P["y"] += (y - P["y"]) * u
    P["esc"] *= 1 + (esc - 1) * u


def agitar(P, t, t0, d=0.9, amp=6.0):
    k = bump(t, t0, t0 + d)
    P["rot"] += amp * math.sin(t * 40) * k
    P["x"] += amp * 1.4 * math.sin(t * 55) * k


@lru_cache(maxsize=2)
def _halo(cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.15) ** 2) / r
    m = np.exp(-d * d * 1.6)[..., None]
    dc = np.clip(d, 0, 1)[..., None]
    col = np.concatenate([np.ones_like(dc), 0.58 + 0.22 * dc, 0.42 + 0.36 * dc], -1)   # naranja al centro → rosa
    return m.astype(np.float32), col.astype(np.float32)


def halo(im, k, cx=1180, cy=420, r=900):
    """Luz de la lámpara de atardecer proyectada en la pared."""
    if k <= 0.01:
        return im
    m, col = _halo(cx, cy, r)
    a = m * (0.85 * k)
    im[:] = im * (1 - a) + col * a
    return im


def flash(im, k):
    if k > 0.01:
        im[:] = im * (1 - k) + k
    return im


def notas_musica(im, t, t0, t1, x0, y0, cada=0.45, sem=0):
    if t < t0:
        return im
    n = int((min(t, t1) - t0) / cada) + 1
    for i in range(n):
        ti = t0 + i * cada
        v = (t - ti) / 2.2
        if not 0 <= v <= 1:
            continue
        lado = -1 if (i + sem) % 2 else 1
        x = x0 + lado * (60 + v * 260) + math.sin(t * 3 + i) * 25
        y = y0 - v * 420
        pegar(im, stk("nota_musical", 80 + 20 * ((i + sem) % 3)), x, y, esc=rebote(t, ti, 0.3), rot=lado * 12 + math.sin(t * 4 + i) * 10,
              alfa=1 - pr(v, 0.65, 1.0), sombra=0.15)
    return im


def copos(im, t, t0, dur=3.2, n=8, sem=0):
    if not t0 < t < t0 + dur + 1.5:
        return im
    rg = np.random.default_rng(sem)
    for i in range(n):
        ti = t0 + i * 0.18
        if t < ti:
            continue
        x = rg.uniform(250, 1850) + math.sin(t * 1.5 + i) * 40
        y = -80 + (t - ti) * rg.uniform(220, 320)
        a = 1 - pr(t, t0 + dur, t0 + dur + 0.6)
        pegar(im, stk("copo", int(rg.uniform(70, 120))), x, y, rot=t * 40 + i * 30, alfa=a, sombra=0.1)
    return im


_GRIETAS = []
for _i in range(5):
    _rg = np.random.default_rng(40 + _i)
    _a = _rg.uniform(0, 2 * math.pi)
    _pts, _p = [(0.0, 0.0)], np.zeros(2)
    for _j in range(6):
        _a += _rg.uniform(-0.6, 0.6)
        _p = _p + np.array([math.cos(_a), math.sin(_a)]) * _rg.uniform(0.04, 0.08)
        _pts.append(tuple(_p))
    _GRIETAS.append(_pts)


def grietas(im, t, t0, cx, cy, escala):
    if t < t0:
        return im
    u = pr(t, t0, t0 + 0.25)
    for pts in _GRIETAS:
        k = max(2, int(len(pts) * u))
        q = np.array([[cx + x * escala, cy + y * escala] for x, y in pts[:k]], np.int32)
        cv2.polylines(im, [q], False, (0.30, 0.20, 0.22), 10, cv2.LINE_AA)
        cv2.polylines(im, [q], False, (1.0, 1.0, 1.0), 2, cv2.LINE_AA)
    return im


def tache(im, t, t0, cx, cy, r=110):
    if t < t0:
        return im
    k = e_out(pr(t, t0, t0 + 0.25))
    for s in (-1, 1):
        p0 = (int(cx - r * k), int(cy - s * r * k))
        p1 = (int(cx + r * k), int(cy + s * r * k))
        cv2.line(im, p0, p1, (1, 1, 1), 30, cv2.LINE_AA)
        cv2.line(im, p0, p1, C.ROJO, 18, cv2.LINE_AA)
    return im


# ---- ganchos de m13 … m1
def mod_m11(im, t, a, P):
    toc, ech = ww("m11", 2, "tocador"), ww("m11", 1, "echas")
    if t > toc - 0.2:       # espejo de tocador detrás del body mist
        k = e_back(pr(t, toc - 0.2, toc + 0.3), 1.4)
        ax, ay = int(150 * k), int(205 * k)
        if ax > 4:
            cv2.ellipse(im, (1180, 470), (ax + 22, ay + 22), 0, 0, 360, (0.93, 0.66, 0.76), -1, cv2.LINE_AA)
            cv2.ellipse(im, (1180, 470), (ax, ay), 0, 0, 360, (0.84, 0.92, 0.97), -1, cv2.LINE_AA)
            cv2.ellipse(im, (1120, 380), (int(ax * 0.18), int(ay * 0.35)), -20, 0, 360, (0.96, 0.98, 1.0), -1, cv2.LINE_AA)
            cv2.rectangle(im, (1180 - ax - 60, 790), (1180 + ax + 60, 820), (0.80, 0.62, 0.50), -1, cv2.LINE_AA)

    def encima(im):
        if ech - 0.05 < t < ech + 1.4:      # «te lo echas»: nube de perfume
            rg = np.random.default_rng(7)
            for i in range(26):
                v = pr(t, ech + i * 0.02, ech + 0.9 + i * 0.02)
                if v <= 0:
                    continue
                ang = math.radians(rg.uniform(-200, -150))
                r = v * rg.uniform(180, 380)
                x, y = 1150 + math.cos(ang) * r, 285 + math.sin(ang) * r * 0.6
                cv2.circle(im, (int(x), int(y)), int(4 + 10 * v), (1.0, 0.86, 0.92), -1, cv2.LINE_AA)
    return encima


def mod_p8(im, t, a, P):
    rom, com, tre = ww("p8", 1, "rompen"), ww("p8", 1, "comezon"), ww("p8", 2, "tres")
    agitar(P, t, rom, 0.6)
    agitar(P, t, com, 1.0, 5)
    mover(P, t, tre, x=870, esc=0.62)
    if t > tre:
        P["gris"] = max(P["gris"], 0.5 * pr(t, tre, tre + 0.4))
    inc = ww("p8", 1, "increible")

    def encima(im):
        if inc < t < inc + 1.4:
            C.destellos(im, t, [(P["x"] - 250, P["y"] - 180), (P["x"] + 240, P["y"] - 160), (P["x"] + 200, P["y"] + 170)], 1.2)
        grietas(im, t, rom, P["x"] + 40 * P["esc"], P["y"] - 20 * P["esc"], 520 * P["esc"])
    return encima


def mod_m9(im, t, a, P):
    copos(im, t, ww("m9", 1, "frio"), sem=9)


def mod_p7(im, t, a, P):
    cam, chi, f2 = ww("p7", 1, "campana"), ww("p7", 1, "chiquita"), INI("p7", 2)
    e = 1 + 0.45 * suave(pr(t, cam - 0.15, cam + 0.35))
    e += (0.38 - e) * suave(pr(t, chi - 0.1, chi + 0.3))
    e += (0.8 - e) * suave(pr(t, f2 - 0.4, f2 + 0.1))
    P["esc"] *= e
    P["y"] -= 50 * (e - 1) if e > 1 else -60 * (1 - e)


def mod_m10(im, t, a, P):
    de, br = ww("m10", 1, "desenreda"), ww("m10", 1, "brillosito")
    P["rot"] += 16 * math.sin((t - de) * 9) * bump(t, de - 0.1, de + 1.4)

    def encima(im):
        if br < t < br + 1.6:
            C.destellos(im, t, [(1580, 380), (1760, 470), (1600, 800), (1300, 330)], 1.3 * bump(t, br, br + 1.6) + 0.2)
    return encima


def mod_m8(im, t, a, P):
    pa = ww("m8", 2, "parece")
    P["esc"] *= 1 + 0.12 * bump(t, pa + 0.2, pa + 0.8)


def mod_p9(im, t, a, P):
    qu, ir = ww("p9", 1, "quiebra"), ww("p9", 1, "irritar")
    agitar(P, t, qu, 0.9, 6)
    k = bump(t, ir - 0.1, ir + 1.6)
    if k > 0:
        P["tinte"] = ((0.95, 0.30, 0.32), 0.35 * k)


def mod_m7(im, t, a, P):
    charms = [("osito", "oso", 150, 1490, 650), ("fresa", "fresa", 130, 1600, 600), ("estrella", "estrella", 110, 1710, 660)]

    def encima(im):
        piv = (1420, 430)
        for i, (pal, nom, alto, x, y) in enumerate(charms):
            t0 = ww("m7", 1, pal)
            if t < t0:
                continue
            th = math.radians(10 * math.sin(t * 2.6 + i * 1.3) + 10 * amort(t, t0, 2.0, 2.0))
            L = math.hypot(x - piv[0], y - piv[1])
            a0 = math.atan2(x - piv[0], y - piv[1]) + th
            cx, cy = piv[0] + L * math.sin(a0), piv[1] + L * math.cos(a0)
            s = rebote(t, t0, 0.4)
            cv2.line(im, piv, (int(piv[0] + (cx - piv[0]) * s), int(piv[1] + (cy - alto * 0.45 - piv[1]) * s)), (0.85, 0.7, 0.4), 5,
                     cv2.LINE_AA)
            pegar(im, stk(nom, alto), cx, cy, esc=s, rot=-math.degrees(th), sombra=0.25)
        cv2.circle(im, piv, 14, (0.85, 0.7, 0.4), 5, cv2.LINE_AA)
    return encima


def mod_p6(im, t, a, P):
    ll, f2 = ww("p6", 1, "llora"), INI("p6", 2) + 1.5

    def encima(im):
        if not ll < t < f2:
            return
        w = stk("bebe", P["alto"]).shape[1] * P["esc"]
        h = P["alto"] * P["esc"]
        x0, y0 = P["x"] - w / 2, P["y"] - h / 2
        for ojo in (0.335, 0.455):
            ex, ey = x0 + ojo * w, y0 + 0.185 * h
            for j in range(3):
                ph = ((t - ll) * 1.3 + j / 3) % 1
                cv2.ellipse(im, (int(ex), int(ey + ph * 150)), (9, 14), 0, 0, 360, (0.98, 0.75, 0.45)[::-1], -1, cv2.LINE_AA)
    return encima


def mod_m6(im, t, a, P):
    br, ex = ww("m6", 1, "brillosito"), ww("m6", 1, "exagerar")

    def encima(im):
        if br < t < br + 1.6:
            C.destellos(im, t, [(P["x"] - 200, P["y"] - 260), (P["x"] + 180, P["y"] - 200), (P["x"] - 170, P["y"] + 150),
                                (P["x"] + 210, P["y"] + 120)], 1.4 * bump(t, br, br + 1.6) + 0.2)
        tache(im, t, ex + 0.35, 1660, 610, r=95)
    return encima


def mod_p5(im, t, a, P):
    agitar(P, t, ww("p5", 1, "plastico"), 1.0, 4)


def mod_m5(im, t, a, P):
    d = ww("m5", 1, "derraman")
    P["rot"] += 24 * math.sin((t - d) * 5.5) * bump(t, d - 0.1, d + 1.5)


def mod_p4(im, t, a, P):
    agitar(P, t, ww("p4", 1, "lata"), 1.1, 6)


def mod_m4(im, t, a, P):
    mover(P, t, ww("m4", 2, "comida"), x=900, y=470, esc=0.72)
    cu = ww("m4", 2, "cuarto")
    corazones(im, t, cu, cu + 1.4, 1500, 560, n=6, sem=44)


def mod_m3(im, t, a, P):
    agitar(P, t, ww("m3", 1, "pierda"), 1.0, 6)
    mover(P, t, ww("m3", 2, "mesa"), x=860, esc=0.7)
    ge = ww("m3", 2, "gente")
    corazones(im, t, ge, ge + 1.4, 1250, 560, n=6, sem=33)


def mod_p2(im, t, a, P):
    irr = ww("p2", 1, "irritar")
    k = bump(t, irr - 0.1, irr + 1.8)
    if k > 0:
        P["tinte"] = ((0.95, 0.30, 0.32), 0.38 * k)
    agitar(P, t, irr, 0.8, 4)
    mover(P, t, ww("p2", 2, "tres"), x=880, esc=0.7)


def mod_m2(im, t, a, P):
    ru, mu, f2 = ww("m2", 1, "ruido"), ww("m2", 1, "musica"), INI("m2", 2)

    def encima(im):
        if ru - 0.1 < t < ru + 1.8:      # el ruido llega por los lados y se queda afuera de los audífonos
            for side in (-1, 1):
                for j in range(3):
                    v = ((t - ru) * 1.1 + j / 3) % 1
                    x = 1180 + side * (860 - 420 * v)
                    ys = np.linspace(380, 680, 9)
                    q = np.array([[x + (14 if i % 2 else -14), y] for i, y in enumerate(ys)], np.int32)
                    cv2.polylines(im, [q], False, (0.55, 0.52, 0.56), 7, cv2.LINE_AA)
        notas_musica(im, t, mu, f2, 1180, 330, sem=2)
    return encima


def mod_p1(im, t, a, P):
    tr, cj, exc = ww("p1", 1, "tristeza"), ww("p1", 1, "cajon"), ww("p1", 2, "excepcion")
    k = suave(pr(t, tr - 0.1, tr + 0.5))
    P["sy"] *= 1 - 0.12 * k
    P["y"] += 40 * k
    P["gris"] = max(P["gris"], 0.4 * k)
    mover(P, t, exc, x=860, esc=0.7)

    def encima(im):
        if cj + 0.3 < t < exc - 0.05:
            pegar(im, C.cinta("SECRETO", 50, C.ROSA_FUERTE, (1, 1, 1), 3), 1650, 640, esc=rebote(t, cj + 0.3, 0.35), rot=-16, sombra=0.2)
        ar = ww("p1", 2, "arte")
        if t > ar:
            C.destellos(im, t, [(1480, 330), (1760, 360), (1820, 640), (1420, 620)], 1.1)
    return encima


def mod_m1(im, t, a, P):
    fo, imp, am = ww("m1", 1, "foto"), ww("m1", 1, "impresa"), ww("m1", 1, "amigas")

    def encima(im):
        if imp - 0.2 < t < am + 0.4:       # la foto sale de la cámara y se va a un lado
            u = e_out(pr(t, imp - 0.2, imp + 0.7))
            v = suave(pr(t, am - 0.1, am + 0.4))
            x, y = 1180 + (1640 - 1180) * u, 760 + (540 - 760) * u
            pegar(im, stk("fotos_b", int(180 + 80 * u)), x, y, rot=-4 + 12 * u, alfa=1 - v, esc=1 - 0.3 * v, sombra=0.25)
        flash(im, 0.85 * bump(t, fo, fo + 0.35))
        st = a["sello_t"]
        corazones(im, t, st + 0.2, st + 1.6, 1180, 520, n=9, sem=11)
    return encima


MOD = {"m15": mod_m15, "m14": mod_m14, "p10": mod_p10, "m11": mod_m11, "m10": mod_m10, "p8": mod_p8, "m9": mod_m9,
       "p7": mod_p7, "m8": mod_m8, "p9": mod_p9, "m7": mod_m7, "p6": mod_p6, "m6": mod_m6, "p5": mod_p5, "m5": mod_m5, "p4": mod_p4,
       "m4": mod_m4, "m3": mod_m3, "p2": mod_p2, "m2": mod_m2, "p1": mod_p1, "m1": mod_m1}

# sonidos de los ganchos (mismas anclas)
ev(ww("m11", 1, "echas"), "spray", 0.45, 0.2)
ev(ww("m11", 2, "tocador") - 0.2, "destello", 0.3)
ev(ww("m10", 1, "desenreda"), "whoosh", 0.3)
ev(ww("m10", 1, "brillosito"), "destello", 0.45)
ev(ww("p9", 1, "quiebra"), "crujido", 0.5)
ev(ww("p9", 1, "irritar"), "bajon", 0.3)
ev(ww("p8", 1, "rompen"), "crujido", 0.55, 0.1)
ev(ww("p8", 2, "tres") - 0.1, "whoosh", 0.3, -0.3)
ev(ww("m9", 1, "frio"), "destello", 0.3)
ev(ww("p7", 1, "campana") - 0.15, "boing_triste", 0.4)
ev(ww("p7", 1, "chiquita") - 0.1, "whoosh", 0.3)
ev(ww("m8", 2, "parece"), "whoosh", 0.35)
for _w in ("osito", "fresa", "estrella"):
    ev(ww("m7", 1, _w), "ding", 0.3, 0.6)
ev(ww("p6", 1, "llora"), "boing_triste", 0.4)
ev(ww("m6", 1, "brillosito"), "destello", 0.45)
ev(ww("m6", 1, "exagerar") + 0.35, "sello", 0.4, 0.6)
ev(ww("p5", 1, "plastico"), "crujido", 0.4)
ev(ww("m5", 1, "derraman"), "whoosh", 0.3)
ev(ww("p4", 1, "lata"), "lata", 0.5, 0.6)
ev(ww("m4", 2, "comida") - 0.1, "whoosh", 0.3, -0.3)
ev(ww("m4", 2, "cuarto"), "corazones", 0.35, 0.5)
ev(ww("p3", 1, "pelicula"), "claqueta", 0.5, 0.6)
ev(ww("m3", 1, "pierda"), "boing_triste", 0.4)
ev(ww("m3", 2, "gente"), "corazones", 0.35)
ev(ww("p2", 1, "irritar"), "bajon", 0.3)
ev(ww("m2", 1, "musica"), "cajita", 0.35)
ev(ww("p1", 1, "tristeza"), "boing_triste", 0.45)
ev(ww("p1", 1, "cajon") + 0.3, "cinta", 0.45, 0.6)
ev(ww("p1", 2, "arte"), "destello", 0.45, 0.6)
ev(ww("m1", 1, "foto"), "flash", 0.55)
ev(ww("m1", 2, "rapidisimo"), "whoosh", 0.3)


# ============================================================ SUSCRIBE (como el final de suscripción de Amaya)
@lru_cache(maxsize=1)
def logo_play(w=330, h=232):
    im = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((5, 5, w + 5, h + 5), radius=int(h * 0.3), fill=(232, 38, 44, 255))
    d.polygon([(w * 0.40 + 5, h * 0.28 + 5), (w * 0.40 + 5, h * 0.72 + 5), (w * 0.66 + 5, h * 0.5 + 5)], fill=(255, 255, 255, 255))
    return C.a_rgba(im)


@lru_cache(maxsize=4)
def boton(txt, suscrito=False, w=560, h=128):
    im = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w + 6, h + 6), radius=h // 2, fill=(222, 222, 226, 255) if suscrito else (232, 38, 44, 255))
    f = C.fuente("Poppins-ExtraBold.ttf", 54)
    bb = f.getbbox(txt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x0 = (w + 12 - tw) / 2 + (34 if suscrito else 0)
    col = (88, 88, 96, 255) if suscrito else (255, 255, 255, 255)
    d.text((x0 - bb[0], (h + 12 - th) / 2 - bb[1]), txt, font=f, fill=col)
    if suscrito:
        d.line([(x0 - 78, h * 0.55), (x0 - 54, h * 0.76), (x0 - 16, h * 0.32)], fill=col, width=13, joint="curve")
    return C.a_rgba(im)


def boton_suscribe(im, t, x, y, t0, clic, sale=None, sem=0):
    """Botón rojo «SUSCRÍBETE» → la mano da clic con destellos → «✓ SUSCRITO» gris + la campana que suena."""
    if t < t0 or (sale is not None and t > sale + 0.4):
        return im
    s = rebote(t, t0, 0.45) * (1 - suave(pr(t, sale, sale + 0.35)) if sale else 1) * (1 - 0.08 * bump(t, clic - 0.02, clic + 0.18))
    pegar(im, boton("SUSCRITO", True) if t > clic + 0.05 else boton("SUSCRÍBETE"), x, y, esc=s, sombra=0.25)
    if t > clic:
        c = t - clic
        rot = 26 * math.sin(c * 13) * math.exp(-c * 1.3)
        pegar(im, stk("campana", 170), x + 400, y - 70, esc=s * rebote(t, clic + 0.05, 0.35), rot=rot, ancla=(0.5, 0.08), sombra=0.25)
        if c < 1.2:
            C.destellos(im, t, [(x - 300, y - 90), (x + 300, y - 100), (x - 260, y + 100), (x + 220, y + 110)], 1.4 * (1.2 - c))
    if clic - 0.8 < t < clic + 0.9:      # la mano de Amaya (su sticker) entra y da clic
        u = e_out(pr(t, clic - 0.8, clic - 0.12))
        w_ = suave(pr(t, clic + 0.35, clic + 0.9))
        mx = 1780 + (x + 90 - 1780) * u + w_ * 600
        my = 1200 + (y + 18 - 1200) * u + w_ * 500
        pegar(im, stk("mano", 230), mx, my, esc=1 - 0.12 * bump(t, clic - 0.08, clic + 0.18), rot=-12, ancla=(0.36, 0.03), sombra=0.3)
    return im


class SU:
    antes = ww("suscribe", 0, "antes")
    lista = ww("suscribe", 0, "lista")
    sus = ww("suscribe", 0, "suscribete")
    gratis = ww("suscribe", 0, "gratis")
    semana = ww("suscribe", 0, "semana")
    f1 = INI("suscribe", 1)
    faltan = ww("suscribe", 1, "faltan")
    mejores = ww("suscribe", 1, "mejores")
    peores = ww("suscribe", 1, "peores")
    uno = ww("suscribe", 1, "uno")
    casa = ww("suscribe", 1, "casa")


ev(SU.antes, "pop", 0.5, 0.2)
ev(SU.antes + 0.3, "pop_avatar", 0.45, -0.6)
ev(SU.lista, "pop", 0.4, 0.3)
ev(SU.sus - 0.75, "whoosh", 0.3, 0.7)
ev(SU.sus, "clic", 0.6, 0.3)
ev(SU.sus + 0.05, "campana", 0.5, 0.6)
ev(SU.sus + 0.1, "destello", 0.4)
ev(SU.gratis, "nota", 0.35, 0.6)
ev(SU.semana, "nota", 0.35, 0.6)
for _k in range(8):
    ev(SU.antes + 0.6 + 0.12 * _k, "pop", 0.22, -0.4 + 0.12 * _k)
ev(SU.f1 - 0.3, "whoosh", 0.35)
ev(SU.faltan, "letras", 0.45)
ev(SU.mejores, "misterio", 0.35, -0.4)
ev(SU.peores, "letras", 0.35, 0.4)
ev(SU.uno, "pop", 0.4, 0.4)
ev(SU.casa, "cae", 0.55, 0.4)
ev(SU.casa + 0.35, "cinta", 0.45, 0.4)
ev(SU.casa + 0.6, "misterio", 0.4, 0.4)

SOMBRA_MISTERIO = ((0.36, 0.17, 0.27), 1.0)


def suscribe(t):
    im = np.empty((H, W, 3), np.float32)
    im[:] = (0.985, 0.86, 0.90)
    # fila de stickers de Amaya abajo
    for k, n in enumerate(("mora", "latte", "perrito_negro", "bola_disco", "labios", "hortensia", "estrella", "bebida")):
        S(im, n, 140, 650 + k * 168, 960 + (12 if k % 2 else -6), t, SU.antes + 0.6 + 0.12 * k, modo="pop", rot=(-8, 6, -4, 8)[k % 4],
          sem=900 + k)
    avatar(im, t, 330, 640, SU.antes + 0.3, si=(SU.sus + 0.1, SU.casa + 0.5), sem=5)
    s1 = SU.f1 - 0.3
    if t < s1 + 0.5:
        if t > SU.antes:
            s = rebote(t, SU.antes, 0.5) * (1 - suave(pr(t, s1, s1 + 0.35)))
            pegar(im, logo_play(), 1180, 290, esc=s * (1 + 0.04 * math.sin(t * 3)), sombra=0.25)
        boton_suscribe(im, t, 1180, 560, SU.lista, SU.sus, sale=s1)
        N(im, "¡es gratis!", 1660, 300, t, SU.gratis, s1, sem=910, rosa=True, rot=8, px=58)
        N(im, "listas nuevas\ncada semana", 1640, 770, t, SU.semana, s1, sem=911, rot=-5)
    else:
        R(im, "¡Faltan...", 1180, 160, 110, t, SU.faltan, sem=920, cada=0.04)
        R(im, "MEJORES", 900, 330, 76, t, SU.mejores, sem=921, cada=0.04)
        S(im, "audifonos", 290, 800, 590, t, SU.mejores + 0.1, modo="pop", rot=-8, sem=922, tinte=SOMBRA_MISTERIO)
        S(im, "camara", 290, 1010, 620, t, SU.mejores + 0.25, modo="pop", rot=7, sem=923, tinte=SOMBRA_MISTERIO)
        R(im, "?", 905, 600, 160, t, SU.mejores + 0.45, sem=924)
        R(im, "PEORES", 1500, 330, 76, t, SU.peores, sem=925, cada=0.04)
        if t < SU.casa + 0.2:
            S(im, "calcetines", 320, 1500, 610, t, SU.uno, modo="pop", rot=-4, sem=926, tinte=SOMBRA_MISTERIO, sale=SU.casa - 0.1)
            R(im, "?", 1500, 610, 160, t, SU.uno + 0.2, sem=927, sale=SU.casa - 0.1)
        S(im, "cajon", 380, 1500, 620, t, SU.casa, rot=4, sem=928)
        if t > SU.casa + 0.35:
            pegar(im, C.cinta("SECRETO", 60, C.ROSA_FUERTE, (1, 1, 1), 3), 1500, 630, esc=rebote(t, SU.casa + 0.35, 0.35), rot=-16,
                  sombra=0.2)
            N(im, "¿ya sabes cuál?", 1690, 820, t, SU.casa + 0.6, sem=929, rosa=True, rot=6)
    return im


# ============================================================ CIERRE
@lru_cache(maxsize=2)
def globo(w=640, h=300):
    im = Image.new("RGBA", (w + 20, h + 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lc = (96, 62, 64, 255)
    d.rounded_rectangle((10, 10, w + 10, h + 10), radius=70, fill=(255, 255, 255, 255), outline=lc, width=6)
    d.polygon([(120, h + 4), (90, h + 80), (210, h + 4)], fill=(255, 255, 255, 255))
    d.line([(120, h + 10), (90, h + 80), (210, h + 10)], fill=lc, width=6)
    return C.a_rgba(im)


@lru_cache(maxsize=2)
def caja_video(w=500, h=282, txt="próxima lista"):
    im = Image.new("RGBA", (w + 20, h + 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 10, h + 10), radius=22, fill=(255, 250, 252, 255), outline=(217, 79, 134, 255), width=8)
    for k in range(0, w - 40, 36):
        d.line([(30 + k, 30), (30 + k + 18, 30)], fill=(240, 180, 200, 255), width=4)
    d.polygon([(w / 2 - 30, h / 2 - 40), (w / 2 - 30, h / 2 + 60), (w / 2 + 55, h / 2 + 10)], fill=(240, 160, 190, 255))
    f = C.fuente("Inkfree.ttf", 44)
    bb = f.getbbox(txt)
    d.text(((w + 20 - (bb[2] - bb[0])) / 2 - bb[0], h + 30), txt, font=f, fill=(90, 42, 60, 255))
    return C.a_rgba(im)


class CI:
    lista = ww("cierre", 0, "lista")
    coment = ww("cierre", 0, "comentarios")
    cual = ww("cierre", 0, "cual")
    carta = ww("cierre", 0, "carta")
    peor = ww("cierre", 0, "peor")
    f1 = INI("cierre", 1)
    like = ww("cierre", 1, "like")
    sus = ww("cierre", 1, "suscribete")
    soy = ww("cierre", 1, "soy")
    vemos = ww("cierre", 1, "vemos")
    bye = ww("cierre", 1, "bye")
    espero = ww("cierre", 1, "espero")


ev(CI.lista, "letras", 0.4)
for _k in range(25):
    ev(CI.lista + 0.2 + 0.05 * _k, "pop", 0.12, -0.3 + 0.03 * _k)
ev(CI.coment - 0.25, "whoosh", 0.3)
ev(CI.coment, "pop", 0.5, 0.2)
ev(CI.carta, "cae", 0.45, 0.6)
ev(CI.peor, "boing_triste", 0.35, -0.2)
ev(CI.f1 - 0.2, "whoosh", 0.3)
ev(CI.like, "pop", 0.5, -0.2)
ev(CI.like + 0.3, "clic", 0.5, -0.2)
ev(CI.like + 0.35, "corazones", 0.4, -0.2)
ev(CI.sus, "clic", 0.55, 0.4)
ev(CI.sus + 0.05, "campana", 0.5, 0.6)
ev(CI.soy, "letras", 0.45)
ev(CI.vemos - 0.2, "whoosh", 0.35)
ev(CI.vemos, "ding", 0.4)
ev(CI.bye, "pop_avatar", 0.4, -0.6)
ev(CI.espero, "corazones", 0.35, 0.3)
for _k in range(6):
    ev(CI.f1 + 0.15 * _k, "pop", 0.25, -0.2 + 0.1 * _k)

_RECAP = list(LISTA)


def cierre(t):
    im = C.fondo("vichy_amaya", t + 90)
    C.esquinas(im, t, t0=-10, sem=4)
    avatar(im, t, 330, 640, T0("cierre") + 0.2, si=(CI.espero, CI.like, CI.sus + 0.1, CI.bye), sem=6)
    # repaso: los 25 stickers de la lista
    if t < CI.coment + 0.2:
        for i, e in enumerate(_RECAP):
            r, c = divmod(i, 7)
            nom = LAY[e][0]
            S(im, nom, 128, 770 + c * 172, 210 + r * 168, t, CI.lista + 0.2 + 0.05 * i, modo="pop", rot=(-6, 5, -3, 7)[i % 4],
              sem=950 + i, gris=0.4 if LISTA[e][0] == "p" else 0.0, sale=CI.coment - 0.3 + 0.004 * i)
    # comentarios
    s0 = CI.f1 - 0.25
    if CI.coment - 0.1 < t < s0 + 0.5:
        s = rebote(t, CI.coment, 0.45) * (1 - suave(pr(t, s0, s0 + 0.35)))
        pegar(im, globo(), 1230, 440, esc=s, sombra=0.25)
        if t > CI.cual and t < CI.peor - 0.1:
            pegar(im, C.texto("¿Cuál vas a poner", px=54), 1230, 380, esc=s * rebote(t, CI.cual, 0.3), sombra=0)
            pegar(im, C.texto("en tu carta?", px=54), 1230, 460, esc=s * rebote(t, CI.cual + 0.1, 0.3), sombra=0)
        if t > CI.peor - 0.1:
            pegar(im, C.texto("¿Y el PEOR regalo", px=54, col=C.ROSA_FUERTE), 1230, 380, esc=s * rebote(t, CI.peor - 0.1, 0.3), sombra=0)
            pegar(im, C.texto("que te han dado?", px=54), 1230, 460, esc=s * rebote(t, CI.peor, 0.3), sombra=0)
        S(im, "carta", 260, 1660, 760, t, CI.carta, rot=8, sem=960, sale=CI.peor - 0.1)
        S(im, "calcetines", 200, 1550, 790, t, CI.peor + 0.1, modo="pop", rot=-6, sem=961, gris=0.4, sale=s0)
        S(im, "canasta", 220, 1760, 780, t, CI.peor + 0.25, modo="pop", rot=6, sem=962, gris=0.4, sale=s0)
        S(im, "pulsera_b", 120, 860, 760, t, CI.coment + 0.3, modo="pop", sem=963, sale=s0)
    # «esas solo son algunas de las mejores y peores cosas»: dos montoncitos
    if s0 < t < CI.espero + 0.4:
        sa = CI.espero - 0.05
        for k, (n, x, y, g) in enumerate((("camara", 880, 430, 0), ("audifonos", 1090, 480, 0), ("bloqueador", 960, 660, 0),
                                          ("calcetines", 1450, 440, .4), ("canasta", 1650, 490, .4), ("tinte", 1540, 670, .4))):
            S(im, n, 210, x, y, t, CI.f1 + 0.15 * k, modo="pop", rot=(-6, 5)[k % 2], sem=980 + k, gris=g, sale=sa)
        N(im, "mejores", 970, 240, t, CI.f1 + 0.3, sa, sem=990, rosa=True, rot=-4, px=60)
        N(im, "peores", 1550, 240, t, CI.f1 + 0.6, sa, sem=991, rot=5, px=60)
    # like + suscríbete
    s1 = CI.vemos - 0.2
    if CI.f1 - 0.3 < t < s1 + 0.5:
        if t > CI.like:
            s = rebote(t, CI.like, 0.45) * (1 - suave(pr(t, s1, s1 + 0.35))) * (1 + 0.12 * bump(t, CI.like + 0.3, CI.like + 0.6))
            pegar(im, stk("pulgar", 240), 900, 380, esc=s, rot=-6, sombra=0.25)
            corazones(im, t, CI.like + 0.35, CI.like + 1.4, 900, 300, n=5, sem=970)
            if t < CI.like + 1.0:
                u = e_out(pr(t, CI.like - 0.2, CI.like + 0.25))
                pegar(im, C.cursor(80), 1200 + (930 - 1200) * u, 700 + (420 - 700) * u, esc=1 - 0.15 * bump(t, CI.like + 0.25, CI.like + 0.45),
                      ancla=(0.05, 0.05), sombra=0.2)
        N(im, "¡espero les guste!", 1220, 700, t, CI.espero, CI.soy - 0.15, sem=976, rosa=True, rot=-4, px=60)
        corazones(im, t, CI.espero, CI.espero + 1.2, 1220, 640, n=5, sem=977)
        boton_suscribe(im, t, 1440, 400, CI.like + 0.4, CI.sus, sale=s1)
        R(im, "Soy Amaya", 1220, 700, 130, t, CI.soy, sale=s1, sem=975, cada=0.05)
    # pantalla final: dos videos + listón
    if t > CI.vemos - 0.1:
        u = e_back(pr(t, CI.vemos - 0.1, CI.vemos + 0.4), 1.3)
        pegar(im, liston("¡GRACIAS POR VER!", 52), 1240, 175 - (1 - u) * 300, rot=-2, sombra=0.22)
        for k, (x, txt) in enumerate(((960, "próxima lista"), (1530, "otra lista"))):
            v = e_back(pr(t, CI.vemos + 0.1 * k, CI.vemos + 0.45 + 0.1 * k), 1.3)
            pegar(im, caja_video(txt=txt), x, 590 + (1 - v) * 700, rot=(-1.5, 1.5)[k], sombra=0.25)
        C.destellos(im, t, [(700, 300), (1800, 330), (1250, 900)], 0.9)
    im = sacudir(im, *C.temblor(t, CI.sus, 6))
    return im
FONDO_M = ("vichy_amaya", "rayas")


def item(esc, t):
    a = ANC[esc]
    mejor = a["tipo"] == "m"
    k = ORDEN.index(esc)
    im = C.fondo(FONDO_M[k % 2] if mejor else "rayas_gris", t + k * 7)
    C.esquinas(im, t, t0=-10, sem=k)
    # encabezado: MEJOR / PEOR + número
    R(im, "MEJOR" if mejor else "PEOR", 330, 150, 104, t, a["tit"], sem=100 + k)
    R(im, f"#{a['num']}", 330, 320, 190, t, a["num_t"], sem=200 + k, cada=0.08)
    # adornos de Amaya
    d1, d2 = DECOS[(2 * k) % len(DECOS)], DECOS[(2 * k + 1) % len(DECOS)]
    S(im, d1, 150, 770, 175, t, a["stk"] + 0.55, modo="pop", rot=-8 + 4 * (k % 3), sem=300 + k)
    S(im, d2, 160, 1800, 860, t, a["stk"] + 0.85, modo="pop", rot=6 - 3 * (k % 4), sem=400 + k)
    nom, alto, x, y = LAY[esc]
    P = dict(x=x, y=y, alto=alto, rot=-3 if k % 2 else 3, sx=1.0, sy=1.0, esc=1.0, bob=1.0, gris=0.0)
    if not mejor and t > a["sello_t"]:
        P["rot"] += math.sin(t * 40) * 5 * bump(t, a["sello_t"] + 0.1, a["sello_t"] + 1.0)
        P["gris"] = 0.35 * pr(t, a["sello_t"], a["sello_t"] + 0.4)
    encima = MOD[esc](im, t, a, P) if esc in MOD else None
    dibuja_sec(im, t, a, True)
    S(im, nom, P["alto"], P["x"], P["y"], t, a["stk"], rot=P["rot"], sx=P["sx"], sy=P["sy"], esc=P["esc"], bob=P["bob"],
      gris=P["gris"], sem=k, tinte=P.get("tinte"))
    dibuja_sec(im, t, a, False)
    if encima:
        encima(im)
    if mejor and t > a["stk"] + 0.6:
        C.destellos(im, t, [(P["x"] - 330, P["y"] - 250), (P["x"] + 320, P["y"] - 200), (P["x"] + 300, P["y"] + 260)], 0.9)
    # cinta con el nombre
    if t > a["stk"] + 0.3:
        u = e_out(pr(t, a["stk"] + 0.3, a["stk"] + 0.7))
        col = C.ROSA_CLARO if mejor else C.hexrgb("ddd3d8")
        pegar(im, C.cinta(a["nombre"], 54, col, C.CIRUELA, k), 1180 - (1 - u) * 1400, 955, rot=-2.5, sombra=0.18)
    C.cuelga_etiqueta(im, len(a["precio"]), 1530, 250, t, a["precio_t"])
    if a.get("credito") and t > a["credito"]:
        pegar(im, insignia(), 1130, 118, esc=rebote(t, a["credito"], 0.45), rot=-3 + math.sin(t * 1.6) * 1.5, sombra=0.25)
    for (t0, txt, nx, ny, rosa, t1) in a["notas"]:
        N(im, txt, nx, ny, t, t0, t1, sem=int(t0 * 10), rosa=rosa)
    # Amaya se asoma y reacciona al sello
    st = a["sello_t"]
    avatar(im, t, 210, 430, st - 0.5, sale=st + 2.6, si=(st + 0.15,) if mejor else (), no=() if mejor else (st + 0.15,),
           sem=k, lado=1)
    C.golpe_sello(im, "si" if mejor else "no", 560, 770, t, st, rot=-12, esc=0.72 if mejor else 0.64)
    return sacudir(im, *C.temblor(t, st))


def generica(esc, t):
    im = C.fondo("vichy_amaya", t)
    C.esquinas(im, t, t0=-10, sem=3)
    R(im, esc.upper(), 960, 540, 120, t, T0(esc) + 0.2, sem=9)
    return im


ESCENAS = {"gancho": gancho, "bienvenida": bienvenida, "suscribe": suscribe, "cierre": cierre}


def cruda(esc, t):
    if esc in ESCENAS:
        return ESCENAS[esc](t)
    if esc in ANC:
        return item(esc, t)
    return generica(esc, t)


# ------------------------------------------------------------ transiciones
D_TR = 0.55


def _trans(k):
    e = ORDEN[k]
    if e == "bienvenida" or (e in LISTA and LISTA[e][0] == "p"):
        return "tv"
    return "rasgado"


for _k in range(1, len(ORDEN)):
    _tv = _trans(_k) == "tv"
    ev(T0(ORDEN[_k]) - 0.15, "tv" if _tv else "rasgado", 0.4 if _tv else 0.5)


def cuadro(t):
    k = 0
    for i, e in enumerate(ORDEN):
        if t >= T0(e) - 0.15:
            k = i
    e = ORDEN[k]
    b = T0(e) - 0.15
    if k > 0 and t < b + D_TR:
        u = pr(t, b, b + D_TR)
        A, Bm = cruda(ORDEN[k - 1], t), cruda(e, t)
        im = C.tv(A, Bm, u, t) if _trans(k) == "tv" else C.rasgado(A, Bm, u, sem=k)
    else:
        im = cruda(e, t)
    return C.acabado(im, t)


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e: Mundo for e in ORDEN}
