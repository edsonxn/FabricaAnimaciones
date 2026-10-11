# -*- coding: utf-8 -*-
"""Escena 6 · el hartazgo (3:07-3:49): diez años de tributo y templos derribados, presión de encomenderos y frailes, la olla tapada,
los emisarios de pueblo en pueblo con la promesa, el levantamiento de 1540 (Tlaltenango, Nochistlán, Juchipila), las primeras muertes
(memorial sobrio) y el refugio en el peñol del Mixtón."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_a as MA
import mundos_g as MG
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E6 = "hartazgo"
MP = KM.MAPA
t_diez, t_trib, t_trab, t_amos, t_derr, t_templos = (T(E6, "diez", frase=0), T(E6, "tributos", frase=0), T(E6, "trabajaron", frase=0), T(E6, "amos", frase=0),
                                                     T(E6, "derribaban", frase=0), T(E6, "templos", frase=0))
t_abusos, t_encom, t_presion, t_frailes, t_oblig, t_aband, t_creen = (T(E6, "abusos", frase=1), T(E6, "encomenderos", frase=1), T(E6, "presion", frase=1), T(E6, "frailes", frase=1),
                                                                      T(E6, "obligarlos", frase=1), T(E6, "abandonar", frase=1), T(E6, "creencias", frase=1))
t_tension, t_crecia, t_olla, t_tapada = T(E6, "tension", frase=2), T(E6, "crecia", frase=2), T(E6, "olla", frase=2), T(E6, "tapada", frase=2)
t_mens, t_emis, t_pueblo, t_promesa, t_dioses, t_volver, t_ancianos, t_juventud = (T(E6, "mensajes", frase=3), T(E6, "emisarios", frase=3), T(E6, "pueblo", frase=3), T(E6, "promesa", frase=3),
                                                                                  T(E6, "dioses", frase=3), T(E6, "volverian", frase=3), T(E6, "ancianos", frase=3), T(E6, "juventud", frase=3))
t_hacia, t_cuarenta, t_levant, t_tlal, t_noch, t_juch = (T(E6, "hacia", frase=4), T(E6, "cuarenta", frase=4), T(E6, "levantaron", frase=4), T(E6, "tlaltenango", frase=4),
                                                        T(E6, "nochistlan", frase=4), T(E6, "juchipila", frase=4))
t_mataron, t_encom1, t_sacerd, t_despues, t_refug, t_penol, t_paredes, t_vert, t_mixton = (T(E6, "mataron", frase=5), T(E6, "encomendero", frase=5), T(E6, "sacerdotes", frase=5),
                                                                                          T(E6, "despues", frase=5), T(E6, "refugiaron", frase=5), T(E6, "penol", frase=5),
                                                                                          T(E6, "paredes", frase=5), T(E6, "verticales", frase=5), T(E6, "mixton", frase=5))
T_A, T_B, T_C, T_D1, T_D2, T_E, T_F1, T_F2 = (T0(E6), INI(E6, 1) - 0.15, INI(E6, 2) - 0.15, INI(E6, 3) - 0.15, t_promesa - 0.25, INI(E6, 4) - 0.15, INI(E6, 5) - 0.15, t_despues - 0.2)


# ------------------------------------------------------------------------------------------------ A. diez años de tributo; los templos caen
def _tributo_fila(lz, t, y=905, s=24):
    """Caxcanes que cargan costales hacia el encomendero (cinta continua: entran por la izquierda y dejan su carga en la pila)."""
    v = K2.v_marcha(s)
    largo = 1500.0
    for i in range(7):
        x = -160 + ((t - T_A) * v + i * largo / 7 + 60 * h01(2, i)) % largo
        a = smooth(prog(x, -160, -60)) * (1 - smooth(prog(x, 1180, 1300)))
        if a < 0.02:
            continue
        spec = K2.variar("caxcana" if i % 3 == 1 else "caxcan", 300 + i)
        K2.cuerpo(lz, x, y + 10 * (i % 2), s, spec, t, piernas="camina", brazos="carga", mirar=1, vista="perfil", seed=i + 30, alfa=a, obj_d=MG.costal_mano,
                  emocion="cansado", ph=t * 5.0 + i)


@shot(T_A, bg=lambda t: PA.cielo(0.15), post=[acabado], ent=("tinta", 0.6))
def a_tributo(lz, t):
    cx = 30.0 * (t - T_A)
    PA.sol(lz, 1460, 250, 64, t, 0.15)
    PA.sierras(lz, t, cx, 0.15, y0=600, capas=4, semilla=23)
    p = PA.pal(0.15)
    # templo en el plano medio que se derrumba al decir «derribaban»
    MG.templo_derribado(lz, 470, 720, 38, t, prog(t, t_derr - 0.1, t_templos + 1.3))
    degradado_v(lz, 0, W, 715, H, p["pasto"][0], p["pasto"][1], 715, H)
    # milpa con dos caxcanes que labran (trabajo para los nuevos amos)
    for k in range(9):
        xx = 980 + 60 * k
        for j in range(3):
            lz.relleno(rect_red(xx + 12 * j - 4, 760 - 40 - 10 * (k % 2), 8, 48, 4), (226, 196, 88), capa=1)
            lz.relleno(np.array([(xx + 12 * j, 740), (xx + 12 * j + 16, 726), (xx + 12 * j + 2, 744)]), (90, 160, 90), capa=1)
    for i, x in enumerate((1080, 1330)):
        K2.cuerpo(lz, x, 790, 16, K2.variar("caxcan", 410 + i), t, piernas="idle", brazos="labra", mirar=-1, vista="perfil", seed=i + 50, emocion="cansado")
    PA.aves(lz, t, n=5, seed=9)
    # encomendero junto a su pila de costales
    MG.pila_costales(lz, 1500, 980, 26, int(3 + 12 * smooth(prog(t, T_A, t_amos + 1.0))))
    K2.cuerpo(lz, 1720, 990, 28, "encomendero", t, piernas="idle", brazos="señala" if t > t_trab else "idle", mirar=-1, vista="perfil", seed=4, emocion="serio",
              objetivo=(1300, 820))
    _tributo_fila(lz, t)
    PA.flores_frente(lz, t, cx * 2.0, n=10, amb=0.15, y0=980, seed=11)
    # rótulos
    c = lerp(1530, 1540, e_inout(prog(t, t_diez - 0.2, t_amos)))
    k = U.pop(t, t_diez - 0.2) * U.salida(t, T_B - 0.15)
    if k > 0.01:
        lz.texto(str(int(c)), W / 2, 150, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, W / 2, 255, "diez años", color=U.COL["naranja"], px=44, k=k, cola=None)
    k = U.pop(t, t_trib) * U.salida(t, t_derr - 0.15)
    if k > 0.01:
        U.llamada(lz, 1500, 700, "tributo", color=U.COL["oro"], px=48, k=k, cola="abajo", color_texto=(60, 36, 20))
    k = U.pop(t, t_trab) * U.salida(t, t_derr - 0.15)
    if k > 0.01:
        U.llamada(lz, 1200, 620, "trabajo", color=U.COL["naranja"], px=44, k=k, cola="abajo")
    k = U.pop(t, t_templos)
    if k > 0.01:
        U.llamada(lz, 470, 470, "templos derribados", color=U.COL["rojo"], px=48, k=k, cola="abajo")
    snd(t_trib, "monedas", 0.35)
    snd(t_derr + 0.3, "crujido", 0.5)


# ------------------------------------------------------------------------------------------------ B. abusos de un lado, presión de los frailes del otro
@shot(T_B, bg=lambda t: bg_grad((70, 26, 110), (18, 8, 46), mid=(46, 18, 88), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def b_presion(lz, t):
    U.bokeh(lz, t, seed=33, n=10, colores=((236, 70, 140), (122, 90, 255), (255, 150, 44)), alfa=0.30)
    sq = smooth(prog(t, t_abusos, t_creen + 0.6))                 # cuánto aprietan las dos fuerzas
    # el caxcán en medio, cada vez más agobiado
    K2.busto(lz, W / 2, 860, 140, "caxcan", t, yaw=0.0, bajar=0.35 * sq, emocion="preocupado" if t < t_aband else "triste", ojos="abiertos", seed=12,
             temblor=2.0 * sq, mirar=(-0.4 if t < t_frailes else 0.4, 0.0))
    # encomendero (izquierda) y fraile (derecha)
    ke = pk(t, t_abusos - 0.1, 0.45)
    if ke > 0.01:
        K2.busto(lz, 330 + 60 * sq, 930, 112 * ke, "encomendero", t, yaw=0.5, emocion="enojo", ojos="abiertos", seed=5, habla=0.7 if t_abusos < t < t_presion else 0.0)
        U.llamada(lz, 330, 330, "encomenderos", color=U.COL["rojo"], px=44, k=ke, cola=None)
    kf = pk(t, t_frailes - 0.1, 0.45)
    if kf > 0.01:
        K2.busto(lz, W - 330 - 60 * sq, 930, 112 * kf, "fraile", t, yaw=-0.5, emocion="serio", ojos="abiertos", seed=7, habla=0.7 if t_frailes < t < t_creen else 0.0)
        U.llamada(lz, W - 330, 330, "frailes", color=U.COL["morado"], px=44, k=kf, cola=None)
    # flechas gruesas que empujan hacia el centro (laten)
    for sd, t0, col in ((-1, t_abusos, (222, 60, 70)), (1, t_presion, (150, 110, 200))):
        a = smooth(prog(t, t0, t0 + 0.4))
        if a > 0.01:
            lat = 18 * math.sin(t * 7) * a
            x0 = W / 2 + sd * 640
            x1 = W / 2 + sd * (300 - 60 * sq) - sd * lat
            MA_.flecha_pantalla(lz, x0, 520, x1, 520, color=col, ancho=34, alfa=a)
    # globo de pensamiento: la flor de sus creencias se apaga al decir «abandonar»
    kb = pk(t, t_oblig - 0.2, 0.4)
    if kb > 0.01:
        bx, by = W / 2 + 260, 190
        for r_, dx, dy in ((14, -150, 190), (22, -110, 140)):
            lz.relleno(circulo(bx + dx, by + dy, r_ * kb, 16), (250, 244, 255), alfa=0.95, capa=2)
        lz.relleno(elipse(bx, by, 170 * kb, 120 * kb, 0, 40), (250, 244, 255), alfa=0.95, capa=2)
        marchita = e_inout(prog(t, t_aband, t_creen + 0.5))
        MA.flor_xuchitl(lz, bx, by, 80 * kb, t, u=1.0 - 0.7 * marchita, seed=4, alfa=1.0 - 0.5 * marchita, sombra=False)
        if marchita > 0.05:                                        # tachón rojo
            f = min(1.0, marchita * 2)
            lz.trazo(np.array([(bx - 90, by - 70), (bx - 90 + 180 * f, by - 70 + 140 * f)]), (222, 60, 70), 14.0, afinar=False, temblor=0.0, capa=2)
    k = U.pop(t, t_creen - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2 + 260, 345, "sus antiguas creencias", color=U.COL["magenta"], px=40, k=k, cola=None)
    snd(t_abusos, "whoosh", 0.4)
    snd(t_presion, "whoosh", 0.4)
    snd(t_aband, "bonk", 0.3)


# ------------------------------------------------------------------------------------------------ C. la tensión: una olla tapada
@shot(T_C, bg=lambda t: bg_grad((90, 24, 70), (22, 6, 30), mid=(60, 16, 60), ym=0.55), post=[acabado], ent=("zoom", 0.5))
def c_olla(lz, t):
    U.bokeh(lz, t, seed=41, n=9, colores=((255, 110, 60), (236, 70, 140), (255, 190, 60)), alfa=0.28)
    pres = smooth(prog(t, T_C, T_D1 + 0.1)) * 0.95 + 0.05
    z = lerp(1.0, 1.12, prog(t, T_C, T_D1))                       # la cámara se acerca a la olla
    with lz.grupo(800 * (1 - z), 760 * (1 - z), z):             # acerca la cámara a (800, 760)
        MG.olla(lz, 800, 900, 72, t, pres)
    MG.termometro(lz, 1540, 860, 520, pres, t)
    k = U.pop(t, t_tension - 0.1)
    if k > 0.01:
        U.llamada(lz, 1540, 230, "tensión", color=U.COL["rojo"], px=60, k=k * U.repop(t, t_crecia), cola=None)
    k = U.pop(t, t_olla) * U.salida(t, T_D1 - 0.1)
    if k > 0.01:
        U.llamada(lz, 800, 160, "una olla tapada", color=U.COL["naranja"], px=56, k=k, cola=None)
    snd(t_crecia, "reloj_rapido", 0.35)
    snd(t_tapada, "bonk", 0.3)


# ------------------------------------------------------------------------------------------------ D1. emisarios de pueblo en pueblo (noche, con antorchas)
PUEBLOS6 = [("tlaltenango", "Tlaltenango"), ("teul", "Teúl"), ("jalpa", "Jalpa"), ("juchipila", "Juchipila"), ("apozol", "Apozol"), ("nochistlan", "Nochistlán"), ("moyahua", "Moyahua")]
ORDEN_LUZ = ["juchipila", "apozol", "jalpa", "moyahua", "tlaltenango", "nochistlan", "teul"]       # orden en que les llega el mensaje (recuadro)
ALDEAS = [(260, 0), (1500, 1), (2740, 2), (3980, 3)]                                                 # x del mundo de cada aldea del paisaje nocturno
V_RUN = 560.0                                                                                       # px/s del corredor (mundo)
CAM_INS = (-103.1, 21.56, 4.2)


def _x_run(t):
    return 260 + V_RUN * max(0.0, t - t_mens + 0.2)


def _luces(t):
    return [(*__import__("kz_mapa_dib").CIUDADES[l], smooth(prog(t, t_mens + 0.45 * i, t_mens + 0.45 * i + 0.4))) for i, l in enumerate(ORDEN_LUZ)]


def _post_d1(img, t):
    img = acabado(img, t)
    return MG.inset_mapa(img, t, CAM_INS, _luces(t))


@shot(T_D1, bg=lambda t: bg_grad((22, 24, 70), (8, 8, 30), mid=(16, 16, 50), ym=0.6), post=[_post_d1], ent=("tinta", 0.6))
def d1_emisarios(lz, t):
    xr = _x_run(t)
    camx = xr - 760                                                          # la cámara acompaña al corredor
    lz.relleno(circulo(250, 330, 62, 40), (246, 240, 220), capa=0)          # luna con halo
    lz.halo(250, 330, 260, (190, 200, 255), alfa=0.25, capa=0)
    U.chispas(lz, t, n=26, seed=14, area=(0, 0, W, 560))
    MG.colinas_noche(lz, t, camx, y0=560, semilla=5)
    # camino iluminado por la luna
    xs = np.linspace(-40, W + 40, 40)
    lz.trazo(np.array([(x, 965 + 12 * math.sin((x + camx) * 0.004)) for x in xs]), (70, 70, 130), 34.0, afinar=False, temblor=0.0, capa=1)
    for xa, i in ALDEAS:
        x = xa - camx
        if -500 < x < W + 500:
            MG.aldea_noche(lz, x, 880, 1.9, t, smooth(prog(xr, xa - 40, xa + 160)), seed=i + 3)
    # relevos: cada corredor lleva la antorcha hasta la aldea siguiente y otro sale de ahí
    for i in range(len(ALDEAS) - 1):
        a, b = ALDEAS[i][0], ALDEAS[i + 1][0]
        if a - 60 <= xr <= b + 40:
            x = xr - camx
            K2.cuerpo(lz, x, 975, 34, K2.variar("caxcan", 500 + i), t, piernas="corre", brazos="balanceo", mirar=1, vista="perfil", seed=60 + i, obj_d=MG.antorcha_mano,
                      ph=t * 9.0)
            lz.halo(x + 30, 975 - 400, 320, (255, 170, 80), alfa=0.30, capa=1)
            for k in range(12):                                              # estela de chispas
                ph = (t * 1.6 + h01(i, k)) % 1.0
                lz.relleno(circulo(x - 60 - ph * 380, 975 - 390 + 40 * math.sin(k + t * 3) + 90 * ph, 7 * (1 - ph), 8), (255, 210, 120), alfa=0.9 * (1 - ph), capa=2)
        elif xr > b + 40 and b - camx > -200:                               # el que llegó se queda junto a la fogata
            K2.cuerpo(lz, b - camx - 180, 975, 34, K2.variar("caxcan", 500 + i), t, piernas="idle", brazos="arriba", mirar=1, vista="perfil", seed=60 + i, obj_d=MG.antorcha_mano)
    MG.matorral_noche(lz, camx * 1.5, y=H + 10)
    k = U.pop(t, t_emis)
    if k > 0.01:
        U.llamada(lz, 860, 130, "emisarios de pueblo en pueblo", color=U.COL["naranja"], px=56, k=k, cola=None)
    for xa, i in ALDEAS[1:]:
        snd(t_mens - 0.2 + (xa - 260) / V_RUN, "pluck", 0.3)


# ------------------------------------------------------------------------------------------------ D2. la promesa: los dioses vuelven, los viejos rejuvenecen
@shot(T_D2, bg=lambda t: bg_grad((54, 20, 110), (12, 6, 40), mid=(36, 14, 80), ym=0.5), post=[acabado], ent=("zoom", 0.5))
def d2_promesa(lz, t):
    U.chispas(lz, t, n=20, seed=8)
    U.bokeh(lz, t, seed=52, n=10, colores=((255, 206, 80), (122, 90, 255), (236, 70, 140)), alfa=0.3)
    k = U.pop(t, T_D2 + 0.05)
    if k > 0.01:
        U.globo(lz, W / 2, 140, "una promesa", px=60, k=k, cola=None)
    # izquierda: Xochipilli sube entre haces de luz
    kd = e_out(prog(t, T_D2 + 0.05, t_volver + 0.6))
    if kd > 0.01:
        U.haces_luz(lz, 520, 760, t, n=9, largo=900, color=(255, 230, 160), alfa=0.18 * kd)
        lz.halo(520, 700, 330, (255, 200, 90), alfa=0.35 * kd, capa=1)
        K2.busto(lz, 520, 1060 - 230 * kd, 130, "xochipilli", t, yaw=0.35, emocion="alegre", ojos="abiertos", seed=21, alfa=min(1.0, kd * 1.4))
        U.llamada(lz, 520, 235, "los dioses volverían", color=U.COL["oro"], px=44, k=U.pop(t, t_dioses - 0.1), cola=None, color_texto=(60, 36, 20))
    # derecha: el anciano se vuelve joven (fundido con destellos)
    ka = pk(t, t_ancianos - 0.25, 0.45)
    if ka > 0.01:
        j = smooth(prog(t, t_juventud - 0.1, t_juventud + 0.7))
        K2.busto(lz, 1400, 840, 130 * ka, "anciano_caxcan", t, yaw=-0.35, emocion="pensativo" if j < 0.2 else "sorpresa", ojos="abiertos", seed=24, alfa=1.0 - j)
        if j > 0.01:
            K2.busto(lz, 1400, 840, 130 * ka, "caxcan", t, yaw=-0.35, emocion="alegre", ojos="abiertos", seed=24, alfa=j)
            AB.petalos(lz, t, t_juventud, (1400, 480), n=20, dur=1.8, color=((255, 240, 160), (255, 206, 80), (255, 255, 255)), spread=(-math.pi, 0.0), seed=9, tam=(8, 16))
        U.llamada(lz, 1400, 235, "los ancianos, jóvenes otra vez", color=U.COL["teal"], px=44, k=U.pop(t, t_ancianos), cola=None)
    snd(t_volver, "amanecer", 0.35)
    snd(t_juventud, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ E. 1540: los caxcanes se levantan
def cam_e(t):
    return Klog(t, [(T_E, (-103.12, 21.58, 4.6)), (T_F1, (-103.08, 21.52, 5.3))])


def _rojo(img, t):
    return acabado(U.gradacion(img, luces=(1.0, 0.86, 0.84), sombras=(0.92, 0.80, 0.90), contraste=1.08, saturacion=0.9), t)


@shot(T_E, bg=lambda t: MP.base(cam_e(t), t, exag=12.0, rios_umbral=0.7), post=[_rojo], ent=("tinta", 0.6))
def e_levantamiento(lz, t):
    cam = cam_e(t)
    MD.montes(lz, cam)
    for i, (lug, nom) in enumerate(PUEBLOS6):
        clave = {"tlaltenango": t_tlal, "nochistlan": t_noch, "juchipila": t_juch}.get(lug)
        MD.ciudad(lz, cam, lug, t, T_E, tam=0.85 if clave is None else 1.1, tipo="pueblo", nombre=None, px=22, semilla=i + 4,
                  llama=clave is not None and t > clave + 0.2)
        if clave is not None:
            MD.onda(lz, cam, lug, t, clave, dur=1.6, r_deg=0.35, n=3, ancho=5.0, periodo=0.35, alfa=0.9, color=(255, 120, 90))
            MD.insignia_batalla(lz, cam, lug, t, clave, año=None, s=1.0)
            x, y = MA_.proy(cam, lug)
            k = U.pop(t, clave)
            if k > 0.01:
                dx, dy = {"tlaltenango": (0, -90), "nochistlan": (190, -40), "juchipila": (-200, -30)}[lug]
                U.llamada(lz, x + dx, y + dy, nom, color=U.COL["rojo"], px=38, k=k, cola=None)
    c = lerp(1530, 1540, e_inout(prog(t, t_hacia, t_cuarenta + 0.2)))
    k = U.pop(t, T_E + 0.05)
    if k > 0.01:
        lz.texto(str(int(c)), 270, 150, 140, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U._registrar(lz, 270, 150, 380, 150)
    k = U.pop(t, t_levant)
    if k > 0.01:
        U.llamada(lz, 1500, 150, "¡se levantan!", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_levant + 0.6), cola=None)
    for tt in (t_tlal, t_noch, t_juch):
        snd(tt, "tambor", 0.5)


# ------------------------------------------------------------------------------------------------ F1. un encomendero y dos sacerdotes (memorial sobrio)
GRIS = lambda img, t: acabado(U.gradacion(img, luces=(0.9, 0.88, 0.95), sombras=(0.85, 0.85, 0.95), contraste=1.0, saturacion=0.55), t)


@shot(T_F1, bg=lambda t: bg_grad((60, 52, 84), (20, 16, 34), mid=(40, 34, 60), ym=0.5), post=[GRIS], ent=("fundido", 0.5))
def f1_muertes(lz, t):
    lz.halo(W / 2, 560, 700, (120, 110, 160), alfa=0.25, capa=0)
    lz.relleno(np.array([(0, 900), (W, 880), (W, H), (0, H)]), (34, 28, 50), alfa=0.9, capa=0)
    for i, (x, spec, t0) in enumerate(((520, "encomendero", t_encom1 - 0.1), (960, "fraile", t_sacerd - 0.25), (1400, "fraile", t_sacerd - 0.05))):
        k = pk(t, t0, 0.45)
        if k <= 0.01:
            continue
        for dv in (-110, 110):                                     # velas al pie del retrato
            yv = 905
            lz.relleno(rect_red(x + dv - 16, yv - 90 * k, 32, 90 * k, 6), (236, 228, 214), capa=1)
            llama(lz, x + dv, yv - 90 * k, 0.28 * k, t, seed=i * 2 + (dv > 0))
            lz.halo(x + dv, yv - 110 * k, 110, (255, 200, 120), alfa=0.3 * k, capa=1)
        w_, h_ = 340 * k, 430 * k
        lz.relleno(rect_red(x - w_ / 2 + 10, 560 - h_ / 2 + 14, w_, h_, 18), (10, 6, 20), alfa=0.4, capa=1)
        lz.relleno(rect_red(x - w_ / 2, 560 - h_ / 2, w_, h_, 18), (210, 200, 222), capa=1)
        lz.relleno(rect_red(x - w_ / 2 + 14, 560 - h_ / 2 + 14, w_ - 28, h_ - 28, 12), (86, 76, 112), capa=1)
        with lz.recorte(rect_red(x - w_ / 2 + 14, 560 - h_ / 2 + 14, w_ - 28, h_ - 28, 12)):
            K2.busto(lz, x, 560 + h_ * 0.42, 62 * k, spec, t, yaw=0.0, emocion="serio", ojos="cerrados", seed=40 + i, brazo=False)
        # crespón negro en diagonal
        c = smooth(prog(t, t0 + 0.5, t0 + 0.9))
        if c > 0.01:
            x0, y0 = x + w_ / 2 - 90 * k, 560 - h_ / 2
            lz.relleno(np.array([(x0, y0), (x0 + 60 * k, y0), (x + w_ / 2, y0 + 120 * k * c), (x + w_ / 2, y0 + 180 * k * c)]), (16, 12, 24), alfa=0.95, capa=2)
    k = U.pop(t, t_mataron)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "un encomendero y dos sacerdotes", color=U.COL["oscuro"], px=54, k=k, cola=None)
    snd(t_mataron, "gong", 0.4)


# ------------------------------------------------------------------------------------------------ F2. el refugio: el peñol del Mixtón
@shot(T_F2, bg=lambda t: PA.cielo(0.55), post=[acabado], ent=("tinta", 0.6))
def f2_penol(lz, t):
    cx = 22.0 * (t - T_F2)
    gx, gy, z = K(t, [(T_F2, (560, 880, 1.6)), (t_refug + 0.6, (600, 860, 1.6)), (t_paredes, (720, 640, 1.45)), (t_mixton - 0.2, (980, 640, 1.0)), (T1(E6), (980, 640, 1.04))])
    PA.sol(lz, 1550, 230, 56, t, 0.55)
    PA.sierras(lz, t, cx, 0.55, y0=700, capas=4, semilla=31)
    PA.aves(lz, t, n=6, seed=12, y0=150, y1=330)
    with lz.grupo(W / 2 - gx * z, H / 2 - gy * z, z):
        MG.penol(lz, t, cx=980, y_base=1000, ancho=720, alto=600, sube=0.12 + 0.88 * smooth(prog(t, T_F2, T1(E6) - 0.3)), fogatas=smooth(prog(t, t_penol, t_penol + 1.0)))
        p = PA.pal(0.55)
        lz.relleno(np.array([(0, 990), (W, 970), (W, H + 200), (0, H + 200)]), p["pasto"][1], capa=1)
    k = U.pop(t, t_paredes) * U.salida(t, t_mixton - 0.1)
    if k > 0.01:
        MG.flecha_altura(lz, 1450, 420, 990, alfa=k)
        U.llamada(lz, 1640, 700, "paredes casi verticales", color=U.COL["teal"], px=40, k=k, cola=None)
    k = U.pop(t, t_penol) * U.salida(t, t_paredes - 0.1)
    if k > 0.01:
        U.llamada(lz, 980, 300, "un peñol", color=U.COL["naranja"], px=56, k=k, cola="abajo")
    k = U.pop(t, t_mixton)
    if k > 0.01:
        U.llamada(lz, 980, 300, "el Mixtón", color=U.COL["rojo"], px=80, k=k * U.repop(t, t_mixton + 0.5), cola="abajo")
    snd(t_mixton, "gong", 0.5)
    snd(t_refug, "whoosh", 0.35)
