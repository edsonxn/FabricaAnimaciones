# -*- coding: utf-8 -*-
"""Escena 8 «victima»: el expediente con el nombre tachado mientras pasan los meses y el periódico que llega girando en mayo
(«LA VÍCTIMA ERA ARUP»); la Ópera de Sídney de noche sobre la bahía, trazada como un plano de ingeniería; la sala de servidores
intacta (0 intrusiones); la mano que mueve los hilos de una persona, no los de la máquina."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, bezier2, elipse_, pulso, suave

MESES = ["FEBRERO", "MARZO", "ABRIL", "MAYO"]


def vela(h, bx, by, alto, ancho, inclina, sem, tono=210):
    """Una de las conchas de la Ópera: vela apuntada con costillas."""
    punta = np.array([bx + inclina, by - alto])
    izq = bezier2(np.array([bx - ancho / 2, by]), np.array([bx - ancho * 0.55 + inclina * 0.4, by - alto * 0.7]), punta, n=14)
    der = bezier2(punta, np.array([bx + ancho * 0.45 + inclina * 0.9, by - alto * 0.45]), np.array([bx + ancho / 2, by]), n=14)
    P = np.vstack([izq, der[1:]])
    h.pieza(P, tono, sem, w=6, luz=(-0.6, -0.7), d=22, trama=0.6, rim=0.5, sombra=0.6)
    for q in range(1, 6):                                          # costillas
        b = np.array([bx - ancho / 2 + ancho * q / 6, by])
        h.trazo(bezier2(b, (b + punta) / 2 + (-12, 0), punta, n=10), 2.5, sem + q, alfa=0.45, jit=0.3, taper=(0, 0.5))


class Victima(BaseNoir):
    TR_SALIDA = ("barrido", 0.6)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.emp = Frontal(sem=210)
        self.t_meses = w("meses")
        self.t_nombre = w("nombre")
        self.t_mayo = w("mayo")
        self.t_confirmo = w("confirmó")
        self.t_era = w("Era una")
        self.t_miles = w("miles")
        self.t_misma = w("La misma")
        self.t_opera = w("Ópera")
        self.t_aclaro = w("Y aclaró")
        self.t_nadie = w("nadie", frase=2)
        self.t_ninguna = w("Ninguna")
        self.t_vuln = w("vulnerada", fin=True)
        self.t_noeng = w("No engañaron")
        self.t_maq = w("máquinas")
        self.t_eng = w("Engañaron", frase=3, n=1)
        self.t_persona = w("persona")
        self.plano(t0, self.p_expediente)
        self.plano(self.t_era - 0.35, self.p_opera, tr="fundido", dur=0.7)
        self.plano(self.t_aclaro - 0.35, self.p_servidores, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_noeng - 0.35, self.p_hilos, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ meses sin nombre; en mayo, el periódico
    def p_expediente(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960, 540, -0.02)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        h.pieza(PR.rot(C.rect(250, 150, 820, 800), -0.03, np.array([660, 550])), 150, 20, w=6, luz=(0.2, -1), d=14, trama=0.4, rim=0.3)
        h.pieza(PR.rot(C.rect(290, 200, 740, 720), -0.03, np.array([660, 550])), 224, 21, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
        with C.fijo(h):
            N.texto_maquina(h, "EXPEDIENTE", 330, 250, 64, t, -99, cps=1e9, tono=0.05, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, "Fraude por videollamada", 330, 350, 38, t, self.t0 + 0.4, cps=26, tono=0.08, encuadrar=False)
            N.texto_maquina(h, "Monto: HK$ 200 000 000", 330, 420, 38, t, self.t0 + 1.2, cps=26, tono=0.08, encuadrar=False)
            N.texto_maquina(h, "Víctima:", 330, 520, 46, t, self.t_nombre - 0.6, cps=26, tono=0.05, encuadrar=False)
        if t > self.t_nombre - 0.2:                              # el nombre, tachado
            a = clamp01((t - self.t_nombre + 0.2) / 0.35)
            h.pieza(C.rect(580, 512, 400 * a, 64), 12, 30, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.8)
        dm = max(1.2, self.t_mayo - self.t_meses)
        for k, m in enumerate(MESES):                            # las hojas de los meses que pasan
            tk = self.t_meses - 0.2 + k * dm / 3.3
            a = clamp01((t - tk) / 0.3)
            if a <= 0:
                continue
            x, y = 1380 + 34 * k, 330 + 26 * k
            P = PR.rot(C.rect(x - 210, y - 150 - 300 * (1 - a), 420, 300), 0.05 * (k - 1.5), np.array([x, y]))
            h.pieza(P, 226 if k == 3 else 200, 40 + k, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
            c = P.mean(0)
            N.texto_maquina(h, m, c[0], c[1], 74, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        h.ambiente[:] = 0.40
        h.luz_radial(900, 480, 1500, (1.0, 1.0, 1.0), k=0.9)
        h.camara(1.0, W / 2, H / 2, 0.0)
        PR.periodico(h, t, self.t_confirmo - 0.75, "LA VÍCTIMA ERA ARUP", sub="La firma británica confirma el fraude de HK$ 200 millones",
                     cx=W / 2, cy=H / 2 + 20, dur=0.8, s=1.25, sem=60, cabecera="EL DIARIO DE LA NOCHE")
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la Ópera de Sídney
    def p_opera(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960 - 14 * u, 520, 0.0)
        h.pieza(C.rect(-200, -200, W + 400, 900), 60, 5, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, grad=(150, -200, 720))
        r = np.random.default_rng(4)
        for q in range(70):                                       # estrellas
            sx_, sy_ = r.uniform(-100, W + 100), r.uniform(-150, 420)
            e = C.rect(sx_, sy_, 4, 4)
            h.emitir(e, 0.5 + 0.4 * math.sin(t * 3 + q))
        # el puente del puerto, lejos
        arco = [(1250 + 700 * q / 20, 590 - 190 * math.sin(math.pi * q / 20)) for q in range(21)]
        h.trazo(np.array(arco), 9, 10, color=(40, 40, 40), jit=0.3, taper=(0, 0))
        h.trazo(np.array([[1150, 600], [2050, 600]]), 9, 11, color=(40, 40, 40), jit=0.3, taper=(0, 0))
        for q in range(1, 20):
            h.trazo(np.array([arco[q], (arco[q][0], 600)]), 2.5, 12 + q, color=(50, 50, 50), jit=0.2, taper=(0, 0))
        # el podio y las conchas (aparecen trazándose, como un plano que se construye)
        h.pieza(C.rect(160, 640, 1280, 70), 90, 40, w=6, luz=(-0.6, -0.7), d=12, trama=0.5, rim=0.5)
        h.pieza(C.rect(100, 700, 1400, 26), 60, 41, w=4, luz=(-0.6, -0.7), d=6, trama=0.3)
        velas = [(420, 640, 330, 300, 90, 0), (640, 640, 420, 340, 110, 1), (880, 640, 500, 380, 130, 2), (1130, 640, 330, 280, -110, 3),
                 (1270, 640, 230, 210, -80, 4), (300, 640, 220, 220, 60, 5)]
        for bx, by, al, an, inc, k in velas:
            a = e_out(clamp01((t - self.t_misma + 0.2 - 0.14 * k) / 0.6)) if t > self.t_misma - 0.3 else 0.0
            a = max(a, 0.0)
            if t < self.t_misma - 0.3:
                a = 0.0
            vela(h, bx, by, al, an, inc, 50 + 8 * k, tono=90 + int(120 * a))        # en penumbra; se ilumina al nombrarla
        # el agua
        h.pieza(C.rect(-200, 724, W + 400, 500), 30, 120, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, grad=(8, 724, 1100))
        N.reflejo(h.img, 724, k=0.5, t=t)
        C.banda(h, "FIRMA BRITÁNICA DE INGENIERÍA", 520, 90, 50, t, self.t_era, claro=True, sem=6)
        C.banda(h, "ARUP", 270, 250, 130, t, self.t_era + 0.5, sem=7)
        C.banda(h, "≈ 18 000 EMPLEADOS", 840, 250, 50, t, self.t_miles - 0.2, claro=True, sem=8)
        C.banda(h, "ÓPERA DE SÍDNEY", 1470, 930, 62, t, self.t_opera, claro=True, sem=9)
        h.ambiente[:] = 0.75
        h.luz_radial(780, 520, 1100, (1.0, 1.0, 1.0), k=0.8 * smooth(clamp01((t - self.t_misma) / 1.0)))
        N.motas(h, t, n=40, k=0.3)
        return h.acabado(t, niebla=dict(dens=0.16, vel=14, y0=500, y1=1000), bloom=0.5)

    # ------------------------------------------------------------------ los sistemas, intactos
    def p_servidores(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.img[:] = 0.05
        for k in range(7):                                        # pasillo de bastidores en perspectiva
            f = k / 6.0
            for sx in (-1, 1):
                x0 = 960 + sx * (880 - 620 * f)
                wr = 250 * (1 - 0.72 * f)
                top, bot = 80 + 300 * f, 1000 - 330 * f
                R = C.rect(x0 - (wr if sx > 0 else 0), top, wr, bot - top)
                h.pieza(R, 44 - 20 * f, 20 + k * 2 + (sx > 0), w=5 * (1 - 0.6 * f), luz=(0, -1), d=8, trama=0.4, rim=0.4)
                nl = 12
                for j in range(nl):
                    yy = top + (bot - top) * (j + 0.5) / nl
                    on = (math.sin(t * (3 + (j * 7 + k * 3) % 5) + j * 1.7 + k) > 0.2)
                    led = C.rect(x0 - (wr * 0.8 if sx > 0 else -wr * 0.2), yy, wr * 0.12, max(2.0, 7 * (1 - 0.6 * f)))
                    if on:
                        h.emitir(led, 0.9 * (1 - 0.5 * f))
        h.pieza(np.array([[300, 1000], [1620, 1000], [1130, 660], [790, 660]]), 26, 80, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False,
                grad=(10, 660, 1000))
        # el candado, cerrado e intacto
        cxk, cyk = 960, 470
        arc = [(cxk - 80 + 160 * q / 14, cyk - 100 - 120 * math.sin(math.pi * q / 14)) for q in range(15)]
        h.trazo(np.array(arc), 30, 90, color=(210, 210, 210), jit=0.4, taper=(0, 0))
        h.pieza(C.rect(cxk - 130, cyk - 90, 260, 220), 200, 91, w=7, luz=(0, -1), d=14, trama=0.4, rim=0)
        h.pieza(elipse_(cxk, cyk, 24, 24, n=16), 14, 92, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        h.pieza(C.rect(cxk - 9, cyk, 18, 62), 14, 93, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.3)
        C.banda(h, "NADIE ENTRÓ A SUS SISTEMAS", 960, 150, 60, t, self.t_nadie, claro=True, sem=10)
        C.banda(h, "INTRUSIONES: 0", 960, 800, 84, t, self.t_ninguna, sem=11)
        h.ambiente[:] = 0.5
        h.luz_radial(960, 460, 700, (1.0, 1.0, 1.0), k=1.0)
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=300, y1=1080), bloom=0.6)

    # ------------------------------------------------------------------ no a la máquina: a la persona
    def p_hilos(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.img[:] = 0.06
        pers = smooth(clamp01((t - self.t_eng + 0.2) / 0.5))
        # la máquina, a la izquierda: intacta, sin hilos
        h.pieza(C.rect(210, 430, 380, 520), 46, 20, w=7, luz=(0.3, -1), d=16, trama=0.5, rim=0.6)
        for j in range(7):
            h.pieza(C.rect(240, 460 + j * 66, 320, 44), 26, 30 + j, w=3, luz=(0, -1), d=3, trama=0.2)
            led = C.rect(520, 474 + j * 66, 22, 14)
            if math.sin(t * (3 + j) + j) > 0:
                h.emitir(led, 0.9)
        C.banda(h, "LAS MÁQUINAS: NO", 400, 300, 50, t, self.t_maq - 0.2, claro=True, sem=12)
        # la persona, a la derecha, colgada de hilos
        s = 1.55
        bal = 0.5 * math.sin(t * 1.7) * pers
        px_, py_ = 1380 + 40 * bal, 1060 - 26 * pers
        self.emp.dibujar(h, dict(x=px_, y=py_, s=s, luz=(-0.3, -1.0), rim=0.9, pelo="oscuro", traje=150, mira=0.0, cabeza=bal * 0.8))
        if pers > 0:
            mx, my = 1380 + 90 * math.sin(t * 1.7), 60
            cruz = np.array([[mx - 230, my + 40], [mx + 230, my + 10]])
            for q, (dx, dy) in enumerate(((-128, -360), (128, -360), (0, -830), (-62, -30), (62, -30))):
                a = cruz[0] + (cruz[1] - cruz[0]) * (0.1 + 0.2 * q)
                b = np.array([px_ + dx * s * 0.62, py_ + dy * s * 0.62])
                h.trazo(np.array([a, a + (b - a) * pers]), 2.5, 60 + q, color=(225, 225, 225), jit=0.2, taper=(0, 0))
            h.trazo(cruz, 20, 70, color=(60, 60, 60), jit=0.3, taper=(0, 0))
            PR.mano(h, mx + 60, my - 70 - 300 * (1 - pers), s=1.5, ang=math.pi / 2 + 0.1, d=1, tono=40, sem=72, dedos=0.2, manga=20)
        C.banda(h, "ENGAÑARON A UNA PERSONA", 1330, 1010, 56, t, self.t_persona - 0.2, sem=13)
        h.ambiente[:] = 0.26
        h.luz_cono(400, -400, math.pi / 2, 0.36, 1700, (1.2, 1.2, 1.2), k=1.0 - 0.6 * pers, suave=0.5)
        h.luz_cono(1380, -400, math.pi / 2, 0.40, 1800, (1.6, 1.6, 1.6), k=pers, suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=900, sube=False))

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        dm = max(1.2, self.t_mayo - self.t_meses)
        self.ev(self.t0 + 0.4, "tecleo_rapido", 0.5, -0.4, dur=1.6)
        self.ev(self.t_nombre - 0.2, "tachon", 0.9, -0.2)
        for k in range(4):
            self.ev(self.t_meses - 0.2 + k * dm / 3.3, "papel_arranca", 0.7, 0.4)
        self.ev(self.t_confirmo - 0.75, "periodico_gira", 0.9, 0.0)
        self.ev(self.t_confirmo, "periodico_golpe", 1.0, 0.0)
        self.ev(self.t_era - 0.3, "barrido_aire", 0.5, 0.0, dur=0.8)
        self.ev(self.t_era + 0.5, "golpe_grave", 0.9, -0.4)
        self.ev(self.t_misma - 0.2, "crecer", 0.6, 0.0, dur=1.6)
        self.ev(self.t_opera, "sello_golpe", 0.8, 0.4)
        self.ev(self.t_aclaro - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_aclaro, "zumbido_servidores", 0.6, 0.0, dur=self.t_noeng - self.t_aclaro)
        self.ev(self.t_nadie, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_ninguna, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_noeng - 0.35, "sombra_crece", 0.7, 0.0, dur=3.0)
        self.ev(self.t_eng - 0.2, "hilo_tenso", 0.9, 0.4)
        self.ev(self.t_persona - 0.2, "golpe_grave", 1.0, 0.3)
