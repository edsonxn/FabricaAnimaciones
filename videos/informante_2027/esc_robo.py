# -*- coding: utf-8 -*-
"""Escena 9 «robo»: la hoja «FEBRERO 2027» entre relámpagos; de madrugada, en el laboratorio, la barra de copia que avanza y el
reloj que corre mientras los datos se van por el cable (la cámara de vigilancia mira hacia otro lado); la carrera: dos autos
con banderín, llanta con llanta, por la avenida mojada; el velocímetro en rojo y el pedal del freno que nadie pisa."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import props as PR
import props4 as PR4
import props5 as PR5
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, pulso, suave, tubo


class Robo(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_feb = w("Febrero")
        self.t_segun = w("según")
        self.t_madru = w("De madrugada")
        self.t_copia = w("copia")
        self.t_saca = w("saca")
        self.t_oper = w("La operación")
        self.t_dos = w("dos horas")
        self.t_ladron = w("El ladrón")
        self.t_china = w("China")
        self.t_desde = w("Y desde")
        self.t_negocio = w("negocio")
        self.t_carrera = w("Es una carrera")
        self.t_yen = w("Y en una")
        self.t_frena = w("frena")
        self.t_pierde = w("pierde")
        self.plano(t0, self.p_fecha)
        self.plano(self.t_madru - 0.35, self.p_copia, tr="relampago", dur=0.6)
        self.plano(self.t_desde - 0.35, self.p_carrera, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_yen - 0.3, self.p_freno, tr="empuje", dur=0.5, centro=(W * 0.4, H * 0.55))

    # ------------------------------------------------------------------ febrero de 2027
    def p_fecha(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960 + 5 * u, 540, 0.0)
        K.pared(h, 58, 22, ladrillo=True)
        K.calendario(h, t, self.t_feb, "FEBRERO", "2027", "", cx=560, cy=540, s=1.0, sem=20)
        K.carpeta(h, 1400, 620, 0.62, "2027", t, -99, ang=0.06, sem=50, px=230)
        C.banda(h, "SEGÚN EL EXPEDIENTE", 1400, 300, 50, t, self.t_segun, claro=True, sem=5)
        fl = max(N.relampago(t, [self.t_feb + 0.1]), 0.0)
        h.ambiente[:] = 0.46 + 1.0 * fl
        h.luz_radial(560, 420, 1000, (1.0, 1.0, 1.0), k=1.0)
        h.luz_persiana(np.array([[900, -200], [2100, -260], [2100, 900], [800, 1100]]), k=0.9, n=14, abierto=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=200, y1=1080, sube=False), bloom=0.45, flash=0.3 * fl)

    # ------------------------------------------------------------------ la copia
    def p_copia(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 520, 0.0)
        M27.laboratorio().pegar(h, 1.0, oscuro=0.8)
        tip = PR.caja_negra(h, 640, 980, 1.05, 1.0, t, sem=40, cable=False)
        PR4.camara_vigilancia(h, 250, 330, 1.2, ang=0.5 + 0.15 * math.sin(t * 0.8), led=1.0, t=t, sem=60)
        f = clamp01((t - self.t_copia) / max(2.0, self.t_dos - self.t_copia + 0.4))
        # el cable por el que se va el modelo: pulsos de luz hacia la derecha
        xs = np.linspace(760, W + 100, 60)
        ys = 880 + 50 * np.sin(np.linspace(0, 3 * math.pi, 60)) - 120 * np.linspace(0, 1, 60) ** 2
        h.trazo(np.stack([xs, ys], 1), 12, 70, color=(26, 26, 26), jit=0.4, taper=(0, 0))
        if 0 < f:
            for q in range(7):
                a = (t * 1.1 + q / 7.0) % 1.0
                i = int(a * 59)
                h.emitir(elipse_(xs[i], ys[i], 12, 12, n=10), 1.2, blur=2)
                h.luz_radial(xs[i], ys[i], 110, (1.0, 1.0, 1.0), k=0.9)
        # el panel: barra de copia y reloj de la madrugada
        h.pieza(C.rect(960, 250, 760, 330), 16, 80, w=6, luz=(0, -1), d=8, trama=0.2, rim=0.7)
        N.texto_maquina(h, "COPIANDO EL MODELO...", 1000, 280, 46, t, self.t_copia - 0.4, cps=30, tono=0.95, encuadrar=False)
        K.barra(h, 1000, 370, 680, 54, f, sem=85)
        N.texto_maquina(h, f"{int(f * 100):3d} %", 1000, 450, 60, t, self.t_copia, cps=1e9, tono=0.95, fuente=K.IMPACT, encuadrar=False)
        mins = 3 * 60 + 2 + int(f * 114)
        N.texto_maquina(h, f"{mins // 60:02d}:{mins % 60:02d} a. m.", 1390, 450, 60, t, -99, cps=1e9, tono=0.95, fuente=K.IMPACT, encuadrar=False)
        h.luz_fija(C.rect(960, 250, 760, 330), 0.85)
        C.banda(h, "DE MADRUGADA", 420, 110, 60, t, self.t_madru + 0.1, sem=5)
        C.banda(h, "MENOS DE 2 HORAS", 1340, 690, 70, t, self.t_dos - 0.3, claro=True, sem=6)
        C.banda(h, "EL LADRÓN: CHINA", 1340, 820, 80, t, self.t_china - 0.3, sem=7)
        al = (int(t * 4) % 2) if f >= 1.0 else 0                     # al terminar, la alarma: ya es tarde
        h.ambiente[:] = 0.42 + 0.35 * al
        h.luz_cono(640, -300, math.pi / 2, 0.36, 1800, (1.3, 1.3, 1.3), suave=0.5)
        h.luz_radial(tip[0], tip[1], 400, (1.0, 1.0, 1.0), k=1.0)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.22, vel=12, y0=200, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ una carrera entre dos potencias
    def p_carrera(self, h, t, u):
        v = 520.0
        cx = 1500 + (t - self.t_desde) * v
        h.camara(0.86, cx, 640, 0.012 * math.sin(t * 1.3))
        per = 4800.0
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        for dxl in (0, 3540):
            MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36, dx=dxl)
        for rep in (-1, 0, 1):                                       # la calle se repite (la carrera no tiene fin)
            dx = (cx // per + rep) * per
            MU.calle().pegar(h, 1.0, dx=dx)
        d1 = 40 * math.sin(t * 0.9)                                  # se adelantan y se alcanzan
        PR5.auto(h, cx + 260 - d1, 1090, 1.25, t, vel=3.0, sem=40, tono=46, bandera="estrella")
        PR5.auto(h, cx - 300 + d1, 1200, 1.45, t, vel=3.0, sem=80, tono=30, bandera="franjas")
        for a in (cx + 260 - d1, cx - 300 + d1):
            h.luz_cono(a + 240, 1060, 0.0, 0.2, 800, (1.5, 1.5, 1.5), k=1.0, suave=0.6)
        h.ambiente[:] = 1.0
        h.luz_radial(cx, 500, 1800, (0.9, 0.9, 0.9), k=0.6)
        N.lluvia(h, t, n=600, vel=1900, viento=0.5)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "YA NO ES UN NEGOCIO", 520, 120, 60, t, self.t_negocio - 0.6, sem=5)
        C.banda(h, "ES UNA CARRERA", 1380, 150, 96, t, self.t_carrera + 0.2, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.22, y0=300, y1=1080, vel=60), bloom=0.5)

    # ------------------------------------------------------------------ el que frena, pierde
    def p_freno(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, 0.0)
        K.pared(h, 26, 6)
        h.pieza(np.asarray(suave([(-100, 1200), (-100, 380), (400, 250), (1520, 250), (2020, 380), (2020, 1200)], 4)), 44, 10, w=8,
                luz=(0, -1), d=24, trama=0.6, rim=0.7)                                           # el tablero del auto
        vv = clamp01(0.55 + 0.4 * smooth(clamp01((t - self.t_yen) / 2.5)) + 0.01 * math.sin(t * 30))
        PR5.velocimetro(h, 680, 660, 330, vv, t, sem=30)
        # pedales: el acelerador, a fondo; el freno, intacto
        pis = smooth(clamp01((t - self.t_yen) / 0.8))
        for k, (x, nom, hund) in enumerate(((1280, "FRENO", 0.0), (1560, "ACELERADOR", pis))):
            y = 620 + 90 * hund
            h.pieza(np.array([[x - 90, y], [x + 90, y], [x + 104, y + 250], [x - 104, y + 250]]), 90 - 40 * hund, 60 + k * 10, w=6,
                    luz=(0.2, -1), d=12, trama=0.5, rim=0.8)
            for q in range(5):
                h.trazo(np.array([[x - 70, y + 36 + q * 44], [x + 70, y + 36 + q * 44]]), 6, 62 + k * 10 + q, alfa=0.7, jit=0.3)
            C.banda(h, nom, x, 960, 34, t, self.t_yen, claro=(k == 0), sem=20 + k)
        # el zapato sobre el acelerador
        zx, zy = 1560, 640 + 90 * pis - 60
        h.pieza(np.asarray(suave([(zx - 80, zy + 30), (zx - 60, zy - 150), (zx + 60, zy - 170), (zx + 96, zy + 20), (zx + 70, zy + 210),
                                  (zx - 60, zy + 210)], 4)), 16, 90, w=6, luz=(0.2, -1), d=14, trama=0.4, rim=0.9)
        h.pieza(np.asarray(tubo(np.array([[zx, zy - 150], [zx + 30, zy - 420], [zx + 60, zy - 800]]), 150, 170)), 34, 91, w=6,
                luz=(0.2, -1), d=16, trama=0.6, rim=0.8)
        C.banda(h, "EL QUE FRENA, PIERDE", 960, 130, 84, t, self.t_frena - 0.2, sem=5)
        g = pulso(t, self.t_pierde, 0.3, 1.0)
        h.ambiente[:] = 0.4
        h.luz_radial(680, 660, 800, (1.0, 1.0, 1.0), k=1.2 + g)
        h.luz_radial(1420, 700, 700, (1.0, 1.0, 1.0), k=0.9)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, vel=10, y0=0, y1=1080, sube=False), bloom=0.5, flash=0.2 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_feb - 0.2, "papel_arranca", 0.9, -0.3)
        self.ev(self.t_feb + 0.1, "trueno_noir", 0.8, 0.2, dur=4.0)
        self.ev(self.t_segun, "sello_golpe", 0.8, 0.3)
        self.ev(self.t_madru - 0.35, "relampago_corto", 0.6, 0.0)
        self.ev(self.t_madru, "zumbido_servidores", 0.7, 0.0, dur=self.t_desde - self.t_madru)
        self.ev(self.t_madru + 0.3, "camara_zoom", 0.5, -0.5)
        self.ev(self.t_copia, "datos", 0.7, 0.3, dur=max(2.0, self.t_dos - self.t_copia + 0.4))
        self.ev(self.t_copia, "reloj_pared", 0.5, 0.4, dur=max(2.0, self.t_dos - self.t_copia + 0.4))
        self.ev(self.t_dos - 0.3, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_dos + 0.5, "alarma_leds", 0.7, 0.0, dur=max(0.8, self.t_desde - self.t_dos - 0.6))
        self.ev(self.t_china - 0.3, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_desde - 0.35, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_desde, "motores_carrera", 0.8, 0.0, dur=self.t_yen - self.t_desde)
        self.ev(self.t_desde, "lluvia_amb", 0.6, 0.0, dur=self.t_yen - self.t_desde)
        self.ev(self.t_carrera + 0.2, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_yen - 0.3, "motor_acelera", 0.9, 0.0, dur=self.t1 - self.t_yen)
        self.ev(self.t_frena - 0.2, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_pierde, "golpe_grave", 1.0, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
