# -*- coding: utf-8 -*-
"""Coreografía (3/4): la industria (ferrocarril transcontinental de 1869, Carnegie, Rockefeller y Edison, la Estatua de la Libertad y
los inmigrantes de Nueva York, la guerra con España de 1898, los hermanos Wright), las guerras (Ford y el Modelo T, la Primera Guerra
Mundial, los locos años veinte, el crac del 29 y la Gran Depresión, el New Deal, Pearl Harbor, Normandía, Hiroshima y Nagasaki) y la
Guerra Fría (dos superpotencias, Corea y Vietnam, los misiles de Cuba, el Plan Marshall, Hollywood y el rock and roll, la Luna).
Capas: 0 = EE. UU., 1 = Cuba / el mundo de fuera."""
import math

import mapa as M
import obj_a as A
import obj_us1 as P1
import obj_us2 as P2
import obj_us3 as P3
from core import FIN, INI, T, kf
from coreo_util import CI, COL, andar, ciudad, foco, ga, grupo, lugar, pa, para, titulo
from motor import e_inout, lerp, prog


def cortes(R):
    pass


def construir(R):
    _industria(R)
    _guerras(R)
    _guerra_fria(R)


# ------------------------------------------------------------------ INDUSTRIA
def _industria(R):
    e = "industria"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_fer, t_une, t_atl, t_pac = W(0, "ferrocarril"), W(0, "une"), W(0, "atlantico"), W(0, "pacifico")
    t_ace, t_car, t_pet, t_roc, t_bom, t_edi, t_fab = (W(1, "acero"), W(1, "carnegie"), W(1, "petroleo"), W(1, "rockefeller"), W(1, "bombilla"),
                                                       W(1, "edison"), W(1, "fabrica"))
    t_bajo, t_est, t_doce, t_inm, t_pue, t_vida = W(2, "bajo"), W(2, "estatua"), W(2, "doce"), W(2, "inmigrantes"), W(2, "puerto"), W(2, "vida")
    t_mil3, t_ven, t_pr, t_guam, t_fil = W(3, "mil"), W(3, "vence"), W(3, "puerto"), W(3, "guam"), W(3, "filipinas")
    t_mil4, t_her, t_wri, t_vue, t_dun = W(4, "mil"), W(4, "hermanos"), W(4, "wright"), W(4, "vuelo"), W(4, "dunas")

    # cámara: el oeste del ferrocarril -> el país -> el este industrial -> Nueva York -> el Caribe -> Kitty Hawk
    para(R, i0 - 0.7, t_une + 0.2, -110.0, 40.8, 1.55)
    para(R, t_atl + 0.2, t_pac + 0.6, -96.0, 39.5, 0.80)
    foco(R, t_car - 0.2, t_bajo - 0.5, (-80.6, 41.2), 2.6)
    foco(R, t_bajo + 0.3, t_mil3 - 0.6, CI["ellis_island"], 6.4)
    para(R, t_mil3 + 0.3, t_mil4 - 0.4, -81.0, 26.4, 2.0)
    foco(R, t_mil4 + 0.4, FIN(e) + 0.6, CI["kitty_hawk"], 6.0)

    R.anio(i0 + 0.1, 1869)
    R.anio(t_ace, 1879)
    R.anio(t_bajo, 1892)
    R.anio(t_mil3 + 0.2, 1898)
    R.anio(t_mil4 + 0.2, 1903)

    # frase 0: el primer ferrocarril transcontinental (Promontory, 1869)
    R.terreno(i0 - 0.3, "eeuu_mod", COL["eeuu"], 0.8)
    R.ruta(M.RUTAS["union_pacific"], i0 - 0.1, 2.4, ancho=6.0, t1=t_ace - 0.2)
    R.ruta(M.RUTAS["central_pacific"], i0, 2.4, ancho=6.0, t1=t_ace - 0.2)
    andar(R, lambda p: P3.locomotora_us(p), M.RUTAS["union_pacific"], i0, 3.2, t1=t_ace - 0.2, s=0.34, sem=400, zs=0.4, z=2, fps=6)
    andar(R, lambda p: P3.locomotora_us(p), M.RUTAS["central_pacific"], i0 + 0.1, 3.2, t1=t_ace - 0.2, s=0.34, sem=401, zs=0.4, z=2, fps=6)
    R.snd(i0, "pasos", 0.3, dur=2.0)
    ciudad(R, t_fer - 0.2, t_ace - 0.2, "promontory", "PROMONTORY", "arriba", 42)
    pa(R, P1.obrero_ferrocarril(0, "feliz"), 300, 1010, 1.04, t_fer - 0.15, t_ace - 0.1, sem=402, extra=[(0.05, "clink", 0.4)])
    pa(R, P3.clavo_oro(), 960, 1000, 0.8, t_une - 0.2, t_atl + 0.4, sem=403, entra="cae", dy=320, extra=[(0.05, "clink", 0.55)])
    titulo(R, t_fer - 0.1, t_ace - 0.2, "FERROCARRIL TRANSCONTINENTAL", px=72)
    R.ruta(M.RUTAS["ferro_este"], t_atl - 0.3, 1.4, ancho=6.0, t1=t_ace - 0.2)
    andar(R, lambda p: P3.locomotora_us(p), M.RUTAS["ferro_este"][::-1], t_atl - 0.3, 2.0, t1=t_ace - 0.2, s=0.30, sem=404, zs=0.4, z=2, fps=6)
    R.sello(t_une, "locomotora", "LA INDUSTRIA", color=(196, 132, 60))
    pa(R, P3.vagon_tren(1), 1620, 1000, 0.7, t_une, t_ace - 0.1, sem=405)

    # frase 1: acero, petróleo, bombilla: una fábrica gigante
    ciudad(R, t_ace - 0.1, t_bajo - 0.2, "pittsburgh", "PITTSBURGH", "abajo", 40)
    ga(R, P3.aceria(), CI["pittsburgh"], t_ace - 0.1, t_bajo - 0.2, s=0.50, off=(0, -20), sem=410, zs=0.45, z=2, entra="sube", dy=260,
       extra=[(0.05, "fuego", 0.4, {"dur": 1.4})])
    pa(R, P1.carnegie(0, "feliz"), 300, 1010, 1.04, t_car - 0.15, t_bajo, sem=411)
    R.texto(t_car, t_pet, "ACERO", (300, 590), px=44, d=0.3)
    ciudad(R, t_pet - 0.1, t_bajo - 0.2, "cleveland", "CLEVELAND", "abajo", 38)
    ga(R, P3.torre_petroleo_us(), CI["cleveland"], t_pet - 0.1, t_bajo - 0.2, s=0.44, off=(-60, -10), sem=412, zs=0.45, z=2, entra="sube",
       dy=260, extra=[(0.05, "chorro", 0.4)])
    pa(R, P1.rockefeller(0, "serio"), 570, 1010, 1.0, t_roc - 0.2, t_bajo, sem=413, flip=True)
    pa(R, P3.barril_petroleo(), 800, 1000, 0.6, t_roc, t_bajo, sem=414)
    R.texto(t_pet + 0.1, t_bom, "PETRÓLEO", (570, 590), px=44, d=0.3)
    pa(R, lambda t: P3.bombilla(round(0.5 + 0.5 * abs(math.sin((t - t_bom) * 3.0)), 1)), 1360, 900, 0.85, t_bom - 0.2, t_bajo, sem=415,
       extra=[(0.05, "ding", 0.5)])
    pa(R, P1.edison(0, "feliz"), 1620, 1010, 1.04, t_edi - 0.2, t_bajo, sem=416, flip=True)
    R.texto(t_edi, t_bajo - 0.1, "LA BOMBILLA", (1490, 500), px=44, d=0.3)
    titulo(R, t_fab - 0.2, t_bajo - 0.2, "UNA FÁBRICA GIGANTE", px=82)

    # frase 2: la Estatua de la Libertad y 12 millones de inmigrantes
    ciudad(R, t_est, t_mil3 - 0.2, "ellis_island", "ELLIS ISLAND", "izq", 40)
    ga(R, P3.estatua_libertad(), CI["ellis_island"], t_bajo - 0.1, t_mil3 - 0.2, s=0.42, off=(80, -20), sem=420, zs=0.5, z=2, entra="pluma",
       d_in=1.0, extra=[(0.05, "fanfarria", 0.4)])
    andar(R, lambda p: P3.vapor_inmigrantes(p), M.RUTAS["inmigrantes"], t_est - 0.2, 3.2, t1=t_mil3 - 0.2, s=0.40, sem=421, zs=0.4, z=3,
          fps=4)
    R.snd(t_inm, "ola", 0.35, dur=1.2)
    pa(R, P1.inmigrante(0, "feliz"), 300, 1010, 1.04, t_inm - 0.15, t_mil3, sem=422)
    pa(R, P1.inmigrante_mujer(0, "feliz"), 560, 1010, 1.0, t_inm + 0.1, t_mil3, sem=423, flip=True)
    pa(R, P3.maleta(), 1620, 1000, 0.7, t_pue - 0.1, t_mil3, sem=424)
    R.contador(t_doce - 0.2, t_inm + 0.6, 0, 12, (960, 196), px=82, formato="{} MILLONES DE INMIGRANTES", hasta_t=t_vida - 0.1)
    R.snd(t_doce - 0.2, "reloj_rapido", 0.35, dur=0.9)
    titulo(R, t_vida - 0.6, t_mil3 - 0.2, "UNA VIDA NUEVA", px=80)

    # frase 3: 1898, la guerra con España: Puerto Rico, Guam y Filipinas
    R.terreno(t_mil3 - 0.2, "cuba", COL["espana"], 0.6, capa=1)
    andar(R, lambda p: P3.acorazado_maine(p), M.RUTAS["flota_1898"], t_mil3 - 0.1, 3.0, t1=t_mil4 - 0.2, s=0.40, sem=430, zs=0.4, z=3, fps=4)
    ga(R, A.estallido(), CI["la_habana"], t_ven - 0.1, t_pr, s=0.40, off=(0, -60), sem=431, zs=0.35, z=4, extra=[(0.0, "canonazo", 0.5)])
    R.terreno(t_ven + 0.2, "cuba", (150, 170, 200), 1.0, capa=1)
    pa(R, P1.rough_rider(0, "feliz"), 300, 1010, 1.04, t_mil3 - 0.15, t_mil4, sem=432)
    pa(R, P2.bandera_borgona(), 560, 1010, 0.86, t_ven - 0.1, t_pr, sem=433, flip=True)
    titulo(R, t_ven - 0.2, t_mil4 - 0.2, "GUERRA CON ESPAÑA (1898)", px=78)
    for k, (tt, txt) in enumerate(((t_pr, "PUERTO RICO"), (t_guam, "GUAM"), (t_fil, "FILIPINAS"))):
        R.texto(tt - 0.15, t_mil4 - 0.2, txt, (1560, 470 + 90 * k), px=50, d=0.35)
        R.snd(tt - 0.1, "pluck", 0.35)
    pa(R, P3.bandera_eeuu(), 1600, 1010, 0.6, t_pr, t_mil4, sem=434)

    # frase 4: 1903, los hermanos Wright en Kitty Hawk
    R.terreno(t_mil4, None, COL["espana"], 0.6, capa=1)
    ciudad(R, t_mil4, FIN(e) + 0.3, "kitty_hawk", "KITTY HAWK", "abajo", 46)
    andar(R, lambda p: P3.avion_wright(p), [(-75.84, 35.98), (-75.60, 36.08)], t_her, 3.4, t1=FIN(e) + 0.3, s=0.46, sem=440, zs=0.4, z=3,
          fps=8, extra=[(0.05, "zoom_whoosh", 0.4)])
    pa(R, P1.hermano_wright(0, "feliz"), 300, 1010, 1.04, t_mil4, FIN(e) + 0.3, sem=441)
    pa(R, P1.hermano_wright(1, "asombro"), 560, 1010, 1.0, t_wri - 0.1, FIN(e) + 0.3, sem=442, flip=True)
    titulo(R, t_vue - 0.3, FIN(e) + 0.2, "EL PRIMER VUELO CON MOTOR", px=76)
    R.contador(t_dun - 0.4, t_dun + 0.6, 0, 12, (1560, 520), px=60, formato="{} SEGUNDOS", hasta_t=FIN(e) + 0.2)
    lugar(R, t_dun, FIN(e) + 0.2, "CAROLINA DEL NORTE", (-76.6, 36.6), off=(0, 0), px=40)


# ------------------------------------------------------------------ GUERRAS: Ford, Primera Guerra Mundial, años veinte, crac, New Deal, Segunda Guerra Mundial
def _guerras(R):
    e = "guerras"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_hen, t_aut, t_tod, t_mil0, t_pri = W(0, "henry"), W(0, "automovil"), W(0, "todos"), W(0, "mil"), W(0, "primera")
    t_loc, t_jaz, t_vot, t_bol, t_des, t_mil1 = W(1, "locos"), W(1, "jazz"), W(1, "voto"), W(1, "bolsa"), W(1, "desploma"), W(1, "mil")
    t_gran, t_uno, t_pie, t_fra, t_new = W(2, "gran"), W(2, "uno"), W(2, "pierde"), W(2, "franklin"), W(2, "new")
    t_mil3, t_jap, t_pea, t_ent, t_seg = W(3, "mil"), W(3, "japon"), W(3, "pearl"), W(3, "entra"), W(3, "segunda")
    t_tro, t_nor, t_ter, t_bom, t_hir = W(4, "tropas"), W(4, "normandia"), W(4, "termina"), W(4, "bombas"), W(4, "hiroshima")

    # cámara: Detroit -> el Atlántico (1917) -> Nueva York (jazz, Wall Street) -> el país en crisis -> costa del Pacífico -> el Atlántico
    foco(R, i0 - 0.6, t_tod, CI["detroit"], 5.0)
    para(R, t_mil0 + 0.6, t_loc - 0.4, -73.0, 40.5, 2.1)
    foco(R, t_loc + 0.3, t_gran - 0.4, CI["nueva_york"], 5.4)
    para(R, t_gran + 0.3, t_mil3 - 0.4, -95.0, 38.5, 0.95)
    para(R, t_jap - 0.4, t_tro - 0.6, -118.0, 36.0, 1.7)
    para(R, t_tro + 0.2, t_bom - 0.4, -72.0, 40.0, 1.8)
    para(R, t_bom + 0.2, FIN(e) + 0.6, -86.0, 38.5, 1.0)

    R.anio(i0 + 0.1, 1908)
    R.anio(t_mil0 + 0.2, 1917)
    R.anio(t_loc, 1920)
    R.anio(t_mil1 + 0.2, 1929)
    R.anio(t_gran, 1933)
    R.anio(t_mil3 + 0.2, 1941)
    R.anio(t_tro, 1944)
    R.anio(t_bom, 1945)

    # frase 0: Henry Ford y el Modelo T; 1917, la Primera Guerra Mundial
    R.terreno(i0 - 0.3, None, COL["espana"], 0.4, capa=1)
    ciudad(R, i0, t_mil0, "detroit", "DETROIT", "abajo", 46)
    pa(R, P1.henry_ford(0, "feliz"), 300, 1010, 1.04, t_hen - 0.15, t_mil0 + 0.1, sem=500)
    for k, P in enumerate(([(-83.6, 42.2), (-82.7, 42.45)], [(-82.6, 42.15), (-83.5, 42.42)])):
        andar(R, lambda p: P3.modelo_t(p), P, t_hen + 0.3 * k, 2.6, t1=t_mil0, s=0.34, sem=501 + k, zs=0.4, z=2, fps=8)
    R.snd(t_aut, "zoom_whoosh", 0.35, dur=0.8)
    pa(R, P3.cadena_montaje(), 1250, 1000, 0.8, t_aut - 0.2, t_mil0 + 0.1, sem=503, entra="sube", dy=320, extra=[(0.05, "clink", 0.4)])
    pa(R, P3.modelo_t(1), 1620, 1000, 0.86, t_tod - 0.3, t_mil0 + 0.1, sem=504, flip=True)
    titulo(R, t_aut - 0.1, t_mil0 - 0.1, "EL MODELO T", px=82)
    R.ruta(M.RUTAS["tropas_europa"], t_mil0, 1.8, ancho=5.0, t1=t_loc - 0.2, flecha=True)
    andar(R, lambda p: P3.vapor_inmigrantes(p), M.RUTAS["tropas_europa"], t_mil0 + 0.2, 2.6, t1=t_loc - 0.2, s=0.36, sem=505, zs=0.4, z=3,
          fps=4)
    pa(R, P1.doughboy(0, "serio"), 300, 1010, 1.04, t_mil0 + 0.1, t_loc, sem=506, extra=[(0.05, "tambor", 0.35)])
    pa(R, P1.doughboy(1, "enojo"), 560, 1010, 0.98, t_pri - 0.2, t_loc, sem=507, flip=True)
    titulo(R, t_pri - 0.2, t_loc - 0.2, "PRIMERA GUERRA MUNDIAL", px=78)
    lugar(R, t_pri, t_loc - 0.2, "A EUROPA", (-66.0, 38.8), off=(0, 0), px=40)
    R.sello(t_pri, "avion", "GUERRAS MUNDIALES", color=(122, 126, 78))

    # frase 1: los locos años veinte, el jazz, el voto femenino; el crac de 1929
    ciudad(R, t_loc, t_bol - 0.2, "nueva_york", "NUEVA YORK", "abajo", 42)
    pa(R, P1.musico_jazz(0, "feliz"), 300, 1010, 1.02, t_loc - 0.1, t_bol, sem=510, extra=[(0.05, "fanfarria", 0.35)])
    pa(R, P1.flapper(0, "feliz"), 560, 1010, 1.0, t_jaz - 0.1, t_bol, sem=511, flip=True)
    R.texto(t_jaz, t_bol - 0.1, "JAZZ", (430, 600), px=50, d=0.3)
    pa(R, P1.sufragista(0, "feliz"), 1620, 1010, 1.02, t_vot - 0.2, t_bol, sem=512, flip=True)
    pa(R, P3.urna_voto(), 1360, 1000, 0.72, t_vot - 0.1, t_bol, sem=513, extra=[(0.05, "pop", 0.4)])
    R.texto(t_vot + 0.1, t_bol - 0.1, "VOTO FEMENINO", (1490, 500), px=40, d=0.4)
    titulo(R, t_loc - 0.1, t_bol - 0.2, "LOS LOCOS AÑOS VEINTE", px=78)
    pa(R, P3.grafico_crash(), 960, 1000, 1.05, t_bol - 0.1, t_gran, sem=514, entra="sube", dy=340, extra=[(0.15, "apagon", 0.5)])
    pa(R, P1.corredor_bolsa(0, "miedo"), 300, 1010, 1.02, t_des - 0.1, t_gran, sem=515)
    pa(R, P1.corredor_bolsa(1, "lloron"), 1620, 1010, 1.0, t_des + 0.1, t_gran, sem=516, flip=True)
    titulo(R, t_des - 0.1, t_gran - 0.2, "EL CRAC DEL 29", px=84)
    ga(R, P3.skyline_nyc(), CI["nueva_york"], t_loc, t_gran - 0.2, s=0.40, off=(-160, -10), sem=517, zs=0.4, z=1, entra="sube", dy=260)

    # frase 2: Gran Depresión (1 de cada 4 sin empleo) y el New Deal de Franklin Roosevelt
    pa(R, P1.desempleado(0, "lloron"), 300, 1010, 1.02, t_gran - 0.1, t_mil3, sem=520)
    pa(R, P3.fila_pan(), 760, 1010, 0.9, t_uno - 0.2, t_fra, sem=521, entra="sube", dy=300, extra=[(0.05, "pasos", 0.35, {"dur": 1.0})])
    titulo(R, t_gran - 0.1, t_fra - 0.2, "LA GRAN DEPRESIÓN", px=82)
    R.texto(t_uno, t_fra - 0.1, "1 DE CADA 4 SIN EMPLEO", (960, 320), px=60, d=0.5)
    R.romper("estados", t_gran, t_pie, t_new - 0.3, t_new + 0.4, gap=8.0, deriva=14.0, fijas=(0,), colores=lambda t, i: (150, 156, 176))
    R.snd(t_gran, "crujido", 0.4, dur=0.8)
    pa(R, P1.fdr(0, "feliz"), 1620, 1010, 1.06, t_fra - 0.15, t_mil3, sem=522, flip=True, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_fra + 0.1, t_mil3 - 0.1, "FRANKLIN ROOSEVELT", (1580, 580), px=38, d=0.4)
    pa(R, P3.aguila_new_deal(), 960, 1000, 0.9, t_new - 0.3, t_mil3, sem=523, entra="sube", dy=320)
    titulo(R, t_new - 0.2, t_mil3 - 0.2, "EL NEW DEAL", px=84)

    # frase 3: 1941, Pearl Harbor: EE. UU. entra en la Segunda Guerra Mundial
    R.ruta(M.RUTAS["pacifico_oeste"], t_jap - 0.2, 1.4, ancho=5.0, t1=t_tro - 0.2, flecha=True)
    lugar(R, t_pea - 0.2, t_tro - 0.2, "HACIA HAWÁI", (-123.4, 34.2), off=(0, 0), px=40)
    for k in range(3):
        pa(R, lambda t, k=k: P3.avion_caza(int(t * 8 + k) % 4), lambda t, k=k: lerp(-220, 2140, prog(t, t_jap - 0.1 + 0.2 * k, t_ent + 0.4)),
           lambda t, k=k: 300 + 70 * k, 0.5, t_jap - 0.1 + 0.2 * k, t_ent + 0.4, sem=530 + k, z=4, entra="fija", flip=True)
    R.snd(t_jap, "zoom_whoosh", 0.45, dur=1.0)
    pa(R, lambda t: P3.acorazado_arizona(int(t * 4) % 4), 960, 1000, 1.0, t_pea - 0.3, t_tro, sem=533, entra="sube", dy=300,
       extra=[(0.05, "canonazo", 0.55), (0.3, "fuego", 0.4, {"dur": 1.6})])
    titulo(R, t_pea - 0.2, t_ent - 0.2, "PEARL HARBOR (1941)", px=82)
    pa(R, P1.marinero(0, "miedo"), 300, 1010, 1.0, t_pea - 0.1, t_tro, sem=534)
    pa(R, P1.soldado_ww2(0, "enojo"), 1620, 1010, 1.04, t_ent - 0.2, t_tro, sem=535, flip=True)
    titulo(R, t_seg - 0.3, t_tro - 0.2, "SEGUNDA GUERRA MUNDIAL", px=78)

    # frase 4: Normandía; Hiroshima y Nagasaki
    R.ruta(M.RUTAS["tropas_europa"], t_tro - 0.2, 1.4, ancho=5.0, t1=t_bom - 0.2, flecha=True)
    for k in range(2):
        andar(R, lambda p: P3.lancha_desembarco(p), M.RUTAS["tropas_europa"], t_tro - 0.1 + 0.4 * k, 2.4, t1=t_bom - 0.2, s=0.34, sem=540 + k,
              zs=0.4, z=3, fps=4, off=(0, 50 * k))
    pa(R, P1.soldado_ww2(1, "enojo"), 300, 1010, 1.04, t_tro - 0.1, t_bom, sem=542)
    pa(R, P1.soldado_ww2(0, "serio"), 560, 1010, 0.98, t_tro + 0.2, t_bom, sem=543, flip=True)
    titulo(R, t_nor - 0.2, t_ter - 0.1, "NORMANDÍA (1944)", px=82)
    lugar(R, t_nor, t_bom - 0.2, "A NORMANDÍA", (-66.0, 38.8), off=(0, 0), px=40)
    pa(R, P3.hongo_atomico(), 960, 1010, 1.15, t_bom - 0.2, FIN(e) + 0.3, sem=544, entra="sube", dy=420, extra=[(0.05, "apagon", 0.6)])
    titulo(R, t_hir - 0.3, FIN(e) + 0.2, "HIROSHIMA Y NAGASAKI (1945)", px=74)


# ------------------------------------------------------------------ GUERRA FRÍA
def _guerra_fria(R):
    e = "guerra_fria"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_sal, t_sup, t_est, t_uni, t_enf, t_gue = W(0, "salen"), W(0, "superpotencias"), W(0, "estados"), W(0, "union"), W(0, "enfrentadas"), W(0, "guerra")
    t_com, t_cor, t_vie, t_mil1, t_mis, t_cub, t_bor = (W(1, "combaten"), W(1, "corea"), W(1, "vietnam"), W(1, "mil"), W(1, "misiles"),
                                                        W(1, "cuba"), W(1, "borde"))
    t_pla, t_eur, t_cul, t_hol, t_roc, t_con = W(2, "plan"), W(2, "europa"), W(2, "cultura"), W(2, "hollywood"), W(2, "rock"), W(2, "conquista")
    t_car, t_mil3, t_cua, t_nei, t_pis, t_luna = W(3, "carrera"), W(3, "mil"), W(3, "cuando"), W(3, "neil"), W(3, "pisa"), W(3, "luna")

    # cámara: el país -> Florida y Cuba -> la costa atlántica -> Los Ángeles -> Cabo Cañaveral
    para(R, i0 - 0.7, t_mil1 + 0.3, -95.0, 38.0, 0.80)
    para(R, t_mis - 0.4, t_pla - 0.5, -81.5, 26.0, 2.2)
    para(R, t_pla + 0.1, t_eur + 0.6, -72.0, 40.0, 2.0)
    foco(R, t_hol - 0.6, t_car - 0.6, CI["los_angeles"], 5.0)
    foco(R, t_car + 0.4, FIN(e) + 0.6, CI["cabo_canaveral"], 4.6)

    R.anio(i0 + 0.1, 1947)
    R.anio(t_cor, 1950)
    R.anio(t_vie, 1965)
    R.anio(t_mil1 + 0.2, 1962)
    R.anio(t_pla, 1948)
    R.anio(t_car, 1957)
    R.anio(t_mil3 + 0.2, 1969)

    # frase 0: dos superpotencias, la Guerra Fría
    pa(R, P3.bandera_eeuu(), 330, 1010, 1.05, t_sup - 0.2, t_com, sem=600, entra="sube", dy=320)
    R.texto(t_est, t_com - 0.1, "ESTADOS UNIDOS", (330, 530), px=44, d=0.35)
    pa(R, P3.bandera_urss(), 1590, 1010, 1.05, t_uni - 0.2, t_com, sem=601, entra="sube", dy=320, flip=True)
    R.texto(t_uni, t_com - 0.1, "UNIÓN SOVIÉTICA", (1590, 530), px=44, d=0.35)
    pa(R, P3.misil_nuclear(), 960, 1000, 0.9, t_enf - 0.2, t_com, sem=602, entra="sube", dy=320, extra=[(0.05, "siseo", 0.4)])
    titulo(R, t_gue - 0.3, t_com - 0.1, "LA GUERRA FRÍA", px=88)
    R.sello(t_com - 0.1, "cohete", "GUERRA FRÍA", color=(176, 64, 58))

    # frase 1: Corea y Vietnam; 1962, los misiles de Cuba
    pa(R, P1.soldado_ww2(0, "serio"), 300, 1010, 1.02, t_com - 0.1, t_mis - 0.3, sem=605)
    R.texto(t_cor - 0.1, t_mis - 0.4, "COREA (1950-53)", (420, 300), px=50, d=0.4)
    pa(R, lambda t: P3.helicoptero_huey(int(t * 10) % 4), lambda t: lerp(2140, 1300, e_inout(prog(t, t_vie - 0.3, t_vie + 1.0))),
       lambda t: 420 + 14 * math.sin(t * 3.0), 0.7, t_vie - 0.3, t_mis - 0.3, sem=606, z=3, entra="fija", flip=True,
       extra=[(0.05, "viento", 0.4, {"dur": 1.2})])
    R.texto(t_vie, t_mis - 0.4, "VIETNAM (1955-75)", (1450, 640), px=50, d=0.4)
    ciudad(R, t_mis - 0.4, t_pla - 0.2, "la_habana", "LA HABANA", "arriba", 42)
    ciudad(R, t_mis - 0.2, t_pla - 0.2, "miami", "MIAMI", "der", 38)
    R.terreno(t_mis - 0.3, "cuba", COL["urss"], 0.8, capa=1)
    R.ruta(M.RUTAS["misiles_cuba"], t_mis - 0.1, 0.9, ancho=6.0, t1=t_pla - 0.2, flecha=True)
    ga(R, P3.misil_nuclear(), CI["la_habana"], t_mis - 0.2, t_pla - 0.2, s=0.42, off=(-120, -20), sem=607, zs=0.4, z=2, entra="sube", dy=240,
       extra=[(0.05, "siseo", 0.45)])
    pa(R, P1.kennedy(0, "serio"), 300, 1010, 1.04, t_mis - 0.15, t_pla, sem=608)
    pa(R, P1.lider_sovietico(0, "enojo"), 1620, 1010, 1.04, t_cub - 0.2, t_pla, sem=609, flip=True)
    titulo(R, t_mis - 0.1, t_pla - 0.2, "CRISIS DE LOS MISILES (1962)", px=72)
    R.texto(t_bor, t_pla - 0.2, "AL BORDE DE LA GUERRA NUCLEAR", (960, 320), px=52, d=0.5)

    # frase 2: el Plan Marshall; Hollywood y el rock and roll
    R.terreno(t_pla - 0.2, None, COL["urss"], 0.5, capa=1)
    R.ruta(M.RUTAS["tropas_europa"], t_pla - 0.1, 1.2, ancho=5.0, t1=t_hol - 0.3, flecha=True)
    andar(R, lambda p: P3.vapor_inmigrantes(p), M.RUTAS["tropas_europa"], t_pla, 2.0, t1=t_hol - 0.3, s=0.36, sem=610, zs=0.4, z=3, fps=4)
    pa(R, P2.bolsa_dolares(), 1600, 1000, 0.86, t_pla - 0.1, t_hol - 0.2, sem=611, entra="cae", dy=300, extra=[(0.05, "monedas", 0.45)])
    titulo(R, t_pla - 0.1, t_cul - 0.1, "PLAN MARSHALL", px=86)
    lugar(R, t_eur - 0.2, t_hol - 0.3, "A EUROPA", (-66.0, 38.8), off=(0, 0), px=40)
    pa(R, P1.fdr(0, "feliz"), 300, 1010, 0.98, t_pla, t_cul, sem=612)
    ciudad(R, t_hol - 0.3, t_car - 0.2, "los_angeles", "LOS ÁNGELES", "abajo", 42)
    ga(R, P3.letrero_hollywood(), CI["los_angeles"], t_hol - 0.3, t_car - 0.2, s=0.56, off=(0, -60), sem=613, zs=0.45, z=2, entra="pluma",
       d_in=0.9, extra=[(0.05, "fanfarria", 0.35)])
    pa(R, P1.rockero(0, "guino"), 1620, 1010, 1.04, t_roc - 0.2, t_car, sem=614, flip=True, extra=[(0.05, "pluck", 0.5)])
    pa(R, P3.guitarra_electrica(), 1340, 1000, 0.7, t_roc, t_car, sem=615)
    pa(R, P3.disco_vinilo(), 330, 1000, 0.8, t_hol, t_car, sem=616, extra=[(0.05, "brillo", 0.35)])
    titulo(R, t_cul - 0.1, t_car - 0.2, "HOLLYWOOD Y ROCK AND ROLL", px=72)

    # frase 3: la carrera espacial: Neil Armstrong pisa la Luna (1969)
    ciudad(R, t_car, FIN(e) + 0.3, "cabo_canaveral", "CABO CAÑAVERAL", "abajo", 40)
    pa(R, lambda t: P3.sputnik(), lambda t: lerp(-100, 2000, prog(t, t_car - 0.2, t_mil3 + 0.6)), lambda t: 260 + 40 * math.sin(t * 1.6), 0.5,
       t_car - 0.2, t_mil3 + 0.6, sem=620, z=3, entra="fija", extra=[(0.05, "pin", 0.4)])
    ga(R, P3.cohete_saturno(), CI["cabo_canaveral"], t_car, FIN(e) + 0.3, s=0.60, off=(-60, -20), sem=621, zs=0.45, z=3, entra="sube", dy=520,
       d_in=1.4, extra=[(0.05, "zoom_whoosh", 0.5)])
    titulo(R, t_car - 0.1, t_cua - 0.1, "LA CARRERA ESPACIAL", px=82)
    pa(R, P3.luna(), 1560, 520, 1.05, t_cua - 0.3, FIN(e) + 0.3, sem=622, entra="pluma", d_in=0.9)
    pa(R, P3.modulo_lunar(), 1680, 1000, 0.7, t_nei - 0.2, FIN(e) + 0.3, sem=623)
    pa(R, P1.astronauta(0, "feliz"), 300, 1010, 1.06, t_nei - 0.15, FIN(e) + 0.3, sem=624, extra=[(0.05, "fanfarria", 0.45)])
    R.texto(t_nei + 0.1, FIN(e) + 0.2, "NEIL ARMSTRONG", (300, 570), px=42, d=0.4)
    pa(R, P3.huella_bota(), 640, 1000, 0.7, t_pis - 0.1, FIN(e) + 0.3, sem=625, extra=[(0.05, "golpe_suave", 0.5)])
    titulo(R, t_luna - 0.3, FIN(e) + 0.2, "20 DE JULIO DE 1969", px=82)
