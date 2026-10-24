# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 10 Jiggies más CRUELES de Banjo-Tooie» (SECUENCIA YT, Crónicas del gaming, 23-oct-2026).
Kit TRANSLÚCIDO nuevo nucleo/mg_banjo.py (regla del usuario 22-oct: nada de carteles opacos que tapen el video; humo chocolate
difuminado, filetes miel con panal, Cooper Black + Arial Rounded):
- `puesto` con el Jiggy REAL que gira y, al irse, el medidor de CRUELDAD en panales (arriba a la derecha).
- PEGATINAS de cada personaje/objeto que nombra la voz (banjokazooie.fandom.com, pegatinas/_fuentes.txt).
- Fichas translúcidas a la derecha solo con datos del guion.
- MG nuevos de ESTE guion: marcador de puntos con metas (Zubbas 40/50 en 60 s; olla de oro 75/90 de 100 en 45 s), contrarreloj
  (15 dinamitas en 200 s con «UN HUEVO = BOOM»; 20 Clinkers en 200 s con gas tóxico), recados de la familia de Scrotty, cadena
  hasta Weldar y la carrera contra Canary Mary (acelera si te pegas, acelerón final y el truco).
- Sin mapa: el único mapa real de la isla es el pergamino del manual, sin nombres, y no se pueden ubicar los sitios con certeza.
  python fab.py bt_jiggies_crueles fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py bt_jiggies_crueles fx         audio/fx.wav
"""
import os

import mg_banjo as B
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_FX, _FY = .74, .42     # fichas: a la derecha (el rótulo de puesto va arriba)
JIGGY = os.path.join(_PEG, "jiggy.png")

CAMARA = {}
FUNDIDO = {}


def _p(slug):
    return os.path.join(_PEG, slug + ".png")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=T.pegatina(_p(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=660):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(items, y=.66, tam=290, dur=5.0):
    """Pegatinas en fila; items = [(ancla, slug, titulo)], cada una entra con su palabra."""
    xs = (.11, .29, .47, .65, .83)
    return [peg(a, s, t, dur=dur - .9 * i, x=xs[i], y=y, tam=tam) for i, (a, s, t) in enumerate(items)]


def ficha(en, titulo, texto, sub=None, dur=6.0, a=None):
    d = dict(tipo="mg", fn=B.ficha(titulo, texto, sub), en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, cruel, dur=3.8):
    return [dict(tipo="mg", fn=B.puesto(num, titulo, JIGGY), en=en, dur=dur, x=.5, y=.17, sale=.45, nombre=f"puesto {num}",
                 ver=1.4),
            dict(tipo="mg", fn=B.crueldad(cruel), en=(en, dur - .2), dur=4.2, x=.84, y=.13, sale=.35,
                 nombre=f"crueldad {num}", ver=1.3)]


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


FX = [
    # ================================================================ GANCHO
    grande("hay noventa Jiggies", "jiggy", "90 Jiggies", lado="der", dur=4.2, tam=420),
    peg("ir a pelear contra la bruja", "grunty", "Gruntilda", tam=360),
    *fila([("Una carrera que", "canary_mary", "Canary Mary"),
           ("Una cueva llena de basura", "clinker", "Clinker"),
           ("un cerdo de vacaciones", "chris_bacon", "Chris P. Bacon")], dur=8.0),
    grande("un jefe que es un soplete", "weldar", "Weldar", lado="der", dur=5.0, tam=560),
    ficha("Así que hoy te traigo", "Los 10 Jiggies más crueles", "Del *menos malo* al *peor*, y cómo sacarlos.",
          sub="Banjo-Tooie / Rare / 2000", a=("contra la tele|fin", .8)),

    # ================================================================ CONTEXTO
    peg("En Banjo-Kazooie, cada mundo", "bk_1998", "Banjo-Kazooie (1998)", tam=380),
    grande("los de Rare conectaron la isla", "caja_bt", "Banjo-Tooie (2000)", lado="der", dur=4.4, tam=520),
    peg("un tren que viaja", "chuffy", "Chuffy", tam=380),
    *fila([("que Mumbo", "mumbo", "Mumbo Jumbo"), ("y Humba Wumba", "humba", "Humba Wumba")], dur=4.6, tam=320),
    ficha("y un cien por ciento", "90 Jiggies", "Con *70* llegas a la bruja. El *100 %* pide los 90.", sub="el cien por ciento",
          dur=6.5),

    # ================================================================ 10 · ZUBBAS
    *puesto("Número diez", 10, "El nido de los Zubbas", 1),
    grande("Humba Wumba convierte a Banjo", "bee_banjo", "Banjo abeja", lado="der", dur=4.4, tam=520),
    ficha("En la puerta, un Zubba", "La entrada", "*20* aguijonazos en *10* segundos, solo para pasar.", sub="los Zubbas",
          dur=6.0),
    mg(B.marcador("El nido de los Zubbas", [(40, "Página de Cheato", _p("cheato_page")), (50, "Jiggy", JIGGY)], 60, 60,
                  iconos=[((214, 52, 40), "1"), ((72, 200, 90), "2"), ((52, 104, 214), "3")],
                  pasos=[(1, 40), (2, 50)]),
       "Dentro empieza lo bueno", ("a que les apuntes|fin", .4),
       ["Sesenta segundos", "Con cuarenta puntos", "Para el Jiggy necesitas cincuenta"], "zubbas"),
    ficha("El truco: olvídate de los rojos", "El truco", "Persigue a los *azules*: valen el *triple*.", dur=5.5),

    # ================================================================ 9 · OLLA DE ORO
    *puesto("Número nueve", 9, "La olla de oro de Gruntilda", 2),
    peg("Mumbo tiene que hacer su danza", "mumbo", "Mumbo", tam=380),
    peg("Banjo le dispara los cuatro tipos de huevo", "granada", "Huevos", tam=340),
    mg(B.marcador("La olla de oro", [(75, "Página de Cheato", _p("cheato_page")), (90, "Jiggy", JIGGY)], 100, 45,
                  pasos=[(1, 75), (2, 90)]),
       "Una sala con las paredes", ("En cuarenta y cinco segundos|fin", .6),
       ["Tienes cuarenta y cinco segundos", "Con setenta y cinco aciertos", "Para el Jiggy, noventa"], "olla"),
    ficha("El truco es no apuntar", "El truco", "Barre la pared *fila por fila*, sin volver atrás.", dur=5.5),

    # ================================================================ 8 · CHRIS P. BACON
    *puesto("En el ocho", 8, "Un cerdo de vacaciones", 2),
    grande("Dentro está Chris P. Bacon", "chris_bacon", "Chris P. Bacon", lado="der", dur=5.0, tam=560),
    ficha("Basta una sola mordida", "Una regla", "*Una* mordida de piraña y vuelves a *empezar*.", sub="Chris P. Bacon", dur=6.0),
    ficha("su nombre salió de un concurso", "Chris P. Bacon", "Suena a *crispy bacon*: tocino crujiente.",
          sub="Nintendo Official Magazine UK", dur=7.5),

    # ================================================================ 7 · SCROTTY
    *puesto("Número siete", 7, "El Jiggy de los recados", 2),
    mg(B.recados("La familia de Scrotty", _p("scrotty"),
                 [(_p("scrat"), "Scrat", "Enfermo", "Al chamán del acantilado"),
                  (_p("scrit"), "Scrit", "Se encogió", "Devolverle su tamaño"),
                  (_p("scrut"), "Scrut", "Se escapó de casa", "Rescatarla en Witchyworld")], JIGGY),
       "Scrotty es una dinosaurio enorme", ("la respuesta es no|fin", 1.2),
       ["Scrat está enfermo", "Scrit se encogió", "Y Scrut se escapó", "Tres tareas", "varios viajes en tren",
        "medio mapa recorrido", "Que Scrotty se encontró", "la respuesta es no"], "recados"),

    # ================================================================ 6 · MR. PATCH
    *puesto("Número seis", 6, "Mr. Patch", 3),
    grande("Es un dinosaurio inflable", "mr_patch", "Mr. Patch", lado="izq", dur=4.4, tam=560),
    ficha("Doce, con huevos granada", "Mr. Patch", "*12* parches, solo con *huevos granada*.", sub="Witchyworld", dur=6.0),
    peg("Al primer golpe sale", "granada", "Huevo granada", tam=320),
    ficha("ten los huevos granada listos", "El truco", "Granadas listas, y apunta *volando en círculo*.", dur=6.0),

    # ================================================================ 5 · LORD WOO FAK FAK
    *puesto("Número cinco", 5, "Lord Woo Fak Fak", 3),
    grande("Es un pez enorme", "woo_fak_fak", "Lord Woo Fak Fak", lado="der", dur=4.6, tam=600),
    ficha("Hay seis, y solo", "Forúnculos", "*6*, y solo sirve el que *parpadea*. Luego, los ojos.", sub="Jolly Roger's Lagoon",
          dur=7.5),
    grande("convertir a Banjo en un submarino", "submarino", "Submarino", lado="izq", dur=5.0, tam=460),

    # ================================================================ 4 · WELDAR
    *puesto("En el cuatro", 4, "Weldar", 4),
    mg(B.cadena("Para llegar a Weldar", [(_p("mumbo"), "Hechizos de Mumbo"), (_p("washer"), "Transformaciones"),
                                         (None, "Tareas en la fábrica")], (_p("weldar"), "WELDAR")),
       "Llegar a su sótano exige", ("que casi no ve|fin", .5),
       ["una cadena de tareas", "hechizos de Mumbo", "y transformaciones", "Weldar es un soplete"], "cadena weldar", y=.48),
    ficha("Tiene seis placas", "Weldar", "*6* placas. Tras el *tercer* golpe, suelo *electrificado*.", sub="Grunty Industries",
          dur=8.0),

    # ================================================================ 3 · ORDNANCE STORAGE
    *puesto("Número tres", 3, "Ordnance Storage", 4),
    grande("Banjo agarra a Kazooie", "blaster", "Breegull Blaster", lado="der", dur=4.6, tam=520),
    mg(B.contrarreloj("Ordnance Storage", 15, 200, remate="UN HUEVO = BOOM"),
       "Hay quince cartuchos", ("vuela el almacén entero|fin", 1.0),
       ["Desde el primero", "Y la regla de oro", "vuela el almacén entero"], "dinamita"),
    ficha("date una vuelta antes", "El truco", "Una vuelta *sin prisa* y luego, el *oído*.", dur=6.0),

    # ================================================================ 2 · CLINKER'S CAVERN
    *puesto("Número dos", 2, "La cueva de Clinker", 4),
    peg("las botas para trepar", "botas", "Botas para trepar", tam=330),
    mg(B.contrarreloj("La cueva de Clinker", 20, 200, icono=_p("clinker"), remate="GAS TÓXICO", gas=True, hasta=.75),
       "Tienes que eliminar a veinte", ("y el reloj no se detiene|fin", .4),
       ["en doscientos segundos", "Y si el tiempo se acaba", "se llena de gas tóxico"], "clinkers"),
    ficha("Escucha a los Clinkers", "El truco", "*Escúchalos* antes de verlos.", dur=5.0),

    # ================================================================ 1 · CANARY MARY
    *puesto("Y llegamos al número uno", 1, "Canary Mary", 5, dur=4.2),
    grande("Canary Mary, en Cloud Cuckooland", "canary_mary", "Canary Mary", lado="der", dur=5.0, tam=600),
    ficha("Para ganártelos, dos carreras", "Canary Mary", "Carrera 1: el *Jiggy*. Carrera 2: la *página de Cheato*.",
          sub="Cloud Cuckooland", dur=6.0),
    mg(B.carrera(_p("banjo"), _p("canary_mary")), "La mecánica es simple", ("pase lo que pase|fin", .8),
       ["machacar el botón A", "Si te le pegas", "Y al final da un acelerón"], "carrera"),
    mg(B.carrera(_p("banjo"), _p("canary_mary")), "El truco que más funciona", ("como si no hubiera mañana|fin", 1.0),
       ["El truco que más funciona"] * 4, "carrera truco"),

    # ================================================================ CIERRE
    *fila([("Una abeja contrarreloj", "bee_banjo", "Zubbas"), ("un cerdo con una Game Boy", "chris_bacon", "Chris P. Bacon"),
           ("dos cuevas en primera persona", "clinker", "Clinkers"), ("y una canaria tramposa", "canary_mary", "Canary Mary")],
          dur=7.0, tam=280),
    grande("nuestro video de los diez secretos", "devil_bottles", "Bottles' Revenge", lado="der", dur=5.5, tam=520),
]
ROTULOS = []
SFX = {   # uno distinto por momento (regla: nada de SFX repetidos)
    "zumbido": ("Swarm of cartoon bees buzzing around a honey hive, playful 90s platformer", 3),
    "arcoiris": ("Magical cartoon rainbow appearing with a sparkling shimmer and chime glissando", 3),
    "mordida": ("Cartoon piranha snapping bite, sharp chomp underwater with bubbles", 2),
    "inflar": ("Giant inflatable toy dinosaur inflating fast with air pump hiss and rubber squeak", 3),
    "chispazo": ("Electric floor sparking and zapping, buzzing electricity crackle, cartoon factory", 3),
    "boom": ("Cartoon dynamite warehouse explosion, big comedic boom with falling debris", 3),
    "gas": ("Toxic gas hissing out of vents filling a sewer cave, ominous", 3),
    "sello": ("Rubber stamp slammed on paper with a firm comedic thump", 1),
    "salida": ("Cartoon race starting pistol shot followed by a quick whoosh", 2),
}
PISTAS = [
    dict(sfx="zumbido", en="Los Zubbas son abejas", vol=.35),
    dict(sfx="arcoiris", en="para que aparezca un arcoíris", vol=.4),
    dict(sfx="mordida", en="Basta una sola mordida", vol=.45),
    dict(sfx="sello", en="la respuesta es no", vol=.5),
    dict(sfx="inflar", en="él se infla hasta llenar la carpa", vol=.4),
    dict(sfx="chispazo", en="electrifica el suelo", vol=.4),
    dict(sfx="boom", en="vuela el almacén entero", vol=.5),
    dict(sfx="gas", en="se llena de gas tóxico", vol=.4),
    dict(sfx="salida", en="La mecánica es simple", vol=.4),
]
