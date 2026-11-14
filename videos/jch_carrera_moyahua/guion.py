# -*- coding: utf-8 -*-
"""Reel VERTICAL para Facebook (perfil de Juchipila de Edson): la CAIN Road Race México 2026 y el cierre de la carretera 23.
Sin canal de YouTube. Formato debate: narrador con los datos + dos voces que representan cada postura (EN CONTRA / A FAVOR;
no son vecinos reales, en pantalla dicen «postura»). Motor SECUENCIA YT en vertical: clips reales por beat (yt-dlp, recorte 9:16),
pegatinas y mapa con la ruta.

FUENTES (consultadas el 10-nov-2026):
- Secturz / Gobierno de Zacatecas, boletín 23-oct-2026 «Zacatecas recibirá por primera vez CAIN Road Race México 2026, en Moyahua»
  (turismo.zacatecas.gob.mx): 13-15 nov; actividades principalmente 14 y 15; tramo caseta fitozoosanitaria de Jesús María (km 78)
  → Moyahua de Estrada (km 105); 100 pilotos de 16 entidades; categorías Profesional, Amateur, Novatos, Doble Propósito; hotel sede
  Paraíso Caxcán; Le Roy Barragán Ocampo (secretario de Turismo) y Jorge Quiñones Soto (presidente de CAIN Road Race México).
- NTR Zacatecas (oct-2026) «Llegará CAIN Road Race a Zacatecas con más de 100 pilotos»: 27.5 km, 97 curvas; cañón de Juchipila;
  nueva edición en mayo de 2027; carrera el domingo, salida individual cada 30 s a partir del mediodía; ~50 marshals (15 itinerantes),
  ambulancias, PC, Guardia Nacional; revisión de motos y equipo; acceso gratuito; no colocarse en salidas de curva ni cruzar;
  llegar antes de las 10. Desde 2016.
- NTR Zacatecas (nov-2026) «Sin coordinación corporaciones en Cain Road Race» (PC de Moyahua, Juchipila y Apozol): ~10 accidentes en
  promedio durante la carrera; el Estado sin coordinación con los municipios; entre los tres solo cuatro ambulancias; Hospital
  Comunitario de Juchipila solo atención primaria, «no tienen cirujano, equipo de trauma, anestesiólogo»; carretera federal 23 a
  Guadalajara bloqueada tres o cuatro horas; la ciudadanía reclama que se detendrán servicios como los taxis a Zacatecas y
  Guadalajara; mínimo 10 ambulancias, grúas, ~40 voluntarios, drones; en Moyahua mínimo tres accidentes viales por semana; tramos
  más peligrosos km 80 (Jesús María) y 105; un participante que ya llegaba se accidentó (ambas piernas).
- Imagen Zacatecas (23-oct-2026): beneficiaría a Moyahua, Juchipila, Apozol y Jalpa; alianza con la carrera de la Isla de Man.
- Mazatlán Interactivo (nov-2021), sexta edición en Concordia, Sinaloa: unos 15 000 espectadores, 150 competidores, sin percances.
- Luz Noticias (16-nov-2023): Jorge Quiñónez Soto «se espera una derrama económica de más de 10 millones de pesos» (Concordia).
Ojo: el usuario recordaba «viernes 13 o 14»: el evento es del 13 al 15 y la CARRERA el domingo 15.
"""

TITULO = "¿Cerrar la carretera por una carrera de motos?"
ARCHIVO = "jch_carrera_moyahua"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
FORMATO = "vertical"
GAP = 0.16
DURACION = None
BPM = 100

NARRADOR = "gbTn1bmCvNgk0QEAVyfM"   # Enrique M. Nieto (mexicano, «Credible and Rich»; elegido por Edson el 10-nov-2026)
CONTRA = "iBGVhgcEZS6A5gTOjqSJ"     # Gabiyoya (mexicana, mediana edad): la postura EN CONTRA
FAVOR = "ojGau167OE7nUATM1xDa"      # Marto (mexicano, conversacional): la postura A FAVOR
VOZ = dict(motor="elevenlabs", voice_id=NARRADOR, modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.45, style=0.35,
           sin_etiquetas=("whisper", "excit", "shout"))
FONETICA = {}
# Whisper escribe «Moyagua» y «Aposol» (así se pronuncian): no es error de la voz
CER_MAX_POR_FRASE = {"contra_1": .03, "contra_5": .03, "favor_4": .03, "favor_5": .03}
TAIL_MAX_POR_FRASE = {"contra_1": .5, "favor_4": .5}

ESCENAS = [
    {"id": "gancho", "pre": 1.6, "frases": [
        "[serious] Este domingo, la carretera que nos saca a Guadalajara va a estar cerrada. [short pause] Tres o cuatro horas.",
        "¿Para qué? [short pause] Para una carrera de motos.",
        "Y en el cañón ya hay pleito.",
    ]},
    {"id": "que", "frases": [
        "Se llama Caín Road Race. Es la primera vez que llega a Zacatecas.",
        "El evento va del trece al quince de noviembre, y la carrera es el domingo quince, a partir del mediodía.",
        "Veintisiete kilómetros y medio, desde la caseta de Jesús María, en el kilómetro setenta y ocho, hasta Moyahua, en el ciento cinco.",
        "[short pause] Noventa y siete curvas.",
        "Esperan a cien pilotos de dieciséis estados. Salen uno por uno, cada treinta segundos, contra el reloj.",
    ]},
    {"id": "pleito", "pre": 0.4, "frases": [
        "[short pause] Y aquí es donde el pueblo se divide.",
    ]},
    {"id": "contra", "frases": [
        "[worried] ¿Y si alguien se pone grave ese domingo? ¿Por dónde lo sacamos?",
        "Protección Civil de Moyahua, Juchipila y Apozol dice que el Estado no los había incluido en la planeación.",
        "Que entre los tres municipios tienen cuatro ambulancias.",
        "Y que el hospital comunitario de Juchipila no tiene cirujano, ni anestesiólogo, ni equipo de trauma.",
        "Calculan unos diez accidentes durante la carrera.",
        "[serious] Y en Moyahua, sin carrera, ya atienden por lo menos tres accidentes de moto a la semana.",
        "De hecho, uno de los pilotos que ya venía llegando, ya se cayó. Se lastimó las dos piernas.",
        "[annoyed] ¿Y los taxis a Guadalajara y a Zacatecas? ¿Que se esperen?",
    ]},
    {"id": "favor", "pre": 0.3, "frases": [
        "[calm] A ver, a ver. Esas motos ya vienen cada fin de semana. Sin reglas y sin ambulancias.",
        "Lo que dicen los organizadores: la carrera trae cincuenta marshals, ambulancias, Protección Civil y Guardia Nacional.",
        "Revisan cada moto y cada piloto: traje de cuero completo, casco certificado y seguro.",
        "Y trae gente. En Concordia, Sinaloa, donde se corre desde dos mil dieciséis, una sola edición juntó a unos quince mil espectadores.",
        "Gente que come, que duerme, que carga gasolina. El hotel sede está en Apozol.",
        "[amused] Y los burritos de Moyahua no se van a vender solos.",
        "¿Cuándo fue la última vez que alguien de Nuevo León o de Yucatán vino a gastar al cañón a propósito?",
        "Los organizadores quieren repetir en mayo de dos mil veintisiete.",
        "Si sale bien, el cañón de Juchipila queda en el mapa de las carreras.",
    ]},
    {"id": "balanza", "pre": 0.4, "frases": [
        "Las dos cosas son ciertas.",
        "Unas horas de carretera cerrada y un cañón que puede salir en el mapa.",
        "Un riesgo real y cuatro ambulancias para tres municipios.",
    ]},
    {"id": "consejos", "frases": [
        "Si vas a viajar el domingo, sal temprano.",
        "Y si vas a ir a verla, la entrada es gratis: llega antes de las diez, no te pares en la salida de las curvas y no cruces la carretera.",
    ]},
    {"id": "cierre", "post": 3.0, "frases": [
        "[warm] Y tú, ¿de qué lado estás? Te leo en los comentarios.",
        "Con respeto, que aquí todos somos vecinos.",
    ]},
]

# Quién dice cada frase (clave escena_índice). Las dos posturas abren su bloque y lo cierran; el narrador da los datos.
VOZ_POR_FRASE = {
    "contra_0": CONTRA, "contra_7": CONTRA,
    "favor_0": FAVOR, "favor_5": FAVOR, "favor_6": FAVOR, "favor_8": FAVOR,
}
# NEUTRALIDAD (Edson, 10-nov-2026): el narrador NO toma postura; solo da los datos de cada lado. Toda opinión va en boca de
# las voces EN CONTRA / A FAVOR (rótulo «POSTURA» en pantalla) y el cierre pregunta, no concluye.

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=4.6,              # reel: ritmo rápido
    transicion="slideleft",
    fundido=0.25,
    ambiente=0.0,
    ambiente_por={"scene-001": 0.8, "scene-002": 0.8},   # rugido real de las motos en el gancho (onboard)
    yt=dict(sufijo="", min_s=20, max_min=240, alto=1080, evitar_canales=[]),
)
TRANSICIONES = [("continua", 0.1)] * 40
MEZCLA = dict(fx=-6.0)

LYRIA = dict(
    estilo="Tense modern documentary underscore for a vertical news reel: pulsing low synth bass, tight electronic percussion, "
           "subtle distorted guitar textures that evoke motorcycles, instrumental only, no vocals, steady under narration.",
    escenas={
        "gancho": ("tense, building, a heartbeat-like pulse", 4),
        "que": ("driving and energetic, racing momentum", 6),
        "contra": ("dark and worried, low strings and sparse pulses", 4),
        "favor": ("warm, optimistic, light acoustic guitar over the beat", 6),
        "pleito": ("sudden drop to a low held tone, a single deep hit", 4),
        "balanza": ("suspended, unresolved, sparse", 3),
        "consejos": ("light steady pulse, practical and friendly", 4),
        "cierre": ("calm resolution, soft and open", 3),
    },
    tramos=[(["gancho", "que", "pleito", "contra"], "Begin with a tense pulse right away. End on a dark low held tone."),
            (["favor", "balanza", "consejos", "cierre"], "Begin warmer and optimistic. End softly, resolved and open.")])
