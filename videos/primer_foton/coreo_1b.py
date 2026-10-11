# -*- coding: utf-8 -*-
"""Escenas 2-3: calor (sopa de partículas) y higgs (el campo que da masa; el fotón se queda sin ella)."""
import math

import cv2
import numpy as np

import kit as K
import pintura as P
from coreo_util import balistica, bump, kf, pulso
from escenas import FIN, INI, escena
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi

# =========================================================== 2. CALOR
_r2 = np.random.default_rng(7)
N_E = 70
E_X = _r2.uniform(0, W, N_E)
E_V = _r2.uniform(90, 330, N_E)
E_PH = _r2.uniform(0, 100, N_E)
E_R = _r2.uniform(2.5, 7, N_E)


def capas_calor():
    far = P.cosmos(31, (30, 8, 28), (196, 56, 34), [(480, 0.5, (222, 84, 40), .6), (300, 0.95, (248, 144, 50), .5),
                                                   (220, 1.5, (255, 204, 86), .4)], estrellas=0)
    return [(far, 0.3)]


def brasas(img, t, n=N_E):
    for i in range(n):
        y = H - ((E_PH[i] + t * E_V[i]) % (H + 80)) + 40
        x = E_X[i] + 30 * math.sin(t * 1.3 + E_PH[i])
        g = 1 - (H - y) / (H + 80)
        cv2.circle(img, (int(x * 4), int(y * 4)), int(E_R[i] * (0.5 + 0.8 * g) * 4), (255, int(150 + 80 * g), int(40 + 80 * g)), -1, cv2.LINE_AA, 2)


SOPA = [K.quark("rojo", "miedo", "o"), K.electron("grandes", "grito"), K.proton("miedo", "grito"), K.quark("verde", "grandes", "o"),
        K.neutron("grandes", "o"), K.quark("azul", "miedo", "grito"), K.electron("miedo", "o"), K.proton("grandes", "o"),
        K.quark("rojo", "esfuerzo", "o")]


ESC_SOPA = [2.4, 2.0, 1.7, 2.4, 1.7, 2.4, 2.0, 1.7, 2.4]


@escena("calor")
def calor(C, t):
    from coreo_util import ORO  # noqa: F401
    t0 = INI("calor")
    capas = C.capas_de("calor", capas_calor)
    heat = prog(t, 8.15, 9.3)
    C.cam = (1.0 + 0.05 * prog(t, t0, FIN("calor")) + 0.03 * bump(t, 9.17, 0.5, 1.0), 9 * math.sin(t * 53) * heat, 7 * math.sin(t * 41 + 1) * heat)
    img = C.base("calor", capas)
    oscuro = 1 - prog(t, 7.95, 9.0)
    img = (img.astype(np.float32) * (1 - 0.94 * oscuro) + np.array((14, 10, 26), np.float32) * 0.94 * oscuro).astype(np.uint8)
    brasas(img, t)
    nv = e_out(prog(t, 8.3, 9.4))
    for k in range(7):
        x = 90 + k * 150 + 20 * math.sin(k * 3.1)
        P.mancha_din(img, x, H + 40 - 360 * nv * (0.8 + 0.25 * math.sin(k * 2.3)), 150, 210, (255, 128, 44), 0.8 * nv, k, t * 2, 0.16)
        P.mancha_din(img, x, H + 80 - 300 * nv * (0.8 + 0.25 * math.sin(k * 2.3)), 100, 150, (255, 214, 96), 0.7 * nv, k + 9, t * 2.6, 0.16)
    C.fondo(img)
    # --- A: bombilla dormida (no había luz)
    if t < 9.0:
        flick = 1 if (7.79 < t < 7.95 and int(t * 30) % 3 == 0) else 0
        C.pon(K.bombilla("dormido" if not flick else "grandes", "recta" if not flick else "o", flick), 540, 930, 2.3, 0.05 * math.sin(t * 2.2),
              t_in=t0 + 0.05, modo="pop", dur=0.4, t_out=8.2, d_out=0.35, sale="baja")
        for k in range(3):                                   # zZz: la bombilla duerme
            ph = ((t - t0) * 0.5 + k / 3) % 1.0
            C.rot("Z" if k != 1 else "z", 760 + 40 * math.sin(ph * 6 + k) + 30 * k, 760 - 330 * ph, 110 - 20 * k, 0.2 * math.sin(ph * 5), (170, 182, 214),
                  t_in=t0 + 0.4, dur=0.2, t_out=7.75, d_out=0.15, s=1 - 0.3 * ph)
        C.rot("AL PRINCIPIO", 540, 420, 100, -0.04, (210, 214, 232), t_in=6.89, t_out=8.2, d_out=0.3)
        C.rot("SIN LUZ", 540, 1420, 150, 0.03, (150, 160, 190), t_in=7.79, tira=True, t_out=8.1, d_out=0.15)
    # --- B: termómetro que revienta
    nivel = kf(t, [(8.15, 0.12), (9.17, 1.0)], e_inout)
    ojos = "esfuerzo" if t < 9.17 else "miedo"
    boca = "triste" if t < 8.9 else "grito"
    tr = prog(t, 9.75, 10.4)
    if 8.15 <= t < 10.4:
        shake = 6 * math.sin(t * 60) * prog(t, 8.6, 9.2)
        C.pon(K.termometro(round(nivel * 20) / 20, ojos, boca), 540 + shake, 1000 + 1000 * e_in(tr), 2.4 * (1 - 0.3 * tr), 0,
              t_in=8.15, modo="sube", dur=0.45, vida=1.0 + 1.5 * heat)
        if t > 8.3:
            for k in range(5):
                ph = ((t - 8.3) * 1.3 + k * 0.37) % 1.0
                C.pon(K.gota_sudor(), 540 + (-1) ** k * (90 + 30 * k) * (0.6 + ph), 980 + 300 * ph * ph + k * 12, 1.4 * (1 - ph * 0.4), 0)
        if t > 9.17:
            u = t - 9.17
            C.pon(K.CHISPA, 540 + 160 * u, 420 - 700 * u + 900 * u * u, 1.0, 6 * u)
            C.rot("¡IMPOSIBLE!", 540, 380, 120, -0.05, (255, 236, 130), t_in=9.17, dur=0.3, t_out=9.9, d_out=0.2)
        elif t < 9.17:
            C.rot("CALOR", 540, 330, 150, 0.03, (255, 236, 130), t_in=8.97, dur=0.3, t_out=9.17, d_out=0.05)
    # --- C: la olla de la sopa de partículas
    s_olla = e_out(prog(t, 9.8, 10.5))
    if t > 9.7:
        oy = 1330 + 700 * (1 - s_olla)
        py = oy - 10
        for i in range(9):
            per = 0.9
            tt = t - 10.0 - i * 0.37
            if tt < 0:
                continue
            u = (tt % per) / per
            ciclo = int(tt / per)
            ang = ((i * 53 + ciclo * 97) % 140 - 70) * pi / 180
            dist = 300 + 60 * ((i * 7 + ciclo * 3) % 5)
            x1 = 540 + math.sin(ang) * dist * 1.1
            x = 540 + (x1 - 540) * u
            y = py - 520 * 4 * u * (1 - u) + 120 * u * u - 20
            C.pon(SOPA[i], x, y, ESC_SOPA[i], 0.5 * math.sin(t * 6 + i) + (u - 0.5) * 2)
        C.pon(K.olla(), 540, oy, 2.5, 0.0, vida=0.5)
        for k, dx in enumerate((-230, -90, 70, 210)):
            C.pon(K.llama(t, 0, 0, 1.0, k), 540 + dx, oy + 330 + 6 * math.sin(t * 9 + k), 1.5 + 0.2 * math.sin(t * 7 + k), 0)
        C.rot("SOPA DE", 540, 380, 118, -0.04, (255, 236, 130), t_in=10.0, dur=0.3)
        C.rot("PARTÍCULAS", 540, 520, 118, 0.03, (255, 150, 90), t_in=10.35, dur=0.3, tira=True)
    return C.fin()


# =========================================================== 3. HIGGS
_r3 = np.random.default_rng(11)
N_P = 8
PA_FX = _r3.uniform(0.7, 1.9, (N_P, 2))
PA_PH = _r3.uniform(0, 6.28, (N_P, 2))
PA_C = _r3.uniform([200, 760], [880, 1300], (N_P, 2))
PA_A = _r3.uniform([140, 200], [300, 420], (N_P, 2))
REST = [(190, 1230), (540, 1210), (890, 1230), (360, 1450), (730, 1450), (170, 1680), (540, 1690), (910, 1680)]
TIPOS = [("proton",), ("quark", "rojo"), ("electron",), ("neutron",), ("quark", "verde"), ("electron",), ("proton",), ("quark", "azul")]
ESC_P = {"quark": 3.1, "electron": 2.7, "proton": 2.4, "neutron": 2.4}
RAD_P = {"quark": 27, "electron": 36, "proton": 48, "neutron": 45}
_gt = np.arange(0, 80, 1 / 120.0)
_f = 1 - 0.9 * np.array([smooth(prog(x, 14.55, 16.3)) for x in _gt])
TM = np.cumsum(_f) / 120.0
PESOS = [(17.30, 2), (17.52, 5), (17.74, 7), (17.96, 1), (18.18, 4), (18.34, 6)]
T_PESO = {idx: tc for tc, idx in PESOS}


def tm(t):
    return float(np.interp(t, _gt, TM))


def capas_higgs():
    far = P.cosmos(41, (150, 54, 36), (236, 120, 46), [(460, 0.6, (240, 150, 58), .55), (300, 1.0, (255, 196, 90), .45),
                                                      (220, 1.5, (255, 226, 140), .35)], estrellas=0)
    return [(far, 0.3)]


def pos_part(i, t):
    s = tm(t)
    cx, cy = PA_C[i]
    ax, ay = PA_A[i]
    x = cx + ax * math.sin(PA_FX[i, 0] * s * 3.2 + PA_PH[i, 0])
    y = cy + ay * math.sin(PA_FX[i, 1] * s * 3.0 + PA_PH[i, 1])
    k = e_inout(prog(t, 16.0, 17.1))
    return lerp(x, REST[i][0], k), lerp(y, REST[i][1], k)


def cara_part(i, t):
    if i in T_PESO and t >= T_PESO[i] + 0.25:
        return "esfuerzo", "triste"
    if t > 16.3:
        return "grandes", "o"
    if t < 14.55:
        return ("estrellas", "abierta") if i % 2 else ("grandes", "abierta")
    return "grandes", "o"


def dib_part(i, t):
    tp = TIPOS[i]
    o, b = cara_part(i, t)
    if tp[0] == "quark":
        return K.quark(tp[1], o, b)
    if tp[0] == "electron":
        return K.electron(o, b)
    if tp[0] == "proton":
        return K.proton(o, b)
    return K.neutron(o, b)


def miel_y(t):
    return lerp(2000, 470, e_out(prog(t, 14.62, 16.4))) - 150 * e_inout(prog(t, 19.0, 20.4))


@escena("higgs")
def higgs(C, t):
    t0 = INI("higgs")
    capas = C.capas_de("higgs", capas_higgs)
    C.cam = (1.0 + 0.05 * prog(t, t0, FIN("higgs")) + 0.05 * bump(t, 14.52, 0.5, 1.0) + 0.04 * bump(t, 20.22, 0.5, 1.0),
             8 * math.sin(t * 50) * pulso(t, 14.52, 0.4), 5 * math.sin(t * 43) * pulso(t, 14.52, 0.4))
    img = C.base("higgs", capas)
    brasas(img, t, 40)
    my = miel_y(t)
    if my < 1990:
        xs = np.linspace(-60, W + 60, 36)
        top = my + 24 * np.sin(xs / 80 + t * 2.0) + 10 * np.sin(xs / 33 - t * 3.1)
        poly = np.vstack([np.stack([xs, top], 1), [(W + 60, H + 60), (-60, H + 60)]])
        P.poligono(img, poly, (232, 164, 48), 0.95)
        P.poligono(img, np.vstack([np.stack([xs, top], 1), np.stack([xs[::-1], top[::-1] + 26], 1)]), (255, 214, 120), 0.7)
        P.poligono(img, np.vstack([np.stack([xs, top + 260 + 14 * np.sin(xs / 50)], 1), [(W + 60, H + 60), (-60, H + 60)]]), (190, 110, 30), 0.35)
        for k in range(14):
            bx = 80 + (k * 197) % 940
            by = H - ((t * (40 + (k % 5) * 14) + k * 211) % (H - my + 40))
            if by > my + 40:
                cv2.circle(img, (int(bx * 4), int(by * 4)), int((10 + (k % 4) * 5) * 4), (255, 226, 150), 3, cv2.LINE_AA, 2)
        for k in range(5):                         # remolinos de pincel en la miel
            cx_, cy_ = 150 + (k * 223) % 800, my + 160 + (k * 311) % 700
            a0 = t * (28 + 6 * k) * (1 if k % 2 else -1)
            cv2.ellipse(img, (int(cx_ * 4), int(cy_ * 4)), (int((120 + 30 * k) * 4), int(60 * 4)), 12 * k, a0, a0 + 130, (255, 214, 120), 9, cv2.LINE_AA, 2)
            cv2.ellipse(img, (int(cx_ * 4), int(cy_ * 4)), (int((120 + 30 * k) * 4), int(60 * 4)), 12 * k, a0 + 150, a0 + 210, (214, 138, 36), 7, cv2.LINE_AA, 2)
    C.fondo(img)
    # --- cronómetro y rótulo de la billonésima
    C.pon(K.cronometro(2 * pi * prog(t, 12.4, 14.4)), 820, 560, 1.9, 0.0, t_in=12.46, dur=0.4, t_out=14.45, d_out=0.3, vida=0.6)
    C.rot("UNA BILLONÉSIMA", 520, 300, 96, -0.04, (255, 246, 214), t_in=12.56, dur=0.3, t_out=14.45, d_out=0.25)
    C.rot("DE SEGUNDO", 520, 410, 96, 0.03, (255, 150, 90), t_in=13.24, dur=0.3, t_out=14.45, d_out=0.25, tira=True)
    # --- partículas
    for i in range(N_P):
        x, y = pos_part(i, t)
        d = dib_part(i, t)
        sq, dy = 0.0, 0.0
        if i in T_PESO and t >= T_PESO[i] + 0.2:
            sq = 0.22 * (1 - prog(t, T_PESO[i] + 0.2, T_PESO[i] + 0.5)) + 0.16
            dy = 12
        C.pon(d, x, y + dy, ESC_P[TIPOS[i][0]], 0.15 * math.sin(t * 5 + i) * (1 - prog(t, 16.3, 17.2)), sq=sq, t_in=t0 + 0.04 * i)
    # --- pesas que caen
    for (tc, idx) in PESOS:
        x, y = REST[idx]
        if t < tc - 0.05:
            continue
        tp = TIPOS[idx][0]
        rad = RAD_P[tp] * ESC_P[tp]
        v = prog(t, tc - 0.05, tc + 0.2)
        wy = lerp(-200, y + 12 - rad * 0.82 - 30, e_in(v))
        C.pon(K.pesa_rusa() if idx % 2 else K.mancuerna(), x, wy, 1.5, 0.0)
        if tc + 0.2 < t < tc + 0.7:
            C.rot("¡BONK!", x + 60, y - rad - 90 - 30 * prog(t, tc + 0.2, tc + 0.7), 66, -0.1, (255, 236, 130), t_in=tc + 0.2, dur=0.2,
                  t_out=tc + 0.55, d_out=0.15)
    C.rot("MASA", 520, 300, 170, -0.04, (255, 236, 130), t_in=17.92, dur=0.3, t_out=19.2, d_out=0.25, tira=True)
    # --- interruptor del campo de Higgs
    on = e_back(prog(t, 14.52, 14.72), 3.0)
    ax = lerp(-1.0, 1.0, min(1.0, max(0.0, on)))
    if 14.1 <= t < 16.8:
        C.pon(K.placa_interruptor(), 820, 1000, 2.0, 0.04, t_in=14.1, modo="sube", dur=0.45, t_out=16.4, d_out=0.35, sale="sube_fuera")
        C.pon(K.palanca(round(ax * 10) / 10), 820, 1000, 2.0, 0.04, t_in=14.1, modo="sube", dur=0.45, t_out=16.4, d_out=0.35, sale="sube_fuera")
        if 14.52 < t < 14.9:
            C.rot("¡CLIC!", 560, 700, 120, -0.12, (255, 236, 130), t_in=14.52, dur=0.2, t_out=14.85, d_out=0.15)
            C.pon(K.CHISPA5, 820, 900, 1.6, t * 6, t_in=14.52, modo="pop", dur=0.2, t_out=14.8, d_out=0.2)
    C.rot("CAMPO DE", 470, 330, 112, -0.04, (255, 246, 214), t_in=15.08, dur=0.3, t_out=16.4, d_out=0.25)
    C.rot("HIGGS", 470, 470, 160, 0.03, (255, 150, 90), t_in=15.5, dur=0.3, t_out=16.4, d_out=0.25, tira=True)
    # --- Foti pasa volando, sin peso
    if t > 18.7:
        x = kf(t, [(19.3, -360), (19.98, 540)], e_out)
        y = 900 + 30 * math.sin(t * 5) * (1 - prog(t, 19.9, 20.4))
        m = prog(t, 19.3, 19.98)
        C.foti(x, y, 2.4 + bump(t, 20.22, 0.4, 0.3), 0.0, "grandes" if t < 20.1 else "guino", "abierta" if t < 20.1 else "lengua", dur=0.2,
               largo=420 if m < 1 else 300, amp=26, sem=5)
        if t >= 20.22:
            C.rot("FOTÓN", 540, 400, 190, -0.04, (255, 236, 130), t_in=20.22, dur=0.3)
            C.rot("MASA: 0", 540, 560, 130, 0.03, (255, 246, 214), t_in=20.7, dur=0.3, tira=True)
            for j, (dx, dy, tt) in enumerate([(-330, -240, 20.3), (340, -260, 20.4), (-340, 220, 20.5), (350, 200, 20.6)]):
                C.pon(K.CHISPA, 540 + dx, 900 + dy + 8 * math.sin(t * 3 + j), 0.8, t * 0.5 + j, t_in=tt, modo="pop", dur=0.3)
    out = C.fin()
    g = pulso(t, 19.98, 0.3) * 0.3
    if g > 0.01:
        out = np.clip(out.astype(np.float32) * (1 - g) + 255 * g, 0, 255).astype(np.uint8)
    return out
