# -*- coding: utf-8 -*-
"""Coreografía (3/4): la primera República y la pérdida del norte (Imperio de Iturbide, Constitución Federal de 1824, golpes y deudas,
separación de Texas en 1836, guerra con Estados Unidos en 1846-1848 y Tratado de Guadalupe Hidalgo), la Reforma y el Segundo Imperio
(Benito Juárez, Constitución de 1857 y separación Iglesia-Estado, intervención francesa y Batalla de Puebla del 5 de mayo de 1862,
Maximiliano de Habsburgo, resistencia de Juárez en el norte y triunfo republicano de 1867) y el Porfiriato (Porfirio Díaz durante más de
30 años, 20.000 km de ferrocarriles, telégrafo, electricidad y petróleo, el Centenario y el Palacio de Bellas Artes, desigualdad agraria).
Capas de territorio: 0 = México, 1 = Texas / territorio perdido / Imperio de Maximiliano, 2 = Estados Unidos."""
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
    _perdida_norte(R)
    _reforma(R)
    _porfiriato(R)


# ------------------------------------------------------------------ REPÚBLICA Y PÉRDIDA DEL NORTE (1822-1848)
def _perdida_norte(R):
    e = "perdida_norte"
    i0 = INI(e)
    t_imp, t_itu, t_vein, t_conv, t_rep, t_fed = (T(e, "imperio"), T(e, "iturbide"), T(e, "veinticuatro"), T(e, "convierte"),
                                                  T(e, "republica"), T(e, "federal"))
    t_pero, t_gol, t_deu, t_luc, t_lib, t_con = (T(e, "pero"), T(e, "golpes"), T(e, "deudas"), T(e, "lucha"),
                                                 T(e, "liberales"), T(e, "conservadores"))
    t_tre, t_pro, t_tex, t_sep, t_diez, t_gue, t_eeuu = (T(e, "treinta"), T(e, "provincia"), T(e, "texas"), T(e, "separa"),
                                                         T(e, "diez"), T(e, "guerra"), T(e, "estados"))
    t_ejer, t_ocu, t_cap, t_cua, t_pie, t_mit, t_terr = (T(e, "ejercito"), T(e, "ocupa"), T(e, "capital"), T(e, "cuarenta"),
                                                         T(e, "pierde"), T(e, "mitad"), T(e, "territorio"))

    # cámara: todo el México de 1824 (de California a Yucatán) -> Texas y frontera norte -> ocupación y pérdida de 1848
    R.camara(i0 - 0.2, -102.0, 23.8, 1.10)
    R.camara(t_pero + 0.2, -101.8, 23.6, 1.45)
    R.camara(t_tre + 0.1, -101.8, 24.0, 1.15)
    R.camara(FIN(e) + 0.4, -102.0, 23.8, 1.12)

    # años
    R.anio(i0 + 0.1, 1822)
    R.anio(t_vein, 1824)
    R.anio(t_tre, 1836)
    R.anio(t_gue - 0.2, 1846)
    R.anio(t_cua, 1848)

    # frase 0: del breve Imperio de Iturbide a la República Federal de 1824
    R.terreno(t_vein - 0.1, "mexico_1824", COL["mexico_1824"], 1.0)
    pa(R, M1.iturbide(0, "serio", True), 320, 1010, 1.1, i0, t_pero, sem=150, sale="izq_fuera", d_out=0.5)
    R.texto(t_imp, t_vein - 0.1, "I IMPERIO (1822)", (320, 580), px=44, d=0.35)
    pa(R, M2.libro_constitucion("1824"), 960, 990, 0.96, t_vein - 0.1, t_pero, sem=151, entra="sube", dy=300,
       extra=[(0.05, "fanfarria", 0.4)])
    titulo(R, t_rep - 0.1, t_pero - 0.1, "REPÚBLICA FEDERAL (1824)", px=76)
    R.sello(t_rep, "gorro", "REPÚBLICA (1824)", color=(198, 56, 52))

    # frase 1: golpes militares, deudas externas y lucha entre liberales y conservadores
    R.romper("caudillos_xix", t_gol - 0.1, t_gol + 0.5, t_tre - 0.3, t_tre + 0.2, capa=0, gap=12.0, deriva=22.0)
    R.snd(t_gol, "crujido", 0.45, dur=0.8)
    pa(R, M1.soldado_mx_xix(0, "enojo"), 320, 1010, 1.04, t_gol - 0.1, t_tre, sem=152)
    R.texto(t_lib - 0.1, t_tre - 0.1, "LIBERALES", (320, 600), px=44, d=0.35)
    pa(R, M1.iturbide(0, "enojo"), 1580, 1010, 1.04, t_con - 0.2, t_tre, sem=153, flip=True)
    R.texto(t_con - 0.1, t_tre - 0.1, "CONSERVADORES", (1580, 600), px=44, d=0.35)
    pa(R, A.bolsa_dinero(), 960, 1000, 0.72, t_deu - 0.1, t_tre, sem=154, extra=[(0.05, "monedas", 0.4)])
    R.texto(t_deu, t_tre - 0.1, "DEUDA EXTERNA", (960, 770), px=44, d=0.35)
    ga(R, A.espadas(), CI["cdmx"], t_luc - 0.1, t_tre, s=0.45, off=(0, -30), sem=155, zs=0.35, z=3,
       extra=[(0.05, "espada", 0.5)])
    titulo(R, t_gol, t_tre - 0.1, "GOLPES Y LUCHAS INTERNAS", px=72)

    # frase 2: 1836 separación de Texas; 1846 estalla la guerra contra Estados Unidos
    R.terreno(t_tex - 0.1, "texas_1836", COL["texas"], 0.9, capa=1)
    R.terreno(t_tex - 0.1, "mexico_1836", COL["mexico_1824"], 0.9)
    ciudad(R, t_tex - 0.1, t_gue - 0.3, "alamo", "SAN ANTONIO", "abajo", 40)
    lugar(R, t_tex, t_gue - 0.3, "TEXAS (1836)", (-99.5, 26.2), off=(0, 0), px=46)
    R.snd(t_sep, "crujido", 0.45, dur=0.7)

    R.terreno(t_gue - 0.2, "eeuu_1846", COL["eeuu"], 1.0, capa=2)
    lugar(R, t_eeuu - 0.1, t_ejer - 0.2, "ESTADOS UNIDOS", (-97.5, 26.2), off=(0, 0), px=44)
    R.ruta(M.RUTAS["eeuu_norte"], t_gue - 0.1, 1.6, ancho=5.0, t1=t_pie, flecha=True)
    R.ruta(M.RUTAS["eeuu_ oeste"], t_gue, 1.8, ancho=5.0, t1=t_pie, flecha=True)
    R.ruta(M.RUTAS["eeuu_scott"], t_ejer - 0.2, 1.5, ancho=5.0, t1=t_pie + 0.2, flecha=True)
    andar(R, lambda p: M3.jinete(p, "eeuu"), M.RUTAS["eeuu_norte"], t_gue, 1.8, t1=t_pie, s=0.34, sem=156, zs=0.4, z=3, fps=8)
    andar(R, lambda p: M3.jinete(p, "eeuu"), M.RUTAS["eeuu_ oeste"][1:], t_gue + 0.1, 1.7, t1=t_pie, s=0.34, sem=157, zs=0.4, z=3, fps=8)
    R.snd(t_gue, "canonazo", 0.48)
    titulo(R, t_gue - 0.1, t_ejer - 0.1, "GUERRA CON ESTADOS UNIDOS (1846)", px=70)

    # frase 3: ocupación de la capital y pérdida de más de la mitad del territorio en 1848
    ciudad(R, t_cap - 0.2, FIN(e) + 0.3, "cdmx", "CIUDAD DE MÉXICO", "izq", 40)
    pa(R, M1.soldado_eeuu(0, "enojo"), 320, 1010, 1.08, t_ejer - 0.1, FIN(e) + 0.3, sem=158)
    pa(R, M1.soldado_mx_xix(0, "serio"), 1580, 1010, 1.08, t_ejer, FIN(e) + 0.3, sem=159, flip=True)
    R.terreno(t_pie - 0.1, "perdido_1848", COL["perdido"], 1.2, capa=1)
    R.terreno(t_pie - 0.1, "mexico_mod", COL["mexico_mod"], 1.2)
    R.terreno(t_pie + 0.8, None, COL["eeuu"], 0.8, capa=2)
    lugar(R, t_pie + 0.1, FIN(e) + 0.3, "TERRITORIO CEDIDO (1848)", (-106.5, 25.8), off=(0, 0), px=44)
    R.contador(t_mit - 0.2, t_terr + 0.2, 0, 55, (960, 196), px=84, formato="-{} % DEL TERRITORIO", hasta_t=FIN(e) + 0.3)
    R.snd(t_pie, "impacto", 0.5)


# ------------------------------------------------------------------ LA REFORMA Y EL SEGUNDO IMPERIO (1857-1867)
def _reforma(R):
    e = "reforma"
    i0 = INI(e)
    t_gen, t_ben, t_jua, t_pro, t_cons, t_sep, t_igl, t_est = (T(e, "generacion"), T(e, "benito"), T(e, "juarez", frase=0),
                                                               T(e, "promulga"), T(e, "constitucion"), T(e, "separa"),
                                                               T(e, "iglesia"), T(e, "estado"))
    t_ses, t_tro, t_fra, t_inv, t_der, t_cin, t_may, t_pue = (T(e, "sesenta", frase=1), T(e, "tropas"), T(e, "francia"),
                                                              T(e, "invaden"), T(e, "derrotadas"), T(e, "cinco"),
                                                              T(e, "mayo"), T(e, "puebla"))
    t_reg, t_imp, t_seg, t_arc, t_max, t_hab = (T(e, "regresan"), T(e, "imponen"), T(e, "segundo"), T(e, "archiduque"),
                                                T(e, "maximiliano"), T(e, "habsburgo"))
    t_jua2, t_res, t_nor, t_siete, t_tri, t_rest = (T(e, "juarez", frase=3), T(e, "resiste"), T(e, "norte"),
                                                    T(e, "siete", frase=3), T(e, "triunfan"), T(e, "restauran"))

    # cámara: centro de México -> Veracruz y Puebla -> país dividido entre el Imperio y el norte republicano -> Querétaro y CDMX
    R.camara(i0 - 0.2, -99.5, 20.2, 3.2)
    R.camara(t_ses + 0.1, -97.6, 19.2, 4.4)
    R.camara(t_der - 0.1, -97.9, 19.1, 4.6)
    R.camara(t_reg - 0.2, -97.9, 19.1, 4.6)
    R.camara(t_reg + 0.3, -101.8, 23.6, 1.65)
    R.camara(t_nor + 0.2, -103.2, 26.2, 1.55)
    R.camara(t_siete - 0.2, -103.2, 26.2, 1.55)
    R.camara(t_tri + 0.2, -100.2, 21.6, 2.2)
    R.camara(FIN(e) + 0.4, -100.2, 21.6, 2.2)

    # años
    R.anio(i0 + 0.1, 1857)
    R.anio(t_ses, 1862)
    R.anio(t_seg, 1864)
    R.anio(t_siete - 0.2, 1867)

    # limpiamos territorio perdido del norte y pintamos la República liberal
    R.terreno(i0 - 0.3, None, COL["perdido"], 0.6, capa=1)
    R.terreno(i0 - 0.2, "mexico_mod", COL["reforma_lib"], 0.9)

    # frase 0: Benito Juárez, Constitución de 1857 y separación Iglesia-Estado
    pa(R, M1.juarez(0, "serio"), 310, 1010, 1.15, t_ben - 0.2, t_ses, sem=160, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_ben, t_ses - 0.1, "BENITO JUÁREZ", (310, 560), px=48, d=0.4)
    pa(R, M2.libro_constitucion("1857"), 860, 990, 0.94, t_cons - 0.15, t_ses, sem=161, entra="sube", dy=280,
       extra=[(0.05, "escribir", 0.4, {"dur": 0.8})])
    R.texto(t_cons, t_ses - 0.1, "CONSTITUCIÓN DE 1857", (860, 740), px=42, d=0.4)
    pa(R, M2.catedral_virreinal(), 1420, 1010, 0.48, t_sep - 0.1, t_ses, sem=162)
    titulo(R, t_sep - 0.1, t_ses - 0.1, "LEYES DE REFORMA", px=78)
    R.sello(t_cons + 0.1, "balanza", "LA REFORMA", color=(74, 138, 104))

    # frase 1: 1862 invasión francesa y heroica Batalla de Puebla (5 de mayo)
    R.ruta(M.RUTAS["francia_inv"][:3], t_fra - 0.2, 1.4, ancho=5.0, t1=t_reg - 0.2, flecha=True)
    ciudad(R, t_fra, t_der - 0.2, "veracruz", "VERACRUZ", "der", 42)
    ciudad(R, t_cin - 0.1, t_reg - 0.3, "puebla", "PUEBLA (5 MAYO 1862)", "abajo", 44)
    ga(R, M2.fuerte_puebla(), CI["puebla"], t_der - 0.2, t_reg - 0.2, s=0.52, off=(0, -10), sem=163, zs=0.5, z=2,
       entra="sube", dy=280, extra=[(0.05, "canonazo", 0.5)])
    grupo(R, lambda p: M1.soldado_frances(p % 2, "enojo"), M.RUTAS["francia_inv"][:3], t_fra - 0.1, 1.4, n=2, ancho=85,
          t1=t_reg - 0.2, s=0.38, sem=164, fps=6)
    ga(R, A.espadas(), CI["puebla"], t_cin, t_reg - 0.2, s=0.44, off=(110, -40), sem=166, zs=0.4, z=4,
       extra=[(0.05, "espada", 0.55)])
    pa(R, M1.zaragoza(0, "enojo"), 320, 1010, 1.1, t_der - 0.1, t_reg, sem=167, extra=[(0.05, "fanfarria", 0.4)])
    R.texto(t_der + 0.1, t_reg - 0.1, "IGNACIO ZARAGOZA", (330, 580), px=44, d=0.4)
    pa(R, M1.soldado_frances(0, "enojo"), 1580, 1010, 1.06, t_fra - 0.1, t_reg, sem=168, flip=True)
    titulo(R, t_cin - 0.1, t_reg - 0.1, "¡VICTORIA EN PUEBLA! (5 DE MAYO)", px=72)

    # frase 2: Segundo Imperio bajo Maximiliano de Habsburgo (1864-1867)
    R.terreno(t_imp - 0.1, "imperio_max", COL["imperio_max"], 1.1, capa=1)
    R.terreno(t_imp - 0.1, "republica_juarez", COL["reforma_lib"], 1.1)
    pa(R, M1.maximiliano(0, "serio"), 1560, 1010, 1.12, t_seg - 0.1, t_tri, sem=169, flip=True,
       extra=[(0.05, "cuerno", 0.38)])
    R.texto(t_max - 0.1, t_tri - 0.1, "MAXIMILIANO DE HABSBURGO", (1480, 580), px=42, d=0.4)
    titulo(R, t_seg - 0.1, t_jua2 - 0.1, "SEGUNDO IMPERIO (1864)", px=74)

    # frase 3: Juárez resiste en el norte (Paso del Norte) y restaura la República en 1867
    ciudad(R, t_nor + 0.1, t_siete - 0.3, "paso_norte", "PASO DEL NORTE", "abajo", 42)
    ciudad(R, t_tri + 0.1, FIN(e) + 0.3, "queretaro", "QUERÉTARO (1867)", "izq", 44)
    R.ruta(M.RUTAS["juarez_norte"], t_jua2 - 0.1, 1.4, ancho=4.5, t1=t_tri, flecha=True)
    R.ruta(M.RUTAS["juarez_regreso"], t_siete - 0.3, 1.6, ancho=5.0, t1=FIN(e) + 0.3, flecha=True)
    pa(R, M1.juarez(0, "serio"), 320, 1010, 1.15, t_jua2 - 0.1, FIN(e) + 0.3, sem=170,
       extra=[(0.05, "fanfarria", 0.45)])
    R.texto(t_jua2 + 0.1, FIN(e) + 0.2, "REPÚBLICA RESTAURADA", (340, 560), px=44, d=0.4)
    R.terreno(t_tri - 0.1, None, COL["imperio_max"], 0.9, capa=1)
    R.terreno(t_tri - 0.1, "mexico_mod", COL["mexico_mod"], 1.1)
    titulo(R, t_tri - 0.1, FIN(e) + 0.3, "¡TRIUNFA LA REPÚBLICA! (1867)", px=74)


# ------------------------------------------------------------------ EL PORFIRIATO (1876-1911)
def _porfiriato(R):
    e = "porfiriato"
    i0 = INI(e)
    t_set, t_pod, t_por, t_gob, t_tre = T(e, "setenta"), T(e, "poder"), T(e, "porfirio"), T(e, "gobierna"), T(e, "treinta")
    t_ord, t_pro, t_vein, t_vias, t_tel, t_ele, t_pet = (T(e, "orden"), T(e, "progreso"), T(e, "veinte"), T(e, "vias"),
                                                         T(e, "telegrafo"), T(e, "electricidad"), T(e, "petrolero"))
    t_ciu, t_pal, t_tea, t_cen, t_ind = T(e, "ciudades"), T(e, "palacios"), T(e, "teatros"), T(e, "centenario"), T(e, "independencia")
    t_pero, t_riq, t_hac, t_cam, t_obr, t_tie, t_der = (T(e, "pero"), T(e, "riqueza"), T(e, "haciendas"), T(e, "campesinos"),
                                                        T(e, "obreros"), T(e, "tierras"), T(e, "derechos"))

    # cámara: plano general con las grandes líneas férreas -> acercamiento a la capital del Centenario -> campo y minas
    R.camara(i0 - 0.2, -101.8, 23.8, 1.55)
    R.camara(t_ciu - 0.2, -101.5, 24.0, 1.50)
    R.camara(t_ciu + 0.3, -99.13, 19.45, 5.2)
    R.camara(t_pero - 0.2, -99.13, 19.45, 5.2)
    R.camara(t_pero + 0.3, -100.2, 21.2, 2.8)
    R.camara(FIN(e) + 0.4, -100.5, 21.5, 2.5)

    # años
    R.anio(i0 + 0.1, 1876)
    R.anio(t_vein, 1895)
    R.anio(t_cen - 0.2, 1910)

    # frase 0: Porfirio Díaz gobierna más de 30 años
    R.terreno(i0 - 0.1, "mexico_mod", COL["porfiriato"], 1.0)
    pa(R, M1.porfirio_diaz(0, "serio"), 310, 1010, 1.15, i0, FIN(e) + 0.3, sem=175, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_por - 0.1, FIN(e) + 0.2, "PORFIRIO DÍAZ", (310, 560), px=48, d=0.4)
    R.contador(t_tre - 0.2, t_tre + 0.6, 0, 30, (960, 196), px=84, formato="+{} AÑOS EN EL PODER", hasta_t=t_ord - 0.1)
    R.snd(t_tre - 0.2, "reloj_rapido", 0.35, dur=0.8)

    # frase 1: Orden y Progreso, 20.000 km de vías férreas, telégrafo, electricidad y petróleo
    R.ruta(M.RUTAS["ferrocarril_norte"], t_ord, 2.4, ancho=5.0, t1=FIN(e) + 0.2, flecha=True)
    R.ruta(M.RUTAS["ferrocarril_golfo"], t_pro, 1.6, ancho=5.0, t1=FIN(e) + 0.2, flecha=True)
    andar(R, lambda p: M3.locomotora(p), M.RUTAS["ferrocarril_norte"], t_ord + 0.1, 3.0, t1=t_ciu - 0.2, s=0.42,
          sem=176, zs=0.45, z=3, fps=6)
    R.snd(t_vias - 0.2, "siseo", 0.45, dur=1.2)
    R.contador(t_vein - 0.1, t_vias + 0.4, 0, 20_000, (960, 196), px=80, formato="{:,} KM DE VÍAS FÉRREAS", hasta_t=t_ciu - 0.2)
    R.sello(t_vias, "locomotora", "PORFIRIATO", color=(196, 146, 68))
    ciudad(R, t_pet - 0.2, t_ciu - 0.3, "tampico", "TAMPICO", "abajo", 42)
    ga(R, M2.torre_petroleo(), CI["tampico"], t_pet - 0.2, t_ciu - 0.2, s=0.42, off=(0, -18), sem=177, zs=0.45, z=2,
       entra="sube", dy=260)
    pa(R, C.fabrica(), 820, 1010, 0.65, t_ele - 0.2, t_ciu - 0.1, sem=178, extra=[(0.05, "bling", 0.4)])
    R.texto(t_ele - 0.1, t_ciu - 0.2, "ELECTRICIDAD Y TELÉGRAFO", (820, 740), px=38, d=0.4)

    # frase 2: palacios, teatros y el Centenario de la Independencia (1910)
    ciudad(R, t_ciu + 0.3, t_pero - 0.2, "cdmx", "CIUDAD DE MÉXICO", "abajo", 46)
    ga(R, M2.palacio_bellas_artes(), CI["cdmx"], t_pal - 0.1, FIN(e) + 0.2, s=0.52, off=(-140, -10), sem=179, zs=0.5, z=2,
       entra="pluma", d_in=1.0, extra=[(0.05, "crece", 0.45)])
    ga(R, M2.angel_independencia(), CI["cdmx"], t_cen - 0.2, FIN(e) + 0.2, s=0.52, off=(150, -10), sem=180, zs=0.5, z=2,
       entra="sube", dy=320, extra=[(0.05, "brillo", 0.45)])
    titulo(R, t_cen - 0.1, t_pero - 0.1, "EL CENTENARIO (1910)", px=78)

    # frase 3: haciendas vs millones de campesinos y obreros sin tierras y sin derechos
    pa(R, A.bolsa_dinero(), 740, 1010, 0.85, t_riq - 0.1, FIN(e) + 0.3, sem=181, extra=[(0.05, "monedas", 0.4)])
    R.texto(t_hac - 0.1, FIN(e) + 0.2, "GRANDES HACIENDAS", (740, 760), px=40, d=0.4)
    pa(R, M1.campesino_pre(0, "serio"), 1260, 1010, 1.04, t_cam - 0.1, FIN(e) + 0.3, sem=182)
    pa(R, M1.minero_plata(0, "enojo"), 1540, 1010, 1.04, t_obr - 0.1, FIN(e) + 0.3, sem=183, flip=True)
    R.texto(t_tie - 0.1, FIN(e) + 0.2, "SIN TIERRAS NI DERECHOS", (1400, 590), px=42, d=0.4)
    titulo(R, t_pero + 0.1, FIN(e) + 0.2, "DESIGUALDAD SOCIAL", px=76)
