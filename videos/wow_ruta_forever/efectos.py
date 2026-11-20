# -*- coding: utf-8 -*-
"""EFECTOS de «La RUTA del 1 al 60 en WoW Forever, zona por zona» (19-nov-2026; helpers de wow_oro_forever).
Por parada: tarjeta R.parada (nucleo/mg_ruta.py, NUEVO) + mapa real de la zona con la ruta (coordenadas de `_coords.md`, Wowhead Forever)
+ pegatinas (pegatinas/_creditos.json) + comentarios (com). MG nuevos: parada, curva_xp, bifurcacion. SIN Overgear.
python fab.py wow_ruta_forever fx --seco · FAB_FX_FINAL=1 python fab.py wow_ruta_forever fx hoja"""
import os

import mg_tes as T
import mg_wow as M
import peg_estilos as PE
import mg_ruta as R

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
TEMA_PEG = "wow"
AMAR, ROJO, VERDE, BLANCO, NAR = (255, 255, 160), (255, 70, 60), (40, 210, 90), (240, 240, 240), (255, 150, 60)
V, GR, RJ = "verde", "gris", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    if slug.startswith("o_"):
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6):
    xs = (.14, .32, .50, .68, .86)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    if slug.startswith("o_"):   # íconos de 56 px: más chicos, que no se vean borrosos (regla 10-nov)
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    if slug.startswith("o_"):   # ícono entero, sin el zoom de cara (recortado se veía como una mancha borrosa, 15-nov)
        foco = (.5, .5, 1.0)
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420, foco=(.5, .25, 2.0)):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, foco=foco, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def sil(en, slug, nombre, sub=None, dur=4.4, lado="izq", alto=820, marco="museo"):
    # PERSONAS REALES = OPACAS (el usuario, 10-nov-2026): PE.silueta recortaba con rembg y la foto de Michel Koiter salía
    # translúcida, fundida con el gameplay. Ahora retrato con marco opaco a media pantalla (antes PE.silueta).
    return pv(en, slug, nombre, dur=dur, x=(.25 if lado == "izq" else .75), y=.50, tam=640,
              marco=marco, estancia="kenburns")


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.5, zmin=1.0):
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.60, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel([(F(s), n) for s, n in fotos], tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus((F(a_[0]), a_[1]), (F(b_[0]), b_[1]), ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def P(x, y, rot, sub=None, foto=None):
    return (x, y, rot, sub, F(foto) if foto else None)


CAMARA = {}
FUNDIDO = {}


def W(px, py):
    """Píxel de mapas/mundo_forever.jpg (4080×3187) -> % de mapas/mundo_forever_ancho.jpg (5666×3187: el mismo con 793 px de
    mar a cada lado, para que en 16:9 no se corten Zephras, Cuna del Invierno ni Bahía del Botín; revisión visual 19-nov)."""
    return round((px + 793) / 56.66, 1), round(py / 31.87, 1)


def par(n, a, b, titulo, ali, hor, de, dur=6.5):
    """Tarjeta de capítulo de la parada n (tramo a-b): sale al decir «Parada…»."""
    return dict(tipo="mg", fn=R.parada(n, a, b, titulo, ali, hor), en=(de, -.2), dur=dur, x=.5, y=.40, sale=.4,
                nombre=f"MG parada {n}", ver=1.0, marcas=[(de, .3), (de, 1.6), (de, 2.8)])


MUNDO = [W(2082, 728), W(3073, 2510), W(3460, 2357), W(3295, 1691), W(865, 2160), W(3499, 1400), W(3138, 2976), W(3770, 2204),
         W(415, 1810), W(1022, 2363), W(1098, 1068), W(3530, 2252), W(1131, 699), W(906, 912)]
NOM = ["1 · Isla Zephras", "2 · Páramos", "3 · Crestagrana", "4 · Los Humedales", "5 · Mil Agujas", "6 · Arathi", "7 · Tuercespina",
       "8 · Claros del Río", "9 · Shen'dralas", "10 · Tanaris", "11 · Azshara", "12 · Estepas", "13 · Cuna del Invierno", "14 · Hyjal"]

FX = [
    # ====================================================================== GANCHO
    dict(tipo="mg", fn=PE.banda(F("claros_rio"), "CLAROS DEL RÍO", "151 misiones nuevas · del 36 al 47", foco=(.5, .55, 1.3), alto=380, tema="wow"),
         en=("Una zona nueva con ciento cincuenta y una", -.1), dur=4.6, x=.5, y=.78, sale=.3, nombre="banda claros", ver=1.0),
    pv("Un Monte Hyjal que no empieza en el sesenta", "monte_hyjal", "Monte Hyjal · desde el 53", dur=4.0, x=.78, y=.45, tam=520),
    mg(R.bifurcacion("LA ALIANZA Y LA HORDA YA NO SUBEN IGUAL", "CLAROS DEL RÍO",
                     ("ALIANZA · a pie", ["Villa del Lago", "Fortaleza de Farholde"]), ("HORDA · en barco", ["muelle de Tanaris", "Puerto Polvomecha"])),
       ("Y algo que nadie te avisa", -.2), ("en barco desde el otro continente|fin", 1.0),
       [("Y algo que nadie te avisa", .3), "Unos llegan a la zona nueva caminando", ("Unos llegan a la zona nueva caminando", 1.3),
        "y los otros, casi siempre", ("y los otros, casi siempre", 1.4)], "bifurcación gancho", y=.52),
    mg(R.curva_xp("EXPERIENCIA PARA LLEGAR AL 60", [(1, 0), (10, 27600), (20, 167200), (30, 499000), (40, 1154400), (50, 2306100),
                                                   (60, 4084700)], (30, 60), "88 %"),
       ("Llegar al sesenta pide cuatro millones", -.2), ("está entre el treinta y el sesenta|fin", 1.4),
       [("Llegar al sesenta pide", .3 + .4 * k) for k in range(7)] + ["Y el ochenta y ocho por ciento"], "curva xp", y=.52),
    mapa("mundo_forever_ancho", [P(x, y, n) for (x, y), n in zip(MUNDO, NOM)], ("Por eso hoy te traigo la ruta completa", -.2),
         ("qué es nuevo de Forever en ese tramo|fin", .3),
         [("Por eso hoy te traigo la ruta completa", .4 + 1.0 * k) for k in range(14)], "AZEROTH", "las 14 paradas", zmax=1.15),
    com("Y antes de empezar, un consejo de un espectador", "Ugzg4tbBsFWYqJdHkdp4AaABAg", dur=9.0, x=.32, y=.30),
    # ====================================================================== P1 · 1-10
    par(1, 1, 10, "LAS ZONAS INICIALES", ["Elwynn · Dun Morogh", "Teldrassil · Isla Zephras"], ["Durotar · Mulgore", "Tirisfal · Isla Zephras"],
        "Parada uno. Del nivel uno al diez"),
    mapa("elwynn", [P(49.4, 41.3, "Abadía de Villanorte", None, "abadia_villanorte"), P(42.4, 66.6, "Villadorada", "posada", None)],
         ("Cada raza empieza en su valle", -.2), ("baja a su primer pueblo con posada|fin", .5),
         [("Cada raza empieza en su valle", .3), "hacia el nivel cinco o seis"], "BOSQUE DE ELWYNN", "Alianza · humanos"),
    filav("Los humanos bajan a Villadorada", [("kharanos", "Kharanos · Dun Morogh", "Y los enanos y gnomos, a Kharanos"),
                                               ("dolanaar", "Dolanaar · Teldrassil", "Los elfos de la noche, a Dolanaar")], y=.62, tam=300, dur=4.5),
    filav("En la Horda, los orcos y los trols", [("cerrotajo", "Cerrotajo · Durotar", "bajan del Valle de los Retos a Cerrotajo"), ("pezuna_sangre", "Pezuña de Sangre · Mulgore", "Los taurens, al Poblado"),
                                                ("remol", "Rémol · Tirisfal", "Y los renegados, a Rémol")], y=.62, tam=270, dur=4.0),
    mapa("zephras", [P(42.2, 23.5, "Poblado Thendal", None, "zephras_torre"), P(43.4, 45.1, "Aldea Shen'dar", "posada", "zephras_pueblo"),
                     P(63.2, 77.5, "Valanaar", "posada", "zephras_valanaar"), P(63.2, 85.6, "Muelles Celestiales", "dirigibles a Dalaran y Cima del Trueno", None)],
         ("Y la novedad de Forever es la séptima salida", -.2), ("y los de la Horda a Cima del Trueno|fin", .3),
         [("Y la novedad de Forever es la séptima salida", .4), "donde empiezan los cielonatos", "Es la zona inicial que más dura",
          "Los cielonatos salen hacia el trece"], "ISLA ZEPHRAS", "cielonatos · del 3 al 12"),
    pv("donde empiezan los cielonatos", "cielonato", "Cielonato", dur=4.2, x=.80, y=.52, tam=480),
    mg(M.contadores("MISIONES NUEVAS EN LAS ZONAS DE SIEMPRE", [("inv_misc_book_09", "Elwynn y Ventormenta", 100, 0, 1),
                                                           ("inv_misc_book_09", "Mulgore, Durotar, Dun Morogh", 50, 1, 2)], ("más de cien · unas cincuenta", 2)),
       ("Pero las zonas de siempre también cambiaron", -.2), ("unas cincuenta cada una|fin", .4),
       ["tiene más de cien misiones nuevas", "y Mulgore, Durotar", "unas cincuenta cada una"], "misiones nuevas iniciales", y=.56),
    mapa("tirisfal", [P(61.0, 52.7, "Rémol", "Shari Stilwell · nivel 8", "shari_stilwell"), P(21.8, 46.1, "Fuerte de Bandarion", "subzona nueva", "fuerte_bandarion")],
         ("Y si eres renegado, en Tirisfal", -.2), ("con Shari Stilwell, en Rémol|fin", .4),
         [("Y si eres renegado, en Tirisfal", .4), "el Fuerte de Bandarion"], "CLAROS DE TIRISFAL", "Horda · renegados"),
    rel("Hogger sigue siendo nivel once", "hogger", "Hogger", "nivel 11 · siempre", dur=4.6, x=.74),
    # ====================================================================== P2 · 10-15
    par(2, 10, 15, "EL PRIMER CAMBIO DE ZONA", ["Páramos · Loch Modan", "Costa Oscura"], ["Los Baldíos", "Bosque de Argénteos"],
        "Parada dos. Del diez al quince", dur=4.6),
    mapa("paramos", [P(56.8, 47.3, "Colina del Centinela", "posada y vuelo", None)],
         ("En la Alianza, los humanos bajan a los Páramos", -.2), ("Ahí tienes posada y maestro de vuelo|fin", .3), [],
         "PÁRAMOS DE PONIENTE", "Alianza · 10-18"),
    mapa("loch_modan", [P(35.0, 46.8, "Thelsamar", "posada y vuelo", None)], ("Los enanos y gnomos van a Loch Modan", -.2),
         ("a Thelsamar|fin", 1.2), [], "LOCH MODAN", "Alianza"),
    mapa("costa_oscura", [P(38.6, 43.4, "Auberdine", "posada y vuelo", None)], ("toman el barco a Costa Oscura", -.6),
         ("con centro en Auberdine|fin", .3), [], "COSTA OSCURA", "Alianza · elfos"),
    mapa("baldios", [P(52.1, 30.6, "El Cruce", "posada y vuelo", None)],
         ("En la Horda, orcos, trols y taurens se juntan", -.2), ("Y los renegados bajan al Bosque", -.2), [],
         "LOS BALDÍOS", "Horda · 10-25"),
    mapa("argenteos", [P(43.6, 41.4, "El Sepulcro", "posada y vuelo", None)], ("Y los renegados bajan al Bosque de Argénteos", -.2),
         ("a El Sepulcro|fin", .4), [], "BOSQUE DE ARGÉNTEOS", "Horda · renegados"),
    pv("El Salón de Señores Feudales", "salon_senores_feudales", "El Salón de Señores Feudales · 13-18", dur=5.0, x=.74, y=.50, tam=620),
    pv("las Ruinas de Lordaeron, del quince al veinte", "ruinas_lordaeron", "Ruinas de Lordaeron · bajo Entrañas", dur=5.0, x=.26, y=.50, tam=620),
    cam(("mucho más grande que la Sima Ígnea", -1.0), "ruinas_lordaeron_carga", "5 misiones nuevas", dur=3.2, x=.86, y=.24, tam=260),
    mapa("paramos", [P(56.8, 47.3, "Colina del Centinela", None, None), P(43.0, 69.3, "Arroyo de la Luna", None, None),
                     P(38.2, 77.5, "Minas de la Muerte", "entrada", "minas_muerte")],
         ("En los Páramos, de la Colina", -.4), ("a la entrada de las Minas de la Muerte|fin", .5),
         [("En los Páramos, de la Colina", .2), "al Arroyo de la Luna", "a la entrada de las Minas de la Muerte"], "PÁRAMOS DE PONIENTE", "la ruta"),
    # ====================================================================== P3 · 15-20
    par(3, 15, 20, "CRESTAGRANA Y SIERRA ESPOLÓN", ["Montañas Crestagrana", "Vallefresno (elfos)"], ["sur de Los Baldíos", "Sierra Espolón"],
        "Parada tres. Del quince al veinte"),
    pv("con centro en Villa del Lago, junto al lago", "villa_del_lago", "Villa del Lago", dur=4.4, x=.76, y=.52, tam=560),
    mapa("baldios", [P(52.1, 30.6, "El Cruce", None, None), P(44.8, 58.7, "Campamento Taurajo", None, None)],
         ("La Horda baja al sur de Los Baldíos", -.2), ("y de ahí sube a Sierra Espolón", 0.0),
         [("La Horda baja al sur de Los Baldíos", .3), "al Campamento Taurajo"], "LOS BALDÍOS", "Horda · hacia el sur"),
    mapa("crestagrana", [P(24.0, 45.1, "Villa del Lago", "posada", "villa_del_lago"), P(46.2, 39.7, "Molino de Alther", None, None),
                         P(76.9, 62.7, "Cascadas Petravista", None, None), P(93.8, 21.3, "Avanzada del Sur", "puerta a Claros del Río", None)],
         ("En Crestagrana, la ruta va de Villa del Lago", -.2), ("a la que la Alianza volverá al treinta y seis|fin", .3),
         [("En Crestagrana, la ruta va de Villa del Lago", .4), "al Molino de Alther", "y a las cascadas del este", "ahí está la Avanzada del Sur"],
         "MONTAÑAS CRESTAGRANA", "Alianza · 15-25", zmax=1.3),
    pv("La mazmorra de este tramo, para la Alianza", "minas_muerte", "Las Minas de la Muerte", dur=4.6, x=.74, y=.52, tam=600),
    pv("Para la Horda son las Cuevas de los Lamentos", "cuevas_lamentos", "Cuevas de los Lamentos", dur=4.6, x=.26, y=.52, tam=600),
    # ====================================================================== burla0 (vito_232)
    com("Vito nos escribió esto", "UgxcjgLh03cohbb_bv54AaABAg", dur=8.0, x=.32, y=.30),
    # ====================================================================== P4 · 20-25
    par(4, 20, 25, "OCASO, HUMEDALES, VALLEFRESNO Y LADERAS", ["Bosque del Ocaso", "Los Humedales", "Vallefresno (elfos)"],
        ["Laderas de Trabalomas", "Vallefresno"], "Parada cuatro. Del veinte al veinticinco"),
    mapa("humedales", [P(10.6, 55.3, "Puerto de Menethil", "posada y vuelo", "puerto_menethil"), P(66.8, 47.2, "Refugio Faucedraco", "subzona nueva", None)],
         ("y Los Humedales, con centro", -.2), ("y subzonas nuevas como el Refugio Faucedraco|fin", .4),
         [("y Los Humedales, con centro", .4), "el Refugio Faucedraco"],
         "LOS HUMEDALES", "Alianza · unas 50 misiones nuevas"),
    mapa("vallefresno", [P(36.1, 50.8, "Astranaar", "Alianza · posada y vuelo", None)],
         ("Los elfos de la noche siguen en Vallefresno", -.2), ("con centro en Astranaar|fin", .6),
         [("Los elfos de la noche siguen en Vallefresno", .4)], "VALLEFRESNO", "elfos de la noche"),
    com("alexafm nos escribió", "UgwXpCm7L23FHp1cq9N4AaABAg", dur=9.0, x=.32, y=.32),
    mapa("laderas", [P(61.5, 20.0, "Molino Tarren", "posada y vuelo", None), P(31.8, 36.7, "Campos de Trabalomas", None, None)],
         ("alexafm, esta parada es para ti", -.1), ("y baja a Vallefresno|fin", .3),
         [("alexafm, esta parada es para ti", .5), ("sal de Argénteos hacia el Molino Tarren", .5)], "LADERAS DE TRABALOMAS", "Horda · 20-31"),
    pv("el Castillo de Colmillo Oscuro, en Argénteos", "colmillo_oscuro", "Castillo de Colmillo Oscuro", dur=4.0, x=.26, y=.52, tam=560),
    pv("y las Cavernas de Brazanegra", "brazanegra", "Cavernas de Brazanegra", dur=3.6, x=.74, y=.52, tam=560),
    # ====================================================================== P5 · 25-30
    par(5, 25, 30, "LAS MIL AGUJAS Y LA EXCAVACIÓN", ["Los Humedales", "Mil Agujas (Thalanaar)"], ["Mil Agujas", "Laderas de Trabalomas"],
        "Parada cinco. Del veinticinco al treinta"),
    pv("con centro en el Poblado Viento Libre", "viento_libre", "Poblado Viento Libre", dur=3.6, x=.76, y=.50, tam=560),
    mapa("mil_agujas", [P(45.7, 50.7, "Poblado Viento Libre", "posada y vuelo", "viento_libre"), P(18.6, 22.2, "Campamento E'thok", "centauros", None),
                        P(70.8, 76.7, "El Desierto de Sal", "la pista", None)],
         ("La ruta en Las Mil Agujas baja del poblado", -.2), ("corren los goblins y los gnomos|fin", .4),
         [("La ruta en Las Mil Agujas baja del poblado", .3), "hacia los centauros del oeste", "y termina en el Desierto de Sal"], "LAS MIL AGUJAS", "Horda · 25-35"),
    mapa("humedales", [P(10.6, 55.3, "Puerto de Menethil", None, None), P(38.5, 60.5, "Sitio de Excavación", "mazmorra nueva · 10 misiones", "excavacion_humedales")],
         ("Y aquí está la segunda mazmorra nueva", -.2), ("La Horda las recoge en Sentencia", 0.0),
         [("Y aquí está la segunda mazmorra nueva", .2), ("Y aquí está la segunda mazmorra nueva", 1.4)], "LOS HUMEDALES", "excavación · 24-29"),
    pv("porque está llena de raptores escondidos", "excavacion_humedales_carga", "Sitio de Excavación · raptores", dur=4.6, x=.74, y=.50, tam=620),
    mg(M.contadores("EXPERIENCIA EN MAZMORRAS", [("spell_holy_borrowedtime", "más por muerte en mazmorra (%)", 50, 0, 1)], ("desde el 8 de noviembre", 1)),
       ("Un consejo de este tramo", -.2), ("el ocho de noviembre|fin", 1.0), [("Un consejo de este tramo", .6), "el ocho de noviembre"], "xp mazmorras", y=.56),
    # ====================================================================== P6 · 30-35
    par(6, 30, 35, "ARATHI, ALTERAC Y DESOLACE", ["Arathi · Refugio de la Zaga", "Dalaran · Desolace"], ["Arathi · Sentencia", "Alterac · Desolace"],
        "Parada seis. Del treinta al treinta y cinco"),
    mapa("arathi", [P(46.1, 46.6, "Refugio de la Zaga", "Alianza", "refugio_zaga"), P(73.9, 35.8, "Sentencia", "Horda", "sentencia"),
                    P(68.1, 29.9, "Círculo de Vínculo", None, None), P(69.0, 70.1, "Poblado Secacorteza", "trols", None),
                    P(21.8, 64.6, "Castillo de Stromgarde", None, "stromgarde")],
         ("En las Tierras Altas de Arathi", -.2), ("y el Castillo de Stromgarde|fin", .4),
         [("En las Tierras Altas de Arathi", .4), "el Refugio de la Zaga en el centro", "y Sentencia al este", "los círculos de vínculo",
          "el poblado de los trols Secacorteza", "y el Castillo de Stromgarde"], "TIERRAS ALTAS DE ARATHI", "los dos bandos · 30-40", zmax=1.3),
    com("Rubén nos escribió que le encanta", "Ugw0lVoQLKUBXnJ9jtN4AaABAg", dur=12.0, x=.32, y=.32),
    pv("Dalaran vuelve a su sitio", "dalaran", "Dalaran · en su sitio", dur=5.0, x=.74, y=.50, tam=640),
    mapa("alterac", [P(16.7, 68.8, "Ciudad de Dalaran", "mazmorra nueva · 28-33", "dalaran_mazmorra")],
         ("Y tiene mazmorra nueva: la Ciudad de Dalaran", -.2), ("de nivel treinta y tres para los dos bandos|fin", .3), [], "MONTAÑAS DE ALTERAC", "6 misiones de nivel 33"),
    mapa("desolace", [P(65.1, 8.3, "Punta de Nijel", "Alianza", None), P(25.3, 70.4, "Aldea Cazasombras", "Horda", None),
                      P(49.3, 60.1, "Cementerio de Kodos", None, None)],
         ("En Kalimdor, toca Desolace", -.2), ("el Cementerio de Kodos|fin", .4),
         [("En Kalimdor, toca Desolace", .4), "y la Horda en Aldea Cazasombras", "el Cementerio de Kodos"], "DESOLACE", "los dos bandos · 30-39"),
    mapa("tirisfal", [P(85.1, 31.4, "Monasterio Escarlata", "desde el 31", None)], ("Y si quieres otra mazmorra", -.2),
         ("con su cementerio al treinta y uno|fin", .4), [], "CLAROS DE TIRISFAL", "mazmorra"),
    # ====================================================================== P7 · 35-40
    par(7, 35, 40, "TUERCESPINA, EL MARJAL Y TIERRAS INHÓSPITAS", ["Vega de Tuercespina", "Marjal (Theramore)"], ["Vega (Grom'Gol)", "Kargath · Rocal"],
        "Parada siete. Del treinta y cinco al cuarenta"),
    mapa("tuercespina", [P(38.2, 3.5, "Asentamiento Rebelde", "Alianza", None), P(31.9, 28.4, "Campamento Grom'Gol", "Horda", "gromgol"),
                         P(36.1, 11.3, "Expedición de Nesingwary", None, None), P(45.5, 9.0, "Base de Kurzen", None, None),
                         P(31.9, 50.5, "Arena Gurubashi", None, "arena_gurubashi"), P(27.2, 75.6, "Bahía del Botín", "los dos bandos", "bahia_botin")],
         ("En la Vega, la Alianza entra por", -.2), ("en los conjuntos JcJ|fin", .3),
         [("En la Vega, la Alianza entra por", .4), "y la Horda por el Campamento Grom'Gol", "La ruta pasa por la Expedición de Nesingwary",
          "la base de Kurzen", "y la Arena Gurubashi", ("y la Arena Gurubashi", 1.2)], "VEGA DE TUERCESPINA", "30-44", zmax=1.35),
    pv("En el Marjal Revolcafango, la Alianza tiene", "theramore", "Isla Theramore", dur=6.4, x=.14, y=.62, tam=340),
    pv("la Horda tiene Kargath", "kargath", "Kargath", dur=3.0, x=.32, y=.62, tam=340),
    mapa("tuercespina_oeste", [P(47.6, 28.4, "Grom'Gol", None, None), P(47.6, 50.5, "Arena Gurubashi", None, None),
                               P(16.6, 50.6, "La Ciudad Anegada", "mazmorra nueva · 35-40", "ciudad_anegada")],
         ("Y aquí está la tercera mazmorra nueva", -.2), ("frente a la costa oeste de la Vega|fin", .4),
         [("Y aquí está la tercera mazmorra nueva", .3), ("Y aquí está la tercera mazmorra nueva", 1.0), "Una ciudad trol hundida"],
         "VEGA DE TUERCESPINA", "mar adentro"),
    pv("Tiene ocho misiones: la Horda las recoge", "ciudad_anegada_2", "La Ciudad Anegada · 8 misiones", dur=5.0, x=.74, y=.50, tam=620),
    mg(R.bifurcacion("AL 38, LA RUTA DE FOREVER SE SEPARA", "nivel 38",
                     ("RUTA DE CLASSIC", ["Vega · Marjal", "Tierras Inhóspitas"]), ("RUTA DE FOREVER", ["Claros del Río", "Shen'dralas"])),
       ("Y de Grom'Gol sale también la misión", -.2), ("se separa de la de Classic|fin", 1.2),
       [("Y de Grom'Gol sale también la misión", .3 + .7 * k) for k in range(3)] + [("Porque al treinta y ocho", .2), ("Porque al treinta y ocho", .9)],
       "bifurcación 38", y=.52),
    # ====================================================================== burla1 (SolidNano)
    com("SolidNano nos escribió", "UgzeW9YY3FTee9_o3tl4AaABAg", dur=8.5, x=.32, y=.30),
    # ====================================================================== P8 · Claros del Río
    par(8, 36, 45, "CLAROS DEL RÍO, LA ZONA NUEVA", ["a pie desde Villa del Lago", "Fortaleza de Farholde"], ["en barco desde Tanaris", "Rog'mar"],
        "Parada ocho. Del treinta y seis al cuarenta y cinco"),
    ban("En inglés se llama Riverglades", "claros_rio_2", "CLAROS DEL RÍO", "Riverglades · zona disputada", dur=5.0, foco=(.45, .62, 1.2)),
    mg(M.contadores("CLAROS DEL RÍO", [("inv_misc_book_09", "misiones nuevas", 151, 0, 1), ("inv_misc_groupneedmore", "para los dos bandos", 108, 1, 2)],
                    ("del 36 al 47", 2)),
       ("Tiene ciento cincuenta y una misiones nuevas", -.2), ("sirven para los dos bandos|fin", 1.0),
       [("Tiene ciento cincuenta y una", .4), "Y ciento ocho de ellas", ("sirven para los dos bandos", .6)], "contador claros", y=.56),
    mapa("crestagrana", [P(24.0, 45.1, "Villa del Lago", "salida", "villa_del_lago")], ("La Alianza entra a pie", -.4),
         ("hasta las puertas de Las Estepas Ardientes|fin", .3), [], "MONTAÑAS CRESTAGRANA", "Alianza · a pie"),
    mapa("riverglades", [P(28.7, 62.4, "Colinas Espinosas", None, None), P(64.4, 83.0, "Fortaleza de Farholde", "Alianza · posada y vuelo", "farholde")],
         ("En el poste de los letreros", -.2), ("en una isla del sureste|fin", .4),
         [("En el poste de los letreros", .3), "cruza las Colinas Espinosas", "hasta la Fortaleza de Farholde"], "CLAROS DEL RÍO", "Alianza"),
    mapa("tanaris", [P(51.2, 27.5, "Gadgetzan", None, "gadgetzan"), P(68.6, 23.0, "muelle", "barco a Claros del Río", None)],
         ("La Horda llega en barco", -.2), ("hasta el Puerto Polvomecha", -.5), [("La Horda llega en barco", .3), "desde un muelle al este de Gadgetzan"],
         "TANARIS", "Horda · en barco"),
    mapa("riverglades", [P(78.9, 55.2, "Puerto Polvomecha", "sin vuelo", "polvomecha"), P(59.6, 45.9, "Rog'mar", "vuela a Rocal · Kargath · Estepas · Arathi", None)],
         ("hasta el Puerto Polvomecha", -.4), ("Y desde Farholde, la Alianza vuela", -.3),
         [("hasta el Puerto Polvomecha", .2), ("corre por la carretera hasta Rog'mar", .3)], "CLAROS DEL RÍO", "Horda"),
    mapa("riverglades", [P(59.6, 64.4, "Avanzada de Terral", None, "avanzada_terral"), P(47.3, 47.9, "Claro Soleado", None, None),
                         P(28.7, 42.8, "Sudario Crepuscular", None, None), P(65.1, 18.0, "Pedreg'ok", "ogros aliados de la Horda", "pedregok"),
                         P(48.6, 26.3, "Bastión de Krol'dok", "mazmorra · 40-45", "kroldok")],
         ("La ruta va por la Avanzada de Terral", -.2), ("con once misiones|fin", .4),
         [("La ruta va por la Avanzada de Terral", .3), "el Claro Soleado", "el Sudario Crepuscular", "y Pedreg'ok", "Y al norte está la mazmorra nueva"],
         "CLAROS DEL RÍO", "la ruta · 36-47", zmax=1.35),
    pv("Hazla una vez, entre el cuarenta y dos", "kroldok", "Bastión de Krol'dok · 11 misiones", dur=5.0, x=.74, y=.50, tam=640),
    pv("Y otro dato: en Claros del Río hay tres lagos", "claros_rio_4", "Claros del Río · lagos", dur=5.0, x=.26, y=.50, tam=640),
    rel("Los que ya la hicieron lo resumen así", "claros_rio_3", "Claros del Río", "del 40 al 44", dur=5.0, x=.76),
    # ====================================================================== gracias1
    com("Sakaan nos escribió", "UgwXsmRwZJY4ZQ40oyF4AaABAg", dur=9.5, x=.30, y=.30),
    com("Y Mateo, que lleva dieciocho años", "UgwV9WDZX-h0qFrmest4AaABAg", dur=8.0, x=.68, y=.34),
    # ====================================================================== P9 · Shen'dralas
    par(9, 38, 45, "SHEN'DRALAS, LA OTRA ZONA NUEVA", ["solo misiones neutrales"], ["Orgrul y Nerlokh", "dos campamentos propios"],
        "Parada nueve. Del treinta y ocho al cuarenta y cinco"),
    mapa("desolace", [P(25.3, 70.4, "Aldea Cazasombras", None, None), P(60.5, 90.2, "Valle de los Huesos", "entrada a Shen'dralas", "valle_huesos")],
         ("Está entre Desolace, Feralas y Mulgore", -.2), ("al sur de Desolace|fin", .4),
         [("Está entre Desolace, Feralas y Mulgore", .4), "y se entra a pie por el Valle de los Huesos"], "DESOLACE", "la entrada"),
    mapa("shendralas", [P(24.9, 25.7, "Valle de los Huesos", None, None), P(35.8, 12.8, "Orgrul", "Horda", "orgrul"),
                        P(21.0, 22.6, "Nerlokh", "Horda", "nerlokh")],
         ("Sus misiones van del treinta y ocho", -.2), ("que se sepa, ninguno|fin", .4),
         [("Sus misiones van del treinta y ocho", .3), "con Orgrul", "y Nerlokh"], "SHEN'DRALAS", "38-49"),
    mapa("shendralas", [P(24.9, 25.7, "Valle de los Huesos", None, None), P(32.9, 45.1, "Mirador de Sombrapar", None, None),
                        P(62.2, 54.9, "Frente Magram", "centauros", None), P(70.3, 72.0, "Jardines Desolados", None, None),
                        P(35.0, 46.4, "Mordent Evenshade", "shen'dralar", None)],
         ("La ruta baja del Valle de los Huesos", -.2), ("te espera en el centro de la zona|fin", .4),
         [("La ruta baja del Valle de los Huesos", .3), "al Mirador de Sombrapar", "hasta el Frente Magram", "a los Jardines Desolados", "Mordent Evenshade"],
         "SHEN'DRALAS", "la ruta"),
    pv("Un consejo práctico: deja tu piedra de hogar", "shendralas", "Shen'dralas", dur=4.4, x=.76, y=.50, tam=600),
    # ====================================================================== burla2 (josejuanandrade)
    com("José Juan nos escribió", "UgynxzVDSKhJG6jsks54AaABAg", dur=9.0, x=.32, y=.32),
    # ====================================================================== P10 · 40-48
    par(10, 40, 48, "TANARIS, FERALAS, TIERRAS DEL INTERIOR", ["Tanaris · Plumaluna", "Pico Nidal"], ["Tanaris · Mojache", "Sañadiente"],
        "Parada diez. Del cuarenta al cuarenta y ocho"),
    mg(M.contadores("AL NIVEL 40 (DE ORO)", [("ability_mount_ridinghorse", "Equitación", 100, 0, 1), ("ability_dualwield", "Doble especialización", 50, 1, 2)],
                    ("junta el oro antes", 2)),
       ("Al cuarenta llegan las dos compras grandes", -.2), ("Junta el oro antes de llegar|fin", .8),
       ["la equitación, unos cien de oro", "que cuesta cincuenta", "Junta el oro antes de llegar"], "compras del 40", y=.56),
    mapa("tanaris", [P(51.2, 27.5, "Gadgetzan", "los dos bandos", "gadgetzan"), P(68.6, 23.0, "muelle", "barco a Claros del Río", None)],
         ("En Tanaris, los dos bandos comparten Gadgetzan", -.2), ("el muelle del barco a Claros del Río|fin", .4),
         [("En Tanaris, los dos bandos comparten Gadgetzan", .3), "Y al este está el muelle"], "TANARIS", "40-50"),
    mapa("feralas", [P(31.1, 44.6, "Bastión Plumaluna", "Alianza", "plumaluna"), P(75.2, 43.8, "Campamento Mojache", "Horda", "mojache")],
         ("En Feralas, la Alianza está", -.2), ("en el Campamento Mojache, al este|fin", .4),
         [("En Feralas, la Alianza está", .4), "y la Horda en el Campamento Mojache"], "FERALAS", "40-50"),
    mapa("interior", [P(14.4, 48.0, "Pico Nidal", "Alianza", "pico_nidal"), P(78.3, 79.5, "Poblado Sañadiente", "Horda", None)],
         ("En las Tierras del Interior, la Alianza sube", -.2), ("La ruta acaba en Jintha'Alor", -.1),
         [("En las Tierras del Interior, la Alianza sube", .4), "y la Horda al Poblado Sañadiente"],
         "TIERRAS DEL INTERIOR", "41-49"),
    mapa("tanaris", [P(51.2, 27.5, "Gadgetzan", None, None), P(38.7, 19.9, "Zul'Farrak", "mazmorra · 45-51", "zulfarrak")],
         ("La mazmorra estrella es Zul'Farrak", -.2), ("y otra en Dalaran|fin", .3), [("La mazmorra estrella es Zul'Farrak", .4)], "TANARIS", "Zul'Farrak"),
    carr([("dalaran", "Dalaran · Alianza"), ("cima_trueno_dirigible", "Cima del Trueno · Horda")],
         ("Y eso es un patrón", -.2), ("la Horda tiene lo mismo|fin", .4), ["en Dalaran hay dos archimagos", "Y en Cima del Trueno, la Horda"],
         "MISIONES DE MAZMORRA PARA TODO EL MAPA"),
    # ====================================================================== P11 · 48-52
    par(11, 48, 52, "UN'GORO, AZSHARA Y UNA PRISIÓN", ["Un'Goro · Punta Talrendis", "Alcaz (Theramore)"], ["Un'Goro · Valormok", "Alcaz (el Marjal)"],
        "Seguimos con la siguiente parada"),
    mapa("azshara", [P(11.7, 77.9, "Punta Talrendis", "Alianza", None), P(21.8, 50.0, "Valormok", "Horda", None),
                     P(70.5, 29.3, "Campamento thalassiano", "subzona nueva", None)],
         ("La primera es Azshara renovada", -.2), ("y un campamento de vanguardia thalassiano|fin", .4),
         [("La primera es Azshara renovada", .3), "con la Alianza en Punta Talrendis", "la Horda en Valormok", "y un campamento de vanguardia"],
         "AZSHARA", "unas 60 misiones nuevas"),
    mapa("alcaz_isla", [P(28.6, 50.5, "muelle", "Sargento Ulka · Horda", None), P(61.8, 43.6, "Prisión de Alcaz", "mazmorra nueva · 48-53", "alcaz")],
         ("La segunda es la Prisión de Alcaz", -.2), ("Y hay una neutral en Bahía del Botín|fin", .4),
         [("La segunda es la Prisión de Alcaz", .3), ("La segunda es la Prisión de Alcaz", 1.4)], "ISLA DE ALCAZ", "frente al Marjal · 9 misiones"),
    mapa("ungoro", [P(43.6, 7.2, "Refugio de Marshal", "posada y vuelo", None), P(51.8, 20.9, "Fosas de alquitrán", None, None),
                    P(49.1, 49.3, "El volcán", "Cresta del Penacho en Llamas", "ungoro")],
         ("Y el Cráter de Un'Goro, al cuarenta y ocho", -.2), ("hasta el volcán|fin", .4),
         [("Y el Cráter de Un'Goro, al cuarenta y ocho", .3), "por las fosas de alquitrán", "hasta el volcán"], "CRÁTER DE UN'GORO", "48-55"),
    mapa("pantano", [P(46.0, 53.8, "Rocal", "Horda", None), P(70.0, 52.9, "Templo de Atal'Hakkar", "mazmorra · clase del 50", "atal_hakkar")],
         ("Y El Templo de Atal'Hakkar", -.2), ("con las misiones de clase del cincuenta|fin", .4), [("Y El Templo de Atal'Hakkar", .4)],
         "PANTANO DE LAS PENAS", "mazmorra"),
    # ====================================================================== P12 · 50-55
    par(12, 50, 55, "ESTEPAS, PESTE DEL OESTE Y ROCA NEGRA", ["Vigilia de Morgan", "Campamento del Orvallo"], ["Peñasco Llamarada", "El Baluarte"],
        "Parada doce. Del cincuenta al cincuenta y cinco"),
    mapa("estepas", [P(85.9, 67.6, "Vigilia de Morgan", "Alianza", "vigilia_morgan"), P(65.5, 23.0, "Peñasco Llamarada", "Horda", "penasco_llamarada")],
         ("En Las Estepas Ardientes, los centros", -.2), ("vuela directo a la Vigilia de Morgan|fin", .4),
         [("En Las Estepas Ardientes, los centros", .4), "y la Horda en el Peñasco Llamarada"], "LAS ESTEPAS ARDIENTES", "50-59"),
    mapa("peste_oeste", [P(42.7, 85.3, "Campamento del Orvallo", "Alianza", None), P(26.4, 51.7, "El Baluarte", "Horda · sin vuelo", None)],
         ("En las Tierras de la Peste del Oeste", -.2), ("El Baluarte no tiene maestro de vuelo|fin", .4),
         [("En las Tierras de la Peste del Oeste", .4), "La Horda tiene El Baluarte"], "TIERRAS DE LA PESTE DEL OESTE", "46-57"),
    mapa("estepas", [P(29.5, 36.0, "Montaña Roca Negra", "Profundidades · 52-56", "profundidades_roca_negra"),
                     P(29.0, 29.0, "Franclorn Forjador", "su tumba", "franclorn")],
         ("Y la mazmorra del tramo es una de las más grandes", -.2), ("Solo lo puedes ver estando muerto|fin", .4),
         [("Y la mazmorra del tramo es una de las más grandes", .4), "Franclorn Forjador, sobre su tumba"], "LAS ESTEPAS ARDIENTES", "Roca Negra"),
    mg(M.contadores("ORO EN LAS MISIONES", [("inv_misc_coin_01", "desde el nivel", 48, 0, 1)], ("cambio del 10 de noviembre", 1)),
       ("una buena noticia para la bolsa", -.4), ("gracias a un cambio del diez de noviembre|fin", .8),
       [("una buena noticia para la bolsa", .2), "gracias a un cambio del diez"], "oro misiones", y=.56),
    rel("el Oso espectral", "o_oso_espectral", "Oso espectral", "Legado · nivel 55", dur=4.6, x=.76, tam=340),
    # ====================================================================== gracias2
    com("Lololulu dice que somos", "UgyvqUUzSbC5nw7AN454AaABAg", dur=5.0, x=.30, y=.30),
    com("Massimo nos contó que es su primera vez", "UgxVOLeYJkYITs564314AaABAg", dur=6.0, x=.68, y=.30),
    com("Y Alexander, que con su vida de hoy", "UgzFH0oj7wjPSiJ1a114AaABAg", dur=7.0, x=.32, y=.60),
    com("Y al sargento Sevilla", "UgxOXY1t1FSe_-vN8fF4AaABAg", dur=6.0, x=.68, y=.36),
    # ====================================================================== P13 · 53-58
    par(13, 53, 58, "CUNA DEL INVIERNO, SILITHUS Y PESTE DEL ESTE", ["Vista Eterna · Fuerte Cenarion", "Capilla de la Esperanza"],
        ["Vista Eterna · Fuerte Cenarion", "Capilla de la Esperanza"], "Parada trece. Del cincuenta y tres"),
    mapa("cuna_invierno", [P(61.2, 38.2, "Vista Eterna", "los dos bandos", "vista_eterna"), P(51.2, 27.1, "Aldea Estrella Fugaz", None, None),
                           P(58.7, 51.8, "Mazthoril", "cueva", None), P(58.2, 85.6, "Garganta Negro Rumor", "a Hyjal", None)],
         ("En Cuna del Invierno, el centro es Vista Eterna", -.2), ("y termina en la Garganta Negro Rumor, al sur|fin", .4),
         [("En Cuna del Invierno, el centro es Vista Eterna", .4), "La ruta sube a la Aldea Estrella Fugaz", "baja a la cueva de Mazthoril",
          "y termina en la Garganta Negro Rumor"], "CUNA DEL INVIERNO", "53-60"),
    filav("En Silithus, el centro es el Fuerte Cenarion", [("fuerte_cenarion", "Fuerte Cenarion · Silithus", None),
                                                          ("capilla_esperanza", "Capilla de la Esperanza de la Luz", "la Capilla de la Esperanza")],
          y=.62, tam=340, dur=4.2),
    mapa("azshara", [P(39.6, 32.3, "Bastión Faucenegra", "mazmorra nueva · 55-60", "bastion_faucenegra")],
         ("Y la mazmorra nueva de este tramo es el Bastión Faucenegra", -.2), ("No la confundas con el Bastión", .1), [],
         "AZSHARA", "ciudad furbolg · 8 misiones"),
    pv("es una de las entradas a las Cavernas del Túmulo", "cavernas_tumulo", "Cavernas del Túmulo · 9 de diciembre", dur=5.0, x=.74, y=.50, tam=620),
    mapa("peste_este_forever", [P(71.9, 49.1, "Capilla de la Esperanza de la Luz", "unas 15 misiones nuevas", "capilla_esperanza")],
         ("En la Capilla tienes, además", -.2), ("también rinde más que antes|fin", .4), [], "TIERRAS DE LA PESTE DEL ESTE", "57-60"),
    # ====================================================================== P14 · Hyjal
    par(14, 56, 60, "EL MONTE HYJAL RENOVADO", ["campamento de la Alianza"], ["campamento de la Horda"], "Parada catorce, la última"),
    mg(M.contadores("MONTE HYJAL", [("inv_misc_book_09", "misiones nuevas", 143, 0, 1), ("spell_nature_starfall", "desde el nivel", 53, 1, 2)],
                    ("no hace falta ser 60", 2)),
       ("Sus ciento cuarenta y tres misiones nuevas", -.2), ("y terminar de subir ahí|fin", .6),
       [("Sus ciento cuarenta y tres misiones", .4), "van del cincuenta y tres al sesenta", "O sea, puedes entrar antes"], "contador hyjal", y=.56),
    mapa("cuna_invierno", [P(61.2, 38.2, "Vista Eterna", None, None), P(58.2, 85.6, "Garganta Negro Rumor", "entrada a Hyjal", None)],
         ("Se entra a pie desde Cuna del Invierno", -.2), ("te lleva de vuelta a Vista Eterna|fin", .4),
         [("Se entra a pie desde Cuna del Invierno", .3), "por la Garganta Negro Rumor"], "CUNA DEL INVIERNO", "a Hyjal a pie"),
    pv("La historia es preciosa", "monte_hyjal_2", "Monte Hyjal", dur=5.0, x=.74, y=.50, tam=640),
    mapa("hyjal", [P(59.3, 74.3, "Laderas Maculadas", "vuelo", None), P(53.6, 58.5, "Santuario de Aviana", None, None),
                   P(13.3, 49.9, "Flora Antigua", "campamentos A y H", None), P(78.5, 36.9, "Cima de la Eternidad", None, None)],
         ("La ruta sube de las Laderas Maculadas", -.2), ("y termina en la Cima de la Eternidad|fin", .4),
         [("La ruta sube de las Laderas Maculadas", .3), "al Santuario de Aviana", "cruza a la Flora Antigua", "y termina en la Cima de la Eternidad"],
         "MONTE HYJAL", "53-60"),
    pv("El Bancal del Creador", "bancal_creador", "El Bancal del Creador · 58-60", dur=5.0, x=.74, y=.50, tam=600),
    carr([("cavernas_tumulo_2", "Cavernas del Túmulo · 10"), ("cumbre_hyjal", "Cumbre Hyjal · 20"), ("guarida_onyxia", "Guarida de Onyxia · 40")],
         ("Y al llegar al sesenta", -.2), ("y la Guarida de Onyxia|fin", .6), ["las Cavernas del Túmulo", "la Cumbre Hyjal", "y la Guarida de Onyxia"],
         "LAS BANDAS DEL 9 DE DICIEMBRE"),
    # ====================================================================== CIERRE
    mapa("mundo_forever_ancho", [P(x, y, n) for (x, y), n in zip(MUNDO, NOM)], ("Y esa es la ruta completa", -.2),
         ("Si te quedas con una sola idea", .3), [("Y esa es la ruta completa", .3 + .65 * k) for k in range(14)], "AZEROTH", "del 1 al 60", zmax=1.15),
]



FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="151 MISIONES NUEVAS", en="Tiene ciento cincuenta y una misiones nuevas", dur=2.6, tam=130, color="amarillo", y=.2),
    dict(texto="SIN MAESTRO DE VUELO", en="el Puerto Polvomecha no tiene maestro de vuelo", dur=2.6, tam=120, color="rojo", y=.85),
    dict(texto="DESDE EL 53", en="van del cincuenta y tres al sesenta", dur=2.4, tam=150, color="amarillo", y=.2),
    dict(texto="EL BALUARTE: SIN VUELO", en="El Baluarte no tiene maestro de vuelo", dur=2.6, tam=100, color="rojo", y=.92),
]
SFX = {}
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.26) for e in (
    "Parada uno. Del nivel uno", "Parada dos. Del diez", "Parada tres. Del quince", "Parada cuatro. Del veinte", "Parada cinco. Del veinticinco",
    "Parada seis. Del treinta", "Parada siete. Del treinta y cinco", "Parada ocho. Del treinta y seis", "Parada nueve. Del treinta y ocho",
    "Parada diez. Del cuarenta", "Seguimos con la siguiente parada", "Parada doce. Del cincuenta", "Parada trece. Del cincuenta y tres",
    "Parada catorce, la última")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Por eso hoy te traigo la ruta completa", "Y esa es la ruta completa")]


# ====================================================================== REVISIÓN VISUAL (19-nov-2026): promesas sin apoyo
# (coordenadas de `_coords.md`, todas WHF). Van AL FINAL (regla 13-nov).
FX += [
    mapa("baldios", [P(52.1, 30.6, "El Cruce", None, None), P(62.2, 37.9, "Trinquete", "y al sur", None)],
         ("En Los Baldíos, sube de El Cruce", -.2), ("hacia Trinquete y el sur|fin", -.1),
         [("En Los Baldíos, sube de El Cruce", .3), "hacia Trinquete y el sur"], "LOS BALDÍOS", "Horda · la ruta"),
    mapa("sierra_espolon", [P(47.8, 60.8, "Refugio Roca del Sol", "Horda · posada y vuelo", None)],
         ("y de ahí sube a Sierra Espolón", -.2), ("al Refugio Roca del Sol|fin", .1), [("y de ahí sube a Sierra Espolón", .4)],
         "SIERRA ESPOLÓN", "Horda · 15-27"),
    mapa("bosque_ocaso", [P(74.2, 47.1, "Villa Oscura", "posada y vuelo", None)], ("La Alianza tiene dos caminos", -.1),
         ("y Los Humedales, con centro", -.3), [("el Bosque del Ocaso, con centro", .3)], "BOSQUE DEL OCASO", "Alianza · 18-30"),
    pv("un barco nuevo de Menethil a Costasur", "puerto_menethil", "Barco nuevo desde Menethil", dur=3.8, x=.74, y=.50, tam=560),
    mapa("laderas", [P(61.5, 20.0, "Molino Tarren", "Horda · posada y vuelo", None)], ("La Horda sube a las Laderas", -.2),
         ("con centro en el Molino Tarren|fin", .3), [("La Horda sube a las Laderas", .4)], "LADERAS DE TRABALOMAS", "Horda · 20-31"),
    mapa("vallefresno", [P(74.0, 62.1, "Puesto del Hachazo", "Horda", None), P(12.0, 34.1, "Avanzada de Zoram'gar", "Horda", None)],
         ("O a Vallefresno, al Puesto", -.3), ("y a la Avanzada de Zoram'gar|fin", .3),
         [("O a Vallefresno, al Puesto", .3), "y a la Avanzada de Zoram'gar"], "VALLEFRESNO", "Horda"),
    mapa("feralas", [P(89.5, 46.3, "Thalanaar", "Alianza · entrada", None)], ("Y la Alianza puede entrar por Thalanaar", -.2),
         ("en el borde con Feralas|fin", .2), [("Y la Alianza puede entrar por Thalanaar", .5)], "FERALAS", "borde con Las Mil Agujas"),
    mapa("pantano", [P(46.0, 53.8, "Rocal", "Horda · posada y vuelo", None)], ("Y en el Pantano de las Penas, Rocal", .1),
         ("Y aquí está la tercera mazmorra nueva", 0.0), [("Y en el Pantano de las Penas", .6)], "PANTANO DE LAS PENAS", "Horda"),
    mapa("inhospitas", [P(35.2, 10.3, "Uldaman", "mazmorra · 44-50", None)], ("Y si vas a Uldaman", .2),
         ("es del cuarenta y cuatro al cincuenta|fin", .4), [("Y si vas a Uldaman", .6)], "TIERRAS INHÓSPITAS", "guárdala para más tarde"),
    mapa("riverglades", [P(64.4, 83.0, "Fortaleza de Farholde", "vuela a Villa del Lago · Thelsamar · Morgan", "farholde")],
         ("Y desde Farholde, la Alianza vuela", -.2), ("a Thelsamar y a la Vigilia de Morgan|fin", .1),
         [("Y desde Farholde, la Alianza vuela", .4)], "CLAROS DEL RÍO", "vuelos de la Alianza"),
    mapa("tanaris", [P(51.2, 27.5, "Gadgetzan", None, None), P(68.6, 23.0, "muelle de los goblins", "misiones nuevas", None)],
         ("Y si vienes de Claros del Río, Tanaris", -.2), ("en el muelle de los goblins|fin", .6),
         [("Y si vienes de Claros del Río", .3), "en el muelle de los goblins"], "TANARIS", "el puente con Claros del Río"),
    mapa("frondavil", [P(68.5, 6.1, "Bastión Fauces de Madera", "túnel a Cuna del Invierno", None)], ("No la confundas con el Bastión", -.2),
         ("sitios totalmente distintos|fin", .4), [("el Bastión Fauces de Madera", .3)], "FRONDAVIL", "otro bastión, otro sitio"),
]
ROTULOS += [
    dict(texto="PRIMER 60 · EN 3 DÍAS", en="en algo más de tres días", dur=2.4, tam=120, color="amarillo", y=.2),
    dict(texto="EL MURO DEL 50", en="el famoso muro de los cincuenta", dur=2.4, tam=140, color="amarillo", y=.2),
]

# Densidad (chequeo 19-nov: pegatinas 1,4/min contra 1,8 del canal) → pegatinas en frases que nombran algo y no tenían nada.
FX += [
    cam("escondido bajo Forjaz", "salon_senores_feudales_carga", "bajo Forjaz", dur=3.4, x=.16, y=.66),
    cam("como una ciudad con habitantes", "dalaran_carga", "Dalaran · ciudad viva", dur=3.6, x=.16, y=.66),
    cam("Los cielonatos salen hacia el trece", "cielonato_2", "Cielonatos · al 13", dur=3.6, x=.16, y=.66, foco=(.31, .32, 1.7)),
    cam("Pero su camino natural del cuarenta", "claros_rio", "Claros del Río · 40-45", dur=4.0, x=.80, y=.40, tam=320),
    pv("Mucha gente cree que Hyjal", "monte_hyjal", "Monte Hyjal · antes del 60", dur=5.0, x=.74, y=.50, tam=600),
    mg(M.contadores("HASTA EL NIVEL 20", [("spell_holy_borrowedtime", "horas de media", 20, 0, 1)], ("según los creadores", 1)),
       ("llegar al veinte en Forever tarda", -.2), ("veinte horas y media|fin", 1.0), [("llegar al veinte en Forever tarda", .5), "veinte horas y media"],
       "horas al 20", y=.56),
] + filav("La Horda las recoge en Sentencia", [("sentencia", "Sentencia · Arathi", None),
                                              ("cima_trueno_dirigible", "Cima del Trueno", "y en Cima del Trueno")], y=.64, tam=320)   + filav("Claros del Río, Shen'dralas y Hyjal te están esperando", [("claros_rio_2", "Claros del Río", None),
                                                                    ("shendralas", "Shen'dralas", "Shen'dralas y Hyjal te están"),
                                                                    ("monte_hyjal_2", "Monte Hyjal", "y Hyjal te están esperando")],
          y=.62, tam=290, dur=5.0)
ROTULOS += [
    dict(texto="LEGADO · JUGUETE AL 15", en="Y al quince llega tu primera recompensa", dur=2.6, tam=110, color="amarillo", y=.2),
    dict(texto="DEL 35 EN ADELANTE, OTRA RUTA", en="del treinta y cinco en adelante", dur=2.8, tam=100, color="amarillo", y=.2),
]
# Jintha'Alor: su rótulo tapaba el pin y tocaba el de Sañadiente en el mapa → pegatina aparte (revisión visual 19-nov).
FX += [pv("La ruta acaba en Jintha'Alor", "jinthaalor", "Jintha'Alor · ciudad trol", dur=3.6, x=.74, y=.50, tam=560)]
