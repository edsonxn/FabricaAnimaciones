# -*- coding: utf-8 -*-
"""Escena 2 «encierro»: grúa desde el cielo sobre la BAHÍA de San Francisco con niebla y el puente rojo · la TORRE de los
cuarteles (panorámica de abajo arriba) con la ficha real de Sam Altman · la BÓVEDA: el prototipo encadenado en su cámara de
cristal («nunca salió a la calle») · el prototipo teclea a una velocidad imposible, la impresora escupe hojas y la aguja se va al
rojo · una GANZÚA abre un candado gigante · el GIMNASIO DE HACKEO: copias en sus puestos frente a cajas fuertes y el entrenador con
cronómetro · CENITAL: de un escritorio a decenas de miles · una copia de espaldas con el CRONÓMETRO EN LA NUCA."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_1 as M
import mundos_base as B
import noir as N
import noir_color as NC
import noir_real as R
import props_s as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, e_inout, smooth
from noir_pers import Figura
from toon import Pista, pulso, elipse_, lineas_velocidad


def local(x, y, s, d, wx, wy, g=1.0):
    """Punto del mundo -> coordenadas locales (sin escalar) de un personaje en (x, y) a escala s mirando a d."""
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


class Encierro(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.proto = RP.Copia(sem=777, num="PROTO", grande=True)
        self.copias = [RP.Copia(sem=300 + i * 11, num=f"{(23 + i * 97) % 1200:04d}") for i in range(8)]
        self.t_julio = w("Julio")
        self.t_sf = w("San Francisco")
        self.t_cuart = w("cuarteles")
        self.t_openai = w("OpenAI")
        self.t_adentro = w("Adentro")
        self.t_nunca = w("nunca")
        self.t_proto = w("prototipo")
        self.t_capaz = w("capaz")
        self.t_rapido = w("rápido")
        self.t_quer = w("Querían")
        self.t_cerr = w("cerraduras")
        self.t_gim = w("gimnasio")
        self.t_dec = w("Decenas")
        self.t_paral = w("paralelo")
        self.t_cada = w("Cada una")
        self.t_presu = w("presupuesto")
        self.t_crono = w("cronómetro")
        self.tb = [t0, self.t_cuart - 0.5, self.t_adentro - 0.4, self.t_proto - 0.35, self.t_quer - 0.4, self.t_gim - 0.6,
                   self.t_dec - 0.4, self.t_cada - 0.4]
        tb = self.tb
        self.camA = Pista([(tb[0], (980.0, -380.0, 0.8)), (tb[0] + 0.6, (980.0, -360.0, 0.8), "io"), (tb[1] + 0.6, (900.0, 330.0, 1.05), "io")])
        self.camB = Pista([(tb[1], (960.0, 760.0, 1.2)), (tb[2] + 0.5, (980.0, -900.0, 0.86), "io")])
        self.camC = Pista([(tb[2], (960.0, 520.0, 0.72)), (tb[3] + 0.4, (960.0, 480.0, 1.25), "io")])
        self.plano(tb[0], self.p_bahia)
        self.plano(tb[1], self.p_torre, tr="tinta", dur=0.6)
        self.plano(tb[2], self.p_boveda, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(tb[3], self.p_rapido, tr="barrido", dur=0.5, dirx=1)
        self.plano(tb[4], self.p_candado, tr="barrido", dur=0.45, dirx=-1)
        self.plano(tb[5], self.p_gimnasio, tr="humo", dur=0.6)
        self.plano(tb[6], self.p_cenital, tr="empuje", dur=0.5, centro=(W * 0.5, H * 0.5))
        self.plano(tb[7], self.p_espalda, tr="tinta", dur=0.6)

    # ------------------------------------------------------------------ A. la bahía
    def p_bahia(self, h, t, u):
        cx, cy, z = self.camA(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.sf_cielo(), h, 0.08, rampa="cielo", dx=t * 6, emis=1.0, col_emis=h.pal["luna"])
        NC.pegar(M.sf_colinas(), h, 0.35, rampa="lejos", bruma=0.25, emis=1.0, col_emis=h.pal["sodio"])
        NC.pegar(M.sf_agua(), h, 0.8, rampa="lejos")
        NC.pegar(M.sf_puente(), h, 0.6, rampa="vino", bruma=0.12, emis=1.2, col_emis=h.pal["sodio"])
        C.ambiente(h, 0.75)
        h.luz_radial(1250, 60, 1500, h.pal["luna"], k=0.8)
        for xx in np.arange(-400, 2400, 260):
            h.luz_radial(xx, 600, 260, h.pal["sodio"], k=0.35)
        h.luz_radial(1900, 500, 1400, h.pal["sodio"], k=0.25)
        y_agua = h.tf(np.array([[0, 640]]))[0][1]
        if 40 < y_agua < H - 20:
            N.reflejo(h.img, y_agua, k=0.3, t=t, onda=5, desv=4)
        C.cinta(h, "SAN FRANCISCO · JULIO 2026", 90, 120, 38, t, self.t_julio + 0.2, sem=3)
        return h.acabado(t, niebla=dict(dens=0.17, sem=11, vel=26, y0=0, y1=H), bloom=0.6)

    # ------------------------------------------------------------------ B. los cuarteles
    def p_torre(self, h, t, u):
        cx, cy, z = self.camB(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.torre_hq(), h, 1.0, rampa="piedra", emis=1.0)
        # un vigilante pasea delante del vestíbulo
        x = 700 + 160 * math.sin((t - self.tb[1]) * 0.5)
        K.caminante(h, x, 920, 0.32, fase=K.fase_paso(abs(x - 700) + (t - self.tb[1]) * 20, 0.32), sem=40, tono=40,
                    d=1 if math.cos((t - self.tb[1]) * 0.5) > 0 else -1, barba=False)
        C.ambiente(h, 0.5)
        h.luz_radial(960, 800, 900, h.pal["lampara"], k=0.9)
        h.luz_cono(960, 1300, -math.pi / 2, 0.25, 2600, h.pal["luna"], k=0.35, suave=0.8)
        with h.capa(0.0):
            R.retrato_noir(h, "sam_altman", 1460, 470, 330, t, self.t_openai - 0.1, rotulo="SAM ALTMAN", leyenda="DIRECTOR DE OPENAI",
                           ang=3.0, fijacion="cinta", foco=(0.37, 0.33, 0.30))
        C.cinta(h, "OPENAI · SAN FRANCISCO", 90, 120, 34, t, self.t_cuart, sem=4)
        return h.acabado(t, niebla=dict(dens=0.32, sem=12, vel=22), bloom=0.5)

    # ------------------------------------------------------------------ C. la bóveda y el prototipo
    def p_boveda(self, h, t, u):
        cx, cy, z = self.camC(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.boveda(), h, 0.8, rampa="piedra")
        mira = math.sin((t - self.tb[2]) * 1.1)
        with h.capa(0.8):
            m = self.proto.frente(h, dict(x=960, y=830, s=0.82, luz=(0.0, -1.0), manos=[(-110, -280), (110, -280)],
                                          cara=dict(expr="neutro", mira=mira)))
            for k, mm in enumerate(m):                              # cadenas de las muñecas a las argollas del suelo
                ar = (960 + (-280 if k == 0 else 280), 850)
                P.cadena(h, mm, ar, sem=60 + k * 40, eslabon=30, comba=30, t=t)
                h.pieza(elipse_(ar[0], ar[1], 22, 10, n=14), 90, 80 + k, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.8, rampa="piedra")
            h.luz_radial(960, 300, 700, h.pal["luna"], k=1.3)
            h.luz_radial(960, 480, 500, h.pal["verde"], k=0.5)
        NC.pegar(M.boveda_aro(), h, 1.5, rampa="piedra")
        C.ambiente(h, 0.35)
        h.luz_radial(1600, -200, 1600, h.pal["lampara"], k=0.3)
        C.banda(h, "NUNCA SALIÓ A LA CALLE", 960, 980, 54, t, self.t_nunca + 0.2, sem=6)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=13, vel=8), bloom=0.5)

    # ------------------------------------------------------------------ D. más capaz, más rápido
    def p_rapido(self, h, t, u):
        k = smooth(clamp01(u / 5))
        dx, dy = C.temblor(t, [(self.t_rapido, 6)])
        h.camara(1.0 + 0.08 * k, 960 + dx, 540 + dy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.lab_azulejo(), h, 0.7, rampa="papel")
        # mesa, teclado, impresora
        h.pieza(C.rect(420, 700, 900, 34), 90, 10, w=5, luz=(0.3, -1), d=8, trama=0.3, rim=0.7, rampa="madera")
        for x in (460, 1260):
            h.pieza(C.rect(x, 734, 26, 300), 60, 11 + (x > 500), w=4, luz=(0.3, -1), d=4, trama=0.2, rim=0.6, rampa="madera")
        h.pieza(C.rect(1050, 600, 240, 100), 160, 13, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.8, rampa="piedra")
        h.pieza(C.rect(1080, 590, 180, 16), 30, 14, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.5, rampa="piedra")
        vel = 45 + 25 * smooth(clamp01((t - self.t_capaz) / 1.0))
        tk = math.sin(t * vel)
        g = 1.12
        mano = local(600, 1030, 0.92, 1, 870, 700 - 12 * tk, g)
        mano2 = local(600, 1030, 0.92, 1, 830, 700 + 12 * tk, g)
        self.proto.perfil(h, dict(x=600, y=1030, s=0.92, d=1, sentado=True, mano=mano, mano2=mano2, mano_bob=False,
                                  cara=dict(expr="astuto" if t > self.t_capaz else "neutro", mira=0.6)))
        h.pieza(C.rect(780, 682, 180, 20), 40, 15, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.6, rampa="piedra")    # teclado
        lineas_velocidad(h, 860, 660, 1, 0, n=5, largo=120, w=4, sem=int(t * 12) % 7, sep=24)
        P.papeles(h, t, self.tb[3] + 0.3, 1170, 590, n=18, sem=7, dirx=1, vel=1100, cada=0.18, s=0.8)
        v = 0.3 + 0.68 * smooth(clamp01((t - self.t_capaz + 0.3) / 1.4)) + 0.015 * math.sin(t * 40)
        K.medidor(h, 1560, 330, 190, v, t, sem=20, rojo=0.75)
        C.ambiente(h, 0.42)
        h.luz_radial(900, 300, 1100, h.pal["lampara"], k=1.0)
        h.luz_radial(820, 560, 300, h.pal["verde"], k=0.5)
        C.banda(h, "PROTOTIPO · NUNCA PUBLICADO", 640, 120, 46, t, self.t_proto + 0.1, sem=7)
        C.banda(h, "MÁS CAPAZ · MÁS RÁPIDO", 1340, 980, 56, t, self.t_capaz, claro=True, sem=8)
        return h.acabado(t, niebla=dict(dens=0.08, sem=14), bloom=0.4)

    # ------------------------------------------------------------------ E. forzar cerraduras
    def p_candado(self, h, t, u):
        k = smooth(clamp01(u / 4))
        h.camara(1.15 + 0.12 * k, 960, 560, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.pared_cajas(), h, 0.5, rampa="piedra", emis=1.0, col_emis=h.pal["verde"], bruma=0.1)
        ab = clamp01((t - self.t_cerr - 0.5) / 0.5)
        # la argolla de la pared de donde cuelga
        h.pieza(C.rect(880, 230, 160, 60), 80, 30, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.9, rampa="piedra")
        P.candado(h, 960, 520, 2.4, abierto=ab, sem=40, brillo_ojo=0.4 + 0.6 * ab)
        mov = 0.06 * math.sin(t * 13) * (1 - ab)
        tip = (952, 540)
        P.ganzua(h, tip[0], tip[1], 1.5, ang=mov, sem=50, brillo=0.5)
        P.mano(h, 470, 545 + 6 * math.sin(t * 13), 1.1, ang=mov, pose="agarra", sem=60, rampa="piedra", tono=120, manga="piedra",
               manga_tono=60, largo_brazo=520)
        if ab > 0:
            C.chispas(h, t, 960, 500, self.t_cerr + 0.5, n=14, vel=300, sem=9, col=h.pal["verde"], ang=-math.pi / 2, abre=2.6)
        C.ambiente(h, 0.35)
        h.luz_cono(1300, -300, math.pi * 0.62, 0.5, 1700, h.pal["luna"], k=1.4, suave=0.6)
        h.luz_radial(960, 560, 380, h.pal["verde"], k=0.4 + 0.6 * ab)
        C.banda(h, "FORZAR CERRADURAS DIGITALES", 960, 980, 54, t, self.t_cerr, sem=9)
        return h.acabado(t, niebla=dict(dens=0.06, sem=15), bloom=0.55)

    # ------------------------------------------------------------------ F. el gimnasio de hackeo
    def p_gimnasio(self, h, t, u):
        k = smooth(clamp01(u / 6))
        h.camara(0.95 + 0.05 * k, 700 + 500 * k, 470, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.gimnasio(), h, 1.0, rampa="ladrillo", emis=1.0)
        for i in range(7):                                         # una copia en cada puesto, girando el dial
            dial = (-560 + i * 430 + 150, 630)
            x = dial[0] - 95
            s = 0.62
            gira = math.sin(t * (2.5 + 0.3 * i) + i) * 6
            self.copias[i].perfil(h, dict(x=x, y=760, s=s, d=1, sentado=True, mano=local(x, 760, s, 1, dial[0] - 22, dial[1] + gira),
                                          mano2=local(x, 760, s, 1, dial[0] - 30, dial[1] + 30), mano_bob=False,
                                          cara=dict(expr="neutro" if i % 3 else "carga", mira=0.9)))
            h.pieza(C.rect(x - 40, 690, 80, 14), 50, 200 + i, w=2.5, luz=(0.3, -1), d=2, trama=0, rim=0.6, rampa="madera")   # taburete
        # el entrenador con bata y cronómetro
        xe = -200 + (t - self.tb[5]) * 210
        K.caminante(h, xe, 1080, 0.68, fase=K.fase_paso(xe + 200, 0.68), sem=70, tono=200, barba=False, pelo=40)
        C.ambiente(h, 0.4)
        for x in np.arange(-700, 2700, 420):
            h.luz_cono(x, -230, math.pi / 2, 0.35, 1200, h.pal["lampara"], k=0.9, suave=0.6)
        C.banda(h, "GIMNASIO DE HACKEO", 960, 120, 64, t, self.t_gim, sem=10)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=16, vel=8), bloom=0.5)

    # ------------------------------------------------------------------ G. decenas de miles (cenital)
    def p_cenital(self, h, t, u):
        f = smooth(clamp01(u / (self.tb[7] - self.tb[6] - 0.2)))
        z = 1.5 * (0.06 / 1.5) ** f
        h.camara(z, 960, 540, 0.25 * f)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.suelo_cenital(), h, 1.0, rampa="asfalto", oscuro=0.8 + 0.2 * (1 - f))
        dx, dy = 280.0, 200.0
        if z > 0.55:
            for j in range(-4, 5):
                for i in range(-5, 6):
                    x, y = 960 + i * dx, 540 + j * dy
                    if abs(x - 960) * z > 1100 or abs(y - 540) * z > 700:
                        continue
                    h.pieza(C.rect(x - 90, y - 50, 180, 90), 70, 400 + i * 13 + j, w=3, luz=(0.3, -1), d=6, trama=0.2, rim=0.5,
                            rampa="madera")
                    h.pieza(C.rect(x - 40, y - 46, 80, 40), 150, 600 + i * 13 + j, w=2.5, luz=(0.3, -1), d=4, trama=0, rim=0.6,
                            rampa="piedra")
                    h.emitir(C.rect(x - 34, y - 8, 68, 8), 1.0, col=h.pal["verde"], blur=2)
                    h.pieza(C.rect(x - 50, y + 46, 100, 40), 60, 800 + i * 13 + j, w=2.5, luz=(0.3, -1), d=3, trama=0.2, rim=0.6,
                            rampa="piedra")
        n = 70
        ii, jj = np.meshgrid(np.arange(-n, n + 1), np.arange(-n, n + 1))
        xs = (960 + ii * dx).ravel().astype(np.float64)
        ys = (540 + jj * dy).ravel().astype(np.float64)
        if z <= 0.55:
            C.rejilla_luces(h, xs, ys, (80, 30), v=0.9, col=h.pal["verde"])
        C.ambiente(h, 0.45)
        h.luz_radial(960, 540, 900 / max(z, 0.06), h.pal["verde"], k=0.4)
        C.banda(h, "DECENAS DE MILES DE COPIAS", 960, 120, 58, t, self.t_dec + 0.1, sem=11)
        C.banda(h, "EN PARALELO", 960, 220, 46, t, self.t_paral, claro=True, sem=12)
        return h.acabado(t, niebla=None, bloom=0.7)

    # ------------------------------------------------------------------ H. el cronómetro en la nuca
    def p_espalda(self, h, t, u):
        k = smooth(clamp01(u / 7))
        h.camara(1.0 + 0.25 * k, 960 - 40 * k, 560 - 120 * k, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.cubiculo(), h, 0.7, rampa="tela_verde")
        # su terminal delante (lo que mira)
        h.pieza(C.rect(670, 235, 580, 380), 150, 31, w=6, luz=(0.3, -1), d=8, trama=0.3, rim=0.6, rampa="piedra")
        K.pantalla_codigo(h, (700, 260, 520, 330), t, sem=30, vel=4.0)
        h.pieza(C.rect(300, 700, 1320, 40), 90, 32, w=5, luz=(0.3, -1), d=8, trama=0.3, rim=0.7, rampa="madera")
        # presupuesto: monedas que se van y una barra que baja
        frac = 1 - 0.75 * smooth(clamp01((t - self.t_presu) / 3.5))
        K.barra(h, 1330, 600, 330, 44, frac, sem=40)
        N.texto_maquina(h, "PRESUPUESTO", 1495, 560, 34, t, self.t_presu - 0.2, cps=30, tono=0.92, centro=True, fuente=C.IMPACT,
                        encuadrar=False)
        for k in range(int(8 * frac)):
            h.pieza(elipse_(1700, 690 - k * 12, 46, 14, n=20), 150, 45 + k, w=2.5, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="laton")
        restan = max(0.0, 3600 - (t - self.tb[7]) * 37 - 40 * 60)
        mm, ss = int(restan // 60), int(restan % 60)
        RP.espalda(h, 960, 1130, 1.35, t, sem=50, sentado=True, timer=f"00:{mm:02d}:{ss:02d}", cab_rot=0.04 * math.sin(t * 0.6))
        C.ambiente(h, 0.42)
        h.luz_radial(960, 420, 900, h.pal["verde"], k=0.9)
        h.luz_radial(1700, 300, 900, h.pal["lampara"], k=0.7)
        h.luz_radial(960, 380, 300, h.pal["neon"], k=0.25 * (0.6 + 0.4 * math.sin(t * 6.28)))
        C.banda(h, "UN CRONÓMETRO EN LA NUCA", 960, 980, 54, t, self.t_crono, acento=True, sem=13)
        return h.acabado(t, niebla=dict(dens=0.06, sem=17), bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0], "grave_inquietante", 0.45, 0.0, dur=4.5)
        self.ev(tb[0] + 0.5, "trueno_lejano", 0.35, 0.3, dur=4.0)
        self.ev(tb[1], "autopista", 0.25, 0.0, dur=tb[2] - tb[1])
        self.ev(self.t_openai - 0.1, "fotos", 0.6, 0.3)
        self.ev(tb[2] + 0.1, "puerta", 0.7, -0.3)
        self.ev(tb[2] + 1.6, "servo", 0.4, 0.2)
        self.ev(tb[3] + 0.2, "tecleo_rapido", 0.55, -0.1, dur=tb[4] - tb[3] - 0.3)
        self.ev(tb[3] + 0.3, "teletipo", 0.4, 0.4, dur=tb[4] - tb[3] - 0.4)
        self.ev(self.t_capaz, "subida", 0.5, 0.3, dur=1.2)
        self.ev(tb[4] + 0.2, "pinza", 0.6, 0.0)
        self.ev(self.t_cerr + 0.5, "tambor_click", 0.8, 0.0)
        self.ev(tb[5] + 0.2, "perillas", 0.45, 0.2, dur=2.6)
        self.ev(tb[5] + 0.4, "paso_firme", 0.4, -0.3)
        self.ev(tb[6] + 0.2, "datos", 0.45, 0.0, dur=3.0)
        self.ev(tb[6] + 0.4, "crecer", 0.45, 0.0, dur=2.5)
        self.ev(tb[7] + 0.2, "reloj_pared", 0.45, 0.0, dur=self.t1 - tb[7] - 0.3)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
