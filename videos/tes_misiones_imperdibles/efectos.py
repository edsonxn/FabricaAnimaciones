# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 25 misiones de Skyrim que NUNCA debes saltarte» (SECUENCIA YT, Crónicas de Tamriel, 28-oct-2026).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 26 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con cifras del guion (UESP), arriba a la derecha.
- Pegatinas con la imagen REAL (wiki de Fandom) de cada personaje u objeto que se nombra; los clave, GRANDES.
- Comentarios REALES (reglas 27/28-oct-2026): gancho (@sebastiannarvaez6185, @EnriqueJVidal-ei1nk), «Oblivion» (23) y 5 de
  agradecimiento (21, 14, 7 y dos en el cierre).
- MG NUEVOS de este guion (regla 19-oct-2026): versiones «¿Quién dice la verdad?» (Saadia, 20) · inversion «Lo que le pagas
  a Ralis» (10) · fragmentos «El Amuleto de Gauldur» (3). Del kit: contadores (Kyne, 22), plazo (Desenterrado no: 72 h ya
  salió) — no se repiten.
- Mapas reales (tema tes) con FOTO de cada paso y ruta, en 15 de las 25 misiones (el usuario, 29-oct-2026: «al menos la
  mitad, con donde inician y sus objetivos»): 25, 23, 22, 21, 20, 18, 17, 16, 8, 7, 6, 5, 4, 3 y 2 (ventana).
  Coordenadas reales de la base de datos del mapa de UESP calibradas sobre el mapa de papel (`_coords_uesp.py`).
  python fab.py tes_misiones_imperdibles fx --seco   tiempos      python fab.py tes_misiones_imperdibles fx hoja   previews/fx_NN.jpg
"""
import os

import mg_tes as T

CAMARA = {}
FUNDIDO = {}

_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")   # imágenes reales de la wiki
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


def grande(en, slug, titulo, dur=4.5, x=.25, tam=640):
    """Pegatina GRANDE (media pantalla): los personajes y objetos clave."""
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


def com(en, cid, dur=6.0, x=.30, y=.30):
    """Comentario REAL del canal (tarjeta de `fab.py yt comentario`)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760)


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


# ---- los MG nuevos (solo cifras del guion)
def _versiones():
    return T.versiones("¿Quién dice la verdad?",
                       (P("saadia"), "Saadia", ["Noble de Hammerfell", "La persigue el Dominio"], 0),
                       (P("kematu"), "Los alik'r", ["Vendió Taneth al Dominio", "En la Gran Guerra"], 1),
                       veredicto=("Sin pruebas", 2), remate=("Eliges a ciegas", 3))


def _inversion():
    return T.inversion("Lo que le pagas a Ralis", (P("ralis"), "Ralis Sedarys"),
                       [(1000, "Para seguir excavando"), (2000, "Desaparecen los mineros"), (3000, "Mueren los mercenarios"),
                        (5000, "Y otra vez")],
                       nota=("Se te necesita", 4), despierta=(P("ahzidal"), "Ahzidal", 5),
                       remate=("11 000 para despertar a tu jefe", 6))


def _fragmentos():
    return T.fragmentos("El Amuleto de Gauldur", (P("gauldur"), "Gauldur"), (P("amuleto_gauldur"), "Amuleto de Gauldur"),
                        [(P("mikrul"), "Mikrul", "Folgunthur"), (P("jyrik"), "Jyrik", "Saarthal"),
                         (P("sigdis"), "Sigdis", "Sala de Geirmund")],
                        bono=("+30 salud · +30 magia · +30 aguante", 6))


FX = [
    # ---- avisos (uno por puesto)
    aviso("Veinticinco misiones todas comprobadas", "Top 25", "Misiones que nunca debes saltarte", dur=4.5),
    aviso("Número veinticinco", "Misión · número 25", "Simas insondables"),
    aviso("En el veinticuatro", "Misión · número 24", "La expedición perdida"),
    aviso("Número veintitrés", "Misión · número 23", "Vuelta a las raíces"),
    aviso("En el veintidós", "Misión · número 22", "Las pruebas sagradas de Kyne"),
    aviso("Número veintiuno", "Misión · número 21", "Que no se apaguen las llamas"),
    aviso("En el veinte", "Misión · número 20", "En tiempos de necesidad"),
    aviso("Número diecinueve", "Misión · número 19", "Viejos amigos"),
    aviso("En el dieciocho", "Misión · número 18", "El Vial Blanco"),
    aviso("Número diecisiete", "Misión · número 17", "Desaparecido en acto de servicio"),
    aviso("En el dieciséis", "Misión · número 16", "La leyenda de Águila Roja"),
    aviso("Número quince", "Misión · número 15", "Un nuevo yacimiento de stalhrim"),
    aviso("En el catorce", "Misión · número 14", "Se sirve mejor fría"),
    aviso("Número trece", "Misión · número 13", "El cráneo de Arvak"),
    aviso("En el doce", "Misión · número 12", "Estigma mortal"),
    aviso("Número once", "Misión · número 11", "Libro negro: El regente amarillento"),
    aviso("En el diez", "Misión · número 10", "Desenterrado"),
    aviso("Número nueve", "Misión · número 9", "Durnehviir"),
    aviso("En el ocho", "Misión · número 8", "La gloria de los muertos"),
    aviso("Número siete", "Misión · número 7", "Al alba"),
    aviso("En el seis", "Misión · número 6", "El despertar de la Reina Loba"),
    aviso("Número cinco", "Misión · número 5", "El guerrero de ébano"),
    aviso("En el cuatro", "Misión · número 4", "Descifrar lo transmundano"),
    aviso("Número tres", "Misión · número 3", "Leyenda prohibida"),
    aviso("En el dos", "Misión · número 2", "Tocando el cielo"),
    aviso("llegamos al número uno", "Misión · número 1", "La mente de la locura", dur=4.5),

    # ---- gancho
    com("En el video de las misiones", "UgxpWfnpyO4DmhyywAJ4AaABAg", dur=9.5),
    com("nos contó que Arniel", "UgxVRMXvtlW6ERT6KDV4AaABAg", dur=7.5),
    peg("el mejor amuleto del juego", "amuleto_gauldur", "", dur=1.6, x=.12, tam=290),
    peg("un caballo inmortal", "arvak", "", dur=1.6, x=.29, tam=290),
    peg("una casa gratis", "mansion_severin", "", dur=1.6, x=.46, tam=290),
    peg("un bastón que convierte", "wabbajack", "", dur=2.6, x=.63, tam=290),
    peg("empieza con un mendigo", "dervenin", "", dur=2.2, x=.17, tam=360),
    grande("dentro de la cabeza de un emperador", "sheogorath", "", dur=3.0, x=.75, tam=560),

    # ---- 25 · Simas insondables
    mapa("skyrim", [(.89, .78, "Riften · muelles", "inicio", P("fathoms")), (.84, .82),
                    (.774, .814, "Avanchnzel", "meta", P("lexicon"))],
         de="en los muelles de Riften", a=("en las montañas de Jerall|fin", .8),
         marcas=["en los muelles de Riften", "lleves un léxico a Avanchnzel"], titulo="Skyrim", sub="Simas insondables", ajuste=.6),
    peg("Breya muere junto a un centurión", "breya", "Breya", dur=4.0, x=.17),
    ficha("Tenía que subir un veinticinco", "Conocimiento antiguo", "*+25 %* de armadura… con la armadura *enana.*",
          origen="Efecto permanente", dur=6.0),
    ficha("se equivocó al revés", "Error del parche", "Ahora vale con *todas*, menos con la *enana.*", origen="Bethesda",
          rojo=True, dur=7.0),

    # ---- 24 · La expedición perdida
    peg("el mago Calcelmo", "calcelmo", "Calcelmo", dur=4.5, x=.17),
    ficha("No sobrevive nadie", "La expedición", "Supervivientes: *0.*", origen="Nchuand-Zel", rojo=True, dur=4.5),
    grande("los autómatas dwemer de toda", "centurion", "Autómatas dwemer", dur=5.0, x=.75, tam=560),
    peg("con los falmer", "falmer", "Falmer", dur=4.0, x=.17, tam=380),

    # ---- 23 · Vuelta a las raíces
    peg("Es Sinderion", "sinderion", "Sinderion", dur=4.5, x=.17),
    grande("la raíz de nirn carmesí", "nirn_carmesi", "Raíz de nirn carmesí", dur=4.5, x=.75, tam=480),
    com("nos recordó que se dice Oblivion", "Ugz2pMFkyhOQRp78FYZ4AaABAg", dur=6.5),
    mapa("skyrim", [(.663, .281, "Límite Sombrío · entrada de Alftand", "inicio", P("nirn_carmesi")), (.70, .45), (.72, .60),
                    (.750, .709, "Granja Sarethi · Avrusa", "meta", P("avrusa"))],
         de="Juntar treinta raíces", a=("a su granja cerca de Riften|fin", .8),
         marcas=["Juntar treinta raíces", "Avrusa Sarethi"], titulo="Skyrim", sub="Vuelta a las raíces", ajuste=.6),
    ficha("El premio es Descubrimiento", "Descubrimiento de Sinderion", "*25 %* de sacar *dos* pociones en vez de una.",
          origen="Efecto permanente", dur=7.0),

    # ---- 22 · Kyne
    peg("un viejo cazador Froki", "froki", "Froki", dur=4.0, x=.17),
    mapa("skyrim", [(.715, .798, "Choza de Froki", "inicio", P("froki")), (.64, .66),
                    (.52, .52, "Carrera Blanca · cangrejo del barro", "paso", None), (.58, .44),
                    (.63, .34, "El Pálido · skeever", "paso", None), (.55, .55), (.47, .66),
                    (.42, .76, "Falkreath · lobo y oso", "paso", None), (.48, .62), (.60, .45),
                    (.70, .26, "Hibernalia · gato sable", "meta", None)],
         de="Un cangrejo del barro", a=("Y al final un trol|fin", .6),
         marcas=["Un cangrejo del barro", "un skeever", "y un lobo", "un gato sable"],
         titulo="Skyrim", sub="Las pruebas sagradas de Kyne", ajuste=1.0, traza=99),
    grande("el Símbolo de Kyne", "simbolo_kyne", "Símbolo de Kyne", dur=4.5, x=.25, tam=460),
    ficha("Diez por ciento menos", "Símbolo de Kyne", "*-10 %* de daño de animales · *+5 %* con arco.", origen="Recompensa",
          dur=6.0),
    ficha("reduce el daño de todas", "Error", "Vale contra *todas* las criaturas: ≈ *83* de armadura.", origen="Símbolo de Kyne",
          rojo=True, dur=7.0),

    # ---- 21 · Que no se apaguen las llamas
    mapa("skyrim", [(.33, .20, "Soledad · Colegio de Bardos", "inicio", P("viarmo")), (.35, .28),
                    (.341, .351, "Respiro del Muerto · el verso", "meta", P("olaf"))],
         de="Para entrar en el Colegio", a=("en el Respiro del Muerto|fin", 1.8),
         marcas=["Colegio de Bardos de Soledad", "en el Respiro del Muerto"], titulo="Skyrim", sub="Que no se apaguen las llamas", ajuste=.6),
    grande("Olaf Ojo Único ejecutó", "olaf", "Olaf Ojo Único", dur=4.5, x=.75, tam=520),
    peg("al bardo Svaknir", "svaknir", "Svaknir", dur=4.0, x=.17),
    ficha("ahora es una fiesta cada semana", "Pastel de carne", "En realidad es un pastel de *manzana.*",
          origen="Festival", dur=6.0),
    com("nos escribió que le gusta", "Ugyc7_uwHsGT33mS6KZ4AaABAg", dur=7.0),

    # ---- 20 · Saadia
    peg("unos guerreros alik'r", "alikr", "Guerrero alik'r", dur=4.0, x=.17),
    mg(_versiones(), ("Es Saadia que trabaja", -.2), ("Eliges a ciegas|fin", .8),
       ["Es Saadia que trabaja", "Los alik'r te cuentan", "no te da pruebas", "Eliges a ciegas"], "versiones saadia"),
    mapa("skyrim", [(.545, .49, "Carrera Blanca · Saadia", "inicio", P("saadia")), (.47, .50),
                    (.392, .498, "Guarida de los Timadores · Kematu", "peligro", P("kematu"))],
         de="Para hablar con su jefe", a=("El guarda pierde las llaves|fin", .5),
         marcas=["Para hablar con su jefe", "Pagas la multa"], titulo="Skyrim", sub="En tiempos de necesidad", ajuste=.6),
    ficha("se puede cobrar a los dos", "Doble cobro", "*1 100* monedas por traicionar a todo el mundo.", origen="Trampa",
          dur=6.0),

    # ---- 19 · Viejos amigos
    grande("el mago Neloth", "neloth", "Neloth", dur=4.5, x=.75, tam=520),
    peg("una antigua aprendiz suya", "ildari", "Ildari", dur=4.5, x=.17),
    peg("corazones de piedra", "corazon_piedra", "Corazón de piedra", dur=4.0, x=.17, tam=360),
    ficha("te promete una cama", "Promesa de Neloth", "Cama y cofre en su torre: *no existen.*", origen="Error",
          rojo=True, dur=7.0),

    # ---- 18 · El Vial Blanco
    peg("el viejo alquimista Nurelion", "nurelion", "Nurelion", dur=4.5, x=.17),
    mapa("skyrim", [(.78, .42, "Ventalia · Nurelion", "inicio", P("nurelion")), (.73, .38),
                    (.684, .359, "Cueva abandonada · Curalmil", "meta", P("vial"))],
         de="Lo encuentras en la Cueva", a=("Y está roto|fin", .8),
         marcas=["Lo encuentras en la Cueva", "custodiado por un draugr"], titulo="Skyrim", sub="El Vial Blanco", ajuste=.6),
    peg("Su aprendiz Quinto Navale", "quinto", "Quinto Navale", dur=4.0, x=.17),
    ficha("se rellena solo cada día", "Vial Blanco", "Se rellena *cada día.* *+100* de salud, o *+50 %* a una mano.",
          origen="Reparado", dur=8.0),

    # ---- 17 · Desaparecido
    peg("Fralia Melena Gris discute", "fralia", "Fralia Melena Gris", dur=4.5, x=.17),
    grande("Su hijo Thorald", "thorald", "Thorald Melena Gris", dur=4.5, x=.75, tam=500),
    mapa("skyrim", [(.545, .49, "Carrera Blanca · Fralia", "inicio", P("fralia")), (.42, .40), (.30, .29), (.22, .21),
                    (.165, .165, "Bastión de la Guardia del Norte · Thorald", "meta", P("thorald"))],
         de="Lo tienen preso los thalmor", a=("en el Bastión de la Guardia del Norte|fin", 2.0),
         marcas=["Lo tienen preso los thalmor", "en el Bastión de la Guardia del Norte"], titulo="Skyrim", sub="Desaparecido en acto de servicio", ajuste=.5, traza=99),
    peg("convenciendo a Idolaf", "idolaf", "Idolaf Batallador", dur=3.5, x=.17, tam=360),
    peg("que el padre Eorlund", "eorlund", "Eorlund Melena Gris", dur=4.0, x=.17),
    ficha("al general Tulio", "Vía pacífica", "El diálogo está grabado. *Nunca* se activa.", origen="Error", rojo=True, dur=7.0),

    # ---- 16 · Águila Roja
    grande("La leyenda de Águila Roja un rey", "aguila_roja", "Águila Roja", dur=5.0, x=.75, tam=520),
    mapa("skyrim", [(.214, .459, "Reducto del Águila Roja", "inicio", P("aguila_roja")),
                    (.230, .423, "Torres Hendidas · la espada", "paso", P("furia_aguila")),
                    (.249, .437, "Túmulo del Rebelde", "meta", None)],
         de=("Recuperas la espada", -.4), a=("y la llevas a su túmulo|fin", 2.0),
         marcas=["Recuperas la espada", "en las Torres Hendidas", "y la llevas a su túmulo"], titulo="Skyrim", sub="La leyenda de Águila Roja", ajuste=.5),
    ficha("Diez de fuego y los no muertos", "Perdición del Águila Roja", "*10* de fuego. Los no muertos *arden* y huyen.",
          origen="Espada", dur=6.5),

    # ---- 15 · stalhrim
    peg("Baldor Hierro Forjado", "baldor", "Baldor Hierro Forjado", dur=4.5, x=.17),
    peg("El hielo encantado", "stalhrim", "Stalhrim", dur=4.0, x=.75, y=.55, tam=380),
    peg("un tal Ancarion", "ancarion", "Ancarion", dur=4.0, x=.17),
    grande("saber forjarlo con herrería", "armadura_stalhrim", "Armadura de stalhrim", dur=5.0, x=.75, tam=520),
    ficha("saber forjarlo con herrería", "Stalhrim", "Requiere herrería *80.* Daño del ébano, *menos* peso.", origen="Forja",
          dur=7.0, x=.30),
    ficha("Y los encantamientos de escarcha", "Stalhrim", "Escarcha *+25 %* más fuerte.", origen="Encantamiento", dur=5.0),

    # ---- 14 · Se sirve mejor fría
    peg("el capitán Veleth", "veleth", "Capitán Veleth", dur=4.0, x=.17),
    grande("Vendil Severin ataca", "vendil", "Vendil Severin", dur=4.5, x=.75, tam=500),
    grande("La Mansión Severin con todo", "mansion_severin", "Mansión Severin", dur=5.0, x=.25, tam=600),
    ficha("A partir del sesenta", "Se sirve mejor fría", "Casa *gratis* + hasta *10 000* monedas.", origen="Recompensa",
          dur=6.0),
    com("nos contó que se pasó el juego", "Ugwr_GZEoP1Oiprao8F4AaABAg", dur=7.5),

    # ---- 13 · Arvak
    grande("Busca a su caballo", "craneo_arvak", "Cráneo de Arvak", dur=4.5, x=.75, tam=420),
    grande("Un caballo esqueleto en llamas", "arvak", "Arvak", dur=5.0, x=.25, tam=640),
    ficha("no muere para siempre", "Invocar a Arvak", "No muere *para siempre.* No cuesta *nada.*", origen="Conjuración",
          dur=6.0),
    ficha("puedes invocar dos Arvak", "Almas gemelas", "*Dos* Arvak a la vez.", origen="Ventaja", dur=5.0),

    # ---- 12 · Estigma mortal
    grande("Haknir Estigma Mortal Un pirata", "haknir", "Haknir Estigma Mortal", dur=5.0, x=.75, tam=500),
    ficha("cuatro cofres escondidos", "Tesoro de Haknir", "*4* cofres. *Sin* marcadores. Una pieza en cada uno.",
          origen="Búsqueda del tesoro", dur=7.0),
    ficha("Con ochenta montones de oro", "Túmulo de Gyldenhul", "*80* montones de oro… y un *rastrillo.*", origen="Isla de los horkers",
          dur=8.0),
    grande("La armadura sube tu aguante", "armadura_estigma", "Armadura de Estigma Mortal", dur=5.5, x=.25, tam=520),
    ficha("más de seis mil cuatrocientas", "Botín", "Más de *6 400* monedas.", origen="Estigma mortal", dur=4.5),

    # ---- 11 · Libro negro
    grande("Los libros negros de Hermaeus Mora", "hermaeus", "Hermaeus Mora", dur=5.0, x=.75, tam=560),
    peg("detrás de un sacerdote dragón Dukaan", "dukaan", "Dukaan", dur=4.0, x=.17),
    peg("Al final eliges una de tres", "libro_negro", "El regente amarillento", dur=4.5, x=.17, tam=380),
    mg(T.contadores("Elige una (permanente)", [("Buscador de poder · combate", 10, 0, 0),
                                                ("Buscador de hechicería · hechizos y encantamientos", 10, 1, 1),
                                                ("Buscador de sombras · sigilo", 10, 2, 2)],
                    remate=("Y puedes cambiar gratis", 3)),
       ("Buscador de poder", -.3), ("Hermaeus Mora es el único|fin", .6),
       ["Buscador de poder", "Buscador de hechicería", "Buscador de sombras", "relees el libro"], "contadores libro negro"),

    # ---- 10 · Desenterrado
    peg("Ralis Sedarys excava", "ralis", "Ralis Sedarys", dur=1.8, x=.17),
    mg(_inversion(), ("para seguir Mil monedas", -.6), ("Once mil monedas para financiar|fin", .8),
       ["para seguir Mil monedas", "Luego dos mil", "Luego tres mil", "Luego cinco mil", "Se te necesita", "despertando a Ahzidal",
        "Once mil monedas"], "inversion ralis"),
    grande("Pero sus reliquias valen", "mascara_ahzidal", "Máscara de Ahzidal", dur=5.0, x=.25, tam=460),
    ficha("cincuenta por ciento de resistencia", "Reliquias de Ahzidal", "*50 %* contra el fuego. Con *4* puestas: *+10* encantamiento.",
          origen="Desenterrado", dur=7.5),

    # ---- 9 · Durnehviir
    grande("un dragón no muerto Durnehviir", "durnehviir", "Durnehviir", dur=5.0, x=.75, tam=600),
    peg("guardaría a Valérica", "valerica", "Valérica", dur=4.5, x=.17),
    ficha("Trescientos de daño", "Desgarro del alma", "*300* de daño. Atrapa el alma. Si muere, se levanta *contigo.*",
          origen="Grito", dur=8.0),

    # ---- 8 · La gloria de los muertos
    grande("Kodlak Melena Blanca el Heraldo", "kodlak", "Kodlak Melena Blanca", dur=5.0, x=.75, tam=520),
    mapa("skyrim", [(.545, .49, "Carrera Blanca · Forja del Cielo", "inicio", P("kodlak")), (.62, .38), (.68, .26),
                    (.696, .156, "Tumba de Ysgramor", "meta", P("wuuthrad"))],
         de="Para liberarla vas a la Tumba", a=("en la Forja del Cielo|fin", 1.0),
         marcas=["Para liberarla vas", "a la Tumba de Ysgramor"], titulo="Skyrim", sub="La gloria de los muertos", ajuste=.5, traza=99),
    peg("una cabeza de bruja de Glenmoril", "cabeza_bruja", "Cabeza de bruja de Glenmoril", dur=4.5, x=.17, tam=380),
    grande("y con el Escudo de Ysgramor", "escudo_ysgramor", "Escudo de Ysgramor", dur=5.0, x=.25, tam=460),
    ficha("veinte de resistencia a la magia", "Escudo de Ysgramor", "*+20* resistencia a la magia · *+20* de salud.",
          origen="Recompensa", dur=6.0),
    peg("Farkas se para", "farkas", "Farkas", dur=4.5, x=.17),

    # ---- 7 · Al alba
    peg("la Luz de Meridia", "luz_meridia", "Luz de Meridia", dur=4.0, x=.17, tam=360),
    ficha("más de ciento cincuenta sitios", "Luz de Meridia", "Puede salir en más de *150* cofres.", origen="Al alba", dur=5.0),
    mapa("skyrim", [(.278, .218, "Monte Kilkreath · estatua de Meridia", "inicio", P("meridia")),
                    (.292, .211, "Ruinas de Kilkreath · Malkoran", "meta", P("malkoran"))],
         de="Te lleva al Monte Kilkreath", a=("de pedestal en pedestal|fin", .8),
         marcas=["Te lleva al Monte Kilkreath", "Te manda limpiar su templo"], titulo="Skyrim", sub="Al alba", ajuste=.4),
    ficha("cuarenta y tres cadáveres", "Templo de Kilkreath", "*43* cadáveres con oro: más de *5 000.*", origen="Botín", dur=6.0),
    grande("es el Quebrantador de amaneceres", "dawnbreaker", "Quebrantador de amaneceres", dur=5.0, x=.25, tam=500),
    com("nadie le había explicado", "UgyQu8Ua86q9VZ6IevJ4AaABAg", dur=8.0),

    # ---- 6 · Reina Loba
    mapa("skyrim", [(.33, .20, "Soledad · Falk Barba de Fuego", "inicio", P("falk")),
                    (.270, .194, "Cueva Cráneo de Lobo", "peligro", P("potema"))],
         de="En Soledad Falk Barba", a=("Parece una falsa alarma|fin", 1.0),
         marcas=["En Soledad Falk Barba", "en la Cueva Cráneo de Lobo"], titulo="Skyrim", sub="El despertar de la Reina Loba", ajuste=.4),
    grande("resucitar a Potema", "potema", "Potema, la Reina Loba", dur=5.0, x=.75, tam=560),
    ficha("Las flechas no le hacen nada", "Potema", "Flechas: *nada.* Magia: *sí.*", origen="Catacumbas", dur=5.5),
    peg("recuperas su calavera", "calavera_potema", "Calavera de Potema", dur=4.0, x=.17, tam=380),
    peg("el Escudo de Soledad", "escudo_soledad", "Escudo de Soledad", dur=4.0, x=.17, tam=380),

    # ---- 5 · Guerrero de ébano
    grande("un guerrero con armadura de ébano", "guerrero_ebano", "Guerrero de ébano", dur=5.5, x=.75, tam=600),
    ficha("al nivel ochenta", "Guerrero de ébano", "Solo a partir del nivel *80.*", origen="Requisito", dur=5.0, x=.30),
    mapa("skyrim", [(.89, .78, "Riften", "inicio", None),
                    (.934, .719, "Última Vigilia", "peligro", P("guerrero_ebano"))],
         de="Te espera en la Última Vigilia", a=("hasta que le pegas tú|fin", .6),
         marcas=["Te espera en la Última Vigilia", ("Te espera en la Última Vigilia", 1.2)], titulo="Skyrim", sub="El guerrero de ébano", ajuste=.4),
    ficha("dos mil setenta y uno", "Guerrero de ébano", "*2 071* de salud. Gritos. *Reflejar golpes.*", origen="Jefe",
          rojo=True, dur=7.0),
    peg("la Cuchilla de Mehrunes", "cuchilla_mehrunes", "Cuchilla de Mehrunes", dur=4.0, x=.17, tam=380),

    # ---- 4 · Oghma
    grande("vive Séptimo Signo", "septimo", "Séptimo Signo", dur=5.0, x=.75, tam=520),
    mapa("skyrim", [(.740, .097, "Puesto de Séptimo Signo", "inicio", P("septimo")), (.70, .19),
                    (.663, .281, "Alftand · bajada al Límite Sombrío", "meta", None)],
         de="Te manda al Límite Sombrío", a=("a leer un Pergamino antiguo|fin", 1.0),
         marcas=["Te manda al Límite Sombrío", "a la Torre de Mzark"], titulo="Skyrim", sub="Descifrar lo transmundano", ajuste=.5),
    grande("El Oghma Infinium", "oghma", "Oghma Infinium", dur=4.5, x=.25, tam=460),
    peg("Y Hermaeus Mora que le había", "hermaeus", "Hermaeus Mora", dur=4.0, x=.75, y=.58, tam=420),
    ficha("cinco puntos en seis habilidades", "Oghma Infinium", "*+5* a *6* habilidades: *30* niveles gratis.",
          origen="Poder · sombra · magia", dur=7.0),

    # ---- 3 · Gauldur
    mapa("skyrim", [(.381, .240, "Folgunthur · Mikrul", "inicio", P("mikrul")), (.50, .23), (.62, .22),
                    (.692, .239, "Saarthal · Jyrik", "paso", P("jyrik")), (.74, .40), (.72, .58),
                    (.698, .691, "Sala de Geirmund · Sigdis", "paso", P("sigdis")), (.55, .64), (.35, .60), (.22, .55),
                    (.182, .514, "Roca de la Cuenca · Gauldur", "meta", P("gauldur"))],
         de="Cada hijo está en una mazmorra", a=("aparece el propio Gauldur|fin", .2),
         marcas=["Mikrul en Folgunthur", "Jyrik en Saarthal", "Sigdis en la Sala", "la Roca de la Cuenca"],
         titulo="Skyrim", sub="Leyenda prohibida", ajuste=1.0, traza=99),
    mg(_fragmentos(), ("Gauldur era un archimago", -.2), ("borró todo registro del crimen|fin", .3),
       ["en tres pedazos", "Sus tres hijos", ("Sus tres hijos", .5), ("Sus tres hijos", 1.0), 99999, 99999, 99999],
       "fragmentos gauldur (se parte)"),
    mg(_fragmentos(), ("Y fulmina a sus tres hijos", -.1), ("El mejor amuleto sin trampas|fin", .6),
       [("Y fulmina", -4), ("Y fulmina", -4), ("Y fulmina", -4), ("Y fulmina", -4), ("Y fulmina", .1),
        ("a sus tres hijos", .5), "Treinta más de salud"], "fragmentos gauldur (se recompone)"),
    ficha("Lo ideal nivel treinta y seis", "Consejo", "Lee el libro a nivel *36.* El botín se fija *al leerlo.*",
          origen="Leyenda prohibida", dur=4.2),

    # ---- 2 · Tocando el cielo
    peg("Con Serana llegas", "serana", "Serana", dur=4.0, x=.17),
    mapa("skyrim", [(.146, .294, "Cueva de Sima Negra · Gelebor", "meta", P("gelebor"))],
         de=("Con Serana llegas", .8), a=("te abre un pasaje|fin", .8), marcas=["la Cueva de Sima Negra"], titulo="Skyrim", sub="Tocando el cielo", ventana=True),
    grande("el Archicoadjutor Vyrthur", "vyrthur", "Vyrthur", dur=5.0, x=.75, tam=520),
    peg("que persigue Harkon", "harkon", "Harkon", dur=3.5, x=.17, tam=360),
    grande("El Arco de Auriel ya salió", "arco_auriel", "Arco de Auriel", dur=5.0, x=.25, tam=520),
    ficha("Con flechas bendecidas", "Arco de Auriel", "Bendecidas: rayos *10 s.* Malditas: *apagas el sol.*",
          origen="Flechas", dur=8.0),

    # ---- 1 · La mente de la locura
    peg("un mendigo Dervenin", "dervenin", "Dervenin", dur=4.0, x=.17),
    grande("Su señor es Sheogorath", "sheogorath", "Sheogorath", dur=5.5, x=.75, tam=600),
    peg("Pelagio el Loco", "pelagio", "Pelagio el Loco", dur=4.0, x=.17),
    grande("te da el Wabbajack", "wabbajack", "Wabbajack", dur=5.0, x=.25, tam=480),
    peg("en pollo", "pollo", "", dur=1.4, x=.12, y=.66, tam=260),
    peg("en conejo en queso", "queso", "", dur=1.4, x=.27, y=.66, tam=260),
    peg("en un bollo dulce", "bollo", "", dur=2.0, x=.42, y=.66, tam=260),
    ficha("y te lo comes", "Bollo dulce", "Personaje esencial convertido y comido: *desaparece.*", origen="Wabbajack",
          rojo=True, dur=6.5),

    # ---- cierre (agradecimientos)
    com("nos dijo que sigue alucinando", "Ugw9HMZ082GXDrFU_LB4AaABAg", dur=6.5, x=.30, y=.28),
    com("nos dio las gracias", "UgyURQpUf5EqoN9PRZ54AaABAg", dur=5.5, x=.70, y=.62),
]
