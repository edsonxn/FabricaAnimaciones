# -*- coding: utf-8 -*-
"""La historia de Tequisquiapan (Short VERTICAL 1080x1920, ≤ 3 min; estilo BOCETO + GUACHE sobre mapa con RELIEVE REAL).

Canal Cronopapel. Pedido del usuario (22-oct-2026): «video similar [a Aguascalientes] pero vertical de 3 minutos de algún pueblo
aleatorio del Bajío» → sorteo: Tequisquiapan (Querétaro). Kit de `videos/historia_aguascalientes/` adaptado a vertical (mapa de
Querétaro a 700 px/°, `_mapa_notas.md`). Reglas nuevas del 22-oct: links de Google Maps de cada lugar en la descripción, DECIRLO en
el video (frase «ruta_1») y muchas fotos reales (~1 cada 8 s; `fotos/creditos.json`). Voz ElevenLabs «Alberto Rodríguez».
Datos: `_hechos.md` ([HECHO]/[CRONISTA]/[LEYENDA]). NO afirmar: el decreto de Carranza (solo la placa de 1978), la leyenda de
Montañez como hecho, «tercer monolito del mundo», tequesquite = nitrato.
"""

TITULO = "La historia de Tequisquiapan"
ARCHIVO = "tequisquiapan"
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = 178.5               # Short: YouTube corta a 3:00
BPM = 112
GAP = 0.16
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4", idioma="es",
           tomas=1, stability=0.5)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

ALIAS_QA = {
    "tequisquiapan": "tequisquiapan", "tequesquite": "tequesquite", "otomies": "otomies", "otomíes": "otomies",
    "montanez": "montanez", "montañez": "montanez", "bernal": "bernal", "carranza": "carranza", "esquites": "esquites",
    "chichimecas": "chichimecas", "opalo": "opalo", "ópalo": "opalo",
}

SUBTITULOS = False
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.3, "post": 0.12, "frases": [
        "[curious] Este pueblo tiene un monumento que dice: «aquí está el centro de México»… [short pause] y no es cierto.",
        "Se llama como una sal, fue capital de Querétaro por unos días, y su estación de tren lleva el nombre de otro pueblo.",
        "Esta es la historia de Tequisquiapan, en el corazón del Bajío… y cómo llegar a cada lugar.",
    ]},
    {"id": "origenes", "pre": 0.15, "post": 0.12, "frases": [
        "Mucho antes de los españoles, aquí ya brotaba agua caliente.",
        "Otomíes y chichimecas venían a sus manantiales a hacer tratos… y a bañarse.",
        "Del náhuatl viene el nombre: Tequisquiapan, «lugar sobre el agua de tequesquite».",
        "El tequesquite es una sal blanca que todavía se le echa a los esquites.",
    ]},
    {"id": "fundacion", "pre": 0.15, "post": 0.12, "frases": [
        "La fundación oficial es del 24 de julio de 1551, con un nombre larguísimo: Santa María de la Asunción y de las Aguas Calientes.",
        "[whispers] La tradición dice que un cacique otomí plantó una cruz bajo un mezquite… pero eso es más leyenda que historia.",
        "En 1567 La Pila Grande ya regaba las huertas de una hacienda: hoy es el Parque La Pila.",
        "El nombre definitivo llegó en 1656.",
    ]},
    {"id": "siglos", "pre": 0.15, "post": 0.12, "frases": [
        "En 1897 la parroquia estrenó un reloj que funciona con pesas de hasta 150 kilos.",
        "En 1902 llegó el tren… pero su estación se llamó «Bernal», como el pueblo de la peña.",
        "En 1910 la Presa Centenario le dio a la región su primera luz eléctrica.",
        "Y en mayo de 1920, en plena rebelión contra Carranza, el gobernador declaró a Tequisquiapan capital de Querétaro… por unos días.",
    ]},
    {"id": "centro", "pre": 0.15, "post": 0.12, "frases": [
        "¿Y el centro de México? Este monumento es de 1978, y su placa le atribuye la idea a Venustiano Carranza.",
        "Pero nadie ha encontrado ese decreto, y el centro calculado del país está en Zacatecas, a unos 450 kilómetros.",
    ]},
    {"id": "turismo", "pre": 0.15, "post": 0.12, "frases": [
        "En los años cincuenta llegó la fama: cada fin de semana, familias de la capital venían a sus aguas termales.",
        "En 1976 nació la Feria Nacional del Queso y el Vino, y en 2012 Tequisquiapan se volvió Pueblo Mágico.",
        "Sus artesanos tejen cestos de vara, en sus cerros hay ópalos, y muy cerca está la Peña de Bernal: un volcán que nunca salió, de 433 metros.",
    ]},
    {"id": "ruta", "pre": 0.15, "post": 1.2, "frases": [
        "Para comprobarlo: la parroquia y su reloj, la plaza, el monumento, el Parque La Pila, el mercado de artesanías, la Presa Centenario y la Peña de Bernal.",
        "Te dejo en la descripción cómo llegar a cada lugar.",
        "[serious] Eso sí: el pueblo de las aguas termales se queda sin agua; su acuífero pierde 5 millones de metros cúbicos al año.",
        "Si vas, cuídala. [short pause] Y dime: ¿qué pueblo del Bajío contamos después?",
    ]},
]

TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)

# Fotos reales: clave corta → fotos/<clave>.jpg (copias ASCII de los archivos de Commons; créditos en fotos/creditos.json)
FOTOS = {}

SFX_ELEVEN = {
    "pop": dict(prompt="Soft paper cut-out sticker popping onto a wooden desk, light cardboard tap, dry, close", seg=0.6, variantes=4),
    "whoosh": dict(prompt="Quick soft paper whoosh, a sheet of drawing paper swept through the air, short", seg=0.8, variantes=3),
    "escribir": dict(prompt="Pencil scribbling fast on rough drawing paper, short burst", seg=1.2, variantes=3),
    "foto": dict(prompt="Old printed photograph slapped onto a notebook page, paper flap and a strip of tape pressed down", seg=0.8, variantes=4),
    "agua_termal": ("Warm thermal spring water bubbling gently in a stone pool, soft", 4),
    "chapuzon": ("Person stepping into a warm pool, gentle splash and relaxed sigh", 1.5),
    "campana": dict(prompt="Single bronze church bell toll in a small colonial Mexican town plaza, light reverb", seg=3, bib=False),
    "reloj": ("Old church tower clock mechanism ticking, heavy gears and a weight chain", 3),
    "tren": ("Steam locomotive whistle and chugging arrival at a small rural station, early 1900s", 5),
    "luz": ("Old electric switch clunk and a hum of light bulbs turning on", 1.5),
    "presa": ("Water rushing over a small dam spillway, steady", 3),
    "galope": dict(prompt="A few horses galloping on a dry dirt road, passing by", seg=3, variantes=2),
    "sello": dict(prompt="Heavy rubber stamp pressed on a paper document, firm thump", seg=0.7, variantes=2),
    "feria": ("Small Mexican town fair with a festive crowd, clinking wine glasses and a distant band", 5),
    "copas": ("Two wine glasses clinking in a toast, close", 0.8),
    "cesteria": ("Dry wooden reeds being woven into a basket by hand, creaking twigs", 2),
    "camara": ("Vintage film camera shutter click and wind", 0.8),
    "multitud": ("Relaxed weekend crowd chatter in a small plaza, families and children", 4),
    "golpe_suave": dict(prompt="Soft muffled thud of a small cardboard cut-out landing on a table", seg=0.6, variantes=3),
    "crece": dict(prompt="Short magical rising shimmer, something growing quickly, soft paper rustle", seg=1.0, variantes=3),
    "pasos": dict(prompt="Footsteps walking on cobblestones, several people, short", seg=1.5, variantes=2),
    "papel": dict(prompt="Sheet of old paper being unrolled and handled, crisp rustle", seg=1.0, variantes=2),
    "brillo": dict(prompt="Short sparkling chime twinkle, magical glint", seg=0.8, variantes=2),
    "volcan": ("Deep slow rumble of rock rising underground, cinematic, no explosion", 2.5),
    "gotas": ("Water drops falling slowly into an almost empty stone basin, echo", 2.5),
    "pluck": dict(prompt="Single soft plucked guitar string note, warm, short", seg=0.7, variantes=3),
}

LYRIA = dict(
    estilo=("Warm, lively animated-history score for a small town in the Bajío of central Mexico: jarana and vihuela strumming, "
            "violins, a light trumpet and soft hand percussion, with a modern documentary pulse. Instrumental only, no singing. "
            "Middle frequencies kept clear so a Spanish narrator can speak distinctly over it."),
    escenas={},
    tramos=[
        (["gancho", "origenes", "fundacion"],
         "Begin with a curious plucked hook, turn ancient and warm (hot springs, clay flute), then humble colonial guitar and strings."),
        (["siglos", "centro", "turismo", "ruta"],
         "A chugging railway rhythm and growing pride, a playful wink, a festive fair waltz, then a reflective ending that fades out."),
    ],
)
