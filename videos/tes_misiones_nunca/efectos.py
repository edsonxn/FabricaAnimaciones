# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 15 misiones de Skyrim que NUNCA debes hacer» (SECUENCIA YT, Crónicas de Tamriel).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 16 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con datos del guion, arriba a la derecha.
- Pegatinas con la imagen REAL (wiki de Fandom) de cada personaje u objeto que se nombra; ~1 de cada 5 grande.
- 4 motion graphics NUEVOS de este guion (regla del 19-oct-2026), con retratos reales:
  sospechosos «El Carnicero de Ventalia» (12) · rehenes «Una vida por otra» (7, y vuelve en el 2 con Astrid tachada) ·
  cadena «La trampa de la Hermandad» (4 → 3) · balanza «La cuenta de Maro» (2).
  python fab.py tes_misiones_nunca fx --seco   tiempos      python fab.py tes_misiones_nunca fx hoja   previews/fx_NN.jpg (MÍRALA)
  python fab.py tes_misiones_nunca fx          audio/fx.wav
"""
import os

import mg_tes as T

CAMARA = {}
FUNDIDO = {}

_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")   # imágenes reales de la wiki de Fandom


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


REHENES = [(P("fultheim"), "El mercenario"), (P("alea"), "La madre"), (P("vasha"), "El khajiita"), (P("astrid"), "Astrid")]
CADENA = [("La boda", P("vittoria")), ("El Emperador viene", P("emperador")), ("La sopa envenenada", P("raiz_jarrin")),
          ("Era un doble", P("maro")), ("Alguien te vendió", P("astrid")), ("El santuario arde", P("armadura_hermandad"))]

FX = [
    # ---- avisos (uno por puesto)
    aviso("hoy van las quince misiones", "Top 15", "Misiones que nunca debes hacer", dur=4.5),
    aviso("Número quince", "Misión · número 15", "Las piedras de Barenziah"),
    aviso("En el catorce", "Misión · número 14", "El experimento de Arniel"),
    aviso("Número trece", "Misión · número 13", "La forja de Aetherium"),
    aviso("En el doce", "Misión · número 12", "Un asesino en Ventalia"),
    aviso("Número once", "Misión · número 11", "Envenenar una meadería"),
    aviso("En el diez", "Misión · número 10", "La cárcel de la que nadie sale"),
    aviso("Número nueve", "Misión · número 9", "Talar el árbol más antiguo"),
    aviso("En el ocho", "Misión · número 8", "Apagar un faro"),
    aviso("Número siete", "Misión · número 7", "La cabaña"),
    aviso("En el seis", "Misión · número 6", "El contrato más triste"),
    aviso("Número cinco", "Misión · número 5", "El escondite"),
    aviso("En el cuatro", "Misión · número 4", "La boda"),
    aviso("Número tres", "Misión · número 3", "Matar al Emperador"),
    aviso("Número dos", "Misión · número 2", "Destruir la Hermandad Oscura"),
    aviso("llegamos al número uno", "Misión · número 1", "El dragón del principio"),

    # ---- gancho
    grande("mates al único dragón", "paarthurnax", "Paarthurnax", dur=5.5, tam=700),

    # ---- 15 · piedras de Barenziah
    peg("recoges una gema rara de un cofre", "cofre", "Un cofre", dur=4.5),
    ficha("Encontrar las otras veintitrés", "Piedras de Barenziah", "*24* piedras por toda la provincia. Sin mapa, sin "
          "marcador, sin pistas.", origen="Misión", dur=7.0),
    peg("en ruinas llenas de falmer", "falmer", "Falmer", dur=3.6),
    peg("Vex, del Gremio de Ladrones", "vex", "Vex", dur=4.0),
    grande("a recuperar la corona", "corona_barenziah", "Corona de Barenziah", dur=5.0, tam=600),
    peg("salen tres fantasmas", "fantasma", "Tres fantasmas", dur=3.6),
    ficha("Una bendición permanente", "El premio", "Encuentras *más gemas* en los cofres.", origen="Corona de Barenziah", dur=5.0),
    peg("el juego te premia con más gemas", "gema", "Más gemas", dur=4.5, tam=320),

    # ---- 14 · el experimento de Arniel
    peg("vive un mago, Arniel Gane", "arniel", "Arniel Gane", dur=5.0),
    ficha("Primero te pide diez engranajes", "Engranajes dwemer", "Te pide *10.* Cada uno pesa *10.*", origen="Primer encargo",
          dur=6.5),
    peg("Cada uno pesa diez", "engranaje", "Engranaje dwemer", dur=4.5, tam=340),
    peg("una gema de alma deformada", "gema_deformada", "Gema de alma deformada", dur=4.5, tam=360),
    grande("Dentro hay una daga legendaria", "keening", "Afiladura", dur=5.0, tam=600),
    peg("un hechizo para invocar su fantasma", "sombra_arniel", "La sombra de Arniel", dur=5.0),

    # ---- 13 · la forja de Aetherium
    peg("un cristal rarísimo, el Aetherium", "fragmento_aetherium", "Aetherium", dur=4.5, tam=380),
    peg("la voz de Katria", "katria", "Katria", dur=5.5),
    peg("autómatas y rompecabezas", "centurion", "Autómatas dwemer", dur=4.0),
    peg("Una corona que te deja usar", "corona_aetherial", "La corona", dur=7.0, x=.13, y=.68, tam=300),
    peg("un escudo y un bastón", "escudo_aetherial", "El escudo", dur=5.2, x=.30, y=.68, tam=300),
    peg("y un bastón", "baston_aetherial", "El bastón", dur=4.8, x=.45, y=.68, tam=300),
    ficha("Una corona que te deja usar", "La corona", "Usa *dos* piedras guardianas a la vez.", origen="Forja de Aetherium",
          dur=5.0),
    ficha("Pero solo puedes forjar uno", "Solo uno", "El fragmento se consume. Las otras *dos* piezas se pierden para siempre.",
          origen="Forja de Aetherium", rojo=True, dur=6.0),

    # ---- 12 · Sangre en el hielo
    mg(T.sospechosos("El Carnicero de Ventalia", (P("amuleto_nigromante"), "El amuleto"), (P("wuunferth"), "Wuunferth"),
                     (P("calixto"), "Calixto")),
       ("y un amuleto", -.3), ("historia del amuleto|fin", .8),
       ["y un amuleto", "todo apunta a", "arrestan al mago", "hay otro cadáver", "el Carnicero era"], "carnicero"),
    ficha("es una misión famosa por sus errores", "Misión rota", "Si el siguiente asesinato no se dispara, se queda *colgada* "
          "para siempre.", origen="Sangre en el hielo", rojo=True, dur=7.0),

    # ---- 11 · Honningbrew
    grande("Maven, la dueña de media Riften", "maven", "Maven Black-Briar", dur=5.0, tam=620),
    peg("la meadería Honningbrew", "aguamiel_honningbrew", "Meadería Honningbrew", dur=4.5, tam=420),
    peg("te presentas ante Sabjorn", "sabjorn", "Sabjorn", dur=5.0),
    peg("el sótano de ratas", "skeever", "Ratas del sótano", dur=4.0, x=.40, tam=320),
    peg("le echas veneno a la cuba", "veneno", "Veneno", dur=4.5, tam=360),
    peg("en manos de Mallus", "mallus", "Mallus", dur=4.5),
    ficha("Tenía a Mallus trabajando gratis", "Sabjorn", "Tenía a Mallus atrapado en una *deuda* que no podía pagar.",
          origen="Tampoco era un santo", dur=6.5),

    # ---- 10 · Cidhna
    peg("un hombre llamado Eltrys", "eltrys", "Eltrys", dur=5.0),
    peg("la familia más rica de Markarth", "thonar", "Thonar Silver-Blood", dur=4.5),
    ficha("Te mandan a la mina de Cidhna", "Mina de Cidhna", "Para el resto de tus días.", origen="Markarth", rojo=True, dur=5.0),
    peg("Y entras sin nada", "harapos", "Lo que te dejan", dur=5.0, tam=340),
    peg("a cambio de skooma", "skooma", "Skooma", dur=4.0, tam=340),
    grande("llegar hasta el Rey Harapiento", "madanach", "Madanach, el Rey Harapiento", dur=5.0, tam=620),
    peg("picando piedra en ropa interior", "pico", "Pico", dur=4.0, tam=340),

    # ---- 9 · Eldergleam
    peg("hay un árbol sagrado", "gildergreen", "Gildergreen", dur=3.4, tam=440),
    peg("La sacerdotisa Danica", "danica", "Danica", dur=4.5),
    grande("el Eldergleam, un gigante", "eldergleam", "Eldergleam", dur=5.5, tam=680),
    peg("a una bruja cuervo", "cuervo_bruja", "Bruja cuervo", dur=4.0),
    ficha("la daga que hicieron para matar spriggans", "Nettlebane", "Hecha para matar *spriggans.*", origen="Daga", dur=5.0),
    peg("el peregrino que se te pegó", "maurice", "El peregrino", dur=5.0),
    grande("salen spriggans por todas partes", "spriggan", "Spriggans", dur=5.0, tam=620),

    # ---- 8 · el faro
    peg("un argoniano llamado Jaree-Ra", "jaree_ra", "Jaree-Ra", dur=5.0),
    grande("apagar el fuego del faro", "faro", "El faro de Soledad", dur=4.5, x=.27, tam=560),
    ficha("Un barco, el Icerunner", "Icerunner", "Sin la luz, se estrella contra las rocas.", origen="El barco", dur=5.5),
    peg("te espera Deeja", "deeja", "Deeja", dur=5.0),
    ficha("En su cuerpo encuentras una nota", "La nota", "Su hermano le pedía que te *matara* en cuanto llegaras.",
          origen="Deeja", rojo=True, dur=5.5),

    # ---- 7 · la cabaña
    peg("a un niño que quiere ver muerta", "aventus", "Aventus Aretino", dur=4.0, x=.13, tam=340),
    peg("la directora de su orfanato", "grelod", "Grelod", dur=3.6, x=.30, tam=340),
    ficha("una nota con dos palabras", "La nota", "*Lo sabemos.*", origen="Hermandad Oscura", rojo=True, dur=5.0),
    grande("con Astrid sentada encima", "astrid", "Astrid", dur=5.5, tam=640),
    mg(T.rehenes("Una vida por otra", REHENES, arriba=3, dudas=4),
       ("Uno de los tres tiene", -.2), ("hasta que alguien muera|fin", .6),
       ["Un mercenario", "una madre de seis", "y un khajiita", "Uno de los tres tiene", "que presume de ladrón"], "cabaña"),
    mg(T.rehenes("Una vida por otra", REHENES, arriba=3, dudas=4, tachar=[(0, 5)]),
       "Y lo peor viene después", ("de una puerta|fin", .6),
       ["Y lo peor viene después"] * 4 + ["El juego nunca te dice", "Matas a un desconocido"], "cabaña 2"),

    # ---- 6 · Narfi
    grande("vive Narfi, un mendigo", "narfi", "Narfi", dur=5.5, tam=620),
    peg("Nazir te lo encarga", "nazir", "Nazir", dur=4.5),
    peg("la encuentras en el fondo del río", "reyda", "Reyda", dur=4.5, tam=380),
    ficha("Si le mientes, se pone feliz", "Narfi", "Va a esperar a su hermana *hasta que vuelva.*", origen="Si le mientes",
          dur=5.5),

    # ---- 5 · Helgi
    peg("la casa de Hroggar", "hroggar", "Hroggar", dur=4.5),
    peg("una tal Alva", "alva", "Alva", dur=3.6, x=.34, tam=340),
    grande("aparece el fantasma de Helgi", "helgi", "Helgi", dur=5.5, tam=620),
    peg("Es Laelette, una vampira", "laelette", "Laelette", dur=5.0, tam=420),
    peg("ir a contárselo a su marido", "thonnir", "Su marido", dur=3.6),
    grande("La culpable de verdad era Alva", "alva", "Alva", dur=6.0, tam=620),

    # ---- 4 · la boda
    grande("se casa Vittoria Vici", "vittoria", "Vittoria Vici", dur=5.5, tam=620),
    peg("con un capa de la tormenta", "asgeir", "El novio", dur=4.0),
    peg("Babette, la vampira", "babette", "Babette", dur=5.0),
    mg(T.cadena("La trampa de la Hermandad", CADENA), ("Y todo esto", -.2), ("Era el cebo|fin", .6),
       ["Y todo esto", "que venir a Skyrim"], "cadena"),

    # ---- 3 · el Emperador
    peg("Te haces pasar por el Gourmet", "gourmet", "El Gourmet", dur=4.5),
    peg("La cocinera está tan emocionada", "gianna", "La cocinera", dur=3.8),
    mg(T.cadena("La trampa de la Hermandad", CADENA), ("Una raíz venenosa", -.3), ("bienvenida a la familia|fin", .8),
       [("Una raíz venenosa", -.3), ("Una raíz venenosa", -.3), "Una raíz venenosa", "era un doble", "Alguien de la Hermandad",
        "está ardiendo", "la traidora era"], "cadena 2"),
    grande("solo te pide una cosa", "emperador", "Titus Mede II", dur=5.0, tam=600),

    # ---- 2 · destruir la Hermandad
    mg(T.rehenes("Una vida por otra", REHENES, arriba=3, tachar=[(3, 4)]), "Vuelve a la cabaña", ("Parece lo correcto|fin", .3),
       ["Vuelve a la cabaña"] * 4 + [("puedes matar a", .3)], "cabaña 3"),
    peg("te mandan con el comandante Maro", "maro", "Comandante Maro", dur=4.5),
    mg(T.balanza("La cuenta de Maro", ("3 000 monedas", P("oro")),
                 [("Shadowmere", P("shadowmere")), ("20 000 monedas en contratos", P("oro")),
                  ("Maestros de Alquimia y Armadura ligera", P("babette")),
                  ("Armadura antigua de la Hermandad", P("armadura_hermandad")), ("Cicero", P("cicero"))],
                 remate=("3 000 monedas a cambio de todo eso", 6)),
       ("hasta que haces la cuenta", -.3), ("a cambio de todo eso|fin", 1.4),
       ["hasta que haces la cuenta", "no hay Shadowmere", "veinte mil monedas", "maestros de Alquimia", "la armadura antigua",
        "ni Cicero", "Tres mil monedas a cambio"], "balanza"),

    # ---- 1 · Paarthurnax
    grande("vive Paarthurnax, un dragón", "paarthurnax", "Paarthurnax", dur=5.5, tam=700),
    peg("lucha a tu lado contra Alduin", "alduin", "Alduin", dur=3.6, tam=420),
    peg("las Cuchillas, Delphine", "delphine", "Delphine", dur=5.5, x=.13, tam=340),
    peg("y Esbern", "esbern", "Esbern", dur=4.8, x=.30, tam=340),
    ficha("Y te dan un ultimátum", "Ultimátum", "Hasta que no lo mates, no hay *nada* de qué hablar.", origen="Las Cuchillas",
          rojo=True, dur=5.5),
    ficha("La recompensa? Ninguna", "La recompensa", "*Ninguna.* Solo lo que se le cae al dragón.", origen="Las Cuchillas",
          rojo=True, dur=6.0),
    peg("lo que se le cae al dragón", "escamas_dragon", "Escamas de dragón", dur=3.5, tam=380),
    grande("vuelves con Arngeir", "arngeir", "Arngeir", dur=6.0, tam=620),

    # ---- cierre
    ficha("en el canal tienes las ocho misiones", "Las 8 misiones daédricas PROHIBIDAS de Skyrim", "Ya está en el canal.",
          origen="Video recomendado", dur=6.0, x=.5, y=.40),
    peg("acuérdate del faro", "faro", "El faro", dur=4.5, tam=440),
]

SFX = {
    "mision_a": ("Deep nordic war drum hit with a short low horn swell, dark fantasy game quest notification", 3),
    "mision_b": ("Low ominous choir breath with a single deep drum hit, dark fantasy quest started sting", 3),
    "monedas": ("Handful of gold coins pouring into a leather pouch, medieval fantasy", 2),
    "sello": ("Heavy rubber stamp slammed hard on a wooden desk, single thud", 1),
    "cerrojo": ("Old heavy wooden door slammed shut and an iron bolt locked, dark cabin", 2),
    "cadena": ("Heavy iron chain link snapping and breaking, metallic clank", 2),
    "fuego": ("Large fire suddenly bursting into flames with a whoosh, burning wood", 3),
}
_AV = ["hoy van las quince misiones", "Número quince", "En el catorce", "Número trece", "En el doce", "Número once",
       "En el diez", "Número nueve", "En el ocho", "Número siete", "En el seis", "Número cinco", "En el cuatro", "Número tres",
       "Número dos", "llegamos al número uno"]
PISTAS = [dict(sfx="mision_a" if k % 2 == 0 else "mision_b", en=a, vol=.6 if k in (0, 15) else .5) for k, a in enumerate(_AV)] + [
    dict(sfx="sello", en="arrestan al mago", vol=.55),
    dict(sfx="sello", en=("el Carnicero era", .5), vol=.6),
    dict(sfx="cerrojo", en="La puerta está cerrada", vol=.5),
    dict(sfx="cadena", en="la traidora era", vol=.55),
    dict(sfx="fuego", en="está ardiendo", vol=.45),
    dict(sfx="monedas", en="Maro te paga tres mil monedas", vol=.45),
    dict(sfx="monedas", en="Tres mil monedas a cambio", vol=.4),
]
