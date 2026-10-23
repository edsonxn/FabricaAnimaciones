# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 15 cosas más INÚTILES de Skyrim» (SECUENCIA YT, Crónicas de Tamriel, 23-oct-2026).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 16 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con datos del guion, arriba a la derecha.
- Pegatinas con la imagen REAL (wiki de Fandom) de cada personaje u objeto que se nombra; ~1 de cada 5 grande.
- 6 motion graphics NUEVOS de este guion (regla del 19-oct-2026): agenda «La agenda de Nazeem» (15) · lena «La cuenta de la
  leña» (14) · salud «Bollo contra poción» y receta «La panadería de Skyrim» (10) · trato «El trato de Clavicus Vile» (4, en dos
  apariciones) · compraventa «El negocio del Pergamino» (1). Más la rejilla de probabilidad (2 de 101) de la Cuchilla (5).
- 3 mapas reales (tema tes): Piedra de la Torre (13), santuario de Clavicus (4) y Punta Mellada en ventana (2).
  python fab.py tes_cosas_inutiles fx --seco   tiempos      python fab.py tes_cosas_inutiles fx hoja   previews/fx_NN.jpg (MÍRALA)
"""
import os

import mg_tes as T

CAMARA = {}
FUNDIDO = {}

_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")   # imágenes reales de la wiki de Fandom
_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas")
TEMA_MAPA = "tes"


def P(slug):
    return os.path.join(_PEG, slug + ".png")


def ficha(en, nombre, efecto, origen=None, dur=5.0, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    """Pegatina con la imagen REAL de lo que nombra la voz (regla de canal): abajo a la izquierda."""
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.75, tam=640):
    """Pegatina GRANDE (media pantalla) para los personajes clave, del lado contrario a las fichas."""
    return peg(en, slug, titulo, dur=dur, x=x, y=.50, tam=tam)


def aviso(en, arriba, titulo, dur=3.6):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, slug + ".jpg"), puntos, TEMA_MAPA, titulo=titulo, sub=sub,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


AGENDA = [(20, 8, "Posada", T.ORO), (8, 12, "Mercado", T.HUESO), (12, 16, "Paseo", T.GRIS), (16, 20, "Posada", T.ORO)]
INGREDIENTES = [(P("sal"), "Sal"), (P("harina"), "Harina"), (P("mantequilla"), "Mantequilla"), (P("leche"), "Leche"),
                (P("huevo"), "Huevo")]
HACHA = ["22 de daño", "Quita 20 de aguante", "El arma más lenta del juego", "Sin ventajas de Herrería"]


def _trato(datos=()):
    return T.trato("El trato de Clavicus Vile", (P("barbas"), "Barbas"), (P("mascara"), "Máscara de Clavicus Vile"),
                   (P("hacha_arrep"), "Hacha del arrepentimiento"), ["Le devuelves al perro", "Matas a Barbas"], list(datos),
                   sello=("NI ES ARTEFACTO", 2 + len(datos)) if datos else None)


FX = [
    # ---- avisos (uno por puesto)
    aviso("hoy van las quince cosas", "Top 15", "Las cosas más inútiles de Skyrim", dur=4.5),
    aviso("Número quince", "Inútil · número 15", "Nazeem"),
    aviso("En el catorce", "Inútil · número 14", "Cortar leña"),
    aviso("Número trece", "Inútil · número 13", "La Piedra de la Torre"),
    aviso("En el doce", "Inútil · número 12", "La Llave de cera"),
    aviso("Número once", "Inútil · número 11", "Clarividencia"),
    aviso("En el diez", "Inútil · número 10", "El bollo dulce"),
    aviso("Número nueve", "Inútil · número 9", "Telequinesia"),
    aviso("En el ocho", "Inútil · número 8", "Reflejos rápidos"),
    aviso("Número siete", "Inútil · número 7", "Los caballos"),
    aviso("En el seis", "Inútil · número 6", "Dos poderes de raza"),
    aviso("Número cinco", "Inútil · número 5", "La Cuchilla de Mehrunes"),
    aviso("En el cuatro", "Inútil · número 4", "El Hacha del arrepentimiento"),
    aviso("Número tres", "Inútil · número 3", "Ser hombre lobo"),
    aviso("Número dos", "Inútil · número 2", "Proyectar voz"),
    aviso("llegamos al número uno", "Inútil · número 1", "El Pergamino Antiguo"),

    # ---- gancho
    peg("insultar a un bandido", "bandido", "Un bandido", dur=3.6),

    # ---- 15 · Nazeem
    grande("Si has pasado por el mercado", "nazeem", "Nazeem", dur=6.0, x=.25, tam=640),
    ficha("presume de que aconseja", "Nazeem", "Dice que aconseja al jarl. *Nunca* pisa el palacio.", origen="Carrera Blanca",
          dur=8.0),
    peg("ni el jarl ni nadie", "balgruuf", "El jarl", dur=3.6),
    peg("la granja la trabaja otro", "wilmuth", "Wilmuth", dur=3.4),
    mg(T.agenda("La agenda de Nazeem", AGENDA, retrato=P("nazeem"), remate=("Horas de trabajo: 0", 4)),
       ("Y él qué hace todo el", -.2), ("vuelve a la posada a descansar|fin", 1.6),
       ["Duerme doce horas", "pasa cuatro horas", "pasea un rato", "a las cuatro de la", ("descansar", .6)], "agenda"),
    peg("un guardia con una flecha", "guardia", "Un guardia", dur=4.0),

    # ---- 14 · cortar leña
    peg("el leñador Hod", "hod", "Hod", dur=5.0),
    peg("Coges el hacha", "hacha_lenador", "Hacha de leñador", dur=4.0, tam=340),
    mg(T.lena("La cuenta de la leña", P("lena"), P("hogar_brisa"), 5, 5000, "Hogar de la Brisa",
              remate=("1 000 veces la misma animación", 4)),
       ("La casa más barata", -.2), ("para tener un techo|fin", 1.4),
       ["La casa más barata", "el Hogar de la Brisa", "O sea mil piezas", "Mil veces la misma", "para tener un techo"], "leña"),
    ficha("cada pieza vale una moneda", "Leña", "Hod la paga a *5.* Cualquier otro mercader, a *1.*", origen="Precio", dur=6.5),
    peg("Eres el Sangre de Dragón", "dragon", "El Sangre de Dragón", dur=4.5, tam=440),

    # ---- 13 · la Piedra de la Torre
    grande("y luego está esta", "piedra_torre", "La Piedra de la Torre", dur=4.0, tam=600),
    mapa("skyrim", [(.56, .215, "Lucero del Alba", "inicio"), (.60, .225), (.645, .205, "Piedra de la Torre", "meta"),
                    (.69, .22), (.73, .215, "Hibernalia", "paso")],
         de="Está a medio camino", a=("a pulso|fin", .8), marcas=["Lucero del Alba", "acantilado nevado", "Hibernalia"],
         titulo="Skyrim", sub="La Piedra de la Torre"),
    ficha("Su poder es abrir sola", "La Piedra de la Torre", "Una vez al día abre una cerradura *experta* o menor.",
          origen="Piedra guardiana", dur=6.5),
    ficha("Las de nivel maestro", "Nivel maestro", "Esas *no* las abre.", origen="La Piedra de la Torre", rojo=True, dur=4.5),
    peg("cualquier ganzúa", "ganzua", "Una ganzúa", dur=4.5, tam=440),
    ficha("no cuentan en tus estadísticas", "Estadísticas", "Lo que abre la piedra *no cuenta.* Ni para el logro de ladrón.",
          origen="La Piedra de la Torre", rojo=True, dur=6.5),

    # ---- 12 · la Llave de cera
    ficha("Es una ventaja de Abrir cerraduras", "Llave de cera", "Te da una copia de la llave de la cerradura que *ya "
          "forzaste.*", origen="Abrir cerraduras · nivel 50", dur=8.0),
    peg("acabas de abrir", "ganzua", "Ya está abierta", dur=4.0, tam=420),
    ficha("está Irrompible", "Irrompible", "Las ganzúas *no se rompen nunca.*", origen="Abrir cerraduras · nivel 100", dur=6.5),

    # ---- 11 · Clarividencia
    ficha("Es un hechizo de Ilusión", "Clarividencia", "Muestra el camino a tu objetivo actual.", origen="Ilusión · novato",
          dur=7.0),
    ficha("pero gastando veinticinco puntos", "Clarividencia", "*25* de magia por segundo.", origen="Coste", rojo=True, dur=5.5),

    # ---- 10 · el bollo dulce
    peg("A ver si lo adivino", "guardia", "Un guardia", dur=4.0),
    grande("Es la comida más famosa", "bollo", "Bollo dulce", dur=4.5, x=.25, tam=560),
    ficha("Hay ciento sesenta bollos", "Bollo dulce", "*160* colocados a mano, en más de *80* sitios.", origen="Comida", dur=6.0),
    mg(T.salud("Salud", (P("bollo"), "Bollo dulce", 5), (P("pocion_curacion"), "Poción de curación menor", 25), 5),
       ("Te cura cinco puntos", -.2), ("con mucha educación|fin", .8),
       ["Te cura cinco puntos", "te cura veinticinco", "comerte cinco bollos", "un draugr te espera"], "salud"),
    mg(T.receta("La panadería de Skyrim", INGREDIENTES, (P("bollo"), "Bollo dulce"), "+5 de salud",
                remate=("Un punto por ingrediente", 6)),
       ("Y con Hearthfire", -.2), ("no fallan|fin", .8),
       ["Sal harina", "harina mantequilla", "mantequilla leche", "leche y un huevo", "un huevo", "Cinco ingredientes para cinco",
        "Un punto por ingrediente"], "receta"),

    # ---- 9 · Telequinesia
    peg("un hechizo de Alteración", "telequinesia", "Telequinesia", dur=4.5, tam=380),
    ficha("Y cuesta ciento setenta", "Telequinesia", "*170* de magia por segundo. En combate, *no sirve.*",
          origen="Alteración · adepto", dur=8.0),
    peg("se lo compras a Tolfdir", "tolfdir", "Tolfdir", dur=4.5),
    ficha("un veinticinco por ciento", "El libro", "*25 %* de que aparezca en una ruina.", origen="Telequinesia", dur=5.0),

    # ---- 8 · Reflejos rápidos
    peg("Es una ventaja de Bloquear", "escudo", "Bloquear", dur=4.5, tam=380),
    ficha("el tiempo se ralentiza", "Reflejos rápidos", "El tiempo se ralentiza si *bloqueas* un ataque de poder.",
          origen="Bloquear · nivel 30", dur=8.0),
    ficha("tiene un error famoso", "Error", "La cámara lenta puede *no terminar nunca.*", origen="Reflejos rápidos", rojo=True,
          dur=7.0),

    # ---- 7 · los caballos
    grande("un caballo debería ser", "caballo", "Un caballo", dur=5.0, x=.25, tam=620),
    ficha("puedes luchar montado", "Combate a caballo", "Armas y arco, sí. Magia, *no.*", origen="Caballos", dur=6.0),
    ficha("El caballo cuenta como testigo", "Testigo", "Si cometes un crimen delante de él, *te vio.*", origen="Caballos",
          rojo=True, dur=7.0),
    grande("Shadowmere solo lo consigues", "shadowmere", "Shadowmere", dur=5.5, x=.25, tam=600),

    # ---- 6 · dos poderes de raza
    ficha("El imperial tiene la Voz", "Voz del Emperador", "Calma a la gente cercana *60* segundos. Una vez al día.",
          origen="Poder imperial", dur=8.0),
    peg("Ni animales ni monstruos", "draugr", "Ni monstruos", dur=4.0, tam=380),
    peg("El bosmer tiene Dominar", "bosmer", "Bosmer", dur=4.0),
    ficha("El bosmer tiene Dominar", "Dominar animal", "Un animal aliado *60* segundos. Una vez al día.", origen="Poder bosmer",
          dur=7.0),
    peg("Un lobo amigo", "lobo", "Un lobo", dur=4.0, x=.13, tam=340),
    peg("contra el primer bandido", "bandido", "Un bandido", dur=3.0, x=.32, tam=340),
    ficha("Encuentra unas cuantas monedas", "Suerte imperial", "Unas monedas *de más* en los cofres con oro.",
          origen="Imperial", dur=6.5),

    # ---- 5 · la Cuchilla de Mehrunes
    peg("vive Silo Vesuio", "silo", "Silo Vesuio", dur=5.0),
    peg("las piezas de la daga", "cuchilla", "Cuchilla de Mehrunes", dur=5.5, x=.40, tam=420),
    grande("Mehrunes Dagon te pone una condición", "dagon", "Santuario de Mehrunes Dagon", dur=5.0, x=.75, tam=600),
    mg(T.rejilla("Muerte instantánea", n=101, encendidas=2, remate=("2 de 101", 1)),
       ("La probabilidad Según", -.2), ("ninguna ventaja de Herrería|fin", .6),
       ["La probabilidad Según", "dos entre ciento uno"], "rejilla"),
    peg("Miraak y Karstaag", "miraak", "Miraak", dur=4.5, x=.13, tam=340),
    peg("y Karstaag son inmunes", "karstaag", "Karstaag", dur=4.0, x=.30, tam=340),

    # ---- 4 · el Hacha del arrepentimiento
    grande("te encuentras con un perro", "barbas", "Barbas", dur=5.0, x=.75, tam=620),
    peg("el compañero de Clavicus Vile", "clavicus", "Clavicus Vile", dur=4.5, tam=440),
    mapa("skyrim", [(.425, .775, "Falkreath", "inicio"), (.475, .775), (.525, .748), (.585, .718, "Santuario de Clavicus", "meta")],
         de="Lo acompañas por media", a=("te manda a por un hacha|fin", .6), marcas=["Lo acompañas", "hasta el santuario"],
         titulo="Skyrim", sub="El mejor amigo de un daedra"),
    mg(_trato(), ("Y cuando vuelves con ella", -.2), ("te la puedes quedar|fin", .8),
       ["Si le devuelves al perro", "si matas a Barbas"], "trato"),
    grande("Barbas es invulnerable", "barbas", "Barbas", dur=5.0, x=.25, tam=600),
    mg(_trato(HACHA), ("Así que matas al perro", -.2), ("del arrepentimiento|fin", .8),
       [("Así que matas al perro", 0), ("Así que matas al perro", 0), "Un hacha de veintidós", "le quita veinte puntos",
        "Es el arma cuerpo a cuerpo", "No mejora con ninguna", "ni siquiera cuenta como"], "trato 2"),

    # ---- 3 · hombre lobo
    grande("Los Compañeros de Carrera Blanca", "aela", "Aela la Cazadora", dur=5.5, x=.25, tam=600),
    grande("Te transformas una vez al día", "hombre_lobo", "Hombre lobo", dur=5.0, x=.25, tam=560),
    ficha("Te transformas una vez al día", "Forma bestial", "*150* segundos al día. *+30* por cada cadáver.",
          origen="Hombre lobo", dur=7.0),
    ficha("mientras eres lobo no puedes", "Sin", "Equipo, hechizos, gritos ni poderes. *Ni el mapa.*", origen="Forma bestial",
          rojo=True, dur=12.0),
    ficha("antes de Dawnguard", "Árbol de ventajas", "*Ninguno* hasta Dawnguard.", origen="Hombre lobo", rojo=True, dur=7.0),

    # ---- 2 · Proyectar voz
    mapa("skyrim", [(.60, .46, "Punta Mellada", "peligro")], de="Sus tres palabras están", a=("sacerdote dragón Krosis|fin", .6),
         marcas=["en Punta Mellada"], titulo="Skyrim", ventana=True),
    peg("un sacerdote dragón Krosis", "krosis", "Krosis", dur=4.5),
    ficha("Y cada palabra te cuesta", "Proyectar voz", "*3* almas de dragón. Las *3* palabras hacen lo mismo.", origen="Grito",
          dur=10.0),
    ficha("Insultos", "Lo que grita", "Oye, *cerebro de queso.* Oye, *nariz de melón.* Oye, *feo.*", origen="Proyectar voz",
          dur=6.5),
    peg("un gigante o a un mamut", "gigante", "Un gigante", dur=4.5, x=.13, tam=340),
    peg("o a un mamut", "mamut", "Un mamut", dur=4.2, x=.32, tam=340),

    # ---- 1 · el Pergamino Antiguo
    peg("Un Pergamino Antiguo un Elder Scroll", "pergamino", "Pergamino Antiguo", dur=6.0, x=.30, tam=640),
    peg("el grito que derrota a Alduin", "alduin", "Alduin", dur=4.0, tam=440),
    ficha("Pesa veinte", "Pergamino Antiguo", "Peso *20*, pero *0* en tu inventario. Valor: *0* monedas.",
          origen="Objeto de misión", dur=6.0),
    peg("llevárselo a Urag", "urag", "Urag gro-Shub", dur=3.0, x=.75, y=.50, tam=560),
    mg(T.compraventa("El negocio del Pergamino", (P("pergamino"), "Pergamino Antiguo"),
                     [("Lo usas una vez", None), ("Urag te lo compra", 2000), ("Dawnguard lo pide otra vez", None),
                      ("Urag te lo revende", -4000)], remate=("El doble", 4)),
       ("te lo compra por dos mil", -1.0), ("volver a comprarlo más caro|fin", .8),
       [("te lo compra por dos mil", -1.0), "por dos mil monedas", "Y si tienes Dawnguard", "por cuatro mil", "El doble"],
       "compraventa"),

    # ---- cierre
    ficha("en el canal tienes los ocho", "Los 8 exploits más ROTOS de Skyrim", "Ya está en el canal.",
          origen="Video recomendado", dur=6.0, x=.5, y=.40),
    peg("Que se lo quede", "bollo", "Cura cinco", dur=4.0, tam=420),
]

SFX = {
    "aviso_c": ("Single deep frame drum hit with a short rising low brass swell, nordic fantasy quest notification", 3),
    "aviso_d": ("Low male choir hum swelling into one soft drum hit, fantasy quest objective sting", 3),
    "monedas_b": ("Small stack of gold coins clinking onto a wooden table one by one, medieval tavern", 2),
    "hachazo": ("Single axe chop splitting a wooden log on a chopping block, crisp wood crack", 1),
    "sello_b": ("Wax seal stamp pressed hard onto parchment on a wooden desk, dull thud", 1),
}
_AV = ["hoy van las quince cosas", "Número quince", "En el catorce", "Número trece", "En el doce", "Número once",
       "En el diez", "Número nueve", "En el ocho", "Número siete", "En el seis", "Número cinco", "En el cuatro", "Número tres",
       "Número dos", "llegamos al número uno"]
PISTAS = [dict(sfx="aviso_c" if k % 2 == 0 else "aviso_d", en=a, vol=.6 if k in (0, 15) else .5) for k, a in enumerate(_AV)] + [
    dict(sfx="hachazo", en="partes un tronco", vol=.5),
    dict(sfx="monedas_b", en="cada pieza de leña por cinco", vol=.45),
    dict(sfx="monedas_b", en="Mil veces la misma", vol=.4),
    dict(sfx="sello_b", en="ni siquiera cuenta como", vol=.55),
    dict(sfx="monedas_b", en="por dos mil monedas", vol=.45),
    dict(sfx="monedas_b", en="por cuatro mil", vol=.45),
]
