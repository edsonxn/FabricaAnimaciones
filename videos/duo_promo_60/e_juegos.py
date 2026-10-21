# -*- coding: utf-8 -*-
"""Escena «juegos» (18-35 s), en el teléfono de Ana con la pestaña Juegos de la v24:
  lista de juegos + turnos asíncronos (la ficha «Te toca» brinca entre Ana de día y Beto de noche) ->
  ¿Qué tanto me conoces? (pregunta real de KNOW) -> Dibújalo (un gato que se dibuja trazo a trazo) -> Torre al cielo (grúa) ->
  4 en línea (Ana gana: «Beto te debe: 💆 Un masaje de 10 minutos») -> Asalto al cochinito (resortera, el fuerte vuela).
Textos reales de E:/CalendarioPareja/index.html (KNOW, WORDS, PRIZES y las tarjetas de la pestaña)."""
import math

import e_medida as EM
from comun import ANA_C, BETO_C, K, Cam, css, subir, utileria, velo_bajo, ventana
from duo import (A, B, BG, BLANCO, CARD, FIRE, GOLD, INK, LINE, MUT, O, OK, TEL_H, TEL_W, W, H, ancho_texto, avatar, boton,
                 burst, clamp, e_in, e_io, e_out, envolver, fondo_app, golpe, hexa, kf, lerp, mix, palomita, pestanas, pill,
                 pop, pr, rnd, smooth, sobre, tarjeta, telefono, toast, trazo, vuelo, ww, _corazon)

TEL = (540.0, 990.0)
T0, T1 = 18.0, 35.0
j_hay, j_jue, j_dos, j_tur = ww("juegos", 0, "hay"), ww("juegos", 0, "juegos"), ww("juegos", 0, "dos"), ww("juegos", 0, "turnos")
j_aun, j_con, j_mis, j_tie = ww("juegos", 0, "aunque"), ww("juegos", 0, "conectados"), ww("juegos", 0, "mismo"), ww("juegos", 0, "tiempo")
k_que, k_con, k_dib = ww("juegos", 1, "que"), ww("juegos", 1, "conoces"), ww("juegos", 1, "dibujalo")
k_tor, k_cie = ww("juegos", 1, "torre"), ww("juegos", 1, "cielo")
c_cua, c_lin, c_deb, c_mas = ww("juegos", 2, "cuatro"), ww("juegos", 2, "linea"), ww("juegos", 2, "debes"), ww("juegos", 2, "masaje")
r_rev, r_asa, r_coch = ww("juegos", 3, "revancha"), ww("juegos", 3, "asalto"), ww("juegos", 3, "cochinito")

S_QTMC, S_DIB, S_TOR, S_C4, S_SG = k_que - 0.25, k_dib - 0.3, k_tor - 0.25, c_cua - 0.45, 31.75
T_REV = 31.45                         # Ana toca «Revancha» (durante el suspiro de Beto)
T_IMP = r_coch + 0.08                 # el corazón llega al cochinito
T_SALE = 34.55                        # el teléfono se va (entra el hogar)


def camara(t):
    z = kf(t, [(T0, 1.0), (S_QTMC - 0.1, 1.0), (S_QTMC + 0.4, 1.12), (T_SALE, 1.12), (T1 + 0.2, 0.9)])
    cy = kf(t, [(T0, 960.0), (S_QTMC - 0.1, 960.0), (S_QTMC + 0.4, 900.0), (T_SALE, 900.0)])
    return Cam(z, 540.0, cy)


def y_tel(t):
    return TEL[1] + 2400 * e_in(pr(t, T_SALE, T_SALE + 0.65))


# ------------------------------------------------------------------ piezas de pantalla
def cabecera(p, titulo, op=1.0):
    p.rrect(18, 56, 54, 92, 12, None, op, borde=LINE, w=1.5)
    p.texto("←", 36, 74, 16, INK, "b", op)
    p.texto(titulo, 68, 74, 20, INK, "x", op, "lm")


def casita_iso(p, cx, cy, s, t, op=1.0):
    """Miniatura isométrica de «Nuestro hogar» para la tarjeta destacada."""
    def iso(x, y, z):
        return (cx + (x - y) * s * 0.866, cy + (x + y) * s * 0.5 - z * s)
    pasto, tierra = hexa("7BC86C"), hexa("8B5A2B")
    p.poly([iso(-3, -3, 0), iso(3, -3, 0), iso(3, 3, 0), iso(-3, 3, 0)], pasto, op)
    p.poly([iso(-3, 3, 0), iso(3, 3, 0), iso(3, 3, -0.8), iso(-3, 3, -0.8)], mix(tierra, BG, 0.2), op)
    p.poly([iso(3, -3, 0), iso(3, 3, 0), iso(3, 3, -0.8), iso(3, -3, -0.8)], tierra, op)
    p.poly([iso(-2.5, -2.5, 0.02), iso(1, -2.5, 0.02), iso(1, 1, 0.02), iso(-2.5, 1, 0.02)], hexa("D9A066"), op)
    p.poly([iso(-2.5, -2.5, 0), iso(1, -2.5, 0), iso(1, -2.5, 2), iso(-2.5, -2.5, 2)], hexa("F2E6D8"), op)
    p.poly([iso(-2.5, -2.5, 0), iso(-2.5, 1, 0), iso(-2.5, 1, 2), iso(-2.5, -2.5, 2)], hexa("E3D3C2"), op)
    p.poly([iso(-1.6, -1.2, 0.02), iso(0.2, -1.2, 0.02), iso(0.2, 0.2, 0.02), iso(-1.6, 0.2, 0.02)], A, op * 0.8)
    for x, y, c in ((2, -1.8, hexa("3E9A5B")), (2.2, 1.8, hexa("4CAF64"))):
        bx, by = iso(x, y, 0)
        p.circ(bx, by - s * 1.2, s * 0.9 * (1 + 0.04 * math.sin(t * 2 + x)), c, op)


JUEGOS = [   # (emoji, título, descripción, estado, color del estado) — tarjetas reales de la pestaña
    ("🔮", "¿Qué tanto me conoces?", "Contesta algo sobre ti y adivina lo de tu pareja.", "Te toca adivinar", A),
    ("🎨", "Dibújalo", "Uno dibuja y el otro adivina. Suman como equipo.", "Empezar", None),
    ("🔴", "4 en línea", "El clásico de conectar cuatro… y quien gane cobra un premio.", "Te toca mover", A),
    ("🏗️", "Torre al cielo", "Altura 5.7 m · récord 5.7 m", "Turno de Beto", None),
    ("🐷", "Asalto al cochinito", "Rompe el cochinito de tu pareja con la resortera.", "Retar a Beto", B),
]


def lista(p, t):
    fondo_app(p, t)
    p.texto("Por turnos, cuando cada quien pueda", 18, 62, 13, MUT, "s", 1, "lm")
    p.texto("Juegos", 18, 92, 26, INK, "x", 1, "lm")
    avatar(p, 400 - 18 - 19 - 28, 80, "A", ANA_C, 19)
    avatar(p, 400 - 18 - 19, 80, "B", BETO_C, 19)
    sc = -230 * e_io(pr(t, j_tur, j_tie + 0.3))
    with p.clip(0, 110, TEL_W, TEL_H):
        with p.grupo(0, sc):
            op, dy = subir(t, j_hay + 0.1)
            y0 = 120 + dy
            p.sombra(18, y0, 382, y0 + 180, 22, blur=30, op=0.6 * op, dy=10)
            p.rrect(18, y0, 382, y0 + 180, 22, op=op, hg=(18, 382, ((0, sobre(B, CARD, 0.55)), (1, sobre(A, CARD, 0.45)))))
            with p.clip(18, y0, 382, y0 + 180):
                casita_iso(p, 300, y0 + 92, 15, t, op)
            pill(p, "Nuevo · en 3D", 32, y0 + 26, hexa("1A1320"), GOLD, px=11, emo="✨")
            p.texto("Nuestro hogar", 32, y0 + 118, 20, BLANCO, "x", op, "lm")
            p.texto("4 cuartos · 28 cosas", 32, y0 + 142, 12, hexa("F1E3F4"), "s", op, "lm")
            # la nota de los turnos (se ilumina en «aunque no estemos conectados»)
            yn = y0 + 202
            hl = smooth(pr(t, j_aun, j_aun + 0.3)) * (1 - smooth(pr(t, j_tie + 0.4, j_tie + 0.8)))
            if hl > 0:
                p.rrect(14, yn - 10, 386, yn + 44, 14, sobre(A, BG, 0.25), hl)
            lin = envolver("No necesitan estar conectados al mismo tiempo: cada quien hace su jugada cuando puede.", 12.5, "m", 360)
            p.parrafo(lin, 22, yn - 2, 12.5, 18, mix(MUT, INK, hl), "m", op)
            y = yn + 54
            for i, (emo, tit, des, est, col) in enumerate(JUEGOS):
                op, dy = subir(t, j_jue + 0.08 * i)
                y1 = y + dy
                lin = envolver(des, 12, "m", 250)[:2]
                alto = 64 + len(lin) * 16 + 10
                tarjeta(p, 18, y1, 382, y1 + alto, 20, op)
                p.rrect(32, y1 + 18, 78, y1 + 64, 14, sobre(B, CARD, 0.12), op)
                p.emoji(emo, 55, y1 + 41, 24, op)
                p.texto(tit, 92, y1 + 28, 16, INK, "x", op, "lm")
                p.parrafo(lin, 92, y1 + 40, 12, 16, MUT, "m", op)
                if col is not None:
                    pill(p, est, 92, y1 + alto - 18, BLANCO, col, px=10.5)
                else:
                    pill(p, est, 92, y1 + alto - 18, MUT, LINE, px=10.5)
                p.texto("→", 360, y1 + 30, 18, A, "b", op)
                y += alto + 12
    pestanas(p, "Juegos", t, t_cambio=j_hay, de="Misiones")


def qtmc(p, t):
    fondo_app(p, t)
    cabecera(p, "¿Qué tanto me conoces?")
    p.texto("Adivina cómo completó Beto la frase", 18, 122, 13, MUT, "m", 1, "lm")
    tarjeta(p, 18, 142, 382, 640, 24)
    avatar(p, 46, 176, "B", BETO_C, 14, 1.0, CARD, 2)
    p.texto("Beto completó:", 68, 176, 13, MUT, "b", 1, "lm")
    p.texto("Mi domingo ideal es…", 36, 218, 24, INK, "x", 1, "lm")
    ops = ["Quedarme en pijama todo el día", "Salir a pasear o de excursión", "Ver a la familia o a amigos", "Ponerme al día con pendientes"]
    t_ok = k_con + 0.45
    for i, o in enumerate(ops):
        op, dy = subir(t, S_QTMC + 0.15 + 0.07 * i)
        y = 262 + i * 74 + dy
        if i == 0 and t >= t_ok:
            s = 0.96 + 0.04 * pop(t, t_ok, 0.3)
            with p.pivote(200, y + 30, s):
                p.sombra(36, y, 364, y + 60, 16, blur=20, op=0.6 * op, dy=8, color=A)
                p.rrect(36, y, 364, y + 60, 16, op=op, hg=(36, 364))
                p.texto(o, 56, y + 30, 15, BLANCO, "b", op, "lm")
                p.circ(338, y + 30, 13, BLANCO, op)
                palomita(p, 338, y + 30, 12, e_out(pr(t, t_ok + 0.05, t_ok + 0.3)), op, 2.6, A)
        else:
            p.rrect(36, y, 364, y + 60, 16, sobre(LINE, CARD, 0.5), op, borde=LINE, w=1.5)
            p.texto(o, 56, y + 30, 15, INK if t < t_ok else MUT, "s", op, "lm")
    if t >= t_ok + 0.25:
        k = pop(t, t_ok + 0.25, 0.35)
        with p.pivote(200, 580, 0.5 + 0.5 * k):
            pill(p, "¡Acertaste! · +1", 200, 580, BLANCO, OK, px=16, anchor="m", emo="🎯")
    p.texto(f"Aciertos: tú {3 if t >= t_ok + 0.25 else 2} · Beto 1", 200, 680, 14, INK, "b", 1)
    pestanas(p, "Juegos", t)


GATO = [   # trazos del gato en una hoja de 0..1 (cabeza, orejas, ojos, bigotes, boca, cuerpo y cola)
    [(0.5 + 0.2 * math.cos(a), 0.36 + 0.18 * math.sin(a)) for a in [2 * math.pi * k / 30 for k in range(31)]],
    [(0.34, 0.26), (0.33, 0.1), (0.44, 0.2)],
    [(0.56, 0.2), (0.67, 0.1), (0.66, 0.26)],
    [(0.43, 0.33), (0.43, 0.36)],
    [(0.57, 0.33), (0.57, 0.36)],
    [(0.46, 0.44), (0.5, 0.47), (0.54, 0.44)],
    [(0.36, 0.41), (0.2, 0.38)], [(0.36, 0.45), (0.2, 0.47)], [(0.64, 0.41), (0.8, 0.38)], [(0.64, 0.45), (0.8, 0.47)],
    [(0.4, 0.53), (0.33, 0.7), (0.34, 0.86), (0.66, 0.86), (0.67, 0.7), (0.6, 0.53)],
    [(0.66, 0.82), (0.8, 0.8), (0.86, 0.66), (0.8, 0.56)],
]


def dibujalo(p, t):
    fondo_app(p, t)
    cabecera(p, "Dibújalo")
    p.texto("Beto dibujó · ¿qué es?", 18, 122, 13, MUT, "m", 1, "lm")
    x0, y0, x1, y1 = 18, 142, 382, 506
    p.sombra(x0, y0, x1, y1, 22, blur=26, op=0.55, dy=10)
    p.rrect(x0, y0, x1, y1, 22, hexa("FBF5F8"))
    u_tot = pr(t, S_DIB + 0.2, k_tor - 0.55)                          # repetición trazo a trazo
    largos = [sum(math.dist(a, b) for a, b in zip(s, s[1:])) for s in GATO]
    total = sum(largos)
    hecho = u_tot * total
    lado = x1 - x0 - 40
    for s, l in zip(GATO, largos):
        if hecho <= 0:
            break
        u = min(1.0, hecho / l)
        pts = [(x0 + 20 + a * lado, y0 + 6 + b * lado) for a, b in trazo(s, u)]
        p.polilinea(pts, 6, hexa("FF5E7E"))
        hecho -= l
    if 0 < u_tot < 1:                                                 # la punta del lápiz
        s_i, h = 0, u_tot * total
        for i, l in enumerate(largos):
            if h <= l:
                s_i = i
                break
            h -= l
        pt = trazo(GATO[s_i], h / largos[s_i])[-1]
        p.emoji("✏️", x0 + 20 + pt[0] * lado + 16, y0 + 6 + pt[1] * lado - 16, 30)
    for i, c in enumerate(("2A1F2D", "FF5E7E", "FF8A5B", "FFB648", "22C58B", "3B82F6", "8B5CF6", "8B5A2B")):
        x = 46 + i * 44
        p.circ(x, 534, 14, hexa(c))
        if i == 1:
            p.circ(x, 534, 18, INK, w=2)
    # la respuesta que escribe Ana
    p.rrect(18, 566, 382, 616, 16, CARD, 1.0, borde=A if t > k_dib else LINE, w=1.5)
    n = int(clamp(pr(t, k_dib + 0.2, k_dib + 0.6)) * 4)
    p.texto("gato"[:n] + ("|" if (t * 3) % 1 < 0.5 and n < 4 else ""), 36, 591, 18, INK, "b", 1, "lm")
    if t >= k_dib + 0.65:
        k = pop(t, k_dib + 0.65, 0.3)
        with p.pivote(200, 660, 0.5 + 0.5 * k):
            pill(p, "¡Adivinaste! · +1 punto de equipo", 200, 660, BLANCO, OK, px=14, anchor="m", emo="🎉")
    pestanas(p, "Juegos", t)


COLS_T = (O, A, B, GOLD, OK, hexa("3B82F6"))


def cielo(p, x0, y0, x1, y1, t, sol=True):
    """Cielo de los juegos de física (Torre y Asalto): degradado vertical en franjas, sol, nubes que pasan y montañas."""
    n = 24
    for i in range(n):
        u = i / (n - 1)
        p.rect(x0, y0 + (y1 - y0) * i / n, x1, y0 + (y1 - y0) * (i + 1) / n + 1, mix(hexa("7EC8F2"), hexa("D8F0FF"), u))
    if sol:
        p.glow(x1 - 60, y0 + 60, 90, hexa("FFE7A0"), 0.6, 1.4)
        p.circ(x1 - 60, y0 + 60, 26, hexa("FFE07A"))
    for k in range(3):
        cx = x0 + ((t * (14 + 6 * k) + k * 150) % (x1 - x0 + 160)) - 80
        cy = y0 + 70 + 60 * k
        for dx, r in ((-26, 18), (0, 26), (26, 20)):
            p.circ(cx + dx, cy, r, BLANCO, 0.9)
    p.poly([(x0, y1 - 70), (x0 + 90, y1 - 150), (x0 + 170, y1 - 80), (x0 + 250, y1 - 160), (x1, y1 - 90), (x1, y1), (x0, y1)],
           hexa("9CB8D6"))


def torre(p, t):
    fondo_app(p, t)
    cabecera(p, "Torre al cielo")
    alt = "6.3 m · ¡récord!" if t >= k_cie + 0.45 else "5.7 m · récord 5.7 m"
    p.texto(f"Altura {alt}", 18, 122, 13, GOLD if t >= k_cie + 0.45 else MUT, "b", 1, "lm")
    x0, y0, x1, y1 = 18, 140, 382, 720
    p.sombra(x0, y0, x1, y1, 22, blur=26, op=0.55, dy=10)
    with p.clip(x0, y0, x1, y1):
        cielo(p, x0, y0, x1, y1, t)
        p.rect(x0, y1 - 46, x1, y1, hexa("6DBE5A"))
        p.rect(x0, y1 - 46, x1, y1 - 40, hexa("8AD474"))
        yb = y1 - 46
        for i in range(8):                                            # la torre que ya construyeron
            off = 10 * math.sin(i * 1.7)
            bw, bh = 86, 34
            p.rrect(200 - bw / 2 + off, yb - bh * (i + 1), 200 + bw / 2 + off, yb - bh * i, 6, COLS_T[i % 6])
            p.rect(200 - bw / 2 + off + 6, yb - bh * (i + 1) + 4, 200 + bw / 2 + off - 6, yb - bh * (i + 1) + 8, BLANCO, 0.3)
        top = yb - 34 * 8
        # grúa: riel arriba, carrito que va y viene, cable y bloque
        p.rect(x0, y0 + 40, x1, y0 + 48, hexa("4A4458"))
        suelta = k_cie
        xc = 200 + 110 * math.sin((t - S_TOR) * 3.2) if t < suelta else 200 + 110 * math.sin((suelta - S_TOR) * 3.2)
        p.rrect(xc - 18, y0 + 34, xc + 18, y0 + 56, 5, GOLD)
        if t < suelta:
            yblk = y0 + 150
            p.linea((xc, y0 + 56), (xc, yblk - 17), 2.5, hexa("4A4458"))
            xb = xc
        else:
            # cae con gravedad y se acomoda arriba de la torre (con rebote)
            xb = 200 + 110 * math.sin((suelta - S_TOR) * 3.2)
            xb = lerp(xb, 200 + 6, e_out(pr(t, suelta, suelta + 0.35)))
            tc = t - suelta
            yblk = min(y0 + 150 + 0.5 * 2600 * tc * tc, top - 17)
            p.linea((xc, y0 + 56), (xc, y0 + 120), 2.5, hexa("4A4458"))
        land = suelta + math.sqrt(2 * max(1, top - 17 - (y0 + 150)) / 2600)
        sq = 1 + 0.12 * golpe(t, land, 0.3)
        with p.pivote(xb, yblk + 17, sq):
            p.rrect(xb - 43, yblk - 17, xb + 43, yblk + 17, 6, A)
            p.rect(xb - 37, yblk - 13, xb + 37, yblk - 9, BLANCO, 0.3)
        if t >= land:
            burst(p, xb, top, t, land, n=14, fuerza=0.35, semilla=21, dur=0.8, escala=0.5)
    pestanas(p, "Juegos", t)


C4 = {(0, 0): "A", (1, 0): "A", (2, 0): "A", (4, 0): "B", (5, 0): "B", (0, 1): "B", (1, 1): "B", (2, 1): "A", (4, 1): "A",
      (1, 2): "B", (2, 2): "B", (2, 3): "A"}
C4_B = (5, 1, S_C4 + 0.15)            # la jugada que hizo Beto (cuando pudo)
C4_A = (3, 0, c_cua)                  # la de Ana: cuatro en línea abajo


def cuatro(p, t):
    fondo_app(p, t)
    cabecera(p, "4 en línea")
    p.texto("En juego:", 18, 122, 13, MUT, "m", 1, "lm")
    p.emoji("💆", 90, 122, 15)
    p.texto("Un masaje de 10 minutos", 104, 122, 13, INK, "b", 1, "lm")
    x0, y0, cw = 32, 160, 48
    bx0, by0, bx1, by1 = 22, 150, 378, 150 + 6 * cw + 20
    p.sombra(bx0, by0, bx1, by1, 22, blur=26, op=0.55, dy=10)
    p.rrect(bx0, by0, bx1, by1, 22, hexa("2E2346"), 1.0, borde=hexa("4A3C6A"), w=2)

    def centro(c, r):
        return x0 + 10 + c * cw + cw / 2 - 4, by1 - 10 - r * cw - cw / 2

    piezas = dict(C4)
    gana = t >= C4_A[2] + 0.25
    for (c, r, tt), q in ((C4_B, "B"), (C4_A, "A")):
        if t >= tt:
            piezas[(c, r)] = (q, tt)
    for c in range(7):
        for r in range(6):
            x, y = centro(c, r)
            p.circ(x, y, 19, hexa("17121C"))
    for (c, r), v in piezas.items():
        q, tt = (v, None) if isinstance(v, str) else v
        x, y = centro(c, r)
        if tt is not None:                                            # cae desde arriba
            tc = t - tt
            y = min(y, by0 - 20 + 0.5 * 3800 * tc * tc)
        col = ANA_C if q == "A" else BETO_C
        p.circ(x, y, 18, col)
        p.circ(x - 5, y - 6, 6, BLANCO, 0.25)
    if gana:                                                          # la línea ganadora en dorado
        u = e_out(pr(t, C4_A[2] + 0.25, c_lin + 0.3))
        xa, ya = centro(0, 0)
        xb, yb = centro(3, 0)
        for c in range(4):
            x, y = centro(c, 0)
            p.glow(x, y, 40, GOLD, 0.7 * u, 1.6)
            p.circ(x, y, 21, GOLD, u, w=3)
        p.polilinea([(xa, ya), (lerp(xa, xb, u), ya)], 8, GOLD, 0.9)
        burst(p, (xa + xb) / 2, ya, t, c_lin, n=26, fuerza=0.6, semilla=31, dur=1.3, escala=0.8)
    yt = by1 + 34
    if t >= c_lin:
        k = pop(t, c_lin, 0.35)
        with p.pivote(200, yt, 0.5 + 0.5 * k):
            p.emoji("🏆", 112, yt, 26)
            p.texto("¡Ganaste!", 132, yt + 1, 24, GOLD, "x", 1, "lm")
    else:
        p.texto("Te toca mover", 200, yt, 18, MUT, "b", 1)
    if t >= c_deb - 0.05:
        op, dy = subir(t, c_deb - 0.05)
        y = yt + 34 + dy
        tarjeta(p, 18, y, 382, y + 160, 22, op)
        p.texto("Beto te debe:", 200, y + 34, 15, MUT, "b", op)
        p.emoji("💆", 200, y + 74, 34, op)
        p.texto("Un masaje de 10 minutos", 200, y + 112, 17, INK, "x", op)
        y2 = y + 176
        boton(p, "Ya se cobró", 18, y2, 196, 46, op, 14)
        rev = t >= T_REV
        p.rrect(204, y2, 382, y2 + 46, 16, sobre(B, CARD, 0.3) if not rev else None, op, borde=B, w=2)
        if rev:
            with p.pivote(293, y2 + 23, 1 - 0.08 * golpe(t, T_REV, 0.25)):
                p.rrect(204, y2, 382, y2 + 46, 16, B, op)
        p.texto("Revancha", 293, y2 + 23.5, 14, BLANCO, "b", op)
    pestanas(p, "Juegos", t)


FUERTE = [   # piezas del fuerte de Beto: (x, y desde el suelo, ancho, alto, material)
    (236, 0, 14, 70, "madera"), (330, 0, 14, 70, "madera"), (226, 70, 128, 14, "madera"), (250, 84, 14, 50, "vidrio"),
    (316, 84, 14, 50, "vidrio"), (242, 134, 96, 14, "piedra"), (262, 0, 56, 26, "piedra"), (226, 148, 128, 0, "techo"),
]
MAT = {"madera": hexa("B07A4A"), "vidrio": hexa("BDE7F5"), "piedra": hexa("8E8A99")}


def asalto(p, t):
    fondo_app(p, t)
    cabecera(p, "Asalto al cochinito")
    p.texto("Te toca disparar", 200, 124, 22, INK, "x", 1)
    p.texto("En juego: 🍳 Desayuno en la cama".replace("🍳 ", ""), 200, 152, 13, MUT, "m", 1)
    x0, y0, x1, y1 = 18, 172, 382, 600
    p.sombra(x0, y0, x1, y1, 22, blur=26, op=0.55, dy=10)
    suelo = y1 - 40
    with p.clip(x0, y0, x1, y1):
        cielo(p, x0, y0, x1, y1, t)
        p.rect(x0, suelo, x1, y1, hexa("6DBE5A"))
        p.rect(x0, suelo, x1, suelo + 6, hexa("8AD474"))
        # el fuerte: antes del impacto quieto; después, cada pieza sale volando con giro
        ti = t - T_IMP
        for i, (bx, by, bw, bh, m) in enumerate(FUERTE):
            cx, cy = bx + bw / 2, suelo - by - bh / 2
            ang = 0.0
            if ti > 0:
                vx = (120 + 260 * rnd(i, 51)) * (1 if cx > 270 else 0.6)
                vy = -(260 + 380 * rnd(i, 52))
                cx += vx * ti
                cy += vy * ti + 0.5 * 1500 * ti * ti
                ang = (rnd(i, 53) - 0.5) * 9 * ti
            if m == "techo":
                h = 46
                pts = [(cx - 70, cy + h / 2), (cx + 70, cy + h / 2), (cx, cy - h / 2)]
                pts = [rot(q, (cx, cy), ang) for q in pts]
                p.poly(pts, hexa("C2603E"))
                continue
            pts = [rot(q, (cx, cy), ang) for q in ((cx - bw / 2, cy - bh / 2), (cx + bw / 2, cy - bh / 2), (cx + bw / 2, cy + bh / 2),
                                                   (cx - bw / 2, cy + bh / 2))]
            p.poly(pts, MAT[m], 0.8 if m == "vidrio" else 1.0)
            p.polilinea(pts, 1.5, mix(MAT[m], BG, 0.4), 1.0, cerrado=True)
        if ti < 0:
            p.emoji("🐷", 290, suelo - 48, 46)
        else:
            burst(p, 290, suelo - 50, t, T_IMP, n=30, fuerza=0.7, semilla=41, dur=1.4, escala=0.8)
            for k in range(10):                                       # monedas del cochinito
                v = (rnd(k, 61) - 0.5) * 500, -(300 + 400 * rnd(k, 62))
                if ti < 1.6:
                    p.circ(290 + v[0] * ti, suelo - 50 + v[1] * ti + 750 * ti * ti, 9, GOLD)
                    p.circ(290 + v[0] * ti, suelo - 50 + v[1] * ti + 750 * ti * ti, 9, hexa("C9821A"), w=2)
        # resortera y el corazón que se lanza
        sx, sy = 82, suelo - 70
        p.polilinea([(sx, suelo), (sx, sy + 20), (sx - 20, sy - 10)], 9, hexa("7A4B2A"))
        p.polilinea([(sx, sy + 20), (sx + 20, sy - 10)], 9, hexa("7A4B2A"))
        jala = e_out(pr(t, r_rev, r_rev + 0.4)) * (1 - smooth(pr(t, r_asa, r_asa + 0.06)))
        if t < r_asa:
            hx, hy = sx - 44 * jala, sy + 8 * jala
            p.polilinea([(sx - 20, sy - 10), (hx, hy), (sx + 20, sy - 10)], 3, hexa("4A2A18"))
            p.poly(_corazon(hx, hy, 15), hg=(hx - 15, hx + 15))
        else:
            p.linea((sx - 20, sy - 10), (sx + 20, sy - 10), 3, hexa("4A2A18"))
            v = vuelo(t, r_asa, T_IMP - r_asa, (sx - 44, sy + 8), (290, suelo - 48), curva=-170)
            if v:
                for j in range(5):                                    # estela
                    vj = vuelo(t - 0.03 * (j + 1), r_asa, T_IMP - r_asa, (sx - 44, sy + 8), (290, suelo - 48), curva=-170)
                    if vj:
                        p.circ(vj[0], vj[1], 8 - j, A, 0.35 - 0.06 * j)
                p.poly(_corazon(v[0], v[1], 15), hg=(v[0] - 15, v[0] + 15))
    for i, (emo, nom) in enumerate((("❤️", "Corazón"), ("⚫", "Hierro"), ("💣", "Bomba"), ("✨", "Triple"))):
        x = 60 + i * 93
        on = i == 0
        p.rrect(x - 40, 616, x + 40, 690, 16, CARD, 1.0, borde=A if on else LINE, w=2 if on else 1.5)
        p.emoji(emo, x, 642, 22)
        p.texto(nom, x, 674, 11, INK if on else MUT, "b", 1)
    if t >= T_IMP + 0.3:
        k = pop(t, T_IMP + 0.3, 0.35)
        with p.pivote(200, 730, 0.5 + 0.5 * k):
            pill(p, "¡Rompiste su cochinito!", 200, 730, hexa("1A1320"), GOLD, px=16, anchor="m", emo="🏆")
    pestanas(p, "Juegos", t)


def rot(q, c, a):
    if a == 0:
        return q
    ca, sa = math.cos(a), math.sin(a)
    dx, dy = q[0] - c[0], q[1] - c[1]
    return (c[0] + ca * dx - sa * dy, c[1] + sa * dx + ca * dy)


PANTALLAS = [(T0 - 1, None), (j_hay, lista), (S_QTMC, qtmc), (S_DIB, dibujalo), (S_TOR, torre), (S_C4, cuatro), (S_SG, asalto)]
DUR_SW = 0.32


def home_final(p, t):
    EM.home(p, t, "Ana", t_in=None, t_cambio=EM.l_camb, xp=165)


def pantalla(p, t):
    i = max(k for k, (ts, _) in enumerate(PANTALLAS) if t >= ts)
    ts, f = PANTALLAS[i]
    f = f or home_final
    u = e_io(pr(t, ts, ts + DUR_SW))
    if i > 0 and u < 1:
        fa = PANTALLAS[i - 1][1] or home_final
        with p.grupo(-400 * u, 0):
            fa(p, t)
        with p.grupo(400 * (1 - u), 0):
            f(p, t)
    else:
        f(p, t)


# ------------------------------------------------------------------ dibujo
def dibujar(p, t):
    if t < T0 or t > T1 + 0.5:
        return
    cam = camara(t)
    with cam.aplicar(p):
        telefono(p, TEL[0], y_tel(t), K, t, pantalla)
    frente(p, t, cam)


def wifi_tachado(p, x, y, s, op):
    for k, r in enumerate((14, 28, 42)):
        p.elip(x, y + 18 * s, r * s, r * s, MUT, op, a0=225, a1=315, w=6 * s)
    p.circ(x, y + 18 * s, 5 * s, MUT, op)
    p.linea((x - 34 * s, y - 26 * s), (x + 34 * s, y + 30 * s), 7 * s, hexa("FF4D5E"), op)


def frente(p, t, cam):
    # --- los turnos: Ana (de día) y Beto (de noche); la ficha «Te toca» brinca de uno al otro
    if j_tur - 0.3 <= t <= S_QTMC + 0.3:
        ob = ventana(t, j_tur - 0.3, S_QTMC + 0.3, 0.3, 0.35)
        velo_bajo(p, 1240, 220, 0.8 * ob)
        y = 1610
        for j, (x, letra, col, emo, hora) in enumerate(((240, "A", ANA_C, "☀️", "9:41"), (840, "B", BETO_C, "🌙", "23:10"))):
            s = pop(t, j_tur - 0.25 + 0.1 * j, 0.4) * (1 - e_in(pr(t, S_QTMC, S_QTMC + 0.3)))
            with p.pivote(x, y, s):
                p.glow(x, y, 220, col, 0.22, 1.6)
                avatar(p, x, y, letra, col, 86, 1.0, BG, 6)
                with p.pivote(x + 70, y - 70, 1 + 0.12 * math.sin(t * 5 + j)):
                    p.emoji(emo, x + 70, y - 70, 64)
                pill(p, hora, x, y + 128, INK, CARD, px=30, anchor="m")
        # la ficha
        saltos = [j_tur, j_tur + 0.55, j_aun + 0.1, j_con, j_tie]
        lado = sum(1 for s_ in saltos if t >= s_) % 2                 # 0 = Ana, 1 = Beto
        ts = max([s_ for s_ in saltos if t >= s_] + [j_tur - 1])
        u = e_io(pr(t, ts, ts + 0.42))
        xa, xb = 240, 840
        de, a = (xb, xa) if lado == 0 else (xa, xb)
        x = lerp(de, a, u) if t >= j_tur else xa
        yy = y - 170 - 120 * math.sin(math.pi * u)
        k = pop(t, j_tur - 0.2, 0.35) * (1 - e_in(pr(t, S_QTMC, S_QTMC + 0.3)))
        with p.pivote(x, yy, k):
            w = ancho_texto("Te toca", 34, "x") + 50
            p.sombra(x - w / 2, yy - 32, x + w / 2, yy + 32, 32, blur=20, op=0.6, dy=8, color=A)
            p.rrect(x - w / 2, yy - 32, x + w / 2, yy + 32, 32, op=1.0, hg=(x - w / 2, x + w / 2))
            p.texto("Te toca", x, yy + 1, 34, BLANCO, "x")
        if t >= j_con - 0.1:
            wifi_tachado(p, 540, y - 20, 1.6, smooth(pr(t, j_con - 0.1, j_con + 0.2)) * (1 - smooth(pr(t, S_QTMC, S_QTMC + 0.3))))
    # --- utilería de cada juego (bordes del teléfono)
    utileria(p, "🎮", 120, 1500, 120, t, j_jue, j_tur - 0.2)
    utileria(p, "🎲", 960, 1400, 110, t, j_jue + 0.15, j_tur - 0.2, 1.0)
    utileria(p, "🤔", 110, 520, 120, t, S_QTMC + 0.2, k_con + 0.45)
    utileria(p, "🎯", 110, 520, 130, t, k_con + 0.45, S_DIB + 0.1)
    utileria(p, "🎨", 990, 560, 120, t, S_DIB + 0.25, S_TOR + 0.1, 1.0)
    utileria(p, "☁️", 120, 600, 130, t, S_TOR + 0.2, S_C4 + 0.1, 2.0)
    # 4 en línea: el masaje
    if c_deb - 0.1 <= t <= T_REV + 0.4:
        k = e_out(pr(t, c_deb - 0.1, c_deb + 0.25)) * (1 - e_in(pr(t, T_REV, T_REV + 0.3)))
        with p.pivote(540, 230, 0.7 + 0.3 * k):
            toast(p, "Beto te debe un masaje", 540, 180, k, 40, "💆")
    utileria(p, "💆", 930, 1500, 190, t, c_mas, T_REV + 0.1)
    if c_mas <= t <= T_REV + 0.4:
        for i in range(10):
            t0 = c_mas + 0.08 * i
            if t0 <= t <= t0 + 1.4:
                u = (t - t0) / 1.4
                x = 930 + (rnd(i, 71) - 0.5) * 300
                y = 1400 - 420 * u
                p.poly(_corazon(x, y, 16 + 14 * rnd(i, 72)), (A, B, O)[i % 3], math.sin(math.pi * u) * 0.9)
    # Asalto: el cochinito sale volando hacia la cámara
    if T_IMP <= t <= T_SALE + 0.6:
        u = pr(t, T_IMP, T_IMP + 0.9)
        x = lerp(*css(cam, (TEL[0], y_tel(t)), 290, 520)[:1], 820, e_out(u)) if False else lerp(css(cam, (TEL[0], y_tel(t)), 290, 520)[0], 820, e_out(u))
        y = lerp(css(cam, (TEL[0], y_tel(t)), 290, 520)[1], 560, e_out(u)) - 200 * math.sin(math.pi * min(1, u))
        s = lerp(0.3, 1.0, e_out(u)) * (1 - e_in(pr(t, T_SALE + 0.1, T_SALE + 0.5)))
        with p.pivote(x, y, s):
            p.emoji("🐷", x, y + 10 * math.sin(t * 9), 230)
        burst(p, 540, 900, t, T_IMP, n=40, fuerza=1.0, semilla=81, dur=1.6, escala=1.6)
        for k in range(16):                                           # lluvia de monedas que suben (se las lleva el hogar)
            t0 = T_IMP + 0.1 + 0.04 * k
            if t0 <= t:
                tau = t - t0
                xk = 540 + (rnd(k, 91) - 0.5) * 700
                yk = 1000 - 900 * e_out(pr(t, t0, t0 + 1.2)) + 40 * math.sin(tau * 5 + k)
                if tau < 1.6:
                    moneda(p, xk, yk, 30, math.sin(tau * 8 + k), 1 - e_in(pr(t, t0 + 1.1, t0 + 1.6)))


def moneda(p, x, y, r, giro=1.0, op=1.0):
    """Moneda dorada (la 🪙 de la app), con giro en x."""
    rx = r * max(0.15, abs(giro))
    p.elip(x, y + 3, rx, r, hexa("A86A12"), op)
    p.elip(x, y, rx, r, GOLD, op)
    p.elip(x, y, rx * 0.68, r * 0.68, hexa("FFD36B"), op, w=max(1, r * 0.1))
    p.elip(x - rx * 0.3, y - r * 0.3, rx * 0.2, r * 0.25, BLANCO, op * 0.5)
