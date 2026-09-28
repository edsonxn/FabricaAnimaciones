# -*- coding: utf-8 -*-
"""Escenas del video "10 cosas que hacías hace 40.000 años". Coreografía anclada a palabras."""
from escena_base import *  # noqa: F401,F403  (Escena, Item, D, E, F, helpers...)


# ============================================================ INTRO
class Intro(Escena):
    PAL = "arcoiris"

    def preparar(self):
        f0, f1, f2 = self.fr
        self.t_internet = self.w("internet")
        self.t_ciudades = self.w("ciudades")
        self.t_agri = self.w("agricultura")
        self.x_int = self.w("internet", fin=True)
        self.x_ciu = self.w("ciudades", fin=True)
        self.x_agr = self.w("agricultura", fin=True)
        self.t_cer = self.w("cerebros")
        self.t_tuyo = self.w("tuyo")
        self.t_mismo = self.w("mismo")
        self.t_diez = self.w("diez")
        self.t_hielo = self.w("hielo")
        self.t_rep = self.w("repitiendo")
        self.f1, self.f2 = f1["t0"], f2["t0"]
        for k, tt in enumerate((0.15, 0.42, 0.7)):
            self.ev(tt, "impacto" if k == 1 else "pop", 0.8 if k == 1 else 0.6, tono=0.8 + 0.2 * k)
        for tt, xx, pan in ((self.t_internet, self.x_int, -0.5), (self.t_ciudades, self.x_ciu, 0), (self.t_agri, self.x_agr, 0.5)):
            self.ev(tt, "pop", 0.7, pan=pan)
            self.ev(xx, "error", 0.55, pan=pan)
        self.ev(self.f1 - 0.25, "whoosh", 0.6, dur=0.4)
        self.ev(self.t_cer, "brillo", 0.7)
        self.ev(self.t_tuyo, "boing", 0.6, pan=-0.5)
        self.ev(self.t_tuyo + 0.12, "boing", 0.6, pan=0.5, tono=1.2)
        self.ev(self.t_mismo, "ding", 0.6)
        self.ev(self.f2 - 0.2, "whoosh", 0.6, dur=0.4)
        self.ev(self.t_diez, "impacto", 0.9)
        self.ev(self.t_hielo, "brillo", 0.5, tono=1.3)
        self.ev(self.t_rep, "eco", 0.7)
        self.post_fx(self.t_diez + 0.05, self.t_diez + 1.0, lambda img, t, u: E.warhol(img, t, u), 0.08)
        self.post_fx(self.t_rep, self.t1, lambda img, t, u: E.droste(img, 4, 0.58, 0.15, fase=((t - self.t_rep) * 1.2) % 1.0) * u + img * (1 - u), 0.2)
        self.post_fx(0.0, self.fr[0]["t0"], lambda img, t, u: E.ojo_pez(img, 0.35 * u), 0.3)

    def fondo(self, t):
        pul = env_bombo(t)
        if t < self.f1 - 0.2:
            if t < self.fr[0]["t0"]:
                return F.tunel(t, "neon", vel=1.4, pulso=pul)
            return mezcla_fondos(t, self.fr[0]["t0"] - 0.15, lambda tt: F.tunel(tt, "neon", vel=1.4, pulso=pul),
                                 lambda tt: F.cueva(tt, tinte=0.9, pulso=pul))
        if t < self.f2 - 0.2:
            return mezcla_fondos(t, self.f1 - 0.2, lambda tt: F.cueva(tt, tinte=0.9), lambda tt: F.espiral(tt, "acido", pulso=pul))
        if t < self.t_hielo:
            return mezcla_fondos(t, self.f2 - 0.2, lambda tt: F.espiral(tt, "acido"), lambda tt: F.rayos(tt, "arcoiris", pulso=pul))
        return mezcla_fondos(t, self.t_hielo, lambda tt: F.rayos(tt, "arcoiris"), lambda tt: F.anillos(tt, "oceano", pulso=pul))

    def camara(self, t):
        return 1.0 + 0.03 * math.sin(t * 0.9), 0.02 * math.sin(t * 1.3), 0.0, 0.0

    def dibujar(self, lz, t):
        # ---- apertura: HACE / 40.000 / AÑOS
        if t < self.t_internet + 0.2:
            fuera = e_in(prog(t, self.t_internet - 0.25, self.t_internet + 0.2))
            with lz.grupo(0, -330 * fuera, 1 - 0.55 * fuera):
                for k, (txt, y, px, tt, col) in enumerate((("HACE", 300, 110, 0.15, BLANCO), ("40.000", 520, 250, 0.42, AMARILLO),
                                                           ("AÑOS", 740, 110, 0.7, BLANCO))):
                    kk = pop(t, tt, 0.3)
                    if kk > 0:
                        lz.texto(txt, 960, y, px, "snap", color=col if k != 1 else color_arcoiris(t * 0.3),
                                 borde=NEGRO, borde_px=14 if k == 1 else 10, k=kk, rot=0.04 * math.sin(t * 3 + k), seed=k)
        # ---- sin internet, ciudades ni agricultura
        if self.t_internet - 0.1 <= t < self.f1 + 0.1:
            fuera = e_in(prog(t, self.f1 - 0.25, self.f1 + 0.05))
            for k, (tt, xx, x, fn) in enumerate(((self.t_internet, self.x_int, 460, lambda lz, s: D.wifi(lz, 0, 60, 1.4 * s, seed=5)),
                                                 (self.t_ciudades, self.x_ciu, 960, lambda lz, s: D.ciudad(lz, 20, 140, 0.95 * s, seed=6)),
                                                 (self.t_agri, self.x_agr, 1460, lambda lz, s: D.trigo(lz, 0, 130, 1.6 * s, seed=7)))):
                kk = pop(t, tt, 0.3) * (1 - fuera)
                if kk <= 0:
                    continue
                with lz.grupo(x, 520 + 18 * math.sin(t * 2.5 + k), kk, 0.05 * math.sin(t * 2 + k)):
                    fn(lz, 1.0)
                    D.tache(lz, 0, 0, 1.25, prog(t, xx - 0.05, xx + 0.3), seed=40 + k)
        # ---- cerebros como el tuyo
        if self.f1 - 0.2 <= t < self.f2 + 0.1:
            fuera = e_in(prog(t, self.f2 - 0.25, self.f2 + 0.05))
            kb = pop(t, self.t_cer, 0.35) * (1 - fuera)
            if kb > 0:
                subir = e_inout(prog(t, self.t_tuyo - 0.1, self.t_tuyo + 0.4))
                D.cerebro(lz, 960, lerp(520, 400, subir), kb * lerp(1.5, 1.05, subir), t, seed=9,
                          brillo=0.5 + 0.5 * math.sin(t * 6))
            kc = pop(t, self.t_tuyo, 0.35) * (1 - fuera)
            if kc > 0:
                ola = e_out(prog(t, self.t_mismo - 0.05, self.t_mismo + 0.3))
                sube = (-150 - 60 * ola, -300 - 170 * ola + 20 * math.sin(t * 10) * ola)
                D.personaje(lz, lerp(-200, 470, kc), 900, 0.92, t, "cave", seed=11,
                            mano_d=(sube[0] * -1, sube[1]), mirar=(1, -0.2), boca=0.3 * ola)
                D.personaje(lz, lerp(2120, 1450, kc), 900, 0.92, t, "tu", seed=12,
                            mano_i=sube, mirar=(-1, -0.2), boca=0.3 * ola, accesorios=("auriculares",))
                ke = pop(t, self.t_mismo, 0.3)
                if ke > 0:
                    lz.texto("=", 960, 720, 200, "snap", color=AMARILLO, borde=NEGRO, borde_px=12, k=ke * (1 - fuera), seed=13)
        # ---- 10 cosas / Edad de Hielo / repitiendo
        if t >= self.f2 - 0.2:
            k10 = pop(t, self.t_diez, 0.35)
            if k10 > 0:
                lz.texto("10", 960, 370, 330, "snap", color=color_arcoiris(t * 0.4), borde=NEGRO, borde_px=18,
                         k=k10 * (1 + 0.06 * env_bombo(t)), rot=0.06 * math.sin(t * 2), seed=14)
                lz.texto("COSAS", 960, 590, 120, "snap", color=BLANCO, borde=NEGRO, borde_px=11, k=pop(t, self.t_diez + 0.2), seed=15)
            kh = pop(t, self.t_hielo, 0.3)
            if kh > 0:
                lz.texto("EDAD DE HIELO", 960, 715, 70, "print", color=(200, 240, 255), borde=NEGRO, borde_px=9, k=kh, rot=-0.04, seed=16)
                for k in range(14):
                    fx = (h01(k, 1) * 2100 + 60 * math.sin(t + k)) % 2000 - 40
                    fy = ((t - self.t_hielo) * (90 + 60 * h01(k, 2)) + h01(k, 3) * 1100) % 1150 - 60
                    D.copo(lz, fx, fy, 0.6 + 0.6 * h01(k, 4), t * (0.5 + h01(k, 5)), seed=100 + k)
                mx = lerp(2200, -400, prog(t, self.t_hielo, self.t1 + 0.5))
                D.mamut(lz, mx, 880, 0.75, t, seed=17)


# ============================================================ 1. MANOS
class Manos(Item):
    PAL = "fuego"
    SELLO = "HACE ~40.000 AÑOS"
    ANTES_PERSISTE = True

    def escena(self):
        self.t_indo = self.w("indonesia")
        self.t_esp = self.w("espana")
        self.t_alg = self.w("alguien")
        self.t_apoy = self.w("apoyaba")
        self.t_mano = self.w("mano", frase=1)
        self.t_sopl = self.w("soplaba")
        self.t_enc = self.w("encima", fin=True)
        self.t_selfie = self.w("selfie")
        self.t_msj = self.w("mensaje")
        self.t_yo = self.w("yo estuve aqui")
        self.t_aqui = self.w("aqui")
        self.ev(self.t_indo, "pop", 0.6, pan=-0.5)
        self.ev(self.t_esp, "pop", 0.6, pan=0.5, tono=1.2)
        self.ev(self.t_apoy, "whoosh", 0.5, dur=0.3)
        self.ev(self.t_mano, "golpe_suave", 0.8)
        self.ev(self.t_sopl, "spray", 0.75, dur=self.t_enc + 0.35 - self.t_sopl)
        self.ev(self.t_enc + 0.45, "revelar", 0.7)
        self.ev(self.C, "whoosh", 0.6, dur=0.35)
        self.ev(self.t_selfie, "obturador", 1.0)
        self.ev(self.t_selfie + 0.35, "whoosh", 0.4, dur=0.5, tono=1.5)
        for k, word in enumerate(("yo", "estuve", "aqui")):
            self.ev(self.w(word, frase=2), "pop", 0.55, tono=1.0 + 0.15 * k)
        self.post_fx(self.t_sopl + 0.1, self.t_enc, lambda img, t, u: E.ojo_pez(img, 0.28 * u), 0.2)
        self.post_fx(self.t_msj, self.t_yo - 0.1, lambda img, t, u: E.warhol(img, t, u), 0.06)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.6 + k * math.pi
            D.mano(lz, x + 300 * math.cos(a), y + 150 * math.sin(a), 0.42 * s, a, seed=30 + k)

    def fondo_hoy(self, t):
        return F.rejilla(t, pulso=env_bombo(t))

    def camara(self, t):
        if self.B <= t < self.C:
            z = 1.0 + 0.1 * prog(t, self.B, self.C)
            sh = 5 * math.sin(t * 40) * campana(t, self.t_sopl, self.t_enc)
            return z, 0.02 * math.sin(t), sh, 0.0
        if t >= self.C:
            return 1.0 + 0.04 * math.sin(t * 1.2), -0.03, 0.0, 0.0
        return 1.0, 0.0, 0.0, 0.0

    def antes(self, lz, t):
        # al pasar a HOY, la pared con el estarcido se encoge y se vuelve la polaroid
        u = e_inout(prog(t, self.C - 0.1, self.C + 0.35))
        sc = lerp(1.0, 0.34, u)
        tx, ty = lerp(0, 1330 - 930 * sc, u), lerp(0, 500 - 690 * sc, u)
        if u > 0:
            with lz.grupo(1330, 520, 1.0, 0.0):
                with lz.capa(0):
                    lz.forma(rect_red(-200, -230, 400, 460, 8), BLANCO, NEGRO, 6, seed=73)
                    lz.relleno(rect_red(-170, -200, 340, 320, 4), (112, 66, 38), seed=74)
                lz.texto("40.000 a.C.", 0, 170, 40, "print", color=NEGRO, borde=None, seed=75, alfa=u, capa=0)
        with lz.grupo(tx, ty, sc):
            for k, (tt, x, fr, lab) in enumerate(((self.t_indo, 470, [(ROJO, 1), (BLANCO, 1)], "SULAWESI"),
                                                  (self.t_esp, 1450, [((198, 11, 30), 1), ((255, 196, 0), 2), ((198, 11, 30), 1)], "EL CASTILLO"))):
                kk = pop(t, tt, 0.3) * sale(t, self.t_apoy - 0.1, 0.3)
                if kk > 0:
                    D.bandera(lz, x, 470, kk * 1.1, fr, seed=40 + k, t=t)
                    lz.texto(lab, x - 10, 640, 46, "print", color=BLANCO, borde=NEGRO, borde_px=7, k=kk, seed=42 + k)
            sp = prog(t, self.t_sopl, self.t_enc - 0.05)
            D.estarcido(lz, 930, 690, 1.25, sp)
            if 0 < sp < 1:
                rng = np.random.default_rng(int(t * 30))
                n = 60
                uu = rng.random(n)
                px = lerp(1950, 1000, uu) + rng.normal(0, 30, n)
                py = lerp(430, 560, uu) + rng.normal(0, 40, n) * uu
                lz.puntos(np.stack([px, py], 1), rng.uniform(3, 8, n), OCRE, capa=2)
            ent = e_out(prog(t, self.t_apoy, self.t_mano + 0.1))
            ret = e_in(prog(t, self.t_enc - 0.1, self.t_enc + 0.22))
            if ent > 0 and ret < 1:
                sq = 1 - 0.06 * campana(t, self.t_mano, self.t_mano + 0.25)
                D.mano(lz, lerp(1500, 930, ent) + ret * 1100, lerp(1200, 690, ent) + ret * 600, 1.25 * sq,
                       lerp(0.6, 0.0, ent) + 0.5 * ret, seed=50)
            if ret >= 1 and u < 0.5:
                for k in range(6):
                    a = k / 6 * 2 * math.pi + t
                    rr = 330 + 30 * math.sin(t * 5 + k)
                    D.destellos(lz, [(930 + rr * math.cos(a), 560 + rr * 0.7 * math.sin(a))], t, 1.0, seed=60 + k)

    def hoy(self, lz, t):
        ent = e_out(prog(t, self.C, self.C + 0.4))
        x = lerp(-400, 470, ent)
        brazo = (170, -560)
        D.personaje(lz, x, 890, 0.95, t, "tu", seed=12, mano_d=brazo, mano_i=(-140, -330),
                    mirar=(0.6, -0.6), boca=0.25 if t > self.t_selfie else 0.0,
                    accesorios=("gafas",) if t > self.t_msj else ())
        D.telefono(lz, x + brazo[0] * 0.95, 890 + brazo[1] * 0.95 - 60, 0.42, -0.25, t=t, seed=70,
                   pantalla=lambda lz: D.ui_camara(lz, t, 71))
        fl = campana(t, self.t_selfie - 0.02, self.t_selfie + 0.22)
        if fl > 0:
            with lz.capa(2):
                lz.forma(estrella(x + 160, 890 - 590, 170 * fl, 45 * fl, 8, t), (255, 255, 230), None, 0, seed=72)
        ks = pop(t, self.t_selfie + 0.15, 0.3)
        if ks > 0:
            lz.texto("SELFIE ORIGINAL", 1330, 805, 44, "snap", color=AMARILLO, borde=NEGRO, borde_px=7, k=ks, rot=-0.05, seed=76)
        pal = (("YO", self.w("yo", frase=2)), ("ESTUVE", self.w("estuve", frase=2)), ("AQUÍ!", self.t_aqui))
        px = 92
        anchos = [ancho_texto(p, "snap", px) for p, _ in pal]
        esp = 30
        x0 = 1290 - (sum(anchos) + esp * 2) / 2
        for k, ((word, tw), wd) in enumerate(zip(pal, anchos)):
            kk = pop(t, tw, 0.3)
            if kk > 0:
                lz.texto(word, x0 + wd / 2, 215 + 10 * math.sin(t * 4 + k), px, "snap", color=color_arcoiris(t * 0.3 + k * 0.2),
                         borde=NEGRO, borde_px=10, k=kk, rot=-0.04, seed=80 + k)
            x0 += wd + esp
        ka = prog(t, self.t_aqui + 0.1, self.t_aqui + 0.45)
        if ka > 0:
            D.trazo_parcial(lz, catmull([(1640, 275), (1630, 330), (1545, 330)], 8), ka, AMARILLO, 14, seed=85)
            if ka >= 1:
                lz.forma([(1545, 305), (1545, 355), (1505, 330)], AMARILLO, NEGRO, 5, seed=86)


# ============================================================ 2. COMIDA
class Comida(Item):
    PAL = "acido"
    SELLO = "HACE +45.500 AÑOS"
    PX, PY, PS = 1150, 520, 1.1

    def escena(self):
        self.t_pint = self.w("pinturas")
        self.t_sul = self.w("sulawesi")
        self.t_cerdos = self.w("cerdos")
        self.t_despues = self.w("despues")
        self.t_seg = self.w("seguimos")
        self.t_foto = self.w("fotografiando")
        self.t_comer = self.w("comer")
        self.p_ini, self.p_fin = self.t_pint, self.t_cerdos - 0.1
        self.ev(self.t_pint, "pincel", 0.6, dur=self.p_fin - self.t_pint)
        self.ev(self.t_sul, "pop", 0.6, pan=0.4)
        self.ev(self.t_cerdos, "oink", 0.9, pan=0.2)
        self.ev(self.C, "reloj_rapido", 0.6, dur=self.t_seg - self.C)
        self.ev(self.t_foto, "obturador", 0.9)
        for k in range(4):
            self.ev(self.t_comer - 0.5 + k * 0.25, "pop", 0.45, pan=0.3, tono=1.3 + 0.1 * k)
        self.post_fx(self.t_foto, self.t_foto + 0.7, lambda img, t, u: E.ojo_pez(img, 0.3 * u), 0.12)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.4 + k * math.pi
            D.hamburguesa(lz, x + 330 * math.cos(a), y + 160 * math.sin(a), 0.4 * s, seed=30 + k)

    def fondo_hoy(self, t):
        if t < self.t_seg - 0.1:
            return F.espiral(t, "acido", vel=1.2, pulso=env_bombo(t))
        return mezcla_fondos(t, self.t_seg - 0.1, lambda tt: F.espiral(tt, "acido", vel=1.2),
                             lambda tt: F.puntos(tt, "chicle", pulso=env_bombo(tt)))

    def punta_pincel(self, pr):
        """Posición (escenario) de la punta del pincel para un avance de pintura pr."""
        if pr < 0.3125:
            P, f = D.CERDO_CUERPO, pr / 0.3125
        elif pr < 0.5:
            P, f = D.CERDO_CABEZA, (pr - 0.3125) / 0.1875
        else:
            a = pr * 40
            return self.PX + 120 * math.cos(a) * self.PS, self.PY + 50 * math.sin(a * 1.3) * self.PS
        P = np.vstack([P, P[:1]])
        seg = np.hypot(*np.diff(P, axis=0).T)
        d = np.concatenate([[0.0], np.cumsum(seg)])
        L = d[-1] * f
        px, py = np.interp(L, d, P[:, 0]), np.interp(L, d, P[:, 1])
        return self.PX + px * self.PS, self.PY + py * self.PS

    def camara(self, t):
        if self.B <= t < self.C:
            return 1.03, 0.015 * math.sin(t * 0.8), -20 * math.sin(t * 0.6), 0.0
        if self.C <= t < self.t_seg:
            return 1.0 + 0.1 * math.sin((t - self.C) * 3), (t - self.C) * 0.8, 0.0, 0.0
        return 1.0, 0.0, 0.0, 0.0

    def antes(self, lz, t):
        pr = prog(t, self.p_ini, self.p_fin)
        vivo = campana(t, self.t_cerdos, self.t_cerdos + 0.9)
        with lz.grupo(self.PX, self.PY, 1.0, 0.06 * math.sin(t * 25) * vivo):
            D.cerdo_rupestre(lz, 0, 0, self.PS * (1 + 0.08 * vivo), pr)
        tx, ty = self.punta_pincel(pr)
        ent = e_out(prog(t, self.B, self.B + 0.5))
        cx = lerp(-300, 330, ent)
        mano = ((tx - cx) / 0.9, (ty - 890) / 0.9) if 0 < pr < 1 else (140, -250)

        def pincel(lz, hx, hy):
            lz.trazo([(hx, hy), (hx + 30, hy - 70)], D.MARRON, 12, seed=90)
            lz.forma(elipse(hx - 4, hy + 8, 12, 18, 0.4), OCRE, NEGRO, 4, seed=91)
        D.personaje(lz, cx, 890, 0.9, t, "cave", seed=21, mano_d=mano, obj_d=pincel,
                    mirar=(1, -0.4), boca=0.5 * vivo, cejas=vivo)
        chip(lz, 1500, 870, "SULAWESI · INDONESIA", pop(t, self.t_sul, 0.3), 40, seed=92)
        kv = pop(t, self.t_cerdos + 0.05, 0.3) * sale(t, self.C - 0.1, 0.2)
        if kv > 0:
            lz.texto("¡OINK!", 1500, 300, 110, "snap", color=(255, 150, 190), borde=NEGRO, borde_px=11, k=kv, rot=0.12, seed=93)

    def hoy(self, lz, t):
        kt = pop(t, self.C, 0.3) * sale(t, self.t_seg - 0.25, 0.25)
        if kt > 0:
            lz.texto("45.000 AÑOS", 960, 470, 150, "snap", color=AMARILLO, borde=NEGRO, borde_px=13, k=kt,
                     rot=-(t - self.C) * 0.8, seed=94)
            lz.texto("DESPUÉS...", 960, 640, 90, "snap", color=BLANCO, borde=NEGRO, borde_px=10,
                     k=pop(t, self.t_despues, 0.3) * kt, rot=-(t - self.C) * 0.8, seed=95)
        if t < self.t_seg - 0.2:
            return
        ent = e_out(prog(t, self.t_seg - 0.2, self.t_seg + 0.25))
        D.hamburguesa(lz, 1250, lerp(1300, 760, ent), 1.25, seed=96)
        fx = lerp(-300, 560, ent)
        tel = (1030, 380)
        D.personaje(lz, fx, 900, 0.95, t, "tu", seed=22, mano_d=((tel[0] - fx) / 0.95, (tel[1] + 120 - 900) / 0.95),
                    mirar=(1, 0.3), boca=0.3 * (t > self.t_foto))
        D.telefono(lz, tel[0], tel[1], 0.55, 0.3, t=t, seed=97,
                   pantalla=lambda lz: (D.hamburguesa(lz, 0, -20, 0.55, seed=98), D.ui_camara(lz, t, 99)))
        fl = campana(t, self.t_foto - 0.02, self.t_foto + 0.2)
        if fl > 0:
            with lz.capa(2):
                lz.forma(estrella(tel[0] + 30, tel[1] + 60, 150 * fl, 40 * fl, 8, t), (255, 255, 230), None, 0, seed=100)
        for k in range(4):
            tk = self.t_comer - 0.5 + k * 0.25
            u = prog(t, tk, tk + 1.6)
            if 0 < u < 1:
                hx = 1350 + 90 * k + 30 * math.sin(t * 4 + k)
                hy = lerp(560, 260, e_out(u))
                D.corazon_like(lz, hx, hy, 1.6 * pop(t, tk, 0.25), seed=101 + k)
                lz.texto("+1", hx + 60, hy - 40, 44, "snap", color=BLANCO, borde=NEGRO, borde_px=6, k=pop(t, tk, 0.25), seed=110 + k)


# ============================================================ 3. MÚSICA
class Musica(Item):
    PAL = "lima"
    SELLO = "HACE +40.000 AÑOS"

    def escena(self):
        self.t_ale = self.w("alemania")
        self.t_fla = self.w("flautas")
        self.t_hue = self.w("hueso")
        self.t_mar = self.w("marfil")
        self.t_agr = self.w("agricultura")
        self.t_antes = self.w("antes", frase=2)
        self.t_play = self.w("playlist")
        self.ev(self.t_ale, "pop", 0.6, pan=-0.5)
        self.ev(self.t_fla, "whoosh", 0.5, dur=0.35)
        self.ev(self.t_hue, "pop", 0.5, pan=-0.3)
        self.ev(self.t_mar, "pop", 0.5, pan=0.3, tono=1.2)
        self.ev(self.t_antes, "whoosh", 0.4, dur=0.3)
        self.ev(self.t_agr, "pop", 0.6, pan=0.3)
        self.ev(self.t_play, "brillo", 0.7)
        self.post_fx(self.t_fla + 0.3, self.C - 0.2, lambda img, t, u: E.ondular(img, t, 9 * u, 110), 0.3)
        self.post_fx(self.t_play + 0.7, self.t1, lambda img, t, u: E.planeta(img, t * 0.6, u), 0.25)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(3):
            a = t * 1.8 + k * 2.09
            D.nota(lz, x + 320 * math.cos(a), y + 150 * math.sin(a), 0.8 * s, color_arcoiris(k / 3 + t * 0.2), seed=30 + k, doble=k == 1)

    def fondo_antes(self, t):
        return F.caleido(t, "lima", n=8, pulso=env_bombo(t), sat=0.75)

    def fondo_hoy(self, t):
        return F.rejilla(t, pulso=env_bombo(t))

    def antes(self, lz, t):
        kf = pop(t, self.t_ale, 0.3) * sale(t, self.t_fla - 0.1, 0.3)
        if kf > 0:
            D.bandera(lz, 960, 520, 1.6 * kf, [(NEGRO, 1), ((221, 0, 0), 1), ((255, 206, 0), 1)], seed=40, t=t)
            lz.texto("ALEMANIA", 960, 720, 64, "snap", color=BLANCO, borde=NEGRO, borde_px=8, k=kf, seed=41)
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.25))
        for k, (tt, y, col, lab, lx) in enumerate(((self.t_fla, 470, D.MARFIL, "HUESO DE AVE", 520),
                                                   (self.t_mar, 690, (252, 248, 236), "MARFIL DE MAMUT", 1400))):
            ent = e_out(prog(t, tt, tt + 0.45))
            if ent <= 0:
                continue
            beat = int(t / (BEAT / 2))
            on = {(beat + k) % 5, (beat * 3 + k) % 5}
            with lz.grupo(lerp(-800 if k == 0 else 2700, 960, ent) - 1500 * fuera, y + 14 * math.sin(t * 2 + k)):
                D.flauta(lz, 0, 0, 1.55, -0.06 + 0.04 * math.sin(t * 1.5 + k), seed=42 + k * 10, agujeros_on=on)
            kl = pop(t, (self.t_hue if k == 0 else self.t_mar) + 0.1, 0.3) * (1 - fuera)
            chip(lz, lx, y - 115 if k == 0 else y + 110, lab, kl, 42, seed=60 + k)
        if self.t_fla + 0.4 < t < self.C + 0.3:
            for k in range(10):
                u = ((t - self.t_fla) * 0.5 + k / 10) % 1.0
                nx = 1320 + u * 620 + 40 * math.sin(u * 9 + k)
                ny = 470 - u * 380 + 30 * math.cos(u * 7 + k)
                D.nota(lz, nx - 1500 * fuera, ny, 0.7 * (1 - u * 0.3), color_arcoiris(k * 0.13 + t * 0.2),
                       rot=0.3 * math.sin(t * 3 + k), seed=70 + k, doble=k % 3 == 0)
        if self.t_mar + 0.2 < t:
            mx = lerp(2100, -300, prog(t, self.t_mar, self.C + 1.0))
            D.mamut(lz, mx - 1500 * fuera, 930, 0.45, t, seed=80)

    def hoy(self, lz, t):
        kl = e_out(prog(t, self.t_antes - 0.1, self.t_antes + 0.5))
        if kl > 0:
            x0, x1 = 200, 1720
            D.trazo_parcial(lz, [(x0, 360), (x1, 360)], kl, BLANCO, 14, seed=120)
            if kl >= 1:
                lz.forma([(x1 + 30, 360), (x1 - 10, 334), (x1 - 10, 386)], BLANCO, NEGRO, 4, seed=121)
            chip(lz, x0 + 90, 440, "MÚSICA · 40.000", pop(t, self.t_antes, 0.3), 36, seed=122)
            D.nota(lz, x0 + 20, 320, 0.7 * pop(t, self.t_antes, 0.3), MAGENTA, seed=123)
            xa = x0 + (40 - 12) / 40 * (x1 - x0)
            ka = pop(t, self.t_agr, 0.3)
            if ka > 0:
                D.trigo(lz, xa, 300, 0.6 * ka, seed=124)
                chip(lz, xa, 440, "AGRICULTURA · 12.000", ka, 36, seed=125)
            chip(lz, x1 - 20, 440, "HOY", pop(t, self.t_antes + 0.3, 0.3), 36, seed=126)
        ent = e_out(prog(t, self.t_antes, self.t_antes + 0.5))
        if ent > 0:
            fase = (t / BEAT) % 1.0
            salto = 30 * abs(math.sin(math.pi * fase))
            x = lerp(-300, 560, ent)
            brazo = (150, -330 - 100 * abs(math.sin(math.pi * fase)))
            D.personaje(lz, x, 900, 0.9, t, "tu", seed=23, salto=salto, incl=0.1 * math.sin(math.pi * t / BEAT),
                        mano_d=brazo, mano_i=(-160, -300 + 60 * math.sin(math.pi * t / BEAT)), accesorios=("auriculares",),
                        ojos="cerrados" if t > self.t_play else "normal", boca=0.3)
        kp = pop(t, self.t_play - 0.1, 0.35)
        if kp > 0:
            def pantalla(lz):
                lz.relleno(rect_red(-95, -185, 190, 60, 20), (40, 200, 110), seed=130, temblor=0.3)
                lz.texto("PLAYLIST", 0, -155, 30, "snap", color=BLANCO, borde=NEGRO, borde_px=3, seed=131, temblor=0.2)
                for k, (tit, col) in enumerate((("Flauta de hueso", MAGENTA), ("Tambor de cuero", CIAN), ("Canto en cueva", AMARILLO))):
                    yy = -90 + k * 62
                    lz.relleno(rect_red(-85, yy - 22, 44, 44, 8), col, seed=132 + k, temblor=0.2)
                    lz.texto(tit, 20, yy, 17, "semi", color=NEGRO, borde=None, seed=135 + k, temblor=0.2)
                D.ecualizador(lz, -80, 175, 160, 80, t, env_bombo(t), seed=140)
            D.telefono(lz, 1280, 640, 1.05 * kp, 0.08 * math.sin(t * 2), pantalla=pantalla, t=t, seed=141)


# ============================================================ 4. HÉROES
class Heroes(Item):
    PAL = "neon"
    SELLO = "HACE ~40.000 AÑOS"
    ANTES_PERSISTE = True

    def escena(self):
        self.t_hl = self.w("hombre leon")
        self.t_marf = self.w("marfil")
        self.t_cuerpo = self.w("cuerpo")
        self.t_cabeza = self.w("cabeza")
        self.t_leon2 = self.w("leon", frase=1, n=1)
        self.t_imag = self.w("imaginacion")
        self.t_arana = self.w("hombre arana")
        self.t_tata = self.w("tataranieto")
        self.ev(self.t_hl, "aparicion", 0.8)
        self.ev(self.t_marf, "pop", 0.5, pan=-0.5)
        self.ev(self.t_cuerpo, "pop", 0.5, pan=0.5)
        self.ev(self.t_cabeza, "pop", 0.5, pan=0.5, tono=1.2)
        self.ev(self.t_leon2, "rugido", 0.9)
        self.ev(self.t_imag, "brillo", 0.7)
        self.ev(self.t_arana, "comic", 0.9, pan=0.4)
        self.ev(self.t_tata, "ding", 0.6)
        self.post_fx(self.t_arana, self.t_arana + 0.35, lambda img, t, u: E.rgb_split(img, 18 * u, t * 3), 0.05)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.3 + k * math.pi
            lz.forma(estrella(x + 330 * math.cos(a), y + 150 * math.sin(a), 60 * s, 26 * s, 5, rot=t * 2), AMARILLO, NEGRO, 6, seed=30 + k)

    def fondo_antes(self, t):
        return F.espiral(t, "neon", brazos=4, vel=0.25, pulso=env_bombo(t), sat=0.8)

    def fondo_hoy(self, t):
        if t < self.t_arana - 0.1:
            return F.espiral(t, "neon", brazos=4, vel=0.5, pulso=env_bombo(t))
        return mezcla_fondos(t, self.t_arana - 0.1, lambda tt: F.espiral(tt, "neon", brazos=4),
                             lambda tt: F.rayos(tt, "chicle", n=18, pulso=env_bombo(tt)))

    def camara(self, t):
        if self.t_cabeza - 0.1 <= t < self.C + 0.2:
            u = e_inout(prog(t, self.t_cabeza - 0.1, self.t_cabeza + 0.5)) * (1 - e_inout(prog(t, self.C - 0.2, self.C + 0.2)))
            return 1 + 0.9 * u, 0.0, 0.0, 330 * u
        return 1.0 + 0.02 * math.sin(t), 0.0, 0.0, 0.0

    def antes(self, lz, t):
        sube = e_out(prog(t, self.t_hl, self.t_hl + 0.7))
        if sube <= 0:
            return
        fuera = e_inout(prog(t, self.C - 0.15, self.C + 0.35))
        x = lerp(960, 470, fuera)
        s = lerp(1.05, 0.72, fuera)
        y = lerp(1450, 900, sube)
        with lz.capa(0):
            for k in range(16):
                a = k / 16 * 2 * math.pi + t * 0.7
                r0, r1_ = 150 * s, (420 + 40 * math.sin(t * 4 + k)) * s
                cy = y - 300 * s
                lz.trazo([(x + r0 * math.cos(a), cy + r0 * math.sin(a)), (x + r1_ * math.cos(a), cy + r1_ * math.sin(a))],
                         color_arcoiris(k / 16 + t * 0.2), 12, seed=40 + k)
        D.hombre_leon(lz, x, y, s, 0.45 + 0.55 * abs(math.cos((t - self.t_hl) * 1.3)), seed=41)
        if fuera < 0.5:
            chip(lz, 430, 560, "MARFIL · 31 cm", pop(t, self.t_marf, 0.3) * (1 - fuera * 2) * sale(t, self.t_cabeza - 0.2, 0.2), 42, seed=50)
            kc = prog(t, self.t_cuerpo, self.t_cuerpo + 0.35) * (1 - fuera * 2)
            if kc > 0:
                flecha(lz, (1450, 700), (1040, 640), kc * sale(t, self.t_cabeza - 0.2, 0.2), seed=51)
                chip(lz, 1520, 740, "CUERPO HUMANO", pop(t, self.t_cuerpo, 0.3) * sale(t, self.t_cabeza - 0.2, 0.2), 42, seed=52)
            kh = prog(t, self.t_cabeza, self.t_cabeza + 0.35) * (1 - fuera * 2)
            if kh > 0:
                flecha(lz, (1230, 440), (1080, 430), kh, seed=53, curva=-0.2)
                chip(lz, 1260, 370, "CABEZA DE LEÓN", pop(t, self.t_cabeza, 0.3), 36, seed=54)
            kr = pop(t, self.t_leon2, 0.25) * sale(t, self.C - 0.2, 0.2)
            if kr > 0:
                lz.texto("¡GRRR!", 760, 380, 80, "snap", color=(255, 170, 60), borde=NEGRO, borde_px=10, k=kr, rot=-0.15, seed=55)

    def hoy(self, lz, t):
        kb = pop(t, self.t_imag - 0.05, 0.35)
        if kb > 0:
            D.cerebro(lz, 470, 250, 0.55 * kb, t, seed=60, brillo=0.6 + 0.4 * math.sin(t * 6))
            chip(lz, 470, 395, "IMAGINACIÓN", kb, 38, seed=61)
        ka = pop(t, self.t_arana, 0.35)
        if ka > 0:
            with lz.capa(0):
                lz.forma(estrella(1420, 560, 330 * ka, 200 * ka, 14, rot=t * 0.3), AMARILLO, NEGRO, 8, seed=62)
            D.mascara_arana(lz, 1420, 560, 1.25 * ka, seed=63, rot=0.08 * math.sin(t * 3))
            chip(lz, 1420, 800, "HOMBRE ARAÑA", ka, 42, seed=64)
        kt = prog(t, self.t_tata - 0.1, self.t_tata + 0.45)
        if kt > 0:
            arbol = catmull([(620, 560), (800, 360), (1060, 330), (1260, 430)], 10)
            D.trazo_parcial(lz, arbol, kt, BLANCO, 14, seed=65)
            if kt >= 1:
                lz.forma(np.array([(1275, 450), (1235, 440), (1262, 410)]), BLANCO, NEGRO, 4, seed=66)
            lz.texto("TATARANIETO", 1010, 280, 70, "snap", color=MAGENTA, borde=NEGRO, borde_px=9,
                     k=pop(t, self.t_tata, 0.3), rot=-0.05, seed=67)


# ============================================================ 5. JOYAS
class Joyas(Item):
    PAL = "chicle"
    SELLO = "HACE +40.000 AÑOS"

    def escena(self):
        self.t_col = self.w("collares")
        self.t_cas = self.w("cascara")
        self.t_con = self.w("conchas")
        self.t_die = self.w("dientes")
        self.t_perf = self.w("perforados", fin=True)
        self.t_nadie = self.w("nadie")
        self.t_sob = self.w("sobrevivir")
        self.t_quien = self.w("quien")
        self.t_grupo = self.w("grupo")
        self.t_igual = self.w("igual")
        self.t_acc = self.w("accesorios")
        n = 15
        self.t_cuentas = [lerp(self.t_cas, self.t_perf, k / (n - 1)) for k in range(n)]
        for k, tk in enumerate(self.t_cuentas):
            self.ev(tk, "clink", 0.4, pan=-0.6 + 1.2 * k / (n - 1), tono=1.0 + 0.04 * k)
        self.check = [("COMIDA", self.t_nadie + 0.15, True), ("AGUA", self.t_nadie + 0.45, True),
                      ("FUEGO", self.t_nadie + 0.75, True), ("COLLAR", self.t_sob, False)]
        for _, tk, ok in self.check:
            self.ev(tk + 0.15, "ding" if ok else "error", 0.5, pan=0.4)
        self.ev(self.t_quien, "pop", 0.6, pan=-0.4)
        self.ev(self.t_grupo, "boing", 0.6, pan=-0.4)
        self.ev(self.t_igual, "whoosh", 0.4, dur=0.3)
        self.ev(self.t_acc, "bling", 0.9, pan=0.4)
        self.post_fx(self.t_perf + 0.05, self.t_nadie - 0.05, lambda img, t, u: E.caleido(img, 8, t * 0.8, u), 0.15)

    def iconos_titulo(self, lz, t, x, y, s):
        D.destellos(lz, [(x - 300, y - 60), (x + 300, y + 40), (x + 240, y - 150), (x - 250, y + 150)], t, 1.8 * s, seed=30)

    def fondo_antes(self, t):
        return F.ondas(t, "chicle", pulso=env_bombo(t))

    def fondo_hoy(self, t):
        return F.plasma(t, "ocaso", pulso=env_bombo(t))

    def antes(self, lz, t):
        n_vis = sum(1 for tk in self.t_cuentas if t >= tk)
        k = pop(t, self.t_col, 0.35)
        if k <= 0:
            return
        mover = e_inout(prog(t, self.t_nadie - 0.2, self.t_nadie + 0.3))
        with lz.grupo(lerp(960, 560, mover), lerp(430, 470, mover), k * lerp(1.55, 1.0, mover)):
            D.collar(lz, 0, 0, 1.0, n_vis=n_vis, seed=40, t=t)
        if mover < 0.5:
            for kk, (tt, x, lab) in enumerate(((self.t_cas, 420, "CÁSCARA DE AVESTRUZ"), (self.t_con, 960, "CONCHAS"),
                                               (self.t_die, 1500, "DIENTES"))):
                chip(lz, x, 800, lab, pop(t, tt, 0.3) * (1 - mover * 2), 42, seed=50 + kk, rot=-0.03 + 0.03 * kk)
        if mover > 0:
            with lz.grupo(1400, 560, e_back(mover)):
                lz.forma(rect_red(-260, -250, 520, 500, 18), (255, 250, 235), NEGRO, 6, seed=60)
                lz.texto("PARA SOBREVIVIR:", 0, -190, 42, "snap", color=NEGRO, borde=None, seed=61)
                for i, (lab, tk, ok) in enumerate(self.check):
                    kk = pop(t, tk, 0.25)
                    if kk <= 0:
                        continue
                    yy = -90 + i * 95
                    lz.texto(lab, -60, yy, 48, "print", color=NEGRO, borde=None, k=kk, seed=62 + i)
                    if ok:
                        palomita(lz, 170, yy, 1.3, prog(t, tk + 0.1, tk + 0.3), seed=70 + i)
                    else:
                        D.tache(lz, 170, yy, 0.22, prog(t, tk + 0.1, tk + 0.35), seed=74)

    def hoy(self, lz, t):
        ent = e_out(prog(t, self.C, self.C + 0.4))
        gx = lerp(-500, 0, ent)
        D.personaje(lz, gx + 480, 900, 0.85, t, "cave", seed=31, accesorios=("collar",), mirar=(0.5, 0), boca=0.2)
        kq = pop(t, self.t_quien, 0.3) * sale(t, self.t_grupo - 0.05, 0.25)
        if kq > 0:
            lz.forma(elipse(gx + 700, 330, 150, 70), BLANCO, NEGRO, 6, seed=80)
            lz.forma([(gx + 620, 385), (gx + 560, 450), (gx + 660, 395)], BLANCO, NEGRO, 5, seed=81)
            lz.texto("¡SOY YO!", gx + 700, 330, 50, "snap", color=NEGRO, borde=None, k=kq, seed=82)
        kg = pop(t, self.t_grupo, 0.35)
        if kg > 0:
            for i, dx in enumerate((-230, 230)):
                D.personaje(lz, gx + 480 + dx, 930, 0.72 * kg, t, "cave", seed=33 + i, accesorios=("collar",),
                            mirar=(-0.5 if dx > 0 else 0.5, 0))
            lz.texto("MI TRIBU", gx + 480, 300, 70, "snap", color=AMARILLO, borde=NEGRO, borde_px=9, k=kg, rot=-0.04, seed=83)
        ki = pop(t, self.t_igual, 0.3)
        if ki > 0:
            lz.texto("=", 1010, 620, 170, "snap", color=CIAN, borde=NEGRO, borde_px=11, k=ki, seed=84)
            D.personaje(lz, lerp(2300, 1450, e_out(prog(t, self.t_igual, self.t_igual + 0.4))), 900, 0.9, t, "tu", seed=34,
                        accesorios=("cadena", "gafas", "aro") if t >= self.t_acc - 0.05 else ("cadena",),
                        mano_d=(150, -260), mano_i=(-150, -260), boca=0.25)
        kb = pop(t, self.t_acc, 0.3)
        if kb > 0:
            D.destellos(lz, [(1300, 420), (1600, 380), (1560, 700), (1330, 650), (1450, 300)], t, 2.0 * kb, seed=85)
            chip(lz, 1450, 250, "TU TRIBU HOY", kb, 44, seed=86, fondo=(20, 20, 40), color=CIAN, fuente="snap")


# ============================================================ 6. MODA
class Moda(Item):
    PAL = "ocaso"
    SELLO = "HACE ~40.000 AÑOS"

    def escena(self):
        self.t_agu = self.w("agujas")
        self.t_ojo = self.w("ojo")
        self.t_sib = self.w("siberia")
        self.t_arq = self.w("arqueologos")
        self.t_abr = self.w("abrigarse")
        self.t_dec = self.w("decorar")
        self.t_luc = self.w("lucirla")
        self.ev(self.t_agu, "whoosh", 0.6, dur=0.4)
        self.ev(self.t_ojo, "boing", 0.8)
        self.ev(self.t_sib, "viento", 0.6, dur=1.3)
        self.ev(self.t_arq, "pop", 0.5)
        self.ev(self.t_abr, "brr", 0.6, pan=-0.5)
        n = 9
        self.t_punt = [lerp(self.t_dec, self.t_luc - 0.05, k / (n - 1)) for k in range(n)]
        for tk in self.t_punt:
            self.ev(tk, "puntada", 0.45, pan=0.5)
        self.ev(self.t_luc, "flashes", 0.8, dur=1.0)
        self.post_fx(self.t_luc + 0.05, self.t1, lambda img, t, u: E.espejo(img) * u + img * (1 - u), 0.12)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.5 + k * math.pi
            D.aguja(lz, x + 330 * math.cos(a), y + 150 * math.sin(a), 0.5 * s, a, seed=30 + k)

    def fondo_antes(self, t):
        return F.anillos(t, "oceano", vel=0.4, pulso=env_bombo(t))

    def fondo_hoy(self, t):
        if t < self.t_luc - 0.1:
            return F.ondas(t, "ocaso", pulso=env_bombo(t))
        return mezcla_fondos(t, self.t_luc - 0.1, lambda tt: F.ondas(tt, "ocaso"),
                             lambda tt: F.rayos(tt, "chicle", n=20, pulso=env_bombo(tt)))

    def camara(self, t):
        if self.t_ojo - 0.1 <= t < self.C:
            u = e_inout(prog(t, self.t_ojo - 0.1, self.t_ojo + 0.35)) * (1 - e_inout(prog(t, self.t_sib - 0.1, self.t_sib + 0.3)))
            return 1 + 0.8 * u, 0.0, 380 * u, 60 * u
        return 1.0 + 0.02 * math.sin(t * 1.1), 0.01 * math.sin(t * 0.7), 0.0, 0.0

    def antes(self, lz, t):
        ent = e_out(prog(t, self.t_agu, self.t_agu + 0.5))
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        if ent > 0:
            D.aguja(lz, lerp(2400, 960, ent), 560 - 700 * fuera, 2.0, (1 - ent) * 6 + 0.05 * math.sin(t * 2), seed=40)
        ko = pop(t, self.t_ojo, 0.35) * sale(t, self.t_sib - 0.1, 0.3)
        if ko > 0:
            D.ojo_flotante(lz, 660, 470, 0.75 * ko, t, seed=41, mirar=(math.sin(t * 3), 0.3))
        ks = pop(t, self.t_sib, 0.3) * (1 - fuera)
        if ks > 0:
            lz.texto("SIBERIA", 960, 780, 110, "snap", color=(200, 240, 255), borde=NEGRO, borde_px=11, k=ks, rot=-0.03, seed=42)
            for k in range(18):
                fx = (h01(k, 1) * 2100 + 60 * math.sin(t + k)) % 2000 - 40
                fy = ((t - self.t_sib) * (160 + 90 * h01(k, 2)) + h01(k, 3) * 1100) % 1150 - 60
                D.copo(lz, fx, fy, 0.5 + 0.7 * h01(k, 4), t * (0.5 + h01(k, 5)), seed=100 + k)

    def hoy(self, lz, t):
        kl = pop(t, self.t_arq, 0.3) * sale(t, self.t_abr - 0.1, 0.25)
        if kl > 0:
            D.aguja(lz, 960, 520, 1.3, 0.05, seed=50)
            lx = 960 + 300 * math.sin((t - self.t_arq) * 2.2)
            with lz.grupo(lx, 500, kl):
                lz.trazo([(80, 80), (190, 190)], D.MARRON, 30, seed=51, afinar=False)
                lz.forma(circulo(0, 0, 110, 40), (210, 240, 255), NEGRO, 12, seed=52)
            chip(lz, 960, 800, "LOS ARQUEÓLOGOS CREEN...", kl, 44, seed=53)
        ka = pop(t, self.t_abr, 0.3) * sale(t, self.t_luc - 0.1, 0.2)
        if ka > 0:
            tiembla = 6 * math.sin(t * 60)
            D.personaje(lz, 480 + tiembla, 900, 0.85 * ka, t, "cave", seed=54, mano_i=(-60, -230), mano_d=(60, -230),
                        boca=0.15, cejas=0.6)
            chip(lz, 480, 330, "ABRIGARSE", ka, 46, seed=55)
            palomita(lz, 690, 330, 1.4, prog(t, self.t_abr + 0.1, self.t_abr + 0.35), seed=56)
        kd = pop(t, self.t_dec - 0.1, 0.3) * sale(t, self.t_luc - 0.05, 0.2)
        if kd > 0:
            D.cuero(lz, 1400, 600, 0.95 * kd, seed=57)
            n_p = sum(1 for tk in self.t_punt if t >= tk)
            pts = [(1240 + i * 40, 600 + (40 if i % 2 else -40)) for i in range(n_p + 1)]
            if len(pts) >= 2:
                lz.trazo(pts, ROJO, 10, seed=58)
            if n_p < len(self.t_punt):
                ax, ay = pts[-1]
                D.aguja(lz, ax + 60, ay - 40, 0.55, -0.7, seed=59)
            chip(lz, 1400, 330, "DECORAR", kd, 46, seed=60)
        kp = pop(t, self.t_luc, 0.3)
        if kp > 0:
            D.personaje(lz, 640, 910, 0.95 * kp, t, "cave", seed=61, mano_i=(-40, -120), mano_d=(170, -420),
                        accesorios=("collar", "gafas"), incl=0.08 * math.sin(t * 5), boca=0.3)
            for k in range(4):
                tk = self.t_luc + 0.14 * k
                f = campana(t, tk, tk + 0.18)
                if f > 0:
                    with lz.capa(2):
                        lz.forma(estrella(260 + 150 * k, 990, 70 * f, 18 * f, 8), (255, 255, 230), None, 0, seed=63 + k)

    def ui(self, lz, t):
        r = Item.ui(self, lz, t)
        kp = pop(t, self.t_luc, 0.3)
        if kp > 0:
            lz.texto("¡LUCIRLA!", 960, 330, 110, "snap", color=color_arcoiris(t * 0.4), borde=NEGRO, borde_px=12, k=kp, seed=62)
        return r


# ============================================================ 7. CUENTA
class Cuenta(Item):
    PAL = "arcoiris"
    SELLO = "HACE ~43.000 AÑOS"
    ANTES_PERSISTE = True

    def escena(self):
        self.t_hue = self.w("hueso")
        self.t_sur = self.w("sur")
        self.t_29 = self.w("veintinueve")
        self.t_prop = self.w("proposito")
        self.t_nosab = self.w("no sabemos")
        self.t_tu = self.w("tu haces")
        self.t_mismo = self.w("mismo", frase=2)
        self.t_app = self.w("app")
        paso = BEAT / 8
        t_ini = math.ceil(self.t_29 / paso) * paso
        self.t_marcas = [t_ini + k * paso for k in range(29)]
        self.ev(self.t_hue, "whoosh", 0.5, dur=0.4)
        self.ev(self.t_sur, "pop", 0.5, pan=0.4)
        for k, tk in enumerate(self.t_marcas):
            self.ev(tk, "tick", 0.5, pan=-0.6 + 1.2 * k / 28, tono=1.0 + k * 0.02)
        self.ev(self.t_marcas[-1] + 0.08, "ding", 0.7)
        self.ev(self.t_nosab, "hmm", 0.6)
        self.ev(self.t_tu, "pop", 0.5, pan=0.5)
        self.ev(self.t_app, "ding", 0.8, pan=0.3, tono=1.3)
        self.post_fx(self.t_mismo, self.t_mismo + 0.55,
                     lambda img, t, u: E.droste(img, 4, 0.6, 0.1, fase=(t * 2) % 1) * u + img * (1 - u), 0.1)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.2 + k * math.pi
            with lz.grupo(x + 320 * math.cos(a), y + 150 * math.sin(a), 1.6 * s, a):
                D.hueso_mini(lz, seed=30 + k)

    def fondo_antes(self, t):
        return F.liso(t)

    def fondo_hoy(self, t):
        return F.puntos(t, "arcoiris", pulso=env_bombo(t))

    def camara(self, t):
        z = 1.0
        for tk in self.t_marcas:
            if tk <= t < tk + 0.2:
                z += 0.025 * (1 - (t - tk) / 0.2)
        return z, 0.0, 0.0, 0.0

    def antes(self, lz, t):
        ent = e_out(prog(t, self.t_hue, self.t_hue + 0.45))
        if ent <= 0:
            return
        fuera = e_inout(prog(t, self.C - 0.1, self.C + 0.35))
        n = sum(1 for tk in self.t_marcas if t >= tk)
        x, y, s = lerp(960, 520, fuera), lerp(640, 640, fuera), lerp(1.3, 0.75, fuera)
        D.hueso(lz, lerp(-700, x, ent), y, s, 0.0, marcas=n, seed=40)
        if n > 0 and fuera < 1:
            lz.texto(str(n), 960, 420, 170, "snap", color=color_arcoiris(n / 29), borde=NEGRO, borde_px=13,
                     k=(1 + 0.25 * max(0, 1 - (t - self.t_marcas[n - 1]) / 0.12)) * (1 - fuera), seed=41)
        chip(lz, 960, 830, "PERONÉ DE BABUINO · MONTES LEBOMBO", pop(t, self.t_sur, 0.3) * (1 - fuera), 38, seed=42)
        kp = pop(t, self.t_prop, 0.3) * (1 - fuera)
        if kp > 0:
            lz.texto("¡A PROPÓSITO!", 1500, 470, 64, "snap", color=ROJO, borde=NEGRO, borde_px=8, k=kp, rot=0.1, seed=43)

    def hoy(self, lz, t):
        for k, (txt, dx, dy) in enumerate((("¿DÍAS?", -260, -260), ("¿LUNAS?", 250, -300), ("¿ANIMALES?", 0, -420))):
            kk = pop(t, self.t_nosab + 0.15 * k, 0.3) * sale(t, self.t_tu - 0.1, 0.3)
            if kk > 0:
                lz.texto(txt, 520 + dx + 20 * math.sin(t * 3 + k), 600 + dy, 58, "snap", color=color_arcoiris(k * 0.3 + t * 0.2),
                         borde=NEGRO, borde_px=8, k=kk, rot=0.1 * math.sin(t * 2 + k), seed=50 + k)
        kt = pop(t, self.t_tu, 0.35)
        if kt > 0:
            D.personaje(lz, lerp(2200, 1600, e_out(prog(t, self.t_tu, self.t_tu + 0.4))), 900, 0.85, t, "tu", seed=51,
                        mano_i=(-260, -300), mirar=(-1, -0.2), boca=0.2)
            ka = pop(t, self.t_app - 0.15, 0.35)

            def pantalla(lz):
                lz.relleno(rect_red(-95, -185, 190, 370, 20), (30, 26, 50), seed=60, temblor=0.3)
                lz.trazo(D.arco(0, -30, 70, -math.pi / 2, -math.pi / 2 + 2 * math.pi * min(1, max(0.02, (t - self.t_app + 0.2) * 1.5)), 40),
                         VERDE, 14, seed=61)
                lz.texto("29", 0, -30, 70, "snap", color=BLANCO, borde=None, seed=62, temblor=0.2)
                lz.texto("DÍAS", 0, 70, 30, "snap", color=CIAN, borde=None, seed=63, temblor=0.2)
                for i in range(12):
                    cx, cy = -70 + (i % 6) * 28, 120 + (i // 6) * 30
                    lz.relleno(rect_red(cx - 10, cy - 10, 20, 20, 5), VERDE, seed=64 + i, temblor=0.2)
            if ka > 0:
                D.telefono(lz, 1180, 560, 1.0 * ka, -0.08, pantalla=pantalla, t=t, seed=65)


# ============================================================ 8. PESCA
class Pesca(Item):
    PAL = "oceano"
    SELLO = "HACE ~42.000 AÑOS"

    def escena(self):
        self.t_tim = self.w("timor")
        self.t_pes = self.w("pescaban")
        self.t_atu = self.w("atunes")
        self.t_mar = self.w("mar abierto")
        self.t_tec = self.w("tecnica")
        self.t_plan = self.w("planificacion")
        self.t_sushi = self.w("sushi")
        self.t_lejos = self.w("lejos")
        self.salto0, self.salto1 = self.t_pes, self.t_atu + 0.55
        self.ev(self.t_tim, "pop", 0.5, pan=-0.4)
        self.ev(self.salto0, "chapuzon", 0.8, pan=0.4)
        self.ev(self.salto1, "chapuzon", 0.6, pan=-0.2, tono=1.3)
        self.ev(self.t_atu + 0.1, "pop", 0.6)
        self.ev(self.t_mar, "whoosh", 0.6, dur=0.6, tono=0.7)
        self.ev(self.t_tec, "ding", 0.5, pan=-0.3)
        self.ev(self.t_plan, "ding", 0.5, pan=0.3, tono=1.25)
        self.ev(self.t_sushi, "brillo", 0.8)
        self.ev(self.t_lejos, "whoosh", 0.5, dur=0.8, tono=1.4)
        self.post_fx(self.B + 0.3, self.t_pes - 0.1, lambda img, t, u: E.ondular(img, t, 7 * u, 130), 0.3)

    def iconos_titulo(self, lz, t, x, y, s):
        D.atun(lz, x + 330 * math.cos(t * 1.5), y + 140 * math.sin(t * 1.5), 0.45 * s, t, seed=30)

    def fondo_antes(self, t):
        return F.plasma(t, "oceano", vel=0.6, pulso=env_bombo(t), sat=0.8)

    def fondo_hoy(self, t):
        if t < self.t_sushi - 0.2:
            return F.plasma(t, "oceano", vel=0.6, sat=0.8)
        return mezcla_fondos(t, self.t_sushi - 0.2, lambda tt: F.plasma(tt, "oceano", vel=0.6, sat=0.8),
                             lambda tt: F.tunel(tt, "oceano", vel=1.2, pulso=env_bombo(tt)))

    def camara(self, t):
        if self.t_mar - 0.1 <= t < self.t_sushi - 0.2:
            u = e_inout(prog(t, self.t_mar - 0.1, self.t_mar + 0.6))
            return lerp(1.0, 0.45, u), 0.0, 0.0, lerp(0, -60, u)
        return 1.0, 0.0, 0.0, 0.0

    def mar(self, lz, t):
        with lz.capa(0):
            D.olas(lz, 640, t, seed=40, w=3200, x0=-1300, fondo=2600)
        atrapado = t >= self.salto1
        D.canoa(lz, 760, 640, 1.0, t=t, seed=41)
        D.personaje(lz, 760, 640, 0.62, t, "cave", seed=42, mano_d=(160, -260) if not atrapado else (110, -420),
                    mano_i=(-120, -250) if not atrapado else (-110, -420), boca=0.5 if atrapado else 0.0,
                    mirar=(1, 0.5), salto=10 * math.sin(t * 2.2))
        if not atrapado:
            lz.trazo([(760 + 160 * 0.62 + 10, 640 - 260 * 0.62), (1100, 400), (1180, 860)], (240, 240, 240), 3, seed=43)

    def atun_en_escena(self, lz, t):
        u = prog(t, self.salto0, self.salto1)
        if 0 < u < 1:
            x = lerp(1350, 800, u)
            y = 860 - math.sin(math.pi * u) * 620
            D.atun(lz, x, y, 0.9, t, seed=44, rot=-math.pi * (u - 0.5) * 0.9 + math.pi)
        elif u <= 0:
            D.atun(lz, 1300 + 150 * math.sin(t * 0.9), 880, 0.75, t, seed=44, rot=math.pi)
        else:
            D.atun(lz, 780, 520, 0.6, t, seed=44, rot=math.pi + 0.3)

    def antes(self, lz, t):
        if t >= self.C + 0.35:
            return
        self.atun_en_escena(lz, t)
        self.mar(lz, t)
        chip(lz, 420, 330, "TIMOR · JERIMALAI", pop(t, self.t_tim, 0.3) * sale(t, self.C - 0.1, 0.2), 42, seed=45)
        ka = pop(t, self.t_atu + 0.1, 0.3) * sale(t, self.C - 0.1, 0.2)
        if ka > 0:
            lz.texto("¡ATÚN!", 1400, 330, 110, "snap", color=AMARILLO, borde=NEGRO, borde_px=11, k=ka, rot=0.1, seed=46)

    def hoy(self, lz, t):
        if t < self.t_sushi - 0.15:
            if t >= self.C + 0.35:
                self.atun_en_escena(lz, t)
                self.mar(lz, t)
            km = pop(t, self.t_mar + 0.1, 0.3)
            if km > 0:
                z = max(0.45, 1 - 0.55 * e_inout(prog(t, self.t_mar - 0.1, self.t_mar + 0.6)))
                with lz.grupo(960, 540, 1 / z):
                    with lz.grupo(-960, -540):
                        lz.texto("MAR ABIERTO", 960, 250, 110, "snap", color=BLANCO, borde=NEGRO, borde_px=11, k=km, seed=47)
                        for i, (lab, tt) in enumerate((("TÉCNICA", self.t_tec), ("PLANIFICACIÓN", self.t_plan))):
                            kk = pop(t, tt, 0.3)
                            if kk > 0:
                                chip(lz, 600 + 720 * i, 420, lab, kk, 54, seed=48 + i, fuente="snap")
                                palomita(lz, 600 + 720 * i + (215 if i == 0 else 330), 420, 1.6, prog(t, tt + 0.1, tt + 0.35), seed=50 + i)
            return
        u = prog(t, self.t_lejos - 0.1, self.t1 + 0.2)
        k = pop(t, self.t_sushi, 0.35) * lerp(1.0, 0.15, e_in(u))
        D.sushi(lz, 960, 560 - 60 * e_in(u), 1.9 * k, seed=51)
        D.destellos(lz, [(700, 400), (1220, 380), (1260, 700), (660, 720)], t, 2.0 * k, seed=52)
        lz.texto("¡SUSHI!", 960, 250, 120, "snap", color=(255, 130, 120), borde=NEGRO, borde_px=12,
                 k=pop(t, self.t_sushi + 0.05, 0.3) * (1 - e_in(u)), seed=53)
        for i in range(2):
            with lz.grupo(960 + 170 * k, 470 - 40 * i, k, -0.5 + 0.08 * i):
                lz.trazo([(0, 0), (380, -60)], (200, 150, 90), 14, seed=54 + i, afinar=False)


# ============================================================ 9. LIGAR
class Ligar(Item):
    PAL = "chicle"
    SELLO = "HACE ~47.000 AÑOS"

    def escena(self):
        self.t_anc = self.w("ancestros", frase=1)
        self.t_tuv = self.w("tuvieron")
        self.t_hij = self.w("hijos")
        self.t_nea = self.w("neandertales")
        self.t_fuera = self.w("fuera")
        self.t_uno = self.w("uno y dos")
        self.t_nea2 = self.w("neandertal", frase=2)
        self.ev(self.B + 0.15, "pasos", 0.5, dur=1.3)
        self.ev(self.t_tuv, "latido", 0.8)
        self.ev(self.t_hij, "bebe", 0.8)
        self.ev(self.t_nea, "pop", 0.5, pan=0.5)
        self.ev(self.t_fuera, "pop", 0.45, pan=-0.4)
        self.ev(self.t_uno, "ding", 0.6)
        self.ev(self.t_nea2 + 0.15, "match", 0.9)

        def corazon_vineta(img, t, u):
            import cv2
            m = np.zeros((H, W), np.float32)
            pts = corazon(960, 600, 520 + 20 * math.sin(t * 6)).astype(np.int32)
            cv2.fillPoly(m, [pts], 1.0, cv2.LINE_AA)
            m = cv2.GaussianBlur(m, (0, 0), 40)[..., None]
            tinte = np.array([0.55, 0.1, 0.3], np.float32)
            return img * (m + (1 - m) * (1 - 0.6 * u)) + tinte * (1 - m) * 0.35 * u
        self.post_fx(self.t_tuv, self.C - 0.1, corazon_vineta, 0.3)
        self.post_fx(self.C + 0.6, self.t_fuera - 0.1, lambda img, t, u: E.caleido(img, 6, t * 0.5, 0.6 * u), 0.3)

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(3):
            a = t * 1.5 + k * 2.09
            lz.forma(corazon(x + 320 * math.cos(a), y + 150 * math.sin(a), 50 * s), ROJO, NEGRO, 6, seed=30 + k)

    def fondo_antes(self, t):
        return F.plasma(t, "chicle", pulso=env_bombo(t))

    def fondo_hoy(self, t):
        return F.anillos(t, "neon", vel=0.5, pulso=env_bombo(t))

    def antes(self, lz, t):
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.3))
        amor = t >= self.t_tuv
        xs, ps = caminar(t, self.B + 0.15, 1.3, -300, 620)
        xn, pn = caminar(t, self.B + 0.15, 1.3, 2200, 1300)
        oy = 1400 * fuera
        D.personaje(lz, xs, 900 + oy, 0.95, t, "cave", seed=41, paso=ps, mirar=(1, -0.1), ojos="corazon" if amor else "normal",
                    mano_d=(150, -300) if amor else (125, -175), boca=0.2 if amor else 0.0)
        D.personaje(lz, xn, 900 + oy, 0.95, t, "neander", seed=42, paso=pn, mirar=(-1, -0.1), ojos="corazon" if amor else "normal",
                    mano_i=(-150, -300) if amor else (-125, -175), boca=0.2 if amor else 0.0)
        kb = pop(t, self.t_hij, 0.4)
        if kb > 0:
            D.bebe(lz, 960, 820 + oy, 1.3 * kb, t, seed=43)
            for k in range(8):
                u = ((t - self.t_hij) * 0.6 + k / 8) % 1
                lz.forma(corazon(960 + 260 * math.sin(k * 2.3 + u * 3), 700 - u * 500 + oy, 34 * (1 - u) * kb), ROJO, NEGRO, 4, seed=44 + k)
        kl = pop(t, self.t_nea, 0.3) * (1 - fuera)
        chip(lz, 620, 330, "SAPIENS", kl, 46, seed=52)
        chip(lz, 1300, 330, "NEANDERTAL", kl, 46, seed=53)

    def hoy(self, lz, t):
        ent = e_out(prog(t, self.C, self.C + 0.5))
        D.adn(lz, lerp(2800, 960, ent), 560, 1.25, t, largo=1300, marca=(0.5, 0.62), seed=60)
        chip(lz, 420, 350, "FUERA DE ÁFRICA", pop(t, self.t_fuera, 0.3), 42, seed=61)
        ku = pop(t, self.t_uno, 0.35)
        if ku > 0:
            flecha(lz, (1300, 340), (1090, 490), prog(t, self.t_uno, self.t_uno + 0.35), color=(255, 150, 40), seed=62)
            lz.texto("1–2 % NEANDERTAL", 1380, 290, 72, "snap", color=(255, 170, 60), borde=NEGRO, borde_px=9, k=ku, rot=-0.04, seed=63)
        km = pop(t, self.t_nea2 + 0.15, 0.35)
        if km > 0:
            def pantalla(lz):
                lz.relleno(rect_red(-95, -185, 190, 370, 20), (255, 90, 140), seed=70, temblor=0.3)
                lz.texto("¡MATCH!", 0, -120, 40, "snap", color=BLANCO, borde=NEGRO, borde_px=4, seed=71, temblor=0.2)
                lz.forma(circulo(-42, 10, 44, 24), D.PIEL, NEGRO, 5, seed=72)
                lz.forma(circulo(42, 10, 44, 24), D.PIEL_N, NEGRO, 5, seed=73)
                lz.forma(corazon(0, 110, 50), ROJO, NEGRO, 5, seed=74)
            D.telefono(lz, 960, 700, 1.05 * km, 0.06 * math.sin(t * 3), pantalla=pantalla, t=t, seed=75)


# ============================================================ 10. DESPEDIDA (tono sereno)
class Despedida(Item):
    PAL = "cosmos"
    SELLO = "HACE ~40.000 AÑOS"

    def escena(self):
        self.t_mungo = self.w("mungo")
        self.t_aus = self.w("australia")
        self.t_mujer = self.w("mujer")
        self.t_crem = self.w("cremacion")
        self.t_homb = self.w("hombre")
        self.t_ocre = self.w("ocre")
        self.t_honrar = self.w("honrar")
        self.t_humano = self.w("humano")
        self.ev(self.t_mungo, "pin", 0.6)
        self.ev(self.t_mujer, "fuego", 0.45, dur=self.C - self.t_mujer + 0.3)
        self.ev(self.t_crem, "campana", 0.4)
        self.ev(self.t_ocre, "arena", 0.5, dur=1.2)
        self.ev(self.t_honrar, "campana", 0.45, tono=1.5)
        self.ev(self.t_humano, "campana", 0.5, tono=1.26)

    def wob(self, t):
        return 1.3

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 0.8 + k * math.pi
            D.flor(lz, x + 330 * math.cos(a), y + 140 * math.sin(a), 0.5 * s, color_arcoiris(0.85 + 0.1 * k, 0.6), seed=30 + k, t=t)

    def fondo_titulo(self, t):
        return F.rayos(t, "cosmos", n=12, vel=0.02, sat=0.8)

    def fondo_antes(self, t):
        return F.cosmos(t)

    def fondo_hoy(self, t):
        return F.cosmos(t)

    def camara(self, t):
        return 1.0 + 0.04 * prog(t, self.B, self.t1), 0.0, 0.0, 0.0

    def antes(self, lz, t):
        esq = e_inout(prog(t, self.t_mujer - 0.2, self.t_mujer + 0.5))
        fuera = e_in(prog(t, self.C - 0.15, self.C + 0.35))
        km = e_out(prog(t, self.t_mungo - 0.3, self.t_mungo + 0.3))
        if km > 0:
            D.australia(lz, lerp(960, 330, esq), lerp(560, 480, esq) - 900 * fuera, km * lerp(1.25, 0.55, esq),
                        pin=prog(t, self.t_mungo, self.t_mungo + 0.4), t=t, seed=40)
            chip(lz, lerp(1440, 330, esq), lerp(470, 700, esq) - 900 * fuera, "LAGO MUNGO", pop(t, self.t_aus, 0.4), 44, seed=41)
        kf = e_out(prog(t, self.t_mujer, self.t_mujer + 0.8))
        if kf > 0:
            with lz.capa(0):
                D.humo(lz, 1100, 700 - 900 * fuera, t, seed=42)
            D.fuego(lz, 1100, 830 - 900 * fuera, 0.9 * kf, t, seed=43)
        kc = e_out(prog(t, self.t_crem, self.t_crem + 0.7)) * (1 - fuera)
        if kc > 0:
            chip(lz, 1100, 330, "LA CREMACIÓN MÁS ANTIGUA CONOCIDA", kc, 40, seed=44, rot=-0.01)

    def hoy(self, lz, t):
        kh = e_out(prog(t, self.C, self.C + 0.8))
        if kh > 0:
            D.figura_yacente(lz, 960, 620, 1.2 * (0.9 + 0.1 * kh), seed=50, ocre=prog(t, self.t_ocre, self.t_ocre + 1.1), t=t)
            if self.t_ocre <= t < self.t_ocre + 1.3:
                rng = np.random.default_rng(int(t * 20))
                n = 40
                px = rng.uniform(640, 1300, n)
                py = rng.uniform(250, 600, n)
                lz.puntos(np.stack([px, py], 1), rng.uniform(2, 5, n), (190, 40, 28), capa=2)
            chip(lz, 960, 820, "OCRE ROJO", e_out(prog(t, self.t_ocre, self.t_ocre + 0.5)), 42, seed=51)
        kh2 = e_out(prog(t, self.t_honrar, self.t_honrar + 0.8))
        if kh2 > 0:
            for i, (x, col) in enumerate(((420, (240, 120, 180)), (560, AMARILLO), (1360, (160, 140, 250)), (1500, (250, 150, 90)))):
                D.flor(lz, x, lerp(1100, 610, kh2) + 20 * (i % 2), 0.8, col, seed=52 + i, t=t)
            for i, x in enumerate((690, 1230)):
                D.vela(lz, x, lerp(1200, 800, kh2), 0.9, t, seed=60 + i)
        kc = e_out(prog(t, self.t_humano - 0.1, self.t_humano + 1.0))
        if kc > 0:
            pts = corazon(960, 330, 150)[::5]
            with lz.capa(2):
                n = int(len(pts) * kc)
                if n > 1:
                    lz.trazo(pts[:n], (255, 240, 200), 3, seed=70)
                lz.puntos(pts[:max(1, n)], 6, (255, 250, 220))


# ============================================================ OUTRO
class Outro(Escena):
    PAL = "arcoiris"

    def preparar(self):
        self.t_cuevas = self.w("cuevas")
        self.t_pant = self.w("pantallas")
        self.t_cer = self.w("cerebro")
        self.t_hard = self.w("hardware")
        self.t_apps = self.w("aplicaciones")
        self.t_selfie = self.w("selfie")
        self.t_cav = self.w("cavernas")
        self.t_siendo = self.w("siendo")
        self.t_wifi = self.w("wifi")
        self.f1, self.f2 = self.fr[1]["t0"], self.fr[2]["t0"]
        self.fin = self.fr[2]["t1"] + 0.12
        self.ev(self.t_cuevas, "pop", 0.5)
        self.ev(self.t_pant, "morph", 0.8)
        self.ev(self.t_cer, "brillo", 0.6)
        self.ev(self.t_hard, "zap", 0.6)
        for k in range(6):
            self.ev(self.t_apps + 0.1 * k, "pop", 0.4, pan=-0.6 + 0.24 * k, tono=1.0 + 0.1 * k)
        self.ev(self.t_selfie, "obturador", 0.9)
        self.ev(self.t_siendo + 0.2, "puf", 0.8)
        self.ev(self.t_wifi, "ding", 0.8, tono=1.5)
        self.ev(self.fin, "impacto", 0.9)
        self.post_fx(self.t_wifi + 0.3, self.fin, lambda img, t, u: E.warhol(img, t, u), 0.05)

    def fondo(self, t):
        pul = env_bombo(t)
        if t < self.t_pant:
            return F.cueva(t, tinte=0.8, pulso=pul)
        if t < self.f1 - 0.2:
            return mezcla_fondos(t, self.t_pant, lambda tt: F.cueva(tt, tinte=0.8), lambda tt: F.rejilla(tt, pulso=pul))
        if t < self.fin:
            return mezcla_fondos(t, self.f1 - 0.2, lambda tt: F.rejilla(tt), lambda tt: F.tunel(tt, "neon", vel=0.8, pulso=pul))
        return mezcla_fondos(t, self.fin, lambda tt: F.tunel(tt, "neon"), lambda tt: F.rayos(tt, "arcoiris", n=16, pulso=pul))

    def camara(self, t):
        return 1.0 + 0.03 * math.sin(t * 1.1), 0.015 * math.sin(t * 0.9), 0.0, 0.0

    def dibujar(self, lz, t):
        tipos = ["camara", "musica", "corazon", "chat", "mapa", "juego"]
        # cueva -> pantalla
        if t < self.f1 + 0.1:
            fuera = e_in(prog(t, self.f1 - 0.25, self.f1 + 0.1))
            k = pop(t, self.fr[0]["t0"], 0.4) * (1 - fuera)
            if k > 0:
                arco_p = np.vstack([[(-230, 260)], D.arco(0, -20, 230, math.pi, 2 * math.pi, 40, ry=280), [(230, 260)]])
                tel = rect_red(-170, -290, 340, 560, 44)
                A_ = remuestrear_n(arco_p, 120)
                B_ = remuestrear_n(tel, 120)
                ia = int(np.argmin(A_[:, 0] * 0.3 - A_[:, 1]))
                ib = int(np.argmin(B_[:, 0] * 0.3 - B_[:, 1]))
                A_, B_ = np.roll(A_, -ia, 0), np.roll(B_, -ib, 0)
                u = e_inout(prog(t, self.t_pant - 0.05, self.t_pant + 0.45))
                P = A_ * (1 - u) + B_ * u
                with lz.grupo(960, 560, k):
                    if u < 0.5:
                        cerro = blob(0, 0, 520, seed=3, irr=0.08) * [1, 0.55] + [0, 320]
                        lz.forma(cerro, (110, 80, 60), NEGRO, 7, seed=80)
                    col = tuple(int(lerp(a, b, u)) for a, b in zip((25, 18, 20), (30, 30, 44)))
                    lz.forma(P, col, NEGRO, 9, seed=81)
                    if u < 0.6:
                        D.estarcido(lz, 0, 150, 0.55, 1.0 - u / 0.6, capa=1)
                    if u > 0.3:
                        for i, tp in enumerate(tipos):
                            ki = pop(t, self.t_pant + 0.2 + 0.07 * i, 0.3)
                            if ki > 0:
                                icono_app(lz, -75 + (i % 2) * 150, -170 + (i // 2) * 150, 0.95 * ki, tp, seed=90 + i, t=t)
        # cerebro: mismo hardware, apps nuevas
        if self.f1 - 0.2 <= t < self.f2 + 0.2:
            fuera = e_in(prog(t, self.f2 - 0.2, self.f2 + 0.15))
            kb = pop(t, self.t_cer, 0.4) * (1 - fuera)
            if kb > 0:
                D.cerebro(lz, 960, 540, 1.3 * kb, t, seed=100, brillo=0.5)
                kh = prog(t, self.t_hard, self.t_hard + 0.5)
                if kh > 0:
                    with lz.grupo(960, 540, 1.3 * kb):
                        for i in range(6):
                            y = -60 + i * 24
                            D.trazo_parcial(lz, [(-150, y), (-60, y), (-30, y + 20), (80, y + 20)], kh, CIAN, 6, seed=110 + i)
                    lz.texto("MISMO HARDWARE", 960, 290, 70, "snap", color=CIAN, borde=NEGRO, borde_px=9,
                             k=pop(t, self.t_hard, 0.3) * kb, seed=111)
                ka = pop(t, self.t_apps, 0.4) * kb
                if ka > 0:
                    for i, tp in enumerate(tipos):
                        a = i / 6 * 2 * math.pi + t * 0.9
                        icono_app(lz, 960 + 420 * math.cos(a), 560 + 230 * math.sin(a), 0.9 * pop(t, self.t_apps + 0.1 * i, 0.3) * kb, tp,
                                  seed=120 + i, t=t)
                    lz.texto("APPS NUEVAS", 960, 840, 70, "snap", color=MAGENTA, borde=NEGRO, borde_px=9, k=ka, seed=121)
        # selfie -> cavernícola con wifi
        if self.f2 - 0.2 <= t < self.fin + 0.25:
            fuera = e_in(prog(t, self.fin - 0.1, self.fin + 0.2))
            ent = e_out(prog(t, self.f2 - 0.1, self.f2 + 0.4))
            cav = t >= self.t_siendo + 0.2
            x = lerp(-300, 760, ent)
            brazo = (170, -560)
            yb = 920 + 1400 * fuera
            D.personaje(lz, x, yb, 1.0, t, "cave" if cav else "tu", seed=130, mano_d=brazo, mano_i=(-150, -300),
                        mirar=(0.6, -0.6), boca=0.3 if t > self.t_selfie else 0.0)
            D.telefono(lz, x + brazo[0], yb + brazo[1] - 60, 0.44, -0.25, t=t, seed=131,
                       pantalla=lambda lz: D.ui_camara(lz, t, 132))
            fl = campana(t, self.t_selfie - 0.02, self.t_selfie + 0.22)
            if fl > 0:
                with lz.capa(2):
                    lz.forma(estrella(x + 180, yb - 620, 170 * fl, 45 * fl, 8, t), (255, 255, 230), None, 0, seed=133)
            kp = campana(t, self.t_siendo + 0.05, self.t_siendo + 0.6)
            if kp > 0:
                with lz.capa(2):
                    for i in range(9):
                        a = i / 9 * 2 * math.pi
                        lz.forma(blob(x + 170 * math.cos(a) * kp, 700 + 200 * math.sin(a) * kp, 110 * kp, seed=140 + i, irr=0.2),
                                 (245, 245, 250), NEGRO, 5, seed=140 + i)
            kc = pop(t, self.t_cav, 0.3) * (1 - fuera)
            if kc > 0:
                lz.texto("CAVERNÍCOLA", 1400, 420, 84, "snap", color=(236, 146, 48), borde=NEGRO, borde_px=10, k=kc, rot=-0.06, seed=134)
            kw = pop(t, self.t_wifi, 0.35) * (1 - fuera)
            if kw > 0:
                D.wifi(lz, x - 10, 300, 1.2 * kw, seed=135)
                lz.texto("...CON WIFI", 1400, 580, 84, "snap", color=CIAN, borde=NEGRO, borde_px=10, k=kw, rot=-0.04, seed=136)
        # tarjeta final
        if t >= self.fin:
            k1 = pop(t, self.fin, 0.4)
            lz.texto("¿CUÁL TE", 960, 300, 120, "snap", color=AMARILLO, borde=NEGRO, borde_px=12, k=k1, rot=-0.04, seed=150)
            lz.texto("SORPRENDIÓ MÁS?", 960, 450, 110, "snap", color=BLANCO, borde=NEGRO, borde_px=12,
                     k=pop(t, self.fin + 0.2, 0.4), rot=-0.02, seed=151)
            chip(lz, 960, 620, "¡DÉJALO EN LOS COMENTARIOS!", pop(t, self.fin + 0.6, 0.4), 46, seed=152, fuente="snap")
            ke = e_out(prog(t, self.fin + 0.3, self.fin + 0.9))
            D.personaje(lz, lerp(-200, 330, ke), 1010, 0.8, t, "cave", seed=153, mano_d=(150, -390 + 40 * math.sin(t * 12)),
                        mirar=(0.6, -0.3), boca=0.3)
            D.personaje(lz, lerp(2120, 1590, ke), 1010, 0.8, t, "tu", seed=154, mano_i=(-150, -390 + 40 * math.sin(t * 12 + 1)),
                        mirar=(-0.6, -0.3), boca=0.3, accesorios=("auriculares",))

    def render(self, lz, t):
        img = Escena.render(self, lz, t)
        neg = prog(t, self.t1 - 0.6, self.t1 - 0.05)
        return img * (1 - neg) if neg > 0 else img



# id de escena (guion.py) -> clase que la dibuja
CLASES = dict(intro=Intro, manos=Manos, comida=Comida, musica=Musica, heroes=Heroes, joyas=Joyas,
              moda=Moda, cuenta=Cuenta, pesca=Pesca, ligar=Ligar, despedida=Despedida, outro=Outro)
