# -*- coding: utf-8 -*-
"""Escena 2 «mensaje»: el correo del «director financiero» se escribe en la pantalla (remitente, asunto, URGENTE, el candado del
secreto); el empleado, de frente, mira el anzuelo del que cuelga el mensaje (sospecha); al otro lado, una figura sin rostro mueve
la pieza siguiente en un tablero; la invitación a la reunión y el ojo de la cámara que se enciende."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
import props2 as P2
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso

PANT = (300.0, 110.0, 1320.0, 800.0)          # la ventana del correo (mundo)


class Mensaje(BaseNoir):
    TR_SALIDA = ("barrido", 0.6)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.emp = Frontal(sem=210)
        self.autor = Frontal(sem=230)
        self.t_mensaje = w("mensaje")
        self.t_venia = w("Venía")
        self.t_director = w("director")
        self.t_reino = w("Reino")
        self.t_hablaba = w("Hablaba")
        self.t_trans = w("transacción")
        self.t_urgente = w("Urgente")
        self.t_deesas = w("De esas")
        self.t_nadie = w("nadie", fin=True)
        self.t_ynuestro = w("Y nuestro")
        self.t_sospecho = w("sospechó")
        self.t_engano = w("engaño")
        self.t_pero = w("Pero quien")
        self.t_contaba = w("contaba")
        self.t_asique = w("Así que")
        self.t_mejor = w("mejor")
        self.t_invito = w("Lo invitó")
        self.t_reunion = w("reunión")
        self.t_camara = w("cámara")
        self.cam_a = Pista([(t0, (1000, 520, 1.12)), (self.t_hablaba, (940, 500, 1.0), "io"), (self.t_ynuestro, (900, 560, 1.16), "io")])
        self.plano(t0, self.p_correo)
        self.plano(self.t_ynuestro - 0.35, self.p_sospecha, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_pero - 0.35, self.p_autor, tr="humo", dur=0.7)
        self.plano(self.t_invito - 0.35, self.p_camara, tr="empuje", dur=0.6, centro=(W * 0.3, H * 0.5))

    # ------------------------------------------------------------------ el correo
    def p_correo(self, h, t, u):
        cx, cy, z = self.cam_a(t)
        h.camara(z, cx, cy, -0.025 + 0.004 * math.sin(t * 0.5))
        MU.escritorio().pegar(h, 1.0, oscuro=0.6)
        x, y, w, hh = PANT
        C.monitor(h, PANT, sem=20, pie=False)
        ab = e_out(clamp01((t - self.t_mensaje + 0.25) / 0.45))         # la ventana se abre al decir «mensaje»
        h.pieza(C.rect(x, y, w, hh), 30, 21, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        if ab <= 0.02:                                                   # antes de abrirse: el aviso del mensaje nuevo, latiendo
            lat = 1.0 + 0.08 * math.sin(t * 7)
            sx, sy = x + w / 2, y + hh / 2
            h.pieza(C.rect(sx - 150 * lat, sy - 95 * lat, 300 * lat, 190 * lat), 200, 26, w=6, luz=(0, -1), d=6, sombra=0.3, trama=0)
            h.trazo(np.array([[sx - 150 * lat, sy - 95 * lat], [sx, sy + 20], [sx + 150 * lat, sy - 95 * lat]]), 7, 27, jit=0.4)
            h.pieza(elipse_(sx + 150, sy - 95, 40, 40, n=20), 20, 28, w=4, luz=(0, -1), d=3, sombra=0, trama=0)
            N.texto_maquina(h, "1", sx + 150, sy - 97, 50, t, -99, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        if ab > 0.02:
            vw, vh = (w - 80) * ab, (hh - 80) * (0.2 + 0.8 * ab)
            vx, vy = x + w / 2 - vw / 2, y + hh / 2 - vh / 2
            h.pieza(C.rect(vx, vy, vw, vh), 214, 22, w=4, luz=(0, -1), d=6, sombra=0, trama=0, jit=0.5)
            h.pieza(C.rect(vx, vy, vw, 64 * ab), 40, 23, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        if ab > 0.95:
            N.texto_maquina(h, "BANDEJA DE ENTRADA  (1 nuevo)", x + 70, y + 54, 30, t, -99, cps=1e9, tono=0.92, encuadrar=False)
            N.texto_maquina(h, "DE:", x + 80, y + 150, 40, t, self.t_venia - 0.3, cps=30, tono=0.10, encuadrar=False)
            N.texto_maquina(h, "Director financiero", x + 290, y + 146, 48, t, self.t_director - 0.2, cps=26, tono=0.04, encuadrar=False)
            N.texto_maquina(h, "(oficina central · Reino Unido)", x + 290, y + 214, 32, t, self.t_reino - 0.2, cps=34, tono=0.08,
                            encuadrar=False)
            N.texto_maquina(h, "ASUNTO:", x + 80, y + 300, 40, t, self.t_hablaba, cps=30, tono=0.10, encuadrar=False)
            N.texto_maquina(h, "Transacción confidencial", x + 290, y + 296, 48, t, self.t_trans - 0.25, cps=24, tono=0.04,
                            encuadrar=False)
            h.pieza(C.rect(x + 80, y + 372, w - 160, 4), 90, 24, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
            r = np.random.default_rng(7)                                  # cuerpo del mensaje: renglones tachados
            for k in range(6):
                tk = self.t_trans + 0.5 + 0.22 * k
                if t < tk:
                    continue
                L = (w - 200) * r.uniform(0.55, 1.0) * clamp01((t - tk) / 0.3)
                h.pieza(C.rect(x + 80, y + 410 + k * 44, L, 20), 70, 30 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.4)
            C.banda(h, "URGENTE", x + w - 330, y + 150, 70, t, self.t_urgente, sem=9, mundo=True)
            if t > self.t_deesas:                                         # el candado: «no se comenta con nadie»
                a = e_out(clamp01((t - self.t_deesas) / 0.35))
                cxk, cyk = x + w - 250, y + 600 - 30 * (1 - a)
                cierra = smooth(clamp01((t - self.t_nadie + 0.5) / 0.3))
                arc = [(cxk - 44 + 88 * q / 12, cyk - 60 - 62 * math.sin(math.pi * q / 12) + 26 * (1 - cierra)) for q in range(13)]
                h.trazo(np.array(arc), 16, 41, color=(30, 30, 30), jit=0.4, taper=(0, 0))
                h.pieza(C.rect(cxk - 70, cyk - 50, 140, 116), 36, 42, w=5, luz=(0, -1), d=6, trama=0.3, rim=0.5)
                h.pieza(elipse_(cxk, cyk, 13, 13, n=14), 220, 43, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
                N.texto_maquina(h, "No lo comentes con nadie.", x + 80, y + 700, 40, t, self.t_deesas + 0.5, cps=22, tono=0.04,
                                encuadrar=False)
            if int(t * 2.4) % 2 == 0:                                     # cursor
                h.pieza(C.rect(x + 80, y + 760, 18, 30), 30, 44, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        # la mano en el ratón, en primer término
        mov = 14 * math.sin(t * 1.3) + 60 * pulso(t, self.t_mensaje - 0.4, 0.8, 1.0)
        h.pieza(elipse_(1640 - mov, 950, 84, 60, n=26), 46, 50, w=6, luz=(-0.4, -1), d=10, trama=0.4, rim=0.6)
        PR.mano(h, 1820 - mov, 950, s=1.25, ang=math.pi - 0.12, d=1, tono=128, sem=52, dedos=0.55, manga=160)
        h.ambiente[:] = 0.26
        C.luz_rect(h, C.rect(x, y, w, hh), 1.25, suave_=6.0)
        h.luz_radial(1650, 940, 560, (0.9, 0.9, 0.9), k=1.3)
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ la sospecha (el anzuelo)
    def p_sospecha(self, h, t, u):
        h.camara(1.0 + 0.035 * u, 960 + 8 * u, 540, 0.0)
        C.oficina_hk().pegar(h, 0.5, oscuro=0.8, dx=-12 * u)
        atras = smooth(clamp01((t - self.t_sospecho) / 0.5))                # se echa hacia atrás al sospechar
        sw = math.sin(t * 1.5) * (0.5 - 0.3 * atras)
        hx, hy = 1290 + 150 * sw, 470 + 26 * abs(sw)
        s = 2.5 - 0.12 * atras
        p = dict(x=640 - 50 * atras, y=470 + 474 * s, s=s, luz=(0.9, -0.3), rim=0.9, pelo="oscuro", traje=150,
                 mira=clamp01((hx - 1100) / 300) * 2 - 0.4, cabeza=-0.6 * atras)
        self.emp.dibujar(h, p)
        # el sedal, el anzuelo y el mensaje que cuelga
        h.trazo(np.array([[1290, -40], [1290 + 60 * sw, 200], [hx, hy - 120]]), 3.5, 60, color=(225, 225, 225), jit=0.3, taper=(0, 0))
        gan = [(hx + 46 * math.cos(a) - 46, hy - 74 + 46 * math.sin(a)) for a in np.linspace(-0.3, math.pi * 1.25, 16)]
        h.trazo(np.array([(hx, hy - 120)] + gan), 9, 61, color=(235, 235, 235), jit=0.3, taper=(0, 0.6))
        ang = 0.25 * sw
        hoja = PR.rot(C.rect(hx - 250, hy - 40, 400, 290), ang, np.array([hx - 50, hy - 40]))
        h.pieza(hoja, 170, 62, w=4, luz=(0.4, -1), d=8, trama=0, rim=0)
        for k in range(5):
            a = hoja[0] + (hoja[3] - hoja[0]) * (0.34 + 0.12 * k) + (hoja[1] - hoja[0]) * 0.1
            h.trazo(np.array([a, a + (hoja[1] - hoja[0]) * (0.8 if k < 4 else 0.45)]), 6, 64 + k, alfa=0.55, jit=0.3)
        ctr = hoja[0] + (hoja[1] - hoja[0]) * 0.5 + (hoja[3] - hoja[0]) * 0.17
        N.texto_maquina(h, "CONFIDENCIAL", ctr[0], ctr[1], 38, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        C.banda(h, "¿UN ENGAÑO?", 1330, 900, 84, t, self.t_engano, sem=11, claro=True)
        h.ambiente[:] = 0.30
        h.luz_radial(900, 620, 1300, (1.0, 1.0, 1.0), k=1.5)                # la pantalla, fuera de cuadro a la derecha
        h.luz_cono(hx, -300, math.pi / 2, 0.30, 1300, (1.2, 1.2, 1.2), k=0.35, suave=0.6)
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=900, sube=False))

    # ------------------------------------------------------------------ el autor: iba una jugada por delante
    def p_autor(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540 - 6 * u, 0.0)
        h.img[:] = 0.05
        ap = 1.0
        self.autor.dibujar(h, dict(x=960, y=1330, s=2.6, luz=(0.0, -1.0), rim=0.55, pelo="sombrero", traje=26,
                                   mira=0.3 * math.sin(t * 0.8), cabeza=0.02 * math.sin(t * 0.6)))
        # la cara queda en sombra: nunca se le ve
        h.pieza(elipse_(960, 1330 - 470 * 2.6, 120, 100, n=24), 6, 70, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, alfa=0.93)
        movs = [(self.t_contaba - 0.15, "caballo", (1, 0), (2, 2)), (self.t_asique + 0.1, "alfil", (2, 0), (5, 3)),
                (self.t_mejor - 0.1, "peon", (4, 1), (4, 3))]
        P2.ajedrez(h, t, movs, cx=W / 2, cy=1010, ancho=1500, prof=520)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "UNA JUGADA POR DELANTE", W / 2, 1000, 60, t, self.t_contaba + 0.3, sem=13, claro=True)
        h.ambiente[:] = 0.16
        h.luz_cono(W / 2, -500, math.pi / 2, 0.50, 1900, (1.7, 1.7, 1.7), k=ap, suave=0.5)
        N.humo(h, t, 1240, 560, k=0.8, ancho=1.6, viento=(-18, -60))
        N.motas(h, t, n=70, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-200, y1=800, sube=False))

    # ------------------------------------------------------------------ la invitación y el ojo de la cámara
    def p_camara(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960 - 10 * u, 540, 0.02 - 0.005 * u)
        MU.escritorio().pegar(h, 1.0, oscuro=0.7)
        # tarjeta de la invitación
        ent = e_out(clamp01((t - self.t_invito + 0.3) / 0.5))
        tx, ty = 980 + 900 * (1 - ent), 250
        h.pieza(PR.rot(C.rect(tx, ty, 800, 560), -0.03, np.array([tx + 400, ty + 280])), 224, 80, w=4, luz=(0.2, -1), d=10, trama=0,
                rim=0)
        if ent > 0.98:
            N.texto_maquina(h, "INVITACIÓN", tx + 400, ty + 90, 64, t, -99, cps=1e9, tono=0.04, centro=True, fuente=N.FUENTE_SELLO,
                            encuadrar=False)
            N.texto_maquina(h, "Reunión por video", tx + 70, ty + 190, 46, t, self.t_reunion - 0.3, cps=24, tono=0.05, encuadrar=False)
            N.texto_maquina(h, "Convoca: Dir. financiero", tx + 70, ty + 280, 34, t, self.t_reunion + 0.4, cps=30, tono=0.15,
                            encuadrar=False)
            N.texto_maquina(h, "Asistentes: varios directivos", tx + 70, ty + 340, 34, t, self.t_reunion + 1.0, cps=30, tono=0.15,
                            encuadrar=False)
        # la cámara: el ojo que se enciende
        on = smooth(clamp01((t - self.t_camara) / 0.25))
        cxl, cyl = 520, 540
        h.pieza(C.rect(cxl - 330, cyl - 210, 660, 420), 34, 90, w=8, luz=(0.3, -1), d=16, trama=0.5, rim=0.7)
        for k, (rr, tn) in enumerate(((180, 20), (150, 52), (112, 14), (70, 40), (34, 8))):
            h.pieza(elipse_(cxl, cyl, rr, rr, n=44), tn, 91 + k, w=5, luz=(0.3, -1), d=10, trama=0.3 if k < 2 else 0, rim=0.6)
        h.pieza(elipse_(cxl - 46, cyl - 52, 30, 18, rot=-0.6, n=16), 235, 97, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False,
                alfa=0.75)
        led = np.array([[cxl + 250, cyl - 170], [cxl + 280, cyl - 170], [cxl + 280, cyl - 140], [cxl + 250, cyl - 140]])
        h.pieza(led, 40 + 190 * on, 98, w=3, luz=(0, -1), d=2, sombra=0, trama=0)
        if on > 0:
            par = 0.75 + 0.25 * math.sin(t * 9)
            h.emitir(led, 1.3 * on * par)
            h.luz_radial(cxl + 265, cyl - 155, 300, (0.9, 0.9, 0.9), k=1.4 * on * par)
            h.luz_radial(cxl, cyl, 150, (0.8, 0.8, 0.8), k=0.9 * on)
        C.banda(h, "CON CÁMARA", cxl, cyl + 300, 78, t, self.t_camara, sem=15, claro=True)
        h.ambiente[:] = 0.36
        h.luz_radial(1150, 420, 1200, (1.0, 1.0, 1.0), k=0.9)
        h.luz_radial(cxl, cyl - 60, 620, (1.0, 1.0, 1.0), k=1.1)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "zumbido_lampara", 0.35, 0.0, dur=self.t_ynuestro - self.t0)
        self.ev(self.t_mensaje - 0.25, "sobre_desliza", 0.8, 0.0)
        for ini, n, cps in ((self.t_director - 0.2, 19, 26), (self.t_trans - 0.25, 24, 24), (self.t_deesas + 0.5, 25, 22)):
            self.ev(ini, "tecleo_rapido", 0.5, 0.0, dur=n / cps)
        self.ev(self.t_urgente, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_nadie - 0.5, "interruptor", 0.7, 0.3)
        self.ev(self.t_ynuestro - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_sospecho, "grave_inquietante", 0.6, 0.0, dur=3.0)
        self.ev(self.t_engano, "sello_golpe", 0.9, 0.2)
        self.ev(self.t_pero - 0.3, "sombra_crece", 0.6, 0.0, dur=3.0)
        for tm in (self.t_contaba - 0.15, self.t_asique + 0.1, self.t_mejor - 0.1):
            self.ev(tm + 0.35, "pieza_ajedrez", 0.9, 0.0)
        self.ev(self.t_invito - 0.3, "sobre_desliza", 0.8, 0.4)
        self.ev(self.t_reunion - 0.3, "tecleo_rapido", 0.5, 0.3, dur=0.8)
        self.ev(self.t_camara, "camara_zoom", 0.9, -0.3)
        self.ev(self.t_camara, "sello_golpe", 0.8, -0.3)
