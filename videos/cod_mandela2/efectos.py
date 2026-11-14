# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 EFECTOS MANDELA de Call of Duty que TÚ recordaste (parte 2)» (SECUENCIA YT, Expediente 141, 13-nov-2026).
Helpers de videos/cod_misterios/efectos.py (kit nucleo/mg_cod.py + peg_estilos/peg_anim/presenta con tema «cod»).
MG propios de este guion: `C.fusion` (dos recuerdos reales → el recuerdo falso: Weaver+Pyle, AUG+MTAR, Downhill+Alpine, Verrückt+Kino)
y `C.caso(..., "falso" | "a_medias")` al cierre de cada puesto. Sonidos nombrados: PISTAS voz=True con sfx/s_*.mp3.
    python fab.py cod_mandela2 fx --seco   tiempos      FAB_FX_FINAL=1 python fab.py cod_mandela2 fx hoja   previews/fx_NN.jpg
"""
import os

import mg_cod as C
import mg_wow as W
import peg_estilos as PE

TEMA = "cod"
CAMARA = {}
FUNDIDO = {}

_FX, _FY = .75, .30            # fichas: arriba a la derecha
_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_MAPA = "cod"


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    return os.path.join(_PEG, slug + ".png")


def ficha(en, titulo, texto, tipo=None, dur=4.0, x=.27, y=.28, ancho=640):
    return dict(tipo="mg", fn=C.ficha(titulo, texto, tipo, ancho=ancho), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + titulo, ver=1.2)


def peg(en, slug, titulo, dur=3.4, x=.17, y=.64, tam=380, giro=-5.0):
    return dict(tipo="mg", fn=C.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def pv(en, slug, titulo, dur=3.6, x=.17, y=.62, tam=400, **anim):
    """Pegatina con marco + entrada + estancia + salida que rotan (catálogo 5-nov-2026)."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(P(slug), titulo, tam, tema=TEMA, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila([(P(s), e) for s, e in fotos], tam, TEMA, marco), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.06, nombre="pegatina pila " + nombre, ver=2.0)


def sil(en, slug, nombre=None, sub=None, dur=4.2, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=3.8, x=.77, y=.52, tam=440):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.0, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.2, x=.16, y=.66, tam=300, foco=(.5, .3, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.78, y=.52, ancho=460, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.64, tam=280):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.4, sale=.4,
                nombre="pantalla " + slug, ver=2.0)


def puesto(en, n, titulo, sub, dur=4.2):
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub, total=20), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


def mg(fn, de, a, marcas, nombre, x=.5, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def caso(en, estado, titulo, sub=None, dur=3.2, x=.72, y=.26):
    """Veredicto del expediente (MG propio de este guion): al cerrar cada puesto."""
    return mg_en(C.caso(estado, titulo, sub), en, dur, "caso " + titulo, x=x, y=y)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def vid(n, de, a, desde=0.0, recorte=0.0):
    """Corte rápido con OTRO clip ya bajado (medios/scene-NNN.mp4) a cuadro entero (va PRIMERO en FX)."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", f"scene-{n:03d}.mp4"), de=de, a=a, desde=desde,
                recorte=recorte, entra=.12, sale=.12, nombre=f"corte clip {n:03d}")


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    fx = dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)
    if kw.get("entrada"):
        fx["entra"] = fx["sale"] = .05
    return fx


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def tabl(fotos, hilos, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.tablero(_f(fotos), hilos, titulo, TEMA), de, a, marcas, "tablero")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA, titulo), de, a, marcas, "versus")


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro(_f(fotos), tema=TEMA, destaca=destaca, titulo=titulo), de, a, marcas, "muro")



FX = [
    # ---------------- gancho: un elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.33, y=.42),
    leg("c_cod4", "EXPEDIENTE 141 · PARTE 2", ["Asunto: tu memoria", "20 efectos Mandela", "4 los mandaste tú"],
        de="Asunto: tu memoria", a=("En el expediente anterior les", -.1), x=.78, y=.50),
    mg_en(C.objetivo("Mándame tus efectos Mandela", "Expediente anterior"), "les pedí sus efectos Mandela", 2.6, "objetivo pedido", x=.30, y=.82),
    pv("la AUG en la granja de Zombies", "aug", "¿La AUG en la Granja?", dur=2.6, x=.80, y=.62, tam=330),
    pv("una frase de Alex Mason", "mason", "Alex Mason", dur=2.6, x=.18, y=.64, tam=320),
    pv("un Black Ops que salió", "c_bo1", "¿Black Ops en 2007?", dur=2.6, x=.80, y=.62, tam=320),
    mg_en(C.objetivo("Revisar cada recuerdo", "Con el juego en pantalla", completo=True), "Los revisé todos", 2.6, "objetivo revisar",
          x=.30, y=.82),
    caso("tiene razón. A medias", "a_medias", "Uno de ustedes", "Lo verás en el número seis", dur=2.6),
    sil("escucha al sargento Gaz", "gaz", "Gaz", "SAS · Call of Duty 4", lado="der", dur=4.4),
    pv(("de Call of Duty 4.|fin", .2), "fng", "F.N.G. · el campo de tiro", dur=2.8, x=.16, y=.66, tam=280),
    mg_en(C.radio("GAZ", "«Remember, switching to your…»", "ENTRENAMIENTO / F.N.G."), ("de Call of Duty 4.|fin", -.1), 3.2,
          "radio gaz corto", x=.5, y=.26),
    mg_en(C.objetivo("Completa la frase", "¿Sidearm? ¿Secondary?"), "Cómo termina esa frase", 3.0, "objetivo frase", x=.30, y=.82),
    pv("Medio internet también", "infinityward", "Infinity Ward · 2007", dur=2.6, x=.80, y=.62, tam=300),
    mg_en(C.marcador("Número 1", 20, "Al final del expediente"), "Te lo enseño en el número", 2.6, "marcador numero uno", x=.55, y=.36),
    mg_en(C.contador(20, "EFECTOS MANDELA", "PARTE 2"), "Veinte efectos Mandela de Call", 2.8, "contador 20", x=.30, y=.30),
    mg_en(C.logro("4 efectos son tuyos", "Llegaron por los comentarios"), "cuatro me los mandaste", 3.0, "logro cuatro", x=.5, y=.84),

    # ---------------- 20 · la bomba
    puesto("Número veinte", 20, "La bomba que nunca desactivaste", "CAMPAÑA / CALL OF DUTY 4"),
    pv("Call of Duty 4, dos mil siete", "c_cod4", "Call of Duty 4 · 2007", dur=2.2, x=.80, y=.62, tam=320),
    rel("Misión Shock and Awe", "shock_awe", "Shock and Awe", "Call of Duty 4", dur=3.4, x=.77, y=.52, tam=420),
    cam("la capital de Al-Asad", "alasad", "Al-Asad", dur=2.6),
    mg_en(C.marcador("Bomba nuclear", 300, "En la ciudad"), "aparece una bomba nuclear", 2.8, "marcador bomba", x=.55, y=.36),
    mg_en(C.objetivo("Desactiva la bomba", "Antes de que explote"), "una misión para desactivarla", 2.4, "objetivo bomba", x=.30, y=.82),
    mg_en(C.fallida("Misión inexistente", "Nunca estuvo en el juego"), "No existe. El helicóptero", 2.2, "fallida bomba"),
    ficha("el sargento Jackson muere", "Paul Jackson", "Muere *arrastrándose* entre las ruinas.", "INTEL / SHOCK AND AWE", dur=3.4),
    pv("la del cuarto de control", "war_room", "No Fighting in the War Room", dur=3.4, x=.80, y=.62, tam=340),
    mg_en(C.objetivo("Sube los códigos de aborto", "Penúltima misión", completo=True), "subes los códigos de aborto", 3.0,
          "objetivo aborto", x=.30, y=.82),
    pv("los misiles nucleares de Zakhaev", "zakhaev", "Zakhaev", dur=2.8, x=.80, y=.60, tam=320),
    mg_en(C.balanza("Lo que tu cabeza juntó", [("Desactivar la bomba de la ciudad", False, "no existe"),
                                               ("Abortar los misiles de Zakhaev", True, "sí existe")]),
          "Tu cabeza juntó las dos", 2.6, "balanza bomba", y=.50),
    caso("y salvó a Jackson", "falso", "La bomba desactivada", "Shock and Awe · CoD 4", dur=2.6),

    # ---------------- 19 · la mira de la Intervention
    puesto("En el diecinueve", 19, "La mira de la Intervention", "MULTIJUGADOR / MODERN WARFARE 2"),
    rel("la mira de la Intervention", "intervention", "Intervention", "Francotirador · MW2", dur=3.6, x=.77, y=.52, tam=440),
    pv("Modern Warfare 2, dos mil nueve", "c_mw2", "Modern Warfare 2 · 2009", dur=2.8, x=.18, y=.40, tam=300),
    mg_en(C.contador(2022, "", "LA IMAGEN SE PUBLICA", desde=2009), "En dos mil veintidós alguien", 2.8, "contador 2022", x=.30, y=.30),
    mg_en(C.marcador("Semicírculo negro", 1, "Debajo de la mira"), "un semicírculo negro", 3.0, "marcador semicirculo", x=.5, y=.70),
    ficha("Es la sombra del soporte", "La sombra", "Sombra del *soporte de la mira*.", "INTEL / MW2 2009", dur=3.4),
    mg_en(C.objetivo("Mira el visor", "No por el visor", completo=True), "Miraste por ese visor", 3.0, "objetivo visor", x=.30, y=.82),
    caso("Y nunca miraste el visor", "falso", "La mira limpia", "Siempre tuvo la sombra", dur=2.6),

    # ---------------- 18 · Richtofen
    puesto("Número dieciocho", 18, "El uniforme de Richtofen", "ZOMBIES / WORLD AT WAR Y BLACK OPS"),
    cam("Edward Richtofen, el doctor", "richtofen", "Richtofen", dur=3.0, x=.16, y=.66),
    ficha("el que habla con las voces", "Edward Richtofen", "Habla con *las voces de su cabeza*.", "INTEL / ULTIMIS", dur=3.2, x=.73),
    mg_en(C.espejo("¿De qué color es el uniforme?", ("VERDE", "Tu memoria", ["Uniforme verde militar"], None),
                   ("CAQUI", "World at War · Black Ops", ["Tirando a marrón", "Gorra de oficial y guantes"], None), "MISMO UNIFORME"),
          "lo recuerda de uniforme verde", 7.0, "espejo uniforme", x=.5, y=.40),
    pv("en World at War y en Black Ops", "c_waw", "World at War", dur=2.6, x=.87, y=.84, tam=220),
    caso("lo pintó de otro color", "falso", "Richtofen de verde", "Siempre fue caqui", dur=2.6),

    # ---------------- 17 · Nuketown
    puesto("En el diecisiete", 17, "El césped de Nuketown", "MULTIJUGADOR / BLACK OPS 2"),
    rel("Nuketown dos mil veinticinco, Black", "nuketown2025", "Nuketown 2025", "Black Ops 2", dur=3.4, x=.77, y=.52, tam=440),
    ficha("dos casas, un autobús", "Nuketown 2025", "2 casas · 1 autobús · *maniquíes*.", "INTEL / BLACK OPS 2", dur=3.4),
    mg_en(C.objetivo("¿Jardín de verdad?", "Lo que recuerdas"), "como un jardín de verdad", 2.4, "objetivo jardin", x=.30, y=.82),
    mg_en(C.marcador("Césped enrollado", 12, "Junto a la casa amarilla"), "el césped está enrollado", 3.2, "marcador cesped", x=.55, y=.36),
    caso("Ni vecinos de verdad", "falso", "Césped de verdad", "Era artificial", dur=2.4),

    # ---------------- 16 · Double Tap
    puesto("Número dieciséis", 16, "Double Tap, segunda parte", "ZOMBIES / BLACK OPS"),
    pv("en Origins no había máquina", "double_tap", "Double Tap", dur=2.8, x=.80, y=.62, tam=320),
    rel("Ascension, Black Ops, dos mil diez", "ascension", "Ascension", "Black Ops · 2010", dur=3.4, x=.77, y=.52, tam=420),
    ficha("la base soviética de los cohetes", "Ascension", "Cohetes soviéticos y *monos espaciales*.", "INTEL / BLACK OPS", dur=3.4),
    pv("junto a Mule Kick", "mule_kick", "Mule Kick", dur=2.6, x=.18, y=.64, tam=300),
    carr([("phd", "PhD Flopper"), ("staminup", "Stamin-Up")], de="Ese mapa trajo dos perks", a=("Double Tap solo llegó", -.1),
         marcas=["PhD Flopper", "Stamin-Up"], titulo="Las perks nuevas de Ascension"),
    pv(("dentro de Der Wunderfizz", .8), "wunderfizz", "Der Wunderfizz", dur=2.8, x=.80, y=.70, tam=300),
    mg_en(C.linea("Double Tap en Ascension", [("2010", "Black Ops", "No está"), ("2017", "Black Ops 3", "Solo en Der Wunderfizz")], h=400),
          "Double Tap solo llegó con", 4.2, "linea double tap", x=.5, y=.30),
    caso(("dentro de Der Wunderfizz|fin", .3), "falso", "Double Tap en Ascension", "Solo en Black Ops 3", dur=2.0, x=.30, y=.26),

    # ---------------- 15 · Downhill
    puesto("En el quince", 15, "La montaña que nunca volvió", "MULTIJUGADOR / BLACK OPS 2"),
    pv("Downhill, Black Ops 2", "downhill", "Downhill · Alpes franceses", dur=3.0, x=.80, y=.62, tam=340),
    mg_en(C.marcador("Góndola", 40, "Cruza el mapa"), "con góndolas que cruzan", 2.8, "marcador gondola", x=.55, y=.30),
    mg_en(C.fallida("Sin remasterizar", "Downhill solo existe en Black Ops 2"), "Downhill solo existe en", 2.2, "fallida downhill"),
    mg(C.fusion((P("downhill"), "DOWNHILL", "Black Ops 2 · 2013"), (P("alpine"), "ALPINE", "Cold War · 2020"), "Downhill remasterizado"),
       de="Lo que tienes en la cabeza", a=("Otro mapa|fin", 0), marcas=["Lo que tienes en la cabeza", "Alpine, de Cold War", "Mismo frío"],
       nombre="fusion downhill", y=.50),
    caso(("Otro mapa|fin", 0), "falso", "Downhill remasterizado", "Era Alpine, de Cold War", dur=2.4, y=.20),

    # ---------------- 14 · cámara del Pack-a-Punch
    puesto("Número catorce", 14, "La cámara del Pack-a-Punch", "ZOMBIES / KINO DER TOTEN"),
    rel("En el teatro de Kino der Toten", "kino", "Kino der Toten", "Black Ops · 2010", dur=3.0, x=.77, y=.52, tam=420),
    pv("cuando mejoras un arma", "pap", "Pack-a-Punch", dur=2.8, x=.21, y=.58, tam=300),
    mg_en(C.marcador("Tele del proyector", 10, "Te ves a ti mismo"), "en las teles del cuarto", 3.2, "marcador tele", x=.55, y=.32),
    mg_en(C.balanza("¿Existe la cámara?", [("Jugando en consola o PC", True, "sí"), ("En pantalla dividida", False, "se apaga"),
                                           ("En la versión de iPhone", False, "no existe")]),
          "La cámara está en el juego", 6.4, "balanza camara", y=.50),
    pv("la versión de iPhone", "iphone", "Black Ops Zombies · iOS", dur=2.6, x=.12, y=.20, tam=240),
    caso("y en qué pantalla", "a_medias", "La cámara de Kino", "Depende de la pantalla", dur=2.6),

    # ---------------- 13 · devolver la granada
    puesto("En el trece", 13, "Devolver la granada", "CAMPAÑA / CALL OF DUTY 2"),
    pv("Call of Duty 2, dos mil cinco", "c_cod2", "Call of Duty 2 · 2005", dur=2.8, x=.80, y=.62, tam=320),
    ficha("Normandía, el norte de África", "Call of Duty 2", "Normandía · *norte de África*.", "INTEL / CAMPAÑA", dur=3.2),
    mg_en(C.marcador("Granada", 3, "A tus pies"), "granadas de palo alemanas", 2.6, "marcador granada", x=.5, y=.66),
    mg_en(C.objetivo("Devuelve la granada", "Lo que recuerdas"), "recuerda agarrarlas y devolverlas", 2.4, "objetivo granada", x=.30, y=.82),
    mg_en(C.fallida("No se puede", "Solo correr o tirarte al suelo"), "eso no se podía hacer", 2.4, "fallida granada"),
    caso("fue en otro juego", "falso", "Devolver granadas en CoD 2", "Llegó después", dur=2.4),

    # ---------------- 12 · los perros
    puesto("Número doce", 12, "Los perros de World at War", "MULTIJUGADOR / WORLD AT WAR"),
    rel("Cuando un rival consigue los perros", "perros", "Perros", "Racha de bajas", dur=3.4, x=.77, y=.52, tam=400),
    pv("el anunciador japonés", "c_waw", "World at War · 2008", dur=2.8, x=.18, y=.64, tam=320),
    mg_en(C.radio("ANUNCIADOR", "«Los cobardes mandan perros»", "LO QUE RECUERDAS"), "los cobardes mandan perros", 2.6,
          "radio cobardes", x=.5, y=.26),
    mg_en(C.radio("ANUNCIADOR JAPONÉS", "«The savages send dogs to do their work»", "MULTIJUGADOR / WORLD AT WAR"),
          ("perros. Escucha.|fin", -.1), 4.2, "radio savages", x=.5, y=.26),
    caso("Ni cobardes, ni nada", "falso", "Los cobardes", "Dice «savages»", dur=2.6),

    # ---------------- 11 · el armario de Nacht
    puesto("En el once", 11, "El armario de los zombis", "ZOMBIES / NACHT DER UNTOTEN"),
    rel("Nacht der Untoten, de World", "nacht", "Nacht der Untoten", "World at War · 2008", dur=3.0, x=.77, y=.52, tam=420),
    ficha("un búnker, cuatro ventanas", "Nacht der Untoten", "1 búnker · *4 ventanas* · 1 armario.", "INTEL / WORLD AT WAR", dur=3.0),
    mg_en(C.marcador("Armario", 8, "Piso de arriba"), "un armario en la pared", 2.6, "marcador armario", x=.55, y=.36),
    mg_en(C.espejo("¿Qué sale del armario?", ("PTRS-41", "Lo que recuerdas", ["Antitanque"], P("ptrs")),
                   ("KAR98K", "Lo que sale", ["Con mira", "1500 puntos"], P("kar98k")), "MISMO ARMARIO"),
          "salía el PTRS-41", 7.4, "espejo armario", x=.5, y=.40),
    pv("solo salía de la caja misteriosa", "caja", "La caja misteriosa", dur=2.6, x=.80, y=.62, tam=300),
    caso("solo salía de la caja misteriosa|fin", "falso", "PTRS en el armario", "Era un Kar98k", dur=2.4),
    peg("un espectador me escribió", "com_UgzdPVWBh-q8W6o2CZx4AaABAg", "", dur=8.0, x=.36, y=.30, tam=760, giro=-2),
    mg_en(C.sello("MANIPULADORA", "CONFESIÓN"), "Lo de manipuladora", 2.4, "sello manipuladora", x=.64, y=.62),
    mg_en(C.contador(30, "SEGUNDOS", "MIRANDO UN ARMARIO"), "durante treinta segundos", 2.6, "contador treinta", x=.30, y=.30),

    # ---------------- 10 · Lullaby of a Deadman
    puesto("Número diez", 10, "La canción que no era de Kino", "ZOMBIES / VERRÜCKT"),
    rel("Lullaby of a Deadman.", "lullaby", "Lullaby of a Deadman", "Banda sonora de Zombies", dur=3.2, x=.77, y=.52, tam=420),
    pv("sonando en Kino der Toten", "kino", "Kino der Toten", dur=2.6, x=.18, y=.64, tam=300),
    pv("es de Verrückt", "verruckt", "Verrückt · el manicomio", dur=3.0, x=.80, y=.62, tam=330),
    mg_en(C.contador(3, "VECES", "LA CADENA DEL RETRETE"), "tirar tres veces", 3.0, "contador cadena", x=.30, y=.30),
    mg_en(C.marcador("Retrete", 2, "Baño del lado alemán"), "en el baño del lado", 3.4, "marcador retrete", x=.55, y=.40),
    mg_en(C.radio("LULLABY OF A DEADMAN", "Suena: canción secreta de Verrückt", "BAÑO DEL LADO ALEMÁN"), ("lado alemán|fin", 2.0), 5.0,
          "radio lullaby", x=.5, y=.24),
    mg(C.fusion((P("verruckt"), "VERRÜCKT", "Lullaby of a Deadman"), (P("kino"), "KINO", "Ciento quince"), "Lullaby en Kino"),
       de="La canción de Kino es otra", a=("de YouTube de dos mil diez|fin", 0), marcas=["La canción de Kino", "Ciento quince", "montajes de YouTube"],
       nombre="fusion lullaby", y=.50),
    caso("de YouTube de dos mil diez|fin", "falso", "Lullaby en Kino", "Es de Verrückt", dur=2.2),

    # ---------------- 9 · Wunderwaffe
    puesto("En el nueve", 9, "La Wunderwaffe", "ZOMBIES / DER RIESE"),
    rel("La Wunderwaffe DG-2", "wunderwaffe", "Wunderwaffe DG-2", "Der Riese", dur=3.4, x=.77, y=.52, tam=440),
    pv("el arma de rayos de Der Riese", "der_riese", "Der Riese", dur=2.6, x=.18, y=.64, tam=300),
    mg_en(C.contador(24, "ZOMBIS", "LA LEYENDA"), "mataba veinticuatro zombis", 2.4, "contador leyenda", x=.30, y=.30),
    mg_en(C.contador(10, "ZOMBIS", "POR DISPARO, COMO MÁXIMO"), "Mata hasta diez", 2.8, "contador diez", x=.70, y=.30),
    pv("Con Pack-a-Punch o sin él", "pap", "Pack-a-Punch", dur=2.6, x=.18, y=.64, tam=300),
    ficha("trae veinticuatro cargas", "Munición", "3 + *24* de reserva.", "INTEL / DER RIESE", dur=3.0),
    ficha("nunca hay más de veinticuatro", "Límite", "Máximo *24 zombis* a la vez.", "INTEL / WORLD AT WAR", dur=3.2, x=.73),
    caso("en el sitio equivocado", "falso", "24 de un tiro", "Máximo 10", dur=2.4),

    # ---------------- 8 · Andrés
    puesto("Número ocho", 8, "Este me lo mandó Andrés", "CAMPAÑA / BLACK OPS"),
    peg("Me escribió que Black Ops", "com_Ugz5_SxOl2jDb0wNjT14AaABAg", "", dur=7.0, x=.36, y=.30, tam=760, giro=2),
    mg_en(C.sello("EN VIVO", "EFECTO MANDELA"), "Acabas de hacer un efecto", 2.6, "sello en vivo", x=.74, y=.62),
    pv("Black Ops salió el nueve", "c_bo1", "Black Ops · 9-11-2010", dur=3.0, x=.80, y=.62, tam=330),
    mg_en(C.contador(15, "MISIONES", "BLACK OPS · CAMPAÑA"), "la campaña tiene quince", 2.8, "contador quince", x=.30, y=.30),
    pv("salió Call of Duty 4", "c_cod4", "Call of Duty 4 · 2007", dur=2.8, x=.18, y=.64, tam=320),
    pv("junto al logo de Treyarch", "treyarch", "Treyarch", dur=2.6, x=.80, y=.62, tam=290),
    mg_en(C.descifra("Tr/11-09-10", "9 NOV 2010", "LA FECHA EN LA INTRO", "Junto al logo de Treyarch"), "se lee once, nueve", 3.6,
          "descifra fecha", x=.5, y=.30),
    caso("tres años atrás", "falso", "Black Ops de 2007", "Salió en 2010", dur=2.4),

    # ---------------- 7 · Mason y Woods
    puesto("En el siete", 7, "El reencuentro de Mason y Woods", "CAMPAÑA / BLACK OPS 2"),
    pv("misión Victoria pírrica", "pirrica", "Victoria pírrica", dur=2.8, x=.80, y=.62, tam=330),
    pv("Mason y Hudson abren", "mason", "Mason", dur=2.6, x=.18, y=.64, tam=300),
    cam("Hudson abren un contenedor", "hudson", "Hudson", dur=2.4, x=.84, y=.66),
    mg_en(C.marcador("Contenedor", 6, "Angola · 1986"), "un contenedor en Angola", 2.6, "marcador contenedor", x=.55, y=.36),
    peg("Rafa recuerda que Mason", "com_Ugy5ufFGlvSuVt3TAlZ4AaABAg", "", dur=6.4, x=.36, y=.30, tam=760, giro=-2),
    mg_en(C.radio("MASON", "«Frank, soy yo, Mason»", "DOBLAJE LATINO / VICTORIA PÍRRICA"), ("lo que dice de verdad|fin", -.1), 3.8,
          "radio frank", x=.5, y=.26),
    mg_en(C.balanza("¿Dónde está el «me recuerdas»?", [("Doblaje latino", False, "no está"), ("Versión en inglés", False, "no está")]),
          "Ni en el doblaje latino", 4.0, "balanza recuerdas", y=.50),
    caso("El juego no lo dice", "falso", "«¿Me recuerdas?»", "Mason nunca lo dice", dur=2.4),

    # ---------------- 6 · la perk de Moon
    puesto("Número seis", 6, "La perk de Moon, otra vez", "ZOMBIES / MOON"),
    rel("La perk de Moon, otra vez", "moon", "Moon", "Black Ops · 2011", dur=3.0, x=.77, y=.52, tam=420),
    peg("Y metal me escribió", "com_UgwR4poiAMmxZRQHcyl4AaABAg", "", dur=6.4, x=.36, y=.30, tam=760, giro=2),
    pv("Encima de las plataformas del biodomo", "gravity_lift", "Plataforma de gravedad", dur=3.0, x=.18, y=.64, tam=320),
    ficha("doble puntos, carpintero", "Potenciadores", "Doble puntos · Carpintero · *Nuke* · Insta-Kill.", "INTEL / MOON", dur=3.4),
    mg_en(C.marcador("Destello verde", 4, "Video de 2011"), "un destello verde", 3.2, "marcador destello", x=.55, y=.36),
    pv("en Shangri-La, el mapa anterior", "shangrila", "Shangri-La", dur=3.0, x=.80, y=.62, tam=330),
    rel("una botella de perk", "perk_bottle", "Botella de perk", "Una fracción de segundo", dur=3.2, x=.77, y=.52, tam=400),
    caso("En otro mapa", "a_medias", "La perk de Moon", "La viste en Shangri-La", dur=2.6),

    # ---------------- 5 · el M1911 de Alcatraz
    puesto("En el cinco", 5, "El M1911 de Alcatraz", "ZOMBIES / MOB OF THE DEAD"),
    rel("Mob of the Dead, Black Ops", "motd", "Mob of the Dead", "Black Ops 2 · 2013", dur=3.0, x=.77, y=.52, tam=420),
    pv("la prisión de Alcatraz", "alcatraz", "Alcatraz", dur=2.6, x=.18, y=.64, tam=320, marco="polaroid"),
    sil("y Brutus, el guardia", "brutus", "Brutus", "El guardia", lado="der", dur=3.4),
    pv("haber sacado el M1911", "m1911", "M1911", dur=2.8, x=.18, y=.64, tam=320),
    mg_en(C.marcador("M1911", 1, "Girando en la caja"), "Y aquí está, girando", 3.0, "marcador m1911", x=.55, y=.32),
    mg_en(C.fallida("No se puede sacar", "Solo sale en la ruleta"), "Pero no se puede sacar", 2.4, "fallida m1911"),
    ficha("han gastado millones de puntos", "La ruleta", "Millones de puntos · *ni un M1911*.", "INTEL / MOB OF THE DEAD", dur=3.2),
    caso("Los que lo sacaron, no", "a_medias", "El M1911 de la caja", "Se ve, pero no se saca", dur=2.6),

    # ---------------- 4 · Hoover
    puesto("Número cuatro", 4, "El director Hoover", "MULTIJUGADOR / BLACK OPS 2"),
    rel("el mapa Raid", "raid", "Raid", "Black Ops 2", dur=3.0, x=.77, y=.52, tam=420),
    pv("al anunciador del FBI", "fbi", "FBI", dur=2.6, x=.18, y=.64, tam=290),
    mg_en(C.radio("FBI", "«Buen trabajo, equipo. El director Hoover estará complacido.»", "LO QUE RECUERDAS"), "Buen trabajo, equipo",
          4.0, "radio fbi", x=.5, y=.26),
    mg_en(C.fallida("Frase no encontrada", "El FBI no la tiene"), "El FBI no tiene esa frase", 2.2, "fallida fbi"),
    pv("el SDC, el ejército chino", "sdc", "SDC", dur=2.8, x=.80, y=.62, tam=290),
    mg_en(C.radio("SDC", "«Our generals will be pleased»", "ANUNCIADOR / SDC"), ("ejército chino. Escucha.|fin", -.1), 3.8,
          "radio sdc", x=.5, y=.26),
    pv("J. Edgar Hoover murió", "hoover", "J. Edgar Hoover", dur=3.6, x=.22, y=.52, tam=600, marco="museo"),
    mg_en(C.linea("Hoover y Black Ops 2", [("1972", "Muere Hoover", "Director del FBI"), ("2025", "Black Ops 2", "El multijugador")], h=400),
          "El multijugador de Black Ops", 4.0, "linea hoover", x=.5, y=.30),
    caso("complacido desde la tumba", "falso", "Hoover complacido", "Dice «generales»", dur=2.4),

    # ---------------- campaña de suscripción
    mg_en(C.contador(100, "PERSONAS", "VEN ESTOS EXPEDIENTES"), "De cada cien personas", 2.6, "contador cien", x=.30, y=.30),
    mg_en(C.contador(0, "SUSCRITAS", "DE ESAS CIEN"), "ni una está suscrita", 2.6, "contador cero", x=.70, y=.30),
    mg_en(C.logro("Ya eres de la unidad", "Expediente 141"), "ya eres de la unidad", 3.0, "logro unidad", x=.5, y=.30),
    mg_en(C.objetivo("Suscríbete", "El siguiente expediente te llega primero"), ("Suscríbete, y el siguiente", 0), 3.2,
          "objetivo suscribete subs", x=.30, y=.82),

    # ---------------- 3 · la AUG en la Granja
    puesto("Número tres", 3, "La AUG en la Granja", "ZOMBIES / BLACK OPS 2"),
    peg("Este me lo mandó brexxy", "com_Ugz7EOCl7eQvnRkWqVF4AaABAg", "", dur=7.0, x=.36, y=.30, tam=760, giro=-2),
    rel("La Granja, el mapa de Zombies", "farm", "La Granja", "Black Ops 2 · 2012", dur=3.0, x=.77, y=.52, tam=420),
    muro([("mtar", "MTAR"), ("galil", "Galil"), ("raygun", "Ray Gun")], de="la MTAR, la Galil", a=("La AUG no está", -.05),
         marcas=["la MTAR", "la Galil", "la Ray Gun"], titulo="La caja de la Granja"),
    mg_en(C.fallida("AUG no encontrada", "Ningún modo de Black Ops 2"), "La AUG no está", 2.4, "fallida aug"),
    pv("De Black Ops 1", "c_bo1", "Black Ops 1 · 2010", dur=2.6, x=.80, y=.62, tam=300),
    rel("con mira Swarovski", "aug", "AUG", "Mira Swarovski · Black Ops 1", dur=3.2, x=.77, y=.52, tam=420),
    ficha("se convertía en la AUG-50M3", "AUG-50M3", "Con *escopeta debajo*.", "INTEL / PACK-A-PUNCH", dur=3.2),
    mg(C.fusion((P("aug"), "AUG", "Black Ops 1 · 2010"), (P("mtar"), "MTAR", "La Granja · 2012"), "AUG en la Granja"),
       de="Y en la Granja sí está", a=("Jugaron mucho Black Ops 1|fin", 0), marcas=["Y en la Granja sí está", "parece una AUG", "Tú y tus hermanos"],
       nombre="fusion aug", y=.50),
    caso(("Jugaron mucho Black Ops 1|fin", 0), "falso", "La AUG en la Granja", "Era la MTAR", dur=2.4),

    # ---------------- 2 · el ojo de Weaver (sin enseñar la herida)
    puesto("En el dos", 2, "El ojo de Weaver", "CAMPAÑA / BLACK OPS"),
    rel("Grigori Weaver, el agente ruso", "weaver", "Grigori Weaver", "El del parche en el ojo", dur=3.4, x=.77, y=.52, tam=440),
    pv("En Baikonur", "baikonur", "Baikonur", dur=2.6, x=.80, y=.62, tam=320, marco="polaroid"),
    sil(("lo tiene en el suelo|fin", 0), "kravchenko", "Kravchenko", "Black Ops", lado="izq", dur=3.4),
    mg_en(C.sello("CUCHILLO", "NO UN PURO"), "Fue un cuchillo", 2.4, "sello cuchillo", x=.72, y=.42),
    pv("World at War, dos mil ocho. La", "semper_fi", "Semper Fi · World at War", dur=3.0, x=.80, y=.62, tam=330),
    ficha("Un oficial japonés interroga", "Semper Fi", "Interrogan al *soldado Pyle*.", "INTEL / WORLD AT WAR", dur=3.2),
    mg(C.fusion((P("weaver"), "WEAVER", "Black Ops · cuchillo"), (P("semper_fi"), "PYLE", "World at War · cigarro"), "Weaver + puro"),
       de="Dos juegos de Treyarch", a=("en una sola tortura|fin", 0), marcas=["Dos juegos de Treyarch", "dos ojos", "Y tu memoria"],
       nombre="fusion weaver", y=.50),
    caso(("en una sola tortura|fin", 0), "falso", "El puro de Weaver", "Fue un cuchillo", dur=2.4),

    # ---------------- 1 · la frase de Gaz
    puesto("Y el número uno", 1, "La frase de Gaz", "CAMPAÑA / CALL OF DUTY 4"),
    sil("el campo de tiro", "gaz", "Gaz", "Call of Duty 4", lado="der", dur=3.6),
    pv("Medio internet la cita así", "fng", "F.N.G.", dur=2.6, x=.16, y=.66, tam=280),
    mg_en(C.radio("LO QUE CITA INTERNET", "«Cambiar a tu sidearm siempre es más rápido que recargar»", "MEDIO INTERNET"),
          "Medio internet la cita así", 4.4, "radio internet", x=.5, y=.26),
    mg_en(C.radio("GAZ", "«…switching to your pistol is always faster than reloading»", "CALL OF DUTY 4 / F.N.G."),
          ("Escucha el final|fin", -.1), 4.6, "radio gaz", x=.5, y=.26),
    mg_en(C.descifra("SIDEARM", "PISTOL", "LA PALABRA DE GAZ", "Pistola"), "La palabra que dice Gaz", 3.6, "descifra pistol", x=.5, y=.30),
    mg_en(C.objetivo("Acuchilla la sandía", "Knife the watermelon"), "acuchillar una sandía", 3.0, "objetivo sandia", x=.30, y=.82),
    caso("con otra palabra", "falso", "«Sidearm»", "Gaz dice «pistol»", dur=2.4),

    # ---------------- cierre
    mg_en(C.sello("EXPEDIENTE CERRADO", "141"), "Expediente cerrado", 2.4, "sello cerrado", x=.5, y=.46),
    mg_en(C.balanza("Veinte efectos Mandela", [("Falsos", False, "17"), ("A medias", None, "3")]), ("me los dieron ustedes|fin", 0),
          3.6, "balanza cierre", y=.50),
    peg("Como el de lycanroc", "com_UgwZ18R2A1eoAmLaKA54AaABAg", "", dur=4.6, x=.36, y=.30, tam=760, giro=2),
    pv("la carta física de Pawn", "pawn", "Pawn Takes Pawn", dur=3.0, x=.80, y=.62, tam=330),
    peg("O el que dijo que los", "com_UgxxEqwK7vmmUY4_0up4AaABAg", "", dur=5.2, x=.62, y=.30, tam=760, giro=-2),
    mg_en(C.objetivo("¿Qué recuerdas tú?", "Escríbelo en los comentarios"), "Escríbelo", 3.2, "objetivo comentarios", x=.30, y=.82),
    mg_en(C.logro("Sale en la parte tres", "Si tu efecto es bueno"), "sale en la parte tres", 2.8, "logro parte tres", x=.5, y=.30),
    pv("tienes la parte uno", "c_bo2", "20 efectos Mandela · parte 1", dur=2.8, x=.18, y=.64, tam=310),
    pv("los treinta misterios", "motd", "30 misterios de CoD", dur=2.8, x=.80, y=.62, tam=310),
    mg_en(C.sello("RETÍRATE, SOLDADO", "EXPEDIENTE 141"), "Retírate, soldado", 3.0, "sello retirate", x=.5, y=.46),
]

ROTULOS = [
    dict(texto="NO EXISTE", en="No existe. El helicóptero", tam=150, color="amarillo", y=.22, dur=1.6),
    dict(texto="QUICKSCOPE", en="de los quickscopes", tam=130, color="amarillo", y=.22, dur=1.6),
    dict(texto="SIEMPRE ESTUVO", en="Siempre estuvo. Es la", tam=140, color="amarillo", y=.22, dur=1.8),
    dict(texto="CÉSPED ARTIFICIAL", en="Es césped artificial", tam=120, color="amarillo", y=.22, dur=2.0),
    dict(texto="LOS DOS TIENEN RAZÓN", en="Y los dos tienen razón", tam=100, color="amarillo", y=.22, dur=2.0),
    dict(texto="SALVAJES", en="Salvajes.|fin", tam=160, color="amarillo", y=.22, dur=1.6),
    dict(texto="MERCI", en="Merci", tam=170, color="amarillo", y=.22, dur=1.6),
    dict(texto="115", en="Ciento quince", tam=180, color="amarillo", y=.86, dur=1.6),
    dict(texto="EFECTO MANDELA EN VIVO", en="Acabas de hacer un efecto", tam=96, color="amarillo", y=.22, dur=2.4),
    dict(texto="Y YA", en="Y ya. Ni en", tam=170, color="amarillo", y=.22, dur=1.4),
    dict(texto="LO VISTE EN OTRO MAPA", en="Pero no lo soñaste", tam=100, color="amarillo", y=.22, dur=2.4),
    dict(texto="GENERALES, NO HOOVER", en="Generales, no Hoover", tam=110, color="amarillo", y=.22, dur=2.0),
    dict(texto="NO ESTÁN LOCOS", en="no están locos", tam=130, color="amarillo", y=.22, dur=1.8),
    dict(texto="FUE UN CUCHILLO", en="Fue un cuchillo", tam=130, color="amarillo", y=.22, dur=1.8),
    dict(texto="PISTOL", en="Dice pistola", tam=180, color="amarillo", y=.22, dur=1.6),
]

SFX = {}
# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/cod/ → sfx/cod_*.mp3), solo en momentos clave
PISTAS = [
    dict(sfx="cod_sello", en="Expediente ciento", vol=.30),
    dict(sfx="cod_puesto", en="Número veinte. La bomba", vol=.24),
    dict(sfx="cod_fallida", en="No existe. El helicóptero", vol=.26),
    dict(sfx="cod_puesto", en="Número dieciséis", vol=.22),
    dict(sfx="cod_fallida", en="Downhill solo existe en", vol=.24),
    dict(sfx="cod_radio", en="los cobardes mandan perros", vol=.20),
    dict(sfx="cod_puesto", en="Número diez", vol=.22),
    dict(sfx="cod_logro", en="Acabas de hacer un efecto", vol=.26),
    dict(sfx="cod_puesto", en="Número seis", vol=.22),
    dict(sfx="cod_fallida", en="Pero no se puede sacar", vol=.24),
    dict(sfx="cod_radio", en="Buen trabajo, equipo", vol=.20),
    dict(sfx="cod_logro", en="ya eres de la unidad", vol=.28),
    dict(sfx="cod_fallida", en="La AUG no está", vol=.24),
    dict(sfx="cod_puesto", en="Y el número uno", vol=.26),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco (post), a nivel de voz
    dict(sfx="s_gaz_corto", en=("de Call of Duty 4.|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_savages", en=("perros. Escucha.|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_lullaby", en=("lado alemán|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_frank", en=("lo que dice de verdad|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_sdc", en=("ejército chino. Escucha.|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_gaz", en=("Escucha el final|fin", .1), vol=1.0, voz=True),
]

# Cortes rápidos con clips ya bajados (debajo de todo lo demás; 13-nov-2026)
VIDEOS = [
    vid(64, "una frase de Alex Mason", ("y un Black Ops que salió", -.1), desde=1.0),       # Woods en el contenedor
    vid(60, "y un Black Ops que salió", ("Los revisé todos", -.1), desde=1.0),              # campaña de Black Ops
    vid(72, "Veinte efectos Mandela de Call", ("Y esta vez, cuatro", -.1), desde=0.5),      # el destello de 2011
    vid(91, "Y esta vez, cuatro", ("Número veinte", -.1), desde=1.0),                       # la AUG en el Pack-a-Punch (b78 trae texto)
    vid(79, "Pero no se puede sacar", ("Hay jugadores que han", -.1), desde=0.5),          # tapa el texto del youtuber de b78 (0:14+)
    # Weaver de rodillas ANTES del ataque (jJySHN3Hsr0 1-6,5 s; desde 15 s se acerca el cuchillo: nunca)
    dict(tipo="video", ruta=os.path.join(_AQUI, "medios", "extra_weaver.mp4"), de="Kravchenko lo tiene en el suelo",
         a=("Mucha gente recuerda que Kravchenko", -.05), desde=0.0, recorte=0.0, entra=.12, sale=.12, nombre="corte weaver"),
]
FX = VIDEOS + FX

# ---- 2.ª pasada (chequeo 13-nov: pegatinas 4,3/min contra el mínimo de 5; fichas 0,8 contra 1,4 del canal)
_I, _D = dict(x=.18, y=.64, tam=280), dict(x=.80, y=.62, tam=280)
FX += [
    pv("Siempre estuvo. Es la", "intervention", "Siempre estuvo", **_D),
    pv("Lo tuviste delante en cada partida", "c_bo1", "Black Ops · 2010", **_D),
    pv("En dos mil veinticinco ya no quedaba", "nuketown2025", "Nuketown 2025", **_I),
    pv("Muchos recuerdan Double Tap junto", "double_tap", "¿Double Tap?", **_D),
    pv("Hay quien jura haberlo jugado", "c_bocw", "¿Remasterizado?", **_I),
    pv("Unos juran que esa cámara", "kino", "Kino der Toten", **_I),
    pv("Mucha gente recuerda agarrarlas", "c_cod2", "Call of Duty 2", **_I),
    pv("Los salvajes mandan perros", "perros", "Los salvajes", **_I),
    pv("Y ya que hablamos de mapas alemanes", "kino", "Kino der Toten", **_D),
    pv("La leyenda dice que con Pack-a-Punch", "pap", "Pack-a-Punch", **_D),
    pv("Y aun así lo mandaste tres", "c_cod4", "2007 = Call of Duty 4", **_I),
    pv("Woods llevaba años preso", "pirrica", "Victoria pírrica", **_D),
    pv("Que recordaba a gente consiguiéndola", "perk_bottle", "¿Una perk gratis?", **_I),
    pv("Así que no, en Moon no había", "moon", "Moon", **_D),
    pv("Hay jugadores que han gastado", "caja", "La caja", **_D),
    pv("El multijugador de Black Ops 2 pasa", "c_bo2", "Black Ops 2", **_I),
    pv("recuerda perfectamente la AUG", "aug", "AUG", **_D),
    pv("Y el cigarro existe", "c_waw", "World at War · 2008", **_I),
    pv("Gaz sigue diciendo que el cuchillo", "gaz", "Gaz", **_D),
    ficha("Mucha gente recuerda una misión para", "El recuerdo", "Una misión para *desactivar la bomba*.", "INTEL / RECUERDO", dur=3.0),
    ficha(("Un disparo, y la electricidad", 0), "Wunderwaffe DG-2", "La electricidad *salta de zombi en zombi*.", "INTEL / DER RIESE", dur=3.2),
    ficha("y dentro está Frank Woods", "Victoria pírrica", "Angola · *Woods en el contenedor*.", "INTEL / BLACK OPS 2", dur=3.2),
    ficha("cuatro gánsteres y Brutus", "Mob of the Dead", "Alcatraz · *4 gánsteres y Brutus*.", "INTEL / BLACK OPS 2", dur=3.2),
    ficha("Y hay otro detalle: J. Edgar", "J. Edgar Hoover", "Director del FBI · *muere en 1972*.", "INTEL / HISTORIA", dur=3.4, x=.73),
    ficha("Ahí la AUG salía de la caja", "AUG", "En la caja de *todos los mapas* de BO1.", "INTEL / BLACK OPS 1", dur=3.2),
    ficha("Y no acaba ahí: Gaz sigue", "F.N.G.", "«Knife the *watermelon*».", "INTEL / CALL OF DUTY 4", dur=3.2),
    ficha("Black Ops salió el nueve", "Fecha real", "*9 de noviembre de 2010*.", "INTEL / BLACK OPS", dur=3.0, x=.73),
]
# «La canción de Kino es otra: Ciento quince» → se OYE el arranque de «115» (Elena Siegman / Kevin Sherwood, vK_uuXRtP2Q 7,4-11,4 s)
PISTAS.append(dict(sfx="s_115", en=("Ciento quince.|fin", .05), vol=.45))
