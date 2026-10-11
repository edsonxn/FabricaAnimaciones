# -*- coding: utf-8 -*-
"""Escenas de "Neandertales: 7 mitos que la ciencia ya derrumbó" — estilo doodle (sin psicodelia).
Cada mito: título -> fase A (sello FALSO + la evidencia) -> fase B (el paralelo con hoy).
Toda aparición está anclada a la palabra que la nombra (self.w)."""
from escena_base import *  # noqa: F401,F403

ROJO_SELLO = (205, 40, 40)


def icono_mito(lz, i, x, y, s, t):
    """El ícono del mito i (0..6), compacto para ir en fila."""
    if i == 1:
        for j in range(3):
            garra(lz, x + (j - 1) * 46 * s * 2, y - 20 * s + 14 * s * abs(j - 1), 1.6 * s, (j - 1) * 0.25, seed=200 + j)
    elif i == 4:
        D.adn(lz, x, y, 0.75 * s * 2, t, largo=280, marca=(0.36, 0.64), seed=210, vertical=True)
    elif i == 6:
        oreja(lz, x, y, 0.7 * s * 2)
    else:
        dibujar_icono(lz, ("pegamento", "", "corazon", "pastilla", "", "mamut", "")[i], x, y, s, t)


# ============================================================ utilidades
def entra(t, t0, desde, hasta, dur=0.45):
    """Posición de algo que se desliza desde 'desde' hasta 'hasta' con leve rebote."""
    return lerp(desde, hasta, e_back(prog(t, t0, t0 + dur), 1.2))


def giro(t, seed=0):
    return 0.03 * math.sin(t * 1.7 + seed) + 0.02 * math.sin(t * 3.1 + seed * 2)


def punto(x, y, s, rot, px, py):
    """Coordenadas del mundo de un punto local (px, py) de un objeto colocado con (x, y, s, rot)."""
    c, sn = math.cos(rot), math.sin(rot)
    return x + s * (px * c - py * sn), y + s * (px * sn + py * c)


class ItemLlegaEnMovimiento(Item):
    """Ítem al que se llega con un movimiento de cámara (paneo, bajada, zoom): su tarjeta 'MITO N' ya está en
    pantalla mientras la cámara llega, así el plano nunca queda vacío."""
    ADELANTO = 0.55

    def preparar(self):
        Item.preparar(self)
        self.A = self.t0 - self.ADELANTO


def sello_falso(lz, t, t0, x=1500, y=430, dur=1.9):
    """Sello rojo FALSO que cae con golpe y se va."""
    u = prog(t, t0, t0 + 0.2)
    if u <= 0 or t > t0 + dur:
        return
    salida = e_in(prog(t, t0 + dur - 0.3, t0 + dur))
    k = (1 + 1.4 * (1 - e_out(u))) * (1 - salida)
    if k <= 0.01:
        return
    w = ancho_texto("FALSO", "snap", 100) + 90
    with lz.capa(2):
        with lz.grupo(x, y, k, -0.14):
            lz.forma(rect_red(-w / 2, -70, w, 140, 18), (255, 246, 236), ROJO_SELLO, 12, seed=901)
            lz.texto("FALSO", 0, 4, 100, "snap", color=ROJO_SELLO, borde=None, seed=902)


def corazones(lz, t, t0, x, y, n=5, dur=2.0, seed=0):
    """Corazones que suben desde (x, y)."""
    for i in range(n):
        u = (t - t0 - 0.25 * i) / dur
        if 0 < u < 1:
            hx = x + 60 * math.sin(u * 5 + i * 2.1) + (i - n / 2) * 40
            hy = y - 320 * u
            lz.forma(corazon(hx, hy, 34 * (1 - 0.3 * u)), ROJO, NEGRO, 5, seed + i, capa=2)


# ---- objetos nuevos (tinta del estilo doodle)
def lasca(lz, x, y, s=1.0, rot=0.0, seed=11, col=(150, 150, 160)):
    """Punta de piedra (sílex) tallada: apunta hacia +x."""
    with lz.grupo(x, y, s, rot):
        lz.forma([(-70, 6), (-20, -46), (30, -34), (110, 2), (30, 36), (-24, 46)], col, NEGRO, 6, seed)
        lz.trazo([(-20, -30), (50, -12)], (208, 208, 216), 5, seed=seed + 1)
        lz.trazo([(-30, 24), (40, 14)], (108, 108, 120), 4, seed=seed + 2)


def alquitran(lz, x, y, s=1.0, seed=12, gota=0.0):
    with lz.grupo(x, y, s):
        lz.forma(blob(0, 0, 60, seed=seed, irr=0.16, lob=5) * [1.0, 0.72], (36, 30, 32), NEGRO, 5, seed)
        lz.trazo([(-24, -14), (8, -24)], (120, 114, 120), 6, seed=seed + 1)
        if gota > 0:
            lz.forma(elipse(30, 44 + 40 * gota, 12, 18), (36, 30, 32), NEGRO, 4, seed + 3)


def mango(lz, x, y, s=1.0, rot=0.0, seed=13):
    with lz.grupo(x, y, s, rot):
        lz.forma(rect_red(-200, -16, 400, 32, 14), (176, 116, 62), NEGRO, 6, seed)
        lz.trazo([(-150, -4), (-60, -2)], (122, 78, 40), 4, seed=seed + 1)
        lz.trazo([(40, 5), (130, 3)], (122, 78, 40), 4, seed=seed + 2)


def herramienta(lz, x, y, s=1.0, rot=0.0, u=1.0, seed=14, tar=1.0):
    """Palo con punta de piedra pegada con alquitrán. u: 0 piezas separadas, 1 armada."""
    sep = (1 - u) * 160
    with lz.grupo(x, y, s, rot):
        mango(lz, -20 - sep, 0, 1.0, 0.0, seed)
        lasca(lz, 205 + sep, 0, 0.85, 0.0, seed + 3)
        if tar > 0 and u > 0.55:
            alquitran(lz, 178, 4, 0.55 * tar, seed + 6)


def corteza(lz, x, y, s=1.0, rot=0.0, seed=15):
    with lz.grupo(x, y, s, rot):
        lz.forma(catmull([(-90, -10), (-30, -32), (50, -26), (98, -6), (60, 16), (-40, 20)], 6, True),
                 (238, 234, 224), NEGRO, 6, seed)
        for k in range(5):
            lz.trazo([(-70 + k * 34, -14 + 4 * (k % 2)), (-60 + k * 34, 8)], (62, 52, 52), 5, seed=seed + k)


def abedul(lz, x, y, s=1.0, seed=16):
    """y = base del tronco."""
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-38, -420, 76, 420, 16), (244, 240, 232), NEGRO, OW, seed)   # tronco blanco
        for k in range(8):
            lz.trazo([(-30 + 6 * (k % 2), -380 + k * 50), (-6 + 14 * (k % 3) - 6, -372 + k * 50)], (52, 46, 48), 6, seed=seed + k)
        for bx, by, br in ((0, -470, 110), (-80, -410, 80), (80, -420, 84), (-30, -540, 70), (60, -510, 62)):
            lz.forma(blob(bx, by, br, seed=seed + bx, irr=0.14), (108, 176, 82), NEGRO, 6, seed + bx)


def pino(lz, x, y, s=1.0, seed=17):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-16, -70, 32, 70, 6), (120, 78, 44), NEGRO, 5, seed)
        for k, (w, yy) in enumerate(((150, -60), (120, -150), (90, -230), (60, -300))):
            lz.forma([(-w, yy), (w, yy), (0, yy - 120)], (58, 140, 82), NEGRO, 6, seed + k + 1)


def garra(lz, x, y, s=1.0, rot=0.0, seed=18, cortes=0.0, brillo=0.0):
    """Garra de águila: base ancha arriba, punta curva hacia abajo."""
    with lz.grupo(x, y, s, rot):
        lz.forma(catmull([(-26, -50), (26, -50), (30, -10), (22, 30), (2, 66), (-30, 96), (-14, 50), (-26, 6)], 6, True),
                 (78, 56, 44), NEGRO, 6, seed)
        lz.trazo([(-10, -40), (-2, -8), (-4, 30)], (136, 104, 84), 5, seed=seed + 1)
        for k in range(int(3 * cortes + 0.001)):
            lz.trazo([(-32 + 9 * k, -22 + 22 * k), (-8 + 9 * k, -14 + 22 * k)], (252, 246, 228), 4, seed=seed + 5 + k)
        if brillo > 0:
            lz.forma(estrella(12, -22, 20 * brillo, 6 * brillo, 4, rot=brillo * 3), (255, 255, 225), None, 0, seed + 9, capa=2)


def muela(lz, x, y, s=1.0, absceso=0.0, seed=19):
    """Muela con banda de sarro amarillo; absceso 0..1 = bulto rojo en la raíz."""
    with lz.grupo(x, y, s):
        if absceso > 0:
            lz.forma(circulo(-52, 150, 34 * absceso, 20), (222, 70, 80), NEGRO, 5, seed + 9)
        pts = catmull([(-95, -115), (-60, -155), (-20, -138), (0, -122), (20, -138), (60, -155), (95, -115), (102, -40),
                       (86, 30), (62, 120), (32, 154), (12, 64), (-12, 64), (-32, 154), (-62, 120), (-86, 30), (-102, -40)], 6, True)
        lz.forma(pts, (250, 248, 240), NEGRO, OW, seed)
        lz.trazo(catmull([(-93, 12), (-40, 26), (0, 30), (40, 26), (93, 12)], 6), (206, 158, 66), 30, seed=seed + 1)
        lz.trazo([(-60, -110), (-30, -125)], BLANCO, 8, seed=seed + 2)


def oreja(lz, x, y, s=1.0, col=None, seed=20):
    col = col or D.PIEL_N
    with lz.grupo(x, y, s):
        lz.forma(catmull([(-40, -130), (20, -150), (84, -104), (94, -20), (62, 52), (32, 114), (-20, 124), (-52, 84), (-42, 20)], 6, True),
                 col, NEGRO, OW, seed)
        lz.trazo(catmull([(-20, -96), (30, -108), (58, -60), (44, 10), (18, 60), (0, 78)], 6), (170, 110, 80), 8, seed=seed + 1)
        lz.trazo(catmull([(4, -50), (30, -40), (20, 0)], 5), (170, 110, 80), 6, seed=seed + 2)


def botiquin(lz, x, y, s=1.0, abre=0.0, seed=22):
    with lz.grupo(x, y, s):
        lz.trazo(arco(0, -84, 52, math.pi, 2 * math.pi, 14), (120, 120, 130), 12, seed=seed + 4)
        lz.forma(rect_red(-130, -80, 260, 200, 18), (250, 248, 244), NEGRO, OW, seed)
        lz.relleno(rect_red(-15, -36, 30, 110, 4), ROJO, seed + 1)
        lz.relleno(rect_red(-55, 4, 110, 30, 4), ROJO, seed + 2)
        with lz.grupo(-130, -80, 1.0, -abre * 0.55):      # tapa con bisagra a la izquierda
            lz.forma(rect_red(0, -46, 260, 46, 12), (236, 96, 86), NEGRO, 6, seed + 3)


def moho(lz, x, y, s=1.0, seed=23):
    """Placa con colonias de moho verde-azulado (Penicillium)."""
    with lz.grupo(x, y, s):
        lz.forma(circulo(0, 0, 120, 40), (244, 240, 226), NEGRO, OW, seed)
        for k, (cx, cy, r) in enumerate(((-30, -22, 44), (36, 26, 34), (-10, 46, 24), (48, -38, 22))):
            lz.forma(blob(cx, cy, r, seed=seed + k, irr=0.2, lob=8), (110, 196, 164), NEGRO, 4, seed + k)
            lz.relleno(blob(cx, cy, r * 0.55, seed=seed + k + 9, irr=0.2, lob=6), (64, 146, 156), seed + k + 9)


def hoja(lz, x, y, s=1.0, rot=0.0, seed=24):
    with lz.grupo(x, y, s, rot):
        lz.forma(catmull([(0, -150), (70, -80), (84, 10), (40, 90), (0, 130), (-40, 90), (-84, 10), (-70, -80)], 6, True),
                 (110, 184, 72), NEGRO, OW, seed)
        lz.trazo([(0, -140), (0, 150)], (60, 120, 44), 6, seed=seed + 1)
        for k in range(4):
            lz.trazo([(0, -90 + 50 * k), (46, -50 + 50 * k)], (60, 120, 44), 4, seed=seed + 2 + k)
            lz.trazo([(0, -90 + 50 * k), (-46, -50 + 50 * k)], (60, 120, 44), 4, seed=seed + 8 + k)


def pinon(lz, x, y, s=1.0, seed=25):
    with lz.grupo(x, y, s, 0.5):
        lz.forma(catmull([(0, -46), (26, -10), (18, 40), (0, 50), (-18, 40), (-26, -10)], 6, True), (196, 150, 96), NEGRO, 5, seed)
        lz.trazo([(-8, -20), (-6, 30)], (140, 96, 56), 4, seed=seed + 1)
        lz.trazo([(8, -18), (6, 28)], (140, 96, 56), 4, seed=seed + 2)


def hongo(lz, x, y, s=1.0, seed=26):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-16, -6, 32, 56, 10), (246, 236, 214), NEGRO, 5, seed)
        lz.forma(catmull([(-52, -6), (-40, -40), (0, -56), (40, -40), (52, -6)], 6, True), (220, 70, 64), NEGRO, 5, seed + 1)
        for k, (px, py) in enumerate(((-22, -26), (10, -38), (26, -18))):
            lz.relleno(circulo(px, py, 6, 10), BLANCO, seed + 2 + k)


def musgo(lz, x, y, s=1.0, seed=27):
    with lz.grupo(x, y, s):
        lz.forma(blob(0, 0, 44, seed=seed, irr=0.25, lob=9) * [1.2, 0.8], (96, 160, 70), NEGRO, 5, seed)
        for k in range(6):
            lz.relleno(circulo(-30 + 12 * k, -8 + 10 * (k % 2), 6, 8), (150, 206, 96), seed + 1 + k)


def barra_genoma(lz, x0, x1, y, naranja, t, k=1.0):
    """100 casillas (1 % cada una); las primeras `naranja` (0..100) en naranja: la parte neandertal."""
    n = 100
    ancho = (x1 - x0) / n
    lz.forma(rect_red(x0 - 14, y - 60 * k, x1 - x0 + 28, 120 * k, 24), (250, 246, 238), NEGRO, 7, seed=300)
    for i in range(n):
        naran = i < naranja
        col = (255, 150, 40) if naran else ((110, 200, 255) if i % 2 else (255, 130, 176))
        lz.relleno(rect_red(x0 + i * ancho + 1, y - 44 * k, ancho - 2, 88 * k, 3), col, seed=301 + i, temblor=0.15)


def pantalla_audio(lz, t, t0):
    lz.relleno(rect_red(-95, -185, 190, 370, 20), (236, 229, 221), seed=730, temblor=0.3)
    kk = pop(t, t0, 0.3)
    if kk > 0:
        with lz.grupo(0, -40, kk):
            lz.relleno(rect_red(-82, -32, 164, 64, 28), (190, 240, 170), seed=731, temblor=0.3)
            lz.relleno([(-64, -15), (-64, 15), (-42, 0)], (60, 100, 60), seed=732)
            for i in range(9):
                h = 6 + 16 * abs(math.sin(i * 1.7 + t * 3))
                lz.trazo([(-28 + i * 8, -h), (-28 + i * 8, h)], (60, 100, 60), 4, seed=733 + i)
            lz.texto("1:00", 0, 52, 30, "snap", color=(60, 100, 60), borde=None, k=kk, seed=750)


# ============================================================ INTRO
class Intro(Escena):
    def preparar(self):
        self.f1, self.f2 = self.fr[1]["t0"], self.fr[2]["t0"]
        self.t_bru = self.w("brutos")
        self.t_tor = self.w("torpes")
        self.t_cer = self.w("cerebro")
        self.t_pro = self.w("promedio")
        self.t_tuy = self.w("tuyo")
        self.t_sie = self.w("siete")
        self.t_der = self.w("derrumbó")
        self.t_sube = self.fr[0]["t0"] - 0.15
        self.lineas = ["NEANDERTALES:", "7 MITOS QUE LA", "CIENCIA YA DERRUMBÓ"]
        for i in range(3):
            self.ev(0.15 + 0.3 * i, "impacto" if i == 0 else "pop", 0.8, tono=0.9 + 0.1 * i)
        self.ev(self.t_sube, "whoosh", 0.5, dur=0.4)
        self.ev(self.t_bru, "error", 0.5, pan=0.4)
        self.ev(self.t_tor, "error", 0.5, pan=0.4, tono=0.9)
        self.ev(self.t_cer, "brillo", 0.7)
        self.ev(self.f2 - 0.2, "whoosh", 0.5, dur=0.4)
        for k in range(7):
            self.ev(self.t_sie + 0.14 * k, "pop", 0.45, pan=-0.6 + 0.2 * k, tono=0.9 + 0.08 * k)
        self.ev(self.t_der, "impacto", 0.7)

    def fondo(self, t):
        return mezcla_fondos(t, self.t_sube, lambda tt: fondo_estilo("titulo", tt, "ocre", env_bombo(tt)),
                             lambda tt: fondo_estilo("libre", tt, "ocre", env_bombo(tt)))

    def camara(self, t):
        return 1.0 + 0.02 * math.sin(t * 0.8), 0.006 * math.sin(t * 0.6), 0.0, 0.0

    def dibujar(self, lz, t):
        sube = e_inout(prog(t, self.t_sube, self.t_sube + 0.5))
        px = 118
        for lin in self.lineas:                       # que el renglón más ancho quepa
            px = min(px, 118 * 1650 / max(1650, ancho_texto(lin, "snap", 118)))
        with lz.grupo(960, lerp(540, 138, sube), lerp(1.0, 0.5, sube)):
            for i, lin in enumerate(self.lineas):
                k = pop(t, 0.15 + 0.3 * i, 0.35)
                if k > 0:
                    lz.texto(lin, 0, (i - 1) * px * 1.2, px, "snap", color=color_arcoiris(t * 0.2 + i * 0.25), borde=NEGRO,
                             borde_px=12, k=k, rot=0.03 * math.sin(t * 2 + i), seed=10 + i)
        # 1) brutos y torpes
        if t < self.f2 + 0.2:
            fuera = e_in(prog(t, self.f1 - 0.2, self.f1 + 0.2))
            xn = entra(t, self.t_sube + 0.2, -300, 520) - 1300 * fuera
            if t > self.t_sube + 0.2:
                D.personaje(lz, xn, 930, 0.95, t, "neander", seed=22, mano_i=(-150, -150), mano_d=(150, -150),
                            boca=0.0, cejas=0.8, mirar=(0.6, 0.2), ojos="normal")
            for i, (tt, txt) in enumerate(((self.t_bru, "¿BRUTOS?"), (self.t_tor, "¿TORPES?"))):
                kk = pop(t, tt, 0.3) * (1 - fuera)
                if kk > 0:
                    chip(lz, 1330, 470 + 130 * i, txt, kk, 56, seed=30 + i, fuente="snap", rot=-0.04 + 0.05 * i)
                    D.tache(lz, 1330, 470 + 130 * i, 0.62 * kk, prog(t, tt + 0.45, tt + 0.75), seed=32 + i)
        # 2) cerebro más grande que el tuyo
        if self.f1 - 0.25 <= t < self.f2 + 0.2:
            fuera = e_in(prog(t, self.f2 - 0.25, self.f2 + 0.2))
            k1 = pop(t, self.t_cer, 0.4) * (1 - fuera)
            if k1 > 0:
                D.cerebro(lz, 620, 620, 1.55 * k1, t, seed=41, brillo=0.6)
                chip(lz, 620, 830, "NEANDERTAL", k1, 46, seed=42, fuente="snap")
            k2 = pop(t, self.t_tuy - 0.1, 0.4) * (1 - fuera)
            if k2 > 0:
                D.cerebro(lz, 1300, 640, 1.2 * k2, t, seed=43, col=(160, 200, 255))
                chip(lz, 1300, 830, "TÚ", k2, 46, seed=44, fuente="snap")
                lz.texto(">", 960, 640, 210, "snap", color=AMARILLO, borde=NEGRO, borde_px=16, k=k2, rot=0.0, seed=45)
            chip(lz, 960, 380, "EN PROMEDIO", pop(t, self.t_pro, 0.3) * (1 - fuera), 44, seed=46)
        # 3) siete mitos, derrumbados
        if t >= self.f2 - 0.3:
            for i in range(7):
                tk = self.t_sie + 0.14 * i
                k = pop(t, tk, 0.35)
                if k > 0:
                    gx = 260 + 233 * i
                    icono_mito(lz, i, gx, 620 + 10 * math.sin(t * 2 + i), 0.5 * k, t)
                    lz.texto(str(i + 1), gx, 800, 84, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=k, seed=50 + i)
                    D.tache(lz, gx, 620, 0.6 * k, prog(t, self.t_der + 0.09 * i, self.t_der + 0.09 * i + 0.3), seed=60 + i)


# ============================================================ 1. TORPES
class Torpes(Item):
    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_dos = self.w("doscientos", frase=1)
        self.t_alq = self.w("alquitrán", frase=1)
        self.t_abe = self.w("abedul", frase=1)
        self.t_peg1 = self.w("pegamento", frase=1)
        self.t_obt = self.w("obtenían", frase=2)
        self.t_cal = self.w("calentando", frase=2)
        self.t_cor = self.w("corteza", frase=2)
        self.t_pgb = self.w("pegaban", frase=2)
        self.t_pie = self.w("piedras", frase=2)
        self.t_man = self.w("mangos", frase=2)
        self.t_mar = self.w("Mar del Norte", frase=3)
        self.t_her = self.w("herramienta", frase=3)
        self.t_cin = self.w("cincuenta", frase=3)
        self.t_pg3 = self.w("pegamento", frase=3)
        self.t_tub = self.w("tubito", frase=4)
        self.t_ver = self.w("versión", frase=4)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_alq, "pop", 0.5, pan=0.4)
        self.ev(self.t_abe, "pop", 0.5, pan=0.5, tono=1.1)
        self.ev(self.t_cal, "fuego", 0.4, dur=2.4)
        self.ev(self.t_pgb, "golpe_suave", 0.7)
        self.ev(self.t_mar, "chapuzon", 0.5)
        self.ev(self.t_her, "aparicion", 0.5)
        self.ev(self.t_pg3, "ding", 0.5, tono=1.3)
        self.ev(self.t_tub, "boing", 0.6, pan=0.4)
        self.ev(self.t_ver, "boing", 0.6, pan=-0.4, tono=1.15)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "pegamento", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.26 * s, t)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal)
        f3 = e_in(prog(t, self.t_mar - 0.35, self.t_mar + 0.15))
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        herr_x, herr_y = 1190, 640
        # ---- frases 1 y 2: el pegamento de abedul
        if f3 < 1:
            with lz.grupo(-1500 * f3, 0):
                kn = pop(t, self.B + 0.15, 0.45)
                cal = t >= self.t_cal - 0.1
                if kn > 0:
                    xn = entra(t, self.B + 0.15, -300, 400)
                    mano = (250 + 8 * math.sin(t * 6), -140) if cal else (150, -170)
                    obj = (lambda lz, hx, hy: corteza(lz, hx + 40, hy - 8, 0.8, -0.1, seed=70)) if cal else None
                    D.personaje(lz, xn, 900, 1.0, t, "neander", seed=71, mano_i=(-150, -170), mano_d=mano, obj_d=obj,
                                mirar=(1, 0.3), boca=0.0, cejas=0.4)
                    if cal:
                        D.fuego(lz, 400 + 250 + 90, 906, 0.85 * pop(t, self.t_cal, 0.4), t, seed=72)
                chip(lz, 430, 330, "ITALIA · ~200.000 AÑOS", pop(t, self.t_dos, 0.3) * sale(t, self.t_obt - 0.1), 40, seed=73)
                ka = pop(t, self.t_abe, 0.45)
                if ka > 0:
                    abedul(lz, 1700, 900, 0.8 * ka, seed=74)
                chip(lz, 1700, 340, "ABEDUL", pop(t, self.t_abe + 0.1, 0.3), 40, seed=75)
                kq = pop(t, self.t_alq, 0.4)
                if kq > 0:
                    mover = e_inout(prog(t, self.t_pgb - 0.1, self.t_pgb + 0.5))
                    ax, ay = lerp(1010, herr_x - 40, mover), lerp(780, herr_y + 4, mover)
                    if mover < 1:
                        alquitran(lz, ax, ay + 8 * math.sin(t * 2), 1.15 * kq, seed=76, gota=0.5 + 0.5 * math.sin(t * 3))
                        chip(lz, 1010, 650, "ALQUITRÁN DE ABEDUL", kq * (1 - mover), 38, seed=77)
                kh = pop(t, self.t_pgb, 0.4)
                if kh > 0:
                    u = e_inout(prog(t, self.t_pgb, self.t_pgb + 0.7))
                    herramienta(lz, herr_x, herr_y + 6 * math.sin(t * 2), 1.15 * kh, -0.08, u=u, seed=78)
                    chip(lz, herr_x + 60, 470, "PIEDRA AFILADA", pop(t, self.t_pie, 0.3), 38, seed=79)
                    chip(lz, herr_x - 60, 810, "MANGO DE MADERA", pop(t, self.t_man, 0.3), 38, seed=80)
        # ---- frase 3: la herramienta del Mar del Norte
        if self.t_mar - 0.4 <= t < self.C + 0.4:
            with lz.grupo(-1500 * fb, 0):
                ola = e_out(prog(t, self.t_mar - 0.2, self.t_mar + 0.6))
                D.olas(lz, lerp(1150, 830, ola), t, amp=16, seed=111, capas=3)
                kh = pop(t, self.t_her, 0.45)
                if kh > 0:
                    rot = -0.14 + 0.05 * math.sin(t * 1.6)
                    y0 = 610 + 12 * math.sin(t * 1.6)
                    herramienta(lz, 960, y0, 1.6 * kh, rot, u=1.0, seed=81)
                    if t >= self.t_pg3 - 0.1:
                        jx, jy = punto(960, y0, 1.6 * kh, rot, 178, 4)
                        D.destellos(lz, [(jx - 30, jy - 55), (jx + 34, jy - 40), (jx + 6, jy + 52)], t, 1.2, seed=82)
                chip(lz, 430, 330, "MAR DEL NORTE", pop(t, self.t_mar, 0.3), 42, seed=83)
                chip(lz, 1490, 330, "~50.000 AÑOS", pop(t, self.t_cin, 0.3), 44, seed=84)
                chip(lz, 960, 890, "TODAVÍA CON SU PEGAMENTO", pop(t, self.t_pg3, 0.3), 40, seed=85)

    def hoy(self, lz, t):
        kt = pop(t, self.t_tub, 0.4)
        if kt > 0:
            dibujar_icono(lz, "pegamento", 1400, 600 + 8 * math.sin(t * 2), 1.5 * kt, t)
            chip(lz, 1400, 250, "TÚ", kt, 64, seed=90, fuente="snap", rot=0.04)
        kv = pop(t, self.t_ver, 0.4)
        if kv > 0:
            herramienta(lz, 480, 620 + 8 * math.sin(t * 2 + 1), 1.05 * kv, -0.1, u=1.0, seed=91)
            chip(lz, 480, 250, "ELLOS", kv, 64, seed=92, fuente="snap", rot=-0.04)
            lz.texto("=", 940, 610, 200, "snap", color=BLANCO, borde=NEGRO, borde_px=14, k=kv, seed=93)


# ============================================================ 2. JOYAS
class Joyas(ItemLlegaEnMovimiento):
    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_kra = self.w("Krapina", frase=1)
        self.t_och = self.w("ocho", frase=1)
        self.t_gar = self.w("garras", frase=1)
        self.t_cie = self.w("ciento", frase=1)
        self.t_cor = self.w("cortes", frase=2)
        self.t_pul = self.w("pulidas", frase=2)
        self.t_col = self.w("collar", frase=2)
        self.t_ant = self.w("antigua", frase=3)
        self.t_dec = self.w("decenas", frase=3)
        self.t_hum = self.w("humanos", frase=3)
        self.t_tu = self.w("Tú", frase=4)
        self.t_col4 = self.w("collar", frase=4)
        self.t_ell = self.w("Ellos", frase=4)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_kra, "pin", 0.5, pan=-0.4)
        for i in range(8):
            self.ev(self.t_och + 0.13 * i, "pop", 0.4, pan=-0.6 + 0.17 * i, tono=0.9 + 0.05 * i)
        self.ev(self.t_cor, "puntada", 0.5)
        self.ev(self.t_pul, "brillo", 0.6)
        self.ev(self.t_col, "whoosh", 0.6, dur=0.6)
        self.ev(self.t_ant, "bling", 0.6)
        self.ev(self.t_tu, "pop", 0.5, pan=0.4)
        self.ev(self.t_ell, "boing", 0.6, pan=-0.4)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "collar", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.24 * s, t)

    def _pos(self, i, u):
        """Posición de la garra i: en fila (u=0) o colgando de un collar (u=1)."""
        fx, fy = 700 + i * 140, 640
        a = i / 7
        cx = 720 + a * 1000
        cy = 470 + 250 * (1 - (2 * a - 1) ** 2)
        return lerp(fx, cx, u), lerp(fy, cy + 36, u)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal, x=1560, y=440)
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-1500 * fb, 0):
            kn = pop(t, self.B + 0.15, 0.45)
            if kn > 0:
                D.personaje(lz, 300, 900, 0.85 * kn, t, "neander", seed=101, mano_i=(-130, -150), mano_d=(150, -190),
                            mirar=(1, 0.2), boca=0.2, cejas=0.6)
            fuera_c = sale(t, self.t_dec - 0.3, 0.25)      # los rótulos de arriba dejan sitio al de "decenas"
            chip(lz, 430, 330, "KRAPINA · CROACIA", pop(t, self.t_kra, 0.3) * fuera_c, 40, seed=102)
            chip(lz, 1490, 330, "HACE ~130.000 AÑOS", pop(t, self.t_cie, 0.3) * fuera_c, 40, seed=103)
            u = e_inout(prog(t, self.t_col - 0.1, self.t_col + 0.8))
            if u > 0:                                    # el cordel del collar
                pts =[(720 + a * 1000, 470 + 250 * (1 - (2 * a - 1) ** 2) - 6) for a in np.linspace(0, 1, 30)]
                n = max(2, int(30 * u))
                lz.trazo(pts[:n], (150, 100, 60), 6, seed=104)
            for i in range(8):
                k = pop(t, self.t_och + 0.13 * i, 0.35)
                if k <= 0:
                    continue
                gx, gy = self._pos(i, u)
                cortes = clamp01((t - self.t_cor - 0.1 * i) / 0.3)
                brillo = campana(t, self.t_pul + 0.08 * i, self.t_pul + 0.08 * i + 0.6)
                rot = lerp(0.0, 0.04 * math.sin(t * 2 + i), u)
                garra(lz, gx, gy + 5 * math.sin(t * 2 + i) * u, 1.35 * k, rot, seed=110 + i, cortes=cortes, brillo=brillo)
            chip(lz, 960, 890, "LA JOYERÍA MÁS ANTIGUA DE EUROPA", pop(t, self.t_ant, 0.3), 40, seed=105)
            chip(lz, 960, 330, "DECENAS DE MILES DE AÑOS ANTES DE LOS HUMANOS MODERNOS", pop(t, self.t_dec, 0.3), 32, seed=106)

    def hoy(self, lz, t):
        kt = pop(t, self.t_tu, 0.4)
        ke = pop(t, self.t_ell, 0.4)
        if kt > 0:
            D.personaje(lz, 1380, 900, 0.95 * kt, t, "tu", seed=120, accesorios=("collar",), mano_d=(140, -200),
                        boca=-0.5, mirar=(-0.6, 0))
            chip(lz, 1380, 260, "TÚ", kt, 64, seed=121, fuente="snap", rot=0.04)
        if ke > 0:
            s0 = 0.95 * ke
            salto = 60 * abs(math.sin((t - self.t_ell) * 5)) * math.exp(-(t - self.t_ell) * 1.6)
            D.personaje(lz, 560, 900, s0, t, "neander", seed=122, mano_d=(140, -200), salto=salto, boca=-0.5, mirar=(0.6, 0))
            with lz.grupo(560, 900 - salto, s0):       # el collar de garras sobre el pecho
                for j, p in enumerate(arco(0, -262, 58, 0.5, math.pi - 0.5, 5, ry=52)):
                    garra(lz, p[0], p[1] + 8, 0.32, 0.0, seed=130 + j)
            chip(lz, 560, 260, "ELLOS", ke, 64, seed=123, fuente="snap", rot=-0.04)


# ============================================================ 3. CUIDADO
class Cuidado(Item):
    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_sha = self.w("Shanidar", frase=1)
        self.t_bra = self.w("brazo", frase=1)
        self.t_coj = self.w("cojera", frase=1)
        self.t_sor = self.w("sordera", frase=1)
        self.t_cua = self.w("cuarenta", frase=2)
        self.t_gru = self.w("grupo", frase=2)
        self.t_cui = self.w("cuidó", frase=2)
        self.t_cov = self.w("Cova Negra", frase=3)
        self.t_sin = self.w("síndrome", frase=3)
        self.t_sei = self.w("seis", frase=3)
        self.t_cd4 = self.w("Cuidar", frase=4)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_sha, "pin", 0.5, pan=-0.4)
        for tt, tono in ((self.t_bra, 1.0), (self.t_coj, 0.9), (self.t_sor, 0.8)):
            self.ev(tt, "error", 0.4, pan=0.4, tono=tono)
        self.ev(self.t_cua, "ding", 0.5)
        self.ev(self.t_gru, "pasos", 0.4, dur=0.9)
        self.ev(self.t_cui, "latido", 0.7)
        self.ev(self.t_cov, "pin", 0.5, pan=-0.4)
        self.ev(self.t_sin, "bebe", 0.5, pan=0.3)
        self.ev(self.t_sei, "campana", 0.4)
        self.ev(self.t_cd4, "latido", 0.8)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "corazon", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.24 * s, t)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal, x=1560, y=440)
        f2 = self.fr[2]["t0"]
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        sale1 = e_in(prog(t, f2 - 0.2, f2 + 0.2))
        with lz.grupo(-1500 * fb, 0):
            kn = pop(t, self.B + 0.15, 0.45)
            xh = 640
            if kn > 0:
                baston = lambda lz, hx, hy: lz.trazo([(hx, hy + 10), (hx - 14, -8)], (140, 90, 50), 14, seed=140, afinar=False)
                D.personaje(lz, xh, 900, 1.0 * kn, t, "neander", seed=141, incl=-0.05, mano_i=(-150, -110),
                            mano_d=(110, -70), obj_i=baston, mirar=(1, 0.3), cejas=-0.2, paso=0.2)
            chip(lz, 430, 330, "SHANIDAR · IRAK", pop(t, self.t_sha, 0.3), 40, seed=142)
            for i, (tt, txt, x, y) in enumerate(((self.t_bra, "BRAZO ATROFIADO", 1320, 470), (self.t_coj, "COJERA", 1320, 600),
                                                 (self.t_sor, "SORDERA", 1320, 730))):
                k = pop(t, tt, 0.3) * (1 - sale1)
                if k > 0:
                    chip(lz, x, y, txt, k, 42, seed=143 + i)
            ks = pop(t, self.t_sor, 0.3) * (1 - sale1)
            if ks > 0:
                oreja(lz, 1640, 730, 0.5 * ks)
                D.tache(lz, 1640, 730, 0.9 * ks, prog(t, self.t_sor + 0.2, self.t_sor + 0.5), seed=147)
            kc = pop(t, self.t_cua, 0.4)
            if kc > 0:
                lz.texto("40+ AÑOS", 1320, 500, 130, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, k=kc, rot=-0.05, seed=148)
            for j, (cx, cs, seedj) in enumerate(((240, 0.62, 150), (1040, 0.6, 151), (1180, 0.5, 152))):
                kg = pop(t, self.t_gru + 0.2 * j, 0.4)
                if kg > 0:
                    hueso = (lambda lz, hx, hy: D.hueso(lz, hx + 30, hy - 20, 0.25, 0.7, seed=153)) if j != 1 else None
                    D.personaje(lz, entra(t, self.t_gru + 0.2 * j, cx - 200, cx), 900, cs * kg, t, "neander", seed=seedj,
                                mano_d=(150, -200), obj_d=hueso, mirar=(1 if cx < xh else -1, 0.2), boca=-0.3)
            corazones(lz, t, self.t_cui, xh, 480, n=6, seed=160)
            chip(lz, 960, 340, "SU GRUPO LO CUIDÓ", pop(t, self.t_cui, 0.3), 42, seed=161)

    def hoy(self, lz, t):
        f4 = self.fr[4]["t0"]
        pasa = e_inout(prog(t, f4 - 0.3, f4 + 0.3))
        if pasa < 1:
            with lz.grupo(-1500 * pasa, 0):
                kb = pop(t, self.C + 0.1, 0.45)
                if kb > 0:
                    D.bebe(lz, 560, 730 + 6 * math.sin(t * 2), 2.2 * kb, t, seed=170)
                    D.personaje(lz, 1120, 900, 0.9 * kb, t, "neander", seed=171, mano_i=(-250, -150), mirar=(-1, 0.4),
                                boca=-0.3, cejas=0.4)
                    D.personaje(lz, 1520, 900, 0.7 * kb, t, "neander", seed=172, mirar=(-1, 0.2), boca=-0.2)
                chip(lz, 430, 330, "COVA NEGRA · ESPAÑA", pop(t, self.t_cov, 0.3), 40, seed=173)
                chip(lz, 1490, 330, "SÍNDROME DE DOWN", pop(t, self.t_sin, 0.3), 40, seed=174)
                ks = pop(t, self.t_sei, 0.4)
                if ks > 0:
                    lz.texto("AL MENOS 6 AÑOS", 480, 440, 80, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=ks, rot=-0.04, seed=176)
        kc = pop(t, self.t_cd4 - 0.1, 0.4)
        if kc > 0:
            k = kc * (1 + 0.06 * env_bombo(t))
            lz.forma(corazon(960, 600, 230 * k), ROJO, NEGRO, 10, seed=180)
            D.personaje(lz, 460, 900, 0.95 * kc, t, "neander", seed=181, mano_d=(230, -260), boca=-0.5, mirar=(1, 0))
            D.personaje(lz, 1460, 900, 0.95 * kc, t, "tu", seed=182, mano_i=(-230, -260), boca=-0.5, mirar=(-1, 0))
            lz.texto("CUIDAR", 960, 330, 110, "snap", color=BLANCO, borde=NEGRO, borde_px=12, k=kc, rot=-0.03, seed=183)


# ============================================================ 4. DIETA
class Dieta(ItemLlegaEnMovimiento):
    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_sid = self.w("Sidrón", frase=1)
        self.t_sar = self.w("sarro", frase=1)
        self.t_pin = self.w("piñones", frase=1)
        self.t_mus = self.w("musgo", frase=1)
        self.t_hon = self.w("hongos", frase=1)
        self.t_abs = self.w("absceso", frase=2)
        self.t_ala = self.w("álamo", frase=2)
        self.t_ana = self.w("analgésico", frase=2)
        self.t_moh = self.w("moho", frase=2)
        self.t_pen = self.w("penicilina", frase=2)
        self.t_bot = self.w("botiquín", frase=3)
        self.t_ten = self.w("tenía", frase=3)
        self.t_bos = self.w("bosque", frase=3)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_sid, "pin", 0.5, pan=-0.4)
        self.ev(self.t_sar, "puntada", 0.5)
        for k, tt in enumerate((self.t_pin, self.t_mus, self.t_hon)):
            self.ev(tt, "pop", 0.5, pan=0.3 + 0.1 * k, tono=1 + 0.12 * k)
        self.ev(self.t_abs, "error", 0.6)
        self.ev(self.t_ala, "revelar", 0.5, pan=-0.4)
        self.ev(self.t_moh, "puf", 0.5, pan=0.4)
        self.ev(self.t_pen, "ding", 0.5, pan=0.4)
        self.ev(self.t_bot, "clink", 0.6, pan=-0.4)
        self.ev(self.t_bos, "viento", 0.4, dur=1.2)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "pastilla", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.24 * s, t)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal, x=1560, y=440)
        f2 = self.fr[2]["t0"]
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        sale1 = e_in(prog(t, f2 - 0.2, f2 + 0.2))
        with lz.grupo(-1500 * fb, 0):
            kt = pop(t, self.B + 0.15, 0.45)
            if kt > 0:
                ab = pop(t, self.t_abs, 0.4)
                dolor = 6 * math.sin(t * 30) * campana(t, self.t_abs, self.t_abs + 1.5)
                muela(lz, 960 + dolor, 590, 1.5 * kt, absceso=ab, seed=310)
            chip(lz, 430, 330, "EL SIDRÓN · ESPAÑA", pop(t, self.t_sid, 0.3), 40, seed=311)
            ks = pop(t, self.t_sar, 0.3) * (1 - sale1)
            if ks > 0:
                chip(lz, 600, 700, "SARRO", ks, 42, seed=312)
                flecha(lz, (690, 690), (830, 640), prog(t, self.t_sar, self.t_sar + 0.3), color=AMARILLO, ancho=12, seed=313, curva=0.2)
            # lupa sobre el sarro: qué comió
            kl = pop(t, self.t_pin - 0.3, 0.4) * (1 - sale1)
            if kl > 0:
                with lz.grupo(1330, 590, kl):
                    lz.forma(circulo(0, 0, 200, 60), (255, 250, 238), NEGRO, 12, seed=314)
                    lz.trazo(circulo(0, 0, 176, 60), (200, 190, 170), 4, cerrado=True, seed=315)
                    k1, k2, k3 = pop(t, self.t_pin, 0.35), pop(t, self.t_mus, 0.35), pop(t, self.t_hon, 0.35)
                    if k1 > 0:
                        pinon(lz, -70, 40, 1.3 * k1, seed=316)
                    if k2 > 0:
                        musgo(lz, 20, -70, 1.4 * k2, seed=317)
                    if k3 > 0:
                        hongo(lz, 80, 40, 1.3 * k3, seed=318)
                for i, (tt, txt) in enumerate(((self.t_pin, "PIÑONES"), (self.t_mus, "MUSGO"), (self.t_hon, "HONGOS"))):
                    chip(lz, 1740, 480 + 110 * i, txt, pop(t, tt, 0.3) * (1 - sale1), 38, seed=319 + i)
            # frase 2: absceso, álamo y penicilina
            chip(lz, 1010, 890, "ABSCESO", pop(t, self.t_abs, 0.3), 42, seed=322)
            flecha(lz, (930, 870), (890, 830), prog(t, self.t_abs, self.t_abs + 0.3), color=AMARILLO, ancho=12, seed=336, curva=0.2)
            kh = pop(t, self.t_ala, 0.4)
            if kh > 0:
                hoja(lz, 400, 560 + 8 * math.sin(t * 2), 1.4 * kh, -0.4, seed=323)
                chip(lz, 400, 790, "ÁLAMO", kh, 42, seed=324)
                flecha(lz, (540, 590), (780, 620), prog(t, self.t_ala, self.t_ala + 0.3), color=AMARILLO, ancho=12, seed=325, curva=0.2)
            chip(lz, 400, 870, "ANALGÉSICO NATURAL", pop(t, self.t_ana, 0.3), 34, seed=326)
            km = pop(t, self.t_moh, 0.4)
            if km > 0:
                moho(lz, 1500, 560, 1.3 * km, seed=327)
                chip(lz, 1500, 790, "MOHO CON PENICILINA", pop(t, self.t_pen, 0.3), 36, seed=328)
                flecha(lz, (1360, 590), (1130, 620), prog(t, self.t_moh, self.t_moh + 0.3), color=AMARILLO, ancho=12, seed=329, curva=-0.2)

    def hoy(self, lz, t):
        kt = pop(t, self.C + 0.1, 0.45)
        if kt > 0:
            cheek = (70, -330) if t < self.t_bot else (150, -190)
            D.personaje(lz, 400, 900, 0.95 * kt, t, "tu", seed=330, mano_d=cheek, boca=0.5, cejas=-0.4, mirar=(1, 0.3))
            botiquin(lz, 960, 640, 1.3 * kt, abre=e_out(prog(t, self.t_bot, self.t_bot + 0.4)), seed=331)
            if t >= self.t_bot + 0.3:
                D.pastilla(lz, 960, 520 - 30 * e_out(prog(t, self.t_bot + 0.3, self.t_bot + 0.7)), 0.5 * pop(t, self.t_bot + 0.3, 0.3), seed=332)
            chip(lz, 400, 330, "TÚ: EL BOTIQUÍN", pop(t, self.C + 0.3, 0.3), 42, seed=333)
        kb = pop(t, self.t_ten, 0.4)
        if kb > 0:
            for j, (px_, ps) in enumerate(((1290, 0.8), (1720, 1.05), (1860, 0.75))):
                pino(lz, px_, 900, ps * kb, seed=340 + j)
            D.personaje(lz, 1480, 900, 0.95 * kb, t, "neander", seed=334, boca=-0.3, mirar=(-0.6, 0), mano_d=(150, -220))
            chip(lz, 1480, 330, "ÉL: EL BOSQUE", kb, 42, seed=335)


# ============================================================ 5. GENES
class Genes(Item):
    STAMP = dict(x=960, y=420)

    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_anc = self.w("ancestros", frase=1)
        self.t_tuv = self.w("tuvieron", frase=1)
        self.t_hij = self.w("hijos", frase=1)
        self.t_sob = self.w("sobrevivieron", frase=1)
        self.t_afr = self.w("África", frase=2)
        self.t_uno = self.w("uno", frase=2)
        self.t_cua = self.w("cuatro", frase=2)
        self.t_gen = self.w("genoma", frase=2)
        self.t_nea = self.w("neandertal", frase=2)
        self.t_par = self.w("parte", frase=3)
        self.t_sig = self.w("sigue", frase=3)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_anc, "pop", 0.5, pan=-0.4)
        self.ev(self.t_tuv, "latido", 0.6)
        self.ev(self.t_hij, "bebe", 0.7)
        self.ev(self.t_sob, "ding", 0.6)
        self.ev(self.t_gen, "revelar", 0.6)
        self.ev(self.t_uno, "tick", 0.6)
        self.ev(self.t_cua, "tick", 0.6, tono=1.4)
        self.ev(self.t_par, "brillo", 0.6)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            D.adn(lz, x + 340 * math.cos(a), y + 150 * math.sin(a), 0.22 * s, t, largo=300, seed=350)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal, **self.STAMP)
        f2 = self.fr[2]["t0"]
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        sale1 = e_in(prog(t, f2 - 0.2, f2 + 0.25))
        with lz.grupo(-1500 * fb, 0):
            if sale1 < 1:
                with lz.grupo(-1400 * sale1, 0):
                    acerca = e_inout(prog(t, self.t_tuv - 0.3, self.t_tuv + 0.6))
                    xa = entra(t, self.B + 0.15, -300, 520) + 90 * acerca
                    xn = entra(t, self.B + 0.15, 2200, 1400) - 90 * acerca
                    D.personaje(lz, xa, 900, 0.95, t, "cave", seed=351, mano_d=(200, -200), mirar=(1, 0.2), boca=0.2)
                    D.personaje(lz, xn, 900, 0.95, t, "neander", seed=352, mano_i=(-200, -200), mirar=(-1, 0.2), boca=0.2)
                    chip(lz, 520, 330, "ANCESTROS", pop(t, self.t_anc, 0.3), 42, seed=353)
                    if t >= self.t_tuv:
                        corazones(lz, t, self.t_tuv, 960, 560, n=5, dur=2.4, seed=354)
                    kb = pop(t, self.t_hij, 0.45)
                    if kb > 0:
                        D.bebe(lz, 960, 760 + 8 * math.sin(t * 3), 2.2 * kb, t, seed=355)
                    ks = pop(t, self.t_sob, 0.3)
                    if ks > 0:
                        palomita(lz, 1090, 560, 1.6 * ks, prog(t, self.t_sob, self.t_sob + 0.4), seed=356)
                        chip(lz, 960, 400, "¡SOBREVIVIERON!", ks, 44, seed=357)
            # frase 2: 1 – 4 % del genoma
            ka = pop(t, self.t_afr, 0.35)
            if ka > 0:
                chip(lz, 960, 330, "SI TUS ANTEPASADOS VIENEN DE FUERA DE ÁFRICA", ka, 36, seed=358)
            kg = pop(t, f2 + 0.05, 0.4)
            if kg > 0:
                pct = 1 if t < self.t_cua else lerp(1, 4, e_out(prog(t, self.t_cua, self.t_cua + 0.4)))
                nar = 0 if t < self.t_uno else pct
                barra_genoma(lz, 260, 1660, 640, nar, t, kg)
                chip(lz, 440, 520, "TU GENOMA", kg, 40, seed=359)
                if nar > 0:
                    lz.texto("1–4 %", 1000, 810, 120, "snap", color=(255, 170, 60), borde=NEGRO, borde_px=13,
                             k=pop(t, self.t_uno, 0.3), rot=-0.03, seed=360)
                kn = pop(t, self.t_nea, 0.3)
                if kn > 0:
                    chip(lz, 500, 800, "NEANDERTAL", kn, 42, seed=362)
                    flecha(lz, (440, 765), (290, 700), prog(t, self.t_nea, self.t_nea + 0.3), color=AMARILLO, ancho=12, seed=361, curva=0.3)

    def hoy(self, lz, t):
        k = pop(t, self.C + 0.1, 0.45)
        if k > 0:
            D.personaje(lz, 520, 900, 1.0 * k, t, "tu", seed=370, mano_d=(150, -200), boca=-0.4, mirar=(1, 0))
            D.adn(lz, 520, 714, 0.28 * k, t, largo=600, marca=(0.42, 0.58), seed=371)
            kl = pop(t, self.t_par, 0.4)
            if kl > 0:
                with lz.grupo(1260, 570, kl):
                    lz.forma(circulo(0, 0, 250, 60), (255, 250, 238), NEGRO, 12, seed=372)
                    D.adn(lz, 0, 0, 1.0, t, largo=400, marca=(0.36, 0.64), seed=373)
                flecha(lz, (680, 690), (1000, 610), prog(t, self.t_par, self.t_par + 0.3), color=AMARILLO, ancho=14, seed=374, curva=0.15)
            chip(lz, 1260, 880, "UNA PARTE DE ELLOS SIGUE EN TI", pop(t, self.t_sig, 0.3), 40, seed=375)


# ============================================================ 6. EXTINCIÓN
class Extincion(ItemLlegaEnMovimiento):
    X0, X1, YB = 200, 1720, 620

    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_lin = self.w("linaje", frase=1)
        self.t_tre = self.w("trescientos", frase=1)
        self.t_gla = self.w("glaciaciones", frase=1)
        self.t_des = self.w("desaparecieron", frase=2)
        self.t_cua = self.w("cuarenta", frase=2)
        self.t_con = self.w("convivir", frase=2)
        self.t_deb = self.w("debate", frase=3)
        self.t_cli = self.w("clima", frase=3)
        self.t_enf = self.w("enfermedades", frase=3)
        self.t_com = self.w("competencia", frase=3)
        self.t_mez = self.w("mezcla", frase=3)
        self.t_esp = self.w("especie", frase=4)
        self.t_mis = self.w("mismo", frase=4)
        self.t_fra = self.w("fracaso", frase=4)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_lin, "revelar", 0.5, dur=1.0)
        self.ev(self.t_tre, "ding", 0.6)
        self.ev(self.t_gla, "hielo", 0.5)
        self.ev(self.t_cua, "campana", 0.5)
        self.ev(self.t_con, "pop", 0.5)
        for k, tt in enumerate((self.t_cli, self.t_enf, self.t_com, self.t_mez)):
            self.ev(tt, "pop", 0.55, pan=-0.5 + 0.35 * k, tono=1 + 0.1 * k)
        self.ev(self.fr[3]["t0"] + 0.05, "hmm", 0.6)
        self.ev(self.t_esp, "revelar", 0.5, dur=1.0)
        self.ev(self.t_fra, "error", 0.7)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "mamut", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.22 * s, t)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal, x=1560, y=440)
        f3 = self.fr[3]["t0"]
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        baja = e_in(prog(t, f3 - 0.2, f3 + 0.35))
        with lz.grupo(-1500 * fb, 0):
            # la nieve de las glaciaciones
            if t >= self.t_gla and baja < 1:
                with lz.capa(2):
                    for i in range(16):
                        u = ((t - self.t_gla) * (0.12 + 0.03 * (i % 4)) + h01(i, 1)) % 1.0
                        D.copo(lz, 100 + 1720 * h01(i, 2) + 30 * math.sin(t * 1.5 + i), 200 + 760 * u,
                               (0.35 + 0.35 * h01(i, 3)) * min(1, (t - self.t_gla) * 2), t * 0.6 + i, seed=380 + i)
            with lz.grupo(0, 900 * baja):
                kb = pop(t, self.B + 0.15, 0.4)
                fr = e_inout(prog(t, self.t_lin, self.t_tre + 0.5)) * kb
                lz.forma(rect_red(self.X0, self.YB - 24, self.X1 - self.X0, 48, 24), (74, 50, 36), NEGRO, 6, seed=381)
                if fr > 0.01:
                    lz.forma(rect_red(self.X0, self.YB - 24, (self.X1 - self.X0) * fr, 48, 24), (200, 132, 76), NEGRO, 6, seed=382)
                    km = 0.5 * kb * sale(t, self.t_des - 0.1, 0.3)        # el mamut se va cuando "desaparecieron"
                    if km > 0.02:
                        D.mamut(lz, self.X0 + (self.X1 - self.X0) * fr, self.YB - 84, km, t, seed=383)
                lz.texto("+300.000 AÑOS", 800, 430, 110, "snap", color=AMARILLO, borde=NEGRO, borde_px=13,
                         k=pop(t, self.t_tre, 0.35), rot=-0.03, seed=384)
                chip(lz, 430, 330, "GLACIACIONES", pop(t, self.t_gla, 0.3), 40, seed=385)
                kc = pop(t, self.t_cua, 0.35)
                if kc > 0:
                    lz.trazo([(self.X1, self.YB - 70), (self.X1, self.YB + 70)], ROJO_SELLO, 10, seed=386)
                    chip(lz, 1500, 760, "HACE ~40.000 AÑOS", kc, 42, seed=387)
                kv = pop(t, self.t_con, 0.4)
                if kv > 0:
                    D.personaje(lz, 1500, self.YB - 24, 0.42 * kv, t, "neander", seed=388, mirar=(1, 0), boca=-0.3)
                    D.personaje(lz, 1640, self.YB - 24, 0.42 * kv, t, "cave", seed=389, mirar=(-1, 0), boca=-0.3)
                    chip(lz, 1570, 330, "CONVIVIERON", kv, 40, seed=390)
            # frase 3: ¿por qué?
            kq = pop(t, f3 + 0.05, 0.4) * (1 - fb)
            if kq > 0:
                lz.texto("¿POR QUÉ?", 960, 290, 120, "snap", color=AMARILLO, borde=NEGRO, borde_px=13, k=kq, rot=-0.03, seed=396)
            for i, (tt, txt, x, y) in enumerate(((self.t_cli, "¿CLIMA?", 620, 460), (self.t_enf, "¿ENFERMEDADES?", 1300, 460),
                                                   (self.t_com, "¿COMPETENCIA?", 620, 700), (self.t_mez, "¿MEZCLA?", 1300, 700))):
                kk = pop(t, tt, 0.3) * (1 - fb)
                if kk > 0:
                    chip(lz, x, y, txt, kk, 60, seed=391 + i, fuente="snap", rot=-0.04 + 0.03 * i)

    def hoy(self, lz, t):
        x0, x1 = 300, 1620
        for i, (tt, txt, y, col) in enumerate(((self.t_esp, "NEANDERTALES", 570, (200, 132, 76)),
                                              (self.t_mis, "NUESTRA ESPECIE", 780, (90, 170, 235)))):
            k = pop(t, tt - 0.1, 0.4)
            if k > 0:
                fr = e_inout(prog(t, tt, tt + 1.1))
                lz.forma(rect_red(x0, y - 34, x1 - x0, 68, 34), (74, 50, 36), NEGRO, 6, seed=400 + i)
                if fr > 0.01:
                    lz.forma(rect_red(x0, y - 34, (x1 - x0) * fr, 68, 34), col, NEGRO, 6, seed=402 + i)
                chip(lz, x0 + 200, y - 90, txt, k, 42, seed=404 + i, fuente="snap")
                if fr > 0.9:
                    lz.texto("~300.000 AÑOS", (x0 + x1) / 2, y + 4, 44, "snap", color=BLANCO, borde=NEGRO, borde_px=6, k=k, seed=406 + i)
        kf = pop(t, self.t_fra - 0.1, 0.35)
        if kf > 0:
            lz.texto("FRACASO", 960, 290, 130, "snap", color=BLANCO, borde=NEGRO, borde_px=14, k=kf, rot=-0.03, seed=408)
            D.tache(lz, 960, 290, 1.0 * kf, prog(t, self.t_fra + 0.05, self.t_fra + 0.4), seed=409)


# ============================================================ 7. HABLA
class Habla(Item):
    def escena(self):
        self.t_fal = self.w("falso", frase=1)
        self.t_esc = self.w("escanear", frase=1)
        self.t_oid = self.w("oído", frase=1)
        self.t_cie = self.w("científicos", frase=1)
        self.t_ran = self.w("rango", frase=1)
        self.t_son = self.w("sonidos", frase=1)
        self.t_par = self.w("parecido", frase=1)
        self.t_aut = self.w("autores", frase=2)
        self.t_com = self.w("comunicación", frase=2)
        self.t_hab = self.w("hablada", frase=2)
        self.t_efi = self.w("eficiente", frase=2)
        self.t_aud = self.w("audios", frase=3)
        self.t_min = self.w("minuto", frase=3)
        self.t_ell = self.w("Ellos", frase=3)
        self.t_oi3 = self.w("oído", frase=3)
        self.ev(self.t_fal, "impacto", 0.8)
        self.ev(self.t_esc, "obturador", 0.6)
        self.ev(self.t_oid, "pop", 0.5)
        self.ev(self.t_son, "eco", 0.5)
        self.ev(self.t_par, "ding", 0.5, tono=1.2)
        self.ev(self.t_com, "comic", 0.4)
        self.ev(self.t_efi, "brillo", 0.5)
        self.ev(self.t_aud, "ding", 0.6, tono=1.4)
        self.ev(self.t_oi3, "boing", 0.5)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "chat", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.22 * s, t)

    def antes(self, lz, t):
        sello_falso(lz, t, self.t_fal, x=1560, y=440)
        f2 = self.fr[2]["t0"]
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        sale1 = e_in(prog(t, f2 - 0.2, f2 + 0.25))
        with lz.grupo(-1500 * fb, 0):
            kn = pop(t, self.B + 0.15, 0.45)
            xh = 430
            if kn > 0:
                habla = t >= self.t_hab
                D.personaje(lz, xh, 900, 0.95 * kn, t, "neander", seed=410, mirar=(1, 0.1),
                            boca=(0.5 + 0.5 * math.sin(t * 12)) * 0.5 if habla else 0.0)
            # el escáner alrededor de la cabeza
            ke = pop(t, self.t_esc - 0.2, 0.4) * (1 - sale1)
            if ke > 0:
                with lz.grupo(xh, 560, ke):
                    lz.trazo(rect_red(-180, -190, 360, 380, 50), (186, 192, 208), 30, cerrado=True, seed=411)
                    lz.trazo(rect_red(-180, -190, 360, 380, 50), NEGRO, 4, cerrado=True, seed=412)
                    ys = 170 * math.sin((t - self.t_esc) * 3.2)
                    lz.trazo([(-160, ys), (160, ys)], (90, 230, 255), 9, seed=413, capa=2)
                chip(lz, xh, 330, "ESCÁNER", ke, 40, seed=414)
            # oído + sonidos + rango
            ko = pop(t, self.t_oid, 0.4) * (1 - sale1)
            if ko > 0:
                oreja(lz, 900, 560, 1.15 * ko)
                for j in range(3):
                    u = ((t - self.t_son) * 0.9 + j / 3) % 1.0
                    if t >= self.t_son:
                        lz.trazo(arco(900, 560, 170 + 90 * u, -0.7, 0.7, 14), (90, 200, 255), 8, seed=415 + j, capa=2)
                chip(lz, 900, 330, "OÍDO INTERNO", ko, 40, seed=418)
            kr = pop(t, self.t_ran, 0.4) * (1 - sale1)
            if kr > 0:
                for r, (txt, y, col) in enumerate((("NEANDERTAL", 560, (200, 132, 76)), ("HUMANO", 790, (90, 170, 235)))):
                    chip(lz, 1560, y - 165, txt, kr, 36, seed=419 + r)
                    for b in range(10):
                        h = 40 + 90 * abs(math.sin(b * 0.7 + 0.5)) * (1 + 0.04 * r * math.sin(t * 3 + b))
                        lz.forma(rect_red(1280 + b * 60, y - h, 46, h, 6), col, NEGRO, 5, seed=421 + r * 10 + b)
                lz.texto("≈", 1170, 680, 180, "snap", color=AMARILLO, borde=NEGRO, borde_px=14,
                         k=pop(t, self.t_par, 0.3) * (1 - sale1), seed=443)
            # frase 2: hablar
            kc = pop(t, self.t_aut, 0.4) * (1 - fb)
            if kc > 0:
                xc = entra(t, self.t_aut, 2200, 1440)
                D.personaje(lz, xc, 900, 0.95, t, "cave", seed=444, mirar=(-1, 0.1),
                            boca=(0.5 + 0.5 * math.sin(t * 10 + 1)) * 0.5 if t >= self.t_hab else 0.0)
                if t >= self.t_com:
                    for lado, (bx, by) in enumerate(((640, 480), (1210, 480))):
                        kb = pop(t, self.t_com + 0.35 * lado, 0.3)
                        if kb > 0:
                            with lz.grupo(bx, by, kb):
                                lz.forma(rect_red(-90, -46, 180, 92, 40), BLANCO, NEGRO, 6, seed=445 + lado)
                                cola = -1 if lado == 0 else 1
                                lz.forma([(-30 * cola + 10, 40), (-100 * cola, 90), (-30 * cola + 50 * cola, 40)], BLANCO, None, 0, seed=447 + lado)
                                for d in range(3):
                                    lz.relleno(circulo(-40 + 40 * d, 0, 10 + 4 * math.sin(t * 8 + d), 12), (80, 80, 96), seed=449 + d)
                chip(lz, 960, 330, "TAN EFICIENTE COMO LA NUESTRA", pop(t, self.t_efi, 0.3), 42, seed=452)

    def hoy(self, lz, t):
        k = pop(t, self.C + 0.1, 0.45)
        if k > 0:
            D.telefono(lz, 1330, 570, 1.25 * k, giro(t, 3), t=t, seed=460, pantalla=lambda lz: pantalla_audio(lz, t, self.t_aud))
            chip(lz, 1330, 330, "HOY: AUDIOS DE UN MINUTO", pop(t, self.t_aud, 0.3), 40, seed=461)
        ke = pop(t, self.t_ell, 0.4)
        if ke > 0:
            escucha = t >= self.t_oi3
            D.personaje(lz, 560, 900, 0.95 * ke, t, "neander", seed=462, mano_d=(120, -350) if escucha else (150, -170),
                        mirar=(1, 0), boca=0.0, cejas=0.4 if escucha else 0.0)
            chip(lz, 560, 330, "ELLOS: YA TENÍAN EL OÍDO", ke, 40, seed=463)


# ============================================================ CIERRE
class Cierre(OutroGenerico):
    def preparar(self):
        OutroGenerico.preparar(self)
        self.f1, self.f2 = self.fr[1]["t0"], self.fr[2]["t0"]
        self.t_lla = self.w("llama")
        self.t_nea = self.w("neandertal")
        self.t_cum = self.w("cumplido")
        self.t_pal = [self.w(p) for p in ("cerebro", "herramientas", "joyas", "medicinas", "compasión")]
        self.t_mit = self.w("mitos")
        self.t_cre = self.w("creías")
        self.ev(self.t_nea, "pop", 0.5)
        self.ev(self.t_cum, "latido", 0.7)
        for k, tt in enumerate(self.t_pal):
            self.ev(tt, "pop", 0.5, pan=-0.6 + 0.3 * k, tono=1 + 0.08 * k)
        for k in range(7):
            self.ev(self.f2 - 0.1 + 0.12 * k, "pop", 0.4, pan=-0.6 + 0.2 * k, tono=0.9 + 0.06 * k)

    def dibujar(self, lz, t):
        if t >= self.fin:
            for i, lin in enumerate(partir_lineas(self.d.get("cierre", "¿CUÁL CREÍAS?"), 18)):
                lz.texto(lin, 960, 380 + i * 140, 110, "snap", color=AMARILLO if i == 0 else BLANCO, borde=NEGRO,
                         borde_px=12, k=pop(t, self.fin + 0.15 * i, 0.4), rot=-0.03, seed=150 + i)
            return
        fuera = e_in(prog(t, self.fin - 0.1, self.fin + 0.2))
        with lz.grupo(0, 0, 1.0 - 0.0 * fuera):
            # 1) "neandertal" como cumplido
            if t < self.f1 + 0.2:
                sale = e_in(prog(t, self.f1 - 0.25, self.f1 + 0.15))
                with lz.grupo(0, 900 * sale):
                    k = pop(t, self.t0 - 0.5, 0.45)          # ya están en pantalla mientras llega el paneo
                    if k > 0:
                        cum = t >= self.t_cum
                        D.personaje(lz, 560, 900, 0.95 * k, t, "tu", seed=470, mano_d=(300, -250), mirar=(1, 0), boca=0.3)
                        D.personaje(lz, 1360, 900, 0.95 * k, t, "neander", seed=471, mirar=(-1, 0), boca=-0.5 if cum else 0.0,
                                    ojos="corazon" if cum else "normal")
                    chip(lz, 560, 330, "¡NEANDERTAL!", pop(t, self.t_nea, 0.3), 46, seed=472, fuente="snap")
                    if t >= self.t_cum:
                        corazones(lz, t, self.t_cum, 1360, 460, n=6, seed=473)
                        chip(lz, 1360, 330, "¡UN CUMPLIDO!", pop(t, self.t_cum, 0.3), 46, seed=474, fuente="snap")
            # 2) todo lo que sí tenían
            if self.f1 - 0.3 <= t < self.f2 + 0.2:
                sale = e_in(prog(t, self.f2 - 0.25, self.f2 + 0.15))
                with lz.grupo(0, -900 * sale):
                    for i, (tt, txt, ic) in enumerate(zip(self.t_pal, ("CEREBRO GRANDE", "HERRAMIENTAS", "JOYAS", "MEDICINAS", "COMPASIÓN"),
                                                           (None, "pegamento", 1, "pastilla", "corazon"))):
                        kk = pop(t, tt, 0.35)
                        if kk > 0:
                            gx = 360 + 300 * i
                            if ic is None:
                                D.cerebro(lz, gx, 560, 0.95 * kk, t, seed=475)
                            elif ic == 1:
                                icono_mito(lz, 1, gx, 560, 0.9 * kk, t)
                            else:
                                dibujar_icono(lz, ic, gx, 560, 0.85 * kk, t)
                            chip(lz, gx, 800 + 60 * (i % 2), txt, kk, 32, seed=476 + i)
            # 3) los siete mitos
            if t >= self.f2 - 0.3:
                for i in range(7):
                    k = pop(t, self.f2 - 0.1 + 0.12 * i, 0.35) * (1 - fuera)
                    if k > 0:
                        gx = 260 + 233 * i
                        salto = 30 * campana(t, self.t_cre + 0.1 * i, self.t_cre + 0.1 * i + 0.5)
                        icono_mito(lz, i, gx, 600 - salto, 0.5 * k, t)
                        lz.texto(str(i + 1), gx, 780, 84, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=k, seed=490 + i)


PROPIAS = dict(intro=Intro, torpes=Torpes, joyas=Joyas, cuidado=Cuidado, dieta=Dieta, genes=Genes,
               extincion=Extincion, habla=Habla, cierre=Cierre)
CLASES = clases_automaticas(PROPIAS)
