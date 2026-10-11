# -*- coding: utf-8 -*-
"""Escena 2 «testigos»: rueda de reconocimiento que se enciende (Hinton da un paso al frente) · tambor de revólver de 10 recámaras
con una sola bala (1 en 10) · carta de renuncia con la credencial y fichas de póker («apostando con nuestras vidas») · multitud bajo
la lluvia (video real entintado) que se llena de firmas · pasillo de servidores que se apaga («pausado») · el arma que alguien desliza
por la mesa para que la guarden."""
import math

import cv2
import numpy as np

import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave

TESTIGOS = [dict(x=200, pelo="blanco", alto=1.08, traje=86), dict(x=620, pelo="oscuro", gafas=True, traje=58, alto=0.97),
            dict(x=1040, pelo="calvo", barba=True, traje=100, ancho=1.1), dict(x=1460, pelo="rizado", traje=48, alto=1.02)]


class Testigos(BaseNoir):
    TR_SALIDA = ("barrido", 0.55)

    def armar(self):
        w = self.w
        self.figs = [Frontal(sem=20 + 7 * k) for k in range(4)]
        self.t_test = w("testigos")
        self.t_geo = w("Geoffrey")
        self.t_padrino = w("padrino")
        self.t_pos = w("posibilidad")
        self.t_diez = w("diez")
        self.t_termine = w("termine")
        self.t_inv = w("Un investigador")
        self.t_escr = w("escribió")
        self.t_apost = w("apostando")
        self.t_mas = w("Más de mil")
        self.t_mil = w("mil")
        self.t_peti = w("petición")
        self.t_frenar = w("frenar")
        self.t_ycomp = w("Y una de")
        self.t_pausado = w("pausado")
        self.t_seg = w("seguridad")
        self.t_cuando = w("Cuando los")
        self.t_arma = w("arma")
        self.t_guarde = w("guarde")
        self.t_mal = w("mal", desde=5)
        self.cam_r = Pista([(self.t0, (1000, 420, 0.92)), (self.t_test, (950, 430, 0.98), "io"), (self.t_geo, (900, 440, 1.0), "io"),
                            (self.t_geo + 1.2, (330, 470, 1.55), "io"), (self.t_pos, (300, 470, 1.65), "l")])
        self.plano(self.t0, self.p_rueda)
        self.plano(self.t_pos - 0.35, self.p_tambor, tr="empuje", dur=0.6, centro=(W * 0.2, H * 0.55))
        self.plano(self.t_inv - 0.3, self.p_renuncia, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_mas - 0.3, self.p_multitud, tr="humo", dur=0.7)
        self.plano(self.t_ycomp - 0.3, self.p_servidores, tr="barrido", dur=0.55, dirx=-1)
        self.plano(self.t_cuando - 0.3, self.p_arma, tr="tinta", dur=0.8)

    # ------------------------------------------------------------------ rueda de reconocimiento
    def p_rueda(self, h, t, u):
        cx, cy, z = self.cam_r(t)
        h.camara(z, cx, cy, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.85)
        enc = 0.0 if t < self.t_test else min(1.0, (t - self.t_test) / 0.08)
        if self.t_test < t < self.t_test + 0.5:            # parpadeo de los tubos al encenderse
            enc *= 0.4 + 0.6 * (int((t - self.t_test) * 30) % 3 != 1)
        paso = smooth(clamp01((t - self.t_geo) / 0.7))
        for k, (F, d) in enumerate(zip(self.figs, TESTIGOS)):
            p = dict(d)
            p.update(y=900 + (40 * paso if k == 0 else 0), s=1.06 * (1 + (0.06 * paso if k == 0 else 0)),
                     luz=(0.0, -1.0), rim=0.9, placa=True, mira=0.6 * math.sin(t * 0.5 + k * 2))
            p["x"] = d["x"] + 2 * math.sin(t * 0.9 + k)                     # se balancean un poco (nervios)
            p["cabeza"] = 0.04 * math.sin(t * 0.6 + k)
            F.dibujar(h, p)
            yp = p["y"] - 300 * p["s"] * p.get("alto", 1.0)
            PR.placa(h, p["x"], yp, f"Nº {k + 1}", -99, -100, s=0.62 * p["s"], sem=60 + k)
            if k == 0 and t >= self.t_geo:
                N.texto_maquina(h, "G. HINTON", p["x"], yp + 4 * p["s"], 22 * p["s"], t, self.t_geo, cps=30, tono=0.92, centro=True)
            F.manos_placa(h, p, yp)
        N.texto_maquina(h, "«EL PADRINO DE LA IA»", 210, 40, 40, t, self.t_padrino, cps=30, tono=0.05, centro=True)
        h.ambiente[:] = 0.30 + 0.05 * enc
        for k, d in enumerate(TESTIGOS):
            kk = max(0.18, enc) * (1.0 if (k == 0 or t < self.t_geo) else 1 - 0.75 * smooth(clamp01((t - self.t_geo) / 0.6)))
            if kk > 0:
                h.luz_cono(d["x"], -540, math.pi / 2, 0.30, 1650, (1.5, 1.5, 1.5), k=kk, suave=0.5)
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=900, sube=False), grano=0.08)

    # ------------------------------------------------------------------ uno en diez
    def p_tambor(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.10
        # gira rápido y frena: la bala queda arriba (ángulo -pi/2) justo en «termine»
        T = max(0.3, self.t_termine - (self.t_pos - 0.35))
        k = clamp01(u / T)
        giro = (1 - (1 - k) ** 3) * (2 * math.pi * 5)
        ang = -math.pi / 2 - (2 * math.pi * 5) + giro
        cx, cy = W / 2 + 40, H / 2 + 10
        r = 360 * (1.0 + 0.04 * u)
        PR.tambor(h, cx, cy, r, ang=ang, cargada=0, n=10, sem=5, brillo=1.0 if k >= 1 else 0.5)
        if k >= 1:                                            # golpe: la bala arriba, el resto vacío
            h.luz_radial(cx, cy - r * 0.66, 200, (1.0, 1.0, 1.0), k=pulso(t, self.t_termine, 0.6, 1.0))
        N.sello(h, "1 EN 10", W / 2 + 560, 230, 120, t, self.t_diez, rot=8)
        N.texto_maquina(h, "probabilidad estimada por G. Hinton (BBC, sept. 2026)", W / 2 + 40, 990, 30, t, self.t_diez + 0.3, cps=40,
                        tono=0.85, centro=True)
        h.ambiente[:] = 0.30
        h.luz_cono(W / 2 - 300, -300, math.atan2(800, 300), 0.6, 1600, (1.6, 1.6, 1.6), suave=0.6)
        return h.acabado(t, niebla=None, bloom=0.5, contraste=6.0)

    # ------------------------------------------------------------------ la renuncia
    def p_renuncia(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2 + 10 * u, H / 2, -0.04 + 0.01 * u)
        MU.escritorio().pegar(h, 1.0)
        # carta
        P = PR.rect(-420 + W / 2, -440 + H / 2, 720, 900)
        h.pieza(P, 226, 3, w=3, luz=(0.2, -1), d=12, trama=0, rim=0)
        N.texto_maquina(h, "RENUNCIA", W / 2 - 60, 200, 54, t, self.t0, cps=1e9, tono=0.05, centro=True)
        N.texto_maquina(h, "A quien corresponda:", W / 2 - 360, 290, 30, t, self.t0, cps=1e9, tono=0.08)
        N.texto_maquina(h, "Me voy. Las empresas", W / 2 - 360, 380, 34, t, self.t_escr, cps=24, tono=0.05)
        N.texto_maquina(h, "están apostando con", W / 2 - 360, 440, 34, t, self.t_escr + 0.9, cps=24, tono=0.05)
        N.texto_maquina(h, "nuestras vidas.", W / 2 - 360, 500, 34, t, self.t_apost, cps=24, tono=0.05)
        # credencial del laboratorio que alguien deja sobre la carta
        dl = smooth(clamp01((t - self.t_inv - 0.6) / 0.6))
        bx, by = W / 2 + 520 - 260 * dl, H / 2 + 330 - 80 * dl
        h.pieza(PR.rot(PR.rect(bx - 130, by - 85, 260, 170), 0.3 - 0.2 * dl, np.array([bx, by])), 200, 8, w=4, luz=(0.2, -1), d=8,
                trama=0)
        h.pieza(PR.rot(PR.rect(bx - 110, by - 60, 80, 100), 0.3 - 0.2 * dl, np.array([bx, by])), 60, 9, w=3, luz=(0.2, -1), d=4,
                trama=0.4)
        N.texto_maquina(h, "ACCESO: LABORATORIO", bx + 40, by - 40, 18, t, self.t0, cps=1e9, tono=0.08, centro=True)
        # fichas de póker que caen sobre la carta al decir «apostando»
        for k in range(9):
            r = np.random.default_rng(k + 30)
            tk = self.t_apost + 0.08 * k
            if t < tk:
                continue
            a = clamp01((t - tk) / 0.18)
            fx, fy = W / 2 - 250 + r.uniform(-150, 380), H / 2 + 260 + r.uniform(-60, 120)
            fy -= (1 - a) * 500
            rr = 44
            h.pieza(elipse_(fx, fy, rr, rr * 0.9, n=28), 40 if k % 2 else 200, 40 + k, w=4, luz=(0.2, -1), d=6, trama=0.2, rim=0.7)
            for j in range(6):
                q = j * math.pi / 3
                h.trazo(np.array([[fx + math.cos(q) * rr * 0.62, fy + math.sin(q) * rr * 0.56],
                                  [fx + math.cos(q) * rr * 0.92, fy + math.sin(q) * rr * 0.83]]), 7, 60 + j,
                        color=gris(230 if k % 2 else 30), jit=0)
        h.ambiente[:] = 0.42
        h.luz_radial(W / 2 - 150, H / 2 - 150, 1100, (1.2, 1.2, 1.2))
        N.humo(h, t, W / 2 + 700, H / 2 - 300, k=0.6, ancho=1.5, viento=(-20, -60))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ mil firmas
    def p_multitud(self, h, t, u):
        N.clip_noir(h, "multitud_2", t, self.t_mas - 0.3, inicio=0.5, z0=1.05, z1=1.2, dur=6.0, tinta=0.6, poster=0.4)
        # firmas que se escriben solas, cada vez más rápido
        nfir = int(clamp01((t - self.t_mil) / 3.2) ** 1.6 * 46)
        for k in range(nfir):
            r = np.random.default_rng(k + 900)
            fx, fy = r.uniform(140, W - 380), r.uniform(120, H - 140)
            P = [(fx, fy)]
            for j in range(int(r.integers(6, 11))):
                P.append((P[-1][0] + r.uniform(12, 34), fy + r.uniform(-28, 22)))
            prog_ = clamp01((t - self.t_mil - k * 0.06) / 0.25)
            n = max(2, int(len(P) * prog_))
            h.trazo(np.array(suave(P[:n], 4, cerrado=False)), 3.0, 200 + k, color=gris(235), jit=0.4, tf=False)
        N.sello(h, "+1.000 FIRMAS", W - 360, 220, 96, t, self.t_mil + 0.2, rot=-6, tono=0.97)
        N.sello(h, "FRENAR", W - 360, 840, 120, t, self.t_frenar, rot=5, tono=0.97)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None, contraste=5.0)

    # ------------------------------------------------------------------ entrenamiento pausado
    def p_servidores(self, h, t, u):
        N.clip_noir(h, "servidores_5", t, self.t_ycomp - 0.3, inicio=0.0, z0=1.0, z1=1.15, dur=7.0, tinta=0.5, poster=0.3, trama=0.3)
        ap = clamp01((t - self.t_pausado + 0.1) / 1.2)
        if ap > 0:                                         # las filas de luces se apagan desde el fondo hacia la cámara
            yy, xx = np.ogrid[0:H, 0:W]
            d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 2.2
            m = np.clip((ap * 1.4 - d) / 0.15, 0, 1).astype(np.float32)
            h.img *= (1 - 0.92 * m)[..., None]
        N.sello(h, "ENTRENAMIENTO PAUSADO", W / 2, H / 2, 86, t, self.t_pausado + 0.5, rot=-4, tono=0.96)
        N.texto_maquina(h, "«por seguridad»", W / 2, H / 2 + 120, 40, t, self.t_seg, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el arma sobre la mesa
    def p_arma(self, h, t, u):
        h.camara(1.25 + 0.05 * u, W / 2 + 60, 560, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.7)
        PR.mesa(h, W / 2, 760, ancho=1500, fondo=260, alto=320, tono=58, sem=3)
        # una mano limpia (puño blanco: los que lo fabrican) desliza el revólver hacia nosotros
        dl = e_out(clamp01((t - self.t_arma + 0.2) / 1.2))
        gx = W / 2 + 420 - 420 * dl
        PR.revolver(h, gx, 650, s=1.25, ang=0.05, d=-1, sem=7)
        PR.mano(h, gx + 200, 628, s=0.9, ang=0.08, d=-1, tono=150, sem=9, dedos=1.0, manga=215)
        # «algo anda mal»: la lámpara parpadea y se balancea
        sw = 0.08 * math.sin((t - self.t_cuando) * 2.3) * (1 + 2 * smooth(clamp01((t - self.t_mal) / 0.5)))
        par = 1.0
        if t > self.t_mal - 0.2:
            par = 0.25 if int((t - self.t_mal) * 14) % 4 == 1 else 1.0
        h.ambiente[:] = 0.22
        PR.lampara_colgante(h, W / 2 + 60, -400, largo=560, ang=sw, k=par, s=1.2, abre=0.62, alcance=1600, sem=30)
        N.humo(h, t, W / 2 - 600, 560, k=0.5, ancho=2.0, viento=(30, -50))
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=700, sube=False))

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_lejana", 0.35, 0.0, dur=self.t_pos - self.t0)
        self.ev(self.t_test, "focos", 0.9, 0.0)
        self.ev(self.t_geo, "paso_firme", 0.6, -0.4)
        for i in range(len("«EL PADRINO DE LA IA»")):
            self.ev(self.t_padrino + i / 30, "tecla", 0.35, -0.3, tono=1.05)
        self.ev(self.t_pos - 0.35, "barrido_aire", 0.5, -0.5, dur=0.6)
        self.ev(self.t_pos - 0.2, "tambor_gira", 0.9, 0.0, dur=self.t_termine - self.t_pos + 0.2)
        self.ev(self.t_termine, "tambor_click", 1.0, 0.0)
        self.ev(self.t_diez, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_inv - 0.3, "barrido_aire", 0.5, 0.4, dur=0.6)
        for k, (ini, s) in enumerate(((self.t_escr, "Me voy. Las empresas"), (self.t_escr + 0.9, "están apostando con"),
                                      (self.t_apost, "nuestras vidas."))):
            for i in range(len(s)):
                self.ev(ini + i / 24, "tecla", 0.4, 0.0, tono=1.0 + 0.03 * (i % 4))
        for k in range(9):
            self.ev(self.t_apost + 0.08 * k + 0.18, "ficha", 0.6, -0.2 + 0.05 * k)
        self.ev(self.t_mas - 0.3, "multitud", 0.6, 0.0, dur=self.t_ycomp - self.t_mas + 0.3)
        for k in range(0, 46, 3):
            self.ev(self.t_mil + 3.2 * (k / 46) ** (1 / 1.6), "pluma", 0.35, -0.5 + k / 46)
        self.ev(self.t_mil + 0.2, "sello_golpe", 0.8, 0.4)
        self.ev(self.t_frenar, "sello_golpe", 0.9, 0.4)
        self.ev(self.t_ycomp - 0.3, "zumbido_servidores", 0.6, 0.0, dur=self.t_pausado - self.t_ycomp + 0.4)
        self.ev(self.t_pausado - 0.1, "apagon", 0.9, 0.0)
        self.ev(self.t_pausado + 0.5, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_arma - 0.2, "revolver_desliza", 0.8, 0.3, dur=1.2)
        self.ev(self.t_mal - 0.2, "lampara_chisporrotea", 0.7, 0.0, dur=1.2)
