# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Godrick QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 11-nov-2026).
Fórmula de Mohg/Morgott (docs/estilo_secuencia_yt.md § REGLA DE ORO · PEGATINAS · MOTION GRAPHICS NUEVOS · MAPAS) con el kit
de Elden Ring (nucleo/mg_er.py) y los estilos de nucleo/peg_estilos.py (tema «er»):
- PEGATINAS reales de eldenring.fandom.com (bajar_pegatinas.py; identidad en previews/pegatinas_check.jpg).
- COMENTARIOS reales (≤ 10 días, `yt comentario`): Justin y Ádolf (pidieron el tema), Diego, Wolfdragon, lksdmn (votación),
  Tristán, Amand, Gun-chikito (agradecen); críticas con contraburla: José (p5b), Gonzalo (p4b), Madrizu (cierre).
- FICHAS solo con citas del guion (verificadas en _investigacion/dossier.md). Lo CORTADO lleva rótulo «Contenido cortado».
- MG NUEVOS (mg_er): `votacion` (narrador anterior vs nuevo profeta, al inicio y en el cierre), `injerto` (los miembros que
  Godrick se cose, 3 apariciones) y `linaje` (Godfrey → Godrick / Godefroy, 2 apariciones). Además `cien`, `mensaje`, `puesto`.
- MAPAS (limgrave, mundo): Velo Tormentoso, Leyndell, Agheel, Morne, el Puente del Sacrificio, Haight, Liurnia, Altus,
  la cabaña de Roderika, la Capilla de la espera.
- PISTAS voz=True: los 4 sonidos (sfx/s_*.mp3) con la voz callada (`post` en guion.py).
  python fab.py er_godrick_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA, con FAB_FX_FINAL=1)
"""
import os

import mg_er as E
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .30     # fichas: arriba a la derecha
TEMA_MAPA = "er"
TEMA = "er"

CAMARA = {}
FUNDIDO = {}

_P = lambda s: os.path.join(_PAN, s + ".jpg")
_G = lambda s: os.path.join(_PEG, s + ".png")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    """Pegatina con animación de presentación variada (nucleo/peg_anim.py, regla del 5-nov-2026); los comentarios, tarjeta fija."""
    if slug.startswith("com_"):
        return dict(tipo="mg", fn=T.pegatina(_G(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                    nombre="pegatina " + slug, ver=1.0)
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_G(slug), titulo, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=680):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.50, tam=tam)


def fila(en, items, y=.64, tam=340, dur=4.6):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [peg(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, cid, dur=6.0, x=.30, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


def sil(en, ruta, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con la cara visible y el video corriendo detrás."""
    fn = PE.silueta(ruta, nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="silueta " + os.path.basename(ruta), ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
    """Objeto flotando sobre un círculo de runas."""
    return dict(tipo="mg", fn=PE.reliquia(_G(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="reliquia " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    """Medallón para las menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(_G(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="camafeo " + slug, ver=1.0)


def ban(en, ruta, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    """Tira de cine a todo lo ancho con el rostro en primer plano."""
    return dict(tipo="mg", fn=PE.banda(ruta, nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="banda " + os.path.basename(ruta), ver=1.2)


def leg(ruta, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    """Expediente de pergamino con retrato en sepia; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(ruta, titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + titulo, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(ruta, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico(list(fotos), tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="abanico " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(_P(slug), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None, y=_FY):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=_G(icono) if icono else None),
             en=en, x=_FX, y=y, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def msg(lineas, de, a, marcas, nombre):
    """Mensaje del suelo (texto ámbar) abajo, para citas que la voz lee."""
    return mg(E.mensaje(lineas), de, a, marcas, "mensaje " + nombre, y=.76)


def cortado(de, a, sub, nombre):
    """Rótulo «CONTENIDO CORTADO» arriba (lo que no llegó al juego final se dice como tal y se marca en pantalla)."""
    return mg(E.puesto("Contenido cortado", sub), de, a, [], "cortado " + nombre, y=.10)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


C_JUSTIN, C_ADOLF = "UgzGyY8IWYnCg4URqAd4AaABAg", "UgzYn89hW5PP36ZRuI54AaABAg"
C_DIEGO, C_WOLF, C_LKSDMN = "UgwBFIKKPVelW3o3h7R4AaABAg", "UgyVJS8Og4UmM-4tZHV4AaABAg", "Ugw-r_CJZwl0atRCRLh4AaABAg"
C_TRISTAN, C_AMAND, C_GUN = "Ugy4ugg3qhqP86IQLQt4AaABAg", "Ugxak9VXs4Sx2-yrBwh4AaABAg", "UgxXFG7xdHs42gwdNH94AaABAg"
C_JOSE, C_GONZALO, C_MADRIZU = "UgzecfpN69pGrW5jk7l4AaABAg", "UgzWKdLFWzwEg5qrSrB4AaABAg", "UgwOBW3OeA0dU8FXZjl4AaABAg"

# Coordenadas (fracción de la imagen; mapas/limgrave_rejilla.jpg y mundo_rejilla.jpg)
L_VELO, L_AGHEEL, L_HAIGHT, L_PUENTE = (.42, .21), (.68, .37), (.945, .405), (.815, .585)
L_MORNE, L_CABANA, L_KENNETH, L_PASO = (.73, .905), (.575, .225), (.80, .31), (.64, .305)
M_VELO, M_LEYND, M_ALTUS, M_LIUR, M_CAEL, M_FARUM = (.36, .70), (.48, .41), (.37, .37), (.17, .60), (.60, .73), (.88, .48)

MIEMBROS = [("Hombres de Roderika", "brazos, piernas, cabezas"), ("Halcones de guerra", "sin garras"),
            ("Un dragón muerto", "en su propio brazo"), ("Tú", "la siguiente rama")]
HIJOS = [("Godrick", "el enclenque de la camada"), ("Godefroy", "encerrado para siempre")]

# Los 4 sonidos ORIGINALES con la voz callada (regla del 31-oct-2026; cortes en sfx/, −18 LUFS)
PISTAS = [
    dict(sfx="s_faraon", en="el narrador anterior sonaba así|fin", vol=1.0, voz=True),
    dict(sfx="s_kneel", en="Escúchalo de su boca|fin", vol=1.0, voz=True),
    dict(sfx="s_caceria", en="Traedme un Sinluz|fin", vol=1.0, voz=True),
    dict(sfx="s_branch", en="Escúchalo tú mismo|fin", vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    pant("vastago_foto", ("El primer jefe que te mató en Elden Ring", -.3), ("y un escudo dorado del linaje de Godfrey|fin", .2),
         zoom=(1.0, 1.12)),
    rel("un escudo dorado del linaje de Godfrey", "escudo_bestia", "Escudo dorado", "del linaje de Godfrey", dur=3.6, x=.78, y=.50),
    sil("salió del taller del hombre de hoy", _G("godrick_modelo"), "Godrick", "el Injertado", dur=5.0, lado="der", encuadre=(0, .5)),
    com("Justin nos dejó un comentario de cuatro palabras", C_JUSTIN, dur=5.4),
    com("Y Ádolf lo remató", C_ADOLF, dur=5.0, x=.70, y=.36),
    cam("Tu favorito", "godrick", "Godrick", dur=3.4, x=.80, y=.66),
    peg("Godrick el Injertado tiene fama de chiste", "godrick_f1", "Godrick el Injertado", tam=420, x=.20, y=.60),
    rel("el gordo de los brazos cosidos", "runa_godrick", "Gran Runa de Godrick", dur=4.0, x=.78, y=.52),
    aba([(_P("velo_carga"), "Un castillo"), (_G("caballero_godrick"), "Sus caballeros"), (_G("recuerdo_crisalidas"), "Una pila"),
         (_G("brazo_dragon"), "Un dragón")],
        ("Pero ese chiste tenía un castillo", -.2), ("a la que tú también ibas a ir a parar|fin", .5),
        ["un castillo lleno de miembros", "un trol crucificado", "una pila de cadáveres", "tú también ibas a ir a parar"],
        "chiste", x=.50, y=.62),
    puesto("Así que van las cinco peores atrocidades", "Las 5 peores atrocidades de", "Godrick", dur=4.4),
    mg(E.injerto(miembros=MIEMBROS[3:], titulo="Lo que tenía pensado", remate=""), ("Es lo que tenía pensado hacer contigo", -.3),
       ("Es lo que tenía pensado hacer contigo|fin", 1.6), ["hacer contigo"], "injerto gancho"),

    # ================================================================ VOTACIÓN DE VOCES
    mg(E.puesto("Algo ha cambiado", "La voz del canal"), ("Antes de empezar, algo ha cambiado", -.1), ("Y ya lo notaste|fin", .6),
       [], "cambio", y=.80),
    msg(["Lo de Miqueya y Mojé", "no tiene defensa."], ("Muchos de ustedes se quejaron de la voz", -.1),
        ("no tiene defensa|fin", .8), ["se quejaron de la voz", "no tiene defensa"], "quejas"),
    cam("un sistema de voz nuevo", "miquella", "Miquella", foco=(.45, .55, 1.7), dur=3.4, x=.16, y=.66),
    cam("Pero la decisión no es mía", "mohg", "Mohg", dur=3.4, x=.84, y=.66),
    mg(E.votacion(), ("Para que compares", -.2), ("y se queda en el canal|fin", 1.0),
       ["el narrador anterior sonaba así", "Y yo sueno así", "Escribe en los comentarios", "El que tenga más comentarios gana"],
       "votacion"),
    com("Diego escribió que en estos videos", C_DIEGO, dur=6.0),
    mg(E.puesto("Ganador imposible", "Loquendo"), ("Lo único que no puede ganar es Loquendo", -.1),
       ("y sigue sin presentarse|fin", .6), [], "loquendo", y=.80),
    com("Wolfdragon nos escribió", C_WOLF, dur=5.0, x=.30, y=.30),
    com("Y lksdmn pidió más videos", C_LKSDMN, dur=5.4, x=.70, y=.36),
    mg(E.puesto("Duración", "Veinticinco minutos"), ("Este dura veinticinco minutos", -.1), ("Ponte cómodo|fin", .8), [],
       "duracion", y=.80),

    # ================================================================ 5 · EL COBARDE DORADO
    puesto("Número cinco", "Atrocidad número 5", "El cobarde dorado"),
    pant("godrick_concepto", ("la guerra que estalló cuando se rompió", -.3), ("cada uno eligió un bando|fin", .3), zoom=(1.0, 1.10)),
    aba([(_G("malenia"), "Malenia"), (_G("radahn"), "Radahn"), (_G("mohg"), "Mohg"), (_G("ranni"), "Ranni")],
        ("Los semidioses se pelearon por los pedazos", -.2), ("y cada uno eligió un bando|fin", .5),
        ["se pelearon", "por los pedazos", "cada uno", "eligió un bando"], "semidioses", x=.50, y=.62, tam=270),
    sil("Kenneth Haight, el noble", _G("kenneth"), "Kenneth Haight", "el noble de Necrolimbo", dur=5.0, lado="der",
        encuadre=(0, .55)),
    mapa("limgrave", [(L_KENNETH[0], L_KENNETH[1], "Kenneth Haight", "Necrolimbo", _G("kenneth_cara")),
                      (.62, .26), (L_VELO[0], L_VELO[1], "Velo Tormentoso", "su escondite", _G("godrick"))],
         ("el noble que te encuentras en Necrolimbo", -.2), ("se escondió de Radahn en ese castillo|fin", 1.0),
         ["que te encuentras en Necrolimbo", "en ese castillo"], titulo="Necrolimbo", sub="Donde se esconde",
         ventana=True, x=.30, y=.40, traza=99),
    ficha("Primero se escondió entre las mujeres", "Kenneth Haight", "Primero se escondió *entre las mujeres* para huir de la "
          "capital. Luego se escondió de Radahn en ese castillo.", tipo="Lo que te cuenta",
          a=("se escondió de Radahn en ese castillo|fin", .4)),
    cam("se escondió de Radahn", "radahn", "Radahn", dur=3.4, x=.86, y=.74),
    pant("vastago_foto", ("en la sala del Vástago injertado", -.4), ("hay un cofre con el Velo de imitador|fin", .2),
         zoom=(1.0, 1.10)),
    rel("el Velo de imitador", "velo_imitador", "Velo de imitador", dur=5.0, x=.24, y=.52),
    ficha("Su descripción dice que, cuando a Godrick lo echaron", "Velo de imitador", "Cuando a Godrick lo echaron de Leyndell, "
          "*fue uno de los muchos tesoros que se llevó consigo*.", tipo="Herramienta", icono="velo_imitador",
          a=("que se llevó consigo|fin", .8)),
    mapa("mundo", [(M_LEYND[0], M_LEYND[1], "Leyndell", "la capital"), (.43, .52), (.40, .62),
                   (M_VELO[0], M_VELO[1], "Velo Tormentoso", "con el botín", _G("velo_imitador"))],
         ("Leyndell, la capital del reino", -.2), ("que se llevó consigo|fin", .8),
         ["Leyndell, la capital del reino", "que se llevó consigo"], titulo="Las Tierras Intermedias", sub="La huida",
         ventana=True, x=.30, y=.45, traza=99),
    rel("Las Cenizas de soldado de Godrick", "cenizas_soldado", "Cenizas de soldado de Godrick", dur=5.0, x=.76, y=.52),
    ficha("lo dicen claro", "Cenizas de soldado de Godrick", "Los soldados que sirven a Godrick el Injertado son *lo que queda "
          "del ejército que huyó* de la capital del Árbol Áureo.", tipo="Cenizas", icono="cenizas_soldado",
          a=("de la capital del Árbol Áureo|fin", .6)),
    sil("La Lectora de Dedos Enia", _G("enia"), "Enia", "Lectora de Dedos", dur=5.2, lado="izq", encuadre=(0, .55)),
    ficha("lo resume peor", "Enia · Lectora de Dedos", "No era más que un *pariente lejano*. El enclenque de la camada, con la "
          "sangre divina *muy diluida*.", tipo="Lo que te dice", a=("con la sangre divina muy diluida|fin", .6)),
    mg(E.linaje(hijos=HIJOS[:1], titulo="La sangre de Godfrey", remate=""), ("se sienta bajo una estatua de Godfrey", -.4),
       ("Y al que le habla mientras pelea|fin", .8),
       ["una estatua de Godfrey", "El antepasado al que no se parece", "Y al que le habla"], "linaje 1"),

    # ---- 5b · la humillación
    cam("Kenneth sigue", "kenneth_cara", "Kenneth", dur=3.4, x=.84, y=.66),
    peg("luego insultó a Malenia", "malenia", "Malenia", tam=420, x=.20, y=.60),
    ficha("le lamió las botas en vez de morir", "Kenneth Haight", "Insultó a Malenia, perdió contra ella y *le lamió las botas* "
          "en vez de morir como un hombre.", tipo="Lo que te cuenta", a=("morir como un hombre|fin", .5)),
    mg(E.puesto("En el japonés original", "Le lamió los dedos de los pies"), ("En el japonés original", -.1),
       ("y le juró obediencia|fin", .6), [], "japones pies", y=.80),
    mapa("limgrave", [(L_VELO[0], L_VELO[1], "Velo Tormentoso", "su castillo"), (.55, .30), (.62, .35),
                      (L_AGHEEL[0], L_AGHEEL[1], "Lago de Agheel", "el monumento", _P("monumento"))],
         ("Junto al Lago de Agheel", -.3), ("lo puedes leer|fin", .6), ["Junto al Lago de Agheel", "hay un monumento"],
         titulo="Lago de Agheel", sub="El monumento", entrada="desenrolla", traza=99),
    pant("monumento", ("La humillación de Godrick el Dorado", -.3), ("se arrodilla y suplica clemencia|fin", 1.0),
         zoom=(1.0, 1.14)),
    msg(["La humillación de Godrick el Dorado.", "Ahora se arrodilla y suplica clemencia."],
        ("La humillación de Godrick el Dorado", -.1), ("se arrodilla y suplica clemencia|fin", 1.4),
        ["La humillación de Godrick", "ahora se arrodilla"], "humillacion"),
    cam("bajo la espada de Miquella", "miquella", "Miquella", foco=(.45, .55, 1.7), dur=3.4, x=.84, y=.30),
    rel("el que en su pelea te ordena", "hacha", "Hacha de Godrick", dur=4.4, x=.76, y=.52),
    com("Y aquí, una aclaración para José", C_JOSE, dur=7.0),
    peg("el que la tenía de hija terminó podrido en Caelid", "radahn", "Radahn, en Caelid", tam=440, x=.78, y=.58),
    mapa("mundo", [(M_CAEL[0], M_CAEL[1], "Caelid", "podrido", _G("radahn"))], ("terminó podrido en Caelid", -.4),
         ("vagando sin juicio entre cadáveres|fin", 1.0), ["terminó podrido en Caelid"], titulo="Caelid", sub="Radahn",
         ventana=True, x=.28, y=.40, traza=99),
    grande("Se llama Godrick, y tiene monumento", "godrick", "Godrick el Dorado", lado="izq", dur=4.4, tam=640),
    ficha("Kenneth cierra su opinión", "Kenneth Haight", "Y pensar que es *sangre de Godfrey*. El último del linaje dorado.",
          tipo="Lo que te cuenta", a=("casi no lo dirías|fin", .5)),
    peg("Y pensar que es sangre de Godfrey", "godfrey", "Godfrey", tam=400, x=.20, y=.60),
    mg(E.injerto(miembros=MIEMBROS[:1], titulo="¿Y con su tiempo libre?", remate=""), ("Hasta que te preguntas qué hizo", -.3),
       ("en los cuatro puestos que quedan|fin", .8), ["escondido en su castillo"], "injerto tiempo"),

    # ================================================================ 4 · SUS FEUDOS DEL TERROR
    puesto("Número cuatro", "Atrocidad número 4", "Sus feudos del terror"),
    mapa("limgrave", [(L_VELO[0], L_VELO[1], "Velo Tormentoso", "su castillo"), (.62, .40), (L_PUENTE[0], L_PUENTE[1]),
                      (.80, .72), (L_MORNE[0], L_MORNE[1], "Castillo de Morne", "su feudo", _P("morne"))],
         ("Godrick no gobernaba solo Velo Tormentoso", -.3), ("está el Castillo de Morne|fin", .8),
         ["solo Velo Tormentoso", "está el Castillo de Morne"], titulo="Península del Llanto", sub="Sus feudos",
         entrada="mesa", traza=99),
    grande("soy Edgar, alcaide de este castillo", "edgar", "Edgar, alcaide de Morne", lado="izq", dur=5.0, tam=600),
    ficha("Y quien lo manda se presenta así", "Edgar", "Soy Edgar, alcaide de este castillo *por mandato del propio Lord "
          "Godrick*.", tipo="Lo que te dice", a=("por mandato del propio Lord Godrick|fin", .8)),
    pant("morne", ("Cuando llegas, Morne está en llamas", -.3), ("se han rebelado|fin", .4), zoom=(1.0, 1.12)),
    peg("Los Bastardos, esas criaturas peludas", "leonino", "Los Bastardos", tam=420, x=.78, y=.58),
    msg(["Me servían bien...", "o eso creía."], ("Edgar no lo entiende", -.1), ("o eso creía|fin", 1.0),
        ["Me servían bien", "o eso creía"], "servian"),
    rel("Un látigo", "latigo", "Látigo", dur=5.0, x=.76, y=.52),
    ficha("Su descripción no deja dudas", "Látigo", "Látigo de cuero que no se usaba para combatir, *sino como instrumento de "
          "dolor*.", tipo="Arma", icono="latigo", a=("sino como instrumento de dolor|fin", .8)),
    mg(E.puesto("Así los servían", "Esclavos con látigo"), ("Ese era el servicio", -.1), ("para que trabajaran|fin", .6), [],
       "servicio", y=.80),
    sil("te espera el Bastardo leonino", _G("leonino"), "Bastardo leonino", "el jefe de Morne", dur=5.0, lado="der",
        encuadre=(0, .5)),
    rel("La espada se llama Espadón de hoja injertada", "espadon_injertado", "Espadón de hoja injertada", dur=5.4, x=.24, y=.52),
    ficha("Hoy su descripción habla", "Espadón de hoja injertada", "Una espada hecha *uniendo las espadas de los guerreros que "
          "sirvieron a Godfrey*.", tipo="Primera versión (1.00)", icono="espadon_injertado",
          a=("Hasta las armas de su castillo estaban injertadas|fin", .6), y=.42),
    cortado(("en la primera versión del juego", -.2), ("que sirvieron a Godfrey|fin", .6), "Versión 1.00 del juego",
            "espadon"),
    com("Tristán nos escribió", C_TRISTAN, dur=4.2),
    mg(E.injerto(miembros=MIEMBROS[:2], titulo="Cada vez más cosidos", remate=""), ("Cada vez más miembros", -.4),
       ("Cada vez más cosidos|fin", 1.0), ["Cada vez más miembros", "Cada vez más cosidos"], "injerto tristan"),

    # ---- 4b · Irina, Edgar y Haight
    sil("Irina, la hija de Edgar", _G("irina"), "Irina", "la hija de Edgar", dur=5.0, lado="izq", encuadre=(0, .5)),
    mapa("limgrave", [(L_MORNE[0], L_MORNE[1], "Castillo de Morne", "Edgar"), (.80, .72),
                      (L_PUENTE[0], L_PUENTE[1], "Puente del Sacrificio", "Irina", _G("irina_cara"))],
         ("Una chica ciega que encuentras junto al Puente del Sacrificio", -.3), ("con una carta para su padre|fin", .6),
         ["Una chica ciega", "junto al Puente del Sacrificio"], titulo="Puente del Sacrificio", sub="Irina",
         ventana=True, margen=.2, ajuste=.95, traza=99),
    pant("edgar_irina", ("Y la siguiente vez que pasas por el puente", -.3), ("Irina está muerta|fin", 1.4), zoom=(1.0, 1.10),
         oscuro=.1),
    ficha("Edgar lo reconoce, roto", "Edgar", "*Elegí el deber* antes que la seguridad de mi hija.", tipo="Lo que te dice",
          a=("la seguridad de mi hija|fin", .8)),
    mapa("mundo", [(.40, .88, "Morne", "su castillo"), (.30, .78), (.22, .68),
                   (M_LIUR[0], M_LIUR[1], "Choza del Vengador", "Liurnia", _G("edgar"))],
         ("te invade en la Choza del Vengador", -.3), ("un vengador|fin", .8), ["Más adelante enloquece", "en Liurnia"],
         titulo="Liurnia de los Lagos", sub="El vengador", entrada="foco", traza=99),
    mapa("limgrave", [(L_MORNE[0], L_MORNE[1], "Morne"), (.86, .62), (L_HAIGHT[0], L_HAIGHT[1], "Fuerte de Haight",
                                                                         "la costa este", _G("kenneth_cara"))],
         ("Igual que el Fuerte de Haight", -.3), ("el fuerte de la familia de Kenneth|fin", .6),
         ["Igual que el Fuerte de Haight", "la familia de Kenneth"], titulo="Fuerte de Haight", sub="Otra pieza del mapa",
         ventana=True, x=.30, margen=.2, ajuste=.95, traza=99),
    ficha("Kenneth te cuenta quién se lo quitó", "Kenneth Haight", "Un caballero comandante de Velo Tormentoso. Un necio, y *loco "
          "de remate*. Obsesionado con la sangre.", tipo="Lo que te cuenta", a=("Obsesionado con la sangre|fin", .6)),
    sil("el comandante usa Tajo sangriento", _G("comandante_haight"), "Caballero comandante", "Fuerte de Haight", dur=5.0,
        lado="izq", encuadre=(0, .5)),
    rel("la Exultación del Señor de la Sangre", "exaltacion", "Exultación del Señor de la Sangre", dur=5.0, x=.80, y=.50),
    cam("El talismán de Mohg", "mohg", "Mohg", dur=3.6, x=.16, y=.30),
    com("Por cierto, Gonzalo", C_GONZALO, dur=7.0),
    cam("controlado por Miquella", "miquella", "Miquella", foco=(.45, .55, 1.7), dur=3.4, x=.84, y=.66),
    rel("este caballero nunca vio a Miquella", "exaltacion", "Al cuello, en Necrolimbo", dur=4.4, x=.24, y=.52),
    mg(E.puesto("Ni tan mal", "Ni tan mojado"), ("Ni tan mal, dice", -.1), ("está ni tan mojado|fin", 1.0), [], "ni tan mal",
       y=.80),
    aba([(_G("latigo"), "Esclavos con látigo"), (_G("comandante_haight"), "El comandante"),
         (_G("irina_cara"), "Una chica ciega")],
        ("Esclavos con látigo en Morne", -.2), ("muerta en un puente|fin", .6),
        ["Esclavos con látigo", "Un comandante adorador", "Y una chica ciega"], "reino", x=.50, y=.62),
    mg(E.puesto("Y todavía", "No hemos entrado"), ("Ese era el reino de Godrick", -.1), ("todavía no hemos entrado en su castillo|fin", .8),
       [], "castillo", y=.80),

    # ================================================================ 3 · EL DRAGÓN Y SU PROPIO BRAZO
    puesto("Número tres", "Atrocidad número 3", "El dragón y su brazo"),
    sil("Varré, el del Rostro Alabastrado", _G("varre"), "Varré", "el Rostro Alabastrado", dur=5.0, lado="izq", encuadre=(0, .5)),
    ficha("te avisa", "Varré", "Dicen que el viejo Godrick tiene *un juguete nuevo y feroz* que injertarse.", tipo="Lo que te dice",
          a=("prepárate para lo peor|fin", .6)),
    pant("dragon_estatua", ("El juguete está en la arena", -.3), ("atravesado de lado a lado|fin", .6), zoom=(1.0, 1.12)),
    peg("hay un dragón muerto, atravesado", "dragon_empalado", "El dragón empalado", tam=440, x=.78, y=.56),
    ficha("Poderoso dragón, eres un heredero de verdad", "Godrick · a la estatua", "Poderoso dragón, *eres un heredero de "
          "verdad*. Préstame tu fuerza.", tipo="Lo que dice", a=("Préstame tu fuerza|fin", .6)),
    mg(E.puesto("En japonés", "Dragón, descendiente como yo"), ("En japonés, la frase es más reveladora", -.1),
       ("descendiente como yo|fin", .8), [], "japones dragon", y=.80),
    sil("Un Sinluz miserable, jugando a ser señor", _G("godrick_modelo"), "Godrick", "el Injertado", dur=5.0, lado="izq",
        encuadre=(0, .5)),
    rel("la frase que lleva grabada su propia hacha", "hacha", "Hacha de Godrick", dur=4.4, x=.76, y=.52),
    msg(["¡Te ordeno que te arrodilles!", "¡Soy señor de todo cuanto es dorado!"], ("en la traducción oficial", -.1),
        ("Escúchalo de su boca|fin", .2), ["Te ordeno que te arrodilles", "Soy señor de todo cuanto es dorado"], "kneel es"),
    ficha("Escúchalo de su boca|fin", "Godrick · al empezar la pelea", "*I command thee, kneel!* I am the lord of all that is "
          "golden!", tipo="Voz original", a=("Escúchalo de su boca|fin", 11.4)),

    # ---- 3b · se corta el brazo
    mg(E.injerto(miembros=MIEMBROS[2:3], titulo="Lo que hace siempre", remate=""), ("Busca algo de otro para pegárselo", -.3),
       ("Busca algo de otro para pegárselo|fin", 1.4), ["algo de otro"], "injerto pierde"),
    peg("en el muñón se cose la cabeza del dragón", "brazo_dragon", "La cabeza del dragón, cosida", tam=460, x=.22, y=.58),
    ficha("el más auténtico de los dragones", "Godrick · fase 2", "Ahh, el más auténtico de los dragones, préstame tu fuerza. "
          "Antepasados, todos vosotros. *Sed testigos*.", tipo="Lo que dice", a=("Sed testigos|fin", .6)),
    rel("La descripción del Dragón injertado", "dragon_arma", "Dragón injertado", dur=5.0, x=.24, y=.52),
    ficha("el arma que sale de su recuerdo", "Dragón injertado", "La encarnación del poder que aún quedaba en la *cabeza de "
          "dragón injertada* en el brazo izquierdo de Godrick.", tipo="Arma · habilidad «Sed testigos»", icono="dragon_arma",
          a=("Y su habilidad se llama Sed testigos|fin", .8)),
    rel("el arma que sale de su recuerdo", "recuerdo_injertado", "Recuerdo del Injertado", dur=3.8, x=.76, y=.62, tam=380),
    mg(E.injerto(miembros=MIEMBROS[:3], titulo="Fíjate en lo que está pasando", remate=""), ("Un hombre que se mutila delante de ti", -.3),
       ("Y lo usa para escupir fuego|fin", .8), ["Un hombre que se mutila", "delante de ti", "el cadáver de una criatura"],
       "injerto dragon"),
    peg("Diego, también preguntaste para cuándo los dragones", "dragon_empalado", "El dragón que hay", tam=440, x=.20, y=.58),
    mg(E.puesto("Pedido de Diego", "Un dragón, cosido"), ("Aquí tienes uno", -.1), ("pero es el dragón que hay|fin", .6), [],
       "diego dragon", y=.80),
    ficha("Le habla a la estatua del trono", "Godrick · al matarte", "*Gran Godfrey*, ¿lo has visto?", tipo="Lo que dice",
          dur=5.0),
    grande("Todo lo que hace es para un antepasado", "godfrey", "Godfrey, primer Señor del Círculo", lado="der", dur=4.6, tam=600),

    # ---- 3c · Godefroy
    mapa("mundo", [(M_VELO[0], M_VELO[1], "Velo Tormentoso"), (.38, .55), (.40, .45),
                   (M_ALTUS[0], M_ALTUS[1], "Cárcel eterna", "del linaje dorado", _G("godefroy"))],
         ("En la Meseta Altus, al sur", -.3), ("La del linaje dorado|fin", .8), ["En la Meseta Altus", "La del linaje dorado"],
         titulo="Meseta de Altus", sub="La cárcel eterna", entrada="desenrolla", traza=99),
    sil("Se llama Godefroy, el Injertado", _G("godefroy"), "Godefroy", "el Injertado", dur=5.2, lado="der", encuadre=(0, .5)),
    mg(E.linaje(hijos=HIJOS, titulo="La sangre de Godfrey", remate="Los dos se injertaban"),
       ("El juego no dice exactamente qué parentesco", -.4), ("y que también se injertaba|fin", 1.0),
       ["exactamente", "qué parentesco", "con Godrick#2", "era de su sangre", "también se injertaba"], "linaje 2"),
    rel("Lo que sí cuenta son las Cenizas de Kristoff", "kristoff", "Cenizas de Kristoff", dur=5.0, x=.24, y=.52),
    ficha("Tras la primera defensa de Leyndell", "Cenizas de Kristoff", "Se ganó el honor de un entierro en el Árbol Áureo *por "
          "capturar a Godefroy el Injertado*.", tipo="Cenizas", icono="kristoff", a=("capturar a Godefroy el Injertado|fin", .8)),
    rel("deja caer el Icono de Godfrey", "icono_godfrey", "Icono de Godfrey", dur=4.6, x=.76, y=.52),
    mg(E.puesto("Otra vez", "Todo vuelve a Godfrey"), ("Otra vez, todo vuelve a Godfrey", -.1),
       ("todo vuelve a Godfrey|fin", .5), [], "godfrey", y=.80),
    mg(E.linaje(hijos=HIJOS, titulo="El linaje dorado", remate="El que más lejos llegó: Godrick"),
       ("El linaje dorado no solo perdió su gracia", -.4), ("es el que más lejos llegó|fin", 1.2),
       ["El linaje dorado", "perdió su gracia", "coserse a otros", "el enclenque de la camada#2", "el que más lejos llegó"],
       "linaje 3"),

    # ================================================================ 2 · LOS HOMBRES DE RODERIKA
    puesto("Número dos", "Atrocidad número 2", "Hombres de Roderika"),
    mapa("limgrave", [(L_PASO[0], L_PASO[1], "Primera gracia", "inicio"), (.60, .26),
                      (L_CABANA[0], L_CABANA[1], "Cabaña de la Colina", "Roderika", _G("roderika")), (.50, .22),
                      (L_VELO[0], L_VELO[1], "Velo Tormentoso", "el castillo")],
         ("En la Colina Tormentosa", -.3), ("Se llama Roderika|fin", .6),
         ["En la Colina Tormentosa", "en una cabaña junto al camino", "al castillo"], titulo="Colina Tormentosa",
         sub="La cabaña", traza=99),
    sil("Viene de otra tierra", _G("roderika"), "Roderika", "viene de otra tierra", dur=5.4, lado="izq", encuadre=(0, .55)),
    ficha("te dice lo que pasó con los demás", "Roderika", "*A todos los injertaron.* A todos los que vinieron conmigo. Cruzaron "
          "el mar por mí. Lucharon por mí.", tipo="Lo que te dice", a=("Lucharon por mí|fin", .6)),
    mg(E.injerto(centro="La araña", sub_centro="el Vástago injertado", miembros=[("Brazos", None), ("Piernas", None),
                                                                                 ("Cabezas", None)],
                 titulo="Se los pegaron a la araña", remate=""),
       ("Solo para que les quitaran los brazos", -.2), ("y se los pegaron a la araña|fin", 1.0),
       ["los brazos#2", "Las piernas", "Hasta la cabeza"], "injerto arana"),
    msg(["¿Sabías que si la araña te injerta", "te conviertes en crisálida?"], ("Y añade, como si no pesara nada", -.1),
        ("Tiene gracia, si lo piensas|fin", .8), ["sabías que si la araña", "te conviertes en crisálida"], "crisalida"),
    pant("vastago_foto", ("La araña es el Vástago injertado", -.3), ("rostro de joven noble y pelo plateado|fin", .5),
         zoom=(1.0, 1.12)),
    mg(E.puesto("En japonés", "El príncipe injertado"), ("En japonés, su nombre significa", -.1), ("el príncipe injertado|fin", 1.0),
       [], "principe", y=.80),
    msg(["Las wikis lo atribuyen a Godrick.", "El juego nunca lo dice."], ("Las wikis lo atribuyen a la técnica", -.1),
        ("nunca lo dice con esas palabras|fin", .6), ["Las wikis lo atribuyen", "nunca lo dice"], "wikis"),
    cam("Roderika no fue injertada", "roderika", "Roderika", dur=3.6, x=.16, y=.66),
    ficha("Da miedo, ¿sabes?", "Roderika", "Que te corten los brazos. O las piernas. O la cabeza. *Quiero ser como los demás*, "
          "pero me da demasiado miedo.", tipo="Lo que te dice", a=("me da demasiado miedo|fin", .6)),
    msg(["Diles que los quiero."], ("Y te hace un encargo", -.1), ("Diles que los quiero|fin", .8), ["Diles que los quiero"],
        "encargo"),
    ficha("aunque tenga un corazón cobarde", "Roderika", "Y que, aunque tenga un corazón cobarde, *seguro que pronto me uniré a "
          "su club*.", tipo="Lo que te dice", a=("me uniré a su club|fin", .8)),

    # ---- 2b · el club
    mapa("limgrave", [(L_CABANA[0], L_CABANA[1], "Cabaña", "Roderika"), (.48, .21),
                      (L_VELO[0] + .01, L_VELO[1] + .01, "Torre de defensa", "la pila", _G("recuerdo_crisalidas"))],
         ("Lo encuentras en Velo Tormentoso", -.3), ("Y encima, un trol crucificado|fin", .4),
         ["en Velo Tormentoso", "cerca de la Torre de defensa"], titulo="Velo Tormentoso", sub="El club", ventana=True,
         x=.28, traza=99),
    rel("Bajo el trol, tirado entre los muertos, hay un broche", "recuerdo_crisalidas", "Recuerdo de las crisálidas", dur=5.0,
        x=.76, y=.52),
    ficha("Su descripción: recuerdo que dejaron", "Recuerdo de las crisálidas", "Recuerdo que dejaron las *crisálidas "
          "sacrificadas para el injerto*. Un broche envuelto en terciopelo rojo, con restos de sangre.", tipo="Objeto clave",
          icono="recuerdo_crisalidas", a=("Pero no se oyen sus voces|fin", .8)),
    msg(["Espíritus apenas visibles intentan decir algo.", "Pero no se oyen sus voces."],
        ("Espíritus apenas visibles intentan decir algo", -.1), ("Pero no se oyen sus voces|fin", 1.0),
        ["Espíritus apenas visibles", "Pero no se oyen"], "espiritus"),
    rel("Y para los halcones de guerra del castillo", "halcon", "Cenizas de halcón de guerra", dur=5.0, x=.24, y=.52),
    ficha("Sus cenizas cuentan que les cortaron las garras", "Cenizas de halcón de guerra", "Les cortaron las garras *para "
          "injertarles espadas finísimas* en su lugar.", tipo="Cenizas", icono="halcon", a=("en su lugar|fin", .6)),
    mg(E.injerto(miembros=MIEMBROS[:2], titulo="El club", remate=""), ("Eso es lo que queda de los hombres", -.3),
       ("debajo de un trol|fin", .6), ["Un broche#3", "debajo de un trol"], "injerto club"),
    cam("ya se ha convertido en afinadora de espíritus", "roderika", "Roderika, afinadora", dur=3.8, x=.84, y=.66),
    mapa("mundo", [(M_VELO[0], M_VELO[1], "Velo Tormentoso", "la pila"), (.60, .60),
                   (M_FARUM[0], M_FARUM[1], "Farum Azula", "al final del juego")],
         ("al llegar a Farum Azula", -.3), ("en esa misma pila de cadáveres|fin", .6), ["al llegar a Farum Azula", "aparece algo nuevo"],
         titulo="Farum Azula", sub="El final del viaje", ventana=True, traza=99),
    grande("Su capucha carmesí", "capucha", "Capucha carmesí", lado="der", dur=5.6, tam=620),
    cam("La de Roderika", "roderika", "Roderika", dur=4.4, x=.16, y=.66),
    msg(["Solo deja su ropa", "donde están los suyos."], ("El juego no dice qué le pasó", -.1),
        ("donde están los suyos|fin", 1.2), ["El juego no dice#2", "Solo deja su ropa"], "ropa"),
    com("Amand escribió que cuando crees", C_AMAND, dur=7.0),
    mg(E.cien("De cada 100 que ven el canal", 4, remate=("Menos de cinco, suscritos", 1)), ("De cada cien personas", -.2),
       ("y la meta es mil|fin", .6), ["De cada cien personas", "menos de cinco"], "cien", y=.46),
    com("Gun-chikito nos escribió", C_GUN, dur=5.0, x=.30, y=.30),
    mg(E.puesto("Suscríbete", "740 → 1 000"), ("Si llegaste hasta aquí", -.1), ("No pide injertarte nada|fin", .8), [],
       "suscripcion", y=.80),

    # ================================================================ 1 · TÚ ERAS EL INGREDIENTE
    puesto("Número uno#3", "Atrocidad número 1", "Tú eras el ingrediente"),
    sil("Varré te recibe en Necrolimbo", _G("varre"), "Varré", "te manda a Godrick", dur=5.0, lado="izq", encuadre=(0, .5)),
    mapa("limgrave", [(L_PASO[0], L_PASO[1], "Primera gracia", "Varré", _G("varre")), (.58, .27),
                      (L_VELO[0], L_VELO[1], "Velo Tormentoso", "a Godrick")],
         ("y te manda allí", -.3), ("donde la gracia te guía|fin", .8), ["y te manda allí", "a Godrick#5"],
         titulo="Necrolimbo", sub="El camino", ventana=True, x=.74, traza=99),
    ficha("cuando le cuentas de dónde vienes", "Roderika", "Te convenció *el de la máscara blanca*, supongo.", tipo="Lo que te dice",
          a=("supongo|fin", .6)),
    msg(["El mismo camino.", "El mismo castillo.", "El mismo final."], ("El mismo camino", -.1), ("el mismo final|fin", 1.2),
        ["El mismo camino", "el mismo castillo", "el mismo final"], "mismo"),
    cam("Kenneth Haight: yo de ti", "kenneth_cara", "Kenneth Haight", dur=3.6, x=.16, y=.66),
    ficha("me cuidaría mucho de las cacerías", "Kenneth Haight", "Esa panda de depravados está obsesionada con *sacrificar a "
          "Sinluz como tú* en nombre del injerto.", tipo="Lo que te cuenta", a=("en nombre del injerto|fin", .6)),
    mg(E.puesto("En japonés", "Ofrendas para su injerto"), ("En japonés, lo dice más claro", -.1), ("su abominable injerto|fin", .8),
       [], "ofrendas", y=.80),
    sil("Y Rogier, el hechicero", _G("rogier"), "Rogier", "el hechicero", dur=5.0, lado="izq", encuadre=(0, .5)),
    ficha("lo repite", "Rogier", "Este sitio está plagado de *cazadores de Sinluz*. Sacrifican a los nuestros para injertarlos.",
          tipo="Lo que te dice", a=("para injertarlos|fin", .6)),
    peg("Godrick reúne a sus caballeros", "caballero_godrick", "Caballeros de Godrick", tam=420, x=.20, y=.60),
    cortado(("En los archivos del juego hay un monólogo", -.2), ("Traedme un Sinluz|fin", 12.4), "Monólogo de la cacería",
            "caceria"),
    ficha("Pide una rama poderosa", "Godrick · monólogo cortado", "Una *rama poderosa*, una ofrenda fresca que injertar. "
          "Traedme un Sinluz.", tipo="No llegó al juego", dur=6.0, y=.40),
    msg(["«Fetch me a mighty branch...", "Bring me a Tarnished!»"], ("Traedme un Sinluz|fin", .3), ("Traedme un Sinluz|fin", 12.2),
        [], "fetch"),

    # ---- 1b · la rama y Gostoc
    mg(E.puesto("Tsugiki", "Una rama para injertar"), ("Su nombre japonés, tsugiki", -.1), ("injerto de árboles|fin", 1.0), [],
       "tsugiki", y=.80),
    mg(E.injerto(miembros=MIEMBROS, titulo="Eres una rama", remate=""), ("Para Godrick, tú no eres un rival", -.3),
       ("Eres una rama|fin", 1.2), ["Para Godrick, tú no eres", "Para Godrick, tú no eres", "tú no eres un rival", "Eres una rama"],
       "injerto rama"),
    pant("gostoc_foto", ("Gostoc, el guardián", -.3), ("te roba las runas|fin", .3), zoom=(1.0, 1.10)),
    sil("Te abre una entrada lateral", _G("gostoc"), "Gostoc", "el guardián", dur=5.0, lado="izq", encuadre=(0, .5)),
    ficha("Si lo espías, lo encuentras revolviendo cadáveres", "Gostoc", "Basura. Otro que es todo piel y huesos. Ahh, *este "
          "tampoco tiene ni un músculo*.", tipo="Lo que dice", a=("ni un músculo|fin", .6)),
    msg(["Tranquilo, tengo grandes planes", "para lo que queda de ti."], ("Y si te mata, te consuela", -.1),
        ("para lo que queda de ti|fin", 1.0), ["tengo grandes planes", "para lo que queda de ti"], "planes"),
    cortado(("en los archivos cortados del juego", -.2), ("Escúchalo tú mismo|fin", 8.5), "Gostoc, hijo de Godrick", "gostoc"),
    ficha("Gostoc tenía otra presentación", "Gostoc · línea cortada", "Soy *hijo de Godrick*, sin duda. Elegido por la sangre para "
          "injertar.", tipo="No llegó al juego", a=("para injertar|fin", .8), y=.40),
    cam("Soy hijo de Godrick, sin duda", "godrick", "Godrick", dur=3.6, x=.16, y=.66),
    msg(["«A fine branch...", "Begin the graft!»"], ("Escúchalo tú mismo|fin", .3), ("Escúchalo tú mismo|fin", 8.3), [], "branch"),

    # ---- 1c · no vales ni para injertarte
    mg(E.puesto("Así te veían", "Una rama magnífica"), ("Una rama magnífica", -.1), ("Así te veían en Velo Tormentoso|fin", .8), [],
       "rama magnifica", y=.80),
    grande("Si Godrick te mata en la primera fase", "godrick_f1", "Godrick · primera fase", lado="der", dur=4.6, tam=620),
    msg(["Sinluz miserable.", "No vales ni para injertarte."], ("te lo dice a la cara", -.1), ("No vales ni para injertarte|fin", 1.2),
        ["Sinluz miserable#2", "No vales ni para injertarte"], "no vales"),
    aba([(_G("roderika"), "Los de Roderika"), (_G("halcon"), "Los halcones"), (_G("dragon_empalado"), "El dragón muerto")],
        ("Los hombres de Roderika sirvieron", -.2), ("El dragón muerto sirvió|fin", .6),
        ["Los hombres de Roderika#2", "Los halcones#2", "El dragón muerto"], "sirvieron", x=.50, y=.62),
    mg(E.puesto("Y tú", "No servías para nada"), ("Y tú, según él", -.1), ("no servías para nada|fin", .8), [], "nada", y=.80),
    pant("vastago_foto", ("A la Capilla de la espera", -.3), ("La que te arrastró a la Tumba abandonada|fin", .4),
         zoom=(1.0, 1.12), oscuro=.05),
    msg(["Las obras del injerto", "del linaje dorado."], ("Las wikis la cuentan entre las obras", -.1),
        ("del linaje dorado#3|fin", .1), ["Las wikis la cuentan", "del linaje dorado#3"], "obras"),
    mg(E.injerto(miembros=MIEMBROS, titulo="Un producto terminado", remate="Y tú eras la siguiente materia prima"),
       ("Tu primera muerte en Elden Ring", -.3), ("la siguiente materia prima|fin", 1.4),
       ["Tu primera muerte", "Elden Ring#2", "un producto", "terminado", "la siguiente materia prima"], "injerto producto"),
    rel("Sus últimas palabras las repite su recuerdo", "recuerdo_injertado", "Recuerdo del Injertado", dur=5.0, x=.24, y=.52),
    ficha("algún día volveremos juntos", "Recuerdo del Injertado", "Algún día volveremos juntos a nuestro *hogar bañado en rayos "
          "de oro*.", tipo="Recuerdo", icono="recuerdo_injertado", a=("bañado en rayos de oro|fin", .8)),
    peg("En japonés, se lo dice a sus soldados", "caballero_godrick", "Sus soldados", tam=400, x=.78, y=.60),

    # ================================================================ CIERRE
    aba([(_P("velo_carga"), "El botín"), (_G("latigo"), "El látigo"), (_G("brazo_dragon"), "El dragón"),
         (_G("recuerdo_crisalidas"), "El séquito"), (_G("godrick"), "Tú")],
        ("Esa es la lista", -.2), ("como a una rama más|fin", .8),
        ["Huye de todas las guerras#2", "Gobierna esclavos con látigo", "Se corta su propio brazo", "Convierte un séquito entero",
         "Y te espera en su castillo"], "lista", x=.50, y=.62, tam=270),
    grande("fue el único que te mandaron a matar primero", "godrick", "Godrick, el primero", lado="izq", dur=4.6, tam=620),
    mg(E.puesto("El débil", "También tenía hambre"), ("Lo que nadie te dijo", -.1), ("también tenía hambre|fin", 1.0), [], "hambre",
       y=.80),
    com("una respuesta para Madrizu", C_MADRIZU, dur=7.4),
    cam("Lo de Ranni no lo retiro", "ranni", "Ranni", dur=3.8, x=.84, y=.66),
    peg("donde murió Godwyn", "godwyn", "Godwyn", tam=400, x=.20, y=.60),
    mg(E.puesto("La atrocidad", "Es la mía, por contarlo"), ("Pero claro, la atrocidad es la mía", -.1), ("por contarlo|fin", 1.0),
       [], "atrocidad mia", y=.80),
    msg(["Los comentarios se leen todos."], ("Los comentarios se leen todos", -.1), ("vamos mejorando el canal|fin", .6),
        ["Los comentarios se leen todos"], "se leen"),
    com("Este video existe porque Justin y Ádolf", C_JUSTIN, dur=4.6, x=.28, y=.30, tam=640),
    com("y Ádolf lo pidieron", C_ADOLF, dur=4.2, x=.72, y=.40, tam=640),
    mg(E.votacion(titulo="No te olvides de votar"), ("Así que no te olvides de votar", -.2), ("El que tenga más comentarios se queda|fin", 1.2),
       ["no te olvides de votar", "Narrador anterior#3", "o nuevo profeta#2", "El que tenga más comentarios se queda"], "votacion cierre"),
    aba([(_G("godfrey"), "Godfrey"), (_G("godwyn"), "Godwyn"), (_G("messmer"), "Messmer"), (_G("rennala"), "Rennala")],
        ("Ya están apuntados Godfrey y Godwyn", -.2), ("y hasta Bayle el Temible|fin", .6),
        ["Godfrey#8", "y Godwyn", "Messmer, que piden", "Rennala"], "apuntados", x=.50, y=.62),
    mg(E.puesto("Y hasta", "Bayle el Temible"), ("y hasta Bayle el Temible", -.1), ("Dinos cuál quieres que sea el siguiente|fin", .6),
       [], "bayle", y=.80),
    aba([(_G("marika"), "Márika y Radagon"), (_G("miquella"), "Miquella"), (_G("malenia"), "Malenia"), (_G("ranni"), "Ranni"),
         (_G("radahn"), "Radahn"), (_G("mohg"), "Mohg")],
        ("En el canal tienes las atrocidades de Márika", -.2), ("Morgott y Mohg|fin", .6),
        ["de Márika y Radagon", "de Miquella#2", "Malenia#4", "Ranni#4", "Radahn#3", "Morgott y Mohg"], "en el canal",
        x=.50, y=.62, tam=260),
    mg(E.puesto("Suscríbete", "Rumbo a los 1 000"), ("Y si te suscribes", -.1), ("nos acercas a los mil|fin", .8), [],
       "suscribete", y=.80),
    pant("vastago_foto", ("la próxima vez que un Vástago injertado te mate", -.3), ("recuerda de dónde viene|fin", .4),
         zoom=(1.0, 1.10)),
    grande("para Godrick, ni siquiera valías como rama", "godrick_modelo", "Godrick el Injertado", lado="der", dur=4.6, tam=640),
]
