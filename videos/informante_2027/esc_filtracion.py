# -*- coding: utf-8 -*-
"""Escena 13 «filtracion»: octubre, una mano desliza el sobre por la ranura de la puerta de la redacción; el espejo: Daniel a
un lado y, al otro, su silueta (el informante que él mismo escribió); el titular que da la vuelta al mundo (tres periódicos);
la sala del comité: diez personas bajo las lámparas."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos27 as M27
import noir as N
import props as PR
from basen import BaseNoir
from comite import Comite
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import elipse_, pulso


class Filtracion(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.com = Comite()
        self.t_oct = w("Octubre")
        self.t_alguien = w("Alguien")
        self.t_filtra = w("filtra")
        self.t_period = w("periódico")
        self.t_fijate = w("Fíjate")
        self.t_hombre = w("El hombre")
        self.t_inf = w("informante")
        self.t_ypuso = w("Y puso")
        self.t_decisivo = w("decisivo")
        self.t_titular = w("El titular")
        self.t_mundo = w("mundo")
        self.t_una = w("una inteligencia")
        self.t_control = w("control")
        self.t_decision = w("Y la decisión")
        self.t_diez = w("diez")
        self.t_direct = w("Directivos")
        self.t_china = w("Con China")
        self.t_dosm = w("dos meses")
        self.plano(t0, self.p_sobre)
        self.plano(self.t_fijate - 0.35, self.p_espejo, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_titular - 0.35, self.p_titular, tr="relampago", dur=0.6)
        self.plano(self.t_decision - 0.35, self.p_sala, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ el sobre
    def p_sobre(self, h, t, u):
        h.camara(1.0 + 0.016 * u, 980 + 8 * u, 540, 0.0)
        K.pared(h, 50, 16, ladrillo=True)
        K.plano_(h, C.rect(-300, 940, W + 600, 400), 44, 8, grad=(12, 940, 1200))
        K.puerta(h, 1060, 150, 460, 790, sem=20, tono=30, vidrio="REDACCIÓN", t=t, rendija=0.5)
        K.plano_(h, C.rect(1190, 640, 200, 26), 6, 40)                                   # la ranura del correo
        h.anillo(h.tf(C.rect(1184, 634, 212, 38)), 5 * h.zoom, 41, color=(170, 170, 170), jit=0.4)
        ida = smooth(clamp01((t - self.t_alguien + 0.2) / (self.t_filtra - self.t_alguien + 0.6)))
        ent = smooth(clamp01((t - self.t_filtra - 0.2) / 0.5))
        mx = 100 + 880 * ida
        if ent < 1:
            PR.sobre(h, mx + 230 + 150 * ent, 650, 0.62 * (1 - 0.6 * ent), ang=0.05, sem=60, texto="" if ent > 0.2 else "MEMO", t=t)
        PR.mano(h, mx - 80 * ent, 665, 1.15, ang=0.0, d=1, sem=80, dedos=0.3 + 0.6 * ent, manga=30)
        C.banda(h, "OCTUBRE DE 2027", 430, 110, 64, t, self.t_oct, sem=5)
        C.banda(h, "ALGUIEN DE DENTRO", 430, 210, 46, t, self.t_alguien, claro=True, sem=6)
        C.banda(h, "FILTRA EL MEMORANDO", 430, 990, 54, t, self.t_filtra, sem=7)
        h.ambiente[:] = 0.4
        h.luz_cono(1290, -300, math.pi / 2, 0.36, 1700, (1.5, 1.5, 1.5), suave=0.5)
        h.luz_radial(mx + 100, 660, 420, (1.0, 1.0, 1.0), k=0.9)
        N.lluvia(h, t, n=260, vel=1700, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=300, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ el informante escribió a otro informante
    def p_espejo(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 530, 0.0)
        K.pared(h, 60, 24, paneles=9)
        K.plano_(h, C.rect(-300, 960, W + 600, 400), 44, 8, grad=(12, 960, 1200))
        s = 1.45
        base = dict(y=300 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.9, mira=0.0, cabeza=0.03 * math.sin(t * 0.8))
        self.dan.dibujar(h, dict(x=520, **base, **K.DAN))
        # el marco del espejo y, dentro, la misma figura en tinta: el personaje
        ap = smooth(clamp01((t - self.t_ypuso + 0.3) / 0.6))
        h.pieza(C.rect(1040, 90, 720, 900), 30, 40, w=10, luz=(0, -1), d=14, trama=0.5, rim=0.8)
        K.plano_(h, C.rect(1080, 130, 640, 820), 170, 41, grad=(90, 130, 950))
        if ap < 1:                                                   # primero, su reflejo; luego, el personaje en tinta
            self.dan.dibujar(h, dict(x=1400, **base, **K.DAN))
        if ap > 0:
            h.silueta = ((12, 12, 12), ap)
            self.dan.dibujar(h, dict(x=1400, **base, **K.DAN))
            h.silueta = None
            N.texto_maquina(h, "?", 1400, 300, 150, t, self.t_ypuso + 0.4, cps=1e9, tono=0.95, centro=True, fuente=K.IMPACT, encuadrar=False)
        h.pieza(C.rect(1040, 950, 720, 60), 30, 44, w=8, luz=(0, -1), d=8, trama=0.4, rim=0.8)
        C.banda(h, "EL AUTOR: FUE INFORMANTE", 520, 110, 46, t, self.t_inf - 0.3, sem=5)
        C.banda(h, "SU PERSONAJE: OTRO INFORMANTE", 1400, 60, 44, t, self.t_ypuso + 0.5, claro=True, sem=6)
        C.banda(h, "FÍJATE EN EL DETALLE", 520, 1010, 46, t, self.t_fijate, claro=True, sem=7)
        h.ambiente[:] = 0.36
        h.luz_cono(520, -420, math.pi / 2, 0.3, 1900, (1.6, 1.6, 1.6), suave=0.5)
        h.luz_cono(1400, -420, math.pi / 2, 0.3, 1900, (1.4, 1.4, 1.4), k=0.55 + 0.45 * ap, suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el titular da la vuelta al mundo
    def p_titular(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M27.redaccion().pegar(h, 1.0, oscuro=0.8)
        h.ambiente[:] = 0.5
        h.luz_persiana(np.array([[1100, -300], [2200, -340], [2200, 760], [900, 1000]]), k=1.1, n=16, abierto=0.5)
        N.motas(h, t, n=90, k=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        tit = "IA SECRETA, FUERA DE CONTROL"
        PR.periodico(h, t, self.t_titular - 0.2, tit, "Un informante lo advierte desde dentro", cx=520, cy=360, dur=0.7, s=0.62, sem=60,
                     cabecera="NUEVA YORK")
        PR.periodico(h, t, self.t_mundo - 0.5, tit, "Los laboratorios callan", cx=1400, cy=420, dur=0.7, s=0.62, sem=160, cabecera="LONDRES")
        PR.periodico(h, t, self.t_una - 0.2, tit, "«Piden detenerla»: el memorando interno", cx=960, cy=620, dur=0.8, s=1.0, sem=260,
                     cabecera="EDICIÓN MUNDIAL")
        g = pulso(t, self.t_una + 0.6, 0.3, 1.0)
        C.banda(h, "FUERA DE CONTROL", 960, 1010, 80, t, self.t_control - 0.5, sem=5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=1080, sube=False), bloom=0.45, flash=0.22 * g)

    # ------------------------------------------------------------------ una sala con diez personas
    def p_sala(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 520, 0.0)
        self.com.dibujar(h, t, lamparas=1.0)
        C.banda(h, "10 PERSONAS", 960, 110, 100, t, self.t_diez - 0.2, sem=5)
        C.banda(h, "DIRECTIVOS Y FUNCIONARIOS", 960, 230, 46, t, self.t_direct, claro=True, sem=6)
        C.banda(h, "CHINA: A SOLO 2 MESES", 960, 1010, 64, t, self.t_china + 0.4, sem=7)
        h.ambiente[:] = 0.34
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.6, 0.0, dur=self.t_fijate - t0)
        self.ev(self.t_oct, "sello_golpe", 0.8, -0.3)
        self.ev(self.t_filtra - 0.2, "sobre_desliza", 1.0, 0.2)
        self.ev(self.t_filtra, "sello_golpe", 0.8, -0.3)
        self.ev(self.t_fijate - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_inf - 0.3, "sello_golpe", 0.8, -0.3)
        self.ev(self.t_ypuso - 0.3, "sombra_crece", 0.7, 0.3, dur=2.0)
        self.ev(self.t_ypuso + 0.5, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_titular - 0.35, "relampago_corto", 0.6, 0.0)
        self.ev(self.t_titular, "teletipo", 0.5, 0.0, dur=self.t_decision - self.t_titular)
        for k, tk in enumerate((self.t_titular - 0.2, self.t_mundo - 0.5, self.t_una - 0.2)):
            self.ev(tk, "periodico_gira", 0.8, -0.4 + 0.4 * k, dur=0.7)
            self.ev(tk + 0.6, "periodico_golpe", 0.8 + 0.1 * k, -0.4 + 0.4 * k)
        self.ev(self.t_control - 0.5, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_decision - 0.2, "puerta", 0.8, 0.0)
        self.ev(self.t_decision, "zumbido_lampara", 0.5, 0.0, dur=self.t1 - self.t_decision)
        self.ev(self.t_diez - 0.2, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_china + 0.4, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_china + 0.4, "reloj_pared", 0.6, 0.0, dur=self.t1 - self.t_china - 0.6)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
