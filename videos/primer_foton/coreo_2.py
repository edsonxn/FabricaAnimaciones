# -*- coding: utf-8 -*-
"""Escenas 4-6: multitud (más de mil millones de fotones por átomo), niebla (luz atrapada 380 000 años) y libre (recombinación: la luz escapa)."""
import math

import cv2
import numpy as np

import kit as K
import pintura as P
from coreo_util import balistica, bump, kf, pulso
from escenas import FIN, INI, escena
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY


def flash(out, a, col=255):
    if a <= 0.01:
        return out
    return np.clip(out.astype(np.float32) * (1 - a) + col * a, 0, 255).astype(np.uint8)


# =========================================================== 4. MULTITUD
N_S = 950
_rs = np.random.default_rng(5)
S_A = _rs.uniform(0, 2 * pi, N_S)
S_V = _rs.uniform(130, 640, N_S)
S_B = 25.47 + 1.9 * (np.arange(N_S) / N_S) ** 0.8
S_R = _rs.choice([4.5, 6.0, 8.0, 11.0], N_S, p=[.4, .3, .2, .1])
S_D = _rs.choice([-1, 1], N_S)
S_C = [(255, 230, 120), (255, 246, 200), (255, 196, 90), (255, 214, 66)]
CARAS = [("feliz", "abierta"), ("guino", "lengua"), ("grandes", "sonrisa"), ("estrellas", "abierta"), ("feliz", "sonrisa"), ("grandes", "abierta")]


def capas_multitud():
    far = P.cosmos(51, (8, 24, 52), (22, 88, 108), [(520, 0.8, (30, 70, 120), .55), (340, 1.2, (40, 120, 130), .4), (240, 1.6, (90, 60, 150), .3)],
                   estrellas=380)
    return [(far, 0.3)]


def orbita_punteada(img, cx, cy, rx, ry, rot, t):
    for k in range(40):
        a = 2 * pi * k / 40 + t * 0.5
        if k % 2:
            continue
        x, y = rx * math.cos(a), ry * math.sin(a)
        c, s = math.cos(rot), math.sin(rot)
        cv2.circle(img, (int((cx + x * c - y * s) * 4), int((cy + x * s + y * c) * 4)), 14, (230, 240, 255), -1, cv2.LINE_AA, 2)


@escena("multitud")
def multitud(C, t):
    t0 = INI("multitud")
    capas = C.capas_de("multitud", capas_multitud)
    zoom = 1.0 - 0.15 * e_inout(prog(t, 25.4, 28.4)) + 0.05 * bump(t, 22.99, 0.5, 1.0)
    C.cam = (zoom, 8 * math.sin(t * 0.8), -10 * math.cos(t * 0.6))
    img = C.base("multitud", capas)
    fx, fy = C.xy(540, 900)
    P.halo(img, fx, fy, 520 + 60 * math.sin(t * 3), (255, 226, 130), 0.55, 6)
    ax, ay = C.xy(540, 1400)
    if t > 23.9:
        orbita_punteada(img, ax, ay, 190 * C.k(), 78 * C.k(), 0.25, t)
    # enjambre de fotones (detrás de todo)
    if t > 25.47:
        k = C.k()
        for i in range(N_S):
            tb = S_B[i]
            if t < tb:
                continue
            r = ((t - tb) * S_V[i]) % 1500 + 60
            th = S_A[i] + S_D[i] * 0.55 * math.log(1 + r / 120)
            x, y = fx + r * math.cos(th) * k, fy + r * math.sin(th) * 1.15 * k
            if -20 < x < W + 20 and -20 < y < H + 20:
                cv2.circle(img, (int(x * 4), int(y * 4)), int(S_R[i] * k * 4 * min(1, (t - tb) * 4)), S_C[i % 4], -1, cv2.LINE_AA, 2)
    C.fondo(img)
    # --- Foti original (continúa de la escena anterior)
    ojos, boca = ("guino", "lengua") if t < 22.7 else ("grandes", "abierta")
    C.foti(540, 900 + 14 * math.sin(t * 2.5), 2.4 + bump(t, 22.99, 0.5, 0.25) + bump(t, 25.47, 0.5, 0.3), 0.04 * math.sin(t * 2), ojos, boca,
           largo=300, amp=22, sem=5)
    # clones en dos anillos
    for k in range(6):
        a = k * pi / 3 + t * 0.3
        o, b = CARAS[k % 6]
        C.foti(540 + 340 * math.cos(a), 900 + 320 * math.sin(a), 1.25, 0.3 * math.sin(t * 2 + k), o, b, t_in=22.99 + 0.08 * k, cola=False, sem=k)
    for k in range(12):
        a = k * pi / 6 + 0.26 - t * 0.2
        o, b = CARAS[(k + 2) % 6]
        C.foti(540 + 470 * math.cos(a), 900 + 440 * math.sin(a), 0.85, 0.3 * math.sin(t * 2 + k), o, b, t_in=23.55 + 0.05 * k, cola=False, sem=k + 7)
    # --- el átomo (uno solo)
    if t > 23.9:
        ang = t * 3.2
        ex_, ey_ = 190 * math.cos(ang), 78 * math.sin(ang)
        c, s = math.cos(0.25), math.sin(0.25)
        px_, py_ = 540 + ex_ * c - ey_ * s, 1400 + ex_ * s + ey_ * c
        if math.sin(ang) < 0:
            C.pon(K.electron("feliz", "sonrisa"), px_, py_, 1.2, 0.0, t_in=24.0)
        C.pon(K.proton("grandes", "sonrisa"), 540, 1400, 1.7, 0.0, t_in=24.0, modo="pop")
        if math.sin(ang) >= 0:
            C.pon(K.electron("feliz", "sonrisa"), px_, py_, 1.2, 0.0, t_in=24.0)
    C.rot("1 ÁTOMO", 540, 1590, 100, -0.03, (255, 246, 214), t_in=24.23, tira=True)
    # --- cifras
    C.rot("MÁS DE", 540, 280, 100, -0.04, (255, 246, 214), t_in=26.13, dur=0.3)
    C.rot("1 000 000 000", 540, 410, 118, 0.03, (255, 150, 90), t_in=26.53, dur=0.3, tira=True)
    C.rot("FOTONES", 540, 540, 150, -0.03, (255, 236, 130), t_in=27.23, dur=0.3)
    out = C.fin()
    return flash(out, pulso(t, 25.47, 0.3) * 0.3)


# =========================================================== 5. NIEBLA
# Foti rebota entre electrones: (t del choque, posición)
WP = [(31.98, (110, 800)), (32.28, (380, 960)), (32.72, (250, 1260)), (32.88, (470, 1330)), (33.50, (760, 1090)), (33.76, (900, 1300)),
      (33.90, (700, 1420)), (34.06, (560, 1190)), (34.99, (540, 960))]
GOLPES = ["¡PAF!", "¡PUM!", "¡ZAS!", "¡PAF!", "¡PUM!", "¡ZAS!", "¡AY!"]
RING = 10
DECOR = [(120, 520), (940, 560), (140, 1500), (930, 1520), (540, 720), (300, 1650)]            # electrones de adorno (posición libre)
_rf = np.random.default_rng(13)
FOG = [(_rf.uniform(0, W), _rf.uniform(200, 1800), _rf.uniform(260, 430), _rf.uniform(0, 6.28), _rf.choice([0, 1])) for _ in range(14)]


def capas_niebla():
    far = P.cosmos(61, (150, 62, 82), (244, 160, 112), [(520, 0.7, (232, 116, 100), .55), (340, 1.1, (252, 190, 130), .5), (230, 1.6, (255, 226, 176), .4)],
                   estrellas=0)
    return [(far, 0.3)]


def electron_pos(i, t):
    """Posición del electrón i: libre (golpeado o de adorno) y, desde 35.0, en jaula alrededor de Foti."""
    if i < len(WP) - 2:
        tc, (x, y) = WP[i + 1]
        dx = 0.0
        if t > tc:                                             # el golpe lo empuja un poco
            u = prog(t, tc, tc + 0.5)
            dx = (30 if x < 540 else -30) * e_out(u) * (1 - 0.0)
        bx, by = x + dx, y + 8 * math.sin(t * 2 + i)
    else:
        j = i - (len(WP) - 2)
        x, y = DECOR[j % len(DECOR)]
        bx, by = x + 14 * math.sin(t * 1.3 + j), y + 10 * math.cos(t * 1.7 + j)
    k = e_inout(prog(t, 35.0, 35.7))
    a = i * 2 * pi / RING + t * 0.9
    return lerp(bx, 540 + 285 * math.cos(a), k), lerp(by, 960 + 285 * math.sin(a), k)


def foti_niebla(t):
    xy = kf(t, [(w[0], w[1]) for w in WP], e_out)
    return xy


def niebla_blobs(img, t, frente):
    for i, (x, y, r, ph, tipo) in enumerate(FOG):
        if (i % 3 == 0) != frente:
            continue
        xx = x + 90 * math.sin(t * 0.35 + ph)
        yy = y + 40 * math.sin(t * 0.5 + ph * 1.3)
        col = (255, 226, 200) if tipo else (244, 160, 146)
        P.mancha_din(img, xx, yy, r, r * 0.62, col, 0.17 if frente else 0.34, seed=i, t=t, rough=0.18)


@escena("niebla")
def niebla(C, t):
    t0 = INI("niebla")
    capas = C.capas_de("niebla", capas_niebla)
    shake = pulso(t, 32.28, 0.25) + pulso(t, 32.72, 0.2) + pulso(t, 32.88, 0.2) + pulso(t, 33.5, 0.2) + pulso(t, 33.9, 0.2) + pulso(t, 34.06, 0.25)
    C.cam = (1.0 + 0.05 * prog(t, t0, FIN("niebla")), 10 * math.sin(t * 61) * min(1, shake), 8 * math.sin(t * 47) * min(1, shake))
    img = C.base("niebla", capas)
    fx, fy = C.xy(540, 960)
    niebla_blobs(img, t, False)
    C.fondo(img)
    # --- rótulos de la niebla
    C.rot("NIEBLA", 540, 300, 150, -0.03, (255, 246, 214), t_in=30.8, dur=0.3, t_out=31.9, d_out=0.25)
    C.rot("ARDIENTE", 540, 450, 130, 0.03, (255, 130, 70), t_in=31.1, dur=0.3, t_out=31.9, d_out=0.25, tira=True)
    # --- electrones
    nel = len(WP) - 2 + len(DECOR)
    for i in range(nel):
        x, y = electron_pos(i, t)
        golpe = (i < len(WP) - 2) and WP[i + 1][0] <= t < WP[i + 1][0] + 0.45
        caged = t > 35.4
        o, b = ("grandes", "o")
        if golpe:
            o, b = "miedo", "grito"
        elif caged:
            o, b = "enojado", "dientes"
        if i < RING or True:
            C.pon(K.electron(o, b), x, y, 2.0 if i < len(WP) - 2 else 1.7, 0.2 * math.sin(t * 3 + i), t_in=t0 + 0.04 * i,
                  sq=(0.3 * (1 - prog(t, WP[i + 1][0], WP[i + 1][0] + 0.3)) if golpe and i < len(WP) - 2 else 0.0))
    # --- calendarios que vuelan (pasan los años)
    if t > 35.2:
        for j in range(8):
            ph = ((t - 35.2) * 0.62 + j / 8) % 1.0
            C.pon(K.hoja_calendario(), 90 + (j * 137) % 900, 2050 - ph * 2300, 1.15, 0.3 * math.sin(t * 2 + j), t_in=35.2 + 0.1 * j, dur=0.2)
    # --- Foti rebotando y luego atrapado
    if t >= WP[0][0]:
        x, y = foti_niebla(t)
        mareo = t >= 33.5
        ojos = "mareado" if t >= 33.9 else ("miedo" if t >= 32.28 else "grandes")
        boca = "triste" if t >= 35.4 else ("grito" if t >= 32.28 else "o")
        if t >= 35.4:
            ojos = "cerrados"
        sq = 0.0
        for (tc, _) in WP[1:-1]:
            if tc <= t < tc + 0.3:
                sq = 0.25 * (1 - prog(t, tc, tc + 0.3))
        vida = 1.0 + 2.5 * prog(t, 35.0, 35.6)
        C.foti(x, y, 1.9, 0.5 * math.sin(t * 9) if t < 35.0 else 0.0, ojos, boca, t_in=WP[0][0], dur=0.3, largo=300, amp=22, vida=vida, sem=3)
        for (tc, p) in WP[1:-1]:
            if tc <= t < tc + 0.5:
                u = prog(t, tc, tc + 0.5)
                C.pon(K.CHISPA, p[0], p[1] - 90 - 30 * u, 0.9, 5 * u, t_in=tc, modo="pop", dur=0.15, t_out=tc + 0.3, d_out=0.2)
        for j, (tc, p) in enumerate(WP[1:-1]):
            if tc <= t < tc + 0.6:
                px_ = min(max(p[0] + (-110 if p[0] > 540 else 110), 130), 950)
                C.rot(GOLPES[j], px_, p[1] - 170, 70 + (14 if j % 2 else 0), (-0.12 if j % 2 else 0.1), (255, 236, 130), t_in=tc, dur=0.15, t_out=tc + 0.45, d_out=0.15)
    # --- 380 000 años
    v = 380000 * e_out(prog(t, 35.49, 36.9))
    if t > 35.49:
        C.rot(f"{int(v):,}".replace(",", " "), 540, 330, 170, -0.03, (255, 236, 130), t_in=35.49, dur=0.3)
    C.rot("AÑOS", 540, 480, 150, 0.03, (255, 130, 70), t_in=36.71, dur=0.3, tira=True)
    out = C.fin()
    img2 = out.copy()
    niebla_blobs(img2, t, True)                        # niebla por delante
    return img2


# =========================================================== 6. LIBRE
NUC = [(200, 700), (470, 610), (800, 740), (210, 1170), (580, 1290), (880, 1120)]
_rn = np.random.default_rng(23)
N_COPOS = 26
CP_X = _rn.uniform(0, W, N_COPOS)
CP_V = _rn.uniform(110, 260, N_COPOS)
CP_R = _rn.uniform(16, 38, N_COPOS)
CP_PH = _rn.uniform(0, 100, N_COPOS)


def capas_libre():
    calida = P.cosmos(61, (150, 62, 82), (244, 160, 112), [(520, 0.7, (232, 116, 100), .55), (340, 1.1, (252, 190, 130), .5), (230, 1.6, (255, 226, 176), .4)],
                      estrellas=0)
    fria = P.cosmos(71, (8, 14, 46), (30, 70, 130), [(520, 0.7, (30, 50, 120), .55), (340, 1.1, (50, 110, 170), .4), (240, 1.6, (110, 80, 170), .3)],
                    estrellas=420)
    return [(calida, 0.3), (fria, 0.3)]


def copo(img, x, y, r, rot):
    for k in range(6):
        a = rot + k * pi / 3
        x1, y1 = x + r * math.cos(a), y + r * math.sin(a)
        cv2.line(img, (int(x * 4), int(y * 4)), (int(x1 * 4), int(y1 * 4)), (225, 244, 255), 5, cv2.LINE_AA, 2)
        for f in (0.55,):
            bx, by = x + r * f * math.cos(a), y + r * f * math.sin(a)
            for sg in (-1, 1):
                cv2.line(img, (int(bx * 4), int(by * 4)), (int((bx + r * 0.3 * math.cos(a + sg * 0.8)) * 4), int((by + r * 0.3 * math.sin(a + sg * 0.8)) * 4)),
                         (225, 244, 255), 4, cv2.LINE_AA, 2)


@escena("libre")
def libre(C, t):
    t0 = INI("libre")
    calida, fria = C.capas_de("libre", capas_libre)
    C.cam = (1.0 + 0.05 * prog(t, t0, FIN("libre")) + 0.08 * bump(t, 46.44, 0.5, 1.0), 6 * math.sin(t * 0.7), -8 * math.cos(t * 0.5))
    z, dx, dy = C.cam
    w = e_inout(prog(t, 38.6, 40.0))
    img = P.componer([calida], z, dx, dy)
    if w > 0.01:
        img = (img.astype(np.float32) * (1 - w) + P.componer([fria], z, dx, dy).astype(np.float32) * w).astype(np.uint8)
    # copos al enfriarse
    if t > 38.6:
        for i in range(N_COPOS):
            y = ((t - 38.6) * CP_V[i] + CP_PH[i] * 20) % (H + 120) - 60
            copo(img, CP_X[i] + 30 * math.sin(t + i), y, CP_R[i], t * 0.6 + i)
    # niebla caliente (se despeja al decir «la niebla se despejó»)
    fog_a = 1.0 - e_inout(prog(t, 43.6, 45.2))
    sweep = e_in(prog(t, 43.6, 45.2))
    if fog_a > 0.02:
        for i, (x, y, r, ph, tipo) in enumerate(FOG):
            xx = x + 90 * math.sin(t * 0.35 + ph) + (-1 if x < W / 2 else 1) * 1000 * sweep
            yy = y + 40 * math.sin(t * 0.5 + ph * 1.3)
            col = (255, 226, 200) if (tipo and w < 0.5) else ((206, 226, 255) if tipo else (190, 170, 220))
            P.mancha_din(img, xx, yy, r, r * 0.62, col, (0.34 if i % 3 else 0.2) * max(fog_a, 0.0) * (1 - 0.3 * w), seed=i, t=t, rough=0.18)
    C.fondo(img)
    # --- termómetro que baja y «frío»
    if 38.3 <= t < 41.0:
        C.pon(K.termometro(round(kf(t, [(38.4, 0.85), (39.4, 0.06)], e_out) * 20) / 20, "cerrados", "zigzag"), 860, 640, 1.6, 0.05, t_in=38.3, modo="sube", dur=0.4,
              vida=1.0 + 2 * prog(t, 38.8, 39.4), t_out=40.2, d_out=0.35, sale="sube_fuera")
    C.rot("¡FRÍO!", 520, 330, 170, -0.04, (150, 210, 255), t_in=39.01, dur=0.3, t_out=39.8, d_out=0.25, tira=True)
    # --- jaula de electrones -> átomos
    kj = e_inout(prog(t, 40.23, 41.4))
    for i in range(RING):
        a = i * 2 * pi / RING + t * 0.9
        cx_, cy_ = 540 + 285 * math.cos(a), 960 + 285 * math.sin(a)
        if i < 6:
            nx, ny = NUC[i]
            b = t * 3.2 + i
            tx, ty = nx + 125 * math.cos(b), ny + 125 * math.sin(b) * 0.55
            x, y = lerp(cx_, tx, kj), lerp(cy_, ty, kj)
            o, bo = ("feliz", "sonrisa") if kj > 0.9 else ("grandes", "o")
            ordr = 1 if math.sin(b) >= 0 else -1
        else:
            x, y = cx_, cy_
            o, bo = "enojado", "dientes"
            ordr = 1
        if i >= 6 and t > 40.3:
            x, y = cx_ + (cx_ - 540) * 2 * prog(t, 40.3, 41.2), cy_ + (cy_ - 960) * 2 * prog(t, 40.3, 41.2)
        if i < 6 and ordr < 0:
            C.pon(K.electron(o, bo), x, y, 1.6, 0.0, t_out=None)
        elif i >= 6:
            C.pon(K.electron(o, bo), x, y, 2.0, 0.0, t_out=41.3, d_out=0.2)
    for i in range(6):
        nx, ny = NUC[i]
        C.pon(K.proton("grandes", "sonrisa"), nx, ny + 6 * math.sin(t * 2 + i), 1.5, 0.0, t_in=40.2 + 0.12 * i, modo="pop")
        b = t * 3.2 + i
        if math.sin(b) >= 0 and kj > 0.0:
            x, y = lerp(540 + 285 * math.cos(i * 2 * pi / RING + t * 0.9), nx + 125 * math.cos(b), kj), lerp(960 + 285 * math.sin(i * 2 * pi / RING + t * 0.9), ny + 125 * math.sin(b) * 0.55, kj)
            C.pon(K.electron("feliz" if kj > 0.9 else "grandes", "sonrisa" if kj > 0.9 else "o"), x, y, 1.6, 0.0)
        if t > 41.1 + 0.15 * i:
            u = prog(t, 41.1 + 0.15 * i, 41.9 + 0.15 * i)
            C.pon(K.corazon(), nx + 70 + 14 * math.sin(u * 6), ny - 90 - 150 * u, 1.0 * (1 - 0.4 * u), 0.1 * math.sin(u * 8), t_in=41.1 + 0.15 * i, dur=0.2,
                  t_out=41.9 + 0.15 * i, d_out=0.2)
    C.rot("ÁTOMOS", 540, 330, 190, -0.03, (255, 236, 130), t_in=42.95, dur=0.3, t_out=44.2, d_out=0.25, tira=True)
    # --- Foti: tiritando, luego libre
    esc = prog(t, 46.44, 47.15)
    if t < 46.2:
        base_s = 1.9
        ojos = "cerrados" if t < 40.2 else ("miedo" if t < 45.2 else "grandes")
        boca = "zigzag" if t < 44.5 else ("o" if t < 45.38 else "abierta")
        if t >= 45.38:
            ojos, boca = "feliz", "abierta"
        C.foti(540, 960, base_s + 0.4 * bump(t, 45.5, 0.4, 1.0) - 0.4 * prog(t, 45.9, 46.2), 0.0, ojos, boca, largo=300, amp=22,
               vida=1.0 + 2.5 * (1 - prog(t, 39.6, 40.2)) * prog(t, 38.4, 38.8) + 2.0 * (t < 44.5 and t > 38.4), sem=3)
    elif esc < 1:
        x = lerp(540, 1000, e_in(esc) ** 1.3)
        y = lerp(960, -260, e_in(esc))
        C.foti(x, y, lerp(1.5, 3.4, e_in(esc)), 0.0 - 0.5 * esc, "grandes", "abierta", largo=700, amp=34, sem=3)
    C.rot("¡LIBRE!", 540, 400, 200, -0.04, (255, 236, 130), t_in=45.5, dur=0.3, t_out=46.4, d_out=0.15, tira=True)
    out = C.fin()
    if 46.44 <= t < 47.3:                              # líneas de velocidad y destello
        r = np.random.default_rng(int(t * 30))
        for _ in range(26):
            a = r.uniform(0, 2 * pi)
            r0, r1 = r.uniform(250, 600), r.uniform(900, 1500)
            cv2.line(out, (int((540 + r0 * math.cos(a)) * 4), int((960 + r0 * math.sin(a)) * 4)), (int((540 + r1 * math.cos(a)) * 4), int((960 + r1 * math.sin(a)) * 4)),
                     (255, 246, 214), int(r.uniform(3, 9)), cv2.LINE_AA, 2)
    return flash(out, pulso(t, 46.55, 0.45) * 0.75)
