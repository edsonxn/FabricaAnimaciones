# -*- coding: utf-8 -*-
"""Reel VERTICAL para Facebook (Juchipila): invitación tipo comercial a los bikers y al público de la CAIN Road Race México 2026
(13-15 nov, carrera dom 15) para que ENTREN a Juchipila a comer lo local: las gorditas fritas (imprescindibles, ahí sentados,
recién hechas; broma: «viniste por la carrera, vas a volver por las gorditas»), birria tatemada, antojos, guayaba, y a caminar
jardín, templo, callejones y mercado. Secuela del reel jch_carrera_moyahua (mismo narrador). Motor SECUENCIA YT en vertical:
clips reales por beat (yt-dlp, recorte 9:16) con crédito del canal + kit_jch (mapa, fichas, cifras).

FUENTES (consultadas el 12-nov-2026):
- Imagen Zacatecas (19-ago-2018) «Gorditas de Juchipila, una deliciosa opción»: en el Callejón de los Jambados están las gorditas
  estilo Juchipila, fritas en aceite, con lomo, rajas, queso o chorizo; una pareja las vende desde hace 40 años (en 2018);
  de 7:30 a 13:00; también tostadas, tacos dorados, horchata, café y chocolate; el municipio tiene birria tatemada de chivo y borrego.
- Cookpad, «Gorditas estilo Juchipila» (2016): masa de maíz aplanada y frita en aceite; encima salsa de tomate verde, queso fresco
  y cebolla; hay quien las prefiere de lomo de cerdo; versión de chorizo con frijoles, repollo y crema.
- Secturz / Gobierno de Zacatecas (23-oct-2026): evento 13-15 nov; tramo caseta de Jesús María (km 78) → Moyahua (km 105);
  hotel sede Paraíso Caxcán en Apozol. NTR Zacatecas (oct-2026): carrera el domingo desde el mediodía; entrada gratis; llegar
  antes de las 10; nueva edición en mayo de 2027. NTR (nov-2026): la federal 23 cerrada 3-4 h.
- Distancia Moyahua → Juchipila: OSRM sobre OpenStreetMap, 17.2 km, ~18 min (_ruta.json, 2.º tramo). Apozol queda al norte de
  Juchipila y la carrera al sur: desde el hotel sede se pasa por Juchipila.
- Tesis UNAM (ru.dgb.unam.mx) y Rev. Geográfica de América Central (2011): el Cañón de Juchipila, con Calvillo, es de las
  principales zonas productoras de guayaba del país.
- Wikipedia «Juchipila»: templo de San Francisco; Mercado 27 de Septiembre, con la estatua de Xochipilli enfrente.
"""

TITULO = "Viniste por la carrera… vas a volver por las gorditas"
ARCHIVO = "jch_gorditas"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
FORMATO = "vertical"
GAP = 0.16
DURACION = None
BPM = 104

NARRADOR = "gbTn1bmCvNgk0QEAVyfM"   # Enrique M. Nieto (el mismo del reel de la carrera, elegido por Edson el 10-nov-2026)
VOZ = dict(motor="elevenlabs", voice_id=NARRADOR, modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.45, style=0.4,
           sin_etiquetas=("whisper", "excit", "shout"))
FONETICA = {}
# Whisper escribe «Moyagua», «Aposol» y «Kine Road Race»: no es error de la voz
CER_MAX_POR_FRASE = {"gancho_1": .09, "donde_0": .03, "donde_2": .03, "broma_0": .05}

ESCENAS = [
    {"id": "gancho", "pre": 1.2, "frases": [
        "[warm] Este fin de semana, el cañón se llena de motos.",
        "Llega la Caín Road Race, y tú ya vienes en camino.",
        "Ya sea que traigas la moto o que vengas a ver la carrera, escucha bien: [short pause] antes de irte, entra a Juchipila.",
        "[amused] Y ven con mucha hambre.",
    ]},
    {"id": "donde", "frases": [
        "La carrera es el domingo quince, desde el mediodía, de Jesús María a Moyahua.",
        "La meta queda a diecisiete kilómetros de Juchipila. Unos veinte minutos.",
        "Y si te quedas en el hotel sede, en Apozol, Juchipila te queda de paso. Todos los días.",
        "Juchipila está en el corazón del cañón, entre cerros y palmas.",
    ]},
    {"id": "gorditas", "pre": 0.3, "frases": [
        "[serious] Ahora sí, lo importante.",
        "Aquí hay algo que no te puedes ir sin probar: las gorditas de Juchipila.",
        "Una gordita de maíz que se fríe en aceite hasta que queda dorada y crujiente.",
        "Y encima, lo que tú escojas: lomo, rajas, queso o chorizo.",
        "Luego, la salsa: picante, de jitomate, que no pica, o las dos juntas. Su queso, su cebolla, y su chile verde frito a un lado.",
        "¿No sabes cómo pedirla? Nomás di: [short pause] sírvamela como se acostumbra. Y en el puesto te la van a servir como debe ser.",
        "Y no te la lleves para el camino. Siéntate, pídela recién hecha y cómetela ahí, caliente, que truene.",
        "[amused] Una no alcanza. Nadie pide una.",
        "Búscalas en el Callejón de los Jambados, donde hay familias que llevan más de cuarenta años friéndolas.",
        "Y si el callejón está lleno, no te preocupes: hay gorditas en varios lugares. Búscalas en Google Maps, o date una vuelta alrededor del centro: hay varios puestos muy buenos.",
        "Son de almuerzo: salen desde temprano, y cuando se acaban, se acaban.",
        "Y si te gustan rellenas, también las hay: de las que se abren y se rellenan. Otra opción más.",
        "Y para acompañar: un agua de horchata, un cafecito… [short pause] o lo que no puede faltar: una coca de vidrio, bien fría.",
        "Gordita frita de lomo, con su queso, su cebolla y su chile, y la coca bien helada: [short pause] ese es el combo perfecto.",
    ]},
    {"id": "broma", "pre": 0.3, "frases": [
        "[amused] Y te lo advertimos de una vez:",
        "tú vienes por la carrera, [short pause] pero vas a volver por las gorditas.",
        "[laughs softly] Las motos que nos perdonen.",
        "El próximo año ya no vas a preguntar a qué hora sale la carrera. Vas a preguntar a qué hora abren las gorditas.",
    ]},
    {"id": "mas", "frases": [
        "Si te quedas con hambre, en el mismo callejón está la birria tatemada, de chivo y de borrego.",
        "Para el antojo: chicharrones, churros y pan del pueblo.",
        "Y llévate fruta. El cañón de Juchipila es de las principales zonas de guayaba de todo el país.",
        "Pregúntale a la gente de los puestos: aquí todos tienen su lugar favorito, y te lo van a recomendar.",
    ]},
    {"id": "caminar", "pre": 0.3, "frases": [
        "Ya comiste. Ahora camina.",
        "Siéntate un rato en el jardín, entra al templo de San Francisco y piérdete en sus callejones.",
        "Date una vuelta por el mercado y por sus puestos.",
        "Y tómate la foto con las letras de Juchipila, para que se vea dónde estuviste.",
    ]},
    {"id": "consejos", "frases": [
        "A los bikers: deja la moto, quítate el casco y date la vuelta a pie. [short pause] Aquí no hay curvas, pero hay sabor.",
        "Y si vas a ver la carrera, recuerda llegar antes de las diez. Así que almuerza temprano, en Juchipila.",
        "[amused] Y si la carretera se cierra unas horas, mejor que te encuentre aquí, comiendo.",
        "Y trae efectivo, que en muchos puestos se paga así.",
    ]},
    {"id": "local", "frases": [
        "Cada gordita, cada plato de birria, cada bolsa de guayaba que compras aquí se queda en una familia de Juchipila.",
        "Los organizadores quieren volver en mayo del dos mil veintisiete.",
        "[warm] Nosotros también queremos que vuelvas. Aunque ya sabemos que vas a volver por las gorditas.",
    ]},
    {"id": "cierre", "post": 2.0, "frases": [
        "[warm] Juchipila, Zacatecas. Aquí te esperamos.",
        "Y si eres de Juchipila y tienes un puesto de comida o un negocio, déjalo en los comentarios, para que todos sepan a dónde ir.",
    ]},
]

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=4.4,              # reel: ritmo rápido
    transicion="slideleft",
    fundido=0.25,
    ambiente=0.0,
    ambiente_por={},         # se decide al ver los clips (rugido de motos en el gancho, chisporroteo del aceite)
    yt=dict(sufijo="", min_s=20, max_min=240, alto=1080, evitar_canales=[]),
)
TRANSICIONES = [("continua", 0.1)] * 50
MEZCLA = dict(fx=-6.0)

LYRIA = dict(
    estilo="Warm festive Mexican small-town underscore for a food and travel commercial: bright nylon guitars, light "
           "percussion, a touch of brass, inviting and joyful, instrumental only, no vocals, steady under narration.",
    escenas={
        "gancho": ("building energy, motorcycle-rally drive", 4), "donde": ("driving, road trip", 4),
        "gorditas": ("warm, appetizing, sizzling groove", 6), "broma": ("playful, a cheeky stop", 3),
        "mas": ("festive market bustle", 5), "caminar": ("relaxed stroll in a sunny plaza", 4),
        "consejos": ("friendly practical pulse", 4), "local": ("heartfelt, proud", 4), "cierre": ("warm resolution", 3),
    },
    tramos=[(["gancho", "donde", "gorditas", "broma"], "Begin with road energy, settle into a warm appetizing groove."),
            (["mas", "caminar", "consejos", "local", "cierre"], "Festive and relaxed, end warm and resolved.")])
