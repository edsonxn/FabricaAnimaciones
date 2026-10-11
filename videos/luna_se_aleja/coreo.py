# -*- coding: utf-8 -*-
"""La Luna se está yendo: gancho, unas, espejos, dias, pasado, futuro, cierre."""
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
CREMA = (255, 246, 214)
ORO = (255, 224, 110)


def flash(out, a, col=255):
    if a <= 0.01:
        return out
    return np.clip(out.astype(np.float32) * (1 - a) + col * a, 0, 255).astype(np.uint8)


def capas_espacio(seed=3, c0=(8, 12, 40), c1=(40, 40, 100), estrellas=360):
    far = P.cosmos(seed, c0, c1, [(520, 0.8, (30, 36, 100), .5), (340, 1.2, (60, 50, 130), .4), (240, 1.7, (120, 70, 150), .25)], estrellas=estrellas)
    return [(far, 0.3)]


def orbita(img, cx, cy, rx, ry, t, col=(220, 230, 255), n=60):
    for k in range(n):
        if k % 2:
            continue
        a = 2 * pi * k / n
        cv2.circle(img, (int((cx + rx * math.cos(a)) * 4), int((cy + ry * math.sin(a)) * 4)), 10, col, -1, cv2.LINE_AA, 2)


def cam_suave(C, t, a, b, z=0.05):
    u = (t - a) / max(1e-6, b - a)
    C.cam = (1.0 + z * u, 6 * math.sin(t * 0.8), -12 * math.cos(t * 0.5))


# ------------------------------------------------------------------ 1. gancho
@escena("gancho")
def gancho(C, t):
    t0 = INI("gancho")
    t_yen, t_lej = T("gancho", "yendo"), T("gancho", "lejos", frase=1)
    capas = C.capas_de("e1", lambda: capas_espacio(3))
    cam_suave(C, t, t0, FIN("gancho"))
    img = C.base("gancho", capas)
    u = prog(t, t0, FIN("gancho"))
    mx, my = lerp(560, 800, e_inout(u)), lerp(660, 380, e_inout(u))
    orbita(img, *C.xy(540, 900), 330, 330, t) if False else None
    C.fondo(img)
    # la Tierra, abajo, sigue con la mirada a la Luna
    C.pon(X.tierra("grandes" if t < t_lej else "miedo", "triste" if t < t_lej else "o"), 540, 1400, 3.0, 0.02 * math.sin(t * 1.5), vida=0.8)
    # la Luna se va despidiéndose con la mano
    sc = lerp(2.0, 1.2, e_inout(u))
    C.pon(X.luna("grandes", "sonrisa"), mx, my, sc, 0.1 * math.sin(t * 2), t_in=t0 + 0.05, vida=0.8)
    C.pon(X.mano(0), mx - 150 * sc / 2, my + 40, 0.5 * sc, 0.5 * math.sin(t * 7) - 0.3, t_in=t0 + 0.3, dur=0.3, vida=1.0)
    C.rot("LA LUNA", 540, 280, 140, -0.04, CREMA, t_in=T("gancho", "luna"), dur=0.3, t_out=t_lej - 0.1, d_out=0.2)
    C.rot("SE VA", 540, 430, 150, 0.03, (255, 150, 90), t_in=t_yen, dur=0.3, tira=True, t_out=t_lej - 0.1, d_out=0.2)
    C.rot("CADA AÑO", 540, 290, 130, -0.03, ORO, t_in=T("gancho", "ano", frase=1), dur=0.3)
    C.rot("MÁS LEJOS", 540, 440, 130, 0.03, (255, 150, 90), t_in=t_lej, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 2. uñas
@escena("unas")
def unas(C, t):
    t0 = INI("unas")
    t_cm, t_un = T("unas", "centimetros"), T("unas", "unas")
    capas = C.capas_de("e2", lambda: capas_espacio(7, (14, 18, 54), (60, 50, 120)))
    cam_suave(C, t, t0, FIN("unas"))
    img = C.base("unas", capas)
    C.fondo(img)
    # arriba: la Luna recorre 4 cm de una regla cada «año» (1,8 s)
    ciclo = ((t - t0) % 1.8) / 1.8
    mx = 120 + 4 * 75 * e_inout(min(1.0, ciclo * 1.25))
    C.pon(X.regla(9, 34), 120, 560, 2.2, 0.0, t_in=t0 + 0.1, dur=0.3)
    C.pon(X.luna("grandes", "sonrisa", 88), mx, 440, 1.1, 0.0, t_in=t0 + 0.2, vida=0.8)
    C.rot("4 CM POR AÑO", 540, 290, 110, -0.03, ORO, t_in=t_cm, dur=0.3, tira=True)
    # abajo: el dedo con la uña que crece lo mismo
    una = 52 * e_inout(min(1.0, ciclo * 1.25))
    C.pon(X.dedo_una(una), 540, 1050, 3.0, 0.0, t_in=t0 + 0.6, modo="sube", dur=0.45, vida=0.6)
    C.pon(X.regla(9, 34), 940, 1560, 2.0, -pi / 2, t_in=t_un + 0.1, dur=0.3) if False else None
    C.rot("= TUS UÑAS", 540, 1640, 130, 0.03, (255, 150, 90), t_in=t_un + 0.2, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 3. espejos
@escena("espejos")
def espejos(C, t):
    t0 = INI("espejos")
    t_esp, t_las = T("espejos", "espejos"), T("espejos", "laseres", frase=1)
    t_vol = T("espejos", "volver", frase=1)
    capas = C.capas_de("e3", lambda: capas_espacio(13, (6, 8, 30), (30, 30, 80)) + [(_suelo_lunar(), 1.0)])
    cam_suave(C, t, t0, FIN("espejos"))
    img = C.base("espejos", capas)
    # láser Tierra -> espejo (ida y vuelta, en bucle)
    ex, ey = C.xy(540, 1330)
    tx, ty = C.xy(210, 330)
    if t >= t_las:
        ciclo = ((t - t_las) % 1.6) / 1.6
        d = ciclo * 2 if ciclo < 0.5 else 2 - ciclo * 2
        d = 1 - abs(1 - ciclo * 2)
        cv2.line(img, (int(tx * 4), int(ty * 4)), (int(ex * 4), int(ey * 4)), (255, 120, 120), 6, cv2.LINE_AA, 2)
        cv2.line(img, (int(tx * 4), int(ty * 4)), (int(ex * 4), int(ey * 4)), (255, 220, 220), 2, cv2.LINE_AA, 2)
        px, py = lerp(tx, ex, d), lerp(ty, ey, d)
        P.halo(img, px, py, 60, (255, 230, 230), 0.9, 4)
        P.disco(img, px, py, 16, (255, 255, 255), 1.0)
    C.fondo(img)
    C.pon(X.tierra("grandes", "sonrisa", 96), 210, 330, 1.2, 0.0, t_in=t0 + 0.1, vida=0.8)
    C.pon(X.astronauta("grandes", "sonrisa", "dcha" if t < t_esp + 1.5 else "arriba"), 360, 1260, 1.9, 0.0, t_in=t0 + 0.2, vida=0.6)
    C.pon(X.espejo_lunar(), 700, 1330, 1.6, 0.0, t_in=t_esp, modo="cae", dur=0.35, vida=0.4)
    C.rot("ESPEJOS", 620, 570, 150, -0.03, CREMA, t_in=t_esp, dur=0.3, t_out=t_las - 0.1, d_out=0.2)
    C.rot("EN LA LUNA", 620, 710, 110, 0.03, ORO, t_in=t_esp + 0.3, dur=0.3, tira=True, t_out=t_las - 0.1, d_out=0.2)
    if t >= t_las:
        C.rot("LÁSER", 640, 560, 160, -0.03, (255, 130, 130), t_in=t_las, dur=0.3)
        C.pon(K.cronometro(2 * pi * ((t - t_las) % 1.6) / 1.6), 880, 820, 1.4, 0.0, t_in=t_vol - 0.5, dur=0.3)
        C.rot("IDA Y VUELTA", 760, 970, 62, 0.04, CREMA, t_in=t_vol - 0.3, dur=0.25, tira=True)
    return C.fin()


def _suelo_lunar():
    suelo = P.vacio()
    P.mancha(suelo, BW / 2, BH - 40, 900, 330, (170, 168, 180), 21, rough=0.04)
    P.mancha(suelo, 300, BH - 120, 400, 150, (190, 188, 200), 22, rough=0.06)
    for (x, y, rx, ry) in [(220, BH - 260, 70, 22), (700, BH - 200, 90, 26), (900, BH - 300, 50, 16)]:
        P.mancha(suelo, x, y, rx, ry, (140, 138, 154), int(x), rough=0.05)
    P.textura(suelo, 0.02, 0.04)
    return suelo


# ------------------------------------------------------------------ 4. días
@escena("dias")
def dias(C, t):
    t0 = INI("dias")
    t_mar, t_fre = T("dias", "mareas"), T("dias", "frenan")
    t_dia, t_mil = T("dias", "dias", frase=1), T("dias", "milisegundos", frase=1)
    capas = C.capas_de("e4", lambda: capas_espacio(17, (10, 14, 44), (50, 44, 110)))
    cam_suave(C, t, t0, FIN("dias"))
    img = C.base("dias", capas)
    ex, ey = C.xy(440, 880)
    # marea: el agua se abulta hacia la Luna (y hacia el lado opuesto)
    ang = 0.0
    for sg in (1, -1):
        P.mancha_din(img, ex + sg * 130 * C.k(), ey, 330 * C.k(), 250 * C.k(), (90, 160, 250), 0.75, seed=1 + (sg > 0), t=t, rough=0.06)
    C.fondo(img)
    C.pon(X.tierra("grandes", "sonrisa", 96), 440, 880, 2.4, 0.3 * (t - t0) * (1 - 0.6 * prog(t, t_fre, t_fre + 2.0)), t_in=t0 + 0.05, vida=0.6)
    # la Luna se aleja empujada por la marea
    mx = lerp(850, 930, e_inout(prog(t, t0, FIN("dias"))))
    C.pon(X.luna("grandes", "sonrisa", 88), mx, 640, 1.0, 0.0, t_in=t0 + 0.2, vida=0.8)
    C.pon(X.flecha_arriba((250, 130, 60), 160), mx - 10, 780, 0.9, pi / 2, t_in=t_mar, dur=0.3)
    C.rot("MAREAS", 540, 300, 140, -0.04, (130, 190, 255), t_in=t_mar, dur=0.3, t_out=t_dia - 0.1, d_out=0.2)
    C.rot("FRENAN A LA TIERRA", 540, 440, 78, 0.03, ORO, t_in=t_fre, dur=0.3, tira=True, t_out=t_dia - 0.1, d_out=0.2)
    # reloj: el día se alarga
    if t >= t_dia - 0.2:
        C.pon(X.reloj_cara(((t - t_dia) * 0.18) % 1.0, "grandes", "sonrisa", 24), 540, 1480, 1.5, 0.0, t_in=t_dia - 0.2, dur=0.35, vida=0.6)
        C.rot("DÍAS MÁS LARGOS", 540, 300, 92, -0.03, CREMA, t_in=t_dia, dur=0.3, tira=True)
        C.rot("+ MILISEGUNDOS", 540, 1700, 80, 0.03, (255, 150, 90), t_in=t_mil, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 5. pasado
def capas_pasado():
    far = P.fondo_liso(41, (240, 150, 90), (120, 70, 130), [(520, 0.7, (255, 190, 110), .5), (300, 1.2, (210, 100, 120), .4)])
    mar = P.vacio()
    P.mancha(mar, BW / 2, BH - 60, 1000, 420, (60, 150, 170), 5, rough=0.03)
    P.mancha(mar, BW / 2, BH - 160, 900, 260, (80, 180, 190), 6, rough=0.04)
    P.textura(mar, 0.02, 0.04)
    return [(far, 0.25), (mar, 1.0)]


@escena("pasado")
def pasado(C, t):
    t0 = INI("pasado")
    t_400, t_22 = T("pasado", "cuatrocientos"), T("pasado", "veintidos")
    capas = C.capas_de("e5", capas_pasado)
    cam_suave(C, t, t0, FIN("pasado"))
    img = C.base("pasado", capas)
    sx, sy = C.xy(820, 480)
    P.halo(img, sx, sy, 380, (255, 220, 140), 0.7, 6)
    P.disco(img, sx, sy, 90, (255, 236, 170), 1.0)
    C.fondo(img)
    # el calendario retrocede
    v = 400000000 * e_out(prog(t, t_400, t_400 + 1.8))
    C.pon(X.reloj_cara(((t - t0) * 0.5) % 1.0, "grandes", "sonrisa", 22), 300, 1090, 2.0, 0.0, t_in=t_22 - 0.4, dur=0.35, vida=0.8)
    C.rot("22 H", 300, 1330, 160, -0.04, (255, 236, 130), t_in=t_22, dur=0.3, tira=True)
    C.rot("HACE", 540, 270, 100, -0.03, CREMA, t_in=t0 + 0.4, dur=0.3)
    if t >= t_400:
        C.rot(f"{int(v):,}".replace(",", " "), 540, 400, 118, 0.02, (255, 150, 90), t_in=t_400, dur=0.3)
        C.rot("DE AÑOS", 540, 540, 100, -0.03, CREMA, t_in=t_400 + 1.8, dur=0.3, tira=True)
    # un pez antiguo salta del mar
    ph = ((t - t0) * 0.45) % 1.0
    fx = 120 + 800 * ph
    fy = 1500 - 520 * 4 * ph * (1 - ph)
    C.pon(X.pez("grandes", "o"), fx, fy, 0.9, -0.5 + 1.0 * ph * 2 - 0.0, t_in=t0 + 0.3, dur=0.3, vida=1.0)
    return C.fin()


# ------------------------------------------------------------------ 6. futuro
@escena("futuro")
def futuro(C, t):
    t0 = INI("futuro")
    t_600, t_peq, t_ecl = T("futuro", "seiscientos"), T("futuro", "pequena"), T("futuro", "eclipses")
    capas = C.capas_de("e6", lambda: capas_espacio(23, (6, 6, 24), (30, 24, 70)))
    cam_suave(C, t, t0, FIN("futuro"))
    img = C.base("futuro", capas)
    sx, sy = C.xy(540, 900)
    P.halo(img, sx, sy, 520, (255, 220, 120), 0.5, 6)
    C.fondo(img)
    C.pon(X.sol_disco(110, 1.0), 540, 900, 2.3, t * 0.05, t_in=t0 + 0.05, vida=0.6)
    # la Luna cubre el Sol y se va achicando
    k = 1.0 - 0.3 * e_inout(prog(t, t_peq - 0.2, t_peq + 1.6))
    mx = 540 + 6 * math.sin(t * 2)
    C.pon(X.disco(90, (74, 72, 96)), mx, 900, 3.02 * k, 0.0, t_in=t0 + 0.2, dur=0.4)
    if t < t_peq:
        C.rot("ECLIPSE TOTAL", 540, 330, 120, -0.03, ORO, t_in=t0 + 0.5, dur=0.3, tira=True)
    C.rot(f"+ {int(600 * e_out(prog(t, t_600, t_600 + 1.4)))} MILLONES DE AÑOS", 540, 1560, 70, 0.02, CREMA, t_in=t_600, dur=0.3, tira=True)
    if t >= t_peq + 0.4:
        C.rot("LA LUNA YA NO TAPA", 540, 330, 90, -0.03, (255, 150, 90), t_in=t_peq + 0.4, dur=0.3, tira=True)
        C.pon(X.tache(60), 880, 540, 2.0, 0.0, t_in=t_ecl, modo="pop", dur=0.3)
    return C.fin()


# ------------------------------------------------------------------ 7. cierre
@escena("cierre")
def cierre(C, t):
    t0 = INI("cierre")
    t_sue, t_enc = T("cierre", "suerte"), T("cierre", "encaja")
    capas = C.capas_de("e7", lambda: capas_espacio(29, (10, 14, 50), (70, 50, 120)))
    cam_suave(C, t, t0, FIN("cierre"))
    img = C.base("cierre", capas)
    sx, sy = C.xy(540, 640)
    P.halo(img, sx, sy, 460, (255, 226, 130), 0.6, 6)
    C.fondo(img)
    C.pon(X.sol_disco(110, 1.0), 540, 640, 1.9, t * 0.05, t_in=t0 + 0.05, vida=0.6)
    C.pon(X.disco(90, (74, 72, 96)), 540, 640, 2.28, 0.0, t_in=t_enc - 0.3, modo="pop", dur=0.4)
    C.pon(K.persona("grandes", "o", "arriba"), 540, 1380, 1.7, 0.0, t_in=t0 + 0.2, vida=0.8)
    C.pon(X.gafas_eclipse(), 540, 1380 - 118 * 1.7, 1.7 * 0.62, 0.0, t_in=t0 + 0.5, dur=0.3)
    C.rot("TENEMOS SUERTE", 540, 290, 100, -0.03, ORO, t_in=t_sue, dur=0.3, tira=True)
    for j, (dx, dy, tt) in enumerate([(-360, -60, t_enc + 0.2), (360, -80, t_enc + 0.35), (-340, 300, t_enc + 0.5), (350, 280, t_enc + 0.65)]):
        C.pon(K.corazon(26), 540 + dx, 700 + dy + 10 * math.sin(t * 3 + j), 1.0, 0.1 * math.sin(t + j), t_in=tt, modo="pop", dur=0.3)
    C.rot("ENCAJA PERFECTO", 540, 1700, 80, 0.02, (255, 150, 90), t_in=t_enc, dur=0.3, tira=True)
    return C.fin()
