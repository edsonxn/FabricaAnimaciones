# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA (wow_objetos_raros): MAPAS REALES con rutas, motion graphics, pegatinas, pantallas,
rótulos y apoyos anclados a las palabras de la voz. Receta: docs/estilo_secuencia_yt.md · formato y tipos: nucleo/secuencia_fx.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera la capa)    python fab.py <v> fx hoja
MAPAS (el usuario, 22-oct-2026: «usa mapas reales del juego para indicar dónde se obtienen o cuando muestres misiones y sus
cadenas con rutas»): mapas de Wowhead Classic en mapas/ (`eses` = rótulos en español; zona: coordenadas del juego de Questie;
mundo/continente: centro de cada zona colocado a mano y pasado al mapa del mundo con `kal()`/`ek()`, comprobado en una hoja).
Nombres en pantalla = localización oficial es-MX de Wowhead (tooltips locale=11, 22-oct-2026).
"""

import os
import mg_tes as T
import mg_wow as M

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=420):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def gran(en, slug, titulo, dur=4.5, x=.25, tam=660):
    return peg(en, slug, titulo, dur, x, .50, tam)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.7, zmin=1.0):
    """Mapa real a cuadro entero con la ruta (mg_wow.ruta): un pin por paso en su marca; la última marca pone el premio en verde."""
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin,
                                           objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def kal(x, y):
    """% del mapa de Kalimdor (-6) -> % del mapa del mundo (-1)."""
    return (128 + (x / 100 * 1022 - 385) * .826) / 1024 * 100, (130 + (y / 100 * 668 - 100) * .858) / 683 * 100


def ek(x, y):
    """% del mapa de los Reinos del Este (-3) -> % del mapa del mundo (-1)."""
    return (700 + (x / 100 * 1024 - 400) * .785) / 1024 * 100, (285 + (y / 100 * 683 - 290) * .786) / 683 * 100


# centro de cada zona en su mapa de continente (comprobados sobre los bordes de zona de Wowhead, 22-oct-2026)
K = dict(teldrassil=(43, 11), costa_oscura=(47.5, 28), claro_luna=(53.5, 20.5), frondavil=(52, 30), cuna=(59, 25),
         azshara=(63.5, 37), vallefresno=(49, 40), feralas=(41.5, 72), marjal=(56.5, 67), tanaris=(57, 84), ungoro=(50, 83),
         silithus=(43, 84), aq=(42, 88))
E = dict(tdp_este=(58.5, 22), tdp_oeste=(51, 22), interior=(57.5, 32), dun_morogh=(45, 53), loch_modan=(52, 52),
         garganta=(48, 59), estepas=(51, 63), ventormenta=(45.5, 67), poniente=(42, 72), argenteos=(43, 30))


def mk(z, t1, t2=None, dx=0.0, dy=0.0, foto=None):
    """Punto del mapa del mundo a partir de una zona de K/E (con desplazamiento opcional en % del mundo) y su foto."""
    x, y = kal(*K[z]) if z in K else ek(*E[z])
    return (x + dx, y + dy, t1, t2, foto)


def F(slug):
    """Foto de un paso del mapa = pegatina real de Wowpedia (pegatinas/<slug>.png)."""
    return os.path.join(_PEG, slug + ".png")


CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== MAPAS REALES con rutas (MG nuevo `ruta`)
    # Regla del 23-oct-2026 (el usuario): en cada paso del mapa sale la FOTO de lo que la voz nombra (personaje, lugar u objeto
    # que hay que juntar): pegatina real con F(slug) o ícono real de Wowhead con "ico:<ícono>" (nombres es-MX de los tooltips).
    # intro: los sitios del video en el mapa del mundo
    mapa("azeroth_eses", [mk("garganta", "Núcleo de Magma", foto=F("ragnaros")), mk("tdp_este", "Stratholme", foto=F("rivendare")),
                          mk("feralas", "La Masacre", foto=F("helnurath")), mk("silithus", "Ahn'Qiraj", foto=F("cthun"))],
         ("Te voy a enseñar en el mapa", -.2), ("que los esconden|fin", .6),
         ["Te voy a enseñar", "dónde se consiguen", "y la ruta", "de las cadenas"], "AZEROTH", "doce objetos, dos continentes"),
    # 12 Puño de Verigan: Ventormenta -> Poniente -> Dun Morogh -> materiales (3 mazmorras, 2 continentes)
    mapa("azeroth_eses", [mk("ventormenta", "Duthorian Rall", "Ventormenta", foto=F("duthorian")),
                          mk("poniente", "Daphne Fontana", "Páramos de Poniente", foto=F("daphne")),
                          mk("dun_morogh", "Jordan Fontana", "puertas de Forjaz", foto=F("jordan")),
                          mk("poniente", "Minas de la Muerte", "Madera de roble de Piedrablanca", -1.2, 2.2, foto="ico:inv_tradeskillitem_01"),
                          mk("loch_modan", "Bailor Petramano", "Envío de mena refinada", foto="ico:inv_crate_01"),
                          mk("argenteos", "Castillo de Colmillo Oscuro", "Martillo de herrería de Jordan", foto="ico:inv_hammer_09"),
                          mk("vallefresno", "Cavernas de Brazanegra", "Gema kor corrupta", foto="ico:inv_misc_gem_ruby_02"),
                          mk("costa_oscura", "Thundris Tejevientos", "Gema kor purificada", foto=F("thundris")),
                          mk("dun_morogh", "Puño de Verigan", "vuelta con Jordan", 1.5, -2.5)],
         ("empieza con Duthorian Rall", -.3), ("dejas de usar a nivel treinta|fin", .4),
         ["Duthorian Rall", "a los Páramos de Poniente", "vas con Jordan Fontana", "Madera de roble blanco", "Bailor Petramano",
          "su martillo perdido", "Cavernas de Brazanegra", "Thundris Tejevientos", "en otro continente", "Son tres mazmorras"],
         "PUÑO DE VERIGAN", "paladín · nivel 20", objeto="inv_hammer_05", zmax=2.0),
    # 11 sable de hielo: Roca Sableinvernal en Cuna del Invierno
    mapa("cuna_invierno_eses", [(49.9, 9.8, "Rivern Ventogélido", "Roca Sableinvernal", F("rivern"))],
         ("porque Rivern Ventogélido", -.2), ("exactamente dos miembros|fin", .9),
         ["Rivern Ventogélido", "exactamente dos miembros"], "CUNA DEL INVIERNO", "Entrenadores de Sableinvernal",
         objeto="ability_mount_pinktiger", zmax=1.5),
    # 10 Ferromazo: entrada de la Montaña Roca Negra en la Garganta de Fuego
    mapa("garganta_fuego_eses", [(34.8, 85.3, "Montaña Roca Negra", "Profundidades de Roca Negra", F("dagran"))],
         ("Para llegar hasta el emperador", -.2), ("hasta el Palacio Imperial|fin", .6),
         ["Montaña Roca Negra", "el Palacio Imperial"], "LA GARGANTA DE FUEGO", "Emperador Dagran Thaurissan",
         objeto="spell_frost_frostbrand", zmax=1.5),
    # 9 Corcel nefasto: Estepas Ardientes -> Cuna del Invierno -> Frondavil -> La Masacre (los objetos del ritual no son ítems
    # en Wowhead: sin foto inventada; en La Masacre sale Lord Hel'nurath, el dueño de los corceles)
    mapa("azeroth_eses", [mk("estepas", "Mor'zul Sangredoble", "Estepas Ardientes", foto=F("morzul")), mk("cuna", "Cuna del Invierno"),
                          mk("frondavil", "Lord Banehollow", "Guarida de Jaedenar", foto=F("banehollow")),
                          mk("feralas", "La Masacre", "el ritual", foto=F("helnurath"))],
         ("La cadena empieza en las Estepas Ardientes", -.2), ("un ritual dentro de La Masacre|fin", .8),
         ["Estepas Ardientes con", "Cuna del Invierno y", "Lord Banehollow", "dentro de La Masacre", "La Masacre|fin"],
         "CORCEL NEFASTO", "la montura épica del brujo", objeto="ability_mount_dreadsteed", zmax=2.0),
    # 8 Quel'Serrar: La Masacre (Feralas) -> Guarida de Onyxia (Marjal Revolcafango)
    mapa("kalimdor_enus", [(41.0, 70.5, "La Masacre", "Compendio de Nostro", "ico:inv_misc_book_11"),
                           (43.0, 72.5, "Tradicionalista Lydros", "el Ateneo", F("lydros")),
                           (56.6, 71.0, "Guarida de Onyxia", "Marjal Revolcafango", F("onyxia"))],
         ("cae en La Masacre", -.3), ("su Respiración profunda la caliente|fin", .4),
         ["cae en La Masacre", "Tradicionalista Lydros", "Guarida de Onyxia", "Respiración profunda"],
         "KALIMDOR", "la ruta de Quel'Serrar", objeto="inv_sword_01", zmax=2.2),
    # 7 Rhok'delar: Núcleo -> Frondavil -> 4 demonios -> Frondavil
    mapa("azeroth_eses", [mk("garganta", "Núcleo de Magma", "Hoja petrificada vieja", foto="ico:spell_nature_resistnature"),
                          mk("frondavil", "Ancianos de Frondavil", "Vartrus, Stoma, Hastat", foto=F("hastat")),
                          mk("ungoro", "Simone la Discreta", "Cráter de Un'Goro"),
                          mk("estepas", "Franklin el Amistoso", "Estepas Ardientes", foto=F("franklin")),
                          mk("silithus", "Nelson the Nice", "Silithus", foto=F("nelson")),
                          mk("cuna", "Artorius el Afable", "Cuna del Invierno", foto=F("artorius")),
                          mk("frondavil", "Rhok'delar", "vuelta con los Ancianos", 1.2, 3.0)],
         ("Empieza con una Hoja petrificada vieja", -.2), ("repartidos por dos continentes|fin", .5),
         ["Hoja petrificada vieja", "Los Ancianos de Frondavil", "Simone la Discreta", "Franklin el Amistoso", "Nelson the Nice",
          "Artorius el Afable", "Son demonios con nombre", "dos continentes"],
         "RHOK'DELAR", "la misión épica del cazador", objeto="inv_weapon_bow_01", zmax=2.0),
    # 6 Destrero: las dos entradas de Stratholme
    mapa("tdp_este_eses", [(31.3, 15.7, "Entrada principal", "lado escarlata", os.path.join(_PAN, "stratholme.jpg")),
                           (47.9, 23.9, "Entrada de servicio", "lado no-muerto", F("rivendare"))],
         ("Stratholme tiene dos entradas", -.2), ("la del lado no-muerto|fin", .6),
         ["Stratholme tiene dos entradas", "la de servicio", "lado no-muerto"],
         "TIERRAS DE LA PESTE DEL ESTE", "Stratholme", objeto="ability_mount_undeadhorse", zmax=1.8),
    # 2 Atiesh: Naxxramas -> Tanaris -> Naxxramas + Ahn'Qiraj -> Stratholme
    mapa("azeroth_eses", [mk("tdp_este", "Naxxramas", "Astilla de Atiesh ×40", 1.0, -1.0, foto="ico:inv_qiraj_jewelblessed"),
                          mk("tanaris", "Anacronos", "Cavernas del Tiempo", foto=F("anacronos")),
                          mk("tdp_este", "Kel'Thuzad", "Cabeza del báculo Atiesh", 2.5, 1.0, foto=F("kelthuzad")),
                          mk("aq", "C'Thun", "Base de Atiesh · Ahn'Qiraj", foto=F("cthun")),
                          mk("tdp_este", "Stratholme", "el demonio Atiesh", -2.0, -0.8, foto=F("atiesh_demonio"))],
         ("Para armarlo hay que juntar", -.2), ("dos espadas en las manos|fin", .4),
         ["cuarenta Astillas de Atiesh", "con Anacronos", "de Kel'Thuzad", "la base de C'Thun", "purificarlo en Stratholme",
          "dos espadas en las manos"],
         "ATIESH", "el bastón de Medivh", objeto="inv_staff_medivh", zmax=2.0),
    # 1 Cetro: Fuerte Cenarion -> Guarida Alanegra -> Tanaris -> Azshara -> Teldrassil -> Claro de la Luna -> gong
    mapa("azeroth_eses", [mk("silithus", "Baristolth del Mar de Dunas", "Fuerte Cenarion", .5, -1.5, foto=F("baristolth")),
                          mk("garganta", "Guarida Alanegra", "Capazote · Nefarian", foto=F("nefarian")),
                          mk("tanaris", "Anacronos", "Cavernas del Tiempo", foto=F("anacronos")),
                          mk("azshara", "Maws", "Fragmento de cetro azul", foto=F("maws")),
                          mk("teldrassil", "Fuego fatuo", "Fragmento de cetro verde", foto="ico:inv_misc_gem_emerald_03"),
                          mk("claro_luna", "Guardián Remulos", "Eranikus", foto=F("remulos")),
                          mk("aq", "Gong del Escarabajo", "Ahn'Qiraj")],
         ("arranca en el Fuerte Cenarion", -.3), ("para todo el reino|fin", .6),
         ["Baristolth del Mar de Dunas", "Señor de linaje Capazote", "con Anacronos#2", "llamado Maws", "fuego fatuo en Teldrassil",
          "Guardián Remulos", "Gong del Escarabajo", "se abre la guerra"],
         "EL CETRO DEL MAR DE DUNAS", "la cadena más larga del Vanilla", objeto="inv_misc_qirajicrystal_05", zmax=2.0),

    # =========================================================== MG nuevos: forja (recetas de legendario) y sorteo (probabilidad)
    dict(tipo="mg", fn=M.forja("SULFURAS, MANO DE RAGNAROS", [
        ("inv_misc_gem_pearl_05", "Ojo de Sulfuras · Ragnaros", None), ("spell_fire_sealoffire", "Lingotes de sulfuron", 8),
        ("inv_ingot_mithril", "Barras de hierro negro", 20), ("inv_misc_stonetablet_05", "Barras de arcanita", 50),
        ("inv_misc_gem_bloodstone_03", "Sangre de la montaña", 10)], ("inv_hammer_unique_sulfuras", "Sulfuras"), "LA DE MÁS DPS"),
         de=("El martillo pide ocho", -.3), a=("la de más daño bruto|fin", .8),
         marcas=["El martillo pide", "ocho lingotes de sulfuron", "veinte barras de hierro", "cincuenta de arcanita",
                 "diez Sangres de la Montaña", "Hasta la Guarida Alanegra", "fue el arma cuerpo"],
         y=.52, sale=.4, nombre="MG forja Sulfuras", ver=1.0),
    dict(tipo="mg", fn=M.forja("TRUENO FURIOSO", [
        ("spell_ice_lament", "Atadura izquierda · Barón Geddon", None), ("spell_ice_lament", "Atadura derecha · Garr", None),
        ("inv_ingot_thorium", "Barras de elementium", 10), ("spell_fire_selfdestruct", "Esencia del Señor del Fuego", None)],
        ("inv_sword_39", "Trueno Furioso"), "PARCHE 1.6 · 12-JUL-2005"),
         de=("el Barón Geddon guarda", -.3), a=("un enano guerrero llamado Wray|fin", .6),
         marcas=["el Barón Geddon guarda", "Garr la derecha", "diez barras de elementium", "la Esencia del Señor del Fuego",
                 "te llevas la espada", "Llegó en el parche"],
         y=.60, sale=.4, nombre="MG forja Trueno", ver=1.0),
    dict(tipo="mg", fn=M.sorteo("BARÓN OSAHENDIDO · STRATHOLME", 5000, "ability_mount_undeadhorse", "Muertes del barón",
                                "DESDE EL PARCHE 3.0.2: 1 %"),
         de=("En Classic la probabilidad", -.2), a=("un acto de caridad|fin", .6),
         marcas=["En Classic la probabilidad", "cinco mil muertes del barón", "la subió al uno por ciento"],
         y=.52, sale=.4, nombre="MG sorteo destrero", ver=1.0),
    dict(tipo="mg", fn=M.contadores("SEÑORES DEL ESCARABAJO · CLASSIC 2019", [
        ("inv_misc_qirajicrystal_05", "Flamegor (Rusia)", 90, 0, 1), ("inv_misc_qirajicrystal_05", "Fairbanks (EE. UU.)", 49, 2, 3)]),
         de=("En Classic de dos mil diecinueve", -.2), a=("con miles de jugadores|fin", .8),
         marcas=["hubo noventa Señores", "en Flamegor", "cuarenta y nueve", "en Fairbanks"],
         y=.62, sale=.4, nombre="MG contadores escarabajo", ver=1.0),

    # =========================================================== pantallas completas (3)
    pant("guarida_onyxia", "La hoja se enfría con el tiempo", ("clavarla en su cadáver|fin", .3), zoom=(1.0, 1.14), pan=(0, 0, .2, -.2)),
    pant("stratholme", "Número seis, las Riendas", ("del Barón Osahendido, en Stratholme|fin", .3), zoom=(1.0, 1.12)),
    pant("karazhan", "abría un portal a la puerta de Karazhan", ("mejor que los jugadores|fin", .3), zoom=(1.0, 1.10), pan=(0, -.3, 0, .2)),

    # =========================================================== pegatinas (fuera de los tramos de mapa)
    # intro
    peg("los jefes soltaban Sulfuras", "sulfuras", "Sulfuras", dur=4.0, x=.13, tam=340),
    peg("y Trueno Furioso", "thunderfury", "Trueno Furioso", dur=3.6, x=.32, tam=340),
    # 12 Verigan
    peg("un paladín podía ganarse", "duthorian", "Duthorian Rall", dur=4.0, x=.17, tam=360),
    peg("Jordan Fontana la bautizó", "jordan", "Jordan Fontana", dur=5.0, x=.17, tam=420),
    # 11 sable
    gran("las Riendas del sable de hielo", "rivern", "Rivern Ventogélido", dur=4.8, x=.25, tam=600),
    peg("ser exaltado con Darnassus", "thundris", "Darnassus", dur=0.1, x=-1, tam=10),   # marcador vacío (sin pegatina)
    # 10 Ferromazo
    gran("Número diez, Ferromazo", "dagran", "Emperador Dagran Thaurissan", dur=5.0, x=.25, tam=620),
    peg("la forjó Franclorn Forjamaestro", "franclorn", "Franclorn Forjamaestro", dur=3.6, x=.13, tam=340),
    peg("del Mariscal Windsor", "windsor", "Mariscal Windsor", dur=4.0, x=.32, tam=340),
    # 9 Corcel nefasto
    gran("el Corcel nefasto", "corcel_nefasto", "Corcel nefasto", dur=4.8),
    peg("una Campana de Dethmoora", "banehollow", "Lord Banehollow", dur=0.1, x=-1, tam=10),   # marcador vacío (sin pegatina)
    peg("El ritual invoca a un corcel", "corcel_nefasto", "Corcel xorothiano", dur=4.0, x=.17, tam=380),
    gran("Los mejores corceles son de Lord Hel'nurath", "helnurath", "Lord Hel'nurath", dur=4.5, x=.75, tam=600),
    peg("el Destrero", "destrero", "Destrero del paladín", dur=4.5, x=.17, tam=420),
    # 8 Quel'Serrar
    gran("Número ocho, Quel'Serrar", "quelserrar", "Quel'Serrar", dur=4.5, x=.25, tam=560),
    peg("El libro, por cierto", "lydros", "Tradicionalista Lydros", dur=4.0, x=.17, tam=380),
    gran("Onyxia es la única banda", "onyxia", "Onyxia", dur=5.0, x=.25, tam=640),
    # 7 Rhok'delar
    gran("Número siete, Rhok'delar", "rhokdelar", "Rhok'delar", dur=4.8, x=.25, tam=620),
    peg("antes del parche uno punto ocho", "hastat", "Hastat el Anciano", dur=4.0, x=.17, tam=380),
    peg("de Azuregos", "azuregos", "Azuregos", dur=3.6, x=.13, tam=340),
    peg("de dragón negro de Onyxia", "onyxia", "Onyxia", dur=3.6, x=.32, tam=340),
    # 6 Destrero
    gran("el caballo esquelético del Barón", "rivendare", "Barón Osahendido", dur=3.9, x=.75, tam=620),
    peg("Era el único caballo esquelético", "deathcharger_reins", "Destrero de la muerte", dur=4.5, x=.17, tam=420),
    peg("los tauren pudieran subirse", "destrero", "Destrero de la muerte", dur=0.1, x=-1, tam=10),   # marcador vacío
    peg("su caballo favorito", "rivendare", "Barón Osahendido", dur=4.0, x=.17, tam=380),
    # 5 Sulfuras
    gran("Número cinco, Sulfuras", "ragnaros", "Ragnaros", dur=4.8, x=.75, tam=620),
    peg("a Lokhtos Tratoscuro", "lokhtos", "Lokhtos Tratoscuro", dur=4.2, x=.17, tam=400),
    peg("en Reddit que por fin", "sulfuras", "Sulfuras, Mano de Ragnaros", dur=4.5, x=.25, y=.50, tam=600),
    # 4 Crematoria
    gran("Número cuatro, la Crematoria corrupta", "crematoria_corrupta", "Crematoria corrupta", dur=4.8, x=.25, tam=620),
    peg("del cofre de los Cuatro Jinetes", "cuatro_jinetes", "Los Cuatro Jinetes", dur=4.0, x=.17, tam=400),
    gran("Detrás se oye al Rey Exánime", "rey_exanime", "El Rey Exánime", dur=4.5, x=.75, tam=620),
    peg("mataba a su propio hijo Renault", "renault", "Renault Mograine", dur=3.8, x=.13, tam=340),
    peg("liberaba a Fairbanks", "fairbanks", "Fairbanks", dur=3.6, x=.32, tam=340),
    # 3 Trueno Furioso
    gran("Número tres, Trueno Furioso", "thunderfury", "Trueno Furioso", dur=4.5, x=.25, tam=600),
    peg("el Príncipe Thunderaan, hijo de Al'Akir", "thunderaan", "Príncipe Thunderaan", dur=4.0, x=.86, y=.16, tam=270),
    peg("con el Alto señor Demitrian", "demitrian", "Alto señor Demitrian", dur=4.0, x=.86, y=.16, tam=270),
    peg("Did someone say Thunderfury", "thunderfury", "¿Alguien dijo Trueno Furioso?", dur=4.0, x=.25, y=.50, tam=560),
    peg("Thunderaan apareció de paseo", "thunderaan", "Príncipe Thunderaan", dur=5.0, x=.75, y=.50, tam=600),
    # 2 Atiesh
    gran("Número dos, Atiesh", "atiesh", "Atiesh", dur=4.5, x=.25, tam=600),
    peg("Fue el primer legendario para lanzadores", "medivh", "Medivh", dur=4.0, x=.75, y=.50, tam=560),
    peg("treinta y nueve astillas", "kelthuzad", "Kel'Thuzad buscaba las astillas", dur=0.1, x=-1, tam=10),   # marcador vacío
    # 1 Cetro
    gran("Número uno, el Cetro del Mar de Dunas", "cetro", "El cetro del Mar de Dunas", dur=4.8, x=.25, tam=560),
    gran("y el tanque negro", "tanque_negro", "Cristal resonador negro qiraji", dur=5.5, x=.25, tam=600),
    peg("Fue la primera montura legendaria", "gong", "Gong del Escarabajo", dur=4.5, x=.17, tam=400),
    # cierre
    peg("Lo seguro es que Onyxia", "onyxia", "Onyxia", dur=3.6, x=.13, tam=340),
    peg("y Roca Negra ya esperan", "dagran", "Profundidades de Roca Negra", dur=3.6, x=.32, tam=340),
]
FX = [d for d in FX if d.get("x", 0) >= 0]   # quita los marcadores vacíos

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="20 AÑOS", en="después de unos veinte años", dur=2.6, tam=150, color="amarillo", y=.2),
    dict(texto="NUNCA EXISTIÓ", en="Esa misión nunca existió", dur=2.4, tam=130, color="rojo", y=.2),
]
SFX = {}
PISTAS = []

# APOYOS: tooltips REALES de Wowhead (classic, es-MX; ids comprobados el 22-oct en nether.wowhead.com) y tarjetas SOLO con datos
# del guion (o de su fuente verificada, en el docstring de guion.py).
V, GRIS, ROJO = "verde", "gris", "#ff3b3b"
APOYOS = [
    # ---- intro
    dict(en="Forever sale el cuatro de noviembre", dur=4.2, x=.72, size=.44, tarjeta=dict(titulo="World of Warcraft Forever",
         calidad="amarillo", icono="inv_misc_map_01", lineas=["Sale el 4 de noviembre de 2026", "Nivel 60 para siempre",
                                                             dict(t="Antes del Núcleo de Magma", c=GRIS)])),
    # ---- 12 Verigan
    dict(en="Número doce, el Puño de Verigan", dur=5.0, x=.72, size=.44, wowhead="classic/6953"),
    dict(en="La quitaron en el parche cuatro punto cero punto tres", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Puño de Verigan",
         calidad="azul", icono="inv_hammer_05", lineas=["Solo paladines · nivel 20", "Horda: Guja templada en sangre",
                                                       dict(t="Quitado en el parche 4.0.3", c=ROJO)])),
    # ---- 11 sable
    dict(en="Número once, las Riendas", dur=5.0, x=.72, size=.44, wowhead="classic/13086"),
    dict(en="La descripción del objeto dice", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="Riendas del sable de hielo",
         calidad="morado", icono="ability_mount_pinktiger", lineas=["100 de oro · Exaltado",
                                                                   dict(t="«…y un buen suministro de ratones falsos y cordel»", c=GRIS)])),
    dict(en="La Horda no tuvo nada parecido", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Entrenadores de Sableinvernal",
         calidad="amarillo", icono="ability_mount_pinktiger", lineas=["Solo Alianza · 2 miembros",
                                                                     dict(t="Horda sin felino hasta el parche 3.2", c=ROJO)])),
    # ---- 10 Ferromazo
    dict(en="La comunidad calcula que sale entre", dur=5.0, x=.72, size=.44, wowhead="classic/11684"),
    dict(en="Las Profundidades de Roca Negra están confirmadas", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Ferromazo",
         calidad="morado", icono="spell_frost_frostbrand", lineas=["0,18 % – 0,59 % (estimación)", dict(t="Roca Negra: confirmada en Forever", c=V)])),
    # ---- 9 Corcel nefasto
    dict(en="Número nueve, el Corcel nefasto", dur=4.5, x=.72, size=.44, wowhead="classic/spell/23161"),
    dict(en="Para eso el brujo necesita", dur=6.5, x=.72, size=.46, anim="fade", tarjeta=dict(titulo="El ritual de La Masacre",
         calidad="morado", icono="ability_mount_dreadsteed", lineas=["Campana de Dethmoora", "Rueda de la Marcha Negra",
                                                                    "Vela del Juicio Final"])),
    dict(en="En el parche dos punto cuatro", dur=4.8, x=.72, size=.44, tarjeta=dict(titulo="Corcel nefasto", calidad="gris",
         icono="ability_mount_dreadsteed", lineas=["2.4.0: pasa al entrenador", dict(t="4.0.1: la cadena desaparece", c=ROJO)])),
    # ---- 8 Quel'Serrar
    dict(en="Todo empieza con un libro", dur=3.8, x=.72, size=.44, wowhead="classic/18401"),
    dict(en="La quitaron en el parche tres punto dos punto dos", dur=4.5, x=.72, size=.44, wowhead="classic/18348"),
    dict(en="Así que, de toda esta lista, Quel'Serrar", dur=4.8, x=.72, size=.44, tarjeta=dict(titulo="Guarida de Onyxia",
         calidad="amarillo", icono="inv_misc_head_dragon_01", lineas=["Única banda clásica confirmada", dict(t="Abre el 9 de diciembre", c=V)])),
    # ---- 7 Rhok'delar
    dict(en="Número siete, Rhok'delar", dur=4.5, x=.72, size=.44, wowhead="classic/18713"),
    dict(en="Además pide tendones de dragón", dur=5.0, x=.72, size=.42, wowhead="classic/18715"),
    # ---- 6 Destrero
    dict(en="Y en el parche uno punto tres", dur=4.6, x=.72, size=.44, wowhead="classic/13335"),
    dict(en="Lo que nadie ha dicho es si la probabilidad", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Riendas de destrero de la muerte",
         calidad="morado", icono="ability_mount_undeadhorse", lineas=["Classic: 0,02 %", "Parche 3.0.2: 1 %", dict(t="Forever: ¿?", c=GRIS)])),
    # ---- 5 Sulfuras
    dict(en="Ragnaros suelta el Ojo de Sulfuras", dur=4.8, x=.72, size=.44, wowhead="classic/17204"),
    dict(en="Y en abril de dos mil veintiséis", dur=5.0, x=.72, size=.44, wowhead="classic/17182"),
    # ---- 4 Crematoria
    dict(en="Al equiparla, el espíritu de Mograine", dur=5.0, x=.72, size=.44, wowhead="classic/22691"),
    dict(en="Además te vuelve hostil", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Crematoria corrupta", calidad="morado",
         icono="inv_sword_2h_ashbringercorrupt", lineas=[dict(t="Alba Argenta: hostil", c=ROJO), dict(t="Cruzada Escarlata: amistosa", c=V)])),
    # ---- 3 Trueno: el MG forja ocupa casi toda la sección; tooltip al final
    dict(en="Fue tan rara y tan presumida", dur=5.0, x=.72, size=.44, wowhead="classic/19019"),
    # ---- 2 Atiesh
    dict(en="Número dos, Atiesh", dur=4.5, x=.72, size=.44, wowhead="classic/22589"),
    dict(en="Y un personaje del juego moderno", dur=5.0, x=.72, size=.44, wowhead="classic/22726"),
    dict(en="En Forever, Naxxramas ni siquiera", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Naxxramas", calidad="gris",
         icono="inv_trinket_naxxramas03", lineas=[dict(t="No anunciada en Forever", c=ROJO)])),
    # ---- 1 Cetro
    dict(en="Número uno, el Cetro", dur=4.5, x=.72, size=.44, wowhead="classic/21175"),
    dict(en="El fragmento rojo sale de Nefarian", dur=1.0, x=.72, size=.40, wowhead="classic/21138"),
    dict(en="El primero en tocarlo", dur=5.0, x=.72, size=.44, wowhead="classic/21176"),
    dict(en="El primero del mundo fue Kalahad", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Primer Señor del Escarabajo",
         calidad="naranja", icono="inv_misc_qirajicrystal_05", lineas=["Kalahad · reino Medivh", "22 de enero de 2006"])),
    dict(en="Fue la primera montura legendaria", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Cristal resonador negro qiraji",
         calidad="naranja", icono="inv_misc_qirajicrystal_05", lineas=["1.ª montura legendaria", "Única hasta Dragonflight",
                                                                      dict(t="Feb. 2009: reinos con la puerta abierta", c=ROJO)])),
    # ---- cierre
    dict(en="Forever todavía no confirma", dur=7.5, x=.72, size=.46, tarjeta=dict(titulo="World of Warcraft Forever", calidad="amarillo",
         icono="inv_misc_map_01", lineas=[dict(t="Núcleo · Naxxramas · Ahn'Qiraj: sin confirmar", c=GRIS),
                                         "Primavera 2027: cadena legendaria nueva", "Verano 2027: banda icónica rehecha"])),
]
APOYOS = [a for a in APOYOS if a.get("dur", 1) > 1.0]   # el fragmento rojo cae justo con el mapa del cetro: fuera
