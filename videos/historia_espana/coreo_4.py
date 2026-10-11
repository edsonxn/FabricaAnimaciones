# -*- coding: utf-8 -*-
"""Coreografía (4/4): el siglo XIX (Napoleón, Goya, la Pepa, las independencias, el siglo del caos, 1898), el siglo XX (República,
Guerra Civil, Guernica, dictadura, turismo, Transición, Constitución, Europa, Barcelona 92), el cierre y los cambios de escena.
Capas "eu": 0 = España, 10 = Francia, 12 = zona sublevada / dictadura, 13 = Europa. Capas "am": 0 = imperio -> repúblicas, 1 = España, 2 = EE. UU."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_es1 as E1
import obj_es2 as E2
import obj_es3 as E3
import obj_es4 as E4
from core import FIN, INI, T, kf
from coreo_util import andar, CI, ciudad, COL, formacion, ga, lugar, mece, pa, titulo
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from trans import SFX, Transicion

PAISES = M.CELDAS_PAISES["independencias"]
COL_PAIS = {"Mexico": (110, 170, 110), "Guatemala": (120, 180, 210), "Honduras": (90, 140, 200), "El Salvador": (110, 150, 210), "Nicaragua": (130, 170, 220),
            "Costa Rica": (200, 120, 130), "Panama": (220, 150, 120), "Colombia": (236, 200, 90), "Venezuela": (226, 170, 80), "Ecuador": (200, 190, 100),
            "Peru": (210, 110, 100), "Bolivia": (170, 196, 110), "Chile": (190, 120, 160), "Argentina": (140, 190, 230), "Paraguay": (180, 140, 190),
            "Uruguay": (150, 200, 220), "Dominican Rep.": (150, 140, 200), "Cuba": COL["imperio"], "Puerto Rico": COL["imperio"],
            "Philippines": COL["imperio"], "Spain": COL["imperio"]}
POS_BANDERA = {"Mexico": (-102.0, 24.0), "Guatemala": (-90.4, 15.6), "Honduras": (-86.8, 14.9), "El Salvador": (-89.0, 13.7), "Nicaragua": (-85.1, 12.7),
               "Costa Rica": (-84.1, 9.9), "Panama": (-80.2, 8.5), "Colombia": (-73.5, 4.0), "Venezuela": (-66.0, 7.5), "Ecuador": (-78.4, -1.4),
               "Peru": (-75.2, -9.5), "Bolivia": (-64.8, -17.0), "Chile": (-70.6, -30.0), "Argentina": (-64.0, -35.5), "Paraguay": (-58.3, -23.3),
               "Uruguay": (-56.0, -32.8), "Dominican Rep.": (-70.5, 18.9)}


def cortes(R):
    pass


def construir(R):
    _ochocientos(R)
    _siglo_xx(R)
    _cierre(R)
    _transiciones(R)


# ------------------------------------------------------------------ SIGLO XIX
def _ochocientos(R):
    e = "ochocientos"
    i0 = INI(e)
    t_1808, t_nap, t_inv, t_sienta, t_herm, t_trono = T(e, "mil"), T(e, "napoleon"), T(e, "invade"), T(e, "sienta"), T(e, "hermano"), T(e, "trono")
    t_pueblo, t_levanta, t_goya, t_pinta, t_mundo, t_palabra, t_guerr = (T(e, "pueblo"), T(e, "levanta"), T(e, "goya"), T(e, "pinta"), T(e, "mundo"),
                                                                         T(e, "palabra"), T(e, "guerrilla"))
    t_cadiz, t_firma, t_const, t_pepa = T(e, "cadiz"), T(e, "firma"), T(e, "constitucion"), T(e, "pepa")
    t_otro, t_mar, t_quince, t_amer, t_indep, t_nacen, t_conoces = (T(e, "otro"), T(e, "mar", frase=3), T(e, "quince"), T(e, "america"), T(e, "independiza"),
                                                                    T(e, "nacen"), T(e, "conoces"))
    t_resto, t_caos, t_guerras, t_reina, t_exilio, t_rey, t_renun, t_repub, t_once = (T(e, "resto"), T(e, "caos"), T(e, "guerras"), T(e, "reina"),
                                                                                      T(e, "exilio"), T(e, "rey"), T(e, "renuncia"), T(e, "republica"),
                                                                                      T(e, "once"))
    t_1898, t_pierde, t_cuba, t_pr, t_filip, t_guerra, t_eeuu = (T(e, "mil", frase=5), T(e, "pierde"), T(e, "cuba"), T(e, "puerto"), T(e, "filipinas"),
                                                                 T(e, "guerra", frase=5), T(e, "estados"))
    t_f4 = INI(e, 4)
    t_f5 = INI(e, 5)
    # ---- territorio (Europa)
    R.terreno(i0 - 0.3, "espana", COL["espana"], 0.8)
    R.terreno(t_inv - 0.1, "ocupada_1810", COL["francia"], 2.2, capa=10)
    R.terreno(t_otro, "francia", COL["francia"], 0.8, capa=10)
    R.terreno(t_resto + 0.2, None, COL["francia"], 1.0, capa=10)
    R.sello(t_const + 0.1, "libro", "CONSTITUCIÓN DE 1812", color=(160, 50, 50))
    # ---- territorio (América): el imperio de 1810 se rompe por sus fronteras reales
    R.terreno(t_otro - 0.6, "am_1810", COL["imperio"], 0.3, rej="am")
    i_cuba, i_pr, i_fil = PAISES.index("Cuba"), PAISES.index("Puerto Rico"), PAISES.index("Philippines")

    def color_pais(t, i):                       # en 1898 Cuba se independiza; Puerto Rico y Filipinas pasan a EE. UU.
        u = e_inout(prog(t, t_pierde + 0.2, t_pierde + 1.4))
        c = COL_PAIS[PAISES[i]]
        if i == i_cuba:
            return tuple(lerp(a, b, u) for a, b in zip(c, (110, 196, 170)))
        if i in (i_pr, i_fil):
            return tuple(lerp(a, b, u) for a, b in zip(c, COL["eeuu"]))
        return c
    fijas = [PAISES.index(p) for p in M.QUEDAN_1825]
    R.romper("independencias", t_indep - 0.2, t_indep + 0.9, FIN(e) + 1.0, FIN(e) + 1.01, colores=color_pais, rej="am", fijas=fijas, gap=10, deriva=26,
             nervio=0.4)
    R.snd(t_indep - 0.1, "crujido", 0.9, dur=1.0)
    R.terreno(t_f4 + 1.2, "usa", COL["eeuu"], 0.05, capa=2, rej="am")
    R.terreno(t_pierde + 0.3, "usa_1898", COL["eeuu"], 1.6, capa=2, rej="am")
    # ---- cámara
    R.camara(i0 - 0.3, -0.8, 46.4, 1.3)
    R.camara(t_nap + 0.6, -0.9, 46.1, 1.3)
    R.camara(t_sienta, -2.2, 42.5, 1.5)
    R.camara(t_trono, -3.7, 40.6, 2.4)
    R.camara(t_pueblo, -3.7, 40.4, 3.0)
    R.camara(t_guerr, -3.6, 40.2, 2.4)
    R.camara(t_cadiz - 0.2, -6.3, 36.6, 5.0)
    R.camara(t_pepa + 0.2, -6.3, 36.55, 5.3)
    R.camara(t_mar + 0.6, -55.0, 15.0, 0.3)
    R.camara(t_amer, -82.0, 12.0, 0.36)
    R.camara(t_nacen, -76.0, 2.0, 0.28)
    R.camara(t_conoces + 0.4, -75.0, 1.0, 0.28)
    R.camara(t_f4 + 0.9, -3.6, 40.0, 2.3)
    R.camara(t_rey, -3.0, 41.0, 2.1)
    R.camara(FIN(e, 4), -3.2, 40.6, 2.0)
    R.camara(t_f5 + 1.0, -74.0, 20.5, 0.7)
    R.camara(t_pr + 0.5, -73.0, 20.0, 0.72)
    R.camara(t_filip + 0.3, 124.0, 13.0, 0.75)
    R.camara(FIN(e) + 0.3, 123.0, 13.0, 0.8)
    R.rejilla(t_mar - 0.1, "am", 1.0)
    R.rejilla(t_f4 - 0.1, "eu", 0.9)
    R.rejilla(t_f5 - 0.1, "am", 1.0)
    # ---- años
    R.anio(i0, 1713)
    R.anio(t_1808 + 0.7, 1808)
    R.anio(t_const - 0.2, 1808)
    R.anio(t_const + 0.4, 1812)
    R.anio(t_quince - 0.2, 1810)
    R.anio(t_conoces, 1825)
    R.anio(t_guerras - 0.2, 1833)
    R.anio(t_reina + 0.2, 1868)
    R.anio(t_rey + 0.2, 1873)
    R.anio(t_once + 0.3, 1874)
    R.anio(t_1898 - 0.2, 1874)
    R.anio(t_1898 + 0.7, 1898)
    # ---- Napoleón y su hermano
    Pn = M.RUTAS["napoleon"]
    R.ruta(Pn, t_nap - 0.2, 2.2, ancho=5.5, t1=t_pueblo, flecha=True)
    andar(R, lambda p: E4.napoleon(p, "enojo"), Pn, t_nap - 0.2, (t_trono + 0.2) - t_nap, t1=t_pueblo, s=0.85, sem=200, z=3, fps=6, snd=("tambor", 0.4))
    for k in range(3):
        # columna a la IZQUIERDA de Napoleón y a distancia fija en pantalla: centrada en él se le encimaba (y a José, que queda a su derecha)
        # (mismo camino y reloj que él: con salidas escalonadas el retraso en la ruta deshacía la separación y se apilaban)
        R.act(lambda t, k=k: E4.soldado_frances(int(t * 6 + 201 + k) % 4), pos_geo=R.camino_pos(Pn, t_nap - 0.2, (t_trono + 0.2) - t_nap),
              off=(-220 - 185 * k, 20 - 50 * (k % 2)), s=0.62, t_in=t_inv + 0.12 * k, d_in=0.4, entra="pop", sem=201 + k,
              sfx=[(0, "pasos", 0.3)] if k == 0 else [], t_out=t_pueblo, sale="encoger", zs=0.5, z=2,
              flip=float(M.U(Pn[1][0])) < float(M.U(Pn[0][0])))
    ga(R, E4.jose_bonaparte(0, "feliz"), CI["madrid"], t_herm - 0.15, t_pueblo, s=0.62, off=(240, 40), sem=204, z=2, extra=[(0.1, "brillo", 0.4)])
    lugar(R, t_nap, t_inv + 0.3, "NAPOLEÓN", CI["paris"], off=(230, -60), px=54)
    lugar(R, t_herm, t_pueblo - 0.1, "JOSÉ BONAPARTE", CI["madrid"], off=(350, -290), px=44)
    # ---- el pueblo, Goya, la guerrilla
    for k, x in enumerate((420, 760, 1100)):
        pa(R, lambda t, k=k: E4.madrileno(int(t * 5 + k) % 2, "enojo"), x, 1010, 1.05, t_levanta - 0.2 + 0.1 * k, t_goya - 0.3, sem=205 + k, d_out=0.25,
           extra=[(0.05, "tambor", 0.3)] if k == 0 else [])
    titulo(R, t_pueblo - 0.1, t_goya - 0.2, "2 DE MAYO DE 1808", px=78)
    pa(R, E4.goya(0, "serio"), 380, 1010, 1.2, t_goya - 0.05, t_cadiz - 0.2, sem=208)      # entra cuando el madrileño de ese lado ya se fue
    pa(R, E4.cuadro_3mayo(), 1220, 900, 1.3, t_pinta - 0.2, t_mundo + 0.6, sem=209, entra="pluma", d_in=0.7, snd=("pincel", 0.5))
    R.texto(t_goya, t_mundo + 0.5, "GOYA: «EL 3 DE MAYO»", (1220, 420), px=52, d=0.5)
    # fijos en pantalla, bajo el título: el zoom hacia Cádiz sacaba a los anclados al mapa por arriba, encima del rótulo
    for k, (gx, gy) in enumerate(((600, 690), (880, 770), (1160, 690), (1440, 770))):
        pa(R, lambda t, k=k: E4.guerrillero(int(t * 4 + k) % 2, "enojo"), gx, gy, 0.8, t_palabra + 0.12 * k, t_cadiz - 0.5, sem=210 + k, z=2)
    titulo(R, t_guerr - 0.15, t_cadiz - 0.6, "«GUERRILLA»", px=104)
    # ---- Cádiz y la Pepa
    ciudad(R, t_cadiz - 0.1, t_otro - 0.3, "cadiz", "CÁDIZ", "der", 52)
    pa(R, E4.constitucion_1812(), 1060, 990, 1.15, t_firma - 0.2, t_otro, sem=214, extra=[(0.1, "papel", 0.5)])
    pa(R, E4.diputado(0, "feliz"), 450, 1010, 1.15, t_firma - 0.1, t_otro, sem=215)
    titulo(R, t_pepa - 0.1, t_otro - 0.1, "«LA PEPA» (1812)", px=84)
    # ---- independencias
    titulo(R, t_quince - 0.1, t_f4 - 0.2, "1810 – 1825", px=82, x=1420, y=330)
    pa(R, E4.libertador(0, "serio"), 300, 1010, 1.15, t_indep - 0.2, t_f4 - 0.1, sem=216, extra=[(0.1, "fanfarria", 0.45)])
    orden = ["Mexico", "Guatemala", "Dominican Rep.", "Venezuela", "Colombia", "Ecuador", "Peru", "Bolivia", "Paraguay", "Chile", "Argentina", "Uruguay"]
    for k, p in enumerate(orden):
        t0 = t_indep + 0.3 + (t_conoces - t_indep) * k / len(orden)
        ga(R, lambda t, p=p, k=k: E4.bandera_pais(p, int(t * 4 + k) % 6), POS_BANDERA[p], t0, t_f4 - 0.1, s=0.62 if p not in ("Mexico", "Argentina", "Colombia", "Peru") else 0.78,
           sem=217 + k, z=2, zs=0.3, snd=("pop", 0.3))
    # ---- un siglo de caos
    titulo(R, t_caos - 0.1, t_f5 - 0.2, "UN SIGLO DE CAOS", px=82)
    pa(R, A.espadas(), 960, 560, 0.9, t_guerras - 0.1, t_reina, sem=235, extra=[(0.05, "espada", 0.5)])
    andar(R, lambda p: E4.isabel2(p, "lloron"), [CI["madrid"], (-2.6, 41.0), (-1.3, 41.3)], t_reina - 0.2, 2.0, t1=t_rey - 0.3, s=0.62, sem=236, z=2, fps=4)
    lugar(R, t_exilio - 0.1, t_rey - 0.3, "ISABEL II", CI["madrid"], off=(-250, 20), px=46)
    andar(R, lambda p: E4.amadeo(p, "lloron"), [CI["madrid"], (0.5, 41.2), (3.8, 41.6)], t_rey - 0.2, 2.0, t1=t_repub + 0.2, s=0.62, sem=237, z=2, fps=4)
    lugar(R, t_renun - 0.1, t_repub + 0.1, "AMADEO DE SABOYA", (0.5, 41.2), off=(0, 90), px=44)
    pa(R, E4.calendario(), 1540, 960, 1.05, t_repub - 0.15, t_f5 - 0.1, sem=238, extra=[(0.1, "papel", 0.4)])
    R.contador(t_once - 0.3, t_once + 0.6, 0, 11, (1540, 560), px=72, formato="{} MESES", hasta_t=t_f5 - 0.1)
    R.snd(t_once - 0.3, "reloj_rapido", 0.4, dur=0.9)
    # ---- 1898
    andar(R, lambda p: E4.acorazado(p), [(-73.5, 25.8), (-74.6, 24.2), (-75.2, 22.6)], t_1898 - 0.3, (t_cuba + 0.2) - t_1898, t1=FIN(e) + 0.5, s=0.42,
          sem=239, z=2, zs=0.2, fps=3,
          snd=("canonazo", 0.4))
    andar(R, lambda p: E4.acorazado(p), [(129.5, 16.5), (127.4, 15.2), (125.4, 14.2)], t_filip - 0.3, 1.8, t1=FIN(e) + 0.5, s=0.42, sem=240, z=2,
          zs=0.2, fps=3, snd=None, flip=True)
    for k, (t0, geo, txt, off, t1) in enumerate(((t_cuba, (-80.5, 21.4), "CUBA", (0, -80), t_filip - 0.3), (t_pr, (-66.4, 18.2), "PUERTO RICO", (0, 70), t_filip - 0.3),
                                                 (t_filip, (117.6, 12.2), "FILIPINAS", (0, 0), FIN(e) + 0.4))):
        lugar(R, t0 - 0.1, t1, txt, geo, off=off, px=50)
        R.snd(t0, "golpe_suave", 0.45)
    titulo(R, t_guerra - 0.1, FIN(e) + 0.4, "1898: «EL DESASTRE»", px=82)


# ------------------------------------------------------------------ SIGLO XX
def _siglo_xx(R):
    e = "siglo_xx"
    i0 = INI(e)
    t_1931, t_llega, t_seg, t_cinco, t_golpe, t_guerra = (T(e, "mil"), T(e, "llega"), T(e, "segunda"), T(e, "cinco"), T(e, "golpe"),
                                                          T(e, "guerra", frase=0))
    t_tres, t_horror, t_muertos, t_pic, t_bomb, t_guern = T(e, "tres"), T(e, "horror"), T(e, "muertos"), T(e, "picasso"), T(e, "bombardeo"), T(e, "guernica")
    t_gana, t_franco, t_dict, t_36 = T(e, "gana"), T(e, "franco", frase=2), T(e, "dictador"), T(e, "treinta y seis")
    t_hambre, t_cens, t_exil, t_sesenta, t_tur, t_din = T(e, "hambre"), T(e, "censura"), T(e, "exilio"), T(e, "sesenta"), T(e, "turismo"), T(e, "dinero")
    t_muere, t_1975, t_jc, t_abre, t_dem = T(e, "franco", frase=4), T(e, "mil", frase=4), T(e, "juan"), T(e, "abre"), T(e, "democracia")
    t_1978, t_vota, t_cons = T(e, "mil", frase=5), T(e, "vota"), T(e, "constitucion")
    t_sobre, t_golpe2, t_entra, t_europa, t_92, t_mira, t_bcn = (T(e, "sobrevive"), T(e, "golpe", frase=6), T(e, "entra"), T(e, "europa"), T(e, "noventa"),
                                                                 T(e, "mira"), T(e, "barcelona"))
    # ---- territorio (vuelta a la rejilla de Europa bajo el barrido del cambio de escena)
    R.rejilla((FIN("ochocientos") + i0) / 2, "eu", 0.0)
    R.terreno(i0 - 0.2, "espana", COL["espana"], 0.4)
    R.terreno(t_seg - 0.2, "espana", COL["republica"], 1.0)
    R.terreno(t_golpe, "rep36", COL["republica"], 1.4)
    R.terreno(t_golpe, "nac36", COL["nacional"], 1.4, capa=12)
    R.terreno(t_tres - 0.1, "rep38", COL["republica"], 2.4)
    R.terreno(t_tres - 0.1, "nac38", COL["nacional"], 2.4, capa=12)
    R.terreno(t_gana - 0.2, None, COL["republica"], 1.2)
    R.terreno(t_gana - 0.2, "espana", COL["nacional"], 1.2, capa=12)
    R.terreno(t_dict, "espana", COL["franco"], 1.2, capa=12)
    R.terreno(t_sesenta, "espana", (176, 150, 120), 1.4, capa=12)
    R.terreno(t_dem - 0.2, "espana", COL["democracia"], 1.4, capa=12)
    R.terreno(t_europa - 0.3, "ue", (90, 120, 190), 1.4, capa=13)
    R.terreno(t_92 - 0.2, None, (90, 120, 190), 0.8, capa=13)
    R.sello(t_seg + 0.1, "gorro", "SEGUNDA REPÚBLICA", color=(120, 70, 140))
    R.sello(t_cons + 0.1, "urna", "DEMOCRACIA", color=(190, 60, 50))
    # ---- cámara
    R.camara(i0 - 0.3, -3.4, 40.2, 2.2)
    R.camara(t_golpe, -3.6, 40.0, 2.3)
    R.camara(t_horror, -3.2, 40.6, 2.3)
    R.camara(t_pic - 0.2, -2.7, 43.1, 4.6)
    R.camara(t_guern + 0.3, -2.68, 43.25, 5.2)
    R.camara(t_gana - 0.3, -2.7, 43.2, 5.3)
    R.camara(t_gana + 0.5, -3.6, 40.1, 2.3)
    R.camara(t_sesenta, -2.0, 39.0, 2.5)
    R.camara(t_din + 0.2, -1.6, 38.8, 2.6)
    R.camara(t_muere, -3.6, 40.0, 2.3)
    R.camara(t_sobre, -3.6, 40.0, 2.25)
    R.camara(t_entra + 0.2, 1.0, 45.4, 1.05)
    R.camara(t_europa + 0.6, 1.5, 45.8, 1.0)
    R.camara(t_92, 2.17, 41.5, 3.0)
    R.camara(t_bcn + 0.3, 2.17, 41.42, 4.6)
    R.camara(FIN(e) + 0.3, 2.17, 41.4, 4.9)
    # ---- años
    R.anio(i0, 1898)
    R.anio(t_1931 + 0.7, 1931)
    R.anio(t_cinco, 1931)
    R.anio(t_golpe + 0.3, 1936)
    R.anio(t_bomb - 0.2, 1936)
    R.anio(t_bomb + 0.2, 1937)
    R.anio(t_gana - 0.2, 1937)
    R.anio(t_gana + 0.6, 1939)
    R.anio(t_hambre, 1939)
    R.anio(t_hambre + 0.8, 1945)
    R.anio(t_sesenta - 0.1, 1945)
    R.anio(t_sesenta + 0.6, 1960)
    R.anio(t_muere, 1960)
    R.anio(t_1975 + 0.8, 1975)
    R.anio(t_1978 - 0.2, 1975)
    R.anio(t_1978 + 0.8, 1978)
    R.anio(t_golpe2, 1981)
    R.anio(t_europa, 1981)
    R.anio(t_europa + 0.4, 1986)
    R.anio(t_92 - 0.1, 1986)
    R.anio(t_92 + 0.5, 1992)
    # ---- la República
    pa(R, lambda t: E4.bandera_republica(int(t * 4) % 6), 1240, 1000, 1.2, t_llega - 0.1, t_golpe - 0.1, sem=250, extra=[(0.1, "fanfarria", 0.4)])
    for k, (x, m) in enumerate(((330, False), (620, True), (910, False))):
        pa(R, lambda t, k=k, m=m: E4.ciudadano_1931(int(t * 5 + k) % 2, "feliz", m), x, 1010, 1.0, t_seg - 0.1 + 0.12 * k, t_golpe - 0.1, sem=251 + k)
    # ---- la Guerra Civil
    titulo(R, t_guerra - 0.15, t_pic - 0.3, "GUERRA CIVIL (1936-1939)", px=76)
    pa(R, lambda t: E4.miliciano(int(t * 3) % 2, "enojo"), 1460, 1000, 1.15, t_golpe + 0.2, t_pic - 0.2, sem=254, flip=True, extra=[(0.1, "canonazo", 0.4)])
    pa(R, lambda t: E4.soldado_nacional(int(t * 3 + 1) % 2, "enojo"), 440, 1000, 1.15, t_golpe + 0.4, t_pic - 0.2, sem=255)
    lugar(R, t_golpe + 0.8, t_pic - 0.7, "REPUBLICANOS", (-1.6, 39.4), off=(0, 0), px=46)
    lugar(R, t_golpe + 1.0, t_pic - 0.7, "SUBLEVADOS", (-5.6, 41.6), off=(0, 0), px=46)
    # ---- Guernica
    ciudad(R, t_bomb - 0.1, t_gana - 0.4, "guernica", "GUERNICA, 1937", "abajo", 48)
    ga(R, lambda t: E4.pueblo_llamas(int(t * 6) % 6), CI["guernica"], t_bomb - 0.2, t_gana - 0.4, s=0.5, off=(-60, -20), sem=256, z=1, snd=("fuego", 0.4))
    R.act(lambda t: E4.bombardero(round(t * 3.0, 1)), pos=lambda t: (lerp(2200, -300, prog(t, t_bomb - 0.6, t_gana)), 260 + 20 * math.sin(t * 2), 0.8),
          t_in=t_bomb - 0.6, d_in=0.1, entra="fija", sem=257, sfx=[(0, "zoom_whoosh", 0.4)], t_out=t_gana, sale="cortar", z=3, flip=True)
    for k in range(3):
        tb = t_bomb - 0.1 + 0.25 * k
        R.act(E4.bomba(), pos=lambda t, tb=tb, k=k: (lerp(2200, -300, prog(tb, t_bomb - 0.6, t_gana)) - 40, 300 + 900 * e_in(prog(t, tb, tb + 0.8)), 0.8),
              t_in=tb, d_in=0.05, entra="fija", sem=258 + k, sfx=[(0.75, "explosion", 0.35)], t_out=tb + 0.8, sale="cortar", z=3)
    pa(R, E4.cuadro_gris(), 1450, 920, 1.05, t_pic - 0.2, t_gana - 0.4, sem=261, entra="pluma", d_in=0.7, snd=("pincel", 0.5))
    R.texto(t_pic, t_gana - 0.5, "PICASSO: «GUERNICA»", (1450, 1030), px=54, d=0.5)
    # ---- la dictadura
    pa(R, E4.general(0, "serio"), 470, 1010, 1.25, t_franco - 0.15, t_jc - 0.3, sem=262, sale="baja", d_out=0.6, extra=[(0.1, "tambor", 0.5)])
    pa(R, lambda t: C.vela(round(0.8 + 0.2 * math.sin(t * 9), 2)), 760, 1000, 1.0, t_muere + 0.1, t_jc - 0.2, sem=286, extra=[(0.1, "campana", 0.4)])
    titulo(R, t_muere, t_dem - 0.2, "20 DE NOVIEMBRE DE 1975", px=70)
    titulo(R, t_dict - 0.1, t_hambre - 0.2, "DICTADURA", px=96)
    R.contador(t_36 - 0.4, t_36 + 0.8, 0, 36, (960, 330), px=78, formato="{} AÑOS", hasta_t=t_hambre - 0.1)
    R.snd(t_36 - 0.4, "reloj_rapido", 0.4, dur=1.2)
    pa(R, E4.cartilla(), 1000, 980, 1.05, t_hambre - 0.15, t_sesenta - 0.2, sem=263)
    R.texto(t_hambre, t_sesenta - 0.3, "HAMBRE", (1000, 640), px=60, d=0.3)
    R.texto(t_cens - 0.05, t_sesenta - 0.3, "CENSURADO", (1430, 300), px=84, d=0.25)
    R.snd(t_cens, "sello", 0.7)
    for k in range(3):
        andar(R, lambda p, k=k: E2.exiliado(p, k == 1), [(-3.7, 40.4), (-3.0, 41.3), (-2.0, 42.2)], t_exil - 0.2 + 0.15 * k, 2.6,
              t1=t_sesenta, s=0.48, sem=264 + k, z=2, fps=4, snd=None, ease=lambda u: u, off=formacion(k, 3, 110))
    R.texto(t_exil, t_sesenta - 0.2, "EXILIO", (560, 520), px=50, d=0.3)      # fuera de la ruta de los exiliados (subía hasta Cataluña)
    # ---- los sesenta: turismo
    ga(R, E4.sombrilla(), CI["benidorm"], t_tur - 0.2, t_muere, s=0.48, off=(80, 30), sem=267, z=1)
    for k, (dx, m) in enumerate(((-130, False), (200, True))):
        ga(R, lambda t, k=k, m=m: E4.turista(int(t * 3 + k) % 2, m), CI["benidorm"], t_tur + 0.1 * k, t_muere, s=0.5, off=(dx, 50), sem=268 + k, z=2)
    lugar(R, t_tur, t_muere - 0.2, "BENIDORM", CI["benidorm"], off=(0, 110), px=40)
    R.act(lambda t: E4.seat600(round(t * 2.0, 1)), pos=lambda t: (lerp(2150, 1250, e_out(prog(t, t_din - 0.4, t_muere))), 1010, 0.9), t_in=t_din - 0.4, d_in=0.1,
          entra="fija", sem=270, sfx=[(0, "bocinazo", 0.4)], t_out=t_muere + 0.1, sale="encoger", z=3, flip=True)
    titulo(R, t_sesenta - 0.1, t_muere - 0.2, "LOS AÑOS SESENTA", px=76)
    # ---- Transición
    pa(R, E4.juan_carlos(0, "feliz"), 1450, 1010, 1.2, t_jc - 0.15, t_1978, sem=271, extra=[(0.1, "brillo", 0.5)])
    R.texto(t_jc, t_1978 - 0.1, "JUAN CARLOS I", (1450, 560), px=58, d=0.5)
    titulo(R, t_dem - 0.1, t_1978 - 0.1, "LA TRANSICIÓN", px=84)
    # ---- Constitución de 1978
    pa(R, E4.urna(), 900, 1000, 1.1, t_1978 - 0.1, t_sobre, sem=272)
    for k, (x0, x, m, c) in enumerate(((-150, 300, False, (200, 120, 80)), (-300, 560, True, (90, 140, 190)), (2100, 1430, False, (120, 160, 100)))):
        R.act(lambda t, k=k, m=m, c=c: E4.votante(int(t * 4 + k) % 2, "feliz", m, c),
              pos=lambda t, x0=x0, x=x: (lerp(x0, x, e_out(prog(t, t_1978, t_vota + 0.2))), 1010, 1.0), t_in=t_1978, d_in=0.1, entra="fija", sem=273 + k,
              sfx=[(0, "pasos", 0.3)] if k == 0 else [], t_out=t_sobre, sale="encoger", z=2, flip=x0 > 1000)
    pa(R, E4.constitucion_1978(), 1170, 990, 0.85, t_cons - 0.2, t_sobre, sem=276)
    titulo(R, t_1978 - 0.1, t_sobre - 0.1, "REFERÉNDUM: CONSTITUCIÓN DE 1978", px=66)
    # ---- golpe fallido, Europa, Barcelona 92
    pa(R, E4.tricornio_tachado(), 960, 760, 1.0, t_golpe2 - 0.15, t_entra, sem=277, extra=[(0.3, "error", 0.4)])
    R.texto(t_golpe2, t_entra - 0.1, "23-F (1981): FRACASA", (960, 330), px=64, d=0.5)
    ga(R, E4.estrellas_europa(), (8.0, 50.6), t_europa - 0.2, t_92 - 0.1, s=0.42, sem=278, z=2, zs=0.3)
    titulo(R, t_europa - 0.1, t_92 - 0.2, "1986: ENTRA EN EUROPA", px=72)
    ga(R, E4.aros_olimpicos(), CI["barcelona"], t_mira - 0.2, FIN(e) + 0.5, s=0.5, off=(-330, -150), sem=279, z=2, snd=("fanfarria", 0.5))
    ga(R, E4.sagrada_familia(), CI["barcelona"], t_bcn - 0.2, FIN(e) + 0.5, s=0.5, off=(340, 70), sem=280, z=2, entra="pluma", d_in=0.7, snd=("crece", 0.4))
    for k, (x, y) in enumerate(((560, 300), (1380, 260), (960, 200))):
        pa(R, lambda t, k=k: Bb.chispas(14, 120 + 40 * math.sin(t * 6 + k)), x, y, 0.8, t_bcn + 0.15 * k, FIN(e) + 0.5, entra="pop", sem=281 + k, z=1,
           snd=("explosion", 0.25))
    ciudad(R, t_bcn - 0.1, FIN(e) + 0.4, "barcelona", "BARCELONA 92", "abajo", 54)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_hoy, t_49, t_hab, t_recibe, t_90, t_tur = T(e, "hoy"), T(e, "cuarenta"), T(e, "habitantes"), T(e, "recibe"), T(e, "noventa"), T(e, "turistas")
    t_ib, t_rom, t_god, t_ara, t_jud, t_cri, t_todos, t_rin = (T(e, "iberos"), T(e, "romanos"), T(e, "godos"), T(e, "arabes"), T(e, "judios"),
                                                              T(e, "cristianos"), T(e, "todos"), T(e, "rincon"))
    t_que, t_pais, t_dime, t_coment = T(e, "que"), T(e, "pais"), T(e, "dimelo"), T(e, "comentarios")
    R.terreno(i0 - 0.3, "espana", COL["espana"], 0.8, capa=12)
    R.camara(i0 - 0.3, -3.6, 40.2, 2.0)
    R.camara(t_recibe, -3.6, 40.0, 2.15)
    R.camara(t_ib, -3.6, 39.6, 2.0)
    R.camara(t_rin + 0.3, -3.4, 39.8, 1.8)
    R.camara(FIN(e) + 1.2, -3.4, 39.8, 1.75)
    R.anio(i0, 1992)
    R.anio(t_hoy + 0.8, 2026)
    # cifras
    R.contador(t_49 - 0.3, t_hab, 0, 49_000_000, (960, 200), px=84, hasta_t=t_ib - 0.1)
    R.texto(t_hab - 0.1, t_ib - 0.2, "HABITANTES", (960, 300), px=52, d=0.4)
    R.snd(t_49 - 0.3, "reloj_rapido", 0.4, dur=1.0)
    R.contador(t_90 - 0.3, t_tur, 0, 90_000_000, (960, 420), px=84, formato="+ {:,}", hasta_t=t_ib - 0.1)
    R.texto(t_tur - 0.1, t_ib - 0.2, "TURISTAS AL AÑO", (960, 520), px=52, d=0.4)
    for k in range(2):
        R.act(lambda t: C.avion(), pos=lambda t, k=k: (lerp(-250 if k == 0 else 2170, 2170 if k == 0 else -250, prog(t, t_recibe - 0.2 + 0.4 * k, t_ib)),
                                                       780 - 160 * k + 30 * math.sin(t * 2), 0.6),
              t_in=t_recibe - 0.2 + 0.4 * k, d_in=0.1, entra="fija", sem=290 + k, sfx=[(0, "zoom_whoosh", 0.3)], t_out=t_ib, sale="cortar", z=3, flip=k == 1)
    # todos dejaron algo: la fila de personajes de todas las épocas
    figs = ((t_ib, E1.ibero(0, "feliz")), (t_rom, E1.legionario(0, "feliz")), (t_god, E1.rey_godo(0, "feliz")), (t_ara, E2.califa(0, "feliz")),
            (t_jud, E2.exiliado(0)), (t_cri, E2.rey_cristiano(0, "feliz")))
    for k, (t0, d) in enumerate(figs):
        x = 260 + 280 * k
        pa(R, d, x, 1010, 0.95, t0 - 0.1, t_que - 0.1, sem=292 + k, z=2, extra=[(0.0, "pluck", 0.4, {"tono": 1.0 + 0.1 * k})])
    titulo(R, t_todos - 0.1, t_que - 0.2, "TODOS DEJARON ALGO", px=80)
    # despedida
    titulo(R, t_que - 0.15, FIN(e) + 1.2, "¿QUÉ PAÍS SIGUE?", px=92)
    pa(R, lambda t: A.signo_pregunta(), lambda t: 560 + 0 * t, lambda t: 560 + 14 * math.sin(t * 4), 1.0, t_pais - 0.2, FIN(e) + 1.2, sem=298)
    pa(R, lambda t: A.signo_pregunta(), lambda t: 1380 + 0 * t, lambda t: 600 + 14 * math.sin(t * 4 + 1), 0.8, t_pais, FIN(e) + 1.2, sem=299)
    pa(R, C.boton_suscribir(), 900, 940, 1.0, t_dime - 0.2, FIN(e) + 1.2, sem=300, extra=[(0.1, "pop", 0.5), (0.2, "bling", 0.5)])
    R.texto(t_dime, FIN(e) + 1.2, "SUSCRÍBETE", (900, 940), px=72, d=0.6)
    pa(R, C.campana(), 1260, 930, 0.9, t_coment - 0.3, FIN(e) + 1.2, sem=301, extra=[(0.1, "campana", 0.5)])


# ------------------------------------------------------------------ cambios de escena procedurales
def _transiciones(R):
    tipos = ["tinta", "pincel", "papel", "portal", "rollo", "puntos", "ola", "pincel", "tinta", "papel", "persianas"]
    colores = [(198, 52, 46), (236, 184, 64), (86, 150, 112), (74, 128, 182), (150, 80, 150), (206, 70, 58), (70, 110, 180), (176, 120, 72),
               (120, 70, 140), (206, 70, 58), (232, 160, 60)]
    ids = [e["id"] for e in __import__("escena_base").TL["escenas"]]
    centros = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]
    extra = getattr(R, "trans_extra", [])
    k = 0
    for tc in centros:
        tipo, color = tipos[k % len(tipos)], colores[k % len(colores)]
        R.trans.append(Transicion(tc, tipo, color, (960, 540), (960, 540), dur=0.8, seed=k + 1))
        R.snd(tc - 0.4, SFX[tipo], 0.5, dur=0.8)
        k += 1
    for tc, tipo in extra:
        color = colores[k % len(colores)]
        R.trans.append(Transicion(tc, tipo, color, (960, 540), (960, 540), dur=0.8, seed=k + 1))
        R.snd(tc - 0.4, SFX[tipo], 0.5, dur=0.8)
        k += 1
