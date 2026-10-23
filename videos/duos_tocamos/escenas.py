# -*- coding: utf-8 -*-
"""«Así tocamos» — Los Duos, vertical y sin narrador: plano secuencia con tiempo global (kit duos.py, copiado del anuncio).
    intro    el logo nace sobre el escenario + «¡ASÍ TOCAMOS!»
    canción  (indita, ojos, amor, teodora) tomas de sus videos reales cortadas al pulso de la canción (cortes.json), con un
             empujón de cámara en cada pulso; al empezar, rótulo con la primera frase que se canta; siempre «● EN VIVO»,
             logo chico y el ecualizador que baila con la música real
    cierre   logo, lema, WhatsApp, precio y zona"""
import json
import math

from duos import (BLANCO, CREMA, H, ORO, TINTA, TL, TOTAL, VERDE_WA, W, P, acabado, ancho, chispas, clamp, clip_borroso,
                  clip_lleno, confeti, destellos, e_back, ecualizador, emoji, escenario, golpe, logo, marca_agua, nota, notas,
                  polvo, pr, smooth, texto, texto_oro, velo)
from escena_base import Escena
import runpy

G = runpy.run_path("guion.py")
CANCION = G["CANCION"]
ESC = {e["id"]: e for e in TL["escenas"]}
T = {k: ESC[k]["t0"] for k in ESC}
CORTES = json.load(open("cortes.json", encoding="utf-8"))
SECCIONES = ["intro", "indita", "ojos", "amor", "teodora", "cierre"]
# tomas de cada canción, en orden: (video, segundo del video donde empieza la toma)
TOMAS = {
    "indita": [(1, 40.0), (4, 10.0), (1, 0.5), (4, 22.5), (1, 24.0), (1, 32.0), (4, 28.0), (1, 44.5), (2, 62.0), (1, 18.0)],
    "ojos": [(4, 12.0), (2, 63.5), (1, 36.0), (4, 46.0), (1, 4.0), (2, 23.0), (4, 30.5), (1, 47.0), (2, 66.0), (4, 17.0)],
    "amor": [(3, 31.4), (1, 11.3), (3, 22.3), (2, 22.0), (3, 35.0), (3, 0.3), (2, 44.0), (2, 52.0)],
    "teodora": [(2, 4.0), (1, 20.0), (4, 47.0), (2, 50.0), (1, 28.0), (4, 15.5), (2, 65.0), (1, 38.0), (4, 32.0)],
}


def rebote(t, t0, dur=0.42):
    u = clamp((t - t0) / dur)
    return e_back(u) if u < 1 else 1.0


def aparece(t, t0, dur=0.32):
    return clamp((t - t0) / dur)


def en_vivo(p, t, x, y, op=1.0, k=1.0):
    if op <= 0.004:
        return
    with p.pivote(x, y, k):
        lat = 0.6 + 0.4 * math.sin(t * 8)
        p.rrect(x - 120, y - 30, x + 120, y + 30, 30, (0.80, 0.08, 0.10), 0.95 * op)
        p.circ(x - 80, y, 12, BLANCO, op * (0.6 + 0.4 * lat))
        texto(p, "EN VIVO", x + 18, y + 1, 44, BLANCO, "anton", op, esp=0.10, sombra=0.0, contorno=0.0)


# ------------------------------------------------------------------ intro
def intro(p, t):
    escenario(p, t, fuerza=1.0)
    clip_borroso(p, "v3", 33.0 + t, 0.35, op=0.7)
    logo(p, W / 2, 820, 1.0, t, 0.25, 1.0, lema=False)
    destellos(p, t, 0.55, W / 2, 820, 20, 520)
    k = rebote(t, 1.25, 0.45)
    if k > 0:
        texto(p, "¡ASÍ", W / 2, 1090, 100, BLANCO, "anton", min(1, k), esp=0.06)
        texto_oro(p, "TOCAMOS!", W / 2, 1220, 150, "anton", min(1, k), esp=0.04, brillo=clamp((t - 1.5) / 1.0))
    en_vivo(p, t, W / 2, 1400, aparece(t, 1.9, 0.3), rebote(t, 1.9, 0.4))
    notas(p, t, 8, 0.8, semilla=7)


# ------------------------------------------------------------------ canciones
def toma_en(sec, t):
    cs = [T[sec]] + CORTES["cortes"][sec]
    i = max(j for j, c in enumerate(cs) if t >= c - 1e-6)
    i = min(i, len(TOMAS[sec]) - 1)
    return i, cs[i]


def cancion(p, t, sec):
    t0 = T[sec]
    i, tc = toma_en(sec, t)
    v, s0 = TOMAS[sec][i]
    s = t - tc
    pul = sum(golpe(t, b, 0.18) for b in CORTES["pulsos"][sec] if 0 <= t - b < 0.2)
    z = 1.11 - 0.06 * clamp(s / 3.5) + 0.010 * pul
    clip_lleno(p, f"v{v}", s0 + s, z=z, dx=(-1) ** i * 18 * clamp(s / 3.5))
    if i:
        p.im += 0.10 * golpe(t, tc, 0.2)
    velo(p, 1000, 1920, 0.78)
    velo(p, 0, 330, 0.55, arriba=True)
    marca_agua(p, t)
    en_vivo(p, t, W / 2, 222, 1.0, 0.8)
    notas(p, t, 5, 0.6, semilla=17 + len(sec), y_min=300, y_max=1100)
    # rótulo de la canción al empezar
    u = t - t0
    k = rebote(t, t0 + 0.35, 0.45)
    sale = smooth(clamp((u - 4.6) / 0.5))
    if k > 0 and sale < 1:
        op = min(1, k) * (1 - sale)
        n = SECCIONES.index(sec)
        texto(p, f"EN VIVO  ·  {n} DE 4", W / 2, 1255, 40, CREMA, "mont", op, esp=0.18)
        tit = CANCION[sec][2]
        px = min(96.0, 96.0 * 760 / ancho(tit, 96, esp=0.02))         # los títulos largos se achican para caber con las notas
        with p.pivote(W / 2, 1345, 0.6 + 0.4 * k):
            texto_oro(p, tit, W / 2, 1345, px, "anton", op, esp=0.02, brillo=clamp((u - 0.6) / 1.1))
            mw = ancho(tit, px, esp=0.02) / 2 + 60
            for sg in (-1, 1):
                nota(p, W / 2 + sg * mw, 1340 + math.sin(t * 4 + sg) * 6, 78, op, doble=sg > 0)
        chispas(p, t, W / 2, 1345, 760, 160, 7, fuerza=op)
    ecualizador(p, W / 2, 1540, 780, 130, t, 0.95, 1.0)
    # avance: cuatro puntos dorados, el de la canción actual encendido
    for j in range(4):
        x = W / 2 + (j - 1.5) * 38
        act = SECCIONES.index(sec) - 1 == j
        p.circ(x, 1590, 9 if act else 6, ORO if act else CREMA, 1.0 if act else 0.45)


# ------------------------------------------------------------------ cierre
def cierre(p, t):
    t0 = T["cierre"]
    escenario(p, t, fuerza=1.1)
    clip_borroso(p, "v2", 64.0 + (t - t0) * 0.6, 0.32, op=0.6)
    logo(p, W / 2, 600, 0.95, t, t0 + 0.2, 1.0, lema=True, t_lema=t0 + 0.9)
    destellos(p, t, t0 + 0.45, W / 2, 600, 20, 500)
    k = rebote(t, t0 + 1.4, 0.45)
    if k > 0:
        a = min(1, k)
        texto(p, "CONTRATACIONES", W / 2, 930, 56, CREMA, "anton", a, esp=0.2)
        with p.pivote(W / 2, 1080, k):
            p.rrect(W / 2 - 430, 985, W / 2 + 430, 1175, 50, TINTA, 0.82)
            p.rrect(W / 2 - 430, 985, W / 2 + 430, 1175, 50, None, 1.0, borde=ORO, w=4)
            p.circ(W / 2 - 350, 1080, 58, VERDE_WA, 1.0)
            emoji(p, "📞", W / 2 - 350, 1080, 60, 1.0, ang=-10)
            texto_oro(p, "449 306 5431", W / 2 + 60, 1080, 104, "anton", 1.0, esp=0.03, contorno=0.05)
    k2 = rebote(t, t0 + 2.0, 0.45)
    if k2 > 0:
        texto(p, "$1,200 POR HORA", W / 2, 1265, 80, BLANCO, "anton", min(1, k2), esp=0.06)
        texto(p, "AGUASCALIENTES Y SUS MUNICIPIOS", W / 2, 1360, 42, CREMA, "mont", aparece(t, t0 + 2.4, 0.4), esp=0.08)
    ecualizador(p, W / 2, 1530, 640, 100, t, aparece(t, t0 + 0.5, 0.5), 1.0)
    notas(p, t, 10, 0.9, semilla=91)
    confeti(p, t, t0 + 0.3, 70, 3.5, semilla=37, fuerza=0.9)
    polvo(p, t, 25, 0.6)


def _bloque(t):
    i = 0
    for j, k in enumerate(SECCIONES):
        if t >= T[k]:
            i = j
    return i


def pintar(i, t):
    p = P()
    sec = SECCIONES[i]
    if sec == "intro":
        intro(p, t)
    elif sec == "cierre":
        cierre(p, t)
    else:
        cancion(p, t, sec)
    return p.im


def cuadro(t):
    i = _bloque(t)
    tc = T[SECCIONES[i]]
    flash = 0.0
    if i > 0 and t - tc < 0.3:                          # cambio de canción: fundido corto con destello
        u = smooth((t - tc) / 0.3)
        img = pintar(i - 1, t) * (1 - u) + pintar(i, t) * u
        flash = 0.25 * (1 - abs(u - 0.5) * 2)
    else:
        img = pintar(i, t)
    sac = 0.35 * golpe(t, 0.5, 0.35) + 0.30 * golpe(t, T["cierre"] + 0.45, 0.35)
    flash += 0.10 * golpe(t, 0.45, 0.25)
    img = acabado(img, t, flash=flash, sacudida=sac)
    img *= smooth(pr(t, 0.0, 0.25))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.8, TOTAL))
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
