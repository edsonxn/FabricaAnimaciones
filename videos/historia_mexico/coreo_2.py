# -*- coding: utf-8 -*-
"""Coreografía (2/4): la Conquista (desembarco de Hernán Cortés en Veracruz en 1519, caballos y cañones, la alianza con los tlaxcaltecas,
el asedio de Tenochtitlan, la epidemia de viruela y la caída de agosto de 1521, nacimiento de la Nueva España), el Virreinato de la Nueva
España (300 años de Centroamérica a California y Texas, minas de plata de Zacatecas y Guanajuato, el Galeón de Manila y la ruta de Veracruz,
sociedad mestiza y arte barroco, Sor Juana Inés de la Cruz) y la Guerra de Independencia (desigualdad criolla, el Grito de Dolores de Miguel
Hidalgo el 16 de septiembre de 1810, José María Morelos y el Congreso de Chilpancingo, Vicente Guerrero en las montañas y el Plan de Iguala
con Agustín de Iturbide en 1821).
Capas de territorio: 0 = Imperio mexica -> Nueva España -> Imperio de Iturbide, 1 = Tlaxcala / insurgentes, 50 = lago de Texcoco."""
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


def cortes(R):
    pass


def construir(R):
    _conquista(R)
    _virreinato(R)
    _independencia(R)


# ------------------------------------------------------------------ CONQUISTA (1519-1521)
def _conquista(R):
    e = "conquista"
    i0 = INI(e)
    t_mil, t_her, t_des, t_ver, t_qui, t_cab, t_can = (T(e, "mil", frase=0), T(e, "hernan"), T(e, "desembarca"), T(e, "veracruz"),
                                                       T(e, "quinientos"), T(e, "caballos"), T(e, "canones"))
    t_riv, t_tla, t_unen, t_der = T(e, "rivales"), T(e, "tlaxcaltecas"), T(e, "unen"), T(e, "derribar")
    t_ase, t_agua, t_epi, t_vir, t_ten, t_cae, t_ago = (T(e, "asedio"), T(e, "agua"), T(e, "epidemia"), T(e, "viruela"),
                                                        T(e, "tenochtitlan"), T(e, "cae"), T(e, "agosto"))
    t_rui, t_tem, t_lev, t_cap, t_virr, t_esp = (T(e, "ruinas"), T(e, "templos"), T(e, "levanta"), T(e, "capital"),
                                                 T(e, "virreinato"), T(e, "espana", frase=3))

    # cámara: ruta marítima a Veracruz -> avance por Tlaxcala -> asedio de Tenochtitlan
    R.camara(i0 - 0.2, -91.5, 20.2, 2.5)
    R.camara(t_ver + 0.2, -96.5, 19.3, 4.6)
    R.camara(t_riv - 0.2, -96.5, 19.3, 4.6)
    R.camara(t_tla + 0.1, -98.2, 19.35, 5.2)
    R.camara(t_ase - 0.2, -98.2, 19.35, 5.2)
    R.camara(t_ase + 0.2, -99.1, 19.44, 6.8)
    R.camara(FIN(e) + 0.4, -99.1, 19.44, 6.2)

    # años
    R.anio(i0 + 0.1, 1519)
    R.anio(t_epi, 1520)
    R.anio(t_cae, 1521)

    # frase 0: Hernán Cortés desembarca en Veracruz con 500 soldados, caballos y cañones
    R.ruta(M.RUTAS["cortes_mar"], i0 - 0.2, 1.8, ancho=5.0, t1=t_riv + 0.2, flecha=True)
    for k in range(2):
        andar(R, lambda p, k=k: M3.galeon(p + k), M.RUTAS["cortes_mar"], i0 - 0.2 + 0.2 * k, 1.9, t1=t_riv + 0.2, s=0.34,
              sem=90 + k, zs=0.4, z=2, fps=4, off=formacion(k, 2, 140), flip=True)
    R.snd(i0, "ola", 0.4, dur=1.2)
    ciudad(R, t_ver - 0.2, t_riv - 0.3, "veracruz", "VERACRUZ (1519)", "der", 44)
    pa(R, M1.cortes(0, "serio"), 290, 1010, 1.12, t_her - 0.1, t_ase - 0.1, sem=92, extra=[(0.05, "cuerno", 0.38)])
    R.texto(t_her + 0.1, t_riv - 0.1, "HERNÁN CORTÉS", (290, 580), px=46, d=0.4)
    pa(R, M1.malinche(0, "serio"), 540, 1010, 1.0, t_ver + 0.1, t_tla - 0.2, sem=93, flip=True)
    pa(R, lambda t: M3.jinete(int(t * 6) % 4, "cortes"), 1220, 1010, 0.72, t_cab - 0.15, t_ase - 0.1, sem=94,
       extra=[(0.05, "galope", 0.4, {"dur": 1.2})])
    pa(R, lambda t: M3.canon(int(t * 3) % 2), 1600, 1010, 0.85, t_can - 0.15, t_ase - 0.1, sem=95,
       extra=[(0.05, "canonazo", 0.48)])
    R.contador(t_qui - 0.2, t_qui + 0.6, 0, 500, (960, 196), px=80, formato="{} SOLDADOS", hasta_t=t_riv - 0.1)

    # frase 1: alianza con los guerreros tlaxcaltecas y marcha hacia Tenochtitlan
    R.ruta(M.RUTAS["cortes_tierra"], t_riv - 0.1, 2.2, ancho=5.0, t1=t_rui, flecha=True)
    ciudad(R, t_tla + 0.2, t_ase - 0.3, "tlaxcala", "TLAXCALA", "arriba", 42)
    andar(R, lambda p: M3.jinete(p, "cortes"), M.RUTAS["cortes_tierra"], t_riv, 2.3, t1=t_ase + 0.4, s=0.32, sem=96, zs=0.4, z=3, fps=8)
    R.snd(t_tla, "pasos", 0.4, dur=1.8)
    pa(R, M1.tlaxcalteca(0, "enojo"), 740, 1010, 1.05, t_tla - 0.1, t_ase - 0.1, sem=100)
    R.texto(t_tla + 0.1, t_ase - 0.2, "ALIADOS TLAXCALTECAS", (740, 590), px=42, d=0.4)
    titulo(R, t_unen - 0.1, t_ase - 0.1, "ALIANZA CONTRA EL IMPERIO", px=72)

    # frase 2: asedio por agua y tierra, epidemia de viruela y caída de Tenochtitlan (13-ago-1521)
    ciudad(R, t_ase + 0.2, FIN(e) + 0.3, "tenochtitlan", "TENOCHTITLAN", "abajo", 48)
    ga(R, M2.templo_mayor(), CI["tenochtitlan"], t_ase - 0.2, t_rui + 0.1, s=0.55, off=(0, 0), sem=101, zs=0.5, z=2)
    ga(R, A.espadas(), CI["tenochtitlan"], t_ase + 0.1, t_rui, s=0.44, off=(-130, -40), sem=102, zs=0.4, z=4,
       extra=[(0.05, "espada", 0.55)])
    for k in range(2):
        ga(R, lambda t, k=k: A.llama(int(t * 8) + k), CI["tenochtitlan"], t_agua + 0.12 * k, t_rui, s=0.34,
           off=(-80 + 160 * k, 20), sem=103 + k, zs=0.4, z=4, extra=[(0.0, "fuego", 0.4, {"dur": 1.4})] if k == 0 else ())
    ga(R, M2.epidemia_nube(), CI["tenochtitlan"], t_epi - 0.1, t_rui, s=0.52, off=(0, -140), sem=105, zs=0.45, z=3,
       entra="sube", dy=220, extra=[(0.05, "viento", 0.45, {"dur": 1.4})])
    R.texto(t_vir - 0.1, t_cae - 0.2, "EPIDEMIA DE VIRUELA", (340, 560), px=44, d=0.4)
    pa(R, M1.guerrero_aguila(0, "enojo"), 340, 1010, 1.04, t_ase, t_rui, sem=106)
    pa(R, M1.soldado_esp(0, "enojo"), 1320, 1010, 1.04, t_ase + 0.1, t_rui, sem=107, flip=True)
    R.terreno(t_cae - 0.1, "conquista_1521", COL["conquista"], 1.1)
    R.terreno(t_cae, None, COL["tlaxcala"], 0.7, capa=1)
    R.sello(t_cae, "espadas", "CONQUISTA", color=(188, 56, 52))
    titulo(R, t_cae - 0.1, t_rui - 0.1, "CAÍDA DE TENOCHTITLAN (1521)", px=72)

    # frase 3: de los templos indígenas a la capital del Virreinato de la Nueva España
    R.terreno(t_rui, None, M.AGUA_LAGO, 1.2, capa=50)
    R.morf(M2.templo_mayor(), M2.catedral_virreinal(), t_lev - 0.1, 0.8, (960, 1010, 1.05), sem=108,
           salida=FIN(e) + 0.3, t_a=t_rui - 0.1)
    R.snd(t_lev, "campana", 0.45)
    titulo(R, t_virr - 0.2, FIN(e) + 0.3, "VIRREINATO DE LA NUEVA ESPAÑA", px=72)


# ------------------------------------------------------------------ VIRREINATO DE LA NUEVA ESPAÑA (1535-1821)
def _virreinato(R):
    e = "virreinato"
    i0 = INI(e)
    t_tre, t_esp, t_ext, t_cen, t_cal, t_tex = (T(e, "trescientos"), T(e, "espana"), T(e, "extiende"), T(e, "centroamerica"),
                                                T(e, "california"), T(e, "texas"))
    t_min, t_zac, t_gua, t_pla, t_com, t_eur, t_asi, t_gal = (T(e, "minas"), T(e, "zacatecas"), T(e, "guanajuato"), T(e, "plata"),
                                                              T(e, "comercio"), T(e, "europa"), T(e, "asia"), T(e, "galeon"))
    t_enc, t_ind, t_esp2, t_afr, t_mes, t_bar = (T(e, "encuentro"), T(e, "indigenas"), T(e, "espanoles"), T(e, "africanos"),
                                                 T(e, "mestiza"), T(e, "barroco"))
    t_let, t_pen, t_sor, t_poe, t_oro = T(e, "letras"), T(e, "pensamiento"), T(e, "sor"), T(e, "poeta"), T(e, "oro")

    # cámara: plano continental de toda la Nueva España -> minas del Bajío y costas -> centro cultural en CDMX
    R.camara(i0 - 0.2, -102.0, 23.6, 1.06)
    R.camara(t_min - 0.2, -102.0, 23.6, 1.06)
    R.camara(t_min + 0.3, -101.5, 20.4, 1.85)
    R.camara(t_enc - 0.2, -101.5, 20.4, 1.85)
    R.camara(t_enc + 0.3, -99.2, 19.6, 4.5)
    R.camara(FIN(e) + 0.4, -99.15, 19.45, 5.2)

    # años
    R.anio(i0 + 0.1, 1535)
    R.anio(t_min, 1565)
    R.anio(t_enc, 1650)
    R.anio(t_sor, 1680)

    # frase 0: 300 años, la Nueva España de Centroamérica a California y Texas
    R.terreno(i0 - 0.1, "nueva_espana", COL["nueva_espana"], 1.5)
    R.snd(i0, "whoosh", 0.45, dur=0.9)
    R.sello(t_ext, "columnas", "NUEVA ESPAÑA", color=(218, 158, 58))
    R.contador(t_tre - 0.2, t_tre + 0.7, 0, 300, (960, 196), px=84, formato="{} AÑOS DE VIRREINATO", hasta_t=t_min - 0.3)
    R.snd(t_tre - 0.2, "reloj_rapido", 0.35, dur=0.9)
    lugar(R, t_cen, t_min - 0.3, "CENTROAMÉRICA", (-95.0, 17.5), off=(0, 0), px=40)
    lugar(R, t_cal, t_min - 0.3, "LAS CALIFORNIAS", (-111.5, 25.8), off=(0, 0), px=42)
    lugar(R, t_tex, t_min - 0.3, "TEXAS Y NUEVO MÉXICO", (-101.5, 25.8), off=(0, 0), px=42)
    pa(R, M1.virrey(0, "serio"), 300, 1010, 1.1, t_esp - 0.1, t_min - 0.1, sem=110, extra=[(0.05, "fanfarria", 0.32)])
    R.texto(t_esp + 0.1, t_min - 0.2, "EL VIRREY", (300, 590), px=46, d=0.4)

    # frase 1: minas de plata de Zacatecas y Guanajuato + Camino Real y Galeón de Manila
    ciudad(R, t_zac, t_enc - 0.3, "zacatecas", "ZACATECAS", "abajo", 42)
    ciudad(R, t_gua - 0.1, t_enc - 0.3, "guanajuato", "GUANAJUATO", "der", 42)
    ciudad(R, t_com, t_enc - 0.3, "acapulco", "ACAPULCO", "abajo", 42)
    ciudad(R, t_com + 0.1, t_enc - 0.3, "veracruz", "VERACRUZ", "der", 42)
    ga(R, M2.cerro_mina_plata(), CI["zacatecas"], t_zac - 0.1, t_enc - 0.3, s=0.46, off=(0, -18), sem=111, zs=0.45, z=2,
       entra="sube", dy=280, extra=[(0.05, "crece", 0.45)])
    ga(R, M2.cerro_mina_plata(), CI["guanajuato"], t_gua - 0.1, t_enc - 0.3, s=0.42, off=(-30, -10), sem=112, zs=0.45, z=2,
       entra="sube", dy=260)
    R.ruta(M.RUTAS["camino_plata"], t_min + 0.2, 2.0, ancho=4.5, t1=t_enc - 0.2, flecha=True)
    R.ruta(M.RUTAS["galeon_manila"], t_asi - 0.3, 2.0, ancho=5.0, t1=t_enc - 0.2, flecha=True)
    R.ruta(M.RUTAS["ruta_veracruz"], t_eur - 0.2, 2.0, ancho=5.0, t1=t_enc - 0.2, flecha=True)
    andar(R, lambda p: M3.galeon(p), M.RUTAS["galeon_manila"], t_asi - 0.3, 2.2, t1=t_enc - 0.2, s=0.38, sem=113, zs=0.4, z=3, fps=4)
    andar(R, lambda p: M3.galeon(p), M.RUTAS["ruta_veracruz"], t_eur - 0.2, 2.2, t1=t_enc - 0.2, s=0.36, sem=114, zs=0.4, z=3, fps=4)
    R.snd(t_gal - 0.2, "ola", 0.4, dur=1.4)
    pa(R, M1.minero_plata(0, "serio"), 290, 1010, 1.05, t_min, t_enc - 0.1, sem=115)
    pa(R, M2.real_de_a_ocho(), 1560, 1010, 0.96, t_pla - 0.15, t_enc - 0.1, sem=116, entra="sube", dy=300,
       extra=[(0.05, "monedas", 0.5)])
    R.texto(t_pla, t_enc - 0.2, "REAL DE A OCHO", (1560, 720), px=44, d=0.4)
    titulo(R, t_gal - 0.2, t_enc - 0.2, "EL GALEÓN DE MANILA", px=74)

    # frase 2: sociedad mestiza, arte barroco y catedrales
    ciudad(R, t_enc + 0.3, FIN(e) + 0.3, "cdmx", "CIUDAD DE MÉXICO", "abajo", 48)
    ciudad(R, t_enc + 0.4, FIN(e) + 0.3, "puebla", "PUEBLA", "der", 42)
    ga(R, M2.catedral_virreinal(), CI["cdmx"], t_enc + 0.2, FIN(e) + 0.3, s=0.55, off=(0, -10), sem=117, zs=0.5, z=2,
       entra="pluma", d_in=1.1, extra=[(0.05, "campana", 0.4)])
    pa(R, M1.campesina_pre(0, "feliz"), 280, 1010, 0.98, t_ind - 0.1, t_let - 0.1, sem=118)
    pa(R, M1.virrey(0, "feliz"), 540, 1010, 0.98, t_esp2 - 0.1, t_let - 0.1, sem=119)
    pa(R, M1.vicente_guerrero(0, "feliz"), 800, 1010, 0.98, t_afr - 0.1, t_let - 0.1, sem=120, flip=True)
    titulo(R, t_mes - 0.1, t_let - 0.1, "SOCIEDAD MESTIZA Y ARTE BARROCO", px=70)

    # frase 3: Sor Juana Inés de la Cruz, la Décima Musa del Siglo de Oro
    pa(R, M1.sor_juana(0, "feliz"), 340, 1010, 1.16, t_let - 0.1, FIN(e) + 0.3, sem=121, extra=[(0.05, "brillo", 0.45)])
    R.texto(t_sor - 0.1, FIN(e) + 0.2, "SOR JUANA INÉS DE LA CRUZ", (380, 580), px=46, d=0.45)
    pa(R, A.rollo_escritura(), 1380, 1010, 0.72, t_pen - 0.1, FIN(e) + 0.3, sem=122, extra=[(0.05, "escribir", 0.4, {"dur": 0.9})])
    pa(R, M2.libro_constitucion("1689"), 1630, 1010, 0.72, t_poe - 0.1, FIN(e) + 0.3, sem=123)
    titulo(R, t_sor, FIN(e) + 0.2, "LA MAYOR POETA DEL SIGLO DE ORO", px=70)


# ------------------------------------------------------------------ INDEPENDENCIA (1810-1821)
def _independencia(R):
    e = "independencia"
    i0 = INI(e)
    t_des, t_nac, t_cri, t_chi, t_lib = T(e, "desigualdad"), T(e, "nacidos"), T(e, "criollos"), T(e, "chispa"), T(e, "libertad")
    t_mad, t_die, t_och, t_hid, t_cam, t_dol, t_reb = (T(e, "madrugada"), T(e, "dieciseis"), T(e, "ochocientos"), T(e, "hidalgo"),
                                                       T(e, "campana"), T(e, "dolores"), T(e, "rebelion"))
    t_mue, t_mor, t_sur, t_chil, t_sob, t_esc = (T(e, "muerte"), T(e, "morelos"), T(e, "sur"), T(e, "chilpancingo"),
                                                 T(e, "soberania"), T(e, "esclavitud"))
    t_mon, t_gue, t_res, t_anos = T(e, "montanas"), T(e, "guerrero"), T(e, "resistencia"), T(e, "guerrillas")
    t_fin, t_vein, t_itu, t_plan, t_igu, t_ind = (T(e, "finalmente"), T(e, "veintiuno"), T(e, "iturbide"), T(e, "plan"),
                                                  T(e, "iguala"), T(e, "independencia"))

    # cámara: Bajío (Dolores, Guanajuato, Guadalajara) -> sur (Chilpancingo, Oaxaca, Acapulco) -> Iguala y Ciudad de México
    R.camara(i0 - 0.2, -101.2, 20.8, 3.6)
    R.camara(t_mue - 0.2, -101.2, 20.8, 3.6)
    R.camara(t_mor + 0.2, -99.2, 17.8, 4.0)
    R.camara(t_fin - 0.2, -99.5, 17.9, 4.0)
    R.camara(t_fin + 0.2, -99.3, 19.0, 4.2)
    R.camara(FIN(e) + 0.4, -99.3, 19.2, 4.0)

    # años
    R.anio(i0 + 0.1, 1808)
    R.anio(t_die, 1810)
    R.anio(t_chil, 1813)
    R.anio(t_gue, 1817)
    R.anio(t_vein, 1821)

    # frase 0: desigualdad entre peninsulares y criollos -> chispa de la libertad
    pa(R, M1.virrey(0, "serio"), 320, 1010, 1.08, i0, t_mad, sem=130)
    R.texto(t_nac, t_mad - 0.1, "PENINSULARES", (320, 600), px=44, d=0.35)
    pa(R, M1.iturbide(0, "enojo"), 1580, 1010, 1.08, t_cri - 0.1, t_mad, sem=131, flip=True)
    R.texto(t_cri, t_mad - 0.1, "CRIOLLOS", (1580, 600), px=44, d=0.35)
    pa(R, lambda t: A.llama(int(t * 8)), 960, 880, 1.05, t_chi - 0.1, t_mad, sem=132,
       extra=[(0.05, "fuego", 0.45, {"dur": 1.2})])
    titulo(R, t_des, t_mad - 0.1, "LA CHISPA DE LA LIBERTAD", px=74)

    # frase 1: 16 de septiembre de 1810, Miguel Hidalgo y la campana de Dolores
    R.terreno(t_die, "insurgentes_1810", COL["insurgentes"], 1.1, capa=1)
    ciudad(R, t_dol - 0.2, t_mue - 0.3, "dolores", "DOLORES (1810)", "arriba", 44)
    ciudad(R, t_dol + 0.1, t_mue - 0.3, "guanajuato", "GUANAJUATO", "abajo", 42)
    R.ruta(M.RUTAS["hidalgo"], t_hid, 2.2, ancho=5.0, t1=t_mue - 0.2, flecha=True)
    grupo(R, lambda p: M1.campesino_pre(p % 2, "enojo"), M.RUTAS["hidalgo"], t_hid + 0.1, 2.2, n=3, ancho=90, t1=t_mue - 0.3,
          s=0.36, sem=133, fps=6)
    pa(R, M1.hidalgo(0, "enojo"), 320, 1010, 1.15, t_hid - 0.2, t_mue - 0.1, sem=136, extra=[(0.05, "campana", 0.55)])
    R.texto(t_hid, t_mue - 0.2, "MIGUEL HIDALGO", (320, 560), px=48, d=0.4)
    pa(R, M2.campana_dolores(), 960, 880, 1.05, t_cam - 0.2, t_mue - 0.1, sem=137, entra="sube", dy=320,
       extra=[(0.05, "campana", 0.55)])
    titulo(R, t_die - 0.1, t_mue - 0.1, "¡GRITO DE DOLORES! (16 SEP 1810)", px=72)
    R.sello(t_cam, "campana", "GRITO DE DOLORES", color=(74, 146, 98))

    # frase 2: José María Morelos, campañas del sur y Congreso de Chilpancingo (1813)
    R.terreno(t_mor - 0.1, "morelos_sur", COL["morelos"], 1.0, capa=1)
    ciudad(R, t_chil - 0.1, t_mon - 0.2, "chilpancingo", "CHILPANCINGO (1813)", "arriba", 44)
    ciudad(R, t_sur + 0.2, t_mon - 0.2, "acapulco", "ACAPULCO", "abajo", 40)
    ciudad(R, t_sur + 0.3, t_mon - 0.2, "oaxaca", "OAXACA", "der", 42)
    R.ruta(M.RUTAS["morelos"], t_mor + 0.1, 2.0, ancho=5.0, t1=t_fin - 0.2, flecha=True)
    andar(R, lambda p: M3.jinete(p, "insurgente"), M.RUTAS["morelos"], t_mor + 0.1, 2.2, t1=t_fin - 0.2, s=0.36, sem=138, zs=0.4, z=3, fps=8)
    R.snd(t_mor, "galope", 0.45, dur=1.8)
    pa(R, M1.morelos(0, "serio"), 310, 1010, 1.14, t_mor - 0.1, t_mon - 0.1, sem=139, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_mor + 0.1, t_mon - 0.2, "JOSÉ MARÍA MORELOS", (330, 580), px=44, d=0.4)
    pa(R, M2.libro_constitucion("1813"), 1540, 1010, 0.88, t_chil - 0.1, t_mon - 0.1, sem=140, entra="sube", dy=280,
       extra=[(0.05, "escribir", 0.4, {"dur": 0.8})])
    R.texto(t_sob - 0.1, t_mon - 0.2, "SENTIMIENTOS DE LA NACIÓN", (1520, 740), px=38, d=0.4)
    titulo(R, t_esc - 0.2, t_mon - 0.1, "FIN DE LA ESCLAVITUD", px=74)

    # frase 3: Vicente Guerrero y la resistencia en las montañas del sur
    pa(R, M1.vicente_guerrero(0, "serio"), 320, 1010, 1.1, t_gue - 0.15, FIN(e) + 0.3, sem=141, extra=[(0.05, "espada", 0.45)])
    R.texto(t_gue, FIN(e) + 0.2, "VICENTE GUERRERO", (330, 590), px=44, d=0.4)
    lugar(R, t_mon + 0.1, t_fin - 0.2, "SIERRA DEL SUR", (-99.8, 17.9), off=(0, -30), px=44)
    titulo(R, t_res - 0.1, t_fin - 0.1, "LA RESISTENCIA INSURGENTE", px=72)

    # frase 4: 1821, Agustín de Iturbide y Guerrero sellan el Plan de Iguala y consuman la Independencia
    ciudad(R, t_igu - 0.1, FIN(e) + 0.3, "iguala", "IGUALA (1821)", "abajo", 42)
    ciudad(R, t_ind, FIN(e) + 0.3, "cdmx", "CIUDAD DE MÉXICO", "arriba", 46)
    R.ruta(M.RUTAS["trigarante"], t_plan - 0.1, 1.6, ancho=5.0, t1=FIN(e) + 0.3, flecha=True)
    andar(R, lambda p: M3.jinete(p, "trigarante"), M.RUTAS["trigarante"], t_plan - 0.1, 1.5, t1=t_ind - 0.2, s=0.36,
          sem=142, zs=0.4, z=3, fps=8)
    pa(R, M1.iturbide(0, "feliz"), 1540, 1010, 1.1, t_itu - 0.15, FIN(e) + 0.3, sem=143, flip=True,
       extra=[(0.05, "fanfarria", 0.45)])
    R.texto(t_itu, FIN(e) + 0.2, "AGUSTÍN DE ITURBIDE", (1520, 580), px=44, d=0.4)
    R.terreno(t_ind - 0.2, None, COL["morelos"], 0.6, capa=1)
    R.terreno(t_ind - 0.2, "imperio_iturbide", COL["imperio_iturbide"], 1.2)
    titulo(R, t_plan - 0.1, FIN(e) + 0.3, "¡MÉXICO INDEPENDIENTE! (1821)", px=76)

