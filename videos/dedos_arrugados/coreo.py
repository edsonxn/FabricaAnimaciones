# -*- coding: utf-8 -*-
"""¿Por qué se arrugan los dedos en el agua?: gancho, falso, vasos, neumatico, prueba, cierre."""
import math

import cv2
import numpy as np

import sh_kit as K
import sh_props as X
import sh_pintura as P
from sh_motor import FIN, INI, T, escena
from sh_util import balistica, bump, estela, kf, pulso
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY
CREMA = (255, 250, 232)
AZUL_T = (70, 130, 240)
ROSA_T = (255, 130, 150)
ORO = (255, 230, 120)


def capas_agua(seed=3, c0=(70, 190, 230), c1=(24, 100, 170)):
    far = P.fondo_liso(seed, c0, c1, [(520, 0.7, (110, 214, 240), .5), (300, 1.2, (50, 150, 210), .45), (220, 1.6, (180, 240, 255), .3)])
    return [(far, 0.3)]


def capas_lab(seed=7):
    far = P.fondo_liso(seed, (252, 226, 170), (236, 190, 130), [(520, 0.7, (255, 238, 190), .5), (300, 1.2, (240, 180, 120), .4)])
    mesa = P.vacio()
    import cv2 as _c
    _c.rectangle(mesa, (0, BH - 700), (BW, BH), (176, 120, 80, 255), -1)
    _c.rectangle(mesa, (0, BH - 712), (BW, BH - 684), (214, 160, 110, 255), -1)
    for k in range(6):
        _c.line(mesa, (0, BH - 640 + k * 100), (BW, BH - 640 + k * 100), (146, 98, 66, 255), 4)
    P.textura(mesa, 0.02, 0.04)
    return [(far, 0.25), (mesa, 0.8)]


def capas_rio(seed=9):
    far = P.fondo_liso(seed, (190, 226, 170), (120, 180, 140), [(520, 0.7, (214, 240, 190), .5), (300, 1.2, (96, 160, 120), .4)])
    rio = P.vacio()
    P.mancha(rio, BW / 2, BH - 360, 1100, 380, (80, 170, 220), seed + 1, rough=0.05)
    P.mancha(rio, BW / 2, BH - 300, 900, 220, (110, 200, 240), seed + 2, rough=0.05)
    P.mancha(rio, 140, BH - 90, 300, 150, (130, 124, 140), seed + 3, rough=0.08)
    P.mancha(rio, BW - 120, BH - 120, 340, 170, (146, 140, 156), seed + 4, rough=0.08)
    P.textura(rio, 0.02, 0.04)
    return [(far, 0.25), (rio, 1.0)]


def cam_suave(C, t, a, b, z=0.05):
    u = (t - a) / max(1e-6, b - a)
    C.cam = (1.0 + z * u, 8 * math.sin(t * 0.7), -10 * math.cos(t * 0.5))


def agua_sobre(out, nivel, t, a=0.5, col=(60, 140, 230)):
    xs = np.linspace(-40, W + 40, 30)
    top = nivel + 16 * np.sin(xs / 90 + t * 2.2) + 7 * np.sin(xs / 37 - t * 3.1)
    poly = np.vstack([np.stack([xs, top], 1), [(W + 40, H + 40), (-40, H + 40)]])
    P.poligono(out, poly, col, a)
    P.poligono(out, np.vstack([np.stack([xs, top], 1), np.stack([xs[::-1], top[::-1] + 14], 1)]), (200, 240, 255), min(0.9, a + 0.2))


# ------------------------------------------------------------------ 1. gancho
@escena("gancho")
def gancho(C, t):
    t0 = INI("gancho")
    t_arr = T("gancho", "arrugan")
    t_emp = T("gancho", "empapen")
    capas = C.capas_de("agua", capas_agua)
    cam_suave(C, t, t0, FIN("gancho"))
    img = C.base("gancho", capas)
    for i in range(18):                               # burbujas
        ph = ((t - t0) * 0.35 + i / 18) % 1.0
        cv2.circle(img, (int((70 + (i * 173) % 940) * 4), int((H - ph * (H + 100)) * 4)), int((10 + (i % 4) * 8) * 4), (220, 246, 255), 4, cv2.LINE_AA, 2)
    C.fondo(img)
    ar = 0 if t < t_arr else (1 if t < t_arr + 1.0 else 2)
    bajada = 1 - e_out(prog(t, t0, t0 + 0.7))
    C.pon(X.mano(ar, "grandes" if t < t_emp else "miedo", "o" if t < t_emp else "grito"), 540, 780 - 360 * bajada, 2.6, 0.04 * math.sin(t * 2), vida=1.0)
    out = C.fin()
    agua_sobre(out, lerp(1500, 1010, e_out(prog(t, t0 + 0.2, t0 + 0.9))), t, 0.5)
    return out


# ------------------------------------------------------------------ 2. falso
@escena("falso")
def falso(C, t):
    t0 = INI("falso")
    t_abs, t_pie = T("falso", "absorber"), T("falso", "piel")
    t_no, t_sis = T("falso", "pero", frase=1), T("falso", "sistema", frase=1)
    capas = C.capas_de("lab2", capas_lab)
    cam_suave(C, t, t0, FIN("falso"))
    img = C.base("falso", capas)
    C.fondo(img)
    # frase 1: el agua resbala por la piel
    C.pon(X.mano(0, "grandes", "sonrisa"), 540, 1250, 2.2, 0.0, t_in=t0 + 0.1, vida=0.8)
    if t < t_no:
        for i in range(8):
            ph = ((t - t0) * 0.9 + i / 8) % 1.0
            gx = 250 + (i * 83) % 560
            C.pon(X.gotita("", "", 1.0), gx + 40 * ph * (1 if i % 2 else -1), 560 + 700 * ph, 0.8 + 0.2 * (i % 3), 0.0)
        C.pon(X.tache(70), 800, 700, 2.0, 0.0, t_in=t_abs + 0.2, modo="pop", dur=0.3)
        C.rot("¿ABSORBER AGUA?", 540, 300, 96, -0.03, CREMA, t_in=t_abs, dur=0.3, tira=True)
        C.rot("NO", 540, 450, 190, 0.03, (255, 100, 100), t_in=t_pie, dur=0.3)
    # frase 2: el cerebro manda la orden por los nervios
    if t >= t_no - 0.2:
        C.pon(X.cerebro("grandes", "sonrisa"), 540, 520, 2.1, 0.03 * math.sin(t * 3), t_in=t_no, dur=0.4, vida=1.0)
        C.rot("SISTEMA NERVIOSO", 540, 1700, 92, -0.02, (255, 236, 120), t_in=t_sis, dur=0.3, tira=True)
        out_early = None
    out = C.fin()
    if t >= t_no - 0.2:
        u = ((t - t_no) * 0.9) % 1.0
        pts = np.array([(540 + 130 * math.sin(y / 60.0), y) for y in np.linspace(700, 1130, 18)])
        cv2.polylines(out, [np.rint(pts * 4).astype(np.int32).reshape(-1, 1, 2)], False, (255, 236, 90), 9, cv2.LINE_AA, 2)
        p = pts[int(u * 17)]
        P.halo(out, p[0], p[1], 60, (255, 250, 200), 0.9, 4)
    return out


# ------------------------------------------------------------------ 3. vasos
def dedo_corte(img, cx, cy, k, t):
    """Corte de la yema (pintado a guache): la piel se pliega y los vasos sanguíneos se estrechan con k (0..1)."""
    w = 290
    xs = np.linspace(-w, w, 80)
    dome = 230 * np.sqrt(np.clip(1 - (xs / w) ** 2, 0, 1)) ** 0.8
    top = cy - 120 - dome + 26 * k * np.sin(xs / 24.0 + t * 0.6) * np.minimum(1, (w - np.abs(xs)) / 60) + 8 * np.sin(xs / 7.0) * k
    arc = cy - 200 - 150 * np.sqrt(np.clip(1 - (xs / w) ** 2, 0, 1)) * 0.0
    poly = np.vstack([np.stack([cx + xs, top], 1), [(cx + w, cy + 380), (cx - w, cy + 380)]])
    P.poligono(img, poly, (232, 170, 130), 1.0)
    inner = np.vstack([np.stack([cx + xs * 0.9, top + 34 + 0.1 * dome], 1), [(cx + w * 0.9, cy + 380), (cx - w * 0.9, cy + 380)]])
    P.poligono(img, inner, (246, 196, 160), 1.0)
    grosor = int(34 * (1 - 0.7 * k)) + 4
    for x0 in (-120, 20, 140):
        pts = np.array([(cx + x0 + 26 * math.sin(y / 50 + x0), y) for y in np.linspace(cy - 60, cy + 360, 14)])
        cv2.polylines(img, [np.rint(pts * 4).astype(np.int32).reshape(-1, 1, 2)], False, (206, 50, 60), grosor, cv2.LINE_AA, 2)
        cv2.polylines(img, [np.rint(pts * 4).astype(np.int32).reshape(-1, 1, 2)], False, (240, 100, 110), max(2, grosor // 3), cv2.LINE_AA, 2)


@escena("vasos")
def vasos(C, t):
    t0 = INI("vasos")
    t_min, t_vas = T("vasos", "minutos"), T("vasos", "vasos")
    t_con, t_pli = T("vasos", "contraigan"), T("vasos", "pliega")
    capas = C.capas_de("agua2", lambda: capas_agua(15, (150, 120, 200), (70, 60, 140)))
    cam_suave(C, t, t0, FIN("vasos"))
    img = C.base("vasos", capas)
    k = e_inout(prog(t, t_vas, t_pli + 0.6))
    dedo_corte(img, *C.xy(540, 900), k, t)
    C.fondo(img)
    C.pon(K.cronometro(2 * pi * prog(t, t0, t_min + 1.0)), 860, 380, 1.6, 0.0, t_in=t0 + 0.1, dur=0.35)
    C.rot("5 MIN", 860, 540, 90, 0.04, CREMA, t_in=t_min, dur=0.3)
    C.rot("VASOS SANGUÍNEOS", 540, 1560, 90, -0.02, (255, 130, 140), t_in=t_vas, dur=0.3, tira=True)
    if t >= t_con:
        C.rot("¡SE CONTRAEN!", 540, 1720, 100, 0.03, (255, 236, 120), t_in=t_con, dur=0.3, tira=True)
    if t >= t_pli:
        C.rot("LA PIEL SE PLIEGA", 540, 300, 96, -0.03, CREMA, t_in=t_pli, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 4. neumático
@escena("neumatico")
def neumatico(C, t):
    t0 = INI("neumatico")
    t_neu = T("neumatico", "neumatico")
    t_can = T("neumatico", "canalizan", frase=1)
    capas = C.capas_de("lab3", lambda: capas_agua(19, (120, 140, 170), (60, 70, 100)))
    cam_suave(C, t, t0, FIN("neumatico"))
    img = C.base("neumatico", capas)
    C.fondo(img)
    if t < t_can - 0.2:
        # carretera mojada y un neumático que rueda levantando agua
        u = prog(t, t0, t_can - 0.2)
        x = lerp(-120, 1200, u)
        C.pon(X.neumatico(), x, 1100, 2.4, x / 96.0 / 2.4, vida=0.3)
        for i in range(6):
            ph = ((t - t0) * 1.3 + i / 6) % 1.0
            C.pon(X.gotita("", "", 1.0), x - 120 - 160 * ph, 1190 - 200 * 4 * ph * (1 - ph), 0.8, 0.0)
        C.rot("RANURAS", 540, 330, 150, -0.03, CREMA, t_in=t_neu - 0.3, dur=0.3, tira=True)
        C.rot("COMO UN NEUMÁTICO", 540, 1560, 88, 0.02, (255, 236, 120), t_in=t_neu, dur=0.3, tira=True)
    else:
        C.pon(X.mano(2, "grandes", "sonrisa"), 540, 1000, 2.9, 0.0, t_in=t_can - 0.2, dur=0.4, vida=0.8)
        for i in range(8):
            ph = ((t - t_can) * 0.9 + i / 8) % 1.0
            a = -pi / 2 + (i - 3.5) * 0.28
            C.pon(X.gotita("", "", 1.0), 540 + 360 * ph * math.cos(a) * 0.9 + (i - 3.5) * 40, 460 - 160 * ph - 140 * abs(i - 3.5) / 3.5 * ph, 0.8 * (1 - ph * 0.5), 0.0)
        C.rot("CANALIZAN EL AGUA", 540, 330, 90, -0.03, AZUL_T, t_in=t_can, dur=0.3, tira=True)
        C.rot("¡MÁS AGARRE!", 540, 1700, 120, 0.03, (255, 236, 120), t_in=T("neumatico", "agarre", frase=1), dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 5. prueba
@escena("prueba")
def prueba(C, t):
    t0 = INI("prueba")
    t_exp, t_moj = T("prueba", "experimentos"), T("prueba", "mojados")
    t_rap = T("prueba", "rapido")
    t_sec = T("prueba", "secos", frase=1)
    capas = C.capas_de("lab", capas_lab)
    cam_suave(C, t, t0, FIN("prueba"))
    img = C.base("prueba", capas)
    C.fondo(img)
    seco = t >= t_sec - 0.1
    # izquierda: dedos lisos; derecha: dedos arrugados
    ciclo = ((t - t0) % 2.2) / 2.2
    C.pon(X.mano(0, "esfuerzo" if not seco else "grandes", "triste" if not seco else "sonrisa"), 290, 1050, 1.7, 0.1 * math.sin(t * 9) * (0 if seco else 1), t_in=t0 + 0.1, vida=1.2)
    C.pon(X.mano(2, "feliz", "sonrisa"), 790, 1050, 1.7, 0.0, t_in=t0 + 0.2, vida=0.8)
    col = (240, 90, 100) if not seco else (120, 200, 120)
    # canicas
    C.pon(X.disco(34, col), 290 + 40 * ciclo, 1470 + 120 * (ciclo ** 2) * (0 if seco else 1), 1.0, 0.0, t_in=t0 + 0.3, dur=0.3)
    C.pon(X.disco(34, col), 790, 1470 - 200 * e_out(min(1.0, ciclo * 1.6)) if not seco else 1470, 1.0, 0.0, t_in=t0 + 0.3, dur=0.3)
    if not seco:
        C.pon(X.tache(46), 290, 760, 1.4, 0.0, t_in=t_moj + 0.4, modo="pop", dur=0.25)
        C.pon(X.palomita(46), 790, 760, 1.4, 0.0, t_in=t_moj + 0.4, modo="pop", dur=0.25)
        C.rot("OBJETOS MOJADOS", 540, 300, 96, -0.03, AZUL_T, t_in=t_moj, dur=0.3, tira=True)
        C.rot("¡MÁS RÁPIDO!", 790, 640, 70, 0.05, (255, 150, 90), t_in=t_rap, dur=0.3)
    else:
        C.pon(X.palomita(46), 290, 760, 1.4, 0.0, t_in=t_sec + 0.2, modo="pop", dur=0.25)
        C.pon(X.palomita(46), 790, 760, 1.4, 0.0, t_in=t_sec + 0.2, modo="pop", dur=0.25)
        C.rot("OBJETOS SECOS", 540, 300, 96, -0.03, (150, 110, 60), t_in=t_sec - 0.2, dur=0.3, tira=True)
        C.rot("=", 540, 1150, 220, 0.0, ORO, t_in=t_sec + 0.5, dur=0.3)
    return C.fin()


# ------------------------------------------------------------------ 6. cierre
@escena("cierre")
def cierre(C, t):
    t0 = INI("cierre")
    t_anc, t_pec = T("cierre", "ancestros"), T("cierre", "peces")
    t_sis = T("cierre", "sistema", frase=1)
    capas = C.capas_de("rio", capas_rio)
    cam_suave(C, t, t0, FIN("cierre"))
    img = C.base("cierre", capas)
    C.fondo(img)
    if t < t_sis - 0.3:
        C.pon(X.cazador("grandes", "sonrisa"), 330, 1150, 1.9, 0.0, t_in=t0 + 0.1, vida=0.8)
        C.pon(X.pez("grandes", "o"), 760 + 30 * math.sin(t * 9), 1020 + 20 * math.sin(t * 11), 1.2, 0.3 * math.sin(t * 9), t_in=t_pec - 0.2, dur=0.3, vida=1.6)
        C.pon(X.roca(), 880, 1520, 1.2, 0.0, t_in=t0 + 0.2)
        C.rot("ANCESTROS", 540, 300, 140, -0.03, (255, 236, 120), t_in=t_anc, dur=0.3, t_out=t_sis - 0.3, d_out=0.2, tira=True)
        C.rot("PECES RESBALOSOS", 540, 460, 84, 0.03, CREMA, t_in=t_pec, dur=0.3, t_out=t_sis - 0.3, d_out=0.2, tira=True)
    else:
        C.pon(X.neumatico(), 540, 940, 3.3, t * 0.4, t_in=t_sis - 0.3, dur=0.4, vida=0.2)
        C.pon(X.mano(2, "feliz", "sonrisa"), 540, 1000, 2.1, 0.0, t_in=t_sis - 0.1, dur=0.4, vida=1.0)
        C.rot("ANTIDESLIZANTE", 540, 330, 110, -0.03, (255, 236, 120), t_in=t_sis, dur=0.3, tira=True)
        C.rot("INTEGRADO", 540, 1650, 130, 0.03, (255, 150, 90), t_in=t_sis + 0.6, dur=0.3, tira=True)
        for j, (dx, dy, tt) in enumerate([(-360, -240, t_sis + 0.2), (360, -260, t_sis + 0.35), (-340, 280, t_sis + 0.5), (350, 260, t_sis + 0.65)]):
            C.pon(K.CHISPA, 540 + dx, 1000 + dy + 8 * math.sin(t * 3 + j), 0.8, t * 0.5 + j, t_in=tt, modo="pop", dur=0.3)
    return C.fin()
