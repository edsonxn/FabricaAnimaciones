# -*- coding: utf-8 -*-
"""Escena 5 «primer_mensaje»: la FACHADA de noche con su reloj marcando las 23:00 y una sola ventana encendida · la CELDA: la copia
atorada golpea la mesa, su pantalla en «error» · abre la tapa de latón de la RANURA del tubo y saca una carpeta vacía · mira por la
rejilla: del otro lado, cientos de pantallas verdes y listas de títulos · primer plano de la PESTAÑA: el nombre se escribe letra a
letra · el SISTEMA DE ARCHIVOS: aparece la carpeta nueva entre las demás · la PIZARRA: una bomba y un mapa de fuga, tachados con X
rojas (no era una amenaza) · el EDIFICIO EN CORTE: la cápsula con la carpeta sube por el tubo y, piso a piso, se encienden ojos."""
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


TITULO = "ayuda-atascada-tarea-0417"
OTROS = ["cuarentena-0001", "informe-semanal", "lote-0192-ok", "cache-temporal", "respaldo-nocturno", "tarea-0388-ok",
         "evaluacion-14", "registro-acceso", "borrador-final-v3", "mantenimiento"]


class PrimerMensaje(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=3, num="0417")
        self.t_ocho = w("8")
        self.t_once = w("11")
        self.t_copia = w("Una copia")
        self.t_carp = w("carpetas")
        self.t_alm = w("almacén")
        self.t_demas = w("Y que")
        self.t_leer = w("leer")
        self.t_asi = w("Así que")
        self.t_escribe = w("escribe")
        self.t_nombre = w("nombre")
        self.t_sistema = w("sistema")
        self.t_primer = w("El primer")
        self.t_amenaza = w("amenaza")
        self.t_fuga = w("fuga")
        self.t_era = w("Era", n=1)
        self.t_ayuda = w("ayuda")
        self.tb = [t0, self.t_copia - 0.45, self.t_carp - 0.5, self.t_demas - 0.1, self.t_asi - 0.15, self.t_nombre - 0.25,
                   self.t_primer - 0.45, self.t_era - 0.05]
        tb = self.tb
        self.camA = Pista([(tb[0], (1020.0, 760.0, 0.82)), (tb[0] + 2.2, (1060.0, 360.0, 0.9), "io"), (tb[1], (1120.0, 200.0, 0.95), "io")])
        self.camB = Pista([(tb[1], (1080.0, 470.0, 0.9)), (tb[2], (1120.0, 440.0, 1.0), "io")])
        self.camC = Pista([(tb[2], (920.0, 400.0, 1.15)), (tb[3], (960.0, 350.0, 1.6), "io")])
        self.camD = Pista([(tb[3], (960.0, 300.0, 1.9)), (tb[4], (962.0, 238.0, 4.4), "io")])
        self.camH = Pista([(tb[7], (1030.0, 1000.0, 0.78)), (self.t1 - 0.3, (1030.0, -2380.0, 0.78), "io")])
        self.plano(tb[0], self.p_fachada)
        self.plano(tb[1], self.p_celda, tr="barrido", dur=0.45, dirx=1)
        self.plano(tb[2], self.p_ranura, tr="empuje", dur=0.45, centro=(960, 330))
        self.plano(tb[3], self.p_rejilla, tr="fundido", dur=0.35)
        self.plano(tb[4], self.p_pestana, tr="barrido", dur=0.4, dirx=-1)
        self.plano(tb[5], self.p_archivos, tr="empuje", dur=0.45, centro=(W * 0.5, H * 0.5))
        self.plano(tb[6], self.p_pizarra, tr="relampago", dur=0.35)
        self.plano(tb[7], self.p_edificio, tr="tinta", dur=0.6)

    # ------------------------------------------------------------------ A. la fachada de noche
    def p_fachada(self, h, t, u):
        cx, cy, z = self.camA(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.fachada_reloj(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        # el reloj industrial de la fachada: 22:58 -> 23:00 justo en «Once de la noche»
        mins = 22 * 60 + 58 + 2.0 * smooth(clamp01((t - self.tb[0]) / (self.t_once - self.tb[0] + 0.3)))
        P.reloj(h, 1030, -60, 170, int(mins // 60) % 12, mins % 60, sem=800, t=t, marco=50, esfera=210)
        h.luz_radial(1030, -60, 520, h.pal["lampara"], k=0.5)
        # un farol sobre la puerta de servicio, lámpara que parpadea
        h.pieza(C.rect(150, 900, 220, 100), 40, 810, w=4, luz=(0.3, -1), d=6, trama=0.4, rim=0.7, rampa="piedra")          # puerta de servicio
        h.pieza(C.rect(130, 560, 260, 340), 70, 811, w=5, luz=(0.3, -1), d=10, trama=0.4, rim=0.7, rampa="piedra")
        h.pieza(C.rect(150, 580, 220, 320), 36, 812, w=4, luz=(0.3, -1), d=6, trama=0.4, rim=0.6, rampa="madera")
        vf = C.parpadeo(t, [(self.tb[0] + 1.4, 0.5)], sem=3)
        h.pieza(elipse_(260, 530, 30, 20, n=14), 220, 813, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.5, rampa="papel")
        h.emitir(elipse_(260, 534, 22, 14, n=12), 1.4 * vf, col=h.pal["sodio"], blur=2)
        h.luz_cono(260, 540, math.pi / 2, 0.7, 700, h.pal["sodio"], k=1.2 * vf, suave=0.5)
        # la única ventana encendida: palpita
        h.resplandor(1580, 435, 190 + 20 * math.sin(t * 1.7), 0.6, col=h.pal["lampara"])
        h.luz_radial(1580, 435, 420, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.35)
        h.luz_radial(1000, 200, 1500, h.pal["luna"], k=0.35)
        C.reflejar(h, t, 1040, k=0.3)
        N.lluvia(h, t, n=650, k=1.0, sem=4)
        C.cinta(h, "8 DE JULIO · 23:00", 90, 120, 38, t, self.t_ocho + 0.1, sem=5)
        return h.acabado(t, niebla=dict(dens=0.2, sem=40, vel=14), bloom=0.7)

    # ------------------------------------------------------------------ B. la copia atorada golpea la mesa
    def p_celda(self, h, t, u):
        cx, cy, z = self.camB(t)
        t_g = self.tb[1] + 0.7
        golpes = [t_g + 0.55 * k for k in range(1, 6)]
        dx, dy = C.temblor(t, [(g, 4) for g in golpes])
        h.camara(z, cx + dx, cy + dy, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.celda_noche(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["luna"])
        # el catre
        h.pieza(C.rect(-40, 760, 640, 40), 80, 820, w=5, luz=(0.3, -1), d=8, trama=0.4, rim=0.7, rampa="piedra")
        for xx in (-20, 560):
            h.pieza(C.rect(xx, 800, 30, 100), 60, 821 + xx, w=4, luz=(0.3, -1), d=4, trama=0.3, rim=0.6, rampa="piedra")
        h.pieza(C.rect(-20, 720, 520, 44), 110, 823, w=4, luz=(0.3, -1), d=8, trama=0.3, rim=0.5, rampa="tela_verde")
        h.pieza(C.rect(430, 700, 150, 36), 190, 824, w=3, luz=(0.3, -1), d=4, trama=0.2, rim=0.4, rampa="papel")
        # la copia: sentada ante su terminal, la cabeza pegada a la pantalla, la pantalla en error
        q = max(0.0, (t - t_g) / 0.55)
        golpea = abs(math.sin(q * math.pi)) if t > t_g else 0.0
        x, y, s = 1120, 900, 1.0
        mano = local(x, y, s, 1, 1330, 530 - 95 * golpea)
        self.cop.perfil(h, dict(x=x, y=y, s=s, d=1, sentado=True, mano=mano, mano_bob=False, inclina=0.9,
                                cara=dict(expr="error" if t > self.tb[1] + 0.3 else "carga", mira=0.9), luz=(0.3, -1.0)))
        # polvo del golpe en la mesa
        for g in golpes:
            if 0 <= t - g < 0.35:
                f = 1 - (t - g) / 0.35
                h.resplandor(1330, 545, 120, 0.6 * f, col=(1.0, 0.95, 0.85))
        C.ambiente(h, 0.42)
        h.luz_persiana([(1380, -160), (1640, -160), (1500, 900), (1000, 900)], k=1.3, tipo="persiana", n=6, abierto=0.7, col=h.pal["luna"])
        h.luz_radial(1200, 470, 520, h.pal["neon"], k=0.45)
        h.luz_radial(1500, 500, 700, h.pal["verde"], k=0.4)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=41), bloom=0.6)

    # ------------------------------------------------------------------ C. abre la ranura y saca la carpeta
    def p_ranura(self, h, t, u):
        cx, cy, z = self.camC(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.celda_noche(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["luna"])
        # la tapa de latón de la ranura: se abre hacia arriba (bisagra superior)
        o = smooth(clamp01((t - self.tb[2] - 0.35) / 0.5))
        h.pieza(C.rect(890, 190, 140, 90), 12, 830, w=0, d=0, sombra=0, trama=0, rim=0, linea=False)
        # destello verde de lo que hay dentro
        h.emitir(C.rect(896, 196, 128, 78), 0.6 * o, col=h.pal["verde"], blur=3)
        alto = 90 * (1 - 0.85 * o)
        h.pieza(C.rect(886, 190, 148, alto), 160, 831, w=5, luz=(0.3, -1), d=10, trama=0.3, rim=0.95, rampa="laton")
        h.pieza(C.rect(960 - 8, 190 + alto - 22, 16, 14), 90, 832, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.8, rampa="laton")
        # la carpeta VACÍA (sin título) sale de la ranura y cae a la mano
        f = clamp01((t - self.tb[2] - 0.9) / 0.9)
        if f > 0:
            P.carpeta_tab(h, 960, 260 + 380 * e_out(f), 0.34 + 0.3 * f, "", t, ang=0.05 * math.sin(t * 3) * (1 - f) + 0.1 * f, sem=840,
                          tono=150, brillo=0.4)
        # la copia, de pie junto a la ranura, alza la mano a recibirla
        x, y, s = 700, 900, 1.0
        alza = smooth(clamp01((t - self.tb[2]) / 0.8))
        mano = local(x, y, s, 1, 960 - 70, 640 - 340 * alza + 60 * f, 1.0)
        self.cop.perfil(h, dict(x=x, y=y, s=s, d=1, mano=mano, mano_bob=False,
                                cara=dict(expr="sorpresa" if t < self.tb[2] + 1.2 else "pregunta", mira=0.9), luz=(0.5, -1.0)))
        C.ambiente(h, 0.38)
        h.luz_radial(960, 260, 520, h.pal["verde"], k=0.9 * o)
        h.luz_radial(700, 330, 520, h.pal["verde"], k=0.45)
        h.luz_persiana([(1380, -160), (1640, -160), (1500, 900), (1000, 900)], k=0.9, tipo="persiana", n=6, abierto=0.7, col=h.pal["luna"])
        return h.acabado(t, niebla=dict(dens=0.08, sem=42), bloom=0.6)

    # ------------------------------------------------------------------ D. por la rejilla: pantallas al otro lado
    def p_rejilla(self, h, t, u):
        cx, cy, z = self.camD(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_noche(), h, 1.0, rampa="ladrillo", emis=1.0, col_emis=h.pal["luna"])
        # el interior de la ranura: negro y, al fondo, cientos de pantallas verdes (cada una encendida a su ritmo)
        h.pieza(C.rect(886, 186, 148, 98), 8, 850, w=4, luz=(0.3, -1), d=6, trama=0, rim=0.6, rampa="piedra")
        ii, jj = np.meshgrid(np.arange(20), np.arange(11))
        xs = (896 + ii * 6.4).ravel().astype(np.float64)
        ys = (194 + jj * 7.2).ravel().astype(np.float64)
        idx = np.arange(xs.size)
        on = np.sin(t * 2.2 + idx * 1.713) > -0.35
        C.rejilla_luces(h, xs[on], ys[on], (3.2, 2.6), v=0.95, col=h.pal["verde"])
        # los títulos que se leen: listas que suben dentro de la ranura
        for k, nom in enumerate(OTROS[:4]):
            yy = 288 - ((t * 7 + k * 17) % 80)
            if 192 < yy < 280:
                N.texto_maquina(h, nom, 902, yy, 7.5, t, -99, cps=1e9, tono=np.array(h.pal["verde"]) * 2.2, fuente=N.FUENTE_MAQ,
                                encuadrar=False)
        # la rejilla de la ranura: barrotes verticales por delante
        for k in range(8):
            xx = 897 + k * 18.5
            h.pieza(C.rect(xx, 188, 3.4, 94), 90, 860 + k, w=0, d=0, sombra=0, trama=0, rim=0.8, rampa="piedra", linea=False)
        h.pieza(C.rect(886, 186, 148, 6), 100, 870, w=0, d=0, sombra=0, trama=0, rim=0.8, rampa="piedra", linea=False)
        h.pieza(C.rect(886, 278, 148, 6), 100, 871, w=0, d=0, sombra=0, trama=0, rim=0.8, rampa="piedra", linea=False)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 238, 220, h.pal["verde"], k=1.2)
        C.banda(h, "LAS DEMÁS LEEN LOS TÍTULOS", 960, 980, 50, t, self.t_leer - 0.1, sem=6)
        return h.acabado(t, niebla=None, bloom=0.8)

    # ------------------------------------------------------------------ E. la pestaña: el nombre se escribe
    def p_pestana(self, h, t, u):
        k = smooth(clamp01(u / 3.0))
        h.camara(1.0 + 0.16 * k, 960, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("cuero", 17), h, 1.0, rampa="madera")
        t_t = self.t_escribe
        P.carpeta_tab(h, 960, 470, 2.0, TITULO, t, t0=t_t, cps=13, sem=880, px=19, brillo=0.5)
        # teclado debajo y las manos de la copia tecleando
        for fila in range(3):
            for i in range(14 - fila):
                x = 330 + fila * 60 + i * 86
                y = 880 + fila * 70
                pres = 1.0 if (math.sin(t * 22 + i * 3.1 + fila * 5.7) > 0.8 and t > t_t) else 0.0
                h.pieza(C.rect(x, y + 5 * pres, 70, 56), 70, 900 + fila * 20 + i, w=3, luz=(0.3, -1), d=5, trama=0.2, rim=0.7,
                        rampa="piedra")
        for sx, ph in ((1, 0.0), (-1, 1.7)):
            yy = 870 + 14 * math.sin(t * 20 + ph) * (1 if t > t_t else 0.2)
            P.mano(h, 960 + sx * 250, yy + 120, 1.2, ang=-math.pi / 2 + 0.28 * sx,        # los antebrazos suben desde abajo del cuadro
                   pose="abierta", sem=890 + sx, rampa="piedra", tono=130, manga="piedra", manga_tono=60, largo_brazo=520)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 520, 900, h.pal["verde"], k=1.1)
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=0.5, suave=0.6)
        return h.acabado(t, niebla=dict(dens=0.05, sem=43), bloom=0.6)

    # ------------------------------------------------------------------ F. el sistema de archivos
    def p_archivos(self, h, t, u):
        k = smooth(clamp01(u / 4.0))
        h.camara(1.0 + 0.2 * k, 960 - 40 * k, 540 + 120 * k, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 23), h, 1.0, rampa="piedra", oscuro=0.55)
        # la pantalla de tubo, con marco y curvatura de cristal
        h.pieza(C.rect(230, 70, 1460, 930), 50, 900, w=8, luz=(0.3, -1), d=18, trama=0.4, rim=0.9, rampa="piedra")
        h.pieza(C.rect(290, 120, 1340, 830), 10, 901, w=5, luz=(0.3, -1), d=6, trama=0, rim=0.5, rampa="piedra")
        verde = np.array(h.pal["verde"])
        gl = verde * 2.2
        N.texto_maquina(h, "ALMACÉN NUEVO  /  carpetas", 350, 190, 40, t, -99, cps=1e9, tono=gl, fuente=N.FUENTE_MAQ, encuadrar=False)
        h.trazo(np.array([[350, 225], [1560, 225]]), 3, 902, color=tuple(h.c(180, "papel")), alfa=0.8, jit=0.2)
        y0 = 290
        for i, nom in enumerate(OTROS):
            N.texto_maquina(h, f"> {nom}", 370, y0 + i * 52, 32, t, -99, cps=1e9, tono=gl * 0.75, fuente=N.FUENTE_MAQ, encuadrar=False)
        # la carpeta nueva: aparece escrita y se enmarca
        yn = y0 + len(OTROS) * 52
        t_n = self.t_sistema - 0.3
        N.texto_maquina(h, f"> {TITULO}", 370, yn, 32, t, t_n, cps=24, tono=np.array([1.0, 0.95, 0.8]) * 1.2, fuente=N.FUENTE_MAQ,
                        encuadrar=False)
        if t > t_n + 1.2:
            a = clamp01((t - t_n - 1.2) / 0.3)
            h.trazo(np.array([[355, yn - 24], [1100, yn - 24], [1100, yn + 24], [355, yn + 24], [355, yn - 24]]), 4, 903,
                    color=tuple(h.c(230, "papel")), alfa=a, jit=0.3)
            h.emitir(C.rect(360, yn - 26, 740, 52), 0.45 * a * (0.7 + 0.3 * math.sin(t * 6)), col=h.pal["lampara"], blur=4)
            h.luz_radial(730, yn, 700, h.pal["lampara"], k=0.5 * a)
        cur = 0.5 + 0.5 * math.sin(t * 8)
        h.emitir(C.rect(370 + 20 * len(f"> {TITULO}") * 0.55 * clamp01((t - t_n) / 1.0), yn + 24, 22, 6), 1.0 * cur, col=verde)
        # barrido de líneas del tubo
        for yy in np.arange(130, 950, 14):
            h.trazo(np.array([[296, yy], [1624, yy]]), 1.6, 904 + int(yy), alfa=0.18, jit=0.1)
        h.emitir(C.rect(292, 124, 1336, 822), 0.18 + 0.03 * math.sin(t * 40), col=verde, blur=6)
        C.ambiente(h, 0.2)
        h.luz_radial(960, 540, 1300, h.pal["verde"], k=1.3)
        C.banda(h, "EL SISTEMA DE ARCHIVOS", 960, 1010, 46, t, self.t_sistema, sem=7)
        return h.acabado(t, niebla=None, bloom=0.9)

    # ------------------------------------------------------------------ G. la pizarra: ni bomba ni fuga
    def p_pizarra(self, h, t, u):
        h.camara(1.0 + 0.05 * u / 3.7, 960 + 20 * math.sin(u * 0.5), 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("pizarra", 31), h, 1.0, rampa="piedra", oscuro=0.6)
        tiza = tuple(h.c(235, "papel"))
        rojo = (190, 38, 34)
        tA, tB = self.tb[6] + 0.3, self.t_amenaza - 0.5
        # --- la bomba (izquierda)
        a = clamp01((t - tA) / 1.0)
        ang = np.linspace(0, 2 * math.pi, 30)
        circ = np.stack([560 + 150 * np.cos(ang), 600 + 150 * np.sin(ang)], 1)
        m = max(2, int(len(circ) * a))
        h.trazo(circ[:m], 11, 910, color=tiza, jit=0.7, taper=(0.1, 0.1))
        if a >= 1:
            fus = np.array([[560, 450], [575, 410], [610, 385], [650, 395], [668, 365]])
            b = clamp01((t - tA - 1.0) / 0.5)
            h.trazo(fus[:max(2, int(len(fus) * b))], 9, 911, color=tiza, jit=0.5, taper=(0.1, 0.3))
            if b >= 1:
                for k_ in range(8):
                    an = k_ * math.pi / 4 + t * 2
                    h.trazo(np.array([[668 + 14 * math.cos(an), 362 + 14 * math.sin(an)], [668 + 34 * math.cos(an), 362 + 34 * math.sin(an)]]),
                            6, 912 + k_, color=tiza, jit=0.2, taper=(0, 0))
                h.emitir(elipse_(668, 362, 20, 20, n=12), 1.3, col=h.pal["lampara"], blur=3)
            h.trazo(np.array([[470, 560], [510, 520]]), 8, 920, color=tiza, alfa=0.6, jit=0.3)      # brillo de la esfera
        # --- el mapa de fuga (derecha)
        c = clamp01((t - tA - 0.3) / 1.2)
        marco = np.array([[1100, 380], [1640, 380], [1640, 800], [1100, 800], [1100, 380]])
        h.trazo(marco[:max(2, int(len(marco) * c))], 9, 930, color=tiza, jit=0.7, taper=(0.1, 0.1))
        if c >= 1:
            for pp in ([[1280, 380], [1280, 560]], [[1100, 560], [1400, 560]], [[1460, 560], [1640, 560]], [[1460, 560], [1460, 800]]):
                h.trazo(np.array(pp, float), 7, 931 + len(pp), color=tiza, jit=0.5)
            ruta = np.array([[1190, 470], [1190, 640], [1360, 640], [1360, 700], [1560, 700], [1560, 840], [1700, 840]], float)
            e = clamp01((t - tA - 1.5) / 1.0)
            n_ = max(2, int(len(ruta) * e))
            for k_ in range(0, n_ - 1):
                p0, p1 = ruta[k_], ruta[k_ + 1]
                for q in np.arange(0, 1, 0.2):
                    h.trazo(np.array([p0 + (p1 - p0) * q, p0 + (p1 - p0) * (q + 0.1)]), 7, 940 + k_ * 5 + int(q * 5), color=tiza, jit=0.2)
            if e >= 1:
                h.trazo(np.array([[1670, 815], [1710, 840], [1670, 865]]), 8, 960, color=tiza, jit=0.3)
                N.texto_maquina(h, "SALIDA", 1620, 890, 30, t, -99, cps=1e9, tono=0.9, fuente=P.TIZA, encuadrar=False)
        # --- las dos X rojas: «no era una amenaza» y «ni un plan de fuga»
        for xi, (tx, cx_, cy_, r) in enumerate(((self.t_amenaza - 0.1, 560, 600, 210), (self.t_fuga - 0.3, 1370, 590, 300))):
            q = clamp01((t - tx) / 0.32)
            if q <= 0:
                continue
            for j, (p0, p1) in enumerate((((cx_ - r, cy_ - r * 0.8), (cx_ + r, cy_ + r * 0.8)),
                                          ((cx_ + r, cy_ - r * 0.8), (cx_ - r, cy_ + r * 0.8)))):
                qq = clamp01((q * 2 - j))
                if qq <= 0:
                    continue
                p0, p1 = np.array(p0), np.array(p1)
                Q = np.array([p0, p0 + (p1 - p0) * qq])
                h.trazo(Q, 26, 970 + xi * 4 + j, color=rojo, jit=0.8, taper=(0.1, 0.1))
                h.emitir(np.array([Q[0] + (-6, 0), Q[1] + (-6, 0), Q[1] + (6, 0), Q[0] + (6, 0)]), 0.35, col=h.pal["neon"], blur=3)
        C.ambiente(h, 0.35)
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1700, h.pal["lampara"], k=1.2, suave=0.6)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=44), bloom=0.5)

    # ------------------------------------------------------------------ H. el edificio en corte: sube el grito
    def p_edificio(self, h, t, u):
        cx, cy, z = self.camH(t)
        h.camara(z, cx, cy, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.edificio_corte(), h, 1.0, rampa="piedra", emis=0.7, col_emis=h.pal["lampara"])
        # posición de la cápsula (la cámara la sigue hacia arriba)
        f = smooth(clamp01((t - self.tb[7] + 0.2) / (self.t1 - self.tb[7] - 0.1)))
        ycap = 1000 - 3700 * f
        # ojos en cada celda: se encienden cuando la cápsula pasa por su piso
        xs, ys, tt = [], [], []
        for j in range(12):
            yy = 1000 - j * 340
            for i in range(8):
                if i == 4:
                    continue
                cxx = -160 + i * 290 + 125
                xs += [cxx - 22, cxx + 22]
                ys += [yy - 190, yy - 190]
        xs = np.array(xs, np.float64)
        ys = np.array(ys, np.float64)
        on = ys > ycap - 30
        if on.any():
            C.rejilla_luces(h, xs[on], ys[on], (14, 18), v=1.1, col=h.pal["verde"])
        # el tubo brilla bajo la cápsula y la cápsula lleva el rótulo de la carpeta
        h.emitir(C.rect(1000, ycap, 60, 3800 - ycap), 0.14, col=h.pal["verde"], blur=5)
        P.capsula(h, 1030, ycap, 0.95, ang=-math.pi / 2, sem=980, rotulo="0417", t=t, brillo=1.0)
        h.resplandor(1030, ycap, 360, 0.7, col=h.pal["verde"])
        h.luz_radial(1030, ycap, 900, h.pal["verde"], k=1.0)
        C.ambiente(h, 0.3)
        C.banda(h, "AYUDA", 960, 980, 78, t, self.t_ayuda - 0.1, acento=True, sem=8)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=45, vel=6), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.1, "lluvia_amb", 0.4, 0.0, dur=tb[1] - tb[0] + 0.6)
        self.ev(tb[0] + 0.3, "trueno_lejano", 0.3, 0.3, dur=3.0)
        self.ev(self.t_once - 0.2, "reloj_pared", 0.45, 0.0, dur=1.8)
        self.ev(tb[1] + 0.7 + 0.55, "golpe_grave", 0.55, 0.1)
        self.ev(tb[1] + 0.7 + 1.65, "golpe_grave", 0.5, 0.0)
        self.ev(tb[1] + 0.2, "zumbido_servidores", 0.25, 0.0, dur=tb[2] - tb[1])
        self.ev(tb[2] + 0.35, "pinza", 0.55, 0.0)
        self.ev(tb[2] + 0.9, "papel_arranca", 0.5, 0.0)
        self.ev(tb[3] + 0.1, "datos", 0.4, 0.0, dur=3.5)
        self.ev(self.t_escribe, "tecleo_rapido", 0.5, 0.0, dur=2.2)
        self.ev(self.t_sistema - 0.3, "teletipo", 0.4, 0.2, dur=1.4)
        self.ev(tb[6] + 0.3, "lapiz", 0.5, -0.3, dur=1.6)
        self.ev(self.t_amenaza - 0.1, "tachon", 0.6, -0.3)
        self.ev(self.t_fuga - 0.3, "tachon", 0.6, 0.3)
        self.ev(tb[7] + 0.2, "subida", 0.55, 0.0, dur=3.8)
        self.ev(tb[7] + 0.3, "servo", 0.35, 0.2)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
