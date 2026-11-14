# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «La Reina Loba de Soledad» (SECUENCIA YT, Crónicas de Tamriel, 12-nov-2026). FORMATO NUEVO: historia de lore.
REGLA DE ORO (tes_secretos_40): lo que dice la voz SE VE (escenas de Flow con el acabado de Skyrim = `pant()` a cuadro entero cuando
el juego no lo tiene), pegatinas reales con el rotador `pv()`, estilos de peg_estilos, MG de `mg_tes` nuevos para este guion
(cronología de la familia, cordura de Pelagio, versiones de su infancia, informe de Kintyra…), mapas de Tamriel y de Skyrim con
ruta, placa del personaje en cada frase de una voz de personaje (sale de guion.NARRA), comentarios y campaña.
    python fab.py tes_reina_loba fx --seco      FAB_FX_FINAL=1 python fab.py tes_reina_loba fx hoja
"""
import os

import mg_tes as T
import mg_wow as W
import peg_estilos as PE
from _arbol import arbol as ARBOL, PERSONAS as _PERS
# v3 (13-nov): redes de relaciones e intenciones (mg_tes.red), una por capítulo; plan en previews/relaciones_plan.md
from _relaciones import (red_cap1, red_cap2, red_cap3, red_cap4, red_cap5, red_cap6, red_cap7,
                         PASOS_CAP1A, PASOS_CAP3)

CAMARA = {}
FUNDIDO = {}

_AQUI = os.path.dirname(os.path.abspath(__file__))
_FX, _FY = .76, .30
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_PEG = "tes"
TEMA_MAPA = "tes"


def P(slug):
    return os.path.join(_PEG, slug + ".png")


# ---------------------------------------------------------------- helpers (de tes_builds_rotas / tes_secretos_40)
def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro(_f(fotos), tema=TEMA_PEG, destaca=destaca, titulo=titulo), de, a, marcas, "muro")


def ficha(en, nombre, efecto, origen=None, dur=4.5, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def sil(en, slug, nombre=None, sub=None, dur=4.5, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.0, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas, sello=None, x=.74, y=.50, ancho=560, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def mis(en, arriba, titulo, dur=3.4, y=.30):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def capitulo(en, n, titulo):
    return dict(tipo="mg", fn=T.mision(f"Capítulo {n}", titulo), en=en, dur=3.6, y=.16, sale=.4, nombre="capítulo " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(P("com_" + cid), "", tam, giro=-3.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + cid, ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    """Escena de Flow con el acabado de Skyrim a cuadro entero (lo que el juego no tiene: la boda, el asedio, el carruaje…)."""
    return dict(tipo="pantalla", fn=W.pantalla(P("flow_" + slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla flow_" + slug, ver=2.0)


def fl3(n, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.08):
    """v3 (13-nov): escena de Flow v3 (pegatinas/flow3_NNN.png, Oblivion 2006 / Skyrim vanilla) a cuadro entero."""
    return dict(tipo="pantalla", fn=W.pantalla(P("flow3_" + n), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla flow3_" + n, ver=2.0)


def mapa(img, titulo, puntos, de, a, marcas, sub, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, img), puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)
    e = .05 if kw.get("entrada") else .5
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=e, sale=e, nombre="mapa " + sub, ver=4.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def pt(xy, nombre, tipo, foto=None):
    return (xy[0], xy[1], nombre, tipo) + ((P(foto),) if foto else ())


def narra(en, nombre, lema, dur=4.0):
    return dict(tipo="mg", fn=T.narrador(nombre, lema), en=en, dur=dur, x=.80, y=.83, sale=.35, nombre="placa narra " + nombre, ver=1.2)


# ---------------------------------------------------------------- coordenadas
# mapas/tamriel.jpg (Fandom «Tamriel Map», rotulado; rejilla en videos/tes_seres_poderosos/previews/_tamriel_rejilla.jpg)
IMPERIAL, SOLEDAD_T, CAMLORN = (.545, .49), (.42, .058), (.064, .265)
GILANE, MOURNHOLD, LILMOTH = (.164, .456), (.818, .495), (.79, .955)
ROCA_ALTA, PARAMO, SKYRIM_T = (.14, .21), (.24, .40), (.52, .20)
ESTIVALIA, PYANDONEA = (.12, .74), (.03, .97)
# mapas/skyrim.jpg (UESP, `_coords_uesp.py` del 12-nov)
SOLEDAD, CRANEO, PUENTE = (.342, .202), (.270, .194), (.261, .264)
TEMPLO, CATACUMBAS, PALACIO = (.357, .185), (.351, .155), (.372, .212)

# ---------------------------------------------------------------- comentarios (≤ 10 días, ninguno usado antes)
C_BRANDO, C_ROLFASO, C_EME = "Ugz3wyKcm_Nvkv4yYmJ4AaABAg", "UgzLBOZs1FQI6gvvMut4AaABAg", "Ugx8K4yad15Ioos64ap4AaABAg"
C_MOTO, C_CLAUDIO, C_DSEG = "UgxzWftu5yXE5F_jkUV4AaABAg", "UgyzlGAAMm4iJvIs3Xp4AaABAg", "UgwhKefaeoCNUbdLKnh4AaABAg"
C_JUANK, C_EXONIK = "UgyWGLp7SYyjRkhMV8t4AaABAg", "UgxsOvyP6jbokXmarD54AaABAg"

FX = [
    # ================= GANCHO: la cueva, el ritual, la calavera; un elemento nuevo cada 2-3 s
    zoom(0.0, "Afuera, dos esqueletos", 1.12),
    pv("Al oeste de Soledad", "soledad", "Soledad", dur=2.6, x=.18, y=.60, tam=360, entrada="tinta"),
    pv("Afuera, dos esqueletos", "esqueleto_skyrim", "Dos esqueletos", dur=2.4, x=.80, y=.60, tam=320, marco="naipe"),
    pv("Adentro, una luz azul", "cueva_wolfskull", "Cueva Cráneo de Lobo", dur=3.0, x=.20, y=.58, tam=420),
    pv("Una calavera con diadema", "potema_calavera", "Calavera de Potema", dur=3.0, x=.78, y=.56, tam=380, entrada="aplasta"),
    pv("debajo del Templo de los Divinos", "templo_divinos", "Templo de los Divinos", dur=2.8, x=.20, y=.60, tam=360, marco="vitral"),
    pant("cerradura", "abrió la cerradura más difícil del palacio imperial", ("Una reina que hizo desaparecer", .2), zoom=(1.05, 1.15)),
    pant("torre_kintyra", "Una reina que hizo desaparecer", ("Una madre que vio a su hijo", .2)),
    pant("carruaje", "Una madre que vio a su hijo", ("Y una anciana que", .2), oscuro=.1),
    pant("anciana_gema", "Y una anciana que", ("Hay una frase en Skyrim", .1)),
    pv("La dice Styrr", "styrr", "Styrr · sacerdote de Arkay", dur=4.0, x=.20, y=.58, tam=420, marco="museo"),
    mis("Esta es la historia de Potema Septim", "Crónicas de Tamriel", "La Reina Loba de Soledad", dur=4.2, y=.30),
    sil("Es una historia de familia", "potema_calavera", "Potema Septim", "La Reina Loba", dur=4.0, lado="der", alto=820),

    # ================= 1 · LA NIÑA DE LAS CERRADURAS
    capitulo("Capítulo uno", 1, "La niña de las cerraduras"),
    mapa("tamriel.jpg", "Tamriel", [pt(CAMLORN, "Camlorn", "inicio"), pt(IMPERIAL, "Ciudad Imperial", "poder", "ciudad_imperial")],
         "la ciudad bretona de Camlorn", ("Pelagio la convierte en anillo", .1), ["la ciudad bretona de Camlorn", "Un príncipe imperial, Pelagio"],
         "Camlorn", entrada="desenrolla"),
    pant("camlorn_lobo", "Él con la espada y ella con la hechicería", ("Y Quintila encierra el alma", .1)),
    pant("gema_lobo", "Y Quintila encierra el alma", ("Ese primer hijo nace", .1), zoom=(1.0, 1.18)),
    # ÁRBOL GENEALÓGICO (el usuario, 13-nov: «para no perdernos»), 1 de 5: crece con la historia
    mg(ARBOL([dict(ver=["pelagio2", "antioco"]), dict(ver=["quintila"]), dict(ver=["potema"], foco=["potema"])]),
       "Pelagio la convierte en anillo", ("Ese primer hijo nace", .1),
       ["Pelagio la convierte en anillo", "y se casa con ella", "hasta que nació su primer hijo"], "árbol 1", y=.5),
    mg(T.cronologia("La familia Septim", [("3E 63", "Pelagio y Quintila: el lobo", 0), ("3E 67", "Nace Potema", 1),
                                           ("3E 80", "El contrato robado", 2), ("3E 81", "Reina de Soledad, a los 14", 3)]),
       "Ese primer hijo nace", ("La niña crece en el Palacio Imperial", .1),
       ["Ese primer hijo nace", "Una niña.#2", "Su abuelo, el emperador Uriel Segundo", "La llaman Potema"], "cronología 1", y=.46),
    pant("cuna_potema", "la mira en la cuna", ("La niña crece en el Palacio Imperial", .1)),
    pv("bajo la Torre de Oro Blanco", "torre_oro_blanco", "Torre de Oro Blanco", dur=3.6, x=.78, y=.56, tam=420, entrada="cae"),
    pv("Le roba al archimago", "libro_hechizos", "Libro del archimago", dur=2.6, x=.18, y=.60, tam=320),
    pv("Un broche con un diamante rojo", "broche_diamante", "El broche del diamante rojo", dur=4.0, x=.76, y=.54, tam=440, entrada="cristal"),
    pant("nina_tapiz", "Año ochenta. Llueve", ("Del otro lado, su abuelo", 1.5)),
    # ficha("Del otro lado, su abuelo", "El contrato", "Una boda prometida con Soledad y el *oro* que no se devolvió",  # v3: sale por red cap1
    #       "Salón de los Registros", dur=5.0),  # v3: sale por red cap1
    # RED 1A · el trato roto, Potema escucha (v3, 13-nov)
    mg(red_cap1(PASOS_CAP1A), ("Del otro lado, su abuelo", 1.5), "Corre al Salón de los Registros",
       [("Del otro lado, su abuelo", 1.6), "al embajador de Soledad", "la boda prometida con su tía", "El embajador amenaza con el contrato",
        "Potema no espera al final"], "red cap 1A", y=.5),
    pant("cerradura", "Corre al Salón de los Registros", ("Cuando el paje llega", .1), zoom=(1.0, 1.2)),
    mis("Tardó casi medio minuto", "Cerradura forzada", "Maestra", dur=3.0, y=.30),
    # RED 1B · el contrato ya no está (v3, 13-nov)
    mg(red_cap1(), ("Cuando el paje llega", .2), "Sesenta y dos años",
       ["Cuando el paje llega", "ya no está", "el emperador tiene que ofrecer", "Ofrece a su nieta", "Es, lo admito", "El novio es Mantiarco"],
       "red cap 1B", y=.5),
    # cam("Es, lo admito", "uriel_ii", "Uriel II", dur=3.4, x=.18, y=.62),  # v3: sale por red cap1
    # cam("Tiene trece años", "pelagio_ii", "Pelagio II", dur=3.0, x=.18, y=.62),  # v3: sale por red cap1
    pant("boda_soledad", "Sesenta y dos años", ("Los libros lo cierran", .1)),  # v3: antes de «El novio es Mantiarco»
    leg("libro_emblema_potema", "La Reina Loba · libro I", ["Waughin Jarth", "Dentro del juego"], "Los libros lo cierran", ("Capítulo dos", -.3),
        ["Los libros lo cierran"]),

    # ================= 2 · LA REINA DE SOLEDAD
    capitulo("Capítulo dos. La reina", 2, "La reina de Soledad"),
    mapa("tamriel.jpg", "Tamriel", [pt(IMPERIAL, "Ciudad Imperial", "inicio"), pt(SOLEDAD_T, "Soledad", "poder", "palacio_azul")],
         "Se casa a los catorce años", ("Mientras tanto, en Soledad", .1), ["Se casa a los catorce años", "su padre se convierte"],
         "A Soledad", ventana=True, ancho=900, x=.70, y=.45, entrada="foco"),
    ficha("disuelve el Consejo de Ancianos", "Pelagio II", "Disuelve el Consejo y cobra a cada uno *su asiento*", "Tesoro: vacío", dur=4.4),
    pv("las viejas casas de la ciudad", "palacio_azul", "Palacio Azul", dur=3.6, x=.20, y=.58, tam=420, marco="polaroid"),
    mg(T.cordura("Quince años", P("potema_reina_joven"), [("Pierde un embarazo.", 0), ("Y otro.", 1), ("Y otro.", 2)], final=("Un hijo: Uriel", 3)),
       "Pierde un embarazo", ("El curandero, Kelmeth", .1),
       ["Pierde un embarazo", "Y otro. Y otro", "Durante quince años", "da a luz a un hijo"], "quince años", y=.48),
    pant("espejo", "El curandero, Kelmeth", ("Pero mientras grita", .3)),
    mg(ARBOL([dict(ver=["pelagio2", "quintila", "antioco", "potema", "mantiarco", "uriel"], foco=["mantiarco", "potema", "uriel"]),
              dict(ver=["bathorgh"], foco=["mantiarco", "potema", "uriel", "bathorgh"]),
              dict(foco=["bathorgh", "uriel"], nota="El heredero estorba")]),
       "El problema se llama Bathorgh", ("Potema ya se había", .1),
       ["El problema se llama Bathorgh", "Es el hijo del primer matrimonio", "el heredero legítimo"], "árbol 2", y=.5),
    # mg(T.sospechosos("El hombre al que no se puede golpear", (P("palacio_azul"), "Cartas de amor"), (P("bathorgh"), "Bathorgh"),  # v3: sale por red cap2
    #                  (P("potema_reina_joven"), "Potema")),  # v3: sale por red cap2
    #    "Potema ya se había encargado", ("Ese mismo día, Bathorgh", .1),  # v3: sale por red cap2
    #    ["Potema ya se había encargado", "con pruebas falsas de traición", "aparecen cartas de amor", "fechadas justo cuando", "Ahora manda restaurar"],  # v3: sale por red cap2
    #    "Bathorgh", y=.50),  # v3: sale por red cap2
    # RED 2 · el heredero que estorba (v3, 13-nov)
    mg(red_cap2(), "Potema ya se había encargado", ("Ese mismo día, Bathorgh", .1),
       ["Potema ya se había encargado", "Lord Thone, con pruebas falsas", "Ahora manda restaurar", "aparecen cartas de amor",
        "fechadas justo cuando"], "red cap 2", y=.5),
    pant("torneo", "Ese mismo día, Bathorgh", ("El bebé de Potema", .1)),
    ficha("lo deshereda y lo destierra", "Bathorgh", "*Desheredado* y desterrado la misma noche", "Gracias a unas cartas", rojo=True, dur=3.6),
    ficha("Ni era mujer lobo", "«Reina Loba»", "Un insulto de sus *enemigos*. Nunca fue mujer lobo", "Lo que casi todos cuentan mal",
          rojo=True, dur=4.6, x=.26, y=.30),

    # ================= PREGUNTA AL PÚBLICO (el usuario, 12-nov)
    mis("Un momento. Antes de seguir", "Pregunta al público", "¿Les gusta este formato?", dur=4.0, y=.30),
    mg(T.votacion("¿Qué quieren en el canal?", ["Historias de lore como esta", "Solo listas y tops"], remate="Escríbanlo en los comentarios"),
       "Pero necesitamos saberlo", ("Que viene un funeral", -.2),
       ["Pero necesitamos saberlo", "Si quieren más historias así", "Si prefieren seguir solo con listas", "también lo vamos a saber"],
       "votación formato", y=.42),

    # ================= 3 · LA GEMA DEL LOBO
    capitulo("Capítulo tres", 3, "La gema del lobo"),
    pant("funeral", "muere en plena fiesta", ("El Consejo de Ancianos retrasa", .1)),
    mapa("tamriel.jpg", "Al funeral", [pt(MOURNHOLD, "Almalexia · Magnus", "paso", "magnus"), pt(GILANE, "Gilane · Céforo", "paso", "cefor_i"),
                                       pt(SOLEDAD_T, "Soledad · Potema", "paso", "potema_reina_joven"), pt(IMPERIAL, "Ciudad Imperial", "poder", "antioco")],
         "Al funeral llegan sus hijos", ("El Consejo de Ancianos retrasa", .1),
         ["Magnus, de diecinueve años", "Céforo, de veintiuno", "Antíoco, el heredero", "Y la última en llegar"], "funeral", entrada="mesa"),
    pant("balcon_collar", "En un balcón, su madre", ("Potema la usa esa misma noche", .1)),
    rel("Y le hace un regalo", "gema_lobo", "Gema de alma amarilla", "Encantada con Ilusión", dur=4.4, x=.76, y=.52),
    # mg(T.cadena("La trampa", [("Hechiza al espía", None), ("Entra al estudio", None), ("Usa su sello", None), ("Falsifica la carta", None)]),  # v3: sale por red cap3
    #    "Potema la usa esa misma noche", ("A la mañana siguiente", .1),  # v3: sale por red cap3 (misma ventana: se encimaba)
    #    ["Hechiza al espía", "entra en el estudio", "usa su sello", "falsifica una carta", "A la mañana siguiente"], "trampa", y=.50),  # v3: sale por red cap3
    # RED 3 · la gema del lobo (v3, 13-nov; ALTERNATIVA del plan: solo los 3 primeros pasos, el versus «Primera partida» se queda)
    mg(red_cap3(PASOS_CAP3[:3]), "Potema la usa esa misma noche", ("A la mañana siguiente", .1),
       ["Potema la usa esa misma noche", "Hechiza al espía", "falsifica una carta"], "red cap 3", y=.5),
    vs(("potema_reina_joven", "Potema"), ("antioco", "Antíoco"), "O renuncia al trono", ("Antíoco es coronado", .1),
       ["O renuncia al trono", "Un buen sueldo motiva más", "Yo seré emperador"], ganador=1, titulo="Primera partida"),
    ficha("Mantiarco muere al poco tiempo", "Regente de Soledad", "En nombre de un niño de *dos años*", "Y un collar que hechiza", dur=4.4),

    # ================= 4 · LOS ELFOS DEL MAR
    capitulo("Capítulo cuatro", 4, "Los elfos del mar"),
    cam("Antíoco reina veintiún años", "antioco", "Antíoco Septim", dur=3.4, x=.16, y=.64),
    pv("tiene una hija con su segunda esposa", "kintyra_ii", "Kintyra", dur=3.4, x=.80, y=.58, tam=380, entrada="volteo"),
    pv("Y el Palacio Azul de Soledad se convierte", "palacio_azul", "El Palacio Azul", dur=3.6, x=.20, y=.58, tam=420, marco="museo"),
    pant("barco_maormer", "Año ciento diez", ("Viene su rey, Orgnum", .5), zoom=(1.0, 1.14)),
    mapa("tamriel.jpg", "El mar", [pt(PYANDONEA, "Pyandonea", "inicio"), pt(ESTIVALIA, "Artaeum · los psijic", "paso", "artaeum_flow"),
                                   pt(SOLEDAD_T, "Soledad", "poder")],
         "Viene su rey, Orgnum", ("Antes pedían cincuenta", -.2), ["Viene su rey, Orgnum", "Humilla a los emisarios psijic"],
         "maormer", ventana=True, ancho=900, x=.70, y=.45, entrada="pliegue"),
    # mg(T.contadores("El negocio de la regente", [("Pedían los psijic", 50, 0, 1), ("Paga Antíoco", 12, 2, 3), ("Cobran", 8, 3, 4)],  # v3: sale por red cap4
    #                 remate=("Ganancia de Potema: 4 millones", 5)),  # v3: sale por red cap4
    #    "Antes pedían cincuenta", ("Los libros dicen que a ella", .1),  # v3: sale por red cap4
    #    ["Antes pedían cincuenta", "Al final lo hacen por ocho", "Potema les paga los ocho", "y le cobra los doce", "esa noche, el rey", "duerme con la regente"],  # v3: sale por red cap4
    #    "negocio psijic", y=.46),  # v3: sale por red cap4
    # RED 4 · el negocio de la regente (v3, 13-nov)
    mg(red_cap4(), "Antes pedían cincuenta", ("Tres meses después, frente a Artaeum", .1),
       ["Antes pedían cincuenta", "Al final lo hacen por ocho", "y le cobra los doce", "duerme con la regente", "en muchas culturas distintas",
        "hacer que la gente te odie"], "red cap 4", y=.5),
    pant("tormenta_artaeum", "Tres meses después, frente a Artaeum", ("Un momento, que hay correo", .1)),
    mis("Es la Guerra de la Isla", "Tercera Era · 110", "La Guerra de la Isla", dur=3.2, y=.30),

    # ================= CRÍTICA 1: @brandovelasquez957
    com("Un momento, que hay correo", C_BRANDO, dur=9.0, x=.50, y=.40, tam=900),
    narra("Decidimos. Hoy narra uno solo", "el Profeta", "Hoy narra uno solo", dur=4.0),
    mg(T.contadores("Lo que te espera esta noche", [("Reina con elfos de jalea", 1, 0, 0), ("Hijos quemados", 1, 1, 1), ("Emperadores locos", 1, 2, 2)],
                    remate=("Dormir: no garantizado", 3)),
       "Eso sí: con una reina", ("Capítulo cinco", -.3),
       ["con una reina", "un hijo quemado vivo", "un emperador loco", "no te prometo que duermas"], "no duermes", y=.46),

    # ================= 5 · LA EMPERATRIZ DE QUINCE AÑOS
    capitulo("Capítulo cinco", 5, "La emperatriz de quince años"),
    ficha("el emperador cae en coma", "Antíoco", "Coma durante la visita de Potema. Muere al año", "Nadie demostró nunca nada", rojo=True, dur=4.4),
    pant("luto_espejo", "scene-098",  # v3: cubre todo el beat 098 (antes: «Potema se viste de luto»)
         ("Y entra al Consejo de Ancianos", .1)),
    pant("consejo", "Y entra al Consejo de Ancianos", "scene-102:fin"),  # v3: hasta el final del beat 102 (antes: «El Consejo no la escucha» +.1)
    mg(T.versiones("¿De quién es hija Kintyra?", (P("antioco"), "Antíoco", ["El padre oficial"], 0),
                   (P("capitan_guardia"), "El capitán de la guardia", ["O el chico", "de la cisterna"], 1), veredicto=("CALUMNIA", 2)),
       "acusa: Kintyra no sería hija", ("La posteridad os juzgará", .1),
       ["acusa: Kintyra no sería hija", "del capitán de la guardia", "O del chico que limpia"], "calumnia", y=.48),
    pv("Kintyra, de quince años", "kintyra_ii", "Kintyra II · 15 años", dur=4.0, x=.20, y=.50, tam=440, marco="carta"),
    mis("es coronada el tres de Primera Semilla", "Tercera Era · 120", "Emperatriz Kintyra II", dur=3.4, y=.30),
    mg(ARBOL([dict(ver=[k for k in _PERS if k not in ("pelagio3", "katariah")], tacha=["antioco", "mantiarco", "pelagio2"],
                   foco=["kintyra", "potema", "uriel"], nota="La sobrina emperatriz contra la tía"),
              dict(foco=["cefor"], nota="Bianki, esposa de Céforo")]),
       "Potema y Uriel son desterrados", ("lo que hace mejor que hablar", 1.6),
       ["Potema y Uriel son desterrados", "a su cuñada, la reina Bianki"], "árbol 3", y=.5),
    mapa("tamriel.jpg", "Roca Alta", [pt(IMPERIAL, "Ciudad Imperial", "inicio", "kintyra_ii"), pt(PARAMO, "Montañas Cola de Dragón", "paso"),
                                      pt(ROCA_ALTA, "La Cañada", "poder", "torre_cañada")],
         "el duque Mentin de La Cañada pide auxilio", ("En la torre del castillo", .1),
         ["el duque Mentin de La Cañada", "montañas Cola de Dragón", "una ventisca mágica"], "La Cañada", entrada="foco"),
    leg("torre_cañada", "La carta falsa", ["Petición de refuerzos", "Con la letra de Kintyra"], "En la torre del castillo de La Cañada",
        ("Desaparecen los guardias", .1), ["Kintyra nunca escribió esa carta"], sello=("FALSA", 0)),
    pant("torre_kintyra", "Desaparecen los guardias", ("Cuando le preguntan al duque", .1)),
    # ficha("Y el oro.", "Duque Mentin", "Traicionó al Imperio por *miedo*… y por *oro*", "Duque de La Cañada", dur=4.0, x=.26, y=.30),  # v3: sale por red cap5
    # ficha("su mejor arma es el miedo", "El ejército de muertos", "Un rumor que ella misma *fomentaba*", "Todavía no era verdad", dur=4.6),  # v3: sale por red cap5
    # RED 5 · la trampa de La Cañada (v3, 13-nov)
    mg(red_cap5(), "Cuando le preguntan al duque", "Kintyra muere en su celda",
       ["Cuando le preguntan al duque", ("Cuando le preguntan al duque", 1.6), "si fue por miedo", "Y el oro", "Y sobre los rumores de que Potema",
        "su mejor arma es el miedo"], "red cap 5", y=.5),
    mg(T.informe("Expediente: Kintyra II", (P("kintyra_ii"), "Kintyra Septim II"),
                 [("Celda", "Torre de La Cañada", 0), ("Muerte", "23 de Fuego Hogar, 3E 123", 1), ("Orden de", "Uriel, hijo de Potema", 2)],
                 sello=("DIAMANTES ROTOS", 3)),
       "Kintyra muere en su celda", ("Capítulo seis", -.3),
       ["Kintyra muere en su celda", "veintitrés de Fuego Hogar", "por orden del hijo", "Lo llaman Diamantes Rotos"], "Kintyra", y=.48),

    # ================= 6 · LA GUERRA DEL DIAMANTE ROJO
    capitulo("Capítulo seis", 6, "La guerra del Diamante Rojo"),
    rel("El diamante rojo es el emblema", "estandarte_diamante_rojo", "El Diamante Rojo", "Emblema de los Septim", dur=3.3, x=.76, y=.50),
    mg(ARBOL([dict(ver=[k for k in _PERS if k not in ("pelagio3", "katariah")], tacha=["antioco", "mantiarco", "pelagio2", "kintyra"],
                   foco=["potema", "uriel"]),
              dict(foco=["potema", "uriel", "cefor", "magnus"], nota="Potema y Uriel contra Céforo y Magnus")]),
       "Y ahora dos ramas de la misma familia", ("En el ciento veintiuno, Uriel asedia", 1.8),
       ["Y ahora dos ramas de la misma familia", "se lo disputan"], "árbol 4", y=.5),
    pant("corona_uriel", "asedia durante dos semanas", "scene-121:fin"),  # v3: hasta el final del beat 121 (antes: «Su apellido de verdad» +2)
    ficha("Su apellido de verdad era Mantiarco", "Uriel «Septim» III", "Apellido real: *Mantiarco*", "El Septim valía más", dur=4.0),
    mapa("tamriel.jpg", "Tamriel partido en dos", [pt(GILANE, "Gilane · Céforo", "paso", "cefor_i"), pt(LILMOTH, "Lilmoth · Magnus", "paso", "magnus"),
                                                   pt(IMPERIAL, "Ciudad Imperial · Uriel III", "poder", "uriel_iii"), pt(SOLEDAD_T, "Soledad · Potema", "poder")],
         "Del otro lado quedan los dos hermanos", ("Verano del ciento veintisiete", .1),
         ["Céforo, rey de Gilane", "Y Magnus, rey de Lilmoth", "Tamriel entero se parte", "Los argonianos de Magnus"], "guerra", entrada="desenrolla"),
    pant("arenga", "Verano del ciento veintisiete", ("Uriel ha sido derrotado", .1), zoom=(1.0, 1.08)),
    mapa("tamriel.jpg", "Páramo del Martillo", [pt(PARAMO, "Ichidag", "poder", "cefor_i"), pt(GILANE, "Gilane", "paso")],
         "Uriel ha sido derrotado", ("Ese torpe idiota", -.1), ["en la campiña de Ichidag"], "Ichidag", ventana=True, ancho=820, x=.70, y=.45),
    pant("batalla_cienaga", "Pero no hay tiempo para llorar", ("Reúne a sus tropas", .1)),
    pant("arenga", "Reúne a sus tropas", ("Lo mira desde un cerro", .1), zoom=(1.12, 1.0)),
    pv("bajo el estandarte del diamante rojo", "estandarte_diamante_rojo", "Estandarte del Diamante Rojo", dur=4.2, x=.20, y=.40, tam=420, entrada="desenrolla"),
    pant("batalla_cienaga", "Lo mira desde un cerro", ("Y entonces sube al cerro", .1), zoom=(1.1, 1.22)),
    pant("mensajera", "Y entonces sube al cerro", ("Una turba asaltó la caravana", .1)),
    pant("carruaje", "Una turba asaltó la caravana", ("Céforo es proclamado emperador", 0), oscuro=.05),  # v3: antes acababa en «Ese día, el ejército»
    # pv("Céforo es proclamado emperador", "cefor_i", "Céforo I · emperador", dur=3.4, x=.80, y=.58, tam=400, marco="museo"),  # v3: sale por red cap6
    # RED 6 · dos ramas, un diamante (v3, 13-nov)
    mg(red_cap6(), "Céforo es proclamado emperador", "Antes de lo que viene",
       ["Céforo es proclamado emperador", ("Céforo es proclamado emperador", 1.3), "Ese día, el ejército de Potema",
        "gana la batalla de Estrella del Halcón", "Ella no mira a nadie"], "red cap 6", y=.5),
    mis("gana la batalla de Estrella del Halcón", "Batalla ganada", "Estrella del Halcón", dur=3.4, y=.45),  # v3: y .30 → .45 (centro de la red 6)

    # ================= AGRADECIMIENTOS + corrección (≥ 4 capturas)
    com("los comentarios de esta semana", C_MOTO, dur=5.2, x=.30, y=.32, tam=720),
    com("Lore de primera", C_CLAUDIO, dur=4.0, x=.68, y=.30, tam=680),
    com("Es el primer video que veo", C_DSEG, dur=4.6, x=.32, y=.62, tam=680),
    com("le dan ganas de volver a Skyrim", C_JUANK, dur=4.4, x=.30, y=.32, tam=700),
    com("Y @Exonik_Snk", C_EXONIK, dur=5.0, x=.68, y=.58, tam=700),
    ficha("Los leemos todos", "Comentarios", "Se leen *todos*. Y se toman en cuenta", "Los buenos y los que duelen", dur=4.0),
    ficha("@sinnombre5459 tiene razón", "Corrección", "Hermaeus Mora cobra los secretos de los *Skaal*", "No los de los Barbas Grises",
          dur=5.6, x=.26, y=.30),

    # ================= CRÍTICA 2: @rolfaso
    com("Y @rolfaso pregunta", C_ROLFASO, dur=6.0, x=.50, y=.40, tam=880),
    pv("Ella tenía generales vampiros", "vampiro_skyrim", "General vampiro", dur=3.6, x=.78, y=.58, tam=380, entrada="aplasta"),

    # ================= 7 · LA LOBA SOLA
    capitulo("Capítulo siete", 7, "La loba sola"),
    mg(T.soldados("Siete provincias cambian de bando", 7, remate=("Le queda Soledad", 1)), "los nobles de siete provincias", ("Y es aquí, no antes", .1),
       ["los nobles de siete provincias", "A Potema solo le queda"], "bando", y=.46),
    pv("Sus nigromantes levantan", "nigromante_skyrim", "Nigromantes", dur=3.4, x=.20, y=.60, tam=380),
    pv("Doncellas que son esqueletos", "draugr_skyrim", "Muertos que sirven", dur=3.0, x=.78, y=.58, tam=380, marco="naipe"),
    mapa("skyrim.jpg", "Soledad", [pt(SOLEDAD, "Soledad", "inicio", "soledad"), pt(CRANEO, "Cueva Cráneo de Lobo", "poder", "cueva_wolfskull")],
         "Y en una cueva al oeste de la ciudad", ("Año ciento treinta y siete", .1), ["Esa cueva todavía lleva el nombre"], "Cráneo de Lobo",
         ventana=True, ancho=900, x=.70, y=.45, entrada="foco"),
    pant("asedio", "Año ciento treinta y siete", ("Todos sus primos han muerto", .1)),
    mg(T.cronologia("Las edades del asedio", [("Magnus", "58 años", 0), ("Céforo", "60 años", 1), ("Potema", "70 años", 2)]),
       "Magnus tiene cincuenta y ocho años", ("En la ciudad sitiada", .1), ["Magnus tiene", "Céforo, sesenta", "Y Potema, setenta"], "edades", y=.46),
    pant("anciana_gema", "En la ciudad sitiada", ("La anciana le paga", .1)),
    rel("Al cuello lleva una gema amarilla", "gema_lobo", "La gema del lobo", "Una bestia de cuatro patas dentro", dur=4.4, x=.76, y=.50),
    mg(T.receta("La maldición", [(P("gema_lobo"), "Gema del lobo"), (P("nigromante_skyrim"), "Encantador nórdico")], (P("gema_lobo"), "Gema maldita"),
                "Quita la *sabiduría* año tras año"),
       "La anciana le paga a un encantador", ("Y compra un anillo barato", .1),
       ["La anciana le paga", "Una maldición#2", "Un veneno lento"], "maldición", y=.48),
    ficha("Y compra un anillo barato", "Anillo «de levitación»", "En realidad: resistencia al *fuego*", "Regalo para el tío Céforo",
          rojo=True, dur=5.4),
    pant("anciana_gema", "Luego se agacha", ("La anciana se va por un túnel", .1), zoom=(1.12, 1.25)),
    pant("muerte_cama", "La anciana se va por un túnel", "scene-170:fin", oscuro=.05),  # v3: todo el beat 170
    # ficha("en el ciento cuarenta, el emperador Céforo", "Céforo I", "Muere al caerse del *caballo*", "¿Llevaba un anillo?", rojo=True, dur=5.0),  # v3: sale por red cap7
    # RED 7 · lo que dejó la anciana (v3, 13-nov)
    mg(red_cap7(), "Tres años después, en el ciento cuarenta", "Y un último correo",
       ["Tres años después, en el ciento cuarenta", "muere al caerse de su caballo", "si llevaba puesto un anillo", "Tampoco hace falta"],
       "red cap 7", y=.5),

    # ================= CRÍTICA 3: @Eme_4r
    com("Y un último correo", C_EME, dur=7.0, x=.50, y=.40, tam=880),

    # ================= 8 · PELAGIO EL LOCO
    capitulo("Capítulo ocho", 8, "Pelagio el Loco"),
    mg(T.versiones("Su infancia: dos versiones", (P("libro_emblema_potema"), "La novela", ["12 años", "Niño en el asedio"], 0),
                   (P("pelagio_iii"), "Las crónicas", ["18 años", "Su primera batalla"], 1)),
       "hay dos versiones de su infancia", ("De joven, Pelagio es guapo", .1),
       ["hay dos versiones", "En las crónicas"], "dos versiones", y=.48),
    sil("De joven, Pelagio es guapo", "pelagio_iii", "Pelagio III", "Rey de Soledad", dur=5.0, lado="der", alto=860),
    mg(T.cordura("La cordura de Pelagio", P("pelagio_iii"),
                 [("Un corazón que le ensancha la cintura", 0), ("Como abrazar a un esqueleto", 1), ("Una declaración de guerra sin firmar", 2),
                  ("Se arranca la ropa en un discurso", 3)]),
       "Primero, el peso", ("En el ciento cuarenta y uno", .1),
       ["Primero, el peso", "como si la agarrara un esqueleto", "una declaración de guerra", "se arranca la ropa"], "cordura Pelagio", y=.48),
    mg(ARBOL([dict(ver=list(_PERS), tacha=["potema", "uriel", "cefor", "kintyra", "antioco", "mantiarco", "pelagio2", "quintila"],
                   foco=["pelagio3", "katariah"]),
              dict(tacha=["magnus"], foco=["magnus"]),
              dict(foco=["pelagio3", "magnus"], nota="¿Parricida?")]),
       "En el ciento cuarenta y uno se casa con Katariah", ("Pelagio es coronado emperador", .1),
       ["En el ciento cuarenta y uno se casa con Katariah", "muere Magnus, dormido", "Hay quien acusa a Pelagio"], "árbol 5", y=.5),
    pant("coronacion_pelagio", "scene-186",  # v3: todo el beat (debajo había subtítulos de Sheogorath)
         ("Con el embajador argoniano", .1)),
    pant("argoniano", "Con el embajador argoniano", ("Al final de un gran baile", .1)),
    mg(T.cordura("Cordura: segunda parte", P("pelagio_iii"),
                 [("Gruñe al embajador argoniano", 0), ("Obsesión con la limpieza", 1), ("Intenta ahorcarse en un baile", 2)],
                 final=("AL ASILO · 3E 147", 3)),
       "solo habla con gruñidos", ("Hay un libro, El baile del asilo", .1),
       ["solo habla con gruñidos", "está obsesionado con la limpieza", "intenta ahorcarse", "lo encierran en un asilo"], "cordura 2", y=.48),
    pant("baile_vacio", "Hay un libro, El baile del asilo", ("Se corta a sí mismo", .1), zoom=(1.0, 1.12)),
    ficha("Años después, en el escritorio", "Las invitaciones", "Cinco montones, con su letra de *niño*", "Nadie las recibió", dur=5.0),
    ficha("muere en el ciento cincuenta y tres", "Pelagio III", "Muere a los *34 años*, de fiebre", "Templo de Kynareth, en una isla", dur=4.6),
    mg(T.votacion("¿Qué volvió loco a Pelagio?", ["La gema de su tía", "Su estancia en Roca Alta", "Las piedras de Soledad"],
                  remate="La que menos los deje dormir"),
       "Fue la gema de su tía", ("Antes del final, un dato", -.2),
       ["Fue la gema de su tía", "Los bretones dicen", "Y otra leyenda dice", "Elijan la que menos"], "teorías", y=.44),

    # ================= CAMPAÑA DE SUSCRIPCIÓN (~75 %)
    mg(T.rejilla("De cada 100 que ven el canal", n=100, encendidas=13, remate=("Solo 13 están suscritos", 0)),
       "Antes del final, un dato", ("Somos seis mil seiscientos sesenta", -.2), ["solo trece están suscritos"], "campaña rejilla", y=.46),
    mg(T.contadores("La meta del canal", [("Suscriptores", 6660, 0, 1), ("Meta", 10000, 1, 2)], remate=("Ese botón también es tu voto", 2)),
       "Somos seis mil seiscientos sesenta", ("Capítulo nueve", -.3), ["Somos seis mil", "nos acercas a diez mil", "ese botón también"],
       "campaña meta", y=.46),

    # ================= 9 · QUINIENTOS AÑOS DESPUÉS (Skyrim)
    capitulo("Capítulo nueve", 9, "Quinientos años después"),
    pv("le suplica a la jarl Elisif", "elisif", "Jarl Elisif", dur=3.4, x=.18, y=.60, tam=400, marco="museo"),
    pv("Y Falk Barba de Fuego", "falk_firebeard", "Falk Barba de Fuego", dur=3.4, x=.80, y=.60, tam=400),
    mis("Es la misión El hombre de la falsa alarma", "Misión iniciada", "El hombre de la falsa alarma", dur=3.6),
    mapa("skyrim.jpg", "Soledad", [pt(PALACIO, "Palacio Azul", "inicio", "palacio_azul"), pt(PUENTE, "Puente del Dragón", "paso"),
                                   pt(CRANEO, "Cueva Cráneo de Lobo", "poder", "cueva_wolfskull")],
         "Bajas a la Cueva Cráneo de Lobo", ("Has dormido mucho tiempo", .1), ["Bajas a la Cueva Cráneo", "llegas a unas ruinas"], "misión 1",
         ventana=True, ancho=900, x=.70, y=.45, entrada="mesa"),
    ficha("Quieren atarla a su voluntad", "El ritual", "Atarla con sangre de *inocentes*", "No solo despertarla", rojo=True, dur=4.4),
    mis("Rompiste la atadura", "Misión completada", "El hombre de la falsa alarma", dur=3.4),
    mis("Es El despertar de la Reina Loba", "Misión iniciada", "El despertar de la Reina Loba", dur=3.6),
    pv("Styrr, el sacerdote del Salón", "styrr", "Styrr", dur=3.4, x=.20, y=.58, tam=400, marco="carta"),
    mapa("skyrim.jpg", "Soledad", [pt(TEMPLO, "Templo de los Divinos", "inicio", "templo_divinos"),
                                   pt(CATACUMBAS, "Catacumbas de Potema", "poder", "catacumbas_potema")],
         "La entrada está al fondo del Templo", ("Por fin has llegado", .1), ["detrás de una verja"], "catacumbas",
         ventana=True, ancho=820, x=.70, y=.45, entrada="foco"),
    sil("Por fin has llegado", "potema_calavera", "Potema", "Espíritu", dur=5.4, lado="der", alto=860),
    pv("Las Catacumbas de Potema", "catacumbas_potema", "Catacumbas de Potema", dur=3.6, x=.20, y=.58, tam=420, entrada="cortinilla"),
    pv("salen draugr del agua", "draugr_skyrim", "Draugr", dur=3.0, x=.80, y=.58, tam=360),
    rel("Y cuando aparecen sus restos", "potema_restos", "Restos de Potema", "Diadema de piedra lunar", dur=4.4, x=.76, y=.50),
    ficha("Fuerza Implacable", "Fuerza Implacable", "Grito · también ella era *Sangre de Dragón*", "Potema usa la Voz", dur=4.6),
    rel("solo queda su calavera", "potema_calavera", "Calavera de Potema", "Santificada por Styrr", dur=4.4, x=.24, y=.50),
    ficha("que nadie se entere", "Falk Barba de Fuego", "Que el regreso de Potema siga en *silencio*", "Petición de la jarl", dur=4.4),
    mis("Hasta Skyrim la quiso callar", "Misión completada", "El despertar de la Reina Loba", dur=3.6),

    # ================= 9b · EL ALA DE PELAGIO
    pv("El Ala de Pelagio", "ala_pelagio", "Ala de Pelagio", dur=4.0, x=.20, y=.58, tam=440, marco="vitral"),
    pv("Un mendigo loco de Soledad, Dervenin", "dervenin", "Dervenin", dur=3.4, x=.80, y=.58, tam=380),
    rel("te da un hueso", "pelvis_pelagio", "Pelvis de Pelagio", "Para entrar en su mente", dur=4.0, x=.76, y=.50),
    mis("Y con ella entras en su mente", "Misión iniciada", "La mente de la locura", dur=3.4),
    sil("está el Príncipe de la Locura", "sheogorath_skyrim", "Sheogorath", "Príncipe de la Locura", dur=5.0, lado="der", alto=860),
    rel("Te da el Wabbajack", "wabbajack", "Wabbajack", None, dur=4.0, x=.76, y=.50),
    mg(T.cadena("La mente de Pelagio", [("La Paranoia", None), ("La Confianza", None), ("Los Terrores Nocturnos", None)]),
       "Y tienes que curar tres partes", ("Con el Wabbajack conviertes", .1),
       ["La Paranoia", "La Confianza", "Y los Terrores Nocturnos"], "mente", y=.50),
    carr([("sacerdote_dragon", "Sacerdote dragón → cofre"), ("atronach_llamas", "Atronach → hoguera"), ("pelagio_nino", "Bandido → Pelagio niño")],
         "Un sacerdote dragón, en un cofre", ("Y la primera pesadilla", .1),
         ["Un sacerdote dragón", "Un atronach de llamas", "Un jefe bandido"], titulo="Pesadillas"),
    rel("Es un lobo.", "hombre_lobo", "El primer terror", "Un lobo", dur=4.0, x=.50, y=.50, tam=620),

    # ================= CIERRE
    mg(T.cadena("El Trono Rubí", [("Antíoco · se rió de ella", P("antioco")), ("Kintyra · la echó", P("kintyra_ii")),
                                  ("Uriel III · una noche", P("uriel_iii")), ("Pelagio III · la gema", P("pelagio_iii"))]),
       "La Reina Loba nunca se sentó", ("Quinientos años después, unos", .1),
       ["Lo tuvo su hermano", "Lo tuvo su sobrina", "Lo tuvo su hijo", "Y lo tuvo el niño", "Y lo tuvo el niño|fin"], "trono", y=.50),
    sil("Y ni muerta se dejó atar", "potema_calavera", "Potema", "Ni muerta se dejó atar", dur=3.0, lado="der", alto=860),
    mg(T.votacion("¿Qué historia cuenta el Profeta?", ["Los Sload", "Olaf Ojo Único", "Los hijos de Gauldur"], remate="Déjalo en los comentarios"),
       "Ahora te toca a ti", ("Y si te gustó este formato", .1), ["¿Los Sload", "¿Olaf Ojo Único", "¿Los hijos de Gauldur"], "próxima historia",
       y=.42),
    rel("Y si encuentras una gema amarilla", "gema_lobo", "No te la pongas", None, dur=4.0, x=.76, y=.50),
]

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_iniciada", en=e, vol=.20) for e in ("Es la misión El hombre", "Es El despertar de la Reina Loba",
                                                                   "Y con ella entras en su mente")]
PISTAS += [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Rompiste la atadura", "Hasta Skyrim la quiso callar")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.20) for e in ("Bajas a la Cueva Cráneo", "Las Catacumbas de Potema")]
PISTAS += [dict(sfx="grito", en=("Fuerza Implacable|fin", .1), vol=.80), dict(sfx="monedas", en="Al final lo hacen por ocho", vol=.22),
           dict(sfx="subir_nivel", en="Desde esta noche, soy Uriel", vol=.18)]

# ---- RELLENO de huecos > 6 s sin pegatina ni MG (sesión 4, 12-nov): fichas, pegatinas y escenas en la frase que las nombra
FX += [
    ficha("abrir lo que está cerrado", "Ganzúa", "Abre lo que está cerrado", origen="Habilidad: Forzar cerraduras", dur=4.0),
    ficha("Chantajea a la doncella de su madre", "Clases de ganzúa", "Maestra: una doncella bosmer · Pago: su silencio", origen="Palacio Imperial", dur=4.5),
    ficha("Al rey de Gilane, su corona", "Botín de una niña de doce", "Libro de hechizos · Corona de Gilane · Grabados khajiitas", origen="Robado", dur=6.0, rojo=True),
    # ficha("El embajador amenaza con el contrato", "Contrato de boda", "Firmado por el emperador", origen="Soledad · Ciudad Imperial", dur=4.5),  # v3: sale por red cap1
    # ficha("y como el documento no existe", "Contrato de boda", "DESAPARECIDO", origen="Salón de los Registros", dur=4.5, rojo=True),  # v3: sale por red cap1
    rel("Mientras tanto, en Soledad, la niña", "palacio_azul", "Palacio Azul", "Soledad", dur=4.5, x=.76, y=.50),
    ficha("le da órdenes a Lord Vhokken", "Lord Vhokken", "Su mano derecha · gigante calvo · voz de trueno", origen="Soledad", dur=6.5),
    pv("se llamará Uriel, como su bisabuelo", "uriel_iii_ob", "Uriel III · de mayor", dur=4.0, x=.80, y=.56, tam=380),
    ban("Sus enemigos ya la llamaban", "carga_reina_soledad", "La Reina Loba", "Así la llamaban sus enemigos", foco=(.5, .47, 1.0), dur=6.0),
    mg(T.votacion("¿Te gusta este formato?", ["Historia completa", "Listas y tops"]), "Esto es nuevo en el canal", ("Pero necesitamos saberlo", 0),
       ["Una sola historia", "Nada de listas"], "votación formato", y=.46),
    ficha("El Consejo de Ancianos retrasa", "Coronación de Antíoco", "Retrasada seis semanas", origen="Consejo de Ancianos", dur=4.5),
    cam("pone a su maestro de espías", "antioco", "Antíoco lo sabe", dur=4.0, x=.18, y=.62),
    ficha("Con un collar que hechiza", "Collar de la gema del lobo", "Hechiza a quien lo mira", origen="Regalo de Quintila", dur=5.0),
    ficha("por todas las enfermedades venéreas", "Antíoco Septim", "Estado de salud: todas", origen="Emperador", dur=4.5, rojo=True),
    ficha("Potema escucha a todos", "Promesas de Potema", "Cero", origen="Reyes resentidos con el emperador", dur=5.0),
    # pv("su capacidad para mentir funcionaba", "maormer", "Maormer · elfos del mar", dur=4.5, x=.80, y=.56, tam=420),  # v3: sale por red cap4 (va de icono en el nexo)
    ficha("Decidan, o dejaré", "Ultimátum", "Una sola voz o un oyente menos", origen="@brandovelasquez957", dur=4.5, rojo=True),
    cam("Potema y su hijo visitan", "uriel_iii", "Uriel III · su hijo", dur=4.5, x=.18, y=.62),
    pv("en la Sala de los Mapas", "ciudad_imperial", "Ciudad Imperial", dur=4.5, x=.80, y=.56, tam=420),
    # ficha("Cuando le preguntan al duque", "Duque Mentin", "Traidor · La Cañada", origen="Roca Alta", dur=5.0),  # v3: sale por red cap5
    pv("Que ella fomenta ese rumor", "draugr_skyrim", "El ejército de muertos: un rumor", dur=5.0, x=.82, y=.72, tam=420),  # v3: (.80, .56) → esquina vacía de la red 5
    # rel("Ella no mira a nadie", "estandarte_potema", "Estandarte de Potema", "La Reina Loba", dur=5.0, x=.76, y=.50),  # v3: sale por red cap6
    pv("Bienvenido: escogiste buen día", "soledad", "Bienvenido a Soledad", dur=4.5, x=.80, y=.56, tam=420),
    ficha("El Profeta no hace acentos", "Acento khajiita", "No disponible", origen="El Profeta", dur=4.5, rojo=True),
    ficha("te cobra con los secretos de los Skaal", "Corrección", "Los Skaal, no los Barbas Grises", origen="@sinnombre5459", dur=5.0),
    ficha("Te contesto como contestaría Potema", "Pregunta de vuelta", "¿Importa quién la cuenta?", origen="El Profeta", dur=6.0),
    pv("la Reina Loba invoca daedra", "atronach_llamas", "Daedra invocados", dur=4.5, x=.80, y=.56, tam=420),
    pv("Sus aliados la abandonan", "esqueleto_skyrim", "Soledad · tierra de muerte", dur=5.0, x=.20, y=.56, tam=420),
    pant("muerte_cama", "Murió en su cama", ("Tres años después", 0), zoom=(1.0, 1.08)),
    # ficha("Los libros no dicen si llevaba", "Anillo de levitación", "Regalo de su hermana · ¿maldito?", origen="Céforo I", dur=5.0, rojo=True),  # v3: sale por red cap7
    ficha("Ciego, no. Selectivo", "El Profeta", "Visión: selectiva", origen="Respuesta a @Eme_4r", dur=4.0),
    pv("déjame presentarte al sobrino", "pelagio_iii", "Pelagio III", dur=5.0, x=.80, y=.56, tam=440),
    pv("sufre terrores nocturnos", "pelagio_nino", "Terrores nocturnos", dur=4.5, x=.80, y=.56, tam=420),
    pv("La misma ciudad", "palacio_azul", "El mismo palacio", dur=4.0, x=.20, y=.56, tam=420),
    cam("Katariah se convierte en emperatriz", "katariah", "Katariah · emperatriz", dur=4.5, x=.18, y=.62),
    rel("un hombre de Puente del Dragón", "palacio_azul", "Palacio Azul", "Cuarta Era, 201", dur=4.0, x=.76, y=.50),
    pv("salen luces y ruidos extraños", "cueva_wolfskull", "Cueva Cráneo de Lobo", dur=5.0, x=.80, y=.56, tam=440),
    pv("¡Escúchanos, Reina Loba!", "potema_espiritu_2", "La Reina Loba despierta", dur=4.5, x=.80, y=.56, tam=440),
    pv("Matas al maestro del ritual", "nigromante_skyrim", "Maestro del ritual", dur=4.5, x=.80, y=.56, tam=420),
    ficha("Y te da una llave", "Llave de las Catacumbas de Potema", "Abre la verja del Templo de los Divinos", origen="Styrr", dur=5.0),
    pv("Su espíritu lanza rayos que giran", "potema_espiritu_2", "Espíritu de Potema", dur=4.0, x=.80, y=.56, tam=420),
    pv("De las tumbas salen oleadas de draugr", "draugr_skyrim", "Oleadas de draugr", dur=4.5, x=.20, y=.56, tam=420),
    # (13-nov) fuera pv «El ala suroeste»: la misma pegatina ala_pelagio ya estaba en pantalla a la vez
    ficha("Una criada entra una vez al año", "Ala de Pelagio", "Limpieza: una vez al año", origen="Las telarañas", dur=5.0),
    pv("Un bosque con niebla, arcos de piedra", "mente_arcos", "La mente de Pelagio", dur=5.0, x=.80, y=.56, tam=460),
    pv("¡Mi verdugo lleva tres días sin dormir!", "sheogorath_skyrim", "Sheogorath", dur=4.5, x=.20, y=.56, tam=420),
    pv("Estás dentro de la cabeza", "mente_bosque", "Dentro de la cabeza de Pelagio", dur=5.0, x=.80, y=.56, tam=460),
    pv("vive aterrada por un demonio hombre lobo", "hombre_lobo", "El demonio de Camlorn", dur=4.5, x=.80, y=.56, tam=440),
    pv("Generales vampiros#2", "vampiro_skyrim", "Generales vampiros", dur=4.0, x=.20, y=.58, tam=420),
    pv("se ve una bestia de cuatro patas", "gema_lobo", "Una bestia de cuatro patas", dur=4.5, x=.78, y=.52, tam=480),
    pv("Bajas a la Cueva Cráneo de Lobo", "cueva_wolfskull", "Cueva Cráneo de Lobo", dur=4.5, x=.80, y=.56, tam=440),
    ficha("Trampas de aceite", "Catacumbas de Potema", "Trampas de aceite · puertas de piedra que giran", origen="Templo de los Divinos", dur=5.0),
    pv("tomando el té con el emperador", "mesa_te", "El té", dur=5.0, x=.80, y=.56, tam=460),
    pv("Pelagio duerme en una cama", "mente_bosque", "Los Terrores Nocturnos", dur=5.0, x=.80, y=.56, tam=460),
]

# v3 (13-nov): ESCENAS DE FLOW v3 (Oblivion 2006 / Skyrim vanilla, flow/escenas_v3.md) a cuadro entero en la frase
# que cuentan; quitan el gameplay que no encajaba (glitch, tops, HUD). Debajo de pegatinas, fichas y redes.
# Generado por _flow3_plan.py --emitir (recortadas contra las pantallas de v2 que ya estaban).
FLOW3 = [
    # extra tras el OCR (14-nov): gancho sin la fogata con «Take Empty Wine Bottle» → la cueva de Flow (vuelve en el 206: misma cueva, a propósito)
    dict(fl3("206", "scene-001", ("scene-001:fin", .3), zoom=(1.0, 1.16), pan=(-.4, .2, .3, -.1), oscuro=.08), nombre="pantalla flow3_206 gancho"),
    # 244 (cierre): bandido con flechas → la gema amarilla con el lobo dentro, la que «no te pongas» (ya salió en el 164)
    dict(fl3("164", "scene-244", "scene-244:fin", zoom=(1.18, 1.0), pan=(.2, 0, 0, 0), oscuro=.05), nombre="pantalla flow3_164 cierre"),
    # 175: sala de guerra con subtítulos de Galmar → el Palacio Azul de Soledad, otro encuadre (en el 180 «la misma ciudad, el mismo palacio»)
    dict(fl3("180", "scene-175", ("scene-175:fin", 0.0), zoom=(1.30, 1.38), pan=(.7, .5, .4, .3), oscuro=.10), nombre="pantalla flow3_180 sobrino"),
    fl3("003", ("scene-003", 0.00), ("scene-003:fin", 0.00), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("009", ("scene-009", 0.00), ("scene-009:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("011", ("scene-011", 0.00), ("scene-011:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("017", ("scene-017", 0.00), ("scene-017:fin", 0.00), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("022", ("scene-022", 0.00), ("scene-022:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.08),
    fl3("023", ("scene-023", 0.00), ("scene-023:fin", -0.88), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("026", ("scene-026", 1.12), ("scene-026:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("027", ("scene-027", 0.00), ("scene-027:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("029", ("scene-029", 2.50), ("scene-029:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("030", ("scene-030", 0.00), ("scene-030:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("031", ("scene-031", 0.00), ("scene-031:fin", 0.00), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("034", ("scene-034", 0.00), ("scene-034:fin", 0.00), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("036", ("scene-036", 0.00), ("scene-036:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("037", ("scene-037", 0.00), ("scene-037:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("038", ("scene-038", 0.00), ("scene-038:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("039", ("scene-039", 0.00), ("scene-039:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.08),
    fl3("040", ("scene-040", 0.00), ("scene-040:fin", 0.00), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("043", ("scene-043", 0.00), ("scene-043:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("044", ("scene-044", 0.00), ("scene-044:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("045", ("scene-045", 0.00), ("scene-045:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("046", ("scene-046", 0.00), ("scene-046:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("047", ("scene-047", 0.00), ("scene-047:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("048", ("scene-048", 0.00), ("scene-048:fin", -3.98), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("050", ("scene-050", 4.67), ("scene-050:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("051", ("scene-051", 0.00), ("scene-051:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("052", ("scene-052", 0.00), ("scene-052:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("064", ("scene-064", 0.00), ("scene-064:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("068", ("scene-068", 0.00), ("scene-068:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("069", ("scene-069", 0.00), ("scene-069:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("070", ("scene-070", 0.00), ("scene-070:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.22),
    fl3("071", ("scene-071", 0.00), ("scene-071:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("072", ("scene-072", 0.00), ("scene-072:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("073", ("scene-073", 0.00), ("scene-073:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("074", ("scene-074", 0.00), ("scene-074:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("075", ("scene-075", 0.00), ("scene-075:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.08),
    fl3("076", ("scene-076", 0.00), ("scene-076:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("077", ("scene-077", 0.00), ("scene-077:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("078", ("scene-078", 0.00), ("scene-078:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("079", ("scene-079", 0.00), ("scene-079:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("083", ("scene-083", 0.12), ("scene-083:fin", 0.00), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("086", ("scene-086", 0.00), ("scene-086:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("087", ("scene-087", 0.00), ("scene-087:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.22),
    fl3("088", ("scene-088", 0.00), ("scene-088:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("089", ("scene-089", 0.00), ("scene-089:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("096", ("scene-096", 0.00), ("scene-096:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("103", ("scene-103", 0.00), ("scene-103:fin", 0.00), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.08),
    fl3("105", ("scene-105", 0.00), ("scene-105:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("106", ("scene-106", 0.00), ("scene-106:fin", 0.00), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.22),
    fl3("109", ("scene-109", 0.00), ("scene-109:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("110", ("scene-110", 0.00), ("scene-110:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("113", ("scene-113", 0.00), ("scene-113:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("114", ("scene-114", 0.00), ("scene-114:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("115", ("scene-115", 0.00), ("scene-115:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("116", ("scene-116", 0.00), ("scene-116:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.22),
    fl3("117", ("scene-117", 0.00), ("scene-117:fin", 0.00), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("127", ("scene-127", 4.37), ("scene-127:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("128", ("scene-128", 0.00), ("scene-128:fin", -1.54), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("137", ("scene-137", 0.00), ("scene-137:fin", 0.00), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("148", ("scene-148", 0.00), ("scene-148:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.08),
    fl3("149", ("scene-149", 0.00), ("scene-149:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("150", ("scene-150", 0.00), ("scene-150:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("151", ("scene-151", 0.00), ("scene-151:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("158", ("scene-158", 5.20), ("scene-158:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("163", ("scene-163", 0.00), ("scene-163:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("164", ("scene-164", 0.00), ("scene-164:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("165", ("scene-165", 0.00), ("scene-165:fin", 0.00), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("172", ("scene-172", 0.00), ("scene-172:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("173", ("scene-173", 0.00), ("scene-173:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("174", ("scene-174", 0.00), ("scene-174:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("177", ("scene-177", 0.00), ("scene-177:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("178", ("scene-178", 0.00), ("scene-178:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("179", ("scene-179", 0.00), ("scene-179:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("180", ("scene-180", 0.00), ("scene-180:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("181", ("scene-181", 0.00), ("scene-181:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("182", ("scene-182", 0.00), ("scene-182:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("183", ("scene-183", 0.00), ("scene-183:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.22),
    fl3("184", ("scene-184", 0.00), ("scene-184:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("185", ("scene-185", 0.00), ("scene-185:fin", 0.00), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.22),
    fl3("190", ("scene-190", 0.00), ("scene-190:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("191", ("scene-191", 0.00), ("scene-191:fin", -4.28), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("195", ("scene-195", 0.00), ("scene-195:fin", 0.50), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("196", ("scene-196", 0.00), ("scene-196:fin", 0.50), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.08),
    fl3("197", ("scene-197", 0.00), ("scene-197:fin", 0.50), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.08),
    fl3("198", ("scene-198", 0.00), ("scene-198:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("199", ("scene-199", 0.00), ("scene-199:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("200", ("scene-200", 0.00), ("scene-200:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("201", ("scene-201", 0.00), ("scene-201:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.22),
    fl3("206", ("scene-206", 0.00), ("scene-206:fin", 0.00), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.08),
    fl3("213", ("scene-213", 0.00), ("scene-213:fin", 0.00), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.08),
    fl3("218", ("scene-218", 0.00), ("scene-218:fin", 0.00), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.08),
    fl3("226", ("scene-226", 0.00), ("scene-226:fin", 0.50), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("227", ("scene-227", 0.00), ("scene-227:fin", 0.50), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.08),
    fl3("228", ("scene-228", 0.00), ("scene-228:fin", 0.00), zoom=(1.04, 1.12), pan=(-0.6, 0, 0.6, 0), oscuro=0.08),
    fl3("232", ("scene-232", 0.00), ("scene-232:fin", 0.00), zoom=(1.06, 1.14), pan=(0.5, 0.3, -0.5, -0.3), oscuro=0.08),
    fl3("236", ("scene-236", 0.00), ("scene-236:fin", 0.00), zoom=(1.12, 1.03), pan=(0, -0.5, 0, 0.5), oscuro=0.22),
    fl3("239", ("scene-238", 0.00), ("scene-239:fin", 0.50), zoom=(1.03, 1.12), pan=(0.6, 0, -0.6, 0), oscuro=0.22),
    fl3("240", ("scene-240", 0.00), ("scene-240:fin", 0.00), zoom=(1.0, 1.1), pan=(0, 0, 0, 0), oscuro=0.22),
    fl3("242", ("scene-242", 0.00), ("scene-242:fin", 0.00), zoom=(1.1, 1.0), pan=(0, 0, 0, 0), oscuro=0.22),
]

# ---- PLACA del personaje en cada frase de una voz de personaje (sale de guion.NARRA)
import re as _re  # noqa: E402
import guion as _G  # noqa: E402

_LEMA = {"Potema": "La Reina Loba", "Maestro del ritual": "Nigromante · Cráneo de Lobo", "Styrr": "Sacerdote de Arkay · Soledad",
         "Uriel II": "Emperador · su abuelo", "Pelagio II": "Emperador · su padre", "Antíoco": "Emperador · su medio hermano",
         "Kintyra II": "Emperatriz · su sobrina", "Duque Mentin": "Duque de La Cañada", "Uriel III": "Su hijo",
         "Mensajera": "Jinete redguard", "Pelagio III": "El Loco", "Falk Barba de Fuego": "Administrador de Soledad",
         "Sheogorath": "Príncipe de la Locura"}
PLACAS = []
_nw = lambda t: [w for w in (_re.sub(r"[\W_]+", "", x.lower()) for x in _re.sub(r"\[[^\]]*\]\s*", "", t).split()) if w]
_antes = []                                    # palabras de la voz ANTES de esta frase: el ancla lleva #N si ya se dijo
for _e in _G.ESCENAS:
    for _i, _tx in enumerate(_e["frases"]):
        _tx = _tx[1] if isinstance(_tx, (tuple, list)) else _tx
        _v = _G.NARRA.get(f"{_e['id']}_{_i}", "el Profeta")
        if _v != "el Profeta":
            _limpio = _re.sub(r"\[[^\]]*\]\s*", "", _tx)
            _ancla = " ".join(_limpio.split()[:5]).rstrip(",.:;¡!¿?")
            _ag = _nw(_ancla)
            _n = sum(1 for _k in range(len(_antes) - len(_ag) + 1) if _antes[_k:_k + len(_ag)] == _ag)
            PLACAS.append(narra(_ancla + (f"#{_n + 1}" if _n else ""), _v, _LEMA.get(_v, ""), dur=3.4))
            PLACAS[-1]["_pal"] = len(_antes)           # posición (en palabras de la voz) donde arranca la placa
        _antes += _nw(_tx)

# v3 (13-nov): placa que cae DENTRO de una red de relaciones → arriba a la derecha (x=.84, y=.09), donde la red solo tiene humo.
# Rango de cada red por sus anclas de/a (sin el desfase en segundos); las demás placas no se tocan.
_REDES_RANGO = [("Del otro lado, su abuelo", "Corre al Salón de los Registros"), ("Cuando el paje llega", "Sesenta y dos años"),
                ("Potema ya se había encargado", "Ese mismo día, Bathorgh"), ("Potema la usa esa misma noche", "A la mañana siguiente"),
                ("Antes pedían cincuenta", "Tres meses después, frente a Artaeum"), ("Cuando le preguntan al duque", "Kintyra muere en su celda"),
                ("Céforo es proclamado emperador", "Antes de lo que viene"), ("Tres años después, en el ciento cuarenta", "Y un último correo")]


def _pal_de(txt):
    ag = _nw(txt)
    return next((k for k in range(len(_antes) - len(ag) + 1) if _antes[k:k + len(ag)] == ag), None)


_RANGOS = [(_pal_de(a), _pal_de(b)) for a, b in _REDES_RANGO]
assert all(a is not None and b is not None and a < b for a, b in _RANGOS), f"ancla de red no encontrada: {_RANGOS}"
for _p in PLACAS:
    _w = _p.pop("_pal")
    if any(a <= _w < b for a, b in _RANGOS):
        _p.update(x=.84, y=.09)
FX = FX + PLACAS

import json as _json  # noqa: E402

_AJ = os.path.join(_AQUI, "_ajustes.json")
if os.path.exists(_AJ) and not os.environ.get("FAB_SIN_AJUSTES"):
    for _k, _v in sorted(_json.load(open(_AJ, encoding="utf-8")).items(), key=lambda kv: -int(kv[0])):
        _d = FX[int(_k)]
        if _v.get("quitar"):
            FX.pop(int(_k))
            continue
        if "retraso" in _v:
            _e = _d["en"]
            _d["en"] = (_e[0], _e[1] + _v["retraso"]) if isinstance(_e, tuple) else (_e, _v["retraso"])
        if "dur" in _v:
            _d["dur"] = _v["dur"]

# v3: las escenas de Flow v3 van DESPUÉS de los ajustes (_ajustes.json va por índice de FX: no lo mueven)
FX += FLOW3
