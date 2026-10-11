# -*- coding: utf-8 -*-
"""Escena 4 «dinero»: la semana se tacha día a día en el calendario; quince órdenes de pago vuelan desde su terminal a cinco cajas
fuertes (15 -> 5); el contador sube hasta HK$ 200 000 000 sobre fajos que se apilan; tres objetos de atraco tachados (revólver,
pasamontañas, cerradura) y la puerta principal abierta por la que sale el maletín, con la orden firmada y sellada."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, bezier2, elipse_, pulso, suave

DIAS = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]


def tache(h, cx, cy, r, a, sem=0, w=16, color=(240, 240, 240)):
    """Tachón en X que se traza (a: 0..1)."""
    if a <= 0:
        return
    a1, a2 = clamp01(a * 2), clamp01(a * 2 - 1)
    h.trazo(np.array([[cx - r, cy - r], [cx - r + 2 * r * a1, cy - r + 2 * r * a1]]), w, sem, color=color, jit=0.6, taper=(0.2, 0.2))
    if a2 > 0:
        h.trazo(np.array([[cx + r, cy - r], [cx + r - 2 * r * a2, cy - r + 2 * r * a2]]), w, sem + 1, color=color, jit=0.6, taper=(0.2, 0.2))


def caja_fuerte(h, x, y, s, sem, brillo=0.0, n=""):
    h.pieza(C.rect(x - 110 * s, y - 120 * s, 220 * s, 240 * s), 52 + 60 * brillo, sem, w=7 * s, luz=(-0.4, -1), d=14 * s, trama=0.5, rim=0.7)
    h.pieza(C.rect(x - 86 * s, y - 96 * s, 172 * s, 192 * s), 70 + 70 * brillo, sem + 1, w=4 * s, luz=(-0.4, -1), d=8 * s, trama=0.3, rim=0.5)
    h.pieza(elipse_(x, y, 46 * s, 46 * s, n=26), 30, sem + 2, w=5 * s, luz=(-0.4, -1), d=8 * s, trama=0.3, rim=0.7)
    for q in range(4):
        a = q * math.pi / 2 + brillo * 2.2
        h.trazo(np.array([[x, y], [x + 62 * s * math.cos(a), y + 62 * s * math.sin(a)]]), 8 * s, sem + 3 + q, jit=0.3)
    for q in (-1, 1):
        h.pieza(C.rect(x - 124 * s, y + q * 70 * s - 16 * s, 16 * s, 32 * s), 24, sem + 8 + q, w=3 * s, luz=(0, -1), d=3, trama=0)


class Dinero(BaseNoir):
    TR_SALIDA = ("barrido", 0.6)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_semana = w("semana")
        self.t_hizo = w("hizo")
        self.t_pidieron = w("pidieron", fin=True)
        self.t_quince = w("Quince")
        self.t_cinco = w("cinco")
        self.t_hk = w("Hong", frase=1)
        self.t_dosc = w("Doscientos")
        self.t_mas = w("Más de")
        self.t_amer = w("americanos", fin=True)
        self.t_pistola = w("Sin pistola")
        self.t_pasa = w("Sin pasamontañas")
        self.t_forzar = w("Sin forzar")
        self.t_botin = w("El botín")
        self.t_puerta = w("puerta")
        self.t_firma = w("firma")
        self.t_sello = w("sello")
        self.plano(t0, self.p_semana)
        self.plano(self.t_quince - 0.35, self.p_quince, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_dosc - 0.35, self.p_monto, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_pistola - 0.35, self.p_sin, tr="barrido", dur=0.55, dirx=-1)
        self.plano(self.t_botin - 0.3, self.p_puerta, tr="fundido", dur=0.5)

    # ------------------------------------------------------------------ la semana
    def p_semana(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960 + 12 * u, 540, 0.015)
        MU.corcho().pegar(h, 1.0, oscuro=0.8)
        dur = max(1.5, self.t_pidieron - self.t_semana)
        for k, d in enumerate(DIAS):
            x, y = 170 + k * 232, 330 + 26 * math.sin(k * 1.9)
            ang = 0.05 * math.sin(k * 2.3)
            P = PR.rot(C.rect(x, y, 204, 250), ang, np.array([x + 102, y + 125]))
            h.pieza(P, 222, 20 + k, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
            h.pieza(PR.rot(C.rect(x, y, 204, 62), ang, np.array([x + 102, y + 125])), 34, 30 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                    linea=False)
            N.texto_maquina(h, d, x + 102, y + 30, 40, t, -99, cps=1e9, tono=0.95, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            h.pieza(elipse_(x + 102, y - 4, 10, 10, n=12), 26, 40 + k, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.8)        # chincheta
            tk = self.t_semana - 0.2 + k * dur / 7.0
            tache(h, x + 102, y + 150, 62, clamp01((t - tk) / 0.28), sem=50 + 2 * k, w=18, color=(18, 18, 18))
        N.texto_maquina(h, "LA SEMANA SIGUIENTE", 960, 200, 62, t, self.t_semana - 0.3, cps=22, tono=0.94, centro=True,
                        fuente=N.FUENTE_SELLO, encuadrar=False)
        N.texto_maquina(h, "Hizo lo que le pidieron.", 960, 760, 50, t, self.t_hizo, cps=22, tono=0.94, centro=True, encuadrar=False)
        h.ambiente[:] = 0.40
        h.luz_cono(960, -500, math.pi / 2, 0.62, 2100, (1.4, 1.4, 1.4), suave=0.6)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ 15 -> 5
    def p_quince(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, 0.0)
        h.img[:] = 0.07
        org = np.array([250.0, 560.0])
        dest = [np.array([1560.0, 150.0 + k * 200]) for k in range(5)]
        dur = max(2.0, self.t_hk + 1.2 - self.t_quince)
        llegan = [0] * 5
        vuelo = []
        for q in range(15):
            tk = self.t_quince + q * dur / 16.0
            a = clamp01((t - tk) / 0.75)
            k = q % 5
            if a >= 1:
                llegan[k] += 1
            elif a > 0:
                vuelo.append((q, k, a))
        for k in range(5):                                       # los cables
            c = bezier2(org + (90, 0), np.array([900.0, 540 + (k - 2) * 60.0]), dest[k] - (130, 0), n=30)
            h.trazo(c, 4, 20 + k, color=(110, 110, 110), jit=0.4, taper=(0, 0))
        # el terminal del empleado
        C.monitor(h, (110.0, 440.0, 280.0, 190.0), sem=30)
        h.pieza(C.rect(110, 440, 280, 190), 200, 34, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        N.texto_maquina(h, "ENVIAR", 250, 535, 46, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        for k in range(5):
            br = clamp01(llegan[k] / 3.0) * 0.6 + 0.4 * pulso(t, self.t_quince + (k + 5 * (llegan[k] - 1)) * dur / 16.0 + 0.75, 0.4, 1.0)
            caja_fuerte(h, dest[k][0], dest[k][1], 0.72, 60 + 12 * k, brillo=clamp01(br))
            N.texto_maquina(h, f"CUENTA {k + 1}", dest[k][0] + 100, dest[k][1] - 30, 34, t, self.t_cinco - 0.2 + 0.12 * k, cps=30, tono=0.9,
                            encuadrar=False)
            if llegan[k]:
                N.texto_maquina(h, "×" + str(llegan[k]), dest[k][0] + 100, dest[k][1] + 14, 40, t, -99, cps=1e9, tono=0.97,
                                fuente=N.FUENTE_SELLO, encuadrar=False)
        for q, k, a in vuelo:                                    # las órdenes de pago en vuelo
            c = bezier2(org + (90, 0), np.array([900.0, 540 + (k - 2) * 60.0]), dest[k] - (130, 0), n=30)
            p = c[min(len(c) - 1, int(smooth(a) * (len(c) - 1)))]
            P = PR.rot(C.rect(p[0] - 46, p[1] - 30, 92, 60), 0.5 * math.sin(a * 7 + q), p)
            h.pieza(P, 228, 130 + q, w=3, luz=(0, -1), d=4, trama=0, rim=0)
            h.trazo(np.array([P[0] * 0.7 + P[3] * 0.3, P[1] * 0.7 + P[2] * 0.3]) , 3, 150 + q, alfa=0.6, jit=0.2)
            h.luz_radial(p[0], p[1], 150, (0.8, 0.8, 0.8), k=0.9)
        tot = sum(llegan)
        N.texto_maquina(h, f"{tot:02d}", 800, 800, 230, t, -99, cps=1e9, tono=0.97, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        N.texto_maquina(h, "TRANSFERENCIAS", 800, 960, 56, t, -99, cps=1e9, tono=0.85, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        C.banda(h, "5 CUENTAS · HONG KONG", 800, 110, 56, t, self.t_cinco, claro=True, sem=5)
        h.ambiente[:] = 0.55
        h.luz_radial(250, 540, 600, (0.9, 0.9, 0.9), k=0.9)
        h.luz_radial(1560, 540, 1100, (0.9, 0.9, 0.9), k=0.8)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=None, bloom=0.5)

    # ------------------------------------------------------------------ el monto
    def p_monto(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960, 540 - 5 * u, 0.0)
        h.img[:] = 0.06
        sub = clamp01((t - self.t_dosc) / max(1.2, self.t_mas - self.t_dosc - 0.5))
        sub = 1 - (1 - sub) ** 3
        # fajos de billetes que se apilan al fondo
        nf = int(sub * 60)
        for q in range(nf):
            col, fila = q % 12, q // 12
            x, y = 150 + col * 140 + 10 * math.sin(q * 3.1), 1040 - fila * 62
            h.pieza(C.rect(x, y - 54, 126, 54), 150 - 14 * (q % 3), 20 + q, w=3.5, luz=(0, -1), d=6, trama=0.3, rim=0.4, sombra=0.5)
            h.pieza(C.rect(x + 46, y - 54, 34, 54), 226, 100 + q, w=2, luz=(0, -1), d=2, trama=0, sombra=0)
        v = int(round(200_000_000 * sub / 100_000) * 100_000)
        s = f"{v:,}".replace(",", " ")
        N.texto_maquina(h, "HK$", 250, 250, 120, t, -99, cps=1e9, tono=0.80, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        N.texto_maquina(h, s, 1100, 250, 210, t, -99, cps=1e9, tono=0.98, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        N.texto_maquina(h, "doscientos millones de dólares de Hong Kong", 960, 410, 42, t, self.t_dosc + 0.2, cps=30, tono=0.85,
                        centro=True, encuadrar=False)
        C.banda(h, "MÁS DE US$ 25 000 000", 960, 560, 92, t, self.t_mas, claro=True, sem=6)
        h.ambiente[:] = 0.6
        h.luz_cono(960, -500, math.pi / 2, 0.6, 2200, (1.2, 1.2, 1.2), suave=0.6)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.35)

    # ------------------------------------------------------------------ sin pistola, sin pasamontañas, sin forzar nada
    def p_sin(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, -0.01)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        ts = (self.t_pistola, self.t_pasa, self.t_forzar)
        xs = (360, 960, 1560)
        for k in range(3):
            a = e_out(clamp01((t - ts[k] + 0.25) / 0.35))
            if a <= 0:
                continue
            x, y = xs[k], 500 + 500 * (1 - a)
            h.pieza(PR.rot(C.rect(x - 230, y - 250, 460, 500), 0.04 * (k - 1), np.array([x, y])), 216, 20 + k, w=4, luz=(0.2, -1), d=10,
                    trama=0, rim=0)
            if k == 0:
                PR.revolver(h, x - 10, y + 10, s=1.0, ang=-0.15, d=1, sem=40)
            elif k == 1:                                          # pasamontañas
                h.pieza(np.array(suave([(x - 110, y + 170), (x - 130, y - 20), (x - 96, y - 150), (x, y - 196), (x + 96, y - 150),
                                        (x + 130, y - 20), (x + 110, y + 170)], 5)), 30, 50, w=7, luz=(0.3, -1), d=16, trama=0.6, rim=0.6)
                h.pieza(np.array(suave([(x - 84, y - 50), (x, y - 70), (x + 84, y - 50), (x + 76, y - 4), (x, y + 10), (x - 76, y - 4)], 4)),
                        150, 51, w=4, luz=(0.3, -1), d=5, trama=0.3)
                for sx in (-1, 1):
                    h.pieza(elipse_(x + sx * 40, y - 34, 18, 11, n=14), 232, 52 + sx, w=3, luz=(0, -1), d=2, trama=0, sombra=0)
                    h.pieza(elipse_(x + sx * 40, y - 34, 7, 7, n=10), 8, 55 + sx, w=0, luz=(0, -1), d=1, trama=0, sombra=0, linea=False)
                for q in range(6):
                    h.trazo(np.array([[x - 100 + q * 40, y + 60], [x - 104 + q * 40, y + 160]]), 3, 60 + q, alfa=0.5, jit=0.4)
            else:                                                 # cerradura con ganzúa
                h.pieza(elipse_(x, y - 20, 150, 150, n=40), 96, 70, w=7, luz=(0.3, -1), d=16, trama=0.5, rim=0.7)
                h.pieza(elipse_(x, y - 20, 108, 108, n=36), 150, 71, w=5, luz=(0.3, -1), d=8, trama=0.3, rim=0.5)
                h.pieza(elipse_(x, y - 50, 30, 30, n=18), 10, 72, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
                h.pieza(np.array([[x - 16, y - 40], [x + 16, y - 40], [x + 28, y + 50], [x - 28, y + 50]]), 10, 73, w=0, luz=(0, -1), d=1,
                        sombra=0, trama=0, linea=False)
                h.trazo(np.array([[x + 200, y + 190], [x + 60, y + 30], [x + 6, y - 10]]), 7, 74, jit=0.3, taper=(0.2, 0.7))
            N.texto_maquina(h, ("SIN PISTOLA", "SIN PASAMONTAÑAS", "SIN FORZAR NADA")[k], x, y + 300, 46, t, ts[k], cps=40, tono=0.95,
                            centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            tache(h, x, y - 10, 190, clamp01((t - ts[k] - 0.25) / 0.3), sem=80 + 2 * k, w=26, color=(14, 14, 14))
        h.ambiente[:] = 0.42
        h.luz_radial(960, 440, 1500, (1.0, 1.0, 1.0), k=0.8)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ por la puerta principal
    def p_puerta(self, h, t, u):
        h.camara(0.93 + 0.025 * u, 960, 520, 0.0)
        h.img[:] = 0.07
        # fachada del banco: columnas, dintel y la puerta abierta que derrama luz
        h.pieza(C.rect(-100, -100, W + 200, 1000), 46, 10, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, grad=(24, 0, 900))
        for k in range(6):
            x = 100 + k * 344
            if k in (2, 3):
                continue
            h.pieza(C.rect(x - 46, 150, 92, 750), 96, 20 + k, w=6, luz=(-0.5, -0.6), d=20, trama=0.6, rim=0.6)
            for q in range(4):
                h.trazo(np.array([[x - 30 + q * 20, 170], [x - 30 + q * 20, 880]]), 3, 30 + k * 5 + q, alfa=0.4, jit=0.3)
            h.pieza(C.rect(x - 66, 110, 132, 44), 110, 60 + k, w=5, luz=(-0.5, -0.6), d=8, trama=0.3, rim=0.6)
        h.pieza(C.rect(-100, 20, W + 200, 96), 80, 70, w=6, luz=(0, -1), d=14, trama=0.5, rim=0.5)
        N.texto_maquina(h, "ENTRADA PRINCIPAL", 960, 66, 54, t, -99, cps=1e9, tono=0.95, centro=True, fuente=N.FUENTE_SELLO,
                        track=10, encuadrar=False)
        ab = smooth(clamp01((t - self.t_botin + 0.2) / 0.9))
        pu = C.rect(700, 190, 520, 710)
        h.pieza(pu, 236, 80, w=7, luz=(0, -1), d=4, sombra=0, trama=0)
        for sx in (-1, 1):                                        # las dos hojas que se abren
            an = 260 * (1 - 0.82 * ab)
            x0 = 700 if sx < 0 else 1220 - an
            h.pieza(C.rect(x0, 190, an, 710), 40, 81 + sx, w=6, luz=(0, -1), d=10, trama=0.5, rim=0.5)
        for q in range(4):                                        # escalones
            h.pieza(C.rect(560 - q * 60, 900 + q * 46, 800 + q * 120, 46), 90 - 12 * q, 90 + q, w=5, luz=(0, -1), d=8, trama=0.4, rim=0.5)
        # el maletín que baja los escalones solo
        sale = smooth(clamp01((t - self.t_puerta + 0.3) / 1.6))
        if sale > 0:
            mx, my = 960 - 40 * sale, 880 + 150 * sale - 26 * abs(math.sin(sale * math.pi * 4))
            sc = 0.7 + 0.5 * sale
            h.pieza(C.rect(mx - 120 * sc, my - 150 * sc, 240 * sc, 150 * sc), 26, 100, w=6, luz=(0, -1), d=10, trama=0.5, rim=0.9)
            h.trazo(np.array([[mx - 46 * sc, my - 150 * sc], [mx - 40 * sc, my - 190 * sc], [mx + 40 * sc, my - 190 * sc],
                              [mx + 46 * sc, my - 150 * sc]]), 10 * sc, 101, jit=0.3, taper=(0, 0))
            for sx in (-1, 1):
                h.pieza(C.rect(mx + sx * 70 * sc - 12 * sc, my - 150 * sc, 24 * sc, 30 * sc), 200, 102 + sx, w=2, luz=(0, -1), d=2, trama=0)
        # la orden, firmada y sellada
        if t > self.t_firma - 0.5:
            a = e_out(clamp01((t - self.t_firma + 0.5) / 0.4))
            ox, oy = 1560, 620 + 600 * (1 - a)
            h.pieza(PR.rot(C.rect(ox - 250, oy - 300, 500, 600), 0.06, np.array([ox, oy])), 226, 110, w=4, luz=(0.2, -1), d=10, trama=0,
                    rim=0)
            N.texto_maquina(h, "ORDEN DE PAGO", ox, oy - 230, 44, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO,
                            encuadrar=False)
            for q in range(5):
                h.pieza(C.rect(ox - 190, oy - 150 + q * 46, 380 * (0.6 + 0.4 * ((q * 7) % 3) / 2), 14), 120, 112 + q, w=0, luz=(0, -1), d=1,
                        sombra=0, trama=0, linea=False, alfa=0.7, jit=0.3)
            fa = clamp01((t - self.t_firma) / 0.7)
            if fa > 0:                                            # la firma
                xs = np.linspace(0, 300 * fa, max(2, int(60 * fa)))
                ys = 34 * np.sin(xs * 0.07) * np.cos(xs * 0.023) - xs * 0.08
                h.trazo(np.stack([ox - 170 + xs, oy + 150 + ys], 1), 5, 120, jit=0.4, taper=(0.1, 0.3))
            N.sello(h, "AUTORIZADO", ox + 20, oy + 40, 62, t, self.t_sello, rot=-12, tono=0.05)
        h.ambiente[:] = 0.26
        C.luz_rect(h, np.array([[700 + 200 * (1 - ab), 190], [1220 - 200 * (1 - ab), 190], [1420, 1100], [500, 1100]]), 1.5 * ab, suave_=14)
        h.luz_radial(1560, 600, 700, (0.9, 0.9, 0.9), k=0.9 * clamp01((t - self.t_firma + 0.5) / 0.4))
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=400, y1=1080), bloom=0.55)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        dur = max(1.5, self.t_pidieron - self.t_semana)
        for k in range(7):
            self.ev(self.t_semana - 0.2 + k * dur / 7.0, "tachon", 0.7, -0.6 + 0.2 * k)
        self.ev(self.t0, "reloj_pared", 0.5, 0.0, dur=self.t_quince - self.t0)
        self.ev(self.t_quince - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        d2 = max(2.0, self.t_hk + 1.2 - self.t_quince)
        for q in range(15):
            self.ev(self.t_quince + q * d2 / 16.0, "sobre_desliza", 0.5, -0.5, dur=0.6)
            self.ev(self.t_quince + q * d2 / 16.0 + 0.75, "caja_registradora" if q % 5 == 4 else "ficha", 0.55, 0.5)
        self.ev(self.t_cinco, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_dosc - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_dosc, "fichas_mezcla", 0.7, 0.0, dur=max(1.2, self.t_mas - self.t_dosc - 0.5))
        self.ev(self.t_mas, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_mas, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_pistola - 0.35, "barrido_aire", 0.6, -0.3, dur=0.7)
        for k, tk in enumerate((self.t_pistola, self.t_pasa, self.t_forzar)):
            self.ev(tk - 0.2, "fotos", 0.7, -0.5 + 0.5 * k)
            self.ev(tk + 0.25, "tachon", 0.9, -0.5 + 0.5 * k)
        self.ev(self.t_botin - 0.2, "puerta", 0.9, 0.0)
        self.ev(self.t_puerta, "pasos_mojados", 0.5, 0.0, dur=1.6)
        self.ev(self.t_firma, "pluma", 0.9, 0.5)
        self.ev(self.t_sello, "sello_golpe", 1.0, 0.5)
