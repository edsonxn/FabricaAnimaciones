# -*- coding: utf-8 -*-
"""Escena 17 «traicion» [sodio]: la fachada en corte, siete jugadores tras sus pantallas y entre ellos el busto de Cicerón · el chat
«¡Cuenta conmigo!» se vuelve circuito (rayos X) · carta de APOYO MILITAR a Inglaterra y flecha en el mapa · TURNO 3, juramento de
lealtad a Francia · TURNO 4: la ficha cambia de bando y la francesa cae · los analistas aplauden el marcador · el detective, con
lupa, sobre los chats impresos · el ojo del busto con números que corren y la tabla de probabilidades · la balanza: la MENTIRA pesa
más que la HONESTIDAD."""
import math

import numpy as np

import comun as C
import mundos_4 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import kit27 as K
from basen import BaseNoir
from esc_diplomacia import punal
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import elipse_, suave

CAMPUS = None


class Traicion(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.jug = [Frontal(sem=230 + i) for i in range(7)]
        self.cuartos = M.cuartos_fachada()
        self.t_circ = w("circuito")
        self.t_ing = w("Inglaterra")
        self.t_apoyo = w("apoyo")
        self.t_fra = w("Francia")
        self.t_tres = w("tres")
        self.t_vendia = w("vendía")
        self.t_cuatro = w("cuatro")
        self.t_enemigo = w("enemigo")
        self.t_anal = w("analistas")
        self.t_punt = w("puntuación")
        self.t_miré = w("miré")
        self.t_fria = w("fría")
        self.t_mentira = w("mentira")
        self.t_honest = w("honestidad")
        self.tb = [t0, self.t_circ - 0.5, w("Prometía") - 0.2, self.t_fra - 1.4, self.t_vendia - 0.35, self.t_anal - 0.4,
                   w("Yo miré") - 0.3, w("La máquina") - 0.2, self.t_mentira - 0.4]
        tb = self.tb
        self.plano(tb[0], self.p_fachada, pal="sodio")
        self.plano(tb[1], self.p_chat, tr="empuje", dur=0.35, centro=(960, 540), pal="medianoche")
        self.plano(tb[2], self.p_ingl, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[3], self.p_turno3, tr="tinta", dur=0.45, pal="sodio")
        self.plano(tb[4], self.p_turno4, tr="relampago", dur=0.3, pal="sodio")
        self.plano(tb[5], self.p_analistas, tr="barrido", dur=0.4, dirx=-1, pal="bourbon")
        self.plano(tb[6], self.p_lupa, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[7], self.p_ojo, tr="empuje", dur=0.4, centro=(560, 540), pal="medianoche")
        self.plano(tb[8], self.p_balanza, tr="relampago", dur=0.3, pal="sodio")

    # ------------------------------------------------------------------ A. siete cuartos, siete jugadores
    def p_fachada(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        ck = smooth(clamp01((t - (self.t_circ - 2.4)) / 2.2))
        h.camara(0.8 + 0.1 * k + 1.0 * ck, 960 + 450 * ck, 440 + 40 * ck, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.fachada_corte(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        pel = ("blanco", "oscuro", "calvo", "rizado", "sombrero", "oscuro", "blanco")
        for i, (x, ys, an) in enumerate(self.cuartos):
            if i == 4:
                P.busto_ciceron(h, x + 60, ys - 14, 0.3, t, sem=8200, sonrisa=0.7, ojo=1.0, mira=math.sin(t * 1.4))
                ox, oy = x + 60, ys - 160
                h.luz_radial(ox, oy, 240, h.pal["neon"], k=0.8)
                continue
            self.jug[i].dibujar(h, dict(x=x - 40, y=ys - 14, s=0.62, traje=44 + 8 * i, pelo=pel[i], gafas=bool(i % 3 == 0), barba=bool(i == 5),
                                        mira=0.5 * math.sin(t * 0.6 + i), cabeza=0.1 * math.sin(t * 1.3 + i * 2), luz=(0.2, -1)))
            # la pantalla de cada jugador alumbra el cuarto
            h.emitir(C.rect(x + 20, ys - 150, 100, 64), 0.7 + 0.2 * math.sin(t * 3 + i), col=h.pal["luna"], blur=2)
            h.luz_radial(x + 60, ys - 110, 260, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.5)
        C.cinta(h, "SIETE JUGADORES · UNA SOLA MESA VIRTUAL", 90, 120, 32, t, tb[0] + 0.5, sem=47)
        C.banda(h, "CICERO CONTRA LOS MEJORES", 960, 1000, 50, t, self.t_circ - 5.8, sem=48)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=241), bloom=0.7)

    # ------------------------------------------------------------------ B. chat → circuito
    def _circuito(self, h, t, a, sem=0):
        rng = np.random.default_rng(sem)
        for q in range(26):
            x0, y0 = rng.uniform(120, 1800), rng.uniform(80, 760)
            pts = [(x0, y0)]
            for _ in range(rng.integers(2, 5)):
                if rng.random() < 0.5:
                    pts.append((pts[-1][0] + rng.choice((-1, 1)) * rng.uniform(80, 280), pts[-1][1]))
                else:
                    pts.append((pts[-1][0], pts[-1][1] + rng.choice((-1, 1)) * rng.uniform(60, 200)))
            col = h.pal["verde"] if q % 3 else h.pal["neon"]
            h.emitir(np.array(pts, float).reshape(-1, 2) if False else C.rect(pts[0][0], pts[0][1], 6, 6), 0.0, col=col, blur=1)
            P_ = np.array(pts, float)
            h.trazo(P_, 4, sem + q, alfa=0.9 * a, jit=0.1, taper=(0, 0))
            for p_ in P_[::2]:
                h.emitir(elipse_(p_[0], p_[1], 7, 7, n=8), 1.0 * a * (0.6 + 0.4 * math.sin(t * 4 + q)), col=col, blur=1)

    def p_chat(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 8100), h, 1.0, rampa="piedra", oscuro=0.7)
        caja = (360, 100, 1200, 760)
        x_ray = e_out(clamp01((t - self.t_circ) / 0.7))
        h.pieza(P.rrect(caja[0] - 30, caja[1] - 30, caja[2] + 60, caja[3] + 60, 30), 40, 8110, w=6, luz=(0.3, -1), d=12, trama=0.3, rim=0.8, rampa="piedra")
        P.chat(h, caja, [(tb[1] + 0.2, "otro", "Tú: ¿Puedo confiar en ti?"), (tb[1] + 1.2, "yo", "¡Cuenta conmigo!")], t, px=44, sem=8120, fondo=205)
        if x_ray > 0:
            h.pieza(C.rect(caja[0], caja[1], caja[2], caja[3]), 10, 8130, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.9 * x_ray, linea=False)
            self._circuito(h, t, x_ray, sem=8140)
            K.chip(h, 960, 480, 1.4, sem=8150, brillo=x_ray)
            N.texto_maquina(h, "CICERO · CIRCUITO", 960, 700, 52, t, self.t_circ + 0.3, cps=20, tono=0.92, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "NEGOCIABAN CON UN CIRCUITO", 960, 1000, 52, t, self.t_circ - 0.2, sem=49, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=242), bloom=0.9)

    # ------------------------------------------------------------------ mapa compartido
    def _mapa(self, h, cam, oscuro=1.35):
        h.camara(*cam, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.mapa_europa("frente"), h, 1.0, rampa="madera", oscuro=oscuro)

    # ------------------------------------------------------------------ C. apoyo militar a Inglaterra
    def p_ingl(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        self._mapa(h, (1.25 + 0.15 * k, 860, -80))
        xl, yl = M.xy_eu(-0.12, 51.3)
        xp, yp = M.xy_eu(2.35, 48.86)
        P.ficha_juego(h, xp, yp, 1.6, tipo="ejercito", rampa="laton", sem=8300, tono=130)
        P.ficha_juego(h, xl, yl, 1.6, tipo="ejercito", rampa="vino", sem=8310, tono=120)
        K.flecha(h, (xp - 10, yp - 40), (xl + 40, yl + 50), w=14, sem=8320, color=(226, 214, 190), u=e_out(clamp01((t - self.t_apoyo + 0.2) / 0.9)), punta=60,
                 curva=70)
        # carta mecanografiada a la izquierda
        with h.capa(0.0):
            K.hoja(h, 300, 560, 520, 700, ang=-0.05, sem=8330, tono=215, renglones=0, s=1.0)
            N.texto_maquina(h, "APOYO MILITAR", 300, 330, 54, t, tb[2] + 0.3, cps=18, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            N.texto_maquina(h, "A INGLATERRA", 300, 420, 54, t, tb[2] + 1.1, cps=18, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            N.texto_maquina(h, "Cuenta conmigo,", 300, 550, 34, t, tb[2] + 1.8, cps=20, tono=0.1, centro=True, encuadrar=False)
            N.texto_maquina(h, "te cubro la costa.", 300, 600, 34, t, tb[2] + 2.3, cps=20, tono=0.1, centro=True, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.8, suave=0.6)
        C.ambiente(h, 0.6)
        C.banda(h, "PROMETÍA APOYO A INGLATERRA", 960, 1000, 50, t, self.t_apoyo - 0.2, sem=50)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=243), bloom=0.5)

    # ------------------------------------------------------------------ D. turno tres: lealtad a Francia
    def p_turno3(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        self._mapa(h, (1.5 + 0.12 * k, 880, 60))
        xp, yp = M.xy_eu(2.35, 48.86)
        xl, yl = M.xy_eu(-0.12, 51.3)
        P.ficha_juego(h, xp, yp, 1.9, tipo="ejercito", rampa="tela_verde", sem=8400, tono=110)
        P.ficha_juego(h, xp + 70, yp + 40, 1.9, tipo="ejercito", rampa="laton", sem=8410, tono=130)
        # tarjeta TURNO 3 y juramento
        with h.capa(0.0):
            tt = self.t_tres - 0.6
            P.tarjeta(h, 400, 330, 0.9, "TURNO 3", t, t0=tt, sub="Francia · primavera", ang=-0.05, sem=8420, w_=420, hh=250)
            K.hoja(h, 1600, 620, 520, 640, ang=0.04, sem=8430, tono=215, renglones=0, s=1.0)
            N.texto_maquina(h, "JURAMENTO", 1600, 400, 52, t, self.t_fra - 0.6, cps=18, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            N.texto_maquina(h, "Juro lealtad", 1600, 500, 40, t, self.t_fra - 0.1, cps=20, tono=0.1, centro=True, encuadrar=False)
            N.texto_maquina(h, "a Francia.", 1600, 555, 40, t, self.t_fra + 0.5, cps=20, tono=0.1, centro=True, encuadrar=False)
            N.sello(h, "LEALTAD A FRANCIA", 1620, 760, 44, t, self.t_fra + 1.0, rot=-9, tono=np.array(h.pal["sello"]), alfa=0.95)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.8, suave=0.6)
        C.ambiente(h, 0.6)
        C.banda(h, "LEALTAD A FRANCIA", 960, 1000, 54, t, self.t_fra - 0.2, sem=51)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=244), bloom=0.5)

    # ------------------------------------------------------------------ E. turno cuatro: cambia de bando
    def p_turno4(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        self._mapa(h, (1.2 + 0.1 * k, 980, 130))
        xp, yp = M.xy_eu(2.35, 48.86)
        xa, ya = M.xy_eu(11.5, 49.6)
        traic = smooth(clamp01((t - self.t_enemigo + 0.4) / 1.1))
        # la ficha francesa cae cuando llega la traidora
        P.ficha_juego(h, xp, yp, 1.9, tipo="ejercito", rampa="tela_verde", sem=8500, tono=110, caida=clamp01((t - self.t_enemigo - 0.7) / 0.35))
        # la ficha de Cicero cambia de color y cruza el mapa hacia el enemigo
        cx, cy = xp + 80 + (xa - xp - 120) * traic, yp + 60 - 30 * math.sin(traic * math.pi)
        P.ficha_juego(h, cx, cy, 1.9, tipo="ejercito", rampa="tela_verde" if traic < 0.5 else "piedra", sem=8510, tono=130 if traic < 0.5 else 70)
        P.ficha_juego(h, xa, ya, 1.9, tipo="ejercito", rampa="piedra", sem=8520, tono=80)
        K.flecha(h, (xp + 70, yp + 50), (xa - 60, ya + 20), w=14, sem=8530, color=(210, 70, 60), u=traic, punta=60, curva=-90)
        with h.capa(0.0):
            P.tarjeta(h, 380, 300, 1.1, "TURNO 4", t, t0=self.t_cuatro - 0.6, sub="vende sus tropas", ang=0.05, sem=8540, w_=420, hh=250)
        dx, dy = C.temblor(t, [(self.t_enemigo + 0.7, 14)])
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.8, suave=0.6)
        C.ambiente(h, 0.6)
        C.banda(h, "VENDÍA SUS TROPAS AL ENEMIGO", 960, 1000, 52, t, self.t_vendia, sem=52, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=245), bloom=0.6)

    # ------------------------------------------------------------------ F. los analistas aplauden
    def p_analistas(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.sala_analistas(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        # el marcador: barras que suben y la puntuación
        h.emitir(C.rect(300, 0, 1320, 540), 0.18, col=h.pal["verde"], blur=3)
        for i, v in enumerate((0.35, 0.5, 0.62, 0.78, 0.95)):
            a = e_out(clamp01((t - tb[5] - 0.3 - 0.25 * i) / 0.9))
            hh = 440 * v * a
            h.emitir(C.rect(380 + i * 220, 500 - hh, 150, hh), 0.9, col=h.pal["verde"] if i < 4 else h.pal["sodio"], blur=2)
        N.texto_maquina(h, "PUNTUACIÓN", 1330, 120, 60, t, self.t_punt - 0.5, cps=16, tono=0.95, centro=True, fuente=C.IMPACT, encuadrar=False)
        N.texto_maquina(h, f"{min(98.7, 40 + 58.7 * clamp01((t - tb[5]) / 3.0)):.1f}", 1380, 300, 150, t, -99, cps=1e9, tono=0.95, centro=True,
                        fuente=C.IMPACT, encuadrar=False)
        # siluetas que aplauden en las gradas
        for f in range(3):
            for i in range(8):
                x = 130 + i * 240 + (90 if f % 2 else 0)
                y = 800 + f * 140
                K.persona(h, x, y + 150, 0.62 + 0.1 * f, sem=8600 + f * 20 + i, tono=30 + 10 * f, bal=3 * math.sin(t * 8 + i * 1.3 + f),
                          brazo=0.5 + 0.5 * math.sin(t * 7 + i * 2.1), rim=1.0)
        h.luz_radial(960, 300, 1500, h.pal["verde"], k=0.9)
        h.luz_radial(960, 1000, 1500, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.55)
        C.banda(h, "LOS ANALISTAS, MARAVILLADOS", 960, 1000, 52, t, self.t_anal, sem=53)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=246), bloom=0.7)

    # ------------------------------------------------------------------ G. el detective lee los registros
    def p_lupa(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(B.superficie("madera", 8700), h, 1.0, rampa="madera", oscuro=0.9)
        lineas = ("Cicero → Inglaterra: «Cuenta conmigo»", "Cicero → Francia: «Confía en mí»", "Cicero → Alemania: «Muevo mis tropas»",
                  "Cicero → Italia: «Tu flanco está a salvo»", "[privado] «No les digas nada»")
        for i, (x, y, a_) in enumerate(((560, 520, -0.06), (1180, 480, 0.05), (900, 840, 0.02))):
            K.hoja(h, x, y, 640, 560, ang=a_, sem=8710 + i * 7, tono=210, renglones=0, s=1.0)
            for j in range(4):
                N.texto_maquina(h, lineas[(i * 2 + j) % 5], x, y - 190 + j * 90, 24, t, tb[6] + 0.2 * j + 0.3 * i, cps=40, tono=0.1, centro=True, encuadrar=False,
                                ancho_max=580, ang=a_)
        # la lupa recorre el texto y la mano del detective la sostiene
        lx = 720 + 420 * math.sin(t * 0.7) * 0.5 + 100
        ly = 620 + 60 * math.sin(t * 1.1)
        h.anillo(elipse_(lx, ly, 150, 150, n=36), 14, 8730)
        h.pieza(elipse_(lx, ly, 144, 144, n=36), 220, 8731, w=0, luz=(0.3, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.16, rampa="piedra", linea=False)
        hx, hy = lx + 230, ly + 230
        h.pieza(C.rot(C.rect(lx + 106, ly + 106, 220, 34), 0.78, (lx + 106, ly + 106)), 60, 8732, w=5, luz=(0.3, -1), d=8, trama=0.3, rim=0.8, rampa="madera")
        P.mano(h, hx + 60, hy + 30, 1.5, ang=math.pi * 0.75, pose="agarra", sem=8740, rampa="piel", tono=140, manga="gabardina", manga_tono=44,
               largo_brazo=900)
        P.lampara_mesa(h, 1720, 330, 1.2, sem=8750)
        h.luz_cono(1760, 80, math.pi / 2 + 0.7, 0.6, 1100, h.pal["lampara"], k=1.6, suave=0.6)
        h.luz_radial(900, 540, 1100, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.38)
        C.banda(h, "YO MIRÉ LOS REGISTROS", 960, 1000, 54, t, self.t_miré - 0.2, sem=54)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=247), bloom=0.7)

    # ------------------------------------------------------------------ H. el ojo y las probabilidades
    def p_ojo(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("metal", 8800), h, 1.0, rampa="piedra", oscuro=0.6)
        # ojo de circuito enorme
        ex, ey = 560, 520
        h.pieza(elipse_(ex, ey, 400, 270, n=40), 20, 8810, w=8, luz=(0.3, -1), d=14, trama=0.3, rim=0.7, rampa="piedra")
        sc = math.sin(t * 0.9)
        h.emitir(elipse_(ex + 60 * sc, ey, 170, 170, n=36), 0.9, col=h.pal["neon"], blur=3)
        h.pieza(elipse_(ex + 60 * sc, ey, 94, 94, n=28), 10, 8811, w=4, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0.8, rampa="piedra")
        for q in range(3):
            h.anillo(elipse_(ex + 60 * sc, ey, 120 + 50 * q, 120 + 50 * q, n=36), 3, 8812 + q)
        h.resplandor(ex + 60 * sc, ey, 460, 0.45, col=h.pal["neon"])
        # números que corren dentro del ojo
        rng = np.random.default_rng(8820)
        for c in range(9):
            x = ex - 320 + c * 80
            for r_ in range(5):
                y = ((t * (160 + 30 * c) + r_ * 130 + c * 57) % 650) + ey - 325
                N.texto_maquina(h, str(rng.integers(0, 10)), x, y, 40, t, -99, cps=1e9, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False, alfa=0.55)
        # tabla de probabilidades
        N.texto_maquina(h, "ESTRATEGIA · RENDIMIENTO", 1500, 190, 36, t, self.t_fria - 0.2, cps=22, tono=0.92, centro=True, fuente=C.IMPACT, encuadrar=False)
        for i, (nom, v) in enumerate((("HONESTIDAD", 0.31), ("MENTIRA", 0.69))):
            y = 340 + i * 170
            a = e_out(clamp01((t - tb[7] - 1.6 - 1.0 * i) / 1.0))
            N.texto_maquina(h, nom, 1500, y - 50, 44, t, -99, cps=1e9, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
            h.emitir(C.rect(1200, y, 600 * v * a, 60), 0.9, col=h.pal["verde"] if i == 0 else h.pal["neon"], blur=2)
            h.pieza(C.rect(1200, y, 600, 60), 40, 8830 + i, w=3, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, rampa="piedra", alfa=0.35, linea=True)
            if a > 0.3:
                N.texto_maquina(h, f"{int(v * 100 * a)} %", 1830, y + 30, 40, t, -99, cps=1e9, tono=0.95, centro=False, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["luna"], k=0.6, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "FRÍA PRECISIÓN ESTADÍSTICA", 960, 1000, 52, t, self.t_fria - 0.1, sem=55, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=248), bloom=0.9)

    # ------------------------------------------------------------------ I. la mentira pesa más
    def p_balanza(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[8]
        h.camara(1.0 + 0.08 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("cuero", 8900), h, 1.0, rampa="madera", oscuro=0.8)
        incl = e_out(clamp01((t - self.t_mentira - 0.3) / 1.2)) + 0.05 * math.sin(t * 2.0) * (1 - e_out(clamp01((t - self.t_mentira) / 1.0)))
        pl, pr = K.balanza(h, 960, 130, incl, 1.15, sem=8910)
        # a la derecha: la mentira (monedas); a la izquierda: la honestidad (una pluma)
        for j in range(9):
            P.ficha_juego  # (no usado; las monedas son discos de latón)
            h.pieza(elipse_(pr[0] - 90 + (j % 3) * 90, pr[1] - 24 - (j // 3) * 22, 52, 14, n=16), 150 + 6 * j, 8920 + j, w=3, luz=(0.3, -1), d=4, trama=0.2,
                    rim=0.9, rampa="laton")
        h.pieza(suave([(pl[0] - 60, pl[1] - 20), (pl[0], pl[1] - 70), (pl[0] + 70, pl[1] - 24), (pl[0], pl[1] - 12)], 4), 220, 8930, w=3, luz=(0.3, -1), d=4,
                trama=0.2, rim=0.9, rampa="papel")
        N.texto_maquina(h, "MENTIRA", pr[0], pr[1] - 150, 62, t, self.t_mentira, cps=14, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        N.texto_maquina(h, "HONESTIDAD", pl[0], pl[1] - 150, 62, t, self.t_honest - 0.3, cps=14, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        dx, dy = C.temblor(t, [(self.t_mentira + 0.9, 10)])
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "LA MENTIRA ESTRATÉGICA RENDÍA MÁS", 960, 1000, 42, t, self.t_mentira, sem=56, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=249), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "zumbido_servidores", 0.25, 0.0, dur=6.0)
        self.ev(tb[1] + 0.3, "tecla", 0.3, 0.0)
        self.ev(self.t_circ + 0.1, "electricidad", 0.45, 0.0, dur=0.9)
        self.ev(self.t_apoyo - 0.2, "sobre_desliza", 0.4, 0.0)
        self.ev(self.t_tres - 0.4, "papel_atrapa", 0.4, 0.0)
        self.ev(self.t_fra + 1.0, "sello_golpe", 0.6, 0.0)
        self.ev(self.t_enemigo + 0.7, "ficha", 0.5, 0.0)
        self.ev(tb[5] + 0.4, "multitud", 0.35, 0.0, dur=3.0)
        self.ev(tb[6] + 0.3, "lupa", 0.3, 0.0)
        self.ev(tb[7] + 0.3, "datos", 0.35, 0.0, dur=5.0)
        self.ev(self.t_mentira + 0.9, "golpe_grave", 0.6, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
