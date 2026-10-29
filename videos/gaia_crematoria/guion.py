# -*- coding: utf-8 -*-
"""La Crematoria: dos padres, dos hijos y una espada — Canal Gaia Eterna (gaia_eterna), 16:9, 40+ min, terror + heroísmo.

Pedido del usuario (29-oct-2026): primer video de Gaia Eterna (canal de su esposa) con el estilo de «Pamela» (`videos/wow_darrowshire/`:
pegatina Flow + pegatinas reales del juego, docs/estilo_pegatina_flow.md § 8), 40 min MÍNIMO, MAPAS REALES con ruta en algunas escenas
(nucleo/mg_mapa.py, tema "wow"), VARIAS VOCES de ElevenLabs para los personajes con emociones (VOZ_POR_FRASE) y SFX DEL JUEGO.
Narradora = la voz clonada de la dueña del canal. Tema elegido entre 3 con datos (canales/formula/gaia_eterna.md).

Lore: `fuentes_lore.md` (verificado el 29-oct con warcraft.wiki.gg por su API + nombres oficiales es de los tooltips de Wowhead).
Canon que se sigue: el cómic «Ashbringer» (Neilson) + Chronicle vol. 3 + las misiones de Classic/WotLK; lo de Classic que el cómic
desplazó se cuenta como «lo que vivieron los jugadores» (Ribalimpia, el evento del Monasterio). Los diálogos son ADAPTACIONES al
español de las líneas del juego y del cómic (las oficiales en español no se pudieron verificar), cortas y en voz de cada personaje.
NO se afirma: el orden exacto entre la muerte de Taelan y la primera batalla de la Capilla; quién bautizó la espada en TBC (se cuenta
la del cómic); fechas más allá de las de Chronicle (22, 25 y 27 tras el Portal Oscuro).

Estructura: los actos viven en `actos_1.py`, `actos_2.py`, `actos_3.py` (una lista ACTOS cada uno). En cada acto, `frases` mezcla
textos de la narradora (str) y líneas de personaje («(personaje, texto)»); aquí se aplanan a ESCENAS (solo str) y VOZ_POR_FRASE
(«<id>_<i>»: voz del personaje). `plan` = notas visuales/mapa/SFX para el tramo de escenas (el núcleo las ignora).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from actos_1 import ACTOS as _A1  # noqa: E402
from actos_2 import ACTOS as _A2  # noqa: E402
from actos_3 import ACTOS as _A3  # noqa: E402

TITULO = "La Crematoria: dos padres, dos hijos y una espada maldita"
ARCHIVO = "gaia_crematoria"
ESTILO_VISUAL = "pegatina_flow"
DURACION = None
BPM = 66
GAP = 0.45
# Narradora: voz clonada de la dueña del canal («Zyan gameplay 2»), SOLO en la cuenta 2 de ElevenLabs (tts_eleven salta sola).
VOZ = dict(motor="elevenlabs", voice_id="BwV6RplmLHPGm7QVf6II", modelo="eleven_v4_turbo", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/gaia_prueba_voz/muestras/19_mezcla_parrafo.mp3",
           tomas=1, stability=0.5)
# Reparto elegido por el usuario el 29-oct-2026 en `casting.html` (biblioteca pública de ElevenLabs, todas en español).
VOCES = {
    "alexandros": "t3eeeqhBjrUqcrPvDqUn",   # Salvatore (épica, grave)
    "tirion": "gSYqSbtMajxq5LUT0bNl",       # Elder (firme, de anciano)
    "renault": "iDEmt5MnqUotdwCIVplo",      # Enrique Mondragón
    "darion": "byWOh4ohcovt7I8koF2I",       # Alejandro (joven, ronca)
    "taelan": "htFfPSZGJwjBv1CL0aMD",       # Antonio (joven, suave)
    "isillien": "OLmSqlYzB06EIKJRy5b0",     # Murdock (villano)
    "kelthuzad": "UFO0Yv86wqRxAt1DmXUu",    # Mordred (villano sarcástico)
    "rey_exanime": "k8cFOyAg7B9qwBlDDNTC",  # Miguel (de tráiler)
    "eitrigg": "GTY55jD77hLBRrnQOhNk",      # Ludovico (grave)
}
# Voces que llevan tratamiento en la mezcla (eco/reverberación de ultratumba): muerto o no-muerto.
VOCES_ULTRATUMBA = ("kelthuzad", "rey_exanime")

ACTOS = _A1 + _A2 + _A3
ESCENAS, VOZ_POR_FRASE, PERSONAJE_POR_FRASE = [], {}, {}
for _a in ACTOS:
    _fr = []
    for _i, _f in enumerate(_a["frases"]):
        if isinstance(_f, tuple):
            _per, _f = _f
            VOZ_POR_FRASE[f"{_a['id']}_{_i}"] = VOCES[_per]
            PERSONAJE_POR_FRASE[f"{_a['id']}_{_i}"] = _per
        _fr.append(_f)
    ESCENAS.append({k: v for k, v in _a.items() if k not in ("frases", "plan")} | {"frases": _fr})

MEZCLA = dict(musica=-20.0, sfx=-23.0)
SUBTITULOS = False
ALIAS_QA = {   # lo que escribe Whisper -> grafía del guion (minúsculas, sin tildes); se completa tras `seleccionar`
    "lord dairon": "lordaeron", "lordairon": "lordaeron", "lordoran": "lordaeron",
    "mugrain": "mograine", "mowgrain": "mograine", "mograin": "mograine", "mogrein": "mograine",
    "kelthuzad": "kel thuzad", "keltuzad": "kel thuzad", "kel tuzad": "kel thuzad", "gelsusad": "kel thuzad",
    "naxramas": "naxxramas",
    # seleccionar del 29-oct (las claves van ya normalizadas: minúsculas, sin tildes ni apóstrofos)
    "tyrion": "tirion", "badin": "vadin", "vadim": "vadin", "bavin": "vadin",
    "eitrig": "eitrigg", "eitrich": "eitrigg", "eitrith": "eitrigg",
    "renaud": "renault", "reno": "renault", "reynold": "renault", "dayon": "darion",
    "balnazar": "balnazzar", "rivalimpia": "ribalimpia", "isilien": "isillien", "y silian": "isillien", "avendis": "abbendis",
    "alexandro": "alexandros", "thailand": "taelan", "caelan": "taelan", "carandra": "karandra",
    "sidon": "saidan", "saidanda throhan": "saidan dathrohan", "datrohan": "dathrohan", "arfas": "arthas",
    "costa sur": "costasur", "mardenhold": "mardenholde", "valle norte": "vallenorte", "renfrey": "renfray",
    "casteldarrow": "castel darrow", "miranda": "myranda", "terrayende": "terrallende", "terraliande": "terrallende",
    "sabra hex": "zabra hexx", "troll": "trol", "coltira": "koltira", "tasarian": "thassarian", "orbas": "orbaz",
    "nicolas verenhoff": "nicholas zverenhoff", "villarefugio": "villa refugio", "sejifrente": "cejifrente",
    "agonia descarcha": "agonia de escarcha", "albargenta": "alba argenta", "comico": "comic", "daria casa": "daria caza", "bartilas": "barthilas",
}
# nombres que Whisper destroza aunque la voz los dice bien (comprobado al leer la transcripción completa)
# costasur_8: Whisper se come el «El» inicial tras [sad]; plaga_6: «lo/los separó» (una letra)
CER_MAX_POR_FRASE = {"naxxramas_10": 0.20, "capilla_1_16": 0.03, "costasur_8": 0.04, "plaga_6": 0.02}
MUSICA = {}
# Estilo común de Flow (docs/estilo_pegatina_flow.md § 1): el de Darrowshire + la Luz heroica de esta historia.
FICHA = dict(
    estilo=("Hand-painted 2D cut-out animation art for a dark epic fairy-tale retelling of World of Warcraft lore: stylized Warcraft "
            "proportions (chunky silhouettes, big hands and shoulders, oversized armor), hand-painted textures with visible brush "
            "strokes and paper grain, clean dark ink outlines; gothic HORROR and HEROIC mood in Lordaeron: ashen greys, sickly plague "
            "green and cold moonlight blue palette, with warm holy golden Light as the heroic accent, long shadows, drifting fog, "
            "strong depth"),
    cierre=" No text, no letters, no numbers, no watermark, no logos.",
)
