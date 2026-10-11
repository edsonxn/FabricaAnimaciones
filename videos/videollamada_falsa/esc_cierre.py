# -*- coding: utf-8 -*-
"""Escena 12 «cierre»: la sala de interrogatorio: el detective de perfil y, enfrente, un sospechoso al que le tiembla la cara
bajo la lámpara; la misma silla con una máscara que no tiembla y que, al caer, deja un rostro vacío; la oficina con la persiana:
«VER PARA CREER» se escribe y se tacha; el expediente se cierra con el sello CASO ABIERTO bajo la lluvia."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_truco import mascara
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto, Detective, Frontal
from toon import Pista, elipse_, pulso, suave, tiembla


class Cierre(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = Busto(sem=5)
        self.det = Detective(sem=3)
        self.sosp = Frontal(sem=900)
        self.t_vida = w("vida")
        self.t_mentir = w("mentirosos")
        self.t_temblaba = w("temblaba")
        self.t_ahora = w("Ahora la cara")
        self.t_tiembla = w("tiembla")
        self.t_ahora2 = w("Ahora la cara", n=1)
        self.t_suya = w("suya")
        self.t_ver = w("Ver para")
        self.t_eso = w("Eso decíamos")
        self.t_pues = w("Pues")
        self.t_alcanza = w("alcanza", fin=True)
        self.t_caso = w("Caso")
        self.plano(t0, self.p_interroga)
        self.plano(self.t_ahora - 0.35, self.p_mascara, tr="empuje", dur=0.6, centro=(W * 0.62, H * 0.42))
        self.plano(self.t_ver - 0.35, self.p_ventana, tr="humo", dur=0.7)
        self.plano(self.t_caso - 0.5, self.p_caso, tr="tinta", dur=0.7)

    # ------------------------------------------------------------------ toda una vida buscando caras que tiemblan
    def p_interroga(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960 + 14 * u, 500, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.9)
        sw = 0.10 * math.sin(t * 1.3)
        PR.lampara_colgante(h, 1120, -700, largo=700, ang=sw, k=1.3, sem=20, abre=0.6, alcance=1700)
        PR.mesa(h, 1120, 960, ancho=900, fondo=140, alto=260, tono=80, sem=30)
        tb = pulso(t, self.t_temblaba - 0.3, 2.2, 1.0) + 0.25
        dx, dy = tiembla(t, 7 * tb, 22, 1)
        s = 2.05
        self.sosp.dibujar(h, dict(x=1300 + dx, y=400 + 474 * s + dy, s=s, luz=(-0.2, -1.0), rim=0.85, pelo="calvo", traje=50, barba=True,
                                  mira=0.9 * math.sin(t * 5), cabeza=0.2 * math.sin(t * 7) * tb))
        for q in range(4):                                         # gotas de sudor
            f = ((t * 0.8 + q * 0.27) % 1.0)
            h.pieza(elipse_(1300 + (-58 + 38 * q) + dx, 400 + 150 * f, 6, 9, n=10), 236, 50 + q, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                    linea=False, alfa=1 - f)
        # el detective, de perfil, en primer término a la izquierda
        self.busto.dibujar(h, dict(x=330, y=520, s=1.05, d=1, luz=(0.9, -0.5), brasa=pulso(t, self.t_vida, 1.4, 1.0), arriba=0.3,
                                   rot=-0.02))
        tip = self.busto.punta(dict(x=330, y=520, s=1.05, d=1))
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.0, viento=(30, -120))
        C.banda(h, "SE LES NOTABA EN LA CARA", 1240, 1000, 54, t, self.t_temblaba - 0.3, claro=True, sem=5)
        h.ambiente[:] = 0.40
        h.luz_radial(330, 480, 700, (1.0, 1.0, 1.0), k=1.1)                 # el detective, a contraluz de la lámpara
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ ahora la cara no tiembla, ni es suya
    def p_mascara(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 520, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.75)
        PR.lampara_colgante(h, 960, -700, largo=560, ang=0.04 * math.sin(t * 1.1), k=1.4, sem=20, abre=0.62, alcance=1800)
        s = 2.7
        self.sosp.dibujar(h, dict(x=960, y=470 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.85, pelo="calvo", traje=50, mira=0.0))
        cae = smooth(clamp01((t - self.t_suya + 0.5) / 0.8))
        h.pieza(elipse_(960, 470, 46 * s, 62 * s, n=30), 90, 40, w=5, luz=(0, -1), d=12, trama=0.5, sombra=0.6)     # debajo no hay rostro
        mascara(h, 960 + 330 * cae, 462 + 520 * cae * cae, 2.3, 50, tono=234, ang=1.1 * cae)
        if cae < 0.05:                                             # los rasgos serenos pintados en la máscara
            for sx in (-1, 1):
                h.trazo(np.array([[960 + sx * 40, 372], [960 + sx * 120, 366]]), 10, 60 + sx, jit=0.4)
            h.trazo(np.array([[960, 420], [948, 520], [974, 530]]), 5, 63, jit=0.4)
        C.banda(h, "YA NO TIEMBLA", 400, 300, 70, t, self.t_tiembla - 0.2, claro=True, sem=6)
        C.banda(h, "NI SIQUIERA ES SUYA", 1500, 300, 62, t, self.t_suya - 0.2, sem=7)
        h.ambiente[:] = 0.26
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ ver para creer
    def p_ventana(self, h, t, u):
        h.camara(1.05 + 0.03 * u, 1100 - 10 * u, 430, 0.0)
        MU.oficina().pegar(h, 1.0)
        p = dict(x=1360.0, y=905.0, s=1.0, d=1, luz=(1.0, -0.4), fumar=pulso(t, self.t_eso, 1.8, 1.0), giro=0.5, viento=0.05, hombros=0.5)
        self.det.dibujar(h, p)
        tip = self.det.punta_cigarro(p)
        h.emitir(np.array([[tip[0] - 4, tip[1] - 4], [tip[0] + 4, tip[1] - 4], [tip[0] + 4, tip[1] + 4], [tip[0] - 4, tip[1] + 4]]), 1.0)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=110, k=0.9)
        h.ambiente[:] = 0.32
        h.luz_persiana(np.array([[60, -420], [1080, -470], [1080, 640], [-80, 900]]), k=1.4, n=15, abierto=0.5)
        h.luz_radial(1550, 60, 760, (1.0, 1.0, 1.0), k=3.0)
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4)
        C.banda(h, "VER PARA CREER", 560, 300, 104, t, self.t_ver, sem=9)
        tch = clamp01((t - self.t_pues) / 0.4)
        if tch > 0:                                                # se tacha
            with C.fijo(h):
                h.trazo(np.array([[130.0, 312], [130 + 860 * tch, 290]]), 20, 70, color=(240, 240, 240), jit=0.6, taper=(0.1, 0.1))
        C.banda(h, "YA NO ALCANZA", 560, 480, 84, t, self.t_alcanza - 0.5, claro=True, sem=8)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ caso abierto
    def p_caso(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960, 540, -0.02 + 0.004 * u)
        MU.escritorio().pegar(h, 1.0, oscuro=0.85)
        h.pieza(PR.rot(C.rect(470, 130, 980, 820), 0.02, np.array([960, 540])), 150, 20, w=7, luz=(0.2, -1), d=16, trama=0.5, rim=0.3)
        h.pieza(PR.rot(C.rect(470, 90, 330, 60), 0.02, np.array([960, 540])), 150, 21, w=6, luz=(0.2, -1), d=8, trama=0.4, rim=0.3)
        with C.fijo(h):
            N.texto_maquina(h, "EXPEDIENTE", 560, 220, 56, t, -99, cps=1e9, tono=0.06, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, "La videollamada donde", 560, 330, 50, t, -99, cps=1e9, tono=0.06, encuadrar=False)
            N.texto_maquina(h, "nadie era real", 560, 400, 50, t, -99, cps=1e9, tono=0.06, encuadrar=False)
            N.texto_maquina(h, "Hong Kong, enero de 2024", 560, 500, 36, t, -99, cps=1e9, tono=0.12, encuadrar=False)
        N.sello(h, "CASO ABIERTO", 1010, 700, 130, t, self.t_caso + 0.25, rot=-9, tono=0.04)
        h.ambiente[:] = 0.40
        h.luz_radial(960, 480, 1300, (1.0, 1.0, 1.0), k=1.0)
        N.lluvia(h, t, n=300, capas=(0.9, 1.0), vel=2000, k=0.5)
        N.salpicaduras(h, t, 0, H, n=30, k=0.7, ritmo=1.6)
        osc = 1.0 - 0.9 * smooth(clamp01((t - (self.t1 - 1.6)) / 1.5))
        return h.acabado(t, niebla=None, oscuro=osc)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "zumbido_lampara", 0.5, 0.0, dur=self.t_ver - self.t0)
        self.ev(self.t_vida, "calada", 0.6, -0.5, dur=1.4)
        self.ev(self.t_temblaba - 0.3, "grave_inquietante", 0.7, 0.3, dur=2.5)
        self.ev(self.t_ahora - 0.35, "camara_zoom", 0.7, 0.0)
        self.ev(self.t_tiembla - 0.2, "sello_golpe", 0.8, -0.4)
        self.ev(self.t_suya - 0.5, "caida", 0.8, 0.3, dur=0.9)
        self.ev(self.t_suya + 0.3, "corona_cae", 0.7, 0.4)
        self.ev(self.t_ver - 0.35, "sombra_crece", 0.6, 0.0, dur=2.5)
        self.ev(self.t_ver, "lluvia_amb", 0.8, 0.0, dur=self.t1 - self.t_ver)
        self.ev(self.t_ver, "tecleo_rapido", 0.6, -0.4, dur=0.9)
        self.ev(self.t_pues, "tachon", 1.0, -0.4)
        self.ev(self.t_alcanza - 0.5, "sello_golpe", 0.9, -0.3)
        self.ev(self.t_caso - 0.5, "tinta_mancha", 0.6, 0.0, dur=0.8)
        self.ev(self.t_caso + 0.25, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_caso + 0.3, "trueno_noir", 0.8, 0.0, dur=4.0)
