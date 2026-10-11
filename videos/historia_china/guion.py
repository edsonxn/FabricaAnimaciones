# -*- coding: utf-8 -*-
"""La historia de China en 3 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa que se rompe y se reúne).

Hilo narrativo: el «ciclo dinástico» (Mandato del Cielo): un imperio que se une, se corrompe, se rompe y vuelve a unirse.

Datos y fuentes (todo verificable en Britannica / Cambridge History of China / UNESCO / Banco Mundial):
  - Dinastía Shang (~1600-1046 a. C.): huesos oraculares = la escritura china más antigua que se conserva (UNESCO, Memoria del Mundo).
  - Zhou (1046-256 a. C.): «Mandato del Cielo». Periodo de los Reinos Combatientes: siete grandes estados. Confucio (551-479 a. C.).
  - Qin Shi Huang unifica China en 221 a. C. (escritura, moneda, pesos y medidas, ancho de los ejes de los carros); une murallas
    del norte; ejército de terracota (miles de figuras, mausoleo UNESCO); muere en 210 a. C. y la dinastía cae en 206 a. C.
  - Han (206 a. C.-220 d. C.): Ruta de la Seda (desde ~130 a. C.); papel perfeccionado por Cai Lun (105 d. C.). Tres Reinos en 220.
  - Sui reunifica en 589; Gran Canal (605-609), el canal artificial más largo del mundo; Tang (618-907): Chang'an ~1 millón de
    habitantes; pólvora descubierta por alquimistas taoístas (siglo IX).
  - Song (960-1279): papel moneda, imprenta de tipos móviles (Bi Sheng, ~1040), brújula magnética para navegar.
  - Yuan (1271-1368): Kublai Kan, nieto de Gengis Kan; conquista total de los Song en 1279.
  - Ming (1368-1644): Zhu Yuanzhang, campesino huérfano; Ciudad Prohibida (1406-1420); expediciones de Zheng He (1405-1433) con
    cientos de barcos, casi noventa años antes de Colón (1492); Gran Muralla de ladrillo.
  - Qing (1644-1912): manchúes en Pekín en 1644; mayor extensión territorial; Guerra del Opio (1839-42), Tratado de Nankín: Hong
    Kong cedido a Gran Bretaña (1842); Puyi abdica en 1912 con seis años.
  - República (1912); invasión japonesa (1937); República Popular (1 oct 1949, Mao); Gran Salto Adelante (1958-62, hambruna);
    Mao muere en 1976; reformas de Deng Xiaoping desde 1978 («no importa que el gato sea blanco o negro...»); Banco Mundial:
    cientos de millones salieron de la pobreza extrema; ~1.400 millones de habitantes; mayor red de tren de alta velocidad del mundo.
"""

TITULO = "La historia de China en 3 minutos"
ARCHIVO = "historia_china_3min"
ESTILO_VISUAL = "boceto"
DURACION = 190
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)
# Whisper escribe a su manera los nombres chinos/mongoles que Dan pronuncia bien: equivalencias para el control de calidad
ALIAS_QA = {"the king": "de qin", "king": "qin", "chou": "zhou", "zo": "zhou", "kou": "zhou", "san": "han", "genghis": "gengis", "khan": "kan"}
SUBTITULOS = False            # los subtítulos manuscritos los dibuja la propia escena
TRANSICIONES = [("continua", 0.1)] * 12
MUSICA = {
    "gancho": dict(sabor="lounge", raiz=41),
    "rio": dict(sabor="lounge", raiz=41),
    "zhou": dict(sabor="lounge", raiz=43),
    "qin": dict(sabor="lounge", raiz=43),
    "han": dict(sabor="lounge", raiz=41),
    "tang": dict(sabor="esperanza", raiz=43),
    "song": dict(sabor="lounge", raiz=43),
    "yuan": dict(sabor="lounge", raiz=41),
    "ming": dict(sabor="lounge", raiz=43),
    "qing": dict(sabor="lounge", raiz=41),
    "moderna": dict(sabor="lounge", raiz=43),
    "cierre": dict(sabor="esperanza", raiz=41),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Un imperio que se rompió una y otra vez, y siempre volvió a unirse.",
        "Esta es la historia de China, en tres minutos.",
    ]},
    {"id": "rio", "frases": [
        "Todo empieza junto a un río amarillo, hace unos cuatro mil años.",
        "Aldeas de agricultores cultivan mijo y arroz.",
        "Nacen los primeros reyes: la dinastía Shang.",
        "Sus adivinos graban preguntas en huesos y los echan al fuego: es la escritura china más antigua.",
    ]},
    {"id": "zhou", "frases": [
        "Después llegan los Zhou, con una idea poderosa: el Mandato del Cielo.",
        "El rey manda mientras el cielo lo apruebe. Si gobierna mal, cae.",
        "Y cae: el reino se parte en siete estados que pelean durante siglos.",
    ]},
    {"id": "qin", "frases": [
        "Hasta que el rey de Qin los conquista a todos.",
        "En doscientos veintiuno antes de Cristo, nace el primer emperador.",
        "Unifica la escritura, la moneda, y hasta el ancho de los ejes de los carros.",
        "Une las murallas del norte, y se hace enterrar con un ejército de barro.",
        "Pero su imperio apenas le sobrevive cuatro años.",
    ]},
    {"id": "han", "frases": [
        "Llegan los Han, y China se abre al mundo.",
        "Por la Ruta de la Seda, caravanas de camellos llevan seda hasta Roma.",
        "Pero vuelven la corrupción y las rebeliones, y el imperio se rompe en tres reinos.",
    ]},
    {"id": "tang", "frases": [
        "Casi cuatrocientos años después, China vuelve a unirse.",
        "Con los Tang llega la edad de oro: poetas, bailarinas, y una capital de un millón de personas.",
        "Unos alquimistas buscan la vida eterna, y en su lugar inventan la pólvora.",
    ]},
    {"id": "song", "frases": [
        "Con los Song, China es la región más avanzada del planeta.",
        "Inventa el papel moneda y la imprenta de tipos móviles, y navega guiada por la brújula.",
    ]},
    {"id": "yuan", "frases": [
        "Pero del norte llega una tormenta de jinetes: los mongoles.",
        "Un nieto de Gengis Kan conquista toda China, y funda la dinastía Yuan.",
    ]},
    {"id": "ming", "frases": [
        "Un campesino huérfano los expulsa, y funda los Ming.",
        "Levantan la Ciudad Prohibida y la Gran Muralla de ladrillo.",
        "Su almirante zarpa con cientos de barcos gigantes, casi un siglo antes que Colón.",
        "Y de pronto, China le da la espalda al mar.",
    ]},
    {"id": "qing", "frases": [
        "En mil seiscientos cuarenta y cuatro, los manchúes entran en Pekín.",
        "Nace la dinastía Qing, y China se hace más grande que nunca.",
        "Pero Europa ya tiene vapor y cañones, y quiere comprar té y seda.",
        "Los ingleses pagan con opio. Cuando China intenta frenarlos, estalla la Guerra del Opio.",
        "China pierde, y Hong Kong pasa a manos británicas.",
        "Y en mil novecientos doce, abdica el último emperador: un niño de seis años.",
    ]},
    {"id": "moderna", "frases": [
        "Terminan más de dos mil años de emperadores, y llegan las guerras entre caudillos, la invasión japonesa y la guerra civil.",
        "En mil novecientos cuarenta y nueve, Mao proclama la República Popular China.",
        "Sus campañas, como el Gran Salto Adelante, provocan una hambruna terrible.",
        "Muere Mao, y su sucesor abre la economía: da igual el color del gato, mientras cace ratones.",
        "En cuarenta años, cientos de millones salen de la pobreza, y China se vuelve la segunda economía del mundo.",
        "Hoy tiene mil cuatrocientos millones de habitantes, y la red de trenes rápidos más grande del planeta.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Se rompió, se unió, se rompió otra vez, y aquí sigue, después de tres mil años.",
        "¿Qué país quieres ver en tres minutos? Dímelo en los comentarios.",
    ]},
]


# Música con Lyria (nucleo/lyria.py): estilo chino moderno y juguetón, con hueco para la voz; un bloque por escena
LYRIA = dict(
    estilo=("Playful yet epic animated-history documentary score blending traditional Chinese instruments (guzheng, pipa, erhu, bamboo flute, "
            "taiko and wood blocks) with a light modern pulse, in the feel of a fast-moving illustrated history explainer. Bright, rhythmic, "
            "constantly evolving, with short stingers at scene changes. Pentatonic melodies kept low so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: plucked guzheng motif over a light ticking pulse, curiosity building, a cheeky rise and a bright hit at the end.", 5),
        "rio": ("Sunrise by the Yellow River: soft bamboo flute and gentle guzheng arpeggios, warm pastoral rhythm, a small gong, then a low ritual drum.", 3),
        "zhou": ("Regal and then falling apart: wooden blocks and plucked strings, a dramatic drop, a cracking rhythm, restless and unstable.", 5),
        "qin": ("Conquest and power: deep taiko drums, marching low strings, determined rhythm, a big hit for the first emperor, then a sudden fading ending.", 7),
        "han": ("Adventurous caravan on the Silk Road: erhu melody, hand drums with a walking camel rhythm, open and curious, then tension and a break.", 5),
        "tang": ("Golden age: elegant pipa and guzheng dance, light and festive, then a comic bubbling alchemy section and a big firework explosion.", 6),
        "song": ("Inventive clockwork curiosity: marimba and wood blocks, bright playful pizzicato, ideas clicking into place.", 5),
        "yuan": ("Storm of horsemen: galloping drums, horse-head fiddle, urgent and stormy, rising to a triumphant dark power chord.", 8),
        "ming": ("Majestic palace theme with gongs, then sweeping seafaring strings and flute for the voyage, then a door-slam silence and low closing tone.", 6),
        "qing": ("Dramatic tension: war drums, cannon-like hits, bitter strings, a sad small melody for the child emperor at the end.", 7),
        "moderna": ("Chaos of war with snare and taiko, a solemn pause, then a tense ticking build, then optimistic modern pulses and plucked synth climbing to a triumphant finish.", 7),
        "cierre": ("Playful resolving outro: pentatonic theme returns brightly, light percussion, friendly and inviting, a final warm chord and fade.", 5),
    },
)
