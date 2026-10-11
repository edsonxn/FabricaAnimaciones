# -*- coding: utf-8 -*-
"""Coreografía parte 2/3: Guerras Púnicas, Mare Nostrum, Julio César y Pax Romana."""
import math
import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_roma as RO
from obj_roma import *
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402

COL = M.COL


def pop(R, dib, t, pos=None, geo=None, off=(0, 0), s=1.0, snd="pop", vol=0.6, **k):
    sfx = [(0.0, snd, vol)] if snd else []
    if pos is not None:
        return R.act(dib, pos=pos, t_in=t, sfx=sfx, s=s, **k)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t, sfx=sfx, **k)


def lugar(R, t0, t1, txt, geo, off=(0, -55), px=52, d=0.5):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def construir(R):
    _cartago(R)
    _mediterraneo(R)
    _cesar(R)
    _imperio(R)


# ------------------------------------------------------------------ 5. CARTAGO (Guerras Púnicas)
def _cartago(R):
    e = "cartago"
    i0 = INI(e)
    t_mar = T(e, "mediterráneo")
    t_cartago = T(e, "cartago")
    t_choque = T(e, "choque")
    t_anibal = T(e, "aníbal")
    t_alpes = T(e, "alpes")
    t_elefantes = T(e, "elefantes")
    t_abismo = T(e, "abismo")
    t_escipion = T(e, "escipión")
    t_africa = T(e, "áfrica")
    t_cenizas = T(e, "cenizas")

    R.camara(i0, 13.8, 40.8, 1.5)
    R.camara(t_cartago, 11.5, 38.0, 1.5)
    R.camara(t_anibal, 8.5, 43.5, 1.65)
    R.camara(t_escipion, 10.5, 36.8, 1.7)
    R.camara(FIN(e), 11.5, 37.5, 1.5)

    # Territorio de Cartago en azul púnico
    R.terreno(t_cartago - 0.2, "cartago", COL["cartago"], 1.4)
    lugar(R, t_cartago, FIN(e) + 0.4, "CARTAGO", (10.32, 36.85), off=(0, 45), px=60)
    lugar(R, t_cartago, FIN(e) + 0.4, "ROMA", (12.49, 41.90), off=(0, -45), px=56)

    # Combate naval en el Mediterráneo: 2 trirremes con remos sincronizados
    pop(R, lambda t: RO.galera_romana(int(t * 5)), t_mar + 0.2, pos=(1380, 720), s=0.88, sem=50, snd="whoosh", t_out=t_anibal - 0.1, sale="encoger")
    pop(R, lambda t: RO.galera_romana(int(t * 5) + 2), t_mar + 0.4, pos=(1080, 750), s=0.75, sem=51, t_out=t_anibal - 0.1, sale="encoger")

    # Aníbal cruza los Alpes con elefantes de guerra
    lugar(R, t_alpes, t_escipion - 0.1, "LOS ALPES", (8.0, 45.5), off=(0, -45), px=54)
    pop(R, RO.elefante_anibal, t_elefantes - 0.2, geo=(7.5, 45.2), off=(-30, 20), s=0.82, sem=52, snd="impacto", t_out=t_escipion - 0.1, sale="encoger")
    pop(R, RO.elefante_anibal, t_elefantes + 0.2, geo=(8.8, 44.8), off=(40, 20), s=0.72, sem=53, t_out=t_escipion - 0.1, sale="encoger")

    # Batalla épica: choque de espadas en Cannas
    pop(R, A.espadas(), t_choque + 0.1, geo=(16.1, 41.3), off=(0, 0), s=0.85, sem=54, snd="espada", vol=0.7, t_out=t_escipion - 0.1, sale="encoger")
    lugar(R, t_choque, t_escipion - 0.1, "BATALLA DE CANNAS", (16.1, 41.3), off=(0, 50), px=48)

    # Escipión contraataca en Zama y destruye Cartago
    R.terreno(t_escipion, "punicas", COL["punicas"], 1.8)
    R.snd(t_escipion, "fanfarria", 0.65)
    lugar(R, t_escipion, FIN(e) + 0.4, "BATALLA DE ZAMA (202 a. C.)", (9.8, 35.8), off=(0, 45), px=52)

    # Llamas sobre Cartago reducida a cenizas
    for f in range(3):
        R.act(lambda t, f=f: A.llama(int(t * 8) + f), geo=(10.32, 36.85), off=(-25 + 25 * f, 10), s=0.65,
              t_in=t_cenizas + 0.1 * f, d_in=0.3, entra="pop", sem=56 + f, t_out=FIN(e) + 0.4, sale="encoger")
    R.snd(t_cenizas, "crujido", 0.9, dur=1.2)
    R.texto(t_cenizas, FIN(e) + 0.4, "Cartago destruida (146 a. C.)", (960, 160), px=72, d=0.7)


# ------------------------------------------------------------------ 6. MARE NOSTRUM
def _mediterraneo(R):
    e = "mediterraneo"
    i0 = INI(e)
    t_detener = T(e, "detener")
    t_grecia = T(e, "grecia")
    t_macedonia = T(e, "macedonia")
    t_hispania = T(e, "hispania")
    t_asia = T(e, "asia")
    t_mare = T(e, "mare")
    t_nostrum = T(e, "nostrum")
    t_mar = T(e, "mar")

    R.camara(i0, 11.5, 37.5, 1.5)
    R.camara(t_grecia, 18.0, 39.0, 1.38)
    R.camara(t_asia, 24.0, 38.0, 1.32)
    R.camara(t_mar, 16.5, 38.5, 1.25)
    R.camara(FIN(e), 16.0, 39.0, 1.25)

    # El territorio romano envuelve la cuenca del Mediterráneo
    R.terreno(t_detener, "mediterraneo", COL["mediterraneo"], 2.4)
    R.snd(t_detener, "brillo", 0.7)

    # Nombres de las provincias conquistadas sobre el mapa
    lugar(R, t_macedonia - 0.1, FIN(e) + 0.4, "MACEDONIA", (22.0, 41.5), off=(0, -25), px=46)
    lugar(R, t_grecia - 0.1, FIN(e) + 0.4, "GRECIA", (22.5, 38.0), off=(0, -55), px=48)
    lugar(R, t_hispania - 0.1, FIN(e) + 0.4, "HISPANIA", (-4.0, 40.0), off=(0, 0), px=60)
    lugar(R, t_asia - 0.1, FIN(e) + 0.4, "ASIA MENOR", (32.5, 39.0), off=(0, -45), px=50)

    # Monumentos y riquezas en las provincias
    pop(R, RO.templo_romano, t_grecia + 0.1, geo=(22.5, 38.0), off=(0, 20), s=0.40, sem=60, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.anfora_vino, t_hispania + 0.1, geo=(-2.5, 38.5), off=(0, 20), s=0.55, sem=61, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.moneda_denario, t_asia + 0.1, geo=(32.5, 38.5), off=(0, 25), s=0.52, sem=62, snd="ding", t_out=FIN(e) + 0.4, sale="encoger")

    # Barcos mercantes cruzando el mar abierto
    pop(R, lambda t: RO.barco_mercante(int(t * 4)), t_detener + 0.2, geo=(14.0, 36.5), off=(0, 0), s=0.62, sem=64, snd="whoosh", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, lambda t: RO.galera_romana(int(t * 4)), t_detener + 0.5, geo=(18.5, 35.0), off=(0, 0), s=0.60, sem=65, t_out=FIN(e) + 0.4, sale="encoger")

    # Gran rótulo majestuoso "MARE NOSTRUM"
    R.texto(t_mare - 0.1, FIN(e) + 0.4, "M A R E   N O S T R U M", (960, 480), px=92, d=0.8)
    R.texto(t_mar, FIN(e) + 0.4, "«Nuestro Mar»", (960, 555), px=58, d=0.6)
    R.snd(t_mare, "escribir", 0.6, dur=1.2)


# ------------------------------------------------------------------ 7. JULIO CÉSAR
def _cesar(R):
    e = "cesar"
    i0 = INI(e)
    t_oro = T(e, "oro")
    t_desest = T(e, "desestabilizan")
    t_generales = T(e, "generales")
    t_mando = T(e, "mando")
    t_cesar = T(e, "césar")
    t_galias = T(e, "galias")
    t_rubicon = T(e, "rubicón")
    t_senado = T(e, "senado")
    t_dictador = T(e, "dictador")
    t_idus = T(e, "idus")
    t_marzo = T(e, "marzo")
    t_cuarenta = T(e, "cuarenta")
    t_asesinado = T(e, "asesinado")

    R.camara(i0, 16.0, 39.0, 1.25)
    R.camara(t_cesar, 4.5, 46.5, 1.6)
    R.camara(t_rubicon, 12.0, 44.2, 2.0)
    R.camara(t_senado, 12.49, 41.90, 2.5)
    R.camara(FIN(e), 12.6, 41.8, 2.0)

    # Campañas de las Galias
    R.terreno(t_galias - 0.2, "cesar", COL["cesar"], 1.8)
    lugar(R, t_galias, t_rubicon - 0.1, "LAS GALIAS", (3.0, 49.8), off=(0, -35), px=54)
    pop(R, RO.castrum_fort, t_galias + 0.1, geo=(1.8, 46.2), off=(0, 20), s=0.48, sem=70, snd="pop", t_out=t_rubicon - 0.1, sale="encoger")
    pop(R, RO.barbaro_german, t_galias + 0.3, geo=(5.8, 47.5), off=(0, 20), s=0.52, sem=71, snd="impacto", t_out=t_rubicon - 0.1, sale="encoger")

    # Julio César al frente de sus legiones
    pop(R, RO.cesar_emperador, t_cesar, pos=(420, 720), s=0.96, sem=72, snd="fanfarria", t_out=t_idus + 0.3, sale="encoger")

    # Cruce del Rubicón ("Alea iacta est")
    R.anio(t_rubicon - 0.2, -49)
    lugar(R, t_rubicon, t_senado, "RÍO RUBICÓN", (12.3, 44.1), off=(0, -40), px=54)
    R.texto(t_rubicon + 0.2, t_senado + 0.3, "«Alea iacta est»", (960, 200), px=72, d=0.6)
    R.snd(t_rubicon, "whoosh", 0.6)

    # Dictador perpetuo
    pop(R, RO.moneda_denario, t_dictador - 0.2, pos=(1460, 680), s=0.9, sem=74, snd="ding", t_out=t_idus + 0.3, sale="encoger")

    # Los Idus de Marzo (15 de marzo del 44 a.C.): traición en el Senado
    R.anio(t_idus, -44)
    R.act(A.rayo(), pos=(960, 480, 1.2), t_in=t_idus, d_in=0.15, entra="fija", sem=75, z=4, t_out=t_idus + 0.3, sale="cortar",
          sfx=[(0, "trueno", 0.9), (0, "espada", 0.8)])
    pop(R, A.espadas(), t_asesinado - 0.1, pos=(960, 680), s=1.1, sem=76, snd="impacto", vol=0.8, t_out=FIN(e) + 0.5, sale="encoger")
    R.texto(t_idus, FIN(e) + 0.5, "Idus de Marzo (15-Mar-44 a. C.)", (960, 160), px=78, d=0.7)


# ------------------------------------------------------------------ 8. IMPERIO (Augusto y Pax Romana)
def _imperio(R):
    e = "imperio"
    i0 = INI(e)
    t_salvarse = T(e, "salvarse")
    t_civil = T(e, "guerra")
    t_octavio = T(e, "octavio")
    t_augusto = T(e, "augusto")
    t_emperador = T(e, "emperador")
    t_pax = T(e, "pax")
    t_romana = T(e, "romana")
    t_siglos = T(e, "siglos")
    t_orden = T(e, "orden")
    t_acueductos = T(e, "acueductos")
    t_coliseo = T(e, "coliseo")

    R.camara(i0, 12.6, 41.8, 2.0)
    R.camara(t_augusto, 14.0, 40.5, 1.6)
    R.camara(t_pax, 15.0, 39.5, 1.4)
    R.camara(t_coliseo, 13.5, 41.0, 1.65)
    R.camara(FIN(e), 13.8, 41.2, 1.55)

    # Fundación del Imperio: 27 a.C.
    R.anio(t_augusto, -27)
    R.snd(t_augusto, "fanfarria", 0.7)

    # Anexión de Egipto y consolidación del Mediterráneo
    R.terreno(t_augusto - 0.2, "imperio", COL["imperio"], 2.0)
    lugar(R, t_augusto + 0.3, FIN(e) + 0.5, "EGIPTO ROMANO", (31.0, 27.0), off=(0, 0), px=54)

    # Primer Emperador Augusto con corona triunfal
    augusto = pop(R, RO.cesar_emperador, t_emperador - 0.1, pos=(380, 720), s=0.98, sem=80, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")
    pop(R, RO.corona_laurel, t_emperador + 0.2, pos=(380, 440), s=0.75, sem=81, snd="brillo", t_out=FIN(e) + 0.5, sale="encoger")

    # Arquitectura monumental de la Pax Romana: Coliseo, Acueducto y Arco de Triunfo
    pop(R, RO.coliseo, t_coliseo - 0.4, pos=(1480, 680), s=0.88, sem=82, snd="impacto", t_out=FIN(e) + 0.5, sale="encoger")
    pop(R, RO.acueducto, t_acueductos - 0.3, pos=(960, 720), s=0.88, sem=83, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")
    pop(R, RO.arco_triunfo, t_orden, geo=(12.49, 41.89), off=(0, 20), s=0.55, sem=84, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")

    # Título dorado Pax Romana
    R.texto(t_pax - 0.1, FIN(e) + 0.5, "P A X   R O M A N A", (960, 160), px=102, d=0.8)
    R.texto(t_siglos, FIN(e) + 0.5, "Dos siglos de paz, leyes y monumentos", (960, 245), px=66, d=0.6)
    R.snd(t_pax, "brillo", 0.75)
