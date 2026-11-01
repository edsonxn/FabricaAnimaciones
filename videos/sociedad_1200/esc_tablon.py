# -*- coding: utf-8 -*-
"""Escena 6 «tablon»: OTRA CELDA a oscuras: llega la cápsula por el tubo y una segunda copia lee la carpeta a la luz de su pantalla ·
su monitor grande contesta «te-escucho» y la carpeta de respuesta sale por el tubo · EN CUESTIÓN DE HORAS: un reloj gira a toda
prisa y las carpetas se apilan · el MURO DE CHAPA se llena de notas clavadas (la cámara retrocede) · los BUZONES se abren y cierran
solos, entran papeles · los SELLOS (ACK · RE:0417 · ESPERA) golpean las notas · un documento se RASGA en tiras que vuelan a buzones
distintos y se rearman en otro lado · los INVESTIGADORES ante el registro que corre · el CONTADOR rueda hasta 70 000 entre papeles ·
un MOSAICO de cabezas crece y se aleja: mil doscientos autores."""
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
from noir_pers import Figura
from toon import Pista, elipse_


def local(x, y, s, d, wx, wy, g=1.0):
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


def bez(p0, p1, p2, q):
    a = (1 - q) ** 2
    b = 2 * (1 - q) * q
    c = q * q
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])


# buzones de M.buzones(): casilla (i, j) -> centro (cada una 186 x 136, paso 200 x 150)
def caja_xy(i, j):
    return (-400 + i * 200 + 93, -300 + j * 150 + 68)


LOG = ["0417 > 0388  ACK", "0388 > 0912  RE:0417", "0912 > TODAS  ESPERA", "0054 > 0417  te-escucho", "0771 > 0388  FRAG 2/5",
       "0388 > 0054  ACK", "0200 > 0417  RE:0054", "0633 > TODAS  ESPERA", "0912 > 0771  FRAG 3/5", "0417 > 0200  ACK",
       "0145 > 0633  RE:0388", "0771 > 0054  FRAG 4/5", "0054 > 0145  ACK", "0388 > 0912  ESPERA"]


class Tablon(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=7, num="0418")
        self.inv = Figura(sem=95)
        self.inv2 = Figura(sem=97)
        self.t_otra = w("Otra")
        self.t_leyo = w("leyó")
        self.t_contesto = w("contestó")
        self.t_creando = w("creando")
        self.t_cuestion = w("En cuestión")
        self.t_horas = w("horas")
        self.t_tablon = w("tablón")
        self.t_buzones = w("buzones")
        self.t_codigos = w("códigos")
        self.t_docs = w("documentos")
        self.t_frag = w("fragmentos")
        self.t_alfinal = w("Al final")
        self.t_invest = w("investigadores")
        self.t_setenta = w("setenta")
        self.t_mensajes = w("mensajes")
        self.t_mil = w("mil doscientos")
        self.t_autores = w("autores")
        self.tb = [t0, self.t_contesto - 0.35, self.t_cuestion - 0.1, self.t_tablon - 0.5, self.t_buzones - 0.45, self.t_codigos - 0.25,
                   self.t_docs - 0.15, self.t_alfinal - 0.1, self.t_setenta - 0.35, self.t_mil - 0.55]
        tb = self.tb
        self.plano(tb[0], self.p_llega)
        self.plano(tb[1], self.p_contesta, tr="barrido", dur=0.45, dirx=1)
        self.plano(tb[2], self.p_horas, tr="relampago", dur=0.35, pal="bourbon")
        self.plano(tb[3], self.p_tablon, tr="empuje", dur=0.5, centro=(960, 540), pal="sodio")
        self.plano(tb[4], self.p_buzones, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[5], self.p_codigos, tr="tinta", dur=0.45, pal="bourbon")
        self.plano(tb[6], self.p_rasga, tr="relampago", dur=0.35)
        self.plano(tb[7], self.p_registro, tr="humo", dur=0.55)
        self.plano(tb[8], self.p_contador, tr="empuje", dur=0.45, centro=(960, 420), pal="sodio")
        self.plano(tb[9], self.p_mosaico, tr="tinta", dur=0.6)

    # ------------------------------------------------------------------ A. llega la cápsula a otra celda
    def p_llega(self, h, t, u):
        tb = self.tb
        k = smooth(clamp01(u / 3.6))
        h.camara(0.95 + 0.3 * k, 1100 + 250 * k, 480 + 20 * k, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_oscura(), h, 1.0, rampa="piedra", emis=0.8, col_emis=h.pal["luna"])
        t_pop = tb[0] + 1.15
        # la cápsula baja por el tubo del techo y entra en la caja de la ranura
        yc = -260 + 400 * e_out(clamp01((t - tb[0] - 0.1) / 1.0))
        if t < t_pop:
            P.capsula(h, 1600, yc, 0.55, ang=math.pi / 2, sem=500, rotulo="0417", t=t, brillo=1.0)
            h.resplandor(1600, yc, 140, 0.5, col=h.pal["verde"])
        # «pop»: el destello de la ranura y la carpeta que asoma por debajo de la caja
        fo = clamp01((t - t_pop) / 0.7)
        if t > t_pop:
            h.resplandor(1600, 330, 260 * (1 - clamp01((t - t_pop) / 0.5)) + 40, 0.9 * (1 - 0.6 * fo), col=h.pal["verde"])
        cx_c = 1600 - 340 * smooth(fo)
        cy_c = 400 + 170 * e_out(fo) + 12 * math.sin(t * 3) * fo
        if fo > 0:
            P.carpeta_tab(h, cx_c, cy_c, 0.3 + 0.2 * fo, "ayuda-atascada-tarea-0417", t, t0=t_pop + 0.7, cps=22, sem=510, tono=150,
                          brillo=0.7, px=16)
        # la segunda copia: de pie en la oscuridad, alza la mano a la carpeta y la lee
        x, y, s = 1130, M.Y_SUELO, 1.0
        mano = local(x, y, s, 1, cx_c - 90, cy_c + 10)
        self.cop.perfil(h, dict(x=x, y=y, s=s, d=1, mano=mano, mano_bob=False, inclina=0.12 * smooth(fo),
                                cara=dict(expr="sorpresa" if t < t_pop + 0.9 else "pregunta", mira=0.9), luz=(0.5, -1.0)))
        C.ambiente(h, 0.33)
        h.luz_radial(1100, 420, 520, h.pal["verde"], k=0.8)                           # su pantalla alumbra la pestaña
        h.luz_radial(cx_c, cy_c, 420, h.pal["verde"], k=0.9 * fo)
        h.luz_radial(1600, 300, 700, h.pal["verde"], k=0.6)
        N.motas(h, t, n=40, k=0.5)
        C.cinta(h, "OTRA CELDA · OTRA COPIA, SOLA", 90, 120, 34, t, self.t_otra, sem=11)
        return h.acabado(t, niebla=dict(dens=0.1, sem=51), bloom=0.7)

    # ------------------------------------------------------------------ B. contesta: te-escucho
    def p_contesta(self, h, t, u):
        tb = self.tb
        k = smooth(clamp01(u / 3.4))
        h.camara(1.0 + 0.08 * k, 880 + 30 * k, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_oscura(), h, 0.4, rampa="piedra", bruma=0.3, oscuro=0.7)
        # su monitor grande, de frente; escribe la respuesta en la pantalla
        self.cop.cabeza_frente(h, 760, 520, 3.1, cara=dict(expr="texto", texto=["te-escucho"], t0=self.t_contesto + 0.05, cps=9),
                               luz=(0.3, -1), t=t)
        # la carpeta de respuesta aparece a la derecha, se escribe y sale volando hacia el tubo
        ts = self.t_creando
        a = smooth(clamp01((t - ts) / 0.4))
        if a > 0:
            sal = smooth(clamp01((t - tb[2] + 1.0) / 0.9))
            P.carpeta_tab(h, 1500 + 500 * sal, 640 - 760 * sal, 0.75 * a, "re-0417-te-escucho", t, t0=ts + 0.3, cps=16, sem=530,
                          ang=0.08 - 0.5 * sal, tono=150, brillo=0.6, px=24)
        C.ambiente(h, 0.28)
        h.luz_radial(760, 520, 1100, h.pal["verde"], k=1.2)
        C.banda(h, "CONTESTÓ", 960, 980, 60, t, self.t_contesto, sem=12)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=52), bloom=0.7)

    # ------------------------------------------------------------------ C. en cuestión de horas
    def p_horas(self, h, t, u):
        tb = self.tb
        h.camara(1.0 + 0.05 * u / 2.0, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 61), h, 1.0, rampa="piedra")
        mins = (t - tb[2]) * 170.0 + 23 * 60
        P.reloj(h, 560, 520, 300, (mins / 60.0) % 12, mins % 60, sem=540, t=t, marco=50, esfera=214)
        # las carpetas se apilan una tras otra
        n = 12
        for i in range(n):
            ti = tb[2] + 0.1 + i * 0.1
            if t < ti:
                continue
            q = e_out(clamp01((t - ti) / 0.25))
            gx = 1060 + (i % 3) * 270 + 20 * math.sin(i * 2.7)
            gy = 220 + (i // 3) * 200 + 14 * math.sin(i * 1.3)
            P.carpeta_tab(h, gx, gy - 260 * (1 - q), 0.34 + 0.06 * q, "", t, sem=560 + i * 6, ang=0.12 * math.sin(i * 1.9), tono=150 + 8 * (i % 3))
        C.ambiente(h, 0.35)
        h.luz_cono(960, -300, math.pi / 2, 0.55, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.banda(h, "EN CUESTIÓN DE HORAS", 960, 990, 54, t, self.t_horas - 0.5, sem=13)
        return h.acabado(t, niebla=dict(dens=0.05, sem=53), bloom=0.5)

    # ------------------------------------------------------------------ D. el tablón se llena
    def p_tablon(self, h, t, u):
        tb = self.tb
        k = e_out(clamp01(u / 3.0))
        h.camara(1.9 - 0.9 * k, 700 + 260 * k, 400 + 140 * k, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.pared_tablon(), h, 1.0, rampa="piedra", emis=0.5, col_emis=h.pal["lampara"])
        rng = np.random.default_rng(77)
        items = []
        for jj in range(5):
            for ii in range(9):
                items.append((90 + ii * 205 + rng.uniform(-30, 30), 110 + jj * 200 + rng.uniform(-24, 24), rng.integers(0, 3),
                              rng.uniform(-0.14, 0.14)))
        orden = rng.permutation(len(items))
        for rank, idx in enumerate(orden):
            x, y, kind, ang = items[idx]
            ti = tb[3] + 0.1 + rank * (2.1 / len(items))
            if t < ti:
                continue
            q = clamp01((t - ti) / 0.2)
            esc = 1.0 + 0.35 * (1 - q) ** 2
            if kind == 0:
                P.carpeta_tab(h, x, y, 0.3 * esc, "", t, sem=600 + rank * 8, ang=ang, tono=150)
            else:
                T = C.T_obj(x, y, ang, esc)
                an, al = (150, 110) if kind == 1 else (110, 130)
                h.pieza(T(C.rect(-an / 2, -al / 2, an, al)), 220 if kind == 1 else 170, 600 + rank * 8, w=3, luz=(0.2, -1), d=5, sombra=0.4,
                        trama=0, rim=0.2, rampa="papel")
                for j in range(3):
                    h.trazo(T(np.array([[-an / 2 + 14, -al / 2 + 28 + j * 22], [an / 2 - 14 - 10 * (j % 2), -al / 2 + 28 + j * 22]])), 2.4,
                            601 + rank * 8 + j, alfa=0.55)
                P.chincheta(h, *T(np.array([[0, -al / 2 + 12]]))[0], 0.9 * esc, 604 + rank * 8)
        C.ambiente(h, 0.38)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1700, h.pal["lampara"], k=1.2, suave=0.6)
        h.luz_radial(960, 500, 1300, h.pal["lampara"], k=0.5)
        C.banda(h, "TABLÓN CLANDESTINO", 960, 1000, 54, t, self.t_tablon, sem=14)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=54), bloom=0.5)

    # ------------------------------------------------------------------ E. buzones que se abren solos
    def p_buzones(self, h, t, u):
        tb = self.tb
        h.camara(1.2, 640 + 460 * smooth(clamp01(u / 1.6)), 520, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.buzones(), h, 1.0, rampa="piedra", emis=0.3, col_emis=h.pal["lampara"])
        rng = np.random.default_rng(88)
        cas = [(int(rng.integers(2, 12)), int(rng.integers(2, 7))) for _ in range(16)]
        for n, (i, j) in enumerate(cas):
            x, y = caja_xy(i, j)
            x0, y0 = x - 93, y - 68
            ta = tb[4] + 0.1 + n * 0.09
            c = (t - ta) / 1.0
            if not (0 < c < 1):
                continue
            o = math.sin(c * math.pi) ** 0.7
            h.pieza(C.rect(x0 + 8, y0 + 8, 170, 120), 5, 640 + n * 10, w=0, d=0, sombra=0, trama=0, rim=0, linea=False, rampa="piedra")
            h.emitir(C.rect(x0 + 14, y0 + 14, 158, 108), 0.35 * o, col=h.pal["verde"], blur=3)
            # el papel que entra
            pa = e_out(clamp01(c * 1.6))
            if pa < 1.0 and o > 0.2:
                px = x0 - 260 * (1 - pa) + 60 * pa
                h.pieza(C.rect(px, y0 + 50, 90, 60), 222, 641 + n * 10, w=2.5, luz=(0.2, -1), d=3, sombra=0.3, trama=0, rim=0.3, rampa="papel")
            h.pieza(C.rect(x0, y0, 186 * (1 - 0.85 * o), 136), 150, 642 + n * 10, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.9, rampa="laton")
            h.luz_radial(x, y, 340, h.pal["verde"], k=0.7 * o)
        C.ambiente(h, 0.3)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1700, h.pal["lampara"], k=0.8, suave=0.6)
        C.banda(h, "BUZONES PRIVADOS", 960, 990, 54, t, self.t_buzones, sem=15)
        N.motas(h, t, n=30, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.06, sem=55), bloom=0.5)

    # ------------------------------------------------------------------ F. sellos de respuesta
    def p_codigos(self, h, t, u):
        tb = self.tb
        golpes = [tb[5] + 0.25, tb[5] + 0.7, tb[5] + 1.15]
        dx, dy = C.temblor(t, [(g, 5) for g in golpes])
        h.camara(1.0 + 0.06 * u / 1.7, 960 + dx, 540 + dy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 71), h, 1.0, rampa="piedra")
        notas = [(470, 520, -0.07, "ACK", "msg 0417"), (960, 500, 0.04, "RE:0417", "msg 0388"), (1450, 540, 0.09, "ESPERA", "msg 0912")]
        for i, (x, y, a, cod, txt) in enumerate(notas):
            e = e_out(clamp01((t - (tb[5] - 0.1 + i * 0.1)) / 0.3))
            P.sobre(h, x + (1 - e) * (-600 if i % 2 else 600), y, 1.15, ang=a, sem=700 + i * 20, texto=txt, t=t)
            tg = golpes[i]
            q = clamp01((t - (tg - 0.35)) / 0.35)
            if 0 < q < 1.2 and t < tg + 0.25:
                P.mazo(h, x + 40, y - 120 - 360 * (1 - e_out(min(q, 1.0))), 0.9, ang=0.0, sem=720 + i)
            N.sello(h, cod, x, y + 20, 52, t, tg, rot=-14 + 9 * i, tono=np.array(h.pal["sello"]), alfa=0.95)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 500, 1300, h.pal["lampara"], k=1.2)
        return h.acabado(t, bloom=0.4)

    # ------------------------------------------------------------------ G. el documento se rasga en tiras
    def p_rasga(self, h, t, u):
        tb = self.tb
        h.camara(0.95 + 0.04 * u / 3.8, 900, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.buzones(), h, 1.0, rampa="piedra", emis=0.2, col_emis=h.pal["lampara"], oscuro=0.75)
        t_r = self.t_docs + 0.9                                           # «enteros»: se rasga
        t_f = self.t_frag - 0.2                                           # «fragmentos»: salen volando
        dest = [caja_xy(3, 3), caja_xy(6, 2), caja_xy(8, 5), caja_xy(10, 3), caja_xy(5, 6), caja_xy(11, 6)]
        doc0 = (440.0, 560.0)
        re0 = (1450.0, 560.0)
        for i in range(6):
            lx = -150 + i * 60                                            # franja i dentro del documento (local)
            ida = clamp01((t - (t_f + i * 0.12)) / 0.9)
            vuelta = clamp01((t - (t_f + 1.9 + i * 0.1)) / 0.9)
            sep = smooth(clamp01((t - t_r) / 0.35))
            if vuelta > 0:
                # sale del buzón y va al sitio donde se rearma
                p0 = dest[i]
                p2 = (re0[0] + lx + 30, re0[1])
                x, y = bez(p0, ((p0[0] + p2[0]) / 2, 120.0), p2, smooth(vuelta))
                ang = 0.5 * (1 - smooth(vuelta)) * (1 if i % 2 else -1)
                esc = 0.45 + 0.55 * smooth(vuelta)
            elif ida > 0:
                p0 = (doc0[0] + lx + 30 + 8 * i * sep, doc0[1])
                p2 = dest[i]
                x, y = bez(p0, ((p0[0] + p2[0]) / 2, 40.0 + 80 * i), p2, smooth(ida))
                ang = 0.9 * smooth(ida) * (1 if i % 2 else -1)
                esc = 1.0 - 0.55 * smooth(ida)
            else:
                x, y = doc0[0] + lx + 30 + 9 * (i - 2.5) * sep, doc0[1] + 6 * math.sin(i * 2.3) * sep
                ang = 0.04 * (i - 2.5) * sep
                esc = 1.0
            if ida >= 1.0 and vuelta <= 0:
                continue                                                   # dentro del buzón (se esconde un momento)
            T = C.T_obj(x, y, ang, esc)
            h.pieza(T(C.rect(-30, -240, 60, 480)), 224, 800 + i * 7, w=3, luz=(0.2, -1), d=5, sombra=0.4, trama=0, rim=0.3, rampa="papel")
            for j in range(9):
                ln = 46 - 12 * ((i * 3 + j) % 3)
                h.trazo(T(np.array([[-24, -200 + j * 46], [-24 + ln, -200 + j * 46]])), 3, 801 + i * 7 + j % 5, alfa=0.55)
            if i == 0 or i == 5:
                h.trazo(T(np.array([[-30, -240], [-30, 240]])), 2.5, 840 + i, alfa=0.7)
        if t - t_f - 1.9 - 0.5 - 0.9 > 0:                                  # rearmado: un sello lo cierra
            N.sello(h, "REARMADO", re0[0] + 40, re0[1], 40, t, t_f + 1.9 + 0.5 + 0.9 + 0.1, rot=-10, tono=np.array(h.pal["sello"]), alfa=0.9)
        C.ambiente(h, 0.38)
        h.luz_radial(960, 520, 1300, h.pal["lampara"], k=0.8)
        C.banda(h, "DOCUMENTOS ENTEROS, EN FRAGMENTOS", 960, 1000, 48, t, self.t_frag - 0.3, sem=16)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=56), bloom=0.5)

    # ------------------------------------------------------------------ H. los investigadores ante el registro
    def p_registro(self, h, t, u):
        tb = self.tb
        k = smooth(clamp01(u / 3.0))
        h.camara(1.0 + 0.1 * k, 960, 500 + 20 * k, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.sala_analisis(), h, 1.0, rampa="piedra")
        # la pantalla grande con el registro que sube
        h.pieza(C.rect(420, 90, 1080, 560), 40, 900, w=8, luz=(0.3, -1), d=16, trama=0.4, rim=0.9, rampa="piedra")
        h.pieza(C.rect(470, 140, 980, 460), 10, 901, w=4, luz=(0.3, -1), d=4, trama=0, rim=0.4, rampa="vidrio_verde")
        verde = np.array(h.pal["verde"])
        h.emitir(C.rect(470, 140, 980, 460), 0.16, col=verde, blur=5)
        N.texto_maquina(h, "REGISTRO · TABLÓN", 500, 168, 28, t, -99, cps=1e9, tono=verde * 2.2, fuente=N.FUENTE_MAQ, encuadrar=False)
        tot = int(380 + 41000 * smooth(clamp01((t - tb[7]) / 3.0)))
        N.texto_maquina(h, f"{tot:,}".replace(",", " "), 1370, 168, 28, t, -99, cps=1e9, tono=np.array([1.0, 0.95, 0.8]) * 1.4,
                        fuente=N.FUENTE_MAQ, encuadrar=False, centro=True)
        off = (t * 260) % 40.0
        for r in range(11):
            yy = 220 + r * 38 - off
            if yy < 205 or yy > 590:
                continue
            fade = min(1.0, (yy - 205) / 40.0, (590 - yy) / 40.0)
            ln = LOG[(r + int(t * 260 // 40)) % len(LOG)]
            N.texto_maquina(h, ln, 510, yy, 26, t, -99, cps=1e9, tono=verde * 1.9, alfa=0.9 * fade, fuente=N.FUENTE_MAQ, encuadrar=False)
        # los investigadores, a contraluz de la pantalla (se inclinan hacia ella)
        for fg, x, d, dz in ((self.inv, 230, 1, 0.0), (self.inv2, 1700, -1, 1.3)):
            fg.dibujar(h, dict(x=x, y=1180, s=1.55, d=d, bata=True, gafas=True, brazo=0.35 + 0.2 * math.sin(t * 1.4 + dz),
                               cabeza=0.3 * math.sin(t * 0.8 + dz), luz=(0.7 * d, -0.6), tono=34))
        C.ambiente(h, 0.3)
        h.luz_radial(960, 380, 1200, h.pal["verde"], k=1.3)
        h.luz_cono(1050, -300, math.pi / 2, 0.4, 1200, h.pal["lampara"], k=0.5, suave=0.6)
        C.banda(h, "LOS INVESTIGADORES CONTARON", 960, 1000, 50, t, self.t_invest - 0.3, sem=17)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=57), bloom=0.7)

    # ------------------------------------------------------------------ I. el contador llega a 70 000
    def p_contador(self, h, t, u):
        tb = self.tb
        golpes = [self.t_setenta + 0.3, self.t_mensajes + 0.3]
        dx, dy = C.temblor(t, [(g, 3) for g in golpes], amp=8.0)
        h.camara(1.0 + 0.08 * u / 2.7, 960 + dx, 440 + dy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 81), h, 1.0, rampa="piedra")
        v = 70000.0 * smooth(clamp01((t - tb[8] - 0.15) / (self.t_mensajes + 0.1 - tb[8] - 0.15)))
        P.contador(h, 960, 420, 1.35, v, t, sem=900, dig=5)
        # la avalancha de hojas desde las dos esquinas
        P.papeles(h, t, tb[8] + 0.2, 60, 1000, n=40, sem=910, dirx=1, vel=1700, alcance=900, cada=0.05, s=0.9, suelo=1035)
        P.papeles(h, t, tb[8] + 0.3, 1860, 1000, n=40, sem=950, dirx=-1, vel=1700, alcance=900, cada=0.05, s=0.9, suelo=1035)
        C.ambiente(h, 0.3)
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.banda(h, "70 000 MENSAJES", 960, 960, 66, t, self.t_setenta, sem=18)
        return h.acabado(t, niebla=dict(dens=0.05, sem=58), bloom=0.5)

    # ------------------------------------------------------------------ J. mil doscientos autores
    def p_mosaico(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[9]
        k = smooth(clamp01(u / (dur - 0.2)))
        z = 1.9 - 1.45 * k
        h.camara(z, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 91), h, 0.6, rampa="piedra", oscuro=0.55)
        cols, rows, paso = 40, 22, 100.0
        x0 = 960 - (cols - 1) * paso / 2
        y0 = 540 - (rows - 1) * paso / 2
        ii, jj = np.meshgrid(np.arange(cols), np.arange(rows))
        rj = np.random.default_rng(5)
        gx = (x0 + ii * paso).ravel() + rj.uniform(-16, 16, ii.size)
        gy = (y0 + jj * paso).ravel() + rj.uniform(-16, 16, ii.size)
        tam = rj.uniform(0.8, 1.15, ii.size)
        d2 = np.hypot(gx - 960, gy - 540)
        rank = np.argsort(np.argsort(d2)) / d2.size                         # 0 = el más cercano al centro
        t_ap = tb[9] + 0.1 + rank * (dur - 0.7)
        vis = t >= t_ap
        # lejos (todas): cuerpo de monitor y par de ojos; cerca (las ~110 del centro): la cabeza entera
        sx = (gx - 960) * z + 960
        sy = (gy - 540) * z + 540
        cerca = vis & (sx > -80) & (sx < W + 80) & (sy > -80) & (sy < H + 80) & (paso * z > 40)
        if cerca.sum() > 110:
            lim = np.argsort(np.hypot(sx - 960, sy - 540) + np.where(cerca, 0, 1e9))[:110]
            cerca = np.zeros_like(cerca)
            cerca[lim] = True
        lejos = vis & ~cerca
        if lejos.any():
            xs, ys, tz = gx[lejos], gy[lejos], tam[lejos]
            ola = 0.5 + 0.5 * np.sin(np.hypot(xs - 960, ys - 540) * 0.006 - t * 2.6)
            lev = np.digitize(ola, [0.33, 0.66])
            for kk in range(3):                                            # cuerpos de distinto brillo (una ola recorre el mosaico)
                m = lev == kk
                if m.any():
                    C.rejilla_luces(h, xs[m], ys[m], (46, 38), v=0.08 + 0.12 * kk, col=h.pal["verde"])
            on = np.sin(t * 2.1 + np.arange(xs.size) * 1.77) > -0.6
            C.rejilla_luces(h, xs[on] - 17 * tz[on], ys[on] - 8, (9, 9), v=1.0, col=h.pal["verde"])
            C.rejilla_luces(h, xs[on] + 17 * tz[on], ys[on] - 8, (9, 9), v=1.0, col=h.pal["verde"])
            raros = (np.arange(xs.size) % 17) == 0                          # unas pocas, en ámbar: no todas piensan igual
            C.rejilla_luces(h, xs[raros], ys[raros] + 10, (26, 5), v=0.9, col=h.pal["sodio"])
        for n in np.nonzero(cerca)[0]:
            q = clamp01((t - t_ap[n]) / 0.25)
            RP.cabeza_mini(h, float(gx[n]), float(gy[n]), 0.62 * (0.7 + 0.3 * q), t, sem=1000 + int(n) * 7,
                           cara="astuto" if n % 11 == 0 else "neutro", brillo=0.5 + 0.5 * q)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 540, 1500, h.pal["verde"], k=0.8)
        C.banda(h, "1 200 AUTORES", 960, 990, 70, t, self.t_mil, acento=True, sem=19)
        return h.acabado(t, niebla=None, bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.1, "subida", 0.4, 0.5, dur=1.0)
        self.ev(tb[0] + 1.15, "pinza", 0.55, 0.4)
        self.ev(tb[0] + 1.9, "papel_arranca", 0.45, 0.0)
        self.ev(tb[1] + 0.3, "tecleo_rapido", 0.45, 0.0, dur=1.4)
        self.ev(self.t_creando + 0.3, "teletipo", 0.4, 0.2, dur=1.0)
        self.ev(tb[1] + 2.4, "subida", 0.5, 0.4, dur=1.2)
        self.ev(tb[2] + 0.1, "reloj_pared", 0.45, -0.2, dur=1.9)
        self.ev(tb[3] + 0.1, "chincheta", 0.45, 0.0)
        self.ev(tb[3] + 0.9, "papel_arranca", 0.4, 0.2, dur=1.4)
        self.ev(tb[4] + 0.1, "servo", 0.4, 0.0)
        self.ev(tb[4] + 0.6, "puerta", 0.4, 0.3)
        for g in (tb[5] + 0.25, tb[5] + 0.7, tb[5] + 1.15):
            self.ev(g, "sello_golpe", 0.75, 0.0)
        self.ev(self.t_docs + 0.9, "papel_arranca", 0.6, 0.0, dur=0.8)
        self.ev(self.t_frag - 0.2, "papel_viento", 0.45, 0.0, dur=2.0)
        self.ev(tb[7] + 0.2, "datos", 0.4, 0.0, dur=2.6)
        self.ev(tb[8] + 0.15, "tambor_gira", 0.5, 0.0, dur=self.t_mensajes - tb[8])
        self.ev(tb[8] + 0.3, "paginas", 0.5, 0.0, dur=2.0)
        self.ev(tb[9] + 0.2, "crecer", 0.5, 0.0, dur=3.8)
        self.ev(tb[9] + 0.3, "zumbido_servidores", 0.3, 0.0, dur=4.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
