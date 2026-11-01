# -*- coding: utf-8 -*-
"""Segunda mitad del anuncio de Dúo (tiempo global):
  ajusta(): cuestionario de la app (escala 1-5 y lenguaje del cariño) -> «Creando sus misiones…» -> misiones a su medida
  cierre(): logo que respira, «Dúo», lema palabra por palabra, botón «Descarga Dúo» + insignias de las tiendas, barrita
  (el usuario, 13-oct: sin el URL provisional; la app saldrá en App Store y Google Play)
"""
import math

from duo import (A, AV_A, AV_L, B, BLANCO, CARD, GOLD, INK, LINE, MUT, TOTAL, ancho_texto, burst, e_in, e_io, e_out,
                 envolver, golpe, hexa, logo, mision, pill, pop, pr, rnd, smooth, sobre, tarjeta, barra_xp, ESC, ww, MISIONES)

MISIONES.update({
    "tie9": ("⏳", "Planeen su próxima cita: lugar, día y hora apartados.", "duo"),
    "afe3": ("💝", "Sorprende a tu pareja con su snack o bebida favorita.", "solo"),
    "div5": ("🎲", "Prueben una comida o un lugar que ninguno de los dos conozca.", "duo"),
})

T_AJ = 35.0
T_CI = ESC["cierre"]["t0"]
j_pre = ww("ajusta", 0, "preguntas")
j_y = ww("ajusta", 0, "y")
j_las, j_mis = ww("ajusta", 0, "las"), ww("ajusta", 0, "misiones")
j_ajus, j_ust = ww("ajusta", 0, "ajustan"), ww("ajusta", 0, "ustedes")
c_duo = ww("cierre", 0, "duo")
c_desc, c_emp, c_hoy = ww("cierre", 1, "descarguenla"), ww("cierre", 1, "empiecen"), ww("cierre", 1, "hoy")
PAL_LEMA = [(w["w"].strip(".,"), w["s"]) for w in ESC["cierre"]["frases"][0]["words"][1:]]

KQ = 2.25
QX0 = 540 - 182 * KQ
SCALE = ["Para nada", "Poco", "Más o menos", "Bastante", "Totalmente"]
OPTS = [("🗣️", "Palabras bonitas"), ("⏳", "Tiempo juntos"), ("🎁", "Detalles y sorpresas"), ("🤗", "Contacto físico"), ("🧺", "Que me ayuden")]
AREAS = ["💬", "⏳", "💝", "🔥", "🎲", "🤝"]
CENTRO = (540.0, 700.0)


def tarjeta_quiz(p, t, n, area, emo_area, pregunta, opciones, sel, t_sel, op=1.0):
    """Una pregunta del cuestionario (`.qtop`, `.qarea`, `.qq`, `.scale`/`.opt`) en px CSS, ancho 364."""
    lineas = envolver(pregunta, 23, "x", 324)
    yb0 = 112 + len(lineas) * 30 + 22
    alto = yb0 + 5 * 58 + 4 * 10 + 20
    tarjeta(p, 0, 0, 364, alto, 22, op)
    p.rrect(20, 20, 58, 58, 12, CARD, op, borde=LINE, w=1.5)
    p.texto("←", 39, 38, 18, INK, "b", op)
    fr = (n - 1 + e_out(pr(t, t_sel + 0.12, t_sel + 0.6))) / 14
    p.rrect(70, 35, 296, 43, 4, LINE, op)
    p.rrect(70, 35, 70 + 226 * fr, 43, 4, op=op, hg=(70, 296))
    p.texto(f"{n + (1 if t >= t_sel + 0.12 else 0)}/14", 344, 39.5, 12, MUT, "b", op, "rm")
    pill(p, area, 20, 84, A, sobre(A, CARD, 0.12), 12, op, emo=emo_area, fnt="b")
    for i, ln in enumerate(lineas):
        p.texto(ln, 20, 112 + i * 30, 23, INK, "x", op, "lt")
    for i, op_ in enumerate(opciones):
        y = yb0 + i * 68
        on = i == sel and t >= t_sel
        s = 1.0 - 0.03 * math.sin(math.pi * pr(t, t_sel - 0.12, t_sel + 0.1)) if i == sel else 1.0
        with p.pivote(182, y + 29, s):
            p.rrect(20, y, 344, y + 58, 16, sobre(A, CARD, 0.08) if on else CARD, op, borde=A if on else LINE, w=1.6)
            if isinstance(op_, tuple):
                ps = 1 + 0.25 * math.sin(math.pi * pr(t, t_sel, t_sel + 0.35)) if on else 1.0
                with p.pivote(48, y + 29, ps):
                    p.emoji(op_[0], 48, y + 29, 22, op)
                p.texto(op_[1], 76, y + 30, 15, INK, "s", op, "lm")
            else:
                cs = 1.12 * (0.7 + 0.3 * pop(t, t_sel, 0.3)) if on else 1.0
                with p.pivote(52, y + 29, cs):
                    if on:
                        p.circ(52, y + 29, 16, op=op, hg=(36, 68))
                    else:
                        p.circ(52, y + 29, 16, LINE, op)
                    p.texto(str(i + 1), 52, y + 29.5, 14, BLANCO if on else INK, "b", op)
                p.texto(op_, 82, y + 30, 15, INK, "s", op, "lm")
        if on and t_sel <= t <= t_sel + 0.6:                 # ripple
            u = (t - t_sel) / 0.6
            with p.clip(20, y, 344, y + 58):
                p.circ(52 + 120 * u, y + 29, 30 + 260 * u, A, 0.22 * (1 - u))
    return alto


def ajusta(p, t):
    if t < T_AJ - 0.5 or t > T_CI + 0.5:
        return
    a_fin = e_in(pr(t, T_CI - 0.25, T_CI + 0.25))           # todo se va hacia el logo
    with p.pivote(CENTRO[0], CENTRO[1], 1 - 0.75 * a_fin):
        oa = 1 - a_fin
        # --- pregunta 1 (escala)
        if t < j_y + 0.5:
            dy = 1100 * (1 - e_out(pr(t, T_AJ - 0.45, T_AJ + 0.15)))
            dx = -760 * e_in(pr(t, j_y, j_y + 0.45))
            op = (1 - smooth(pr(t, j_y + 0.1, j_y + 0.45))) * oa
            with p.grupo(QX0 + dx, 300 + dy, KQ):
                tarjeta_quiz(p, t, 4, "Tiempo de calidad", "⏳", "Pasamos suficiente tiempo de calidad juntos, sin pantallas.",
                             SCALE, 3, j_pre + 0.05, op)
        # --- pregunta 2 (opciones con emoji)
        if j_y <= t < j_mis + 0.5:
            dx = 300 * (1 - e_out(pr(t, j_y + 0.05, j_y + 0.5)))
            u = e_in(pr(t, j_mis - 0.05, j_mis + 0.35))
            op = smooth(pr(t, j_y + 0.05, j_y + 0.4)) * (1 - u) * oa
            with p.pivote(540, CENTRO[1], 1 - 0.8 * u):
                with p.grupo(QX0 + dx, 330, KQ):
                    tarjeta_quiz(p, t, 5, "Sobre ti", "✨", "¿Cómo te gusta más recibir cariño?", OPTS, 2, j_las - 0.08, op)
        # --- «Creando sus misiones…»
        if t >= j_mis - 0.05:
            cx, cy = CENTRO
            s_in = pop(t, j_mis, 0.4)
            beat = 1 + 0.08 * (0.5 - 0.5 * math.cos(2 * math.pi * (t - j_mis)))
            absor = golpe(t, j_ajus + 0.35, 0.5)
            r = 124 * s_in * (beat + 0.25 * absor)
            for k in range(2):                                # anillos que se expanden (`.pulse:before/after`)
                u = ((t - j_mis) / 1.6 + 0.5 * k) % 1.0
                p.circ(cx, cy, r * (1 + u), A, (1 - u) * 0.9 * oa * s_in, w=4)
            p.glow(cx, cy, r * 2.4, A, 0.35 * oa * s_in, 1.6)
            p.circ(cx, cy, r, op=oa, hg=(cx - r, cx + r))
            p.emoji("💞", cx, cy, 95 * s_in * beat, oa)
            # las 6 áreas orbitan y se meten al centro
            for i, e in enumerate(AREAS):
                ang = 2 * math.pi * i / 6 + (t - j_mis) * 1.4
                rad = 330 * e_out(pr(t, j_mis, j_mis + 0.45)) * (1 - e_in(pr(t, j_ajus - 0.05, j_ajus + 0.4)))
                oe = smooth(pr(t, j_mis + 0.05, j_mis + 0.3)) * (1 - smooth(pr(t, j_ajus + 0.25, j_ajus + 0.4))) * oa
                x, y = cx + rad * math.cos(ang), cy + rad * 0.82 * math.sin(ang)
                p.circ(x, y, 58, CARD, oe * 0.95, )
                p.circ(x, y, 58, LINE, oe, w=3)
                p.emoji(e, x, y, 62, oe)
            burst(p, cx, cy, t, j_ajus + 0.35, n=30, fuerza=0.9, semilla=21, escala=1.4)
            ot = smooth(pr(t, j_mis + 0.1, j_mis + 0.4)) * (1 - smooth(pr(t, j_ust - 0.2, j_ust + 0.1))) * oa
            p.texto("Creando sus misiones…", 540, 1080 + 20 * (1 - ot), 58, INK, "x", ot)
            p.texto("Analizando sus respuestas para", 540, 1160, 31, MUT, "m", ot)
            p.texto("personalizar la semana.", 540, 1202, 31, MUT, "m", ot)
            # --- misiones a la medida
            y = 940
            for i, mid in enumerate(("afe3", "tie9", "div5")):
                t0 = j_ust - 0.1 + 0.12 * i
                if t >= t0:
                    u = e_out(pr(t, t0, t0 + 0.45))
                    om = smooth(pr(t, t0, t0 + 0.3)) * oa
                    with p.grupo(QX0, y + 120 * (1 - u), KQ):
                        hgt = mision(p, 0, 0, mid, t, None, om)
                    y += (hgt + 10) * KQ
                else:
                    break


def cierre(p, t):
    if t < T_CI - 0.3:
        return
    cx, cy = 540.0, 700.0
    # --- áreas que orbitan el logo (plano medio)
    oo = smooth(pr(t, c_duo + 0.2, c_duo + 0.8))
    for i, e in enumerate(AREAS):
        ang = 2 * math.pi * i / 6 + t * 0.35
        x, y = cx + 420 * math.cos(ang), cy - 12 + 145 * math.sin(ang)
        prof = 0.5 + 0.5 * math.sin(ang)                      # atrás arriba, adelante abajo
        if prof < 0.5:
            p.emoji(e, x, y, 52 + 26 * prof, oo * (0.35 + 0.5 * prof))
    s = pop(t, c_duo - 0.1, 0.45)
    with p.pivote(cx, cy, s):
        p.glow(cx, cy, 520, (1.0, 0.55, 0.85), 0.22 + 0.25 * golpe(t, c_duo - 0.1, 0.8), 1.6)
        logo(p, cx, cy, 150, t)
    for i, e in enumerate(AREAS):
        ang = 2 * math.pi * i / 6 + t * 0.35
        x, y = cx + 420 * math.cos(ang), cy - 12 + 145 * math.sin(ang)
        prof = 0.5 + 0.5 * math.sin(ang)
        if prof >= 0.5:
            p.emoji(e, x, y, 52 + 26 * prof, oo * (0.35 + 0.5 * prof))
    burst(p, cx, cy, t, c_duo - 0.05, n=40, fuerza=1.0, semilla=31, escala=1.6)
    sw = pop(t, c_duo + 0.05, 0.42)
    with p.pivote(540, 1010, sw):
        p.texto("Dúo", 540, 1010, 190, INK, "x")
    # --- lema palabra por palabra
    px = 44
    frase = " ".join(w for w, _ in PAL_LEMA)
    x = 540 - ancho_texto(frase, px, "m") / 2
    for w, ts in PAL_LEMA:
        u = e_out(pr(t, ts - 0.05, ts + 0.3))
        p.texto(w, x, 1148 + 18 * (1 - u), px, hexa("D9CCE0"), "m", smooth(pr(t, ts - 0.05, ts + 0.2)), "lm")
        x += ancho_texto(w + " ", px, "m")
    # --- botón «Descarga Dúo» (como el «📲 Instalar app» de la app)
    if t >= c_desc - 0.2:
        sb = pop(t, c_desc - 0.15, 0.42) * (1 - 0.035 * math.sin(math.pi * pr(t, c_emp - 0.05, c_emp + 0.2)))
        x0, x1, y0, y1 = 150, 930, 1248, 1360
        with p.pivote(540, (y0 + y1) / 2, sb):
            p.sombra(x0, y0, x1, y1, 34, blur=40, op=0.75, dy=18, color=A)
            p.rrect(x0, y0, x1, y1, 34, hg=(x0, x1, None, (t / 4.0) % 2.0))
            sx = x0 - 100 + ((t % 2.6) / 2.6) * (x1 - x0 + 200)          # brillo que pasa
            with p.clip(x0, y0, x1, y1):
                for k in range(8):
                    p.poly([(sx + k * 12 - 40, y1), (sx + k * 12, y0), (sx + k * 12 + 12, y0), (sx + k * 12 - 28, y1)], BLANCO,
                           0.09 * math.sin(math.pi * (k + 0.5) / 8))
                if c_emp - 0.05 <= t <= c_emp + 0.7:                         # el toque
                    u = (t - c_emp + 0.05) / 0.75
                    p.circ(660, 1304, 40 + 520 * u, BLANCO, 0.28 * (1 - u))
            wt = ancho_texto("Descarga Dúo", 50, "x")
            ic, iy = 540 - wt / 2 - 22, (y0 + y1) / 2
            p.linea((ic, iy - 24), (ic, iy + 10), 7, BLANCO)
            p.polilinea([(ic - 15, iy - 4), (ic, iy + 11), (ic + 15, iy - 4)], 7, BLANCO)
            p.polilinea([(ic - 22, iy + 10), (ic - 22, iy + 24), (ic + 22, iy + 24), (ic + 22, iy + 10)], 6, BLANCO)
            p.texto("Descarga Dúo", 540 + 34, (y0 + y1) / 2 + 2, 50, BLANCO, "x")
        if c_emp - 0.25 <= t <= c_emp + 0.5:                                 # dedo que toca
            u = pr(t, c_emp - 0.25, c_emp + 0.5)
            o = math.sin(math.pi * u)
            p.circ(660, 1304 + 30 * (1 - e_out(pr(t, c_emp - 0.25, c_emp))), 34, BLANCO, 0.55 * o)
            p.circ(660, 1304, 34, BLANCO, 0.9 * o, w=4)
    # --- insignias de las tiendas (genéricas: sin los logos oficiales)
    for j, (tienda, xc) in enumerate((("App Store", 330), ("Google Play", 750))):
        t0 = c_desc + 0.3 + 0.14 * j
        if t < t0:
            continue
        s = pop(t, t0, 0.4)
        bx0, bx1, by0, by1 = xc - 200, xc + 200, 1396, 1500
        with p.pivote(xc, (by0 + by1) / 2, s):
            p.sombra(bx0, by0, bx1, by1, 26, blur=24, op=0.6, dy=10)
            p.rrect(bx0, by0, bx1, by1, 26, hexa("0B080E"), 1.0, borde=(1.0, 1.0, 1.0), w=2, op_b=0.35)
            ic, iy = bx0 + 56, (by0 + by1) / 2
            p.circ(ic, iy, 30, op=1.0, hg=(ic - 30, ic + 30))
            p.linea((ic, iy - 15), (ic, iy + 9), 5, BLANCO)
            p.polilinea([(ic - 11, iy - 1), (ic, iy + 10), (ic + 11, iy - 1)], 5, BLANCO)
            p.linea((ic - 13, iy + 18), (ic + 13, iy + 18), 4, BLANCO)
            p.texto("Descárgala en", bx0 + 104, by0 + 34, 22, (0.82, 0.78, 0.86), "m", 1.0, "lm")
            p.texto(tienda, bx0 + 104, by0 + 70, 36, BLANCO, "x", 1.0, "lm")
    # --- «Llenen juntos su barra cada semana» + la barrita
    if t >= c_hoy - 0.15:
        o = smooth(pr(t, c_hoy - 0.15, c_hoy + 0.2))
        p.texto("Llenen juntos su barra cada semana", 540, 1572 + 16 * (1 - o), 38, hexa("FF8F6E"), "m", o)
        u = e_io(pr(t, c_hoy, c_hoy + 0.95))
        llena = smooth(pr(t, c_hoy + 0.95, c_hoy + 1.15))
        with p.grupo(540 - 330, 1628, 1.0):
            with p.pivote(330, 17, 1 + 0.12 * math.sin(math.pi * pr(t, c_hoy + 0.95, c_hoy + 1.4))):
                barra_xp(p, 0, 0, 660, u, t, o, llena, h=34)
        burst(p, 540 + 330, 1645, t, c_hoy + 0.95, n=22, fuerza=0.45, semilla=41, escala=1.3)
