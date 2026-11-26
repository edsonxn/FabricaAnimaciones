# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Los MITOS de Ocarina of Time que eran REALES» (26-nov-2026).
Investigación R45 del 26-nov (canales/formula/cronicas_gaming.md § FÓRMULA VIGENTE): nuestro ganador oot_remake_eliminado ×15
+ fuera Robe «DESMENTÍ los MITOS… de MARIO 64 que son Reales» ×4,1 (716 k). Variable: SOLO el ángulo (mito verificado).
Datos y fuentes: investigacion.md (agente, 26-nov). Fuera a propósito: los cuadros de Mario (ya fueron el n.º 1 de
oot_remake_eliminado) y la «pelea secreta» de Skull Kid del remake (oot_remake_anadido dijo que no es nueva).
Voz del canal: Carlos Aguilar (12-nov-2026); desde el 26-nov es la voz por defecto, sin votación ni mención de Hope (el usuario).
Comentarios (pegatinas/com_*.png, ≤ 10 días): gracias @jhunoadguerrero-ilusionista, @mau-azp (cierre) y la duda justa de
@lindaclark6221 sobre la granja del puente (se explica, sin burla). Sin críticas nuevas.
"""

TITULO = "12 MITOS de Ocarina of Time que eran REALES"
ARCHIVO = "oot_mitos_reales"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 88
HOPE = "tnSpp4vdxKPjI9w0GnoV"
# Voz del canal desde el 12-nov-2026: Carlos Aguilar (ElevenLabs, «Resonate and Powerful», Latinoamérica), turbo.
# Sin [whispers] ni [excited] (regla 2-nov). Solo la cuenta 4 tiene saldo (26-nov).
VOZ = dict(motor="elevenlabs", voice_id="8MeTTgXVwMEhRVfblXOj", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/_muestras_voz_gaming/05_carlos_aguilar.mp3", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"))
VOZ_POR_FRASE = {}   # 26-nov: Carlos Aguilar es LA voz del canal; sin votación ni mención de la anterior (el usuario)
FONETICA = {}
# 26-nov: Whisper escribe «Gilia», «iliana», «Cacarico», «Vigoron»: falsas alarmas de nombres
CER_MAX_POR_FRASE = {"p12_1": .03, "p12_2": .04, "p5_0": .08, "p4_3": .03}
TAIL_MAX_POR_FRASE = {"com1_1": 1.05}
GAP_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={'scene-068': 0.95},   # 068 = el canto de la v1.0 («Escucha»)
    recorte_por={'scene-001': 0.131, 'scene-004': 0.131, 'scene-006': 0.131, 'scene-008': 0.125, 'scene-011': 0.131, 'scene-012': 0.125, 'scene-013': 0.125, 'scene-015': 0.131, 'scene-017': 0.131, 'scene-018': 0.131, 'scene-025': 0.131, 'scene-026': (0.03, 0.02, 0.03, 0.17), 'scene-028': (0.03, 0.02, 0.03, 0.17), 'scene-032': 0.125, 'scene-033': 0.131, 'scene-035': 0.131, 'scene-038': 0.131, 'scene-039': 0.131, 'scene-040': 0.131, 'scene-043': 0.131, 'scene-044': 0.131, 'scene-045': 0.131, 'scene-046': 0.131, 'scene-047': 0.131, 'scene-049': 0.131, 'scene-050': 0.131, 'scene-051': 0.131, 'scene-054': (0.0, 0.135, 0.0, 0.135), 'scene-055': (0.0, 0.135, 0.0, 0.135), 'scene-056': (0.0, 0.135, 0.0, 0.135), 'scene-057': 0.125, 'scene-058': 0.131, 'scene-059': 0.131, 'scene-062': (0.375, 0.165, 0.01, 0.215), 'scene-063': (0.375, 0.165, 0.01, 0.215), 'scene-064': (0.375, 0.165, 0.01, 0.215), 'scene-073': 0.131, 'scene-076': 0.131},
    yt=dict(sufijo="", min_s=30, max_min=1300, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora OFICIAL de Ocarina of Time (armar_musica_ost.py -> audio/musica.wav), regla del 23-oct.
LYRIA = dict(estilo="", escenas={})


ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[serious] En 1998 no había internet en casa. Los secretos de Ocarina of Time se contaban en el recreo.",
        "[curious] Que en un templo se oía un rezo de verdad. Que Ganon sangraba rojo. Que el búho pesado era un sabio disfrazado.",
        "[deadpan] Y tú pensabas que eran inventos del niño que decía que su tío trabajaba en Nintendo.",
        "[serious] Pues hoy revisé 12 de esos mitos, uno por uno. [short pause] Y casi todos eran verdad.",
    ]},
    {"id": "contexto", "frases": [
        "Las reglas son simples. Cada mito se lleva un sello. Real, a medias, o falso.",
        "Y donde se pueda, te enseño qué pasa en el remake de Switch 2, el que salió el 5 de noviembre.",
        "[mischievously] Empezamos por el más inofensivo. Y terminamos con uno que Nintendo prefirió no explicar.",
    ]},
    {"id": "p12", "frases": [
        "[curious] Número 12. [short pause] El pez imposible del estanque.",
        "Se decía que en el estanque de pesca del Lago Hylia vivía un pez enorme, que casi nadie lograba sacar.",
        "[serious] Real. Es la locha hyliana, y no sale todas las veces que pagas por pescar.",
        "[amused] Lo mejor es cómo se pesca. Solo muerde el señuelo hundido, que el dueño del estanque considera trampa. Si lo usas, te regaña.",
        "[deadpan] O sea, el pez legendario solo se deja atrapar si haces trampa. [short pause] Y en el remake sigue ahí, esperando a los tramposos.",
    ]},
    {"id": "p11", "frases": [
        "[playful] Número 11. [short pause] La venganza de las gallinas.",
        "En el recreo alguien siempre juraba que si le pegabas mucho a un cuco, llegaba un ejército de gallinas a matarte.",
        "[serious] Real. Golpea a un cuco varias veces, y aparece una bandada que no puedes derrotar.",
        "Te atacan sin parar, hasta que sales de la zona o te metes en una casa.",
        "[deadpan] El enemigo más peligroso de Hyrule no es Ganondorf. Es una gallina con rencor. [short pause] Y en el remake siguen igual de rencorosas.",
    ]},
    {"id": "p10", "frases": [
        "[mischievously] Número 10. [short pause] Montar a Epona de niño.",
        "Este lo juró media generación. Que con un truco, Link niño podía subirse a Epona en el Rancho Lon Lon.",
        "[serious] Falso. De niño, Epona es una potranca, demasiado joven para cargarte. La montas hasta siete años después.",
        "Todos los videos donde Link niño cabalga usan códigos de trucos o mods.",
        "[amused] Link niño sí monta a Epona. Pero en Majora's Mask. [short pause] Tu primo te mintió, aunque se adelantó un juego.",
    ]},
    {"id": "p9", "frases": [
        "[curious] En el 9, el corredor de la pradera.",
        "Es un hombre que corre por Hyrule sin parar. Y el mito decía que nadie le podía ganar, por más rápido que fueras.",
        "[serious] Real. El juego está programado para que siempre llegue antes que tú. Por exactamente un segundo. Hagas lo que hagas.",
        "Lo han probado con códigos, con atajos y con todo. No hay forma.",
        "[deadpan] Es el único personaje de Hyrule que hace más trampa que tú con la locha.",
    ]},
    {"id": "com1", "frases": [
        "[warm] Alguien escribió en el video de los jefes de Banjo-Tooie: buen trabajo, tienes mi apoyo total.",
        "[warm] Gracias. Todos los comentarios se leen, y se toman en cuenta para mejorar cada video.",
    ]},
    {"id": "p8", "frases": [
        "[serious] Número 8. [short pause] Los esqueletos que crecen.",
        "De noche, en la pradera de Hyrule, salen del suelo unos esqueletos pequeños, los Stalchildren. Y el rumor decía que si matabas muchos, salía uno gigante.",
        "[impressed] Real. Si vas de niño y derrotas a 10, sale uno más grande. Y al llegar a 20, uno enorme.",
        "El contador se borra al amanecer. Y si caminas por el sendero de tierra, ni siquiera salen.",
        "[deadpan] O sea, un jefe secreto que solo aparece si te pasas la noche entera matando esqueletos sin ningún motivo. [short pause] Que es justo lo que hacíamos.",
    ]},
    {"id": "p7", "frases": [
        "[curious] En el 7, el Zelda secreto.",
        "Las revistas hablaban de un Zelda escondido para el 64DD, el lector de discos de la Nintendo 64, con mazmorras distintas.",
        "[serious] Real. Se llamaba Ura Zelda. Eiji Aonuma contó en Iwata Asks que ya hablaban de hacerlo para el 64DD, reutilizando las mazmorras de Ocarina.",
        "El 64DD fracasó, y ese Zelda salió años después en GameCube, como Master Quest, en un disco de regalo.",
        "[thoughtful] Y de rebote nació otro juego. Aonuma no quería rehacer mazmorras, y empezó a diseñar unas nuevas. Esas terminaron en Majora's Mask.",
    ]},
    {"id": "p6", "frases": [
        "[playful] Número 6. [short pause] El búho que nadie dejaba hablar.",
        "Kaepora Gaebora. Aparece cada dos pasos, habla sin parar, y al final te pregunta si quieres oírlo otra vez.",
        "Y el mito decía que no era un búho cualquiera, sino un sabio disfrazado.",
        "[serious] Real. Una piedra chismosa del juego ya decía que el búho era un sabio antiguo. Y el libro oficial Hyrule Historia lo confirmó en 2011. Es Rauru, el sabio de la luz, uno de los que construyeron el Templo del Tiempo.",
        "[deadpan] Así que durante años le saltamos el diálogo a un sabio milenario. [short pause] Por eso nos repetía todo.",
    ]},
    {"id": "com2", "frases": [
        "[warm] Y una corrección justa. En el video de lo que añadió el remake, alguien preguntó: ¿cuál granja del puente? No entendí nada.",
        "Tienes razón, faltó contexto. En el juego de 1998, Link niño trepaba por la cadena del puente levadizo de la Ciudadela, y ahí había tres rupias rojas escondidas, que volvían a salir cada vez que entrabas.",
        "En el remake, Link resbala en la cadena y esas rupias ya no existen. Lo conté en el video de lo que Nintendo eliminó. [short pause] El chiste solo se entendía si viste ese. Anotado.",
    ]},
    {"id": "p5", "frases": [
        "[serious] Número 5. [short pause] La historia sangrienta de Kakariko.",
        "El rumor decía que debajo de Kakariko, en el pozo y en el Templo de las Sombras, había salas de tortura.",
        "La entrada del templo lo dice con todas sus letras. Aquí se reúne la historia sangrienta de Hyrule, de codicia y de odio.",
        "Dentro hay guillotinas, potros de tortura, manchas de sangre y huesos por todas partes.",
        "[thoughtful] Pero quién torturaba a quién, el juego nunca lo dice. Lo de los sheikah interrogando a los enemigos de la familia real es teoría de fans. Así que, a medias.",
        "[deadpan] Y en el remake, las manchas rojas ahora son oscuras y secas. [short pause] Nintendo escribió historia sangrienta en la puerta, y luego le pasó el trapeador.",
    ]},
    {"id": "p4", "frases": [
        "[curious] En el 4, los que se pierden en el bosque.",
        "Se decía que quien se perdía en el Bosque Perdido se convertía en un monstruo.",
        "[serious] Real, y lo dice el propio juego. Fado, una de las kokiri, cuenta que todo el que entra al bosque, menos los kokiri, se pierde y se vuelve Stalfos.",
        "Y pone un ejemplo. Grog, el muchacho que encuentras en el bosque durante el intercambio de la espada de Biggoron.",
        "[thoughtful] Cuando regresas a buscarlo, ya no está. Y Fado te explica qué le pasó. [short pause] El muchacho al que le hiciste un favor terminó convertido en esqueleto.",
        "Lo de que los niños perdidos se vuelven Skull Kids, eso el juego solo lo insinúa.",
    ]},
    {"id": "p3", "frases": [
        "[serious] Número 3. [short pause] Ganon sangraba rojo.",
        "En el recreo se peleaban. Unos juraban que, en el final, Ganondorf escupía sangre roja. Otros, que era verde.",
        "[impressed] Y tenían razón los dos. Los primeros cartuchos, las versiones 1.0 y 1.1, traen sangre roja. Desde la 1.2, es verde.",
        "[curious] Y no fue lo único que se borró. El símbolo Gerudo era una media luna con una estrella, en el Escudo Espejo y en los bloques. En las versiones de GameCube, Nintendo lo cambió por otro.",
        "[deadpan] Pero se le olvidaron algunas lunas en la tumba de Dampé. [short pause] Ahí siguen, como si nada.",
    ]},
    {"id": "p2", "frases": [
        "[mischievously] Número 2. [short pause] El mito más famoso de todos. La Trifuerza se puede conseguir.",
        "En 1999, una jugadora aseguró en internet que la había conseguido, en un Templo de la Luz, tocando una canción secreta.",
        "[serious] Falso. Nunca dio los pasos, y semanas después reconoció que era mentira. El código se ha revisado de arriba abajo, y no hay Trifuerza.",
        "[curious] Pero en 2022, en el maratón benéfico Summer Games Done Quick, un grupo de fans lo hizo realidad.",
        "Con TASBot, un robot que presiona los botones, metieron código nuevo a través de los mandos, en un cartucho original, en una Nintendo 64 real. Y Link tomó la Trifuerza en vivo.",
        "[deadpan] En tu partida sigue siendo falso. [short pause] Pero tardó 23 años en dejar de ser mentira.",
    ]},
    {"id": "p1", "post": 7.0, "frases": [
        "[serious] Y el número 1. [short pause] El rezo del Templo del Fuego.",
        "El mito decía que en la música del Templo del Fuego se oía a alguien rezando, de verdad. Y que Nintendo la cambió a escondidas.",
        "[thoughtful] Y sí, es real. En las primeras versiones del cartucho, la música trae una voz que canta un rezo islámico real. Escucha.",
    ]},
    # post: se OYE el canto en la versión 1.0 (clip con ambiente_por, la voz callada); fuente en plan_clips.py
    {"id": "p1b", "frases": [
        "Esa voz salió de un CD comercial de sonidos para músicos. Koji Kondo, el compositor, no sabía lo que decía.",
        "[serious] Desde la versión 1.2, esa música cambió por otra, sin la voz. Y así siguió en GameCube, en 3DS, y hasta en la aplicación Nintendo Music.",
        "[curious] Lo de que la quitaron por las quejas de alguien, eso es falso. Todo apunta a que fue la propia norma de Nintendo contra las referencias religiosas reales.",
        "[deadpan] Y si quieres saber cuál tienes, mira detrás del cartucho. Si los números llevan una letra B, el tuyo ya no reza.",
    ]},
    {"id": "cierre", "frases": [
        "[warm] Y para cerrar. En el ranking de mundos de Banjo-Tooie, alguien escribió que el nivel que más disfruta es la laguna, pero que el que más le gusta por su diseño son los picos fuego helados. Gracias por contarlo.",
        "[curious] Ahora te toca a ti. ¿Cuál de estos mitos te contaron en el recreo? [short pause] Te leo en los comentarios.",
        "[playful] Si quieres ver lo que Nintendo quitó del remake, aquí lo tienes. Suscríbete, que todavía quedan mitos. Nos vemos pronto.",
    ]},
]
