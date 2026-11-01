# -*- coding: utf-8 -*-
"""Coreografía (3/4): Reforma (1858, el motín en el palacio de Guadalajara, Juárez y Guillermo Prieto), Porfiriato (el ferrocarril de
1888, tequila y tranvías), la Cristiada (1926-1929 en Los Altos) y el siglo XX (cine de oro, mariachi y charro, la metrópoli y los
Mundiales de 1970 y 1986, la explosión de Analco en 1992 y el «Silicon Valley mexicano»)."""
import obj_a as A
from core import FIN, INI, T
from coreo_peg import BALON, C_CRISTERO, CO, HO, SI, XI, XX, ciclo_pant, grupo_ciclo
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo
import mapa as M


def cortes(R):
    pass


def construir(R):
    _reforma(R)
    _porfiriato(R)
    _cristiada(R)
    _siglo20(R)


# ------------------------------------------------------------------ REFORMA
def _reforma(R):
    e = "reforma"
    i0 = INI(e)
    t_dec, t_lib, t_con, t_mil, t_ent, t_pal = (T(e, "decadas"), T(e, "liberales"), T(e, "conservadores"), T(e, "mil"), T(e, "entra"),
                                                T(e, "palacio"))
    t_pel, t_apu, t_jua, t_poe, t_pri, t_int, t_val = (T(e, "peloton"), T(e, "apunta"), T(e, "juarez"), T(e, "poeta"), T(e, "prieto"),
                                                       T(e, "interpone"), T(e, "valientes"))
    t_sol, t_baj, t_sob, t_gan = T(e, "soldados"), T(e, "bajan"), T(e, "sobrevive"), T(e, "ganar")

    R.camara(i0 - 0.2, -103.3, 20.8, 1.25)
    R.camara(t_mil - 0.1, -103.3, 20.75, 1.6)
    R.camara(t_pal + 0.1, -103.35, 20.67, 3.8)
    R.camara(FIN(e) + 0.4, -103.35, 20.67, 4.0)

    R.anio(i0, 1857)
    R.sello(t_dec, "columnas", "REFORMA", color=(74, 138, 104))
    # frase 0: liberales contra conservadores
    R.terreno(t_lib - 0.1, "jalisco", COL["liberales"], 0.7)
    R.terreno(t_con - 0.1, "altos", COL["conservadores"], 0.7, capa=1)
    pa(R, XX(1), 330, 1010, 1.0, i0 - 0.1, t_pal, sem=200)
    R.texto(t_lib, t_pal - 0.1, "LIBERALES", (330, 580), px=46, d=0.4)
    pa(R, XI(4), 1600, 1010, 1.0, t_con - 0.1, t_pal, sem=201, flip=True)
    R.texto(t_con, t_pal - 0.1, "CONSERVADORES", (1600, 580), px=46, d=0.4)
    pa(R, A.espadas(), 960, 820, 0.9, t_con + 0.2, t_pal, sem=202, extra=[(0.05, "espada", 0.45)])
    R.anio(t_mil, 1858)
    R.terreno(t_pal - 0.2, None, COL["conservadores"], 0.4, capa=1)
    pa(R, XI(5), 960, 1010, 1.15, t_pal - 0.15, FIN(e) + 0.3, sem=203, entra="sube", dy=360, z=1)
    titulo(R, t_pal, t_pel - 0.1, "PALACIO DE GOBIERNO · GUADALAJARA", px=60)

    # frase 1: el pelotón, Juárez y Prieto
    for k in range(3):
        pa(R, XI(4), 230 + 140 * k, 1010 - 18 * (k % 2), 0.95, t_pel - 0.1 + 0.12 * k, t_baj, sem=204 + k, z=3, sale="baja", d_out=0.5)
    R.snd(t_apu, "crujido", 0.4)
    pa(R, XI(1), 1600, 1010, 1.05, t_jua - 0.15, FIN(e) + 0.3, sem=207, z=3)
    R.texto(t_jua, FIN(e) + 0.2, "BENITO JUÁREZ", (1600, 560), px=46, d=0.4)
    pa(R, XI(2), 1150, 1010, 1.0, t_pri - 0.15, FIN(e) + 0.3, sem=208, z=4, entra="der", dx=700, extra=[(0.05, "whoosh", 0.4)])
    R.texto(t_pri, t_val - 0.1, "GUILLERMO PRIETO", (1150, 470), px=42, d=0.4)
    R.texto(t_val - 0.1, FIN(e) + 0.3, "«¡LOS VALIENTES NO ASESINAN!»", (960, 196), px=74, d=0.9)
    R.snd(t_val - 0.1, "escribir", 0.4, dur=0.9)

    # frase 2: bajan las armas
    R.snd(t_baj, "golpe_suave", 0.4)
    R.texto(t_sob, FIN(e) + 0.2, "JUÁREZ SOBREVIVE", (1600, 470), px=40, d=0.4)


# ------------------------------------------------------------------ PORFIRIATO
def _porfiriato(R):
    e = "porfiriato"
    i0 = INI(e)
    t_paz, t_mil, t_fer, t_gdl = T(e, "paz"), T(e, "mil"), T(e, "ferrocarril"), T(e, "guadalajara")
    t_teq, t_tre, t_pai, t_ciu, t_fab, t_mer, t_tra = (T(e, "tequila"), T(e, "tren"), T(e, "pais"), T(e, "ciudad"), T(e, "fabricas"),
                                                       T(e, "mercados"), T(e, "tranvias"))

    R.camara(i0 - 0.2, -102.4, 20.6, 1.5)
    R.camara(t_gdl + 0.2, -102.7, 20.55, 1.55)
    R.camara(t_ciu - 0.1, -103.35, 20.67, 3.4)
    R.camara(FIN(e) + 0.4, -103.35, 20.67, 3.6)

    R.anio(i0, 1876)
    pa(R, XI(8), 960, 1000, 1.25, i0 - 0.1, t_fer - 0.3, sem=219, entra="izq", dx=1200, extra=[(0.05, "chorro", 0.3, {"dur": 1.0})])
    R.sello(t_paz, "locomotora", "PORFIRIATO", color=(196, 146, 68))
    R.anio(t_mil, 1888)
    R.ruta(M.RUTAS["tren"], t_fer - 0.3, 2.4, ancho=6.0, t1=t_ciu, dash=18, hueco=10)
    R.act(XI(8), pos_geo=R.camino_pos(M.RUTAS["tren"], t_fer - 0.2, 3.4), off=(0, -8), s=0.62, t_in=t_fer - 0.3, d_in=0.3, entra="pop",
          sem=220, zs=0.4, z=3, t_out=t_ciu)
    R.snd(t_fer - 0.2, "chorro", 0.35, dur=1.5)
    ciudad(R, t_gdl, t_ciu, "guadalajara", "GUADALAJARA", "abajo", 42)
    titulo(R, t_fer, t_teq - 0.1, "EL FERROCARRIL · 1888", px=74, snd=True)
    pa(R, SI(1), 330, 1010, 0.9, t_teq - 0.15, FIN(e) + 0.3, sem=221, extra=[(0.05, "pluck", 0.3)])
    pa(R, CO(5), 520, 1010, 0.5, t_tre - 0.1, FIN(e) + 0.3, sem=222)
    # la ciudad se llena: edificios y tranvía
    R.terreno(t_ciu - 0.1, "metro", COL["metro"], 1.2)
    for k, (dx, dy, dib) in enumerate(((-170, 20, SI(7)), (-60, -10, CO(2)), (70, 10, SI(7)), (180, 30, CO(0)))):
        ga(R, dib, CI["guadalajara"], t_fab - 0.1 + 0.12 * k, FIN(e) + 0.3, s=0.42,
           off=(dx, dy), sem=223 + k, zs=0.4, z=2)
    pa(R, SI(6), 1450, 1010, 0.6, t_mer - 0.1, FIN(e) + 0.3, sem=227)
    R.act(XI(9), pos=lambda t: (2100 - 700 * min(1.0, max(0.0, (t - t_tra) / 2.0)), 1010, 0.8), t_in=t_tra - 0.1, d_in=0.2, entra="fija",
          sem=228, z=3, flip=True)
    R.snd(t_tra, "ding", 0.35)
    R.terreno(FIN(e) + 0.4, None, COL["metro"], 0.3)


# ------------------------------------------------------------------ CRISTIADA
def _cristiada(R):
    e = "cristiada"
    i0 = INI(e)
    t_mil, t_cie, t_tem, t_cam, t_alt, t_lev, t_viv = (T(e, "mil"), T(e, "cierra"), T(e, "templos"), T(e, "campesinos"), T(e, "altos"),
                                                       T(e, "levantan"), T(e, "viva"))
    t_gue, t_cri, t_com, t_cab, t_dec, t_mue = (T(e, "guerra"), T(e, "cristera"), T(e, "combates"), T(e, "caballo"), T(e, "decenas"),
                                                T(e, "muertos"))
    t_mil2, t_igl, t_fir, t_paz, t_her, t_san = (T(e, "mil", frase=2), T(e, "iglesia"), T(e, "firman"), T(e, "paz"), T(e, "heridas"),
                                                 T(e, "sanar"))

    R.camara(i0 - 0.2, -102.6, 21.0, 1.5)
    R.camara(t_alt - 0.1, -102.4, 21.15, 2.4)
    R.camara(t_gue - 0.1, -102.4, 21.1, 2.5)
    R.camara(t_mil2 - 0.1, -102.5, 21.0, 2.1)
    R.camara(FIN(e) + 0.4, -102.6, 21.0, 2.0)

    R.anio(i0, 1926)
    R.sello(t_cie, "sombrero_rev", "LA CRISTIADA", color=(198, 70, 60))
    pa(R, XX(2), 960, 1010, 1.0, i0 - 0.1, t_gue - 0.1, sem=240, entra="sube", dy=340, extra=[(0.05, "golpe_suave", 0.45)])
    R.texto(t_tem, t_cam - 0.1, "TEMPLOS CERRADOS", (960, 196), px=74, d=0.6)
    R.terreno(t_alt - 0.15, "altos", COL["cristeros"], 1.0)
    pa(R, XX(0), 330, 1010, 1.05, t_cam - 0.1, FIN(e) + 0.3, sem=241)
    pa(R, XX(1), 1600, 1010, 1.0, t_lev, t_mil2, sem=242, flip=True)
    R.texto(t_viv - 0.1, t_gue - 0.1, "«¡VIVA CRISTO REY!»", (960, 196), px=78, d=0.6)
    R.snd(t_viv - 0.1, "cuerno", 0.4)

    titulo(R, t_cri - 0.1, t_mil2 - 0.2, "LA GUERRA CRISTERA · 1926-1929", px=66, snd=True)
    grupo_ciclo(R, C_CRISTERO, M.RUTAS["cristeros"], t_com - 0.2, 3.4, n=4, ancho=95, t1=t_mil2, s=0.58, sem=243, fps=11,
                extra=[(0.05, "galope", 0.4, {"dur": 2.0})])
    ciudad(R, t_alt, t_mil2, "tepatitlan", "TEPATITLÁN", "abajo", 36)
    ciudad(R, t_alt + 0.2, t_mil2, "san_juan_lagos", "SAN JUAN DE LOS LAGOS", "der", 34)
    for k, (dx, dy) in enumerate(((-120, 30), (0, 60), (120, 40))):
        ga(R, SI(8), CI["arandas"], t_mue - 0.1 + 0.15 * k, FIN(e) + 0.3, s=0.3, off=(dx, dy), sem=246 + k, zs=0.4, z=2)
    R.anio(t_mil2, 1929)
    pa(R, CO(7), 1600, 1010, 0.7, t_fir - 0.15, FIN(e) + 0.3, sem=249, entra="sube", dy=300, extra=[(0.05, "pincel", 0.3)])
    R.texto(t_paz, FIN(e) + 0.2, "LOS ARREGLOS · 1929", (1600, 640), px=42, d=0.4)
    R.terreno(t_her, None, COL["cristeros"], 2.0)


# ------------------------------------------------------------------ SIGLO XX
def _siglo20(R):
    e = "siglo20"
    i0 = INI(e)
    t_cin, t_oro, t_mun, t_mar, t_cha, t_sim, t_mex = (T(e, "cine"), T(e, "oro"), T(e, "mundo"), T(e, "mariachi"), T(e, "charro"),
                                                       T(e, "simbolo"), T(e, "mexico"))
    t_cre, t_met, t_mil, t_fut, t_set, t_och = (T(e, "crece"), T(e, "metropoli"), T(e, "millones"), T(e, "futbol"), T(e, "setenta"),
                                                T(e, "ochenta"))
    t_nov, t_tra, t_gas, t_dre, t_est, t_ana = (T(e, "noventa"), T(e, "tragedia"), T(e, "gasolina"), T(e, "drenaje"), T(e, "estallar"),
                                                T(e, "analco"))
    t_rei, t_ele, t_sof, t_apo, t_sil = T(e, "reinventa"), T(e, "electronica"), T(e, "software"), T(e, "apodo"), T(e, "silicon")

    R.camara(i0 - 0.2, -103.5, 20.5, 1.7)
    R.camara(t_cre - 0.1, -103.38, 20.66, 2.6)
    R.camara(t_met + 0.4, -103.38, 20.66, 3.8)
    R.camara(t_nov - 0.1, -103.34, 20.66, 4.2)
    R.camara(t_rei - 0.1, -103.38, 20.66, 3.2)
    R.camara(FIN(e) + 0.4, -103.38, 20.66, 3.0)

    R.anio(i0, 1940)
    R.sello(t_cin, "aguila", "SIGLO XX", color=(56, 138, 84))
    # frase 0: cine de oro, mariachi y charro
    pa(R, XX(6), 330, 1010, 0.95, i0 - 0.1, t_cre - 0.1, sem=260, extra=[(0.05, "crujido", 0.3)])
    titulo(R, t_oro - 0.1, t_cre - 0.2, "EL CINE DE ORO", px=78)
    pa(R, XX(3), 820, 1010, 1.0, t_mar - 0.15, t_cre - 0.1, sem=261, extra=[(0.05, "fanfarria", 0.35)])
    pa(R, XX(4), 1100, 1010, 1.0, t_mar + 0.05, t_cre - 0.1, sem=262)
    pa(R, XX(5), 1610, 1010, 1.05, t_cha - 0.15, t_cre - 0.1, sem=263)
    pa(R, SI(5), 560, 1010, 0.9, t_sim - 0.1, t_cre - 0.1, sem=264)
    R.anio(t_sim, 1955)

    # frase 1: la metrópoli y los Mundiales
    R.terreno(t_cre - 0.1, "metro", COL["metro"], 1.5)
    for k, (n, dx, dy) in enumerate(((1, -170, 0), (2, -70, -20), (3, 40, 10), (4, 150, -10))):
        ga(R, HO(n), CI["guadalajara"], t_met - 0.1 + 0.12 * k, t_nov - 0.1, s=0.42, off=(dx + 60, dy - 40), sem=265 + k, zs=0.4, z=2,
           entra="sube", dy=260, extra=[(0.05, "crece", 0.35)] if k == 0 else ())
    R.contador(t_mil - 0.3, t_mil + 0.6, 0, 5, (960, 196), px=78, formato="{} MILLONES", hasta_t=t_fut - 0.2)
    ga(R, XX(7), CI["estadio"], t_fut - 0.15, t_nov - 0.1, s=0.5, off=(-60, 30), sem=269, zs=0.4, z=3, extra=[(0.05, "fanfarria", 0.3)])
    R.anio(t_set, 1970)
    R.texto(t_set, t_nov - 0.2, "MUNDIALES 1970 · 1986", (960, 196), px=74, d=0.6)
    R.anio(t_och, 1986)
    ga(R, BALON, CI["estadio"], t_fut + 0.1, t_nov - 0.1, s=0.22, off=(110, 40), sem=270, zs=0.4, z=4, entra="cae", dy=500)

    # frase 2: 22 de abril de 1992
    R.anio(t_nov, 1992)
    pa(R, HO(0), 960, 1030, 1.75, t_nov + 0.2, t_rei - 0.1, sem=271, entra="sube", dy=200, extra=[(0.05, "impacto", 0.6), (0.2, "fuego", 0.4)])
    titulo(R, t_tra - 0.1, t_rei - 0.2, "22 DE ABRIL DE 1992", px=78)
    R.texto(t_ana - 0.1, t_rei - 0.1, "BARRIO DE ANALCO", (1560, 420), px=48, d=0.4)
    R.texto(t_gas, t_rei - 0.2, "gasolina en el drenaje", (960, 300), px=48, d=0.5)

    # frase 3: Silicon Valley mexicano
    pa(R, HO(5), 380, 1010, 0.8, t_ele - 0.15, FIN(e) + 0.3, sem=272, extra=[(0.05, "bling", 0.3)])
    pa(R, HO(6), 380, 700, 0.42, t_sof - 0.1, FIN(e) + 0.3, sem=273)
    pa(R, HO(11), 1600, 1010, 1.0, t_rei, FIN(e) + 0.3, sem=274)
    titulo(R, t_apo, FIN(e) + 0.3, "«SILICON VALLEY MEXICANO»", px=74, snd=True)
    R.terreno(FIN(e) + 0.4, None, COL["metro"], 0.3)
