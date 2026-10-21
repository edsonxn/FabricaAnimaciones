# -*- coding: utf-8 -*-
"""Escena «ciclo» (44,5-53 s) y «cierre» (53-60 s).
  ciclo: el teléfono de Ana en «Mi ciclo» (la tarjeta de la fase recorre las fases y «💡 Para ti» cambia sus consejos) ->
         la cámara viaja al de Beto: «Ciclo de Ana» con la «Guía para acompañar» estilo revista -> modo embarazo.
  cierre: los círculos del logo se juntan, los íconos de lo que trae Dúo orbitan, el lema palabra por palabra, el botón
          «Descarga Dúo» y las insignias genéricas de App Store y Google Play (sin URL ni arte oficial).
Textos reales: CONSEJOS-CICLO.md, GUIA-EMBARAZO.md y las capturas de E:/CalendarioPareja/guia (v11-guia, v12-embarazo, v21-consejos)."""
import math

from comun import ANA_C, BETO_C, K, Cam, css, subir, utileria, ventana
from duo import (A, B, BG, BLANCO, CARD, GOLD, INK, LINE, MUT, O, OK, TEL_H, TEL_W, W, H, ancho_texto, avatar, boton, burst,
                 calendario, e_in, e_io, e_out, envolver, fondo_app, golpe, hexa, insignia, kf, lerp, logo, mix, pestanas, pill, pop,
                 pr, rnd, smooth, sobre, tarjeta, telefono, ww, _corazon)

T0 = 44.5
y_llevo, y_ciclo, y_cons, y_cada, y_fase = (ww("ciclo", 0, w) for w in ("llevo", "ciclo", "consejos", "cada", "fase"))
g_mi, g_sale, g_guia, g_acomp = ww("ciclo", 1, "mi"), ww("ciclo", 1, "sale"), ww("ciclo", 1, "guia"), ww("ciclo", 1, "acompa")
g_hasta, g_emb = ww("ciclo", 1, "hasta"), ww("ciclo", 1, "embarazo")
c_duo = ww("cierre", 0, "duo")
LEMA = [(w, ww("cierre", 0, w)) for w in ("misiones", "diarias", "para", "crecer", "en", "pareja")]
d_desc, d_jue, d_hoy = ww("cierre", 1, "descarguenla"), ww("cierre", 1, "jueguen"), ww("cierre", 1, "hoy")
T_CI = 53.0
T_CAE = 52.75                          # los teléfonos se van
ANA2, BETO2 = (540.0, 990.0), (1620.0, 990.0)


def camara(t):
    cx = kf(t, [(T0, 540.0), (g_mi - 0.15, 540.0), (g_mi + 0.45, BETO2[0])])
    z = kf(t, [(T0, 1.0), (g_mi - 0.15, 1.0), (g_mi + 0.15, 0.9), (g_mi + 0.45, 1.0)])
    return Cam(z, cx, 960.0)


def y_tels(t):
    return 990.0 + 1900 * (1 - e_out(pr(t, 44.05, 44.75))) + 2300 * e_in(pr(t, T_CAE, T_CAE + 0.55))


# ------------------------------------------------------------------ Mi ciclo (Ana)
FASES = [   # (emoji, nombre, subtítulo, color, consejos reales «Para ti», fuente)
    ("🌱", "Fase folicular", "Ana · Día 9 del ciclo", OK,
     ("Buen momento para empezar algo nuevo: un hábito, un proyecto o un plan con tu pareja.",
      "Si haces ejercicio, quizá estos días sientas que rindes más: aprovéchalo."), "Fuente: Mayo Clinic"),
    ("✨", "Ventana fértil", "Ana · Día 13 del ciclo", B,
     ("Es normal notar un flujo más transparente y elástico: es señal de que estás ovulando.",
      "El cálculo de la app es una estimación y no sirve como método anticonceptivo."), "Fuentes: NHS"),
    ("🌙", "Fase lútea", "Ana · Día 20 del ciclo", hexa("6F7BD9"),
     ("Si tienes más sueño o más hambre, es normal: la progesterona sube en esta fase.",
      "Dormir bien y moverte un poco te ayudan a sentirte mejor."), "Fuentes: NHS · ACOG"),
    ("🌧️", "Días previos al periodo", "Ana · Día 24 del ciclo · Periodo en 5 días", A,
     ("Dormir bien, moverte un poco y bajarle a la sal, la cafeína y el alcohol ayudan con los síntomas.",
      "Dile a tu pareja qué necesitas con «Hoy necesito»: así no tiene que adivinar."), "Fuente: Office on Women's Health"),
]
T_FASES = [0.0, y_cons + 0.05, y_cada - 0.1, y_fase + 0.05]


def fase_i(t):
    return max(i for i, tf in enumerate(T_FASES) if t >= tf)


def mi_ciclo(p, t):
    fondo_app(p, t)
    i = fase_i(t)
    emo, nom, sub, col, tips, fuente = FASES[i]
    p.texto(sub.split(" · Periodo")[0], 18, 62, 13, MUT, "s", 1, "lm")
    p.texto("Mi ciclo", 18, 92, 26, INK, "x", 1, "lm")
    avatar(p, 400 - 18 - 19 - 28, 80, "A", ANA_C, 19)
    avatar(p, 400 - 18 - 19, 80, "B", BETO_C, 19)
    tc = T_FASES[i]
    s = 1 - 0.06 * golpe(t, tc, 0.3)
    with p.pivote(200, 225, s):
        tarjeta(p, 18, 120, 382, 330, 24)
        p.glow(200, 168, 120, col, 0.25, 1.5)
        with p.pivote(200, 168, 0.5 + 0.5 * pop(t, tc, 0.35) if i > 0 else 1.0):
            p.emoji(emo, 200, 168, 46)
        p.texto(nom, 200, 220, 23 if len(nom) < 18 else 20, INK, "x")
        p.texto(sub, 200, 250, 12.5, MUT, "m")
        # la rueda del ciclo en barra: 4 tramos y el marcador del día
        x0, x1 = 44, 356
        for k, (_, _, _, ck, _, _) in enumerate(FASES):
            a, b = x0 + (x1 - x0) * k / 4 + 2, x0 + (x1 - x0) * (k + 1) / 4 - 2
            p.rrect(a, 286, b, 298, 6, ck, 1.0 if k == i else 0.35)
        mx = lerp(x0 + (x1 - x0) * (T_FASES.index(T_FASES[max(0, i - 1)]) + 0.5) / 4, x0 + (x1 - x0) * (i + 0.5) / 4,
                  e_out(pr(t, tc, tc + 0.3)) if i > 0 else 1)
        p.circ(mx, 292, 10, BLANCO)
        p.circ(mx, 292, 10, col, 1.0, w=3)
    # 💡 Para ti
    op, dy = subir(t, 44.6)
    y0 = 348 + dy
    tarjeta(p, 18, y0, 382, y0 + 300, 22, op)
    p.texto(f"💡 PARA TI · {nom.upper()}".replace("💡 ", ""), 50, y0 + 26, 10.5, A, "x", op, "lm", esp=0.06)
    p.emoji("💡", 36, y0 + 26, 14, op)
    p.texto("IDEAS PARA ESTOS DÍAS", 30, y0 + 52, 10.5, MUT, "x", op, "lm", esp=0.06)
    yy = y0 + 70
    ot = smooth(pr(t, tc + 0.05, tc + 0.25)) if i > 0 else 1.0
    for tip in tips:
        lin = envolver(tip, 13.5, "m", 310)[:3]
        p.poly(_corazon(38, yy + 10, 7), A, op * ot)
        p.parrafo(lin, 54, yy, 13.5, 19, INK, "m", op * ot)
        yy += len(lin) * 19 + 14
    p.texto(fuente, 30, y0 + 282, 10.5, MUT, "s", op * ot, "lm")
    with p.clip(0, 0, TEL_W, TEL_H - 70):
        calendario(p, 18, y0 + 318, t, op, hoy=21, periodo=(), estimado=(26, 27, 28), fertil=range(10, 15), ovu=14)
    pestanas(p, "Ciclo", t)


# ------------------------------------------------------------------ Ciclo de Ana (Beto) y embarazo
def guia(p, t):
    fondo_app(p, t)
    p.texto("Para acompañar a Ana", 18, 62, 13, MUT, "s", 1, "lm")
    p.texto("Ciclo de Ana", 18, 92, 26, INK, "x", 1, "lm")
    avatar(p, 400 - 18 - 19 - 28, 80, "B", BETO_C, 19)
    avatar(p, 400 - 18 - 19, 80, "A", ANA_C, 19)
    sc = -110 * e_io(pr(t, g_guia - 0.2, g_guia + 0.4))
    with p.clip(0, 110, TEL_W, TEL_H):
        with p.grupo(0, sc):
            tarjeta(p, 18, 120, 382, 300, 24)
            p.emoji("🌧️", 200, 160, 40)
            p.texto("Días previos al periodo", 200, 206, 21, INK, "x")
            p.texto("Ana · Día 24 del ciclo · Periodo en 5 días", 200, 232, 12, MUT, "m")
            p.rrect(36, 252, 364, 284, 12, sobre(LINE, CARD, 0.6))
            p.texto("Hoy: Con ganas de cariño · Cansancio · Antojos", 200, 268, 11.5, MUT, "s")
            # la guía estilo revista
            y0 = 318
            alto = 420
            hl = smooth(pr(t, g_guia, g_guia + 0.3))
            tarjeta(p, 18, y0, 382, y0 + alto, 22, 1.0, borde=mix(LINE, GOLD, hl))
            if g_guia <= t <= g_guia + 0.8:
                u = (t - g_guia) / 0.8
                cx = 18 + (-0.5 + 1.7 * u) * 364
                with p.clip(18, y0, 382, y0 + alto):
                    p.poly([(cx - 90, y0 + alto), (cx + 30, y0), (cx + 150, y0), (cx + 30, y0 + alto)], GOLD, 0.16 * math.sin(math.pi * u))
            p.texto("GUÍA PARA ACOMPAÑAR · DÍAS PREVIOS AL PERIODO", 34, y0 + 26, 9.5, A, "x", 1, "lm", esp=0.05)
            for k, ln in enumerate(("Antes del periodo:", "paciencia de campeón")):
                p.texto(ln, 34, y0 + 58 + k * 28, 22, INK, "x", 1, "lm")
            p.texto("QUÉ ESTÁ PASANDO", 34, y0 + 124, 10.5, MUT, "x", 1, "lm", esp=0.06)
            lin = envolver("El estrógeno y la progesterona caen antes del periodo. Esa bajada puede traer irritabilidad, "
                           "tristeza o cansancio.", 13, "m", 324)
            p.parrafo(lin, 34, y0 + 138, 13, 19, INK, "m")
            yj = y0 + 150 + len(lin) * 19 + 14
            p.texto("TU JUGADA DE HOY", 34, yj, 10.5, MUT, "x", 1, "lm", esp=0.06)
            yj += 18
            for n, txt in enumerate(("Puede haber más sensibilidad o cansancio: no te lo tomes personal.", "Escucha más y resuelve menos.")):
                op, dy = subir(t, g_acomp + 0.15 * n)
                p.circ(46, yj + 12 + dy, 12, op=op, hg=(34, 58))
                p.texto(str(n + 1), 46, yj + 12 + dy, 12, BLANCO, "x", op)
                l2 = envolver(txt, 13, "m", 290)
                p.parrafo(l2, 68, yj + 2 + dy, 13, 19, INK, "m", op)
                yj += len(l2) * 19 + 12
    pestanas(p, "Ciclo", t)


def embarazo(p, t):
    fondo_app(p, t)
    p.texto("Para acompañar a Ana", 18, 62, 13, MUT, "s", 1, "lm")
    p.texto("Embarazo de Ana", 18, 92, 26, INK, "x", 1, "lm")
    avatar(p, 400 - 18 - 19 - 28, 80, "B", BETO_C, 19)
    avatar(p, 400 - 18 - 19, 80, "A", ANA_C, 19)
    tarjeta(p, 18, 120, 382, 400, 24)
    with p.pivote(200, 166, 0.5 + 0.5 * pop(t, g_emb - 0.2, 0.4)):
        p.emoji("🤰", 200, 166, 50)
    p.texto("22 semanas", 200, 222, 28, INK, "x")
    p.texto("Ana · 2º trimestre · faltan 18 semanas", 200, 252, 12.5, MUT, "m")
    for k, nom in enumerate(("1er trimestre", "2º trimestre", "3er trimestre")):
        a, b = 40 + k * 108, 40 + (k + 1) * 108 - 6
        if k == 0:
            p.rrect(a, 280, b, 290, 5, op=1.0, hg=(a, b))
        elif k == 1:
            p.rrect(a, 280, b, 290, 5, LINE)
            p.rrect(a, 280, a + (b - a) * 0.6 * e_out(pr(t, g_emb - 0.1, g_emb + 0.5)), 290, 5, op=1.0, hg=(a, b))
        else:
            p.rrect(a, 280, b, 290, 5, LINE)
        p.texto(nom, (a + b) / 2, 306, 10.5, INK if k == 1 else MUT, "b")
    p.rrect(36, 326, 364, 386, 16, sobre(LINE, CARD, 0.6))
    p.emoji("🥥", 64, 356, 28)
    p.parrafo(["Su bebé ya es más o menos", "del tamaño de un coco"], 88, 336, 13.5, 19, INK, "s")
    op, dy = subir(t, g_emb + 0.25)
    y0 = 418 + dy
    tarjeta(p, 18, y0, 382, y0 + 230, 22, op)
    p.texto("GUÍA PARA ACOMPAÑAR · 2º TRIMESTRE", 34, y0 + 26, 9.5, A, "x", op, "lm", esp=0.05)
    p.texto("El trimestre de la energía", 34, y0 + 58, 21, INK, "x", op, "lm")
    p.texto("QUÉ ESTÁ PASANDO", 34, y0 + 92, 10.5, MUT, "x", op, "lm", esp=0.06)
    lin = envolver("Para muchas, las náuseas bajan y vuelve la energía. Entre las semanas 16 y 24 se sienten los primeros "
                   "movimientos del bebé.", 13, "m", 324)
    p.parrafo(lin, 34, y0 + 106, 13, 19, INK, "m", op)
    pestanas(p, "Ciclo", t)


def pantalla_beto(p, t):
    u = e_io(pr(t, g_emb - 0.35, g_emb + 0.05))
    if u < 1:
        with p.grupo(-400 * u, 0):
            guia(p, t)
    if u > 0:
        with p.grupo(400 * (1 - u), 0):
            embarazo(p, t)


# ------------------------------------------------------------------ cierre
ICONOS = ["✅", "🎲", "🏡", "🌻", "📅", "💬"]
LOGO_Y = 700


def cierre(p, t):
    if t < T_CI - 0.3:
        return
    # íconos de lo que trae Dúo, en órbita elíptica (detrás y delante del logo)
    def orbita(delante):
        for i, emo in enumerate(ICONOS):
            t0 = c_duo + 0.15 + 0.1 * i
            if t < t0:
                continue
            a = 2 * math.pi * i / len(ICONOS) + (t - c_duo) * 0.7
            z = math.sin(a)
            if (z > 0) != delante:
                continue
            x, y = 540 + 410 * math.cos(a), LOGO_Y + 170 * z
            s = (0.75 + 0.35 * z) * pop(t, t0, 0.4)
            with p.pivote(x, y, s):
                p.sombra(x - 74, y - 74, x + 74, y + 74, 74, blur=24, op=0.5, dy=10)
                p.circ(x, y, 74, CARD, 0.95)
                p.circ(x, y, 74, LINE, 0.95, w=3)
                p.emoji(emo, x, y, 76)
    orbita(False)
    u = e_io(pr(t, T_CI - 0.25, c_duo + 0.1))
    r = 175
    if u < 1:
        p.circ(lerp(-200, 540 - r * 0.44, u), LOGO_Y, r, ANA_C)
        p.circ(lerp(W + 200, 540 + r * 0.44, u), LOGO_Y, r, BETO_C)
    else:
        p.glow(540, LOGO_Y, 520, (1.0, 0.6, 0.9), 0.32 * math.exp(-(t - c_duo) * 2.0) + 0.08, 1.5)
        with p.pivote(540, LOGO_Y, 1 + 0.08 * golpe(t, c_duo + 0.1, 0.4)):
            logo(p, 540, LOGO_Y, r, t)
    burst(p, 540, LOGO_Y, t, c_duo + 0.08, n=50, fuerza=1.1, semilla=5, escala=1.8)
    orbita(True)
    s = pop(t, c_duo + 0.12, 0.42)
    with p.pivote(540, 1020, s):
        p.texto("Dúo", 540, 1020, 180, INK, "x")
    # lema palabra por palabra
    lineas = [LEMA[:2], LEMA[2:]]
    for k, ln in enumerate(lineas):
        px = 58
        txt = " ".join(w for w, _ in ln)
        palabras = ["Misiones", "diarias"] if k == 0 else ["para", "crecer", "en", "pareja."]
        tot = ancho_texto(" ".join(palabras), px, "m")
        x = 540 - tot / 2
        y = 1160 + k * 76
        for (w, tw), real in zip(ln, palabras):
            op = smooth(pr(t, tw - 0.05, tw + 0.2))
            p.texto(real, x, y + 16 * (1 - op), px, hexa("E6DAEC") if real != "pareja." else INK, "m" if real != "pareja." else "x",
                    op, "lm", hg=(x, x + ancho_texto(real, px, "x")) if real == "pareja." else None)
            x += ancho_texto(real + " ", px, "m")
    # botón y tiendas
    if t >= d_desc - 0.1:
        k = pop(t, d_desc - 0.1, 0.4)
        prs = 1 - 0.07 * golpe(t, d_desc + 0.35, 0.3)
        with p.pivote(540, 1380, k * prs):
            with p.grupo(540 - 300, 1325, 2.0):
                boton(p, "Descarga Dúo", 0, 0, 300, 56, 1.0, 22, emo="💞")
    xs = []
    w_a = insignia_ancho("apple", 118)
    w_g = insignia_ancho("google", 118)
    gap = 30
    xa = 540 - (w_a + w_g + gap) / 2
    for tienda, x0, tt in (("apple", xa, d_jue - 0.1), ("google", xa + w_a + gap, d_hoy - 0.15)):
        if t >= tt:
            k = pop(t, tt, 0.4)
            with p.pivote(x0 + (w_a if tienda == "apple" else w_g) / 2, 1560, k):
                insignia(p, x0, 1501, tienda, 1.0, 118)
    burst(p, 540, 1500, t, d_hoy, n=50, fuerza=1.2, semilla=11, dur=1.8, escala=1.8)
    if t >= d_hoy:
        for i in range(14):
            t0 = d_hoy + 0.06 * i
            if t0 <= t <= t0 + 1.8:
                uu = (t - t0) / 1.8
                x = 540 + (rnd(i, 11) - 0.5) * 900
                y = 1800 - 700 * uu
                p.poly(_corazon(x, y, 18 + 16 * rnd(i, 12)), (A, B, O)[i % 3], math.sin(math.pi * uu) * 0.85)


def insignia_ancho(tienda, alto=100):
    arriba, nombre = ("Descárgala en", "App Store") if tienda == "apple" else ("Disponible en", "Google Play")
    return alto * 0.62 + max(ancho_texto(nombre, alto * 0.36, "x"), ancho_texto(arriba, alto * 0.2, "s")) + alto * 0.42


# ------------------------------------------------------------------ dibujo
def dibujar(p, t):
    if t < 44.0:
        return
    if t < T_CAE + 0.6:
        cam = camara(t)
        y = y_tels(t)
        with cam.aplicar(p):
            telefono(p, ANA2[0], y, K, t, mi_ciclo)
            if t > g_mi - 0.5:
                telefono(p, BETO2[0], y, K, t, pantalla_beto)
        frente(p, t, cam)
    cierre(p, t)


def frente(p, t, cam):
    utileria(p, "💡", 960, 420, 120, t, y_cons, g_mi - 0.1)
    for i in range(1, 4):
        emo = FASES[i][0]
        lado = 110 if i % 2 else 970
        utileria(p, emo, lado, 1250, 130, t, T_FASES[i], (T_FASES[i + 1] if i + 1 < 4 else g_mi - 0.1), i * 1.3)
    utileria(p, "📖", 110, 640, 120, t, g_guia, g_emb - 0.2)
    utileria(p, "💗", 970, 1420, 110, t, g_acomp, g_emb - 0.2, 1.0)
    utileria(p, "🥥", 960, 1180, 140, t, g_emb + 0.1, T_CAE + 0.1)
    utileria(p, "🍼", 120, 1400, 110, t, g_emb + 0.25, T_CAE + 0.1, 1.5)
