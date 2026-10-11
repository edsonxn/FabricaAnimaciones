# -*- coding: utf-8 -*-
"""Escena 3 «sospechoso»: el detective entra en la sala de interrogatorio; enfrente, la caja negra con su luz que late · reglas
escritas a máquina que se tachan (video real entintado) · un árbol de tinta que CRECE como una red de neuronas · páginas de libros
(video) y palabras que entran a la caja · pared de perillas (miles de millones de ajustes) · la siguiente palabra · ajedrez que
juega solo · la sombra de la caja finge ser un hombre (mentir) · linterna dentro de la caja: túnel de números · se apaga la luz."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
import props2 as P2
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Detective, avance_paso
from toon import Pista, elipse_, pulso

CAJA = (900.0, 880.0)
LAMP = (900.0, -650.0)


class Sospechoso(BaseNoir):
    TR_SALIDA = ("fundido", 0.7)

    def armar(self):
        w = self.w
        self.det = Detective(sem=3)
        self.t_sosp = w("sospechoso", fin=True)
        self.t_desc = w("descubrí")
        self.t_prog = w("programó")
        self.t_crees = w("crees")
        self.t_nadie = w("Nadie escribió")
        self.t_linea = w("línea por línea")
        self.t_crecer = w("crecer")
        self.t_dieron = w("Le dieron")
        self.t_human = w("humanidad")
        self.t_ajustes = w("ajustes")
        self.t_predecir = w("predecir")
        self.t_palabra = w("palabra", fin=True)
        self.t_algun = w("Y en algún")
        self.t_razonar = w("razonar")
        self.t_planear = w("planear")
        self.t_mentir = w("mentir")
        self.t_inq = w("Lo inquietante")
        self.t_adentro = w("adentro")
        self.t_son = w("Son números")
        self.t_caja = w("caja negra")
        self.t_apagada = w("apagada")
        te = self.t0
        self.camina = Pista([(te, 2150.0), (self.t_sosp + 0.3, 1380.0, "o")])
        self.cam1 = Pista([(te, (1250, 400, 0.82)), (self.t_sosp + 0.3, (1150, 410, 0.9), "io"), (self.t_prog, (950, 360, 1.25), "io"),
                           (self.t_nadie, (920, 340, 1.4), "l")])
        self.plano(te, self.p_sala)
        self.plano(self.t_nadie - 0.3, self.p_reglas, tr="barrido", dur=0.5, dirx=1)
        self.plano(self.t_crecer - 0.15, self.p_arbol, tr="tinta", dur=0.6)
        self.plano(self.t_dieron - 0.2, self.p_libros, tr="empuje", dur=0.6)
        self.plano(self.t_ajustes - 0.5, self.p_perillas, tr="barrido", dur=0.45, dirx=-1)
        self.plano(self.t_predecir - 0.3, self.p_palabra, tr="humo", dur=0.5)
        self.plano(self.t_algun - 0.2, self.p_ajedrez, tr="barrido", dur=0.5, dirx=1)
        self.plano(self.t_mentir - 0.35, self.p_sombra, tr="relampago", dur=0.35)
        self.plano(self.t_inq - 0.2, self.p_linterna, tr="empuje", dur=0.6, centro=(W * 0.47, H * 0.5))
        self.plano(self.t_son - 0.25, self.p_numeros, tr="empuje", dur=0.6)

    # ------------------------------------------------------------------ la sala
    def sala(self, h, t, lamp_k=1.0, sombra_humana=0.0):
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.8)
        P2  # noqa
        PR.caja_negra(h, CAJA[0], CAJA[1] - 60, s=1.0, led=1.0, t=t, sem=11)
        PR.mesa(h, 900, 790, ancho=900, fondo=150, alto=110, tono=54, sem=3)
        sw = 0.05 * math.sin(t * 1.4)
        PR.lampara_colgante(h, LAMP[0], LAMP[1], largo=700, ang=sw, k=lamp_k, s=1.1, abre=0.5, alcance=1500, sem=30)

    def p_sala(self, h, t, u):
        cx, cy, z = self.cam1(t)
        h.camara(z, cx, cy, 0.0)
        self.sala(h, t)
        x = float(self.camina(t))
        anda = clamp01((self.t_sosp + 0.3 - t) / 0.4)
        p = dict(x=x, y=900, s=1.0, d=-1, luz=(-0.5, -1), andar=anda, paso=(2150 - x) / avance_paso(Detective.ZANCADA, 1.0), viento=0.1, fumar=0.0, hombros=0.2)
        # la puerta abierta: un rectángulo de luz del pasillo detrás de él (entra en silueta) y la luz derramada en el suelo
        h.emitir(np.array([[1950, -230], [2240, -230], [2240, 900], [1950, 900]]), 0.85, blur=2.0)
        h.luz_persiana(np.array([[1950, 900], [2240, 900], [1700, 1100], [1050, 1100]]), k=0.9, tipo="liso", suave=6)
        h.luz_radial(2100, 500, 1100, (0.9, 0.9, 0.9), k=0.8)
        self.det.dibujar(h, p)
        if t > self.t_prog:                                 # las reglas que nadie escribió: líneas en la pared que se tachan
            for k, s in enumerate(("SI ve_un_gato ENTONCES di 'gato'", "SI pregunta ENTONCES responde", "REGLA 3: no mentir")):
                N.texto_maquina(h, s, 120, -140 + k * 70, 34, t, self.t_prog + 0.15 * k, cps=40, tono=0.85,
                                borrar=(self.t_crees - 0.3 + 0.1 * k, 0.6))
        h.ambiente[:] = 0.30
        N.motas(h, t, n=80, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.25, vel=12, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ reglas tachadas (video real)
    def p_reglas(self, h, t, u):
        N.clip_noir(h, "maquina_0", t, self.t_nadie - 0.3, inicio=0.5, z0=1.05, z1=1.25, dur=3.0, tinta=0.6, poster=0.4)
        h.camara(1.0, W / 2, H / 2, 0.0)
        for k, s in enumerate(("10  SI x > 0 ENTONCES ...", "20  SI ... ENTONCES ...", "30  IR A 10")):
            N.texto_maquina(h, s, 300, 160 + k * 90, 52, t, self.t_nadie + 0.2 + 0.25 * k, cps=40, tono=0.04)
        tx = clamp01((t - self.t_linea - 0.2) / 0.35)
        if tx > 0:                                         # una X enorme de tinta tacha las reglas
            h.trazo(np.array([[220, 120], [220 + 900 * tx, 120 + 300 * tx]]), 26, 7, color=gris(8), taper=(0.1, 0.3))
            h.trazo(np.array([[1120, 120], [1120 - 900 * tx, 120 + 300 * tx]]), 26, 8, color=gris(8), taper=(0.1, 0.3))
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ lo hicieron crecer
    def p_arbol(self, h, t, u):
        h.camara(1.0 + 0.08 * u, W / 2, H / 2 + 60 - 40 * u, 0.0)
        h.img[:] = 0.62                                      # papel bajo la lámpara
        g = smooth(clamp01(u / 1.6))
        P2.arbol_tinta(h, W / 2, 1000, 1.25, g * 1.25, sem=2)
        h.pieza(elipse_(W / 2, 1006, 30, 14, n=16), 40, 5, w=4, luz=(0, -1), d=4, trama=0)       # la semilla
        h.ambiente[:] = 0.55
        h.luz_radial(W / 2, 200, 1100, (1.0, 1.0, 1.0))
        return h.acabado(t, niebla=None, bloom=0.6)

    # ------------------------------------------------------------------ todo lo escrito (video real) entra en la caja
    def p_libros(self, h, t, u):
        N.clip_noir(h, "libros_2", t, self.t_dieron - 0.2, inicio=1.0, vel=1.6, z0=1.0, z1=1.12, dur=4.0, tinta=0.6, poster=0.4)
        palabras = ["amor", "guerra", "ley", "dios", "dinero", "miedo", "verdad", "poder", "λόγος", "logos", "yo", "love", "muerte", "nunca",
                    "siempre", "mentira", "ciencia", "hambre"]
        for k, s in enumerate(palabras):                      # palabras que vuelan hacia el centro (hacia la caja)
            r = np.random.default_rng(k + 70)
            t0 = self.t_dieron + 0.12 * k
            if t < t0:
                continue
            a = clamp01((t - t0) / 1.6)
            ang = r.uniform(0, 6.28)
            R = (1 - e_inout(a)) * r.uniform(700, 1000)
            x, y = W / 2 + math.cos(ang) * R * 1.4, H / 2 + math.sin(ang) * R * 0.8
            N.texto_maquina(h, s, x + 3, y + 3, 40 + 30 * (1 - a), t, -99, cps=1e9, tono=0.0, alfa=0.9 * (1 - a ** 3), centro=True)
            N.texto_maquina(h, s, x, y, 40 + 30 * (1 - a), t, -99, cps=1e9, tono=0.97, alfa=1 - a ** 3, centro=True)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ miles de millones de ajustes
    def p_perillas(self, h, t, u):
        z = 1.25 - 0.3 * smooth(clamp01(u / 3.5))
        h.camara(z, W / 2, H / 2, 0.0)
        h.img[:] = 0.18
        P2.perillas(h, t, self.t_ajustes, cols=30, filas=17, x0=W / 2 - 15 * 68, y0=H / 2 - 8 * 68)
        N.sello(h, "×1.000.000.000", W / 2, H / 2, 110, t, self.t_ajustes + 0.4, rot=-5, tono=0.97)
        h.ambiente[:] = 0.35
        h.luz_radial(W / 2, H / 2 - 100, 1000, (1.2, 1.2, 1.2))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la siguiente palabra
    def p_palabra(self, h, t, u):
        h.camara(1.0 + 0.05 * u, W / 2, H / 2, 0.01)
        h.img[:] = 0.78
        tx = self.t_predecir - 0.1
        N.texto_maquina(h, "El detective encendió un", 220, 420, 60, t, tx, cps=30, tono=0.05)
        cand = [("cigarro", 61), ("fósforo", 22), ("auto", 4), ("farol", 2)]
        fin = self.t_palabra
        for k, (s, pc) in enumerate(cand):
            t1 = tx + 0.9 + 0.12 * k
            if t < t1:
                continue
            y = 560 + k * 74
            elegido = t > fin and k == 0
            N.texto_maquina(h, f"{s:<9s} {pc:>3d} %", 1180, y, 46, t, t1, cps=1e9, tono=0.05 if (k == 0) else 0.35,
                            alfa=1.0 if (t < fin or k == 0) else 0.25)
            ww = 420 * pc / 61 * clamp01((t - t1) / 0.4)
            h.pieza(PR.rect(1180, y + 56, ww, 10), 30 if k == 0 else 120, 300 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0,
                    linea=False)
            if elegido:
                N.texto_maquina(h, "cigarro.", 1140, 420, 60, t, fin, cps=1e9, tono=0.05)
        h.ambiente[:] = 0.6
        h.luz_radial(W / 2, H / 2, 1300, (0.8, 0.8, 0.8))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ ajedrez que juega solo
    def p_ajedrez(self, h, t, u):
        h.camara(1.0 + 0.06 * u, W / 2, H / 2 + 30, 0.0)
        h.img[:] = 0.06
        movs = [(self.t_razonar - 0.1, "peon", (4, 1), (4, 3)), (self.t_planear - 0.1, "caballo", (6, 0), (5, 2)),
                (self.t_planear + 0.8, "alfil", (5, 0), (2, 3))]
        P2.ajedrez(h, t, movs, cx=W / 2, cy=980, ancho=1500, prof=560)
        h.ambiente[:] = 0.25
        h.luz_cono(W / 2, -500, math.pi / 2, 0.55, 1900, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=60, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.15, vel=8, y0=0, y1=600, sube=False))

    # ------------------------------------------------------------------ mentir: la sombra finge
    def p_sombra(self, h, t, u):
        h.camara(1.05, 700, 380, 0.0)
        self.sala(h, t, lamp_k=0.0)
        # sombra en la pared: la caja proyecta la silueta de un hombre con sombrero
        k = smooth(clamp01((t - self.t_mentir) / 0.6))
        h.silueta = ((8, 8, 8), 0.85)
        sx = 300 + 40 * u
        if k < 1:
            P = PR.rect(sx - 140, 120, 280, 650)
            h.pieza(P, 10, 70, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=1 - k, linea=False)
        if k > 0:
            sil = Detective(sem=90)
            sil.dibujar(h, dict(x=sx, y=900, s=1.45, d=1, luz=(0, -1), fumar=0.0, viento=0.1, cigarro=False))
        h.silueta = None
        h.ambiente[:] = 0.18
        h.luz_cono(2600, 380, math.pi, 0.35, 3200, (1.4, 1.4, 1.4), suave=0.5)      # foco desde la derecha
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ la linterna dentro de la caja
    def p_linterna(self, h, t, u):
        h.camara(2.2 + 0.4 * smooth(clamp01(u / 4)), CAJA[0], CAJA[1] - 330, 0.0)
        self.sala(h, t, lamp_k=0.3)
        ab = smooth(clamp01((t - self.t_inq - 0.4) / 1.0))
        cx, cy = CAJA[0], CAJA[1] - 60 - 520 / 2 + 20
        if ab > 0:
            P2.tunel_numeros(h, t, cx, cy, k=ab * 0.9)
        # mano con linterna que entra desde la derecha
        mx = CAJA[0] + 330 - 60 * smooth(clamp01(u / 1.2))
        PR.mano(h, mx, CAJA[1] - 330, s=0.55, ang=0.1, d=-1, tono=140, sem=8, dedos=0.0, manga=70)
        h.pieza(PR.rot(PR.rect(mx - 120, CAJA[1] - 350, 110, 36), 0.1, np.array([mx, CAJA[1] - 330])), 50, 9, w=3, luz=(0, -1), d=4,
                trama=0, rim=0.9)
        h.ambiente[:] = 0.16
        h.luz_cono(mx - 120, CAJA[1] - 336, math.pi + 0.1, 0.28, 900, (1.8, 1.8, 1.8), suave=0.4)
        N.texto_maquina(h, "¿qué hay adentro?", CAJA[0], CAJA[1] - 640, 30, t, self.t_adentro, cps=30, tono=0.9, centro=True)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ números y la luz que se apaga
    def p_numeros(self, h, t, u):
        N.clip_noir(h, "codigo_3", t, self.t_son - 0.25, inicio=2.0, z0=1.1, z1=1.6, dur=5.0, tinta=0.5, poster=0.3, trama=0.3)
        h.camara(1.0, W / 2, H / 2, 0.0)
        for k in range(26):                                  # columnas de cifras que caen
            r = np.random.default_rng(k)
            x = 40 + k * 72
            v = r.uniform(120, 300)
            y = (t * v + r.uniform(0, 1200)) % 1300 - 150
            fila = "".join(str(d) for d in r.integers(0, 10, 6))
            for j, c in enumerate(fila):
                N.texto_maquina(h, c, x + 2, y - j * 46 + 2, 44, t, -99, cps=1e9, tono=0.0, alfa=0.8)
                N.texto_maquina(h, c, x, y - j * 46, 44, t, -99, cps=1e9, tono=0.97, alfa=0.35 + 0.65 * (j == 0))
        h.ambiente[:] = 1.0
        apaga = smooth(clamp01((t - self.t_apagada) / 0.25))
        return h.acabado(t, niebla=None, oscuro=1 - 0.85 * apaga)        # ni en el apagón queda negro: las cifras siguen cayendo, tenues

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "zumbido_lampara", 0.4, 0.0, dur=self.t_son - self.t0)
        for k in range(8):
            self.ev(self.t0 + 0.2 + k * 0.48, "paso_madera", 0.6, 0.5 - 0.08 * k)
        self.ev(self.t0 + 0.1, "puerta", 0.6, 0.6)
        self.ev(self.t_prog, "tecleo_rapido", 0.4, -0.4, dur=1.0)
        self.ev(self.t_crees - 0.3, "tachon", 0.6, -0.4)
        self.ev(self.t_nadie - 0.3, "barrido_aire", 0.5, 0.4, dur=0.5)
        self.ev(self.t_nadie + 0.2, "tecleo_rapido", 0.6, 0.0, dur=1.6)
        self.ev(self.t_linea + 0.2, "tachon", 0.9, 0.0)
        self.ev(self.t_crecer - 0.15, "tinta_mancha", 0.6, 0.0, dur=0.6)
        self.ev(self.t_crecer, "crecer", 0.8, 0.0, dur=2.0)
        self.ev(self.t_dieron - 0.2, "paginas", 0.8, 0.0, dur=3.2)
        self.ev(self.t_ajustes - 0.5, "barrido_aire", 0.5, -0.4, dur=0.45)
        self.ev(self.t_ajustes, "perillas", 0.7, 0.0, dur=2.6)
        self.ev(self.t_ajustes + 0.4, "sello_golpe", 0.8, 0.0)
        tx = self.t_predecir - 0.1
        for i in range(len("El detective encendió un")):
            self.ev(tx + i / 30, "tecla", 0.4, -0.2, tono=1.0 + 0.03 * (i % 5))
        self.ev(self.t_palabra, "carro_maquina", 0.6, 0.3)
        self.ev(self.t_razonar - 0.1, "pieza_ajedrez", 0.8, 0.0)
        self.ev(self.t_planear + 0.6, "pieza_ajedrez", 0.8, 0.2)
        self.ev(self.t_planear + 1.5, "pieza_ajedrez", 0.8, -0.2)
        self.ev(self.t_mentir - 0.35, "relampago_corto", 0.6, 0.0)
        self.ev(self.t_mentir, "grave_inquietante", 0.9, 0.0, dur=2.5)
        self.ev(self.t_inq + 0.3, "linterna_click", 0.8, 0.5)
        self.ev(self.t_inq + 0.4, "tunel", 0.7, 0.0, dur=3.2)
        self.ev(self.t_son - 0.25, "datos", 0.6, 0.0, dur=self.t_apagada - self.t_son + 0.3)
        self.ev(self.t_apagada, "interruptor", 1.0, 0.0)
