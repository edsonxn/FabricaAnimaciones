# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Banjo-Tooie: su historia y los 10 secretos QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming, 19-oct-2026).
Fórmula de Warcraft/Tamriel/Runa (docs/estilo_secuencia_yt.md § PEGATINAS y § MOTION GRAPHICS NUEVOS) con el kit N64 nuevo
(nucleo/mg_gaming.py):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de banjokazooie.fandom.com en pegatinas/, fuentes en
  pegatinas/_fuentes.txt), chicas abajo a la izquierda, en fila cuando la voz enumera, ~1 de cada 5 GRANDE del lado contrario.
- rótulo `puesto` por secreto (arriba), fichas (cuadro de diálogo) a la derecha SOLO con datos del guion.
- MG nuevos de ESTE guion: dos líneas de tiempo (así se hizo / lo que vino después / el regreso de Bottles' Revenge), el Stop 'n'
  Swop (memoria que se vacía, Nintendo lo tacha, XBLA 2009), las familias Jinjo (1..9 = 45 + la gris) y el concurso de las pesas.
  python fab.py banjo_tooie fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py banjo_tooie fx         audio/fx.wav
"""
import os

import mg_gaming as G
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_FX, _FY = .74, .40     # fichas: a la derecha (el rótulo de puesto va arriba)

CAMARA = {}
FUNDIDO = {}


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=660):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(en, items, y=.66, tam=330, dur=5.0):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [peg(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None):
    d = dict(tipo="mg", fn=G.ficha(titulo, texto, tipo=tipo), en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, dur=3.6):
    return dict(tipo="mg", fn=G.puesto(num, titulo), en=en, dur=dur, x=.5, y=.16, sale=.45, nombre=f"puesto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


FX = [
    # ================================================================ GANCHO
    grande("Un fantasma con cuernos", "devil_bottles", "Bottles demonio", lado="der", dur=5.0),
    peg("se va a poder jugar de forma oficial", "evercade", "Evercade / 30 de octubre", tam=380),
    *fila("que mató a un personaje", [
        ("bottles", "Bottles", None),
        ("game_pak", "Cartuchos vivos", "que escondió cartuchos vivos"),
        ("grunty_cabeza", "Una promesa", "y que dejó una promesa")], dur=6.0),
    ficha("Así que hoy te cuento", "Banjo-Tooie", "Su historia, su lado oscuro y *10 secretos* que seguramente ignoraste.",
          tipo="Rare / Nintendo 64 / 2000", a=("que seguramente ignoraste|fin", 1.0)),

    # ================================================================ ORIGEN
    peg("el estudio británico Rare", "rare_logo", "Rare", tam=340),
    grande("en mil novecientos noventa y ocho, Banjo-Kazooie", "bk_1998", "Banjo-Kazooie (1998)", lado="der", dur=4.4),
    *fila("Un oso con pantalones cortos", [
        ("banjo", "Banjo", None),
        ("kazooie", "Kazooie", "una pájara gruñona")], dur=5.0),
    ficha("Gruntilda, aplastada bajo una roca", "Gruntilda",
          "Oso estúpido y Kazooie tonta, *¡volveré en Banjo-Tooie!*", tipo="Final de Banjo-Kazooie (1998)",
          a=("volvería en Banjo-Tooie|fin", 1.4)),
    peg("Mumbo te enseñaba fotos", "mumbo", "Mumbo Jumbo", tam=380),
    *fila("Huevos de colores y una llave de hielo", [
        ("huevo_azul", "Huevo azul", None),
        ("huevo_rosa", "Huevo rosa", None),
        ("ice_key", "Llave de hielo", "una llave de hielo")], dur=5.0),
    peg("Hasta el nombre era un chiste", "caja_bt", "Banjo-Tooie", tam=440, x=.80, y=.60),

    # ================================================================ DESARROLLO
    *fila("Al frente del diseño estaba Gregg Mayles", [
        ("mayles", "Gregg Mayles", None),
        ("kirkhope", "Grant Kirkhope", "y Grant Kirkhope otra vez")], dur=6.5, tam=300),
    ficha("Chris Sutherland contó", "Chris Sutherland", "Cuatro o cinco del equipo jugaban *GoldenEye* a la hora de la comida, "
          "*durante un par de años*.", tipo="Programador de Banjo-Tooie", a=("durante un par de años|fin", 1.2)),
    peg("agarrar a Kazooie del cuello", "kazooie", "Kazooie, munición incluida", tam=380),
    peg("conectados entre sí", "chuffy", "Chuffy, el tren entre mundos", tam=380, x=.80),
    peg("Grant Kirkhope tuvo el doble", "kirkhope", "Grant Kirkhope", tam=320),
    mg(G.linea_tiempo([("1998", "Empieza, justo cuando sale el primero"), ("1999", "La fecha prevista: no llega"),
                       ("2000", "Sale el 20 de noviembre")], "Así se hizo", w=1300, h=400),
       ("La idea de Rare era sacarlo", -.3), ("plataformas del año|fin", 1.0),
       ["La idea de Rare", ("La idea de Rare", .4), "finales de mil novecientos noventa y nueve", "Salió en Norteamérica"],
       "linea 1", y=.42),
    peg("Gregg Mayles publicó el fax", "mayles", "Gregg Mayles", tam=320),
    ficha("con una nota que decía splendid game", "El fax de Nintendo Japón",
          "Aprobación del juego, con una nota a mano: *Splendid game*, una carita y un pulgar arriba.",
          tipo="Lo que publicó Mayles / dic. 2025", a=("Era Miyamoto aplaudiendo", 0)),
    peg("Era Miyamoto aplaudiendo", "miyamoto", "Shigeru Miyamoto", tam=340, x=.17),
    ficha("Hasta que Mayles confesó", "La nota", "La escribió *él mismo*. Era una broma.", tipo="Lo que confesó después",
          dur=4.4),

    # ================================================================ LORE
    *fila("Banjo, Kazooie, Mumbo y Bottles", [
        ("banjo", "Banjo", None),
        ("kazooie", "Kazooie", "Kazooie, Mumbo"),
        ("mumbo", "Mumbo", "Mumbo y Bottles"),
        ("bottles", "Bottles", "Bottles, el topo")], dur=6.0, tam=300),
    *fila("Mingella y Blobbelda", [
        ("mingella", "Mingella", None),
        ("blobbelda", "Blobbelda", "y Blobbelda")], dur=4.2),
    grande("una perforadora gigante", "hag1", "Hag 1", lado="der", dur=4.0, tam=620),
    grande("solo un esqueleto con túnica", "gruntilda_bt", "Gruntilda, en esqueleto", dur=4.6, tam=640),
    dict(tipo="destello", en="la casa explota", dur=.5, fuerza=.9),
    dict(tipo="temblor", en="la casa explota", amp=14, dur=1.0),
    peg("arrastrarse fuera de los escombros", "bottles_bt", "El fantasma de Bottles", tam=420, dur=5.0),
    ficha("Gregg Mayles lo admitió", "Gregg Mayles", "Fue algo *deliberado*. No queríamos repetir el primer juego: "
          "*queríamos sorprender*.", tipo="Nintendo Life / 2020", a=("querían sorprender|fin", 1.2)),
    peg("una máquina, el B.O.B.", "bob", "B.O.B. (Big-O-Blaster)", tam=420),
    grande("King Jingaling, y lo dejan convertido en zombi", "jingaling", "King Jingaling", lado="der", dur=4.6),

    # ================================================================ 10 / SIN RIMAS
    puesto("Número diez.", 10, "La bruja que no rima"),
    peg("Gruntilda hablaba siempre en verso", "grunty_hag1", "Gruntilda", tam=420),
    *fila("Sus hermanas le pusieron una condición", [
        ("mingella", "Mingella", None),
        ("blobbelda", "Blobbelda", None)], dur=4.6),
    ficha("O dejaba las rimas", "El trato de las hermanas", "O dejas *las rimas*, o no hay *cuerpo nuevo*.",
          tipo="La condición para ayudarla", a=("Les ponía de los nervios|fin", 1.0)),
    grande("No volvió a rimar hasta Nuts and Bolts", "grunty_nb", "Gruntilda en Nuts & Bolts", lado="der", dur=4.6),

    # ================================================================ 9 / CÓDIGOS AL REVÉS
    puesto("En el nueve, los trucos.", 9, "Códigos al revés"),
    grande("La bruja se vengó de Cheato", "cheato", "Cheato", dur=5.0, tam=560),
    peg("pisando letras en una sala", "code_chamber", "La sala de códigos", tam=460, x=.80, y=.62),
    ficha("si escribes primero la palabra cheato", "El truco del truco", "*CHEATO* + el código al revés. "
          "Para EGGS: *CHEATOSGGE*.", tipo="Templo de Mayahem", a=("el código al revés|fin", 2.0)),
    peg("detrás del templo de Jiggywiggy", "jiggywiggy", "Master Jiggywiggy", tam=400),
    ficha("un contenedor de huevos, seguido de Jingaling", "El cartel", "Un contenedor de huevos, seguido de Jingaling.",
          tipo="Detrás del templo", a=("Nido y rey|fin", .3)),
    ficha("Nestking, y tienes", "NESTKING", "Huevos y plumas *infinitos*.", tipo="Código", dur=4.0),

    # ================================================================ 8 / CARTUCHOS VIVOS
    puesto("Número ocho, y este es", 8, "Los cartuchos vivos"),
    grande("Son cartuchos de Banjo-Kazooie", "game_pak", "Banjo-Kazooie Game Pak", lado="der", dur=6.0, tam=640),
    *fila("Dos huevos de colores y una llave de hielo", [
        ("huevo_azul", "Huevo azul", None),
        ("huevo_rosa", "Huevo rosa", None),
        ("ice_key", "Llave de hielo", "una llave de hielo#2")], dur=5.0),
    peg("los de Rare metieron el cartucho", "game_pak", "El cartucho, dentro del juego", tam=420, x=.80, y=.60),

    # ================================================================ 7 / LA FAMILIA GRIS
    puesto("En el siete, una tragedia", 7, "La familia gris"),
    mg(G.jinjos("Las familias Jinjo"), ("hay cuarenta y cinco Jinjos", -.3), ("los grises eran diez|fin", 1.2),
       ["La blanca tiene", "la naranja dos", "la amarilla tres", "y así hasta", ("y así hasta", .25), ("y así hasta", .5),
        ("y así hasta", .75), ("y así hasta", 1.0), "la negra, que tiene", "Es la de la familia gris"], "jinjos", y=.52),
    grande("dentro de los datos del juego", "casa_gris_oculta", "La casa gris, intacta", lado="der", dur=5.6, tam=560),
    peg("con una etiqueta que dice", "grey_jinjo", "Jinjo gris", tam=380),

    # ================================================================ 6 / KAZOOIE DRAGÓN
    puesto("Número seis. Kazooie puede", 6, "Kazooie dragón"),
    grande("Kazooie puede convertirse en dragón", "dragon_kazooie", "Dragon Kazooie", lado="der", dur=4.4),
    peg("Primero necesitas la llave de hielo", "ice_key", "Llave de hielo", tam=340),
    peg("Dentro está el Mega-Glowbo", "mega_glowbo", "Mega-Glowbo", tam=400),
    peg("Humba Wumba, la chamana", "humba", "Humba Wumba", tam=420, x=.80, y=.60),
    *fila("Un premio enorme", [
        ("ice_key", "1 / Llave", None),
        ("mega_glowbo", "2 / Mega-Glowbo", None),
        ("humba", "3 / Humba", None),
        ("dragon_kazooie", "4 / Dragón", None)], dur=6.0, tam=300),

    # ================================================================ 5 / EL MUNDO A MEDIAS
    puesto("En el cinco, el mundo", 5, "El mundo a medias"),
    ficha("Banjo-Kazooie tenía cien Jiggies", "Jiggies", "Banjo-Kazooie: *100* / Banjo-Tooie: *90*",
          tipo="Las piezas de puzle", a=("tienen explicación|fin", 1.0)),
    peg("Banjo-Kazooie tenía cien Jiggies", "jiggy", "Jiggy", tam=340),
    grande("Cauldron Keep, el castillo de las brujas", "cauldron_keep", "Cauldron Keep", dur=5.0, tam=620),
    *fila("Una última pelea con Klungo", [
        ("klungo", "Klungo", None),
        ("tower", "El concurso", "un concurso"),
        ("grunty_hag1", "El combate final", "y el combate final")], dur=5.0),

    # ================================================================ 4 / EL CONCURSO
    puesto("Número cuatro. El concurso", 4, "El concurso de la muerte"),
    grande("el Tower of Tragedy", "tower", "Tower of Tragedy", lado="der", dur=5.0, tam=620),
    mg(G.concurso(("Banjo y Kazooie", "Mingella", "Blobbelda"), "Tower of Tragedy"),
       ("Sobre cada concursante", -.3), ("debajo de la roca|fin", 1.0),
       ["Sobre cada concursante", "a Mingella", "y a Blobbelda"], "concurso", y=.52),
    grande("el icono de un Bottles con cuernos", "devil_bottles", "Bottles demonio", lado="der", dur=5.0, tam=560),

    # ================================================================ 3 / BANJO-THREEIE
    puesto("En el tres, la promesa", 3, "Banjo-Threeie"),
    grande("a Gruntilda solo le queda la cabeza", "grunty_cabeza", "La cabeza de Gruntilda", dur=6.0, tam=620),
    mg(G.linea_tiempo([("2002", "Microsoft compra Rare"), ("2008", "Nuts & Bolts, en Xbox"),
                       ("2019", "Banjo llega a Smash"), ("2024", "Banjo-Tooie en Switch Online")],
                      "Lo que vino después", w=1500, h=380, rojo_ultimo=False),
       ("En dos mil dos, Microsoft", -.3), ("a Nintendo Switch Online|fin", 1.2),
       ["En dos mil dos, Microsoft", "Microsoft compró Rare", "Fue Nuts and Bolts", "en dos mil diecinueve",
        "en octubre de dos mil veinticuatro"], "linea 2", y=.30),
    peg("Fue Nuts and Bolts", "caja_nb", "Nuts & Bolts (2008)", tam=420),
    peg("una cabeza metida en un cuerpo de robot", "grunty_nb", "Gruntilda robot", tam=420, x=.80, y=.66),
    peg("como luchador de Super Smash Bros.", "smash", "Banjo en Smash", tam=460),

    # ================================================================ 2 / STOP 'N' SWOP
    puesto("Número dos. El misterio", 2, "Stop 'n' Swop"),
    mg(G.swop("Stop 'n' Swop"), ("Encendías Banjo-Kazooie", -.3), ("El truco podía dejar de funcionar|fin", 1.0),
       ["Encendías Banjo-Kazooie", "apagabas la consola", "el cartucho de Banjo-Tooie", "Pero Nintendo le pidió"],
       "swop", y=.50),
    peg("el Rare Witch Project", "huevo_amarillo", "Los huevos escondidos", tam=380),
    peg("metidos en esos cartuchos vivos", "game_pak", "Banjo-Kazooie Game Pak", tam=400, x=.80, y=.62),
    mg(G.swop("Stop 'n' Swop"), ("Stop 'n' Swop funcionó por fin", -.2), ("sin tener que cambiar de cartucho|fin", 1.2),
       ["Stop 'n' Swop funcionó"] * 2 + [("Stop 'n' Swop funcionó", .1), ("Stop 'n' Swop funcionó", .2), "en dos mil nueve"],
       "swop 2009", y=.50),

    # ================================================================ 1 / BOTTLES' REVENGE
    puesto("Y llegamos al número uno.", 1, "Bottles' Revenge"),
    peg("Recuerdas que Bottles muere", "bottles", "Bottles", tam=400),
    grande("Bottles se vuelve un demonio con cuernos", "devil_bottles", "Bottles demonio", lado="der", dur=6.0, tam=640),
    ficha("Si tu amigo te gana", "Bottles' Revenge", "Si el enemigo poseído *te gana*, se cambian los papeles: "
          "*él es Banjo y tú, el demonio*.", tipo="Modo cortado / 2 jugadores", a=("tú eres el demonio|fin", 1.4)),
    peg("Old King Coal, el rey de carbón", "old_king_coal", "Old King Coal", tam=420),
    mg(G.linea_tiempo([("2000", "Se corta, pero se queda en el cartucho"), ("2026", "Evercade: 30 de octubre")],
                      "El regreso de Bottles", w=1100, h=380),
       ("Y ahora viene lo bueno", -.2), ("Bottles' Revenge#2|fin", 1.6),
       ["Y ahora viene lo bueno", ("Y ahora viene lo bueno", .3), "sale el Banjo-Kazooie Double Pack"], "linea 3", y=.30),
    peg("para Evercade, hecho junto a Rare", "evercade", "Evercade", tam=420),
    peg("va a ser Kazooie", "kazooie", "Kazooie", tam=420, x=.80, y=.62),

    # ================================================================ CIERRE
    *fila("Un fantasma vengativo", [
        ("devil_bottles", "Bottles demonio", None),
        ("tower", "El concurso", "un concurso con pesas"),
        ("grey_jinjo", "La familia gris", "una familia que nadie vio"),
        ("game_pak", "Cartuchos vivos", "unos cartuchos que corren")], dur=7.0, tam=300),
    grande("la última Navidad en la que Banjo", "caja_bt", "Banjo-Tooie (2000)", lado="der", dur=5.0, tam=600),
    peg("Kazooie convertida en dragón", "dragon_kazooie", "Dragon Kazooie", tam=400),
    peg("Banjo-Kazooie, el primero", "bk_1998", "Banjo-Kazooie", tam=400),
]
ROTULOS = []
SFX = {   # uno distinto por momento (regla: nada de SFX repetidos)
    "explosion": ("Cartoon house exploding in a magic blast, wooden debris, rumble, whimsical 90s platformer", 3),
    "pesa1": ("Heavy cartoon one-ton weight dropping with a whistle then a big comedic crash and dust", 3),
    "pesa2": ("Giant iron weight slamming onto a wooden stage, deep thud and wood creak, cartoon", 3),
    "cartucho": ("Cartoon boing boing hopping footsteps of a small living box, playful", 3),
    "dragon": ("Magical transformation sparkle swirl ending in a small fiery dragon roar, whimsical", 3),
    "fantasma": ("Ghostly cartoon mole laugh turning devilish with a spooky echo, playful horror", 3),
    "apagado": ("Old game console power switch clicking off with a fading electronic hum", 3),
}
PISTAS = [
    dict(sfx="explosion", en="la casa explota", vol=.5),
    dict(sfx="pesa1", en="a Mingella", vol=.5),
    dict(sfx="pesa2", en="y a Blobbelda", vol=.5),
    dict(sfx="cartucho", en="que van dando saltitos", vol=.4),
    dict(sfx="dragon", en="Kazooie sale convertida en dragón", vol=.45),
    dict(sfx="fantasma", en="Bottles se vuelve un demonio", vol=.45),
    dict(sfx="apagado", en="apagabas la consola", vol=.45),
]
