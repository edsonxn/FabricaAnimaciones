# -*- coding: utf-8 -*-
"""Escenas para 'El Asalto Pirata: Batalla en el Fuerte del Caribe' (Estilo Kurzgesagt Isométrico).

Máxima densidad visual, dioramas que llenan el encuadre (calidad idéntica a Independencia),
cámara en continuo movimiento cinemático, combate cuerpo a cuerpo y artillería pesada.
"""
import math
import sys
import cv2
import numpy as np

# Asegurar importación de módulos del núcleo
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")

import kz_gente_iso as G
import kz_iso as I
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_obj as O
import kz_ui as U
from motor import (H, W, catmull, circulo, e_back, e_inout, e_out, elipse, h01,
                   lerp, prog, rect_red, smooth, Lienzo)
import plano as P
from escena_base import Escena, TL
from util import K, bg_grad


def safe_w(esc, palabra, default=None):
    try:
        return esc.w(palabra)
    except Exception:
        return default if default is not None else (esc.t0 + 1.0)


def nubes(lz, t, escala=1.0):
    """Nubes suaves caribeñas a la deriva en capas."""
    for i in range(12):
        x = (h01(i, 1) * 2600 - 300 + t * (10 + 7 * h01(i, 2))) % 2600 - 300
        y = 650 + 400 * h01(i, 3) if i % 2 else 50 + 260 * h01(i, 4)
        r = 80 + 80 * h01(i, 5)
        for (dx, dy, rr, c, a) in ((0, 20, 1.0, (170, 110, 150), 0.45),
                                   (-r * 0.7, 8, 0.7, (170, 110, 150), 0.45),
                                   (r * 0.7, 12, 0.75, (170, 110, 150), 0.45),
                                   (0, 0, 0.95, (255, 225, 210), 0.85),
                                   (-r * 0.65, -4, 0.66, (255, 225, 210), 0.85),
                                   (r * 0.65, 0, 0.7, (255, 225, 210), 0.85),
                                   (-r * 0.2, -r * 0.3, 0.55, (255, 245, 235), 0.9)):
            lz.relleno(circulo(x + dx, y + dy, r * rr * escala, 18), c, alfa=a, capa=0)


def aves(lz, t, t0, origen, n=11, vel=1.1):
    """Bandada de gaviotas caribeñas en vuelo."""
    if t < t0:
        return
    u = t - t0
    for i in range(n):
        ang = -2.35 + 1.7 * h01(i, 9)
        sp = (160 + 170 * h01(i, 10)) * vel
        x = origen[0] + math.cos(ang) * sp * u + 35 * (h01(i, 11) - 0.5)
        y = origen[1] + math.sin(ang) * sp * u * 0.8 - 20 * u
        a = max(0.0, 1.0 - u / 4.5)
        if a <= 0 or x < -50 or x > W + 50 or y < -50 or y > H + 50:
            continue
        al = math.sin(u * 14 + i * 1.8) * 8
        s = 0.9 + 0.5 * h01(i, 12)
        lz.relleno(np.array([[x - 12 * s, y - al * s], [x, y + 1 * s],
                             [x + 12 * s, y - al * s], [x, y - 2 * s]]),
                   (45, 30, 65), alfa=a, capa=2)


# =========================================================================================
# ESCENA 1: ACERCAMIENTO NAVAL A LA BAHÍA COLONIAL
# =========================================================================================
class EscenaAcercamiento(Escena):
    """Galeón corsario navegando a toda vela hacia la costa fortificada."""

    def preparar(self):
        self.t_galeon = safe_w(self, "galeon", self.t0 + 3.8)
        self.t_bastion = safe_w(self, "bastion", self.t0 + 9.0)
        self.ev(self.t0 + 0.2, "whoosh", 0.5)
        self.ev(self.t0 + 1.2, "ola", 0.75)
        self.ev(self.t_galeon, "pop", 0.45)
        self.ev(self.t_bastion, "tambor", 0.75)

    def fondo(self, t):
        return bg_grad((20, 65, 145), (245, 210, 135), mid=(85, 165, 215), ym=0.58)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        nubes(lz, t, escala=1.2)
        I.luz(mul=(1.0, 0.98, 0.92), mix=(255, 230, 180), k=0.15)

        # Cámara cinematográfica con encuadre que llena toda la pantalla
        cx, cy, cz, zm = K(t, [
            (self.t0, (110, 65, 20, 2.70)),
            (self.t0 + 7.5, (135, 55, 28, 3.10)),
            (self.t1, (160, 45, 35, 3.50))
        ])
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))

        # Isla caribeña tropical ajustada
        I.isla(lz, iso, -30, -50, 270, 210, color_top=(238, 220, 160), esp=22,
               c_tierra=(172, 126, 88), c_roca=(128, 104, 126), seed=14)

        # Sector de agua turquesa con oleaje en la parte baja
        pts_agua = [(-30, -50), (95, -50), (45, 160), (-30, 160)]
        O.agua(lz, iso, pts_agua, t, c1=(55, 165, 228), c2=(35, 120, 200), z=-1.0)

        m = I.Mundo()

        # Palmeras tropicales agrupadas en la arena mecidas por el viento
        for i, (px, py, ph) in enumerate([
            (60, -35, 78), (95, -20, 72), (130, -5, 84), (165, 10, 74),
            (195, 25, 68), (220, 45, 80)
        ]):
            O.palmera(lz, iso, px, py, h=ph, seed=i + 1, t=t)

        # Poblado colonial y almacén portuario
        A.casa_colonial(m, 110, 60, w=48, d=38, h=34, muro=A.CAL, techo=A.TEJA, ventanas=2, seed=1)
        A.casa_colonial(m, 170, 80, w=44, d=36, h=32, muro=A.CANTERA, techo=A.TEJA, ventanas=2, seed=2)
        B.choza(m, 75, 70, r=14, h=22, seed=3)

        # Muelle de madera adentrándose en el agua
        B.muelle(m, 35, 10, largo=95, ancho=24, h=8, eje="x")

        # Barriles y cajas de mercancías en el muelle
        O.barril(lz, iso, 65, 14, s=1.1)
        O.barril(lz, iso, 71, 18, s=1.0)
        O.caja_madera(lz, iso, 95, 20, s=1.2)
        O.caja_madera(lz, iso, 100, 26, s=1.1)

        # Gente en el puerto: guardias coloniales y comerciantes
        G.persona(lz, iso, 85, 12, t, "realista", dir=(-1, 0), accion="vitorea", h=38)
        G.persona(lz, iso, 110, 15, t, "comerciante", dir=(-1, 0.5), accion="trabaja", h=36)
        G.persona(lz, iso, 140, 50, t, "campesino", dir=(0.7, 0.7), vel=1.5, h=36)

        # Torre vigía de piedra en la loma con bandera imperial española
        O.muro_piedra(lz, iso, 215, 105, 26, 26, 44, color=(220, 206, 186))
        O.bandera(lz, iso, 228, 118, h=52, w=30, alto=18, color=(226, 60, 60), t=t)

        # Galeón corsario navegando a toda vela en el sector de agua
        u_nav = prog(t, self.t0, self.t1)
        bx = float(lerp(-15, 55, e_inout(u_nav)))
        by = float(lerp(80, 20, e_inout(u_nav)))
        B.barco(m, bx, by, t_fn=lambda: t, s=1.85, vela=(252, 246, 235),
                casco=(105, 66, 48), banderas=(218, 48, 48), dir=1)

        m.dibujar(lz, iso)

        # Bandada de gaviotas volando sobre las aguas
        aves(lz, t, self.t0 + 0.6, (W * 0.38, H * 0.35), n=12)

        # Elementos UI Kurzgesagt
        U.fecha_lugar(lz, t, self.t0 + 0.3, self.t1, "Mar Caribe", "Año 1680")

        k_gal = U.pop(t, self.t_galeon)
        if k_gal > 0.01:
            U.llamada(lz, 1360, 240, "Navío Corsario", color=U.COL["rojo"], px=34, k=k_gal)

        k_bas = U.pop(t, self.t_bastion)
        if k_bas > 0.01:
            U.llamada(lz, 500, 200, "Bastión de San Felipe", color=U.COL["morado"], px=34, k=k_bas)


# =========================================================================================
# ESCENA 2: BOMBARDEO Y DESCARGA DE ARTILLERÍA
# =========================================================================================
class EscenaBombardeo(Escena):
    """Batería de artillería costera abriendo fuego con cañones pesados sobre el mar."""

    def preparar(self):
        self.t_fuego1 = self.t0 + 1.2
        self.t_fuego2 = self.t0 + 4.5
        self.t_fuego3 = self.t0 + 8.2
        self.t_fuego4 = self.t0 + 11.5

        self.ev(self.t0 + 0.2, "whoosh", 0.5)
        self.ev(self.t_fuego1, "canonazo", 0.98)
        self.ev(self.t_fuego1 + 0.45, "chapuzon", 0.85)
        self.ev(self.t_fuego2, "canonazo", 0.98)
        self.ev(self.t_fuego3, "canonazo", 0.98)
        self.ev(self.t_fuego4, "explosion", 0.98)

    def fondo(self, t):
        return bg_grad((34, 44, 90), (235, 140, 90), mid=(130, 85, 125), ym=0.55)

    def camara(self, t):
        # Temblor de cámara sísmico en cada disparo de cañón (dx, dy - SIN rotación!)
        shake = 0.0
        for tf in (self.t_fuego1, self.t_fuego2, self.t_fuego3, self.t_fuego4):
            if 0 <= t - tf < 0.7:
                u = (t - tf) / 0.7
                shake += 12.0 * math.sin(u * 32.0) * (1.0 - u)
        return 1.0, 0.0, float(shake), float(shake * 0.35)

    def dibujar(self, lz, t):
        nubes(lz, t, escala=1.0)
        I.luz(mul=(1.0, 0.94, 0.88), mix=(255, 185, 130), k=0.22)

        # Cámara cinemática en plano cerrado sobre las piezas de artillería
        cx, cy, cz, zm = K(t, [
            (self.t0, (135, 65, 25, 2.90)),
            (self.t0 + 7.0, (155, 52, 35, 3.35)),
            (self.t1, (175, 40, 45, 3.80))
        ])
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))

        # Macizo rocoso y bastión fortificado
        I.isla(lz, iso, 15, -10, 245, 160, color_top=(215, 202, 182), esp=24,
               c_tierra=(150, 115, 88), c_roca=(110, 94, 114), seed=21)

        # Cuadrícula empedrada del baluarte
        I.cuadricula(lz, iso, 35, 10, 235, 150, 20, color=(255, 255, 255), alfa=0.15)

        # Muro almenado y parapeto de cantera
        O.muro_piedra(lz, iso, 30, 15, 20, 140, 34, color=(215, 200, 182))
        O.muro_piedra(lz, iso, 30, 15, 180, 20, 34, color=(215, 200, 182))
        O.muro_piedra(lz, iso, 210, 15, 20, 140, 34, color=(215, 200, 182))

        # Torreón defensivo en la esquina del fuerte
        O.muro_piedra(lz, iso, 195, 105, 34, 34, 48, color=(205, 192, 174))
        O.bandera(lz, iso, 212, 122, h=54, w=30, alto=18, color=(226, 55, 55), t=t)

        m = I.Mundo()

        # Cañones pesados sobre cureña apuntando al mar
        d1 = t - self.t_fuego1 if (0.0 <= t - self.t_fuego1 <= 2.2) else -1.0
        d2 = t - self.t_fuego2 if (0.0 <= t - self.t_fuego2 <= 2.2) else -1.0
        d3 = t - self.t_fuego3 if (0.0 <= t - self.t_fuego3 <= 2.2) else -1.0
        d4 = t - self.t_fuego4 if (0.0 <= t - self.t_fuego4 <= 2.2) else -1.0

        B.canon(m, 65, 32, dir=-1, disparo=d1, escala=1.65)
        B.canon(m, 110, 32, dir=-1, disparo=d2, escala=1.65)
        B.canon(m, 155, 32, dir=-1, disparo=d3, escala=1.65)
        B.canon(m, 195, 32, dir=-1, disparo=d4, escala=1.65)

        # Artilleros y oficiales reales disparando y cargando munición
        G.persona(lz, iso, 80, 44, t, "realista", dir=(-1, 0), accion="pelea", h=40, seed=1)
        G.persona(lz, iso, 125, 44, t, "realista", dir=(-1, 0), accion="pelea", h=40, seed=2)
        G.persona(lz, iso, 170, 44, t, "realista", dir=(-1, 0), accion="pelea", h=40, seed=3)
        G.persona(lz, iso, 150, 75, t, "oficial", dir=(-1, -0.3), accion="pelea", h=42, seed=4)

        # Soldados de refresco corriendo con sacos de pólvora
        G.persona(lz, iso, 100, 95, t, "realista", dir=(-0.8, -0.6), vel=2.2, accion="carga", h=38, seed=5)
        G.persona(lz, iso, 160, 100, t, "realista", dir=(-0.8, -0.6), vel=2.2, accion="carga", h=38, seed=6)

        # Almacenes de pólvora, barriles y pertrechos
        O.barril(lz, iso, 92, 68, s=1.2)
        O.barril(lz, iso, 99, 73, s=1.1)
        O.barril(lz, iso, 105, 69, s=1.0)
        O.caja_madera(lz, iso, 140, 72, s=1.3)
        O.caja_madera(lz, iso, 147, 78, s=1.2)

        m.dibujar(lz, iso)

        # Ondas sonoras doradas expansivas de cada cañonazo
        for (cx_c, cy_c, tf) in [(65, 32, self.t_fuego1), (110, 32, self.t_fuego2),
                                 (155, 32, self.t_fuego3), (195, 32, self.t_fuego4)]:
            px, py = iso.P(cx_c, cy_c, 12)
            U.ondas_sonoras(lz, float(px), float(py), t, t0=tf, n=5, r1=760, color=(255, 215, 80))

        # Alerta roja en pantalla
        k_alt = U.pop(t, self.t0 + 0.6)
        if k_alt > 0.01:
            U.llamada(lz, 960, 120, "¡BATERÍA DE COSTA EN FUEGO!", color=U.COL["rojo"], px=44, k=k_alt)


# =========================================================================================
# ESCENA 3: ASALTO AL BALUARTE Y COMBATE CUERPO A CUERPO
# =========================================================================================
class EscenaCombate(Escena):
    """Asalto al patio del bastión: violento choque cuerpo a cuerpo entre piratas y defensores."""

    def preparar(self):
        self.t_asalto = safe_w(self, "sable", self.t0 + 1.2)
        self.t_llamas = safe_w(self, "llamas", self.t0 + 8.2)

        self.ev(self.t0 + 0.2, "whoosh", 0.5)
        self.ev(self.t_asalto, "espada", 0.88)
        self.ev(self.t0 + 3.2, "espada", 0.88)
        self.ev(self.t0 + 5.8, "explosion", 0.95)
        self.ev(self.t0 + 8.2, "fuego", 0.75)
        self.ev(self.t0 + 11.2, "espada", 0.88)

    def fondo(self, t):
        return bg_grad((42, 18, 62), (225, 105, 75), mid=(155, 60, 78), ym=0.6)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        nubes(lz, t, escala=0.9)
        I.luz(mul=(1.0, 0.90, 0.84), mix=(255, 155, 105), k=0.28)

        # Cámara cinemática en plano cerrado sobre el patio en combate
        cx, cy, cz, zm = K(t, [
            (self.t0, (105, 90, 20, 2.95)),
            (self.t0 + 7.0, (125, 80, 30, 3.45)),
            (self.t1, (145, 70, 40, 3.95))
        ])
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))

        # Suelo empedrado del baluarte ajustado
        I.isla(lz, iso, 5, 0, 230, 180, color_top=(200, 188, 172), esp=20,
               c_tierra=(142, 108, 82), c_roca=(102, 90, 106), seed=18)

        # Cuadrícula de adoquines
        I.cuadricula(lz, iso, 20, 15, 215, 165, 18, color=(255, 255, 255), alfa=0.15)

        # Muros almenados y portón principal roto por la explosión
        O.muro_piedra(lz, iso, 20, 15, 16, 65, 40, color=(195, 180, 165))
        O.muro_piedra(lz, iso, 20, 120, 16, 65, 40, color=(195, 180, 165))
        O.empalizada(lz, iso, [(20, 80), (20, 120)], h=32)

        # Portón destrozado en llamas con humo denso y chispas
        O.fuego(lz, iso, 22, 100, s=3.2, t=t, halo=True)
        O.humo(lz, iso, 22, 100, 22, t, n=12, s=2.2, vel=24.0)
        O.chispas(lz, iso, 22, 100, 20, t, n=18)

        m = I.Mundo()

        # Arquería colonial del patio interior
        A.portal_arcos(m, 70, 150, n=5, paso=24, d=16, h=44, muro=A.CAL)

        # Piratas atacantes cargando con machetes y sables enérgicamente
        G.persona(lz, iso, 60, 90, t, "insurgente", dir=(1, 0), accion="pelea", h=42, seed=1)
        G.persona(lz, iso, 70, 115, t, "dragon", dir=(1, -0.3), accion="pelea", h=44, seed=2)
        G.persona(lz, iso, 45, 75, t, "insurgente", dir=(1, 0.4), vel=2.4, accion="carga", h=40, seed=3)
        G.persona(lz, iso, 40, 130, t, "insurgente", dir=(1, -0.4), vel=2.4, accion="carga", h=40, seed=4)
        G.persona(lz, iso, 85, 70, t, "dragon", dir=(1, 0.2), accion="pelea", h=42, seed=9)

        # Defensores de la corona combatiendo cuerpo a cuerpo con sables y mosquetes
        G.persona(lz, iso, 95, 95, t, "realista", dir=(-1, 0), accion="pelea", h=42, seed=5)
        G.persona(lz, iso, 105, 120, t, "realista", dir=(-1, 0.2), accion="pelea", h=42, seed=6)
        G.persona(lz, iso, 120, 85, t, "oficial", dir=(-1, -0.2), accion="pelea", h=44, seed=7)
        G.persona(lz, iso, 130, 110, t, "realista", dir=(-1, 0.1), accion="pelea", h=42, seed=8)

        # Cajas rotas y barriles volcados por el combate
        O.barril(lz, iso, 85, 65, s=1.2)
        O.barril(lz, iso, 91, 70, s=1.1)
        O.caja_madera(lz, iso, 135, 130, s=1.3)
        O.caja_madera(lz, iso, 142, 136, s=1.1)

        m.dibujar(lz, iso)

        # Llamadas UI de combate
        k_as = U.pop(t, self.t0 + 0.5)
        if k_as > 0.01:
            U.llamada(lz, 400, 180, "Asalto al Baluarte", color=U.COL["rojo"], px=36, k=k_as)

        k_cor = U.pop(t, self.t0 + 5.5)
        if k_cor > 0.01:
            U.llamada(lz, 1500, 240, "Combate cuerpo a cuerpo", color=U.COL["morado"], px=32, k=k_cor)


# =========================================================================================
# ESCENA 4: EL BOTÍN Y LA FUGA TRIUNFAL
# =========================================================================================
class EscenaFuga(Escena):
    """El galeón pirata huye hacia el horizonte cargado con el botín bajo el ocaso caribeño."""

    def preparar(self):
        self.t_botin = safe_w(self, "cincuenta", self.t0 + 1.2)
        self.t_leyenda = safe_w(self, "leyenda", self.t0 + 8.2)

        self.ev(self.t0 + 0.2, "whoosh", 0.5)
        self.ev(self.t_botin, "monedas", 0.88)
        self.ev(self.t0 + 4.2, "brillo", 0.78)
        self.ev(self.t_leyenda, "fanfarria", 0.95)

    def fondo(self, t):
        return bg_grad((65, 20, 85), (255, 125, 45), mid=(185, 55, 80), ym=0.52)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        nubes(lz, t, escala=1.3)
        # Haces de luz celestial dorada cruzando el cielo
        U.haces_luz(lz, 960, -90, t, n=11, alfa=0.34, color=(255, 225, 130))

        # Cámara elevándose y contemplando la fuga hacia alta mar
        cx, cy, cz, zm = K(t, [
            (self.t0, (110, 60, 20, 2.75)),
            (self.t0 + 7.0, (135, 45, 28, 3.10)),
            (self.t1, (160, 30, 35, 3.45))
        ])
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))

        # Isla de agua oceánica profunda en el crepúsculo
        I.isla(lz, iso, 0, -30, 250, 190, color_top=(45, 95, 160), esp=20,
               c_tierra=(25, 55, 105), c_roca=(20, 40, 80), seed=15)

        # Ondulaciones del agua marina
        pts_agua = [(0, -30), (250, -30), (250, 160), (0, 160)]
        O.agua(lz, iso, pts_agua, t, c1=(45, 110, 180), c2=(30, 75, 135), z=-1.0)

        m = I.Mundo()

        # Palmeras de la costa lejana en silueta crepuscular
        for i, (px, py, ph) in enumerate([(190, -10, 72), (215, 15, 78), (235, 40, 68)]):
            O.palmera(lz, iso, px, py, h=ph, seed=i + 3, t=t)

        # Galeón navegando rápidamente a toda vela hacia alta mar
        u_fuga = prog(t, self.t0, self.t1)
        bx = float(lerp(30, 160, e_inout(u_fuga)))
        by = float(lerp(80, 20, e_inout(u_fuga)))
        B.barco(m, bx, by, t_fn=lambda: t, s=2.65, vela=(252, 235, 195),
                casco=(95, 60, 48), banderas=(215, 45, 45), dir=1)

        m.dibujar(lz, iso)

        # Contador dinámico de botín
        u_cont = smooth(prog(t, self.t0 + 0.8, self.t0 + 5.0))
        doblones = int(lerp(0, 50000, u_cont))

        # Pastilla del botín con monedas de oro
        if u_cont > 0.05:
            P.pastilla(lz, 960, 310, f"{doblones:,} DOBLONES DE ORO", px=50, k=1.0,
                       fondo=(255, 215, 60), color=(45, 20, 10))

        # Título y cierre majestuoso
        k_cie = U.pop(t, self.t_leyenda)
        if k_cie > 0.01:
            P.pastilla(lz, 960, 480, "EL BOTÍN DEL CARIBE", px=56, k=k_cie,
                       fondo=(255, 255, 255), color=(35, 18, 55))
            P.rotulo(lz, 960, 560, "LEYENDA DE LOS MARES DEL SUR", px=30, color=(255, 220, 80))


# =========================================================================================
# REGISTRO OBLIGATORIO DE ESCENAS
# =========================================================================================
CLASES = {
    "acercamiento": EscenaAcercamiento,
    "bombardeo": EscenaBombardeo,
    "combate": EscenaCombate,
    "fuga": EscenaFuga,
}
