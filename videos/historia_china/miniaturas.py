# -*- coding: utf-8 -*-
"""Miniaturas oficiales de Cronopapel para «La historia de China en 3 minutos».
Generadas como cuadros nativos del motor (Boceto + Guache + Mapa de relieve).
Técnicas de YouTube aplicadas:
  - Tipografía Impact ultragruesa con silueta de papel ceñida y bicromía de alto contraste (Blanco + Amarillo #FFE21E).
  - Personaje en primer plano en escala grande (escala 2.4) con expresión de shock/asombro.
  - Ganchos de alta curiosidad que complementan el título sin redundancia.
  - Composición que respeta la zona segura de duración de YouTube (esquina inferior derecha).

Uso:
  python fab.py historia_china miniatura
"""
import math
import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import boceto as B
import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from core import Fractura, estampar, pintar_celdas
from motor import H, W

M.cargar()

T = 0.37
WOB = 0.0


def render_texto_pegatina(linea1, linea2=None, px1=200, px2=150,
                          col1=(255, 255, 255), col2=(255, 226, 30),
                          rot=-3.0, sw1=11, sw2=9):
    """Genera texto de alto impacto con tipografía Impact, contorno negro de tinta y silueta ceñida de papel."""
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
    
    # Máscara para la pegatina
    im_mask = Image.new("L", (tot_w, tot_h), 0)
    d_mask = ImageDraw.Draw(im_mask)
    x1 = pad + (max_w - w1) // 2 - bb1[0]
    y1 = pad - bb1[1]
    d_mask.text((x1, y1), linea1, font=f1, fill=255, stroke_width=sw1 + 10, stroke_fill=255)
    
    if linea2:
        x2 = pad + (max_w - w2) // 2 - bb2[0]
        y2 = y1 + h1 + inter
        d_mask.text((x2, y2), linea2, font=f2, fill=255, stroke_width=sw2 + 10, stroke_fill=255)
        
    # Letras con contorno negro
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
    """Estampa la pegatina sobre la hoja con recorte de papel y sombra."""
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
    """Compone la imagen final de boceto con el texto nítido."""
    base = np.clip(h.componer(), 0, 1)
    if hasattr(h, "_textos_overlay"):
        for xa, ya, xb, yb, rgb, alpha in h._textos_overlay:
            col_f = rgb.astype(np.float32) / 255.0
            a = alpha[..., None]
            base[ya:yb, xa:xb] = base[ya:yb, xa:xb] * (1.0 - a) + col_f * a
    return base


def sobrevivio(lz=None):
    """Variante 1: Gancho de curiosidad extrema (¿CÓMO SOBREVIVIÓ?).
    Mapa fracturado en caudillos/reinos, emperador gigante con manos levantadas en shock."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(104.5, 35.5, 1.22, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    fr = Fractura("caudillos", 0.0, 1.0, 10.0, 11.0, gap=15, deriva=50, nervio=1.5)
    S_campo = M.CAMPOS["prc"]
    pintar_celdas(img, cam, S_campo, fr, t=0.5, g=1.0, fase=0)
    h.fondo = img
    
    # Sello dinástico Han (漢)
    estampar(h, "漢", 1370, 240, px=200, rot=-0.06, color=(196, 52, 52), desgaste=0.08, semilla=2, peg=True)
    
    # Cronómetro 3 min
    crono = C.cronometro(aguja=math.radians(115))
    crono.dibujar(h, 1750, 240, s=1.3, rot=0.06, peg=True, fase_=0)
    
    # Emperador chino gigante con ambas manos levantadas en pánico
    emp = Bb.persona(
        ropa=Bb.ORO,
        piel=Bb.PIEL,
        sombrero_="mianguan",
        cara="asombro",
        brazos=(115, 120),
        pose=0,
        traje="tunica",
        faja=Bb.ROJO_CH,
        cuello=Bb.ROJO_CH,
        bigote=True,
        barba=Bb.NEGRO
    )
    emp.dibujar(h, 1510, 960, s=2.40, rot=-0.02, peg=True, fase_=0)
    
    # Texto de gancho: ¿CÓMO (blanco) / SOBREVIVIÓ? (amarillo #FFE21E)
    arr, peg = render_texto_pegatina("¿CÓMO", "SOBREVIVIÓ?", px1=195, px2=175,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 550, 280)
    
    return componer_miniatura(h)


def rompio(lz=None):
    """Variante 2: Gancho directo al núcleo del video (¿SE ROMPIÓ? / 5.000 AÑOS).
    Mapa de China agrietándose, emperador asombrado señalando."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(104.5, 35.5, 1.22, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    fr = Fractura("caudillos", 0.0, 1.0, 10.0, 11.0, gap=15, deriva=50, nervio=1.5)
    S_campo = M.CAMPOS["prc"]
    pintar_celdas(img, cam, S_campo, fr, t=0.5, g=1.0, fase=0)
    h.fondo = img
    
    # Sello Qin (秦)
    estampar(h, "秦", 1370, 240, px=200, rot=-0.06, color=(196, 52, 52), desgaste=0.08, semilla=5, peg=True)
    
    # Cronómetro
    crono = C.cronometro(aguja=math.radians(115))
    crono.dibujar(h, 1750, 240, s=1.3, rot=0.06, peg=True, fase_=0)
    
    # Emperador gigante
    emp = Bb.persona(
        ropa=Bb.ORO,
        piel=Bb.PIEL,
        sombrero_="mianguan",
        cara="asombro",
        brazos=(35, 120),
        pose=0,
        traje="tunica",
        faja=Bb.ROJO_CH,
        cuello=Bb.ROJO_CH,
        bigote=True,
        barba=Bb.NEGRO
    )
    emp.dibujar(h, 1510, 960, s=2.40, rot=0.02, peg=True, fase_=0)
    
    # Texto
    arr, peg = render_texto_pegatina("¿SE ROMPIÓ?", "5.000 AÑOS", px1=185, px2=170,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 550, 280)
    
    return componer_miniatura(h)


def milenario(lz=None):
    """Variante 3: Valor y promesa épica (5.000 AÑOS / EN 3 MINUTOS).
    Mapa unificado de China en rojo terracota, torre de la muralla y emperador señalando."""
    h = B.Hoja()
    h.limpiar()
    
    cam = M.Cam()
    cam.fijar(104.5, 35.5, 1.22, 0.0)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, fase=0)
    
    # Territorio unificado
    S_campo = M.CAMPOS["prc"]
    S = cam.proyectar(S_campo)
    M.pintar(img, S, M.COL["prc"], 1.0, 0, sombra=0.18)
    h.fondo = img
    
    # Torre de la Gran Muralla (ubicada al norte sin tapar el texto)
    muralla = A.torre_muralla(s=1.2)
    mx, my = cam.pant(111.0, 41.5)
    muralla.dibujar(h, mx, my - 25, s=1.10, rot=-0.04, peg=True, fase_=0)
    
    # Sello Qin
    estampar(h, "秦", 1370, 240, px=200, rot=-0.06, color=(196, 52, 52), desgaste=0.08, semilla=5, peg=True)
    
    # Cronómetro
    crono = C.cronometro(aguja=math.radians(115))
    crono.dibujar(h, 1750, 240, s=1.3, rot=0.06, peg=True, fase_=0)
    
    # Emperador gigante
    emp = Bb.persona(
        ropa=Bb.ORO,
        piel=Bb.PIEL,
        sombrero_="mianguan",
        cara="asombro",
        brazos=(35, 120),
        pose=0,
        traje="tunica",
        faja=Bb.ROJO_CH,
        cuello=Bb.ROJO_CH,
        bigote=True,
        barba=Bb.NEGRO
    )
    emp.dibujar(h, 1510, 960, s=2.40, rot=0.02, peg=True, fase_=0)
    
    # Texto
    arr, peg = render_texto_pegatina("5.000 AÑOS", "EN 3 MINUTOS", px1=195, px2=150,
                                    col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0)
    estampar_texto_miniatura(h, arr, peg, 550, 280)
    
    return componer_miniatura(h)


VARIANTES = {
    "sobrevivio": sobrevivio,
    "rompio": rompio,
    "milenario": milenario,
}
