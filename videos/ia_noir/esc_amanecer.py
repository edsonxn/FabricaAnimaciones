# -*- coding: utf-8 -*-
"""Escena 10 «amanecer» (cierre): gotas en el vidrio (video real) y la ciudad que se aclara al dejar de llover · la ciudad en la niebla
(video) · grúas que levantan a toda prisa un andamio con forma de CABEZA gigante sobre el horizonte (el sucesor) · un foco (video) ·
la mano que duda sobre el interruptor de palanca · la carpeta sellada CASO ABIERTO y el detective que se aleja en la niebla; iris."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_lluvia import fondo_ciudad, luces_calle, reflejar
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Detective, avance_paso
from toon import Pista, elipse_, pulso, suave


PERFIL = [(-0.42, 1.0), (-0.48, 0.80), (-0.44, 0.58), (-0.30, 0.48), (-0.26, 0.30), (-0.30, 0.0), (0.22, 0.0), (0.22, 0.16),
          (0.30, 0.22), (0.34, 0.30), (0.30, 0.34), (0.36, 0.40), (0.33, 0.44), (0.46, 0.55), (0.36, 0.59), (0.38, 0.66),
          (0.30, 0.76), (0.28, 0.88), (0.10, 1.02), (-0.20, 1.06)]


def _corte(P, y):
    """Intersecciones x del polígono P con la horizontal y (mín, máx) o None."""
    xs = []
    n = len(P)
    for k in range(n):
        (x0, y0), (x1, y1) = P[k], P[(k + 1) % n]
        if (y0 - y) * (y1 - y) <= 0 and y0 != y1:
            xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
    return (min(xs), max(xs)) if len(xs) >= 2 else None


def cabeza_andamio(h, cx, base, alto, prog, t, sem=0):
    """Andamio con forma de CABEZA DE PERFIL (mirando a la derecha): rejilla que sube con prog (0..1), chispas en el frente de obra y
    un ojo que se enciende al final."""
    P = [(cx + px * alto, base - py * alto) for px, py in PERFIL]
    filas = 26
    paso = alto * 1.06 / filas
    hechas = int(filas * prog)
    prev = None
    for i in range(hechas + 1):
        y = base - i * paso
        c = _corte(P, y)
        if c is None:
            continue
        h.trazo(np.array([[c[0], y], [c[1], y]]), 3, sem + i, color=gris(22), jit=0.4)
        if prev is not None:
            for k in range(9):
                f = k / 8
                h.trazo(np.array([[prev[1][0] + f * (prev[1][1] - prev[1][0]), prev[0]], [c[0] + f * (c[1] - c[0]), y]]), 2.0,
                        sem + 100 + i * 9 + k, color=gris(30), jit=0.3)
            if i % 2 == 0:
                h.trazo(np.array([[prev[1][0], prev[0]], [c[1], y]]), 1.6, sem + 400 + i, color=gris(35), alfa=0.7)
        prev = (y, c)
    if hechas >= 2:                                          # contorno del perfil ya construido
        Q = [p for p in P if p[1] >= base - hechas * paso]
        if len(Q) > 2:
            h.trazo(np.array(Q + [Q[0]]), 6, sem + 900, color=gris(12), jit=0.6, taper=(0, 0))
    if 0 < prog < 1 and prev is not None:                     # chispas de soldadura
        r = np.random.default_rng(int(t * 24))
        for _ in range(6):
            x = r.uniform(prev[1][0], prev[1][1])
            h.emitir(elipse_(x, prev[0], 5, 5, n=8), 1.4)
            h.luz_radial(x, prev[0], 120, (0.8, 0.8, 0.8), k=0.6)
    if prog > 0.7:                                            # el ojo se enciende
        q = (cx + 0.20 * alto, base - 0.66 * alto)
        h.emitir(elipse_(q[0], q[1], alto * 0.04, alto * 0.018, n=14), 0.5 + 0.9 * smooth(clamp01((prog - 0.7) * 4)))
        h.luz_radial(q[0], q[1], alto * 0.2, (0.9, 0.9, 0.9), k=smooth(clamp01((prog - 0.7) * 4)))


def grua(h, x, base, alto, brazo, ang, sem=0):
    """Grúa torre de celosía con su pluma girando (ang) y el cable con la carga."""
    for k in range(int(alto // 40)):
        y = base - k * 40
        h.trazo(np.array([[x - 18, y], [x + 18, y - 40]]), 2, sem + k, color=gris(20))
        h.trazo(np.array([[x + 18, y], [x - 18, y - 40]]), 2, sem + 200 + k, color=gris(20))
    for sx in (-18, 18):
        h.trazo(np.array([[x + sx, base], [x + sx, base - alto]]), 4, sem + 400 + sx, color=gris(15))
    c = math.cos(ang)
    tip = np.array([x + brazo * c, base - alto])
    h.trazo(np.array([[x - brazo * 0.3 * c, base - alto], tip]), 7, sem + 500, color=gris(15))
    h.trazo(np.array([[x, base - alto - 60], tip]), 2, sem + 501, color=gris(25))
    h.trazo(np.array([[x, base - alto - 60], [x - brazo * 0.3 * c, base - alto]]), 2, sem + 502, color=gris(25))
    gx = x + brazo * 0.7 * c
    h.trazo(np.array([[gx, base - alto], [gx, base - alto + 220]]), 1.6, sem + 503, color=gris(30))
    h.pieza(PR.rect(gx - 30, base - alto + 220, 60, 30), 30, sem + 504, w=2, luz=(0, -1), d=2, trama=0)
    h.emitir(elipse_(tip[0], tip[1], 5, 5, n=8), 1.0 + 0.6 * math.sin(h.t * 4 + sem))


def interruptor(h, cx, cy, s, ang, sem=0):
    """Interruptor de cuchilla de laboratorio: placa, bornes y palanca con mango (ang 0 = abajo/apagado, 1 = arriba/encendido)."""
    h.pieza(PR.rect(cx - 260 * s, cy - 360 * s, 520 * s, 720 * s), 40, sem, w=7, luz=(0.3, -1), d=14, trama=0.4, rim=0.9)
    for sx in (-1, 1):
        h.pieza(PR.rect(cx + sx * 90 * s - 24 * s, cy - 300 * s, 48 * s, 90 * s), 200, sem + 2 + sx, w=4, luz=(0.3, -1), d=6, trama=0,
                rim=0.9)
        h.pieza(PR.rect(cx + sx * 90 * s - 24 * s, cy + 200 * s, 48 * s, 70 * s), 200, sem + 5 + sx, w=4, luz=(0.3, -1), d=6, trama=0,
                rim=0.9)
    a = math.pi / 2 - ang * math.pi * 0.85                    # la palanca gira sobre el eje de abajo
    piv = np.array([cx, cy + 230 * s])
    tip = piv + 460 * s * np.array([math.cos(a + math.pi), math.sin(a + math.pi)]) * np.array([0.0, 1.0]) + \
        np.array([0, 0]) if False else piv + 460 * s * np.array([0.25 * math.cos(a), -math.sin(a)])
    for sx in (-1, 1):
        P = np.array([piv + (sx * 90 * s - 10 * s, 0), piv + (sx * 90 * s + 10 * s, 0), tip + (sx * 90 * s + 10 * s, 0),
                      tip + (sx * 90 * s - 10 * s, 0)])
        h.pieza(P, 210, sem + 10 + sx, w=4, luz=(0.3, -1), d=4, trama=0, rim=0.95)
    h.pieza(PR.rect(tip[0] - 120 * s, tip[1] - 16 * s, 240 * s, 32 * s), 60, sem + 20, w=5, luz=(0.3, -1), d=6, trama=0.2, rim=0.9)
    h.pieza(PR.rect(tip[0] - 26 * s, tip[1] - 120 * s, 52 * s, 110 * s), 26, sem + 21, w=5, luz=(0.3, -1), d=6, trama=0.3, rim=0.9)
    N.texto_maquina(h, "ENCENDER", cx, cy - 400 * s, 40 * s, h.t, -99, cps=1e9, tono=0.9, centro=True)
    return tip


class Amanecer(BaseNoir):
    TR_SALIDA = ("corte", 0.0)

    def armar(self):
        w = self.w
        self.det = Detective(sem=3)
        self.t_dejo = w("Dejó")
        self.t_encendida = w("encendida")
        self.t_durante = w("Durante toda")
        self.t_planeta = w("planeta")
        self.t_ahora = w("Ahora estamos")
        self.t_sucesor = w("sucesor")
        self.t_prisa = w("prisa")
        self.t_quiza = w("Quizá")
        self.t_pensar = w("pensar")
        self.t_sino = w("Sino si")
        self.t_encenderlas = w("encenderlas")
        self.t_caso = w("Caso abierto")
        self.plano(self.t0, self.p_vidrio)
        self.plano(self.t0 + 1.9, self.p_ciudad, tr="fundido", dur=0.8)
        self.plano(self.t_durante - 0.3, self.p_niebla, tr="humo", dur=0.6)
        self.plano(self.t_ahora - 0.3, self.p_sucesor, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_quiza - 0.3, self.p_foco, tr="empuje", dur=0.45)
        self.plano(self.t_sino - 0.3, self.p_interruptor, tr="barrido", dur=0.45, dirx=-1)
        self.plano(self.t_caso - 0.3, self.p_carpeta, tr="relampago", dur=0.3)
        self.plano(self.t_caso + 1.4, self.p_adios, tr="tinta", dur=0.8)

    # ------------------------------------------------------------------ deja de llover
    def p_vidrio(self, h, t, u):
        N.clip_noir(h, "gotas_vidrio_0", t, self.t0, inicio=1.0, z0=1.0, z1=1.08, dur=3.0, tinta=0.4, poster=0.3, trama=0.2)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    def p_ciudad(self, h, t, u):
        z = 0.85 + 0.05 * u
        h.camara(z, 1010, -1500, 0.0)
        aclara = smooth(clamp01(u / 3.0))
        MU.cielo().pegar(h, 0.05, oscuro=1.0 + 0.7 * aclara, dx=-(t * 6.0) % 400)
        MU.lejos().pegar(h, 0.3, bruma=0.55 + 0.15 * aclara, tono_bruma=0.40 + 0.2 * aclara)
        MU.medio().pegar(h, 0.6, bruma=0.28 + 0.1 * aclara, tono_bruma=0.40 + 0.15 * aclara)
        MU.calle().pegar(h, 1.0)
        h.ambiente[:] = 0.78 + 0.3 * aclara
        N.lluvia(h, t, n=int(650 * (1 - aclara)), k=1 - aclara)
        return h.acabado(t, niebla=dict(dens=0.25 + 0.15 * aclara, y0=-1500, y1=1000, vel=20, tono=0.10 + 0.2 * aclara))

    def p_niebla(self, h, t, u):
        N.clip_noir(h, "amanecer_4", t, self.t_durante - 0.3, inicio=1.0, z0=1.0, z1=1.12, dur=5.0, tinta=0.5, poster=0.4, expo=0.95)
        N.texto_maquina(h, "lo más inteligente del planeta", W / 2, 960, 44, t, self.t_planeta - 0.6, cps=30, tono=0.97, centro=True)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el sucesor
    def p_sucesor(self, h, t, u):
        h.camara(0.62, 1010, -1250, 0.0)
        MU.cielo().pegar(h, 0.05, oscuro=1.6, dx=-(t * 6.0) % 400)
        MU.lejos().pegar(h, 0.3, bruma=0.7, tono_bruma=0.58)
        # la cabeza gigante crece detrás del horizonte, a toda prisa
        prog = clamp01((t - self.t_ahora) / 3.6) ** 0.8 + 0.25 * smooth(clamp01((t - self.t_prisa) / 0.6))
        with h.capa(0.45):
            cabeza_andamio(h, 960, 330, 1180, min(1.0, prog), t, sem=7)
            for k, (gx, al, br) in enumerate(((260, 1250, 520), (1720, 1350, 560), (560, 1050, 420))):
                grua(h, gx, 360, al, br, t * (0.9 + 0.8 * (t > self.t_prisa)) + k * 2, sem=900 + 100 * k)
        MU.medio().pegar(h, 0.6, bruma=0.4, tono_bruma=0.52)
        MU.calle().pegar(h, 1.0)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=dict(dens=0.3, y0=-2500, y1=1000, vel=20, tono=0.3))

    # ------------------------------------------------------------------ pensar
    def p_foco(self, h, t, u):
        N.clip_noir(h, "interruptor_4", t, self.t_quiza - 0.3, inicio=8.8, vel=0.88, z0=1.0, z1=1.25, dur=4.0, tinta=0.45, poster=0.3, expo=1.8,
                    gamma=0.6)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None, bloom=0.6)

    def p_interruptor(self, h, t, u):
        h.camara(1.0 + 0.06 * u, W / 2, H / 2, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.5)
        h.camara(1.0 + 0.06 * u, W / 2, H / 2, 0.0)
        duda = 0.2 + 0.12 * math.sin(t * 2.3) + 0.06 * math.sin(t * 7.1)
        tip = interruptor(h, W / 2, H / 2 + 60, 1.0, duda, sem=5)
        # la mano se acerca, se detiene sobre el mango, tiembla
        lleg = e_out(clamp01((t - self.t_sino) / 1.2))
        tb = 4 * math.sin(t * 31) * clamp01((t - self.t_sino - 1.0) * 2)
        PR.mano(h, tip[0] + 380 - 300 * lleg + tb, tip[1] - 60 + tb, s=1.1, ang=0.15, d=-1, tono=140, sem=9, dedos=0.6)
        h.ambiente[:] = 0.25
        h.luz_cono(W / 2, -400, math.pi / 2, 0.55, 1900, (1.7, 1.7, 1.7), suave=0.5)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=800, sube=False))

    # ------------------------------------------------------------------ caso abierto
    def p_carpeta(self, h, t, u):
        h.camara(1.0 + 0.05 * u, W / 2, H / 2, -0.02)
        MU.escritorio().pegar(h, 1.0)
        h.pieza(PR.rect(W / 2 - 520, H / 2 - 360, 1040, 720), 180, 3, w=5, luz=(0.2, -1), d=14, trama=0.2, rim=0)
        h.pieza(PR.rect(W / 2 - 520, H / 2 - 420, 360, 70), 180, 4, w=5, luz=(0.2, -1), d=6, trama=0.2, rim=0)
        N.texto_maquina(h, "EXPEDIENTE: LA MÁQUINA", W / 2 - 420, H / 2 - 300, 40, t, -99, cps=1e9, tono=0.06)
        N.texto_maquina(h, "Oct. 2026", W / 2 - 420, H / 2 - 240, 30, t, -99, cps=1e9, tono=0.2)
        N.sello(h, "CASO ABIERTO", W / 2 + 40, H / 2 + 80, 130, t, self.t_caso + 0.15, rot=-9)
        h.ambiente[:] = 0.45
        h.luz_radial(W / 2, H / 2 - 100, 1100, (1.2, 1.2, 1.2))
        return h.acabado(t, niebla=None)

    def p_adios(self, h, t, u):
        h.camara(1.15, 1250, 620, 0.0)
        aclara = 1.0
        MU.cielo().pegar(h, 0.05, oscuro=1.6, dx=-(t * 6.0) % 400)
        MU.lejos().pegar(h, 0.3, bruma=0.7, tono_bruma=0.58)
        MU.medio().pegar(h, 0.6, bruma=0.4, tono_bruma=0.52)
        MU.calle().pegar(h, 1.0)
        x = 1000 + 150 * u
        p = dict(x=x, y=905, s=0.82, d=1, luz=(0.5, -1), andar=1.0, paso=(x - 1000) / avance_paso(Detective.ZANCADA, 0.82), viento=0.3, fumar=0.0, hombros=0.4)
        self.det.dibujar(h, p)
        h.ambiente[:] = 0.95
        reflejar(h, t, k=0.3)
        img = h.acabado(t, niebla=dict(dens=0.35 + 0.1 * u, y0=-800, y1=1000, vel=25, tono=0.32))
        cierra = smooth(clamp01((u - 1.4) / 1.6))
        sx, sy = h.tf(np.array([[x, 905 - 230]]))[0]
        return N.iris(img, cierra, cx=sx, cy=sy)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_amb", 0.7, 0.0, dur=3.5)
        self.ev(self.t0, "gotas_vidrio", 0.6, 0.0, dur=3.0)
        self.ev(self.t0 + 2.0, "pajaros_ciudad", 0.35, 0.3, dur=self.t_ahora - self.t0 - 1.0)
        self.ev(self.t_ahora - 0.3, "obra", 0.7, 0.0, dur=self.t_quiza - self.t_ahora + 0.3)
        self.ev(self.t_prisa, "subida", 0.6, 0.0, dur=1.0)
        self.ev(self.t_quiza - 0.3, "zumbido_foco", 0.5, 0.0, dur=3.8)
        self.ev(self.t_sino, "grave_inquietante", 0.7, 0.0, dur=3.5)
        self.ev(self.t_caso + 0.15, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_caso + 1.4, "pasos_mojados", 0.6, 0.2, dur=2.8)
        self.ev(self.t1 - 1.6, "iris", 0.5, 0.0)
