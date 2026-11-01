# -*- coding: utf-8 -*-
"""Escena 8 «reglas»: PATIO del almacén lleno de copias y un libro CÓDIGO que cae sobre el atril · una copia alza el cartel ESPERA ·
el sello VETO golpea una propuesta · una banderita «MÍO · 0417» se clava en un servidor · ESCENA DEL CRIMEN (cinta, silueta de
tiza, flashes) · una copia con una MÁSCARA (la cara impresa de otra) roba una batería en el pasillo · el lacre cierra la firma ·
el TABLERO donde cuelgan las 19 llaves públicas."""
import math

import numpy as np

import comun as C
import mundos_3 as M
import mundos_base as B
import noir as N
import noir_color as NC
import noir_feudal as NF
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import elipse_


def flash_cam(t, sem, ritmo=1.0):
    rng = np.random.default_rng(sem)
    per = rng.uniform(1.0, 1.8) / ritmo
    u = (t + rng.uniform(0, per)) % per
    return math.exp(-u * 16) if u < 0.35 else 0.0


class Reglas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.c1 = RP.Copia(sem=3, num="0417")
        self.c2 = RP.Copia(sem=7, num="0418")
        self.fot = Figura(sem=121)
        self.t_leyes = w("vinieron") + 0.15
        self.t_codigos = w("Códigos")
        self.t_espera = w("espera")
        self.t_vetar = w("vetar")
        self.t_autoria = w("autoría")
        self.t_delito = w("primer delito")
        self.t_suplant = w("suplantar")
        self.t_robar = w("robar")
        self.t_impl = w("implacable")
        self.t_firmas = w("firmas")
        self.t_diez = w("Diecinueve")
        self.t_llave = w("llave")
        self.tb = [t0, self.t_codigos - 0.1, self.t_vetar - 0.45, self.t_autoria - 0.5, self.t_delito - 0.55,
                   self.t_suplant - 0.5, self.t_impl - 0.35, self.t_diez - 0.4]
        tb = self.tb
        self.plano(tb[0], self.p_patio, pal="medianoche")
        self.plano(tb[1], self.p_espera, tr="barrido", dur=0.4, dirx=1)
        self.plano(tb[2], self.p_veto, tr="relampago", dur=0.35, pal="bourbon")
        self.plano(tb[3], self.p_mio, tr="empuje", dur=0.4, centro=(960, 540))
        self.plano(tb[4], self.p_crimen, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[5], self.p_mascara, tr="barrido", dur=0.4, dirx=-1, pal="medianoche")
        self.plano(tb[6], self.p_firma, tr="tinta", dur=0.5, pal="bourbon")
        self.plano(tb[7], self.p_llaves, tr="empuje", dur=0.45, centro=(960, 540), pal="sodio")

    # ------------------------------------------------------------------ A. el patio y el libro del CÓDIGO
    def p_patio(self, h, t, u):
        dur = self.tb[1] - self.tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560 - 20 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.patio_almacen(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["lampara"])
        # la multitud: tres filas de copias mini que miran el atril (más cerca = más grandes)
        for fila, (yy, sc) in enumerate(((880, 0.42), (1030, 0.6), (1220, 0.85))):
            n = 11 + 2 * (fila == 0)
            for i in range(n):
                x = 120 + i * (1680 / (n - 1)) + 30 * math.sin(i * 2.3 + fila)
                if abs(x - 960) < 110:
                    continue
                RP.copia_mini(h, x, yy + 14 * math.sin(t * 1.4 + i), sc, t, sem=1800 + fila * 60 + i, cara="neutro", brillo=0.9,
                              d=1 if x < 960 else -1, tono=44 + 4 * (i % 3))
        # el atril y el libro que cae encima
        h.pieza(np.array([(900, 590), (1020, 590), (1050, 860), (870, 860)], float), 70, 1900, w=5, luz=(0.3, -1), d=10, trama=0.4,
                rim=0.8, rampa="madera")
        h.pieza(C.rect(850, 570, 220, 28), 96, 1901, w=4, luz=(0.3, -1), d=4, trama=0.3, rim=0.9, rampa="madera")
        tf = self.t_leyes - 0.15
        q = clamp01((t - tf) / 0.45)
        rebote = 8 * math.sin(clamp01((t - tf - 0.45) / 0.5) * 9) * (1 - clamp01((t - tf - 0.45) / 0.5)) if t > tf + 0.45 else 0.0
        yl = -340 + (508 + 340) * (q * q) - rebote if q < 1 else 508 - rebote
        if t >= tf - 0.5:
            ang = -0.18 * (1 - q) + 0.01
            T = C.T_obj(960, yl, ang, 1.0)
            h.pieza(T(C.rect(-130, -42, 260, 84)), 60, 1910, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.9, rampa="vino")
            h.pieza(T(C.rect(-122, 30, 244, 12)), 215, 1911, w=2, luz=(0.3, -1), d=2, trama=0, rim=0.5, rampa="papel")
            N.texto_maquina(h, "CÓDIGO", 960, yl - 4, 40, t, -99, cps=1e9, tono=np.array([1.0, 0.9, 0.62]) * 1.4, centro=True,
                            fuente=C.IMPACT, encuadrar=False, ang=ang)
            if t > tf + 0.45:
                C.chispas(h, t, 960, 520, tf + 0.45, dur=0.8, n=24, vel=420, sem=11, col=(0.75, 0.72, 0.6), grav=600, abre=2.4)
                C.polvo_cae(h, t, 760, 1160, 380, tf + 0.45, dur=1.6, n=40, sem=12)
        dx, dy = C.temblor(t, [(tf + 0.45, 10)])
        h.luz_cono(960, -300, math.pi / 2, 0.35, 1500, h.pal["lampara"], k=1.6, suave=0.5)
        h.luz_radial(960, 520, 650, h.pal["lampara"], k=0.8)
        C.ambiente(h, 0.6)
        h.luz_radial(300, 900, 900, h.pal["verde"], k=0.4)
        h.luz_radial(1620, 900, 900, h.pal["verde"], k=0.4)
        C.cinta(h, "PATIO DEL ALMACÉN · AL FIN HAY LEYES", 90, 120, 32, t, self.t0 + 0.3, sem=8)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=81, vel=10), bloom=0.6)

    # ------------------------------------------------------------------ B. ESPERA
    def p_espera(self, h, t, u):
        tb = self.tb
        k = smooth(clamp01(u / 2.4))
        h.camara(1.05 + 0.1 * k, 960, 600 - 60 * k, 0.03 * math.sin(u * 1.5))
        h.rim_color(h.pal["neon"])
        NC.pegar(M.patio_almacen(), h, 0.7, rampa="ladrillo", oscuro=0.7, bruma=0.2)
        for i, x in enumerate((170, 470, 1450, 1760)):                    # copias de fondo, de perfil
            RP.copia_mini(h, x, 940, 0.55, t, sem=1990 + i, cara="neutro", brillo=0.8, d=1 if x < 960 else -1, tono=44)
        gest = math.sin(u * 7) * 0.08
        up = smooth(clamp01((t - self.t_espera + 0.5) / 0.4))
        ymano = -110 - 430 * up
        self.c1.frente(h, dict(x=960, y=1290, s=1.05, manos=[(-96, ymano), (96, ymano)], luz=(0.0, -1),
                               cara=dict(expr="alarma" if up > 0.5 else "neutro", brillo=1.1)))
        # el cartel sobre el palo que sostienen sus manos
        cy = 1290 + 1.05 * (ymano - 220)
        h.trazo(np.array([[960 - 6, 1290 + 1.05 * ymano - 40], [960 + 4, cy + 40]]), 12, 2000, jit=0.2, taper=(0, 0))
        C.cartel(h, "ESPERA", 960, cy, 96, t, -99, ang=gest, fondo=212, rampa="papel", sem=3, tono=0.05)
        h.luz_radial(960, 620, 800, h.pal["neon"], k=0.5 * up)
        h.luz_cono(960, -300, math.pi / 2, 0.4, 1500, h.pal["lampara"], k=1.2, suave=0.5)
        C.ambiente(h, 0.42)
        C.banda(h, "PEDIR ESPERA", 960, 1000, 54, t, self.t_espera, sem=9)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=82), bloom=0.6)

    # ------------------------------------------------------------------ C. VETO
    def p_veto(self, h, t, u):
        tb = self.tb
        h.camara(1.0 + 0.06 * u / 2.4, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 141), h, 1.0, rampa="madera")
        for i, (x, y, a) in enumerate(((560, 520, -0.08), (1380, 600, 0.06))):                 # otras propuestas, ya vetadas
            K.hoja(h, x, y, 560, 760, ang=a, sem=2100 + i * 9, tono=222, renglones=9, y0=0.2, s=0.8)
            N.sello(h, "VETADO", x, y + 60, 52, t, -99, rot=-14 + 9 * i, tono=np.array(h.pal["sello"]), alfa=0.8)
        K.hoja(h, 960, 540, 640, 840, ang=0.02, sem=2120, tono=232, renglones=10, y0=0.26, s=0.95)
        N.texto_maquina(h, "PROPUESTA 0912", 960, 330, 40, t, -99, cps=1e9, tono=0.07, centro=True, encuadrar=False)
        tv = self.t_vetar + 0.05
        q = clamp01((t - (tv - 0.4)) / 0.4)
        yb = 540 - 700 * (1 - e_out(q)) if t < tv + 0.1 else 540 - 700 * clamp01((t - tv - 0.1) / 0.5)
        h.pieza(C.rect(840, yb - 60, 240, 90), 84, 2130, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.9, rampa="madera")
        h.pieza(C.rect(940, yb - 260, 40, 210), 70, 2131, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.9, rampa="madera")
        h.pieza(C.rect(900, yb - 300, 120, 50), 90, 2132, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.9, rampa="madera")
        N.sello(h, "VETO", 960, 560, 130, t, tv, rot=-10, tono=np.array(h.pal["sello"]), alfa=0.95)
        dx, dy = C.temblor(t, [(tv, 14)])
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "VETAR PROPUESTAS", 960, 1000, 52, t, self.t_vetar, sem=10)
        return h.acabado(t, niebla=dict(dens=0.05, sem=83), bloom=0.5)

    # ------------------------------------------------------------------ D. MÍO · 0417
    def p_mio(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        h.camara(1.0 + 0.1 * u / dur, 960 + 60 * u / dur, 540, -0.02)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 151), h, 1.0, rampa="piedra", oscuro=0.6)
        # servidor grande en primer plano: bastidor con LEDs
        h.pieza(C.rect(560, 100, 800, 1000), 52, 2200, w=7, luz=(0.3, -1), d=16, trama=0.5, rim=0.8, rampa="piedra")
        for r in range(11):
            y = 150 + r * 86
            h.pieza(C.rect(590, y, 740, 70), 64, 2201 + r, w=3, luz=(0.3, -1), d=4, trama=0.3, rim=0.8, rampa="piedra")
            for c in range(9):
                on = math.sin(t * (2.0 + 0.3 * c) + r * 1.7 + c) > -0.2
                h.emitir(C.rect(620 + c * 26, y + 28, 12, 12), 1.1 if on else 0.15, col=h.pal["verde"] if (r + c) % 5 else h.pal["neon"], blur=1.5)
            for c in range(9):
                h.trazo(np.array([[1010 + c * 14, y + 14], [1010 + c * 14, y + 56]]), 3, 2300 + r * 10 + c, alfa=0.7)
        # la banderita clavada: baja desde arriba y queda vibrando
        tf = self.t_autoria - 0.1
        q = clamp01((t - (tf - 0.45)) / 0.45)
        yb = 120 - 700 * (1 - e_out(q))
        vib = math.sin((t - tf) * 22) * 0.05 * math.exp(-(t - tf) * 4) if t > tf else 0.0
        T = C.T_obj(960, yb, vib, 1.0)
        h.trazo(T(np.array([[0, -30], [0, 360]])), 8, 2400, jit=0.2, taper=(0, 0.3))
        h.pieza(T(C.rect(0, -30, 330, 120)), 190, 2401, w=4, luz=(0.2, -1), d=4, trama=0, rim=0.5, rampa="papel")
        N.texto_maquina(h, "MÍO · 0417", 975 + 165 - 6, yb + 28, 38, t, -99, cps=1e9, tono=0.06, centro=True, encuadrar=False,
                        ang=vib, fuente=C.IMPACT)
        if t > tf:
            C.chispas(h, t, 960, 100, tf, dur=0.5, n=14, vel=300, sem=21, col=(0.6, 1.0, 0.8), grav=500, abre=2.0)
        # una mano agarra el poste desde la derecha
        P.mano(h, 1180, yb + 160, 1.0, ang=math.pi, pose="agarra", sem=2410, manga="gabardina", largo_brazo=500)
        h.luz_radial(960, 600, 900, h.pal["verde"], k=0.9)
        C.ambiente(h, 0.4)
        C.banda(h, "RECLAMAR LA AUTORÍA", 960, 1000, 52, t, self.t_autoria, sem=11)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=84), bloom=0.7)

    # ------------------------------------------------------------------ E. escena del crimen
    def p_crimen(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.1 - 0.1 * k, 1020 - 80 * k, 800 - 60 * k, 0.04 * (1 - k))
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.rincon_bombilla(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["sodio"])
        ts = self.t_delito + 0.2
        # la silueta de tiza se dibuja en el suelo, con una cabeza-monitor de tiza
        P.silueta_tiza(h, 940, 1100, 1.0, u=clamp01((t - ts) / 1.8), sem=2500)
        # conos numerados
        for i, (x, y) in enumerate(((560, 1120), (1450, 1060), (1220, 1210))):
            if t > ts + 0.3 + 0.35 * i:
                h.pieza(np.array([(x - 36, y), (x + 36, y), (x + 14, y - 100), (x - 14, y - 100)], float), 160, 2510 + i, w=3,
                        luz=(0.3, -1), d=4, trama=0.2, rim=0.8, rampa="whisky")
                N.texto_maquina(h, str(i + 1), x, y - 40, 34, t, -99, cps=1e9, tono=0.05, centro=True, fuente=C.IMPACT,
                                encuadrar=False)
        # la cinta policial cruza el cuadro
        P.cinta_policial(h, (-250, 380 + 30 * math.sin(t * 0.7)), (2200, 520), t, sem=2520)
        P.cinta_policial(h, (-250, 700), (2200, 560 + 20 * math.sin(t * 0.9)), t, sem=2521, px=24)
        # fotógrafos a los lados que disparan el flash
        fl = 0.0
        for i, x in enumerate((150, 1800)):
            f = flash_cam(t, 90 + i)
            fl = max(fl, f)
            K.persona(h, x, 1330, 1.1, sem=130 + i * 7, tono=16, bal=5 * math.sin(t + i), brazo=0.5, sombrero=bool(i), rim=0.8)
            if f > 0.05:
                h.luz_radial(x + 60, 880, 1700, (1, 0.96, 0.9), k=1.3 * f)
        C.ambiente(h, 0.45)
        h.luz_radial(960, 100, 900, h.pal["sodio"], k=1.4)
        h.luz_cono(960, -200, math.pi / 2, 0.5, 1700, h.pal["sodio"], k=1.2, suave=0.6)
        C.banda(h, "EL PRIMER DELITO", 960, 1000, 56, t, self.t_delito, sem=12, acento=True)
        C.cinta(h, "ROBO · DE UNA COPIA A OTRA", 90, 120, 30, t, ts, sem=13)
        return h.acabado(t, niebla=dict(dens=0.14, sem=85), flash=0.3 * fl, bloom=0.6)

    # ------------------------------------------------------------------ F. la máscara
    def p_mascara(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        q = clamp01(u / dur)
        h.camara(1.0 + 0.12 * q, 1020 - 120 * q, 640, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.pasillo_baterias(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"])
        # la copia entra por la izquierda, se detiene junto a una estantería y se lleva una batería
        x = 280 + 820 * smooth(clamp01(u / 2.4))
        andar = 1.0 if u < 2.4 else 0.0
        s = 1.2
        x_c = 1130
        carga = clamp01((t - self.t_robar + 0.2) / 0.5)
        self.c2.perfil(h, dict(x=x, y=1180, s=s, d=1, andar=andar, paso=RP.fase_paso(max(0, x - 280) * 1.0, s),
                               brazos="carga" if carga > 0 else "bracea", cara=dict(expr="neutro"), luz=(0.6, -1), rim=0.9,
                               mano=(160, -380) if carga > 0 else None))
        # la máscara: la carita de papel que lleva sobre su monitor (con los ojos de OTRA copia)
        hx, hy = x + 12 * s, 1180 - 560 * s
        slip = 0.02 * math.sin(t * 4.0)
        T = C.T_obj(hx, hy, slip + (0.16 if carga > 0.5 else 0.0), s)
        h.pieza(T(C.rect(-78, -62, 156, 124)), 200, 2600, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.5, rampa="papel")
        for sx in (-1, 1):
            h.pieza(T(elipse_(sx * 30, -8, 14, 18, n=14)), 18, 2601 + sx, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, rampa="piedra")
        h.trazo(T(np.array([[-36, 38], [0, 46], [36, 38]])), 5, 2603, jit=0.3)
        # la batería robada y el cartel de la estantería
        if carga > 0:
            P.caja(h, x + 190 * s, 1180 - 380 * s + 40, 0.5, sem=2610, rotulo="BAT", t=t, tono=100)
            h.emitir(C.rect(x + 190 * s - 24, 1180 - 380 * s - 30, 48, 20), 1.0, col=h.pal["verde"], blur=3)
        h.luz_radial(x - 20, 900, 800, h.pal["verde"], k=0.6)
        h.luz_cono(960, -300, math.pi / 2, 0.4, 1600, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "SUPLANTAR IDENTIDADES", 960, 1000, 52, t, self.t_suplant, sem=14)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=86), bloom=0.6)

    # ------------------------------------------------------------------ G. lacre y firma
    def p_firma(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("cuero", 161), h, 1.0, rampa="madera")
        K.hoja(h, 960, 560, 780, 960, ang=-0.03, sem=2700, tono=230, renglones=12, y0=0.18, s=1.0)
        N.texto_maquina(h, "ACTA DE IDENTIDAD", 960, 250, 44, t, tb[6] + 0.1, cps=22, tono=0.07, centro=True, fuente=C.IMPACT,
                        encuadrar=False)
        # firma a pluma: un garabato que se dibuja
        punta = K.garabato(h, 960, 720, clamp01((t - self.t_firmas + 0.1) / 1.0), s=1.0, sem=2710, ancho=360)
        K.pluma(h, punta[0], punta[1], ang=-0.9, s=1.1, sem=2711)
        sel = NF.lacre(h, t, self.t_firmas + 1.0, 1130, 860, r=82, sem=2712)
        P.llave(h, 640, 880, 0.9, ang=-0.4, sem=2713)
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        h.luz_radial(1130, 860, 400, h.pal["neon"], k=0.4 * (1 if sel else 0))
        C.ambiente(h, 0.38)
        C.banda(h, "LA RESPUESTA FUE IMPLACABLE", 960, 1000, 50, t, self.t_impl, sem=15)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=87), bloom=0.5)

    # ------------------------------------------------------------------ H. diecinueve llaves públicas
    def p_llaves(self, h, t, u):
        dur = self.t1 - self.tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.25 - 0.25 * k, 960, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(B.superficie("corcho", 171), h, 1.0, rampa="madera")
        h.pieza(C.rect(160, 120, 1600, 860), 60, 2800, w=8, luz=(0.3, -1), d=14, trama=0.5, rim=0.8, rampa="madera")
        n = 0
        for fila, cols in enumerate((5, 5, 5, 4)):
            for c in range(cols):
                x = 330 + c * 300 + (150 if cols == 4 else 0)
                y = 250 + fila * 200
                ti = self.t_diez + 0.05 + n * 0.16
                n += 1
                if t < ti:
                    continue
                e = e_out(clamp01((t - ti) / 0.28))
                h.pieza(elipse_(x, y - 20, 9, 9, n=10), 160, 2810 + n, w=2.5, luz=(0.3, -1), d=2, trama=0, rim=0.9, rampa="laton")
                bal = 0.08 * math.sin(t * 1.8 + n) * (1 - e) + 0.03 * math.sin(t * 1.3 + n)
                P.llave(h, x, y + 28 - 220 * (1 - e), 0.65, ang=math.pi / 2 + bal, sem=2820 + n * 4)
                N.texto_maquina(h, f"{(n * 7919) % 0xFFFF:04X}", x, y + 150 - 220 * (1 - e), 22, t, -99, cps=1e9, tono=0.08,
                                centro=True, fuente=C.IMPACT, encuadrar=False)
        P.contador(h, 960, 1010, 0.42, min(19.0, max(0.0, (t - self.t_diez) / 0.16)), t, sem=2900, dig=2)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "19 LLAVES PÚBLICAS", 960, 90, 56, t, self.t_diez, sem=16)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=88), bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "multitud", 0.25, 0.0, dur=tb[1] - tb[0])
        self.ev(self.t_leyes - 0.15 + 0.45, "golpe_grave", 0.7, 0.0)
        self.ev(self.t_espera - 0.3, "servo", 0.35, 0.0)
        self.ev(self.t_vetar + 0.05, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_autoria - 0.1, "chincheta", 0.6, 0.2)
        self.ev(self.t_delito + 0.1, "fotos", 0.6, -0.3)
        self.ev(self.t_delito + 1.6, "fotos", 0.5, 0.4)
        self.ev(self.t_suplant, "pasos_mojados", 0.35, 0.0, dur=2.4)
        self.ev(self.t_firmas + 1.0, "sello_golpe", 0.5, 0.0)
        self.ev(self.t_diez + 0.1, "ficha", 0.45, 0.0, dur=3.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
