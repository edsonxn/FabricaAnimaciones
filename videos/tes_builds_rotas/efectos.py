# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 10 builds más ROTAS de Skyrim» (SECUENCIA YT, Crónicas de Tamriel, 10-nov-2026).
REGLA DE ORO (tes_secretos_40) + kits del 5-nov: pegatinas `pv()` con el rotador, estilos de peg_estilos, presentaciones
(tier en el gancho, carrusel de piedras, versus Arquero–Asesino, muro de comentarios, podio final), mapas con ruta y `entrada=`
(coordenadas UESP de `_coords_uesp.py`), fichas de inventario con datos de UESP (`_investigacion.md`) y MG NUEVO `mg_tes.bucle`.
Cada build: aviso de puesto → ficha de la build (raza + piedra) → pegatinas de piedra/objeto/libro/personaje en su segundo → MG.
    python fab.py tes_builds_rotas fx --seco      python fab.py tes_builds_rotas fx hoja
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


# ---------------------------------------------------------------- helpers (de tes_seres_poderosos)
def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def tier(items, de, a, marcas, titulo=None, filas=("S", "A", "B", "C", "D")):
    import presenta as PR
    return _pres(PR.tierlist([(P(s), n, f) for s, n, f in items], filas, titulo, TEMA_PEG), de, a, marcas, "tier list")


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def podi(tres, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.podio(_f(tres), titulo, TEMA_PEG), de, a, marcas, "podio")


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


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def mis(en, arriba, titulo, dur=3.0, y=.30):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(P("com_" + cid), "", tam, giro=-3.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + cid, ver=1.0)


def aviso(en, n, titulo, dur=3.4):
    return dict(tipo="mg", fn=T.mision(f"Build número {n}", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


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


# ---------------------------------------------------------------- coordenadas UESP (mapas/skyrim.jpg, `_coords_uesp.py`)
GUARDIANAS, CAUCE = (.505, .675), (.547, .633)
SOMBRIA, RIFTEN = (.883, .823), (.887, .783)
VOLKIHAR, RITUAL, CARRERA = (.090, .078), (.608, .519), (.539, .525)
SANTUARIO, FALKREATH = (.409, .745), (.434, .753)
SENOR, MORTHAL, APRENDIZ = (.503, .341), (.404, .311), (.364, .274)
AMANTE, MARKARTH = (.159, .445), (.108, .488)
HIBERNALIA, NOCTURNAL, LUCERO = (.744, .183), (.577, .212), (.555, .198)
ATRONACH = (.788, .588)

# ---------------------------------------------------------------- comentarios (≤ 10 días, ninguno usado antes)
C_NPC, C_UNION, C_JINBEI = "UgzfSdO-HC6p8YGBExZ4AaABAg", "UgxGmr6C8A_eLlrFMrR4AaABAg", "UgzSJ4BkkwvexITj7oF4AaABAg"
C_EDGAR, C_YETRISE = "Ugz-N2L_9u_o78TCuK94AaABAg", "UgzYlJHfo9-g-E7Y6qR4AaABAg"
C_REAPEK, C_DJ, C_ESTEBAN = "UgzbsSrLV6bXLU0aLJh4AaABAg", "UgyS2qH64fCSfoN8pCV4AaABAg", "UgyQvodQPI8m3xNf-zl4AaABAg"

PIEDRAS = [("piedra_ladron", "Ladrón"), ("piedra_sombria", "Sombría"), ("piedra_aprendiz", "Aprendiz"), ("piedra_ritual", "Ritual"),
           ("piedra_senor", "Señor"), ("piedra_atronach", "Atronach"), ("piedra_amante", "Amante")]

FX = [
    # ================= GANCHO: un elemento nuevo cada 2-3 s
    zoom(0.0, "Un nigromante con un ejército", 1.12),
    pv("Un arquero que mata dragones", "arco_hueso_dragon", "Arco de hueso de dragón", dur=2.6, x=.18, y=.60, tam=380, entrada="tinta"),
    pv("Un mago con la barra de magia", "tunica_miraak", "Coste: cero", dur=2.4, x=.80, y=.58, tam=360, marco="naipe"),
    rel("Un asesino que tumba a un dragón", "dragon_legendario", "Dragón legendario", "Una puñalada", dur=2.8, x=.24, y=.52, tam=440),
    pv("Un nigromante con un ejército", "esclavo_muerto", "Esclavo muerto", dur=2.4, x=.78, y=.60, tam=340, entrada="aplasta"),
    pv("con sal y unos peces", "sal", "Montón de sal", dur=2.6, x=.18, y=.58, tam=320, marco="vitral"),
    mis("Las diez más rotas de Skyrim", "Crónicas de Tamriel", "Las 10 builds más ROTAS", dur=3.4, y=.30),
    ficha("Cada una, probada", "Probadas", "Cada build, *en partida*", "Fuentes en la descripción", dur=3.2),
    tier([("bosmer", "Arquero", "C"), ("khajiit", "Carterista", "C"), ("altmer", "Titiritero", "B"), ("senor_vampiro", "Vampiro", "B"),
          ("esclavo_muerto", "Nigromante", "B"), ("guantes_hermandad", "Asesino", "A"), ("tunica_miraak", "Mago sin coste", "A"),
          ("piedra_atronach", "Pararrayos", "A"), ("orc", "Artesano", "S"), ("sal", "Boticario", "S")],
         "dos de ellas son trampas", ("Es borrar Skyrim", .3),
         ["dos de ellas son trampas", "Te diré cuáles", "quédate hasta el número uno", "ya no es una build", "Es borrar Skyrim"],
         "La tabla de las builds"),

    # ================= 10 · ARQUERO FANTASMA
    aviso("Número diez", 10, "El Arquero Fantasma"),
    ficha("La build que acaba haciendo todo el mundo", "El 90 %", "De los jugadores acaba de *arquero sigiloso*", "Dato sin fuente: es un chiste",
          dur=3.6, x=.24, y=.30),
    pv("elfo del bosque, con más diez", "bosmer", "Elfo del bosque · +10 Arquería", dur=3.6, x=.18, y=.60, tam=380),
    mapa("skyrim.jpg", "Skyrim", [pt(CAUCE, "Cauce Boscoso", "inicio", "riverwood"), pt(GUARDIANAS, "Piedras guardianas", "poder", "piedras_guardianas")],
         "Piedra: la del Ladrón", ("aunque en el menú esté en combate", .4), ["Piedra: la del Ladrón", "al suroeste de Cauce Boscoso"],
         "Piedras guardianas", ventana=True, ancho=900, x=.70, y=.45, entrada="foco"),
    ficha("la sube la piedra del Ladrón", "Piedra del Ladrón", "Sigilo *+20 %* más rápido. Incluye *Arquería*",
          "No la del Guerrero", dur=4.4, x=.26, y=.30),
    mg(T.barras("Multiplicador del arco", [(None, "Máxima tensión", 2, 0, T.HUESO), (None, "Puntería mortífera (sigilo)", 3, 1, T.ORO)],
                unidad="×", remate=("×6 por flecha", 2)),
       "Las ventajas: Máxima tensión", ("a la mitad de velocidad", .3), ["Máxima tensión", "Puntería mortífera", "Y Mano firme"],
       "multiplicador arco", y=.40),
    rel("El arco de hueso de dragón, de Dawnguard", "arco_hueso_dragon", "Arco de hueso de dragón", "20 de daño · el más alto", dur=4.6, x=.74, y=.50),
    pv("se le quita a un Guardián", "guardian_keeper", "Guardián", dur=3.0, x=.20, y=.60, tam=360, marco="estampilla"),
    ficha("el grito Ralentizar tiempo", "Ralentizar tiempo", "El mundo al *10 %* durante *16 s*", "Grito · 3 palabras", dur=5.0),
    pv("Tiempo de sobra para vaciar la aljaba", "ralentizar_tiempo", "Ralentizar tiempo", dur=3.0, x=.20, y=.60, tam=340),
    rel("Cinta dorada al mérito", "libro_cinta_dorada", "Cinta dorada al mérito", "Libro de Arquería", dur=5.0, x=.76, y=.52, tam=440),
    mis("la flecha está clavada en su cinta", "Moraleja", "El buen arquero era el otro", dur=3.6, y=.30),

    # ================= 9 · CARTERISTA ENVENENADOR
    aviso("Número nueve", 9, "El Carterista Envenenador"),
    pv("Raza: khajiita", "khajiit", "Khajiita · +10 Discreción", dur=3.4, x=.18, y=.60, tam=380),
    mapa("skyrim.jpg", "La Grieta", [pt(RIFTEN, "Ríften", "inicio", "riften"), pt(SOMBRIA, "Piedra Sombría", "poder", "piedra_sombria")],
         "Piedra: la Sombría", ("sesenta segundos invisible", .4), ["Piedra: la Sombría", "al sur de Ríften"], "piedra Sombría",
         entrada="pliegue"),
    ficha("con la ventaja Envenenado", "Envenenado", "Mete *venenos* en su bolsillo", "Robo 40", dur=4.0),
    ficha("no lo cuenta como crimen", "Recompensa por tu cabeza", "*0* monedas", "Ni delante de toda la plaza", dur=4.0, rojo=True, x=.24),
    mg(T.contadores("Guardia de Carrera Blanca", [("Venenos en el bolsillo", 3, None, 0), ("Testigos", 12, None, 0), ("Recompensa", 0, None, None)],
                    remate=("NADIE LLAMA A LOS GUARDIAS", 1)),
       "Le metes tres venenos a un guardia", ("nadie te pone recompensa", .4), ["se los va tomando", "nadie te pone recompensa"],
       "contador veneno", y=.36, x=.70),
    ficha("Toque perfecto", "Toque perfecto", "Roba *cualquier objeto equipado*", "Robo 100", dur=4.0),
    rel("puedes robarle a Astrid", "astrid", "Astrid", "Su armadura y su daga", dur=4.0, x=.76, y=.52, tam=440),
    aba([("armadura_hermandad", "Armadura"), ("hoja_infortunio", "Daga"), ("hoja_infortunio", "Y otra")],
        "Al final te dan otra daga", ("Una para cada mano", .6), ["Al final te dan otra daga", "Una para cada mano"], "dos dagas", x=.30),

    # ================= CORREO (crítica con burla disfrazada)
    com("Un momento, que hay correo", C_NPC, dur=7.5, x=.32, y=.34, tam=820),
    mis("Nueve likes. Mensaje recibido", "Mensaje recibido", "Narra el ganador: el Profeta", dur=4.0, y=.70),
    ficha("en la banca, peleándose", "La banca", "*Tres* voces peleando por un dato", "Johnny · MariCarmen · Hope", dur=4.4, x=.70, y=.30),

    # ================= 8 · TITIRITERO
    aviso("Número ocho", 8, "El Titiritero"),
    pv("Raza: alto elfo", "altmer", "Alto elfo · +10 Ilusión", dur=3.4, x=.18, y=.60, tam=380),
    mapa("skyrim.jpg", "Hjaalmarch", [pt(MORTHAL, "Morthal", "inicio", "morthal"), pt(APRENDIZ, "Piedra del Aprendiz", "poder", "piedra_aprendiz")],
         "Piedra: la del Aprendiz", ("al oeste de Morthal", .6), ["Piedra: la del Aprendiz", "al oeste de Morthal"], "piedra Aprendiz",
         ventana=True, ancho=860, x=.70, y=.45),
    mg(T.versiones("La piedra del Aprendiz", (P("piedra_aprendiz"), "Pantalla de carga", ["Duplica tu magia"], 0),
                   (P("altmer"), "La verdad", ["Solo duplica la regeneración", "Y te deja débil a la magia"], 1), veredicto=("FALSO", 2), pie=None),
       "Este mito lo desmiento yo", ("el doble de debilidad", .4), ["La pantalla de carga dice", "Falso: solo duplica", "el doble de debilidad"], "mito aprendiz", y=.42),
    ficha("Mago fraternal y Furia", "Mago fraternal + Furia", "*+10* y *+12* niveles de tope", "Ilusión 40 · 70", dur=4.4),
    ficha("Y Señor de la mente", "Señor de la mente", "Hasta *no muertos* y *autómatas enanos*", "Ilusión 90", dur=4.0, x=.26),
    rel("lo vende Drevis Neloren", "drevis", "Drevis Neloren", "Colegio de Hibernalia", dur=4.0, x=.76, y=.52, tam=420),
    mg(T.niveles("Tope de nivel del hechizo maestro", [("Sin ventajas", 25), ("Con las ventajas", 47)],
                 notas=[(1, "TODOS CONTRA TODOS", T.ORO, 1)], unidad=""),
       "hasta nivel veinticinco", ("Tú solo sales a recoger", .2), ["hasta nivel veinticinco", "hasta nivel cuarenta y siete"],
       "niveles titiritero", y=.44, x=.30),
    mis("Hace terapia de grupo", "Terapia de grupo", "Pregúntenle a la banca", dur=3.0, y=.30),

    # ================= 7 · SEÑOR DE LOS VAMPIROS
    aviso("Número siete", 7, "El Señor de los Vampiros"),
    mapa("skyrim.jpg", "Mar de Fantasmas", [pt(LUCERO, "Lucero del Alba", "inicio"), pt(VOLKIHAR, "Castillo Vólkijar", "poder", "castillo_volkihar")],
         "Se consigue aceptando el regalo", ("te alinea con su clan", .6), ["el regalo de Lord Járkon", "en el castillo Vólkijar"],
         "Castillo Volkihar", entrada="desenrolla"),
    sil("Lord Járkon", "harkon", "Lord Járkon", "El regalo", dur=4.0, lado="der", alto=860),
    mg(T.contadores("Forma de Señor · nivel 46+", [("Salud extra", 250, None, 0), ("Magia extra", 200, None, 1), ("Aguante extra", 100, None, 2)]),
       "A nivel cuarenta y seis", ("magia y aguante a la vez", .2), ["doscientos cincuenta de salud", "doscientos de magia", "magia y aguante"],
       "stats vampiro", y=.36, x=.70),
    pv("Puedes agarrar a un arquero", "senor_vampiro", "Señor de los Vampiros", dur=4.0, x=.20, y=.60, tam=400),
    ficha("te conviertes en niebla", "Forma de niebla", "*Invulnerable* mientras regeneras", "Ventaja de vampiro", dur=4.0),
    rel("si Serana te acompaña", "serana", "Serana", "Tu daño: 0", dur=5.0, x=.24, y=.52, tam=440),
    ficha("baja a cero", "Absorción vampírica", "Daño a la salud: *0*", "Si Serana te acompaña", dur=4.0, rojo=True),
    ficha("iba a tener tiempo límite", "Contenido cortado", "La forma de Señor tenía *tiempo límite*", "Járkon grabó el aviso", dur=4.4),

    # ================= 6 · NIGROMANTE INFINITO
    aviso("Número seis", 6, "El Nigromante Infinito"),
    pv("Raza: bretón", "breton", "Bretón · +10 Conjuración", dur=3.2, x=.18, y=.60, tam=380),
    mapa("skyrim.jpg", "Carrera Blanca", [pt(CARRERA, "Carrera Blanca", "inicio", "carrera_blanca"), pt(RITUAL, "Piedra Ritual", "poder", "piedra_ritual")],
         "Piedra: la Ritual", ("Gigantes y mamuts incluidos", .3), ["Piedra: la Ritual", "al este de Carrera Blanca"], "piedra Ritual",
         ventana=True, ancho=880, x=.70, y=.45, entrada="mesa"),
    aba([("gigante", "Gigantes"), ("mamut", "Mamuts")], "Gigantes y mamuts incluidos", ("Y aquí viene lo roto", .2),
        ["Gigantes y mamuts"], "gigantes", x=.28),
    rel("La Corona aetérica", "corona_aeterica", "Corona aetérica", "Dos piedras a la vez", dur=4.6, x=.74, y=.50),
    mg(T.bucle("La Corona aetérica", ["Ponte la corona", "Usa la Ritual", "Quítatela", "Vuelve a ponerla"], [2, 3, 4, 99],
               unidad=" ejércitos", remate=("Sin límite", 3)),
       "Y si te quitas la corona", ("de no muertos, sin límite", .4),
       ["Y si te quitas la corona", "puedes usar la Ritual otra vez", "Ejércitos de no", "de no muertos, sin límite"], "bucle corona", y=.46),
    pv("Conjurar a un señor dremora", "senor_dremora", "Señor dremora · 545 de salud", dur=4.0, x=.80, y=.58, tam=400),
    ficha("Esclavo muerto", "Esclavo muerto", "Reanima *para siempre* hasta nivel *40*", "Conjuración maestra", dur=4.4),
    sil("Úlfric Capa de la Tormenta, reanimado", "ulfric", "Úlfric reanimado", "Sigue gritando", dur=5.2, lado="izq", alto=900),
    ficha("en Legendario, tus invocaciones", "Letra pequeña", "En Legendario tus invocaciones reciben *×0,25*", "Dificultad Legendario", dur=4.4, rojo=True),
    rel("Mannimarco, rey gusano", "libro_mannimarco", "Mannimarco, rey gusano", "Sube… Alquimia", dur=4.6, x=.76, y=.52, tam=420),

    # ================= AGRADECIMIENTOS (5 juntos + la voz recuerda que se leen todos)
    com("Los comentarios de esta semana", C_UNION, dur=5.0, x=.30, y=.28, tam=720),
    com("Tus videos se merecen más views", C_JINBEI, dur=4.2, x=.70, y=.30, tam=640),
    com("Videazo", C_REAPEK, dur=3.6, x=.30, y=.70, tam=600),
    com("@estebato2448", C_ESTEBAN, dur=4.4, x=.70, y=.70, tam=640),
    com("@DJRaygadaVargas", C_DJ, dur=5.2, x=.50, y=.34, tam=760),
    mis("Los leemos todos", "Se leen todos", "Los buenos, y los que duelen", dur=4.4, y=.72),

    # ================= 5 · ASESINO DE LA HERMANDAD
    aviso("Número cinco", 5, "El Asesino de la Hermandad"),
    mis("Un dragón, una puñalada", "Contrato", "Un dragón · cero testigos", dur=3.0, y=.30),
    pv("Raza: khajiita o elfo del bosque", "khajiit", "Khajiita o bosmer", dur=3.2, x=.18, y=.60, tam=360, marco="naipe"),
    mg(T.barras("Ataque sigiloso con daga", [(None, "Puñalada por la espalda", 6, 0, T.HUESO), (None, "Hoja del asesino", 15, 1, T.HUESO),
                                              (P("guantes_hermandad"), "+ Guantes de la Hermandad", 30, 2, T.ORO)],
                unidad="×", remate=("×30", 3)),
       "Las ventajas: Puñalada", ("Recursos Humanos", .2), ["Puñalada por la espalda", "con dagas, por quince", "Por treinta", "Recursos Humanos"],
       "multiplicador asesino", y=.42),
    mapa("skyrim.jpg", "Falkreath", [pt(FALKREATH, "Falkreath", "inicio"), pt(SANTUARIO, "Santuario de la Hermandad", "poder", "santuario_hermandad")],
         "Al unirte a la Hermandad Oscura", ("Por treinta", .3), ["Al unirte a la Hermandad", "Astrid te da unos guantes"],
         "Santuario", ventana=True, ancho=600, x=.20, y=.72, entrada="foco"),
    mg(T.golpes("¿Cuántas puñaladas?", (P("dragon_legendario"), "Dragón legendario"), 4163,
                [(P("hoja_infortunio"), "Daga de 139 · ×30", 1, 4)], fases=("Adepto", "Legendario"), remate=("UNA PUÑALADA", 0)),
       "un dragón legendario tiene", ("Una puñalada", .3), ["un dragón legendario tiene", "basta una daga"], "golpes dragón", y=.44),
    rel("la Navaja de Mehrunes", "navaja_mehrunes", "Navaja de Mehrunes", "Muerte instantánea", dur=4.4, x=.76, y=.52, tam=420),
    aba([("miraak", "Mirák"), ("karstaag", "Karstaag")], "Solo Mirák y Karstaag", ("son inmunes", .5), ["Solo Mirák y Karstaag"],
        "inmunes", x=.28),
    mg(T.versiones("La Navaja de Mehrunes", (P("navaja_mehrunes"), "La comunidad", ["1 de cada 100 golpes"], 0),
                   (P("navaja_mehrunes"), "El código del juego", ["2 de 101 = 1,98 %", "Casi el doble"], 1), veredicto=("FALSO", 2), pie=None),
       "Todos dicen que la Navaja", ("noventa y ocho por ciento", .4), ["Todos dicen", "Por un descuido", "noventa y ocho"], "mito navaja", y=.42),
    pv("de la habitación de Babette", "babette", "Babette", dur=3.4, x=.80, y=.60, tam=340),
    rel("Testigo sagrado", "libro_testigo_sagrado", "Testigo sagrado", "Libro de Discreción", dur=8.6, x=.26, y=.50, tam=460),
    pv("Un poeta conoce a la Madre Noche", "madre_noche", "La Madre Noche", dur=3.6, x=.78, y=.58, tam=360, marco="vitral"),
    ficha("dos piedras en los ojos", "Nota del editor", "Una piedra *negra* y una *blanca*", "Testigo sagrado", dur=4.0, rojo=True),
    mis("Lo sé, Roirek", "Crónicas de ChatGPT", "Acertando. Qué horrible.", dur=4.4, y=.72),

    # ================= 4 · MAGO SIN COSTE
    aviso("Número cuatro", 4, "El Mago Sin Coste"),
    pv("Raza: elfo oscuro", "dunmer", "Elfo oscuro · +10 Destrucción", dur=3.4, x=.18, y=.60, tam=380),
    mapa("skyrim.jpg", "Hjaalmarch", [pt(MORTHAL, "Morthal", "inicio", "morthal"), pt(SENOR, "Piedra del Señor", "poder", "piedra_senor")],
         "Piedra: la del Señor", ("lo único que importa es sobrevivir", .3), ["Piedra: la del Señor", "al este de Morthal"],
         "piedra Señor", entrada="desenrolla"),
    mg(T.contadores("Coste de Destrucción", [("Prenda 1", 25, None, 0), ("Prenda 2", 50, None, 1), ("Prenda 3", 75, None, 2),
                                             ("Prenda 4", 100, None, 3)], remate=("COSTE: 0", 4)),
       "cuatro prendas que reducen", ("totalmente legal", .3), ["cuatro prendas", "veinticinco por ciento", "bajan el coste a cero", "Cero",
                                                                "totalmente legal"], "coste cero", y=.36, x=.70),
    ficha("¿Cómo se llega al veinticinco", "Reforzar destrucción", "*−25 %* por prenda", "Encantamiento 100 + gema grande", dur=4.6),
    ficha("Con Doble destrucción e Impacto", "Impacto", "A dos manos, *desequilibra*", "Destrucción 40", dur=4.0, x=.26),
    rel("una espada de escarcha", "escarchafilo", "Espada de escarcha", "Usos infinitos", dur=4.0, x=.76, y=.52, tam=400),
    mg(T.versiones("Aristocrático · altos elfos", (P("altmer"), "Su descripción", ["Magia ×25 más rápido"], 0),
                   (P("altmer"), "La cuenta real", ["≈ ×9,33", "Mucho. Pero no 25"], 1), veredicto=("FALSO", 2), pie=None),
       "Su poder racial dice", ("Pero no veinticinco", .4), ["Su poder racial dice", "Haz la cuenta", "Pero no veinticinco"], "mito altmer", y=.42),
    pv("Los magos estudian años", "colegio_hibernalia", "Colegio de Hibernalia", dur=3.4, x=.20, y=.60, tam=400, marco="estampilla"),

    # ================= 3 · PARARRAYOS
    aviso("Número tres", 3, "El Pararrayos"),
    mis("Tu bola de fuego me recarga", "Absorción", "Gracias", dur=2.8, y=.30),
    ficha("Incluido el aliento de dragón", "Absorción de hechizos", "Anula el efecto *entero*. Incluido el *aliento de dragón*",
          "Todo lo que no sea físico", dur=4.6),
    mapa("skyrim.jpg", "Marca Oriental", [pt(RIFTEN, "Ríften", "inicio"), pt(ATRONACH, "Piedra del Atronach", "poder", "piedra_atronach")],
         "más la piedra del Atronach", ("Durante un minuto", .4), ["la piedra del Atronach"], "piedra Atronach",
         ventana=True, ancho=860, x=.28, y=.45),
    mg(T.barras("Absorción permanente (Dragonborn)", [(P("piedra_atronach"), "Piedra del Atronach", 50, 0, T.HUESO),
                                                        (None, "Ventaja Atronach", 30, 1, T.HUESO), (P("tunica_miraak"), "Túnica de Mirák", 15, 2, T.HUESO),
                                                        (None, "Guantes o botas", 5, 3, T.ORO)], unidad=" %", remate=("100 %", 4)),
       "El permanente, de Dragonborn", ("Con cualquier raza", .3),
       ["piedra del Atronach, cincuenta", "La ventaja Atronach", "La túnica de Mirák", "Y sus guantes", "Cien. Con cualquier"], "absorción", y=.42),
    sil("Mirák lleva siglos", "miraak", "Mirák", "Te deja su ropa", dur=4.6, lado="izq", alto=880),
    ficha("Es un error: un vampiro", "Necromago + vampiro", "*100 %* permanente", "Error · lo arregla el parche no oficial", dur=4.6, rojo=True),
    pv("un sacerdote dragón y un dragón", "sacerdote_dragon", "Sacerdote dragón", dur=3.6, x=.20, y=.60, tam=380),

    # ================= CAMPAÑA
    mg(T.rejilla("De cada cien que ven el canal", n=100, encendidas=13, remate=("Solo 13 suscritos", 1)),
       "De cada cien que ven", ("están suscritos", .6), ["De cada cien que ven", "solo trece están suscritos"], "rejilla suscritos", y=.44),
    mg(T.contadores("Meta del canal", [("Suscriptores", 6580, None, 0), ("Siguiente meta", 7000, 0, 1), ("La gran meta", 10000, 1, 2)]),
       "Somos seis mil", ("Menos esfuerzo que el bucle", .2), ["Somos seis mil", "pasamos de siete mil", "camino de diez mil"],
       "meta subs", y=.36, x=.70),

    # ================= 2 · ARTESANO LEGENDARIO
    aviso("Número dos", 2, "El Artesano Legendario"),
    pv("Raza: orco", "orc", "Orco · +5 Encantamiento y Herrería", dur=3.4, x=.18, y=.60, tam=380),
    mapa("skyrim.jpg", "La Marca", [pt(MARKARTH, "Markarth", "inicio", "markarth"), pt(AMANTE, "Piedra del Amante", "poder", "piedra_amante")],
         "Piedra: la del Amante", ("quince por ciento más rápido", .4), ["Piedra: la del Amante", "al noreste de Markarth"],
         "piedra Amante", entrada="pliegue"),
    mg(T.bucle("El bucle legal", ["Ropa de alquimia", "Poción de encantamiento", "Mejor ropa", "Y otra vez"], [0, 20, 32, 40],
               unidad=" %"),
       "con ropa de alquimia haces", ("el equipo de herrería", .3),
       ["con ropa de alquimia haces", "Con esa poción", "Y otra vez", "Hasta que deja de subir"], "bucle legal", y=.46),
    mg(T.niveles("Daño extra del arma", [("Legendario normal", 20), ("Calidad 29 · juego base", 52), ("Calidad 41 · Dragonborn", 73)],
                 notas=[(2, "LA ETIQUETA MIENTE", T.SANGRE, 2)], unidad="+"),
       "Lo medí yo", ("El número sigue subiendo", .3), ["Lo medí yo", "calidad veintinueve", "más setenta y tres"], "niveles artesano",
       y=.44, x=.30),
    ficha("ochenta por ciento menos", "Tope de armadura", "*80 %* menos de daño físico", "567 de armadura", dur=4.4),
    vs(("arco_hueso_dragon", "El artesano"), ("guantes_hermandad", "El asesino"), "Ahora junta esto", ("No queda nada vivo", .5),
       ["Ahora junta esto", "por treinta en sigilo", "No queda nada vivo"], ganador=None, titulo="Juntos"),

    # ================= 1 · DIOS DEL BOTICARIO
    aviso("Y el número uno", 1, "El Dios del Boticario"),
    ficha("Aviso: esto es un error", "Exploit", "El *parche no oficial* lo corrige", "En consolas sin mods sigue ahí", dur=4.6, rojo=True),
    mg(T.bucle("Reforzar restauración", ["Ponte la ropa", "Haz la poción", "Quítate la ropa", "Bébetela"], [38, 120, 900, 10000],
               remate=("Miles de por ciento", 3)),
       "El procedimiento es así", ("cifras de miles de por ciento", .8),
       ["Haces la poción", "Te quitas la ropa", "Hasta que la ventana", "cifras de miles"], "bucle boticario", y=.46, x=.40),
    aba([("sal", "Montón de sal"), ("abecean", "Abecean Longfin")], "Los ingredientes", ("están llenos", .5),
        ["un montón de sal", "unos peces"], "ingredientes", x=.13, y=.74, tam=230),
    mapa("skyrim.jpg", "La Grieta", [pt(SOMBRIA, "Camino del sur", "inicio"), pt(RIFTEN, "Muelle de Ríften", "poder", "abecean")],
         "Los barriles del muelle", ("están llenos", .5), ["Los barriles del muelle de Ríften"], "muelle Riften", ventana=True, ancho=600,
         x=.81, y=.45),
    rel("Congelación, un hechizo de principiante", "congelacion", "Congelación", "Mata dragones", dur=4.4, x=.76, y=.52, tam=400),
    pv("Los Barbas Grises", "barbas_grises", "Arngeir · Barbas Grises", dur=4.0, x=.20, y=.58, tam=380),
    mapa("skyrim.jpg", "Lucero del Alba", [pt(LUCERO, "Lucero del Alba", "inicio"), pt(NOCTURNAL, "Templo Nocturnal", "poder", "templo_nocturnal")],
         "el Templo Nocturnal", ("de ayudante de cocina", .3), ["el Templo Nocturnal"], "Templo Nocturnal", ventana=True, ancho=820,
         x=.30, y=.45, entrada="foco"),
    rel("Mannimarco, rey gusano. El rey", "libro_mannimarco", "Mannimarco, rey gusano", "Ayudante de cocina", dur=4.0, x=.76, y=.52, tam=400),

    # ================= CIERRE
    podi([("orc", "El Artesano"), ("sal", "El Boticario"), ("piedra_atronach", "El Pararrayos")], "Este es el top", ("borra el juego", 1.2),
         ["Este es el top", "Del arquero que hace", "al alquimista que borra"], "El podio de las builds"),
    pv("La Hoja de ébano", "hoja_ebano", "Hoja de ébano", dur=3.6, x=.20, y=.60, tam=380),
    pv("una mano? ¿El hombre lobo", "hombre_lobo", "¿El hombre lobo?", dur=2.4, x=.80, y=.60, tam=320),
    mis("Déjalo en los comentarios", "Te toca", "¿Cuál falta?", dur=3.6, y=.30),
    mis("Y suscríbete", "Camino de diez mil", "Nos vemos en Tamriel", dur=4.4, y=.30),
]

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Número diez", "Número nueve", "Número ocho", "Número siete",
                                                                 "Número seis", "Número cinco", "Número cuatro", "Número tres", "Número dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.22) for e in ("Piedra: la del Ladrón", "Piedra: la Sombría", "Piedra: la Ritual",
                                                                  "en el castillo Vólkijar", "Piedra: la del Señor", "Piedra: la del Amante")]
PISTAS += [dict(sfx="subir_nivel", en="Y el número uno", vol=.24), dict(sfx="mision_completada", en="Este es el top", vol=.22),
           dict(sfx="grito", en=("vaciar la aljaba.|fin", .1), vol=.85),            # «el grito Ralentizar tiempo» = se oye (silencio p10b)
           dict(sfx="grito", en=("Contra sus propios soldados.|fin", .1), vol=.85)]              # Úlfric reanimado grita (silencio p6b)

# ---- EXTRA (chequeo 10-nov: fichas 1,2 → mediana 1,5 · pegatinas 2,4 → 3,0): donde la voz nombra algo sin apoyo
EXTRA = [
    carr(PIEDRAS, "Con su raza, su piedra", ("Cada una, probada", .1), ["su raza, su piedra", "sus ventajas", "el equipo", "dónde se consigue"],
         titulo="Las piedras de este top"),
    # ficha Mano firme: ya va en el MG multiplicador arco
    # ficha("Y Mano firme", "Mano firme", "Al apuntar, el tiempo al *50 %*", "Arquería 40 · 60", dur=4.0, x=.26),
    pv("en el Colegio de Hibernalia", "colegio_hibernalia", "Colegio de Hibernalia", dur=3.0, x=.20, y=.52, tam=360),
    cam("la única novia que", "serana", "Serana", dur=3.4, x=.80, y=.66),
    cam("Járkon llegó a grabar", "harkon", "Járkon", dur=3.4, x=.18, y=.66),
    ficha("Con Almas gemelas", "Almas gemelas", "*Dos* invocaciones a la vez", "Conjuración 100", dur=4.0, x=.26),
    pv("Y el hechizo maestro Esclavo muerto", "esclavo_muerto", "Esclavo muerto", dur=3.6, x=.20, y=.60, tam=340, marco="vitral"),
    pv("Astrid te da unos guantes", "guantes_hermandad", "Guantes de la Hermandad", dur=4.0, x=.78, y=.58, tam=380),
    ficha("de la misión daédrica Fragmentos", "Fragmentos del pasado", "Silus Vesuius · *Lucero del Alba*", "Misión daédrica", dur=4.0, x=.26),
    ficha("Encantador perspicaz y una gema", "Encantador", "*×3,13* a Reforzar destrucción", "Encantamiento 100 · 5 rangos", dur=4.0, x=.26),
    pv("un bretón con su poder racial", "breton", "Bretón · Piel de dragón", dur=3.6, x=.78, y=.60, tam=360),
    pv("la ventaja Necromago", "senor_vampiro", "Vampiro + Necromago", dur=3.6, x=.20, y=.60, tam=360, marco="naipe"),
    ficha("Con los Libros Negros", "Buscador de hechizos", "Encantamientos *+10 %*", "Libro Negro · Dragonborn", dur=4.0, x=.70),
    ficha("Las pociones de Reforzar restauración", "Reforzar restauración", "Potencia *todo* lo que te pones", "Y el aumento se queda", dur=4.6),
    ficha("Y en Xbox One", "Xbox One", "Más de *10.000 %*: el juego se cuelga", "Congelación mata dragones", dur=4.0, rojo=True, x=.80, y=.20),
]
FX = FX + EXTRA

# ---- CRÍTICAS 2 y 3 (regla del 11-nov-2026: mínimo 2-3 por video, contraburla con el propio tema)
CRITICAS = [
    com("Más correo", C_EDGAR, dur=9.5, x=.32, y=.34, tam=780),
    ficha("con la letra pequeña al final", "Contrato daédrico", "Buenos datos *· letra pequeña*", "Reseña de 7 likes", dur=4.0, x=.72, y=.30),
    aba([("tunica_miraak", "Túnica"), ("escarchafilo", "Y más")], "el mago sin coste también usa ayuda", ("magia de verdad", .4),
        ["el mago sin coste", "cuatro prendas encantadas"], "ayuda del mago", x=.72),
    com("Y el último correo", C_YETRISE, dur=5.0, x=.32, y=.34, tam=760),
    mg(T.bucle("Talento real", ["Poción", "Ropa", "Poción", "Ropa"], [2, 3, 4, 5], unidad=" vueltas", remate=("Él solito", 3)),
       "Como el del que hace el bucle", ("él solito", .4), ["Como el del que hace", "poción, ropa", "ropa, poción", "él solito"],
       "bucle talento", y=.46, x=.66),
    aba([("sal", "Sal"), ("abecean", "Pescado")], "Necesita sal y pescado", ("sal y pescado", .8), ["sal y pescado"], "sal y pescado", x=.30),
]
FX = FX + CRITICAS
# ---- v3 (el usuario, 12-nov-2026): GANÓ EL PROFETA → narra 8 de cada 10 datos y se burla desde arriba; la BANCA (Johnny, MariCarmen,
# Hope, empate a 2 votos) se pelea por el resto. Placa en cada relevo (sale de guion.NARRA) + papeleta del resultado y del cierre.
import re as _re  # noqa: E402
import guion as _G  # noqa: E402

_LEMA = {"el Profeta": "Ganador de la votación"}
_robados, _prev, PLACAS = {}, None, []
for _e in _G.ESCENAS:
    for _i, _tx in enumerate(_e["frases"]):
        _v = _G.NARRA[f"{_e['id']}_{_i}"]
        if _v != _prev and _prev is not None:
            _limpio = _re.sub(r"\[[^\]]*\]\s*", "", _tx)
            _ancla = " ".join(_limpio.split()[:5]).rstrip(",.:;¡!¿?")
            if _v == "el Profeta":
                PLACAS.append(narra(_ancla, "el Profeta", _LEMA[_v], dur=2.6))
                if _ancla.startswith("Este es el top"):
                    PLACAS.pop()   # el podio del cierre ocupa la pantalla: sin placa
            else:
                _robados[_v] = _robados.get(_v, 0) + 1
                PLACAS.append(narra(_ancla, _v, f"En la banca · dato robado n.º {_robados[_v]}", dur=3.6))
        _prev = _v
PLACAS += [
    mg(T.votacion("Resultado de la votación", ["el Profeta · 9", "Johnny · 2", "MariCarmen · 2", "Hope · 2"],
                  remate="Narra el ganador"),
       "Ustedes votaron, y ganó", ("Es lo justo", .4),
       ["Ustedes votaron, y ganó", "Así que narro yo", "Los tres empatados", "se pelean por las migajas", "Es lo justo"],
       "votación resultado", y=.42),
    mg(T.votacion("¿Quién de la banca habla más?", ["Johnny", "MariCarmen", "Hope"], remate="No va a pasar"),
       "vota en los comentarios", ("Nos vemos en Tamriel", .2),
       ["vota en los comentarios", "vota en los comentarios", "vota en los comentarios", "No va a pasar"], "votación banca", y=.42),
]
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
