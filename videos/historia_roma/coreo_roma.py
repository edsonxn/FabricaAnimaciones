# -*- coding: utf-8 -*-
"""Coreografía completa de «La historia de Roma en 5 minutos» (12 escenas continuas)."""
import math

import numpy as np

import mapa as M
import obj_roma as RO
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402

COL = M.COL


def pop(R, dib, t, pos=None, geo=None, off=(0, 0), s=1.0, snd="pop", vol=0.6, **k):
    sfx = [(0.0, snd, vol)] if snd else []
    if pos is not None:
        return R.act(dib, pos=pos, t_in=t, sfx=sfx, s=s, **k)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t, sfx=sfx, **k)


def construir(R):
    _gancho(R)
    _origenes(R)
    _republica(R)
    _italia(R)
    _cartago(R)
    _mediterraneo(R)
    _cesar(R)
    _imperio(R)
    _maxima(R)
    _crisis(R)
    _division(R)
    _caida(R)


# ------------------------------------------------------------------ 1. GANCHO
def _gancho(R):
    e = "gancho"
    t_aldea = T(e, "pequeña")
    t_mundo = T(e, "mundo")
    t_tres = T(e, "tres")
    t_historia = T(e, "historia")
    t_roma = T(e, "roma")

    R.camara(0.0, 15.0, 40.0, 1.15)
    R.camara(t_mundo, 14.0, 41.0, 1.25)
    R.camara(FIN(e), 13.5, 41.5, 1.35)

    R.terreno(t_aldea, "lacio", COL["lacio"], 1.0)
    R.terreno(t_mundo, "maxima", COL["maxima"], 1.8)

    R.snd(t_aldea, "pop", 0.6)
    R.snd(t_mundo, "brillo", 0.7)
    R.snd(t_historia, "escribir", 0.6, dur=0.9)

    R.texto(t_historia - 0.05, FIN(e) + 0.8, "LA HISTORIA DE ROMA", (960, 160), px=110, d=0.8)
    R.texto(t_roma + 0.3, FIN(e) + 0.8, "en 5 minutos", (960, 265), px=76, d=0.6)
    pop(R, RO.estandarte_spqr, t_roma + 0.4, pos=(960, 680), s=0.85, snd="impacto", t_out=FIN(e) + 0.6)


# ------------------------------------------------------------------ 2. ORÍGENES
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_753 = T(e, "setecientos")
    t_tiber = T(e, "tíber")
    t_pastores = T(e, "pastores")
    t_colinas = T(e, "colinas")
    t_nace = T(e, "nace")

    R.terreno(i0 - 0.4, "lacio", COL["lacio"], 1.0)
    R.camara(i0, 13.5, 41.5, 1.35)
    R.camara(t_tiber, 12.5, 41.9, 2.8)
    R.camara(t_colinas, 12.5, 41.9, 3.2)
    R.camara(FIN(e), 12.5, 41.9, 2.9)

    R.rio(M.RIO_TIBER, t_tiber, 1.8, color=(130, 185, 215), ancho=18)
    R.anio(t_753, -753)

    R.snd(t_tiber, "whoosh", 0.5)
    pop(R, RO.choza_lacio, t_colinas, pos=(960, 620), s=0.95, snd="pop", t_out=FIN(e) + 0.4)
    R.texto(t_nace, FIN(e) + 0.4, "Roma: 753 a. C.", (960, 180), px=68, d=0.6)


# ------------------------------------------------------------------ 3. REPÚBLICA
def _republica(R):
    e = "republica"
    i0 = INI(e)
    t_509 = T(e, "quinientos")
    t_republica = T(e, "república")
    t_senado = T(e, "senado")
    t_spqr = T(e, "pe")

    R.camara(i0, 12.5, 41.9, 2.9)
    R.camara(t_republica, 12.8, 42.0, 2.3)
    R.camara(FIN(e), 13.0, 42.0, 2.1)

    R.anio(t_509, -509)
    R.snd(t_republica, "impacto", 0.6)

    pop(R, RO.senador, t_senado - 0.2, pos=(1380, 680), s=0.9, snd="pop", t_out=FIN(e) + 0.5)
    pop(R, RO.estandarte_spqr, t_spqr - 0.1, pos=(540, 680), s=0.85, snd="impacto", t_out=FIN(e) + 0.5)
    R.texto(t_spqr - 0.1, FIN(e) + 0.5, "S · P · Q · R", (960, 180), px=92, d=0.6)


# ------------------------------------------------------------------ 4. ITALIA
def _italia(R):
    e = "italia"
    i0 = INI(e)
    t_pelear = T(e, "pelear")
    t_samnitas = T(e, "samnitas")
    t_via = T(e, "vía")
    t_onda = T(e, "ondea")

    R.camara(i0, 13.0, 42.0, 2.1)
    R.camara(t_samnitas, 13.5, 41.2, 1.85)
    R.camara(t_onda, 14.0, 40.5, 1.7)
    R.camara(FIN(e), 14.0, 40.5, 1.65)

    R.terreno(t_samnitas, "italia", COL["italia"], 1.8)
    R.ruta(M.VIA_APIA, t_via, 1.8, ancho=4.5)
    R.snd(t_via, "escribir", 0.5)

    pop(R, lambda t: RO.legionario(int(t * 3)), t_pelear, pos=(480, 680), s=0.9, snd="pop", t_out=FIN(e) + 0.4)
    R.texto(t_onda, FIN(e) + 0.4, "Italia romana", (960, 180), px=74, d=0.6)


# ------------------------------------------------------------------ 5. CARTAGO
def _cartago(R):
    e = "cartago"
    i0 = INI(e)
    t_mar = T(e, "mediterráneo")
    t_anibal = T(e, "aníbal")
    t_elefantes = T(e, "elefantes")
    t_escipion = T(e, "escipión")
    t_cenizas = T(e, "cenizas")

    R.camara(i0, 14.0, 40.5, 1.65)
    R.camara(t_mar, 11.5, 38.5, 1.55)
    R.camara(t_anibal, 8.5, 43.5, 1.6)
    R.camara(t_escipion, 10.5, 36.5, 1.7)
    R.camara(FIN(e), 11.0, 37.5, 1.55)

    R.terreno(t_mar, "cartago", COL["cartago"], 1.2)
    R.terreno(t_cenizas, "punicas", COL["punicas"], 1.6)

    pop(R, RO.elefante_anibal, t_elefantes - 0.2, pos=(540, 520), s=0.85, snd="impacto", t_out=t_escipion + 0.2)
    pop(R, RO.galera_romana, t_mar + 0.3, pos=(1350, 720), s=0.85, snd="whoosh", t_out=FIN(e) + 0.4)
    R.snd(t_cenizas, "impacto", 0.7)
    R.texto(t_cenizas, FIN(e) + 0.4, "Victoria sobre Cartago (146 a. C.)", (960, 180), px=66, d=0.6)


# ------------------------------------------------------------------ 6. MARE NOSTRUM
def _mediterraneo(R):
    e = "mediterraneo"
    i0 = INI(e)
    t_detener = T(e, "detener")
    t_grecia = T(e, "grecia")
    t_mare = T(e, "mare")
    t_mar = T(e, "mar")

    R.camara(i0, 11.0, 37.5, 1.55)
    R.camara(t_grecia, 18.0, 38.5, 1.35)
    R.camara(t_mar, 18.0, 38.0, 1.3)
    R.camara(FIN(e), 17.0, 38.5, 1.3)

    R.terreno(t_grecia, "mediterraneo", COL["mediterraneo"], 2.2)
    R.snd(t_grecia, "brillo", 0.6)

    pop(R, RO.galera_romana, t_detener, pos=(960, 680), s=0.9, snd="whoosh", t_out=FIN(e) + 0.4)
    R.texto(t_mare - 0.1, FIN(e) + 0.4, "MARE NOSTRUM", (960, 520), px=100, d=0.8)


# ------------------------------------------------------------------ 7. CÉSAR
def _cesar(R):
    e = "cesar"
    i0 = INI(e)
    t_oro = T(e, "oro")
    t_galias = T(e, "galias")
    t_rubicon = T(e, "rubicón")
    t_idus = T(e, "idus")

    R.camara(i0, 17.0, 38.5, 1.3)
    R.camara(t_galias, 6.0, 46.0, 1.5)
    R.camara(t_rubicon, 12.0, 44.0, 1.7)
    R.camara(FIN(e), 12.5, 42.0, 1.6)

    R.terreno(t_galias, "cesar", COL["cesar"], 1.6)
    R.anio(t_idus, -44)

    pop(R, RO.cesar_emperador, t_rubicon - 0.2, pos=(1380, 660), s=0.95, snd="pop", t_out=FIN(e) + 0.4)
    R.snd(t_idus, "impacto", 0.8)
    R.texto(t_idus, FIN(e) + 0.4, "Idus de Marzo (44 a. C.)", (960, 180), px=72, d=0.6)


# ------------------------------------------------------------------ 8. IMPERIO
def _imperio(R):
    e = "imperio"
    i0 = INI(e)
    t_salvarse = T(e, "salvarse")
    t_augusto = T(e, "augusto")
    t_pax = T(e, "pax")
    t_coliseo = T(e, "coliseo")

    R.camara(i0, 12.5, 42.0, 1.6)
    R.camara(t_pax, 15.0, 39.0, 1.35)
    R.camara(FIN(e), 14.5, 40.0, 1.3)

    R.terreno(t_augusto, "imperio", COL["imperio"], 1.8)
    R.snd(t_pax, "brillo", 0.7)

    pop(R, RO.coliseo, t_coliseo - 0.4, pos=(540, 700), s=0.85, snd="impacto", t_out=FIN(e) + 0.5)
    pop(R, RO.acueducto, t_coliseo, pos=(1380, 700), s=0.85, snd="pop", t_out=FIN(e) + 0.5)
    R.texto(t_pax - 0.1, FIN(e) + 0.5, "PAX ROMANA", (960, 180), px=96, d=0.7)


# ------------------------------------------------------------------ 9. MÁXIMA EXTENSIÓN
def _maxima(R):
    e = "maxima"
    i0 = INI(e)
    t_117 = T(e, "ciento")
    t_trajano = T(e, "trajano")
    t_britania = T(e, "britania")
    t_eufrates = T(e, "éufrates")

    R.camara(i0, 14.5, 40.0, 1.3)
    R.camara(t_britania, -1.0, 52.0, 1.4)
    R.camara(t_eufrates, 36.0, 36.0, 1.4)
    R.camara(FIN(e), 17.0, 42.0, 1.2)

    R.terreno(t_trajano, "maxima", COL["maxima"], 2.2)
    R.anio(t_117, 117)
    R.snd(t_trajano, "brillo", 0.8)

    pop(R, RO.corona_laurel, t_trajano + 0.2, pos=(960, 340), s=1.1, snd="pop", t_out=FIN(e) + 0.5)
    R.texto(t_117, FIN(e) + 0.5, "Máxima Extensión: 117 d. C.", (960, 160), px=76, d=0.6)


# ------------------------------------------------------------------ 10. CRISIS
def _crisis(R):
    e = "crisis"
    i0 = INI(e)
    t_territorio = T(e, "territorio")
    t_tercero = T(e, "tercero")
    t_germanes = T(e, "pueblos")
    t_rin = T(e, "rin")

    R.camara(i0, 17.0, 42.0, 1.2)
    R.camara(t_rin, 12.0, 46.5, 1.5)
    R.camara(FIN(e), 14.0, 44.0, 1.35)

    R.rio(M.RIO_RIN, t_rin, 1.5, color=(160, 80, 80), ancho=16)
    R.rio(M.RIO_DANUBIO, t_rin + 0.3, 1.8, color=(160, 80, 80), ancho=16)

    R.romper("barbaros", t_tercero, t_tercero + 0.8, t_tercero + 2.4, t_tercero + 3.4, gap=18, deriva=36)
    R.snd(t_tercero, "crujido", 0.8)
    R.snd(t_germanes, "impacto", 0.7)

    R.texto(t_tercero, FIN(e) + 0.4, "Crisis del Siglo III", (960, 180), px=84, d=0.6)


# ------------------------------------------------------------------ 11. DIVISIÓN
def _division(R):
    e = "division"
    i0 = INI(e)
    t_dividir = T(e, "dividir")
    t_constantino = T(e, "constantino")
    t_oriente = T(e, "oriente")

    R.camara(i0, 14.0, 44.0, 1.35)
    R.camara(t_constantino, 27.0, 41.5, 1.5)
    R.camara(FIN(e), 20.0, 39.0, 1.25)

    R.terreno(t_dividir, "occidente", COL["occidente"], 1.6)
    R.snd(t_constantino, "brillo", 0.7)

    R.texto(t_dividir, FIN(e) + 0.4, "OCCIDENTE", (560, 420), px=78, d=0.6)
    R.texto(t_constantino, FIN(e) + 0.4, "ORIENTE (Constantinopla)", (1420, 420), px=72, d=0.6)


# ------------------------------------------------------------------ 12. CAÍDA Y LEGADO
def _caida(R):
    e = "caida"
    i0 = INI(e)
    t_476 = T(e, "cuatrocientos")
    t_colapsa = T(e, "colapsa")
    t_murió = T(e, "murió")
    t_vivos = T(e, "vivos")

    R.camara(i0, 20.0, 39.0, 1.25)
    R.camara(t_colapsa, 15.0, 40.0, 1.2)
    R.camara(FIN(e), 15.0, 40.0, 1.15)

    R.anio(t_476, 476)
    R.terreno(t_colapsa, "oriente", COL["oriente"], 2.0)
    R.snd(t_colapsa, "impacto", 0.7)

    pop(R, RO.estandarte_spqr, t_murió, pos=(620, 680), s=0.85, snd="pop")
    pop(R, RO.corona_laurel, t_vivos - 0.2, pos=(1320, 640), s=0.9, snd="brillo")
    R.texto(t_vivos - 0.2, FIN(e) + 1.0, "EL LEGADO DE ROMA", (960, 200), px=96, d=0.8)
