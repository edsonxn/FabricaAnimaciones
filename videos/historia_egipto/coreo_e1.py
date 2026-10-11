# -*- coding: utf-8 -*-
"""Coreografía (1/3): gancho, orígenes, pirámides, reino medio y reino nuevo."""
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
    _gancho(R)
    _origenes(R)
    _piramides(R)
    _intermedio1(R)
    _reino_nuevo(R)


# ------------------------------------------------------------------ 1. GANCHO
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_rio = T(e, "rio")
    t_desierto = T(e, "desierto")
    t_monumentos = T(e, "monumentos")
    t_tiempo = T(e, "tiempo")
    t_reyes = T(e, "reyes")
    t_dioses = T(e, "dioses")
    t_historia = T(e, "historia")
    t_egipto = T(e, "egipto")
    t_cinco = T(e, "cinco")

    # Terreno inicial: el Nilo verde y el desierto líbico
    R.terreno(i0 - 0.2, "unificado", COL["antiguo"], 1.5)
    R.camara(0.0, 31.2, 28.5, 2.0)
    R.camara(t_rio, 31.0, 29.5, 2.6)
    R.camara(t_monumentos, 31.13, 29.98, 4.0)
    R.camara(t_reyes, 31.25, 29.85, 3.8)
    R.camara(t_egipto, 31.2, 28.5, 2.8)
    R.camara(FIN(e), 31.2, 28.0, 2.6)

    # Contador de años: orígenes c. 3100 a. C.
    R.anio(0.0, -3100)
    R.anio(t_monumentos, -2600)
    R.anio(t_reyes, -2500)
    R.anio(t_egipto, -3100)

    # Monumentos eternos: la Gran Pirámide y la Esfinge asoman en el horizonte
    R.act(A.gran_piramide_guiza(), geo=CIU["guiza"], off=(0, 20), s=0.55,
          t_in=t_monumentos - 0.2, d_in=0.6, entra="pop", sem=101,
          sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.4)], t_out=t_historia - 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_monumentos, t_historia - 0.3, "PIRÁMIDES DE GUIZA", CIU["guiza"], off=(0, -180), px=56)

    R.act(A.gran_esfinge(), geo=CIU["guiza"], off=(110, 50), s=0.45,
          t_in=t_monumentos + 0.3, d_in=0.5, entra="pop", sem=102,
          sfx=[(0, "pop", 0.4)], t_out=t_historia - 0.3, sale="encoger", zs=0.5, z=2)

    # Faraón divino con la doble corona Pschent
    R.act(personaje_egipcio("faraon", corona="pschent", mirada=1.0), geo=CIU["menfis"], off=(-90, 40), s=0.52,
          t_in=t_reyes - 0.2, d_in=0.5, entra="pop", sem=103,
          sfx=[(0, "pop", 0.5), (0.1, "fanfarria", 0.5)], t_out=t_historia - 0.3, sale="encoger", zs=0.6, z=2)
    lugar(R, t_reyes, t_historia - 0.3, "EL FARAÓN DIOS", CIU["menfis"], off=(-90, -160), px=54)

    # Título grande del video
    R.texto(t_egipto - 0.3, FIN(e) + 0.8, "EGIPTO", (960, 220), px=155, d=0.9)
    R.texto(t_cinco - 0.1, FIN(e) + 0.8, "EN 5 MINUTOS", (960, 390), px=86, d=0.8)
    R.snd(t_egipto, "escribir", 0.6, dur=0.9)
    R.snd(t_cinco, "pluck", 0.5)


# ------------------------------------------------------------------ 2. ORÍGENES (Narmer y unificación)
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_franja = T(e, "franja")
    t_crecidas = T(e, "crecidas")
    t_narmer = T(e, "narmer")
    t_unifica = T(e, "unifica")
    t_corona = T(e, "corona")
    t_dinastias = T(e, "dinastias")
    t_menfis = T(e, "menfis")
    t_jeroglificos = T(e, "jeroglificos")
    t_templos = T(e, "templos")

    R.terreno(i0 - 0.2, "nilo_corredor", COL["predinastico"], 1.0)
    R.terreno(t_unifica - 0.2, "unificado", COL["antiguo"], 1.5)

    R.camara(i0 - 0.2, 31.5, 27.5, 2.5)
    R.camara(t_crecidas, 31.8, 26.5, 3.2)
    R.camara(t_narmer - 0.2, 32.6, 25.7, 4.2) # Tebas / Hieracómpolis
    R.camara(t_menfis - 0.2, 31.25, 29.85, 4.8) # Menfis
    R.camara(t_jeroglificos - 0.2, 31.2, 29.5, 4.0)

    R.anio(i0, -3100)
    R.anio(t_dinastias, -3000)

    # Sello de dinastía: Dinastía I
    R.sello(t_narmer, "I", "DINASTÍA I", COL["antiguo"])

    # Barca de papiro navegando por las aguas del Nilo
    R.act(A.barca_papiro(), geo=(32.0, 26.8), off=(0, 20), s=0.55,
          t_in=t_franja, d_in=0.6, entra="pop", sem=110,
          sfx=[(0, "ola", 0.5)], t_out=t_narmer - 0.2, sale="encoger", z=1)
    lugar(R, t_franja, t_narmer - 0.3, "EL NILO SAGRADO", (32.0, 26.8), off=(0, -110), px=54)

    # El Rey Narmer unificando con la maza y la Paleta de Narmer
    R.act(A.paleta_narmer(), geo=CIU["tebas"], off=(110, 30), s=0.52,
          t_in=t_narmer - 0.2, d_in=0.5, entra="pop", sem=111,
          sfx=[(0, "pop", 0.5), (0.1, "golpe_suave", 0.4)], t_out=t_dinastias - 0.2, sale="encoger", z=2)
    lugar(R, t_narmer, t_dinastias - 0.3, "PALETA DE NARMER", CIU["tebas"], off=(110, -170), px=52)

    R.act(personaje_egipcio("faraon", corona="hedjet", mirada=1.0), geo=CIU["tebas"], off=(-70, 40), s=0.55,
          t_in=t_narmer, d_in=0.45, entra="pop", sem=112,
          sfx=[(0, "pop", 0.5)], t_out=t_dinastias - 0.2, sale="encoger", z=2)
    lugar(R, t_unifica, t_dinastias - 0.3, "REY NARMER (~3100 a.C.)", CIU["tebas"], off=(-70, -160), px=54)

    # Capital en Menfis con la doble corona
    R.act(personaje_egipcio("faraon", corona="pschent", mirada=1.0), geo=CIU["menfis"], off=(-70, 30), s=0.56,
          t_in=t_menfis - 0.3, d_in=0.5, entra="pop", sem=113,
          sfx=[(0, "pop", 0.5), (0.1, "fanfarria", 0.5)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_menfis, FIN(e), "MENFIS (CAPITAL)", CIU["menfis"], off=(-390, 0), px=50)

    # Escriba sentado inventando los jeroglíficos y el cartucho real
    R.act(A.escriba_sentado(), geo=CIU["saqqara"], off=(80, 40), s=0.52,
          t_in=t_jeroglificos - 0.2, d_in=0.5, entra="pop", sem=114,
          sfx=[(0, "pop", 0.5), (0.1, "escribir", 0.4)], t_out=FIN(e), sale="encoger", z=2)
    R.act(A.cartucho_real(), geo=CIU["saqqara"], off=(190, 20), s=0.46,
          t_in=t_templos - 0.2, d_in=0.5, entra="pop", sem=115,
          sfx=[(0, "brillo", 0.4)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_jeroglificos, FIN(e), "JEROGLÍFICOS Y ESCRIBAS", CIU["saqqara"], off=(135, 150), px=50)


# ------------------------------------------------------------------ 3. PIRÁMIDES (Reino Antiguo)
def _piramides(R):
    e = "piramides"
    i0 = INI(e)
    t_reino = T(e, "reino")
    t_antiguo = T(e, "antiguo")
    t_imhotep = T(e, "imhotep")
    t_saqqara = T(e, "saqqara")
    t_guiza = T(e, "guiza")
    t_keops = T(e, "keops")
    t_esfinge = T(e, "esfinge")
    t_cuatro = T(e, "cuatro")

    R.terreno(i0 - 0.2, "unificado", COL["antiguo"], 1.2)
    R.camara(i0 - 0.2, 31.25, 29.85, 4.4)
    R.camara(t_imhotep - 0.2, 31.22, 29.87, 5.4) # Saqqara
    R.camara(t_guiza - 0.2, 31.13, 29.98, 6.0)  # Meseta de Guiza
    R.camara(t_esfinge - 0.2, 31.14, 29.97, 6.5) # Esfinge
    R.camara(t_cuatro - 0.2, 31.13, 29.98, 5.0)

    R.anio(i0, -2686)
    R.anio(t_imhotep, -2650)
    R.anio(t_keops, -2550)

    # Sello de dinastía: Reino Antiguo
    R.sello(t_antiguo, "IV", "REINO ANTIGUO", COL["antiguo"])

    # Imhotep y la primera pirámide escalonada en Saqqara
    R.act(A.piramide_escalonada(), geo=CIU["saqqara"], off=(-20, 20), s=0.55,
          t_in=t_imhotep - 0.2, d_in=0.6, entra="pop", sem=120,
          sfx=[(0, "pop", 0.5), (0.2, "tambor", 0.5)], t_out=t_guiza - 0.2, sale="encoger", z=1)
    lugar(R, t_saqqara, t_guiza - 0.3, "SAQQARA: PIRÁMIDE ESCALONADA", CIU["saqqara"], off=(-20, -160), px=54)

    # En Guiza: miles de trabajadores con el trineo de bloques
    R.act(A.trineo_bloque(), geo=CIU["guiza"], off=(-120, 80), s=0.48,
          t_in=t_guiza - 0.2, d_in=0.5, entra="pop", sem=121,
          sfx=[(0, "golpe_suave", 0.5)], t_out=FIN(e), sale="encoger", z=2)

    # La Gran Pirámide de Keops (con piramidión dorado brillante)
    R.act(A.gran_piramide_guiza(), geo=CIU["guiza"], off=(0, 20), s=0.65,
          t_in=t_keops - 0.3, d_in=0.7, entra="pop", sem=122,
          sfx=[(0, "pop", 0.5), (0.3, "brillo", 0.6)], t_out=FIN(e), sale="encoger", z=1)
    lugar(R, t_keops, FIN(e), "GRAN PIRÁMIDE DE KEOPS (146 m)", CIU["guiza"], off=(0, -210), px=56)

    # La Gran Esfinge vigilando a su lado
    R.act(A.gran_esfinge(), geo=CIU["guiza"], off=(160, 50), s=0.48,
          t_in=t_esfinge - 0.2, d_in=0.5, entra="pop", sem=123,
          sfx=[(0, "pop", 0.5), (0.1, "viento", 0.4)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_esfinge, FIN(e), "LA GRAN ESFINGE", CIU["guiza"], off=(160, 150), px=50)


# ------------------------------------------------------------------ 4. INTERMEDIO Y REINO MEDIO (Karnak e Hicsos)
def _intermedio1(R):
    e = "intermedio1"
    i0 = INI(e)
    t_sequias = T(e, "sequias")
    t_caos = T(e, "caos")
    t_tebas = T(e, "tebas")
    t_medio = T(e, "medio")
    t_karnak = T(e, "karnak")
    t_asia = T(e, "asia")
    t_hicsos = T(e, "hicsos")
    t_delta = T(e, "delta")

    # Caos / fragmentación territorial -> reunificación tebana -> invasión hicsos en el delta
    R.terreno(i0 - 0.2, "alto_egipto", COL["medio"], 1.2)
    R.terreno(t_hicsos - 0.2, "delta", COL["hicsos"], 1.2)

    R.camara(i0 - 0.2, 31.5, 28.0, 3.5)
    R.camara(t_tebas - 0.2, 32.64, 25.68, 4.6)  # Tebas
    R.camara(t_karnak - 0.2, 32.66, 25.72, 4.8) # Karnak
    R.camara(t_asia - 0.4, 32.66, 25.72, 4.8)   # Mantener Tebas/Karnak centrados
    R.camara(t_asia + 0.3, 32.5, 30.8, 3.8)    # Transición al Delta y el Sinaí
    R.camara(t_delta - 0.2, 31.5, 31.0, 4.4)

    R.anio(i0, -2181)
    R.anio(t_medio, -2055)
    R.anio(t_hicsos, -1650)

    # Sello de dinastía: Reino Medio
    R.sello(t_medio, "XII", "REINO MEDIO", COL["medio"])

    # Príncipe tebano con cetro y corona blanca
    R.act(personaje_egipcio("faraon", corona="hedjet", mirada=1.0), geo=CIU["tebas"], off=(-110, 30), s=0.52,
          t_in=t_tebas - 0.2, d_in=0.5, entra="pop", sem=130,
          sfx=[(0, "pop", 0.5), (0.1, "fanfarria", 0.4)], t_out=t_asia - 0.2, sale="encoger", z=2)
    lugar(R, t_tebas, t_karnak - 0.2, "PRÍNCIPES DE TEBAS", CIU["tebas"], off=(-110, 150), px=52)

    # Templo de Karnak y gran obelisco de granito rosa
    R.act(Bb.templo_karnak(), geo=CIU["karnak"], off=(20, 20), s=0.52,
          t_in=t_karnak - 0.3, d_in=0.6, entra="pop", sem=131,
          sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.5)], t_out=t_asia - 0.2, sale="encoger", z=1)
    R.act(Bb.obelisco(), geo=CIU["karnak"], off=(110, 10), s=0.54,
          t_in=t_karnak, d_in=0.5, entra="pop", sem=132,
          sfx=[(0, "pop", 0.4)], t_out=t_asia - 0.2, sale="encoger", z=2)
    lugar(R, t_karnak, t_asia - 0.3, "TEMPLOS DE KARNAK", CIU["karnak"], off=(60, 140), px=54)

    # Invasión de los Hicsos: carros de guerra veloces entrando por el este del Delta
    R.act(Bb.carro_faraon(), geo=(32.2, 30.9), off=(-30, 20), s=0.52,
          t_in=t_hicsos - 0.2, d_in=0.5, entra="pop", sem=133,
          sfx=[(0, "cuerno", 0.5), (0.2, "tambor", 0.5)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_hicsos, FIN(e), "INVASIÓN HICSA (CARROS DE GUERRA)", (32.2, 30.9), off=(-30, -160), px=54)


# ------------------------------------------------------------------ 5. REINO NUEVO (Expansión, Hatshepsut y Tutmosis III)
def _reino_nuevo(R):
    e = "reino_nuevo"
    i0 = INI(e)
    t_adoptan = T(e, "adoptan")
    t_expulsar = T(e, "expulsar")
    t_nuevo = T(e, "nuevo")
    t_imperio = T(e, "imperio")
    t_eufrates = T(e, "eufrates")
    t_hatshepsut = T(e, "hatshepsut")
    t_rojo = T(e, "rojo")
    t_tutmosis = T(e, "tutmosis")
    t_estrategia = T(e, "estratega")

    # El imperio del Reino Nuevo se expande al Levante y Siria
    R.terreno(i0 - 0.2, "reino_nuevo", COL["nuevo"], 1.5)

    R.camara(i0 - 0.2, 32.0, 30.0, 3.2)
    R.camara(t_eufrates - 0.2, 34.5, 32.5, 2.4)   # Hacia el Levante y Éufrates
    R.camara(t_hatshepsut - 0.2, 34.0, 26.0, 3.0) # Mar Rojo y Punt
    R.camara(t_tutmosis - 0.2, 33.5, 31.5, 3.2)

    R.anio(i0, -1550)
    R.anio(t_hatshepsut, -1479)
    R.anio(t_tutmosis, -1458)

    # Sello de dinastía: Reino Nuevo / Dinastía XVIII
    R.sello(t_nuevo, "XVIII", "REINO NUEVO", COL["nuevo"])

    # Carro de guerra egipcio imperial
    R.act(Bb.carro_faraon(), geo=(31.8, 30.2), off=(0, 20), s=0.55,
          t_in=t_adoptan - 0.2, d_in=0.5, entra="pop", sem=140,
          sfx=[(0, "pop", 0.5), (0.1, "fanfarria", 0.5)], t_out=t_hatshepsut - 0.2, sale="encoger", z=2)
    lugar(R, t_nuevo, t_hatshepsut - 0.3, "IMPERIO DEL REINO NUEVO", (31.8, 30.2), off=(0, -160), px=56)

    # Reina Hatshepsut como faraón y su barco de expedición a Punt
    R.act(personaje_egipcio("reina", corona="nemes", mirada=-1.0), geo=(34.2, 27.2), off=(-90, 30), s=0.52,
          t_in=t_hatshepsut - 0.2, d_in=0.5, entra="pop", sem=141,
          sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.5)], t_out=t_tutmosis - 0.2, sale="encoger", z=2)
    R.act(Bb.barco_punt(), geo=(34.2, 27.2), off=(70, 20), s=0.48,
          t_in=t_rojo - 0.3, d_in=0.6, entra="pop", sem=142,
          sfx=[(0, "ola", 0.5)], t_out=t_tutmosis - 0.2, sale="encoger", z=1)
    lugar(R, t_hatshepsut, t_tutmosis - 0.3, "HATSHEPSUT: EXPEDICIÓN A PUNT", (34.2, 27.2), off=(0, -160), px=54)

    # Tutmosis III: el 'Napoleón de Egipto', faraón guerrero con corona Khepresh
    R.act(personaje_egipcio("faraon", corona="khepresh", mirada=1.0, cetro=False), geo=(35.0, 32.5), off=(0, 30), s=0.56,
          t_in=t_tutmosis - 0.2, d_in=0.5, entra="pop", sem=143,
          sfx=[(0, "pop", 0.5), (0.2, "fanfarria", 0.6)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_tutmosis, FIN(e), "TUTMOSIS III (EXPANSIÓN IMPERIAL)", (35.0, 32.5), off=(0, -160), px=56)
