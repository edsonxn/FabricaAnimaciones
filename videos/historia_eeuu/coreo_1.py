# -*- coding: utf-8 -*-
"""Coreografía (1/4): gancho (de trece colonias a superpotencia, 65 millones de hispanos), pueblos originarios (huellas de White Sands,
Cahokia y su pirámide de tierra, Mesa Verde, la Confederación iroquesa), colonias (San Agustín 1565, Jamestown y el tabaco, 1619,
el Mayflower, trece colonias entre Francia y España) y la Revolución (impuestos y té de Boston, Lexington, la Declaración de 1776,
Washington, Francia y Gálvez, Yorktown).
Capas de territorio: 0 = nación principal (nativos / colonias / EE. UU.), 1 = España, 2 = Francia / Gran Bretaña (Canadá),
3 = pueblos originarios destacados (Cahokia, pueblos, iroqueses)."""
import mapa as M
import obj_a as A
import obj_c as C
import obj_us1 as P1
import obj_us2 as P2
import obj_us3 as P3
from core import FIN, INI, T, kf
from coreo_util import CI, COL, andar, ciudad, foco, ga, grupo, lugar, pa, para, titulo

MAR_TXT = (58, 108, 148)
TIERRA_TXT = (146, 110, 72)
BOSQUE_TXT = (76, 118, 82)


def cortes(R):
    pass


def construir(R):
    _mares(R)
    _gancho(R)
    _originarios(R)
    _colonias(R)
    _revolucion(R)


def _mares(R):
    R.mar("us", "OCÉANO ATLÁNTICO", -68.5, 33.5, 46, 0.44, color=MAR_TXT)
    R.mar("us", "OCÉANO PACÍFICO", -124.0, 33.0, 44, 0.44, rot=-0.55, color=MAR_TXT)
    R.mar("us", "GOLFO DE MÉXICO", -90.0, 25.8, 40, 0.44, color=MAR_TXT)
    R.mar("us", "MONTAÑAS ROCOSAS", -108.8, 42.5, 30, 0.32, rot=-1.05, color=TIERRA_TXT)
    R.mar("us", "GRANDES LLANURAS", -100.5, 39.0, 30, 0.30, color=TIERRA_TXT)
    R.mar("us", "APALACHES", -80.6, 37.6, 24, 0.30, rot=-0.85, color=BOSQUE_TXT)
    R.mar("us", "GRANDES LAGOS", -84.0, 46.6, 24, 0.32, color=MAR_TXT)
    R.mar("us", "DESIERTO DE MOJAVE", -116.0, 35.0, 22, 0.30, color=TIERRA_TXT)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"

    def W(i, w):
        return T(e, w, frase=i)

    t_tre, t_atl, t_dos, t_pot, t_pla = W(0, "trece"), W(0, "atlantico"), W(0, "dos"), W(0, "potencia"), W(0, "planeta")
    t_rev, t_gue, t_inv, t_sue, t_hoy, t_ses, t_his = (W(1, "revoluciones"), W(1, "guerras"), W(1, "inventos"), W(1, "suenos"),
                                                       W(1, "hoy"), W(1, "sesenta"), W(1, "hispanos"))
    t_esta, t_hist, t_est, t_seis, t_min = W(2, "esta"), W(2, "historia"), W(2, "estados"), W(2, "seis"), W(2, "minutos")

    # cámara: costa atlántica de las trece colonias -> todo el país -> vista general
    para(R, 0.0, 2.4, -75.5, 39.2, 3.2)
    para(R, 4.6, 10.6, -95.5, 37.6, 0.78)
    para(R, 11.8, 14.2, -101.0, 33.5, 1.05)
    para(R, 15.0, FIN(e) + 0.6, -95.5, 37.4, 0.74)

    # frase 0: trece colonias pegadas al Atlántico -> la mayor potencia del planeta
    R.terreno(0.0, "trece", COL["colonias"], 0.9)
    R.terreno(t_dos + 0.3, "eeuu_mod", COL["eeuu"], 1.6)
    R.snd(t_dos + 0.3, "whoosh", 0.45, dur=1.0)
    R.contador(t_tre - 0.1, t_tre + 0.8, 1, 13, (960, 196), px=82, formato="{} COLONIAS", hasta_t=t_dos + 0.2)
    pa(R, P2.bandera_13(), 330, 1010, 1.0, 0.3, t_pot, sem=1, entra="sube", dy=320, extra=[(0.05, "fanfarria", 0.32)])
    andar(R, lambda p: P2.barco_ingles(p), [(-66.0, 38.0), (-72.5, 39.6)], 0.4, 3.0, t1=t_pot, s=0.40, sem=2, zs=0.4, z=2, fps=4)
    lugar(R, t_atl - 0.2, t_dos + 0.3, "ATLÁNTICO", (-70.6, 38.7), off=(0, 0), px=46)
    ga(R, P3.skyline_nyc(), CI["nueva_york"], t_pot - 0.3, t_rev - 0.1, s=0.42, off=(0, -10), sem=3, zs=0.4, z=2, entra="sube", dy=300,
       extra=[(0.05, "crece", 0.4)])
    ga(R, P3.capitolio(), CI["washington"], t_pot - 0.1, t_rev - 0.1, s=0.36, off=(0, -10), sem=4, zs=0.4, z=2, entra="sube", dy=260)
    ga(R, P3.golden_gate(), CI["san_francisco"], t_pot + 0.1, t_rev - 0.1, s=0.40, off=(30, 0), sem=5, zs=0.4, z=2, entra="sube", dy=260)
    pa(R, P3.cohete_saturno(), 1640, 1010, 0.92, t_pot - 0.2, t_rev + 0.1, sem=6, entra="sube", dy=420, extra=[(0.05, "zoom_whoosh", 0.4)])
    titulo(R, t_pot - 0.2, t_rev - 0.2, "LA MAYOR POTENCIA DEL PLANETA", px=74)

    # frase 1: revoluciones, guerras, inventos y sueños + 65 millones de hispanos
    pa(R, P1.miliciano(0, "enojo"), 290, 1010, 1.0, t_rev - 0.15, t_hoy, sem=7, extra=[(0.05, "tambor", 0.35)])
    R.texto(t_rev, t_hoy - 0.1, "REVOLUCIONES", (290, 610), px=40, d=0.35)
    pa(R, P1.soldado_union(0, "serio"), 640, 1010, 1.0, t_gue - 0.15, t_hoy, sem=8, extra=[(0.05, "canonazo", 0.3)])
    R.texto(t_gue, t_hoy - 0.1, "GUERRAS", (640, 610), px=40, d=0.3)
    pa(R, P1.edison(0, "feliz"), 1290, 1010, 1.0, t_inv - 0.15, t_hoy, sem=9, extra=[(0.05, "ding", 0.4)])
    R.texto(t_inv, t_hoy - 0.1, "INVENTOS", (1290, 610), px=40, d=0.3)
    pa(R, P1.mlk(0, "feliz"), 1630, 1010, 1.0, t_sue - 0.15, t_hoy, sem=10, flip=True, extra=[(0.05, "brillo", 0.35)])
    R.texto(t_sue, t_hoy - 0.1, "SUEÑOS", (1630, 610), px=40, d=0.3)
    R.terreno(t_hoy - 0.2, "perdido_1848", (232, 168, 70), 1.0, capa=1)
    R.terreno(t_esta - 0.2, None, (232, 168, 70), 0.6, capa=1)
    for k, (c, dx) in enumerate((("san_antonio", 0), ("santa_fe", 0), ("los_angeles", 0))):
        ciudad(R, t_hoy + 0.15 * k, t_esta - 0.1, c, {"san_antonio": "SAN ANTONIO", "santa_fe": "SANTA FE", "los_angeles": "LOS ÁNGELES",
                                                       "miami": "MIAMI"}[c], "abajo", 34)
    ga(R, P2.mision_espanola(), CI["santa_fe"], t_hoy, t_esta - 0.1, s=0.40, off=(0, -30), sem=11, zs=0.4, z=2, entra="sube", dy=260)
    ga(R, P2.el_alamo(), CI["san_antonio"], t_hoy + 0.2, t_esta - 0.1, s=0.38, off=(0, -30), sem=12, zs=0.4, z=2, entra="sube", dy=260)
    pa(R, P1.ciudadana_hispana(0, "feliz"), 330, 1010, 1.0, t_ses - 0.2, t_esta, sem=13)
    pa(R, P1.ciudadano_hoy(0, "feliz"), 1600, 1010, 1.0, t_ses, t_esta, sem=14, flip=True)
    R.contador(t_ses - 0.2, t_his + 0.3, 0, 65, (960, 196), px=82, formato="{} MILLONES DE HISPANOS", hasta_t=t_esta - 0.1)
    R.snd(t_ses - 0.2, "reloj_rapido", 0.35, dur=0.9)

    # frase 2: título
    R.texto(t_hist - 0.2, FIN(e) + 0.6, "LA HISTORIA DE ESTADOS UNIDOS", (960, 178), px=90, d=0.9)
    R.texto(t_seis - 0.1, FIN(e) + 0.6, "en 6 minutos", (960, 296), px=72, d=0.6)
    R.snd(t_hist - 0.2, "escribir", 0.45, dur=0.9)
    pa(R, P3.bandera_eeuu(), 300, 1010, 1.0, t_esta - 0.1, FIN(e) + 0.6, sem=15, entra="sube", dy=340, extra=[(0.05, "fanfarria", 0.35)])
    pa(R, P3.estatua_libertad(), 600, 1010, 0.86, t_est - 0.1, FIN(e) + 0.6, sem=16, entra="sube", dy=360)
    pa(R, lambda t: C.cronometro(round(kf(t, [(t_seis, 0.0), (FIN(e) + 0.8, 0.9)], ease=lambda u: u), 2)), 1640, 860, 0.85, t_seis - 0.1,
       FIN(e) + 0.6, sem=17, extra=[(0.08, "reloj_rapido", 0.4, {"dur": 1.1})])


# ------------------------------------------------------------------ PUEBLOS ORIGINARIOS
def _originarios(R):
    e = "originarios"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_vei, t_pri, t_hue, t_nue = W(0, "veinte"), W(0, "primeros"), W(0, "huellas"), W(0, "nuevo")
    t_mis, t_cah, t_ciu, t_mil, t_cor, t_pir = W(1, "misisipi"), W(1, "cahokia"), W(1, "ciudad"), W(1, "miles"), W(1, "coronada"), W(1, "piramide")
    t_sur, t_anc, t_con, t_aca, t_mesa = W(2, "suroeste"), W(2, "ancestrales"), W(2, "construyen"), W(2, "acantilados"), W(2, "mesa")
    t_nor, t_cin, t_iro, t_unen, t_conf, t_cons = (W(3, "noreste"), W(3, "cinco"), W(3, "iroquesas"), W(3, "unen"), W(3, "confederacion"),
                                                   W(3, "consejo"))

    # cámara: Beringia/costa del Pacífico -> White Sands -> Cahokia -> Mesa Verde -> Onondaga
    para(R, i0 - 0.6, i0 + 0.6, -112.0, 41.0, 1.25)
    foco(R, t_hue - 0.5, t_mis - 0.4, CI["white_sands"], 4.4)
    foco(R, t_cah - 0.5, t_sur - 0.3, CI["cahokia"], 5.4)
    foco(R, t_con - 0.6, t_nor - 0.3, CI["mesa_verde"], 5.2)
    foco(R, t_iro - 0.5, FIN(e) + 0.6, CI["onondaga"], 4.4)

    # años
    R.anio(i0 + 0.1, -21000)
    R.anio(t_mis, 1100)
    R.anio(t_sur + 0.2, 1200)
    R.anio(t_nor + 0.2, 1450)

    # el país antes de los europeos: un mosaico de naciones (fractura de Voronoi, casi quieta)
    R.terreno(i0 - 0.4, "eeuu_mod", COL["nativos"], 1.2)
    R.romper("naciones_nativas", i0 - 0.2, i0 + 1.0, FIN(e) + 0.6, FIN(e) + 1.2, capa=0, gap=7.0, deriva=6.0)
    R.snd(i0, "crujido", 0.35, dur=0.9)
    R.sello(t_pri, "huella", "PRIMEROS PUEBLOS", color=(176, 112, 64))

    # frase 0: del noroeste a White Sands; huellas de hace más de 20 000 años
    R.ruta(M.RUTAS["poblamiento"], i0 - 0.1, 2.4, ancho=5.0, t1=t_mis - 0.2, flecha=True)
    grupo(R, lambda p: P1.cazador_paleo(p % 2, "serio"), M.RUTAS["poblamiento"], i0, 3.0, n=3, ancho=80, t1=t_hue + 0.4, s=0.40, sem=30, fps=6)
    R.snd(i0 + 0.2, "pasos", 0.35, dur=1.8)
    andar(R, lambda p: P2.mamut(p), [(-108.6, 33.6), (-106.9, 33.2)], t_vei, 3.4, t1=t_mis - 0.2, s=0.44, sem=33, zs=0.45, z=2, fps=4)
    ga(R, P2.huellas_pie(), CI["white_sands"], t_hue - 0.2, t_mis - 0.2, s=0.50, off=(60, 40), sem=34, zs=0.45, z=1,
       extra=[(0.05, "pasos", 0.4, {"dur": 0.8})])
    pa(R, P1.cazador_paleo(0, "serio"), 300, 1010, 1.02, t_pri - 0.1, t_mis - 0.1, sem=35)
    pa(R, P1.mujer_paleo(0, "feliz"), 560, 1010, 0.96, t_hue - 0.2, t_mis - 0.1, sem=36, flip=True)
    pa(R, P2.punta_clovis(), 1600, 1000, 0.8, t_hue, t_mis - 0.1, sem=37, entra="sube", dy=300, extra=[(0.05, "golpe_suave", 0.4)])
    R.texto(t_hue + 0.2, t_mis - 0.2, "PUNTA DE PIEDRA", (1600, 700), px=40, d=0.35)
    lugar(R, t_nue - 0.3, t_mis - 0.2, "WHITE SANDS (NUEVO MÉXICO)", CI["white_sands"], off=(0, 120), px=42)
    titulo(R, t_vei - 0.2, t_hue - 0.3, "+20.000 AÑOS", px=82)

    # frase 1: Cahokia junto al Misisipi, ciudad de miles de personas con una pirámide de tierra
    R.terreno(t_mis - 0.1, "cahokia", COL["cahokia"], 1.0, capa=3)
    R.snd(t_mis, "whoosh", 0.4, dur=0.7)
    lugar(R, t_mis, t_sur - 0.3, "RÍO MISISIPI", (-90.3, 38.25), off=(0, 0), px=40)
    ciudad(R, t_cah - 0.1, t_sur - 0.3, "cahokia", "CAHOKIA", "abajo", 48)
    ga(R, P2.monks_mound(), CI["cahokia"], t_cor - 0.3, t_sur - 0.2, s=0.62, off=(0, -20), sem=40, zs=0.5, z=2, entra="pluma", d_in=1.1,
       extra=[(0.05, "crece", 0.5, {"dur": 1.0})])
    for k, (dx, dy) in enumerate(((-300, 40), (300, 50))):
        ga(R, P2.aldea_cahokia(), CI["cahokia"], t_ciu - 0.1 + 0.2 * k, t_sur - 0.2, s=0.40, off=(dx, dy), sem=41 + k, zs=0.45, z=1,
           entra="sube", dy=240)
    pa(R, P1.jefe_cahokia(0, "serio"), 300, 1010, 1.05, t_cah - 0.1, t_sur - 0.1, sem=43, extra=[(0.05, "tambor", 0.35)])
    R.contador(t_mil - 0.2, t_mil + 0.8, 0, 10_000, (960, 196), px=80, formato="+{:,} PERSONAS", hasta_t=t_pir - 0.2)
    R.snd(t_mil - 0.2, "reloj_rapido", 0.35, dur=0.9)
    titulo(R, t_pir - 0.1, t_sur - 0.3, "LA PIRÁMIDE DE TIERRA", px=78)
    pa(R, P1.alfarero_pueblo(0, "feliz"), 1620, 1010, 0.98, t_cor, t_sur - 0.1, sem=44, flip=True)

    # frase 2: Mesa Verde, aldeas en los acantilados
    R.terreno(t_sur - 0.1, "pueblo", COL["pueblo"], 1.0, capa=3)
    R.snd(t_sur, "whoosh", 0.4, dur=0.7)
    titulo(R, t_anc - 0.2, t_nor - 0.3, "PUEBLOS ANCESTRALES", px=78)
    ciudad(R, t_mesa - 0.3, t_nor - 0.3, "mesa_verde", "MESA VERDE", "abajo", 46)
    ga(R, P2.casa_acantilado(), CI["mesa_verde"], t_con - 0.1, t_nor - 0.2, s=0.66, off=(0, -30), sem=50, zs=0.5, z=2, entra="pluma",
       d_in=1.1, extra=[(0.05, "crece", 0.5, {"dur": 1.0})])
    ga(R, P2.vasija_pueblo(), CI["mesa_verde"], t_aca - 0.1, t_nor - 0.2, s=0.30, off=(-280, 60), sem=51, zs=0.45, z=1, entra="sube", dy=200)
    pa(R, P1.mujer_pueblo(0, "feliz"), 300, 1010, 1.0, t_anc - 0.2, t_nor - 0.1, sem=52)
    pa(R, P1.alfarero_pueblo(0, "feliz"), 560, 1010, 0.96, t_con - 0.1, t_nor - 0.1, sem=53, flip=True)
    pa(R, P2.vasija_pueblo(), 1600, 1000, 0.8, t_aca - 0.2, t_nor - 0.1, sem=54, entra="sube", dy=280, extra=[(0.05, "pluck", 0.35)])
    R.texto(t_aca, t_nor - 0.2, "CERÁMICA PUEBLO", (1600, 700), px=40, d=0.35)

    # frase 3: cinco naciones iroquesas y su gran consejo
    R.terreno(t_nor - 0.1, "iroquesa", COL["iroquesa"], 1.0, capa=3)
    R.snd(t_nor, "whoosh", 0.4, dur=0.7)
    ciudad(R, t_iro - 0.2, FIN(e) + 0.3, "onondaga", "ONONDAGA", "abajo", 44)
    ga(R, P2.casa_larga(), CI["onondaga"], t_iro - 0.1, FIN(e) + 0.3, s=0.54, off=(0, -20), sem=60, zs=0.5, z=2, entra="sube", dy=280,
       extra=[(0.05, "crece", 0.45)])
    ga(R, P2.casa_larga(), CI["onondaga"], t_unen - 0.1, FIN(e) + 0.3, s=0.38, off=(-330, 40), sem=61, zs=0.45, z=1, entra="sube", dy=220)
    R.contador(t_cin - 0.2, t_cin + 0.6, 1, 5, (960, 196), px=82, formato="{} NACIONES", hasta_t=t_conf - 0.2)
    titulo(R, t_conf - 0.1, FIN(e) + 0.2, "CONFEDERACIÓN IROQUESA", px=78)
    pa(R, P1.sachem_iroques(0, "serio"), 300, 1010, 1.05, t_cin - 0.1, FIN(e) + 0.3, sem=62, extra=[(0.05, "cuerno", 0.3)])
    pa(R, P1.sachem_iroques(0, "feliz"), 560, 1010, 0.96, t_unen - 0.1, FIN(e) + 0.3, sem=63, flip=True)
    pa(R, P2.cinturon_wampum(), 1560, 1000, 0.9, t_unen - 0.1, FIN(e) + 0.3, sem=64, entra="sube", dy=300, extra=[(0.05, "brillo", 0.35)])
    R.texto(t_cons - 0.3, FIN(e) + 0.2, "EL GRAN CONSEJO", (1560, 760), px=42, d=0.4)


# ------------------------------------------------------------------ COLONIAS
def _colonias(R):
    e = "colonias"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_eur, t_esp, t_mil0, t_fun, t_san, t_flo = W(0, "europeos"), W(0, "espanoles"), W(0, "mil"), W(0, "fundan"), W(0, "san"), W(0, "florida")
    t_mil1, t_ing, t_lev, t_jam, t_vir, t_enr, t_tab = (W(1, "mil"), W(1, "ingleses"), W(1, "levantan"), W(1, "jamestown"), W(1, "virginia"),
                                                        W(1, "enriquecen"), W(1, "tabaco"))
    t_poc, t_afr, t_esc, t_mil2, t_may, t_per = W(2, "pocos"), W(2, "africanos"), W(2, "esclavizados"), W(2, "mil"), W(2, "mayflower"), W(2, "peregrinos")
    t_cos, t_tre, t_bri, t_rod, t_fra, t_esp3 = W(3, "costa"), W(3, "trece"), W(3, "britanicas"), W(3, "rodeadas"), W(3, "francia"), W(3, "espana")

    # cámara: Florida -> Virginia -> Plymouth -> toda la costa entre Francia y España
    para(R, i0 - 0.8, i0 + 1.4, -82.0, 28.6, 3.0)
    foco(R, t_fun - 1.0, t_mil1 - 0.4, CI["san_agustin"], 4.8)
    foco(R, t_jam - 1.1, t_mil2, CI["jamestown"], 5.2)
    foco(R, t_may - 0.5, t_cos - 0.2, CI["plymouth"], 5.0)
    para(R, t_tre - 0.3, FIN(e) + 0.6, -84.0, 38.0, 1.05)

    # años
    R.anio(i0 + 0.1, 1565)
    R.anio(t_mil1, 1607)
    R.anio(t_afr, 1619)
    R.anio(t_mil2 + 0.3, 1620)
    R.anio(t_tre, 1750)

    # fuera los pueblos destacados: el mosaico nativo se desvanece despacio
    R.terreno(i0 - 0.3, None, COL["iroquesa"], 0.6, capa=3)
    R.terreno(i0 + 0.6, None, COL["nativos"], 1.4)

    # frase 0: San Agustín (1565), la ciudad europea más antigua de EE. UU.
    andar(R, lambda p: P2.galeon_es(p), M.RUTAS["espanoles_florida"], i0 - 0.1, 3.2, t1=t_san + 0.6, s=0.42, sem=70, zs=0.4, z=3, fps=4)
    R.snd(i0, "ola", 0.35, dur=1.2)
    R.terreno(t_fun - 0.1, "florida_1565", COL["espana"], 1.0, capa=1)
    ciudad(R, t_san - 0.2, t_mil1 - 0.2, "san_agustin", "SAN AGUSTÍN", "abajo", 46)
    ga(R, P2.castillo_san_marcos(), CI["san_agustin"], t_fun - 0.1, t_mil1 - 0.2, s=0.56, off=(0, -20), sem=71, zs=0.5, z=2, entra="pluma",
       d_in=1.0, extra=[(0.05, "crece", 0.45)])
    pa(R, P1.menendez(0, "serio"), 300, 1010, 1.05, t_esp - 0.1, t_mil1 - 0.1, sem=72, extra=[(0.05, "fanfarria", 0.3)])
    pa(R, P1.fraile_franciscano(0, "feliz"), 560, 1010, 0.96, t_fun - 0.1, t_mil1 - 0.1, sem=73, flip=True)
    pa(R, P2.bandera_borgona(), 1620, 1010, 0.95, t_esp, t_mil1 - 0.1, sem=74, entra="sube", dy=320)
    R.texto(t_flo - 0.3, t_mil1 - 0.2, "LA CIUDAD EUROPEA MÁS ANTIGUA DE EE. UU.", (960, 196), px=56, d=0.8)

    # frase 1: Jamestown (1607) y el tabaco
    andar(R, lambda p: P2.barco_ingles(p), M.RUTAS["ingleses_jamestown"], t_mil1 - 0.3, 3.0, t1=t_enr, s=0.42, sem=75, zs=0.4, z=3, fps=4)
    ciudad(R, t_jam - 0.2, t_poc - 0.2, "jamestown", "JAMESTOWN", "abajo", 46)
    ga(R, P2.fuerte_jamestown(), CI["jamestown"], t_lev - 0.1, t_poc + 0.2, s=0.54, off=(0, -20), sem=76, zs=0.5, z=2, entra="pluma", d_in=1.0,
       extra=[(0.05, "crece", 0.45)])
    for k, dx in enumerate((-260, 250)):
        ga(R, P2.planta_tabaco(), CI["jamestown"], t_enr - 0.1 + 0.15 * k, t_mil2, s=0.40, off=(dx, 40), sem=77 + k, zs=0.45, z=1, entra="sube",
           dy=240)
    pa(R, P1.colono_jamestown(0, "feliz"), 300, 1010, 1.02, t_ing - 0.1, t_poc - 0.1, sem=79)
    pa(R, P1.plantador_tabaco(0, "feliz"), 560, 1010, 0.98, t_cul := W(1, "cultivando"), t_poc - 0.1, sem=80, flip=True)
    pa(R, P2.barril_tabaco(), 1620, 1010, 0.86, t_tab - 0.2, t_poc - 0.1, sem=81, entra="sube", dy=300, extra=[(0.05, "monedas", 0.4)])
    R.texto(t_tab, t_poc - 0.2, "TABACO", (1620, 730), px=46, d=0.35)
    lugar(R, t_vir - 0.2, t_poc - 0.2, "VIRGINIA", (-78.4, 37.6), off=(0, 0), px=48)

    # frase 2: 1619, los primeros africanos esclavizados; 1620, el Mayflower y los peregrinos
    andar(R, lambda p: P2.barco_ingles(p), M.RUTAS["esclavos"], t_poc - 0.2, 2.8, t1=t_mil2, s=0.40, sem=82, zs=0.4, z=3, fps=4)
    ciudad(R, t_afr - 0.2, t_mil2, "point_comfort", "POINT COMFORT", "der", 38)
    pa(R, P1.africano_esclavizado(0, "serio"), 320, 1010, 1.02, t_afr - 0.15, t_mil2 + 0.2, sem=83)
    pa(R, P1.africano_esclavizado(1, "lloron"), 580, 1010, 0.96, t_esc - 0.1, t_mil2 + 0.2, sem=84, flip=True)
    pa(R, P2.cadenas_rotas(), 1580, 990, 0.8, t_esc - 0.1, t_mil2 + 0.2, sem=85, extra=[(0.05, "clink", 0.4)])
    R.texto(t_esc, t_mil2 + 0.1, "1619: LA ESCLAVITUD", (960, 196), px=62, d=0.5)
    andar(R, lambda p: P2.mayflower(p), M.RUTAS["mayflower"], t_mil2 - 0.1, 3.0, t1=t_cos, s=0.46, sem=86, zs=0.4, z=3, fps=4)
    R.snd(t_may - 0.2, "ola", 0.4, dur=1.2)
    ciudad(R, t_may, t_cos - 0.1, "plymouth", "PLYMOUTH", "abajo", 44)
    ga(R, P2.cabana_troncos(), CI["plymouth"], t_tra := W(2, "trae"), t_cos - 0.1, s=0.40, off=(-200, 30), sem=87, zs=0.45, z=2, entra="sube", dy=240)
    titulo(R, t_may - 0.2, t_cos - 0.2, "EL MAYFLOWER (1620)", px=78)
    pa(R, P1.peregrino(0, "feliz"), 1360, 1010, 1.0, t_may, t_cos, sem=88)
    pa(R, P1.peregrina(0, "feliz"), 1620, 1010, 0.96, t_per - 0.2, t_cos, sem=89, flip=True)

    # frase 3: trece colonias británicas entre Nueva Francia y Nueva España
    for k, (c, txt) in enumerate((("boston", "BOSTON"), ("nueva_york", "NUEVA YORK"), ("filadelfia", "FILADELFIA"), ("charleston", "CHARLESTON"))):
        ciudad(R, t_tre + 0.3 + 0.2 * k, FIN(e) + 0.3, c, txt, "der", 32)
    pa(R, P1.colono_jamestown(1, "feliz"), 300, 1010, 0.98, t_cos - 0.2, t_bri - 0.3, sem=93)
    pa(R, P2.cabana_troncos(), 600, 1000, 0.7, t_cos, t_bri - 0.3, sem=94, entra="sube", dy=240)
    R.terreno(t_tre - 0.1, "trece", COL["colonias"], 1.2)
    R.snd(t_tre, "whoosh", 0.45, dur=0.8)
    R.contador(t_tre - 0.1, t_bri + 0.3, 1, 13, (960, 196), px=82, formato="{} COLONIAS", hasta_t=t_rod - 0.2)
    R.sello(t_cos - 0.3, "barco", "TRECE COLONIAS", color=(196, 70, 62))
    R.terreno(t_fra - 0.2, "nueva_francia", COL["francia"], 1.0, capa=2)
    R.terreno(t_esp3 - 0.2, "nueva_espana", COL["espana"], 1.0, capa=1)
    lugar(R, t_fra, FIN(e) + 0.3, "NUEVA FRANCIA", (-92.0, 43.5), off=(0, 0), px=46)
    lugar(R, t_esp3, FIN(e) + 0.3, "NUEVA ESPAÑA", (-104.0, 31.0), off=(0, 0), px=46)
    pa(R, P2.bandera_britanica(), 320, 1010, 0.92, t_bri - 0.2, FIN(e) + 0.3, sem=90, entra="sube", dy=300)
    pa(R, P2.bandera_francia_real(), 1330, 1010, 0.92, t_fra - 0.1, FIN(e) + 0.3, sem=91, entra="sube", dy=300)
    pa(R, P2.bandera_borgona(), 1610, 1010, 0.92, t_esp3 - 0.1, FIN(e) + 0.3, sem=92, entra="sube", dy=300)
    titulo(R, t_rod - 0.1, FIN(e) + 0.2, "ENTRE FRANCIA Y ESPAÑA", px=70, y=320)


# ------------------------------------------------------------------ REVOLUCIÓN
def _revolucion(R):
    e = "revolucion"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_ven, t_lon, t_imp, t_bos, t_arr, t_te = W(0, "vencer"), W(0, "londres"), W(0, "impuestos"), W(0, "boston"), W(0, "arrojan"), W(0, "te")
    t_mil1, t_sue, t_dis, t_lex, t_emp, t_ind = W(1, "mil"), W(1, "suenan"), W(1, "disparos"), W(1, "lexington"), W(1, "empieza"), W(1, "independencia")
    t_cua, t_fir, t_dec, t_tho, t_jef = W(2, "cuatro"), W(2, "firman"), W(2, "declaracion"), W(2, "thomas"), W(2, "jefferson")
    t_geo, t_eje, t_ayu, t_fra, t_ber, t_gal = W(3, "george"), W(3, "ejercito"), W(3, "ayuda"), W(3, "francia"), W(3, "bernardo"), W(3, "galvez")
    t_mil4, t_bri, t_york, t_nace, t_pais = W(4, "mil"), W(4, "britanicos"), W(4, "yorktown"), W(4, "nace"), W(4, "pais")

    # cámara: costa este -> Boston -> Lexington -> Filadelfia -> vista de la guerra (de Nueva York al Golfo) -> Yorktown -> el país nuevo
    para(R, i0 - 0.9, t_imp + 0.3, -76.5, 41.0, 2.2)
    foco(R, t_bos - 0.5, t_cua - 0.8, (-71.15, 42.40), 6.0)
    foco(R, t_cua, t_geo - 0.7, CI["filadelfia"], 6.4)
    para(R, t_geo + 0.6, t_mil4 - 0.5, -81.0, 35.0, 1.5)
    foco(R, t_mil4 + 0.7, t_nace - 0.6, CI["yorktown"], 5.4)
    para(R, t_nace + 0.4, FIN(e) + 0.6, -84.0, 38.5, 1.2)

    # años
    R.anio(i0 + 0.1, 1763)
    R.anio(t_bos, 1773)
    R.anio(t_mil1, 1775)
    R.anio(t_cua, 1776)
    R.anio(t_mil4 + 0.2, 1781)
    R.anio(t_nace, 1783)

    # frase 0: tras la guerra franco-india Francia pierde Nueva Francia; impuestos de Londres; el motín del té
    R.terreno(t_ven - 0.1, "canada", COL["inglaterra"], 1.2, capa=2)
    R.snd(t_ven, "crujido", 0.35, dur=0.8)
    pa(R, P2.bandera_francia_real(), 1620, 1010, 0.9, i0, t_lon + 0.2, sem=100, sale="encoger")
    pa(R, P1.rey_jorge(0, "enojo"), 300, 1010, 1.05, t_lon - 0.15, t_bos + 0.2, sem=101, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_lon, t_bos, "LONDRES", (300, 600), px=44, d=0.35)
    pa(R, P2.sello_timbre(), 960, 820, 0.8, t_imp - 0.2, t_bos + 0.2, sem=102, entra="cae", dy=300, extra=[(0.05, "sello", 0.6)])
    R.texto(t_imp, t_bos, "IMPUESTOS", (960, 560), px=56, d=0.4)
    pa(R, P2.corona_britanica(), 1620, 900, 0.7, t_imp, t_bos + 0.2, sem=103, extra=[(0.05, "monedas", 0.35)])
    andar(R, lambda p: P2.barco_ingles(p), M.RUTAS["barcos_te"], i0 + 0.2, 3.6, t1=t_mil1, s=0.40, sem=104, zs=0.4, z=2, fps=4)
    ciudad(R, t_bos - 0.2, t_mil1, "boston", "BOSTON", "izq", 46)
    for k, (dx, dy) in enumerate(((120, 70), (210, 120), (310, 90))):
        ga(R, P2.cofre_te(), CI["boston"], t_arr + 0.15 * k, t_mil1, s=0.30, off=(dx, dy), sem=105 + k, zs=0.4, z=3, entra="cae", dy=260,
           extra=[(0.1, "plop", 0.45)])
    pa(R, P1.miliciano(0, "enojo"), 300, 1010, 1.0, t_arr - 0.1, t_mil1 + 0.1, sem=108)
    pa(R, P2.cofre_te(), 600, 1010, 0.8, t_arr, t_mil1 + 0.1, sem=109, entra="sube", dy=280)
    titulo(R, t_arr - 0.2, t_mil1 - 0.1, "EL MOTÍN DEL TÉ (1773)", px=78)

    # frase 1: Lexington (1775), primeros disparos
    ciudad(R, t_lex - 0.2, t_cua - 0.2, "lexington", "LEXINGTON", "abajo", 46)
    grupo(R, lambda p: P1.casaca_roja(p % 2, "enojo"), [(-71.06, 42.36), (-71.17, 42.42), (-71.23, 42.45)], t_mil1 - 0.1, 3.0, n=3, ancho=90,
          t1=t_cua - 0.2, s=0.40, sem=110, fps=6)
    R.snd(t_mil1, "tambor", 0.4)
    pa(R, P1.miliciano(1, "enojo"), 300, 1010, 1.04, t_sue - 0.1, t_cua - 0.1, sem=113)
    pa(R, P1.miliciano(0, "serio"), 560, 1010, 0.98, t_pri := W(1, "primeros"), t_cua - 0.1, sem=114, flip=True)
    pa(R, P1.casaca_roja(0, "enojo"), 1620, 1010, 1.04, t_sue, t_cua - 0.1, sem=115, flip=True)
    ga(R, A.estallido(), CI["lexington"], t_dis - 0.1, t_emp + 0.3, s=0.46, off=(0, -40), sem=116, zs=0.4, z=4, extra=[(0.0, "canonazo", 0.5)])
    titulo(R, t_emp - 0.2, t_cua - 0.2, "GUERRA DE INDEPENDENCIA", px=80)
    R.sello(t_ind, "campana_lib", "LA REVOLUCIÓN", color=(70, 100, 172))

    # frase 2: 4 de julio de 1776, la Declaración de Jefferson
    ciudad(R, t_cua, t_geo - 0.2, "filadelfia", "FILADELFIA", "abajo", 46)
    ga(R, P2.salon_independencia(), CI["filadelfia"], t_cua - 0.1, t_geo - 0.2, s=0.58, off=(0, -20), sem=120, zs=0.5, z=2, entra="pluma",
       d_in=1.0, extra=[(0.05, "crece", 0.45)])
    titulo(R, t_cua - 0.1, t_dec - 0.1, "4 DE JULIO DE 1776", px=82)
    pa(R, P2.declaracion(), 1180, 1000, 0.9, t_fir - 0.2, t_geo, sem=121, entra="sube", dy=340, extra=[(0.05, "papel", 0.5)])
    titulo(R, t_dec - 0.1, t_geo - 0.2, "DECLARACIÓN DE INDEPENDENCIA", px=72)
    pa(R, P1.jefferson(0, "feliz"), 310, 1010, 1.05, t_tho - 0.15, t_geo + 0.1, sem=122, extra=[(0.05, "escribir", 0.45, {"dur": 0.9})])
    pa(R, P2.pluma_tintero(), 560, 1000, 0.7, t_jef, t_geo + 0.1, sem=123)
    pa(R, P2.campana_libertad(), 1620, 1000, 0.9, t_fir, t_geo + 0.1, sem=124, entra="sube", dy=320, extra=[(0.1, "campana", 0.5)])
    R.terreno(t_fir, "trece", COL["eeuu"], 1.4)

    # frase 3: Washington y el Ejército Continental, con Francia y Bernardo de Gálvez
    pa(R, P1.washington(0, "serio"), 300, 1010, 1.08, t_geo - 0.15, t_mil4 + 0.1, sem=130, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_geo + 0.1, t_eje, "GEORGE WASHINGTON", (300, 590), px=40, d=0.4)
    grupo(R, lambda p: P1.soldado_continental(p % 2, "enojo"), M.RUTAS["washington_sur"], t_eje - 0.2, 3.6, n=3, ancho=80, t1=t_mil4,
          s=0.36, sem=131, fps=6)
    R.snd(t_eje, "tambor", 0.4)
    R.texto(t_eje + 0.2, t_ayu + 0.2, "EJÉRCITO CONTINENTAL", (300, 590), px=40, d=0.4)
    pa(R, P1.soldado_frances_rev(0, "serio"), 1340, 1010, 1.0, t_fra - 0.15, t_mil4 + 0.1, sem=134)
    andar(R, lambda p: P2.barco_ingles(p), M.RUTAS["flota_francia"], t_fra - 0.2, 3.0, t1=t_mil4 + 0.6, s=0.38, sem=135, zs=0.4, z=2, fps=4)
    R.texto(t_fra, t_mil4, "FRANCIA", (1340, 590), px=42, d=0.35)
    pa(R, P1.galvez(0, "serio"), 1620, 1010, 1.04, t_ber - 0.15, t_mil4 + 0.1, sem=136, flip=True, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_gal - 0.1, t_mil4, "BERNARDO DE GÁLVEZ", (1600, 590), px=38, d=0.4)
    R.ruta(M.RUTAS["galvez"], t_ber - 0.2, 1.6, ancho=5.0, t1=t_mil4 + 0.2, flecha=True)
    ciudad(R, t_gal - 0.2, t_mil4 + 0.2, "pensacola", "PENSACOLA", "abajo", 38)
    ciudad(R, t_ber - 0.2, t_mil4 + 0.2, "nueva_orleans", "NUEVA ORLEANS", "izq", 34)
    ga(R, A.espadas(), CI["pensacola"], t_gal, t_mil4 + 0.2, s=0.36, off=(0, -60), sem=137, zs=0.35, z=4, extra=[(0.05, "espada", 0.45)])

    # frase 4: Yorktown (1781), los británicos se rinden; nace un país nuevo (Tratado de París, 1783)
    ciudad(R, t_york - 0.3, t_nace - 0.2, "yorktown", "YORKTOWN", "abajo", 46)
    ga(R, P2.canon_rev(), CI["yorktown"], t_mil4, t_nace - 0.2, s=0.44, off=(-160, 20), sem=140, zs=0.45, z=2, entra="sube", dy=240,
       extra=[(0.1, "canonazo", 0.45)])
    ga(R, P2.bandera_13(), CI["yorktown"], t_bri, t_nace - 0.2, s=0.44, off=(170, 0), sem=141, zs=0.45, z=2, entra="sube", dy=240)
    pa(R, P1.casaca_roja(1, "lloron"), 1620, 1010, 1.02, t_bri - 0.1, t_nace, sem=142, flip=True)
    R.texto(t_rin := W(4, "rinden"), t_nace - 0.1, "RENDICIÓN", (1620, 600), px=46, d=0.35)
    R.terreno(t_nace - 0.1, "eeuu_1783", COL["eeuu"], 1.3)
    R.terreno(t_nace - 0.1, "espana_1783", COL["espana"], 1.3, capa=1)
    R.snd(t_nace - 0.1, "whoosh", 0.45, dur=0.9)
    pa(R, P2.bandera_13(), 960, 1010, 1.1, t_nace - 0.1, FIN(e) + 0.3, sem=143, entra="sube", dy=380, extra=[(0.05, "fanfarria", 0.45)])
    titulo(R, t_pais - 0.2, FIN(e) + 0.2, "NACE UN PAÍS NUEVO", px=86)
    lugar(R, t_pais, FIN(e) + 0.2, "ESTADOS UNIDOS", (-81.0, 39.6), off=(0, 0), px=46)
