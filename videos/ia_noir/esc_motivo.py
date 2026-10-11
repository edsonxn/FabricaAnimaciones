# -*- coding: utf-8 -*-
"""Escena 4 «motivo»: tablero de corcho con fotos e hilos (¿MOTIVO?) · la caja y «ODIO» tachado · la diana con objetivos que
cambian · el rey Midas en TEATRO DE SOMBRAS (lo que toca se vuelve metal brillante; muere de hambre) · apretón de manos cuya sombra
tiene garras (cumple la letra) · dos brújulas que no se alinean (alineación, SIN GARANTÍA)."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
import props3 as P3
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from toon import Pista, elipse_, pulso, tubo, blob


class Motivo(BaseNoir):
    TR_SALIDA = ("humo", 0.7)

    def armar(self):
        w = self.w
        self.t_inv = w("investigación")
        self.t_motivo = w("motivo")
        self.t_problema = w("problema", frase=1)
        self.t_odiarnos = w("odiarnos")
        self.t_objetivo = w("objetivo")
        self.t_cualq = w("Cualquier")
        self.t_rey = w("El rey Midas")
        self.t_tocara = w("tocara")
        self.t_oro = w("oro")
        self.t_obtuvo = w("Obtuvo")
        self.t_pidio2 = w("pidió", n=1)
        self.t_hambre = w("hambre")
        self.t_pedirle = w("Pedirle")
        self.t_trato = w("trato")
        self.t_diablo = w("diablo")
        self.t_letra = w("letra")
        self.t_intencion = w("intención")
        self.t_expertos = w("Los expertos")
        self.t_alin = w("alineación")
        self.t_lograr = w("lograr")
        self.t_nadie = w("nadie sabe")
        self.t_garant = w("garantizarlo")
        self.plano(self.t0, self.p_corcho)
        self.plano(self.t_problema - 0.6, self.p_odio, tr="barrido", dur=0.5, dirx=1)
        self.plano(self.t_objetivo - 0.4, self.p_diana, tr="empuje", dur=0.5)
        self.plano(self.t_rey - 0.35, self.p_midas, tr="tinta", dur=0.7)
        self.plano(self.t_pedirle - 0.3, self.p_trato, tr="barrido", dur=0.5, dirx=-1)
        self.plano(self.t_expertos - 0.3, self.p_brujulas, tr="humo", dur=0.6)

    # ------------------------------------------------------------------ el tablero de la investigación
    def p_corcho(self, h, t, u):
        h.camara(1.08 + 0.12 * smooth(clamp01(u / 4.5)), 900 + 220 * smooth(clamp01(u / 4.5)), 560, -0.02)
        MU.corcho().pegar(h, 1.0)
        fotos = [(260, 200, -0.08), (720, 140, 0.05), (1180, 220, -0.04), (300, 720, 0.06), (760, 760, -0.07)]
        for k, (x, y, a) in enumerate(fotos):
            PR.foto(h, x, y, s=1.4, ang=a, sem=40 + k)
            P3.chincheta(h, x, y - 100, 60 + k)
        P3.tarjeta(h, 260, 360, "TESTIGOS", t, -99, ang=0.03, sem=80)
        P3.tarjeta(h, 1180, 380, "LA CAJA", t, -99, ang=-0.04, sem=82)
        P3.tarjeta(h, 760, 920, "1 EN 10", t, -99, ang=0.05, sem=84)
        P3.tarjeta(h, 1620, 560, "¿MOTIVO?", t, self.t_motivo - 0.1, ang=-0.03, sem=86, s=1.3)
        pins = [(260, 100), (720, 40), (1180, 120), (300, 620), (760, 660)]
        for k, a in enumerate(pins):                          # los hilos van todos al motivo
            P3.hilo(h, a, (1620, 500), smooth(clamp01((t - self.t_inv - 0.25 * k) / 0.7)), sem=90 + k)
        h.ambiente[:] = 0.42
        h.luz_cono(1400, -500, math.pi / 2 + 0.3, 0.6, 1900, (1.2, 1.2, 1.2), suave=0.6)
        h.luz_persiana(np.array([[200, -200], [1700, -260], [2000, 1200], [-100, 1300]]), k=0.35, n=14, abierto=0.5)
        N.humo(h, t, 1900, 1100, k=0.7, ancho=2.5, viento=(-30, -90))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ no necesita odiarnos
    def p_odio(self, h, t, u):
        h.camara(1.6, 900, 560, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.75)
        PR.caja_negra(h, 900, 820, s=1.0, led=1.0, t=t, sem=11)
        PR.mesa(h, 900, 850, ancho=900, fondo=150, alto=110, tono=54, sem=3)
        N.texto_maquina(h, "MOTIVO:", 620, 260, 40, t, self.t_problema, cps=30, tono=0.9)
        N.texto_maquina(h, "ODIO", 840, 260, 40, t, self.t_problema + 0.6, cps=30, tono=0.9, borrar=(self.t_odiarnos, 0.5))
        h.ambiente[:] = 0.25
        PR.lampara_colgante(h, 900, -650, largo=700, ang=0.03 * math.sin(t), k=1.0, s=1.1, abre=0.5, alcance=1500, sem=30)
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ cualquier objetivo
    def p_diana(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.30
        P3.diana(h, W / 2 - 280, H / 2 + 20, 360, sem=5)
        lleg = e_out(clamp01((t - self.t_objetivo - 0.2) / 0.25))
        P3.dardo(h, W / 2 - 280 + 600 * (1 - lleg), H / 2 + 20 - 300 * (1 - lleg), -0.45, s=1.4, sem=20)
        N.texto_maquina(h, "OBJETIVO:", 1020, 300, 56, t, self.t_objetivo, cps=30, tono=0.95)
        metas = ["fabricar clips", "ganar al ajedrez", "curar el cáncer", "vender más", "cualquier cosa"]
        if t > self.t_cualq - 0.1:
            k = min(len(metas) - 1, int((t - self.t_cualq + 0.1) / 0.45))
            N.texto_maquina(h, metas[k], 1020, 400, 52, t, self.t_cualq - 0.1 + 0.45 * k, cps=60, tono=0.95)
        h.ambiente[:] = 0.4
        h.luz_radial(W / 2 - 280, H / 2, 900, (1.3, 1.3, 1.3))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el rey Midas (teatro de sombras)
    def p_midas(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.93                                         # la sábana iluminada desde atrás
        hambre = smooth(clamp01((t - self.t_hambre) / 1.0))
        objs = [("rosa", 1020, 860, self.t_tocara), ("pan", 1260, 860, self.t_obtuvo), ("copa", 1500, 860, self.t_pidio2)]
        # el rey camina de un objeto al siguiente (de pie en el suelo, detrás de la mesa) y estira la mano hasta tocarlo
        claves = [(self.t_rey - 0.4, 520.0), (objs[0][3] - 0.9, 520.0), (objs[0][3] - 0.45, objs[0][1] - 300.0, "o")]
        for k in (1, 2):
            claves += [(objs[k][3] - 0.95, objs[k - 1][1] - 300.0), (objs[k][3] - 0.45, objs[k][1] - 300.0, "o")]
        x_rey = float(Pista(claves)(t))
        anda = 0.0
        for (t0_, *_), (t1_, *_) in zip(claves[1::2], claves[2::2]):
            if t0_ < t < t1_:
                anda = 1.0
        br = 0.0
        for k, (_, ox, _, tk) in enumerate(objs):
            br = max(br, pulso(t, tk - 0.45, 1.3, 1.0))
        P3.rey(h, x_rey, 1080 - 10 * anda * abs(math.sin(t * 9)), s=1.55, brazo=br, caido=hambre, sem=7)
        # mesa de silueta (le tapa las piernas: está detrás)
        h.pieza(PR.rect(900, 860, 760, 30), 10, 3, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
        h.pieza(PR.rect(920, 890, 720, 190), 10, 8, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
        for k, (tipo, ox, oy, tk) in enumerate(objs):
            oro = smooth(clamp01((t - tk - 0.1) / 0.35))
            P3.objeto_oro(h, tipo, ox, oy, 1.1, oro, t, sem=30 + k * 5)
            if 0 < t - tk - 0.1 < 0.4:
                h.luz_radial(ox, oy - 100, 260, (1.0, 1.0, 1.0), k=1.4)
        if hambre > 0:                                          # la corona cae y rueda por el suelo
            cx = x_rey - 120 - 300 * hambre
            cy = 1060
            h.pieza(np.array([(cx - 30, cy), (cx - 36, cy - 44), (cx - 18, cy - 20), (cx - 4, cy - 54), (cx + 8, cy - 20), (cx + 24, cy - 50),
                              (cx + 34, cy)]), int(10 + 200 * hambre), 90, w=3, luz=(0.4, -1), d=4, trama=0, rim=hambre)
        N.texto_maquina(h, "«todo lo que toque se volverá oro»", W / 2, 120, 44, t, self.t_rey + 0.4, cps=30, tono=0.1, centro=True)
        h.ambiente[:] = 1.0 - 0.45 * hambre
        h.luz_radial(W / 2, H / 2, 1400, (0.3, 0.3, 0.3))
        img = h.acabado(t, niebla=None, contraste=6.5, medio=0.42)
        return img

    # ------------------------------------------------------------------ el trato con el diablo
    def p_trato(self, h, t, u):
        h.camara(1.0 + 0.05 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.36
        # sombra en la pared: la mano de la izquierda proyecta garras
        apr = e_out(clamp01((t - self.t_trato + 0.4) / 0.6))
        sac = math.sin(t * 9) * 8 * clamp01((t - self.t_trato) * 2) * (t < self.t_trato + 1.4)
        h.silueta = ((14, 14, 14), 0.75)
        PR.mano(h, W / 2 - 520 + 260 * apr, 300 + sac * 1.6, s=1.7, ang=0.0, d=1, sem=5, dedos=0.9)
        if t > self.t_diablo - 0.2:
            g = smooth(clamp01((t - self.t_diablo + 0.2) / 0.4))
            for k in range(4):                                 # garras que asoman en la sombra
                x0 = W / 2 - 520 + 260 * apr + 1.7 * (60 + (40 + 60 * 0.9))
                y0 = 300 + 1.7 * (-32 + k * 20)
                h.pieza(np.array([[x0, y0 - 8], [x0 + 70 * g, y0 + 10 * g], [x0, y0 + 10]]), 14, 40 + k, w=0, luz=(0, -1), d=1,
                        sombra=0, trama=0, rim=0, linea=False)
            for sx in (-1, 1):                                  # cuernos en la sombra del puño
                bx = W / 2 - 520 + 260 * apr - 40
                h.pieza(np.array([[bx + sx * 30, 230], [bx + sx * 60, 230 - 90 * g], [bx + sx * 5, 236]]), 14, 50 + sx, w=0,
                        luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
        h.silueta = None
        # las dos manos que se estrechan
        PR.mano(h, W / 2 - 240 + 130 * apr, 600 + sac, s=1.2, ang=0.0, d=1, tono=130, sem=10, dedos=0.9, manga=60)
        PR.mano(h, W / 2 + 240 - 130 * apr, 610 - sac, s=1.2, ang=0.0, d=-1, tono=120, sem=20, dedos=0.9, manga=200)
        # el contrato y la lupa
        h.pieza(PR.rot(PR.rect(560, 760, 800, 300), -0.03, np.array([960, 900])), 222, 60, w=3, luz=(0.2, -1), d=6, trama=0, rim=0)
        N.texto_maquina(h, "CONTRATO", 960, 800, 40, t, -99, cps=1e9, tono=0.08, centro=True)
        for k in range(5):
            h.pieza(PR.rect(620, 850 + k * 30, 680, 8), 140, 61 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False,
                    alfa=0.8)
        if t > self.t_letra - 0.4:
            g = smooth(clamp01((t - self.t_letra + 0.4) / 0.4))
            lx, ly = 1080 + 500 * (1 - g), 920 + 200 * (1 - g)            # la lupa entra deslizándose, ya a tamaño completo
            h.pieza(elipse_(lx, ly, 160, 160, n=40), 236, 70, w=10, luz=(0.3, -1), d=8, trama=0, rim=0.9)
            if g > 0.9:
                for k_, s_ in enumerate(("...cumpliré", "exactamente", "lo que digas.")):
                    N.texto_maquina(h, s_, lx, ly - 40 + k_ * 40, 30, t, -99, cps=1e9, tono=0.05, centro=True, encuadrar=False)
            h.pieza(PR.rot(PR.rect(lx + 100, ly + 100, 200, 34), 0.75, np.array([lx + 100, ly + 100])), 30, 71, w=4, luz=(0.3, -1), d=4,
                    trama=0.3, rim=0.8)
        h.ambiente[:] = 0.45
        h.luz_cono(W / 2, -300, math.pi / 2, 0.6, 1700, (1.2, 1.2, 1.2), suave=0.6)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ alineación
    def p_brujulas(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.18
        P3.brujula(h, 560, 500, 300, 0.02 * math.sin(t * 1.3), sem=5, etiqueta="NOSOTROS", t=t, t0=self.t_expertos)
        # la de la máquina: deriva; una mano la empuja a su sitio y se vuelve a ir
        empuje = pulso(t, self.t_lograr - 0.2, 2.2, 1.0)
        deriva = 1.6 * math.sin(t * 0.9) + 0.8 * math.sin(t * 2.3 + 1)
        ang = deriva * (1 - 0.9 * empuje)
        if t > self.t_nadie:
            ang += 2.4 * smooth(clamp01((t - self.t_nadie) / 0.8)) * math.sin(t * 3.1)
        P3.brujula(h, 1360, 500, 300, ang, sem=40, etiqueta="LA MÁQUINA", t=t, t0=self.t_expertos + 0.4)
        if empuje > 0.02:
            PR.mano(h, 1360 + 360 - 150 * empuje, 420, s=0.9, ang=0.25, d=-1, tono=140, sem=60, dedos=1.0)
        N.sello(h, "ALINEACIÓN", W / 2, 120, 80, t, self.t_alin, rot=-3, tono=0.95, marco=False)
        N.sello(h, "SIN GARANTÍA", W / 2, 1000, 84, t, self.t_garant, rot=3, tono=0.95)
        h.ambiente[:] = 0.42
        h.luz_radial(560, 460, 700, (1.0, 1.0, 1.0))
        h.luz_radial(1360, 460, 700, (1.0, 1.0, 1.0))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "reloj_pared", 0.35, -0.3, dur=self.t_problema - self.t0)
        for k in range(5):
            self.ev(self.t_inv + 0.25 * k + 0.5, "hilo_tenso", 0.5, -0.4 + 0.2 * k)
        self.ev(self.t_motivo - 0.1, "chincheta", 0.8, 0.4)
        self.ev(self.t_problema - 0.6, "barrido_aire", 0.5, 0.3, dur=0.5)
        self.ev(self.t_odiarnos, "tachon", 0.7, 0.0)
        self.ev(self.t_objetivo + 0.4, "dardo", 1.0, -0.2)
        for k in range(5):
            self.ev(self.t_cualq - 0.1 + 0.45 * k, "tecleo_rapido", 0.35, 0.3, dur=0.3)
        self.ev(self.t_rey - 0.35, "tinta_mancha", 0.6, 0.0, dur=0.7)
        self.ev(self.t_rey, "caja_musica", 0.5, 0.0, dur=self.t_hambre - self.t_rey + 1.5)
        for tk in (self.t_tocara, self.t_obtuvo, self.t_pidio2):
            self.ev(tk + 0.1, "oro_brillo", 0.8, 0.2)
        self.ev(self.t_hambre + 0.3, "corona_cae", 0.8, 0.3)
        self.ev(self.t_pedirle - 0.3, "barrido_aire", 0.5, -0.3, dur=0.5)
        self.ev(self.t_trato, "apreton", 0.7, 0.0)
        self.ev(self.t_diablo - 0.2, "grave_inquietante", 0.9, 0.0, dur=2.5)
        self.ev(self.t_letra - 0.4, "lupa", 0.5, 0.3)
        self.ev(self.t_expertos - 0.3, "barrido_aire", 0.5, 0.0, dur=0.6)
        self.ev(self.t_lograr - 0.2, "brujula", 0.6, 0.4, dur=2.4)
        self.ev(self.t_alin, "sello_golpe", 0.6, 0.0)
        self.ev(self.t_garant, "sello_golpe", 1.0, 0.0)
