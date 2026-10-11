# -*- coding: utf-8 -*-
"""Kit de dibujo del video 'historia_60' (estilo Kurzgesagt, vertical 1080x1920): personajes con ciclo de caminata,
paisaje en capas (colinas, nubes, hierba), partículas y utilidades de fondo. Todo son rellenos planos sobre el Lienzo."""
import math

import numpy as np

import plano as P
from motor import (W, H, circulo, clamp01, e_back, e_in, e_inout, e_out, elipse, h01, lerp, prog, r1, rect_red,
                   remuestrear, ruido1, smooth)
from plano import TINTA, aclarar, mezcla, oscurecer

PI = math.pi
PIEL = [(255, 205, 165), (232, 172, 128), (196, 128, 92), (150, 96, 68), (110, 70, 52)]
NEG = (30, 26, 62)


# ------------------------------------------------------------------ geometría
def capsula(x0, y0, x1, y1, w0, w1=None, n=8):
    """Cápsula (segmento redondeado) de (x0,y0) a (x1,y1) con anchos w0 y w1."""
    ang = math.atan2(y1 - y0, x1 - x0)
    r0, r1_ = w0 / 2, (w1 if w1 is not None else w0) / 2
    a = np.linspace(ang + PI / 2, ang + 3 * PI / 2, n)
    b = np.linspace(ang - PI / 2, ang + PI / 2, n)
    return np.concatenate([np.stack([x0 + r0 * np.cos(a), y0 + r0 * np.sin(a)], 1),
                           np.stack([x1 + r1_ * np.cos(b), y1 + r1_ * np.sin(b)], 1)])


def poli(*pts):
    return np.array(pts, float)


def rot_pts(Pp, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    Q = np.asarray(Pp, float) - [cx, cy]
    return np.stack([Q[:, 0] * c - Q[:, 1] * s, Q[:, 0] * s + Q[:, 1] * c], 1) + [cx, cy]


def curva(y_fn, x0=-40, x1=None, paso=30.0, base=None):
    """Polígono cerrado bajo la curva y = y_fn(x) hasta 'base' (por defecto el borde inferior)."""
    x1 = W + 40 if x1 is None else x1
    xs = np.arange(x0, x1 + paso, paso)
    ys = np.array([y_fn(x) for x in xs])
    b = H + 60 if base is None else base
    return np.concatenate([np.stack([xs, ys], 1), [[xs[-1], b], [xs[0], b]]])


# ------------------------------------------------------------------ fondos
def degradado_img(top, bot, mid=None, ym=0.55):
    """Imagen float32 HxWx3 con degradado vertical de 2 o 3 colores (ym = posición del color medio, 0..1)."""
    v = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    top, bot = np.array(top, np.float32) / 255, np.array(bot, np.float32) / 255
    if mid is None:
        c = top + (bot - top) * v
    else:
        mid = np.array(mid, np.float32) / 255
        u1 = np.clip(v / ym, 0, 1)
        u2 = np.clip((v - ym) / (1 - ym), 0, 1)
        c = np.where(v < ym, top + (mid - top) * u1, mid + (bot - mid) * u2)
    return np.ascontiguousarray(np.broadcast_to(c[:, None, :], (H, W, 3)).astype(np.float32))


def rect_full(lz, color, alfa=1.0, capa=None):
    lz.relleno(rect_red(-20, -20, W + 40, H + 40, 0), color, alfa=alfa, capa=capa)


def colinas(lz, y0, col, amp=60.0, frec=0.004, semilla=0, dx=0.0, sombra=0.0, base=None):
    """Cordillera suave de colinas (ruido 1D) desde y0 hasta abajo. dx = desplazamiento horizontal (paralaje)."""
    def f(x):
        return y0 + amp * (ruido1((x + dx) * frec, semilla, 0) + 0.45 * ruido1((x + dx) * frec * 2.3, semilla, 1))
    lz.relleno(curva(f, base=base), col)
    if sombra > 0:      # banda de sombra bajo la cresta
        lz.relleno(curva(lambda x: f(x) + 34, base=base), oscurecer(col, sombra), alfa=0.0 if sombra <= 0 else 0.0)
    return f


def nube(lz, x, y, s=1.0, col=(255, 255, 255), alfa=0.9):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-90, -22, 180, 44, 22), col, alfa=alfa)
        lz.relleno(circulo(-34, -26, 34, 24), col, alfa=alfa)
        lz.relleno(circulo(18, -40, 44, 28), col, alfa=alfa)
        lz.relleno(circulo(62, -20, 26, 20), col, alfa=alfa)


def nubes(lz, t, y0, n=4, vel=20.0, col=(255, 255, 255), alfa=0.85, semilla=1, esc=1.0, dy=110.0):
    for i in range(n):
        x = ((h01(semilla, i, 1) * (W + 500) + vel * t) % (W + 500)) - 250
        y = y0 + dy * (h01(semilla, i, 2) - 0.5) * 2
        nube(lz, x, y, esc * (0.7 + 0.7 * h01(semilla, i, 3)), col, alfa)


def hierba(lz, x0, x1, y, t, col, n=14, alto=46.0, semilla=0, viento=1.0, dx=0.0):
    """Mechones de hierba que se mecen (triángulos curvos)."""
    for i in range(n):
        x = x0 + (x1 - x0) * (i + h01(semilla, i)) / n + dx
        h = alto * (0.6 + 0.8 * h01(semilla, i, 5))
        sw = math.sin(t * 2.2 + i * 1.7) * 7 * viento
        for k in (-1, 0, 1):
            lz.relleno(poli((x + k * 7 - 4, y), (x + k * 12 + sw * (0.6 + 0.4 * abs(k)), y - h * (1 - 0.18 * abs(k))),
                            (x + k * 7 + 4, y)), col if k else oscurecer(col, 0.12))


def particulas(lz, t, n, x0, x1, y0, y1, vel=(0.0, -40.0), r=(2.0, 5.0), col=(255, 255, 255), alfa=0.7, semilla=0,
               vaiven=20.0, capa=2, tw=True):
    """Polvo/chispas/copos que derivan; posiciones periódicas (función de t)."""
    pts, rs = [], []
    for i in range(n):
        u = h01(semilla, i, 1)
        px = x0 + (x1 - x0) * u + vaiven * math.sin(t * (0.6 + h01(semilla, i, 2)) + i)
        py = y0 + (y1 - y0) * ((h01(semilla, i, 3) + t * vel[1] / max(1, (y1 - y0))) % 1.0)
        px += vel[0] * t
        px = x0 + ((px - x0) % max(1.0, (x1 - x0)))
        pts.append((px, py))
        rr = lerp(r[0], r[1], h01(semilla, i, 4))
        if tw:
            rr *= 0.6 + 0.4 * math.sin(t * 3 + i * 2.1)
        rs.append(max(0.5, rr))
    lz.puntos(np.array(pts), np.array(rs), col, capa=capa)


def chispa(lz, x, y, r, col=(255, 240, 200), rot=0.0, alfa=1.0):
    """Destello de 4 puntas."""
    with lz.grupo(x, y, 1.0, rot):
        lz.relleno(poli((0, -r), (r * 0.16, -r * 0.16), (r, 0), (r * 0.16, r * 0.16), (0, r), (-r * 0.16, r * 0.16),
                        (-r, 0), (-r * 0.16, -r * 0.16)), col, alfa=alfa)


def pajaro_v(lz, x, y, s, t, col=(40, 34, 84), fase=0.0):
    """Ave lejana en 'V' que bate las alas."""
    a = 0.45 * math.sin(t * 9 + fase)
    for lado in (-1, 1):
        lz.relleno(poli((0, 0), (lado * 20 * s, (-14 - 16 * a) * s), (lado * 42 * s, (-2 + 10 * a) * s),
                        (lado * 20 * s, (-4 - 8 * a) * s)), col)


# ------------------------------------------------------------------ persona
def persona(lz, x, y, s=1.0, t=0.0, *, ph=0.0, paso=0.0, mirar=1, piel=PIEL[1], pelo=(58, 40, 44), pelo_t="corto",
            ropa=(226, 120, 72), ropa2=None, falda=0.0, cinto=None, sombrero=None, brazos=None, boca=0.0,
            ceja=0.0, obj_d=None, obj_i=None, inc=0.0, salto=0.0, sombra=0.28, sentado=False, barba=False,
            capa_=None, extra_torso=None, ojo=1.0, fijo_i=False, fijo_d=False):
    """Personaje de perfil (origen en los pies, ~230 px de alto a s=1). ph = fase de la caminata (rad; que avance con
    la posición para que los pies no resbalen), paso = amplitud 0..1, mirar = +1 derecha / -1 izquierda.
    brazos = (lejano_hombro, lejano_codo, cercano_hombro, cercano_codo): ángulos (rad) desde colgando; + = hacia delante.
    obj_d / obj_i: callables lz -> None dibujados en la mano cercana / lejana (coordenadas locales de la mano)."""
    d = 1 if mirar >= 0 else -1
    ropa2 = ropa2 or oscurecer(ropa, 0.42)
    piel_s = oscurecer(piel, 0.18)
    respira = 1.6 * math.sin(t * 2.4)
    cadera_y = -96 + (0 if sentado else 0)
    with lz.grupo(x, y - salto, s):
        if sombra > 0 and salto < 400:
            lz.relleno(elipse(0, 4 + salto, 44 * (1 - min(0.5, salto / 500)), 9, 0, 28), (14, 12, 44), alfa=sombra)
        # ---- piernas
        bob = -4.0 * abs(math.sin(ph)) * paso
        hip = (0.0, cadera_y + bob)
        for i in (1, 0):                                  # 1 = pierna lejana (primero), 0 = cercana
            f = ph + i * PI
            if sentado:
                th, k = (1.35 if i == 0 else 1.15), 1.35
            else:
                th = 0.62 * math.sin(f) * paso
                k = 0.95 * paso * max(0.0, math.sin(f + 2.0 - PI / 2 + 0.6)) + 0.1 * paso
            kx = hip[0] + 47 * math.sin(th) * d
            ky = hip[1] + 47 * math.cos(th)
            if sentado:
                kx, ky = hip[0] + 47 * d * (1.0 if i == 0 else 0.85), hip[1] + 8
            ang2 = th - k
            fx = kx + 46 * math.sin(ang2) * d
            fy = ky + 46 * math.cos(ang2)
            if sentado:
                fx, fy = kx + 8 * d, ky + 46
            col = ropa2 if falda < 0.6 else piel_s
            if i == 1:
                col = oscurecer(col, 0.22)
            lz.relleno(capsula(hip[0], hip[1], kx, ky, 24, 21), col)
            lz.relleno(capsula(kx, ky, fx, fy, 21, 17), col if falda < 0.9 else piel_s)
            lz.relleno(elipse(fx + 8 * d, fy + 3, 17, 8.5, (ang2 * 0.4) * d, 18),
                       oscurecer(cinto or (110, 78, 62), 0.05 + 0.2 * i))
        # ---- tronco y brazos (grupo con inclinación)
        with lz.grupo(hip[0], hip[1], 1.0, inc * d):
            torso_h = 84
            top = -torso_h + respira * 0.4
            # brazo lejano
            if brazos is None:
                sw = math.sin(ph) * paso
                A = (0.6 * sw + 0.05, 0.3 + 0.25 * max(0, sw), -0.6 * sw + 0.05, 0.3 + 0.25 * max(0, -sw))
            else:
                A = brazos
            sh_x, sh_y = -3 * d, top + 14

            def brazo(a1, a2, col, mano, cerca):
                ex = sh_x + 43 * math.sin(a1) * d
                ey = sh_y + 43 * math.cos(a1)
                hx = ex + 40 * math.sin(a1 + a2) * d
                hy = ey + 40 * math.cos(a1 + a2)
                lz.relleno(capsula(sh_x, sh_y, ex, ey, 19, 16), col)
                lz.relleno(capsula(ex, ey, hx, hy, 16, 14), col if falda < 2 else piel)
                lz.relleno(circulo(hx, hy, 9.5, 14), piel if cerca else piel_s)
                return hx, hy, a1 + a2

            manga_l = oscurecer(ropa, 0.28)
            hxl, hyl, al = brazo(A[0], A[1], manga_l, piel_s, False)
            if obj_i is not None:
                with lz.grupo(hxl, hyl, 1.0, 0.0 if fijo_i else -al * d):
                    obj_i(lz)
            # torso
            torso = rect_red(-25, top, 50, torso_h + 6, 23)
            lz.relleno(torso, ropa)
            lz.relleno(rect_red(4 * d - 4 + (0 if d > 0 else -22), top + 6, 26, torso_h - 6, 13), oscurecer(ropa, 0.22), alfa=0.55)
            if falda > 0.05:
                fl = 30 + 58 * falda
                lz.relleno(poli((-27, -22), (27, -22), (34, -22 + fl), (-34, -22 + fl)), ropa2)
                lz.relleno(poli((-27, -22), (-10, -22), (-16, -22 + fl), (-34, -22 + fl)), oscurecer(ropa2, 0.15), alfa=0.6)
            if cinto is not None:
                lz.relleno(rect_red(-26, -22, 52, 11, 5), cinto)
            if extra_torso is not None:
                extra_torso(lz, top, d)
            # brazo cercano
            hxr, hyr, ar = brazo(A[2], A[3], ropa, piel, True)
            if obj_d is not None:
                with lz.grupo(hxr, hyr, 1.0, 0.0 if fijo_d else -ar * d):
                    obj_d(lz)
            # ---- cabeza
            hc = (5 * d, top - 22 + respira * 0.3)
            lz.relleno(rect_red(hc[0] - 9, top - 8, 18, 18, 6), piel_s)              # cuello
            lz.relleno(circulo(hc[0] - 8 * d, hc[1] + 5, 6.5, 12), piel_s)            # oreja
            lz.relleno(circulo(hc[0], hc[1], 27, 40), piel)
            lz.relleno(circulo(hc[0] + 26.5 * d, hc[1] + 4, 4.6, 10), piel)           # nariz
            _pelo(lz, hc, d, pelo, pelo_t)
            if barba:
                a = np.linspace(0.2, PI - 0.1, 12)
                bp = np.stack([hc[0] + d * 26 * np.cos(a) * 1.0, hc[1] + 2 + 26 * np.sin(a)], 1)
                lz.relleno(np.concatenate([bp, np.stack([hc[0] + d * 16 * np.cos(a[::-1]), hc[1] + 6 + 15 * np.sin(a[::-1])], 1)]), pelo)
            # cara: ojo, ceja, boca
            bl = 1.0 if (t % 3.3) > 0.13 else 0.15
            ex, ey = hc[0] + 12 * d, hc[1] - 3
            lz.relleno(elipse(ex, ey, 3.7 * ojo, 4.4 * ojo * bl, 0, 14), TINTA)
            if ceja != 0 or True:
                lz.relleno(capsula(ex - 7 * d, ey - 10 - 2 * ceja, ex + 6 * d, ey - 10 + 2 * ceja, 3.2, 3.2, 5), oscurecer(pelo, 0.1))
            my = hc[1] + 13
            if boca > 0.05:
                lz.relleno(elipse(hc[0] + 14 * d, my + 2, 5.5, 2.5 + 6 * boca, 0, 16), (120, 40, 56))
            else:
                lz.relleno(capsula(hc[0] + 9 * d, my, hc[0] + 18 * d, my - 1.5, 2.6, 2.6, 5), (150, 70, 74))
            if sombrero is not None:
                sombrero(lz, hc, d)
    return None


def _pelo(lz, hc, d, col, tipo):
    cx, cy = hc
    if tipo == "calvo":
        return
    if tipo in ("corto", "largo", "moño", "rizos"):
        a = np.linspace(-0.30, -PI - 0.80 if tipo != "largo" else -PI - 1.3, 24)
        R = 29.5
        outer = np.stack([cx + d * R * np.cos(a), cy + R * np.sin(a)], 1)
        fin = a[-1]
        inner = np.array([[cx + d * (R * 0.55) * math.cos(fin), cy + (R * 0.55) * math.sin(fin)],
                          [cx + d * -4, cy - 6], [cx + d * 12, cy - 14], [cx + d * 24, cy - 12]])
        lz.relleno(np.concatenate([outer, inner]), col)
        if tipo == "largo":
            lz.relleno(capsula(cx - 20 * d, cy - 4, cx - 24 * d, cy + 52, 22, 15), col)
        if tipo == "moño":
            lz.relleno(circulo(cx - 16 * d, cy - 32, 11, 16), col)
        if tipo == "rizos":
            for j in range(6):
                aa = -0.2 - j * 0.55
                lz.relleno(circulo(cx + d * 28 * math.cos(aa), cy + 28 * math.sin(aa), 8.5, 12), col)


# ------------------------------------------------------------------ animales sencillos
def buey(lz, x, y, s=1.0, t=0.0, ph=0.0, mirar=1, col=(150, 96, 70), paso=1.0):
    d = 1 if mirar >= 0 else -1
    with lz.grupo(x, y, s):
        lz.relleno(elipse(0, 3, 70, 9, 0, 24), (14, 12, 44), alfa=0.25)
        bob = -3 * abs(math.sin(ph)) * paso
        for i, off in enumerate((-46, -24, 26, 48)):          # patas
            f = ph + (i % 2) * PI
            a = 0.5 * math.sin(f) * paso
            lz.relleno(capsula(off * d, -62 + bob, (off + 60 * math.sin(a) * 0.5) * d, -6 - 8 * max(0, math.sin(f + 1.2)) * paso, 18, 14),
                       oscurecer(col, 0.32 if i in (0, 2) else 0.12))
        lz.relleno(elipse(0, -92 + bob, 78, 44, 0, 36), col)
        lz.relleno(elipse(-10 * d, -84 + bob, 66, 30, 0, 30), oscurecer(col, 0.16), alfa=0.6)
        lz.relleno(circulo(32 * d, -112 + bob, 30, 22), oscurecer(col, 0.1))                # joroba
        hx = 84 * d
        lz.relleno(capsula(52 * d, -104 + bob, hx, -86 + bob, 34, 32), col)                # cuello
        lz.relleno(elipse(hx + 14 * d, -76 + bob, 26, 20, 0.2 * d, 20), aclarar(col, 0.12))  # cabeza
        lz.relleno(elipse(hx + 34 * d, -68 + bob, 12, 9, 0, 14), (232, 190, 170))
        lz.relleno(circulo(hx + 8 * d, -84 + bob, 3.6, 10), TINTA)
        lz.relleno(capsula(hx - 2 * d, -98 + bob, hx + 16 * d, -122 + bob, 8, 5), (246, 232, 206))  # cuerno
        lz.relleno(capsula(-72 * d, -98 + bob, -84 * d, -60 + bob + 6 * math.sin(t * 5), 7, 5), oscurecer(col, 0.3))  # cola


# ------------------------------------------------------------------ poses
def brazos_marcha(ph, paso):
    sw = math.sin(ph) * paso
    return (0.6 * sw + 0.05, 0.3 + 0.25 * max(0, sw), -0.6 * sw + 0.05, 0.3 + 0.25 * max(0, -sw))


def mezcla_brazos(A, B, u):
    return tuple(a + (b - a) * u for a, b in zip(A, B))


def ik(x, y, s, mirar, objetivo, subir=True):
    """Ángulos (hombro, codo) del brazo de `persona` (pies en x,y; escala s) para que la mano llegue a `objetivo`."""
    d = 1 if mirar >= 0 else -1
    sx, sy = x - 3 * d * s, y - 166 * s
    X, Y = (objetivo[0] - sx) * d / s, (objetivo[1] - sy) / s
    L1, L2 = 43.0, 40.0
    r = min(math.hypot(X, Y), L1 + L2 - 0.6)
    phi = math.atan2(X, Y)
    c = (r * r - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    a2 = math.acos(max(-1.0, min(1.0, c)))
    a1 = phi - math.atan2(L2 * math.sin(a2), L1 + L2 * math.cos(a2))
    return a1, a2


def mano_pos(x, y, s, mirar, a1, a2):
    d = 1 if mirar >= 0 else -1
    sx, sy = x - 3 * d * s, y - 166 * s
    return (sx + s * d * (43 * math.sin(a1) + 40 * math.sin(a1 + a2)), sy + s * (43 * math.cos(a1) + 40 * math.cos(a1 + a2)))
