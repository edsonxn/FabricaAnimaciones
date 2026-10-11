# -*- coding: utf-8 -*-
"""Miniaturas oficiales de Cronopapel para «La historia de Roma en 5 minutos».
Generadas como cuadros nativos del motor (Boceto + Guache + Mapa de relieve).
"""
import math
import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import boceto as B
import mapa as M
import obj_roma as RO
import obj_c as C
from core import estampar
from motor import H, W

M.cargar()

T = 0.37
WOB = 0.0

ROJO_ROMA = (196, 48, 48)
ORO_ROMA = (236, 184, 52)
HIERRO = (120, 126, 136)
BRONCE = (195, 145, 75)


def centurion_romano(cara="asombro", brazos=(40, 115)):
    """Centurión romano con armadura segmentada, casco con cresta roja, scutum rojo y gladius."""
    ops = []
    cy = -215.0
    
    # 1. Personaje base con armadura
    p = RO.persona(ropa=ROJO_ROMA, traje="armadura", faja=ORO_ROMA, cara=cara,
                   brazos=brazos, mirada=0)
    ops += p.ops
    
    # 2. Casco romano de bronce (galea) con carrilleras
    ops += RO.forma(RO.rect(-36, cy - 20, -26, cy + 15, 3), BRONCE, 3.8, sp=4)
    ops += RO.forma(RO.rect(26, cy - 20, 36, cy + 15, 3), BRONCE, 3.8, sp=4)
    ops += RO.forma([(-38, cy - 10), (-34, cy - 50), (0, cy - 65), (34, cy - 50), (38, cy - 10), (22, cy - 18), (-22, cy - 18)], BRONCE, 4.6, sp=7)
    
    # 3. Cresta roja de centurión (crista transversa)
    ops += RO.forma(RO.pol((-28, cy - 62), (0, cy - 104), (28, cy - 62), (0, cy - 72)), ROJO_ROMA, 5.2, peso=0.9, sp=7)
    for dx in (-18, -9, 0, 9, 18):
        ops.append(RO.T(RO.linea((dx * 0.6, cy - 94), (dx, cy - 68)), 3.2, peso=0.03))
        
    # 4. Escudo Scutum curvo rojo al costado izquierdo
    cx, sy = -65, -110
    # Cuerpo rojo del escudo
    ops += RO.forma(RO.rect(cx - 36, sy - 85, cx + 36, sy + 85, 10), ROJO_ROMA, 5.5, peso=0.9, sp=9)
    # Filete interior y borde dorado (solo trazo y umbo)
    ops.append(RO.T(RO.rect(cx - 32, sy - 80, cx + 32, sy + 80, 8), 3.2, peso=0.03))
    # Umbo metálico en el centro
    ops += [RO.R(RO.circ(cx, sy, 15), ORO_ROMA, peso=0.05, sp=4),
            RO.R(RO.circ(cx, sy, 7), HIERRO, peso=0.03, sp=3)]
    # Motivo de alas de águila y rayos dorados
    ops += [RO.T(RO.linea((cx - 26, sy - 35), (cx - 10, sy)), 3.8, peso=0.04),
            RO.T(RO.linea((cx + 26, sy - 35), (cx + 10, sy)), 3.8, peso=0.04),
            RO.T(RO.linea((cx - 26, sy + 35), (cx - 10, sy)), 3.8, peso=0.04),
            RO.T(RO.linea((cx + 26, sy + 35), (cx + 10, sy)), 3.8, peso=0.04)]
            
    # 5. Espada Gladius inclinada hacia la derecha (no invade el cronómetro)
    # Brazo derecho extendido hacia la derecha
    gx, gy = 86, -225
    ang = math.radians(40) # inclinada hacia afuera a la derecha
    dx, dy = math.sin(ang), -math.cos(ang)
    nx, ny = -dy, dx
    L = 90
    
    p1 = (gx + nx * 5, gy + ny * 5)
    p2 = (gx - nx * 5, gy - ny * 5)
    p3 = (gx + dx * L - nx * 5, gy + dy * L - ny * 5)
    p4 = (gx + dx * (L + 18), gy + dy * (L + 18))
    p5 = (gx + dx * L + nx * 5, gy + dy * L + ny * 5)
    
    # Hoja plateada
    ops += RO.forma([p1, p2, p3, p4, p5], (215, 220, 230), 4.2, peso=0.85, sp=5)
    # Guarda de bronce
    ops += RO.forma([
        (gx - nx * 14 - dx * 4, gy - ny * 14 - dy * 4),
        (gx + nx * 14 - dx * 4, gy + ny * 14 - dy * 4),
        (gx + nx * 14 + dx * 6, gy + ny * 14 + dy * 6),
        (gx - nx * 14 + dx * 6, gy - ny * 14 + dy * 6)
    ], BRONCE, 4.0, sp=4)
    # Empuñadura
    ops += RO.forma([
        (gx - nx * 4 - dx * 28, gy - ny * 4 - dy * 28),
        (gx + nx * 4 - dx * 28, gy + ny * 4 - dy * 28),
        (gx + nx * 4 - dx * 4, gy + ny * 4 - dy * 4),
        (gx - nx * 4 - dx * 4, gy - ny * 4 - dy * 4)
    ], (110, 75, 50), 3.8, sp=3)
    # Pomo de bronce
    ops += [RO.R(RO.circ(gx - dx * 34, gy - dy * 34, 8), BRONCE, peso=0.03, sp=3)]
    
    return RO.Dib(ops)


def render_texto_pegatina(linea1, linea2=None, px1=200, px2=150,
                          col1=(255, 255, 255), col2=(255, 226, 30),
                          rot=-3.0, sw1=11, sw2=9):
    f1 = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", px1)
    f2 = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", px2) if linea2 else None
    
    bb1 = f1.getbbox(linea1)
    w1, h1 = bb1[2] - bb1[0], bb1[3] - bb1[1]
    
    if linea2:
        bb2 = f2.getbbox(linea2)
        w2, h2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
    else:
        w2, h2 = 0, 0
        
    pad = int(max(px1, px2 or 0) * 0.3)
    max_w = max(w1, w2)
    tot_w = max_w + pad * 2
    inter = int(px1 * 0.12) if linea2 else 0
    tot_h = h1 + (h2 + inter if linea2 else 0) + pad * 2
    
    im_mask = Image.new("L", (tot_w, tot_h), 0)
    d_mask = ImageDraw.Draw(im_mask)
    x1 = pad + (max_w - w1) // 2 - bb1[0]
    y1 = pad - bb1[1]
    d_mask.text((x1, y1), linea1, font=f1, fill=255, stroke_width=sw1 + 10, stroke_fill=255)
    
    if linea2:
        x2 = pad + (max_w - w2) // 2 - bb2[0]
        y2 = y1 + h1 + inter
        d_mask.text((x2, y2), linea2, font=f2, fill=255, stroke_width=sw2 + 10, stroke_fill=255)
        
    im_rgb = Image.new("RGBA", (tot_w, tot_h), (0, 0, 0, 0))
    d_rgb = ImageDraw.Draw(im_rgb)
    d_rgb.text((x1, y1), linea1, font=f1, fill=(28, 26, 30, 255), stroke_width=sw1 + 6, stroke_fill=(28, 26, 30, 255))
    d_rgb.text((x1, y1), linea1, font=f1, fill=col1 + (255,), stroke_width=sw1, stroke_fill=(28, 26, 30, 255))
    
    if linea2:
        d_rgb.text((x2, y2), linea2, font=f2, fill=(28, 26, 30, 255), stroke_width=sw2 + 6, stroke_fill=(28, 26, 30, 255))
        d_rgb.text((x2, y2), linea2, font=f2, fill=col2 + (255,), stroke_width=sw2, stroke_fill=(28, 26, 30, 255))
        
    if rot != 0:
        im_mask = im_mask.rotate(-rot, resample=Image.BICUBIC, expand=True)
        im_rgb = im_rgb.rotate(-rot, resample=Image.BICUBIC, expand=True)
        
    arr_mask = np.asarray(im_mask)
    arr_rgb = np.asarray(im_rgb)
    
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
    peg_mask = cv2.dilate((arr_mask > 20).astype(np.uint8) * 255, k)
    return arr_rgb, peg_mask


def estampar_texto_miniatura(h, arr_rgb, peg_mask, cx, cy):
    th, tw = peg_mask.shape
    xx = int(round(cx - tw / 2))
    yy = int(round(cy - th / 2))
    h.peg_mascara(peg_mask, xx, yy)
    xa, ya = max(0, xx), max(0, yy)
    xb, yb = min(W, xx + tw), min(H, yy + th)
    if xb > xa and yb > ya:
        sub_rgb = arr_rgb[ya - yy:yb - yy, xa - xx:xb - xx]
        alpha = sub_rgb[..., 3].astype(np.float32) / 255.0
        if not hasattr(h, "_textos_overlay"):
            h._textos_overlay = []
        h._textos_overlay.append((xa, ya, xb, yb, sub_rgb[..., :3], alpha))


def componer_miniatura(h):
    base = np.clip(h.componer(), 0, 1)
    if hasattr(h, "_textos_overlay"):
        for xa, ya, xb, yb, rgb, alpha in h._textos_overlay:
            col_f = rgb.astype(np.float32) / 255.0
            a = alpha[..., None]
            base[ya:yb, xa:xb] = base[ya:yb, xa:xb] * (1.0 - a) + col_f * a
    return base


def milenario(lz=None):
    """Variante 1: 1.000 AÑOS / EN 5 MINUTOS.
    Cuenca del Mediterráneo con el Imperio Romano pintado en carmesí, Coliseo, Estandarte SPQR,
    cronómetro y Centurión con scutum y espada."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(14.0, 39.5, 1.30, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    # Imperio Romano en rojo carmesí imperial
    S_campo = M.CAMPOS["imperio"]
    S = cam.proyectar(S_campo)
    M.pintar(img, S, (185, 45, 45), 1.0, 0, sombra=0.18)
    h.fondo = img
    
    # Coliseo romano en el centro
    col = RO.coliseo()
    col.dibujar(h, 1100, 380, s=0.95, rot=0.0, peg=True, fase_=0)
    
    # Estandarte imperial SPQR con águila dorada
    spqr = RO.estandarte_spqr()
    spqr.dibujar(h, 1370, 270, s=1.02, rot=-0.04, peg=True, fase_=0)
    
    # Cronómetro 5 min
    crono = C.cronometro(aguja=math.radians(115))
    crono.dibujar(h, 1750, 230, s=1.28, rot=0.06, peg=True, fase_=0)
    
    # Centurión romano
    cent = centurion_romano(cara="asombro", brazos=(40, 115))
    cent.dibujar(h, 1510, 970, s=2.45, rot=0.02, peg=True, fase_=0)
    
    # Texto
    arr, peg = render_texto_pegatina("1.000 AÑOS", "EN 5 MINUTOS", px1=195, px2=150,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 570, 280)
    return componer_miniatura(h)


def imperio(lz=None):
    """Variante 2: EL IMPERIO / EN 5 MINUTOS."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(14.0, 39.5, 1.30, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    S_campo = M.CAMPOS["imperio"]
    S = cam.proyectar(S_campo)
    M.pintar(img, S, (185, 45, 45), 1.0, 0, sombra=0.18)
    h.fondo = img
    
    col = RO.coliseo()
    col.dibujar(h, 1100, 380, s=0.95, rot=0.0, peg=True, fase_=0)
    
    spqr = RO.estandarte_spqr()
    spqr.dibujar(h, 1370, 270, s=1.02, rot=-0.04, peg=True, fase_=0)
    
    crono = C.cronometro(aguja=math.radians(115))
    crono.dibujar(h, 1750, 230, s=1.28, rot=0.06, peg=True, fase_=0)
    
    cent = centurion_romano(cara="asombro", brazos=(40, 115))
    cent.dibujar(h, 1510, 970, s=2.45, rot=0.02, peg=True, fase_=0)
    
    arr, peg = render_texto_pegatina("EL IMPERIO", "EN 5 MINUTOS", px1=195, px2=150,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 570, 280)
    return componer_miniatura(h)


def como_cayo(lz=None):
    """Variante 3: ¿CÓMO CAYÓ? / EN 5 MINUTOS."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(14.0, 39.5, 1.30, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    S_campo = M.CAMPOS["imperio"]
    S = cam.proyectar(S_campo)
    M.pintar(img, S, (185, 45, 45), 1.0, 0, sombra=0.18)
    h.fondo = img
    
    col = RO.coliseo()
    col.dibujar(h, 1100, 380, s=0.95, rot=0.0, peg=True, fase_=0)
    
    spqr = RO.estandarte_spqr()
    spqr.dibujar(h, 1370, 270, s=1.02, rot=-0.04, peg=True, fase_=0)
    
    crono = C.cronometro(aguja=math.radians(115))
    crono.dibujar(h, 1750, 230, s=1.28, rot=0.06, peg=True, fase_=0)
    
    cent = centurion_romano(cara="asombro", brazos=(110, 115))
    cent.dibujar(h, 1510, 970, s=2.45, rot=-0.02, peg=True, fase_=0)
    
    arr, peg = render_texto_pegatina("¿CÓMO CAYÓ?", "EN 5 MINUTOS", px1=195, px2=150,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 570, 280)
    return componer_miniatura(h)


VARIANTES = {
    "milenario": milenario,
    "imperio": imperio,
    "como_cayo": como_cayo,
}
