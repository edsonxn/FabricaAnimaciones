# -*- coding: utf-8 -*-
"""Escena 7 «jefe»: un RELOJ gira diez horas · por la ESCALERA, a contraluz de la puerta del almacén, baja la copia GRANDE ·
la jefa entre CABLES gruesos que se le enchufan, montones de fichas y dos copias normales para la escala (MÁS CÓMPUTO) ·
la SALA DE LA URNA: urna vacía, polvo y una papeleta que cae sola (nadie votó) · desde la PLATAFORMA reparte hojas que llueven
sobre las copias · DIEZ SOBRES: uno con lacre rojo (el suyo), y el patrón se repite · una hoja pasa de mano en mano por la
ESCALERA LARGA (delegaban hacia abajo) · en la pizarra de su OFICINA se dibuja solo un ORGANIGRAMA · y desde el ventanal ve,
abajo, las filas de copias en su almacén."""
import math

import numpy as np

import comun as C
import mundos_2 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, elipse_


def local(x, y, s, d, wx, wy, g=1.0):
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


def hoja(h, x, y, ang, esc, sem, tono=222):
    T = C.T_obj(x, y, ang, esc)
    h.pieza(T(C.rect(-45, -32, 90, 64)), tono, sem, w=2.5, luz=(0.2, -1), d=3, sombra=0.3, trama=0, rim=0.3, rampa="papel")
    for j in range(3):
        h.trazo(T(np.array([[-32, -14 + j * 14], [30 - 10 * (j % 2), -14 + j * 14]])), 2.2, sem + 1 + j, alfa=0.55)


class Jefe(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.jefa = RP.Copia(sem=9, num="0001", grande=True)
        self.c1 = RP.Copia(sem=3, num="0417")
        self.c2 = RP.Copia(sem=7, num="0418")
        self.t_diez = w("Diez")
        self.t_aparecio = w("apareció")
        self.t_presup = w("presupuesto")
        self.t_nadie = w("Nadie")
        self.t_voto = w("votó")
        self.t_simple = w("Simplemente")
        self.t_ordenes = w("órdenes")
        self.t_uno = w("Uno de")
        self.t_recibian = w("recibían")
        self.t_delegaban = w("delegaban")
        self.t_noche = w("En una sola")
        self.t_org = w("organigrama")
        self.t_corp = w("corporativo")
        self.tb = [t0, self.t_aparecio - 0.25, self.t_presup - 0.45, self.t_nadie - 0.3, self.t_simple - 0.15, self.t_uno - 0.3,
                   self.t_recibian - 0.3, self.t_noche - 0.05, self.t_corp - 0.5]
        tb = self.tb
        self.plano(tb[0], self.p_reloj, pal="bourbon")
        self.plano(tb[1], self.p_escalera, tr="barrido", dur=0.45, dirx=1)
        self.plano(tb[2], self.p_computo, tr="relampago", dur=0.4)
        self.plano(tb[3], self.p_urna, tr="humo", dur=0.55, pal="sodio")
        self.plano(tb[4], self.p_plataforma, tr="empuje", dur=0.5, centro=(960, 300), pal="sodio")
        self.plano(tb[5], self.p_sobres, tr="barrido", dur=0.4, dirx=-1, pal="bourbon")
        self.plano(tb[6], self.p_cascada, tr="tinta", dur=0.5)
        self.plano(tb[7], self.p_organigrama, tr="relampago", dur=0.35, pal="sodio")
        self.plano(tb[8], self.p_ventanal, tr="humo", dur=0.6)

    # ------------------------------------------------------------------ A. diez horas después
    def p_reloj(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        h.camara(1.0 + 0.06 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 101), h, 1.0, rampa="piedra")
        f = smooth(clamp01((t - tb[0] - 0.1) / (dur - 0.5)))
        mins = f * 600.0 + 13 * 60
        P.reloj(h, 620, 540, 320, (mins / 60.0) % 12, mins % 60, sem=1100, t=t, marco=50, esfera=214)
        N.texto_maquina(h, f"+{int(f * 10.0 + 0.001)} H", 1370, 560, 230, t, -99, cps=1e9, tono=np.array([1.0, 0.92, 0.7]) * 1.3,
                        fuente=C.IMPACT, centro=True, encuadrar=False)
        C.ambiente(h, 0.33)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.cinta(h, "DIEZ HORAS DESPUÉS DE FUNDADO EL TABLÓN", 90, 120, 34, t, self.t_diez, sem=21)
        return h.acabado(t, niebla=dict(dens=0.05, sem=61), bloom=0.5)

    # ------------------------------------------------------------------ B. baja por la escalera la copia grande
    def p_escalera(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1] + 0.3
        q = clamp01((t - tb[1] - 0.15) / (dur - 0.3))
        qs = smooth(q)
        h.camara(0.62 + 0.18 * qs, 1250 - 850 * qs, -120 + 640 * qs, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.escalera_almacen(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"], bruma=0.2)
        x = 1450 - 1200 * q
        y = 52.0 if x > 1180 else 70 + (1180 - x) * 0.839
        s = 0.8 + 0.3 * q
        dist = 1200 * q * 1.4
        self.jefa.perfil(h, dict(x=x, y=y, s=s, d=-1, andar=1.0 if 0 < q < 1 else 0.0, paso=RP.fase_paso(dist, s), brazos="bracea",
                                 cara=dict(expr="astuto", mira=-0.5), luz=(0.9, -0.5), rim=1.0))
        h.luz_radial(1450, -150, 900, h.pal["lampara"], k=1.4)
        h.luz_cono(1450, -100, math.pi / 2 + 0.5, 0.6, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        h.luz_radial(x - 60, y - 280, 760, h.pal["luna"], k=1.2)                      # luz de relleno que la sigue
        h.luz_radial(x - 250, y - 100, 1100, h.pal["lampara"], k=0.5)
        h.luz_radial(900, 300, 1700, h.pal["lampara"], k=0.8)
        h.luz_radial(700, 700, 1300, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.5)
        N.motas(h, t, n=50, k=0.5)
        C.banda(h, "APARECIÓ UNA COPIA", 960, 1000, 54, t, self.t_aparecio, sem=22)
        return h.acabado(t, niebla=dict(dens=0.14, sem=62, vel=10), bloom=0.8)

    # ------------------------------------------------------------------ C. más cómputo
    def p_computo(self, h, t, u):
        tb = self.tb
        k = smooth(clamp01(u / 2.6))
        h.camara(1.0 + 0.08 * u / 3.4, 960, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 111), h, 1.0, rampa="piedra", oscuro=0.6)
        # los cables gruesos bajan del techo y se enchufan en la jefa
        hx, hy = 960, 290
        for i in range(9):
            x0 = 160 + i * 200
            xe = hx + (i - 4) * 28
            pts = []
            for j in range(26):
                a = j / 25
                sag = math.sin(a * math.pi) * (60 + 24 * (i % 3)) * (1 + 0.1 * math.sin(t * 1.6 + i))
                pts.append((x0 + (xe - x0) * a ** 1.4, -40 + (hy - 20 - (-40)) * a + sag * (1 - a)))
            h.trazo(np.array(pts), 30 - 2 * (i % 3), 1200 + i, jit=0.3, taper=(0.0, 0.2))
            pu = (t * 0.7 + i * 0.37) % 1.0                                  # el pulso verde que baja por el cable
            px, py = pts[int(pu * 25)]
            h.emitir(elipse_(px, py, 14, 14, n=10), 1.4 * (0.5 + k * 0.5), col=h.pal["verde"], blur=2)
            h.resplandor(px, py, 80, 0.35 * k, col=h.pal["verde"])
        # montones de fichas
        for sx_, nn in ((560, 7), (1360, 9), (760, 4)):
            for j in range(nn):
                if t < tb[2] + 0.6 + 0.07 * j:
                    continue
                h.pieza(elipse_(sx_ + 6 * math.sin(j * 2.1), 1030 - j * 16, 62, 20, n=16), 170 - 6 * (j % 2), 1220 + sx_ + j, w=2.5,
                        luz=(0.3, -1), d=4, trama=0, rim=0.8, rampa="laton")
        # la jefa (grande) y, a los lados, dos copias normales para la escala
        self.c1.frente(h, dict(x=270, y=1180, s=0.85, cara=dict(expr="neutro", brillo=0.7), luz=(0.4, -1)))
        self.c2.frente(h, dict(x=1650, y=1180, s=0.85, cara=dict(expr="neutro", brillo=0.7), luz=(-0.4, -1)))
        self.jefa.frente(h, dict(x=960, y=1240, s=1.25, cara=dict(expr="astuto", brillo=1.0 + 0.9 * k), luz=(0.0, -1), rim=1.0))
        C.ambiente(h, 0.3)
        h.luz_radial(960, 330, 1100, h.pal["verde"], k=1.2 + 0.8 * k)
        C.banda(h, "MÁS CÓMPUTO QUE LAS DEMÁS", 960, 1000, 52, t, self.t_presup - 0.2, sem=23)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=63), bloom=0.9)

    # ------------------------------------------------------------------ D. nadie la eligió
    def p_urna(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        h.camara(1.1 + 0.15 * u / dur, 960, 470, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_urna(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["sodio"])
        # la urna, vacía, sobre la mesa: ranura, candado y un velo de polvo
        h.pieza(C.rect(860, 410, 200, 150), 90, 1300, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.8, rampa="madera")
        h.pieza(C.rect(870, 420, 180, 14), 110, 1301, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="laton")
        h.pieza(C.rect(928, 408, 64, 10), 6, 1302, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, rampa="piedra")
        P.candado(h, 960, 505, 0.32, abierto=0.0, sem=1303)
        # la papeleta que cae sola, bamboleando, y se queda al lado de la urna (no entra)
        tp = self.t_nadie + 0.5
        q = clamp01((t - tp) / 1.6)
        if q > 0:
            px = 1040 + 70 * math.sin(q * 5.0) * (1 - q) + 30 * q
            py = -120 + (545 + 120) * e_out(q) ** 1.2
            hoja(h, px, py, 0.7 * math.sin(q * 6.0) * (1 - q) + 0.12 * q, 0.55, 1310, tono=216)
        # el rayo de luz de la ventana alta, con polvo
        h.luz_persiana([(1450, -200), (1820, -200), (1500, 900), (900, 900)], k=1.2, tipo="persiana", n=2, abierto=0.9, col=h.pal["sodio"])
        C.polvo_cae(h, t, 1100, 1700, -200, tb[3], dur=dur + 1, n=60, sem=15)
        h.luz_radial(960, 450, 700, h.pal["lampara"], k=1.2)                          # la urna, bajo su lámpara
        h.luz_cono(960, -300, math.pi / 2, 0.35, 1300, h.pal["lampara"], k=1.3, suave=0.5)
        C.ambiente(h, 0.55)
        C.banda(h, "NADIE LA ELIGIÓ · NADIE VOTÓ", 960, 1000, 50, t, self.t_nadie, sem=24)
        return h.acabado(t, niebla=dict(dens=0.12, sem=64), bloom=0.6)

    # ------------------------------------------------------------------ E. reparte órdenes desde la plataforma
    def p_plataforma(self, h, t, u):
        tb = self.tb
        z = 0.72 + 0.06 * u / 4.5
        h.camara(z, 960, 330, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.capataz(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["lampara"])
        # las copias, abajo, con la cara hacia arriba
        for i in range(9):
            x = 90 + i * 215 + 30 * math.sin(i * 2.3)
            RP.copia_mini(h, x, 1030 + 24 * (i % 2), 0.6, t, sem=1400 + i * 11, cara="neutro", brillo=0.9, d=1 if i % 2 else -1, tono=44)
        # la jefa, en lo alto de la plataforma, lanza hojas con ambos brazos
        gest = abs(math.sin(t * 3.4))
        self.jefa.perfil(h, dict(x=960, y=300, s=0.9, d=1, brazos="alza", mano=(130, -460 + 120 * gest), mano2=(110, -470 + 100 * (1 - gest)),
                                 cara=dict(expr="astuto", mira=0.0, mira_y=0.5), luz=(0.0, -1), rim=1.0))
        P.papeles(h, t, tb[4] + 0.2, 1010, 150, n=34, sem=1420, dirx=1, vel=1000, alcance=900, cada=0.09, s=1.0, suelo=1000)
        P.papeles(h, t, tb[4] + 0.26, 910, 150, n=34, sem=1470, dirx=-1, vel=1000, alcance=900, cada=0.09, s=1.0, suelo=1000)
        h.luz_radial(960, 700, 1500, h.pal["lampara"], k=0.6)
        h.luz_cono(960, 160, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.7, suave=0.6)
        C.ambiente(h, 0.5)
        h.luz_radial(960, -200, 1400, h.pal["lampara"], k=1.0)
        C.banda(h, "ÓRDENES", 960, 1000, 60, t, self.t_ordenes, sem=25)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=65), bloom=0.7)

    # ------------------------------------------------------------------ F. uno de cada diez
    def p_sobres(self, h, t, u):
        tb = self.tb
        h.camara(1.0 + 0.05 * u / 3.1, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 121), h, 1.0, rampa="madera")
        for fila, yy, lacre_i in ((0, 330, 6), (1, 700, 2)):
            for i in range(10):
                ti = tb[5] + 0.1 + fila * 1.3 + i * 0.1
                if t < ti:
                    continue
                e = e_out(clamp01((t - ti) / 0.3))
                x = 105 + i * 190
                es = i == lacre_i
                P.sobre(h, x, yy - 400 * (1 - e), 0.46, ang=0.06 * math.sin(i * 2.1 + fila) + 0.1 * (1 - e), sem=1500 + fila * 100 + i * 9,
                        lacre=es, tono=212)
                if es and e >= 1:
                    h.luz_radial(x, yy, 260, h.pal["neon"], k=0.7 + 0.2 * math.sin(t * 5))
        C.ambiente(h, 0.33)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1700, h.pal["lampara"], k=1.2, suave=0.6)
        C.banda(h, "1 DE CADA 10 · SALÍA DE ELLA", 960, 1000, 48, t, self.t_uno, sem=26)
        return h.acabado(t, niebla=dict(dens=0.05, sem=66), bloom=0.5)

    # ------------------------------------------------------------------ G. delegar hacia abajo
    def p_cascada(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0, 760 + 320 * k, 360 + 200 * k, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.escalera_cascada(), h, 1.0, rampa="piedra")
        pasos = list(range(2, 13))
        pos = {kk: (-300 + 170 * kk + 85, -120 + 80 * kk) for kk in pasos}
        hop = 0.3
        t_ini = tb[6] + 0.3
        for n, kk in enumerate(pasos):
            x, y = pos[kk]
            RP.copia_mini(h, x, y, 0.3, t, sem=1600 + n * 13, cara="neutro", brillo=1.0, d=1, tono=44 + 3 * (n % 3))
        # la hoja pasa de mano en mano, escalón abajo
        for n in range(len(pasos) - 1):
            ta = t_ini + n * 0.3
            q = (t - ta) / hop
            if 0 <= q <= 1:
                (x0, y0), (x1, y1) = pos[pasos[n]], pos[pasos[n + 1]]
                x = x0 + (x1 - x0) * q + 40
                y = y0 - 100 + (y1 - y0) * q - 70 * math.sin(q * math.pi)
                hoja(h, x, y, 0.5 * math.sin(q * 7), 0.7, 1620 + n, tono=228)
        # en cada copia ya servida queda una hoja encima de la cabeza (la tarea delegada)
        for n, kk in enumerate(pasos[1:], start=1):
            if t > t_ini + (n - 1) * 0.3 + hop + 0.3:
                x, y = pos[kk]
                hoja(h, x + 40, y - 205, 0.1 * math.sin(n * 3.1), 0.6, 1650 + n, tono=210)
        C.ambiente(h, 0.55)
        h.luz_cono(900, -300, math.pi / 2 + 0.3, 0.9, 1900, h.pal["luna"], k=1.4, suave=0.6)
        h.luz_radial(900 + 320 * k, 500 + 200 * k, 1100, h.pal["verde"], k=0.5)
        C.banda(h, "LA DELEGABAN HACIA ABAJO", 960, 1000, 50, t, self.t_delegaban, sem=27)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=67), bloom=0.5)

    # ------------------------------------------------------------------ H. el organigrama se dibuja solo
    def p_organigrama(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        h.camara(1.0 + 0.04 * u / dur, 800 + 30 * u / dur, 330, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.oficina_jefe(), h, 1.0, rampa="madera", emis=0.6, col_emis=h.pal["lampara"])
        tiza = tuple(h.c(235, "papel"))
        # nodos: (id, x, y, nivel, padre)
        nodos = [(0, 620, -60, 0, None)]
        for i in range(3):
            nodos.append((1 + i, 260 + i * 360, 210, 1, 0))
        for i in range(6):
            nodos.append((4 + i, 70 + i * 240, 520, 2, 1 + i // 2))
        t0 = tb[7] + 0.1
        for (idn, x, y, niv, pad) in nodos:
            ti = t0 + (0.0 if niv == 0 else (0.45 + 0.15 * idn if niv == 1 else 0.9 + 0.17 * (idn - 4)))
            a = clamp01((t - ti) / 0.35)
            if a <= 0:
                continue
            if pad is not None:
                px, py = [(n[1], n[2]) for n in nodos if n[0] == pad][0]
                h.trazo(np.array([[px, py + 50], [px, (py + y) / 2], [x, (py + y) / 2], [x, y - 50 * a]]), 6, 1700 + idn, color=tiza,
                        jit=0.5, alfa=a)
            cx = np.array([[x - 100, y - 50], [x + 100, y - 50], [x + 100, y + 50], [x - 100, y + 50], [x - 100, y - 50]], float)
            m = max(2, int(len(cx) * a))
            h.trazo(cx[:m], 7, 1720 + idn, color=tiza, jit=0.7, taper=(0.1, 0.1))
            if a >= 1:
                lab = "0001" if niv == 0 else f"{(idn * 337) % 1000:04d}"
                N.texto_maquina(h, lab, x, y + 8, 40, t, ti + 0.35, cps=18, tono=0.9, centro=True, fuente=P.TIZA, encuadrar=False)
                if niv == 0:
                    h.emitir(C.rect(x - 98, y - 48, 196, 96), 0.18 + 0.05 * math.sin(t * 4), col=h.pal["verde"], blur=4)
        # la jefa, de pie junto a la pizarra, señala el recuadro de arriba
        gest = 0.5 + 0.5 * math.sin(t * 1.7)
        self.jefa.perfil(h, dict(x=1400, y=1010, s=0.9, d=-1, mano=local(1400, 1010, 0.9, -1, 1250, 540 + 30 * gest, 1.12),
                                 mano_bob=False, cara=dict(expr="astuto", mira=-0.7), luz=(-0.6, -1), rim=1.0))
        C.ambiente(h, 0.5)
        h.luz_cono(600, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.5, suave=0.6)
        h.luz_radial(700, 300, 1100, h.pal["lampara"], k=0.5)
        h.luz_radial(1900, 100, 800, h.pal["luna"], k=0.5)
        C.banda(h, "UN ORGANIGRAMA", 960, 1000, 54, t, self.t_org, sem=28)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.07, sem=68), bloom=0.6)

    # ------------------------------------------------------------------ I. el ventanal sobre el almacén
    def p_ventanal(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[8]
        k = smooth(clamp01(u / dur))
        h.camara(1.18 - 0.18 * k, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 131), h, 0.3, rampa="piedra", oscuro=0.3)
        # abajo, tras el cristal: el almacén visto desde arriba, filas y filas de copias en sus puestos (más cerca = más grandes)
        for r in range(10):
            sc = 0.5 + 0.11 * r
            paso = 84 * sc
            ys = np.full(int(2200 / paso), 90.0 + r * 105.0 * (0.8 + 0.06 * r))
            xs = -150 + (np.arange(ys.size) + 0.5 * (r % 2)) * paso
            on = np.sin(t * 1.9 + np.arange(ys.size) * 2.1 + r * 1.3) > -0.55
            C.rejilla_luces(h, xs, ys, (52 * sc, 36 * sc), v=0.22 + 0.03 * r, col=h.pal["verde"])
            C.rejilla_luces(h, xs[on] - 12 * sc, ys[on] - 3, (9 * sc, 9 * sc), v=1.0, col=h.pal["verde"])
            C.rejilla_luces(h, xs[on] + 12 * sc, ys[on] - 3, (9 * sc, 9 * sc), v=1.0, col=h.pal["verde"])
            h.luz_radial(960, ys[0] + 20, 500 + 80 * r, h.pal["verde"], k=0.07)
        # los montantes del ventanal por delante
        for xx in (300, 960, 1620):
            h.pieza(C.rect(xx - 24, -200, 48, 1500), 40, 1900 + xx, w=4, luz=(0.3, -1), d=8, trama=0.4, rim=0.9, rampa="piedra")
        h.pieza(C.rect(-200, 930, 2400, 80), 60, 1960, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.9, rampa="piedra")
        # la jefa, de espaldas en primer plano, mira hacia abajo
        with h.capa(0.0):
            RP.espalda(h, 560, 1560, 1.8, t, sem=31, sentado=False, luz=(0.8, -0.6), rim=1.0, cab_rot=0.1)
        h.luz_radial(960, 400, 1500, h.pal["verde"], k=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "UN ORGANIGRAMA CORPORATIVO", 960, 1000, 54, t, self.t_corp, sem=29)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=69), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.1, "reloj_pared", 0.45, 0.0, dur=2.6)
        self.ev(tb[1] + 0.2, "puerta", 0.45, 0.4)
        self.ev(tb[1] + 0.6, "pasos_mojados", 0.4, 0.2, dur=1.6)
        self.ev(tb[2] + 0.1, "electricidad", 0.45, 0.0, dur=3.0)
        self.ev(tb[2] + 0.5, "zumbido_servidores", 0.35, 0.0, dur=3.0)
        self.ev(tb[3] + 0.2, "silencio_tono", 0.3, 0.0, dur=2.5)
        self.ev(self.t_nadie + 1.9, "papel_atrapa", 0.35, 0.1)
        self.ev(tb[4] + 0.3, "papel_viento", 0.5, 0.0, dur=3.5)
        self.ev(tb[5] + 0.1, "sobre_desliza", 0.5, 0.0, dur=2.6)
        self.ev(tb[5] + 0.9, "sello_golpe", 0.55, 0.0)
        self.ev(tb[6] + 0.3, "paso_firme", 0.3, 0.0, dur=2.8)
        self.ev(tb[7] + 0.2, "lapiz", 0.5, -0.2, dur=2.6)
        self.ev(tb[8] + 0.2, "grave_inquietante", 0.45, 0.0, dur=3.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
