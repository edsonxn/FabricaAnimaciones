# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Lo que Nintendo AÑADIÓ en SECRETO al REMAKE de Ocarina of Time» (SECUENCIA YT, Crónicas del gaming,
11-nov-2026). Kit de oot_remake_eliminado (translúcido): `puesto` = «Añadido número N», `ficha` = diálogo N64 (mg_majora),
VENTANAS del original (medios/n64/, bajar_ventanas.py), pegatinas reales variadas (pv/sil/rel/cam/leg) y comentarios reales
(pegatinas/com_*.png: 3 críticas con contraburla + la pregunta de Master Quest + el agradecimiento).
MG nuevos de ESTE guion con mg_oot: contadores 0->173 frases, 0->5 millones, 1->2 ocarinas, 4->5 botellas, 0->84 estatuas,
partitura de la Canción de Saria, línea de Master Quest «en el código»; 4 mapas reales de Hyrule (mapas/hyrule_3ds.png) con
ruta: Bosque Kokiri, Ciudadela, las 4 camas del Salón, los templos de los sabios y el Bosque Perdido (cierre del puesto 1).
    FAB_FX_FINAL=1 python fab.py oot_remake_anadido fx hoja    previews/fx_NN.jpg (MÍRALA)
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
    return dict(tipo="mg", fn=M.puesto(num, titulo, arriba=f"Añadido número {num}"), en=en, dur=dur, x=.5, y=.17, sale=.45,
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


FX = [
    # ================================================================ GANCHO (MG desde el primer segundo)
    rel("hay una máscara que todavía no puedes usar", "mascara_103", "¿Una máscara nueva?", "En el código del remake", x=.78, y=.46,
        tam=440, dur=5.0),
    mg(O.contador(0, 173, "Frases escritas para ella", _P("mascara_verdad"), sub_antes="Anunciadas", sub_despues="En el código"),
       ("Tiene 173 frases", -.2), ("nadie en Hyrule sabe qué es|fin", .6), ["Y nadie en Hyrule"], "contador 173", y=.40),
    *filav("Esa máscara, unos sabios", [("mascara_103", "La máscara", None), ("darunia", "Los sabios", "unos sabios"),
                                         ("botella", "5.ª botella", "una quinta botella"), ("mq_logo", "Master Quest", "un Master Quest")],
           y=.66, tam=280, dur=6.4),
    ficha("Así que hoy te cuento", "Ocarina of Time (Switch 2)", "*12 cosas* que Nintendo añadió *sin anunciarlas*.",
          tipo="Lo añadido", a=("a la que nadie vio venir|fin", .5)),

    # ================================================================ CONTEXTO
    pv("solo en Switch 2", "switch2", "Nintendo Switch 2", tam=300, x=.84, y=.28, dur=4.0),
    mg(O.contador(0, 5, "Millones de copias en 4 días", _P("switch2"), sub_antes="5 de noviembre", sub_despues="9 de noviembre"),
       ("en cuatro días vendió", -.2), ("de 5 millones de copias|fin", .8), [], "ventas", y=.40),
    pv("El Ocarina de Nintendo 64", "n64", "Nintendo 64 (1998): 7,6 millones", tam=320, x=.16, y=.64, dur=4.4),
    ficha("Este ya va por el 70 por ciento", "En una semana", "El remake ya lleva el *70 %* de lo que vendió el original "
          "*en toda su vida*.", tipo="Según Kotaku", a=("en una semana|fin", .5)),
    ficha("Y hasta la caja esconde algo", "La caja de Switch 2", "Por dentro: un *mapa de Hyrule*. Debajo del cartucho: *Navi*.",
          tipo="Edición física", a=("aparece Navi|fin", .6), x=.27, y=.30),
    pv("debajo del cartucho aparece Navi", "navi", "Navi", tam=240, x=.84, y=.66, dur=3.0),
    sil("El jefe secreto de Skull Kid", "skull_kid_oot", "Skull Kid", "Bosque Perdido, desde 1998", lado="izq", dur=5.6,
        encuadre=(0, .7)),
    ficha("ya te atacaba en 1998", "¿Jefe secreto?", "*No.* Ya te atacaba en *1998*, con la misma *rupia de 200*.",
          tipo="Desmentido", a=("la misma rupia de 200|fin", .6)),

    # ================================================================ 12 / KOROKS
    puesto("Número 12.", 12, "Koroks en el Bosque Kokiri"),
    mapa([(*KOKIRI, "Bosque Kokiri", "poder"), (*BOSQUE_P, "Bosque Perdido")], ("En el bosque donde empieza todo", -.2),
         ("como polen|fin", .3), ["En el bosque donde empieza todo", "flotan unas hojitas"], titulo="Bosque Kokiri",
         sub="Restos mágicos que flotan", ventana=True, x=.74, y=.40),
    grande("muchas tienen la silueta de un Korok", "korok", "Los Koroks", lado="izq", dur=5.4, tam=560),
    pv("Después de la Gran Inundación", "kokiri", "Kokiris", tam=300, x=.82, y=.30, dur=3.6),
    ficha("Game Informer dice", "Game Informer", "El *único añadido* que apunta al *futuro de la saga*.", tipo="La prensa",
          a=("al futuro de la saga|fin", .4)),

    # ================================================================ 11 / LINK ACTÚA
    puesto("En el 11, Link por fin actúa", 11, "Link por fin actúa"),
    *ventana("ocarina", ("En la Nintendo 64, Link tocaba la ocarina", -.3), ("una flauta de adorno|fin", .3), sw2=False),
    mg(O.partitura(["v", ">", "<", "v", ">", "<"], "Canción de Saria"), ("En el remake mueve los dedos", -.2),
       ("que suena distinto según el lugar|fin", .4), ["Y el sonido es una ocarina real"], "partitura saria", y=.30),
    pv("una ocarina real grabada", "ocarina", "Ocarina real grabada", tam=280, x=.84, y=.66, dur=3.6),
    pv("Link niño levanta los brazos", "link_nino", "Link niño", tam=300, x=.16, y=.62, dur=3.4),
    pv("El adulto no", "link_adulto", "Link adulto", tam=320, x=.84, y=.58, dur=3.4),

    # ================================================================ 10 / OCARINA DE SARIA
    puesto("Número 10.", 10, "La ocarina de Saria ya no se pierde"),
    grande("Saria le regala a Link", "saria", "Saria", lado="der", dur=4.6, tam=520),
    *ventana("zelda", ("cuando Zelda te daba la Ocarina del Tiempo", -.3), ("La nueva la sustituía|fin", .3), sw2=False),
    mg(O.contador(1, 2, "Ocarinas en el inventario", _P("ocarina_hadas"), sub_antes="Nintendo 64", sub_despues="Switch 2"),
       ("En el remake te quedas con las dos", -.2), ("que ya no te quitan|fin", .5), ["y eliges cuál tocar"], "dos ocarinas",
       y=.40),
    *filav("En el remake te quedas con las dos", [("ocarina_hadas", "Ocarina de las Hadas", None),
                                                    ("ocarina_tiempo", "Ocarina del Tiempo", "y eliges cuál tocar")],
           y=.70, tam=260, dur=5.0),

    # ================================================================ 9 / QUINTA BOTELLA
    puesto("En el 9, una quinta botella", 9, "Una quinta botella"),
    mapa([(*CIUDADELA, "Ciudadela de Hyrule", "poder")], ("La primera vez que entras a la Ciudadela", -.2),
         ("se le escapó un bicho|fin", .3), [], titulo="Tienda de pociones", sub="Ciudadela de Hyrule", ventana=True, x=.76,
         y=.40),
    pv("Te presta una botella vacía", "botella", "Botella vacía", tam=260, x=.16, y=.62, dur=3.6),
    pv("con una poción roja de premio", "pocion", "Poción roja", tam=260, x=.84, y=.62, dur=3.4),
    mg(O.contador(4, 5, "Botellas", _P("botella"), sub_antes="Nintendo 64", sub_despues="Switch 2"),
       ("había solo cuatro botellas", -.3), ("tardaba bastante más|fin", .5), [], "botellas", y=.40),
    leg("aonuma", "Game Informer", ["«Las botellas son tan importantes…»", "Pidió la primera antes"],
        ("Las botellas son tan importantes", -.2), ("que la primera llegara antes|fin", .5),
        marcas=["Las botellas son tan importantes", "él mismo pidió"], sello=("5.ª BOTELLA", 1), x=.76, y=.48),

    # ================================================================ 8 / SEMILLA DEL MERCADER
    puesto("Número 8.", 8, "Una tienda en el bolsillo"),
    ficha("la Semilla del Mercader Deku", "Semilla del Mercader Deku", "La lanzas y aparece un *vendedor Deku* donde cae.",
          tipo="Objeto nuevo", a=("aparece un vendedor Deku|fin", .5)),
    rel("aparece un vendedor Deku", "deku_vendedor", "Vendedor Deku", "Aparece donde cae la semilla", x=.22, y=.48, tam=420,
        dur=4.6),
    *filav("Así puedes comprar flechas", [("deku_vendedor", "Flechas", None), ("deku_vendedor", "Bombas", "bombas"),
                                          ("deku_vendedor", "Semillas", "o semillas")], y=.66, tam=240, dur=4.4),
    ficha("si te quedabas sin flechas", "Nintendo 64", "Sin flechas en el *Templo del Bosque* = *media vuelta*.",
          tipo="Antes", a=("te tocaba dar media vuelta|fin", .4), x=.27, y=.34),

    # ================================================================ 7 / REDEADS Y MANO MUERTA
    puesto("En el 7, los ReDeads", 7, "ReDeads y Mano Muerta"),
    *ventana("redead", ("Cuando un ReDead te ve", -.2), ("lo ves forcejear|fin", .3)),
    sil("Te paraliza en cualquier postura", "redead", "ReDead", "Ahora con bandas rojas", lado="izq", dur=5.0, encuadre=(0, .7)),
    rel("Y la Mano Muerta del Fondo del Pozo", "mano_muerta", "Mano Muerta", "Fondo del Pozo, Kakariko", x=.78, y=.46, tam=460,
        dur=6.0),

    # ================================================================ CRÍTICA 1: LOQUENDO
    com("alguien me escribió esto en el video anterior", "UgzIFbzZXlrRTRKk4f14AaABAg", dur=7.5),
    ficha("Lo intenté, de verdad", "Loquendo", "Pidió su pago en *rupias de la granja del puente*.", tipo="Contraoferta",
          a=("Nintendo la eliminó|fin", .4), x=.74, y=.66),
    pv("rupias de la granja del puente", "rupia", "Granja del puente: eliminada", tam=240, x=.84, y=.30, dur=3.6),

    # ================================================================ 6 / EL SALÓN
    puesto("Número 6.", 6, "Un salón que se abre soñando"),
    sil("Kaepora Gaebora te cuenta en Kakariko", "kaepora", "Kaepora Gaebora", "«A través de los sueños»", lado="izq", dur=5.6,
        encuadre=(0, .75)),
    mapa([(*KOKIRI, "Casa de Link"), (*KAKARIKO, "Albergue de Kakariko"), (*LAGO, "Laboratorio del lago"),
          (*GERUDO, "Campamento Gerudo", "poder")],
         ("Cualquier cama con un brillo verde", -.2), ("el campamento del Valle Gerudo|fin", .8),
         ["La de tu casa en el bosque", "el albergue de Kakariko", "el laboratorio del lago", "o el campamento del Valle Gerudo"],
         titulo="Las camas que brillan", sub="Entradas al Salón"),
    ficha("Es el Salón de los Enemigos Caídos", "Salón de los Enemigos Caídos", "*84 estatuas*: una por cada tipo de enemigo "
          "derrotado.", tipo="Zona secreta", a=("que derrotaste|fin", .4), x=.27, y=.30),
    mg(O.contador(0, 84, "Estatuas", _P("redead"), sub_antes="Al entrar", sub_despues="Completo"),
       ("Tiene 84 estatuas", -.2), ("que derrotaste|fin", .4), [], "84 estatuas", y=.72, x=.30),
    ficha("Y puedes volver a pelear con cada jefe", "Revanchas", "Cada jefe *contra reloj*, con *ránking mundial* y un *trofeo* "
          "en tu casa.", tipo="Pruebas", a=("del Bosque Kokiri|fin", .3), x=.27, y=.30),

    # ================================================================ 5 / MÁSCARA DE LA VERDAD
    puesto("En el 5, la Máscara de la Verdad", 5, "La Máscara de la Verdad"),
    rel("la Máscara de la Verdad lee pensamientos", "mascara_verdad", "Máscara de la Verdad", "Lee pensamientos", x=.78, y=.46,
        tam=440, dur=4.6),
    pv("las Piedras Chismosas", "gossip", "Piedra Chismosa (N64)", tam=280, x=.84, y=.62, dur=3.8),
    ficha("si te acercas a alguien de frente", "De frente / por la espalda", "De frente *reacciona*. Por la espalda, oyes *lo que "
          "piensa*.", tipo="Switch 2", a=("lo que piensa de verdad|fin", .4), x=.27, y=.30),
    pv("la máscara Keaton para su hijo", "mascara_keaton", "Máscara Keaton", tam=260, x=.16, y=.40, dur=4.4),
    pv("un niño que persigue un cuco", "cuco", "El cuco", tam=240, x=.84, y=.62, dur=3.4),
    pv("hasta las vacas tienen pensamientos", "vaca", "Las vacas también", tam=260, x=.16, y=.62, dur=3.0),

    # ================================================================ CRÍTICA 2: TIKTOK
    com("Y otro me dejó este consejo", "UgxTR9tM3E5GvcJOawt4AaABAg", dur=6.6),
    ficha("en TikTok no cabe una lista de 12", "TikTok", "Ahí apenas llegaríamos a la *Semilla del Mercader*.",
          tipo="Cálculo serio", a=("a la Semilla del Mercader|fin", .4), x=.74, y=.66),

    # ================================================================ 4 / GANONDORF
    puesto("Número 4.", 4, "Ganondorf ya no es un mudo"),
    pv("al sacar la Espada Maestra", "espada_maestra", "Espada Maestra", tam=260, x=.16, y=.40, dur=3.8),
    ficha("Escucha", "Ganondorf (voz nueva)", "«You're *entertaining*, I'll give you that. For a *child* at most.»",
          tipo="Remake, en inglés", a=("Eres entretenido", -.2), x=.27, y=.30),
    sil("Eres entretenido, te lo concedo", "ganondorf", "Ganondorf", "Ahora con voz", lado="der", dur=5.0, encuadre=(0, .6)),
    pv("tomando la Trifuerza", "trifuerza", "La Trifuerza", tam=280, x=.16, y=.40, dur=4.0),
    leg("aonuma", "Game Informer", ["La escena original", "«explicaba muy poco»"], ("Aonuma explicó que la escena original", -.2),
        ("y cómo reaccionaba|fin", .4), marcas=["explicaba muy poco"], sello=("MÁS ESCENA", 1), x=.76, y=.48),

    # ================================================================ 3 / LOS SABIOS
    puesto("En el 3, una pregunta de 28 años", 3, "¿Los sabios estaban muertos?"),
    mapa([(.72, .47, "Templo del Bosque"), (*MONTANA, "Templo del Fuego"), (.30, .86, "Templo del Agua"),
          (*CIUDADELA, "Cámara de los Sabios", "poder")],
         ("Saria, Darunia y Ruto desaparecían", -.2), ("los daba por muertos|fin", .4),
         ["Saria", "Darunia", "y Ruto"], titulo="Los templos", sub="Donde desaparecían los sabios"),
    *ventana("rauru", ("en la Cámara de los Sabios, cada uno lo cuenta", -.2), ("Así lo dice Darunia|fin", .2)),
    ficha(("Así lo dice Darunia", .8), "Darunia", "«I'd be a pile of *gravel* right now if *Rauru* hadn't pulled me outta the fire.»",
          tipo="Voz nueva en inglés", a=("Que sin Rauru", .3), x=.27, y=.30),
    sil("Que sin Rauru", "darunia", "Darunia", "Sabio del Fuego", lado="der", dur=5.6, encuadre=(0, .6)),
    *filav("Saria dice lo mismo", [("saria", "Saria", None), ("rauru", "Rauru", "Rauru la llamó"),
                                   ("ruto", "Ruto", "No murieron")], y=.66, tam=260, dur=6.0),

    # ================================================================ CRÍTICA 3: VOZ
    com("para el que escribió que mi voz es insufrible", "UgzmJSs-ifaFE_lYT_p4AaABAg", dur=6.0),
    rel("Kaepora Gaebora también hablaba mucho", "kaepora", "Kaepora Gaebora", "Con tema musical propio", x=.80, y=.62, tam=380,
        dur=4.6),

    # ================================================================ 2 / MASTER QUEST
    puesto("Número 2.", 2, "Master Quest, escondido"),
    com("alguien me preguntó si va a salir", "UgznCuHwUwG9P-CtH8h4AaABAg", dur=5.0, x=.30, y=.30, tam=700),
    mg(O.linea_tiempo([("1998", "Ocarina of Time (N64)", _P("n64")), ("2003", "Master Quest en GameCube", _P("gamecube")),
                       ("2026", "Remake: sin Master Quest", _P("switch2")), ("2026", "…pero en el código", _P("mq_logo"))],
                      titulo="Master Quest"),
       ("los dataminers encontraron en el código", -.2), ("de la tripa de Jabu Jabu|fin", .6),
       [("los dataminers encontraron", .1), "El mundo en espejo", "las mazmorras cambiadas", "y hasta vacas"], "línea mq",
       y=.70),
    pv("y hasta vacas dentro", "vaca", "Vacas en Jabu Jabu", tam=260, x=.84, y=.30, dur=3.6),
    leg("aonuma", "A IGN", ["«No vamos a anunciar", "nada por ahora»"], ("cuando le preguntaron a Aonuma", -.2),
        ("ya es casi un sí|fin", .5), marcas=["no iban a anunciar nada", "casi un sí"], sello=("CASI UN SÍ", 1), x=.22, y=.48),

    # ================================================================ 1 / LA MÁSCARA 103
    puesto("Y lo número 1.", 1, "La máscara que todavía no existe"),
    dict(tipo="destello", en="La máscara que todavía no existe", dur=.45, fuerza=.5),
    *filav("Las máscaras de los amiibo", [("amiibo", "Amiibo anunciados", None), ("link_nino", "Máscara 101: Link niño",
                                                                                        "amiibo de Link niño"),
                                           ("zelda_nina", "Máscara 102: Zelda niña", "y de Zelda niña"),
                                           ("mascara_103", "Máscara 103: ¿?", "hay una tercera")], y=.64, tam=250, dur=6.4),
    mg(O.contador(0, 173, "Frases de reacción", _P("mascara_103"), sub_antes="Amiibo anunciado", sub_despues="Escritas"),
       ("Tiene 173 frases de reacción", -.2), ("de otro mundo|fin", .4), [], "contador 173 b", y=.36),
    ficha("Uno de ellos hasta le dice monstruo", "Los personajes", "*Rara*, *inquietante*, de *otro mundo*… y hasta "
          "«*monstruo*».", tipo="Reacciones", a=("si vienes por él|fin", .4), x=.27, y=.30),
    sil("Los fans creen que es un amiibo del duende", "skull_kid", "Skull Kid", "¿El amiibo secreto?", lado="der", dur=5.0,
        encuadre=(0, .7)),
    pv("el remake de la secuela, la de la luna", "majora", "Majora's Mask (2000)", tam=340, x=.16, y=.58, dur=4.4),
    mapa([(*KOKIRI, "Bosque Kokiri"), (*BOSQUE_P, "¿Máscara 103?", "poder")], ("Pero el último punto de este mapa", -.2),
         ("Y una cosa más", -.3), ["el último punto"], titulo="Bosque Perdido", sub="El tocón de Skull Kid"),

    # ================================================================ CIERRE
    com("Alguien escribió en el video de Mario 64", "UgwA4u_c8rOC26tTk-l4AaABAg", dur=7.0),
    ficha("Todos los comentarios se leen", "Gracias", "Todos los comentarios *se leen* y se toman en cuenta para *mejorar*.",
          tipo="Comentarios", a=("para mejorar cada video|fin", .4), x=.74, y=.66),
    ficha("Ahora te pregunto a ti", "Tu turno", "De estas *12 cosas*, ¿cuál te *sorprendió más*?", tipo="Comentarios",
          a=("Te leo en los comentarios|fin", .6)),
    grande("si quieres ver lo que Nintendo quitó", "video_eliminado", "Lo que Nintendo ELIMINÓ del remake", lado="der", dur=6.0,
           tam=560),
]
ROTULOS = []
SFX = {}        # el sonido original (ambiente_por: Ganondorf y Darunia) y la OST dan la vida; sin SFX añadidos
PISTAS = []
