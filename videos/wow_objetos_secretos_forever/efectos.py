# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 15 OBJETOS SECRETOS de WoW Forever que nadie te explica» (motor SECUENCIA YT, Crónicas de Warcraft, 1-nov-2026).
- MG NUEVOS de este guion (nucleo/mg_wow.py): `ocultos` (la bolsa con 12 594 casillas tapadas), `chat` (/cantar y /bailar en la
  ventana de chat), `duplica` (la banana: bosque contra cueva), `conjunto` (los anillos «Cómplices»), `reloj_oro` (el don que corre
  desconectado), `subasta` (mercado negro), `pizarra` (Shen'Serrar en tiza), `censurado` (el legendario borrado) y `tiempos` (la crisálida).
- MAPAS REALES con ruta en 10 de 15 puestos. Riverglades y Zephras son zonas nuevas sin mapa real descargable: sin mapa.
- Overgear campaña 2 con el kit Forever, fondo de marca SIEMPRE y creativo CRONICAS10 sin audio.
- Pegatinas variadas (`nucleo/peg_estilos.py`), tooltips REALES de Wowhead Forever es-MX y tarjetas SOLO con datos del guion.
- Comentarios reales: 5 agradecimientos + 3 críticas con burla (el usuario, 1-nov).
  python fab.py wow_objetos_secretos_forever apoyos | fx hoja | fx
"""
import os

import mg_mapa as MP
import mg_tes as T
import mg_wow as M
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("scene-037", -9.73)   # «CRONICAS10» suena en ~303,2 s: el rótulo del creativo (2,5 s) entra con la palabra
TEMA_MAPA = "wow"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=420):
    return dict(tipo="mg", fn=T.pegatina(F(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def gran(en, slug, titulo, dur=4.5, x=.25, tam=660):
    return peg(en, slug, titulo, dur, x, .50, tam)


def com(en, id_, dur=5.2, x=.30, y=.30, tam=760):
    return peg(en, "com_" + id_, "", dur, x, y, tam)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .25, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(F(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema="wow"), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.7, zmin=1.0):
    """Mapa real a cuadro entero con la ruta (mg_wow.ruta): un pin por paso en su marca, con la foto de lo que se nombra."""
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def donde(nom, puntos, de, a, marcas, titulo, sub=None, x=.70, y=.42):
    """«¿Dónde está?»: ventana sobre el clip, 3-5 s."""
    fn = MP.mapa(os.path.join(_MAP, nom + ".jpg"), puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana")
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + titulo, ver=3.0)


def mg(fn, de, a, marcas, nombre, y=.60, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def kal(x, y):
    """% del mapa de Kalimdor -> % del mapa del mundo (calibrado en wow_objetos_raros, 22-oct-2026)."""
    return (128 + (x / 100 * 1022 - 385) * .826) / 1024 * 100, (130 + (y / 100 * 668 - 100) * .858) / 683 * 100


def ek(x, y):
    """% del mapa de los Reinos del Este -> % del mapa del mundo."""
    return (700 + (x / 100 * 1024 - 400) * .785) / 1024 * 100, (285 + (y / 100 * 683 - 290) * .786) / 683 * 100


BLANCO, ROJO, VERDE, GRIS, ORO_T = M.BLANCO, M.ROJO, M.VERDE, M.GRIS, M.ORO_T
BOLSA = ["inv_throwingaxe_01", "inv_misc_food_24", "inv_misc_herb_blacklotus", "inv_jewelry_ring_54", "inv_misc_stonetablet_04",
         "inv_frog2_blue", "inv_misc_web_02", "ability_mount_undeadhorse", "spell_nature_swiftness", "inv_misc_fish_69"]
AMAR = (255, 255, 160)

CAMARA = {}
FUNDIDO = {
    "scene-037": 0,                                # corte seco del creativo («LINK IN THE DESCRIPTION») al «Número once»
}
FX = [
    # =========================================================== gancho: MG desde el segundo 1
    mg(M.ocultos("OBJETOS DE WOW FOREVER", [("objetos, y más", 31000, BLANCO), ("con las estadísticas escondidas", 12594, ROJO)], BOLSA,
                 revela="REVELADO PARA TODOS"),
       ("más de treinta y un mil objetos", -.5), ("el juego se lo revela a todos|fin", 1.0),
       ["más de treinta y un mil", "doce mil quinientos", "consigue uno y el juego"], "ocultos gancho", y=.52),
    aba([("cercenarrocas", "Hacha"), ("banana", "Banana"), ("loto", "Loto negro"), ("llave", "Llave")], "encontraron un hacha", ("con el nombre borrado|fin", .8),
        ["un hacha que mina", "una banana que", "mercado negro que vende", "una llave que"], "gancho"),
    com("Como nos escribió un espectador", "UgxNUEuhQMM7b46ar-t4AaABAg", dur=6.2),
    # =========================================================== 15 Delicia
    rel("Número quince", "delicia", "Delicia de descarrioaleta sabrosa", "receta nueva · Alianza"),
    donde("reinos_este_eses", [(.54, .69, "Montañas Crestagrana")], ("las Montañas Crestagrana", -.4), ("ochenta y cinco de Cocina|fin", .6),
          ["las Montañas Crestagrana"], "Montañas Crestagrana", x=.30),
    cam("la hermana de la Delicia", "delicia", "La hermana de Los Baldíos", dur=4.4, foco=(.5, .5, 1.0)),   # icono entero
    peg("te convertía en un múrloc", "murloc", "Múrloc", dur=3.4, x=.13, tam=360),
    peg("o en un ogro", "ogro", "Ogro", dur=3.0, x=.31, tam=360),
    gran("ahora te convierte en un orco", "grunido", "Orco ninja… o pirata", dur=4.0, x=.25, tam=540),
    gran("volverás a ser múrloc", "murloc", "Esta vez, a propósito", dur=3.6, x=.76, tam=600),
    # =========================================================== 14 Saltavientos
    rel("Número catorce", "saltavientos", "Saltavientos musical", "se consigue cantando"),
    mg(M.chat([("Cantas frente a las ranas.", AMAR), ("Una sola rana: no pasa nada.", ROJO), ("Dos o más: aparece una rana nueva.", VERDE)], "/cantar"),
       ("escribir el gesto de cantar", -.6), ("en el tronco de al lado|fin", 1.2),
       ["escribir el gesto", "si sobre la roca queda una sola", "tienen que ser al menos dos", "Si lo haces bien"], "chat cantar", x=.30, y=.70),
    # =========================================================== gracias 1
    com("gracias por comentarios como estos", "Ugz84d60LthINJhfjvt4AaABAg", dur=5.2, y=.26),
    com("Todos se leen", "UgyCTRdo285axs4NRa54AaABAg", dur=5.4, x=.68, y=.68),
    # =========================================================== 13 Babosa
    rel("Número trece", "babosa", "Babosa agitada", "mascota · Horda"),
    mapa("entranas", [(66, 24, "Entrañas", "con un vendedor llamado Boyle", F("boyle")), (49, 46, "El canal", "una babosa en el agua", F("babosa"))],
         ("Esta es para la Horda", -.2), ("le bailas|fin", .3), ["empieza en Entrañas", "bajas al canal"], "ENTRAÑAS", "bailarle a una babosa", zmax=1.6),
    peg("Le compras un Fango de baba nutritivo", "fango", "Fango de baba nutritivo", dur=4.2, x=.80, y=.28, tam=320),
    mg(M.chat([("Bailas frente a la babosa.", AMAR), ("La babosa te devuelve el baile.", VERDE)], "/bailar"),
       ("Y le sigues bailando", -.5), ("hasta que la babosa te devuelve el baile|fin", 1.2),
       ["Y le sigues", "hasta que la babosa"], "chat bailar", x=.30, y=.70),
    # =========================================================== burla 1
    com("también nos llegan comentarios como este", "Ugzjp48cJ-IfVZwrBEd4AaABAg", dur=6.6, y=.30),
    peg("cómo bailarle a una babosa", "babosa", "Todos los gustos", dur=4.0, x=.80, y=.62, tam=380),
    # =========================================================== 12 Cría de crocolisco
    rel("Número doce", "cria_croco", "Cría de crocolisco", "mascota · botín"),
    mapa("ventormenta", [(61, 73, "Canales de Ventormenta", "la Bestia de cloaca", F("sewer_beast")), (70, 28, "Por toda la ciudad", "casi nadie nada ahí")],
         ("En los canales de la capital", -.2), ("casi nadie se mete a nadar ahí|fin", .4), ["En los canales", "recorre los canales"],
         "VENTORMENTA", "la leyenda de las cloacas", zmax=1.5),
    leg("sewer_beast", "BESTIA DE CLOACA", ["Crocolisco raro", "Nivel 50", "Cría: 1,52 %"], ("En Forever le dieron algo", -.2),
        ("uno coma cincuenta y dos por ciento de probabilidad|fin", .6), ["En Forever le dieron", "uno coma cincuenta"], ("SUELTA CRÍA", 1)),
    gran("Está pescando un cocodrilo", "sewer_beast", "Está pescando", dur=3.0, x=.74, tam=620),
    # =========================================================== Overgear campaña 2: kit «WoW - Forever (nov)» + fondo de marca SIEMPRE
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="tú eliges, y pagas", a="scene-037", entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Talentos, rotación", dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="tú eliges, y pagas", dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción", a=CODIGO,
         entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a="scene-037", entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== 11 Banana
    rel("Número once", "banana", "Banana dorada", "abalorio", dur=3.4),
    mg(M.duplica("BANANA DORADA", "inv_misc_food_24", ("+16", "15 s"), ("+32", "30 s"), "BOSQUES Y PRADERAS", "EN CUALQUIER OTRO SITIO", "SOLO UNA BANANA"),
       ("Su efecto es real", -.3), ("con una banana en la mano|fin", 1.0), ["Su efecto es real", "se duplican en bosques", "En una cueva"], "banana", y=.68),
    # =========================================================== burla 2
    com("aquí va una reseña muy detallada", "UgyLra8yqW9zGb2baQ54AaABAg", dur=7.0, y=.30),
    peg("es de la banana", "banana", "La culpable", dur=3.0, x=.76, y=.60, tam=420),
    # =========================================================== 10 Crisálida
    rel("Número diez", "crisalida", "Crisálida transformadora", "abalorio"),
    donde("kalimdor_enus", [(.46, .61, "Mulgore")], ("misión de élite nueva en Mulgore", -.4), ("para nivel treinta|fin", .4),
          ["misión de élite"], "Mulgore", x=.30),
    mg(M.tiempos("CRISÁLIDA TRANSFORMADORA", [("5 s: ATURDIDO", 5, ROJO), ("8 s: +60 %", 8, (20, 130, 40)), ("5 MIN DE REUTILIZACIÓN", 12, (70, 70, 90))], "absorbes 260-300 de daño"),
       ("Al usarla, absorbes", -.3), ("sesenta por ciento más de velocidad durante ocho segundos|fin", .6),
       ["te aturdes tú mismo", "Cuando el aturdimiento", "durante ocho segundos", "Al usarla, absorbes"], "crisalida", y=.74),
    # =========================================================== 9 Cercenarrocas
    rel("Número nueve", "cercenarrocas", "Cercenarrocas", "el hacha que mina"),
    mapa("reinos_este_eses", [(45.5, 67, "Ventormenta", "capital de la Alianza"), (42, 75, "Minas de la Muerte", "Rhahk'Zor, primer jefe", F("rhahkzor"))],
         ("Lo suelta Rhahk'Zor", -.2), ("cinco por ciento de probabilidad|fin", .4), ["Lo suelta Rhahk'Zor", "las Minas de la Muerte"], "MINAS DE LA MUERTE", "5,45 %", zmax=2.2),
    mg(M.contadores("EL CERCENARROCAS", [("trade_mining", "Cargas para minar", 30, 0, 1), ("inv_throwingaxe_01", "Vueltas a las Minas, de media", 18, 2, 3)],
                    remate=("SIN HABILIDAD DE MINERÍA", 4)),
       ("Tiene treinta cargas", -.2), ("ciento veinticinco de habilidad solo para tocar el hierro|fin", .8),
       ["Tiene treinta", "cuando se acaban", "Con un cinco por ciento", "dieciocho vueltas", "un minero normal"], "cercenarrocas", y=.74),
    # =========================================================== gracias 2
    com("otra tanda de comentarios", "Ugy28dO2Wp7-M9Wj3ax4AaABAg", dur=4.6, y=.26),
    com("Gracias a los que nos ven", "Ugyw34VhbGJdf7yIB194AaABAg", dur=5.0, x=.68, y=.68),
    # =========================================================== 8 Sortija
    rel("Número ocho. La Sortija", "contramaestre", "Sortija de contramaestre", "nivel 17"),
    cam("Cae de Mr. Smite", "smite", "Mr. Smite · 1,01 %", dur=4.2),
    mg(M.conjunto("CONJUNTO «CÓMPLICES»", (F("contramaestre"), "Sortija de contramaestre", "nivel 17"), (F("media_naranja"), "La media naranja", "nivel 60"),
                  ["Enfado: +50 de fuerza, 10 s", "+22 de fuerza fijos"], ("44 DE FUERZA", "94 ENFADADO"), "¿DÓNDE CAE?"),
       ("conjunto de dos piezas", -.3), ("dónde cae la media naranja|fin", 1.0),
       ["conjunto de dos piezas", "La otra mitad", "cincuenta de fuerza", "más veintidós fijos", "Sumado todo", "nadie sabe todavía"], "conjunto", y=.66),
    # =========================================================== burla 3
    com("Un comentario que ya venía roncando", "UgwFly67BE4afgM2Vy54AaABAg", dur=5.6, y=.30),
    rel("la Bolsa de dormir acogedora", "bolsa_dormir", "Bolsa de dormir acogedora", "dormir da experiencia", dur=4.6),
    # =========================================================== 7 Don del galope
    rel("Número siete", "galope", "Don del galope", "épico · 150 de oro"),
    gran("Mister Graphed, agente del mercado negro", "graphed", "Mister Graphed", dur=4.4, x=.25, tam=560),
    mg(M.reloj_oro("DON DEL GALOPE", "spell_nature_swiftness", 360, (150, 300)),
       ("La trampa está en una línea", -.3), ("juegues o no|fin", 1.0), ["La trampa está", "el tiempo corre aunque", "Así que mantenerlo", "juegues o no"], "don del galope", y=.70),
    # =========================================================== 6 Loto negro
    rel("Número seis", "loto", "Loto negro", "la planta más peleada"),
    mg(M.subasta("MISTER GRAPHED · MERCADO NEGRO", [("inv_misc_herb_blacklotus", "Loto negro", 50, BLANCO), ("inv_misc_pelt_wolf_01", "Pellejos prístinos", "EN VENTA", BLANCO),
                                                    ("inv_misc_monsterscales_09", "Escamas prístinas", "EN VENTA", BLANCO), ("inv_misc_gem_pearl_05", "Cristales arcanos", "EN VENTA", BLANCO)]),
       ("Pues el mismo Mister Graphed", -.2), ("para que nadie pueda pedir una fortuna|fin", 1.0),
       ["lo vende a cincuenta", "junto a pellejos", "escamas prístinas", "y cristales arcanos"], "mercado loto", y=.62),
    mg(M.subasta("MATERIALES QUE NO EXISTÍAN", [("inv_misc_questionmark", "Fel Crystal", "¿PARA QUÉ?", M.NARANJA), ("inv_misc_questionmark", "Stranglevine", "¿PARA QUÉ?", M.NARANJA)],
                 sello="RECETAS ESCONDIDAS", cab=("MATERIAL", "RECETA")),
       ("Pero también vende dos materiales", -.2), ("esas recetas están escondidas en algún sitio|fin", 1.0),
       ["Fel Crystal", "Stranglevine", "esas recetas están"], "materiales", y=.62),
    # =========================================================== 5 Riendas
    rel("Número cinco", "riendas", "Riendas de destrero de la muerte", "ahora en subasta"),
    mg(M.subasta("CASA DE SUBASTAS DEL MERCADO NEGRO", [("ability_mount_undeadhorse", "Riendas de destrero de la muerte", 3000, (163, 53, 238)),
                                                        ("inv_helmet_01", "Piezas de los primeros conjuntos", 400, (0, 112, 221)), ("inv_box_petcarrier_01", "Gato de compañía", 100, BLANCO)],
                 cab=("LOTE", "PUJA")),
       ("la montura del barón Rivendare", -.3), ("y un gato de compañía por cien|fin", 1.2), ["con una puja de tres mil", "En el mismo lote", "un gato de compañía"], "subasta", y=.62),
    gran("sacarla en Stratholme", "rivendare", "Barón Rivendare", dur=4.4, x=.75, tam=620),
    donde("reinos_este_eses", [(.57, .08, "Stratholme")], ("él hizo Stratholme solo", -.4), ("para conseguirla|fin", .4), ["él hizo Stratholme"], "Stratholme", x=.30),
    # =========================================================== 4 Llave de piedra
    rel("Número cuatro", "llave", "Llave de piedra", "nadie sabe qué abre"),
    mapa("reinos_este_eses", [(50.5, 35, "Muralla de Thoradin", "la Página quemada", "ficha:" + os.path.join(_D, "apoyos", "wowhead_5e4a2c4875.png")), (47, 29.5, "Entrañas", "el libro entre escombros", F("fragmento")),
                              (49, 62, "Montaña Roca Negra", "el saco vigilado", F("grunido"))],
         ("Todo empieza en la Muralla", -.2), ("La página te manda|fin", 5.0), ["Todo empieza en la Muralla", "entrada trasera de Entrañas"], "LA PISTA DE LA LLAVE", "Reinos del Este", zmax=1.9),
    mapa("azeroth_eses", [(*ek(49, 62), "Montaña Roca Negra"), (*ek(56, 83), "El Portal Oscuro"), (*kal(49, 80), "Cresta de la Pluma de Fuego", "cráter de Un'Goro")],
         ("El libro enseña tres dibujos", -.2), ("en el cráter de Un'Goro|fin", .5), ["la Montaña Roca Negra", "el Portal Oscuro", "la Cresta de la Pluma"], "LOS TRES DIBUJOS", "el libro de Entrañas", zmax=1.5),
    gran("Con el fragmento sacas la Llave de piedra", "llave", "Llave de piedra", dur=4.0, x=.25, tam=520),
    # =========================================================== 3 Shen'Serrar
    peg("Número tres. Shen'Serrar", "quelserrar", "¿Shen'Serrar?", dur=4.0),
    mg(M.pizarra(["Shen'Serrar", "lezal", "melor'na", "adala", "fal"], [(0, "HOJA OCULTA"), ((2, 3, 4), "«la verdad es una luz que guía»")], "«LA HOJA OCULTA ES NUESTRA LUZ GUÍA»"),
       ("en la pizarra, escrito en élfico", -.2), ("es nuestra luz guía|fin", 1.2), ["escrito en élfico", "Shen significa oculto", "El resto se parece", "así que la frase podría"], "pizarra", y=.56),
    gran("frente a Onyxia", "onyxia", "Onyxia", dur=4.0, x=.75, tam=640),
    donde("kalimdor_enus", [(.55, .71, "Guarida de Onyxia")], ("la Guarida de Onyxia vuelve", -.4), ("el nueve de diciembre|fin", .8), ["la Guarida de Onyxia"], "Guarida de Onyxia", x=.30),
    # =========================================================== 2 Las 75 monturas
    rel("Número dos", "destrero", "75 monturas ocultas", "todavía sin ver", dur=4.0),
    mg(M.contadores("LO QUE SIGUE ESCONDIDO", [("ability_mount_undeadhorse", "Monturas", 75, 0, 1), ("spell_nature_swiftness", "Hechizos sin ver", 1773, 1, 2),
                                               ("inv_misc_questionmark", "Objetos del Núcleo de Magma", 130, 2, 3)]),
       ("salieron setenta y cinco monturas", -.3), ("con las estadísticas escondidas|fin", 1.0), ["salieron setenta", "También mil setecientos", "Solo del Núcleo", "objetos del juego original"], "escondido", y=.72),
    mg(M.ocultos("LO QUE QUEDA POR SABER", [("revelados en la beta", 4419, VERDE), ("todavía escondidos, y más", 8000, ROJO)], BOLSA, sello="UN TERCIO"),
       ("Durante la beta se revelaron", -.3), ("un tercio de lo que hay|fin", 1.0), ["Durante la beta", "aún quedan", "O sea que", "un tercio"], "ocultos final", y=.52),
    # =========================================================== 1 El legendario
    mg(M.censurado("EL PRIMER LEGENDARIO DE FOREVER", [("spell_nature_natureguardian", "Ritual · Círculo Cenarion"), ("spell_nature_starfall", "Efusiones de luz lunar"),
                                                       ("spell_nature_lightning", "Cargado de tormenta"), ("inv_misc_map_01", "Cima de Hyjal"),
                                                       ("spell_shadow_summoninfernal", "La caída de Archimonde")], "¿BASTÓN DE SANADOR?"),
       ("En los datos de la beta hay", -.3), ("las fueron juntando una a una|fin", 1.0),
       ["nombre borrado", "estadísticas cifradas", "las pistas a su alrededor", "los mineros de datos", "fueron juntando"], "legendario", y=.54),
    mapa("kalimdor_enus", [(55, 21, "Claro de la Luna", "sátiros y Círculo Cenarion", F("cenarius")), (55, 30, "Cima de Hyjal", "Sylvestris Dusksong", F("hyjal")),
                           (49, 80, "Cráter de Un'Goro", "puzle de pilones")],
         ("Hay un ritual con el Círculo", -.2), ("un puzle de pilones en el cráter de Un'Goro|fin", .6),
         ["Hay un ritual", "encuentros en la Cima", "cráter de Un'Goro"], "LAS PISTAS DEL LEGENDARIO", "lo que los datos no borraron", zmax=1.9),
    pant("nordrassil", "El objeto que se potencia", ("Así que todo apunta", 2.5), zoom=(1.0, 1.12)),
    gran("Hyjal Summit abre", "hyjal", "9 de diciembre", dur=3.4, x=.75, tam=540),
    # =========================================================== cierre
    aba([("cercenarrocas", "Hacha"), ("banana", "Banana"), ("loto", "Loto negro"), ("llave", "Llave")], "Un hacha que mina#2", ("y un legendario sin nombre|fin", .6),
        ["Un hacha que mina#2", "una banana que entiende", "un mercado negro#3", "una llave sin puerta"], "cierre"),
]
ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="15 OBJETOS SECRETOS", en="los quince objetos secretos", dur=2.8, tam=130, color="amarillo", y=.2),
    dict(texto="DE LA BETA", en="Todo esto salió en la beta", dur=2.4, tam=120, color="amarillo", y=.2),
    dict(texto="«CÓMEME»", en="Su descripción entera son dos palabras", dur=3.0, tam=170, color="amarillo", y=.2),
    dict(texto="1,52 %", en="uno coma cincuenta y dos por ciento", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="ES DE LA BANANA", en="es de la banana", dur=2.4, tam=130, color="amarillo", y=.2),
    dict(texto="ATURDIDO", en="el objeto te deja aturdido a ti", dur=2.2, tam=150, color="rojo", y=.2),
    dict(texto="¿+150 %?", en="ciento cincuenta por ciento de velocidad", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="150 DE ORO", en="ciento cincuenta era el precio", dur=2.4, tam=150, color="amarillo", y=.2),
    dict(texto="¿QUÉ ABRE?", en="siguen buscando qué abre", dur=2.6, tam=150, color="amarillo", y=.2),
    dict(texto="9 DE DICIEMBRE", en="vuelve en Forever el nueve de diciembre", dur=2.6, tam=140, color="amarillo", y=.2),
    dict(texto="PRIMAVERA DE 2027", en="la primavera de dos mil veintisiete", dur=2.8, tam=130, color="amarillo", y=.2),
    dict(texto="ESPECULACIÓN", en="Todo esto es especulación", dur=2.4, tam=130, color="rojo", y=.2),
]
SFX = {}
# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/wow/, copiado a sfx/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.22) for e in ("consigue uno y el juego", "Número quince", "Número diez", "Número cinco")]
PISTAS += [dict(sfx="mision_aceptada", en=e, vol=.30) for e in ("Esta es para la Horda", "Lo suelta Rhahk'Zor", "Todo empieza en la Muralla", "Hay un ritual con")]
PISTAS += [dict(sfx="subasta", en=e, vol=.28) for e in ("Unos días después apareció", "con una puja de tres mil")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Hoy te traigo los quince", "Número uno. El primer legendario")]

# APOYOS: tooltips REALES de Wowhead Forever (es-MX) y tarjetas SOLO con datos del guion (fuentes en videos/_investigacion_wow_objetos_secretos_forever.md)
V, GR, RJ = "verde", "gris", "#ff3b3b"
APOYOS = [
    # ---- 15
    dict(en="Es una receta nueva", dur=5.0, x=.72, y=.72, size=.46, wowhead="forever/251525"),
    dict(en="Blizzard aclaró que eso era", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Efecto provisional", calidad=RJ, icono="inv_misc_fish_69",
         lineas=["Antes: múrloc u ogro", dict(t="Ahora: orco ninja o pirata", c=V)])),
    dict(en="Y la nota de los desarrolladores", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Nota de los desarrolladores", calidad="amarillo", icono="inv_misc_note_01",
         lineas=[dict(t="Puede que vuelvan transformaciones parecidas", c=V)])),
    # ---- 14
    dict(en="En el sur de la isla Zephras", dur=5.2, x=.72, size=.50, wowhead="forever/268109"),
    dict(en="Y no hace falta ningún nivel", dur=3.8, x=.72, size=.50, tarjeta=dict(titulo="Saltavientos musical", calidad="azul", icono="inv_frog2_blue",
         lineas=[dict(t="Sin requisito de nivel", c=V), dict(t="Sin requisito de facción", c=V)])),
    dict(en="En Wowhead, el comentario más votado", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Homenaje", calidad="amarillo", icono="inv_frog2_blue",
         lineas=["Ocarina of Time", dict(t="Cantarle a las ranas daba una pieza de corazón", c=V)])),
    # ---- 13
    dict(en="Ahí se abre una misión", dur=4.4, x=.72, size=.50, wowhead="forever/275682"),
    # ---- 12
    dict(en="La mayoría de los jugadores nunca la vio", dur=4.4, x=.72, size=.50, wowhead="forever/282047"),
    dict(en="En la beta el nivel estaba limitado", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="La beta", calidad="azul", icono="ability_hunter_pet_crocolisk",
         lineas=["Nivel máximo: 20", dict(t="Bestia de cloaca: nivel 50", c=RJ), "Solución: bandas enteras"])),
    # ---- 11
    dict(en="Lo más curioso es que en Wowhead", dur=5.0, x=.72, size=.50, wowhead="forever/270226"),
    # ---- 10
    dict(en="Según los que la probaron", dur=5.4, x=.72, size=.50, wowhead="forever/276895"),
    dict(en="En la Temporada de Descubrimiento", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Crisálida transformadora", calidad="azul", icono="inv_misc_web_02",
         lineas=["Equipo de nivel 30", dict(t="Reutilización: 5 minutos", c=GR)])),
    # ---- 9
    dict(en="Es un hacha a dos manos", dur=4.6, x=.72, size=.50, wowhead="forever/872"),
    dict(en="Pero tiene un uso nuevo", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Filones", calidad="verde", icono="trade_mining",
         lineas=["Cobre · Estaño · Plata · Hierro", dict(t="No pide Minería", c=V)])),
    dict(en="Y como las cargas no aparecen", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="En la subasta", calidad="amarillo", icono="inv_throwingaxe_01",
         lineas=["Las cargas no salen en la descripción", dict(t="Nadie sabe cuántas le quedan", c=RJ)])),
    # ---- 8
    dict(en="Número ocho. La Sortija", dur=4.8, x=.28, y=.30, size=.46, wowhead="forever/284715"),
    # ---- 7
    dict(en="Entre sus cosas vende este objeto", dur=5.0, x=.72, size=.50, wowhead="forever/271871"),
    dict(en="y se suma a la zanahoria", dur=3.6, x=.28, y=.30, size=.44, wowhead="classic/11122"),
    dict(en="Y se pueden llevar hasta diez", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Don del galope", calidad="morado", icono="spell_nature_swiftness",
         lineas=["Hasta 10 a la vez", dict(t="¿Se suman entre ellos? Sin confirmar", c=GR)])),
    # ---- 6
    dict(en="En el World of Warcraft original", dur=5.2, x=.72, size=.50, wowhead="classic/13468"),
    # ---- 5
    dict(en="Unos días después apareció", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Madam Swyndle", calidad="amarillo", icono="inv_misc_coin_17",
         lineas=["Casa de subastas del mercado negro", dict(t="Lotes al azar · gana la puja más alta", c=V)])),
    dict(en="Ahora, con oro suficiente", dur=4.6, x=.72, size=.50, wowhead="classic/13335"),
    # ---- 4
    dict(en="Junto a él hay una Página rota", dur=5.2, x=.72, size=.50, tarjeta=dict(titulo="Página rota", calidad="blanco", icono="inv_misc_savageleatherscraps",
         lineas=["«página 155»", dict(t="Y un cuchillo: Fragmento de piedra angular", c=V)])),
    dict(en="Esa página ciento cincuenta y cinco existe", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Manual oficial impreso", calidad="amarillo", icono="inv_misc_book_09",
         lineas=["Página 155", dict(t="Un orco guerrero y un mapa", c=V), "Sur de los Reinos del Este"])),
    dict(en="Según algunos sitios", dur=5.2, x=.72, size=.50, tarjeta=dict(titulo="Según algunos sitios", calidad="gris", icono="inv_misc_stonetablet_04",
         lineas=["Se habría movido a Riverglades", dict(t="Tras un peón del Crepúsculo dormido", c=GR)])),
    # ---- 3
    dict(en="En el sexto episodio del pódcast", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Pódcast oficial · episodio 6", calidad="amarillo", icono="inv_misc_note_02",
         lineas=["Josh Greenfield, «Aggrend»", dict(t="Detrás de él, una pizarra", c=V)])),
    dict(en="Y Quel'Serrar era justo eso", dur=4.6, x=.72, size=.50, wowhead="classic/18348"),
    # ---- 2
    dict(en="En Forever, las monturas, mascotas", dur=5.6, x=.72, size=.50, tarjeta=dict(titulo="Ocultas hasta que las consigas", calidad="morado", icono="inv_misc_questionmark",
         lineas=["Monturas · Mascotas", "Juguetes · Apariencias", dict(t="No salen en tu colección", c=RJ)])),
    # ---- 1
    dict(en="Hay efusiones de luz lunar", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Pistas en los datos", calidad="naranja", icono="spell_nature_starfall",
         lineas=["Efusión de luz lunar", "Don de Cenarius", dict(t="Cargado de tormenta", c="#7ad7ff")])),
    dict(en="Y una teoría muy buena", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Teoría: Stormwraith", calidad="naranja", icono="spell_nature_lightning",
         lineas=["No sale en la lista de jefes", dict(t="¿Modo difícil secreto?", c=RJ)])),
    dict(en="Y hay un mapa de un solo jugador", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="La caída de Archimonde", calidad="naranja", icono="spell_shadow_summoninfernal",
         lineas=["Mapa de un solo jugador", dict(t="Cielo oscurecido de Archimonde", c=RJ)])),
    dict(en="Así que todo apunta", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="¿Bastón legendario?", calidad="naranja", icono="inv_staff_30",
         lineas=["Druidas · Chamanes · Sacerdotes", dict(t="Rama del Árbol del Mundo: 6 recipientes", c=V)])),
]
