# -*- coding: utf-8 -*-
"""El espacio del plano secuencia «dos lunas»: Tierra en el origen del mundo (radio 100 px), la Luna en una órbita de
radio 700, el Sol a la izquierda (luz desde el lado izquierdo). Todo se dibuja en pantalla a partir de la cámara.
Tomas de este módulo: 1 intro, 2 hoy (marea), 3 origen (captura / 2024 PT5 / choque gigante), 4 órbita (Hill, Jano y
Epimeteo, L4). Dibujo escala NO real (cuerpos exagerados): se declara con «sin escala» donde hay una cota."""
import math

import numpy as np

import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, cam_claves, kf, pop, ventana, campana
from anclas import A

ER = 100.0                 # radio de la Tierra (px de mundo)
RL = 700.0                 # radio de la órbita de la Luna
MR = 52.0                  # radio de la Luna (exagerado)
HILL = 2680.0              # radio de la esfera de Hill de la Tierra (1,47 M km ≈ 3,82 × órbita lunar)
LUZ = math.pi              # el Sol está a la izquierda: ángulo HACIA la luz
LIN = lambda x: x          # noqa: E731  (ease lineal para kf)

AZUL = (150, 170, 235)
ORO = (255, 214, 90)
TINTA = (34, 28, 80)
MENTA = (130, 230, 200)
ROSA = (255, 140, 170)


# ======================================================================== órbita de la Luna y de la segunda
def ang_luna(t):
    """Ángulo de la Luna en su órbita (la velocidad cambia entre tomas: lapso de tiempo en el espacio grande)."""
    return float(kf(t, [(0, -0.45), (22, 0.02), (41.5, 0.30), (68.3, 0.62), (T_LUNA1, PHI_A),
                        (82.8, PHI_A + 0.95 * (82.8 - T_LUNA1)), (133.0, PHI_A + 0.95 * (82.8 - T_LUNA1) + 0.24 * 50.2)], ease=LIN))


def radio_luna1(t):
    """Radio de la órbita de la Luna: nace cerca (330) y se aleja hasta 700 al abrir la cámara en la toma 4."""
    if t < T_LUNA1:
        return RL
    return float(kf(t, [(T_LUNA1, 330.0), (82.3, 330.0), (84.8, RL)]))


def luna_mundo(t, radio=None):
    radio = radio_luna1(t) if radio is None else radio
    return np.array(K.pos_orbita(0, 0, radio, radio, 0, ang_luna(t)))


def fondo(t, cam, tono=0, brillo=1.0):
    c = cam.ancla + (np.array([W / 2, H / 2]) - cam.pant) / cam.z
    return K.fondo_espacio(t, brillo=brillo, dx=-c[0] * 0.04 * min(cam.z, 2), dy=-c[1] * 0.04 * min(cam.z, 2), tono=tono)


def nebulas(lz, cam, lista):
    """Nubes de gas lejanas (paralaje muy lento). lista: [(x_pant, y_pant, r, color, seed, alfa)]."""
    c = cam.ancla + (np.array([W / 2, H / 2]) - cam.pant) / cam.z
    for sx, sy, r, col, seed, al in lista:
        K.nebulosa(lz, sx - c[0] * 0.08, sy - c[1] * 0.08, r, col, seed=seed, alfa=al)


def fondo_vivo(lz, t, cam):
    """Sol al borde izquierdo (de ahí viene la luz) y rocas lejanas que derivan: profundidad detrás de los cuerpos."""
    c = cam.ancla + (np.array([W / 2, H / 2]) - cam.pant) / cam.z
    lz.halo(-110 - c[0] * 0.02, 520 - c[1] * 0.02, 900, (255, 190, 110), alfa=0.17, r0=0.0, dureza=1.3, capa=0)
    lz.halo(-70 - c[0] * 0.02, 520 - c[1] * 0.02, 300, (255, 232, 180), alfa=0.28, r0=0.0, dureza=1.4, capa=0)
    for i in range(9):
        r = 5.0 + 8.0 * h01(i, 1, 7)
        vx = 7.0 + 9.0 * h01(i, 2, 7)
        x = (h01(i, 3, 7) * (W + 300) + vx * t * 0.6 - c[0] * 0.05) % (W + 300) - 150
        y = 90 + h01(i, 4, 7) * (H - 180) - c[1] * 0.05 + 10 * math.sin(t * 0.4 + i)
        K.roca(lz, x, y, r, seed=i + 11, rot=t * (0.2 + 0.3 * h01(i, 5, 7)), tipo="ceniza", ang_luz=LUZ, luz=0.55)


def kuri_ui(lz, t, x, y, s=1.0, mirar=(0.0, 0.0), **kw):
    P.kuri(lz, x, y + 7 * math.sin(t * 2.1), s, t, mirar=mirar, **kw)


def chip(lz, t, x, y, texto, t0, t1=None, px=42, fondo=(255, 255, 255), alfa=1.0):
    """Pastilla que entra con rebote en t0 y (opcional) se apaga en t1."""
    k = pop(t, t0, 0.35)
    if t1 is not None:
        k *= 1 - e_in(prog(t, t1, t1 + 0.3))
    if k > 0.01:
        P.pastilla(lz, x, y, texto, px=px, k=k, fondo=fondo, color=TINTA, alfa=alfa)


def fantasma(lz, x, y, r, t, alfa=1.0):
    """Cuerpo hipotético: disco translúcido con contorno punteado que corre."""
    lz.relleno(circulo(x, y, r, 48), (255, 255, 255), alfa=0.14 * alfa)
    th_ = np.linspace(0, 2 * np.pi, 72)
    P.discontinua(lz, np.stack([x + r * np.cos(th_), y + r * np.sin(th_)], 1), (255, 255, 255), 3.0, 12, 10, fase=t * 25)


def marca_x(lz, x, y, s=1.0, k=1.0, color=(255, 90, 110)):
    """✗ roja (entra con rebote: k es la escala)."""
    if k <= 0.01:
        return
    d = 22 * s * k
    for a, b in (((-d, -d), (d, d)), ((-d, d), (d, -d))):
        lz.trazo(np.array([[x + a[0], y + a[1]], [x + b[0], y + b[1]]]), color, 9 * s * min(k, 1.0), afinar=False, temblor=0.0)


def bez2(p0, p1, p2, u):
    return (1 - u) ** 2 * np.asarray(p0, float) + 2 * (1 - u) * u * np.asarray(p1, float) + u * u * np.asarray(p2, float)


def kepler(a, e, w, M):
    """Posición relativa al foco para la anomalía media M (periapsis en el ángulo w; sentido horario en pantalla)."""
    E_ = M
    for _ in range(7):
        E_ = E_ - (E_ - e * math.sin(E_) - M) / (1 - e * math.cos(E_))
    x = a * (math.cos(E_) - e)
    y = a * math.sqrt(1 - e * e) * math.sin(E_)
    c, s_ = math.cos(w), math.sin(w)
    return np.array([x * c - y * s_, x * s_ + y * c])


def trail(lz, f, t, dur=0.5, n=12, color=(255, 255, 255), ancho=7.0, alfa=1.0):
    """Estela de un objeto cuya posición en pantalla es f(tt) (tapers hacia atrás)."""
    pts = [np.asarray(f(t - dur * k / n), float) for k in range(n + 1)]
    for k in range(n):
        u = k / n
        lz.trazo(np.array([pts[k], pts[k + 1]]), mezcla(color, (30, 30, 80), u * 0.8), max(1.0, ancho * (1 - u)),
                 afinar=False, temblor=0.0)


def fondo_comun(lz, t, cam):
    """Fondo: nubes de gas de color propio por toma (se mezclan con suavidad) + Sol y rocas lejanas."""
    a_a = 0.55 - 0.30 * e_inout(prog(t, 41.0, 46.0)) + 0.30 * e_inout(prog(t, 82.0, 90.0))
    a_t = 0.50 * e_inout(prog(t, 41.0, 46.0)) * (1 - e_inout(prog(t, 82.0, 90.0)))
    a_o = 0.45 * e_inout(prog(t, 84.0, 92.0))
    nebulas(lz, cam, [(500, 280, 760, (130, 70, 210), 2, a_a), (1500, 760, 640, (70, 120, 220), 5, 0.4),
                      (1300, 380, 720, (40, 170, 190), 7, a_t), (400, 820, 600, (230, 90, 140), 9, a_t * 0.8),
                      (1200, 700, 760, (240, 130, 70), 11, a_o * 0.7), (500, 300, 600, (60, 90, 230), 13, a_o)])
    fondo_vivo(lz, t, cam)


def guias_vert(lz, p, y1, alfa, col=(255, 255, 255)):
    P.discontinua(lz, np.array([p, [p[0], y1]]), col, 3.0, largo=12, hueco=10, fase=0)


# ======================================================================== cámara de las tomas 1-4
def cam_espacio(t):
    m0 = luna_mundo(0.0)
    m1 = luna_mundo(0.8)
    CL = [
        (0.0, m0, (1130, 520), 6.2),
        (0.8, m1, (1130, 520), 6.7),
        (3.4, (0, 0), (340, 610), 1.40),
        (E_T2, (0, 0), (380, 590), 1.34),
        (24.0, (0, 0), (470, 560), 1.2),
        (30.4, (0, 0), (470, 560), 1.2),
        (32.6, (0, 0), (700, 545), 1.45),
        (41.4, (0, 0), (700, 545), 1.40),
        (44.5, (0, 0), (760, 570), 1.05),
        (66.5, (0, 0), (760, 570), 1.05),
        (68.7, (0, 0), (700, 560), 1.2),
        (82.4, (0, 0), (700, 560), 1.2),
        (86.6, (0, 0), (860, 560), 0.55),
        (88.5, (0, 0), (1010, 560), 0.17),
        (98.6, (0, 0), (1010, 560), 0.17),
        (100.6, (0, 0), (860, 560), 0.62),
        (116.6, (0, 0), (860, 560), 0.62),
        (119.0, (0, 0), (620, 560), 0.68),
        (133.0, (0, 0), (620, 560), 0.68),
    ]
    return cam_claves(t, CL)


E_T2 = 21.8
E_ORIGEN = A.primera - 0.55
E_ORBITA = A.segunda - 0.55
T_LUNA1 = A.luna_o + 0.0          # la Luna nace (se junta la roca)
PHI_A = 2.2                       # ángulo (órbita) donde se forma la Luna


# ======================================================================== tomas 1 y 2
def _tierra(lz, t, cam, lunas, amp, jit=0.0):
    E = cam.a_pant((0, 0))
    x = E[0] + jit * 4 * math.sin(t * 37)
    y = E[1] + jit * 3 * math.cos(t * 29)
    K.tierra_marea(lz, x, y, ER * cam.z, t, lunas, rot=0.45 * t, ang_luz=LUZ, amp=amp)
    return np.array([x, y])


def toma_12(lz, t, cam):
    z = cam.z
    E = cam.a_pant((0, 0))
    th = ang_luna(t)
    mw = luna_mundo(t)
    mp = cam.a_pant(mw)
    th2 = th + 0.22
    # --- órbitas
    a_orb = e_out(prog(t, 3.0, 4.2)) if z < 3.5 else 0.0
    if a_orb > 0.01 and z < 3.5:
        K.orbita(lz, E[0], E[1], RL * z, RL * z, 0, AZUL, 3.0, alfa=0.5 * a_orb, fase=t * 26)
    # órbitas candidatas: "dónde podría vivir"
    r2 = float(kf(t, [(10.2, RL), (10.9, RL * 1.45), (11.5, RL * 0.62), (12.1, RL * 1.22), (12.9, RL)]))
    cand = ventana(t, 10.3, 12.6, 0.3, 0.5)
    if cand > 0.02:
        for rr, col in ((RL * 1.45, ROSA), (RL * 0.62, MENTA), (RL * 1.22, ORO)):
            K.orbita(lz, E[0], E[1], rr * z, rr * z, 0, col, 3.0, alfa=0.55 * cand, fase=-t * 30)
    # --- Tierra (con sus mareas)
    amp = 0.0
    lunas = [(math.atan2(mp[1] - E[1], mp[0] - E[0]), 1.0)]
    pos2 = np.array(K.pos_orbita(0, 0, r2, r2, 0, th2))
    p2 = cam.a_pant(pos2)
    v2 = pop(t, A.dos0, 0.4) * (1 - e_in(prog(t, 21.2, 22.0)))
    if v2 > 0.01:
        lunas.append((math.atan2(p2[1] - E[1], p2[0] - E[0]), 1.0))
    loco = ventana(t, A.mareas_i - 0.1, A.locura + 1.5, 0.3, 0.8)
    amp = 0.12 * loco * 0.0 + 0.2 * loco * (0.65 + 0.35 * math.sin(t * 9)) + 0.0
    if t > 29.8:                       # marea de la Luna sola: crece al hablar de los océanos
        amp = 0.22 * e_inout(prog(t, 29.8, 32.4))
        amp += 0.14 * e_inout(prog(t, A.estira - 0.3, A.estira + 0.9))
    amp = max(amp, 0.0)
    Ec = _tierra(lz, t, cam, lunas, amp, jit=loco * 1.0)
    # --- la Luna
    escala_l = 1.0
    K.cuerpo_rocoso(lz, mp[0], mp[1], MR * z * escala_l, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t)
    if t < A.tierra_i + 0.4:                 # toma cerrada: realce de la Luna
        pass
    # --- segunda Luna
    if v2 > 0.01:
        fant = 1.0 - 0.62 * e_inout(prog(t, A.quizas, A.quizas + 0.8)) - 0.38 * e_inout(prog(t, 21.2, 21.9))
        gr = 1.0 + 0.42 * pop(t, A.enorme, 0.45) * (1 - e_in(prog(t, 21.0, 21.8)))
        rr = MR * z * v2 * gr
        K.cuerpo_rocoso(lz, p2[0], p2[1], rr, "ceniza", seed=5, ang_luz=LUZ, rot=-0.05 * t, alfa=fant)
        if fant < 0.9:   # contorno punteado de «fantasma»
            th_ = np.linspace(0, 2 * np.pi, 80)
            P.discontinua(lz, np.stack([p2[0] + rr * 1.1 * np.cos(th_), p2[1] + rr * 1.1 * np.sin(th_)], 1), (255, 255, 255),
                          3.0, 12, 10, fase=t * 25, frac=1.0)
        k_d = campana(t, A.dos0 - 0.1, A.dos0 + 0.9)
        if k_d > 0.01:
            K.destello(lz, p2[0], p2[1], 90 * k_d * z / 1.25, t, alfa=min(1.0, k_d * 1.5))
        # signo de pregunta
        q = ventana(t, A.dos0 + 0.3, A.junto + 0.2, 0.2, 0.3) + ventana(t, A.quizas, 21.7, 0.3, 0.5) * 0.9
        if q > 0.02:
            P.rotulo(lz, p2[0] + rr + 46, p2[1] - rr * 0.55 - 6 * math.sin(t * 3), "?", px=110, color=ORO, alfa=min(1.0, q))
    # --- la piedrita
    if A.piedrita - 0.05 < t < A.piedrita + 1.6:
        u = prog(t, A.piedrita + 0.55, A.piedrita + 1.5)
        base = cam.a_pant(np.array(K.pos_orbita(0, 0, RL + 190, RL + 190, 0, th2 + 0.02)))
        k_p = pop(t, A.piedrita, 0.3)
        px_ = base[0] + e_in(u) * 760
        py_ = base[1] - e_in(u) * 300 + 6 * math.sin(t * 4)
        K.roca(lz, px_, py_, 12 * k_p * z / 1.25, seed=3, rot=t * 3, tipo="ceniza", ang_luz=LUZ)
        if u < 0.2:
            P.rotulo(lz, base[0] + 20, base[1] - 56, "una piedrita", px=36, alfa=k_p * 0.95)
    # --- el realce de la Luna en la toma 2: anillos
    for i, t0 in enumerate((A.luna_h - 0.2, A.luna_h + 0.5)):
        u = prog(t, t0, t0 + 1.1)
        if 0 < u < 1:
            P.onda(lz, mp[0], mp[1], MR * z * (1.15 + 2.2 * e_out(u)), 7.0, (255, 255, 255), alfa=0.6 * (1 - u))
    return E, mp, p2, v2


def agenda(lz, t):
    """Tres preguntas de la intro (arriba)."""
    chip(lz, t, 560, 84, "¿De dónde sale?", A.donde1 - 0.15, 13.7, 40, ORO)
    chip(lz, t, 980, 84, "¿Dónde vive?", A.donde2 - 0.15, 13.7, 40, MENTA)
    chip(lz, t, 1440, 84, "¿Qué le hace a la Tierra?", A.que_i - 0.15, 13.7, 40, ROSA)


# ----------------------------------------------------------------------- las 81 lunitas
def _slots(n=81, r=18.0):
    pts = []
    for i in range(-12, 13):
        for j in range(-12, 13):
            pts.append(((i + 0.5 * j) * 2.04 * r, j * math.sqrt(3) * 1.02 * r))
    pts.sort(key=lambda p: (p[0] ** 2 + p[1] ** 2, p[1], p[0]))
    return pts[:n]


SLOTS = _slots()
CENTRO_81 = np.array([300.0, 240.0])


def lunitas_81(lz, t, mp, alfa_total=1.0):
    t_ini = A.ochenta - 0.35
    if t < t_ini or alfa_total <= 0.01:
        return
    n = len(SLOTS)
    r = 18.0
    pulso = (1.0 + 0.06 * campana(t, A.tierra_h - 0.1, A.tierra_h + 0.7)) * alfa_total
    for i, (sx, sy) in enumerate(SLOTS):
        # las más cercanas al centro llegan primero (se apilan hacia fuera)
        t0 = t_ini + i * 0.0175
        u = prog(t, t0, t0 + 0.6)
        if u <= 0:
            continue
        dst = CENTRO_81 + np.array([sx, sy]) * pulso
        src = np.asarray(mp, float)
        ctrl = (src + dst) / 2 + np.array([0.0, -140.0 - 40 * h01(i, 3, 3)])
        v = e_out(u)
        p = (1 - v) ** 2 * src + 2 * (1 - v) * v * ctrl + v * v * dst
        rr = r * (0.5 + 0.5 * e_back(min(1.0, u * 1.2)))
        P.luna(lz, p[0], p[1], rr * pulso, LUZ)
    # contorno de la Tierra que forman
    k = e_out(prog(t, A.tierra_h - 0.2, A.tierra_h + 0.5))
    if k > 0.01:
        th_ = np.linspace(0, 2 * np.pi, 120)
        R_ = 190 * pulso
        P.discontinua(lz, np.stack([CENTRO_81[0] + R_ * np.cos(th_), CENTRO_81[1] + R_ * np.sin(th_)], 1), (110, 190, 255),
                      5.0, 18, 12, fase=t * 30, frac=k)
        P.pastilla(lz, CENTRO_81[0] + 395, CENTRO_81[1] - 40, "1 Tierra = 81 Lunas", px=40, k=k, fondo=(110, 190, 255),
                   color=TINTA)


# ----------------------------------------------------------------------- regla 384 400 km y mareas
def regla_distancia(lz, t, E, mp):
    f = e_inout(prog(t, A.cuatro - 0.2, A.km + 0.5)) * (1 - e_in(prog(t, A.poca - 0.2, A.poca + 0.4)))
    if f <= 0.01:
        return
    yr = max(E[1], mp[1]) + 210
    p0 = np.array([E[0], yr])
    p1 = np.array([mp[0], yr])
    for p, c in ((E, p0), (mp, p1)):
        P.discontinua(lz, np.array([p, c]), (255, 255, 255), 2.5, 10, 9, fase=t * 20, frac=f)
    K.regla(lz, p0, p1, "384 400 km", px=38, frac=f, lado=-1)
    if f > 0.9:
        P.rotulo(lz, (p0[0] + p1[0]) / 2, yr + 100, "(sin escala)", px=26, alfa=0.6 * min(1, (f - 0.9) * 10), color=(210, 215, 245))


def barquito(lz, x, y, ang, s=1.0):
    """Barquito (casco y vela) que va sobre el agua; `ang` = dirección normal hacia fuera de la Tierra."""
    with lz.grupo(x, y, s, ang + math.pi / 2):
        lz.relleno(np.array([[-18, 0], [18, 0], [12, 10], [-12, 10]]), (255, 120, 90))
        lz.trazo(np.array([[0, 0], [0, -34]]), (255, 255, 255), 3, afinar=False, temblor=0.0)
        lz.relleno(np.array([[2, -32], [2, -6], [24, -6]]), (255, 255, 255))


def mareas_toma2(lz, t, cam, E, mp, v2):
    if t < A.poca - 0.4:
        return
    ang = math.atan2(mp[1] - E[1], mp[0] - E[0])
    r = ER * cam.z
    # barquito que da vueltas: sube en las dos marea altas
    vb = ventana(t, A.poca + 0.6, A.dia + 1.0, 0.4, 0.5)
    if vb > 0.02:
        ph = (t - A.poca) * 1.9
        f = math.cos(2 * (ph - ang))
        amp_t = 0.22 * e_inout(prog(t, 29.8, 32.4)) * 1.0
        rr = r * (1.0 + amp_t * f) + 6
        bx, by = E[0] + rr * math.cos(ph), E[1] + rr * math.sin(ph)
        barquito(lz, bx, by, ph, 1.5 * vb)
    cnt = e_out(prog(t, A.dos_veces - 0.1, A.dos_veces + 0.5)) * (1 - e_in(prog(t, A.dia + 1.0, A.dia + 1.5)))
    if cnt > 0.01:
        P.pastilla(lz, E[0], E[1] - r * 1.55, "2 veces al día", px=44, k=cnt, fondo=(110, 190, 255), color=TINTA)
    # flechas de tirón
    near = e_out(prog(t, A.tira, A.tira + 0.6))
    far = e_out(prog(t, A.lejano - 0.2, A.lejano + 0.6))
    out = 1 - e_in(prog(t, 41.0, 41.4))
    if near > 0.01:
        c, s_ = math.cos(ang), math.sin(ang)
        pul = 0.92 + 0.08 * math.sin(t * 4)
        a = E + np.array([c, s_]) * r * 1.12
        b = a + np.array([c, s_]) * r * 0.62 * pul
        K.flecha(lz, a, b, ORO, ancho=10, frac=near, alfa=out, capa=2)
        if far > 0.01:
            a2 = E - np.array([c, s_]) * r * 1.12
            b2 = a2 - np.array([c, s_]) * r * 0.30 * pul
            K.flecha(lz, a2, b2, ORO, ancho=6, frac=far, alfa=out, capa=2)
        kn = e_out(prog(t, A.cercano, A.cercano + 0.5))
        kf_ = e_out(prog(t, A.lejano, A.lejano + 0.5))
        if kn > 0.01:
            P.pastilla(lz, a[0] + c * 120, a[1] + s_ * 120 - 70, "más fuerte", px=38, k=kn * out, fondo=ORO, color=TINTA)
        if kf_ > 0.01:
            P.pastilla(lz, a2[0] - c * 80, a2[1] - s_ * 80 - 70, "más débil", px=38, k=kf_ * out, fondo=(255, 236, 170), color=TINTA)


# ======================================================================== Kuri (mascota) en las tomas 1-4
def kuri_toma(lz, t, E, mp):
    pos = kf(t, [(0.0, (330, 880)), (0.9, (330, 880)), (3.4, (1690, 930)), (30.2, (1690, 930)), (32.6, (1640, 420)),
                 (1000.0, (1640, 420))])
    s = float(kf(t, [(0.0, 1.8), (0.9, 1.8), (3.4, 1.0), (1000.0, 1.0)]))
    head = np.array([pos[0], pos[1] - 90 * s])
    if A.ochenta - 0.3 < t < 31.0:
        tgt = CENTRO_81
    elif t > 33.0:
        tgt = E
    else:
        tgt = mp
    d = np.asarray(tgt, float) - head
    n = max(1.0, float(np.hypot(*d)))
    mirar = tuple(d / n * 0.9)
    loco = ventana(t, A.mareas_i - 0.1, A.locura + 1.5, 0.3, 0.8)
    feliz = 1.0 if (A.quizas < t < 22.2) else 0.0
    kuri_ui(lz, t, pos[0], pos[1], s, mirar, boca=loco, feliz=feliz,
            aleteo=ventana(t, A.donde1 - 0.8, A.planeta + 0.6, 0.3, 0.4) * (0.5 + 0.5 * math.sin(t * 7)))


# ======================================================================== dispatcher de las tomas 1-4 (se va completando)
def dibujar_espacio(lz, t, cam):
    fondo_comun(lz, t, cam)
    E, mp, p2, v2 = toma_12(lz, t, cam)
    if t < 21.9:
        agenda(lz, t)
    else:
        mareas_toma2(lz, t, cam, E, mp, v2)
        regla_distancia(lz, t, E, mp)
        lunitas_81(lz, t, mp, 1.0 - e_in(prog(t, 30.4, 31.2)))
    kuri_toma(lz, t, E, mp)
