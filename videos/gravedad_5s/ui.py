# -*- coding: utf-8 -*-
"""Capa de interfaz del plano secuencia «gravedad 5 s» (capa 2, encima del mundo):
  - Contador superior «SEGUNDO 0..5» con puntos de avance (verde azulado en versión A, rojo coral en versión B).
  - Insignia superior izquierda «VERSIÓN A / VERSIÓN B».
  - Diagramas, reglas de altura (0 m a 5 m), manómetro de presión, vectores tangentes y tarjetas comparativas.
  - OJO: Poppins no tiene glifos para flechas Unicode ni superíndices: todas las flechas, checks y cruces son vectoriales.
"""
import math

import numpy as np

import plano as P
import kz_ui as KU
from motor import W, H, prog, clamp01, lerp, e_in, e_out, circulo, rect_red, ancho_texto
from mundo_comun import ventana, campana, pop
from anclas import A, Z1, Z2, Z3, Z4, B0, TOTAL
import kit_grav as KG
import ui_base as UB
from ui_base import ent, pildora, texto_q, ROJO_O, TEAL, AZUL_OSC, NARANJA, MORADO, VERDE
import mundo_paisaje as MP
import gente as G


# ======================================================================== contador de segundos e insignia
def segundo(t):
    """(versión, número 0..5, alfa) del contador superior."""
    if A.cero_a - 0.35 < t < A.sobreviviria + 0.8:
        n = 0
        dt_1 = (A.dos_v - A.cero_a) * 0.52
        dt_3 = A.dos_v + (A.cinco_ca - A.dos_v) * 0.36
        dt_4 = A.dos_v + (A.cinco_ca - A.dos_v) * 0.70
        for tt, v in ((A.cero_a + dt_1, 1), (A.dos_v, 2), (dt_3, 3), (dt_4, 4), (A.cinco_ca, 5)):
            if t >= tt:
                n = v
        return "A", n, ventana(t, A.cero_a - 0.1, A.sobreviviria + 0.5, 0.3, 0.4)
    if A.cero_b - 0.35 < t < A.suerte - 0.25:
        n = 0
        dt_1 = A.cero_b + (A.tres_b - A.cero_b) * 0.36
        dt_2 = A.cero_b + (A.tres_b - A.cero_b) * 0.70
        dt_4 = A.tres_b + (A.cinco_b - A.tres_b) * 0.55
        for tt, v in ((dt_1, 1), (dt_2, 2), (A.tres_b, 3), (dt_4, 4), (A.cinco_b, 5)):
            if t >= tt:
                n = v
        return "B", n, ventana(t, A.cero_b - 0.1, A.suerte - 0.35, 0.3, 0.4)
    return None, 0, 0.0


def _cambios_seg():
    dt_a1 = A.cero_a + (A.dos_v - A.cero_a) * 0.52
    dt_a3 = A.dos_v + (A.cinco_ca - A.dos_v) * 0.36
    dt_a4 = A.dos_v + (A.cinco_ca - A.dos_v) * 0.70
    dt_b1 = A.cero_b + (A.tres_b - A.cero_b) * 0.36
    dt_b2 = A.cero_b + (A.tres_b - A.cero_b) * 0.70
    dt_b4 = A.tres_b + (A.cinco_b - A.tres_b) * 0.55
    return [A.cero_a, dt_a1, A.dos_v, dt_a3, dt_a4, A.cinco_ca,
            A.cero_b, dt_b1, dt_b2, A.tres_b, dt_b4, A.cinco_b]


_CAMBIOS = _cambios_seg()


def contador(lz, t):
    v, n, a = segundo(t)
    if a <= 0.01 or v is None:
        return
    col = TEAL if v == "A" else (232, 74, 82)
    rp = 1.0
    for tc in _CAMBIOS:
        rp = max(rp, KU.repop(t, tc, 0.22, 0.35))
    x, y = W / 2, 74
    with lz.capa(2):
        lz.relleno(rect_red(x - 170 + 3, y - 44 + 5, 340, 112, 30), (10, 6, 40), alfa=0.24 * a)
        lz.relleno(rect_red(x - 170, y - 44, 340, 112, 30), (28, 24, 70), alfa=0.86 * a)
        lz.texto("SEGUNDO", x - 40, y - 4, 30, "geo", color=(224, 226, 246), borde=None, alfa=a, temblor=0.0)
        with lz.grupo(x + 98, y - 2, rp):
            lz.relleno(circulo(0, 0, 40, 40), col, alfa=a)
            lz.texto(str(n), 0, 3, 54, "geo_x", color=(255, 255, 255), borde=None, alfa=a, temblor=0.0)
        for i in range(6):
            cx = x - 136 + i * 34
            lz.relleno(circulo(cx, y + 42, 9, 16), col if i <= n else (82, 78, 124), alfa=a)


def insignia_version(lz, t):
    aA = ventana(t, A.suave - 0.2, A.sobreviviria + 0.6, 0.3, 0.4)
    aB = ventana(t, A.total - 0.2, A.suerte - 0.3, 0.3, 0.4)
    for a, letra, sub, col, t0 in (
        (aA, "VERSIÓN A · SUAVE", "solo tu peso en la superficie", TEAL, A.suave - 0.2),
        (aB, "VERSIÓN B · TOTAL", "toda la gravedad del universo", (232, 74, 82), A.total - 0.2),
    ):
        if a <= 0.01:
            continue
        k = KU.pop(t, t0)
        with lz.capa(2):
            with lz.grupo(44, 44, k):
                w1 = ancho_texto(letra, "geo_x", 28) + 38
                w2 = UB.ancho_q(sub, 24) + 32
                lz.relleno(rect_red(3, 5, w1, 48, 18), (10, 6, 40), alfa=0.24 * a)
                lz.relleno(rect_red(0, 0, w1, 48, 18), col, alfa=a)
                lz.texto(letra, w1 / 2, 25, 28, "geo_x", color=(255, 255, 255), borde=None, alfa=a, temblor=0.0)
                lz.relleno(rect_red(0, 56, w2, 40, 16), (28, 24, 70), alfa=0.84 * a)
                texto_q(lz, w2 / 2, 76, sub, 24, (236, 238, 252), alfa=a, capa=2)


# ======================================================================== UI por escena
def _ui_intro(lz, t, ctx, est):
    S = ctx.get("S")
    # 1. Salto en el parque: flecha vectorial de gravedad hacia abajo
    k, a = ent(t, A.salto - 0.05, Z1[0] - 0.15)
    if a > 0.01 and S is not None:
        px, py = S.pt(G.X_PROTA - 100, 225)
        with lz.capa(2):
            UB.flecha(lz, (px, py - 85), (px, py + 25), col=(255, 214, 76), ancho=7.5, punta=22.0, alfa=a)
        pildora(lz, px - 140, py - 35, "GRAVEDAD: 9,8 m/s2", px=30, k=k, fondo=(28, 24, 70), color=(255, 224, 108), alfa=a)

    # 2. En el espacio: MITO de salir disparados como cohetes
    k, a = ent(t, A.creen, A.rara - 0.1)
    if a > 0.01:
        pildora(lz, 1380, 250, "MITO: salir volando como cohetes", px=32, k=k, fondo=ROJO_O, color=(255, 255, 255),
                alfa=a, icono="cruz")

    # 3. Tarjetas de las dos versiones del experimento
    k1, a1 = ent(t, A.depende - 0.1, Z2[0] - 0.1)
    if a1 > 0.01:
        with lz.capa(2):
            for idx, (yy, tit, sub, col, t0) in enumerate((
                (390, "1. VERSIÓN SUAVE", "Solo desaparece tu peso aquí", TEAL, A.depende),
                (565, "2. VERSIÓN TOTAL", "Toda la gravedad del universo", ROJO_O, A.apagues - 0.2),
            )):
                kk = KU.pop(t, t0)
                if kk <= 0.01:
                    continue
                with lz.grupo(1410, yy, kk):
                    lz.relleno(rect_red(-290 + 4, -62 + 6, 580, 124, 24), (10, 6, 40), alfa=0.28 * a1)
                    lz.relleno(rect_red(-290, -62, 580, 124, 24), (28, 24, 70), alfa=0.90 * a1)
                    lz.relleno(rect_red(-274, -48, 548, 44, 16), col, alfa=a1)
                    lz.texto(tit, 0, -25, 28, "geo_x", color=(255, 255, 255), borde=None, alfa=a1, temblor=0.0)
                    lz.texto(sub, 0, 26, 28, "geo", color=(234, 238, 255), borde=None, alfa=a1, temblor=0.0)


def _ui_version_a(lz, t, ctx, est):
    S = ctx.get("S")
    if S is None:
        return
    # 1. En la casa: flotando a ras del piso
    k, a = ent(t, A.quieto - 0.1, A.caminando - 0.25)
    if a > 0.01:
        cx, cy = S.pt(MP.X_CASA, 365)
        pildora(lz, cx, max(210, cy), "QUIETO EN CASA: solo flotas a ras del piso", px=31, k=k,
                fondo=(255, 255, 255), color=AZUL_OSC, alfa=a, icono="check")

    # 2. Caminando en el parque: regla vertical de 0 a 5 metros junto al árbol
    k, a = ent(t, A.impulso - 0.1, A.aire_a + 0.2)
    if a > 0.01:
        rx, y0 = S.pt(MP.X_ARBOL_5M - 70, 0)
        _, y5 = S.pt(MP.X_ARBOL_5M - 70, 275)
        with lz.capa(2):
            lz.trazo(np.array([[rx, y0], [rx, y5]], float), (255, 255, 255, int(230 * a)), 4.5, afinar=False)
            for m_i in range(6):
                ym = lerp(y0, y5, m_i / 5.0)
                lz.trazo(np.array([[rx - 12, ym], [rx + 12, ym]], float), (255, 255, 255, int(230 * a)), 3.5, afinar=False)
                if m_i in (0, 5):
                    lz.texto(f"{m_i} m", rx - 46, ym + 2, 28, "geo_x", color=(255, 255, 255), borde=None, alfa=a, temblor=0.0)
            alt_u = clamp01(est.get("alt_parque", 0.0))
            yp = lerp(y0, y5, alt_u)
            UB.flecha(lz, (rx, y0 - 10), (rx, min(y0 - 35, yp)), col=(110, 240, 210), ancho=6.5, punta=20.0, alfa=a)
        pildora(lz, W / 2, 205, f"IMPULSO AL CAMINAR: 1 m/s  ({alt_u * 5.0:.1f} m)", px=31, k=k,
                fondo=TEAL, color=(255, 255, 255), alfa=a)

    # 3. Perros, bicicletas y tazas en cámara lenta
    k, a = ent(t, A.perros - 0.1, A.aire_a + 0.3)
    if a > 0.01:
        pildora(lz, W / 2, 965, "PERROS · BICICLETAS · CAFÉ EN CÁMARA LENTA", px=31, k=k,
                fondo=(28, 24, 70), color=(255, 228, 122), alfa=a)


def _ui_viento_mar(lz, t, ctx, est):
    S = ctx.get("S")
    # 1. Atmósfera como resorte que rebota hacia arriba y caída de presión
    k, a = ent(t, A.atmosfera - 0.15, A.oidos - 0.15)
    if a > 0.01:
        estir = e_out(prog(t, A.rebota_v - 0.15, A.golpe_v + 0.3))
        with lz.capa(2):
            lz.relleno(rect_red(1380 - 210, 250, 420, 320, 26), (24, 20, 64), alfa=0.86 * a)
            KG.resorte_aire(lz, 1290, 515, 105.0, estir, col=(126, 218, 255), alfa=a)
            niv_p = 1.0 - 0.45 * estir
            lz.relleno(rect_red(1430, 315, 38, 190, 12), (56, 52, 96), alfa=a)
            h_b = 190 * niv_p
            lz.relleno(rect_red(1430, 315 + (190 - h_b), 38, h_b, 12), (240, 110, 84) if estir > 0.3 else TEAL, alfa=a)
            UB.flecha(lz, (1492, 330), (1492, 490), col=(255, 196, 128), ancho=5.5, punta=16.0, alfa=a)
            lz.texto("AIRE", 1290, 542, 26, "geo_x", color=(180, 232, 255), borde=None, alfa=a, temblor=0.0)
            lz.texto("PRESIÓN", 1450, 542, 26, "geo_x", color=(255, 196, 128), borde=None, alfa=a, temblor=0.0)
        pildora(lz, 1380, 205, "EL AIRE REBOTA COMO UN RESORTE", px=30, k=k, fondo=NARANJA, color=(255, 255, 255), alfa=a)

    # 2. Golpe seco en los oídos
    k, a = ent(t, A.oidos - 0.1, A.coches_v - 0.15)
    if a > 0.01 and S is not None:
        px, py = S.pt(G.X_PROTA + 65 + est.get("deriva", 0.0) * 115.0, 210 + est.get("alt_parque", 0.0) * 275.0)
        for rr in (42, 72):
            P.onda(lz, px, py - 45, rr * (0.8 + 0.3 * ((t * 3) % 1)), 6.0, (255, 118, 108), alfa=a * 0.75)
        pildora(lz, W / 2, 210, "¡GOLPE SECO EN LOS OÍDOS! (CAÍDA DE PRESIÓN)", px=32, k=k,
                fondo=ROJO_O, color=(255, 255, 255), alfa=a)

    # 3. Burbujas flotantes de agua y coches
    k, a = ent(t, A.coches_v - 0.1, A.gira - 0.15)
    if a > 0.01:
        pildora(lz, W / 2, 210, "COCHES Y OLAS EN GRANDES BURBUJAS FLOTANTES", px=31, k=k,
                fondo=TEAL, color=(255, 255, 255), alfa=a)

    # 4. Rotación terrestre y deriva tangencial en línea recta
    k, a = ent(t, A.gira - 0.1, A.cinco_ca - 0.2)
    if a > 0.01:
        with lz.capa(2):
            UB.flecha(lz, (520, 265), (1400, 265), col=(255, 224, 96), ancho=9.0, punta=28.0, alfa=a,
                      frac=clamp01(prog(t, A.gira, A.moverse + 0.5)))
        pildora(lz, W / 2, 205, "GIRO TERRESTRE (1 600 km/h): DERIVA EN LÍNEA RECTA", px=31, k=k,
                fondo=(28, 24, 70), color=(255, 226, 104), alfa=a)


def _ui_caida_a(lz, t, ctx, est):
    # 1. La gravedad regresa de golpe: flechas rojas hacia abajo
    k, a = ent(t, A.cinco_ca - 0.05, A.humanidad - 0.2)
    if a > 0.01:
        with lz.capa(2):
            for xx in (380, 760, 1160, 1540):
                UB.flecha(lz, (xx, 250), (xx, 420), col=ROJO_O, ancho=8.0, punta=24.0, alfa=a * 0.85)
        pildora(lz, W / 2, 205, "¡VUELVE LA GRAVEDAD! TODO CAE DE 5 A 10 METROS", px=32, k=k,
                fondo=ROJO_O, color=(255, 255, 255), alfa=a)

    # 2. En la versión suave la humanidad sobreviviría
    k, a = ent(t, A.humanidad - 0.15, Z3[0] - 0.1)
    if a > 0.01:
        pildora(lz, W / 2, 210, "VERSIÓN SUAVE: GOLPE DURÍSIMO, PERO SOBREVIVIMOS", px=34, k=k,
                fondo=VERDE, color=(255, 255, 255), alfa=a, icono="check")


def _ui_version_b(lz, t, ctx, est):
    # 1. Interior aplastado y corteza rota con lava
    k, a = ent(t, A.cero_b - 0.1, A.tres_b - 0.55)
    if a > 0.01:
        pildora(lz, 1430, 250, "NÚCLEO A MILLONES DE ATMÓSFERAS", px=30, k=k,
                fondo=(28, 24, 70), color=(255, 216, 102), alfa=a)
        if t > A.rebota_b - 0.15:
            k2, a2 = ent(t, A.rebota_b - 0.1, A.tres_b - 0.55)
            pildora(lz, 1430, 340, "LA CORTEZA SE ROMPE Y BROTA LAVA", px=30, k=k2,
                    fondo=ROJO_O, color=(255, 255, 255), alfa=a2)

    # 2. Segundo 3: Tierra y Luna salen en línea recta
    k, a = ent(t, A.tres_b - 0.05, A.sol_b - 0.45)
    if a > 0.01:
        pildora(lz, 1380, 230, "SIN ÓRBITA: TIERRA Y LUNA SALEN EN LÍNEA RECTA", px=30, k=k,
                fondo=(28, 24, 70), color=(132, 232, 255), alfa=a)

    # 3. El Sol se hincha y apaga su fusión nuclear
    k, a = ent(t, A.sol_b - 0.05, A.nuclear + 0.45)
    if a > 0.01:
        pildora(lz, 1410, 210, "EL SOL SE HINCHA Y APAGA SU FUSIÓN NUCLEAR", px=30, k=k,
                fondo=NARANJA, color=(255, 255, 255), alfa=a, icono="cruz")

    # 4. Segundo 5: desplome y superficie fundida
    k, a = ent(t, A.cinco_b - 0.1, A.suerte - 0.25)
    if a > 0.01:
        pildora(lz, W / 2, 945, "¡COLAPSO EN SEGUNDO 5! TODA LA SUPERFICIE SE FUNDE", px=34, k=k,
                fondo=ROJO_O, color=(255, 255, 255), alfa=a)


def _ui_cierre(lz, t, ctx, est):
    # 1. En el espacio: interruptor tachado + curvatura del espacio
    k, a = ent(t, A.suerte - 0.1, Z4[0] - 0.15)
    if a > 0.01:
        with lz.capa(2):
            with lz.grupo(1440, 470, k):
                lz.relleno(rect_red(-220 + 4, -155 + 6, 440, 310, 28), (10, 6, 40), alfa=0.28 * a)
                lz.relleno(rect_red(-220, -155, 440, 310, 28), (28, 24, 70), alfa=0.88 * a)
                P.interruptor(lz, 0, -25, 1.35, encendido=1.0)
                UB.prohibido(lz, 0, -25, 92, alfa=a, color=ROJO_O)
                lz.texto("SIN INTERRUPTOR", 0, 108, 30, "geo_x", color=(255, 255, 255), borde=None, alfa=a, temblor=0.0)
        if t > A.forma - 0.2:
            k2, a2 = ent(t, A.forma - 0.15, Z4[0] - 0.15)
            pildora(lz, 750, 915, "ES LA CURVATURA DEL ESPACIO POR CADA ÁTOMO", px=32, k=k2,
                    fondo=TEAL, color=(255, 255, 255), alfa=a2, icono="check")

    # 2. De vuelta en el parque: cierre cálido
    k, a = ent(t, A.tiron - 0.1, A.fin - 0.2)
    if a > 0.01:
        pildora(lz, W / 2, 190, "EL TIRÓN INVISIBLE QUE UNE EL MAR, EL AIRE Y EL SOL", px=33, k=k,
                fondo=(28, 24, 70), color=(255, 228, 118), alfa=a, icono="check")


def dibujar(lz, t, ctx, est):
    contador(lz, t)
    insignia_version(lz, t)
    _ui_intro(lz, t, ctx, est)
    _ui_version_a(lz, t, ctx, est)
    _ui_viento_mar(lz, t, ctx, est)
    _ui_caida_a(lz, t, ctx, est)
    _ui_version_b(lz, t, ctx, est)
    _ui_cierre(lz, t, ctx, est)


def post(img, t, ctx, est):
    return img
