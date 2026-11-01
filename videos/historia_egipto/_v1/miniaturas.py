# -*- coding: utf-8 -*-
"""Miniaturas oficiales de Cronopapel para «La historia de Egipto en 5 minutos».
Generadas como cuadros nativos del motor (Boceto + Guache + Mapa de relieve).
"""
import math
import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import boceto as B
from boceto import Dib, R, circ, elip, linea
import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from core import estampar
from motor import H, W
from obj_base import forma, rayita, rect, personaje_egipcio, _rotar

M.cargar()

T = 0.37
WOB = 0.0

CREMA = (246, 236, 208)
GRIS_CL = (206, 208, 216)
ROJO_CH = (200, 66, 60)
ORO_EGIPTO = (226, 175, 52)


def cronometro(aguja=0.0):
    """Cronómetro sticker de Cronopapel."""
    ops = forma(circ(0, 0, 100, n=42), CREMA, 6.4, peso=0.8, sp=11) + forma(rect(-18, -128, 18, -100, 4), GRIS_CL, 5, sp=6) + [B.T(linea((58, -84), (84, -108)), 7, peso=0.03)]
    for i in range(12):
        a = i * math.pi / 6
        ops.append(rayita(84 * math.cos(a), 84 * math.sin(a), 94 * math.cos(a), 94 * math.sin(a), 4.2))
    ops += [B.T(_rotar(linea((0, 0), (0, -70)), aguja, 0, 0), 6, peso=0.02), R(circ(0, 0, 8, n=10), ROJO_CH, peso=0.01, sp=3)]
    return Dib(ops)


def render_texto_pegatina(linea1, linea2=None, px1=205, px2=155,
                          col1=(255, 255, 255), col2=(255, 226, 30),
                          rot=-3.0, sw1=12, sw2=10):
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
    """Variante 1: 5.000 AÑOS / EN 5 MINUTOS.
    Valle del Nilo verde con el mar, Gran Pirámide, Faraón con nemes y cetro, cartucho real y cronómetro."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(31.2, 28.2, 2.30, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    # Resaltar territorio histórico de Egipto en oro antiguo
    if "unificado" in M.CAMPOS:
        S_unif = cam.proyectar(M.CAMPOS["unificado"])
        M.pintar(img, S_unif, ORO_EGIPTO, alfa=0.92, fase=0, sombra=0.18)
        
    M.pintar_nilo(img, cam, fase=0)
    h.fondo = img
    
    # Gran Pirámide de Guiza en el horizonte
    pir = A.gran_piramide_guiza()
    pir.dibujar(h, 1060, 360, s=1.1, rot=0.0, peg=True, fase_=0)
    
    # Cartucho real / jeroglífico en la parte superior central
    cart = A.cartucho_real()
    cart.dibujar(h, 1370, 240, s=1.05, rot=-0.05, peg=True, fase_=0)
    
    # Cronómetro 5 min
    cr = cronometro(aguja=math.radians(115))
    cr.dibujar(h, 1750, 240, s=1.3, rot=0.06, peg=True, fase_=0)
    
    # Faraón divino en primer plano con expresión de asombro
    far = personaje_egipcio(tipo="faraon", corona="nemes", mirada=-1.0, cetro=True, cara="asombro")
    far.dibujar(h, 1530, 1020, s=2.80, rot=0.02, peg=True, fase_=0)
    
    # Texto
    arr, peg = render_texto_pegatina("5.000 AÑOS", "EN 5 MINUTOS", px1=205, px2=155,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 580, 285)
    return componer_miniatura(h)


def faraones(lz=None):
    """Variante 2: FARAONES / EN 5 MINUTOS."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(31.2, 28.2, 2.30, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    if "unificado" in M.CAMPOS:
        S_unif = cam.proyectar(M.CAMPOS["unificado"])
        M.pintar(img, S_unif, ORO_EGIPTO, alfa=0.92, fase=0, sombra=0.18)
        
    M.pintar_nilo(img, cam, fase=0)
    h.fondo = img
    
    pir = A.gran_piramide_guiza()
    pir.dibujar(h, 1060, 360, s=1.1, rot=0.0, peg=True, fase_=0)
    
    cart = A.cartucho_real()
    cart.dibujar(h, 1370, 240, s=1.05, rot=-0.05, peg=True, fase_=0)
    
    cr = cronometro(aguja=math.radians(115))
    cr.dibujar(h, 1750, 240, s=1.3, rot=0.06, peg=True, fase_=0)
    
    far = personaje_egipcio(tipo="faraon", corona="pschent", mirada=-1.0, cetro=True, cara="asombro")
    far.dibujar(h, 1530, 1020, s=2.80, rot=0.02, peg=True, fase_=0)
    
    arr, peg = render_texto_pegatina("FARAONES", "EN 5 MINUTOS", px1=205, px2=155,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 580, 285)
    return componer_miniatura(h)


VARIANTES = {
    "milenario": milenario,
    "faraones": faraones,
}
