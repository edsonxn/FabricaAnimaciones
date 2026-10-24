# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 15 armas más PODEROSAS de Skyrim» (SECUENCIA YT, Crónicas de Tamriel, 23-oct-2026).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 16 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con cifras del guion (UESP), arriba a la derecha.
- Pegatinas con la imagen REAL (wiki de Fandom / UESP) de cada arma, personaje u objeto que se nombra; las armas, GRANDES.
- MG NUEVOS de este guion (regla del 19-oct-2026): ruleta «La ruleta del Wabbajack» (14) · niveles «La trampa del nivel»
  (Ruiseñor 6 y Azote 4) · golpes «¿Cuántos golpes para un dragón ancestral?» (4) · barras «Una sola puñalada» (1). Del kit:
  traiciones (Hoja de ébano 10 → 30, 9), rejilla (26 de 100, parálisis de la Desgarradora, 3), receta (la daga, 1).
- 6 mapas reales (tema tes) con FOTO de lo que se nombra: el Katariah (15), Laberintia (8), Monte Kilkreath (7), ruta del
  Azote (4), Riften (3), Cueva de Sima Negra (2) y la ruta del forjador (1).
  python fab.py tes_armas_poderosas fx --seco   tiempos      python fab.py tes_armas_poderosas fx hoja   previews/fx_NN.jpg (MÍRALA)
"""
import os

import mg_tes as T

CAMARA = {"scene-026": dict(a=(1, 0, 0), b=(1.15, 0, -.1))}   # cielo nocturno casi quieto: acercamiento lento
FUNDIDO = {}

_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")   # imágenes reales de la wiki
_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas")
TEMA_MAPA = "tes"

FUEGO, ESCARCHA, RAYO, VERDE = (255, 150, 90), (150, 200, 255), (200, 180, 255), (140, 220, 140)


def P(slug):
    return os.path.join(_PEG, slug + ".png")


def ficha(en, nombre, efecto, origen=None, dur=5.0, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    """Pegatina con la imagen REAL de lo que nombra la voz (regla de canal): abajo a la izquierda."""
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.25, tam=640):
    """Pegatina GRANDE (media pantalla): el arma de cada puesto y los personajes clave."""
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


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


# ---- datos de los MG nuevos (solo cifras del guion / investigacion.md)
RULETA = [("Fuego", FUEGO), ("Escarcha", ESCARCHA), ("Rayos", RAYO), ("Robar vida", T.SANGRE), ("Muerte", T.SANGRE),
          ("Pollo", T.HUESO), ("Cangrejo", T.HUESO), ("Queso", T.HUESO), ("Bollo dulce", T.ORO), ("Curar", VERDE),
          ("Invisible", T.GRIS)]
RUISENOR = [("1-18", 5), ("19-26", 10), ("27-35", 15), ("36-45", 25), ("46+", 25)]
AZOTE = [("1-18", 20), ("19-26", 25), ("27-35", 20), ("36-45", 35), ("46+", 40)]
DAGA = [(P("hueso_dragon"), "Hueso de dragón"), (P("tiras_cuero"), "Tiras de cuero")]


def _punalada():
    return T.barras("Una sola puñalada", [(P("desgarradora"), "Desgarradora gélida", 900, 1, T.HUESO),
                                          (P("daga_hueso"), "Daga de hueso de dragón", 1980, 0, T.ORO),
                                          (P("daga_hueso"), "La misma, con el bucle", 7650, 3, T.SANGRE)],
                    refs=[("Dragón anciano", 2255, 2), ("Dragón legendario", 4163, 3)], remate=("Dragón a dragón", 4))


def _ruleta():
    return T.ruleta("La ruleta del Wabbajack", RULETA, [0, 3, 4, 5, 6, 7, 8, 9, 10])


FX = [
    # ---- avisos (uno por puesto)
    aviso("hoy van las quince armas", "Top 15", "Las armas más poderosas de Skyrim", dur=4.5),
    aviso("Número quince", "Arma · número 15", "Viento Cortante"),
    aviso("En el catorce", "Arma · número 14", "Wabbajack"),
    aviso("Número trece", "Arma · número 13", "Espada de Sangreskal"),
    aviso("En el doce", "Arma · número 12", "Maza de Molag Bal"),
    aviso("Número once", "Arma · número 11", "Hacha rúnica de la Guardia del Alba"),
    aviso("En el diez", "Arma · número 10", "Volendrung"),
    aviso("Número nueve", "Arma · número 9", "Hoja de ébano"),
    aviso("En el ocho", "Arma · número 8", "Bastón de Magnus"),
    aviso("Número siete", "Arma · número 7", "Quebrantadora del amanecer"),
    aviso("En el seis", "Arma · número 6", "Hoja de Ruiseñor"),
    aviso("Número cinco", "Arma · número 5", "Espada de Miraak"),
    aviso("En el cuatro", "Arma · número 4", "Azote de dragones"),
    aviso("Número tres", "Arma · número 3", "Desgarradora gélida"),
    aviso("Número dos", "Arma · número 2", "Arco de Auriel"),
    aviso("llegamos al número uno", "Arma · número 1", "La que forjas tú", dur=4.0),

    # ---- gancho
    peg("Espadas que paralizan", "desgarradora", "", dur=1.8, x=.14, tam=340),
    peg("martillos que te roban", "volendrung", "", dur=1.8, x=.31, tam=340),
    peg("arcos que hacen llover", "arco_auriel", "", dur=2.4, x=.48, tam=340),

    # ---- 15 · Viento Cortante
    grande("Es una cimitarra", "windshear", "Viento Cortante", dur=3.4, x=.25, tam=560),
    mapa("skyrim", [(.33, .205, "Soledad", "inicio"), (.355, .17), (.38, .135, "El Katariah", "meta", P("katariah"))],
         de="clavada en la proa", a=("frente a la costa de Soledad|fin", .8), marcas=["clavada en la proa", "Katariah"],
         titulo="Skyrim", ventana=True),
    peg("del emperador Titus Mede", "titus", "Titus Mede II", dur=4.0, x=.17),
    ficha("Sobre el papel su encantamiento", "Viento Cortante", "El golpe con la empuñadura *a veces* derriba.",
          origen="Encantamiento", dur=7.0),
    ficha("Pero por un error", "Error", "Tambaleo en *cada* golpe. Normal o potente.", origen="Viento Cortante", rojo=True,
          dur=8.0),
    ficha("Cuarenta monedas", "Viento Cortante", "Valor: *40* monedas.", origen="Arma única", dur=5.0),

    # ---- 14 · Wabbajack
    grande("Es el bastón de Sheogorath", "wabbajack", "Wabbajack", dur=4.5, x=.75, tam=600),
    peg("el príncipe de la locura", "sheogorath", "Sheogorath", dur=4.5, x=.17),
    mg(_ruleta(), ("Puede lanzar fuego", -.3), ("la ruleta juega en tu contra|fin", .8),
       ["Puede lanzar fuego", "Puede robarle", "puede matarlo", "en un pollo", "cangrejo del barro", "queso de cabra",
        "en un bollo dulce", "puede curarlo", "volverlo invisible"], "ruleta"),
    ficha("Su daño elemental", "Wabbajack", "*60* de daño elemental. No lo reduce *nada.*", origen="El secreto", dur=8.0),
    peg("convertido en bollo dulce", "bollo", "Bollo dulce", dur=4.5, x=.17, tam=380),

    # ---- 13 · Espada de Sangreskal
    grande("Está en Solstheim", "sangreskal", "Espada de Sangreskal", dur=5.0, x=.25, tam=600),
    peg("en el cadáver de Graciano", "graciano", "Graciano Cerelio", dur=3.5, x=.75, y=.55, tam=420),
    peg("un sacerdote dragón Zahkriisos", "zahkriisos", "Zahkriisos", dur=4.0, x=.17),
    ficha("Lanza una onda", "Espada de Sangreskal", "Cada ataque potente lanza una onda de *30* de daño.",
          origen="Mandoble · 21 de daño", dur=8.0),
    ficha("hay una segunda Espada", "Secreto", "Una *segunda* espada detrás del muro de palabras.", origen="Túmulo de Sangreskal",
          dur=7.0),

    # ---- 12 · Maza de Molag Bal
    peg("una casa abandonada", "casa_abandonada", "Casa abandonada · Markarth", dur=4.5, x=.25, y=.55, tam=520),
    peg("Es Molag Bal", "molag_bal", "Molag Bal", dur=4.0, x=.75, y=.55, tam=440),
    peg("un seguidor de Boethiah Logrolf", "logrolf", "Logrolf", dur=4.0, x=.17),
    grande("La recompensa es una maza", "maza_molag", "Maza de Molag Bal", dur=5.0, x=.25, tam=560),
    ficha("La recompensa es una maza", "Maza de Molag Bal", "*-25* de aguante y *-25* de magia por golpe. Atrapa almas.",
          origen="Maza · 16 de daño", dur=9.0),
    ficha("Por una etiqueta mal puesta", "Error", "Su daño al aguante cuenta como *fuego.* Llamas aumentadas: *25 → 37.*",
          origen="Maza de Molag Bal", rojo=True, dur=10.0),

    # ---- 11 · Hacha rúnica
    peg("Florencio Baenio", "florencio", "Florencio Baenio", dur=4.5, x=.17),
    grande("Una de las recompensas", "hacha_runica", "Hacha rúnica", dur=5.0, x=.75, tam=560),
    mg(T.contadores("Hacha rúnica de la Guardia del Alba", [("No muertos matados", 100, 0, 1), ("Daño solar extra", 100, 0, 1)],
                    remate=("En área", 2)),
       ("Pero cada diez no muertos", -.2), ("Un solo golpe limpia una tumba|fin", .6),
       ["Pero cada diez no muertos", "Hasta cien", "Y en área"], "contadores hacha"),
    ficha("rompe al instante", "Hacha rúnica", "Rompe *al instante* cualquier barrera mágica.", origen="Guardia del Alba", dur=5.0),
    ficha("debía reiniciarse cada día", "Error", "El contador *nunca* se reinicia.", origen="Hacha rúnica", rojo=True, dur=7.0),

    # ---- 10 · Volendrung
    peg("el príncipe de los parias", "malacath", "Malacath", dur=4.0, x=.17),
    peg("los orcos de Largashbur", "largashbur", "Largashbur", dur=4.5, x=.75, y=.55, tam=520),
    peg("Matas al gigante", "gigante", "El gigante", dur=3.5, x=.17, tam=380),
    grande("lo convierte en Volendrung", "volendrung", "Volendrung", dur=5.0, x=.25, tam=600),
    ficha("Veinticinco de daño", "Volendrung", "*25* de daño. Absorbe *50* de aguante por golpe.", origen="Martillo de guerra",
          dur=7.0),
    ficha("Todos los martillos de guerra", "Velocidad", "Martillos de guerra: *0,6.* Volendrung: *0,7.*", origen="Volendrung",
          dur=9.0),

    # ---- 9 · Hoja de ébano
    peg("Nelkir el hijo del jarl", "nelkir", "Nelkir", dur=4.5, x=.17),
    grande("Detrás está la Hoja de ébano", "hoja_ebano", "Hoja de ébano", dur=5.0, x=.75, tam=600),
    mg(T.traiciones("Hoja de ébano", n=10, ini=10, paso=4, cada=2, etiqueta="Absorber salud"),
       ("Empieza siendo poca cosa", -.2), ("Nunca se gasta|fin", .6),
       ["Empieza siendo poca cosa", "cada vez que matas a dos amigos", "Diez traiciones después"], "traiciones"),
    ficha("Por un error aunque la empuñas", "Error", "A dos manos, pero cuenta como espada *a una mano.*", origen="Hoja de ébano",
          rojo=True, dur=7.0),

    # ---- 8 · Bastón de Magnus
    mapa("skyrim", [(.73, .225, "Colegio de Hibernalia", "inicio"), (.62, .27), (.52, .33),
                    (.455, .395, "Laberintia", "peligro", P("morokei"))],
         de="te mandan a buscarlo", a=("uno de los jefes más duros del juego|fin", .6),
         marcas=["Colegio de Hibernalia", "a Laberintia"], titulo="Skyrim", sub="El Bastón de Magnus", ajuste=1.0),
    grande("El bastón lanza un chorro", "baston_magnus", "Bastón de Magnus", dur=5.0, x=.25, tam=580),
    ficha("El bastón lanza un chorro", "Bastón de Magnus", "Absorbe *20* de magia por segundo. Sin magia, *salud.*",
          origen="Bastón", dur=9.0),
    ficha("sin parches tiene un error", "Error", "Sin parches, la absorción de salud *puede no funcionar.*", origen="Bastón de Magnus",
          rojo=True, dur=6.0),

    # ---- 7 · Quebrantadora del amanecer
    peg("la Luz de Meridia", "luz_meridia", "Luz de Meridia", dur=4.0, x=.17, tam=360),
    mapa("skyrim", [(.33, .205, "Soledad", "inicio"), (.30, .24), (.265, .275, "Monte Kilkreath", "meta", P("meridia"))],
         de="subes con ella al Monte", a=("al oeste de Soledad|fin", 1.0), marcas=["Monte Kilkreath", "al oeste de Soledad"],
         titulo="Skyrim", ventana=True),
    peg("un nigromante Malkoran", "malkoran", "Malkoran", dur=4.0, x=.17),
    grande("La espada quema", "quebrantadora", "Quebrantadora del amanecer", dur=5.0, x=.75, tam=600),
    ficha("puede soltar una explosión", "Quebrantadora del amanecer", "*10* de fuego. Al matar no muertos, *explosión* de luz.",
          origen="Espada · 12 de daño", dur=9.0),
    ficha("Y tiene la mayor carga", "Carga", "*5 000.* La mayor de las armas que se gastan.", origen="Quebrantadora del amanecer",
          dur=7.0),

    # ---- 6 · Hoja de Ruiseñor
    peg("Te la da Karliah", "karliah", "Karliah", dur=4.5, x=.17),
    peg("asesinó Mercer Frey", "mercer", "Mercer Frey", dur=1.8, x=.75, y=.55, tam=420),
    grande("Cada golpe absorbe veinticinco", "ruisenor", "Hoja de Ruiseñor", dur=5.0, x=.25, tam=600),
    ficha("Cada golpe absorbe veinticinco", "Hoja de Ruiseñor", "Absorbe *25* de salud y *25* de aguante por golpe.",
          origen="Espada · nivel 46+", dur=7.0),
    mg(T.niveles("La trampa del nivel · aguante", RUISENOR,
                 notas=[(4, "No se mejora en la forja", T.SANGRE, 2), (3, "+25 por error", T.ORO, 3)]),
       ("Pero es un arma que sube", -.2), ("Muy de ladrones|fin", .8),
       ["Pero es un arma que sube", "a partir del nivel cuarenta y seis", "no se puede mejorar", "por otro error"], "niveles ruiseñor"),

    # ---- 5 · Espada de Miraak
    peg("del primer Sangre de Dragón", "miraak_db", "Miraak", dur=4.5, x=.75, y=.55, tam=480),
    grande("Y tiene un récord", "espada_miraak", "Espada de Miraak", dur=6.0, x=.25, tam=600),
    ficha("Y tiene un récord", "Espada de Miraak", "*16* de daño base. Récord de las espadas a una mano.",
          origen="Nivel 60+", dur=7.0),
    mg(T.barras("Daño base · espadas a una mano", [(P("espada_daedrica"), "Espada daédrica", 14, 0, T.HUESO),
                                                     (P("espada_hueso"), "Espada de hueso de dragón", 15, 1, T.HUESO),
                                                     (P("espada_miraak"), "Espada de Miraak", 16, 2, T.ORO)],
                remate=("Pesa 3. Menos que una daga", 2)),
       ("Más que la espada daédrica", -.3), ("Menos que una daga|fin", .5),
       ["Más que la espada daédrica", "Más que la de hueso", "Y pesa tres"], "barras miraak"),

    # ---- 4 · Azote de dragones
    mapa("skyrim", [(.535, .655, "Cauce Boscoso", "inicio", P("delphine")), (.48, .58), (.40, .52), (.30, .50),
                    (.23, .49), (.19, .47, "Refugio Celestial", "meta", P("refugio"))],
         de="La historia principal te lleva", a=("al este de Markarth|fin", .8),
         marcas=["con Esbern y Delphine", "Refugio Celestial"], titulo="Skyrim",
         sub="El camino de los Cuchillas", ajuste=1.0),
    grande("está esta katana", "azote", "Azote de dragones", dur=5.0, x=.25, tam=640),
    ficha("En su mejor versión", "Azote de dragones", "*+40* contra dragones. *10* de descarga al resto.",
          origen="Katana · nivel 46+", dur=8.0),
    mg(T.niveles("La trampa del nivel · contra dragones", AZOTE, notas=[(2, "Promete 30, hace 20", T.SANGRE, 1)]),
       ("Y otra vez ojo con el nivel", -.2), ("y en realidad hace veinte|fin", .8),
       [("Y otra vez ojo con el nivel", 0), "la descripción te promete treinta"], "niveles azote"),
    mg(T.golpes("¿Cuántos golpes para un dragón ancestral?", (P("dragon_anciano"), "Dragón ancestral"), 3071,
                [(P("azote"), "Azote de dragones", 38, 38), (P("desgarradora"), "Arma número 3", 38, 52)],
                remate=("14 golpes menos", 2)),
       ("Hice las cuentas", -.2), ("no hay espada mejor|fin", .1),
       ["necesitas unos treinta y ocho", "contra un dragón de escarcha", "catorce golpes menos"], "golpes"),

    # ---- 3 · Desgarradora gélida
    peg("la espada de cristal de Mercer", "mercer", "Mercer Frey", dur=4.0, x=.17),
    mapa("skyrim", [(.885, .78, "Riften", "inicio"), (.87, .755, "Hacienda Bosque de la Grieta", "meta", P("riftweald"))],
         de="en los túneles de su casa", a=("Bosque de la Grieta|fin", 1.2), marcas=["de Riften", "Bosque de la Grieta"],
         titulo="Skyrim", ventana=True, x=.30, y=.45),
    grande("En su mejor versión cada golpe", "desgarradora", "Desgarradora gélida", dur=5.0, x=.25, tam=620),
    ficha("En su mejor versión cada golpe", "Desgarradora gélida", "*30* de escarcha + *15* del filo. Parálisis *2* s.",
          origen="Espada · nivel 46+", dur=5.5),
    mg(T.rejilla("Parálisis por golpe", n=100, encendidas=26, remate=("1 de cada 4", 1)),
       ("Y puede paralizar", -.2), ("Solo espera|fin", .4), ["Y puede paralizar", "un golpe de cada cuatro"], "rejilla"),
    ficha("el frío sube hasta", "Escarcha aumentada", "El frío sube a *45.*", origen="Destrucción", dur=5.0),
    peg("te cuelas en la casa", "riftweald", "La casa de Mercer", dur=5.0, x=.75, y=.55, tam=520),

    # ---- 2 · Arco de Auriel
    mapa("skyrim", [(.10, .50, "Markarth", "inicio"), (.09, .44), (.085, .38, "Cueva de Sima Negra", "meta",
                                                                          P("valle_olvidado"))],
         de="bajando por la Cueva", a=("cerca de Markarth|fin", 1.0), marcas=["Cueva de Sima Negra", "cerca de Markarth"],
         titulo="Skyrim", ventana=True),
    peg("Lo custodia Gelebor", "gelebor", "Gelebor", dur=4.5, x=.17),
    grande("Sus flechas queman", "arco_auriel", "Arco de Auriel", dur=5.0, x=.75, tam=620),
    ficha("Sus flechas queman", "Arco de Auriel", "Daño solar. *Triple* contra no muertos.", origen="Según su descripción",
          dur=7.0),
    peg("las flechas élficas bendecidas", "flecha_sol", "Flecha bendecida por el sol", dur=5.0, x=.17, tam=380),
    ficha("Durante diez segundos", "Bendecidas por el sol", "Disparadas al sol: *10* s de rayos.", origen="Arco de Auriel",
          dur=7.0),
    peg("las que hace Serana", "serana", "Serana", dur=4.5, x=.17),

    # ---- 1 · la daga que forjas tú
    grande("Es una daga de hueso", "daga_hueso", "Daga de hueso de dragón", dur=5.0, x=.75, tam=620),
    mg(T.receta("Se forja", DAGA, (P("daga_hueso"), "Daga de hueso de dragón"), "Herrería 100 + Armadura de dragón",
                remate=("Requiere Dawnguard", 2)),
       ("Necesitas Herrería al cien", -.2), ("Y tener Dawnguard|fin", .8),
       ["un hueso de dragón", "unas tiras de cuero", "Y tener Dawnguard"], "receta daga"),
    ficha("Doce de daño base", "Daga de hueso de dragón", "*12* de daño base.", origen="Daga", dur=5.0),
    ficha("la ventaja Hoja del asesino", "Hoja del asesino", "Ataques furtivos con daga: *×15.*", origen="Discreción · 50",
          dur=6.5),
    peg("los Guantes etéreos", "guantes", "Guantes etéreos", dur=4.0, x=.17, tam=380),
    ficha("ese multiplicador se duplica", "Guantes etéreos", "El multiplicador se duplica: *×30.*", origen="Hermandad Oscura",
          dur=3.4),
    mg(_punalada(), ("una sola puñalada por la espalda", -.4), ("de un dragón legendario|fin", 1.2),
       ["una sola puñalada por la espalda", "Desgarradora gélida en la misma", "Y un dragón anciano", "siete mil seiscientos",
        "Más que la vida entera"], "barras puñalada"),
    mapa("skyrim", [(.52, .50, "Carrera Blanca · Forja del Cielo", "inicio", P("forja_cielo")), (.49, .60), (.46, .70),
                    (.43, .78, "Falkreath · la Hermandad Oscura", "meta", P("guantes"))],
         de="Todas las demás armas", a=("dragón a dragón|fin", 1.0),
         marcas=["Todas las demás armas", "te la ganaste tú"], titulo="Skyrim", sub="La ruta del forjador", ajuste=1.0),

    # ---- cierre
    ficha("en el canal tienes las quince", "Las 15 cosas más INÚTILES de Skyrim", "Ya está en el canal.",
          origen="Video recomendado", dur=6.0, x=.5, y=.40),
    peg("la armería del Refugio Celestial", "azote", "Encima de la mesa", dur=4.5, x=.25, y=.55, tam=520),
]

SFX = {
    "aviso_e": ("Deep nordic war drum hit followed by a short low horn call, fantasy quest notification", 3),
    "aviso_f": ("Steel sword being drawn from a scabbard with a low choir swell, fantasy weapon reveal sting", 3),
    "ruleta": ("Wooden prize wheel spinning fast with clicking pegs then slowing to a stop, single final click", 2),
    "golpe_metal": ("Heavy steel blade clanging on armor, single hit, medieval combat", 1),
    "forja": ("Blacksmith hammer striking a glowing blade on an anvil three times, sparks hiss", 1),
}
_AV = ["hoy van las quince armas", "Número quince", "En el catorce", "Número trece", "En el doce", "Número once",
       "En el diez", "Número nueve", "En el ocho", "Número siete", "En el seis", "Número cinco", "En el cuatro", "Número tres",
       "Número dos", "llegamos al número uno"]
PISTAS = [dict(sfx="aviso_e" if k % 2 == 0 else "aviso_f", en=a, vol=.6 if k in (0, 15) else .5) for k, a in enumerate(_AV)] + [
    dict(sfx="ruleta", en="Puede lanzar fuego", vol=.4),
    dict(sfx="ruleta", en="en un pollo", vol=.35),
    dict(sfx="golpe_metal", en="se vuelve a tambalear", vol=.45),
    dict(sfx="forja", en="La forjas tú", vol=.5),
]

# Hojas de prueba de los MG nuevos (python _prueba_mg.py): (nombre, fn, marcas, tiempos)
PRUEBAS = [
    ("ruleta", _ruleta(), [1, 3, 5, 7, 8.3, 9.6, 10.9, 12.5, 14], [0.5, 2.8, 6.8, 9.0, 12.4, 16]),
    ("niveles", T.niveles("La trampa del nivel · aguante", RUISENOR,
                          notas=[(4, "No se mejora en la forja", T.SANGRE, 2), (3, "+25 por error", T.ORO, 3)]),
     [0.5, 3, 5, 7], [0.4, 1.5, 3.2, 5.4, 7.6, 9]),
    ("golpes", T.golpes("¿Cuántos golpes para un dragón ancestral?", (P("dragon_anciano"), "Dragón ancestral"), 3071,
                        [(P("azote"), "Azote de dragones", 38, 38), (P("desgarradora"), "Arma número 3", 38, 52)],
                        remate=("14 golpes menos", 2)), [0.5, 4, 6.5], [0.3, 1.5, 3.2, 4.6, 6.0, 7.5]),
    ("barras", T.barras("Una sola puñalada", [(P("desgarradora"), "Desgarradora gélida", 900, 1, T.HUESO),
                                               (P("daga_hueso"), "Daga de hueso de dragón", 1980, 0, T.ORO),
                                               (P("daga_hueso"), "La misma, con el bucle", 7650, 3, T.SANGRE)],
                        refs=[("Dragón anciano", 2255, 2), ("Dragón legendario", 4163, 3)], remate=("Dragón a dragón", 4)),
     [0.5, 2.5, 4.5, 6.5, 8.5], [0.4, 1.4, 3.2, 5.0, 7.4, 9.2]),
]
