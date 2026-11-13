# -*- coding: utf-8 -*-
"""Cómo vuela un Falcon 9 (CRS-30) — kit LÍNEA 3D (`nucleo/linea3d.py` + `linea3d_cohetes.py`): todo el cuadro se dibuja
en función del tiempo global (`cuadro(t)`), con 11 planos encadenados por fundidos cortos. El mundo va en KM con el centro de la
Tierra en el origen; el cohete en metros × 0,001. Trayectorias ESQUEMÁTICAS (forma plausible, sin cifras de altura ni
velocidad en pantalla); los TIEMPOS de los eventos son los oficiales de NASA (ver guion.py). Costa del Cabo y laguna: OSM.
"""
import json
import math
import os
import re
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))

import linea3d_cohetes as K  # noqa: E402
from linea3d import (L3, R_T, latlon_xyz, Cam, Sitio, base_de, chorro, circulo3d, clamp, cuerpo_revolucion, curva_suave, e_inout,  # noqa: E402
                     e_out, etiqueta3d, globo, lerp, nrm, pr, rejilla_suelo, rnd, smooth, ancho_texto)
from motor import H, W  # noqa: E402

TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}
M = 0.001                                    # km por metro


# ------------------------------------------------------------------ anclas a la voz
def _norm(s):
    s = s.lower()
    for a, b in zip("áéíóúü", "aeiouu"):
        s = s.replace(a, b)
    return re.sub(r"[^a-zñ0-9]", "", s)


def ww(esc, frase, palabra, n=0, fin=False):
    obj = [_norm(x) for x in palabra.split()]
    ws = ESC[esc]["frases"][frase]["words"]
    nw = [_norm(x["w"]) for x in ws]
    hits = [ws[i + len(obj) - 1]["e"] if fin else ws[i]["s"]
            for i in range(len(ws) - len(obj) + 1) if all(nw[i + j].startswith(obj[j]) for j in range(len(obj)))]
    if len(hits) <= n:
        raise KeyError(f"[{esc}:{frase}] no está '{palabra}' en {[x['w'] for x in ws]}")
    return hits[n]


def T0(esc):
    return ESC[esc]["t0"]


# ------------------------------------------------------------------ reloj de misión (tiempo de video -> segundos de misión)
RELOJ = [
    (T0("despegue") + 0.6, -10.0), (ww("despegue", 0, "vez", fin=True), 0.0),
    (ww("maxq", 0, "max"), 58.0), (T0("meco") - 0.1, 76.0),
    (ww("meco", 0, "apagan"), 139.0), (ww("meco", 0, "separan"), 142.0),
    (ww("divide", 0, "sigue"), 149.0), (ww("regreso", 0, "da"), 150.0), (ww("regreso", 0, "vuelta", fin=True), 152.0),
    (ww("regreso", 0, "quema"), 160.0), (ww("regreso", 0, "costa", fin=True), 204.0),
    (ww("regreso", 1, "cae"), 300.0), (ww("regreso", 1, "quema"), 380.0), (ww("regreso", 1, "denso", fin=True), 400.0),
    (T0("aterrizaje") - 0.05, 420.0), (ww("aterrizaje", 0, "cincuenta"), 446.0), (ww("aterrizaje", 0, "aterriza"), 470.0),
    (T0("orbita") - 0.3, 482.0), (ww("orbita", 0, "apaga"), 515.0),
    (ww("orbita", 1, "doce"), 690.0), (ww("orbita", 1, "suelta"), 708.0), (ww("orbita", 1, "estacion"), 760.0),
    (T0("cierre"), 768.0),
]
_RT, _RM = np.array([a for a, b in RELOJ]), np.array([b for a, b in RELOJ])


def mision(t):
    return float(np.interp(t, _RT, _RM))


EVENTOS = [(58, "MAX-Q"), (139, "MECO"), (152, "REGRESO"), (380, "ENTRADA"), (470, "ATERRIZAJE"), (515, "SECO"),
           (708, "DRAGON")]

# ------------------------------------------------------------------ geografía y trayectorias (esquemáticas)
SITIO = Sitio(28.5616, -80.5774)             # SLC-40 (OSM)
LZ = (28.4858, -80.5429)                     # Landing Zone 1 (OSM)
LZ_E, LZ_N = (float(v) for v in SITIO.latlon_a_en(*LZ))
AZ = 45.0                                    # rumbo de la órbita de la EEI desde 28,5° N
SA, CA = math.sin(math.radians(AZ)), math.cos(math.radians(AZ))
P_LZ = SITIO.a_mundo(LZ_E, LZ_N, 0.0)
PIE = 2.43 * M                               # altura de la base de las toberas con las patas abiertas

ASC = curva_suave([(0, 0, 0), (10, 0, 0.25), (20, 0.05, 1.2), (30, 0.3, 3), (45, 1.3, 7), (58, 3.0, 11.5), (80, 7, 20),
                   (110, 17, 38), (139, 33, 64), (160, 50, 85), (200, 95, 120), (260, 200, 155), (330, 420, 180),
                   (420, 900, 198), (515, 1600, 210), (540, 1790, 210), (708, 3080, 211), (800, 3790, 211)], paso=0.25, suav=10)
BOO = curva_suave([(0, 0, 0), (10, 0, 0.25), (20, 0.05, 1.2), (30, 0.3, 3), (45, 1.3, 7), (58, 3.0, 11.5), (80, 7, 20),
                   (110, 17, 38), (139, 33, 64), (142, 35.5, 67), (152, 43, 76), (170, 54, 92), (204, 62, 112), (230, 60, 120),
                   (260, 53, 122), (300, 41, 112), (340, 25, 90), (380, 12, 62), (400, 7, 46), (430, 2.4, 21), (446, 0.8, 7.5),
                   (460, 0.12, 1.4), (470, 0, 0), (900, 0, 0)], paso=0.25, suav=6)


def p_asc(m):
    s, h = ASC(min(max(m, 0.0), 800.0))
    return SITIO.gran_circulo(AZ, s, h)


def p_boo(m):
    if m < 0:
        return SITIO.P.copy()
    s, h = BOO(min(m, 900.0))
    w = smooth(pr(m, 204, 466))
    e, n = s * SA + LZ_E * w, s * CA + LZ_N * w
    b = smooth(pr(m, 432, 450))              # quema de aterrizaje: caída que frena hasta tocar LZ-1 justo a T+470 s
    if b > 0:                                # (la curva suavizada dejaba el cohete a 10 m de altura y 40 m de la plataforma)
        q = max(470.0 - m, 0.0) / 24.0
        e, n, h = lerp(e, LZ_E + 0.8 * q * q * SA, b), lerp(n, LZ_N + 0.8 * q * q * CA, b), lerp(h, 7.5 * q * q, b)
    return SITIO.a_mundo(e, n, h + PIE * smooth(pr(m, 440, 470)))


def arriba(p):
    return nrm(p)


def prog_asc(m):
    if m < 4:
        return SITIO.U
    return nrm(p_asc(m + 0.5) - p_asc(m - 0.5))


def slerp(a, b, u):
    a, b = nrm(a), nrm(b)
    d = clamp(float(a @ b), -1, 1)
    om = math.acos(d)
    if om < 1e-5:
        return a
    return nrm((math.sin((1 - u) * om) * a + math.sin(u * om) * b) / math.sin(om))


def eje_boo(m):
    """Nariz de la etapa 1: prógrado -> media vuelta (nariz hacia la costa) -> cola abajo."""
    pro = prog_asc(min(m, 139))
    if m <= 149.6:
        return pro
    p = p_boo(m)
    up = arriba(p)
    dh = nrm(SA * SITIO.E + CA * SITIO.N - up * ((SA * SITIO.E + CA * SITIO.N) @ up))
    bb = nrm(-dh * 0.9 + up * 0.45)
    if m < 204:
        return slerp(pro, bb, e_inout(pr(m, 149.6, 152)))
    return slerp(bb, up, e_inout(pr(m, 204, 300)))


def motores_boo(m):
    if 0 <= m < 139:
        return list(range(9))
    if 152 <= m < 204 or 380 <= m < 400:
        return [0, 1, 5]
    if 446 <= m < 470:
        return [0]
    return []


def mvac(m):
    return 149 <= m < 515


def marco(p):
    u = arriba(p)
    e = nrm(np.cross([0, 0, 1.0], u))
    return e, np.cross(u, e), u


# ------------------------------------------------------------------ OSM: costa del Cabo y laguna
def _cargar_osm():
    def ways(ruta, filtro):
        out = []
        for e in json.load(open(os.path.join(AQUI, "datos", ruta), encoding="utf-8"))["elements"]:
            if not filtro(e):
                continue
            segs = [e["geometry"]] if "geometry" in e else [m["geometry"] for m in e.get("members", []) if m.get("geometry")]
            for g in segs:
                if len(g) >= 4:
                    out.append(np.array([[p["lat"], p["lon"]] for p in g]))
        return out
    costa = ways("osm_cabo.json", lambda e: e.get("tags", {}).get("natural") == "coastline")
    agua = ways("osm_agua.json", lambda e: True)
    agua = [g for g in agua if np.hypot(*np.ptp(g, 0)) > 0.02]          # fuera canales y trocitos (< ~2 km)
    a_xyz = lambda g: SITIO.a_mundo(*SITIO.latlon_a_en(g[:, 0], g[:, 1]), 0.0)
    return [a_xyz(g) for g in costa], [a_xyz(g) for g in agua]


COSTA_CABO, LAGUNA = _cargar_osm()


def mapa_cabo(lz, op=1.0, op_agua=0.45):
    lz.lineas(COSTA_CABO, op * 0.9, 1.2)
    lz.lineas(LAGUNA, op * op_agua, 0.9)


# ------------------------------------------------------------------ HUD
def hud_reloj(lz, m, op=1.0, arco=True):
    if op <= 0.01:
        return
    signo = "T+" if m >= 0 else "T-"
    s = int(round(abs(m))) if m < 0 else int(abs(m))
    txt = f"{signo} {s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"
    cx, cy, Rr = W / 2, 952 + 1500, 1500.0
    if arco:
        k = 0.0196

        def ang(mm):
            d = mm - m
            return math.copysign(k * abs(d) ** 0.6, d)
        A = np.linspace(-0.66, 0.66, 160)
        pts = np.stack([cx + Rr * np.sin(A), cy - Rr * np.cos(A)], 1)
        mid = len(A) // 2
        lz.l2(pts[:mid + 1], op * 0.85, 1.4)
        lz.l2(pts[mid:], op * 0.3, 1.0)
        for ie, (mm, nom) in enumerate(EVENTOS):
            a = ang(mm)
            if abs(a) > 0.64:
                continue
            x, y = cx + Rr * math.sin(a), cy - Rr * math.cos(a)
            fade = op * clamp((0.64 - abs(a)) / 0.12)
            pasado = mm <= m
            lz.c2(x, y, 6.5, fade * (1.0 if pasado else 0.5), w=1.2, lleno=pasado)
            if not pasado:
                lz.c2(x, y, 2.0, fade * 0.5, lleno=True)
            alto = 20 if ie % 2 == 0 else 44
            if ie % 2:
                lz.l2([(x, y - 9), (x, y - alto + 4)], fade * 0.35, 0.8)
            lz.texto(nom, x, y - alto, 17, "SemiBold Condensed", fade * (0.95 if pasado else 0.55), "mb", esp=0.14)
        lz.l2([(cx, cy - Rr - 12), (cx, cy - Rr + 12)], op, 1.6)
    lz.texto(txt, cx, 1016, 40, "SemiBold Condensed", op, "mm", esp=0.08, fondo=True)


def hud_motores(lz, x, y, nombre, estado, encendidos, total, op=1.0, der=False):
    if op <= 0.01:
        return
    an = "rm" if der else "lm"
    lz.texto(nombre, x, y - 46, 19, "SemiBold Condensed", op * 0.8, an, esp=0.2)
    lz.texto(estado, x, y + 46, 22, "SemiBold Condensed", op, an, esp=0.1)
    cx = x - 34 if der else x + 34
    if total == 9:
        pos = [(0, 0)] + [(math.cos(2 * math.pi * k / 8 - math.pi / 2) * 20, math.sin(2 * math.pi * k / 8 - math.pi / 2) * 20)
                          for k in range(8)]
        lz.c2(cx, y, 30, op * 0.5, w=1.0)
    else:
        pos = [(0, 0)]
        lz.c2(cx, y, 16, op * 0.5, w=1.0)
    for i, (dx, dy) in enumerate(pos):
        on = i in encendidos
        lz.c2(cx + dx, y + dy, 5.5 if total == 9 else 9, op * (1.0 if on else 0.45), w=1.0, lleno=on)


def hud_mision(lz, op):
    lz.texto("FALCON 9  ·  CRS-30", 64, 62, 30, "SemiBold Condensed", op, "lm", esp=0.16)
    lz.texto("21 MAR 2024  ·  CABO CAÑAVERAL, FLORIDA", 64, 96, 19, "Light Condensed", op * 0.85, "lm", esp=0.16)


def estado_s1(m):
    if m < 0:
        return "EN PLATAFORMA"
    if m < 139:
        return "9 MOTORES"
    if m < 152:
        return "MEDIA VUELTA" if m >= 145 else "MECO"
    if m < 204:
        return "QUEMA DE REGRESO"
    if m < 380:
        return "CAÍDA LIBRE"
    if m < 400:
        return "QUEMA DE ENTRADA"
    if m < 446:
        return "DESCENSO"
    if m < 470:
        return "QUEMA DE ATERRIZAJE"
    return "EN TIERRA · LZ-1"


def estado_s2(m):
    if m < 142:
        return "EN ESPERA"
    if m < 149:
        return "SEPARADA"
    if m < 515:
        return "MVAC ENCENDIDO"
    if m < 708:
        return "SECO · EN ÓRBITA"
    return "DRAGON LIBRE"


def hud(lz, t, op_reloj=1.0, op_mision=1.0):
    m = mision(t)
    hud_mision(lz, op_mision)
    hud_reloj(lz, m, op_reloj)
    hud_motores(lz, 64, 990, "ETAPA 1", estado_s1(m), motores_boo(m), 9, op_reloj)
    hud_motores(lz, W - 64, 990, "ETAPA 2", estado_s2(m), [0] if mvac(m) else [], 1, op_reloj, der=True)


# ------------------------------------------------------------------ piezas de escena
def cohete_pila(lz, base, eje, m, t, sep=0.0, aletas=0.0, patas=0.0, s2=True, s1=True, morro=0.0, chorro_s1=None, ref=None):
    """Pila completa o separada. sep = metros que la etapa 2 se aleja; chorro_s1 = (largo m, ancho m)."""
    ref = ref if ref is not None else SITIO.N
    a = nrm(eje)
    if s2:
        b2 = base + a * (K.Z_S2 + sep) * M
        if mvac(m) and sep > 0.5:
            chorro(lz, b2, -a, 34 * M, 1.6 * M, t * 1.3, n=55, op=0.9, semilla=9, w=0.9, abre=2.2)
        K.etapa2(lz, b2, a, M, ref=ref)
        K.dragon(lz, base + a * (K.Z_DRAGON + sep) * M, a, M, ref=ref, morro=morro)
    if s1:
        enc = motores_boo(m)
        if enc and chorro_s1:
            largo, ancho = chorro_s1
            for i, p in enumerate(K.salidas_motores(base, a, M, ref=ref, cuales=enc)):
                chorro(lz, p, -a, largo * M, ancho * M, t, n=60 if len(enc) > 3 else 45, op=0.85, semilla=i * 7, w=0.9)
        K.etapa1(lz, base, a, M, aletas=aletas, patas=patas, ref=ref)


def trayecto(lz, f, m0, m1, op=1.0, w=1.4, guion=None, n=240):
    if m1 <= m0:
        return
    P = np.array([f(x) for x in np.linspace(m0, m1, n)])
    lz.linea(P, op, w, guion=guion)


def anillo_eei(lz, op, alt=420.0):
    """Órbita de la Estación (gran círculo con el rumbo del despegue), en trazos."""
    a = math.radians(AZ)
    d = math.sin(a) * SITIO.E + math.cos(a) * SITIO.N
    s = np.linspace(0, 2 * math.pi, 400)
    P = (np.cos(s)[:, None] * SITIO.U[None] + np.sin(s)[:, None] * d[None]) * (R_T + alt)
    vis = 1.0 - oculto_tierra(lz.cam.pos, P)
    lz.linea(P, op * vis, 1.0, guion=3)
    return P


def oculto_tierra(c, P):
    """1 donde la Tierra tapa el punto visto desde c (el segmento c->P pasa por dentro de la esfera)."""
    d = P - c
    L2 = np.sum(d * d, -1)
    s = np.clip(-(d @ c) / np.maximum(L2, 1e-9), 0, 1)
    q = c + d * s[:, None]
    return ((np.linalg.norm(q, axis=-1) < R_T - 1) & (s < 0.999)).astype(float)


def pos_eei(alt=420.0, s_km=4300.0):
    return SITIO.gran_circulo(AZ, s_km, alt)


# ------------------------------------------------------------------ planos
def cam_global(az, el, dist, mira_off=(0, 0, 0)):
    c = SITIO.P * 0.0 + nrm(SITIO.P + SITIO.N * 1500 + SITIO.E * 2500) * R_T * 0.0
    d = math.cos(math.radians(el)) * (math.sin(math.radians(az)) * SITIO.E + math.cos(math.radians(az)) * SITIO.N) \
        + math.sin(math.radians(el)) * SITIO.U
    centro = SITIO.P * 0.55 + np.asarray(mira_off)
    return Cam(centro + d * dist, centro, SITIO.U, 38)


def p_gancho(t):
    t_doce, t_fal, t_est = ww("gancho", 0, "doce"), ww("gancho", 0, "falcon"), ww("gancho", 0, "estacion")
    t_y, t_casa = ww("gancho", 1, "y"), ww("gancho", 1, "casa", fin=True)
    u = e_inout(pr(t, t_y - 0.3, t_casa - 0.4))
    # cámara: lejos (sobre el Atlántico, gira despacio, globo a la derecha) -> baja en diagonal hacia Florida desde el sureste
    pos0 = latlon_xyz(31.0, -64.0 + 0.9 * t, R_T + 15000.0)
    pos1 = SITIO.a_mundo(330.0, -260.0, 160.0)
    r0, r1 = np.linalg.norm(pos0) - R_T, np.linalg.norm(pos1) - R_T
    pos = slerp(pos0, pos1, u) * (R_T + math.exp(lerp(math.log(r0), math.log(r1), u)))
    mira = SITIO.a_mundo(30 * SA, 30 * CA, 50.0) * e_inout(pr(u, 0.0, 0.5))
    uc = smooth(pr(u, 0.3, 1.0))
    cam = Cam(pos, mira, nrm(np.array([0, 0, 1.0]) * (1 - uc) + SITIO.U * uc), 40, cerca=0.5, centro=(lerp(W * 0.63, W * 0.5, uc), H * 0.52))
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, op=smooth(pr(t, 0.0, 0.8)), paso=10)
    if u > 0.3:
        mapa_cabo(lz, smooth(pr(u, 0.3, 0.8)) * 0.8)
    op_eei = smooth(pr(t, 0.5, 1.5)) * (1 - 0.6 * u)
    anillo_eei(lz, op_eei * 0.6)
    # trayectoria de ascenso hasta la separación de la Dragon
    k = e_out(pr(t, ww("gancho", 0, "minutos"), t_est + 0.3))
    if k > 0:
        mf = 708 * k
        trayecto(lz, p_asc, 0, mf, 1.0, 1.8, n=300)
        lz.puntos(p_asc(mf), 4.0, 1.0)
    if t >= t_est - 0.1:
        pe = pos_eei()
        ex, ny, uz = marco(pe)
        K.estacion(lz, pe, (ex, uz), esc=1.4, op=smooth(pr(t, t_est - 0.1, t_est + 0.4)) * (1 - u) * 0.9, w=0.8)
        etiqueta3d(lz, pe, "ESTACIÓN ESPACIAL", "ÓRBITA A ~400 KM", dx=-120, dy=-90, op=smooth(pr(t, t_est, t_est + 0.4)) * (1 - u),
                   px=26)
    if t >= t_fal - 0.1:
        etiqueta3d(lz, p_asc(300), "FALCON 9", "DESPEGA DE CABO CAÑAVERAL", dx=140, dy=110,
                   op=smooth(pr(t, t_fal, t_fal + 0.4)) * (1 - smooth(pr(t, t_y - 0.4, t_y))), px=26)
    # regreso de la etapa 1
    if t > t_y:
        kb = e_out(pr(t, ww("gancho", 1, "primera"), t_casa))
        trayecto(lz, p_boo, 139, 139 + (470 - 139) * kb, 1.0, 1.6, n=200)
        trayecto(lz, p_asc, 0, 160, 0.9, 1.4, n=120)
        etiqueta3d(lz, p_boo(250), "ETAPA 1", "VUELVE A CABO CAÑAVERAL", dx=-170, dy=-80,
                   op=smooth(pr(t, ww("gancho", 1, "vuelve"), ww("gancho", 1, "vuelve") + 0.4)), px=26)
        lz.puntos(SITIO.P, 3.5, smooth(pr(u, 0.5, 0.9)))
    # cifra grande
    op12 = smooth(pr(t, t_doce - 0.15, t_doce + 0.25)) * (1 - smooth(pr(t, t_y - 0.5, t_y)))
    if op12 > 0:
        lz.texto("12 MIN", 120, 470, 150, "Bold Condensed", op12, "lm", esp=0.04)
        lz.l2([(124, 560), (124 + 380 * e_out(pr(t, t_doce, t_doce + 0.6)), 560)], op12 * 0.8, 1.2)
        lz.texto("DEL DESPEGUE A LA SEPARACIÓN DE LA DRAGON", 124, 592, 22, "SemiBold Condensed", op12 * 0.9, "lm", esp=0.14)
    return lz


def p_despegue(t):
    t_cabo, t_crs = ww("despegue", 0, "cabo"), ww("despegue", 0, "crs")
    t_nueve, t_enc, t_vez = ww("despegue", 0, "nueve"), ww("despegue", 0, "encienden"), ww("despegue", 0, "vez", fin=True)
    m = mision(t)
    b0 = SITIO.P
    E, N, U = SITIO.E, SITIO.N, SITIO.U
    alt = 0.0 if t <= t_vez else 70 * M * (t - t_vez) ** 1.6                 # sube a escala de video, no del reloj
    base = b0 + U * alt
    u = e_inout(pr(t, T0("despegue"), T0("despegue") + 6.0))
    mira = b0 + U * lerp(0.028, 0.038, u) + U * alt * 0.8 + E * 0.004
    cp = b0 + U * lerp(0.012, 0.022, u) - N * lerp(0.155, 0.13, u) + E * lerp(-0.055, -0.028, u)
    cam = Cam(cp + U * alt * 0.5, mira, U, 40, cerca=0.001)
    lz = L3(cam)
    rejilla_suelo(lz, b0, E, N, 0.16, 0.008, op=0.22)
    lz.linea(circulo3d(b0, U, 0.022, 96), 0.35, 1.0, cerrada=True)
    lz.linea(np.array([b0 - N * 0.004, b0 - N * 0.06]), 0.35, 1.0)        # foso de llamas
    lz.linea(np.array([b0 - N * 0.004 + E * 0.006, b0 - N * 0.06 + E * 0.006]), 0.35, 1.0)
    K.torre(lz, b0 + E * 0.013, U, E, M, alto=80, op=0.6)
    # vapor / polvo al encender
    if t > t_enc:
        g = pr(t, t_enc, t_enc + 2.5)
        for i in range(70):
            ang = rnd(i, 3) * 2 * math.pi
            rr = (0.004 + 0.06 * g * (0.3 + 0.7 * rnd(i, 4)))
            d = math.cos(ang) * E + math.sin(ang) * N
            p = b0 + d * rr + U * 0.002 * rnd(i, 5)
            lz.linea(np.array([p, p + d * 0.006 * (0.5 + rnd(i, 6))]), 0.55 * (1 - g * 0.6) * rnd(i, 7), 0.8)
    plume = (lerp(14, 70, pr(t, t_enc, t_vez + 1.0)), lerp(1.5, 4.5, pr(t, t_enc, t_vez + 1.0))) if t > t_enc else None
    cohete_pila(lz, base, U, max(m, 0.1) if t > t_enc else -1, t, chorro_s1=plume)
    etiqueta3d(lz, b0 + U * 0.004 + E * 0.013, "SLC-40", "CABO CAÑAVERAL, FLORIDA", dx=160, dy=-40,
               op=smooth(pr(t, t_cabo, t_cabo + 0.4)) * (1 - smooth(pr(t, t_nueve - 0.3, t_nueve))), px=26)
    # vista inferior: 9 motores
    vi = smooth(pr(t, t_nueve - 0.15, t_nueve + 0.3)) * (1 - smooth(pr(t, t_vez - 0.05, t_vez + 0.3)))
    if vi > 0.01:
        cx, cy, rr = 1440, 500, 250 * (0.85 + 0.15 * e_out(vi))
        th = np.linspace(0, 2 * math.pi, 120)
        circ = np.stack([cx + rr * np.cos(th), cy + rr * np.sin(th)], 1)
        cv2.fillPoly(lz.b, [np.round(circ * 2 * 16).astype(np.int32)], 0, cv2.LINE_AA, shift=4)
        ci = Cam(base - U * 0.016 + E * 0.0015, base + U * 0.01, N, 34, cerca=0.0005, centro=(cx, cy))
        sub = L3(ci)
        sub.b = lz.b
        enc = [k for k in range(9) if t > t_enc + 0.05 * (k % 3)]
        for i, p in enumerate(K.salidas_motores(base, U, M, ref=N)):
            cuerpo_revolucion(sub, p, U, [(0, 0.46 * M), (1.35 * M, 0.2 * M)], anillos=[0, 0.7 * M, 1.35 * M], op=vi, w=1.4,
                              gen=6, ref=N)
            if i in enc:
                fl = 0.75 + 0.25 * math.sin(t * 40 + i * 2.1)
                sub.linea(circulo3d(p, U, 0.32 * M, 32, ref=N), vi * fl, 2.2, cerrada=True)
                for j in range(10):
                    a = 2 * math.pi * j / 10 + t * 3
                    uu, vv = base_de(U, N)
                    q = p + (math.cos(a) * uu + math.sin(a) * vv) * 0.05 * M
                    sub.linea(np.array([q, q + (math.cos(a) * uu + math.sin(a) * vv) * 0.25 * M * fl]), vi * 0.7, 1.0)
        cuerpo_revolucion(sub, base + U * 1.3 * M, U, [(0, 1.55 * M), (0.6 * M, R_CU)], anillos=[0, 0.6 * M], op=vi * 0.6, w=1.0,
                          gen=0, ref=N, rellenar=False)
        lz.l2(circ, vi * 0.9, 1.4, cerrada=True)
        lz.texto("VISTA INFERIOR", cx, cy - rr - 26, 20, "SemiBold Condensed", vi * 0.9, "mm", esp=0.2)
        lz.texto(f"{len(enc)} / 9 MERLIN", cx, cy + rr + 30, 26, "SemiBold Condensed", vi, "mm", esp=0.12)
    hud(lz, t, op_reloj=smooth(pr(t, t_cabo, t_cabo + 0.5)), op_mision=smooth(pr(t, t_crs - 0.2, t_crs + 0.3)))
    return lz


R_CU = K.R * M


def p_maxq(t):
    m = mision(t)
    t_max = ww("maxq", 0, "max")
    p = p_boo(m)
    a = prog_asc(m)
    e, n, u = marco(p)
    dh = nrm(SA * SITIO.E + CA * SITIO.N)
    side = nrm(np.cross(dh, u))
    k = pr(t, T0("maxq"), T0("meco"))
    ctr = p + a * 36 * M
    cam = Cam(ctr + side * lerp(0.17, 0.15, k) - u * 0.02 + dh * 0.03, ctr + a * 0.004, u, 40, cerca=0.0005)
    lz = L3(cam)
    trayecto(lz, p_boo, max(0, m - 40), m, 0.5, 1.2, n=120)
    # conos de choque en la nariz: se abren y brillan más cerca de Max Q
    q = math.exp(-((m - 58) / 16) ** 2)
    nose = p + a * 69.4 * M
    oq = smooth(pr(t, T0("maxq"), T0("maxq") + 0.4)) * (0.35 + 0.65 * q)
    for j in range(4):
        fase = ((t * 1.5 + j / 4) % 1.0)
        largo = (10 + 26 * fase) * M
        ancho = (2.6 + (5 + 9 * q) * fase) * M
        cuerpo_revolucion(lz, nose - a * largo, a, [(0, ancho), (largo, 0.25 * M)], anillos=[], op=oq * (1 - fase) * 1.0, w=1.4,
                          gen=0, ref=SITIO.N, rellenar=False)
    uu, vv = base_de(a, u)
    for i in range(22):                                  # aire que pasa a lo largo del cuerpo
        ang = 2 * math.pi * i / 22
        d = math.cos(ang) * uu + math.sin(ang) * vv
        if (cam.pos - p) @ d < 0:
            continue
        z = ((rnd(i, 1) - t * (1.2 + q)) % 1.0) * 80 - 10
        r0 = (2.6 + 3.0 * rnd(i, 2) + 4 * q) * M
        q0 = p + a * z * M + d * r0
        lz.linea(np.array([q0, q0 - a * (5 + 6 * rnd(i, 3)) * M]), oq * 0.6 * rnd(i, 4), 0.8)
    cohete_pila(lz, p, a, m, t, chorro_s1=(lerp(60, 110, pr(m, 40, 80)), lerp(5, 10, pr(m, 40, 80))))
    # medidor de presión dinámica (curva cualitativa)
    gx, gy, gw, gh = 1320, 300, 460, 220
    og = smooth(pr(t, t_max - 0.6, t_max - 0.1))
    if og > 0:
        lz.texto("PRESIÓN DINÁMICA", gx, gy - 24, 20, "SemiBold Condensed", og * 0.85, "lb", esp=0.2)
        lz.l2([(gx, gy), (gx, gy + gh), (gx + gw, gy + gh)], og * 0.6, 1.0)
        xs = np.linspace(0, 140, 120)
        ys = np.exp(-((xs - 58) / 26) ** 2) * (xs / 58) ** 0.5
        pts = np.stack([gx + xs / 140 * gw, gy + gh - ys / ys.max() * gh * 0.9], 1)
        hasta = int(np.clip(m / 140 * 120, 2, 120))
        lz.l2(pts[:hasta], og, 1.8)
        x58 = gx + 58 / 140 * gw
        if m >= 57:
            lz.l2([(x58, gy + gh), (x58, gy + gh * 0.1)], og * 0.5, 1.0)
            lz.c2(x58, gy + gh * 0.1, 6, og, lleno=True)
            lz.texto("MAX-Q  ·  T+ 00:00:58", x58 + 14, gy + gh * 0.1, 24, "SemiBold Condensed", og, "lm", esp=0.1)
        lz.c2(*pts[hasta - 1], 4, og, lleno=True)
    etiqueta3d(lz, nose, "MÁXIMA PRESIÓN DEL AIRE", "EL MOMENTO MÁS DURO PARA LA ESTRUCTURA", dx=-170, dy=-40,
               op=smooth(pr(t, ww("maxq", 0, "maxima"), ww("maxq", 0, "maxima") + 0.3)), px=26)
    hud(lz, t)
    return lz


def p_meco(t):
    m = mision(t)
    t_apagan, t_sep = ww("meco", 0, "apagan"), ww("meco", 0, "separan")
    p = p_boo(min(m, 142)) if m < 142 else p_boo(m)
    a = prog_asc(139) if m >= 120 else prog_asc(m)
    e, n, u = marco(p)
    side = nrm(np.cross(a, u))
    sep = 0.0 if t < t_sep else 1.2 * (t - t_sep) ** 1.6 * 9                 # metros (pistones y luego se aleja)
    k = pr(t, T0("meco"), T0("divide"))
    foco = p + a * (lerp(30, 50, smooth(pr(t, t_apagan, t_sep + 1.5)))) * M
    dist = lerp(0.12, 0.085, smooth(pr(t, t_apagan, t_sep + 1.0)))
    cam = Cam(foco + nrm(side + a * 0.25 - u * 0.25) * dist, foco, u, 40, cerca=0.0003)
    lz = L3(cam)
    pl = 1 - smooth(pr(t, t_apagan, t_apagan + 0.35))
    cohete_pila(lz, p, a, m, t, sep=sep, chorro_s1=(110 * pl, 12 * pl) if pl > 0.02 else None)
    if pl > 0.02 and m >= 139:
        for i, q in enumerate(K.salidas_motores(p, a, M, ref=SITIO.N)):
            chorro(lz, q, -a, 110 * M * pl, 12 * M * pl, t, n=40, op=0.8 * pl, semilla=i * 7, w=0.9)
    etiqueta3d(lz, p + a * 8 * M, "MECO", "APAGADO DE MOTORES · T+ 02:19", dx=-230, dy=-170,
               op=smooth(pr(t, t_apagan, t_apagan + 0.3)) * (1 - smooth(pr(t, t_sep - 0.2, t_sep + 0.2))), px=26)
    etiqueta3d(lz, p + a * (47.5 + sep * 0.5) * M, "SEPARACIÓN", "T+ 02:22", dx=170, dy=-70,
               op=smooth(pr(t, t_sep, t_sep + 0.3)), px=26)
    hud(lz, t)
    return lz


def p_divide(t):
    m = mision(t)
    t_dos, t_sig = ww("divide", 0, "dos"), ww("divide", 0, "sigue")
    k = e_inout(pr(t, T0("divide"), T0("regreso")))
    foco = SITIO.a_mundo(45 * SA, 45 * CA, 60)
    e, n, u = SITIO.E, SITIO.N, SITIO.U
    dh = SA * e + CA * n
    cam = Cam(foco - np.cross(u, dh) * lerp(260, 300, k) - dh * lerp(60, 120, k) + u * lerp(40, 90, k), foco + dh * 30 * k, u, 40,
              cerca=0.05)
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=2, op_rej=0.18, limbo=0.0)
    mapa_cabo(lz, 0.8)
    lz.puntos(SITIO.P, 3.0, 0.8)
    trayecto(lz, p_asc, 0, 139, 0.9, 1.6, n=150)
    # etapa 2 sigue
    trayecto(lz, p_asc, 139, max(m, 139.5), 1.0, 1.8, n=60)
    fut = smooth(pr(t, t_sig - 0.3, t_sig + 0.8))
    if fut > 0:
        trayecto(lz, p_asc, m, m + 180 * fut, 0.55, 1.2, guion=4, n=120)
    fb = smooth(pr(t, ww("divide", 0, "dos") - 0.1, ww("divide", 0, "dos") + 0.9))
    if fb > 0:
        trayecto(lz, p_boo, m, m + (470 - m) * fb, 0.45, 1.1, guion=4, n=160)
    lz.puntos(p_asc(m), 4.5, 1.0)
    trayecto(lz, p_boo, 139, max(m, 139.5), 1.0, 1.6, n=40)
    lz.puntos(p_boo(m), 4.5, 1.0)
    sp = smooth(pr(t, t_dos - 0.4, t_dos))
    if sp > 0:
        x, y = cam.px(p_asc(142))
        lz.c2(x, y, 10 + 30 * pr(t, t_dos, t_dos + 0.6), sp * (1 - pr(t, t_dos, t_dos + 0.6)), w=1.4)
    etiqueta3d(lz, p_asc(m), "ETAPA 2", "SIGUE HACIA LA ÓRBITA", dx=-170, dy=-90, op=smooth(pr(t, t_dos - 0.1, t_dos + 0.3)), px=26)
    etiqueta3d(lz, p_boo(m), "ETAPA 1", "VA A VOLVER", dx=170, dy=90, op=smooth(pr(t, t_dos + 0.2, t_dos + 0.6)), px=26)
    hud(lz, t)
    return lz


def p_regreso(t):
    m = mision(t)
    t_vuelta, t_quema, t_reg, t_costa = (ww("regreso", 0, "media"), ww("regreso", 0, "quema"), ww("regreso", 0, "regresar"),
                                         ww("regreso", 0, "costa", fin=True))
    p = p_boo(m)
    a = eje_boo(m)
    e, n, u = marco(p)
    dh = nrm(SA * SITIO.E + CA * SITIO.N)
    side = nrm(np.cross(dh, u))
    # cámara: cerca del cohete -> se aleja (log) y deja ver el regreso a la costa
    k = e_inout(pr(t, t_reg - 0.5, t_costa + 0.2))
    dist = math.exp(lerp(math.log(0.11), math.log(230), k))
    kf = (dist - 0.11) / (230 - 0.11)                 # al final el encuadre abarca cohete y costa (foco al ritmo de la distancia)
    foco = (p + a * 0.02 * (1 - k)) * (1 - kf) + SITIO.a_mundo(30 * SA, 30 * CA, 55) * kf
    cp = foco + (side * 0.85 + u * 0.25 + dh * 0.2) / np.linalg.norm(side * 0.85 + u * 0.25 + dh * 0.2) * dist
    cam = Cam(cp, foco, u, 40, cerca=dist * 0.002)
    lz = L3(cam)
    if k > 0.25:
        x, y = cam.px(p)
        lz.c2(x, y, 14, smooth(pr(k, 0.25, 0.45)) * 0.8, w=1.2)
    if k > 0.05:
        globo(lz, (0, 0, 0), R_T, paso=2, op_rej=0.18 * smooth(pr(k, 0.05, 0.5)), op_costa=0.75 * smooth(pr(k, 0.05, 0.5)),
              limbo=0.0)
        mapa_cabo(lz, smooth(pr(k, 0.2, 0.7)) * 0.85)
        trayecto(lz, p_asc, 0, 300, 0.45 * k, 1.2, n=200)
        trayecto(lz, p_boo, 139, m, 1.0 * k, 1.6, n=120)
        trayecto(lz, p_boo, m, 470, 0.5 * smooth(pr(k, 0.6, 1)), 1.1, guion=4, n=150)
        lz.puntos(SITIO.P, 3.5, k)
        etiqueta3d(lz, P_LZ, "CABO CAÑAVERAL", None, dx=-190, dy=-90, op=smooth(pr(t, t_costa - 0.3, t_costa + 0.1)), px=24)
    enc = motores_boo(m)
    cohete_pila(lz, p, a, m, t, s2=False, aletas=smooth(pr(m, 206, 230)), chorro_s1=(70, 7) if enc else None, ref=SITIO.N)
    if k < 0.5:
        # flechas de giro durante la media vuelta
        og = smooth(pr(t, t_vuelta - 0.2, t_vuelta + 0.1)) * (1 - smooth(pr(t, t_quema - 0.1, t_quema + 0.2)))
        if og > 0:
            c = p + a * 24 * M
            arc = circulo3d(c, np.cross(a, side) if abs(np.cross(a, side) @ side) < 2 else side, 30 * M, 50, 0.3, 2.6, ref=a)
            lz.linea(arc, og * 0.8, 1.2, guion=2)
        etiqueta3d(lz, p + a * 10 * M, "QUEMA DE REGRESO", "3 MOTORES · T+ 02:32", dx=170, dy=70,
                   op=smooth(pr(t, t_quema, t_quema + 0.3)) * (1 - k * 2), px=26)
    else:
        etiqueta3d(lz, p, "ETAPA 1", "QUEMA DE REGRESO", dx=150, dy=-60, op=smooth(pr(k, 0.6, 0.9)), px=24)
    hud(lz, t)
    return lz


def p_cae(t):
    m = mision(t)
    t_cae, t_quema, t_denso = ww("regreso", 1, "cae"), ww("regreso", 1, "quema"), ww("regreso", 1, "denso", fin=True)
    p = p_boo(m)
    a = eje_boo(m)
    e, n, u = marco(p)
    dh = nrm(SA * SITIO.E + CA * SITIO.N)
    side = nrm(np.cross(dh, u))
    k = pr(t, T0("regreso") + 4.5, T0("aterrizaje"))
    foco = p + u * 0.012
    ar = smooth(pr(t, t_quema - 0.6, t_quema + 0.4))                 # sube un poco la cámara: la capa de aire denso se ve como plano
    cam = Cam(foco + side * lerp(0.13, 0.11, k) - dh * 0.05 - u * lerp(lerp(0.035, 0.02, k), -0.035, ar), foco, u, 40,
              cerca=0.0005)
    lz = L3(cam)
    # capa de aire denso (plano a ~40 km bajo el cohete)
    capa = p - u * lerp(0.11, 0.05, smooth(pr(t, t_quema - 0.4, t_denso)))
    oc = smooth(pr(t, t_quema - 0.3, t_quema + 0.3))
    if oc > 0:
        rejilla_suelo(lz, capa, e, n, 0.35, 0.02, op=0.55 * oc, w=0.9)
        etiqueta3d(lz, capa - side * 0.12 - dh * 0.06, "AIRE DENSO", "ATMÓSFERA BAJA", dx=-150, dy=-40,
                   op=smooth(pr(t, ww("regreso", 1, "aire"), ww("regreso", 1, "aire") + 0.3)), px=24)
    # rayas de velocidad (cae)
    vel = smooth(pr(t, T0("regreso") + 4.4, t_cae + 0.3))
    for i in range(46):
        ang = rnd(i, 1) * 2 * math.pi
        rr = (6 + 40 * rnd(i, 2)) * M
        d = math.cos(ang) * e + math.sin(ang) * n
        z = ((rnd(i, 3) + t * 1.4) % 1.0) * 140 - 40
        q = p + d * rr + u * z * M
        lz.linea(np.array([q, q + u * (8 + 10 * rnd(i, 4)) * M]), vel * 0.35 * rnd(i, 5), 0.8)
    enc = motores_boo(m)
    cohete_pila(lz, p, a, m, t, s2=False, aletas=1.0, chorro_s1=(lerp(35, 55, oc), 6) if enc else None)
    etiqueta3d(lz, p + a * 5 * M, "CAE DE COLA", "MOTORES POR DELANTE", dx=170, dy=60,
               op=smooth(pr(t, t_cae, t_cae + 0.3)) * (1 - smooth(pr(t, t_quema - 0.3, t_quema))), px=26)
    etiqueta3d(lz, p - a * 4 * M, "QUEMA DE ENTRADA", "T+ 06:20 · FRENA LA CAÍDA", dx=170, dy=40,
               op=smooth(pr(t, t_quema, t_quema + 0.3)) * (1 - smooth(pr(t, t_denso + 0.4, t_denso + 0.8))), px=26)
    etiqueta3d(lz, p + a * 46 * M, "ALETAS DE REJILLA", None, dx=-150, dy=-50,
               op=smooth(pr(t, t_cae + 0.5, t_cae + 0.8)) * (1 - smooth(pr(t, t_quema - 0.3, t_quema))), px=22)
    hud(lz, t)
    return lz


def p_aterrizaje(t):
    m = mision(t)
    t_aterr, t_nueve, t_desp = ww("aterrizaje", 0, "aterriza"), ww("aterrizaje", 0, "nueve"), ww("aterrizaje", 0, "despego", fin=True)
    p = p_boo(m)
    a = eje_boo(m)
    E, N, U = SITIO.E, SITIO.N, SITIO.U
    # cámara: junto a la plataforma -> sube y se aleja para ver el Cabo
    k = e_inout(pr(t, t_aterr + 0.8, t_nueve + 0.6))
    dist = math.exp(lerp(math.log(0.12), math.log(23.0), k))
    medio = (SITIO.P + P_LZ) / 2
    kf = (dist - 0.12) / (23.0 - 0.12)                                  # el foco se mueve al ritmo de la distancia (si no, la
    foco = (p + U * 0.019) * (1 - kf) + (medio - N * 1.0) * kf         # plataforma se sale del cuadro a media subida)
    el_d = lerp(30, 9, smooth(pr(m, 452, 471)))                         # desde arriba (se ve el suelo subir) -> a ras de suelo
    az, el = math.radians(lerp(75 - 15 * smooth(pr(m, 420, 470)), 160, k)), math.radians(lerp(el_d, 52, k))   # desde el mar: detrás, la costa
    d = math.cos(el) * (math.sin(az) * E + math.cos(az) * N) + math.sin(el) * U
    cam = Cam(foco + d * dist, foco, U, 40, cerca=dist * 0.002)
    lz = L3(cam)
    rejilla_suelo(lz, P_LZ, E, N, lerp(0.2, 14, k), lerp(0.01, 1.0, k), op=0.2)
    og = 1 - smooth(pr(m, 462, 471))                                   # rejilla grande: el suelo sube mientras cae
    if og > 0:
        rejilla_suelo(lz, P_LZ, E, N, 6.0, 0.3, op=0.22 * og, w=0.8)
    mapa_cabo(lz, lerp(0.6, 1.0, k))
    K.zona_aterrizaje(lz, P_LZ, U, M, op=0.85)
    if k > 0.2:
        # SLC-40 y la distancia
        ok = smooth(pr(k, 0.2, 0.6))
        lz.linea(circulo3d(SITIO.P, U, 0.15, 64), ok * 0.8, 1.2, cerrada=True)
        lz.puntos(SITIO.P, 3.0, ok)
        trayecto(lz, p_asc, 0, 40, ok * 0.6, 1.2, n=80)
        etiqueta3d(lz, SITIO.P, "SLC-40", "DESPEGUE", dx=160, dy=-60, op=ok, px=26)
        etiqueta3d(lz, P_LZ, "LZ-1", "ATERRIZAJE", dx=-160, dy=60, op=ok, px=26)
        od = smooth(pr(t, t_nueve - 0.2, t_nueve + 0.4))
        if od > 0:
            uu = e_out(pr(t, t_nueve - 0.2, t_nueve + 0.6))
            A, B = SITIO.P + U * 0.3, P_LZ + U * 0.3
            lz.linea(np.array([A, A + (B - A) * uu]), od, 1.6)
            for q in (A, B):
                lz.linea(np.array([q - U * 0.3, q + U * 0.3]), od * 0.7, 1.0)
            x, y = cam.px((A + B) / 2)
            lz.texto("9 KM", x + 26, y, 44, "Bold Condensed", od, "lm", esp=0.06, fondo=True)
    # rayas de velocidad mientras cae
    vel = 1 - smooth(pr(m, 452, 466))
    if vel > 0 and k <= 0:
        e_, n_ = marco(p)[:2]
        for i in range(40):
            ang = rnd(i, 1) * 2 * math.pi
            rr = (8 + 45 * rnd(i, 2)) * M
            dd_ = math.cos(ang) * e_ + math.sin(ang) * n_
            z = 100 - ((rnd(i, 3) + t * 1.6) % 1.0) * 150
            q = p + dd_ * rr + U * z * M
            lz.linea(np.array([q, q + U * (8 + 12 * rnd(i, 4)) * M]), vel * 0.35 * rnd(i, 5), 0.8)
    enc = motores_boo(m)
    pat = smooth(pr(m, 459, 466))
    cohete_pila(lz, p, a, m, t, s2=False, aletas=1.0, patas=pat, chorro_s1=(lerp(40, 14, pr(m, 446, 470)), 3.5) if enc else None)
    # polvo al tocar
    if t > t_aterr:
        g = pr(t, t_aterr, t_aterr + 1.8)
        for i in range(60):
            ang = rnd(i, 8) * 2 * math.pi
            d = math.cos(ang) * E + math.sin(ang) * N
            r0 = (6 + 55 * g * (0.4 + 0.6 * rnd(i, 9))) * M
            q = P_LZ + d * r0 + U * 0.6 * M * rnd(i, 10)
            lz.linea(np.array([q, q + d * 5 * M]), 0.6 * (1 - g) * rnd(i, 11), 0.8)
    etiqueta3d(lz, p + a * 3 * M, "QUEMA DE ATERRIZAJE", "1 MOTOR · PATAS ABIERTAS", dx=170, dy=60,
               op=smooth(pr(t, ww("aterrizaje", 0, "cincuenta") - 0.1, ww("aterrizaje", 0, "cincuenta") + 0.2))
               * (1 - smooth(pr(t, t_aterr - 0.2, t_aterr + 0.1))),
               px=26)
    etiqueta3d(lz, p + a * 40 * M, "EN TIERRA", "T+ 00:07:50", dx=150, dy=-60,
               op=smooth(pr(t, t_aterr, t_aterr + 0.3)) * (1 - smooth(pr(k, 0.15, 0.3))), px=28)
    hud(lz, t)
    return lz


def p_orbita(t):
    m = mision(t)
    t_apaga, t_suelta, t_est = ww("orbita", 0, "apaga"), ww("orbita", 1, "suelta"), ww("orbita", 1, "estacion")
    p = p_asc(min(m, 540)) if m < 540 else p_asc(540)
    a = prog_asc(540)
    e, n, u = marco(p)
    side = nrm(np.cross(a, u))
    sep = 0.0 if t < t_suelta else 14 * (1 - math.exp(-(t - t_suelta) * 1.4)) + 2.5 * (t - t_suelta)
    k = e_inout(pr(t, t_suelta + 0.3, T0("cierre")))
    PE = p + a * 0.16 + u * 0.012 - side * 0.03                     # Estación (esquemática: más cerca de lo real para que quepa)
    foco = (p + a * (10 + sep * 0.5) * M) * (1 - k) + ((p + a * (K.Z_DRAGON - K.Z_S2 + sep) * M + PE) / 2) * k
    dist = lerp(0.075, 0.2, k)
    gi = 0.5 * pr(t, T0("orbita"), T0("cierre"))                     # giro lento alrededor de la pila
    cp = foco + nrm(side * 0.9 - a * (0.15 + gi) + u * (0.22 - 0.08 * k)) * dist
    cam = Cam(cp, foco, u, 40, cerca=0.0005)
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=5, op_rej=0.2, op_costa=0.8, limbo=0.9)
    # Estación (esquemática, por delante en la órbita)
    oi = smooth(pr(t, t_est - 0.6, t_est - 0.1))
    if oi > 0:
        pe = PE
        lz.linea(np.array([p + a * (K.Z_DRAGON - K.Z_S2 + sep + 8) * M, pe]), oi * 0.45, 1.0, guion=3)
        K.estacion(lz, pe, (side, a), M, op=oi * 0.95, w=0.9)
        etiqueta3d(lz, pe, "ESTACIÓN ESPACIAL", "LLEGADA PREVISTA: 23 MAR 2024", dx=-190, dy=-90, op=oi, px=26)
    # etapa 2 + Dragon
    base2 = p
    if 149 <= m < 515 or (t < t_apaga + 0.35):
        pl = 1 - smooth(pr(t, t_apaga, t_apaga + 0.35))
        if pl > 0.02:
            chorro(lz, base2, -a, 40 * M * pl, 2.2 * M * pl, t * 1.3, n=60, op=0.9 * pl, semilla=9, w=0.9, abre=2.6)
    K.etapa2(lz, base2, a, M, ref=u)
    K.dragon(lz, base2 + a * (K.Z_DRAGON - K.Z_S2 + sep) * M, a, M, ref=u, morro=smooth(pr(m, 760, 775)))
    etiqueta3d(lz, base2 + a * 2 * M, "SECO", "T+ 00:08:35 · ÓRBITA", dx=-170, dy=-80,
               op=smooth(pr(t, t_apaga, t_apaga + 0.3)) * (1 - smooth(pr(t, t_suelta - 0.6, t_suelta - 0.2))), px=26)
    etiqueta3d(lz, base2 + a * (K.Z_DRAGON - K.Z_S2 + sep + 6) * M, "DRAGON SE SEPARA", "T+ 00:11:48", dx=170, dy=-70,
               op=smooth(pr(t, t_suelta, t_suelta + 0.3)) * (1 - smooth(pr(t, t_est - 0.9, t_est - 0.5))), px=26)
    hud(lz, t, op_reloj=1 - smooth(pr(t, T0("cierre") - 0.4, T0("cierre"))))
    return lz


VUELOS = [("AXIOM-2", "MAY 2023"), ("EUCLID", "JUL 2023"), ("STARLINK 6-11", "AGO 2023"), ("STARLINK 6-24", "OCT 2023"),
          ("AXIOM-3", "ENE 2024")]


def p_cierre(t):
    t_prop, t_cinco, t_reu = ww("cierre", 0, "propulsor"), ww("cierre", 0, "cinco"), ww("cierre", 0, "reutilizan")
    t_sus = ww("cierre", 1, "suscribete")
    E, N, U = SITIO.E, SITIO.N, SITIO.U
    base = P_LZ + U * PIE
    k = e_inout(pr(t, t_sus - 0.5, t_sus + 1.6))
    if k < 1:
        az = math.radians(200 + 24 * pr(t, T0("cierre"), t_sus))
        el = math.radians(8)
        d = math.cos(el) * (math.sin(az) * E + math.cos(az) * N) + math.sin(el) * U
        foco0 = base + U * 0.03
        d0 = d
    C0, C1 = (W * 0.32, H / 2), (W / 2, H / 2 - 110)
    az1, el1, D1 = math.radians(205), math.radians(68), 24000.0
    d1 = math.cos(el1) * (math.sin(az1) * E + math.cos(az1) * N) + math.sin(el1) * U
    G = SITIO.P * 0.7
    if k <= 0:
        cam = Cam(foco0 + d0 * 0.13, foco0, U, 40, cerca=0.0005, centro=C0)
    else:                                              # viaje logarítmico de la plataforma al globo
        if k >= 1:
            d0 = d1
        else:
            az0 = math.radians(200 + 24)
            d0 = math.cos(math.radians(8)) * (math.sin(az0) * E + math.cos(az0) * N) + math.sin(math.radians(8)) * U
        dist = math.exp(lerp(math.log(0.13), math.log(D1), k))
        kf = (dist - 0.13) / (D1 - 0.13)               # el foco viaja al ritmo de la distancia: nunca bajo tierra
        foco = (base + U * 0.03) * (1 - kf) + G * kf
        dd = nrm(lerp(d0, d1, smooth(k)))
        cc = (lerp(C0[0], C1[0], smooth(k)), lerp(C0[1], C1[1], smooth(k)))
        cam = Cam(foco + dd * dist, foco, U, 40 if k < 1 else 40, cerca=dist * 0.002, centro=cc)
    lz = L3(cam)
    if k > 0.2:
        globo(lz, (0, 0, 0), R_T, op=smooth(pr(k, 0.35, 0.7)), paso=10)
        trayecto(lz, p_asc, 0, 760, smooth(pr(k, 0.4, 0.8)), 1.8, n=300)
        anillo_eei(lz, smooth(pr(k, 0.5, 0.9)) * 0.5)
    rejilla_suelo(lz, P_LZ, E, N, 0.25, 0.01, op=0.22 * (1 - k))
    mapa_cabo(lz, 0.35 + 0.4 * k)
    K.zona_aterrizaje(lz, P_LZ, U, M, op=0.85)
    K.etapa1(lz, base, U, M, aletas=1.0, patas=1.0, ref=N)
    ol = 1 - smooth(pr(t, t_sus - 0.6, t_sus - 0.1))
    etiqueta3d(lz, base + U * 47 * M, "B1080", "PROPULSOR REUTILIZADO", dx=-170, dy=-40,
               op=smooth(pr(t, t_prop, t_prop + 0.3)) * ol, px=30)
    # historial de vuelos
    x0, y0 = 1250, 300
    oh = smooth(pr(t, t_cinco - 0.3, t_cinco)) * ol
    if oh > 0:
        lz.texto("VUELOS DE ESTE PROPULSOR", x0, y0 - 50, 22, "SemiBold Condensed", oh * 0.85, "lm", esp=0.2)
        lz.l2([(x0, y0 - 30), (x0 + 480, y0 - 30)], oh * 0.6, 1.0)
        for i, (nom, fecha) in enumerate(VUELOS + [("CRS-30", "MAR 2024")]):
            ti = t_cinco - 0.1 + i * 0.14
            oi = smooth(pr(t, ti, ti + 0.2)) * ol
            y = y0 + i * 52
            ult = i == 5
            lz.texto(f"{i + 1}", x0, y, 26, "Bold Condensed", oi * (1 if ult else 0.6), "lm")
            lz.texto(nom, x0 + 46, y, 30 if ult else 26, "SemiBold Condensed", oi * (1 if ult else 0.85), "lm", esp=0.1)
            lz.texto(fecha, x0 + 480, y, 22, "Light Condensed", oi * 0.8, "rm", esp=0.12)
            if ult:
                lz.l2([(x0 - 14, y - 22), (x0 - 14, y + 22)], oi, 2.0)
    # bucle de reutilización
    orr = smooth(pr(t, t_reu - 0.2, t_reu + 0.2)) * ol
    if orr > 0:
        c = base + U * 24 * M
        for j in range(3):
            a0 = t * 2.2 + j * 2 * math.pi / 3
            arc = circulo3d(c, U, 16 * M, 30, a0, a0 + 1.6, ref=N)
            lz.linea(arc, orr, 1.6)
            tip, prev = arc[-1], arc[-3]
            dd = nrm(tip - prev)
            rad = nrm(tip - c)
            lz.linea(np.array([tip - dd * 2.4 * M + rad * 1.4 * M, tip, tip - dd * 2.4 * M - rad * 1.4 * M]), orr, 1.6)
        lz.texto("SE REUTILIZAN", 1250, 680, 40, "Bold Condensed", orr, "lm", esp=0.08)
    # suscripción
    os_ = smooth(pr(t, t_sus, t_sus + 0.4)) * (1 - smooth(pr(t, TOTAL - 0.6, TOTAL - 0.1)))
    if os_ > 0:
        cx, cy = W / 2, 905
        tw = ancho_texto("SUSCRÍBETE", 40, "Bold Condensed", 0.12)
        x0b, x1b = cx - tw / 2 - 70, cx + tw / 2 + 30
        lz.r2(x0b, cy - 38, x1b, cy + 38, 0.0)
        lz.l2([(x0b, cy - 38), (x1b, cy - 38), (x1b, cy + 38), (x0b, cy + 38)], os_, 1.6, cerrada=True)
        bx = x0b + 36
        th = np.linspace(math.pi, 2 * math.pi, 20)
        campana = [(bx - 11, cy + 10)] + [(bx + 11 * math.cos(a), cy - 2 + 13 * math.sin(a)) for a in th] + [(bx + 11, cy + 10)]
        lz.l2(campana + [(bx - 11, cy + 10)], os_, 1.4)
        lz.c2(bx, cy + 14, 3, os_, lleno=True)
        lz.texto("SUSCRÍBETE", bx + 28, cy, 40, "Bold Condensed", os_, "lm", esp=0.12)
        lz.texto("EL PRÓXIMO LANZAMIENTO, EXPLICADO", cx, cy + 66, 22, "SemiBold Condensed", os_ * 0.85, "mm", esp=0.18)
    hud_mision(lz, ol)
    return lz


# ------------------------------------------------------------------ montaje
PLANOS = [
    (0.0, p_gancho), (T0("despegue"), p_despegue), (T0("maxq"), p_maxq), (T0("meco"), p_meco), (T0("divide"), p_divide),
    (T0("regreso"), p_regreso), (ww("regreso", 1, "cae") - 0.25, p_cae), (T0("aterrizaje"), p_aterrizaje),
    (T0("orbita"), p_orbita), (T0("cierre"), p_cierre),
]
FUNDIDO = 0.3


def cuadro(t):
    idx = max(i for i, (t0, _) in enumerate(PLANOS) if t >= t0 or i == 0)
    img = PLANOS[idx][1](t).final(t)
    if idx > 0 and t < PLANOS[idx][0] + FUNDIDO:          # fundido con el plano anterior
        u = smooth(pr(t, PLANOS[idx][0], PLANOS[idx][0] + FUNDIDO))
        prev = PLANOS[idx - 1][1](t).final(t)
        img = prev * (1 - u) + img * u
    img *= smooth(pr(t, 0.0, 0.5))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.5, TOTAL - 0.02))
    return img.astype(np.float32)


def eventos_sfx():
    """(t, nombre, vol, pan, dur) de todo el video: lanzamiento con rugido, cortes, encendidos, estampido y pitidos del HUD."""
    v = []
    v += [(ww("gancho", 0, "doce"), "hud", 0.5, -0.3, None), (ww("gancho", 0, "falcon"), "hud", 0.45, 0.2, None),
          (ww("gancho", 0, "estacion"), "hud", 0.45, 0.3, None), (ww("gancho", 1, "primera"), "whoosh", 0.5, 0.0, None)]
    v += [(T0("despegue") + 0.6, "hud", 0.5, 0.0, None), (ww("despegue", 0, "nueve"), "ignicion", 0.85, 0.0, 4.0),
          (ww("despegue", 0, "vez", fin=True) - 0.2, "despegue", 1.0, 0.0, 5.0)]
    v += [(ww("maxq", 0, "max") - 0.3, "viento", 0.8, 0.0, 3.0), (ww("maxq", 0, "max") + 0.1, "hud", 0.45, 0.4, None)]
    v += [(ww("meco", 0, "apagan"), "corte", 0.85, 0.0, 1.5), (ww("meco", 0, "separan"), "separacion", 0.9, 0.0, 1.5),
          (ww("divide", 0, "sigue"), "encendido", 0.55, 0.3, 2.0), (ww("divide", 0, "dos"), "hud", 0.45, -0.3, None)]
    v += [(ww("regreso", 0, "media"), "rcs", 0.7, -0.2, 1.2), (ww("regreso", 0, "quema"), "encendido", 0.8, 0.0, 1.8),
          (ww("regreso", 0, "regresar") - 0.3, "whoosh", 0.6, 0.0, None), (ww("regreso", 0, "costa"), "hud", 0.45, -0.3, None),
          (ww("regreso", 1, "cae") - 0.2, "caida", 0.75, 0.0, 2.5), (ww("regreso", 1, "quema"), "encendido", 0.85, 0.0, 1.6),
          (ww("regreso", 1, "aire"), "hud", 0.4, -0.3, None)]
    t_at = ww("aterrizaje", 0, "aterriza")
    v += [(ww("aterrizaje", 0, "cincuenta"), "encendido", 0.85, 0.0, 1.6), (t_at - 0.75, "estampido", 0.8, 0.0, None),
          (t_at, "toque", 0.95, 0.0, None), (ww("aterrizaje", 0, "nueve"), "hud", 0.5, 0.2, None),
          (ww("aterrizaje", 0, "despego"), "hud", 0.4, -0.2, None)]
    v += [(ww("orbita", 0, "apaga"), "apagado", 0.7, 0.0, None), (ww("orbita", 0, "apaga") + 0.3, "hud", 0.45, -0.3, None),
          (ww("orbita", 1, "suelta"), "suelta", 0.8, 0.2, None), (ww("orbita", 1, "estacion") - 0.5, "hud", 0.45, 0.4, None)]
    t_c = ww("cierre", 0, "cinco")
    v += [(ww("cierre", 0, "propulsor"), "hud", 0.5, -0.3, None)]
    v += [(t_c - 0.1 + i * 0.14, "tic", 0.4, 0.4, None) for i in range(6)]
    v += [(ww("cierre", 0, "reutilizan") - 0.2, "whoosh", 0.5, 0.2, None),
          (ww("cierre", 1, "suscribete") - 0.5, "whoosh", 0.6, 0.0, None), (ww("cierre", 1, "suscribete"), "campana", 0.6, 0.0, None)]
    return sorted(v)


try:
    from escena_base import Escena  # noqa: E402

    class Mundo(Escena):
        def preparar(self):
            for t, nom, vol, pan, dur in eventos_sfx():
                if self.t0 <= t < self.t1 or (self.idx == 0 and t < self.t0):
                    kw = {"dur": dur} if dur else {}
                    self.ev(t, nom, vol, pan, **kw)

        def render(self, lz, t):
            return cuadro(t)

    CLASES = {e["id"]: Mundo for e in TL["escenas"]}
except Exception:                                    # fuera del motor (hojas de prueba)
    CLASES = {}
