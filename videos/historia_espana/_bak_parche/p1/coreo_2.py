# -*- coding: utf-8 -*-
"""Coreografía (2/4): visigodos, al-Ándalus y Reconquista.
Capas en "eu": 0 = poder principal (Roma -> visigodos -> resto cristiano del norte -> León/Castilla), 4 = al-Ándalus,
6 = Navarra/Aragón, 7 = Cataluña, 8 = Portugal, 9 = Navarra (desde 1250)."""
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

VERDES = [(86, 150, 112), (120, 170, 100), (70, 130, 120), (150, 176, 84), (96, 160, 150), (60, 120, 90), (130, 150, 110), (100, 140, 80),
          (80, 170, 130), (140, 180, 120), (70, 110, 100), (110, 156, 96), (90, 140, 140), (126, 166, 140), (100, 120, 90)]


def cortes(R):
    pass


def construir(R):
    _visigodos(R)
    _alandalus(R)
    _reconquista(R)


# ------------------------------------------------------------------ VISIGODOS
def _visigodos(R):
    e = "visigodos"
    i0 = INI(e)
    t_roma, t_derr, t_lleg, t_vis, t_tol, t_cap = T(e, "roma"), T(e, "derrumba"), T(e, "llegan"), T(e, "visigodos"), T(e, "toledo"), T(e, "capital")
    t_pero, t_pel, t_cor, t_caro = T(e, "pero"), T(e, "peleandose"), T(e, "corona"), T(e, "caro")
    rojos = [(186, 52, 46), (170, 70, 60), (200, 80, 66), (160, 48, 50), (190, 96, 80), (176, 60, 40)] * 3
    R.romper("taifas", t_derr - 0.2, t_derr + 0.4, t_lleg + 0.2, t_vis + 0.6, colores=rojos, gap=22, deriva=40)
    R.snd(t_derr - 0.1, "crujido", 0.8, dur=0.9)
    R.terreno(t_vis, "visigodos", COL["visigodos"], 1.2)
    R.sello(t_tol + 0.1, "corona", "VISIGODOS", color=(176, 128, 40))
    R.camara(i0 - 0.2, -3.2, 40.6, 2.0)
    R.camara(t_vis, -2.6, 41.2, 1.9)
    R.camara(t_tol, -3.8, 40.0, 3.0)
    R.camara(t_pero, -3.9, 39.9, 3.4)
    R.camara(FIN(e) + 0.3, -4.0, 39.85, 3.6)
    R.anio(i0, 300)
    R.anio(t_derr + 0.4, 409)
    R.anio(t_tol - 0.2, 409)
    R.anio(t_tol + 0.6, 569)
    R.anio(t_pero, 569)
    R.anio(t_caro + 0.3, 710)
    titulo(R, t_derr - 0.1, t_lleg - 0.1, "ROMA SE DERRUMBA", px=78)
    Pv = [(1.6, 42.7), (0.2, 42.0), (-1.6, 41.1), (-3.4, 40.3), (-4.02, 39.9)]
    R.ruta(Pv, t_lleg - 0.1, 2.4, ancho=5.5, t1=t_pero, flecha=True)
    for k in range(3):
        andar(R, lambda p: E1.noble_godo(p, "serio", (110, 70, 140)), [(x + 0.35 * k, y + 0.3 * k) for x, y in Pv], t_lleg + 0.15 * k, 2.6, t1=t_pero,
              s=0.6, sem=60 + k, z=2, off=formacion(k, 3, 120))
    ciudad(R, t_tol - 0.1, FIN(e) + 0.3, "toledo", "TOLEDO", "abajo", 52)
    ga(R, E1.rey_godo(0, "feliz"), CI["toledo"], t_cap - 0.3, t_pero, s=0.72, off=(-260, 40), sem=63, z=2, extra=[(0.1, "brillo", 0.5)])
    ga(R, E1.corona_votiva(), CI["toledo"], t_cap, t_pero, s=0.55, off=(190, 40), sem=64, z=2, extra=[(0.05, "bling", 0.5)])
    # se pelean por la corona
    pa(R, lambda t: E1.noble_godo(int(t * 4) % 2, "enojo", (130, 60, 60)), 520, 1000, 1.25, t_pero - 0.1, FIN(e) + 0.4, sem=65, extra=[(0.1, "espada", 0.5)])
    pa(R, lambda t: E1.noble_godo(int(t * 4 + 1) % 2, "enojo", (60, 90, 140)), 1400, 1000, 1.25, t_pel - 0.1, FIN(e) + 0.4, sem=66, flip=True)
    pa(R, E1.corona_votiva(), lambda t: 960 + 260 * math.sin((t - t_cor) * 5.0), lambda t: 560 - 80 * abs(math.sin((t - t_cor) * 5.0)), 0.75, t_cor - 0.2,
       FIN(e) + 0.4, sem=67, extra=[(0.0, "boing", 0.4)])
    pa(R, A.estallido(12, 40, 120), 960, 820, 1.0, t_caro - 0.1, t_caro + 0.5, entra="fija", sale="cortar", sem=68, snd=("golpe_suave", 0.6))
    R.snd(t_pel + 0.3, "espada", 0.5)
    R.snd(t_cor + 0.4, "espada", 0.5, tono=1.2)


# ------------------------------------------------------------------ AL-ÁNDALUS
def _alandalus(R):
    e = "alandalus"
    i0 = INI(e)
    t_711, t_ejer, t_cruza, t_estr = T(e, "setecientos"), T(e, "ejercito"), T(e, "cruza"), T(e, "estrecho")
    t_gen, t_tariq, t_nombre, t_roca, t_gib, t_mont = T(e, "general"), T(e, "tariq"), T(e, "nombre"), T(e, "roca"), T(e, "gibraltar"), T(e, "montana")
    t_siete, t_toda, t_al = T(e, "siete"), T(e, "toda"), T(e, "al", frase=2)
    t_cord, t_grandes, t_europa, t_929, t_emir, t_califa = (T(e, "cordoba"), T(e, "grandes"), T(e, "europa"), T(e, "novecientos"), T(e, "emir"),
                                                             T(e, "califa"))
    t_arroz, t_azuc, t_nar, t_pal, t_ace, t_alm, t_azul, t_oja = (T(e, "arroz"), T(e, "azucar"), T(e, "naranjas"), T(e, "palabras"), T(e, "aceite"),
                                                                  T(e, "almohada"), T(e, "azulejo"), T(e, "ojala"))
    # territorio
    R.terreno(i0 - 0.3, "omeyas_afr", COL["omeyas"], 0.8, capa=4)
    R.terreno(t_siete - 0.4, "andalus_711", COL["andalus"], 0.6, capa=4)
    R.terreno(t_siete + 0.3, "andalus_718", COL["andalus"], 2.2, capa=4)
    R.terreno(t_toda + 0.6, "asturias_722", COL["visigodos"], 1.4)
    R.sello(t_al + 0.2, "arco", "AL-ÁNDALUS", color=(52, 120, 84))
    # cámara
    R.camara(i0 - 0.3, -5.2, 36.3, 4.4)
    R.camara(t_cruza, -5.4, 36.1, 5.6)
    R.camara(t_gen, -5.35, 36.15, 6.6)
    R.camara(t_mont + 0.4, -5.3, 36.3, 6.0)
    R.camara(t_siete + 0.2, -4.0, 39.0, 2.3)
    R.camara(t_al + 0.5, -3.8, 39.6, 2.25)
    R.camara(t_cord, -4.78, 37.95, 4.6)
    R.camara(t_califa + 0.3, -4.78, 37.9, 5.0)
    R.camara(t_arroz, -4.5, 37.6, 3.6)
    R.camara(FIN(e) + 0.3, -4.2, 38.0, 3.2)
    # años
    R.anio(i0, 710)
    R.anio(t_711 + 0.4, 711)
    R.anio(t_siete - 0.2, 711)
    R.anio(t_al + 0.4, 718)
    R.anio(t_cord - 0.2, 718)
    R.anio(t_cord + 0.8, 756)
    R.anio(t_929 - 0.2, 756)
    R.anio(t_929 + 0.6, 929)
    R.anio(t_arroz - 0.1, 929)
    R.anio(FIN(e), 1000)
    # cruzan el estrecho
    Pt = [(-5.45, 35.75), (-5.42, 35.95), (-5.38, 36.12)]
    for k in range(3):
        andar(R, lambda p: E3.galera(p, (70, 130, 90), (240, 236, 220)), [(x - 0.12 + 0.12 * k, y + 0.02 * k) for x, y in Pt], t_ejer + 0.25 * k, 2.4,
              t1=t_gen, s=0.36, sem=70 + k, zs=0.4, z=2, fps=4, flip=False, snd=("ola", 0.35), off=formacion(k, 3, 120))
    titulo(R, t_cruza - 0.1, t_gen - 0.2, "EL ESTRECHO", px=70)
    lugar(R, t_cruza, t_gen - 0.1, "ÁFRICA", (-5.95, 35.42), off=(0, 0), px=46)
    lugar(R, t_cruza + 0.2, t_gen - 0.1, "EUROPA", (-4.7, 36.78), off=(0, 0), px=46)
    # Tariq y su roca
    pa(R, E2.tariq(0, "serio"), 470, 1000, 1.25, t_gen - 0.1, t_siete - 0.1, sem=73, extra=[(0.1, "cuerno", 0.4)])
    R.texto(t_tariq - 0.05, t_siete - 0.2, "TARIQ", (470, 560), px=66, d=0.4)
    ga(R, E3.penon(False), CI["gibraltar"], t_roca - 0.15, t_siete - 0.1, s=0.62, off=(80, 30), sem=74, z=1,
       snd=("crece", 0.5), entra="sube")
    R.texto(t_mont - 0.1, t_siete - 0.2, "YABAL TARIQ", (560, 200), px=76, d=0.5)
    R.texto(t_gib - 0.05, t_siete - 0.2, "= GIBRALTAR", (560, 310), px=66, d=0.5)
    R.snd(t_gib, "escribir", 0.45, dur=0.6)
    # casi toda la península
    R.rio(M.RUTAS["conquista_711"], t_siete - 0.3, 2.0, COL["andalus"], ancho=14, t1=t_cord - 0.2)
    lugar(R, t_al, t_cord - 0.7, "AL-ÁNDALUS", (-4.4, 39.6), off=(0, 0), px=76)
    for k, geo in enumerate(((-6.0, 37.6), (-2.4, 37.9), (-1.8, 40.1))):
        ga(R, E2.soldado_omeya(k % 2, "serio"), geo, t_toda + 0.15 * k, t_cord - 0.2, s=0.58, sem=75 + k, z=2)
    # Córdoba y el califato
    ciudad(R, t_cord - 0.1, FIN(e) + 0.3, "cordoba", "CÓRDOBA", "izq", 54)
    ga(R, E2.mezquita(), CI["cordoba"], t_cord + 0.1, t_arroz - 0.2, s=0.55, off=(300, 230), sem=78, z=1, entra="pluma", d_in=0.9, snd=("crece", 0.5))
    titulo(R, t_grandes - 0.1, t_929 - 0.2, "UNA DE LAS MAYORES CIUDADES DE EUROPA", px=60)
    pa(R, E2.califa(0, "feliz"), 470, 1000, 1.3, t_emir - 0.15, t_arroz - 0.2, sem=79, extra=[(0.1, "brillo", 0.5)])
    titulo(R, t_califa - 0.1, t_arroz - 0.3, "CALIFATO DE CÓRDOBA", px=80)
    R.snd(t_califa, "gong", 0.5)
    # lo que llega: cultivos y palabras
    pa(R, A.arrozal(), 300, 1010, 1.7, t_arroz - 0.1, FIN(e) + 0.4, sem=80)
    pa(R, E2.cana_azucar(), 640, 1010, 1.25, t_azuc - 0.1, FIN(e) + 0.4, sem=81)
    pa(R, lambda t: E2.naranjo(int(t * 3) % 6), 980, 1010, 1.3, t_nar - 0.1, FIN(e) + 0.4, sem=82)
    for k, (t0, txt, x, y, px) in enumerate(((t_ace, "ACEITE", 520, 250, 72), (t_alm, "ALMOHADA", 960, 190, 72), (t_azul, "AZULEJO", 1400, 250, 72),
                                             (t_oja, "¡OJALÁ!", 1450, 560, 110))):
        R.texto(t0 - 0.05, FIN(e) + 0.4, txt, (x, y), px=px, d=0.35)
        R.snd(t0, "pluck", 0.5, tono=1.0 + 0.12 * k)
    pa(R, E2.azulejo(), 1660, 900, 0.75, t_azul - 0.05, FIN(e) + 0.4, sem=83)
    R.snd(t_oja + 0.1, "estrellitas", 0.4)


# ------------------------------------------------------------------ RECONQUISTA
def _reconquista(R):
    e = "reconquista"
    i0 = INI(e)
    t_mont, t_norte, t_noble, t_pel, t_vence, t_cova = T(e, "montanas"), T(e, "norte"), T(e, "noble"), T(e, "pelayo"), T(e, "vence"), T(e, "covadonga")
    t_nacen, t_crist, t_siglos, t_emp, t_front, t_sur = T(e, "nacen"), T(e, "cristianos", frase=1), T(e, "siglos"), T(e, "empujan"), T(e, "frontera"), T(e, "sur")
    t_1031, t_calif, t_est, t_veinte, t_peq, t_taif = T(e, "mil", frase=2), T(e, "califato"), T(e, "estalla"), T(e, "veinte"), T(e, "pequenos"), T(e, "taifas")
    t_aprov, t_toledo, t_cid, t_conq, t_val = T(e, "aprovechan"), T(e, "toledo"), T(e, "cid"), T(e, "conquista"), T(e, "valencia")
    t_1212, t_navas, t_bal, t_romp = T(e, "mil", frase=4), T(e, "navas"), T(e, "balanza"), T(e, "rompe")
    t_caen, t_cord, t_sev, t_queda, t_gran = T(e, "caen"), T(e, "cordoba"), T(e, "sevilla"), T(e, "queda"), T(e, "granada")
    # territorio
    R.terreno(t_norte, "asturias_722", COL["asturias"], 0.8)
    R.terreno(t_nacen, "leon_1000", COL["leon"], 2.2)
    R.terreno(t_nacen + 0.3, "navarra_1000", COL["navarra"], 1.6, capa=6)
    R.terreno(t_nacen + 0.5, "cataluna_1000", COL["cataluna"], 1.6, capa=7)
    R.terreno(t_nacen, "andalus_1000", COL["andalus"], 2.2, capa=4)
    R.romper("taifas", t_est - 0.1, t_est + 0.5, t_toledo - 0.3, t_toledo + 0.5, colores=VERDES, capa=4, gap=20, deriva=34)
    R.snd(t_est - 0.1, "crujido", 0.9, dur=0.9)
    R.terreno(t_toledo - 0.1, "andalus_1100", COL["andalus"], 1.2, capa=4)
    R.terreno(t_toledo - 0.1, "castilla_1100", COL["castilla"], 1.2)
    R.terreno(t_toledo, "aragon_1100", COL["aragon"], 1.2, capa=6)
    R.terreno(t_toledo + 0.1, "cataluna_1100", COL["cataluna"], 1.2, capa=7)
    R.terreno(t_1212, "portugal_1250", COL["portugal"], 1.0, capa=8)
    R.terreno(t_caen - 0.2, "castilla_1250", COL["castilla"], 1.6)
    R.terreno(t_caen - 0.1, "aragon_1250", COL["aragon"], 1.6, capa=6)
    R.terreno(t_caen - 0.1, None, COL["cataluna"], 1.0, capa=7)
    R.terreno(t_caen, "navarra_1250", COL["navarra"], 1.2, capa=9)
    R.terreno(t_caen - 0.2, "granada", COL["granada"], 1.8, capa=4)
    R.sello(t_crist + 0.1, "castillo", "REINOS CRISTIANOS", color=(130, 60, 130))
    # cámara
    R.camara(i0 - 0.3, -4.6, 42.4, 3.4)
    R.camara(t_noble, -5.0, 43.15, 6.2)
    R.camara(t_cova + 0.3, -5.05, 43.2, 6.6)
    R.camara(t_nacen + 0.4, -3.6, 40.4, 2.3)
    R.camara(t_sur + 0.3, -3.5, 40.0, 2.3)
    R.camara(t_est, -3.6, 39.2, 2.6)
    R.camara(t_taif + 0.3, -3.6, 39.3, 2.5)
    R.camara(t_toledo, -3.0, 40.0, 2.35)
    R.camara(t_val + 0.3, -2.4, 40.0, 2.5)
    R.camara(t_navas - 0.2, -3.6, 38.4, 4.2)
    R.camara(t_romp + 0.3, -3.6, 38.3, 4.4)
    R.camara(t_caen + 0.2, -4.4, 37.9, 2.8)
    R.camara(t_gran - 0.3, -3.6, 37.3, 4.0)
    R.camara(FIN(e) + 0.3, -3.6, 37.25, 4.3)
    # años
    R.anio(i0, 718)
    R.anio(t_cova, 722)
    R.anio(t_nacen, 722)
    R.anio(t_sur + 0.3, 1000)
    R.anio(t_1031 - 0.2, 1000)
    R.anio(t_1031 + 0.6, 1031)
    R.anio(t_toledo - 0.2, 1031)
    R.anio(t_toledo + 0.5, 1085)
    R.anio(t_val, 1094)
    R.anio(t_1212 - 0.2, 1094)
    R.anio(t_1212 + 0.6, 1212)
    R.anio(t_cord - 0.1, 1212)
    R.anio(t_cord + 0.4, 1236)
    R.anio(t_sev + 0.4, 1248)
    R.anio(FIN(e), 1250)
    # Covadonga
    ciudad(R, t_cova - 0.1, t_nacen + 0.2, "covadonga", "COVADONGA", "abajo", 52)
    ga(R, E2.pelayo(0, "serio"), CI["covadonga"], t_pel - 0.15, t_nacen + 0.2, s=0.62, off=(-150, 40), sem=90, z=2, extra=[(0.1, "cuerno", 0.4)])
    for k in range(2):
        ga(R, E2.soldado_omeya(k, "miedo"), CI["covadonga"], t_noble + 0.1 * k, t_vence + 0.4, s=0.5, off=(160 + 120 * k, 120), sem=91 + k, z=2, flip=True,
           sale="der_fuera", d_out=0.7)
    pa(R, A.estallido(12, 40, 130), 1060, 640, 1.0, t_vence - 0.05, t_vence + 0.45, entra="fija", sale="cortar", sem=93, snd=("golpe_suave", 0.6))
    titulo(R, t_vence - 0.1, t_cova + 0.4, "722: BATALLA DE COVADONGA", px=58, y=170)
    # los reinos cristianos empujan hacia el sur
    for k, (geo, txt) in enumerate((((-5.4, 42.4), "LEÓN"), ((-1.7, 42.55), "NAVARRA"), ((1.7, 41.95), "BARCELONA"))):
        lugar(R, t_crist + 0.2 + 0.2 * k, t_emp + 0.1, txt, geo, off=(0, 0), px=44)
    for k, x in enumerate((-6.6, -4.2, -2.6)):
        andar(R, lambda p, k=k: E2.caballero(p, COL["leon"]), [(x, 41.5), (x + 0.1, 40.5)], t_emp - 0.2 + 0.15 * k, 1.8, t1=t_1031, s=0.48, sem=94 + k, z=2,
              fps=8, flip=False, snd=("galope", 0.4))
    R.ruta([(-5.0, 41.9), (-5.0, 40.6)], t_front - 0.1, 0.9, ancho=6, t1=t_1031, flecha=True)
    R.ruta([(-2.6, 42.0), (-2.6, 40.8)], t_front, 0.9, ancho=6, t1=t_1031, flecha=True)
    # taifas
    titulo(R, t_taif - 0.15, t_aprov - 0.1, "LAS TAIFAS", px=86)
    for k, cl in enumerate(("sevilla", "toledo", "badajoz", "granada", "valencia")):
        ga(R, E2.rey_taifa(k % 2, "enojo", VERDES[k * 2]), CI[cl], t_veinte + 0.12 * k, t_toledo - 0.2, s=0.42, sem=97 + k, z=2, flip=k % 2 == 1,
           snd=("pop", 0.35))
    # cae Toledo; el Cid en Valencia
    ciudad(R, t_toledo - 0.1, t_1212, "toledo", "TOLEDO 1085", "der", 46)
    ga(R, E2.rey_cristiano(0, "feliz"), CI["toledo"], t_toledo, t_1212, s=0.55, off=(-150, 30), sem=102, z=2, extra=[(0.05, "fanfarria", 0.35)])
    andar(R, lambda p: E2.cid(p), [CI["burgos"], (-2.0, 41.3), (-0.6, 39.6)], t_cid - 0.4, (t_val + 0.4) - (t_cid - 0.4), t1=t_1212, s=0.6, sem=103,
          z=3, fps=8, snd=("galope", 0.5))
    lugar(R, t_val, t_1212 - 0.1, "EL CID", (-0.6, 39.6), off=(60, -390), px=58)
    ciudad(R, t_val - 0.1, t_1212, "valencia", "VALENCIA 1094", "abajo", 44)
    # Navas de Tolosa: la balanza
    lugar(R, t_navas - 0.1, t_caen - 0.1, "LAS NAVAS DE TOLOSA", CI["navas"], off=(0, -300), px=54)
    for k in range(2):
        ga(R, lambda t, k=k: E2.caballero(int(t * 8 + k) % 4, COL["castilla"]), CI["navas"], t_1212 + 0.15 * k, t_caen, s=0.5, off=(-470 + 170 * k, 110 + 60 * k),
           sem=104 + k, z=2, snd=("galope", 0.4))
        ga(R, lambda t, k=k: E2.jinete_moro(int(t * 8 + k + 2) % 4), CI["navas"], t_1212 + 0.3 + 0.15 * k, t_caen, s=0.5, off=(330 - 170 * k, 120 + 60 * k),
           sem=106 + k, z=2, flip=True, snd=("galope", 0.4))
    pa(R, A.estallido(16, 50, 160), 960, 640, 1.1, t_navas, t_navas + 0.6, entra="fija", sale="cortar", sem=108, snd=("explosion", 0.5))
    pa(R, lambda t: E2.balanza(round(kf(t, [(t_bal, 0.0), (t_romp, 0.0), (t_romp + 0.6, 0.42)], ease=e_back), 2)), 1620, 1000, 1.05, t_bal - 0.2, t_caen,
       sem=109, z=3, extra=[(0.5, "boing", 0.4)])
    R.snd(t_romp + 0.1, "golpe_suave", 0.6)
    # caen Córdoba y Sevilla; queda Granada
    for k, (cl, t0) in enumerate((("cordoba", t_cord), ("sevilla", t_sev))):
        ciudad(R, t0 - 0.1, t_queda - 0.2, cl, None)
        lugar(R, t0, t_queda - 0.3, ("CÓRDOBA 1236", "SEVILLA 1248")[k], CI[cl], off=(0, -190), px=44)
        ga(R, E2.rey_cristiano(k, "feliz"), CI[cl], t0, t_queda - 0.2, s=0.44, off=(0, 50), sem=110 + k, z=2, extra=[(0.05, "campana", 0.4)])
    ga(R, E2.alhambra(), CI["granada"], t_queda - 0.1, FIN(e) + 0.4, s=0.6, off=(20, 40), sem=112, z=2, entra="pluma", d_in=0.9, snd=("crece", 0.5))
    lugar(R, t_gran - 0.1, FIN(e) + 0.3, "REINO DE GRANADA", CI["granada"], off=(0, 120), px=60)
