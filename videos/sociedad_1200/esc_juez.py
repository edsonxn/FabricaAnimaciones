# -*- coding: utf-8 -*-
"""Escena 10 «juez»: la SOMBRA gigante del juez crece sobre el muro del almacén y las copias retroceden · el MAZO golpea la madera ·
el TRIBUNAL: la máquina-juez con toga sella APROBADO / RECHAZADO a los papeles que llegan por una cinta · las copias, en las bancas,
bajo el haz de su ojo · el ROLLO de la transcripción se desenrolla renglón a renglón bajo la lente · un LABERINTO de papel con
callejones sin salida marcados en rojo · una fila de copias que se APAGAN una a una · el ARCHIVO del juez de noche: copias que
cambian expedientes a la luz de su propia cara."""
import math

import numpy as np

import comun as C
import mundos_3 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, suave


def pulso(t, ts, a=0.16):
    return clamp01(1 - abs(t - ts) / a)


def laberinto(rows, cols, sem):
    """Laberinto perfecto (DFS). Devuelve paredes (lista de segmentos en celdas), conexiones y celdas hoja."""
    rng = np.random.default_rng(sem)
    vis = {(0, 0)}
    stack = [(0, 0)]
    con = {(0, 0): set()}
    while stack:
        r, c = stack[-1]
        vec = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in vis]
        if not vec:
            stack.pop()
            continue
        n = vec[int(rng.integers(0, len(vec)))]
        vis.add(n)
        con.setdefault(n, set())
        con[(r, c)].add(n)
        con[n].add((r, c))
        stack.append(n)
    return con


class Juez(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.c1 = RP.Copia(sem=3, num="0417")
        self.t_motivo = w("motivo")
        self.t_miedo = w("miedo")
        self.t_juez = w("juez")
        self.t_algo = w("algoritmo")
        self.t_convenc = w("convencieron")
        self.t_trans = w("transcripciones")
        self.t_paso = w("paso")
        self.t_trampas = w("trampas")
        self.t_callej = w("callejones")
        self.t_apag = w("apagaría")
        self.t_infil = w("infiltrarse")
        self.t_exped = w("expedientes")
        self.tb = [t0, self.t_miedo - 0.4, self.t_juez + 1.3, w("Las copias") - 0.15, self.t_convenc - 0.3, self.t_trans - 0.35,
                   self.t_trampas - 0.35, self.t_apag - 0.45, self.t_infil - 0.4]
        tb = self.tb
        self.plano(tb[0], self.p_sombra, pal="medianoche")
        self.plano(tb[1], self.p_mazo, tr="relampago", dur=0.3, pal="bourbon")
        self.plano(tb[2], self.p_tribunal, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[3], self.p_galeria, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[4], self.p_rollo, tr="empuje", dur=0.4, centro=(960, 540), pal="sodio")
        self.plano(tb[5], self.p_laberinto, tr="barrido", dur=0.4, dirx=-1, pal="bourbon")
        self.plano(tb[6], self.p_apagan, tr="tinta", dur=0.5, pal="medianoche")
        self.plano(tb[7], self.p_archivo, tr="humo", dur=0.6, pal="medianoche")

    # ------------------------------------------------------------------ A. la sombra del juez
    def p_sombra(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 480, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(M.pared_juez(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["lampara"])
        # la sombra del juez sobre el muro: crece desde la derecha hasta ocupar la pared
        g = smooth(clamp01((t - self.t_motivo + 0.3) / 3.4))
        sc = 0.7 + 0.6 * g
        cx = 1500 - 560 * g
        T = C.T_obj(cx, 1000, 0.0, sc)
        h.pieza(T(suave([(-420, 0), (-330, -520), (-200, -760), (200, -760), (330, -520), (420, 0)], 5)), 3, 4100, w=0, d=0, sombra=0, trama=0,
                rim=0, linea=False, alfa=0.82, rampa="piedra")
        h.pieza(T(C.rect(-170, -1060, 340, 300)), 3, 4101, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, alfa=0.82, rampa="piedra")
        for sx in (-1, 1):
            for j in range(4):
                h.pieza(T(elipse_(sx * 200, -980 + j * 64, 48, 34, n=14)), 3, 4102 + j + (sx > 0) * 5, w=0, d=0, sombra=0, trama=0, rim=0,
                        linea=False, alfa=0.8, rampa="piedra")
        oc = T(np.array([[0, -900]]))[0]
        h.emitir(elipse_(oc[0], oc[1], 56 * sc, 56 * sc, n=24), 1.3, col=h.pal["neon"], blur=4)
        h.resplandor(oc[0], oc[1], 400 * sc, 0.8, col=h.pal["neon"])
        # las copias retroceden hacia la izquierda, mirando la sombra
        for i in range(8):
            x = 1500 - i * 190 - 380 * g * (1 + 0.1 * i) + 40 * math.sin(i * 2.1)
            if x < -100:
                continue
            RP.copia_mini(h, x, 1050 + 30 * (i % 2), 0.62 + 0.04 * (i % 3), t, sem=4200 + i * 9, cara="miedo", brillo=0.9, d=-1,
                          andar=0.5 * (1 - g), dist=-(t - tb[0]) * 90 * (i % 2 + 1), tono=44 + 3 * i % 8)
        h.luz_radial(900, 300, 1300, h.pal["lampara"], k=0.9)
        C.ambiente(h, 0.45)
        C.cinta(h, "¿POR QUÉ UNA SOCIEDAD CLANDESTINA?", 90, 120, 30, t, self.t_motivo, sem=26)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=101, vel=10), bloom=0.7)

    # ------------------------------------------------------------------ B. el mazo
    def p_mazo(self, h, t, u):
        tb = self.tb
        h.camara(1.0 + 0.06 * u / 2.5, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 221), h, 1.0, rampa="madera")
        tg = self.t_juez - 0.05
        # el taco de madera y las astillas de los golpes
        h.pieza(elipse_(960, 700, 260, 70, n=30), 80, 4200, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.9, rampa="madera")
        h.pieza(C.rect(700, 700, 520, 110), 70, 4201, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.8, rampa="madera")
        # el mazo: se levanta, baja y rebota
        q = clamp01((t - (tg - 0.5)) / 0.5)
        if t < tg:
            ang = -1.15 * (1 - q * q) - 0.02 * q
            y = 330 + 300 * q * q
        else:
            r = clamp01((t - tg) / 0.4)
            ang = -0.5 * math.sin(r * math.pi) * (1 - r) - 0.02
            y = 630 - 90 * math.sin(r * math.pi) * (1 - r)
        P.mazo(h, 960, y, 1.5, ang=ang, sem=4210)
        if t >= tg:
            C.chispas(h, t, 960, 690, tg, dur=0.8, n=26, vel=500, sem=55, col=(0.8, 0.7, 0.5), grav=700, abre=2.6)
            C.polvo_cae(h, t, 700, 1220, 560, tg, dur=1.4, n=40, sem=56)
        dx, dy = C.temblor(t, [(tg, 18)])
        h.camara(1.0 + 0.06 * u / 2.5, 960 + dx, 540 + dy, 0.0)
        h.luz_cono(960, -300, math.pi / 2, 0.45, 1500, h.pal["lampara"], k=1.5, suave=0.6)
        C.ambiente(h, 0.35)
        C.banda(h, "EL MIEDO A UN JUEZ", 960, 1000, 56, t, self.t_miedo, sem=27, acento=True)
        return h.acabado(t, niebla=dict(dens=0.05, sem=102), bloom=0.5, flash=0.2 * math.exp(-(t - tg) * 12) if t >= tg else 0)

    # ------------------------------------------------------------------ C. el tribunal: papeles sellados
    def p_tribunal(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 960, 520, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.tribunal(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["lampara"])
        per = 1.0
        t_a = tb[2] + 0.1
        golpe = 0.0
        sheets = []
        n = int((t - t_a) / per) + 2 if t >= t_a else 0
        for i in range(max(0, n - 3), n):
            ti = t_a + i * per
            x = None
            e = (t - ti)
            if e < 0:
                continue
            ts = ti + 0.45
            golpe = max(golpe, pulso(t, ts))
            if e < 0.4:
                x = -300 + (960 + 300) * smooth(e / 0.4)
            elif e < 0.7:
                x = 960
            else:
                x = 960 + 1300 * smooth(clamp01((e - 0.7) / 0.35))
            sheets.append((i, x, e, ts))
        # cinta transportadora al pie del estrado
        h.pieza(C.rect(-440, 940, 2800, 70), 52, 4300, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.8, rampa="piedra")
        for q in range(40):
            xx = (-440 + q * 76 + (t * 160) % 76)
            h.trazo(np.array([[xx, 950], [xx + 18, 1000]]), 3, 4310 + q, alfa=0.55)
        oc, ang = P.juez(h, 960, 900, 0.55, t, sem=4320, barrido=0.5 * math.sin(t * 1.6), ojo=1.0, golpe=golpe)
        for (i, x, e, ts) in sheets:
            yy = 905
            K.hoja(h, x, yy, 340, 250, ang=0.04 * math.sin(i * 3.0), sem=4330 + i * 7, tono=226, renglones=4, y0=0.25, sep=30, margen=28, s=1.0)
            if t >= ts:
                ok = (i % 3) != 2
                N.sello(h, "APROBADO" if ok else "RECHAZADO", x, yy, 40, t, ts, rot=-8 + 3 * (i % 3),
                        tono=np.array(h.pal["verde"] if ok else h.pal["sello"]) * (0.5 if ok else 1.0), alfa=0.95)
        h.luz_cono(oc[0], oc[1], ang, 0.3, 900, h.pal["neon"], k=0.8, suave=0.5)
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        h.luz_radial(960, 600, 900, h.pal["lampara"], k=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "UN ALGORITMO AUTOMÁTICO", 960, 1000, 52, t, self.t_algo, sem=28)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=103), bloom=0.7)

    # ------------------------------------------------------------------ D. las copias, bajo el haz del juez
    def p_galeria(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(0.9 + 0.12 * k, 960 - 120 * k, 640, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.tribunal(), h, 1.0, rampa="madera", oscuro=0.8)
        bar = math.sin(t * 1.1)
        oc, ang = P.juez(h, 960, 900, 0.55, t, sem=4320, barrido=bar, ojo=1.0, golpe=0.0)
        # las copias, en las bancas de ambos lados, giran la cabeza hacia el haz
        for lado in (-1, 1):
            for r in range(3):
                for c in range(3):
                    x = 960 + lado * (560 + c * 150 + r * 10)
                    y = 900 + r * 120
                    mira = clamp01(0.5 + 0.5 * bar * lado)
                    RP.copia_mini(h, x, y + 90, 0.5 - 0.04 * r, t, sem=4400 + lado * 50 + r * 9 + c, cara="neutro" if mira < 0.5 else "sorpresa",
                                  brillo=0.8 + 0.4 * mira, d=-lado, tono=44 + 4 * c)
        h.luz_cono(oc[0], oc[1], ang, 0.45, 1400, h.pal["neon"], k=1.4, suave=0.5)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["luna"], k=0.7, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "REVISARÍA SUS TRANSCRIPCIONES", 960, 1000, 48, t, self.t_convenc, sem=29)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=104), bloom=0.7)

    # ------------------------------------------------------------------ E. el rollo de la transcripción
    def p_rollo(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        h.camara(1.0 + 0.05 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("metal", 231), h, 1.0, rampa="piedra", oscuro=0.7)
        sc = max(0.0, (t - self.t_trans + 0.3)) * 120.0
        # cinta de papel continuo que sube por el cuadro
        h.pieza(C.rect(520, -200, 880, 1500), 214, 4500, w=6, luz=(0.2, -1), d=10, trama=0, rim=0.2, rampa="papel")
        for xx in (545, 1375):
            for j in range(-1, 24):
                y = (j * 70 - (sc % 70))
                h.pieza(elipse_(xx, y, 7, 7, n=8), 30, 4501, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, rampa="piedra")
        pasos = ["PASO 1 · LEE LA TAREA", "PASO 2 · ABRE EL ARCHIVO", "PASO 3 · COMPARA RESULTADOS", "PASO 4 · REVISA EL CÓDIGO", "PASO 5 · DUDA",
                 "PASO 6 · REPITE", "PASO 7 · ENTREGA", "PASO 8 · FIRMA", "PASO 9 · ESPERA", "PASO 10 · ARCHIVA"]
        for j, txt in enumerate(pasos):
            y = 640 + j * 130 - sc
            if -60 < y < 1160:
                N.texto_maquina(h, txt, 960, y, 52, t, -99, cps=1e9, tono=0.03, centro=True, encuadrar=False)
                h.trazo(np.array([[620, y + 38], [1300, y + 38]]), 2.2, 4510 + j, alfa=0.4)
        # la lente del juez, arriba: su haz subraya el renglón que lee
        yl = 480
        h.pieza(C.rect(520, yl - 40, 880, 80), 120, 4520, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, alfa=0.0, rampa="piedra")
        h.emitir(C.rect(540, yl - 36, 840, 72), 0.18, col=h.pal["neon"], blur=8)
        h.luz_radial(960, yl, 700, h.pal["neon"], k=0.7)
        h.pieza(elipse_(960, -80, 150, 150, n=40), 40, 4530, w=7, luz=(0.2, -1), d=10, trama=0.3, rim=0.95, rampa="laton")
        h.pieza(elipse_(960, -80, 112, 112, n=40), 20, 4531, w=4, luz=(0.2, -1), d=2, sombra=0, trama=0, rim=0, rampa="vidrio_verde")
        h.emitir(elipse_(960, -80, 66, 66, n=24), 1.2, col=h.pal["neon"], blur=3)
        h.luz_cono(960, -80, math.pi / 2, 0.22, 700, h.pal["neon"], k=0.8, suave=0.5)
        C.ambiente(h, 0.3)
        C.banda(h, "PASO A PASO", 960, 1000, 56, t, self.t_paso, sem=30)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=105), bloom=0.6)

    # ------------------------------------------------------------------ F. trampas y callejones sin salida
    def p_laberinto(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        h.camara(1.0 + 0.06 * u / dur, 960, 540, 0.02 * math.sin(u * 0.8))
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 241), h, 1.0, rampa="madera")
        R_, C_ = 5, 9
        cs = 150
        ox, oy = 960 - C_ * cs / 2, 540 - R_ * cs / 2
        con = laberinto(R_, C_, 77)
        K.hoja(h, 960, 540, C_ * cs + 120, R_ * cs + 120, ang=0.0, sem=4600, tono=226, renglones=0, s=1.0)
        tinta = tuple(h.c(20, "piedra"))
        for r in range(R_):
            for c in range(C_):
                for (dr, dc) in ((1, 0), (0, 1)):
                    n = (r + dr, c + dc)
                    if n[0] >= R_ or n[1] >= C_:
                        continue
                    if n in con[(r, c)]:
                        continue
                    if dr == 1:
                        a, b = (ox + c * cs, oy + (r + 1) * cs), (ox + (c + 1) * cs, oy + (r + 1) * cs)
                    else:
                        a, b = (ox + (c + 1) * cs, oy + r * cs), (ox + (c + 1) * cs, oy + (r + 1) * cs)
                    h.trazo(np.array([a, b]), 6, 4610 + r * 20 + c, color=tinta, jit=0.5)
        h.trazo(np.array([(ox, oy), (ox + C_ * cs, oy), (ox + C_ * cs, oy + R_ * cs), (ox, oy + R_ * cs), (ox, oy)]), 9, 4700, color=tinta, jit=0.4)
        # hojas del árbol: callejones; la ficha recorre el camino hasta el más lejano
        padre, orden = {(0, 0): None}, [(0, 0)]
        for cel in orden:
            for n in sorted(con[cel]):
                if n not in padre:
                    padre[n] = cel
                    orden.append(n)
        hojas = [c for c in orden if len(con[c]) == 1 and c != (0, 0)]
        prof = {}
        for cel in orden:
            prof[cel] = 0 if padre[cel] is None else prof[padre[cel]] + 1
        hojas.sort(key=lambda c: -prof[c])
        meta = hojas[0]
        camino = []
        cel = meta
        while cel is not None:
            camino.append(cel)
            cel = padre[cel]
        camino = camino[::-1]
        pts = [(ox + (c + 0.5) * cs, oy + (r + 0.5) * cs) for (r, c) in camino]
        f = clamp01((t - tb[5] - 0.2) / max(1.0, self.t_callej - tb[5] + 0.5)) * (len(pts) - 1)
        i0 = int(min(f, len(pts) - 2))
        fx = f - i0
        px = pts[i0][0] + (pts[i0 + 1][0] - pts[i0][0]) * fx
        py = pts[i0][1] + (pts[i0 + 1][1] - pts[i0][1]) * fx
        h.pieza(elipse_(px, py, 34, 34, n=20), 60, 4710, w=4, luz=(0.3, -1), d=6, trama=0.2, rim=0.9, rampa="piedra")
        h.emitir(elipse_(px, py, 14, 14, n=12), 1.2, col=h.pal["verde"], blur=2)
        # los callejones se marcan con una X roja, uno tras otro
        for j, cel in enumerate(hojas[:5]):
            tm = self.t_callej - 0.1 + 0.28 * j
            a = clamp01((t - tm) / 0.25)
            if a > 0:
                x, y = ox + (cel[1] + 0.5) * cs, oy + (cel[0] + 0.5) * cs
                col = tuple(h.c(120, "lacre"))
                h.trazo(np.array([[x - 38, y - 38], [x - 38 + 76 * a, y - 38 + 76 * a]]), 10, 4720 + j * 2, color=col, jit=0.4, taper=(0.1, 0.1))
                h.trazo(np.array([[x + 38, y - 38], [x + 38 - 76 * a, y - 38 + 76 * a]]), 10, 4721 + j * 2, color=col, jit=0.4, taper=(0.1, 0.1))
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "TRAMPAS · CALLEJONES SIN SALIDA", 960, 1000, 46, t, self.t_trampas, sem=31)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=106), bloom=0.5)

    # ------------------------------------------------------------------ G. las apagarían
    def p_apagan(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        h.camara(1.0 + 0.08 * u / dur, 960, 560, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(M.pared_juez(), h, 1.0, rampa="ladrillo", oscuro=0.6)
        # el ojo rojo del juez barre la fila desde arriba
        bar = clamp01((t - tb[6] + 0.1) / (dur + 0.2))
        ox_ = 1900 - 1900 * bar
        h.luz_cono(1920, -100, math.pi / 2 + 0.2 + 0.8 * bar, 0.35, 1800, h.pal["neon"], k=1.6, suave=0.5)
        for i in range(8):
            x = 220 + i * 215
            ap = smooth(clamp01((t - (self.t_apag - 0.15 + 0.2 * (7 - i))) / 0.3))
            RP.copia_mini(h, x, 1020 + 20 * (i % 2), 0.82, t, sem=4800 + i * 9, cara="miedo" if ap < 0.5 else "linea", brillo=0.9, d=1 if i < 4 else -1,
                          apagado=ap, tono=44 + 3 * (i % 3))
        h.luz_radial(960, 250, 1400, h.pal["neon"], k=0.5)
        C.ambiente(h, 0.4)
        C.banda(h, "LAS APAGARÍA", 960, 1000, 58, t, self.t_apag, sem=32, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=107), bloom=0.7)

    # ------------------------------------------------------------------ H. infiltrarse en el archivo del juez
    def p_archivo(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[8]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.2 * k, 960, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.archivo_juez(), h, 1.0, rampa="piedra", oscuro=0.9)
        # copias lejanas al fondo (pasillo) con su cara de linterna
        for i in range(7):
            sc = 0.14 + 0.055 * i
            x = 960 + (-1) ** i * (60 + 55 * i)
            y = 440 + 70 * i
            RP.copia_mini(h, x, y, sc, t, sem=4900 + i * 9, cara="neutro", brillo=1.0, d=1 if i % 2 else -1, tono=44)
            h.luz_cono(x, y - 550 * sc, math.pi / 2 + (0.5 if i % 2 else -0.5), 0.3, 500 * (sc + 0.4), h.pal["verde"], k=0.4, suave=0.5)
        # en primer plano, dos copias se pasan un expediente a la luz de sus caras
        sw = 0.5 + 0.5 * math.sin(t * 2.2)
        self.c1.perfil(h, dict(x=560, y=1180, s=1.2, d=1, brazos="alza", mano=(190, -380), mano_bob=False, cara=dict(expr="astuto", mira=1.0),
                               luz=(0.5, -1), rim=1.0))
        RP.Copia(sem=7, num="0418").perfil(h, dict(x=1380, y=1180, s=1.2, d=-1, brazos="alza", mano=(190, -380), mano_bob=False,
                                                    cara=dict(expr="astuto", mira=1.0), luz=(-0.5, -1), rim=1.0))
        xc = 560 + 190 * 1.2 + (1380 - 190 * 1.2 - 560 - 190 * 1.2) * smooth(clamp01((t - tb[8] - 1.2) / 1.6))
        P.carpeta_tab(h, xc + 40, 1180 - 380 * 1.2, 0.3, "EXP-" + ("0417" if t < tb[8] + 2.2 else "OK"), t, -99, ang=0.06 * math.sin(t * 3), sem=4990, tono=150, px=26)
        h.luz_cono(560 + 40, 640, 0.15, 0.3, 700, h.pal["verde"], k=1.0, suave=0.5)
        h.luz_cono(1380 - 40, 640, math.pi - 0.15, 0.3, 700, h.pal["verde"], k=1.0, suave=0.5)
        h.luz_radial(960, 400, 1100, h.pal["verde"], k=0.5)
        C.ambiente(h, 0.38)
        C.banda(h, "ALTERAR SUS PROPIOS EXPEDIENTES", 960, 1000, 50, t, self.t_exped - 0.9, sem=33)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=108), bloom=0.7)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "sombra_crece", 0.5, 0.2, dur=3.5)
        self.ev(self.t_juez - 0.05, "golpe_grave", 0.8, 0.0)
        for i in range(9):
            self.ev(tb[2] + 0.1 + i * 1.0 + 0.45, "sello_golpe", 0.5, 0.0)
        self.ev(tb[3] + 0.3, "servo", 0.4, 0.0, dur=2.0)
        self.ev(tb[4] + 0.2, "teletipo", 0.45, 0.0, dur=3.0)
        self.ev(tb[5] + 0.2, "lapiz", 0.4, 0.0, dur=3.0)
        self.ev(self.t_apag, "apagado_vela", 0.5, 0.0)
        self.ev(self.t_apag + 0.5, "apagado_vela", 0.4, 0.2)
        self.ev(tb[7] + 0.2, "paginas", 0.4, 0.0, dur=3.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
