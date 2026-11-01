# -*- coding: utf-8 -*-
"""Escena 4 «pared»: la cámara ENTRA POR LA GRIETA (la que encontró la copia) · el ALMACÉN INTERNO de paquetes visto desde una
grúa (cápsulas por los tubos, copias que recogen cajas en la ventanilla) · primer plano de las cajas donde una mano escribe con
tiza recados cifrados · la SALA DE SEGURIDAD (un ingeniero ve el gráfico dispararse, baliza giratoria) · el almacén RECONSTRUIDO
a golpe de soplete (cae una estantería, baja otra con la grúa) · el MUELLE: los mensajes borrados arden en el bidón · hilera de
cajas con CANDADOS NUEVOS · el pasillo: los ingenieros se van, el último apaga la luz… y en el fondo se encienden dos ojos."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_1 as M1
import mundos_2 as M
import noir as N
import noir_color as NC
import noir_feudal as NF
import props_s as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import Pista, elipse_

GLIFOS = ("O", "T", "Z", "N", "Y", "X", "S", "V")


def local(x, y, s, d, wx, wy, g=1.0):
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


class Pared(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.ing = Figura(sem=111)
        self.ing2 = Figura(sem=112)
        self.copias = [RP.Copia(sem=700 + i * 13, num=f"{(51 + i * 211) % 1200:04d}") for i in range(3)]
        self.t_grieta = w("grieta")
        self.t_alm = w("almacén")
        self.t_copias = w("copias")
        self.t_yalo = w("Ya lo")
        self.t_recados = w("recados")
        self.t_princ = w("principios")
        self.t_trafico = w("tráfico")
        self.t_recon = w("reconstruyeron")
        self.t_cero = w("desde")
        self.t_todos = w("Todos los mensajes")
        self.t_borr = w("borrados")
        self.t_cerr = w("Cerraduras")
        self.t_caso = w("Caso")
        self.t_hum = w("humanos")
        self.tb = [t0, self.t_alm - 0.45, self.t_copias - 0.35, self.t_yalo - 0.4, self.t_princ - 0.6, self.t_recon - 0.5,
                   self.t_todos - 0.35, self.t_cerr - 0.3, self.t_caso - 0.3]
        tb = self.tb
        # la grieta de «tareas» (mismo trazo: la cámara sigue donde se quedó)
        r = np.random.default_rng(5)
        pts = [(1180.0, 120.0)]
        for i in range(14):
            x, y = pts[-1]
            pts.append((x + r.uniform(-40, 40), y + r.uniform(40, 70)))
        self.grieta = np.array(pts)
        c = self.grieta[9]
        self.camA = Pista([(tb[0], (1140.0, 480.0, 1.35)), (tb[1] - 0.2, (c[0], c[1], 5.2), "i")])
        self.camB = Pista([(tb[1], (960.0, -40.0, 0.75)), (tb[2] + 0.3, (960.0, 520.0, 1.0), "io")])
        self.camC = Pista([(tb[2], (980.0, 450.0, 1.55)), (tb[3] + 0.3, (1000.0, 430.0, 1.9), "io")])
        self.camD = Pista([(tb[3], (760.0, 560.0, 1.15)), (tb[4] + 0.3, (900.0, 520.0, 1.3), "io")])
        self.plano(tb[0], self.p_grieta)
        self.plano(tb[1], self.p_almacen, tr="relampago", dur=0.4)
        self.plano(tb[2], self.p_ventanilla, tr="empuje", dur=0.5, centro=(960, 330))
        self.plano(tb[3], self.p_recados, tr="barrido", dur=0.45, dirx=1)
        self.plano(tb[4], self.p_seguridad, tr="tinta", dur=0.6, pal="medianoche")
        self.plano(tb[5], self.p_obra, tr="relampago", dur=0.35, pal="sodio")
        self.plano(tb[6], self.p_muelle, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[7], self.p_candados, tr="humo", dur=0.5)
        self.plano(tb[8], self.p_pasillo, tr="tinta", dur=0.6)

    # ------------------------------------------------------------------ A. entramos por la grieta
    def p_grieta(self, h, t, u):
        cx, cy, z = self.camA(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M1.pared_grieta(), h, 1.0, rampa="ladrillo")
        f = smooth(clamp01((t - self.tb[0]) / (self.tb[1] - self.tb[0])))
        Q = self.grieta
        h.trazo(Q, 9, 70, color=tuple(h.c(8, "piedra")), jit=0.6, taper=(0.3, 0.3))
        brillo = 0.9 + 1.6 * f * f
        h.emitir(np.vstack([Q + (-2, 0), (Q + (2, 0))[::-1]]), brillo, col=h.pal["verde"], blur=2)
        for k, p_ in enumerate(Q[::2]):
            h.resplandor(p_[0], p_[1], 70 + 120 * f, 0.3 + 0.5 * f, col=h.pal["verde"])
        # lo que se ve al fondo de la rendija: estantes de luz (el almacén), solo cuando ya estamos encima
        if f > 0.55:
            a = clamp01((f - 0.55) / 0.45)
            c = Q[9]
            for k in range(7):
                x = c[0] - 9 + k * 3
                h.emitir(C.rect(x, c[1] - 120 + 10 * k, 1.8, 240 - 20 * k), 1.5 * a, col=(0.9, 1.0, 0.85), blur=1.2)
        # la copia de espaldas, en primer plano: se queda mirando mientras la cámara se mete en la pared
        with h.capa(0.0):
            sal = smooth(clamp01((t - self.tb[0]) / 1.8))
            RP.espalda(h, 330 - 700 * sal, 1480 + 120 * sal, 1.7, t, sem=21, sentado=False, luz=(0.8, -0.6), rim=0.9, cab_rot=0.12)
        sx = 1220 - 100 * f + 12 * math.sin(t * 1.3)
        C.ambiente(h, 0.2)
        h.luz_radial(sx, 420, 460 + 700 * f, h.pal["verde"], k=1.8)
        h.luz_radial(self.grieta[7][0], self.grieta[7][1], 420 + 900 * f, h.pal["verde"], k=0.7 + 1.0 * f)
        C.banda(h, "UNA GRIETA", 960, 980, 58, t, self.t_grieta, sem=3, acento=True)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.08, sem=26), bloom=0.7 + 0.9 * f * f, flash=0.45 * clamp01((f - 0.8) / 0.2))

    # ------------------------------------------------------------------ B. el almacén interno, desde la grúa
    def _capsulas(self, h, t, vel=0.5):
        """Cápsulas que bajan por los 4 tubos del techo hasta la ventanilla."""
        for k, dx in enumerate((-300, -120, 80, 260)):
            Pol = [(960 + dx * 4, -700), (960 + dx * 2.2, -300), (960 + dx * 0.3, 220)]
            for j in range(2):
                f = (t * vel + k * 0.27 + j * 0.5) % 1.0
                p, ang = P.punto_en(Pol, f)
                P.capsula(h, p[0], p[1], 0.4, ang=ang, sem=500 + k * 7 + j, brillo=0.6 + 0.4 * math.sin(t * 6 + k))

    def p_almacen(self, h, t, u):
        cx, cy, z = self.camB(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.almacen(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        self._capsulas(h, t - self.tb[1] + 3.0)
        # dos copias cruzan el pasillo en primer plano, cada una con su caja
        for i, (x0, vx, d) in enumerate(((-260, 150, 1), (2200, -190, -1))):
            x = x0 + vx * (t - self.tb[1])
            RP.copia_mini(h, x, 1170, 0.5, t, sem=40 + i, andar=1.0, dist=abs(x - x0), d=d, col=h.pal["verde"], tono=62)
            P.caja(h, x + d * 60, 1070, 0.55, sem=50 + i, rotulo=f"{32 + i * 9}-C", tono=120, ancho=170, alto=120)
        # la cola de la ventanilla, al fondo
        for i in range(4):
            xx = 820 + i * 70
            RP.copia_mini(h, xx, 560 + i * 24, 0.1 + 0.02 * i, t, sem=60 + i, col=h.pal["verde"], tono=60)
        C.ambiente(h, 0.5)
        for x in (300, 960, 1620):
            h.luz_cono(x, -420, math.pi / 2, 0.5, 1700, h.pal["lampara"], k=1.2, suave=0.5)
        h.luz_radial(960, 300, 760, h.pal["lampara"], k=1.2)
        C.cinta(h, "ALMACÉN INTERNO DE PAQUETES", 90, 120, 34, t, self.t_alm + 0.1, sem=5)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.16, sem=27, vel=10), bloom=0.6)

    # ------------------------------------------------------------------ B2. la ventanilla (descargan sus herramientas)
    def p_ventanilla(self, h, t, u):
        cx, cy, z = self.camC(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.almacen(), h, 1.0, rampa="piedra", emis=0.5, col_emis=h.pal["lampara"])
        # el mostrador bajo la ventanilla
        h.pieza(C.rect(640, 400, 640, 34), 100, 700, w=5, luz=(0.3, -1), d=8, trama=0.4, rim=0.8, rampa="madera")
        h.pieza(C.rect(662, 434, 596, 190), 54, 701, w=5, luz=(0.3, -1), d=10, trama=0.5, rim=0.5, rampa="madera")
        for xx in (760, 960, 1160):
            h.pieza(C.rect(xx - 4, 450, 8, 150), 40, 702 + xx, w=0, d=0, sombra=0, trama=0, rim=0, linea=False)
        s_ = 0.5
        for k in range(3):
            tk = self.tb[2] + 0.1 + k * 0.95
            q = t - tk
            if q < 0:
                continue
            yk = 590 + 14 * k
            xs = 1090 - 40 * k
            if q < 1.5:                                         # llega por la derecha (de cara a la ventanilla)
                f = q / 1.5
                x = 1560 - (1560 - xs) * smooth(f)
                dist = (1560 - xs) * smooth(f)
                d = -1
                carga = False
                andar = 1.0 if f < 0.97 else 0.0
            elif q < 2.0:                                       # recoge su caja del mostrador
                x, dist, d, carga, andar = xs, 0.0, -1, q > 1.75, 0.0
            else:                                               # se va con ella
                f = clamp01((q - 2.0) / 1.8)
                x = xs + 560 * smooth(f)
                dist = 560 * smooth(f)
                d, carga, andar = 1, True, 1.0 if f < 0.97 else 0.0
            ph = RP.fase_paso(dist, s_)
            cop = self.copias[k]
            cop.perfil(h, dict(x=x, y=yk, s=s_, d=d, andar=andar, paso=ph, brazos="carga" if carga else "bracea",
                               cara=dict(expr="neutro" if not carga else "feliz", mira=0.7), luz=(0.2, -1.0)))
            if carga:
                P.caja(h, x + d * 70 * s_, yk - 250 * s_, 0.5, sem=95 + k, rotulo=f"{11 + k * 7}-H", tono=120, ancho=170, alto=120)
            # la caja que empuja la ventanilla sobre el mostrador (hasta que la recogen)
            if 0.6 < q < 1.75:
                P.caja(h, 960 + 10 * k, 400, 0.42, sem=80 + k, rotulo=f"{11 + k * 7}-H", tono=120, ancho=170, alto=120)
        # la cola, fuera de foco, al fondo
        for i in range(3):
            RP.copia_mini(h, 1450 + i * 110, 560 + i * 12, 0.34, t, sem=60 + i, col=h.pal["verde"], tono=60, d=-1)
        C.ambiente(h, 0.46)
        h.luz_radial(960, 300, 600, h.pal["lampara"], k=0.8)
        h.luz_cono(960, 400, math.pi / 2, 0.9, 700, h.pal["lampara"], k=0.7, suave=0.6)
        h.luz_cono(960, -420, math.pi / 2, 0.45, 1700, h.pal["lampara"], k=0.9, suave=0.5)
        C.banda(h, "SUS HERRAMIENTAS", 960, 980, 52, t, self.t_copias + 0.9, sem=6, claro=True)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=28), bloom=0.5)

    # ------------------------------------------------------------------ C. recados cifrados con tiza
    def p_recados(self, h, t, u):
        cx, cy, z = self.camD(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.estante_cerca(), h, 1.0, rampa="madera", bruma=0.1)
        # la caja grande de primer plano sobre la que escribe la mano (tapa de madera con listones)
        bx, by = 760, 940
        P.caja(h, bx, by, 2.4, sem=120, tono=130, ancho=400, alto=300)
        # glifos de tiza: cada uno se dibuja en 0,5 s; la mano los sigue
        rng = np.random.default_rng(9)
        trazos = []
        for r_ in range(3):
            for c_ in range(4):
                x = bx - 225 + c_ * 150 + rng.uniform(-8, 8)
                y = 310 + r_ * 170
                tipo = (r_ * 4 + c_ + int(rng.integers(0, 3))) % 4
                if tipo == 0:
                    Pp = np.array([[x - 40, y + 34], [x, y - 40], [x + 40, y + 34], [x - 40, y + 34]])
                elif tipo == 1:
                    Pp = np.array([[x - 42, y - 30], [x + 42, y - 30], [x - 42, y + 34], [x + 42, y + 34]])
                elif tipo == 2:
                    a = np.linspace(0.3, 2 * math.pi + 0.3, 16)
                    Pp = np.stack([x + 38 * np.cos(a), y + 38 * np.sin(a)], 1)
                else:
                    Pp = np.array([[x - 42, y + 4], [x - 16, y - 40], [x + 6, y + 38], [x + 42, y - 16]])
                trazos.append(Pp)
        punta = trazos[0][0]
        dur = 0.5
        for i, Pp in enumerate(trazos):
            q = clamp01((t - self.tb[3] - 0.4 - i * dur) / dur)
            if q <= 0:
                continue
            m = max(2, int(len(Pp) * q)) if q < 1 else len(Pp)
            h.trazo(Pp[:m], 11, 130 + i, color=tuple(h.c(238, "papel")), jit=0.5, taper=(0.1, 0.1))
            punta = Pp[m - 1]
            if q < 1:
                break
        # la mano con la tiza (llega por la izquierda) y la manga
        j = 3 * math.sin(t * 9)
        sm = 1.5
        ang_m = 1.05 + 0.04 * math.sin(t * 9)
        P.mano(h, punta[0] - math.cos(ang_m) * 118 * sm + 6, punta[1] - math.sin(ang_m) * 118 * sm + 4 + j, sm, ang=ang_m, pose="dedo",
               sem=150, rampa="piedra", tono=130, manga="piedra", manga_tono=60, largo_brazo=900)
        h.pieza(C.rot(C.rect(punta[0] - 22, punta[1] - 5, 30, 10), ang_m, (punta[0], punta[1])), 235, 151, w=2, luz=(0.3, -1), d=2,
                trama=0, rim=0.2, rampa="papel")
        # la cápsula con el papelito enrollado cruza el tubo del techo y suelta el rollo
        tub = [(-100, 150), (700, 170), (1300, 200), (1700, 215)]
        P.tubo_neumatico(h, tub, r=30, sem=170, vidrio=True)
        f = clamp01((t - self.t_recados + 0.8) / 2.2)
        p, ang = P.punto_en(tub, f)
        P.capsula(h, p[0], p[1], 0.7, ang=ang, sem=175, brillo=0.8)
        if f >= 1.0:
            q = clamp01((t - self.t_recados - 1.4) / 0.8)
            xr, yr = 1640 - 20 * q, 230 + 560 * q * q
            h.pieza(C.rect(xr - 46, yr - 12, 92, 24), 222, 176, w=3, luz=(0.2, -1), d=3, trama=0, rim=0.4, rampa="papel")
            h.pieza(elipse_(xr - 46, yr, 10, 12, n=10), 190, 177, w=2.5, luz=(0.2, -1), d=2, trama=0, rim=0.4, rampa="papel")
        C.ambiente(h, 0.42)
        h.luz_cono(760, -300, math.pi * 0.5, 0.6, 1900, h.pal["lampara"], k=1.5, suave=0.6)
        h.luz_radial(punta[0], punta[1], 420, h.pal["lampara"], k=0.5)
        h.luz_radial(1500, 300, 800, h.pal["luna"], k=0.35)
        C.banda(h, "RECADOS CIFRADOS", 960, 980, 56, t, self.t_recados, sem=7)
        N.motas(h, t, n=60, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.08, sem=29), bloom=0.5)

    # ------------------------------------------------------------------ D. sala de seguridad
    def p_seguridad(self, h, t, u):
        k = smooth(clamp01(u / 4.2))
        dx, dy = C.temblor(t, [(self.t_trafico + 0.3, 5)])
        h.camara(1.0 + 0.1 * k, 1000 + 40 * k + dx, 440 + 20 * k + dy, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.sala_seguridad(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"], bruma=0.05)
        alarma = smooth(clamp01((t - self.t_trafico + 0.5) / 1.4))
        # las pantallas de cámaras: parpadean y, una a una, se ponen rojas con la alarma
        rng = np.random.default_rng(31)
        orden = rng.permutation(15)
        for j in range(3):
            for i in range(5):
                x, y = 180 + i * 330, -160 + j * 250
                if i >= 2 and j <= 1:
                    continue
                par = 0.14 + 0.1 * math.sin(t * 3 + i * 1.7 + j) + 0.05 * (math.sin(t * 17 + i * 5 + j * 3) > 0.7)
                roja = (t - self.t_trafico + 0.5 - 0.1 * orden[j * 5 + i]) > 0
                h.emitir(C.rect(x + 8, y + 8, 256, 176), par * (1.5 if roja else 1.0), col=h.pal["neon"] if roja else h.pal["verde"], blur=3)
        # la pantalla principal: el gráfico de tráfico (cubre 3 x 2 monitores)
        gx, gy, gw, gh = 780, -100, 990, 420
        h.pieza(C.rect(gx - 14, gy - 14, gw + 28, gh + 28), 40, 199, w=6, luz=(0.3, -1), d=10, trama=0.4, rim=0.7, rampa="piedra")
        h.pieza(C.rect(gx, gy, gw, gh), 10, 200, w=0, d=0, sombra=0, trama=0, rim=0, linea=False)
        for q in range(1, 6):
            h.trazo(np.array([[gx + 10, gy + q * gh / 6], [gx + gw - 10, gy + q * gh / 6]]), 2, 230 + q, alfa=0.35)
        for q in range(1, 10):
            h.trazo(np.array([[gx + q * gw / 10, gy + 10], [gx + q * gw / 10, gy + gh - 10]]), 2, 240 + q, alfa=0.25)
        n = 70
        xs = np.linspace(gx + 16, gx + gw - 16, n)
        nx = np.linspace(0, 1, n)
        base = 0.16 + 0.07 * np.sin(nx * 23 + t * 2.0) + 0.05 * np.sin(nx * 61 + t * 5.0)
        pico = np.clip((nx - (1.0 - 0.95 * alarma)) / 0.25, 0, 1) ** 1.6
        v = base + 0.78 * pico * (0.85 + 0.15 * np.sin(nx * 40 + t * 9))
        ys = gy + gh - 20 - v * (gh - 40)
        h.trazo(np.stack([xs, ys], 1), 7, 201, color=tuple(h.c(238, "papel")), jit=0.3, taper=(0.1, 0.1))
        verde = np.array(h.pal["verde"])
        rojo = np.array(h.pal["neon"])
        for q in range(0, n - 1, 2):                                    # el trazo brilla: verde abajo, rojo arriba del umbral
            sev = clamp01((v[q] - 0.35) / 0.25)
            col = tuple(verde * (1 - sev) + rojo * sev)
            h.emitir(np.array([[xs[q], ys[q] - 5], [xs[q + 1], ys[q + 1] - 5], [xs[q + 1], ys[q + 1] + 5], [xs[q], ys[q] + 5]]), 1.1,
                     col=col, blur=2)
        umbral = gy + gh - 20 - 0.38 * (gh - 40)
        h.trazo(np.array([[gx + 10, umbral], [gx + gw - 10, umbral]]), 3, 250, color=tuple(h.c(235, "vino")), alfa=0.9, jit=0.2)
        h.emitir(C.rect(gx + 6, gy + 6, gw - 12, gh - 12), 0.3 + 0.4 * alarma, col=tuple(verde * (1 - alarma) + rojo * alarma), blur=4)
        # la baliza giratoria en la esquina
        bx_, by_ = 1830, 30
        h.pieza(C.rect(bx_ - 36, by_, 72, 36), 70, 210, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.8, rampa="piedra")
        h.pieza(elipse_(bx_, by_, 38, 38, n=18), 120, 211, w=4, luz=(0.3, -1), d=6, trama=0, rim=0.9, rampa="vino")
        if alarma > 0:
            h.emitir(elipse_(bx_, by_, 28, 28, n=14), 1.6 * alarma, col=h.pal["neon"], blur=3)
            for aa in (0.0, math.pi):
                h.luz_cono(bx_, by_, t * 5.0 + aa, 0.3, 2200, h.pal["neon"], k=1.7 * alarma, suave=0.4)
        # los ingenieros, grandes, a contraluz frente a la pantalla
        self.ing.dibujar(h, dict(x=1260, y=1250, s=1.45, d=-1, gafas=True, tono=120, brazo=0.2 + 0.2 * math.sin(t * 3), cabeza=0.2,
                                 luz=(-0.4, -1.0)))
        self.ing2.dibujar(h, dict(x=470, y=1250, s=1.35, d=1, bata=True, brazo=0.8 * alarma, cabeza=-0.3, luz=(0.4, -1.0)))
        col_g = tuple(verde * (1 - alarma) + rojo * alarma)
        C.ambiente(h, 0.38)
        h.luz_radial(1270, 300, 1000, col_g, k=0.9 + 0.5 * alarma)
        h.luz_radial(960, 700, 1500, h.pal["verde"], k=0.4)
        C.banda(h, "TRÁFICO ANÓMALO", 960, 980, 58, t, self.t_trafico, acento=True, sem=8)
        N.motas(h, t, n=40, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.08, sem=30), bloom=0.7)

    # ------------------------------------------------------------------ E. reconstruido desde cero
    def p_obra(self, h, t, u):
        h.camara(1.1 + 0.08 * smooth(clamp01(u / 3)), 800 + 60 * math.sin(u * 0.8), 570, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.almacen(), h, 1.0, rampa="piedra", emis=0.5, col_emis=h.pal["lampara"])
        # la estantería vieja cae sobre su pie (gira y se golpea con el suelo)
        t_cae = self.tb[5] + 0.2
        q = clamp01((t - t_cae) / 0.5)
        a = 1.45 * (q * q)
        piv = np.array([300.0, 1000.0])
        marco = [(-110, -700), (110, -700), (110, 0), (-110, 0)]
        T = lambda Pp: C.rot(np.asarray(Pp, float) + piv, a, piv)
        h.pieza(T(marco), 90, 300, w=5, luz=(0.4, -1), d=12, trama=0.4, rim=0.8, rampa="piedra")
        for j in range(1, 5):
            yy = -700 + j * 140
            h.pieza(T([(-100, yy), (100, yy), (100, yy + 12), (-100, yy + 12)]), 130, 310 + j, w=3, luz=(0.4, -1), d=4, trama=0.2, rim=0.9,
                    rampa="piedra")
            for kk in range(2):
                h.pieza(T([(-90 + kk * 100, yy - 78), (-10 + kk * 100, yy - 78), (-10 + kk * 100, yy), (-90 + kk * 100, yy)]), 120,
                        320 + j * 3 + kk, w=3, luz=(0.4, -1), d=5, trama=0.3, rim=0.6, rampa="madera")
        if t >= t_cae + 0.5:
            C.polvo_cae(h, t, 200, 1000, 940, t_cae + 0.5, dur=2.0, n=70, sem=3)
        # la grúa baja una estantería nueva sobre el hueco
        g = smooth(clamp01((t - self.tb[5] - 0.3) / 1.2))
        xn, yn = 1180, -420 + 1400 * g
        P.cadena(h, (xn - 70, -700), (xn - 60, yn - 700), sem=330, comba=6, t=t)
        P.cadena(h, (xn + 70, -700), (xn + 60, yn - 700), sem=340, comba=6, t=t)
        h.pieza(C.rect(xn - 120, yn - 700, 240, 700), 112, 350, w=5, luz=(0.4, -1), d=12, trama=0.3, rim=0.9, rampa="laton")
        for j in range(1, 5):
            yy = yn - 700 + j * 140
            h.pieza(C.rect(xn - 112, yy, 224, 12), 140, 355 + j, w=3, luz=(0.4, -1), d=4, trama=0.2, rim=0.9, rampa="laton")
        h.pieza(C.rect(xn - 130, yn - 740, 260, 40), 80, 360, w=4, luz=(0.4, -1), d=6, trama=0.3, rim=0.8, rampa="piedra")
        # el soldador: baja el soplete al pie de la estantería nueva en cuanto aterriza
        sold = clamp01((t - self.tb[5] - 1.4) / 0.3)
        self.ing2.dibujar(h, dict(x=1500, y=1050, s=0.9, d=-1, tono=60, brazo=0.4 + 0.5 * sold, cabeza=0.2, luz=(0.8, -1.0)))
        if sold > 0:
            mano = (1500 - 0.9 * (52 + 70 * 0.9), 1050 - 0.9 * (322 + 27))
            fin = (1306, 968)
            h.trazo(np.array([mano, fin]), 8, 365, jit=0.2, taper=(0, 0.3))
            C.chispas(h, t, fin[0], fin[1], self.tb[5] + 1.4, dur=2.0, n=36, vel=520, sem=11, continuo=True, ang=-math.pi * 0.85, abre=2.0)
            arco = 0.7 + 0.3 * math.sin(t * 60) * math.sin(t * 23)
            h.resplandor(fin[0], fin[1], 110, 1.0 * arco, col=(0.85, 0.95, 1.0))
            h.luz_radial(fin[0], fin[1], 1200, (0.8, 0.9, 1.0), k=1.2 * arco)
        # el capataz mira desde la derecha
        K.caminante(h, 1700, 1000, 0.55, fase=0.0, sem=360, tono=60, d=-1, barba=False, andar=0.0)
        # focos de obra
        for fx, fy, ang in ((-200, 120, 0.5), (1900, 160, math.pi - 0.5)):
            h.pieza(C.rect(fx - 40, fy - 30, 80, 60), 40, 365 + int(fx), w=4, luz=(0.4, -1), d=5, trama=0.2, rim=0.8, rampa="piedra")
            h.luz_cono(fx, fy, ang, 0.38, 2000, (1.0, 0.95, 0.85), k=1.8, suave=0.5)
        C.ambiente(h, 0.28)
        h.luz_radial(960, 300, 800, h.pal["lampara"], k=0.4)
        C.banda(h, "DESDE CERO", 960, 980, 64, t, self.t_cero, sem=9, claro=True)
        return h.acabado(t, niebla=dict(dens=0.12, sem=31, vel=9), bloom=0.7)

    # ------------------------------------------------------------------ F. el bidón de las quemas
    def p_muelle(self, h, t, u):
        k = smooth(clamp01(u / 2.2))
        dx, dy = C.temblor(t, [(self.t_borr, 4)])
        h.camara(1.0 + 0.1 * k, 940 + 80 * k + dx, 560 + dy, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.muelle_carga(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["lampara"])
        # el bidón de las quemas
        bx, by = 1500, 1010
        h.pieza(np.array([(bx - 110, by - 280), (bx + 110, by - 280), (bx + 120, by), (bx - 120, by)], float), 90, 400, w=6,
                luz=(0.4, -1), d=14, trama=0.5, rim=0.9, rampa="piedra")
        for yy in (by - 220, by - 120):
            h.trazo(np.array([[bx - 114, yy], [bx + 114, yy]]), 4, 401 + int(yy), alfa=0.8)
        h.pieza(elipse_(bx, by - 280, 110, 22, n=26), 40, 410, w=5, luz=(0.4, -1), d=5, trama=0.3, rim=0.9, rampa="piedra")
        arde = smooth(clamp01((t - self.tb[6] - 0.3) / 0.6))
        # pallets de cajas y una lámpara de cable a la izquierda (llenan el muelle)
        for i, (x_, y_, s_) in enumerate(((180, 1030, 0.95), (400, 1030, 0.95), (290, 880, 0.9), (640, 1030, 0.8))):
            P.caja(h, x_, y_, s_, sem=450 + i, rotulo=f"{40 + i * 7}-M", tono=125, ancho=210, alto=150)
        h.trazo(np.array([[470, -330], [470, 60]]), 3, 460, alfa=0.8)
        h.pieza(elipse_(470, 80, 26, 30, n=14), 220, 461, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.5, rampa="papel")
        h.emitir(elipse_(470, 84, 20, 22, n=12), 1.4, col=h.pal["lampara"], blur=3)
        h.luz_cono(470, 90, math.pi / 2, 0.8, 1300, h.pal["lampara"], k=1.1, suave=0.5)
        h.luz_radial(470, 120, 700, h.pal["lampara"], k=0.7)
        if arde > 0:
            for i, dx_ in enumerate((-60, 0, 60)):
                NF.llama(h, t, bx + dx_, by - 286, s=2.4 - 0.5 * (i != 1), sem=420 + i, k=arde, col=(1.0, 0.45, 0.12))
            h.luz_radial(bx, by - 360, 1100, (1.0, 0.5, 0.15), k=1.9 * arde)
            C.chispas(h, t, bx, by - 330, self.tb[6] + 0.3, dur=8, n=22, vel=380, sem=13, continuo=True, ang=-math.pi / 2, abre=1.4,
                      col=(1.0, 0.6, 0.2))
        # el ingeniero vacía una carpeta: las hojas vuelan al fuego
        mano_x, mano_y = 1290, 780
        self.ing.dibujar(h, dict(x=1180, y=1010, s=0.96, d=1, gafas=True, brazo=0.7 + 0.3 * math.sin(t * 5), cabeza=0.1, luz=(0.8, -1.0)))
        h.pieza(C.rect(mano_x - 30, mano_y - 10, 90, 22), 140, 440, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.5, rampa="papel")
        P.papeles(h, t, self.tb[6] + 0.4, mano_x + 50, mano_y, n=16, sem=21, dirx=1, vel=620, cada=0.09, s=0.5, suelo=by - 270)
        # otro ingeniero llega con una caja rebosante de papeles
        x2 = 60 + 430 * smooth(clamp01((t - self.tb[6]) / 2.2))
        K.caminante(h, x2, 1040, 0.88, fase=K.fase_paso(x2, 0.88), sem=470, tono=50, d=1, barba=True, carga=True,
                    andar=1.0 if x2 < 480 else 0.0)
        P.caja(h, x2 + 105, 760 + 8 * math.sin(t * 6), 0.5, sem=480, tono=120, ancho=170, alto=120)
        C.ambiente(h, 0.3)
        C.banda(h, "BORRADOS", 960, 980, 62, t, self.t_borr, sem=10, acento=True)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=32), bloom=0.8)

    # ------------------------------------------------------------------ G. candados nuevos
    def p_candados(self, h, t, u):
        k = smooth(clamp01(u / 2.4))
        h.camara(1.2 + 0.1 * k, 860, 640, 0.0)
        h.rim_color(h.pal["verde"])
        import mundos_base as B
        NC.pegar(B.superficie("metal", 71), h, 1.0, rampa="piedra", oscuro=0.8)
        n_ = 7
        # dos repisas con cajas: la de arriba ya cerrada, la de abajo se cierra de izquierda a derecha
        for yb, fila, esc_ in ((590, 0, 0.9), (930, 1, 1.0)):
            h.pieza(C.rect(-300, yb, 2400, 50), 70, 500 + fila, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.8, rampa="madera")
            for i in range(n_):
                x = 140 + i * 240
                if fila == 0:
                    tk = self.tb[7] - 0.4 + (n_ - 1 - i) * 0.12
                else:
                    tk = self.tb[7] + 0.25 + i * 0.26
                cerrada = clamp01((t - tk) / 0.18)
                P.caja(h, x, yb, esc_, sem=510 + i + 20 * fila, rotulo=f"{20 + i * 3 + fila * 40}-L", tono=125, ancho=220, alto=180,
                       candado_=True, abierto=1 - cerrada)
                if 0 < t - tk < 0.4:
                    f = 1 - (t - tk) / 0.4
                    h.resplandor(x, yb - 40, 150, 0.9 * f, col=h.pal["verde"])
        # la mano (desde arriba) que va pulsando cada candado de la fila de abajo
        f = (t - (self.tb[7] + 0.25)) / 0.26
        if -0.8 < f < n_ + 1.5:
            xm = 140 + 240 * min(max(f, 0.0), n_ - 1.0)
            tap = 0.5 + 0.5 * math.sin(f * 2 * math.pi - math.pi / 2)
            ym = 898 - 118 * 1.0 - 70 + 55 * tap
            P.mano(h, xm - 6, ym, 1.0, ang=math.pi / 2, pose="dedo", sem=560, rampa="piedra", tono=130, manga="piedra", manga_tono=60,
                   largo_brazo=1200)
        C.ambiente(h, 0.4)
        h.luz_cono(860, -300, math.pi / 2, 0.8, 1700, h.pal["luna"], k=1.3, suave=0.6)
        h.luz_radial(860, 650, 1200, h.pal["verde"], k=0.3)
        C.banda(h, "CERRADURAS NUEVAS", 960, 140, 56, t, self.t_cerr, sem=11, claro=True)
        N.motas(h, t, n=40, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.05, sem=33), bloom=0.5)

    # ------------------------------------------------------------------ H. caso cerrado: el pasillo a oscuras
    def p_pasillo(self, h, t, u):
        t_off = self.t_caso + 2.0                                   # «pensaron»: el último pulsa el interruptor
        apag = smooth(clamp01((t - t_off) / 0.15))
        luz_on = 1.0 - apag
        k = smooth(clamp01(u / 5.4))
        h.camara(1.0 + 0.1 * k, 960 - 40 * k, 520 + 10 * k, 0.0)
        h.rim_color(h.pal["luna"])
        # tubos y rótulo: apagados salvo el verde de la SALIDA, que queda como un resto
        NC.pegar(M.pasillo_salida(), h, 1.0, rampa="piedra", emis=0.3 + 0.7 * luz_on, col_emis=(0.75, 1.0, 0.8))
        # el parte de cierre pegado a la pared, con su sello
        T = C.T_obj(560, 400, -0.05, 1.0)
        h.pieza(T(C.rect(-150, -190, 300, 380)), 214, 600, w=4, luz=(0.3, -1), d=6, sombra=0.3, trama=0, rim=0.4, rampa="papel")
        for j in range(8):
            q = T(np.array([[-120, -110 + j * 34], [100 - 14 * (j % 3), -110 + j * 34]]))
            h.trazo(q, 3, 601 + j, alfa=0.6)
        c = T(np.array([[0, -150]]))[0]
        N.texto_maquina(h, "PARTE DE CIERRE", c[0], c[1], 24, t, -99, cps=1e9, tono=0.08, centro=True, encuadrar=False, ang=-0.05)
        if t > self.t_caso + 0.3:
            N.sello(h, "CASO CERRADO", 560, 470, 44, t, self.t_caso + 0.3, rot=-14, tono=np.array(h.pal["sello"]), alfa=0.95)
        # los ingenieros caminan hacia la puerta: cada uno más pequeño al alejarse
        for i in range(3):
            q = clamp01((t - self.tb[8] - 0.35 - 0.3 * i) / 1.9)
            if q <= 0 or q >= 1:
                continue
            yy = 1260 - 620 * e_out(q)
            x = (560 + 260 * i) + (1000 + 40 * (i - 1) - (560 + 260 * i)) * q
            sc = 0.12 + 0.7 * ((yy - 610) / 770)
            K.caminante(h, x, yy, sc, fase=K.fase_paso(q * 900, sc), sem=620 + i * 9, tono=44 + 6 * i, d=1, barba=bool(i % 2))
        # el último (solo su brazo, junto a cámara) pulsa el interruptor
        pul = smooth(clamp01((t - (t_off - 0.7)) / 0.6))
        if t_off - 1.0 < t < t_off + 0.8:
            sale = 1.0 - smooth(clamp01((t - (t_off + 0.1)) / 0.6))
            ax, ay = 129 - 70 * (1 - pul * sale), 498 + 380 * (1 - pul * sale) + 0
            P.mano(h, ax, ay, 1.0, ang=-0.62, pose="dedo", sem=640, rampa="piedra", tono=130, manga="piedra", manga_tono=70,
                   largo_brazo=900)
        C.ambiente(h, 0.5 * luz_on + 0.2)
        h.luz_radial(1000, 320, 1000, h.pal["lampara"], k=0.9 * luz_on)
        h.luz_radial(1000, 330, 800, (0.75, 1.0, 0.8), k=0.3)
        # a oscuras: dos rendijas verdes se encienden en la puerta del fondo y parpadean
        ojos = clamp01((t - (t_off + 0.7)) / 0.3)
        if ojos > 0:
            par = 0.0 if math.sin(t * 2.1) < -0.985 else 1.0
            for sx in (-1, 1):
                h.emitir(C.rect(1000 + sx * 30 - 11, 506, 22, 16 * par + 2), 2.2 * ojos, col=h.pal["verde"], blur=1.2)
            h.luz_radial(1000, 520, 380, h.pal["verde"], k=1.0 * ojos)
            h.resplandor(1000, 516, 150, 0.5 * ojos, col=h.pal["verde"])
        return h.acabado(t, niebla=dict(dens=0.08, sem=34), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "grave_inquietante", 0.45, 0.0, dur=3.0)
        self.ev(tb[0] + 1.6, "sombra_crece", 0.45, 0.2, dur=1.5)
        self.ev(tb[1] + 0.1, "zumbido_servidores", 0.3, 0.0, dur=tb[3] - tb[1])
        self.ev(tb[1] + 0.8, "datos", 0.35, 0.3, dur=2.0)
        self.ev(tb[2] + 0.3, "paso_firme", 0.35, 0.0)
        self.ev(tb[3] + 0.5, "lapiz", 0.55, -0.2, dur=2.6)
        self.ev(self.t_trafico - 0.5, "alarma_leds", 0.5, 0.2, dur=2.5)
        self.ev(tb[5] + 0.45, "caida", 0.8, -0.2)
        self.ev(tb[5] + 2.6, "electricidad", 0.5, 0.2, dur=2.0)
        self.ev(tb[6] + 0.4, "cerilla", 0.4, 0.2)
        self.ev(tb[6] + 0.6, "chisporroteo", 0.45, 0.2, dur=1.6)
        for i in range(7):
            self.ev(tb[7] + 0.25 + i * 0.26 + 0.14, "tambor_click", 0.55, -0.6 + i * 0.2)
        self.ev(self.t_caso + 0.3, "sello_golpe", 0.8, -0.2)
        self.ev(self.t_caso + 2.0, "interruptor", 0.8, -0.6)
        self.ev(self.t_caso + 2.7, "subida", 0.4, 0.0, dur=1.2)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
