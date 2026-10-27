# -*- coding: utf-8 -*-
"""Crónicas del gaming — «Zelda Ocarina of Time REMAKE: los 15 CAMBIOS frente al ORIGINAL de N64» (26-oct-2026).
Tema elegido por el usuario entre 3 propuestas con datos (`fab.py ideas cronicas_gaming`): Mundo N «Los 35 CAMBIOS de Zelda
Ocarina of Time REMAKE vs. el ORIGINAL» ×14,4 (317 k), N Deluxe «100 cambios…» ×6,5, Mundo N «10 cosas que Nintendo AÚN
ESCONDE…» ×4,7. Variable que cambia respecto a zelda_oot/majora_mask: SOLO el ángulo (comparativa del remake en vez de
historia + secretos); mismo público y misma fórmula (SECUENCIA YT + pegatinas + fichas translúcidas + MG nuevos). Sale el lun
2-nov-2026, 3 días antes del lanzamiento. Voz ElevenLabs Hope con `eleven_v4_turbo` (el usuario, 26-oct: «suena perfecto», mitad
de créditos). Música = banda sonora OFICIAL de Ocarina (regla del 23-oct).

Datos verificados el 26-oct-2026 ([O] oficial de Nintendo; [D] visto en el Direct/demo según la prensa; se dicen como tales):
- [O] nintendo.com «The Legend of Zelda 40th Anniversary celebration revealed in new Nintendo Direct presentation» (8-sep-2026):
  sale el 5-nov, 59,99 US$, solo Switch 2; gráficos rehechos hasta la textura de cada material; acciones más ágiles, cargas
  más rápidas, más fluido; efectos renovados y música orquestal sinfónica; cinemáticas con voz completa y ampliadas, más
  diálogo; lugares remodelados con cámara libre; el ciclo día/noche sigue en todas partes, también en los pueblos; botones
  nuevos para saltar y correr; cámara con el stick derecho; «Threads of Time» (progreso + siguiente objetivo, un gran tapiz que
  se llena); tararear o tocar una canción aprendida al micrófono y Link la toca; ocarina tocable y ocarina eléctrica de HORI
  (este año); amiibo Link niño y Zelda niña (2027) -> máscaras especiales de estilo retro; app ZELDA NOTES (registro del día
  con enemigos derrotados, Gossip Quest con imágenes de pista -> partituras, ocarina virtual con partituras por QR, concurso de
  más de 2 000 preguntas: un intento gratis al día, más con rupias del juego).
- Nintendo of America en YouTube: anuncio «Nintendo Direct 6.9.2026» (r8eMoxo4ipE), «Overview Trailer» (8v8eDMh1o3g),
  «Mr. Aonuma Gameplay Demonstration» (PQvD3p2yGwc, 15:10).
- Aonuma (GamingHQ / toy-people, 11-sep-2026): las pantallas de carga entre ciertas zonas se mantuvieron «a propósito, para
  conservar la esencia del original»; «en gran parte un remake fiel… con controles modernos». Jugadores divididos (2-3 s).
- [D] GameRant (features confirmed): giroscopio para apuntar (como OoT 3D y BotW), esprint (mantener A en tierra, X en el agua),
  Threads of Time opcional. Everything Edinburgh: bolsa inicial 99 -> 200, inventario en cuadrícula con accesos en la cruceta,
  mantener rodar = esprint (adiós a las volteretas), medidor de buceo como barra junto a Link, la Ciudadela con calles nuevas
  y más gente. The Spike: mazmorras nuevas / Hyrule abierto NO confirmados.
- Original: N64, noviembre de 1998; primer 40/40 de Famitsu; Metacritic 99 (el más alto). OoT 3D (2011, Grezzo): pantalla
  táctil, giroscopio. Bolsa de adulto (200) = Casa Skulltula por 10 Skulltulas doradas (Zelda Wiki). Mercado de la Ciudadela =
  fondos prerrenderizados con cámaras fijas, puertas modeladas que no se ven (TCRF); en 3DS ya en 3D real; mod de fans
  «OoT unJPEG» (Reonu) los rehace en 3D para N64 (Time Extension, ago/oct-2026). Botas de hierro en la pantalla de equipo.
"""

TITULO = "Zelda Ocarina of Time REMAKE: los 15 CAMBIOS frente al ORIGINAL de N64"
ARCHIVO = "oot_remake_cambios"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
# Voz del canal (Hope) con el modelo turbo, por defecto desde el 26-oct-2026: corchetes iguales, mitad de créditos.
VOZ = dict(motor="elevenlabs", voice_id="tnSpp4vdxKPjI9w0GnoV", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/banjo_tooie/ref_hope.mp3", tomas=1, stability=0.5)

# ElevenLabs dice el inglés nativo: solo lo que lea mal
FONETICA = {}
# Revisado el 26-oct leyendo voz/eval.json: Whisper escribe «Greso» (Grezzo), «Escúltula/escóltula», «Cacarico», «Yaunuma»
# (y Aonuma) y «59 dólares con 99 centavos» (bien dicho): falsas alarmas. Cola de cierre_4 = ElevenLabs habla hasta el final.
CER_MAX_POR_FRASE = {"contexto_2": .02, "contexto_6": .13, "p15_2": .08, "p9_4": .06}
TAIL_MAX_POR_FRASE = {"cierre_4": 1.05}
GAP_MAX_POR_FRASE = {"contexto_6": .8}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen del gameplay...
    # ...salvo donde conviene OÍR el juego (el usuario, 26-oct-2026: música del juego, gritos de Link, SFX de Zelda): esos
    # beats bajan CON su audio y armar_musica_ost.py aparta la banda sonora ahí (volumen 0,5 = ~10 dB bajo la voz)
    ambiente_por={"scene-001": .6, "scene-017": .6, "scene-023": .5, "scene-024": .5, "scene-041": .5, "scene-043": .5,
                  "scene-050": .9, "scene-051": .9, "scene-054": .7, "scene-059": .8, "scene-060": .8, "scene-062": .8,
                  "scene-063": .8, "scene-064": .8, "scene-065": .9, "scene-067": .6, "scene-068": .6, "scene-075": .7,
                  "scene-076": .6, "scene-077": .6, "scene-080": .6},
    # marco NSO de ZeldaCentral fijado a 0,131 (lección de zelda_oot); 3DS de ZorZelda 0,037 (plan_clips.py)
    recorte_por={'scene-003': 0.131, 'scene-005': 0.131, 'scene-006': 0.131, 'scene-007': 0.131, 'scene-008': 0.037,
                 'scene-015': 0.131, 'scene-016': 0.131, 'scene-017': 0.131, 'scene-021': 0.131, 'scene-026': 0.131,
                 'scene-032': 0.131, 'scene-033': 0.131, 'scene-036': 0.131, 'scene-037': 0.131, 'scene-038': 0.131,
                 'scene-041': 0.131, 'scene-043': 0.131, 'scene-045': 0.131, 'scene-046': 0.131, 'scene-050': 0.131,
                 'scene-054': 0.131, 'scene-058': 0.131, 'scene-062': 0.131, 'scene-066': 0.131, 'scene-067': 0.131,
                 'scene-071': 0.131, 'scene-076': 0.131},
    yt=dict(sufijo="", min_s=30, max_min=1100, alto=1080,
            evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
# Sin Lyria: la música es la banda sonora OFICIAL de Ocarina of Time (armar_musica_ost.py -> audio/musica.wav).
LYRIA = dict(estilo="", escenas={})

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[excited] El 5 de noviembre vuelve Ocarina of Time. [short pause] 28 años después, en Nintendo Switch 2, y con cambios que nadie se atrevió a hacer en 1998.",
        "Link puede saltar cuando quiere. La cámara por fin es tuya. [curious] Y la ocarina se puede tocar tarareando.",
        "[playful] Pero no todo cambió. Hay una cosa del original que Nintendo dejó igual a propósito, y Eiji Aonuma explicó por qué.",
        "Así que hoy te cuento cómo llegamos a este remake, y los 15 cambios más grandes frente al Ocarina of Time de Nintendo 64.",
    ]},
    {"id": "contexto", "frases": [
        "[serious] Primero, un poco de contexto. Ocarina of Time salió en noviembre de 1998, para la Nintendo 64.",
        "Fue el primer juego en sacar un 40 sobre 40 en la revista Famitsu, y todavía hoy es el juego con la nota más alta de Metacritic, un 99.",
        "[curious] No es la primera vez que se rehace. En 2011, Nintendo y el estudio Grezzo lo llevaron a la Nintendo 3DS, con gráficos nuevos y la pantalla táctil para los objetos.",
        "Pero aquello fue un lavado de cara. [short pause] Lo de ahora es otra cosa.",
        "Nintendo lo anunció en su Direct del 9 de junio. Y en septiembre, en el Direct del 40 aniversario de Zelda, publicó una demostración de 15 minutos jugada por el propio Eiji Aonuma.",
        "[impressed] Todo está rehecho, hasta la textura de cada material. Los lugares se remodelaron, el juego va más fluido, y las cargas son más cortas.",
        "Saldrá solo en Switch 2, a 59,99 dólares en Estados Unidos. [short pause] Y Aonuma lo resumió así: un remake en gran parte fiel al original, con controles modernos.",
        "[playful] Fiel, sí. Pero con muchos cambios. Vamos con ellos, del más pequeño al más grande.",
    ]},
    {"id": "p15", "frases": [
        "[excited] Número 15. [short pause] Una bolsa más grande.",
        "En el original, Link empezaba con una bolsa de solo 99 rupias. Y en cuanto querías algo caro, tocaba juntar y esperar.",
        "La primera mejora era la bolsa de adulto, de 200 rupias. Te la daban en la Casa Skulltula de Kakariko, a cambio de 10 Skulltulas doradas.",
        "[curious] En las imágenes del Direct, el contador del remake ya marca 200 desde el principio.",
        "Parece poca cosa. Pero menos viajes para juntar rupias es menos relleno, justo al empezar la aventura.",
    ]},
    {"id": "p14", "frases": [
        "[playful] En el 14, unas figuras que traen máscaras.",
        "Nintendo anunció dos amiibo nuevos para 2027. Link niño, y Zelda niña.",
        "Al usarlos en el remake, desbloquean unas máscaras especiales de estilo retro.",
        "[curious] En el original, las máscaras eran parte de una misión, la de la tienda de máscaras felices. Aquí llegan desde fuera del juego.",
        "Nintendo todavía no ha detallado qué máscaras son, ni si hacen algo más que cambiar el aspecto de Link.",
    ]},
    {"id": "p13", "frases": [
        "[serious] Número 13. [short pause] El cambio que no hicieron.",
        "Las cargas son más rápidas, pero al pasar entre ciertas zonas, sigue habiendo una pantalla de carga.",
        "Y no es un descuido. Aonuma dijo que la mantuvieron a propósito, para conservar la esencia del juego original.",
        "[amused] A muchos jugadores no les convenció. Hay quien cree que es una necesidad técnica, y hay quien dice que esos dos o tres segundos ayudan a separar cada lugar.",
        "[thoughtful] Lo curioso es esto. En 1998, esa pausa era una necesidad del cartucho. En 2026, es una decisión.",
    ]},
    {"id": "p12", "frases": [
        "[curious] En el 12, el juego sale de la consola.",
        "El remake se conecta con Zelda Notes, una sección de la aplicación de Nintendo Switch para el celular.",
        "Guarda un registro de cada día, con datos como los enemigos que derrotaste. Y tiene un juego de encontrar lugares a partir de imágenes de pista.",
        "También te deja tocar una ocarina virtual en la pantalla, y crear partituras para compartirlas con un código QR.",
        "[amused] Y trae un concurso de más de 2000 preguntas. Un intento gratis al día. [short pause] Y si quieres más, pagas con rupias del juego.",
    ]},
    {"id": "p11", "frases": [
        "[thoughtful] Número 11. [short pause] El tiempo ya no se detiene.",
        "En la Nintendo 64, el día y la noche pasaban en el campo de Hyrule. Pero al entrar a sitios como la Ciudadela o el Bosque Kokiri, el reloj se congelaba.",
        "Si querías que se hiciera de noche, tenías que salir al campo, y esperar.",
        "En el remake, el ciclo de día y noche sigue en todas partes, también dentro de los pueblos.",
        "[curious] Así que la plaza del mercado puede cambiar de ambiente mientras estás dentro. Y el pueblo deja de ser una foto fija.",
    ]},
    {"id": "p10", "frases": [
        "[playful] En el 10, un menú nuevo.",
        "En el original solo tenías tres botones C para tus objetos. Para cambiar de arma, pausabas, buscabas en una cuadrícula, y volvías.",
        "[sighs] Las botas de hierro del Templo del Agua son el ejemplo más famoso. Ponerlas, quitarlas, y ponerlas otra vez, siempre desde el menú.",
        "En la demo del remake, el inventario es una cuadrícula que se recorre rápido, con accesos directos en la cruceta.",
        "[curious] Y según quienes analizaron las imágenes, Link puede seguir moviéndose mientras sostiene un objeto.",
    ]},
    {"id": "p9", "frases": [
        "[curious] Número 9. [short pause] Apuntar moviendo el control.",
        "En la Nintendo 64, el tirachinas, el arco y el gancho se apuntaban con el stick, en primera persona.",
        "En el remake se puede apuntar con el giroscopio, moviendo el control o la consola.",
        "[amused] No es nuevo del todo. La versión de 3DS ya lo hacía en 2011, y también Breath of the Wild.",
        "Pero para una Skulltula dorada en lo alto de una pared, es la diferencia entre un tiro y cinco.",
    ]},
    {"id": "p8", "frases": [
        "[impressed] En el 8, un pueblo que por fin es de verdad.",
        "En la Nintendo 64, la plaza del mercado de la Ciudadela de Hyrule no era un escenario en 3D. Eran fondos pintados de antemano, vistos desde cámaras fijas.",
        "Por eso no podías girar la cámara ahí. Y por eso esos fondos esconden detalles raros, como puertas modeladas que nunca llegas a ver.",
        "La versión de 3DS ya la hizo en 3D. Pero en el remake la cámara se mueve libre por la plaza, y en las imágenes se ven calles nuevas y mucha más gente.",
        "[curious] Hasta un mod de fans para la Nintendo 64 está rehaciendo esos fondos en 3D este mismo año. La Ciudadela era una espina clavada para todos.",
    ]},
    {"id": "p7", "frases": [
        "[warm] Número 7. [short pause] Una orquesta para Koji Kondo.",
        "La música original de Koji Kondo la generaba la propia consola, con instrumentos grabados en pequeñas muestras dentro del cartucho.",
        "En el remake, Nintendo habla de música orquestal sinfónica, y de efectos de sonido renovados.",
        "[curious] Lo que todavía no ha dicho es si se podrá elegir la banda sonora original.",
        "[thoughtful] Y es un cambio grande. Porque en Ocarina of Time, la música no es un fondo. Es el centro del juego.",
    ]},
    {"id": "p6", "frases": [
        "[playful] En el 6, adiós a depender de Navi.",
        "[amused] En 1998, si te perdías, la ayuda principal era Navi. [short pause] ¡Hey, escucha!, y una pista que a veces no ayudaba mucho.",
        "El remake trae una función nueva que en inglés se llama Threads of Time, los Hilos del Tiempo.",
        "Te deja revisar en cualquier momento lo que llevas hecho, y cuál es tu siguiente objetivo.",
        "[warm] Y mientras avanzas, se va llenando un gran tapiz con tu aventura. Es opcional. Así que quien quiera perderse como en 1998, puede.",
    ]},
    {"id": "p5", "frases": [
        "[excited] Número 5. [short pause] Hyrule por fin habla.",
        "En la Nintendo 64 todo era texto. Link gritaba al atacar, y poco más.",
        "En el remake, las cinemáticas tienen voces completas, se ampliaron, y los personajes tienen más diálogo.",
        "[curious] Es la primera vez que la historia de Ocarina of Time se cuenta con actores de voz.",
        "Lo que Nintendo no ha aclarado es la pregunta que todos se hacen. [short pause] Si Link dirá una sola palabra.",
    ]},
    {"id": "p4", "frases": [
        "[playful] En el 4, la ocarina, como nunca la tocaste.",
        "En el original, cada canción era una secuencia de botones, con las notas del botón A y los cuatro botones C.",
        "En Switch 2 puedes tararear, o tocar, una canción que ya aprendiste frente al micrófono de la consola. Y Link la toca.",
        "Y el juego responde a dos ocarinas de verdad que salen este año. Una se toca soplando, y la otra, electrónica, de la marca Hori, toca canciones enteras con un botón.",
        "[amused] Así que, por fin, la Canción de Epona puede salir de tu propia voz.",
    ]},
    {"id": "p3", "frases": [
        "[excited] Número 3. [short pause] Correr de verdad.",
        "[amused] En la Nintendo 64, rodar era más rápido que correr. Por eso media generación cruzó Hyrule dando volteretas sin parar.",
        "En el remake, Link tiene un esprint. Mantienes el botón, y corre. Y en el agua, también puede acelerar nadando.",
        "Según quienes analizaron la demo, mantener el botón de rodar ahora lo pone a correr. Así que el truco de las volteretas pierde sentido.",
        "Y el aire al bucear ya no es una cuenta atrás arriba de la pantalla. [short pause] Ahora es una barra, junto a Link.",
    ]},
    {"id": "p2", "frases": [
        "[serious] En el 2, la cámara.",
        "La Nintendo 64 tenía un solo stick. La cámara iba detrás de Link, la centrabas con el botón Z, y para mirar alrededor tenías la vista en primera persona.",
        "En el remake, la cámara es libre. Se maneja con el stick derecho, y da la vuelta completa alrededor de Link.",
        "[curious] Y eso cambia hasta los escenarios. Nintendo dice que los lugares se remodelaron para que la cámara pueda moverse por ellos.",
        "Rincones que en 1998 se pensaron para verse desde un solo ángulo, ahora se pueden mirar desde todos lados.",
    ]},
    {"id": "p1", "frases": [
        "[excited] Y el cambio número 1. [short pause] Link puede saltar.",
        "En Ocarina of Time, Link nunca saltaba cuando tú querías. Saltaba solo, al correr hacia un borde.",
        "En 1998, casi nadie sabía moverse en tres dimensiones, y el salto automático evitaba muchas caídas.",
        "En el remake hay un botón para saltar, cuando y donde tú quieras.",
        "[thoughtful] Parece lo más simple del mundo. Pero todas las mazmorras se diseñaron para un Link que no saltaba. Así que la gran pregunta es qué atajos van a aparecer, y qué tuvo que cambiar Nintendo para que nada se rompa.",
        "[curious] Lo sabremos el 5 de noviembre.",
    ]},
    {"id": "cierre", "frases": [
        "[thoughtful] Y lo que todavía no sabemos también importa.",
        "Nintendo no ha confirmado mazmorras nuevas, ni un campo de Hyrule más grande, ni si vuelve Master Quest, la versión con las mazmorras más difíciles.",
        "Lo confirmado es un remake fiel, con controles modernos, voces, orquesta, y un Link que por fin salta.",
        "[curious] Ahora dime tú en los comentarios. [short pause] ¿Qué cambio te gusta más? ¿Y cuál no debieron tocar?",
        "[warm] Y si quieres saber cómo nació este juego, aquí tienes la historia de Ocarina of Time y sus 12 secretos. Nos vemos en Hyrule.",
    ]},
]
