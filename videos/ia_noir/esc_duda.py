# -*- coding: utf-8 -*-
"""Escena 9 «duda»: el detective escribe su informe con la luz de la persiana en rayas · titular escéptico y la pared de PATRONES ·
la imprenta (video real) y los sellos de los peligros de hoy (fraudes, mentiras, empleos, poder) · el vendedor del fin del mundo con su
cartel en oferta (eco del loco de la esquina) · dados reales y dados dibujados que giran sin caer nunca."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Busto, Frontal
from toon import Pista, elipse_, pulso

_PIPS = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
         5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}


def dado3d(h, cx, cy, r, ax, ay, az, sem=0, tono=225):
    """Dado en 3D (proyección ortográfica) con caras sombreadas por orientación y sus puntos."""
    V = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
    def R(a, b, c):
        Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
        Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
        Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
        return Rz @ Ry @ Rx
    M = R(ax, ay, az)
    caras = [((0, 1, 3, 2), (-1, 0, 0), 1), ((4, 6, 7, 5), (1, 0, 0), 6), ((0, 4, 5, 1), (0, -1, 0), 2),
             ((2, 3, 7, 6), (0, 1, 0), 5), ((0, 2, 6, 4), (0, 0, -1), 3), ((1, 5, 7, 3), (0, 0, 1), 4)]
    Vr = V @ M.T
    luz = np.array([-0.4, -0.7, 0.6])
    luz /= np.linalg.norm(luz)
    for idx, nrm, num in sorted(caras, key=lambda c: (M @ np.array(c[1], float))[2]):
        n = M @ np.array(nrm, float)
        if n[2] <= 0.02:
            continue
        P = np.array([[cx + Vr[i][0] * r, cy + Vr[i][1] * r] for i in idx])
        b = 0.45 + 0.55 * max(0.0, float(n @ luz))
        h.pieza(P, int(tono * b), sem + num, w=4, luz=(0, -1), d=1, sombra=0, trama=0.3 * (1 - b), rim=0)
        c0 = P.mean(0)
        u = (P[1] - P[0]) / 2
        v = (P[3] - P[0]) / 2
        for px, py in _PIPS[num]:
            q = c0 + u * px * 0.55 + v * py * 0.55
            h.pieza(elipse_(q[0], q[1], r * 0.13 * max(0.3, n[2]), r * 0.13, n=12), 15, sem + 20 + num, w=0, luz=(0, -1), d=1, sombra=0,
                    trama=0, rim=0, linea=False)


class Duda(BaseNoir):
    TR_SALIDA = ("fundido", 0.9)

    def armar(self):
        w = self.w
        self.busto = Busto(sem=5)
        self.vend = Frontal(sem=400)
        self.t_historia = w("historia")
        self.t_muchos = w("Muchos expertos")
        self.t_exag = w("exagerado")
        self.t_deseos = w("deseos")
        self.t_patrones = w("patrones")
        self.t_peligros = w("peligros")
        self.t_fraudes = w("fraudes")
        self.t_mentiras = w("mentiras")
        self.t_empleos = w("empleos")
        self.t_poder = w("poder")
        self.t_fin = w("Y que el fin")
        self.t_venta = w("venta")
        self.t_nadie = w("Nadie, ni siquiera")
        self.t_prob = w("probabilidad")
        self.t_dormir = w("dormir", fin=True)
        self.plano(self.t0, self.p_oficina)
        self.plano(self.t_muchos - 0.3, self.p_titular, tr="relampago", dur=0.3)
        self.plano(self.t_deseos - 0.3, self.p_patrones, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_peligros - 0.3, self.p_imprenta, tr="empuje", dur=0.45)
        self.plano(self.t_fin - 0.3, self.p_vendedor, tr="tinta", dur=0.6)
        self.plano(self.t_nadie - 0.3, self.p_dados_real, tr="barrido", dur=0.45, dirx=-1)
        self.plano(self.t_prob + 0.6, self.p_dados, tr="empuje", dur=0.45)

    # ------------------------------------------------------------------ el informe
    def p_oficina(self, h, t, u):
        h.camara(1.3, 900, 200, 0.0)
        MU.oficina().pegar(h, 1.0, oscuro=0.55)
        h.camara(1.0, W / 2, H / 2, 0.0)
        p = dict(x=1180 - 12 * u, y=560, s=1.05, d=-1, luz=(-1.0, -0.3), brasa=0.25, arriba=-0.0, rot=0.06)
        self.busto.dibujar(h, p)
        tip = self.busto.punta(p)
        h.emitir(elipse_(tip[0], tip[1], 6, 6, n=10), 1.0)
        N.humo(h, t, tip[0], tip[1], k=0.9, ancho=2.0, viento=(40, -120))
        N.texto_maquina(h, "INFORME — CASO: LA MÁQUINA", 120, 900, 34, t, self.t0 + 0.4, cps=30, tono=0.85)
        h.ambiente[:] = 0.22
        h.luz_persiana(np.array([[-200, -200], [1500, -60], [1500, 1300], [-200, 1260]]), k=1.3, n=18, abierto=0.5, mundo=False)
        h.luz_radial(300, 1000, 500, (0.6, 0.6, 0.6))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ ¿exagerado?
    def p_titular(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.08
        PR.periodico(h, t, self.t_muchos - 0.2, "¿UN MIEDO EXAGERADO?", "Muchos investigadores dudan del riesgo existencial",
                     cabecera="EL DIARIO DE LA NOCHE", sem=21)
        h.ambiente[:] = 0.5
        h.luz_radial(W / 2, H / 2, 1100, (1.0, 1.0, 1.0))
        return h.acabado(t, niebla=None)

    def p_patrones(self, h, t, u):
        h.camara(1.0 + 0.05 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.14
        for fila in range(13):                                  # filas del mismo motivo que se desplazan como un telar
            off = (t * (40 if fila % 2 else -40)) % 160
            for k in range(14):
                x = -160 + k * 160 + off
                y = 40 + fila * 80
                N.texto_maquina(h, "la siguiente", x, y, 22, t, -99, cps=1e9, tono=0.45 if (k + fila) % 3 else 0.7)
        h.pieza(PR.rect(W / 2 - 520, H / 2 - 150, 1040, 300), 12, 3, w=4, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.9)
        N.texto_maquina(h, "sin deseos.", W / 2, H / 2 - 50, 64, t, self.t_deseos, cps=30, tono=0.95, centro=True)
        N.texto_maquina(h, "solo patrones.", W / 2, H / 2 + 50, 64, t, self.t_patrones, cps=30, tono=0.95, centro=True)
        h.ambiente[:] = 0.7
        h.luz_radial(W / 2, H / 2, 1000, (0.6, 0.6, 0.6))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ los peligros de hoy
    def p_imprenta(self, h, t, u):
        N.clip_noir(h, "imprenta_0", t, self.t_peligros - 0.3, inicio=2.0, z0=1.05, z1=1.2, dur=8.5, tinta=0.55, poster=0.4)
        for s, tk, x, y, r in (("FRAUDES", self.t_fraudes, 520, 260, -8), ("MENTIRAS", self.t_mentiras, 1380, 330, 6),
                               ("EMPLEOS PERDIDOS", self.t_empleos, 640, 640, 4), ("PODER EN POCAS MANOS", self.t_poder, 1240, 860, -5)):
            N.sello(h, s, x, y, 92, t, tk, rot=r, tono=0.96)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el vendedor del fin del mundo
    def p_vendedor(self, h, t, u):
        h.camara(1.35, MU.X_ESQUINA - 40, 620, 0.0)
        from esc_lluvia import fondo_ciudad, luces_calle, reflejar
        fondo_ciudad(h, t)
        MU.calle().pegar(h, 1.0)
        x, y = MU.X_ESQUINA - 40, 905
        self.vend.dibujar(h, dict(x=x, y=y, s=0.85, luz=(0.4, -1), traje=70, pelo="sombrero", mira=0.4 * math.sin(t * 2)))
        P = np.array([[x - 92, 560], [x + 92, 560], [x + 96, 830], [x - 96, 830]])
        h.pieza(P, 215, 91, w=5, luz=(0.4, -1), d=10, trama=0.1)
        N.texto_maquina(h, "EL FIN", x, 612, 54, t, -99, cps=1e9, tono=0.03, centro=True, fuente=N.FUENTE_SELLO)
        N.texto_maquina(h, "DEL MUNDO", x, 672, 36, t, -99, cps=1e9, tono=0.03, centro=True, fuente=N.FUENTE_SELLO)
        N.sello(h, "¡OFERTA!", x, 770, 34, t, self.t_venta - 0.3, rot=-6, tono=0.05)
        # la etiqueta del precio que se balancea
        ang = 0.25 * math.sin(t * 2.5)
        tag = PR.rot(PR.rect(x + 90, 520, 120, 70), ang, np.array([x + 90, 520]))
        h.pieza(tag, 230, 95, w=4, luz=(0.4, -1), d=4, trama=0)
        N.texto_maquina(h, "$ 9.99", x + 150, 555, 26, t, -99, cps=1e9, tono=0.05, centro=True)
        luces_calle(h)
        reflejar(h, t)
        N.lluvia(h, t, n=500)
        return h.acabado(t, niebla=dict(dens=0.22, y0=300, y1=1000, vel=40))

    # ------------------------------------------------------------------ dados
    def p_dados_real(self, h, t, u):
        N.clip_noir(h, "dados_0", t, self.t_nadie - 0.3, inicio=0.5, z0=1.1, z1=1.25, dur=2.4, tinta=0.5, poster=0.4, expo=0.9)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    def p_dados(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.07
        for k, (x, y) in enumerate(((W / 2 - 230, H / 2 - 20), (W / 2 + 230, H / 2 + 40))):
            fy = 30 * math.sin(t * 1.8 + k * 2)                # flotan: nunca caen
            dado3d(h, x, y + fy, 150, t * (1.7 + 0.3 * k), t * (2.3 - 0.4 * k), t * 0.9 + k, sem=10 + 40 * k)
        N.texto_maquina(h, "¿la probabilidad real?", W / 2, 920, 48, t, self.t_prob + 0.8, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 0.35
        h.luz_cono(W / 2, -300, math.pi / 2, 0.6, 1600, (1.6, 1.6, 1.6), suave=0.6)
        N.motas(h, t, n=70, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=0, y1=700, sube=False))

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_lejana", 0.35, -0.3, dur=self.t_muchos - self.t0)
        self.ev(self.t0 + 0.4, "tecleo_rapido", 0.45, -0.4, dur=1.2)
        self.ev(self.t_muchos - 0.3, "periodico_gira", 0.7, 0.0)
        self.ev(self.t_deseos - 0.3, "telar", 0.5, 0.0, dur=self.t_peligros - self.t_deseos + 0.3)
        self.ev(self.t_peligros - 0.3, "imprenta", 0.8, 0.0, dur=self.t_fin - self.t_peligros + 0.3)
        for tk in (self.t_fraudes, self.t_mentiras, self.t_empleos, self.t_poder):
            self.ev(tk, "sello_golpe", 0.95, 0.0)
        self.ev(self.t_fin - 0.3, "tinta_mancha", 0.5, 0.0, dur=0.6)
        self.ev(self.t_fin, "lluvia_amb", 0.6, 0.0, dur=self.t_nadie - self.t_fin)
        self.ev(self.t_venta - 0.3, "caja_registradora", 0.9, 0.3)
        self.ev(self.t_nadie - 0.3, "dados", 0.9, 0.0)
        self.ev(self.t_prob + 0.6, "grave_inquietante", 0.8, 0.0, dur=self.t1 - self.t_prob)
        self.ev(self.t_dormir, "reloj_pared", 0.5, 0.3, dur=self.t1 - self.t_dormir)
