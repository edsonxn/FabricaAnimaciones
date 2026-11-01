# -*- coding: utf-8 -*-
"""Figuras y utilería PROPIAS de los tramos 6-7 de «Tres noches» (15-oct-2026), con el pintor del kit «grabado de peste».
Como fig.py: (x, y) = punto del SUELO en pantalla y `s` = escala de pantalla; las que reciben `cam` se dibujan en el mundo.
  necrofago     muerto viviente de la Plaga (esqueleto encorvado con jirones, brazos que buscan, ojos verdes)
  cara_necrofago  el SUSTO de 5:50: cráneo podrido pegado a la cámara + la garra que entra por el borde
  caja          caja «sospechosa» de 2008 (tablas, calavera pintada, tapa que se abre y suelta gas verde)
  calabaza      calabaza tallada de Halloween (Hallow's End) con la vela dentro
  portal        óvalo de portal de mago que gira
  carta, revista, mapa_azeroth, globo   el gabinete de los médicos (CDC, The Lancet, el contagio sobre el mapa)
  cana, vela    el funeral: la caña de pescar clavada en la nieve, las velas de los dolientes"""
import math

import numpy as np

import grabado as GR
import grabado_3d as G3
from grabado import ESPECTRO, HIELO, ORO, PLAGA, SANGRE, TINTA, catmull, circ_pts, lerp, rnd, smooth, tr


# ------------------------------------------------------------------ el necrófago
def pose_necrofago(t, fase=0.0, anda=1.0, ataca=0.0):
    """Andar arrastrado: encorvado, rodillas dobladas, brazos al frente buscando; `ataca` 0..1 levanta las garras."""
    a = t * 6.2832 * 0.7 * max(anda, 0.2) + fase
    sa = math.sin(a)
    k = min(anda, 1.5)
    return dict(tr=0.16 * sa * k, cab=0.35 + 0.15 * math.sin(a * 0.5 + 1.0), hi=1.25 + 0.25 * sa + 1.0 * ataca,
                ci=0.55 - 0.35 * ataca, hd=1.35 - 0.25 * sa + 1.0 * ataca, cd=0.5 - 0.3 * ataca,
                pi=0.32 + 0.25 * max(0.0, sa) * k, ri=-0.55 - 0.3 * max(0.0, sa) * k,
                pd=0.3 + 0.25 * max(0.0, -sa) * k, rd=-0.55 - 0.3 * max(0.0, -sa) * k,
                salto=0.0, mand=0.45 + 0.35 * max(0.0, math.sin(a * 1.7 + 2.0)))


def necrofago(g, x, y, s, t, fase=0.0, anda=1.0, ataca=0.0, op=1.0, ojos=1.0, sem=0):
    """Muerto viviente de la Plaga: el esqueleto de la danza encorvado, con carne gris a jirones, trapos y aura verde."""
    if op <= 0.01 or s <= 0.004:
        return
    pose = pose_necrofago(t, fase, anda, ataca)
    g.acento_luz(x, y - 230 * s, 300 * s, PLAGA, 0.6 * op)
    GR.esqueleto(g, x, y, 0.92 * s, pose, t, op=op, tono=0.22, ojos=ojos)
    with g.grupo(x, y, s):                                   # trapos podridos que cuelgan de la cadera y jirones de carne
        for i in range(5):
            x0 = -46 + 22 * i
            L = 70 + 40 * rnd(i, sem + 3)
            ond = 6 * math.sin(t * 3 + i + sem)
            trapo = [(x0 - 9, -168), (x0 + 11, -168), (x0 + 7 + ond, -168 + L), (x0 + 1 + ond, -168 + L * 0.8),
                     (x0 - 5 + ond, -168 + L)]
            g.figura(np.float32(trapo), 0.55 + 0.3 * rnd(i, sem), contorno=1.6, op=op, ang=90, per=3.8, cruz=False)
        g.acento(np.float32([(-50, -190), (52, -190), (60, -100), (-58, -100)]), PLAGA, 0.45 * op, sem=sem)
    if ojos > 0.05:                                          # brasas verdes en las cuencas
        hx, hy = x + 0.0, y - 380 * s
        g.acento_luz(hx, hy, 70 * s, PLAGA, 0.9 * ojos * op, 1.2)


def cara_necrofago(g, x, y, s, t, boca=1.0):
    """El SUSTO del acto 2: un cráneo podrido enorme, ladeado, con las cuencas ardiendo en verde y una garra que entra."""
    R = 300 * s
    ang = -0.18 + 0.03 * math.sin(t * 9)
    g.acento_luz(x, y, R * 2.4, PLAGA, 0.85, 1.1)
    GR.craneo(g, x, y, R, t, ang=ang, mand=0.95 * boca, tono=0.3, tono2=0.75, ojos=0.0)
    # sombra desde arriba: la frente se hunde en tinta (cara de susto, no de calavera de feria)
    g.trama(circ_pts(x, y - R * 0.2, R * 1.05, 48, R * 0.95),
            lambda X, Y: np.clip(0.95 - (Y - (y - R * 1.1)) / (R * 1.1), 0.0, 0.95), ang=-20, per=4.6, cruz=False)
    for sg in (-1, 1):                                       # rendijas verdes que arden en las cuencas
        ex, ey = x + sg * R * 0.36 * math.cos(ang), y - R * 0.05 + sg * R * 0.36 * math.sin(ang)
        g.acento_luz(ex, ey, R * 0.55, PLAGA, 1.0, 1.0)
        rend = circ_pts(ex, ey, R * 0.035, 16, R * 0.12)
        g.papel(rend, 1.0)
        g.acento(rend, PLAGA, 1.0)
    for i in range(9):                                       # jirones de carne colgando de pómulos y mandíbula
        x0 = x + (i - 4) * R * 0.2 + R * 0.05 * rnd(i, 4)
        y0 = y + R * (0.25 + 0.25 * abs(i - 4) / 4)
        L = R * (0.35 + 0.4 * rnd(i, 5))
        ond = R * 0.03 * math.sin(t * 6 + i)
        tira = [(x0 - R * 0.05, y0), (x0 + R * 0.05, y0), (x0 + R * 0.02 + ond, y0 + L), (x0 - R * 0.03 + ond, y0 + L * 0.9)]
        g.figura(np.float32(tira), 0.6, contorno=2.4, ang=88, per=4.6, cruz=False)
    g.acento(circ_pts(x, y, R * 1.05, 40), PLAGA, 0.35, sem=7)
    # la garra: entra desde abajo a la izquierda, dedos largos y huesudos
    bx, by = x - R * 1.25, y + R * 1.25
    for f in range(4):
        a0 = math.radians(-70 + f * 16)
        dedo = [(bx, by), (bx + R * 0.55 * math.cos(a0), by + R * 0.55 * math.sin(a0)),
                (bx + R * 0.95 * math.cos(a0 + 0.25), by + R * 0.95 * math.sin(a0 + 0.25) - R * 0.05),
                (bx + R * 1.12 * math.cos(a0 + 0.55), by + R * 1.12 * math.sin(a0 + 0.55) + R * 0.05)]
        P = catmull(np.float32(dedo), 6)
        g.trazo(P, R * 0.16, R * 0.03, op=1.0, afilado=0.6)
        g.trazo(P, R * 0.07, R * 0.01, color=g.fondo_papel, op=0.85, afilado=0.8)


# ------------------------------------------------------------------ cajas sospechosas y calabazas
def caja(g, cam, X, Z, t, lado=120.0, alza=1.0, abre=0.0, op=1.0, sem=0, gas=0.0):
    """Caja de tablas en el mundo (cara frontal, el costado que ve la cámara y la tapa) con una calavera pintada.
    `alza` 0..1 = aparece (sube del suelo), `abre` 0..1 = la tapa salta, `gas` 0..1 = nube verde que sale."""
    if alza <= 0.01 or op <= 0.01:
        return
    h = lado * GR.e_out(alza)
    m = lado / 2
    G3.sombra_contacto(g, cam, X, Z, lado * 0.75, lado * 0.3, op=0.8 * op)
    if cam.C[0] > X + m:
        G3.plano(g, cam, (X + m, -h, Z - m), (0, 0, 1), (0, 1, 0), lado, h, 0.62, familias=((0.0, lado / 5),), quiebre=0.25,
                 tramo=lado / 2.5, contorno=2.2, op=op)
    elif cam.C[0] < X - m:
        G3.plano(g, cam, (X - m, -h, Z + m), (0, 0, -1), (0, 1, 0), lado, h, 0.62, familias=((0.0, lado / 5),), quiebre=0.25,
                 tramo=lado / 2.5, contorno=2.2, op=op)
    tapa_y = -h - 70 * GR.e_out(abre)
    if cam.C[1] < -h:
        G3.plano(g, cam, (X - m, tapa_y, Z - m), (1, 0, 0), (0, 0, 1), lado, lado, 0.3, familias=((90.0, lado / 5),),
                 contorno=2.2, op=op)
    G3.plano(g, cam, (X - m, -h, Z - m), (1, 0, 0), (0, 1, 0), lado, h, 0.42, familias=((0.0, lado / 5),), quiebre=0.25,
             tramo=lado / 2.5, contorno=2.4, op=op)
    for dx in (-m + 8, m - 8):                               # listones de las esquinas
        G3.trazo3d(g, cam, [(X + dx, 0, Z - m - 2), (X + dx, -h, Z - m - 2)], 7, afilado=0.0, op=op)
    if alza > 0.6:                                           # la calavera pintada (aviso que nadie leyó)
        px, py, zc = cam.pt(X, -h * 0.5, Z - m - 3)
        GR.craneo(g, px, py, 0.22 * lado * cam.k(zc), t, tono=0.0, tono2=0.3, op=0.8 * op)
        g.acento(circ_pts(px, py, 0.3 * lado * cam.k(zc), 16), PLAGA, 0.6 * op, sem=sem)
    if abre > 0.01 or gas > 0.01:
        px, py, zc = cam.pt(X, -h - 10, Z)
        k = cam.k(zc)
        fz = max(gas, abre)
        g.acento_luz(px, py - 60 * k, 260 * k * (0.6 + 0.6 * fz), PLAGA, 0.75 * fz * op)
        G3.humo(g, px, py, 1.1 * k, t, sem=sem, op=0.55 * fz * op, color=PLAGA, alto=320 * (0.5 + fz), hebras=4)


def calabaza(g, cam, X, Z, t, r=55.0, luz=1.0, sem=0, op=1.0):
    """Calabaza tallada (Hallow's End, el Halloween de Azeroth) con vela dentro."""
    px, py, zc = cam.pt(X, 0, Z)
    k = cam.k(zc)
    R = r * k
    if R < 2 or op <= 0.01:
        return
    G3.sombra_contacto(g, cam, X, Z, r * 1.3, r * 0.45, op=0.8 * op)
    cy = py - R * 0.85
    gajos = [circ_pts(px + dx * R, cy, R * (0.62 - 0.12 * abs(dx)), 24, R * 0.82) for dx in (-0.45, 0.45, 0.0)]
    for gj in gajos:
        g.figura(gj, 0.35, contorno=2.0, op=op, tono2=0.8, luz=-30, ang=90, per=3.8, modo="contorno", cruz=False)
    g.trazo([(px, cy - R * 0.8), (px + R * 0.12, cy - R * 1.15)], 6 * k ** 0.5 + 1, op=op, afilado=0.0)
    lat = luz * (0.85 + 0.15 * math.sin(t * 11 + sem))
    cara = [[(px - R * 0.42, cy - R * 0.12), (px - R * 0.15, cy - R * 0.12), (px - R * 0.28, cy - R * 0.38)],
            [(px + R * 0.42, cy - R * 0.12), (px + R * 0.15, cy - R * 0.12), (px + R * 0.28, cy - R * 0.38)],
            [(px - R * 0.45, cy + R * 0.18), (px - R * 0.2, cy + R * 0.32), (px, cy + R * 0.22), (px + R * 0.2, cy + R * 0.32),
             (px + R * 0.45, cy + R * 0.18), (px + R * 0.2, cy + R * 0.48), (px - R * 0.2, cy + R * 0.48)]]
    for c in cara:
        g.macizo(np.float32(c), op)
        if lat > 0.05:
            g.papel(GR.inflar(np.float32(c), -1.2), 0.9 * lat * op)
            g.acento(np.float32(c), ORO, 0.95 * lat * op, sem=sem)
    g.acento(gajos[2], ORO, 0.35 * op, sem=sem + 1)
    if lat > 0.05:
        g.acento_luz(px, cy, R * 3.2, ORO, 0.45 * lat * op)


# ------------------------------------------------------------------ portal de mago
def portal(g, x, y, rx, ry, t, color=ESPECTRO, fuerza=1.0, op=1.0, giro=1.0):
    """Óvalo de portal (Shattrath → capitales): anillo de piedra con runas y remolino de líneas que gira hacia el centro."""
    if op <= 0.01:
        return
    aro = circ_pts(x, y, rx * 1.12, 60, ry * 1.1)
    hueco = circ_pts(x, y, rx, 60, ry)
    g.figura(aro, 0.45, contorno=3.0, op=op, ang=0, per=4.6, modo="anillos", centro=(x, y), cruz=False)
    g.papel(hueco, op)
    g.trama(hueco, lambda X, Y: np.clip(0.15 + 0.6 * np.sqrt(((X - x) / rx) ** 2 + ((Y - y) / ry) ** 2), 0, 1) * op,
            modo="anillos", centro=(x, y), per=5.0, cruz=False)
    for i in range(10):                                      # runas talladas en el aro (trazos)
        a = i / 10 * 6.2832 + 0.2
        rx_, ry_ = x + rx * 1.06 * math.cos(a), y + ry * 1.05 * math.sin(a)
        e = max(3.0, rx * 0.035)
        g.trazo([(rx_ - e, ry_ - e), (rx_, ry_ + e), (rx_ + e, ry_ - e)], max(1.0, e * 0.3), op=0.8 * op, afilado=0.0)
        if i % 2:
            g.trazo([(rx_, ry_ - 1.4 * e), (rx_, ry_ + e)], max(1.0, e * 0.3), op=0.8 * op, afilado=0.0)
    for j in range(7):                                       # remolino: espirales que giran y se cierran al centro
        a0 = j / 7 * 6.2832 + t * 1.6 * giro
        P = [(x + rx * (1 - u) * math.cos(a0 + 3.2 * u), y + ry * (1 - u) * math.sin(a0 + 3.2 * u)) for u in np.linspace(0, 0.9, 22)]
        g.trazo(np.float32(P), max(1.0, rx * 0.025), op=0.75 * op, afilado=0.8, sem=j)
    g.acento(hueco, color, 0.7 * fuerza * op, sem=3)
    g.acento_luz(x, y, max(rx, ry) * 1.8, color, 0.7 * fuerza * op)


# ------------------------------------------------------------------ el gabinete (lienzos para estampar)
def carta(t, escribe=1.0):
    """La carta de los Centros para el Control de Enfermedades: pergamino con membrete, renglones y lacre."""
    s = GR.G(t, 520, 640, alfa=True)
    perg = GR.silueta_ruido(np.float32([(14, 12), (506, 8), (510, 630), (10, 634)]), 3.0, sem=11, paso=12)
    s.figura(perg, 0.06, contorno=2.6, ang=0, per=5.0, cruz=False)
    s.texto("C · D · C", 260, 70, 44, TINTA, "gotica")
    s.texto("Atlanta, Georgia", 260, 118, 24, TINTA, "gara_i", 0.85)
    s.trazo([(90, 146), (430, 146)], 1.6, op=0.8)
    n = int(12 * escribe)
    for i in range(n):                                       # renglones manuscritos
        yy = 190 + i * 30
        x1 = 440 if i % 4 != 3 else 300
        pts = [(70 + u * (x1 - 70), yy + 4 * math.sin(u * 40 + i)) for u in np.linspace(0, 1, 30)]
        s.trazo(np.float32(pts), 1.6, op=0.8, afilado=0.2, sem=i)
    s.texto("los datos", 380, 548, 26, TINTA, "gara_i", 0.9 * smooth(escribe))
    sello = circ_pts(420, 590, 34, 24)
    s.figura(sello, 0.3, contorno=2.2, ang=0, per=3.6, cruz=False)
    s.acento(sello, SANGRE, 0.9, sem=2)
    return s


def revista(t):
    """La portada de The Lancet Infectious Diseases (vol. 7, n.º 9, 2007) como libro grabado."""
    s = GR.G(t, 560, 720, alfa=True)
    tapa = np.float32([(20, 20), (540, 20), (540, 700), (20, 700)])
    s.figura(tapa, 0.12, contorno=3.0, ang=0, per=5.0, cruz=False)
    s.trazo(np.float32([(40, 40), (520, 40), (520, 680), (40, 680)]), 1.4, cerrado=True, op=0.8, afilado=0.0)
    s.texto("THE LANCET", 280, 120, 66, TINTA, "grab")
    s.texto("Infectious Diseases", 280, 190, 38, TINTA, "gara_i")
    s.trazo([(80, 232), (480, 232)], 2.0, afilado=0.0)
    s.texto("Vol. 7 · n.º 9 · 2007", 280, 270, 26, TINTA, "gara_b", 0.9)
    s.texto("Lofgren & Fefferman", 280, 610, 30, TINTA, "gara_i", 0.9)
    with s.grupo(280, 440, 1.0):                             # grabado de portada: la epidemia virtual (dragón y gente)
        for i in range(7):
            a = i / 7 * 6.2832
            s.figura(circ_pts(120 * math.cos(a), 90 * math.sin(a), 16, 12), 0.2, contorno=1.4, ang=0, per=3.4, cruz=False)
            s.acento(circ_pts(120 * math.cos(a), 90 * math.sin(a), 18, 12), SANGRE, 0.5 + 0.3 * (i % 2), sem=i)
        GR.craneo(s, 0, 0, 44, t)
    s.acento(tapa, SANGRE, 0.12, sem=5)
    return s


# contornos (muy simplificados) de los Reinos del Este y Kalimdor, en el lienzo del mapa (900x600)
_REINOS = [(600, 60), (680, 70), (700, 130), (660, 190), (700, 260), (690, 330), (640, 380), (660, 450), (620, 520),
           (560, 560), (520, 500), (540, 420), (500, 360), (540, 300), (520, 230), (560, 160), (560, 100)]
_KALIMDOR = [(170, 70), (250, 60), (300, 120), (320, 200), (360, 260), (340, 360), (360, 440), (300, 540), (230, 560),
             (190, 480), (150, 420), (170, 330), (120, 260), (150, 170)]
CIUDADES = {"Forjaz": (618, 300), "Ventormenta": (585, 455), "Orgrimmar": (315, 230), "Entrañas": (590, 150)}


def mapa_azeroth(t, contagio=0.0, foco="Forjaz", titulo=True, plaga=0.0):
    """Mapa grabado de Azeroth con el contagio que se extiende en rojo desde `foco` (`contagio` 0..1) o, con `plaga` 0..1,
    las cajas verdes de 2008 que aparecen una a una en las capitales."""
    s = GR.G(t, 900, 600, alfa=True)
    perg = GR.silueta_ruido(np.float32([(10, 10), (890, 6), (894, 590), (6, 594)]), 3.0, sem=21, paso=14)
    s.figura(perg, 0.04, contorno=2.6, ang=0, per=5.0, cruz=False)
    s.trama(np.float32([(20, 20), (880, 20), (880, 580), (20, 580)]), 0.3, ang=0, per=6.0, cruz=False)   # el mar
    for k_, cont in enumerate((_REINOS, _KALIMDOR)):
        pol = catmull(GR.silueta_ruido(np.float32(cont), 6.0, sem=30 + k_, paso=10), 3, cerrado=True)
        s.figura(pol, 0.22, contorno=2.6, ang=60, per=4.2, cruz=False, tono2=0.5, luz=-60)
        s.trazo(GR.inflar(pol, 8), 1.0, cerrado=True, op=0.6)
    for nom, (cx, cy) in CIUDADES.items():
        s.circ(cx, cy, 6, TINTA)
        s.texto(nom, cx + 12, cy - 10, 20, TINTA, "gara_i", 0.85, "lm")
    if titulo:
        s.texto("AZEROTH", 450, 44, 34, TINTA, "gotica")
    if contagio > 0.01:
        fx, fy = CIUDADES[foco]
        for i in range(60):                                  # puntos de contagio que brotan alrededor del foco y saltan
            d = 30 + 420 * rnd(i, 41) ** 1.4
            if d > 450 * contagio:
                continue
            a = rnd(i, 42) * 6.2832
            px, py = fx + d * math.cos(a), fy + 0.7 * d * math.sin(a)
            if not (20 < px < 880 and 20 < py < 580):
                continue
            r = 5 + 7 * rnd(i, 43)
            s.acento(circ_pts(px, py, r, 10), SANGRE, 0.95, sem=i)
            s.circ(px, py, r * 0.45, TINTA, 0.8)
        s.acento_luz(fx, fy, 260 * contagio, SANGRE, 0.5)
    for i, (nom, (cx, cy)) in enumerate(CIUDADES.items()):
        u = smooth(pr_(plaga, i / len(CIUDADES), (i + 0.6) / len(CIUDADES)))
        if u <= 0.01:
            continue
        caja_ = np.float32([(cx - 16, cy - 40), (cx + 16, cy - 40), (cx + 16, cy - 10), (cx - 16, cy - 10)])
        s.figura(caja_, 0.4, contorno=2.0, op=u, ang=0, per=3.6, cruz=False)
        s.acento(circ_pts(cx, cy - 25, 46 * u + 4, 16), PLAGA, 0.9 * u, sem=i)
        s.acento_luz(cx, cy - 25, 110 * u, PLAGA, 0.6 * u)
    return s


def pr_(x, a, b):
    return min(1.0, max(0.0, (x - a) / max(b - a, 1e-6)))


def globo(g, x, y, r, t, rojo=0.0):
    """Globo terráqueo del mundo REAL sobre su pie (las cuarentenas de 2020): meridianos que giran, continentes en trama."""
    g.figura(np.float32([(x - r * 0.5, y + r * 1.45), (x + r * 0.5, y + r * 1.45), (x + r * 0.2, y + r * 1.2),
                         (x - r * 0.2, y + r * 1.2)]), 0.35, contorno=2.0, ang=0, per=4, cruz=False)
    g.trazo([(x, y + r * 1.2), (x, y + r)], max(2, r * 0.08), afilado=0.0)
    g.figura(circ_pts(x, y, r, 48), 0.1, contorno=2.6, tono2=0.6, luz=-40, ang=0, per=4.0, modo="contorno", cruz=False)
    rot = t * 0.4
    for i in range(6):                                       # meridianos
        a = (i / 6 * math.pi + rot) % math.pi
        rx = r * math.cos(a)
        g.trazo(circ_pts(x, y, abs(rx) + 0.5, 30, r), 1.0, cerrado=True, op=0.5)
    for j in (-0.5, 0.0, 0.5):
        g.trazo(circ_pts(x, y + j * r, r * math.sqrt(1 - j * j), 30, r * 0.12), 1.0, cerrado=True, op=0.45)
    for i in range(5):                                       # continentes que giran con el globo
        a = (i * 1.3 + rot) % 6.2832
        if math.cos(a) < 0.1:
            continue
        cx = x + r * 0.75 * math.sin(a)
        cy = y + r * (0.45 * rnd(i, 3) - 0.25)
        rr = r * 0.22 * math.cos(a) ** 0.5
        pol = GR.silueta_ruido(circ_pts(cx, cy, rr * (0.6 + 0.4 * math.cos(a)), 14, rr), rr * 0.2, sem=i, paso=6)
        g.figura(pol, 0.55, contorno=1.4, ang=30, per=3.4, cruz=False)
        if rojo > 0.01:
            g.acento(pol, SANGRE, 0.9 * rojo, sem=i)
    g.trazo(circ_pts(x, y, r * 1.12, 40), max(2, r * 0.05), op=0.8, afilado=0.0)      # meridiano de latón


# ------------------------------------------------------------------ el funeral
def cana(g, cam, X, Z, t, agua=(0.0, 0.0), op=1.0):
    """Caña de pescar clavada en la nieve junto al agua, con el sedal y el corcho que sube y baja."""
    base = (X, 0.0, Z)
    punta = (X + 120, -330, Z - 60)
    G3.trazo3d(g, cam, [base, punta], 7, afilado=0.9, op=op)
    cx, cz = agua
    corcho = (cx, -6 + 6 * math.sin(t * 2.1), cz)
    G3.trazo3d(g, cam, [punta, ((punta[0] + cx) / 2, -150, (punta[2] + cz) / 2), corcho], 1.2, afilado=0.0, op=0.8 * op)
    px, py, zc = cam.pt(*corcho)
    k = cam.k(zc)
    g.figura(circ_pts(px, py - 6 * k, 9 * k + 1, 12), 0.0, contorno=1.4, op=op)
    g.acento(circ_pts(px, py - 6 * k, 9 * k + 1, 12), SANGRE, 0.8 * op)
    for j in range(2):                                       # ondas del corcho
        rr = (14 + ((t * 20 + j * 18) % 36)) * k
        g.trazo(circ_pts(px, py, rr, 24, rr * 0.25), 1.0, cerrado=True, op=0.5 * op * (1 - rr / (52 * k)))


def vela(g, x, y, s, t, fuerza=1.0, sem=0, op=1.0, color=ORO):
    """Vela de doliente (en la mano o en la nieve): cirio, pabilo y llama."""
    if op <= 0.01:
        return
    g.figura(np.float32([(x - 7 * s, y), (x + 7 * s, y), (x + 7 * s, y - 46 * s), (x - 7 * s, y - 46 * s)]), 0.05,
             contorno=1.4, op=op, tono2=0.5, luz=0, ang=90, per=3.6, cruz=False)
    if fuerza > 0.02:
        GR.llama(g, x, y - 48 * s, 0.35 * s * (0.6 + 0.4 * fuerza), t, sem=sem, color=color, acento=0.9)
        g.acento_luz(x, y - 60 * s, 70 * s * fuerza, color, 0.4 * fuerza * op)


def corona_lich(g, x, y, s, t, op=1.0):
    """La silueta del Rey Exánime en las nubes: yelmo con corona de púas, en azul helado (aún no ha llegado)."""
    with g.grupo(x, y, s):
        yelmo = [(-90, 40), (-110, -40), (-80, -120), (-40, -150), (0, -158), (40, -150), (80, -120), (110, -40), (90, 40),
                 (40, 20), (0, 60), (-40, 20)]
        g.figura(catmull(np.float32(yelmo), 4, True), 0.4, contorno=2.6, op=op, tono2=0.9, luz=0, ang=80, per=4.6)
        for i, (dx, h) in enumerate(((-90, 120), (-50, 170), (0, 220), (50, 170), (90, 120))):
            g.figura(np.float32([(dx - 16, -130), (dx + 16, -130), (dx, -130 - h)]), 0.3, contorno=2.0, op=op, ang=90, per=4)
        for sg in (-1, 1):
            g.figura(circ_pts(sg * 36, -40, 14, 12, 8), 0.0, contorno=1.4, op=op)
            g.acento_luz(sg * 36, -40, 50, HIELO, 0.9 * op)
        g.acento(catmull(np.float32(yelmo), 4, True), HIELO, 0.6 * op, sem=4)
    g.acento_luz(x, y - 60 * s, 300 * s, HIELO, 0.45 * op)
