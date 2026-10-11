# -*- coding: utf-8 -*-
"""Escena 6 «veneno»: en la mesa del maestre, el frasco se destapa y los cristales morados ruedan junto a un mapa donde la ruta
se traza desde más allá del mar; corte del cáliz: un cristal cae al vino, se hunde y se deshace en volutas moradas, y a la
derecha una mano se cierra en un puño; un cofre de joyas se abre sobre terciopelo y la cámara entra en una piedra que brilla."""
import math

import numpy as np

import comun as C
import mundos_j2 as M2
import mundos_j3 as M3
import noir as N
import noir_color as NC
import noir_feudal as NF
import props_j as P
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, elipse_, pulso, suave


class Veneno(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_nombre = w("nombre")
        self.t_estr = w("Estrangulador")
        self.t_crist = w("Cristales")
        self.t_mar = w("mar")
        self.t_desh = w("Se deshacen")
        self.t_rastro = w("rastro")
        self.t_garg = w("garganta")
        self.t_puno = w("puño")
        self.t_un = w("Un veneno")
        self.t_bols = w("bolsillo")
        self.t_esc = w("Se esconde")
        self.t_todos = w("todos")
        self.plano(t0, self.p_frasco)
        self.plano(self.t_desh - 0.35, self.p_disuelve, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_un - 0.35, self.p_cofre, tr="humo", dur=0.6)

    def p_frasco(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 7.5))
        h.camara(1.0 + 0.10 * k, 960 + 60 * k, 600, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M2.botica_estantes(), h, 0.7, rampa="madera", dy=60)
        NC.pegar(M2.botica_mesa(), h, 1.0, rampa="madera")
        # mapa de pergamino con la costa y la ruta que llega de oriente
        with h.con_rampa("pergamino"):
            h.pieza(np.array([(1120, 880), (1820, 860), (1840, 1120), (1110, 1140)]), 200, 20, w=3, d=4, trama=0.1, rim=0.3)
        costa = [(1140 + 40 * j, 960 + 40 * math.sin(j * 0.9) + 10 * math.sin(j * 2.3)) for j in range(9)]
        costa2 = [(1500 + 40 * j, 1010 + 30 * math.sin(j * 1.3) + 12 * math.cos(j * 2.1)) for j in range(9)]
        h.trazo(np.array(costa), 3, 21, color=(60, 40, 30), alfa=0.9)
        h.trazo(np.array(costa2), 3, 22, color=(60, 40, 30), alfa=0.9)
        a = clamp01((t - self.t_mar + 0.8) / 1.2)
        if a > 0:
            ruta = np.array([(1800 - 640 * v, 1080 - 120 * math.sin(math.pi * v) - 60 * v) for v in np.linspace(0, a, max(2, int(30 * a)))])
            for j in range(0, len(ruta) - 1, 2):
                h.trazo(ruta[j:j + 2], 4, 23 + j, color=h.c(120, "lacre"), alfa=0.95)
        # el frasco: el tapón salta y los cristales ruedan por la mesa
        ab = smooth(clamp01((t - self.t_crist + 0.3) / 0.5))
        P.frasco(h, t, 760, 900, 1.5, sem=30, brillo=0.6 + 0.4 * ab)
        if ab > 0:
            for i in range(5):
                rr = smooth(clamp01((t - self.t_crist - 0.1 * i) / 0.8))
                P.cristales(h, t, 880 + 70 * i * rr + 30 * i, 960 + 10 * i, 0.5, n=3, sem=40 + i, brillo=rr)
        NF.vela(h, t, 300, 820, s=1.2, sem=50, alto=170, luz=1.1, alcance=1100)
        C.ambiente(h, 0.3)
        C.cartela(h, "El Estrangulador", "cristales de más allá del mar", 960, 160, t, self.t_estr, px=84, sem=7)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=13, vel=8.0), bloom=0.5)

    def p_disuelve(self, h, t, u):
        pal = h.pal
        h.camara(1.0 + 0.02 * u, 960, 540, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M3.terciopelo(), h, 0.4, rampa="vino", oscuro=0.6)
        # el cáliz enorme en corte: la copa con el vino y su superficie ondulada
        cx, top, bot = 640, 260, 860
        with h.con_rampa("oro"):
            h.pieza(suave([(cx - 360, top), (cx + 360, top), (cx + 330, top + 300), (cx + 200, bot - 60), (cx + 60, bot), (cx - 60, bot),
                           (cx - 200, bot - 60), (cx - 330, top + 300)], 4), 150, 60, w=6, d=14, trama=0.3, rim=1.0)
        with h.con_rampa("vino"):
            hon = [(cx - 330 + 660 * v, top + 60 + 8 * math.sin(v * 12 + t * 3)) for v in np.linspace(0, 1, 30)]
            cuerpo = hon + [(cx + 300, top + 300), (cx + 180, bot - 80), (cx + 50, bot - 30), (cx - 50, bot - 30), (cx - 180, bot - 80),
                            (cx - 300, top + 300)]
            h.pieza(suave(cuerpo, 3), 70, 61, w=0, d=0, sombra=0.3, trama=0, rim=0.5)
        # el cristal cae, entra (salpica) y se hunde mientras se deshace
        tc = self.t_desh + 0.1
        if t < tc:
            y = -100 + (top + 60 + 100) * clamp01((t - (tc - 0.6)) / 0.6) ** 2
            P.cristales(h, t, cx, y, 0.6, n=1, sem=70, brillo=1.0)
        else:
            v = t - tc
            yk = top + 70 + 380 * (1 - math.exp(-v * 1.2))
            tam = max(0.0, 1 - v / 2.6)
            if tam > 0:
                P.cristales(h, t, cx + 10 * math.sin(v * 3), yk, 0.6 * tam, n=1, sem=70, brillo=tam)
            for j in range(10):                                                     # volutas moradas que se disuelven
                fj = j / 10
                vv = max(0.0, v - fj * 0.6)
                if vv <= 0:
                    continue
                px = cx + 120 * math.sin(vv * 1.5 + j) * (0.3 + vv * 0.4)
                py = yk - 20 - 60 * vv + 40 * math.sin(j)
                r = 20 + 50 * vv
                al = 0.5 * math.exp(-vv * 0.6)
                h.pieza(elipse_(px, py, r, r * 0.6, rot=j, n=16), 120, 80 + j, w=0, d=0, sombra=0, trama=0, rim=0, alfa=al, linea=False,
                        rampa="purpura")
            if v < 0.6:
                for j in range(8):
                    a = math.pi * (0.1 + 0.8 * j / 7)
                    q = (cx + math.cos(a) * 300 * v, top + 60 - math.sin(a) * 260 * v + 500 * v * v)
                    h.pieza(elipse_(q[0], q[1], 8, 10, n=8), 80, 90 + j, w=1.5, d=1, sombra=0, trama=0, rim=0.9, rampa="vino")
        # el puño que se cierra (la garganta)
        cierra = smooth(clamp01((t - self.t_garg) / 1.2))
        if t > self.t_garg - 0.6:
            ap = smooth(clamp01((t - self.t_garg + 0.6) / 0.4))
            P.puno(h, 1560 + 300 * (1 - ap), 560, 1.5, cierra, sem=100, d=-1)
        C.ambiente(h, 0.3)
        h.luz_radial(640, 300, 900, pal["vela"], k=1.1)
        h.luz_radial(1500, 400, 700, pal["vela"], k=0.8)
        C.banda(h, "SIN DEJAR RASTRO", 640, 980, 52, t, self.t_rastro, claro=True, sem=7)
        C.banda(h, "COMO UN PUÑO", 1500, 980, 56, t, self.t_puno, sem=8)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.5)

    def p_cofre(self, h, t, u):
        pal = h.pal
        abre = smooth(clamp01((t - self.t_esc + 0.4) / 0.9))
        zoom = smooth(clamp01((t - self.t_todos + 0.6) / 1.6))
        h.camara(1.0 + 0.04 * u + 0.9 * zoom, 960 + 120 * zoom, 600 - 40 * zoom, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M3.terciopelo(), h, 1.0, rampa="purpura", oscuro=0.8)
        with h.con_rampa("oro"):                                                     # sortijas y una cadena junto al cofre
            for i, (x, y) in enumerate(((420, 820), (1560, 880), (1500, 760))):
                h.pieza(elipse_(x, y, 36, 26, n=20), 160, 10 + i, w=3, d=4, trama=0, rim=1.0)
                h.pieza(elipse_(x, y, 24, 16, n=20), 30, 13 + i, w=2, d=0, sombra=0, rim=0, rampa="purpura")
        P.cofre(h, t, 960, 840, 1.6, abre=abre, sem=20)
        if abre > 0.4:                                                               # el collar asoma del cofre
            P.collar_grande(h, t, 1080, 560, 0.42, falta=-1, n=7, sem=30, brillo=abre)
        NF.vela(h, t, 300, 760, s=1.1, sem=40, alto=150, luz=1.0, alcance=900)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 500, 900, pal["vela"], k=1.0)
        C.banda(h, "A LA VISTA DE TODOS", 960, 160, 56, t, self.t_todos - 0.2, claro=True, sem=9)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.55)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "chisporroteo", 0.4, -0.3, dur=self.t_desh - t0)
        self.ev(self.t_estr, "grave_inquietante", 0.6, 0.0, dur=4.0)
        self.ev(self.t_crist - 0.3, "desenchufa", 0.6, -0.2)
        self.ev(self.t_crist, "fichas_mezcla", 0.5, 0.0)
        self.ev(self.t_mar - 0.8, "pluma", 0.5, 0.3)
        self.ev(self.t_desh - 0.35, "barrido_aire", 0.5, 0.0, dur=0.55)
        self.ev(self.t_desh + 0.1, "cafe_sirve", 0.5, -0.2)
        self.ev(self.t_rastro, "sombra_crece", 0.5, 0.0, dur=2.5)
        self.ev(self.t_garg, "apreton", 0.8, 0.3)
        self.ev(self.t_un - 0.35, "barrido_aire", 0.5, 0.0, dur=0.6)
        self.ev(self.t_esc - 0.4, "puerta", 0.5, 0.0)
        self.ev(self.t_todos - 0.2, "oro_brillo", 0.7, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.5, 0.0, dur=0.8)
