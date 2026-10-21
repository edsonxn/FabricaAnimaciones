# -*- coding: utf-8 -*-
"""Escena «hogar» (35-44,5 s): «Nuestro hogar», la casa isométrica de la app flotando en una isla de pasto, con su HUD
(🪙 monedas y 🏠 valor) y el dock (Muebles · Huerto · Ampliar · Fotos). Las monedas que ganan con las misiones caen al contador
y cada mueble que compran cae del cielo con rebote. Luego la cámara baja al huerto (v24): las plantas crecen con el tiempo en un
día-noche acelerado mientras su tanque 💧 tenga agua; una se marchita sin agua y la gota la revive."""
import math

import e_juegos as EJ
from comun import Cam, utileria, ventana
from duo import (A, B, BG, BLANCO, CARD, GOLD, INK, LINE, MUT, O, OK, W, H, ancho_texto, burst, clamp, e_in, e_io, e_out,
                 golpe, hexa, kf, lerp, mix, pill, pop, pr, rnd, smooth, sobre, ww)

T0, T1 = 35.0, 44.5
o_gan, o_mis, o_dec, o_hog = ww("hogar", 0, "ganamos"), ww("hogar", 0, "misiones"), ww("hogar", 0, "decoramos"), ww("hogar", 0, "hogar")
u_ten, u_hue, u_cre = ww("hogar", 1, "tenemos"), ww("hogar", 1, "huerto"), ww("hogar", 1, "crece")
u_ver, u_si, u_acor, u_reg = ww("hogar", 1, "verdad"), ww("hogar", 1, "si"), ww("hogar", 1, "acordamos"), ww("hogar", 1, "regarlo")
T_ENTRA = 34.75
T_SALE = 44.05

S = 62.0                               # px por casilla a cámara 1
OX, OY = 540.0, 1010.0


def iso(x, y, z=0.0):
    return (OX + (x - y) * S * 0.866, OY + (x + y) * S * 0.5 - z * S)


def subida(t):
    """La isla sube desde abajo al entrar y se hunde al salir (px)."""
    return 1700 * (1 - e_out(pr(t, T_ENTRA, T_ENTRA + 0.75))) + 1900 * e_in(pr(t, T_SALE, T_SALE + 0.55))


HUERTO_C = iso(3.2, -2.8, 1.0)
CASA_C = iso(-0.6, -1.2, 0.9)


def camara(t):
    z = kf(t, [(T0, 1.3), (u_hue - 0.35, 1.3), (u_hue + 0.3, 2.3), (T_SALE, 2.3), (T1, 1.4)])
    cx = kf(t, [(T0, CASA_C[0]), (u_hue - 0.35, CASA_C[0]), (u_hue + 0.3, HUERTO_C[0]), (T_SALE, HUERTO_C[0]), (T1, 540.0)])
    cy = kf(t, [(T0, CASA_C[1]), (u_hue - 0.35, CASA_C[1]), (u_hue + 0.3, HUERTO_C[1]), (T_SALE, HUERTO_C[1]), (T1, 960.0)])
    return Cam(z, cx, cy)


# ------------------------------------------------------------------ primitivas isométricas
def oscuro(c, k):
    return tuple(v * k for v in c)


def caja(p, x, y, z, dx, dy, dz, col, op=1.0, top=None):
    """Prisma isométrico: tapa, cara +y (izquierda, sombra) y cara +x (derecha, luz)."""
    p.poly([iso(x, y + dy, z), iso(x + dx, y + dy, z), iso(x + dx, y + dy, z + dz), iso(x, y + dy, z + dz)], oscuro(col, 0.72), op)
    p.poly([iso(x + dx, y, z), iso(x + dx, y + dy, z), iso(x + dx, y + dy, z + dz), iso(x + dx, y, z + dz)], oscuro(col, 0.88), op)
    p.poly([iso(x, y, z + dz), iso(x + dx, y, z + dz), iso(x + dx, y + dy, z + dz), iso(x, y + dy, z + dz)], top or col, op)


def plano(p, x, y, z, dx, dy, col, op=1.0):
    p.poly([iso(x, y, z), iso(x + dx, y, z), iso(x + dx, y + dy, z), iso(x, y + dy, z)], col, op)


PASTO, PASTO2, TIERRA = hexa("7BC86C"), hexa("6AB85C"), hexa("8B5A2B")
PISO, PARED, PARED2 = hexa("D9A066"), hexa("F2E6D8"), hexa("E3D3C2")
MADERA = hexa("B07A4A")


def isla(p, t):
    caja(p, -5, -5, -1.0, 10, 10, 1.0, TIERRA, top=PASTO)
    for i in range(10):                                               # cuadros de pasto alternados
        for j in range(10):
            if (i + j) % 2 == 0:
                plano(p, -5 + i, -5 + j, 0.002, 1, 1, PASTO2, 0.55)
    for k in range(7):                                                # caminito de piedras hacia la puerta
        x, y = 1.0 + k * 0.55, 1.4 + 0.25 * math.sin(k)
        cx, cy = iso(x, y, 0.01)
        p.elip(cx, cy, 16, 9, hexa("C9C2B8"))
    plano(p, -4.5, -4.5, 0.02, 5.0, 5.0, PISO)
    for i in range(10):                                               # duelas del piso
        p.poly([iso(-4.5 + 0.5 * i, -4.5, 0.025), iso(-4.5 + 0.5 * i + 0.02, -4.5, 0.025), iso(-4.5 + 0.5 * i + 0.02, 0.5, 0.025),
                iso(-4.5 + 0.5 * i, 0.5, 0.025)], oscuro(PISO, 0.85))
    # paredes del fondo con ventanas
    caja(p, -4.7, -4.7, 0, 5.2, 0.2, 2.6, PARED, top=hexa("CDBBA8"))
    caja(p, -4.7, -4.5, 0, 0.2, 5.0, 2.6, PARED2, top=hexa("CDBBA8"))
    for x0 in (-3.6, -1.2):
        p.poly([iso(x0, -4.49, 1.0), iso(x0 + 1.2, -4.49, 1.0), iso(x0 + 1.2, -4.49, 2.0), iso(x0, -4.49, 2.0)], hexa("9FD4F0"))
        p.poly([iso(x0 + 0.58, -4.48, 1.0), iso(x0 + 0.62, -4.48, 1.0), iso(x0 + 0.62, -4.48, 2.0), iso(x0 + 0.58, -4.48, 2.0)], BLANCO, 0.8)
    p.poly([iso(-4.49, -2.6, 1.0), iso(-4.49, -1.4, 1.0), iso(-4.49, -1.4, 2.0), iso(-4.49, -2.6, 2.0)], hexa("8CC6E6"))
    # cuadro en la pared
    p.poly([iso(-4.49, -0.8, 1.2), iso(-4.49, -0.1, 1.2), iso(-4.49, -0.1, 1.8), iso(-4.49, -0.8, 1.8)], A)


def arbol(p, x, y, t, k=1.0):
    bx, by = iso(x, y, 0)
    p.elip(bx, by, 40 * k, 18 * k, oscuro(PASTO, 0.7), 0.6)
    p.rect(bx - 7 * k, by - 70 * k, bx + 7 * k, by, hexa("7A4B2A"))
    sw = 4 * math.sin(t * 1.5 + x)
    for dx, dy, r, c in ((0, -110, 52, hexa("3E9A5B")), (-26, -80, 38, hexa("4CAF64")), (24, -86, 40, hexa("4CAF64")),
                         (0, -140, 34, hexa("5CC274"))):
        p.circ(bx + (dx + sw) * k, by + dy * k, r * k, c)


MUEBLES = [   # (nombre, precio 🪙, función de dibujo, ancla de profundidad x+y)
    ("tapete", 60), ("sillon", 180), ("mesa", 70), ("tele", 150), ("cama", 160), ("lampara", 50), ("planta", 40),
]


def t_mueble(i):
    return o_dec + 0.06 + 0.2 * i


def caida(t, i):
    u = e_out(pr(t, t_mueble(i), t_mueble(i) + 0.35))
    return 5.0 * (1 - u), (1 + 0.15 * golpe(t, t_mueble(i) + 0.35, 0.25))


def mueble(p, nombre, t, dz):
    if nombre == "tapete":
        plano(p, -3.7, -3.6, 0.03 + dz, 2.4, 1.7, A)
        plano(p, -3.5, -3.4, 0.035 + dz, 2.0, 1.3, sobre(BLANCO, A, 0.2))
    elif nombre == "sillon":
        caja(p, -3.6, -1.5, dz, 2.2, 0.8, 0.45, hexa("8B5CF6"))
        caja(p, -3.6, -0.75, dz, 2.2, 0.28, 1.0, hexa("7646E0"))
        caja(p, -3.75, -1.5, dz, 0.2, 1.0, 0.7, hexa("7646E0"))
        caja(p, -1.4, -1.5, dz, 0.2, 1.0, 0.7, hexa("7646E0"))
    elif nombre == "mesa":
        caja(p, -3.0, -3.0, dz, 1.1, 0.7, 0.32, MADERA)
        cx, cy = iso(-2.45, -2.65, 0.32 + dz)
        p.emoji("🍿", cx, cy - 14, 26)
    elif nombre == "tele":
        caja(p, -3.5, -4.45, dz, 1.8, 0.45, 0.45, hexa("4A3C5A"))
        caja(p, -3.35, -4.42, 0.45 + dz, 1.5, 0.08, 0.85, hexa("1A1622"))
        u = 0.5 + 0.5 * math.sin(t * 3)
        p.poly([iso(-3.28, -4.33, 0.52 + dz), iso(-1.92, -4.33, 0.52 + dz), iso(-1.92, -4.33, 1.24 + dz), iso(-3.28, -4.33, 1.24 + dz)],
               mix(hexa("3B82F6"), hexa("8B5CF6"), u))
    elif nombre == "cama":
        caja(p, -1.3, -4.4, dz, 1.6, 2.1, 0.42, hexa("F6EEF7"))
        caja(p, -1.3, -2.9, 0.42 + dz, 1.6, 0.6, 0.05, A)
        caja(p, -1.3, -3.6, 0.42 + dz, 1.6, 0.7, 0.04, sobre(A, BLANCO, 0.6))
        caja(p, -1.2, -4.35, 0.42 + dz, 0.65, 0.4, 0.14, BLANCO)
        caja(p, -0.45, -4.35, 0.42 + dz, 0.65, 0.4, 0.14, BLANCO)
        caja(p, -1.35, -4.55, dz, 1.7, 0.15, 1.0, MADERA)
    elif nombre == "lampara":
        caja(p, -0.35, -1.0, dz, 0.08, 0.08, 1.5, hexa("4A3C5A"))
        caja(p, -0.55, -1.2, 1.5 + dz, 0.48, 0.48, 0.35, hexa("FFD36B"))
        cx, cy = iso(-0.3, -0.95, 1.6 + dz)
        p.glow(cx, cy, 140, sobre(GOLD, BG, 0.5), 0.35, 1.5)
    elif nombre == "planta":
        caja(p, -4.3, -4.3, dz, 0.5, 0.5, 0.4, hexa("C2603E"))
        cx, cy = iso(-4.05, -4.05, 0.4 + dz)
        for k in range(6):
            a = -1.3 + 0.52 * k + 0.08 * math.sin(t * 1.4 + k)
            p.polilinea([(cx, cy), (cx + 30 * math.sin(a), cy - 50 * math.cos(a) - 10)], 12, hexa("3E9A5B"))


# ------------------------------------------------------------------ huerto
PARCELAS = [(1.8, -4.3, "girasol"), (3.3, -4.3, "chile"), (1.8, -2.6, "cempasuchil"), (3.3, -2.6, "pina")]
T_RIEGO = u_reg + 0.05


def etapa(t):
    """Crecimiento común: brote, día-noche acelerado (crece), y al regar termina de crecer."""
    e = 0.15 + 0.6 * e_io(pr(t, u_cre - 0.05, u_si))
    return e + 0.25 * e_out(pr(t, T_RIEGO + 0.2, T_RIEGO + 0.8))


def marchita(t, tipo):
    if tipo != "chile":
        return 0.0
    return smooth(pr(t, u_si, u_acor + 0.2)) * (1 - e_out(pr(t, T_RIEGO + 0.15, T_RIEGO + 0.6)))


def tanque(t, tipo):
    """Gotas en el tanque (0..4): se vacía con el tiempo; el chile se queda en 0 hasta el riego."""
    base = 4 - 3 * pr(t, u_cre - 0.05, u_si)
    if tipo == "chile":
        base = 4 - 4 * pr(t, u_cre - 0.05, u_si - 0.2)
    return min(4.0, base + 4 * e_out(pr(t, T_RIEGO + 0.1, T_RIEGO + 0.45)))


def planta(p, x, y, tipo, t):
    e = etapa(t)
    m = marchita(t, tipo)
    bx, by = iso(x + 0.6, y + 0.7, 0.3)
    alto = 95 * e
    verde = mix(hexa("3E9A5B"), hexa("8C7A48"), m)
    inc = 0.9 * m                                                     # se dobla
    sw = 3 * math.sin(t * 2 + x)
    pts = []
    for k in range(9):
        v = k / 8
        ang = inc * v * v
        pts.append((bx + sw * v + math.sin(ang) * alto * v * 0.9, by - math.cos(ang) * alto * v))
    p.polilinea(pts, 6, verde)
    for k in (3, 5, 7):
        if k / 8 > e * 1.2:
            continue
        px_, py_ = pts[k]
        for sx in (-1, 1):
            p.elip(px_ + sx * 14, py_ + 4 * m * 10, 15, 7, verde, 1.0, ang=sx * (25 + 40 * m))
    tx, ty = pts[-1]
    if e < 0.35:
        p.circ(tx, ty, 7, hexa("5CC274"))
        return
    f = clamp((e - 0.35) / 0.5)
    r = 24 * f
    if tipo == "girasol":
        for k in range(12):
            a = 2 * math.pi * k / 12
            p.elip(tx + math.cos(a) * r * 0.9, ty + math.sin(a) * r * 0.9, r * 0.5, r * 0.22, mix(hexa("FFD23F"), hexa("9A8A50"), m),
                   1.0, ang=math.degrees(a))
        p.circ(tx, ty, r * 0.55, hexa("6B3E1E"))
    elif tipo == "cempasuchil":
        for k in range(9):
            a = 2 * math.pi * k / 9 + t
            p.circ(tx + math.cos(a) * r * 0.45, ty + math.sin(a) * r * 0.45, r * 0.5, hexa("FF8A1F"))
        p.circ(tx, ty, r * 0.55, hexa("FFB13D"))
    elif tipo == "chile":
        for k, dx in enumerate((-16, 0, 16)):
            cx, cy = tx + dx * f, ty + 18 * f + 10 * m * 3
            p.elip(cx, cy, 6 * f, 18 * f, mix(hexa("E3342F"), hexa("7A5A3A"), m), 1.0, ang=15 * (k - 1) + 50 * m)
    else:                                                             # piña
        p.elip(tx, ty + 8, r * 0.6, r * 0.85, hexa("F2B33D"))
        for k in range(4):
            p.linea((tx - r * 0.5, ty - r * 0.3 + k * r * 0.35), (tx + r * 0.5, ty - r * 0.6 + k * r * 0.35), 2, hexa("B07A2A"))
        for k in range(5):
            a = -0.9 + 0.45 * k
            p.polilinea([(tx, ty - r * 0.6), (tx + 22 * f * math.sin(a), ty - r * 0.6 - 26 * f * math.cos(a))], 6, hexa("3E9A5B"))


def barra_agua(p, x, y, gotas, t, op=1.0):
    """La barrita azul del tanque (4 gotas) sobre cada parcela, como en el panel del huerto."""
    w = 84
    p.rrect(x - w / 2 - 22, y - 13, x + w / 2 + 6, y + 13, 13, sobre(CARD, BG, 0.9), op, borde=LINE, w=1.5)
    p.emoji("💧", x - w / 2 - 8, y, 16, op)
    for k in range(4):
        x0 = x - w / 2 + 8 + k * 19
        lleno = clamp(gotas - k)
        p.rrect(x0, y - 6, x0 + 16, y + 6, 4, LINE, op)
        if lleno > 0:
            p.rrect(x0, y - 6, x0 + 16 * lleno, y + 6, 4, hexa("3B82F6"), op)
    if gotas <= 0.05:
        b = 0.5 + 0.5 * math.sin(t * 9)
        p.rrect(x - w / 2 - 22, y - 13, x + w / 2 + 6, y + 13, 13, None, op * b, borde=hexa("FF4D5E"), w=2.5)


def huerto(p, t):
    for x, y, tipo in PARCELAS:
        caja(p, x, y, 0, 1.2, 1.4, 0.3, MADERA, top=hexa("5A3A22"))
        for k in range(3):
            p.poly([iso(x + 0.15, y + 0.25 + 0.4 * k, 0.305), iso(x + 1.05, y + 0.25 + 0.4 * k, 0.305),
                    iso(x + 1.05, y + 0.3 + 0.4 * k, 0.305), iso(x + 0.15, y + 0.3 + 0.4 * k, 0.305)], hexa("4A2E1A"))
    for x, y, tipo in sorted(PARCELAS, key=lambda q: q[0] + q[1]):
        planta(p, x, y, tipo, t)


# ------------------------------------------------------------------ HUD y dock (pantalla)
def monedas(t):
    v = 600 + 640 * e_io(pr(t, o_gan + 0.2, o_mis + 0.6))
    for i, (_, precio) in enumerate(MUEBLES):
        v -= precio * smooth(pr(t, t_mueble(i) + 0.35, t_mueble(i) + 0.5))
    return v


def valor(t):
    v = 12290
    for i, (_, precio) in enumerate(MUEBLES):
        v += precio * smooth(pr(t, t_mueble(i) + 0.35, t_mueble(i) + 0.5))
    return v


def hud(p, t, op):
    from e_juegos import moneda
    y = 170
    m = int(round(monedas(t)))
    s = 1 + 0.12 * max(golpe(t, o_mis + 0.6, 0.3), max(golpe(t, t_mueble(i) + 0.4, 0.25) for i in range(len(MUEBLES))))
    with p.pivote(60, y, s):
        txt = f"{m:,}"
        w = ancho_texto(txt, 60, "x") + 130
        p.sombra(40, y - 56, 40 + w, y + 56, 56, blur=24, op=0.55 * op, dy=8)
        p.rrect(40, y - 56, 40 + w, y + 56, 56, CARD, op, borde=LINE, w=2)
        moneda(p, 100, y, 32, 1.0, op)
        p.texto(txt, 150, y + 3, 60, INK, "x", op, "lm")
    txt = f"{int(round(valor(t))):,}"
    w2 = ancho_texto(txt, 44, "x") + 110
    x2 = 40 + ancho_texto(f"{m:,}", 60, "x") + 130 + 20
    p.rrect(x2, y - 46, x2 + w2, y + 46, 46, CARD, op * 0.9, borde=LINE, w=2)
    p.emoji("🏠", x2 + 48, y, 46, op)
    p.texto(txt, x2 + 84, y + 3, 44, MUT, "x", op, "lm")
    p.texto("monedas para gastar", 70, y + 90, 32, MUT, "s", op, "lm")
    # precio de cada mueble que se compra
    for i, (nom, precio) in enumerate(MUEBLES):
        t0 = t_mueble(i) + 0.35
        if t0 <= t <= t0 + 0.9:
            u = (t - t0) / 0.9
            p.texto(f"−{precio}", 300, y + 150 - 90 * e_out(u), 50, hexa("FF8A8A"), "x", op * math.sin(math.pi * min(1, u * 1.3)))


def dock(p, t, op):
    items = (("🛋️", "Muebles"), ("🌱", "Huerto"), ("🧱", "Ampliar"), ("📷", "Fotos"))
    x0, x1, y0, y1 = 110, 970, 1730, 1860
    p.sombra(x0, y0, x1, y1, 40, blur=30, op=0.6 * op, dy=10)
    p.rrect(x0, y0, x1, y1, 40, sobre(CARD, BG, 0.9), op, borde=LINE, w=2)
    act = 1 if t >= u_hue - 0.2 else (0 if t >= o_dec - 0.2 else -1)
    for i, (emo, nom) in enumerate(items):
        cx = x0 + (x1 - x0) * (i + 0.5) / 4
        if i == act:
            tc = u_hue - 0.2 if i == 1 else o_dec - 0.2
            with p.pivote(cx, (y0 + y1) / 2, 1 - 0.08 * golpe(t, tc, 0.25)):
                p.rrect(cx - 96, y0 + 12, cx + 96, y1 - 12, 30, op=op, hg=(cx - 96, cx + 96))
        p.emoji(emo, cx, y0 + 48, 40, op)
        p.texto(nom, cx, y0 + 98, 22, BLANCO if i == act else MUT, "b", op)


def cielo_tiempo(p, t):
    """Día-noche acelerado (al decir «crece de verdad»): sol y luna que giran detrás de la isla."""
    u = pr(t, u_cre - 0.1, u_si + 0.1)
    if u <= 0 or u >= 1:
        return 0.0
    ang = math.pi * (1 + 2 * u)
    for k, (col, r) in enumerate(((hexa("FFE07A"), 70), (hexa("F3EBD8"), 56))):
        a = ang + k * math.pi
        x, y = 540 + 470 * math.cos(a), 700 + 420 * math.sin(a)
        if y < 900:
            p.glow(x, y, r * 3, col, 0.5, 1.5)
            p.circ(x, y, r, col)
    return 0.5 - 0.5 * math.cos(2 * math.pi * u)                         # noche 0..1..0


# ------------------------------------------------------------------ dibujo
def dibujar(p, t):
    if t < T_ENTRA or t > T1 + 0.4:
        return
    cam = camara(t)
    noche = cielo_tiempo(p, t)
    dy = subida(t)
    with cam.aplicar(p):
        with p.grupo(0, dy):
            p.elip(OX, OY + 420, 520, 120, (0, 0, 0), 0.35)               # sombra de la isla sobre el «vacío»
            isla(p, t)
            arbol(p, 4.2, 2.6, t, 1.1)
            arbol(p, -4.0, 3.6, t, 0.9)
            arbol(p, 4.4, -4.6, t, 0.8)
            huerto(p, t)
            orden = sorted(range(len(MUEBLES)), key=lambda i: {"tapete": -9, "tele": -8, "planta": -7, "cama": -6}.get(MUEBLES[i][0], 0))
            for i in orden:
                if t >= t_mueble(i):
                    z, sq = caida(t, i)
                    mueble(p, MUEBLES[i][0], t, z)
                    if t >= t_mueble(i) + 0.33 and t <= t_mueble(i) + 1.0:
                        cx, cy = iso(-2.0, -2.0, 0)
                        burst(p, cx, cy, t, t_mueble(i) + 0.35, n=10, fuerza=0.35, semilla=100 + i, dur=0.7, escala=0.6)
            # barras de agua de cada parcela
            if t >= u_hue:
                ob = smooth(pr(t, u_hue, u_hue + 0.3))
                for x, y, tipo in PARCELAS:
                    bx, by = iso(x + 0.6, y + 0.7, 2.4)
                    with p.grupo(bx, by, 1.7 / max(cam.z, 1e-3)):
                        barra_agua(p, 0, 0, tanque(t, tipo), t, ob)
                        if tipo == "chile" and marchita(t, tipo) > 0.3:
                            p.texto("Sin agua: no crece", 0, 34, 15, hexa("FF8A8A"), "b", marchita(t, tipo))
                        if t >= T_RIEGO + 0.7:
                            k = pop(t, T_RIEGO + 0.7 + 0.08 * PARCELAS.index((x, y, tipo)), 0.3)
                            with p.pivote(0, -34, 0.5 + 0.5 * k):
                                pill(p, "¡Listas!", 0, -34, BLANCO, OK, px=14, anchor="m")
            # gotas que caen al regar
            if T_RIEGO - 0.2 <= t <= T_RIEGO + 0.9:
                for k in range(16):
                    t0 = T_RIEGO - 0.2 + 0.03 * k
                    x, y, _ = PARCELAS[k % 4]
                    bx, by = iso(x + 0.6 + (rnd(k, 5) - 0.5) * 0.6, y + 0.7, 0.3)
                    tau = t - t0
                    if 0 <= tau <= 0.5:
                        yy = by - 260 + 1040 * tau * tau * 2
                        if yy < by:
                            p.poly([(bx, yy - 14), (bx + 7, yy), (bx, yy + 8), (bx - 7, yy)], hexa("6FB6FF"), 0.9)
    if noche > 0:
        p.im *= 1 - 0.5 * noche * (1 - 0.25 * __import__("numpy").float32([0.2, 0.3, 1.0]))
    op = smooth(pr(t, T_ENTRA + 0.3, T_ENTRA + 0.7)) * (1 - smooth(pr(t, T_SALE - 0.1, T_SALE + 0.2)))
    hud(p, t, op)
    dock(p, t, op)
    frente(p, t, cam)


def frente(p, t, cam):
    from e_juegos import moneda
    # monedas de las misiones: caen al contador
    if o_gan - 0.2 <= t <= o_mis + 1.0:
        k = pop(t, o_gan, 0.35) * (1 - e_in(pr(t, o_dec - 0.3, o_dec)))
        with p.pivote(540, 400, k):
            pill(p, "Semana con la barra llena · +300", 540, 420, hexa("1A1320"), GOLD, px=42, anchor="m", emo="🏆")
        for i in range(22):
            t0 = o_gan + 0.1 + 0.05 * i
            dur = 0.7
            if t0 <= t <= t0 + dur:
                u = e_io((t - t0) / dur)
                x0, y0 = 540 + (rnd(i, 7) - 0.5) * 600, 480 + rnd(i, 8) * 200
                x, y = lerp(x0, 100, u), lerp(y0, 170, u) - 160 * math.sin(math.pi * u)
                moneda(p, x, y, 26 - 8 * u, math.cos((t - t0) * 9 + i))
    # riego: el botón «+1 gota» de la app y la gota grande
    if u_acor - 0.2 <= t <= T_SALE:
        k = pop(t, u_acor - 0.2, 0.35) * (1 - e_in(pr(t, T_SALE - 0.3, T_SALE)))
        prs = 1 - 0.1 * golpe(t, T_RIEGO - 0.25, 0.25)
        with p.pivote(540, 1560, k * prs):
            w = ancho_texto("+1 gota", 44, "x") + 130
            p.sombra(540 - w / 2, 1505, 540 + w / 2, 1615, 55, blur=26, op=0.6, dy=10, color=hexa("3B82F6"))
            p.rrect(540 - w / 2, 1505, 540 + w / 2, 1615, 55, hexa("3B82F6"))
            p.emoji("💧", 540 - w / 2 + 62, 1560, 52)
            p.texto("+1 gota", 540 - w / 2 + 104, 1562, 44, BLANCO, "x", 1, "lm")
    utileria(p, "💧", 860, 1380, 150, t, T_RIEGO - 0.3, T_SALE - 0.2, 1.0)
    utileria(p, "🌱", 190, 1380, 130, t, u_hue, u_cre + 0.3, 0.5)
    if t >= T_RIEGO + 0.5:
        for i in range(12):                                           # destellos al florecer
            t0 = T_RIEGO + 0.5 + 0.05 * i
            if t0 <= t <= t0 + 0.8:
                u = (t - t0) / 0.8
                x = 540 + (rnd(i, 3) - 0.5) * 800
                y = 900 + (rnd(i, 4) - 0.5) * 500 - 120 * u
                r = 16 + 18 * math.sin(math.pi * u)
                q = r * 0.22
                p.poly([(x, y - r), (x + q, y - q), (x + r, y), (x + q, y + q), (x, y + r), (x - q, y + q), (x - r, y), (x - q, y - q)],
                       (1, 0.95, 0.8), math.sin(math.pi * u))
