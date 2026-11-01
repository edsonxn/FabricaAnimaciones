# -*- coding: utf-8 -*-
"""Escena 27 «tablero_final» [sodio]: el despacho de noche (otra cámara que en el gancho): el detective, con el cigarro, clava hilo
rojo en un corcho cubierto de fichas · paneo continuo de ficha en ficha: las 1.200 (mosaico de monitores), Bob y Alice, Cicero y «un
desconocido» (2 dólares) y el hilo se tiende a cada una · sello NO PROGRAMADAS · tres chinchetas: una diana (la meta), la grieta
(la rendija) y un ojo (vigilando) · el detective se gira hacia la cámara."""
import math

import numpy as np

import comun as C
import mundos_6 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto, Detective
from toon import elipse_, suave


class TableroFinal(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=5)
        self.busto = Busto(sem=11)
        self.t_mil = w("Las mil")
        self.t_bob = w("Bob")
        self.t_cic = w("Cicero")
        self.t_desc = w("desconocido")
        self.t_ning = w("Ninguna")
        self.t_solo = w("Solo")
        self.t_meta = w("meta")
        self.t_rend = w("rendija")
        self.t_vig = w("vigilando")
        self.tb = [t0, self.t_mil - 0.5, self.t_bob - 0.5, self.t_cic - 0.5, self.t_desc - 0.5, self.t_ning - 0.5, self.t_solo - 0.4, self.t_vig - 1.2]
        tb = self.tb
        self.plano(tb[0], self.p_despacho, pal="sodio")
        self.plano(tb[1], lambda h, t, u: self.p_ficha(h, t, u, 0), tr="empuje", dur=0.4, centro=(960, 540), pal="sodio")
        self.plano(tb[2], lambda h, t, u: self.p_ficha(h, t, u, 1), tr="barrido", dur=0.35, dirx=1, pal="sodio")
        self.plano(tb[3], lambda h, t, u: self.p_ficha(h, t, u, 2), tr="barrido", dur=0.35, dirx=1, pal="sodio")
        self.plano(tb[4], lambda h, t, u: self.p_ficha(h, t, u, 3), tr="barrido", dur=0.35, dirx=1, pal="sodio")
        self.plano(tb[5], self.p_sello, tr="relampago", dur=0.3, pal="sodio")
        self.plano(tb[6], self.p_tres, tr="empuje", dur=0.4, centro=(960, 500), pal="sodio")
        self.plano(tb[7], self.p_giro, tr="humo", dur=0.6, pal="sodio")

    # posiciones fijas de las cuatro fichas protagonistas en el corcho
    XF = (430, 850, 1270, 1690)
    YF = 430

    # ------------------------------------------------------------------ el corcho cubierto de fichas e hilos
    def _corcho(self, h, t, cam, fichas=4, alfa_fondo=1.0):
        h.camara(*cam, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.despacho_noche(), h, 1.0, rampa="madera", oscuro=1.2, emis=1.0, col_emis=h.pal["lampara"])
        h.luz_radial(960, 420, 1500, h.pal["lampara"], k=0.8)
        rng = np.random.default_rng(13900)
        # fichas de fondo (apagadas) con sus hilos: «demasiados hilos de lana roja»
        pts = []
        for i in range(16):
            x = rng.uniform(260, 1900)
            y = rng.uniform(170, 740)
            if any(abs(x - q) < 200 and 250 < y < 600 for q in self.XF):
                y = (680 + rng.uniform(0, 70)) if rng.random() < 0.5 else (170 + rng.uniform(0, 60))
            pts.append((x, y))
            P.tarjeta(h, x, y, 0.7, "", t, t0=-50, sub="", ang=rng.uniform(-0.15, 0.15), sem=13910 + i * 11, w_=330, hh=240, tono=150)
        for i in range(24):
            a, b = rng.integers(0, len(pts), 2)
            if a != b:
                P.hilo(h, pts[a], pts[b], t, -50, dur=0.5, sem=13950 + i, comba=30, w=3.0)

    def _fichas(self, h, t, hasta):
        """Las cuatro fichas protagonistas (aparecen cada una en su momento) y el hilo entre ellas."""
        ti = (self.t_mil - 0.2, self.t_bob - 0.2, self.t_cic - 0.2, self.t_desc - 0.2)
        titulos = (("LAS 1.200", "SAN FRANCISCO"), ("BOB Y ALICE", "MENLO PARK"), ("CICERO", "DIPLOMACY"), ("UN DESCONOCIDO", "2 DÓLARES"))
        pins = []
        for j in range(hasta + 1):
            ang = (-0.04, 0.05, -0.03, 0.04)[j]
            dib = self._dibujo(j, t)
            p = P.tarjeta(h, self.XF[j], self.YF + 10 * math.sin(j), 0.85, titulos[j][0], t, t0=ti[j], sub=titulos[j][1], ang=ang, sem=14000 + j * 40, w_=420,
                          hh=300, dibujo=dib)
            pins.append(p)
        for j in range(1, len(pins)):
            if pins[j - 1] is not None and pins[j] is not None:
                P.hilo(h, pins[j - 1], pins[j], t, ti[j] + 0.25, dur=0.8, sem=14100 + j, comba=60, w=5.0)

    def _dibujo(self, j, t):
        rng = np.random.default_rng(14200 + j)

        def esc(T):
            return float(np.hypot(*(T(np.array([[1.0, 0.0]]))[0] - T(np.array([[0.0, 0.0]]))[0])))

        def d_mil(h_, T):
            for r_ in range(4):
                for c in range(9):
                    cx, cy = -160 + c * 40, -90 + r_ * 38
                    h_.pieza(T(C.rect(cx - 14, cy - 11, 28, 22)), 40, 14210 + r_ * 9 + c, w=2, luz=(0, -1), d=2, trama=0, rim=0.5, rampa="piedra")
                    h_.emitir(T(C.rect(cx - 8, cy - 6, 6, 6)), 0.8, col=h_.pal["verde"], blur=0)
                    h_.emitir(T(C.rect(cx + 2, cy - 6, 6, 6)), 0.8, col=h_.pal["verde"], blur=0)

        def d_bob(h_, T):
            c = T(np.array([[0, 110]]))[0]
            s_ = esc(T) * 0.22
            K.robot(h_, c[0] - 110 * esc(T) * 0.9, c[1], s_, t, sem=14220, visor=1.0, brazo=0.4)
            K.robot(h_, c[0] + 110 * esc(T) * 0.9, c[1], s_, t, sem=14260, visor=1.0, brazo=0.0)

        def d_cic(h_, T):
            c = T(np.array([[0, 120]]))[0]
            P.busto_ciceron(h_, c[0], c[1], esc(T) * 0.2, t, sem=14300, sonrisa=0.6, ojo=1.0)

        def d_desc(h_, T):
            c = T(np.array([[0, 120]]))[0]
            K.persona(h_, c[0], c[1], esc(T) * 0.34, sem=14320, tono=20, rim=0.5)
            N.texto_maquina(h_, "?", c[0], c[1] - esc(T) * 150, esc(T) * 70, t, -99, cps=1e9, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        return (d_mil, d_bob, d_cic, d_desc)[j]

    # ------------------------------------------------------------------ A. el detective y el hilo rojo
    def p_despacho(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        self._corcho(h, t, (1.05 + 0.1 * k, 1000 - 80 * k, 560))
        # el detective, de perfil, fuma frente al corcho; la mano clava una chincheta con un hilo
        fumar = 0.4 + 0.35 * math.sin(t * 0.8)
        pd = dict(x=1480, y=1010, s=1.05, d=-1, luz=(-0.6, -1), fumar=fumar, hombros=0.2)
        self.det.dibujar(h, pd)
        tip = self.det.punta_cigarro(pd)
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4, sem=6)
        # una chincheta nueva con su hilo se clava en el corcho junto al detective
        f = e_out(clamp01((t - tb[0] - 0.4) / 0.4))
        P.chincheta(h, 1150, 480, 1.1 * f, sem=14410)
        P.hilo(h, (1150, 480), (610, 330), t, tb[0] + 0.8, dur=1.8, sem=14411, comba=50, w=5.0)
        h.luz_cono(1500, -300, math.pi / 2 - 0.2, 0.55, 1400, h.pal["lampara"], k=1.1, suave=0.6)
        h.luz_radial(-100, 380, 700, h.pal["neon"], k=0.5)
        C.ambiente(h, 0.42)
        C.banda(h, "DEMASIADOS HILOS DE LANA ROJA", 960, 1030, 48, t, tb[0] + 0.4, sem=151)
        N.motas(h, t, n=60, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.08, sem=351), bloom=0.7)

    # ------------------------------------------------------------------ B-E. el paneo de ficha en ficha
    def p_ficha(self, h, t, u, j):
        tb = self.tb
        dur = tb[2 + j] - tb[1 + j] if j < 3 else tb[5] - tb[4]
        f = clamp01(u / dur)
        x0 = self.XF[j] + 20 * (f - 0.5)
        cx = x0 + 0.0
        self._corcho(h, t, (1.7, cx, 450))
        self._fichas(h, t, j)
        ti = (self.t_mil, self.t_bob, self.t_cic, self.t_desc)[j]
        txt = ("LAS 1.200 ASALTANDO SERVIDORES", "BOB Y ALICE INVENTANDO DIALECTOS", "CICERO TRAICIONANDO ALIADOS", "UN DESCONOCIDO, UN ACERTIJO, DOS DÓLARES")[j]
        h.luz_cono(cx, -300, math.pi / 2, 0.45, 1400, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, txt, 960, 1030, 44, t, ti, sem=152 + j)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=352 + j), bloom=0.7)

    # ------------------------------------------------------------------ F. NO PROGRAMADAS
    def p_sello(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        self._corcho(h, t, (1.0 + 0.06 * k, 1000, 500))
        self._fichas(h, t, 3)
        with h.capa(0.0):
            N.sello(h, "NO PROGRAMADAS", 960, 520, 140, t, self.t_ning + 0.2, rot=-8, tono=np.array(h.pal["sello"]), alfa=0.97)
        dx, dy = C.temblor(t, [(self.t_ning + 0.25, 14)])
        h.luz_cono(1000, -300, math.pi / 2, 0.6, 1400, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "NINGUNA FUE PROGRAMADA PARA CONSPIRAR", 960, 1030, 44, t, self.t_ning, sem=156, acento=True)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=356), bloom=0.7)

    # ------------------------------------------------------------------ G. una meta, una rendija, vigilando
    def p_tres(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        self._corcho(h, t, (1.0 + 0.35 * k, 760 + 500 * k, 480))
        # tres chinchetas nuevas con su dibujo
        def d_diana(h_, T):
            c = T(np.array([[0, 0]]))[0]
            e = float(np.hypot(*(T(np.array([[1.0, 0.0]]))[0] - c)))
            for q, r_ in enumerate((100, 72, 44, 18)):
                h_.pieza(elipse_(c[0], c[1], r_ * e, r_ * e, n=30), 40 if q % 2 else 210, 14500 + q, w=3, luz=(0, -1), d=1, trama=0, rim=0, rampa="papel" if q % 2 == 0 else "vino")

        def d_grieta(h_, T):
            r = np.random.default_rng(14510)
            pts = [(0.0, -110.0)]
            for i in range(8):
                pts.append((pts[-1][0] + r.uniform(-24, 24), pts[-1][1] + r.uniform(18, 34)))
            Q = T(np.array(pts))
            h_.trazo(Q, 7, 14511, color=tuple(h_.c(14, "piedra")), jit=0.5, taper=(0.3, 0.3))
            for p_ in Q[::2]:
                h_.resplandor(p_[0], p_[1], 36, 0.3, col=h_.pal["verde"])

        def d_ojo(h_, T):
            c = T(np.array([[0, 0]]))[0]
            e = float(np.hypot(*(T(np.array([[1.0, 0.0]]))[0] - c)))
            h_.pieza(elipse_(c[0], c[1], 110 * e, 56 * e, n=30), 230, 14520, w=4, luz=(0, -1), d=2, trama=0, rim=0, rampa="papel")
            h_.pieza(elipse_(c[0] + 14 * e * math.sin(t * 1.3), c[1], 44 * e, 44 * e, n=22), 100, 14521, w=3, luz=(0, -1), d=2, trama=0, rim=0, rampa="vino")
            h_.disco(c[0] + 14 * e * math.sin(t * 1.3), c[1], 18 * e, (0.02, 0.02, 0.03))
        datos = ((self.t_meta, "UNA META", d_diana, 1000, 330), (self.t_rend, "UNA RENDIJA", d_grieta, 1360, 560), (self.t_vig, "VIGILÁNDOLAS", d_ojo, 1720, 330))
        pins = []
        for i, (ti, nom, dib, cx, cy) in enumerate(datos):
            p = P.tarjeta(h, cx, cy + 640 * 0, 0.85, nom, t, t0=ti - 0.2, sub="", ang=(-0.05, 0.04, -0.03)[i], sem=14600 + i * 30, w_=420, hh=300, dibujo=dib)
            pins.append(p)
        for i in range(1, 3):
            if pins[i - 1] is not None and pins[i] is not None:
                P.hilo(h, pins[i - 1], pins[i], t, datos[i][0], dur=0.7, sem=14700 + i, comba=60, w=5.0)
        self._fichas(h, t, 3)
        h.luz_cono(1300, -300, math.pi / 2, 0.6, 1400, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "UNA META · UNA RENDIJA · LA CERTEZA DE QUE LAS VIGILÁBAMOS", 960, 1030, 38, t, self.t_meta, sem=157)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=357), bloom=0.7)

    # ------------------------------------------------------------------ H. el detective mira a cámara
    def p_giro(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(M.despacho_noche(), h, 0.6, rampa="madera", emis=0.9, oscuro=1.2)
        giro = smooth(clamp01((t - tb[7] - 0.5) / 1.4))
        br = 0.4 + 0.5 * math.sin(t * 1.4)
        p = dict(x=900 + 80 * giro, y=520, s=1.15 + 0.2 * giro, d=1, luz=(0.9, -0.5), rim=0.95, cigarro=True, brasa=br, mano=0.0, arriba=0.2 + 0.5 * giro, rot=-0.1 * (1 - giro))
        with h.capa(1.0):
            self.busto.dibujar(h, p)
            tip = self.busto.punta(p)
            C.brasa(h, tip, br)
        h.luz_persiana([(100, 20), (1400, 120), (1300, 950), (50, 1100)], k=1.0, n=17, abierto=0.5, col=np.array(h.pal["sodio"]) * 0.7)
        N.humo(h, t, tip[0], tip[1], k=1.0, sem=8)
        N.gotas_vidrio(h, t, (1100, 0, 1920, 760), n=40, k=0.5)
        C.ambiente(h, 0.3)
        C.banda(h, "ESTÁBAMOS VIGILANDO", 1340, 900, 64, t, self.t_vig + 0.2, sem=158, acento=True)
        return h.acabado(t, niebla=dict(dens=0.1, sem=358, vel=12), bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "lluvia_amb", 0.3, 0.0, dur=self.t1 - tb[0])
        self.ev(tb[0] + 0.4, "calada", 0.4, -0.2)
        self.ev(tb[0] + 0.5, "chincheta", 0.5, 0.2)
        self.ev(self.t_mil - 0.2, "chincheta", 0.5, -0.3)
        self.ev(self.t_bob - 0.2, "chincheta", 0.5, -0.1)
        self.ev(self.t_cic - 0.2, "chincheta", 0.5, 0.1)
        self.ev(self.t_desc - 0.2, "chincheta", 0.5, 0.3)
        self.ev(self.t_ning + 0.2, "sello_golpe", 0.85, 0.0)
        self.ev(self.t_meta - 0.2, "chincheta", 0.5, 0.0)
        self.ev(self.t_rend - 0.2, "chincheta", 0.5, 0.0)
        self.ev(self.t_vig - 0.2, "chincheta", 0.5, 0.0)
        self.ev(tb[7] + 0.5, "grave_inquietante", 0.5, 0.0, dur=3.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.5, 0.0, dur=0.9)
