# -*- coding: utf-8 -*-
"""Kit «terror CRT» (horizontal 1920x1080): cuarto a oscuras cuya única luz es una tele CRT dibujada en 2D.

Ideas del estilo:
  - El juego (video real de yt-dlp o pantallas dibujadas) NUNCA va suelto: vive dentro de la tele. La pantalla se pinta en un búfer
    aparte (`P(SW, SH)`), pasa por `crt()` (curvatura, scanlines, tracking de VHS, aberración, ruido) y se pega en el cuarto.
  - El cuarto se dibuja «sin luz» (albedo) y `iluminar()` lo multiplica por la luz de la tele (su color y su brillo medio salen de
    la propia pantalla: lo que se ve en el juego tiñe el cuarto). Las siluetas se dibujan después, casi negras con luz de borde.
  - Cámara = zoom con `p.cam`: del cuarto entero a «dentro de la pantalla» y de vuelta, sin cortes.
"""
import functools
import math

import cv2
import numpy as np

from pix import (BLANCO, NEGRO, FUENTES, W, H, Clip, P, ancho_texto, clamp, e_out, golpe, lerp, mix, pop, pr, rnd, smooth, _rejilla)

FUENTES.update(pixel="Retro Gaming.ttf", serif="Baskervville-Bold.ttf", mano="RetjehDemo-Rough.ttf", mono_b="consolab.ttf")

# ------------------------------------------------------------------ paleta
HUESO = (0.90, 0.87, 0.78)
SANGRE = (0.82, 0.05, 0.06)
SANGRE2 = (0.40, 0.02, 0.03)
FRIO = (0.28, 0.58, 0.66)          # luz de tele, verde-azulada enferma
CRT_VERDE = (0.50, 1.00, 0.66)
SIL = (0.010, 0.011, 0.016)        # silueta casi negra

# ------------------------------------------------------------------ geometría
SW, SH = 1216, 912                 # búfer de pantalla (4:3)
SX0, SY0, SX1, SY1 = 1040.0, 300.0, 1580.0, 705.0      # pantalla en el mundo
SC = ((SX0 + SX1) / 2, (SY0 + SY1) / 2)
SUELO = 765.0


# ================================================================== CRT
@functools.lru_cache(maxsize=4)
def _mapas(w, h, k=0.10):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = (xs / w - 0.5) * 2, (ys / h - 0.5) * 2
    f = 1 + k * (u * u + v * v)
    return (u * f / 2 + 0.5) * w, (v * f / 2 + 0.5) * h, (1 - 0.55 * np.clip(u * u + v * v - 0.25, 0, 1) ** 1.2)[..., None].astype(np.float32)


@functools.lru_cache(maxsize=4)
def _scan(h):
    y = np.arange(h, dtype=np.float32)
    return (1 - 0.30 * (0.5 + 0.5 * np.cos(y * math.pi / 2.0)))[:, None, None].astype(np.float32)


def ruido_tv(w, h, t, nivel=1.0):
    rng = np.random.default_rng(int(t * 30) * 13 + 5)
    n = cv2.resize(rng.random((h // 3, w // 3)).astype(np.float32), (w, h), interpolation=cv2.INTER_NEAREST)
    fil = cv2.resize(0.55 + 0.45 * rng.random((h // 5, 1)).astype(np.float32), (1, h), interpolation=cv2.INTER_NEAREST)
    g = (n * fil) ** 1.4 * nivel
    return np.repeat(g[..., None], 3, axis=2)


def crt(img, t, glitch=0.0, tono=(1.0, 1.0, 1.0), ruido=0.045, freeze=None):
    """Efecto de tubo: curvatura, tracking de VHS (bandas corridas), aberración, scanlines, bloom, grano y viñeta."""
    h, w = img.shape[:2]
    mx, my, vin = _mapas(w, h)
    y = np.arange(h, dtype=np.float32)
    dx = 1.6 * np.sin(y * 0.045 + t * 2.3) + 0.8 * np.sin(y * 0.19 - t * 5.0)
    if glitch > 0.02:
        rng = np.random.default_rng(int(t * 24) * 7 + 3)
        for _ in range(int(2 + 9 * glitch)):
            y0 = int(rng.integers(0, h - 30))
            hh = int(rng.integers(6, 120))
            dx[y0:y0 + hh] += rng.choice([-1, 1]) * (30 + 220 * glitch) * rng.random()
        # barra de tracking que sube
        yb = int((1 - (t * 0.9) % 1.0) * h)
        dx[max(0, yb - 40):yb + 40] += 60 * glitch * np.sin(np.arange(max(0, yb - 40), min(h, yb + 40)) * 0.4)
    out = cv2.remap(img, (mx + dx[:, None]).astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    ca = int(round(2 + 14 * glitch))
    out[..., 0] = np.roll(out[..., 0], ca, axis=1)
    out[..., 2] = np.roll(out[..., 2], -ca, axis=1)
    luz = np.clip(out - 0.55, 0, None)
    out = out + cv2.GaussianBlur(luz, (0, 0), 7) * 0.9
    out = out * _scan(h)
    yb = ((t * 70) % (h + 260)) - 130                                  # barra de brillo que baja despacio
    out = out * (1 + 0.10 * np.exp(-(((y - yb) / 70.0) ** 2)))[:, None, None].astype(np.float32)
    rng = np.random.default_rng(int(t * 30) + 11)
    g = cv2.resize(rng.standard_normal((h // 2, w // 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_LINEAR) * ruido
    out = out + g[..., None]
    out = out * vin * np.float32(tono)
    return np.clip(out, 0, 1.4)


def crt_superpuesto(base, ov, mask, t):
    """Pega encima de una pantalla YA procesada un rótulo/cuadro estable (sin bandas de glitch) con la misma curvatura y scanlines:
    sirve para texto que tiene que leerse aunque el video de abajo esté corrompido. `mask` 0..1 (SHxSW) = dónde tapa."""
    h, w = ov.shape[:2]
    mx, my, _ = _mapas(w, h)
    ov2 = cv2.remap(ov, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    m2 = cv2.remap(mask.astype(np.float32), mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)[..., None]
    ov2 = (ov2 + cv2.GaussianBlur(np.clip(ov2 - 0.5, 0, None), (0, 0), 6) * 0.8) * _scan(h)
    return base * (1 - m2) + ov2 * m2


def color_medio(img):
    c = cv2.resize(img, (6, 4), interpolation=cv2.INTER_AREA).reshape(-1, 3).mean(0)
    return c


# ================================================================== pantallas dibujadas (dentro del búfer SWxSH)
def corazon(q, x, y, r, color, op=1.0):
    q.circ(x - r * 0.5, y - r * 0.2, r * 0.58, color, op)
    q.circ(x + r * 0.5, y - r * 0.2, r * 0.58, color, op)
    q.poly([(x - r * 1.04, y - r * 0.05), (x + r * 1.04, y - r * 0.05), (x, y + r * 1.15)], color, op)


def _fondo_morado(q, t, a=(0.12, 0.06, 0.20), b=(0.03, 0.02, 0.08)):
    q.fondo(a, b)
    for i in range(-6, 16):
        x = i * 130 + (t * 26) % 130
        q.poly([(x, 0), (x + 60, 0), (x - 280 + 60, SH), (x - 280, SH)], (1, 1, 1), 0.035)


def pant_archivo(t, k_ben=0.0, rojo=0.0, parpadeo=0.0):
    """Pantalla de selección de archivo (UI original): el archivo 1 ya tiene dueño."""
    q = P(SW, SH)
    _fondo_morado(q, t)
    q.texto("ELIGE UN ARCHIVO", SW / 2, 110, 54, HUESO, "pixel", 0.95)
    for i, y in enumerate((250, 450, 650)):
        sel = i == 0
        col = HUESO if sel else (0.35, 0.33, 0.45)
        q.rrect(150, y, SW - 150, y + 150, 18, (0.05, 0.03, 0.10), 0.92, borde=col, w=6 if sel else 3)
        q.texto(f"ARCHIVO {i + 1}", 200, y + 40, 28, col, "pixel", 0.9, "lm")
        if sel and k_ben > 0.01:
            dx = int(6 * rojo * (1 if int(t * 20) % 2 else -1))
            q.texto("BEN", 330 + dx, y + 100, 78, SANGRE, "pixel", min(1, k_ben) * 0.9 * rojo, "lm")
            q.texto("BEN", 330, y + 100, 78, mix(HUESO, SANGRE, 0.4 * rojo), "pixel", min(1, k_ben), "lm")
            for j in range(3):
                corazon(q, 880 + j * 62, y + 100, 22, SANGRE if rojo > 0.3 else (0.9, 0.2, 0.25), min(1, k_ben))
        else:
            q.texto("- NUEVO -" if not sel else "", 330, y + 100, 38, col, "pixel", 0.6, "lm")
        if sel and (int(t * 2.5) % 2 == 0):
            q.poly([(106, y + 56), (106, y + 96), (136, y + 76)], HUESO, 0.9)
    if parpadeo > 0:
        q.im *= 1 - 0.4 * parpadeo
    return q


def pant_hud_dia(q, t, u, rojo):
    """Marcador del «tercer día»: llena la barra, salta y aparece el día 4. `u` 0..1 avance; `rojo` 0..1 tras el salto."""
    q.rrect(300, 60, SW - 300, 150, 16, (0, 0, 0), 0.62, borde=HUESO, w=3)
    dia = "DÍA 4" if rojo > 0.5 else "DÍA 3"
    col = SANGRE if rojo > 0.5 else HUESO
    q.texto(dia, SW / 2, 105, 46, col, "pixel", 1.0)
    for i in range(3):
        q.circ(380 + i * 52, 105, 15, HUESO, 0.9 if i < 2 or u > 0.98 else 0.9, w=0 if (i < 2 or u > 0.98) else 4)
    for i in range(3):
        q.circ(SW - 380 - i * 52, 105, 15, (0.4, 0.4, 0.5), 0.5, w=4)
    q.rrect(300, 168, SW - 300, 190, 8, (0, 0, 0), 0.55)
    q.rrect(304, 172, 304 + (SW - 608) * clamp(u), 186, 6, mix((0.95, 0.75, 0.2), SANGRE, clamp(u * 1.2)), 0.95)


def pant_agua(t, u_hunde=0.0, glitch=0.0):
    """Estanque de noche visto desde dentro: un niño que se hunde despacio. Todo dibujado."""
    q = P(SW, SH)
    q.fondo((0.08, 0.38, 0.45), (0.01, 0.08, 0.12))
    sup = 170.0
    pts = [(x, sup + 7 * math.sin(x * 0.016 + t * 1.4) + 4 * math.sin(x * 0.047 - t * 1.1)) for x in range(-20, SW + 40, 20)]
    q.poly([(-20, -20)] + pts + [(SW + 40, -20)], (0.02, 0.03, 0.07))                       # noche sobre el agua
    q.glow(SW * 0.72, 40, 300, (0.7, 0.8, 1.0), 0.7, 2.0)                                    # luna
    q.circ(SW * 0.72, 54, 36, (0.82, 0.88, 0.98), 0.85)
    q.polilinea(pts, 5, (0.55, 0.85, 0.95), 0.75)
    for k in range(4):                                                                        # haces de luz
        x = 200 + k * 270 + 40 * math.sin(t * 0.5 + k)
        q.poly([(x - 50, sup), (x + 50, sup), (x + 190, SH), (x - 120, SH)], (0.45, 0.9, 1.0), 0.10, aditivo=True)
    for i in range(36):                                                                       # burbujas
        x = (rnd(i, 1) * SW + 18 * math.sin(t * 0.8 + i)) % SW
        y = (rnd(i, 2) * SH - t * (30 + 50 * rnd(i, 3))) % SH
        if y > sup + 8:
            q.circ(x, y, 3 + 7 * rnd(i, 4), (0.6, 0.9, 1.0), 0.35, w=2)
    cx = SW / 2 + 90 * math.sin(t * 0.35)
    cy = lerp(sup + 120, SH - 190, e_out(u_hunde)) + 16 * math.sin(t * 0.9)
    sil, rim = (0.004, 0.012, 0.02), (0.60, 0.98, 1.0)
    for dx, col, op in ((5, rim, 0.55), (0, sil, 1.0)):
        x = cx + dx
        for s in (-1, 1):                                                                     # brazos y piernas a la deriva
            q.polilinea([(x + s * 40, cy + 40), (x + s * 120, cy - 10 + 18 * math.sin(t * 1.1 + s)), (x + s * 190, cy - 70 + 26 * math.sin(t * 0.9 + s))], 18, col, op)
            q.polilinea([(x + s * 22, cy + 150), (x + s * 50, cy + 250), (x + s * 38 + 14 * math.sin(t + s), cy + 330)], 22, col, op)
        q.elip(x, cy + 70, 56, 100, col, op)
        q.circ(x, cy - 52, 44, col, op)
        for h in range(9):                                                                    # pelo flotando hacia arriba
            a = -math.pi / 2 + (h - 4) * 0.28
            q.polilinea([(x + 30 * math.cos(a), cy - 52 + 30 * math.sin(a)),
                         (x + 70 * math.cos(a) + 12 * math.sin(t * 1.3 + h), cy - 52 + 70 * math.sin(a) - 12),
                         (x + 105 * math.cos(a) + 24 * math.sin(t * 1.0 + h * 2), cy - 52 + 110 * math.sin(a) - 30)], 6, col, op)
    q.im *= 0.95 + 0.10 * math.sin(t * 0.7)
    return q


def pant_foro(t, t0, n_lineas=14):
    """Página de texto de un tablero, en verde de terminal. El título y las fechas son legibles; el resto, barras de texto."""
    q = P(SW, SH)
    q.fondo((0.02, 0.05, 0.04), (0.01, 0.03, 0.025))
    q.rect(0, 0, SW, 74, (0.05, 0.16, 0.10), 0.9)
    q.texto("/x/ - PARANORMAL", 40, 38, 34, CRT_VERDE, "mono_b", 1.0, "lm")
    q.texto("7 SEP 2010  ...  15 SEP 2010", SW - 40, 38, 30, CRT_VERDE, "mono_b", 0.8, "rm")
    q.texto("BEN DROWNED: HAUNTED CARTRIDGE", 60, 140, 40, (0.95, 1.0, 0.95), "mono_b", pr(t, t0, t0 + 0.4), "lm")
    for i in range(n_lineas):
        ti = t0 + 0.3 + i * 0.16
        u = pr(t, ti, ti + 0.4)
        if u <= 0:
            continue
        y = 205 + i * 50
        ancho = 380 + 760 * rnd(i, 4)
        col = CRT_VERDE if i % 4 else (0.9, 0.2, 0.2)
        q.rect(60, y - 10, 60 + ancho * u, y + 10, col, 0.45 + 0.30 * rnd(i, 7))
        if i % 5 == 0:
            q.texto(">>" + str(1000 + i * 37), 60 + ancho + 24, y, 22, CRT_VERDE, "mono_b", 0.8 * u, "lm")
    return q


def pant_texto(t, txt, color=HUESO, px=120, fnt="pixel"):
    q = P(SW, SH)
    q.fondo((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    q.texto(txt, SW / 2, SH / 2, px, color, fnt, 1.0)
    return q


def pant_clip(nombre, seg, ini, fin, brillo=1.0):
    """Video real (yt-dlp) en bucle dentro de [ini, fin] segundos del archivo, a pantalla completa 4:3 (recorta los lados)."""
    q = P(SW, SH)
    d = max(0.1, fin - ini)
    q.imagen(Clip.cuadro(nombre, ini + (seg % d)), 0, 0, SW, SH, 1.0, 0.0, brillo)
    return q


# ================================================================== cuarto
def iluminar(p, centro, radio, color, k, amb=(0.050, 0.060, 0.080)):
    """Multiplica la imagen (albedo del cuarto) por la luz de la tele: ambiente + caída radial coloreada."""
    h, w = p.H // 4, p.W // 4
    gx, gy = _rejilla(w, h)
    d = np.sqrt((gx * 4 - centro[0]) ** 2 + (gy * 4 - centro[1]) ** 2) / max(radio, 1)
    f = np.clip(1 - d, 0, 1) ** 1.7
    luz = np.float32(amb) + f[..., None] * np.float32(color) * k
    luz = cv2.resize(luz, (p.W, p.H), interpolation=cv2.INTER_LINEAR)
    p.im *= luz


def cuarto_albedo(p, t):
    """Pared, piso, ventana con luna, repisa y póster (sin luz: lo ilumina `iluminar`)."""
    p.fondo((0.30, 0.32, 0.36), (0.28, 0.30, 0.34))
    for x in range(0, 1960, 70):                                    # papel tapiz rayado
        p.rect(x, 0, x + 34, SUELO - 20, (0.34, 0.36, 0.42), 0.55)
    p.rect(0, SUELO - 24, 1920, SUELO + 6, (0.42, 0.40, 0.38))                         # zócalo
    p.rect(0, SUELO + 6, 1920, 1080, (0.30, 0.22, 0.18), grad=((0.34, 0.25, 0.20), (0.18, 0.12, 0.10)))
    for i in range(-2, 14):                                          # tablones en perspectiva
        p.linea((i * 190, SUELO + 6), (i * 330 - 400, 1080), 3, (0.10, 0.07, 0.06), 0.7)
    p.elip(900, 930, 620, 130, (0.20, 0.16, 0.20), 0.9)                                # alfombra
    p.elip(900, 930, 560, 105, (0.13, 0.11, 0.17), 0.9)
    # repisa con cartuchos y un peluche (siluetas)
    p.rect(660, 395, 940, 412, (0.40, 0.30, 0.22))
    for i in range(7):
        h_ = 52 + 12 * rnd(i, 3)
        p.rect(674 + i * 34, 395 - h_, 674 + i * 34 + 26, 395, mix((0.4, 0.4, 0.45), (0.5, 0.2, 0.2), rnd(i, 5) * 0.5))
    p.elip(900, 366, 24, 30, (0.45, 0.40, 0.35))
    p.elip(900, 328, 18, 18, (0.45, 0.40, 0.35))
    p.rect(740, 160, 900, 300, (0.18, 0.20, 0.30))                                  # póster
    p.rect(748, 168, 892, 292, (0.10, 0.12, 0.20))
    p.poly([(748, 292), (800, 215), (840, 262), (870, 230), (892, 292)], (0.05, 0.06, 0.12))


def ventana(p, t, k=1.0):
    """Ventana de noche con luna (emisiva, se dibuja DESPUÉS de iluminar) y cortinas que respiran."""
    x0, y0, x1, y1 = 120, 130, 430, 540
    p.rect(x0 - 16, y0 - 16, x1 + 16, y1 + 16, (0.06, 0.05, 0.05))
    p.rect(x0, y0, x1, y1, (0.03, 0.05, 0.11), grad=((0.03, 0.05, 0.12), (0.06, 0.09, 0.16)))
    p.glow(330, 240, 150, (0.55, 0.7, 1.0), 0.55, 2.0)
    p.circ(330, 240, 24, (0.85, 0.9, 1.0), 0.9)
    p.rect((x0 + x1) / 2 - 5, y0, (x0 + x1) / 2 + 5, y1, (0.05, 0.04, 0.04))
    p.rect(x0, (y0 + y1) / 2 - 5, x1, (y0 + y1) / 2 + 5, (0.05, 0.04, 0.04))
    for s, xa in ((-1, x0 - 16), (1, x1 + 16)):                      # cortinas
        sw = 8 * math.sin(t * 0.6 + s)
        p.poly([(xa, y0 - 30), (xa + s * 95 + sw, y0 - 30), (xa + s * 70 + sw * 1.6, y1 + 90), (xa, y1 + 90)], (0.08, 0.05, 0.07), 0.96)
    p.poly([(x0 + 40, y1), (x1 - 20, y1), (x1 + 330, SUELO + 250), (x0 - 140, SUELO + 250)], (0.45, 0.58, 0.85), 0.045 * k, aditivo=True)   # luz en el piso


def tele(p, scr, t, apagada=False, led=True):
    """Cuerpo de la tele CRT, antena, mesa y pantalla (`scr` = float32 SHxSW ya con efecto CRT)."""
    p.poly([(1070, 800), (1550, 800), (1580, 960), (1040, 960)], (0.02, 0.015, 0.015), 0.5)        # sombra en el piso
    # antena de conejo
    p.elip(1310, 238, 70, 22, (0.07, 0.07, 0.07))
    for (x, y), tip in (((1270, 238), (1150, 72)), ((1350, 238), (1500, 96))):
        p.linea((x, y), tip, 7, (0.45, 0.46, 0.5))
        p.circ(tip[0], tip[1], 11, (0.55, 0.56, 0.6))
    # caja
    p.rrect(985, 232, 1635, 780, 44, (0.11, 0.10, 0.10), grad=((0.17, 0.155, 0.15), (0.07, 0.065, 0.065)), borde=(0.24, 0.22, 0.21), w=3)
    p.rrect(1012, 270, 1608, 735, 40, (0.025, 0.025, 0.025))
    p.imagen((np.clip(scr, 0, 1) * 255).astype(np.uint8), SX0, SY0, SX1, SY1, 1.0, 34.0)
    # reflejo en el vidrio
    p.poly([(SX0 + 20, SY0 + 10), (SX0 + 150, SY0 + 10), (SX0 + 30, SY0 + 190)], (1, 1, 1), 0.05)
    p.rrect(SX0, SY0, SX1, SY1, 34, None, borde=(0.0, 0.0, 0.0), w=5, op_b=0.6)
    # panel inferior
    for i, x in enumerate((1090, 1160)):
        p.circ(x, 757, 17, (0.05, 0.05, 0.05))
        p.circ(x, 757, 13, (0.20, 0.19, 0.18))
        p.linea((x, 757), (x + 7 * (1 if i else -1), 748), 3, (0.7, 0.68, 0.6))
    for i in range(6):
        p.rect(1290 + i * 24, 744, 1304 + i * 24, 770, (0.03, 0.03, 0.03))
    if led:
        on = 0.55 + 0.45 * (math.sin(t * 2.0) > -0.2)
        p.circ(1580, 757, 7, SANGRE, 0.9 * on if not apagada else 0.3)
        p.glow(1580, 757, 40, SANGRE, 0.35 * on)
    # mesa
    p.rect(1010, 780, 1610, 806, (0.20, 0.14, 0.10))
    p.rect(1030, 806, 1048, 940, (0.12, 0.08, 0.06))
    p.rect(1572, 806, 1590, 940, (0.12, 0.08, 0.06))


def consola(p, t, k_cart=0.0, cx=1180, y=915):
    """Consola gris de cartuchos (diseño genérico original) en el piso, con el cartucho entrando por arriba (k_cart 0..1)."""
    p.poly([(cx - 130, y + 35), (cx + 130, y + 35), (cx + 160, y + 70), (cx - 160, y + 70)], (0.02, 0.02, 0.02), 0.45)
    p.rrect(cx - 130, y - 20, cx + 130, y + 36, 8, (0.30, 0.30, 0.34), grad=((0.38, 0.38, 0.42), (0.22, 0.22, 0.26)))
    p.rect(cx - 70, y - 28, cx + 70, y - 14, (0.10, 0.10, 0.12))
    for i in range(4):
        p.rect(cx - 100 + i * 52, y + 10, cx - 70 + i * 52, y + 22, (0.06, 0.06, 0.07))
    if k_cart > 0:
        yc = lerp(y - 190, y - 70, smooth(k_cart))
        cartucho(p, cx, yc, 0.8)
    p.circ(cx + 90, y - 22, 6, SANGRE, 0.9)


def cartucho(p, x, y, s=1.0, ang=0.0):
    """Cartucho gris con etiqueta escrita a mano («Majora» como en el relato)."""
    with p.grupo(x, y, s):
        if ang:
            pass
        p.rrect(-90, -70, 90, 70, 10, (0.36, 0.36, 0.38), grad=((0.46, 0.46, 0.48), (0.26, 0.26, 0.28)), borde=(0.15, 0.15, 0.17), w=3)
        p.rect(-62, 42, 62, 70, (0.14, 0.14, 0.15))
        for i in range(9):
            p.rect(-54 + i * 12, 46, -48 + i * 12, 66, (0.62, 0.55, 0.25))
        p.rect(-62, -52, 62, 22, (0.82, 0.78, 0.66))
        p.rect(-62, -52, 62, -46, (0.65, 0.2, 0.2))
        p.texto("MAJORA", 0, -14, 30, (0.12, 0.10, 0.10), "mano", 0.95)
        p.linea((-52, 8), (40, 6), 2, (0.2, 0.2, 0.2), 0.5)


def cartel_garaje(p, x, y, t, s=1.0, ang=0.0):
    """Cartón escrito a mano que cuelga y se mece."""
    a = ang + 0.05 * math.sin(t * 1.7)
    ca, sa = math.cos(a), math.sin(a)

    def rot(px_, py_):
        return (x + px_ * ca - py_ * sa, y + px_ * sa + py_ * ca)
    pts = [rot(-190 * s, -75 * s), rot(190 * s, -75 * s), rot(190 * s, 75 * s), rot(-190 * s, 75 * s)]
    p.poly(pts, (0.60, 0.46, 0.30))
    p.polilinea(pts, 3, (0.30, 0.2, 0.12), 0.9, cerrado=True)
    p.polilinea([rot(-150 * s, -75 * s), rot(0, -160 * s), rot(150 * s, -75 * s)], 3, (0.8, 0.8, 0.8), 0.7)
    with p.grupo(*rot(0, -16 * s), 1.0):
        pass
    cx_, cy_ = rot(0, -14 * s)
    p.texto("VENTA", cx_, cy_ - 22 * s, 52 * s, (0.12, 0.08, 0.06), "mano", 1.0)
    p.texto("DE GARAJE", cx_, cy_ + 34 * s, 52 * s, (0.12, 0.08, 0.06), "mano", 1.0)


# ------------------------------------------------------------------ siluetas
def jugador(p, t, luz, giro=0.0, k=1.0):
    """Jugador sentado en el piso, de espaldas a la cámara (silueta a contraluz con luz de borde). giro 0..1 = gira la cabeza."""
    x0 = 610.0
    resp = 4 * math.sin(t * 1.5)
    hx = x0 + 4 - 40 * giro
    hy = 690 + resp * 0.5

    def forma(dx, col, op):
        x = x0 + dx
        p.elip(x, 1000, 215, 78, col, op)                                                                            # base: piernas cruzadas
        for s_ in (-1, 1):
            p.elip(x + s_ * 205, 990, 125, 58, col, op)
        p.elip(x, 905, 140, 130, col, op)                                                                            # torso (sudadera)
        p.elip(x, 818 + resp, 158, 70, col, op)                                                                      # hombros
        p.polilinea([(x + 140, 805), (x + 196, 888), (x + 300, 934)], 46, col, op)                                  # brazo hacia la tele
        p.polilinea([(x - 140, 805), (x - 192, 892), (x - 70, 962)], 46, col, op)
        p.elip(x + 3, 770 + resp * 0.5, 92, 40, col, op)                                                             # capucha caída
        p.rect(x - 30, hy + 40, x + 30, 780, col, op)                                                                # cuello
        p.circ(hx + dx, hy, 64, col, op)                                                                             # cabeza
        for s_ in (-1, 1):
            p.elip(hx + dx + s_ * 62, hy + 6, 11, 18, col, op)                                                       # orejas
        for i in range(9):                                                                                           # pelo desordenado
            a = math.pi + (i - 4) * 0.34
            p.poly([(hx + dx + 50 * math.cos(a), hy + 50 * math.sin(a)), (hx + dx + 86 * math.cos(a + 0.15) + 4 * math.sin(t + i), hy + 86 * math.sin(a + 0.15)),
                    (hx + dx + 50 * math.cos(a + 0.4), hy + 50 * math.sin(a + 0.4))], col, op)
        if giro > 0.35:                                                                                               # perfil: nariz hacia la estatua
            p.poly([(hx + dx - 58, hy - 4), (hx + dx - 90, hy + 16), (hx + dx - 56, hy + 26)], col, op)
    forma(7, mix(luz, (1, 1, 1), 0.1), 0.50 * k)
    forma(0, SIL, k)
    cx_, cy_ = x0 + 310, 944
    p.rrect(cx_ - 46, cy_ - 18, cx_ + 46, cy_ + 20, 14, SIL, k)                                                      # control
    p.rrect(cx_ - 46, cy_ - 18, cx_ + 46, cy_ + 20, 14, None, borde=mix(luz, (1, 1, 1), 0.1), w=2, op_b=0.45 * k)
    # cable del control a la consola
    p.polilinea([(cx_ + 46, cy_), (cx_ + 120, cy_ + 34), (cx_ + 190, cy_ + 12), (1080, 950)], 5, (0.03, 0.03, 0.04), k)


def estatua(p, t, luz, k=1.0, ojos=0.0, esc=1.0):
    """Estatua alta de una figura de capucha puntiaguda (diseño genérico original), de pie en el cuarto, a contraluz."""
    if k <= 0.01:
        return
    x0, yf = 330.0, 800.0
    inc = 0.015 * math.sin(t * 0.7)

    def forma(dx, col, op):
        x = x0 + dx
        for s_ in (-1, 1):                                                                                           # botas y piernas
            p.poly([(x + s_ * 18, 700), (x + s_ * 54, 700), (x + s_ * 52, 790), (x + s_ * 74, 800), (x + s_ * 74, 812), (x + s_ * 14, 812), (x + s_ * 14, 790)], col, op)
        p.poly([(x - 62, 700), (x + 62, 700), (x + 84, 612), (x + 70, 508), (x - 70, 508), (x - 84, 612)], col, op)   # túnica con vuelo
        p.rect(x - 72, 606, x + 72, 630, col, op)                                                                    # cinturón
        p.poly([(x - 108, 500), (x + 108, 500), (x + 72, 560), (x - 72, 560)], col, op)                              # hombros
        for s_ in (-1, 1):                                                                                           # brazos largos y caídos
            p.poly([(x + s_ * 98, 500), (x + s_ * 118, 520), (x + s_ * 116, 650), (x + s_ * 124, 708), (x + s_ * 98, 708), (x + s_ * 92, 640)], col, op)
            p.elip(x + s_ * 110, 722, 15, 22, col, op)                                                               # manos
        p.rect(x - 14, 470, x + 14, 510, col, op)                                                                    # cuello
        hx_, hy_ = x + 8 * inc * 40, 442
        p.elip(hx_, hy_, 40, 48, col, op)                                                                            # cabeza (ladeada)
        for s_ in (-1, 1):
            p.poly([(hx_ + s_ * 34, hy_ - 4), (hx_ + s_ * 104, hy_ - 30 - 8 * s_), (hx_ + s_ * 36, hy_ + 24)], col, op)   # orejas largas
        p.poly([(hx_ + 44, hy_ - 14), (hx_ + 34, hy_ - 52), (hx_ - 10, hy_ - 92), (hx_ - 84, hy_ - 108), (hx_ - 160, hy_ - 80),    # gorro largo que cae
                (hx_ - 214, hy_ - 14), (hx_ - 232, hy_ + 52), (hx_ - 188, hy_ + 2), (hx_ - 130, hy_ - 44), (hx_ - 68, hy_ - 58),
                (hx_ - 30, hy_ - 36), (hx_ - 44, hy_ - 8)], col, op)
    forma(7, mix(luz, (1, 1, 1), 0.1), 0.42 * k)
    forma(0, (0.012, 0.015, 0.020), k)
    if ojos > 0.01:
        for s_ in (-1, 1):
            p.glow(x0 + s_ * 17, 446, 40 * esc, (0.85, 0.95, 1.0), 0.95 * ojos * k, 2.0)
            p.elip(x0 + s_ * 17, 446, 7 * esc, 4.5 * esc, (0.97, 0.99, 1.0), ojos * k)


def polvo(p, t, centro, k=1.0, n=70):
    """Motas de polvo en el haz de la tele (más claras cerca de la luz)."""
    for i in range(n):
        x = (rnd(i, 1) * 1900 + 20 * math.sin(t * 0.3 + i)) % 1920
        y = (rnd(i, 2) * 1000 - t * (6 + 14 * rnd(i, 3))) % 1000 + 40
        d = math.hypot(x - centro[0], y - centro[1])
        a = clamp(1 - d / 900) ** 1.4 * (0.4 + 0.6 * rnd(i, 4)) * k
        p.circ(x, y, 1.6 + 2.6 * rnd(i, 5), (0.7, 0.85, 0.95), 0.55 * a, aditivo=True)


def luz_suelo(p, color, k):
    """Charco de luz de la tele sobre el piso."""
    p.poly([(1060, 806), (1560, 806), (1940, 1090), (700, 1090)], color, 0.10 * k, aditivo=True)
    p.elip(1310, 900, 420, 70, color, 0.14 * k, aditivo=True)


# ------------------------------------------------------------------ tarjetas que se «salen» de la tele (cierre)
def tarjeta(p, tipo, x, y, s, op, t, color=FRIO):
    if op <= 0.01:
        return
    with p.grupo(x, y, s):
        p.rrect(-150, -100, 150, 100, 12, (0.04, 0.05, 0.07), op, borde=color, w=3, op_b=op)
        p.rect(-150, -100, 150, -72, mix((0.05, 0.06, 0.08), color, 0.22), op)
        for i in range(3):
            p.circ(-130 + i * 20, -86, 5, mix(color, (1, 1, 1), 0.3), op)
        if tipo == "video":
            p.rect(-134, -60, 134, 50, (0.02, 0.03, 0.05), op)
            p.poly([(-20, -26), (-20, 26), (26, 0)], mix(color, (1, 1, 1), 0.5), op)
            p.rect(-134, 70, 134, 78, (0.15, 0.17, 0.2), op)
            p.rect(-134, 70, -30 + 40 * math.sin(t * 0.7), 78, SANGRE, op)
        elif tipo == "web":
            p.rrect(-134, -62, 134, -42, 8, (0.1, 0.12, 0.15), op)
            for i in range(6):
                p.rect(-134, -22 + i * 20, -134 + 80 + 190 * rnd(i, 9), -12 + i * 20, mix(color, (1, 1, 1), 0.2), 0.45 * op)
        else:
            for i, (xx, w_, c) in enumerate(((-100, 150, color), (100, 130, (0.5, 0.5, 0.55)), (-80, 170, color))):
                yy = -44 + i * 50
                p.rrect(xx - w_ / 2, yy - 18, xx + w_ / 2, yy + 18, 16, mix((0.05, 0.06, 0.08), c, 0.4), op)
            for j in range(3):
                p.circ(-30 + j * 18, 66, 5, color, op * (0.4 + 0.6 * (math.sin(t * 5 - j) > 0)))


def pared_pantallas(p, t, k0, k1):
    """Muchas pantallitas encendidas en la oscuridad: los lectores."""
    for j in range(5):
        for i in range(15):
            n = j * 15 + i
            x, y = 70 + i * 130, 90 + j * 150
            if 940 < x + 60 and x - 60 < 1700 and y + 40 > 190:
                continue
            u = pr(t, k0 + 1.3 * rnd(n, 2), k0 + 1.3 * rnd(n, 2) + 0.4) * pr(k1, 0, 1)
            if u <= 0:
                continue
            fl = 0.55 + 0.45 * math.sin(t * (2 + 6 * rnd(n, 3)) + n)
            c = mix((0.25, 0.6, 0.7), (0.5, 0.45, 0.8), rnd(n, 4))
            p.rect(x - 38, y - 28, x + 38, y + 28, c, 0.32 * u * fl)
            p.glow(x, y, 90, c, 0.5 * u * fl, 2.0)
