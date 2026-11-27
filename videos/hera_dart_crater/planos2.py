# -*- coding: utf-8 -*-
"""Planos 2: el impacto, el resultado, la pregunta. Mundo LOCAL en metros (Didymos en el origen)."""
import math

import numpy as np

from comun import (H, W, L3, Cam, E, ap, cabecera, clamp, contador, e_inout, e_out, etiqueta3d, F0, F1, foto, lerp, pr,
                   real, smooth, T0, T1, vacio, vent, ww, a_img, _Img, circulo3d, nrm)
from p3d import (O, X, Y, Z, SOL, R_DID, R_DIM, R_ORB, P_ANTES, P_DESPUES, cam_orb, pos_dim, didymos, dimorphos, orbita,
                 flecha3d, reloj)
from planos1 import rp, con_foto
from _seg import SEG

PD = np.array([R_ORB, 0.0, 0.0])      # Dimorphos en el momento del choque (DART llega desde -y)
DIR_DART = nrm(np.array([0.15, 1.0, -0.1]))


# ------------------------------------------------------------------ IMPACTO
def i_aprox(t):
    """Cámara detrás de DART: Dimorphos crece de punto a montaña de rocas."""
    t0 = F0("impacto", 1) - 0.3
    t1 = F1("impacto", 2) + 0.3
    k = pr(t, t0, t1)
    dist = 9000 * (1 - k) ** 2.2 + 140                  # metros de DART al centro de Dimorphos
    P_dart = PD - DIR_DART * dist
    cam = Cam(P_dart - DIR_DART * 34 + np.array([0, 0, 9.0]), PD, Z, 40, cerca=0.1, centro=(W * 0.5, H * 0.42))
    lz = L3(cam)
    E.estrellas(lz)
    didymos(lz, t, rocas=80)
    dimorphos(lz, PD, yaw=40, rocas=320)
    E.dart(lz, P_dart, E.rot_ypr(math.degrees(math.atan2(DIR_DART[1], DIR_DART[0])), 0, 0), rosa=1.0)
    o = ap(t, t0 + 0.2)
    lz.texto("22 500 KM/H", 1600, 200, 86, "Bold Condensed", o, "mm", esp=0.03)
    lz.texto("SIN FRENAR · SIN EXPLOSIVOS", 1600, 260, 24, "SemiBold Condensed", o * 0.9, "mm", esp=0.18)
    lz.texto(f"DISTANCIA {dist / 1000:4.1f} KM", 120, 200, 26, "SemiBold Condensed", o * 0.85, "lm", esp=0.16)
    cabecera(lz, "DART · APROXIMACIÓN FINAL · 26-SEP-2022")
    return lz


def i_choque(t):
    """El choque visto de lado (como LICIACube): destello y nube de eyección."""
    tc = ww("impacto", 8, "chorros") - 0.3
    tch = F0("impacto", 8) - 0.3
    lz = L3(cam_orb(PD, 1500, -60, 35, centro=(W * 0.62, H * 0.42)))
    E.estrellas(lz)
    didymos(lz, t, rocas=60)
    dimorphos(lz, PD, yaw=40, rocas=200)
    s = t - tch
    if s > 0:
        Pi = PD - DIR_DART * R_DIM * 0.95
        fl = math.exp(-s * 3.0)
        lz.puntos(Pi, r=30 * fl + 2, op=min(1.0, fl * 1.5))
        E.eyeccion(lz, Pi, -DIR_DART + np.array([0, 0, 0.15]), s, 800, 300, n=900, abre=1.8, ritmo=0.35)
    o = ap(t, tc)
    lz.texto("EYECCIÓN", 1500, 860, 60, "Bold Condensed", o, "mm", esp=0.06)
    lz.texto("ROCAS Y POLVO DISPARADOS AL ESPACIO", 1500, 910, 22, "SemiBold Condensed", o * 0.9, "mm", esp=0.16)
    cabecera(lz, "RECREACIÓN 3D · EL CHOQUE VISTO DE LADO")
    return lz


# ------------------------------------------------------------------ RESULTADO
def r_barras(t):
    t0 = F0("resultado", 1) - 0.3
    ta0 = ww("resultado", 1, "setenta") - 0.2
    lz = L3(cam_orb(np.array([0, 0, 0]), 4300, 10, 58, centro=(W * 0.62, H * 0.55)))
    E.estrellas(lz)
    fo = 1.0 - 0.8 * ap(t, ta0 - 0.5, 0.6)               # el par se apaga cuando entran las barras
    orbita(lz, 0.45 * fo, R_ORB, guion=3)
    didymos(lz, t, op=fo, rocas=60)
    dimorphos(lz, pos_dim(-60 + (t - T0("resultado")) * 30), op=fo, yaw=t * 9)
    o1 = vent(t, T0("resultado") + 0.2, ta0 - 0.3)
    lz.texto("¿SE MOVIÓ?", 120, 470, 150, "Bold Condensed", o1, "lm", esp=0.03)
    lz.texto("LA META DE LA NASA: CAMBIAR SU VUELTA", 124, 580, 30, "SemiBold Condensed",
             o1 * ap(t, F0("resultado", 1)), "lm", esp=0.14)
    reloj(lz, 1520, 220, P_ANTES, vent(t, F0("resultado", 1) + 0.3, ta0 - 0.3) * 0.8, 64, "ANTES DEL CHOQUE")
    cabecera(lz, "¿SE MOVIÓ?")
    x, y = 300, 480
    maxv = 33 * 60.0
    items = [("LO MÍNIMO QUE BUSCABA LA NASA", 73.0, "73 SEGUNDOS", ww("resultado", 1, "setenta") - 0.2),
             ("LO QUE CAMBIÓ", 33 * 60.0, "33 MINUTOS", F0("resultado", 2) + 0.4)]
    for i, (rot, v, tv, ta) in enumerate(items):
        k = e_out(pr(t, ta, ta + (0.6 if i == 0 else 1.6)))
        o = ap(t, ta, 0.25)
        if o <= 0.01:
            continue
        yy = y + i * 220
        w = max(4.0, 1100 * v / maxv * k)
        lz.texto(rot, x, yy - 60, 26, "SemiBold Condensed", o, "lm", esp=0.16)
        lz.l2([(x, yy - 30), (x + w, yy - 30), (x + w, yy + 30), (x, yy + 30)], o, 1.8, cerrada=True)
        for j in range(int(w // 14)):
            xx = x + 7 + j * 14
            lz.l2([(xx, yy + 26), (xx + 10, yy - 26)], o * 0.45, 1.0)
        lz.texto(tv, x + w + 26, yy, 64, "Bold Condensed", o * min(1, k * 2), "lm", esp=0.03)
    o3 = ap(t, ww("resultado", 2, "treinta") + 1.2)
    lz.texto("MÁS DE 25 VECES LO MÍNIMO", 1500, 300, 46, "Bold Condensed", o3, "mm", esp=0.05)
    return lz


def r_orbitas(t):
    """Órbita de antes (fantasma) y de después: Dimorphos se adelanta."""
    t0 = F0("resultado", 3) - 0.3
    lz = L3(cam_orb(np.array([0, 0, 0]), 4300, 10, 58, centro=(W * 0.5, H * 0.52)))
    E.estrellas(lz)
    orbita(lz, 0.35, R_ORB, guion=3)
    orbita(lz, 0.75, R_ORB - 37 * 3, guion=None)        # la nueva (radio exagerado ×3 para que se note)
    didymos(lz, t, rocas=60)
    s = max(0.0, t - t0)
    a_antes = -60 + s * 30
    a_desp = -60 + s * 30 * (P_ANTES / P_DESPUES) ** 1.0 + s * 6
    Pa = pos_dim(a_antes)
    dimorphos(lz, Pa, op=0.3, rocas=0)
    Pb = pos_dim(a_desp, R_ORB - 37 * 3)
    dimorphos(lz, Pb, yaw=t * 9)
    etiqueta3d(lz, Pa, "SIN EL CHOQUE", None, dx=220, dy=-90, op=ap(t, t0 + 0.6) * 0.8, px=26)
    etiqueta3d(lz, Pb, "DESPUÉS DEL CHOQUE", None, dx=-170, dy=-90, op=ap(t, t0 + 0.6), px=26)
    reloj(lz, 1520, 300, P_ANTES, ap(t, t0) * 0.5, 64, "ANTES")
    reloj(lz, 1520, 520, P_DESPUES, ap(t, t0 + 0.4), 96, "AHORA")
    lz.texto("ÓRBITA EXAGERADA PARA QUE SE VEA", 120, 1000, 18, "SemiBold Condensed", ap(t, t0) * 0.6, "lm", esp=0.16)
    cabecera(lz, "LA NUEVA VUELTA DE DIMORPHOS")
    return lz


def r_retroceso(t):
    """El empujón: la nave empuja hacia un lado y el material expulsado, como un cañón al disparar, empuja más."""
    t0 = F0("resultado", 4) - 0.3
    k = pr(t, t0, F1("resultado", 6) + 0.5)
    lz = L3(cam_orb(PD, lerp(1150, 1000, k), 70, 25, centro=(W * 0.52, H * 0.52)))
    E.estrellas(lz)
    dimorphos(lz, PD, yaw=40)
    Pi = PD - DIR_DART * R_DIM * 0.95
    o1 = ap(t, t0 + 0.2)
    flecha3d(lz, Pi - DIR_DART * 420, Pi - DIR_DART * 40, o1, 2.0)
    etiqueta3d(lz, Pi - DIR_DART * 300, "GOLPE DE LA NAVE", None, dx=-160, dy=-120, op=o1, px=28)
    tc = ww("resultado", 5, "material") - 0.3
    s = max(0.0, t - tc)
    if s > 0:
        E.eyeccion(lz, Pi, -DIR_DART + np.array([0, 0, 0.1]), s, 520, 200, n=500, ritmo=0.5)
    o2 = ap(t, ww("resultado", 6, "empujó") - 0.2)
    if o2 > 0:
        L = 160 + 260 * e_out(pr(t, ww("resultado", 6, "empujó") - 0.2, ww("resultado", 6, "empujó") + 1.5))
        flecha3d(lz, PD + DIR_DART * R_DIM * 0.9, PD + DIR_DART * (R_DIM * 0.9 + L), o2, 3.0)
        etiqueta3d(lz, PD + DIR_DART * (R_DIM * 0.9 + L * 0.7), "EMPUJÓN TOTAL", "NAVE + RETROCESO", dx=160, dy=-140, op=o2, px=30)
    o3 = ap(t, ww("resultado", 6, "cañón") - 0.1)
    lz.texto("COMO EL RETROCESO DE UN CAÑÓN", W / 2, 980, 36, "Bold Condensed", o3, "mm", esp=0.08)
    o4 = ap(t, ww("resultado", 6, "cinco") - 0.1)
    lz.texto("DE 2 A 5 VECES MÁS FUERTE", 1500, 220, 50, "Bold Condensed", o4, "mm", esp=0.05)
    o5 = vent(t, ww("resultado", 5, "mil") - 0.1, F0("resultado", 6) - 0.2)
    lz.texto("MÁS DE 1 000 TONELADAS", 1500, 220, 50, "Bold Condensed", o5, "mm", esp=0.05)
    cabecera(lz, "RECREACIÓN 3D · POR QUÉ EMPUJÓ DE MÁS")
    return lz


# ------------------------------------------------------------------ PREGUNTA
def q_punto(t):
    """Desde la Tierra los dos asteroides son un solo punto de luz."""
    t0 = T0("pregunta")
    k = smooth(pr(t, ww("pregunta", 0, "Desde") - 0.6, F0("pregunta", 1) - 0.3))
    d = 3000 * (1 + 400 * k ** 3) * (1 - 0.25 * smooth(pr(t, t0, ww("pregunta", 0, "Desde"))))
    lz = L3(cam_orb(np.array([R_ORB * 0.4, 0, 0]), d, 20, 15))
    E.estrellas(lz)
    if d < 60000:
        didymos(lz, t, rocas=40)
        dimorphos(lz, pos_dim(130), rocas=30)
    else:
        x, y = lz.cam.px(np.array([R_ORB * 0.4, 0, 0]))
        lz.c2(x, y, 3, 1.0, lleno=True)
        lz.c2(x, y, 16, 0.5 * ap(t, F0("pregunta", 0) + 2.5), w=1.2)
        ou = vent(t, ww("pregunta", 0, "punto") - 0.3, F0("pregunta", 1) + 0.6)
        lz.texto("ASÍ SE VEN DESDE LA TIERRA", x + 60, y - 20, 34, "SemiBold Condensed", ou, "lm", esp=0.16)
        lz.texto("UN SOLO PUNTO DE LUZ", x + 60, y + 34, 64, "Bold Condensed", ou, "lm", esp=0.04)
    o = ap(t, F0("pregunta", 1) - 0.2)
    for i, (txt, pal) in enumerate((("¿QUÉ TAN GRANDE ES EL CRÁTER?", "grande"), ("¿CUÁNTO PESA DIMORPHOS?", "pesa"),
                                     ("¿SE DEFORMÓ ENTERO?", "deformó"))):
        oi = ap(t, ww("pregunta", 1, pal) - 0.3)
        lz.texto(txt, 160, 330 + i * 110, 56, "Bold Condensed", oi * (1 - ap(t, ww("pregunta", 2, "apuestas") - 0.4)), "lm", esp=0.04)
    oa = vent(t, ww("pregunta", 2, "apuestas") - 0.1, F0("pregunta", 4) - 0.2)
    lz.texto("LAS APUESTAS", 160, 280, 64, "Bold Condensed", oa, "lm", esp=0.12)
    lz.texto("A · UN CRÁTER DE UNOS 10 M", 160, 380, 52, "Bold Condensed", oa * ap(t, ww("pregunta", 2, "pequeño") - 0.2), "lm", esp=0.04)
    lz.texto("B · SE DESHACE Y SE REARMA", 160, 470, 52, "Bold Condensed", oa * ap(t, ww("pregunta", 2, "otros") - 0.2), "lm", esp=0.04)
    ob = vent(t, F0("pregunta", 3) - 0.1, F0("pregunta", 4) - 0.2)
    lz.texto("SIN ESO: ¿CUÁNTO EMPUJAR?", 160, 600, 52, "Bold Condensed", ob, "lm", esp=0.04)
    o4 = ap(t, ww("pregunta", 4, "ver") - 0.1)
    lz.texto("HAY QUE IR A VER", 160, 760, 70, "Bold Condensed", o4, "lm", esp=0.04)
    cabecera(lz, "DESDE LA TIERRA · UN PUNTO DE LUZ")
    return lz


def S(k, d=0.0):
    return SEG.get(k, d)


FN = "FOTO: NASA / JOHNS HOPKINS APL"


def _draco_fotos(t):
    """Base negra para las fotos de DRACO a pantalla grande."""
    lz = vacio()
    E.estrellas(lz, op=0.4)
    cabecera(lz, "IMÁGENES REALES DE DRACO · NASA / JHU APL")
    return lz


def _base2(cab):
    def f(t):
        lz = vacio()
        E.estrellas(lz, op=0.35)
        cabecera(lz, cab)
        return lz
    return f


def r_sol(t):
    """El par alrededor del Sol: su vuelta (~770 días) cambió 0,15 s. ESQUEMA."""
    from p3d import orbita_planeta, pos_planeta, sol
    t0 = F0("resultado", 7) - 0.3
    k = pr(t, t0, F1("resultado", 7) + 0.3)
    lz = L3(cam_orb(np.array([0.2, 0.1, 0]), 6.0, 10 + 15 * k, 55, fov=36, centro=(W * 0.42, H * 0.53), cerca=0.01))
    E.estrellas(lz, op=0.3)
    sol(lz)
    orbita_planeta(lz, 1.0, 0.35)
    orbita_planeta(lz, 1.64, 0.8, e=0.38, varpi=math.radians(-40))
    P = pos_planeta(1.64, -20 + 40 * k, 0.38, math.radians(-40))
    lz.puntos(P, r=5, op=1.0)
    etiqueta3d(lz, P, "DIDYMOS + DIMORPHOS", "UNA VUELTA AL SOL: UNOS 770 DÍAS", dx=150, dy=-120, op=ap(t, t0 + 0.3), px=28)
    o = ap(t, ww("resultado", 7, "quince") - 0.2)
    lz.texto("0,15 SEGUNDOS", 1520, 300, 90, "Bold Condensed", o, "mm", esp=0.03)
    lz.texto("LO QUE CAMBIÓ SU VUELTA AL SOL", 1520, 370, 24, "SemiBold Condensed", o * 0.9, "mm", esp=0.16)
    lz.texto("ESQUEMA · NO A ESCALA", W - 80, 1010, 18, "SemiBold Condensed", ap(t, t0) * 0.6, "rm", esp=0.16)
    cabecera(lz, "HASTA SU ÓRBITA ALREDEDOR DEL SOL")
    return lz


PLANOS = [
    # ---------------- IMPACTO
    (T0("impacto"), rp("nasa_sala", S("sala_ini", 0.0), T0("impacto"), "26-SEP-2022 · A 11 MILLONES DE KM", "TRANSMISIÓN DE LA NASA")),
    (F0("impacto", 1) - 0.3, i_aprox),
    (F0("impacto", 2) - 0.3, rp("draco", S("draco_ini", 0.0), F0("impacto", 2) - 0.3, "DRACO · DIMORPHOS: UN PUNTO DE LUZ",
                                "JUNTO A DIDYMOS · VIDEO 10× MÁS RÁPIDO")),
    (F0("impacto", 3) - 0.3, con_foto(_draco_fotos,
                                      dict(nombre="dart_ultima2", cx=960, cy=540, ancho=760, t0=F0("impacto", 3) - 0.3,
                                           t1=F0("impacto", 4) - 0.2, rotulo="2,5 MINUTOS ANTES", sub=FN, estilo=0, asp=1.0),
                                      dict(nombre="dart_ultima1", cx=960, cy=540, ancho=760, t0=F0("impacto", 4) - 0.3,
                                           t1=F0("impacto", 5) - 0.2, rotulo="11 SEGUNDOS ANTES", sub=FN, estilo=0, asp=1.0))),
    (F0("impacto", 5) - 0.3, rp("draco", S("draco_fin", 33.0), F0("impacto", 5) - 0.3, "LAS ÚLTIMAS FOTOS", "A VELOCIDAD REAL",
                                tfin=S("draco_ultimo", 38.5))),
    (F0("impacto", 7) - 0.3, rp("apl_sala", S("sala_festejo", 80.0), F0("impacto", 7) - 0.3, "CENTRO DE CONTROL · APL",
                                "SE CORTA LA SEÑAL: IMPACTO")),
    (F0("impacto", 8) - 0.3, con_foto(i_choque, dict(nombre="licia_eyeccion", cx=960, cy=500, ancho=1180,
                                                      t0=ww("impacto", 8, "esto") - 0.1, t1=F0("impacto", 9) - 0.2,
                                                      rotulo="FOTO REAL DE LICIACUBE", sub="FOTO: ASI / NASA · CC BY 2.0",
                                                      estilo=1, asp=1.9))),
    (F0("impacto", 9) - 0.3, con_foto(rp("hubble_x3", 0.0, F0("impacto", 9) - 0.3, "HUBBLE", "EL BRILLO SE TRIPLICA", vel=0.35,
                                         tfin=S("x3_fin", 2.9)),
                                      dict(nombre="webb_hubble", cx=1380, cy=760, ancho=700, t0=F0("impacto", 9) + 0.6,
                                           t1=F0("impacto", 10) - 0.2, rotulo="HUBBLE Y WEBB", sub="FOTO: ESA/WEBB, ESA/HUBBLE · CC BY 4.0",
                                           estilo=2, asp=2.5))),
    (F0("impacto", 10) - 0.3, con_foto(_base2("LA COLA · COMO LA DE UN COMETA"),
                                       dict(nombre="hubble_cola", cx=560, cy=520, ancho=700, t0=F0("impacto", 10) - 0.3,
                                            t1=T1("impacto") + 0.3, rotulo="HUBBLE · DÍAS DESPUÉS", sub="FOTO: NASA, ESA, STSCI · CC BY 4.0",
                                            estilo=0, asp=1.48),
                                       dict(nombre="soar_cola", cx=1330, cy=560, ancho=860, t0=ww("impacto", 10, "chile") - 0.2,
                                            t1=T1("impacto") + 0.3, rotulo="TELESCOPIO SOAR · CHILE",
                                            sub="FOTO: CTIO/NOIRLAB/SOAR · CC BY 4.0", estilo=3, asp=1.49))),
    # ---------------- RESULTADO
    (T0("resultado"), r_barras),
    (F0("resultado", 3) - 0.3, r_orbitas),
    (F0("resultado", 4) - 0.3, con_foto(r_retroceso, dict(nombre="hubble_rocas", cx=470, cy=500, ancho=560,
                                                          t0=ww("resultado", 5, "mil") - 0.2, t1=F0("resultado", 6) - 0.2,
                                                          rotulo="HUBBLE: ROCAS QUE ESCAPAN", sub="FOTO: NASA, ESA, D. JEWITT · CC BY 4.0",
                                                          estilo=2, asp=1.13))),
    (F0("resultado", 7) - 0.3, r_sol),
    (F0("resultado", 8) - 0.3, rp("apl_sala", S("sala_final", 120.0), F0("resultado", 8) - 0.3, "LA PRIMERA VEZ",
                                  "QUE MOVEMOS UN CUERPO DEL SISTEMA SOLAR")),
    # ---------------- PREGUNTA
    (T0("pregunta"), q_punto),
    (F0("pregunta", 4) - 0.3, rp("hera_trailer", S("trailer", 5.0), F0("pregunta", 4) - 0.3, "HERA", "AGENCIA ESPACIAL EUROPEA")),
]


def sfx():
    return [(T0("impacto"), "hud", 0.6, 0.0, None), (F0("impacto", 1) - 0.3, "whoosh", 0.7, 0.0, None),
            (F0("impacto", 3) - 0.2, "foto", 0.6, 0.0, None), (F0("impacto", 4) - 0.2, "foto", 0.6, 0.0, None),
            (F0("impacto", 5) + 0.5, "foto", 0.5, 0.0, None), (F0("impacto", 5) + 1.5, "foto", 0.5, 0.0, None),
            (F0("impacto", 6) - 0.2, "senal", 0.8, 0.0, None), (F0("impacto", 8) - 0.1, "impacto", 0.9, 0.0, None),
            (ww("impacto", 8, "chorros"), "rocas", 0.6, 0.0, None), (F0("impacto", 9), "hud", 0.5, 0.0, None),
            (F0("impacto", 10) - 0.3, "whoosh", 0.5, 0.0, None),
            (ww("resultado", 1, "setenta"), "tic", 0.6, 0.0, None), (F0("resultado", 2) + 0.4, "pulso", 0.9, 0.0, None),
            (F0("resultado", 3) - 0.3, "whoosh", 0.5, 0.0, None), (ww("resultado", 5, "material"), "rocas", 0.6, 0.0, None),
            (ww("resultado", 6, "cañón"), "impacto", 0.45, 0.0, None), (F0("resultado", 8), "sello", 0.6, 0.0, None),
            (T0("pregunta"), "whoosh", 0.5, 0.0, None), (ww("pregunta", 1, "grande"), "tic", 0.5, -0.2, None),
            (ww("pregunta", 1, "pesa"), "tic", 0.5, 0.0, None), (ww("pregunta", 1, "deformó"), "tic", 0.5, 0.2, None),
            (ww("pregunta", 4, "ver"), "pulso", 0.8, 0.0, None)]
