# -*- coding: utf-8 -*-
"""Coreografía parte 1/3: Gancho, Orígenes, República y Conquista de Italia."""
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
    _gancho(R)
    _origenes(R)
    _republica(R)
    _italia(R)


# ------------------------------------------------------------------ 1. GANCHO
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_aldea = T(e, "pequeña")
    t_chozas = T(e, "chozas")
    t_rio = T(e, "río")
    t_mundo = T(e, "mundo")
    t_tres = T(e, "tres")
    t_personas = T(e, "personas")
    t_historia = T(e, "historia")
    t_roma = T(e, "roma")
    t_cinco = T(e, "cinco")

    # Cámara dinámica: inicia en el Lacio, abre plano al Mediterráneo entero
    R.camara(0.0, 13.0, 42.0, 1.8)
    R.camara(t_aldea + 0.4, 12.5, 41.9, 2.2)
    R.camara(t_mundo - 0.2, 14.5, 40.0, 1.45)
    R.camara(t_tres, 16.0, 39.5, 1.22)
    R.camara(t_historia, 15.0, 38.0, 1.14)
    R.camara(FIN(e), 15.0, 38.5, 1.18)

    # Atmósfera: sol brillante y nubes en el cielo
    R.act(A.sol_brillo(54), pos=(1680, 220, 0.95), t_in=0.2, d_in=0.6, entra="pop", sem=1, sfx=[(0, "brillo", 0.5)], z=-1, t_out=t_historia - 0.2, sale="sube_fuera")
    for k in range(3):
        R.act(lambda t, k=k: Bb.pajaro(int(t * 6) + k), pos=lambda t, k=k: (1900 - 240 * (t - 0.5) + 80 * k, 240 + 60 * k + 15 * math.sin(t * 3.5 + k), 0.55),
              t_in=0.5 + 0.2 * k, d_in=0.3, entra="pop", sem=2 + k, t_out=t_mundo - 0.2, sale="encoger", peg=False, z=2)

    # Territorio: el Lacio pequeño que se expande a la gloria máxima del imperio
    R.terreno(t_aldea - 0.1, "lacio", COL["lacio"], 1.1)
    pop(R, RO.choza_lacio, t_chozas, geo=(12.49, 41.90), off=(0, 20), s=0.75, sem=5, snd="pop", t_out=t_mundo - 0.1, sale="encoger")
    lugar(R, t_aldea, t_mundo - 0.2, "ROMA", (12.49, 41.90), off=(0, -70), px=62)

    R.terreno(t_mundo - 0.2, "maxima", COL["maxima"], 2.2)
    R.snd(t_mundo, "brillo", 0.75)
    R.snd(t_tres, "whoosh", 0.6, dur=0.8)


    # Título cinematográfico y cronómetro
    R.texto(t_historia - 0.05, FIN(e) + 0.8, "LA HISTORIA DE", (1060, 70), px=60, d=0.7)
    R.texto(t_roma - 0.05, FIN(e) + 0.8, "ROMA", (1060, 135), px=104, d=0.9)
    R.texto(t_cinco - 0.05, FIN(e) + 0.8, "en 5 minutos", (1060, 198), px=52, d=0.6)
    R.snd(t_historia, "escribir", 0.5, dur=0.7)
    R.snd(t_roma, "escribir", 0.65, dur=0.9)
    R.snd(t_cinco, "escribir", 0.5, dur=0.6)

    # Cronómetro giratorio en la esquina superior derecha
    pop(R, lambda t: C.cronometro((t - t_cinco) * 2.0 * math.pi / max(0.6, FIN(e) - t_cinco + 0.6)), t_cinco + 0.15, pos=(1680, 240, 0.90),
        t_out=FIN(e) + 0.6, sale="encoger", d_in=0.5, snd="pop", vol=0.7, sem=12)
    R.snd(t_cinco + 0.3, "reloj_rapido", 0.45, dur=1.6)


# ------------------------------------------------------------------ 2. ORÍGENES (753 a.C.)
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_753 = T(e, "setecientos")
    t_tiber = T(e, "tíber")
    t_pastores = T(e, "pastores")
    t_latinos = T(e, "latinos")
    t_colinas = T(e, "colinas")
    t_comerciar = T(e, "comerciar")
    t_nace = T(e, "nace")
    t_reyes = T(e, "reyes")
    t_etruscos = T(e, "etruscos")

    # Desvanecer elementos previos
    R.terreno(i0 - 0.3, "lacio", COL["lacio"], 1.0)
    R.camara(i0, 13.5, 41.5, 1.4)
    R.camara(t_753, 12.6, 42.0, 2.5)
    R.camara(t_tiber + 0.3, 12.49, 41.90, 3.3)
    R.camara(t_colinas, 12.49, 41.90, 3.6)
    R.camara(t_nace, 12.55, 41.95, 3.1)
    R.camara(FIN(e), 12.7, 42.1, 2.7)

    # Contador de años: de 2026 hacia el 753 a.C.
    R.anio(i0, 2026)
    R.anio(t_753 - 0.2, 2026)
    R.anio(t_753 + 0.6, -753)
    R.snd(t_753, "reloj_rapido", 0.55, dur=1.5)

    # El río Tíber se traza en azul acuarela
    R.rio(M.RIO_TIBER, t_tiber - 0.2, 1.8, color=(120, 180, 220), ancho=24)
    R.snd(t_tiber, "whoosh", 0.5, dur=1.2)
    lugar(R, t_tiber + 0.2, FIN(e) + 0.4, "Río Tíber", (12.35, 42.15), off=(-30, -50), px=46)

    # Aldea de las 7 colinas con chozas y pastores
    pop(R, RO.choza_lacio, t_colinas - 0.2, geo=(12.42, 41.93), off=(-90, 20), s=0.68, sem=20, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.choza_lacio, t_colinas + 0.1, geo=(12.55, 41.94), off=(90, -20), s=0.62, sem=21, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.choza_lacio, t_colinas + 0.35, geo=(12.48, 41.85), off=(0, 75), s=0.65, sem=22, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")

    # Pastores latinos trabajando
    pop(R, persona((150, 100, 70), PIEL, "paja", "feliz", (25, 75), 0, traje="corta", acc_d="azada"),
        t_pastores, geo=(12.45, 41.86), off=(-70, 70), s=0.55, sem=23, t_out=t_nace - 0.1, sale="encoger")
    pop(R, persona((120, 80, 60), PIEL, "pelo", "normal", (30, 40), 1, traje="corta", acc_d="tazon"),
        t_latinos, geo=(12.53, 41.88), off=(70, 80), s=0.52, sem=24, t_out=t_nace - 0.1, sale="encoger")

    # Barco primitivo navegando por el Tíber
    P_tiber = R.camino_pos(M.RIO_TIBER, t_tiber + 0.8, 3.4, ease=lambda u: u)
    R.act(RO.barco_mercante, pos_geo=P_tiber, off=lambda t: (0, -4 + 3 * math.sin(t * 4)), s=0.28, t_in=t_tiber + 0.8, d_in=0.4,
          entra="pop", sem=25, t_out=t_nace - 0.1, sale="encoger", zs=0.5, z=1)

    # Nacimiento de Roma: primer rey (Rómulo con cetro y manto)
    rey_romulo = pop(R, persona(ROJO_ROMA, PIEL, "corona", "feliz", (25, 110), 0, traje="tunica", faja=ORO_ROMA, cuello=ORO_ROMA, bigote=True),
                     t_nace + 0.2, pos=(1380, 720), s=0.92, sem=26, snd="fanfarria", t_out=FIN(e) + 0.4, sale="encoger")
    lugar(R, t_nace, FIN(e) + 0.4, "MONTE PALATINO", (12.49, 41.89), off=(0, 75), px=54)

    # Vecinos etruscos al norte en Toscana
    lugar(R, t_etruscos - 0.1, FIN(e) + 0.4, "ETRURIA", (11.8, 43.2), off=(0, -40), px=56)
    pop(R, RO.villa_romana, t_etruscos + 0.1, geo=(11.6, 43.0), off=(0, 20), s=0.5, sem=28, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    R.texto(t_nace + 0.1, FIN(e) + 0.4, "Fundación: 753 a. C.", (960, 160), px=72, d=0.7)


# ------------------------------------------------------------------ 3. REPÚBLICA (509 a.C.)
def _republica(R):
    e = "republica"
    i0 = INI(e)
    t_509 = T(e, "quinientos")
    t_tiran = T(e, "tiranía")
    t_expulsan = T(e, "expulsan")
    t_rey = T(e, "rey")
    t_juran = T(e, "juran")
    t_republica = T(e, "república")
    t_senado = T(e, "senado", frase=2)
    t_spqr = T(e, "pe")

    R.camara(i0, 12.7, 42.1, 2.7)
    R.camara(t_509, 12.5, 41.9, 2.5)
    R.camara(t_republica, 12.5, 41.9, 2.2)
    R.camara(t_spqr, 12.6, 41.8, 2.0)
    R.camara(FIN(e), 12.8, 41.7, 1.9)

    R.anio(t_509, -509)
    R.snd(t_509, "reloj_rapido", 0.5, dur=1.2)

    # Templo de Júpiter Capitolino en el Foro
    pop(R, RO.templo_romano, i0 + 0.2, pos=(960, 560), s=0.95, sem=30, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")

    # Expulsión del rey tirano (Tarquinio): aparece y cae fuera del encuadre
    rey_tirano = R.act(persona((100, 30, 40), PIEL, "corona", "enfado", (20, 130), 0, traje="tunica", barba=NEGRO),
                       pos=(520, 720), s=0.9, t_in=t_509, d_in=0.4, entra="pop", sem=31, snd=[(0, "pop", 0.5)],
                       t_out=t_expulsan + 0.2, sale="caer", d_out=0.9)
    R.act(A.pulgar(False), pos=(520, 480, 0.75), t_in=t_tiran, d_in=0.3, entra="pop", sem=32, t_out=t_expulsan + 0.5, sale="encoger", snd="bocinazo", vol=0.35)
    R.snd(t_expulsan, "crujido", 0.8)

    # Nace la República: senadores y cónsules toman el poder
    R.snd(t_republica, "brillo", 0.7)
    pop(R, RO.senador, t_juran, pos=(1420, 700), s=0.92, sem=33, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")
    pop(R, persona(MARMOL, PIEL_OSC, "letrado", "feliz", (20, 80), 1, traje="tunica", faja=PURPURA_IMP),
        t_senado - 0.2, pos=(1200, 720), s=0.88, sem=34, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")

    # Estandarte imperial SPQR izado con orgullo
    pop(R, RO.estandarte_spqr, t_spqr - 0.2, pos=(500, 680), s=0.9, sem=35, snd="impacto", t_out=FIN(e) + 0.5, sale="encoger")
    R.texto(t_spqr - 0.1, FIN(e) + 0.5, "SENATUS POPULUSQUE ROMANUS", (960, 160), px=84, d=0.7)
    R.texto(t_spqr + 0.3, FIN(e) + 0.5, "S · P · Q · R", (960, 245), px=96, d=0.6)
    R.snd(t_spqr, "escribir", 0.55, dur=1.0)


# ------------------------------------------------------------------ 4. ITALIA (Guerras Samnitas y Vía Apia)
def _italia(R):
    e = "italia"
    i0 = INI(e)
    t_enemigos = T(e, "enemigos")
    t_pelear = T(e, "pelear")
    t_legiones = T(e, "legiones")
    t_samnitas = T(e, "samnitas")
    t_calzadas = T(e, "calzadas")
    t_via = T(e, "vía")
    t_griegas = T(e, "griegas")
    t_peninsula = T(e, "península")
    t_ondea = T(e, "ondea")

    R.camara(i0, 12.8, 41.7, 1.9)
    R.camara(t_enemigos, 13.5, 41.5, 1.85)
    R.camara(t_samnitas, 14.2, 41.0, 1.75)
    R.camara(t_via, 14.8, 40.8, 1.65)
    R.camara(t_ondea, 14.5, 40.5, 1.55)
    R.camara(FIN(e), 13.8, 40.8, 1.5)

    # El territorio de Roma absorbe toda la península itálica
    R.terreno(t_samnitas - 0.2, "italia", COL["italia"], 2.0)
    R.snd(t_pelear, "impacto", 0.6)

    # Campamento militar y calzada Vía Apia trazada de Roma a Brindisi
    pop(R, RO.castrum_fort, t_legiones - 0.2, geo=(13.2, 42.2), off=(0, 20), s=0.48, sem=40, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    R.ruta(M.VIA_APIA, t_via - 0.2, 2.2, ancho=5.5, color=(160, 50, 45))
    R.snd(t_via, "escribir", 0.55, dur=1.2)
    lugar(R, t_via, FIN(e) + 0.4, "VÍA APIA", (15.0, 41.2), off=(0, -40), px=54)

    # Legionario en marcha y jinete de caballería
    pop(R, lambda t: RO.legionario(int(t * 4)), t_pelear, pos=(420, 720), s=0.92, sem=42, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, lambda t: RO.jinete_romano(int(t * 6)), t_samnitas + 0.2, pos=(1520, 750), s=0.78, sem=43, snd="galope", t_out=FIN(e) + 0.4, sale="encoger")

    # Guerras contra samnitas: espadas chocando en los Apeninos
    pop(R, A.espadas(), t_samnitas, geo=(14.2, 41.4), off=(0, -20), s=0.75, sem=44, snd="espada", vol=0.6, t_out=t_griegas - 0.1, sale="encoger")
    lugar(R, t_samnitas, t_griegas - 0.1, "SAMNIO", (14.2, 41.4), off=(0, 45), px=48)

    # Ciudades griegas del sur (Tarento, Siracusa)
    lugar(R, t_griegas, FIN(e) + 0.4, "MAGNA GRECIA", (16.8, 39.5), off=(0, -30), px=52)
    pop(R, RO.templo_romano, t_griegas + 0.2, geo=(15.3, 37.1), off=(0, 20), s=0.4, sem=46, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")

    # Villas romanas esparcidas por la península unificada
    pop(R, RO.villa_romana, t_peninsula, geo=(11.5, 43.5), off=(0, 20), s=0.45, sem=47, t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.villa_romana, t_peninsula + 0.3, geo=(14.5, 40.8), off=(0, 20), s=0.42, sem=48, t_out=FIN(e) + 0.4, sale="encoger")

    R.texto(t_ondea, FIN(e) + 0.4, "Italia unificada bajo el águila", (960, 160), px=74, d=0.7)
    R.snd(t_ondea, "brillo", 0.6)
