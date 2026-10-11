# -*- coding: utf-8 -*-
"""Escena 18 «marcador»: el tablero de corcho con las dos columnas (COARTADA / HECHOS) unidas por hilos; el libro de cuentas con
los aciertos y los fallos (palomita y tache); la pista: el auto del EXPEDIENTE y el de la REALIDAD, al 75 %; el tablero de la
estación («RETRASADO»); la ficha vuelve de 2030 a 2029."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props as PR
import props3 as PR3
import props5 as PR5
from basen import BaseNoir
from esc_dudas import regla_anios
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, pulso


def marca(h, x, y, ok, u, sem=0, s=1.0):
    """Palomita (ok) o tache, dibujados a pluma con progreso u."""
    if u <= 0:
        return
    if ok:
        P = np.array([[x - 34 * s, y], [x - 10 * s, y + 30 * s], [x + 44 * s, y - 40 * s]])
        n = max(2, int(3 * min(1.0, u) + 0.999))
        h.trazo(P[:n], 13 * s, sem, color=(14, 14, 14), jit=0.5, taper=(0.2, 0.3))
    else:
        h.trazo(np.array([[x - 34 * s, y - 34 * s], [x + 34 * s, y + 34 * s]]), 13 * s, sem, color=(14, 14, 14), jit=0.5, taper=(0.2, 0.2))
        if u > 0.5:
            h.trazo(np.array([[x + 34 * s, y - 34 * s], [x - 34 * s, y + 34 * s]]), 13 * s, sem + 1, color=(14, 14, 14), jit=0.5,
                    taper=(0.2, 0.2))


class Marcador(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_entonces = w("Entonces")
        self.t_compare = w("Comparé")
        self.t_hechos = w("hechos")
        self.t_equipo = w("Su equipo")
        self.t_cuenta = w("cuenta")
        self.t_fallaron = w("fallaron")
        self.t_otras = w("Otras")
        self.t_centavo = w("centavo")
        self.t_final = w("La cuenta final")
        self.t_tres = w("tres cuartas")
        self.t_veloc = w("velocidad")
        self.t_noes = w("No es que")
        self.t_falsa = w("falsa")
        self.t_retras = w("retrasada")
        self.t_yeste = w("Y este año")
        self.t_volvio = w("volvió")
        self.t_calc = w("Su cálculo")
        self.t_2029 = w("dos mil veintinueve")
        self.plano(t0, self.p_compara)
        self.plano(self.t_equipo - 0.35, self.p_cuenta, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_final - 0.35, self.p_pista, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_noes - 0.35, self.p_estacion, tr="humo", dur=0.6)
        self.plano(self.t_yeste - 0.35, self.p_vuelve, tr="barrido", dur=0.55, dirx=-1)

    # ------------------------------------------------------------------ la coartada contra los hechos
    def p_compara(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        MU.corcho().pegar(h, 1.0, oscuro=0.85)
        C.banda(h, "LA COARTADA", 520, 130, 60, t, self.t_entonces + 0.3, sem=5, mundo=True)
        C.banda(h, "LOS HECHOS", 1400, 130, 60, t, self.t_entonces + 0.9, claro=True, sem=6, mundo=True)
        filas = (("«AGENTES EN 2025»", "AGENTES EN 2025"), ("«CARRERA CON CHINA»", "CONTROLES DE CHIPS"), ("«INGRESOS RÉCORD»", "INGRESOS RÉCORD"))
        for k, (a, b) in enumerate(filas):
            tk = self.t_entonces + 1.4 + k * 0.9
            if t < tk:
                continue
            y = 330 + k * 220
            PR3.tarjeta(h, 520, y, a, t, tk, ang=-0.04 + 0.03 * k, sem=40 + k * 10, s=1.35)
            PR3.chincheta(h, 520, y - 60, sem=45 + k * 10)
            PR3.tarjeta(h, 1400, y, b, t, tk + 0.25, ang=0.04 - 0.03 * k, sem=70 + k * 10, s=1.35)
            PR3.chincheta(h, 1400, y - 60, sem=75 + k * 10)
            PR3.hilo(h, (520, y - 60), (1400, y - 60), u=clamp01((t - tk - 0.4) / 0.4), sem=100 + k)
        PR.mano(h, 960 + 30 * math.sin(t * 1.3), 1010, 1.3, ang=-1.2, d=1, sem=130, dedos=0.3)
        h.ambiente[:] = 0.4
        h.luz_cono(960, -600, math.pi / 2, 0.7, 2400, (1.5, 1.5, 1.5), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ la cuenta
    def p_cuenta(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, -0.012)
        MU.escritorio().pegar(h, 1.0, oscuro=0.75, dx=-140, dy=60)
        T = K.hoja(h, 960, 560, 1560, 920, ang=-0.015, sem=10)
        P = T([(-700, -410)])[0]
        N.texto_maquina(h, "LA CUENTA · FEBRERO DE 2026", P[0], P[1], 54, t, self.t_equipo, cps=20, tono=0.05, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        filas = ((self.t_cuenta - 0.2, "Prueba de programación: predijo 85 %, fue 74,5 %", False),
                 (self.t_fallaron + 0.4, "Ventaja del líder: predijo meses, fue casi nula", False),
                 (self.t_otras, "Agentes torpes pero útiles en 2025", True),
                 (self.t_centavo - 0.9, "Ingresos: predijo 18 000 M, fueron 20 000 M", True))
        for k, (tk, s_, ok) in enumerate(filas):
            y = -250 + k * 150
            K.plano_(h, T(C.rect(-700, y + 80, 1400, 4)), 110, 30 + k)
            P = T([(-700, y)])[0]
            N.texto_maquina(h, s_, P[0], P[1], 38, t, tk, cps=34, tono=0.06, encuadrar=False)
            P = T([(640, y + 22)])[0]
            marca(h, P[0], P[1], ok, clamp01((t - tk - 1.0) / 0.3), sem=50 + k * 3)
        K.taza_arriba(h, 1760, 180, 1.0, 90, t)
        C.banda(h, "ALGUNAS FALLARON", 420, 1020, 50, t, self.t_fallaron, sem=5)
        C.banda(h, "OTRAS, CASI AL CENTAVO", 1440, 1020, 50, t, self.t_centavo - 0.4, claro=True, sem=6)
        h.ambiente[:] = 0.36
        h.luz_cono(800, -600, math.pi / 2 - 0.06, 0.6, 2400, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ a tres cuartas partes de la velocidad
    def p_pista(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 30, 8)
        av = smooth(clamp01((t - self.t_final + 0.2) / 2.4))
        x0, x1 = 240, 1680
        for k, (nom, f, y) in enumerate((("EXPEDIENTE", 1.0, 400), ("REALIDAD", 0.75, 760))):
            K.plano_(h, C.rect(x0 - 60, y, x1 - x0 + 240, 70), 60, 20 + k, grad=(30, y, y + 70))                  # el carril
            for q in range(14):
                K.plano_(h, C.rect(x0 + q * 120 - ((t * 240 * f) % 120), y + 30, 60, 8), 200, 30 + k * 20 + q, alfa=0.7)
            xa = x0 + (x1 - x0) * f * av
            PR5.auto(h, xa, y + 40, 0.9, t, vel=3.0 * f, sem=80 + k * 40, tono=40 + 20 * k)
            h.luz_cono(xa + 170, y + 14, 0.0, 0.2, 500, (1.4, 1.4, 1.4), k=0.9, suave=0.6)
            C.banda(h, nom, 250, y - 150, 46, t, self.t_final, claro=(k == 1), sem=5 + k)
            h.luz_radial(xa, y - 40, 600, (1.0, 1.0, 1.0), k=0.8)
        h.trazo(np.array([[x1 + 110, 300], [x1 + 110, 880]]), 9, 70, color=(240, 240, 240), jit=0.3, taper=(0, 0))        # la meta
        C.banda(h, "75 %", 1500, 590, 150, t, self.t_tres, claro=True, sem=8)
        C.banda(h, "DE LA VELOCIDAD DEL EXPEDIENTE", 960, 1010, 50, t, self.t_veloc - 0.4, sem=9)
        h.ambiente[:] = 0.5
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, vel=20, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ viene un poco retrasada
    def p_estacion(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 520, 0.0)
        K.pared(h, 60, 22, ladrillo=True)
        for q in (500, 1420):                                        # el tablero cuelga de dos cadenas
            h.trazo(np.array([[q, -100], [q, 190]]), 8, 20 + q, color=(30, 30, 30), jit=0.3, taper=(0, 0))
        bal = 0.012 * math.sin(t * 1.1)
        c = np.array([960, 190])
        h.pieza(PR.rot(C.rect(300, 190, 1320, 560), bal, c), 14, 30, w=8, luz=(0, -1), d=10, trama=0.2, rim=0.7)
        h.luz_fija(PR.rot(C.rect(320, 210, 1280, 520), bal, c), 0.9)
        N.texto_maquina(h, "LLEGADAS", 960, 260, 60, t, -99, cps=1e9, tono=0.95, centro=True, fuente=K.IMPACT, track=6.0, encuadrar=False)
        filas = (("DESTINO", "SUPERINTELIGENCIA", self.t_noes), ("PREVISTA", "2027", self.t_noes + 0.5),
                 ("ESTADO", "RETRASADA" if int(t * 2.5) % 2 or t < self.t_retras else "", self.t_retras - 0.4))
        for k, (a, b, tk) in enumerate(filas):
            y = 370 + k * 120
            K.plano_(h, C.rect(340, y + 76, 1240, 3), 80, 40 + k)
            N.texto_maquina(h, a, 360, y, 50, t, -99, cps=1e9, tono=0.6, fuente=K.IMPACT, encuadrar=False)
            N.texto_maquina(h, b, 760, y, 66 if k == 2 else 56, t, tk, cps=30, tono=0.97, fuente=K.IMPACT, track=3.0, encuadrar=False)
        # el andén: maleta, banco y un farol; el detective espera (su sombrero y hombros en primer término)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 50, 8, grad=(12, 930, 1200))
        h.pieza(C.rect(260, 870, 520, 26), 70, 60, w=5, luz=(0, -1), d=6, trama=0.4, rim=0.7)
        for q in (300, 720):
            h.pieza(C.rect(q, 896, 22, 90), 50, 61 + q, w=4, luz=(0, -1), d=4, trama=0.3)
        h.pieza(C.rect(1300, 850, 200, 130), 90, 70, w=5, luz=(0.2, -1), d=8, trama=0.5, rim=0.7)
        h.trazo(np.array([[1360, 850], [1370, 810], [1430, 810], [1440, 850]]), 8, 71, jit=0.3)
        C.banda(h, "NO ERA FALSA", 420, 110, 50, t, self.t_falsa - 0.6, sem=5)
        C.banda(h, "VIENE UN POCO RETRASADA", 1420, 110, 50, t, self.t_retras - 0.4, claro=True, sem=6)
        h.ambiente[:] = 0.42
        h.luz_cono(960, -400, math.pi / 2, 0.6, 1900, (1.4, 1.4, 1.4), k=0.9, suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=14, y0=300, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ volvió a acercar la fecha: 2029
    def p_vuelve(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 560, 0.0)
        K.pared(h, 30, 8)
        xs = regla_anios(h, t, sem=20)
        mv = smooth(clamp01((t - self.t_volvio + 0.2) / 1.2))
        fx = xs[4] + (xs[3] - xs[4]) * mv
        h.trazo(np.array([[xs[4], 750], [xs[4], 560]]), 4, 38, color=(150, 150, 150), alfa=0.6, jit=0.3, taper=(0, 0))       # donde estaba
        h.trazo(np.array([[fx, 750], [fx, 520]]), 7, 40, color=(240, 240, 240), jit=0.3, taper=(0, 0))
        h.pieza(np.asarray(elipse_(fx, 450, 96, 96, n=40)), 228, 41, w=7, luz=(0.2, -1), d=12, trama=0.2, rim=0)
        h.anillo(h.tf(np.asarray(elipse_(fx, 450, 76, 76, n=40))), 5 * h.zoom, 42, color=(30, 30, 30), jit=0.4)
        N.texto_maquina(h, "SU", fx, 420, 40, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
        N.texto_maquina(h, "APUESTA", fx, 468, 34, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
        PR.mano(h, fx + 190, 460 + 6 * math.sin(t * 6), 1.25, ang=0.0, d=-1, sem=60, dedos=0.5)
        C.banda(h, "AGOSTO DE 2026 · DATOS NUEVOS", 460, 100, 50, t, self.t_yeste + 0.2, sem=5)
        C.banda(h, "ACERCA LA FECHA", 460, 200, 54, t, self.t_volvio, claro=True, sem=6)
        C.banda(h, "SUPERINTELIGENCIA: 2029", 1300, 250, 76, t, self.t_2029 - 0.2, claro=True, sem=7)
        g = pulso(t, self.t_2029, 0.3, 1.0)
        h.ambiente[:] = 0.5
        h.luz_radial(fx, 450, 700, (1.0, 1.0, 1.0), k=1.0 + g)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, vel=10, y0=0, y1=1080, sube=False), bloom=0.5, flash=0.2 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        for k in range(3):
            self.ev(self.t_entonces + 1.4 + k * 0.9, "chincheta", 0.7, -0.4)
            self.ev(self.t_entonces + 1.8 + k * 0.9, "hilo_tenso", 0.5, 0.0)
        self.ev(self.t_equipo - 0.35, "paginas", 0.7, 0.0)
        for tk in (self.t_cuenta - 0.6, self.t_fallaron - 0.9, self.t_fallaron + 0.4, self.t_otras, self.t_centavo - 0.9):
            self.ev(tk, "tecleo_rapido", 0.5, -0.2, dur=0.9)
        for tk in (self.t_fallaron + 0.1, self.t_fallaron + 1.4):
            self.ev(tk, "tachon", 0.8, 0.4)
        for tk in (self.t_otras + 1.0, self.t_centavo + 0.1):
            self.ev(tk, "lapiz", 0.8, 0.4)
        self.ev(self.t_final - 0.35, "motores_carrera", 0.7, 0.0, dur=self.t_noes - self.t_final)
        self.ev(self.t_tres, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_noes - 0.35, "silencio_tono", 0.4, 0.0, dur=self.t_yeste - self.t_noes)
        self.ev(self.t_noes, "teletipo", 0.5, 0.0, dur=1.6)
        self.ev(self.t_retras - 0.4, "campana_bolsa", 0.7, 0.0)
        self.ev(self.t_yeste - 0.35, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_volvio - 0.2, "fichas_empuja", 0.9, 0.0)
        self.ev(self.t_2029 - 0.2, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_2029, "golpe_grave", 0.9, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
