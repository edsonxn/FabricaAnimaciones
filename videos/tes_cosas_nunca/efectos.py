# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 20 cosas que NUNCA debes hacer en Skyrim» (SECUENCIA YT, Crónicas de Tamriel, 27-oct-2026).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 21 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con cifras del guion (UESP), arriba a la derecha.
- Pegatinas con la imagen REAL (wiki de Fandom) de cada personaje u objeto que se nombra; los clave, GRANDES.
- 3 comentarios REALES del canal (regla 27-oct-2026): gancho (@DavidSanchez-nz2cb), «jarl» (@federicoherrera2105), n.º 15.
- MG NUEVOS de este guion (regla 19-oct-2026): plazo «72 horas» (Lydia 18 · Sanguinare 3) · paciencia «La paciencia de
  Lydia» (14) · escalado «Subir de nivel sin pelear» (2) · reinicio «El cofre que se vacía» (1). Del kit: trato (la
  estrella, 12), contadores (agresión / asesinato, 15).
- Mapa real (tema tes) con FOTO de cada paso: la resaca de Sanguine (8).
  python fab.py tes_cosas_nunca fx --seco   tiempos      python fab.py tes_cosas_nunca fx hoja   previews/fx_NN.jpg (MÍRALA)
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


def com(en, cid, dur=6.0):
    """Comentario REAL del canal (tarjeta de `fab.py yt comentario`)."""
    return peg(en, "com_" + cid, "", dur=dur, x=.30, y=.30, tam=760)


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
def _plazo_lydia():
    return T.plazo("Le dijiste que esperara", 72, (P("lydia"), "Lydia"), avisos=[(72, "Se ha cansado de esperar")],
                   final=("Se va", 1))


def _plazo_vampiro():
    return T.plazo("Sanguinare Vampiris", 72, (P("vampiro"), "Tú"),
                   avisos=[(30, "Al amanecer te sientes débil"), (54, "Al anochecer, una sed extraña")],
                   curas=[(P("pocion_curacion"), "Poción"), (P("azura"), "Santuario"), (P("pluma_halcon"), "Pluma de halcón")],
                   final=("Vampiro", 1))


def _paciencia():
    return T.paciencia("La paciencia de Lydia", (P("lydia"), "Lydia"), golpes=3, remate=("Mira dónde está Lydia", 4))


def _escalado():
    return T.escalado("Subir de nivel sin pelear", (P("daga_hierro"), "Daga de hierro"), (100, "Dagas de hierro"), (20, 50),
                      (P("daga_hierro"), "Tu espada"),
                      [(27, P("dragon_escarcha"), "Dragón de escarcha · 27", 2), (78, P("dragon_legendario"), "Legendario · 78", 3)],
                      remate=("Todo por cien dagas de hierro", 4))


def _reinicio():
    return T.reinicio("Guardar cosas en cualquier cofre",
                      [(P("estrella_azura"), "Estrella de Azura"), (P("cota_ebano"), "Cota de ébano"),
                       (P("daga_hierro"), "Daga"), (P("pluma_halcon"), "Plumas"), (P("garrote"), "Garrote"),
                       (P("pocion_curacion"), "Pociones"), (P("ganzua"), "Ganzúas"), (P("barril"), "Barril")],
                      10, (P("hogar_brisa"), "Dentro de tu casa", 10), remate=("Cien horas de botín", 11))


FX = [
    # ---- avisos (uno por puesto)
    aviso("aquí van las veinte cosas", "Top 20", "Lo que nunca debes hacer en Skyrim", dur=4.5),
    aviso("Número veinte", "Nunca · número 20", "Atacar una gallina"),
    aviso("En el diecinueve", "Nunca · número 19", "Robar un caballo"),
    aviso("Número dieciocho", "Nunca · número 18", "Dejar a tu seguidor esperando"),
    aviso("En el diecisiete", "Nunca · número 17", "Que tu seguidor vaya delante"),
    aviso("Número dieciséis", "Nunca · número 16", "Sacar un arma en una pelea a puñetazos"),
    aviso("En el quince", "Nunca · número 15", "Gritarle a la gente"),
    aviso("Número catorce", "Nunca · número 14", "Bolas de fuego cerca de tu seguidor"),
    aviso("En el trece", "Nunca · número 13", "Quedarte la Llave maestra"),
    aviso("Número doce", "Nunca · número 12", "Darle la estrella a quien no debes"),
    aviso("En el once", "Nunca · número 11", "Moverte cuando muere un dragón"),
    aviso("Número diez", "Nunca · número 10", "Robarle a quien tiene familia"),
    aviso("En el nueve", "Nunca · número 9", "Ir a la cárcel"),
    aviso("Número ocho", "Nunca · número 8", "Beber con un desconocido"),
    aviso("En el siete", "Nunca · número 7", "Matar a un comerciante"),
    aviso("Número seis", "Nunca · número 6", "Matar a Cicerón"),
    aviso("En el cinco", "Nunca · número 5", "Enfadar a un gigante"),
    aviso("Número cuatro", "Nunca · número 4", "Transformarte delante de testigos"),
    aviso("En el tres", "Nunca · número 3", "Ignorar una enfermedad"),
    aviso("Número dos", "Nunca · número 2", "Subir de nivel sin pelear"),
    aviso("llegamos al número uno", "Nunca · número 1", "Guardar cosas en cualquier cofre", dur=4.5),

    # ---- gancho
    com("En el video de las misiones", "UgyMA7FtfA_PT3SZH5V4AaABAg", dur=9.0),
    peg("Un botón que pulsas", "barril", "", dur=1.6, x=.14, tam=300),
    peg("un cofre cualquiera", "cofre", "", dur=1.6, x=.31, tam=300),
    peg("una gallina", "pollo", "", dur=2.4, x=.48, tam=300),
    com("nos corrigió cómo se dice", "UgwNcSsvmI-euGxgzh14AaABAg", dur=5.5),

    # ---- 20 · gallina
    grande("las gallinas de los pueblos", "pollo", "Gallina", dur=4.5, x=.75, tam=560),
    ficha("pegarle a una gallina con dueño", "Gallina con dueño", "Pegarle es un *crimen.* Con su recompensa.",
          origen="Animal de granja", dur=6.0),
    ficha("los animales de granja contaban", "Error", "Los animales de granja contaban como *testigos.*",
          origen="Juego original", rojo=True, dur=8.0),
    peg("Iona tu guardia personal", "iona", "Iona · Villa Melosa", dur=4.5, x=.17),

    # ---- 19 · caballo
    grande("Ves un caballo atado", "caballo", "Caballo con dueño", dur=4.5, x=.75, tam=560),
    ficha("Cincuenta monedas de recompensa", "Robo de caballo", "*50* monedas cada vez que te ven *montarlo.*",
          origen="Recompensa", dur=9.0),
    peg("Los caballos igual que las gallinas", "caballo", "Testigo", dur=3.5, x=.17, tam=360),
    peg("Y tus seguidores tienen principios", "lydia", "Lydia", dur=4.5, x=.17),

    # ---- 18 · seguidor esperando
    grande("Le dices a Lydia", "lydia", "Lydia", dur=4.0, x=.25, tam=560),
    mg(_plazo_lydia(), ("Pues a las setenta y dos horas", -.6), ("Tu seguidor se ha cansado de esperar|fin", 1.4),
       ["Pues a las setenta y dos horas", "se ha cansado de esperar"], "plazo lydia"),
    ficha("Su cuerpo desaparece", "Salón de los Muertos", "Sus cosas acaban en un *ataúd.* Y una carta de *herencia.*",
          origen="Si tu seguidor muere", dur=9.0),

    # ---- 17 · trampas
    ficha("Las placas de presión", "Placa de presión", "La puede pisar *cualquiera.* Y se *rearma.*", origen="Trampa",
          dur=8.0),
    ficha("tu seguidor puede abandonarte", "Seguidor", "Si tu trampa le hace mucho daño: te *abandona* y te *ataca.*",
          origen="Fuego amigo", rojo=True, dur=6.5),
    ficha("existe la ventaja Pies ligeros", "Pies ligeros", "Pisas las placas y *no pasa nada.*", origen="Discreción",
          dur=6.0),

    # ---- 16 · pelea a puñetazos
    grande("Uthgerd la Indómita", "uthgerd", "Uthgerd la Indómita", dur=4.5, x=.75, tam=560),
    ficha("La apuesta suele ser de cien", "Pelea a puñetazos", "Apuesta: *100.* Si ganas, te llevas *100* más.",
          origen="Carrera Blanca", dur=7.0),
    ficha("rompe la pelea", "Agresión", "Cualquier daño que no sea un puñetazo: *40* monedas.", origen="Recompensa",
          rojo=True, dur=8.0),
    grande("la Cota de ébano", "cota_ebano", "Cota de ébano", dur=5.0, x=.25, tam=520),
    peg("la armadura de Boethiah", "boethiah", "Boethiah", dur=3.5, x=.75, y=.55, tam=380),

    # ---- 15 · Fus Ro Dah
    ficha("Gritar en la ciudad sin darle", "Fuerza implacable", "Sin darle a nadie: un *aviso* del guardia.",
          origen="Fus Ro Dah", dur=7.0),
    mg(T.contadores("Fuerza implacable", [("Agresión", 40, 0, 0), ("Asesinato", 1000, 1, 1), ("Caída por un barranco", 0, 2, 2)],
                    remate=("El barranco hace el resto", 3)),
       ("Pero si el grito golpea", -.3), ("El barranco hace el resto|fin", .6),
       ["es agresión", "si lo mata", "Las muertes por caída", "El barranco hace el resto"], "contadores fus"),
    com("nos dejó su plan", "Ugxe-I3h17bOKEaP18N4AaABAg", dur=7.0),
    peg("Mirar a Delphine", "delphine", "Delphine", dur=4.0, x=.75, y=.58, tam=420),

    # ---- 14 · fuego amigo
    ficha("Tus seguidores son personajes protegidos", "PNJ protegido", "Los enemigos lo tumban. Solo *tú* puedes matarlo.",
          origen="Seguidor", dur=9.0),
    mg(_paciencia(), ("Los primeros golpes los perdona", -.3), ("mirar dónde está Lydia|fin", .8),
       ["Los primeros golpes", "con un aviso", "si le das más de tres", "y va a por ti", "mirar dónde está Lydia"], "paciencia"),

    # ---- 13 · Llave maestra
    peg("el artefacto de Nocturnal", "nocturnal", "Nocturnal", dur=4.5, x=.75, y=.55, tam=440),
    peg("Una ganzúa que no se rompe", "ganzua", "Llave maestra", dur=4.0, x=.17, tam=420),
    ficha("No te da ninguna bonificación", "Llave maestra", "*Sin* bonificación. Y tu habilidad puede *no subir.*",
          origen="Error", rojo=True, dur=8.0),
    peg("Aunque Mercer Frey sí podía", "mercer", "Mercer Frey", dur=4.0, x=.17),
    ficha("las bendiciones de los Ruiseñores", "Lo que pierdes", "Las bendiciones de *Ruiseñor* y la misión *siguiente.*",
          origen="Si no la devuelves", dur=8.0),

    # ---- 12 · la estrella
    peg("encuentras una Estrella de Azura rota", "estrella_azura", "Estrella de Azura", dur=4.0, x=.17, tam=400),
    peg("Aranea Ienith", "aranea", "Aranea Ienith", dur=4.0, x=.17),
    peg("O Nelacar", "nelacar", "Nelacar", dur=4.0, x=.75, y=.55, tam=440),
    peg("a Malyn Varen", "malyn", "Malyn Varen", dur=4.0, x=.17),
    mg(T.balanza("¿A quién se la das?", ("Estrella de Azura", P("estrella_azura")),
                 [("Almas de personas: no", None), ("Aranea, seguidora", P("aranea")), ("Estrella Negra", P("estrella_negra")),
                  ("Admite cualquier alma", None)],
                 remate=("La diosa te da la peor", 4)),
       ("Con Aranea la Estrella de Azura", -.3), ("te premia con la peor versión|fin", .6),
       ["Con Aranea la Estrella", "Y Aranea como seguidora", "Con Nelacar la Estrella Negra", "admite cualquier alma",
        "Es mejor en todo"], "balanza estrella"),

    # ---- 11 · alma del dragón
    grande("Matas un dragón", "dragon", "El alma del dragón", dur=4.5, x=.75, tam=600),
    ficha("si en ese instante viajas", "Error", "Viaje rápido, caballo, cofre o charla: el alma *se pierde.*",
          origen="Al morir el dragón", rojo=True, dur=9.0),
    grande("Miraak puede aparecer", "miraak_db", "Miraak", dur=4.5, x=.25, tam=560),
    ficha("la ventaja Desintegrar", "Desintegrar", "Las cenizas se *hunden.* Sin huesos ni escamas.", origen="Error",
          rojo=True, dur=7.5),

    # ---- 10 · matones
    ficha("puede contratar matones", "Matones a sueldo", "Normalmente *tres.* Te esperan en el camino.",
          origen="Venganza", dur=7.0),
    peg("Basta con que el robo", "bandido", "Matón a sueldo", dur=4.0, x=.17),
    ficha("a veces los contrata un niño", "Error", "A veces los contrata un *niño.*", origen="Matones", rojo=True, dur=6.0),
    peg("un Corazón de espinas", "corazon_espinas", "Corazón de espinas", dur=4.5, x=.75, y=.55, tam=420),

    # ---- 9 · cárcel
    peg("la opción fácil es ir a la cárcel", "guardia", "Guardia", dur=4.0, x=.17),
    ficha("Cada condena te quita progreso", "Cárcel", "Pierdes *progreso* en tus habilidades. Los niveles, *no.*",
          origen="Condena", rojo=True, dur=10.0),
    ficha("te quitan todo lo robado", "Cofre de pruebas", "Lo robado, confiscado. Fugarte: *100* monedas.",
          origen="Cárcel", dur=9.0),

    # ---- 8 · Sanguine
    grande("un tal Sam Guevenne", "sam", "Sam Guevenne", dur=5.0, x=.75, tam=560),
    mapa("skyrim", [(.105, .49, "Markarth · templo de Dibella", "inicio", P("senna")), (.20, .50),
                    (.30, .49, "Paraje de Rorik · la cabra", "paso", P("ennis")), (.42, .52),
                    (.54, .51, "Carrera Blanca · el anillo", "paso", P("ysolda")), (.64, .54),
                    (.73, .51, "Arboleda · Moira", "peligro", P("cuervo_bruja")), (.70, .44, "Morvunskar", "meta", P("sanguine"))],
         de="Te despiertas en el Templo", a=("como en un cuento|fin", .8),
         marcas=["Templo de Dibella", "un granjero Ennis", "compraste un anillo", "Prometido con Moira", "Ysolda dice"],
         titulo="Skyrim", sub="La resaca de Sanguine", ajuste=1.0, traza=99),
    grande("en realidad es Sanguine", "sanguine", "Sanguine", dur=5.0, x=.25, tam=600),

    # ---- 7 · comerciante
    ficha("la mayoría de los comerciantes", "Comerciante", "No es esencial. Si muere, *para siempre.*", origen="PNJ",
          rojo=True, dur=8.0),
    peg("es de Lucano Valerio", "lucano", "Lucano Valerio", dur=4.0, x=.17),
    peg("su hermana Camila", "camilla", "Camila Valerio", dur=4.0, x=.75, y=.55, tam=420),
    ficha("la tienda se queda abandonada", "Comerciante de Cauce Boscoso", "Si mueren los dos: *abandonada* para siempre.",
          origen="Tienda", rojo=True, dur=8.0),

    # ---- 6 · Cicerón
    grande("conoces a Cicerón", "cicero", "Cicerón", dur=5.0, x=.75, tam=560),
    peg("cuida a la Madre Noche", "madre_noche", "Madre Noche", dur=3.5, x=.17, tam=380),
    ficha("puedes perdonarle la vida", "Si lo perdonas", "Vuelve como *guardián* de la Madre Noche y como *seguidor.*",
          origen="Cicerón", dur=9.0),
    peg("Sombra el caballo", "shadowmere", "Sombra", dur=4.0, x=.17, tam=440),
    peg("al espectro de Lucien Lachance", "lucien", "Lucien Lachance", dur=5.0, x=.75, y=.55, tam=420),

    # ---- 5 · gigante
    grande("Los gigantes de Skyrim no son", "gigante", "Gigante", dur=5.0, x=.75, tam=600),
    ficha("Un gigante es de nivel treinta y dos", "Gigante", "Nivel *32.* *591* de salud. Te mata de *un golpe.*",
          origen="Aunque bloquees", rojo=True, dur=9.0),
    peg("le atacas a los mamuts", "mamut", "Mamut · nivel 38", dur=4.5, x=.17, tam=420),
    grande("el garrote de un gigante", "garrote", "Garrote de gigante", dur=5.0, x=.25, tam=520),

    # ---- 4 · hombre lobo
    peg("Si te unes a los Compañeros", "aela", "Aela la Cazadora", dur=4.0, x=.17),
    grande("son mil monedas de recompensa", "hombre_lobo", "Hombre lobo", dur=5.0, x=.75, tam=600),
    ficha("son mil monedas de recompensa", "Transformación", "*1 000* monedas. Basta con que te *vean.*",
          origen="Recompensa", rojo=True, dur=9.0, x=.30),
    peg("el Señor de los vampiros", "senor_vampiro", "Señor de los vampiros", dur=4.5, x=.17, tam=420),
    grande("M'aiq el Mentiroso", "maiq", "M'aiq el Mentiroso", dur=4.5, x=.75, tam=520),

    # ---- 3 · Sanguinare Vampiris
    ficha("hay un diez por ciento", "Sanguinare Vampiris", "*10 %* de contagio. De entrada, *-25* de salud.",
          origen="Enfermedad", dur=8.0),
    mg(_plazo_vampiro(), ("Pero si en tres días no te curas", -.4), ("Una sola|fin", .8),
       ["Pero si en tres días", "Antes de esos tres días"], "plazo vampiro"),
    peg("con un mago llamado Falion", "falion", "Falion · Morthal", dur=4.5, x=.17, tam=420),
    ficha("Al sol en la peor etapa", "Vampiro al sol", "*-60* de salud, magia y aguante. Regeneración *0.*",
          origen="Etapa 4", rojo=True, dur=9.0),

    # ---- 2 · subir sin pelear
    mg(_escalado(), ("Y sin darte cuenta", -.3), ("Subir demasiado|fin", 1.6),
       ["Y sin darte cuenta", "sin haber blandido", "Los dragones de escarcha", "los dragones legendarios",
        "Subir demasiado"], "escalado"),
    ficha("Los enemigos se vuelven demasiado duros", "Aviso de UESP", "Subir demasiado sin combate *rompe* el juego.",
          origen="Nivel", rojo=True, dur=7.0),

    # ---- 1 · cofres
    mg(_reinicio(), ("Vacías la mochila", -.2), ("Y las estanterías de libros|fin", .2),
       ["en un barril", "el cofre de una cueva", "en un saco", "tan tranquilo", "Pero en Skyrim casi", "su estado original",
        "una mazmorra que ya despejaste", "los cofres de los comerciantes", "Pasados diez días", "Y lo que dejaste dentro",
        "Los únicos contenedores seguros", "Lo de fuera de la casa"], "reinicio"),
    ficha("En una mazmorra que ya despejaste", "Reinicio", "*10* días. *30* si la despejaste. Comerciantes: *2.*",
          origen="Contenedores", dur=8.0, y=.80),
    ficha("Si les metes demasiados", "Error", "Demasiados libros: los *pierdes todos.*", origen="Estanterías",
          rojo=True, dur=7.0),
    ficha("En una pantalla de carga", "Pantalla de carga", "Lo que guardes fuera de casa *puede no estar* después.",
          origen="El juego te avisa", dur=9.0),

    # ---- cierre
    peg("con lo de Lydia y la bola de fuego", "lydia", "Lydia", dur=4.0, x=.17),
    ficha("los ocho exploits más ROTOS", "Los 8 exploits más ROTOS de Skyrim", "Ya está en el canal.",
          origen="Video recomendado", dur=6.0, x=.5, y=.40),
    peg("dejes algo en un barril", "barril", "Piénsalo dos veces", dur=4.0, x=.25, y=.55, tam=420),
]

SFX = {
    "aviso_e": ("Deep nordic war drum hit followed by a short low horn call, fantasy quest notification", 3),
    "aviso_f": ("Low dramatic choir swell with a soft metallic shimmer, fantasy warning notification", 3),
    "gallina": ("Single startled chicken squawk and wing flaps, farm animal", 2),
    "fus": ("Powerful dragon shout shockwave, deep booming voice blast with rushing wind, fantasy", 2),
    "fuego": ("Fireball spell whoosh and explosion, fantasy magic", 2),
    "cofre_vacio": ("Old wooden chest lid creaking open then hollow empty thud, eerie wind", 1),
}
_AV = ["aquí van las veinte cosas", "Número veinte", "En el diecinueve", "Número dieciocho", "En el diecisiete",
       "Número dieciséis", "En el quince", "Número catorce", "En el trece", "Número doce", "En el once", "Número diez",
       "En el nueve", "Número ocho", "En el siete", "Número seis", "En el cinco", "Número cuatro", "En el tres", "Número dos",
       "llegamos al número uno"]
PISTAS = [dict(sfx="aviso_e" if k % 2 == 0 else "aviso_f", en=a, vol=.6 if k in (0, 20) else .5) for k, a in enumerate(_AV)] + [
    dict(sfx="gallina", en="la propia gallina podía denunciarte", vol=.45),
    dict(sfx="fus", en="el famoso Fus Ro Dah", vol=.45),
    dict(sfx="fuego", en="Una bola de fuego en un pasillo", vol=.45),
    dict(sfx="cofre_vacio", en="Y lo que dejaste dentro desaparece", vol=.5),
]

# Hojas de prueba de los MG nuevos (python _prueba_mg.py): (nombre, fn, marcas, tiempos)
PRUEBAS = [
    ("plazo_lydia", _plazo_lydia(), [0.5, 6], [0.3, 2, 4, 6.2, 7, 8.5]),
    ("plazo_vampiro", _plazo_vampiro(), [0.5, 8], [0.3, 3, 5.5, 8.2, 9, 10.5]),
    ("paciencia", _paciencia(), [0.5, 2, 3.5, 5, 7], [0.3, 0.7, 2.2, 3.7, 5.3, 7.5]),
    ("escalado", _escalado(), [0.5, 5, 6, 7.5, 9], [0.3, 2, 4, 6.2, 7.8, 9.5]),
    ("reinicio", _reinicio(), [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 8, 10, 11.5], [1, 4.4, 6.5, 8.3, 9.4, 12]),
]
