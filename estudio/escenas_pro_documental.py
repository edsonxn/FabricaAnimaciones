# -*- coding: utf-8 -*-
"""Escenas del ESTUDIO para el estilo Documental de Misterio (pro_documental y pro_crimen).
Inspirado en 'Detrás del Enigma': fotos y documentos de archivo, texto serif blanco/amarillo,
sellos rojos de 'CONFIDENCIAL'/'CLASIFICADO', cifras gigantes y acabado de celuloide con grano,
polvo y viñeta.
Se adapta automáticamente tanto a horizontal (1920x1080) como a vertical (1080x1920).
"""
import math

import cv2
import numpy as np

import config
import docu as D
import estilos
from escena_base import (BLANCO, Escena, circulo, dibujar_icono, ICONOS,
                         e_in, e_inout, e_out, lerp, partir_lineas, pop, prog, sale, env_bombo, TL)
from motor import W, H, ancho_texto, rect_red

estilos.activar("documental")

VERT = H > W
CX = W / 2
CY = H * 0.52 if VERT else 540
FUENTE_TITULO = "vox_serif"
FUENTE_TAG = "geo"
ANCHO_LIN = 13 if VERT else 22
Y_TITULO = 230 if VERT else 110

AMARILLO_DOCU = (235, 240, 40)
ROJO_DOCU = (220, 26, 26)
BLANCO_DOCU = (250, 248, 240)

SLOTS = ([(CX - 210, H * 0.22), (CX + 200, H * 0.77), (CX + 190, H * 0.25), (CX - 200, H * 0.80)] if VERT else
         [(430, 280), (1490, 800), (1490, 280), (430, 800)])


def _palabra(esc, palabra, defecto, desde=0):
    if not palabra:
        return defecto
    try:
        return esc.w(palabra.split()[0], desde=desde)
    except (KeyError, IndexError):
        return defecto


def _px_que_cabe(lineas, px, ancho_max, fuente=FUENTE_TITULO):
    mx = max((ancho_texto(l, fuente, 100) for l in lineas), default=1) or 1
    return min(px, ancho_max / mx * 100)


def fondo_archivo(t):
    """Fondo oscuro texturizado de archivo con viñeta y sutil pozo de luz."""
    BW, BH = W, H
    # Fondo base pizarra/carbón muy oscuro
    img = np.full((BH, BW, 3), (0.04, 0.038, 0.035), dtype=np.float32)
    # Luz cenital tenue
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    dx = (xx - CX) / (W * 0.6)
    dy = (yy - CY) / (H * 0.6)
    dist = np.sqrt(dx * dx + dy * dy)
    luz = np.clip(1.0 - dist * 0.75, 0.0, 1.0)
    img += luz[..., None] * np.array([0.035, 0.03, 0.025], dtype=np.float32)
    return np.clip(img, 0, 1)


def dibujar_sello_rojo(lz, txt, x, y, k, rot=-7.0):
    """Sello rojo desgastado (CONFIDENCIAL, CLASIFICADO, CASO CERRADO) que estampa."""
    if k <= 0:
        return
    txt = txt.upper().strip()
    px = 44 if VERT else 42
    w = ancho_texto(txt, FUENTE_TAG, px) + 50
    h = px * 1.7
    with lz.capa(2):
        with lz.grupo(x, y, k, rot=math.radians(rot)):
            # Borde doble de sello de caucho
            lz.trazo(rect_red(-w / 2, -h / 2, w, h, 4), ROJO_DOCU, ancho=5.0, cerrado=True)
            lz.trazo(rect_red(-w / 2 + 6, -h / 2 + 6, w - 12, h - 12, 2), ROJO_DOCU, ancho=2.0, cerrado=True)
            lz.texto(txt, 0, px * 0.08, px, FUENTE_TAG, color=ROJO_DOCU, borde=None, alfa=0.92)


def dibujar_tarjeta_archivo(lz, x, y, w, h, rot, k):
    """Lámina de expediente con borde desgastado y ligera rotación 3D."""
    if k <= 0:
        return
    with lz.capa(0):
        with lz.grupo(x, y, k, rot=math.radians(rot)):
            # Sombra
            lz.relleno(rect_red(-w / 2 + 10, -h / 2 + 15, w, h, 8), (0, 0, 0), alfa=0.45)
            # Papel manila / archivo antiguo
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, 8), (225, 215, 195), alfa=0.95)
            # Clip o grapa arriba
            lz.trazo(rect_red(-30, -h / 2 - 12, 60, 24, 6), (120, 120, 130), ancho=4.0, cerrado=True)


class _BaseDocu(Escena):
    """Base de documental: tipografía Baskerville, etiquetas de expediente y grano de cine."""

    def preparar_comun(self, solo_abajo=False):
        self.claves = []
        slots = [sl for sl in SLOTS if sl[1] > H * 0.5] if solo_abajo else SLOTS
        for i, (palabra, texto) in enumerate(self.d.get("claves", [])[:4]):
            tc = _palabra(self, palabra, self.t0 + 0.6 + 1.2 * i)
            self.claves.append((tc, texto.upper()[:24], slots[i % len(slots)]))
            self.ev(tc, "pop", 0.45, pan=-0.3 if slots[i % len(slots)][0] < CX else 0.3, tono=0.9 + 0.1 * i)

        self.t_cifra = None
        if self.d.get("cifra"):
            self.t_cifra = _palabra(self, self.d.get("cifra_palabra"), self.t0 + 1.0)
            self.ev(self.t_cifra, "impacto", 0.8)

        # Sello de archivo si está indicado o en momentos clave
        self.estampa_txt = self.d.get("estampa") or ("EXPEDIENTE" if self.idx == 0 else "EVIDENCIA")
        self.t_estampa = self.t0 + 0.45
        self.ev(self.t_estampa, "impacto", 0.75, dur=0.3)

    def fondo(self, t):
        return fondo_archivo(t)

    def camara(self, t):
        u = t - self.t0
        # Zoom lento de investigación (efecto cámara lenta estilo documental)
        return (1.0 + 0.03 * prog(u, 0, self.t1 - self.t0), 0.003 * math.sin(u * 0.2),
                10 * math.sin(u * 0.18), 8 * math.cos(u * 0.22))

    def rotulo(self, lz, t):
        tit = self.d.get("titulo")
        if not tit:
            return
        k = pop(t, self.t0 + 0.1, 0.35) * sale(t, self.t1 - 0.22, 0.22)
        if k > 0:
            with lz.capa(2):
                lz.texto(tit.upper()[:28], CX, Y_TITULO, 40 if VERT else 38, FUENTE_TITULO,
                         color=AMARILLO_DOCU, borde=(10, 8, 6), borde_px=8, k=k)

    def dibujar_claves(self, lz, t):
        for i, (tc, texto, (x, y)) in enumerate(self.claves):
            k = pop(t, tc, 0.28) * sale(t, self.t1 - 0.2, 0.2)
            if k > 0:
                with lz.capa(2):
                    px = 34 if VERT else 32
                    w = ancho_texto(texto, FUENTE_TAG, px) + 36
                    h = px * 1.5
                    with lz.grupo(x, y + 4 * math.sin(t * 1.6 + i), k):
                        lz.relleno(rect_red(-w / 2, -h / 2, w, h, 6), (18, 16, 14), alfa=0.9)
                        lz.trazo(rect_red(-w / 2, -h / 2, w, h, 6), AMARILLO_DOCU, ancho=2.0, cerrado=True)
                        lz.texto(texto, 0, px * 0.08, px, FUENTE_TAG, color=BLANCO_DOCU, borde=None)

    def dibujar_cifra(self, lz, t):
        if self.t_cifra is None:
            return
        k = pop(t, self.t_cifra, 0.35) * sale(t, self.t1 - 0.25, 0.25)
        if k > 0:
            txt = str(self.d["cifra"])[:14]
            px = min(220, int((W * 0.8) / max(1, ancho_texto(txt, FUENTE_TITULO, 100)) * 100))
            y = H * 0.22 if VERT else 240
            with lz.capa(2):
                lz.texto(txt, CX, y, px, FUENTE_TITULO, color=ROJO_DOCU,
                         borde=(15, 10, 8), borde_px=10, k=k * (1 + 0.04 * env_bombo(t)))

    def render(self, lz, t):
        img = Escena.render(self, lz, t)
        # Acabado cinematográfico de celuloide con viñeta, grano fino y partículas de polvo
        return D.acabado(img, t, fuerza_vineta=0.68, grano=0.038, polvo=0.25, teal=0.06, calido=0.04)


class IntroDocu(_BaseDocu):
    """Intro Documental: Título misterioso en Baskerville + lámina de archivo que se estampa."""

    def preparar(self):
        self.lineas = partir_lineas(config.TITULO.upper(), ANCHO_LIN)[:4]
        for i in range(len(self.lineas)):
            self.ev(0.12 + 0.3 * i, "impacto" if i == 0 else "pop", 0.75, tono=0.85 + 0.08 * i)
        self.fin_titulo = self.fr[1]["t0"] - 0.2 if len(self.fr) > 1 else max(self.t0 + 2.0, self.fr[0]["t1"] - 0.4)
        self.preparar_comun(solo_abajo=True)

    def dibujar(self, lz, t):
        sube = e_inout(prog(t, self.fin_titulo - 0.1, self.fin_titulo + 0.45))
        n = len(self.lineas)
        px = _px_que_cabe(self.lineas, (118 if n <= 2 else 96) if VERT else (112 if n <= 3 else 86), W * 0.82)
        y_fin = H * 0.18 if VERT else 165

        with lz.grupo(CX, lerp(CY, y_fin, sube), 1 - 0.42 * sube):
            for i, lin in enumerate(self.lineas):
                k = pop(t, 0.12 + 0.3 * i, 0.35)
                if k > 0:
                    with lz.capa(2):
                        lz.texto(lin, 0, -(n - 1) * px * 0.64 + i * px * 1.28, px, FUENTE_TITULO,
                                 color=AMARILLO_DOCU if i == 0 else BLANCO_DOCU,
                                 borde=(12, 10, 8), borde_px=10)

        # Sello que cae con fuerza
        k_sello = pop(t, self.t_estampa, 0.28)
        if k_sello > 0:
            y_sello = CY + (120 if VERT else 80)
            dibujar_sello_rojo(lz, self.estampa_txt, CX + 60, y_sello, k_sello, rot=-6.0)

        self.dibujar_claves(lz, t)


class LibreDocu(_BaseDocu):
    """Escena Documental: Carpeta de evidencia con dibujo central, etiquetas y sello."""

    def preparar(self):
        self.ic = self.d.get("icono") if self.d.get("icono") in ICONOS else "ojo"
        self.ic2 = self.d.get("icono2") if self.d.get("icono2") in ICONOS else None
        self.ev(self.t0 + 0.1, "aparicion", 0.5)
        n = len(self.fr)
        self.tc = (self.fr[n // 2]["t0"] - 0.2 if n > 1 else self.t0 + (self.t1 - self.t0) * 0.5) if self.ic2 else 1e9
        self.preparar_comun()

    def dibujar(self, lz, t):
        k = pop(t, self.t0 + 0.1, 0.4) * sale(t, self.t1 - 0.15, 0.2)
        mov = e_inout(prog(t, self.tc - 0.1, self.tc + 0.45))

        if VERT:
            p1, p2 = (CX, lerp(CY, H * 0.38, mov)), (CX, H * 0.67)
        else:
            p1, p2 = (lerp(CX, 540, mov), CY), (1380, CY)

        s1 = lerp(1.0, 0.76, mov)
        w_tarjeta = int((380 if VERT else 440) * s1)
        h_tarjeta = int((380 if VERT else 440) * s1)

        if k > 0:
            dibujar_tarjeta_archivo(lz, p1[0], p1[1], w_tarjeta, h_tarjeta, -2.5, k)
            dibujar_icono(lz, self.ic, p1[0], p1[1] + 6 * math.sin(t * 1.5), s1 * 0.9 * k, t)

        if self.ic2 and t >= self.tc:
            k2 = pop(t, self.tc + 0.1, 0.4) * sale(t, self.t1 - 0.15, 0.2)
            if k2 > 0:
                dibujar_tarjeta_archivo(lz, p2[0], p2[1], int(w_tarjeta * 0.85), int(h_tarjeta * 0.85), 3.0, k2)
                dibujar_icono(lz, self.ic2, p2[0], p2[1] + 6 * math.sin(t * 1.5 + 1), 0.72 * k2, t)

        # Sello de evidencia
        k_sello = pop(t, self.t_estampa, 0.25)
        if k_sello > 0:
            dibujar_sello_rojo(lz, self.estampa_txt, p1[0] + 120, p1[1] - 130, k_sello, rot=-11.0)

        self.dibujar_cifra(lz, t)
        self.dibujar_claves(lz, t)
        self.rotulo(lz, t)


class CierreDocu(_BaseDocu):
    """Cierre Documental: Gran veredicto / conclusión con sello 'CASO CERRADO'."""

    def preparar(self):
        self.fin = self.fr[-1]["t1"] + 0.12 if self.fr else self.t0 + 1.0
        self.ev(self.fin, "impacto", 0.9)
        self.preparar_comun()

    def dibujar(self, lz, t):
        if t >= self.fin:
            lineas = partir_lineas(self.d.get("cierre", "¿ENIGMA RESUELTO?").upper(), 13 if VERT else 20)[:4]
            px = _px_que_cabe(lineas, 104 if VERT else 98, W * 0.76)
            y0 = CY - (len(lineas) - 1) * px * 0.65
            with lz.capa(2):
                for i, lin in enumerate(lineas):
                    k = pop(t, self.fin + 0.14 * i, 0.38)
                    if k > 0:
                        lz.texto(lin, CX, y0 + i * px * 1.3, px, FUENTE_TITULO,
                                 color=AMARILLO_DOCU if i == 0 else BLANCO_DOCU,
                                 borde=(12, 10, 8), borde_px=10)

            k_sello = pop(t, self.fin + 0.5, 0.28)
            if k_sello > 0:
                dibujar_sello_rojo(lz, "CASO CERRADO", CX, CY + 140, k_sello, rot=-5.0)

        self.dibujar_claves(lz, t)
        self.rotulo(lz, t)

    def render(self, lz, t):
        img = _BaseDocu.render(self, lz, t)
        neg = prog(t, self.t1 - 0.6, self.t1 - 0.05)
        return img * (1 - neg) if neg > 0 else img


def clases_documental():
    n = len(TL["escenas"])
    return {e["id"]: (IntroDocu if k == 0 else CierreDocu if k == n - 1 else LibreDocu)
            for k, e in enumerate(TL["escenas"])}
