# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Ranni QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 21-oct-2026).
Fórmula de docs/estilo_secuencia_yt.md (§ PEGATINAS, § MOTION GRAPHICS NUEVOS) con el kit de Elden Ring (nucleo/mg_er.py):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de eldenring.fandom.com en pegatinas/), chicas abajo a la
  izquierda, en fila cuando la voz enumera, y ~1 de cada 5 GRANDE (media pantalla) del lado contrario a las fichas.
- PANTALLAS a cuadro entero (pantallas/) donde el clip no enseña lo que hace falta ver (≤ ~10 s cada una).
- fichas de descripción SOLO con citas verificadas (guion.py: fuentes), arriba a la derecha; rótulo de puesto por atrocidad.
- MG NUEVOS de este guion: `marionetas` (Seluvis → el titiritero acaba colgando de los hilos de Ranni), `sombra` (los Dos
  Dedos, Ranni y Blaidd: ella corta su hilo y la sombra enloquece), `domino` (de la Runa robada a la Fragmentación) y
  `constelacion` (los que la quisieron se apagan; quedan la Luna y tú).
  python fab.py er_ranni_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_ranni_atrocidades fx         audio/fx.wav
"""
import os

import mg_er as E
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_FX, _FY = .74, .30     # fichas: arriba a la derecha

CAMARA = {}
FUNDIDO = {}


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=680):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.50, tam=tam)


def fila(en, items, y=.64, tam=340, dur=4.6):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [peg(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=os.path.join(_PEG, icono + ".png") if icono else None),
             en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


def mensaje(lineas, de, a, marcas, y=.78):
    return dict(tipo="mg", fn=E.mensaje(lineas), de=de, a=a, marcas=marcas, y=y, sale=.5, nombre="MG mensaje " + lineas[0], ver=3.0)


_DOMINO = ["Roba la Runa de la Muerte", "Godwyn muere solo en alma", "Brota la raíz de la muerte", "Márika rompe el Anillo",
           "La Fragmentación"]

FX = [
    # ================================================================ GANCHO
    grande("es la bruja Ranni", "ranni_npc", "Ranni la Bruja", lado="izq", dur=5.4, tam=700),
    peg("un sombrero puntiagudo", "sombrero", "Sombrero de bruja", x=.83, y=.64, tam=340),
    peg("para casarse con ella", "anillo_luna", "Anillo de la Luna Oscura", x=.83, y=.62, tam=340),
    pant("torre_ranni", "Ella misma lo confiesa", ("los cuchillos negros que matan dioses|fin", .3), zoom=(1.0, 1.12)),
    ficha("robé un fragmento de la Runa de la Muerte", "Ranni la Bruja",
          "Robé un fragmento de la *Runa de la Muerte*, y con un ritual terrible forjé *los cuchillos negros que matan dioses*.",
          tipo="Lo que confiesa", a=("los cuchillos negros que matan dioses|fin", 1.0)),
    peg("forjé los cuchillos negros", "cuchillo_negro", "Cuchillo negro", tam=400),
    mensaje(["Todo lo hice yo."], ("con tres palabras", -.1), ("todo lo hice yo|fin", 1.6), ["todo lo hice yo"]),
    puesto("las cinco peores atrocidades de Ranni", "Las 5 peores atrocidades de", "Ranni", dur=4.2),
    peg("un rastro de cadáveres", "runa_muerte", "Runa de la Muerte", tam=380),
    peg("Te pasó a ti", "frasco", "Tú, el Sinluz", x=.80, y=.60, tam=340),

    # ================================================================ 5 · EL PRECEPTOR DE LAS MARIONETAS
    puesto("Número cinco. El preceptor", "Atrocidad número 5", "El preceptor de las marionetas"),
    pant("torre_seluvis", "Cuando entras al servicio de la bruja", ("preceptor en las artes de la hechicería|fin", .2),
         zoom=(1.0, 1.10), pan=(0, 0, .08, 0)),
    *fila("allí encontrarás a Iji", [
        ("iji", "Iji, consejero de guerra", None),
        ("seluvis", "Seluvis, preceptor", "y a Seluvis, preceptor")], dur=4.6),
    grande("Seluvis es ese mago", "seluvis", "Preceptor Seluvis", lado="izq", dur=5.0, tam=600),
    ficha("no sé qué es lo que la señora ve", "Preceptor Seluvis",
          "No sé qué es lo que la señora ve en *un Sinluz de provincias* como tú.", tipo="Lo que te dice",
          a=("de provincias como tú|fin", .8)),
    peg("una guerrera llamada Nepheli", "nepheli", "Nepheli Loux", tam=400),
    peg("le des a beber una poción", "pocion_seluvis", "Poción de Seluvis", x=.83, y=.62, tam=340),
    dict(tipo="mg", fn=E.marionetas(munecos=("Nepheli",)), de=("Esa poción convierte", -.2), a=("como un hijo para él|fin", .6),
         marcas=["Esa poción convierte", "Y Seluvis las colecciona"], y=.50, sale=.4, nombre="MG marionetas 1", ver=5.0),
    *fila("Debajo de un suelo falso", [
        ("marioneta_dolores", "Marioneta de Dolores", None),
        ("marioneta_jarwight", "Marioneta de Jarwight", "tiene un cuarto secreto")], y=.34, dur=6.0),
    mensaje(["Marioneta de Seluvis.", "No tocar."], ("te espera un mensaje", -.1), ("No tocar|fin", 1.4),
            ["marioneta de Seluvis", "No tocar"], y=.80),
    grande("El hombre que convierte personas en muñecos", "seluvis", "Su profesor de magia", lado="der", dur=4.4, tam=560),
    peg("Te da un brebaje ámbar", "brebaje", "Brebaje ámbar", tam=420),
    ficha("dáselo a la señora y asegúrate", "Preceptor Seluvis",
          "Dáselo a la señora y asegúrate de que se lo beba. *Cuando lo haga, mi plan dará fruto*.", tipo="Lo que te dice",
          icono="brebaje", a=("mi plan dará fruto|fin", .8)),
    dict(tipo="mg", fn=E.marionetas(munecos=("Nepheli", "Ranni")), de=("Quería convertir a su propia señora", -.2),
         a=("una marioneta más de su colección|fin", .9),
         marcas=["Quería convertir", "Quería convertir", "a su propia señora"], y=.50, sale=.4, nombre="MG marionetas 2", ver=5.0),
    grande("ella se da cuenta enseguida", "ranni_retrato", "Ranni la Bruja", lado="izq", dur=5.0, tam=600),
    peg("le entregas la Hoja matadedos", "matadedos", "Hoja matadedos", x=.84, y=.68, tam=360),
    ficha("le entregas la Hoja matadedos", "Hoja matadedos",
          "Prueba de *la alta traición* de la Ciudad Eterna. Se dice que puede *herir a la Voluntad Mayor* y a sus vasallos.",
          tipo="Objeto clave", icono="matadedos", dur=6.4),
    *fila("Seluvis aparece muerto en su torre", [
        ("seluvis", "Seluvis, muerto", None),
        ("pidia", "Pidia, su ayudante", "muere también Pidia")], dur=5.0),
    peg("todavía te vende marionetas", "marioneta_jarwight", "Marioneta en venta", x=.83, y=.62, tam=340),
    dict(tipo="mg", fn=E.marionetas(munecos=("Nepheli", "Ranni")), de=("Él quería una muñeca obediente", -.2),
         a=("quién mueve los hilos de verdad|fin", 1.4),
         marcas=["Él quería una muñeca", "Él quería una muñeca", "Él quería una muñeca", "le enseñó quién mueve"],
         y=.50, sale=.4, nombre="MG marionetas vuelta", ver=5.0),
    peg("le pasó a los que le fueron leales", "blaidd", "Blaidd", x=.80, y=.60, tam=360),

    # ================================================================ 4 · LA SOMBRA
    puesto("Número cuatro. Blaidd", "Atrocidad número 4", "Blaidd, el medio lobo"),
    grande("Blaidd fue tu mejor amigo", "blaidd_npc", "Blaidd, el medio lobo", lado="der", dur=5.0, tam=720),
    *fila("te ayuda contra Darriwil", [
        ("darriwil", "Darriwil, caballero sabueso", None),
        ("radahn_estelar", "Radahn", "en el festival de Radahn")], dur=4.6),
    ficha("su único propósito es luchar", "Blaidd",
          "Mi único propósito es luchar por el destino de Ranni, *con espada y colmillo*.", tipo="Lo que te dice",
          icono="espadon_real", a=("con espada y colmillo|fin", 1.0)),
    dict(tipo="mg", fn=E.sombra(), de=("El consejero Iji te lo cuenta", -.2), a=("no se saliera del camino|fin", .6),
         marcas=["los Dos Dedos le dieron", "Su propia sombra"], y=.50, sale=.4, nombre="MG sombra 1", ver=5.0),
    grande("Y el viejo Iji sigue", "iji", "Iji, consejero de guerra", lado="izq", dur=6.0, tam=600),
    ficha("pero si la señora, como Empírea", "Iji, consejero de guerra",
          "Si la señora se resiste a ser un instrumento de los Dos Dedos, *la sombra enloquecerá* y pasará a ser *una horrible "
          "maldición*.", tipo="Lo que te cuenta", a=("una horrible maldición|fin", .8)),
    dict(tipo="mg", fn=E.sombra(), de=("Se rebeló contra los Dos Dedos", -.4), a=("no me dejaría controlar por esa cosa|fin", 1.4),
         marcas=["Se rebeló contra", "Se rebeló contra", "Y lo dice sin pestañear", "no me dejaría controlar"],
         y=.50, sale=.4, nombre="MG sombra 2", ver=5.0),
    peg("la bruja que planeó la noche más famosa", "cuchillo_negro", "Cuchillo negro", tam=380),
    grande("Lo encuentras encerrado en una celda", "blaidd", "Blaidd, encerrado", lado="izq", dur=5.0, tam=620),
    ficha("el viejo Iji me encerró aquí", "Blaidd", "El viejo Iji me encerró aquí. *Soy parte de su ser. Su propia sombra*.",
          tipo="Lo que te dice", dur=7.0),
    pant("torre_ranni2", "Y al final, Blaidd se escapa", ("pase lo que pase|fin", .3), zoom=(1.0, 1.12)),
    ficha("hablando solo", "Blaidd, enloquecido", "No, soy parte de su ser. *Nunca podría traicionarla*, pase lo que pase.",
          tipo="Lo que murmura", a=("pase lo que pase|fin", .8)),
    peg("Y tienes que matarlo tú", "espadon_real", "Espadón real", tam=420),
    peg("Su guantelete lo describe", "guantelete_blaidd", "Guanteletes de Blaidd", x=.17, tam=380),
    ficha("Su guantelete lo describe", "Guanteletes de Blaidd",
          "Blaidd, que servía como sombra de Ranni, fue un aliado leal que *desafiaría al destino mismo* si este le ordenaba "
          "volverse contra su señora.", tipo="Armadura de manos", icono="guantelete_blaidd",
          a=("volverse contra su señora|fin", .8)),
    pant("blaidd_dunas", "Y lo desafió", ("Se volvió loco antes que traicionarla|fin", .4), zoom=(1.0, 1.08)),
    ficha("Iji lo resume con una frase", "Iji, consejero de guerra",
          "Blaidd se convirtió en una maldición que atormentaba a la señora, pero *en su locura, se entregó a ella*.",
          tipo="Lo que dice", a=("se entregó a ella|fin", 1.0)),
    *fila("La libertad se la quedó la bruja", [
        ("ranni_retrato", "Ranni, libre", None),
        ("blaidd", "Blaidd, la factura", "La factura la pagó el lobo")], dur=4.4),

    # ================================================================ 3 · LAS QUE PUSIERON LAS MANOS
    puesto("Número tres. Las que pusieron", "Atrocidad número 3", "Las que pusieron las manos"),
    pant("asesinato_godwyn", "La bruja no mató a Godwyn", ("asesinas de los Cuchillos Negros|fin", .5), zoom=(1.0, 1.12)),
    peg("Su armadura cuenta", "armadura_cuchillo", "Armadura de cuchillo negro", tam=420),
    ficha("Su armadura cuenta", "Armadura de cuchillo negro",
          "Todas eran mujeres, y se rumoreaba que eran *numen con lazos muy estrechos con la mismísima Márika*.",
          tipo="Armadura de torso", icono="armadura_cuchillo", a=("con la mismísima Márika|fin", 1.2)),
    grande("Sí, con Márika", "marika", "Márika la Eterna", lado="izq", dur=4.4, tam=620),
    peg("Una de ellas se llamaba Tiche", "tiche", "Cenizas de Tiche", tam=400),
    ficha("Sus cenizas cuentan", "Cenizas de Tiche",
          "En la noche de la conspiración, impregnó su cuchillo con la Runa de la Muerte y *mató a Godwyn el Dorado*.",
          tipo="Cenizas espirituales", icono="tiche", a=("y mató a Godwyn el Dorado|fin", .8)),
    grande("Tiche era hija de la cabecilla", "alecto", "Alecto, cabecilla de los Cuchillos Negros", lado="izq", dur=5.4, tam=620),
    pant("prision_alecto", "La madre sobrevivió", ("en la misión de la bruja|fin", .3), zoom=(1.0, 1.12)),
    peg("Tu recompensa son las cenizas de su hija", "tiche", "Cenizas de Tiche", x=.83, y=.62, tam=360),
    grande("Y luego está Iji", "iji", "Iji, el herrero", lado="izq", dur=4.4, tam=600),
    ficha("Iji se despide de ti", "Iji, consejero de guerra",
          "Mi propósito está llegando a su fin. Te alcanzaré pronto, Blaidd. *Solo espero que aceptes mis disculpas*.",
          tipo="Su despedida", a=("que aceptes mis disculpas|fin", .8)),
    peg("cubierto de llamas negras", "yelmo_iji", "Yelmo espejo de Iji", tam=380),
    peg("tres asesinas de los Cuchillos Negros", "asesina", "Asesina de los Cuchillos Negros", x=.83, y=.60, tam=400),
    grande("en una conversación escondida", "muneca", "Ranni en miniatura", lado="izq", dur=5.6, tam=560),
    ficha("deja escapar: Blaidd e Iji", "Ranni la Bruja",
          "Blaidd e Iji, los dos, *están dispuestos a darme demasiado*. Diles que los quiero.", tipo="Lo que deja escapar",
          a=("Diles que los quiero|fin", 1.0)),
    *fila("no queda ninguno en pie", [
        ("blaidd", "Blaidd", None),
        ("iji", "Iji", None),
        ("seluvis", "Seluvis", None)], dur=3.6),

    # ================================================================ 2 · LA NOCHE DE LOS CUCHILLOS NEGROS
    puesto("Ya en el podio, el número dos", "Atrocidad número 2", "La noche de los Cuchillos Negros"),
    grande("Godwyn el Dorado era el primogénito", "godwyn_icono", "Godwyn el Dorado", lado="der", dur=5.0, tam=640),
    peg("del dragón contra el que peleó", "fortissax", "Fortissax", tam=420),
    pant("godwyn_ojo", "Y en la Noche de los Cuchillos Negros", ("Pero no murió del todo|fin", .3), zoom=(1.0, 1.15)),
    peg("Ella misma lo cuenta así", "runa_muerte", "Runa de la Muerte", tam=400),
    ficha("Ella misma lo cuenta así", "Ranni la Bruja",
          "Robé la Runa de la Muerte, *maté mi propia carne de Empírea*, y la deseché.", tipo="Lo que confiesa",
          a=("y la deseché|fin", .8)),
    dict(tipo="mg", fn=E.domino(_DOMINO), de=("Esa misma noche, ella sacrificó", -.2), a=("los que viven en la muerte|fin", .8),
         marcas=["Esa misma noche", "A Godwyn le arrancaron", "De ahí brota la raíz"], y=.50, sale=.4, nombre="MG domino 1",
         ver=5.0),
    pant("raices_profundas", "Los no muertos de las catacumbas", ("todo eso sale de ese cuerpo|fin", .4), zoom=(1.0, 1.10),
         pan=(0, 0, .15, 0)),
    *fila("Los no muertos de las catacumbas", [
        ("raiz", "Raíz de la muerte", None),
        ("revenant", "Los que viven en la muerte", "los que adoran a Godwyn")], dur=5.0),
    grande("Maliketh, la Espada Negra", "maliketh", "Maliketh, la Espada Negra", lado="izq", dur=4.6, tam=620),
    ficha("Su espada lo cuenta", "Espada negra de Maliketh",
          "Después de que robaran un fragmento de la Muerte aquella noche fatídica, Maliketh *selló la hoja dentro de su propia "
          "carne*, para que nadie volviera a robar la Muerte.", tipo="Arma", icono="espada_maliketh",
          a=("robar la Muerte nunca más|fin", .8)),
    peg("el pobre terminó como Gurranq", "gurranq", "Gurranq, clérigo bestia", tam=420),
    peg("raíces de la muerte para devorarlas", "raiz", "Raíz de la muerte", x=.83, y=.62, tam=320),
    dict(tipo="mg", fn=E.domino(_DOMINO), de=("Y después vino lo peor", -.2), a=("y empezó la Fragmentación|fin", 2.6),
         marcas=["Y después vino lo peor", "Y después vino lo peor", "Y después vino lo peor", "Márika hizo pedazos",
                 "y empezó la Fragmentación"], y=.50, sale=.4, nombre="MG domino 2", ver=5.0),

    # ================================================================ 1 · LA ERA DE LAS ESTRELLAS
    puesto("Y llegamos al número uno", "Atrocidad número 1", "La era de las estrellas"),
    grande("la bruja te pregunta", "ranni_retrato", "Ranni la Bruja", lado="izq", dur=5.6, tam=640),
    ficha("vendrías a mí, incluso ahora", "Ranni la Bruja", "¿Vendrías a mí, incluso ahora, *mi único señor*?",
          tipo="Lo que te pregunta", a=("mi único señor|fin", 1.0)),
    peg("le pones el anillo de la Luna Oscura", "anillo_luna", "Anillo de la Luna Oscura", tam=420),
    peg("lo que promete el día de la boda", "mandoble_luna", "Mandoble de la Luna Oscura", x=.83, y=.62, tam=360),
    peg("Delante de los restos de Márika", "marika", "Márika", tam=380),
    mensaje(["Ahora llega la era de las estrellas.", "Un viaje de mil años bajo la Luna."], ("Y anuncia", -.1),
            ("bajo la sabiduría de la Luna|fin", .8), ["ahora llega la era", "Un viaje de mil años"], y=.80),
    ficha("Aquí comienza la noche helada", "Ranni, la diosa", "Aquí comienza *la noche helada que lo abarca todo*.",
          tipo="Lo que anuncia", a=("el miedo, la duda y la soledad|fin", .8)),
    grande("Con su orden nuevo, y contigo de consorte", "ranni_npc", "Ranni y su consorte", lado="izq", dur=5.0, tam=640),
    dict(tipo="mg", fn=E.constelacion(["Blaidd", "Iji", "Seluvis", "Tiche", "Alecto", "Godwyn"], remate="Consorte eterno"),
         de=("Todos los que la quisieron", -.2), a=("no hay final de divorcio|fin", .8),
         marcas=["la quisieron, Blaidd", "Iji, y hasta Seluvis", "y hasta Seluvis", "acabaron muertos por el camino",
                 "acabaron muertos por el camino", "acabaron muertos por el camino", "Y el último que queda", "Mi bello consorte"],
         y=.50, sale=.4, nombre="MG constelacion", ver=5.0),
    peg("las conversaciones escondidas de su muñequita", "muneca", "Ranni en miniatura", tam=400),
    mensaje(["Vayamos juntos."], ("Vayamos juntos. A la oscuridad", -.2), ("Vayamos juntos. A la oscuridad|fin", 2.4),
            ["Vayamos juntos. A la oscuridad"], y=.80),
    grande("mucha gente, sabiendo todo esto", "ranni_npc", "Ranni la Bruja", lado="der", dur=5.6, tam=680),

    # ================================================================ CIERRE
    *fila("dejó un preceptor muerto", [
        ("seluvis", "Seluvis", None),
        ("blaidd", "Blaidd", "un lobo loco"),
        ("iji", "Iji", "un herrero en llamas"),
        ("alecto", "Alecto", "una madre sin hija"),
        ("godwyn_icono", "Godwyn", "un dios sin alma")], tam=300, dur=7.5),
    grande("te volverías a casar con Ranni", "ranni_retrato", "¿Te volverías a casar?", lado="der", dur=4.6, tam=620),
    puesto("en el canal tienes las atrocidades de Márika", "Ya en el canal · Las 5 peores", "Márika · Radagon · Miquella",
           dur=6.0),
    peg("una muñeca con sombrero", "muneca", "Ranni en miniatura", x=.80, y=.60, tam=420),
]
ROTULOS = []
SFX = {   # uno distinto por momento (regla: nada de SFX repetidos)
    "cuchillo": ("A cursed dagger slowly drawn from a sheath, with a dark magical hiss and a faint ghostly whisper, dark fantasy", 3),
    "hilos": ("Wooden marionette joints clattering and taut strings creaking in an empty stone tower, eerie, dark fantasy", 3),
    "aullido": ("A single distant lonely wolf howl under a cold night sky, long reverb, dark fantasy", 4),
    "llamas": ("Low crackling black flames with a hollow magical rumble, ominous, dark fantasy", 3),
    "viento": ("Freezing night wind rising over an empty land with a faint high celestial shimmer, dark fantasy", 4),
}
PISTAS = [
    dict(sfx="cuchillo", en="forjé los cuchillos negros", vol=.45),
    dict(sfx="hilos", en="Esa poción convierte", vol=.4),
    dict(sfx="aullido", en="Y al final, Blaidd se escapa", vol=.45),
    dict(sfx="llamas", en="cubierto de llamas negras", vol=.4),
    dict(sfx="viento", en="Aquí comienza la noche helada", vol=.45),
]
