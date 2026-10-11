# -*- coding: utf-8 -*-
"""Escenas para 'La Conspiración y el Grito de Dolores' — Kurzgesagt ISOMÉTRICO (calidad Bitácora Perdida).
Recreación de alta fidelidad con el motor de 'independencia_mx':
  1. intro: Interior en corte de la tertulia secreta (sala criolla, candelabros, conspiradores, 'en secreto', shh... psst).
  2. conspiracion: Mapa con relieve real topográfico (ETOPO1) del Bajío + Medallones de Josefa Ortiz y Allende.
  3. correo: Calle colonial empedrada de Querétaro con acueducto y mensajero a caballo en la noche.
  4. dolores: Diorama isométrico de Dolores al amanecer: isla flotante en el cielo con nubes,
     iglesia de cantera, campana repicando con ondas sonoras doradas concéntricas, multitud en la plaza y retrato de Hidalgo.
  5. cierre: Celebración y estallido patriótico con haces de luz divina, medallón de Hidalgo y gran rótulo.
"""
import math
import os
import sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.abspath(os.path.join(AQUI, "..", "..", "nucleo"))
if NUCLEO not in sys.path:
    sys.path.insert(0, NUCLEO)
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import kz_retrato as RT
import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import (W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back,
                    circulo, elipse, rect_red, h01, componer, Lienzo)
from escena_base import Escena, TL
from util import T, T0, T1, K, Klog, bg_grad
import mundos
import mundos_e


def safe_w(esc, palabra, default=None):
    try:
        return esc.w(palabra)
    except Exception:
        return default if default is not None else (esc.t0 + 1.0)


def nubes(lz, t, escala=1.0):
    """Nubes suaves rosadas a la deriva debajo y alrededor de la isla diorama."""
    for i in range(10):
        x = (h01(i, 1) * 2400 - 240 + t * (6 + 5 * h01(i, 2))) % 2400 - 240
        y = 560 + 480 * h01(i, 3) if i % 2 else 80 + 300 * h01(i, 4)
        r = 70 + 70 * h01(i, 5)
        for (dx, dy, rr, c, a) in ((0, 18, 1.0, (190, 110, 150), 0.55),
                                   (-r * 0.7, 6, 0.7, (190, 110, 150), 0.55),
                                   (r * 0.7, 10, 0.75, (190, 110, 150), 0.55),
                                   (0, 0, 0.95, (255, 214, 206), 0.9),
                                   (-r * 0.65, -4, 0.66, (255, 214, 206), 0.9),
                                   (r * 0.65, 0, 0.7, (255, 214, 206), 0.9),
                                   (-r * 0.2, -r * 0.3, 0.55, (255, 240, 232), 0.9)):
            lz.relleno(circulo(x + dx, y + dy, r * rr * escala, 18), c, alfa=a, capa=0)


def aves(lz, t, t0, origen, n=9, vel=1.0):
    """Bandada de pájaros saliendo en vuelo."""
    if t < t0:
        return
    u = t - t0
    for i in range(n):
        ang = -2.3 + 1.6 * h01(i, 9)
        sp = (150 + 160 * h01(i, 10)) * vel
        x = origen[0] + math.cos(ang) * sp * u + 30 * (h01(i, 11) - 0.5)
        y = origen[1] + math.sin(ang) * sp * u * 0.8 - 18 * u
        a = max(0.0, 1.0 - u / 4.5)
        if a <= 0 or x < -40 or x > W + 40 or y < -40 or y > H + 40:
            continue
        al = math.sin(u * 13 + i * 1.7) * 7
        s = 0.8 + 0.5 * h01(i, 12)
        lz.relleno(np.array([[x - 11 * s, y - al * s], [x, y + 1 * s],
                             [x + 11 * s, y - al * s], [x, y - 2 * s]]),
                   (66, 34, 80), alfa=a, capa=2)


# ============================================================================
# CLASES DE ESCENAS ISOMÉTRICAS (CALIDAD INDEPENDENCIA DE MÉXICO)
# ============================================================================

class EscenaIntro(Escena):
    """Escena 1: La tertulia secreta en Querétaro (interior en corte colonial)."""

    def preparar(self):
        self.t_calma = safe_w(self, "calma", self.t0 + 2.5)
        self.t_rebel = safe_w(self, "rebelion", self.t0 + 8.0)
        self.ev(self.t0 + 0.3, "brillo", 0.4)
        self.ev(self.t_calma, "suspiro", 0.4)
        self.ev(self.t_rebel, "revelar", 0.5)

    def fondo(self, t):
        return bg_grad((40, 22, 92), (130, 58, 124), mid=(84, 38, 112), ym=0.5)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        I.luz(mul=(1.0, 0.96, 0.92), mix=(255, 170, 110), k=0.06)
        U.bokeh(lz, t, seed=11, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)

        u_pan = prog(t, self.t0, self.t1)
        zm = 3.35 + 0.04 * (t - self.t0)
        iso = I.Iso(150, 125, 40, zm, sx0=930, sy0=650)

        mundos_e.sala_criolla(lz, iso, t)

        m = I.Mundo()
        mundos_e.mueble_sala(m, t, plan=prog(t, self.t0 + 1.0, self.t0 + 5.0))

        # Conspiradores alrededor de la mesa
        pos = ((60, 108), (60, 134), (200, 108), (200, 134), (98, 174), (144, 174))
        tipos = ("noble", "comerciante", "regidor", "escribano", "noble", "comerciante")
        for i, (px, py) in enumerate(pos):
            m.add(px - 4, py - 4, px + 4, py + 4, 40,
                  (lambda px, py, i: (lambda lz, iso: G.persona(lz, iso, px, py, t, tipos[i],
                                                                dir=(-0.8 if px > 130 else 0.8, 0.0),
                                                                h=50, accion="habla" if i % 2 == 0 else None,
                                                                cara="habla" if i % 2 == 0 else None)))(px, py, i),
                  fijo=False, clave=px + py + 10)

        # Centinela en la puerta
        m.add(2, 198, 10, 206, 40,
              lambda lz, iso: G.persona(lz, iso, 6, 204, t, "regidor", dir=(0.8, -0.6), h=52, cara="miedo"),
              fijo=False, clave=215)

        m.dibujar(lz, iso)
        N.araña(lz, iso, 130, 118, 130, t, velas=5, s=1.25)

        # Rótulos de cápsula y fecha/lugar
        U.fecha_lugar(lz, t, self.t0 + 0.3, self.t1 - 0.2, "Nueva España", "Septiembre de 1810")

        k_sec = U.pop(t, self.t0 + 1.2) * U.salida(t, self.t1 - 0.8)
        if k_sec > 0.01:
            U.llamada(lz, 960, 200, "en secreto", color=U.COL["rojo"], px=56, k=k_sec, cola="abajo")
            U.globo(lz, 750, 470, "shh…", px=30, k=k_sec)
            U.globo(lz, 1170, 480, "psst", px=30, k=k_sec)


class EscenaConspiracion(Escena):
    """Escena 2: Mapa topográfico real ETOPO1 del Bajío y retratos de Josefa Ortiz y Allende."""

    def preparar(self):
        self.t_allende = safe_w(self, "Allende", self.t0 + 6.0)
        self.t_delatados = safe_w(self, "descubrieron", self.t0 + 13.0)
        self.ev(self.t0 + 0.2, "whoosh", 0.4)
        self.ev(self.t_allende, "pop", 0.4)
        self.ev(self.t_delatados, "ding", 0.5)

    def fondo(self, t):
        cam = Klog(t, [(self.t0, (-100.9, 21.7, 1.6)), (self.t1, (-100.45, 20.75, 3.1))])
        return KM.MAPA.base(cam, t, exag=12.0, rios_umbral=0.7)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        I.luz()
        cam = Klog(t, [(self.t0, (-100.9, 21.7, 1.6)), (self.t1, (-100.45, 20.75, 3.1))])

        # Ciudades del Bajío con marcadores animados
        MD.ciudad(lz, cam, "queretaro", t, self.t0 + 0.2, tam=1.2, tipo="ciudad", nombre="Querétaro")
        MD.ciudad(lz, cam, (-100.74, 20.91), t, self.t0 + 1.0, tam=1.1, tipo="pueblo", nombre="San Miguel")
        MD.ciudad(lz, cam, "dolores", t, self.t0 + 1.8, tam=1.1, tipo="pueblo", nombre="Dolores")
        MD.ciudad(lz, cam, "guanajuato", t, self.t0 + 2.5, tam=1.2, tipo="ciudad", nombre="Guanajuato")

        # Ruta de la conspiración conectando las ciudades
        pts_ruta = [(-100.39, 20.59), (-100.74, 20.91), (-100.93, 21.16)]
        MD.ruta(lz, cam, pts_ruta, color=(255, 215, 64), frac=prog(t, self.t0 + 0.8, self.t0 + 4.5), ancho=7.0)

        # Medallones con retratos en las esquinas
        MD.medallon(lz, 320, 360, 95, "josefa", t, emocion="serio", borde=(250, 206, 90), fondo=(80, 40, 110))
        U.llamada(lz, 320, 500, "Josefa Ortiz", color=U.COL["morado"], px=30, k=1.0)

        MD.medallon(lz, 1600, 360, 95, "allende", t, emocion="serio", borde=(250, 206, 90), fondo=(40, 70, 140))
        U.llamada(lz, 1600, 500, "Ignacio Allende", color=U.COL["azul"], px=30, k=1.0)

        # Rótulo de alerta si son delatados
        k_del = U.pop(t, self.t_delatados)
        if k_del > 0.01:
            U.llamada(lz, 960, 160, "¡DESCUBIERTOS!", color=U.COL["rojo"], px=64, k=k_del)


class EscenaCorreo(Escena):
    """Escena 3: Calle empedrada de Querétaro y correo a galope tendido en la noche."""

    def preparar(self):
        self.t_galope = safe_w(self, "galope", self.t0 + 3.0)
        self.t_oscuros = safe_w(self, "oscuros", self.t0 + 9.0)
        self.ev(self.t0 + 0.2, "whoosh", 0.4)
        self.ev(self.t_galope, "golpe_suave", 0.5)

    def fondo(self, t):
        return bg_grad((24, 18, 54), (54, 40, 88), mid=(38, 28, 70), ym=0.5)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        CAL = mundos_e.CalleQueretaro()
        iso = I.Iso(220, 240, 20, 2.6, sx0=960, sy0=600)
        CAL.suelo(lz, iso, t)
        m = CAL.objetos(t, gente=0.5, farolas=1.0)

        # Mensajero a caballo galopando a toda velocidad
        u_cab = prog(t, self.t0, self.t1)
        x_cab = lerp(-60, 480, (u_cab * 2.4) % 1.0)
        m.add(x_cab - 15, 220, x_cab + 15, 250, 30,
              (lambda x: (lambda lz, iso: G.caballo(lz, iso, x, 235, t, dir=1,
                                                   color=(140, 80, 50), vel=2.8,
                                                   jinete="arriero", s=1.15)))(x_cab),
              fijo=False, clave=350)
        m.dibujar(lz, iso)

        U.fecha_lugar(lz, t, self.t0 + 0.3, self.t1, "Querétaro", "Noche del 15 de septiembre")

        k_cab = U.pop(t, self.t_galope)
        if k_cab > 0.01:
            U.llamada(lz, 960, 140, "correo a galope tendido", color=U.COL["verde"], px=46, k=k_cab)


class EscenaDolores(Escena):
    """Escena 4: El Grito de Dolores al amanecer (diorama isométrico completo)."""

    def preparar(self):
        self.t_noticia = safe_w(self, "noticia", self.t0 + 2.0)
        self.t_campana = safe_w(self, "campana", self.t0 + 7.5)
        self.t_repique = safe_w(self, "repique", self.t0 + 13.0)
        self.ev(self.t0 + 0.2, "amanecer", 0.5)
        self.ev(self.t_campana, "ding", 0.6)
        self.ev(self.t_repique, "ding", 0.5)

    def fondo(self, t):
        return bg_grad((52, 30, 110), (236, 140, 120), mid=(176, 84, 150), ym=0.55)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        nubes(lz, t, escala=1.1)
        I.luz(mul=(1.0, 0.95, 0.92), mix=(255, 170, 130), k=0.10)

        DOL = mundos.Dolores()

        # Cámara con zoom suave hacia el atrio y campanario
        cx, cy, cz, zm = K(t, [(self.t0, (230, 230, 10, 0.85)),
                               (self.t0 + 6.0, (230, 180, 40, 1.45)),
                               (self.t1, (240, 160, 60, 2.2))])
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))

        DOL.suelo(lz, iso, t, isla=True)

        # Campana oscilando
        DOL.ang = 0.55 * math.sin((t - self.t0) * 8.0) * math.exp(-(t - self.t0) * 0.04)

        m = DOL.objetos(t, gente=1.0)
        # Cura Hidalgo en el atrio alzando la voz
        m.add(210, 150, 220, 165, 40,
              lambda lz, iso: G.persona(lz, iso, 215, 158, t, "cura", h=52, dir=(0.7, 0.7), accion="vitorea"),
              fijo=False, clave=450)
        m.dibujar(lz, iso)

        # Ondas sonoras doradas concéntricas del campanario
        camp_x, camp_y = iso.P(180, 130, 115)
        U.ondas_sonoras(lz, float(camp_x), float(camp_y), t, t0=self.t0 + 2.5, n=6,
                        color=(255, 225, 90), r1=540)

        # Aves saliendo en vuelo
        aves(lz, t, self.t0 + 3.0, (W * 0.45, H * 0.4))

        # Medallón de Miguel Hidalgo en la esquina
        MD.medallon(lz, 260, 320, 95, "hidalgo", t, emocion="serio", borde=(250, 206, 90), fondo=(50, 30, 90))
        U.llamada(lz, 260, 460, "Miguel Hidalgo", color=U.COL["oro"], px=32)

        U.fecha_lugar(lz, t, self.t0 + 0.3, self.t1, "Dolores, Guanajuato", "16 de septiembre de 1810")

        k_gr = U.pop(t, self.t_campana)
        if k_gr > 0.01:
            U.llamada(lz, 960, 140, "el grito de dolores", color=U.COL["rojo"], px=62, k=k_gr)


class EscenaCierre(Escena):
    """Escena 5: El estallido libertario y nacimiento de la nación."""

    def preparar(self):
        self.t_nacio = safe_w(self, "nacio", self.t0 + 1.5)
        self.t_chispa = safe_w(self, "chispa", self.t0 + 6.0)
        self.ev(self.t0 + 0.2, "amanecer", 0.6)
        self.ev(self.t_chispa, "brillo", 0.5)

    def fondo(self, t):
        return bg_grad((70, 40, 130), (255, 175, 110), mid=(190, 90, 150), ym=0.55)

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        nubes(lz, t, escala=1.2)
        U.haces_luz(lz, 960, -100, t, n=9, alfa=0.28, color=(255, 235, 160))

        DOL = mundos.Dolores()
        iso = I.Iso(230, 230, 10, 0.82)
        DOL.suelo(lz, iso, t, isla=True)
        m = DOL.objetos(t, gente=1.0)
        m.dibujar(lz, iso)

        # Medallón central de Hidalgo
        MD.medallon(lz, 960, 360, 110, "hidalgo", t, emocion="serio", borde=(255, 215, 60), fondo=(60, 20, 80))

        # Pastilla final de cierre
        P.pastilla(lz, 960, 530, "EL NACIMIENTO DE UNA NACIÓN", px=44, k=1.0, fondo=(255, 255, 255), color=(28, 20, 60))
        P.rotulo(lz, 960, 610, "16 DE SEPTIEMBRE DE 1810", px=32, color=(255, 220, 80))


# Registro obligatorio para el motor
CLASES = {
    "intro": EscenaIntro,
    "conspiracion": EscenaConspiracion,
    "correo": EscenaCorreo,
    "dolores": EscenaDolores,
    "cierre": EscenaCierre,
}
