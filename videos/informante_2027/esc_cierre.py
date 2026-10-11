# -*- coding: utf-8 -*-
"""Escena 20 «cierre»: el detective ante su ventana, con el expediente sobre el escritorio; Daniel vuelve a casa bajo la lluvia
(la casa de su familia, encendida); el pasillo y la puerta cerrada de la sala, con luz por debajo y sombras que pasan; primer
plano del detective: las dos preguntas a máquina; lanza la colilla; la carpeta recibe el sello «CASO ABIERTO»."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
from basen import BaseNoir
from comite import jardin
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto, Detective
from toon import Pista, elipse_, pulso


class Cierre(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.busto = Busto(sem=5)
        self.t_nose = w("No sé")
        self.t_ojala = w("Ojalá")
        self.t_eldice = w("Él dice")
        self.t_pero = w("Pero conozco")
        self.t_nadie = w("nadie arriesga")
        self.t_fortuna = w("fortuna")
        self.t_cree = w("cree", fin=True)
        self.t_ensu = w("En su expediente")
        self.t_destino = w("destino")
        self.t_diez = w("diez personas")
        self.t_cerrada = w("cerrada")
        self.t_yosolo = w("Yo solo")
        self.t_quien = w("Quién está")
        self.t_ysi = w("Y si alguien")
        self.t_avisar = w("avisar", fin=True)
        self.t_caso = w("Caso")
        self.plano(t0, self.p_ventana)
        self.plano(self.t_pero - 0.35, self.p_casa, tr="humo", dur=0.8)
        self.plano(self.t_ensu - 0.35, self.p_puerta, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_yosolo - 0.35, self.p_busto, tr="empuje", dur=0.6, centro=(W * 0.3, H * 0.5))
        self.plano(self.t_caso - 0.5, self.p_sello, tr="relampago", dur=0.6)

    # ------------------------------------------------------------------ no sé si tiene razón
    def p_ventana(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 1020 + 10 * u, 480, 0.006 * math.sin(t * 0.5))
        MU.oficina().pegar(h, 1.0)
        fum = pulso(t, self.t_ojala - 1.2, 1.8, 1.0)
        p = dict(x=900.0, y=905.0, s=1.0, d=1, luz=(1.0, -0.5), fumar=fum, giro=0.6, viento=0.06, hombros=0.2)
        self.det.dibujar(h, p)
        tip = self.det.punta_cigarro(p)
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4)
        h.luz_radial(tip[0], tip[1], 90 + 120 * fum, (0.6, 0.6, 0.6), k=0.6 + fum)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=90, k=0.8)
        h.ambiente[:] = 0.30
        h.luz_persiana(np.array([[60, -420], [1080, -470], [1080, 640], [-80, 900]]), k=1.4, n=15, abierto=0.5)
        h.luz_radial(1550, 60, 760, (1.0, 1.0, 1.0), k=3.0)
        N.motas(h, t, n=90, k=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "¿Tiene razón?", 1100, 140, 60, t, self.t_nose, cps=16, tono=0.95, encuadrar=False)
        N.texto_maquina(h, "Ojalá se equivoque.", 1100, 240, 44, t, self.t_ojala, cps=20, tono=0.9, encuadrar=False)
        N.texto_maquina(h, "Él dice lo mismo.", 1100, 310, 44, t, self.t_eldice, cps=20, tono=0.97, encuadrar=False)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ nadie arriesga la fortuna de su familia por nada
    def p_casa(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960 - 8 * u, 560, 0.0)
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.6, tono_bruma=0.34)
        jardin(h, t, fr=0.0, amp=0.2, luz_v=1.0)
        av = smooth(clamp01((t - self.t_pero) / (self.t_ensu - self.t_pero)))
        K.caminante(h, 1850 - 800 * av, 1040, 0.9, fase=K.fase_paso(800 * av, 0.9), sem=200, tono=40, d=-1, luz=(-0.6, -0.8), rim=0.95)
        h.ambiente[:] = 0.75
        h.luz_radial(700, 700, 1000, (1.0, 1.0, 1.0), k=1.1)
        N.lluvia(h, t, n=420, vel=1600, k=0.7)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "NADIE ARRIESGA ESTO", 1420, 150, 64, t, self.t_nadie + 0.2, sem=5)
        C.banda(h, "POR UNA HISTORIA EN LA QUE NO CREE", 1400, 260, 44, t, self.t_cree - 1.4, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.24, y0=300, y1=1080, vel=24), bloom=0.5)

    # ------------------------------------------------------------------ diez personas en una sala cerrada
    def p_puerta(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 1010 + 8 * u, 540 - 4 * u, 0.0)
        K.pared(h, 46, 14, paneles=10)
        K.plano_(h, C.rect(-300, 950, W + 600, 400), 36, 8, grad=(8, 950, 1200))
        for k in (0, 1):                                             # puerta doble de la sala de juntas
            K.puerta(h, 760 + k * 400, 130, 400, 820, sem=20 + k * 10, tono=30, rendija=0.6 + 0.4 * math.sin(t * 1.7) ** 2,
                     vidrio="SALA DE JUNTAS" if k == 0 else "PRIVADO", t=t)
        for q in range(5):                                           # sombras que se mueven al otro lado
            fx = 780 + ((t * 46 + q * 170) % 760)
            K.plano_(h, C.rect(fx, 938, 44, 16), 6, 60 + q, alfa=0.9)
            sx = 820 + ((t * 30 + q * 150) % 660)
            K.plano_(h, np.asarray(elipse_(sx, 300 + 20 * math.sin(q * 2.0), 26, 34, n=14)), 30, 70 + q, alfa=0.45)
        p = dict(x=330.0, y=1010.0, s=1.12, d=1, luz=(1.0, -0.3), fumar=0.0, giro=0.5, viento=0.05, hombros=0.3)
        self.det.dibujar(h, p)
        C.banda(h, "EL DESTINO DEL MUNDO", 440, 100, 54, t, self.t_destino - 0.6, sem=5)
        C.banda(h, "10 PERSONAS", 1500, 100, 80, t, self.t_diez, claro=True, sem=6)
        C.banda(h, "A PUERTA CERRADA", 1500, 210, 50, t, self.t_cerrada - 0.5, sem=7)
        h.ambiente[:] = 0.42
        h.luz_cono(1160, -300, math.pi / 2, 0.42, 1700, (1.3, 1.3, 1.3), k=0.9, suave=0.5)
        h.luz_radial(360, 640, 620, (1.0, 1.0, 1.0), k=1.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.22, vel=10, y0=200, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ las dos preguntas
    def p_busto(self, h, t, u):
        h.camara(1.0 + 0.016 * u, 960, 540, 0.0)
        h.img[:] = 0.05
        tira = clamp01((t - self.t_avisar - 0.2) / 0.6)
        mano = smooth(clamp01((t - self.t_avisar + 0.5) / 0.6))
        br = pulso(t, self.t_yosolo + 0.4, 1.4, 1.0)
        p = dict(x=430, y=540, s=1.16, d=1, luz=(0.9, -0.5), brasa=br, arriba=0.35, rot=-0.02, mano=mano, tira=tira, cigarro=tira < 0.2)
        self.busto.dibujar(h, p)
        if tira < 0.2:
            tip = self.busto.punta(dict(x=430, y=540, s=1.16, d=1))
            N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.0, viento=(30, -120))
            h.luz_radial(tip[0], tip[1], 120 + 140 * br, (0.7, 0.7, 0.7), k=0.6 + br)
        N.texto_maquina(h, "¿QUIÉN ESTÁ EN ESA SALA?", 900, 380, 46, t, self.t_quien, cps=18, tono=0.96, encuadrar=False)
        N.texto_maquina(h, "¿Y ALGUIEN NOS VA A AVISAR?", 900, 500, 46, t, self.t_ysi, cps=18, tono=0.96, encuadrar=False)
        h.ambiente[:] = 0.32
        h.luz_persiana(np.array([[-300, -420], [1400, -470], [1400, 700], [-420, 960]]), k=1.4, n=15, abierto=0.5)
        h.luz_radial(1300, 460, 900, (1.0, 1.0, 1.0), k=0.5)
        N.lluvia(h, t, n=260, vel=1500, k=0.5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ caso abierto
    def p_sello(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, -0.01)
        MU.escritorio().pegar(h, 1.0, oscuro=0.7, dx=-60, dy=30)
        K.taza_arriba(h, 300, 800, 1.2, 90, t)
        K.carpeta(h, 960, 560, 1.15, "2027", t, -99, ang=-0.04, sem=20, px=170, sub="")
        C.banda(h, "CASO ABIERTO", 960, 400, 130, t, self.t_caso + 0.15, sem=9)
        g = pulso(t, self.t_caso + 0.15, 0.3, 1.0)
        osc = smooth(clamp01((t - self.t1 + 2.2) / 1.8))             # la lámpara se va apagando
        h.ambiente[:] = 0.32 * (1 - 0.8 * osc)
        h.luz_cono(960, -620, math.pi / 2, 0.56, 2400, (1.7, 1.7, 1.7), k=1.0 - 0.9 * osc, suave=0.5)
        N.motas(h, t, n=110, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=1080, sube=False), bloom=0.45, flash=0.3 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.8, 0.0, dur=self.t_ensu - t0)
        for ini, n in ((self.t_nose, 13), (self.t_ojala, 19), (self.t_eldice, 17)):
            self.ev(ini, "tecleo_rapido", 0.5, 0.3, dur=n / 19)
            self.ev(ini + n / 19 + 0.05, "carro_maquina", 0.4, 0.4)
        self.ev(self.t_ojala - 1.2, "calada", 0.6, -0.2, dur=1.4)
        for k in range(8):
            self.ev(self.t_pero + 0.3 + k * 0.75, "pasos_mojados", 0.5, 0.6 - 0.12 * k)
        self.ev(self.t_nadie + 0.2, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_ensu - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_ensu, "zumbido_lampara", 0.5, 0.0, dur=self.t_yosolo - self.t_ensu)
        self.ev(self.t_diez, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_cerrada - 0.5, "puerta", 0.9, 0.2)
        self.ev(self.t_yosolo - 0.35, "lluvia_amb", 0.7, 0.0, dur=self.t1 - self.t_yosolo)
        for ini, n in ((self.t_quien, 24), (self.t_ysi, 26)):
            self.ev(ini, "tecleo_rapido", 0.55, 0.3, dur=n / 18)
        self.ev(self.t_avisar + 0.3, "colilla", 0.8, -0.3)
        self.ev(self.t_caso - 0.5, "trueno_noir", 0.9, 0.0, dur=4.0)
        self.ev(self.t_caso + 0.15, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_caso + 0.15, "golpe_grave", 1.0, 0.0)
