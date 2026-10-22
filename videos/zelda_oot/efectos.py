# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Zelda: Ocarina of Time: su historia y los 12 secretos QUE IGNORASTE» (SECUENCIA YT, Crónicas del
gaming, 22-oct-2026). Fórmula de banjo_tooie (docs/estilo_secuencia_yt.md § PEGATINAS y § MOTION GRAPHICS NUEVOS) con el kit
N64 con PIEL PINTADA EN FLOW (nucleo/mg_zelda.py; marcos en ui/, prompts.json):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de zelda.fandom.com / mariowiki / Wikipedia en
  pegatinas/, fuentes en pegatinas/_fuentes.txt), chicas abajo a la izquierda, en fila cuando la voz enumera, ~1 de cada 5
  GRANDE del lado contrario.
- rótulo `puesto` por secreto (arriba), fichas (cuadro de diálogo) a la derecha SOLO con datos del guion.
- MG NUEVOS de ESTE guion: `ocarina` (5 botones y las canciones nota a nota), `paradoja` (el bucle de la canción de la
  tormenta con el sello «NADIE»), `versiones` (1.0 / 1.1 / 1.2 / GameCube: canto, sangre y símbolo gerudo) y `tres_lineas`
  (la cronología que se parte en tres); además una escalera de recompensas de las Skulltulas con `linea_tiempo`.
  python fab.py zelda_oot fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py zelda_oot fx         audio/fx.wav
"""
import os

import mg_tes as T
import mg_zelda as Z

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
Z.usar(os.path.join(_AQUI, "ui"))     # marcos pintados en Flow (prompts.json; el usuario, 22-oct-2026)
_FX, _FY = .74, .40     # fichas: a la derecha (el rótulo de puesto va arriba)

CAMARA = {}
FUNDIDO = {}


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=Z.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=660):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(en, items, y=.66, tam=330, dur=5.0):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    paso = max(.17, (tam + 90) / 1920)                # cada cinta cabe en su hueco (no se pisan)
    return [peg(a or en, s, t, dur=dur, x=.12 + paso * i, y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, piel="piedra"):
    d = dict(tipo="mg", fn=Z.ficha(titulo, texto, tipo=tipo, piel=piel), en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, dur=3.6):
    return dict(tipo="mg", fn=Z.puesto(num, titulo), en=en, dur=dur, x=.5, y=.19, sale=.45, nombre=f"puesto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


CANCIONES = [("Canción de Saria", "v><v><"), ("Canción de Epona", "^<>^<>"), ("Nana de Zelda", "<^><^>"),
             ("Canción del Sol", ">v^>v^"), ("Canción del Tiempo", ">Av>Av"), ("Canción de la tormenta", "Av^Av^"),
             ("Canción de Saria", "v><v><"), ("Nana de Zelda", "<^><^>")]

FX = [
    # ================================================================ GANCHO
    grande("vuelve a lanzar un juego", "link_epona", "Ocarina of Time (1998)", lado="der", dur=5.0),
    ficha("Rehecho desde cero", "Ocarina of Time", "Rehecho desde cero para *Nintendo Switch 2*. Sale el *5 de noviembre*.",
          tipo="Nintendo / 2026", dur=5.0),
    ficha("la nota más alta de la historia de Metacritic", "Metacritic", "*99*: el único juego con esa nota.",
          tipo="Récord Guinness", dur=4.4),
    *fila("Una vaca que aparece dentro de tu casa", [
        ("vaca", "Una vaca", None),
        ("templo_fuego", "Un canto borrado", "un canto que Nintendo borró"),
        ("ocarina", "Una canción", "una canción que nadie compuso")], dur=6.5),
    ficha("Así que hoy te cuento", "Ocarina of Time", "Su historia, la de Link y *12 secretos* que seguramente ignoraste.",
          tipo="Nintendo / Nintendo 64 / 1998", a=("que seguramente ignoraste|fin", 1.0)),

    # ================================================================ ORIGEN
    peg("Mientras un equipo de Nintendo hacía Super Mario", "mario", "Super Mario 64", tam=380),
    *fila("Al frente estaba Shigeru Miyamoto", [
        ("miyamoto", "Shigeru Miyamoto", None),
        ("kondo", "Koji Kondo", "con Koji Kondo"),
        ("aonuma", "Eiji Aonuma", "un joven Eiji Aonuma")], dur=7.5, tam=300),
    grande("Todo el juego iba a pasar dentro del castillo de Ganon", "ganondorf", "El castillo de Ganon", lado="der", dur=5.4),
    peg("dentro del castillo de Peach", "peach", "El castillo de Peach", tam=360),
    peg("Y pensó en hacerlo en primera persona", "link_concepto", "Boceto de Link", tam=360),
    peg("también habría un Link niño", "link_nino", "Link niño", tam=420, x=.80, y=.60),
    peg("El problema más difícil fue pelear", "link_adulto", "Link", tam=420),
    ficha("En los estudios Toei de Kioto", "Toei Kyoto Studio Park", "Un show de ninjas: rodean al héroe, pero "
          "*atacan de uno en uno*.", tipo="La inspiración del fijado", a=("atacaban de uno en uno|fin", 1.0), piel="pergamino"),
    ficha("Así quedó el fijado con el gatillo Z", "Fijado Z", "Apuntas, la cámara *se centra en el enemigo* y los demás "
          "*esperan su turno*.", tipo="Z-targeting / 1998", a=("lo han copiado|fin", .8)),
    peg("un lector de discos de la consola", "n64dd", "Nintendo 64DD", tam=420),
    ficha("Doscientos cincuenta y seis megabits", "El cartucho", "*256 megabits*: el juego más grande que Nintendo había "
          "hecho.", tipo="Noviembre de 1998", dur=4.6),
    ficha("Y entonces llovieron las notas", "Las notas", "Famitsu: *40/40*, el primero de la historia. Metacritic: *99*, "
          "el único.", tipo="Crítica", a=("único con un noventa y nueve en Metacritic|fin", 1.0)),
    peg("Vendió siete millones", "link_ocarina", "7,6 millones de copias", tam=440, x=.80, y=.58),

    # ================================================================ LORE
    peg("unos niños que nunca crecen", "kokiri", "Los Kokiri", tam=460),
    peg("Todos menos él", "link_nino", "Link, sin hada", tam=380, x=.80, y=.60),
    *fila("el Gran Árbol Deku", [
        ("arbol_deku", "Gran Árbol Deku", None),
        ("navi", "Navi", "Navi, y le pide")], dur=5.5),
    grande("ese hombre es Ganondorf", "ganondorf", "Ganondorf, rey de los Gerudo", lado="der", dur=5.0),
    peg("la princesa Zelda le cuenta su sueño", "zelda_nina", "Princesa Zelda", tam=420),
    *fila("Ganondorf busca la Trifuerza", [
        ("trifuerza", "La Trifuerza", None),
        ("ocarina", "La Ocarina del Tiempo", "y la Ocarina del Tiempo")], dur=5.0),
    peg("y saca la Espada Maestra", "espada_maestra", "Espada Maestra", tam=400, x=.80, y=.58),
    dict(tipo="destello", en="toma la Trifuerza", dur=.5, fuerza=.8),
    grande("Cuando despierta, ya es adulto", "link_adulto", "Link, siete años después", lado="der", dur=5.0),
    grande("Un misterioso guerrero sheikah", "sheik", "Sheik", dur=5.0, tam=600),
    peg("se revela que Sheik era Zelda", "zelda_adulta", "Zelda", tam=440, x=.80, y=.58),
    peg("Zelda devuelve a Link a su infancia", "link_nino", "De vuelta a la infancia", tam=400),

    # ================================================================ 12 / LA VACA
    puesto("Número doce.", 12, "Una vaca en tu casa"),
    peg("Malon te reta", "malon", "Malon", tam=440),
    peg("una carrera de obstáculos a caballo", "epona", "Epona", tam=420, x=.80, y=.60),
    ficha("en menos de cincuenta segundos", "Carrera de obstáculos", "Rancho Lon Lon: batir *50 segundos*.",
          tipo="Link adulto", dur=4.4),
    grande("Te regalan una vaca", "vaca", "Tu premio", lado="der", dur=5.0, tam=560),
    grande("Una vaca, dentro de la casa", "vaca", "Dentro de casa", dur=4.0, tam=520),
    peg("Si le tocas la canción de Epona", "leche", "Leche Lon Lon", tam=360, x=.80, y=.60),

    # ================================================================ 11 / EL PESCADOR
    puesto("En el once, el pescador calvo.", 11, "El pescador calvo"),
    peg("su dueño lleva siempre un sombrero", "pescador", "El dueño del estanque", tam=440),
    peg("lanzas el anzuelo hacia él", "cana", "Caña de pescar", tam=400, x=.80, y=.60),
    ficha("Está completamente calvo", "El estanque de pesca", "Solo *de adulto*: el anzuelo le quita el sombrero.",
          tipo="Lago Hylia", a=("te vuelve a regañar|fin", .8), piel="pergamino"),

    # ================================================================ 10 / LOS CUADROS DE MARIO
    puesto("Número diez.", 10, "Los cuadros de Mario"),
    peg("Cuando encuentras a Zelda de niña", "zelda_nina", "Zelda espiando", tam=400),
    *fila("Son Mario, Luigi", [
        ("mario", "Mario", None),
        ("luigi", "Luigi", "Luigi, la princesa"),
        ("peach", "Peach", "la princesa Peach"),
        ("bowser", "Bowser", "Bowser y Yoshi"),
        ("yoshi", "Yoshi", "y Yoshi")], dur=4.2, tam=290),
    ficha("Si le disparas a esa ventana", "Las ventanas del patio", "Ventana de Mario: *rupia roja*. La otra: un soldado "
          "te lanza *una bomba*.", tipo="Con el tirachinas", a=("y te lanza una bomba|fin", 1.0)),
    dict(tipo="temblor", en="te lanza una bomba", amp=10, dur=.8),
    peg("enseña un nivel de Super Mario Bros.", "mario", "Super Mario Bros.", tam=400, x=.80, y=.60),

    # ================================================================ 9 / PIEDRAS SHEIKAH
    puesto("En el nueve, las piedras chismosas.", 9, "Las piedras chismosas"),
    grande("las piedras Sheikah", "gossip", "Piedra Sheikah", lado="der", dur=5.0, tam=520),
    peg("Si te pones la Máscara de la Verdad", "mascara_verdad", "Máscara de la Verdad", tam=400),
    ficha("Si les pegas con la espada", "Piedra Sheikah", "Espada: te dice *la hora del día*.", tipo="Primer truco",
          dur=4.4),
    dict(tipo="destello", en="despegan", dur=.4, fuerza=.7),
    dict(tipo="temblor", en="despegan", amp=12, dur=1.0),
    ficha("Salen disparadas al cielo", "Piedra Sheikah", "Bomba: *despega como un cohete*.", tipo="Segundo truco", dur=4.0),
    ficha("Si les tocas la canción de la tormenta", "Piedra Sheikah", "Canción de la tormenta: a veces, *un hada*.",
          tipo="Tercer truco", a=("si sabes cómo preguntarle|fin", .8), piel="pergamino"),

    # ================================================================ 8 / LA CASA DE LAS SKULLTULAS
    puesto("Número ocho.", 8, "La casa maldita"),
    grande("convertida en arañas doradas", "rico_maldito", "La familia maldita", lado="der", dur=5.0, tam=560),
    peg("cien Skulltulas doradas", "skulltula", "Skulltula dorada", tam=400),
    mg(Z.linea_tiempo([("10", "Cartera más grande"), ("20", "Piedra de la agonía"), ("30", "Cartera aún mayor"),
                       ("40", "Bombchus"), ("50", "Pieza de corazón"), ("100", "Rupia de 200")],
                      "Las recompensas", w=1720, h=400),
       ("Cada diez te dan un premio", -.3), ("ya no tienes nada que comprar|fin", 1.0),
       ["Cada diez te dan un premio", "Una cartera más grande", "la piedra de la agonía", "otra cartera todavía mayor",
        "bombchus", "una pieza de corazón", "una rupia enorme"], "skulltulas", y=.40),

    # ================================================================ 7 / LA CADENA DE BIGGORON
    puesto("Número siete.", 7, "La cadena de Biggoron"),
    *fila("Empieza con un huevo de bolsillo", [
        ("huevo", "Huevo de bolsillo", None),
        ("cuco", "Pollo", "se convierte en un pollo"),
        ("seta", "Seta", "una seta mágica"),
        ("pocion", "Poción", "una poción")], y=.30, tam=260, dur=7.0),
    *fila("una sierra, una espada rota", [
        ("sierra", "Sierra", None),
        ("espada_rota", "Espada rota", "una espada rota"),
        ("rana", "Rana", "un frasco de colirio"),
        ("resguardo", "Resguardo", "termina con un resguardo")], y=.68, tam=260, dur=5.5),
    ficha("Y algunos tienen el tiempo contado", "Contrarreloj", "La seta y el colirio *se echan a perder* en unos minutos.",
          tipo="Hay que cruzar Hyrule corriendo", a=("hay que cruzar Hyrule corriendo|fin", .8)),
    grande("Al final, Biggoron", "biggoron", "Biggoron", lado="der", dur=5.0, tam=600),
    ficha("Pero tarda tres días", "Biggoron", "Tarda *3 días*. O tocas *6 veces* la canción del Sol.",
          tipo="La forja", a=("para que pasen más rápido|fin", .8), piel="pergamino"),
    grande("El premio es la espada de Biggoron", "espada_biggoron", "Espada de Biggoron", dur=6.0, tam=600),

    # ================================================================ 6 / EL TEMPLO DEL AGUA
    puesto("En el seis, el templo más odiado", 6, "El Templo del Agua"),
    peg("tocando la canción de Zelda", "zelda_nina", "Nana de Zelda", tam=380, x=.80, y=.60),
    peg("lo que de verdad desesperaba eran las botas de hierro", "botas_hierro", "Botas de hierro", tam=420),
    ficha("Ponte las botas, menú", "Templo del Agua", "Botas *puestas*: menú. Botas *fuera*: menú. Y otra vez.",
          tipo="Decenas de veces", a=("en una sola mazmorra|fin", .6)),
    grande("Eiji Aonuma, el que la diseñó", "aonuma", "Eiji Aonuma", dur=5.6, tam=520),
    ficha("pidió perdón en público", "Eiji Aonuma", "Lo que más lamento es lo difícil que era *ponerse y quitarse esas "
          "botas*. Debí hacerlo *mucho más fácil*.", tipo="Disculpa pública / 2009", a=("debió hacerlo mucho más fácil|fin", 1.0), piel="pergamino"),
    peg("las botas de hierro pasaron a un botón", "botas_3ds", "Botas de hierro (3DS)", tam=420, x=.80, y=.60),

    # ================================================================ 5 / EL JUEGO QUE CAMBIÓ EN SILENCIO
    puesto("Número cinco.", 5, "El juego que cambió"),
    grande("la música del Templo del Fuego", "templo_fuego", "Templo del Fuego", lado="der", dur=6.0, tam=560),
    mg(Z.versiones(["1.0", "1.1", "1.2", "GameCube"],
                   [("Canto del Templo del Fuego", [("SÍ", None), ("SÍ", None), ("NO", "rojo"), ("NO", "rojo")]),
                    ("Sangre de Ganondorf", [("ROJA", "rojo"), ("ROJA", "rojo"), ("VERDE", "verde"), ("VERDE", "verde")]),
                    ("Símbolo gerudo", [("ORIGINAL", None), ("ORIGINAL", None), ("ORIGINAL", None), ("CAMBIA", "rojo")])]),
       ("En la versión uno punto dos", -.3), ("y en los bloques del tiempo|fin", 1.0),
       ["En la versión uno punto dos", "el canto desapareció", "la sangre que escupe Ganondorf", "cambió también el símbolo"],
       "versiones", y=.48),
    peg("si tienes un cartucho de los primeros", "sangre_roja", "Versión 1.0: roja", dur=6.0, x=.27, y=.55, tam=520),
    peg("si tienes un cartucho de los primeros", "sangre_verde", "Versión 1.2: verde", dur=6.0, x=.73, y=.55, tam=520),

    # ================================================================ 4 / EL ZELDA EN DISCO
    puesto("En el cuatro, el Zelda", 4, "El Zelda en disco"),
    grande("el sesenta y cuatro de de, una unidad", "n64dd", "Nintendo 64DD", lado="der", dur=6.0, tam=560),
    ficha("Su nombre era Ura Zelda", "Ura Zelda", "Expansión en disco con *las mazmorras rehechas*.", tipo="64DD",
          a=("La expansión se quedó guardada|fin", .6), piel="pergamino"),
    *fila("Miyamoto le dio a Eiji Aonuma a elegir", [
        ("miyamoto", "Shigeru Miyamoto", None),
        ("aonuma", "Eiji Aonuma", "a Eiji Aonuma")], dur=6.0, tam=320),
    grande("así nació Majora's Mask", "majora", "Majora's Mask", lado="der", dur=5.0, tam=560),
    peg("volvió como Master Quest", "mq_logo", "Master Quest (2002)", tam=480),

    # ================================================================ 3 / LA OCARINA DE CINCO NOTAS
    puesto("Número tres.", 3, "Cinco notas"),
    mg(Z.ocarina(CANCIONES, "La ocarina: cinco notas"),
       ("El mando de Nintendo sesenta y cuatro", -.2), ("las bandas sonoras más famosas|fin", 1.0),
       ["solo tenía cinco botones libres", "La de Saria", "la de Epona", "la nana de Zelda", "la del Sol", "la del Tiempo",
        "Y tenían que ser cortas", "Por eso la canción de Saria", "la nana de Zelda#2"], "ocarina", y=.50),

    # ================================================================ 2 / LA CANCIÓN QUE NADIE COMPUSO
    puesto("Número dos.", 2, "La canción que nadie compuso"),
    peg("un niño con una ocarina", "ocarina", "Un niño con una ocarina", tam=380),
    mg(Z.paradoja(["Adulto: el hombre del molino te la enseña", "Viajas al pasado con la Espada Maestra",
                   "De niño, se la tocas", "Él la aprende de ti"]),
       ("Te enseña esa canción", -.3), ("todavía no habías hecho|fin", .8),
       ["Te enseña esa canción", "Entonces vuelves al pasado", "entras al molino de niño",
        "y el hombre aprende la canción de ti", "Él te la enseña porque", "Nadie la compuso"], "paradoja", y=.50),

    # ================================================================ 1 / TRES CAMINOS
    puesto("Y llegamos al número uno.", 1, "Tres caminos"),
    peg("Zelda devuelve a Link a su infancia#2", "zelda_adulta", "Zelda", tam=420),
    peg("Hyrule seguía existiendo en el futuro", "link_adulto", "Hyrule, sin héroe", tam=420, x=.80, y=.60),
    grande("el libro Hyrule Historia", "hyrule_historia", "Hyrule Historia (2011)", lado="der", dur=5.0, tam=520),
    mg(Z.tres_lineas("OCARINA OF TIME", [("Link adulto se va", ["The Wind Waker"], False),
                                         ("Link niño avisa del peligro", ["Majora's Mask", "Twilight Princess"], False),
                                         ("Link pierde contra Ganon", ["A Link to the Past", "The Legend of Zelda"], True)]),
       ("divide la cronología en tres", -.2), ("de este juego|fin", 1.0),
       ["divide la cronología en tres", "En una, Link adulto se va", "En otra, Link niño avisa", "Y hay una tercera"],
       "tres lineas", y=.50),
    ficha("el remake de Nintendo Switch 2 vuelve", "Ocarina of Time", "Remake para *Nintendo Switch 2*: "
          "*5 de noviembre de 2026*.", tipo="El punto de partida", a=("todo lo demás|fin", 1.0)),

    # ================================================================ CIERRE
    *fila("Una vaca en casa", [
        ("vaca", "La vaca", None),
        ("pescador", "El pescador", "un pescador calvo"),
        ("templo_fuego", "El canto borrado", "un canto borrado"),
        ("ocarina", "La canción", "una canción que nadie compuso#2")], dur=5.0, tam=300),
    grande("y que todavía hoy marca", "link_adulto", "Ocarina of Time (1998)", lado="der", dur=5.0, tam=600),
    peg("con Majora's Mask", "majora", "Majora's Mask", tam=400),
]
ROTULOS = []
SFX = {   # uno distinto por momento (regla: nada de SFX repetidos)
    "vaca": ("A single friendly cartoon cow moo inside a small wooden house, light and comedic", 3),
    "bomba": ("Small cartoon bomb fuse hiss then a pop explosion, retro adventure game", 3),
    "cohete": ("Stone launching into the sky like a firework rocket, whoosh rising then a distant sparkle pop", 3),
    "botas": ("Heavy iron boots clanking down onto a stone floor underwater, muffled metallic thud", 3),
    "sello": ("Rubber stamp slammed hard on paper, a single loud dramatic thump", 2),
    "puerta": ("Huge ancient stone temple door grinding open with a deep rumble and a holy shimmer", 4),
}
PISTAS = [
    dict(sfx="vaca", en="Una vaca, dentro de la casa", vol=.45),
    dict(sfx="bomba", en="te lanza una bomba", vol=.45),
    dict(sfx="cohete", en="despegan", vol=.45),
    dict(sfx="botas", en="Para hundirte, te las ponías", vol=.4),
    dict(sfx="sello", en="Nadie la compuso", vol=.5),
    dict(sfx="puerta", en="abre la puerta del Templo del Tiempo", vol=.4),
]
