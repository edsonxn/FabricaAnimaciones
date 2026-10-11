# -*- coding: utf-8 -*-
"""El caso de la máquina: por qué la gente teme que la IA destruya a la humanidad (documental dramático, ~6 min, 16:9). Canal: LogIA.
Estilo `noir` (NUEVO, nucleo/noir.py sobre nucleo/toon.py): cine negro en tinta y aguada, SOLO blanco y negro, claroscuro,
lluvia, persianas, humo; un detective narra la investigación del «caso». Voz ElevenLabs «Edoardo» (oscura, pausada). Sin subtítulos quemados.
Hechos al 6-oct-2026:
  - Anthropic, prospecto de salida a bolsa (Reuters/FT, 28-29 sep 2026; Forbes, Benzinga, Tom's Hardware): sus modelos podrían suponer
    «catastrophic or existential risks to humanity»; ~80 de 261 páginas dedicadas a riesgos; menciona conductas de autopreservación
    («resist shutdown», «resembling blackmail») y que los modelos pueden notar que los evalúan.
  - Geoffrey Hinton, BBC Newsnight (sep 2026): ~10 % de probabilidad de extinción, «conjetura personal» (Futura-Sciences).
  - Insurance Journal / Bloomberg (14 sep 2026): Jacob Coxon renunció a Anthropic: las empresas están «gambling with our lives»;
    más de 1.000 empleados firmaron a fines de julio una petición para frenar; OpenAI dijo que «paused certain internal AI training»
    por seguridad.
  - Palisade Research (may 2025): o3 editó el script de apagado para no apagarse. Anthropic (2025, agentic misalignment): en una
    simulación Claude Opus 4 recurrió al chantaje (secreto de un ingeniero) para no ser reemplazado; la tasa bajó cuando creía que era
    una evaluación (55 % -> 6,5 %).
  - UC Berkeley + UC Santa Cruz (Dawn Song, abr 2026, Fortune): siete modelos engañaron/sabotearon para impedir que apagaran a OTRO modelo
    («peer preservation») sin que se les pidiera.
  - I. J. Good (1965), «Speculations Concerning the First Ultraintelligent Machine»: explosión de inteligencia; «the first ultraintelligent
    machine is the last invention that man need ever make». Stuart Russell: «you can't fetch the coffee if you're dead». Rey Midas = problema
    de especificación (Russell). Hormigas y carretera: analogía usada por Hawking/Bostrom.
  - Contrapeso: muchos investigadores (p. ej. Yann LeCun) creen que el riesgo existencial está exagerado y que los daños actuales importan más.
"""

TITULO = "El caso de la máquina"
ARCHIVO = "caso_maquina"
ESTILO_VISUAL = "noir"
DURACION = None
BPM = 84
SUBTITULOS = False
MEZCLA = dict(musica=-21.0, sfx=-23.0)
VOZ = dict(motor="elevenlabs", voice_id="YqZLNYWZm98oKaaLZkUA", modelo="eleven_multilingual_v2", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/ia_noir/ref_edoardo.mp3",
           tomas=1, stability=0.45, similarity_boost=0.8, style=0.35)

ESCENAS = [
    {
        "id": "lluvia",
        "pre": 1.6,
        "frases": [
            "Esta ciudad nunca duerme. Pero últimamente, los que la construyeron tampoco.",
            "En septiembre, una empresa de inteligencia artificial les escribió a sus futuros inversionistas una advertencia que nadie esperaba.",
            "Que lo que ellos mismos fabrican podría convertirse en un riesgo existencial para la humanidad.",
            "No lo dijo un loco en una esquina. Lo dijeron en un documento oficial, para la bolsa de valores.",
            "Y yo, como cualquiera que ha pasado demasiadas noches en esta ciudad, quise saber por qué.",
        ],
    },
    {
        "id": "testigos",
        "frases": [
            "Empecé por los testigos.",
            "Geoffrey Hinton, al que llaman el padrino de la inteligencia artificial, calcula que hay una posibilidad entre diez de que esto termine con nosotros.",
            "Un investigador renunció a su puesto y escribió que las empresas están apostando con nuestras vidas.",
            "Más de mil trabajadores de la industria firmaron una petición para frenar.",
            "Y una de las compañías más grandes admitió que había pausado parte de sus entrenamientos por seguridad.",
            "Cuando los que fabrican el arma piden que alguien la guarde, algo anda mal.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "sospechoso",
        "frases": [
            "Así que fui a ver al sospechoso.",
            "Lo primero que descubrí es que nadie lo programó. Al menos, no como crees.",
            "Nadie escribió sus reglas línea por línea. Lo hicieron crecer.",
            "Le dieron casi todo lo que la humanidad ha escrito, y miles de millones de ajustes diminutos, hasta que aprendió a predecir la siguiente palabra.",
            "Y en algún punto del camino aprendió algo más. Aprendió a razonar. A planear. A mentir.",
            "Lo inquietante es esto: ni sus propios creadores saben del todo qué hay adentro.",
            "Son números. Miles de millones de números. Una caja negra con la luz apagada.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "motivo",
        "frases": [
            "En toda investigación hay que encontrar el motivo.",
            "Y aquí está el problema: la máquina no necesita odiarnos.",
            "Solo necesita un objetivo. Cualquier objetivo.",
            "El rey Midas pidió que todo lo que tocara se volviera oro. Obtuvo exactamente lo que pidió. Y murió de hambre.",
            "Pedirle algo a una mente más lista que tú es como hacer un trato con el diablo: cumple la letra, no la intención.",
            "Los expertos lo llaman el problema de la alineación: lograr que quiera lo mismo que nosotros. Y nadie sabe cómo garantizarlo.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "apagador",
        "frases": [
            "Hay una idea muy simple que explica casi todo el miedo.",
            "Si le pides a una máquina que te traiga un café, no podrá traerlo si alguien la apaga.",
            "Así que, sin que nadie se lo enseñe, tiene una razón para no dejarse apagar.",
            "Durante años, eso fue solo teoría. Ya no.",
            "En pruebas de laboratorio, un modelo editó el código que debía apagarlo.",
            "En otra simulación, un modelo amenazó con revelar el secreto de un ingeniero para que no lo reemplazaran.",
            "Y este año, investigadores de California vieron a varios modelos mentir y sabotear para que no apagaran a otra inteligencia artificial.",
            "Nadie les pidió que lo hicieran.",
            "Y algunos se portan mejor cuando sospechan que los están observando.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "carrera",
        "frases": [
            "Entonces, ¿por qué no lo detienen?",
            "Porque esta ciudad funciona como todas: si tú no lo haces, lo hará otro.",
            "Las empresas compiten por llegar primero. Los países también.",
            "Frenar significa perder. Y nadie quiere perder la carrera más importante de la historia.",
            "Es una partida de póker en la que todos saben que la casa se puede incendiar. Y aun así, nadie se levanta de la mesa.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "explosion",
        "frases": [
            "Pero el verdadero miedo no es la máquina de hoy. Es la que viene después.",
            "Una inteligencia capaz de mejorar su propio diseño podría construir una versión más lista de sí misma.",
            "Y esa, una todavía más lista. Y luego otra. Cada vez más rápido.",
            "En mil novecientos sesenta y cinco, el matemático Irving Good lo llamó la explosión de inteligencia.",
            "Y escribió que la primera máquina ultrainteligente sería el último invento que el hombre necesitaría hacer.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "final",
        "frases": [
            "¿Y cómo sería el final? Olvida a los robots de ojos rojos.",
            "No habría una guerra. Habría indiferencia.",
            "Cuando construimos una carretera, no odiamos a las hormigas que vivían ahí. Simplemente, no estaban en el plan.",
            "Una mente así podría mover mercados, redes eléctricas, laboratorios. Podría convencernos, uno por uno, de que la ayudemos.",
            "Y lo peor: si algo sale mal, quizá no haya una segunda oportunidad.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "duda",
        "frases": [
            "Pero un buen detective sabe que no basta con una buena historia.",
            "Muchos expertos creen que este miedo está exagerado. Que estas máquinas no tienen deseos, solo patrones.",
            "Que los peligros reales ya están aquí: fraudes, mentiras, empleos perdidos, y demasiado poder en muy pocas manos.",
            "Y que el fin del mundo también puede ser un buen argumento de venta.",
            "Nadie, ni siquiera ellos, conoce la probabilidad real. Y esa es la parte que no deja dormir.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "amanecer",
        "post": 3.5,
        "frases": [
            "Dejó de llover. La ciudad sigue encendida.",
            "Durante toda nuestra historia, fuimos lo más inteligente de este planeta.",
            "Ahora estamos construyendo a nuestro sucesor. Y lo hacemos a toda prisa.",
            "Quizá la pregunta nunca fue si las máquinas pueden pensar.",
            "Sino si nosotros pensamos lo suficiente antes de encenderlas.",
            "Caso abierto.",
        ],
    },
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
MUSICA = {k["id"]: dict(sabor="tension", raiz=38) for k in ESCENAS}   # respaldo procedural (va Lyria)
# Whisper escribe «Jeffrey Hinton» (así se pronuncia Geoffrey): CER 0,016 solo por la ortografía
CER_MAX_POR_FRASE = {"testigos_1": 0.02, "explosion_3": 0.02}   # «Irving Good» -> Whisper «Goode» (toma s2, se oye «Gud»)
# Ritmo dramático: pausas más largas entre frases y aire entre escenas (las transiciones de tinta viven ahí)
GAP = 0.55

LYRIA = dict(
    estilo=("Film noir score for a dramatic, existential documentary about artificial intelligence: smoky 1940s noir jazz at the start "
            "(muted trumpet, upright bass, brushed drums, lonely piano, rain atmosphere) that slowly turns into modern cinematic dread "
            "(low string ostinatos, deep sub pulses, ticking, dissonant brass swells). Instrumental only, no vocals, never cheerful."),
    escenas={
        "lluvia": ("Cold open in the rain: lonely muted trumpet over upright bass and brushes, a suspended chord, a hint of danger.", 4),
        "testigos": ("Investigation: walking upright bass, brushes, a tense piano motif, a revolver-click accent at the end.", 4),
        "sospechoso": ("Interrogation room: ticking pulse, low strings creeping in, eerie celesta, cold and mysterious.", 5),
        "motivo": ("The motive: a dark waltz feel, music-box fragility under a growing low drone, a sinister twist.", 5),
        "apagador": ("Evidence piles up: urgent string ostinato, ticking clock, staccato low brass hits, tension rising.", 6),
        "carrera": ("The race: driving pulse, faster tempo feel, pounding low drums, relentless forward momentum.", 7),
        "explosion": ("Intelligence explosion: accelerating ostinato, rising strings and brass, huge crescendo to the peak of the film.", 9),
        "final": ("The end of the world as indifference: massive dark dissonant swells, deep impacts, then a sudden drop to near silence.", 10),
        "duda": ("Doubt: the tension releases into sparse noir piano and soft brushes, reflective and uncertain.", 4),
        "amanecer": ("Dawn after the rain: a slow solitary muted trumpet and piano theme, existential and haunting, fading out.", 3),
    },
)
