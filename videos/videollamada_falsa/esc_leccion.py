# -*- coding: utf-8 -*-
"""Escena 11 «leccion»: la señal de aviso que parpadea; una voz y una cara que se duplican (clonar) bajo la lluvia de fotos y
videos que todos dejamos en internet; la pared del detective: la regla vieja se tacha y se escribe la nueva; el teléfono (cuelga,
y marca tú el número conocido); dos personas que acuerdan una palabra clave; el reloj y el candado: la prisa y el secreto."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave


def paso(h, n, texto, t, t0, y=150):
    """Cabecera de un paso de la regla nueva (fija en pantalla)."""
    if t < t0:
        return
    with C.fijo(h):
        N.texto_maquina(h, str(n), 130, y, 200, t, -99, cps=1e9, tono=0.97, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
    C.banda(h, texto, 250 + 24 * len(texto), y + 6, 80, t, t0, claro=True, sem=800 + n)


class Leccion(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.a = Frontal(sem=810)
        self.b = Frontal(sem=830)
        self.t_rareza = w("rareza")
        self.t_aviso = w("aviso")
        self.t_hoy = w("Hoy basta")
        self.t_voz = w("voz")
        self.t_video = w("video", frase=1)
        self.t_cara = w("cara")
        self.t_todos = w("Y todos")
        self.t_internet = w("internet")
        self.t_asi = w("Así que")
        self.t_nueva = w("nueva")
        self.t_vieja = w("vieja")
        self.t_si = w("Si alguien")
        self.t_pantalla = w("pantalla")
        self.t_cuelga = w("cuelga")
        self.t_llama = w("Y llama")
        self.t_numero = w("número")
        self.t_acuerda = w("Acuerda")
        self.t_clave = w("clave")
        self.t_familia = w("familia")
        self.t_unaque = w("Una que")
        self.t_ydesc = w("Y desconfía")
        self.t_prisa = w("prisa")
        self.t_secreto = w("secreto", frase=5)
        self.t_son = w("Son las")
        self.plano(t0, self.p_aviso)
        self.plano(self.t_hoy - 0.35, self.p_clonar, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_asi - 0.35, self.p_regla, tr="humo", dur=0.7)
        self.plano(self.t_si - 0.35, self.p_telefono, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_acuerda - 0.35, self.p_clave, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_ydesc - 0.35, self.p_dos, tr="barrido", dur=0.55, dirx=1)

    # ------------------------------------------------------------------ es un aviso
    def p_aviso(self, h, t, u):
        h.camara(1.0 + 0.05 * u, 960, 540, 0.0)
        h.img[:] = 0.05
        on = 0.55 + 0.45 * (math.sin(t * 9.0) > 0) if t > self.t_aviso - 0.2 else 0.35
        tri = np.array([[960, 170], [1380, 880], [540, 880]])
        h.pieza(tri, 30, 20, w=14, luz=(0, -1), d=16, trama=0.4, rim=0.6)
        t2 = np.array([[960, 280], [1270, 810], [650, 810]])
        h.pieza(t2, 80 + 150 * on, 21, w=6, luz=(0, -1), d=8, trama=0, sombra=0)
        h.emitir(t2, 0.4 * on, blur=4)
        h.pieza(np.array([[925, 420], [995, 420], [978, 660], [942, 660]]), 10, 22, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        h.pieza(elipse_(960, 730, 36, 36, n=20), 10, 23, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        for q in range(8):                                        # destellos que giran
            a = t * 1.6 + q * math.pi / 4
            h.luz_cono(960, 560, a, 0.10, 1400, (1.0, 1.0, 1.0), k=0.5 * on, suave=0.8)
        C.banda(h, "NO ES UNA RAREZA", 960, 950, 56, t, self.t_rareza - 0.3, claro=True, sem=5)
        C.banda(h, "ES UN AVISO", 960, 1010, 84, t, self.t_aviso, sem=6)
        h.ambiente[:] = 0.42
        h.luz_radial(960, 560, 900, (1.0, 1.0, 1.0), k=0.9 * on)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.24, vel=14, y0=0, y1=1080), bloom=0.6)

    # ------------------------------------------------------------------ clonar una voz, clonar una cara
    def p_clonar(self, h, t, u):
        ab_ = smooth(clamp01((t - self.t_video + 0.7) / 0.7))             # empieza cerrado sobre la voz y se abre al llegar la cara
        h.camara(1.4 - 0.4 * ab_ + 0.02 * u, 490 + 470 * ab_, 520 + 20 * ab_, 0.0)
        h.img[:] = 0.06
        # la voz y su copia
        cv_ = smooth(clamp01((t - self.t_voz + 0.3) / 0.6))
        for q in range(34):
            amp = 30 + 230 * abs(math.sin(t * (6 + q * 0.31) + q * 1.1)) * (0.4 + 0.6 * abs(math.sin(q * 0.3)))
            bx = 120 + q * 22
            h.trazo(np.array([[bx, 360 - amp / 2], [bx, 360 + amp / 2]]), 12, 20 + q, color=(240, 240, 240), jit=0, taper=(0, 0))
            if cv_ > 0:
                h.trazo(np.array([[bx, 360 + 330 * cv_ - amp / 2], [bx, 360 + 330 * cv_ + amp / 2]]), 12, 60 + q, color=(240, 240, 240),
                        alfa=0.5 + 0.5 * cv_, jit=0, taper=(0, 0))
        C.banda(h, "UN POCO DE AUDIO", 480, 120, 46, t, self.t_hoy + 0.4, claro=True, sem=7)
        C.banda(h, "= UNA VOZ CLONADA", 480, 920, 50, t, self.t_voz, sem=8)
        # la cara y su copia
        cc = smooth(clamp01((t - self.t_cara + 0.3) / 0.6))
        s = 1.7
        look = dict(pelo="oscuro", traje=150, gafas=True)
        if t > self.t_video - 0.4:
            self.a.dibujar(h, dict(look, x=1330, y=420 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.8, mira=0.4 * math.sin(t)))
            if cc > 0:
                self.a.dibujar(h, dict(look, x=1330 + 380 * cc, y=420 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.8, mira=0.4 * math.sin(t)))
            C.banda(h, "UN POCO DE VIDEO", 1500, 110, 46, t, self.t_video, claro=True, sem=9)
            C.banda(h, "= UNA CARA CLONADA", 1500, 1000, 50, t, self.t_cara, sem=10)
        # todo lo que dejamos en internet: llueven fotos y videos
        if t > self.t_todos - 0.2:
            r = np.random.default_rng(11)
            for q in range(26):
                x = r.uniform(60, W - 60)
                v = r.uniform(260, 520)
                y = ((t - self.t_todos + r.uniform(0, 4)) * v) % 1300 - 110
                ang = 0.4 * math.sin(t * 1.3 + q)
                P = PR.rot(C.rect(x - 60, y - 45, 120, 90), ang, np.array([x, y]))
                h.pieza(P, 214, 200 + q, w=3, luz=(0, -1), d=4, trama=0, rim=0, sombra=0.3)
                if q % 2:
                    h.pieza(PR.rot(np.array([[x - 14, y - 18], [x + 20, y], [x - 14, y + 18]]), ang, np.array([x, y])), 30, 240 + q, w=0,
                            luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
                else:
                    h.pieza(PR.rot(np.array(elipse_(x, y - 6, 16, 20, n=12)), ang, np.array([x, y])), 60, 240 + q, w=0, luz=(0, -1), d=1,
                            sombra=0, trama=0, linea=False)
            C.banda(h, "TODO ESTÁ EN INTERNET", 960, 540, 80, t, self.t_internet - 0.3, sem=11)
        h.ambiente[:] = 0.6
        h.luz_radial(960, 500, 1500, (1.0, 1.0, 1.0), k=0.6)
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ la regla nueva
    def p_regla(self, h, t, u):
        h.camara(1.1 + 0.03 * u, 720, 180, 0.0)
        MU.oficina().pegar(h, 1.0)
        h.ambiente[:] = 0.34
        h.luz_persiana(np.array([[60, -420], [1080, -470], [1080, 640], [-80, 900]]), k=1.4, n=15, abierto=0.5)
        with C.fijo(h):
            N.texto_maquina(h, "REGLA N.º 1", 330, 250, 60, t, -99, cps=1e9, tono=0.95, borrar=(self.t_vieja - 0.6, 0.6), encuadrar=False)
            N.texto_maquina(h, "Fíate de lo que ves.", 330, 340, 46, t, -99, cps=1e9, tono=0.95, borrar=(self.t_vieja - 0.4, 0.6),
                            encuadrar=False)
            N.texto_maquina(h, "REGLA NUEVA", 330, 520, 96, t, self.t_nueva - 0.5, cps=14, tono=0.97, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, "Lo que ves también se falsifica.", 330, 680, 52, t, self.t_vieja + 0.2, cps=22, tono=0.95, encuadrar=False)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ 1 cuelga, 2 llama tú
    def p_telefono(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960, 540, -0.01)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        # el teléfono de disco
        h.pieza(np.array(suave([(520, 950), (560, 620), (700, 520), (1220, 520), (1360, 620), (1400, 950)], 5)), 40, 20, w=9, luz=(0.3, -1),
                d=22, trama=0.6, rim=0.7)
        cx, cy = 960, 760
        h.pieza(elipse_(cx, cy, 190, 170, n=44), 200, 21, w=6, luz=(0.3, -1), d=10, trama=0.3, sombra=0.4)
        marca = 0.0
        if t > self.t_llama:                                      # el disco gira al marcar
            f = ((t - self.t_llama) / 0.9) % 1.0
            marca = math.sin(math.pi * min(1.0, f * 1.6)) * 2.4
        for q in range(10):
            a = -math.pi / 2 + q * 0.56 + marca
            h.pieza(elipse_(cx + 130 * math.cos(a), cy + 116 * math.sin(a), 24, 22, n=14), 26, 22 + q, w=3, luz=(0, -1), d=3, trama=0)
        h.pieza(elipse_(cx, cy, 60, 54, n=24), 60, 40, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.5)
        # el auricular: descolgado y con la pantalla hablando; cae sobre la horquilla en «cuelga»
        cu = e_out(clamp01((t - self.t_cuelga + 0.15) / 0.3))
        ay = 270 + 250 * cu
        h.pieza(np.array(suave([(560, ay + 60), (600, ay - 10), (720, ay - 30), (1200, ay - 30), (1320, ay - 10), (1360, ay + 60),
                                (1280, ay + 110), (1180, ay + 50), (740, ay + 50), (640, ay + 110)], 5)), 30, 50, w=9, luz=(0.3, -1), d=18,
                trama=0.6, rim=0.8)
        if cu < 0.9:                                              # la pantalla que pide dinero, arriba a la derecha
            pan = C.rect(1470, 150, 360, 250)
            C.monitor(h, (1470.0, 150.0, 360.0, 250.0), sem=60)
            h.pieza(pan, 190, 64, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
            N.texto_maquina(h, "«Transfiere", 1650, 230, 40, t, self.t_si + 0.3, cps=24, tono=0.05, centro=True, encuadrar=False)
            N.texto_maquina(h, "ahora.»", 1650, 300, 40, t, self.t_si + 0.8, cps=24, tono=0.05, centro=True, encuadrar=False)
            C.luz_rect(h, pan, 0.9, suave_=5)
        paso(h, 1, "CUELGA", t, self.t_cuelga)
        if t > self.t_llama:
            with C.fijo(h):
                N.texto_maquina(h, "2", 130, 330, 200, t, -99, cps=1e9, tono=0.97, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            C.banda(h, "LLAMA TÚ", 250 + 24 * 8, 336, 80, t, self.t_llama, claro=True, sem=12)
            C.banda(h, "A UN NÚMERO QUE YA CONOCÍAS", 1480, 930, 44, t, self.t_numero, sem=13)
        h.ambiente[:] = 0.38
        h.luz_cono(960, -500, math.pi / 2, 0.6, 2100, (1.4, 1.4, 1.4), suave=0.6)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ 3 la palabra clave
    def p_clave(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 520, 0.0)
        MU.cafeteria().pegar(h, 1.0, oscuro=0.8)
        ac = smooth(clamp01((t - self.t_clave + 0.4) / 0.6))          # se inclinan el uno hacia el otro
        s = 2.0
        self.a.dibujar(h, dict(x=560 + 60 * ac, y=470 + 474 * s, s=s, luz=(0.8, -0.6), rim=0.85, pelo="oscuro", traje=150, gafas=True,
                               mira=0.9, cabeza=0.6 * ac))
        self.b.dibujar(h, dict(x=1360 - 60 * ac, y=470 + 474 * s, s=s, luz=(-0.8, -0.6), rim=0.85, pelo="rizado", traje=70,
                               mira=-0.9, cabeza=-0.6 * ac))
        if t > self.t_clave:                                          # el susurro: puntos que viajan de boca a oído
            for q in range(6):
                f = ((t - self.t_clave) * 0.9 + q / 6.0) % 1.0
                h.pieza(elipse_(700 + 520 * f, 520 - 40 * math.sin(math.pi * f), 12, 12, n=10), 236, 60 + q, w=0, luz=(0, -1), d=1,
                        sombra=0, trama=0, linea=False, alfa=math.sin(math.pi * f))
            C.banda(h, "● ● ● ● ● ●", 960, 330, 60, t, self.t_clave + 0.2, sem=14)
        paso(h, 3, "PALABRA CLAVE", t, self.t_clave - 0.2)
        C.banda(h, "CON TU FAMILIA Y CON TU EQUIPO", 960, 930, 46, t, self.t_familia - 0.2, claro=True, sem=15)
        C.banda(h, "QUE NO ESTÉ EN NINGÚN VIDEO", 960, 1010, 46, t, self.t_unaque, sem=16)
        h.ambiente[:] = 0.36
        h.luz_cono(960, -600, math.pi / 2, 0.5, 2000, (1.5, 1.5, 1.5), suave=0.6)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=900, sube=False))

    # ------------------------------------------------------------------ 4 la prisa y el secreto
    def p_dos(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.img[:] = 0.06
        # el reloj (la prisa)
        a1 = e_out(clamp01((t - self.t_prisa + 0.3) / 0.4))
        cx, cy, r = 520, 600, 270 * a1
        if a1 > 0.05:
            h.pieza(elipse_(cx, cy, r + 26, r + 26, n=50), 40, 20, w=8, luz=(-0.4, -1), d=18, trama=0.6, rim=0.8)
            h.pieza(elipse_(cx, cy, r, r, n=50), 214, 21, w=5, luz=(-0.4, -1), d=10, trama=0.3, sombra=0.4)
            am = t * 7.0
            h.trazo(np.array([[cx, cy], [cx + r * 0.55 * math.sin(am / 12), cy - r * 0.55 * math.cos(am / 12)]]), 20, 22, jit=0.3, taper=(0, 0.4))
            h.trazo(np.array([[cx, cy], [cx + r * 0.84 * math.sin(am), cy - r * 0.84 * math.cos(am)]]), 12, 23, jit=0.3, taper=(0, 0.5))
        # el candado (el secreto)
        a2 = e_out(clamp01((t - self.t_secreto + 0.3) / 0.4))
        kx, ky = 1400, 640 + 500 * (1 - a2)
        arc = [(kx - 120 + 240 * q / 14, ky - 150 - 180 * math.sin(math.pi * q / 14)) for q in range(15)]
        h.trazo(np.array(arc), 44, 30, color=(200, 200, 200), jit=0.4, taper=(0, 0))
        h.pieza(C.rect(kx - 200, ky - 140, 400, 340), 206, 31, w=8, luz=(0.3, -1), d=18, trama=0.4, rim=0)
        h.pieza(elipse_(kx, ky, 36, 36, n=18), 12, 32, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        h.pieza(C.rect(kx - 13, ky, 26, 100), 12, 33, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.3)
        paso(h, 4, "DESCONFÍA", t, self.t_ydesc + 0.2)
        C.banda(h, "DE LA PRISA", 520, 930, 62, t, self.t_prisa, claro=True, sem=17)
        C.banda(h, "Y DEL SECRETO", 1400, 930, 62, t, self.t_secreto, claro=True, sem=18)
        C.banda(h, "LAS HERRAMIENTAS MÁS VIEJAS DEL OFICIO", 1180, 150, 40, t, self.t_son + 0.3, sem=19)
        h.ambiente[:] = 0.36
        h.luz_cono(520, -500, math.pi / 2, 0.36, 1900, (1.5, 1.5, 1.5), k=a1, suave=0.5)
        h.luz_cono(1400, -500, math.pi / 2, 0.36, 1900, (1.5, 1.5, 1.5), k=a2, suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=900, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t_aviso - 0.2, "alarma_leds", 0.7, 0.0, dur=max(1.2, self.t_hoy - self.t_aviso))
        self.ev(self.t_aviso, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_hoy - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_voz - 0.3, "datos", 0.5, -0.4, dur=1.2)
        self.ev(self.t_cara - 0.3, "datos", 0.5, 0.4, dur=1.2)
        self.ev(self.t_todos, "papel_viento", 0.7, 0.0, dur=max(1.5, self.t_asi - self.t_todos))
        self.ev(self.t_internet - 0.3, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_asi - 0.35, "sombra_crece", 0.6, 0.0, dur=2.5)
        self.ev(self.t_nueva - 0.5, "tecleo_rapido", 0.6, -0.3, dur=0.9)
        self.ev(self.t_vieja - 0.6, "tachon", 0.9, -0.3)
        self.ev(self.t_vieja + 0.2, "tecleo_rapido", 0.6, -0.3, dur=1.5)
        for tk in (self.t_si, self.t_acuerda, self.t_ydesc):
            self.ev(tk - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_cuelga - 0.1, "interruptor", 1.0, 0.0)
        self.ev(self.t_cuelga, "sello_golpe", 0.9, -0.5)
        for q in range(4):
            self.ev(self.t_llama + q * 0.9, "tambor_gira", 0.6, 0.0, dur=0.8)
        self.ev(self.t_llama, "sello_golpe", 0.9, -0.5)
        self.ev(self.t_acuerda, "cafeteria_amb", 0.5, 0.0, dur=max(2.0, self.t_ydesc - self.t_acuerda))
        self.ev(self.t_clave - 0.2, "sello_golpe", 0.9, -0.5)
        self.ev(self.t_ydesc + 0.2, "sello_golpe", 0.9, -0.5)
        self.ev(self.t_prisa, "reloj_pared", 0.8, -0.4, dur=max(1.5, self.t1 - self.t_prisa))
        self.ev(self.t_secreto, "interruptor", 0.9, 0.4)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
