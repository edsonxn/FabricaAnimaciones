# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja

wow_100_curiosidades_tbc_wotlk (tramo 6, 24-oct-2026: Terrallende, intro + c100…c051):
  · MAPAS: el de Terrallende entero a pantalla en la intro (el recorrido por zonas) y, en cada parada, el mapa REAL de su zona
    en ventana (x=.70) con su FOTO; ruta cuando la voz va de un sitio a otro; la Cicatriz Muerta, a pantalla (viaje de Arthas).
    Coordenadas leídas en mapas/<zona>_rejilla.jpg y, las dudosas, de Wowpedia ({{coords}} del PNJ).
  · MG nuevos (mg_wow): paradero «los cinco héroes de la expedición» (c100), simon «cuatro luces, una secuencia» (c073),
    franquicia «las sucursales de Gurgthock» (c079).
  · Pegatinas de Wowpedia (_pegatinas_bajar.py) y tarjetas SOLO con datos del guion (x=.72; nunca a la vez que un mapa en ventana).
(tramo 7, 26-oct-2026: Rasganorte, c050…c001 + cierre): mapa de Rasganorte entero a pantalla al empezar (c050) y el mismo
  patrón por parada (coordenadas de Wowpedia con _coords.py, verificadas en mapas/<zona>_rejilla.jpg de _rejilla.py).
  · MG nuevos (mg_wow): altares «los dioses que se comieron» (c030), apariciones de Harrison Jones (c031); y del kit:
    paradero «los tres Barbabronce» (c016) y cadena «la cura que nadie tiene» (c001).
"""

import os
import mg_tes as T
import mg_wow as M

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")


def P(slug):
    return os.path.join(_PEG, slug + ".png")


# PEGATINAS — REGLA FIJA DEL CANAL (18-oct-2026): cada personaje/criatura/objeto que nombra la voz, su imagen REAL animada,
# abajo a la izquierda (en fila si la voz enumera); ~1 de cada 5 GRANDE (x=.25, y=.50, tam 560-640) del lado contrario a la tarjeta.
def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=420):
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def gran(en, slug, titulo, dur=4.8, tam=600, x=.25):
    return peg(en, slug, titulo, dur=dur, x=x, y=.50, tam=tam)


# PANTALLA COMPLETA (18-oct-2026): imagen REAL a cuadro entero cuando el clip no enseña lo que la curiosidad necesita ver.
_PAN = os.path.join(_AQUI, "pantallas")


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


# MAPAS REALES CON RUTA (23-oct-2026) + FOTOS EN EL MAPA (23-oct-2026): mapas/<zona>.jpg de Wowhead (es-ES).
_MAP = os.path.join(_AQUI, "mapas")
TEMA_MAPA = "wow"


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, tema=None, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, tema or TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


_ZONA = dict(fuego="Península del Fuego Infernal", zangar="Marisma de Zangar", terokkar="Bosque de Terokkar",
             shattrath="Shattrath", nagrand="Nagrand", filospada="Montañas Filospada", tormenta="Tormenta Abisal",
             sombraluna="Valle Sombraluna", cancion_eterna="Bosque Canción Eterna", tierras_fantasma="Tierras Fantasma",
             quel_danas="Isla de Quel'Danas", bruma_sangre="Isla Bruma de Sangre", paso_muerte="Paso de la Muerte",
             tanaris="Tanaris", boreal="Tundra Boreal", fiordo="Fiordo Aquilonal", dragones="Cementerio de Dragones",
             pardas="Colinas Pardas", zuldrak="Zul'Drak", sholazar="Cuenca de Sholazar", cumbres="Las Cumbres Tormentosas",
             canto_cristal="Bosque Canto de Cristal", invierno="Conquista del Invierno", corona="Corona de Hielo")


def parada(zona, n, puntos, en, marcas=None, dur=5.0, pre=.3):
    """Mapa de la zona en VENTANA (derecha) para «dónde está» la curiosidad n: 1 lugar (su marcador late) o una ruta corta.
    marcas: una por lugar con nombre; por defecto, el propio ancla."""
    return mapa(zona, puntos, de=(en, -pre), a=(en, dur), marcas=marcas or [en], titulo=_ZONA[zona], sub=f"N.º {n}",
                ventana=True, ancho=1000)


CAMARA = {}
FUNDIDO = {}
V, GRIS, ROJO = "verde", "gris", "#ff3b3b"

FX = [
    # ======================================================== INTRO: el recorrido entero, a pantalla
    # el mapa ya trae pintado el nombre de cada zona: solo el inicio y la meta llevan rótulo (24-oct: con los 8, se amontonaban)
    mapa("terrallende", [(.70, .51, "Portal Oscuro", "inicio"), (.57, .50), (.33, .46), (.47, .66), (.50, .73), (.40, .70),
                         (.32, .64), (.28, .50), (.38, .30), (.48, .20), (.58, .17), (.66, .34), (.70, .58),
                         (.67, .80, "Valle Sombraluna", "meta", P("illidan"))],
         de=("Vamos a recorrer las dos expansiones", -.3), a=("es una persona|fin", .6),
         marcas=[("Vamos a recorrer las dos expansiones", .3), ("es una persona|fin", -1.2)], titulo="Terrallende",
         sub="Primera parte del viaje", ajuste=.85, traza=99),

    # ======================================================== PENÍNSULA DEL FUEGO INFERNAL (100-94)
    # ---- 100 Bastión del Honor + MG «los cinco héroes»
    parada("fuego", 100, [(.555, .63, "Bastión del Honor", "meta", P("danath"))], "El Bastión del Honor es la base", dur=4.6),
    dict(tipo="mg", fn=M.paradero("LOS CINCO HÉROES DE LA EXPEDICIÓN", [
        (P("danath"), "Danath Trollbane", "Bastión del Honor"), (P("khadgar"), "Khadgar", "Shattrath"),
        (P("kurdran"), "Kurdran Wildhammer", "Valle Sombraluna"), (P("alleria"), "Alleria", None), (P("turalyon"), "Turalyon", None)],
        sello=("DESAPARECIDOS", 5)),
        de=("Su comandante, Danath Trollbane", -.4), a=("y en Terrallende, nada|fin", 1.4),
        marcas=["Danath Trollbane", "Khadgar te espera", "Kurdran Wildhammer", "Alleria y Turalyon", "y Turalyon", "y en Terrallende, nada"],
        y=.74, sale=.4, nombre="MG paradero", ver=5.0),
    # ---- 99 Camino de la Gloria
    parada("fuego", 99, [(.86, .52, "Portal Oscuro", "inicio"), (.72, .52), (.60, .52), (.48, .52, "Ciudadela del Fuego Infernal", "meta")],
           "El camino que va del Portal Oscuro", marcas=["del Portal Oscuro", "a la Ciudadela del Fuego Infernal"], dur=7.0),
    peg("La Horda de Gul'dan lo construyó", "guldan", "Gul'dan", dur=4.5, tam=460),
    # ---- 98 Segador vil
    gran("el Segador vil", "segador_vil", "Segador vil", dur=4.5, tam=620),
    parada("fuego", 98, [(.48, .52, "Ciudadela del Fuego Infernal", "inicio"), (.55, .43, "El Segador vil", "peligro", P("segador_vil"))],
           "patrulla el centro de la zona", marcas=["Es una máquina de la Legión", "patrulla el centro de la zona"], pre=3.0, dur=4.5),
    # ---- 97 Pozas de Aggonar
    parada("fuego", 97, [(.23, .38, "Templo de Telhamat", "inicio"), (.32, .34), (.42, .31, "Pozas de Aggonar", "meta", P("aggonis"))],
           "Los draenei del Templo de Telhamat", marcas=["del Templo de Telhamat", "te mandan a limpiarlas"], dur=6.5),
    gran("Ve a verlo: es uno de los pocos", "aggonis", "Aggonis", dur=5.0, tam=560),
    # ---- 96 Kazzak
    gran("Lord Kazzak se mudó", "kazzak", "Lord Kazzak", dur=4.5, tam=620),
    parada("fuego", 96, [(.62, .14, "Trono de Kil'jaeden", "meta", P("kazzak"))], "Es la montaña del norte de la península", dur=5.0),
    peg("Su colega Caminante del Destino", "caminante", "Caminante del Destino", dur=4.5),
    # ---- 95 Magtheridon
    parada("fuego", 95, [(.475, .52, "Ciudadela del Fuego Infernal", "peligro", P("magtheridon"))],
           "Debajo de la Ciudadela del Fuego Infernal", dur=4.8),
    peg("hasta que Illidan lo derrotó", "illidan", "Illidan", dur=4.0),
    peg("los orcos de la Mano Arrasada", "orco_vil", "Orco vil", dur=4.0),
    gran("Puedes entrar a verlo encadenado", "magtheridon", "Magtheridon", dur=5.0, tam=620),
    # ---- 94 Salas Arrasadas
    peg("Cuando cae el brujo Nethekurse", "nethekurse", "Nethekurse", dur=4.5),
    gran("Cada tanto Kargath grita", "kargath", "Kargath Puño Maldito", dur=5.0, tam=600),

    # ======================================================== MARISMA DE ZANGAR (93-90)
    parada("zangar", 93, [(.68, .46, "Telredor", "meta", P("telredor"))], "Y los draenei construyeron un pueblo entero",
           marcas=["Telredor, al que se sube"], dur=6.0),
    parada("zangar", 92, [(.82, .38, "El Lodo Muerto", "inicio"), (.66, .40), (.50, .40, "Reserva Colmillo Torcido", "meta", P("vashj"))],
           "Las bombas de vapor de los naga", marcas=["Las bombas de vapor", "hacia el Reserva Colmillo Torcido"], dur=7.0),
    peg("de Lady Vashj drenan el agua", "vashj", "Lady Vashj", dur=5.0),
    peg("Los esporelines te piden ayuda", "esporelin", "Esporelín", dur=4.5, tam=380),
    peg("una mascota murcielespora diminuta", "murcielespora", "Murcielespora diminuta", dur=4.0, x=.75, y=.55, tam=380),
    parada("zangar", 91, [(.68, .46, "Telredor", "inicio"), (.45, .50), (.18, .49, "Esporaggar", "meta", P("esporelin"))],
           "Está escondido al oeste", marcas=["Está escondido al oeste", "detrás de los hongos más grandes"], dur=6.0),
    parada("zangar", 90, [(.50, .40, "Lago Serpiente", "meta")], "en medio del Lago Serpiente", pre=2.5, dur=3.5),
    gran("El Rondador de abajo sale", "rondador", "El Rondador de abajo", dur=5.5, tam=620),

    # ======================================================== TEROKKAR Y SHATTRATH (89-83)
    gran("invocaron a Murmur", "murmur", "Murmur", dur=4.5, tam=560),
    parada("terokkar", 89, [(.42, .52, "Yermos de Hueso", "inicio"), (.39, .66, "Auchindoun", "meta", P("auchindoun"))],
           "Por eso los Yermos de Hueso", marcas=["Por eso los Yermos de Hueso", "son el cráter"], dur=6.5),
    parada("terokkar", 88, [(.72, .80, "Skettis", "meta", P("arakkoa"))], "Skettis, la ciudad de los arakkoa", dur=5.0),
    peg("Ahí vive la sombra de Terokk", "terokk", "Terokk", dur=4.5),
    parada("shattrath", 87, [(.756, .316, "Taberna del Fin del Mundo", "meta", P("haris"))], "En la Taberna del Fin del Mundo de Shattrath",
           pre=1.0, dur=4.6),
    gran("Se llama Haris Pilton", "haris", "Haris Pilton", dur=5.0, tam=600),
    parada("shattrath", 86, [(.70, .27, "Bajo Arrabal", "meta", P("griftah"))], "En el Bajo Arrabal de Shattrath", pre=1.0, dur=4.6),
    peg("Griftah ofrece el jabón con cuerda", "griftah", "Griftah", dur=5.0),
    gran("Se llaman Level Setenta Elite Tauren Chieftain", "l70etc", "L70ETC", dur=5.5, tam=580),
    parada("shattrath", 85, [(.756, .316, "Taberna del Fin del Mundo", "meta", P("l70etc"))], "junto al escenario de la Taberna",
           pre=1.2, dur=4.5),
    peg("Voren'thal el Vidente desertó", "vorenthal", "Voren'thal el Vidente", dur=4.5, x=.13, tam=380),
    peg("se rindió ante A'dal", "adal", "A'dal", dur=4.0, x=.32, tam=380),
    parada("shattrath", 84, [(.24, .33, "Alto Aldor", "inicio", P("aldor")), (.33, .50), (.43, .68, "Grada del Arúspice", "meta", P("vorenthal"))],
           "Las dos facciones viven en terrazas opuestas", marcas=["Las dos facciones viven", "en terrazas opuestas"], dur=6.0),
    peg("llamado Zephyr que vende viajes", "zephyr", "Zephyr", dur=5.0),
    parada("tanaris", 83, [(.65, .47, "Cavernas del Tiempo", "meta")], "a las Cavernas del Tiempo, en Tanaris", pre=1.0, dur=4.5),

    # ======================================================== NAGRAND (82-77)
    parada("nagrand", 82, [(.36, .70, "Oshu'gun", "meta", P("oshugun"))], "La montaña de cristal de Nagrand", dur=5.0),
    peg("dentro agoniza K'ure", "kure", "K'ure", dur=4.5, tam=380),
    parada("nagrand", 81, [(.36, .70, "Oshu'gun", "inicio"), (.47, .50), (.56, .34, "Garadar", "meta", P("garrosh"))],
           "En Garadar, el pueblo de los orcos marrones", marcas=["En Garadar", "Garrosh Grito Infernal"], dur=6.5),
    peg("La Gran Madre Geyah", "geyah", "Gran Madre Geyah", dur=5.0, x=.13, tam=360),
    peg("Thrall en persona viene", "thrall", "Thrall", dur=3.2, x=.31, tam=360),
    gran("Esa escena es el origen", "garrosh", "Garrosh Grito Infernal", dur=5.0, tam=600),
    parada("nagrand", 80, [(.56, .34, "Garadar", "inicio"), (.44, .40), (.33, .45, "Puesto Primasol", "paso"), (.29, .32),
                           (.27, .20, "Colina Mazo de Guerra", "meta", P("corki"))],
           "Primero lo tienen los Sangrelodo", marcas=["Primero lo tienen", "en el Puesto Primasol", "la Colina Mazo de Guerra"], pre=.6, dur=7.5),
    gran("Lo rescatas, vuelve a casa", "corki", "Corki", dur=5.0, tam=580),
    parada("nagrand", 79, [(.43, .21, "Pozo de peleas", "meta", P("gurgthock"))], "un pozo de peleas con un goblin", pre=1.5, dur=4.5),
    peg("con su ayudante Wodin", "wodin", "Wodin", dur=2.6, x=.13, tam=340),
    gran("contra Mogor, el ogro", "mogor", "Mogor", dur=2.6, tam=580),
    dict(tipo="mg", fn=M.franquicia(P("gurgthock"), "LAS SUCURSALES DE GURGTHOCK", [
        ("Nagrand", "Burning Crusade"), ("Anfiteatro de la Angustia", "Wrath of the Lich King"),
        ("Tierras Altas Crepusculares", "Cataclysm"), ("Hermandad de Camorristas", "Mists of Pandaria")], sello=("3 EXPANSIONES", 4)),
        de=("Vuelve en Zul'Drak", -.6), a=("de pequeño emprendedor, nada|fin", 1.0),
        marcas=["Vuelve en Zul'Drak", "con el Anfiteatro de la Angustia", "luego en las Tierras Altas Crepusculares",
                "luego en la Hermandad de Camorristas", "sucursales en tres expansiones"],
        y=.50, sale=.4, nombre="MG franquicia", ver=5.0),
    parada("nagrand", 78, [(.12, .39, "Cordillera del Crepúsculo", "meta")], "Y la Cordillera del Crepúsculo, al oeste", pre=.4, dur=4.8),
    parada("nagrand", 77, [(.43, .45, "Halaa", "meta", P("halaa"))], "Halaa es un pueblo en una isla flotante", dur=5.0),
    peg("con monturas de talbuk", "talbuk", "Talbuk", dur=4.0, tam=360),

    # ======================================================== MONTAÑAS FILOSPADA (76-71)
    peg("mandó a su hijo Sabellian", "sabellian", "Sabellian", dur=4.5),
    gran("Gruul se ganó el apellido", "gruul", "Gruul el Asesino de Dragones", dur=5.0, tam=620),
    parada("filospada", 76, [(.62, .24, "Guarida de Gruul", "peligro", P("gruul"))], "Vuela despacio sobre la zona", dur=4.8),
    parada("filospada", 75, [(.53, .43, "Círculo de Sangre", "meta", P("sablemane"))], "En el Círculo de Sangre", dur=4.6),
    peg("Se llama Baron Sablemane", "sablemane", "Baron Sablemane", dur=5.0, x=.13, tam=380),
    peg("es Sabellian, el hijo de Alamuerte", "sabellian", "Sabellian", dur=3.6, x=.33, tam=420),
    peg("Gorgrom el Devoradragones", "gorgrom", "Gorgrom", dur=4.0, x=.13, tam=360),
    peg("y a Goc", "goc", "Goc", dur=3.5, x=.31, tam=360),
    parada("filospada", 74, [(.53, .57, "Bastión Señor del Trueno", "inicio", P("rexxar")), (.65, .63),
                             (.77, .60, "Aldea Mok'Nathal", "meta", P("leoroxx"))],
           "está sentado en la Bastión Señor del Trueno", marcas=["la Bastión Señor del Trueno", "en una aldea al este"], dur=9.0),
    peg("con su osa Misha", "misha", "Misha", dur=4.0),
    peg("Su padre, Leoroxx, lo echó", "leoroxx", "Leoroxx", dur=4.5),
    parada("filospada", 73, [(.31, .58, "Ogri'la", "meta", P("ogrila"))], "hay ogros que meditan", pre=1.2, dur=4.5),
    dict(tipo="mg", fn=M.simon("CUATRO LUCES, UNA SECUENCIA"),
         de=("juegas con reliquias apexis", -.3), a=("y si fallas, te electrocuta|fin", 2.6),
         marcas=["juegas con reliquias apexis", "a un juego de luces de colores", "y si fallas, te electrocuta"],
         x=.66, y=.50, sale=.4, nombre="MG simon", ver=5.0),
    gran("Entonces aparece Vim'gol el Vil", "vimgol", "Vim'gol el Vil", dur=5.0, tam=600),
    parada("filospada", 71, [(.60, .68, "Estación de Toshley", "meta", P("toshley"))], "Estación de Toshley, el puesto de los gnomos", dur=4.8),
    peg("el ingeniero Smiles O'Byron", "smiles", "Smiles O'Byron", dur=4.5, tam=380),

    # ======================================================== TORMENTA ABISAL (70-66)
    parada("tormenta", 70, [(.34, .645, "Área 52", "meta", P("area52"))], "Si sales de Área cincuenta y dos", dur=4.8),
    parada("tormenta", 69, [(.34, .645, "Área 52", "inicio"), (.40, .58), (.46, .52, "Ecodomo de la Tierra Media", "meta", P("ecodomo"))],
           "Son los ecodomos", marcas=["Son los ecodomos", "para salvar los últimos animales"], pre=.4, dur=5.5),
    peg("construidos por los etéreos del Protectorado", "etereo", "Etéreo del Protectorado", dur=4.5),
    peg("Adentro hay talbuks", "talbuk", "Talbuk", dur=3.5, tam=340),
    peg("una de las forjas de maná de Kael'thas", "kaelthas", "Kael'thas", dur=4.5),
    parada("tormenta", 68, [(.62, .40, "Forja de Maná Ultris", "peligro")], "La Forja de Maná Ultris saltó", dur=4.8),
    peg("un gigante llamado Culuthas", "culuthas", "Culuthas", dur=4.5, tam=400),
    parada("tormenta", 67, [(.62, .40, "Forja de Maná Ultris", "inicio"), (.61, .64), (.58, .88, "Poblado Kirin'Var", "meta", P("vargoth"))],
           "En el Poblado Kirin'Var", marcas=["En el Poblado Kirin'Var", "destruido por Kael'thas"], pre=.4, dur=6.0),
    gran("queda vivo un solo mago, el Archimago Vargoth", "vargoth", "Archimago Vargoth", dur=5.0, tam=560),
    gran("Es Dimensius el Devoratodo", "dimensius", "Dimensius el Devoratodo", dur=5.0, tam=620),
    parada("tormenta", 66, [(.60, .33, "Capitán Saeed", "inicio", P("saeed")), (.62, .40, "Dimensius", "peligro", P("dimensius"))],
           "El Capitán Saeed te lleva marchando", marcas=["El Capitán Saeed", "hasta el lugar"], pre=.4, dur=6.0),

    # ======================================================== VALLE SOMBRALUNA (65-61)
    parada("sombraluna", 65, [(.51, .37, "Mano de Gul'dan", "meta", P("mano_guldan"))], "se llama Mano de Gul'dan", pre=2.0, dur=4.5),
    peg("Gul'dan usó la Cifra de la Condena", "guldan", "Gul'dan", dur=5.0, tam=460),
    gran("al final Illidan se sentó en la cima", "illidan", "Illidan", dur=5.0, tam=620),
    parada("sombraluna", 64, [(.51, .37, "Mano de Gul'dan", "inicio"), (.64, .37), (.77, .34, "Templo Oscuro", "peligro", P("caminante"))],
           "Y en la puerta, afuera", marcas=["Y en la puerta", "patrulla Caminante del Destino"], pre=.4, dur=6.0),
    gran("Maiev Cantosombrío, la guardiana", "maiev", "Maiev Cantosombrío", dur=5.0, tam=600),
    parada("sombraluna", 63, [(.58, .49, "Jaula de la Guardiana", "meta", P("maiev"))], "en la Jaula de la Guardiana", pre=1.8, dur=3.9),
    peg("Akama y sus Lengua de Ceniza", "akama", "Akama", dur=4.5, tam=400),
    parada("sombraluna", 62, [(.70, .85, "Arrecife del Ala Abisal", "meta", P("draco_abisal"))], "En el Arrecife del Ala Abisal", dur=4.8),
    peg("con el Capitán Skyshatter", "skyshatter", "Capitán Skyshatter", dur=4.5),
    gran("te regalan uno de los suyos como montura", "draco_abisal", "Draco abisal", dur=4.5, tam=560),
    gran("juegas como Teron Gorefiend", "teron", "Teron Gorefiend", dur=5.0, tam=620),

    # ======================================================== QUEL'THALAS E ISLA DE QUEL'DANAS (60-56)
    parada("cancion_eterna", 60, [(.63, .28, "Lunargenta", "peligro", P("muru"))], "Debajo de Lunargenta", dur=4.6),
    peg("Kael'thas capturó al naaru M'uru", "kaelthas", "Kael'thas", dur=4.0, tam=400),
    gran("Durante toda la expansión puedes bajar a verlo", "muru", "M'uru", dur=5.0, tam=600),
    peg("Su corazón acaba en manos de Velen", "velen", "Velen", dur=4.5),
    gran("que siguió Arthas con la Plaga", "arthas", "Arthas", dur=4.5, tam=600),
    mapa("tierras_fantasma", [(.405, .14, "Cicatriz Muerta", "inicio", P("arthas")), (.385, .24), (.365, .45), (.35, .64),
                              (.335, .79, "Ciudad de la Muerte", "peligro", P("darkhan"))],
         de=("Puedes caminarla completa", -.3), a=("sigue vivo, o algo parecido|fin", .6),
         marcas=["Puedes caminarla completa", "En el extremo sur está la Ciudad"], titulo="Tierras Fantasma", sub="La Cicatriz Muerta"),
    parada("tierras_fantasma", 58, [(.14, .56, "Aguja Brisaveloz", "meta", P("sylvanas"))], "las ruinas de la Aguja Brisaveloz", pre=1.0, dur=4.8),
    gran("Cuando se lo das, Sylvanas se queda callada", "sylvanas", "Sylvanas", dur=5.0, tam=560),
    parada("tierras_fantasma", 57, [(.79, .62, "Zul'Aman", "meta", P("harrison"))], "debutó en Zul'Aman", pre=1.5, dur=4.5),
    gran("Llegó en el parche dos punto tres", "harrison", "Harrison Jones", dur=5.0, tam=600),
    parada("quel_danas", 56, [(.65, .26, "Bancal del Magister", "meta", P("kaelthas"))], "Y en la Bancal del Magister", dur=5.0),
    gran("Lo dice después de que ya lo mataste", "kaelthas", "Kael'thas", dur=4.5, tam=600),

    # ======================================================== ISLAS DRAENEI, KARAZHAN, CAVERNAS (55-51)
    peg("un draenei llamado Kessel", "kessel", "Kessel", dur=5.0),
    gran("porque el Exodar no es una ciudad", "exodar", "El Exodar", dur=5.0, tam=600),
    parada("bruma_sangre", 54, [(.17, .52, "Espiral Vectorial", "peligro", P("sironas"))], "Los cristales de la Espiral Vectorial", dur=4.8),
    peg("Los elfos de sangre de Sironas", "sironas", "Sironas", dur=4.5, tam=400),
    parada("paso_muerte", 53, [(.46, .72, "Karazhan", "meta", P("aran"))], "En Karazhan, el fantasma", dur=4.6),
    gran("La Sombra de Aran es Nielas Aran", "aran", "Sombra de Aran", dur=5.0, tam=600),
    peg("desde ahí Medivh miraba el cielo", "medivh", "Medivh", dur=5.0, tam=440),
    parada("tanaris", 51, [(.65, .47, "Cavernas del Tiempo", "meta")], "En las Cavernas del Tiempo, las Antiguas", dur=4.8),
    gran("camina un humano llamado Kel'Thuzad", "kelthuzad", "Kel'Thuzad", dur=5.0, tam=560),
    peg("Sally Melenablanca", "whitemane", "Sally Melenablanca", dur=6.5, x=.12, y=.66, tam=320),
    peg("Renault Mograine y el", "renault", "Renault Mograine", dur=5.5, x=.29, y=.66, tam=320),
    peg("el pequeño Jimmy Vishas", "jimmy", "Jimmy Vishas", dur=4.5, x=.46, y=.66, tam=320),
    peg("con Herod el abusivo", "herod", "Herod", dur=3.8, x=.63, y=.66, tam=320),

    # ######################################################## RASGANORTE (tramo 7, 26-oct-2026)
    # OJO anclas: la voz busca la PRIMERA vez que se dicen las palabras en todo el video («Número cincuenta» = el n.º 51);
    # aquí van frases propias de cada curiosidad (_anclas.py comprueba que todo cae en su curiosidad)
    # ======================================================== el recorrido entero, a pantalla
    mapa("rasganorte", [(.22, .60, "Tundra Boreal", "inicio", P("garrosh")), (.40, .70), (.78, .77), (.52, .58), (.76, .57),
                        (.71, .38), (.48, .40), (.24, .42), (.56, .20), (.52, .42), (.37, .49),
                        (.39, .31, "Corona de Hielo", "meta", P("rey_exanime"))],
         de=("En el Bastión Grito de Guerra de la Tundra Boreal", -1.8), a=("acabamos de ver llorando en Nagrand|fin", .5),
         marcas=[("En el Bastión Grito de Guerra de la Tundra Boreal", -1.0), ("acabamos de ver llorando en Nagrand|fin", -.8)],
         titulo="Rasganorte", sub="Segunda parte del viaje", ajuste=.85, traza=99),

    # ======================================================== TUNDRA BOREAL (50-45)
    # ---- 50 Garrosh en Grito de Guerra
    gran("Garrosh Grito Infernal llegó a Rasganorte", "garrosh", "Garrosh Grito Infernal", dur=5.0, tam=600),
    parada("boreal", 50, [(.42, .53, "Bastión Grito de Guerra", "meta", P("saurfang"))], "Le grita a Varok Colmillosauro", dur=5.0),
    # ---- 49 D.E.H.T.A.
    parada("boreal", 49, [(.57, .44, "Campamento D.E.H.T.A.", "meta", P("lathorius"))],
           "hay un campamento de druidas que persigue cazadores", pre=.6, dur=5.0),
    peg("con el Archidruida Lathorius al frente", "lathorius", "Archidruida Lathorius", dur=2.8),
    gran("Sus misiones te mandan a liberar mamuts", "mamut", "Mamut", dur=4.5, tam=560),
    peg("El enemigo es la expedición de Hemet Nesingwary", "nesingwary", "Hemet Nesingwary", dur=5.0),
    # ---- 48 Mechazod
    parada("boreal", 48, [(.57, .18, "Pista de Aterrizaje de Palanqueta", "inicio"), (.61, .24),
                          (.64, .29, "Campos de Géiseres", "meta", P("mechazod"))],
           "En la Pista de Aterrizaje de Palanqueta", marcas=["En la Pista de Aterrizaje de Palanqueta", "se activa en los géiseres"],
           dur=10.0),
    peg("El Maestro de Engranajes Mechazod se activa", "mechazod", "Maestro de Engranajes Mechazod", dur=6.5, x=.13, tam=380),
    peg("los gnomos eran mecagnomos", "mecagnomo", "Mecagnomo", dur=4.5, x=.33, tam=360),
    # ---- 47 Keristrasza
    gran("Keristrasza, la dragona roja que te ayuda", "keristrasza", "Keristrasza", dur=5.0, tam=600),
    peg("contra el azul Malygos", "malygos", "Malygos", dur=4.0),
    parada("boreal", 47, [(.26, .22, "El Nexo", "peligro", P("keristrasza"))], "hasta que él la captura", pre=1.0, dur=4.4),
    # ---- 46 Escudo de Tránsito
    parada("boreal", 46, [(.45, .33, "Saliente Ámbar", "inicio"), (.39, .345), (.33, .35, "Escudo de Tránsito", "meta", P("nexo"))],
           "La isla de Gelidar tiene un puente", marcas=["La isla de Gelidar tiene un puente", "el Escudo de Tránsito"], dur=6.0),
    gran("Malygos robando la magia del mundo", "malygos", "Malygos", dur=4.5, tam=620),
    peg("Y adentro de la isla están el Nexo", "nexo", "El Nexo", dur=5.0, tam=460),
    # ---- 45 Taunka'le
    parada("boreal", 45, [(.77, .35, "Poblado Taunka'le", "meta", P("taunka"))], "En el Poblado Taunka'le viven", pre=.4, dur=5.0),
    gran("Los taunka tienen el pelaje más denso", "taunka", "Taunka", dur=5.0, tam=600),

    # ======================================================== FIORDO AQUILONAL (44-42)
    peg("de dónde salieron los humanos, y la respuesta son los vrykul", "vrykul", "Vrykul", dur=4.5),
    parada("fiordo", 44, [(.67, .53, "Nafsavar", "meta", P("ymiron"))], "En Nafsavar, con un elixir", pre=.4, dur=5.0),
    gran("ves el eco del rey Ymiron", "ymiron", "Rey Ymiron", dur=5.0, tam=600),
    parada("fiordo", 43, [(.575, .44, "Fortaleza de Utgarde", "peligro", P("ingvar"))], "En la Fortaleza de Utgarde, el jefe final",
           pre=.4, dur=5.0),
    peg("Ingvar el Saqueador cae", "ingvar", "Ingvar el Saqueador", dur=4.0, x=.13, tam=380),
    peg("Annhylde la Invocadora baja del techo", "annhylde", "Annhylde la Invocadora", dur=4.5, x=.33, tam=400),
    gran("Fue la primera val'kyr que vio el juego", "valkyr", "Val'kyr", dur=4.5, tam=560),
    peg("antes de que Sylvanas las convirtiera", "sylvanas", "Sylvanas", dur=3.5, x=.80, y=.55, tam=360),
    parada("fiordo", 42, [(.53, .66, "Nuevo Agamand", "meta", P("boticario"))], "En Nuevo Agamand, el pueblo de los Renegados",
           pre=.4, dur=5.0),
    peg("Te mandan a recoger ingredientes", "boticario", "Sociedad Real de Boticarios", dur=4.5),

    # ======================================================== CEMENTERIO DE DRAGONES (41-35)
    parada("dragones", 41, [(.60, .50, "Templo del Reposo del Dragón", "meta", P("reposo_dragon"))],
           "Alrededor del Templo del Reposo del Dragón", pre=.4, dur=5.0),
    gran("está Alexstrasza en persona", "alexstrasza", "Alexstrasza", dur=5.0, tam=600),
    parada("dragones", 40, [(.56, .34, "Reposo de Galakrond", "meta", P("galakrond"))], "En el centro del Cementerio hay un esqueleto",
           pre=.4, dur=5.0),
    gran("Es el protodragón del que descienden", "galakrond", "Galakrond", dur=5.0, tam=620),
    gran("Naxxramas se mudó", "naxxramas", "Naxxramas", dur=4.5, tam=600),
    parada("dragones", 39, [(.78, .46, "Fortaleza de Hibergarde", "inicio"), (.87, .51, "Naxxramas", "peligro", P("naxxramas"))],
           "La necrópolis voló de un continente", marcas=["La necrópolis voló de un continente", "la Plaga la estacionó encima"],
           pre=.3, dur=7.0),
    parada("dragones", 38, [(.38, .17, "Angrathar, la Puerta de Cólera", "peligro", P("puerta_colera"))],
           "La Puerta de Cólera es el lugar de la cinemática", pre=.4, dur=5.0),
    peg("la mancha verde de la peste de Putress", "putress", "Putress", dur=3.0, x=.13, y=.66, tam=360),
    peg("y los cuerpos de Bolvar", "bolvar", "Bolvar Fordragon", dur=4.5, x=.33, y=.66, tam=420),
    peg("y Saurfang el joven", "dranosh", "Saurfang el joven", dur=3.6, x=.53, y=.66, tam=360),
    peg("con Thrall y Varian", "thrall", "Thrall", dur=4.0, x=.13, tam=360),
    peg(("con Thrall y Varian", .6), "varian", "Varian", dur=3.4, x=.31, tam=360),
    parada("dragones", 37, [(.84, .72, "Costa Olvidada", "meta", P("orik"))], "En la Costa Olvidada, al sureste", pre=.4, dur=5.0),
    gran("los hombres que Arthas trajo", "arthas", "Arthas", dur=4.0, tam=560),
    peg("a cazar a Mal'Ganis", "malganis", "Mal'Ganis", dur=4.0, x=.80, y=.55, tam=380),
    peg("Orik Trueheart te da un elixir", "orik", "Orik Trueheart", dur=4.5),
    parada("dragones", 36, [(.73, .23, "Caverna Agonía de Escarcha", "meta", P("agonia_escarcha"))],
           "En la Caverna Agonía de Escarcha puedes ver", pre=.4, dur=5.0),
    peg("Muradin Barbabronce leyendo la inscripción", "muradin", "Muradin Barbabronce", dur=4.0, x=.13, tam=380),
    peg("la espada volando a la mano del príncipe", "arthas", "Arthas", dur=4.0, x=.33, tam=400),
    parada("dragones", 35, [(.71, .75, "Nueva Vega del Amparo", "meta")], "Nueva Vega del Amparo, en el Cementerio", pre=.4, dur=5.0),
    gran("con la Gran General Abbendis siguiendo una voz", "abbendis", "Gran General Abbendis", dur=5.0, tam=560),

    # ======================================================== COLINAS PARDAS (34-31)
    parada("pardas", 34, [(.513, .425, "Fauceparda", "meta", P("furbolg"))], "Fauceparda, la capital de los furbolgs", pre=.4, dur=5.0),
    peg("hasta la prisión de Yogg-Saron", "yogg", "Yogg-Saron", dur=4.0),
    gran("a su dios oso, Ursoc", "ursoc", "Ursoc", dur=5.0, tam=620),
    parada("pardas", 33, [(.59, .27, "Campamento de la Brigada", "meta", P("gryan"))], "La Brigada de los Páramos de Poniente, con Gryan",
           pre=.3, dur=6.0),
    gran("Es la única unidad del juego que pasó", "gryan", "Gryan Stoutmantle", dur=5.0, tam=560),
    parada("pardas", 32, [(.29, .31, "Arroyoplata", "meta", P("huargen"))], "Los tramperos de Arroyoplata", pre=.4, dur=5.0),
    peg("Arugal, el mago del Castillo de Colmillo Oscuro", "arugal", "Arugal", dur=5.0, tam=400),
    parada("pardas", 32, [(.85, .25, "Isla Luna de Sangre", "peligro", P("arugal"))], "Está en la Isla Luna de Sangre", pre=.3, dur=5.0),
    parada("pardas", 31, [(.726, .246, "Ruinas de Drakil'jin", "meta", P("harrison"))], "segunda aparición: las Ruinas de Drakil'jin",
           pre=.3, dur=5.0),
    dict(tipo="mg", fn=M.apariciones(P("harrison"), "LAS APARICIONES DE HARRISON JONES", [
        ("Zul'Aman", "Burning Crusade"), ("Colinas Pardas", "Wrath of the Lich King"), ("Uldum", "Cataclysm"), ("Draenor", None)],
        actual=1, sello=("EN CADA EXPANSIÓN", 4)),
        de=("Después se queda tranquilo en el campamento", -.3), a=("en un templo que no es suyo|fin", .3),
        marcas=[("Después se queda tranquilo en el campamento", .1), ("Después se queda tranquilo en el campamento", 1.0),
                "lo arrastran a Uldum en Cataclysm", "Un arqueólogo que aparece", "en cada expansión"],
        y=.50, sale=.4, nombre="MG apariciones", ver=5.0),

    # ======================================================== ZUL'DRAK (30-25)
    peg("Los trols Drakkari de Zul'Drak sacrificaron", "drakkari", "Trol Drakkari", dur=4.5),
    mapa("zuldrak", [(.534, .368, "Altar de Rhunok", "inicio", P("rhunok")), (.403, .398, "Altar de Sseratus", "paso", P("sseratus")),
                     (.636, .70, "Altar de Har'koa", "meta", P("harkoa"))],
         de=("Los trols Drakkari de Zul'Drak sacrificaron", -.3), a=("y puedes ver los altares|fin", .2),
         marcas=[("Los trols Drakkari de Zul'Drak sacrificaron", .4), "y puedes ver los altares", ("y puedes ver los altares|fin", -.3)],
         titulo=_ZONA["zuldrak"], sub="N.º 30", ventana=True, ancho=1000),
    dict(tipo="mg", fn=M.altares("LOS DIOSES QUE SE COMIERON", [
        (P("rhunok"), "Rhunok", "el oso", False), (P("quetzlun"), "Quetz'lun", "la serpiente alada", False),
        (P("sseratus"), "Sseratus", None, False), (P("akali"), "Akali", "el rinoceronte", False),
        (P("harkoa"), "Har'koa", "la leopardo de las nieves", True)], sello=("SE COMIERON A SUS DIOSES", 5)),
        de=("Mataron a Rhunok el oso", -.2), a=("y aun así perdió la guerra|fin", .6),
        marcas=["Mataron a Rhunok el oso", "a Quetz'lun la serpiente alada", "a Sseratus, a Akali", "a Akali el rinoceronte",
                "Har'koa, la leopardo de las nieves", "se comió a sus dioses"],
        y=.50, sale=.4, nombre="MG altares", ver=5.0),
    parada("zuldrak", 29, [(.747, .43, "Altar de Mam'toth", "peligro")], "En el centro de Zul'Drak hay un cráter enorme", pre=.4, dur=5.0),
    gran("Lo que quedó es el Altar de Mam'toth", "crater_mamtoth", "El cráter de Mam'toth", dur=5.0, tam=620),
    gran("Gymer, el rey de los gigantes, está preso", "gymer", "Gymer", dur=5.0, tam=620),
    gran("Drakuru, el trol simpático", "drakuru", "Drakuru", dur=5.0, tam=560),
    parada("zuldrak", 27, [(.28, .44, "Voltarus", "peligro", P("voltarus"))], "en Voltarus, el zigurat flotante", pre=1.5, dur=5.0),
    peg("el Rey Exánime en persona te dice", "rey_exanime", "El Rey Exánime", dur=4.5),
    parada("zuldrak", 26, [(.473, .571, "Anfiteatro de la Angustia", "meta", P("gurgthock"))], "abrió su segunda sucursal en Zul'Drak",
           pre=.4, dur=5.0),
    peg("Mismo pozo, mismo ayudante trol, Wodin", "wodin", "Wodin", dur=3.5, x=.13, tam=340),
    gran("termina con Vladof el Carnicero", "vladof", "Vladof el Carnicero", dur=5.0, tam=580),
    parada("zuldrak", 25, [(.28, .88, "Fortaleza de Drak'Tharon", "peligro", P("drakkari"))],
           "En la Fortaleza de Drak'Tharon, el último jefe", pre=.4, dur=5.0),

    # ======================================================== CUENCA DE SHOLAZAR (24-21)
    mapa("sholazar", [(.50, .33, "Pilar Iluminado", "inicio"), (.33, .47, "Pilar Toquesol"), (.36, .70, "Pilar Musgoluz"),
                      (.53, .77, "Pilar del Trecho Celestial"), (.68, .60, "Pilar Sangrevida", "meta")],
         de=("con pilares de piedra que la sellan", -.4), a=("con pilares de piedra que la sellan", 5.4),
         marcas=[("con pilares de piedra que la sellan", k * .8) for k in range(5)],
         titulo=_ZONA["sholazar"], sub="N.º 24", ventana=True, ancho=1000),
    gran("y la misma guardiana: Freya", "freya", "Freya", dur=4.5, tam=600),
    parada("sholazar", 24, [(.75, .36, "La Avalancha", "peligro")], "Uno de los pilares cayó, en la Avalancha", pre=.3, dur=4.8),
    parada("sholazar", 23, [(.28, .39, "Pedestal de los Creadores", "inicio"), (.55, .48), (.81, .53, "Mirador de los Creadores", "meta")],
           "en el Pedestal de los Creadores", marcas=["en el Pedestal de los Creadores", "en el Mirador de los Creadores"], pre=.3, dur=6.5),
    gran("despiertas al Etymidian", "etymidian", "El Etymidian", dur=5.0, tam=600),
    parada("sholazar", 22, [(.27, .59, "Campamento Base de Nesingwary", "meta", P("nesingwary"))], "Hemet Nesingwary llegó a Sholazar",
           pre=.4, dur=5.0),
    peg("Loque'nahak, el leopardo espectral", "loquenahak", "Loque'nahak", dur=5.0, tam=430),
    parada("sholazar", 21, [(.536, .566, "Cánope de Hablalluvia", "inicio", P("oraculo")),
                            (.57, .69, "Colina Corazón Frenético", "meta", P("corazon_frenetico"))],
           "En Sholazar tienes que elegir entre dos tribus",
           marcas=["En Sholazar tienes que elegir entre dos tribus", "y la elección correcta trae un dragón"], pre=.3, dur=5.5),
    peg("Los Oráculos, ranas místicas", "oraculo", "Oráculo", dur=4.0, x=.13, tam=380),
    peg("y los Corazón Frenético, lobos chaparros", "corazon_frenetico", "Corazón Frenético", dur=4.0, x=.33, tam=400),
    gran("puede traer un protodraco verde", "protodraco_verde", "Protodraco verde", dur=5.0, tam=600),

    # ======================================================== LAS CUMBRES TORMENTOSAS (20-14)
    parada("cumbres", 20, [(.406, .856, "K3", "meta", P("k3"))], "La base goblin de las Cumbres Tormentosas", pre=.4, dur=5.0),
    parada("cumbres", 19, [(.482, .692, "Poblado Brunnhildar", "meta", P("hyldnir"))], "En el Poblado Brunnhildar, las vrykul",
           pre=.4, dur=5.0),
    gran("Las Hyldnir te capturan", "hyldnir", "Hyldnir", dur=5.0, tam=580),
    peg("para ganarte el favor de Hodir", "hodir", "Hodir", dur=2.6, tam=380),
    parada("cumbres", 18, [(.33, .58, "Templo de las Tormentas", "meta", P("thorim"))], "En lo alto del Templo de las Tormentas",
           pre=.4, dur=5.0),
    peg("Su esposa, Sif, fue asesinada", "sif", "Sif", dur=4.5, x=.13, tam=380),
    peg("el culpable fue su hermano Loken", "loken", "Loken", dur=4.0, x=.33, tam=400),
    gran("Tú le llevas las pruebas al templo", "thorim", "Thorim", dur=5.0, tam=600),
    gran("el Protodraco Perdido en el Tiempo", "ppt", "Protodraco Perdido en el Tiempo", dur=5.0, tam=620),
    mapa("cumbres", [(.31, .69, "Ruta 1", "inicio"), (.35, .76, "Ruta 2"), (.51, .70, "Ruta 3"), (.52, .34, "Ruta 4", "meta", P("ppt"))],
         de=("Aparece en varias rutas, cada muchas horas", -.3), a=("Aparece en varias rutas, cada muchas horas", 6.0),
         marcas=[("Aparece en varias rutas, cada muchas horas", k * .9) for k in range(4)],
         titulo=_ZONA["cumbres"], sub="N.º 17", ventana=True, ancho=1000),
    peg("con una dragona azul, Vyragosa", "vyragosa", "Vyragosa", dur=4.5),
    parada("cumbres", 16, [(.29, .73, "Fuerte Escarcha", "meta", P("muradin"))], "El enano que todo el mundo cree muerto", pre=.3, dur=5.0),
    peg("gracias a Brann, el otro hermano", "brann", "Brann Barbabronce", dur=2.4),
    dict(tipo="mg", fn=M.paradero("LOS TRES BARBABRONCE", [
        (P("magni"), "Magni", "Forjaz"), (P("brann"), "Brann", "Ulduar"), (P("muradin"), "Muradin", "Cumbres, con amnesia")]),
        de=("Los tres Barbabronce están repartidos", -.3), a=("con amnesia entre gigantes|fin", 1.0),
        marcas=["Magni en Forjaz", "Brann en Ulduar", "y Muradin con amnesia"], y=.74, sale=.4, nombre="MG paradero barbabronce", ver=5.0),
    parada("cumbres", 15, [(.422, .248, "Ulduar", "meta", P("algalon"))], "En Ulduar hay un jefe que la mayoría", pre=.4, dur=5.0),
    gran("Algalon el Observador solo aparece", "algalon", "Algalon el Observador", dur=5.0, tam=600),
    gran("La montura más rara de Wrath es la cabeza", "cabeza_mimiron", "Cabeza de Mimiron", dur=5.0, tam=600),
    peg("Mimiron, el guardián ingeniero", "mimiron", "Mimiron", dur=4.0, x=.13, tam=380),
    peg("y Yogg-Saron lo suelta solo si", "yogg", "Yogg-Saron", dur=4.5, x=.33, tam=400),

    # ======================================================== DALARAN Y CANTO DE CRISTAL (13-9)
    gran("Si vas a las Laderas de Trabalomas", "crater_dalaran", "Alterac y Trabalomas, en Classic", dur=5.5, tam=600),
    parada("canto_cristal", 13, [(.27, .33, "Dalaran", "meta", P("dalaran"))], "la ciudad flota ahora sobre el Bosque Canto de Cristal",
           pre=1.0, dur=5.0),
    peg("Korialstrasz, consorte de Alexstrasza", "korialstrasz", "Korialstrasz", dur=5.0, tam=440),
    peg("La ciudad la dirige Rhonin", "rhonin", "Rhonin", dur=4.0, x=.13, tam=360),
    peg("casado con Vereesa Brisaveloz", "vereesa", "Vereesa Brisaveloz", dur=4.5, x=.31, tam=360),
    gran("Es el Refugio del Archimago Vargoth", "vargoth", "Archimago Vargoth", dur=5.0, tam=560),
    gran("Minigob Manacapón anda suelto", "minigob", "Minigob Manacapón", dur=5.0, tam=580),
    parada("canto_cristal", 9, [(.74, .79, "Mirador Brisaveloz", "inicio"), (.78, .49, "Dominio de los Atracasol", "meta")],
           "Hay dos campamentos, un par de misiones", marcas=["Hay dos campamentos, un par de misiones", "y el resto es paisaje"],
           pre=.3, dur=5.5),

    # ======================================================== CONQUISTA DEL INVIERNO (8)
    parada("invierno", 8, [(.505, .205, "Fortaleza de Conquista del Invierno", "meta", P("demoledor"))],
           "Cada dos horas y media los dos bandos", pre=.3, dur=5.5),
    gran("El que gana abre la Cámara de Archavon", "archavon", "Archavon el Vigía de Piedra", dur=5.0, tam=560),

    # ======================================================== CORONA DE HIELO (7-1)
    parada("corona", 7, [(.73, .21, "Torneo Argenta", "meta")], "El Torneo Argenta, en el norte de la Corona de Hielo", pre=.4, dur=5.0),
    gran("y un Caballero Negro se cuela al torneo", "caballero_negro", "El Caballero Negro", dur=5.0, tam=560),
    parada("corona", 6, [(.73, .36, "Caída de Sindragosa", "meta", P("sindragosa"))], "La dragona de hielo que vuela sobre la Ciudadela",
           pre=.4, dur=5.0),
    peg("destrozada por el Alma de Dragón de Alamuerte", "alamuerte", "Alamuerte", dur=4.5),
    gran("hasta que el Rey Exánime la levantó", "sindragosa", "Sindragosa", dur=5.0, tam=620),
    parada("corona", 5, [(.09, .41, "Puerto del Embate", "meta", P("malganis"))], "En Puerto del Embate, los Escarlata", pre=.4, dur=5.0),
    peg("El Gran Almirante Barean Westwind", "westwind", "Barean Westwind", dur=5.5, x=.13, tam=380),
    peg("era el señor del terror disfrazado", "malganis", "Mal'Ganis", dur=4.5, x=.33, tam=420),
    peg("El Martillo de Orgrim y el Rompecielos", "martillo_orgrim", "Martillo de Orgrim", dur=5.0, x=.16, tam=440),
    peg(("El Martillo de Orgrim y el Rompecielos", .8), "rompecielos", "Rompecielos", dur=4.5, x=.80, y=.55, tam=440),
    parada("corona", 3, [(.797, .723, "Pináculo de los Cruzados", "meta", P("tirion"))], "El Pináculo de los Cruzados, el campamento",
           pre=.4, dur=5.0),
    gran("con torre, vendedores y Tirion al frente", "tirion", "Tirion Fordring", dur=5.0, tam=600),
    parada("corona", 2, [(.53, .84, "Ciudadela de la Corona de Hielo", "peligro", P("rey_exanime"))],
           "En las Cámaras de Reflexión, el Rey Exánime", pre=.4, dur=5.0),
    peg("aparece Uther, aparece Arthas", "uther", "Uther", dur=3.5, x=.13, tam=380),
    peg(("aparece Uther, aparece Arthas", .9), "arthas", "Arthas", dur=3.5, x=.32, tam=400),
    peg("Jaina o Sylvanas, según tu bando", "jaina", "Jaina", dur=4.0, x=.13, tam=380),
    peg(("Jaina o Sylvanas, según tu bando", .6), "sylvanas", "Sylvanas", dur=3.6, x=.32, tam=380),
    parada("corona", 1, [(.79, .30, "La Vigilia Silenciosa", "meta", P("bridenbrad"))], "hay un paladín agonizando en una colina",
           pre=.4, dur=5.5),
    dict(tipo="mg", fn=M.cadena("LA CURA QUE NADIE TIENE", [
        (P("alexstrasza"), "Alexstrasza", "Reina de los Dragones", False), (P("remulos"), "Remulos", "Claro de la Luna", False),
        (P("adal"), "A'dal", "Shattrath", False)], remate=("NINGUNO PUEDE CURARLO", 3)),
        de=("vas por una cura con Alexstrasza", -.3), a=("para que la Plaga no lo levante jamás|fin", .5),
        marcas=["vas por una cura con Alexstrasza", "con Remulos en el Claro de la Luna", "y con A'dal en Shattrath",
                "ninguno puede curarlo"], y=.50, sale=.4, nombre="MG cadena bridenbrad", ver=5.0),
    gran("Bridenbrad existió", "bridenbrad", "Cruzado Bridenbrad", dur=6.0, tam=600),

    # ======================================================== CIERRE
    gran("es el cráter de Dalaran", "crater_dalaran", "El cráter de Dalaran", dur=5.0, tam=600),
    peg("yo apuesto que el gnomo del banco", "minigob", "Minigob Manacapón", dur=4.0),
    peg("tienes más paciencia que Thorim", "thorim", "Thorim", dur=4.5),
]
ROTULOS = []
SFX = {}
PISTAS = []


def tar(en, titulo, lineas, dur=5.5, icono="inv_misc_map_01", calidad="amarillo", **kw):
    """Tarjeta a la derecha (x=.72) SOLO con datos del guion."""
    return dict(en=en, dur=dur, x=kw.pop("x", .72), size=kw.pop("size", .44),
                tarjeta=dict(titulo=titulo, calidad=calidad, icono=icono, lineas=lineas), **kw)


APOYOS = [
    # ---- intro
    tar("Cien lugares, dos expansiones y una sola regla", "100 curiosidades", ["Burning Crusade + Wrath of the Lich King",
        dict(t="Todo se puede ir a ver", c=V), dict(t="Cuenta regresiva: 100 → 1", c=GRIS)], dur=6.0, icono="inv_misc_questionmark", calidad="oro"),
    # ---- 100-94
    tar("La fundaron los Hijos de Lothar", "Hijos de Lothar", ["Cruzaron el Portal Oscuro tras la Segunda Guerra",
        dict(t="Atrapados al cerrarse el portal", c=ROJO)], dur=4.6, y=.24, icono="inv_misc_note_01"),
    tar("Bájate de la montura y mira el suelo", "Camino de la Gloria", [dict(t="Pavimentado con restos draenei", c=ROJO),
        dict(t="Calaveras y costillas, una por una", c=GRIS)], icono="spell_shadow_raisedead"),
    tar("Hoy sigue ahí, patrullando", "Segador vil", ["Máquina de la Legión", dict(t="Patrulla", der="desde 2007"),
        dict(t="Un golpe y al cementerio", c=ROJO)], icono="spell_shadow_raisedead"),
    tar("Aggonar cayó ahí, nadie sabe cómo", "Aggonar", ["Señor del foso", dict(t="Su sangre vil envenenó el agua", c=ROJO),
        dict(t="Causa de su muerte: desconocida", c=GRIS)], dur=5.0, icono="spell_shadow_raisedead"),
    tar("En Classic vivía en las Tierras Devastadas", "Lord Kazzak", [dict(t="Classic", der="Tierras Devastadas"),
        dict(t="Burning Crusade", der="Trono de Kil'jaeden", c=V)], dur=5.0, icono="spell_shadow_raisedead", calidad="oro"),
    tar("Su sangre gotea a los barriles", "Horno de Sangre", ["Sangre de Magtheridon",
        dict(t="Mano Arrasada → orcos viles rojos", c=ROJO)], icono="spell_shadow_raisedead"),
    tar("si llevas veinticuatro amigos", "Guarida de Magtheridon", [dict(t="Banda", der="25 jugadores"),
        dict(t="Lo sueltas un rato", c=GRIS)], dur=4.0, icono="inv_misc_key_03", calidad="oro"),
    tar("una hora y veinte para llegar", "Salas Arrasadas · heroico", [dict(t="Desde Nethekurse", der="1 h 20 min", c=ROJO),
        "Prisioneros de tu facción", dict(t="Si tardas, Kargath los ejecuta", c=GRIS)], dur=7.0, icono="inv_misc_key_03"),
    # ---- 93-90
    tar("En la Marisma de Zangar no hay árboles", "Marisma de Zangar", [dict(t="Hongos gigantes", der="40 m"),
        dict(t="Telredor: se sube en elevador", c=GRIS)], dur=5.0),
    tar("Los druidas de la Expedición Cenarion", "Bombas de vapor naga", ["Drenan la marisma hacia el Reserva",
        dict(t="Tú las saboteas una por una", c=V)], icono="inv_misc_note_01"),
    tar("Esporaggar es el único pueblo", "Esporaggar", ["Hongos que caminan y hablan",
        dict(t="Premio", der="murcielespora diminuta", c=V)], dur=5.0, icono="inv_misc_note_01"),
    tar("el segundo jefe no se busca", "Caverna Santuario Serpiente", [dict(t="El Rondador de abajo", der="se pesca", c=V),
        dict(t="Estanque frente a su plataforma", c=GRIS)], dur=5.0, icono="inv_misc_fish_02", calidad="oro"),
    # ---- 89-83
    tar("Auchindoun era la ciudad de los muertos", "Auchindoun", ["Ciudad de los muertos draenei",
        dict(t="Explotó desde adentro", c=ROJO), dict(t="Consejo de la Sombra", c=GRIS)], dur=5.0, icono="spell_shadow_raisedead"),
    tar("Fue la primera zona del juego hecha", "Skettis", [dict(t="Solo con montura voladora", c=ROJO),
        "Diarias de la Guardia del Cielo Sha'tari"], dur=5.0),
    tar("la bolsa se llama, textualmente", "«Bolsa gigantesca»", [dict(t="Espacios", der="22"),
        dict(t="Precio", der="1 200 de oro", c=ROJO)], dur=4.5, icono="inv_misc_bag_10", calidad="morado"),
    tar("En Wrath subió la apuesta", "En Wrath", [dict(t="Espacios", der="24"), dict(t="Precio", der="10 000 de oro", c=ROJO)],
        dur=4.5, icono="inv_misc_bag_10", calidad="morado"),
    tar("Lo echaron de la ciudad una temporada", "Griftah", [dict(t="Exiliado por estafador", c=ROJO),
        "Vendía en la entrada, vigilado", dict(t="Readmitido", der="parche 2.3", c=V)], icono="inv_misc_coin_01"),
    tar("La banda existe de verdad", "Level 70 Elite Tauren Chieftain", ["Empleados de Blizzard",
        dict(t="BlizzCon", der="hasta 2014"), dict(t="Les cerró Metallica", c=GRIS)], dur=5.0, icono="inv_misc_note_01", calidad="oro"),
    tar("Los draenei del Aldor no les creen", "Shattrath: elige bando", [dict(t="Aldor", der="draenei"),
        dict(t="Arúspices", der="elfos de sangre"), dict(t="El otro bando: traidor para siempre", c=ROJO)], dur=5.5),
    tar("Es la agencia de viajes más exclusiva", "Zephyr", ["Viaje directo a las Cavernas del Tiempo",
        dict(t="Hace falta reputación", der="Vigilantes del Tiempo", c=GRIS)], dur=5.0, icono="inv_misc_gem_pearl_04"),
    # ---- 82-77
    tar("Los orcos la tenían por sagrada", "Oshu'gun", [dict(t="En realidad: la Genedar", c=V), "Nave draenei estrellada",
        dict(t="Dentro agoniza K'ure", c=GRIS)], dur=5.5, icono="inv_misc_gem_pearl_04"),
    tar("Se avergüenza de ser hijo de Grom", "Garrosh en Garadar", ["Hijo de Grom Grito Infernal",
        dict(t="Avergonzado de su padre", c=ROJO)], dur=5.0, icono="inv_misc_note_01"),
    tar("La misión de la tercera se llama", "«Corki desapareció otra vez»", [dict(t="Secuestros en la misma zona", der="3", c=ROJO)],
        dur=4.5, icono="inv_misc_note_01"),
    tar("Nagrand tiene dos lugares a los que", "Solo con montura voladora", [dict(t="Meseta Elemental", der="norte"),
        dict(t="Cordillera del Crepúsculo", der="oeste")], dur=6.0),
    tar("El bando que lo controla tiene vendedores", "Halaa", ["Cambia de dueño varias veces al día",
        dict(t="Se conquista bombardeando desde un wyvern", c=ROJO), dict(t="Paga en fragmentos y marcas", c=GRIS)], dur=6.0),
    # ---- 76-71
    tar("Alamuerte mandó a su hijo Sabellian", "Dragones negros en Draenor", ["El linaje de Sabellian, hijo de Alamuerte",
        dict(t="Cazados por los gronn", c=ROJO)], dur=5.0, icono="inv_misc_head_dragon_01"),
    tar("Quiere venganza por los dragones", "Baron Sablemane", [dict(t="En realidad: Sabellian", c=ROJO),
        "Hijo de Alamuerte en forma mortal", dict(t="Vuelve en Dragonflight", c=GRIS)], dur=5.5, icono="inv_misc_head_dragon_01"),
    tar("El campeón de la Horda de Durotar", "Rexxar", ["Héroe de Warcraft III", dict(t="Exiliado por su padre", c=ROJO)],
        dur=4.5, icono="inv_misc_note_01"),
    tar("en el que no pasa nada, hasta que", "Círculo de runas", [dict(t="Jugadores, uno por runa", der="5"),
        dict(t="Sin letrero ni pista", c=GRIS)], dur=6.0, icono="inv_misc_questionmark"),
    tar("Toshley es la Tosche Station", "Estación de Toshley", [dict(t="Tosche Station", der="Star Wars"),
        dict(t="Ataque de bichos", der="Starship Troopers"), dict(t="Smiles O'Byron", der="Star Trek"),
        dict(t="Francotiradores", der="StarCraft")], dur=13.0, icono="inv_misc_questionmark", calidad="oro"),
    # ---- 70-66
    tar("El texto dice: el destello de luz", "Neuralizador A-52", [dict(t="«El destello de luz que no viste", c=V),
        dict(t="no te borró la memoria»", c=V), dict(t="Hombres de Negro", c=GRIS)], dur=6.0, icono="inv_misc_questionmark"),
    tar("Son los únicos zoológicos de Azeroth", "Ecodomos", ["Animales de Draenor en una burbuja",
        dict(t="Afuera: el Vacío Abisal", c=GRIS)], dur=5.0),
    tar("Las otras siguen bombeando energía", "Forjas de maná", ["Energía del Vacío Abisal para la flota de Kael",
        dict(t="Tú las apagas una por una", c=V)], dur=5.0, icono="spell_shadow_raisedead"),
    tar("Te habla a través de una imagen", "Bastón de Vargoth", ["Invoca una copia de Vargoth",
        dict(t="Consejos no pedidos", c=GRIS)], dur=5.0, icono="inv_staff_13", calidad="azul"),
    tar("Fue el primer señor del Vacío del juego", "Dimensius el Devoratodo", [dict(t="Primer señor del Vacío del juego", c=V),
        dict(t="Mucho antes de la trama del Vacío", c=GRIS)], dur=5.0, icono="spell_shadow_raisedead", calidad="oro"),
    # ---- 65-61
    tar("Desde entonces el valle es ceniza", "Mano de Gul'dan", ["Erupción con forma de garra",
        dict(t="Separó a los orcos de los elementos", c=ROJO)], dur=5.0, icono="spell_shadow_raisedead"),
    tar("es el Templo de Karabor", "Templo Oscuro", [dict(t="Antes: Templo de Karabor", c=V), "Lo más sagrado de los draenei",
        dict(t="Horda → Magtheridon → Illidan", c=GRIS)], dur=6.0, icono="inv_misc_key_03", calidad="oro"),
    tar("Te dice, con la humildad de siempre", "Maiev Cantosombrío", ["Persiguió a Illidan diez mil años",
        dict(t="«Ella sola bastaba»", c=V)], dur=5.0, icono="inv_misc_note_01"),
    tar("Y en la ceremonia final aparece Illidan", "Ala Abisal · exaltado", [dict(t="Premio", der="draco abisal", c="morado"),
        dict(t="Illidan descubre al espía", c=ROJO)], dur=5.5, icono="ability_mount_netherdrakepurple", calidad="morado"),
    tar("El espíritu del primer caballero", "Teron Gorefiend", ["Primer caballero de la muerte",
        dict(t="Te posee para matar a un dragón", c=ROJO), dict(t="Luego, jefe del Templo Oscuro", c=GRIS)], dur=6.0,
        icono="spell_shadow_raisedead"),
    # ---- 60-56
    tar("hasta que en el parche dos punto cuatro", "M'uru", ["Prisionero de los Caballeros de Sangre",
        dict(t="Kael lo roba", der="parche 2.4", c=ROJO), dict(t="Su corazón enciende la Fuente del Sol", c=V)], dur=6.0,
        icono="inv_misc_gem_pearl_04", calidad="oro"),
    tar("Hay una franja de tierra muerta", "La Cicatriz Muerta", ["El camino de la Plaga a la Fuente del Sol",
        dict(t="Ni una hoja en veinte años", c=ROJO)], dur=5.5, icono="spell_shadow_raisedead"),
    tar("Un collar, el collar de la Dama", "El collar de la Dama", ["Te lo entrega una aparición",
        dict(t="Llévaselo a Sylvanas, a Entrañas", c=V)], dur=5.0, icono="inv_jewelry_ring_03"),
    tar("Es la única vez en todo el juego", "Lamento de los Altonato", [dict(t="La única vez que Sylvanas canta", c=V)],
        dur=4.5, icono="inv_misc_note_01", calidad="oro"),
    tar("Después lo encuentras en las Colinas Pardas", "Harrison Jones", [dict(t="Debut", der="Zul'Aman · 2.3"),
        "Colinas Pardas · Uldum · Draenor"], dur=5.0, icono="inv_misc_note_01"),
    tar("La Ofensiva Sol Devastado abría", "Ofensiva Sol Devastado", ["Vendedores, portal y posada",
        dict(t="Se abrían con las diarias del servidor", c=V), dict(t="Servidores lentos: semanas sin tienda", c=GRIS)], dur=6.0),
    # ---- 55-51
    tar("el chiste es Han Solo", "La Carrera de Kessel", ["Avisas a tres aldeas en elekk",
        dict(t="Han Solo y su Kessel Run", c=GRIS)], dur=5.0, icono="inv_misc_note_01"),
    tar("Si entras al Castillo en Terrallende", "El Exodar", [dict(t="Un ala del Castillo de la Tempestad", c=V),
        "Los mismos pasillos"], dur=5.0, icono="inv_misc_gem_pearl_04"),
    tar("Es la única zona inicial del juego", "Isla Bruma de Sangre", [dict(t="Roja por la radiación", c=ROJO),
        "Agua, tierra y animales envenenados"], dur=5.0, icono="spell_shadow_raisedead"),
    tar("Y en el teatro de la torre", "El teatro de Karazhan", ["El Mago de Oz", "Caperucita Roja", "Romulo y Julianne",
        dict(t="Una obra al azar", c=GRIS)], dur=6.5, icono="inv_misc_note_01", calidad="oro"),
    tar("Adentro, y esto lo conocemos", "Criptas de Karazhan", [dict(t="Nunca se abrieron oficialmente", c=ROJO),
        "Los pecadores invertidos", dict(t="Hechas completas, nunca usadas", c=GRIS)], dur=8.0, icono="inv_misc_key_03"),
    tar("Son los futuros jefes del Monasterio", "Antiguas Laderas de Trabalomas", ["Costasur antes de la Plaga",
        dict(t="Los villanos del Monasterio, de niños", c=V)], dur=5.5, y=.26, icono="inv_misc_questionmark", calidad="oro"),

    # ######################################################## RASGANORTE (tramo 7)
    # ---- 50-45
    tar("Entre un pueblo y el otro hay una expansión", "Garrosh, dos expansiones", [dict(t="Burning Crusade", der="Garadar"),
        dict(t="Wrath", der="señor supremo de la Horda", c=ROJO), dict(t="Así se fabrica un tirano", c=GRIS)], dur=6.0,
        icono="inv_misc_note_01"),
    tar("Druidas por el Trato Ético y Humano", "D.E.H.T.A.", ["Druidas por el Trato Ético y Humano de los Animales",
        dict(t="La parodia de PETA", c=GRIS)], dur=5.0, icono="inv_misc_note_01"),
    tar("matar cazadores y recoger sus orejas", "Misiones de D.E.H.T.A.", ["Liberar mamuts de las trampas",
        dict(t="Matar cazadores", c=ROJO), dict(t="Recoger sus orejas", c=ROJO), dict(t="Muy ético", c=GRIS)], dur=5.0,
        icono="inv_misc_note_01"),
    tar("Mechazod ofrece curarlos", "La Maldición de la Carne", [dict(t="Antes", der="mecagnomos de los titanes"),
        dict(t="Ahora", der="gnomos de carne", c=ROJO), dict(t="«Gracias, pero no»", c=GRIS)], dur=6.0, icono="inv_misc_gear_01"),
    tar("Cuando entras a la mazmorra, el último jefe es ella", "El Nexo · último jefe", [dict(t="Keristrasza", c=ROJO),
        "Congelada por Malygos como consorte", dict(t="La liberas de la única manera posible", c=GRIS)], dur=6.0,
        icono="spell_frost_frostnova"),
    tar("tres instancias en una roca", "Gelidar", [dict(t="El Nexo", c=V), dict(t="El Oculus", c=V),
        dict(t="El Ojo de la Eternidad", c=V), dict(t="Tres instancias en una roca", c=GRIS)], dur=5.0, icono="inv_misc_key_03"),
    tar("Son parientes de los tauren de Mulgore", "Taunka", [dict(t="Primos de los tauren", der="Mulgore"),
        "Separados hace milenios", dict(t="Juramento de sangre con la Horda", c=V)], dur=6.0, icono="inv_misc_note_01"),
    # ---- 44-42
    tar("Algunos padres los escondieron", "El origen de los humanos", ["Bebés vrykul débiles y pequeños",
        dict(t="Ymiron ordena matarlos", c=ROJO), dict(t="Sus descendientes: Ventormenta y Lordaeron", c=V)], dur=6.5,
        icono="inv_misc_note_01", calidad="oro"),
    tar("Y el fiordo está lleno de ellas", "Fortaleza de Utgarde", [dict(t="Ingvar cae a media pelea", c=ROJO),
        "Annhylde lo levanta como no-muerto", dict(t="La primera val'kyr del juego", c=V)], dur=5.0, icono="inv_misc_key_03"),
    tar("Es la Sociedad Real de Boticarios", "Nuevo Agamand", ["Una peste nueva, probada en vrykul",
        dict(t="Explota en la Puerta de Cólera", c=ROJO), dict(t="La Horda, cómplice sin saberlo", c=GRIS)], dur=6.5,
        icono="spell_shadow_raisedead"),
    # ---- 41-35
    tar("La Plaga llegó a levantar esos huesos", "Cementerio de Dragones", ["A donde los dragones van a morir",
        dict(t="Santuarios", der="5, uno por vuelo"), dict(t="La Plaga levanta los huesos", c=ROJO)], dur=6.0,
        icono="inv_misc_head_dragon_01"),
    tar("Puedes caminar dentro de su caja torácica", "Galakrond", ["El protodragón del que descienden todos",
        dict(t="Devoraba a su propia especie", c=ROJO), dict(t="La cabeza: más grande que una posada", c=GRIS)], dur=5.5,
        icono="inv_misc_head_dragon_01", calidad="oro"),
    tar("En Classic flotaba sobre las Tierras de la Peste", "Naxxramas", [dict(t="Classic", der="Tierras de la Peste"),
        dict(t="Wrath", der="Cementerio de Dragones", c=V)], dur=4.5, icono="spell_shadow_raisedead"),
    tar("En Classic sigue completa", "La Puerta de Cólera", [dict(t="Wrath original", der="abría la Batalla por Entrañas"),
        dict(t="Cataclysm", der="la borró", c=ROJO), dict(t="Classic", der="sigue completa", c=V)], dur=6.0,
        icono="spell_shadow_raisedead", calidad="oro"),
    tar("Les prometió que volverían a casa", "La Primera Legión", ["Los hombres que Arthas trajo",
        dict(t="Les quemó los barcos", c=ROJO), dict(t="Veinte años esperando en la playa", c=GRIS)], dur=6.0,
        icono="spell_shadow_raisedead"),
    tar("Todo el mundo salió de ahí convencido", "¿Murió Muradin?", [dict(t="Todos creen que sí", c=GRIS),
        dict(t="El juego nunca lo dice", c=V)], dur=5.0, icono="inv_misc_questionmark"),
    tar("Fundaron un pueblo entero, con catedral", "Embate Escarlata", ["Huyeron en barco a Rasganorte",
        dict(t="Catedral y puerto", der="Nueva Vega del Amparo"), dict(t="Siguen una voz", c=ROJO)], dur=6.0,
        icono="inv_misc_note_01"),
    # ---- 34-31
    tar("Tú lo matas en las raíces del árbol", "Vordrassil", ["Un árbol del mundo fallido",
        dict(t="Sus raíces llegaron a Yogg-Saron", c=ROJO), dict(t="Ursoc volvió corrompido", c=GRIS)], dur=6.0,
        icono="spell_shadow_raisedead"),
    tar("Reconoces a los personajes de las misiones", "Brigada de los Páramos de Poniente", [dict(t="Classic", der="milicia contra los Defias"),
        dict(t="Wrath", der="guerra contra la Horda", c=V), dict(t="A treinta grados bajo cero", c=GRIS)], dur=6.0,
        icono="inv_misc_note_01"),
    tar("El canal ya contó la historia de Arugal", "Arugal", [dict(t="Classic", der="Colmillo Oscuro"),
        dict(t="Wrath", der="sombra en Rasganorte", c=ROJO), dict(t="Lo matas por segunda vez", c=GRIS)], dur=5.5,
        icono="spell_shadow_raisedead"),
    # ---- 29-25
    tar("Único caso de dios que eligió volarse", "Mam'toth", ["El dios mamut", dict(t="Se destruyó a sí mismo", c=ROJO),
        dict(t="Se llevó el altar y a los sacerdotes", c=GRIS)], dur=5.5, icono="spell_shadow_raisedead"),
    tar("Dura cinco minutos y es lo más poderoso", "Gymer, Rey de la Tormenta", [dict(t="Duración", der="5 minutos"),
        dict(t="Viajas en su hombro", c=V), dict(t="Él lanza trols; tú eliges", c=GRIS)], dur=6.0, icono="inv_misc_questionmark",
        calidad="oro"),
    tar("Pasaste dos zonas trabajando para los dos lados", "Drakuru", [dict(t="Colinas Pardas", der="trol simpático"),
        dict(t="Zul'Drak", der="caballero de la muerte", c=ROJO), dict(t="Lo matas por orden de Arthas", c=GRIS)], dur=6.0,
        icono="spell_shadow_raisedead"),
    tar("La recompensa final es un anillo", "Anfiteatro de la Angustia", [dict(t="Último rival", der="Vladof el Carnicero"),
        dict(t="Premio", der="anillo o arma épica", c="morado"), dict(t="2.ª sucursal de Gurgthock", c=GRIS)], dur=6.0,
        icono="inv_jewelry_ring_03", calidad="morado"),
    tar("Es la única mazmorra en la que el grupo", "Drak'Tharon · último jefe", [dict(t="El Profeta Tharon'ja", c=ROJO),
        "Te convierte en esqueleto", dict(t="Habilidades nuevas; luego, tu carne", c=GRIS)], dur=6.0, icono="spell_shadow_raisedead"),
    # ---- 24-21
    tar("El Avatar de Freya te recibe en persona", "Cuenca de Sholazar", ["Reserva natural de los titanes",
        dict(t="Hermana del Cráter de Un'Goro", c=V), dict(t="Un pilar caído: entra la Plaga", c=ROJO)], dur=6.0,
        icono="inv_misc_questionmark"),
    tar("Es el único viaje intercontinental gratis", "Puerta de los titanes", [dict(t="Sholazar", der="Rasganorte"),
        dict(t="Un'Goro", der="Kalimdor", c=V), dict(t="La usan cuatro personas", c=GRIS)], dur=5.5, icono="inv_misc_map_01",
        calidad="oro"),
    tar("Para los cazadores era la mascota más buscada", "Loque'nahak", [dict(t="Bestia espiritual", c=V), "Aparece cada muchas horas",
        dict(t="Medio servidor acampó por turnos", c=GRIS)], dur=6.0, icono="inv_misc_questionmark", calidad="oro"),
    tar("La mayoría eligió a los lobos", "Elige tribu", [dict(t="Oráculos", der="huevo misterioso", c=V),
        dict(t="Corazón Frenético", der="sin montura", c=ROJO)], dur=5.5, icono="inv_misc_questionmark"),
    # ---- 20-14
    tar("Es el K dos de la vida real", "K3", [dict(t="K2", der="la 2.ª cima del mundo"), dict(t="K3", der="un número más", c=V)],
        dur=5.5, icono="inv_misc_questionmark"),
    tar("Montas sus osos, peleas en su arena", "Poblado Brunnhildar", ["Las vrykul no aceptan hombres",
        dict(t="Te disfrazan de guerrera gigante", c=V), dict(t="Tres metros y trenzas", c=GRIS)], dur=6.0, icono="inv_misc_note_01"),
    tar("Thorim dejó de gobernar", "Thorim", ["Su esposa Sif, asesinada", dict(t="El culpable: su hermano Loken", c=ROJO),
        dict(t="Un dios deprimido", c=GRIS)], dur=5.0, icono="inv_misc_note_01"),
    tar("Si ves a alguien quieto en lo alto", "Protodraco Perdido en el Tiempo", [dict(t="Montura garantizada", c=V),
        "Comparte lugar con Vyragosa", dict(t="Años esperando en una roca", c=GRIS)], dur=6.0, icono="inv_misc_head_dragon_01",
        calidad="morado"),
    tar("Se hace llamar Yorg Stormheart", "Yorg Stormheart", ["Rey de los enanos de Fuerte Escarcha",
        dict(t="En realidad: Muradin Barbabronce", c=V), dict(t="El hielo le borró la memoria", c=GRIS)], dur=6.0,
        icono="inv_misc_questionmark", calidad="oro"),
    tar("Es un enviado de los titanes", "Algalon el Observador", [dict(t="Requisito", der="4 guardianes en difícil"),
        dict(t="Tiempo", der="1 hora", c=ROJO), dict(t="Decide si Azeroth se reinicia", c=GRIS)], dur=6.5, icono="inv_misc_key_03",
        calidad="oro"),
    tar("Veinticinco personas, el jefe final", "Cabeza de Mimiron", [dict(t="Banda", der="25 jugadores"),
        dict(t="Yogg-Saron sin ayuda de guardianes", c=ROJO), dict(t="Trofeo de servidor · 2009", c=GRIS)], dur=6.0,
        icono="inv_misc_questionmark", calidad="oro"),
    # ---- 13-9
    tar("los magos levantaron la ciudad completa", "Dalaran", [dict(t="Classic", der="burbuja violeta"),
        dict(t="Wrath", der="vuela a Rasganorte", c=V), dict(t="Cataclysm", der="el cráter, un lago", c=GRIS)], dur=6.0,
        icono="inv_misc_map_01"),
    tar("En Dalaran, la plataforma de vuelo", "Alto de Krasus", ["Krasus no es un mago", dict(t="Es Korialstrasz, un dragón", c=V),
        dict(t="Consorte de Alexstrasza", c=GRIS)], dur=6.0, icono="inv_misc_head_dragon_01"),
    tar("si encuentras ocho libros de magia", "Educación Superior", [dict(t="Libros repartidos", der="8"),
        "Aparecen y desaparecen", dict(t="Abre otra sala secreta", c=V)], dur=6.0, icono="inv_misc_note_01", calidad="oro"),
    tar("una carta con una varita", "Hacedor de Travesuras", [dict(t="Varita que convierte en oveja", c=V), "Solo dentro de Dalaran",
        dict(t="Parche 3.1", c=GRIS)], dur=6.0, icono="inv_staff_13", calidad="azul"),
    tar("Los árboles son de cristal porque", "Bosque Canto de Cristal", ["Cristalizado por los dragones azules",
        dict(t="Batalla contra los Altonato de Shandaral", c=GRIS), dict(t="Casi sin misiones", c=V)], dur=6.0,
        icono="inv_misc_gem_pearl_04"),
    # ---- 8-1
    tar("Es la única banda del juego cuya puerta", "Cámara de Archavon", [dict(t="Jefes", der="4"),
        dict(t="Solo para el dueño del lago", c=ROJO), dict(t="¿Perdiste? Vuelve en 2 h 30", c=GRIS)], dur=6.0,
        icono="inv_misc_key_03", calidad="oro"),
    tar("En el parche tres punto uno aparecieron las obras", "Torneo Argenta", [dict(t="Parche 3.1", der="las obras"),
        "Semana a semana: carpa y gradas", dict(t="Luego, el Coliseo de los Cruzados", c=V)], dur=6.0, icono="inv_misc_note_01"),
    tar("El cráter de su caída tiene su silueta", "Caída de Sindragosa", ["Consorte de Malygos",
        dict(t="Muerta en la Guerra de los Ancestros", c=ROJO), dict(t="Diez mil años después: dracoliche", c=GRIS)], dur=6.0,
        icono="spell_frost_frostnova"),
    tar("Mal'Ganis se escapa, como siempre", "Mal'Ganis", [dict(t="Stratholme", der="empujó a Arthas"),
        dict(t="Puerto del Embate", der="era Barean Westwind", c=ROJO), dict(t="Se escapa otra vez", c=GRIS)], dur=5.5,
        icono="spell_shadow_raisedead"),
    tar("Hay que volar hasta ellos", "Naves de guerra", ["Una por facción", "Misiones, vendedores y cañones",
        dict(t="Los únicos pueblos en movimiento", c=V)], dur=6.0, icono="inv_misc_map_01"),
    tar("Al llegar es una colina vacía", "Pináculo de los Cruzados", [dict(t="Al llegar", der="colina vacía"),
        dict(t="Tras la cadena", der="fuerte completo", c=V), dict(t="Cambio de fases", c=GRIS)], dur=6.0, icono="inv_misc_map_01"),
    tar("Es la única mazmorra donde el jefe final no se mata", "Cámaras de Reflexión", [dict(t="El Rey Exánime te persigue", c=ROJO),
        "Muros de hielo, uno tras otro", dict(t="No se gana: se huye", c=GRIS)], dur=6.0, icono="spell_frost_frostnova"),
    tar("Bridenbrad existió", "Cruzado Bridenbrad", ["Hermano de un empleado de Blizzard", dict(t="Murió de cáncer", c=GRIS),
        dict(t="La cadena de misiones es su funeral", c=V)], dur=7.0, icono="inv_misc_note_01", calidad="oro"),
    # ---- cierre
    tar("Y esas son las cien", "100 curiosidades", [dict(t="Terrallende", der="100 → 51"), dict(t="Rasganorte", der="50 → 1"),
        dict(t="Todas siguen ahí", c=V)], dur=6.0, icono="inv_misc_questionmark", calidad="oro"),
]
