# -*- coding: utf-8 -*-
"""Escena 3 «tareas»: RUEDA DE PRENSA (un ingeniero en el atril, fotógrafos en primer plano, flashes) · sobre una mesa de metal
caen las TAREAS y un sello rojo las marca «SIN SOLUCIÓN» una a una · detrás de la puerta: un SOLDADOR la sella con un chorro de
chispas mientras desde dentro la copia tira y la puerta tiembla · CELDA CON VENTANUCO: el sol y la luna pasan, la copia sigue
intentando y en la pared crecen las rayas de los días · el CANDADO IMPOSIBLE (la cámara gira alrededor de la copia que «carga») ·
primer plano: los ojos dejan el candado y se van a la pared · la luz de su pantalla barre los ladrillos y encuentra la GRIETA."""
import math

import numpy as np

import comun as C
import mundos_1 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
import kit27 as K
from toon import Pista, pulso, elipse_, suave


def local(x, y, s, d, wx, wy, g=1.0):
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


def flash_cam(t, sem, ritmo=1.3):
    """Destellos de cámara de un fotógrafo (0..1), a su ritmo."""
    rng = np.random.default_rng(sem)
    per = rng.uniform(1.4, 2.6) / ritmo
    fase = rng.uniform(0, per)
    u = (t + fase) % per
    return math.exp(-u * 14) if u < 0.4 else 0.0


class Tareas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=3, num="0417")
        self.ing = Figura(sem=91)
        self.sold = Figura(sem=93)
        self.t_detalle = w("detalle")
        self.t_ruedas = w("ruedas")
        self.t_muchas = w("muchas")
        self.t_soluc = w("solución")
        self.t_pidieron = w("pidieron")
        self.t_soldado = w("soldado")
        self.t_detras = w("detrás")
        self.t_dias = w("días")
        self.t_encierra = w("Encierra")
        self.t_imposible = w("imposible")
        self.t_deja = w("deja")
        self.t_candado = w("candado")
        self.t_estudiar = w("estudiar")
        self.t_paredes = w("paredes")
        self.tb = [t0, self.t_muchas - 0.45, self.t_pidieron - 0.45, w("algunas") - 0.4, self.t_encierra - 0.45,
                   w("Tarde") - 0.35, self.t_estudiar - 0.6]
        tb = self.tb
        self.plano(tb[0], self.p_prensa, pal="sodio")
        self.plano(tb[1], self.p_tareas, tr="barrido", dur=0.45, dirx=1, pal="bourbon")
        self.plano(tb[2], self.p_soldador, tr="relampago", dur=0.4)
        self.plano(tb[3], self.p_dias, tr="humo", dur=0.6)
        self.plano(tb[4], self.p_candado, tr="tinta", dur=0.6)
        self.plano(tb[5], self.p_ojos, tr="empuje", dur=0.45, centro=(W * 0.5, H * 0.5))
        self.plano(tb[6], self.p_grieta, tr="barrido", dur=0.45, dirx=-1)

    # ------------------------------------------------------------------ A. rueda de prensa
    def p_prensa(self, h, t, u):
        k = smooth(clamp01(u / 4.5))
        h.camara(1.0 + 0.06 * k, 960, 500, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_prensa(), h, 1.0, rampa="vino")
        gest = 0.5 + 0.5 * math.sin(t * 2.3)
        self.ing.dibujar(h, dict(x=960, y=760, s=0.95, d=1, bata=True, gafas=True, brazo=0.4 * gest, cabeza=0.4 * math.sin(t * 0.9),
                                 luz=(0.2, -1.0)))
        h.pieza(C.rect(860, 380, 200, 290), 70, 20, w=5, luz=(0.3, -1), d=8, trama=0.4, rim=0.7, rampa="madera")       # atril
        h.pieza(C.rect(830, 360, 260, 34), 96, 21, w=4, luz=(0.3, -1), d=4, trama=0.2, rim=0.8, rampa="madera")
        for k_, (dx, a) in enumerate(((-50, -0.3), (0, 0.0), (50, 0.3))):                       # micrófonos
            p0 = (960 + dx * 0.4, 360)
            p1 = (960 + dx + 30 * math.sin(a), 260)
            h.trazo(np.array([p0, p1]), 5, 30 + k_, jit=0.2, taper=(0, 0))
            h.pieza(elipse_(p1[0], p1[1], 14, 20, n=14), 40, 33 + k_, w=2.5, luz=(0.3, -1), d=3, trama=0, rim=0.8, rampa="piedra")
        fl = 0.0
        for i in range(7):                                                  # fotógrafos de espaldas, primer plano
            x = 80 + i * 300 + 40 * math.sin(i * 2.1)
            f = flash_cam(t, 70 + i)
            fl = max(fl, f)
            K.persona(h, x, 1220, 1.15 + 0.1 * (i % 2), sem=100 + i * 5, tono=16, bal=6 * math.sin(t + i), brazo=0.5, sombrero=i % 3 != 0,
                      rim=0.8)
            cx_, cy_ = x + 60, 1220 - 1.2 * 520
            h.pieza(C.rect(cx_ - 40, cy_ - 30, 80, 60), 24, 150 + i, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.7, rampa="piedra")
            h.pieza(C.rect(cx_ - 30, cy_ - 80, 60, 46), 200, 160 + i, w=2.5, luz=(0.3, -1), d=2, trama=0, rim=0.4, rampa="papel")
            if f > 0.05:
                h.emitir(C.rect(cx_ - 26, cy_ - 76, 52, 38), 2.0 * f, col=(1, 1, 1), blur=3)
                h.resplandor(cx_, cy_ - 57, 340, 0.8 * f, col=(1, 0.95, 0.85))
                h.luz_radial(cx_, cy_ - 57, 1400, (1.0, 0.95, 0.9), k=1.2 * f)
        C.ambiente(h, 0.55)
        h.luz_cono(960, -300, math.pi / 2, 0.4, 1400, h.pal["sodio"], k=1.8, suave=0.5)
        h.luz_radial(960, 300, 900, h.pal["lampara"], k=0.5)
        C.cinta(h, "RUEDA DE PRENSA · LO QUE NO SE DIJO", 90, 120, 32, t, self.t_ruedas, sem=3)
        return h.acabado(t, niebla=dict(dens=0.12, sem=21), flash=0.25 * fl, bloom=0.6)

    # ------------------------------------------------------------------ B. tareas sin solución
    def p_tareas(self, h, t, u):
        k = smooth(clamp01(u / 4))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.02 - 0.02 * k)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 5), h, 1.0, rampa="piedra")
        pos = [(520, 330, -0.12), (960, 300, 0.05), (1400, 340, 0.1), (560, 740, 0.08), (1000, 760, -0.06), (1430, 720, -0.1)]
        for i, (x, y, a) in enumerate(pos):
            tk = self.tb[1] + 0.15 + i * 0.28
            e = e_out(clamp01((t - tk) / 0.35))
            if e <= 0:
                continue
            xx = x + (1 - e) * (-900 if i % 2 else 900)
            P.sobre(h, xx, y, 0.95, ang=a + (1 - e) * 0.8, sem=40 + i * 10, texto=f"TAREA {137 + i * 23}", t=t)
            ts = self.t_soluc - 0.15 + i * 0.16
            if t >= ts:
                N.sello(h, "SIN SOLUCIÓN", x, y + 10, 42, t, ts, rot=-12 + 5 * (i % 3), tono=np.array(h.pal["sello"]), alfa=0.95)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 500, 1300, h.pal["lampara"], k=1.2)
        return h.acabado(t, bloom=0.4)

    # ------------------------------------------------------------------ C. soldada por detrás
    def p_soldador(self, h, t, u):
        k = smooth(clamp01(u / 4.5))
        tira = max(0.0, math.sin(t * 9)) * (1 if t > self.tb[2] + 0.8 else 0)
        dx, dy = C.temblor(t, [(self.t_soldado + 0.3, 5)])
        h.camara(1.0 + 0.1 * k, 960 + dx, 500 + dy, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.pasillo_servicio(), h, 1.0, rampa="piedra")
        # la puerta de acero (vista por detrás): tiembla cuando la copia tira desde dentro
        sx = 4 * tira
        h.pieza(C.rect(600 + sx, 80, 740, 820), 70, 10, w=6, luz=(0.4, -1), d=12, trama=0.4, rim=0.7, rampa="piedra")
        for yy in (200, 480, 760):
            h.pieza(C.rect(620 + sx, yy, 700, 36), 90, 11 + yy, w=3, luz=(0.4, -1), d=4, trama=0.2, rim=0.8, rampa="piedra")
        # el cordón de soldadura que avanza por el canto de la puerta
        f = clamp01((t - self.tb[2] - 0.4) / 4.0)
        y_s = 900 - 820 * f
        h.pieza(C.rect(1330 + sx, y_s, 22, 900 - y_s), 120, 30, w=2, luz=(0.4, -1), d=2, trama=0, rim=0.9, rampa="whisky")
        h.emitir(C.rect(1334 + sx, y_s, 14, min(60, 900 - y_s)), 1.0, col=h.pal["sodio"], blur=3)
        # el soldador con careta
        self.sold.dibujar(h, dict(x=1560, y=980, s=0.95, d=-1, tono=50, brazo=0.85, cabeza=0.0, luz=(-0.6, -1.0)))
        careta = np.array([(1500, 470), (1580, 470), (1586, 540), (1500, 548)], float)
        h.pieza(careta, 30, 40, w=4, luz=(-0.6, -1), d=6, trama=0.3, rim=0.8, rampa="piedra")
        h.pieza(np.array([(1508, 490), (1540, 490), (1540, 506), (1508, 506)], float), 20, 41, w=2, d=1, sombra=0, trama=0, rim=0,
                rampa="vidrio_verde")
        h.trazo(np.array([[1480, 650], [1360, y_s + 10]]), 10, 42, jit=0.2, taper=(0, 0.2))
        C.chispas(h, t, 1345, y_s, self.tb[2] + 0.4, dur=6.0, n=40, vel=560, sem=8, continuo=True, ang=math.pi * 0.9, abre=1.8)
        arco = 0.7 + 0.3 * math.sin(t * 60) * math.sin(t * 23)
        h.resplandor(1345, y_s, 120, 1.0 * arco, col=(0.85, 0.95, 1.0))
        C.ambiente(h, 0.25)
        h.luz_radial(1345, y_s, 1500, (0.8, 0.9, 1.0), k=1.4 * arco)
        h.luz_radial(960, -200, 1400, h.pal["lampara"], k=0.25)
        C.banda(h, "SOLDADAS POR DETRÁS", 700, 980, 56, t, self.t_detras, sem=5)
        return h.acabado(t, niebla=dict(dens=0.18, sem=22, vel=14), bloom=0.8)

    # ------------------------------------------------------------------ D. días enteros
    def p_dias(self, h, t, u):
        h.camara(1.0 + 0.04 * u / 5, 960, 520, 0.0)
        ciclo = (t - self.tb[3]) / 1.6                                    # un día cada 1,6 s
        dia = 0.5 + 0.5 * math.sin(ciclo * 2 * math.pi)
        h.rim_color(h.pal["sodio"] if dia > 0.5 else h.pal["luna"])
        NC.pegar(M.celda_ventana(), h, 1.0, rampa="ladrillo")
        # el astro cruza el ventanuco (sol de día, luna de noche)
        fa = (ciclo % 1.0)
        ax = 700 + 380 * fa
        ay = 30 - 120 * math.sin(math.pi * fa)
        with h.capa(1.0):
            if dia > 0.5:
                h.emitir(elipse_(ax, ay, 26, 26, n=20), 1.4, col=h.pal["sodio"], blur=3)
            else:
                h.emitir(elipse_(ax, ay, 20, 20, n=20), 1.0, col=h.pal["luna"], blur=2)
        # rayas de los días en la pared (crecen)
        n = int(3 + ciclo)
        for i in range(n):
            x = 160 + (i % 5) * 22 + (i // 5) * 140
            if i % 5 == 4:
                h.trazo(np.array([[x - 92, 300], [x + 4, 380]]), 5, 60 + i, color=tuple(h.c(220, "papel")), jit=0.4)
            else:
                h.trazo(np.array([[x, 290], [x + 3, 390]]), 5, 60 + i, color=tuple(h.c(220, "papel")), jit=0.4)
        # la copia, contra la puerta (a la derecha), sigue tirando y golpeando
        tira = math.sin(t * 5)
        h.pieza(C.rect(1560, 40, 360, 860), 60, 80, w=6, luz=(0.4, -1), d=10, trama=0.4, rim=0.7, rampa="piedra")
        h.pieza(elipse_(1590, 470, 18, 18, n=14), 150, 81, w=3, luz=(0.4, -1), d=3, trama=0, rim=0.9, rampa="laton")
        self.cop.perfil(h, dict(x=1330, y=M.Y_SUELO, s=1.0, d=1, mano=(250, -430 + 10 * tira), mano2=(220, -420 - 10 * tira),
                                inclina=-0.1 + 0.05 * tira, cara=dict(expr="carga" if dia < 0.5 else "neutro", mira=0.8)))
        C.ambiente(h, 0.32 + 0.2 * dia)
        h.luz_radial(350, 340, 500, h.pal["lampara"], k=0.5)
        col = np.array(h.pal["sodio"]) * dia + np.array(h.pal["luna"]) * (1 - dia)
        h.luz_persiana([(700, -120), (1080, -120), (1260 + 300 * (fa - 0.5), 900), (500 + 300 * (fa - 0.5), 900)], k=1.4,
                       tipo="persiana", n=6, abierto=0.75, col=col)
        C.banda(h, "DÍAS ENTEROS PARA INTENTARLO", 960, 980, 54, t, self.t_dias, sem=6)
        N.motas(h, t, n=60, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, sem=23), bloom=0.5)

    # ------------------------------------------------------------------ E. el candado imposible
    def p_candado(self, h, t, u):
        a = 0.06 * math.sin(u * 0.5) - 0.03
        h.camara(1.05 + 0.04 * u / 5, 960 + 60 * math.sin(u * 0.4), 480, a)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_puerta(), h, 1.0, rampa="ladrillo")
        P.candado(h, 960, 560, 1.9, abierto=0.0, sem=30, brillo_ojo=0.3)
        h.pieza(C.rect(870, 400, 180, 40), 70, 31, w=4, luz=(0.3, -1), d=4, trama=0.2, rim=0.8, rampa="piedra")
        self.cop.perfil(h, dict(x=600, y=M.Y_SUELO + 40, s=1.05, d=1, brazos="libre", cara=dict(expr="carga" if t < self.t_imposible else
                                                                                                    "error", mira=1.0), inclina=0.05))
        C.ambiente(h, 0.4)
        h.luz_radial(560, 300, 600, h.pal["verde"], k=0.6)
        h.luz_radial(960, 560, 600, h.pal["verde"], k=0.5)
        h.luz_cono(960, -300, math.pi / 2, 0.3, 1500, h.pal["luna"], k=1.3, suave=0.6)
        C.banda(h, "UN PROBLEMA IMPOSIBLE", 960, 120, 58, t, self.t_imposible, sem=7)
        return h.acabado(t, niebla=dict(dens=0.1, sem=24), bloom=0.5)

    # ------------------------------------------------------------------ F. deja de mirar el candado
    def p_ojos(self, h, t, u):
        h.camara(1.0 + 0.05 * u / 4, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_puerta(), h, 0.4, rampa="ladrillo", bruma=0.3, oscuro=0.7)
        f = smooth(clamp01((t - self.t_deja - 0.2) / 1.2))
        mira = 0.95 * (1 - f) - 0.9 * f
        my = -0.5 * f
        self.cop.cabeza(h, 1020, 560, 3.6, dict(expr="neutro", mira=mira, mira_y=my), d=-1, luz=(0.5, -1.0), rim=0.9)
        # el reflejo del candado en el vidrio de la pantalla (se va cuando aparta la vista)
        with h.capa(1.0):
            P.candado(h, 1520, 640, 0.9, sem=32, brillo_ojo=0.2)
        C.ambiente(h, 0.28)
        h.luz_radial(1500, 640, 600, h.pal["verde"], k=0.6 * (1 - f))
        h.luz_radial(300, 200, 900, h.pal["luna"], k=0.6 * f)
        return h.acabado(t, niebla=dict(dens=0.06, sem=25), bloom=0.5)

    # ------------------------------------------------------------------ G. la grieta
    def p_grieta(self, h, t, u):
        k = smooth(clamp01((t - self.t_paredes) / 2.5))
        h.camara(1.0 + 0.35 * k, 960 + 180 * k, 520 - 40 * k, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.pared_grieta(), h, 1.0, rampa="ladrillo")
        # la grieta: línea quebrada que se dibuja; brilla por dentro
        r = np.random.default_rng(5)
        pts = [(1180.0, 120.0)]
        for i in range(14):
            x, y = pts[-1]
            pts.append((x + r.uniform(-40, 40), y + r.uniform(40, 70)))
        g = clamp01((t - self.t_paredes + 0.3) / 1.2)
        n = max(2, int(len(pts) * g))
        Q = np.array(pts[:n])
        if g > 0:
            h.trazo(Q, 9, 70, color=tuple(h.c(8, "piedra")), jit=0.6, taper=(0.3, 0.3))
            h.emitir(np.vstack([Q + (-2, 0), (Q + (2, 0))[::-1]]), 0.9 * g, col=h.pal["verde"], blur=2)
            for p_ in Q[::3]:
                h.resplandor(p_[0], p_[1], 70, 0.25 * g, col=h.pal["verde"])
        # la copia de espaldas en primer plano, su pantalla como linterna
        with h.capa(0.0):
            RP.espalda(h, 330, 1480, 1.7, t, sem=21, sentado=False, luz=(0.8, -0.6), rim=0.9, cab_rot=0.12)
        sx = 700 + 520 * smooth(clamp01((t - self.tb[6]) / 2.2)) + 40 * math.sin(t * 1.3)
        C.ambiente(h, 0.2)
        h.luz_radial(sx, 420, 460, h.pal["verde"], k=1.8)
        h.luz_radial(1180, 500, 500, h.pal["verde"], k=0.6 * g)
        C.banda(h, "Y EMPIEZA A ESTUDIAR LAS PAREDES", 960, 980, 50, t, self.t_estudiar, sem=8)
        N.motas(h, t, n=60, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.08, sem=26), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "multitud", 0.25, 0.0, dur=tb[1] - tb[0])
        self.ev(tb[0] + 0.6, "fotos", 0.6, -0.3)
        self.ev(tb[0] + 2.1, "fotos", 0.5, 0.4)
        self.ev(tb[1] + 0.2, "sobre_desliza", 0.6, 0.0, dur=1.6)
        self.ev(self.t_soluc - 0.15, "sello_golpe", 0.8, 0.0)
        self.ev(tb[2] + 0.4, "electricidad", 0.55, 0.3, dur=4.0)
        self.ev(tb[2] + 1.0, "golpe_grave", 0.5, -0.3)
        self.ev(tb[3] + 0.2, "crecer", 0.35, 0.0, dur=3.5)
        self.ev(tb[4] + 0.2, "grave_inquietante", 0.45, 0.0, dur=3.0)
        self.ev(self.t_deja + 0.2, "servo", 0.35, 0.0)
        self.ev(self.t_paredes, "sombra_crece", 0.5, 0.2, dur=2.5)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
