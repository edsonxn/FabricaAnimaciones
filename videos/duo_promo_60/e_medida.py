# -*- coding: utf-8 -*-
"""Escena «medida» (8-18 s): el teléfono de Ana con sus misiones del día; las respuestas del cuestionario de cada quien vuelan a
las misiones (a la medida); «📍 Estamos a distancia» parte la toma en dos teléfonos, las misiones cambian a las de distancia y
termina en una videollamada cenando «juntos». También define `home()` (pantalla de Misiones), que reusa la escena de juegos."""
import math

from comun import BETO_C, ANA_C, K, Cam, css, subir, utileria, ventana
from duo import (A, B, BG, BLANCO, CARD, CUERPO, GOLD, INK, LINE, MISIONES, MUT, OK, TEL_H, TEL_W, W, H, ancho_texto, avatar,
                 burst, e_in, e_io, e_out, envolver, fondo_app, golpe, h2, hexa, interruptor, kf, lerp, mision, pestanas, pill,
                 pop, pr, rnd, smooth, sobre, tarjeta, tarjeta_xp, telefono, toast, vuelo, ww, _corazon, palomita)

ANA_T = (540.0, 990.0)
BETO_X = 1420.0

m_cada, m_mis, m_jun = ww("medida", 0, "cada"), ww("medida", 0, "misiones"), ww("medida", 0, "juntos")
m_seg, m_cont, m_quien = ww("medida", 0, "segun"), ww("medida", 0, "contesto"), ww("medida", 0, "quien")
l_si, l_lej, l_camb = ww("medida", 1, "si"), ww("medida", 1, "lejos"), ww("medida", 1, "cambian")
l_cenar, l_vid = ww("medida", 1, "cenar"), ww("medida", 1, "videollamada")
T0, T1 = 8.0, 18.0
T_SALE = 17.35                       # se cierra la videollamada y Beto vuelve detrás de Ana


def camara(t):
    z = kf(t, [(T0, 1.0), (m_seg, 1.0), (m_seg + 0.5, 0.72), (l_lej - 0.1, 0.72), (l_lej + 0.6, 0.6), (T_SALE, 0.6), (T1, 1.0)])
    cx = kf(t, [(T0, 540.0), (m_seg, 540.0), (m_seg + 0.5, 873.0), (l_lej - 0.1, 873.0), (l_lej + 0.6, (540 + BETO_X) / 2),
                (T_SALE, (540 + BETO_X) / 2), (T1, 540.0)])
    cy = kf(t, [(T0, 960.0), (m_seg, 960.0), (m_seg + 0.5, 1010.0), (l_lej - 0.1, 1010.0), (l_lej + 0.6, 990.0), (T_SALE, 990.0),
                (T1, 960.0)])
    return Cam(z, cx, cy)


def y_ana(t):
    return ANA_T[1] + 1900 * (1 - e_out(pr(t, 7.55, 8.35)))


def x_beto(t):
    return lerp(540.0, BETO_X, e_io(pr(t, l_lej - 0.05, l_lej + 0.65))) - (BETO_X - 540) * e_io(pr(t, T_SALE, T1 - 0.05))


def tel_ana(t):
    return (ANA_T[0], y_ana(t))


def tel_beto(t):
    return (x_beto(t), ANA_T[1])


# ------------------------------------------------------------------ pantalla de Misiones (px CSS)
def alto_m(mid):
    lineas = envolver(MISIONES[mid][1], 15, "s", 364 - 28 - 46 - 14 - 44 - 14)
    return 14 + max(46, len(lineas) * 21 + 8 + 19) + 14


NORMAL = {"Ana": ("tie1", "afe2", "afe1"), "Beto": ("afe2", "equ1", "com8")}
LEJOS = {"Ana": ("tie40", "com41"), "Beto": ("tie40", "afe42")}
FOCO = {"Ana": "Elegidas para Ana según lo que contestó. Ahora le sumaría más: ⏳ Tiempo de calidad",
        "Beto": "Elegidas para Beto según lo que contestó. Ahora le sumaría más: 💝 Afecto y detalles"}
Y_MIS = 452


def ys(ids, y0=Y_MIS, gap=10):
    out, y = [], y0
    for m in ids:
        out.append(y)
        y += alto_m(m) + gap
    return out


def home(p, t, quien="Ana", t_in=None, t_cambio=None, medida=None, xp=165, checks=(), tab_op=1.0):
    """Home de la v24: encabezado, tarjeta de la semana, «Tus misiones de hoy» (foco a la medida) y las misiones.
    t_in = cuándo entran las misiones (rise); t_cambio = cambian a las de distancia (salen a la izquierda, entran por la derecha);
    medida = {índice: t} misiones que reciben la respuesta del cuestionario (barrido dorado + pill «A su medida»)."""
    fondo_app(p, t)
    yo, otro = (("A", ANA_C), ("B", BETO_C)) if quien == "Ana" else (("B", BETO_C), ("A", ANA_C))
    p.texto("Semana del 19 oct", 18, 62, 13, MUT, "s", 1, "lm")
    p.texto(f"Hola, {quien}", 18, 92, 26, INK, "x", 1, "lm")
    avatar(p, 400 - 18 - 19 - 28, 80, yo[0], yo[1], 19)
    avatar(p, 400 - 18 - 19, 80, otro[0], otro[1], 19)
    tarjeta_xp(p, 18, 128, t, xp, nivel=2, racha=7, dias=[1, 1, 0.5, 0, 0, 0, 0], por=(xp * 0.55, xp * 0.45), hoy=2,
               nombres=("Ana", "Beto"))
    lejos = t_cambio is not None and t >= t_cambio + 0.25
    ids_a, ids_b = NORMAL[quien], LEJOS[quien]
    op_h, dy_h = subir(t, t_in - 0.15) if t_in is not None else (1.0, 0.0)
    h2(p, "Tus misiones de hoy", 392 + dy_h, op_h, f"{len(checks)}/{len(ids_b) if lejos else len(ids_a)}")
    foco = FOCO[quien] if not lejos else "Están a distancia: misiones que se pueden hacer lejos."
    ofo = op_h * (1 - (smooth(pr(t, t_cambio, t_cambio + 0.15)) * (1 - smooth(pr(t, t_cambio + 0.25, t_cambio + 0.45)))
                       if t_cambio is not None else 0.0))
    lin = envolver(foco, 12.5, "m", 356)[:2]
    p.parrafo(lin, 22, 408 + dy_h, 12.5, 18, MUT, "m", ofo)
    # misiones normales (salen a la izquierda al cambiar)
    sal = e_in(pr(t, t_cambio, t_cambio + 0.4)) if t_cambio is not None else 0.0
    if sal < 1:
        for i, (mid, y) in enumerate(zip(ids_a, ys(ids_a))):
            op, dy = subir(t, t_in + 0.08 * i) if t_in is not None else (1.0, 0.0)
            dx = -440 * e_in(pr(t, (t_cambio or 0) + 0.06 * i, (t_cambio or 0) + 0.06 * i + 0.4)) if t_cambio is not None else 0.0
            with p.grupo(dx, 0):
                mision(p, 18, y + dy, mid, t, None, op)
                if medida and i in medida and t >= medida[i]:
                    tm = medida[i]
                    a = alto_m(mid)
                    if t <= tm + 0.8:
                        u = (t - tm) / 0.8
                        cx = 18 + (-0.5 + 1.7 * u) * 364
                        with p.clip(18, y, 382, y + a):
                            p.poly([(cx - 70, y + a), (cx + 20, y), (cx + 120, y), (cx + 30, y + a)], GOLD, 0.30 * math.sin(math.pi * u))
                    k = pop(t, tm, 0.3)
                    p.rrect(18, y, 382, y + a, 20, None, smooth(pr(t, tm, tm + 0.2)), borde=GOLD, w=2.2)
                    with p.pivote(382 - 12, y + 2, 0.4 + 0.6 * k):
                        pill(p, "A su medida", 382 - 12, y + 2, hexa("1A1320"), GOLD, px=11, anchor="r", emo="✨")
    # misiones de distancia (entran por la derecha)
    if t_cambio is not None and t >= t_cambio + 0.2:
        for i, (mid, y) in enumerate(zip(ids_b, ys(ids_b))):
            dx = 440 * (1 - e_out(pr(t, t_cambio + 0.2 + 0.08 * i, t_cambio + 0.65 + 0.08 * i)))
            with p.grupo(dx, 0):
                mision(p, 18, y, mid, t, None, 1.0)
                if i == 0:
                    pill(p, "A distancia", 382 - 12, y + 2, BLANCO, hexa("3B82F6"), px=11, anchor="r", emo="📍")
    pestanas(p, "Misiones", t, tab_op)


def videollamada(p, t, quien, t0, plato):
    """La pantalla de la videollamada: la otra persona grande con su plato, uno mismo en la esquina, botones abajo."""
    p.rect(0, 0, TEL_W, TEL_H, hexa("0E0A12"))
    otro, c_otro, c_yo, yo = ("B", BETO_C, ANA_C, "A") if quien == "Ana" else ("A", ANA_C, BETO_C, "B")
    nom = "Beto" if quien == "Ana" else "Ana"
    p.glow(200, 360, 330, c_otro, 0.35, 1.4)
    p.glow(200, 700, 260, sobre(GOLD, BG, 0.6), 0.18, 1.5)          # la luz de la cocina del otro
    bob = 6 * math.sin(t * 2.2 + (0 if quien == "Ana" else 1.5))
    avatar(p, 200, 360 + bob, otro, c_otro, 118, 1.0, None)
    p.emoji(plato, 200, 590, 120)
    p.emoji("🍴", 284 if quien == "Ana" else 118, 540 + 10 * math.sin(t * 4), 44)
    p.texto(nom, 26, 82, 18, BLANCO, "x", 1, "lm")
    p.texto("En videollamada · 20:30", 26, 106, 12, MUT, "s", 1, "lm")
    # uno mismo (esquina)
    p.sombra(276, 70, 384, 220, 16, blur=16, op=0.6, dy=6)
    p.rrect(276, 70, 384, 220, 16, hexa("241C2B"), 1.0, borde=LINE, w=1.5)
    avatar(p, 330, 140, yo, c_yo, 34, 1.0, None)
    pill(p, "Misión: cenar «juntos» · +25 XP", 200, 690, BLANCO, sobre(B, BG, 0.55), px=12, anchor="m", emo="⏳")
    for i, (emo, col) in enumerate((("🎙️", LINE), ("📹", LINE), ("📞", hexa("FF4D5E")))):
        x = 200 + (i - 1) * 86
        p.circ(x, 780, 30, col)
        p.emoji(emo, x, 780, 26)


def pantalla_ana(p, t):
    if t < l_vid - 0.25 or t > T_SALE + 0.1:
        home(p, t, "Ana", t_in=m_cada + 0.2, t_cambio=l_camb, medida={0: m_quien + 0.15, 1: m_quien + 0.35}, xp=165)
        return
    videollamada(p, t, "Ana", l_vid, "🍝")


def pantalla_beto(p, t):
    if t < l_vid - 0.1 or t > T_SALE + 0.1:
        home(p, t, "Beto", t_in=None, t_cambio=l_camb + 0.08, xp=165)
        return
    videollamada(p, t, "Beto", l_vid, "🌮")


def transicion_llamada(p, t, tel, cam, t0):
    """Barrido circular que abre la videollamada (y la cierra en T_SALE) sobre la pantalla del teléfono."""
    u = e_out(pr(t, t0 - 0.25, t0 + 0.1)) * (1 - e_out(pr(t, T_SALE - 0.15, T_SALE + 0.1)))
    if 0.02 < u < 0.98:
        x, y = css(cam, tel, 200, 430)
        p.glow(x, y, 600 * cam.z, BLANCO, 0.25 * math.sin(math.pi * u), 1.5)


# ------------------------------------------------------------------ dibujo
def telefonos(p, t):
    if t < 7.5 or t >= T1:
        return
    cam = camara(t)
    with cam.aplicar(p):
        if l_lej - 0.1 < t < T1:
            telefono(p, tel_beto(t)[0], tel_beto(t)[1], K, t, pantalla_beto)
        telefono(p, tel_ana(t)[0], tel_ana(t)[1], K, t, pantalla_ana)
    transicion_llamada(p, t, tel_ana(t), cam, l_vid)
    if l_lej < t < T1:
        transicion_llamada(p, t, tel_beto(t), cam, l_vid)


RESP = [   # (quién, color, letra, afirmación real del cuestionario inicial, respuesta, misión que recibe)
    ("Ana", ANA_C, "A", "Pasamos suficiente tiempo de calidad juntos, sin pantallas.", "Casi nunca", 0),
    ("Beto", BETO_C, "B", "Nos demostramos cariño físico (abrazos, besos) con frecuencia.", "A veces", 1),
]


def tarjeta_resp(p, x0, y0, quien, col, letra, txt, resp, op, t, t_on):
    """Tarjeta «X contestó»: la afirmación real del cuestionario inicial y su escala de 5 puntos con la respuesta elegida."""
    ancho = 460
    lin = envolver(txt, 26, "s", ancho - 56)
    alto = 96 + len(lin) * 35 + 92
    tarjeta(p, x0, y0, x0 + ancho, y0 + alto, 30, op)
    avatar(p, x0 + 50, y0 + 52, letra, col, 26, op, CARD, 3)
    p.texto(f"{quien} contestó", x0 + 90, y0 + 52, 25, MUT, "b", op, "lm")
    p.parrafo(lin, x0 + 28, y0 + 90, 26, 35, INK, "s", op)
    yb = y0 + 90 + len(lin) * 35 + 44
    opciones = ["Nunca", "Casi nunca", "A veces", "Seguido", "Siempre"]
    k = opciones.index(resp)
    for j in range(5):
        x = x0 + 46 + j * 44
        if j == k and t >= t_on:
            with p.pivote(x, yb, 0.6 + 0.4 * pop(t, t_on, 0.3)):
                p.circ(x, yb, 19, op=op, hg=(x - 19, x + 19))
                palomita(p, x, yb, 17, e_out(pr(t, t_on + 0.05, t_on + 0.3)), op, w=3.5)
        else:
            p.circ(x, yb, 17, LINE, op, w=3)
    p.texto(resp, x0 + 46 + 5 * 44 + 4, yb + 1, 25, INK if t >= t_on else MUT, "x", op, "lm")
    return alto


def frente(p, t):
    if t < T0 - 0.1 or t >= T1 + 0.2:
        return
    cam = camara(t)
    # --- utilería de las misiones (al decir «misiones» / «juntos»)
    if t < m_seg + 0.3:
        x, y = css(cam, tel_ana(t), 0, Y_MIS + 40)
        utileria(p, "📵", 100, y - 40, 130, t, m_mis + 0.1, m_seg + 0.1)
        x, y = css(cam, tel_ana(t), 400, Y_MIS + alto_m("tie1") + 60)
        utileria(p, "🤗", 990, y, 130, t, m_jun - 0.1, m_seg + 0.1, 1.3)
    # --- las respuestas del cuestionario de cada quien
    if m_seg - 0.2 <= t <= l_lej + 0.3:
        for i, (quien, col, letra, txt, resp, idx) in enumerate(RESP):
            ta = m_seg + 0.05 + 0.35 * i
            s = pop(t, ta, 0.4) * (1 - e_in(pr(t, l_lej - 0.15, l_lej + 0.25)))
            if s <= 0.01:
                continue
            x0, y0 = 595, 520 + 470 * i
            with p.pivote(x0 + 230, y0 + 100, s):
                alto = tarjeta_resp(p, x0, y0, quien, col, letra, txt, resp, 1.0, t, m_cont + 0.15 * i)
            # la respuesta vuela a la misión que la toma (en «cada quien»)
            tm = m_quien + 0.15 + 0.2 * i
            yy = Y_MIS + sum(alto_m(m) + 10 for m in NORMAL["Ana"][:idx]) + alto_m(NORMAL["Ana"][idx]) / 2
            xb, yb = css(cam, tel_ana(t), 300, yy)
            v = vuelo(t, tm - 0.45, 0.45, (x0 + 120, y0 + alto - 50), (xb, yb), curva=-120)
            if v:
                p.glow(v[0], v[1], 90, col, 0.8 * (1 - 0.3 * v[2]), 1.6)
                p.circ(v[0], v[1], 16, (1, 0.95, 0.9), 1 - 0.3 * v[2])
            burst(p, xb, yb, t, tm, n=18, fuerza=0.5, semilla=5 + i, dur=1.0, escala=1.0)
    # --- «Estamos a distancia»: tarjeta con el interruptor, pins y el arco entre los dos teléfonos
    if l_lej - 0.3 <= t <= T_SALE + 0.5:
        op = ventana(t, l_lej - 0.3, T_SALE + 0.4, 0.3, 0.4)
        s = 0.6 + 0.4 * pop(t, l_lej - 0.3, 0.4)
        with p.pivote(540, 165, s):
            x0, x1 = 540 - 300, 540 + 300
            tarjeta(p, x0, 110, x1, 220, 34, op)
            p.emoji("📍", x0 + 50, 165, 44, op)
            p.texto("Estamos a distancia", x0 + 90, 165, 34, INK, "x", op, "lm")
            with p.grupo(x1 - 130, 165, 1.9):
                interruptor(p, 0, 0, smooth(pr(t, l_lej, l_lej + 0.3)), op)
        xa, ya = css(cam, tel_ana(t), 200, -40)
        xb, yb = css(cam, tel_beto(t), 200, -40)
        if xb - xa > 60:
            n = 26
            for j in range(n):
                u = (j + (t * 1.5) % 1.0) / n
                bx = lerp(xa, xb, u)
                by = lerp(ya, yb, u) - 150 * math.sin(math.pi * u)
                p.circ(bx, by, 5, mix_ab(u), op * 0.8)
            for x_, y_, c in ((xa, ya, ANA_C), (xb, yb, BETO_C)):
                k = pop(t, l_lej + 0.4, 0.4)
                with p.pivote(x_, y_, k):
                    p.emoji("📍", x_, y_ - 20, 56, op)
            # corazones que viajan por el arco al cenar
            if t >= l_cenar:
                for k in range(5):
                    u = ((t - l_cenar) * 0.55 + k / 5) % 1.0
                    bx = lerp(xa, xb, u)
                    by = lerp(ya, yb, u) - 150 * math.sin(math.pi * u)
                    p.poly(_corazon(bx, by, 18), (A, B, hexa("FF8A5B"))[k % 3], op * math.sin(math.pi * u))
    # --- cenar «juntos»: platos de cada quien y la cámara de la videollamada
    if l_cenar - 0.1 <= t <= T_SALE + 0.4:
        xa, ya = css(cam, tel_ana(t), 200, 900)
        xb, yb = css(cam, tel_beto(t), 200, 900)
        utileria(p, "🍝", xa, ya + 150, 150, t, l_cenar, T_SALE)
        utileria(p, "🌮", xb, yb + 150, 150, t, l_cenar + 0.12, T_SALE, 1.1)
        if t >= l_vid:
            k = pop(t, l_vid, 0.4) * (1 - e_in(pr(t, T_SALE - 0.1, T_SALE + 0.2)))
            with p.pivote(540, ya + 300, k):
                pill(p, "Cenando «juntos» · 20:30", 540, ya + 300, INK, CARD, px=34, anchor="m", emo="🕗")


def mix_ab(u):
    return tuple(a + (b - a) * u for a, b in zip(ANA_C, BETO_C))
