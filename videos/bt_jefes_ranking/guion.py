# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Los 10 JEFES de Banjo-Tooie, del PEOR al MEJOR» (5-nov-2026, ~25 min).
Pedido del usuario: «otro video de Banjo-Tooie, un top largo de 25 minutos»; eligió JEFES entre 3 con datos (jefes / 40 cambios /
transformaciones). Quinto video de Banjo-Tooie del canal; variable que cambia respecto a bt_mundos_ranking: SOLO el sujeto
(jefes en vez de mundos). Ranking = media de 7 listas (investigacion_jefes.md § 1). Klungo y los dragones cuentan como un puesto.
Motor SECUENCIA YT, voz ElevenLabs Hope, OST del juego (audio/ost + audio/ost_extra: vs_coal, vs_woo, vs_weldar), SFX del juego,
kit mg_banjo (+ vida_jefe, escalera, mira, nuevos de este guion). Nada de lo YA USADO en banjo_tooie, bt_jiggies_crueles,
bt_mundos_ranking ni bt_50_secretos (lista en bt_50_secretos/investigacion_secretos.md).
⚠ dichos con «según…»: Terry macho (wiki/manual), Mingy «muere de verdad» (wiki), «Juanetes» (traducción al español).
NO decir: «voz de Mel Blanc» (Terry); que «How about a few nuts 'n' bolts?» anuncia Nuts & Bolts; que Mr. Patch es el ÚNICO tema
de Tooie del álbum de Rare (solo «está»).
Sonidos nombrados (regla del 31-oct): p06 risa/saludo de Klungo (clip con ambiente), p04 tema de Mr. Patch y p03 tema de Mingy
(SUBE_DB en armar_musica_ost.py), p01 electricidad de Weldar (clip con ambiente): cada uno con `post` y la voz callada.
"""

TITULO = "Los 10 JEFES de Banjo-Tooie, del PEOR al MEJOR"
ARCHIVO = "bt_jefes_ranking"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
# Voz del canal (Hope) con el modelo turbo. Sin [whispers] ni [excited] (el usuario, 2-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"))
# ElevenLabs dice el inglés nativo; solo lo que leería mal
# 5-nov: falsas alarmas de Whisper (cifras en dígitos, Kazui, Hellfire, Clungo, Welder…), comparadas palabra a palabra
# con textos.json: se aceptan con la CER de la toma + .0015; tail > 1 = hablan hasta el final y la transcripción termina bien
CER_MAX_POR_FRASE = {"fuera_1": 0.0555, "mitad_0": 0.0695, "cierre_0": 0.0314, "critica_1": 0.0145, "intro_0": 0.0106, "metodo_1": 0.0189, "metodo_2": 0.0211, "p01_0": 0.0293, "p01b_3": 0.0295, "p02_10": 0.0234, "p02_2": 0.0511, "p02_6": 0.0141, "p02_8": 0.0241, "p03_0": 0.0228, "p03_6": 0.0311, "p04_1": 0.0216, "p04_4": 0.0218, "p05_0": 0.0383, "p05_1": 0.0303, "p05_2": 0.0303, "p05_5": 0.0189, "p05_6": 0.0156, "p05_8": 0.029, "p06_0": 0.0229, "p06b_4": 0.0083, "p06b_5": 0.0165, "p06b_7": 0.0015, "p07_0": 0.0165, "p07_8": 0.0244, "p08_0": 0.0213, "p08_2": 0.0246, "p08_3": 0.0244, "p08_4": 0.0226, "p09_9": 0.0199, "p10_1": 0.0375, "p10_4": 0.0223}
TAIL_MAX_POR_FRASE = {"p06b_8": 1.12, "intro_0": 1.15, "p01_0": 1.06, "p02_10": 1.08, "p06b_4": 1.04, "p06b_7": 1.11}
FONETICA = {"Hag 1": "Hag One", "3D": "tres de", "Nuts & Bolts": "Nuts and Bolts", "McJiggy's": "Mac Jiggys"}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,           # ambiente_por = beats donde se OYE el juego (regla del 26-oct); lo rellena plan_clips.py
    ambiente_por={'scene-038': 0.7, 'scene-049': 0.7, 'scene-065': 0.7, 'scene-075': 0.9, 'scene-076': 0.9, 'scene-084': 0.7, 'scene-119': 0.6, 'scene-135': 0.6, 'scene-144': 0.8, 'scene-145': 0.8, 'scene-157': 0.9, 'scene-158': 0.9},   # plan_clips.py (5-nov): 075/076 saludo de Klungo, 157/158 suelo eléctrico de Weldar
    recorte_por={'scene-001': (0, 0, 0, 0.075), 'scene-002': (0, 0, 0, 0.075), 'scene-003': (0, 0, 0, 0.075), 'scene-004': (0, 0, 0, 0.075), 'scene-006': (0, 0, 0, 0.075), 'scene-008': (0, 0, 0, 0.075), 'scene-009': (0, 0, 0, 0.075), 'scene-010': (0, 0, 0, 0.075), 'scene-011': (0, 0, 0, 0.075), 'scene-012': (0, 0, 0, 0.075), 'scene-013': (0, 0, 0, 0.075), 'scene-014': (0, 0, 0, 0.075), 'scene-015': (0, 0, 0, 0.075), 'scene-016': (0, 0, 0, 0.075), 'scene-017': (0, 0, 0, 0.075), 'scene-018': (0, 0, 0, 0.075), 'scene-019': (0, 0, 0, 0.075), 'scene-020': (0, 0, 0, 0.075), 'scene-021': (0, 0, 0, 0.075), 'scene-023': (0, 0, 0, 0.075), 'scene-024': (0, 0, 0, 0.075), 'scene-026': (0, 0, 0, 0.075), 'scene-029': (0, 0, 0, 0.075), 'scene-030': (0, 0, 0, 0.075), 'scene-031': (0, 0, 0, 0.075), 'scene-032': (0, 0, 0, 0.075), 'scene-033': (0, 0, 0, 0.075), 'scene-034': (0, 0, 0, 0.075), 'scene-035': (0, 0, 0, 0.075), 'scene-036': (0, 0, 0, 0.075), 'scene-037': (0, 0, 0, 0.075), 'scene-038': (0, 0, 0, 0.075), 'scene-039': (0, 0, 0, 0.075), 'scene-041': (0, 0, 0, 0.075), 'scene-042': (0, 0, 0, 0.075), 'scene-043': (0, 0, 0, 0.075), 'scene-044': (0, 0, 0, 0.075), 'scene-046': (0, 0, 0, 0.075), 'scene-047': (0, 0, 0, 0.075), 'scene-048': (0, 0, 0, 0.075), 'scene-049': (0, 0, 0, 0.075), 'scene-050': (0, 0, 0, 0.075), 'scene-051': (0, 0, 0, 0.075), 'scene-053': (0, 0, 0, 0.075), 'scene-054': (0, 0, 0, 0.075), 'scene-056': 0.144, 'scene-057': 0.144, 'scene-062': (0, 0, 0, 0.075), 'scene-063': (0, 0, 0, 0.075), 'scene-064': (0, 0, 0, 0.075), 'scene-065': (0, 0, 0, 0.075), 'scene-066': (0, 0, 0, 0.075), 'scene-067': (0, 0, 0, 0.075), 'scene-068': (0, 0, 0, 0.075), 'scene-069': (0, 0, 0, 0.075), 'scene-070': (0, 0, 0, 0.075), 'scene-071': (0, 0.08, 0, 0.18), 'scene-072': (0, 0, 0, 0.075), 'scene-073': (0, 0, 0, 0.075), 'scene-074': (0, 0, 0, 0.075), 'scene-075': (0, 0, 0, 0.075), 'scene-076': (0, 0, 0, 0.075), 'scene-077': (0, 0, 0, 0.075), 'scene-078': (0, 0, 0, 0.075), 'scene-079': (0, 0.1, 0, 0), 'scene-080': (0, 0, 0, 0.075), 'scene-081': (0, 0, 0, 0.075), 'scene-082': (0, 0, 0, 0.075), 'scene-083': (0, 0, 0, 0.075), 'scene-084': (0, 0, 0, 0.075), 'scene-085': (0, 0, 0, 0.075), 'scene-086': (0, 0, 0, 0.075), 'scene-087': (0, 0.1, 0, 0), 'scene-088': (0, 0, 0, 0.075), 'scene-092': (0, 0, 0, 0.075), 'scene-093': (0, 0, 0, 0.075), 'scene-094': (0, 0, 0, 0.075), 'scene-095': (0, 0, 0, 0.075), 'scene-096': (0, 0, 0, 0.075), 'scene-097': (0, 0, 0, 0.075), 'scene-098': (0, 0, 0, 0.075), 'scene-099': (0, 0, 0, 0.075), 'scene-100': (0, 0, 0, 0.075), 'scene-101': (0, 0, 0, 0.075), 'scene-102': (0, 0, 0, 0.075), 'scene-103': (0, 0, 0, 0.075), 'scene-104': (0, 0, 0, 0.075), 'scene-105': (0, 0, 0, 0.075), 'scene-106': (0, 0, 0, 0.075), 'scene-107': (0, 0, 0, 0.075), 'scene-108': (0, 0, 0, 0.075), 'scene-109': (0, 0, 0, 0.075), 'scene-110': (0, 0, 0, 0.075), 'scene-111': (0, 0, 0, 0.075), 'scene-112': (0, 0, 0, 0.075), 'scene-113': (0, 0, 0, 0.075), 'scene-114': (0, 0, 0, 0.075), 'scene-115': (0, 0, 0, 0.075), 'scene-116': (0, 0, 0, 0.075), 'scene-118': (0, 0.08, 0, 0.18), 'scene-119': (0, 0, 0, 0.075), 'scene-122': (0, 0, 0, 0.075), 'scene-125': (0, 0, 0, 0.075), 'scene-127': (0, 0, 0, 0.075), 'scene-128': (0, 0, 0, 0.075), 'scene-129': (0, 0, 0, 0.075), 'scene-130': (0, 0, 0, 0.075), 'scene-131': (0, 0, 0, 0.075), 'scene-132': (0, 0, 0, 0.075), 'scene-134': (0, 0, 0, 0.075), 'scene-135': (0, 0, 0, 0.075), 'scene-136': (0, 0, 0, 0.075), 'scene-137': (0, 0, 0, 0.075), 'scene-138': (0, 0, 0, 0.075), 'scene-139': (0, 0, 0, 0.075), 'scene-140': (0, 0, 0, 0.075), 'scene-141': (0, 0, 0, 0.075), 'scene-142': (0, 0, 0, 0.075), 'scene-143': (0, 0, 0, 0.075), 'scene-144': (0, 0, 0, 0.075), 'scene-145': (0, 0, 0, 0.075), 'scene-146': (0, 0, 0, 0.075), 'scene-147': (0, 0, 0, 0.075), 'scene-148': (0, 0, 0, 0.075), 'scene-149': (0, 0, 0, 0.075), 'scene-150': (0, 0, 0, 0.075), 'scene-151': (0, 0, 0, 0.075), 'scene-153': (0, 0, 0, 0.075), 'scene-154': (0, 0, 0, 0.075), 'scene-155': (0, 0, 0, 0.075), 'scene-156': (0, 0, 0, 0.075), 'scene-157': (0, 0, 0, 0.075), 'scene-158': (0, 0, 0, 0.075), 'scene-163': (0, 0, 0, 0.075), 'scene-164': (0, 0, 0, 0.075), 'scene-165': (0, 0, 0, 0.075), 'scene-166': (0, 0, 0, 0.075), 'scene-167': (0, 0, 0, 0.075), 'scene-168': (0, 0, 0, 0.075), 'scene-169': (0, 0, 0, 0.075)},   # PROS sin la marca de abajo; P01 marco NSO; Smash y XBLA sin rótulos
    yt=dict(sufijo="", min_s=15, max_min=1100, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora del juego (armar_musica_ost.py -> audio/musica.wav).

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Tres jefes de Banjo-Tooie casi no existen. Uno iba a ser una roca. Otro, unos engranajes llamados The Kogs. [short pause] Y el tercero, una avispa gigante.",
        "[amused] Hay un tótem que se autodestruye y sigue hablando. Un pez que, después de morir, te pide que dejes de dispararle. [short pause] Y un dragón que te confunde con el repartidor de pizza.",
        "Un rey de carbón que pierde los dos brazos y sigue diciendo que va ganando. Y un robot que se hace pasar por tu mejor amigo.",
        "[sarcastic] Ya te contamos la historia de Banjo-Tooie, sus Jiggies más crueles, sus ocho mundos y cincuenta secretos. Creías que estaba todo. [short pause] Faltaban ellos.",
        "[playful] Estos son los diez jefes de Banjo-Tooie, del peor al mejor. Y el número uno ni siquiera estaba en los planes de Rare.",
    ]},
    {"id": "metodo", "frases": [
        "Para que no sea solo nuestra opinión, juntamos siete rankings de jugadores y creadores de contenido, y sacamos la media de cada jefe.",
        "Están Easy Geek, Super Joe Bros, que trae dos, la suya y la de su chat, ivanavi, Acute-Dilute, MABUS y WatchMojo. Cada jefe tiene su nota en cada lista.",
        "Klungo, al que peleas tres veces, cuenta como uno. Los dos dragones de Hailfire Peaks, también. [short pause] Quedan diez. Empezamos por abajo.",
    ]},

    # ================================================================ 10 · TERRY
    {"id": "p10", "frases": [
        "Número diez. Terry, en Terrydactyland. Un pterodáctilo gigante que vive en un nido, en la cima de la montaña, y que te recibe a escupitajos mientras subes.",
        "[deadpan] Te acusa de robarle los huevos. Kazooie, con la delicadeza de siempre, le contesta que da igual, que su especie está a punto de extinguirse.",
        "Tiene treinta de vida. Escupe desde lo alto, y no apunta a donde estás, sino a donde vas a estar. Si corres en círculo, falla.",
        "Cuando se cansa, suelta en el nido unos mocos con vida, los Mucoids, y se esconde bajo las nubes. Los rompes rodando, le disparas huevos, y vuelta a empezar.",
        "Por el nombre sería un pteranodon, y así lo llama la versión japonesa. Pero los pteranodon no tenían dientes. [short pause] Y Terry, sí.",
        "¿Por qué está el último? Porque cada vez que escupe, la cámara salta a una vista desde arriba y te quita el control. Las listas lo repiten: el personaje es interesante, la pelea no tanto.",
        "[sighs] Y aquí nos toca corregir algo. En nuestro ranking de mundos lo llamamos «la jefa». [short pause] Según la wiki de Banjo, que cita el manual, Terry es macho, y padre soltero: su esposa lo dejó antes del juego.",
        "[amused] Perdón, Terry. Ya tenías bastante. Al final, cuando descubre que tú no tenías sus huevos, se disculpa por haber sido tan bruto. Y Kazooie le contesta que ella lo disfrutó.",
        "Luego te pide que le devuelvas a sus crías. La última es tan gorda que hay que llevarla en el Taxi Pack, y Terry duda de que quepa en el nido: «¿No podrías darle con un huevo granada?». Kazooie lo llama desalmado. [short pause] «Es broma».",
        "En el documento de diseño de Rare, de enero de mil novecientos noventa y nueve, Terry iba a dar vueltas volando por debajo del borde del nido mientras te atacaban los mocos.",
        "Y en ese primer plan, Terrydactyland no era el sexto mundo del juego. Era el primero, en el sitio que acabó ocupando Mayahem Temple.",
        "Según la wiki, además, es el único jefe que no acaba destruido ni derrotado del todo: puedes volver a su nido cuando quieras, y ahí sigue.",
    ]},

    # ================================================================ 9 · OLD KING COAL
    {"id": "p09", "frases": [
        "Número nueve. Old King Coal, en Glitter Gulch Mine. Un rey hecho de carbón que vive dentro de la caldera del tren, Chuffy.",
        "Si intentas usar el tren antes de tiempo, la caldera te habla, y te avisa de que primero tienes que pelear con él.",
        "Tiene cincuenta de vida, la segunda cifra más alta del juego, solo por detrás del jefe final. Y no tiene punto débil: casi todo le hace daño.",
        "Casi. Los huevos de fuego no le hacen nada, que para eso es carbón. Los de hielo, en cambio, le quitan más.",
        "[amused] Lo mejor es cómo pierde. Primero se le cae el brazo izquierdo, y dice que no pasa nada, que tiene otro. Luego el derecho, y dice que no necesita brazos. [short pause] Luego la mitad de arriba. Y ahí ya propone sentarse a hablar.",
        "Mientras tanto, la caldera se calienta: el suelo se pone al rojo y el humo te ahoga. Te salvas subiéndote a los trozos grandes de su propio cuerpo, donde no te alcanza.",
        "¿Por qué el noveno? Porque es el más fácil del juego. Subido a una plataforma, no te puede tocar. Super Joe Bros le pone buena nota… por el esfuerzo.",
        "Y casi ni existe. En la primera lista de mundos de Rare, el jefe de la mina era «Boss Boulder». [short pause] Una roca.",
        "Su entrada también iba a ser otra: muchos trozos de carbón juntándose, uno a uno, para formar su cuerpo. Rare se quedó con la opción B, salir del carbón de golpe, porque era menos exigente para la consola.",
        "En alemán se llama Briketto Blanko, un chiste con el nombre del cantante Roberto Blanco. Y la wiki lo compara con el Caballero Negro de Monty Python, el que pierde los brazos y dice que solo es un rasguño.",
        "En Xbox 360, el logro por vencerlo se llama «A Merry Old Soul», como la canción infantil del rey alegre. Él jura que no es ese rey. Su pie, en cambio, sí te va a alegrar la cabeza.",
        "Y otro dato de los archivos de Rare: probaron que un segundo jugador controlara a un jefe con el mando. Lo quitaron, porque así nadie podía ganarle.",
    ]},

    # ================================================================ 8 · TARGITZAN
    {"id": "p08", "frases": [
        "Número ocho. Targitzan, en Mayahem Temple. El dios maya del tiro al blanco: un tótem que gira sobre sí mismo, cubierto de dianas.",
        "La traducción al español lo llamó Apuntzan, de apuntar. Y su título completo es todavía mejor: Despótico Dios Tótem Mareado.",
        "Para llegar a él necesitas veinte estatuas de jade, y el Breegull Blaster, el modo en que Kazooie se convierte en arma, porque toda la pelea es en primera persona.",
        "Tiene dieciséis de vida: cuatro pisos, con cuatro dianas cada uno. Cada piso que rompes lo hace más bajo, suelta más Moggies, y le salen más caras que escupen dardos.",
        "Cuando pierde el piso de abajo grita que ya no siente las piernas, y le ordena a sus Moggies inútiles que vayan a por ti.",
        "Las losas donde te cubres se rompen y no vuelven. Y cuando cae el último piso, invoca su autodestrucción sagrada, y explota durante tres segundos.",
        "¿Por qué el octavo? Porque te exige dominar el apuntado en primera persona en el primer mundo. Para una de las listas es un tiro al blanco sin cerebro… con una pinta y una música increíbles.",
        "[amused] Detalle: se autodestruye. Pero si vuelves a su templo convertido en Mumbo, el tótem sigue ahí, diciéndote que solo pueden entrar Banjo y Kazooie. Es un dios. Morirse no le quita el trabajo.",
        "Sus ojos son joyas, así que no tiene animación de parpadeo. Y el Jiggy que corona su cabeza no se alcanza nunca, salvo con un glitch y un Kazooie de cuerda.",
        "Años después, en Nuts and Bolts, volvió como una estatua dorada en Banjoland… que escupe balones de fútbol.",
    ]},

    # ================================================================ comentarios: agradecimientos
    {"id": "gracias", "frases": [
        "Antes de seguir, unos comentarios. riuma77 escribió en el video de los Jiggies: «Qué videojuego más interesante, solo pude disfrutar del primero».",
        "Y en el de Rare dijo que es una pena que Nintendo se desligara, porque le habría gustado ver más Banjo y más Conker en las consolas siguientes. Nos pasa igual.",
        "antilopezmexicanos dejó en Majora's Mask una de las mejores lecturas del héroe del tiempo que hemos visto: que su destino terrible nunca fue la luna, sino salvar Hyrule y perderlo todo.",
        "Y riuma77, otra vez, nos contó que nunca consiguió la máscara de la Fiera Deidad. [short pause] Gracias, de verdad. Todos los comentarios se leen, y muchos acaban cambiando el siguiente video.",
    ]},

    # ================================================================ 7 · LORD WOO FAK FAK
    {"id": "p07", "frases": [
        "Número siete. Lord Woo Fak Fak, en Jolly Roger's Lagoon. Un pez abisal gigante que vive en el fondo del mar, en el cofre de Davy Jones, y que se queja de lo apretado que está.",
        "En español, Pez Linterna de Gran Autoestima. Banjo intenta salir del paso diciéndole que le traen el correo. No cuela.",
        "En la primera fase tiene seis forúnculos en el cuerpo, y solo puedes reventar el que parpadea. Él te dispara con la luz de su antena… con los ojos cerrados.",
        "En la segunda fase abre los ojos, y hay que darle tres veces en cada uno, mientras te lanza burbujas que te dejan atrapado.",
        "Al caer, se despide de sus cien años de tiranía oceánica, con un final, dice, nada digno. Por cierto: en la vida real, solo las hembras de este pez tienen farol. Y él es lord.",
        "[deadpan] Y cuando revientan los forúnculos, sale sangre roja. En un juego para todas las edades. Super Joe Bros todavía se pregunta cómo consiguieron colarlo.",
        "¿Por qué el séptimo? Porque nadar y apuntar en primera persona en una sala estrecha es torpe, y cuesta no perderlo de vista. Convertido en submarino es más fácil, pero no todos lo saben.",
        "[amused] Lo mejor viene después. Si le sigues disparando cuando ya ganaste, protesta: «¡Deja de dispararme! Estoy muerto, y no tengo más Jiggies». Si insistes, te dice que conoce a tu padre.",
        "Su tema es un arreglo dramático de la música del fondo del mar, y está en Super Smash Bros. Ultimate, en su versión original. En Japón, por cierto, se llama Rey Woohaha.",
        "Según la wiki, el rey Jingaling se va de pesca con él. Pero te pide que no se lo cuentes a nadie.",
    ]},

    # ================================================================ 6 · KLUNGO
    {"id": "p06", "post": 2.6, "frases": [
        "Número seis. Klungo, el secuaz de Grunty, y el único jefe al que peleas tres veces: dos en los túneles de Isle O' Hags, y la última en la entrada de Cauldron Keep, donde cae del techo.",
        "Escucha cómo te saluda antes de cada pelea.",
    ]},
    {"id": "p06b", "frases": [
        "En cada pelea son tres golpes. Tras cada uno se protege con un escudo, te lanza pociones, y se bebe una distinta.",
        "La roja lo vuelve gigante, y salta para aplastarte. La verde lo hace invisible. Y la azul lo multiplica: dos, tres, cuatro Klungos. El de verdad es el que se mueve el último, y tiene la nariz más clara.",
        "En Nintendo 64, qué poción toca en cada pelea es aleatorio. En Xbox 360, en cambio, siempre van en el mismo orden: roja, verde y azul.",
        "¿Por qué en medio de la tabla? Porque las tres peleas son fáciles, pero el personaje es imposible de olvidar. Ninguna lista lo sube ni lo baja: todas lo dejan justo aquí.",
        "[amused] Y aun así, un canal, Jiggylookback, enfrentó a todos los jefes con estadísticas, en un todos contra todos. ¿El ganador? No fue Grunty. No fue Weldar. [short pause] Fue Klungo. Inteligencia, cinco de cinco.",
        "Tras la tercera derrota se lamenta de que cada vez está menos guapo, y de que ahora la señora Klungo ya no lo querrá. [short pause] Sí: existe una señora Klungo. Solo la nombra esa vez.",
        "Y un detalle que casi nadie vio: en la escena del principio del juego hay un segundo Klungo, sin texturas, que camina hacia una roca y desaparece.",
        "Y su voz, según la wiki, son grabaciones de los Gruntlings, los secuaces pequeños de Grunty, ralentizadas.",
        "En Xbox 360 hasta tiene logro propio: Knocked Out Klungo, por tumbarlo tres veces. Y al final de la historia, en la fiesta de Bottles, Klungo se come toda la comida. Se lo había ganado.",
    ]},

    # ================================================================ crítica (burla disfrazada)
    {"id": "critica", "frases": [
        "Y ahora, una pregunta del público. JaVik0 vio nuestro video de Majora's Mask, el que se llama «su historia y los doce secretos», y escribió: «¿Y los secretos?».",
        "[sarcastic] Excelente pregunta, JaVik0. Estaban ahí, los doce, con su número en pantalla. Pero lo entendemos: en Majora's Mask el tiempo se acaba en tres días, y a lo mejor la luna te cayó antes del primero.",
        "[playful] Hoy no hay riesgo. Estos son jefes, y los jefes no se esconden: te esperan al final del pasillo, con su barra de vida y todo.",
    ]},

    {"id": "mitad", "frases": [
        "[playful] Vamos por la mitad. Abajo quedaron Terry, Old King Coal, Targitzan, Lord Woo Fak Fak y Klungo.",
        "Arriba quedan cinco. Y entre ellos hay dos dragones, un globo con parches, un traidor, un tanque y un soplete.",
    ]},

    # ================================================================ 5 · CHILLI BILLI Y CHILLY WILLY
    {"id": "p05", "frases": [
        "Número cinco. Chilli Billi y Chilly Willy, en Hailfire Peaks. Dos dragones hermanos, de cuello larguísimo y cuerpecito ridículo: el rojo vive en el cráter del volcán, y el azul, en el lago helado de la cima.",
        "Al verte, cada uno cree que eres el repartidor de pizza. Billi había pedido una de carne picante de doce pies. Willy, una de anchoas.",
        "Kazooie le contesta al rojo con un «me temo que no, cara de verruga». Y el dragón decide que, si no hay pizza, se come a los repartidores.",
        "Se les hace daño con el huevo contrario: hielo al de fuego, y fuego al de hielo. Y hay que meterlo por dentro de unos cañones gigantes, que te sirven de escudo hasta que revientan.",
        "Cuando bajan los cañones, te barren con la lengua. Y el de hielo, además, puede tirarte de la plataforma: muerte instantánea.",
        "Un detalle raro: no importa el orden. El primero que enfrentes tiene seis de vida, y el segundo, doce. Y los dos juntos dan un solo Jiggy: cuando Kazooie pide un trofeo, el segundo dragón le dice que es lo único que tiene.",
        "¿Y por qué son dos? Porque Hailfire Peaks eran dos mundos. En la lista temprana de Rare había unas cuevas de hielo y una isla de lava. Al fundirlas en una montaña, el jefe se duplicó.",
        "¿Por qué el quinto? Es el puesto más dividido de todos: diseño genial, pelea plana y repetida. Una lista los pone entre los mejores. Otra se queja de que deberías pelear contra los dos a la vez.",
        "[amused] Al irse volando, uno anuncia que va a por un par de hamburguesas de Big Al. El otro pregunta por dónde queda el autoservicio de McJiggy's.",
        "Chilly Willy, por cierto, se llama igual que el pingüino de los dibujos animados.",
    ]},

    # ================================================================ 4 · MR. PATCH
    {"id": "p04", "post": 3.2, "frases": [
        "Número cuatro. Mr. Patch, en Witchyworld. Un dinosaurio inflable cubierto de parches, que vive dentro de la carpa del circo.",
        "En español, Señor Parche, Cosa Inflable, Extraña e Inestable. Se presenta presumiendo de lo grande y fuerte que es. Kazooie le responde que Klungo, al principio del juego, era más grande.",
        "Tiene doce parches, y solo los huevos granada los revientan. Tras el primero, la pelea sube al aire: vuelas, apuntas, y esquivas pelotas de playa explosivas.",
        "Y cada parche que revientas lo hace más pequeño… y más rápido.",
        "Cuando lo intentas con huevos normales, se ríe de ti: así nunca le vas a ganar. En la revancha te pide calma, porque él no es un inflable violento. Kazooie le dice que solo es aire caliente.",
        "¿Por qué el cuarto? Es el favorito del público, pero volar y apuntar a la vez frustra a muchos. Una de las listas lo bajó, según dijo, con un nudo en el estómago.",
        "Su documento de diseño, de octubre de mil novecientos noventa y ocho, traía otras ideas: globos teledirigidos que al reventar soltaban granadas, y un solo punto de vuelo en el centro. Hoy hay cuatro.",
        "Y volvió años después, en Nuts and Bolts: encadenado en Nutty Acres, y en Banjoland, de metal y sin un solo parche.",
        "Además, está en Super Smash Bros. Ultimate. Y cuando Rare cumplió treinta y cinco años, en dos mil veinte, publicó un álbum oficial con su música. Entre sus pistas, la de Mr. Patch. Escúchala.",
    ]},

    {"id": "fuera", "frases": [
        "Antes del podio, los que se quedaron fuera. En Banjo-Tooie, Conga ya no pelea: solo vigila la puerta de la carpa del circo.",
        "Los Zubbas no son jefes: son un minijuego, en el que disparas convertido en abeja. Y los Uggers son solo los secuaces que salen de la Hag 1.",
        "[amused] Y el jefe que nunca llegó. En los primeros planes de Rare, Cloud Cuckooland se llamaba Mushroomland, y su jefe era una avispa gigante.",
        "Ahora sí. Quedan tres. [short pause] El podio.",
    ]},

    # ================================================================ 3 · MINGY JONGO
    {"id": "p03", "post": 3.2, "frases": [
        "Número tres. Mingy Jongo, en Cloud Cuckooland. [short pause] La traición.",
        "En ese mundo hay dos calaveras de Mumbo. En una está tu amigo. En la otra, un robot disfrazado de él. Cuál es cuál se sortea en cada partida.",
        "Hay pistas: la falsa tiene las antorchas apagadas, y en el primer piso, un Jinjo en vez de un Minjo. Además, el robot te saluda «Hola, Banjo», cuando el Mumbo de verdad casi siempre te llama oso.",
        "Al acercarte, te fulmina en plena escena y te quita un panal. Si entras con uno solo, mueres antes de que empiece la pelea.",
        "Tiene ocho de vida. Te dispara magia que te persigue, desde la mitad se teletransporta, y cada golpe le arranca un trozo del disfraz y deja ver el metal.",
        "Con el primero se lamenta: su elaborado disfraz está arruinado, y deja ver su malvada naturaleza cibernética. Antes ya te había avisado de que no hay escapatoria, y de que la resistencia es inútil.",
        "¿Por qué el tercero? Por el giro. Que el chamán que te ayuda todo el juego te dispare es el momento que más recuerda la gente. Para una de las listas, es el mejor jefe de Tooie.",
        "Rare iba a ponerle ojos rojos con el disfraz, para insinuar que era malo, y un látigo eléctrico. Le quitó los ojos para que la sorpresa fuera el ataque.",
        "Según la wiki, es el único jefe del juego que muere de verdad: explota, y suelta un líquido verde.",
        "Y su música es la única que no sale de su mundo. Es el tema de Mumbo, vuelto en tu contra. Escucha.",
    ]},

    # ================================================================ 2 · HAG 1
    {"id": "p02", "frases": [
        "Número dos. La Hag 1, en lo alto de Cauldron Keep. El tanque perforador de las hermanas, con Gruntilda al volante.",
        "Tiene cien de vida, el doble que cualquier otro, y solo le haces daño cuando Grunty asoma la cabeza, en primera persona.",
        "Son diez fases: láseres, el doble de láseres, mortero, doble mortero y el taladro. A la mitad metes un Kazooie de cuerda por el tubo de escape para volar una batería. Luego, la otra.",
        "Sin tanque, Grunty pelea con magia, manda a sus Uggers, te echa gas tóxico, y al final prepara su hechizo más fuerte. Le das con un huevo mientras lo sostiene… y se le cae.",
        "Entre fase y fase te hace preguntas, con cinco segundos para contestar. Si aciertas, ataca más lento. Si fallas, más rápido.",
        "[amused] Y habla sin parar. En la primera fase no encuentra el botón del láser, y pide que alguien le pase el manual. Cuando pierde las baterías, pide que llamen a una grúa.",
        "Y en un descuido se le escapa su apellido: Gruntilda Winkybunion. En la traducción al español, Gruntilda Juanetes. [short pause] Al momento, amenaza con demandarte si se lo cuentas a alguien. Lo sentimos, Grunty.",
        "¿Por qué no es la primera? Por larga. Las listas se quejan de las cámaras que te hacen mirar al lado equivocado. Pero en espectáculo, ninguna pelea del juego le gana.",
        "Y no iba a ser así. En el plan original del castillo subías la torre peleando contra las hermanas, Mingella y Blobbelda, una por una, antes de llegar a Grunty en la cima.",
        "Y antes de la perforadora, en el guion temprano, las hermanas huían de Spiral Mountain en un caldero mecánico volador.",
        "Un misterio que la wiki no sabe explicar: las huellas de la perforadora suben en vertical por las paredes de Wasteland y de Quagmire. La Hag 1, al parecer, también trepa.",
    ]},

    # ================================================================ 1 · WELDAR
    {"id": "p01", "post": 2.8, "frases": [
        "Número uno. Weldar, en Grunty Industries. Un soplete con forma de serpiente… que casi no ve.",
        "Llegar a él ya es un jefe: Mumbo apaga el electroimán con su descarga, Banjo se convierte en lavadora para pulsar un interruptor, y bajas al sótano del taller de reparaciones.",
        "Al verte, Weldar dice que se dejó las gafas. Y te pide que te acerques, porque desde ahí no te ve para pegarte.",
        "Tiene seis golpes, y todos van a la boca: un huevo de fuego, una granada o un Kazooie de cuerda, justo cuando aspira.",
        "Entre medias te lanza bolas de fuego azules, suelta tuercas y tornillos con patas, y salta para aplastarte. Cuando le das, se queja: «Por favor, no hagas eso. Estoy lleno de gas inflamable».",
        "Tras el tercer golpe pierde la paciencia, busca su interruptor de emergencia, y electrifica los cables del suelo. Escucha.",
    ]},
    {"id": "p01b", "frases": [
        "¿Por qué es el número uno? Porque es difícil, pero justo: la pelea crece de verdad a mitad de camino, y está a la altura del mundo más enrevesado del juego. Tres de las siete listas lo ponen primero.",
        "Al perder, su cabeza sale volando, choca con una caja de alta tensión y apaga el ventilador gigante de la planta de aire, donde había escondido su Jiggy. Y se le escapa en voz alta: ¿cuándo aprenderá a callarse?",
        "Su última pregunta es si le puedes recomendar a un buen técnico de reparaciones.",
        "Si vuelves a buscar pelea, la cabeza te pregunta si eres un oso. Kazooie le contesta que sí, y que él va directo a la planta de reciclaje.",
        "Y lo más bonito: en la primera lista de Rare, el jefe de la fábrica ni siquiera era él. Eran The Kogs. [short pause] Weldar no existía… y acabó siendo el mejor.",
        "Un último detalle: si al aterrizar cae encima de un Kazooie de cuerda, el juego entero se cuelga.",
        "Y no acabó en la basura del todo: en Nuts and Bolts, según la wiki, Mumbo encontró su cuerpo y lo convirtió en un lanzallamas, el Aliento de Weldar.",
    ]},

    # ================================================================ cierre
    {"id": "cierre", "frases": [
        "Ese es el ranking: de Terry a Weldar, según siete listas de jugadores. [short pause] ¿Estás de acuerdo? ¿Mingy Jongo merecía el primero? ¿Old King Coal se merece algo mejor que el noveno?",
        "Déjalo en los comentarios. Los leemos todos, y como viste hoy, a veces acaban en el siguiente video.",
        "[playful] Y si es tu primera vez en el canal, suscríbete. Quedan muchos jefes por poner en orden. Nos vemos en la próxima.",
    ]},
]
