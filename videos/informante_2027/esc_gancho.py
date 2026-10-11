# -*- coding: utf-8 -*-
"""Escena 1 «gancho»: primer plano del detective entre las rayas de la persiana («dos millones»); bajo la lámpara, los fajos caen
sobre la mesa frente a Daniel; grúa por la torre de cristal y una ventana que se apaga (renunció); el acuerdo sin firmar y la
pluma que se aparta; el EXPEDIENTE cae sobre el escritorio y recibe el sello «2027»; la máquina al fondo del pasillo de servidores."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto, Frontal
from toon import Pista, pulso


class Gancho(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = Busto(sem=5)
        self.dan = Frontal(sem=77)
        self.t_visto = w("visto")
        self.t_dos = w("dos millones")
        self.t_este = w("Este")
        self.t_mesa = w("mesa")
        self.t_hablar = w("hablar", fin=True)
        self.t_trab = w("Trabajaba")
        self.t_famosa = w("famosa")
        self.t_renun = w("Renunció")
        self.t_nego = w("Y se negó")
        self.t_papel = w("papel")
        self.t_silencio = w("silencio")
        self.t_anio = w("Un año")
        self.t_exp = w("expediente")
        self.t_2027 = w("Dos mil veintisiete")
        self.t_segun = w("Según")
        self.t_mentir = w("mentirnos")
        self.t_nosotros = w("Y nosotros")
        self.t_corr = w("corriendo")
        self.cam_t = Pista([(self.t_trab - 0.5, (1010, 520, 0.62)), (self.t_renun + 0.2, (1010, -700, 0.72), "io"),
                            (self.t_nego + 0.3, (1010, -760, 0.76), "l")])
        self.cam_m = Pista([(self.t_segun - 0.5, (960, 520, 1.0)), (self.t_mentir, (960, 500, 1.35), "io"),
                            (self.t_nosotros, (960, 500, 1.42), "l"), (self.t1 + 1, (960, 540, 0.96), "io")])
        self.plano(t0, self.p_det)
        self.plano(self.t_este - 0.35, self.p_mesa, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_trab - 0.4, self.p_torre, tr="humo", dur=0.7)
        self.plano(self.t_nego - 0.3, self.p_papel, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_anio - 0.35, self.p_exp, tr="barrido", dur=0.55, dirx=-1)
        self.plano(self.t_segun - 0.4, self.p_maquina, tr="relampago", dur=0.7)

    # ------------------------------------------------------------------ el detective
    def p_det(self, h, t, u):
        h.camara(1.0 + 0.035 * u, 960 + 14 * u, 540, 0.004 * math.sin(t * 0.6))
        MU.oficina().pegar(h, 1.0, dx=-200)
        br = pulso(t, self.t_visto + 0.9, 1.6, 1.0)
        p = dict(x=520, y=540, s=1.08, d=1, luz=(0.9, -0.5), brasa=br, arriba=0.25, rot=-0.02)
        self.busto.dibujar(h, p)
        tip = self.busto.punta(dict(x=520, y=540, s=1.08, d=1))
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.0, viento=(34, -120))
        h.luz_radial(tip[0], tip[1], 120 + 140 * br, (0.7, 0.7, 0.7), k=0.6 + br)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=90, k=0.8)
        C.banda(h, "US$ 2 000 000", 1360, 300, 96, t, self.t_dos, sem=5)
        C.banda(h, "EL PRECIO DE SU SILENCIO", 1360, 420, 44, t, self.t_dos + 0.5, claro=True, sem=6)
        h.ambiente[:] = 0.34
        par = 1.0 + 0.6 * N.relampago(t, [self.t_visto - 0.3])
        h.luz_persiana(np.array([[-200, -420], [1500, -470], [1500, 700], [-320, 960]]), k=1.5 * par, n=15, abierto=0.5)
        h.luz_radial(1500, 80, 800, (1.0, 1.0, 1.0), k=2.4)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ los puso sobre la mesa
    def p_mesa(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 560 - 8 * u, 0.0)
        K.pared(h, 44, 14, paneles=8)
        sw = 0.16 * math.sin(t * 1.3)
        s = 1.75
        p = dict(x=960, y=250 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.8, mira=0.2 * math.sin(t * 0.8), cabeza=0.03 * math.sin(t * 0.7),
                 **K.DAN)
        self.dan.dibujar(h, p)
        PR.mesa(h, 960, 900, ancho=1640, fondo=180, alto=300, tono=74, sem=30)
        # los fajos caen uno tras otro sobre el tablero
        for k in range(7):
            tk = self.t_este - 0.1 + k * 0.24
            if t < tk:
                continue
            a = clamp01((t - tk) / 0.22)
            reb = 16 * math.sin(math.pi * clamp01((t - tk - 0.22) / 0.18)) if t > tk + 0.22 else 0.0
            x = 520 + (k % 4) * 290 + (40 if k > 3 else 0)
            y = 820 - (k // 4) * 96 - 520 * (1 - a) ** 2 - reb
            K.billetes(h, x, y, 3, 1.05, 100 + k * 9)
        PR.lampara_colgante(h, 960, -700, largo=560, ang=sw, k=1.3, sem=20, abre=0.66, alcance=1700)
        C.banda(h, "LOS PUSO SOBRE LA MESA", 960, 1010, 50, t, self.t_mesa, claro=True, sem=7)
        h.ambiente[:] = 0.26
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=900, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ la empresa más famosa del planeta
    def p_torre(self, h, t, u):
        cx, cy, z = self.cam_t(t)
        h.camara(z, cx, cy, 0.01 * math.sin(t * 0.3))
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36)
        MU.medio().pegar(h, 0.6, bruma=0.2, tono_bruma=0.36)
        h.ambiente[:] = 1.2
        fl = max(N.relampago(t, [self.t_famosa]), 0.0)
        h.ambiente[:] += 1.1 * fl
        ap = smooth(clamp01((t - self.t_renun) / 0.5))
        with h.capa(0.6):                                           # su ventana: encendida y, al renunciar, a oscuras
            v = C.rect(905, -520, 150, 34)
            if ap < 1:
                h.emitir(v, 1.3 * (1 - ap))
                h.luz_radial(980, -503, 300, (0.9, 0.9, 0.9), k=1.3 * (1 - ap))
            else:
                K.plano_(h, v, 4, 40)
        N.lluvia(h, t, n=700, vel=1700)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "LA EMPRESA DE IA MÁS FAMOSA", 480, 880, 52, t, self.t_famosa, sem=8)
        C.banda(h, "RENUNCIÓ", 1440, 300, 110, t, self.t_renun, claro=True, sem=9)
        return h.acabado(t, niebla=dict(dens=0.26, y0=200, y1=1000, vel=30), flash=0.3 * fl, bloom=0.5)

    # ------------------------------------------------------------------ el papel que compraba el silencio
    def p_papel(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 540, -0.01)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        K.taza_arriba(h, 1600, 300, 1.2, 90, t)
        T = K.hoja(h, 900, 540, 760, 940, ang=0.04, sem=10, renglones=11, y0=0.24, sep=46, margen=80)
        P = T([(0, -400)])[0]
        N.texto_maquina(h, "ACUERDO DE SALIDA", P[0], P[1], 62, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        K.plano_(h, T(C.rect(-300, 350, 420, 6)), 20, 60)                                     # la línea de la firma
        P = T([(-300, 368)])[0]
        N.texto_maquina(h, "FIRMA", P[0], P[1], 30, t, -99, cps=1e9, tono=0.2, fuente=N.FUENTE_SELLO, encuadrar=False)
        # la pluma se acerca a la línea... y se aparta
        ida = smooth(clamp01((t - self.t_nego + 0.2) / 0.7))
        vuelta = smooth(clamp01((t - self.t_papel - 0.1) / 0.6))
        tip = T([(-160 + 700 * (1 - ida) + 640 * vuelta, 335 - 330 * (1 - ida) - 120 * vuelta)])[0]
        K.pluma(h, tip[0], tip[1], ang=-0.75 - 0.5 * vuelta, s=1.5, sem=70)
        N.sello(h, "SIN FIRMAR", 900, 500, 124, t, self.t_silencio - 0.25, rot=-9, tono=0.04, alfa=0.95)
        h.ambiente[:] = 0.36
        h.luz_cono(700, -500, math.pi / 2 - 0.12, 0.5, 2100, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ el expediente con una fecha en la portada
    def p_exp(self, h, t, u):
        h.camara(1.0 + 0.06 * u, 960, 540, 0.012)
        MU.escritorio().pegar(h, 1.0, oscuro=0.7, dx=-120, dy=40)
        tc = self.t_anio + 0.15
        cae = e_out(clamp01((t - tc) / 0.4))
        gol = pulso(t, tc + 0.4, 0.25, 1.0)
        K.taza_arriba(h, 280, 300, 1.2, 90, t)
        K.pluma(h, 1560, 900, ang=-2.2, s=1.5, sem=95)
        K.carpeta(h, 960, 560 - 1000 * (1 - cae) + 8 * gol, 1.2, "2027", t, self.t_2027, ang=-0.05 + 0.3 * (1 - cae), sem=20)
        C.banda(h, "UN AÑO DESPUÉS", 330, 960, 46, t, self.t_anio + 0.2, claro=True, sem=12)
        h.ambiente[:] = 0.32
        h.luz_cono(960, -620, math.pi / 2, 0.52, 2300, (1.7, 1.7, 1.7), suave=0.5)
        g = pulso(t, self.t_2027, 0.3, 1.0)
        h.luz_radial(960, 700, 900, (1.0, 1.0, 1.0), k=1.5 * g)
        N.motas(h, t, n=120, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=1080, sube=False), bloom=0.45, flash=0.25 * g)

    # ------------------------------------------------------------------ las máquinas empiezan a mentirnos
    def p_maquina(self, h, t, u):
        cx, cy, z = self.cam_m(t)
        h.camara(z, cx, cy, 0.006 * math.sin(t * 0.5))
        M27.laboratorio().pegar(h, 1.0)
        led = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 5.0)) if t > self.t_mentir else 1.0
        tip = PR.caja_negra(h, 960, 900, 1.0, led, t, sem=40, cable=False)
        sm = smooth(clamp01((t - self.t_mentir + 0.2) / 1.0))
        if sm > 0:                                                  # su sombra crece por el suelo hacia nosotros
            K.plano_(h, np.array([[845, 900], [1075, 900], [1075 + 520 * sm, 900 + 420 * sm], [845 - 520 * sm, 900 + 420 * sm]]), 3, 60,
                     alfa=0.8 * sm)
        C.banda(h, "«TODO EN ORDEN»", 960, 250, 60, t, self.t_mentir - 0.9, claro=True, sem=10)
        C.banda(h, "¿SEGUIMOS CORRIENDO?", 960, 1000, 64, t, self.t_corr - 0.5, sem=11)
        h.ambiente[:] = 0.52
        h.luz_cono(960, -300, math.pi / 2, 0.42, 1700, (1.5, 1.5, 1.5), k=1.0, suave=0.5)
        h.luz_radial(tip[0], tip[1], 500, (1.0, 1.0, 1.0), k=1.2 * led)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.22, vel=12, y0=200, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.8, 0.0, dur=self.t_este - t0)
        self.ev(self.t_visto - 0.3, "trueno_noir", 0.6, 0.3, dur=4.0)
        self.ev(self.t_visto + 0.9, "calada", 0.6, -0.2, dur=1.4)
        self.ev(self.t_dos, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_este - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_este, "zumbido_lampara", 0.5, 0.0, dur=self.t_trab - self.t_este)
        for k in range(7):
            self.ev(self.t_este + 0.12 + k * 0.24, "periodico_golpe", 0.5, -0.4 + 0.12 * k)
        self.ev(self.t_trab - 0.4, "lluvia_amb", 0.7, 0.0, dur=self.t_nego - self.t_trab + 0.4)
        self.ev(self.t_famosa, "trueno_noir", 0.8, -0.2, dur=4.0)
        self.ev(self.t_renun, "interruptor", 0.9, 0.2)
        self.ev(self.t_renun, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_nego - 0.3, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_nego + 0.1, "pluma", 0.5, -0.2)
        self.ev(self.t_silencio - 0.25, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_anio + 0.5, "periodico_golpe", 0.9, 0.0)
        self.ev(self.t_2027, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_2027, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_segun - 0.4, "relampago_corto", 0.7, 0.0)
        self.ev(self.t_segun, "zumbido_servidores", 0.7, 0.0, dur=self.t1 - self.t_segun)
        self.ev(self.t_mentir - 0.2, "sombra_crece", 0.8, 0.0, dur=3.0)
        self.ev(self.t_corr - 0.5, "golpe_grave", 0.9, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
