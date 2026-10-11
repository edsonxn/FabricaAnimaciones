# -*- coding: utf-8 -*-
"""Escena 9 · el castigo (5:07-5:42), paleta gris-violeta y sin mostrar violencia: ejecuciones (cañones, perros, espadas) como iconos duotono,
miles de cautivos llevados a las minas, pueblos en ruinas y huida a la sierra, la ciudad del cerro que se desvanece sobre un refugio escondido,
la investigación secreta del Consejo de Indias sobre el virrey (retrato real bajo la lupa) y la decisión: quedarse en la sierra o bajar al valle."""
import math

import numpy as np

import kz_ui as U
import kz_abstracto as AB
import kz_pers2d as K2
import kz_retrato as RT
import plano as P
import paisajes as PA
import mundos_f as MF
import mundos_j as MJ
import mundos_a as MA_s
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E9 = "castigo"
t_siguio, t_brutal, t_prision, t_ejec, t_canones, t_perros, t_espadas = (T(E9, "siguio", frase=0), T(E9, "brutal", frase=0), T(E9, "prisioneros", frase=0), T(E9, "ejecutados", frase=0),
                                                                         T(E9, "canones", frase=0), T(E9, "perros", frase=0), T(E9, "espadas", frase=0))
t_miles, t_encad, t_minas, t_esclavas = T(E9, "miles", frase=1), T(E9, "encadenadas", frase=1), T(E9, "minas", frase=1), T(E9, "esclavas", frase=1)
t_pueblos, t_ruinas, t_sobrev, t_huyeron, t_sierra = T(E9, "pueblos", frase=2), T(E9, "ruinas", frase=2), T(E9, "sobrevivientes", frase=2), T(E9, "huyeron", frase=2), T(E9, "sierra", frase=2)
t_levantado, t_ciudades, t_ahora, t_escondido = T(E9, "levantado", frase=3), T(E9, "ciudades", frase=3), T(E9, "ahora", frase=3), T(E9, "escondido", frase=3)
t_crueldad, t_anos, t_consejo, t_invest, t_secreta, t_conducta, t_virrey = (T(E9, "crueldad", frase=4), T(E9, "anos", frase=4), T(E9, "consejo", frase=4), T(E9, "investigacion", frase=4),
                                                                            T(E9, "secreta", frase=4), T(E9, "conducta", frase=4), T(E9, "virrey", frase=4))
t_quedo, t_decidir, t_sierra2, t_volvia, t_valle = T(E9, "quedo", frase=5), T(E9, "decidir", frase=5), T(E9, "sierra", frase=5), T(E9, "volvia", frase=5), T(E9, "valle", frase=5)
T_A, T_B, T_C, T_D, T_E, T_F = T0(E9), INI(E9, 1) - 0.15, INI(E9, 2) - 0.15, INI(E9, 3) - 0.15, INI(E9, 4) - 0.15, INI(E9, 5) - 0.15


def GRIS(img, t):
    return acabado(U.gradacion(img, luces=(0.94, 0.9, 1.0), sombras=(0.86, 0.84, 0.98), contraste=1.02, saturacion=0.62), t)


BG_G = lambda t: bg_grad((70, 58, 96), (20, 14, 34), mid=(44, 34, 64), ym=0.55)


# ------------------------------------------------------------------------------------------------ A. lo que siguió fue brutal
@shot(T_A, bg=BG_G, post=[GRIS], ent=("fundido", 0.6))
def a_brutal(lz, t):
    U.bokeh(lz, t, seed=91, n=8, colores=((150, 130, 190), (110, 90, 150)), alfa=0.22)
    # fila de prisioneros en silueta, cabeza baja, de espaldas a la luz
    lz.relleno(rect_red(0, 960, W, 140, 0), (30, 22, 44), capa=1)
    for i in range(9):                                                   # prisioneros de cuerpo entero, cabizbajos
        x = 140 + 205 * i + 24 * h01(2, i)
        spec = dict(K2.variar("caxcan" if i % 3 else "caxcana", 1300 + i), ropa=(86, 74, 110), ropa2=(104, 92, 126), tocado=None, pelo=(30, 24, 40))
        K2.cuerpo(lz, x, 990, 34, spec, t, piernas="idle", brazos="idle", mirar=1 if i % 2 else -1, vista="perfil", seed=1300 + i, cara="minima", sombra=False, alfa=0.95,
                  emocion="triste")
    for j, x in enumerate((40, 1880)):                                   # guardias en silueta a los lados
        MA_s.silueta_guerrero(lz, x, 1000, 30, (22, 16, 34), t, seed=j, alfa=0.95, lanza=True)
    k = U.pop(t, t_brutal - 0.1) * U.salida(t, t_ejec - 0.1)
    if k > 0.01:
        P.rotulo(lz, W / 2, 360, "brutal", px=170, k=0.8 + 0.2 * k, color=(236, 228, 246), alfa=k)
    # los tres medios de ejecución como iconos duotono con un destello local (sin mostrar el acto)
    for j, (t0, fn, nombre) in enumerate(((t_canones, MJ.icono_canon, "cañones"), (t_perros, lambda lz, x, y, s: MJ.icono_perro(lz, x, y, s, t), "perros"),
                                           (t_espadas, MJ.icono_espada, "espadas"))):
        k = pk(t, t0 - 0.1, 0.45)
        if k > 0.01:
            x = 520 + 440 * j
            lz.halo(x, 420, 260 * k, (214, 80, 96), alfa=0.30 * (1 - 0.6 * smooth(prog(t, t0 + 0.3, t0 + 1.2))), capa=1)
            lz.relleno(circulo(x, 420, 170 * k, 48), (46, 36, 66), alfa=0.9, capa=2)
            fn(lz, x + (20 if j == 1 else 0), 440 if j != 2 else 470, 50 * k)
            U.llamada(lz, x, 640, nombre, color=U.COL["oscuro"], px=44, k=k, cola=None)
    k = U.pop(t, t_prision - 0.1) * U.salida(t, t_canones - 0.15)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "prisioneros ejecutados", color=U.COL["oscuro"], px=56, k=k, cola=None)
    snd(t_brutal, "gong", 0.5)
    for tt in (t_canones, t_perros, t_espadas):
        snd(tt, "tambor", 0.35)


# ------------------------------------------------------------------------------------------------ B. miles de personas encadenadas, a las minas
@shot(T_B, bg=lambda t: bg_grad((96, 80, 120), (40, 30, 56)), post=[GRIS], ent=("tinta", 0.6))
def b_minas(lz, t):
    MJ.mina_corte(lz, t)
    # fila de cautivos encadenados que llega por la ladera hacia la entrada
    MF.fila_encadenada(lz, t, T_B - 4.0, y=520, n=8, s=17, x_ini=-1300, vel=120, alfa=1.0)
    k = U.pop(t, t_miles)
    if k > 0.01:
        U.llamada(lz, 1360, 170, "miles, a las minas", color=U.COL["oscuro"], px=60, k=k * U.repop(t, t_minas + 0.2), cola=None)
    k = U.pop(t, t_esclavas)
    if k > 0.01:
        U.llamada(lz, 1360, 270, "como esclavos", color=U.COL["morado"], px=48, k=k, cola=None)
    snd(t_encad, "crujido", 0.35)


# ------------------------------------------------------------------------------------------------ C. pueblos en ruinas; los sobrevivientes huyen a la sierra
@shot(T_C, bg=lambda t: PA.cielo(0.8), post=[GRIS], ent=("tinta", 0.6))
def c_ruinas(lz, t):
    cx = 30.0 * (t - T_C)
    PA.sol(lz, 1500, 280, 50, t, 0.8, alfa=0.6)
    PA.sierras(lz, t, cx, 0.8, y0=600, capas=5, semilla=95)
    p = PA.pal(0.8)
    degradado_v(lz, 0, W, 760, H, p["pasto"][0], p["pasto"][1], 760, H)
    # sendero que sube a la sierra y la gente que se aleja por él
    sendero = [(1900, 1060), (1500, 900), (1100, 820), (800, 740), (560, 680)]
    q = np.array(catmull(np.array(sendero, float), 10, False))
    lz.trazo(q, (176, 160, 170), 46.0, afinar=False, temblor=0.0, capa=1)
    seg = np.hypot(*np.diff(q, axis=0).T)
    d = np.r_[0, np.cumsum(seg)]
    for i in range(9):
        f = (0.12 + 0.11 * i + 0.05 * (t - T_C)) % 1.0
        s_ = d[-1] * f
        j = int(np.clip(np.searchsorted(d, s_) - 1, 0, len(q) - 2))
        u = (s_ - d[j]) / max(1e-6, d[j + 1] - d[j])
        px, py = q[j] + (q[j + 1] - q[j]) * u
        sc = 9 + 14 * (py - 680) / 380
        spec = dict(K2.variar("caxcana" if i % 3 == 1 else "caxcan", 1400 + i), tocado=None, ropa=(150, 136, 160))
        K2.cuerpo(lz, px, py, sc, spec, t, piernas="camina", brazos="carga" if i % 2 else "balanceo", mirar=-1, vista="perfil", seed=1400 + i, cara="ninguna", sombra=False,
                  ph=t * 4.5 + i, emocion="triste")
    # pueblo en ruinas en primer plano
    for i, (x, s) in enumerate(((200, 2.6), (560, 3.0), (1660, 2.8), (1260, 2.2))):
        MJ.casa_ruina(lz, x, 1000 - 30 * (i % 2), s, seed=i, humo_t=T_C - 3.0, t=t)
    k = U.pop(t, t_ruinas)
    if k > 0.01:
        U.llamada(lz, 520, 150, "pueblos en ruinas", color=U.COL["oscuro"], px=58, k=k, cola=None)
    k = U.pop(t, t_huyeron)
    if k > 0.01:
        U.llamada(lz, 560, 580, "huyen a la sierra", color=U.COL["morado"], px=46, k=k, cola="abajo")
    snd(t_ruinas, "crujido", 0.35)


# ------------------------------------------------------------------------------------------------ D. de construir ciudades en los cerros a vivir escondidos entre ellos
@shot(T_D, bg=lambda t: bg_grad((40, 34, 84), (14, 10, 34), mid=(28, 24, 62), ym=0.5), post=[GRIS], ent=("tinta", 0.6))
def d_escondidos(lz, t):
    U.chispas(lz, t, n=22, seed=19, area=(0, 0, W, 420))
    lz.relleno(np.array([(0, 640), (360, 380), (700, 470), (960, 300), (1240, 460), (1560, 380), (1920, 560), (1920, H), (0, H)]), (54, 48, 96), capa=0)
    lz.relleno(np.array([(0, 760), (420, 620), (900, 700), (1300, 600), (1920, 740), (1920, H), (0, H)]), (40, 34, 74), capa=0)
    fant = 1.0 - smooth(prog(t, t_ahora - 0.2, t_escondido + 0.4))
    ciudad = smooth(prog(t, T_D, t_ciudades + 0.3))
    MJ.ciudad_fantasma(lz, 960, 480, 80, ciudad * fant, t)
    kr = smooth(prog(t, t_ahora - 0.4, t_ahora + 0.4))
    MJ.refugio(lz, 1280, 1010, 2.1, t, alfa=kr)
    for k in range(6):                                                  # árboles en silueta delante
        x = 120 + 330 * k
        lz.relleno(np.array([(x - 60, 1080), (x, 820 - 60 * h01(3, k)), (x + 60, 1080)]), (24, 20, 46), capa=2)
    k = U.pop(t, t_ciudades) * U.salida(t, t_ahora - 0.1)
    if k > 0.01:
        U.llamada(lz, 960, 140, "levantaron ciudades en los cerros", color=U.COL["naranja"], px=50, k=k, cola=None)
    k = U.pop(t, t_escondido)
    if k > 0.01:
        U.llamada(lz, 960, 140, "ahora vivían escondidos", color=U.COL["morado"], px=56, k=k, cola=None)
    snd(t_ahora, "whoosh", 0.3)


# ------------------------------------------------------------------------------------------------ E. el Consejo de Indias investiga en secreto al virrey
@shot(T_E, bg=lambda t: bg_plano((64, 46, 70)), post=[GRIS], ent=("tinta", 0.6))
def e_consejo(lz, t):
    MJ.sala_consejo(lz, t, 20 * (t - T_E))
    for i, x in enumerate((360, 620, 1180, 1500)):                      # consejeros de negro tras la mesa
        spec = dict(K2.TIPOS["encomendero"], ropa=(36, 30, 44), ropa2=(240, 236, 226), tocado=None, pelo=((200, 196, 204), (60, 44, 40), (120, 100, 90), (190, 186, 196))[i])
        K2.busto(lz, x, 735, 72, spec, t, yaw=(0.4, 0.3, -0.3, -0.4)[i], emocion="serio", ojos="abiertos", seed=1600 + i, brazo=False)
    lz.relleno(rect_red(-20, 760, W + 40, 60, 6), (60, 110, 80), capa=1)
    lz.relleno(rect_red(-20, 800, W + 40, 300, 0), (40, 80, 60), capa=1)
    k = U.pop(t, t_consejo - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 120, "el Consejo de Indias", color=U.COL["rojo"], px=58, k=k, cola=None)
    # el expediente sobre la mesa y el retrato del virrey bajo la lupa
    ke = pk(t, t_invest - 0.2, 0.5)
    if ke > 0.01:
        U.pergamino_grande(lz, 700, 620, 620, 420, t, t_invest - 0.2, lineas=("Nueva Galicia, 1541-1542", "conducta del virrey", "testigos: ..."), titulo="Pesquisa", sello=True)
        MJ.sello_secreto(lz, 760, 760, 1.0, e_back(prog(t, t_secreta, t_secreta + 0.35)))
    kr = pk(t, t_conducta - 0.4, 0.5)
    if kr > 0.01:
        RT.retrato(lz, 1380, 900, 170 * (0.9 + 0.1 * kr), "mendoza", t, emocion="serio", alfa=min(1.0, kr * 1.3), seed=4)
        lx = 1380 + 90 * math.sin(t * 1.6)
        ly = 560 + 50 * math.cos(t * 1.3)
        MJ.lupa(lz, lx, ly, 120 * kr)
    k = U.pop(t, t_virrey)
    if k > 0.01:
        U.llamada(lz, 1380, 260, "...sobre el propio virrey", color=U.COL["oscuro"], px=46, k=k, cola=None)
    snd(t_secreta, "bonk", 0.4)
    snd(t_virrey, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ F. ¿quedarse en la sierra o bajar al valle?
@shot(T_F, bg=lambda t: bg_plano((40, 44, 86)), post=[acabado], ent=("tinta", 0.6))
def f_decision(lz, t):
    MJ.encrucijada(lz, t, 0.0)
    m = math.sin((t - T_F) * 1.6)                                       # la familia mira a un lado y al otro
    mira = -1 if t < t_valle - 0.3 and m < 0.3 else 1
    for i, (dx, tipo) in enumerate(((-110, "caxcana"), (-30, "nino"), (60, "caxcan"), (140, "anciano_caxcan"))):
        K2.cuerpo(lz, 960 + dx * 1.6, 1060, 40 if tipo != "nino" else 32, tipo, t, piernas="idle", brazos="señala" if (i == 2 and t > t_valle) else "idle", mirar=mira if i != 1 else -mira,
                  vista="perfil", seed=1500 + i, emocion="pensativo", objetivo=(1500, 700))
    k = U.pop(t, t_sierra2)
    if k > 0.01:
        U.llamada(lz, 420, 260, "¿quedarse en la sierra?", color=U.COL["azul"], px=48, k=k, cola=None)
    k = U.pop(t, t_valle)
    if k > 0.01:
        U.llamada(lz, 1480, 260, "¿o volver al valle?", color=U.COL["naranja"], px=48, k=k, cola=None)
    k = U.pop(t, t_quedo) * U.salida(t, t_sierra2 - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "lo que quedó de los caxcanes", color=U.COL["oscuro"], px=52, k=k, cola=None)
    snd(t_decidir, "pluck", 0.3)
