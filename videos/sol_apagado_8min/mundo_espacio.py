# -*- coding: utf-8 -*-
"""El espacio del plano secuencia: sistema solar esquemático, el Sol por dentro, la burbuja de luz que se
aleja, los planetas que se escapan, el viaje de escalas (vecindario -> galaxia) y el futuro del Sol.
Todo en coordenadas del mundo (Sol en el origen, 1 UA ≈ 1250 px) salvo las capas de gran escala, que se
dibujan en pantalla a partir de la cámara."""
import math

import numpy as np

import fondos as F
import plano as P
from plano import mezcla, aclarar
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, corazon
from mundo_comun import (SOL, SOL_R, PLANETAS, LUZ_UA, radio_de_tau, formato_tau, Cam, camino, interp_log, pop,
                         ventana, campana)
from anclas import A, D1, B0, BM, B1, D2, TOTAL

ER = PLANETAS["tierra"][2]
UA_PX = 1250.0
AL_PX = 63241.0 * UA_PX              # un año luz en px del mundo
OMEGA0 = 0.012


def omega(R):
    return OMEGA0 * (1250.0 / R) ** 1.5


# ======================================================================== tiempo real desde la desaparición
_TAU = [(A.ahora, 0.0), (A.mercurio, 0.387 * LUZ_UA), (A.venus, 0.723 * LUZ_UA), (A.alcanza, LUZ_UA),
        (A.jupiter, 5.203 * LUZ_UA), (A.neptuno, 30.07 * LUZ_UA)]
_TS = [a for a, _ in _TAU]
_VS = [b for _, b in _TAU]


def tau(t):
    if t < A.ahora:
        return -1.0
    if t <= _TS[-1]:
        return float(np.interp(t, _TS, _VS))
    return _VS[-1] * 2 ** ((t - _TS[-1]) / 1.3)


def radio_burbuja(t):
    return radio_de_tau(max(0.0, tau(t)))


T_LIB = {n: float(np.interp(ua * LUZ_UA, _VS, _TS)) for n, (ua, R, pr, th0) in PLANETAS.items()}


def pos_planeta(nombre, t, libre=True):
    ua, R, pr, th0 = PLANETAS[nombre]
    w = omega(R)
    tl = T_LIB[nombre] if libre else 1e12
    if t <= tl:
        th = th0 - w * t
        return SOL + R * np.array([math.cos(th), math.sin(th)])
    th = th0 - w * tl
    p0 = SOL + R * np.array([math.cos(th), math.sin(th)])
    u = t - tl
    v = R * w
    s = v * u + 2.0 * v * (u - 2.0 * (1 - math.exp(-u / 2.0)))     # acelera de v a 3v (cámara rápida)
    return p0 + np.array([math.sin(th), -math.cos(th)]) * s


def tierra_pos(t, libre=True):
    return pos_planeta("tierra", t, libre)


def luz_planeta(nombre, t, libre=True):
    if not libre:
        return 1.0
    return 1.0 - e_inout(prog(t, T_LIB[nombre], T_LIB[nombre] + 0.5))


def luna_pos(E, t):
    a = 0.22 * t + 1.0
    return E + 190 * np.array([math.cos(a), 0.42 * math.sin(a)]), math.sin(a) >= 0


def sol_visible(t):
    """1 = Sol entero; 0 = desaparecido. Incluye el 'ensayo' de la intro (se apaga y vuelve)."""
    ensayo = e_inout(prog(t, A.apaga, A.apaga + 0.6)) * (1 - e_out(prog(t, A.imposible, A.imposible + 0.7)))
    real = e_in(prog(t, A.ahora, A.ahora + 0.5))
    return 1.0 - max(ensayo, real)


# ======================================================================== cámara del espacio 1
def _cam_amplia(t, z=0.55, frac=0.5, pant=(960.0, 560.0)):
    E = tierra_pos(t)
    return Cam(E * frac, pant, z)


def _cam_tierra(t, z=1.2, pant=(1030.0, 580.0)):
    return Cam(tierra_pos(t), pant, z)


def _cam_sol(t, z=1.25, pant=(960.0, 620.0)):
    return Cam(SOL, pant, z)


def _cam_nucleo(t):
    z = interp_log(t, [(A.segundo - 0.2, 1.25), (A.seiscientos + 0.4, 11.0), (A.luz_s - 1.4, 12.5)])
    return Cam(SOL, (960.0, 540.0), z)


def _cam_sistema(t):
    return Cam(np.array([300.0, -200.0]), (960.0, 560.0), interp_log(t, [(A.jupiter - 1.2, 0.3), (A.jupiter + 1.5, 0.085),
                                                                           (A.collar + 4, 0.075)]))


# galaxia: el Sol está a 0,62 radios del centro, en el ángulo PHI_SOL de la galaxia dibujada
R_GAL = 50000 * AL_PX
INCL = 0.5
PHI_SOL = 2.35


def centro_galaxia(t):
    E = tierra_pos(t)
    rho = 0.62
    off = R_GAL * rho * np.array([math.cos(PHI_SOL), math.sin(PHI_SOL) * INCL])
    return E - off


# estrellas vecinas: (nombre, años luz, ángulo en pantalla, radio visual px, color)
VECINAS = [("Alfa Centauri", 4.24, -0.35, 7.0, (255, 236, 196)), ("Barnard", 5.96, 2.3, 4.0, (255, 170, 140)),
           ("Wolf 359", 7.86, 1.2, 3.5, (255, 160, 130)), ("Lalande", 8.3, -2.1, 4.5, (255, 190, 160)),
           ("Sirio", 8.6, 0.55, 9.0, (200, 220, 255)), ("Luyten", 8.7, -1.3, 3.0, (255, 170, 140)),
           ("Ross 154", 9.7, 2.9, 3.5, (255, 175, 140)), ("Épsilon Eridani", 10.5, -2.7, 5.0, (255, 214, 170)),
           ("Procyon", 11.4, 0.1, 7.5, (240, 240, 255)), ("61 Cygni", 11.4, -0.9, 4.5, (255, 200, 160))]
_RNG_ERR = np.random.default_rng(12)
ERRANTES = [(4 + 14 * _RNG_ERR.random() ** 0.8, _RNG_ERR.random() * 2 * np.pi) for _ in range(46)]


def _cam_escala(t):
    """Viaje de escalas centrado en la Tierra: sistema -> vecindario -> galaxia -> vecindario -> Tierra."""
    E = tierra_pos(t)
    z = interp_log(t, [(A.treinta - 0.8, 0.5), (A.estrella - 1.2, 0.34), (A.estrella + 1.6, 1.3e-6),
                       (A.cuarenta + 2.0, 1.1e-6), (A.galaxia + 1.4, 1.15e-10), (A.chocar - 0.2, 1.1e-10),
                       (A.chocar + 1.6, 9e-7), (A.gigantesco + 0.5, 8e-7), (A.errante - 0.4, 0.9),
                       (A.solos - 0.4, 0.8), (A.solos + 1.3, 4.5e-7), (A.lactea + 0.9, 4.2e-7),
                       (D1[0] - 0.6, 0.95), (D1[0], 1.0)])
    # a escala galáctica, centrar la galaxia (la Tierra queda a un lado)
    u = e_inout(prog(-math.log10(z), 9.2, 9.9))
    GC = centro_galaxia(t)
    pant = np.array([960.0, 560.0]) + u * z * (E - GC)
    return Cam(E, pant, z)


def cam_espacio1(t):
    tramos = [
        (0.0, A.cuanto - 0.7, lambda t: _cam_amplia(t, 0.5 + 0.04 * prog(t, 0, A.cuanto))),
        (A.cuanto + 0.3, A.imposible + 0.6, lambda t: _cam_tierra(t, 1.25, (1060.0, 560.0))),
        (A.sol_i + 0.4, A.superficie - 0.9, lambda t: _cam_sol(t, 1.25, (960.0, 640.0))),
        (A.superficie - 0.2, A.segundo - 0.4, lambda t: _cam_sol(t, 1.3, (820.0, 600.0))),
        (A.segundo - 0.2, A.luz_s - 1.4, _cam_nucleo),
        (A.luz_s + 0.4, A.ahora - 0.4, lambda t: _cam_amplia(t, 0.55)),
        (A.ahora + 0.2, A.vez + 1.0, lambda t: _cam_amplia(t, 0.4, 0.5, (1000.0, 600.0))),
        (A.alcanza - 0.4, A.luna_d + 3.4, lambda t: _cam_tierra(t, 1.05, (1000.0, 600.0))),
        (A.jupiter - 1.2, A.collar + 3.5, _cam_sistema),
        (A.treinta - 0.8, D1[0], _cam_escala),
    ]
    return camino(t, tramos)


def cam_espacio2(t):
    """Después del brillo: del núcleo del Sol hacia fuera; realidad y futuro."""
    base = Cam(np.array([520.0, -90.0]), (960.0, 560.0), 0.55)
    tramos = [
        (BM, B1, lambda t: Cam(SOL, (960.0, 560.0) + (base.a_pant(SOL) - np.array([960.0, 560.0])) * e_out(prog(t, BM, B1)),
                               interp_log(t, [(BM, 9.0), (B1, 0.55)]))),
        (B1 + 0.1, A.luz_r - 1.0, lambda t: base),
        (A.luz_r - 0.4, A.detuviera + 0.6, lambda t: Cam(SOL + np.array([120.0, -80.0]), (900.0, 600.0), 1.35)),
        (A.neutrinos - 0.3, A.neutrinos + 3.2, lambda t: Cam(np.array([500.0, -100.0]), (960.0, 560.0), 0.5)),
        (A.cambiara - 0.4, A.gigante - 0.8, lambda t: Cam(tierra_pos(t, False) * 0.42, (960.0, 470.0), 0.44)),
        (A.gigante + 0.6, A.fin, lambda t: Cam(tierra_pos(t, False) * 0.3, (960.0, 470.0), 0.33)),
    ]
    return camino(t, tramos)


def cam_inmersion(t, d, cam_fn, pos_fn):
    """Cámara que cae hacia el borde superior de la Tierra: (cam, radio de la Tierra en pantalla, u)."""
    u = prog(t, *d)
    c0 = cam_fn(d[0])
    L = pos_fn(t) + np.array([0.0, -ER])
    L0 = pos_fn(d[0]) + np.array([0.0, -ER])
    p0 = c0.a_pant(L0)
    ue = e_inout(u)
    z = math.exp(lerp(math.log(c0.z), math.log(520.0), e_in(u) * 0.35 + ue * 0.65))
    p = p0 + (np.array([960.0, 700.0]) - p0) * ue
    return Cam(L, p, z), ER * z, u


# ======================================================================== dibujo: capas del espacio
def fondo_espacio(t, cam, brillo=1.0):
    return F.espacio(t, brillo_est=brillo, dx=-cam.ancla[0] * 0.03 * min(cam.z, 3), dy=-cam.ancla[1] * 0.03 * min(cam.z, 3))


def _orbitas(lz, t, cam, modo):
    if not (0.02 < cam.z < 2.6):
        return
    for nombre, (ua, R, pr, th0) in PLANETAS.items():
        a = 0.5
        rotura = 0.0
        if modo == 1 and t > A.ahora:
            a = 0.5 - 0.3 * prog(t, T_LIB[nombre], T_LIB[nombre] + 1.5)
            rotura = e_in(prog(t, A.collar - 0.6, A.collar + 2.6))
        if a <= 0.02 or rotura >= 0.99:
            continue
        if rotura > 0.01:
            a = 0.55
        col = mezcla((18, 18, 54), (150, 160, 230), a * (1 - rotura ** 2))
        if rotura <= 0.01:
            P.discontinua(lz, P.arco_pts(0, 0, R, 0, 2 * np.pi, 480), col, 3.0 / max(cam.z, 0.15) * 0.6, 22, 18,
                          fase=t * 8)
        else:   # el "collar" se rompe: los trozos de órbita se abren y se alejan
            for k in range(12):
                a0 = k / 12 * 2 * np.pi + 0.1
                a1 = a0 + (2 * np.pi / 12) * (1 - 0.7 * rotura)
                rr = R * (1 + 0.25 * rotura)
                P.discontinua(lz, P.arco_pts(0, 0, rr, a0, a1, 40), col, 3.0 / max(cam.z, 0.15) * 0.6, 22, 18)


def _sol_y_fantasma(lz, t, vis, extra_corte=0.0, nucleo=1.0, brillo=1.0):
    if vis > 0.002:
        r = SOL_R * (0.12 + 0.88 * e_out(vis))
        if extra_corte > 0.01:
            P.sol_corte(lz, 0, 0, r, t, apertura=extra_corte, nucleo=nucleo, brillo=brillo * vis)
        else:
            P.sol(lz, 0, 0, r, t, brillo=brillo * vis)
    if vis < 0.998:
        a = (1 - vis) * 0.55
        P.discontinua(lz, P.arco_pts(0, 0, SOL_R, 0, 2 * np.pi, 160), mezcla((18, 16, 50), (170, 160, 230), a), 4, 16, 14,
                      fase=t * 6)


def _burbuja(lz, t, cam):
    if t < A.ahora:
        return
    r = radio_burbuja(t)
    if r * cam.z > 9000:
        return
    a_on = e_out(prog(t, A.ahora, A.ahora + 0.5)) * (1 - prog(t, A.collar + 1.0, A.collar + 3.0))
    if a_on <= 0.01:
        return
    esc = 1 / max(cam.z, 0.05)
    # luz "vieja": rayas que viajan por delante de la burbuja (fuera de ella todavía hay luz)
    k = np.arange(90)
    ang = (k * 2.39996) % (2 * np.pi)
    off = 40 + (k * 37 % 23) * 26
    for a_, o in zip(ang[::2], off[::2]):
        rr = r + o * esc * 0.6
        p0 = np.array([math.cos(a_), math.sin(a_)])
        lz.trazo(np.array([p0 * rr, p0 * (rr + 26 * esc)]), (255, 214, 140), 3.2 * esc, afinar=False)
    P.onda(lz, 0, 0, r, 34 * esc, (255, 196, 110), alfa=0.95 * a_on)
    ag = e_out(prog(t, A.grav_o - 0.4, A.grav_o + 0.6)) * a_on
    for j in range(3):
        P.onda(lz, 0, 0, r - (40 + 34 * j) * esc, 7 * esc, (170, 130, 255), alfa=(0.25 + 0.5 * ag) * (1 - 0.25 * j) * a_on,
               frente=0.6, estela=0.6)


def _rayos_luz(lz, t, E, a):
    """Destellos que viajan del Sol a la Tierra (luz y calor)."""
    if a <= 0.01:
        return
    d = E - SOL
    L = np.linalg.norm(d)
    u = d / L
    n = np.array([-u[1], u[0]])
    for k in range(14):
        f = ((t * 0.55 + k / 14) % 1.0)
        p = SOL + u * (SOL_R + f * (L - SOL_R - ER)) + n * (k % 5 - 2) * 30
        lz.trazo(np.array([p, p + u * 60]), mezcla((20, 20, 50), (255, 222, 150), a), 6, afinar=False)


def _planetas(lz, t, cam, modo, tf=None):
    tf = t if tf is None else tf
    libre = modo == 1
    for nombre, (ua, R, pr, th0) in PLANETAS.items():
        if nombre == "tierra":
            continue
        p = pos_planeta(nombre, t, libre)
        if not cam.visible(p, pr * 2.4):
            continue
        if modo == 1 and t > A.treinta - 1.0:     # en el viaje errante solo seguimos a la Tierra
            continue
        rr = max(pr, 11.0 / max(cam.z, 1e-6))
        luzp = luz_planeta(nombre, t, libre)
        if luzp < 0.95:
            lz.relleno(circulo(p[0], p[1], rr * 1.14, 40), mezcla((20, 20, 50), (130, 118, 214), 0.8 * (1 - luzp)))
        if libre and t > T_LIB[nombre] + 0.2 and t > A.jupiter - 1.0:   # estela del escape
            p0 = pos_planeta(nombre, T_LIB[nombre] + 0.01)
            P.discontinua(lz, [p0, p], mezcla((20, 20, 50), (170, 160, 240), 0.55), 3.0 / max(cam.z, 0.05),
                          16 / max(cam.z, 0.05), 12 / max(cam.z, 0.05))
        if modo == 3:    # futuro: la gigante roja se traga a Mercurio y Venus
            if radio_sol_futuro(tf) > R * 0.98 and nombre in ("mercurio", "venus"):
                continue
        P.planeta(lz, p[0], p[1], rr, nombre, t, luz=luzp,
                  ang_luz=math.atan2(-p[1], -p[0]))


def _tierra_y_luna(lz, t, cam, modo, atm=1.0, tf=None):
    tf = t if tf is None else tf
    libre = modo == 1
    E = tierra_pos(t, libre)
    if not cam.visible(E, ER * 3):
        return E
    luz = luz_planeta("tierra", t, libre)
    L, delante = luna_pos(E, t)
    ang = math.atan2(-E[1], -E[0])
    if not delante:
        P.luna(lz, L[0], L[1], 27, math.atan2(-L[1], -L[0]), luz)
    ciud = prog(t, T_LIB["tierra"] + 0.2, T_LIB["tierra"] + 1.2) * (1 - prog(cam.z, 2.5, 6.0)) if libre else 0.0
    seca = e_inout(prog(tf, A.mil_f - 0.2, A.oceanos_fu + 0.6)) if modo == 3 else 0.0
    P.tierra(lz, E[0], E[1], ER, t, rot=0.6 + 0.06 * t, ang_luz=ang, luz=luz, ciudades=ciud, atmosfera=atm * (1 - seca),
             nubes=(1 - prog(cam.z, 3.0, 9.0)) * (1 - seca))
    if seca > 0.01:
        lz.relleno(circulo(E[0], E[1], ER, 120), (176, 120, 84), alfa=0.72 * seca)
        calc = e_inout(prog(tf, A.calcinada - 0.6, A.calcinada + 0.8))
        if calc > 0.01:
            lz.relleno(circulo(E[0], E[1], ER, 120), (96, 40, 38), alfa=0.8 * calc)
            lz.halo(E[0], E[1], ER * 1.3, (255, 90, 40), alfa=0.35 * calc)
    if delante:
        P.luna(lz, L[0], L[1], 27, math.atan2(-L[1], -L[0]), luz)
    return E


# ---- detalles del Sol: Tierras dentro, núcleo, fusión
def _tierras_dentro(lz, t):
    a = ventana(t, A.millon - 0.2, A.noventa - 0.6, 0.4, 0.5)
    if a <= 0.01:
        return
    barrido = e_inout(prog(t, A.millon - 0.2, A.tierras + 1.0))
    paso = 20.0
    xs = np.arange(-SOL_R, SOL_R, paso)
    pts = []
    for j, y in enumerate(np.arange(-SOL_R, SOL_R, paso * 0.866)):
        off = (j % 2) * paso / 2
        for x in xs + off:
            if x * x + y * y < (SOL_R - 6) ** 2 and (x + SOL_R) / (2 * SOL_R) < barrido:
                pts.append((x, y))
    if pts:
        pts = np.array(pts)
        lz.puntos(pts, 7.5, mezcla((255, 180, 80), (60, 132, 230), a))
        lz.puntos(pts + [-1.6, -1.8], 3.4, mezcla((255, 180, 80), (110, 206, 120), a))
        lz.puntos(pts + [2.6, 1.4], 2.2, mezcla((255, 180, 80), (110, 206, 120), a))


def _fusion(lz, t):
    """Protones que chocan y se fusionan en el núcleo (se ve con zoom al centro del Sol)."""
    a = ventana(t, A.segundo, A.luz_s - 1.0, 0.8, 0.8)
    if a <= 0.01:
        return
    rc = SOL_R * 0.23
    rng = np.random.default_rng(5)
    base = rng.random((70, 4))
    for i, (u, v, fu, fv) in enumerate(base):   # hidrógeno que se agita
        x = (u - 0.5) * 2 * rc + 3 * math.sin(t * (2 + fu * 3) + i)
        y = (v - 0.5) * 2 * rc + 3 * math.cos(t * (2 + fv * 3) + i * 1.3)
        if x * x + y * y > rc * rc:
            continue
        lz.relleno(circulo(x, y, 1.6, 16), mezcla((255, 246, 210), (255, 96, 96), a))
    for k in range(40):   # fusiones: dos protones se juntan, destello, sale un fotón
        te = A.segundo + 0.2 + k * 0.23
        if not (te - 0.6 < t < te + 1.6):
            continue
        r_ = rng.random(3) if False else np.array([h01v(k, 1), h01v(k, 2), h01v(k, 3)])
        cx, cy = (r_[0] - 0.5) * rc * 1.4, (r_[1] - 0.5) * rc * 1.4
        ang = r_[2] * 2 * np.pi
        if t < te:
            d = 9 * (1 - e_in(prog(t, te - 0.6, te)))
            for sgn in (-1, 1):
                lz.relleno(circulo(cx + sgn * d * math.cos(ang), cy + sgn * d * math.sin(ang), 1.6, 16), (255, 96, 96))
        else:
            u_ = prog(t, te, te + 0.3)
            lz.halo(cx, cy, 7 * (1 - 0.5 * u_), (255, 250, 220), alfa=(1 - u_) * a)
            lz.relleno(circulo(cx, cy, 2.3, 16), (255, 236, 120))
            if t > A.cuatro - 0.3:   # la masa que falta sale como energía (fotón)
                f = prog(t, te, te + 1.6)
                px = cx + math.cos(ang * 3) * 40 * f + 4 * math.sin(f * 30)
                py = cy + math.sin(ang * 3) * 40 * f + 4 * math.cos(f * 30)
                lz.halo(px, py, 5, (255, 230, 120), alfa=0.9 * (1 - f) * a)


def h01v(k, c):
    return (math.sin(k * 12.9898 + c * 78.233) * 43758.5453) % 1.0


def _etiquetas_sol(lz, t, cam):
    """Rótulos del Sol (en pantalla)."""
    a = ventana(t, A.superficie, A.segundo - 0.5, 0.3, 0.4)
    if a > 0.01:
        p = cam.a_pant(SOL + SOL_R * np.array([math.cos(-0.15), math.sin(-0.15)]))
        P.linea_llamada(lz, p, p + np.array([150, -40]), frac=a)
        P.rotulo(lz, p[0] + 160, p[1] - 40, "superficie ≈ 5 500 °C", 40, alfa=a, ancla=(0, 0.5))
    a = ventana(t, A.nucleo_s, A.segundo - 0.5, 0.3, 0.4)
    if a > 0.01:
        p = cam.a_pant(SOL + SOL_R * 0.12 * np.array([math.cos(-0.55), math.sin(-0.55)]))
        P.linea_llamada(lz, p, p + np.array([470, 150]), frac=a)
        P.rotulo(lz, p[0] + 480, p[1] + 150, "núcleo ≈ 15 millones °C", 40, alfa=a, ancla=(0, 0.5), color=(255, 240, 200))


# ---- vecindario y galaxia (en pantalla)
def _gran_escala(lz, t, cam):
    z = cam.z
    E = tierra_pos(t)
    c = cam.a_pant(E)
    # galaxia
    GC = centro_galaxia(t)
    Rg = R_GAL * z
    ag = prog(-math.log10(max(z, 1e-15)), 7.6, 9.0)
    if ag > 0.01 and Rg < 60000:
        g = cam.a_pant(GC)
        P.galaxia(lz, g[0], g[1], Rg, t, rot=-PHI_SOL + PHI_SOL + t * 0.004, inclin=INCL, alfa=ag)
        if ag > 0.5:
            a2 = ventana(t, A.galaxia - 0.3, A.chocar - 0.2, 0.5, 0.5)
            P.discontinua(lz, np.stack([g[0] + Rg * 0.62 * np.cos(np.linspace(0, 2 * np.pi, 200)),
                                        g[1] + Rg * 0.62 * INCL * np.sin(np.linspace(0, 2 * np.pi, 200))], 1),
                          mezcla((20, 20, 50), (200, 200, 255), 0.6 * a2), 3, 14, 12, fase=-t * 20)
            P.rotulo(lz, g[0], g[1] - 34, "centro de la galaxia", 34, fuente="geo_n", alfa=a2, color=(255, 230, 190))
    # vecindario: estrellas cercanas
    av = prog(-math.log10(max(z, 1e-15)), 3.0, 5.2) * (1 - prog(-math.log10(max(z, 1e-15)), 7.6, 8.6))
    if av > 0.01:
        for i, (nom, al, ang, rv, col) in enumerate(VECINAS):
            p = c + al * AL_PX * z * np.array([math.cos(ang), math.sin(ang)])
            if not (-100 < p[0] < W + 100 and -100 < p[1] < H + 100):
                continue
            lz.halo(p[0], p[1], rv * 5, col, alfa=0.55 * av)
            lz.relleno(circulo(p[0], p[1], rv, 20), mezcla((20, 20, 50), aclarar(col, 0.5), av))
        # Alfa Centauri: distancia
        a1 = ventana(t, A.estrella - 0.2, A.galaxia - 1.0, 0.4, 0.5)
        if a1 > 0.01:
            nom, al, ang, rv, col = VECINAS[0]
            p = c + al * AL_PX * z * np.array([math.cos(ang), math.sin(ang)])
            P.discontinua(lz, [c, p], mezcla((20, 20, 50), (255, 236, 196), a1), 3, 16, 12, fase=-t * 30)
            P.rotulo(lz, p[0], p[1] - 40, "Alfa Centauri · 4,2 años luz", 36, alfa=a1)
            a2 = ventana(t, A.cuarenta - 0.2, A.galaxia - 1.0, 0.3, 0.5)
            m = (c + p) / 2
            P.pastilla(lz, m[0], m[1] + 95, "a 30 km/s: más de 40 000 años", 34, k=e_back(min(1, a2 * 1.2)) if a2 > 0 else 0)
        # espacio entre estrellas
        a3 = ventana(t, A.chocar + 0.6, A.errante - 1.4, 0.4, 0.4)
        if a3 > 0.01:
            for (nom, al, ang, rv, col), txt in zip(VECINAS[:3], ("4,2", "6,0", "7,9")):
                p = c + al * AL_PX * z * np.array([math.cos(ang), math.sin(ang)])
                P.discontinua(lz, [c, p], mezcla((20, 20, 50), (190, 196, 240), a3), 2.5, 12, 12)
                m = c + (p - c) * 0.55
                P.rotulo(lz, m[0], m[1] - 18, f"{txt} años luz", 28, fuente="geo_n", alfa=a3, color=(200, 206, 245))
        # planetas errantes
        a4 = ventana(t, A.solos - 0.2, D1[0] - 1.8, 0.8, 0.6)
        if a4 > 0.01:
            for i, (al, ang) in enumerate(ERRANTES):
                s_ = e_back(prog(t, A.solos + 0.03 * i, A.solos + 0.03 * i + 0.4))
                if s_ <= 0.01:
                    continue
                p = c + al * AL_PX * z * np.array([math.cos(ang), math.sin(ang)])
                if not (-40 < p[0] < W + 40 and -40 < p[1] < H + 40):
                    continue
                rr = 9 * s_ * min(1.0, a4 * 1.5)
                lz.relleno(circulo(p[0], p[1], rr * 1.25, 20), mezcla((20, 20, 50), (130, 110, 210), a4))
                lz.relleno(circulo(p[0], p[1], rr, 20), (24, 22, 52))
            P.pastilla(lz, 960, 170, "planetas errantes", 36, k=a4 * (1 - prog(t, A.lactea + 0.6, A.lactea + 1.1)),
                       fondo=(130, 110, 210), color=(255, 255, 255))
    # marcador "nosotros" a escalas grandes
    am = prog(-math.log10(max(z, 1e-15)), 2.2, 4.0)
    if am > 0.01:
        lz.relleno(circulo(c[0], c[1], 6, 16), mezcla((20, 20, 50), (120, 200, 255), am))
        P.onda(lz, c[0], c[1], 18 + 4 * math.sin(t * 3), 3, (120, 200, 255), alfa=0.8 * am, frente=0.6, estela=0.6)
        P.rotulo(lz, c[0] + 26, c[1] - 26, "nosotros", 30, fuente="geo_n", alfa=am, ancla=(0, 0.5),
                 color=(170, 220, 255))


# ---- 2017: choque de estrellas de neutrones (ventana circular)
def ui_2017(lz, t):
    k = pop(t, A.diecisiete - 0.2, 0.4) * (1 - e_in(prog(t, FIN_OCHO + 0.3, FIN_OCHO + 0.8)))
    if k <= 0.01:
        return
    cx, cy, R = 1480.0, 390.0, 220.0 * k
    with lz.capa(2):
        lz.relleno(circulo(cx, cy, R + 8, 90), (255, 255, 255), alfa=0.9)
        lz.relleno(circulo(cx, cy, R, 90), (16, 14, 44))
        with lz.recorte(circulo(cx, cy, R, 90)):
            u = prog(t, A.diecisiete, A.choque + 0.3)
            sx, sy = cx - 120 * k, cy
            if u < 1:     # espiral de dos estrellas de neutrones
                d = 40 * (1 - u) ** 0.7 * k + 2
                a = u * 40
                for sgn in (-1, 1):
                    P.estrella_neutrones(lz, sx + sgn * d * math.cos(a), sy + sgn * d * math.sin(a), 6 * k)
            else:
                v = prog(t, A.choque + 0.3, A.vez + 0.2)
                lz.halo(sx, sy, 60 * k * (1 - 0.6 * v), (255, 200, 150), alfa=1 - 0.7 * v)
                rr = v * 230 * k
                P.onda(lz, sx, sy, rr, 10 * k, (255, 206, 120), alfa=0.9, frente=0.5, estela=1.0)
                for j in range(3):
                    P.onda(lz, sx, sy, rr - (14 + 12 * j) * k, 3 * k, (170, 130, 255), alfa=0.8, frente=0.6, estela=0.6)
            P.tierra(lz, cx + 150 * k, cy + 10 * k, 16 * k, t, luz=1.0, atmosfera=0.5, nubes=0.5)
    P.rotulo(lz, cx, cy - R - 34, "2017", 44 * max(k, 0.3), alfa=min(1, k))
    P.rotulo(lz, cx, cy + R + 30, "a 130 millones de años luz", 30 * max(k, 0.3), fuente="geo_n", alfa=min(1, k),
             color=(210, 214, 245))


from mundo_comun import FIN as _FIN   # noqa: E402
FIN_OCHO = _FIN("ocho")


# ---- futuro del Sol
def radio_sol_futuro(t):
    g = e_inout(prog(t, A.gigante - 0.8, A.gigante + 2.4))
    enc = e_inout(prog(t, A.enana - 0.3, A.enana + 1.6))
    r = SOL_R * (1 + 0.1 * prog(t, A.mil_f - 0.4, A.mil_f + 1.5)) + g * (1300 - SOL_R)
    return lerp(r, 34.0, enc)


def _sol_futuro(lz, t):
    g = e_inout(prog(t, A.gigante - 0.8, A.gigante + 2.4))
    enc = e_inout(prog(t, A.enana - 0.3, A.enana + 1.6))
    r = radio_sol_futuro(t)
    if g < 0.01:
        P.sol(lz, 0, 0, r, t, brillo=1.0 + 0.4 * prog(t, A.mil_f - 0.4, A.mil_f + 1.5))
        return
    if enc < 0.99:   # gigante roja
        a = 1 - enc
        lz.halo(0, 0, r * 2.2, (255, 90, 60), alfa=0.35 * a)
        lz.halo(0, 0, r * 1.35, (255, 120, 80), alfa=0.5 * a, r0=0.5)
        n = 220
        th = np.linspace(0, 2 * np.pi, n, endpoint=False)
        rr = r * (1 + 0.025 * np.sin(th * 7 + t) + 0.015 * np.sin(th * 13 - t * 1.4))
        lz.relleno(np.stack([rr * np.cos(th), rr * np.sin(th)], 1), mezcla((238, 88, 60), (255, 160, 90), 0.3 * enc),
                   alfa=a)
        lz.relleno(circulo(-r * 0.08, -r * 0.08, r * 0.78, 160), (250, 118, 72), alfa=a)
        lz.relleno(circulo(-r * 0.16, -r * 0.16, r * 0.5, 120), (255, 150, 92), alfa=a)
    if enc > 0.01:   # nebulosa planetaria + enana blanca
        v = prog(t, A.enana - 0.3, A.enana + 4.0)
        for j, col in enumerate(((120, 220, 255), (255, 120, 200), (160, 140, 255))):
            P.onda(lz, 0, 0, 200 + v * (700 + 260 * j), 40, col, alfa=0.7 * enc * (1 - 0.6 * v), frente=0.8, estela=1.6)
        b = 1 - 0.55 * prog(t, A.billones - 0.5, A.billones + 3.0)
        lz.halo(0, 0, 160, (200, 220, 255), alfa=0.8 * enc * b)
        lz.relleno(circulo(0, 0, 30, 40), mezcla((120, 130, 170), (250, 252, 255), b), alfa=enc)


def ui_linea_futuro(lz, t):
    a = ventana(t, A.cambiara - 0.3, A.amanecer_c + 1.4, 0.5, 0.6)
    if a <= 0.01:
        return
    x0, x1, y = 460.0, 1460.0, 118.0
    hitos = [("hoy", 0.0), ("+1 000 M años", 0.3), ("+5 000 M años", 0.62), ("billones de años", 0.95)]
    pos = 0.0
    for tt, v in ((A.mil_f, 0.3), (A.cinco_f, 0.62), (A.billones, 0.95)):
        pos = max(pos, v * e_inout(prog(t, tt - 0.3, tt + 0.6)))
    pos *= 1 - e_inout(prog(t, A.amanecer_c - 1.2, A.amanecer_c + 0.2))    # rebobinar a hoy
    with lz.capa(2):
        lz.relleno(rect_red(x0, y - 5, x1 - x0, 10, 5), (255, 255, 255), alfa=0.25 * a)
        lz.relleno(rect_red(x0, y - 5, (x1 - x0) * pos + 10, 10, 5), (255, 200, 110), alfa=a)
        xp = x0 + (x1 - x0) * pos
        lz.relleno(circulo(xp, y, 13, 24), (255, 255, 255), alfa=a)
    for nom, v in hitos:
        xh = x0 + (x1 - x0) * v
        on = pos >= v - 0.01
        P.rotulo(lz, xh, y + 42, nom, 28 if v else 30, fuente="geo_n", alfa=a * (1.0 if on else 0.5),
                 color=(255, 230, 170) if on else (200, 204, 235))


# ======================================================================== dibujo principal del espacio
def dibujar_espacio(lz, t, cam, modo, atm=1.0, tf=None):
    """modo 1: el Sol desaparece (intro..errante). modo 2: realidad (Sol normal). modo 3: futuro del Sol."""
    lz.M = cam.matriz()
    z = cam.z
    if z > 1e-4:
        _orbitas(lz, t, cam, modo)
        if modo == 1:
            corte = e_inout(prog(t, A.superficie - 0.3, A.superficie + 0.8)) * (1 - e_inout(prog(t, A.luz_s - 1.4, A.luz_s)))
            corte = corte * (1 + 2.7 * e_inout(prog(t, A.segundo - 0.2, A.seiscientos + 0.2)))
            _burbuja(lz, t, cam)
            if cam.visible(SOL, SOL_R * 2):
                _sol_y_fantasma(lz, t, sol_visible(t), extra_corte=corte)
                with lz.recorte(circulo(0, 0, SOL_R * 0.999, 160)):
                    _tierras_dentro(lz, t)
                if z > 3:
                    _fusion(lz, t)
            E = tierra_pos(t)
            _rayos_luz(lz, t, E, ventana(t, A.luz_s - 0.3, A.ahora - 0.2, 0.6, 0.3))
        elif modo == 2:
            corte = e_inout(prog(t, A.luz_r - 0.2, A.luz_r + 0.8)) * (1 - e_inout(prog(t, A.neutrinos - 0.4, A.neutrinos + 0.4)))
            nuc = 1 - e_inout(prog(t, A.detuviera - 0.2, A.detuviera + 1.0))
            nuc = max(nuc, e_inout(prog(t, A.neutrinos - 0.4, A.neutrinos + 0.2)))
            if cam.visible(SOL, SOL_R * 2):
                P.sol_corte(lz, 0, 0, SOL_R, t, apertura=corte, nucleo=nuc) if corte > 0.01 else P.sol(lz, 0, 0, SOL_R, t)
                if corte > 0.05:
                    _paseo_foton(lz, t, corte)
            _neutrinos(lz, t)
        else:
            _sol_futuro(lz, t if tf is None else tf)
        _planetas(lz, t, cam, modo, tf)
        _tierra_y_luna(lz, t, cam, modo, atm, tf)
        _rotulos_mundo(lz, t, cam, modo)
    lz.M = np.eye(3)
    if modo == 1:
        _gran_escala(lz, t, cam)
        _etiquetas_sol(lz, t, cam)


def _paseo_foton(lz, t, corte):
    """Un fotón que rebota de átomo en átomo desde el núcleo hasta la superficie (dentro de la cuña)."""
    a = ventana(t, A.luz_r - 0.2, A.detuviera - 0.3, 0.4, 0.5)
    if a <= 0.01:
        return
    rng = np.random.default_rng(31)
    ang0 = -0.55
    pts = [np.array([0.0, 0.0])]
    for i in range(160):
        p = pts[-1] + rng.normal(0, 12, 2)
        # deriva lenta hacia fuera dentro de la cuña
        dirc = np.array([math.cos(ang0), math.sin(ang0)])
        p = p + dirc * 1.9
        pts.append(p)
    pts = np.array(pts)
    f = e_in(prog(t, A.luz_r, A.detuviera - 0.6))
    n = max(2, int(len(pts) * f))
    for i, (x, y) in enumerate(rng.random((50, 2))):   # "átomos" de la zona radiativa
        rr = SOL_R * (0.28 + 0.4 * x)
        aa = ang0 + (y - 0.5) * 1.4
        lz.relleno(circulo(rr * math.cos(aa), rr * math.sin(aa), 3.5, 12), (255, 226, 160), alfa=0.6 * a)
    lz.trazo(pts[:n], mezcla((255, 180, 80), (255, 255, 230), a), 2.5, afinar=False)
    lz.halo(pts[n - 1][0], pts[n - 1][1], 12, (255, 250, 200), alfa=a)


def _neutrinos(lz, t):
    a = ventana(t, A.neutrinos - 0.2, FIN_REAL + 1.5, 0.3, 0.8)
    if a <= 0.01:
        return
    for k in range(18):
        ang = k * 0.349 + 0.1
        f = ((t - A.neutrinos) * 0.9 + k * 0.07) % 1.0
        r0 = 30 + f * 3200
        d = np.array([math.cos(ang), math.sin(ang)])
        lz.trazo(np.array([d * r0, d * (r0 + 260)]), mezcla((20, 20, 50), (140, 240, 255), a * (1 - f * 0.5)), 3,
                 afinar=False)


FIN_REAL = _FIN("realidad")


def _rotulos_mundo(lz, t, cam, modo):
    """Rótulos pegados a objetos del mundo (con tamaño de letra constante en pantalla)."""
    z = max(cam.z, 1e-6)
    esc = 1 / z
    if modo == 1:
        E = tierra_pos(t)
        k = pop(t, A.nada - 0.1) * (1 - e_in(prog(t, A.hace - 0.3, A.hace)))
        P.pastilla(lz, E[0], E[1] + (ER + 60) , "todo normal", 36 * esc, k=k)
        for nom, tt, txt in (("mercurio", A.mercurio, "3 min"), ("venus", A.venus, "6 min")):
            k = pop(t, tt - 0.05) * (1 - e_in(prog(t, A.grav_o + 1.0, A.grav_o + 1.5)))
            p = pos_planeta(nom, t)
            P.pastilla(lz, p[0], p[1] - PLANETAS[nom][2] - 40 * esc, txt, 30 * esc, k=k)
        if A.disparada - 0.2 < t < A.jupiter:
            a = ventana(t, A.disparada - 0.1, A.jupiter - 1.4, 0.4, 0.6)
            th = PLANETAS["tierra"][3] - omega(1250.0) * T_LIB["tierra"]
            p0 = pos_planeta("tierra", T_LIB["tierra"])
            dirt = np.array([math.sin(th), -math.cos(th)])
            frac = e_out(prog(t, A.disparada - 0.1, A.disparada + 1.2))
            P.discontinua(lz, [p0, p0 + dirt * 2600], mezcla((20, 20, 50), (236, 240, 255), a), 4 * esc, 22 * esc,
                          14 * esc, fase=-t * 30 * esc, frac=frac)
            g = pos_planeta("tierra", t, libre=False)
            lz.relleno(circulo(g[0], g[1], ER, 80), (140, 160, 230), alfa=0.35 * a)
            P.rotulo(lz, g[0] + ER + 20 * esc, g[1], "órbita", 30 * esc, fuente="geo_n", ancla=(0, 0.5),
                     color=(170, 180, 240), alfa=a)
        if A.alcanza - 0.5 < t < A.luna_d + 3.4:
            k = pop(t, A.tiron - 0.1) * (1 - e_in(prog(t, A.luna_d - 0.4, A.luna_d)))
            P.pastilla(lz, E[0] + ER + 170 * esc * 0.8, E[1] - 20, "sin sacudidas", 32 * esc, k=k)
            k = pop(t, A.luna_d - 0.05) * (1 - e_in(prog(t, A.luna_d + 2.6, A.luna_d + 3.2)))
            L, _ = luna_pos(E, t)
            P.rotulo(lz, L[0], L[1] - 50 * esc, "Luna", 34 * esc, k=k, alfa=min(1, k))
        for nom, tt, txt in (("jupiter", A.jupiter, "43 min"), ("neptuno", A.neptuno, "4 h 10 min")):
            k = pop(t, tt - 0.05) * (1 - e_in(prog(t, A.escapan, A.escapan + 0.5)))
            p = pos_planeta(nom, t)
            P.pastilla(lz, p[0], p[1] - PLANETAS[nom][2] - 50 * esc, txt, 30 * esc, k=k)
        # último reflejo de Júpiter viajando hacia la Tierra
        u = prog(t, A.jupiter2 - 0.4, A.escapan - 0.3)
        if 0 < u < 1:
            pj = pos_planeta("jupiter", T_LIB["jupiter"])
            d = np.linalg.norm(E - pj)
            P.onda(lz, pj[0], pj[1], 40 + u * d, 14 * esc, (255, 206, 150), alfa=0.8 * (1 - 0.4 * u), frente=0.6,
                   estela=1.2)
            k = pop(t, A.reflejo - 0.1)
            P.rotulo(lz, pj[0], pj[1] + PLANETAS["jupiter"][2] + 60 * esc, "último reflejo", 30 * esc, k=k, alfa=min(1, k))
        # un año de viaje en línea recta
        a = ventana(t, A.treinta - 0.3, A.estrella - 1.4, 0.4, 0.4)
        if a > 0.01:
            th = PLANETAS["tierra"][3] - omega(1250.0) * T_LIB["tierra"]
            p0 = pos_planeta("tierra", T_LIB["tierra"])
            dirt = np.array([math.sin(th), -math.cos(th)])
            largo = 1250 * 6.3 * e_out(prog(t, A.treinta, A.mil_km + 2.5))
            P.discontinua(lz, [p0, p0 + dirt * largo], mezcla((20, 20, 50), (236, 240, 255), a), 5 * esc, 30 * esc,
                          20 * esc, fase=-t * 40 * esc)
            P.pastilla(lz, E[0], E[1] - ER - 90 * esc, "≈ 946 millones de km en un año", 34 * esc,
                       k=a * pop(t, A.mil_km))
        k = pop(t, A.errante - 0.05) * (1 - e_in(prog(t, A.solos - 0.6, A.solos - 0.1)))
        P.pastilla(lz, E[0], E[1] + ER + 80 * esc, "planeta errante", 36 * esc, k=k, fondo=(130, 110, 210),
                   color=(255, 255, 255))
    elif modo == 2:
        k = pop(t, A.interruptor - 0.3) * (1 - e_in(prog(t, A.luz_r - 1.0, A.luz_r - 0.5)))
        if k > 0.01:
            with lz.grupo(SOL_R + 420, -40, k):
                P.interruptor(lz, 0, 0, 1.3, encendido=1.0)
                lz.trazo(np.array([[-110, -140], [110, 140]]), (255, 90, 90), 22, afinar=False)
                lz.trazo(np.array([[110, -140], [-110, 140]]), (255, 90, 90), 22, afinar=False)
    else:
        pass


# ---- interfaz: título, reloj, barras
def ui_titulo(lz, t, a):
    if a > 0.01:
        P.rotulo(lz, 960, 96, "¿QUÉ PASARÍA SI EL SOL SE APAGARA?", 60, k=0.94 + 0.06 * a, alfa=a)


def ui_preguntas(lz, t, cam):
    E = cam.a_pant(tierra_pos(t))
    for i, (tt, txt, dx, dy) in enumerate(((A.cuanto, "¿cuánto tardaríamos?", -330, -210),
                                           (A.vida_q, "¿y la vida?", 300, -200),
                                           (A.sobrevivir_q, "¿sobreviviríamos?", 250, 210))):
        k = pop(t, tt - 0.1) * (1 - e_in(prog(t, A.imposible - 0.2, A.imposible + 0.3)))
        P.pastilla(lz, E[0] + dx, E[1] + dy, txt, 38, k=k)


def ui_reloj(lz, t):
    a = e_out(prog(t, A.ahora + 0.5, A.ahora + 1.1)) * (1 - prog(t, A.neptuno + 1.2, A.neptuno + 1.8))
    if a <= 0.01:
        return
    tt = tau(t)
    pulso = 1 + 0.12 * campana(t, A.ocho - 0.05, A.ocho + 0.5) + 0.12 * campana(t, A.alcanza - 0.05, A.alcanza + 0.5)
    col = mezcla((255, 255, 255), (255, 214, 120), prog(t, A.alcanza - 0.2, A.alcanza))
    P.rotulo(lz, 960, 88, formato_tau(tt), 72, k=pulso, alfa=a, fuente="geo_x", color=col)
    P.rotulo(lz, 960, 146, "desde que desapareció el Sol", 28, alfa=a * 0.85, fuente="geo_n", color=(200, 205, 240))


def ui_masa(lz, t):
    a = ventana(t, A.noventa - 0.3, A.superficie - 0.6, 0.4, 0.4)
    if a <= 0.01:
        return
    x0, x1, y, h = 260.0, 1660.0, 110.0, 48.0
    f = e_inout(prog(t, A.noventa - 0.2, A.noventa + 1.0))
    with lz.capa(2):
        lz.relleno(rect_red(x0, y - h / 2, (x1 - x0) * 0.9986 * f, h, 10), (255, 170, 70), alfa=a)
        lz.relleno(rect_red(x1 - 4, y - h / 2, 6, h, 2), (120, 200, 255), alfa=a * prog(f, 0.9, 1.0))
    P.rotulo(lz, x0 + 24, y, "Sol · 99,86 %", 36, ancla=(0, 0.5), alfa=a * f, color=(60, 24, 10), sombra=0)
    P.linea_llamada(lz, (x1, y + h / 2 + 4), (x1 - 60, y + 70), frac=a * prog(f, 0.95, 1.0))
    P.rotulo(lz, x1 - 70, y + 84, "planetas y todo lo demás: 0,14 %", 32, fuente="geo_n", ancla=(1, 0.5),
             alfa=a * prog(f, 0.95, 1.0), color=(190, 225, 255))


def ui_energia(lz, t):
    a = ventana(t, A.hora - 0.3, A.ahora - 0.8, 0.4, 0.4)
    if a <= 0.01:
        return
    y1, y2, x0, w = 108.0, 176.0, 560.0, 800.0
    f1 = e_inout(prog(t, A.hora, A.hora + 1.0))
    f2 = e_inout(prog(t, A.humanidad, A.humanidad + 1.0))
    with lz.capa(2):
        lz.relleno(rect_red(x0, y1 - 16, w * f1, 32, 12), (255, 200, 90), alfa=a)
        lz.relleno(rect_red(x0, y2 - 16, w * 0.97 * f2, 32, 12), (120, 190, 255), alfa=a)
    P.rotulo(lz, x0 - 20, y1, "1 hora de luz solar", 30, ancla=(1, 0.5), alfa=a)
    P.rotulo(lz, x0 - 20, y2, "1 año de energía humana", 30, ancla=(1, 0.5), alfa=a * prog(f2, 0.0, 0.2))
    P.rotulo(lz, x0 + w + 20, (y1 + y2) / 2, "≈", 56, ancla=(0, 0.5), alfa=a * f2)


def ui_tierras(lz, t):
    a = ventana(t, A.tierras - 0.1, A.noventa - 0.6, 0.3, 0.4)
    if a > 0.01:
        P.pastilla(lz, 960, 130, "más de 1 300 000 Tierras", 40, k=a)


def ui_fusion(lz, t):
    a = ventana(t, A.seiscientos - 0.3, A.luz_s - 1.2, 0.4, 0.4)
    if a > 0.01:
        P.pastilla(lz, 960, 130, "600 000 000 toneladas de hidrógeno cada segundo", 38, k=a)
    a = ventana(t, A.cuatro - 0.2, A.luz_s - 1.2, 0.4, 0.4)
    if a > 0.01:
        P.pastilla(lz, 960, 212, "4 000 000 t de materia -> energía  (E = mc²)".replace("->", "→") if False else
                   "4 000 000 t de materia se vuelven energía (E = mc²)", 34, k=a, fondo=(255, 214, 120))


def ui_realidad(lz, t):
    a = ventana(t, A.luz_r + 0.3, A.detuviera - 0.5, 0.4, 0.4)
    if a > 0.01:
        P.pastilla(lz, 960, 130, "del núcleo a la superficie: de 10 000 a 170 000 años", 36, k=a)
    a = ventana(t, A.detuviera + 0.4, A.neutrinos - 0.5, 0.4, 0.4)
    if a > 0.01:
        P.pastilla(lz, 960, 130, "seguiría brillando decenas de millones de años", 36, k=a)
    a = ventana(t, A.neutrinos - 0.1, FIN_REAL + 1.0, 0.4, 0.6)
    if a > 0.01:
        P.pastilla(lz, 960, 130, "neutrinos: salen del núcleo en unos 2 segundos", 36, k=a, fondo=(150, 240, 255))
