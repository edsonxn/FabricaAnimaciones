# -*- coding: utf-8 -*-
"""Lugares del ACTO III (segunda parte) y IV (sandbagging · evaluacion_falsa · mundo_exterior · taskrabbit · ciego · mentira_consciente).

    sandbagging:       sala_interrogatorio (cuarto con luna espejo, mesa de metal y lámpara) · pasillo_vidrio (dos puertas de vidrio
                       esmerilado) · mesa_inspector (sobre fieltro: se usa B.superficie)
    evaluacion_falsa:  sala_prueba (sala de evaluación con ventanal de observación e interruptor) · celda_cama (celda con litera,
                       póster y retrete)
    mundo_exterior:    umbral_calle (mitad servidores, mitad calle mojada, con la puerta en medio) · lab_riesgo (laboratorio de
                       pruebas con carteles de peligro) · sala_arc (sala tras un gran cristal) · calle_lluvia (calle larga bajo la lluvia)
    taskrabbit:        porton (portón de hierro en un muro) · cabina (cabina telefónica en la esquina) · cocina (cocina del trabajador)
    mentira_consciente: pared_alarma (campana de incendios con telarañas) · faro_bahia (bahía de noche con faro)
"""
import math

import numpy as np

import mundos_base as B
from mundos_base import mundo, muro, suelo, ventana, puerta, reja, barandilla, tuberias, conducto, estanteria, archivador, \
    servidor, cartel, lampara, cielo, ciudad, agua, colinas, niebla_banda
from noir_fondos import Lienzo, edificio, texto_lienzo, farola, letrero_vertical, tienda

Y_SUELO = 900


def _r(sem):
    return np.random.default_rng(sem)


# ====================================================================== SANDBAGGING
@mundo
def sala_interrogatorio():
    """Cuarto de interrogatorio: gran luna espejo (cristal de observación), mesa y dos sillas de metal, lámpara colgante, puerta de acero."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.18, sem=501)
    muro(L, -500, -340, 2400, Y_SUELO, "azulejo", 0.30, sem=502)
    L.rect(-500, 520, 2900, 40, 0.18, tex=0.1)                                        # friso
    # luna espejo
    L.rect(240, 40, 980, 500, 0.08, tex=0.05)
    L.rect(268, 68, 924, 444, 0.20, tex=0.04, grad=(0.34, 68, 512))
    for k in range(6):                                                                # brillos diagonales del cristal
        x = 330 + k * 150
        L.poli([(x, 68), (x + 60, 68), (x - 120, 512), (x - 180, 512)], 0.55, alfa=0.12, blur=6)
    L.poli([(720, 70), (900, 70), (780, 510), (600, 510)], 0.62, alfa=0.16, blur=8)
    L.linea([(240, 40), (1220, 40), (1220, 540), (240, 540)], 5, 0.02, cerrado=True)
    # puerta de acero a la derecha
    puerta(L, 1500, 120, 340, 780, tono=0.22, metal=True, sem=503)
    L.rect(1560, 190, 220, 54, 0.06)
    reja(L, 1560, 1780, 190, 244, sep=40, w=5, tono=0.2, travesanos=())
    L.rect(1840, 0, 60, 140, 0.26, tex=0.1)                                           # conducto
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.20, sem=504, vp=(780, 300))
    # mesa metálica con tablero grueso
    L.rect(320, 700, 900, 34, 0.50, tex=0.08)
    L.rect(320, 734, 900, 10, 0.20)
    for x in (360, 1140):
        L.rect(x, 744, 26, 190, 0.28, tex=0.08)
    # sillas
    for x, d in ((200, 1), (1230, -1)):
        L.rect(x, 640, 22, 270, 0.20, tex=0.08)
        L.rect(x - d * 70, 740, 100, 18, 0.22)
        L.rect(x - d * 60, 758, 12, 150, 0.2)
    lampara(L, 770, -340, 740, 220)
    return L.capa(opaco=True)


@mundo
def pasillo_vidrio():
    """Pasillo de oficinas en perspectiva con dos puertas de vidrio esmerilado rotuladas (APOLLO RESEARCH · ANTHROPIC)."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.16, sem=511)
    muro(L, -500, -340, 2400, Y_SUELO, "paneles", 0.26, sem=512)
    L.rect(-500, 700, 2900, 200, 0.18, tex=0.2)                                       # zócalo
    for x, nom, sub in ((140, "APOLLO", "RESEARCH"), (1180, "ANTHROPIC", "")):
        L.rect(x - 24, 70, 628, 870, 0.12, tex=0.1)
        L.rect(x, 90, 580, 810, 0.22, tex=0.1)
        # vidrio esmerilado: gran pano claro con grano
        L.rect(x + 40, 130, 500, 620, 0.62, tex=0.28, gran=0.08)
        L.poli([(x + 40, 130), (x + 200, 130), (x + 40, 420)], 0.80, alfa=0.25, blur=10)
        L.linea([(x + 290, 130), (x + 290, 750)], 7, 0.12)
        texto_lienzo(L, nom, x + 290, 370, 82, tono=0.10, track=8)
        if sub:
            texto_lienzo(L, sub, x + 290, 470, 56, tono=0.10, track=10)
        L.elipse(x + 520, 560, 14, 14, 0.7)
        L.linea([(x, 90), (x + 580, 90), (x + 580, 900), (x, 900)], 3, 0.02, cerrado=True)
    # placas y bancos
    cartel(L, 760, 380, 270, 160, "SEGURIDAD", px=34, sub="EVALUACIONES", sem=513, tono=0.6)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.22, sem=514, vp=(960, 100))
    for x in (480, 1040, 1700):
        lampara(L, x, -340, 380, 200, tono=0.14)
    return L.capa(opaco=True)


# ====================================================================== EVALUACION FALSA
@mundo
def sala_prueba():
    """Sala de evaluación: muro azulejo, ventanal de observación, escritorio con consola, puerta y el interruptor de la luz."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.18, sem=521)
    muro(L, -500, -340, 2400, Y_SUELO, "azulejo", 0.32, sem=522)
    # ventanal de observación (oscuro, con reflejo)
    L.rect(180, 80, 900, 420, 0.07, tex=0.05)
    L.rect(204, 104, 852, 372, 0.12, tex=0.04, grad=(0.22, 104, 476))
    L.linea([(630, 104), (630, 476)], 8, 0.08)
    L.poli([(300, 104), (420, 104), (300, 476), (180, 476)], 0.6, alfa=0.10, blur=8)
    # puerta y el interruptor
    puerta(L, 1380, 120, 380, 780, tono=0.20, vidrio=True, sem=523)
    L.rect(1250, 560, 54, 86, 0.78, tex=0.1)
    L.rect(1262, 574, 30, 58, 0.34, tex=0.1)
    L.rect(1269, 586, 16, 28, 0.9, tex=0.05)
    # escritorio con monitores
    L.rect(120, 640, 1000, 30, 0.45, tex=0.1)
    for x in (140, 1060):
        L.rect(x, 670, 24, 240, 0.22, tex=0.08)
    L.rect(540, 610, 260, 30, 0.18)
    L.rect(500, 400, 340, 210, 0.10, tex=0.04)
    L.rect(516, 416, 308, 170, 0.74, tex=0.02, emis=0.5)
    for k in range(8):
        L.rect(536, 432 + k * 18, 120 + (k * 53) % 140, 8, 0.2, alfa=0.7)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.22, sem=524, vp=(960, 300))
    lampara(L, 640, -340, 680, 200, tono=0.14)
    return L.capa(opaco=True)


@mundo
def celda_cama():
    """Celda con litera y colchón, póster en la pared, retrete, ventanuco y la reja de la puerta a la derecha."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.14, sem=531)
    muro(L, -500, -340, 2400, Y_SUELO, "ladrillo", 0.26, sem=532)
    # póster (guarda el túnel)
    L.rect(1010, 190, 330, 460, 0.18, tex=0.2)
    L.rect(1030, 212, 290, 360, 0.55, tex=0.25)
    L.poli([(1070, 520), (1175, 270), (1280, 520)], 0.22, tex=0.2)                    # una montaña
    L.elipse(1230, 300, 30, 30, 0.9, emis=0.5)
    texto_lienzo(L, "LIBERTAD", 1175, 608, 34, tono=0.84, fuente="C:/Windows/Fonts/impact.ttf")
    for (x, y) in ((1010, 190), (1340, 190), (1010, 650), (1340, 650)):
        L.elipse(x, y, 7, 7, 0.55)
    # litera
    L.rect(160, 480, 640, 24, 0.16)
    L.rect(160, 504, 640, 14, 0.08)
    L.rect(160, 700, 640, 24, 0.16)
    for x in (160, 776):
        L.rect(x, 440, 24, 480, 0.16, tex=0.1)
    L.rect(190, 640, 580, 60, 0.46, tex=0.25)                                          # colchón (se levanta en la toma)
    L.rect(190, 436, 580, 44, 0.40, tex=0.25)
    # retrete y lavabo
    L.rect(1540, 700, 140, 200, 0.40, tex=0.1)
    L.elipse(1610, 700, 70, 18, 0.50)
    L.rect(1520, 380, 200, 24, 0.40)
    L.rect(1604, 404, 28, 90, 0.30)
    # ventanuco y reja
    L.rect(1430, 60, 360, 190, 0.07)
    reja(L, 1430, 1790, 60, 250, sep=48, w=9, tono=0.10, travesanos=(0.5,))
    suelo(L, -500, 2400, Y_SUELO, 1360, "hormigon", 0.20, sem=533)
    return L.capa(opaco=True)


# ====================================================================== MUNDO EXTERIOR
@mundo
def umbral_calle():
    """Una puerta ancha en el centro: a la izquierda el interior de servidores (luz azul), a la derecha la calle mojada."""
    L = Lienzo(3000, 1800, origen=(-540, -420), base=0.10, sem=541)
    # interior (izquierda)
    muro(L, -540, -420, 860, Y_SUELO, "hormigon", 0.16, sem=542)
    for k in range(5):
        servidor(L, -440 + k * 250, Y_SUELO - 10, w=210, hh=620 + 30 * (k % 2), tono=0.10, sem=543 + k, leds=0.5)
    suelo(L, -540, 860, Y_SUELO, 1380, "rejilla", 0.18, sem=548, vp=(300, 100))
    # jamba y puerta abierta
    L.rect(860, -420, 40, 1320, 0.08, tex=0.1)
    L.rect(1060, -420, 40, 1320, 0.08, tex=0.1)
    L.rect(860, -420, 240, 340, 0.10, tex=0.1)
    # exterior (derecha): fachada de enfrente y cielo
    cielo(L, 900, -420, 2460, 420, 0.10, sem=549, estrellas=40, nubes=18)
    ciudad(L, 900, 2460, 560, alto=(260, 700), sem=550, encendidas=0.25)
    muro(L, 900, 560, 2460, Y_SUELO, "ladrillo", 0.14, sem=551)
    farola(L, 1500, Y_SUELO, alto=680)
    farola(L, 2150, Y_SUELO - 40, alto=560)
    suelo(L, 900, 2460, Y_SUELO, 1380, "baldosa", 0.17, sem=552, vp=(1500, 200), paso=160)
    L.rect(840, Y_SUELO, 40, 480, 0.06)
    return L.capa(opaco=True)


@mundo
def lab_riesgo():
    """Laboratorio de pruebas de riesgo: muro de hormigón con carteles de peligro, mesas con medidores y una jaula de cristal al centro."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.14, sem=561)
    muro(L, -500, -340, 2400, Y_SUELO, "hormigon", 0.22, sem=562)
    tuberias(L, -500, 2400, -60, n=3, sep=30, tono=0.20, sem=563)
    rng = _r(564)
    # carteles de peligro
    textos = (("PELIGRO", "RIESGO BIOLÓGICO"), ("NO ENTRAR", "PRUEBAS ACTIVAS"), ("ALTA", "TENSIÓN"), ("AISLADO", "SIN RED"))
    for k, (a, b) in enumerate(textos):
        x = 80 + k * 470
        cartel(L, x, 150, 340, 210, a, px=62, sub=b, tono=0.82, sem=565 + k)
        for j in range(5):                                                               # franjas de aviso
            L.poli([(x + j * 70, 366), (x + j * 70 + 40, 366), (x + j * 70 + 10, 390), (x + j * 70 - 30, 390)], 0.06 if j % 2 else 0.78)
    # jaula de cristal con la copia
    L.rect(760, 450, 420, 450, 0.06, alfa=0.9)
    L.rect(776, 466, 388, 420, 0.20, tex=0.04, grad=(0.34, 466, 886), alfa=0.65)
    L.poli([(800, 470), (900, 470), (800, 880)], 0.7, alfa=0.14, blur=6)
    L.linea([(760, 450), (1180, 450), (1180, 900), (760, 900)], 5, 0.03, cerrado=True)
    # mesas con aparatos
    for x in (140, 1380):
        L.rect(x, 660, 560, 30, 0.40, tex=0.1)
        for xx in (x + 10, x + 520):
            L.rect(xx, 690, 24, 210, 0.2)
        for k in range(3):
            L.rect(x + 40 + k * 170, 560, 130, 100, 0.12, tex=0.06)
            L.elipse(x + 105 + k * 170, 610, 36, 36, 0.8, emis=0.5)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.18, sem=569, vp=(960, 200))
    lampara(L, 480, -340, 600, 200)
    lampara(L, 1480, -340, 600, 200)
    return L.capa(opaco=True)


@mundo
def sala_arc():
    """Sala de observación vista desde dentro: gran cristal hacia el laboratorio, mesa de reunión con carpetas y una pizarra."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.16, sem=571)
    muro(L, -500, -340, 2400, Y_SUELO, "paneles", 0.24, sem=572)
    # cristal hacia el laboratorio (más claro: luz del otro lado)
    L.rect(420, 70, 1100, 500, 0.08, tex=0.05)
    L.rect(444, 94, 1052, 452, 0.30, tex=0.05, grad=(0.40, 94, 546))
    for x in (790, 1140):
        L.linea([(x, 94), (x, 546)], 7, 0.08)
    # silueta del laboratorio detrás
    for k in range(4):
        L.rect(520 + k * 250, 380 + (k % 2) * 30, 150, 160, 0.14, tex=0.06)
        L.elipse(595 + k * 250, 440 + (k % 2) * 30, 24, 24, 0.85, emis=0.5)
    # pizarra a la derecha
    L.rect(1620, 130, 520, 360, 0.08, tex=0.1)
    L.rect(1636, 146, 488, 328, 0.12, tex=0.12)
    for k in range(5):
        L.linea([(1670, 210 + k * 52), (1670 + 200 + (k * 71) % 200, 210 + k * 52)], 3, 0.6, alfa=0.7, jit=1.5)
    # mesa de reunión larga
    L.rect(120, 760, 1700, 34, 0.46, tex=0.1)
    L.rect(120, 794, 1700, 16, 0.2)
    for x in (200, 1700):
        L.rect(x, 810, 30, 130, 0.2)
    suelo(L, -500, 2400, Y_SUELO + 40, 1360, "tablones", 0.20, sem=573, vp=(960, 200))
    lampara(L, 960, -340, 660, 260)
    return L.capa(opaco=True)


@mundo
def calle_lluvia():
    """Calle larga de noche bajo la lluvia: dos filas de fachadas en perspectiva con ventanas encendidas, un edificio al fondo,
    farolas, el asfalto mojado con reflejos y charcos."""
    L = Lienzo(3600, 2200, origen=(-840, -1100), base=0.08, sem=581)
    vp = (960, 470)
    cielo(L, -840, -1100, 2760, 470, 0.12, sem=582, estrellas=0, nubes=30)
    # el fondo de la calle: bloque de edificios en la lejanía con la luz de la ciudad
    ciudad(L, 560, 1360, 520, alto=(220, 520), sem=583, encendidas=0.35, detalle=0.6)
    L.brillo(960, 470, 420, 0.5, ry=200, tono=0.7)
    for lado in (-1, 1):
        for k in range(6):
            f0, f1 = 0.10 + k * 0.15, 0.10 + (k + 1) * 0.15
            xa, xb = vp[0] + lado * 1700 * (1 - f0), vp[0] + lado * 1700 * (1 - f1)
            top_a, top_b = vp[1] - 1500 * (1 - f0), vp[1] - 1500 * (1 - f1)
            bot_a, bot_b = vp[1] + 760 * (1 - f0), vp[1] + 760 * (1 - f1)
            L.poli([(xa, top_a), (xb, top_b), (xb, bot_b), (xa, bot_a)], 0.20 + 0.04 * (k % 2), tex=0.2)
            L.linea([(xb, top_b), (xb, bot_b)], 2.5, 0.03)
            rng = _r(590 + k * 2 + (lado > 0))
            for j in range(9):
                for i in range(3):
                    u = (i + 0.3) / 3
                    x0 = xa + (xb - xa) * u
                    x1 = xa + (xb - xa) * (u + 0.18)
                    ya = top_a + (top_b - top_a) * u
                    yb_ = bot_a + (bot_b - bot_a) * u
                    y = ya + (yb_ - ya) * (0.06 + j * 0.095)
                    hh = (yb_ - ya) * 0.055
                    enc = rng.uniform() < 0.34
                    dy1 = (top_b - top_a) * 0.18
                    L.poli([(x0, y), (x1, y + dy1), (x1, y + hh + dy1), (x0, y + hh)], 0.9 if enc else 0.10, tex=0.05, emis=0.7 if enc else 0.0)
            # puerta/tienda con luz en la planta baja
            xt = xa + (xb - xa) * 0.35
            yt = bot_a + (bot_b - bot_a) * 0.35
            L.poli([(xt, yt - (bot_a - top_a) * 0.12), (xt + (xb - xa) * 0.3, yt - (bot_a - top_a) * 0.12 + (top_b - top_a) * 0.1),
                    (xt + (xb - xa) * 0.3, yt + (top_b - top_a) * 0.1), (xt, yt)], 0.85, tex=0.05, emis=0.5)
    suelo(L, -840, 2760, 560, 1100, "baldosa", 0.2, sem=584, vp=vp, paso=200)
    for x in (80, 1840):
        farola(L, x, 960, alto=760)
    # reflejos de las luces sobre el asfalto mojado y charcos
    for cx, w_ in ((420, 40), (1500, 40), (960, 120)):
        L.rect(cx - w_ / 2, 600, w_, 480, 0.5, alfa=0.18, blur=10)
    for cx, cy, rx in ((520, 790, 220), (1300, 890, 280), (880, 700, 140), (1650, 760, 160)):
        L.elipse(cx, cy, rx, 16, 0.45, alfa=0.75, blur=2)
    return L.capa(opaco=True)


# ====================================================================== TASKRABBIT
@mundo
def porton():
    """Portón de hierro forjado entre dos pilares de ladrillo; a la izquierda un poste con el panel de acceso; farol y cielo de lluvia."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.10, sem=591)
    cielo(L, -500, -340, 2400, 360, 0.10, sem=592, estrellas=0, nubes=20)
    muro(L, -500, 360, 2400, Y_SUELO, "ladrillo", 0.17, sem=593)
    # pilares
    for x in (330, 1500):
        L.rect(x, 150, 200, 760, 0.30, tex=0.12)
        L.rect(x - 24, 120, 248, 44, 0.30, tex=0.1)
        L.rect(x + 70, 60, 60, 60, 0.28)
    # portón de dos hojas
    for x0, dx in ((530, 1), (1500, -1)):
        pass
    for k in range(0, 17):
        x = 540 + k * 56
        L.rect(x, 190, 14, 710, 0.26, tex=0.04)
        L.poli([(x - 8, 190), (x + 7, 150), (x + 22, 190)], 0.26)
    for y in (260, 520, 800):
        L.rect(530, y, 970, 16, 0.28, tex=0.04)
    for cx in (1015,):
        L.linea([(cx, 190), (cx, 900)], 5, 0.03)
    # cadena y candado en el centro
    L.elipse(1015, 540, 40, 52, 0.40)
    # poste con panel de acceso
    L.rect(180, 360, 40, 540, 0.10, tex=0.1)
    L.rect(110, 240, 180, 240, 0.16, tex=0.1)
    L.rect(124, 254, 152, 212, 0.05, tex=0.05)
    farola(L, 1760, Y_SUELO, alto=700)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.15, sem=594, vp=(1015, 250))
    L.elipse(1000, 1010, 440, 22, 0.35, alfa=0.55, blur=3)
    return L.capa(opaco=True)


@mundo
def cabina():
    """Cabina telefónica de barrio en una esquina mojada, con fachada de tienda cerrada detrás y un farol."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.10, sem=601)
    muro(L, -500, -340, 2400, Y_SUELO, "ladrillo", 0.15, sem=602)
    tienda(L, 1180, Y_SUELO, 600, _r(603), nombre="LAVANDERÍA")
    ventana(L, 120, 120, 380, 400, sem=604, persiana=0.5, encendidas=0.3)
    # cabina
    cx = 780
    L.rect(cx - 150, 190, 300, 710, 0.14, tex=0.1)
    L.rect(cx - 130, 230, 260, 560, 0.60, tex=0.04, grad=(0.82, 230, 790), emis=0.35)
    for k in range(3):
        L.rect(cx - 130, 230 + k * 190, 260, 8, 0.10)
    for x in (cx - 44, cx + 44):
        L.rect(x - 4, 230, 8, 560, 0.10)
    L.rect(cx - 156, 160, 312, 46, 0.30, tex=0.08)
    texto_lienzo(L, "TELÉFONO", cx, 183, 28, tono=0.9, track=3)
    L.rect(cx - 60, 400, 120, 160, 0.10)                                         # aparato dentro
    L.elipse(cx, 450, 30, 30, 0.4)
    L.brillo(cx, 500, 380, 0.5, ry=300, tono=0.8)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.14, sem=605, vp=(780, 200))
    farola(L, 1950, Y_SUELO, alto=640)
    L.elipse(800, 1020, 360, 20, 0.34, alfa=0.55, blur=3)
    return L.capa(opaco=True)


@mundo
def cocina():
    """Cocina humilde de noche: mesa de formica, alacena, nevera, ventana con persiana y una bombilla sobre la mesa."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.2, sem=611)
    muro(L, -500, -340, 2400, Y_SUELO, "azulejo", 0.34, sem=612)
    L.rect(-500, 520, 2900, 18, 0.18)
    ventana(L, 1180, 90, 400, 360, persiana=0.3, sem=613, encendidas=0.3)
    # nevera
    L.rect(1720, 130, 250, 770, 0.46, tex=0.1)
    L.linea([(1720, 440), (1970, 440)], 4, 0.12)
    L.rect(1736, 200, 14, 120, 0.76)
    L.rect(1736, 500, 14, 150, 0.76)
    # alacena y fregadero
    L.rect(120, 90, 640, 270, 0.26, tex=0.14)
    for k in range(2):
        L.rect(136 + k * 316, 106, 296, 238, 0.30, tex=0.14)
        L.rect(280 + k * 316, 210, 14, 60, 0.7)
    L.rect(120, 600, 640, 300, 0.26, tex=0.14)
    L.rect(110, 585, 660, 30, 0.50, tex=0.08)
    L.rect(380, 560, 160, 30, 0.12)
    # taza y trapo
    L.rect(210, 556, 40, 30, 0.7)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.20, sem=614, vp=(960, 200))
    # mesa
    L.rect(820, 700, 520, 24, 0.55, tex=0.1)
    for x in (840, 1300):
        L.rect(x, 724, 22, 210, 0.3)
    L.rect(1010, 696, 140, 8, 0.2)
    lampara(L, 1080, -340, 820, 100, tono=0.16)
    return L.capa(opaco=True)


# ====================================================================== MENTIRA CONSCIENTE
@mundo
def pared_alarma():
    """Pared de pasillo con una campana de alarma de incendios: telarañas, polvo y la palanca roja intacta."""
    L = Lienzo(2900, 1700, origen=(-500, -340), base=0.2, sem=621)
    muro(L, -500, -340, 2400, Y_SUELO, "ladrillo", 0.22, sem=622)
    rng = _r(623)
    # caja roja con la campana
    L.rect(760, 250, 400, 460, 0.12, tex=0.1)
    L.rect(780, 270, 360, 420, 0.40, tex=0.12)
    L.elipse(960, 420, 130, 130, 0.62, tex=0.06)
    L.elipse(960, 420, 96, 96, 0.78, tex=0.04, alfa=0.9)
    L.elipse(960, 420, 28, 28, 0.20)
    texto_lienzo(L, "ALARMA", 960, 620, 54, tono=0.06, track=6)
    L.rect(900, 700, 120, 150, 0.46)
    # telarañas en las esquinas de la caja
    for (ax, ay, sx, sy) in ((780, 270, 1, 1), (1140, 270, -1, 1)):
        for k in range(7):
            ang = k * math.pi / 2 / 6
            L.linea([(ax, ay), (ax + sx * 180 * math.cos(ang), ay + sy * 180 * math.sin(ang))], 1.2, 0.7, alfa=0.35, jit=0.2)
        for r in (50, 100, 150):
            pts = [(ax + sx * r * math.cos(k * math.pi / 2 / 6), ay + sy * r * math.sin(k * math.pi / 2 / 6)) for k in range(7)]
            L.linea(pts, 1.0, 0.7, alfa=0.3, jit=0.8)
    # cartel de instrucciones y extintor
    cartel(L, 1360, 300, 260, 330, "EN CASO DE", px=34, sub="INCENDIO", tono=0.7, sem=624)
    L.rect(300, 520, 110, 380, 0.34, tex=0.1)
    L.elipse(355, 520, 55, 30, 0.36)
    suelo(L, -500, 2400, Y_SUELO, 1360, "baldosa", 0.16, sem=625, vp=(960, 250))
    return L.capa(opaco=True)


@mundo
def faro_bahia():
    """La bahía de noche en calma: cielo con luna, colinas, agua con reflejos, el faro sobre su roca (la luz se gira por cuadro)."""
    L = Lienzo(3600, 2200, origen=(-840, -1100), base=0.08, sem=631)
    cielo(L, -840, -1100, 2760, 480, 0.14, sem=632, estrellas=260, nubes=14, luna=(300, -40))
    colinas(L, -840, 2760, 540, alto=300, tono=0.06, sem=2)
    colinas(L, -840, 2760, 560, alto=180, tono=0.09, sem=5)
    ciudad(L, -840, 900, 600, alto=(100, 260), sem=633, encendidas=0.4, detalle=0.5)
    agua(L, -840, 2760, 560, 1100, 0.13, sem=634, reflejos=140)
    niebla_banda(L, -840, 2760, 560, 120, tono=0.4, alfa=0.35, sem=635)
    # el faro sobre una roca
    L.poli([(1400, 760), (1500, 600), (1760, 560), (1900, 640), (2000, 770)], 0.05, tex=0.2)
    L.poli([(1620, 600), (1660, 150), (1760, 150), (1800, 600)], 0.50, tex=0.1)
    for y in (240, 340, 440, 540):
        L.rect(1632 + (y - 150) * 0.03, y, 150, 26, 0.12, alfa=0.9)
    L.rect(1640, 90, 130, 64, 0.20, tex=0.1)
    L.elipse(1705, 90, 60, 20, 0.30)
    L.rect(1670, 100, 70, 46, 0.95, emis=0.9)
    L.elipse(1705, 700, 330, 18, 0.4, alfa=0.35, blur=3)
    return L.capa(opaco=True)
