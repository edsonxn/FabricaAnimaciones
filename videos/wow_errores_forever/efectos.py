# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 25 ERRORES que estás cometiendo en WoW Forever» (motor SECUENCIA YT, Crónicas de Warcraft, 6-nov-2026).
- COMPETENCIA DE VOCES (el usuario, 5-nov): placa `mg_wow.narrador` (NUEVA) en cada cambio de voz, sacada sola de guion.NARRA, y
  papeleta `mg_wow.votacion` (NUEVA) en el cierre, donde cada voz marca su casilla cuando pide el voto.
- MAPAS REALES con ruta (rutas de barco, naufragio de la bolsa, campamentos, libros) con FOTO en cada parada.
- Overgear campaña 2 (kit «WoW - Forever (nov)», fondo de marca SIEMPRE, logo blanco, creativo CRONICAS10 sin audio).
- Pegatinas variadas (`peg_anim` + `peg_estilos`): íconos REALES del juego e imágenes de Wowpedia; tarjetas SOLO con datos del guion.
- Comentarios reales: 1 en el gancho, 1 en las voces, 5 agradecimientos, 2 críticas con burla, 1 pregunta (n.º 1).
  python fab.py wow_errores_forever fx --seco | fx hoja | fx
"""
import os
import re
import sys

import mg_mapa as MP  # noqa: F401
import mg_tes as T
import mg_wow as M
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", 0.9)   # el rótulo del creativo (2,5 s) entra con la palabra
TEMA_PEG = "wow"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=340, dur=4.6):
    """Fila de pegatinas variadas; items = [(slug, titulo, ancla o None = la misma)]."""
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


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(F(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema="wow"), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.5, zmin=1.0):
    """Mapa real a cuadro entero con la ruta (mg_wow.ruta): un pin por paso en su marca, con la foto de lo que se nombra."""
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.60, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def kal(x, y):
    """% del mapa de Kalimdor -> % del mapa del mundo (calibrado en wow_objetos_raros, 22-oct-2026)."""
    return (128 + (x / 100 * 1022 - 385) * .826) / 1024 * 100, (130 + (y / 100 * 668 - 100) * .858) / 683 * 100


def ek(x, y):
    """% del mapa de los Reinos del Este -> % del mapa del mundo."""
    return (700 + (x / 100 * 1024 - 400) * .785) / 1024 * 100, (285 + (y / 100 * 683 - 290) * .786) / 683 * 100


def P(xy, rot, sub=None, foto=None):
    return (xy[0], xy[1], rot, sub, F(foto) if foto else None)


BLANCO, ROJO, VERDE, GRIS, ORO_T = M.BLANCO, (255, 70, 60), M.VERDE, M.GRIS, M.ORO_T
AMAR = (255, 255, 160)

# ---------------------------------------------------------------- placas de quién narra (de guion.NARRA)
sys.path.insert(0, _D)
import guion as G  # noqa: E402

ORDEN = ["Remy", "Edoardo", "José", "Mario", "Hope", "MariCarmen", "el Profeta", "el Humano tras el Telón"]
ICO_VOZ = {"Remy": "inv_misc_head_human_01", "Edoardo": "spell_shadow_summonvoidwalker", "José": "inv_misc_map_01",
           "Mario": "ability_rogue_sprint", "Hope": "spell_fire_fire", "MariCarmen": "inv_misc_coin_01",
           "el Profeta": "spell_holy_prayerofhealing", "el Humano tras el Telón": "inv_misc_head_human_02"}


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
            if v != prev and e["id"] != "cierre":
                nom = "El Humano" if v.startswith("el Humano") else v
                out.append(dict(tipo="mg", fn=M.narrador(nom, G.LEMAS[v], ORDEN.index(v) + 1, len(ORDEN), ICO_VOZ[v]), en=(a, -.1),
                                dur=3.6, x=.20, y=.86, sale=.3, nombre=f"narra {v} {e['id']}", ver=1.0))
            prev = v
    return out


CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== gancho: MG desde el segundo 1
    mg(M.contadores("WOW FOREVER · LANZAMIENTO", [("inv_misc_note_01", "4 DE NOVIEMBRE", 4, None, 0),
                                                 ("inv_misc_head_human_01", "personajes en la beta", 8862354, 1, 2),
                                                 ("spell_magic_featherfall", "muertos por una caída", 1157204, 2, 3)]),
       ("salió el cuatro de noviembre", -.4), ("murió por una caída|fin", 1.0),
       ["salió el cuatro", "casi nueve millones", "más de un millón", "murió por una caída"], "lanzamiento", y=.52),
    pv("venden al vendedor", "i_caja", "Lo que mañana vale oro", dur=3.4, x=.18, y=.64, tam=340),
    pv("juegan sin las habilidades", "i_libro_hech", "Ya pagadas", dur=3.0, x=.80, y=.64, tam=340),
    com("Como nos escribió un espectador", "Ugz4KKojTCFUjGvizTl4AaABAg", dur=5.6),
    # =========================================================== las voces
    mg(M.votacion("HOY COMPITEN 8 VOCES", ["Remy", "Edoardo", "José", "Mario", "Hope", "MariCarmen", "el Profeta", "el Humano"],
                  "LA QUE ELIJAS SE QUEDA", icos=[ICO_VOZ[v] for v in ORDEN]),
       ("hoy no narro solo", -.3), ("y vota en los comentarios|fin", .5),
       ["hoy no narro solo", "Siete voces de Crónicas", "Edoardo. Me tocan", "José. El veintidós", "Mario. Diecisiete",
        "Soy Hope", "MariCarmen. Nueve", "El Profeta. Los tres", "Aquí estoy: el humano"], "papeleta inicio", y=.52),
    com("Y alguien pidió una voz propia", "UgwFBqCzZBQoja_RlbV4AaABAg", dur=6.0, x=.70, y=.30),
    # =========================================================== 25 Brujo
    rel("Número veinticinco", "voidwalker", "Abisario", "mascota del brujo"),
    mg(M.contadores("VIDA DE LA MASCOTA POR PUNTO DE AGUANTE", [("spell_shadow_summonvoidwalker", "Classic", 75, None, 0),
                                                              ("spell_shadow_summonvoidwalker", "Forever", 20, 0, 1)], ("÷ 3,75", 1)),
       ("bajó de siete coma cinco a dos", -1.2), ("aguanta como una cortina|fin", .6),
       ["bajó de siete coma", "a dos", "aguanta como una cortina"], "mascota", y=.60),
    pv("usa al abisario o al manáfago", "felhunter", "Manáfago", dur=3.8, x=.80, y=.58, tam=380),
    # =========================================================== 24 Fogata
    rel("Número veinticuatro", "i_fogata", "Fogata", "parte del campamento"),
    pv("un trol de la Horda", "trol", "Un trol de la Horda", dur=3.6, x=.18, y=.60, tam=420),
    pv("Los novatos morían", "valle_pruebas", "El punto de aparición", dur=4.0, x=.76, y=.56, tam=440),
    # =========================================================== 23 Piedra de encuentro
    rel("Número veintitrés", "meeting_stone", "Piedra de encuentro", "no invoca", tam=520),
    pv("el Ritual de invocación del brujo", "i_ritual", "Ritual de invocación", dur=3.8, x=.18, y=.60, tam=340),
    filav("necesita a dos ayudantes más", [("i_brujo", "Brujo", None), ("i_guerrero", "Ayudante", None), ("i_sacerdote", "Ayudante", None)], y=.64, tam=280, dur=3.6),
    # =========================================================== 22 Preajuste
    mg(M.reglas("PREAJUSTE AL PRIMER INICIO", [("inv_misc_map_01", "MEJORADO"), ("inv_misc_book_09", "CLÁSICO")], 0, "SI DUDAS: MEJORADO"),
       ("te pide elegir entre dos", -.3), ("si dudas, Mejorado|fin", .6),
       ["Mejorado o Clásico", "Mejorado o Clásico", "Y Blizzard lo dice claro"], "preajuste", y=.58),
    pv("cinco jabalíes en el bosque de Elwynn", "jabali", "Cinco jabalíes", dur=3.6, x=.80, y=.60, tam=420),
    # =========================================================== 21 Addons
    rel("Número veintiuno", "i_ingenieria", "Addons", "¿quién los hizo?"),
    filav("como Questie, Auctionator o Details", [("i_mapa", "Questie", None), ("i_oro", "Auctionator", None), ("i_espada", "Details", None)], y=.66, tam=280, dur=4.0),
    # =========================================================== gracias 1
    com("gracias por comentarios como estos", "Ugwvob8cbrBRpcXrfmN4AaABAg", dur=7.0, y=.28),
    com("a los malos comentarios les hacemos caso", "UgxcJkK3zjulhsFYFfh4AaABAg", dur=5.6, x=.68, y=.66),
    # =========================================================== 20 Fronteras y capas
    mg(M.capas("LA FRONTERA ENTRE DOS ZONAS", "classicon_rogue", "inv_misc_head_orc_01", "DESAPARECE"),
       ("Si cruzas la línea en plena pelea", -.3), ("que venía a ayudarte también|fin", .8),
       ["Si cruzas la línea", "el enemigo que perseguías", "desaparece", "que venía a ayudarte"], "capas", y=.58),
    # =========================================================== 19 Barco sin grupo
    mapa("azeroth_eses", [P(kal(59, 55), "Trinquete", "Kalimdor", "ratchet"), P(ek(43, 92), "Reinos del Este", "a mitad del mar: otra capa", "reinos_este")],
         ("En la beta, un viaje de Kalimdor", -.2), ("cambió de capa a mitad del mar|fin", .5),
         ["En la beta, un viaje", "cambió de capa"], "UN BARCO, DOS CAPAS", "beta de Forever", zmax=1.3),
    pv("formen el grupo antes de embarcar", "zeppelin", "Primero el grupo", dur=3.6, x=.80, y=.60, tam=420),
    # =========================================================== 18 Los Humedales
    mapa("azeroth_eses", [P(ek(43, 72), "Ventormenta", None, "stormwind"), P(ek(50, 50), "Los Humedales", "a pie", "wetlands"),
                          P(ek(45, 46), "Puerto de Menethil", "el barco de antes", "menethil"), P(kal(45, 24), "Auberdine", "Costa Oscura", "auberdine")],
         ("Cualquier veterano de la Alianza", -.2), ("en Costa Oscura|fin", .6),
         ["Cualquier veterano", "cruzar Los Humedales", "Puerto de Menethil", "a Auberdine, en Costa Oscura"], "LA CARRERA DE LA MUERTE",
         "y la ruta nueva de Forever", zmax=1.4),
    filav("Y hay más rutas nuevas", [("menethil", "Menethil · Costasur", None), ("tanaris", "Tanaris → Riverglades", "otra de Tanaris"),
                                      ("darkshore", "Isla Zephras", "y otra a la Isla Zephras")], y=.66, tam=300, dur=4.4),
    pv("Los cocodrilos de Los Humedales", "crocolisco", "No te van a extrañar", dur=3.4, x=.78, y=.60, tam=440),
    # =========================================================== burla 1
    com("aquí va una opinión con mucha pasión", "UgxLp3LU2Jg2iDGNuNB4AaABAg", dur=7.4, y=.30),
    # =========================================================== 17 Monstruos verdes
    mg(M.filas("EXPERIENCIA POR MUERTE", [("Monstruo de tu nivel", 100, ["inv_misc_head_orc_01"] * 5),
                                          ("Monstruo verde", 80, ["inv_misc_head_orc_01"] * 4),
                                          ("Monstruo gris", 0, ["inv_misc_head_orc_01"] * 1)]),
       ("bajó a propósito la experiencia", -.3), ("Ni las gracias|fin", .6),
       ["bajó a propósito", "entre un cuatro y un veinte", "Y los grises"], "xp verdes", y=.58),
    mg(M.experiencia("CON TODO PUESTO", [("inv_misc_food_15", "Bien alimentado +5 %"), ("spell_fire_fire", "Campamento"),
                                         ("inv_misc_bag_10", "Bolsa de dormir")], ("SUBES MÁS RÁPIDO", 3)),
       ("ahora hay bonos de comida y de campamento", -.3), ("unos quince minutos|fin", .6),
       ["bonos de comida", "y de campamento", "Bien alimentado", "unos quince minutos"], "bonos", y=.60),
    # =========================================================== 16 Recoger en grupo
    rel("Número dieciséis", "i_caja", "Objetos de misión", "no se comparten"),
    pv("el tiburón Bruce de Los Baldíos", "tiburon", "Bruce", dur=4.2, x=.78, y=.56, tam=460),
    # =========================================================== 15 Mazmorras sin misiones
    mg(M.contadores("MISIONES DE MAZMORRA", [("inv_misc_note_01", "Experiencia extra de las misiones", 50, None, 0),
                                             ("inv_misc_head_orc_01", "Experiencia de los monstruos", 20, 0, 1)], ("LAS MISIONES SIGUEN MANDANDO", 2)),
       ("las misiones de mazmorra pasaron a dar", -.3), ("No da igual|fin", .6),
       ["un cincuenta por ciento menos", "alrededor de un veinte", "No da igual"], "mazmorras", y=.58),
    mapa("azeroth_eses", [P(kal(44, 31), "Brazanegra", "tres barras sin misiones", "blackfathom"), P(ek(44, 21), "Ruinas de Lordaeron", "misiones desde el 15", "lordaeron")],
         ("una vuelta a Brazanegra", -.2), ("empiezan al nivel quince|fin", .5),
         ["una vuelta a Brazanegra", "como las Ruinas de Lordaeron"], "MAZMORRAS", "con sus misiones", zmax=1.3),
    # =========================================================== Overgear campaña 2: kit «WoW - Forever (nov)» + fondo de marca SIEMPRE
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="tú eliges, y pagas", a=("Número catorce", -.1), entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Talentos, rotación", dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="tú eliges, y pagas", dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción", a=CODIGO,
         entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=("Número catorce", -.1), entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== 14 Lanzadores
    filav("Ser mago, brujo o sacerdote", [("i_mago", "Mago", None), ("i_brujo", "Brujo", None), ("i_sacerdote", "Sacerdote", None)], y=.64, tam=280, dur=3.8),
    mg(M.contadores("DAÑO DE LOS HECHIZOS EN FOREVER", [("spell_frost_frostbolt02", "Daño base", 25, None, 0),
                                                        ("inv_staff_08", "Lo que aprovechas del poder con hechizos", 100, 0, 1)],
                    ("SIN PODER CON HECHIZOS, PEGAS MENOS", 2)),
       ("bajaron el daño base de los hechizos", -.3), ("en la mayoría de los hechizos de daño directo|fin", .6),
       ["bajaron el daño base", "y subieron cuánto aprovechan", "pegas menos"], "hechizos", y=.58),
    # =========================================================== 13 Libros
    mapa("azeroth_eses", [P(ek(43, 72), "Ventormenta", "Garon Wendell · Barrio de los Magos", "stormwind"),
                          P(ek(44, 20), "Entrañas", "Owen Thadd · Barrio de la Magia", "undercity")],
         ("Se entregan a Garon Wendell", -.2), ("en el Barrio de la Magia de Entrañas|fin", .6),
         ["Se entregan a Garon", "o a Owen Thadd"], "LOS LIBROS DE LA BIBLIOTECA", "unos cuarenta", zmax=1.3),
    filav("Con diez libros te dan un collar", [("i_collar", "10 libros", None), ("i_anillo", "20 libros", "con veinte un anillo"),
                                                ("i_baston", "25 libros", "y con veinticinco un arma")], y=.66, tam=280, dur=4.4),
    pv("el libro de Rumi de Gnomeregan", "gnomeregan", "Rumi de Gnomeregan · cuenta una vez", dur=4.4, x=.76, y=.56, tam=440),
    # =========================================================== 12 Bolsa de dormir
    rel("Número doce", "i_bolsa", "Bolsa de dormir acogedora", "nivel 14"),
    mapa("reinos_este_eses", [(42, 80, "Páramos de Poniente", "el naufragio", F("westfall")), (58, 52, "Loch Modan", None, F("loch_modan")),
                              (46, 34, "Laderas de Trabalomas", "y al final, la bolsa", None)],
         ("en los Páramos de Poniente para la Alianza", -.2), ("al final te llevas la bolsa|fin", .5),
         ["en los Páramos de Poniente", "como Loch Modan", "las Laderas de Trabalomas"], "LA BOLSA DE DORMIR", "búsqueda del tesoro · Alianza",
         objeto="inv_misc_bag_10", zmax=1.6),
    mg(M.experiencia("BOLSA DE DORMIR ACOGEDORA", [("inv_misc_bag_10", "+1 % por muerte"), ("inv_misc_bag_10", "+2 %"), ("inv_misc_bag_10", "+3 %")],
                     ("NO SE PIERDE AL MORIR", 3)),
       ("Da hasta tres acumulaciones", -.3), ("y no se pierden al morir|fin", .6),
       ["Da hasta tres", "un uno por ciento", "por muerte", "no se pierden al morir"], "bolsa", y=.60),
    # =========================================================== 11 Campamento
    filav("Sastrería pone un estandarte", [("i_estandarte", "Sastrería", None), ("i_vela", "Herboristería", "Herboristería una vela"),
                                            ("i_pesca", "Pesca", "y Pesca, una pecera")], y=.64, tam=280, dur=4.6),
    pv("La mejor es la tienda de Peletería", "i_peleteria", "Tienda: 1 h de descanso", dur=4.4, x=.78, y=.58, tam=380),
    # =========================================================== 10 Legado
    mg(M.consola("LA LETRA PEQUEÑA DEL LEGADO", [("Talento", "pide Bien descansado 5/5", ROJO, 0), ("Regateo", "no rebaja la equitación", ROJO, 1),
                                                  ("Emoción de la aventura", "no sirve en mazmorras", ROJO, 2)], [("16 PUNTOS", VERDE, 3)]),
       ("Primera trampa", -.2), ("pero con más dragones|fin", .6),
       ["Primera trampa", "Segunda: Regateo", "Tercera: Emoción", "planea los dieciséis"], "legado", y=.58),
    # =========================================================== gracias 2
    com("otra tanda de comentarios", "Ugydknx6VQkrA2g8_gl4AaABAg", dur=4.4, x=.30, y=.28),
    com("Nos pidieron seguir añadiendo mapas", "UgztUfCvY4o1Bt7QU-B4AaABAg", dur=5.0, x=.70, y=.40),
    com("Gracias: todos se leen", "UgxGTpG5livbEZMU6S14AaABAg", dur=4.4, x=.32, y=.66),
    # =========================================================== 9 Recolección
    mg(M.filas("PUNTOS DE LEGADO POR PROFESIÓN", [("Fabricación (6)", 18, ["trade_alchemy", "trade_blacksmithing", "trade_engraving",
                                                                         "trade_engineering", "inv_misc_armorkit_17", "trade_tailoring"]),
                                                 ("Recolección", 0, ["trade_mining", "trade_herbalism", "inv_misc_pelt_wolf_01"])]),
       ("Alquimia, Herrería, Encantamiento", -.3), ("ni el desuello|fin", .6), ["Alquimia, Herrería", "La recolección no da"], "legado oficios", y=.58),
    # =========================================================== 8 Montura del 40
    rel("Número ocho", "i_caballo", "Equitación de aprendiz", "100 de oro · nivel 40"),
    mapa("kalimdor_enus", [(59, 55, "Trinquete", "Strahad Farsan", F("strahad"))], ("con una misión de Strahad Farsan", -.4),
         ("en Trinquete|fin", 1.2), ["con una misión de Strahad"], "LA MONTURA DEL BRUJO", "gratis, por misión", objeto="spell_nature_swiftness", zmax=1.8),
    pv("con la misión del Tomo de la Nobleza", "i_destrero", "Paladín de la Alianza", dur=4.0, x=.80, y=.58, tam=360),
    pv("tienes dos caballos", "i_corcel_vil", "Uno de ellos, gratis", dur=3.0, x=.20, y=.60, tam=340),
    # =========================================================== 7 Oro
    mg(M.subasta("LO QUE CUESTA LLEGAR AL 60", [("classicon_warrior", "Entrenar del 1 al 60", "207 de oro", AMAR),
                                                ("ability_mount_ridinghorse", "Montura del 40", "100 de oro", AMAR),
                                                ("ability_mount_charger", "Equitación de oficial + épica", "≈ 1 200 de oro", AMAR)],
                 "≈ 1 300 DE ORO", cab=("QUÉ", "PRECIO")),
       ("Entrenar tu clase del uno al sesenta", -.3), ("unos mil trescientos de oro|fin", 1.0),
       ["Entrenar tu clase", "Súmale la montura", "la equitación de oficial", "unos mil trescientos"], "oro", y=.58),
    # =========================================================== burla 2
    com("una reflexión muy profunda", "UgxS9DC-4zQSTzy-H1l4AaABAg", dur=7.4, y=.30),
    pv("hasta el Rey Exánime", "lich_king", "Con alguien al oído", dur=3.6, x=.76, y=.56, tam=460),
    # =========================================================== 6 Idioma (el Humano)
    mg(M.chat([("Opciones › Idiomas y redes sociales", AMAR), ("Idioma preferido en línea: Español", VERDE),
               ("Enfriamiento: 24 horas · toda la cuenta", ROJO)], "Opciones"),
       ("Está en Opciones, Idiomas y redes sociales", -.4), ("esperas un día entero|fin", .8),
       ["Está en Opciones", "Idioma preferido en línea#2", "un enfriamiento de veinticuatro"], "idioma", x=.30, y=.68),
    # =========================================================== 5 Hermandad
    rel("Número cinco", "i_hermandad", "Hermandad", "Familiar Faces"),
    pv("capitales con un puñado de jugadores", "stormwind", "Un puñado de jugadores", dur=4.0, x=.20, y=.58, tam=460),
    # =========================================================== 4 Cajas
    rel("Número cuatro", "i_caja", "Waylaid Crate", "caja interceptada"),
    pv("puede traer una etiqueta de envío", "i_etiqueta", "+50 favor · +2 000 reputación", dur=4.6, x=.20, y=.60, tam=360),
    # =========================================================== 3 Favor
    mapa("azeroth_eses", [P(ek(54, 69), "Three Corners", "Crestagrana · Marcy Baker", "redridge"), P(kal(55, 48), "El Cruce", "Los Baldíos · Dokimi", "crossroads")],
         ("La Alianza tiene el suyo", -.2), ("al oeste del Cruce, en Los Baldíos|fin", .6), ["La Alianza tiene", "La Horda, al oeste"],
         "CAMPAMENTOS DE COMERCIANTES", "Favor de comerciante", zmax=1.3),
    mg(M.subasta("RECETAS CON FAVOR", [("inv_misc_note_01", "Recetas iniciales", "30-45", AMAR), ("trade_engineering", "Ingeniería", "hasta 360", AMAR),
                                       ("ability_mount_kodo_01", "Kodo de carga", "6000 de favor", VERDE)], "600 RECETAS NUEVAS", cab=("QUÉ", "FAVOR")),
       ("Las recetas iniciales cuestan", -.3), ("Así está escrito#2", .4), ["Las recetas iniciales", "Las de ingeniería", "el Kodo de carga", "Así está escrito#2"],
       "favor", y=.58),
    # =========================================================== 2 Lo que ya no se pone solo
    rel("Número dos", "i_libro_hech", "Libro de hechizos", "ya no va solo a la barra"),
    filav("movieron niveles", [("i_furia", "Furia justa · nivel 10", None), ("i_picaro", "Pícaro · nivel 24", "y el pícaro aprende")], y=.64, tam=300, dur=4.4),
    pv("Las bolsas tampoco se equipan solas", "i_bolsa_comp", "5.ª ranura: componentes", dur=4.4, x=.78, y=.58, tam=360),
    # =========================================================== 1 Reglas y facción
    mg(M.reglas("CONJUNTOS DE REGLAS", [("inv_misc_note_01", "NORMAL"), ("inv_sword_04", "JcJ"), ("inv_misc_book_09", "ROL"),
                                        ("inv_bannerpvp_01", "ROL JcJ")], 1, "SIN CAMBIOS"),
       ("hay cinco megarreinos por región", -.3), ("hay que crear un personaje nuevo|fin", .6),
       ["Normal, JcJ", "JcJ, Juego de rol", "Juego de rol, Juego", "Juego de rol JcJ", "no puedes cambiar libremente"],
       "reglas", y=.56),
    com("Un espectador nos lo preguntó", "Ugyppq6BzAsCRa-jT694AaABAg", dur=6.6, x=.30, y=.30),
    # =========================================================== cierre: la votación
    aba([("i_abisario", "Mascota"), ("i_fogata", "Fogata"), ("i_caja", "Cajas"), ("i_libro_hech", "Hechizos")], "Y esos son los veinticinco errores",
        ("a un reino sin vuelta atrás|fin", .6), ["Y esos son los veinticinco", "de una mascota de cartón", "a un reino sin vuelta"], "cierre"),
    mg(M.votacion("¿QUÉ VOZ SE QUEDA?", ["Remy", "Edoardo", "José", "Mario", "Hope", "MariCarmen", "el Profeta", "el Humano"],
                  "VOTA EN LOS COMENTARIOS", icos=[ICO_VOZ[v] for v in ORDEN]),
       ("Y ahora lo importante: vota", -.2), ("nos vemos en Azeroth|fin", .4),
       ["Y yo soy la de siempre", "Te saqué de la Piedra", "Yo también elegí el modo", "No corrí", "Con hache, y con campamento",
        "Te ahorré cien de oro", "Yo no pido votos", "La única voz de esta lista", "Todos los comentarios se leen"], "papeleta cierre", y=.50),
] + placas()
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]
ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="25 ERRORES", en="los veinticinco errores que estás", dur=2.8, tam=140, color="amarillo", y=.2),
    dict(texto="ES UNA PIEDRA", en="Es una piedra", dur=2.2, tam=140, color="amarillo", y=.2),
    dict(texto="−4 % A −20 %", en="entre un cuatro y un veinte", dur=2.4, tam=130, color="rojo", y=.2),
    dict(texto="NO DA IGUAL", en="No da igual", dur=2.0, tam=150, color="rojo", y=.2),
    dict(texto="−25 %", en="un veinticinco por ciento menos", dur=2.2, tam=160, color="rojo", y=.2),
    dict(texto="DOS CABALLOS", en="tienes dos caballos", dur=2.4, tam=140, color="amarillo", y=.2),
    dict(texto="SIN FICHA DE WOW", en="no hay Ficha de World of Warcraft", dur=2.4, tam=120, color="rojo", y=.2),
    dict(texto="24 HORAS", en="un enfriamiento de veinticuatro horas", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="6 DE NOVIEMBRE", en="ajustes para el seis de noviembre", dur=2.4, tam=130, color="amarillo", y=.2),
    dict(texto="UNA VEZ", en="Eso pasa una sola vez por personaje", dur=2.2, tam=150, color="amarillo", y=.2),
    dict(texto="SIN VUELTA ATRÁS", en="hay que crear un personaje nuevo", dur=2.6, tam=130, color="rojo", y=.2),
]
SFX = {}
# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/wow/, copiado a sfx/), solo en momentos clave
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número veinticinco", "Número veinte.", "Número quince", "Número diez", "Número cinco")]
PISTAS += [dict(sfx="mision_completada", en=e, vol=.22) for e in ("Elegir conjunto de reglas", "Y esos son los veinticinco")]
PISTAS += [dict(sfx="subasta", en=e, vol=.26) for e in ("se compran y se venden en la subasta", "vende en la subasta")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Así que hoy te traigo los veinticinco",)]

# APOYOS: tarjetas SOLO con datos del guion (fuentes en videos/_investigacion_wow_errores_forever.md)
V, GR, RJ = "verde", "gris", "#ff3b3b"
APOYOS = [
    dict(en="Y encima, los enemigos de nivel alto", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Notas del lanzamiento", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Enemigos de nivel alto: más vida", dict(t="Las peleas duran más", c=RJ)])),
    dict(en="en los reinos de JcJ es un faro", dur=4.4, x=.72, size=.50, tarjeta=dict(titulo="Fogata en JcJ", calidad=RJ, icono="spell_fire_fire",
         lineas=["Atrae a los enemigos", dict(t="Y además quema", c=RJ)])),
    dict(en="En Forever no hay buscador de mazmorras", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Sin buscador de mazmorras", calidad=RJ,
         icono="inv_misc_groupneedmore", lineas=["Sin cola automática", "Sin grupo automático", dict(t="Sin teletransporte", c=RJ)])),
    dict(en="Lo que sí hay es el tablón", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Buscar grupo", calidad="verde", icono="inv_misc_groupneedmore",
         lineas=["El tablón del Classic", dict(t="Estilo de juego obligatorio", c=V)])),
    dict(en="Forever ya trae de serie", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Ya viene en el juego", calidad="verde", icono="inv_misc_spyglass_02",
         lineas=["Medidor de daño", "Gestor de reutilizaciones", dict(t="Guía de misiones", c=V)])),
    dict(en="salieron cientos de addons", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Addons hechos con IA", calidad=RJ, icono="trade_engineering",
         lineas=["Cientos para Forever", dict(t="En Reddit piden limitarlos", c=RJ)])),
    dict(en="El día del lanzamiento, un periodista", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Kotaku · 5 de noviembre", calidad="amarillo",
         icono="inv_misc_note_02", lineas=["Veía a los jugadores de otra capa", dict(t="Pero no a sus monstruos", c=RJ)])),
    dict(en="El veintitrés de octubre, Blizzard", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Promesa del 23 de octubre", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Los grupos que viajan juntos", dict(t="ya no se separarían", c=V)])),
    dict(en="En Forever hay una ruta nueva", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Ruta nueva", calidad="verde", icono="inv_misc_map_01",
         lineas=["Ventormenta → Auberdine", dict(t="Barco directo", c=V)])),
    dict(en="los objetos de misión no se comparten", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Objetos de misión", calidad=RJ, icono="inv_crate_01",
         lineas=["No se comparten en grupo", dict(t="Cada uno, los suyos", c=RJ)])),
    dict(en="Aggrend dijo que nunca digan nunca", dur=4.4, x=.72, size=.50, tarjeta=dict(titulo="Aggrend · pódcast oficial", calidad="amarillo",
         icono="inv_misc_note_02", lineas=["«Nunca digas nunca»", dict(t="Nada anunciado", c=GR)])),
    dict(en="Por eso las armas de lanzador", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Armas de lanzador", calidad="azul", icono="inv_staff_08",
         lineas=["Daño o sanación desde el nivel 10", dict(t="Equipo de sanador: poder con hechizos", c=V)])),
    dict(en="En la Temporada de Descubrimiento solo", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Libros de la biblioteca", calidad="azul",
         icono="inv_misc_book_09", lineas=["Unos 40 únicos", dict(t="Los recoge cualquier clase", c=V)])),
    dict(en="Hacia el nivel cinco, un aventurero", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="The Great Outdoors", calidad="amarillo",
         icono="spell_fire_fire", lineas=["Nivel 5 · primer pueblo", dict(t="Abre el campamento", c=V)])),
    dict(en="El sistema de legado es nuevo", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Sistema de legado", calidad="naranja",
         icono="inv_misc_book_11", lineas=["De toda la cuenta", dict(t="16 puntos por personaje", c=V)])),
    dict(en="Según un cálculo con los datos", dur=4.8, x=.72, size=.50, tarjeta=dict(titulo="Del 1 al 60", calidad="amarillo", icono="trade_blacksmithing",
         lineas=["Dos de fabricación: hasta 11 puntos", dict(t="Dos de recolección: 5", c=RJ)])),
    dict(en="Y en Forever no hay Ficha", dur=4.4, x=.72, size=.50, tarjeta=dict(titulo="Ficha de WoW", calidad=RJ, icono="inv_misc_coin_01",
         lineas=["No existe en Forever", dict(t="El oro se gana jugando", c=GR)])),
    dict(en="Como en Forever no hay reinos", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Sin reinos", calidad="amarillo", icono="inv_misc_map_01",
         lineas=["Te junta con tu mismo idioma", dict(t="Idioma preferido en línea", c=V)])),
    dict(en="El sistema de capas de Forever", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Familiar Faces", calidad="verde", icono="inv_shirt_guildtabard_01",
         lineas=["Tu hermandad, en tu capa", dict(t="Y la gente con la que te cruzaste", c=V)])),
    dict(en="Si las llenas con los materiales", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Waylaid Crate", calidad="verde", icono="inv_crate_01",
         lineas=["Llénala con lo que pide", dict(t="5-20 de Favor de comerciante", c=V)])),
    dict(en="Hay más de seiscientas recetas", dur=4.4, x=.72, size=.50, tarjeta=dict(titulo="Favor de comerciante", calidad="naranja", icono="inv_misc_coin_17",
         lineas=["+600 recetas nuevas", dict(t="Campamentos de comerciantes", c=V)])),
    dict(en="En las notas del dos de noviembre", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Notas del 2 de noviembre", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Los hechizos no van solos a la barra", dict(t="Las bolsas no se equipan solas", c=RJ)])),
    dict(en="Y según Blizzard, no puedes cambiar", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Cambiar de reglas", calidad=RJ, icono="inv_misc_note_01",
         lineas=["No se puede libremente", dict(t="Personaje nuevo", c=RJ)])),
]
