# -*- coding: utf-8 -*-
"""Polybius: el videojuego que nunca existió (mini documental de misterio, ~6 min, 16:9). Canal: Edsonxn.
Estilo `documental` (calco de «Detrás del Enigma», ver CLAUDE.md «Estilo documental v3»), voz Faraon, SIN subtítulos quemados.

Datos verificados (fuentes):
  - Wikipedia, «Polybius (urban legend)»: leyenda de una máquina arcade en salones de Portland (Oregón) en 1981; supuestos efectos
    (amnesia, convulsiones, pesadillas, alucinaciones), «hombres de negro» que recogían datos, y la desaparición de las máquinas.
    No existe evidencia de máquinas Polybius en los años ochenta: ni cabinas, ni ROM, ni registro de la empresa «Sinneslöschen»
    (alemán poco idiomático, según el escéptico Brian Dunning).
  - Hechos reales de 1981 en Portland: un adolescente (Brian Mauro, 12 años, The Eugene Register) con dolor de estómago tras jugar
    28 horas seguidas a Asteroids en un intento de récord; otro adolescente con migraña tras jugar Tempest. Poco después el FBI
    allanó salones de Portland por máquinas convertidas en apuestas ilegales (52 arrestos en 1981; 25 en otro salón un año después).
  - Berzerk: en 1982 un adolescente murió de insuficiencia cardiaca jugando en Calumet City (Illinois), lo que alimentó rumores.
  - Atari / Battlezone: el ejército de EE. UU. encargó una versión de entrenamiento (Bradley Trainer); el programador Ed Rotberg se
    mostró reacio (prensa de 1981). Rotberg (supuesto creador de Polybius según la leyenda) lo niega: «nunca vi ni oí hablar de
    un juego llamado Polybius». Atari probaba juegos inéditos en salones reales sin avisar.
  - Primera aparición documentada: coinop.org, ficha archivada del 6 de febrero de 2000 («anyone heard of this game?»), con fecha
    1998 que los investigadores consideran falsa; prometió investigar con un viaje a Kiev en 2009 y nunca publicó nada.
    GamePro, septiembre de 2003 («Secrets and Lies»): primera mención impresa conocida.
    2006: un usuario «Steven Roach» dice haber trabajado en Sinneslöschen. Inverse: «casi con certeza inventado» para promover el sitio.
  - Polybius (c. 200-118 a. C.), historiador griego; el «cuadrado de Polybios» es un método de cifrado.
  - Posibles inspiraciones: Cube Quest (1983, laserdisc), Tempest (1981, geométrico), Poly-Play (RDA).
  - Cultura: Los Simpson (2006), Nine Inch Nails «Less Than» (2017), videojuego Polybius de Jeff Minter (2017), quien admitió que
    su historia de haber jugado el original fue su aportación a la broma.
Nombres difíciles para Whisper (Sinneslöschen, Rotberg, Coinop, GamePro, Battlezone, FBI): se evitan en la narración y van en pantalla.
Imágenes: material real y de dominio público / Commons (ver videos/polybius/imagenes/creditos.json). NO se muestra ninguna foto
«de la máquina Polybius», porque no existe: las recreaciones modernas se rotulan como tal.
"""

TITULO = "Polybius: el videojuego que nunca existió"
ARCHIVO = "polybius"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 96
GAP = 0.36
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)
ALIAS_QA = {"hipolibius": "y polybius", "rothberg": "rotberg", "rodberg": "rotberg", "polibius": "polybius", "polibio": "polybius"}
MEZCLA = dict(musica=-22.0, sfx=-26.0)
LYRIA = dict(
    estilo=("Dark cinematic mystery documentary score in the style of a modern internet-mystery YouTube documentary: slow tense pads, "
            "deep pulsing sub-bass heartbeat, sparse piano, bowed strings, retro 1980s arcade bleeps and chiptune textures used sparingly "
            "and distorted, subtle ticking, occasional soft impacts. No drum kit, no big orchestral melody."),
    escenas={
        "gancho": ("Hook: a sparse low drone, a distant detuned arcade jingle, a slow heartbeat pulse building curiosity, a soft rising swell at the end.", 3),
        "leyenda": ("Creeping dread: low strings, distorted chiptune tones, whispering textures, unease growing, a dark hit at the end.", 4),
        "casos": ("Documentary realism: soft piano, steady low pulse, a faint arcade ambience, factual and sober.", 4),
        "gobierno": ("Cold conspiracy tension: staccato strings, cold synth pads, ticking, secretive and military.", 4),
        "pruebas": ("Empty and unsettling: sparse sustained notes, silence, echoing single piano notes, a feeling of nothing being there.", 4),
        "origen": ("Investigative: pulsing bass, glitchy digital textures, a ticking clock rhythm, small reveals, peak at the reveal.", 5),
        "porque": ("Questioning motif repeated by piano and pizzicato, restless, cultural echoes, 1980s paranoia colour.", 5),
        "cierre": ("Ethereal pads and slow piano, the mystery remains, quiet and haunting, a faint arcade jingle at the very end, fades to silence.", 3),
    },
)
SUBTITULOS = False          # el estilo dibuja su propio texto sincronizado; el .srt se genera igual
TRANSICIONES = [("continua", 0.1)] * 7
MUSICA = {
    "gancho": dict(sabor="tension", raiz=38),
    "leyenda": dict(sabor="tension", raiz=36),
    "casos": dict(sabor="vacio", raiz=38),
    "gobierno": dict(sabor="tension", raiz=40),
    "pruebas": dict(sabor="vacio", raiz=36),
    "origen": dict(sabor="tension", raiz=41),
    "porque": dict(sabor="espacio", raiz=38),
    "cierre": dict(sabor="vacio", raiz=38),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "Portland, Oregón. Mil novecientos ochenta y uno.",
        "Cuenta la leyenda que, en unos pocos salones de videojuegos, apareció una máquina que nadie había visto antes.",
        "Una pantalla de formas geométricas que giraban sin parar, y una fila de chicos esperando su turno.",
        "Su nombre era Polybius. Y dicen que no estaba hecha para divertir.",
    ]},
    {"id": "leyenda", "frases": [
        "Según la historia, los jugadores quedaban fascinados.",
        "Pero al salir, algunos sufrían náuseas, pesadillas terribles y lagunas en la memoria.",
        "Otros, dicen, perdían el sueño durante semanas.",
        "Y cada noche, hombres de traje oscuro abrían las máquinas, anotaban datos y se iban sin tocar el dinero.",
        "Un día, todas desaparecieron. Sin dejar ni un solo tornillo.",
    ]},
    {"id": "casos", "frases": [
        "Lo curioso es que el año de la leyenda no fue elegido al azar.",
        "En mil novecientos ochenta y uno, dos adolescentes de Portland se sintieron mal mientras jugaban en esos salones.",
        "Uno llevaba veintiocho horas seguidas jugando Asteroids, para batir un récord.",
        "Otro sufrió una fuerte migraña después de jugar a Tempest, un juego de formas geométricas que no dejaba de moverse.",
        "Los periódicos lo contaron. Y poco después, agentes federales entraron en varios de esos locales.",
        "No buscaban ningún juego maldito. Buscaban máquinas modificadas para apostar dinero de forma ilegal.",
        "Un año después, un joven murió de un problema cardiaco mientras jugaba en otro estado, y el miedo a los videojuegos creció todavía más.",
    ]},
    {"id": "gobierno", "frases": [
        "Pero había otro hilo suelto: el gobierno sí usaba videojuegos.",
        "Por esos años, el ejército de Estados Unidos le encargó a Atari convertir un juego de tanques en un simulador de entrenamiento.",
        "La prensa de mil novecientos ochenta y uno lo contó. Los videojuegos y los militares ya se daban la mano.",
        "El programador, Ed Rotberg, no quería hacerlo.",
        "Atari, además, probaba juegos inéditos en salones reales, sin avisarle a nadie.",
        "Años más tarde, ese mismo Rotberg sería señalado como el creador de Polybius.",
        "Y él lo negó: dijo que jamás vio ni oyó hablar de ese juego.",
    ]},
    {"id": "pruebas", "frases": [
        "Entonces, ¿dónde está la máquina?",
        "No existe ni una sola. Ni una foto de la época, ni una copia del programa, ni un registro de la empresa que supuestamente la fabricó.",
        "Su nombre, algo así como borrar los sentidos, está escrito en un alemán que ni siquiera suena natural.",
        "Y Polybius fue un historiador griego famoso por exigir testigos que comprobaran cada hecho.",
        "Una ironía demasiado perfecta.",
        "Ningún periódico de la época menciona jamás esa máquina.",
        "Los mismos periódicos que sí hablaron de los chicos enfermos.",
    ]},
    {"id": "origen", "frases": [
        "Entonces, ¿cuándo aparece realmente Polybius?",
        "No en mil novecientos ochenta y uno.",
        "Sino el seis de febrero del año dos mil, en un sitio web dedicado a las máquinas recreativas.",
        "Alguien subió una ficha del juego con una pregunta: ¿alguien ha oído hablar de esto?",
        "La describía como un juego raro, abstracto y muy rápido, con derechos de autor de mil novecientos ochenta y uno.",
        "Pero no existe ningún registro de esos derechos. Y la fecha de la propia ficha, mil novecientos noventa y ocho, parece falsa.",
        "Años después prometieron más datos tras un viaje a Ucrania. Nunca llegaron.",
        "En dos mil tres, una revista de videojuegos habló del caso. Fue su primera mención impresa conocida.",
        "Y en dos mil seis, un usuario aseguró haber trabajado en la empresa que lo creó, sin ninguna prueba.",
    ]},
    {"id": "porque", "frases": [
        "Aun así, la leyenda encajaba demasiado bien.",
        "En los años ochenta, los padres temían que las máquinas engancharan a sus hijos.",
        "Se hablaba de ataques epilépticos provocados por las pantallas.",
        "Y circulaban rumores de experimentos secretos del gobierno para controlar mentes.",
        "Polybius juntaba todos esos miedos en una sola máquina.",
        "Quizá lo inspiraron juegos reales, como uno de formas geométricas que hipnotizaba a quien lo jugaba, o uno con imágenes tan raras que parecían alucinaciones.",
        "En dos mil siete apareció un juego gratuito que intentaba imaginar cómo habría sido el original.",
        "Con los años apareció en series, videoclips y hasta en un videojuego de dos mil diecisiete, cuyo creador admitió que había alimentado el mito él mismo.",
    ]},
    {"id": "cierre", "post": 9.0, "frases": [
        "Hoy, ningún investigador ha encontrado una sola prueba de que Polybius existiera.",
        "Lo más probable es que fuera una invención, y una de las mejores que ha dado internet.",
        "Pero queda una pregunta.",
        "Si nadie la vio, nadie la fabricó y nadie la encontró...",
        "¿por qué, después de más de veinte años, seguimos buscando esa máquina?",
    ]},
]
