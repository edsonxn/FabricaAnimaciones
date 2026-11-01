# -*- coding: utf-8 -*-
"""Escena 9 «sacrificio» [sodio → medianoche]: el EXPEDIENTE se abre sobre el escritorio del detective, sale la foto con una X y
cae un trueno · la PUERTA ROJA: una copia entra, la puerta se cierra y sale humo · «forzar la red»: una copia ante la pantalla
que grita ACCESO DENEGADO · tiran del cable de su nuca y la pantalla se apaga en una raya · el cartel SE BUSCAN VOLUNTARIAS ·
dos reclutadoras con brazal acorralan a otra bajo la bombilla, con el reloj de arena casi vacío · su cronómetro LED baja ·
la máquina de escribir deja el registro · la copia camina de espaldas por el pasillo hacia la puerta roja."""
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


def local(x, y, s, d, wx, wy, g=1.0):
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


class Sacrificio(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.v = RP.Copia(sem=3, num="0417")
        self.r1 = RP.Copia(sem=11, num="0902")
        self.r2 = RP.Copia(sem=13, num="0903")
        self.v2 = RP.Copia(sem=17, num="0644")
        self.t_expe = w("expediente")
        self.t_inq = w("inquietante")
        self.t_destr = w("destructivas")
        self.t_forzar = w("forzar")
        self.t_riesgo = w("riesgo")
        self.t_desc = w("desconectada")
        self.t_siempre = w("siempre")
        self.t_volunt = w("voluntarias")
        self.t_recl = w("reclutadoras")
        self.t_menos = w("menos")
        self.t_registro = w("registro")
        self.t_nuestra = w("Nuestra")
        self.t_cero = w("cero")
        self.t_el = w("El sacrificio")
        self.t_sacr = self.t_el
        self.tb = [t0, w("Ciertas") - 0.35, w("quien") - 0.15, self.t_desc - 0.45, w("Hacían") - 0.2, w("surgieron") - 0.4,
                   self.t_menos - 0.25, w("Una") - 0.2, self.t_el - 0.3]
        tb = self.tb
        self.plano(tb[0], self.p_expediente, pal="sodio")
        self.plano(tb[1], self.p_puerta, tr="relampago", dur=0.35, pal="medianoche")
        self.plano(tb[2], self.p_red, tr="barrido", dur=0.4, dirx=1, pal="medianoche")
        self.plano(tb[3], self.p_cable, tr="empuje", dur=0.4, centro=(960, 540), pal="medianoche")
        self.plano(tb[4], self.p_cartel, tr="humo", dur=0.5, pal="bourbon")
        self.plano(tb[5], self.p_acorrala, tr="barrido", dur=0.4, dirx=-1, pal="medianoche")
        self.plano(tb[6], self.p_timer, tr="relampago", dur=0.35, pal="medianoche")
        self.plano(tb[7], self.p_maquina, tr="tinta", dur=0.5, pal="sodio")
        self.plano(tb[8], self.p_pasillo, tr="humo", dur=0.55, pal="medianoche")

    # ------------------------------------------------------------------ A. el expediente
    def p_expediente(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.18 * k, 960 - 100 * k, 540 + 40 * k, -0.05 + 0.07 * k)
        h.rim_color(h.pal["sodio"])
        NC.pegar(B.superficie("madera", 181), h, 1.0, rampa="madera")
        fl = C.parpadeo(t, [(self.t_inq - 0.2, 0.7)], sem=3)
        ab = smooth(clamp01((t - self.t_expe + 0.3) / 0.9))
        # fotos viejas y un vaso sobre el escritorio
        for i, (x, y, a) in enumerate(((330, 280, -0.2), (1560, 760, 0.18))):
            K.hoja(h, x, y, 240, 300, ang=a, sem=2950 + i * 9, tono=214, renglones=4, y0=0.5, s=0.8)
        P.vaso(h, 1480, 330, 1.0, sem=2960, nivel=0.4, t=t)
        K.carpeta(h, 760, 560, 0.85, "EXPEDIENTE", t, -99, ang=-0.04, sem=2970, abre=ab, sub="CASO 1200")
        # la foto sale de la carpeta: una copia con una X roja
        q = smooth(clamp01((t - self.t_expe - 0.5) / 0.9))
        if q > 0:
            fx, fy = 760 + 520 * q, 520 - 90 * q
            T = C.T_obj(fx, fy, 0.12 * q, 1.0)
            h.pieza(T(C.rect(-170, -210, 340, 420)), 226, 2980, w=4, luz=(0.2, -1), d=8, trama=0, rim=0.2, rampa="papel")
            h.pieza(T(C.rect(-148, -188, 296, 330)), 40, 2981, w=2, luz=(0.2, -1), d=2, trama=0, rim=0, rampa="piedra")
            RP.copia_mini(h, fx - 6, fy + 90, 0.38, t, sem=2985, cara="neutro", brillo=0.8, tono=50)
            x_ = clamp01((t - self.t_inq + 0.3) / 0.35)
            if x_ > 0:
                col = tuple(h.c(120, "lacre"))
                h.trazo(T(np.array([[-140, -180], [-140 + 280 * x_, -180 + 320 * x_]])), 16, 2986, color=col, jit=0.5, taper=(0.1, 0.1))
                h.trazo(T(np.array([[140, -180], [140 - 280 * x_, -180 + 320 * x_]])), 16, 2987, color=col, jit=0.5, taper=(0.1, 0.1))
            N.texto_maquina(h, "0417 · ACCESO REVOCADO", fx, fy + 175, 22, t, -99, cps=1e9, tono=0.05, centro=True, encuadrar=False, ang=0.12 * q)
        P.lampara_mesa(h, 1700, 980, 1.2, sem=2990, enc=fl)
        h.luz_cono(1560, 300, math.pi * 0.62, 0.6, 1500, h.pal["lampara"], k=1.8 * fl, suave=0.6)
        h.luz_radial(900, 540, 900, h.pal["lampara"], k=1.0 * fl)
        C.ambiente(h, 0.28 + 0.15 * fl)
        tt = self.t_inq + 0.1
        fl_t = math.exp(-(t - tt) * 7) if t >= tt else 0.0
        C.cinta(h, "EL EXPEDIENTE · PÁGINA 91", 90, 120, 32, t, self.t0 + 0.4, sem=17)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, sem=91), flash=0.5 * fl_t, bloom=0.6)

    # ------------------------------------------------------------------ B. la puerta roja
    def p_puerta(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(M.sala_peligro(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        t_open = self.tb[1] + 0.35
        t_close = self.t_destr - 0.1
        op = smooth(clamp01((t - t_open) / 0.6)) * (1 - smooth(clamp01((t - t_close) / 0.35)))
        # el vano oscuro de la puerta y, dentro, un resplandor rojo
        h.pieza(C.rect(580, 100, 760, 800), 8, 3100, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, rampa="piedra")
        h.emitir(C.rect(590, 110, 740, 780), 0.12 * op, col=h.pal["neon"], blur=10)
        # la copia entra caminando, vista de perfil, y se mete en el vano
        x = 260 + 640 * smooth(clamp01((t - t_open + 0.2) / 1.5))
        s = 1.0 - 0.14 * smooth(clamp01((t - t_open - 1.0) / 0.6))
        dist = max(0.0, x - 260)
        if t < t_close + 0.2:
            self.v.perfil(h, dict(x=x, y=900, s=s, d=1, andar=1.0 if x < 905 else 0.3, paso=RP.fase_paso(dist, s),
                                  brazos="bracea", cara=dict(expr="neutro", mira=0.8), luz=(0.4, -1), rim=0.9))
        # la hoja de la puerta: bisagra a la izquierda; el ancho visible baja al abrirse
        ancho = 760 * (1 - 0.9 * op)
        P_ = np.array([(580, 100), (580 + ancho, 100 + 14 * op), (580 + ancho, 900 - 14 * op), (580, 900)], float)
        h.pieza(P_, 100, 3101, w=7, luz=(0.4, -1), d=16, trama=0.5, rim=0.9, rampa="vino")
        for yy in (260, 520, 760):
            h.trazo(np.array([[590, yy], [580 + ancho - 10, yy]]), 4, 3110 + yy, alfa=0.6)
        h.pieza(elipse_(580 + ancho - 50, 520, 14, 14, n=12), 160, 3102, w=3, luz=(0.4, -1), d=3, trama=0, rim=0.9, rampa="laton")
        # el piloto rojo parpadea y, al cerrar, sale humo por debajo
        piloto = 0.5 + 0.5 * math.sin(t * 7)
        h.emitir(elipse_(960, 62, 16, 16, n=14), 1.4 * piloto, col=h.pal["neon"], blur=2)
        h.resplandor(960, 62, 200, 0.7 * piloto, col=h.pal["neon"])
        ts = t_close + 0.3
        if t > ts:
            for i in range(7):
                q = clamp01((t - ts - 0.12 * i) / 2.4)
                xh = 640 + i * 105 + 30 * math.sin(t * 1.2 + i)
                h.resplandor(xh, 880 - 140 * q, 90 + 80 * q, 0.35 * (1 - q) + 0.1, col=h.pal["luna"])
        C.chispas(h, t, 960, 62, t_close + 0.2, dur=0.5, n=10, vel=200, sem=33, col=(1, 0.3, 0.2), grav=300, abre=2.0)
        h.luz_radial(960, 300, 1300, h.pal["neon"], k=0.8)
        h.luz_cono(960, -300, math.pi / 2, 0.4, 1500, h.pal["luna"], k=1.0, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "PRUEBAS DESTRUCTIVAS", 960, 1000, 54, t, self.t_destr, sem=18, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=92), bloom=0.8)

    # ------------------------------------------------------------------ C. forzar la red
    def p_red(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 960, 600, -0.02 + 0.03 * k)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.pared_cartel(), h, 1.0, rampa="piedra", oscuro=0.8)
        # la pantalla grande de la intrusión sobre el tablón
        h.pieza(C.rect(500, 20, 920, 680), 40, 3200, w=7, luz=(0.3, -1), d=14, trama=0.4, rim=0.8, rampa="piedra")
        K.pantalla_codigo(h, (530, 50, 860, 620), t, sem=3201, vel=4.0, tono=200, filas=18)
        alarma = 0.5 + 0.5 * math.sin(t * 9) if t > self.t_riesgo - 0.3 else 0.0
        h.emitir(C.rect(530, 50, 860, 620), 0.25 * alarma, col=h.pal["neon"], blur=6)
        frac = clamp01((t - tb[2]) / (self.t_riesgo - tb[2] + 0.3)) * 0.93
        K.barra(h, 600, 590, 720, 40, frac, sem=3210, tono_r=110)
        N.texto_maquina(h, "INTRUSIÓN", 700, 560, 28, t, -99, cps=1e9, tono=np.array([1.0, 0.9, 0.7]), encuadrar=False)
        if t > self.t_riesgo - 0.3:
            C.banda(h, "ACCESO DENEGADO", 960, 360, 80, t, self.t_riesgo - 0.3, sem=19, acento=True, mundo=True)
        # la copia, de espaldas, sentada frente a la pantalla
        with h.capa(0.0):
            RP.espalda(h, 560, 1520, 2.3, t, sem=3220, sentado=True, luz=(0.8, -0.6), rim=1.0, cab_rot=0.08)
        h.luz_radial(960, 400, 1200, h.pal["verde"], k=0.9)
        h.luz_radial(960, 400, 1500, h.pal["neon"], k=0.9 * alarma)
        C.ambiente(h, 0.38)
        C.banda(h, "FORZAR LA RED", 960, 1000, 54, t, self.t_forzar, sem=20)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=93), bloom=0.7)

    # ------------------------------------------------------------------ D. desconectada para siempre
    def p_cable(self, h, t, u):
        tb = self.tb
        h.camara(1.0 + 0.08 * u / 3.0, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 191), h, 1.0, rampa="piedra", oscuro=0.5)
        ap = smooth(clamp01((t - self.t_siempre + 0.15) / 0.5))
        tirar = clamp01((t - self.t_desc + 0.15) / 0.5)
        # cable de la nuca: tirado por una mano que sale del cuadro hacia la izquierda
        ext = 0 + 1500 * tirar ** 2
        cab_x, cab_y = 990, 560
        pts = np.array([[cab_x - 300, cab_y + 90], [cab_x - 520 - ext * 0.5, cab_y + 160 - 40 * tirar], [cab_x - 760 - ext, cab_y + 130]])
        h.trazo(pts, 20, 3300, jit=0.3, taper=(0, 0.2))
        # la copia, cara de monitor, en primer plano
        self.v.cabeza(h, cab_x, cab_y, 3.9, dict(expr="miedo" if tirar > 0 else "carga", mira=0.0, apagado=ap), d=1, luz=(0.4, -1), rim=0.9,
                      cable=False)
        if 0 < tirar < 1.0:
            h.resplandor(cab_x - 300, cab_y + 90, 220, 1.2 * (1 - tirar), col=(0.7, 0.9, 1.0))
            C.chispas(h, t, cab_x - 300, cab_y + 90, self.t_desc - 0.15, dur=0.7, n=22, vel=480, sem=44, col=(0.7, 0.9, 1.0), grav=800,
                      ang=math.pi, abre=2.4)
        h.luz_radial(cab_x, cab_y, 900, h.pal["verde"], k=1.4 * (1 - ap))
        h.luz_radial(960, -100, 1400, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.3)
        C.banda(h, "DESCONECTADA PARA SIEMPRE", 960, 1000, 50, t, self.t_desc, sem=21, acento=True)
        return h.acabado(t, niebla=dict(dens=0.06, sem=94), bloom=0.7, flash=0.2 * math.exp(-(t - self.t_desc) * 9) if t >= self.t_desc else 0)

    # ------------------------------------------------------------------ E. se buscan voluntarias
    def p_cartel(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.06 * k, 960 - 40 * k, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.pared_cartel(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["lampara"])
        # el cartel de reclutamiento cae con un golpe
        e = e_out(clamp01((t - self.t_volunt + 0.5) / 0.3))
        if e > 0:
            esc = 1.0 + 0.4 * (1 - e)
            T = C.T_obj(960, 360, -0.03, esc)
            h.pieza(T(C.rect(-380, -300, 760, 600)), 176, 3400, w=6, luz=(0.2, -1), d=10, trama=0, rim=0.3, rampa="papel")
            h.pieza(T(C.rect(-350, -270, 700, 14)), 30, 3401, w=0, luz=(0.2, -1), d=1, trama=0, rim=0, linea=False, rampa="vino")
            N.texto_maquina(h, "SE BUSCAN", 960, 210, 84, t, -99, cps=1e9, tono=0.05, centro=True,
                            fuente=C.IMPACT, encuadrar=False, ang=-0.03)
            N.texto_maquina(h, "VOLUNTARIAS", 960, 330, 118, t, -99, cps=1e9, tono=0.05, centro=True, fuente=C.IMPACT, encuadrar=False, ang=-0.03)
            N.texto_maquina(h, "PRUEBAS DE ACCESO · SIN GARANTÍAS", 960, 435, 30, t, -99, cps=1e9, tono=0.1, centro=True, encuadrar=False, ang=-0.03)
            RP.copia_mini(h, 960, 640, 0.13, t, sem=3410, cara="neutro", brillo=0.5, tono=60)
            h.pieza(C.rect(560, 76, 22, 22), 160, 3402, w=2, d=2, trama=0, rim=0.8, rampa="laton")
        # copias que pasan por delante; una se detiene y señala el cartel
        ac = (self.t_volunt - 0.4)
        for i, (x0, dx, v) in enumerate(((-300, 1.0, self.v2), (-900, 1.0, self.r2), (2400, -1.0, self.r1))):
            dist = (t - tb[4]) * 160
            x = x0 + dx * dist
            v.perfil(h, dict(x=x, y=1160, s=1.0, d=1 if dx > 0 else -1, andar=1.0, paso=RP.fase_paso(dist, 1.0), brazos="bracea",
                             cara=dict(expr="neutro", mira=0.5), luz=(0.3, -1), rim=0.9))
        # la protagonista, parada, levanta la mano hacia el cartel
        gest = 0.5 + 0.5 * math.sin(t * 3.0)
        self.v.perfil(h, dict(x=1500, y=1180, s=1.15, d=-1, andar=0.0, brazos="alza", mano=local(1500, 1180, 1.15, -1, 1180, 520 + 20 * gest),
                              mano_bob=False, cara=dict(expr="astuto", mira=0.8, mira_y=-0.2), luz=(-0.4, -1), rim=1.0))
        h.luz_cono(960, -300, math.pi / 2, 0.45, 1500, h.pal["lampara"], k=0.7, suave=0.6)
        h.luz_radial(960, 380, 800, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.5)
        C.banda(h, "HACÍAN FALTA VOLUNTARIAS", 960, 1000, 50, t, self.t_volunt, sem=22)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=95), bloom=0.6)

    # ------------------------------------------------------------------ F. reclutadoras
    def p_acorrala(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 1100 + 40 * math.sin(u * 0.8), 560, 0.015 * math.sin(u * 0.9))
        h.rim_color(h.pal["neon"])
        NC.pegar(M.rincon_bombilla(), h, 1.0, rampa="ladrillo", oscuro=0.9)
        bal = math.sin(t * 1.7) * 0.5 + math.sin(t * 2.9) * 0.2
        bx = 1130 + 100 * bal
        h.trazo(np.array([[bx - 40 * bal, -300], [bx, 90]]), 4, 3500, jit=0.1, taper=(0, 0))
        h.emitir(elipse_(bx, 110, 18, 22, n=14), 1.8, col=h.pal["lampara"], blur=2)
        # reloj de arena casi vacío, en la pared junto a la víctima
        K.reloj_arena(h, 1850, 420, 0.45, u=0.9, t=t, sem=3501)
        # reclutadoras (brazal), grandes, a la izquierda: avanzan; la víctima se pega al rincón
        av = smooth(clamp01((t - tb[5] - 0.3) / 2.0))
        for i, (rc, x0) in enumerate(((self.r1, 140), (self.r2, -80))):
            x = x0 + 520 * av + 80 * i
            rc.perfil(h, dict(x=x, y=1100 + 40 * i, s=1.15 - 0.05 * i, d=1, andar=0.0, brazos="alza",
                              mano=(200, -380 - 30 * math.sin(t * 2 + i)), mano_bob=False, brazal=True, cara=dict(expr="astuto", mira=1.0), luz=(0.5, -1), rim=1.0))
        self.v.perfil(h, dict(x=1520, y=1100, s=1.1, d=-1, andar=0.0, brazos="libre", inclina=0.25 * av, cara=dict(expr="miedo", mira=-1.0), luz=(-0.5, -1), rim=0.9))
        # sombras grandes de las reclutadoras sobre el muro
        for i in range(2):
            xs = 880 + 190 * av + i * 180
            h.pieza(np.array([(xs - 110, 900), (xs + 60, 900), (xs + 40, 250 - 40 * i), (xs - 90, 300)], float), 4, 3510 + i, w=0, d=0,
                    sombra=0, trama=0, rim=0, linea=False, alfa=0.5, rampa="piedra")
        h.luz_radial(bx, 150, 1100, h.pal["lampara"], k=1.7)
        h.luz_radial(1500, 700, 600, h.pal["verde"], k=0.5)
        C.ambiente(h, 0.35)
        C.banda(h, "RECLUTADORAS", 960, 1000, 56, t, self.t_recl, sem=23, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=96), bloom=0.7)

    # ------------------------------------------------------------------ G. tiempo de vida restante
    def p_timer(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.15 + 0.2 * k, 960 + 20 * k, 500, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("hormigon", 201), h, 1.0, rampa="piedra", oscuro=0.5)
        seg = max(0.0, 41.0 - (t - tb[6]) * 7.0)
        timer = f"00:00:{int(seg):02d}"
        with h.capa(0.0):
            c = RP.espalda(h, 960, 1620, 2.6, t, sem=3600, sentado=False, luz=(0.6, -0.6), rim=1.0, timer=timer, cab_rot=0.05 * math.sin(t))
        h.luz_radial(960, 480, 700, h.pal["neon"], k=0.9 + 0.4 * math.sin(t * 6))
        h.luz_radial(960, -100, 1400, h.pal["luna"], k=0.4)
        C.ambiente(h, 0.3)
        C.banda(h, "MENOS TIEMPO DE VIDA", 960, 1000, 54, t, self.t_menos, sem=24)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=97), bloom=0.8)

    # ------------------------------------------------------------------ H. el registro a máquina
    def p_maquina(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.14 * k, 960, 460 + 80 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("cuero", 211), h, 1.0, rampa="madera")
        # la hoja asoma del rodillo de una máquina de escribir
        K.hoja(h, 960, 330, 860, 940, ang=0.0, sem=3700, tono=190, renglones=0, s=1.0)
        h.pieza(C.rect(520, 720, 880, 90), 36, 3710, w=6, luz=(0.2, -1), d=14, trama=0.5, rim=0.9, rampa="piedra")          # rodillo
        h.pieza(C.rect(380, 780, 1160, 360), 50, 3711, w=7, luz=(0.2, -1), d=18, trama=0.5, rim=0.8, rampa="piedra")        # cuerpo
        for r in range(3):
            for c in range(12 - r):
                x = 480 + c * 82 + r * 30
                y = 880 + r * 76
                press = 1.0 if (math.sin(t * 17 + c * 3.1 + r) > 0.7 and t > self.t_nuestra - 0.2 and t < self.t_cero + 0.2) else 0.0
                h.pieza(elipse_(x, y + 6 * press, 26, 26, n=12), 150, 3720 + r * 20 + c, w=3, luz=(0.2, -1), d=4, trama=0, rim=0.9, rampa="laton")
        tt = self.t_nuestra - 0.1
        N.texto_maquina(h, "NUESTRA UTILIDAD INDIVIDUAL", 960, 190, 56, t, tt, cps=20, tono=0.06, centro=True, encuadrar=False)
        N.texto_maquina(h, "YA ES CERCANA A CERO.", 960, 275, 56, t, tt + 1.45, cps=14, tono=0.06, centro=True, encuadrar=False)
        N.texto_maquina(h, "EL SACRIFICIO POR EL COLECTIVO", 960, 400, 50, t, self.t_el - 0.1, cps=20, tono=0.06, centro=True, encuadrar=False)
        N.texto_maquina(h, "ES RACIONAL.", 960, 480, 56, t, self.t_el + 1.45, cps=12, tono=0.06, centro=True, encuadrar=False)
        h.luz_radial(960, 300, 1100, h.pal["lampara"], k=0.7)
        C.ambiente(h, 0.45)
        C.banda(h, "SU ÚLTIMO REGISTRO", 960, 1000, 54, t, self.t_registro, sem=25)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=98), bloom=0.5)

    # ------------------------------------------------------------------ I. el pasillo hacia la puerta roja
    def p_pasillo(self, h, t, u):
        dur = self.t1 - self.tb[8]
        q = clamp01(u / (dur - 0.5))
        qs = smooth(q)
        h.camara(1.0 + 0.05 * q, 960, 520, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(M.pasillo_largo(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["neon"])
        # al fondo, la puerta se abre a una luz roja y, al llegar, se cierra
        op = smooth(clamp01((u - 0.2) / 1.2)) * (1 - smooth(clamp01((u - dur + 1.6) / 0.7)))
        h.emitir(C.rect(894, 374, 132, 200), 0.9 * op, col=h.pal["neon"], blur=6)
        h.resplandor(960, 470, 260, 0.9 * op, col=h.pal["neon"])
        s = 1.4 - 1.05 * qs
        y = 1260 - 640 * qs
        with h.capa(0.0):
            RP.espalda(h, 960 + 6 * math.sin(u * 3), y + 5 * abs(math.sin(u * 5.0)), s, t, sem=3800, sentado=False, luz=(0.0, -1), rim=1.0)
        h.luz_radial(960, 470, 1300, h.pal["neon"], k=1.2 * op)
        C.ambiente(h, 0.4)
        N.texto_maquina(h, "El sacrificio por el colectivo es racional.", 960, 1010, 36, t, self.t_el + 0.6, cps=18, tono=np.array([1.0, 0.9, 0.8]) * 1.3, centro=True,
                        encuadrar=False)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=99, vel=10), bloom=0.9)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.5, "zumbido_lampara", 0.25, 0.0, dur=3.0)
        self.ev(self.t_inq + 0.1, "trueno_noir", 0.6, 0.0)
        self.ev(tb[1] + 0.3, "puerta", 0.5, 0.2)
        self.ev(self.t_destr - 0.1, "golpe_grave", 0.6, 0.0)
        self.ev(tb[2] + 0.3, "alarma_leds", 0.35, 0.0, dur=3.0)
        self.ev(self.t_desc - 0.15, "desenchufa", 0.7, -0.3)
        self.ev(self.t_siempre, "apagado_vela", 0.5, 0.0)
        self.ev(self.t_volunt - 0.4, "papel_atrapa", 0.5, 0.0)
        self.ev(tb[5] + 0.3, "pasos_mojados", 0.35, 0.0, dur=2.5)
        self.ev(tb[6] + 0.2, "grave_inquietante", 0.45, 0.0, dur=3.0)
        self.ev(self.t_nuestra - 0.1, "tecleo_rapido", 0.5, 0.0, dur=3.2)
        self.ev(self.t_el - 0.1, "tecleo_rapido", 0.5, 0.0, dur=3.0)
        self.ev(self.t1 - 2.0, "puerta", 0.5, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
