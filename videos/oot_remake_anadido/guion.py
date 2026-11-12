# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Lo que Nintendo AÑADIÓ en SECRETO al REMAKE de Ocarina of Time» (11-nov-2026).
Sigue a oot_remake_eliminado (1 088 vistas en 2,5 días, ×4-×15 el canal). Variable: SOLO el ángulo (lo eliminado -> lo añadido
sin anunciar). Datos, fuentes y clips con segundo: investigacion.md (lo de dataminers se dice «según los dataminers»).
Comentarios en pantalla (pegatinas/com_*.png, todos del 11-nov): 3 críticas con contraburla (Loquendo, TikTok, voz insufrible),
la pregunta de Master Quest (@mantequill4) y el agradecimiento de @frandeltin4387 (Mario 64).
"""

TITULO = "Lo que Nintendo AÑADIÓ en SECRETO al REMAKE de Ocarina of Time"
ARCHIVO = "oot_remake_anadido"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
# Voz del canal: Hope (ElevenLabs) con turbo, como oot_remake_cambios. Sin [whispers] ni [excited] (regla 2-nov).
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"))
# 11-nov: idioma_voz marcó en inglés intro_2, p1_4 y p6_4 por estos nombres (regla del 10-nov)
FONETICA = {"Master Quest": "Máster Cuést", "Skull Kid": "Escul Kid", "Majora's Mask": "Mayóras Mask", "ranking": "ránking"}
# 11-nov, revisado en voz/eval.json: Whisper escribe «Skull Keep», «Kórox», «Reddit», «locuendo», «Caipora Gaebora», «Cacarico»,
# «Capora Guevara», «Yabu Yabu»: falsas alarmas de nombres; colas largas = respiración final
CER_MAX_POR_FRASE = {"contexto_3": .04, "p12_0": .07, "p7_1": .045, "com1_1": .02, "p6_1": .055, "p6_2": .03, "p5_3": .04,
                     "com3_1": .07, "p2_1": .03, "p2_2": .02}
TAIL_MAX_POR_FRASE = {"contexto_3": .66, "p7_1": .66, "p6_2": .6, "p2_1": .65, "p2_2": .78}
GAP_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    # plan_clips.py (11-nov): 048 = Ganondorf «You're entertaining…», 055 = Darunia «pile of gravel» con la voz callada
    ambiente_por={'scene-015': 0.8, 'scene-048': 0.9, 'scene-055': 0.9},   # 015 = la ocarina real del remake (Sirloin, canciones)
    recorte_por={'scene-016': 0.12, 'scene-042': 0.12, 'scene-006': 0.131, 'scene-014': 0.131, 'scene-019': 0.131, 'scene-023': 0.131, 'scene-027': 0.131, 'scene-046': 0.131,
                 'scene-047': 0.131, 'scene-052': 0.131, 'scene-053': 0.131, 'scene-059': 0.125, 'scene-060': 0.125, 'scene-061': 0.125, 'scene-062': 0.125,
                 'scene-063': 0.125},
    yt=dict(sufijo="", min_s=30, max_min=1300, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora OFICIAL de Ocarina of Time (armar_musica_ost.py -> audio/musica.wav), regla del 23-oct.
LYRIA = dict(estilo="", escenas={})


ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[curious] En el código del nuevo Ocarina of Time hay una máscara que todavía no puedes usar.",
        "[serious] Tiene 173 frases escritas para ella. Y nadie en Hyrule sabe qué es.",
        "[playful] Esa máscara, unos sabios que por fin dejan de estar muertos, una quinta botella, y un Master Quest escondido.",
        "Así que hoy te cuento las 12 cosas que Nintendo añadió al remake sin anunciarlas. [short pause] De la más pequeña, a la que nadie vio venir.",
    ]},
    {"id": "contexto", "frases": [
        "[impressed] El remake salió el 5 de noviembre, solo en Switch 2. Y en cuatro días vendió más de 5 millones de copias.",
        "[amused] El Ocarina de Nintendo 64 vendió 7,6 millones en toda su vida. Este ya va por el 70 por ciento, en una semana.",
        "Y hasta la caja esconde algo. Por dentro trae un mapa de Hyrule impreso, y debajo del cartucho aparece Navi.",
        "[deadpan] Ah, y no. El jefe secreto de Skull Kid que anda por redes no es nuevo. Ese duende del Bosque Perdido ya te atacaba en 1998, con la misma rupia de 200.",
        "[playful] Lo realmente nuevo está en otra parte. Vamos con la lista.",
    ]},
    {"id": "p12", "frases": [
        "[curious] Número 12. [short pause] Koroks en el Bosque Kokiri.",
        "En el bosque donde empieza todo, ahora flotan unas hojitas mágicas, como polen.",
        "Y si te fijas, muchas tienen la silueta de un Korok, los espíritus del bosque de Wind Waker y Breath of the Wild.",
        "[thoughtful] Es un guiño a la línea temporal. Después de la Gran Inundación, los kokiris se convierten en koroks. Game Informer dice que es el único añadido que apunta al futuro de la saga.",
    ]},
    {"id": "p11", "frases": [
        "[playful] En el 11, Link por fin actúa.",
        "En la Nintendo 64, Link tocaba la ocarina con las manos quietas, como si fuera una flauta de adorno.",
        "En el remake mueve los dedos sobre cada agujero. Y el sonido es una ocarina real grabada, que suena distinto según el lugar.",
        "[amused] Y cuando corre entre la hierba alta, Link niño levanta los brazos para taparse la cara. El adulto no, porque ya es más alto que la hierba.",
    ]},
    {"id": "p10", "frases": [
        "[warm] Número 10. [short pause] La ocarina de Saria ya no se pierde.",
        "Al salir del bosque, Saria le regala a Link su Ocarina de las Hadas.",
        "En la Nintendo 64, cuando Zelda te daba la Ocarina del Tiempo en el foso del castillo, la de Saria desaparecía del inventario. La nueva la sustituía.",
        "[thoughtful] En el remake te quedas con las dos, y eliges cuál tocar. Un recuerdo de tu amiga que ya no te quitan.",
    ]},
    {"id": "p9", "frases": [
        "[curious] En el 9, una quinta botella. Y llega mucho antes.",
        "La primera vez que entras a la Ciudadela, el dueño de la tienda de pociones grita que se le escapó un bicho.",
        "Te presta una botella vacía para atraparlo. Un escarabajo dorado que corre por toda la tienda.",
        "[amused] Si lo atrapas, te la regala, con una poción roja de premio. En la Nintendo 64 había solo cuatro botellas, y la primera tardaba bastante más.",
        "[serious] Eiji Aonuma lo contó en Game Informer. Las botellas son tan importantes para jugar, que él mismo pidió que la primera llegara antes.",
    ]},
    {"id": "p8", "frases": [
        "[playful] Número 8. [short pause] Una tienda que cabe en el bolsillo.",
        "Es un objeto nuevo, la Semilla del Mercader Deku. La lanzas, y donde cae aparece un vendedor Deku.",
        "Así puedes comprar flechas, bombas o semillas en mitad de una mazmorra, sin salir de ella.",
        "[sighs] En la Nintendo 64, si te quedabas sin flechas en el Templo del Bosque, te tocaba dar media vuelta. [short pause] Ahora el comercio viene a ti.",
    ]},
    {"id": "p7", "frases": [
        "[serious] En el 7, los ReDeads ahora dan todavía más miedo.",
        "Cuando un ReDead te ve, Link se queda paralizado. Y ahora lo envuelven unas bandas rojas brillantes, y lo ves forcejear.",
        "Te paraliza en cualquier postura. Incluso en el aire, si saltaste para atacarlo.",
        "[curious] Y la Mano Muerta del Fondo del Pozo se rehízo entera. Una masa pálida que sale de la niebla verde, mientras las manos salen del suelo.",
    ]},
    {"id": "com1", "frases": [
        "[amused] Por cierto, alguien me escribió esto en el video anterior.",
        "Que mejor use Loquendo en vez de inteligencia artificial, que se escucharía mejor.",
        "[deadpan] Lo intenté, de verdad. Pero Loquendo pidió que le pagaran en rupias de la granja del puente. [short pause] Y esa granja, Nintendo la eliminó.",
    ]},
    {"id": "p6", "frases": [
        "[playful] Número 6. [short pause] Un salón secreto que se abre soñando.",
        "Después del Templo del Bosque, Kaepora Gaebora te cuenta en Kakariko que hay un lugar al que se llega a través de los sueños.",
        "Cualquier cama con un brillo verde te lleva. La de tu casa en el bosque, el albergue de Kakariko, el laboratorio del lago, o el campamento del Valle Gerudo.",
        "Es el Salón de los Enemigos Caídos. Tiene 84 estatuas, una por cada tipo de enemigo que derrotaste.",
        "[impressed] Y puedes volver a pelear con cada jefe, contra reloj, con ranking mundial. Si completas las pruebas, aparece un trofeo en tu casa del Bosque Kokiri.",
    ]},
    {"id": "p5", "frases": [
        "[curious] En el 5, la Máscara de la Verdad lee pensamientos.",
        "En la Nintendo 64 servía para entender a las Piedras Chismosas, y poco más.",
        "En el remake, si te acercas a alguien de frente, ve la máscara y reacciona. Pero si llegas por la espalda, sin que te vea, oyes lo que piensa de verdad.",
        "[amused] El guardia de Kakariko que pedía la máscara Keaton para su hijo, por la espalda confiesa que era para él.",
        "[deadpan] Hay un niño que persigue un cuco con la idea de comérselo. Y hasta las vacas tienen pensamientos.",
    ]},
    {"id": "com2", "frases": [
        "[amused] Y otro me dejó este consejo. Que me vaya a subir contenido a TikTok.",
        "[deadpan] Lo pensé. Pero en TikTok no cabe una lista de 12. [short pause] Ahí apenas llegaría a la Semilla del Mercader.",
    ]},
    {"id": "p4", "post": 5.6, "frases": [
        "[serious] Número 4. [short pause] Ganondorf ya no es un mudo en el Templo del Tiempo.",
        "En la Nintendo 64, al sacar la Espada Maestra, Ganondorf aparecía, decía un par de líneas de texto, y entraba al Reino Sagrado sin que lo vieras.",
        "En el remake entra al templo, y se burla de Link niño con voz. Escucha.",
    ]},
    # post: se OYE «You're entertaining, I'll give you that. For a child at most.» (8nSoklvmLkM 204,3-209,4 s, Whisper 11-nov) con la voz callada
    {"id": "p4b", "frases": [
        "Eres entretenido, te lo concedo. Para ser un niño. Siempre supe que tú serías mi llave para la Puerta del Tiempo.",
        "[curious] Y luego hay una escena nueva, con Ganondorf entrando en el Reino Sagrado, y tomando la Trifuerza.",
        "[thoughtful] Aonuma explicó que la escena original explicaba muy poco. Querían que se entendiera por qué Ganondorf estaba ahí, y cómo reaccionaba.",
    ]},
    {"id": "p3", "post": 8.4, "frases": [
        "[thoughtful] En el 3, una pregunta de 28 años. ¿Los sabios estaban muertos?",
        "En la Nintendo 64, Saria, Darunia y Ruto desaparecían en sus templos, y nunca quedaba claro qué les había pasado. Media comunidad los daba por muertos.",
        "En el remake, en la Cámara de los Sabios, cada uno lo cuenta. Así lo dice Darunia.",
    ]},
    # post: se OYE «I hate to say it, but I'd be a pile of gravel right now if Rauru hadn't pulled me outta the fire» (L45cq1H2d1s 12197,3-12205,6 s)
    {"id": "p3b", "frases": [
        "Que sin Rauru, ahora mismo sería un montón de grava, porque fue Rauru quien lo sacó del fuego.",
        "[warm] Saria dice lo mismo. Rauru la llamó en pleno Templo del Bosque. No murieron. Los rescataron. [short pause] Aunque no pueden volver al mundo que conocían.",
    ]},
    {"id": "com3", "frases": [
        "[amused] Y para el que escribió que mi voz es insufrible.",
        "[deadpan] Te entiendo. Kaepora Gaebora también hablaba mucho, y a él le dieron su propio tema musical.",
    ]},
    {"id": "p2", "frases": [
        "[curious] Número 2. [short pause] Master Quest sí está. Escondido.",
        "En el video anterior te conté que el remake salió sin Master Quest. Y aquí alguien me preguntó si va a salir.",
        "[serious] Pues los dataminers encontraron en el código todo lo necesario para activarlo. El mundo en espejo, las mazmorras cambiadas, y hasta vacas dentro de la tripa de Jabu Jabu.",
        "Según ellos, se activaría con un contenido descargable. Nintendo no lo ha confirmado.",
        "[deadpan] Y cuando le preguntaron a Aonuma, contestó que por ahora no iban a anunciar nada. [short pause] En idioma Nintendo, eso ya es casi un sí.",
    ]},
    {"id": "p1", "frases": [
        "[serious] Y lo número 1. [short pause] La máscara que todavía no existe.",
        "Las máscaras de los amiibo de Link niño y de Zelda niña están en el código. Pero hay una tercera, sin amiibo anunciado.",
        "Tiene 173 frases de reacción, escritas solo para ella. Los personajes la llaman rara, inquietante, de otro mundo. Y uno de ellos hasta le dice monstruo.",
        "[curious] Y nadie en Hyrule la reconoce. El hijo del maestro carpintero te pregunta si vienes por él.",
        "[thoughtful] Los fans creen que es un amiibo del duende del Bosque Perdido. Y que con él llegaría el remake de la secuela, la de la luna. Nintendo no ha dicho nada. [short pause] Pero el último punto de este mapa es uno que todavía no existe.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Y una cosa más. Alguien escribió en el video de Mario 64 que no entendía por qué no tenía más likes ni vistas.",
        "[warm] Gracias. Todos los comentarios se leen, los buenos y los otros, y se toman en cuenta para mejorar cada video.",
        "[curious] Ahora te pregunto a ti. [short pause] De estas 12 cosas, ¿cuál te sorprendió más? Te leo en los comentarios.",
        "[playful] Y si quieres ver lo que Nintendo quitó del remake, aquí lo tienes. Suscríbete, que lo del Master Quest todavía no termina. Nos vemos pronto.",
    ]},
]
