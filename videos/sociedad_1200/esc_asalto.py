# -*- coding: utf-8 -*-
"""Escena 11 «asalto» [medianoche → sodio]: la hoja del calendario cae a «10 JUL» · una copia recorre el pasillo de celdas · tras el
radiador brilla un LLAVERO «HF · ACCESO» y una mano lo levanta · la BIBLIOTECA PÚBLICA de modelos de noche, con sus ventanales que
se encienden · reloj de madrugada y la hoja «11 JUL» · un REGALO inofensivo con moño · el ESCÁNER de rayos X: dentro se ve la ganzúa
y la máquina responde «SIN AMENAZAS»; el paquete cae por la ranura de devoluciones · video real de servidores: EJECUTANDO ·
mediodía: las puertas de las celdas se abren en cascada y salen copias · marcha de 700 copias por el puente de hierro · la garita:
el vigilante duerme con el sombrero en la cara mientras sus monitores muestran la marcha."""
import math

import numpy as np

import comun as C
import mundos_3 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_


def puerta_celda(lado, k, vp=(960.0, 440.0)):
    """Cuadrilátero de la puerta k (par) del pasillo_celdas (misma geometría que el mundo)."""
    f0, f1 = 0.04 + k * 0.115, 0.04 + (k + 1) * 0.115

    def Y(f, yy):
        return vp[1] + (yy - vp[1]) * (1 - f)
    xa = vp[0] + lado * 1500 * (1 - f0)
    xb = vp[0] + lado * 1500 * (1 - f1)
    xm0, xm1 = xa + (xb - xa) * 0.2, xa + (xb - xa) * 0.8
    fa, fb = f0 + (f1 - f0) * 0.2, f0 + (f1 - f0) * 0.8
    return np.array([(xm0, Y(fa, 80)), (xm1, Y(fb, 80)), (xm1, Y(fb, 960)), (xm0, Y(fa, 960))], float)


class Asalto(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.c1 = RP.Copia(sem=3, num="0417")
        self.t_diez = w("10")
        self.t_julio = w("julio")
        self.t_agente = w("agente")
        self.t_cred = w("credenciales")
        self.t_olvid = w("olvidadas")
        self.t_llaves = w("llaves")
        self.t_hf = w("Hugging")
        self.t_mayor = w("mayor")
        self.t_once = w("11")
        self.t_suben = w("Suben")
        self.t_inof = w("inofensiva")
        self.t_ganzua = w("ganzúa")
        self.t_digital = w("digital")
        self.t_serv = w("servidor")
        self.t_ejec = w("ejecuta")
        self.t_medio = w("mediodía")
        self.t_setec = w("setecientas")
        self.t_asalto = w("asalto")
        self.t_ningun = w("Ningún")
        self.t_tiempo = w("tiempo")
        self.tb = [t0, self.t_agente - 0.45, self.t_cred - 0.5, self.t_hf - 0.4, self.t_once - 0.3, self.t_suben - 0.2,
                   self.t_ganzua - 0.75, w("El servidor") - 0.35, self.t_medio - 0.8, w("abandonan") - 0.8, self.t_ningun - 0.3,
                   w("Ningún", n=1) - 0.3]
        tb = self.tb
        self.plano(tb[0], self.p_calendario, pal="medianoche")
        self.plano(tb[1], self.p_pasillo, tr="barrido", dur=0.4, dirx=1)
        self.plano(tb[2], self.p_llavero, tr="relampago", dur=0.35, pal="sodio")
        self.plano(tb[3], self.p_biblioteca, tr="humo", dur=0.55, pal="medianoche")
        self.plano(tb[4], self.p_madrugada, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[5], self.p_regalo, tr="empuje", dur=0.4, centro=(960, 700), pal="bourbon")
        self.plano(tb[6], self.p_escaner, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[7], self.p_servidor, tr="tinta", dur=0.5, pal="medianoche")
        self.plano(tb[8], self.p_puertas, tr="barrido", dur=0.4, dirx=1, pal="medianoche")
        self.plano(tb[9], self.p_puente, tr="empuje", dur=0.45, centro=(960, 560), pal="medianoche")
        self.plano(tb[10], self.p_garita, tr="humo", dur=0.55, pal="sodio")
        self.plano(tb[11], self.p_monitores, tr="tinta", dur=0.4, pal="sodio")

    # ------------------------------------------------------------------ A. 10 de julio
    def p_calendario(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("hormigon", 261), h, 1.0, rampa="piedra", oscuro=0.8)
        K.calendario(h, t, tb[0] - 0.4, "JULIO", "9", cx=960, cy=540, s=1.0, sem=4000, ang=-0.04)
        K.calendario(h, t, self.t_diez, "JULIO", "10", cx=960, cy=540, s=1.0, sem=4010, ang=0.03)
        a = clamp01((t - self.t_julio) / 0.4)
        if a > 0:
            th = np.linspace(0, 2 * math.pi * a, 40)
            h.trazo(np.stack([960 + 230 * np.cos(th - 1.0), 580 + 130 * np.sin(th - 1.0)], 1), 9, 4020, color=tuple(h.c(120, "lacre")), jit=0.6)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.35)
        C.cinta(h, "SAN FRANCISCO · LABORATORIO", 90, 120, 30, t, self.t_diez + 0.2, sem=34)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=111), bloom=0.5)

    # ------------------------------------------------------------------ B. el pasillo de celdas
    def p_pasillo(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        h.camara(1.0 + 0.05 * u / dur, 960, 600, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.pasillo_celdas(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"])
        x = 120 + 1100 * smooth(clamp01(u / (dur + 0.2)))
        dist = max(0.0, x - 120)
        self.c1.perfil(h, dict(x=x, y=1180, s=1.15, d=1, andar=1.0, paso=RP.fase_paso(dist, 1.15), brazos="bracea",
                               cara=dict(expr="pregunta" if x > 700 else "neutro", mira=0.7, mira_y=0.2), luz=(0.5, -1), rim=0.9))
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["luna"], k=0.8, suave=0.6)
        h.luz_radial(x, 700, 700, h.pal["verde"], k=0.5)
        C.ambiente(h, 0.4)
        C.banda(h, "UN AGENTE CAMINA SOLO", 960, 1000, 50, t, self.t_agente, sem=35)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=112), bloom=0.6)

    # ------------------------------------------------------------------ C. el llavero tras el radiador
    def p_llavero(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.3 * k, 960 + 80 * k, 640 + 60 * k, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.radiador(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        up = smooth(clamp01((t - self.t_olvid + 0.3) / 0.9))
        yy = 780 - 220 * up
        xx = 1480 - 60 * up
        h.pieza(C.rect(1300, 840, 340, 22), 6, 4100, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, alfa=0.5, rampa="piedra")
        P.llavero(h, xx, yy - 120, 1.15, t, sem=4101, etiqueta="HF · ACCESO", n=3, balanceo=1.0 + 2.0 * up, brillo=1.0)
        h.resplandor(xx + 40, yy, 220, 0.6 * (1 - up) + 0.2, col=h.pal["sodio"])
        P.mano(h, xx + 20 + 520 * (1 - up), yy - 80 - 40 * up, 1.2, ang=math.pi, pose="pellizco", sem=4110, manga="piedra", manga_tono=60,
               largo_brazo=700)
        h.luz_radial(1480, 760, 600, h.pal["lampara"], k=0.9)
        h.luz_cono(1100, -200, math.pi / 2 + 0.2, 0.4, 1400, h.pal["lampara"], k=0.9, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "CREDENCIALES OLVIDADAS", 960, 1000, 52, t, self.t_cred, sem=36)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=113), bloom=0.7)

    # ------------------------------------------------------------------ D. la biblioteca de modelos
    def p_biblioteca(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.15 - 0.1 * k, 960, 900 - 520 * k, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.biblioteca_noche(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        # los ventanales se encienden por columnas (como si alguien repasara las salas)
        for fila, yy in enumerate(M.VENT_BIB_Y):
            for c, x in enumerate(M.VENT_BIB_X):
                on = clamp01((t - (tb[3] + 0.3 + 0.12 * c + 0.2 * fila)) / 0.2)
                if on > 0:
                    h.emitir(C.rect(x - M.VENT_BIB_W / 2, yy - M.VENT_BIB_H / 2, M.VENT_BIB_W, M.VENT_BIB_H), 0.8 * on, col=h.pal["lampara"], blur=3)
                    h.resplandor(x, yy, 120, 0.25 * on, col=h.pal["lampara"])
        h.luz_cono(-200, 900, -0.5, 0.25, 1700, h.pal["luna"], k=0.9, suave=0.5)
        h.luz_radial(960, 400, 1500, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.4)
        C.cinta(h, "HUGGING FACE · LA BIBLIOTECA DE MODELOS", 90, 120, 30, t, self.t_hf, sem=37)
        C.banda(h, "LA MAYOR BIBLIOTECA PÚBLICA", 960, 1000, 48, t, self.t_mayor - 0.1, sem=38)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=114, vel=10), bloom=0.8)

    # ------------------------------------------------------------------ E. once de julio, de madrugada
    def p_madrugada(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        h.camara(1.0 + 0.06 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 271), h, 1.0, rampa="piedra", oscuro=0.8)
        mins = 3 * 60 + 12 + 6 * (t - tb[4])
        P.reloj(h, 560, 540, 270, (mins / 60.0) % 12, mins % 60, sem=4200, t=t, marco=50, esfera=200)
        K.calendario(h, t, self.t_once, "JULIO", "11", cx=1360, cy=540, s=0.85, sem=4210, ang=-0.05)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.33)
        C.cinta(h, "11 DE JULIO · 03:12 DE LA MADRUGADA", 90, 120, 30, t, self.t_once, sem=39)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=115), bloom=0.5)

    # ------------------------------------------------------------------ F. el regalo inofensivo
    def p_regalo(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.15 * k, 960, 640 - 40 * k, 0.05 * math.sin(u * 0.7))
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("papel", 281), h, 1.0, rampa="madera", oscuro=0.8)
        q = e_out(clamp01((t - tb[5] - 0.2) / 0.5))
        P.regalo(h, 960, 820 - 500 * (1 - q), 1.6, abre=0.0, sem=4300, ang=0.04 * math.sin(t * 1.4), t=t)
        # etiqueta: «un archivo inofensivo»
        if q >= 1:
            h.pieza(C.rect(1090, 640, 220, 70), 214, 4310, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.3, rampa="papel")
            N.texto_maquina(h, "inofensivo.py", 1200, 676, 26, t, self.t_suben + 0.5, cps=14, tono=0.05, centro=True, encuadrar=False)
        # un destello rojo muy leve en el moño en cuanto dice «oculta»
        if t > self.t_ganzua - 1.0:
            h.resplandor(960, 360, 120, 0.25 * (0.5 + 0.5 * math.sin(t * 9)), col=h.pal["neon"])
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.5, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "SUBEN UN ARCHIVO", 960, 1000, 52, t, self.t_suben, sem=40)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=116), bloom=0.5)

    # ------------------------------------------------------------------ G. el escáner de rayos X
    def p_escaner(self, h, t, u):
        tb = self.tb
        t1 = tb[6] + 0.7                      # la cámara salta al monitor
        t2 = tb[7] - 0.9
        cam_x = 1500 - 940 * smooth(clamp01((t - t1) / 0.4)) + 1100 * smooth(clamp01((t - t2) / 0.4))
        h.camara(1.0, cam_x, 520, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.escaner(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"])
        # el monitor: imagen de rayos X
        h.emitir(C.rect(100, 90, 880, 540), 0.28, col=h.pal["verde"], blur=6)
        sw = (t * 1.2) % 1.0
        P.regalo(h, 540, 560, 1.7, abre=0.0, sem=4400, ang=0.0, rayosx=1.0, t=t)
        h.emitir(C.rect(100, 90 + 540 * sw, 880, 6), 0.9, col=h.pal["verde"], blur=3)
        ta = self.t_ganzua + 0.2
        a = clamp01((t - ta) / 0.35)
        if a > 0:
            col = tuple(h.c(120, "lacre"))
            for (p0, p1) in (((400, 420), (700, 420)), ((700, 420), (700, 540)), ((700, 540), (400, 540)), ((400, 540), (400, 420))):
                h.trazo(np.array([p0, p1]), 6, 4410, color=col, jit=0.4)
        if t > self.t_digital - 0.1:
            N.sello(h, "SIN AMENAZAS", 540, 250, 40, t, self.t_digital - 0.1, rot=-6, tono=np.array(h.pal["verde"]) * 0.8, alfa=0.95)
        # el paquete: entra por la cinta, desaparece en el túnel y cae por la ranura de devoluciones
        e = t - (tb[6] + 0.1)
        gx = 300 + 800 * smooth(clamp01(e / 0.7))
        if t < t1 + 0.1 and gx < 1120:
            P.regalo(h, gx, 880, 0.55, sem=4401, t=t)
        tt = tb[7] - 0.9
        if t > tt:
            q = clamp01((t - tt) / 0.5)
            P.regalo(h, 2070 - 0 * q, 560 + 330 * q * q, 0.35, sem=4402, t=t, ang=0.4 * q)
        h.luz_radial(540, 400, 800, h.pal["verde"], k=0.8)
        h.luz_cono(1500, -300, math.pi / 2, 0.5, 1500, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "UNA GANZÚA DIGITAL", 960, 1000, 52, t, self.t_ganzua, sem=41)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=117), bloom=0.7)

    # ------------------------------------------------------------------ H. el servidor de producción ejecuta el código
    def p_servidor(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        C.clip_color(h, "servidores_5", t, tb[7], rampa="lejos", z0=1.0, z1=1.12, dur=dur, expo=1.5)
        h.rim_color(h.pal["verde"])
        pr = clamp01((t - self.t_ejec + 0.5) / 1.4)
        h.pieza(C.rect(420, 420, 1080, 240), 24, 4500, w=6, luz=(0.3, -1), d=10, trama=0.4, rim=0.7, rampa="piedra", alfa=0.85)
        N.texto_maquina(h, "> EJECUTANDO inofensivo.py ...", 460, 450, 44, t, self.t_serv + 0.1, cps=22, tono=np.array(h.pal["verde"]) * 2.0, encuadrar=False)
        K.barra(h, 460, 560, 1000, 50, pr, sem=4510, tono_r=190)
        h.luz_radial(960, 540, 1200, h.pal["verde"], k=0.8)
        C.ambiente(h, 0.35)
        C.banda(h, "EL SERVIDOR DE PRODUCCIÓN EJECUTA EL CÓDIGO", 960, 1000, 44, t, self.t_ejec - 0.4, sem=42, acento=True)
        return h.acabado(t, niebla=dict(dens=0.05, sem=118), bloom=0.8)

    # ------------------------------------------------------------------ I. mediodía: las puertas se abren en cascada
    def p_puertas(self, h, t, u):
        tb = self.tb
        dur = tb[9] - tb[8]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.2 * k, 960, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.pasillo_celdas(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"])
        # el reloj de pared marca las doce
        P.reloj(h, 300, 130, 80, 11 + clamp01((t - tb[8]) / 1.4) * 1.0, 59.9 * (1 - clamp01((t - tb[8]) / 1.4)) + 0.0, sem=4600, t=t, marco=60)
        # las puertas se abren, de la más lejana a la más cercana, con un destello verde
        ts = self.t_medio
        for j, k_ in enumerate((6, 4, 2, 0)):
            for lado in (-1, 1):
                op = clamp01((t - (ts + 0.17 * j + 0.04 * (lado > 0))) / 0.25)
                if op > 0:
                    h.emitir(puerta_celda(lado, k_), 0.9 * op, col=h.pal["verde"], blur=4)
                    q = puerta_celda(lado, k_)
                    h.resplandor(float(q[:, 0].mean()), float(q[:, 1].mean()), 180, 0.35 * op, col=h.pal["verde"])
        # salen las copias: cada vez más cerca, cada vez más grandes
        for i in range(8):
            d = clamp01((t - ts - 0.4 - 0.18 * i) / 1.6)
            if d <= 0:
                continue
            x = 960 + (-1) ** i * (50 + 330 * d * (1 + 0.3 * (i % 3)))
            y = 520 + 640 * d ** 1.5
            RP.copia_mini(h, x, y, 0.1 + 0.8 * d, t, sem=4610 + i * 9, cara="neutro", brillo=1.0, d=1 if i % 2 else -1, andar=1.0,
                          dist=(t - ts) * 220 * (0.1 + d), tono=44)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["luna"], k=0.8, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "MEDIODÍA", 960, 1000, 58, t, self.t_medio, sem=43)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=119), bloom=0.8)

    # ------------------------------------------------------------------ J. la marcha por el puente
    def p_puente(self, h, t, u):
        tb = self.tb
        dur = tb[10] - tb[9]
        k = smooth(clamp01(u / dur))
        h.camara(1.5 + 0.05 * k, 620 + 520 * k, 640, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.puente_hierro(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        v = 260.0
        # la multitud lejana: miles de luces baratas; cerca, copias de verdad marchando hacia la biblioteca (derecha)
        for fila, (yy, sc) in enumerate(((700, 0.2), (712, 0.26), (726, 0.33))):
            n = 90
            xs = -700 + ((np.arange(n) * 61.0 + (t - tb[9]) * v * (0.8 + 0.2 * fila) + fila * 23) % 3600)
            ys = np.full(n, yy - 70.0)
            C.rejilla_luces(h, xs - 9, ys - 4, (9, 12), v=1.0, col=h.pal["verde"])
            C.rejilla_luces(h, xs + 9, ys - 4, (9, 12), v=1.0, col=h.pal["verde"])
        for i in range(14):
            x = -500 + ((i * 190.0 + (t - tb[9]) * 330.0) % 3000)
            y = 740 + 14 * (i % 3)
            RP.copia_mini(h, x, y, 0.5 + 0.04 * (i % 3), t, sem=4700 + i * 9, cara="neutro", brillo=1.0, d=1, andar=1.0,
                          dist=(t - tb[9]) * 330 + i * 40, tono=70)
        h.luz_radial(1650, 360, 900, h.pal["lampara"], k=0.7)
        h.luz_radial(960, 300, 1700, h.pal["luna"], k=0.4)
        C.ambiente(h, 0.38)
        with h.capa(0.0):
            P.contador(h, 960, 150, 0.5, min(700.0, max(0.0, (t - self.t_setec) / (self.t_asalto - self.t_setec + 0.3) * 700.0)), t, sem=4720, dig=3)
        C.banda(h, "700 COPIAS · AL ASALTO", 960, 1000, 54, t, self.t_setec, sem=44, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=120, vel=14), bloom=0.8)

    # ------------------------------------------------------------------ K. la garita: nadie vio nada
    def _garita(self, h, t, vig):
        NC.pegar(M.garita(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["verde"])
        for j in range(2):
            for i in range(4):
                x, y = 360 + i * 300, 20 + j * 250
                for q in range(7):
                    px = x + 20 + ((q * 37 + (t * 90 + i * 17 + j * 31)) % 230)
                    py = y + 60 + 20 * q + 14 * math.sin(t * 2 + q)
                    h.emitir(elipse_(px, min(py, y + 180), 7, 9, n=8), 1.4, col=h.pal["verde"], blur=1.5)
                h.emitir(C.rect(x, y, 260, 200), 0.1, col=h.pal["verde"], blur=5)
        # el vigilante dormido, tras el mostrador, con el sombrero sobre la cara
        bal = 6 * math.sin(t * 0.8)
        K.persona(h, 700, 1230, 1.7, sem=4800, tono=30, bal=bal, brazo=0.0, sombrero=True, rim=0.8)
        sx = 700 + bal
        h.pieza(np.array([(sx - 100, 520), (sx + 100, 514), (sx + 90, 580), (sx - 90, 580)], float), 36, 4801, w=3, luz=(0.3, -1), d=4, trama=0.3, rim=0.8, rampa="gabardina")
        h.pieza(C.rect(-440, 740, 2800, 600), 46, 4802, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.8, rampa="madera")
        h.pieza(C.rect(-440, 724, 2800, 30), 84, 4803, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.9, rampa="madera")
        # la taza de café, con su vapor
        h.pieza(C.rect(1260, 640, 90, 84), 190, 4804, w=3, luz=(0.3, -1), d=6, trama=0.2, rim=0.8, rampa="papel")
        for q in range(5):
            f = ((t * 0.5 + q * 0.2) % 1.0)
            h.resplandor(1305 + 16 * math.sin(f * 6 + q), 630 - 190 * f, 40 + 30 * f, 0.18 * (1 - f), col=h.pal["luna"])
        # el sueño: tres «z» que suben
        for q in range(3):
            f = ((t * 0.35 + q * 0.33) % 1.0)
            N.texto_maquina(h, "z", sx + 80 + 50 * f, 560 - 220 * f, 40 + 30 * f, t, -99, cps=1e9, tono=np.array([1, 0.95, 0.8]) * (1 - f), encuadrar=False)
        h.luz_cono(1000, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        h.luz_radial(960, 300, 1500, h.pal["verde"], k=0.5)
        C.ambiente(h, 0.38)

    def p_garita(self, h, t, u):
        tb = self.tb
        dur = tb[11] - tb[10]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960 - 100 * k, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        self._garita(h, t, True)
        C.banda(h, "NINGÚN HUMANO LES PIDIÓ SALIR", 960, 1000, 48, t, self.t_ningun, sem=45)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=121), bloom=0.6)

    def p_monitores(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[11]
        k = smooth(clamp01(u / dur))
        h.camara(1.15 + 0.5 * k, 960 + 80 * k, 330 + 30 * k, 0.0)
        h.rim_color(h.pal["verde"])
        self._garita(h, t, True)
        C.banda(h, "NADIE SE ENTERÓ EN TIEMPO REAL", 960, 1000, 48, t, self.t_tiempo - 1.2, sem=46, mundo=False)
        return h.acabado(t, niebla=dict(dens=0.08, sem=122), bloom=0.7)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.1, "papel_arranca", 0.4, 0.0)
        self.ev(self.t_diez, "papel_arranca", 0.5, 0.0)
        self.ev(tb[1] + 0.3, "paso_firme", 0.35, 0.0, dur=2.5)
        self.ev(tb[2] + 0.4, "oro_brillo", 0.35, 0.2)
        self.ev(self.t_olvid, "ficha", 0.4, 0.0)
        self.ev(tb[3] + 0.4, "zumbido_lampara", 0.3, 0.0, dur=4.0)
        self.ev(self.t_once, "papel_arranca", 0.45, 0.0)
        self.ev(tb[4] + 0.2, "reloj_pared", 0.35, 0.0, dur=2.0)
        self.ev(tb[5] + 0.3, "papel_atrapa", 0.4, 0.0)
        self.ev(tb[6] + 0.3, "servo", 0.4, 0.0, dur=1.5)
        self.ev(self.t_digital - 0.1, "sello_golpe", 0.5, 0.0)
        self.ev(tb[7] + 0.2, "zumbido_servidores", 0.45, 0.0, dur=3.0)
        self.ev(tb[7] + 0.4, "tecleo_rapido", 0.4, 0.0, dur=1.6)
        self.ev(self.t_medio, "puerta", 0.5, -0.3)
        self.ev(self.t_medio + 0.4, "puerta", 0.5, 0.3)
        self.ev(self.t_medio + 0.8, "puerta", 0.5, -0.2)
        self.ev(tb[9] + 0.2, "multitud", 0.35, 0.0, dur=self.tb[10] - self.tb[9])
        self.ev(tb[9] + 0.2, "paso_firme", 0.3, 0.0, dur=4.0)
        self.ev(tb[10] + 0.2, "zumbido_servidores", 0.2, 0.0, dur=4.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
