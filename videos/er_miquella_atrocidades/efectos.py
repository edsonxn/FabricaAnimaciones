# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Miquella QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 19-oct-2026).
Fórmula de Crónicas de Warcraft (docs/estilo_secuencia_yt.md § PEGATINAS) con el kit de Elden Ring (nucleo/mg_er.py):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de eldenring.fandom.com en pegatinas/), chicas abajo a la
  izquierda, en fila cuando la voz enumera, y ~1 de cada 5 GRANDE (media pantalla) del lado contrario a las fichas.
- PANTALLAS a cuadro entero (pantallas/, fuentes en pantallas/_fuentes.txt) donde el clip no enseña lo que hace falta ver.
- fichas de descripción (icono real) SOLO con citas verificadas del guion, arriba a la derecha; rótulo de puesto por atrocidad.
- MG por código: hilos del encanto (y cómo se rompen), el «cosido» Radahn + Mohg, las cruces y la tríada cuerpo/alma/voluntad.
  python fab.py er_miquella_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_miquella_atrocidades fx         audio/fx.wav
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


FX = [
    # ================================================================ GANCHO
    pant("mohg_carga_miquella", ("raptado dentro de su capullo", -.4), ("Todos le tuvimos pena|fin", .2), zoom=(1.0, 1.12)),
    peg("su hermana Malenia", "malenia_icono", "Malenia", tam=360, x=.83, y=.60),
    peg("nunca le vi la cara", "miquella_nino", "Miquella", y=.60),
    grande("el niño bondadoso resultó ser", "miquella", "Miquella el Bondadoso", lado="der", dur=5.2),
    peg("en la descripción de su yelmo", "yelmo_malenia", "Yelmo alado de Malenia", tam=340),
    ficha("Miquella posee la sabiduría", "Yelmo alado de Malenia",
          "Miquella posee *la sabiduría y el encanto de un dios*, y es *el más temible* de todos los Empíreos.",
          tipo="Armadura de cabeza", icono="yelmo_malenia", a=("de todos los Empíreos|fin", .6)),
    grande("sir Ansbach, que te lo suelta", "ansbach", "Sir Ansbach", dur=5.6, tam=600),
    ficha("en la primera conversación sin anestesia", "Sir Ansbach", "Miquella el Bondadoso *es un monstruo*.",
          tipo="Lo que dice", a=("es un monstruo|fin", 1.2)),
    puesto("las cinco peores atrocidades de Miquella", "Las 5 peores atrocidades de", "Miquella", dur=4.2),
    peg("mientras todos mirábamos a Mohg", "mohg", "Mohg, Señor de la Sangre", tam=420),
    peg("el niño del capullo estaba moviendo", "miquella_nino", "El niño del capullo", x=.80, y=.60, tam=360),

    # ================================================================ 5 · EL ENCANTO
    puesto("Número cinco. El encanto", "Atrocidad número 5", "El encanto"),
    peg("puedes conseguir la Rama hechizante", "rama", "Rama hechizante", tam=420),
    ficha("Y la descripción de esa rama", "Rama hechizante",
          "El Empíreo Miquella es amado por mucha gente. De hecho, *ha aprendido muy bien a provocar ese afecto*.",
          tipo="Herramienta", icono="rama", a=("Dice que él sabe cómo hacer que lo quieran|fin", .3)),
    dict(tipo="mg", fn=E.hilos("Miquella", ["Leda", "Ansbach", "Freyja", "el Cornudo", "Thiollier"], "Los seguidores de Miquella"),
         de=("Todo el grupo que te encuentras", -.2), a=("y unos cuantos más|fin", .6),
         marcas=["sigue a Miquella", "Leda, la caballera", "sir Ansbach, Freyja", "Freyja, el Cornudo", "el Cornudo, Thiollier",
                 "Thiollier, y unos"], y=.50, sale=.4, nombre="MG hilos", ver=5.0),
    *fila("Un caballero de la sangre pura", [
        ("ansbach", "Sir Ansbach", None),
        ("freyja", "Freyja", "una guerrera de la guardia de Radahn"),
        ("cornudo", "El Cornudo", "un Cornudo que odia"),
        ("thiollier", "Thiollier", "un envenenador perdidamente enamorado")], dur=9.0),
    grande("lo dice la propia Leda", "leda", "Leda, caballera de la aguja", dur=6.0, tam=640),
    ficha("sin el encanto de Miquella, esos compañeros", "Leda, caballera de la aguja",
          "Sin el encanto de Miquella, *esos compañeros se habrían ido a los golpes* a primera vista.", tipo="Lo que dice",
          a=("a primera vista|fin", .8)),
    peg("solo se aguanta porque hay uno que paga", "frasco", "Las cervezas", tam=300, x=.83, y=.62),
    # MASTER 1 (19-oct): llegaba hasta «mala espina» = 21,6 s de imagen fija; ahora ~9,5 s y vuelve el gameplay
    pant("seguidores", "Y piénsalo un segundo", ("les ayudaste sin preguntar|fin", .3), zoom=(1.0, 1.12), pan=(0, 0, .1, 0)),

    # ---- 5b · se rompe
    peg("Cuando te acercas a la fortaleza de Messmer", "messmer", "Messmer el Empalador", tam=380),
    dict(tipo="destello", en="una luz dorada estalla en el cielo"),
    ficha("Miquella ha roto su Gran Runa", "Gran Runa de Miquella", "Rota. *Partida por su dueño.*", tipo="Gran Runa",
          icono="runa_miquella", dur=4.0),
    dict(tipo="mg", fn=E.hilos("Miquella", ["Leda", "Ansbach", "Freyja", "el Cornudo", "Thiollier"], "Se rompe el encanto"),
         de=("Y con la runa, se rompe el encanto", -.3), a=("con una calma que da miedo|fin", .3),
         marcas=["Y con la runa"] * 6 + ["se rompe el encanto"], y=.50, sale=.4, nombre="MG hilos rotos", ver=5.0),
    peg("el encantamiento del bondadoso Miquella ha expirado", "freyja", "Freyja", tam=380),
    ficha("el encantamiento del bondadoso Miquella ha expirado", "Freyja de la melena roja",
          "El encantamiento del bondadoso Miquella *ha expirado*, y eso puede ser *desorientador*, por decirlo suavemente.",
          tipo="Lo que dice", a=("por decirlo suavemente|fin", .6)),
    *fila("Thiollier, el del veneno", [
        ("thiollier", "Thiollier", None),
        ("aguja_thiollier", "Aguja oculta de Thiollier", "se queda perdido"),
        ("trina", "Santa Trina", "los recuerdos de Santa Trina")], dur=7.0),
    grande("Y la que no despierta es Leda", "leda", "Leda", lado="der", dur=4.4, tam=600),
    peg("eliminar a los que no son dignos", "espada_leda", "Espada de Leda", tam=380),
    peg("Primero va por el Cornudo", "cornudo", "El Cornudo", tam=380),
    peg("Luego va por Ansbach", "ansbach", "Sir Ansbach", tam=380),
    peg("con su espada de sangre", "medalla_sangre", "Caballeros de la sangre pura", x=.83, y=.62, tam=300),
    peg("compartían hoguera", "leda", "Leda", tam=360),

    # ================================================================ 4 · EL TAXI DE LA SANGRE
    puesto("Bajamos al cuatro", "Atrocidad número 4", "El taxi de la sangre"),
    grande("Mohg, el Señor de la Sangre. El de la cueva", "mohg", "Mohg, Señor de la Sangre", lado="der", dur=5.0, tam=720),
    peg("el del tridente", "lanza_mohg", "Lanza sagrada de Mohgwyn", tam=420),
    pant("mohgwyn", ("se lo llevó a su palacio de Mohgwyn", -.3), ("para convertirse en su consorte|fin", .3), zoom=(1.0, 1.10)),
    peg("se robó el capullo de Miquella", "miquella_nino", "Miquella", tam=340),
    peg("Su recuerdo lo cuenta así", "recuerdo_sangre", "Recuerdo del Señor de la Sangre", tam=380),
    ficha("queriendo elevar a Miquella a la divinidad plena", "Recuerdo del Señor de la Sangre",
          "Queriendo elevar a Miquella a la divinidad plena, Mohg quiso ser *su consorte*. Pero *nunca recibió respuesta* "
          "del joven Empíreo.", tipo="Recuerdo", icono="recuerdo_sangre", a=("del joven Empíreo|fin", .6)),
    peg("y con todos mis frascos", "frasco", "Frasco de lágrimas carmesí", tam=320),
    grande("sir Ansbach, que fue comandante", "ansbach", "Sir Ansbach", dur=5.0, tam=600),
    peg("caballeros de la sangre pura de Mohg", "medalla_sangre", "Medalla de caballero de sangre pura", x=.83, y=.62, tam=300),
    ficha("Ansbach te confiesa", "Sir Ansbach", "Una vez reté a Miquella para *liberar a lord Mohg de su encantamiento*.",
          tipo="Lo que dice", a=("De su encantamiento|fin", .6)),
    dict(tipo="mg", fn=E.mensaje(["Mohg no se llevó a Miquella.", "Miquella hizo que Mohg se lo llevara."]),
         de=("Mohg no se llevó a Miquella", -.2), a=("Miquella hizo que Mohg se lo llevara|fin", 1.2),
         marcas=["Mohg no se llevó a Miquella", "Miquella hizo que Mohg"], y=.78, sale=.5, nombre="MG mensaje taxi", ver=3.0),
    peg("ese brazo seco que asoma del capullo", "miquella_nino", "El capullo de Miquella", tam=360),
    peg("fue el taxi", "mohg", "Mohg (el taxi)", x=.80, y=.60, tam=420),

    # ---- 4b · el cascarón
    ficha("más que a nadie, culpo al encantamiento", "Sir Ansbach", "Más que a nadie, *culpo al encantamiento*.",
          tipo="Lo que dice", dur=5.0),
    peg("cuando tú matas a Mohg en su palacio", "recuerdo_sangre", "Mohg, derrotado", tam=380),
    ficha("tras la muerte de lord Mohg en su palacio", "Sir Ansbach",
          "Tras la muerte de lord Mohg, *alguien se ha llevado su cuerpo*.", tipo="Lo que dice",
          a=("qué pensarán hacer con sus restos|fin", .5)),
    grande("un pergamino de corteza blanca", "pergamino", "Pergamino del rito secreto", dur=4.0, tam=560),
    ficha("el Pergamino del rito secreto", "Pergamino del rito secreto",
          "Un señor anunciará el regreso de un dios, y *el alma de ese señor necesitará un recipiente*.", tipo="Objeto clave",
          icono="pergamino", a=("necesitará un recipiente|fin", 1.2)),
    peg("Cuando le entregas ese pergamino a Ansbach", "ansbach", "Sir Ansbach", tam=380),
    ficha("Miquella ha abandonado el alma de lord Mohg", "Sir Ansbach",
          "Miquella ha abandonado el alma de lord Mohg. *Solo desea su cascarón vacío*.", tipo="Lo que dice",
          a=("Solo desea su cascarón vacío|fin", .5)),
    ficha("mi querido señor merecía algo mejor", "Sir Ansbach", "Mi querido señor *merecía algo mejor*.", tipo="Lo que dice",
          dur=4.4),
    pant("mohg_jefe", "Piénsalo. Mohg pasó siglos", ("Ni siquiera un rechazo|fin", .2), zoom=(1.0, 1.12)),
    peg("Yo maté a Mohg en tres partidas", "lanza_mohg", "Mohg", tam=360),
    peg("el trabajo sucio al niño del capullo", "miquella_nino", "El niño del capullo", x=.80, y=.60, tam=360),

    # ================================================================ 3 · EL CONSORTE PROMETIDO
    puesto("Número tres. El general Radahn", "Atrocidad número 3", "El consorte prometido"),
    grande("el de la Plaga Estelar", "radahn", "Radahn, Azote Estelar", lado="der", dur=5.0, tam=720),
    peg("Un recuerdo de la expansión", "recuerdo_dios", "Recuerdo de un dios y un señor", tam=380),
    ficha("en su infancia, Miquella vio en Radahn", "Recuerdo de un dios y un señor",
          "En su infancia, Miquella vio en Radahn *a un señor*. Y pidió su deseo: que Radahn fuera *su rey consorte*.",
          tipo="Recuerdo", icono="recuerdo_dios", a=("fuera su rey consorte|fin", .6)),
    *fila("los gemelos, Miquella y su hermana Malenia", [
        ("miquella_nino", "Miquella", None),
        ("malenia_icono", "Malenia", "su hermana Malenia#2")], dur=4.0),
    peg("medio hermano por parte de Radagon", "radagon", "Radagon", tam=400),
    pant("malenia_vs_radahn", "Él y Malenia pelearon en la batalla de Aeonia",
         ("la putrefacción escarlata|fin", .3), zoom=(1.0, 1.12), pan=(0, 0, .15, 0)),     # antes 12,9 s
    peg("Malenia hizo florecer la putrefacción escarlata", "malenia_icono", "Malenia", tam=360),
    peg("El Yelmo del joven león", "yelmo_leon", "Yelmo del joven león", tam=420),
    ficha("el casco de Radahn cuando era joven", "Yelmo del joven león",
          "Cuando Malenia, la espada de Miquella, hizo florecer la flor de la putrefacción en Aeonia, *Radahn escuchó un "
          "murmullo al oído*.", tipo="Armadura de cabeza", icono="yelmo_leon", a=("escuchó un murmullo al oído|fin", 1.4)),
    dict(tipo="mg", fn=E.mensaje(["Miquella te espera,", "oh consorte prometido"]),
         de=("Y el murmullo decía", -.1), a=("oh consorte prometido|fin", 2.0),
         marcas=["Miquella te espera", "oh consorte prometido"], y=.76, sale=.5, nombre="MG murmullo", ver=3.0),
    peg("lo primero que oye el general", "radahn", "Radahn", tam=380),
    peg("ni al mercader Kalé", "kale", "El mercader Kalé", x=.83, y=.60, tam=320),
    *fila("Malenia no es la espada de Márika", [
        ("marika", "Márika", None),
        ("malenia_icono", "Malenia, espada de Miquella", "Es la espada de Miquella")], dur=5.0),

    # ---- 3b · el cosido
    peg("Luego viene el festival de la guerra", "radahn", "El festival de Radahn", tam=380),
    peg("Y Freyja, que fue de su guardia", "espadon_freyja", "Espadón de Freyja", x=.83, y=.62, tam=320),
    ficha("al concluir el festival de la guerra", "Freyja de la melena roja",
          "El alma del general Radahn tuvo *un final honorable*. Pero el bondadoso Miquella *desea revivirla*.",
          tipo="Lo que dice", a=("desea revivirla|fin", .6)),
    dict(tipo="mg", fn=E.cosido(), de=("Ahora junta las piezas", -.2), a=("necesitará un recipiente#2|fin", 1.0),
         marcas=["El alma de Radahn", "el cuerpo vacío de Mohg", "y un pergamino"], y=.50, sale=.4, nombre="MG cosido", ver=5.0),
    pant("consorte_puerta", ("Al final de la expansión, en Enir-Ilim", -.3), ("te encuentras al Consorte prometido Radahn|fin", .3),
         zoom=(1.0, 1.10)),
    pant("consorte_cerca", "El alma de Radahn, metida dentro", ("Dos hermanos de Miquella cosidos en uno|fin", .2), zoom=(1.05, 1.18)),
    grande("El alma de Radahn, metida dentro", "recuerdo_dios", "Consorte prometido Radahn", lado="izq", dur=4.4, tam=560),
    pant("cuernos_radahn", "Y en los brazos y las piernas", ("nunca dejó de ser suyo|fin", .3), zoom=(1.0, 1.14), pan=(0, 0, .1, .05)),
    peg("los mismos cuernos malditos con los que nació Mohg", "mohg", "Mohg (los cuernos)", tam=380),
    peg("Es el regalo de bodas", "recuerdo_dios", "Consorte prometido Radahn", x=.80, y=.60, tam=380),
    ficha("En un recuerdo, Miquella le dice", "Miquella",
          "Hermano mayor, voy a ser un dios. Si cumplimos nuestra parte del juramento, *prométeme que serás mi consorte*.",
          tipo="Lo que dice, de niño", a=("prométeme que serás mi consorte|fin", .8)),
    peg("En un recuerdo, Miquella le dice", "miquella_nino", "Miquella", tam=380),
    peg("con su propio milagro", "luz_miquella", "Luz de Miquella", tam=400),
    ficha("la Luz de Miquella: un dios y un rey consorte", "Luz de Miquella",
          "Un dios y un rey consorte *es todo lo que el mundo necesita*.", tipo="Milagro", icono="luz_miquella",
          a=("Los demás sobramos|fin", .5)),

    # ================================================================ 2 · LO QUE DEJÓ TIRADO
    puesto("Ya en el podio, el número dos", "Atrocidad número 2", "Lo que dejó tirado"),
    peg("Ansbach, que las va buscando contigo", "arco_ansbach", "Arco largo de Ansbach", tam=380),
    dict(tipo="mg", fn=E.cruces(["la primera carne de mi cuerpo", "mi brazo izquierdo", "mi brazo derecho", "mi ojo", "mi corazón",
                                 "mis dudas y mis vacilaciones", "todos mis miedos"]),
         de=("La primera dice", -.2), a=("Aquí abandono todos mis miedos|fin", 1.2),
         marcas=["aquí abandono la primera carne", "Aquí abandono mi brazo izquierdo", "Aquí abandono mi brazo derecho",
                 "Aquí abandono mi ojo", "Aquí abandono mi corazón", "Aquí abandono mis dudas", "Aquí abandono todos mis miedos"],
         y=.72, sale=.4, nombre="MG cruces", ver=5.0),
    peg("Y la Gran Runa también la dejó atrás", "runa_miquella", "Gran Runa de Miquella", tam=380),
    ficha("Lo que queda de ella dice", "Gran Runa de Miquella",
          "Abandonada por Miquella, *rota y despojada de su abundancia*. Solo conserva el poder de *resistir encantos*.",
          tipo="Gran Runa", icono="runa_miquella", a=("la vacuna contra él mismo|fin", .5)),
    peg("Un niño que lo da todo por su meta", "miquella_nino", "Miquella", tam=360),
    dict(tipo="mg", fn=E.mensaje(["Aquí abandono mi amor."]),   # cruces() chocaba con el rótulo de zona del juego
         de=("Aquí abandono mi amor", -.3), a=("Aquí abandono mi amor|fin", 1.8),
         marcas=["Aquí abandono mi amor"], y=.80, sale=.5, nombre="MG cruz del amor", ver=3.0),

    # ---- 2b · Santa Trina y Malenia
    pant("trina_final", "Y ese amor tiene nombre", ("se rezaba en las Tierras Intermedias|fin", .3), zoom=(1.0, 1.12)),  # antes 18,5 s
    peg("Santa Trina era una figura misteriosa", "espada_trina", "Espada de Santa Trina", tam=380),
    grande("Y resulta que era Miquella", "trina", "Santa Trina", lado="der", dur=5.0, tam=640),
    pant("trina_inicio", "la dejó en ese agujero", ("a punto de marchitarse|fin", .4), zoom=(1.0, 1.10)),
    peg("rodeada de lirios morados", "lirio", "Lirio de Miquella", tam=360),
    ficha("Haz que Miquella se detenga", "Santa Trina",
          "Haz que Miquella se detenga. *No conviertas a la pobre criatura en un dios*. La divinidad sería *la prisión de "
          "Miquella*.", tipo="Lo que dice, tras beber su néctar", a=("ya no tiene salvación|fin", .5)),
    dict(tipo="mg", fn=E.mensaje(["Debes matar a Miquella.", "Concédele el perdón."]),
         de=("debes matar a Miquella", -.2), a=("Concédele el perdón|fin", 1.8),
         marcas=["debes matar a Miquella", "Concédele el perdón"], y=.76, sale=.5, nombre="MG mensaje Trina", ver=3.0),
    grande("Y luego está Malenia", "malenia_icono", "Malenia, espada de Miquella", dur=4.6, tam=560),
    peg("Su yelmo lo dice", "yelmo_malenia", "Yelmo alado de Malenia", tam=380),
    ficha("Malenia esperó a Miquella", "Yelmo alado de Malenia",
          "Malenia esperó a Miquella *a los pies del cascarón*. «Mi hermano *cumplirá su promesa*».",
          tipo="Armadura de cabeza", icono="yelmo_malenia", a=("mi hermano cumplirá su promesa|fin", .6)),
    pant("arbol_sagrado", "Ese árbol se regó", ("nunca llegó a ser un Árbol Áureo|fin", .3), zoom=(1.0, 1.12)),
    peg("Ese árbol se regó", "sobreveste", "Sobreveste del Árbol Sagrado", tam=360),
    *fila("Dejó a su amor en un agujero", [
        ("trina", "Santa Trina", None),
        ("malenia_icono", "Malenia", "a su hermana esperando"),
        ("leda", "Sus seguidores", "a sus seguidores")], dur=6.0),

    # ================================================================ 1 · LA ERA DE LA COMPASIÓN
    puesto("Y llegamos al número uno", "Atrocidad número 1", "La era de la compasión"),
    pant("miquella_llega", "Miquella no quería solo ser un dios", ("Hasta que lees qué significa|fin", .3), zoom=(1.0, 1.12)),
    peg("La Diadema de luz, la corona", "diadema", "Diadema de luz", tam=420),
    ficha("La Diadema de luz, la corona", "Diadema de luz",
          "Este círculo iba a ser la base sobre la que se construiría *la era de la compasión* de Miquella.",
          tipo="Armadura de cabeza", icono="diadema", a=("la era de la compasión de Miquella|fin", .5)),
    ficha("Y su milagro, la Luz de Miquella", "Luz de Miquella",
          "Miquella quiso aceptar todo lo que era y lo que sería, pero *encontró a uno que se negó a ser abrazado*.",
          tipo="Milagro", icono="luz_miquella", a=("Y ese alguien que se negó eres tú|fin", .5)),
    peg("Y ese alguien que se negó eres tú", "frasco", "Tú, el Sinluz", tam=320),
    pant("miquella_aparicion", "Ansbach lo describe mejor que nadie", ("para limpiar el corazón de los hombres|fin", .4),
         zoom=(1.0, 1.10), pan=(0, 0, .12, 0)),
    ficha("puro y radiante, Miquella", "Sir Ansbach", "Puro y radiante, Miquella *usa el amor para limpiar el corazón* de los hombres.",
          tipo="Lo que dice", a=("para limpiar el corazón de los hombres|fin", .6)),
    ficha("Te lo prometo", "Miquella, en la pelea",
          "Te lo prometo: *un viaje de mil años guiado por la compasión*. Señor del viejo orden, *vayamos juntos*.",
          tipo="Lo que te dice al agarrarte", a=("vayamos juntos|fin", .8)),
    grande("Ahora escucha lo que te dice en la pelea", "recuerdo_dios", "Consorte prometido Radahn", dur=4.0, tam=560),
    peg("Y si llevas puesta su runa partida", "runa_miquella", "Gran Runa de Miquella", tam=380),
    ficha("la frase cambia", "Miquella, en la pelea", "Que tus pensamientos *sean solo de amor*.",
          tipo="Con su Gran Runa puesta", icono="runa_miquella", a=("que tus pensamientos sean solo de amor|fin", 1.6)),

    # ---- 1b · la voluntad
    # antes repetía «seguidores» (ya salió en el #5): ahora la Tierra de las Sombras entera
    pant("tierra_sombras", "La era de la compasión de Miquella es el mundo entero", ("nadie con voluntad propia|fin", .3),
         zoom=(1.12, 1.0), pan=(.1, 0, 0, 0)),
    peg("Sin encanto, Leda dice", "leda", "Leda", tam=380),
    peg("Thiollier, que daría todo por Santa Trina", "thiollier", "Thiollier", tam=380),
    ficha("vengo a cumplir el único deseo de Santa Trina", "Thiollier",
          "Vengo a cumplir el único deseo de Santa Trina. *Detendré a Miquella el Bondadoso*. Jamás será un dios.",
          tipo="Antes de pelear contra Leda", a=("Jamás será un dios|fin", .6)),
    grande("Y Ansbach, si cae peleando a tu lado", "ansbach", "Sir Ansbach", dur=5.0, tam=600),
    ficha("Sinluz justo, conviértete", "Sir Ansbach",
          "Sinluz justo, *conviértete en nuestro nuevo señor*. Un señor no para los dioses, sino para los hombres.",
          tipo="Si cae a tu lado", a=("sino para los hombres|fin", .6)),
    peg("en las últimas palabras de Leda", "espada_leda", "Espada de Leda", tam=380),
    ficha("deseaba que Miquella hiciera del mundo", "Leda, caballera de la aguja",
          "Deseaba que Miquella hiciera del mundo *un lugar más amable*.", tipo="Sus últimas palabras",
          a=("por un mundo más amable|fin", .3)),
    dict(tipo="mg", fn=E.triada([("Mohg", "su cuerpo"), ("Radahn", "su alma"), ("Tú", "tu voluntad")]),
         de=("No quería tu cuerpo", -.3), a=("y llamarle a eso compasión|fin", .8),
         marcas=["No quería tu cuerpo", "Ni tu alma", "Quería tu voluntad"], y=.50, sale=.4, nombre="MG triada", ver=5.0),
    grande("la Diadema de luz que te queda", "diadema", "Diadema de luz", lado="der", dur=5.6, tam=620),
    *fila("Márika rompió el mundo", [
        ("marika", "Márika", None),
        ("radagon", "Radagon", "el tal Radagon"),
        ("rennala", "Rennala", "dejó a una reina abrazando un huevo")], dur=6.0),
    grande("Miquella es el único que te hace daño", "miquella", "Miquella el Bondadoso", dur=4.6, tam=620),

    # ================================================================ CIERRE
    peg("titiritero de media Tierra de las Sombras", "miquella_nino", "Miquella", tam=380),
    grande("es chiquito y tiene el pelo dorado", "miquella", "Chiquito y rubio", lado="der", dur=4.0, tam=600),
    *fila("quién fue peor, Miquella", [
        ("miquella_nino", "Miquella", None),
        ("marika", "Márika", "o Márika, que partió")], dur=5.0),
    puesto("en el canal tienes las cinco peores atrocidades de Márika", "Ya en el canal · Las 5 peores",
           "Márika y Radagon", dur=5.0),
    peg("Y si es un niño rubio dentro de un capullo", "miquella_nino", "El niño del capullo", x=.80, y=.60, tam=420),
]
ROTULOS = []
SFX = {   # uno distinto por momento (regla: nada de SFX repetidos)
    "runa": ("A great golden rune shattering in the sky, bright crystalline burst with a deep resonant boom, dark fantasy", 4),
    "susurro": ("Soft eerie whisper in an empty ruined chapel with a long ghostly reverb, dark fantasy", 4),
    "costura": ("Slow wet flesh stitching with taut thread pulled through, grotesque and quiet, dark fantasy", 3),
    "campana": ("One deep ominous church bell toll with a long reverb tail, dark fantasy", 4),
    "cruz": ("Heavy stone cross grinding as it settles into earth, low rumble, dark fantasy", 3),
}
PISTAS = [
    dict(sfx="runa", en="una luz dorada estalla en el cielo", vol=.5),
    dict(sfx="susurro", en="Y el murmullo decía", vol=.45),
    dict(sfx="costura", en="el cuerpo vacío de Mohg", vol=.4),
    dict(sfx="cruz", en="Aquí abandono mi amor", vol=.45),
    dict(sfx="campana", en="Y llegamos al número uno", vol=.5),
]
