# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 15 cosas de Skyrim que PIERDES para siempre» (SECUENCIA YT, Crónicas de Tamriel, 26-nov-2026).
REGLA DE ORO (tes_secretos_40) + kits del 5-nov: pegatinas `pv()`, peg_estilos (reliquia, camafeo, abanico), presentaciones
(carrusel, podio), mapas con ruta y `entrada=` (coordenadas UESP de `_coords.txt`) y MG NUEVOS de este video, repartidos desde
el puesto 15: `mg_tes.perdido` (ficha LO QUE PIERDES con candado y sello) y `mg_tes.bifurcacion` (el camino que eliges y el
que pierdes). Cada puesto: aviso → pegatinas en su segundo → mapa → perdido/bifurcacion → «Cómo no caer» → remate.
    python fab.py tes_pierdes_siempre fx --seco      FAB_FX_FINAL=1 python fab.py tes_pierdes_siempre fx hoja
"""
import os

import mg_tes as T
import peg_estilos as PE

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


# ---------------------------------------------------------------- helpers (de tes_builds_rotas)
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


def podi(tres, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.podio(_f(tres), titulo, TEMA_PEG), de, a, marcas, "podio")


def ficha(en, nombre, efecto, origen=None, dur=4.5, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.24, y=.52, tam=460):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.70, tam=280, foco=(.5, .25, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def mis(en, arriba, titulo, dur=3.0, y=.30):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(P("com_" + cid), "", tam, giro=-3.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + cid, ver=1.0)


def aviso(en, n, titulo, dur=3.4):
    return dict(tipo="mg", fn=T.mision(f"Número {n} · lo que pierdes", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


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



def perd(slug, nombre, causa, de, a, marcas, evitar=None, titulo="Lo que pierdes para siempre", y=.50, x=.5,
         sello="PERDIDO PARA SIEMPRE"):
    return mg(T.perdido(titulo, P(slug) if slug else None, nombre, causa, evitar, sello=sello), de, a, marcas,
              "perdido " + nombre, y=y, x=x)


def bif(titulo, raiz, ramas, de, a, marcas, elige=0, remate=None, sello="PERDIDO", y=.50):
    r = [(P(s) if s else None, n, c) for s, n, c in ramas]
    return mg(T.bifurcacion(titulo, raiz, r, elige=elige, sello=sello, remate=remate), de, a, marcas, "bifurcacion " + titulo, y=y)


def evita(en, texto, dur=3.4):
    return dict(tipo="mg", fn=T.mision("Cómo no caer", texto), en=en, dur=dur, y=.27, sale=.4, nombre="evita " + texto, ver=1.4)


# ---------------------------------------------------------------- coordenadas UESP (mapas/skyrim.jpg, `_coords.txt`, error 0,035)
RIFTEN, BRILLO, SOLEDAD, EMBAJADA = (.887, .783), (.848, .786), (.342, .202), (.310, .182)
RIVERWOOD, HROTHGAR, MARKARTH, VIGILANTES = (.547, .633), (.613, .609), (.108, .488), (.534, .310)
LUCERO, CARRERA, HIBERNALIA, KORVANJUND = (.555, .198), (.539, .525), (.729, .208), (.615, .404)
VENTALIA, MORTHAL, VOLKIHAR, DAYSPRING = (.792, .402), (.404, .311), (.090, .078), (.948, .816)
FORELHOST, HIGHGATE, GREENWALL, SUNGARD = (.913, .832), (.444, .198), (.873, .714), (.335, .574)

# ---------------------------------------------------------------- comentarios (≤ 10 días, ninguno usado antes; R46 + ESTADO.md)
C_ELIANA, C_ADONS, C_ANTONI = "UgxiUxXalsXu7NBW86B4AaABAg", "Ugzk8Yr1Y7-p73nUebh4AaABAg", "UgxiOg5U5cnxk-JxOHh4AaABAg"
C_SRU, C_JOSUE, C_CREEPY = "UgzIppZfraiT1jiw1hx4AaABAg", "UgyMB91Mnv42-28388l4AaABAg", "Ugz9V-VpeV37wvR6PKB4AaABAg"
C_SEBAS, C_ACHE = "Ugykg7e1zig4FDhL1K94AaABAg", "UgwImAHK41EHbsC-Ie54AaABAg"

FX = [
    # ================= GANCHO: un elemento nuevo cada 2-3 s
    zoom(0.0, "Hoy, las quince cosas", 1.12),
    pv("Un bastón que vale mil", "nahkriin", "Nahkriin · su bastón", dur=3.0, x=.80, y=.58, tam=380, entrada="tinta"),
    ficha("Y lo usas una sola vez", "Bastón de Nahkriin", "Valor *1431* · un solo uso: *de llave*", "Skuldafn", dur=3.4),
    aba([("isran", "Isran"), ("trol_acorazado", "Trol acorazado")], "Un fuerte entero", ("Y lo pierdes por decirle", .4),
        ["Un fuerte entero", "un trol con armadura"], "fuerte entero", x=.26),
    pv("Y lo pierdes por decirle que sí", "harkon", "Harkon", dur=2.6, x=.80, y=.58, tam=340, marco="aura"),
    pv("Y una tormenta de rayos", "invocar_tormenta", "Invocar tormenta", dur=3.0, x=.20, y=.60, tam=340, entrada="cristal"),
    mis("Hoy, las quince cosas", "Crónicas de Tamriel", "Las 15 cosas que PIERDES para siempre", dur=3.2, y=.30),
    carr([("brillo_dorado", "Encargos"), ("serana", "Personas"), ("corona_dentada", "Objetos"), ("skuldafn", "Lugares")],
         "Sin consola, sin trucos", ("y cómo no caer", .6), ["Sin consola", "Dónde están", "cómo se pierden", "y cómo no caer"],
         titulo="Lo que se pierde"),
    pv("el único lugar de Skyrim que te roba", "skuldafn", "¿Qué lugar?", dur=3.4, x=.76, y=.56, tam=420, marco="polaroid"),

    # ================= 15 · COLMENAS DE BRILLO DORADO
    aviso("Número quince", 15, "Las colmenas de Brillo Dorado"),
    pv("Brynjolf te manda", "brynjolf", "Brynjolf", dur=3.2, x=.18, y=.60, tam=380, marco="carta"),
    mapa("skyrim.jpg", "La Grieta", [pt(RIFTEN, "Riften", "inicio", "brynjolf"), pt(BRILLO, "Hacienda Brillo Dorado", "meta", "brillo_dorado")],
         "a la Hacienda Brillo Dorado", ("la mujer que manda en Riften", .6), ["a la Hacienda Brillo Dorado", "La hacienda le da miel"],
         "Brillo Dorado", entrada="foco"),
    cam("Maven Black-Briar", "maven", "Maven Black-Briar", dur=3.0, x=.16, y=.72),
    mg(T.contadores("La orden de Brynjolf", [("Colmenas que hay que quemar", 3, None, 0), ("Caja fuerte", 1, 0, 1)],
                    remate=("NI UNA COLMENA MÁS", 2)),
       "La orden: quemar tres colmenas", ("Y aquí cae media humanidad", .3), ["quemar tres colmenas", "abrir la caja fuerte", "y volver"],
       "orden brillo", y=.36, x=.70),
    perd("brynjolf", "Tu parte del botín", "Quemar más de tres colmenas", "Si quemas más de tres", ("Y el fuego se contagia", .2),
         ["Si quemas más de tres", "te olvides de tu parte", "Cero monedas"]),
    pv("Y el fuego se contagia", "colmena", "Colmena", dur=3.4, x=.20, y=.60, tam=340, entrada="ceniza"),
    ficha("Si obedeces, la paga", "La paga de Brynjolf", "Oro que *crece con tu nivel* · o *cero*", "Alto y claro", dur=3.8),
    evita("Cómo no caer: nada de hechizos", "Una colmena, otra, otra… y te vas"),
    mis("el juego te pide moderación", "Brillo Dorado", "Moderación con el fuego", dur=3.0, y=.30),

    # ================= CRÍTICA 1 · @elianalera1925
    com("Y esto va para Eliana", C_ELIANA, dur=6.0, x=.32, y=.34, tam=780),
    mis("la diversión te la cobran", "En Skyrim", "La diversión se cobra", dur=3.2, y=.72),

    # ================= 14 · EMBAJADA DE THALMOR
    aviso("Número catorce", 14, "La Embajada de Thalmor"),
    pv("te cuelas en la fiesta de Elenwen", "elenwen", "Elenwen", dur=3.4, x=.80, y=.58, tam=380, marco="aura"),
    mapa("skyrim.jpg", "Haafingar", [pt(SOLEDAD, "Soledad", "inicio"), pt(EMBAJADA, "Embajada de Thalmor", "meta", "embajada")],
         "al noroeste de Soledad", ("a escondidas", .4), ["al noroeste de Soledad", "Un elfo del servicio"], "Embajada de Thalmor",
         ventana=True, ancho=880, x=.70, y=.45),
    cam("Malborn, te mete el equipo", "malborn", "Malborn", dur=3.0, x=.16, y=.72),
    perd("embajada", "El edificio de la embajada", "Solo se entra una vez: después, ni por la puerta", "Es la única vez que entras",
         ("Así que lo que no saqueaste", .5), ["Es la única vez que entras", "Si vuelves después", "El edificio, no"],
         evitar="sáquealo todo en la fiesta"),
    ficha("Hay trucos para volver a entrar", "Trucos", "Caballo · árbol · *un plato bien colocado*", "Escalar paredes, no jugar", dur=4.2),
    rel("El solar de Elenwen", "embajada", "Solar de Elenwen", "Esa noche, o nunca", dur=3.6, x=.24, y=.52, tam=440),
    pv("Se juega la vida por ti", "malborn", "Malborn", dur=3.6, x=.20, y=.60, tam=380, entrada="vuela"),
    ficha("sale corriendo hacia el este", "Malborn", "Huye al este y *desaparece* del juego", "Tu cómplice", dur=3.8, rojo=True),

    # ================= 13 · SVEN O FAENDAL
    aviso("Número trece", 13, "Sven, o Faendal"),
    mapa("skyrim.jpg", "Cauce Boscoso", [pt(RIVERWOOD, "Cauce Boscoso", "meta", "camilla")], "En Cauce Boscoso hay",
         ("Y Faendal, el elfo arquero", .4), ["En Cauce Boscoso"], "Cauce Boscoso", ventana=True, ancho=760, x=.74, y=.42),
    pv("Camilla, y dos pretendientes", "camilla", "Camilla Valerius", dur=2.8, x=.20, y=.60, tam=340, marco="polaroid"),
    aba([("sven", "Sven"), ("faendal", "Faendal")], "Sven, el bardo", ("una carta de amor falsa", .4), ["Sven, el bardo", "Y Faendal"],
        "sven y faendal", x=.28),
    bif("Cauce Boscoso · solo uno", "¿A quién traicionas?", [("faendal", "Faendal", ["Te aprecia", "Seguidor arquero"]),
                                                            ("sven", "Sven", ["Te odia", "Nunca será tu seguidor"])],
        "Hagas lo que hagas", ("Y no son iguales", .1), ["Hagas lo que hagas", "El traicionado te odia"],
        remate=("Amigo de los dos: imposible", 2)),
    ficha("Faendal, además, entrena Arquería", "Faendal", "Entrena *Arquería*", "Para un arquero que empieza", dur=3.8),
    evita("Cómo no caer: decide antes", "Decide antes de tocar la carta"),
    mis("por veinticinco monedas", "Cauce Boscoso", "Una cita arruinada · 25 de oro", dur=3.2, y=.30),

    # ================= 12 · THIRSK
    aviso("Número doce", 12, "El salón de Thirsk"),
    pv("El salón de Thirsk, en Solstheim", "thirsk", "Salón de Thirsk", dur=3.4, x=.78, y=.56, tam=420, marco="museo"),
    bif("Thirsk · solo una", "¿A quién ayudas?", [("thirsk", "Los nórdicos", ["Maestro de Armadura pesada", "La forja del salón"]),
                                                  ("riekling", "Los rieklings", ["Un riekling de seguidor"])],
        "Dos misiones en el mismo salón", ("Hay una salida a medias", .1),
        ["Dos misiones en el mismo salón", "completar una hace fallar"], remate=("Completar una hace fallar la otra", 2)),
    ficha("Hay una salida a medias", "Salida a medias", "*2* encargos del jefe riekling · y cambias de bando", "Antes del tercero", dur=4.4),
    pv("o un duende azul con lanza", "riekling", "Riekling", dur=3.0, x=.80, y=.60, tam=340, entrada="vuela"),

    # ================= AGRADECIMIENTOS (5)
    mis("gracias a los que comentan", "Comentarios", "Los leo todos", dur=3.0, y=.30),
    com("Un veterano, SrUnknown", C_SRU, dur=5.2, x=.30, y=.32, tam=720),
    com("Y Josué Alejandro", C_JOSUE, dur=4.6, x=.70, y=.62, tam=680),
    com("que se llama Creepy Noodles", C_CREEPY, dur=3.4, x=.30, y=.34, tam=680),
    com("Sebastián Merino nos pone", C_SEBAS, dur=3.4, x=.70, y=.36, tam=680),
    com("Y achezeta se acaba", C_ACHE, dur=3.0, x=.32, y=.66, tam=640),
    mis("esto es capacitación", "Para tu jefe", "Esto es capacitación", dur=3.0, y=.30),

    # ================= 11 · LA PAZ DE ALTO HROTHGAR
    aviso("Número once", 11, "La paz de Alto Hrothgar"),
    mapa("skyrim.jpg", "Alto Hrothgar", [pt(HROTHGAR, "Alto Hrothgar", "meta", "alto_hrothgar")], "sientas a imperiales",
         ("para firmar una tregua", .5), ["sientas a imperiales"], "Alto Hrothgar", ventana=True, ancho=760, x=.74, y=.42),
    aba([("tullius", "Tullius"), ("ulfric", "Ulfric")], "en la misma mesa", ("para firmar una tregua", .4), ["en la misma mesa", "una tregua"],
        "la mesa", x=.28),
    ficha("un logro, el de conquistar un fuerte", "Logro de la guerra civil", "Tomar un fuerte: puede quedar *imposible*",
          "Según el reparto de comarcas", dur=4.2, rojo=True),
    mapa("skyrim.jpg", "El logro", [pt(SUNGARD, "Fuerte Sungard · capas", "inicio"), pt(GREENWALL, "Fuerte Greenwall · Imperio", "inicio"),
                                    pt(HROTHGAR, "Alto Hrothgar", "meta", "alto_hrothgar")],
         "El logro pide tomar", ("Y si la Cuenca", .1), ["el Fuerte Sungard", "o el Fuerte Greenwall"], "Fuertes", entrada="mesa"),
    perd("ondolemar", "Ondolemar", "Muere si la Cuenca pasa a los capas de la tormenta", "muere Ondolemar", ("La recompensa de la tregua", .2),
         ["Y si la Cuenca", "muere Ondolemar", "Aunque sea por la tregua"], titulo="Lo que pierdes en la mesa"),
    evita("toma el fuerte de tu bando", "Toma el fuerte antes de la reunión"),
    mis("Diplomacia nórdica", "Alto Hrothgar", "Diplomacia nórdica", dur=3.0, y=.30),

    # ================= 10 · SALÓN DE LOS VIGILANTES
    aviso("Número diez", 10, "El Salón de los Vigilantes"),
    pv("Es el refugio de los Vigilantes", "salon_vigilantes", "Salón de los Vigilantes", dur=4.0, x=.22, y=.56, tam=420, marco="carta"),
    pv("Ahí está Custodia Carcette", "carcette", "Custodia Carcette", dur=3.6, x=.80, y=.58, tam=380, marco="carta"),
    mg(T.contadores("Fecha de caducidad", [("Tu nivel", 10, None, 0)], remate=("NIVEL 10: TODOS MUEREN", 1)),
       "Pero tiene fecha de caducidad", ("El salón queda en ruinas", 0.0), ["cuando llegas a nivel diez", "los vampiros lo arrasan"],
       "caducidad", y=.36, x=.70),
    perd("carcette", "Custodia Carcette", "Nivel 10 o empezar Dawnguard: los vampiros arrasan el salón", "El salón queda en ruinas",
         ("Ojo: sin Dawnguard", .1), ["El salón queda en ruinas", "no hay forma de salvarlos", "Y con ellos se va todo"]),
    ficha("sin Dawnguard instalado", "Sin Dawnguard", "El salón sigue *en pie* para siempre", "El problema es el DLC", dur=3.8),
    mapa("skyrim.jpg", "El Pálido", [pt(CARRERA, "Carrera Blanca", "inicio"), pt(VIGILANTES, "Salón de los Vigilantes", "meta", "salon_vigilantes"),
                                     pt(LUCERO, "Lucero del Alba", "inicio")],
         "Está en el camino entre Lucero", ("antes del nivel diez", .6), ["Está en el camino", "Si quieres su entrenamiento"],
         "Salón de los Vigilantes", entrada="pliegue"),
    mis("Como un yogur", "Caducidad", "Como un yogur", dur=2.8, y=.30),

    # ================= 9 · LOS ENCARGOS DE LOS JARLS
    aviso("Número nueve", 9, "Los encargos de los jarls"),
    ficha("cada comarca que conquistas", "Guerra civil", "Jarl derrocado = sus encargos *desaparecen*", "Cada comarca", dur=4.0, rojo=True),
    mapa("skyrim.jpg", "Comarcas", [pt(MARKARTH, "Markarth", "peligro", "igmund"), pt(HIBERNALIA, "Hibernalia", "peligro", "korir"),
                                    pt(LUCERO, "Lucero del Alba", "peligro", "skald")],
         "Igmund en Markarth", ("esas misiones desaparecen", .5), ["Igmund en Markarth", "Korir en Hibernalia", "Skald en Lucero"],
         "Jarls desterrados", ventana=True, ancho=900, x=.70, y=.45),
    aba([("igmund", "Igmund"), ("korir", "Korir"), ("skald", "Skald")], "si los destierran antes", ("esas misiones desaparecen", .5),
        ["si los destierran", "esas misiones desaparecen"], "jarls", x=.28),
    ficha("Dengeir y Brunwulf", "El que sube", "Dengeir y Brunwulf: *sin encargos*", "Jarls nuevos", dur=3.8),
    mapa("skyrim.jpg", "Morthal", [pt(MORTHAL, "Morthal · Gorm e Idgrod la Joven", "peligro")], "Y con cada jarl se va su corte",
         ("dejan de darte trabajo", .4), ["En Morthal"], "Morthal", ventana=True, ancho=700, x=.74, y=.40),
    bif("Mueren en las batallas", "Sí o sí", [("severo", "Severio Pelagia", ["Batalla de Carrera Blanca"]),
                                             ("aldis", "Capitán Aldis", ["Batalla de Soledad"])],
        "Y hay dos que mueren", ("La regla es simple", .1), ["Y hay dos que mueren", "y el capitán Aldis"], elige=-1, sello="MUERE"),
    evita("La regla es simple", "Antes de cada batalla, los encargos de ese jarl"),
    mis("tu trabajo de recadero", "Skyrim liberado", "Recadero en paro", dur=3.0, y=.30),

    # ================= CRÍTICA 2 · @AdonsAdndna
    com("Adons me dejó un comentario", C_ADONS, dur=6.0, x=.32, y=.34, tam=760),
    mg(T.contadores("Cosas para llorar", [("En este video", 15, None, 0)], remate=("ESPERA AL NÚMERO TRES", 1)),
       "quince cosas para llorar", ("y luego hablamos", .6), ["quince cosas para llorar", "Espera a ver el número tres"], "llorar", y=.66, x=.70),

    # ================= 8 · LA FORJA DE STALHRIM
    aviso("Número ocho", 8, "La forja de stalhrim"),
    pv("El stalhrim es el hielo encantado", "stalhrim", "Stalhrim", dur=3.4, x=.20, y=.60, tam=360, entrada="cristal"),
    rel("Para forjarlo tú mismo", "armadura_stalhrim", "Armadura de stalhrim", "Herrería de ébano + una misión", dur=4.0, x=.76, y=.52),
    aba([("deor", "Deor"), ("fanari", "Fanari")], "Deor Tallador y Fanari", ("Si cualquiera de los dos muere", 0.0),
        ["Deor Tallador", "Fanari Voz Fuerte"], "deor y fanari", x=.28),
    perd("deor", "Forjar stalhrim", "Si Deor o Fanari mueren antes de terminar la misión", "Si cualquiera de los dos muere",
         ("Y están protegidos", .1), ["Si cualquiera de los dos muere", "nunca aprenderás a forjar", "nunca aprenderás a forjar"]),
    ficha("tus seguidores también cuentan", "Protegidos", "Solo mueren por *ti*… o por *tus seguidores*", "Aldea Skaal", dur=4.0, rojo=True),
    evita("Cómo no caer: haz la misión pronto", "Nada de gritos de área en la aldea"),
    ficha("Las piezas se siguen vendiendo", "Stalhrim", "Comprarlo: *sí* · forjarlo tú: *nunca*", "Solstheim", dur=3.8),
    mis("un Fus Ro Dah con mala puntería", "Aldea Skaal", "Fus Ro Dah con mala puntería", dur=3.2, y=.30),

    # ================= 7 · LA CORONA DENTADA
    aviso("Número siete", 7, "La Corona dentada"),
    mapa("skyrim.jpg", "El Pálido", [pt(KORVANJUND, "Korvanjund", "meta", "korvanjund")], "Está en Korvanjund",
         ("al fondo de la ruina", .4), ["Está en Korvanjund"], "Korvanjund", ventana=True, ancho=760, x=.74, y=.42),
    ficha("Un casco pesado de veintitrés", "Corona dentada", "*23* de armadura · valor *5000*", "Casco pesado", dur=4.2),
    ficha("tiene un muro de palabras", "Korvanjund", "También tiene un *muro de palabras*", "Ya que vas", dur=3.6, x=.26),
    rel("va en el hueco del pelo", "corona_dentada", "Corona dentada", "Va en el hueco del pelo", dur=4.0),
    aba([("corona_dentada", "Corona"), ("mascara_nahkriin", "Máscara")], "se lleva a la vez", ("o una diadema", .4),
        ["se lleva a la vez", "una máscara de sacerdote dragón"], "corona y mascara", x=.30),
    bif("La Corona se entrega", "¿A quién se la das?", [("tullius", "Tullius", ["Ni siquiera hay recompensa", "«Buen trabajo, soldado»"]),
                                                        ("ulfric", "Ulfric", ["Se la queda él"])],
        "tienes que entregarla", ("Lo bueno: esa misión", .1), ["tienes que entregarla", "Si vas con el Imperio"], elige=-1, sello="SE LA QUEDAN"),
    ficha("se puede posponer", "La misión", "Posponerla: *sin consecuencias*", "Úsala mientras tanto", dur=3.6),
    mis("cambiado por una palmadita", "Guerra civil", "Una palmadita en la espalda", dur=3.0, y=.30),

    # ================= 6 · SERANA, COMO VAMPIRA
    aviso("Número seis", 6, "Serana, como vampira"),
    pv("Número seis. Serana", "serana", "Serana", dur=3.2, x=.80, y=.58, tam=400, marco="carta"),
    pv("Falion, el mago de Morthal", "falion", "Falion · Morthal", dur=3.4, x=.20, y=.60, tam=360, marco="carta"),
    bif("Serana", "¿La curas?", [("serana", "Vampira", ["Flechas malditas de sangre", "Te hace Señor vampiro"]),
                                 ("serana", "Humana", ["Ojos de otro color", "Sin flechas ni Señor vampiro"])],
        "Pero curada, ya no puede", ("Y la cura solo es posible", .1), ["Pero curada", "Ni convertirte a ti"], elige=1, sello="SE PIERDE"),
    aba([("arco_auriel", "Arco de Auriel"), ("flechas_malditas", "Flechas malditas")], "flechas malditas de sangre",
        ("las del Arco de Auriel", .6), ["flechas malditas", "las del Arco de Auriel"], "arco y flechas", x=.88, y=.75, tam=180),
    perd("serana", "La cura de Serana", "Preguntarle a destiempo si siempre ha sido vampira", "una pregunta a destiempo",
         ("Cómo no caer: decide qué", .1), ["una pregunta a destiempo", "ella lo llama un don", "La cura queda bloqueada"],
         sello="BLOQUEADA PARA SIEMPRE"),
    evita("Cómo no caer: decide qué quieres", "Guarda flechas malditas antes de curarla"),
    mis("adiós al final más bonito", "Dawnguard", "Adiós al mejor final", dur=3.0, y=.30),

    # ================= CRÍTICA 3 · @antonigirii
    com("Y antonigirii me escribió", C_ANTONI, dur=6.0, x=.32, y=.34, tam=760),
    pv("tanta gente que quemó cinco colmenas", "colmena", "Cinco colmenas", dur=3.2, x=.76, y=.58, tam=340, entrada="sello"),

    # ================= 5 · ARMADURA DE MAESTRE DEL GREMIO
    aviso("Número cinco", 5, "La armadura de maestre del gremio"),
    pv("Erikur es un thane", "erikur", "Erikur · thane de Soledad", dur=3.6, x=.20, y=.60, tam=380, marco="carta"),
    ficha("El Sload delicado", "El Sload delicado", "Encargo especial del *Gremio de Ladrones*", "Objetivo: Erikur", dur=4.0),
    cam("Delvin Mallory te lo encarga", "delvin", "Delvin Mallory", dur=3.0, x=.16, y=.72),
    perd("erikur", "Ser maestre del gremio", "Erikur muere antes de El Sload delicado", "Y si muere antes",
         ("adiós a la armadura de maestre", 0.0), ["Y si muere antes", "el gremio se atasca", "el gremio se atasca"]),
    carr([("maestre", "Armadura de maestre"), ("amuleto_articulacion", "Amuleto de Articulación")], "adiós a la armadura de maestre",
         ("Y de propina", 1.0), ["adiós a la armadura", "y al Amuleto"], titulo="Lo que se va con Erikur"),
    evita("Cómo no caer: haz El Sload", "El Sload delicado, antes de la Hermandad"),
    mis("nunca serás el jefe", "Gremio de Ladrones", "Nunca serás el jefe", dur=3.0, y=.30),

    # ================= 4 · SER HOMBRE LOBO
    aviso("Número cuatro", 4, "Ser hombre lobo"),
    rel("La forma bestial", "hombre_lobo", "Forma bestial", "Una vez al día · 150 s", dur=4.0),
    ficha("una vez al día, ciento cincuenta", "Forma bestial", "*1* vez al día · *150* segundos", "Licantropía", dur=3.8),
    pv("Aela puede devolverte", "aela", "Aela la Cazadora", dur=3.6, x=.77, y=.58, tam=370, marco="aura"),
    mg(T.contadores("Las segundas oportunidades de Aela", [("Veces que te devuelve la licantropía", 1, None, 0)],
                    remate=("LA SEGUNDA CURA ES PARA SIEMPRE", 1)),
       "Pero una sola vez", ("Y ojo: hacerte Señor vampiro", .1), ["Pero una sola vez", "Si te curas otra vez"], "aela una vez", y=.36, x=.70),
    pv("hacerte Señor vampiro también cuenta", "harkon", "Señor vampiro = cura", dur=3.4, x=.20, y=.60, tam=360, marco="carta"),
    perd("totems", "Los Tótems de Hircine", "Curarte por segunda vez", "Y curado, no terminas", ("Aela perdona una vez", .2),
         ["Y curado", "ni la misión de los cazadores", "Cómo no caer"], evitar="termina los Tótems antes"),

    # ================= CAMPAÑA DE SUSCRIPCIÓN (13 de cada 100)
    mg(T.rejilla("De cada cien que ven el canal", n=100, encendidas=13, remate=("Solo 13 suscritos", 1)),
       "De cada cien personas", ("están suscritas", .6), ["De cada cien personas", "solo trece están suscritas"], "rejilla suscritos", y=.44),
    mg(T.contadores("Camino de diez mil", [("Suscriptores", 7100, None, 0), ("La meta", 10000, 0, 1)], remate=("SUSCRIBIRTE ES GRATIS", 2)),
       "Somos siete mil cien", ("Y eso no lo pierdes nunca", .8), ["Somos siete mil cien", "camino de diez mil", "suscribirte es gratis"],
       "meta suscriptores", y=.40, x=.68),

    # ================= 3 · LA GUARDIA DEL ALBA ENTERA
    aviso("Número tres", 3, "La Guardia del Alba entera"),
    pv("Harkon te ofrece su don", "harkon", "Harkon", dur=3.4, x=.77, y=.58, tam=370, marco="aura"),
    bif("Dawnguard", "¿Aceptas el don de Harkon?", [("isran", "Guardia del Alba", ["Tecnología antigua", "4 maestros", "Perros y trols"]),
                                                    ("harkon", "Vampiros Volkihar", ["Cáliz de sangre", "Perros de la muerte"])],
        "Si dices que sí, eliges", ("Pierdes la Tecnología antigua", .1), ["Si dices que sí", "pasa a ser tu enemiga"], elige=1),
    rel("Pierdes la Tecnología antigua", "ballesta_enana", "Tecnología antigua", "Ballesta enana · virotes explosivos", dur=4.2),
    aba([("sorine", "Sorine"), ("isran", "Isran"), ("florentius", "Florentius"),
         ("gunmar", "Gunmar")], "Pierdes cuatro entrenadores", ("Y pierdes seguidores", .1),
        ["Sorine, de Arquería", "Isran, de Armadura", "Florentius, de Restauración", "Y Gunmar"], "cuatro maestros", x=.40, tam=280),
    pv("y los trols con armadura", "trol_acorazado", "Trol acorazado", dur=3.4, x=.78, y=.55, tam=300, marco="carta"),
    ficha("los cinco reclutas", "Seguidores de la Guardia", "Agmaer · Beleval · Celann · Durak · Ingjard", "Cinco menos", dur=4.2),
    mapa("skyrim.jpg", "Dos bandos", [pt(DAYSPRING, "Cañón de Dayspring · Fuerte Guardia del Alba", "inicio", "isran"),
                                      pt(VOLKIHAR, "Castillo Volkihar", "meta", "harkon")],
         "hasta acabas matando a Isran", ("A cambio, te dan", .2), ["hasta acabas matando a Isran"], "Guardia del Alba", entrada="desenrolla"),
    pv("A cambio, te dan el Cáliz", "caliz", "Cáliz de sangre", dur=3.2, x=.20, y=.60, tam=340, marco="museo"),
    evita("aquí no hay doble ruta", "Elige con esta lista en la mano"),
    mis("Por morderle el cuello", "Dawnguard", "Por morderle el cuello al vecino", dur=3.2, y=.30),

    # ================= 2 · LA TERCERA PALABRA DE INVOCAR TORMENTA
    aviso("Número dos", 2, "La tercera palabra de Invocar tormenta"),
    rel("Con las tres palabras", "invocar_tormenta", "Invocar tormenta", "El grito con más daño bruto", dur=4.0),
    mg(T.contadores("Invocar tormenta, palabra a palabra", [("1 palabra · segundos", 60, None, 0), ("2 palabras · segundos", 120, 0, 1),
                                                           ("3 palabras · segundos", 180, 1, 2)], remate=("RAYOS: 40 → 60 → 80", 2)),
       "Con una sola palabra", ("Y es el grito con el enfriamiento", .1), ["Con una sola palabra", "Con dos", "tormenta de tres minutos"],
       "palabras tormenta", y=.40, x=.68),
    ficha("enfriamiento más largo", "Invocar tormenta", "El enfriamiento *más largo* de todos los gritos", "Se lo ha ganado", dur=3.8),
    mapa("skyrim.jpg", "Las palabras", [pt(FORELHOST, "Forelhost", "inicio", "forelhost"), pt(HIGHGATE, "Ruinas del norte", "inicio")],
         "La primera palabra está en Forelhost", ("no se van a ningún lado", .3), ["en Forelhost", "la segunda en otras ruinas"],
         "Palabras 1 y 2", ventana=True, ancho=880, x=.70, y=.45),
    pv("a lomos de Odahviing", "odahviing", "Odahviing", dur=3.4, x=.75, y=.58, tam=380, entrada="vuela"),
    perd("skuldafn", "La 3.ª palabra de Invocar tormenta", "Su muro está en Skuldafn, y a Skuldafn no se vuelve",
         "Es el único grito con un muro", ("Y ojo: sus rayos", .1), ["Es el único grito", "en un lugar al que no puedes", "Cómo no caer"],
         evitar="barre el templo antes del portal"),
    ficha("sus rayos también les pegan", "Invocar tormenta", "Los rayos *también* golpean a tus aliados", "Fuego amigo", dur=3.6, rojo=True),
    mis("a dos palabras", "Invocar tormenta", "A dos palabras de la gloria", dur=3.0, y=.30),

    # ================= 1 · EL BASTÓN DE NAHKRIIN
    aviso("Número uno", 1, "El bastón de Nahkriin"),
    pv("derrotas al sacerdote dragón Nahkriin", "nahkriin", "Nahkriin", dur=3.6, x=.80, y=.58, tam=420, marco="aura"),
    ficha("Su bastón crea un muro de rayos", "Bastón de Nahkriin", "Muro de rayos: *50* por segundo · valor *1431*",
          "Sacerdote dragón", dur=4.6),
    perd("nahkriin", "El bastón de Nahkriin", "Se queda en el sello dragón al abrir el portal", "Pero es la llave",
         ("El truco: si llegas rápido", .1), ["Pero es la llave", "el bastón se queda ahí", "casi todos lo pierden"]),
    rel("se abre el portal a Sovngarde", "sovngarde", "Sovngarde", "El portal de Skuldafn", dur=3.6, x=.76, y=.52),
    ficha("El truco: si llegas rápido", "El truco", "Cruza el portal *ya abierto* sin usar el bastón", "Y te lo quedas", dur=4.2),
    evita("en cuanto se abra el portal", "No esperes a nadie. Corre."),
    mis("El único llavero de Skyrim", "Skuldafn", "Un llavero de 1431 de oro", dur=3.2, y=.30),

    # ================= GEMA: SKULDAFN TE ROBA TRES COSAS
    pv("el templo de Skuldafn, en lo alto", "skuldafn", "Templo de Skuldafn", dur=3.6, x=.76, y=.56, tam=460, marco="polaroid"),
    carr([("nahkriin", "El bastón"), ("invocar_tormenta", "La 3.ª palabra"), ("mascara_nahkriin", "La máscara")],
         "El bastón de Nahkriin. La última", ("nunca habrá Konahrik", .6), ["El bastón de Nahkriin", "La última palabra", "Y la máscara"],
         titulo="Skuldafn te roba tres cosas"),
    mg(T.votacion("Antes de subirte a Odahviing", ["Lee el muro", "Saquea a Nahkriin", "Quédate su bastón", "Corre al portal"],
                  remate="Y no pierdes nada"),
       "haz la lista", ("Y ya que estás", .2), ["lee el muro", "saquea a Nahkriin", "quédate su bastón", "y corre al portal", "y corre al portal"],
       "lista skuldafn", y=.48),
    aba([("embajada", "Embajada"), ("aela", "Aela"), ("harkon", "Harkon")], "Y ya que estás", ("decirle que sí a Harkon", .6),
        ["entra a la embajada", "habla con Aela", "decirle que sí a Harkon"], "repaso", x=.30),
    mis("puedes hacerlo todo. Una vez", "Skyrim", "Puedes hacerlo todo. Una vez", dur=3.2, y=.30),

    # ================= CIERRE
    podi([("nahkriin", "Bastón de Nahkriin"), ("invocar_tormenta", "Invocar tormenta"), ("isran", "Guardia del Alba")], "Este es el top",
         ("a un bastón", 2.6), ["Este es el top", "De unas colmenas", "a un bastón"], "El podio de lo perdido"),
    mis("Ahora te toca a ti", "Te toca", "¿Cuál perdiste tú?", dur=3.6, y=.30),
    mis("Y suscríbete, que vamos", "Camino de diez mil", "Suscríbete", dur=3.2, y=.30),
    pv("Radio Yermo, nuestro canal hermano", "radio_yermo", "Radio Yermo · canal hermano", dur=6.0, x=.72, y=.50, tam=520, marco="monitor"),
    ficha("es todo Fallout", "Radio Yermo", "Todo *Fallout*", "Canal hermano · enlace en la descripción", dur=4.4, x=.26),
    mis("Nos vemos en Tamriel", "Crónicas de Tamriel", "Nos vemos en Tamriel", dur=3.0, y=.30),
]

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in (
    "Número quince", "Número catorce", "Número trece", "Número doce", "Número once", "Número diez", "Número nueve", "Número ocho",
    "Número siete", "Número seis", "Número cinco", "Número cuatro", "Número tres", "Número dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.22) for e in (
    "a la Hacienda Brillo Dorado", "al noroeste de Soledad", "En Cauce Boscoso hay", "Está en Korvanjund",
    "La primera palabra está en Forelhost", "Está en el camino entre Lucero")]
PISTAS += [dict(sfx="monedas", en="Cero monedas", vol=.30), dict(sfx="monedas", en="Un bastón que vale mil", vol=.26),
           dict(sfx="subir_nivel", en="Número uno", vol=.24), dict(sfx="mision_completada", en="Este es el top", vol=.22),
           dict(sfx="mision_iniciada", en="Y ahora, lo que prometí", vol=.22),
           dict(sfx="trueno", en="Y una tormenta de rayos", vol=.45)]   # 26-nov: rayo real de Invocar tormenta (KmxgOEkmNA8 @27,6)
SFX = {}

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
