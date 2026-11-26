# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los MITOS de Ocarina of Time que eran REALES» (SECUENCIA YT, Crónicas del gaming, 26-nov-2026).
Kit translúcido de oot_remake_anadido: `puesto` = «Mito número N», `ficha` = diálogo N64 (mg_majora), pegatinas reales variadas
(pv/sil/rel/cam/leg/aba), mapas reales de Hyrule (mapas/hyrule_3ds.png, coordenadas leídas en mapas/hyrule_rejilla.jpg).
NUEVO en este guion (nucleo/mg_oot.py): `sello(veredicto)` = REAL / A MEDIAS / FALSO de tinta que cae con golpe tras cada mito,
(26-nov: sin votación de voz; Carlos Aguilar es la voz del canal). Comentarios reales: pegatinas/com_*.png.
    FAB_FX_FINAL=1 python fab.py oot_mitos_reales fx hoja    previews/fx_NN.jpg (MÍRALA)
"""
import os

import mg_majora as M
import mg_oot as O
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_N64 = os.path.join(_AQUI, "medios", "n64")
_FX, _FY = .74, .40     # fichas: a la derecha (el cartel del puesto va arriba)
_VW, _VX, _VY = 576, .79, .69
_VH = round(_VW / 1.312)
TEMA = "n64"

CAMARA = {}
FUNDIDO = {}


def _img(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


_P = _img


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    """Pegatina con la siguiente combinación del rotador (marco + entrada + estancia + salida, nunca dos iguales seguidas)."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_img(slug), titulo, tam, tema=TEMA, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return pv(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def filav(en, items, y=.66, tam=300, dur=4.6):
    xs = (.12, .28, .44, .60, .76)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=860, encuadre=(0, .62)):
    fn = PE.silueta(_img(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=480):
    return dict(tipo="mg", fn=PE.reliquia(_img(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .25, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(_img(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(_img(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=290):
    return dict(tipo="mg", fn=PE.abanico([(_img(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + nombre, ver=2.0)


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY):
    d = dict(tipo="mg", fn=M.ficha(titulo, texto, tipo=tipo), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, dur=3.8):
    return dict(tipo="mg", fn=M.puesto(num, titulo, arriba=f"Mito número {num}"), en=en, dur=dur, x=.5, y=.17, sale=.45,
                nombre=f"puesto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def ventana(slug, de, a, desde=0.0, año="1998", sw2=True):
    """El ORIGINAL de N64 en una ventana (FX video) con su marco + la etiqueta SWITCH 2 sobre el cuadro grande.
    sw2=False cuando el cuadro grande TAMBIÉN es de N64 (la ventana es un detalle, no una comparación)."""
    ruta = os.path.join(_N64, slug + ".mp4")
    fx = [dict(tipo="video", de=de, a=a, ruta=ruta, desde=desde, x=_VX, y=_VY, ancho=_VW, entra=.35, sale=.35,
               nombre="ventana " + slug),
          dict(tipo="mg", fn=O.marco(_VW, _VH, año), de=de, a=a, x=_VX, y=_VY - 25 / 1080, sale=.35,
               nombre="marco " + slug, ver=2.0)]
    if sw2:
        fx.append(dict(tipo="mg", fn=O.etiqueta("SWITCH 2", "2026"), de=de, a=a, x=.12, y=.09, sale=.35,
                       nombre="etiqueta sw2", ver=1.0))
    return fx


_MAP = os.path.join(_AQUI, "mapas")


def mapa(puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, "hyrule_3ds.png"), puntos, "zelda", titulo=titulo, sub=sub,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa hyrule", ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa hyrule", ver=4.0)


# Hyrule (mapas/hyrule_3ds.png = «OOT3D Map of Hyrule», Zelda Wiki; coordenadas leídas en mapas/hyrule_rejilla.jpg)
CIUDADELA, KAKARIKO, MONTANA, KOKIRI, BOSQUE_P = (.51, .21), (.66, .24), (.66, .05), (.80, .56), (.71, .50)
LAGO, GERUDO, LONLON = (.28, .80), (.20, .26), (.46, .45)


def com(en, slug, dur=6.0, x=.30, y=.32, tam=760):
    """Comentario REAL del canal (tarjeta de `fab.py yt comentario`) ENTERO y legible: marco simple, sin recortes del rotador."""
    return dict(tipo="mg", fn=M.pegatina(_img("com_" + slug), None, tam, giro=-3.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + slug, ver=1.0)


LAGO_P, PRADERA = (.37, .84), (.41, .39)     # Lago Hylia (el lago entero) y el centro de la pradera de Hyrule


def sello(en, veredicto, sub=None, dur=3.4, x=.78, y=.30):
    """El veredicto del mito: sello de tinta REAL / A MEDIAS / FALSO que cae con golpe (mg_oot.sello) + destello."""
    return [dict(tipo="mg", fn=O.sello(veredicto, sub), en=en, dur=dur, x=x, y=y, sale=.35, nombre="sello " + veredicto,
                 ver=1.2),
            dict(tipo="destello", en=en, dur=.3, fuerza=.35)]


def mito(en, texto, a, x=.27, y=.30):
    """Lo que se contaba en el recreo, en la caja de diálogo de N64."""
    return ficha(en, "Se decía…", texto, tipo="El mito", a=a, x=x, y=y)


FX = [
    # ================================================================ GANCHO (MG desde el primer segundo)
    pv("Los secretos de Ocarina of Time", "n64", "Nintendo 64 (1998)", tam=300, x=.84, y=.30, dur=4.2),
    *filav("Que en un templo se oía un rezo", [("templo_fuego", "Un rezo en un templo", None),
                                               ("ganon", "Ganon sangraba rojo", "Que Ganon sangraba rojo"),
                                               ("kaepora", "El búho era un sabio", "Que el búho pesado")], y=.66, tam=280, dur=4.8),
    pv("se contaban en el recreo", "ocarina_tiempo", "La Ocarina del Tiempo", tam=240, x=.16, y=.30, dur=3.4),
    ficha("Pues hoy revisé 12", "12 mitos del recreo", "Revisados *uno por uno*, con fuentes. *Casi todos* eran verdad.",
          tipo="Este video", a=("Y casi todos eran verdad|fin", .4)),

    # ================================================================ CONTEXTO: LAS REGLAS
    *sello(("Real, a medias, o falso", 0), "REAL", dur=1.6, x=.20, y=.30),
    *sello(("a medias, o falso", .1), "A MEDIAS", dur=1.4, x=.50, y=.30),
    *sello(("o falso", .1), "FALSO", dur=1.6, x=.80, y=.30),
    pv("el remake de Switch 2", "switch2", "Switch 2: 5 de noviembre de 2026", tam=300, x=.84, y=.66, dur=4.4),

    # ================================================================ 12 / LA LOCHA
    puesto("Número 12.", 12, "El pez imposible del estanque"),
    mapa([(*LAGO_P, "Lago Hylia", "poder")], ("en el estanque de pesca del Lago Hylia", -.3), ("que casi nadie lograba sacar|fin", .3),
         [], titulo="Estanque de pesca", sub="Lago Hylia", ventana=True, x=.76, y=.40),
    mito("Se decía que en el estanque", "Un pez *enorme* que casi nadie lograba *sacar*.", ("que casi nadie lograba sacar|fin", .2)),
    *sello("Real. Es la locha", "REAL"),
    grande("Es la locha hyliana", "locha", "Locha hyliana", lado="izq", dur=4.8, tam=600),
    rel("que el dueño del estanque considera trampa", "pescador", "El dueño del estanque", "«Eso es trampa»", x=.78, y=.48, tam=420,
        dur=4.6),
    ficha("Solo muerde el señuelo hundido", "Señuelo hundido", "El único que la hace *morder*… y el que el dueño llama *trampa*.",
          tipo="La regla", a=("te regaña|fin", .4), x=.27, y=.30),
    pv("Y en el remake sigue ahí", "switch2", "Remake: sigue ahí", tam=260, x=.84, y=.30, dur=3.6),

    # ================================================================ 11 / LOS CUCOS
    puesto("Número 11.", 11, "La venganza de las gallinas"),
    mapa([(*KAKARIKO, "Kakariko", "poder")], ("En el recreo alguien siempre juraba", -.2), ("llegaba un ejército de gallinas|fin", .2),
         [], titulo="Aldea Kakariko", sub="La señora de los cucos", ventana=True, x=.76, y=.40),
    mito("si le pegabas mucho a un cuco", "Pégale mucho a un *cuco* y llega un *ejército* de gallinas.", ("a matarte|fin", .2)),
    *sello("Real. Golpea a un cuco", "REAL"),
    sil("aparece una bandada", "cuco", "Cuco", "No se puede derrotar", lado="izq", dur=5.0, encuadre=(0, .8)),
    ficha("Te atacan sin parar", "Cómo escapar", "Sal de la *zona* o métete en una *casa*.", tipo="Supervivencia",
          a=("te metes en una casa|fin", .3), x=.74, y=.30),
    pv("Es una gallina con rencor", "ganondorf", "El segundo más peligroso", tam=260, x=.16, y=.40, dur=3.6),
    pv("siguen igual de rencorosas", "switch2", "Remake: igual de rencorosas", tam=260, x=.84, y=.30, dur=3.4),

    # ================================================================ 10 / EPONA DE NIÑO (FALSO)
    puesto("Número 10.", 10, "Montar a Epona de niño"),
    mapa([(*LONLON, "Rancho Lon Lon", "poder")], ("Este lo juró media generación", -.2), ("en el Rancho Lon Lon|fin", .3), [],
         titulo="Rancho Lon Lon", sub="Donde vive Epona", ventana=True, x=.76, y=.40),
    mito("Que con un truco", "Con un truco, *Link niño* se subía a *Epona*.", ("en el Rancho Lon Lon|fin", .2)),
    *sello("Falso. De niño", "FALSO", "Solo con códigos o mods"),
    *filav("Epona es una potranca", [("malon", "Malon", None), ("potranca", "Epona, 7 años después", "La montas hasta siete")],
           y=.64, tam=300, dur=5.6),
    pv("Link niño sí monta a Epona", "link_nino", "Link niño", tam=260, x=.16, y=.40, dur=3.4),
    rel("Pero en Majora's Mask", "majora", "Majora's Mask (2000)", "Ahí sí la monta", x=.78, y=.50, tam=420, dur=4.6),

    # ================================================================ 9 / EL CORREDOR
    puesto("En el 9, el corredor", 9, "El corredor de la pradera"),
    mapa([(*PRADERA, "Pradera de Hyrule", "poder"), (*CIUDADELA, "Ciudadela")], ("Es un hombre que corre por Hyrule", -.2),
         ("por más rápido que fueras|fin", .2), [], titulo="Pradera de Hyrule", sub="Su pista de carreras", ventana=True, x=.76,
         y=.40),
    sil("Y el mito decía que nadie le podía ganar", "corredor", "El corredor", "Nunca pierde", lado="izq", dur=5.0, encuadre=(0, .7)),
    *sello("Real. El juego está programado", "REAL"),
    mg(O.contador(0, 1, "Segundos de ventaja", _P("corredor"), sub_antes="Salida", sub_despues="Siempre"),
       ("Por exactamente un segundo", -.2), ("Hagas lo que hagas|fin", .5), [], "un segundo", y=.66, x=.30),
    pv("más trampa que tú con la locha", "locha", "La locha (la trampa)", tam=260, x=.84, y=.62, dur=3.4),

    # ================================================================ COM1: GRACIAS
    com("Alguien escribió en el video de los jefes", "UgxuKokZI3i2htbflbR4AaABAg", dur=6.4),
    ficha("Todos los comentarios se leen", "Gracias", "Todos los comentarios *se leen* y se toman en cuenta para *mejorar*.",
          tipo="Comentarios", a=("para mejorar cada video|fin", .3), x=.74, y=.66),

    # ================================================================ 8 / STALCHILDREN
    puesto("Número 8.", 8, "Los esqueletos que crecen"),
    mapa([(*PRADERA, "Pradera de Hyrule (de noche)", "poder")], ("De noche, en la pradera de Hyrule", -.2), ("los Stalchildren|fin", .3),
         [], titulo="Pradera de Hyrule", sub="Solo de noche", ventana=True, x=.76, y=.40),
    mito("Y el rumor decía que si matabas muchos", "Mata *muchos* esqueletos y sale uno *gigante*.", ("salía uno gigante|fin", .2)),
    *sello("Real. Si vas de niño", "REAL"),
    mg(O.contador(0, 20, "Stalchildren derrotados", _P("stalchild"), sub_antes="Al anochecer", sub_despues="Uno enorme"),
       ("y derrotas a 10", -.3), ("uno enorme|fin", .6), [], "contador stalchildren", y=.66, x=.30),
    rel("Y al llegar a 20, uno enorme", "stalchild", "Stalchild", "10 = grande / 20 = enorme", x=.80, y=.60, tam=380, dur=4.0),
    ficha("El contador se borra al amanecer", "Las reglas", "Se reinicia al *amanecer*. Por el *sendero de tierra* no salen.",
          tipo="Letra pequeña", a=("ni siquiera salen|fin", .3), x=.27, y=.30),

    # ================================================================ 7 / URA ZELDA
    puesto("En el 7, el Zelda secreto", 7, "Ura Zelda"),
    rel("el lector de discos de la Nintendo 64", "dd64", "64DD", "El lector de discos", x=.78, y=.48, tam=440, dur=4.8),
    *sello("Real. Se llamaba Ura Zelda", "REAL"),
    leg("aonuma", "Iwata Asks", ["«Master Quest para el 64DD»", "Mazmorras reutilizadas"], ("Eiji Aonuma contó en Iwata Asks", -.2),
        ("reutilizando las mazmorras de Ocarina|fin", .4), marcas=["reutilizando las mazmorras"], sello=("URA ZELDA", 1), x=.22,
        y=.48),
    pv("como Master Quest", "mq_logo", "Master Quest (GameCube)", tam=280, x=.84, y=.30, dur=3.6),
    cam("Aonuma no quería rehacer mazmorras", "aonuma", "Eiji Aonuma", x=.16, y=.30, tam=280, dur=3.6),
    mg(O.linea_tiempo([("1998", "Ocarina of Time", _P("n64")), ("1999", "Ura Zelda (64DD)", _P("dd64")),
                       ("2000", "Majora's Mask", _P("majora")), ("2002", "Master Quest (GameCube)", _P("gamecube"))],
                      titulo="Del Zelda secreto a dos juegos"),
       ("El 64DD fracasó", -.2), ("Esas terminaron en Majora's Mask|fin", .6),
       ["El 64DD fracasó", "como Master Quest", "Y de rebote nació otro juego", "Esas terminaron en Majora's Mask"], "línea ura",
       y=.70),

    # ================================================================ 6 / EL BÚHO ES RAURU
    puesto("Número 6.", 6, "El búho que nadie dejaba hablar"),
    rel("Kaepora Gaebora", "kaepora", "Kaepora Gaebora", "«¿Quieres oírlo otra vez?»", x=.80, y=.32, tam=380, dur=4.6),
    mito("Y el mito decía que no era un búho cualquiera", "El búho era un *sabio* disfrazado.", ("sino un sabio disfrazado|fin", .2)),
    *sello("Real. Una piedra chismosa", "REAL", "Hyrule Historia, 2011"),
    pv("Una piedra chismosa del juego", "gossip", "Piedra chismosa", tam=260, x=.16, y=.62, dur=3.6),
    leg("kaepora", "Hyrule Historia", ["El búho = Rauru", "Libro oficial de Nintendo"], ("Y el libro oficial Hyrule Historia", -.2),
        ("Es Rauru, el sabio de la luz", -.2), marcas=["lo confirmó en 2011"], sello=("CONFIRMADO", 1), x=.22, y=.50),
    # Rauru: el clip del remake ya trae su rótulo «RAURU — Creator of the Temple of Time» (no se duplica)

    # ================================================================ COM2: LA GRANJA DEL PUENTE (corrección justa, sin burla)
    com("Y una corrección justa", "UgyuOJFvvrdtPAtJ_kt4AaABAg", dur=7.0),
    mapa([(*CIUDADELA, "Puente levadizo", "poder")], ("En el juego de 1998, Link niño trepaba", -.2), ("cada vez que entrabas|fin", .3),
         [], titulo="Ciudadela de Hyrule", sub="El puente levadizo", ventana=True, x=.76, y=.40),
    mg(O.contador(0, 60, "Rupias gratis", _P("rupia"), sub_antes="Tres rupias rojas", sub_despues="Cada vez"),
       ("tres rupias rojas escondidas", -.2), ("cada vez que entrabas|fin", .5), [], "60 rupias", y=.66, x=.30),
    grande("Lo conté en el video de lo que Nintendo eliminó", "video_eliminado", "Lo que Nintendo ELIMINÓ del remake", lado="der",
           dur=5.4, tam=520),

    # ================================================================ 5 / LA HISTORIA SANGRIENTA
    puesto("Número 5.", 5, "La historia sangrienta de Kakariko"),
    mapa([(*KAKARIKO, "Kakariko: el pozo", "poder"), (.71, .22, "Templo de las Sombras")], ("El rumor decía que debajo de Kakariko", -.2),
         ("había salas de tortura|fin", .3), [], titulo="Debajo de Kakariko", sub="El pozo y el Templo de las Sombras",
         ventana=True, x=.76, y=.40),
    ficha("Aquí se reúne la historia sangrienta", "Templo de las Sombras", "«Aquí se reúne la *historia sangrienta* de Hyrule, de "
          "*codicia* y de *odio*».", tipo="La inscripción de la entrada", a=("de codicia y de odio|fin", .5), x=.27, y=.22),
    *filav("Dentro hay guillotinas", [("templo_sombras", "Templo de las Sombras", None), ("mano_muerta", "Mano Muerta (el pozo)",
                                                                                          "manchas de sangre")],
           y=.66, tam=300, dur=5.6),
    *sello("Así que, a medias", "A MEDIAS", "Teoría de fans"),
    pv("Lo de los sheikah interrogando", "sheik_ico", "Los sheikah", tam=260, x=.16, y=.62, dur=4.0),
    pv("las manchas rojas ahora son oscuras", "switch2", "Remake: manchas oscuras y secas", tam=260, x=.84, y=.30, dur=3.0),

    # ================================================================ 4 / LOS PERDIDOS DEL BOSQUE
    puesto("En el 4, los que se pierden", 4, "Los que se pierden en el bosque"),
    mapa([(*KOKIRI, "Bosque Kokiri"), (*BOSQUE_P, "Bosque Perdido", "poder")], ("Se decía que quien se perdía", -.2),
         ("se convertía en un monstruo|fin", .3), [], titulo="Bosque Perdido", sub="Nadie sale igual", ventana=True, x=.76, y=.40),
    *sello("Real, y lo dice el propio juego", "REAL"),
    sil("Fado, una de las kokiri", "fado", "Fado", "«Todos se vuelven Stalfos»", lado="izq", dur=5.6, encuadre=(0, .6)),
    *filav("Grog, el muchacho", [("grog", "Grog", None), ("cojiro", "Cojiro, su cuco", "durante el intercambio")], y=.42, tam=280,
           dur=5.4),
    rel("terminó convertido en esqueleto", "stalfos", "Stalfos", "Lo que queda de Grog", x=.78, y=.48, tam=440, dur=4.4),
    pv("se vuelven Skull Kids", "skull_kid_oot", "Skull Kid: solo se insinúa", tam=280, x=.16, y=.62, dur=3.8),

    # ================================================================ 3 / LA SANGRE DE GANON + LA MEDIA LUNA
    puesto("Número 3.", 3, "Ganon sangraba rojo"),
    sil("Unos juraban que, en el final", "ganondorf", "Ganondorf", "¿Roja o verde?", lado="izq", dur=5.0, encuadre=(0, .6)),
    pv("Otros, que era verde", "ganon", "Ganon", tam=260, x=.16, y=.40, dur=2.8),
    *sello("Y tenían razón los dos", "REAL", "Versiones 1.0 y 1.1"),
    mg(O.sangre([("1.0", "Sangre roja", (200, 20, 25)), ("1.1", "Sangre roja", (200, 20, 25)), ("1.2", "Sangre verde", (60, 190, 70))],
                titulo="La sangre de Ganon"),
       ("Los primeros cartuchos", -.2), ("Desde la 1.2, es verde|fin", .6), ["las versiones 1.0", "y 1.1", "Desde la 1.2"],
       "sangre", y=.25),
    *filav("El símbolo Gerudo era una media luna", [("simbolo_gerudo_luna", "Símbolo Gerudo (N64)", None),
                                                   ("escudo_espejo", "Escudo Espejo", "en el Escudo Espejo"),
                                                   ("simbolo_gerudo_nuevo", "GameCube: otro símbolo", "Nintendo lo cambió")],
           y=.64, tam=260, dur=6.6),
    rel("Pero se le olvidaron algunas lunas", "dampe", "La tumba de Dampé", "Lunas sin cambiar", x=.78, y=.48, tam=440, dur=5.0),

    # ================================================================ 2 / LA TRIFUERZA (FALSO… HASTA 2022)
    puesto("Número 2.", 2, "La Trifuerza se puede conseguir"),
    mito("una jugadora aseguró en internet", "La Trifuerza se consigue en el *Templo de la Luz* con una *canción secreta*.",
         ("tocando una canción secreta|fin", .2), x=.27, y=.22),
    *sello("Falso. Nunca dio los pasos", "FALSO", x=.28, y=.82),
    rel("no hay Trifuerza", "trifuerza", "La Trifuerza", "No está en el código", x=.78, y=.48, tam=420, dur=4.0),
    pv("Summer Games Done Quick", "gdq", "SGDQ 2022", tam=320, x=.84, y=.30, dur=4.6),
    ficha("Con TASBot, un robot", "TASBot", "Código nuevo *por los mandos*, en un *cartucho original* y una *N64 real*.",
          tipo="SGDQ 2022, en vivo", a=("en una Nintendo 64 real|fin", .4), x=.27, y=.30),
    pv("en un cartucho original", "n64", "Cartucho original + N64 real", tam=260, x=.84, y=.30, dur=3.4),

    # ================================================================ 1 / EL REZO DEL TEMPLO DEL FUEGO
    puesto("Y el número 1.", 1, "El rezo del Templo del Fuego"),
    dict(tipo="destello", en="El rezo del Templo del Fuego", dur=.45, fuerza=.5),
    mito("El mito decía que en la música del Templo del Fuego", "En la música se oía a alguien *rezando*. Y Nintendo la *cambió*.",
         ("la cambió a escondidas|fin", .2)),
    *sello("Y sí, es real", "REAL", "Versiones 1.0 y 1.1"),
    ficha("Escucha", "Templo del Fuego (v1.0)", "Escucha la *voz* de la música original.", tipo="Nintendo 64, 1998",
          a=("Esa voz salió de un CD", -.2), x=.27, y=.30),
    grande("Esa voz salió de un CD comercial", "voice_spectral", "Voice Spectral: CD de sonidos", lado="der", dur=4.4, tam=520),
    cam("Koji Kondo, el compositor", "kondo", "Koji Kondo", x=.16, y=.70, tam=300, dur=4.0, foco=(.5, .3, 1.4)),
    ficha("Esa voz salió de un CD comercial", "Voice Spectral", "Un *CD de sonidos* para músicos. Nadie en Nintendo sabía qué *decía*.",
          tipo="El origen", a=("no sabía lo que decía|fin", .3), x=.27, y=.30),
    pv("Y así siguió en GameCube", "gamecube", "GameCube: sin la voz", tam=260, x=.16, y=.66, dur=4.0),
    *sello("Lo de que la quitaron por las quejas", "FALSO", "Lo de las quejas", x=.78, y=.66),
    ficha("mira detrás del cartucho", "Tu cartucho", "Dos números solos: *1.0*. Con *A*: 1.1. Con *B*: 1.2, ya *no reza*.",
          tipo="Cómo saberlo", a=("el tuyo ya no reza|fin", .6), x=.30, y=.75),

    # ================================================================ CIERRE
    com("En el ranking de mundos de Banjo-Tooie", "UgwuvfcxIyWnxqUwY9h4AaABAg", dur=11.0),
    ficha("Ahora te toca a ti", "Tu turno", "¿Cuál de estos mitos te contaron en el *recreo*?", tipo="Comentarios",
          a=("Te leo en los comentarios|fin", .4), x=.74, y=.66),
    grande("Si quieres ver lo que Nintendo quitó", "video_eliminado", "Lo que Nintendo ELIMINÓ del remake", lado="der", dur=6.0,
           tam=560),
]
ROTULOS = []
SFX = {}        # el canto original (ambiente_por scene-071) y la OST dan la vida; sin SFX añadidos
PISTAS = []
