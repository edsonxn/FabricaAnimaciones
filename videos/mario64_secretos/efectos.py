# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Super Mario 64: su historia y los 20 secretos QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming, 29-oct-2026).
Kit NUEVO `nucleo/mg_mario64.py` con la interfaz del propio juego sobre humo negro TRANSLÚCIDO (regla del 22-oct):
- `puesto` = la selección de estrella (Estrella de poder que gira + «SECRETO N.º N» con las letras del logo + -título-);
  `ficha` = el cuadro de diálogo del juego (texto que se escribe y triángulo rojo).
- PEGATINAS reales de lo que nombra la voz (pegatinas/, Super Mario Wiki + Wikipedia; bajar_pegatinas.py).
- MG NUEVOS de ESTE guion: `mando` (cruceta 8 direcciones contra stick de 360 grados y sus tres velocidades), `reloj_ttc`
  (minutero 12/3/6/9 → detenido/lento/al azar/rápido), `agua` (la altura del salto al cuadro decide el agua de Wet-Dry World),
  `boton_a` (1 → medio → 0 pulsados), `bit` (un rayo cambia un bit de la altura de Mario), `estrellas` (contador del HUD) y
  `linea_tiempo` (el desarrollo).
- MAPAS REALES con ruta (regla del 23/29-oct): el castillo de Peach de VGMaps (montaje isométrico con modelos del juego) para
  MIPS, el Acuario y el foso, el cuadro de Peach, Tick Tock Clock, la escalera, Yoshi en el tejado y la placa del patio; y
  Jolly Roger Bay (Unagi) y Cool, Cool Mountain (los pingüinos). Tema `mario64` de mg_mapa (monedas + Estrella de poder).
- SFX DEL JUEGO (regla del 29-oct): sfx/m64_*.mp3 recortados de videos de un solo sonido (moneda, estrella, 1-up…).
  python fab.py mario64_secretos fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py mario64_secretos fx         audio/fx.wav
"""
import os

import mg_mario64 as M

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .42     # fichas: a la derecha (el rótulo del secreto va arriba)

CAMARA = {}
FUNDIDO = {}


def _img(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=M.pegatina(_img(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(en, items, y=.66, tam=320, dur=5.0):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    paso = max(.17, (tam + 90) / 1920)
    return [peg(a or en, s, t, dur=dur, x=.12 + paso * i, y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY):
    d = dict(tipo="mg", fn=M.ficha(titulo, texto, tipo=tipo), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, dur=4.2):
    return dict(tipo="mg", fn=M.puesto(num, titulo), en=en, dur=dur, x=.5, y=.15, sale=.45, nombre=f"secreto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, recorte=None, **kw):
    """Mapa REAL con ruta (tema mario64). `puntos` en fracciones de la imagen ENTERA (como en la rejilla); con `recorte`
    se pasan solos al recorte."""
    import mg_mapa as MP
    ruta = next(os.path.join(_MAP, slug + e) for e in (".png", ".jpg") if os.path.exists(os.path.join(_MAP, slug + e)))
    if recorte:
        x0, y0, x1, y1 = recorte
        puntos = [((p[0] - x0) / (x1 - x0), (p[1] - y0) / (y1 - y0)) + tuple(p[2:]) for p in puntos]
    puntos = [p[:4] + ((_img(p[4]) if len(p) > 4 and p[4] else None),) if len(p) > 4 else p for p in puntos]
    fn = MP.mapa(ruta, puntos, "mario64", titulo=titulo, sub=sub, recorte=recorte,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


_CASTILLO = "peachscastle"
FX = [
    # ================================================================ GANCHO
    grande("En el patio del castillo de Peach", "placa", "La placa del patio", lado="der", dur=6.6, tam=640),
    ficha("Durante décadas, media generación", "La leyenda", "«*L is real 2401*»", tipo="Lo que juraba media generación",
          a=("escondido en el juego|fin", .4), x=.27, y=.40),
    peg("Y que Luigi estaba escondido", "luigi_modelo", "Luigi", tam=360, x=.80, y=.60, dur=3.6),
    peg("Super Mario 64 cumplió treinta años", "caja_jp", "Super Mario 64 (1996)", tam=440, x=.78, y=.52, dur=5.4),
    peg("el mismo día que la Nintendo 64", "n64", "Nintendo 64", tam=420, x=.22, y=.64, dur=4.2),
    ficha("Salió en Japón el 23 de junio de 1996", "30 años", "Japón: *23 de junio de 1996*. El mismo día que la consola.",
          tipo="Aniversario: 23 de junio de 2026", a=("el mismo día que la Nintendo 64|fin", .8), x=.70, y=.36),
    *fila("Desde un conejo con nombre", [("mips", "MIPS", "un conejo"), ("estrella", "Estrella de poder", "un rayo cósmico")],
          tam=330, dur=5.4),

    # ================================================================ HISTORIA 1 / UN MARIO EN 3D
    peg("Shigeru Miyamoto ya pensaba", "miyamoto", "Shigeru Miyamoto", tam=420, x=.20, y=.60, dur=5.0),
    fila("mientras su equipo hacía Star Fox", [("snes", "Super Nintendo", None)], tam=380, y=.64, dur=4.0)[0] | dict(x=.80),
    ficha("Mucha gente cree que existió", "Mito", "«Super Mario FX» era el nombre interno del *chip*, no un juego.",
          tipo="Según Dylan Cuthbert (Star Fox)", a=("No hay pruebas de ese juego|fin", .5)),
    peg("Pero Dylan Cuthbert", "superfx", "Chip Super FX", tam=360, x=.20, y=.64, dur=5.4),
    peg("Yoshiaki Koizumi recuerda", "koizumi", "Yoshiaki Koizumi", tam=420, x=.20, y=.60, dur=5.6),
    ficha("Koizumi cuenta que, a las dos", "Iwata pregunta", "Miyamoto, sobre un escritorio a las *3 de la mañana*, "
          "enseñando cómo nada Mario.", tipo="Según Yoshiaki Koizumi", a=("algo así|fin", .4)),
    ficha("Según un documento de copyright", "Desarrollo", "*622 días*: del 7 de septiembre de 1994 al 20 de mayo de 1996.",
          tipo="Documento filtrado en 2020", a=("al 20 de mayo de 1996|fin", .8), x=.27, y=.40),
    *fila("Lo hizo un equipo de unas quince", [("miyamoto", "Miyamoto", None), ("koizumi", "Koizumi", None),
                                               ("tezuka", "Takashi Tezuka", None)], tam=280, dur=4.4),
    peg("Y el compositor Koji Kondo", "kondo", "Koji Kondo", tam=380, x=.80, y=.58, dur=5.2),
    mg(M.linea_tiempo([("1993", "Star Fox"), ("1994", "Empieza el desarrollo"), ("1995", "Shoshinkai: al 50 %"),
                       ("1996", "Sale en Japón")], titulo="Super Mario 64, paso a paso"),
       ("Lo hizo un equipo", -.2), ("límites de memoria|fin", .3),
       ["equipo de unas quince", "veinte personas", "Koji Kondo", "ocho meses"], "linea", y=.70),

    # ================================================================ HISTORIA 2 / EL MANDO Y LA CÁMARA
    peg("La cruceta solo tiene ocho", "mando", "Mando de Nintendo 64", tam=440, x=.78, y=.56, dur=5.4),
    mg(M.mando(), ("La cruceta solo tiene ocho", -.1), ("según cuánto inclinaras el pulgar|fin", .6),
       ["ocho direcciones", "un stick analógico", "caminar de puntillas"], "mando", y=.62),
    grande("La cámara la llevan los hermanos Lakitu", "lakitu", "Los hermanos Lakitu", lado="der", dur=5.6, tam=520),
    peg("como un equipo de televisión", "camara", "La cámara", tam=320, x=.20, y=.62, dur=3.4),
    peg("Miyamoto contó que ese sistema", "castillo", "El castillo de Peach", tam=480, x=.76, y=.54, dur=5.4),
    peg("cambiaron la bandera por estrellas", "estrella", "Estrella de poder", tam=360, x=.22, y=.60, dur=4.0),

    # ================================================================ HISTORIA 3 / SHOSHINKAI Y EL LANZAMIENTO
    ficha("Estaba más o menos al cincuenta", "Shoshinkai 1995", "Al *50 %*. De *32 niveles* planeados quedaron *15*.",
          tipo="24-26 de noviembre de 1995", a=("Al final quedaron quince|fin", .6)),
    peg("En esa demo, la vida", "panfleto", "Folleto de la demo", tam=420, x=.22, y=.58, dur=5.6),
    peg("Miyamoto lo admitió", "miyamoto", "Shigeru Miyamoto", tam=340, x=.20, y=.62, dur=3.6),
    peg("según Howard Lincoln", "lincoln", "Howard Lincoln", tam=340, x=.80, y=.60, dur=4.4),
    *fila("Super Mario 64 salió en Japón el 23", [("caja_jp", "Japón", None), ("caja_pal", "Europa", "Y en Europa")],
          tam=320, dur=6.2),
    mg(M.estrellas("Ventas", [(2, "millones en 3 meses (Norteamérica)"), (12, "millones en total: el más vendido de su "
                                                                            "generación")]),
       ("Solo en Norteamérica vendió", -.1), ("su generación de consolas|fin", .5), ["más de dos millones", "casi doce millones"],
       "ventas", y=.62, x=.70),
    *fila("En 1997 salió en Japón una versión", [("caja_ds", "Super Mario 64 DS", "un remake para la Nintendo DS")],
          tam=380, dur=4.0),
    peg("En 2020 volvió en Super Mario 3D All-Stars", "caja_3das", "3D All-Stars (2020)", tam=420, x=.20, y=.58, dur=4.4),
    peg("hoy se puede jugar en Nintendo Switch Online", "switch", "Nintendo Switch Online", tam=320, x=.80, y=.60, dur=3.4),
    *fila("En 2026 lo hicieron correr en una 3DO", [("tres_do", "3DO", "una 3DO"), ("n3ds", "Nintendo 3DS", "una 3DS"),
                                                   ("snes", "Super Nintendo", "una Super Nintendo real")], tam=300, dur=6.4),

    # ================================================================ 20 / MIPS
    puesto("Número veinte", 20, "El conejo con nombre de máquina"),
    mapa(_CASTILLO, [(.605, .79, "Puerta del sótano", "inicio"), (.63, .765), (.668, .745, "MIPS", "meta", "mips")],
         de=("En el sótano del castillo", -.1), a=("Se llama MIPS|fin", .6), marcas=["En el sótano", "Se llama MIPS"],
         titulo="Sótano del castillo", ventana=True, recorte=(.50, .66, .92, .90)),
    ficha("MIPS es la arquitectura", "MIPS", "El nombre del *procesador* de la Nintendo 64.", tipo="El conejo del sótano",
          a=("de la propia Nintendo 64|fin", .8), x=.27),
    grande("cada vez que perseguías", "mips", "MIPS", lado="der", dur=5.6, tam=520),

    # ================================================================ 19 / LAKITU
    puesto("Número diecinueve", 19, "La cámara tiene nombre y apellido"),
    peg("un Lakitu con una cámara", "lakitu", "Lakitu", tam=420, x=.80, y=.58, dur=5.4),
    peg("Si te miras en un espejo", "camara", "El camarógrafo", tam=340, x=.20, y=.62, dur=4.6),

    # ================================================================ 18 / UNAGI
    puesto("Número dieciocho", 18, "La estrella en la cola"),
    mapa("jollyrogerbay", [(.81, .665, "Entrada", "inicio"), (.66, .56), (.52, .47), (.41, .40, "Unagi", "meta", "unagi")],
         de=("En Jolly Roger Bay, la Bahía", -.1), a=("en ningún cofre|fin", .4), marcas=["Jolly Roger Bay", "una anguila enorme"],
         titulo="Jolly Roger Bay", sub="Bahía del Capitán", recorte=(.28, .02, .98, .76)),
    grande("Brilla en la punta de su cola", "unagi", "Unagi", lado="der", dur=5.8, tam=600),
    peg("Brilla en la punta de su cola", "estrella", "La estrella", tam=300, x=.22, y=.40, dur=4.4),

    # ================================================================ 17 / PINGÜINO
    puesto("Número diecisiete", 17, "El pingüino que no es tuyo"),
    mapa("coolcoolmountain", [(.505, .17, "La cima: el bebé", "inicio", "pinguino_beta"), (.47, .40), (.53, .62),
                              (.58, .82, "Mamá pingüino", "meta", "pinguino")],
         de=("En Cool, Cool Mountain", -.1), a=("muy parecido|fin", .2), marcas=["su bebé perdido", "Pero en el nivel"],
         titulo="Cool, Cool Mountain", sub="Montaña Helada", recorte=(.34, .04, .72, .92)),
    peg("Y si le llevas ese", "pinguinos", "¿Cuál es su bebé?", tam=460, x=.76, y=.56, dur=5.6),
    ficha("Te dice que no es su hijo", "Mamá pingüino", "«Este no es mi bebé. Sus papás deben estar *preocupados*.»",
          tipo="Lo que te dice", a=("preocupados por él|fin", .8), x=.27),
    peg("la mamá te persigue", "pinguino", "Mamá pingüino", tam=380, x=.78, y=.58, dur=4.0),

    # ================================================================ 16 / BAJO EL AGUA
    puesto("Número dieciséis", 16, "Los secretos bajo el agua"),
    ficha("Ese castillo no existe", "Mito", "*No hay* un castillo secreto bajo el agua.", tipo="Rumor de patio de escuela",
          dur=3.6),
    mapa(_CASTILLO, [(.88, .63, "Jolly Roger Bay", "inicio", "cuadro_jrb"), (.77, .635, "El Acuario Secreto", "paso"),
                     (.74, .72), (.82, .86), (.90, .92, "Pilares del sótano", "paso"), (.955, .955, "El foso", "meta", "gorro_invisible")],
         de=("Lo que sí existe es el Acuario", -.1), a=("el gorro de invisibilidad|fin", .6),
         marcas=["a la derecha del cuadro", "Acuario Secreto", "sobre dos pilares", "el agua del foso"],
         titulo="El castillo de Peach", sub="Los secretos del agua", recorte=(.50, .40, 1.0, 1.0)),

    # ================================================================ 15 / DIRE DIRE DOCKS
    puesto("Número quince", 15, "La música que te sigue"),
    peg("Koji Kondo hizo que la música", "kondo", "Koji Kondo", tam=380, x=.20, y=.60, dur=5.0),
    ficha("No suena igual en todo el nivel", "Dire, Dire Docks", "Según la zona se suman *sintetizadores* y luego "
          "*percusión*.", tipo="Gran Muelle", a=("luego la percusión|fin", .6)),

    # ================================================================ 14 / EL CUADRO DE PEACH
    puesto("Número catorce", 14, "El cuadro que te mira"),
    mapa(_CASTILLO, [(.706, .505, "Puerta de 8 estrellas", "inicio"), (.70, .43), (.69, .36, "El cuadro de Peach", "meta",
                                                                                         "cuadro_peach")],
         de=("Cuando abres la puerta de ocho", -.1), a=("un retrato de la princesa Peach|fin", .6),
         marcas=["la puerta de ocho estrellas", "un retrato de la princesa"], titulo="Primer piso", ventana=True,
         recorte=(.56, .30, .84, .56)),
    *fila("la cara de Peach se transforma", [("cuadro_peach", "Peach", None), ("cuadro_bowser", "Bowser", "en la de Bowser")],
          tam=340, dur=5.4),
    ficha("Caes directo a Bowser", "El truco", "El cuadro *no se puede tocar*: hay una pared invisible delante.",
          tipo="Bowser in the Dark World", a=("una pared invisible delante|fin", .6)),

    # ================================================================ 13 / YOSHI
    puesto("Número trece", 13, "El premio de las 120 estrellas"),
    mg(M.estrellas("Estrellas de poder", [(70, "Para el final"), (120, "El tejado se abre")]),
       ("Si consigues las 120 estrellas", -.1), ("subir al tejado del castillo|fin", .3), ["las 120 estrellas", "el cañón"],
       "120", y=.60, x=.70),
    mapa(_CASTILLO, [(.297, .705, "El cañón", "inicio"), (.32, .62), (.37, .55), (.42, .50, "Yoshi", "meta", "yoshi")],
         de=("Y ahí te espera Yoshi", -.3), a=("deja una estela de destellos|fin", .4), marcas=["te espera Yoshi", "Te da un mensaje"],
         titulo="Jardines del castillo", sub="El tejado", recorte=(.02, .38, .60, .80)),
    peg("Cien vidas, cuando ya no", "yoshi_msg", "El mensaje de Yoshi", tam=520, x=.74, y=.52, dur=5.4),

    # ================================================================ 12 / SO LONG KING BOWSER
    puesto("Número doce", 12, "La frase que todos oímos mal"),
    peg("Cuando Mario lanza a Bowser", "mario_bowser", "Mario contra Bowser", tam=520, x=.74, y=.54, dur=5.6),
    peg("Charles Martinet, la voz de Mario", "martinet", "Charles Martinet", tam=400, x=.20, y=.58, dur=5.0),
    ficha("La frase es So long", "Lo que dice", "«So long, *King* Bowser»: hasta luego, *rey* Bowser.",
          tipo="Charles Martinet, 2019", a=("Hasta luego, rey Bowser|fin", 1.4), x=.74),
    peg("en la versión de Switch", "caja_3das", "3D All-Stars", tam=360, x=.20, y=.60, dur=4.4),

    # ================================================================ 11 / ENEMIGOS BORRADOS
    puesto("Número once", 11, "Los enemigos que nunca viste"),
    ficha("Miyamoto contó que hicieron", "Enemigos", "Menos de *40* enemigos, cuando lo normal eran unos *80*.",
          tipo="Miyamoto, 1996", a=("No les dio tiempo|fin", .6)),
    *fila("Está Blargg", [("blargg", "Blargg", None), ("chill_bully", "Bully de hielo", "unos Bullies pequeños"),
                          ("motos", "Motos", "y Motos")], tam=300, dur=8.0),
    *fila("Hasta hay un huevo", [("yoshi_proto", "¿Yoshi?", None), ("hoot", "Hoot, el búho", "Y resultó ser de Hoot")],
          tam=320, dur=5.0),

    # ================================================================ 10 / LA VOZ
    puesto("Número diez", 10, "Mario no siempre tuvo su voz"),
    grande("el primer juego de la serie principal", "martinet", "Charles Martinet", lado="der", dur=6.0, tam=520),
    ficha("Pero en la demo de 1995", "Demo de 1995", "Gritos de *bibliotecas de sonido*: genéricos, de vaquero.",
          tipo="Antes de Charles Martinet", a=("de vaquero|fin", .6), x=.27),
    grande("Luego llegó Martinet", "cabeza", "It's-a me, Mario!", lado="der", dur=5.6, tam=560),

    # ================================================================ 9 / TICK TOCK CLOCK
    puesto("Número nueve", 9, "El reloj que obedece a la hora"),
    mapa(_CASTILLO, [(.603, .275, "Tick Tock Clock", "meta", "cuadro_ttc")], de=("Tick Tock Clock, el Reloj", -.1),
         a=("tercer piso del castillo|fin", .6), marcas=["un reloj de péndulo"], titulo="Tercer piso", ventana=True,
         recorte=(.52, .12, .86, .40)),
    mg(M.reloj_ttc([(0, "Detenido", 0), (15, "Lento", .12), (30, "Al azar", None), (45, "Rápido", 1.1)]),
       ("Si entras con el minutero en las doce", -.2), ("todo va rápido|fin", 1.0),
       ["en las doce", "En las tres", "En las seis", "en las nueve"], "reloj", y=.56),

    # ================================================================ 8 / WET-DRY WORLD
    puesto("Número ocho", 8, "El salto que cambia el agua"),
    mg(M.agua(_img("cuadro_wdw")), ("De la altura a la que saltas", -.2), ("de verdad usa esa división|fin", .2),
       ["Si entras por arriba", "el agua está alta", "Si entras por abajo"], "agua", y=.56),
    peg("Así que, si ese nivel", "cuadro_wdw", "Wet-Dry World", tam=380, x=.20, y=.60, dur=4.4),

    # ================================================================ 7 / LA ESCALERA
    puesto("Número siete", 7, "La escalera sin fin"),
    mapa(_CASTILLO, [(.775, .165, "La escalera", "inicio"), (.84, .10), (.912, .035, "Bowser in the Sky", "meta")],
         de=("Antes de enfrentar a Bowser por última vez", -.1), a=("y nunca llegas|fin", .5),
         marcas=["hay una escalera", "nunca llegas"], titulo="La escalera sin fin", ventana=True, recorte=(.66, .0, .99, .26)),
    ficha("Y la música es una ilusión", "Tono de Shepard", "Una escala que parece *subir para siempre*, aunque se repite.",
          tipo="La música de la escalera", a=("en realidad se repite|fin", .8)),
    peg("Y la música es una ilusión", "shepard", "Tono de Shepard", tam=380, x=.20, y=.60, dur=5.0),

    # ================================================================ 6 / LA CABEZA
    puesto("Número seis", 6, "La cara de las pelotas de ping-pong"),
    grande("Al encender el juego, aparece la cabeza", "cabeza", "La cabeza de Mario", lado="der", dur=6.0, tam=560),
    peg("Se pegó pelotas de ping-pong", "sgi_indy", "Estación SGI Indy", tam=420, x=.78, y=.56, dur=5.6),
    peg("Koizumi le preparó una cara", "koizumi", "Yoshiaki Koizumi", tam=340, x=.20, y=.60, dur=4.0),
    peg("Miyamoto pasó, la vio", "miyamoto", "Shigeru Miyamoto", tam=340, x=.80, y=.60, dur=4.0),
    ficha("Ojo, en otra entrevista", "Discutido", "En otra entrevista, Goddard lo cuenta *sin las pelotas*.",
          tipo="Giles Goddard", a=("la pantalla de título más famosa|fin", -1.0), x=.27),

    # ================================================================ 5 / EL CEREBRO
    puesto("Número cinco", 5, "El juego que agranda el cerebro"),
    peg("el Instituto Max Planck", "max_planck", "Instituto Max Planck", tam=440, x=.76, y=.56, dur=5.6),
    ficha("Pusieron a un grupo de adultos", "El estudio", "*30 minutos* al día durante *2 meses*: más materia gris.",
          tipo="Kühn et al., Molecular Psychiatry, 2013", a=("la memoria y la planificación|fin", .6), x=.27),
    peg("Jugaron la versión de Nintendo DS", "nds", "Nintendo DS", tam=380, x=.80, y=.58, dur=4.0),

    # ================================================================ 4 / BLJ
    puesto("Número cuatro", 4, "Terminar el juego con cero estrellas"),
    ficha("la velocidad se acumula sin límite", "Backwards Long Jump", "Saltos largos de espaldas: la velocidad "
          "*crece sin límite*.", tipo="El salto largo hacia atrás", a=("las puertas que piden estrellas|fin", .6)),
    peg("Nintendo lo corrigió en la versión Shindou", "caja_jp", "Versión Shindou (1997)", tam=360, x=.20, y=.60, dur=4.6),
    mg(M.estrellas("Suigi, récords del mundo", [(0, "estrellas: poco más de 6 minutos"), (120, "estrellas: 1 h 35 min 14 s")]),
       ("El récord actual con cero estrellas", -.1), ("de abril de este año|fin", .4), ["con cero estrellas", "el de 120"],
       "suigi", y=.60, x=.70),
    ficha("Tiene los cinco récords", "La bolsa", "Unos *10 000 dólares* para quien le quite un récord.",
          tipo="Nadie lo ha conseguido", a=("Nadie lo ha conseguido|fin", .8), x=.27),

    # ================================================================ 3 / MEDIO BOTÓN A
    puesto("Número tres", 3, "Medio botón A"),
    mapa("hazymazecave", [(.30, .06, "Entrada", "inicio"), (.37, .20), (.45, .36),
                          (.535, .452, "Watch for Rolling Rocks", "meta", "estrella")],
         de=("una estrella de Hazy Maze Cave", -.1), a=("con medio pulsado|fin", .4),
         marcas=["Hazy Maze Cave", "la Cueva del Laberinto"], titulo="Hazy Maze Cave", sub="Cueva del Laberinto",
         ventana=True, recorte=(.18, .0, .66, .62)),
    mg(M.boton_a([("1", 1.0, "Lo normal: pulsar"), ("0,5", .5, "Medio pulsado: ya venía apretado"),
                  ("0", 0.0, "En 2023: cero")]),
       ("El reto era sacarla pulsando", -.1), ("de otra parte del nivel|fin", .3), ["el menor número", "con medio pulsado",
                                                                                  "ya venía apretado"], "botona", y=.56),
    ficha("pero primero, tenemos que hablar", "El meme", "«Pero primero, tenemos que hablar de *universos paralelos*.»",
          tipo="pannenkoek, 2016", a=("más famosos de internet|fin", .6), x=.5, y=.40),
    ficha("En 2023 bajó esa estrella a cero", "Sin botón A", "En mayo de 2024, el juego entero sin pulsar A: *86 horas*.",
          tipo="Versión de Consola Virtual de Wii", a=("Le llevó 86 horas|fin", .8), x=.27),

    # ================================================================ 2 / EL RAYO CÓSMICO
    puesto("Número dos", 2, "El rayo cósmico"),
    ficha("Nadie pudo repetirlo", "La recompensa", "*1 000 dólares* para quien lo repitiera. Nadie los cobró.",
          tipo="pannenkoek, 2015", a=("a quien lo consiguiera|fin", .8), x=.27),
    mg(M.bit(), ("Al analizar el valor de la altura", -.1), ("y cambió ese bit|fin", .6),
       ["la altura de Mario", "un solo bit", "un rayo cósmico"], "bit", y=.56),
    ficha("Ojo, no está probado", "Hipótesis", "*No está probado*: también pudo ser un cartucho mal puesto o un fallo.",
          tipo="El rayo cósmico", a=("una explicación mejor|fin", .6), x=.27),

    # ================================================================ 1 / LUIGI
    puesto("Número uno", 1, "Luigi era real"),
    mapa(_CASTILLO, [(.895, .475, "La estatua del patio", "meta", "placa")], de=("Recuerda la placa del patio", -.1),
         a=("Nadie los cobró|fin", .4), marcas=["la placa del patio"], titulo="El patio", ventana=True, recorte=(.74, .38, 1.0, .62)),
    ficha("Y en 1998, Nintendo of America", "Nintendo of America, 1998", "«Una *broma* de los programadores.»",
          tipo="Respuesta por carta", a=("una broma de los programadores|fin", .8), x=.27),
    grande("Pero Luigi sí estuvo en el juego", "luigi_modelo", "Luigi", lado="der", dur=6.4, tam=600),
    ficha("Miyamoto lo dijo en 1996", "Miyamoto, 1996", "«Hasta *febrero*, estaba en el juego.»", tipo="Entrevista de 1996",
          a=("estaba en el juego|fin", .6), x=.27),
    ficha("Koizumi lo resumió así", "Yoshiaki Koizumi", "«Con *lágrimas*, tuvimos que pedirle a Luigi que se fuera.»",
          tipo="Iwata pregunta", a=("que se fuera|fin", 1.0), x=.27),
    grande("En 2020, una filtración enorme", "luigi_modelo", "El modelo de Luigi (2020)", lado="izq", dur=6.0, tam=520),
    grande("Y en octubre de 2026, el programador", "placa", "La placa", lado="der", dur=7.0, tam=600),
    ficha("La que mejor encaja no dice", "La placa, según Mochi64", "«*Eternal Star*. We hope so.»",
          tipo="Estrella eterna. Eso esperamos.", a=("Eso esperamos|fin", 1.6), x=.27, y=.40),
    ficha("No es una confirmación de Nintendo", "Ojo", "La mejor coincidencia *estadística*: Nintendo no lo ha confirmado.",
          tipo="Unas 530 tipografías probadas", dur=5.0, x=.27),

    # ================================================================ CIERRE
    *fila("Esos son los veinte secretos", [("mips", "MIPS", None), ("escalera", "La escalera", "una escalera que mentía"),
                                          ("estrella", "Estrella de poder", "un rayo del espacio")], tam=300, dur=7.0),
]
ROTULOS = []
SFX = {}
# SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/m64_*.mp3
PISTAS = [
    dict(sfx="m64_herewego", en="Hoy te cuento cómo se hizo", vol=.55),
    dict(sfx="m64_cuadro", en="Y ahora sí, vamos con los veinte secretos", vol=.6),
    dict(sfx="m64_estrella", en="Número veinte", vol=.32),
    dict(sfx="m64_1up", en="te da una estrella", vol=.5),
    dict(sfx="m64_moneda", en="Número diecinueve", vol=.55),
    dict(sfx="m64_pausa", en="te saluda frente al castillo", vol=.55),
    dict(sfx="m64_moneda", en="Número dieciocho", vol=.55),
    dict(sfx="m64_aparece", en="Brilla en la punta de su cola", vol=.45),
    dict(sfx="m64_moneda", en="Número diecisiete", vol=.55),
    dict(sfx="m64_mammamia", en="la mamá se da cuenta", vol=.6),
    dict(sfx="m64_moneda", en="Número dieciséis", vol=.55),
    dict(sfx="m64_solucion", en="el agua del foso del castillo se vacía", vol=.5),
    dict(sfx="m64_moneda", en="Número quince", vol=.55),
    dict(sfx="m64_moneda", en="Número catorce", vol=.55),
    dict(sfx="m64_bowser_risa", en="se transforma en la de Bowser", vol=.55),
    dict(sfx="m64_moneda", en="Número trece", vol=.55),
    dict(sfx="m64_puerta", en="te deja subir al tejado", vol=.5),
    dict(sfx="m64_1up", en="te regala cien vidas", vol=.55),
    dict(sfx="m64_moneda", en="Número doce", vol=.55),
    dict(sfx="m64_moneda", en="Número once", vol=.55),
    dict(sfx="m64_boo", en="Hasta hay un huevo", vol=.4),
    dict(sfx="m64_moneda", en="Número diez", vol=.55),
    dict(sfx="m64_moneda", en="Número nueve", vol=.55),
    dict(sfx="m64_moneda", en="Número ocho", vol=.55),
    dict(sfx="m64_cuadro", en="De la altura a la que saltas", vol=.5),
    dict(sfx="m64_moneda", en="Número siete", vol=.55),
    dict(sfx="m64_moneda", en="Número seis", vol=.55),
    dict(sfx="m64_moneda", en="Número cinco", vol=.55),
    dict(sfx="m64_moneda", en="Número cuatro", vol=.55),
    dict(sfx="m64_yahoo", en="Y Mario sale disparado", vol=.5),
    dict(sfx="m64_moneda", en="Número tres", vol=.55),
    dict(sfx="m64_moneda", en="Número dos", vol=.55),
    dict(sfx="m64_estrella", en="Y llegamos al número uno", vol=.32),
    dict(sfx="m64_aparece", en="Dice: Eternal Star", vol=.45),
]
