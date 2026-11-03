# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Pokémon Rojo y Azul: su historia y los 20 secretos QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming,
3-nov-2026). Kit NUEVO `nucleo/mg_pokemon.py`: interfaz del Game Boy (cuatro verdes, cuadro de texto de RB translúcido, letra de
píxel, Poké Ball que se agita como al capturar). REGLA DE ORO (tes_secretos_40): las capas SUMAN; lo que dice la voz se ve; ningún
clip ni imagen de otro juego; MG desde el gancho; pegatinas variadas (peg_estilos, tema «pokemon»); `chequeo` antes de `video`.
Regla del 3-nov (cod_mw4_secretos): ≥ 5 MG y ≥ 5 pegatinas por minuto, ningún tramo > 4 s sin nada.
- Puestos `K.puesto` arriba; contador de esquina `K.hud` («aviso», no cuenta); fichas a la derecha; pegatinas abajo a la izquierda.
- MG de ESTE guion: nombres (Satoshi/Shigeru), índice Bulbasaur/Rhydon, ranuras (190 con los 39 huecos reales), ¿Gorochu?, ataques
  (BARRERA), foco, 1 de 256, tabla de tipos, equipo de Oak, mochila ×128, cartas 78 000 → 20 Mew, 300 bytes, pastel de Creatures,
  pistas Ditto = Mew, cable link, PS de «tu partida» y de Game Freak.
- MAPA REAL: arte oficial de Kanto de 1998 (mapas/kanto_rby.png, archives.bulbagarden.net), tema «pokemon»: ruta de medallas,
  Azulona, Carmín, Lavanda y la ruta de MissingNo (Verde → Canela → costa este).
  python fab.py pokemon_rojo_azul fx --seco | fx hoja | fx
"""
import os

import mg_pokemon as K
import mg_wow as W
import peg_estilos as PE

TEMA = "pokemon"
CAMARA = {}
FUNDIDO = {}

_FX, _FY = .75, .34            # fichas: a la derecha
_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def ficha(en, titulo, texto, tipo=None, dur=5.0, x=_FX, y=_FY, ancho=860):
    return dict(tipo="mg", fn=K.ficha(titulo, texto, tipo, ancho=ancho), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + titulo, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-5.0):
    return dict(tipo="mg", fn=K.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.27, tam=640):
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=860, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=500):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.78, y=.52, ancho=480, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.64, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + nombre, ver=2.0)


def com(en, cid, dur=5.0, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=K.pegatina(P("com_" + cid), None, tam, giro=-2.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + cid, ver=1.0)


def puesto(en, n, titulo, dur=4.2):
    return [dict(tipo="mg", fn=K.puesto(n, titulo), en=en, dur=dur, x=.5, y=.16, sale=.45, nombre=f"puesto {n}", ver=1.4)]


def hud(de, a, n):
    return dict(tipo="mg", fn=K.hud(21 - n, 20), de=de, a=a, x=.92, y=.08, sale=.3, nombre=f"aviso hud {n}", ver=1.0)


def mg(de, a, marcas, fn, nombre, x=.5, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def cartel(en, texto, sub=None, dur=3.0, x=.5, y=.80, k=6):
    return mg_en(K.cartel(texto, sub, k), en, dur, "cartel " + texto[:18], x=x, y=y)


def sello(en, texto, dur=2.2, x=.70, y=.40):
    return mg_en(K.sello(texto), en, dur, "sello " + texto, x=x, y=y)


def zoom(de, a, cuanto=1.12, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def mapa(puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, "kanto_rby.png"), puntos, TEMA, titulo=titulo, sub=sub,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa kanto", ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=.5, sale=.5, nombre="mapa kanto", ver=4.0)


# lugares del mapa oficial de Kanto (fracción del dibujo de 800×553)
P_PALETA, VERDE, PLATEADA, CELESTE = (.22, .72), (.16, .55), (.23, .21), (.58, .18)
CARMIN, AZULONA, AZAFRAN, LAVANDA = (.58, .54), (.41, .35), (.60, .35), (.82, .37)
FUCSIA, CANELA, MESETA, SS_ANNE = (.50, .83), (.25, .92), (.07, .16), (.52, .58)

FX = [
    # ================================================================ GANCHO (un elemento nuevo cada 2-3 s)
    zoom(0.0, ("Hay otro que Nintendo", -.1), 1.12),
    rel("se metió en el juego a escondidas", "a_mew", "Mew", "No.151", dur=3.0, x=.76, y=.50, tam=470),
    mg_en(K.exclama(), "a escondidas", 1.4, "exclama mew", x=.62, y=.30),
    cartel("en el último hueco", "Último hueco del *cartucho*", None, dur=2.6, x=.32, y=.82, k=5),
    cam("Nintendo te pedía no tocar", "missingno_rb", "MissingNo.", dur=2.4, x=.16, y=.64, foco=(.5, .5, 1.0)),
    mg_en(K.vida("TU PARTIDA", ":L99", 1.0, 0.0), "podía borrarte la partida", 2.6, "vida partida", x=.70, y=.30),
    peg("medio mundo lo buscó igual", "nintendo_power", "Nintendo Power", dur=2.4, x=.80, y=.62, tam=330, giro=6),
    sil("combate entero contra el Profesor Oak", "oak", "Prof. Oak", "Programado… y prohibido", dur=4.0, lado="der", alto=820),
    sello("nadie podía jugar", "INÉDITO", dur=2.2, x=.32, y=.36),
    mg_en(K.contador("Pokémon", [(30, "años: 27 de febrero de 2026", "30 AÑOS")]), "cumplió treinta años", 3.0, "contador 30", x=.33, y=.32),
    peg("cumplió treinta años", "franquicia", "Pokémon", dur=2.6, x=.78, y=.66, tam=420, giro=4),
    peg("Rojo Fuego y Verde Hoja llegaron", "c_rojofuego", "Rojo Fuego y Verde Hoja", dur=2.6, x=.20, y=.64, tam=430),
    peg("llegaron a Switch", "switch2", "Switch", dur=2.0, x=.47, y=.70, tam=260, giro=7),
    cartel("se anunció la décima generación", "GEN 10: 2027", None, dur=2.4, x=.72, y=.30),
    peg("volvemos al principio", "c_rojo_azul", "Rojo y Azul", dur=2.6, x=.24, y=.62, tam=480),
    mg_en(K.vida("GAME FREAK", None, .9, .05, "Dinero"), "casi arruina a sus creadores", 3.0, "vida game freak", x=.70, y=.30),
    mg_en(K.contador("Hoy", [(20, "secretos que seguramente ignoraste", "20")]), "los veinte secretos", 3.0, "contador 20", x=.66, y=.70),

    # ================================================================ HISTORIA h1
    zoom("Todo empieza con un niño", ("y los insectos desaparecieron", 0), 1.14),
    leg("tajiri_joven", "SATOSHI TAJIRI", ["Creció en las afueras de Tokio", "Cazaba insectos"], de="Satoshi Tajiri creció",
        a=("los charcos y los bosques", 0), x=.78, y=.50),
    cartel("atrapando bichos", "¡Un *bicho* salvaje!", None, dur=2.6, x=.30, y=.80),
    sello("la ciudad creció", "SIN BICHOS", dur=2.6, x=.66, y=.42),
    peg("los insectos desaparecieron", "tajiri", "Satoshi Tajiri", dur=2.6, x=.17, y=.64, tam=340),
    rel("Tajiri fundó Game Freak", "game_freak", "Game Freak", "Empezó como revista", dur=3.6, x=.76, y=.50, tam=460),
    ficha("una revista hecha a mano", "Game Freak", "Empezó como una *revista hecha a mano* sobre videojuegos.", "REVISTA / FANZINE",
          dur=3.6, x=.30, y=.28, ancho=780),
    cam("dibujante Ken Sugimori", "sugimori", "Ken Sugimori", dur=3.0, x=.84, y=.66, foco=(.5, .3, 1.4)),
    rel("vio el cable link", "cable_link", "Cable link", "Game Boy", dur=3.0, x=.24, y=.56, tam=440),
    mg("Se imaginó a sus bichos", ("de una pantalla a otra", .6), [], K.cable("Cable link"), "cable", x=.62, y=.30),
    peg("de una pantalla a otra", "game_boy", "Game Boy", dur=2.6, x=.16, y=.66, tam=300),
    peg("En Dragon Quest Dos", "c_dq2", "Dragon Quest II", dur=3.2, x=.80, y=.58, tam=360, giro=5),
    sello("no podías pasarle un objeto", "NO SE PODÍA", dur=2.2, x=.40, y=.36),
    cartel("Con ese cable, sí se podría", "¡Intercambio *completado*!", None, dur=2.4, x=.36, y=.82),

    # ================================================================ h2
    ficha("En 1990 le presentó", "1990", "Tajiri presenta el proyecto a *Nintendo*. Muchos no lo entienden.", "NINTENDO",
          dur=3.6, x=.74, y=.30, ancho=760),
    sil("Shigeru Miyamoto vio algo", "miyamoto", "Shigeru Miyamoto", "Vio algo", dur=4.6, lado="izq", alto=820),
    mg("hacer dos versiones", ("tenías que hablar con otros", .4), ["dos versiones", "Pokémon distintos"],
       K.dos_versiones("Dos versiones", ("ROJO", P("charmander"), "Unos Pokémon *solo aquí*"),
                       ("VERDE", P("bulbasaur"), "Y otros *solo aquí*")), "dos versiones", x=.62, y=.36),
    mg_en(K.cable("Para completarlo"), "no se acababa en tu Game Boy", 3.0, "cable 2", x=.40, y=.30),
    peg("Se iba a llamar Capsule Monsters", "capsule_portada", "Capsule Monsters", dur=3.6, x=.18, y=.60, tam=400),
    rel("monstruos de cápsula", "capsule_monsters", "Capsule Monsters", "El primer nombre", dur=2.6, x=.76, y=.52, tam=420),
    peg("serie Ultraseven", "ultraseven", "Ultraseven", dur=3.0, x=.78, y=.66, tam=380, giro=5),
    mg_en(K.mito("Capsule Monsters", "Quedó en *Pocket Monsters*", "El nombre", "REGISTRADO"), "el nombre estaba registrado", 4.2,
          "mito nombre", x=.38, y=.36),
    mg_en(K.contador("Desarrollo", [(6, "años de desarrollo", "6 AÑOS")]), "El desarrollo duró seis años", 2.6, "contador 6", x=.70, y=.30),
    mg_en(K.vida("SUELDOS", None, .6, 0.0, "Game Freak"), "ni para pagar los sueldos", 3.0, "vida sueldos", x=.30, y=.30),
    cartel("Cinco personas se fueron", "5 personas *se fueron*", None, dur=2.6, x=.66, y=.80),
    cam("Tajiri dejó de cobrar", "tajiri_2016", "Satoshi Tajiri", dur=3.2, x=.16, y=.66, foco=(.5, .3, 1.5)),
    peg("Lo salvó otra empresa, Creatures", "creatures", "Creatures", dur=3.6, x=.20, y=.62, tam=360),
    mg("a cambio de un tercio", ("derechos de Pokémon|fin", 1.0), ["Creatures", "un tercio", "derechos"],
       K.pastel([("Nintendo", K.AZUL), ("Game Freak", K.LUZ), ("Creatures", K.AMARILLO)], "Los derechos de Pokémon"), "pastel",
       x=.64, y=.40),

    # ================================================================ h3
    mg("Pocket Monsters Rojo y Verde salió", ("Más de treinta y un millones", 2.4), ["1996", "septiembre de 1998", "octubre de 1999"],
       K.linea_tiempo([("1996", "Japón: Rojo y Verde"), ("1998", "América: Rojo y Azul"), ("1999", "Europa")], "Así salió"),
       "linea salida", x=.5, y=.30),
    grande("ya tenía siete años", "game_boy", "Game Boy: 1989", dur=3.0, x=.80, tam=420),
    mg_en(K.contador("Ventas", [(10_000_000, "copias solo en Japón", "10 MILLONES")]), "diez millones de copias", 3.0,
          "contador 10m", x=.30, y=.72),
    mg_en(K.contador("Ventas", [(31_000_000, "copias en el mundo", "31 MILLONES")]), "treinta y un millones", 3.0,
          "contador 31m", x=.70, y=.72),
    aba([("bulbasaur", "Bulbasaur"), ("charmander", "Charmander"), ("squirtle", "Squirtle")], de="eliges a Bulbasaur",
        a=("ganar las ocho medallas", -.2), marcas=["Bulbasaur", "Charmander", "Squirtle"], nombre="iniciales", x=.68, y=.60, tam=300),
    mapa([P_PALETA + ("Pueblo Paleta",), (.20, .62), VERDE + ("Verde",), (.20, .36), PLATEADA + ("Plateada",), (.43, .16),
          CELESTE + ("Celeste",), (.60, .30), (.60, .45), CARMIN + ("Carmín",), (.50, .38), AZULONA + ("Azulona",), (.34, .55),
          FUCSIA + ("Fucsia",), (.62, .55), AZAFRAN + ("Azafrán",), (.40, .80), CANELA + ("Canela",), (.20, .80),
          VERDE + ("Verde",)], de="ganar las ocho medallas", a=("Ciento cincuenta y uno", -.1),
         marcas=["ganar", "las", "ocho", "medallas", "y", "llenar"], titulo="Kanto", sub="Ocho medallas"),
    peg("llenar la Pokédex", "pokedex", "Pokédex", dur=2.2, x=.80, y=.70, tam=320),
    mg_en(K.contador("La caja", [(151, "Pokémon, decía la caja", "151")]), "Ciento cincuenta y uno, decía", 3.0, "contador 151",
          x=.34, y=.32),
    sello("nunca fue del todo verdad", "¿151?", dur=2.4, x=.70, y=.40),

    # ================================================================ SECRETO 20
    *puesto("Número veinte", 20, "Te pusiste el nombre del creador"),
    hud("Número veinte", ("Un creador y su maestro|fin", 0), 20),
    mg("uno de los nombres que te proponía", ("En la versión Verde, los nombres iban al revés|fin", .3),
       ["Satoshi", "Shigeru", "En la versión Verde"], K.nombres(), "nombres", x=.62, y=.42),
    cam("Satoshi, por Satoshi Tajiri", "tajiri", "Satoshi Tajiri", dur=2.6, x=.15, y=.66),
    cam("Shigeru, por Shigeru Miyamoto", "miyamoto", "Shigeru Miyamoto", dur=2.6, x=.15, y=.66, foco=(.5, .3, 1.3)),
    peg("Ash se llama Satoshi", "ash", "Ash = Satoshi", dur=3.2, x=.20, y=.60, tam=380),
    peg("Gary se llama Shigeru", "gary", "Gary = Shigeru", dur=3.0, x=.80, y=.60, tam=380, giro=5),
    cartel("peleando en cada partida", "Creador *vs.* maestro", None, dur=2.4, x=.50, y=.82),

    # ================================================================ SECRETO 19
    *puesto("la oficina escondida", 19, "La oficina escondida"),
    hud("la oficina escondida", ("Para muchos fue el único premio|fin", 0), 19),
    mapa([AZULONA + ("Mansión Azulona", "meta", P("game_freak"))], de="En Ciudad Azulona", a=("Es Game Freak", -.1),
         marcas=["Azulona"], titulo="Ciudad Azulona", ventana=True, x=.72, y=.42),
    rel("Es Game Freak, los que hicieron", "game_freak", "Game Freak", "Último piso", dur=3.0, x=.22, y=.54, tam=420),
    mg("hablar con el programador", ("el diseñador del juego|fin", .4), ["programador", "grafista", "diseñador"],
       K.lista(["El *programador*", "El *grafista*", "El *diseñador*"], "Game Freak"), "lista oficina", x=.72, y=.40),
    cartel("te imprime un diploma", "¡*DIPLOMA*!", "Pokédex completa", dur=3.0, x=.30, y=.30),
    ficha("Para muchos fue el único premio", "Mansión Azulona", "Pokédex *completa* = un *diploma* impreso.", "ÚLTIMO PISO",
          dur=3.6, x=.68, y=.30, ancho=720),
    mg_en(K.contador("Horas", [(151, "Pokémon para el diploma", "151/151")]), "el único premio", 3.0, "contador diploma",
          x=.70, y=.72),

    # ================================================================ SECRETO 18
    *puesto("El primer Pokémon no fue Bulbasaur", 18, "El primer Pokémon no fue Bulbasaur"),
    hud("Número dieciocho", ("Rhydon al capturarlos|fin", 0), 18),
    peg("Bulbasaur es el número uno", "bulbasaur", "No.001", dur=2.6, x=.80, y=.62, tam=340),
    mg("otro número, uno interno", ("fue el primer Pokémon que se diseñó", 0), ["interno", "Rhydon"],
       K.indice(P("bulbasaur"), P("rhydon")), "indice", x=.60, y=.40),
    cam("Según Ken Sugimori, fue", "sugimori", "Ken Sugimori", dur=3.0, x=.15, y=.66, foco=(.5, .3, 1.4)),
    ficha("fue el primer Pokémon que se diseñó", "Rhydon", "Número interno *001*: el primer diseño de Sugimori.", "CÓDIGO INTERNO",
          dur=3.0, x=.32, y=.30, ancho=700),
    rel("Rhydon aparece por todas partes", "a_rhydon", "Rhydon", "El primero que se diseñó", dur=4.0, x=.74, y=.52, tam=480),
    peg("Muchos Pokémon con glitch", "missingno_rb", "Glitch", dur=2.6, x=.18, y=.62, tam=300, giro=7),

    # ================================================================ SECRETO 17
    *puesto("los treinta y nueve Pokémon que se borraron", 17, "Los 39 Pokémon que se borraron"),
    hud("los treinta y nueve Pokémon", ("todavía no existe|fin", 0), 17),
    cam("Según Shigeki Morimoto", "morimoto", "Shigeki Morimoto", dur=3.0, x=.15, y=.66, foco=(.5, .3, 1.4)),
    mg("iba a tener ciento noventa Pokémon", ("está en la posición ciento noventa", 1.4), ["ciento noventa", "Treinta y nueve", "Victreebel"],
       K.ranuras(P("victreebel")), "ranuras", x=.5, y=.44),
    peg("Victreebel, está", "victreebel", "Victreebel", dur=3.0, x=.17, y=.64, tam=340),
    mg_en(K.quien(P("raichu"), "¿GOROCHU?"), "Uno de los borrados era Gorochu", 4.0, "quien gorochu", x=.70, y=.46),
    peg("la evolución de Raichu", "raichu", "Raichu", dur=2.8, x=.20, y=.62, tam=320),
    sello("todavía no existe", "BORRADO", dur=2.2, x=.36, y=.32),

    # ================================================================ SECRETO 16
    *puesto("Pikachu empezó siendo un dulce", 16, "Pikachu empezó siendo un dulce"),
    hud("Pikachu empezó siendo", ("nadie lo ha confirmado del todo|fin", 0), 16),
    rel("Pikachu empezó siendo un dulce", "a_pikachu", "Pikachu", "No.025", dur=3.6, x=.76, y=.52, tam=470),
    sil("Lo dibujó Atsuko Nishida", "nishida", "Atsuko Nishida", "Game Freak", dur=4.0, lado="izq", alto=800),
    peg("un daifuku", "daifuku", "Daifuku", dur=3.6, x=.78, y=.62, tam=380, giro=5),
    mg("algo parecido a una ardilla", ("le dio la forma final", .6), ["ardilla", "obsesionada", "Sugimori"],
       K.lista(["*Daifuku*: un pastelito", "Una *ardilla*", "Forma final: *Sugimori*"], "Así nació Pikachu"), "lista pikachu",
       x=.66, y=.40),
    cam("Y Sugimori le dio la forma", "sugimori", "Ken Sugimori", dur=2.4, x=.15, y=.66, foco=(.5, .3, 1.4)),
    rel("la mascota iba a ser Clefairy", "a_clefairy", "Clefairy", "¿La mascota?", dur=3.6, x=.24, y=.54, tam=440),
    sello("nadie lo ha confirmado", "SIN CONFIRMAR", dur=2.6, x=.70, y=.40),

    # ================================================================ SECRETO 15
    *puesto("el camión más famoso", 15, "El camión más famoso"),
    hud("el camión más famoso", ("Una Galleta Lava|fin", 0), 15),
    mapa([CARMIN + ("Ciudad Carmín",), SS_ANNE + ("S.S. Anne", "meta", P("camion"))], de="Junto al barco S.S. Anne",
         a=("Solo se puede llegar", .4), marcas=["Carmín", "camión"], titulo="Ciudad Carmín", ventana=True, x=.72, y=.42),
    cartel("Solo se puede llegar a él con trucos", "Solo con *trucos*", None, dur=2.8, x=.30, y=.82),
    grande("en los patios nació el rumor", "camion", "El rumor", dur=3.6, x=.74, tam=520),
    mg("si usabas Fuerza en el camión", ("Debajo no había nada|fin", .4), ["Fuerza", "Era mentira"],
       K.mito("Si usabas *Fuerza* en el camión, debajo aparecía Mew.", "Debajo no había *nada*.", "El rumor del camión", "MENTIRA"),
       "mito camión", x=.34, y=.36),
    ficha("Pero el rumor fue tan grande", "Rojo Fuego y Verde Hoja", "Game Freak *escondió algo* debajo del camión.", "2004",
          dur=3.0, x=.64, y=.28, ancho=720),
    peg("en Rojo Fuego y Verde Hoja, Game Freak", "c_rojofuego", "Rojo Fuego", dur=3.0, x=.80, y=.62, tam=340, giro=5),
    rel("Una Galleta Lava", "galleta_lava", "Galleta Lava", "Debajo del camión", dur=3.4, x=.24, y=.54, tam=380),

    # ================================================================ SECRETO 14
    *puesto("El dragón que hacía trampa", 14, "El dragón que hacía trampa"),
    hud("El dragón que hacía trampa", ("nunca pudiste enseñárselo|fin", 0), 14),
    sil("Lance, el último del Alto Mando", "lance", "Lance", "Alto Mando", dur=4.0, lado="der", alto=860),
    peg("su Dragonite", "a_dragonite", "Dragonite", dur=2.6, x=.18, y=.62, tam=360),
    mg("Y ese Dragonite usa Barrera", ("Era el jefe", .2), ["Barrera", "no puede aprender"],
       K.ataques("DRAGONITE de Lance", ["AGILIDAD", "GOLPE", "BARRERA", "HIPERRAYO"], "BARRERA", P("dragonite")), "ataques",
       x=.40, y=.42),
    ficha("Tú, en cambio, nunca pudiste", "Barrera", "Ningún Dragonite *tuyo* podía aprenderla.", "MOVIMIENTO PROHIBIDO",
          dur=3.2, x=.34, y=.30, ancho=720),
    cartel("así que se lo permitieron", "Ventaja de *jefe*", None, dur=2.6, x=.70, y=.80),

    # ================================================================ SECRETO 13
    *puesto("el ataque que hacía justo lo contrario", 13, "El ataque que hacía lo contrario"),
    hud("el ataque que hacía justo", ("Era el juego|fin", 0), 13),
    mg("Foco Energía prometía", ("la dividía entre cuatro|fin", 1.0), ["golpe crítico", "error de programación", "entre cuatro"],
       K.foco(), "foco", x=.56, y=.40),
    mg("Los ataques con cien por ciento", ("doscientas cincuenta y seis|fin", 1.2), ["cien por ciento", "doscientas cincuenta"],
       K.uno_de_256(), "256", x=.70, y=.44),
    ficha("Así que si alguna vez fallaste", "Dos errores", "Foco Energía: crítico *÷ 4*. Precisión 100 %: falla *1 de 256*.",
          "ROJO Y AZUL", dur=3.4, x=.32, y=.30, ancho=760),
    cartel("no era mala suerte", "No era mala suerte: *era el juego*", None, dur=3.0, x=.40, y=.80, k=5),

    # ================================================================ SECRETO 12
    *puesto("Por qué los Pokémon psíquicos eran invencibles", 12, "Los psíquicos invencibles"),
    hud("Pokémon psíquicos eran invencibles", ("hasta la siguiente generación|fin", 0), 12),
    ficha("En Rojo y Azul, el tipo Psíquico", "Tipo Psíquico", "Casi *nada* le hacía daño de verdad.", "ROJO Y AZUL", dur=3.2,
          x=.32, y=.30, ancho=700),
    rel("el tipo Psíquico arrasaba", "alakazam", "Alakazam", "Tipo Psíquico", dur=3.2, x=.76, y=.52, tam=440),
    mg("El tipo Fantasma tenía que ser", ("único ataque Fantasma", 2.0), ["súper eficaz", "al revés", "Lengüetazo"],
       K.tabla_tipos(), "tabla tipos", x=.44, y=.40),
    peg("El tipo Fantasma", "gengar", "Gengar", dur=2.6, x=.82, y=.64, tam=320),
    peg("Lengüetazo", "gastly", "Lengüetazo", dur=2.6, x=.82, y=.66, tam=300, giro=6),
    aba([("alakazam", "Alakazam"), ("a_mewtwo", "Mewtwo")], de="Así que Alakazam y Mewtwo", a=("siguiente generación|fin", .2),
        marcas=["Alakazam", "Mewtwo"], nombre="psiquicos", x=.30, y=.60, tam=320),
    sello("reinaron sin rival", "SIN RIVAL", dur=2.0, x=.70, y=.36),

    # ================================================================ SECRETO 11
    *puesto("el combate contra el Profesor Oak", 11, "El combate contra el Profesor Oak"),
    hud("En el once, el combate", ("El jefe final que nunca fue|fin", 0), 11),
    sil("un entrenador que nunca llegas", "oak", "Profesor Oak", "Entrenador oculto", dur=4.2, lado="izq", alto=820),
    ficha("Dentro del juego hay un entrenador", "Profesor Oak", "Un entrenador *oculto* en el código. Nunca llegas a enfrentarlo.",
          "ENTRENADOR INÉDITO", dur=3.4, x=.70, y=.30, ancho=740),
    mg("Tauros, Exeggutor", ("Un equipo a la altura del campeón|fin", .3), ["Tauros", "Exeggutor", "Arcanine", "Gyarados", "inicial"],
       K.equipo([(P("tauros"), "TAUROS", 66), (P("exeggutor"), "EXEGGUTOR", 67), (P("arcanine"), "ARCANINE", 68),
                 (P("gyarados"), "GYARADOS", 70), (None, "TU RIVAL ELIGIÓ…", 69)], "Equipo del Prof. Oak"), "equipo oak",
       x=.66, y=.44),
    cartel("No tiene ni una línea de diálogo", "Sin *una línea* de diálogo", None, dur=2.8, x=.34, y=.80),
    sello("El jefe final que nunca fue", "INÉDITO", dur=2.2, x=.66, y=.40),

    # ================================================================ SECRETO 10
    *puesto("El Azul que jugaste", 10, "El Azul que jugaste no era el original"),
    hud("El Azul que jugaste", ("eran, por dentro, el Azul japonés|fin", 0), 10),
    mg("Hubo Rojo y Verde", ("el Azul japonés|fin", .3), ["Rojo y Verde", "octubre de 1996", "Rojo y tu Azul"],
       K.linea_tiempo([("FEB 1996", "Rojo y Verde (Japón)"), ("OCT 1996", "Azul por correo"), ("1998", "Rojo y Azul: base, el Azul")],
                      "Tres versiones"), "linea versiones", x=.5, y=.30),
    peg("con la revista CoroCoro", "corocoro", "CoroCoro", dur=3.0, x=.20, y=.66, tam=400),
    cartel("gráficos nuevos y errores corregidos", "Gráficos *nuevos*", "Errores corregidos", dur=3.0, x=.66, y=.80),
    peg("Tu Rojo y tu Azul eran", "c_rojo_azul", "Rojo y Azul", dur=3.0, x=.80, y=.64, tam=380, giro=5),

    # ================================================================ SECRETO 9
    *puesto("los Pokémon musculosos", 9, "Los Pokémon musculosos que casi tuviste"),
    hud("los Pokémon musculosos", ("sigue siendo redondito|fin", 0), 9),
    ficha("Traducir el juego fue tan difícil", "Traducción", "Hubo que *reprogramarlo* desde cero para América.", "1996-1998",
          dur=3.4, x=.32, y=.30, ancho=720),
    cartel("reprogramarlo desde cero", "Reprogramado *desde cero*", None, dur=3.0, x=.34, y=.80),
    sello("demasiado frágil para tocarlo", "FRÁGIL", dur=2.2, x=.70, y=.40),
    mg("Rediseñar a los Pokémon", ("sigue siendo redondito|fin", .3), ["Rediseñar", "dijo que no"],
       K.dos_versiones("La propuesta de América", ("Más músculo", None, "Pokémon *más fuertes* para América"),
                       ("Yamauchi", P("a_pikachu"), "Pikachu se queda *redondito*"), sello_b="NO"), "dos musculos", x=.56, y=.40),
    cam("Hiroshi Yamauchi, el presidente", "yamauchi", "Hiroshi Yamauchi", dur=3.4, x=.15, y=.66, foco=(.5, .3, 1.3)),

    # ================================================================ SECRETO 8
    *puesto("El Pokémon que cambió de color", 8, "El Pokémon que cambió de color"),
    hud("El Pokémon que cambió de color", ("consola virtual, también|fin", 0), 8),
    ficha("Jynx, el Pokémon de hielo", "Jynx", "Tipo *Hielo*, con forma *humana*.", "No.124", dur=3.0, x=.32, y=.30, ancho=640),
    rel("Jynx, el Pokémon de hielo", "jynx_rb", "Jynx", "Rojo y Azul, 1996", dur=3.6, x=.76, y=.50, tam=440),
    leg("weatherford", "ENSAYO, 2000", ["Carole Boston Weatherford", "Caricaturas racistas"], de="la escritora Carole Boston",
        a=("caricaturas racistas de antes|fin", .3), x=.24, y=.50),
    mg("Nintendo la repintó", ("consola virtual, también|fin", .2), ["repintó", "morada"],
       K.dos_versiones("Jynx", ("ANTES", P("jynx_rb"), "Rojo y Azul"), ("DESPUÉS", P("jynx_gs"), "Cara *morada*")), "jynx",
       x=.62, y=.40),
    peg("En Oro y Plata de América", "c_oro_plata", "Oro y Plata", dur=2.8, x=.18, y=.64, tam=360),
    peg("reediciones de Amarillo", "c_amarillo", "Amarillo", dur=2.6, x=.20, y=.66, tam=340, giro=5),

    # ================================================================ SECRETO 7
    *puesto("la leyenda de Pueblo Lavanda", 7, "La leyenda de Pueblo Lavanda"),
    hud("la leyenda de Pueblo Lavanda", ("sabes por qué la gente se la creyó|fin", 0), 7),
    mapa([LAVANDA + ("Pueblo Lavanda", "meta", P("lavanda_rby"))], de="En 2010 empezó a circular", a=("Que la música de Pueblo", .4),
         marcas=["Lavanda"], titulo="Pueblo Lavanda", ventana=True, x=.72, y=.42),
    mg("frecuencias que solo oían los niños", ("Todo era inventado|fin", 1.2), ["frecuencias", "Todo era inventado"],
       K.mito("Su música tenía *frecuencias* que solo oían los niños.", "Todo era *inventado*.", "La leyenda", "FALSO"),
       "mito lavanda", x=.36, y=.36),
    cartel("Es una creepypasta", "*Creepypasta*", "Terror escrito para internet", dur=3.4, x=.66, y=.80),
    sello("No hay ningún caso real", "0 CASOS", dur=2.2, x=.72, y=.38),
    peg("si alguna vez entraste en ese pueblo", "lavanda_rby", "Pueblo Lavanda", dur=3.0, x=.18, y=.62, tam=360),
    zoom("Esta es su música", ("Número seis", -.2), 1.16),          # 6 s del tema de Lavanda con la voz callada

    # ================================================================ SECRETO 6
    *puesto("Ditto es un Mew que salió mal", 6, "¿Ditto es un Mew que salió mal?"),
    hud("Ditto es un Mew que salió mal", ("tampoco lo ha negado|fin", 0), 6),
    ficha("Es una teoría de fans", "Teoría de fans", "¿Ditto, un *Mew* que salió mal? No es *oficial*.", "TEORÍA", dur=3.0,
          x=.32, y=.30, ancho=720),
    sello("Es una teoría de fans", "TEORÍA", dur=2.4, x=.70, y=.38),
    mg("Ditto y Mew comparten", ("aparecen Dittos salvajes|fin", .8), ["rosa", "Transformación", "Cueva Celeste"],
       K.pistas(P("a_ditto"), P("a_mew"), ["Mismo color *rosa*", "Los dos usan *Transformación*", "Dittos en la *Cueva Celeste*"]),
       "pistas", x=.5, y=.40),
    peg("la guarida de Mewtwo", "a_mewtwo", "Mewtwo", dur=2.6, x=.82, y=.66, tam=320, giro=5),
    rel("intentaron clonar a Mew", "a_ditto", "Ditto", "¿Un clon fallido?", dur=3.4, x=.24, y=.54, tam=420),
    cartel("Game Freak nunca lo ha dicho", "Ni *sí*… ni *no*", None, dur=3.0, x=.66, y=.80),

    # ================================================================ SECRETO 5
    *puesto("el Pokémon que podía borrarte la partida", 5, "El Pokémon que podía borrarte la partida"),
    hud("el Pokémon que podía borrarte", ("eso solo hizo que más gente lo buscara|fin", 0), 5),
    mapa([VERDE + ("Viejo de Verde",), (.20, .80), CANELA + ("Isla Canela",), (.31, .90, "Costa este", "meta",
          P("missingno_rb"))], de="Hablas con el viejo", a=("Ahí aparece una figura rota", 1.0),
         marcas=["viejo", "Isla Canela", "surfeas", "costa del este"], titulo="Kanto", sub="La ruta de MissingNo."),
    rel("una figura rota, hecha de cuadros", "missingno_rb", "MissingNo.", "Missing number", dur=4.0, x=.76, y=.50, tam=440),
    cartel("Un número que falta", "*Missing number*: número que falta", None, dur=3.0, x=.34, y=.80, k=5),
    mg("Y te hacía un regalo", ("Caramelos Raros o Bolas Maestras|fin", .3), ["regalo", "sexto lugar", "Miles de niños"],
       K.mochila([("POCIÓN", 3), ("ANTÍDOTO", 2), ("SUPERBALL", 5), ("REPELENTE", 4), ("CUERDA HUIDA", 1), ("CARAMELORARO", 2)]),
       "mochila", x=.66, y=.42),
    peg("cien Caramelos Raros", "rare_candy", "Caramelo Raro", dur=2.4, x=.16, y=.64, tam=280),
    peg("o Bolas Maestras", "masterball", "Bola Maestra", dur=2.4, x=.30, y=.68, tam=260, giro=6),
    grande("En mayo de 1999, Nintendo Power", "nintendo_power", "Nintendo Power, mayo 1999", dur=4.0, x=.26, tam=560),
    mg_en(K.vida("TU PARTIDA", ":L99", 1.0, 0.0, "Aviso"), "podía borrar tu partida", 3.0, "vida partida 2", x=.72, y=.30),
    sello("más gente lo buscara", "¡A BUSCARLO!", dur=2.4, x=.70, y=.66),

    # ================================================================ SECRETO 4
    *puesto("El rumor de Mew que resultó ser verdad", 4, "El rumor de Mew que resultó ser verdad"),
    hud("El rumor de Mew que resultó", ("Mew estuvo en tu cartucho desde el primer día|fin", 0), 4),
    ficha("Durante años, oficialmente", "Mew", "Oficialmente, solo en *eventos* de Nintendo.", "No.151", dur=3.2, x=.32, y=.30,
          ancho=680),
    rel("solo podías conseguir a Mew en un evento", "a_mew", "Mew", "Solo en eventos", dur=3.6, x=.76, y=.52, tam=440),
    mg_en(K.contador("Años", [(1996, "sale el juego", "1996"), (2003, "aparece el glitch", "2003")]), "pero en 2003", 3.6,
          "contador 2003", x=.30, y=.32),
    mg("un truco de dos entrenadores", ("en el momento justo|fin", .6), ["dos entrenadores", "huida"],
       K.lista(["Un entrenador con *vista larga*", "*Huir* en el momento justo", "Otro entrenador → ¡*MEW*!"], "El truco"),
       "lista truco", x=.66, y=.42),
    cartel("uno sí acabó siendo cierto", "¡Un *MEW* salvaje!", None, dur=3.0, x=.34, y=.80),
    sello("desde el primer día", "VERDAD", dur=2.4, x=.70, y=.38, ),

    # ================================================================ SECRETO 3
    *puesto("el concurso que salvó a Pokémon", 3, "El concurso que salvó a Pokémon"),
    hud("el concurso que salvó", ("dieron la vuelta para Pokémon|fin", 0), 3),
    mg_en(K.vida("FENÓMENO", None, .3, .45, "Primeros meses"), "Pokémon vendía, pero no era un fenómeno", 3.0, "vida fenomeno",
          x=.70, y=.30),
    peg("la revista CoroCoro anunció", "corocoro", "CoroCoro", dur=3.0, x=.20, y=.64, tam=420),
    mg_en(K.quien(P("a_mew"), "El Pokémon secreto", revela=True), "un Pokémon que no salía en el juego", 4.0, "quien mew",
          x=.72, y=.46),
    mg("Llegaron unas setenta y ocho mil cartas", ("Por veinte Mew|fin", 1.2), ["setenta y ocho mil", "veinte Mew"],
       K.cartas(P("a_mew")), "cartas", x=.5, y=.42),
    cam("Satoru Iwata, que luego fue", "iwata", "Satoru Iwata", dur=3.6, x=.15, y=.66, foco=(.5, .3, 1.4)),
    ficha("ese anuncio fue el momento", "Satoru Iwata", "Ese anuncio fue el momento en que las cosas *dieron la vuelta*.",
          "PRESIDENTE DE NINTENDO", dur=4.0, x=.70, y=.30, ancho=780),

    # ================================================================ SECRETO 2
    *puesto("El Pokémon que se coló en el cartucho", 2, "El Pokémon que se coló en el cartucho"),
    hud("El Pokémon que se coló", ("el Pokémon más buscado de la historia|fin", 0), 2),
    ficha("Mew no estaba en los planes", "Mew", "*No estaba* en los planes del juego.", "No.151", dur=3.0, x=.32, y=.30, ancho=640),
    sello("no tocaran ni un solo bit más", "NO TOCAR", dur=2.6, x=.70, y=.40),
    mg("al quitar las herramientas de depuración", ("casi como una broma|fin", .8), ["depuración", "trescientos bytes", "metió ahí a Mew"],
       K.bytes300(P("a_mew")), "bytes300", x=.5, y=.42),
    cam("según contó Shigeki Morimoto", "morimoto_2016", "Shigeki Morimoto", dur=3.0, x=.15, y=.66, foco=(.5, .3, 1.4)),
    sil("Ni siquiera Tsunekazu Ishihara", "ishihara", "Tsunekazu Ishihara", "Jefe del proyecto", dur=4.2, lado="der", alto=820),
    grande("esa travesura", "a_mew", "Mew: 300 bytes", dur=4.2, x=.27, tam=600),

    # ================================================================ SECRETO 1
    *puesto("El juego que casi no sale", 1, "El juego que casi no sale"),
    hud("El juego que casi no sale", ("decidió meterlos en una pantalla|fin", 0), 1),
    mg_en(K.vida("GAME FREAK", None, .4, .03, "Seis años"), "estuvo a punto de cerrar", 3.4, "vida cerrar", x=.70, y=.30),
    cartel("otros juegos por encargo", "Juegos *por encargo*", "Para pagar las facturas", dur=3.4, x=.34, y=.80),
    cartel("Cinco personas se fueron cuando", "5 personas *se fueron*", None, dur=2.6, x=.66, y=.80),
    leg("tajiri_2016", "SATOSHI TAJIRI", ["Sin sueldo", "Jornadas larguísimas", "Su padre le pagaba la comida"],
        de="Tajiri seguía trabajando", a=("pagándole la comida|fin", .4), x=.76, y=.50),
    peg("el Game Boy ya parecía", "game_boy", "Game Boy", dur=3.0, x=.18, y=.62, tam=360),
    sello("Nadie esperaba gran cosa", "SIN ESPERANZA", dur=2.4, x=.66, y=.40),
    rel("Hoy Pokémon es la franquicia", "franquicia", "Pokémon", "La franquicia que más ha ganado", dur=4.4, x=.74, y=.52, tam=500),
    mg_en(K.contador("Historia", [(1, "franquicia del entretenimiento", "N.º 1")]), "historia del entretenimiento", 3.0,
          "contador franquicia", x=.30, y=.32),
    peg("un niño que se quedó sin insectos", "tajiri_joven", "Satoshi Tajiri", dur=3.4, x=.20, y=.62, tam=340),
    cartel("meterlos en una pantalla", "Y los metió en una *pantalla*", None, dur=3.0, x=.62, y=.80),

    # ================================================================ CIERRE
    zoom("Treinta años después", ("Y como siempre", -.1), 1.10),
    peg("Rojo Fuego y Verde Hoja ya están en Switch", "c_rojofuego", "Ya en Switch", dur=3.0, x=.20, y=.62, tam=400),
    cartel("la décima generación llega en 2027", "GEN 10: *2027*", None, dur=2.6, x=.70, y=.80),
    com("leemos todos los comentarios", "Ugw2j_5-7ktR9uVpcxl4AaABAg", dur=4.8, x=.30, y=.32, tam=700),
    com("los tomamos en cuenta", "UgxdnznPHsijj-I2lE94AaABAg", dur=4.4, x=.70, y=.62, tam=700),
    com("Riuma nos contó", "Ugw_CCIkctKMyqDDO9l4AaABAg", dur=5.0, x=.30, y=.32, tam=760),
    rel("hoy también tocaba un primero", "c_rojo_azul", "El primer Pokémon", "1996", dur=3.6, x=.76, y=.56, tam=440),
    aba([("bulbasaur", "Bulbasaur"), ("charmander", "Charmander"), ("squirtle", "Squirtle"), ("a_pikachu", "Pikachu")],
        de="Cuál fue tu primer Pokémon", a=("Te leo abajo|fin", .3), marcas=["primer", "Pokémon", "MissingNo", "abajo"],
        nombre="primeros", x=.66, y=.58, tam=290),
    cartel("llegaste a encontrarte a MissingNo", "¿Te salió *MissingNo.*?", None, dur=2.6, x=.30, y=.30, k=5),
    cartel("suscríbete a Crónicas del gaming", "*SUSCRIBIRSE*", "Crónicas del gaming", dur=3.6, x=.50, y=.80),
    mg_en(K.exclama(), "Nos vemos en la siguiente", 1.6, "exclama fin", x=.50, y=.40),
]

# ================================================================ SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/pk_*.mp3
# `python bajar_sfx.py`: interfaz de Rojo/Azul (canal «Matteo», un video por sonido) + gritos cortados entre cambios de sprite.
SFX = {}
_PUESTOS = ["Número veinte", "En el diecinueve", "Número dieciocho", "En el diecisiete", "Número dieciséis", "En el quince",
            "Número catorce", "En el trece", "Número doce", "En el once", "Número diez", "En el nueve", "Número ocho", "En el siete",
            "Número seis", "En el cinco", "Número cuatro", "En el tres", "Número dos", "Y llegamos al número uno"]
_BOLA = ["pk_lanzar", "pk_intento", "pk_pokedex"]
PISTAS = [dict(sfx=_BOLA[i % 3], en=a, vol=.4) for i, a in enumerate(_PUESTOS)] + [
    dict(sfx="pk_start", en="Pokémon cumplió treinta años", vol=.4),
    dict(sfx="pk_pokedex2", en="llenar la Pokédex", vol=.35),
    dict(sfx="pk_puerta", en="En Ciudad Azulona, en el último piso", vol=.4),
    dict(sfx="pk_objeto", en="te imprime un diploma", vol=.45),
    dict(sfx="pk_grito_bulbasaur", en="Bulbasaur es el número uno", vol=.4),
    dict(sfx="pk_pc", en="dentro del código, cada Pokémon", vol=.35),
    dict(sfx="pk_grito_rhydon", en="el número uno de ese código es Rhydon", vol=.45),
    dict(sfx="pk_corte", en="Treinta y nueve se quedaron", vol=.4),
    dict(sfx="pk_grito_victreebel", en="Victreebel, está", vol=.4),
    dict(sfx="pk_grito_raichu", en="la evolución de Raichu", vol=.4),
    dict(sfx="pk_grito_pikachu", en="Pikachu empezó siendo un dulce", vol=.45),
    dict(sfx="pk_grito_clefairy", en="la mascota iba a ser Clefairy", vol=.4),
    dict(sfx="pk_barco", en="Junto al barco S.S. Anne", vol=.35),
    dict(sfx="pk_fuerza", en="si usabas Fuerza en el camión", vol=.45),
    dict(sfx="pk_error", en="Era mentira", vol=.4),
    dict(sfx="pk_objeto", en="Una Galleta Lava", vol=.45),
    dict(sfx="pk_grito_dragonite", en="saca al final a su Dragonite", vol=.45),
    dict(sfx="pk_fallo", en="podían fallar", vol=.4),
    dict(sfx="pk_grito_gengar", en="El tipo Fantasma tenía que ser", vol=.4),
    dict(sfx="pk_grito_gastly", en="Lengüetazo", vol=.4),
    dict(sfx="pk_grito_alakazam", en="Así que Alakazam y Mewtwo", vol=.4),
    dict(sfx="pk_grito_tauros", en="Tauros, Exeggutor", vol=.35),
    dict(sfx="pk_grito_gyarados", en="Arcanine y Gyarados", vol=.35),
    dict(sfx="pk_grito_jynx", en="Jynx, el Pokémon de hielo", vol=.4),
    dict(sfx="pk_teleport", en="Nintendo la repintó", vol=.35),
    dict(sfx="pk_error", en="Todo era inventado", vol=.4),
    dict(sfx="pk_grito_ditto", en="Ditto y Mew comparten", vol=.4),
    dict(sfx="pk_grito_mewtwo", en="la guarida de Mewtwo", vol=.4),
    dict(sfx="pk_vuelo", en="Vuelas a Isla Canela", vol=.4),
    dict(sfx="pk_nivel", en="cien Caramelos Raros", vol=.4),
    dict(sfx="pk_guardar", en="podía borrar tu partida", vol=.45),
    dict(sfx="pk_grito_mew", en="solo podías conseguir a Mew", vol=.4),
    dict(sfx="pk_huir", en="una huida en el momento justo", vol=.4),
    dict(sfx="pk_captura", en="uno sí acabó siendo cierto", vol=.45),
    dict(sfx="pk_compra", en="Llegaron unas setenta y ocho mil cartas", vol=.35),
    dict(sfx="pk_grito_mew", en="Y él metió ahí a Mew", vol=.4),
    dict(sfx="pk_pc_sale", en="Cinco personas se fueron", vol=.35),
    dict(sfx="pk_pokedex2", en="Hoy Pokémon es la franquicia", vol=.35),
    dict(sfx="pk_curar", en="Treinta años después, aquí seguimos", vol=.35),
]
