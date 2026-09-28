# -*- coding: utf-8 -*-
"""Escenas de "7 inventos antiguos que usas todos los días" — estilo recortes de papel.
Recortes que entran deslizándose (stop-motion a 15 fps lo pone el estilo), cámara suave,
cada aparición anclada a la palabra que la nombra."""
from escena_base import *  # noqa: F401,F403

ICONOS_VIDEO = ["pan", "espejo_obsidiana", "rueda_madera", "tablilla", "drenaje", "tablilla_numeros", "moneda_leon"]


def entra(t, t0, desde, hasta, dur=0.45):
    """Posición de un recorte que se desliza desde 'desde' hasta 'hasta' (con leve rebote)."""
    u = e_back(prog(t, t0, t0 + dur), 1.2)
    return lerp(desde, hasta, u)


def giro_papel(t, seed=0):
    """Pequeño bamboleo de recorte sostenido a mano."""
    return 0.04 * math.sin(t * 1.7 + seed) + 0.02 * math.sin(t * 3.1 + seed * 2)


def espejo_moderno(lz, x, y, s, seed=700):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-150, -210, 300, 420, 30), (220, 180, 90), NEGRO, OW, seed)
        lz.forma(rect_red(-125, -185, 250, 370, 20), (200, 228, 245), NEGRO, 5, seed + 1)
        lz.trazo([(-80, -120), (-20, -180)], BLANCO, 12, seed=seed + 2)
        lz.trazo([(-80, -60), (30, -170)], BLANCO, 7, seed=seed + 3)


def pantalla_pago(lz, t, t0):
    lz.relleno(rect_red(-95, -185, 190, 370, 20), (40, 170, 110), seed=720, temblor=0.3)
    for k in range(3):
        r = 30 + 26 * k + 10 * ((t * 2) % 1)
        lz.trazo(arco(0, -60, r, -math.pi * 0.8, -math.pi * 0.2, 14), BLANCO, 6, seed=721 + k)
    kk = pop(t, t0, 0.3)
    if kk > 0:
        lz.forma(circulo(0, 60, 50 * kk, 30), BLANCO, NEGRO, 5, seed=725)
        palomita(lz, 0, 60, 1.6 * kk, 1.0, seed=726)
        lz.texto("PAGADO", 0, 145, 30, "snap", color=BLANCO, borde=NEGRO, borde_px=3, k=kk, seed=727, temblor=0.2)


def pantalla_chat(lz, t, t0):
    lz.relleno(rect_red(-95, -185, 190, 370, 20), (236, 229, 221), seed=730, temblor=0.3)
    n = int(clamp01((t - t0) / 1.6) * 6)
    for k in range(n):
        der = k % 2 == 1
        yy = -170 + k * 58
        w = 120 - 20 * (k % 3)
        x0 = 85 - w if der else -85
        lz.relleno(rect_red(x0, yy, w, 44, 14), (190, 240, 170) if der else BLANCO, seed=731 + k, temblor=0.3)
        lz.trazo([(x0 + 12, yy + 22), (x0 + w - 16, yy + 22)], (140, 140, 150), 5, seed=740 + k)


# ============================================================ INTRO
class Intro(Escena):
    PAL = "chicle"

    def preparar(self):
        self.t_fut = self.w("futuro")
        self.t_inv = self.w("inventos")
        self.t_pir = self.w("piramides")
        self.t_viejos = self.w("viejos")
        self.t_siete = self.w("siete")
        self.t_todos = self.w("todos")
        self.f1, self.f2 = self.fr[1]["t0"], self.fr[2]["t0"]
        self.ev(0.2, "pop", 0.6)
        self.ev(self.t_fut, "brillo", 0.6)
        for k in range(7):
            self.ev(self.t_inv + 0.1 * k, "pop", 0.45, pan=-0.6 + 0.2 * k, tono=0.9 + 0.08 * k)
        self.ev(self.f1 - 0.2, "whoosh", 0.5, dur=0.4)
        self.ev(self.t_pir, "golpe_suave", 0.8)
        self.ev(self.t_pir + 0.6, "boing", 0.5)
        self.ev(self.t_siete, "impacto", 0.9)

    def fondo(self, t):
        if t < self.f1 - 0.2:
            return fondo_estilo("titulo", t, "chicle", env_bombo(t))
        if t < self.f2 - 0.2:
            return mezcla_fondos(t, self.f1 - 0.2, lambda tt: fondo_estilo("titulo", tt, "chicle"),
                                 lambda tt: F.cartulina(tt, "fuego"))
        return mezcla_fondos(t, self.f2 - 0.2, lambda tt: F.cartulina(tt, "fuego"),
                             lambda tt: fondo_estilo("titulo", tt, "lima", env_bombo(tt)))

    def camara(self, t):
        return 1.0 + 0.03 * math.sin(t * 0.8), 0.01 * math.sin(t * 0.6), 0.0, 0.0

    def dibujar(self, lz, t):
        # 1) el "futuro": tú con el celular... rodeado de inventos antiguos
        if t < self.f1 + 0.2:
            fuera = e_in(prog(t, self.f1 - 0.25, self.f1 + 0.15))
            x = entra(t, 0.1, -400, 520) - 1300 * fuera
            D.personaje(lz, x, 900, 1.0, t, "tu", seed=12, mano_d=(160, -330), mirar=(0.6, -0.2),
                        boca=0.3 if t > self.t_inv else 0.0, obj_d=lambda lz, hx, hy: D.telefono(lz, hx + 20, hy - 70, 0.35, 0.2, seed=13))
            kf = pop(t, self.t_fut, 0.3) * (1 - fuera)
            if kf > 0:
                lz.texto("¿FUTURO?", 520, 250, 100, "snap", color=CIAN, borde=NEGRO, borde_px=11, k=kf, rot=-0.05, seed=14)
            for i, ic in enumerate(ICONOS_VIDEO):
                ki = pop(t, self.t_inv + 0.1 * i, 0.3) * (1 - fuera)
                if ki > 0:
                    gx, gy = 960 + 250 * (i % 4), 470 + 250 * (i // 4)
                    dibujar_icono(lz, ic, gx + (125 if i >= 4 else 0), gy + 10 * math.sin(t * 2 + i), 0.5 * ki, t)
        # 2) más viejos que las pirámides
        if self.f1 - 0.3 <= t < self.f2 + 0.2:
            fuera = e_in(prog(t, self.f2 - 0.25, self.f2 + 0.15))
            y = entra(t, self.f1 - 0.1, 1400, 860) + 1200 * fuera
            D.piramides(lz, 1100, y, 1.4, seed=20)
            chip(lz, 1250, y - 470, "PIRÁMIDES: ~4.500 AÑOS", pop(t, self.t_pir + 0.2, 0.3) * (1 - fuera), 42, seed=21)
            for i, ic in enumerate(("pan", "espejo_obsidiana", "rueda_madera", "tablilla")):
                tk = self.t_viejos + 0.15 * i
                k = pop(t, tk, 0.35) * (1 - fuera)
                if k > 0:
                    salto = 40 * abs(math.sin((t - tk) * 5)) * math.exp(-(t - tk) * 1.5)
                    dibujar_icono(lz, ic, 170 + 150 * i, 520 - salto, 0.34 * k, t)
            kk = pop(t, self.t_pir + 1.2, 0.3) * (1 - fuera)
            if kk > 0:
                lz.texto("¡MÁS VIEJOS!", 400, 330, 80, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=kk, rot=-0.06, seed=22)
        # 3) siete inventos
        if t >= self.f2 - 0.3:
            k7 = pop(t, self.t_siete, 0.4)
            if k7 > 0:
                lz.texto("7", 960, 400, 320, "snap", color=(255, 140, 70), borde=NEGRO, borde_px=16,
                         k=k7 * (1 + 0.04 * env_bombo(t)), rot=-0.05 + giro_papel(t), seed=30)
                lz.texto("INVENTOS ANTIGUOS", 960, 610, 90, "snap", color=BLANCO, borde=NEGRO, borde_px=10,
                         k=pop(t, self.t_siete + 0.25, 0.35), seed=31)
            kt = pop(t, self.t_todos, 0.35)
            if kt > 0:
                lz.texto("QUE USAS TODOS LOS DÍAS", 960, 720, 60, "snap", color=AMARILLO, borde=NEGRO, borde_px=8, k=kt, seed=32)
                for i, ic in enumerate(ICONOS_VIDEO):
                    dibujar_icono(lz, ic, 250 + 237 * i, 850 + 10 * math.sin(t * 3 + i), 0.32 * pop(t, self.t_todos + 0.07 * i, 0.3), t)


# ============================================================ 1. PAN
class Pan(Item):
    PAL = "fuego"

    def escena(self):
        self.t_jor = self.w("jordania")
        self.t_pan = self.w("pan", frase=1)
        self.t_cat = self.w("catorce")
        self.t_caz = self.w("cazadores")
        self.t_agr = self.w("agricultura")
        self.t_cer = self.w("cereales")
        self.t_jun = self.w("junco")
        self.t_mol = self.w("molidos")
        self.t_tos = self.w("tostada")
        self.t_har = self.w("harina")
        self.t_agu = self.w("agua", frase=4)
        self.t_fue = self.w("fuego")
        self.ev(self.t_jor, "pin", 0.5, pan=-0.4)
        self.ev(self.t_pan, "golpe_suave", 0.7)
        self.ev(self.t_caz, "fuego", 0.35, dur=2.2)
        self.ev(self.t_agr, "error", 0.4, pan=0.5)
        self.ev(self.t_cer, "pop", 0.5, pan=0.5)
        self.ev(self.t_jun, "pop", 0.5, pan=0.5, tono=1.15)
        self.ev(self.t_mol, "arena", 0.5, dur=1.0)
        self.ev(self.t_tos, "boing", 0.6)
        for k, tt in enumerate((self.t_har, self.t_agu, self.t_fue)):
            self.ev(tt, "pop", 0.5, pan=-0.5 + 0.5 * k, tono=1 + 0.12 * k)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "pan", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.3 * s, t)

    def antes(self, lz, t):
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        chip(lz, 420, 330, "JORDANIA · SHUBAYQA 1", pop(t, self.t_jor, 0.3) * sale(t, self.t_caz - 0.1), 40, seed=40)
        # el pan quemado aparece, luego el cazador recolector lo cocina sobre piedra
        mover = e_inout(prog(t, self.t_caz - 0.1, self.t_caz + 0.5))
        kp = pop(t, self.B + 0.35, 0.4)
        if kp > 0:
            px, py = lerp(960, 1250, mover), lerp(560, 640, mover)
            if mover > 0:
                with lz.capa(1):
                    lz.forma(blob(px, py + 60, 200, seed=41, irr=0.1) * [1, 0.35] + [0, (py + 60) * 0.65], (130, 125, 120), NEGRO, OW, seed=41)
                D.fuego(lz, px, py + 150, 0.75 * mover, t, seed=42)
            D.pan_plano(lz, px, py + giro_papel(t) * 50, 1.3 * kp * (1 - 0.3 * mover), seed=43, quemado=1.6)
            chip(lz, 1480, 430, "¡14.400 AÑOS!", pop(t, self.t_cat, 0.3) * sale(t, self.t_agr - 0.1), 44, seed=44)
        kc = e_out(prog(t, self.t_caz - 0.1, self.t_caz + 0.45))
        if kc > 0:
            moler = self.t_mol - 0.1 <= t < self.C
            mano = (230 + 40 * math.sin(t * 9), -60) if moler else (200, -250)
            D.personaje(lz, lerp(-300, 520, kc) - 1300 * fuera, 900, 0.95, t, "cave", seed=45, mano_d=mano,
                        mirar=(1, 0.5 if moler else 0.3), boca=0.2)
            chip(lz, 520 - 1300 * fuera, 330, "CAZADORES RECOLECTORES", kc, 40, seed=46)
        km = pop(t, self.t_mol - 0.1, 0.3) * (1 - fuera)
        if km > 0:   # piedra de moler: losa + mano de piedra que va y viene
            with lz.grupo(760 + 40 * math.sin(t * 9) * (t < self.C), 880, km):
                lz.forma(elipse(-30, 10, 150, 34), (140, 135, 125), NEGRO, OW, seed=34)
                lz.forma(elipse(0, -22, 55, 26), (170, 165, 150), NEGRO, 5, seed=35)
            with lz.capa(2):
                rng = np.random.default_rng(int(t * 15))
                lz.puntos(np.stack([rng.uniform(640, 880, 12), rng.uniform(850, 900, 12)], 1), 3, (235, 225, 200))
        ka = pop(t, self.t_agr, 0.3) * sale(t, self.t_cer - 0.1)
        if ka > 0:
            D.trigo(lz, 1560, 330, 0.7 * ka, seed=47)
            D.tache(lz, 1560, 270, 0.5 * ka, prog(t, self.t_agr + 0.1, self.t_agr + 0.45), seed=48)
            chip(lz, 1560, 460, "AÚN NO EXISTÍA", ka, 36, seed=49)
        for i, (tt, txt) in enumerate(((self.t_cer, "CEREALES SILVESTRES"), (self.t_jun, "TUBÉRCULOS DE JUNCO"))):
            kk = pop(t, tt, 0.3) * (1 - fuera)
            if kk > 0:
                chip(lz, 1500, 330 + 110 * i, txt, kk, 40, seed=36 + i)

    def hoy(self, lz, t):
        k = pop(t, self.C + 0.15, 0.4)
        if k > 0:
            D.tostada(lz, 1080, 580 + 10 * math.sin(t * 2), 1.3 * k, seed=50)
            D.personaje(lz, lerp(-300, 470, e_out(prog(t, self.C + 0.15, self.C + 0.6))), 900, 0.9, t, "tu", seed=56,
                        mano_d=(260, -330), mirar=(1, 0), boca=0.35 * (0.5 + 0.5 * math.sin(t * 8)))
        for i, (tt, txt, x) in enumerate(((self.t_har, "HARINA", 460), (self.t_agu, "AGUA", 960), (self.t_fue, "FUEGO", 1460))):
            kk = pop(t, tt, 0.3)
            if kk > 0:
                lz.texto(txt, x, 300, 80, "snap", color=(255, 180, 90) if i == 2 else BLANCO, borde=NEGRO, borde_px=9,
                         k=kk, rot=-0.05 + 0.05 * i, seed=51 + i)
                if i < 2:
                    lz.texto("+", x + 250, 300, 80, "snap", color=AMARILLO, borde=NEGRO, borde_px=8, k=kk, seed=55 + i)


# ============================================================ 2. ESPEJO
class Espejo(Item):
    PAL = "cosmos"

    def escena(self):
        self.t_ana = self.w("anatolia")
        self.t_obs = self.w("obsidiana")
        self.t_vid = self.w("vidrio")
        self.t_ref = self.w("reflejaba")
        self.t_tum = self.w("tumbas")
        self.t_esp = self.w("espejo", frase=3)
        self.t_cel = self.w("celular")
        self.ev(self.t_ana, "pin", 0.5, pan=-0.4)
        self.ev(self.t_obs, "revelar", 0.6)
        self.ev(self.t_ref, "brillo", 0.6)
        self.ev(self.t_tum, "campana", 0.35)
        self.ev(self.t_esp, "brillo", 0.5, tono=1.2)
        self.ev(self.t_cel, "obturador", 0.8)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "espejo_obsidiana", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.28 * s, t)

    def antes(self, lz, t):
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        chip(lz, 420, 330, "ANATOLIA · ÇATALHÖYÜK", pop(t, self.t_ana, 0.3) * (1 - fuera), 40, seed=60)
        k = pop(t, self.B + 0.35, 0.45)
        if k > 0:
            ref = t >= self.t_ref
            x = 960 - 1300 * fuera
            D.espejo_obsidiana(lz, x, 560, 1.4 * k, t, seed=61, reflejo=ref)
            if ref:
                with lz.grupo(x + 25, 590, 0.5 * pop(t, self.t_ref, 0.4)):
                    lz.forma(circulo(0, 0, 110, 30), (80, 70, 95), (120, 110, 140), 5, seed=62)
                    for lado in (-1, 1):
                        lz.forma(elipse(lado * 38, -10, 20, 24), (130, 125, 150), None, 0, seed=63 + lado)
                    lz.trazo(catmull([(-30, 45), (0, 60), (30, 45)], 6), (130, 125, 150), 6, seed=66)
            chip(lz, 1470, 430, "OBSIDIANA = VIDRIO VOLCÁNICO", pop(t, self.t_vid, 0.3) * (1 - fuera), 38, seed=67)
        kt = pop(t, self.t_tum, 0.4) * (1 - fuera)
        if kt > 0:
            lz.forma(rect_red(1240, 700, 460, 110, 30), (150, 140, 130), NEGRO, OW, seed=68)
            D.flor(lz, 1330, 690, 0.45 * kt, (240, 150, 190), seed=69, t=t)
            D.espejo_obsidiana(lz, 1560, 700, 0.35 * kt, t, seed=70)
            chip(lz, 1470, 890, "EN TUMBAS, JUNTO A SUS DUEÑOS", kt, 34, seed=71)

    def hoy(self, lz, t):
        ke = pop(t, self.C + 0.15, 0.4)
        if ke > 0:
            espejo_moderno(lz, 1300, 520, 1.15 * ke)
            with lz.grupo(1300, 520, 0.5 * ke):
                lz.forma(circulo(0, -10, 110, 30), D.PIEL, NEGRO, OW, seed=80)
                for lado in (-1, 1):
                    lz.forma(elipse(lado * 36, -20, 22, 27), BLANCO, NEGRO, 4, seed=81 + lado)
                    lz.relleno(circulo(lado * 36 - 6, -18, 10, 12), NEGRO, seed=83 + lado)
                lz.trazo(catmull([(-30, 40), (0, 58), (30, 40)], 6), NEGRO, 6, seed=85)
            D.personaje(lz, 560, 900, 0.95, t, "tu", seed=86, mirar=(1, -0.2), boca=0.2,
                        mano_d=(170, -300) if t >= self.t_cel else (125, -175),
                        obj_d=(lambda lz, hx, hy: D.telefono(lz, hx + 10, hy - 60, 0.38, 0.3, t=t, seed=87,
                                                             pantalla=lambda lz: D.ui_camara(lz, t, 88))) if t >= self.t_cel else None)
            fl = campana(t, self.t_cel + 0.05, self.t_cel + 0.25)
            if fl > 0:
                with lz.capa(2):
                    lz.forma(estrella(560 + 180, 900 - 390, 120 * fl, 35 * fl, 8, t), (255, 255, 230), None, 0, seed=89)


# ============================================================ 3. RUEDA
class Rueda(Item):
    PAL = "lima"

    def escena(self):
        self.t_rue = self.w("rueda", frase=1)
        self.t_pant = self.w("pantanos")
        self.t_esl = self.w("eslovenia")
        self.t_cin = self.w("cinco")
        self.t_car = self.w("carretas")
        self.t_bue = self.w("bueyes")
        self.usos = [(self.w("auto"), "auto"), (self.w("bicicleta"), "bici"), (self.w("maleta"), "maleta"),
                     (self.w("silla"), "silla")]
        self.ev(self.t_rue - 0.2, "pasos", 0.3, dur=0.8)
        self.ev(self.t_rue + 0.5, "golpe_suave", 0.7)
        self.ev(self.t_esl, "pin", 0.5, pan=0.4)
        self.ev(self.t_car - 0.2, "pasos", 0.45, dur=1.6)
        self.ev(self.t_bue, "hmm", 0.4)
        for k, (tt, _) in enumerate(self.usos):
            self.ev(tt, "boing", 0.45, pan=-0.6 + 0.4 * k, tono=1 + 0.1 * k)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "rueda_madera", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.28 * s, t)

    def antes(self, lz, t):
        # pantano: agua y juncos
        kp = pop(t, self.t_pant, 0.4)
        hunde = 420 * e_in(prog(t, self.C - 0.1, self.C + 0.5))
        with lz.capa(0):
            if kp > 0 and hunde < 400:
                D.olas(lz, 820 + 200 * (1 - kp) + hunde, t, amp=8, col=(70, 120, 110), seed=90, capas=2)
                for k in range(9):
                    jx = 150 + k * 210 + 30 * math.sin(k)
                    lz.trazo([(jx, 830 + hunde), (jx + 15 * math.sin(t + k), 640 - 40 * (k % 3) + hunde)], (60, 110, 50), 9, seed=91 + k)
        # la rueda llega rodando y se queda; en fase B se va a la izquierda
        mover = e_inout(prog(t, self.C - 0.1, self.C + 0.4))
        u = e_out(prog(t, self.t_rue - 0.3, self.t_rue + 0.6))
        if u > 0:
            x = lerp(-250, 960, u)
            x = lerp(x, 330, mover)
            s = lerp(1.25, 0.7, mover)
            rot = (x + 250) / 170
            D.rueda_madera(lz, x, lerp(560, 520, mover), s, rot, seed=95)
        if mover < 1:
            chip(lz, 1470, 330, "PANTANOS DE LIUBLIANA · ESLOVENIA", pop(t, self.t_esl, 0.3) * (1 - mover), 36, seed=96)
            chip(lz, 450, 330, "+5.000 AÑOS", pop(t, self.t_cin, 0.3) * (1 - mover), 46, seed=97, fuente="snap")
            chip(lz, 1470, 440, "2 TABLONES + EJE CUADRADO", pop(t, self.t_esl + 0.8, 0.3) * sale(t, self.t_car - 0.1), 34, seed=98)
            chip(lz, 1470, 440, "CARRETAS TIRADAS POR BUEYES", pop(t, self.t_bue, 0.3) * (1 - mover), 34, seed=99)
        # la carreta cruza por abajo mientras se habla de ella
        uc = prog(t, self.t_car - 0.2, self.C + 0.6)
        if 0 < uc < 1:
            D.carreta(lz, lerp(-700, 2300, uc), 905, 0.62, t, seed=94)

    ANTES_PERSISTE = True

    def hoy(self, lz, t):
        for i, (tt, ic) in enumerate(self.usos):
            k = pop(t, tt, 0.35)
            if k > 0:
                x = 760 + 300 * i
                dibujar_icono(lz, ic, x, 560 + 12 * math.sin(t * 3 + i), 0.5 * k, t)
                chip(lz, x, 760, ic.upper().replace("BICI", "BICICLETA"), k, 34, seed=100 + i)
        kf = prog(t, self.C + 0.1, self.C + 0.5)
        if kf > 0:
            flecha(lz, (430, 400), (620, 450), kf, color=AMARILLO, ancho=12, seed=105, curva=-0.2)


# ============================================================ 4. ESCRITURA
class Escritura(Item):
    PAL = "ocre"

    def escena(self):
        self.t_tex = self.w("textos")
        self.t_uru = self.w("uruk")
        self.t_cin = self.w("cinco")
        self.t_jun = self.w("junco")
        self.t_cun = self.w("cuneiforme")
        self.t_poe = self.w("poemas")
        self.t_ceb = self.w("cebada")
        self.t_cer = self.w("cerveza")
        self.t_rec = self.w("recibos")
        self.t_men = self.w("mensajes")
        self.ev(self.t_tex, "golpe_suave", 0.6)
        self.ev(self.t_tex + 0.3, "pincel", 0.35, dur=2.0)
        self.ev(self.t_jun, "pincel", 0.35, dur=self.t_cun - self.t_jun)
        self.ev(self.t_cun, "sello", 0.5, tono=1.4)
        self.ev(self.t_uru, "pin", 0.5, pan=-0.4)
        self.ev(self.t_poe, "error", 0.4)
        self.ev(self.t_ceb, "pop", 0.5, pan=0.3)
        self.ev(self.t_cer, "pop", 0.5, pan=0.5, tono=1.2)
        self.ev(self.t_rec, "sello", 0.9)
        self.ev(self.C + 0.3, "whoosh", 0.4, dur=0.3)
        for k in range(6):
            self.ev(self.t_men + 0.1 + 0.27 * k, "pop", 0.35, pan=0.2 * (-1) ** k, tono=1.3)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "tablilla", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.26 * s, t)

    def antes(self, lz, t):
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        k = pop(t, self.B + 0.35, 0.45)
        if k <= 0:
            return
        # las marcas se van tallando hasta que se dice "cuneiforme"
        marcas = int(clamp01((t - self.t_tex) / max(1.0, self.t_cun - self.t_tex)) * 40)
        x = 960 - 1400 * fuera
        D.tablilla(lz, x, 580, 1.25 * k, marcas=marcas, seed=110, rot=giro_papel(t, 2))
        if 0 < marcas < 40:
            ox = 30 * math.sin(t * 7)
            with lz.grupo(x + 150 + ox, 450, 1.0, -0.6):
                lz.trazo([(0, 0), (160, -160)], (170, 140, 90), 14, seed=111, afinar=False)
        chip(lz, 420, 330, "URUK · MESOPOTAMIA", pop(t, self.t_uru, 0.3) * (1 - fuera), 40, seed=112)
        chip(lz, 1500, 330, "~5.200 AÑOS", pop(t, self.t_cin, 0.3) * (1 - fuera), 44, seed=113, fuente="snap")
        kj = pop(t, self.t_jun, 0.3) * sale(t, self.t_poe - 0.15)
        if kj > 0:
            chip(lz, 420, 450, "JUNCO + ARCILLA HÚMEDA", kj, 38, seed=122)
        kq = pop(t, self.t_cun, 0.3) * sale(t, self.t_poe - 0.15)
        if kq > 0:
            D.cuna(lz, 1480, 470, 6.0 * kq, seed=123, vertical=True)
            chip(lz, 1480, 700, "CUNEIFORME = EN FORMA DE CUÑA", kq, 36, seed=124)
        kp = pop(t, self.t_poe, 0.3) * sale(t, self.t_ceb - 0.1, 0.25)
        if kp > 0:
            lz.texto("¿POEMAS?", 1450, 520, 80, "snap", color=(255, 150, 190), borde=NEGRO, borde_px=9, k=kp, rot=0.06, seed=114)
            D.tache(lz, 1450, 520, 0.9 * kp, prog(t, self.t_poe + 0.3, self.t_poe + 0.6), seed=115)
        kc = pop(t, self.t_ceb, 0.35) * (1 - fuera)
        if kc > 0:
            D.trigo(lz, 1400, 560, 0.8 * kc, seed=116)
            chip(lz, 1400, 760, "CEBADA", kc, 36, seed=117)
        kv = pop(t, self.t_cer, 0.35) * (1 - fuera)
        if kv > 0:
            D.vasija(lz, 1650, 600, 0.9 * kv, seed=118)
            chip(lz, 1650, 760, "CERVEZA", kv, 36, seed=119)
        kr = pop(t, self.t_rec, 0.25) * (1 - fuera)
        if kr > 0:
            with lz.grupo(x, 560, 1.0 + 0.6 * (1 - kr), -0.25):
                lz.trazo(rect_red(-190, -60, 380, 120, 16), (210, 40, 40), 12, cerrado=True, seed=120)
                lz.texto("RECIBO", 0, 4, 90, "snap", color=(210, 40, 40), borde=None, seed=121)

    def hoy(self, lz, t):
        k = pop(t, self.C + 0.2, 0.4)
        if k > 0:
            D.telefono(lz, 960, 560, 1.15 * k, giro_papel(t, 4), t=t, seed=130, pantalla=lambda lz: pantalla_chat(lz, t, self.t_men))
            D.tablilla(lz, 420, 580, 0.6 * k, seed=110, rot=-0.1)
            lz.texto("=", 690, 560, 150, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=k, seed=131)
            n = int(clamp01((t - self.t_men) / 1.6) * 50)
            if n > 0:
                lz.texto(f"+{n} MENSAJES", 1470, 360, 64, "snap", color=CIAN, borde=NEGRO, borde_px=8, k=pop(t, self.t_men, 0.3),
                         rot=-0.04, seed=132)


# ============================================================ 5. BAÑO
class Bano(Item):
    PAL = "oceano"

    def escena(self):
        self.t_moh = self.w("mohenjo")
        self.t_ind = self.w("indo")
        self.t_ban = self.w("bano", frase=1)
        self.t_dre = self.w("drenajes")
        self.t_tap = self.w("tapas")
        self.t_lim = self.w("limpiarlos")
        self.t_ban2 = self.w("bano", frase=3)
        self.t_cua = self.w("cuarenta")
        self.ev(self.t_moh, "pin", 0.5, pan=-0.4)
        self.ev(self.t_dre, "ola", 0.4, dur=1.2)
        self.ev(self.t_tap, "golpe_suave", 0.6)
        self.ev(self.t_lim, "puf", 0.4)
        self.ev(self.t_ban2, "chapuzon", 0.6, tono=0.8)
        self.ev(self.t_cua, "ding", 0.5)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "inodoro", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.25 * s, t)

    ANTES_PERSISTE = True

    def antes(self, lz, t):
        mover = e_inout(prog(t, self.C - 0.1, self.C + 0.4))
        k = pop(t, self.B + 0.35, 0.45)
        if k > 0:
            D.drenaje(lz, lerp(1040, 520, mover), lerp(560, 580, mover), lerp(1.55, 0.95, mover) * k, t, seed=140)
        chip(lz, 460, 330, "MOHENJO-DARO", pop(t, self.t_moh, 0.3) * (1 - mover), 44, seed=141, fuente="snap")
        chip(lz, 1450, 330, "VALLE DEL INDO · PAKISTÁN", pop(t, self.t_ind, 0.3) * (1 - mover), 38, seed=142)
        kd = pop(t, self.t_dre, 0.3) * sale(t, self.t_tap - 0.1)
        if kd > 0:
            chip(lz, 1400, 850, "DRENAJE CUBIERTO BAJO LA CALLE", kd, 36, seed=143)
            flecha(lz, (1400, 800), (1300, 740), prog(t, self.t_dre, self.t_dre + 0.3), color=AMARILLO, ancho=10, seed=144)
        # tapa del drenaje que se levanta (sobre el canal cubierto del dibujo)
        kt = pop(t, self.t_tap - 0.05, 0.3) * (1 - mover)
        if kt > 0:
            sube = 70 * e_out(prog(t, self.t_tap, self.t_tap + 0.5))
            cx, cy = 1040 + 160 * 1.55, 560 + 80 * 1.55 - 6     # borde superior del canal cubierto (drenaje a escala 1.55)
            with lz.grupo(cx, cy - sube, 1.0, -0.15 * (sube / 70)):
                lz.forma(rect_red(-80, -22, 160, 30, 6), (120, 110, 100), NEGRO, OW, seed=145)
                lz.trazo([(-20, -22), (-20, -40), (20, -40), (20, -22)], (80, 80, 80), 6, seed=146)
            chip(lz, 1400, 850, "TAPAS PARA LIMPIARLOS", kt, 38, seed=147)

    def hoy(self, lz, t):
        k = pop(t, self.t_ban2 - 0.15, 0.4)
        if k > 0:
            D.inodoro(lz, 1380, 600, 1.2 * k, seed=150)
            u = prog(t, self.t_ban2, self.t_ban2 + 1.2)
            if 0 < u < 1:
                with lz.capa(2):
                    lz.trazo(espiral(1380, 480, 5, 90 * (1 - u), 2.5, 60, a0=t * 12), (80, 160, 240), 8, seed=151)
            flecha(lz, (800, 560), (1120, 560), prog(t, self.t_ban2, self.t_ban2 + 0.35), color=AMARILLO, ancho=14, seed=152, curva=0.1)
        kc = pop(t, self.t_cua, 0.35)
        if kc > 0:
            lz.texto("45 SIGLOS", 1380, 250, 96, "snap", color=CIAN, borde=NEGRO, borde_px=10, k=kc, rot=-0.05, seed=153)


# ============================================================ 6. HORAS
class Horas(Item):
    PAL = "ocaso"

    def escena(self):
        self.t_bab = self.w("babilonios")
        self.t_60 = self.w("sesenta", frase=1)
        self.t_min = self.w("minutos", frase=1)
        self.t_seg = self.w("segundos")
        self.t_egi = self.w("egipcios")
        self.t_doc = self.w("doce")
        self.t_24 = self.w("veinticuatro")
        self.t_rel = self.w("reloj")
        self.t_cua = self.w("cuatro", frase=3)
        self.ev(self.t_bab, "pop", 0.5, pan=-0.4)
        self.ev(self.t_60, "impacto", 0.6)
        self.ev(self.t_min, "reloj_rapido", 0.35, dur=1.4)
        self.ev(self.t_egi, "whoosh", 0.4, dur=0.3)
        self.t_partes = [lerp(self.t_doc, self.t_24 - 0.1, i / 23) for i in range(24)]
        for i, tt in enumerate(self.t_partes):
            self.ev(tt, "tick", 0.3, pan=-0.5 + i / 23, tono=1 + i * 0.015)
        self.ev(self.t_24, "ding", 0.7)
        self.ev(self.t_rel, "reloj_rapido", 0.4, dur=1.2)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "reloj", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.26 * s, t)

    def antes(self, lz, t):
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        egip = e_inout(prog(t, self.t_egi - 0.2, self.t_egi + 0.3))
        kb = pop(t, self.t_bab - 0.1, 0.4)
        if kb > 0:
            D.tablilla(lz, lerp(480, -500, egip), 580, 1.0 * kb, numeros=True, seed=160, rot=giro_papel(t, 5))
            chip(lz, lerp(480, -500, egip), 330, "BABILONIA: BASE 60", kb, 40, seed=161)
        k6 = pop(t, self.t_60, 0.35) * (1 - egip) if egip < 0.9 else 0.0
        if k6 > 0:
            lz.texto("60", 1000, 480, 240, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, k=k6, rot=-0.05, seed=162)
        km = pop(t, self.t_min, 0.4) * (1 - egip) if egip < 0.9 else 0.0
        if km > 0:
            D.reloj(lz, 1500, 560, 1.0 * km, t, seed=163, vel=4.0)
            chip(lz, 1500, 820, "60 MIN · 60 SEG", pop(t, self.t_seg, 0.3) * km, 40, seed=164)
        if egip > 0:
            partes = sum(1 for tt in self.t_partes if t >= tt)
            x = lerp(2400, 700, egip) - 1400 * fuera
            D.dia_noche(lz, x, 580, 1.25, t, seed=165, partes_visibles=partes)
            chip(lz, x + 640, 330, "EGIPTO: 12 + 12", pop(t, self.t_egi + 0.2, 0.3) * (1 - fuera), 42, seed=166)
            k24 = pop(t, self.t_24, 0.35) * (1 - fuera)
            if k24 > 0:
                lz.texto("= 24 HORAS", x + 660, 590, 96, "snap", color=CIAN, borde=NEGRO, borde_px=10, k=k24, rot=-0.04, seed=167)

    def hoy(self, lz, t):
        k = pop(t, self.C + 0.15, 0.4)
        if k > 0:
            D.reloj(lz, 960, 560, 1.55 * k, t, seed=170, vel=1.0 + 6 * campana(t, self.t_rel, self.t_rel + 1.2))
        kc = pop(t, self.t_cua, 0.35)
        if kc > 0:
            chip(lz, 1500, 330, "MATEMÁTICA DE ~4.000 AÑOS", kc, 40, seed=171)
            D.tablilla(lz, 430, 600, 0.55 * kc, numeros=True, seed=160, rot=-0.12)


# ============================================================ 7. MONEDAS
class Monedas(Item):
    PAL = "acido"

    def escena(self):
        self.t_tru = self.w("trueque")
        self.t_pes = self.w("pesando")
        self.t_lid = self.w("lidia")
        self.t_mon = self.w("monedas", frase=2)
        self.ev(self.t_tru, "whoosh", 0.4, dur=0.5)
        self.ev(self.t_pes, "clink", 0.5, tono=0.8)
        self.t_ele = self.w("electro")
        self.t_oro = self.w("oro")
        self.t_leo = self.w("leon")
        self.t_cel = self.w("celular")
        self.t_val = self.w("valor")
        self.ev(self.t_lid, "pin", 0.5, pan=-0.4)
        self.ev(self.t_mon, "clink", 0.8)
        self.ev(self.t_mon + 0.35, "clink", 0.6, tono=1.2)
        self.ev(self.t_oro, "bling", 0.6)
        self.ev(self.t_leo, "rugido", 0.5)
        self.ev(self.t_cel, "ding", 0.6, tono=1.4)
        self.ev(self.t_val, "pop", 0.5)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            dibujar_icono(lz, "moneda_leon", x + 340 * math.cos(a), y + 150 * math.sin(a), 0.26 * s, t)

    def camara(self, t):
        u = e_inout(prog(t, self.t_leo - 0.15, self.t_leo + 0.35)) * (1 - e_inout(prog(t, self.C - 0.3, self.C + 0.1)))
        return 1 + 0.45 * u, 0.0, 0.0, 30 * u

    ANTES_PERSISTE = True

    def antes(self, lz, t):
        # antes de las monedas: trueque y trozos de metal pesados en balanza
        fuera = e_in(prog(t, self.t_lid - 0.2, self.t_lid + 0.2))
        if t < self.t_lid + 0.25:
            kt = pop(t, self.B + 0.35, 0.35) * (1 - fuera)
            if kt > 0:
                D.vasija(lz, 360, 600, 0.75 * kt, seed=175)
                D.trigo(lz, 900, 560, 0.75 * kt, seed=176)
                flecha(lz, (470, 470), (790, 470), prog(t, self.t_tru, self.t_tru + 0.3), color=AMARILLO, ancho=12, seed=177, curva=-0.25)
                flecha(lz, (790, 700), (470, 700), prog(t, self.t_tru + 0.15, self.t_tru + 0.45), color=AMARILLO, ancho=12, seed=178, curva=-0.25)
                chip(lz, 630, 330, "TRUEQUE", kt, 46, seed=179, fuente="snap")
            kb = pop(t, self.t_pes - 0.05, 0.35) * (1 - fuera)
            if kb > 0:
                D.balanza(lz, 1430, 860, 1.05 * kb, t, seed=174, inclinacion=0.15 * math.sin((t - self.t_pes) * 3) * math.exp(-(t - self.t_pes)))
                chip(lz, 1430, 330, "METAL A PESO", kb, 46, seed=173, fuente="snap")
        mover = e_inout(prog(t, self.C - 0.1, self.C + 0.4))
        k = pop(t, self.t_lid, 0.45)
        if k > 0:
            vueltas = prog(t, self.t_lid, self.t_lid + 1.3)
            giro = math.cos(vueltas * 4 * math.pi) if vueltas < 1 else 1.0
            giro = giro if abs(giro) > 0.35 else math.copysign(0.35, giro)
            rebote = 1 + 0.12 * campana(t, self.t_mon, self.t_mon + 0.35)
            D.moneda_leon(lz, lerp(960, 380, mover), lerp(560, 560, mover), lerp(1.7, 0.8, mover) * k * rebote, giro, seed=180)
        if mover < 1:
            zoom_fuera = sale(t, self.t_leo - 0.25, 0.2)
            chip(lz, 430, 330, "LIDIA · TURQUÍA", pop(t, self.t_lid, 0.3) * (1 - mover) * zoom_fuera, 42, seed=181)
            chip(lz, 1480, 330, "ORO + PLATA = ELECTRO", pop(t, self.t_oro, 0.3) * (1 - mover) * zoom_fuera, 40, seed=182)
            kl = pop(t, self.t_leo + 0.1, 0.3) * (1 - mover)
            if kl > 0:
                lz.texto("¡LEÓN!", 1300, 760, 90, "snap", color=(255, 190, 70), borde=NEGRO, borde_px=11, k=kl, rot=0.08, seed=183)

    def hoy(self, lz, t):
        k = pop(t, self.t_cel - 0.1, 0.4)
        if k > 0:
            D.telefono(lz, 1360, 560, 1.1 * k, giro_papel(t, 6), t=t, seed=190, pantalla=lambda lz: pantalla_pago(lz, t, self.t_cel + 0.4))
            lz.texto("=", 860, 560, 150, "snap", color=AMARILLO, borde=NEGRO, borde_px=10, k=k, seed=191)
        kv = pop(t, self.t_val, 0.35)
        if kv > 0:
            chip(lz, 960, 850, "UN VALOR QUE TODOS ACEPTAN", kv, 42, seed=192, fuente="snap")


# ============================================================ CIERRE
class Cierre(OutroGenerico):
    PAL = "lima"

    def preparar(self):
        OutroGenerico.preparar(self)
        self.iconos = ICONOS_VIDEO
        self.t_pan = self.w("pan")
        self.t_hora = self.w("hora")
        self.t_gar = self.w("garantia")
        self.ev(self.t_pan, "pop", 0.5, pan=-0.3)
        self.ev(self.t_hora, "pop", 0.5, pan=0.3, tono=1.2)
        self.ev(self.t_gar, "sello", 0.9)

    def dibujar(self, lz, t):
        f1 = self.fr[1]["t0"]
        if t < f1 + 0.1:
            fuera = e_in(prog(t, f1 - 0.25, f1 + 0.1))
            kp = pop(t, self.fr[0]["t0"] + 0.2, 0.35) * (1 - fuera)
            if kp > 0:
                D.tostada(lz, 620, 560, 1.2 * kp, seed=200)
            kh = pop(t, self.t_hora, 0.35) * (1 - fuera)
            if kh > 0:
                D.reloj(lz, 1300, 560, 1.2 * kh, t, seed=201)
            return
        OutroGenerico.dibujar(self, lz, t)
        kg = pop(t, self.t_gar, 0.25)
        if kg > 0 and t < self.fin:
            with lz.grupo(960, 560, 1.0 + 0.5 * (1 - kg), -0.12):
                lz.forma(rect_red(-330, -80, 660, 160, 20), (255, 250, 235), (200, 40, 40), 10, seed=202)
                lz.texto("GARANTÍA", 0, -22, 70, "snap", color=(200, 40, 40), borde=None, seed=203)
                lz.texto("+5.000 AÑOS", 0, 45, 48, "snap", color=(200, 40, 40), borde=None, seed=204)


PROPIAS = dict(intro=Intro, pan=Pan, espejo=Espejo, rueda=Rueda, escritura=Escritura, bano=Bano, horas=Horas,
               monedas=Monedas, cierre=Cierre)
CLASES = clases_automaticas(PROPIAS)
