# -*- coding: utf-8 -*-
"""Coreografía (2/4): la república (Constitución de Filadelfia y los tres poderes, Washington primer presidente, trece estados bajo
una bandera), el Oeste (compra de Luisiana, Lewis y Clark, el Sendero de Lágrimas, Texas y la guerra con México, la fiebre del oro)
y la Guerra Civil (norte industrial y sur algodonero, Lincoln y la Confederación, Fort Sumter, Emancipación y Gettysburg, Appomattox,
asesinato de Lincoln y fin de la esclavitud).
Capas: 0 = EE. UU., 1 = España / México, 2 = Unión / norte, 3 = destacados (Luisiana, cherokees, lo perdido en 1848, Confederación)."""
import mapa as M
import obj_a as A
import obj_us1 as P1
import obj_us2 as P2
import obj_us3 as P3
from core import FIN, INI, T
from coreo_util import CI, COL, andar, ciudad, foco, ga, grupo, lugar, pa, para, titulo, tramo


def cortes(R):
    pass


def construir(R):
    _republica(R)
    _oeste(R)
    _civil(R)


# ------------------------------------------------------------------ REPÚBLICA
def _republica(R):
    e = "republica"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_fil, t_red, t_con, t_rep, t_pre, t_cong, t_tri = (W(0, "filadelfia"), W(0, "redactan"), W(0, "constitucion"), W(0, "reparte"),
                                                        W(0, "presidente"), W(0, "congreso"), W(0, "tribunales"))
    t_mil, t_was, t_jur, t_pri, t_nue = W(1, "mil"), W(1, "washington"), W(1, "jura"), W(1, "primer"), W(1, "nueva")
    t_tre, t_est, t_uni, t_ban, t_bar = W(2, "trece"), W(2, "estados"), W(2, "unidos"), W(2, "bandera"), W(2, "barras")

    # cámara: Filadelfia -> Nueva York (Federal Hall, 1789) -> los trece estados
    foco(R, i0 - 0.8, t_mil - 0.5, CI["filadelfia"], 6.0)
    foco(R, t_mil + 0.4, t_tre - 0.6, CI["nueva_york"], 6.2)
    para(R, t_tre + 0.2, FIN(e) + 0.6, -77.5, 37.8, 2.2)

    R.anio(i0 + 0.1, 1787)
    R.anio(t_mil, 1789)
    R.anio(t_tre, 1790)

    # frase 0: la Constitución y los tres poderes
    ciudad(R, t_fil - 0.2, t_pre - 0.3, "filadelfia", "FILADELFIA", "abajo", 46)
    ga(R, P2.salon_independencia(), CI["filadelfia"], i0 - 0.1, t_pre - 0.3, s=0.56, off=(0, -20), sem=200, zs=0.5, z=2, entra="sube", dy=280)
    pa(R, P2.constitucion(), 1250, 1010, 1.0, t_red - 0.2, t_rep + 0.2, sem=201, entra="sube", dy=360, extra=[(0.05, "papel", 0.5)])
    pa(R, P2.pluma_tintero(), 980, 1000, 0.7, t_red, t_rep + 0.2, sem=202, extra=[(0.05, "escribir", 0.45, {"dur": 0.9})])
    titulo(R, t_con - 0.2, t_pre - 0.2, "LA CONSTITUCIÓN (1787)", px=82)
    R.sello(t_con, "estrellas13", "LA REPÚBLICA", color=(62, 88, 150))
    for k, (dib, x, tt, txt) in enumerate(((P3.casa_blanca(), 380, t_pre, "PRESIDENTE"), (P3.capitolio(), 960, t_cong, "CONGRESO"),
                                          (P3.monumento_lincoln(), 1540, t_tri, "TRIBUNALES"))):
        pa(R, dib, x, 1010, 0.86, tt - 0.25, t_mil, sem=203 + k, entra="sube", dy=320, extra=[(0.05, "pluck", 0.4)])
        R.texto(tt - 0.1, t_mil - 0.1, txt, (x, 640), px=46, d=0.35)
    titulo(R, t_pre - 0.2, t_mil - 0.2, "TRES PODERES", px=80)

    # frase 1: 1789, Washington primer presidente
    ciudad(R, t_mil, t_tre - 0.2, "nueva_york", "NUEVA YORK", "abajo", 46)
    pa(R, P1.washington(0, "feliz"), 330, 1010, 1.1, t_was - 0.2, t_tre, sem=210, extra=[(0.05, "fanfarria", 0.4)])
    pa(R, P2.bandera_13(), 600, 1010, 0.9, t_jur - 0.1, t_tre, sem=211, entra="sube", dy=300)
    pa(R, A.multitud(8, 3), 1440, 1010, 1.5, t_jur, t_tre, sem=212, entra="sube", dy=260, extra=[(0.05, "brillo", 0.3)])
    titulo(R, t_pri - 0.2, t_tre - 0.2, "EL PRIMER PRESIDENTE", px=80)
    ga(R, P2.campana_libertad(), CI["nueva_york"], t_jur, t_tre - 0.2, s=0.36, off=(200, 20), sem=213, zs=0.4, z=2, extra=[(0.1, "campana", 0.4)])

    # frase 2: trece estados unidos bajo una bandera
    R.terreno(t_tre - 0.2, "trece", COL["eeuu"], 0.6, capa=3)
    R.romper("estados", t_tre - 0.1, t_est + 0.3, t_uni - 0.2, t_uni + 0.6, capa=3, gap=14.0, deriva=22.0, fijas=(0,))
    R.snd(t_tre, "crujido", 0.4, dur=0.8)
    R.terreno(FIN(e) + 0.2, None, COL["eeuu"], 0.4, capa=3)
    R.contador(t_tre - 0.1, t_est + 0.4, 1, 13, (960, 196), px=82, formato="{} ESTADOS", hasta_t=t_ban - 0.2)
    pa(R, P2.bandera_13(), 960, 1010, 1.18, t_ban - 0.2, FIN(e) + 0.3, sem=214, entra="sube", dy=380, extra=[(0.05, "fanfarria", 0.4)])
    titulo(R, t_ban - 0.1, FIN(e) + 0.2, "BARRAS Y ESTRELLAS", px=82)


# ------------------------------------------------------------------ EL OESTE
def _oeste(R):
    e = "oeste"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_mil0, t_nap, t_luis, t_qui, t_dup, t_tam = W(0, "mil"), W(0, "napoleon"), W(0, "luisiana"), W(0, "quince"), W(0, "duplica"), W(0, "tamano")
    t_lew, t_cru, t_roc, t_lle, t_pac = W(1, "lewis"), W(1, "cruzan"), W(1, "rocosas"), W(1, "llegar"), W(1, "pacifico")
    t_exp, t_arr, t_nat, t_mil2, t_che, t_sen = W(2, "expansion"), W(2, "arrasa"), W(2, "nativos"), W(2, "miles"), W(2, "cherokees"), W(2, "sendero")
    t_ane, t_tex, t_gue, t_mex, t_mil3, t_mit = W(3, "anexar"), W(3, "texas"), W(3, "guerra"), W(3, "mexico"), W(3, "mil"), W(3, "mitad")
    t_ese, t_oro, t_cal, t_mil4, t_bus, t_cont = W(4, "ese"), W(4, "oro"), W(4, "california"), W(4, "miles"), W(4, "buscadores"), W(4, "continente")

    LC = M.RUTAS["lewis_clark"]

    # cámara: Luisiana entera -> la ruta de Lewis y Clark hasta el Pacífico -> sureste cherokee -> Texas y México -> California
    para(R, i0 - 0.8, t_dup + 0.4, -95.0, 39.0, 0.92)
    para(R, t_lew - 0.1, t_cru, -97.0, 44.4, 1.7)
    R.camara(t_roc + 0.3, -108.0, 46.5, 1.8)
    para(R, t_pac - 0.2, t_pac + 0.6, -121.0, 46.0, 2.6)
    para(R, t_exp + 0.5, t_sen + 0.6, -89.5, 36.0, 2.3)
    para(R, t_ane + 0.2, t_mit + 0.8, -104.0, 33.0, 1.05)
    foco(R, t_oro - 0.4, t_mil4 - 0.3, CI["coloma"], 4.4)
    para(R, t_bus, FIN(e) + 0.6, -110.0, 40.0, 1.4)

    R.anio(i0 + 0.1, 1803)
    R.anio(t_lew, 1804)
    R.anio(t_pac, 1805)
    R.anio(t_exp, 1830)
    R.anio(t_sen, 1838)
    R.anio(t_tex, 1845)
    R.anio(t_gue, 1846)
    R.anio(t_mil3 + 0.3, 1848)
    R.anio(t_bus, 1849)

    # frase 0: Napoleón vende Luisiana por 15 millones y el país duplica su tamaño
    R.terreno(i0 - 0.3, "mexico_1824", COL["espana"], 0.8, capa=1)
    R.terreno(i0 - 0.2, "luisiana_1803", COL["francia"], 0.9, capa=3)
    pa(R, P1.napoleon(0, "serio"), 300, 1010, 1.05, t_nap - 0.15, t_dup + 0.2, sem=220, extra=[(0.05, "fanfarria", 0.32)])
    R.texto(t_nap + 0.1, t_dup, "NAPOLEÓN", (300, 600), px=44, d=0.35)
    lugar(R, t_luis - 0.2, t_lew - 0.3, "LUISIANA", (-98.5, 41.5), off=(0, 0), px=56)
    pa(R, P2.bolsa_dolares(), 1600, 1010, 0.9, t_qui - 0.2, t_dup + 0.3, sem=221, entra="cae", dy=320, extra=[(0.05, "monedas", 0.5)])
    R.contador(t_qui - 0.2, t_qui + 0.8, 0, 15, (960, 196), px=84, formato="{} MILLONES DE $", hasta_t=t_dup - 0.1)
    R.terreno(t_dup - 0.2, "eeuu_1803", COL["eeuu"], 1.2)
    R.terreno(t_dup - 0.1, None, COL["francia"], 0.8, capa=3)
    R.snd(t_dup - 0.2, "whoosh", 0.5, dur=0.9)
    titulo(R, t_dup - 0.1, t_lew - 0.2, "EL PAÍS SE DUPLICA", px=84)

    # frase 1: Lewis y Clark, de San Luis al Pacífico
    R.ruta(LC, t_lew - 0.2, 3.6, ancho=5.0, t1=t_exp - 0.2, flecha=True)
    andar(R, lambda p: P2.canoa_lc(p), tramo(LC, LC[0], (-101.27, 47.30)), t_lew - 0.1, 2.0, t1=t_roc + 0.2, s=0.36, sem=222, zs=0.4, z=3, fps=4)
    grupo(R, lambda p: P1.lewis(p % 2, "feliz"), tramo(LC, (-101.27, 47.30), LC[-1]), t_roc - 0.3, 2.4, n=2, ancho=80, t1=t_exp - 0.2,
          s=0.36, sem=223, fps=6)
    R.snd(t_roc - 0.2, "pasos", 0.35, dur=1.6)
    andar(R, lambda p: P2.bisonte(p), [(-104.5, 47.3), (-107.5, 46.6)], t_roc - 0.4, 2.6, t1=t_exp - 0.2, s=0.38, sem=225, zs=0.4, z=2, fps=5)
    ga(R, P2.tipi(), (-106.0, 45.6), t_roc, t_exp - 0.2, s=0.34, off=(0, 0), sem=226, zs=0.4, z=1, entra="sube", dy=200)
    pa(R, P1.lewis(0, "feliz"), 290, 1010, 1.02, t_lew - 0.15, t_exp - 0.1, sem=227)
    pa(R, P1.clark(0, "feliz"), 540, 1010, 1.0, t_lew + 0.2, t_exp - 0.1, sem=228, flip=True)
    pa(R, P1.sacagawea(0, "serio"), 1630, 1010, 1.0, t_roc - 0.1, t_exp - 0.1, sem=229, flip=True)
    titulo(R, t_lew - 0.1, t_roc - 0.2, "LEWIS Y CLARK", px=82)
    R.sello(t_cru, "carreta", "EL OESTE", color=(196, 132, 70))
    ciudad(R, t_pac - 0.4, t_exp - 0.2, "astoria", "FUERTE CLATSOP", "der", 34)
    lugar(R, t_pac - 0.2, t_exp - 0.2, "¡EL PACÍFICO!", (-125.2, 44.6), off=(0, 0), px=48)

    # frase 2: la expansión arrasa a los nativos; el Sendero de Lágrimas cherokee
    R.terreno(t_exp - 0.2, "eeuu_1819", COL["eeuu"], 1.0)
    R.terreno(t_exp - 0.1, "cherokee", COL["cherokee"], 0.8, capa=3)
    ciudad(R, t_che - 0.3, t_ane - 0.2, "new_echota", "NEW ECHOTA", "abajo", 38)
    ciudad(R, t_sen, t_ane - 0.2, "tahlequah", "TERRITORIO INDIO", "abajo", 38)
    R.ruta(M.RUTAS["sendero_lagrimas"], t_che - 0.3, 2.6, ancho=5.0, t1=t_ane - 0.2, flecha=True)
    grupo(R, lambda p: P1.cherokee(p % 2, "lloron"), M.RUTAS["sendero_lagrimas"], t_che - 0.2, 3.6, n=3, ancho=80, t1=t_ane - 0.2, s=0.36,
          sem=230, fps=4)
    R.terreno(t_sen - 0.1, "territorio_indio", COL["territorio_indio"], 1.2, capa=3)
    R.snd(t_sen, "viento", 0.35, dur=1.6)
    pa(R, P1.cherokee(0, "lloron"), 300, 1010, 1.02, t_arr - 0.1, t_ane - 0.1, sem=233)
    pa(R, P1.cherokee(1, "serio"), 560, 1010, 0.96, t_nat - 0.1, t_ane - 0.1, sem=234, flip=True)
    R.contador(t_mil2 - 0.2, t_che + 0.6, 0, 4000, (960, 196), px=78, formato="~{:,} MUERTOS", hasta_t=t_sen - 0.2)
    titulo(R, t_sen - 0.1, t_ane - 0.2, "SENDERO DE LÁGRIMAS (1838)", px=74)

    # frase 3: Texas (1845), guerra con México (1846-1848): México pierde la mitad de su territorio
    R.terreno(t_ane - 0.3, None, COL["cherokee"], 0.5, capa=3)
    R.terreno(t_ane - 0.2, "mexico_1824", COL["mexico"], 0.9, capa=1)
    R.terreno(t_tex - 0.1, "eeuu_1845", COL["eeuu"], 1.0)
    R.terreno(t_tex - 0.1, "mexico_1836", COL["mexico"], 1.0, capa=1)
    R.snd(t_tex, "whoosh", 0.4, dur=0.8)
    ciudad(R, t_tex - 0.1, t_ese - 0.2, "alamo", "EL ÁLAMO", "abajo", 38)
    ga(R, P2.el_alamo(), CI["alamo"], t_tex - 0.1, t_ese - 0.2, s=0.40, off=(0, -30), sem=240, zs=0.4, z=2, entra="sube", dy=240)
    lugar(R, t_tex, t_gue, "TEXAS", (-99.0, 31.4), off=(0, 0), px=52)
    R.ruta(M.RUTAS["kearny"], t_gue - 0.2, 2.2, ancho=5.0, t1=t_ese - 0.3, flecha=True)
    grupo(R, lambda p: P1.soldado_eeuu_1846(p % 2, "enojo"), M.RUTAS["kearny"], t_gue - 0.2, 3.0, n=2, ancho=80, t1=t_ese - 0.3, s=0.34,
          sem=241, fps=6)
    andar(R, lambda p: P2.caballo_us(p), M.RUTAS["taylor_sur"], t_gue, 2.6, t1=t_ese - 0.3, s=0.34, sem=243, zs=0.4, z=2, fps=6)
    R.snd(t_gue, "galope", 0.4, dur=1.4)
    pa(R, P1.soldado_eeuu_1846(0, "enojo"), 300, 1010, 1.0, t_gue - 0.15, t_ese - 0.1, sem=244)
    pa(R, P1.soldado_mexicano_1846(0, "enojo"), 1620, 1010, 1.0, t_mex - 0.15, t_ese - 0.1, sem=245, flip=True)
    ga(R, A.estallido(), (-99.5, 26.5), t_gue + 0.1, t_mil3, s=0.36, off=(0, 0), sem=246, zs=0.35, z=4, extra=[(0.05, "canonazo", 0.4)])
    R.terreno(t_mit - 0.3, "eeuu_1846", COL["eeuu"], 1.1)
    R.terreno(t_mit - 0.3, "mexico_mod", COL["mexico"], 1.1, capa=1)
    R.terreno(t_mit - 0.3, "perdido_1848", COL["perdido"], 1.0, capa=3)
    R.terreno(t_ese, None, COL["perdido"], 0.6, capa=3)
    R.snd(t_mit - 0.3, "crujido", 0.5, dur=0.9)
    pa(R, P2.tratado_1848(), 960, 1000, 0.9, t_mil3 - 0.1, t_ese, sem=247, entra="sube", dy=320, extra=[(0.05, "sello", 0.5)])
    titulo(R, t_mit - 0.2, t_ese - 0.2, "MÉXICO PIERDE LA MITAD DE SU TERRITORIO", px=60)
    lugar(R, t_mit, t_ese - 0.2, "OREGÓN", (-120.0, 44.0), off=(0, 0), px=40)

    # frase 4: oro en California (1848) y la fiebre del oro
    ciudad(R, t_oro - 0.2, t_mil4, "coloma", "SUTTER'S MILL", "der", 40)
    ciudad(R, t_cal, t_mil4, "san_francisco", "SAN FRANCISCO", "izq", 36)
    ga(R, P2.batea_oro(), CI["coloma"], t_oro - 0.1, FIN(e) + 0.3, s=0.40, off=(0, -60), sem=250, zs=0.45, z=3, entra="sube", dy=240,
       extra=[(0.05, "bling", 0.5)])
    ga(R, P2.campamento_mineros(), CI["coloma"], t_cal - 0.1, FIN(e) + 0.3, s=0.40, off=(-260, 40), sem=251, zs=0.45, z=1, entra="sube", dy=200)
    pa(R, P1.buscador_oro(0, "feliz"), 300, 1010, 1.04, t_oro - 0.15, FIN(e) + 0.3, sem=252, extra=[(0.05, "monedas", 0.4)])
    pa(R, P2.pico_pala(), 560, 1000, 0.7, t_cal, FIN(e) + 0.3, sem=253)
    titulo(R, t_oro - 0.1, t_mil4, "¡ORO EN CALIFORNIA!", px=84)
    R.ruta(M.RUTAS["fiebre_oro"], t_mil4 - 0.3, 2.0, ancho=5.0, t1=FIN(e) + 0.3, flecha=True)
    for k in range(2):
        andar(R, lambda p: P2.carreta_cubierta(p), M.RUTAS["fiebre_oro"], t_mil4 - 0.2 + 0.5 * k, 3.0, t1=FIN(e) + 0.3, s=0.30, sem=254 + k,
              zs=0.4, z=2, fps=5, off=(0, 40 * k))
    R.contador(t_mil4 - 0.2, t_cont, 0, 300_000, (960, 196), px=78, formato="+{:,} BUSCADORES", hasta_t=FIN(e) + 0.3)
    pa(R, P1.buscador_oro(1, "asombro"), 1620, 1010, 1.0, t_bus - 0.1, FIN(e) + 0.3, sem=256, flip=True)


# ------------------------------------------------------------------ GUERRA CIVIL
def _civil(R):
    e = "civil"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_par, t_nor, t_ind, t_sur, t_pla, t_alg, t_esc = (W(0, "partido"), W(0, "norte"), W(0, "industrial"), W(0, "sur"), W(0, "plantaciones"),
                                                       W(0, "algodon"), W(0, "esclavitud"))
    t_abr, t_gan, t_onc, t_sep, t_conf = W(1, "abraham"), W(1, "gana"), W(1, "once"), W(1, "separan"), W(1, "confederacion")
    t_mil2, t_est, t_gue, t_san = W(2, "mil"), W(2, "estalla"), W(2, "guerra"), W(2, "sangrienta")
    t_lin3, t_lib, t_get, t_uni, t_fre = W(3, "lincoln"), W(3, "libertad"), W(3, "gettysburg"), W(3, "union"), W(3, "frena")
    t_mil4, t_rin, t_lin4, t_ase, t_esc4, t_abo = W(4, "mil"), W(4, "rinde"), W(4, "lincoln"), W(4, "asesinado"), W(4, "esclavitud"), W(4, "abolida")

    # cámara: el este partido -> Fort Sumter -> Washington/Gettysburg -> Appomattox -> el país entero
    para(R, i0 - 1.0, t_sep + 1.0, -86.0, 37.5, 1.25)
    foco(R, t_mil2 + 0.2, t_lin3 - 0.4, CI["fort_sumter"], 5.4)
    foco(R, t_lib, t_mil4 - 0.4, CI["gettysburg"], 6.0)
    foco(R, t_mil4 + 0.4, t_lin4 - 0.2, CI["appomattox"], 5.0)
    para(R, t_lin4 + 0.7, FIN(e) + 0.6, -88.0, 38.5, 1.05)

    R.anio(i0 + 0.1, 1850)
    R.anio(t_abr, 1860)
    R.anio(t_mil2, 1861)
    R.anio(t_lin3, 1863)
    R.anio(t_mil4 + 0.2, 1865)

    # frase 0: norte industrial / sur algodonero y esclavista
    R.terreno(i0 - 0.3, None, COL["mexico"], 0.6, capa=1)
    R.terreno(t_nor - 0.1, "norte_industrial", COL["union"], 1.0, capa=2)
    R.terreno(t_sur - 0.1, "algodon", (222, 206, 170), 1.0, capa=3)
    R.snd(t_par, "crujido", 0.45, dur=0.8)
    titulo(R, t_par - 0.1, t_abr - 0.2, "UN PAÍS PARTIDO EN DOS", px=80, y=330)
    ga(R, P3.aceria(), CI["pittsburgh"], t_ind - 0.2, t_abr, s=0.44, off=(0, -20), sem=300, zs=0.45, z=2, entra="sube", dy=260,
       extra=[(0.05, "fuego", 0.35, {"dur": 1.2})])
    ga(R, P3.locomotora_us(1), CI["chicago"], t_ind, t_abr, s=0.32, off=(0, 30), sem=301, zs=0.4, z=2)
    for k, (c, dx) in enumerate((("atlanta", -60), ("vicksburg", 40), ("savannah", 0))):
        ga(R, P2.planta_algodon(), CI[c], t_pla - 0.1 + 0.15 * k, t_abr, s=0.32, off=(dx, 20), sem=302 + k, zs=0.4, z=1, entra="sube", dy=200)
    ga(R, P2.mansion_plantacion(), (-88.0, 32.6), t_pla, t_abr, s=0.40, off=(0, 0), sem=305, zs=0.45, z=2, entra="sube", dy=240)
    pa(R, P1.obrero_ferrocarril(0, "serio"), 300, 1010, 1.0, i0 + 0.1, t_abr, sem=306)
    R.texto(t_ind, t_abr - 0.1, "NORTE INDUSTRIAL", (300, 600), px=38, d=0.4)
    pa(R, P1.esclava_algodon(0, "lloron"), 1620, 1010, 1.02, t_alg - 0.15, t_abr, sem=307, flip=True)
    pa(R, P2.fardo_algodon(), 1360, 1000, 0.72, t_alg, t_abr, sem=308, entra="sube", dy=260)
    R.texto(t_esc - 0.1, t_abr - 0.1, "SUR ESCLAVISTA", (1500, 600), px=38, d=0.4)

    # frase 1: Lincoln gana; once estados del sur forman la Confederación
    pa(R, P1.lincoln(0, "serio"), 310, 1010, 1.12, t_abr - 0.15, t_mil2 + 0.2, sem=310, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_abr + 0.1, t_onc, "ABRAHAM LINCOLN", (310, 560), px=40, d=0.4)
    pa(R, P2.bandera_union(), 600, 1010, 0.9, t_gan - 0.1, t_mil2 + 0.2, sem=311, entra="sube", dy=300)
    R.terreno(t_onc - 0.2, "union", COL["union"], 1.0, capa=2)
    R.terreno(t_onc - 0.2, "confederacion", COL["confederacion"], 1.0, capa=3)
    R.romper("estados", t_onc - 0.1, t_onc + 0.6, t_conf - 0.3, t_conf + 0.4, capa=3, gap=12.0, deriva=26.0, fijas=(0,))
    R.snd(t_sep, "crujido", 0.5, dur=0.9)
    R.contador(t_onc - 0.2, t_sep, 1, 11, (960, 196), px=82, formato="{} ESTADOS", hasta_t=t_conf - 0.2)
    titulo(R, t_conf - 0.2, t_mil2 - 0.1, "LA CONFEDERACIÓN", px=84)
    pa(R, P1.soldado_confederado(0, "enojo"), 1620, 1010, 1.0, t_sep - 0.1, t_mil2 + 0.2, sem=312, flip=True)

    # frase 2: 1861, Fort Sumter: estalla la Guerra Civil
    ciudad(R, t_mil2, t_lin3 - 0.2, "fort_sumter", "FORT SUMTER", "der", 44)
    ga(R, P2.canon_civil(), CI["fort_sumter"], t_mil2, t_lin3 - 0.2, s=0.44, off=(-190, 20), sem=315, zs=0.45, z=2, entra="sube", dy=240)
    ga(R, A.estallido(), CI["fort_sumter"], t_est - 0.1, t_gue + 0.6, s=0.50, off=(0, -30), sem=316, zs=0.4, z=4, extra=[(0.0, "canonazo", 0.55)])
    pa(R, P1.soldado_union(0, "enojo"), 300, 1010, 1.04, t_est - 0.15, t_lin3, sem=317)
    pa(R, P1.soldado_confederado(1, "enojo"), 1620, 1010, 1.04, t_est, t_lin3, sem=318, flip=True)
    pa(R, P2.tambor_militar(), 600, 1000, 0.7, t_gue - 0.1, t_lin3, sem=319, extra=[(0.05, "tambor", 0.4)])
    titulo(R, t_gue - 0.2, t_san - 0.1, "GUERRA CIVIL (1861-1865)", px=80)
    R.sello(t_gue, "canones", "GUERRA CIVIL", color=(110, 116, 128))
    R.contador(t_san - 0.2, t_san + 0.8, 0, 620_000, (960, 196), px=76, formato="+{:,} MUERTOS", hasta_t=t_lin3 - 0.1)

    # frase 3: Emancipación y Gettysburg
    pa(R, P1.lincoln(0, "feliz"), 310, 1010, 1.1, t_lin3 - 0.15, t_get, sem=320)
    pa(R, P2.declaracion(), 640, 1000, 0.72, t_lin3 + 0.1, t_get, sem=321, extra=[(0.05, "papel", 0.45)])
    pa(R, P1.liberto(0, "feliz"), 1620, 1010, 1.02, t_lib - 0.15, t_get + 0.2, sem=322, flip=True, extra=[(0.05, "clink", 0.45)])
    R.texto(t_lib, t_get - 0.1, "EMANCIPACIÓN (1863)", (960, 196), px=74, d=0.5)
    ciudad(R, t_get - 0.2, t_mil4, "gettysburg", "GETTYSBURG", "abajo", 46)
    grupo(R, lambda p: P1.soldado_confederado(p % 2, "enojo"), M.RUTAS["lee_gettysburg"][-3:], t_get - 0.3, 1.8, n=3, ancho=80, t1=t_mil4,
          s=0.36, sem=323, fps=6)
    grupo(R, lambda p: P1.soldado_union(p % 2, "enojo"), M.RUTAS["union_gettysburg"], t_get - 0.2, 1.6, n=3, ancho=80, t1=t_mil4, s=0.36,
          sem=326, fps=6)
    ga(R, P2.tienda_campana(), CI["gettysburg"], t_uni, t_mil4, s=0.36, off=(-260, 40), sem=329, zs=0.4, z=1, entra="sube", dy=200)
    ga(R, A.espadas(), CI["gettysburg"], t_fre - 0.1, t_mil4, s=0.36, off=(0, -80), sem=330, zs=0.35, z=4, extra=[(0.05, "espada", 0.45)])
    pa(R, P1.soldado_union(0, "feliz"), 310, 1010, 1.02, t_get + 0.1, t_mil4 + 0.1, sem=331)
    titulo(R, t_fre - 0.2, t_mil4 - 0.1, "LA UNIÓN FRENA AL SUR", px=78)

    # frase 4: 1865, rendición en Appomattox, Lincoln asesinado, esclavitud abolida
    ciudad(R, t_mil4, t_lin4 - 0.1, "appomattox", "APPOMATTOX", "abajo", 44)
    pa(R, P1.soldado_confederado(0, "lloron"), 1620, 1010, 1.0, t_mil4, t_lin4, sem=332, flip=True)
    pa(R, P2.bandera_union(), 330, 1010, 0.95, t_mil4 - 0.1, t_lin4 - 0.1, sem=336, entra="sube", dy=300)
    R.texto(t_rin - 0.1, t_lin4 - 0.1, "EL SUR SE RINDE", (960, 196), px=74, d=0.45)
    R.terreno(t_rin, None, COL["confederacion"], 1.0, capa=3)
    R.terreno(t_rin, None, COL["union"], 1.0, capa=2)
    R.terreno(t_rin, "eeuu_1846", COL["eeuu"], 0.8)
    R.snd(t_rin, "whoosh", 0.45, dur=0.8)
    pa(R, P1.lincoln(0, "serio"), 310, 1010, 1.1, t_lin4 - 0.15, FIN(e) + 0.3, sem=333)
    R.texto(t_ase - 0.2, FIN(e) + 0.2, "ASESINADO (1865)", (310, 560), px=40, d=0.4)
    R.snd(t_ase - 0.1, "impacto", 0.4)
    pa(R, P2.cadenas_rotas(), 1000, 990, 0.9, t_esc4 - 0.2, FIN(e) + 0.3, sem=334, entra="sube", dy=300, extra=[(0.05, "clink", 0.5)])
    pa(R, P1.liberto(1, "feliz"), 1620, 1010, 1.04, t_esc4 - 0.1, FIN(e) + 0.3, sem=335, flip=True)
    titulo(R, t_abo - 0.3, FIN(e) + 0.2, "FIN DE LA ESCLAVITUD", px=84)
