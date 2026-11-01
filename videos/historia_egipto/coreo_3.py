# -*- coding: utf-8 -*-
"""Coreografía (3/4): Alejandro Magno (de Pela a Menfis, Siwa e hijo de Amón, Alejandría, el Faro y la Biblioteca, el reparto del imperio,
Ptolomeo se corona faraón), Cleopatra VII (César y Marco Antonio, Accio, el áspid, el granero de Roma) y el Egipto islámico
(la conquista árabe, El Cairo y Al-Azhar, Saladino y la Ciudadela, las cruzadas, los mamelucos frenan a los mongoles en Ain Yalut).
Capas: 0 = el poder que gobierna Egipto, 1 = Roma / Bizancio, 2 = imperio de Alejandro / cruzados, 3 = Macedonia / mongoles."""
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


def cortes(R):
    pass


def construir(R):
    _alejandro(R)
    _cleopatra(R)
    _islam(R)


# ------------------------------------------------------------------ ALEJANDRO MAGNO Y LOS PTOLOMEOS
def _alejandro(R):
    e = "alejandro"
    i0 = INI(e)
    t_has, t_tre, t_ent, t_vic, t_ale, t_mag = T(e, "hasta"), T(e, "trescientos"), T(e, "entra"), T(e, "victorioso"), T(e, "alejandro"), T(e, "magno")
    t_sac, t_cor, t_hijo, t_amon, t_fun, t_cos, t_met, t_alej = (T(e, "sacerdotes"), T(e, "coronan"), T(e, "hijo"), T(e, "amon"), T(e, "funda", frase=1),
                                                                 T(e, "costa"), T(e, "metropolis"), T(e, "alejandria"))
    t_all, t_faro, t_mar, t_mun, t_bib, t_ant = T(e, "alli"), T(e, "faro"), T(e, "maravilla"), T(e, "mundo"), T(e, "biblioteca"), T(e, "antiguedad")
    t_mue, t_gen, t_pto, t_fun2, t_din, t_gri, t_adop, t_coro = (T(e, "muerte"), T(e, "general"), T(e, "ptolomeo"), T(e, "funda", frase=3), T(e, "dinastia"),
                                                                  T(e, "griegos"), T(e, "adoptan"), T(e, "corona", frase=3))
    # cámara
    R.camara(i0 - 0.2, 24.4, 38.9, 2.4)
    R.camara(t_ent, 26.5, 37.2, 1.6)
    R.camara(t_mag, 30.0, 33.7, 1.15)
    R.camara(t_sac + 0.2, 27.6, 30.2, 2.6)
    R.camara(t_cos - 0.7, 27.8, 30.3, 2.7)
    R.camara(t_cos - 0.4, 29.4, 30.9, 3.6)
    R.camara(t_met, 29.92, 31.17, 8.6)
    R.camara(t_ant + 0.4, 29.92, 31.18, 9.2)
    R.camara(t_mue + 0.2, 31.5, 33.0, 1.15)
    R.camara(t_pto + 0.4, 30.0, 31.6, 1.4)
    R.camara(FIN(e) + 0.6, 29.6, 31.3, 1.5)
    # años
    R.anio(t_tre, -332)
    R.anio(t_fun, -331)
    R.anio(t_mue, -323)
    R.anio(t_fun2, -305)
    # territorio: Macedonia, el imperio de Alejandro (sobre el persa) y el reparto
    R.terreno(i0 - 0.6, None, COL["kush"], 0.4, capa=1)
    R.terreno(i0, "macedonia", COL["macedonia"], 0.9, capa=3)
    R.terreno(t_ent, "alejandro", COL["alejandro"], 1.8, capa=2)
    R.terreno(t_ale + 0.4, None, COL["macedonia"], 0.6, capa=3)
    ciudad(R, i0 + 0.1, t_ent - 0.2, "pela", "PELA", "der", 40)
    lugar(R, i0 + 0.3, t_ent + 0.2, "MACEDONIA", (21.6, 39.9), off=(0, 0), px=48)
    # Alejandro entra victorioso: de Pela a Menfis
    R.ruta(M.RUTAS["alejandro"], t_ent - 0.4, 2.4, ancho=5.0, t1=t_sac, flecha=True)
    andar(R, lambda p: E1.alejandro(p % 2, "feliz"), M.RUTAS["alejandro"], t_has, t_mag + 0.4 - t_has, t1=t_sac, s=0.55, sem=230, zs=0.4, z=3, fps=6,
          off=(0, 80))
    grupo(R, lambda p: E1.griego(p % 2, "feliz", "lanza"), M.RUTAS["alejandro"], t_has + 0.3, t_mag + 0.4 - t_has, n=2, ancho=90, t1=t_sac, s=0.42,
          sem=231, fps=6)
    R.snd(t_ent, "cuerno", 0.45)
    R.snd(t_ent + 0.3, "pasos", 0.4, dur=2.0)
    titulo(R, t_ale - 0.1, t_sac - 0.1, "ALEJANDRO MAGNO", px=80)
    # Siwa: el oráculo de Amón lo proclama hijo del dios
    R.ruta(M.RUTAS["siwa"], t_sac - 0.2, 1.4, ancho=5.0, t1=t_cos)
    ciudad(R, t_sac, t_cos - 0.3, "siwa", "OASIS DE SIWA", "abajo", 42)
    ga(R, E1.sacerdote(0, "feliz"), CI["siwa"], t_sac + 0.1, t_cos + 0.2, s=0.42, off=(-120, 10), sem=233, zs=0.4, z=2)
    ga(R, E2.dios("amon"), CI["siwa"], t_amon - 0.3, t_cos + 0.2, s=0.42, off=(120, 10), sem=234, zs=0.4, z=2, entra="sube", dy=300,
       extra=[(0.05, "brillo", 0.45)])
    R.morf(E1.alejandro(0, "feliz"), E1.alejandro_faraon(0, "feliz"), t_cor - 0.1, 0.7, (1500, 1010, 1.15), sem=235, salida=t_all, t_a=t_sac - 0.2)
    R.texto(t_hijo, t_all - 0.1, "HIJO DE AMÓN", (1500, 545), px=50, d=0.5)
    # Alejandría: la ciudad en cuadrícula
    ciudad(R, t_cos, FIN(e, 2) + 0.2, "alejandria", None)
    titulo(R, t_alej - 0.1, t_all - 0.1, "ALEJANDRÍA", px=86)

    def cuadricula(h, cam, t, fs, te):
        if not (t_met - 0.2 <= t <= FIN(e, 2) + 0.3):
            return
        x0, y0 = cam.pant(*CI["alejandria"])
        y0 += 80
        u = e_inout(prog(t, t_met - 0.2, t_met + 1.0)) * (1 - prog(t, FIN(e, 2), FIN(e, 2) + 0.3))
        for k in range(6):
            x = x0 - 260 + 104 * k
            linea_punteada(h, np.array([(x, y0 - 120), (x, y0 + 110)]), t, 18, 14, 3.4, 300 + k, fs, u)
        for k in range(4):
            y = y0 - 120 + 77 * k
            linea_punteada(h, np.array([(x0 - 260, y), (x0 + 260, y)]), t, 18, 14, 3.4, 310 + k, fs, u)
    R.frente.append(R._acot(cuadricula, t_met - 0.2))
    R.snd(t_met, "escribir", 0.4, dur=1.0)
    for k, (x, sem) in enumerate(((300, 236), (530, 237))):
        pa(R, E1.griego(k, "feliz", "rollo"), x, 1010, 0.9, t_met + 0.2 * k, t_bib - 0.3, sem=sem + 1000, flip=k == 1)
    # el Faro y la Biblioteca
    ga(R, E2.faro(), (29.885, 31.214), t_faro - 0.4, FIN(e, 2) + 0.3, s=0.4, off=(-300, 110), sem=238, zs=0.5, z=2, entra="pluma", d_in=1.0,
       extra=[(0.05, "crece", 0.45)])
    lugar(R, t_faro + 0.2, FIN(e, 2) + 0.2, "EL FARO", (29.885, 31.214), off=(-300, 150), px=46)
    for k, (dx, dy) in enumerate(((-440, -150), (-160, -190), (-420, 40))):
        ga(R, A.estrella5(), (29.885, 31.214), t_mar + 0.15 * k, t_bib, s=0.3, off=(dx, dy), sem=239 + k, zs=0.3, z=3,
           extra=[(0.0, "estrellitas", 0.35)] if k == 0 else ())
    titulo(R, t_mar, t_bib - 0.1, "MARAVILLA DEL MUNDO", px=70)
    ga(R, E2.biblioteca(), CI["alejandria"], t_bib - 0.3, FIN(e, 2) + 0.3, s=0.46, off=(230, 50), sem=242, zs=0.5, z=2, entra="pluma", d_in=1.0)
    lugar(R, t_bib + 0.1, FIN(e, 2) + 0.2, "LA BIBLIOTECA", CI["alejandria"], off=(230, 90), px=46)
    pa(R, E2.estante_rollos(), 330, 1010, 0.82, t_bib - 0.1, FIN(e, 2) + 0.3, sem=243, extra=[(0.05, "papel", 0.4)])
    pa(R, E1.griego(0, "asombro", "rollo"), 600, 1010, 0.82, T(e, "sabia"), FIN(e, 2) + 0.3, sem=244)
    # el imperio se reparte y Ptolomeo se corona faraón
    R.romper("diadocos", t_mue, t_mue + 0.6, t_gen + 0.4, t_pto + 0.4, capa=2, gap=20.0, deriva=50.0,
             colores=[COL["ptolemaico"], (120, 150, 90), (206, 120, 60), (232, 170, 70)])
    R.snd(t_mue, "crujido", 0.5, dur=0.8)
    titulo(R, t_mue - 0.1, t_pto - 0.2, "EL IMPERIO SE REPARTE", px=72)
    R.terreno(t_pto + 0.2, None, COL["alejandro"], 0.6, capa=2)
    R.terreno(t_pto - 0.1, "ptolemaico", COL["ptolemaico"], 1.0)
    R.morf(E1.ptolomeo(0, "serio"), E1.ptolomeo(0, "feliz", True), t_coro - 0.1, 0.7, (330, 1010, 1.15), sem=245, t_a=t_pto - 0.2)
    R.texto(t_pto + 0.2, FIN(e) + 0.3, "PTOLOMEO I", (330, 530), px=52, d=0.4)
    R.sello(t_din, "faro", "LOS PTOLOMEOS", color=(70, 120, 186))
    pa(R, E2.moneda_ptolemaica(), 980, 980, 0.72, t_gri - 0.2, FIN(e) + 0.4, sem=246, extra=[(0.05, "monedas", 0.4)])
    R.texto(t_gri, FIN(e) + 0.3, "REYES GRIEGOS", (980, 740), px=46, d=0.4)
    R.snd(t_coro, "brillo", 0.45)


# ------------------------------------------------------------------ CLEOPATRA
def _cleopatra(R):
    e = "cleopatra"
    i0 = INI(e)
    t_ult, t_ast, t_cul, t_cle, t_sep = T(e, "ultima"), T(e, "astuta"), T(e, "culta"), T(e, "cleopatra", frase=0), T(e, "septima")
    t_ali, t_jul, t_ces, t_lue, t_mar, t_int, t_sal, t_ind = (T(e, "aliada"), T(e, "julio"), T(e, "cesar"), T(e, "luego"), T(e, "marco"), T(e, "intenta"),
                                                              T(e, "salvar"), T(e, "independencia"))
    t_pero, t_bat, t_acc, t_leg, t_oct, t_ven = T(e, "pero"), T(e, "batalla"), T(e, "accio"), T(e, "legiones"), T(e, "octavio"), T(e, "vencen")
    t_cle2, t_eli, t_mue, t_cau, t_egi, t_conv, t_joya, t_gra, t_rom = (T(e, "cleopatra", frase=3), T(e, "elige"), T(e, "muerte"), T(e, "cautiverio"),
                                                                        T(e, "egipto"), T(e, "convierte"), T(e, "joya"), T(e, "granero"), T(e, "romano"))
    # cámara
    R.camara(i0 - 0.2, 29.9, 31.1, 5.4)
    R.camara(t_sep + 0.6, 29.92, 31.15, 5.0)
    R.camara(t_jul, 31.9, 34.2, 1.15)
    R.camara(t_ind, 31.9, 34.5, 1.2)
    R.camara(t_bat, 23.4, 38.4, 3.0)
    R.camara(t_ven + 0.4, 23.5, 38.1, 2.9)
    R.camara(t_eli, 30.9, 30.9, 2.2)
    R.camara(t_gra - 0.2, 31.9, 32.6, 1.25)
    R.camara(FIN(e) + 0.6, 31.9, 32.6, 1.25)
    # años
    R.anio(t_ult, -51)
    R.anio(t_ces, -48)
    R.anio(t_mar, -41)
    R.anio(t_pero, -31)
    R.anio(t_cle2, -30)
    # Cleopatra, astuta y culta
    ga(R, E2.faro(), (29.885, 31.214), i0 - 0.3, t_ali, s=0.42, off=(-200, 30), sem=250, zs=0.5, z=1)
    ga(R, E2.biblioteca(), CI["alejandria"], i0 - 0.1, t_ali, s=0.38, off=(260, 40), sem=251, zs=0.5, z=1)
    lugar(R, i0, t_ali, "ALEJANDRÍA", CI["alejandria"], off=(40, 120), px=46)
    pa(R, E1.cleopatra(0, "feliz"), 330, 1010, 1.2, t_ult - 0.2, t_pero, sem=252, extra=[(0.05, "brillo", 0.4)])
    R.texto(t_cle - 0.1, t_ali + 0.4, "CLEOPATRA VII", (330, 500), px=54, d=0.5)
    R.texto(t_ast, t_ali + 0.2, "ASTUTA", (1400, 720), px=50, d=0.3)
    R.texto(t_cul, t_ali + 0.2, "CULTA: HABLABA 9 IDIOMAS", (1300, 900), px=46, d=0.6)
    for k in range(3):
        pa(R, A.rollo_escritura(), 900 + 230 * k, 1010, 0.42, t_cul + 0.1 * k, t_ali + 0.2, sem=253 + k)
    R.snd(t_cul, "papel", 0.4)
    # César y Marco Antonio
    R.terreno(t_ali - 0.2, "roma_rep", COL["roma"], 1.4, capa=1)
    lugar(R, t_ali, t_ind, "ROMA", (30.5, 38.7), off=(0, 0), px=58)
    R.ruta(M.RUTAS["cesar"], t_jul - 0.3, 1.4, ancho=5.0, t1=t_pero, flecha=True)
    andar(R, lambda p: E3.galera_romana(p), M.RUTAS["cesar"], t_jul - 0.3, 1.8, t1=t_pero, s=0.36, sem=256, zs=0.4, z=2, fps=4)
    R.snd(t_jul - 0.2, "ola", 0.4, dur=1.0)
    pa(R, E1.cesar(0, "serio"), 980, 1010, 1.05, t_ces - 0.2, t_lue + 0.2, sem=257, sale="izq_fuera", d_out=0.5)
    R.texto(t_ces, t_lue, "JULIO CÉSAR", (980, 620), px=50, d=0.4)
    pa(R, E1.marco_antonio(0, "feliz"), 980, 1010, 1.05, t_mar - 0.1, t_pero, sem=258, entra="der", dx=900)
    R.texto(t_mar + 0.2, t_pero - 0.1, "MARCO ANTONIO", (980, 620), px=50, d=0.4)
    pa(R, E2.corazon(), 660, 760, 0.42, t_ces + 0.3, t_pero, sem=259, extra=[(0.05, "latido", 0.4)])
    R.texto(t_sal, t_pero - 0.1, "SALVAR SU REINO", (1500, 300), px=52, d=0.5)
    # Accio: la flota de Octavio vence a la de Cleopatra y Antonio
    ciudad(R, t_bat, t_cle2 - 0.2, "accio", None)
    lugar(R, t_bat + 0.1, t_cle2 - 0.2, "ACCIO", CI["accio"], off=(-10, 170), px=50)
    titulo(R, t_bat - 0.1, t_cle2 - 0.2, "BATALLA DE ACCIO", px=74)
    Pce = [(25.5, 35.5), (23.4, 37.0), (21.6, 38.3), (20.95, 38.85)]
    andar(R, lambda p: E3.barco_cleopatra(p), Pce, t_pero - 0.6, 1.6, t1=t_ven, s=0.4, sem=260, zs=0.4, z=2, fps=4)
    for k in range(2):
        andar(R, lambda p, k=k: E3.galera_romana(p + k), Pce, t_pero - 0.4 + 0.15 * k, 1.6, t1=t_cle2 - 0.2, s=0.34, sem=261 + k, zs=0.4, z=2, fps=4,
              off=((k * 2 - 1) * 170, 60))
    for k in range(3):
        andar(R, lambda p, k=k: E3.trirreme(p + k, (236, 214, 170), (186, 52, 46)), [(18.0, 39.6 - 0.25 * k), (19.6, 39.3 - 0.25 * k), (20.45, 39.1 - 0.25 * k)],
              t_bat - 0.2 + 0.12 * k, 1.2, t1=t_cle2 - 0.2, s=0.34, sem=263 + k, zs=0.4, z=2, fps=4, ease=e_out)
    R.snd(t_acc, "canonazo", 0.45)
    ga(R, A.estallido(14, 50, 150), CI["accio"], t_leg - 0.1, t_leg + 0.5, s=0.7, off=(80, 0), entra="fija", sale="cortar", sem=266, zs=0.3, z=4,
       extra=[(0.0, "explosion", 0.45)])
    for k in range(2):
        ga(R, lambda t, k=k: A.llama(int(t * 8) + k), CI["accio"], t_leg + 0.1 * k, t_cle2 - 0.2, s=0.32, off=(220 * k - 40, 40), sem=267 + k, zs=0.3, z=4,
           extra=[(0.0, "fuego", 0.4, {"dur": 1.4})] if k == 0 else ())
    pa(R, E1.octavio(0, "serio"), 1600, 1010, 1.0, t_oct - 0.2, t_cle2 - 0.1, sem=269, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_oct, t_cle2 - 0.2, "OCTAVIO", (1600, 620), px=50, d=0.4)
    andar(R, lambda p: E3.barco_cleopatra(p), [(20.95, 38.85), (22.0, 37.6), (24.0, 35.6)], t_ven, 1.2, t1=t_cle2 - 0.2, s=0.4, sem=270, zs=0.4, z=3, fps=4,
          entra="fija")
    # el áspid y el fin del Egipto independiente
    pa(R, E1.cleopatra_aspid(0), 330, 1010, 1.2, t_cle2 - 0.1, t_cau + 0.4, sem=271, sale="borrar", d_out=0.8, extra=[(0.05, "siseo", 0.45)])
    R.texto(t_mue, t_cau + 0.3, "EL ÁSPID", (330, 500), px=48, d=0.4)
    R.terreno(t_egi, "roma", COL["roma"], 1.2, capa=1)
    R.terreno(t_conv + 0.4, None, COL["ptolemaico"], 0.8)
    R.sello(t_conv, "laurel", "EGIPTO ROMANO", color=(186, 52, 46))
    for k in range(2):
        ga(R, E1.legionario(k, "serio"), CI["alejandria"], t_egi + 0.2 + 0.15 * k, FIN(e) + 0.4, s=0.4, off=(-90 + 180 * k, 30), sem=272 + k, zs=0.4, z=2)
    ga(R, A.estrella5(), (30.6, 27.6), t_joya - 0.1, FIN(e) + 0.4, s=0.45, off=(0, 0), sem=274, zs=0.3, z=3, extra=[(0.0, "bling", 0.4)])
    R.texto(t_joya, t_gra - 0.1, "LA JOYA", (960, 196), px=78, d=0.4)
    andar(R, lambda p: E3.barco_grano(p), [(29.92, 31.25), (26.0, 33.6), (22.0, 35.8), (18.0, 37.6)], t_gra - 0.3, 2.6, t1=FIN(e) + 0.4, s=0.4, sem=275, zs=0.4,
          z=2, fps=4)
    R.ruta([(29.92, 31.25), (26.0, 33.6), (22.0, 35.8), (18.0, 37.6)], t_gra - 0.3, 2.4, ancho=5.0, t1=FIN(e) + 0.3, flecha=True)
    pa(R, E2.gavilla(), 820, 1010, 0.6, t_gra, FIN(e) + 0.4, sem=276)
    pa(R, E2.saco_grano(), 1010, 1010, 0.55, t_gra + 0.15, FIN(e) + 0.4, sem=277)
    pa(R, E2.anfora(), 1180, 1010, 0.5, t_gra + 0.3, FIN(e) + 0.4, sem=278)
    R.texto(t_gra + 0.1, FIN(e) + 0.3, "EL GRANERO DE ROMA", (960, 196), px=74, d=0.6)


# ------------------------------------------------------------------ EGIPTO ISLÁMICO
def _islam(R):
    e = "islam"
    i0 = INI(e)
    t_sig, t_seis, t_lle, t_con, t_ara, t_fe, t_len = (T(e, "siglos"), T(e, "seiscientos"), T(e, "llega"), T(e, "conquista"), T(e, "arabe"), T(e, "fe"),
                                                       T(e, "lengua"))
    t_nace, t_cai, t_cora, t_com, t_cul = T(e, "nace"), T(e, "cairo"), T(e, "corazon"), T(e, "comercio"), T(e, "cultura")
    t_sul, t_sal, t_lev, t_ciu, t_pro, t_cru = T(e, "sultan"), T(e, "saladino"), T(e, "levanta"), T(e, "ciudadela"), T(e, "protege"), T(e, "cruzadas")
    t_tie, t_mam, t_gob, t_det, t_arr, t_inv, t_mon = (T(e, "tiempo"), T(e, "mamelucos"), T(e, "gobiernan"), T(e, "detener"), T(e, "arrolladora"),
                                                       T(e, "invasion"), T(e, "mongoles"))
    # cámara
    R.camara(i0 - 0.2, 34.6, 27.6, 1.05)
    R.camara(t_len + 0.4, 34.0, 28.0, 1.08)
    R.camara(t_nace + 0.1, 31.25, 30.03, 7.4)
    R.camara(t_cul + 0.6, 31.25, 30.03, 8.0)
    R.camara(t_ciu + 0.4, 31.26, 30.03, 8.4)
    R.camara(t_pro + 0.3, 35.0, 32.6, 2.6)
    R.camara(t_tie, 34.8, 32.3, 2.3)
    R.camara(t_mam + 0.3, 35.6, 31.6, 1.15)
    R.camara(FIN(e) + 0.6, 35.2, 31.6, 1.2)
    # años
    R.anio(t_sig, 395)
    R.anio(t_seis, 641)
    R.anio(t_nace, 969)
    R.anio(t_sul, 1171)
    R.anio(t_cru, 1187)
    R.anio(t_mam, 1250)
    R.anio(t_inv, 1260)
    # territorio
    R.terreno(t_sig, "roma", COL["bizancio"], 1.0, capa=1)
    R.terreno(t_con - 0.2, "bizancio", COL["bizancio"], 1.4, capa=1)
    R.terreno(t_con - 0.2, "califato", COL["califato"], 1.6)
    lugar(R, t_sig + 0.2, t_con - 0.2, "BIZANCIO", (30.6, 33.0), off=(0, 0), px=48)
    pa(R, E1.legionario(0, "serio"), 330, 1010, 1.05, t_sig - 0.1, t_con - 0.1, sem=279, sale="izq_fuera", d_out=0.5)
    R.texto(t_sig + 0.2, t_con - 0.2, "EGIPTO BIZANTINO", (330, 590), px=44, d=0.5)
    pa(R, A.arena_reloj(), 1560, 1010, 0.62, t_sig, t_con - 0.1, sem=278, extra=[(0.05, "reloj_rapido", 0.35, {"dur": 1.0})])
    # la conquista árabe
    R.ruta(M.RUTAS["arabes"], t_lle - 0.3, 2.4, ancho=5.0, t1=t_nace, flecha=True)
    grupo(R, lambda p: E3.jinete_camello(p), M.RUTAS["arabes"], t_lle - 0.3, 3.0, n=2, ancho=150, t1=t_nace, s=0.4, sem=280, fps=5)
    R.snd(t_lle - 0.2, "galope", 0.4, dur=2.0)
    ciudad(R, t_con, t_nace, "medina", "MEDINA", "der", 40)
    pa(R, E1.amr(0, "serio"), 330, 1010, 1.1, t_con - 0.2, t_nace, sem=282, extra=[(0.05, "cuerno", 0.35)])
    R.texto(t_ara, t_nace - 0.1, "AMR IBN AL-AS", (330, 610), px=48, d=0.5)
    pa(R, E2.minarete(300), 980, 1010, 0.75, t_fe - 0.3, t_nace, sem=283, entra="sube", dy=500)
    R.texto(t_fe, t_nace - 0.1, "EL ISLAM", (980, 720), px=48, d=0.4)
    pa(R, A.rollo_escritura(), 1240, 1000, 0.55, t_len - 0.2, t_nace, sem=284)
    R.texto(t_len, t_nace - 0.1, "EL ÁRABE", (1240, 860), px=48, d=0.4)
    R.sello(t_fe + 0.1, "minarete", "EGIPTO ISLÁMICO", color=(60, 130, 90))
    # El Cairo, comercio y cultura
    R.terreno(t_nace, "fatimi", COL["fatimi"], 1.0)
    ga(R, E2.el_cairo(), CI["cairo"], t_nace + 0.2, t_sul, s=0.45, off=(280, 30), sem=285, zs=0.5, z=1, entra="pluma", d_in=1.1,
       extra=[(0.05, "crece", 0.45, {"dur": 1.0})])
    ciudad(R, t_cai - 0.1, t_sul, "cairo", None)
    titulo(R, t_cai, t_sul - 0.1, "EL CAIRO", px=86)
    for k, (dx, dy) in enumerate(((-200, -320), (260, -360), (420, -200))):
        ga(R, A.estrella5(), CI["cairo"], t_cora + 0.12 * k, t_com + 0.4, s=0.28, off=(dx, dy), sem=286 + k, zs=0.3, z=3,
           extra=[(0.0, "estrellitas", 0.35)] if k == 0 else ())
    xc = lambda t: lerp(-200, 900, prog(t, t_com - 0.4, t_sul + 0.3))     # noqa: E731
    for k in range(2):
        pa(R, lambda t, k=k: E3.camello((int(t * 5) + k) % 4), (lambda t, k=k: xc(t) - 260 * k), lambda t: 1010, 0.42, t_com - 0.4, t_sul, sem=289 + k,
           entra="fija", z=3)
    pa(R, A.bolsa_dinero(), 1180, 1000, 0.55, t_com, t_sul, sem=291, extra=[(0.05, "monedas", 0.4)])
    R.texto(t_com + 0.1, t_sul - 0.1, "COMERCIO", (1180, 820), px=46, d=0.4)
    ga(R, E2.mezquita(), (31.262, 30.046), t_cul - 0.2, t_sul, s=0.28, off=(560, 70), sem=292, zs=0.5, z=1, entra="sube", dy=300)
    lugar(R, t_cul, t_sul - 0.1, "AL-AZHAR", (31.262, 30.046), off=(560, 110), px=40)
    pa(R, E2.estante_rollos(), 1690, 1010, 0.56, t_cul, t_sul, sem=293)
    R.texto(t_cul + 0.1, t_sul - 0.1, "CULTURA", (1690, 790), px=46, d=0.4)
    # Saladino, la Ciudadela y las cruzadas
    R.terreno(t_sul, "ayubi", COL["ayubi"], 1.2)
    R.terreno(t_sul, None, COL["bizancio"], 1.0, capa=1)
    pa(R, E1.saladino(0, "serio"), 330, 1010, 1.15, t_sul - 0.2, t_pro + 0.3, sem=294, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_sal, t_pro + 0.2, "SALADINO", (330, 600), px=54, d=0.4)
    ga(R, E2.ciudadela(), CI["ciudadela"], t_lev - 0.2, t_pro + 0.3, s=0.5, off=(60, 30), sem=295, zs=0.5, z=1, entra="pluma", d_in=1.2,
       extra=[(0.05, "crece", 0.45, {"dur": 1.0})])
    lugar(R, t_ciu, t_pro + 0.2, "LA CIUDADELA", CI["ciudadela"], off=(60, 80), px=48)
    R.sello(t_ciu - 0.6, "castillo", "SALADINO", color=(206, 150, 40))
    R.terreno(t_pro, "cruzados", COL["cruzados"], 1.0, capa=2)
    lugar(R, t_cru, FIN(e, 2) + 0.4, "CRUZADOS", (33.9, 34.0), off=(0, 0), px=50)
    for k in range(2):
        andar(R, lambda p, k=k: E3.trirreme(p, (236, 236, 226), (200, 50, 46)), M.RUTAS["cruzados"], t_pro - 0.6 + 0.2 * k, 1.8, t1=t_mam, s=0.32, sem=296 + k,
              zs=0.4, z=2, fps=4, off=formacion(k, 2, 160))
    ga(R, lambda t: E3.jinete(int(t * 6) % 4, "cruzado"), CI["acre"], t_cru - 0.3, t_mam, s=0.38, off=(80, -40), sem=298, zs=0.4, z=3, flip=True)
    andar(R, lambda p: E3.jinete(p, "saladino"), [(31.24, 30.04), (32.6, 31.0), (34.45, 31.5), (35.2, 32.3), (35.45, 32.8)], t_pro, 1.8, t1=t_mam, s=0.38, sem=299,
          zs=0.4, z=3, fps=8)
    R.snd(t_pro, "galope", 0.45, dur=1.8)
    ciudad(R, t_cru - 0.2, t_mam, "jerusalen", "JERUSALÉN", "izq", 40)
    ga(R, A.espadas(), (35.45, 32.8), t_cru + 0.3, t_mam, s=0.34, off=(0, -40), sem=300, zs=0.3, z=4, extra=[(0.05, "espada", 0.5)])
    # los mamelucos detienen a los mongoles en Ain Yalut (1260)
    R.terreno(t_mam - 0.2, "mameluco", COL["mameluco"], 1.2)
    R.terreno(t_mam - 0.4, None, COL["cruzados"], 1.0, capa=2)
    R.sello(t_gob, "espadas", "MAMELUCOS", color=(196, 110, 50))
    pa(R, E1.mameluco(0, "serio"), 330, 1010, 1.1, t_mam - 0.2, FIN(e) + 0.4, sem=301)
    R.texto(t_mam + 0.1, FIN(e) + 0.3, "MAMELUCOS", (330, 600), px=52, d=0.4)
    R.terreno(t_arr - 0.3, "mongoles", COL["mongoles"], 1.6, capa=3)
    lugar(R, t_arr, FIN(e) + 0.3, "MONGOLES", (43.6, 35.2), off=(0, 0), px=54)
    R.ruta(M.RUTAS["mongoles"], t_arr - 0.4, 1.6, ancho=5.0, t1=FIN(e) + 0.3, flecha=True)
    for k in range(3):
        andar(R, lambda p, k=k: E3.jinete(p + k, "mongol"), M.RUTAS["mongoles"], t_arr - 0.3 + 0.15 * k, t_mon + 0.5 - t_arr, t1=t_mon + 0.9, s=0.34,
              sem=302 + k, zs=0.4, z=3, fps=8, off=formacion(k, 3, 120))
    R.snd(t_arr - 0.2, "galope", 0.5, dur=2.2)
    Pm = [(31.24, 30.04), (32.6, 31.0), (34.45, 31.5), (35.0, 32.2), (35.36, 32.55)]
    for k in range(2):
        andar(R, lambda p, k=k: E3.jinete(p + k, "mameluco"), Pm, t_gob + 0.2 * k, t_mon + 0.5 - t_gob, s=0.34, sem=305 + k, zs=0.4, z=3, fps=8,
              off=formacion(k, 2, 120))
    ciudad(R, t_mon + 0.2, FIN(e) + 0.4, "ain_yalut", "AIN YALUT (1260)", "abajo", 40)
    ga(R, A.estallido(14, 50, 150), CI["ain_yalut"], t_mon + 0.4, t_mon + 0.9, s=0.6, off=(0, -50), entra="fija", sale="cortar", sem=307, zs=0.3, z=4,
       extra=[(0.0, "explosion", 0.4)])
    ga(R, A.espadas(), CI["ain_yalut"], t_mon + 0.6, FIN(e) + 0.4, s=0.34, off=(0, -60), sem=308, zs=0.3, z=4, extra=[(0.05, "espada", 0.5)])
