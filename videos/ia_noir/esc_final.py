# -*- coding: utf-8 -*-
"""Escena 8 «final»: cartel de película de serie B del robot de ojos brillantes, tachado y arrugado («olvida») · la autopista de noche
que fluye indiferente (video real) · hormigas reales y la aplanadora que asfalta el hormiguero · pizarra de bolsa que se desploma,
torres eléctricas (video) y la gente movida como marionetas por una mano enorme · la cerilla que se apaga (video real)."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_lluvia import fondo_ciudad
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave, tubo


def robot_cartel(h, x, y, s, t, sem=0):
    """Robot asesino de cartel de los 50: cabeza de cubo, ojos que brillan, pinzas, antena, pisando escombros."""
    def T(P):
        return np.asarray(P, float) * s + (x, y)
    for k, sx in enumerate((-1, 1)):                          # piernas y brazos
        h.pieza(T([(sx * 30, -240), (sx * 90, -240), (sx * 96, 0), (sx * 26, 0)]), 60, sem + k, w=6, luz=(0.4, -1), d=10, trama=0.4,
                rim=0.9)
        h.pieza(T(tubo(np.array([[sx * 120, -560], [sx * 200, -440], [sx * 180, -300]]), 56, 46)), 70, sem + 2 + k, w=6,
                luz=(0.4, -1), d=10, trama=0.4, rim=0.9)
        cx, cy = x + sx * 180 * s, y - 290 * s
        h.trazo(np.array([[cx, cy], [cx + sx * 40 * s, cy + 60 * s], [cx + sx * 10 * s, cy + 90 * s]]), 16 * s, sem + 4 + k)
    h.pieza(T([(-140, -620), (140, -620), (120, -230), (-120, -230)]), 80, sem + 6, w=7, luz=(0.4, -1), d=14, trama=0.5, rim=0.95)
    for k in range(3):
        h.pieza(T([(-80, -560 + k * 90), (80, -560 + k * 90), (80, -510 + k * 90), (-80, -510 + k * 90)]), 40, sem + 7 + k, w=3,
                luz=(0, -1), d=2, trama=0)
    h.pieza(T([(-90, -820), (90, -820), (90, -640), (-90, -640)]), 90, sem + 10, w=7, luz=(0.4, -1), d=12, trama=0.4, rim=0.95)
    h.trazo(T([(0, -820), (0, -900)]), 6 * s, sem + 11)
    h.emitir(T(elipse_(0, -906, 14, 14, n=12)), 1.0 + 0.4 * math.sin(t * 6))
    for sx in (-1, 1):
        q = T([(sx * 40, -740)])[0]
        h.emitir(elipse_(q[0], q[1], 24 * s, 14 * s, n=16), 1.6)
        h.luz_radial(q[0], q[1], 160 * s, (1.0, 1.0, 1.0), k=1.2)
    h.pieza(T([(-60, -680), (60, -680), (60, -664), (-60, -664)]), 20, sem + 12, w=2, luz=(0, -1), d=1, trama=0)


def aplanadora(h, x, y, s, t, sem=0):
    """Apisonadora de vapor de perfil hacia la derecha: rodillo delantero enorme, cabina, chimenea con humo."""
    def T(P):
        return np.asarray(P, float) * s + (x, y)
    h.pieza(T([(-300, -120), (120, -120), (140, -260), (-260, -260)]), 60, sem, w=6, luz=(0.4, -1), d=14, trama=0.4, rim=0.9)
    h.pieza(T([(-260, -260), (-120, -260), (-120, -440), (-260, -440)]), 70, sem + 1, w=6, luz=(0.4, -1), d=10, trama=0.4, rim=0.9)
    h.pieza(T([(-290, -440), (-90, -440), (-100, -470), (-280, -470)]), 40, sem + 2, w=5, luz=(0.4, -1), d=6, trama=0.2, rim=0.9)
    h.pieza(T([(60, -260), (100, -260), (100, -420), (60, -420)]), 30, sem + 3, w=5, luz=(0.4, -1), d=6, trama=0.2, rim=0.9)
    rx, ry = x + 200 * s, y - 130 * s
    h.pieza(elipse_(rx, ry, 130 * s, 130 * s, n=48), 90, sem + 4, w=7, luz=(0.4, -1), d=16, trama=0.5, rim=0.95)
    for k in range(6):
        a = -t * 2.2 + k * math.pi / 3
        h.trazo(np.array([[rx, ry], [rx + math.cos(a) * 110 * s, ry + math.sin(a) * 110 * s]]), 4 * s, sem + 10 + k, alfa=0.6)
    h.pieza(elipse_(x - 200 * s, y - 70 * s, 70 * s, 70 * s, n=32), 40, sem + 5, w=6, luz=(0.4, -1), d=10, trama=0.3, rim=0.9)
    N.humo(h, t, x + 80 * s, y - 430 * s, k=1.0, ancho=3.0, viento=(-120, -90), hebras=4)


class Final(BaseNoir):
    TR_SALIDA = ("fundido", 0.8)

    def armar(self):
        w = self.w
        self.gente = [Frontal(sem=300 + 7 * k) for k in range(5)]
        self.t_final = w("final")
        self.t_olvida = w("Olvida")
        self.t_robots = w("robots")
        self.t_rojos = w("rojos", fin=True)
        self.t_noguerra = w("No habría")
        self.t_indif = w("indiferencia")
        self.t_cuando = w("Cuando construimos")
        self.t_hormigas = w("hormigas")
        self.t_plan = w("plan")
        self.t_mente = w("Una mente")
        self.t_mercados = w("mercados")
        self.t_redes = w("redes")
        self.t_labs = w("laboratorios")
        self.t_convencer = w("convencernos")
        self.t_ayudemos = w("ayudemos")
        self.t_peor = w("Y lo peor")
        self.t_segunda = w("segunda")
        self.t_oport = w("oportunidad", fin=True)
        self.plano(self.t0, self.p_cartel)
        self.plano(self.t_noguerra - 0.3, self.p_autopista, tr="tinta", dur=0.6)
        self.plano(self.t_cuando - 0.3, self.p_carretera, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_hormigas - 0.25, self.p_hormigas, tr="empuje", dur=0.4, centro=(W * 0.6, H * 0.7))
        self.plano(self.t_hormigas + 1.2, self.p_carretera, tr="empuje", dur=0.4)
        self.plano(self.t_mente - 0.3, self.p_bolsa, tr="barrido", dur=0.45, dirx=-1)
        self.plano(self.t_redes - 0.25, self.p_torres, tr="relampago", dur=0.3)
        self.plano(self.t_convencer - 0.4, self.p_marionetas, tr="humo", dur=0.5)
        self.plano(self.t_peor - 0.3, self.p_cerilla, tr="tinta", dur=0.6)

    # ------------------------------------------------------------------ el cartel del robot (olvídalo)
    def p_cartel(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2, H / 2, 0.0)
        MU.calle().pegar(h, 1.0, oscuro=0.6)
        rasga = smooth(clamp01((t - self.t_rojos - 0.1) / 0.6))
        cx, cy = W / 2, H / 2 + 20
        ang = 0.03 + 1.2 * rasga
        esc = 1.0 - 0.75 * rasga
        h.camara(1.0, W / 2, H / 2, 0.0)
        P = PR.rot(PR.rect(cx - 420 * esc, cy - 500 * esc, 840 * esc, 1000 * esc), ang, np.array([cx, cy]))
        P[:, 1] += 900 * rasga ** 2
        h.pieza(P, 196, 3, w=6, luz=(0.2, -1), d=10, trama=0.2, rim=0.0)
        if rasga < 0.5:
            robot_cartel(h, cx, cy + 400, 0.95 * esc, t, sem=10)
            N.texto_maquina(h, "¡EL ROBOT ASESINO!", cx, cy - 430, 70, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO)
            N.texto_maquina(h, "¡LA REBELIÓN DE LAS MÁQUINAS!", cx, cy + 440, 36, t, -99, cps=1e9, tono=0.05, centro=True,
                            fuente=N.FUENTE_SELLO)
        k = smooth(clamp01((t - self.t_olvida) / 0.3))
        if k > 0 and rasga < 0.6:                              # tachón de tinta
            h.trazo(np.array([[cx - 400, cy - 420], [cx - 400 + 800 * k, cy - 420 + 840 * k]]), 34, 20, color=gris(5))
            h.trazo(np.array([[cx + 400, cy - 420], [cx + 400 - 800 * k, cy - 420 + 840 * k]]), 34, 21, color=gris(5))
        h.ambiente[:] = 0.5
        h.luz_radial(cx, cy - 100, 1000, (1.0, 1.0, 1.0))
        N.lluvia(h, t, n=500)
        return h.acabado(t, niebla=None)

    def p_autopista(self, h, t, u):
        N.clip_noir(h, "trafico_2", t, self.t_noguerra - 0.3, inicio=3.0, z0=1.05, z1=1.2, dur=4.0, tinta=0.5, poster=0.35)
        N.sello(h, "INDIFERENCIA", W / 2, H / 2 + 300, 120, t, self.t_indif, rot=-4, tono=0.96)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    def p_hormigas(self, h, t, u):
        N.clip_noir(h, "hormigas_2", t, self.t_hormigas - 0.25, inicio=1.0, z0=1.3, z1=1.45, dur=1.8, tinta=0.35, poster=0.15, trama=0.1)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la carretera sobre el hormiguero
    def p_carretera(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.5
        # cielo de madrugada y suelo de tierra en corte (galerías del hormiguero)
        h.pieza(PR.rect(0, 0, W, 560), 150, 1, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False, grad=(90, 0, 560))
        h.pieza(PR.rect(0, 560, W, 520), 70, 2, w=0, luz=(0, -1), d=1, sombra=0, trama=0.5, rim=0, linea=False)
        avance = (t - self.t_cuando) * 260
        xa = -200 + avance                                     # el asfalto avanza tras la aplanadora
        h.pieza(PR.rect(-10, 520, max(0, xa + 10), 50), 25, 3, w=4, luz=(0, -1), d=4, trama=0.3, rim=0.6)
        # el hormiguero (montículo y galerías) adelante del rodillo
        mx = 1300
        if xa < mx + 200:
            h.pieza(suave([(mx - 180, 560), (mx - 80, 500), (mx, 486), (mx + 90, 504), (mx + 190, 560)], 4), 95, 4, w=4, luz=(0.3, -1),
                    d=8, trama=0.4)
        for k in range(7):
            gx = mx - 220 + k * 70
            h.trazo(np.array([[gx, 600], [gx + 30, 680 + 30 * (k % 3)], [gx - 20, 760 + 20 * (k % 2)], [gx + 40, 830]]), 14, 10 + k,
                    color=gris(30), alfa=0.9)
        r = np.random.default_rng(7)
        for k in range(70):                                    # hormigas que huyen
            bx = mx + r.uniform(-260, 260)
            huye = clamp01((xa - bx + 500) / 400)
            ax = bx + 260 * huye * (1 if k % 2 else -1) + 6 * math.sin(t * 9 + k)
            ay = r.uniform(540, 900)
            h.pieza(elipse_(ax, ay, 6, 3.5, rot=0.3 * math.sin(t * 7 + k), n=8), 10, 100 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                    rim=0, linea=False)
        aplanadora(h, xa + 120, 560, 1.0, t, sem=40)
        N.texto_maquina(h, "no estaban en el plan.", W - 520, 200, 44, t, self.t_plan, cps=30, tono=0.06, centro=True)
        h.ambiente[:] = 0.7
        h.luz_radial(W / 2, 100, 1300, (0.6, 0.6, 0.6))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ mercados
    def p_bolsa(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.12
        filas = ["ACERO", "PETRÓLEO", "BANCOS", "TRIGO", "MONEDA", "ENERGÍA"]
        for k, s in enumerate(filas):
            y = 170 + k * 130
            h.pieza(PR.rect(200, y - 50, 1520, 100), 26, 10 + k, w=3, luz=(0, -1), d=2, trama=0, rim=0.4)
            N.texto_maquina(h, s, 240, y - 26, 48, t, -99, cps=1e9, tono=0.9)
            caida = clamp01((t - self.t_mercados - 0.1 * k) / 0.6)
            val = 100 - int(80 * caida * (0.5 + 0.5 * ((k * 3) % 4) / 3))
            N.texto_maquina(h, f"{val:>4d}", 1300, y - 26, 48, t, -99, cps=1e9, tono=0.9)
            if caida > 0:
                N.texto_maquina(h, "▼", 1520, y - 26, 48, t, -99, cps=1e9, tono=0.9)
        h.ambiente[:] = 0.6
        h.luz_radial(W / 2, H / 2, 1200, (0.8, 0.8, 0.8))
        return h.acabado(t, niebla=None)

    def p_torres(self, h, t, u):
        if t < self.t_labs - 0.2:
            N.clip_noir(h, "cables_2", t, self.t_redes - 0.25, inicio=0.5, z0=1.1, z1=1.25, dur=2.0, tinta=0.6, poster=0.4, expo=0.9)
        else:
            N.clip_noir(h, "servidores_1", t, self.t_labs - 0.2, inicio=1.0, z0=1.1, z1=1.2, dur=2.0, tinta=0.5, poster=0.35, expo=0.8)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ marionetas
    def p_marionetas(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2, H / 2, 0.0)
        fondo_ciudad(h, t, nubes=True)
        h.img *= 0.75
        # la mano enorme en las nubes, con la cruz de la marioneta
        mx, my = W / 2 + 40 * math.sin(t * 0.7), 120
        PR.mano(h, mx + 300, my - 60, s=1.6, ang=0.4, d=-1, tono=50, sem=5, dedos=0.3, manga=30)
        h.pieza(PR.rot(PR.rect(mx - 520, my + 40, 1040, 26), 0.05 * math.sin(t * 1.4), np.array([mx, my + 50])), 30, 6, w=5,
                luz=(0, -1), d=6, trama=0.3, rim=0.8)
        for k in range(5):
            x = 300 + k * 330
            bob = 18 * math.sin(t * 2.2 + k * 1.3) * (1 if t > self.t_convencer else 0.3)
            uno = clamp01((t - self.t_convencer - 0.35 * k) / 0.4)             # uno por uno se les tensan los hilos
            y = 1100 - 30 * uno + bob
            top = np.array([mx - 500 + k * 250 + 0.05 * math.sin(t * 1.4) * 400, my + 52])
            for sx in (-1, 1):
                hilo = np.array([top + (sx * 20, 0), (x + sx * 90, y - 330 * 0.95)])
                h.trazo(hilo, 2.0, 40 + k * 2 + sx, color=gris(225), alfa=0.35 + 0.6 * uno, taper=(0, 0), ruido=0.0)
            h.trazo(np.array([top, (x, y - 520 * 0.95)]), 2.0, 60 + k, color=gris(225), alfa=0.35 + 0.6 * uno, taper=(0, 0), ruido=0.0)
            self.gente[k].dibujar(h, dict(x=x, y=y, s=0.95, luz=(0, -1), traje=50 + 12 * k,
                                          pelo=["sombrero", "oscuro", "rizado", "calvo", "blanco"][k], cabeza=0.08 * math.sin(t * 2 + k)))
        N.texto_maquina(h, "uno por uno.", W - 330, 990, 40, t, self.t_ayudemos - 0.3, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 0.65
        h.luz_cono(W / 2, -300, math.pi / 2, 0.8, 1800, (0.9, 0.9, 0.9), suave=0.6)
        N.lluvia(h, t, n=300, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=20, y0=0, y1=700, sube=False))

    # ------------------------------------------------------------------ la cerilla
    def p_cerilla(self, h, t, u):
        N.clip_noir(h, "cerilla_1", t, self.t_peor - 0.3, inicio=8.0, vel=1.6, z0=1.1, z1=1.3, dur=5.0, tinta=0.5, poster=0.3, expo=1.0)
        apaga = smooth(clamp01((t - self.t_segunda) / (self.t_oport - self.t_segunda + 0.6)))
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None, oscuro=1 - 0.95 * apaga)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_lejana", 0.5, 0.0, dur=self.t_noguerra - self.t0)
        self.ev(self.t_robots - 0.3, "teremin", 0.7, 0.0, dur=1.6)
        self.ev(self.t_olvida, "tachon", 0.8, 0.0)
        self.ev(self.t_rojos + 0.1, "papel_arranca", 0.9, 0.2)
        self.ev(self.t_noguerra - 0.3, "autopista", 0.6, 0.0, dur=self.t_cuando - self.t_noguerra + 0.3)
        self.ev(self.t_indif, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_cuando - 0.3, "aplanadora", 0.8, -0.3, dur=self.t_mente - self.t_cuando + 0.3)
        self.ev(self.t_hormigas - 0.25, "hormigas", 0.6, 0.0, dur=1.6)
        self.ev(self.t_mente - 0.3, "teletipo", 0.7, 0.0, dur=1.8)
        self.ev(self.t_mercados, "caida", 0.8, 0.0, dur=1.0)
        self.ev(self.t_redes - 0.25, "electricidad", 0.9, 0.0, dur=1.4)
        self.ev(self.t_labs - 0.2, "zumbido_servidores", 0.6, 0.0, dur=1.2)
        self.ev(self.t_convencer - 0.4, "caja_musica", 0.6, 0.0, dur=self.t_peor - self.t_convencer + 0.4)
        for k in range(5):
            self.ev(self.t_convencer + 0.35 * k, "hilo_tenso", 0.6, -0.6 + 0.3 * k)
        self.ev(self.t_peor - 0.3, "cerilla", 0.9, 0.0)
        self.ev(self.t_oport, "apagado_vela", 0.8, 0.0)
