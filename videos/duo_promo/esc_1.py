# -*- coding: utf-8 -*-
"""Primera mitad del anuncio de Dúo (plano secuencia, tiempo global):
  intro(): gancho (la plática de «a ver cuándo salimos») -> los dos avatares se funden en el logo (app_0)
  telefonos(): el teléfono de Ana (misiones, barra) y el de Leo (detalles, ciclo), con una cámara que los recorre
  frente(): plano delantero de esas escenas (utilería grande, avatares que llenan la barra, festejo, corazón que viaja)
"""
import math

import numpy as np

from duo import (A, AV_A, AV_L, B, BG, BLANCO, CARD, GOLD, H, INK, LINE, MUT, O, TEL_H, TEL_W, W, P, ancho_texto, avatar,
                 burst, calendario, clamp, e_in, e_io, e_out, encabezado, envolver, float_xp, fondo_app, golpe, h2,
                 hexa, kf, lerp, logo, mision, orbe, pestanas, pill, pop, pr, rnd, smooth, sobre, tarjeta, tarjeta_xp, telefono,
                 toast, vuelo, ww, _corazon, boton, MISIONES)

K = 1.92                                   # escala de la pantalla del teléfono (px CSS -> px)
ANA = (540.0, 990.0)                       # centro del teléfono de Ana en el «mundo»
LEO = (1560.0, 990.0)                      # el de Leo, a la derecha

# ------------------------------------------------------------------ anclas
g_dec, g_aver, g_cuan, g_sal = ww("gancho", 0, "decimos"), ww("gancho", 0, "a ver"), ww("gancho", 0, "cuando"), ww("gancho", 0, "salimos")
g_y, g_nunca = ww("gancho", 1, "y"), ww("gancho", 1, "nunca")
a_hasta, a_llego, a_duo = ww("app", 0, "hasta"), ww("app", 0, "llego"), ww("app", 0, "duo")
a_cada, a_mis, a_jun = ww("app", 1, "cada"), ww("app", 1, "misiones"), ww("app", 1, "juntos")
a_cenar, a_cel = ww("app", 2, "cenar"), ww("app", 2, "celulares")
a_abr, a_20, a_seg = ww("app", 2, "abrazo"), ww("app", 2, "20"), ww("app", 2, "segundos")
a_bai, a_sala = ww("app", 2, "bailar"), ww("app", 2, "sala")
b_cada, b_exp, b_barra, b_llen, b_entre, b_dos = (ww("barra", 0, w) for w in ("cada", "experiencia", "barra", "llenamos", "entre", "dos"))
b_llena, b_sub, b_niv = ww("barra", 1, "llena"), ww("barra", 1, "subimos"), ww("barra", 1, "nivel")
d_hay, d_cons, d_otro = ww("detalle", 0, "hay"), ww("detalle", 0, "consentir"), ww("detalle", 0, "otro")
d_cal, d_ciclo, d_se, d_llev, d_cali = (ww("detalle", 0, w) for w in ("calendario", "ciclo", "se", "llevarle", "calientito"))
d_ahora, d_acu = ww("detalle", 1, "ahora"), ww("detalle", 1, "acuerda")
T_BARRA, T_DET, T_AJ = 18.0, 25.0, 35.0

C1, C2, C3 = a_cel + 0.15, a_seg + 0.10, a_sala + 0.08          # se marcan las tres misiones
C_CAL = d_cali + 0.10                                             # se marca la de la bebida caliente
T_LIKE = d_ahora


# ------------------------------------------------------------------ cámara del mundo de los teléfonos
class Cam:
    def __init__(self, z, cx, cy):
        self.z, self.cx, self.cy = z, cx, cy

    def a(self, x, y):
        return W / 2 - self.cx * self.z + x * self.z, H / 2 - self.cy * self.z + y * self.z


def camara(t):
    z = kf(t, [(9.5, 1.0), (17.95, 1.035), (18.0, 1.035), (18.8, 1.45), (T_DET, 1.45), (T_DET + 0.8, 1.0), (d_cal - 0.05, 1.0),
               (d_cal + 0.55, 1.42), (d_se - 0.1, 1.42), (d_se + 0.45, 1.0), (31.75, 1.0), (32.55, 0.58), (34.8, 0.61)])
    cx = kf(t, [(T_DET, 540.0), (T_DET + 0.8, LEO[0]), (31.75, LEO[0]), (32.55, 1050.0)])
    cy = kf(t, [(18.0, 960.0), (18.8, 700.0), (T_DET, 700.0), (T_DET + 0.8, 960.0), (d_cal - 0.05, 960.0), (d_cal + 0.55, 1172.0),
                (d_se - 0.1, 1172.0), (d_se + 0.45, 960.0), (31.75, 960.0), (32.55, 1010.0)])
    return Cam(z, cx, cy)


def y_tel_ana(t):
    """El teléfono de Ana sube desde abajo (app_1) y ambos caen al irse (ajusta)."""
    return ANA[1] + 1900 * (1 - e_out(pr(t, a_cada - 0.05, a_cada + 0.75))) + caida(t)


def caida(t):
    return 2300 * e_in(pr(t, T_AJ - 0.45, T_AJ + 0.35))


def css_a(cam, tel, t, xc, yc):
    """Px CSS de la pantalla de un teléfono -> px de pantalla."""
    cx, cy = (ANA[0], y_tel_ana(t)) if tel == "ana" else (LEO[0], LEO[1] + caida(t))
    return cam.a(cx - TEL_W * K / 2 + xc * K, cy - TEL_H * K / 2 + yc * K)


# ------------------------------------------------------------------ datos de la semana (teléfono de Ana)
def cuenta(t, t0, dur=0.65):
    return e_out(pr(t, t0, t0 + dur))


def xp_ana(t):
    xp = 180 + 25 * sum(cuenta(t, c + 0.62) for c in (C1, C2, C3))
    return xp + (450 - 255) * e_io(pr(t, b_exp, b_llena))


def por_ana(t):
    n = sum(cuenta(t, c + 0.62) for c in (C1, C2, C3))
    u = e_io(pr(t, b_exp, b_llena))
    return 95 + 25 * n + (230 - 170) * u, 85 + (220 - 85) * u


DIAS_T = (b_exp + 0.3, b_llen, b_dos + 0.2)        # el time-lapse de la semana: X, J y V se llenan


def dias_ana(t):
    n = sum(1 for c in (C1, C2, C3) if t >= c + 0.62)
    m = min(1.0, 0.25 + 0.25 * n)
    d = [1.0, m]
    for td in DIAS_T:
        d.append(clamp(pr(t, td - 0.5, td)))
    return d + [0.0, 0.0]


def hoy_ana(t):
    return 1 + sum(1 for td in DIAS_T if t >= td - 0.5)


MIS_Y0 = 412


def alto_m(mid):
    lineas = envolver(MISIONES[mid][1], 15, "s", 364 - 28 - 46 - 14 - 44 - 14)
    return 14 + max(46, len(lineas) * 21 + 8 + 19) + 14


def ys_misiones(ids, y0=MIS_Y0, gap=10):
    ys, y = [], y0
    for m in ids:
        ys.append(y)
        y += alto_m(m) + gap
    return ys


ANA_IDS = ("tie1", "afe2", "div2")
ANA_YS = ys_misiones(ANA_IDS)


def subir(t, t0, dur=0.5):
    """La entrada `rise` de la app: (opacidad, desplazamiento en y)."""
    u = e_out(pr(t, t0, t0 + dur))
    return smooth(pr(t, t0, t0 + dur * 0.8)), 18 * (1 - u)


def orbes_a_barra(p, t, t0, x, y, xb, yb, n=6, sem=0):
    for i in range(n):
        v = vuelo(t, t0 + 0.05 * i, 0.55, (x + (rnd(i, sem) - 0.5) * 30, y), (xb, yb), curva=-60 - 50 * rnd(i, sem + 1))
        if v:
            orbe(p, v[0], v[1], 1 - 0.3 * v[2], 7)


# ------------------------------------------------------------------ pantallas (px CSS)
def home_ana(p, t):
    fondo_app(p, t)
    av = smooth(pr(t, a_cada + 0.72, a_cada + 0.8))
    p.texto("Semana del 12 oct", 18, 62, 13, MUT, "s", 1, "lm")
    p.texto("Hola, Ana", 18, 92, 26, INK, "x", 1, "lm")
    avatar(p, 400 - 18 - 19 - 28, 80, "A", AV_A, 19, av)
    avatar(p, 400 - 18 - 19, 80, "L", AV_L, 19, av)
    llena = smooth(pr(t, b_llena, b_llena + 0.3))
    s_bar = 1.0 + 0.10 * math.sin(math.pi * pr(t, b_llena, b_llena + 0.45))
    with p.pivote(200, 128 + 71, s_bar):
        alto, (bx0, by0, bx1, by1), dA, dL = tarjeta_xp(
            p, 18, 128, t, xp_ana(t), nivel=4 if t >= b_niv else 3, racha=4, dias=dias_ana(t), por=por_ana(t), llena=llena,
            hoy=hoy_ana(t), lleno_t=[None, C3 + 0.62] + list(DIAS_T) + [None, None], nivel_pop=b_niv)
    frac = xp_ana(t) / 450
    hechas = sum(1 for c in (C1, C2, C3) if t >= c)
    op, dy = subir(t, a_mis - 0.15)
    h2(p, "Tus misiones de hoy", 392 + dy, op, f"{hechas}/3")
    for i, (mid, y, c) in enumerate(zip(ANA_IDS, ANA_YS, (C1, C2, C3))):
        op, dy = subir(t, a_mis + 0.08 * (i + 1))
        mision(p, 18, y + dy, mid, t, c, op)
        yc = y + alto_m(mid) / 2
        float_xp(p, "+25 XP", 346, yc - 30, t, c)
        orbes_a_barra(p, t, c + 0.05, 346, yc, bx0 + (bx1 - bx0) * min(1, frac), (by0 + by1) / 2, sem=i * 3)
    pestanas(p, "Misiones", t, smooth(pr(t, a_cada + 0.5, a_cada + 0.9)))


def home_ana_tarde(p, t):
    """Ana, más tarde (se ve en la toma de los dos teléfonos): la misión que Leo hizo por ella, con su corazón."""
    fondo_app(p, t)
    encabezado(p, "Ana", "Semana del 12 oct", t, 1, "L", AV_A, AV_L)
    tarjeta_xp(p, 18, 128, t, 465 if t >= C_CAL + 0.6 else 450, nivel=4, racha=4, dias=[1, 1, 1, 1, 1, 0, 0], por=(230, 220 + (15 if t >= C_CAL + 0.6 else 0)),
               llena=1.0, hoy=4)
    h2(p, "Leo hoy", 392, 1, "1/3")
    mision(p, 18, 412, "afe20", t, t_check=0.0, hecha_por="Leo", t_like=T_LIKE)
    mision(p, 18, 412 + alto_m("afe20") + 10, "com8", t, None, 0.5, hecha_por="Leo", t_like=None)
    pestanas(p, "Misiones", t)


LEO_IDS = ("afe1", "equ1")


def home_leo(p, t, dx=0.0):
    with p.grupo(dx, 0):
        encabezado(p, "Leo", "Semana del 12 oct", t, 1, "A", AV_L, AV_A)
        xp = 450 + 15 * cuenta(t, C_CAL + 0.62)
        alto, (bx0, by0, bx1, by1), _, _ = tarjeta_xp(p, 18, 128, t, xp, nivel=4, racha=4, dias=[1, 1, 1, 1, 1, 0, 0],
                                                       por=(230, 220 + 15 * cuenta(t, C_CAL + 0.62)), llena=1.0, hoy=4, nombres=("Ana", "Leo"))
        nueva = t >= d_se + 0.2
        hechas = 1 if t >= C_CAL else 0
        h2(p, "Tus misiones de hoy", 392, 1, f"{hechas}/{3 if nueva else 2}")
        foco = ("Ana está en su periodo: hoy cuenta más el cuidado." if nueva else "Elegidas para Ana. Ahora le sumaría más: Afecto y detalles.")
        p.parrafo(envolver(foco, 13, "m", 356), 22, 410, 13, 19, MUT, "m")
        y0 = 456
        corr = alto_m("afe20") + 10
        if nueva:
            op, dy = subir(t, d_se + 0.25)
            yy = y0
            s = 1.0
            mision(p, 18, yy + dy, "afe20", t, C_CAL, op)
            yc = yy + alto_m("afe20") / 2
            float_xp(p, "+15 XP", 346, yc - 30, t, C_CAL)
            orbes_a_barra(p, t, C_CAL + 0.05, 346, yc, bx1 - 4, (by0 + by1) / 2, sem=11)
            desp = corr * e_out(pr(t, d_se + 0.2, d_se + 0.6))
        else:
            desp = 0.0
        for i, mid in enumerate(LEO_IDS):
            op, dy = subir(t, d_cons + 0.08 * i)
            mision(p, 18, y0 + desp + dy + i * (alto_m(LEO_IDS[0]) + 10), mid, t, None, op)


def ciclo_leo(p, t, dx=0.0):
    with p.grupo(dx, 0):
        p.texto("Calendario de Ana", 18, 62, 13, MUT, "s", 1, "lm")
        p.texto("Ciclo", 18, 92, 26, INK, "x", 1, "lm")
        tarjeta(p, 18, 120, 382, 322, 22)
        p.emoji("🩸", 200, 160, 40)
        p.texto("Menstruación", 200, 208, 24, INK, "x")
        p.texto("Ana · Día 2 de su periodo", 200, 238, 14, MUT, "m")
        p.rect(36, 260, 364, 261.5, LINE)
        p.emoji("💡", 46, 284, 15)
        p.parrafo(envolver("Calor, su antojo favorito o encargarte de la casa valen oro.", 13.5, "m", 300), 64, 273, 13.5, 19, INK, "m")
        h2(p, "Calendario", 350, 1, "ciclo de ~28 días")
        calendario(p, 18, 370, t, pulso=d_ciclo)


def pantalla_leo(p, t):
    fondo_app(p, t)
    u1 = e_io(pr(t, d_cal - 0.15, d_cal + 0.25))          # Misiones -> Ciclo
    u2 = e_io(pr(t, d_se - 0.2, d_se + 0.2))               # Ciclo -> Misiones
    u = u1 * (1 - u2)
    if u < 1:
        home_leo(p, t, -400 * u)
    if u > 0:
        ciclo_leo(p, t, 400 * (1 - u))
    if t < d_se - 0.2:
        pestanas(p, "Ciclo" if t >= d_cal - 0.15 else "Misiones", t, t_cambio=d_cal - 0.15, de="Misiones")
    else:
        pestanas(p, "Misiones", t, t_cambio=d_se - 0.2, de="Ciclo")
    if t >= d_acu - 0.1:                                    # el aviso que le llega a Leo
        k = e_out(pr(t, d_acu - 0.1, d_acu + 0.3))
        toast(p, "A Ana le encantó lo que hiciste · +5 XP", 200, -50 + 104 * k, k, 12.5, "❤️")


# ------------------------------------------------------------------ gancho: la plática de siempre
MENSAJES = [   # (quién, texto, emoji, segundo)
    ("L", "¿Salimos el sábado?", "🍝", 0.55),
    ("A", "¡Sí! A ver cuándo", "😅", None),
    ("-", "22 de septiembre", None, None),
    ("A", "¿Y si vamos al cine?", "🍿", None),
    ("L", "A ver cuándo…", None, None),
    ("-", "6 de octubre", None, None),
    ("L", "Este finde sí, ¿eh?", "💪", None),
    ("A", "A ver cuándo", "🙃", None),
]
TS_MSG = [0.55, 1.25, g_dec + 0.25, g_dec + 0.45, g_aver + 0.05, g_cuan - 0.1, g_cuan + 0.05, g_sal + 0.25]
PXM = 46


def burbuja(p, quien, txt, emo, y, t, ta, apagar):
    op = smooth(pr(t, ta, ta + 0.18)) * (1 - 0.45 * apagar)
    if op <= 0.004:
        return 0
    if quien == "-":
        p.texto(txt.upper(), 540, y + 34, 24, MUT, "b", op, esp=0.12)
        return 70
    s = 0.5 + 0.5 * pop(t, ta, 0.30)
    wt = ancho_texto(txt, PXM, "s") + (PXM * 1.45 if emo else 0)
    h = 110
    izq = quien == "A"
    col = sobre(AV_A, CARD, 0.24) if izq else sobre(AV_L, CARD, 0.30)
    x0 = 148 if izq else 932 - wt - 60
    x1 = x0 + wt + 60
    ax = 84 if izq else 996
    with p.pivote(x0 if izq else x1, y + h / 2, s):
        p.sombra(x0, y, x1, y + h, 36, blur=26, op=0.5 * op, dy=10)
        p.rrect(x0, y, x1, y + h, 36, col, op, borde=sobre(AV_A if izq else AV_L, CARD, 0.45), w=2)
        p.texto(txt, x0 + 30, y + h / 2 + 1, PXM, INK, "s", op, "lm")
        if emo:
            p.emoji(emo, x1 - 30 - PXM * 0.55, y + h / 2, PXM * 1.1, op)
    avatar(p, ax, y + h - 28, quien, AV_A if izq else AV_L, 28, op * s, BG, 3)
    return h + 22


def escribiendo(p, quien, y, t, ta):
    """Los tres puntitos de «escribiendo…» justo antes de cada mensaje."""
    if not (ta - 0.32 <= t < ta):
        return
    op = smooth(pr(t, ta - 0.32, ta - 0.22))
    izq = quien == "A"
    x0 = 148 if izq else 932 - 130
    p.rrect(x0, y + 12, x0 + 140, y + 98, 34, sobre(AV_A if izq else AV_L, CARD, 0.2), op)
    for k in range(3):
        b = 0.5 + 0.5 * math.sin(t * 16 - k * 1.1)
        p.circ(x0 + 42 + 28 * k, y + 55 - 7 * b, 9, MUT, op * (0.5 + 0.5 * b))


DIAS_GANCHO = [("SÁB", "13", 70, 260, 0.9), ("DOM", "21", 990, 640, 1.6), ("VIE", "26", 92, 1240, 2.4), ("SÁB", "4", 980, 1500, 3.1),
               ("DOM", "12", 120, 1720, 3.7), ("VIE", "10", 960, 160, 4.4)]


def hojas_calendario(p, t, op):
    """Plano medio del gancho: hojitas de calendario que suben despacio y se van tachando (los planes que no se hicieron)."""
    for i, (dn, num, x, y, tx) in enumerate(DIAS_GANCHO):
        yy = y - t * (18 + 10 * rnd(i, 4)) + 8 * math.sin(t * 0.8 + i)
        o = op * 0.55 * (0.7 + 0.3 * rnd(i, 7))
        s = 0.85 + 0.25 * rnd(i, 8)
        with p.pivote(x, yy, s):
            p.rrect(x - 58, yy - 64, x + 58, yy + 64, 18, sobre(LINE, BG, 0.8), o)
            p.rrect(x - 58, yy - 64, x + 58, yy - 26, 18, sobre(A, BG, 0.35), o)
            p.rect(x - 58, yy - 40, x + 58, yy - 26, sobre(A, BG, 0.35), o)
            p.texto(dn, x, yy - 45, 20, INK, "x", o, esp=0.08)
            p.texto(num, x, yy + 18, 46, MUT, "x", o)
            u = e_out(pr(t, tx, tx + 0.3))
            if u > 0:
                p.polilinea([(x - 34, yy - 10), (x - 34 + 68 * u, yy - 10 + 56 * u)], 6, A, o * 1.3)
                if u >= 1:
                    v = e_out(pr(t, tx + 0.25, tx + 0.5))
                    p.polilinea([(x + 34, yy - 10), (x + 34 - 68 * v, yy - 10 + 56 * v)], 6, A, o * 1.3)


def sep_logo(t, r):
    return r * 0.88 - r * 0.11 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 3.2))


def intro(p, t):
    """0 s -> app_1: plática, «nunca salimos», y los dos círculos que se funden en el logo."""
    if t > a_cada + 0.8:
        return
    # --- hojas de calendario (plano medio)
    hojas_calendario(p, t, 1 - smooth(pr(t, 6.6, 7.3)))
    # --- avatares -> logo
    r = kf(t, [(6.85, 100.0), (a_duo, 150.0)], e_io)
    cy = kf(t, [(6.85, 470.0), (a_duo, 790.0)], e_io)
    sep_g = 580 + 60 * e_io(pr(t, g_nunca, g_nunca + 0.8))
    um = e_io(pr(t, 6.85, a_duo))
    sep = lerp(sep_g, sep_logo(t, 150.0), um)
    s_in = pop(t, 0.1, 0.4)
    bob = 7 * math.sin(t * 1.9) * (1 - um)
    if t < a_cada - 0.02:
        caida_ = 0.06 * smooth(pr(t, g_nunca, g_nunca + 0.6)) * (1 - um)
        with p.pivote(540, cy, s_in * (1 - caida_)):
            if sep < 2 * r:
                logo(p, 540, cy + bob, r, t, 1.0, sep=sep, respira=False)
            else:
                p.glow(540 - sep / 2, cy + bob, r * 2.2, AV_A, 0.18, 1.6)
                p.glow(540 + sep / 2, cy - bob, r * 2.2, AV_L, 0.18, 1.6)
                p.circ(540 - sep / 2, cy + bob, r, AV_A)
                p.circ(540 + sep / 2, cy - bob, r, AV_L)
            ol = 1 - smooth(pr(t, a_hasta, a_llego))
            p.texto("A", 540 - sep / 2, cy + bob + 4, r * 0.85, BLANCO, "x", ol)
            p.texto("L", 540 + sep / 2, cy - bob + 4, r * 0.85, BLANCO, "x", ol)
            on = 1 - smooth(pr(t, 6.7, 7.0))
            p.texto("Ana", 540 - sep / 2, cy + r + 46, 34, MUT, "b", on)
            p.texto("Leo", 540 + sep / 2, cy + r + 46, 34, MUT, "b", on)
        if t >= a_duo:
            p.glow(540, cy, 420, (1.0, 0.6, 0.9), 0.30 * math.exp(-(t - a_duo) * 2.5), 1.5)
    else:                                                   # los círculos vuelan a los avatares del teléfono
        cam = camara(t)
        u = e_io(pr(t, a_cada - 0.02, a_cada + 0.75))
        xa, ya = css_a(cam, "ana", t, 400 - 18 - 19 - 28, 80)
        xl, yl = css_a(cam, "ana", t, 400 - 18 - 19, 80)
        rr = lerp(150, 19 * K, u)
        s0 = sep_logo(a_cada, 150.0)
        p.circ(lerp(540 - s0 / 2, xa, u), lerp(790, ya, u), rr, AV_A)
        p.circ(lerp(540 + s0 / 2, xl, u), lerp(790, yl, u), rr, AV_L)
    # --- burbujas
    apagar = smooth(pr(t, g_nunca - 0.1, g_nunca + 0.4))
    sale = e_in(pr(t, 6.55, 7.15))
    y = 650
    alturas = []
    for (q, txt, emo, _), ta in zip(MENSAJES, TS_MSG):
        alturas.append((y, ta, q))
        y += 70 if q == "-" else 132
    ult = max([yy + 110 for yy, ta, q in alturas if t >= ta - 0.3] + [800])
    scroll = max(0.0, ult - 1640)
    ob = 1 - smooth(pr(t, 6.6, 7.05))
    if ob > 0:
        with p.grupo(0, -scroll + 900 * sale):
            for (q, txt, emo, _), (yy, ta, _) in zip(MENSAJES, alturas):
                if q != "-":
                    escribiendo(p, q, yy, t, ta)
                burbuja(p, q, txt, emo, yy, t, ta, apagar + (1 - ob) * 2.3)
    # --- el aviso: «pospuesto 7 veces»
    if g_nunca - 0.05 <= t < 7.3:
        k = e_out(pr(t, g_nunca - 0.05, g_nunca + 0.3)) * (1 - e_in(pr(t, 6.75, 7.1)))
        with p.grupo(0, -140 * (1 - k)):
            toast(p, "Plan «salir a cenar»: pospuesto 7 veces", 540, 96, k, 36, "😅")
    # --- marca
    if t >= a_duo:
        sale_m = smooth(pr(t, a_cada - 0.1, a_cada + 0.3))
        s = pop(t, a_duo, 0.42)
        with p.pivote(540, 1095, s):
            p.texto("Dúo", 540, 1095 - 60 * sale_m, 190, INK, "x", 1 - sale_m)
        op = smooth(pr(t, a_duo + 0.3, a_duo + 0.6)) * (1 - sale_m)
        p.texto("Misiones en pareja", 540, 1232 + 14 * (1 - op) - 60 * sale_m, 50, hexa("D9CCE0"), "m", op)
        burst(p, 540, 790, t, a_duo, n=46, fuerza=1.1, semilla=3, escala=1.7)


# ------------------------------------------------------------------ los teléfonos
def telefonos(p, t):
    if t < a_cada - 0.06 or t > T_AJ + 0.4:
        return
    cam = camara(t)
    with p.cam(cam.z, cam.cx, cam.cy):
        ya = y_tel_ana(t)
        if t < T_DET + 1.0 or t > 31.6:
            telefono(p, ANA[0], ya, K, t, home_ana if t < T_DET + 0.5 else home_ana_tarde)
        if t > T_DET - 0.1:
            telefono(p, LEO[0], LEO[1] + caida(t), K, t, pantalla_leo)


# ------------------------------------------------------------------ plano delantero
def utileria(p, emo, x, y, px, t, t0, t1, fase=0.0):
    """Un emoji grande que entra con rebote, flota y se va."""
    if t < t0 or t > t1 + 0.3:
        return
    s = pop(t, t0, 0.38) * (1 - e_in(pr(t, t1, t1 + 0.3)))
    yy = y + 12 * math.sin(t * 3.0 + fase)
    with p.pivote(x, yy, s):
        p.sombra(x - px * 0.35, yy - px * 0.2, x + px * 0.35, yy + px * 0.5, px * 0.3, blur=24, op=0.45, dy=18)
        p.emoji(emo, x, yy, px)


def frente(p, t):
    if t < a_cada or t > T_AJ:
        return
    cam = camara(t)
    # --- utilería de las misiones de Ana (borde del teléfono)
    if t < T_BARRA + 0.4:
        for i, (mid, y) in enumerate(zip(ANA_IDS, ANA_YS)):
            _, yc = css_a(cam, "ana", t, 200, y + alto_m(mid) / 2)
            if i == 0:
                utileria(p, "🍝", 96, yc - 20, 150, t, a_cenar, C2 - 0.6)
                utileria(p, "🕯️", 120, yc - 210, 90, t, a_cenar + 0.18, C2 - 0.6, 1.0)
                utileria(p, "📵", 990, yc - 120, 110, t, a_cel - 0.05, C2 - 0.6, 2.0)
            elif i == 1:
                utileria(p, "🤗", 975, yc, 160, t, a_abr, a_bai - 0.3)
                if a_abr <= t <= a_bai:                  # cuenta de 20 segundos
                    u = pr(t, a_abr + 0.1, a_seg + 0.1)
                    op = smooth(pr(t, a_abr, a_abr + 0.2)) * (1 - smooth(pr(t, a_bai - 0.5, a_bai - 0.2)))
                    yy = yc + 12 * math.sin(t * 3.0)
                    p.circ(975, yy, 112, LINE, op * 0.9, w=12)
                    if u > 0:
                        p.elip(975, yy, 112, 112, None, op, a0=-90, a1=-90 + 360 * u, w=12, hg=(863, 1087))
                    p.texto(f"{int(1 + 19 * u)} s", 975, yy + 150, 44, INK, "x", op)
            else:
                utileria(p, "💃", 92, yc - 10, 150, t, a_bai, T_BARRA + 0.1)
                utileria(p, "🕺", 990, yc + 30, 150, t, a_bai + 0.15, T_BARRA + 0.1, 1.5)
                for k in range(6):                       # notas que suben
                    t0 = a_bai + 0.2 + 0.25 * k
                    if t0 <= t <= t0 + 1.6:
                        u = (t - t0) / 1.6
                        x = (110 if k % 2 else 970) + 50 * math.sin(u * 6 + k)
                        p.emoji("🎵" if k % 3 else "🎶", x, yc - 100 - 380 * u, 64, math.sin(math.pi * u))
    # --- foco en la tarjeta de XP durante el zoom de la barra (velo que apaga lo de abajo)
    if 18.2 <= t <= T_DET + 0.6:
        ov = smooth(pr(t, 18.3, 18.9)) * (1 - smooth(pr(t, T_DET, T_DET + 0.5)))
        _, yv = css_a(cam, "ana", t, 200, 128 + 232 + 14)
        ys = np.arange(H, dtype=np.float32)
        a = (np.clip((ys - yv) / 140.0, 0, 1) * 0.78 * ov)[:, None, None]
        p.im *= 1 - a
        p.im += a * np.float32(BG)
    # --- la toma de los dos teléfonos: quién es quién
    if 31.9 <= t <= T_AJ:
        oq = smooth(pr(t, 32.2, 32.6)) * (1 - smooth(pr(t, T_AJ - 0.5, T_AJ - 0.2)))
        for tel, letra, col, nom in (("ana", "A", AV_A, "Ana"), ("leo", "L", AV_L, "Leo")):
            x, y = css_a(cam, tel, t, 200, -60)
            with p.pivote(x, y - 40, 0.6 + 0.4 * pop(t, 32.2, 0.4)):
                avatar(p, x - 52, y - 40, letra, col, 34, oq, BG, 4)
                p.texto(nom, x - 6, y - 38, 44, INK, "x", oq, "lm")
        # «💞 Cuentas vinculadas»: los dos teléfonos unidos por una línea punteada que corre
        xa, ya = css_a(cam, "ana", t, 200, 880)
        xl, yl = css_a(cam, "leo", t, 200, 880)
        yp = max(ya, yl) + 150
        for x0_, y0_, x1_ in ((xa, ya, 540 - 200), (xl, yl, 540 + 200)):
            n = 18
            for j in range(n):
                u = ((j + (t * 2.2) % 1.0) / n)
                bx = (1 - u) ** 2 * x0_ + 2 * u * (1 - u) * x0_ + u * u * x1_
                by = (1 - u) ** 2 * y0_ + 2 * u * (1 - u) * yp + u * u * yp
                p.circ(bx, by, 5, A if x0_ < 540 else B, oq * 0.85)
        sp = 0.6 + 0.4 * pop(t, 32.45, 0.4)
        with p.pivote(540, yp, sp):
            wt = ancho_texto("Cuentas vinculadas", 34, "x") + 34 * 1.5 + 56
            p.sombra(540 - wt / 2, yp - 40, 540 + wt / 2, yp + 40, 40, blur=26, op=0.6 * oq, dy=10)
            p.rrect(540 - wt / 2, yp - 40, 540 + wt / 2, yp + 40, 40, CARD, oq, borde=A, w=2.5)
            p.emoji("💞", 540 - wt / 2 + 28 + 22, yp, 40, oq)
            p.texto("Cuentas vinculadas", 540 - wt / 2 + 28 + 34 * 1.5, yp + 1, 34, INK, "x", oq, "lm")
    # --- «entre los dos»: Ana y Leo llenan la barra
    if b_llen - 0.3 <= t <= b_sub + 0.3:
        s_in = pop(t, b_llen - 0.3, 0.4) * (1 - e_in(pr(t, b_sub - 0.05, b_sub + 0.3)))
        xs = ((230, AV_A, "A", "Ana"), (850, AV_L, "L", "Leo"))
        xb, yb = css_a(cam, "ana", t, 18 + (364 - 36) * min(1, xp_ana(t) / 450) + 18, 128 + 71)
        for j, (x, col, letra, nom) in enumerate(xs):
            yy = 1460 + 10 * math.sin(t * 2.4 + j)
            with p.pivote(x, yy, s_in):
                p.glow(x, yy, 230, col, 0.25, 1.6)
                avatar(p, x, yy, letra, col, 84, 1.0, BG, 6)
                p.texto(nom, x, yy + 128, 38, INK, "b")
            for i in range(14):                          # chorro de orbes de cada quien hacia la barra
                t0 = b_entre - 0.4 + i * 0.12 + j * 0.06
                v = vuelo(t, t0, 0.6, (x, yy - 60), (xb, yb), curva=-120 if j == 0 else -150)
                if v:
                    p.glow(v[0], v[1], 46, col, 0.7 * (1 - 0.4 * v[2]), 1.7)
                    p.circ(v[0], v[1], 9, (1, 0.95, 0.9), 1 - 0.4 * v[2])
    # --- ¡Barra llena!
    festejo(p, t)
    # --- el té de Leo
    if t < 32.4:
        _, yc = css_a(cam, "leo", t, 200, 456 + alto_m("afe20") / 2)
        if d_llev - 0.1 <= t:
            utileria(p, "☕", 975, yc - 30, 165, t, d_llev - 0.1, 31.9)
            if t <= 32.2:
                op = smooth(pr(t, d_llev + 0.1, d_llev + 0.5)) * (1 - smooth(pr(t, 31.6, 32.0)))
                for k in range(3):
                    pts = []
                    for j in range(14):
                        v = j / 13
                        pts.append((975 - 22 + 22 * k + 14 * math.sin(v * 7 - t * 4 + k * 2), yc - 120 - 150 * v))
                    p.polilinea(pts, 16, BLANCO, 0.10 * op)
                    p.polilinea(pts, 6, BLANCO, 0.22 * op)
    # --- el corazón que viaja del teléfono de Ana al de Leo
    if T_LIKE <= t <= d_acu + 1.6:
        xa, ya = css_a(cam, "ana", t, 346, 412 + alto_m("afe20") / 2)
        xl, yl = css_a(cam, "leo", t, 200, 60)
        v = vuelo(t, T_LIKE + 0.08, d_acu - T_LIKE - 0.1, (xa, ya), (xl, yl), curva=-260)
        if v:
            s = 60 + 40 * math.sin(math.pi * v[2])
            p.glow(v[0], v[1], s * 2.2, A, 0.5, 1.6)
            p.poly(_corazon(v[0], v[1], s), hg=(v[0] - s, v[0] + s))
        if t >= d_acu - 0.1:                             # lluvia de corazones + el aviso grande
            for i in range(16):
                t0 = d_acu - 0.1 + 0.05 * i
                if t0 <= t <= t0 + 1.4:
                    u = (t - t0) / 1.4
                    x = xl + (rnd(i, 21) - 0.5) * 420 + 40 * math.sin(u * 5 + i)
                    y = yl + 140 - 420 * u * (0.6 + 0.6 * rnd(i, 22))
                    r = 16 + 22 * rnd(i, 23)
                    p.poly(_corazon(x, y, r), (A, B, O)[i % 3], math.sin(math.pi * u) * 0.9)
            k = e_out(pr(t, d_acu - 0.1, d_acu + 0.25)) * (1 - e_in(pr(t, T_AJ - 0.5, T_AJ - 0.2)))
            with p.pivote(540, 230, 0.7 + 0.3 * k):
                toast(p, "A Ana le encantó lo que hiciste · +5 XP", 540, 190, k, 38, "❤️")


def festejo(p, t):
    """El `.over` de la app al llenar la barra: velo, tarjeta que explota con 🏆, confeti."""
    if t < b_sub - 0.05 or t > T_DET + 0.45:
        return
    sale = e_in(pr(t, T_DET - 0.05, T_DET + 0.35))
    p.oscurecer(0.72 * smooth(pr(t, b_sub - 0.05, b_sub + 0.25)) * (1 - sale))
    burst(p, 540, 640, t, b_sub + 0.05, n=70, fuerza=1.2, semilla=7, dur=1.9, escala=2.0)
    s = (0.4 + 0.6 * pop(t, b_sub, 0.5)) * (1 - 0.3 * sale)
    op = smooth(pr(t, b_sub, b_sub + 0.15)) * (1 - sale)
    k = 2.4
    x0, y0 = 540 - 170 * k, 590
    with p.pivote(540, 960, s):
        with p.grupo(x0, y0, k):
            tarjeta(p, 0, 0, 340, 300, 22, op)
            b = 1 + 0.08 * math.sin(math.pi * 2 * (t - b_sub) / 1.2) ** 2
            with p.pivote(170, 70, b):
                p.emoji("🏆", 170, 70, 62, op)
            p.texto("¡Barra llena!", 170, 140, 26, INK, "x", op)
            p.texto("Completaron la meta de la semana", 170, 176, 14, MUT, "m", op)
            w1, w2 = ancho_texto("y subieron a ", 14, "m"), ancho_texto("nivel 4", 15, "x")
            xi = 170 - (w1 + w2) / 2
            p.texto("y subieron a", xi, 198, 14, MUT, "m", op, "lm")
            sn = pop(t, b_niv, 0.4)
            with p.pivote(xi + w1 + w2 / 2, 198, 0.4 + 0.6 * sn if t >= b_niv else 1.0):
                p.texto("nivel 4", xi + w1, 198, 15, INK, "x", op, "lm", hg=(xi + w1, xi + w1 + w2) if t >= b_niv else None)
            boton(p, "Seguir sumando", 24, 226, 316, 50, op, 15)
    burst(p, 120, 1700, t, b_sub + 0.18, n=40, fuerza=1.3, semilla=9, dur=1.8, escala=1.8)
    burst(p, 960, 1700, t, b_sub + 0.24, n=40, fuerza=1.3, semilla=13, dur=1.8, escala=1.8)
    burst(p, 540, 700, t, b_niv, n=34, fuerza=0.8, semilla=17, dur=1.4, escala=1.5)
