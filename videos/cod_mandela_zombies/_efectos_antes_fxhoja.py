# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 EFECTOS MANDELA de los Zombies de Call of Duty» (SECUENCIA YT, Expediente 141, 22-nov-2026).
Plantilla: videos/cod_mandela3/efectos.py (kit nucleo/mg_cod.py + peg_estilos/peg_anim/presenta, tema «cod»).
MG NUEVOS de este guion: `C.consola` (el código de BO2 que desmiente el desangrado, n.º 4) y `C.golpes` (golpes con Juggernog, n.º 10).
Citas (post): el clip va alineado al hueco (_escribir_busquedas.py) y lo que se OYE es sfx/s_*.mp3 (recortes medidos con
_citas.py) en PISTAS voz=True, al acabar la frase; `ambiente_por` no sirve: suena el beat entero, encima de la voz.
    python fab.py cod_mandela_zombies fx --seco   tiempos      FAB_FX_FINAL=1 python fab.py cod_mandela_zombies fx hoja
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





def com(en, cid, dur=6.4, x=.36, y=.30, giro=-2):
    """Comentario real del canal (pegatinas/com_<id>.png, ≤ 10 días, ninguno repetido)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760, giro=giro)


_D, _I = dict(x=.80, y=.62), dict(x=.18, y=.64)

FX = [
    # ---------------- gancho: un elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.33, y=.42),
    leg("c_bo1", "EXPEDIENTE 141 · ZOMBIS", ["Asunto: tu memoria", "20 efectos Mandela", "Solo el modo Zombies"],
        de="Asunto: tu memoria", a=("Uno de ustedes me escribió", -.1), x=.78, y=.50),
    pv("usó la Ray Gun en la campaña", "raygun", "¿La Ray Gun en la campaña?", dur=2.8, tam=330, **_D),
    pv("Otro, que la Thundergun", "thundergun", "¿La Thundergun en Black Ops?", dur=2.8, tam=330, **_I),
    mg_en(C.fallida("ESTÁN LOCOS", "Eso dijeron todos"), "A los dos les dijeron", 2.2, "fallida locos"),
    mg_en(C.objetivo("No te arrastres", "Te desangras más rápido"), "si caes, no te arrastres", 2.8, "objetivo arrastres", x=.30, y=.82),
    mg_en(C.objetivo("Revisar cada recuerdo", "Juego en pantalla · y su código", completo=True), "Lo revisé todo", 2.6,
          "objetivo revisar", x=.30, y=.82),
    pv("Hay un puente que sí se rompe", "tranzit", "El puente de TranZit", dur=2.4, tam=300, **_D),
    pv("un arma que nunca existió", "blundergat", "¿El arma que no existe?", dur=2.4, tam=300, **_I),
    pv("una pistola de rayos que casi", "raygun", "Casi lo despiden", dur=2.4, tam=300, **_D),
    mg_en(C.contador(20, "EFECTOS MANDELA", "MODO ZOMBIES"), "Veinte efectos Mandela de los zombis", 2.8, "contador 20", x=.30, y=.30),
    mg_en(C.marcador("Número 1", 20, "Lo mandó un suscriptor"), "Y el número uno te lo mandó", 2.6, "marcador numero uno", x=.55, y=.36),

    # ---------------- 20 · Nixon (post: «Oh my God!»)
    puesto("Número veinte. Nixon", 20, "¿Nixon, convertido en zombi?", "ZOMBIES / BLACK OPS · «FIVE»"),
    pv("el mapa Five", "five", "«Five» · el Pentágono", dur=2.6, tam=320, **_D),
    carr([("jfk", "Kennedy"), ("castro", "Castro"), ("mcnamara", "McNamara"), ("nixon", "Nixon")], de="Kennedy, Castro",
         a=("Hay quien recuerda que Nixon", -.1), marcas=["Kennedy", "Castro", "McNamara", "y Nixon"], titulo="Los cuatro de «Five»"),
    mg_en(C.objetivo("¿Se transforma Nixon?", "Lo que recuerdan algunos"), "Hay quien recuerda que Nixon", 2.6, "objetivo nixon",
          x=.30, y=.82),
    mg_en(C.radio("CINEMÁTICA · «FIVE»", "Escucha cómo termina."), "Escucha cómo termina", 3.4, "radio nixon", x=.5, y=.20),
    sil("Nixon grita, y se desmaya", "nixon", "Richard Nixon", "Se desmaya del susto", lado="der", dur=3.6),
    pv("sale de la armería con dos escopetas", "hs10", "Dos HS-10", dur=2.8, tam=300, **_I),
    caso("Nixon no se convirtió", "falso", "Nixon se vuelve zombi", "Se desmaya del susto", dur=2.8),

    # ---------------- 19 · Nikolai (post: «Some things are forgotten… for a reason!»)
    puesto("En el diecinueve", 19, "Las últimas palabras de Nikolai", "ZOMBIES / BLACK OPS 3 · GOROD KROVI"),
    pv("Black Ops 3, el final de Gorod Krovi", "gorod", "Gorod Krovi", dur=2.6, tam=320, **_D),
    vs(("nikolai", "Nikolai original"), ("nikolai_p", "Nikolai joven"), de="El Nikolai de los cuatro originales",
       a=("Hay quien jura que gritaba", -.1), marcas=["El Nikolai de los cuatro", "frente al grupo nuevo"], titulo="Dos Nikolai"),
    ficha("Hay quien jura que gritaba", "Lo que recuerdan", "«*Tenías que ser tú*».", "INTEL / GOROD KROVI", dur=3.0),
    mg_en(C.radio("NIKOLAI · ÚLTIMAS PALABRAS", "La frase real."), "La frase real es esta", 3.0, "radio nikolai", x=.5, y=.20),
    ficha("Algunas cosas se olvidan", "La frase real", "«Some things are forgotten… *for a reason*».", "INTEL / GOROD KROVI",
          dur=3.6, x=.73),
    caso("Y tu memoria se lo tomó", "falso", "«Tenías que ser tú»", "Se olvidan por una razón", dur=2.8),

    # ---------------- 18 · el mapa en llamas
    puesto("Número dieciocho", 18, "El mapa de zombis en llamas", "ZOMBIES / BLACK OPS 1"),
    pv("un edificio que ardía", "c_bo1", "Black Ops 1", dur=2.6, tam=300, **_D),
    mg_en(C.balanza("Mapas de zombis de Black Ops 1", [("Kino der Toten", False, "sin llamas"), ("Five", False, "sin llamas"),
                                                       ("Ascension", False, "sin llamas"), ("Call of the Dead", False, "sin llamas"),
                                                       ("Shangri-La", False, "sin llamas"), ("Moon", False, "sin llamas")]),
          "Ningún mapa de zombis de Black Ops 1", 4.6, "balanza mapas bo1", y=.50),
    pv("The Defector, la ciudad de Hue", "the_defector", "The Defector", dur=3.0, tam=320, **_I),
    pv("mil novecientos sesenta y ocho", "hue", "Hue · 1968", dur=2.6, tam=300, **_D),
    aba([("mason", "Mason"), ("woods", "Woods")], de="Mason y Woods entran", a=("Había fuego", -.1), marcas=["Mason", "Woods"],
        nombre="mason woods"),
    caso("Solo que eran vietnamitas", "falso", "Mapa de zombis en llamas", "Era una misión de campaña", dur=2.8),

    # ---------------- 17 · el zombi de Verrückt
    puesto("En el diecisiete", 17, "El zombi misterioso de Verrückt", "ZOMBIES / WORLD AT WAR"),
    pv("en el manicomio alemán", "verruckt", "Verrückt", dur=2.8, tam=320, **_D),
    mg_en(C.objetivo("¿Un zombi especial?", "Que te seguía haciendo ruidos"), "un zombi especial que lo seguía", 2.6,
          "objetivo zombi especial", x=.30, y=.82),
    ficha("No existe ningún zombi especial", "Verrückt", "Sonidos que se disparan *según dónde estés*.", "INTEL / WORLD AT WAR",
          dur=3.4),
    ficha("Si activas la silla del dentista", "La silla del dentista", "Un *taladro* y un paciente que grita.", "INTEL / VERRÜCKT",
          dur=3.4, x=.73),
    mg_en(C.balanza("Verrückt contra Nacht", [("Más rápidos", True, "Verrückt"), ("Más listos", True, "Verrückt"),
                                              ("Zombi especial", False, "no existe")]), "Y sus zombis son más rápidos", 4.0,
          "balanza verruckt", y=.50),
    caso("Te seguían todos", "falso", "El zombi especial", "Te seguían todos", dur=2.8),

    # ---------------- 16 · la Remington del banco de Town
    puesto("Número dieciséis", 16, "La escopeta del banco de Town", "ZOMBIES / BLACK OPS 2 · TOWN"),
    pv("Black Ops 2, Town", "town", "Town", dur=2.4, tam=300, **_D),
    rel("Un jugador recordaba una Remington", "rem870", "Remington 870", "¿En el banco?", dur=3.6, x=.77, y=.52, tam=420),
    mg_en(C.objetivo("Sin caja misteriosa", "Así se dio cuenta"), "Se dio cuenta de que no estaba", 2.6, "objetivo sin caja",
          x=.30, y=.82),
    ficha("El banco de Town no tiene", "El banco de Town", "Ni un arma. *Solo Speed Cola*.", "INTEL / TOWN", dur=3.2),
    pv("Solo una máquina: Speed Cola", "speed_cola", "Speed Cola", dur=2.6, tam=320, **_I),
    mg_en(C.espejo("¿Dónde está la Remington?", ("TOWN", "El banco", ["Ninguna arma", "Solo Speed Cola"], P("town")), ("TRANZIT", "Granja y estación", ["Granero", "Fuera de la estación"], P("rem870")), "REMINGTON 870"),
          "La Remington sí existe", 4.4, "espejo remington", y=.50),
    caso("La escopeta era real", "a_medias", "La Remington del banco", "Existe, pero en TranZit", dur=2.8),

    # ---------------- crítica 1 · @eltiorandomml8930
    com("Antes del quince, una pausa", "UgwUgj9v0wpbGs0c73F4AaABAg", dur=6.6),
    mg_en(C.logro("Reporte recibido", "Gracias por el reporte"), "Gracias por el reporte", 2.6, "logro reporte", x=.5, y=.30),
    mg_en(C.balanza("Este expediente trae", [("Clip del juego", True, "en cada efecto"), ("La estatua", True, "n.º 1"),
                                             ("El arma", True, "n.º 3"), ("El código", True, "n.º 4")]),
          "trae el clip del juego", 4.0, "balanza clips", y=.55),

    # ---------------- 15 · Quick Revive
    puesto("Número quince", 15, "Quick Revive, dos a la vez", "ZOMBIES / BLACK OPS 1 · SOLITARIO"),
    rel("La máquina azul de Quick Revive", "quick_revive", "Quick Revive", "Solitario", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.objetivo("¿Dos a la vez?", "Lo que recuerda un jugador"), "haber tenido dos Quick Revive", 2.6, "objetivo dos qr",
          x=.30, y=.82),
    mg_en(C.rachas("QUICK REVIVE EN SOLITARIO", [(1, "Primera compra"), (2, "Segunda compra"), (3, "Tercera compra")],
                   fantasma=(2, "Dos a la vez"), nota="NUNCA PASÓ"),
          "se compra hasta tres veces", 5.0, "rachas quick revive", x=.28, y=.50),
    mg_en(C.fallida("LA MÁQUINA DESAPARECE", "A la tercera compra"), "a la tercera, la máquina desaparece", 2.4, "fallida maquina"),
    caso("Tu memoria las juntó", "falso", "Dos Quick Revive a la vez", "Tres, una por una", dur=2.8),

    # ---------------- 14 · Type 100
    puesto("En el catorce", 14, "El subfusil japonés de World at War", "ZOMBIES / WORLD AT WAR"),
    rel("Un jugador recordaba una Type 100", "type100", "Type 100", "Subfusil japonés", dur=3.6, x=.77, y=.52, tam=420),
    mg_en(C.fallida("ESTÁS LOCO", "Eso le dijeron"), "le dijeron que estaba loco", 2.2, "fallida loco"),
    carr([("shi_no_numa", "Shi No Numa"), ("der_riese", "Der Riese")], de="Shi No Numa, el pantano", a=("Esta vez el loco", -.1),
         marcas=["Shi No Numa", "Der Riese"], titulo="Type 100 · pared y caja"),
    caso("Esta vez el loco era", "verdad", "La Type 100 en World at War", "Pared y caja", dur=2.8),

    # ---------------- 13 · el escudo de Richtofen
    puesto("Número trece", 13, "El escudo de Richtofen", "ZOMBIES / BLACK OPS 2 · ORIGINS"),
    pv("En el mapa Origins, de Black Ops 2", "origins", "Origins", dur=2.6, tam=300, **_D),
    sil("que lo armara Richtofen", "richtofen", "Richtofen", "¿Su escudo aguanta más?", lado="izq", dur=3.8),
    rel("Es un mito de patio de recreo", "shield", "Escudo zombi", "El mismo para todos", dur=3.6, x=.77, y=.52, tam=420),
    ficha("Lo único que cambia es la animación", "El escudo", "Solo cambia *la animación*.", "INTEL / ORIGINS", dur=3.2),
    caso("Construir escudos especiales", "falso", "El escudo de Richtofen", "Mito de patio de recreo", dur=2.8),

    # ---------------- 12 · la Thundergun no mataba siempre
    puesto("En el doce, un recuerdo", 12, "La Thundergun no mataba siempre", "ZOMBIES / BLACK OPS 1"),
    pv("El cañón de aire de Kino", "kino", "Kino der Toten", dur=2.6, tam=300, **_I),
    rel("Hay quien recuerda que no tenía", "thundergun", "Thundergun", "¿Daño infinito?", dur=3.6, x=.77, y=.52, tam=420),
    mg_en(C.espejo("Daño de la Thundergun", ("∞", "De cerca", ["Mata siempre"], None), ("15", "Media y larga distancia", ["Solo los tumba"], None), "LA MISMA ARMA"),
          "De cerca, el impacto directo", 5.6, "espejo thundergun", y=.50),
    caso("Guárdala en la memoria", "verdad", "No mataba siempre", "De lejos, 15 de daño", dur=2.6),
    mg_en(C.marcador("Thundergun", 3, "Vuelve en el número tres"), "La Thundergun vuelve en el número", 2.6, "marcador thundergun",
          x=.55, y=.36),

    # ---------------- 11 · tirarse frente a las máquinas
    puesto("Número once", 11, "Tirarte al suelo frente a las máquinas", "ZOMBIES / DE WORLD AT WAR A COLD WAR"),
    pv("frente a las máquinas de perks", "perk_cola", "Las máquinas de perks", dur=2.6, tam=300, **_D),
    mg_en(C.linea("Puntos por tirarte al suelo", [("2008", "Der Riese", "25 puntos"), ("2013", "Origins", "25 puntos"),
                                                  ("2015", "Black Ops 3", "100 · todas"), ("2020", "Cold War", "100 · todas")], h=400),
          "Los dos tienen algo de razón", 6.0, "linea puntos", x=.5, y=.30),
    pv("Der Riese y Origins", "der_riese", "Der Riese", dur=2.4, tam=280, **_I),
    mg_en(C.contador(25, "PUNTOS", "DEBAJO DE LA MÁQUINA"), "veinticinco puntos, como quien", 2.6, "contador 25", x=.30, y=.30),
    mg_en(C.contador(100, "PUNTOS", "BLACK OPS 3 Y COLD WAR"), "y ya daba cien", 2.4, "contador 100", x=.70, y=.30),
    caso("La inflación también llegó", "a_medias", "Puntos por tirarte", "Dos mapas, luego todos", dur=2.6),

    # ---------------- gracias 1 · @markitos453 y @rafaeltroconis6615
    com("Y aquí, dos comentarios", "UgzXH0Xy7ri0iq312YN4AaABAg", dur=7.0, giro=2),
    com("Y Rafael, el del final", "Ugyr1qCVgVLyUBM_xyV4AaABAg", dur=7.0, x=.62, y=.62, giro=-2),
    mg_en(C.logro("Todos se leen", "Y se toman en cuenta"), "Todos los comentarios se leen", 2.8, "logro se leen", x=.5, y=.30),

    # ---------------- 10 · Juggernog (MG nuevo: golpes)
    puesto("Número diez", 10, "¿Cuántos golpes aguantas con Juggernog?", "ZOMBIES / TODA LA SAGA"),
    rel("La máquina roja", "juggernog", "Juggernog", "La máquina roja", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.balanza("¿Con cuántos golpes caes?", [("Al cuarto", None, "bando 1"), ("Aguantas cinco", None, "bando 2"),
                                                  ("Al sexto", None, "bando 3")]), "Unos dicen que caes al cuarto", 4.6,
          "balanza jugg", y=.50),
    ficha("La discusión llegó a una guerra", "Guerra de ediciones", "La wiki *no se ponía de acuerdo*.", "INTEL / COMUNIDAD", dur=3.0,
          x=.73),
    mg(C.golpes("Juggernog", 4, "Caes con el quinto"), de="Con Juggernog aguantas cuatro", a=("Pero en Verrückt", -.1),
       marcas=["aguantas cuatro", "golpes de zombi", "y caes", "con el quinto", "con el quinto"], nombre="golpes jugg", y=.50),
    pv("Pero en Verrückt y Shi No Numa", "verruckt", "Verrückt · 2008", dur=2.6, tam=280, **_I),
    pv("Y en TranZit, con la mejora", "tranzit", "TranZit · hasta 6", dur=2.6, tam=280, **_D),
    caso("Los tres bandos jugaron", "a_medias", "4, 5 o 6 golpes", "Depende del juego", dur=2.8),

    # ---------------- 9 · Ascension en blanco y negro
    puesto("En el nueve", 9, "El filtro en blanco y negro", "ZOMBIES / BLACK OPS 1 · MOON"),
    pv("Moon empezaba en blanco y negro", "moon", "Moon", dur=2.6, tam=300, **_D),
    mg_en(C.objetivo("¿Moon en blanco y negro?", "Dos personas, el mismo recuerdo"), "Lo jugó el día del estreno", 2.8,
          "objetivo moon", x=.30, y=.82),
    vs(("moon", "Moon · color"), ("ascension", "Ascension · gris"), de="Moon empieza a todo color", a=("Y un detalle de Ascension", -.1),
       marcas=["Moon empieza a todo color", "El mapa en blanco y negro"], ganador=1, titulo="¿Cuál era gris?"),
    pv("si tienes Quick Revive y caes", "quick_revive", "Quick Revive", dur=2.4, tam=280, **_I),
    caso("el mapa equivocado", "falso", "Moon en blanco y negro", "Era Ascension", dur=2.8),

    # ---------------- 8 · la intro de Nacht
    puesto("Número ocho", 8, "El avión de Nacht der Untoten", "ZOMBIES / WORLD AT WAR"),
    pv("La intro de los zombis de World at War", "nacht", "Nacht der Untoten", dur=2.6, tam=300, **_D),
    mg_en(C.objetivo("¿Ves caer el avión?", "Lo que recuerda mucha gente"), "empezaba con el avión cayendo", 2.6, "objetivo avion",
          x=.30, y=.82),
    rel("La intro no enseña ningún choque", "b17", "B-17", "Ya destrozado", dur=3.6, x=.77, y=.52, tam=420),
    pv("la misión Hard Landing", "hard_landing", "Hard Landing", dur=3.0, tam=320, **_I),
    ficha("La historia oficial dice", "Línea de tiempo oficial", "Un avión aliado *falla y se estrella*.", "INTEL / ZOMBIES CHRONICLES",
          dur=3.4, x=.73),
    caso("Solo que nunca te lo enseñaron", "a_medias", "El choque en la intro", "Está en la campaña", dur=2.8),

    # ---------------- 7 · Rebirth
    puesto("En el siete, Rebirth", 7, "Rebirth, el mapa de zombis", "ZOMBIES / BLACK OPS 1"),
    mg_en(C.objetivo("¿Mapa «Rebirth»?", "Empezabas atado a la silla"), "Alguien recuerda un mapa de zombis llamado", 2.8,
          "objetivo rebirth", x=.30, y=.82),
    pv("Rebirth es una misión de la campaña", "rebirth", "Rebirth · campaña", dur=3.0, tam=320, **_D),
    pv("el gas Nova 6", "nova6", "Nova 6", dur=2.4, tam=280, **_I),
    pv("en el menú de Black Ops te puedes soltar", "c_bo1", "El menú de Black Ops", dur=2.6, tam=280, **_D),
    pv("Ahí estaba Dead Ops Arcade", "dead_ops", "Dead Ops Arcade", dur=2.8, tam=300, **_I),
    mg_en(C.linea("Rebirth", [("2010", "Black Ops 1", "Misión de campaña"), ("2024", "Warzone", "Zombie Royale")], h=400),
          "Y el giro: en dos mil veinticuatro", 5.0, "linea rebirth", x=.5, y=.30),
    pv("con Zombie Royale", "rebirth_island", "Rebirth Island", dur=2.6, tam=300, **_D),
    caso("Solo se adelantó catorce años", "a_medias", "El mapa Rebirth", "Llegó en 2024", dur=2.8),

    # ---------------- crítica 2 · @ryuzakiletrasymas115
    com("Otro comentario del primer expediente", "Ugy156LaP8zrUxDtEOJ4AaABAg", dur=6.4),
    mg_en(C.logro("Todos lo sabían", "Press F"), "Todos lo sabían", 2.6, "logro press f", x=.5, y=.30),

    # ---------------- 6 · Tombstone
    puesto("Número seis", 6, "Tombstone, jugando solo en Town", "ZOMBIES / BLACK OPS 2 · TOWN"),
    rel("Unos recuerdan comprar Tombstone", "tombstone", "Tombstone Soda", "¿En solitario?", dur=3.6, x=.77, y=.52, tam=420),
    mg_en(C.balanza("Tombstone en solitario", [("Partida en solitario", False, "no aparece"),
                                               ("Cooperativa y todos se van", True, "se puede comprar")]),
          "Los dos tienen razón", 5.0, "balanza tombstone", y=.50),
    mg_en(C.contador(2000, "PUNTOS", "TIRADOS"), "Es tirar dos mil puntos", 2.6, "contador 2000", x=.30, y=.30),
    caso("No la soñaste", "verdad", "Tombstone en solitario", "Solo si te dejan solo", dur=2.8),

    # ---------------- 5 · la Thundergat
    puesto("En el cinco, la Thundergat", 5, "La Thundergat", "ZOMBIES / BLACK OPS 2 · MOB OF THE DEAD"),
    pv("Mob of the Dead, Alcatraz", "mob", "Mob of the Dead", dur=2.4, tam=300, **_D),
    rel("La Blundergat, el trabuco", "blundergat", "Blundergat", "El trabuco", dur=3.2, x=.77, y=.52, tam=420),
    mg(C.rachas("MEJORAS DE LA BLUNDERGAT", [(1, "The Sweeper"), (2, "Acid Gat"), (3, "Magmagat")], fantasma=(4, "Thundergat"),
                nota="NUNCA EXISTIÓ"),
       de="La Blundergat tiene la Sweeper", a=("La explicación más votada", -.1),
       marcas=["la Sweeper", "la Acid Gat", "la Magmagat", "Ninguna eléctrica"], nombre="rachas blundergat", x=.28, y=.50),
    rel("La explicación más votada: Electric Cherry", "electric_cherry", "Electric Cherry", "Chispas al recargar", dur=3.6,
        x=.77, y=.52, tam=420),
    caso("Viste rayos", "falso", "La Thundergat", "Eran chispas de Electric Cherry", dur=2.8),

    # ---------------- 4 · arrastrarse (MG nuevo: consola con el código)
    puesto("Número cuatro", 4, "Si caes, no te arrastres", "ZOMBIES / BLACK OPS 2"),
    mg_en(C.objetivo("¡No te muevas!", "Que te desangras más rápido"), "No te muevas, que te desangras", 2.8, "objetivo no muevas",
          x=.30, y=.82),
    mg(C.consola("_zm_laststand.gsc · BLACK OPS 2", ["laststand_bleedout( delay )", "{", "    // tiempo fijo al caer",
                                                     "    self.bleedout_time = self.bleedout_time - 1;", "    wait 1;", "}"],
                 resalta=(3, 4), nota="Nada mira si te mueves"),
       de="Es falso, y está en el código", a=("Años quedándonos quietos", -.1),
       marcas=["Es falso", "en el código", "toma un tiempo fijo", "le resta uno", "cada segundo", "A la mitad", "En ninguna parte"],
       nombre="consola desangrado", y=.48),
    caso("Años quedándonos quietos", "falso", "Arrastrarte te desangra", "Está en el código", dur=2.8),

    # ---------------- 3 · la Thundergun en Numbers (@estebancastillo67532)
    puesto("En el tres, la Thundergun", 3, "La Thundergun en la campaña", "CAMPAÑA / BLACK OPS 1 · NUMBERS"),
    com("Esteban lo recuerda así", "Ugz1Kso6Ltym85EiVR14AaABAg", dur=5.6),
    pv("la misión Numbers", "numbers", "Numbers", dur=2.6, tam=300, **_D),
    pv("en Kowloon, Hong Kong", "kowloon", "Kowloon", dur=2.6, tam=300, **_I),
    pv("hasta que sale el gas rosa", "nova6", "Nova 6", dur=2.6, tam=300, **_D),
    pv("Sacas una cinta de un casete", "gknova6", "GKNOVA6", dur=2.6, tam=300, **_I),
    pv("en el escondite de armas de Clarke", "clarke", "Clarke", dur=2.4, tam=280, **_D),
    rel("Y ahí está, colgada en la pared", "thundergun", "Thundergun", "En la campaña", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.logro("Thundergun en la campaña", "Recarga a medio cargador"), "se podía recargar a medio cargador", 3.0,
          "logro thundergun", x=.5, y=.30),
    caso("Esteban, tu recuerdo es real", "verdad", "La Thundergun en Black Ops", "Secreto de Numbers", dur=2.8),

    # ---------------- 2 · el puente de TranZit
    puesto("Número dos. El puente", 2, "El puente de TranZit", "ZOMBIES / BLACK OPS 2 · TRANZIT"),
    pv("el autobús entra al puente", "bus", "El autobús", dur=2.6, tam=300, **_D),
    mg_en(C.fallida("FIN DE LA PARTIDA", "El autobús cae del puente"), "el autobús cae y mueren todos", 2.4, "fallida bus"),
    ficha("nunca se rompe", "Lo que dicen otros", "«El puente *nunca se rompe*».", "INTEL / VIDEOS", dur=3.0, x=.73),
    mg_en(C.balanza("El puente de TranZit", [("El puente se derrumba", True, "1.ª vuelta del bus"),
                                             ("El autobús cae", False, "nunca"), ("Los del techo caen", True, "por los escombros")]),
          "El puente que une Town con la estación", 6.0, "balanza puente", y=.50),
    pv("los escombros pueden tirar", "tedd", "T.E.D.D.", dur=2.6, tam=280, **_I),
    caso("El puente cayó", "a_medias", "El puente de TranZit", "Se rompe; el bus no cae", dur=2.8),

    # ---------------- 1 · la Ray Gun en Little Resistance (@SargentoCaboose; post: la voz al revés)
    puesto("Y el número uno", 1, "La Ray Gun en la campaña de World at War", "CAMPAÑA / WORLD AT WAR · LITTLE RESISTANCE"),
    com("Este lo mandó Sargento Caboose", "UgwD4kDGsO4354UhJmB4AaABAg", dur=5.6),
    pv("Misión Little Resistance", "little_resistance", "Little Resistance", dur=2.6, tam=300, **_D),
    pv("Peleliu, la playa", "peleliu", "Peleliu", dur=2.4, tam=280, **_I),
    mg_en(C.objetivo("Tres charcos", "Unos segundos en cada uno"), "te paras en tres charcos", 2.8, "objetivo charcos", x=.30, y=.82),
    mg_en(C.radio("PELELIU · 1944", "Escucha."), ("Escucha|fin", -.4), 3.6, "radio raygun", x=.5, y=.20),
    rel("salen de la arena cuatro estatuas", "shisa", "Shisa", "Perro león de Okinawa", dur=3.6, x=.77, y=.52, tam=420),
    pv("cada una con una Ray Gun", "raygun", "Ray Gun", dur=2.6, tam=300, **_I),
    mg_en(C.contador(2, "DISPAROS", "PARA UN TANQUE"), "Revienta un tanque con dos disparos", 2.6, "contador 2", x=.30, y=.30),
    mg_en(C.descifra("ROTCIDNEFED", "DEFIENDAN", "MENSAJE AL REVÉS", "Radio de un soldado japonés"), "Esa voz rara es un mensaje",
          4.6, "descifra radio", x=.5, y=.36),
    sil("Jesse Snyder, de Treyarch", "jesse", "Jesse Snyder", "Treyarch", lado="izq", dur=3.8),
    mg_en(C.fallida("CASI DESPEDIDO", "La escondió sin consultar a nadie"), "casi lo despiden por eso", 2.6, "fallida despedido"),
    caso("No te lo inventaste, Sargento", "verdad", "La Ray Gun en World at War", "Secreto de Little Resistance", dur=3.0),

    # ---------------- cierre (@Heckgüne17, @AholicChaffyGRS, @SargentoCaboose «Sub 106»)
    mg_en(C.sello("EXPEDIENTE CERRADO", "141"), "Expediente cerrado", 2.4, "sello cerrado", x=.5, y=.46),
    mg_en(C.balanza("Veinte efectos Mandela", [("Falsos", False, "9"), ("A medias", None, "7"), ("Eran verdad", True, "4")]),
          "y los dos mejores me los dieron", 3.6, "balanza cierre", y=.50),
    com("Como Heckgüne", "UgyG9c7xzn48lbSEiMp4AaABAg", dur=4.2, giro=2),
    com("O el de Aholic", "UgzJbnxtGKQ91KhzmI14AaABAg", dur=4.2, x=.62, y=.62, giro=-2),
    com("Y el mismo Sargento Caboose", "UgzP97FZO4mSrI2s3xt4AaABAg", dur=4.2, x=.40, y=.40, giro=1),
    mg_en(C.objetivo("¿Qué recuerdas tú?", "Escríbelo en los comentarios"), "Escríbelo", 3.2, "objetivo comentarios", x=.30, y=.82),
    mg_en(C.logro("Sale en el siguiente expediente", "Si tu efecto es bueno"), "sale en el siguiente expediente", 2.8,
          "logro siguiente", x=.5, y=.30),
    pv("las tres partes de los efectos", "c_waw", "Efectos Mandela · 3 partes", dur=2.6, tam=300, **_I),
    mg_en(C.objetivo("Suscríbete", "El siguiente expediente te llega primero"), "Suscríbete", 3.0, "objetivo suscribete", x=.30, y=.82),
    mg_en(C.sello("RETÍRATE, SOLDADO", "EXPEDIENTE 141"), "Retírate, soldado", 3.0, "sello retirate", x=.5, y=.46),
]

ROTULOS = [
    dict(texto="SE DESMAYA", en="Nixon grita, y se desmaya", tam=150, color="amarillo", y=.22, dur=1.8),
    dict(texto="POR UNA RAZÓN", en="Algunas cosas se olvidan", tam=120, color="amarillo", y=.22, dur=2.0),
    dict(texto="NO ERAN ZOMBIS", en="Solo que eran vietnamitas", tam=120, color="amarillo", y=.22, dur=1.8),
    dict(texto="SOLO SPEED COLA", en="Solo una máquina: Speed Cola", tam=120, color="amarillo", y=.22, dur=1.8),
    dict(texto="TRES VECES", en="se compra hasta tres veces", tam=150, color="amarillo", y=.86, dur=1.6),
    dict(texto="NO ESTABA LOCO", en="No lo estaba", tam=130, color="amarillo", y=.22, dur=1.6),
    dict(texto="EL MISMO ESCUDO", en="El escudo es el mismo", tam=120, color="amarillo", y=.22, dur=1.8),
    dict(texto="∞ / 15", en="solo hace quince de daño", tam=170, color="amarillo", y=.86, dur=1.8),
    dict(texto="CAES CON EL QUINTO", en="y caes con el quinto", tam=110, color="amarillo", y=.86, dur=1.8),
    dict(texto="ERA ASCENSION", en="El mapa en blanco y negro es Ascension", tam=130, color="amarillo", y=.22, dur=1.8),
    dict(texto="SE ADELANTÓ 14 AÑOS", en="Solo se adelantó catorce años", tam=110, color="amarillo", y=.22, dur=2.0),
    dict(texto="NUNCA EXISTIÓ", en="Nunca existió. La Blundergat", tam=150, color="amarillo", y=.22, dur=1.6),
    dict(texto="−1 CADA SEGUNDO", en="le resta uno cada segundo", tam=120, color="amarillo", y=.86, dur=1.8),
    dict(texto="ES REAL", en="Y es verdad. Es un secreto", tam=170, color="amarillo", y=.22, dur=1.4),
    dict(texto="EL AUTOBÚS, NUNCA", en="El autobús, nunca", tam=120, color="amarillo", y=.22, dur=1.8),
    dict(texto="CASI LO DESPIDEN", en="casi lo despiden por eso", tam=120, color="amarillo", y=.22, dur=1.8),
]

SFX = {}
# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/cod/ → sfx/cod_*.mp3), solo en momentos clave
PISTAS = [
    dict(sfx="cod_sello", en="Expediente ciento", vol=.30),
    dict(sfx="cod_fallida", en="A los dos les dijeron", vol=.22),
    dict(sfx="cod_puesto", en="Número veinte. Nixon", vol=.24),
    dict(sfx="cod_puesto", en="Número dieciocho", vol=.22),
    dict(sfx="cod_puesto", en="Número quince", vol=.22),
    dict(sfx="cod_fallida", en="le dijeron que estaba loco", vol=.22),
    dict(sfx="cod_logro", en="Guárdala en la memoria", vol=.22),
    dict(sfx="cod_puesto", en="Número diez", vol=.22),
    dict(sfx="cod_logro", en="Todos los comentarios se leen", vol=.22),
    dict(sfx="cod_puesto", en="Número seis", vol=.22),
    dict(sfx="cod_puesto", en="Número cuatro", vol=.22),
    dict(sfx="cod_logro", en="se podía recargar a medio cargador", vol=.24),
    dict(sfx="cod_fallida", en="el autobús cae y mueren todos", vol=.24),
    dict(sfx="cod_puesto", en="Y el número uno", vol=.26),
    dict(sfx="cod_fallida", en="casi lo despiden por eso", vol=.24),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco (post), a nivel de voz
    dict(sfx="s_nixon", en=("Escucha cómo termina en realidad|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_nikolai", en=("La frase real es esta|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_dentista", en=("suena un taladro", -.2), vol=.75),   # taladro + grito de la silla de Verrückt (bKW8Mur3y80 11,8-16 s), bajo la voz
    dict(sfx="s_raygun", en=("unos segundos en cada uno. Escucha|fin", .1), vol=1.0, voz=True),
]

# ---- 2.ª pasada (chequeo 22-nov: fichas 0,6/min contra 1,4 del canal; pegatinas 3,7 contra 5,6)
_I2, _D2 = dict(x=.18, y=.64, tam=280), dict(x=.80, y=.62, tam=280)
FX += [
    pv("Uno de ustedes me escribió", "c_waw", "World at War · 2008", **_I2),
    pv("Lo revisé todo", "c_bo2", "Black Ops 2", dur=2.2, **_D2),
    pv("Hay quien recuerda que Nixon", "nixon", "¿Nixon zombi?", **_D2),
    pv("Un segundo después sale", "five", "La armería", dur=2.6, **_D2),
    pv("Hay quien jura que gritaba", "nikolai", "Nikolai", **_I2),
    pv("Alguien recuerda un mapa de zombis de Black Ops 1", "kino", "¿Qué mapa?", **_I2),
    pv("No lo va a encontrar", "five", "Tampoco «Five»", dur=2.2, **_D2),
    pv("Hay quien recuerda, de niño", "nacht", "El zombi de siempre", **_I2),
    pv("Si activas la silla del dentista", "verruckt", "La silla", dur=2.4, **_I2),
    pv("Un jugador recordaba una Remington", "town", "Town · el banco", dur=2.4, **_I2),
    pv("en el granero de la Granja", "farm", "La Granja", **_I2),
    pv("y fuera de la estación de autobuses", "bus_depot", "La estación", **_D2),
    pv("Un jugador recuerda haber tenido", "c_bo1", "Black Ops 1", dur=2.4, **_I2),
    pv("No lo estaba. La Type 100", "type100", "Type 100", dur=2.4, **_I2),
    pv("Es un mito de patio de recreo", "richtofen", "Richtofen", dur=2.4, **_I2),
    pv("Tiene razón. De cerca", "thundergun", "Thundergun", dur=2.4, **_I2),
    pv("Unos juran que en Black Ops 1 y 2", "perk_cola", "¿Cuerpo a tierra?", **_I2),
    pv("En Black Ops 3 y en Cold War", "c_cw", "Cold War", dur=2.4, **_D2),
    pv("Otros, que aguantas cinco", "juggernog", "¿Cinco golpes?", dur=2.4, **_I2),
    pv("Un jugador recuerda que Moon", "moon", "Moon · 2011", **_I2),
    pv("todo gris hasta que das la luz", "ascension", "Ascension", dur=2.4, **_D2),
    pv("Mucha gente recuerda que empezaba con el avión", "b17", "¿El choque?", **_I2),
    pv("Empieza con el avión ya destrozado", "nacht", "Nacht der Untoten", dur=2.4, **_I2),
    pv("Ese mapa no existe", "rebirth", "Rebirth", dur=2.4, **_I2),
    pv("La silla sí es real", "dead_ops", "La silla del menú", dur=2.4, **_D2),
    pv("Unos recuerdan comprar Tombstone", "town", "Town", dur=2.2, **_I2),
    pv("Hay quien jura que tenía una tercera mejora", "blundergat", "¿Thundergat?", **_I2),
    pv("En Black Ops 2, al caer", "c_bo2", "Black Ops 2", dur=2.2, **_D2),
    pv("Disparas a seis bombonas blancas", "nova6", "Nova 6", dur=2.2, **_I2),
    pv("Alguien recuerda a su hermano jugando", "tranzit", "TranZit", **_I2),
    pv("Este lo mandó Sargento Caboose", "raygun", "La Ray Gun", dur=2.4, **_D2),
    pv("Esa voz rara es un mensaje", "peleliu", "Peleliu · 1944", dur=2.6, **_I2),
    ficha("Black Ops, el mapa Five", "«Five»", "El Pentágono, *1963*.", "INTEL / BLACK OPS", dur=3.0, x=.73),
    ficha("Hay quien recuerda que Nixon", "Lo que recuerdan", "Nixon *se transforma* delante de todos.", "INTEL / COMUNIDAD", dur=3.0),
    ficha("Alguien recuerda un mapa de zombis de Black Ops 1", "El recuerdo", "Un edificio *en llamas*.", "INTEL / COMUNIDAD", dur=3.0, x=.73),
    ficha("Hay quien recuerda, de niño", "El recuerdo", "Un zombi que *te seguía* con ruidos.", "INTEL / COMUNIDAD", dur=3.0),
    ficha("Un jugador recordaba una Remington", "Remington 870 MCS", "La escopeta *de la pared*.", "INTEL / BLACK OPS 2", dur=3.0, x=.73),
    ficha("La máquina azul de Quick Revive", "Quick Revive en solitario", "Te levantas *tú mismo*.", "INTEL / PERKS", dur=3.0),
    ficha("Un jugador recordaba una Type 100", "Type 100", "Subfusil *japonés* de 1940.", "INTEL / ARMAS", dur=3.0),
    ficha("En las partidas con amigos alguien", "El mito", "El escudo de Richtofen *aguanta más*.", "INTEL / COMUNIDAD", dur=3.0, x=.73),
    ficha("Unos juran que en Black Ops 1 y 2", "Cuerpo a tierra", "Tirarte *frente a la máquina*.", "INTEL / PERKS", dur=3.0, x=.73),
    ficha("Un jugador recuerda que Moon", "Moon", "Black Ops · *2011* · la Luna.", "INTEL / BLACK OPS", dur=3.0, x=.73),
    ficha("Mucha gente recuerda que empezaba con el avión", "La intro", "World at War · *2008*.", "INTEL / WORLD AT WAR", dur=3.0, x=.73),
    ficha("Rebirth es una misión de la campaña", "Rebirth", "Isla *Vozrozhdéniya* · mar de Aral.", "INTEL / CAMPAÑA", dur=3.2, x=.73),
    ficha("Unos recuerdan comprar Tombstone", "Tombstone Soda", "Te deja *tus armas* al morir.", "INTEL / PERKS", dur=3.0),
    ficha("Mob of the Dead, Alcatraz", "Mob of the Dead", "Alcatraz · *Black Ops 2*.", "INTEL / ZOMBIES", dur=3.0, x=.73),
    ficha("Black Ops 2. Alguien recuerda", "TranZit", "El mapa *del autobús*.", "INTEL / BLACK OPS 2", dur=3.0, x=.73),
    ficha("Misión Little Resistance", "Little Resistance", "Peleliu · *1944*.", "INTEL / WORLD AT WAR", dur=3.0, x=.73),
]
