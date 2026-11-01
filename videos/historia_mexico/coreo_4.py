# -*- coding: utf-8 -*-
"""Coreografía (4/4): la Revolución mexicana (Francisco I. Madero en 1910, Emiliano Zapata en el sur con «Tierra y Libertad», Pancho Villa
y la División del Norte, Venustiano Carranza y la Constitución de 1917 en Querétaro, Diego Rivera y Frida Kahlo), el siglo XX (Lázaro
Cárdenas y la expropiación petrolera de 1938, el milagro mexicano, los Juegos Olímpicos y Tlatelolco en 1968, la alternancia del año 2000),
el México actual (130 millones de habitantes, puente entre América del Norte y América Latina, 35 sitios Patrimonio de la Humanidad,
pirámides y capital moderna), el cierre (desfile de tres mil años de historia y pregunta final) y las transiciones procedurales.
Capas de territorio: 0 = México, 1 = División del Norte (Villa), 2 = Ejército Libertador del Sur (Zapata)."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_mx1 as M1
import obj_mx2 as M2
import obj_mx3 as M3
from core import FIN, INI, T, kf
from coreo_util import CI, COL, andar, ciudad, formacion, ga, grupo, lugar, mece, pa, titulo
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from trans import SFX, Transicion


def cortes(R):
    pass


def construir(R):
    _revolucion(R)
    _siglo20(R)
    _actualidad(R)
    _cierre(R)
    _transiciones(R)


# ------------------------------------------------------------------ LA REVOLUCIÓN MEXICANA (1910-1920)
def _revolucion(R):
    e = "revolucion"
    i0 = INI(e)
    t_diez, t_mad, t_conv, t_dic, t_est, t_rev = (T(e, "diez"), T(e, "madero"), T(e, "convoca"), T(e, "dictadura"),
                                                  T(e, "estalla"), T(e, "revolucion"))
    t_sur, t_zap, t_cam, t_tie, t_lib, t_nor, t_vil, t_div = (T(e, "sur"), T(e, "zapata"), T(e, "campesinos"), T(e, "tierra"),
                                                              T(e, "libertad"), T(e, "norte", frase=1), T(e, "villa"),
                                                              T(e, "division"))
    t_bat, t_fac, t_car, t_con, t_que = T(e, "batallas"), T(e, "facciones"), T(e, "carranza"), T(e, "congreso"), T(e, "queretaro")
    t_diec, t_cons, t_pio, t_edu, t_rep, t_obr = (T(e, "diecisiete"), T(e, "constitucion"), T(e, "pionera"),
                                                  T(e, "educacion"), T(e, "reparto"), T(e, "obreros"))
    t_rec, t_ide, t_mur, t_die, t_art, t_fri = (T(e, "reconstruye"), T(e, "identidad"), T(e, "murales"),
                                                T(e, "diego"), T(e, "arte"), T(e, "frida"))

    # cámara: plano nacional de la Revolución -> sur zapatista y norte villista -> Querétaro y Ciudad de México
    R.camara(i0 - 0.2, -101.8, 22.8, 1.38)
    R.camara(t_bat - 0.2, -101.8, 22.8, 1.38)
    R.camara(t_que - 0.1, -100.3, 20.6, 3.8)
    R.camara(t_rec - 0.2, -100.3, 20.6, 3.8)
    R.camara(t_rec + 0.2, -99.13, 19.45, 5.2)
    R.camara(FIN(e) + 0.4, -99.15, 19.45, 5.0)

    # años
    R.anio(i0 + 0.1, 1910)
    R.anio(t_sur, 1914)
    R.anio(t_diec, 1917)
    R.anio(t_rec, 1925)

    # frase 0: 1910, Francisco I. Madero y el estallido de la Revolución mexicana
    ciudad(R, i0 + 0.1, t_sur - 0.2, "san_luis", "SAN LUIS POTOSÍ", "izq", 40)
    pa(R, M1.madero(0, "feliz"), 320, 1010, 1.14, i0, t_sur, sem=190, extra=[(0.05, "fanfarria", 0.4)])
    R.texto(t_mad - 0.1, t_sur - 0.1, "FRANCISCO I. MADERO", (340, 560), px=44, d=0.4)
    pa(R, M1.adelita(0, "serio"), 1320, 1010, 1.06, t_conv, t_sur, sem=191, flip=True)
    R.texto(t_conv + 0.1, t_sur - 0.1, "¡SUFRAGIO EFECTIVO!", (1320, 590), px=42, d=0.4)
    titulo(R, t_est - 0.1, t_sur - 0.1, "¡REVOLUCIÓN MEXICANA! (1910)", px=74)
    R.sello(t_rev, "sombrero_rev", "REVOLUCIÓN (1910)", color=(206, 112, 58))

    # frase 1: Emiliano Zapata en el sur («Tierra y Libertad») y Pancho Villa en el norte («División del Norte»)
    R.terreno(t_sur - 0.1, "rev_sur", COL["rev_sur"], 0.9, capa=2)
    R.terreno(t_nor - 0.1, "rev_norte", COL["rev_norte"], 1.0, capa=1)
    ciudad(R, t_sur, t_bat - 0.3, "cuautla", "MORELOS", "abajo", 42)
    ciudad(R, t_div, t_bat - 0.3, "torreon", "TORREÓN", "der", 42)
    R.ruta(M.RUTAS["zapata_norte"], t_zap, 1.6, ancho=5.0, t1=t_diec, flecha=True)
    R.ruta(M.RUTAS["villa_sur"], t_vil - 0.1, 2.0, ancho=5.0, t1=t_diec, flecha=True)
    andar(R, lambda p: M3.jinete(p, "zapata"), M.RUTAS["zapata_norte"], t_zap, 1.8, t1=t_car, s=0.38, sem=192, zs=0.4, z=3, fps=8)
    for k in range(2):
        andar(R, lambda p, k=k: M3.jinete(p + k, "villa"), M.RUTAS["villa_sur"], t_vil - 0.1 + 0.18 * k, 2.1, t1=t_car,
              s=0.38, sem=193 + k, zs=0.4, z=3, fps=8, off=formacion(k, 2, 130))
    andar(R, lambda p: M3.locomotora(p), M.RUTAS["villa_sur"][:4], t_div - 0.2, 1.8, t1=t_car, s=0.38, sem=195, zs=0.4, z=2, fps=6)
    R.snd(t_vil - 0.1, "galope", 0.5, dur=2.0)
    pa(R, M1.zapata(0, "enojo"), 310, 1010, 1.14, t_zap - 0.1, t_car - 0.1, sem=196)
    R.texto(t_zap, t_car - 0.2, "EMILIANO ZAPATA", (310, 540), px=44, d=0.4)
    R.texto(t_tie - 0.1, t_nor, "«TIERRA Y LIBERTAD»", (330, 480), px=38, d=0.4)
    pa(R, M1.pancho_villa(0, "enojo"), 1590, 1010, 1.14, t_vil - 0.1, t_diec, sem=197, flip=True)
    R.texto(t_vil, t_diec - 0.1, "PANCHO VILLA", (1590, 550), px=46, d=0.4)
    titulo(R, t_div - 0.1, t_bat - 0.1, "LA DIVISIÓN DEL NORTE", px=74)

    # frase 2: batallas entre facciones y Venustiano Carranza en Querétaro
    R.romper("facciones_rev", t_bat - 0.1, t_bat + 0.4, t_con - 0.2, t_diec + 0.3, capa=0, gap=14.0, deriva=26.0)
    ga(R, A.espadas(), CI["celaya"], t_bat, t_diec - 0.1, s=0.44, off=(0, -20), sem=198, zs=0.4, z=4, extra=[(0.05, "espada", 0.5)])
    ciudad(R, t_que, t_diec - 0.2, "queretaro", "QUERÉTARO (1917)", "abajo", 44)
    pa(R, M1.carranza(0, "serio"), 340, 1010, 1.12, t_car - 0.1, t_diec - 0.1, sem=199, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_car, t_diec - 0.1, "VENUSTIANO CARRANZA", (340, 560), px=44, d=0.4)

    # frase 3: Constitución de 1917 (educación gratuita, reparto agrario y derechos obreros)
    R.terreno(t_diec - 0.1, None, COL["rev_norte"], 0.7, capa=1)
    R.terreno(t_diec - 0.1, None, COL["rev_sur"], 0.7, capa=2)
    R.terreno(t_diec - 0.1, "mexico_mod", COL["constitucion"], 1.1)
    pa(R, M2.libro_constitucion("1917"), 960, 990, 1.08, t_cons - 0.15, t_rec - 0.1, sem=200, entra="sube", dy=320,
       extra=[(0.05, "escribir", 0.45, {"dur": 0.9})])
    titulo(R, t_cons - 0.1, t_rec - 0.1, "CONSTITUCIÓN DE 1917", px=80)
    R.sello(t_cons, "libro", "CONSTITUCIÓN 1917", color=(204, 72, 58))
    pa(R, A.rollo_escritura(), 300, 1010, 0.72, t_edu - 0.1, t_rec - 0.1, sem=201)
    R.texto(t_edu, t_rec - 0.1, "ART. 3º EDUCACIÓN", (300, 780), px=38, d=0.35)
    pa(R, M2.planta_maiz(), 620, 1010, 0.78, t_rep - 0.1, t_rec - 0.1, sem=202, entra="sube", dy=240)
    R.texto(t_rep, t_rec - 0.1, "ART. 27 TIERRA", (620, 740), px=38, d=0.35)
    pa(R, M1.obrero_petroleo(0, "feliz"), 1420, 1010, 0.96, t_obr - 0.15, t_rec - 0.1, sem=203, flip=True)
    R.texto(t_obr - 0.1, t_rec - 0.1, "ART. 123 TRABAJO", (1420, 620), px=38, d=0.35)

    # frase 4: murales de Diego Rivera y arte de Frida Kahlo
    ga(R, M2.palacio_bellas_artes(), CI["cdmx"], t_rec + 0.2, FIN(e) + 0.3, s=0.52, off=(0, 10), sem=204, zs=0.5, z=2)
    pa(R, M1.diego_rivera(0, "feliz"), 340, 1010, 1.12, t_die - 0.2, FIN(e) + 0.3, sem=205,
       extra=[(0.05, "pincel", 0.45, {"dur": 0.9})])
    R.texto(t_die - 0.1, FIN(e) + 0.2, "DIEGO RIVERA", (340, 580), px=46, d=0.4)
    pa(R, M1.frida_kahlo(0, "serio"), 1560, 1010, 1.12, t_fri - 0.2, FIN(e) + 0.3, sem=206, flip=True,
       extra=[(0.05, "brillo", 0.45)])
    R.texto(t_fri - 0.1, FIN(e) + 0.2, "FRIDA KAHLO", (1560, 580), px=46, d=0.4)
    titulo(R, t_mur - 0.1, FIN(e) + 0.2, "MURALISMO Y CULTURA MEXICANA", px=72)


# ------------------------------------------------------------------ EL SIGLO XX (1938-2000)
def _siglo20(R):
    e = "siglo20"
    i0 = INI(e)
    t_tre, t_car, t_ent, t_tie, t_nac, t_pet = (T(e, "treinta"), T(e, "cardenas"), T(e, "entrega"), T(e, "tierras"),
                                                T(e, "nacionaliza"), T(e, "petroleo"))
    t_dec, t_mil, t_fab, t_carr, t_uni, t_ciu = (T(e, "decadas"), T(e, "milagro"), T(e, "fabricas"), T(e, "carreteras"),
                                                 T(e, "universidades"), T(e, "ciudades"))
    t_ses, t_cel, t_jue, t_oli, t_tra, t_est, t_tla = (T(e, "sesenta"), T(e, "celebra"), T(e, "juegos"), T(e, "olimpicos"),
                                                       T(e, "tragedia"), T(e, "estudiantil"), T(e, "tlatelolco"))
    t_fin, t_ape, t_ref, t_alt, t_pac, t_dos = (T(e, "finales"), T(e, "apertura"), T(e, "reformas"), T(e, "alternancia"),
                                                T(e, "pacifica"), T(e, "dos"))

    # cámara: costa del Golfo y centro (expropiación petrolera) -> industrialización nacional -> CDMX 1968 y 2000
    R.camara(i0 - 0.2, -98.2, 21.3, 2.8)
    R.camara(t_dec - 0.2, -98.2, 21.3, 2.8)
    R.camara(t_dec + 0.3, -101.2, 23.6, 1.55)
    R.camara(t_ses - 0.2, -101.2, 23.6, 1.55)
    R.camara(t_ses + 0.2, -99.13, 19.44, 5.8)
    R.camara(t_fin - 0.2, -99.13, 19.44, 5.8)
    R.camara(t_fin + 0.2, -100.8, 22.0, 2.2)
    R.camara(FIN(e) + 0.4, -101.2, 22.6, 1.9)

    # años
    R.anio(i0 + 0.1, 1938)
    R.anio(t_mil, 1955)
    R.anio(t_ses, 1968)
    R.anio(t_dos - 0.2, 2000)

    # frase 0: 1938, Lázaro Cárdenas, reparto agrario y expropiación petrolera
    R.terreno(i0 - 0.1, "mexico_mod", COL["cardenas"], 1.0)
    ciudad(R, t_pet - 0.3, t_dec - 0.3, "poza_rica", "POZA RICA", "der", 42)
    ciudad(R, t_pet - 0.2, t_dec - 0.3, "tampico", "TAMPICO", "der", 42)
    ga(R, M2.torre_petroleo(), CI["poza_rica"], t_nac - 0.1, t_dec - 0.2, s=0.52, off=(-35, -15), sem=210, zs=0.5, z=2,
       entra="sube", dy=300, extra=[(0.05, "chorro", 0.5, {"dur": 1.4})])
    ga(R, M2.torre_petroleo(), CI["tampico"], t_pet - 0.1, t_dec - 0.2, s=0.46, off=(-35, -15), sem=211, zs=0.45, z=2,
       entra="sube", dy=280)
    pa(R, M1.lazaro_cardenas(0, "serio"), 310, 1010, 1.15, t_car - 0.15, t_dec, sem=212,
       extra=[(0.05, "fanfarria", 0.4)])
    R.texto(t_car, t_dec - 0.1, "LÁZARO CÁRDENAS", (330, 560), px=46, d=0.4)
    pa(R, M1.campesino_pre(0, "feliz"), 640, 1010, 1.0, t_ent - 0.1, t_dec, sem=213)
    pa(R, M1.obrero_petroleo(0, "feliz"), 1380, 1010, 1.05, t_nac - 0.1, t_dec, sem=214, flip=True)
    titulo(R, t_nac - 0.1, t_dec - 0.1, "EXPROPIACIÓN PETROLERA (1938)", px=72)
    R.sello(t_pet, "torre_petroleo", "PETRÓLEO (1938)", color=(76, 144, 98))

    # frase 1: el «milagro mexicano», fábricas, carreteras, universidades y grandes ciudades
    for k, (cl, nom, lado) in enumerate((("cdmx", "CIUDAD DE MÉXICO", "abajo"), ("monterrey", "MONTERREY", "abajo"),
                                         ("guadalajara", "GUADALAJARA", "izq"))):
        ciudad(R, t_fab + 0.1 * k, t_ses - 0.3, cl, nom, lado, 42)
        ga(R, M2.fabrica_moderna(), CI[cl], t_fab + 0.12 * k, t_ses - 0.3, s=0.42, off=(0, -18), sem=215 + k, zs=0.45, z=2,
           entra="sube", dy=260, extra=[(0.05, "crece", 0.45)] if k == 0 else ())
    pa(R, M2.fabrica_moderna(), 360, 1010, 0.92, t_fab - 0.1, t_ses, sem=218)
    pa(R, M1.ingeniera_hoy(0, "feliz"), 1540, 1010, 1.06, t_uni - 0.1, t_ses, sem=219, flip=True)
    R.texto(t_uni, t_ses - 0.1, "INDUSTRIA Y UNIVERSIDADES", (1500, 590), px=40, d=0.4)
    titulo(R, t_mil - 0.1, t_ses - 0.1, "EL MILAGRO MEXICANO", px=78)

    # frase 2: 1968, Juegos Olímpicos y movimiento estudiantil de Tlatelolco
    ciudad(R, t_ses + 0.2, t_jue - 0.2, "cdmx", "MÉXICO 68", "abajo", 46)
    pa(R, M2.paloma_68(), 960, 860, 1.15, t_jue - 0.15, t_fin, sem=220, entra="sube", dy=320,
       extra=[(0.05, "fanfarria", 0.4)])
    pa(R, M1.ciudadano_hoy(0, "serio"), 320, 1010, 1.06, t_tra - 0.1, t_fin, sem=221)
    pa(R, C.vela(), 1560, 1010, 0.86, t_tla - 0.2, t_fin, sem=222)
    R.texto(t_tla - 0.1, t_fin - 0.1, "2 DE OCTUBRE (TLATELOLCO)", (1520, 740), px=40, d=0.4)
    titulo(R, t_oli - 0.1, t_fin - 0.1, "MÉXICO 1968: OLIMPIADAS Y TLATELOLCO", px=68)

    # frase 3: apertura económica, reformas electorales y alternancia pacífica en el año 2000
    andar(R, lambda p: M3.buque_carga(p), [(-95.8, 19.3), (-90.0, 22.8)], t_ape - 0.1, 2.2, t1=FIN(e) + 0.3, s=0.38,
          sem=223, zs=0.4, z=2, fps=4)
    pa(R, M2.urna_voto(), 960, 990, 1.08, t_ref - 0.1, FIN(e) + 0.3, sem=224, entra="sube", dy=280,
       extra=[(0.05, "sello", 0.45)])
    pa(R, M1.ciudadano_hoy(0, "feliz"), 340, 1010, 1.08, t_alt - 0.1, FIN(e) + 0.3, sem=225)
    pa(R, M1.ingeniera_hoy(0, "feliz"), 1560, 1010, 1.08, t_alt, FIN(e) + 0.3, sem=226, flip=True)
    titulo(R, t_alt - 0.1, FIN(e) + 0.3, "ALTERNANCIA DEMOCRÁTICA (2000)", px=74)


# ------------------------------------------------------------------ ACTUALIDAD: 130 millones, puente continental y 35 sitios UNESCO
def _actualidad(R):
    e = "actualidad"
    i0 = INI(e)
    t_hoy, t_hisp, t_pob, t_cie, t_hab, t_eco = (T(e, "hoy"), T(e, "hispanohablante"), T(e, "poblado"), T(e, "ciento"),
                                                 T(e, "habitantes"), T(e, "economias"))
    t_pue, t_nor, t_lat, t_ind, t_tre, t_pat = (T(e, "puente"), T(e, "norte"), T(e, "latina"), T(e, "industria"),
                                                T(e, "treinta", frase=1), T(e, "patrimonio"))
    t_pir, t_mil, t_cor, t_cap, t_tres, t_viv = (T(e, "piramides"), T(e, "milenarias"), T(e, "corazon"), T(e, "capital"),
                                                 T(e, "tres"), T(e, "vivos"))

    # cámara: plano continental de América del Norte a Centroamérica -> acercamiento al centro y monumentos de México
    R.camara(i0 - 0.2, -101.8, 23.6, 1.48)
    R.camara(t_pue, -101.5, 23.2, 1.32)
    R.camara(t_pir - 0.2, -101.5, 23.2, 1.32)
    R.camara(t_pir + 0.3, -98.8, 19.6, 4.6)
    R.camara(FIN(e) + 0.4, -99.0, 19.5, 4.4)

    # año y sello final
    R.anio(i0 + 0.1, 2026)
    R.terreno(i0 - 0.1, "mexico_mod", COL["mexico_mod"], 0.8)
    R.sello(t_hoy + 0.2, "aguila", "MÉXICO HOY", color=(56, 138, 84))

    # frase 0: el país hispanohablante más poblado del mundo, 130 millones de habitantes
    R.contador(t_cie - 0.2, t_hab + 0.3, 0, 130_000_000, (960, 196), px=84, hasta_t=t_pue - 0.1)
    R.texto(t_hab - 0.1, t_pue - 0.1, "HABITANTES", (960, 296), px=52, d=0.4)
    R.snd(t_cie - 0.2, "reloj_rapido", 0.4, dur=1.0)
    for k in range(4):
        fn = M1.ciudadano_hoy if k % 2 == 0 else M1.ingeniera_hoy
        pa(R, lambda t, k=k, f=fn: f(int(t * 3 + k) % 2, "feliz"), 280 + 300 * k, 1010, 0.86, i0 + 0.15 * k, t_pue,
           sem=230 + k, entra="sube", dy=280, flip=k >= 2)

    # frase 1: puente entre América del Norte y América Latina + industria moderna + 35 sitios Patrimonio Mundial
    lugar(R, t_nor - 0.1, t_pir - 0.3, "AMÉRICA DEL NORTE", (-102.5, 25.8), off=(0, 0), px=44)
    lugar(R, t_lat - 0.1, t_pir - 0.3, "AMÉRICA LATINA", (-92.5, 17.5), off=(0, 0), px=44)
    R.ruta([(-99.13, 19.43), (-100.31, 25.67), (-99.5, 31.5)], t_pue, 1.4, ancho=5.5, t1=t_pir - 0.2, flecha=True)
    R.ruta([(-99.13, 19.43), (-96.72, 17.06), (-90.51, 14.63)], t_pue + 0.2, 1.4, ancho=5.5, t1=t_pir - 0.2, flecha=True)
    andar(R, lambda p: M3.buque_carga(p), [(-105.0, 18.0), (-113.0, 21.5)], t_ind - 0.2, 2.2, t1=t_pir - 0.2, s=0.38,
          sem=235, zs=0.4, z=2, fps=4, flip=True)
    andar(R, lambda p: M3.buque_carga(p), [(-95.8, 19.3), (-88.5, 23.0)], t_ind, 2.2, t1=t_pir - 0.2, s=0.38,
          sem=236, zs=0.4, z=2, fps=4)
    pa(R, M2.fabrica_moderna(), 340, 1010, 0.92, t_ind - 0.1, t_pir, sem=237)
    ga(R, M2.piramide_kukulcan(), CI["chichen_itza"], t_tre - 0.1, t_pir - 0.2, s=0.44, off=(0, 10), sem=238, zs=0.45, z=2,
       entra="sube", dy=260)
    ga(R, M2.monte_alban(), CI["monte_alban"], t_tre, t_pir - 0.2, s=0.42, off=(0, 10), sem=239, zs=0.45, z=2,
       entra="sube", dy=260)
    R.contador(t_tre - 0.1, t_pat + 0.3, 0, 35, (960, 196), px=82, formato="{} SITIOS PATRIMONIO MUNDIAL", hasta_t=t_pir - 0.1)
    R.snd(t_tre, "bling", 0.45)

    # frase 2: de las pirámides milenarias al corazón de su capital, 3.000 años de historia vivos
    ciudad(R, t_pir + 0.3, t_tres - 0.2, "teotihuacan", "TEOTIHUACÁN", "der", 42)
    ciudad(R, t_cap, FIN(e) + 0.3, "cdmx", "CIUDAD DE MÉXICO", "abajo", 46)
    ga(R, M2.piramide_sol(), CI["teotihuacan"], t_pir + 0.2, FIN(e) + 0.3, s=0.52, off=(-35, -15), sem=240, zs=0.5, z=2,
       entra="sube", dy=300, extra=[(0.05, "crece", 0.45)])
    ga(R, M2.palacio_bellas_artes(), CI["cdmx"], t_cor - 0.1, FIN(e) + 0.3, s=0.48, off=(-160, -10), sem=241, zs=0.5, z=2,
       entra="sube", dy=280)
    ga(R, M2.angel_independencia(), CI["cdmx"], t_cap - 0.1, FIN(e) + 0.3, s=0.54, off=(150, -10), sem=242, zs=0.5, z=3,
       entra="sube", dy=320, extra=[(0.05, "brillo", 0.45)])
    R.contador(t_tres - 0.2, t_viv + 0.2, 0, 3000, (960, 196), px=84, formato="{:,} AÑOS DE HISTORIA VIVA", hasta_t=FIN(e) + 0.3)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_tie, t_cho, t_dos, t_mun, t_rai, t_lat = (T(e, "tierra"), T(e, "chocaron"), T(e, "dos"), T(e, "mundos"),
                                                T(e, "raices"), T(e, "latir"))
    t_que, t_pais, t_imp, t_dim, t_com = T(e, "que", frase=1), T(e, "pais"), T(e, "imperio"), T(e, "dimelo"), T(e, "comentarios")

    R.camara(i0 - 0.2, -101.5, 23.4, 1.52)
    R.camara(t_que, -101.8, 23.6, 1.48)
    R.camara(FIN(e) + 1.2, -101.8, 23.6, 1.45)

    # desfile de tres mil años de historia mexicana por la parte inferior de la pantalla
    desfile = [
        (M1.escultor_olmeca(0, "feliz"), 210),
        (M1.rey_maya(0, "feliz"), 420),
        (M1.moctezuma(0, "serio"), 630),
        (M1.sor_juana(0, "feliz"), 840),
        (M1.hidalgo(0, "enojo"), 1050),
        (M1.juarez(0, "serio"), 1260),
        (M1.zapata(0, "serio"), 1470),
        (M1.frida_kahlo(0, "feliz"), 1690),
    ]
    for k, (dib, x) in enumerate(desfile):
        pa(R, dib, x, 1010, 0.84, i0 + 0.1 * k, FIN(e) + 1.2, sem=250 + k, entra="sube", dy=320, flip=k >= 4)
    R.snd(i0 + 0.1, "pasos", 0.35, dur=2.2)

    ga(R, M2.aguila_nopal(), CI["cdmx"], t_rai - 0.2, FIN(e) + 1.2, s=0.52, off=(0, -10), sem=258, zs=0.45, z=2,
       entra="sube", dy=280, extra=[(0.05, "brillo", 0.45)])
    titulo(R, t_cho - 0.1, t_que - 0.1, "TRES MIL AÑOS DE HISTORIA", px=78)

    # pregunta final y llamada a la acción
    titulo(R, t_que, FIN(e) + 1.2, "¿QUÉ PAÍS O IMPERIO SIGUE?", px=78)
    R.texto(t_dim, FIN(e) + 1.1, "¡DÍMELO ABAJO!", (1520, 320), px=56, d=0.4)
    R.texto(t_com - 0.2, FIN(e) + 1.1, "SUSCRÍBETE", (680, 320), px=68, d=0.5)
    pa(R, C.campana(), 1050, 315, 0.82, t_com - 0.3, FIN(e) + 1.2, sem=260, extra=[(0.08, "campana", 0.5)])


# ------------------------------------------------------------------ cambios de escena procedurales
def _transiciones(R):
    tipos = ["tinta", "pincel", "papel", "portal", "rollo", "puntos", "ola", "pincel", "tinta", "papel", "persianas", "portal", "rollo"]
    colores = [
        (72, 152, 126), (208, 76, 58), (204, 66, 54), (188, 56, 52), (218, 158, 58), (74, 146, 98),
        (86, 148, 98), (74, 138, 104), (196, 146, 68), (206, 112, 58), (76, 144, 98), (56, 138, 84), (236, 186, 58),
    ]
    ids = [e["id"] for e in __import__("escena_base").TL["escenas"]]
    centros = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]
    for k, tc in enumerate(centros):
        tipo, color = tipos[k % len(tipos)], colores[k % len(colores)]
        R.trans.append(Transicion(tc, tipo, color, (960, 540), (960, 540), dur=0.8, seed=k + 1))
        R.snd(tc - 0.4, SFX[tipo], 0.45, dur=0.8)
