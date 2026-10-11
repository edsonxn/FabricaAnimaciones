# -*- coding: utf-8 -*-
"""Escena 2 · Nueva España (0:17-1:06): territorio y barco a España, ruta de la plata, pirámide social (tres islas), un criollo se pregunta, decreto de 1804 y la ruina."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_gente_iso as G
import kz_iso_deco as DC
import kz_retrato as RT
import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos
import mundos_b as mb
import mundos_c as mc

E2 = "nueva_espana"
MP = KM.MAPA
RUTA = mb.RutaPlata()
ALTO, MEDIO, BAJO = mc.AltoPoder(), mc.CiudadCriolla(), mc.PuebloTrabajo()

# ------------------------------------------------------------------ anclas
t_mex1, t_no, t_mex2, t_nueva, t_pert, t_rey = T(E2, "mexico", frase=0), T(E2, "no", frase=0), T(E2, "mexico", frase=0, n=1), T(E2, "nueva", frase=0), T(E2, "pertenecia", frase=0), T(E2, "rey", frase=0)
t_minas, t_plata, t_riq1, t_coro, t_riq2, t_nunca, t_aqui = T(E2, "minas", frase=1), T(E2, "plata", frase=1), T(E2, "riqueza", frase=1), T(E2, "corona", frase=1), T(E2, "riqueza", frase=1, n=1), T(E2, "nunca", frase=1), T(E2, "aqui", frase=1)
t_alto, t_pen, t_nac, t_ocup, t_cargos = T(E2, "alto", frase=2), T(E2, "peninsulares", frase=2), T(E2, "nacidos", frase=2), T(E2, "ocupaban", frase=2), T(E2, "cargos", frase=2)
t_deb, t_crio, t_hijos, t_amer, t_din, t_sinp = T(E2, "debajo", frase=3), T(E2, "criollos", frase=3), T(E2, "hijos", frase=3), T(E2, "america", frase=3), T(E2, "dinero", frase=3), T(E2, "poder", frase=3)
t_abajo, t_ind, t_mest, t_escl, t_trab, t_tier, t_minas2 = T(E2, "abajo", frase=4), T(E2, "indigenas", frase=4), T(E2, "mestizos", frase=4), T(E2, "esclavos", frase=4), T(E2, "trabajaban", frase=4), T(E2, "tierra", frase=4), T(E2, "minas", frase=4)
t_preg, t_mand, t_propia, t_crio5 = T(E2, "preguntarse", frase=5), T(E2, "mandaban", frase=5), T(E2, "propia", frase=5), T(E2, "criollos", frase=5)
t_1804, t_rey2, t_exigio, t_iglesia, t_golpe, t_deudas, t_guerras, t_europa = T(E2, "cuatro", frase=6), T(E2, "rey", frase=6), T(E2, "exigio", frase=6), T(E2, "iglesia", frase=6), T(E2, "golpe", frase=6), T(E2, "deudas", frase=6), T(E2, "guerras", frase=6), T(E2, "europa", frase=6)
t_miles, t_fam, t_ruina, t_desc, t_semb = T(E2, "miles", frase=7), T(E2, "familias", frase=7), T(E2, "ruina", frase=7), T(E2, "descontento", frase=7), T(E2, "sembrado", frase=7)
T_PLATA, T_ALTO, T_PREG, T_DEUDAS, T_RUINA = t_minas - 0.3, t_alto - 0.4, t_crio5 - 0.25, t_1804 - 0.5, t_miles - 0.4
RUTA_ATL = [(-96.13, 19.18), (-91.0, 22.4), (-85.2, 24.6), (-79.5, 25.6), (-70.0, 29.0), (-50.0, 32.5), (-30.0, 35.0), (-12.0, 36.3), (-6.3, 36.5)]
GRAD = lambda img, t: U.gradacion(img)


def cielo(lz, t, base=(160, 190, 230), n=9, y0=620, y1=1100, seed=1, escala=1.0):
    """Nubes redondas con base sombreada que pasan lentamente por debajo de la isla (dan altura y movimiento)."""
    for i in range(n):
        x = (h01(seed, i, 1) * 2600 - 360 + t * (7 + 6 * h01(seed, i, 2))) % 2600 - 360
        y = y0 + (y1 - y0) * h01(seed, i, 3)
        r = (70 + 70 * h01(seed, i, 5)) * escala
        for (dx, dy, rr, c) in ((0, r * 0.2, 1.0, P.oscurecer(base, 0.12)), (-r * 0.7, r * 0.08, 0.7, P.oscurecer(base, 0.12)), (r * 0.7, r * 0.12, 0.74, P.oscurecer(base, 0.12)),
                                (0, 0, 0.95, (252, 252, 255)), (-r * 0.65, -r * 0.05, 0.66, (252, 252, 255)), (r * 0.65, 0, 0.7, (252, 252, 255)), (-r * 0.15, -r * 0.3, 0.55, (255, 255, 255))):
            lz.relleno(circulo(x + dx, y + dy, r * rr, 18), c, capa=0)


# ------------------------------------------------------------------------------------------------ 1. EL TERRITORIO Y EL REY
def cam_n1(t):
    return Klog(t, [(T0(E2), (-102.0, 23.0, 0.68)), (t_pert - 0.6, (-101.0, 23.0, 0.70)), (t_rey + 0.4, (-52.0, 29.5, 0.20)), (T_PLATA, (-50.0, 29.5, 0.20))])


VILLAS = (("mexico", "ciudad"), ("puebla", "ciudad"), ("guadalajara", "ciudad"), ("oaxaca", "ciudad"), ("zacatecas", "pueblo"), ("guanajuato", "pueblo"), ("veracruz", "puerto"), ("san_luis", "pueblo"),
          ("valladolid", "pueblo"), ("acapulco", "puerto"), ("chihuahua", "pueblo"), ("tampico", "puerto"))


@shot(T0(E2), bg=lambda t: MP.base(cam_n1(t), t), post=[GRAD], ent=("tinta", 0.7))
def n_mapa(lz, t):
    cam = cam_n1(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=3)
    MD.montes(lz, cam)
    a = smooth(prog(t, t_nueva - 0.1, t_nueva + 0.6))
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.30 * a, borde=(255, 220, 90) if a > 0.02 else None, ancho=5.0, t=t, latido=1.0)
    for k, (lug, tp) in enumerate(VILLAS):
        MD.ciudad(lz, cam, lug, t, t_nueva + 0.25 + 0.12 * k, tam=1.25 if cam[2] > 0.5 else 0.9, tipo=tp, bando="real", semilla=k + 3)
    if t_rey - 0.2 < t:
        MD.pais(lz, cam, "Spain", (255, 210, 70), alfa=0.42 * smooth(prog(t, t_rey, t_rey + 0.5)), borde=(255, 236, 130), ancho=3.0)
    x, y = MP.proy(cam, -104.4, 26.4)
    k1 = U.pop(t, t_mex1) * U.salida(t, t_nueva - 0.1, 0.18)
    if k1 > 0.01:
        U.llamada(lz, float(x), float(y), "México", color=U.COL["morado"], px=52, k=k1, cola="abajo")
        d = smooth(prog(t, t_no, t_mex2 + 0.1))
        if d > 0.01:
            lz.relleno(rect_red(float(x) - 110 * k1, float(y) - 82 * k1, 220 * k1 * d, 8 * k1, 3), (240, 60, 70), capa=2)
    k2 = U.pop(t, t_nueva) * U.salida(t, t_pert + 0.5, 0.35)
    if k2 > 0.01:
        U.llamada(lz, float(x), float(y), "NUEVA ESPAÑA", color=U.COL["naranja"], px=70, k=k2 * U.repop(t, t_nueva + 0.4), cola="abajo")
        for i in range(6):
            U.chispa4(lz, float(x) - 200 + 80 * i, float(y) - 130 - 20 * (i % 2), 10 + 5 * (i % 3), alfa=0.8 * k2 * (0.6 + 0.4 * math.sin(t * 6 + i)))
    # barcos que van y vienen por los dos mares
    for j, (ll, sc) in enumerate(((-94.0, 24.0), (-87.0, 21.0), (-110.5, 21.5), (-106.0, 17.0))):
        bx, by = MP.proy(cam, ll + 0.6 * math.sin(t * 0.3 + j), sc + 0.3 * math.cos(t * 0.25 + j))
        MD.barco_plano(lz, float(bx), float(by), 0.7 * (cam[2] / 0.2) ** 0.1, t, dir=1 if j % 2 else -1, alfa=smooth(prog(t, t_nueva, t_nueva + 0.6)) * (1 - smooth(prog(t, t_pert + 0.2, t_pert + 1.0))))
    f = e_inout(prog(t, t_pert - 0.2, t_rey + 1.1))
    if f > 0.003:
        cab = MD.ruta(lz, cam, RUTA_ATL, color=(255, 236, 160), frac=f, t=t, ancho=5.0, flecha=False)
        if cab is not None:
            MD.barco_plano(lz, cab[0], cab[1] - 6, 1.0 * (cam[2] / 0.2) ** 0.15, t, dir=-1 if f > 0.2 else 1)
    kk = U.pop(t, t_rey + 0.2)
    if kk > 0.01:
        sx, sy = MP.proy(cam, -3.6, 40.4)
        MD.corona(lz, float(sx), float(sy) - 30, 1.5 * kk, t=t)
        U.llamada(lz, float(sx), float(sy) + 6, "ESPAÑA", color=U.COL["rojo"], px=38, k=kk, cola="arriba")
    for txt, ll, rot in (("OCÉANO ATLÁNTICO", (-45.0, 26.0), 0.0), ("GOLFO DE MÉXICO", (-91.5, 24.8), 0.0), ("OCÉANO PACÍFICO", (-112.0, 15.5), 0.0)):
        MD.region(lz, cam, txt, ll, px=34, rot=rot, alfa=0.45, z_max=0.75)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. LA RUTA DE LA PLATA
def cam_n2(t):
    return K(t, [(T_PLATA, (60, -10, 50, 2.35)), (t_plata, (100, 40, 40, 2.55)), (t_riq1 - 0.2, (200, 120, 30, 2.1)), (t_coro, (340, 190, 30, 1.9)), (t_riq2 - 0.1, (620, 330, 30, 2.3)),
                 (t_nunca - 0.2, (700, 440, 24, 2.55)), (t_aqui + 0.3, (740, 440, 10, 1.7)), (T_ALTO, (780, 480, 0, 1.2))])


def _barco_pos(t):
    u = e_in(prog(t, t_nunca - 0.9, T_ALTO + 0.3))
    return lerp(650, 850, u), lerp(510, 585, u)


def _dib_barco(lz, iso, x, y, t, s=1.0, dir=1):
    mm = I.Mundo()
    B.barco(mm, x, y, t_fn=lambda: t, s=s, dir=dir)
    mm.dibujar(lz, iso)


@shot(T_PLATA, bg=lambda t: bg_grad((60, 130, 210), (190, 230, 250)), post=[GRAD], ent=("fundido", 0.6))
def n_plata(lz, t):
    cx, cy, cz, zm = cam_n2(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz()
    cielo(lz, t)
    RUTA.suelo(lz, iso, t, isla=True)
    m = RUTA.objetos(t)
    bx, by = _barco_pos(t)
    m.add(bx - 32, by - 32, bx + 32, by + 32, 90, lambda lz, iso: _dib_barco(lz, iso, bx, by, t, s=1.35), fijo=False, clave=bx + by)
    m.add(768, 528, 832, 592, 90, lambda lz, iso: _dib_barco(lz, iso, 800, 560, t, s=1.1, dir=-1), fijo=False, clave=1360)
    m.add(60, 20, 90, 40, 30, lambda lz, iso: O2.pila_lingotes(lz, iso, 80, 30, n=9, s=0.9, t=t), fijo=False, clave=130)
    m.add(702, 312, 722, 328, 30, lambda lz, iso: O2.pila_lingotes(lz, iso, 712, 318, n=6, s=0.9, t=t), fijo=False)
    for k in range(7):
        tk = t_plata + 0.5 + 0.38 * k
        u = prog(t, tk, tk + 2.8)
        if 0 < u < 1:
            x = lerp(80, 712, e_inout(u))
            y = lerp(30, 318, e_inout(u))
            z = 20 + 70 * math.sin(math.pi * u)
            m.add(x - 4, y - 4, x + 4, y + 4, 40, lambda lz, iso, x=x, y=y, z=z: O2.lingote(lz, iso, x, y, z, 1.1, brillo=1.0), fijo=False, clave=x + y + 60)
    m.dibujar(lz, iso)
    DC.mariposas(lz, iso, 220, 100, 520, 260, n=6, t=t, seed=3)
    DC.aves(lz, t, n=8, seed=5, y0=80, y1=360)
    DC.polvo_luz(lz, t, n=18, seed=2)
    qx, qy = iso.P(88, 0, 90)
    k = U.pop(t, t_minas + 0.1) * U.salida(t, t_riq1 + 0.3)
    if k > 0.01:
        U.llamada(lz, float(qx), float(qy), "Minas de plata", color=U.COL["morado"], px=44, k=k, cola="abajo")
    px_, py_ = iso.P(340, 190, 40)
    k = U.pop(t, t_coro - 0.1) * U.salida(t, t_riq2 + 0.2)
    if k > 0.01:
        U.llamada(lz, float(px_), float(py_) - 30, "Hacia la Corona", color=U.COL["naranja"], px=44, k=k, cola="abajo")
    k = U.pop(t, t_riq2)
    if k > 0.01:
        qx, qy = iso.P(690, 340, 70)
        U.llamada(lz, float(qx), float(qy) - 40, "Puerto de Veracruz", color=U.COL["azul"], px=38, k=k * U.salida(t, t_nunca + 0.3), cola="abajo")


# ------------------------------------------------------------------------------------------------ 3. LA PIRÁMIDE SOCIAL (tres islas)
Z_ALTO, Z_MEDIO, Z_BAJO = 900.0, 450.0, 0.0
OFF = 210.0                                # centro de cada isla (N/2)


def cam_pir(t):
    return K(t, [(T_ALTO, (OFF, OFF + 60, Z_ALTO - 60, 1.9)), (t_pen + 1.4, (OFF + 40, OFF + 20, Z_ALTO, 2.15)), (t_cargos + 0.6, (OFF - 10, OFF + 40, Z_ALTO - 5, 2.3)),
                 (t_deb - 0.05, (OFF, OFF, Z_ALTO - 20, 2.0)), (t_deb + 0.75, (OFF, OFF + 10, Z_MEDIO + 30, 2.1)), (t_hijos, (OFF - 60, OFF - 20, Z_MEDIO, 2.3)), (t_sinp + 0.4, (OFF + 40, OFF + 30, Z_MEDIO, 2.4)),
                 (t_abajo - 0.1, (OFF, OFF, Z_MEDIO - 20, 2.0)), (t_abajo + 0.7, (OFF, OFF + 10, Z_BAJO + 30, 2.1)), (t_mest, (OFF + 70, OFF - 80, Z_BAJO, 2.3)), (t_trab + 0.2, (OFF - 40, OFF + 50, Z_BAJO, 2.3)),
                 (t_minas2 + 0.9, (OFF, OFF, Z_BAJO + 330, 0.80)), (T_PREG, (OFF, OFF, Z_BAJO + 450, 0.72))])


def _con_z(iso, z):
    return I.Iso(iso.cx, iso.cy, iso.cz - z, iso.z, iso.sx0, iso.sy0)


def _visible(iso, z_isla):
    """¿La isla (a la altura z_isla) toca la pantalla? Aproximación por su caja mundial."""
    return _con_z(iso, z_isla).visible(0, 0, mc.N, mc.N, 60, margen=300)


@shot(T_ALTO, bg=lambda t: bg_grad((54, 30, 120), (170, 74, 140), mid=(100, 44, 140), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def n_piramide(lz, t):
    cx, cy, cz, zm = cam_pir(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz()
    U.bokeh(lz, t, seed=8, n=14, colores=((255, 190, 90), (255, 90, 160), (140, 100, 255)), r=(50, 150), alfa=0.22)
    U.chispas(lz, t, n=26, seed=9, tam=(5, 11))
    for nombre, z, mundo in (("bajo", Z_BAJO, BAJO), ("medio", Z_MEDIO, MEDIO), ("alto", Z_ALTO, ALTO)):
        if not _visible(iso, z):
            continue
        iz = _con_z(iso, z)
        mundo.suelo(lz, iz, t)
        mundo.objetos(t).dibujar(lz, iz)
    ialto = _con_z(iso, Z_ALTO)
    for j, (dx, tip) in enumerate(((-90, "llave"), (-30, "pergamino"), (30, "baston"), (90, "sello"))):
        kj = U.pop(t, t_ocup + 0.14 * j + 0.2) * U.salida(t, t_deb - 0.1)
        if kj > 0.01:
            qx, qy = ialto.P(OFF + dx * 0.5, OFF + 80, 120)
            _icono(lz, float(qx) + dx * 0.5, float(qy) - 14 * math.sin(t * 2 + j) * kj, 1.5 * kj, tip)
    imedio = _con_z(iso, Z_MEDIO)
    ibajo = _con_z(iso, Z_BAJO)

    def etq(txt, t0, t1, ref, ox=0, oy=0, col=U.COL["morado"], px=42, cola="abajo"):
        k = U.pop(t, t0) * U.salida(t, t1)
        if k > 0.01:
            U.llamada(lz, float(ref[0]) + ox, float(ref[1]) + oy, txt, color=col, px=px, k=k, cola=cola)
    etq("Peninsulares", t_pen - 0.1, t_nac + 0.05, ialto.P(OFF, OFF + 60, 80), 0, -90, U.COL["rojo"], 56)
    etq("nacidos en España", t_nac, t_ocup + 1.0, ialto.P(OFF, OFF + 60, 0), 0, 30, U.COL["morado"], 40, "arriba")
    etq("Criollos", t_crio - 0.1, t_amer - 0.2, imedio.P(OFF, OFF + 10, 80), 0, -90, U.COL["morado"], 56)
    etq("nacidos en América", t_amer - 0.2, t_din - 0.15, imedio.P(OFF, OFF + 10, 0), 0, 30, U.COL["azul"], 40, "arriba")
    kd = U.pop(t, t_din) * U.salida(t, t_abajo - 0.5)
    if kd > 0.01:
        qx, qy = imedio.P(OFF - 90, OFF - 20, 50)
        U.llamada(lz, float(qx), float(qy), "con dinero", color=U.COL["verde"], px=40, k=kd, cola="abajo")
    ks = U.pop(t, t_sinp - 0.1) * U.salida(t, t_abajo - 0.5)
    if ks > 0.01:
        qx, qy = imedio.P(OFF + 70, OFF + 20, 70)
        _icono(lz, float(qx), float(qy), 2.0 * ks, "llave")
        lz.relleno(np.array([[qx - 52 * ks, qy - 46 * ks], [qx - 38 * ks, qy - 56 * ks], [qx + 52 * ks, qy + 46 * ks], [qx + 38 * ks, qy + 56 * ks]]), (230, 56, 70), capa=2)
        lz.relleno(np.array([[qx + 52 * ks, qy - 46 * ks], [qx + 38 * ks, qy - 56 * ks], [qx - 52 * ks, qy + 46 * ks], [qx - 38 * ks, qy + 56 * ks]]), (230, 56, 70), capa=2)
        U.llamada(lz, float(qx), float(qy) - 74 * ks, "sin poder", color=U.COL["rojo"], px=40, k=ks, cola="abajo")
    for i, (txt, t0, col, ref) in enumerate((("Indígenas", t_ind, U.COL["teal"], (110, 275, 40)), ("Mestizos", t_mest, U.COL["naranja"], (140, 70, 40)), ("Esclavos", t_escl, U.COL["magenta"], (330, 100, 60)))):
        k = U.pop(t, t0 - 0.1) * U.salida(t, t_minas2 + 0.9)
        if k > 0.01:
            qx, qy = ibajo.P(*ref)
            U.llamada(lz, float(qx), float(qy) - 20, txt, color=col, px=46, k=k, cola="abajo")
    # plano final de la pirámide completa: columna de luz y estrellas grandes detrás
    kf = prog(t, t_minas2 + 0.7, T_PREG)
    if kf > 0.01:
        cxp, cyp = ibajo.P(OFF, OFF, 300)
        lz.halo(float(cxp), float(cyp), 700, (255, 190, 240), alfa=0.22 * kf, capa=0)
        for j in range(5):
            U.chispa4(lz, float(cxp) + 520 * math.cos(j * 1.26 + t * 0.2), float(cyp) + 360 * math.sin(j * 1.26 + t * 0.2), 16 + 8 * (j % 3), alfa=0.8 * kf * (0.6 + 0.4 * math.sin(t * 3 + j)))


def _icono(lz, x, y, s, tip):
    with lz.capa(2):
        lz.halo(x, y, 40 * s, (255, 236, 150), alfa=0.35)
        if tip == "llave":
            lz.relleno(circulo(x - 9 * s, y - 6 * s, 8 * s, 14), (250, 206, 70))
            lz.relleno(circulo(x - 9 * s, y - 6 * s, 4 * s, 10), (150, 100, 40))
            lz.relleno(rect_red(x - 2 * s, y - 8 * s, 22 * s, 4.4 * s, 1.4 * s), (250, 206, 70))
            lz.relleno(rect_red(x + 12 * s, y - 8 * s, 3.4 * s, 10 * s, 1.0 * s), (250, 206, 70))
            lz.relleno(rect_red(x + 18 * s, y - 8 * s, 3.4 * s, 7 * s, 1.0 * s), (250, 206, 70))
        elif tip == "pergamino":
            lz.relleno(rect_red(x - 12 * s, y - 14 * s, 24 * s, 28 * s, 3 * s), (252, 240, 210))
            for i in range(4):
                lz.relleno(rect_red(x - 8 * s, y - 8 * s + i * 5.4 * s, 16 * s * (0.7 + 0.3 * h01(i, 4)), 1.8 * s, 0.6 * s), (150, 120, 100))
            lz.relleno(circulo(x + 8 * s, y + 10 * s, 4 * s, 8), (214, 60, 60))
        elif tip == "baston":
            lz.relleno(rect_red(x - 2.4 * s, y - 18 * s, 4.8 * s, 36 * s, 2 * s), (130, 90, 66))
            lz.relleno(circulo(x, y - 20 * s, 6 * s, 12), (250, 206, 70))
            lz.relleno(circulo(x, y - 20 * s, 3 * s, 8), (214, 56, 70))
        else:
            lz.relleno(circulo(x, y, 13 * s, 18), (214, 56, 70))
            lz.relleno(circulo(x, y, 9 * s, 18), (240, 90, 100))
            lz.relleno(elipse(x, y - 1 * s, 4 * s, 6 * s, 0, 10), (250, 230, 160))


# ------------------------------------------------------------------------------------------------ 4. UN CRIOLLO SE PREGUNTA
@shot(T_PREG, bg=lambda t: bg_grad((50, 28, 112), (150, 64, 130), mid=(96, 40, 130), ym=0.5), post=[GRAD], ent=("corte", 0.01))
def n_pregunta(lz, t):
    U.bokeh(lz, t, seed=6, n=18, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.28)
    U.haces_luz(lz, 560, 520, t, n=8, largo=1300, color=(255, 190, 240), alfa=0.12, ancho=0.09)
    U.chispas(lz, t, n=24, seed=12, tam=(5, 12))
    k = U.pop(t, T_PREG + 0.05, 1.3)
    emo = "pensativo" if t < t_mand else "serio"
    RT.retrato(lz, 520, 960, 205 * (0.9 + 0.1 * k), "criollo", t, emocion=emo, habla=0.0, mirar=-0.5 + 0.8 * prog(t, t_preg, t_propia), seed=3)
    for i in range(5):
        u = prog(t, t_preg + 0.12 * i, t_preg + 0.12 * i + 0.4)
        if u > 0.01:
            x = 200 + 190 * (i % 3) + 24 * math.sin(t * 1.4 + i)
            y = 130 + 140 * (i // 3) + 14 * math.sin(t * 1.9 + i * 2)
            U.llamada(lz, x, y, "¿?", color=U.COL["magenta"] if i % 2 else U.COL["morado"], px=64 + 16 * (i % 2), k=U.pop(t, t_preg + 0.12 * i), cola="izq")
    iso = I.Iso(210, 250, 10, 1.55 + 0.04 * (t - T_PREG), sx0=1340, sy0=560)
    I.luz()
    I.isla(lz, iso, 0, 0, 420, 420, color_top=(150, 190, 100), t=t, seed=20, esp=34, sombra=True)
    I.suelo_curvo(lz, iso, [(20, 20), (400, 20), (400, 400), (20, 400)], (236, 220, 176))
    I.suelo_rect(lz, iso, 90, 130, 240, 200, (246, 230, 196))
    I.cuadricula(lz, iso, 90, 130, 330, 330, 20, color=(255, 255, 255), alfa=0.2)
    DC.hierba(lz, iso, 0, 0, 420, 420, n=110, seed=7, t=t)
    m = I.Mundo()
    B.palacio(m, 60, 20, w=300, d=60, h=72, campana=True)
    DC.bosque(m, 4, 4, 416, 416, n=18, seed=19, evitar=((50, 10, 370, 90), (80, 120, 340, 340)), t_fn=lambda: t, tipos=("arbol", "cipres", "arbusto"))
    mu = G.Multitud()
    for i, (x, y) in enumerate(((120, 240), (150, 262), (186, 246), (222, 266), (258, 244), (294, 262), (160, 300), (230, 306))):
        mu.quieto((x, y), "regidor", dir=(0, -1), seed=800 + i, piel=G.PIELES[i % 2], h=36, accion="habla" if i in (2, 5) else None)
    mu.ronda((210, 240), 60, "dama", n=2, seed=820)
    mu.dibujar(m, t)
    for i, (x, y) in enumerate(((150, 90), (180, 92), (210, 90), (240, 92), (270, 90))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y + 12, t, "peninsular", dir=(0, 1), seed=830 + i, piel=G.PIELES[0], h=36, z=36, accion="habla" if i == 2 else None)))(x, y, i), fijo=False, clave=x + y + 90)
    m.dibujar(lz, iso)


# ------------------------------------------------------------------------------------------------ 5. 1804: EL DECRETO
HAC = mb.Hacienda()
T_DINERO = t_golpe - 0.5


def cam_deudas(t):
    return K(t, [(T_DEUDAS, (10, 150, 40, 2.9)), (t_rey2, (50, 170, 40, 3.2)), (t_exigio, (95, 175, 40, 3.5)), (t_iglesia, (115, 170, 40, 3.5)), (T_DINERO, (125, 150, 40, 3.2))])


def _signo(lz, x, y, k, txt="!"):
    if k > 0.01:
        U.llamada(lz, x, y, txt, color=U.COL["rojo"], px=52, k=k, cola="abajo")


@shot(T_DEUDAS, bg=lambda t: bg_grad((90, 150, 220), (230, 240, 252)), post=[GRAD], ent=("fundido", 0.6))
def n_decreto(lz, t):
    cx, cy, cz, zm = cam_deudas(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz()
    cielo(lz, t, base=(170, 200, 236), y0=760, y1=1100, seed=3, escala=1.2)
    HAC.suelo(lz, iso, t)
    m = HAC.objetos(t)
    fx = lerp(-60, 98, e_inout(prog(t, T_DEUDAS + 0.2, t_exigio - 0.2)))
    llega = t > t_exigio - 0.2
    m.add(fx - 5, 176, fx + 5, 184, 40, lambda lz, iso: G.persona(lz, iso, fx, 180, t, "peninsular", dir=(1, 0), vel=0.0 if llega else 1.0, seed=900, piel=G.PIELES[0], h=46, accion=("habla" if llega else None)), fijo=False)
    m.add(125, 172, 135, 182, 40, lambda lz, iso: G.persona(lz, iso, 118, 178, t, "noble", dir=(-1, 0), seed=901, piel=G.PIELES[1], h=46, accion=("habla" if t > t_iglesia else None)), fijo=False)
    m.add(148, 172, 158, 182, 40, lambda lz, iso: G.persona(lz, iso, 140, 184, t, "cura", dir=(-1, 0.2), seed=902, h=46), fijo=False)
    for i, (x, y, tipo) in enumerate(((60, 214, "campesino"), (82, 226, "campesina"), (170, 222, "mestizo"), (192, 210, "indigena"))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tipo, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipo, dir=(0.4, -1), seed=960 + i, h=40, accion="habla" if i == 1 else None)))(x, y, tipo, i), fijo=False)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=8, y0=100, y1=330)
    DC.polvo_luz(lz, t, n=16, seed=4)
    kp = U.salida(t, T_DINERO - 0.1, 0.3)
    if kp > 0.01:
        U.pergamino_grande(lz, 520, 330, 640, 380, t, t_exigio - 0.2, titulo="REAL CÉDULA · 1804", lineas=("Consolidación de Vales Reales", "Pagar las deudas de inmediato"), alfa=kp)
    k = U.pop(t, t_1804 - 0.5) * U.salida(t, t_exigio + 0.2)
    if k > 0.01:
        P.rotulo(lz, W / 2, 540, "1804", px=230, k=k, color=(255, 214, 72))
    qx, qy = iso.P(140, 184, 70)
    k = U.pop(t, t_iglesia) * U.salida(t, T_DINERO)
    if k > 0.01:
        U.llamada(lz, float(qx) + 70, float(qy) - 60, "La Iglesia", color=U.COL["morado"], px=46, k=k, cola="izq")
        _signo(lz, float(qx) + 20, float(qy) - 150, U.pop(t, t_iglesia + 0.3) * U.salida(t, T_DINERO))
    qx, qy = iso.P(118, 178, 70)
    k = U.pop(t, t_iglesia + 0.5) * U.salida(t, T_DINERO)
    if k > 0.01:
        U.llamada(lz, float(qx) - 70, float(qy) - 60, "Propietarios", color=U.COL["naranja"], px=46, k=k, cola="der")
        _signo(lz, float(qx) - 20, float(qy) - 150, U.pop(t, t_iglesia + 0.6) * U.salida(t, T_DINERO))


# ------------------------------------------------------------------------------------------------ 5b. EL DINERO CRUZA EL ATLÁNTICO
RUTA_DINERO = [(-96.13, 19.18), (-85.2, 24.6), (-70.0, 29.0), (-45.0, 33.0), (-20.0, 35.8), (-6.3, 36.5)]


def cam_dinero(t):
    return Klog(t, [(T_DINERO, (-96.13, 19.18, 2.6)), (t_golpe + 0.4, (-86.0, 23.0, 1.1)), (t_deudas, (-52.0, 30.0, 0.22)), (t_guerras - 0.6, (-8.0, 38.0, 0.75)), (t_guerras + 0.4, (2.0, 46.0, 0.52)), (T_RUINA, (2.0, 46.0, 0.50))])


@shot(T_DINERO, bg=lambda t: MP.base(cam_dinero(t), t), post=[GRAD], ent=("fundido", 0.5))
def n_dinero(lz, t):
    cam = cam_dinero(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=5)
    MD.montes(lz, cam)
    for nombre, col in (("Mexico", (255, 96, 70)), ("Spain", (255, 210, 70)), ("France", (80, 130, 230)), ("Portugal", (90, 190, 120)), ("United Kingdom", (230, 90, 120)), ("Italy", (150, 130, 230)), ("Germany", (240, 160, 70))):
        MD.pais(lz, cam, nombre, col, alfa=0.30 if nombre != "Mexico" else 0.26, borde=(255, 236, 160) if nombre in ("Mexico", "Spain") else None, ancho=3.0)
    f = e_inout(prog(t, t_golpe + 0.2, t_guerras - 0.8))
    MD.ciudad(lz, cam, "veracruz", t, T_DINERO, tam=2.2 if cam[2] > 1 else 1.4, tipo="puerto", bando="real", nombre="Veracruz" if cam[2] > 1.2 else None, px=30)
    cab = MD.ruta(lz, cam, RUTA_DINERO, color=(255, 236, 160), frac=f, t=t, ancho=5.0, flecha=False)
    if cab is not None:
        MD.barco_plano(lz, cab[0], cab[1] - 8, 1.1 * (cam[2] / 0.3) ** 0.15, t, dir=-1)
        for j in range(5):
            ph = (t * 0.8 + j * 0.2) % 1.0
            sx = cab[0] - 30 - 90 * ph
            lz.relleno(circulo(sx, cab[1] + 10 - 6 * ph, 4 * (1 - ph) + 1, 8), (250, 206, 70), alfa=0.8 * (1 - ph), capa=2)
    for j, (lug, tipo, col) in enumerate((("madrid", "ciudad", (255, 206, 70)), ("cadiz", "puerto", (255, 206, 70)), ("lisboa", "puerto", (90, 190, 120)), ("paris", "ciudad", (80, 130, 230)),
                                          ("londres", "ciudad", (230, 90, 120)), ("roma", "ciudad", (150, 130, 230)), ("berlin", "ciudad", (240, 160, 70)))):
        MD.ciudad(lz, cam, lug, t, t_guerras - 0.9 + 0.1 * j, tam=1.5 if cam[2] > 0.6 else 1.1, tipo=tipo, bando=col, semilla=j + 40)
    kk = U.pop(t, t_guerras - 0.6)
    if kk > 0.01:
        sx, sy = MP.proy(cam, -3.7, 40.4)
        MD.corona(lz, float(sx), float(sy) - 80, 1.5 * kk, t=t)
    for j, (lug, tt) in enumerate((((2.3, 48.8), t_guerras), ((-0.1, 51.5), t_guerras + 0.25), ((12.5, 41.9), t_guerras + 0.5), ((-9.1, 38.7), t_guerras + 0.75), ((8.7, 50.1), t_guerras + 1.0))):
        MD.insignia_batalla(lz, cam, lug, t, tt, año=None, s=1.2)
        sx, sy = MP.proy(cam, lug[0], lug[1])
        for i in range(4):
            u = ((t - tt) * 0.8 + i * 0.25) % 1.0
            if t > tt:
                lz.relleno(circulo(float(sx) + 10 * math.sin(i * 2 + t), float(sy) - 30 - 70 * u, 8 + 18 * u, 12), (236, 232, 240), alfa=0.5 * (1 - u), capa=2)
    kk = U.pop(t, t_guerras - 0.3)
    if kk > 0.01 and cam[2] < 1.0:
        sx, sy = MP.proy(cam, 3.0, 47.2)
        U.llamada(lz, float(sx), float(sy), "Guerras en Europa", color=U.COL["rojo"], px=52, k=kk * U.repop(t, t_guerras + 0.6), cola=None)
    kk = U.pop(t, t_deudas - 0.2) * U.salida(t, t_guerras - 0.6)
    if kk > 0.01 and cab is not None:
        U.llamada(lz, cab[0], cab[1] - 60, "dinero para la Corona", color=U.COL["naranja"], px=44, k=kk, cola="abajo")
    MD.region(lz, cam, "OCÉANO ATLÁNTICO", (-40.0, 25.0), px=34, alfa=0.45, z_max=0.7)
    MD.brujula(lz, W - 110, H - 120, 1.0)


def _bolsa(lz, iso, x, y, z, i):
    sx, sy = iso.P(x, y, z)
    k = iso.z
    lz.relleno(np.array([(-7, 0), (-8, -9), (-5, -14), (-2, -16), (2, -16), (5, -14), (8, -9), (7, 0)], float) * k + [sx, sy], tint((236, 214, 150)))
    lz.relleno(np.array([(-7, 0), (-8, -9), (-5, -14), (-2, -16), (0, -15), (0, 0)], float) * k + [sx, sy], tint((250, 232, 176)))
    lz.relleno(rect_red(sx - 3 * k, sy - 17 * k, 6 * k, 2.4 * k, 0.8 * k), tint((140, 100, 70)))
    lz.texto("$", sx, sy - 8 * k, int(9 * k), "geo", color=(150, 110, 40), borde=None, temblor=0.0, capa=2)


# ------------------------------------------------------------------------------------------------ 6. LA RUINA Y EL DESCONTENTO
RUINA = mb.PuebloRuina()


def cam_ruina(t):
    return K(t, [(T_RUINA, (-20, 140, 30, 3.0)), (t_fam, (60, 150, 30, 3.3)), (t_ruina, (170, 150, 30, 3.1)), (t_desc - 0.5, (230, 170, 20, 2.7)), (t_desc + 0.7, (180, 250, 0, 2.7)), (T1(E2) - 0.2, (185, 255, 0, 2.2))])


@shot(T_RUINA, bg=lambda t: bg_grad((60, 52, 100), (130, 110, 150)), post=[lambda img, t: U.gradacion(img, luces=(1.0, 0.98, 1.0), sombras=(0.94, 0.95, 1.06), saturacion=0.95)], ent=("fundido", 0.6))
def n_ruina(lz, t):
    cx, cy, cz, zm = cam_ruina(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.86, 0.88, 0.96), mix=(70, 70, 130), k=0.18)
    cielo(lz, t, base=(90, 80, 130), y0=760, y1=1100, seed=6, escala=1.3)
    RUINA.suelo(lz, iso, t)
    m = RUINA.objetos(t)
    for i, (x, y) in enumerate(((44, 52), (114, 54), (190, 54), (270, 54), (52, 150), (130, 150), (210, 154), (292, 148))):
        k = U.pop(t, t_miles + 0.15 * i)
        if k > 0.01:
            m.add(x - 4, y + 4, x + 4, y + 12, 40, (lambda x, y, k: (lambda lz, iso: O2.cartel(lz, iso, x, y + 8, "SE VENDE", h=26 * k, w=40 * k, px=10, t=t)))(x, y, k), fijo=False, clave=x + y + 8)
    for j, (fase, tipo) in enumerate(((0.0, "campesino"), (0.1, "campesina"), (0.2, "nino"), (0.55, "campesino"), (0.65, "campesina"))):
        px_, py_ = -100 + 560 * ((t * 0.045 + fase) % 1.0), 156 + 5 * j
        m.add(px_ - 4, py_ - 4, px_ + 4, py_ + 4, 36, (lambda px_, py_, j, tipo: (lambda lz, iso: G.persona(lz, iso, px_, py_, t, tipo, dir=(1, 0.05), vel=0.8, seed=950 + j, h=36 if tipo != "nino" else 24)))(px_, py_, j, tipo), fijo=False, clave=px_ + py_)
    cx_ = -100 + 560 * ((t * 0.045 + 0.35) % 1.0)
    m.add(cx_ - 14, 166 - 8, cx_ + 14, 166 + 8, 30, (lambda cx_: (lambda lz, iso: O.carreta(lz, iso, cx_, 166, t, mov=1.0, s=1.2)))(cx_), fijo=False, clave=cx_ + 166)
    for i in range(18):
        x = 62 + 34 * (i % 8)
        y = 214 + 40 * (i // 8)
        u = e_back(prog(t, t_semb - 1.2 + 0.07 * i + 0.05 * (i % 3), t_semb - 0.1 + 0.07 * i)) if t > t_desc - 0.3 else 0.0
        m.add(x - 5, y - 5, x + 5, y + 5, 40, (lambda x, y, u: (lambda lz, iso: O2.brote(lz, iso, x, y, max(0.0, min(1.1, u)), t, enojo=True, s=1.3)))(x, y, u), fijo=False)
    m.dibujar(lz, iso)
    O2.nube_tormenta(lz, 520, 130, 1.6, t, relampago=max(0.0, 1.0 - ((t - t_ruina + 0.3) % 2.4) * 4) if t > t_miles else 0.0)
    O2.nube_tormenta(lz, 1400, 160, 1.8, t + 3, relampago=max(0.0, 1.0 - ((t - t_ruina + 1.4) % 2.9) * 4) if t > t_miles else 0.0)
    O2.lluvia(lz, t, dens=0.9 * (1 - prog(t, t_desc, t_desc + 1.0)), alfa=0.5)
    k = U.pop(t, t_fam) * U.salida(t, t_ruina + 0.7)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "Miles de familias", color=U.COL["rojo"], px=70, k=k, cola=None)
    k = U.pop(t, t_desc) * U.salida(t, T1(E2) - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "El descontento", color=U.COL["magenta"], px=70, k=k * U.repop(t, t_semb), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T0(E2) + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_mex1, "pop", 0.4)
snd(t_no + 0.3, "garabato", 0.3, dur=0.6)
snd(t_nueva, "bling", 0.6)
snd(t_pert, "ola", 0.3, dur=1.4)
snd(t_rey + 0.2, "pluck", 0.5)
snd(T_PLATA, "whoosh", 0.3, dur=0.8)
snd(t_minas, "pop", 0.4)
for _k in range(7):
    snd(t_plata + 0.5 + 0.38 * _k, "monedas", 0.2)
snd(t_coro, "pop", 0.4)
snd(t_nunca, "ola", 0.35, dur=2.0)
snd(T_ALTO, "whoosh", 0.3, dur=0.8)
snd(t_pen, "pop", 0.4)
snd(t_crio, "pop", 0.4)
snd(t_din, "monedas", 0.4)
snd(t_sinp, "gong", 0.3)
snd(t_ind, "pop", 0.35)
snd(t_mest, "pop", 0.35)
snd(t_escl, "pop", 0.35)
snd(t_preg, "pluck", 0.4)
snd(t_1804, "bling", 0.6)
snd(t_exigio, "pop", 0.4)
snd(t_golpe, "monedas", 0.5)
snd(t_guerras, "gong", 0.3)
snd(t_miles, "trueno", 0.35)
snd(t_desc, "pluck", 0.4)
