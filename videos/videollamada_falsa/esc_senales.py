# -*- coding: utf-8 -*-
"""Escena 10 «senales»: paneo por la bahía de Hong Kong con una baliza que parpadea (las señales); seis detenidos tras los
barrotes y, sobre la mesa, el abanico de documentos robados con sus contadores (90 préstamos, 54 cuentas); el control facial del
banco: el óvalo de la cámara, la línea que barre y la máscara que se desliza sobre la cara (VERIFICADO); una sola máscara entre
el ojo de la máquina y el ojo del hombre."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_truco import mascara
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave


class Senales(BaseNoir):
    TR_SALIDA = ("barrido", 0.6)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.pres = [Frontal(sem=700 + 7 * k) for k in range(6)]
        self.cara = Frontal(sem=760)
        self.t_yhk = w("Hong")
        self.t_senales = w("señales")
        self.t_meses = w("Meses antes")
        self.t_seis = w("seis")
        self.t_con = w("Con documentos")
        self.t_noventa = w("noventa")
        self.t_cinc = w("cincuenta")
        self.t_ycuando = w("Y cuando")
        self.t_cara = w("cara")
        self.t_usaban = w("Usaban")
        self.t_rostro = w("rostro")
        self.t_misma = w("La misma")
        self.t_maquina = w("máquina")
        self.t_hombre = w("hombre")
        self.cam_b = Pista([(t0, (500, 380, 0.86)), (self.t_meses, (1500, 420, 0.95), "io")])
        self.plano(t0, self.p_bahia)
        self.plano(self.t_meses - 0.35, self.p_detenidos, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_con - 0.3, self.p_documentos, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.6))
        self.plano(self.t_ycuando - 0.35, self.p_facial, tr="barrido", dur=0.55, dirx=-1)
        self.plano(self.t_misma - 0.35, self.p_dos, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ las señales
    def p_bahia(self, h, t, u):
        cx, cy, z = self.cam_b(t)
        h.camara(z, cx, cy, 0.0)
        C.hk_cielo().pegar(h, 0.05, dx=-(t * 5.0) % 300)
        C.hk_lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36)
        C.hk_agua().pegar(h, 0.6)
        C.hk_medio().pegar(h, 0.6, bruma=0.22, tono_bruma=0.36)
        h.ambiente[:] = 1.2
        h.luz_radial(1000, 700, 2200, (0.9, 0.9, 0.9), k=1.0)
        with h.capa(0.6):                                        # balizas de aviso en las azoteas
            for k, (bx, by) in enumerate(((1020, -540), (20, 230), (1960, 130), (2620, 290))):
                on = 0.5 + 0.5 * math.sin(t * 5.0 + k * 1.4)
                if on > 0.4:
                    h.emitir(C.rect(bx - 9, by - 9, 18, 18), 1.4 * on, blur=3)
                    h.luz_radial(bx, by, 330, (1.0, 1.0, 1.0), k=1.6 * on)
        N.lluvia(h, t, n=500, vel=1700)
        C.banda(h, "HONG KONG YA TENÍA SEÑALES", 960, 140, 64, t, self.t_senales - 0.5, sem=5)
        return h.acabado(t, niebla=dict(dens=0.26, y0=200, y1=1000, vel=30), bloom=0.55)

    # ------------------------------------------------------------------ seis detenidos
    def p_detenidos(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 520, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.75)
        looks = [dict(pelo="oscuro", traje=40), dict(pelo="calvo", traje=58), dict(pelo="rizado", traje=34), dict(pelo="oscuro", traje=66),
                 dict(pelo="sombrero", traje=30), dict(pelo="calvo", traje=48, barba=True)]
        for k, F in enumerate(self.pres):
            a = e_out(clamp01((t - self.t_meses - 0.12 * k) / 0.4))
            p = dict(looks[k])
            p.update(x=210 + k * 300, y=900 + 40 * (1 - a), s=1.12, luz=(0.0, -1.0), rim=0.85, mira=0.5 * math.sin(t * 0.8 + k),
                     cabeza=0.3)
            F.dibujar(h, p)
        for k in range(26):                                      # barrotes
            x = -40 + k * 80
            h.pieza(C.rect(x, -80, 20, 1200), 30, 60 + k, w=4, luz=(0.5, -0.7), d=7, trama=0.4, rim=0.9)
        C.banda(h, "AGOSTO DE 2023", 960, 110, 56, t, self.t_meses, claro=True, sem=6)
        C.banda(h, "6 DETENIDOS", 960, 960, 110, t, self.t_seis, sem=7)
        h.ambiente[:] = 0.34
        for k in range(6):
            h.luz_cono(210 + k * 300, -540, math.pi / 2, 0.24, 1650, (1.3, 1.3, 1.3), k=0.8, suave=0.5)
        N.motas(h, t, n=100, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=900, sube=False))

    # ------------------------------------------------------------------ documentos robados -> préstamos y cuentas
    def p_documentos(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960, 540, 0.012)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        for k in range(8):                                       # el abanico de documentos de identidad
            a = e_out(clamp01((t - self.t_con + 0.25 - 0.06 * k) / 0.35))
            ang = (-0.6 + 0.17 * k) * a
            c = np.array([520.0, 1000.0])
            P = PR.rot(C.rect(520 - 150, 1000 - 620, 300, 190), ang, c)
            h.pieza(P, 214, 20 + 4 * k, w=4, luz=(0.2, -1), d=6, trama=0, rim=0)
            f = PR.rot(C.rect(520 - 132, 1000 - 600, 90, 110), ang, c)
            h.pieza(f, 70, 21 + 4 * k, w=2.5, luz=(0, -1), d=2, trama=0.4, sombra=0)
            h.pieza(PR.rot(np.array(elipse_(520 - 87, 1000 - 556, 20, 24, n=14)), ang, c), 150, 22 + 4 * k, w=0, luz=(0, -1), d=1, sombra=0,
                    trama=0, linea=False)
            for q in range(3):
                h.trazo(PR.rot(np.array([[520 - 20.0, 1000 - 590 + q * 34], [520 + 120.0, 1000 - 590 + q * 34]]), ang, c), 5, 60 + k * 3 + q,
                        alfa=0.5, jit=0.3)
        C.banda(h, "DOCUMENTOS ROBADOS", 520, 170, 54, t, self.t_con + 0.1, claro=True, sem=8)
        for k, (tk, n, et, y) in enumerate(((self.t_noventa, 90, "SOLICITUDES DE PRÉSTAMO", 380), (self.t_cinc, 54, "CUENTAS BANCARIAS", 760))):
            if t < tk - 0.2:
                continue
            v = int(n * clamp01((t - tk + 0.2) / 0.9))
            for q in range(min(v, n) // 6):                      # la pila que crece
                h.pieza(PR.rot(C.rect(960 + 3 * math.sin(q * 2.1), y + 60 - q * 9, 300, 56), 0.02 * math.sin(q * 1.7), np.array([1110, y + 60])),
                        206 - 6 * (q % 3), 100 + 40 * k + q, w=2.5, luz=(0.2, -1), d=3, trama=0, rim=0, sombra=0.3)
            with C.fijo(h):
                N.texto_maquina(h, str(v), 1600, y - 30, 210, t, -99, cps=1e9, tono=0.97, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
                N.texto_maquina(h, et, 1560, y + 130, 36, t, tk, cps=40, tono=0.9, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        h.ambiente[:] = 0.42
        h.luz_radial(700, 520, 1500, (1.0, 1.0, 1.0), k=0.9)
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ «muestre la cara»
    def p_facial(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.img[:] = 0.05
        # el teléfono del banco, en vertical, con la cámara encendida
        h.pieza(np.array(suave([(600, 40), (1320, 40), (1340, 60), (1340, 1040), (1320, 1060), (600, 1060), (580, 1040), (580, 60)], 3)),
                22, 20, w=9, luz=(-0.3, -1), d=16, trama=0.4, rim=0.7)
        pan = C.rect(620, 90, 680, 920)
        h.pieza(pan, 130, 21, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0, grad=(70, 90, 1010))
        s = 2.7
        self.cara.dibujar(h, dict(x=960, y=470 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.7, pelo="oscuro", traje=44, mira=0.0))
        pone = smooth(clamp01((t - self.t_usaban) / 0.8))
        if pone > 0:                                              # la máscara del otro, que se desliza sobre la cara
            mascara(h, 960 + 420 * (1 - pone), 470 - 20, 2.25, 40, tono=228, ang=0.4 * (1 - pone))
            if pone > 0.9:                                        # y sobre la máscara aparecen los rasgos del titular
                for sx in (-1, 1):
                    h.pieza(elipse_(960 + sx * 72, 404, 22, 10, n=14), 230, 50 + sx, w=3, luz=(0, -1), d=1, sombra=0, trama=0)
                    h.pieza(elipse_(960 + sx * 72, 404, 8, 8, n=10), 10, 53 + sx, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
                    h.trazo(np.array([[960 + sx * 36, 366], [960 + sx * 110, 360]]), 9, 56 + sx, jit=0.4)
                h.trazo(np.array([[960, 420], [950, 500], [972, 510]]), 5, 60, jit=0.4)
        h.pieza(C.rect(560, 1010, 800, 80), 22, 22, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        # el óvalo guía y la línea de barrido
        h.anillo(h.tf(np.array(elipse_(960, 450, 250, 330, n=50))), 7 * h.zoom, 70, color=(240, 240, 240), jit=0.4)
        yb = 130 + 640 * (0.5 + 0.5 * math.sin(t * 2.6))
        h.trazo(np.array([[700.0, yb], [1220, yb]]), 6, 71, color=(250, 250, 250), jit=0, taper=(0, 0))
        C.banda(h, "«MUESTRE LA CARA»", 300, 300, 50, t, self.t_cara - 0.5, claro=True, sem=9)
        C.banda(h, "EL ROSTRO DE OTRO", 1620, 420, 50, t, self.t_rostro - 0.2, claro=True, sem=10)
        C.banda(h, "VERIFICADO", 960, 900, 84, t, self.t_rostro + 0.5, sem=11)
        h.ambiente[:] = 0.30
        C.luz_rect(h, pan, 1.15, suave_=6)
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ una máscara, dos víctimas
    def p_dos(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.img[:] = 0.05
        mascara(h, 960, 520 + 10 * math.sin(t * 1.2), 2.6, 30, tono=234, ang=0.04 * math.sin(t * 0.8), datos=1.0, t=t)
        # a la izquierda, el ojo de la máquina (un objetivo)
        a1 = smooth(clamp01((t - self.t_maquina + 0.4) / 0.5))
        cxl, cyl = 300, 540
        for k, (rr, tn) in enumerate(((190, 26), (158, 56), (118, 16), (74, 44), (36, 8))):
            h.pieza(elipse_(cxl, cyl, rr, rr, n=44), tn, 60 + k, w=5, luz=(0.3, -1), d=10, trama=0.3 if k < 2 else 0, rim=0.6)
        h.pieza(elipse_(cxl - 48, cyl - 54, 30, 18, rot=-0.6, n=16), 235, 66, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, alfa=0.75)
        # a la derecha, el ojo del hombre
        a2 = smooth(clamp01((t - self.t_hombre + 0.4) / 0.5))
        cxo, cyo = 1620, 540
        ojo = [(cxo - 230, cyo)] + [(cxo - 230 + 460 * q / 10, cyo - 120 * math.sin(math.pi * q / 10)) for q in range(1, 10)] + \
              [(cxo + 230, cyo)] + [(cxo + 230 - 460 * q / 10, cyo + 96 * math.sin(math.pi * q / 10)) for q in range(1, 10)]
        h.pieza(np.array(ojo), 226, 80, w=8, luz=(0, -1), d=14, trama=0.4, sombra=0.5)
        h.pieza(elipse_(cxo - 20 * math.sin(t), cyo - 8, 86, 86, n=36), 70, 81, w=6, luz=(0, -1), d=10, trama=0.4, rim=0.4)
        h.pieza(elipse_(cxo - 20 * math.sin(t), cyo - 8, 38, 38, n=24), 8, 82, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        h.trazo(np.array([(x_, y_ - 4) for x_, y_ in ojo[:11]]), 14, 83, jit=0.4)
        for sx, a_, cx_ in ((-1, a1, cxl + 200), (1, a2, cxo - 240)):                 # las flechas del engaño
            if a_ > 0:
                x0 = 960 + sx * 250
                h.trazo(np.array([[x0, 540], [x0 + (cx_ - x0) * a_, 540]]), 12, 90 + sx, color=(240, 240, 240), jit=0.4, taper=(0, 0))
        C.banda(h, "BURLA A UNA MÁQUINA", 330, 860, 46, t, self.t_maquina, claro=True, sem=12)
        C.banda(h, "BURLA A UN HOMBRE", 1590, 860, 46, t, self.t_hombre, claro=True, sem=13)
        C.banda(h, "LA MISMA MÁSCARA", 960, 110, 64, t, self.t_misma, sem=14)
        h.ambiente[:] = 0.30
        h.luz_cono(960, -500, math.pi / 2, 0.5, 2000, (1.5, 1.5, 1.5), suave=0.5)
        h.luz_radial(cxl, cyl, 500, (0.9, 0.9, 0.9), k=1.2 * a1)
        h.luz_radial(cxo, cyo, 500, (0.9, 0.9, 0.9), k=1.2 * a2)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=900, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_amb", 0.7, 0.0, dur=self.t_meses - self.t0)
        self.ev(self.t_senales - 0.5, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_meses - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_meses, "puerta", 0.9, 0.0)
        self.ev(self.t_seis, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_con - 0.25, "fichas_mezcla", 0.6, -0.4, dur=0.8)
        self.ev(self.t_noventa - 0.2, "paginas", 0.7, 0.4, dur=0.9)
        self.ev(self.t_cinc - 0.2, "caja_registradora", 0.7, 0.4)
        self.ev(self.t_ycuando - 0.35, "barrido_aire", 0.6, -0.3, dur=0.7)
        self.ev(self.t_ycuando, "datos", 0.4, 0.0, dur=max(1.5, self.t_usaban - self.t_ycuando))
        self.ev(self.t_usaban, "pinza", 0.8, 0.3)
        self.ev(self.t_rostro + 0.5, "campana_bolsa", 0.5, 0.0)
        self.ev(self.t_rostro + 0.5, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_misma - 0.35, "sombra_crece", 0.7, 0.0, dur=3.0)
        self.ev(self.t_maquina, "camara_zoom", 0.8, -0.5)
        self.ev(self.t_hombre, "golpe_grave", 0.9, 0.5)
