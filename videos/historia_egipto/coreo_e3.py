# -*- coding: utf-8 -*-
"""Coreografía (3/3): Cleopatra, conquista islámica, era moderna, siglo XX y cierre."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402

COL = M.COL
CIU = M.CIUDADES


def lugar(R, t0, t1, txt, geo, off=(0, -60), px=52, d=0.5):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def construir(R):
    _cleopatra(R)
    _islam(R)
    _modernidad(R)
    _siglo20(R)
    _cierre(R)


# ------------------------------------------------------------------ 10. CLEOPATRA Y ROMA
def _cleopatra(R):
    e = "cleopatra"
    i0 = INI(e)
    t_ultima = T(e, "ultima")
    t_cleopatra = T(e, "cleopatra")
    t_cesar = T(e, "cesar")
    t_antonio = T(e, "antonio")
    t_accio = T(e, "accio")
    t_octavio = T(e, "octavio")
    t_muerte = T(e, "muerte")
    t_romano = T(e, "romano")

    # De reino ptolemaico a provincia romana
    R.terreno(i0 - 0.2, "ptolomeo", COL["ptolomeo"], 1.2)
    R.terreno(t_romano - 0.2, "unificado", COL["romano"], 1.4)

    R.camara(i0 - 0.2, 30.2, 31.0, 3.8)
    R.camara(t_cleopatra - 0.2, 29.92, 31.15, 4.8) # Alejandría
    R.camara(t_accio - 0.2, 28.5, 33.2, 3.6)       # Mar Mediterráneo hacia Grecia
    R.camara(t_romano - 0.2, 31.2, 29.0, 3.0)

    R.anio(i0, -51)
    R.anio(t_accio, -31)
    R.anio(t_romano, -30)

    # Sello: Provincia Romana
    R.sello(t_romano, "SPQR", "PROVINCIA ROMANA", COL["romano"])

    # Cleopatra VII en su trono dorado
    R.act(C.cleopatra_trono(), geo=CIU["alejandria"], off=(-60, 30), s=0.55,
          t_in=t_cleopatra - 0.2, d_in=0.5, entra="pop", sem=190,
          sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.5)], t_out=t_accio - 0.2, sale="encoger", z=2)
    lugar(R, t_cleopatra, t_accio - 0.3, "CLEOPATRA VII (ÚLTIMO FARAÓN)", CIU["alejandria"], off=(-60, -170), px=50)

    # Julio César y Marco Antonio (legionario romano con scutum y penacho)
    R.act(personaje_egipcio("guerrero", corona="casco_romano", piel=PIEL_CL, mirada=-1.0, cetro=False),
          geo=CIU["alejandria"], off=(80, 40), s=0.52,
          t_in=t_cesar - 0.2, d_in=0.5, entra="pop", sem=191,
          sfx=[(0, "pop", 0.5)], t_out=t_accio - 0.2, sale="encoger", z=2)
    lugar(R, t_cesar, t_accio - 0.3, "ALIANZA CON ROMA", CIU["alejandria"], off=(80, -160), px=48)

    # Batalla de Accio: galera de guerra romana con espolón de bronce
    R.act(C.galera_romana(), geo=(28.5, 33.5), off=(0, 20), s=0.54,
          t_in=t_accio - 0.3, d_in=0.6, entra="pop", sem=192,
          sfx=[(0, "pop", 0.5), (0.2, "tambor", 0.6)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_accio, FIN(e), "BATALLA DE ACCIO (31 a.C.)", (28.5, 33.5), off=(0, 120), px=46)


# ------------------------------------------------------------------ 11. ISLAM (Conquista árabe, Saladino y Mamelucos)
def _islam(R):
    e = "islam"
    i0 = INI(e)
    t_seiscientos = T(e, "seiscientos")
    t_arabe = T(e, "arabe")
    t_cairo = T(e, "cairo")
    t_medieval = T(e, "medieval")
    t_saladino = T(e, "saladino")
    t_ciudadela = T(e, "ciudadela")
    t_mamelucos = T(e, "mamelucos")
    t_mongoles = T(e, "mongoles")

    R.terreno(i0 - 0.2, "unificado", COL["islam"], 1.3)
    R.camara(i0 - 0.2, 31.5, 29.5, 3.2)
    R.camara(t_cairo - 0.2, 31.24, 30.05, 4.4)    # El Cairo
    R.camara(t_ciudadela - 0.2, 31.24, 30.05, 4.8)# Ciudadela
    R.camara(t_mongoles - 0.2, 33.5, 31.5, 3.8)   # Camino a Ain Yalut

    R.anio(i0, 641)
    R.anio(t_cairo, 969)
    R.anio(t_saladino, 1171)
    R.anio(t_mongoles, 1260)

    # Sello: Conquista árabe / Califato
    R.sello(t_arabe, "CALIF", "ERA ISLÁMICA", COL["islam"])

    # Conquista árabe: guerrero con turbante y espada curva
    R.act(personaje_egipcio("guerrero", corona="turbante", mirada=1.0, cetro=False),
          geo=CIU["el_cairo"], off=(-90, 40), s=0.52,
          t_in=t_arabe - 0.2, d_in=0.5, entra="pop", sem=201,
          sfx=[(0, "pop", 0.5), (0.1, "cuerno", 0.5)], t_out=t_saladino - 0.2, sale="encoger", z=2)
    lugar(R, t_arabe, t_saladino - 0.3, "CONQUISTA ÁRABE (641 d.C.)", CIU["el_cairo"], off=(-90, -160), px=50)

    # La Ciudadela de Saladino en El Cairo
    R.act(C.ciudadela_saladino(), geo=CIU["el_cairo"], off=(0, 30), s=0.55,
          t_in=t_ciudadela - 0.3, d_in=0.6, entra="pop", sem=202,
          sfx=[(0, "pop", 0.5), (0.2, "fanfarria", 0.6)], t_out=t_mamelucos - 0.2, sale="encoger", z=1)
    lugar(R, t_ciudadela, t_mamelucos - 0.3, "LA CIUDADELA DE SALADINO", CIU["el_cairo"], off=(0, -170), px=48)

    # Los guerreros mamelucos que detienen a los mongoles en Ain Yalut (1260)
    R.act(personaje_egipcio("guerrero", corona="turbante", piel=(195, 130, 90), mirada=1.0, cetro=False),
          geo=(34.5, 32.2), off=(0, 40), s=0.54,
          t_in=t_mamelucos - 0.2, d_in=0.5, entra="pop", sem=203,
          sfx=[(0, "pop", 0.5), (0.1, "golpe_suave", 0.5)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_mongoles, FIN(e), "MAMELUCOS: BATALLA DE AIN YALUT (1260)", (34.5, 32.2), off=(0, -160), px=50)


# ------------------------------------------------------------------ 12. MODERNIDAD (Napoleón, Champollion y Suez)
def _modernidad(R):
    e = "modernidad"
    i0 = INI(e)
    t_setecientos = T(e, "setecientos")
    t_napoleon = T(e, "napoleon")
    t_rosetta = T(e, "rosetta")
    t_descifrar = T(e, "descifrar")
    t_mehmet = T(e, "mehmet")
    t_agricultura = T(e, "agricultura")
    t_ochocientos = T(e, "ochocientos")
    t_suez = T(e, "suez")
    t_rutas = T(e, "rutas")

    R.terreno(i0 - 0.2, "unificado", COL["moderno"], 1.3)
    R.camara(i0 - 0.2, 31.0, 31.0, 3.5)
    R.camara(t_rosetta - 0.2, 30.42, 31.40, 4.8)    # Rosetta / Rashid
    R.camara(t_mehmet - 0.2, 31.24, 30.05, 4.2)     # El Cairo moderno
    R.camara(t_suez - 0.2, 32.55, 30.20, 4.4)       # Istmo de Suez
    R.camara(FIN(e), 32.55, 30.0, 3.8)

    R.anio(i0, 1798)
    R.anio(t_descifrar, 1822)
    R.anio(t_mehmet, 1805)
    R.anio(t_suez, 1869)

    # Sello: Canal de Suez
    R.sello(t_suez, "SUEZ", "CANAL DE SUEZ", COL["moderno"])

    # Piedra de Rosetta y la lupa descifradora de Champollion
    R.act(C.piedra_rosetta(), geo=CIU["rosetta"], off=(0, 20), s=0.52,
          t_in=t_rosetta - 0.3, d_in=0.6, entra="pop", sem=211,
          sfx=[(0, "pop", 0.5), (0.1, "escribir", 0.6)], t_out=t_mehmet - 0.2, sale="encoger", z=2)
    lugar(R, t_rosetta, t_mehmet - 0.3, "PIEDRA DE ROSETTA (CHAMPOLLION, 1822)", CIU["rosetta"], off=(0, -170), px=48)

    # Mehmet Alí modernizando Egipto
    R.act(personaje_egipcio("faraon", corona="turbante", mirada=1.0),
          geo=CIU["el_cairo"], off=(-80, 50), s=0.52,
          t_in=t_mehmet - 0.2, d_in=0.5, entra="pop", sem=212,
          sfx=[(0, "pop", 0.5)], t_out=t_suez - 0.2, sale="encoger", z=2)
    lugar(R, t_mehmet, t_suez - 0.3, "MEHMET ALÍ (MODERNIZACIÓN)", CIU["el_cairo"], off=(-80, -180), px=48)

    # Barco de vapor cruzando el Canal de Suez recién inaugurado
    R.act(C.barco_vapor_suez(), geo=CIU["suez"], off=(0, 20), s=0.55,
          t_in=t_suez - 0.3, d_in=0.6, entra="pop", sem=213,
          sfx=[(0, "cuerno", 0.6), (0.1, "ola", 0.5)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_suez, FIN(e), "CANAL DE SUEZ (1869)", CIU["suez"], off=(0, -170), px=52)


# ------------------------------------------------------------------ 13. SIGLO XX Y PRESENTE
def _siglo20(R):
    e = "siglo20"
    i0 = INI(e)
    t_protectorado = T(e, "protectorado")
    t_independencia = T(e, "independencia")
    t_republica = T(e, "republica")
    t_nacionaliza = T(e, "nacionaliza")
    t_asuan = T(e, "asuan")
    t_crecidas = T(e, "crecidas")
    t_millones = T(e, "millones")
    t_piramides = T(e, "piramides")

    R.terreno(i0 - 0.2, "unificado", COL["moderno"], 1.2)
    R.camara(i0 - 0.2, 31.5, 29.0, 3.2)
    R.camara(t_asuan - 0.2, 32.89, 24.09, 4.8)    # Asuán
    R.camara(t_millones - 0.2, 31.2, 28.5, 2.6)   # Todo Egipto
    R.camara(t_piramides - 0.2, 31.13, 29.98, 4.0)# Guiza

    R.anio(i0, 1922)
    R.anio(t_republica, 1952)
    R.anio(t_asuan, 1970)
    R.anio(t_piramides, 2026)

    # Sello: República de Egipto
    R.sello(t_republica, "EGY", "REPÚBLICA DE EGIPTO", COL["moderno"])

    # La Presa de Asuán domesticando para siempre las crecidas del Nilo
    R.act(C.presa_asuan(), geo=CIU["asuan"], off=(0, 20), s=0.58,
          t_in=t_asuan - 0.3, d_in=0.6, entra="pop", sem=221,
          sfx=[(0, "pop", 0.5), (0.2, "ola", 0.6)], t_out=t_millones - 0.2, sale="encoger", z=1)
    lugar(R, t_asuan, t_millones - 0.3, "GRAN PRESA DE ASUÁN (1970)", CIU["asuan"], off=(0, -170), px=54)

    # Más de 105 millones de personas
    R.texto(t_millones - 0.1, t_piramides - 0.2, "+105 MILLONES DE HABITANTES", (960, 230), px=84, d=0.8)
    R.snd(t_millones, "escribir", 0.5, dur=0.8)

    # Las pirámides y la esfinge siguen erguidas tras 5.000 años de historia
    R.act(A.gran_piramide_guiza(), geo=CIU["guiza"], off=(-60, 20), s=0.58,
          t_in=t_piramides - 0.2, d_in=0.6, entra="pop", sem=222,
          sfx=[(0, "pop", 0.5), (0.2, "brillo", 0.6)], t_out=FIN(e), sale="encoger", z=1)
    R.act(A.gran_esfinge(), geo=CIU["guiza"], off=(80, 45), s=0.48,
          t_in=t_piramides, d_in=0.5, entra="pop", sem=223,
          sfx=[(0, "pop", 0.4)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_piramides, FIN(e), "5.000 AÑOS DE HISTORIA", CIU["guiza"], off=(0, -180), px=56)


# ------------------------------------------------------------------ 14. CIERRE (Outro)
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_faraones = T(e, "faraones")
    t_civilizacion = T(e, "civilizacion")
    t_sagrado = T(e, "sagrado")
    t_comentarios = T(e, "comentarios")

    R.camara(i0 - 0.2, 31.2, 28.0, 2.4)
    R.camara(t_comentarios - 0.2, 31.2, 28.5, 2.8)
    R.camara(FIN(e), 31.2, 28.5, 3.0)

    R.anio(i0, 2026)

    # La barca de papiro sobre el río eterno y la pirámide al fondo
    R.act(A.barca_papiro(), geo=(31.8, 27.5), off=(0, 20), s=0.55,
          t_in=t_sagrado - 0.2, d_in=0.6, entra="pop", sem=231,
          sfx=[(0, "ola", 0.5)], t_out=FIN(e) + 1.0, sale="encoger", z=2)

    # Llamada a los comentarios
    R.texto(t_comentarios - 0.1, FIN(e) + 1.0, "¿QUÉ HISTORIA QUIERES VER?", (960, 240), px=78, d=0.8)
    R.texto(t_comentarios + 0.6, FIN(e) + 1.0, "DÍMELO EN LOS COMENTARIOS", (960, 360), px=66, d=0.8)
    R.snd(t_comentarios, "escribir", 0.5, dur=0.8)
