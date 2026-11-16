# -*- coding: utf-8 -*-
"""EFECTOS de «30 trucos para NUNCA quedarte sin ORO en WoW Forever» (15-nov-2026; helpers de wow_forever_experiencia).
Pegatinas (pv/rel/cam/ban), comentarios (com), mapas con ruta (mapa; coordenadas de `_coords.md`, Wowhead Forever), MG de mg_wow (M)
y MG NUEVOS de economía (nucleo/mg_oro.py: factura, desplome, balanza, escalera, techo, dia_noche). SIN Overgear.
python fab.py wow_oro_forever fx --seco · FAB_FX_FINAL=1 python fab.py wow_oro_forever fx hoja"""
import os

import mg_tes as T
import mg_wow as M
import peg_estilos as PE
import mg_oro as O

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


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
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
EXP = "inv_misc_book_11"   # ícono de experiencia

MON1, MON2, ESP = "ability_mount_ridinghorse", "ability_mount_whitetiger", "ability_mount_nightmarehorse"

FX = [
    # =========================================================== gancho: la factura del 60
    mg(O.factura("LO QUE CUESTA LLEGAR AL 60 MONTADO", [(MON1, "Equitación de aprendiz (nivel 40)", 100), ("ability_dualwield", "Doble especialización (40)", 50),
                                                        (MON2, "Equitación de oficial (nivel 60)", 1000), (ESP, "Montura épica", 200),
                                                        ("inv_misc_book_09", "Entrenar tu clase del 1 al 60", 207)], "TOTAL"),
       ("La equitación cuesta cien", -.2), ("Se gana con costumbres|fin", .3),
       ["La equitación cuesta cien", "otros cincuenta", "la equitación de oficial cuesta mil", "cada montura épica", "los doscientos siete de oro", "Son más de mil quinientos"],
       "factura del 60", y=.55),
    dict(tipo="mg", fn=PE.banda(os.path.join(_PAN, "banda_subasta.jpg"), "30 TRUCOS PARA NUNCA QUEDARTE SIN ORO", "del 30 al 1 · de nivel 5 a nivel 60",
                                foco=(.357, .28, 1.4), alto=380, lado="izq", tema="wow"),
         en=("Hoy te traigo treinta trucos", -.2), dur=5.0, x=.5, y=.80, sale=.3, nombre="banda 30", ver=1.0),
    # =========================================================== 29 montura de clase
    mapa("baldios", [P(62.6, 35.5, "Trinquete", "Strahad Farsan · montura del brujo", "strahad")],
         ("El brujo la consigue con Strahad Farsan", -.3), ("con la misión del Tomo de la Nobleza|fin", .3), [], "LOS BALDÍOS", "montura del 40 gratis"),
    # =========================================================== 28 Honorable
    mg(M.subasta("EQUITACIÓN CON REPUTACIÓN HONORABLE", [(MON1, "Aprendiz · normal", 100, BLANCO), (MON1, "Aprendiz · Honorable", 90, VERDE),
                                                      (MON2, "Oficial · normal", 1000, BLANCO), (MON2, "Oficial · Honorable", 900, VERDE)], "−10 %"),
       ("La equitación de aprendiz baja de cien", -.2), ("Son cien de oro gratis al sesenta|fin", .4),
       ["baja de cien", "a noventa de oro", "Y la de oficial, de mil", "a novecientos", "Son cien de oro gratis"], "honorable", y=.56),
    mapa("elwynn", [P(84.2, 65.0, "Randal Hunter", "instructor de equitación", "randal")],
         ("el instructor humano es Randal Hunter", -.3), ("En la Horda, Kildar", -.1), [], "BOSQUE DE ELWYNN", "Alianza"),
    mapa("orgrimmar", [P(69.2, 13.2, "Kildar", "Valle del Honor", "kildar")],
         ("En la Horda, Kildar", -.2), ("revisa la pestaña de reputación|fin", .2), [], "ORGRIMMAR", "Horda"),
    # =========================================================== burla0 (Ehren)
    com("Y aquí, un mensaje de Ehren", "UgxtHhlqfLdvgShqTsB4AaABAg", dur=7.5, x=.32, y=.30),
    # =========================================================== 26 doble especialización (corrección de Jorge)
    com("Jorge nos escribió", "UgzL7HlTAnv8l1xsJOV4AaABAg", dur=7.0, x=.32, y=.52),
    mg(O.escalera("REESPECIALIZAR CONTRA DOBLE ESPECIALIZACIÓN", [("1.ª vez", "1 o"), ("2.ª vez", "5 o"), ("3.ª vez", "10 o"), ("y sigue…", "+")],
                  ("Doble especialización", "50 o una vez"), "Cambiar después: gratis"),
       ("Porque reespecializar cuesta uno de oro", -.2), ("en lugar de pagar para siempre|fin", .4),
       ["uno de oro la primera vez", "cinco la segunda", "diez la tercera", "y sigue subiendo", "Con la doble", "cambiar es gratis"], "escalera respec", y=.56),
    # =========================================================== 24 recolección
    mg(M.subasta("CUERO: VENDEDOR CONTRA SUBASTA", [("inv_misc_leatherscrap_03", "Cuero ligero · vendedor", "15 c", BLANCO),
                                                 ("inv_misc_leatherscrap_03", "Cuero ligero · subasta", "casi el doble", VERDE),
                                                 ("inv_misc_leatherscrap_05", "Cuero medio · vendedor", "50 c", BLANCO),
                                                 ("inv_misc_leatherscrap_05", "Cuero medio · subasta", "cerca de 90 c", VERDE)]),
       ("El cuero ligero lo paga el vendedor", -.2), ("se acerca a noventa|fin", .6),
       ["El cuero ligero", "en la subasta casi se duplica", "El medio, a cincuenta", "se acerca a noventa"], "cuero", y=.56),
    # =========================================================== 23 Auctionator
    pv("Es un add-on de subasta que ya tiene versión", "auctionator_logo", "Auctionator · versión Forever", dur=4.2, x=.78, y=.55, tam=460),
    mg(O.balanza("¿VENDEDOR O SUBASTA?", ("inv_misc_food_70", "Carne de tortuga"), ("Vendedor", "1 c", 1), ("Subasta", "20 p", 20), "Escanea antes de vender"),
       ("Un ejemplo real: la carne de tortuga", -.2), ("Y lo mismo con la venta", .2),
       ["la carne de tortuga", "te da un cobre", "a veinte platas", ("a veinte platas", 1.2)], "balanza tortuga", y=.56),
    pv("en la pestaña de vender", "auctionator_vender", "Auctionator · vender", dur=4.6, x=.74, y=.52, tam=620),
    # =========================================================== 22 hora de publicar
    mg(O.dia_noche("LA HORA SÍ IMPORTA", "inv_misc_gem_pearl_04", "Perla de oro", "2 o 70 p", "5 o", "Casi el doble por esperar"),
       ("Un jugador vio cómo una perla de oro", -.3), ("Casi el doble por esperar|fin", .8), ["dos de oro con setenta de noche", "a cinco de oro", "Casi el doble"],
       "día y noche", y=.56),
    # =========================================================== gracias1
    com("Alan nos dijo que va despacio", "UgzLV1m3Bq7eBaF0yER4AaABAg", dur=6.0, x=.30, y=.30),
    com("Y León dice que ama que sea lento", "Ugy4zNo2xthE0B7klz94AaABAg", dur=6.0, x=.70, y=.32),
    # =========================================================== 19 misiones nuevas
    mapa("baldios", [P(57.5, 27.2, "Chol'aruk", "élite de nivel 20 · 80 platas", "cholaruk")],
         ("En Los Baldíos hay una élite nueva", -.3), ("antes del nivel trece|fin", .2), [], "LOS BALDÍOS", "Colina Espinosa"),
    # =========================================================== 18 bolsas (Rafael)
    com("Y este va para Rafael", "UgxCYAWAHLtbYaHIADB4AaABAg", dur=6.4, x=.32, y=.30),
    filav("la Bolsa de paño mágico roja tiene catorce casillas", [("o_bolsa_roja", "Bolsa de paño mágico roja · 14", None),
                                                               ("o_caja_feria", "Caja de la Luna Negra · 14", "una caja de catorce casillas")], y=.62, tam=320),
    mapa("mulgore", [P(37.2, 37.8, "Feria de la Luna Negra", "Gelvas Grimegate · diciembre", "gelvas")],
         ("La próxima Feria vuelve en diciembre", -.2), ("La próxima Feria vuelve en diciembre", 4.2), [], "MULGORE", "la Feria de diciembre"),
    # =========================================================== 17 tela
    filav("con paño de seda haces vendas", [("o_seda", "Paño de seda", None), ("o_venda", "Venda de seda pesada · 4 p", "la venda de seda pesada")], y=.62, tam=320),
    # =========================================================== burla1 (Vincent)
    com("Y aquí, Vincent, que comentó", "Ugx9MgSZUQvupXfSY0J4AaABAg", dur=7.0, x=.32, y=.30),
    # =========================================================== 16 páginas
    rel("Las verdes colinas de Tuercespina es esa misión", "o_pagina", "Las verdes colinas de Tuercespina", "15 páginas concretas", dur=5.0, x=.30),
    # =========================================================== 14 caña de hierro grande
    rel("La caña que se vende", "o_cana_hierro", "Caña de pescar de hierro grande", "+20 a pesca · se vende", dur=4.6),
    mapa("desolace", [P(20.0, 80.7, "Concha trampa", "bajo el agua · la caña, muy rara", None)],
         ("sale de las trampas de marisco", -.3), ("Y cada pescador del servidor quiere una|fin", .2), [], "DESOLACE", "al oeste de la Aldea Cazasombras",
         objeto="inv_fishingpole_01"),
    # =========================================================== 13 Supervendedor 680
    mapa("desolace", [P(40.5, 79.2, "Supervendedor 680", "caravana de Gizelton", "supervendedor")],
         ("Es un robot que viaja con la caravana", -.2), ("como la de chuleta de lobo magro|fin", .2), [], "DESOLACE", "solo cuando la caravana para"),
    filav("como la de chuleta de lobo magro", [("o_receta_lobo", "Receta: chuleta de lobo magro · 16 p", None),
                                            ("o_filete", "Chuleta de lobo magro · ~2,5 p de ganancia", "cada chuleta deja")], y=.62, tam=320),
    # =========================================================== 12 talismanes
    filav("Ardientes, del trueno y blasonados", [("o_tal_ardiente", "Talismán ardiente", None), ("o_tal_trueno", "Talismán del trueno", None),
                                               ("o_tal_blasonado", "Talismán blasonado", None)], y=.64, tam=300, dur=3.0),
    filav(("Caen de los Exiliados de las Tierras Altas", .4), [("exiliado_ardiente", "Exiliado ardiente", None),
                                                              ("exiliado_trueno", "Exiliado del trueno", None),
                                                              ("exiliado_blasonado", "Exiliado blasonado", None)], y=.60, tam=340, dur=5.0),
    mapa("arathi", [P(51.4, 50.6, "Exiliados del trueno", "Talismán del trueno", "exiliado_trueno"),
                    P(66.6, 29.8, "Exiliados blasonados", "Talismán blasonado", "exiliado_blasonado"),
                    P(25.2, 30.6, "Exiliados ardientes", "Talismán ardiente", "exiliado_ardiente")],
         ("Los del trueno caen en el centro", -.6), ("sin dar vueltas|fin", .2),
         [("Los del trueno caen en el centro", .2), "los blasonados al noreste", "y los ardientes al noroeste"], "TIERRAS ALTAS DE ARATHI",
         "los tres talismanes"),
    # =========================================================== 11 perlas azules
    mapa("tuercespina", [P(25.9, 26.6, "El Arrecife Mortal", "almejas gigantes bajo el agua", "almeja")],
         ("En la costa de la Vega de Tuercespina", -.3), ("a vigilar la barra de aire|fin", .2), [], "VEGA DE TUERCESPINA", "Perla azul",
         objeto="inv_ore_arcanite_02"),
    mg(O.desplome("PERLA AZUL EN LA SUBASTA", [("1.ª semana", 40), ("4 días después", 15), ("vendedor", .5)], "Vende pronto", ico="inv_ore_arcanite_02"),
       ("Ojo con el precio", -.2), ("Vende pronto|fin", .6), ["a cuarenta platas", "bajaron a quince", "cincuenta cobres"], "perla azul", y=.56),
    # =========================================================== gracias2
    com("Jonathan nos dijo que el video", "UgxBfWWiNyUgz45whtx4AaABAg", dur=5.8, x=.25, y=.30),
    com("Y Jota dice que muchas cosas", "UgxeV-jRsPVqxBAQpjh4AaABAg", dur=7.0, x=.75, y=.36),
    # =========================================================== 10 huevos gigantes
    mapa("tanaris_eses", [P(52.6, 28.0, "Gadgetzan", "Dirge Hojágil · misión de cocina", "dirge"), P(50.1, 30.6, "Rocs", "Huevo gigante", "roc")],
         ("En Gadgetzan hay una misión de cocina", -.3), ("se vendían a un oro cada uno|fin", .1), [("En Gadgetzan hay una misión de cocina", .3), "Caen de los rocs de Tanaris"], "TANARIS", "Huevo gigante",
         objeto="inv_egg_03"),
    mg(O.desplome("HUEVO GIGANTE EN LA SUBASTA", [("7-nov", 100), ("9-nov", 67), ("10-nov", 49), ("12-nov", 31), ("13-nov", 18)],
                  "Lo que todos farmean se hunde en días", ico="inv_egg_03"),
       ("Pero mira lo que pasó", -.2), ("se hunde en días|fin", .6),
       ["Pero mira lo que pasó", "sesenta y siete platas", "cuarenta y nueve", "treinta y una", "dieciocho platas", "lo que todos farmean"], "desplome huevos", y=.55),
    # =========================================================== 09 grises
    mapa("feralas_eses", [P(55.3, 68.0, "Hipogrifos Frayfeather", "picos afilados y huesos de ala", "frayfeather")],
         ("En Feralas, los hipogrifos", -.3), ("En las granjas de las Laderas", -.1), [], "FERALAS", "grises que paga el vendedor"),
    filav("En Feralas, los hipogrifos", [("o_pico", "Pico afilado", None), ("o_hueso", "Hueso hueco de ala", None)], y=.66, tam=280, dur=5.0),
    # =========================================================== 08 tortugas
    mapa("tanaris_eses", [P(54.1, 93.1, "Planoleadores", "tortugas de nivel 48-50", "planeador")],
         ("En la costa sur de Tanaris hay unas tortugas", -.3), ("almejas que a veces traen perlas|fin", .2), [], "TANARIS", "costa sur"),
    filav("Sueltan dos grises que el vendedor paga bien", [("o_tortuga", "Carne de tortuga", "carne de tortuga#2"), ("o_perla_oro", "Perla de oro", "almejas que a veces traen perlas")],
          y=.64, tam=300),
    rel("le salió una perla de oro", "o_perla_oro", "Perla de oro", "1 o al vendedor · hasta 5 o en subasta", dur=4.4),
    # =========================================================== 07 Waylaid Crates
    mapa("crestagrana", [P(9.5, 71.0, "Three Corners", "Marcy Baker · Alianza", None)],
         ("Se entregan en el campamento de Three Corners", -.3), ("Se entregan en el campamento de Three Corners", 4.0), [], "MONTAÑAS CRESTAGRANA", "Waylaid Crates"),
    mapa("baldios", [P(50.0, 29.2, "Al oeste del Cruce", "Dokimi · Horda", None)],
         ("al oeste del Cruce, en Los Baldíos", -.4), ("si eres Horda|fin", 1.6), [], "LOS BALDÍOS", "Waylaid Crates"),
    # =========================================================== burla2 (CaneAttack)
    com("CaneAttack nos escribió", "Ugxmhp_aWWm151Dp5Tp4AaABAg", dur=7.0, x=.32, y=.30),
    # =========================================================== 05 bandas
    pv("entre ellas la Guarida de Onyxia", "onyxia", "Onyxia · bandas del 9-dic", dur=4.6, x=.78, y=.52, tam=520),
    filav("Un jugador compró unos dos mil cardoveloces", [("o_cardopresto", "Cardoveloz · de 3 p a 25 p", None), ("o_fuego", "Elemental de Fuego", "El fuego elemental es otro clásico")],
          y=.62, tam=320),
    # =========================================================== 04 pesca alta
    rel("Los Adornos brillantes se compran", "o_adornos", "Adornos brillantes", "+75 a pesca", dur=4.4, x=.28),
    mapa("tuercespina", [P(27.4, 77.0, "Bahía del Botín", "Viejo Heming · libro de experto", "heming")],
         ("el libro de pesca de experto te lo vende el Viejo Heming", -.3), ("Y el de artesano, Nat Pagle", -.1), [], "VEGA DE TUERCESPINA", "pesca de experto"),
    mapa("marjal_eses", [P(58.5, 60.0, "Nat Pagle", "pesca de artesano", "nat_pagle")],
         ("Y el de artesano, Nat Pagle", -.2), ("en el Marjal Revolcafango|fin", 2.0), [], "MARJAL REVOLCAFANGO", "pesca de artesano"),
    # =========================================================== 03 sátiros
    mapa("frondavil_eses", [P(41.7, 85.0, "Claro Fuego de Jade", "sátiros Jadefire", "satiro_jadefire"), P(42.4, 17.4, "Paso Fuego de Jade", "sátiros Jadefire", None)],
         ("Los sátiros Jadefire de Frondavil", -.3), ("sacó un par de cientos de oro|fin", .2), [], "FRONDAVIL", "paño rúnico y tela de inferi"),
    mapa("azshara", [P(56.4, 20.6, "Sátiros Legashi", "paño rúnico", "satiro_legashi")],
         ("Y llegó al sesenta con más de mil trescientos", -.3), ("Solo con costumbres como estas|fin", .2), [], "AZSHARA", "sátiros Legashi"),
    filav("sueltan paño rúnico y tela de inferi", [("o_runico", "Paño rúnico", None), ("o_vil", "Tela de inferi", None)], y=.66, tam=300),
    # =========================================================== 02 torio y Cristal Arcano
    mapa("estepas", [P(47.3, 33.4, "Filón de torio enriquecido", None, "veta_torio"), P(30.3, 58.6, "Filón", None, None),
                     P(54.4, 60.1, "Filón", None, None), P(61.0, 38.5, "Filón", None, None)],
         ("en Las Estepas Ardientes hay vetas de torio ricas", -.3), ("seis Cristales Arcanos|fin", .3), [], "LAS ESTEPAS ARDIENTES", "vetas de torio ricas"),
    mg(O.techo("EL TECHO DEL CRISTAL ARCANO", "inv_misc_gem_topaz_01", "Cristal Arcano", [("Lo vendió", 9), ("Poco después", 12.5)], ("Mercado negro", 50),
               "Nunca vale más de 50"),
       ("Los vendió a unos nueve de oro", -.2), ("cada veta rica es oro puro|fin", .4),
       ["a unos nueve de oro", "a doce y medio", "cincuenta de oro fijos", "Así que el cristal nunca"], "techo cristal", y=.56),
    pv("Mister Graphed vende el Cristal Arcano", "mister_graphed", "Mister Graphed · Riverglades", dur=4.4, x=.09, y=.18, tam=320,
       marco="museo", estancia="kenburns"),
    # encima del panel del techo (antes, a y=.66, tapaban la barra «Lo vendió»)
    pv("el Loto negro también tiene su techo", "o_loto", "Loto negro · 50 o", dur=4.6, x=.72, y=.135, tam=230),
    pv("el Loto negro también tiene su techo", "o_cristal", "Cristal Arcano · 50 o", dur=4.6, x=.88, y=.135, tam=230),
    # =========================================================== 01 misiones 48+
    mg(M.tiempos("MISIONES QUE DAN ORO", [("Antes: 1 de 4", 25, ROJO), ("Desde el 10-nov: la mayoría del 48 en adelante", 75, VERDE)],
                 "Hazlas en cuanto las tengas"),
       ("Y como en el juego original solo una de cada cuatro", -.2), ("incluso las que nunca lo dieron|fin", .6),
       ["solo una de cada cuatro", "Ahora la mayoría", "incluso las que nunca"], "misiones oro", y=.56),
    pant("hyjal", ("solo con las misiones del Monte Hyjal", -.4), ("el vendedor las paga a tres o cinco de oro|fin", .2), oscuro=.15),
    # =========================================================== cierre
    dict(tipo="mg", fn=PE.banda(os.path.join(_PAN, "banda_gadgetzan.jpg"), "EL ORO SON COSTUMBRES", "no pagues lo que no usas · vende primero · salta de mercado",
                                foco=(.5, .22, 1.0), alto=380, lado="izq", tema="wow"),
         en=("No pagues lo que no usas", -.2), dur=6.0, x=.5, y=.80, sale=.3, nombre="banda cierre", ver=1.0),
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

FX += [
    pv("El brujo la consigue con Strahad Farsan", "strahad", "Strahad Farsan · Trinquete", dur=3.8, x=.17, y=.60, tam=420),
    pv("hay una élite nueva de los jabaespines", "cholaruk", "Chol'aruk · élite nueva", dur=4.0, x=.17, y=.60, tam=440),
    pv("Es un robot que viaja con la caravana", "supervendedor", "Supervendedor 680", dur=4.2, x=.20, y=.40, tam=420),
    pv("Caen de los rocs de Tanaris", "roc", "Roc de Tanaris", dur=3.6, x=.15, y=.62, tam=380),
    pv("unas tortugas, los Planeadores de oleaje", "planeador", "Planoleador · Tanaris", dur=3.8, x=.80, y=.55, tam=420),
    pv("hay almejas gigantes", "almeja", "Almeja gigante", dur=3.6, x=.80, y=.55, tam=380),
    pv("los sátiros Jadefire de Frondavil y los Legashi", "satiro_jadefire", "Sátiro Fuego de Jade", dur=3.8, x=.82, y=.40, tam=380),
    pv("Si eres minero de nivel alto", "veta_torio", "Filón de torio enriquecido", dur=4.0, x=.86, y=.68, tam=380),
]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="42 DE ORO", en="y tienes cuarenta y dos de oro", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="207 DE ORO", en="unos doscientos siete de oro", dur=2.4, tam=150, color="amarillo", y=.2),
    dict(texto="50 DE ORO, NO 10", en="Tienen razón: en el juego, son cincuenta de oro", dur=2.8, tam=130, color="amarillo", y=.2),
    dict(texto="23 DE ORO", en="Veintitrés de oro que, al cuarenta", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="80 PLATAS", en="te da ochenta platas", dur=2.2, tam=150, color="amarillo", y=.82),
    dict(texto="~55 DE ORO", en="ganó unos cincuenta y cinco de oro", dur=2.4, tam=150, color="amarillo", y=.2),
    dict(texto="+1300 DE ORO AL 60", en="Y llegó al sesenta con más de mil trescientos", dur=2.6, tam=120, color="amarillo", y=.85),
]
SFX = {}
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número treinta.", "Número veinticinco", "Número veinte.", "Número quince",
                                                                "Número diez", "Número cinco")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Hoy te traigo treinta trucos", "Número uno. Las misiones del cuarenta y ocho")]

APOYOS = [
    dict(en="El entrenamiento completo, del uno al sesenta", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Instructor de clase", calidad="amarillo",
         icono="inv_misc_book_09", lineas=["Del 1 al 60: ~207 de oro", "igual en todas las clases", dict(t="Compra solo lo que usas", c=V)])),
    dict(en="El sistema de Legado de Forever te da puntos", dur=9.2, x=.72, size=.50, tarjeta=dict(titulo="Legado que ahorra", calidad="morado",
         icono="inv_misc_coin_03", lineas=["Viajero frecuente: vuelos −50 %", "Regateo: −5 % por rango", "Reforzar: menos durabilidad", dict(t="Descuentos para siempre", c=V)])),
    dict(en="La subasta de tu facción se queda con un cinco", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Comisión de la subasta", calidad="amarillo",
         icono="inv_misc_coin_02", lineas=["Tu facción: 5 %", dict(t="Neutrales: 15 %", c=RJ)])),
    dict(en="Un personaje de nivel bajo aparcado junto al buzón", dur=5.6, x=.72, size=.50, tarjeta=dict(titulo="Personaje banco", calidad="verde",
         icono="inv_letter_15", lineas=["Junto al buzón y la subasta", "Vendedor · subasta · desencantar", dict(t="Tu principal sigue jugando", c=V)])),
    dict(en="Y en mar abierto, frente a los Páramos", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Baúl bien sellado", calidad="verde",
         icono="inv_box_04", lineas=["Mar abierto", "No pide habilidad de pesca", "Pocos lances de cada cien"])),
    dict(en="Son cajas interceptadas que caen de los enemigos", dur=5.6, x=.72, size=.50, tarjeta=dict(titulo="Waylaid Crate", calidad="verde",
         icono="inv_box_04", lineas=["Llénala: Favor de comerciante", "Shipping Label: 50 Favor + 2000 rep.", dict(t="Vacía: 17-30 platas (1.ª semana)", c=V)])),
    dict(en="Forever trae más de seiscientas recetas nuevas", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Recetas de Favor", calidad="morado",
         icono="inv_scroll_03", lineas=["+600 recetas nuevas", "Favor de comerciante + reputación", dict(t="El primero pone el precio", c=V)])),
]


# --- DENSIDAD (chequeo 15-nov: mg 0,7/min vs 1,1 del canal; pegatinas 1,2 vs 1,9) ---
# Revisado en su cuadro final (FAB_FX_FINAL=1 fx hoja, 15-nov): fuera las pegatinas que repetían la foto que ya trae el mapa
# (Randal, Kildar, Dirge, Heming, Nat Pagle, Gelvas, Planoleador, huevo, caña de hierro) y la del tooltip de Auctionator (texto cortado; el clip
# de 057 ya enseña el tooltip real); fuera el MG «1300 al 60» (pisaba los mapas de Frondavil y Azshara y repetía el rótulo).
# Legado arranca cuando sale la tarjeta; talismanes termina antes del mapa de Arathi; tortugas solo en «no vio a nadie»;
# cardoveloz a la derecha para no tapar la pegatina; bolsas más ancho (el 14 caía encima de la última casilla).
FX += [
    mg(M.contadores("LEGADO QUE AHORRA", [("inv_misc_coin_03", "Viajero frecuente: vuelos −%", 50, 0, 1), ("inv_misc_coin_02", "Regateo: −% por rango", 5, 1, 2),
                                          ("inv_misc_book_09", "Reforzar: rangos", 5, 2, 3)], ("DESCUENTOS PARA SIEMPRE", 3)),
       ("Viajero frecuente hace que tus vuelos", 2.2), ("eso suma más que cualquier farmeo de un día|fin", .3),
       ["cuesten la mitad", "Regateo te baja", "Y Reforzar", "Ninguno te hace rico"], "legado", y=.56),
    mg(M.filas("CASILLAS DE BOLSA", [("Bolsa de paño mágico roja", 14, ["inv_misc_bag_10_red"]), ("Caja de la Luna Negra", 14, ["inv_box_04"])], ancho=1660),
       ("Más bolsa es más botín por cada salida", -.4), ("se pagan solas|fin", .4), ["Más bolsa", "Es de las primeras inversiones"], "bolsas", y=.56),
    mg(M.subasta("TALISMANES EN LA SUBASTA", [("inv_jewelry_talisman_02", "Talismán del trueno", "20-30 p", BLANCO),
                                            ("inv_jewelry_talisman_05", "Talismán blasonado", "20-30 p", BLANCO),
                                            ("inv_jewelry_talisman_02", "Algunos lo vieron a", "más de 50 p", VERDE)]),
       ("En la subasta, los del trueno y los blasonados", -.2), ("los vieron por encima de cincuenta|fin", .15),
       ["los del trueno", "y los blasonados estaban", "Algunos jugadores"], "talismanes", y=.56),
    mg(O.desplome("CARDOVELOZ EN LA SUBASTA", [("1.er día", 3), ("una semana después", 25)], "×8 en una semana", ico="inv_misc_herb_04", ancho=1080),
       ("Un jugador compró unos dos mil cardoveloces", -.1), ("ya valían veinticinco|fin", 1.0),
       ["a tres platas", "ya valían veinticinco", ("ya valían veinticinco", 1.0)], "cardoveloz", y=.56, x=.64),
    mg(M.contadores("UNA HORA Y VEINTE CON LAS TORTUGAS", [("inv_misc_coin_01", "Oro ganado", 55, 0, 1), ("inv_misc_groupneedmore", "Jugadores que vio", 0, 1, 2)],
                    ("LA PLAYA PARA ÉL SOLO", 2)),
       ("Y lo más curioso: en toda esa hora", -.2), ("tenía la playa para él solo|fin", .4),
       [("Y lo más curioso: en toda esa hora", .3), "no vio a nadie más", "tenía la playa"], "tortugas", y=.56),
    mg(M.subasta("TU PERSONAJE BANCO DECIDE", [("inv_misc_coin_02", "Esto", "al vendedor", BLANCO), ("inv_misc_bag_10_red", "Esto", "a la subasta", BLANCO),
                                               ("inv_enchant_disenchant", "Y esto", "lo desencanto", VERDE)], cab=("OBJETO", "DESTINO")),
       ("Y ese personaje decide con calma", -.2), ("Con un add-on como Disenchantrix|fin", .6),
       ["esto al vendedor", "esto a la subasta", "y esto lo desencanto"], "personaje banco", y=.56),
]
FX += [
    cam("Aprender a recolectar es casi gratis", "o_cuero_ligero", "Cuero ligero", dur=3.4, x=.89, y=.20, tam=240),
    cam("la pareja más sencilla es minería y desuello", "o_torio", "Minería", dur=3.2, x=.11, y=.20, tam=240),
    pv("El nueve de diciembre abren las bandas", "onyxia_guarida", "Guarida de Onyxia", dur=4.0, x=.22, y=.50, tam=460),
    cam("Los que van a entrar necesitan pociones", "o_fuego", "Elemental de Fuego", dur=3.4, x=.89, y=.20, tam=240),
    cam("Y la tela de inferi no es solo para sastres", "o_vil", "Tela de inferi", dur=3.4, x=.89, y=.20, tam=240),
    cam("Y si eres sastre, las talegas pequeñas", "o_seda", "Paño de seda", dur=3.2, x=.11, y=.20, tam=240),
    pv("Hay jugadores que incluso se quedan matando trols", "o_pagina", "Página de Tuercespina", dur=3.4, x=.86, y=.24, tam=260),
    cam("Y cada almeja es como un pequeño cofre", "o_perla_azul", "Perla azul", dur=3.2, x=.89, y=.20, tam=240),
]
