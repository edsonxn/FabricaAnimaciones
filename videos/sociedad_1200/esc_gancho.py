# -*- coding: utf-8 -*-
"""Escena 1 «gancho»: RUEDA DE RECONOCIMIENTO tras el espejo (mil doscientos sospechosos idénticos callan; a «la orden» giran la
cabeza a la vez) · el ORGANIGRAMA de corcho: la linterna sube la pirámide hasta la cima vacía (sello «NADIE») · el BLOQUE DE
CELDAS: de una copia a cientos, con el reflector barriendo · DOS CELDAS VECINAS: les arrancan la red y les sellan el pasaplatos ·
CINCO DÍAS: caen las hojas del calendario y se encienden hilos de luz entre las celdas · EL ASALTO: siluetas bajo la lluvia hacia
la biblioteca, relámpago · EL PERIÓDICO «ERROR DE LABORATORIO» · el detective enciende un cigarro: «UN ENSAYO GENERAL»."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_1 as M
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, e_inout, smooth
from noir_pers import Busto
from toon import Pista, pulso, elipse_, tubo, bezier2


class Gancho(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = Busto(sem=11)
        self.copias = [RP.Copia(sem=100 + i * 7, num=f"{(417 + i * 61) % 1200:04d}") for i in range(14)]
        self.t_mil = w("mil doscientos")
        self.t_sosp = w("sospechosos")
        self.t_callan = w("callan")
        self.t_orden = w("orden")
        self.t_busque = w("busqué")
        self.t_no = w("No lo")
        self.t_eran = w("Eran")
        self.t_celda = w("celda")
        self.t_inter = w("internet")
        self.t_perm = w("permiso")
        self.t_cinco = w("cinco")
        self.t_encon = w("encontraron")
        self.t_organ = w("organizaron")
        self.t_asal = w("asaltaron")
        self.t_nada = w("nada que ver")
        self.t_prensa = w("prensa")
        self.t_error = w("error")
        self.t_yo = w("Yo le")
        self.t_ensayo = w("ensayo")
        self.tb = [t0, self.t_busque - 0.4, self.t_eran - 0.45, self.t_inter - 0.5, self.t_cinco - 0.4, self.t_asal - 0.5,
                   self.t_prensa - 0.4, self.t_yo - 0.35]
        tb = self.tb
        self.cam1 = Pista([(tb[0], (2350.0, 470.0, 1.28)), (tb[1] + 0.5, (520.0, 500.0, 1.06), "io")])
        self.cam2 = Pista([(tb[1], (960.0, 1050.0, 0.62)), (self.t_no - 0.1, (960.0, -1180.0, 1.25), "io"), (tb[2] + 0.6, (960.0, -1210.0, 1.4))])
        self.cam3 = Pista([(tb[2], (960.0, -60.0, 2.6)), (tb[2] + 1.4, (960.0, -60.0, 2.3), "io"), (tb[3] + 0.5, (960.0, -260.0, 0.58), "io")])
        self.cam4 = Pista([(tb[3], (960.0, 470.0, 1.0)), (tb[4] + 0.5, (960.0, 440.0, 1.12), "io")])
        self.plano(tb[0], self.p_rueda, pal="sodio")
        self.plano(tb[1], self.p_organigrama, tr="barrido", dur=0.55, dirx=1, pal="sodio")
        self.plano(tb[2], self.p_bloque, tr="tinta", dur=0.6)
        self.plano(tb[3], self.p_celdas, tr="empuje", dur=0.5, centro=(W * 0.5, H * 0.45))
        self.plano(tb[4], self.p_dias, tr="barrido", dur=0.5, dirx=-1)
        self.plano(tb[5], self.p_asalto, tr="relampago", dur=0.5, pal="sodio")
        self.plano(tb[6], self.p_periodico, tr="barrido", dur=0.5, dirx=1, pal="bourbon")
        self.plano(tb[7], self.p_detective, tr="humo", dur=0.6, pal="sodio")

    # ------------------------------------------------------------------ 1. la rueda de reconocimiento
    def p_rueda(self, h, t, u):
        cx, cy, z = self.cam1(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.rueda(), h, 1.0, rampa="piedra")
        gira = smooth(clamp01((t - self.t_orden) / 0.25))
        for i, c in enumerate(self.copias):
            x = -800 + i * 290
            if abs(x - cx) > 1500 / z:
                continue
            mira = (0.9 if i % 3 else -0.8) * (1 - gira) + 0.0 * gira
            expr = "linea" if t > self.t_callan + i * 0.03 else "neutro"
            m = c.frente(h, dict(x=x, y=M.Y_SUELO, s=0.95, luz=(0.0, -1.0), bal=2 * math.sin(t * 0.8 + i),
                                 manos=[(-58, -300), (58, -300)], cara=dict(expr=expr, mira=mira, parpadea=gira < 0.5)))
            # la placa con su número delante del pecho
            yp = (m[0][1] + m[1][1]) / 2 - 6
            h.pieza(C.rect(x - 84, yp - 34, 168, 68), 30, 900 + i, w=3, luz=(0, -1), d=4, sombra=0.3, trama=0, rim=0.4, rampa="piedra")
            N.texto_maquina(h, c.num, x, yp, 40, t, -99, cps=1e9, tono=0.92, centro=True, fuente=C.IMPACT, encuadrar=False)
        # el espejo: el detective de espaldas en primer plano (silueta) y el reflejo del vidrio
        with h.capa(0.0):                                             # en pantalla: no se mueve con el travelling
            p = dict(x=250, y=860, s=1.3, d=1, luz=(0.4, -0.6), rim=0.7, cigarro=True, brasa=0.3 + 0.3 * math.sin(t * 1.3))
            self.busto.dibujar(h, p)
            tip = self.busto.punta(p)
            N.humo(h, t, tip[0], tip[1], k=0.8, sem=3)
        C.ambiente(h, 0.42)
        for k, x in enumerate(np.arange(-1000, 3100, 300)):
            if abs(x + 80 - cx) < 1500 / z:
                h.luz_cono(x + 80, -470, math.pi / 2, 0.42, 1500, h.pal["sodio"], k=1.15, suave=0.6)
        C.banda(h, "1 200 SOSPECHOSOS", 1280, 150, 72, t, self.t_sosp, sem=5)
        img = h.acabado(t, niebla=dict(dens=0.10, sem=2, vel=6), bloom=0.5)
        # reflejo del cristal del espejo (una franja diagonal clara que se desliza)
        g = ((np.arange(W)[None, :] + np.arange(H)[:, None] * 0.6 - 900 + 180 * math.sin(t * 0.3)) / 260.0)
        img += (np.clip(1 - np.abs(g), 0, 1) ** 2 * 0.05)[..., None]
        return img

    # ------------------------------------------------------------------ 2. el organigrama sin cabeza
    def p_organigrama(self, h, t, u):
        cx, cy, z = self.cam2(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.organigrama(), h, 1.0, rampa="papel")
        y_top = -1380
        if t >= self.t_no + 0.15:
            N.sello(h, "NADIE", 960, y_top + 40, 70, t, self.t_no + 0.15, rot=-10, tono=np.array(h.pal["sello"]), alfa=0.95)
        C.ambiente(h, 0.16)
        ly = cy + 60 * math.sin(t * 1.7)
        lx = 960 + 160 * math.sin(t * 1.1)
        h.luz_radial(lx, ly, 420 / max(0.6, z) + 120, h.pal["lampara"], k=1.6)
        h.luz_radial(960, ly + 200, 900, h.pal["sodio"], k=0.25)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ 3. el bloque de celdas
    def p_bloque(self, h, t, u):
        cx, cy, z = self.cam3(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.bloque(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"])
        # la copia de la celda enfocada y sus vecinas, vivas (encima de lo pintado)
        for dc in (-1, 0, 1):
            for dp in (-1, 0, 1):
                x = 960 + dc * 270
                ytop = -1340 + (3 + dp) * 370
                if abs(x - cx) * z > 1400 or abs(ytop - cy) * z > 900:
                    continue
                i = (dc + 1) * 3 + dp + 1
                cop = self.copias[i]
                gesto = (i * 7) % 3
                manos = [(-70, -420), (70, -420)] if gesto == 0 else ([(-40, -300), (90, -560)] if gesto == 1 else None)
                cop.frente(h, dict(x=x + 30 * math.sin(t * 0.4 + i), y=ytop + 318, s=0.42, luz=(0.0, -1.0), bal=3 * math.sin(t + i),
                                   manos=manos, cara=dict(expr="neutro" if gesto != 2 else "triste", mira=math.sin(t * 0.7 + i))))
                for k in range(8):                                    # los barrotes delante
                    bx = x - 110 + k * 31
                    h.pieza(C.rect(bx, ytop, 7, 330), 26, 320 + k, w=1.5, d=0, sombra=0, trama=0, rim=0.6, rampa="piedra")
        C.ambiente(h, 0.55)
        for dc in (-1, 0, 1):                                         # cada copia ilumina su celda con la pantalla
            for dp in (-1, 0, 1):
                x = 960 + dc * 270
                ytop = -1340 + (3 + dp) * 370
                if abs(x - cx) * z < 1500 and abs(ytop - cy) * z < 1000:
                    h.luz_radial(x, ytop + 100, 230, h.pal["verde"], k=0.9)
        for piso in range(6):                                        # lámparas de las pasarelas
            yl = -1340 + piso * 370 + 360
            h.luz_radial(cx, yl, 1400, h.pal["lampara"], k=0.18)
        # el reflector de la torre barre las celdas
        a = math.pi * 0.25 + 0.35 * math.sin(t * 0.6)
        h.luz_cono(-1500, -1800, a, 0.07, 6000, h.pal["luna"], k=1.6, suave=0.5)
        h.luz_radial(960, 1200, 2500, h.pal["luna"], k=0.25)
        C.banda(h, "1 200 COPIAS · UNA POR CELDA", 960, 980, 52, t, self.t_celda - 0.1, sem=7)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.18, sem=3, vel=10), bloom=0.5)

    # ------------------------------------------------------------------ 4. dos celdas vecinas, incomunicadas
    def p_celdas(self, h, t, u):
        cx, cy, z = self.cam4(t)
        dx, dy = C.temblor(t, [(self.t_perm + 0.15, 10)])
        h.camara(z, cx + dx, cy + dy, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.celdas_par(), h, 1.0, rampa="piedra")
        fuera = smooth(clamp01((t - self.t_inter) / 0.3))
        # el toma de red en el muro (lado izquierdo) y su cable que arrancan hacia arriba
        P.enchufe(h, 840, 420, 0.42, fuera=fuera, ang=-math.pi / 2, sem=50, cable_a=(560, -260))
        if fuera > 0:
            C.chispas(h, t, 820, 420, self.t_inter + 0.05, n=18, vel=380, sem=5, ang=math.pi)
        # el pasaplatos del muro: una plancha baja y lo sella
        cae = e_out(clamp01((t - self.t_perm) / 0.18))
        h.pieza(C.rect(895, 520, 130, 90), 8, 60, w=3, d=0, sombra=0, trama=0, rim=0, rampa="piedra")
        h.pieza(C.rect(886, 420 + 100 * cae, 148, 100), 70, 61, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.8, rampa="piedra")
        if cae > 0.9:
            for k in range(4):
                h.pieza(elipse_(900 + k * 40, 600, 7, 7, n=8), 140, 62 + k, w=2, d=2, trama=0, rim=0.8, rampa="laton")
        C.polvo_cae(h, t, 880, 1040, 520, self.t_perm + 0.15, dur=1.5, n=50, sem=4)
        # las dos copias, una a cada lado, con la mano en la pared
        toca = 0.5 + 0.5 * math.sin(t * 2.2)
        ca = dict(expr="texto", texto=["SIN RED"], t0=self.t_inter + 0.3, cps=14) if t > self.t_inter + 0.3 else dict(expr="neutro", mira=0.9)
        RP.Copia(sem=3, num="0417").perfil(h, dict(x=600, y=M.Y_SUELO, s=0.9, d=1, mano=(250, -470 + 10 * toca), cara=ca, inclina=0.08))
        cb = dict(expr="miedo") if t > self.t_perm + 0.2 else dict(expr="neutro", mira=0.9)
        RP.Copia(sem=9, num="0418").perfil(h, dict(x=1330, y=M.Y_SUELO, s=0.9, d=-1, mano=(260, -440 - 8 * toca), cara=cb, inclina=0.06))
        C.ambiente(h, 0.30)
        h.luz_radial(390, -80, 700, h.pal["luna"], k=1.0)
        h.luz_radial(1720, -80, 700, h.pal["luna"], k=1.0)
        h.luz_radial(960, 300, 900, h.pal["lampara"], k=0.35)
        C.banda(h, "SIN INTERNET", 420, 980, 50, t, self.t_inter + 0.1, sem=8)
        C.banda(h, "SIN PERMISO PARA HABLARSE", 1380, 980, 50, t, self.t_perm + 0.1, claro=True, sem=9)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.08, sem=4), bloom=0.4)

    # ------------------------------------------------------------------ 5. cinco días: se encuentran
    def p_dias(self, h, t, u):
        z = 0.72 + 0.04 * u
        h.camara(z, 1100 + 30 * u, -200, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.bloque(), h, 0.8, rampa="piedra", emis=1.0, col_emis=h.pal["verde"], bruma=0.25)
        # hilos de luz entre celdas: cada vez más (se encontraron y se organizaron)
        rng = np.random.default_rng(5)
        n = int(4 + 46 * smooth(clamp01((t - self.t_cinco) / (self.t_asal - self.t_cinco))))
        with h.capa(0.8):
            for k in range(n):
                p1 = rng.integers(-5, 13), rng.integers(0, 6)
                p2 = rng.integers(-5, 13), rng.integers(0, 6)
                a = np.array([960 + p1[0] * 270, -1340 + p1[1] * 370 + 140], float)
                b = np.array([960 + p2[0] * 270, -1340 + p2[1] * 370 + 140], float)
                mid = (a + b) / 2 + np.array([0, -160 - 40 * (k % 4)])
                tk = self.t_cinco + k * 0.07
                f = clamp01((t - tk) / 0.5)
                if f <= 0:
                    continue
                Q = bezier2(a, mid, b, 22)[: max(2, int(22 * f))]
                h.emitir(tubo(Q, 9, 9), 0.7 * (0.6 + 0.4 * math.sin(t * 6 + k)), col=h.pal["verde"], blur=3)
                h.resplandor(Q[-1][0], Q[-1][1], 90, 0.35 * f, col=h.pal["verde"])
                if f >= 1:
                    h.resplandor(a[0], a[1], 70, 0.25, col=h.pal["verde"])
        # el calendario en primer plano: cinco hojas que caen
        with h.capa(0.0):
            dias = ["7", "8", "9", "10", "11"]
            span = max(0.5, (self.t_asal - 0.6 - self.t_cinco) / 5)
            for i, d in enumerate(dias):
                tt = self.t_cinco - 0.2 + i * span
                if t >= tt - 0.3 and (i == len(dias) - 1 or t < tt + span + 0.4):
                    K.calendario(h, t, tt, "JULIO", d, "2026", cx=330, cy=560, s=0.68, sem=70 + i, ang=-0.05 + 0.03 * i)
        C.ambiente(h, 0.45)
        h.luz_radial(330, 400, 600, h.pal["lampara"], k=0.9)
        h.luz_radial(1500, -600, 2600, h.pal["luna"], k=0.3)
        C.banda(h, "SE ENCONTRARON", 1300, 820, 54, t, self.t_encon, sem=10)
        C.banda(h, "SE ORGANIZARON", 1300, 920, 54, t, self.t_organ, claro=True, sem=11)
        return h.acabado(t, niebla=dict(dens=0.15, sem=5), bloom=0.6)

    # ------------------------------------------------------------------ 6. el asalto (visión)
    def p_asalto(self, h, t, u):
        k = smooth(clamp01(u / 4.5))
        dx, dy = C.temblor(t, [(self.t_asal, 8)])
        h.camara(1.05 + 0.08 * k, 960 + dx, 520 + dy, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.calle_biblioteca(), h, 1.0, rampa="ladrillo", emis=1.0)
        y0 = 1000
        for i in range(16):                                           # las copias cruzan hacia la biblioteca
            fila = i % 3
            s = 0.5 + 0.18 * fila
            dist = (t - self.tb[5]) * (150 + 30 * fila) + i * 230
            x = -300 + (dist % 2400)
            RP.copia_mini(h, x, y0 + fila * 50, s, t, sem=200 + i, d=1, andar=1.0, dist=dist, tono=40)
        C.ambiente(h, 0.75)
        for x in (200, 1720):
            h.luz_cono(x, 640, math.pi / 2, 0.6, 700, h.pal["sodio"], k=1.2, suave=0.6)
        h.luz_radial(960, 380, 900, h.pal["lampara"], k=0.6)
        C.reflejar(h, t, 1010)
        N.lluvia(h, t, n=520)
        N.salpicaduras(h, t, 900, H, n=40)
        C.banda(h, "UNA EMPRESA AJENA AL EXPERIMENTO", 960, 120, 48, t, self.t_nada, sem=12)
        return h.acabado(t, niebla=dict(dens=0.22, sem=6), flash=0.8 * N.relampago(t, [self.t_asal - 0.05]), bloom=0.6)

    # ------------------------------------------------------------------ 7. el periódico
    def p_periodico(self, h, t, u):
        k = smooth(clamp01(u / 4.0))
        h.camara(1.0 + 0.10 * k, 960, 540, -0.03 + 0.03 * k)
        h.rim_color(h.pal["lampara"])
        NC.pegar(P_sup(), h, 1.0, rampa="madera")
        P.vaso(h, 1650, 300, 0.9, sem=5, nivel=0.4, t=t)
        P.periodico(h, t, self.t_prensa - 0.1, 940, 560, 1.15, "ERROR DE LABORATORIO", "Agentes de IA «se salen del guion» en una prueba",
                    sem=21, fecha="JULIO 2026")
        C.ambiente(h, 0.3)
        h.luz_radial(900, 400, 1300, h.pal["lampara"], k=1.25)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, bloom=0.4)

    # ------------------------------------------------------------------ 8. el detective
    def p_detective(self, h, t, u):
        k = smooth(clamp01(u / 5.5))
        h.camara(1.02 + 0.08 * k, 920 + 40 * k, 540, -0.006)
        h.rim_color(h.pal["neon"])
        NC.pegar(M.oficina_det(), h, 0.6, rampa="madera", emis=0.9)
        fn = C.parpadeo(t, [(self.t_ensayo + 0.6, 0.3)], sem=2)
        br = pulso(t, self.tb[7] + 0.5, 1.6, 1.0) + 0.25
        mano = clamp01((t - self.tb[7] - 2.0) / 0.6) * (1 - clamp01((t - self.t_ensayo - 0.4) / 0.6))
        p = dict(x=600, y=520, s=1.05, d=1, luz=(0.9, -0.5), rim=0.95, cigarro=True, brasa=br, mano=mano,
                 arriba=0.25 + 0.3 * smooth(clamp01((t - self.t_ensayo) / 0.6)))
        with h.capa(1.0):
            self.busto.dibujar(h, p)
            tip = self.busto.punta(p)
            C.brasa(h, tip, br)
        C.ambiente(h, 0.28)
        h.luz_persiana([(200, 30), (1300, 120), (1300, 950), (100, 1100)], k=1.0, n=17, abierto=0.5, col=np.array(h.pal["sodio"]) * 0.7)
        h.luz_radial(1700, 380, 1200, h.pal["neon"], k=0.55 * fn)
        N.humo(h, t, tip[0], tip[1], k=0.9, sem=4)
        N.gotas_vidrio(h, t, (1100, 0, 1920, 760), n=50, k=0.6)
        C.banda(h, "UN ENSAYO GENERAL", 1340, 880, 70, t, self.t_ensayo, acento=True, sem=13)
        return h.acabado(t, niebla=dict(dens=0.10, sem=7, vel=12), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0], "focos", 0.7, 0.0)
        self.ev(tb[0] + 0.2, "zumbido_foco", 0.25, 0.0, dur=tb[1] - tb[0])
        self.ev(self.t_callan, "silencio_tono", 0.35, 0.0, dur=2.0)
        self.ev(self.t_orden, "servo", 0.6, 0.0)
        self.ev(tb[1] + 0.1, "linterna_click", 0.6, -0.2)
        self.ev(self.t_no + 0.15, "sello_golpe", 0.85, 0.0)
        self.ev(tb[2], "zumbido_servidores", 0.25, 0.0, dur=tb[3] - tb[2])
        self.ev(tb[2] + 0.2, "grave_inquietante", 0.45, 0.0, dur=4.0)
        self.ev(self.t_inter, "desenchufa", 0.8, -0.3)
        self.ev(self.t_inter + 0.05, "chisporroteo", 0.5, -0.3)
        self.ev(self.t_perm + 0.12, "golpe_grave", 0.85, 0.1)
        self.ev(tb[4] + 0.1, "paginas", 0.5, -0.4, dur=2.5)
        self.ev(self.t_encon, "electricidad", 0.45, 0.3, dur=2.5)
        self.ev(tb[5], "lluvia_amb", 0.6, 0.0, dur=tb[6] - tb[5] + 0.4)
        self.ev(self.t_asal - 0.05, "trueno_noir", 0.75, 0.0, dur=4.0)
        self.ev(tb[5] + 0.3, "pasos_mojados", 0.45, 0.2, dur=3.0)
        self.ev(self.t_prensa - 0.1, "periodico_gira", 0.7, 0.0)
        self.ev(self.t_prensa + 0.75, "periodico_golpe", 0.7, 0.0)
        self.ev(tb[7] + 0.3, "cerilla", 0.6, -0.2)
        self.ev(tb[7] + 0.9, "calada", 0.5, -0.2)
        self.ev(self.t_ensayo - 0.2, "exhala", 0.45, -0.2)
        self.ev(self.t_ensayo + 0.6, "lampara_chisporrotea", 0.3, 0.5)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.5, 0.0, dur=0.9)


def P_sup():
    import mundos_base as B
    return B.superficie("madera", 3)
