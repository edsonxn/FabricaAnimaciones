# -*- coding: utf-8 -*-
"""Escenas de «Un día en la vida hace 30.000 años» — estilo doodle (sin psicodelia), siete momentos del día.
Cada momento: título -> fase A (lo que se hacía) -> fase B (el remate / el dato curioso). Toda aparición está anclada a la palabra que la nombra."""
from escena_base import *  # noqa: F401,F403


# ============================================================ utilidades
def entra(t, t0, desde, hasta, dur=0.45):
    return lerp(desde, hasta, e_back(prog(t, t0, t0 + dur), 1.2))


def lanza(lz, x, y, s, rot, seed=0, col=(150, 110, 70)):
    """Lanza con punta de piedra (origen en la mano; apunta hacia arriba-derecha según rot)."""
    with lz.grupo(x, y, s, rot):
        lz.trazo([(0, 90), (0, -150)], NEGRO, 12, seed=seed)
        lz.trazo([(0, 90), (0, -150)], col, 7, seed=seed + 1)
        lz.forma(np.array([(-14, -140), (0, -205), (14, -140)]), (210, 205, 195), NEGRO, 5, seed=seed + 2)


def animal(lz, x, y, s, tipo, t, flip=False, seed=0, paso=1.0):
    """Cuadrúpedo doodle (origen entre las patas, mira a la derecha). tipo: rino | bisonte | caballo."""
    col, col2 = {"rino": ((160, 150, 165), (120, 110, 125)), "leon": ((214, 170, 110), (170, 128, 80)), "bisonte": ((130, 88, 56), (90, 58, 36)), "caballo": ((196, 146, 92), (120, 80, 50))}[tipo]
    f = -1 if flip else 1
    with lz.grupo(x, y, s * f, 0.0):
        ph = t * 7 * paso
        for i, lx in enumerate((-66, -34, 40, 72)):
            a = math.sin(ph + i * 1.6) * 16 * paso
            lz.forma(rect_red(lx - 9 + a, -92, 18, 92, 6), col2, NEGRO, 5, seed=seed + i)
        lz.forma(elipse(0, -130, 98, 56), col, NEGRO, 6, seed=seed + 5)
        if tipo == "bisonte":
            lz.forma(elipse(40, -176, 54, 44), col2, NEGRO, 6, seed=seed + 6)
            lz.forma(elipse(118, -130, 44, 38), col2, NEGRO, 6, seed=seed + 7)
            lz.trazo([(132, -160), (156, -186), (176, -172)], NEGRO, 7, seed=seed + 8)
        elif tipo == "rino":
            lz.forma(np.array([(84, -168), (108, -188), (132, -160)]), (236, 228, 210), NEGRO, 5, seed=seed + 6)
            lz.forma(elipse(120, -116, 50, 34, -0.2), col, NEGRO, 6, seed=seed + 7)
            lz.forma(np.array([(150, -128), (176, -176), (166, -120)]), (236, 228, 210), NEGRO, 5, seed=seed + 8)
        elif tipo == "leon":
            lz.trazo([(-94, -140), (-140, -170), (-150, -120)], col2, 9, seed=seed + 11)
            lz.forma(np.array([(84, -200), (92, -228), (108, -204)]), col2, NEGRO, 5, seed=seed + 7)
            lz.forma(np.array([(120, -206), (134, -230), (144, -200)]), col2, NEGRO, 5, seed=seed + 8)
            lz.forma(elipse(112, -168, 46, 42), col, NEGRO, 6, seed=seed + 6)
            lz.forma(elipse(146, -156, 20, 15), (240, 222, 190), NEGRO, 5, seed=seed + 9)
        else:
            lz.forma(np.array([(76, -150), (104, -230), (140, -240), (150, -210), (120, -130)]), col, NEGRO, 6, seed=seed + 6)
            lz.forma(elipse(142, -218, 34, 22, -0.4), col, NEGRO, 6, seed=seed + 7)
            lz.trazo([(86, -170), (74, -210), (96, -236)], col2, 10, seed=seed + 8)
            lz.trazo([(-94, -138), (-130, -110), (-124, -60)], col2, 10, seed=seed + 9)
        ex, ey = {"caballo": (148, -222), "leon": (116, -178)}.get(tipo, (124, -128))
        lz.relleno(circulo(ex, ey, 5), NEGRO, seed=seed + 10)


def cueva_roca(lz, x0, y0, x1, y1, seed=0):
    lz.forma(rect_red(x0, y0, x1 - x0, y1 - y0, 40), (92, 70, 62), NEGRO, 8, seed=seed)
    for k in range(9):
        lz.trazo([(x0 + 80 + 190 * k, y0 + 40 + 30 * (k % 3)), (x0 + 130 + 190 * k, y0 + 90)], (70, 52, 46), 6, seed=seed + 1 + k)


def cabana(lz, x, y, s, frac, seed=0):
    """Cabaña de huesos y colmillos de mamut (frac 0..1 = cuánto está construida)."""
    with lz.grupo(x, y, s):
        n = int(14 * frac)
        for k in range(n):
            a = math.pi * (k + 0.5) / 14
            lz.trazo([(-170 * math.cos(a), 0), (-170 * math.cos(a) * 0.15, -170 * math.sin(a))], (232, 218, 182), 11, seed=seed + k)
        if frac > 0.6:
            lz.forma(np.array([(-70, 0), (-50, -90), (50, -90), (70, 0)]), (156, 120, 84), NEGRO, 5, seed=seed + 40)
        if frac > 0.85:
            lz.trazo([(-150, -10), (-90, -210), (0, -240)], (250, 244, 224), 14, seed=seed + 41)
            lz.trazo([(150, -10), (90, -210), (0, -240)], (250, 244, 224), 14, seed=seed + 42)


def pieles(lz, x, y, s, seed=0):
    lz.forma(blob(x, y, 70 * s, seed=seed), (176, 118, 70), NEGRO, 7, seed=seed)
    for k in range(4):
        lz.trazo([(x - 34 * s + 22 * s * k, y - 8 * s), (x - 26 * s + 22 * s * k, y + 10 * s)], (120, 76, 44), 5, seed=seed + 5 + k)


def estrellas_cielo(lz, t, n=24, seed=0, alfa=1.0):
    for i in range(n):
        x = 100 + (i * 173) % 1720
        y = 90 + (i * 97) % 380
        k = 0.6 + 0.4 * math.sin(t * 2.2 + i)
        lz.relleno(estrella(x, y, 13 * k, 5 * k, 4), (255, 244, 190), seed=seed + i, alfa=alfa)


# ============================================================ INTRO
class Intro(Escena):
    def preparar(self):
        self.f1, self.f2 = self.fr[1]["t0"], self.fr[2]["t0"]
        self.t_hace = self.w("treinta")
        self.t_reloj = self.w("reloj")
        self.t_calles = self.w("calles")
        self.t_nadie = self.w("nadie")
        self.t_cer = self.w("cerebro")
        self.t_igual = self.w("igual")
        self.t_camb = self.w("cambia")
        self.t_dia = self.w("dia", frase=2)
        self.t_hielo = self.w("hielo")
        self.ev(0.2, "impacto", 0.8)
        self.ev(self.t_hace, "campana", 0.4)
        for tt in (self.t_reloj, self.t_calles, self.t_nadie):
            self.ev(tt, "error", 0.5, pan=0.3)
        self.ev(self.t_cer, "brillo", 0.6)
        self.ev(self.t_igual, "bling", 0.6)
        self.ev(self.t_camb, "whoosh", 0.5, dur=0.5)
        self.ev(self.t_dia, "pop", 0.6)
        self.ev(self.t_hielo, "hielo", 0.6)

    def fondo(self, t):
        return mezcla_fondos(t, self.f2 - 0.2, lambda tt: fondo_estilo("titulo", tt, "ocre", env_bombo(tt)), lambda tt: fondo_estilo("libre", tt, "ocaso", env_bombo(tt)))

    def camara(self, t):
        return 1.0 + 0.02 * math.sin(t * 0.8), 0.006 * math.sin(t * 0.6), 0.0, 0.0

    def dibujar(self, lz, t):
        # título
        sube = e_inout(prog(t, self.f2 - 0.3, self.f2 + 0.3))
        with lz.grupo(960, lerp(260, 140, sube), lerp(1.0, 0.55, sube)):
            for i, lin in enumerate(("UN DÍA EN LA VIDA", "HACE 30.000 AÑOS")):
                k = pop(t, 0.15 + 0.3 * i, 0.35)
                if k > 0:
                    lz.texto(lin, 0, i * 135, 118, "snap", color=color_arcoiris(t * 0.2 + i * 0.25), borde=NEGRO, borde_px=12, k=k, rot=0.03 * math.sin(t * 2 + i), seed=10 + i)
        # 1) despertar sin reloj, sin calles, sin nadie que mande
        if t < self.f1 + 0.3:
            fuera = e_in(prog(t, self.f1 - 0.25, self.f1 + 0.25))
            with lz.grupo(-2400 * fuera, 0):
                k = pop(t, 0.4, 0.45)
                if k > 0:
                    D.personaje(lz, 560, 960, 0.95 * k, t, "cave", seed=22, mano_i=(-150, -160), mano_d=(150, -240), boca=0.6, cejas=0.3, mirar=(0.6, 0.0), ojos="normal")
                    D.fuego(lz, 250, 960, 0.6 * k, t, seed=23)
                for i, (tt, txt, icono) in enumerate(((self.t_reloj, "SIN RELOJ", "reloj"), (self.t_calles, "SIN CALLES", "ciudad"), (self.t_nadie, "SIN JEFES", "tu"))):
                    kk = pop(t, tt, 0.3)
                    if kk > 0:
                        x = 1280
                        y = 590 + 150 * i
                        dibujar_icono(lz, icono, x - 230, y, 0.3 * kk, t)
                        chip(lz, x + 50, y, txt, kk, 46, seed=30 + i, fuente="snap", rot=-0.04 + 0.04 * i)
                        D.tache(lz, x - 230, y, 0.42 * kk, prog(t, tt + 0.35, tt + 0.65), seed=33 + i)
        # 2) el mismo cerebro
        if self.f1 - 0.25 <= t < self.f2 + 0.25:
            fuera = e_in(prog(t, self.f2 - 0.3, self.f2 + 0.25))
            k1 = pop(t, self.t_cer, 0.4) * (1 - fuera)
            if k1 > 0:
                D.cerebro(lz, 600, 720, 1.3 * k1, t, seed=41, brillo=0.6)
                chip(lz, 600, 930, "SAPIENS · HACE 30.000 AÑOS", k1, 36, seed=42)
            k2 = pop(t, self.t_igual, 0.4) * (1 - fuera)
            if k2 > 0:
                D.cerebro(lz, 1320, 720, 1.3 * k2, t, seed=43, col=(160, 200, 255))
                chip(lz, 1320, 930, "TÚ · HOY", k2, 36, seed=44)
                lz.texto("=", 960, 720, 220, "snap", color=AMARILLO, borde=NEGRO, borde_px=16, k=k2, seed=45)
        # 3) la rueda del día
        if t >= self.f2 - 0.3:
            k = pop(t, self.t_dia - 0.2, 0.5)
            if k > 0:
                D.dia_noche(lz, 960, 650, 1.5 * k, t, seed=46)
                for i in range(7):
                    a = -math.pi / 2 + 2 * math.pi * i / 7 + 0.3 * math.sin(t)
                    kk = pop(t, self.t_dia + 0.12 * i, 0.3)
                    if kk > 0:
                        lz.texto(str(i + 1), 960 + 310 * math.cos(a), 650 + 310 * math.sin(a), 70, "snap", color=AMARILLO, borde=NEGRO, borde_px=9, k=kk, seed=50 + i)
            kh = pop(t, self.t_hielo, 0.4)
            if kh > 0:
                for i in range(5):
                    copo_x = 300 + 330 * i
                    D.copo(lz, copo_x, 360 + 40 * math.sin(t * 2 + i), 0.6 * kh, t * 0.6 + i, seed=60 + i)
                chip(lz, 1570, 650, "ERA DE HIELO", kh, 46, seed=66, fuente="snap")


# ============================================================ 1. AMANECER
class Amanecer(Item):
    def escena(self):
        self.t_frio = self.w("frio", frase=1)
        self.t_brasas = self.w("brasas", frase=1)
        self.t_apag = self.w("apagan", frase=2)
        self.t_enc = self.w("encender", frase=2)
        self.t_golp = self.w("golpeando", frase=2)
        self.t_rato = self.w("rato", frase=2)
        self.t_ropa = self.w("ropa", frase=3)
        self.t_agu = self.w("agujas", frase=3)
        self.t_cua = self.w("cuarenta", frase=3)
        self.t_comp = self.w("compartes", frase=4)
        self.t_grupo = self.w("grupo", frase=4)
        self.t_trein = self.w("treinta", frase=4)
        self.t_fam = self.w("familiares", frase=4)
        self.ev(self.t_frio, "brr", 0.6)
        self.ev(self.t_brasas, "fuego", 0.35, dur=1.6)
        self.ev(self.t_apag, "siseo", 0.6)
        for k in range(3):
            self.ev(self.t_golp + 0.28 * k, "clink", 0.6, tono=1.0 + 0.1 * k)
        self.ev(self.t_rato, "fuego", 0.6, dur=2.4)
        self.ev(self.t_ropa, "pop", 0.6)
        self.ev(self.t_agu, "puntada", 0.6)
        self.ev(self.t_comp, "bling", 0.5)
        self.ev(self.t_trein, "pop", 0.5)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            D.fuego(lz, x + 360 * math.cos(a), y + 160 * math.sin(a), 0.32 * s, t, seed=300 + k)

    def antes(self, lz, t):
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-2400 * fb, 0):
            # amanecer frío
            sol = e_out(prog(t, self.B, self.B + 2.0))
            lz.relleno(circulo(1560, lerp(520, 330, sol), 90), (255, 214, 120), seed=310, alfa=0.9)
            k = pop(t, self.B + 0.1, 0.45)
            if k > 0:
                tirita = 6 * math.sin(t * 28) * (1 if t < self.t_enc else 0.3)
                D.personaje(lz, 640 + tirita, 930, 1.0 * k, t, "cave", seed=311, mano_i=(-100, -150), mano_d=(100, -150), boca=-0.5, cejas=0.7, mirar=(1, 0.2), ojos="normal")
            if t >= self.t_frio - 0.2:
                for i in range(4):
                    D.copo(lz, 330 + 240 * i, 300 + 90 * ((t * 0.5 + i * 0.3) % 1.0), 0.45, t + i, seed=320 + i)
                chip(lz, 640, 360, "BRRR...", pop(t, self.t_frio, 0.3) * sale(t, self.t_apag - 0.2), 50, seed=330, fuente="snap")
            # las brasas y el fuego
            prendido = 1.0 if t < self.t_apag else max(0.0, 1 - e_in(prog(t, self.t_apag, self.t_apag + 0.5)))
            reenc = e_out(prog(t, self.t_rato - 0.4, self.t_rato + 0.4))
            tam = 0.0
            if t >= self.t_brasas - 0.1:
                tam = 0.45 * pop(t, self.t_brasas - 0.1, 0.4) * prendido
            if t >= self.t_apag + 0.5:
                tam = 0.9 * reenc
            if tam > 0.02:
                D.fuego(lz, 1050, 940, tam, t, seed=340)
            chip(lz, 1050, 420, "LAS BRASAS DE ANOCHE", pop(t, self.t_brasas - 0.1, 0.3) * sale(t, self.t_apag - 0.1), 38, seed=341)
            if self.t_apag <= t < self.t_rato + 0.4:
                D.humo(lz, 1050, 800, t - self.t_apag, seed=342, n=5, col=(120, 120, 130))
            # golpear piedras
            if t >= self.t_enc - 0.1:
                kp = pop(t, self.t_enc - 0.1, 0.35) * sale(t, self.t_rato + 0.6)
                if kp > 0:
                    gol = 0.5 + 0.5 * math.sin((t - self.t_golp) * 14) if t >= self.t_golp else 0.0
                    for j, sg in enumerate((-1, 1)):
                        lz.forma(blob(1290 + sg * (40 - 32 * gol), 830, 40 * kp, seed=350 + j), (170, 168, 176), NEGRO, 6, seed=352 + j)
                    if t >= self.t_golp and gol > 0.8:
                        D.destellos(lz, [(1290, 780), (1330, 800), (1250, 800)], t, 1.0, seed=355)
                    chip(lz, 1290, 700, "GOLPEAR PIEDRAS", kp, 36, seed=356)

    def hoy(self, lz, t):
        # ropa de pieles cosida con aguja de hueso
        f4 = e_in(prog(t, self.t_comp - 0.35, self.t_comp + 0.15))
        with lz.grupo(-2400 * f4, 0):
            self._ropa(lz, t)
        self._grupo(lz, t)

    def _ropa(self, lz, t):
        kp = pop(t, self.C + 0.1, 0.4)
        if kp > 0:
            vest = t >= self.t_ropa
            D.personaje(lz, 210 + (0 if vest else 6 * math.sin(t * 28)), 970, 0.7 * kp, t, "cave", seed=359, mano_i=(-100, -150), mano_d=(120, -170 - 30 * math.sin(t * 4)),
                        boca=0.6 if vest else -0.5, cejas=0.1 if vest else 0.7, mirar=(1, 0.1))
        kr = pop(t, self.t_ropa, 0.45)
        if kr > 0:
            pieles(lz, 560, 640, 2.2 * kr, seed=360)
            pieles(lz, 700, 720, 1.6 * kr, seed=361)
            chip(lz, 480, 400, "ROPA DE PIELES", kr, 44, seed=362, fuente="snap")
        ka = pop(t, self.t_agu, 0.4)
        if ka > 0:
            cose = 30 * math.sin(t * 6)
            D.aguja(lz, 980 + cose, 700 - 0.6 * cose, 1.5 * ka, -0.6, seed=363)
            lz.trazo([(765 + cose, 845 - 0.6 * cose), (720 + 20 * math.sin(t * 6), 800), (700, 740)], (240, 230, 200), 5, seed=364)
            chip(lz, 1040, 430, "AGUJA DE HUESO", ka, 44, seed=365, fuente="snap")
        kc = pop(t, self.t_cua - 0.1, 0.4)
        if kc > 0:
            lz.texto(">40.000", 1530, 660, 104, "snap", color=AMARILLO, borde=NEGRO, borde_px=12, k=kc, rot=0.04, seed=366)
            chip(lz, 1530, 780, "AÑOS", kc, 50, seed=367, fuente="snap")
    def _grupo(self, lz, t):
        # el grupo alrededor del fuego
        if t >= self.t_comp - 0.2:
            fade = e_in(prog(t, self.t_comp - 0.25, self.t_comp + 0.2))
            lz.relleno(rect_red(0, 0, 1920, 1080, 0), (20, 16, 30), seed=370, alfa=0.0)
            D.fuego(lz, 960, 900, 1.1 * pop(t, self.t_comp, 0.4), t, seed=371)
            for i, x in enumerate((230, 480, 720, 1200, 1440, 1690)):
                kk = pop(t, self.t_grupo + 0.12 * i, 0.4)
                if kk > 0:
                    D.personaje(lz, x, 950, (0.52 if i % 3 == 2 else 0.68) * kk, t, "cave", seed=372 + i, mano_i=(-110, -150),
                                mano_d=(110, -150 - 30 * math.sin(t * 3 + i)), boca=0.5, cejas=0.1, mirar=(1 if x < 960 else -1, 0.1), ojos="normal")
            chip(lz, 960, 560, "COMPARTES EL FUEGO", pop(t, self.t_comp, 0.3) * sale(t, self.t_trein - 0.1), 46, seed=383, fuente="snap")
            lz.texto("~30", 960, 330, 150, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, k=pop(t, self.t_trein, 0.4), rot=-0.04, seed=380)
            chip(lz, 960, 450, "PERSONAS", pop(t, self.t_trein + 0.1, 0.3), 46, seed=381, fuente="snap")
            chip(lz, 1500, 470, "FAMILIA", pop(t, self.t_fam, 0.3), 46, seed=382, fuente="snap", rot=0.04)


# ============================================================ 2. DESAYUNO
class Desayuno(Item):
    def escena(self):
        self.t_tienda = self.w("tienda", frase=1)
        self.t_refri = self.w("refrigerador", frase=1)
        self.t_recol = self.w("recolectaste", frase=1)
        self.t_frutos = self.w("frutos", frase=1)
        self.t_raices = self.w("raices", frase=1)
        self.t_carne = self.w("carne", frase=1)
        self.t_todos = self.w("todos", frase=2)
        self.t_ninos = self.w("ninos", frase=2)
        self.t_adul = self.w("adultos", frase=2)
        self.t_abue = self.w("abuelos", frase=2)
        self.t_huesos = self.w("huesos", frase=3)
        self.t_mamut = self.w("mamut", frase=3)
        self.t_otros = self.w("otros", frase=4)
        self.t_pesc = self.w("pescado", frase=4)
        self.t_pides = self.w("pides", frase=4)
        self.t_cons = self.w("conseguirlo", frase=4)
        for tt in (self.t_tienda, self.t_refri):
            self.ev(tt, "error", 0.5)
        for k, tt in enumerate((self.t_frutos, self.t_raices, self.t_carne)):
            self.ev(tt, "pop", 0.55, pan=-0.3 + 0.3 * k, tono=1.0 + 0.12 * k)
        for k, tt in enumerate((self.t_ninos, self.t_adul, self.t_abue)):
            self.ev(tt, "pop", 0.5, pan=-0.4 + 0.4 * k, tono=0.9 + 0.12 * k)
        self.ev(self.t_mamut, "rugido", 0.4)
        self.ev(self.t_pesc, "chapuzon", 0.5)
        self.ev(self.t_pides, "bling", 0.5)
        self.ev(self.t_cons, "tambor", 0.5) if False else self.ev(self.t_cons, "golpe_suave", 0.6)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            D.hueso(lz, x + 420 * math.cos(a), y + 170 * math.sin(a), 0.32 * s, a, seed=400 + k)

    def antes(self, lz, t):
        f2 = e_in(prog(t, self.t_todos - 0.35, self.t_todos + 0.15))
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-2400 * fb, 0):
            # sin tienda ni refrigerador
            with lz.grupo(-2400 * f2, 0):
                kt = pop(t, self.t_tienda - 0.1, 0.4)
                if kt > 0:
                    dibujar_icono(lz, "ciudad", 420, 540, 0.75 * kt, t)
                    chip(lz, 420, 330, "TIENDA", kt, 44, seed=410, fuente="snap")
                    D.tache(lz, 420, 560, 0.9 * kt, prog(t, self.t_tienda + 0.3, self.t_tienda + 0.6), seed=411)
                kf = pop(t, self.t_refri - 0.1, 0.4)
                if kf > 0:
                    lz.forma(rect_red(700, 380, 170, 330, 16), (236, 240, 246), NEGRO, 7, seed=412)
                    lz.trazo([(700, 520), (870, 520)], NEGRO, 6, seed=413)
                    lz.trazo([(850, 440), (850, 480)], NEGRO, 10, seed=414)
                    chip(lz, 785, 330, "REFRIGERADOR", kf, 36, seed=415)
                    D.tache(lz, 785, 545, 0.9 * kf, prog(t, self.t_refri + 0.3, self.t_refri + 0.6), seed=416)
                # lo que recolectaste ayer: frutos secos, raíces, carne seca
                kr = pop(t, self.t_recol, 0.4)
                if kr > 0:
                    lz.relleno(rect_red(1050, 640, 640, 230, 40), (170, 120, 70), seed=420)
                    lz.trazo(rect_red(1050, 640, 640, 230, 40), NEGRO, 8, cerrado=True, seed=421)
                    chip(lz, 1370, 560, "LO DE AYER", kr, 40, seed=422, fuente="snap")
                kf1 = pop(t, self.t_frutos, 0.35)
                for i in range(6):
                    if kf1 > 0:
                        lz.forma(circulo(1105 + 44 * (i % 3) + 14 * (i // 3), 715 + 52 * (i // 3), 23 * kf1), (186, 130, 70), NEGRO, 5, seed=430 + i)
                kf2 = pop(t, self.t_raices, 0.35)
                for i in range(3):
                    if kf2 > 0:
                        lz.trazo([(1320 + 44 * i, 680), (1308 + 44 * i, 750), (1330 + 44 * i, 820)], NEGRO, 24 * kf2, seed=443 + i)
                        lz.trazo([(1320 + 44 * i, 680), (1308 + 44 * i, 750), (1330 + 44 * i, 820)], (214, 180, 124), 15 * kf2, seed=440 + i)
                kf3 = pop(t, self.t_carne, 0.35)
                if kf3 > 0:
                    lz.forma(blob(1560, 750, 62 * kf3, seed=449), (150, 60, 50), NEGRO, 6, seed=448)
                    D.hueso(lz, 1560, 750, 0.36 * kf3, 0.5, seed=450, marcas=0)
                chip(lz, 1060, 950, "FRUTOS SECOS", kf1, 34, seed=451)
                chip(lz, 1350, 950, "RAÍCES", kf2, 34, seed=452)
                chip(lz, 1610, 950, "CARNE SECA", kf3, 34, seed=453)
            # todos ayudan: niños, adultos, abuelos
            if t >= self.t_todos - 0.4:
                for i, (tt, sc, inc, txt) in enumerate(((self.t_ninos, 0.5, 0.0, "NIÑOS"), (self.t_adul, 0.85, 0.0, "ADULTOS"), (self.t_abue, 0.7, 0.25, "ABUELOS"))):
                    k = pop(t, tt, 0.4)
                    if k > 0:
                        x = 420 + 540 * i
                        D.personaje(lz, x, 930, sc * k, t, "cave", seed=460 + i, mano_i=(-120, -140), mano_d=(120, -170 + 25 * math.sin(t * 5 + i)), boca=0.6, mirar=(0.4, 0.1), incl=inc)
                        chip(lz, x, 930 - 480 * sc - 30, txt, k, 40, seed=466 + i, fuente="snap")
                lz.texto("TODOS AYUDAN", 960, 330, 92, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.t_todos, 0.4) * sale(t, self.C - 0.1), rot=-0.03, seed=470)

    def hoy(self, lz, t):
        fuera = sale(t, self.t_otros - 0.2)
        for i in range(3):
            kh = pop(t, self.C + 0.15 + 0.12 * i, 0.35) * fuera
            if kh > 0:
                D.hueso(lz, 1130 + 230 * i, 800 + 40 * (i % 2), 0.62 * kh, 0.5 * (i - 1) + 0.05 * math.sin(t * 2 + i), seed=481 + i, marcas=2)
        chip(lz, 1360, 600, "HUESOS DE LA ÉPOCA", pop(t, self.t_huesos, 0.3) * fuera, 42, seed=484, fuente="snap")
        km = pop(t, self.t_mamut - 0.5, 0.5) * fuera
        if km > 0:
            D.mamut(lz, 520, 900, 1.15 * km, t, seed=480)
            lz.texto("¡MUCHO MAMUT!", 960, 330, 96, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=km, rot=-0.03, seed=485)
        kp = pop(t, self.t_pesc - 0.1, 0.45)
        if kp > 0:
            D.olas(lz, 780, t, amp=16, seed=490, capas=3, fondo=1200)
            for i in range(3):
                D.atun(lz, 260 + 240 * i + 40 * math.sin(t * 2 + i), 660 + 40 * math.sin(t * 3 + i * 2), 0.55 * kp, t, seed=491 + i)
            chip(lz, 500, 400, "PESCADO DE RÍO", kp, 46, seed=494, fuente="snap")
        ky = pop(t, self.t_pides - 0.1, 0.4)
        if ky > 0:
            D.hamburguesa(lz, 1560, 640 + 8 * math.sin(t * 2), 1.3 * ky, seed=495)
            chip(lz, 1560, 400, "TÚ PIDES...", ky, 50, seed=496, fuente="snap", rot=0.04)
        kc = pop(t, self.t_cons - 0.6, 0.4)
        if kc > 0:
            D.personaje(lz, 1040, 950, 0.62 * kc, t, "cave", seed=497, mano_i=(-110, -150), mano_d=(150, -300 + 20 * math.sin(t * 5)), boca=0.5, mirar=(-1, 0), cejas=0.4,
                        obj_d=lambda lz, hx, hy: lanza(lz, hx, hy, 0.7, 0.2, seed=499))
            chip(lz, 1040, 520, "ELLOS LO CONSEGUÍAN", kc, 38, seed=498, fuente="snap", rot=-0.03)


# ============================================================ 3. CAZA
class Caza(Item):
    def escena(self):
        self.t_anim = self.w("animales", frase=1)
        self.t_gig = self.w("gigantes", frase=1)
        self.t_mamuts = self.w("mamuts", frase=1)
        self.t_rino = self.w("rinocerontes", frase=1)
        self.t_bis = self.w("bisontes", frase=1)
        self.t_cab = self.w("caballos", frase=1)
        self.t_caz = self.w("cazan", frase=2)
        self.t_grupo = self.w("grupo", frase=2)
        self.t_lanz = self.w("lanzas", frase=2)
        self.t_acorr = self.w("acorralan", frase=2)
        self.t_barr = self.w("barranco", frase=2)
        self.t_solo = self.w("solo", frase=3)
        self.t_alim = self.w("alimenta", frase=3)
        self.t_sem = self.w("semanas", frase=3)
        self.t_peli = self.w("peligroso", frase=3)
        self.t_hues = self.w("huesos", frase=4)
        self.t_colm = self.w("colmillos", frase=4)
        self.t_cabanas = self.w("cabanas", frase=4)
        self.ev(self.t_gig, "rugido", 0.5)
        for k, tt in enumerate((self.t_mamuts, self.t_rino, self.t_bis, self.t_cab)):
            self.ev(tt, "pop", 0.5, pan=-0.5 + 0.3 * k, tono=0.9 + 0.1 * k)
        self.ev(self.t_grupo, "tambor", 0.5)
        self.ev(self.t_lanz, "whoosh", 0.5, dur=0.5)
        self.ev(self.t_acorr, "galope", 0.5, dur=2.0)
        self.ev(self.t_barr, "impacto", 0.6)
        self.ev(self.t_alim, "latido", 0.5)
        self.ev(self.t_peli, "error", 0.6)
        self.ev(self.t_cabanas, "crece", 0.6, dur=1.0)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "mamut", x + 400 * math.cos(a), y + 160 * math.sin(a), 0.3 * s, t)

    def antes(self, lz, t):
        f2 = e_in(prog(t, self.t_caz - 0.3, self.t_caz + 0.2))
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-2400 * fb, 0):
            with lz.grupo(-2400 * f2, 0):
                D.mamut(lz, lerp(-300, 340, e_out(prog(t, self.t_anim - 0.2, self.t_anim + 1.2))), 900, 0.8, t, seed=500)
                ks = ((self.t_rino, "rino", 760), (self.t_bis, "bisonte", 1100), (self.t_cab, "caballo", 1540))
                for i, (tt, tipo, x) in enumerate(ks):
                    k = pop(t, tt, 0.4)
                    if k > 0:
                        animal(lz, x, 900, 1.05 * k, tipo, t, seed=510 + 11 * i)
                        chip(lz, x, 610 - 110 * (i % 2), ("RINOCERONTE LANUDO", "BISONTE", "CABALLO SALVAJE")[i], k, 34, seed=520 + i)
                chip(lz, 340, 470, "MAMUT", pop(t, self.t_mamuts, 0.3), 40, seed=525)
                lz.texto("¡GIGANTES!", 960, 340, 110, "snap", color=AMARILLO, borde=NEGRO, borde_px=12, k=pop(t, self.t_gig, 0.4), rot=-0.03 + 0.03 * math.sin(t * 2), seed=526)
            if t >= self.t_caz - 0.4:
                # cazan en grupo con lanzas y acorralan en un barranco
                lz.forma(np.array([(1300, 700), (1920, 700), (1920, 1100), (1300, 1100), (1300, 820), (1240, 790)]), (150, 112, 82), NEGRO, 8, seed=530)
                lz.relleno(rect_red(1250, 900, 670, 200, 0), (30, 26, 36), seed=531, alfa=0.85)
                chip(lz, 1690, 590, "BARRANCO", pop(t, self.t_barr, 0.3), 46, seed=532, fuente="snap")
                ac = e_inout(prog(t, self.t_acorr, self.t_barr + 0.8))
                D.mamut(lz, lerp(1000, 1340, ac), lerp(760, 790, prog(t, self.t_barr, self.t_barr + 0.8)) + 60 * e_in(prog(t, self.t_barr + 0.3, self.t_barr + 0.9)), 0.52, t, seed=533)
                for i in range(3):
                    k = pop(t, self.t_caz + 0.12 * i, 0.4)
                    if k > 0:
                        x = 150 + 215 * i + 130 * e_inout(prog(t, self.t_lanz, self.t_acorr)) + 110 * ac
                        D.personaje(lz, x, 930, 0.6 * k, t, "cave", seed=540 + i, mano_i=(-110, -150), mano_d=(120, -240), boca=0.3, cejas=0.5, mirar=(1, 0), paso=math.sin(t * 6),
                                    obj_d=lambda lz, hx, hy, i=i: lanza(lz, hx, hy, 0.9, 0.35, seed=550 + i))
                lz.texto("CAZAN EN GRUPO", 960, 330, 92, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.t_caz, 0.4) * sale(t, self.C - 0.1), rot=0.03, seed=560)
                chip(lz, 480, 480, "LANZAS DE PIEDRA", pop(t, self.t_lanz, 0.3) * sale(t, self.t_barr, 0.3), 38, seed=561)

    def hoy(self, lz, t):
        fb2 = e_in(prog(t, self.t_hues - 0.4, self.t_hues + 0.1))
        with lz.grupo(-2400 * fb2, 0):
            km = pop(t, self.t_solo - 0.1, 0.45)
            if km > 0:
                D.mamut(lz, 480, 880, 1.05 * km, t, seed=570)
                chip(lz, 460, 380, "UN SOLO MAMUT", km, 46, seed=571, fuente="snap")
            for i in range(5):
                kk = pop(t, self.t_alim + 0.12 * i, 0.35)
                if kk > 0:
                    D.personaje(lz, 1170 + 160 * i, 950, 0.5 * kk, t, "cave", seed=575 + i, mano_i=(-100, -150), mano_d=(100, -150 - 30 * math.sin(t * 4 + i)), boca=0.7, mirar=(-1, 0))
            chip(lz, 1500, 590, "ALIMENTA A TODOS", pop(t, self.t_alim, 0.3), 40, seed=580)
            kc = pop(t, self.t_sem - 0.1, 0.4)
            if kc > 0:
                lz.texto("SEMANAS", 1500, 450, 84, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=kc, rot=0.04, seed=581)
            kp = pop(t, self.t_peli, 0.4) * sale(t, self.t_hues - 0.4)
            if kp > 0:
                with lz.grupo(960, 300, 0.8 * kp * (1 + 0.06 * math.sin(t * 9))):
                    lz.forma(np.array([(0, -150), (140, 100), (-140, 100)]), (255, 214, 60), NEGRO, 9, seed=582)
                lz.texto("!", 960, 315, 104, "snap", color=NEGRO, borde=None, k=kp, seed=583)
                chip(lz, 960, 470, "MUY PELIGROSO", kp, 38, seed=584, fuente="snap")
        if t >= self.t_hues - 0.4:
            k = min(1.0, prog(t, self.t_hues, self.t_cabanas + 0.8))
            cabana(lz, 960, 960, 2.2, k, seed=590)
            for i, (tt, txt) in enumerate(((self.t_hues, "HUESOS"), (self.t_colm, "COLMILLOS"))):
                kk = pop(t, tt, 0.35)
                if kk > 0:
                    x = 280 + 1360 * i
                    if i == 0:
                        D.hueso(lz, x, 820 + 10 * math.sin(t * 2), 0.6 * kk, 0.5, seed=595, marcas=3)
                    else:
                        lz.trazo([(x - 110, 900), (x - 60, 760), (x + 50, 700), (x + 120, 720)], NEGRO, 40 * kk, seed=597)
                        lz.trazo([(x - 110, 900), (x - 60, 760), (x + 50, 700), (x + 120, 720)], (250, 244, 224), 26 * kk, seed=596)
                    chip(lz, x, 620, txt, kk, 40, seed=599 + i, fuente="snap")
            chip(lz, 960, 320, "CABAÑAS DE HUESOS", pop(t, self.t_cabanas - 0.1, 0.3), 54, seed=598, fuente="snap")


# ============================================================ 4. MEDIODÍA
class Mediodia(Item):
    def escena(self):
        self.t_caz = self.w("cazan", frase=1)
        self.t_camp = self.w("campamento", frase=1)
        self.t_talla = self.w("talla", frase=1)
        self.t_sil = self.w("silex", frase=2)
        self.t_lam = self.w("laminas", frase=2)
        self.t_afi = self.w("afiladas", frase=2)
        self.t_bist = self.w("bisturi", frase=2)
        self.t_agu = self.w("agujas", frase=3)
        self.t_col = self.w("collares", frase=3)
        self.t_fig = self.w("figuras", frase=3)
        self.t_mar = self.w("marfil", frase=3)
        self.t_hues = self.w("hueso", frase=4)
        self.t_buit = self.w("buitre", frase=4)
        self.t_agj = self.w("agujeros", frase=4)
        self.t_fla = self.w("flauta", frase=4)
        self.t_mus = self.w("musica", frase=4)
        for k in range(4):
            self.ev(self.t_talla + 0.3 * k, "clink", 0.6, tono=1.0 + 0.1 * k)
        self.ev(self.t_afi, "bling", 0.6)
        self.ev(self.t_bist, "zap", 0.4)
        for k, tt in enumerate((self.t_agu, self.t_col, self.t_fig)):
            self.ev(tt, "pop", 0.55, pan=-0.4 + 0.4 * k, tono=1.0 + 0.12 * k)
        for k in range(3):
            self.ev(self.t_fla + 0.25 * k, "pluck", 0.5, tono=1.0 + 0.25 * k)
        self.ev(self.t_mus, "bling", 0.6)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "flauta", x + 380 * math.cos(a), y + 150 * math.sin(a), 0.3 * s, t)

    def antes(self, lz, t):
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-2400 * fb, 0):
            # unos cazan (se van), en el campamento se talla
            kc = pop(t, self.t_caz - 0.1, 0.4) * sale(t, self.t_camp + 1.7, 0.1)
            if kc > 0:
                x = lerp(1560, 2500, e_in(prog(t, self.t_camp - 0.2, self.t_camp + 1.6)))
                D.personaje(lz, x, 930, 0.6 * kc, t, "cave", seed=600, mano_d=(120, -240), mirar=(1, 0), paso=math.sin(t * 6), obj_d=lambda lz, hx, hy: lanza(lz, hx, hy, 0.8, 0.3, seed=601))
                D.personaje(lz, x - 230, 940, 0.52 * kc, t, "cave", seed=602, mano_d=(120, -240), mirar=(1, 0), paso=math.sin(t * 6 + 1), obj_d=lambda lz, hx, hy: lanza(lz, hx, hy, 0.7, 0.3, seed=603))
                chip(lz, 1450, 420, "UNOS CAZAN", kc * sale(t, self.t_camp + 1.2), 38, seed=604)
            kp = pop(t, self.t_camp, 0.45)
            if kp > 0:
                golpe = 0.5 + 0.5 * math.sin((t - self.t_talla) * 13) if t >= self.t_talla else 0.0
                D.personaje(lz, 500, 940, 0.95 * kp, t, "cave", seed=610, mano_i=(-110, -60), mano_d=(150 - 50 * golpe, -90 - 90 * golpe), boca=0.3, cejas=0.5, mirar=(1, 0.4),
                            obj_d=lambda lz, hx, hy: lz.forma(blob(hx + 18, hy - 6, 30, seed=611), (150, 148, 156), NEGRO, 6, seed=612))
                lz.forma(blob(720, 860, 66, seed=613), (214, 206, 190), NEGRO, 7, seed=614)
                if t >= self.t_talla and golpe > 0.85:
                    D.destellos(lz, [(700, 800), (760, 830), (690, 850)], t, 1.0, seed=615)
                chip(lz, 500, 360, "EN EL CAMPAMENTO SE TALLA", pop(t, self.t_talla - 0.1, 0.3), 38, seed=616)
            # sílex -> láminas afiladas como bisturí
            ks = pop(t, self.t_sil, 0.4)
            if ks > 0:
                chip(lz, 720, 950, "SÍLEX", ks, 40, seed=617, fuente="snap")
            for i in range(4):
                kl = pop(t, self.t_lam + 0.12 * i, 0.4)
                if kl > 0:
                    xx = lerp(800, 1100 + 150 * i, e_out(prog(t, self.t_lam + 0.12 * i, self.t_lam + 0.7)))
                    lz.forma(np.array([(xx - 60, 660 + 50 * i), (xx + 70, 640 + 50 * i), (xx - 40, 690 + 50 * i)]), (226, 222, 214), NEGRO, 5, seed=620 + i)
            ka = pop(t, self.t_afi, 0.4)
            if ka > 0:
                D.destellos(lz, [(1300, 640), (1420, 700), (1340, 780)], t, 1.2, seed=625)
                lz.texto("≈ BISTURÍ", 1500, 440, 88, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.t_bist, 0.4), rot=0.04, seed=626)
                chip(lz, 1450, 560, "LÁMINAS AFILADAS", ka, 40, seed=627, fuente="snap")

    def hoy(self, lz, t):
        f4 = e_in(prog(t, self.t_hues - 0.4, self.t_hues + 0.1))
        with lz.grupo(-2400 * f4, 0):
            lz.texto("HECHO A MANO", 960, 190, 84, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.C + 0.1, 0.4), rot=-0.03, seed=629)
            for i, (tt, nombre, x, txt) in enumerate(((self.t_agu, "aguja", 360, "AGUJAS"), (self.t_col, "collar", 940, "COLLARES"), (self.t_fig, "hombre_leon", 1560, "FIGURAS DE MARFIL"))):
                k = pop(t, tt, 0.45)
                if k > 0:
                    if nombre == "aguja":
                        D.aguja(lz, x, 680, 1.3 * k, -0.6 + 0.06 * math.sin(t * 3), seed=630)
                    elif nombre == "collar":
                        D.collar(lz, x, 620, 1.15 * k, 99, seed=631, t=t)
                    else:
                        D.hombre_leon(lz, x, 980, 0.78 * k, 1.0, seed=632)
                    chip(lz, x, 340, txt, k, 42, seed=633 + i, fuente="snap")
        if t >= self.t_hues - 0.4:
            kh = pop(t, self.t_hues, 0.4)
            if kh > 0:
                D.hueso(lz, 460, 680, 0.85 * kh, 0.25 + 0.04 * math.sin(t * 2), seed=640, marcas=int(4 * prog(t, self.t_agj, self.t_agj + 0.8)))
                chip(lz, 460, 470, "HUESO DE BUITRE", pop(t, self.t_buit, 0.3), 40, seed=641, fuente="snap")
                chip(lz, 460, 880, "CON AGUJEROS", pop(t, self.t_agj, 0.3), 36, seed=643)
                kq = kh * sale(t, self.t_fla - 0.4)
                if kq > 0:
                    D.personaje(lz, 1380, 960, 0.85 * kq, t, "cave", seed=645, mano_i=(-150, -200 + 20 * math.sin(t * 5)), mano_d=(110, -150), boca=0.4, cejas=0.4, mirar=(-1, 0.1))
                    chip(lz, 1380, 470, "¿Y SI LE HAGO AGUJEROS?", pop(t, self.t_agj - 0.3, 0.3) * kq, 38, seed=646)
            kf = pop(t, self.t_fla - 0.1, 0.45)
            if kf > 0:
                flecha(lz, (760, 700), (1040, 700), prog(t, self.t_fla - 0.3, self.t_fla + 0.3), seed=644)
                D.flauta(lz, 1380, 690, 1.3 * kf, -0.25 + 0.04 * math.sin(t * 3), seed=642, agujeros_on=(0, 1, 2))
                for i in range(4):
                    kn = pop(t, self.t_fla + 0.25 * i, 0.35)
                    if kn > 0:
                        D.nota(lz, 1340 + 110 * i, 480 - 30 * i - 18 * math.sin(t * 3 + i), 1.0 * kn, color=color_arcoiris(0.15 * i), seed=650 + i)
                chip(lz, 1380, 880, "FLAUTA", kf, 46, seed=655, fuente="snap")
            km = pop(t, self.t_mus, 0.4)
            if km > 0:
                lz.texto("¡YA HABÍA MÚSICA!", 960, 220, 100, "snap", color=AMARILLO, borde=NEGRO, borde_px=12, k=km, rot=-0.03, seed=656)


# ============================================================ 5. TARDE
class Tarde(Item):
    def escena(self):
        self.t_nin = self.w("ninos", frase=1)
        self.t_esc = self.w("escuela", frase=1)
        self.t_apr = self.w("aprenden", frase=1)
        self.t_imi = self.w("imitan", frase=1)
        self.t_caza = self.w("caza", frase=1)
        self.t_tall = self.w("tallan", frase=1)
        self.t_hist = self.w("historias", frase=1)
        self.t_mod = self.w("modelaban", frase=2)
        self.t_ani = self.w("animales", frase=2)
        self.t_fig = self.w("figuras", frase=2)
        self.t_arc = self.w("arcilla", frase=2)
        self.t_coc = self.w("cocian", frase=3)
        self.t_horn = self.w("hornos", frase=3)
        self.t_fgr = self.w("figurillas", frase=3)
        self.t_cer = self.w("ceramica", frase=3)
        self.t_mil = self.w("miles", frase=4)
        self.t_vas = self.w("vasijas", frase=4)
        self.t_bar = self.w("barro", frase=4)
        self.ev(self.t_esc, "error", 0.5)
        self.ev(self.t_imi, "pop", 0.5)
        self.ev(self.t_tall, "clink", 0.5)
        self.ev(self.t_hist, "hmm", 0.4)
        for k, tt in enumerate((self.t_mod, self.t_ani)):
            self.ev(tt, "plop", 0.55, pan=-0.3 + 0.6 * k)
        self.ev(self.t_horn, "fuego", 0.5, dur=2.0)
        self.ev(self.t_cer, "bling", 0.6)
        self.ev(self.t_vas, "pop", 0.55)
        self.ev(self.t_mil, "reloj_rapido", 0.4, dur=1.0)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "vasija", x + 380 * math.cos(a), y + 150 * math.sin(a), 0.3 * s, t)

    def antes(self, lz, t):
        f2 = e_in(prog(t, self.t_mod - 0.35, self.t_mod + 0.15))
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-2400 * fb, 0):
            with lz.grupo(-2400 * f2, 0):
                # los niños no van a la escuela pero aprenden: imitan al adulto
                kn = pop(t, self.t_nin - 0.1, 0.45)
                if kn > 0:
                    gol = math.sin(t * 5)
                    D.personaje(lz, 500, 940, 0.9 * kn, t, "cave", seed=700, mano_i=(-110, -150), mano_d=(150, -250 + 60 * gol), boca=0.4, mirar=(1, 0),
                                obj_d=lambda lz, hx, hy: lanza(lz, hx, hy, 0.9, 0.3, seed=701))
                    D.personaje(lz, 900, 940, 0.55 * kn, t, "cave", seed=702, mano_i=(-110, -150), mano_d=(150, -250 + 60 * gol), boca=0.8, mirar=(-1, 0), cejas=0.3,
                                obj_d=lambda lz, hx, hy: lanza(lz, hx, hy, 0.6, -0.3, seed=703))
                    chip(lz, 900, 560, "NIÑOS", kn, 46, seed=704, fuente="snap")
                ke = pop(t, self.t_esc - 0.1, 0.4) * sale(t, self.t_apr - 0.15)
                if ke > 0:
                    with lz.grupo(1480, 620, ke):
                        lz.forma(rect_red(-150, -100, 300, 220, 10), (220, 210, 190), NEGRO, 7, seed=705)
                        lz.forma(np.array([(-180, -100), (0, -200), (180, -100)]), (180, 90, 80), NEGRO, 7, seed=706)
                        lz.forma(rect_red(-36, 10, 72, 110, 6), (150, 100, 70), NEGRO, 6, seed=714)
                    chip(lz, 1480, 370, "ESCUELA", ke, 40, seed=707)
                    D.tache(lz, 1480, 620, 1.0 * ke, prog(t, self.t_esc + 0.3, self.t_esc + 0.6), seed=708)
                lz.texto("PERO APRENDEN", 1380, 350, 80, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.t_apr, 0.4), rot=-0.03, seed=709)
                for i, (tt, txt) in enumerate(((self.t_imi, "IMITAN LA CAZA"), (self.t_tall, "TALLAN PIEDRA"), (self.t_hist, "ESCUCHAN HISTORIAS"))):
                    chip(lz, 1400, 520 + 130 * i, txt, pop(t, tt, 0.3), 46, seed=710 + i, rot=-0.03 + 0.03 * i)
            # modelan animales con arcilla
            if t >= self.t_mod - 0.4:
                km = pop(t, self.t_mod, 0.4)
                if km > 0:
                    lz.relleno(rect_red(520, 880, 880, 120, 30), (150, 100, 70), seed=720)
                    u = prog(t, self.t_mod, self.t_arc + 0.8)
                    with lz.grupo(960, 880, 0.8 * km):
                        lz.forma(blob(0, -80, 60 + 30 * u, seed=722), (190, 120, 96), NEGRO, 7, seed=723)
                        if u > 0.4:
                            lz.forma(blob(70, -150, 40, seed=724), (190, 120, 96), NEGRO, 7, seed=725)
                        if u > 0.6:
                            lz.forma(blob(-74, -110, 34, seed=726), (190, 120, 96), NEGRO, 7, seed=727)
                    D.mano(lz, 880 + 30 * math.sin(t * 4), 760, 0.65, 0.3, seed=728)
                    D.mano(lz, 1060 - 30 * math.sin(t * 4), 760, 0.65, -0.3, seed=729)
                    chip(lz, 960, 360, "MODELAN ANIMALES", km, 50, seed=730, fuente="snap")
                    chip(lz, 500, 620, "ARCILLA", pop(t, self.t_arc, 0.3), 46, seed=731, fuente="snap")

    def hoy(self, lz, t):
        f4 = e_in(prog(t, self.t_mil - 0.4, self.t_mil + 0.1))
        with lz.grupo(-2400 * f4, 0):
            kh = pop(t, self.t_horn - 0.2, 0.45)
            if kh > 0:
                with lz.grupo(540, 900, 1.5 * kh):
                    lz.forma(np.array([(-200, 0), (-160, -180), (0, -260), (160, -180), (200, 0)]), (176, 120, 80), NEGRO, 8, seed=740)
                    lz.forma(elipse(0, -60, 70, 50), (40, 24, 20), NEGRO, 6, seed=741)
                D.fuego(lz, 540, 840, 0.75 * kh, t, seed=742)
                chip(lz, 540, 420, "HORNO DE TIERRA", kh, 42, seed=743, fuente="snap")
            kf = pop(t, self.t_fgr - 0.1, 0.45)
            if kf > 0:
                with lz.grupo(1400, 860, 1.9 * kf, 0.04 * math.sin(t * 2)):
                    for lx in (-50, -22, 26, 54):
                        lz.forma(rect_red(lx - 9, -36, 18, 40, 6), (176, 104, 78), NEGRO, 5, seed=760 + lx)
                    lz.forma(elipse(0, -70, 76, 44), (206, 130, 100), NEGRO, 7, seed=745)
                    lz.forma(blob(82, -108, 34, seed=746), (206, 130, 100), NEGRO, 7, seed=747)
                    lz.forma(np.array([(66, -134), (72, -160), (88, -138)]), (206, 130, 100), NEGRO, 5, seed=761)
                    lz.relleno(circulo(92, -112, 4), NEGRO, seed=762)
                D.destellos(lz, [(1280, 640), (1540, 700), (1420, 560)], t, 1.0, seed=748)
                chip(lz, 1400, 470, "FIGURILLA DE ARCILLA", kf, 40, seed=749, fuente="snap")
            kc = pop(t, self.t_cer, 0.4)
            if kc > 0:
                lz.texto("LA CERÁMICA MÁS ANTIGUA", 960, 240, 80, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=kc, rot=-0.03, seed=750)
        if t >= self.t_mil - 0.4:
            k = pop(t, self.t_mil, 0.45)
            if k > 0:
                lz.texto("MILES DE AÑOS ANTES", 960, 260, 92, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=k, rot=0.03, seed=751)
                D.vasija(lz, 1250, 760, 1.5 * pop(t, self.t_vas, 0.4), seed=752)
                lz.forma(blob(520, 700, 70, seed=753), (206, 130, 100), NEGRO, 7, seed=754)
                D.mano(lz, 460, 620 + 20 * math.sin(t * 4), 0.65, 0.3, seed=755)
                D.mano(lz, 590, 620 - 20 * math.sin(t * 4), 0.65, -0.3, seed=756)
                flecha(lz, (640, 700), (1050, 740), prog(t, self.t_vas - 0.4, self.t_vas + 0.3), seed=757)
                chip(lz, 1250, 560, "VASIJAS", pop(t, self.t_vas, 0.3), 46, seed=758, fuente="snap")
                chip(lz, 520, 820, "TRABAJAN EL BARRO", pop(t, self.t_bar, 0.3), 40, seed=759)


# ============================================================ 6. ATARDECER
class Atardecer(Item):
    def escena(self):
        self.t_reg = self.w("regresan", frase=1)
        self.t_caz = self.w("cazadores", frase=1)
        self.t_carne = self.w("carne", frase=1)
        self.t_cena = self.w("cena", frase=1)
        self.t_asan = self.w("asan", frase=2)
        self.t_bras = self.w("brasas", frase=2)
        self.t_hoyos = self.w("hoyos", frase=2)
        self.t_calien = self.w("calientes", frase=2)
        self.t_buena = self.w("buena", frase=3)
        self.t_comp = self.w("comparte", frase=3)
        self.t_todos = self.w("todos", frase=3)
        self.t_compartir = self.w("compartir", frase=4)
        self.t_mejor = self.w("mejor", frase=4)
        self.t_sob = self.w("sobrevivir", frase=4)
        self.t_inv = self.w("invierno", frase=4)
        self.ev(self.t_reg, "pasos", 0.5, dur=2.0)
        self.ev(self.t_carne, "pop", 0.5)
        self.ev(self.t_cena, "campana", 0.4)
        self.ev(self.t_asan, "fuego", 0.5, dur=2.4)
        self.ev(self.t_hoyos, "plop", 0.5)
        self.ev(self.t_calien, "siseo", 0.5)
        self.ev(self.t_buena, "bling", 0.5)
        self.ev(self.t_comp, "pop", 0.5)
        self.ev(self.t_compartir, "latido", 0.6)
        self.ev(self.t_inv, "brr", 0.6)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "dia_noche", x + 380 * math.cos(a), y + 150 * math.sin(a), 0.3 * s, t)

    def fondo_antes(self, t):
        return fondo_estilo("antes", t, "ocaso", env_bombo(t))

    def antes(self, lz, t):
        f2 = e_in(prog(t, self.t_asan - 0.35, self.t_asan + 0.15))
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        with lz.grupo(-2400 * fb, 0):
            lz.relleno(circulo(1770, lerp(330, 440, prog(t, self.B, self.t_asan + 2)), 100), (255, 160, 80), seed=770, alfa=0.9)
            with lz.grupo(-2400 * f2, 0):
                for i in range(3):
                    k = pop(t, self.t_reg - 0.2 + 0.2 * i, 0.4)
                    if k > 0:
                        x = lerp(-200, 300 + 300 * i, e_out(prog(t, self.t_reg - 0.2 + 0.2 * i, self.t_reg + 1.6)))
                        D.personaje(lz, x, 940, 0.62 * k, t, "cave", seed=780 + i, mano_i=(-110, -150), mano_d=(110, -300), boca=0.7, mirar=(1, 0), paso=math.sin(t * 6 + i),
                                    obj_d=lambda lz, hx, hy, i=i: D.hueso(lz, hx, hy - 30, 0.42, 0.15, seed=790 + i, marcas=2))
                chip(lz, 600, 340, "REGRESAN LOS CAZADORES", pop(t, self.t_caz, 0.3), 42, seed=795, fuente="snap")
                chip(lz, 600, 450, "CARGADOS DE CARNE", pop(t, self.t_carne, 0.3), 36, seed=798)
                D.fuego(lz, 1400, 940, 1.0 * pop(t, self.t_cena - 0.3, 0.45), t, seed=796)
                chip(lz, 1400, 520, "¡A CENAR!", pop(t, self.t_cena, 0.3), 54, seed=797, fuente="snap", rot=0.04)
            if t >= self.t_asan - 0.4:
                # carne al fuego y hoyos con piedras calientes
                ka = pop(t, self.t_asan - 0.1, 0.45)
                if ka > 0:
                    D.fuego(lz, 500, 940, 1.0 * ka, t, seed=800)
                    for sx in (-1, 1):
                        lz.trazo([(500 + sx * 250, 940), (500 + sx * 230, 640)], NEGRO, 20, seed=805 + sx)
                        lz.trazo([(500 + sx * 250, 940), (500 + sx * 230, 640)], (120, 84, 56), 11, seed=807 + sx)
                    lz.trazo([(230, 650), (770, 650)], NEGRO, 18, seed=801)
                    lz.trazo([(230, 650), (770, 650)], (120, 84, 56), 10, seed=809)
                    for i in range(3):
                        lz.forma(blob(380 + 120 * i, 655 + 6 * math.sin(t * 4 + i), 46 * ka, seed=802 + i), (166, 74, 56), NEGRO, 6, seed=812 + i)
                    chip(lz, 500, 460, "ASAN LA CARNE", ka, 44, seed=803, fuente="snap")
                kh = pop(t, self.t_hoyos - 0.1, 0.4)
                if kh > 0:
                    lz.forma(elipse(1300, 900, 250 * kh, 76 * kh), (54, 36, 28), NEGRO, 8, seed=804)
                    cal = pop(t, self.t_calien - 0.1, 0.3)
                    for i in range(6):
                        lz.forma(blob(1180 + 48 * i, 892 + 14 * (i % 2), 28 * kh, seed=810 + i), (lerp(150, 232, cal), lerp(146, 96, cal), lerp(150, 60, cal)), NEGRO, 5, seed=820 + i)
                    D.humo(lz, 1300, 800, t, seed=830, n=5, col=(210, 210, 220))
                    chip(lz, 1250, 640, "HOYOS CON PIEDRAS CALIENTES", kh, 38, seed=831)

    def hoy(self, lz, t):
        f4 = e_in(prog(t, self.t_compartir - 0.4, self.t_compartir + 0.1))
        with lz.grupo(-2400 * f4, 0):
            xs = (240, 500, 740, 1180, 1420, 1680)
            D.fuego(lz, 960, 940, 1.0 * pop(t, self.C + 0.05, 0.4), t, seed=840)
            for i, x in enumerate(xs):
                k = pop(t, self.C + 0.15 + 0.1 * i, 0.4)
                if k > 0:
                    D.personaje(lz, x, 950, (0.5 if i % 3 == 1 else 0.62) * k, t, "cave", seed=845 + i, mano_i=(-110, -150), mano_d=(120, -170 - 30 * math.sin(t * 4 + i)), boca=0.8,
                                mirar=(1 if x < 960 else -1, 0.1))
            lz.texto("LA CAZA FUE BUENA", 960, 240, 88, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.t_buena, 0.4), rot=-0.03, seed=852)
            for i, x in enumerate(xs):
                kk = pop(t, self.t_comp + 0.1 * i, 0.35)
                if kk > 0:
                    u = e_inout(prog(t, self.t_comp + 0.1 * i, self.t_comp + 0.9 + 0.1 * i))
                    D.hueso(lz, lerp(960, x, u), lerp(760, 560, u) - 120 * math.sin(math.pi * u), 0.34 * kk, 0.6 + 3 * (1 - u), seed=855 + i, marcas=2)
            chip(lz, 960, 380, "TODO PARA TODOS", pop(t, self.t_todos, 0.3), 46, seed=860, fuente="snap")
        if t >= self.t_compartir - 0.4:
            k = pop(t, self.t_compartir, 0.45)
            if k > 0:
                lat = 1 + 0.06 * math.sin(t * 7)
                dibujar_icono(lz, "corazon", 420, 720, 1.4 * k * lat, t)
                D.hueso(lz, 420, 720, 0.56 * k, 0.5, seed=861, marcas=3)
                lz.texto("COMPARTIR", 520, 270, 90, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=k, rot=-0.03, seed=862)
                lz.texto("= SOBREVIVIR", 1300, 270, 90, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=pop(t, self.t_sob, 0.4), rot=0.03, seed=863)
                kg = pop(t, self.t_compartir + 0.3, 0.45)
                if kg > 0:
                    D.fuego(lz, 1320, 960, 0.9 * kg, t, seed=871)
                    for j, sx in enumerate((-1, 1)):
                        D.personaje(lz, 1320 + sx * 290, 960, 0.6 * kg, t, "cave", seed=872 + j, mano_i=(-110, -150), mano_d=(110, -150 - 30 * math.sin(t * 4 + j)), boca=0.6, mirar=(-sx, 0.1))
                    D.hueso(lz, 1320 + 150 * math.sin(t * 2.2), 640 - 50 * abs(math.cos(t * 2.2)), 0.3 * kg, t * 2, seed=874, marcas=2)
                ki = pop(t, self.t_inv - 0.1, 0.45)
                if ki > 0:
                    for i in range(6):
                        D.copo(lz, 900 + 170 * i, 480 + 300 * ((t * 0.35 + i * 0.23) % 1.0), 0.6 * ki, t + i, seed=865 + i)
                    chip(lz, 1320, 430, "INVIERNO", ki, 50, seed=870, fuente="snap")


# ============================================================ 7. NOCHE
class Noche(Item):
    def fondo_antes(self, t):
        return fondo_estilo("libre", t, "cosmos", env_bombo(t))

    def fondo_hoy(self, t):
        return fondo_estilo("libre", t, "cosmos", env_bombo(t))

    def escena(self):
        self.t_alr = self.w("alrededor", frase=1)
        self.t_mejor = self.w("mejor", frase=1)
        self.t_hist = self.w("historias", frase=1)
        self.t_chau = self.w("chauvet", frase=2)
        self.t_fran = self.w("francia", frase=2)
        self.t_leo = self.w("leones", frase=2)
        self.t_cab = self.w("caballos", frase=2)
        self.t_rino = self.w("rinocerontes", frase=2)
        self.t_carb = self.w("carbon", frase=2)
        self.t_antor = self.w("antorcha", frase=2)
        self.t_alem = self.w("alemania", frase=3)
        self.t_talo = self.w("tallo", frase=3)
        self.t_marf = self.w("marfil", frase=3)
        self.t_cabl = self.w("cabeza", frase=3)
        self.t_rusia = self.w("rusia", frase=4)
        self.t_ninos = self.w("ninos", frase=4)
        self.t_cuen = self.w("cuentas", frase=4)
        self.t_ropa = self.w("ropa", frase=4)
        self.t_brutos = self.w("brutos", frase=5)
        self.t_art = self.w("artistas", frase=5)
        self.t_tarde = self.w("tarde", frase=5)
        self.ev(self.t_hist, "hmm", 0.4)
        self.ev(self.t_chau, "eco", 0.5)
        for k, tt in enumerate((self.t_leo, self.t_cab, self.t_rino)):
            self.ev(tt, "spray", 0.5, pan=-0.4 + 0.4 * k, dur=0.6)
        self.ev(self.t_antor, "fuego", 0.4, dur=2.0)
        self.ev(self.t_talo, "clink", 0.5)
        self.ev(self.t_marf, "bling", 0.5)
        self.ev(self.t_cuen, "pop", 0.5)
        self.ev(self.t_brutos, "error", 0.5)
        self.ev(self.t_art, "bling", 0.7)
        self.ev(self.t_tarde, "suspiro", 0.4)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "estrella", x + 380 * math.cos(a), y + 150 * math.sin(a), 0.3 * s, t)

    def antes(self, lz, t):
        f2 = e_in(prog(t, self.t_chau - 0.35, self.t_chau + 0.15))
        f3 = e_in(prog(t, self.t_alem - 0.35, self.t_alem + 0.15))
        fb = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        estrellas_cielo(lz, t, 26, seed=900)
        with lz.grupo(-2400 * fb, 0):
            with lz.grupo(-2400 * f2, 0):
                # alrededor del fuego, las historias
                D.fuego(lz, 960, 930, 0.9 * pop(t, self.t_alr - 0.1, 0.45), t, seed=901)
                for i, x in enumerate((230, 480, 720, 1200, 1440, 1690)):
                    k = pop(t, self.t_alr + 0.12 * i, 0.4)
                    if k > 0:
                        D.personaje(lz, x, 955, (0.52 if i % 3 == 1 else 0.66) * k, t, "cave", seed=905 + i, mano_i=(-110, -150), mano_d=(120, -170 - 60 * (i == 2) * math.sin(t * 4)),
                                    boca=0.6 if i == 2 else 0.2, mirar=(1 if x < 960 else -1, 0.0), cejas=0.3)
                kh = pop(t, self.t_hist - 0.2, 0.45)
                if kh > 0:
                    D.etiqueta(lz, 760, 460 + 6 * math.sin(t * 2), "HABÍA UNA VEZ UN MAMUT...", 44, rot=-0.02, seed=912, k=kh)
                    dibujar_icono(lz, "mamut", 1320, 470 + 10 * math.sin(t * 2), 0.5 * kh, t)
                chip(lz, 960, 330, "LO MEJOR DEL DÍA", pop(t, self.t_mejor, 0.3), 56, seed=913, fuente="snap")
            with lz.grupo(-2400 * f3, 0):
                # cueva de Chauvet: pinturas con carbón a la luz de una antorcha
                if t >= self.t_chau - 0.4:
                    cueva_roca(lz, 140, 410, 1780, 930, seed=920)
                    chip(lz, 560, 340, "CUEVA DE CHAUVET · FRANCIA", pop(t, self.t_chau, 0.3), 40, seed=921, fuente="snap")
                    for i, (tt, tipo, x, txt) in enumerate(((self.t_leo, "leon", 340, "LEONES"), (self.t_cab, "caballo", 680, "CABALLOS"), (self.t_rino, "rino", 1020, "RINOCERONTES"))):
                        u = prog(t, tt, tt + 0.9)
                        if u > 0:
                            with lz.recorte(rect_red(x - 170, 430, 340, 440, 10)):
                                animal(lz, x, 800, 0.85, tipo, t, seed=930 + 10 * i, paso=0.0)
                                lz.relleno(rect_red(x - 190, 430 + 440 * u, 380, 500, 0), (92, 70, 62), seed=940 + i)
                            chip(lz, x, 870, txt, pop(t, tt + 0.5, 0.3), 30, seed=942 + i)
                    # el pintor, dentro de la cueva desde el principio
                    kpi = pop(t, self.t_chau + 0.2, 0.4)
                    if kpi > 0:
                        D.personaje(lz, 1330, 905, 0.58 * kpi, t, "cave", seed=957, mano_i=(-150, -260 + 50 * math.sin(t * 5)), mano_d=(100, -150), boca=0.3, cejas=0.4, mirar=(-1, -0.2),
                                    obj_i=lambda lz, hx, hy: lz.trazo([(hx, hy), (hx - 34, hy - 26)], (30, 26, 26), 12, seed=958))
                    D.estarcido(lz, 1510, 830, 0.42,prog(t, self.t_carb, self.t_carb + 0.8), color=(196, 84, 52), rot=0.0, capa=1)
                    chip(lz, 1330, 500, "CON CARBÓN", pop(t, self.t_carb, 0.3), 36, seed=948)
                    kt = pop(t, self.t_antor - 0.1, 0.4)
                    if kt > 0:
                        lz.trazo([(1730, 900), (1710, 740)], NEGRO, 22, seed=949)
                        lz.trazo([(1730, 900), (1710, 740)], (120, 84, 56), 12, seed=945)
                        D.fuego(lz, 1710, 750, 0.45 * kt, t, seed=946)
                        lz.halo(1710, 680, 420, (255, 190, 90), alfa=0.3)
                        chip(lz, 1600, 990, "ANTORCHA", kt, 36, seed=947)
            if t >= self.t_alem - 0.4:
                # hombre con cabeza de león, tallado en marfil
                kl = pop(t, self.t_alem + 0.3, 0.5)
                if kl > 0:
                    D.hombre_leon(lz, 960, 1010, 0.9 * kl, math.cos(0.5 * math.sin(t * 1.5)), seed=950)
                    D.destellos(lz, [(800, 560), (1120, 640), (1080, 440)], t, 1.0, seed=952)
                    chip(lz, 440, 640, "TALLADO EN MARFIL", pop(t, self.t_marf, 0.3), 42, seed=953, fuente="snap", rot=-0.04)
                    dibujar_icono(lz, "mamut", 440, 820 + 8 * math.sin(t * 2), 0.5 * pop(t, self.t_marf + 0.15, 0.3), t)
                    chip(lz, 1500, 520, "CABEZA DE LEÓN", pop(t, self.t_cabl, 0.3), 42, seed=954, fuente="snap", rot=0.04)
                    flecha(lz, (1230, 560), (1100, 520), prog(t, self.t_cabl, self.t_cabl + 0.4), seed=955)
                    lz.texto("~40.000 AÑOS", 1500, 760, 76, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=pop(t, self.t_cabl + 0.5, 0.4), rot=0.03, seed=956)
                chip(lz, 960, 330, "ALEMANIA · HOMBRE-LEÓN", pop(t, self.t_alem, 0.3), 42, seed=951, fuente="snap")

    def hoy(self, lz, t):
        f5 = e_in(prog(t, self.t_brutos - 0.35, self.t_brutos + 0.15))
        estrellas_cielo(lz, t, 26, seed=960)
        with lz.grupo(-2400 * f5, 0):
            # dos niños con miles de cuentas de marfil
            chip(lz, 960, 240, "RUSIA · SUNGIR", pop(t, self.t_rusia, 0.3), 54, seed=961, fuente="snap")
            for i, (x, sc) in enumerate(((560, 0.95), (1360, 0.8))):
                k = pop(t, self.t_ninos + 0.2 * i, 0.45)
                if k > 0:
                    s = sc * 0.9
                    D.personaje(lz, x, 960, s * k, t, "cave", seed=965 + i, mano_i=(-110, -150), mano_d=(110, -150), boca=0.2, mirar=(1 if i == 0 else -1, 0))
                    for j in range(40):
                        if pop(t, self.t_cuen + 0.03 * j, 0.3) > 0:
                            a = j * 6.2832 / 10
                            lz.forma(circulo(x + 92 * s * math.cos(a) * (0.6 + 0.1 * (j // 10)), 960 - 205 * s + 30 * s * (j // 10) + 12 * s * math.sin(a), 7), (250, 244, 224), NEGRO, 3, seed=1970 + j + 50 * i)
            chip(lz, 560, 400, "DOS NIÑOS", pop(t, self.t_ninos, 0.3), 42, seed=975, fuente="snap")
            chip(lz, 1360, 400, "MILES DE CUENTAS DE MARFIL", pop(t, self.t_cuen, 0.3), 34, seed=976)
            kc = pop(t, self.t_ropa, 0.4)
            if kc > 0:
                D.collar(lz, 960, 620, 1.0 * kc, 99, seed=980, t=t)
                chip(lz, 960, 760, "COSIDAS A SU ROPA", kc, 36, seed=981)
        if t >= self.t_brutos - 0.4:
            kb = pop(t, self.t_brutos, 0.4)
            if kb > 0:
                chip(lz, 420, 520, "¿BRUTOS?", kb, 70, seed=985, fuente="snap", rot=-0.04)
                D.tache(lz, 420, 520, 1.0 * kb, prog(t, self.t_brutos + 0.5, self.t_brutos + 0.85), seed=986)
            ka = pop(t, self.t_art, 0.45)
            if ka > 0:
                lz.texto("ARTISTAS", 1240, 520, 150, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, k=ka, rot=0.04, seed=987)
                for i in range(4):
                    D.destellos(lz, [(900 + 230 * i, 350 + 30 * (i % 2))], t, 1.3, seed=990 + i)
            km = pop(t, self.t_tarde - 0.2, 0.4)
            if km > 0:
                D.dia_noche(lz, 760, 860, 0.8 * km, t, seed=995)
                D.personaje(lz, 1180, 1000, 0.5 * km, t, "cave", seed=996, mano_i=(-110, -150), mano_d=(120, -260 + 30 * math.sin(t * 4)), boca=0.8, mirar=(-1, -0.3))


# ============================================================ CIERRE
class Cierre(OutroGenerico):
    def preparar(self):
        OutroGenerico.preparar(self)
        self.f1, self.f2 = self.fr[1]["t0"], self.fr[2]["t0"]
        self.t_duro = self.w("duro")
        self.t_frio = self.w("frio")
        self.t_como = self.w("comodidades")
        self.t_ellos = self.w("ellos")
        self.t_fuego = self.w("fuego")
        self.t_music = self.w("musica")
        self.t_arte = self.w("arte")
        self.t_fam = self.w("familia")
        self.t_tel = self.w("telefono")
        self.t_wifi = self.w("wifi")
        self.t_hist = self.w("historias")
        self.t_hab = self.w("habrias")
        self.ev(self.t_duro, "golpe_suave", 0.6)
        for k, tt in enumerate((self.t_fuego, self.t_music, self.t_arte, self.t_fam)):
            self.ev(tt, "pop", 0.5, pan=-0.6 + 0.4 * k, tono=1.0 + 0.1 * k)
        self.ev(self.t_tel, "bling", 0.5)
        self.ev(self.t_wifi, "bling", 0.5, tono=1.3)
        self.ev(self.t_hist, "brillo", 0.6)

    def dibujar(self, lz, t):
        if t >= self.fin:
            for i, lin in enumerate(partir_lineas(self.d.get("cierre", "¿HABRÍAS SOBREVIVIDO?"), 14)):
                lz.texto(lin, 960, 380 + i * 150, 120, "snap", color=AMARILLO if i == 0 else BLANCO, borde=NEGRO, borde_px=12, k=pop(t, self.fin + 0.15 * i, 0.4), rot=-0.03, seed=150 + i)
            return
        fuera = e_in(prog(t, self.fin - 0.1, self.fin + 0.2))
        with lz.grupo(0, 0, 1.0):
            # 1) un día duro, pero con fuego, música, arte y familia
            if t < self.f1 + 0.2:
                sale_ = e_in(prog(t, self.f1 - 0.25, self.f1 + 0.15))
                with lz.grupo(-2400 * sale_, 0):
                    lz.texto("UN DÍA DURO", 960, 240, 100, "snap", color=AMARILLO, borde=NEGRO, borde_px=12, k=pop(t, self.t_duro, 0.4), rot=-0.03, seed=1000)
                    # frío y sin comodidades (hasta que llega el fuego)
                    kd = pop(t, self.t_duro, 0.4) * sale(t, self.t_fuego - 0.35)
                    if kd > 0:
                        D.personaje(lz, 960 + 6 * math.sin(t * 28), 990, 0.8 * kd, t, "cave", seed=1020, mano_i=(-70, -190), mano_d=(70, -190), boca=-0.5, cejas=0.7, mirar=(0, 0.2))
                        for i in range(6):
                            D.copo(lz, 260 + 280 * i, 420 + 420 * ((t * 0.3 + i * 0.37) % 1.0), 0.55 * kd, t + i, seed=1021 + i)
                        chip(lz, 480, 560, "FRÍO", pop(t, self.t_frio, 0.3) * kd, 60, seed=1028, fuente="snap", rot=-0.05)
                        chip(lz, 1480, 560, "SIN COMODIDADES", pop(t, self.t_como, 0.3) * kd, 44, seed=1029, fuente="snap", rot=0.04)
                    for i, (tt, ic, txt) in enumerate(((self.t_fuego, "fuego", "FUEGO"), (self.t_music, "flauta", "MÚSICA"), (self.t_arte, "hombre_leon", "ARTE"), (self.t_fam, "corazon", "FAMILIA"))):
                        k = pop(t, tt, 0.4)
                        if k > 0:
                            x = 330 + 420 * i
                            y = 640 + 10 * math.sin(t * 2 + i)
                            if ic == "flauta":
                                D.flauta(lz, x, y, 0.72 * k, -0.3, seed=1005, agujeros_on=(0, 1, 2))
                                D.nota(lz, x + 110, y - 150, 0.8 * k, color=color_arcoiris(0.2), seed=1006)
                            else:
                                dibujar_icono(lz, ic, x, y, 0.75 * k, t)
                            chip(lz, x, 880, txt, k, 46, seed=1001 + i, fuente="snap")
            # 2) tú tienes teléfono y wifi; ellos, las mismas ganas de contar historias
            if self.f1 - 0.3 <= t < self.f2 + 0.2:
                sale_ = e_in(prog(t, self.f2 - 0.25, self.f2 + 0.15))
                with lz.grupo(0, -900 * sale_):
                    k1 = pop(t, self.t_tel - 0.1, 0.4)
                    if k1 > 0:
                        dibujar_icono(lz, "telefono", 480, 620, 0.9 * k1, t)
                        dibujar_icono(lz, "wifi", 720, 480, 0.9 * k1, t)
                        chip(lz, 600, 860, "TÚ", k1, 52, seed=1010, fuente="snap")
                    ke = pop(t, self.t_ellos - 0.1, 0.4)
                    if ke > 0:
                        D.personaje(lz, 1400, 940, 0.75 * ke, t, "cave", seed=1011, mano_i=(-130, -200), mano_d=(130, -200 - 30 * math.sin(t * 4)), boca=0.7, mirar=(-1, 0))
                        D.fuego(lz, 1680, 940, 0.5 * ke, t, seed=1012)
                        chip(lz, 1400, 400, "ELLOS", ke, 52, seed=1013, fuente="snap")
                    k2 = pop(t, self.t_hist - 0.2, 0.4)
                    if k2 > 0:
                        lz.texto("=", 990, 600, 200, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, k=k2, seed=1014)
                        chip(lz, 990, 250, "GANAS DE CONTAR HISTORIAS", k2, 50, seed=1015, fuente="snap")
            # 3) ¿habrías sobrevivido?
            if t >= self.f2 - 0.3:
                k = pop(t, self.t_hab - 0.3, 0.45) * (1 - fuera)
                if k > 0:
                    dibujar_icono(lz, "cavernicola", 960, 600, 1.4 * k, t)
                    lz.texto("¿?", 1260, 420, 240, "snap", color=AMARILLO, borde=NEGRO, borde_px=16, k=k, rot=0.05, seed=1016)


PROPIAS = dict(intro=Intro, amanecer=Amanecer, desayuno=Desayuno, caza=Caza, mediodia=Mediodia, tarde=Tarde,
               atardecer=Atardecer, noche=Noche, cierre=Cierre)
CLASES = clases_automaticas(PROPIAS)
