# -*- coding: utf-8 -*-
"""Miniatura de «La Independencia de México, completa»: python _mini.py [variante]  -> salida/independencia_mexico_mini_<variante>.jpg (1280x720) y previews/mini_<variante>.png"""
import math
import sys

import cv2
import numpy as np

import estilos
estilos.activar("kurzgesagt")
import efectos as E
import kz_retrato as R
import kz_ui as U
from motor import Lienzo, a_uint8, componer, catmull, circulo, elipse, rect_red, W, H
from util import bg_grad

T0 = 0.3
VAR = sys.argv[1] if len(sys.argv) > 1 else "campana"

NOCHE = (28, 18, 56)
NOCHE2 = (46, 26, 74)
ORO = (255, 196, 54)
ORO_S = (214, 140, 30)
ORO_L = (255, 238, 150)
AMARILLO = (255, 226, 30)


def fondo():
    bg = bg_grad((16, 10, 52), (255, 128, 58), mid=(92, 30, 110), ym=0.70)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # resplandor del amanecer en el horizonte y de la campana
    for cx, cy, rx, ry, col, a in ((1000, 860, 1250, 360, (255, 150, 60), 0.55), (640, 690, 380, 380, (255, 200, 80), 0.50)):
        d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        g = np.clip(1 - d, 0, 1) ** 1.7 * a
        bg = bg * (1 - g[..., None]) + np.float32(col) / 255 * g[..., None]
    return bg.astype(np.float32)


def montes(lz):
    rng = np.random.RandomState(4)
    for capa_y, col, amp, f in ((800, (70, 30, 92), 70, 0.006), (850, (40, 22, 70), 55, 0.009)):
        xs = np.linspace(-40, W + 40, 70)
        ys = capa_y - amp * (0.5 + 0.5 * np.sin(xs * f + 1.3) + 0.35 * np.sin(xs * f * 2.7 + 0.4)) + rng.randn(70) * 4
        pts = np.vstack([np.stack([xs, ys], 1), [[W + 40, H + 40], [-40, H + 40]]])
        lz.relleno(pts, col, capa=0)


def llama(lz, x, y, s, t, seed=0, capa=1):
    """Llama de antorcha / incendio (gota con núcleo amarillo)."""
    b = 1 + 0.08 * math.sin(t * 9 + seed * 2)
    ext = np.array([(0, -1.5 * b), (0.35, -0.8), (0.62, -0.1), (0.5, 0.45), (0, 0.7), (-0.5, 0.45), (-0.62, -0.1), (-0.3, -0.85)]) * s
    ext = catmull(ext, 6, True) + (x, y)
    lz.relleno(ext, (255, 110, 30), capa=capa)
    mid = catmull(np.array([(0, -1.0 * b), (0.25, -0.4), (0.38, 0.05), (0.28, 0.4), (0, 0.55), (-0.3, 0.4), (-0.38, 0.05), (-0.2, -0.45)]) * s, 6, True) + (x, y)
    lz.relleno(mid, (255, 190, 50), capa=capa)
    nuc = catmull(np.array([(0, -0.5 * b), (0.14, -0.1), (0.2, 0.2), (0, 0.38), (-0.2, 0.2), (-0.14, -0.1)]) * s, 6, True) + (x, y)
    lz.relleno(nuc, (255, 246, 200), capa=capa)


def campana(lz, x, y, s, t, ang=0.0):
    """Campana dorada de iglesia colgada de una viga (x, y = centro del cuerpo)."""
    c, sn = math.cos(ang), math.sin(ang)

    def tr(p):
        px, py = p
        return (x + (px * c - (py + 1.0) * sn) * s, y + (px * sn + (py + 1.0) * c) * s - s)
    perfil = [(0.0, -1.0), (0.16, -0.99), (0.28, -0.86), (0.36, -0.55), (0.46, -0.18), (0.66, 0.22), (0.86, 0.5), (0.97, 0.66), (1.0, 0.76)]
    perfil = [tuple(q) for q in catmull(np.array(perfil), 5, False)]
    der = [tr(p) for p in perfil]
    izq = [tr((-p[0], p[1])) for p in reversed(perfil)]
    cuerpo = np.array(izq + der)
    lz.relleno(catmull(cuerpo, 6, False) if False else cuerpo, ORO_S, capa=1)
    # cara iluminada (izquierda) y cara en sombra (derecha)
    luz = [tr((-p[0] * 0.97, p[1])) for p in perfil] + [tr((-p[0] * 0.30, p[1])) for p in reversed(perfil)]
    lz.relleno(np.array(luz), ORO, capa=1)
    n_ = len(perfil); brillo = [tr((-p[0] * 0.80, p[1] * 0.98)) for p in perfil[3:int(n_ * 0.78)]] + [tr((-p[0] * 0.62, p[1] * 0.98)) for p in reversed(perfil[3:int(n_ * 0.78)])]
    lz.relleno(np.array(brillo), ORO_L, alfa=0.85, capa=1)
    # borde inferior (labio) y bandas decorativas
    for yb, h in ((0.60, 0.06), (0.28, 0.05)):
        ancho = 0.66 + (yb - 0.22) * 0.72 if yb > 0.22 else 0.66
        a = [tr((-ancho, yb)), tr((ancho, yb)), tr((ancho * 1.02, yb + h)), tr((-ancho * 1.02, yb + h))]
        lz.relleno(np.array(a), (176, 104, 24), capa=1)
    lab = [tr((-1.0, 0.70)), tr((1.0, 0.70)), tr((1.06, 0.88)), tr((-1.06, 0.88))]
    lz.relleno(np.array(lab), ORO_S, capa=1)
    lab2 = [tr((-1.0, 0.70)), tr((-0.2, 0.70)), tr((-0.2, 0.88)), tr((-1.06, 0.88))]
    lz.relleno(np.array(lab2), ORO, capa=1)
    # badajo
    bx, by = tr((0.05, 1.12))
    lz.relleno(circulo(bx, by, 0.17 * s), (120, 70, 24), capa=1)
    lz.relleno(circulo(bx - 0.05 * s, by - 0.05 * s, 0.07 * s), ORO, capa=1)
    # corona / asa
    ax, ay = tr((0, -1.0))
    lz.relleno(rect_red(ax - 0.12 * s, ay - 0.16 * s, 0.24 * s, 0.2 * s, 0.05 * s), (120, 70, 24), capa=1)


def viga_campanario(lz, x, y, ancho, alto):
    """Dos pilares de cantera y una viga de madera de la que cuelga la campana."""
    for px in (x - ancho / 2 - 40, x + ancho / 2):
        lz.relleno(rect_red(px, y - 40, 40, alto, 6), (120, 66, 96), capa=0)
        lz.relleno(rect_red(px, y - 40, 14, alto, 6), (174, 100, 120), capa=0)
    lz.relleno(rect_red(x - ancho / 2 - 60, y - 70, ancho + 120, 44, 8), (86, 50, 44), capa=1)
    lz.relleno(rect_red(x - ancho / 2 - 60, y - 70, ancho + 120, 14, 8), (140, 90, 66), capa=1)


def texto_titulo(lz, l1, l2, y1=180, y2=395, px1=205, px2=170, x=64):
    kw = dict(fuente_="vox_x", ancla=(0.0, 0.5), temblor=0.0, capa=2)
    lz.texto(l1, x + 8, y1 + 10, px1, color=(8, 4, 20), borde=(8, 4, 20), borde_px=26, alfa=0.55, **kw)
    lz.texto(l1, x, y1, px1, color=(255, 255, 255), borde=(10, 6, 24), borde_px=22, **kw)
    lz.texto(l2, x + 8, y2 + 10, px2, color=(8, 4, 20), borde=(8, 4, 20), borde_px=24, alfa=0.55, **kw)
    lz.texto(l2, x, y2, px2, color=AMARILLO, borde=(10, 6, 24), borde_px=22, **kw)


def pueblo(lz, y_suelo=868):
    """Pueblo de Dolores al fondo (parroquia de dos torres, casitas y suelo), todo en silueta violeta sin figuras."""
    col, col2 = (46, 26, 74), (62, 34, 92)
    rim = (255, 140, 80)
    # suelo
    xs = np.linspace(-20, 1100, 40)
    ys = y_suelo + 6 * np.sin(xs * 0.011) + 3 * np.sin(xs * 0.05)
    lz.relleno(np.vstack([np.stack([xs, ys], 1), [[1100, H + 40], [-20, H + 40]]]), (34, 20, 58), capa=0)
    # parroquia (a la izquierda, lejos)
    bx = 200
    lz.relleno(rect_red(bx - 120, y_suelo - 150, 240, 150, 6), col2, capa=0)
    for tx in (bx - 150, bx + 70):
        lz.relleno(rect_red(tx, y_suelo - 270, 80, 270, 5), col2, capa=0)
        lz.relleno(np.array([(tx - 6, y_suelo - 270), (tx + 86, y_suelo - 270), (tx + 40, y_suelo - 340)]), col, capa=0)
        lz.relleno(rect_red(tx + 24, y_suelo - 238, 32, 60, 14), (255, 190, 90), alfa=0.85, capa=0)
        lz.relleno(rect_red(tx, y_suelo - 270, 10, 270, 4), rim, alfa=0.45, capa=0)
    lz.relleno(circulo(bx, y_suelo - 150, 50), col2, capa=0)
    lz.relleno(rect_red(bx - 26, y_suelo - 70, 52, 70, 22), (255, 190, 90), alfa=0.8, capa=0)
    # casitas
    for hx, hw, hh in ((20, 90, 70), (360, 110, 85), (500, 90, 60), (760, 120, 80), (900, 100, 66), (1010, 110, 74)):
        if abs(hx - 640) < 0:
            continue
        lz.relleno(rect_red(hx, y_suelo - hh, hw, hh, 4), col, capa=0)
        lz.relleno(np.array([(hx - 8, y_suelo - hh), (hx + hw + 8, y_suelo - hh), (hx + hw - 10, y_suelo - hh - 22), (hx + 10, y_suelo - hh - 22)]), col2, capa=0)
        lz.relleno(rect_red(hx + hw * 0.4, y_suelo - hh * 0.55, hw * 0.2, hh * 0.35, 3), (255, 190, 90), alfa=0.8, capa=0)


def agave(lz, x, y, L, col=(26, 58, 78), rim=(255, 140, 80), capa=1):
    """Maguey de frente: abanico de pencas puntiagudas desde el suelo."""
    for a in (-72, -52, -34, -16, 0, 16, 34, 52, 72):
        r = math.radians(a)
        dx, dy = math.sin(r), -math.cos(r)
        nx, ny = -dy, dx
        l = L * (1.0 - abs(a) / 220)
        w = L * 0.09
        base = (x, y)
        tip = (x + dx * l, y + dy * l)
        mid = (x + dx * l * 0.5, y + dy * l * 0.5)
        pts = np.array([(base[0] + nx * w * 0.5, base[1] + ny * w * 0.5), (mid[0] + nx * w, mid[1] + ny * w), tip, (mid[0] - nx * w, mid[1] - ny * w), (base[0] - nx * w * 0.5, base[1] - ny * w * 0.5)])
        lz.relleno(pts, col if abs(a) % 32 == 0 else (32, 70, 90), capa=capa)
        lz.relleno(np.array([pts[0], pts[1], tip, mid]), rim, alfa=0.35, capa=capa)


def dibujar(var):
    import mini_hidalgo as MH
    lz = Lienzo()
    lz.nuevo(T0, wob=0.0)
    bg = fondo()
    montes(lz)
    for i, (fx, fs) in enumerate(((60, 40), (440, 34), (1060, 44))):
        llama(lz, fx, 846 + (i % 2) * 8, fs, T0, seed=i, capa=0)
    pueblo(lz)
    U.haces_luz(lz, 640, 690, T0, n=9, largo=1500, color=(255, 170, 70), alfa=0.10, ancho=0.05, rot0=0.1, vel=0.0)
    # campanario con la campana (sus pilares apoyan en el suelo)
    viga_campanario(lz, 640, 560, 360, 330)
    campana(lz, 640, 715, 135, T0, ang=0.10)
    for r_, a_ in ((205, 0.85), (265, 0.6), (325, 0.35)):
        for lado in (-1, 1):
            c0 = 0.0 if lado > 0 else math.pi
            th = np.linspace(c0 - 0.60, c0 + 0.60, 24)
            lz.trazo(np.stack([640 + r_ * np.cos(th), 725 + r_ * 0.9 * np.sin(th)], 1), (255, 236, 170, int(255 * a_)), 11 - (r_ - 205) / 40, temblor=0.0, afinar=False, capa=2)
    # Hidalgo, dibujado a medida, con el puño en alto sosteniendo el estandarte
    # luz de la campana sobre el suelo y magueyes de primer plano (separados, sin tapar nada)
    agave(lz, 140, 1100, 300)
    agave(lz, 470, 1110, 190)
    MH.hidalgo(lz, 1225, 640, 170, T0)
    U.chispas(lz, 0.4, n=16, area=(40, 440, 1000, 700), seed=3, color=(255, 214, 120), tam=(6, 15))
    texto_titulo(lz, "11 AÑOS", "DE GUERRA", y1=175, y2=352, px1=195, px2=150)
    return lz, bg


def main():
    lz, bg = dibujar(VAR)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    img = E.acabado(img, 3)
    bgr = cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"previews/mini_{VAR}.png", bgr)
    pq = cv2.resize(bgr, (1280, 720), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"salida/independencia_mexico_mini_{VAR}.jpg", pq, [cv2.IMWRITE_JPEG_QUALITY, 92])
    cel = cv2.resize(pq, (170, 96), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"previews/mini_{VAR}_cel.png", cv2.resize(cel, (680, 384), interpolation=cv2.INTER_NEAREST))
    print("ok")


main()
