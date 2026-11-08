# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 ADD-ONS que necesitas en WoW Forever (y uno que hicimos nosotros)» (SECUENCIA YT, Crónicas de
Warcraft, 7-nov-2026). Modelo: efectos_ref.py (wow_errores_forever).
- Cada add-on: reliquia con su LOGO REAL de CurseForge (a_*) al decir «Número N» + su CAPTURA OFICIAL a cuadro entero (s_*)
  cuando la voz describe lo que hace (promesa visual) + tarjetas solo con datos del guion.
- MG NUEVOS (mg_wow, 7-nov): buscador de los 70 clones, descargas en escala logarítmica, «hecho en casa», meta del doblaje,
  enlaces (PayPal + CurseForge). Mapas: Elwynn (Villanorte → Villadorada, lo que ya está doblado) y bibliotecas de las capitales.
- Los add-ons propios (casa*) van sobre las GRABACIONES de OBS del usuario (_obs.py), con su audio donde la voz calla.
- Comentarios reales (≤ 10 días, no usados): zatherion1 (casa), pirlo2106, AlexAnder, 666nibelheim, quemaloscalor (gracias1),
  santislpslp1595 (gracias2), FenrirMorningstar (burla1).
  python fab.py wow_addons_forever fx --seco | fx hoja | fx
"""
import os
import re
import sys

import mg_tes as T
import mg_wow as M
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", 0.9)
TEMA_PEG = "wow"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=340, dur=4.6):
    xs = (.14, .32, .50, .68, .86)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


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


def _f(fotos):
    return [(F(s), n) for s, n in fotos]


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def podi(tres, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.podio(_f(tres), titulo, TEMA_PEG), de, a, marcas, "podio")


def ek(x, y):
    """% del mapa de los Reinos del Este -> % del mapa del mundo (azeroth_eses)."""
    return (700 + (x / 100 * 1024 - 400) * .785) / 1024 * 100, (285 + (y / 100 * 683 - 290) * .786) / 683 * 100


def P(xy, rot, sub=None, foto=None):
    return (xy[0], xy[1], rot, sub, F(foto) if foto else None)


V, GR, RJ = "verde", "gris", "#ff3b3b"

# ---------------------------------------------------------------- placas de quién narra (de guion.NARRA)
sys.path.insert(0, _D)
import guion as G  # noqa: E402

ORDEN = ["Remy", "el Humano tras el Telón"]
ICO_VOZ = {"Remy": "inv_misc_head_human_01", "el Humano tras el Telón": "inv_misc_head_human_02"}


def _ancla(frase, vistas):
    t = re.sub(r"\[[^\]]+\]", "", frase).strip()
    a = " ".join(t.split()[:5]).rstrip(".,:;")
    vistas[a] = vistas.get(a, 0) + 1
    return a if vistas[a] == 1 else f"{a}#{vistas[a]}"


def placas():
    out, prev, vistas = [], None, {}
    for e in G.ESCENAS:
        for i, f in enumerate(e["frases"]):
            v = G.NARRA[f"{e['id']}_{i}"]
            a = _ancla(f, vistas)
            if v != prev:
                nom = "El Humano" if v.startswith("el Humano") else v
                out.append(dict(tipo="mg", fn=M.narrador(nom, G.LEMAS[v], None, None, ICO_VOZ[v]), en=(a, -.1),
                                dur=3.6, x=.20, y=.86, sale=.3, nombre=f"narra {v} {e['id']}", ver=1.0))
            prev = v
    return out


CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== gancho: MG desde el segundo 1
    mg(M.buscador("forever threat", ["ForeverThreat", "Forever Threat", "ThreatMeterForever", "Forever Threat Meter", "ForeverThreatMeter"],
                  70, "70 PARA HACER LO MISMO"),
       ("Si buscas un medidor", -.3), ("para hacer lo mismo|fin", .8),
       ["Si buscas un medidor", "te salen setenta resultados", "Forever Threat, ForeverThreat", "ForeverThreat, Threat Meter",
        "Threat Meter Forever", "Setenta add-ons", "para hacer lo mismo"], "buscador 70", y=.52),
    pv("llueven add-ons", "i_caja", "Algunos son joyas", dur=3.0, x=.18, y=.62, tam=330),
    pv("mejor ni instalarlos", "i_calavera", "Otros, mejor no", dur=2.8, x=.82, y=.62, tam=300),
    mg(M.descargas("DESCARGAS EN CURSEFORGE", [("inv_misc_questionmark", "El número 1", 215000000),
                                               ("inv_misc_questionmark", "El número 19", 192)], ("UN MILLÓN DE VECES MÁS", 1)),
       ("El número uno lleva", -.3), ("menos de doscientas|fin", .8), ["El número uno lleva", "El diecinueve, menos de"],
       "descargas gancho", y=.55),
    carr([("i_libro", "Leer el lore"), ("i_boca", "Oír a los personajes"), ("i_mapa", "Explorar sin prisa")],
         "una categoría especial", ("uno que hicimos nosotros|fin", .4), ["una categoría especial", "la de inmersión", "uno que hicimos nosotros"],
         titulo="CATEGORÍA ESPECIAL"),
    mg(M.votacion("LA VOTACIÓN DE VOCES TERMINÓ", ["Remy", "Edoardo", "José", "Mario", "Hope", "MariCarmen", "el Profeta", "el Humano"],
                  None, icos=["inv_misc_head_human_01", "spell_shadow_summonvoidwalker", "inv_misc_map_01", "ability_rogue_sprint",
                              "spell_fire_fire", "inv_misc_coin_01", "spell_holy_prayerofhealing", "inv_misc_head_human_02"]),
       ("la votación de voces ya terminó", -.3), ("Gracias a todos los que votaron|fin", .5), ["Ganó la de siempre"], "votación", y=.52),
    # =========================================================== de serie
    pv("Un medidor de daño", "i_espada", "Medidor de daño", dur=3.8, x=.18, y=.62, tam=320),
    pv("un gestor de reutilizaciones", "i_libro_hech", "Gestor de reutilizaciones", dur=3.8, x=.82, y=.62, tam=320),
    # =========================================================== 20 Forever Loot Sparkles
    rel("Número veinte", "a_sparkles", "Forever Loot Sparkles", "número 20"),
    pv("buscas la flor de la misión", "i_herbo", "La flor de la misión", dur=3.6, x=.18, y=.62, tam=340),
    pant("s_sparkles", ("Este add-on le devuelve el brillo", -.2), ("y las vetas de mineral|fin", .3)),
    filav("hace brillar las hierbas", [("i_herbo", "Hierbas", None), ("i_mineria", "Vetas de mineral", "y las vetas de mineral")], y=.66, tam=280, dur=3.4),
    # =========================================================== 19 Favorcraft
    rel("Número diecinueve", "a_favorcraft", "Favorcraft", "el más nuevo"),
    pant("s_favorcraft", ("Eliges las recetas que quieres", -.2), ("comparada con tus bolsas|fin", .3)),
    pant("s_favorcraft2", ("Cubre trescientas nueve recetas", -.2), ("de siete profesiones|fin", .2), zoom=(1.08, 1.0)),
    mg(M.descargas("FAVORCRAFT · CURSEFORGE", [("inv_misc_coin_17", "Recetas que cubre", 309), ("inv_misc_note_01", "Descargas", 192)]),
       ("Cubre trescientas nueve", 1.5), ("descargas. Ciento noventa y dos|fin", .6),
       ["de siete profesiones", "Y tiene ciento noventa"], "favorcraft", y=.55),
    pv("con ChatGPT y con Cursor", "i_nota", "ChatGPT + Cursor", dur=3.4, x=.80, y=.60, tam=320),
    # =========================================================== 18 Books on Map Forever
    rel("Número dieciocho", "a_books", "Books on Map Forever", "para los que leen"),
    mapa("azeroth_eses", [P(ek(43, 72), "Ventormenta", "biblioteca de la capital", "stormwind"),
                          P(ek(44, 20), "Entrañas", "biblioteca de la capital", "undercity")],
         ("los entregas en la biblioteca", -.6), ("en la biblioteca de la capital|fin", .8),
         ["los entregas en la biblioteca", "de la capital"], "LIBROS DE BIBLIOTECA", "se entregan en la capital", zmax=1.3),
    filav("Con diez libros te dan un collar", [("i_collar", "10 libros", None), ("i_anillo", "20 libros", "con veinte un anillo"),
                                               ("i_arco", "25 libros", "y con veinticinco eliges")], y=.66, tam=280, dur=4.6),
    pant("s_books", ("Este add-on pone en el mapa", -.2), ("en cuanto lo recoges|fin", .3)),
    mg(M.contadores("¿CUÁNTOS LIBROS HAY?", [("inv_misc_book_09", "Books on Map Forever", 38, None, 0),
                                             ("inv_misc_book_11", "Otros dos add-ons", 40, 1, 2)], ("NI ELLOS SE PONEN DE ACUERDO", 3)),
       ("dice que hay treinta y ocho", -.4), ("Ni los add-ons se ponen de acuerdo|fin", .6),
       ["dice que hay treinta y ocho", "Otros dos add-ons dicen", "que hay cuarenta", "Ni los add-ons se ponen"], "libros", y=.58),
    # =========================================================== INMERSIÓN
    dict(tipo="mg", fn=PE.banda(F("a_lore"), "ADD-ONS DE INMERSIÓN", "categoría especial", alto=440, tema="wow"), en=("los add-ons de inmersión", -.4),
         dur=4.0, x=.5, y=.78, sale=.3, nombre="banda inmersion", ver=1.0),
    aba([("a_immersion", "17"), ("a_dialogueui", "16"), ("a_narcissus", "15"), ("a_wayfarer", "14"), ("a_lore", "13")],
        "estos cinco son para ti", ("una sorpresa|fin", .6), ["estos cinco", "son para ti", "Y en medio", "una sorpresa", "una sorpresa"], "inmersion"),
    # =========================================================== 17 Forever Immersion
    rel("Número diecisiete", "a_immersion", "Forever Immersion", "la interfaz que desaparece"),
    pant("s_immersion", ("Mientras exploras, desvanece la interfaz", -.2), ("los marcos de los personajes|fin", .3)),
    # =========================================================== 16 Dialogue UI
    rel("Número dieciséis", "a_dialogueui", "Dialogue UI", "misiones de juego de rol"),
    pant("s_dialogueui", ("Cambia la ventana de misiones", -.2), ("al personaje que te habla|fin", .3)),
    # =========================================================== 15 Narcissus (sustituye a Spoken: el usuario, 7-nov)
    rel("Número quince", "a_narcissus", "Narcissus", "tu personaje, como en un RPG"),
    pant("s_narcissus", ("Cambia la ventana de personaje", -.2), ("y el equipo a los lados|fin", .3)),
    # =========================================================== CASA: los add-ons propios (sobre sus grabaciones de OBS)
    mg(M.hecho_en_casa("HECHO EN CASA", [("inv_misc_head_human_02", "Voces", "Misiones con voz en español", "Cada personaje, su voz"),
                                         ("inv_misc_food_15", "Necesidades", "Hambre, sueño, campamento", "Avisa antes de perder el bono")], "GRATIS"),
       ("lo hicimos aquí, en casa", -.6), ("que lo presente él|fin", .3), ["lo hicimos aquí", "en casa", "Como lo hizo él"], "hecho en casa", y=.42),
    com("alguien en los comentarios dijo", "UgzA9p2Z10TE-cp555l4AaABAg", dur=6.0, x=.32, y=.30),
    pv("se llama Remy Dos Veces", "p_remy", "Remy «Dos Veces» · Villadorada", dur=4.6, x=.80, y=.36, tam=380, entrada="sello"),
    pv("también las de los orcos", "p_kaltunk", "Kaltunk · Valle de los Retos", dur=5.0, x=.80, y=.36, tam=380),
    pv("Escucha a Gornek", "p_gornek", "Gornek · Valle de los Retos", dur=4.6, x=.80, y=.36, tam=380),
    mapa("elwynn", [(49, 38, "Villanorte", "abadía · primeras misiones", F("p_willem")), (42, 65, "Villadorada", "la posada", F("p_posada"))],
         ("Ya están las misiones de inicio", -.2), ("en Villanorte y Villadorada|fin", .8), ["misiones de inicio de los humanos", "y Villadorada"],
         "LO QUE YA ESTÁ DOBLADO", "Bosque de Elwynn", zmax=1.5),
    mg(M.enlaces("EN LA DESCRIPCIÓN", [("inv_misc_coin_01", "PayPal · desde 1 dólar", "paypal.me/edsonxn/1USD")], "Nadie tiene que pagar para usarlo"),
       ("Lo único que me frena", .2), ("Nadie tiene que pagar para usarlo|fin", .2),
       ["enlace de PayPal", "Nadie tiene que pagar"], "paypal", y=.40),
    mg(M.enlaces("EN LA DESCRIPCIÓN", [("trade_engineering", "CurseForge · gratis", "Voces Español WoW Forever")]),
       ("Los dos están en CurseForge", -.2), ("también va en la descripción|fin", .6), ["Los dos están en CurseForge"], "curseforge", y=.40),
    mg(M.meta("DOBLAR AZEROTH, ZONA POR ZONA", [("inv_misc_head_human_01", "Villanorte"), ("inv_misc_head_human_02", "Villadorada"),
                                                ("inv_misc_head_orc_01", "Valle de los Retos"), ("achievement_zone_durotar", "Durotar"),
                                                ("inv_misc_map_01", "Renegados"), ("inv_misc_map08", "Todo el juego")], 4,
              "RENEGADOS EN CAMINO · POCO A POCO", ancho=1760),
       ("Ahora estoy empezando por", -.3), ("hasta doblar todo el juego|fin", 1.2),
       ["zonas iniciales de cada raza", "doblar todo el juego", "doblar todo el juego"], "ruta doblaje", y=.42),
    # =========================================================== 14 Wayfarer
    rel("Número catorce", "a_wayfarer", "Wayfarer", "sin mapa y sin flecha"),
    pant("s_wayfarer", ("En vez de mapa, una brújula", -.2), ("en texto, como en dos mil cuatro|fin", .3)),
    pv("una brújula que te da direcciones", "i_brujula", "Brújula con palabras", dur=3.6, x=.80, y=.60, tam=320),
    # =========================================================== 13 Lore Forever
    rel("Número trece", "a_lore", "Lore Forever", "la historia de cada lugar"),
    # =========================================================== gracias 1 (4 agradecimientos + 1 en casa)
    com("Pirlo dice que nos escucha", "UgyUa4dmdJlR95dvYt94AaABAg", dur=7.0, x=.30, y=.30),
    com("Alex dice que esta voz", "UgwtWRTGWGQ9P38e5k14AaABAg", dur=4.0, x=.70, y=.30),
    com("otro nos recordó que lo que importa", "UgwiEdUgNy1K3ulZVwV4AaABAg", dur=4.4, x=.30, y=.66),
    com("Todos los comentarios se leen", "UgzYKTeKJs9SxP86MHF4AaABAg", dur=6.6, x=.66, y=.34),
    # =========================================================== 12 Happy Camper
    rel("Número doce", "a_camper", "Happy Camper", "para los que acampan"),
    pv("El campamento es uno de los sistemas", "i_fogata", "Campamento", dur=3.6, x=.18, y=.62, tam=320),
    pant("s_camper", ("Este add-on comparte en el mapa", -.2), ("los beneficios que te dan|fin", .3)),
    # =========================================================== 11 GatherLite
    rel("Número once", "a_gatherlite", "GatherLite", "para los que recolectan"),
    pant("s_gatherlite", ("Pone en el mapa y en el minimapa", -.2), ("para que no des vueltas a ciegas|fin", .3)),
    pv("las cajas del Favor de comerciante", "i_caja", "Cajas del Favor", dur=3.8, x=.18, y=.62, tam=320),
    filav("si llevas Herboristería y Minería", [("i_herbo", "Herboristería", None), ("i_mineria", "Minería", "y Minería")], y=.66, tam=280, dur=4.4),
    # =========================================================== burla 1
    com("Voz original, por favor", "UgywIfzhyYaah1Cj00t4AaABAg", dur=7.4, x=.32, y=.32),
    # =========================================================== 10 ForeverThreat
    rel("Número diez", "a_threat", "ForeverThreat", "uno de setenta"),
    pv("detecta quién tanquea", "i_escudo_tanque", "Quién tanquea", dur=3.6, x=.18, y=.62, tam=320),
    # =========================================================== 9 DialogKey
    rel("Número nueve", "a_dialogkey", "DialogKey", "el más pequeño"),
    # =========================================================== Overgear campaña 2: kit «WoW - Forever (nov)» + fondo de marca SIEMPRE
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="tú eliges, y pagas", a=("Y aquí empieza la categoría especial", -.1), entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Talentos, rotación", dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="tú eliges, y pagas", dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción", a=CODIGO,
         entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=("Y aquí empieza la categoría especial", -.1), entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== 8 What's Training
    rel("Número ocho", "a_training", "What's Training", "menos viajes al instructor"),
    pant("s_training", ("Añade una pestaña al libro de hechizos", -.2), ("y cuánto cuesta|fin", .3)),
    pv("Aprende, y arrastra", "i_libro_hech", "Aprende, y arrastra", dur=3.0, x=.80, y=.60, tam=320),
    # =========================================================== 7 AtlasLoot
    rel("Número siete", "i_calavera", "AtlasLoot", "el botín de cada jefe"),
    filav("el mejor equipo por clase", [("i_espada", "Equipo por clase", None), ("i_libro", "Profesiones", "profesiones, reputaciones"),
                                        ("i_escudo", "JcJ", "y JcJ")], y=.66, tam=260, dur=4.0),
    pv("un diario de mazmorras con misiones", "a_dfl_journal", "DFL Dungeon Journal · uno de 34", dur=4.4, x=.76, y=.56, tam=420),
    # =========================================================== gracias 2
    com("Solo he jugado una tarde", "UgwsZNkElnCQFciCxZR4AaABAg", dur=6.6, x=.32, y=.32),
    # =========================================================== 6 Baganator
    rel("Número seis", "a_baganator", "Baganator", "tus bolsas en orden"),
    pant("s_baganator", ("Ordena tus bolsas por categorías", -.2), ("sin tener que cambiar de personaje|fin", .3)),
    pv("Forever ya trae la opción de combinar", "i_bolsa", "Combinar bolsas de serie", dur=3.8, x=.18, y=.62, tam=320),
    # =========================================================== 5 OpenMap
    rel("Número cinco", "a_openmap", "OpenMap", "el mapa que Forever no trae"),
    pant("s_openmap", ("Cose todos los mapas de zona", -.2), ("los barcos y los zepelines|fin", .3)),
    mg(M.descargas("OPENMAP · DESCARGAS", [("inv_misc_map_01", "A los pocos días", 160000), ("inv_misc_map08", "Hoy", 700000)]),
       ("Salió el once de octubre", -.2), ("casi setecientas mil|fin", .8), ["pasó las ciento sesenta mil", "va por casi setecientas mil"],
       "openmap", y=.56),
    # =========================================================== 4 Auctionator
    rel("Número cuatro. Auctionator", "a_auctionator", "Auctionator", "subastas sin sufrir"),
    pant("s_auctionator", ("Listas de compra, búsqueda por recetas", -.2), ("más que la subasta|fin", .3)),
    pv("hasta los mil doscientos de oro", "i_montura", "Montura épica · 1 200 de oro", dur=4.0, x=.80, y=.60, tam=340),
    # =========================================================== 3 OneForAll
    rel("Número tres. OneForAll", "a_oneforall", "OneForAll", "el todo en uno"),
    pant("s_oneforall", ("Es un compañero todo en uno", -.2), ("en un solo add-on|fin", .3)),
    filav("un libro de biblioteca cerca", [("i_libro", "Libro cerca", None)], y=.64, tam=300, dur=3.4),
    mg(M.descargas("ONEFORALL · DESCARGAS", [("inv_misc_note_01", "3 de noviembre", 94000), ("inv_misc_coin_17", "Hoy", 590000)],
                   ("× 6 EN CUATRO DÍAS", 2)),
       ("El tres de noviembre tenía", -.3), ("Se multiplicó por seis en cuatro días|fin", .8),
       ["El tres de noviembre tenía", "Hoy pasa de quinientas", "Se multiplicó por seis"], "oneforall", y=.56),
    # =========================================================== 2 Leatrix Plus
    rel("Número dos", "a_leatrix", "Leatrix Plus", "80 comodidades"),
    pant("s_leatrix", ("Unas ochenta opciones de comodidad", -.2), ("invitaciones de desconocidos, y mucho más|fin", .3)),
    filav("marca vender basura y reparar", [("i_oro", "Vender basura", None), ("i_espada", "Reparar", "y reparar")], y=.66, tam=280, dur=3.6),
    # =========================================================== 1 Questie
    rel("Número uno. Questie", "a_questie", "Questie", "el de siempre"),
    pant("s_questie", ("Te enseña quién da cada misión", -.2), ("de toda su base de datos|fin", .3)),
    pant("s_questie2", ("apaga su rastreador de la derecha", -.4), ("bastante feo|fin", .4), zoom=(1.12, 1.0)),
    podi([("a_questie", "Questie · 215 M"), ("a_auctionator", "Auctionator · 205 M"), ("a_leatrix", "Leatrix Plus · 76 M")],
         ("Más de doscientos quince millones", -.2), ("y el número uno|fin", .8),
         ["Más de doscientos quince", "El add-on más descargado", "y el número uno"], titulo="LOS MÁS DESCARGADOS"),
    # =========================================================== cierre
    aba([("a_sparkles", "20"), ("a_narcissus", "15"), ("a_threat", "10"), ("a_openmap", "5"), ("a_questie", "1")],
        "Y esos son los veinte add-ons", ("el mapa de misiones de siempre|fin", .6),
        ["Y esos son los veinte", "de un brillo en el pasto", "hasta el mapa", "el mapa de misiones", "de siempre"], "cierre"),
    mg(M.enlaces("EN LA DESCRIPCIÓN", [("inv_misc_coin_01", "PayPal", "Para doblar más misiones"),
                                       ("trade_engineering", "CurseForge", "Voces y Necesidades")]),
       ("Y si quieres que sigamos doblando", -.2), ("en el enlace de la descripción|fin", .6),
       ["sigamos doblando", "apoya con lo que quieras"], "cierre enlaces", y=.42),
] + placas()
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="20 ADD-ONS", en="los veinte add-ons que de verdad", dur=2.6, tam=140, color="amarillo", y=.2),
    dict(texto="/cdm", en="barra c d m", dur=2.2, tam=150, color="amarillo", y=.2),
    dict(texto="VIENEN APAGADOS", en="Los dos vienen apagados", dur=2.4, tam=130, color="rojo", y=.2),
    dict(texto="600 MIL", en="más de seiscientas mil descargas", dur=2.2, tam=150, color="amarillo", y=.2),
    dict(texto="192", en="descargas. Ciento noventa y dos", dur=2.0, tam=170, color="rojo", y=.2),
    dict(texto="~200 → ~10 000", en="a unos diez mil", dur=2.6, tam=120, color="amarillo", y=.2),
    dict(texto="8,5 MILLONES", en="más de ocho millones y medio", dur=2.4, tam=130, color="amarillo", y=.2),
    dict(texto="F1", en="pulsa F uno al empezar", dur=2.0, tam=170, color="amarillo", y=.2),
    dict(texto="REMY «DOS VECES»", en="se llama Remy Dos Veces", dur=2.6, tam=110, color="amarillo", y=.16),
    dict(texto="¿SIGO? DÍMELO", en="dime en los comentarios si quieres", dur=3.4, tam=130, color="amarillo", y=.2),
    dict(texto="13 MILLONES", en="trece millones de descargas", dur=2.2, tam=140, color="amarillo", y=.2),
    dict(texto="26 000 PUNTOS", en="más de veintiséis mil puntos", dur=2.4, tam=120, color="amarillo", y=.2),
    dict(texto="RITO DE PASO", en="es un rito de paso", dur=2.2, tam=140, color="rojo", y=.2),
    dict(texto="MISIÓN N.º 300", en="tu misión número trescientos", dur=2.4, tam=120, color="amarillo", y=.2),
    dict(texto="NUMY EDITION", en="es la Numy Edition", dur=2.4, tam=130, color="amarillo", y=.2),
    dict(texto="11 MILLONES", en="casi once millones de descargas", dur=2.2, tam=140, color="amarillo", y=.2),
    dict(texto="41 MILLONES", en="más de cuarenta y un millones", dur=2.2, tam=140, color="amarillo", y=.2),
    dict(texto="205 MILLONES", en="doscientos cinco millones", dur=2.2, tam=140, color="amarillo", y=.2),
    dict(texto="SALUD MENTAL", en="es salud mental", dur=2.2, tam=140, color="amarillo", y=.2),
    dict(texto="76 MILLONES", en="setenta y seis millones", dur=2.2, tam=140, color="amarillo", y=.2),
]
SFX = {}
# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/wow/, copiado a sfx/), solo en momentos clave
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número veinte.", "Número quince", "Número diez", "Número cinco")]
PISTAS += [dict(sfx="mision_completada", en=e, vol=.22) for e in ("Así que hice WoW Forever Voces", "Y esos son los veinte add-ons")]
PISTAS += [dict(sfx="subasta", en=e, vol=.26) for e in ("Número cuatro. Auctionator",)]
# SI LA VOZ NOMBRA UN SONIDO, SE OYE (31-oct): en cada post, el PNJ del add-on a nivel de voz (voz=True agacha la música)
PISTAS += [dict(sfx="oye_kaltunk", en=("Valle de los Retos y Durotar|fin", .15), vol=1.0, voz=True),   # OBS 8-nov: Kaltunk (orco), 23,8 s
           dict(sfx="oye_gornek", en=("Escucha a Gornek|fin", .15), vol=1.0, voz=True),   # OBS 8-nov: Gornek (orco), 10,5 s
           dict(sfx="oye_willem", en=("propia voz Escucha|fin", .15), vol=1.0, voz=True),  # OBS g1 4-11 s (Willem)
           dict(sfx="oye_mortero", en=("posada de Villadorada|fin", .15), vol=1.0, voz=True),  # OBS g4 4-9 s
           dict(sfx="oye_lore", en=("sus historias Escucha|fin", .2), vol=1.0, voz=True)]       # TOP 3:21 «Westfall…»
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Así que hoy te traigo", "Número uno. Questie")]

# APOYOS: tarjetas SOLO con datos del guion (fuentes en videos/_investigacion_wow_addons_forever.md)
APOYOS = [
    dict(en="dos cosas que Forever ya trae de serie", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Ya viene en el juego", calidad="verde",
         icono="inv_misc_spyglass_02", lineas=["Medidor de daño · Opciones avanzadas", "Gestor de reutilizaciones · /cdm", dict(t="Vienen apagados", c=RJ)])),
    dict(en="Un aviso: cambia ajustes del juego", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Antes de borrarlo", calidad=RJ,
         icono="inv_misc_note_01", lineas=["Cambia ajustes que se quedan", dict(t="Desmarca sus casillas", c=V)])),
    dict(en="Según 404 Media, Warcraft Logs", dur=5.6, x=.72, size=.50, tarjeta=dict(titulo="404 Media · Warcraft Logs", calidad="amarillo",
         icono="inv_misc_note_02", lineas=["De ~200 programadores a ~10 000", dict(t="~1 000 abusan del sistema", c=RJ)])),
    dict(en="Hasta existe una herramienta, witchcraft", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="witchcraft", calidad="morado",
         icono="trade_engineering", lineas=["Pide add-ons a Claude o Codex", dict(t="Sin salir del juego", c=GR)])),
    dict(en="Y todo vuelve solo cuando entras", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Vuelve sola cuando...", calidad="verde",
         icono="ability_warrior_defensivestance", lineas=["Entras en combate", "Fijas un objetivo", dict(t="Ratón encima o una tecla", c=V)])),
    dict(en="Bigbillygames lo resume así", dur=4.4, x=.72, size=.50, tarjeta=dict(titulo="Bigbillygames", calidad="amarillo",
         icono="inv_misc_note_02", lineas=["«Menos basura de interfaz»", dict(t="mientras paseas", c=GR)])),
    dict(en="Su consejo: pulsa F uno", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Consejo de Bellular", calidad="azul",
         icono="inv_misc_note_01", lineas=["Pulsa F1 al empezar", dict(t="Quita el zoom más agresivo", c=V)])),
    dict(en="Y si lo juntas con Forever Quest Tint", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Forever Quest Tint", calidad="verde",
         icono="inv_misc_note_01", lineas=["Tiñe las misiones nuevas", dict(t="No se te escapa ninguna", c=V)])),
    dict(en="Trae un modo foto que esconde", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Modo foto", calidad="verde",
         icono="inv_misc_spyglass_02", lineas=["Sin interfaz, nombres ni daño", dict(t="Gráficos al máximo", c=V)])),
    dict(en="Un aviso: cambia dos de las vistas", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Antes de instalarlo", calidad=RJ,
         icono="inv_misc_note_01", lineas=["Cambia 2 vistas de cámara", dict(t="Vuelve a guardarlas", c=V)])),
    dict(en="El segundo se llama Necesidades", dur=6.0, x=.72, size=.50, tarjeta=dict(titulo="Necesidades", calidad="naranja",
         icono="inv_misc_food_15", lineas=["Hambre · Sueño", "Campamento · Descanso", dict(t="Avisa antes de perder el bono", c=V)])),
    dict(en="No trae datos cargados", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Wayfarer", calidad="amarillo", icono="inv_misc_book_09",
         lineas=["Solo aprende lo que ves", dict(t="Diario de viaje", c=V)])),
    dict(en="Team Overpowered lo resume así", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Team Overpowered", calidad="amarillo",
         icono="inv_misc_note_02", lineas=["Cientos de horas en Azeroth", dict(t="sin saber por qué importan", c=GR)])),
    dict(en="tiene paquetes de narración en español", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Lore Forever en español", calidad="verde",
         icono="inv_misc_book_11", lineas=["Voz de hombre", dict(t="Voz de mujer", c=V)])),
    dict(en="Campfire Tooltips te explica", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Campfire Tooltips", calidad="verde", icono="spell_fire_fire",
         lineas=["39 objetos de campamento", dict(t="Más sencillo", c=V)])),
    dict(en="Bellular lo dijo mejor", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Bellular", calidad="amarillo", icono="inv_misc_note_02",
         lineas=["Robarle el aggro al tanque", dict(t="y morir: rito de paso", c=RJ)])),
    dict(en="Ojo: Forever usa las reglas", dur=6.0, x=.72, size=.50, tarjeta=dict(titulo="Reglas del WoW moderno", calidad=RJ, icono="inv_misc_note_01",
         lineas=["En combate: enseñar datos, sí", dict(t="Hacer cuentas libres: no", c=RJ), dict(t="WeakAuras: sin versión oficial", c=GR)])),
    dict(en="Pero ojo con cuál bajas", dur=5.6, x=.72, size=.50, tarjeta=dict(titulo="¿Cuál DialogKey?", calidad="amarillo", icono="inv_misc_note_01",
         lineas=[dict(t="Original: parado desde 2019", c=RJ), dict(t="Numy Edition: funciona", c=V)])),
    dict(en="Según Bellular, a niveles bajos", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Consejo de Bellular", calidad="azul",
         icono="inv_misc_book_11", lineas=["Instructor cada dos niveles", dict(t="Llegar sin dinero duele", c=RJ)])),
    dict(en="En Forever no hay buscador de mazmorras", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Sin buscador de mazmorras", calidad=RJ,
         icono="inv_misc_groupneedmore", lineas=["Llega sabiendo qué suelta", dict(t="Con las misiones recogidas", c=V)])),
    dict(en="Pero tiene un límite", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Botín escondido", calidad=RJ, icono="inv_misc_questionmark",
         lineas=["Nadie lo ha visto todavía", dict(t="No sale en el add-on", c=RJ)])),
    dict(en="Dato curioso: es del mismo autor", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="plusmouse", calidad="morado", icono="inv_misc_note_01",
         lineas=["Baganator", dict(t="y Auctionator (n.º 4)", c=V)])),
    dict(en="Su autor lo dice abiertamente", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="OpenMap · About Claude", calidad="verde",
         icono="trade_engineering", lineas=["Claude escribe y revisa código", dict(t="El arte: archivos de Blizzard", c=V)])),
    dict(en="Scottejaye cuenta que no lo conocía", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Scottejaye", calidad="amarillo", icono="inv_misc_note_02",
         lineas=["No lo conocía", dict(t="Ya no vive sin él", c=V)])),
    dict(en="En el foro oficial alguien escribió", dur=6.0, x=.72, size=.50, tarjeta=dict(titulo="Foro oficial", calidad="amarillo", icono="inv_misc_note_02",
         lineas=["«Questie ya no hace falta»", dict(t="Respuesta: «mis FPS…»", c=RJ)])),
]
