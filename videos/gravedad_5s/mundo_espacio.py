# -*- coding: utf-8 -*-
"""El espacio exterior en «gravedad 5 s»:
  1) Intro (Z1..Z2): la Tierra vista desde el espacio con Kuri en escafandra; mito de salir disparados como cohetes;
     presentación de las dos versiones.
  2) Versión B (Z3..A.suerte):
     - Segundo 0: corte del interior terrestre aplastado por el peso de la roca -> rebota hacia afuera, la corteza se rompe
       y brota lava incandescente.
     - Segundo 3: la Tierra y la Luna abandonan su órbita circular y salen disparadas en línea recta tangente;
       el Sol en corte pierde el equilibrio, se hincha y apaga su fusión nuclear.
     - Segundo 5: al regresar la gravedad, la Tierra hinchada se desploma sobre sí misma en una esfera de roca fundida.
  3) Cierre en el espacio (A.suerte..Z4): malla de espacio-tiempo curvada por la masa de la Tierra y de los átomos.
"""
import math

import numpy as np

import fondos as F
import plano as P
import kz_espacio as KE
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, circulo, elipse, rect_red, h01
from mundo_comun import pop, ventana, campana
from anclas import A, Z1, Z2, Z3, Z4
import kit_grav as KG
import ui_base as UB

ROT0 = 1.85


def fondo(t, ex=960.0, ey=560.0):
    return F.espacio(t, brillo_est=1.0, dx=-(ex - 960) * 0.05, dy=-(ey - 560) * 0.05)


def kuri_espacio(lz, t, x, y, s, mirar=(0.0, 0.0), feliz=0.0, aleteo=0.0, boca=0.0, alfa=1.0):
    """Kuri flotando en el espacio con casco de cristal transparente."""
    if alfa <= 0.01:
        return
    bob = 11 * math.sin(t * 1.5)
    rot = 0.09 * math.sin(t * 0.95)
    with lz.grupo(x, y + bob, s, rot):
        P.kuri(lz, 0, 70, 1.0, t, mirar=mirar, feliz=feliz, aleteo=aleteo, boca=boca)
        lz.relleno(circulo(0, -5, 110, 60), (200, 232, 255), alfa=0.20 * alfa)
        lz.relleno(P.borde_luz(0, -5, 110, -math.pi * 0.75, 0.07), (255, 255, 255), alfa=0.55 * alfa)
        lz.relleno(rect_red(-50, 72, 100, 22, 10), (200, 206, 232), alfa=alfa)


def _cohetes_mito(lz, t, x, y, r):
    """Personas/cohetes saliendo disparados radialmente de la Tierra (el mito viral)."""
    a = ventana(t, A.creen - 0.2, A.rara + 0.2, 0.25, 0.35)
    if a <= 0.01:
        return
    u = clamp01(prog(t, A.volando - 0.35, A.cohetes + 0.9))
    angulos = [-2.35, -1.65, -0.85, -0.20, 0.55, 2.45]
    for k, ang in enumerate(angulos):
        d0 = r * 1.02
        d1 = r * (1.18 + 0.68 * u * (0.85 + 0.1 * (k % 3)))
        p0 = [x + d0 * math.cos(ang), y + d0 * math.sin(ang)]
        p1 = [x + d1 * math.cos(ang), y + d1 * math.sin(ang)]
        P.discontinua(lz, np.array([p0, p1], float), (255, 214, 120, int(210 * a)), 4.0, 16.0, 12.0, fase=-t * 28)
        with lz.grupo(p1[0], p1[1], 0.45 * (r / 280.0), ang + math.pi / 2):
            # Flama de cohete y silueta de personita
            lz.relleno(np.array([[-14, 10], [14, 10], [0, 52 + 12 * math.sin(t * 18 + k)]], float), (255, 146, 62), alfa=a)
            lz.relleno(np.array([[-8, 10], [8, 10], [0, 34]], float), (255, 232, 118), alfa=a)
            P.humano(lz, 0, 12, 0.55, t, ropa=(238, 88, 102), brazo=1.0)


def _tierra_interior_y_lava(lz, t, x, y, r):
    """En la versión B: corte del núcleo terrestre, expansión, grietas de lava y colapso fundido en Segundo 5."""
    # 1. Corte del núcleo comprimido (Segundo 0)
    a_int = ventana(t, A.cero_b - 0.3, A.tres_b - 0.55, 0.3, 0.35)
    reb = e_out(prog(t, A.rebota_b - 0.2, A.lava + 0.9))
    colapso = e_in(prog(t, A.cinco_b, A.desploma + 0.3))
    funde = ventana(t, A.cinco_b + 0.15, A.suerte - 0.3, 0.25, 0.6)

    if a_int > 0.01:
        # Capas internas visibles sobre el disco terrestre: manto rojizo, núcleo externo naranja, núcleo interno blanco-amarillo
        for f_r, col in ((0.78, (198, 62, 58)), (0.52, (244, 128, 48)), (0.26, (255, 232, 132))):
            lz.relleno(circulo(x, y, r * f_r * (1.0 + 0.12 * reb), 64), col, alfa=0.88 * a_int)
        # Flechas de presión hacia adentro (antes de soltar) o rebotando hacia afuera
        for k in range(8):
            ang = k * math.pi / 4 + 0.2
            if reb < 0.15:
                p_ext = (x + r * 1.34 * math.cos(ang), y + r * 1.34 * math.sin(ang))
                p_int = (x + r * 1.04 * math.cos(ang), y + r * 1.04 * math.sin(ang))
                UB.flecha(lz, p_ext, p_int, col=(255, 214, 92), ancho=7.0, punta=20.0, alfa=a_int * (1 - reb * 5))
            else:
                p_int = (x + r * 0.65 * math.cos(ang), y + r * 0.65 * math.sin(ang))
                p_ext = (x + r * (1.15 + 0.28 * reb) * math.cos(ang), y + r * (1.15 + 0.28 * reb) * math.sin(ang))
                UB.flecha(lz, p_int, p_ext, col=(255, 120, 68), ancho=7.5, punta=22.0, alfa=a_int)

    # 2. Grietas de lava y fragmentos de corteza cuando la Tierra se rompe
    a_lava = ventana(t, A.rompe - 0.25, A.tres_b - 0.55, 0.2, 0.35) + ventana(t, A.cinco_b - 0.15, A.suerte - 0.3, 0.2, 0.4)
    a_lava = min(1.0, a_lava)
    if a_lava > 0.01:
        u_lv = clamp01(prog(t, A.rompe - 0.2, A.lava + 0.8))
        for i in range(9):
            a0 = i * 2 * math.pi / 9 + 0.3
            pts = []
            for j in range(5):
                s = j / 4.0
                rr = r * (0.25 + 0.74 * s * u_lv)
                aa = a0 + 0.18 * math.sin(j * 1.9 + i)
                pts.append([x + rr * math.cos(aa), y + rr * math.sin(aa)])
            pts = np.array(pts, float)
            lz.trazo(pts, (255, 110, 48, int(240 * a_lava)), 10.0, afinar=True)
            lz.trazo(pts, (255, 234, 128, int(255 * a_lava)), 4.5, afinar=True)
        # Chorros de lava y rocas saliendo al espacio (antes del colapso)
        if colapso < 0.8 and t < A.tres_b:
            for i in range(14):
                ang = i * 2 * math.pi / 14 + 0.15
                d = r * (1.02 + (0.12 + 0.22 * h01(i, 2)) * u_lv * (1.0 - colapso))
                px, py = x + d * math.cos(ang), y + d * math.sin(ang)
                lz.halo(px, py, r * 0.14, (255, 130, 52), alfa=0.65 * a_lava * (1 - colapso))
                lz.relleno(circulo(px, py, r * (0.025 + 0.02 * h01(i, 5)), 14), (255, 206, 88), alfa=a_lava * (1 - colapso))

    # 3. Segundo 5: colapso violento y superficie fundida
    if funde > 0.01:
        lz.halo(x, y, r * 1.55, (255, 118, 48), alfa=0.82 * funde, r0=0.55)
        lz.relleno(circulo(x, y, r * 0.99, 96), (232, 74, 38), alfa=0.85 * funde)
        for i in range(7):
            ang = i * 0.9 + t * 0.2
            lz.relleno(elipse(x + r * 0.35 * math.cos(ang), y + r * 0.35 * math.sin(ang),
                              r * 0.32, r * 0.14, ang + 0.6, 28), (255, 198, 76), alfa=0.72 * funde)
        # Flechas de colapso gravitatorio hacia el centro y onda expansiva
        for k in range(8):
            ang = k * math.pi / 4 + 0.35
            p_ext = (x + r * 1.38 * math.cos(ang), y + r * 1.38 * math.sin(ang))
            p_int = (x + r * 1.04 * math.cos(ang), y + r * 1.04 * math.sin(ang))
            UB.flecha(lz, p_ext, p_int, col=(255, 214, 92), ancho=7.5, punta=22.0, alfa=funde)
        u_onda = prog(t, A.cinco_b + 0.1, A.funde + 0.5)
        if 0.0 < u_onda < 1.0:
            P.onda(lz, x, y, r * (0.95 + 0.9 * u_onda), 26.0, (255, 200, 110), alfa=(1.0 - u_onda) * 0.9)


def _orbita_y_sol(lz, t, ex, ey, r):
    """Segundo 3 de la versión B:
       - La Tierra y la Luna dejan su órbita curva y salen en línea recta tangente.
       - El Sol se hincha de golpe y apaga su fusión nuclear."""
    a_orb = ventana(t, A.tres_b - 0.1, A.nuclear + 0.45, 0.3, 0.35)
    if a_orb <= 0.01:
        return

    # Órbita curva punteada de la Luna alrededor de la Tierra y salida por la tangente
    u_recta = clamp01(prog(t, A.orbita - 0.2, A.espacio_b + 0.7))
    r_orb = r * 1.55
    P.discontinua(lz, elipse(ex, ey, r_orb, r_orb * 0.62, 0.0, 64), (160, 190, 255, int(130 * a_orb)), 4.0, 18.0, 12.0, fase=t * 18)
    ang0 = -0.85
    lx0 = ex + r_orb * math.cos(ang0)
    ly0 = ey + r_orb * 0.62 * math.sin(ang0)
    # Dirección tangente
    tx, ty = -math.sin(ang0), 0.62 * math.cos(ang0)
    norm = math.hypot(tx, ty)
    tx, ty = tx / norm, ty / norm
    lx = lx0 + tx * (210.0 * u_recta)
    ly = ly0 + ty * (210.0 * u_recta)
    if u_recta > 0.02:
        UB.flecha(lz, (lx0, ly0), (lx + tx * 55, ly + ty * 55), col=(130, 224, 255), ancho=6.0, punta=20.0, alfa=a_orb)
    KE.cuerpo_rocoso(lz, lx, ly, r * 0.28, tipo="luna", seed=4, rot=t * 0.2, alfa=a_orb)

    # Flecha tangente de la propia Tierra saliendo en línea recta
    UB.flecha(lz, (ex, ey - r * 1.08), (ex + 220 * max(0.2, u_recta), ey - r * 1.08 - 90 * max(0.2, u_recta)),
              col=(110, 236, 190), ancho=7.5, punta=24.0, alfa=a_orb)

    # El Sol a la derecha (entra cuando dice «Y el Sol...»)
    a_sol = ventana(t, A.sol_b - 0.25, A.nuclear + 0.45, 0.3, 0.35)
    if a_sol > 0.01:
        hincha = e_out(prog(t, A.hincha - 0.2, A.nuclear + 0.5))
        apaga = e_inout(prog(t, A.fusion - 0.2, A.nuclear + 0.6))
        sx, sy = 1410.0, 560.0
        rs = 230.0 * (1.0 + 0.32 * hincha) * pop(t, A.sol_b - 0.3)
        if rs > 5.0:
            P.sol(lz, sx, sy, rs, t, brillo=1.0 - 0.72 * apaga, apagado=apaga * 0.82)
            # Núcleo solar visible que se expande y pierde brillo
            r_nuc = rs * (0.28 + 0.24 * hincha)
            col_nuc = mezcla((255, 252, 220), (148, 54, 48), apaga)
            lz.relleno(circulo(sx, sy, r_nuc, 48), col_nuc, alfa=0.92 * a_sol)
            # Flechas radiales de expansión del Sol
            if hincha > 0.05:
                for k in range(8):
                    aa = k * math.pi / 4
                    p0 = (sx + rs * 0.55 * math.cos(aa), sy + rs * 0.55 * math.sin(aa))
                    p1 = (sx + rs * (0.95 + 0.25 * hincha) * math.cos(aa), sy + rs * (0.95 + 0.25 * hincha) * math.sin(aa))
                    UB.flecha(lz, p0, p1, col=(255, 196, 108), ancho=6.0, punta=18.0, alfa=a_sol * (1 - 0.5 * apaga))


def tierra(lz, t, x, y, r, extra=True):
    # En la versión B la Tierra se hincha al soltar la gravedad y se desploma en Segundo 5
    escala_b = 1.0
    if extra and A.rebota_b - 0.2 < t < A.suerte:
        sube = e_out(prog(t, A.rebota_b - 0.2, A.lava + 0.8))
        baja = e_in(prog(t, A.cinco_b, A.desploma + 0.2))
        escala_b = 1.0 + 0.17 * sube * (1.0 - baja) - 0.05 * baja * (1.0 - prog(t, A.suerte - 0.4, A.suerte))
    r_ef = r * escala_b

    # Malla de espacio-tiempo curvada debajo de la Tierra durante el inicio del cierre
    a_malla = ventana(t, A.suerte - 0.3, Z4[0] + 0.2, 0.35, 0.35) if extra else 0.0
    if a_malla > 0.01:
        KG.malla_curva(lz, x, y + r_ef * 0.52, r_pozo=r_ef * 0.95, prof=r_ef * 0.52, alfa=a_malla)

    rot = ROT0 + t * 0.04
    P.tierra(lz, x, y, r_ef, t, rot=rot, ang_luz=math.pi * 1.15, luz=1.0, nubes=1.0, atmosfera=1.0)
    if not extra:
        return

    _cohetes_mito(lz, t, x, y, r_ef)
    _tierra_interior_y_lava(lz, t, x, y, r_ef)
    _orbita_y_sol(lz, t, x, y, r_ef)


def dibujar(lz, t, x, y, r):
    tierra(lz, t, x, y, r, extra=True)
    # Kuri en escafandra acompañando a la Tierra en el espacio (fuera de la órbita lunar)
    kx = x - r * 1.55 if not (A.tres_b - 0.3 < t < A.cinco_b - 0.2) else x - r * 1.95
    ky = y + r * 0.35 if t < A.suerte - 0.3 else y - r * 0.65
    feliz = 1.0 if t > A.suerte else 0.0
    boca = 0.85 if (A.desaparece < t < A.rara or A.cero_b < t < A.suerte) else 0.0
    aleteo = 0.7 if (A.rebota_b < t < A.suerte) else 0.2
    kuri_espacio(lz, t, max(125.0, kx), ky, 0.92, mirar=(0.7, -0.2), feliz=feliz, aleteo=aleteo, boca=boca)
