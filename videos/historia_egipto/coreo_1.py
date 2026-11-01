# -*- coding: utf-8 -*-
"""Coreografía (1/4): gancho (el río en el desierto, los monumentos, los reyes-dioses), orígenes (la franja verde, la crecida, Narmer
y la doble corona, Menfis, los jeroglíficos), las pirámides (Saqqara e Imhotep, Guiza, Keops, la Esfinge, 3.800 años de récord) y el
Primer Periodo Intermedio y el Reino Medio (sequías, nomarcas, Tebas, Karnak, los hicsos con sus carros).
Capas de territorio: 0 = Egipto, 1 = rivales (Bajo Egipto en la unificación, hicsos)."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_eg1 as E1
import obj_eg2 as E2
import obj_eg3 as E3
from core import FIN, INI, T, kf, linea_punteada
from coreo_util import CI, COL, andar, ciudad, formacion, ga, grupo, lugar, mece, nilo, pa, titulo, tramo
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog

ARENA_TXT = (150, 112, 70)


def cortes(R):
    pass


def construir(R):
    _mares(R)
    _gancho(R)
    _origenes(R)
    _piramides(R)
    _intermedio(R)


def _mares(R):
    R.mar("eg", "MAR MEDITERRÁNEO", 26.0, 33.3, 40, 0.42)
    R.mar("eg", "MAR MEDITERRÁNEO", 32.6, 32.45, 34, 0.40)
    R.mar("eg", "MAR ROJO", 36.9, 21.9, 38, 0.44, rot=-1.02)
    R.mar("eg", "MAR ROJO", 34.15, 27.0, 26, 0.40, rot=-1.0)
    R.mar("eg", "DESIERTO LÍBICO", 27.6, 25.4, 34, 0.32, color=ARENA_TXT)
    R.mar("eg", "DESIERTO ARÁBIGO", 33.55, 25.3, 22, 0.30, rot=-1.15, color=ARENA_TXT)
    R.mar("eg", "SINAÍ", 33.85, 29.05, 26, 0.34, color=ARENA_TXT)
    R.mar("eg", "NUBIA", 31.3, 19.7, 34, 0.33, color=ARENA_TXT)
    R.mar("eg", "ARABIA", 42.6, 24.6, 40, 0.32, color=ARENA_TXT)
    R.mar("eg", "ANATOLIA", 33.2, 39.3, 38, 0.32, color=ARENA_TXT)
    R.mar("eg", "MESOPOTAMIA", 44.4, 33.9, 28, 0.30, rot=-0.55, color=ARENA_TXT)
    R.mar("eg", "RÍO NILO", 31.78, 27.45, 26, 0.46, rot=1.28, color=(60, 110, 160))


def _salto(R, t, n=3, s=0.5):
    """Varias chispas de golpe (aparición importante)."""
    for k in range(n):
        R.snd(t + 0.04 * k, "brillo", 0.25 + 0.05 * k)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    t_rio, t_des, t_civ, t_tie = T(e, "rio"), T(e, "desierto"), T(e, "civilizaciones"), T(e, "tierra")
    t_cons, t_mon, t_des2, t_tiem, t_rey, t_proc, t_dios = (T(e, "construyeron"), T(e, "monumentos"), T(e, "desafiaron"), T(e, "tiempo"), T(e, "reyes"),
                                                           T(e, "proclamaron"), T(e, "dioses"))
    t_esta, t_hist, t_egi, t_cinco, t_min = T(e, "esta"), T(e, "historia"), T(e, "egipto"), T(e, "cinco"), T(e, "minutos")
    # cámara: el valle del Nilo de cerca -> Guiza -> todo Egipto
    R.camara(0.0, 31.55, 26.55, 3.4)
    R.camara(t_tie + 0.3, 31.3, 28.4, 3.1)
    R.camara(t_mon + 0.3, 31.16, 29.93, 7.6)
    R.camara(t_dios + 0.6, 31.2, 29.75, 6.2)
    R.camara(t_egi, 31.0, 27.6, 2.0)
    R.camara(FIN(e) + 0.7, 31.0, 27.4, 1.9)
    # el río: un brillo de agua que recorre el Nilo de Asuán al Delta
    Pn = tramo(nilo(), (32.9, 24.1), (31.24, 30.1), 40)
    R.rio(Pn, t_rio, 2.4, (160, 206, 232), ancho=13, tinta=False, t1=t_cons)
    R.snd(t_rio, "viento", 0.28, dur=3.0)
    # vida en el río y en la orilla desde el primer cuadro
    Pf = tramo(nilo(), (32.62, 25.75), (31.25, 29.9), 30)
    andar(R, lambda p: E3.falua(p), Pf, -0.6, 6.6, t1=t_cons + 0.3, s=0.42, sem=1, zs=0.3, z=2, fps=4, ease=lambda u: u)
    Pb = tramo(nilo(), (31.2, 29.0), (31.95, 26.4), 30)
    andar(R, lambda p: E3.barca_papiro(p), Pb, -0.8, 6.8, t1=t_cons + 0.3, s=0.34, sem=2, zs=0.3, z=2, fps=4, ease=lambda u: u)
    for k, (g, dx) in enumerate((((32.25, 26.1), -70), ((31.85, 26.55), 80), ((31.42, 27.35), -80), ((30.95, 28.05), 80), ((32.62, 25.55), 80))):
        ga(R, E3.palmera(240 + 30 * (k % 2)), g, -0.5 + 0.1 * k, t_cons + 0.2, s=0.3, off=(dx, 10), sem=3 + k, zs=0.4, z=1, entra="fija")
    ga(R, lambda t: E3.cocodrilo(int(t * 3) % 4), (32.42, 25.95), -0.4, t_cons + 0.2, s=0.18, off=(20, 18), sem=9, zs=0.4, z=1, entra="fija")
    ga(R, lambda t: E3.ibis(int(t * 4) % 4), (31.62, 26.95), 0.4, t_cons + 0.2, s=0.24, off=(60, 6), sem=10, zs=0.4, z=1)
    # caravana por el desierto
    grupo(R, lambda p: E3.camello(p), [(29.4, 26.0), (29.9, 26.7), (30.5, 27.3)], t_des - 0.4, 4.6, n=2, ancho=120, t1=t_cons + 0.3, s=0.26, sem=11, fps=5,
          ease=lambda u: u)
    lugar(R, t_des, t_cons - 0.3, "DESIERTO", (29.8, 27.4), off=(0, -10), px=50)
    R.snd(t_des, "arena", 0.3, dur=1.4)
    # la civilización: gente a la orilla
    for k, (dib, g, dx) in enumerate(((E1.campesino(0, "feliz"), (31.4, 27.6), -110), (E1.campesina(0, "feliz"), (31.25, 28.0), 110),
                                      (E1.escriba(0, "feliz"), (31.0, 28.5), -110))):
        ga(R, dib, g, t_civ + 0.15 * k, t_cons + 0.3, s=0.36, off=(dx, 20), sem=13 + k, zs=0.4, z=2)
    R.snd(t_civ, "pluck", 0.4)
    # los monumentos que desafiaron al tiempo
    ga(R, E2.piramides_guiza(), CI["guiza"], t_mon - 0.2, t_esta + 0.2, s=0.5, off=(-90, 10), sem=16, zs=0.5, z=1, entra="sube", d_in=0.7, dy=500)
    ga(R, E2.esfinge(), CI["guiza"], t_mon + 0.3, t_esta + 0.2, s=0.32, off=(250, 70), sem=17, zs=0.5, z=2, entra="sube", d_in=0.6, dy=400)
    ga(R, E2.obelisco(), CI["heliopolis"], t_mon + 0.6, t_esta + 0.2, s=0.38, off=(-20, 30), sem=18, zs=0.5, z=1, entra="sube", d_in=0.5, dy=400)
    R.snd(t_mon - 0.1, "crece", 0.5, dur=0.9)
    pa(R, A.arena_reloj(), 1620, 560, 0.75, t_des2, t_rey + 1.6, sem=19, extra=[(0.05, "tick", 0.35)])
    R.texto(t_tiem - 0.1, t_rey + 1.4, "5.000 AÑOS", (1620, 330), px=56, d=0.5)
    # reyes que se proclamaron dioses
    pa(R, A.sol_brillo(), 330, 690, 1.05, t_dios - 0.1, t_esta + 0.1, sem=20, z=1, entra="pop", extra=[(0.05, "brillo", 0.45)])
    pa(R, E1.keops(0, "serio"), 330, 1020, 1.2, t_rey - 0.1, t_esta + 0.1, sem=21, z=2, extra=[(0.05, "fanfarria", 0.32)])
    pa(R, E2.dios("ra"), 640, 1020, 1.0, t_dios, t_esta + 0.1, sem=22, z=2, entra="sube", dy=600)
    R.texto(t_rey + 0.2, t_esta, "REYES", (330, 510), px=56, d=0.4)
    R.texto(t_dios + 0.1, t_esta, "DIOSES", (640, 560), px=56, d=0.4)
    # título
    R.terreno(t_egi - 0.2, "egipto_mod", COL["egipto_mod"], 0.8)
    R.terreno(FIN(e) + 0.5, None, COL["egipto_mod"], 0.3)
    R.snd(t_egi - 0.2, "whoosh", 0.45, dur=0.8)
    R.texto(t_hist - 0.3, FIN(e) + 0.9, "LA HISTORIA DE EGIPTO", (960, 178), px=100, d=1.0)
    R.texto(t_cinco - 0.1, FIN(e) + 0.9, "en 5 minutos", (960, 300), px=76, d=0.6)
    R.snd(t_hist - 0.3, "escribir", 0.45, dur=1.0)
    pa(R, lambda t: C.cronometro(round(kf(t, [(t_cinco, 0.0), (FIN(e) + 1.2, 0.9)], ease=lambda u: u), 2)), 1660, 860, 0.85, t_cinco - 0.1, sem=23,
       extra=[(0.1, "reloj_rapido", 0.4, {"dur": 1.2})])


# ------------------------------------------------------------------ ORÍGENES
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_fra, t_ver, t_are, t_fer, t_cre = T(e, "franja"), T(e, "verde"), T(e, "arena"), T(e, "fertilizada"), T(e, "crecidas")
    t_tres, t_nar, t_uni, t_alto, t_bajo, t_cor = T(e, "tres"), T(e, "narmer"), T(e, "unifica"), T(e, "alto"), T(e, "bajo"), T(e, "corona")
    t_nace, t_trei, t_cap, t_men = T(e, "nace"), T(e, "treinta"), T(e, "capital"), T(e, "menfis")
    t_sac, t_jer, t_cos, t_tem, t_nom = T(e, "sacerdotes"), T(e, "jeroglificos"), T(e, "cosechas"), T(e, "templos"), T(e, "nombres")
    # cámara
    R.camara(i0 - 0.2, 31.6, 26.35, 4.3)
    R.camara(t_are, 31.8, 26.15, 4.6)
    R.camara(t_cre + 0.6, 31.7, 26.3, 4.0)
    R.camara(t_tres + 0.4, 31.2, 27.65, 2.1)
    R.camara(t_cor + 0.6, 31.2, 27.75, 2.0)
    R.camara(t_trei + 0.4, 31.25, 29.5, 3.6)
    R.camara(t_men + 0.2, 31.25, 29.85, 6.4)
    R.camara(FIN(e) + 0.4, 31.3, 29.78, 6.0)
    # años
    R.anio(t_tres + 0.1, -3100)
    # la franja verde
    lugar(R, t_ver, t_cre - 0.4, "FRANJA VERDE", (31.95, 26.95), off=(170, -30), px=50)
    ga(R, Bb.flecha(), (31.95, 26.95), t_ver - 0.05, t_cre - 0.4, s=0.62, off=(30, 20), sem=30, zs=0.2, z=3, flip=True)
    R.snd(t_ver, "pincel", 0.4, dur=0.8)
    lugar(R, t_are, t_cre + 1.0, "ARENA", (30.9, 25.85), off=(0, 0), px=48)
    lugar(R, t_are + 0.2, t_cre + 1.0, "ARENA", (33.15, 26.75), off=(0, 0), px=48)
    # la vida del valle: campesinos, buey, papiro, animales del Nilo
    V = [((32.25, 26.12), -90), ((32.62, 25.9), 90), ((31.85, 26.55), -110), ((32.05, 26.3), 100), ((31.62, 26.95), -80), ((32.75, 25.6), -90)]
    ga(R, lambda t: E1.segador(int(t * 3) % 2, "feliz"), V[0][0], i0 + 0.3, FIN(e, 0) + 0.2, s=0.36, off=(V[0][1], 10), sem=31, zs=0.4, z=2)
    ga(R, lambda t: E1.campesino(int(t * 3) % 2, "feliz"), V[1][0], i0 + 0.6, FIN(e, 0) + 0.2, s=0.36, off=(V[1][1], 10), sem=32, zs=0.4, z=2)
    ga(R, lambda t: E3.buey(int(t * 4) % 4), V[2][0], t_fra, FIN(e, 0) + 0.2, s=0.26, off=(V[2][1], 10), sem=33, zs=0.4, z=2)
    ga(R, E1.campesina(0, "feliz"), V[3][0], t_fra + 0.4, FIN(e, 0) + 0.2, s=0.34, off=(V[3][1], 10), sem=34, zs=0.4, z=2)
    ga(R, E3.papiro_planta(), V[4][0], i0 + 0.2, FIN(e, 0) + 0.2, s=0.26, off=(V[4][1], 10), sem=35, zs=0.4, z=1)
    ga(R, E2.gavilla(), V[5][0], t_fer, FIN(e, 0) + 0.2, s=0.3, off=(V[5][1], 10), sem=36, zs=0.4, z=1)
    ga(R, lambda t: E3.cocodrilo(int(t * 3) % 4), (32.2, 26.2), i0 + 0.1, FIN(e, 0) + 0.2, s=0.18, off=(10, 6), sem=37, zs=0.4, z=1)
    ga(R, E3.hipopotamo(), (31.75, 26.75), t_are + 0.3, FIN(e, 0) + 0.2, s=0.18, off=(0, 8), sem=38, zs=0.4, z=1)
    ga(R, lambda t: E3.ibis(int(t * 4) % 4), (32.5, 25.95), t_fer, FIN(e, 0) + 0.2, s=0.22, off=(80, 0), sem=39, zs=0.4, z=1)
    andar(R, lambda p: E3.falua(p), tramo(nilo(), (32.7, 25.5), (31.6, 27.0), 20), i0 - 0.2, 6.6, t1=FIN(e, 0) + 0.2, s=0.36, sem=40, zs=0.3, z=2, fps=4,
          ease=lambda u: u)
    R.snd(t_fra, "pluck", 0.35)
    # la crecida: el río se desborda por todo el valle y lo fertiliza
    R.rio(tramo(nilo(), (32.9, 24.1), (31.25, 29.9), 50), t_cre - 0.1, 1.5, (120, 172, 212), ancho=40, tinta=False, t1=t_tres + 0.2)
    pa(R, E2.crecida(), 1590, 600, 0.7, t_cre - 0.1, t_tres + 0.2, sem=41, entra="sube", dy=500, extra=[(0.05, "ola", 0.55)])
    R.texto(t_cre + 0.2, t_tres + 0.1, "LA CRECIDA", (1590, 340), px=56, d=0.5)
    R.snd(t_cre + 0.3, "chapuzon", 0.35)
    # Narmer: Alto y Bajo Egipto se unen bajo la doble corona
    pa(R, E2.paleta_narmer(), 330, 1010, 0.95, t_nar - 0.7, t_nace + 0.4, sem=42, extra=[(0.05, "piedra" if False else "golpe_suave", 0.5)])
    R.texto(t_nar - 0.3, t_nace + 0.3, "PALETA DE NARMER", (330, 660), px=40, d=0.5)
    R.terreno(t_tres + 0.2, "alto", COL["alto"], 0.8)
    R.terreno(t_tres + 0.7, "bajo", COL["bajo"], 0.8, capa=1)
    R.snd(t_tres + 0.2, "whoosh", 0.35, dur=0.6)
    R.snd(t_tres + 0.7, "whoosh", 0.35, dur=0.6)
    titulo(R, t_tres + 0.3, t_nar + 0.4, "DOS REINOS", px=84)
    ga(R, E1.campesino(0, "feliz", None), CI["tebas"], t_tres + 0.5, t_alto - 0.1, s=0.34, off=(-120, 0), sem=55, zs=0.4, z=2)
    ga(R, E1.campesina(0, "feliz"), CI["menfis"], t_tres + 0.9, t_bajo - 0.1, s=0.34, off=(120, 30), sem=56, zs=0.4, z=2)
    lugar(R, t_alto, t_cor + 0.3, "ALTO EGIPTO", (34.4, 26.7), off=(0, 0), px=46)
    lugar(R, t_bajo, t_cor + 0.3, "BAJO EGIPTO", (28.2, 30.2), off=(0, 0), px=46)
    ga(R, E1.rey_alto(0, "serio"), CI["nejen"], t_alto - 0.1, t_cor, s=0.42, off=(110, 10), sem=43, zs=0.4, z=2)
    ga(R, E1.rey_bajo(0, "enojo"), (30.73, 31.2), t_bajo - 0.1, t_cor, s=0.42, off=(-150, 150), sem=44, zs=0.4, z=2)
    andar(R, lambda p: E1.narmer(p % 2, "pschent", "serio"), tramo(nilo(), (32.78, 25.1), (31.25, 29.85), 20), t_uni - 0.1, t_cor - t_uni + 0.3,
          t1=t_sac - 0.2, s=0.48, sem=45, zs=0.4, z=3, fps=5)
    R.snd(t_uni, "pasos", 0.4, dur=1.6)
    pa(R, E2.corona_doble(), 1580, 580, 0.8, t_cor - 0.1, t_nace + 1.6, sem=46, entra="pop", extra=[(0.05, "brillo", 0.5)])
    R.texto(t_cor + 0.3, t_nace + 1.5, "CORONA DOBLE", (1580, 300), px=52, d=0.5)
    R.terreno(t_cor + 0.2, "reino_antiguo", COL["egipto"], 0.9)
    R.terreno(t_cor + 0.2, None, COL["bajo"], 0.7, capa=1)
    R.sello(t_nace + 0.1, "corona_doble", "I DINASTÍA", color=(198, 52, 52))
    # más de treinta dinastías y Menfis
    R.contador(t_trei - 0.3, t_trei + 0.9, 1, 30, (960, 196), px=84, formato="{} DINASTÍAS", hasta_t=t_cap + 0.4)
    R.snd(t_trei - 0.2, "reloj_rapido", 0.35, dur=1.0)
    ciudad(R, t_cap - 0.1, t_jer - 0.3, "menfis", "MENFIS", "abajo", 52)
    ga(R, E2.ciudad_antigua(), CI["menfis"], t_cap, t_jer - 0.3, s=0.42, off=(0, -30), sem=47, zs=0.5, z=1, entra="sube", d_in=0.6, dy=300)
    R.snd(t_cap, "crece", 0.4, dur=0.7)
    R.texto(t_men + 0.2, t_sac + 0.4, "LA CAPITAL", (960, 196), px=74, d=0.5)
    # los jeroglíficos
    pa(R, E1.sacerdote(0, "serio"), 250, 1010, 1.0, t_sac - 0.1, FIN(e) + 0.4, sem=48)
    pa(R, E1.escriba(0, "feliz"), 510, 1010, 0.95, t_sac + 0.3, FIN(e) + 0.4, sem=49, flip=True)
    pa(R, E2.tablilla_jeroglificos(), 1120, 790, 1.0, t_jer - 0.15, FIN(e) + 0.4, sem=50, entra="pluma", d_in=1.6, extra=[(0.05, "escribir", 0.5, {"dur": 1.5})])
    titulo(R, t_jer, FIN(e) + 0.3, "JEROGLÍFICOS", px=82)
    pa(R, E2.gavilla(), 1560, 1010, 0.5, t_cos - 0.1, FIN(e) + 0.4, sem=51)
    pa(R, E2.saco_grano(), 1720, 1010, 0.48, t_cos + 0.1, FIN(e) + 0.4, sem=52)
    R.texto(t_cos, FIN(e) + 0.3, "COSECHAS", (1640, 760), px=42, d=0.4)
    pa(R, E2.columna_papiro(), 770, 1010, 0.62, t_tem - 0.1, FIN(e) + 0.4, sem=53)
    pa(R, E2.cartucho(), 1640, 620, 0.62, t_nom - 0.1, FIN(e) + 0.4, sem=54, extra=[(0.05, "bling", 0.35)])
    R.texto(t_nom + 0.2, FIN(e) + 0.3, "NOMBRES ETERNOS", (1640, 430), px=40, d=0.5)


# ------------------------------------------------------------------ PIRÁMIDES
def _piramides(R):
    e = "piramides"
    i0 = INI(e)
    t_rei, t_eda, t_pir = T(e, "reino"), T(e, "edad"), T(e, "piramides", frase=0)
    t_sab, t_imh, t_pir2, t_esc, t_saq, t_esc2, t_cie = (T(e, "sabio"), T(e, "imhotep"), T(e, "piramide", frase=1), T(e, "escalonada"), T(e, "saqqara"),
                                                         T(e, "escalera"), T(e, "cielo"))
    t_sig, t_guiza, t_miles, t_lev, t_gran, t_keo = T(e, "siglos"), T(e, "guiza"), T(e, "miles"), T(e, "levantan"), T(e, "gran", frase=2), T(e, "keops")
    t_lado, t_esf, t_vig, t_leo, t_ros = T(e, "lado"), T(e, "esfinge"), T(e, "vigila"), T(e, "leon"), T(e, "rostro")
    t_dur, t_cuat, t_alta, t_hum = T(e, "durante"), T(e, "cuatro"), T(e, "alta"), T(e, "humano")
    # cámara
    R.camara(i0 - 0.2, 31.2, 29.62, 4.2)
    R.camara(t_pir + 0.6, 31.2, 29.66, 4.4)
    R.camara(t_imh, 31.22, 29.86, 8.8)
    R.camara(t_cie + 0.4, 31.2, 29.9, 9.2)
    R.camara(t_guiza, 31.17, 29.975, 10.0)
    R.camara(t_keo + 0.8, 31.17, 29.972, 10.4)
    R.camara(t_ros + 0.4, 31.16, 29.97, 9.6)
    R.camara(FIN(e) + 0.6, 31.05, 29.85, 6.5)
    # años y sello
    R.anio(t_rei, -2686)
    R.anio(t_imh, -2650)
    R.anio(t_sig + 0.4, -2560)
    R.sello(t_rei + 0.1, "piramide", "REINO ANTIGUO", color=(206, 146, 44))
    titulo(R, t_eda - 0.1, t_sab - 0.2, "LA EDAD DE ORO", px=82)
    # las pirámides de la necrópolis de Menfis (de sur a norte)
    for k, (g, sc) in enumerate((((31.157, 29.388), 0.17), ((31.206, 29.79), 0.2), ((31.21, 29.81), 0.2), ((31.216, 29.871), 0.18),
                                 ((31.203, 29.896), 0.15), ((31.134, 29.979), 0.24), ((31.128, 29.972), 0.2))):
        ga(R, E2.gran_piramide(False, 7), g, t_rei + 0.5 + 0.22 * k, t_sab, s=sc, off=(0, 6), sem=60 + k, zs=0.4, z=1, entra="sube", d_in=0.4, dy=200)
    R.snd(t_rei + 0.5, "crece", 0.4, dur=1.4)
    andar(R, lambda p: E3.barca_papiro(p), tramo(nilo(), (31.25, 29.2), (31.24, 30.05), 12), i0, 5.0, t1=t_sab, s=0.3, sem=67, zs=0.3, z=2, fps=4)
    # Imhotep y la pirámide escalonada de Saqqara
    pa(R, E1.imhotep(0, "feliz"), 330, 1010, 1.15, t_sab - 0.1, t_sig + 0.1, sem=70, extra=[(0.05, "pluck", 0.4)])
    R.texto(t_imh, t_sig, "IMHOTEP", (330, 630), px=54, d=0.5)
    ga(R, E2.piramide_escalonada(), CI["saqqara"], t_pir2 - 0.2, t_sig + 0.1, s=0.55, off=(60, 40), sem=71, zs=0.5, z=1, entra="pluma", d_in=1.3,
       extra=[(0.05, "crece", 0.5, {"dur": 1.2})])
    ciudad(R, t_saq - 0.1, t_sig + 0.1, "saqqara", "SAQQARA", "izq", 46)
    pa(R, A.sol_brillo(), 1560, 330, 0.85, t_esc2 - 0.2, t_sig + 0.1, sem=72, z=1, entra="sube", dy=300, extra=[(0.1, "brillo", 0.4)])

    def escalera(h, cam, t, fs, te):
        if not (t_esc2 - 0.1 <= t <= t_sig + 0.1):
            return
        x0, y0 = cam.pant(*CI["saqqara"])
        x0, y0 = x0 + 60 * 1.6, y0 - 170
        u = e_inout(prog(t, t_esc2 - 0.1, t_esc2 + 0.9)) * (1 - prog(t, t_sig - 0.2, t_sig + 0.1))
        P = np.array([(x0 + (1490 - x0) * k / 6, y0 + (380 - y0) * k / 6 - 40 * math.sin(k / 6 * math.pi)) for k in range(7)])
        linea_punteada(h, P, t, 26, 18, 5.0, 77, fs, u)
    R.frente.append(R._acot(escalera, t_esc2 - 0.1))
    R.texto(t_esc2 + 0.2, t_sig, "ESCALERA AL CIELO", (1560, 520), px=44, d=0.5)
    # Guiza: miles de trabajadores arrastran los bloques
    ciudad(R, t_guiza - 0.1, t_gran - 0.3, "guiza", "GUIZA", "abajo", 48)
    titulo(R, t_miles, t_keo - 0.2, "MILES DE TRABAJADORES", px=70)
    R.texto(t_sig + 0.1, t_miles - 0.2, "SIGLOS DESPUÉS...", (960, 196), px=70, d=0.6)
    xa = lambda t: lerp(-420, 720, e_inout(prog(t, t_sig + 0.2, t_keo + 0.4)))   # noqa: E731
    pa(R, E2.trineo(), xa, lambda t: 1010, 0.8, t_sig + 0.1, t_lado, sem=73, entra="fija", extra=[(0.1, "arena", 0.35, {"dur": 3.0})])
    for k in range(4):
        pa(R, lambda t, k=k: E1.obrero((int(t * 6) + k) % 4, "enojo"), (lambda t, k=k: xa(t) + 300 + 92 * k), lambda t, k=k: 1012 - 6 * (k % 2), 0.55,
           t_sig + 0.1, t_lado, sem=74 + k, entra="fija", z=3)
    R.snd(t_miles + 0.1, "pasos", 0.35, dur=2.2)
    ga(R, E2.gran_piramide(True), CI["guiza"], t_gran - 0.2, FIN(e, 3) + 0.2, s=0.62, off=(-330, 40), sem=78, zs=0.5, z=1, entra="pluma", d_in=1.4,
       extra=[(0.05, "crece", 0.5, {"dur": 1.2})])
    lugar(R, t_gran + 0.4, t_lado + 0.2, "GRAN PIRÁMIDE", CI["guiza"], off=(-330, 110), px=46)
    pa(R, E1.keops(0, "serio"), 1630, 1010, 1.12, t_keo - 0.15, t_lado + 0.1, sem=79, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_keo + 0.1, t_lado, "KEOPS", (1630, 640), px=54, d=0.4)
    # la Esfinge: cuerpo de león + rostro de rey
    ga(R, E2.esfinge(), CI["guiza"], t_esf - 0.2, FIN(e, 3) + 0.2, s=0.36, off=(-70, 110), sem=80, zs=0.5, z=2, entra="sube", dy=300,
       extra=[(0.05, "rugido", 0.3)])
    lugar(R, t_esf + 0.2, t_leo - 0.2, "GRAN ESFINGE", CI["guiza"], off=(-70, 170), px=44)
    pa(R, E2.leon(0), 330, 1000, 0.62, t_leo - 0.1, FIN(e, 3) + 0.1, sem=81, extra=[(0.05, "rugido", 0.35)])
    R.texto(t_leo + 0.1, FIN(e, 3), "+", (600, 900), px=96, d=0.2)
    pa(R, E1.faraon(0, "nemes", "serio", acc_d=None, acc_i=None, brazos=(8, 8)), 800, 1010, 0.82, t_ros - 0.1, FIN(e, 3) + 0.1, sem=82)
    R.texto(t_ros + 0.2, FIN(e, 3), "=", (1010, 900), px=96, d=0.2)
    pa(R, E2.esfinge(), 1380, 1000, 0.72, t_ros + 0.3, FIN(e, 3) + 0.1, sem=83, extra=[(0.05, "ding", 0.4)])
    # el récord: 146 m durante 3.800 años
    pa(R, E2.gran_piramide(True), 1150, 1030, 1.25, t_dur - 0.1, FIN(e) + 0.5, sem=84, entra="sube", dy=500, extra=[(0.05, "crece", 0.4)])
    pa(R, E2.regla(300), 860, 1030, 0.98, t_cuat, FIN(e) + 0.5, sem=85, entra="sube", dy=400)
    R.texto(t_cuat + 0.3, FIN(e) + 0.4, "146 m", (860, 690), px=56, d=0.4)
    R.contador(t_cuat - 0.2, t_cuat + 0.8, 0, 3800, (960, 196), px=84, formato="{:,} AÑOS", hasta_t=FIN(e) + 0.4)
    R.snd(t_cuat - 0.2, "reloj_rapido", 0.35, dur=1.0)
    pa(R, A.cetro_corona(), 1150, 680, 0.55, t_alta - 0.1, FIN(e) + 0.5, sem=86, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_alta + 0.1, FIN(e) + 0.4, "LA MÁS ALTA", (1520, 520), px=48, d=0.4)
    pa(R, E1.campesino(0, "asombro", None), 1440, 1030, 0.2, t_hum - 0.2, FIN(e) + 0.5, sem=87)
    R.texto(t_hum, FIN(e) + 0.4, "una persona", (1440, 940), px=30, d=0.4)


# ------------------------------------------------------------------ PRIMER PERIODO INTERMEDIO, REINO MEDIO E HICSOS
def _intermedio(R):
    e = "intermedio1"
    i0 = INI(e)
    t_seq, t_dis, t_gob, t_hun, t_caos = T(e, "sequias"), T(e, "disputas"), T(e, "gobernadores"), T(e, "hunden"), T(e, "caos")
    t_pri, t_teb, t_reu, t_rei = T(e, "principes"), T(e, "tebas"), T(e, "reunificar"), T(e, "reino")
    t_flo, t_lit, t_art, t_tem, t_kar = T(e, "florecen"), T(e, "literatura"), T(e, "arte"), T(e, "templos"), T(e, "karnak")
    t_sin, t_asia, t_inv, t_car, t_hic, t_con, t_del = (T(e, "sin"), T(e, "asia"), T(e, "invasores"), T(e, "carros"), T(e, "hicsos"), T(e, "conquistan"),
                                                        T(e, "delta"))
    # cámara
    R.camara(i0 - 0.2, 31.25, 27.85, 2.45)
    R.camara(t_caos + 0.3, 31.4, 27.5, 2.3)
    R.camara(t_reu + 0.6, 31.7, 26.9, 2.5)
    R.camara(t_flo + 0.2, 32.6, 25.73, 6.8)
    R.camara(t_kar + 0.5, 32.66, 25.72, 8.0)
    R.camara(t_asia + 0.2, 33.5, 31.2, 2.6)
    R.camara(FIN(e) + 0.5, 33.1, 31.0, 2.8)
    # años
    R.anio(i0, -2181)
    R.anio(t_teb, -2055)
    R.anio(t_flo, -1950)
    R.anio(t_asia, -1650)
    # sequías y caos: el reino se rompe en nomos
    pa(R, E2.sequia(), 1560, 1010, 0.8, t_seq - 0.1, t_pri + 0.2, sem=90, extra=[(0.05, "viento", 0.4, {"dur": 2.0})])
    R.texto(t_seq + 0.2, t_pri, "SEQUÍAS", (1560, 700), px=52, d=0.4)
    R.terreno(i0 - 0.6, "reino_antiguo", COL["egipto"], 0.4)
    R.romper("nomos", t_dis, t_dis + 0.8, t_reu - 0.2, t_reu + 0.9, capa=0, gap=16.0, deriva=30.0)
    R.snd(t_dis, "crujido", 0.5, dur=0.9)
    for k, (g, dx) in enumerate((((30.8, 28.3), -150), ((31.65, 27.15), 150), ((32.3, 26.0), -150))):
        ga(R, E1.nomarca(k % 2, "enojo", ((200, 140, 90), (150, 110, 170), (110, 150, 130))[k]), g, t_gob - 0.1 + 0.15 * k, t_pri, s=0.45, off=(dx, 20),
           sem=91 + k, zs=0.4, z=2)
    ga(R, A.espadas(), (31.25, 27.6), t_hun - 0.2, t_pri, s=0.45, off=(0, 0), sem=94, zs=0.3, z=3, extra=[(0.05, "espada", 0.5)])
    titulo(R, t_caos - 0.2, t_pri - 0.1, "¡CAOS!", px=100)
    pa(R, A.estallido(14, 50, 150), 960, 560, 1.1, t_caos - 0.1, t_caos + 0.5, entra="fija", sale="cortar", sem=95, z=1,
       extra=[(0.0, "explosion", 0.35)])
    # los príncipes de Tebas reunifican: Reino Medio
    ciudad(R, t_teb - 0.1, t_tem - 0.3, "tebas", "TEBAS", "der", 50)
    ga(R, E1.mentuhotep(0, "feliz"), CI["tebas"], t_pri, t_reu, s=0.48, off=(-90, 10), sem=96, zs=0.4, z=2, extra=[(0.05, "fanfarria", 0.3)])
    andar(R, lambda p: E1.mentuhotep(p % 2, "feliz"), tramo(nilo(), CI["tebas"], CI["menfis"], 20), t_reu, 2.6, t1=t_flo - 0.1, s=0.48, sem=97, zs=0.4, z=2,
          fps=5, off=(-60, 0))
    R.terreno(t_reu, "reino_medio", COL["reino_medio"], 1.4)
    R.sello(t_rei, "anj", "REINO MEDIO", color=(60, 140, 120))
    # literatura, arte y Karnak
    pa(R, E2.papiro_escrito(), 380, 980, 0.85, t_lit - 0.1, FIN(e, 2) + 0.2, sem=98, extra=[(0.05, "papel", 0.45)])
    R.texto(t_lit + 0.1, FIN(e, 2), "LITERATURA", (380, 720), px=46, d=0.4)
    pa(R, lambda t: E1.pintor(int(t * 2) % 2, "feliz"), 760, 1010, 0.9, t_art - 0.1, FIN(e, 2) + 0.2, sem=99, extra=[(0.05, "pincel", 0.4, {"dur": 0.8})])
    pa(R, E3.loto(), 960, 1010, 0.5, t_art + 0.2, FIN(e, 2) + 0.2, sem=100)
    R.texto(t_art + 0.1, FIN(e, 2), "ARTE", (900, 640), px=46, d=0.3)
    ga(R, E2.templo_karnak(), CI["karnak"], t_tem - 0.2, FIN(e, 2) + 0.3, s=0.5, off=(80, 40), sem=101, zs=0.5, z=1, entra="pluma", d_in=1.3,
       extra=[(0.05, "crece", 0.5, {"dur": 1.2})])
    ga(R, E2.columna_papiro(), CI["karnak"], t_tem + 0.4, FIN(e, 2) + 0.3, s=0.32, off=(-200, 50), sem=102, zs=0.5, z=1, entra="sube", dy=300)
    ga(R, E2.columna_papiro(), CI["karnak"], t_tem + 0.55, FIN(e, 2) + 0.3, s=0.32, off=(-280, 56), sem=103, zs=0.5, z=1, entra="sube", dy=300)
    ga(R, E2.obelisco(), CI["karnak"], t_kar - 0.2, FIN(e, 2) + 0.3, s=0.32, off=(330, 50), sem=104, zs=0.5, z=1, entra="sube", dy=300)
    lugar(R, t_kar, FIN(e, 2) + 0.2, "KARNAK", CI["karnak"], off=(80, 120), px=54)
    # los hicsos llegan de Asia con sus carros
    R.ruta(M.RUTAS["hicsos"], t_asia - 0.2, 1.6, ancho=5.0, t1=FIN(e) + 0.3, flecha=True)
    lugar(R, t_asia, t_hic, "DESDE ASIA", (35.4, 32.2), off=(0, 0), px=50)
    for k in range(2):
        andar(R, lambda p, k=k: E3.carro(p, "hicso", (170, 120, 160)), M.RUTAS["hicsos"], t_car - 0.4 + 0.25 * k, 2.6, t1=FIN(e) + 0.3, s=0.3, sem=105 + k,
              zs=0.4, z=2, fps=9, off=formacion(k, 2, 170))
    R.snd(t_car - 0.3, "galope", 0.55, dur=2.6)
    lugar(R, t_hic, FIN(e) + 0.2, "HICSOS", (35.0, 32.4), off=(0, 0), px=60)
    R.terreno(t_con - 0.1, "hicsos", COL["hicsos"], 1.0, capa=1)
    R.terreno(t_con - 0.1, "tebas_sur", COL["reino_medio"], 1.0)
    ciudad(R, t_del - 0.2, FIN(e) + 0.4, "avaris", "ÁVARIS", "abajo", 44)
    ga(R, E1.hicso(0, "enojo"), CI["avaris"], t_del, FIN(e) + 0.4, s=0.42, off=(-130, 20), sem=107, zs=0.4, z=2)
