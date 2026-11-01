# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 10 cosas que DEBES hacer la primera semana de WoW Forever» (motor SECUENCIA YT, Crónicas de
Warcraft, 28-oct-2026; se publica el 1-nov, 3 días ANTES del lanzamiento).
- Abre la campaña Overgear de noviembre (scene-029..035): kit «WoW - Forever (nov)» como en wow_jugadores_rompieron, recorrido
  por overgear.com/games/wow-forever/coaching en scene-032 (`medios/_archivo/coaching_web.mp4`, el brief exige screencast) y
  el creativo del código CRONICAS10_forever (croma) hasta scene-036, sin audio (el código lo dice nuestra voz).
- MG NUEVOS de este guion (nucleo/mg_wow.py): `calendario` (la semana del 1 al 11-nov con HOY, el día que abre y la franja
  del amigo gratis; vuelve en el n.º 1 con el cierre de la reserva), `experiencia` (dos barras: sin nada / con comida +
  hoguera + bolsa), `reglas` (los tipos de servidor como puertas: se elige JcJ, candado y una facción tachada) y `nombre`
  (el campo de nombre y apellido que acepta o rechaza).
- COMENTARIOS REALES (regla del 28-oct): Fede en el gancho, 2 de agradecimiento tras el patrocinio, yuno en la cocina, 6 de
  Darrowshire en el anuncio y 2 en el cierre (tarjetas `pegatinas/com_<id>.png` de `yt comentario`).
- Mapa con ruta de la Bolsa de dormir (beta) y «¿dónde están?» de las mazmorras nuevas.
  python fab.py wow_primera_semana apoyos | fx hoja | fx
"""
import os

import mg_tes as T
import mg_wow as M

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"                   # copias de D:\Cronicas de Warcraft\Overgear\ (kit Forever en forever\)
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"          # rótulo en verde de 10 s: «-10% WITH PROMO CODE CRONICAS10» → «LINK IN…»
CODIGO = ("scene-036", -9.17)   # el creativo entra 2,5 s antes de «CRONICAS10» (296,26 s) y acaba en «gracias»


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=420):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def gran(en, slug, titulo, dur=4.5, x=.25, tam=660):
    return peg(en, slug, titulo, dur, x, .50, tam)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    """Comentario REAL del canal (tarjeta de `yt comentario`), sin título."""
    return peg(en, "com_" + cid, "", dur, x, y, tam)


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.7, zmin=1.0):
    """Mapa real a cuadro entero con la ruta (mg_wow.ruta): un pin por paso en su marca, con la foto de lo que se nombra."""
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin,
                                           objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def kal(x, y):
    """% del mapa de Kalimdor (-6) -> % del mapa del mundo (-1) (calibrado en wow_objetos_raros, 22-oct-2026)."""
    return (128 + (x / 100 * 1022 - 385) * .826) / 1024 * 100, (130 + (y / 100 * 668 - 100) * .858) / 683 * 100


def ek(x, y):
    """% del mapa de los Reinos del Este (-3) -> % del mapa del mundo (-1)."""
    return (700 + (x / 100 * 1024 - 400) * .785) / 1024 * 100, (285 + (y / 100 * 683 - 290) * .786) / 683 * 100


V, ORO, ROJO = M.VERDE, M.ORO_T, M.ROJO
CAMARA = {}
FUNDIDO = {
    "scene-036": 0,                                # corte seco del creativo («LINK IN THE DESCRIPTION») al agradecimiento
}
FX = [
    # =========================================================== gancho
    peg("abre World of Warcraft Forever", "forever", "World of Warcraft Forever", dur=4.4, x=.80, y=.32, tam=420),
    peg("el nivel sesenta es para siempre", "nivel60", "Nivel 60 para siempre", dur=3.8, x=.80, y=.62, tam=320),
    com("Hace unos días Fede nos escribió", "Ugzrce5hGWyNVUff4e94AaABAg", dur=7.0, x=.30, y=.32),
    # =========================================================== 10 el código de invitación
    peg("Los paquetes de Forever traen códigos", "carta", "Invita a un amigo", dur=4.4),
    dict(tipo="mg", fn=M.calendario("LA PRIMERA SEMANA DE FOREVER", 1, 0, 11,
                                    [(3, 3, "Abre Forever", ORO), (3, 10, "Tu amigo juega gratis", V)], hoy=0),
         de=("Con ese código, tu amigo juega", -.2), a=("o salir corriendo de Los Baldíos|fin", .6),
         marcas=["Con ese código", "del cuatro al once"], y=.70, sale=.4, nombre="MG calendario amigo", ver=1.0),
    peg("si lo suyo es la Alianza", "alianza", "Alianza", dur=3.2, x=.13, y=.24, tam=280),
    peg("la Horda o salir corriendo", "horda", "Horda", dur=2.8, x=.30, y=.24, tam=280),
    peg("salir corriendo de Los Baldíos", "kodo", "Los Baldíos", dur=2.6, x=.47, y=.24, tam=300),
    peg("pagar la suscripción", "oro", "Suscripción", dur=3.4, x=.80, y=.40, tam=300),
    # =========================================================== 9 la hora y la cola
    dict(tipo="mg", fn=M.relojes("ABRE FOREVER · MIÉ 4 DE NOVIEMBRE", [("Ciudad de México", 17, 0, ""), ("Bogotá y Lima", 18, 0, ""),
                                                                        ("Buenos Aires y Santiago", 20, 0, ""), ("España", 0, 0, "jue 5")]),
         de=("Eso son las cinco de la tarde", -.3), a=("no se equivocaron|fin", .6),
         marcas=["las cinco de la tarde", "las seis en Bogotá", "las ocho en Buenos Aires", "la medianoche del jueves"],
         y=.66, sale=.4, nombre="MG relojes", ver=1.0),
    dict(tipo="mg", fn=M.capas("LAS CAPAS SE QUEDAN", "classicon_warrior", "ability_hunter_pet_boar", "CAMBIO DE CAPA"),
         de=("Y las capas se quedan", -.2), a=("no fue magia|fin", .6),
         marcas=["Y las capas se quedan", "al cruzar de una zona", "si el jabalí que perseguías", "no fue magia"],
         y=.66, sale=.4, nombre="MG capas", ver=1.0),
    peg("en el barco o el zepelín", "zeppelin", "Zepelín", dur=3.8, x=.84, y=.22, tam=340),
    peg("los talentos rehechos", "talentos", "Talentos rehechos", dur=3.6),
    # =========================================================== 8 la Bolsa de dormir acogedora
    gran("Consigue la Bolsa de dormir acogedora", "bolsa_dormir", "Bolsa de dormir acogedora", dur=4.6, x=.25, tam=420),
    dict(tipo="mg", fn=M.contadores("BOLSA DE DORMIR ACOGEDORA", [
        ("inv_misc_bag_10", "% de experiencia por minuto", 1, 0, 1),
        ("spell_holy_borrowedtime", "% máximo", 3, 1, 2),
    ], remate=("SE SUMA A TODO", 3)), de=("Duermes en ella y ganas", -.2), a=("y al campamento|fin", .8),
        marcas=["Duermes en ella", "por cada minuto", "hasta un tres por ciento", "se suma a la comida"],
        y=.70, sale=.4, nombre="MG bolsa", ver=1.0),
    peg("una nota clavada en una tabla", "carta", "La nota clavada", dur=4.0, x=.17, y=.62, tam=360),
    mapa("reinos_este_eses", [(42.5, 74, "Granja de Alexston", "Páramos de Poniente", F("bolsa_dormir")),
                              (53.5, 50, "Presa de Loch Modan", "salto a la cornisa"),
                              (51.5, 37.5, "Muralla de Thoradin", "subido a una carreta")],
         ("Son seis misiones repartidas", -.3), ("al sur de Los Baldíos|fin", .4),
         ["Son seis misiones", "la presa de Loch Modan", "Muralla de Thoradin"],
         "LA BOLSA DE DORMIR", "así era la ruta en la beta (Alianza)", zmax=1.8),
    peg("guardias de nivel treinta", "montanero", "Guardia de Loch Modan", dur=4.0, x=.80, y=.55, tam=420),
    # =========================================================== Overgear (abre la campaña de noviembre): kit «WoW - Forever (nov)»
    mapa("azeroth_eses", [(*kal(55, 30), "Barrow Deeps", "10 jugadores · 8 jefes", F("illidan")),
                          (*kal(58.5, 35), "Hyjal Summit", "20 jugadores · 13 jefes", F("nordrassil")),
                          (*kal(55.5, 65), "Guarida de Onyxia", "40 jugadores", F("onyxia"))],
         ("Y hablando de llegar a tiempo", -.3), ("hay apenas cinco semanas|fin", .2),
         ["abren Barrow Deeps", "Hyjal Summit y la", "la Guarida de Onyxia"], "9 DE DICIEMBRE", "abren las bandas", zmax=1.7),
    # fondo oficial de marca (Alice, 29-oct: «necesitamos usar otro fondo», Drive «Background/Background.mp4»): cuadro entero
    # DEBAJO de logo, tarjetas, reseñas, packshot y código (va primero en la lista)
    dict(tipo="video", ruta=OG + "background\\Background.mp4", bucle=True, de="los vicios de las primeras", a="scene-036",
         entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "logo-light-bg-small_wow-forever.mp4", croma=True, bucle=True,
         de="Para eso está Overgear", a="El enlace está en la descripción", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25,
         nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Talentos, rotación, addons",
         dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="los vicios de las primeras",
         dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción",
         a=CODIGO, entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a="scene-036", entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== gracias: dos comentarios juntos
    com("gracias por comentarios como estos", "Ugxshe7McCDS3x6Zezd4AaABAg", dur=9.0, x=.30, y=.30, tam=700),
    com("gracias por comentarios como estos", "Ugz84d60LthINJhfjvt4AaABAg", dur=8.6, x=.66, y=.62, tam=700),
    # =========================================================== 7 los libros
    peg("juntar los libros de la biblioteca", "libro", "Libro de la biblioteca", dur=4.2),
    peg("solo los magos los entregaban", "mago", "Mago", dur=3.4, x=.13, y=.24, tam=280),
    peg("cualquier clase puede hacerlo", "guerrero", "Guerrero", dur=2.8, x=.30, y=.24, tam=280),
    peg("clase puede hacerlo", "picaro", "Pícaro", dur=2.5, x=.47, y=.24, tam=280),
    dict(tipo="mg", fn=M.contadores("LIBROS DE LA BIBLIOTECA", [
        ("inv_misc_book_09", "Libros únicos", 40, 0, 1),
        ("inv_jewelry_necklace_07", "Entregas para el collar", 10, 1, 2),
        ("inv_jewelry_ring_05", "Entregas para el anillo", 20, 2, 3),
    ], remate=("Y A LOS 25: PREMIOS MEJORES", 3)), de=("Hay cuarenta libros únicos", -.2), a=("así que cada libro cuenta|fin", .6),
        marcas=["Hay cuarenta", "a los diez, un collar", "a los veinte, un anillo", "Y a los veinticinco"],
        y=.66, sale=.4, nombre="MG libros", ver=1.0),
    mapa("reinos_este_eses", [(44.5, 73, "Catacumbas del Bosque del Ocaso", "muertos vivientes de nivel 28", F("esqueleto"))],
         ("uno está en las catacumbas", -.3), ("de nivel veintiocho|fin", .6),
         ["en las catacumbas"], "UN LIBRO ESCONDIDO", "si se repiten los sitios de la Temporada", zmax=2.0),
    peg("tu mascota demoníaca", "diablillo", "Mascota demoníaca", dur=4.2, x=.80, y=.55, tam=420),
    mapa("reinos_este_eses", [(45.5, 67, "Ventormenta", "Sanctum del Mago"), (47, 29.5, "Entrañas", "Barrio Mágico", F("renegado"))],
         ("se entregaban en Ventormenta", -.3), ("en el Barrio Mágico|fin", .8),
         ["se entregaban en Ventormenta", "y en Entrañas"], "DÓNDE SE ENTREGAN", "en la Temporada de Descubrimiento", zmax=1.6),
    # =========================================================== 6 la cocina
    peg("la comida cocinada da un cinco", "comida", "Comida cocinada", dur=4.4),
    com("ve estos videos mientras come", "Ugx_QZoXnOOuoP3NfF54AaABAg", dur=6.0, x=.32, y=.30, tam=720),
    peg("no vendas la carne de jabalí", "jabali", "Carne de jabalí", dur=3.6, x=.80, tam=380),
    peg("encender una hoguera básica", "hoguera", "Hoguera básica", dur=4.4),
    dict(tipo="mg", fn=M.experiencia("LA SUBIDA MÁS RÁPIDA", [("inv_misc_food_15", "Comida +5 %"), ("spell_fire_fire", "Hoguera"),
                                                              ("inv_misc_bag_10", "Bolsa +3 %")], remate=("TE ADELANTAS", 3)),
         de=("Comida, hoguera y bolsa de dormir juntas", -.4), a=("corra sin parar|fin", 1.4),
         marcas=["Comida, hoguera", "hoguera y bolsa", "bolsa de dormir juntas", "una subida más rápida"],
         y=.66, sale=.4, nombre="MG experiencia", ver=1.0),
    # =========================================================== 5 recolección, montura y vuelos
    peg("Minería, herboristería y desuello", "pico", "Minería", dur=3.6, x=.13, tam=300),
    peg("herboristería y desuello", "hierba", "Herboristería", dur=3.2, x=.30, tam=300),
    peg("y desuello desde el primer día", "cuchillo", "Desuello", dur=2.8, x=.47, tam=300),
    gran("Si eres tauren, tienes ventaja", "tauren", "Tauren", dur=4.6, x=.75),
    peg("el carroñero más rico de Durotar", "orco", "Durotar", dur=3.8, x=.80, y=.55, tam=420),
    peg("no hay Ficha de WoW", "ficha", "Ficha de WoW: no hay", dur=4.0, x=.80, y=.40, tam=320),
    peg("La meta es la montura", "montura", "La primera montura", dur=4.4),
    dict(tipo="mg", fn=M.contadores("LA PRIMERA MONTURA (EN LA BETA)", [
        ("ability_mount_ridinghorse", "Oro a nivel 40", 100, 0, 1),
    ], remate=("PALADÍN Y BRUJO: GRATIS", 2)), de=("En la beta costaba unos cien", -.2), a=("gratis con una misión|fin", .8),
        marcas=["costaba unos cien", "a nivel cuarenta", "el paladín y el brujo"], y=.70, sale=.4, nombre="MG montura 40", ver=1.0),
    peg("el paladín y el brujo", "paladin", "Paladín", dur=3.4, x=.13, y=.24, tam=280),
    peg("y el brujo la conseguían", "brujo", "Brujo", dur=3.0, x=.30, y=.24, tam=280),
    peg("activa cada maestro de vuelo", "grifo", "Maestro de vuelo", dur=4.0),
    mapa("azeroth_eses", [(*ek(45.5, 67), "Ventormenta", "puerto"), (*kal(43.5, 27), "Auberdine", "sin pasar por Menethil")],
         ("Y hay barcos nuevos", -.3), ("sin tener que pasar por Menethil|fin", .8),
         ["como el de Ventormenta", "a Auberdine"], "BARCO NUEVO", "Ventormenta → Auberdine", zmax=1.5),
    dict(tipo="mg", fn=M.contadores("LA MONTURA DE NIVEL 60 (EN LA BETA)", [
        ("ability_mount_ridinghorse", "Oro por la equitación épica", 1000, 0, 1),
        ("inv_misc_coin_01", "Oro por la montura", 200, 1, 2),
    ], remate=("−10 % CON HONORABLE", 3)), de=("Y guarda lo que te sobre", -.2), a=("diez por ciento más barata|fin", 1.2),
        marcas=["costaba mil de oro", "más doscientos", "Y un truco", "un diez por ciento"], y=.66, sale=.4, nombre="MG montura 60", ver=1.0),
    # =========================================================== 4 mazmorras nuevas
    mapa("azeroth_eses", [(*ek(46.5, 53), "Hall of Thanes", "bajo el trono de Forjaz · 13-18", F("magni")),
                          (*ek(47.5, 29.5), "Ruins of Lordaeron", "bajo Entrañas · 15-22", F("renegado")),
                          (*kal(46, 80), "Shaper's Terrace", "cráter de Un'Goro · 58-60", F("devilsaur"))],
         ("Para la Alianza es Hall of Thanes", -.3), ("en el cráter de Un'Goro|fin", .6),
         ["Para la Alianza es Hall", "La Horda tiene Ruins", "como Shaper's Terrace"],
         "MAZMORRAS NUEVAS", "dónde están", zmax=1.6),
    dict(tipo="mg", fn=M.botin("EL BOTÍN DE LAS MAZMORRAS NUEVAS", "achievement_boss_onyxia", "inv_chest_plate04",
                               ["classicon_warrior", "classicon_priest", "classicon_mage", "classicon_rogue", "classicon_hunter"],
                               "LA APARIENCIA, PARA TODOS"),
         de=("Y el cambio importante", -.2), a=("el que gana la tirada|fin", .8),
         marcas=["Y el cambio importante", "ahora sueltan azules", "se la quedan todos", "no solo el que gana"],
         y=.64, sale=.4, nombre="MG botin", ver=1.0),
    mapa("azeroth_eses", [(*ek(49, 62), "Cumbre de Roca Negra", "la cadena termina aquí", F("drakkisath")),
                          (*kal(55.5, 65), "Guarida de Onyxia", "Marjal Revolcafango", F("onyxia"))],
         ("Onyxia vuelve a pedir sintonización", -.3), ("empieza esa cadena|fin", 1.0),
         ["vuelve a pedir sintonización", "en cuanto seas sesenta"], "LA SINTONIZACIÓN DE ONYXIA", "personal, no de cuenta",
         objeto="inv_jewelry_talisman_11", zmax=1.6),
    # =========================================================== 3 Legacy
    dict(tipo="mg", fn=M.contadores("LEGACY", [
        ("achievement_level_60", "Puntos de cuenta al lanzar", 65, 0, 1),
        ("inv_misc_book_11", "Puntos por personaje", 16, 1, 2),
    ]), de=("Legacy sustituye a los logros", -.2), a=("gastar dieciséis|fin", 1.0),
        marcas=["Legacy sustituye", "hay sesenta y cinco", "gastar dieciséis"], y=.66, sale=.4, nombre="MG legacy", ver=1.0),
    peg("llevando cada clase", "guerrero", "Guerrero", dur=3.6, x=.13, tam=280),
    peg("cada clase a ciertos niveles", "mago", "Mago", dur=3.2, x=.30, tam=280),
    peg("a ciertos niveles", "sacerdote", "Sacerdote", dur=2.8, x=.47, tam=280),
    peg("menos en Hardcore", "calavera", "Hardcore", dur=3.0, x=.80, y=.40, tam=280),
    peg("vuelos a mitad de precio", "grifo", "Vuelos a mitad de precio", dur=3.2, x=.13, tam=300),
    peg("talentos desde el nivel nueve", "talentos", "Talentos desde el 9", dur=3.0, x=.30, tam=300),
    peg("el tabernero Wiley", "wiley", "Tabernero Wiley · Trinquete", dur=4.0, x=.80, y=.40, tam=380),
    peg("un tabardo a los cuarenta", "tabardo", "Tabardo · 40 puntos", dur=3.4, x=.13, tam=300),
    # =========================================================== 2 el tipo de servidor
    dict(tipo="mg", fn=M.reglas("ELIGE TU TIPO DE SERVIDOR", [("inv_misc_book_09", "Normal"), ("ability_dualwield", "JcJ"),
                                                              ("spell_holy_mindvision", "Rol"), ("inv_misc_book_11", "Rol + JcJ")], 1,
                                "SIN VUELTA ATRÁS", faccion=("inv_bannerpvp_02", "inv_bannerpvp_01", "Una facción por cuenta")),
         de=("Normal, jugador contra jugador, rol", -.3), a=("un espía de la otra facción|fin", .6),
         marcas=["Normal, jugador", "contra jugador, rol", "rol, y rol", "y rol con jugador", "Y no hay transferencias",
                 "una sola facción por cuenta"],
         y=.62, sale=.4, nombre="MG reglas", ver=1.0),
    peg("un espía de la otra facción", "picaro", "Un espía", dur=3.0, x=.86, y=.20, tam=260),
    peg("es morir en Hardcore", "calavera", "Hardcore", dur=3.4),
    # =========================================================== 1 el nombre y el apellido
    dict(tipo="mg", fn=M.nombre("NOMBRE Y APELLIDO", [("Ana", "Forever", True, "ejemplo oficial")]),
         de=("En Forever los nombres tienen dos partes", -.2), a=("es Ana Forever|fin", 2.2), marcas=["es Ana Forever"],
         y=.70, sale=.4, nombre="MG nombre ana", ver=1.0),
    dict(tipo="mg", fn=M.calendario("RESERVA DE NOMBRES", 1, 0, 4, [(2, 2, "Último día de reserva", ROJO), (3, 3, "Abre Forever", ORO)],
                                    hoy=0, ancho=900),
         de=("puedes reservar hasta tres personajes", -.2), a=("gana el que llega primero|fin", .8),
         marcas=["hasta el tres de noviembre", "Después de eso"], y=.66, sale=.4, nombre="MG calendario reserva", ver=1.0),
    dict(tipo="mg", fn=M.nombre("¿ENTRA O NO ENTRA?", [("Lucía", "Ramírez", True, "acentos, sí"),
                                                      ("Leeegolas", "Elfo", False, "3 letras iguales"),
                                                      ("Matajabalíes", "Supremo", False, "en rol: nombre real")]),
         de=("Así que un Ramírez entra perfecto", -.2), a=("olvídate de Matajabalíes Supremo|fin", 1.4),
         marcas=["un Ramírez", "nada de alargar", "olvídate de Matajabalíes"], y=.62, sale=.4, nombre="MG nombre reglas", ver=1.0),
    peg("olvídate de Matajabalíes", "jabali", "Matajabalíes", dur=3.0, x=.84, y=.20, tam=280),
    # =========================================================== anuncio: comentarios de Darrowshire y la mudanza
    com("Muchos de ustedes nos escribieron", "Ugwdll-Fdj3IOyjODBZ4AaABAg", dur=11.6, x=.28, y=.22, tam=600),
    com("la de la niña que sigue esperando", "UgwC3XfcdZFWxBPJxU94AaABAg", dur=8.8, x=.72, y=.30, tam=600),
    com("Nos dijeron que les encantó", "UgwiIw52now2l8bTFmh4AaABAg", dur=6.0, x=.30, y=.62, tam=600),
    com("que querían más historias así", "Ugyc-5Uogg1E8B-QZ3l4AaABAg", dur=4.4, x=.72, y=.70, tam=600),
    com("y hasta nos pidieron", "UgwlKepNiD-WFyrtAZV4AaABAg", dur=2.8, x=.50, y=.46, tam=600),
    com("el siguiente capítulo", "Ugyz_Et1c5gL3OBTXv94AaABAg", dur=1.8, x=.70, y=.52, tam=600),
    dict(tipo="mg", fn=M.mudanza("UNA NOTICIA PARA EL CANAL", "CRÓNICAS DE WARCRAFT", F("pamela"), "Historias contadas",
                                 ["Listas", "Curiosidades", "Todo lo de Forever"]),
         de=("Por eso tomamos una decisión", -.2), a=("todo lo que traiga Forever|fin", 1.0),
         marcas=["Por eso tomamos", "se va a mudar a otro canal", "muy pronto les daremos", "seguimos con las listas"],
         y=.56, sale=.4, nombre="MG mudanza", ver=1.0),
    # =========================================================== cierre
    com("como estos que nos dejaron hace poco", "Ugz1ecuuJ-62P9Px22J4AaABAg", dur=8.0, x=.30, y=.28, tam=700),
    com("como estos que nos dejaron hace poco", "UgwwB2ynE6YPAR57UKZ4AaABAg", dur=7.6, x=.68, y=.62, tam=700),
    gran("y el miércoles nos vemos en Azeroth", "forever", "Miércoles 4 de noviembre", dur=4.0, x=.50, tam=440),
]
ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="+5 % EXP", en="un cinco por ciento más de experiencia", dur=2.4, tam=150, color="amarillo", y=.2),
    dict(texto="NO VUELVE A CAER", en="si borras un libro", dur=2.6, tam=130, color="rojo", y=.2),
    dict(texto="SIN VUELTA ATRÁS", en="Elige bien el tipo de servidor", dur=2.6, tam=130, color="rojo", y=.2),
    dict(texto="ANTES DEL MARTES", en="Reserva tu nombre y tu apellido", dur=2.6, tam=130, color="amarillo", y=.2),
]
SFX = {}
PISTAS = []

# APOYOS: tarjetas SOLO con datos del guion (fuentes en videos/_investigacion_wow_primera_semana.md)
GRIS = "gris"
APOYOS = []   # 28-oct: las tarjetas de datos se cambiaron por MG (relojes, bolsa, libros, monturas, botín, Legacy)
