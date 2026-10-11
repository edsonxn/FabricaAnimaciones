# -*- coding: utf-8 -*-
"""Coreografía (3/4): Reyes Católicos y Colón, el Imperio (rejilla "am") y el Siglo de Oro.
Capas "eu": 0 = Castilla -> España, 4 = Granada, 6 = Aragón, 8 = Portugal, 9 = Navarra, 10 = Francia. Capas "am": 0 = imperio español."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_es1 as E1
import obj_es2 as E2
import obj_es3 as E3
from core import FIN, INI, T, kf
from coreo_util import andar, CI, ciudad, COL, formacion, ga, lugar, mece, pa, titulo
from motor import e_back, e_in, e_inout, e_out, lerp, prog


def t_lepanto():
    return INI("imperio", 5)


def cortes(R):
    R.corte_extra((FIN("imperio", 4) + INI("imperio", 5)) / 2)      # barrido: de América (Felipe II) a Lepanto


def construir(R):
    _reyes(R)
    _imperio(R)
    _siglo_oro(R)


# ------------------------------------------------------------------ REYES CATÓLICOS
def _reyes(R):
    e = "reyes"
    i0 = INI(e)
    t_1469, t_isa, t_cas, t_casa, t_fer, t_ara = T(e, "mil"), T(e, "isabel"), T(e, "castilla"), T(e, "casa"), T(e, "fernando"), T(e, "aragon")
    t_junt, t_coron, t_1492, t_toman, t_gran = T(e, "juntan"), T(e, "coronas"), T(e, "mil", frase=1), T(e, "toman"), T(e, "granada", frase=1)
    t_mismo, t_expul, t_jud, t_baut, t_neb, t_gram = T(e, "mismo"), T(e, "expulsan"), T(e, "judios"), T(e, "bautizan"), T(e, "nebrija"), T(e, "gramatica")
    t_marino, t_genov, t_colon, t_zarpa, t_oeste, t_india = T(e, "marino"), T(e, "genoves"), T(e, "colon"), T(e, "zarpa"), T(e, "oeste"), T(e, "india")
    t_doce, t_oct, t_llega, t_mundo, t_amer = T(e, "doce"), T(e, "octubre"), T(e, "llega"), T(e, "mundo"), T(e, "america")
    # territorio
    R.terreno(t_junt, "castilla_1250", COL["espana"], 1.0)
    R.terreno(t_junt, "aragon_1250", COL["espana"], 1.0, capa=6)
    R.terreno(t_toman, "espana_1492", COL["espana"], 1.2)
    R.terreno(t_toman + 0.6, None, COL["espana"], 0.4, capa=6)
    R.terreno(t_toman - 0.1, None, COL["granada"], 1.2, capa=4)
    R.terreno(FIN(e) + 0.3, "espana_1512", COL["espana"], 0.1)          # Navarra se une en 1512 (bajo el cambio de escena)
    R.terreno(FIN(e) + 0.3, None, COL["navarra"], 0.1, capa=9)
    R.sello(t_ara + 0.2, "yugo", "REYES CATÓLICOS", color=(170, 50, 60))
    R.terreno(i0, "peninsula_am", COL["espana"], 0.1, rej="am")
    R.terreno(t_oeste - 0.3, "espana", COL["espana"], 0.1, rej="am")
    # cámara
    R.camara(i0 - 0.3, -3.6, 40.0, 2.15)
    R.camara(t_coron, -3.6, 39.6, 2.3)
    R.camara(t_gran - 0.3, -3.6, 37.4, 3.8)
    R.camara(t_mismo + 0.2, -3.6, 39.8, 2.3)
    R.camara(t_neb, -3.8, 40.0, 2.4)
    R.camara(t_marino - 0.1, -6.6, 37.3, 3.8)
    R.camara(t_zarpa, -7.6, 36.8, 3.0)
    R.camara(t_oeste + 0.8, -30.0, 28.0, 0.42)
    R.camara(t_doce, -62.0, 25.0, 0.62)
    R.camara(t_llega, -73.2, 24.3, 1.5)
    R.camara(t_mundo + 0.2, -73.6, 23.6, 1.3)
    R.camara(FIN(e) + 0.3, -72.0, 10.0, 0.26)
    R.rejilla(t_oeste - 0.2, "am", 1.0)
    # años
    R.anio(i0, 1250)
    R.anio(t_1469 + 0.6, 1469)
    R.anio(t_1492 - 0.2, 1469)
    R.anio(t_1492 + 0.7, 1492)
    # Isabel y Fernando
    ga(R, E2.isabel(0, "feliz"), (-4.6, 39.3), t_isa - 0.1, t_coron + 0.4, s=0.66, sem=120, z=2, extra=[(0.1, "brillo", 0.4)])
    ga(R, E2.fernando(0, "feliz"), (-0.6, 40.3), t_fer - 0.1, t_coron + 0.4, s=0.66, sem=121, z=2, flip=True, extra=[(0.1, "brillo", 0.4)])
    lugar(R, t_cas - 0.1, t_coron + 0.4, "ISABEL DE CASTILLA", (-4.6, 39.3), off=(0, 60), px=44)
    lugar(R, t_ara - 0.1, t_coron + 0.4, "FERNANDO DE ARAGÓN", (-0.6, 40.3), off=(0, 60), px=44)
    ga(R, E2.anillos(), (-2.6, 39.9), t_casa - 0.1, t_coron + 0.4, s=0.5, off=(0, -60), sem=122, z=3, extra=[(0.1, "campana", 0.5)])
    # toman Granada: Boabdil entrega la llave
    ga(R, E2.boabdil(0, "lloron"), CI["granada"], t_toman - 0.2, t_mismo, s=0.62, off=(-120, 60), sem=123, z=2)
    ga(R, E2.alhambra(), CI["granada"], t_1492 - 0.1, t_mismo, s=0.5, off=(170, 30), sem=124, z=1, snd=("crece", 0.4))
    titulo(R, t_toman - 0.1, t_mismo - 0.1, "GRANADA, 2 DE ENERO DE 1492", px=66)
    R.snd(t_gran, "fanfarria", 0.45)
    # expulsión de los judíos
    Pj = [(-4.02, 39.86), (-2.6, 39.0), (-0.98, 37.6), (0.4, 37.2)]
    for k, mujer in enumerate((False, True, False)):
        andar(R, lambda p, m=mujer: E2.exiliado(p, m), [(x - 0.45 * k, y + 0.25 * k) for x, y in Pj], t_expul + 0.15 * k, 4.2, t1=t_neb, s=0.52,
              sem=125 + k, z=2, fps=4, snd=None, ease=lambda u: u, off=formacion(k, 3, 90))
    titulo(R, t_expul, t_neb - 0.2, "EXPULSIÓN DE LOS JUDÍOS", px=70)
    R.snd(t_expul, "suspiro", 0.5)
    # Nebrija
    pa(R, E2.nebrija(0), 480, 1000, 1.2, t_neb - 0.15, t_marino, sem=128)
    pa(R, E2.gramatica(), 1380, 980, 1.25, t_gram - 0.2, t_marino, sem=129, extra=[(0.1, "papel", 0.5)])
    R.texto(t_gram, t_marino - 0.1, "GRAMÁTICA CASTELLANA", (1380, 520), px=56, d=0.6)
    R.texto(t_neb, t_marino - 0.1, "NEBRIJA", (480, 560), px=60, d=0.4)
    # Colón zarpa hacia el oeste
    pa(R, E2.colon(0, "feliz"), 470, 1000, 1.25, t_genov - 0.15, t_oeste + 0.4, sem=130, extra=[(0.1, "cuerno", 0.4)])
    R.texto(t_colon - 0.05, t_oeste + 0.2, "CRISTÓBAL COLÓN", (470, 560), px=56, d=0.6)
    ciudad(R, t_marino, t_zarpa - 0.1, "palos", "PALOS", "der", 44)
    Pc = M.RUTAS["colon"][:-1] + [(-71.6, 25.2)]
    R.ruta(Pc, t_zarpa - 0.1, (t_llega + 0.2) - t_zarpa, ancho=5.0, t1=FIN(e) + 0.2)
    for k in range(3):
        andar(R, lambda p, k=k: E2.nao(p + k, 1.0 if k == 0 else 0.8), [(x + 0.6 * k, y - 0.5 * k) for x, y in Pc], t_zarpa + 0.2 * k,
              (t_llega + 0.3) - t_zarpa, t1=t_amer, s=0.5, sem=131 + k, zs=0.25, z=2, fps=3, snd=("ola", 0.35) if k == 0 else None, off=formacion(k, 3, 190))
    R.texto(t_india - 0.1, t_doce - 0.2, "¿LA INDIA?", (1300, 300), px=72, d=0.4)
    # América
    ga(R, lambda t: E2.isla_palmera(int(t * 2) % 6), CI["guanahani"], t_doce - 0.2, FIN(e) + 0.5, s=0.5, off=(0, 30), sem=134, z=1, zs=0.3)
    for k in range(2):
        ga(R, E2.taino(k, "asombro"), CI["guanahani"], t_llega + 0.1 * k, FIN(e) + 0.5, s=0.45, off=(-60 + 90 * k, 10), sem=135 + k, z=2, zs=0.3)
    titulo(R, t_doce - 0.1, t_amer - 0.1, "12 DE OCTUBRE DE 1492", y=140, px=72)
    R.texto(t_amer - 0.1, FIN(e) + 0.6, "AMÉRICA", None, px=110, d=0.6, geo=(-63.0, -8.0), off=(0, 0))
    R.snd(t_amer, "fanfarria", 0.5)


# ------------------------------------------------------------------ IMPERIO
def _imperio(R):
    e = "imperio"
    i0 = INI(e)
    t_emp, t_cortes, t_miles, t_alia, t_mex, t_piz, t_incas = (T(e, "empieza"), T(e, "hernan"), T(e, "miles"), T(e, "aliados"), T(e, "mexicas"),
                                                               T(e, "francisco"), T(e, "incas"))
    t_brut, t_guerra, t_epid, t_millo, t_indig = T(e, "brutal"), T(e, "guerra"), T(e, "epidemias"), T(e, "millones"), T(e, "indigenas", frase=1)
    t_mezcla, t_nace, t_cast, t_cruza = T(e, "mezcla"), T(e, "nace"), T(e, "castellano"), T(e, "cruza")
    t_plata, t_potosi, t_zaca, t_vuelve, t_primera = T(e, "plata"), T(e, "potosi"), T(e, "zacatecas"), T(e, "vuelve"), T(e, "primera")
    t_felipe, t_reina, t_nunca, t_sol, t_filip, t_nombre = T(e, "felipe"), T(e, "reina"), T(e, "nunca"), T(e, "sol"), T(e, "filipinas"), T(e, "nombre")
    t_gana, t_lep, t_armada, t_frac, t_ingl = T(e, "gana"), T(e, "lepanto"), T(e, "armada"), T(e, "fracasa"), T(e, "inglaterra")
    tc = (FIN(e, 4) + INI(e, 5)) / 2
    # territorio (rejilla "am")
    R.terreno(i0 - 0.2, "am_1500", COL["imperio"], 0.8, rej="am")
    R.terreno(t_mex - 0.3, "am_1525", COL["imperio"], 1.4, rej="am")
    R.terreno(t_incas - 0.3, "am_1550", COL["imperio"], 1.4, rej="am")
    R.terreno(t_felipe - 0.2, "am_1600", COL["imperio"], 1.6, rej="am")
    R.sello(t_vuelve + 0.1, "columnas", "IMPERIO ESPAÑOL", color=(176, 60, 50))
    # cámara
    R.camara(i0 - 0.3, -88.0, 19.0, 0.9)
    R.camara(t_cortes, -97.6, 19.6, 1.9)
    R.camara(t_mex + 0.4, -98.0, 19.4, 2.1)
    R.camara(t_piz, -78.5, -7.0, 1.15)
    R.camara(t_incas + 0.4, -74.5, -10.5, 1.5)
    R.camara(t_brut + 0.3, -82.0, 4.0, 0.42)
    R.camara(t_indig, -82.0, 4.0, 0.44)
    R.camara(t_mezcla + 0.3, -48.0, 14.0, 0.25)
    R.camara(t_cruza + 0.5, -46.0, 14.0, 0.26)
    R.camara(t_plata + 0.2, -74.0, -2.0, 0.27)
    R.camara(t_vuelve, -62.0, 6.0, 0.26)
    R.camara(t_felipe + 0.3, -121.0, 6.0, 0.152)
    R.camara(t_filip + 0.5, -121.0, 6.0, 0.153)
    R.camara(tc - 0.05, -120.0, 6.0, 0.155)
    R.camara(tc + 0.05, 17.0, 38.6, 2.0)
    R.camara(t_lep + 0.5, 19.0, 38.5, 2.3)
    R.camara(t_armada - 0.4, -1.5, 50.0, 2.0)
    R.camara(FIN(e) + 0.3, -1.0, 50.6, 2.2)
    R.rejilla(tc, "eu", 0.0)
    R.trans_extra = getattr(R, "trans_extra", []) + [(tc, "rollo")]
    # años
    R.anio(i0, 1492)
    R.anio(t_cortes, 1519)
    R.anio(t_mex + 0.5, 1521)
    R.anio(t_piz - 0.1, 1521)
    R.anio(t_incas + 0.5, 1533)
    R.anio(t_plata - 0.1, 1533)
    R.anio(t_potosi + 0.4, 1545)
    R.anio(t_zaca + 0.4, 1546)
    R.anio(t_felipe - 0.2, 1546)
    R.anio(t_felipe + 0.6, 1580)
    R.anio(t_lep - 0.3, 1580)
    R.anio(t_lep + 0.2, 1571)
    R.anio(t_armada - 0.1, 1571)
    R.anio(t_armada + 0.5, 1588)
    # Cortés y los mexicas
    Pco = [(-94.6, 19.1), (-95.6, 19.3), (-96.6, 19.25)]
    andar(R, lambda p: E3.conquistador_caballo(p), Pco, t_cortes - 0.2, (t_mex + 0.2) - t_cortes, t1=t_piz - 0.5, s=0.55, sem=140, z=3, fps=8,
          snd=("galope", 0.45), off=(0, 10))
    for k in range(3):
        andar(R, lambda p, k=k: E3.tlaxcalteca(p), [(x - 0.8 - 0.5 * k, y + 0.5 - 0.6 * k) for x, y in Pco], t_alia + 0.12 * k, (t_mex + 0.4) - t_alia,
              t1=t_piz - 0.5, s=0.45, sem=141 + k, z=2, fps=6, off=formacion(k, 3, 95))
    ga(R, E3.templo_mayor(), CI["tenochtitlan"], t_cortes + 0.2, t_piz - 0.5, s=0.48, off=(0, -10), sem=144, z=1, entra="pluma", d_in=0.8, snd=("crece", 0.4))
    for k in range(2):
        ga(R, E3.guerrero_aguila(k, "enojo"), CI["tenochtitlan"], t_mex - 0.2 + 0.15 * k, t_piz - 0.5, s=0.48, off=(-250 - 120 * k, 80 + 30 * k), sem=145 + k, z=2)
    titulo(R, t_cortes - 0.1, t_mex - 0.2, "HERNÁN CORTÉS", px=74)
    lugar(R, t_alia, t_mex - 0.2, "+ MILES DE ALIADOS INDÍGENAS", (-96.0, 18.0), off=(0, 150), px=44)
    ciudad(R, t_mex - 0.2, t_piz - 0.6, "tenochtitlan", "TENOCHTITLAN 1521", "abajo", 46)
    # Pizarro y los incas
    Ppi = M.RUTAS["pizarro"][3:]
    R.ruta(Ppi, t_piz - 0.5, 2.0, ancho=5.0, t1=t_brut)
    andar(R, lambda p: E3.conquistador_caballo(p, (120, 90, 140)), Ppi, t_piz - 0.4, (t_incas + 1.1) - t_piz, t1=t_brut + 0.3, s=0.5, sem=148, z=3, fps=8,
          snd=("galope", 0.45), flip=False)
    ga(R, E3.inca(0, "serio"), CI["cuzco"], t_incas - 0.25, t_brut + 0.3, s=0.55, off=(130, 30), sem=149, z=2, extra=[(0.1, "gong", 0.4)])
    titulo(R, t_piz - 0.1, t_incas - 0.2, "FRANCISCO PIZARRO", px=74)
    ciudad(R, t_incas - 0.1, t_brut + 0.3, "cuzco", "CUZCO", "abajo", 46)
    # epidemias
    for k, (geo, s) in enumerate((((-99.0, 19.0), 0.55), ((-90.0, 15.0), 0.42), ((-75.0, -10.0), 0.55), ((-70.0, -16.0), 0.42), ((-74.0, 4.0), 0.4))):
        ga(R, lambda t, k=k: E3.epidemia(int(t * 2 + k) % 6), geo, t_epid - 0.4 + 0.15 * k, t_mezcla, s=s, off=mece(10, 0.8, k), sem=150 + k, z=2,
           entra="pluma", d_in=0.7, snd=("viento", 0.3) if k == 0 else None, zs=0.3)
    titulo(R, t_epid - 0.1, t_mezcla - 0.1, "EPIDEMIAS Y GUERRA", px=76)
    R.texto(t_millo - 0.1, t_mezcla - 0.1, "MILLONES DE MUERTOS", (1420, 640), px=62, d=0.6)
    R.snd(t_brut, "tambor", 0.5, tono=0.7)
    pa(R, A.espadas(), 1420, 420, 0.9, t_brut - 0.1, t_mezcla, sem=153, extra=[(0.05, "espada", 0.5)])
    pa(R, A.estallido(14, 50, 150), 1420, 400, 1.0, t_guerra - 0.05, t_guerra + 0.5, entra="fija", sale="cortar", sem=154, snd=("explosion", 0.4))
    # nace la América hispana; el castellano cruza el océano
    titulo(R, t_nace - 0.1, t_plata - 0.2, "NACE LA AMÉRICA HISPANA", px=74)
    R.rio([CI["sevilla"], (-30.0, 30.0), (-60.0, 24.0), CI["veracruz"]], t_cast - 0.2, 1.6, COL["hispano"], ancho=12, t1=t_plata - 0.2)
    lugar(R, t_cruza, t_plata - 0.2, "ESPAÑOL", (-35.0, 25.0), off=(0, 40), px=50)
    for k, (cl, px) in enumerate((("mexico", 48), ("lima", 44), ("bogota", 42), ("caracas", 40), ("habana", 38))):
        lugar(R, t_cast + 0.15 * k, t_plata - 0.2, "¡HOLA!", CI[cl], off=(0, -10), px=px, d=0.3)
        R.snd(t_cast + 0.15 * k, "pop", 0.3, tono=1.0 + 0.1 * k)
    # la plata
    ga(R, E3.cerro_rico(), CI["potosi"], t_potosi - 0.2, t_felipe, s=0.42, off=(0, 30), sem=155, z=1, entra="sube", snd=("crece", 0.4))
    ciudad(R, t_potosi - 0.1, t_felipe, "potosi", "POTOSÍ", "abajo", 44)
    ga(R, E3.lingotes(), CI["zacatecas"], t_zaca - 0.1, t_felipe, s=0.42, off=(0, 0), sem=156, z=1, snd=("monedas", 0.5))
    ciudad(R, t_zaca - 0.1, t_felipe, "zacatecas", "ZACATECAS", "arriba", 44)
    for k, ruta in enumerate(("flota_peru", "flota_mx")):
        andar(R, lambda p: E3.galeon(p), M.RUTAS[ruta], t_plata + 0.3 * k, (t_felipe + 0.2) - t_plata, t1=t_felipe + 0.3, s=0.28, sem=157 + k, zs=0.2, z=2,
              fps=3, snd=("ola", 0.3), ease=lambda u: u)
    pa(R, E3.real_de_a_ocho(), 1250, 560, 1.05, t_primera - 0.3, t_felipe, sem=159, extra=[(0.1, "monedas", 0.5)])
    titulo(R, t_primera - 0.1, t_felipe - 0.1, "LA PRIMERA POTENCIA DEL MUNDO", px=66)
    # Felipe II y el sol que nunca se pone
    pa(R, E3.felipe2(0, "serio"), 300, 1010, 1.2, t_felipe - 0.1, tc, sem=160, extra=[(0.1, "fanfarria", 0.4)])
    R.texto(t_reina, tc - 0.1, "FELIPE II", (300, 580), px=60, d=0.4)
    pa(R, lambda t: E3.sol_cara(int(t * 3) % 6), lambda t: lerp(1620, 700, e_inout(prog(t, t_nunca - 0.3, tc))),
       lambda t: 470 - 90 * math.sin(math.pi * prog(t, t_nunca - 0.3, tc)), 0.8, t_nunca - 0.4, tc, sem=161, extra=[(0.1, "brillo", 0.5)])
    titulo(R, t_sol - 0.1, tc - 0.1, "«DONDE NUNCA SE PONE EL SOL»", px=66)
    andar(R, lambda p: E3.galeon(p), M.RUTAS["galeon_manila"][:-1], t_felipe + 0.2, tc - t_felipe, t1=tc, s=0.26, sem=162, zs=0.2, z=2, fps=3, snd=None,
          ease=lambda u: u)
    ciudad(R, t_filip - 0.1, tc, "manila", "FILIPINAS (FELIPE)", "der", 40)
    # Lepanto y la Armada Invencible (rejilla "eu")
    for k in range(3):
        ga(R, lambda t, k=k: E3.galera(int(t * 4) + k, (196, 70, 50), (240, 220, 120)), (19.6 + 0.4 * k, 38.2 - 0.25 * k), tc + 0.1 + 0.1 * k, t_armada - 0.2,
           s=0.42, off=mece(5, 2.2, k), sem=163 + k, z=2, zs=0.4, snd=("ola", 0.3) if k == 0 else None)
        ga(R, lambda t, k=k: E3.galera(int(t * 4) + k + 2, (70, 130, 90), (236, 230, 210)), (21.4 + 0.4 * k, 38.6 - 0.25 * k), tc + 0.2 + 0.1 * k, t_armada - 0.2,
           s=0.42, off=mece(5, 2.4, k + 1), sem=166 + k, z=2, zs=0.4, flip=True, snd=None)
    pa(R, A.estallido(16, 50, 160), 1120, 640, 1.0, t_lep - 0.05, t_lep + 0.6, entra="fija", sale="cortar", sem=169, snd=("canonazo", 0.6))
    titulo(R, t_lep - 0.1, t_armada - 0.2, "LEPANTO, 1571", px=80)
    Par = M.RUTAS["armada"]
    for k in range(3):
        andar(R, lambda p, k=k: E3.galeon(p + k), [(x - 0.6 * k, y - 0.35 * k) for x, y in Par], t_armada - 0.6 + 0.2 * k, 3.4, t1=FIN(e) + 0.5, s=0.42,
              sem=170 + k, z=2, zs=0.3, fps=3, snd=("ola", 0.3) if k == 0 else None, ease=lambda u: u, off=formacion(k, 3, 170))
    ga(R, Bb.tormenta(), (0.0, 51.5), t_frac - 0.3, FIN(e) + 0.5, s=0.6, off=mece(6, 1.2), sem=173, z=3, zs=0.3, snd=("trueno", 0.6))
    R.act(E3.galeon(0, 1.0, (120, 90, 70)), pos=lambda t: (430, 860 + 120 * e_in(prog(t, t_frac + 0.3, FIN(e) + 0.4)), 0.7,
                                                           0.5 * e_inout(prog(t, t_frac, FIN(e) + 0.3))),
          t_in=t_frac - 0.1, d_in=0.4, entra="pop", sem=174, sfx=[(0.3, "chapuzon", 0.5)], t_out=FIN(e) + 0.6, sale="encoger", z=3)
    titulo(R, t_armada - 0.1, FIN(e) + 0.3, "LA ARMADA INVENCIBLE, 1588", px=72)
    R.snd(t_ingl, "trueno", 0.5)


# ------------------------------------------------------------------ SIGLO DE ORO
def _siglo_oro(R):
    e = "siglo_oro"
    i0 = INI(e)
    t_siglo, t_cerv, t_quij, t_vel, t_men = T(e, "siglo"), T(e, "cervantes"), T(e, "quijote"), T(e, "velazquez"), T(e, "meninas")
    t_tanta, t_cara, t_quie, t_otra = T(e, "tanta"), T(e, "cara"), T(e, "quiebra"), T(e, "otra")
    t_1700, t_ultimo, t_austr, t_muere, t_hijos, t_estalla, t_trono = (T(e, "mil", frase=2), T(e, "ultimo"), T(e, "austrias"), T(e, "muere"), T(e, "hijos"),
                                                                       T(e, "estalla"), T(e, "trono"))
    t_gana, t_borbon, t_frances, t_pierde, t_tierras, t_gib, t_brit = (T(e, "gana"), T(e, "borbon"), T(e, "frances"), T(e, "pierde"), T(e, "tierras"),
                                                                       T(e, "gibraltar"), T(e, "britanicas"))
    # territorio
    R.terreno(i0 - 0.5, "austrias", COL["austrias"], 0.6)
    R.terreno(t_frances - 0.2, "francia", COL["borbon"], 1.0, capa=10)
    R.terreno(t_tierras - 0.2, "espana_1512", COL["espana"], 1.6)
    R.sello(t_borbon + 0.1, "lis", "BORBONES", color=(50, 80, 160))
    # cámara
    R.camara(i0 - 0.3, -3.7, 40.4, 2.8)
    R.camara(t_vel, -3.7, 40.4, 3.0)
    R.camara(t_tanta, -3.0, 40.2, 2.6)
    R.camara(t_1700, -3.5, 40.3, 2.6)
    R.camara(t_estalla + 0.4, -2.6, 41.0, 2.3)
    R.camara(t_gana + 0.3, 0.0, 45.0, 1.3)
    R.camara(t_tierras + 0.3, 3.0, 45.0, 1.15)
    R.camara(t_gib - 0.4, -5.35, 36.3, 5.0)
    R.camara(FIN(e) + 0.3, -5.35, 36.25, 5.6)
    # años
    R.anio(i0, 1588)
    R.anio(t_cerv + 0.4, 1605)
    R.anio(t_vel - 0.1, 1605)
    R.anio(t_men + 0.4, 1656)
    R.anio(t_tanta, 1656)
    R.anio(t_otra + 0.3, 1680)
    R.anio(t_1700 - 0.2, 1680)
    R.anio(t_1700 + 0.6, 1700)
    R.anio(t_estalla, 1701)
    R.anio(t_gana + 0.2, 1701)
    R.anio(t_brit + 0.3, 1713)
    # Siglo de Oro: Cervantes y el Quijote contra el molino; Velázquez y Las Meninas
    titulo(R, t_siglo - 0.1, t_tanta - 0.2, "EL SIGLO DE ORO", px=92)
    pa(R, E3.cervantes(0, "feliz"), 330, 1010, 1.2, t_cerv - 0.15, t_vel - 0.1, sem=180)
    R.act(lambda t: E3.quijote(int(t * 8) % 4), pos=lambda t: (lerp(700, 1180, e_in(prog(t, t_quij, t_vel))), 980, 0.95), t_in=t_quij - 0.3, d_in=0.4,
          entra="pop", sem=181, sfx=[(0, "galope", 0.5)], t_out=t_vel - 0.1, sale="encoger", z=3)
    pa(R, lambda t: E3.molino(round(t * 2.2, 2)), 1560, 1000, 1.25, t_quij - 0.4, t_vel - 0.1, sem=182, z=2, extra=[(0.1, "viento", 0.4)])
    R.texto(t_quij, t_vel - 0.2, "DON QUIJOTE (1605)", (960, 330), px=58, d=0.5)
    pa(R, E3.velazquez(0, "serio"), 420, 1010, 1.2, t_vel - 0.15, t_tanta - 0.1, sem=183)
    pa(R, E3.meninas(), 1300, 1000, 1.25, t_men - 0.3, t_tanta - 0.1, sem=184, entra="pluma", d_in=0.7, snd=("pincel", 0.5))
    R.texto(t_men, t_tanta - 0.2, "LAS MENINAS (1656)", (1300, 470), px=54, d=0.5)
    # bancarrotas
    pa(R, E3.bancarrota(), 960, 1000, 1.3, t_tanta - 0.1, t_1700 - 0.1, sem=185, extra=[(0.2, "monedas", 0.4)])
    for k, (anio, x, y) in enumerate((("1557", 380, 420), ("1575", 760, 330), ("1596", 1160, 330), ("1607", 1540, 420), ("1627", 420, 640),
                                      ("1647", 1500, 640))):
        t0 = t_cara + 0.25 * k
        R.texto(t0, t_1700 - 0.2, anio, (x, y), px=60, d=0.2)
        R.snd(t0, "golpe_suave", 0.35)
    titulo(R, t_quie - 0.1, t_1700 - 0.2, "¡BANCARROTA!", px=90, y=190)
    # Carlos II, la cuna vacía y la guerra por el trono
    pa(R, E3.carlos2(0, "lloron"), 520, 1010, 1.25, t_ultimo - 0.15, t_muere + 0.3, sem=186, sale="caer", d_out=0.6)
    pa(R, E3.cuna_vacia(), 1350, 1000, 1.1, t_hijos - 0.3, t_estalla - 0.1, sem=187)
    R.texto(t_austr, t_muere + 0.2, "CARLOS II", (520, 560), px=60, d=0.4)
    pa(R, lambda t: E3.felipe5(int(t * 4) % 2, "enojo"), 470, 1010, 1.2, t_estalla - 0.1, t_gana + 0.2, sem=188)
    pa(R, lambda t: E3.archiduque(int(t * 4 + 1) % 2, "enojo"), 1450, 1010, 1.2, t_estalla, t_gana + 0.2, sem=189, flip=True, sale="der_fuera", d_out=0.6)
    pa(R, E1.corona_votiva(), lambda t: 960 + 300 * math.sin((t - t_estalla) * 4.5), lambda t: 560 - 90 * abs(math.sin((t - t_estalla) * 4.5)), 0.7,
       t_estalla, t_gana + 0.2, sem=190, extra=[(0, "boing", 0.4)])
    titulo(R, t_estalla - 0.1, t_gana - 0.2, "GUERRA DE SUCESIÓN", px=80)
    R.snd(t_estalla, "canonazo", 0.5)
    R.snd(t_trono, "espada", 0.5)
    # gana el Borbón; se pierden Flandes e Italia; Gibraltar británico
    andar(R, lambda p: E3.felipe5(p, "feliz"), M.RUTAS["borbon"], t_gana - 0.1, (t_pierde + 0.4) - t_gana, t1=t_gib - 0.3, s=0.85, sem=191, z=3, fps=6)
    titulo(R, t_borbon - 0.1, t_gib - 0.4, "FELIPE V, EL PRIMER BORBÓN", px=70)
    for k, (geo, txt) in enumerate((((4.6, 50.8), "FLANDES"), ((9.2, 45.4), "MILÁN"), ((15.0, 40.8), "NÁPOLES"), ((14.0, 37.5), "SICILIA"))):
        lugar(R, t_tierras + 0.15 * k, t_gib - 0.6, txt, geo, off=(0, 50), px=40)
    R.snd(t_tierras, "borrar", 0.5)
    ga(R, lambda t: E3.penon(True, int(t * 3) % 6), CI["gibraltar"], t_gib - 0.2, FIN(e) + 0.5, s=0.6, off=(60, 190), sem=192, z=2, entra="sube",
       snd=("crece", 0.4))
    titulo(R, t_gib - 0.1, FIN(e) + 0.3, "GIBRALTAR, BRITÁNICO DESDE 1713", px=66)
