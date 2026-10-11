# -*- coding: utf-8 -*-
"""Escena 3 «llamada»: la rejilla se enciende recuadro a recuadro («ahí están todos»); primer plano del falso director: su cara,
la onda de su voz, su mano que saluda; el empleado de frente con la duda (un «?» que se borra) y el ojo enorme con la reunión
reflejada en el iris; la libreta donde toma nota mientras, al fondo, los recuadros se apagan: llamada terminada."""
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

CAJA = (150.0, 70.0, 1620.0, 900.0)


class LlamadaEsc(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.call = C.Llamada(sem=40)
        self.jefe = Frontal(sem=40)                      # el mismo «director financiero» del recuadro 0
        self.emp = Frontal(sem=210)
        self.t_imag = w("Imagínalo")
        self.t_conecta = w("Se conecta")
        self.t_todos = w("todos")
        self.t_director = w("El director")
        self.t_varios = w("Varios")
        self.t_gente = w("Gente")
        self.t_caras = w("Las mismas caras")
        self.t_voces = w("voces")
        self.t_gestos = w("gestos")
        self.t_duda = w("Y la duda")
        self.t_cuerpo = w("cuerpo", fin=True)
        self.t_porque = w("Porque")
        self.t_correo = w("correo")
        self.t_pero = w("Pero no")
        self.t_ojos = w("ojos")
        self.t_enla = w("En la reunión")
        self.t_instr = w("instrucciones")
        self.t_nota = w("Él tomó")
        self.t_yla = w("Y la llamada")
        self.t_termino = w("terminó")
        self.cam_a = Pista([(t0, (960, 540, 1.0)), (self.t_director - 0.3, (960, 540, 1.04), "l"),
                            (self.t_director + 0.6, (520, 330, 1.75), "io"), (self.t_varios - 0.1, (540, 330, 1.8), "l"),
                            (self.t_varios + 0.9, (1380, 330, 1.7), "io"), (self.t_gente, (1380, 760, 1.7), "io"),
                            (self.t_caras - 0.2, (760, 760, 1.65), "io")])
        self.plano(t0, self.p_rejilla)
        self.plano(self.t_caras - 0.3, self.p_jefe, tr="empuje", dur=0.55, centro=(W * 0.3, H * 0.4))
        self.plano(self.t_duda - 0.35, self.p_duda, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_pero - 0.3, self.p_ojo, tr="empuje", dur=0.6, centro=(W * 0.45, H * 0.4))
        self.plano(self.t_enla - 0.35, self.p_nota, tr="barrido", dur=0.6, dirx=1)

    # ------------------------------------------------------------------ todos se conectan
    def p_rejilla(self, h, t, u):
        cx, cy, z = self.cam_a(t)
        h.camara(z, cx, cy, 0.0)
        h.img[:] = 0.05
        C.monitor(h, CAJA, sem=60, pie=False)
        orden = [0, 3, 1, 4, 2, 5]
        ap = [1.0] * 6
        for q, k in enumerate(orden):
            tk = self.t_conecta + 0.25 + q * max(0.2, (self.t_todos - self.t_conecta) / 6.0)
            ap[k] = 1 - clamp01((t - tk) / 0.18)
        habla = 0 if t > self.t_director - 0.2 else None
        self.call.dibujar(h, t, CAJA, apagado=ap, habla=habla, asiente=0.0)
        if t < self.t_conecta + 0.3:
            n = int((t - self.t0) * 2.5) % 4
            C.banda(h, "CONECTANDO" + "." * n, 960, 520, 70, t, -99, sem=3)
        h.ambiente[:] = 0.18
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ la cara, la voz, el gesto
    def p_jefe(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.pieza(C.rect(-100, -100, W + 200, H + 200), 100, 5, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0,
                grad=(46, 0, H))
        for q in range(7):                                         # la estantería detrás (su «oficina»)
            yy = 90 + q * 150
            h.trazo(np.array([[-40, yy], [W + 40, yy]]), 5, 10 + q, alfa=0.45, jit=0.4)
            r = np.random.default_rng(q)
            xx = 20.0
            while xx < W:
                an = r.uniform(26, 70)
                if r.uniform() < 0.8:
                    h.pieza(C.rect(xx, yy - r.uniform(70, 128), an, 126), r.uniform(50, 130), 100 + q * 40 + int(xx), w=2.5, luz=(0, -1),
                            d=3, trama=0.3, sombra=0.3)
                xx += an + 4
        s = 3.3
        nod = 0.5 * (0.5 - 0.5 * math.cos((t - self.t_gestos) * 6.0)) if t > self.t_gestos else 0.0
        p = dict(x=820, y=520 + 474 * s + nod * 40, s=s, luz=(0.0, -1.0), rim=0.8, pelo="blanco", traje=92, gafas=True,
                 mira=0.4 * math.sin(t * 0.9), cabeza=0.03 * math.sin(t * 0.7))
        self.jefe.dibujar(h, p)
        if t > self.t_gestos - 0.2:                               # saluda con la mano
            a = e_out(clamp01((t - self.t_gestos + 0.2) / 0.35))
            PR.mano(h, 1560, 1300 - 620 * a, s=1.5, ang=-math.pi / 2 + 0.25 * math.sin((t - self.t_gestos) * 9), d=1, tono=150, sem=30,
                    dedos=1.0, manga=92)
        if t > self.t_voces - 0.2:                                # la onda de la voz
            a = smooth(clamp01((t - self.t_voces + 0.2) / 0.3))
            for q in range(46):
                amp = (30 + 150 * abs(math.sin(t * (7 + q * 0.37) + q * 1.3)) * (0.4 + 0.6 * abs(math.sin(q * 0.23 + t)))) * a
                bx = 1130 + q * 16
                h.trazo(np.array([[bx, 880 - amp / 2], [bx, 880 + amp / 2]]), 9, 300 + q, color=(240, 240, 240), jit=0, taper=(0, 0))
        C.banda(h, "DIR. FINANCIERO", 340, 930, 46, t, -99, sem=4)
        C.banda(h, "LAS MISMAS CARAS", 1500, 150, 58, t, self.t_caras, claro=True, sem=6)
        C.banda(h, "LAS MISMAS VOCES", 1500, 250, 58, t, self.t_voces, claro=True, sem=7)
        C.banda(h, "LOS MISMOS GESTOS", 1500, 350, 58, t, self.t_gestos, claro=True, sem=8)
        h.ambiente[:] = 0.95
        return h.acabado(t, niebla=None, bloom=0.3, vin=1.2)

    # ------------------------------------------------------------------ la duda se va
    def p_duda(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.pieza(C.rect(-200, -200, W + 400, H + 400), 86, 3, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, grad=(40, 0, H))
        for q in range(9):                                        # archivadores y marcos en la pared del fondo
            h.pieza(C.rect(1450 + (q % 3) * 150, 120 + (q // 3) * 250, 130, 220), 60 + 8 * (q % 2), 300 + q, w=3, luz=(-0.5, -1), d=6,
                    trama=0.4, rim=0.4)
        alivio = smooth(clamp01((t - self.t_cuerpo + 0.4) / 0.8))
        s = 2.5
        p = dict(x=1180, y=500 + 474 * s + 16 * alivio, s=s, luz=(-0.9, -0.3), rim=0.9, pelo="oscuro", traje=150, mira=-0.8,
                 cabeza=0.4 - 0.4 * alivio)
        self.emp.dibujar(h, p)
        # el signo de interrogación que se deshace en humo
        if alivio < 1:
            N.texto_maquina(h, "?", 640, 330 - 120 * alivio, 430 * (1 + 0.25 * alivio), t, -99, cps=1e9, tono=0.95, alfa=1 - alivio,
                            centro=True, fuente="C:/Windows/Fonts/impact.ttf", encuadrar=False)
        N.humo(h, t, 640, 380, k=1.4 * math.sin(math.pi * clamp01(alivio)), ancho=3.0, hebras=6, viento=(10, -120))
        # el correo, abajo: de eso sí se puede desconfiar
        if t > self.t_correo - 0.4:
            a = e_out(clamp01((t - self.t_correo + 0.4) / 0.4))
            PR.sobre(h, 470, 1250 - 420 * a, s=1.25, ang=-0.12, abierto=0.0, sem=40, texto="", t=t)
            C.banda(h, "DEL CORREO, SÍ", 470, 1005, 46, t, self.t_correo, claro=True, sem=9)
        h.ambiente[:] = 0.26
        h.luz_persiana(np.array([[-100, 60], [1300, -60], [1500, 1000], [-200, 1100]]), k=1.0, n=13, abierto=0.5)
        h.luz_radial(360, 560, 1500, (1.0, 1.0, 1.0), k=1.2)                 # la pantalla, a la izquierda
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=900, sube=False))

    # ------------------------------------------------------------------ sus propios ojos
    def p_ojo(self, h, t, u):
        h.camara(1.0 + 0.05 * u, 960, 540, 0.0)
        h.pieza(C.rect(-100, -100, W + 200, H + 200), 118, 5, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)   # piel
        cx, cy = 960, 560
        par = pulso(t, self.t_ojos + 1.2, 0.3, 1.0)                           # un parpadeo
        ab = 1.0 - 0.9 * par
        ojo = [(cx - 760, cy + 10)] + [(cx - 760 + 1520 * q / 12, cy - 300 * ab * math.sin(math.pi * q / 12)) for q in range(1, 12)] + \
              [(cx + 760, cy + 10)] + [(cx + 760 - 1520 * q / 12, cy + 230 * ab * math.sin(math.pi * q / 12)) for q in range(1, 12)]
        h.pieza(np.array(ojo), 226, 20, w=11, luz=(0, -1), d=30, trama=0.5, sombra=0.5, rim=0)
        if ab > 0.3:
            mx = 30 * math.sin(t * 0.7)
            h.pieza(elipse_(cx + mx, cy - 20, 250, 250 * min(1.0, ab * 1.05), n=50), 74, 21, w=9, luz=(0, -1), d=24, trama=0.5, rim=0.4)
            for q in range(26):                                               # fibras del iris
                a = q * 2 * math.pi / 26
                h.trazo(np.array([[cx + mx + 110 * math.cos(a), cy - 20 + 110 * math.sin(a)],
                                  [cx + mx + 236 * math.cos(a), cy - 20 + 236 * math.sin(a) * min(1.0, ab * 1.05)]]), 3.5, 30 + q,
                        alfa=0.5, jit=0.4)
            h.pieza(elipse_(cx + mx, cy - 20, 108, 108, n=36), 8, 22, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
            # la reunión reflejada en la pupila: seis recuadros con su cabecita
            for k in range(6):
                rx = cx + mx - 96 + (k % 3) * 66
                ry = cy - 82 + (k // 3) * 62
                q4 = C.rect(rx, ry, 58, 52)
                h.pieza(q4, 190, 60 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.3)
                h.pieza(elipse_(rx + 29, ry + 22, 10, 12, n=12), 60, 70 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
                h.pieza(C.rect(rx + 12, ry + 36, 34, 16), 50, 80 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.3)
                h.emitir(q4, 0.35 + 0.1 * math.sin(t * 5 + k))
        # párpado superior, pliegue, pestañas y ceja
        arr = [(cx - 780 + 1560 * q / 16, cy + 10 - (300 * ab + 20) * math.sin(math.pi * q / 16)) for q in range(17)]
        h.trazo(np.array(arr), 26, 90, jit=0.5, taper=(0.5, 0.5))
        h.trazo(np.array([(x_, y_ - 110) for x_, y_ in arr[2:15]]), 9, 91, alfa=0.6, jit=0.5)
        for q in range(2, 15):
            x_, y_ = arr[q]
            h.trazo(np.array([[x_, y_], [x_ + (q - 8) * 9, y_ - 50 - 20 * ab]]), 6, 92 + q, taper=(0, 0.9), jit=0.4)
        ceja = [(cx - 700 + 1400 * q / 10, cy - 520 - 70 * math.sin(math.pi * q / 10) - 30 * alz) for q, alz in
                zip(range(11), [smooth(clamp01((t - self.t_ojos) / 0.4))] * 11)]
        h.trazo(np.array(ceja), 60, 120, jit=0.8, taper=(0.3, 0.7))
        C.banda(h, "«LO VI CON MIS PROPIOS OJOS»", 960, 990, 54, t, self.t_ojos, sem=10)
        h.ambiente[:] = 0.55
        h.luz_radial(cx - 300, cy - 100, 1500, (1.0, 1.0, 1.0), k=0.9)
        return h.acabado(t, niebla=None, bloom=0.4, vin=1.3)

    # ------------------------------------------------------------------ toma nota; la llamada termina
    def p_nota(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960 + 6 * u, 540, -0.02)
        MU.escritorio().pegar(h, 1.0, oscuro=0.75)
        # el monitor, arriba, con los recuadros que se van apagando
        caja = (1010.0, 40.0, 820.0, 470.0)
        C.monitor(h, caja, sem=60, pie=False)
        ap = [clamp01((t - (self.t_yla + 0.12 * q)) / 0.2) for q in (2, 0, 4, 1, 5, 3)]
        self.call.dibujar(h, t, caja, apagado=ap, habla=0 if t < self.t_nota else None, rotulos=False,
                          enc=1.0 - 0.9 * min(ap))
        C.banda(h, "LLAMADA FINALIZADA", caja[0] + caja[2] / 2, caja[1] + caja[3] / 2, 54, t, self.t_termino, claro=True, sem=11, mundo=True)
        # la libreta
        lib = PR.rot(C.rect(180, 330, 720, 700), -0.05, np.array([540, 680]))
        h.pieza(lib, 224, 30, w=5, luz=(0.2, -1), d=12, trama=0, rim=0)
        for q in range(9):                                                  # espiral
            a = lib[0] + (lib[1] - lib[0]) * (0.08 + 0.105 * q)
            h.anillo(elipse_(a[0], a[1] - 4, 12, 20, n=14), 4, 31 + q, jit=0.3)
        N.texto_maquina(h, "INSTRUCCIONES", 250, 400, 52, t, self.t_instr - 0.2, cps=20, tono=0.05, fuente=N.FUENTE_SELLO, encuadrar=False)
        r = np.random.default_rng(3)
        n_l = 6
        esc_x = 0.0
        for q in range(n_l):                                                # renglones manuscritos que avanzan
            tk = self.t_nota + q * max(0.25, (self.t_yla - self.t_nota) / n_l)
            a = clamp01((t - tk) / 0.5)
            if a <= 0:
                continue
            L = 520 * r.uniform(0.6, 1.0)
            xs = np.linspace(0, L * a, max(2, int(40 * a)))
            ys = 9 * np.sin(xs * 0.11 + q) * (0.5 + 0.5 * np.sin(xs * 0.031 + q * 2))
            P = np.stack([268 + xs, 520 + q * 74 + ys - (268 + xs - 540) * 0.05], 1)
            h.trazo(P, 5, 45 + q, jit=0.5, taper=(0.1, 0.1))
            if a < 1:
                esc_x = P[-1]
        if isinstance(esc_x, np.ndarray):                                   # la mano con la pluma, donde va escribiendo
            h.trazo(np.array([esc_x, esc_x + (190, -170)]), 13, 55, color=(20, 20, 20), jit=0.2, taper=(0.8, 0))
            PR.mano(h, esc_x[0] + 120, esc_x[1] - 10, s=1.1, ang=math.pi + 0.45, d=1, tono=140, sem=56, dedos=0.2, manga=200)
        h.ambiente[:] = 0.34
        h.luz_radial(520, 640, 900, (1.0, 1.0, 1.0), k=1.0)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "zumbido_servidores", 0.3, 0.0, dur=self.t_duda - self.t0)
        for q in range(6):
            self.ev(self.t_conecta + 0.25 + q * max(0.2, (self.t_todos - self.t_conecta) / 6.0), "interruptor", 0.6, -0.5 + 0.2 * q)
        self.ev(self.t_director - 0.3, "camara_zoom", 0.6, -0.3)
        self.ev(self.t_caras - 0.3, "barrido_aire", 0.6, 0.0, dur=0.7)
        for tb in (self.t_caras, self.t_voces, self.t_gestos):
            self.ev(tb, "sello_golpe", 0.7, 0.4)
        self.ev(self.t_voces, "datos", 0.4, 0.3, dur=1.6)
        self.ev(self.t_duda - 0.35, "barrido_aire", 0.6, -0.3, dur=0.7)
        self.ev(self.t_cuerpo - 0.4, "exhala", 0.7, -0.2, dur=1.6)
        self.ev(self.t_correo - 0.4, "sobre_desliza", 0.7, -0.4)
        self.ev(self.t_pero - 0.3, "camara_zoom", 0.7, 0.0)
        self.ev(self.t_ojos, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_enla - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_nota, "lapiz", 0.8, -0.3, dur=max(1.0, self.t_yla - self.t_nota))
        for q in range(6):
            self.ev(self.t_yla + 0.12 * q, "interruptor", 0.6, 0.5 - 0.1 * q)
        self.ev(self.t_termino, "silencio_tono", 0.5, 0.0, dur=2.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
