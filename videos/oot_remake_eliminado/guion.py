# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Lo que Nintendo ELIMINÓ del REMAKE de Ocarina of Time» (6-nov-2026).
PRUEBA P1 del plan de Claude para subir vistas (canales/formula/cronicas_gaming.md, 6-nov): actualidad en su pico (el remake
salió el 5-nov; Short de Vandal «2 SECRETOS ELIMINADOS del remake» 289 k en 1,5 días; Mundo N «10 cosas que Nintendo AÚN
ESCONDE…» ×4,8). Variable frente a oot_remake_cambios: SOLO el ángulo (lo quitado) + título corto con verbo fuerte (P3).
Datos y fuentes: investigacion.md (CONFIRMADO / REPORTADO; lo reportado se dice «según jugadores / según la reseña»).
Ganondorf comprobado en imagen (previews/_check/hoja_gan.jpg, b5Zg52U0aE4 680-730 s): se arrodilla y dice «I, the mighty
Ganondorf, the Demon King! Defeated?!… Losing to some pathetic child?!»; no hay plano de escupir sangre.
Sin comentarios en pantalla: los 5 de ≤ 10 días ya se enseñaron en otros videos.
"""

TITULO = "Lo que Nintendo ELIMINÓ del REMAKE de Ocarina of Time"
ARCHIVO = "oot_remake_eliminado"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
# Voz del canal: Hope (ElevenLabs) con turbo, como oot_remake_cambios. Sin [whispers] ni [excited] (regla 2-nov).
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"))
FONETICA = {}
# Revisado el 6-nov leyendo voz/eval.json: Whisper escribe «$1,229», «Capora de Abora», «Cacarico», «Unuma», «Fushibayashi»,
# «Hawk White Ng», «cúltulas», «elevadizo»: falsas alarmas de nombres
CER_MAX_POR_FRASE = {"contexto_0": .046, "p10_1": .072, "p11_1": .036, "p9_2": .027, "p9_3": .022, "p8b_1": .046,
                     "p7_3": .02, "p3_4": .02, "p4_1": .014,
                     "p10_2": .028, "p5_2": .037, "p1_3": .015}   # «Si el»→«Y el», «había»→«vi a», «va bordando»: mismo en 2 semillas
TAIL_MAX_POR_FRASE = {"p10_1": .75, "p9_3": .66, "p5_2": .66}
GAP_MAX_POR_FRASE = {}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    # plan_clips.py (6-nov): 026 = «Hey!» de Navi N64 en los 2,2 s callados; 057 = «I, the mighty Ganondorf» del remake en los 6 s callados
    ambiente_por={'scene-015': 0.6, 'scene-019': 0.5, 'scene-021': 0.6, 'scene-026': 0.9, 'scene-027': 0.5, 'scene-031': 0.6, 'scene-045': 0.6,
                  'scene-046': 0.6, 'scene-049': 0.5, 'scene-054': 0.6, 'scene-055': 0.6, 'scene-057': 0.9, 'scene-061': 0.5},
    recorte_por={'scene-001': 0.125, 'scene-008': 0.131, 'scene-011': 0.037, 'scene-012': (0.03, 0, 0.02, 0), 'scene-013': 0.037,
                 'scene-015': 0.125, 'scene-018': 0.131, 'scene-019': 0.131, 'scene-026': 0.131, 'scene-031': 0.131,
                 'scene-036': 0.131, 'scene-049': 0.125, 'scene-050': 0.125, 'scene-053': 0.131, 'scene-054': (0, 0.14, 0, 0.14),
                 'scene-055': (0, 0.14, 0, 0.14), 'scene-060': (0.14, 0, 0.145, 0), 'scene-061': 0.125},
    yt=dict(sufijo="", min_s=30, max_min=1300, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: banda sonora OFICIAL de Ocarina of Time (armar_musica_ost.py -> audio/musica.wav), regla del 23-oct.
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[curious] Si en 1998 te asomabas por la ventana del patio de la princesa Zelda, veías cuadros de Mario, de Peach y de Bowser.",
        "[serious] En el remake de Switch 2, esos cuadros ya no están. Y Nintendo explicó por qué.",
        "[playful] No es lo único. Una granja de rupias, Master Quest, glitches famosos, y hasta una escena de Ganondorf.",
        "Así que hoy te cuento las 12 cosas que Nintendo eliminó del remake de Ocarina of Time. [short pause] De la más pequeña, a la que más está dando que hablar.",
    ]},
    {"id": "contexto", "frases": [
        "[serious] El remake salió el 5 de noviembre, solo en Nintendo Switch 2. En México cuesta 1229 pesos en versión digital.",
        "Lo hizo el mismo equipo de Breath of the Wild y Tears of the Kingdom, y lo rehicieron desde cero. No es el código de 1998 con gráficos nuevos.",
        "[impressed] Ya tiene un 96 en Metacritic, la nota más alta de 2026. El original de Nintendo 64 sigue arriba, con un 99.",
        "[amused] Y lo primero que se eliminó, lo eliminó el propio Eiji Aonuma. Pidió añadir puntos de teletransporte por todo Hyrule, y luego mandó quitarlos todos.",
        "[deadpan] Según él, al final no le convencían. Si viajas de un salto, te saltas lo que hay en el camino.",
        "[playful] Pero lo que la gente está notando de verdad es otra cosa. Vamos con la lista.",
    ]},
    {"id": "p12", "frases": [
        "[curious] Número 12. [short pause] Un guiño que solo existía en la Nintendo 3DS.",
        "En el Ocarina of Time 3D de 2011, había cuadros de Skyward Sword escondidos en el Rancho Lon Lon y en la Fortaleza Gerudo.",
        "En el remake se quitaron. Por la misma razón que vas a oír en el número 1.",
        "[amused] Y cuando le preguntaron si el equipo de la 3DS se iba a enojar, Hidemaro Fujibayashi contestó que no había rencor.",
    ]},
    {"id": "p11", "frases": [
        "[playful] En el 11, la Lupa de la Verdad cambió de forma.",
        "En la Nintendo 64 era una lupa con un ojo dibujado, y la sacabas del fondo del pozo de Kakariko.",
        "En el remake ya no es una lupa. Son unas gafas que Link se pone en la cara, con un ojo que se abre y se cierra.",
        "[amused] Y algunos personajes del juego hasta le comentan a Link su nuevo aspecto.",
    ]},
    {"id": "p10", "frases": [
        "[sighs] Número 10. [short pause] El búho que no se callaba.",
        "Kaepora Gaebora te soltaba un sermón larguísimo. Y al final preguntaba, ¿lo entendiste?",
        "[amused] Si el cursor quedaba en no, y apretabas rápido, te repetía todo el discurso desde el principio.",
        "En el remake sus apariciones son más cortas, y ya no hay pregunta. Fujibayashi contó que reescribieron textos que hoy no se entienden bien.",
    ]},
    {"id": "p9", "frases": [
        "[curious] En el 9, se acabó buscar secretos a ciegas.",
        "En la Nintendo 64, la Piedra de la Agonía hacía vibrar el Rumble Pak cuando había un secreto cerca. Y muchas grutas se abrían con una bomba en un sitio sin ninguna marca.",
        "En el remake, la piedra se cambió por un broche que solo reacciona a las Skulltulas doradas. Y las grutas escondidas se marcan con flores en el suelo.",
        "[thoughtful] Fujibayashi lo explicó así. Querían que el jugador pudiera deducir qué hacer dentro del propio juego, sin una guía al lado.",
        "Y según la reseña de Eurogamer, en el Bosque Perdido ya no hay que seguir la canción de Saria de oído. El tronco correcto brilla en verde.",
    ]},
    {"id": "p8", "post": 2.2, "frases": [
        "[playful] Número 8. [short pause] ¡Hey, escucha!, mucho menos.",
        "En 1998, Navi te interrumpía con esto, a cada rato.",
    ]},
    # post: se OYE el «Hey! Listen!» real de Navi (N64) con la voz callada (regla del 31-oct)
    {"id": "p8b", "frases": [
        "En el remake, al explorar, casi siempre te avisa con un sonido suave. Y parte de sus pistas ahora las dan unas hadas repartidas por el escenario.",
        "[curious] En inglés tiene voz nueva, de la actriz Lisa Reimold. Y el director, HokWai Ng, dijo que algo tan icónico como el Hey, listen, no lo querían tocar.",
        "[amused] Así que la frase sigue ahí. Solo que ahora te la ahorran casi siempre.",
    ]},
    {"id": "p7", "frases": [
        "[serious] En el 7, las Grandes Hadas ya no regalan nada.",
        "En el original, llegabas a su fuente, tocabas la canción de Zelda, y te daban magia o un poder gratis.",
        "Según las guías del remake, ahora cada Gran Hada pide una ofrenda de rupias. 25 la de la Montaña de la Muerte, 50 la del castillo, y 500 la que está junto al castillo de Ganon.",
        "[amused] Fujibayashi dice que es una forma de reverencia, como las donaciones en los templos de Japón. [short pause] Una reverencia de 500 rupias.",
        "Y hay otro cambio. La clasificación del remake ya no avisa de temas sugerentes, algo que la versión de 3DS sí llevaba por la ropa de las hadas.",
    ]},
    {"id": "p6", "frases": [
        "[serious] Número 6. [short pause] Solo una partida.",
        "En la Nintendo 64 había tres archivos de guardado. Tú, tu hermano y tu primo, cada uno con su Link.",
        "En el remake hay una sola ranura, con guardado automático.",
        "[sighs] Y si quieres empezar de cero, pierdes la partida que tenías. [short pause] Así que, si compartes la consola, que sea con alguien de confianza.",
    ]},
    {"id": "p5", "frases": [
        "[curious] En el 5, adiós a los glitches de toda la vida.",
        "En la Nintendo 64 había trucos que rompían el juego. La espada infinita, atravesar paredes por las juntas, o escapar del Bosque Kokiri sin espada ni escudo.",
        "[amused] Hasta había quien inclinaba el cartucho con la consola encendida, para que las paredes desaparecieran.",
        "Como el remake se rehízo desde cero, según los jugadores ninguno de esos trucos funciona. Y la primera speedrun publicada en Switch 2 se hizo sin un solo glitch.",
        "[playful] Aunque, apenas un día después del estreno, ya están apareciendo trucos nuevos para moverse más rápido. Los speedrunners no descansan.",
    ]},
    {"id": "p4", "frases": [
        "[playful] Número 4. [short pause] La granja de rupias del puente.",
        "De niño, en el puente levadizo de la Ciudadela, podías trepar por una de las cadenas y saltar al centro.",
        "Ahí había tres rupias rojas que no se veían. 60 rupias gratis, que volvían a aparecer cada vez que salías y entrabas.",
        "[serious] En el remake, Link resbala al intentar subir por las cadenas, y las rupias ya no existen.",
        "[thoughtful] Nintendo no lo ha explicado. Hay quien cree que es porque ahora empiezas con una bolsa de 200 rupias, y ya no hace falta juntar tanto.",
    ]},
    {"id": "p3", "frases": [
        "[serious] En el 3, Master Quest.",
        "Master Quest era la otra versión de Ocarina of Time, con las mazmorras rehechas y mucho más difíciles. Salió en GameCube en 2003, de regalo al reservar Wind Waker.",
        "En la versión de 3DS venía incluida. Con el mundo en espejo, y los enemigos haciendo el doble de daño.",
        "En el remake no hay Master Quest. Ni modo difícil, ni nueva partida con extras. Terminar la historia no desbloquea nada.",
        "[deadpan] Cuando IGN le preguntó a Aonuma, contestó que no creía que fueran a anunciar nada específico por ahora. [short pause] Que en idioma Nintendo, es un tal vez.",
    ]},
    {"id": "p2", "post": 6.0, "frases": [
        "[serious] Número 2. [short pause] La escena de Ganondorf.",
        "En la primera versión de 1998, después de vencer a Ganondorf en lo alto de su torre, escupía sangre roja.",
        "Meses después, Nintendo sacó otra versión del cartucho, y la sangre pasó a ser verde. La de 3DS la dejó verde.",
        "[curious] En el remake, según los jugadores que ya lo terminaron, ese momento no está. Ganondorf cae de rodillas, y habla.",
    ]},
    # post: se OYE la línea nueva de Ganondorf en inglés (remake) con la voz callada
    {"id": "p2b", "frases": [
        "Yo, el poderoso Ganondorf, el Rey Demonio, ¿derrotado? ¿Por un niño patético?",
        "[thoughtful] Nintendo no ha comentado nada. Pero es el cambio del que más se habla en redes desde el estreno.",
    ]},
    {"id": "p1", "frases": [
        "[curious] Y lo número 1. [short pause] Los cuadros de Mario.",
        "En la Nintendo 64, en el patio donde conoces a Zelda, te asomabas por las ventanas y veías cuadros de Mario, Luigi, Peach, Bowser y Yoshi.",
        "[amused] Y si le disparabas a la ventana con la resortera, un guardia se asomaba, te regañaba, y te lanzaba una bomba.",
        "En el remake, los cuadros ya no están. En su lugar hay un tapiz que se va bordando con tu aventura.",
        "[serious] Aonuma lo explicó en Game Informer. No querían que ese momento interrumpiera la experiencia del mundo. Que un jugador nuevo no se preguntara, ¿y por qué está Yoshi aquí?",
        "[playful] Pero no todo se fue. El guardia de la bomba sigue en su sitio. Y el broche de Bowser que lleva Talon en el pecho, también se quedó.",
    ]},
    {"id": "cierre", "frases": [
        "[thoughtful] Así que el remake quita guiños, atajos y secretos. Y a cambio, trae voces, orquesta, el tapiz, y un coliseo para pelear otra vez con los jefes.",
        "[curious] Ahora te pregunto a ti. [short pause] De estas 12 cosas, ¿cuál es la que más vas a extrañar? Te leo en los comentarios.",
        "[warm] Y si quieres ver todo lo que cambió para bien, aquí tienes los 15 cambios del remake frente al original. Nos vemos en Hyrule.",
    ]},
]
