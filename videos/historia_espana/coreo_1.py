# -*- coding: utf-8 -*-
"""Coreografía (1/4): gancho (el idioma de 600 millones), orígenes (Atapuerca, Altamira, íberos, celtas, fenicios, griegos,
cartagineses, Aníbal) y Roma (conquista, Numancia, calzadas, acueducto, teatro, latín, Trajano y Adriano).
Capas de territorio en "eu": 0 = el poder principal, 1 = íberos, 2 = celtas, 3 = Cartago."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_es1 as E1
import obj_es2 as E2
from core import FIN, INI, T, kf
from coreo_util import CI, COL, andar, ciudad, formacion, ga, lugar, mece, pa, titulo
from motor import e_back, e_in, e_inout, e_out, lerp, prog


def cortes(R):
    pass


def construir(R):
    _mares(R)
    _gancho(R)
    _origenes(R)
    _roma(R)


def _mares(R):
    R.mar("eu", "OCÉANO ATLÁNTICO", -13.2, 40.5, 40)
    R.mar("eu", "OCÉANO ATLÁNTICO", -9.5, 46.5, 40)
    R.mar("eu", "MAR MEDITERRÁNEO", 5.2, 38.4, 40)
    R.mar("eu", "MAR MEDITERRÁNEO", 1.0, 36.6, 38)
    R.mar("eu", "MAR CANTÁBRICO", -5.5, 44.25, 34)
    R.mar("am", "OCÉANO ATLÁNTICO", -38.0, 30.0, 44)
    R.mar("am", "OCÉANO ATLÁNTICO", -28.0, 2.0, 44)
    R.mar("am", "OCÉANO PACÍFICO", -118.0, 2.0, 44)
    R.mar("am", "OCÉANO PACÍFICO", 150.0, 26.0, 44)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_fen, t_rom, t_vis, t_ara, t_todos, t_rin = T(e, "fenicios"), T(e, "romanos"), T(e, "visigodos"), T(e, "arabes"), T(e, "todos"), T(e, "rincon")
    t_aqui, t_idioma, t_hoy, t_600, t_pers = T(e, "aqui"), T(e, "idioma"), T(e, "hoy"), T(e, "seiscientos"), T(e, "personas")
    t_esta, t_hist, t_esp, t_cinco, t_min = T(e, "esta"), T(e, "historia"), T(e, "espana"), T(e, "cinco"), T(e, "minutos")
    # cámara: la península de cerca -> el mundo hispanohablante -> la península
    R.camara(0.0, -3.4, 40.2, 2.1)
    R.camara(t_todos, -3.6, 40.0, 2.35)
    R.camara(t_aqui, -4.0, 40.0, 2.0)
    R.camara(t_idioma + 1.0, -50.0, 12.0, 0.20)
    R.camara(t_pers + 0.3, -52.0, 10.0, 0.19)
    R.camara(t_hist, -3.6, 40.0, 1.6)
    R.camara(t_min + 0.6, -3.6, 39.8, 2.15)
    R.rejilla(t_idioma - 0.2, "am", 0.8)
    R.rejilla(t_esta + 0.1, "eu", 0.6)
    # los pueblos que llegaron
    pa_ = dict(zs=0.5, z=2)
    ga(R, lambda t: E1.barco_fenicio(int(t * 5)), (1.8, 37.3), t_fen - 0.1, t_aqui, s=0.55, off=mece(5, 2.0), sem=1, extra=[(0.1, "ola", 0.4)], **pa_)
    ga(R, E1.fenicio(0), (0.2, 39.0), t_fen + 0.15, t_aqui, s=0.6, sem=2, **pa_)
    ga(R, E1.legionario(0), (1.0, 41.2), t_rom - 0.05, t_aqui, s=0.62, sem=3, extra=[(0.05, "clink", 0.5)], **pa_)
    ga(R, E1.rey_godo(0), (-6.2, 41.4), t_vis - 0.05, t_aqui, s=0.62, sem=4, extra=[(0.1, "brillo", 0.4)], **pa_)
    ga(R, E2.tariq(0), (-4.4, 37.1), t_ara - 0.05, t_aqui, s=0.62, sem=5, flip=True, **pa_)
    R.terreno(t_rin - 0.2, "peninsula", (226, 180, 96), 0.9)
    R.terreno(t_idioma - 0.3, None, (226, 180, 96), 0.4)
    R.snd(t_rin, "brillo", 0.5)
    # el idioma: el mundo hispanohablante se pinta y aparecen los «¡hola!»
    R.terreno(t_idioma, "peninsula_am", COL["hispano"], 0.6, rej="am")
    R.terreno(t_idioma + 0.7, "hispanohablantes", COL["hispano"], 1.6, rej="am")
    R.snd(t_idioma + 0.6, "whoosh", 0.5, dur=1.2)
    R.contador(t_hoy, t_600 + 0.9, 0, 600_000_000, (960, 196), px=96, hasta_t=FIN(e, 1) + 0.5)
    R.snd(t_hoy, "reloj_rapido", 0.45, dur=1.4)
    for k, (cl, px) in enumerate((("madrid", 40), ("mexico", 52), ("lima", 44), ("buenos_aires", 50))):
        t0 = t_hoy + 0.25 + 0.22 * k
        lugar(R, t0, FIN(e, 1) + 0.2, "¡HOLA!", CI[cl], off=(0, -10), px=px, d=0.3)
        R.snd(t0, "pop", 0.3, tono=1.0 + 0.08 * k)
    titulo(R, t_pers - 0.2, FIN(e, 1) + 0.1, "HABLANTES DE ESPAÑOL", y=300, px=58)
    # título
    R.terreno(t_esp - 0.2, "espana", COL["espana"], 0.9)
    R.texto(t_hist - 0.2, FIN(e) + 0.9, "LA HISTORIA DE ESPAÑA", (960, 178), px=104, d=1.0)
    R.texto(t_cinco - 0.1, FIN(e) + 0.9, "en 5 minutos", (960, 300), px=78, d=0.6)
    R.snd(t_hist - 0.2, "escribir", 0.5, dur=1.0)
    R.snd(t_cinco, "pluck", 0.5)
    pa(R, lambda t: C.cronometro(round(kf(t, [(t_cinco, 0.0), (FIN(e) + 1.2, 0.9)], ease=lambda u: u), 2)), 1660, 840, 0.9, t_cinco - 0.1, sem=7,
       extra=[(0.1, "reloj_rapido", 0.4, {"dur": 1.2})])


# ------------------------------------------------------------------ ORÍGENES
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_millon, t_hum, t_ata = T(e, "millon"), T(e, "humanos"), T(e, "atapuerca")
    t_quince, t_pinto, t_bis, t_techo, t_alta = T(e, "quince"), T(e, "pinto"), T(e, "bisontes"), T(e, "techo"), T(e, "altamira")
    t_desp, t_ibe, t_med, t_cel, t_int = T(e, "despues"), T(e, "iberos"), T(e, "mediterraneo"), T(e, "celtas"), T(e, "interior")
    t_mar, t_com, t_tres, t_fen, t_gadir, t_cadiz = T(e, "mar", frase=3), T(e, "comerciantes"), T(e, "tres"), T(e, "fenicios"), T(e, "gadir"), T(e, "cadiz")
    t_gri, t_cart, t_sur, t_base = T(e, "griegos"), T(e, "cartagineses"), T(e, "sur"), T(e, "base")
    t_desde, t_ani, t_ele, t_ata2, t_roma = T(e, "desde"), T(e, "anibal"), T(e, "elefantes"), T(e, "atacar"), T(e, "roma")
    R.terreno(i0 - 0.6, None, COL["espana"], 0.6)
    # cámara
    R.camara(i0 - 0.2, -3.6, 41.6, 3.2)
    R.camara(t_hum, -3.55, 42.3, 5.6)
    R.camara(t_quince - 0.2, -3.9, 42.9, 6.0)
    R.camara(t_bis, -4.1, 43.2, 7.4)
    R.camara(t_alta + 0.4, -4.1, 43.15, 7.0)
    R.camara(t_desp + 0.2, -3.4, 40.0, 2.3)
    R.camara(t_int + 0.3, -3.2, 39.8, 2.3)
    R.camara(t_com, -2.0, 37.8, 1.8)
    R.camara(t_cadiz + 0.3, -3.0, 37.6, 2.2)
    R.camara(t_gri, 0.5, 39.6, 1.7)
    R.camara(t_cart, 2.0, 38.5, 1.45)
    R.camara(t_base + 0.2, 2.0, 38.6, 1.5)
    R.camara(t_ani, 1.0, 39.0, 1.55)
    R.camara(t_ata2, 6.5, 42.5, 1.5)
    R.camara(FIN(e) + 0.3, 9.0, 42.4, 1.5)
    # años
    R.anio(i0 - 0.1, -1_000_000)
    R.anio(t_ata, -1_000_000)
    R.anio(t_quince - 0.1, -1_000_000)
    R.anio(t_quince + 1.0, -15_000)
    R.anio(t_desp - 0.1, -15_000)
    R.anio(t_desp + 0.9, -500)
    R.anio(t_tres - 0.1, -500)
    R.anio(t_tres + 0.7, -1100)
    R.anio(t_gri - 0.2, -1100)
    R.anio(t_gri + 0.6, -575)
    R.anio(t_cart, -575)
    R.anio(t_cart + 0.7, -227)
    R.anio(t_ani - 0.1, -227)
    R.anio(t_ani + 0.6, -218)
    # Atapuerca
    ciudad(R, t_ata - 0.2, t_quince + 0.2, "atapuerca", "ATAPUERCA", "arriba", 50)
    ga(R, E1.humano_atapuerca(0), CI["atapuerca"], t_hum - 0.1, t_quince + 0.1, s=0.62, off=(-280, 170), sem=10, zs=0.4, z=2)
    ga(R, E1.craneo(), CI["atapuerca"], i0 + 0.15, t_quince + 0.1, s=0.56, off=(280, 150), sem=11, zs=0.4, z=2, snd=("plop", 0.5))
    R.snd(t_millon, "tambor", 0.4)
    # Altamira: el pintor y el bisonte que se va pintando
    ciudad(R, t_alta - 0.2, t_desp + 0.1, "altamira", "ALTAMIRA", "arriba", 50)
    pa(R, E1.techo_cueva(), 1220, 860, 1.25, t_quince + 0.1, t_desp + 0.1, sem=12, entra="sube", z=1, snd=("crece", 0.4))
    pa(R, E1.bisonte(), 1230, 730, 1.45, t_bis - 0.1, t_desp + 0.1, sem=13, entra="pluma", d_in=1.5, z=2, snd=("pincel", 0.5))
    pa(R, lambda t: E1.pintor_altamira(int(t * 3) % 2), 430, 1000, 1.25, t_pinto - 0.3, t_desp + 0.1, sem=14, z=3)
    # íberos y celtas
    R.terreno(t_ibe - 0.1, "iberos", COL["iberos"], 1.1, capa=-2)
    R.terreno(t_cel - 0.1, "celtas", COL["celtas"], 1.1, capa=-1)
    R.snd(t_ibe, "whoosh", 0.4, dur=0.8)
    R.snd(t_cel, "whoosh", 0.4, dur=0.8)
    ga(R, E1.ibero(0), (-0.9, 39.4), t_ibe, t_com, s=0.62, sem=15, z=2)
    ga(R, E1.dama_elche(), CI["elche"], t_med - 0.1, t_com, s=0.42, off=(130, -40), sem=16, z=2, extra=[(0.1, "brillo", 0.4)])
    lugar(R, t_ibe, t_com - 0.6, "ÍBEROS", (1.0, 41.95), off=(0, 0), px=58)
    lugar(R, t_med + 0.2, t_com - 0.1, "DAMA DE ELCHE", CI["elche"], off=(130, 60), px=34)
    ga(R, E1.celta(0), (-5.0, 40.4), t_cel, t_com, s=0.62, sem=17, z=2)
    lugar(R, t_cel, t_com - 0.6, "CELTAS", (-6.6, 42.5), off=(0, 0), px=58)
    # fenicios: el barco llega por el Mediterráneo y funda Gadir
    Pf = M.RUTAS["fenicios"]
    R.ruta(Pf, t_mar - 0.2, 2.6, ancho=5.0, t1=t_gri)
    andar(R, lambda p: E1.barco_fenicio(p), Pf, t_mar - 0.1, 2.8, t1=t_gri, s=0.55, sem=18, zs=0.4, z=2, fps=5, snd=("ola", 0.4))
    ciudad(R, t_gadir - 0.1, t_cart, "cadiz", "GADIR (CÁDIZ)", "abajo", 46)
    ga(R, E1.fenicio(0, "feliz"), CI["cadiz"], t_fen, t_gri + 0.4, s=0.62, off=(-170, 60), sem=19, z=2)
    lugar(R, t_fen, t_gri - 0.1, "FENICIOS", CI["cadiz"], off=(-170, -230), px=52)
    # griegos y cartagineses
    R.ruta(M.RUTAS["griegos"], t_gri - 0.1, 1.4, ancho=5.0, t1=t_desde)
    ciudad(R, t_gri + 0.4, t_desde, "ampurias", "AMPURIAS", "izq", 42)
    ga(R, E1.griego(0), CI["ampurias"], t_gri + 0.2, t_desde, s=0.6, off=(80, 120), sem=20, z=2)
    R.terreno(t_cart - 0.1, "cartago", COL["cartago"], 1.3, capa=3)
    ciudad(R, t_cart + 0.2, t_ani, "cartago", "CARTAGO", "abajo", 42)
    ciudad(R, t_base - 0.2, FIN(e) + 0.4, "cartagena", "CARTAGO NOVA", "abajo", 42)
    ga(R, E1.cartagines(0), CI["cartagena"], t_cart + 0.1, t_desde, s=0.62, off=(-130, -30), sem=21, z=2)
    R.snd(t_cart, "tambor", 0.5)
    # Aníbal y los elefantes, de Cartagena a Roma
    Pa = M.RUTAS["anibal"]
    R.rio(Pa, t_ani - 0.2, (FIN(e) + 0.6) - t_ani, COL["cartago"], ancho=16)
    andar(R, lambda p: E1.elefante(p), Pa, t_ani - 0.1, (FIN(e) + 0.4) - t_ani, s=0.6, sem=22, zs=0.4, z=2, fps=5, snd=("cuerno", 0.5), ease=lambda u: u)
    lugar(R, t_ani, t_ata2 - 0.1, "ANÍBAL", CI["cartagena"], off=(40, -230), px=56)
    ciudad(R, t_ata2 - 0.2, FIN(e) + 0.4, "roma", "ROMA", "abajo", 50)
    R.terreno(t_roma - 0.3, "roma_italia", COL["roma"], 0.8)
    R.snd(t_ele, "cuerno", 0.4, tono=0.8)


# ------------------------------------------------------------------ ROMA
def _roma(R):
    e = "roma"
    i0 = INI(e)
    t_mala, t_gana, t_guerra, t_pen = T(e, "mala"), T(e, "gana"), T(e, "guerra"), T(e, "peninsula")
    t_conq, t_200, t_num, t_sit, t_morir, t_rend = T(e, "conquistarla"), T(e, "doscientos"), T(e, "numancia"), T(e, "sitiados"), T(e, "morir"), T(e, "rendirse")
    t_final, t_hisp, t_calz, t_acue, t_teat, t_latin, t_abue, t_espa = (T(e, "final"), T(e, "hispania", frase=2), T(e, "calzadas"), T(e, "acueductos"),
                                                                       T(e, "teatros"), T(e, "latin"), T(e, "abuelo"), T(e, "espanol"))
    t_le, t_emp, t_tra, t_adr = T(e, "le", frase=3), T(e, "emperadores"), T(e, "trajano"), T(e, "adriano")
    # territorio: Roma se queda con la costa, luego con todo
    R.terreno(t_gana, "hispania_197", COL["roma"], 1.4)
    R.terreno(t_gana, None, COL["cartago"], 1.0, capa=3)
    R.terreno(t_200 - 0.2, "hispania_133", COL["roma"], 2.0)
    R.terreno(t_rend + 0.2, "hispania_19", COL["roma"], 1.4)
    R.terreno(t_rend + 1.4, None, COL["iberos"], 0.3, capa=-2)
    R.terreno(t_rend + 1.4, None, COL["celtas"], 0.3, capa=-1)
    R.sello(t_pen + 0.1, "laurel", "HISPANIA ROMANA", color=(186, 52, 46))
    # cámara
    R.camara(i0 - 0.2, 4.5, 40.6, 1.45)
    R.camara(t_pen, 1.0, 40.4, 1.6)
    R.camara(t_conq, -3.0, 40.6, 2.2)
    R.camara(t_num - 0.3, -2.45, 41.75, 5.6)
    R.camara(t_rend, -2.45, 41.8, 6.0)
    R.camara(t_final + 0.2, -3.6, 40.1, 2.3)
    R.camara(t_latin, -3.6, 40.0, 2.35)
    R.camara(t_le, -5.4, 37.7, 4.4)
    R.camara(FIN(e) + 0.3, -5.6, 37.6, 4.8)
    # años
    R.anio(i0, -218)
    R.anio(t_gana + 0.5, -206)
    R.anio(t_200 - 0.2, -206)
    R.anio(t_num, -133)
    R.anio(t_rend + 0.3, -133)
    R.anio(t_final, -19)
    R.anio(t_le - 0.2, -19)
    R.anio(t_tra + 0.4, 98)
    R.anio(t_adr + 0.4, 117)
    # la guerra: choque y legiones que desembarcan
    pa(R, A.estallido(14, 50, 150), 960, 600, 1.2, t_gana - 0.05, t_gana + 0.5, entra="fija", sale="cortar", sem=30, snd=("explosion", 0.5))
    pa(R, A.espadas(), 960, 640, 1.0, t_gana, t_pen + 0.4, sem=31, extra=[(0.05, "espada", 0.5)])
    Pd = M.RUTAS["roma_desembarco"]
    R.ruta(Pd, i0 + 0.1, 1.4, ancho=5.0, t1=t_conq, flecha=True)
    for k in range(3):
        andar(R, lambda p: E1.legionario(p), [(3.1, 42.1), (0.2, 40.8), (-2.2, 39.6)],
              t_guerra + 0.2 * k, 3.0, t1=t_conq + 0.2, s=0.58, sem=32 + k, z=2, flip=True, off=formacion(k, 3, 150))
    titulo(R, t_mala - 0.1, t_gana - 0.1, "¡MALA IDEA!", px=86)
    # Numancia
    titulo(R, t_200 - 0.1, t_num - 0.2, "CASI 200 AÑOS", px=82)
    ciudad(R, t_num - 0.1, t_final, "numancia", None)
    lugar(R, t_num - 0.1, t_final - 0.6, "NUMANCIA", CI["numancia"], off=(0, 190), px=58)
    for k, dx in enumerate((-90, 0, 90)):
        ga(R, E1.numantino(k % 2, "enojo"), CI["numancia"], t_num + 0.15 * k, t_final, s=0.36, off=(dx, 40), sem=36 + k, zs=0.4, z=2, snd=("pop", 0.4))
    for k, (dx, dy) in enumerate(((-300, 140), (300, 130), (-330, -40), (340, -60))):
        ga(R, E1.legionario(k % 2), CI["numancia"], t_sit + 0.1 * k, t_final, s=0.34, off=(dx, dy), sem=40 + k, zs=0.4, z=2, flip=dx > 0, snd=("clink", 0.3))
    for k, dx in enumerate((-60, 70)):
        ga(R, lambda t, k=k: A.llama(int(t * 8) + k), CI["numancia"], t_morir - 0.2, t_final, s=0.5, off=(dx * 2.6, 60), sem=44 + k, zs=0.4, z=1, snd=("fuego", 0.4))
    # Hispania romana: calzadas, acueducto, teatro, latín
    lugar(R, t_final, t_calz - 0.1, "HISPANIA", (-3.8, 40.0), off=(0, 0), px=110)
    R.snd(t_final, "fanfarria", 0.4)
    R.ruta(M.RUTAS["via_augusta"], t_calz - 0.1, 1.4, ancho=5.5, t1=t_le)
    R.ruta(M.RUTAS["via_plata"], t_calz + 0.1, 1.2, ancho=5.5, t1=t_le)
    R.snd(t_calz, "pasos", 0.4, dur=1.0)
    lugar(R, t_calz + 0.3, t_le - 0.2, "VÍA AUGUSTA", (-1.6, 38.6), off=(0, -40), px=34)
    ga(R, E1.acueducto(), CI["segovia"], t_acue - 0.1, t_le, s=0.55, off=(0, 10), sem=46, z=2, snd=("crece", 0.5), entra="pluma", d_in=0.7)
    lugar(R, t_acue + 0.2, t_le - 0.6, "SEGOVIA", CI["segovia"], off=(0, 40), px=36)
    ga(R, E1.teatro_romano(), CI["merida"], t_teat - 0.1, t_le, s=0.52, off=(0, 20), sem=47, z=2, snd=("crece", 0.5), entra="pluma", d_in=0.7)
    lugar(R, t_teat + 0.2, t_le - 0.2, "MÉRIDA", CI["merida"], off=(0, 60), px=36)
    R.texto(t_latin - 0.1, t_le - 0.3, "LATÍN", (720, 990), px=86, d=0.4)
    pa(R, Bb.flecha(), 970, 985, 0.62, t_abue - 0.1, t_le - 0.3, sem=52, snd=("pop", 0.3))      # la fuente no tiene «→»
    R.texto(t_espa - 0.1, t_le - 0.3, "ESPAÑOL", (1210, 990), px=86, d=0.4)
    R.snd(t_latin, "escribir", 0.45, dur=0.5)
    R.snd(t_espa, "escribir", 0.45, dur=0.6)
    # Trajano y Adriano, de Itálica
    ciudad(R, t_le, FIN(e) + 0.4, "italica", "ITÁLICA", "abajo", 48)
    pa(R, E1.emperador_romano(0, "serio"), 640, 960, 1.15, t_tra - 0.15, FIN(e) + 0.5, sem=48, extra=[(0.1, "fanfarria", 0.4)])
    pa(R, E1.emperador_romano(1, "feliz"), 1290, 960, 1.15, t_adr - 0.15, FIN(e) + 0.5, sem=49, flip=True)
    R.texto(t_tra, FIN(e) + 0.4, "TRAJANO", (640, 560), px=64, d=0.5)
    R.texto(t_adr, FIN(e) + 0.4, "ADRIANO", (1290, 560), px=64, d=0.5)
    titulo(R, t_emp - 0.1, FIN(e) + 0.3, "EMPERADORES HISPANOS", px=70)
