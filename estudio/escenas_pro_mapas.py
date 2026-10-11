# -*- coding: utf-8 -*-
"""Escenas del ESTUDIO para el estilo Mapas con Relieve Real (pro_mapas y pro_mapa_guache).
Utiliza el motor de relieve ETOPO1 y Natural Earth (nucleo/kz_mapa.py y kz_mapa_dib.py):
ciudades con mini-dioramas, rutas punteadas en movimiento, etiquetas geográficas y cámara
cinematográfica sobre el mapa.
Se adapta automáticamente tanto a horizontal (1920x1080) como a vertical (1080x1920).
"""
import math

import numpy as np

import config
import estilos
import kz_mapa
import kz_mapa_dib as MD
import plano as P
from escena_base import (BLANCO, Escena, e_in, e_inout, e_out, lerp, partir_lineas, pop, prog, sale, env_bombo, TL)
from motor import W, H, ancho_texto

estilos.activar("kurzgesagt")

VERT = H > W
CX = W / 2
CY = H * 0.52 if VERT else 540
FUENTE = "geo"
ANCHO_LIN = 14 if VERT else 24
Y_TITULO = 240 if VERT else 110

SLOTS = ([(CX - 220, H * 0.22), (CX + 210, H * 0.76), (CX + 200, H * 0.25), (CX - 210, H * 0.79)] if VERT else
         [(420, 280), (1500, 800), (1500, 280), (420, 800)])

# Lugares conocidos con coordenadas por defecto si no están en CIUDADES
LUGARES_EXTRA = {
    "espana": (-3.70, 40.42), "francia": (2.35, 48.86), "italia": (12.50, 41.90),
    "alemania": (13.40, 52.52), "inglaterra": (-0.12, 51.50), "mexico": (-99.13, 19.43),
    "america": (-99.13, 19.43), "europa": (2.35, 48.86)
}


def _resolver_lugar(nombre):
    """Devuelve una clave de ciudad válida de MD.CIUDADES o coordenadas (lon, lat)."""
    if not nombre:
        return "mexico"
    n = nombre.lower().strip()
    for c in MD.CIUDADES:
        if c in n or n in c:
            return c
    for k, v in LUGARES_EXTRA.items():
        if k in n or n in k:
            return v
    # Fallback por defecto: centro histórico
    return "mexico"


def _coords_lugar(lugar):
    lo, la = MD.CIUDADES[lugar] if isinstance(lugar, str) and lugar in MD.CIUDADES else lugar if isinstance(lugar, tuple) else (-99.13, 19.43)
    return float(lo), float(la)


def _palabra(esc, palabra, defecto, desde=0):
    if not palabra:
        return defecto
    try:
        return esc.w(palabra.split()[0], desde=desde)
    except (KeyError, IndexError):
        return defecto


def _px_que_cabe(lineas, px, ancho_max):
    mx = max((ancho_texto(l, FUENTE, 100) for l in lineas), default=1) or 1
    return min(px, ancho_max / mx * 100)


class _BaseMapa(Escena):
    """Base de escenas sobre mapa: fondo con relieve real, cámara y anotaciones."""

    def preparar_comun(self, solo_abajo=False):
        self.claves = []
        slots = [sl for sl in SLOTS if sl[1] > H * 0.5] if solo_abajo else SLOTS
        for i, (palabra, texto) in enumerate(self.d.get("claves", [])[:4]):
            tc = _palabra(self, palabra, self.t0 + 0.6 + 1.2 * i)
            self.claves.append((tc, texto.upper()[:24], slots[i % len(slots)]))
            self.ev(tc, "pop", 0.45, pan=-0.3 if slots[i % len(slots)][0] < CX else 0.3, tono=1.05 + 0.08 * i)

        self.t_cifra = None
        if self.d.get("cifra"):
            self.t_cifra = _palabra(self, self.d.get("cifra_palabra"), self.t0 + 1.0)
            self.ev(self.t_cifra, "impacto", 0.7)

        if self.d.get("titulo"):
            self.ev(self.t0 + 0.1, "whoosh", 0.35, dur=0.35)

    def rotulo(self, lz, t):
        tit = self.d.get("titulo")
        if not tit:
            return
        k = pop(t, self.t0 + 0.1, 0.35) * sale(t, self.t1 - 0.22, 0.22)
        if k > 0:
            P.pastilla(lz, CX, Y_TITULO, tit.upper()[:28], px=42 if VERT else 40, k=k,
                       fondo=(255, 255, 255), color=(26, 22, 54), fuente=FUENTE)

    def dibujar_claves(self, lz, t):
        for i, (tc, texto, (x, y)) in enumerate(self.claves):
            k = pop(t, tc, 0.3) * sale(t, self.t1 - 0.2, 0.2)
            if k > 0:
                y_flota = y + 6 * math.sin(t * 1.8 + i)
                P.pastilla(lz, x, y_flota, texto, px=38 if VERT else 36, k=k,
                           fondo=(235, 240, 255), color=(30, 25, 60), fuente=FUENTE)

    def dibujar_cifra(self, lz, t):
        if self.t_cifra is None:
            return
        k = pop(t, self.t_cifra, 0.4) * sale(t, self.t1 - 0.25, 0.25)
        if k > 0:
            txt = str(self.d["cifra"])[:14]
            px = min(220, int((W * 0.8) / max(1, ancho_texto(txt, FUENTE, 100)) * 100))
            y = H * 0.22 if VERT else 240
            with lz.capa(2):
                P.rotulo(lz, CX, y, txt, px=px, k=k * (1 + 0.03 * env_bombo(t)),
                         color=(255, 220, 80), fuente=FUENTE, rot=0.01 * math.sin(t * 1.5))


class IntroMapa(_BaseMapa):
    """Intro Mapa: Gran vista de mapa con relieve y título principal."""

    def preparar(self):
        self.lugar = _resolver_lugar(self.d.get("lugar") or self.d.get("icono"))
        self.lo, self.la = _coords_lugar(self.lugar)
        self.lineas = partir_lineas(config.TITULO.upper(), ANCHO_LIN)[:4]
        for i in range(len(self.lineas)):
            self.ev(0.12 + 0.28 * i, "impacto" if i == 0 else "pop", 0.75, tono=0.95 + 0.1 * i)
        self.fin_titulo = self.fr[1]["t0"] - 0.2 if len(self.fr) > 1 else max(self.t0 + 2.0, self.fr[0]["t1"] - 0.4)
        self.ev(self.fin_titulo, "whoosh", 0.5, dur=0.4)
        self.preparar_comun(solo_abajo=True)

    def camara_mapa(self, t):
        # Descenso suave de cámara hacia la coordenada
        u = prog(t, self.t0, self.t1)
        z = lerp(0.45, 0.75, e_inout(u))
        return (self.lo, self.la, z)

    def fondo(self, t):
        cam = self.camara_mapa(t)
        return kz_mapa.MAPA.base(cam, t)

    def dibujar(self, lz, t):
        cam = self.camara_mapa(t)
        sube = e_inout(prog(t, self.fin_titulo - 0.1, self.fin_titulo + 0.45))
        n = len(self.lineas)
        px = _px_que_cabe(self.lineas, (126 if n <= 2 else 102) if VERT else (116 if n <= 3 else 90), W * 0.78)
        y_fin = H * 0.18 if VERT else 165

        with lz.grupo(CX, lerp(CY, y_fin, sube), 1 - 0.45 * sube):
            for i, lin in enumerate(self.lineas):
                k = pop(t, 0.12 + 0.28 * i, 0.35)
                if k > 0:
                    with lz.capa(2):
                        P.rotulo(lz, 0, -(n - 1) * px * 0.62 + i * px * 1.25, lin, px=px, k=k,
                                 color=BLANCO if i == 0 else (240, 245, 255), fuente=FUENTE)

        if sube > 0.1:
            MD.ciudad(lz, cam, self.lugar, t, t0=self.fin_titulo + 0.1, tam=1.2, nombre=str(self.lugar).upper())

        self.dibujar_claves(lz, t)


class LibreMapa(_BaseMapa):
    """Escena con viaje entre ciudades sobre el relieve."""

    def preparar(self):
        self.lugar = _resolver_lugar(self.d.get("lugar") or self.d.get("icono"))
        self.destino = _resolver_lugar(self.d.get("icono2") or self.d.get("ruta")) if self.d.get("icono2") or self.d.get("ruta") else None
        self.lo1, self.la1 = _coords_lugar(self.lugar)
        if self.destino and self.destino != self.lugar:
            self.lo2, self.la2 = _coords_lugar(self.destino)
        else:
            self.lo2, self.la2 = self.lo1, self.la1
            self.destino = None

        self.ev(self.t0 + 0.1, "aparicion", 0.55)
        self.preparar_comun()

    def camara_mapa(self, t):
        u = prog(t, self.t0 + 0.5, self.t1 - 0.5)
        if self.destino:
            lo = lerp(self.lo1, self.lo2, e_inout(u))
            la = lerp(self.la1, self.la2, e_inout(u))
            z = 0.85 - 0.15 * math.sin(u * math.pi)
        else:
            lo = self.lo1 + 0.15 * math.sin(u * 1.5)
            la = self.la1 + 0.10 * math.cos(u * 1.2)
            z = 0.80
        return (lo, la, z)

    def fondo(self, t):
        cam = self.camara_mapa(t)
        return kz_mapa.MAPA.base(cam, t)

    def dibujar(self, lz, t):
        cam = self.camara_mapa(t)
        MD.ciudad(lz, cam, self.lugar, t, t0=self.t0 + 0.1, tam=1.1, nombre=str(self.lugar).upper())

        if self.destino:
            MD.ciudad(lz, cam, self.destino, t, t0=self.t0 + 1.2, tam=1.1, nombre=str(self.destino).upper())
            MD.ruta(lz, cam, [self.lugar, self.destino], t, frac=prog(t, self.t0 + 0.8, self.t1 - 0.4),
                    color=(240, 190, 70), ancho=5.0)

        self.dibujar_cifra(lz, t)
        self.dibujar_claves(lz, t)
        self.rotulo(lz, t)


class CierreMapa(_BaseMapa):
    """Cierre con zoom amplio panorámico y mensaje final."""

    def preparar(self):
        self.lugar = _resolver_lugar(self.d.get("lugar") or "mexico")
        self.lo, self.la = _coords_lugar(self.lugar)
        self.fin = self.fr[-1]["t1"] + 0.12 if self.fr else self.t0 + 1.0
        self.ev(self.fin, "impacto", 0.85)
        self.preparar_comun()

    def camara_mapa(self, t):
        u = prog(t, self.t0, self.t1)
        z = lerp(0.80, 0.45, e_inout(u))   # Zoom out panorámico
        return (self.lo, self.la, z)

    def fondo(self, t):
        cam = self.camara_mapa(t)
        return kz_mapa.MAPA.base(cam, t)

    def dibujar(self, lz, t):
        cam = self.camara_mapa(t)
        MD.ciudad(lz, cam, self.lugar, t, t0=self.t0 + 0.1, tam=1.0)

        if t >= self.fin:
            lineas = partir_lineas(self.d.get("cierre", "¿LO SABÍAS?").upper(), 13 if VERT else 20)[:4]
            px = _px_que_cabe(lineas, 108 if VERT else 102, W * 0.74)
            y0 = CY - (len(lineas) - 1) * px * 0.65
            with lz.capa(2):
                for i, lin in enumerate(lineas):
                    k = pop(t, self.fin + 0.14 * i, 0.38)
                    if k > 0:
                        P.rotulo(lz, CX, y0 + i * px * 1.3, lin, px=px, k=k,
                                 color=(255, 230, 80) if i == 0 else BLANCO, fuente=FUENTE)

        self.rotulo(lz, t)

    def render(self, lz, t):
        img = Escena.render(self, lz, t)
        neg = prog(t, self.t1 - 0.55, self.t1 - 0.05)
        return img * (1 - neg) if neg > 0 else img


def clases_mapas():
    n = len(TL["escenas"])
    return {e["id"]: (IntroMapa if k == 0 else CierreMapa if k == n - 1 else LibreMapa)
            for k, e in enumerate(TL["escenas"])}
