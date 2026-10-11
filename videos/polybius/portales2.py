# -*- coding: utf-8 -*-
"""Portales, parte B: gobierno (tanque, prueba de campo), pruebas (hemeroteca), origen (web del año 2000, viaje), por qué (padres,
mente, recreación de 2007) y cierre (búsqueda a oscuras)."""
import functools
import json
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

from portal_base import *  # noqa: F401,F403


# ================================================================================================ GOBIERNO
@portal("tanque")
def tanque(p, t):
    """El mismo campo de batalla de alambre: primero en una cabina de salón, luego en un puesto de entrenamiento con un soldado."""
    g = "gobierno"
    t0, t2 = INI(g, 1), ww(g, 1, "simulador") - 0.5
    u = smooth((t - t2) / 1.0)
    p.fondo((0.010, 0.022, 0.014), (0.020, 0.040, 0.030))
    # pantalla grande que se encoge hacia la izquierda cuando aparece el puesto militar
    x0, y0, x1, y1 = lerp(180, 90, u), lerp(70, 170, u), lerp(1740, 980, u), lerp(950, 830, u)
    p.rrect(x0 - 36, y0 - 36, x1 + 36, y1 + 36, 30, (0.03, 0.035, 0.04))
    pant_tanque(p, x0, y0, x1, y1, t, 1.0)
    p.glow((x0 + x1) / 2, (y0 + y1) / 2, 900, VERDE, 0.10)
    if u < 0.5:
        p.texto("JUEGO DE SALÓN", (x0 + x1) / 2, y1 + 78, 46, (0.75, 0.95, 0.8), "mono", 1 - u * 2)
    if u > 0:
        # puesto de entrenamiento: consola con visor y soldado sentado (casco)
        p.rect(1010, 0, W, H, (0.07, 0.11, 0.08), u, grad=((0.05, 0.08, 0.06), (0.11, 0.16, 0.12)))
        p.glow(1500, 560, 700, (0.3, 0.6, 0.35), 0.18 * u)
        p.rect(1010, 860, 1920, 1080, (0.035, 0.05, 0.04), u)
        p.rrect(1100, 420, 1460, 700, 20, (0.05, 0.07, 0.055), u)
        pant_tanque(p, 1120, 440, 1440, 680, t + 3, u, mira=True)
        p.poly([(1060, 700), (1500, 700), (1560, 860), (1010, 860)], (0.06, 0.08, 0.065), u)
        for k in range(6):
            p.circ(1120 + k * 68, 780 + (k % 2) * 30, 12, (1.0, 0.3, 0.2) if math.sin(t * 4 + k) > 0.3 else (0.3, 0.9, 0.4), u)
        j = persona(p, 1640, 1010, 640, dict(ll=(-1.35, -1.35), lr=(-1.30, -1.30), bl=(-0.9, -0.7 - 0.1 * math.sin(t * 5)), br=(-0.8, -0.9), lean=-0.15, head=-0.2),
                    FIG, 1, alpha=u)
        hx, hy = 1640 + j["hd"][0], 1010 - j["hd"][1]
        p.elip(hx, hy - 14, 62, 50, 0, (0.10, 0.14, 0.09), u, a0=180, a1=360)                         # casco
        p.rect(hx - 66, hy - 18, hx + 66, hy - 6, (0.10, 0.14, 0.09), u)
        p.elip(hx - 30, hy + 4, 14, 36, 0, mix(VERDE, (1, 1, 1), 0.3), 0.45 * u)
        p.rect(1560, 860, 1760, 890, (0.05, 0.05, 0.06), u)
        # estrella y rótulo
        est = [rotp(1700, 250, 90 if k % 2 == 0 else 38, -math.pi / 2 + k * math.pi / 5) for k in range(10)]
        p.poly(est, (0.85, 0.85, 0.80), 0.9 * u)
        p.texto("SIMULADOR DE ENTRENAMIENTO", 1480, 380, 40, (0.75, 0.95, 0.8), "mono", u)
        fl = smooth((t - t2 - 0.5) / 0.8)
        p.linea((1000, 520), (1000 + 80 * fl, 520), 12, (1.0, 0.85, 0.3), u)
        p.poly([(1000 + 80 * fl, 495), (1040 + 80 * fl, 520), (1000 + 80 * fl, 545)], (1.0, 0.85, 0.3), u * fl)


@portal("prueba")
def prueba(p, t):
    """Prueba de campo: un técnico deja un prototipo sin rótulo en un salón real, mira cómo juegan los chicos y cronometra."""
    g = "gobierno"
    t0 = INI(g, 4)
    salon(p, t, luz=0.9)
    cx, cy, ch = 1100, 1050, 800
    cabina(p, cx, cy, ch, t, pant_tunel, color=(0.07, 0.065, 0.06), borde=(0.14, 0.13, 0.11), luz=AMBAR, marq=(0.35, 0.33, 0.30), rotulo="PROTOTIPO")
    # cinta de carrocero con «PRUEBA»
    p.poly([(cx - 150, cy - ch * 0.40), (cx + 150, cy - ch * 0.37), (cx + 150, cy - ch * 0.31), (cx - 150, cy - ch * 0.34)], (0.90, 0.85, 0.60))
    p.texto("PRUEBA · NO A LA VENTA", cx, cy - ch * 0.355, 26, (0.15, 0.12, 0.10), "mono")
    for k, (x, pelo) in enumerate(((820, "corto"), (640, "largo"))):
        if k == 0:
            j = jugador(p, x, 1068, 480, t, 1, FIG, pelo)
        else:
            j = persona(p, x, 1068, 450, pose_estar(t * 1.4, lean=0.08), FIG, 1, pelo=pelo)
        luz_cara(p, j, x, 1068, 1, AMBAR, 480, 0.4)
    # técnico con tablilla y cronómetro, a la derecha
    j = persona(p, 1560, 1068, 660, dict(ll=(0.05, 0), lr=(-0.06, 0), bl=(0.85, 1.25), br=(0.75, 1.5 + 0.12 * math.sin(t * 8)), lean=0.04, head=0.25), FIG, -1,
                ropa="chaqueta",
                objeto=lambda pp, wr, wl, f: pp.poly([(wl[0] + 20, wl[1] - 80), (wl[0] - 90, wl[1] - 55), (wl[0] - 80, wl[1] + 55), (wl[0] + 30, wl[1] + 30)], (0.85, 0.83, 0.74)))
    luz_cara(p, j, 1560, 1068, -1, AMBAR, 660, 0.35)
    reloj(p, 1640, 300, 110, t, h=0, m=(t - t0) * 12.0, segundero=True, cara=(0.90, 0.88, 0.80))
    # hoja de resultados que se va llenando
    u = clamp((t - t0 - 0.8) / 4.0)
    p.rrect(150, 230, 560, 640, 10, (0.90, 0.88, 0.80), 0.95)
    p.texto("PRUEBA DE CAMPO", 355, 275, 34, (0.5, 0.08, 0.08), "mono")
    for k, s in enumerate(("PARTIDAS", "MONEDAS", "MINUTOS", "¿GUSTA?")):
        y = 345 + k * 72
        p.texto(s, 180, y, 28, (0.15, 0.15, 0.2), "mono", 1, "lm")
        p.rect(360, y - 12, 360 + 170 * clamp(u * 1.6 - k * 0.15), y + 12, (0.15, 0.35, 0.65))


# ================================================================================================ PRUEBAS
@functools.lru_cache(maxsize=2)
def _pagina(seed, ancho=900, alto=1200):
    """Página de periódico GENÉRICA (titulares propios, columnas ilegibles) para el lector de microfilm."""
    rng = np.random.default_rng(seed)
    pil = Image.new("RGB", (ancho, alto), (214, 208, 190))
    d = ImageDraw.Draw(pil)
    import tablero as T
    d.text((ancho / 2, 46), "DIARIO LOCAL · 1981", font=T.fnt("serif", 54), fill=(25, 25, 25), anchor="mm")
    d.line([(30, 88), (ancho - 30, 88)], fill=(30, 30, 30), width=4)
    tit = [["SUBE EL PRECIO DE LA GASOLINA", "EL AYUNTAMIENTO APRUEBA EL PRESUPUESTO", "LLUVIAS TODA LA SEMANA"],
           ["CHICOS ENFERMOS TRAS HORAS EN LOS RECREATIVOS", "REDADA EN SALONES DE JUEGO", "EL EQUIPO LOCAL GANA EN CASA"]][seed % 2]
    y = 110
    for k, s in enumerate(tit):
        f = T.fnt("serif", 44 if k == 0 else 34)
        cur, lin = "", []
        for w in s.split():
            if f.getlength((cur + " " + w).strip()) > ancho - 80 and cur:
                lin.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lin.append(cur)
        for ln in lin:
            d.text((40, y), ln, font=f, fill=(20, 20, 20))
            y += 50 if k == 0 else 40
        y += 8
        for c in range(3):
            yy = y
            cw = (ancho - 80 - 40) / 3
            for r in range(int(8 + rng.integers(0, 6))):
                w = cw * (0.55 + 0.45 * rng.random()) if rng.random() < 0.15 else cw
                d.line([(40 + c * (cw + 20), yy), (40 + c * (cw + 20) + w, yy)], fill=(95, 92, 85), width=5)
                yy += 15
        y += 14 * 15 + 26
    return np.asarray(pil, np.float32) / 255.0, tit


def _pegar_img(p, im, x, y, w, op=1.0, tono=(1, 1, 1)):
    """Pega una imagen float32 (h, w, 3) con su esquina superior izquierda en (x, y) del lienzo de 1920 y ancho w."""
    k = w * K / im.shape[1]
    sm = cv2.resize(im, (max(2, int(im.shape[1] * k)), max(2, int(im.shape[0] * k))), interpolation=cv2.INTER_AREA)
    x0, y0 = int(x * K), int(y * K)
    xs0, ys0, xs1, ys1 = max(0, x0), max(0, y0), min(HW, x0 + sm.shape[1]), min(HH, y0 + sm.shape[0])
    if xs1 <= xs0 or ys1 <= ys0:
        return
    reg = p.im[ys0:ys1, xs0:xs1]
    reg *= 1 - op
    reg += sm[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0] * np.float32(tono) * op


@portal("hemeroteca")
def hemeroteca(p, t):
    """Lector de microfilm: pasan los periódicos de 1981. Menciones de la máquina: cero. Noticias de los chicos enfermos: sí."""
    pr_ = "pruebas"
    t0, t6 = INI(pr_, 5), INI(pr_, 6)
    p.fondo((0.020, 0.018, 0.016), (0.050, 0.042, 0.034))
    # mueble del lector
    p.rrect(260, 60, 1660, 960, 30, (0.10, 0.09, 0.085))
    p.rect(330, 120, 1590, 860, (0.02, 0.02, 0.02))
    fase = clamp((t - t6 + 0.4) / 0.8)
    # las páginas se desplazan de derecha a izquierda; en la frase 6 se detiene sobre la noticia de los chicos
    v = (t - t0) * 520 * (1 - smooth(fase))
    for k in range(4):
        im, _ = _pagina(k % 2)
        x = 380 + k * 640 - (v % 1280) + (0 if fase < 1 else 0)
        if -700 < x < 1700 and fase < 1:
            _pegar_img(p, im, x, 150, 560, 1.0, (0.92, 0.95, 0.85))
    if fase > 0:
        im, _ = _pagina(1)
        _pegar_img(p, im, lerp(1700, 640, smooth(fase)), 150, 640, 1.0, (0.95, 0.97, 0.88))
        ur = smooth((t - ww(pr_, 6, "si") + 0.3) / 0.5)
        p.rect(660, 232, 1260, 322, (1.0, 0.9, 0.2), 0.40 * ur)
        p.polilinea(T_circ(960, 278, 330, 70), 8, (0.85, 0.08, 0.08), ur)
    # máscara del visor (tapa lo que sale del cristal) y reflejo
    p.rect(260, 60, 330, 960, (0.10, 0.09, 0.085))
    p.rect(1590, 60, 1660, 960, (0.10, 0.09, 0.085))
    p.rect(260, 860, 1660, 960, (0.10, 0.09, 0.085))
    p.rect(260, 60, 1660, 120, (0.10, 0.09, 0.085))
    p.rect(0, 960, W, H, (0.020, 0.018, 0.016))
    p.rect(0, 0, W, 60, (0.020, 0.018, 0.016))
    p.rect(0, 0, 260, H, (0.020, 0.018, 0.016))
    p.rect(1660, 0, W, H, (0.020, 0.018, 0.016))
    p.poly([(330, 120), (900, 120), (330, 520)], (1, 1, 1), 0.04)
    p.glow(960, 490, 900, (0.9, 0.95, 0.8), 0.07)
    # manivela y bobinas
    for x in (150, 1770):
        engranaje(p, x, 760, 70, (t - t0) * 160 * (1 - smooth(fase)) * (1 if x < 900 else -1), (0.30, 0.28, 0.26), 8)
        p.circ(x, 760, 22, (0.08, 0.07, 0.07))
    # contadores
    p.rrect(330, 880, 1590, 950, 10, (0.03, 0.03, 0.03))
    if fase < 0.5:
        n = int((t - t0) * 37)
        p.texto(f"PÁGINAS REVISADAS: {n:04d}", 370, 915, 34, (0.85, 0.9, 0.75), "mono", 1, "lm")
        p.texto("«POLYBIUS»: 0", 1550, 915, 38, (1.0, 0.3, 0.25), "mono", 1, "rm")
    else:
        p.texto("LOS CHICOS ENFERMOS: SÍ APARECEN", 960, 915, 36, (1.0, 0.9, 0.3), "mono")
    if fase < 0.5:                                                                                  # lupa que busca
        lx, ly = 760 + 380 * math.sin((t - t0) * 0.9), 470 + 160 * math.sin((t - t0) * 1.7)
        p.circ(lx, ly, 110, (1.0, 1.0, 0.9), 0.16)
        poligono(p, lx, ly, 112, 40, 0, 14, (0.25, 0.22, 0.20))
        p.linea((lx + 82, ly + 82), (lx + 190, ly + 190), 26, (0.30, 0.18, 0.10))


def T_circ(cx, cy, rx, ry, n=40):
    return [(cx + rx * math.cos(2 * math.pi * k / n * 1.06 - 0.4), cy + ry * math.sin(2 * math.pi * k / n * 1.06 - 0.4) + 6 * math.sin(k * 0.7)) for k in range(n + 1)]


# ================================================================================================ ORIGEN
@portal("web2000")
def web2000(p, t):
    """Monitor de tubo del año 2000: una base de datos de máquinas recreativas donde alguien sube la ficha. Recreación genérica."""
    o = "origen"
    t0, t3, t4 = ww(o, 2, "sitio") - 0.6, INI(o, 3), INI(o, 4)
    p.fondo((0.030, 0.035, 0.060), (0.060, 0.050, 0.070))
    # escritorio, monitor de tubo
    p.rect(0, 960, W, H, (0.10, 0.075, 0.055))
    p.rrect(170, 30, 1750, 970, 46, (0.78, 0.76, 0.68))
    p.rrect(170, 30, 1750, 970, 46, (0.0, 0.0, 0.0), 0.10)
    p.rrect(230, 80, 1690, 900, 30, (0.02, 0.02, 0.03))
    ax0, ay0, ax1, ay1 = ventana_web(p, 260, 105, 1660, 880, "Base de datos de recreativas", "http://www.recreativas-antiguas.ejemplo/juego/polybius", t, t0)
    p.texto("FICHA DE JUEGO", ax0 + 30, ay0 + 44, 44, (0.15, 0.10, 0.45), "serif", 1, "lm")
    p.linea((ax0 + 30, ay0 + 76), (ax1 - 30, ay0 + 76), 3, (0.15, 0.10, 0.45))
    # recuadro «sin imagen»
    p.rect(ax1 - 380, ay0 + 100, ax1 - 40, ay0 + 360, (0.80, 0.80, 0.78))
    p.linea((ax1 - 380, ay0 + 100), (ax1 - 40, ay0 + 360), 3, (0.6, 0.6, 0.6))
    p.linea((ax1 - 40, ay0 + 100), (ax1 - 380, ay0 + 360), 3, (0.6, 0.6, 0.6))
    p.texto("SIN IMAGEN", ax1 - 210, ay0 + 390, 28, (0.4, 0.4, 0.4), "mono")
    campos = [("Nombre:", "POLYBIUS", t0 + 1.6), ("Año:", "1981", t4 + 2.6), ("Fabricante:", "S············n", t0 + 2.4),
              ("Tipo:", "raro, abstracto, muy rápido", t4 + 0.6), ("Derechos:", "(c) 1981", ww(o, 4, "derechos") - 0.2)]
    for k, (et, val, tc) in enumerate(campos):
        y = ay0 + 130 + k * 62
        p.texto(et, ax0 + 40, y, 32, (0.1, 0.1, 0.1), "sans_b", 1, "lm")
        n = int(clamp((t - tc) / 0.9) * len(val))
        if n:
            p.texto(val[:n], ax0 + 260, y, 32, (0.05, 0.05, 0.35), "mono", 1, "lm")
    # el comentario
    uq = clamp((t - ww(o, 3, "alguien", 1) + 0.2) / 1.6) if t > t3 else 0.0
    q = "¿Alguien ha oído hablar de este juego?"
    p.rect(ax0 + 30, ay0 + 470, ax1 - 30, ay0 + 610, (1.0, 1.0, 0.86))
    p.rect(ax0 + 30, ay0 + 470, ax0 + 40, ay0 + 610, (0.85, 0.65, 0.1))
    p.texto(q[:int(uq * len(q))] + ("|" if 0 < uq < 1 else ""), ax0 + 64, ay0 + 540, 46, (0.12, 0.10, 0.10), "serif_i", 1, "lm")
    # fecha del sistema
    p.rect(ax1 - 300, ay1 - 60, ax1 - 20, ay1 - 14, (0.76, 0.76, 0.76))
    p.texto("06/02/2000", ax1 - 160, ay1 - 37, 30, (0.05, 0.05, 0.05), "mono")
    # cursor del ratón
    mx, my = lerp(1500, ax0 + 520, smooth((t - t3) / 1.2)), lerp(820, ay0 + 560, smooth((t - t3) / 1.2))
    p.poly([(mx, my), (mx, my + 34), (mx + 9, my + 26), (mx + 16, my + 40), (mx + 22, my + 37), (mx + 15, my + 23), (mx + 26, my + 23)], (0.02, 0.02, 0.02))
    # brillo del tubo y líneas
    p.glow(960, 480, 1100, (0.6, 0.7, 1.0), 0.06)
    for y in range(110, 880, 12):
        p.rect(260, y, 1660, y + 2, (0, 0, 0), 0.05)
    p.circ(1620, 935, 9, (0.3, 1.0, 0.4), 0.6 + 0.4 * math.sin(t * 3))
    rotulo_rec(p, "RECREACIÓN · NO ES LA PÁGINA REAL", 1730, 1040)
    zz = 0.16 * smooth((t - t3) / 5.0) - 0.06 * smooth((t - t4) / 4.0)
    zoom_p(p, 1.0 + zz, 0.40 + 0.10 * smooth((t - t4) / 3.0), 0.62 - 0.22 * smooth((t - t4) / 3.0))


@functools.lru_cache(maxsize=1)
def _mapa_mundo():
    """Mapa del mundo (costas reales de Natural Earth) en azul noche, cacheado como imagen."""
    paises = json.load(open(r"C:\FabricaAnimaciones\nucleo\datos\paises.json", encoding="utf-8"))
    pil = Image.new("RGB", (HW, HH), (8, 14, 30))
    d = ImageDraw.Draw(pil)
    for k in range(-180, 181, 30):
        x = _px(k, 0)[0] * K
        d.line([(x, 0), (x, HH)], fill=(14, 24, 46), width=1)
    for k in range(-60, 91, 30):
        y = _px(0, k)[1] * K
        d.line([(0, y), (HW, y)], fill=(14, 24, 46), width=1)
    for nombre, polys in paises.items():
        col = (70, 62, 34) if nombre in ("Ukraine", "Ucrania") else (26, 44, 70)
        for poly in polys:
            ring = poly[0] if isinstance(poly[0][0], list) else poly
            pts = [(_px(lo, la)[0] * K, _px(lo, la)[1] * K) for lo, la in ring]
            if len(pts) > 2:
                d.polygon(pts, fill=col, outline=(70, 100, 140))
    return np.asarray(pil, np.float32) / 255.0


def _px(lon, lat, caja=(-150, 78, 70, 15)):
    l0, la0, l1, la1 = caja
    return (lon - l0) / (l1 - l0) * W, (la0 - lat) / (la0 - la1) * H


@portal("viaje")
def viaje(p, t):
    """Prometieron más datos tras un viaje a Ucrania: el avión cruza el mapa... y el buzón sigue vacío mientras pasan los años."""
    o = "origen"
    t0 = INI(o, 6)
    tn = ww(o, 6, "nunca") - 0.3
    p.im[:] = _mapa_mundo()
    a, b = _px(-122.7, 45.5), _px(30.5, 50.45)
    u = smooth((t - t0 - 0.3) / max(1.0, tn - t0 - 0.6))
    pin(p, a[0], a[1], 16, (0.3, 0.8, 1.0), t)
    pin(p, b[0], b[1], 16, (1.0, 0.8, 0.2), t)
    p.texto("OREGÓN", a[0], a[1] + 56, 34, (0.8, 0.9, 1.0), "sans_b")
    p.texto("KIEV", b[0], b[1] + 56, 34, (1.0, 0.9, 0.6), "sans_b")
    arco(p, a, b, u, 300, (1.0, 0.85, 0.4), 6, True)
    # avión en la punta del arco
    if 0 < u < 1:
        x = lerp(a[0], b[0], u)
        y = lerp(a[1], b[1], u) - 300 * 4 * u * (1 - u)
        ang = math.atan2((b[1] - a[1]) - 300 * 4 * (1 - 2 * u), b[0] - a[0])
        R_ = rot((x, y), math.degrees(ang))
        p.poly([R_((x + 40, y)), R_((x - 26, y - 10)), R_((x - 34, y)), R_((x - 26, y + 10))], (0.95, 0.95, 0.9))
        p.poly([R_((x + 6, y)), R_((x - 16, y - 40)), R_((x - 24, y - 40)), R_((x - 10, y))], (0.95, 0.95, 0.9))
        p.poly([R_((x + 6, y)), R_((x - 16, y + 40)), R_((x - 24, y + 40)), R_((x - 10, y))], (0.95, 0.95, 0.9))
    p.texto("2009", 960, 120, 100, (0.95, 0.9, 0.8), "abril", smooth((t - t0) / 0.5) * (1 - smooth((t - tn) / 0.4)))
    # «Nunca llegaron»: buzón vacío con telarañas y años que pasan
    un = smooth((t - tn) / 0.6)
    if un > 0:
        p.rect(0, 0, W, H, (0.0, 0.0, 0.02), 0.72 * un)
        p.rrect(560, 380, 1360, 860, 20, (0.14, 0.15, 0.20), un)
        p.rect(600, 430, 1320, 520, (0.02, 0.02, 0.03), un)
        p.texto("BANDEJA DE ENTRADA", 960, 475, 40, (0.6, 0.65, 0.75), "mono", un)
        p.texto("0 mensajes", 960, 660, 90, (1.0, 0.3, 0.25), "abril", un)
        for k in range(6):
            aa = math.radians(8 + k * 15)
            p.linea((560, 380), (560 + 260 * math.cos(aa), 380 + 260 * math.sin(aa)), 2, (0.7, 0.7, 0.7), 0.3 * un)
        for r in (80, 150, 220):
            p.polilinea([(560 + r * math.cos(math.radians(8 + k * 15)), 380 + r * math.sin(math.radians(8 + k * 15))) for k in range(6)], 2, (0.7, 0.7, 0.7), 0.25 * un)
        anio = 2009 + int(clamp((t - tn - 0.4) / 2.2) * 17)
        hoja_cal(p, 960, 200, 260, 250, "AÑO", str(anio), ((t - tn) * 5.0) % 1.0 if anio < 2026 else 0.0)


# ================================================================================================ POR QUÉ
@portal("padres")
def padres(p, t):
    """Desde la calle: los padres miran por el escaparate cómo su hijo no se despega de la máquina; el reloj de la calle marca tarde."""
    q = "porque"
    t0 = INI(q, 1)
    p.fondo((0.020, 0.025, 0.060), (0.060, 0.050, 0.100))
    estrellas(p, t, 40, 8, 0.3, 0.5)
    # fachada con gran escaparate; dentro, el salón encendido
    p.rect(0, 180, W, 960, (0.060, 0.050, 0.085))
    x0, y0, x1, y1 = 520, 300, 1800, 900
    q_ = P()
    salon(q_, t, y_suelo=820, n=6, luz=1.0)
    j = jugador(q_, 1040, 1010, 520, t, 1, FIG, "corto")
    sx, sy = cabina_lado(q_, 1330, 1010, 760, -1, t, color=(0.05, 0.05, 0.07), luz=MAG)
    luz_cara(q_, j, 1040, 1010, 1, MAG, 520, 0.6)
    zoom_p(q_, 1.0, 0.5, 0.5)
    sub = cv2.resize(q_.im, (int((x1 - x0) * K), int((y1 - y0) * K)), interpolation=cv2.INTER_AREA)
    p.im[int(y0 * K):int(y0 * K) + sub.shape[0], int(x0 * K):int(x0 * K) + sub.shape[1]] = sub
    p.rect(x0 - 14, y0 - 14, x1 + 14, y0, (0.03, 0.03, 0.05))
    p.rect(x0 - 14, y1, x1 + 14, y1 + 14, (0.03, 0.03, 0.05))
    p.rect(x0 - 14, y0, x0, y1, (0.03, 0.03, 0.05))
    p.rect(x1, y0, x1 + 14, y1, (0.03, 0.03, 0.05))
    p.poly([(x0, y0), (x0 + 420, y0), (x0 + 120, y1), (x0, y1)], (1, 1, 1), 0.05)                     # reflejo del cristal
    neon(p, "VIDEOJUEGOS", 1160, 238, 70, CIAN, t, 3.0)
    suelo(p, 960, (0.05, 0.05, 0.08), (0.015, 0.015, 0.03))
    p.poly([(x0, 960), (x1, 960), (x1 + 200, 1080), (x0 - 300, 1080)], (0.75, 0.35, 0.85), 0.10)     # luz que sale a la acera
    # padres en la acera, de espaldas a nosotros y mirando dentro
    persona(p, 250, 1050, 720, dict(ll=(0.04, 0), lr=(-0.05, 0), bl=(0.1, 0.1), br=(1.15, 1.2 + 0.05 * math.sin(t * 2)), lean=0.06, head=0.1), FIG, 1,
            ropa="chaqueta")
    persona(p, 430, 1055, 660, dict(ll=(0.04, 0), lr=(-0.04, 0), bl=(0.55, 2.3), br=(0.2, 0.3), lean=0.05 + 0.01 * math.sin(t * 1.4), head=0.15), FIG, 1,
            ropa="vestido", pelo="moño")
    # reloj de farola
    p.rect(118, 420, 132, 1050, (0.03, 0.03, 0.05))
    reloj(p, 125, 360, 70, t, h=10.0 + (t - t0) * 0.35, m=(t - t0) * 21.0, segundero=False, cara=(0.90, 0.88, 0.80))
    p.glow(125, 360, 220, (1.0, 0.9, 0.7), 0.25)
    lluvia(p, t, 0.12, 50)


@portal("mente")
def mente(p, t):
    """El rumor: un edificio oficial emite ondas hacia una cabeza con una espiral que gira; encima, una carpeta «ALTO SECRETO»."""
    q = "porque"
    t0 = INI(q, 3)
    p.fondo((0.060, 0.035, 0.070), (0.200, 0.080, 0.100))
    estrellas(p, t, 50, 4, 0.5, 0.4)
    p.glow(1400, 520, 800, (0.5, 0.2, 0.25), 0.22)
    suelo(p, 900, (0.045, 0.03, 0.045), (0.015, 0.012, 0.02))
    columnas(p, 400, 900, 520, 420, (0.30, 0.28, 0.32), FIG, 6, 1.0)
    p.rect(396, 260, 404, 420, (0.25, 0.25, 0.28))                                                   # antena
    for k in range(5):
        r = ((t * 0.5 + k / 5) % 1.0)
        p.elip(400, 260, 60 + 1200 * r, 60 + 1200 * r, 0, (1.0, 0.4, 0.3), 0.0)
        poligono(p, 400, 260, 60 + 1250 * r, 40, 0, 6, (1.0, 0.45, 0.35), 0.5 * (1 - r))
    # cabeza de perfil mirando a la izquierda
    hx, hy = 1380, 500
    p.poly([(1150, 1080), (1190, 900), (1310, 830), (1470, 830), (1620, 900), (1690, 1080)], FIG)
    p.rect(1330, 700, 1460, 850, FIG)
    p.elip(hx, hy, 200, 240, 0, FIG)
    p.poly([(hx - 190, hy - 10), (hx - 250, hy + 70), (hx - 185, hy + 95)], FIG)
    p.circ(hx + 20, hy - 30, 150, (0.06, 0.04, 0.07))
    pts = []
    for k in range(120):                                                                            # espiral que gira
        a = k * 0.26 + t * 2.4
        r = 4 + k * 1.15
        pts.append((hx + 20 + r * math.cos(a), hy - 30 + r * math.sin(a)))
    p.polilinea(pts, 8, (1.0, 0.45, 0.35), 0.9, caps=False)
    p.glow(hx + 20, hy - 30, 220, (1.0, 0.3, 0.25), 0.25 + 0.1 * math.sin(t * 4))
    # carpeta que cae con el sello
    u = ease_back((t - ww(q, 3, "secretos") + 0.5) / 0.7) if t > ww(q, 3, "secretos") - 0.5 else 0.0
    if u > 0:
        cx, cy = 900, lerp(-200, 330, min(u, 1.0))
        p.poly([(cx - 190, cy - 120), (cx - 40, cy - 120), (cx - 10, cy - 150), (cx + 190, cy - 150), (cx + 190, cy + 130), (cx - 190, cy + 130)], (0.72, 0.60, 0.36))
        p.rect(cx - 170, cy - 100, cx + 170, cy + 110, (0.80, 0.68, 0.42))
        us = smooth((t - ww(q, 3, "secretos") - 0.3) / 0.25)
        p.rrect(cx - 150, cy - 30, cx + 150, cy + 50, 8, (0.75, 0.08, 0.08), 0.0)
        p.texto("ALTO SECRETO", cx, cy + 10, 52, (0.72, 0.06, 0.06), "sans_b", us)
        p.polilinea([(cx - 160, cy - 34), (cx + 160, cy - 34), (cx + 160, cy + 54), (cx - 160, cy + 54)], 6, (0.72, 0.06, 0.06), us, cerrado=True)
    p.texto("RUMOR", 1700, 120, 60, (1.0, 0.85, 0.3), "mono", 0.9)
    niebla(p, t, 960, 260, (0.30, 0.15, 0.20), 0.4, 18, 5)


@portal("recreacion")
def recreacion(p, t):
    """2007: un ordenador de sobremesa donde alguien descarga un juego gratuito que IMAGINA cómo habría sido el original."""
    q = "porque"
    t0 = INI(q, 6)
    p.fondo((0.030, 0.030, 0.045), (0.060, 0.050, 0.060))
    p.rect(0, 940, W, H, (0.11, 0.085, 0.065))
    p.rrect(330, 60, 1590, 860, 26, (0.06, 0.06, 0.07))
    p.rect(900, 860, 1020, 930, (0.06, 0.06, 0.07))
    p.rrect(760, 920, 1160, 950, 10, (0.06, 0.06, 0.07))
    p.rect(370, 100, 1550, 820, (0.10, 0.20, 0.38))
    ud = clamp((t - t0 - 0.4) / 1.8)
    if ud < 1:
        p.rrect(560, 340, 1360, 580, 12, (0.90, 0.90, 0.88))
        p.texto("Descargando juego gratuito…", 960, 400, 40, (0.1, 0.1, 0.1), "sans")
        p.rect(620, 460, 1300, 510, (0.7, 0.7, 0.7))
        p.rect(620, 460, 620 + 680 * ud, 510, (0.2, 0.7, 0.3))
        p.texto(f"{int(ud * 100)} %", 960, 545, 30, (0.1, 0.1, 0.1), "mono")
    else:
        ua = smooth((t - t0 - 2.2) / 0.5)
        x0, y0, x1, y1 = lerp(900, 420, ua), lerp(430, 130, ua), lerp(1020, 1500, ua), lerp(490, 790, ua)
        p.rect(x0, y0 - 40 * ua, x1, y1, (0.75, 0.75, 0.76))
        p.rect(x0 + 4, y0 - 36 * ua, x1 - 4, y0, (0.15, 0.25, 0.60))
        p.texto("Homenaje de fans (2007)", x0 + 20, y0 - 18, 28, (1, 1, 1), "sans_b", ua, "lm")
        pant_formas(p, x0 + 6, y0 + 4, x1 - 6, y1 - 6, t, ua, 1.0, True, 1.2)
    p.texto("2007", 200, 200, 110, (0.95, 0.9, 0.8), "abril", smooth((t - t0) / 0.5))
    # teclado, ratón y silueta de espaldas
    p.rrect(700, 965, 1220, 1010, 8, (0.07, 0.07, 0.08))
    p.elip(1330, 990, 40, 26, 0, (0.07, 0.07, 0.08))
    p.elip(960, 1120, 260, 120, 0, FIG)
    p.circ(960, 930, 110, FIG)
    p.elip(960, 838, 90, 26, 0, (0.5, 0.45, 0.8), 0.35)
    rotulo_rec(p, "DIBUJO PROPIO · NO ES EL JUEGO REAL", 1880, 1050)


# ================================================================================================ CENTRO / CIERRE
@portal("busqueda", 0.55)
def busqueda(p, t):
    """Un almacén a oscuras lleno de cabinas tapadas con sábanas: la linterna busca y solo encuentra polvo. Al fondo, quizá, una cabina negra."""
    z = "cierre"
    try:
        t3 = INI(z, 3)
        tf = ww(z, 4, "maquina")
    except Exception:
        t3, tf = 1e9, 1e9
    p.fondo((0.030, 0.034, 0.055), (0.075, 0.070, 0.090))
    suelo(p, 800, (0.110, 0.100, 0.110), (0.030, 0.030, 0.040))
    for k in range(10):                                                                             # vigas
        x = 960 + (k - 4.5) * 420
        p.linea((x, -10), (960 + (k - 4.5) * 120, 420), 10, (0.02, 0.02, 0.028), 1, caps=False)
    # cabinas tapadas en dos filas
    rng = np.random.default_rng(5)
    for fila, (yb, hh, n) in enumerate(((830, 300, 9), (960, 470, 6))):
        for k in range(n):
            x = (k + 0.5) / n * (W + 240) - 120 + (60 if fila else 0)
            if fila == 0 and k == 4:
                continue
            w = hh * 0.42
            col = mix((0.26, 0.26, 0.30), (0.40, 0.38, 0.36), rng.random())
            p.poly([(x - w * 0.62, yb), (x - w * 0.55, yb - hh * 0.9), (x - w * 0.2, yb - hh * 1.02), (x + w * 0.3, yb - hh), (x + w * 0.58, yb - hh * 0.86),
                    (x + w * 0.66, yb)], col)
            for d in (-0.3, 0.05, 0.36):
                p.linea((x + w * d, yb - hh * 0.92), (x + w * (d + 0.06), yb - 6), 3, (0.04, 0.04, 0.05), 0.6, caps=False)
    # la cabina negra del fondo (hueco de la fila): solo se adivina
    cx, cy, ch = 960, 838, 330
    brilla = smooth((t - tf + 0.2) / 0.8) if t > tf - 0.2 else 0.0
    cabina(p, cx, cy, ch, t, pant_formas if brilla > 0.3 else None, color=(0.012, 0.012, 0.018), borde=(0.03, 0.03, 0.04), luz=VIOL, marq=(0.5, 0.2, 0.9),
           encendida=brilla > 0.3)
    # linterna que barre
    oscuro = p.im.copy() * np.float32([0.26, 0.30, 0.42])
    bx = 960 + 620 * math.sin(t * 0.45) * (1 - brilla)
    by = 700 + 90 * math.sin(t * 0.8)
    gx, gy = np.meshgrid(np.arange(HW, dtype=np.float32), np.arange(HH, dtype=np.float32))
    m = np.clip(1 - np.sqrt(((gx - bx * K) / (330 * K)) ** 2 + ((gy - by * K) / (300 * K)) ** 2), 0, 1) ** 1.2
    p.im[:] = oscuro + p.im * m[..., None] * np.float32([1.25, 1.15, 0.95])
    p.haz(960, 1180, math.degrees(math.atan2(by - 1180, bx - 960)), 1300, 20, (1.0, 0.95, 0.8), 0.10)
    polvo(p, t, 60, 2, 0.35, (1.0, 0.95, 0.8), 7)
    if brilla > 0.3:
        p.glow(cx, cy - ch * 0.68, 420, (0.5, 0.3, 1.0), 0.5 * brilla * (0.6 + 0.4 * math.sin(t * 6)))
