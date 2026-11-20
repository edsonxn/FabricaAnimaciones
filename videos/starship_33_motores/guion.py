# -*- coding: utf-8 -*-
"""¿Por qué Starship tiene 33 motores? (~10 min, horizontal). 3.er video de T Menos Cero.
Kit LÍNEA 3D (`nucleo/linea3d.py` + `linea3d_starship.py` + `linea3d_cohetes.py`) + VIDEO REAL de cada suceso que nombra la voz
(yt-dlp, con crédito: `_clips.py`) + fotos reales en marcos de alambre. Voz ElevenLabs «Alberto Rodríguez». Sin subtítulos quemados.
Datos comprobados el 20-nov-2026: `datos.md` (fuentes y lista de lo DUDOSO que no se dice).
"""

TITULO = "¿Por qué Starship tiene 33 motores? La verdadera razón"
ARCHIVO = "starship_33_motores"
ESTILO_VISUAL = "documental"     # kit linea3d + video real con capas
DURACION = None
BPM = 240
GAP = 0.42
SUBTITULOS = False
MEZCLA = dict(musica=-24.0, sfx=-22.0, fx=-17.0)
CER_MAX_POR_FRASE = {"cierre_4": 0.12, "vuelos_5": 0.10}   # Whisper: «bueno 15», «Raptor III»
TAIL_MAX_POR_FRASE = {"vuelos_5": 0.45}   # Whisper: «T-Cero»
GAP_MAX_POR_FRASE = {}
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1,
           stability=0.5)

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[serious] Mira la base de este cohete.",
        "Treinta y tres motores, encendidos al mismo tiempo. Es el cohete más poderoso que se ha construido.",
        "El Saturno V, el que llevó a los astronautas a la Luna, tenía solo cinco.",
        "[short pause] Y la última vez que alguien intentó volar con tantos motores, en la Unión Soviética, el cohete explotó cuatro veces de cuatro.",
        "[curious] Entonces, ¿por qué SpaceX decidió poner treinta y tres?",
        "La respuesta no es solo la fuerza. Tiene que ver con fallar, con fabricar, y con volver a casa.",
        "Esta es la verdadera razón de los treinta y tres motores.",
    ]},
    {"id": "raptor", "frases": [
        "Empecemos por uno solo. Se llama Raptor.",
        "Quema metano y oxígeno líquidos, los dos a temperaturas bajísimas.",
        "Y usa un ciclo que casi nadie se había atrevido a construir: los dos propelentes pasan por sus propias turbinas antes de entrar a la cámara. Nada se desperdicia.",
        "La versión más nueva, el Raptor tres, empuja con unas doscientas cincuenta toneladas de fuerza.",
        "Y pesa poco más de mil quinientos kilos. Más o menos lo que un coche.",
        "[short pause] Ahora multiplica eso por treinta y tres.",
        "Juntos, empujan con más del doble de fuerza que el Saturno V.",
    ]},
    {"id": "anillos", "frases": [
        "Pero no están puestos al azar. Mira la base desde abajo.",
        "En el centro hay tres motores.",
        "Alrededor, un anillo de diez.",
        "Y en la orilla, otros veinte.",
        "Los trece de adentro pueden girar unos grados, como la mano de un piloto. Son los que dirigen el cohete.",
        "Los veinte de afuera van fijos. Su trabajo es uno solo: empujar con toda su fuerza durante el despegue.",
        "Fuerza bruta afuera, precisión en el centro. Y esa división, como vas a ver, es clave para el final del viaje.",
    ]},
    {"id": "saturno", "frases": [
        "Para entender por qué tantos, hay que volver al cohete de la Luna.",
        "El Saturno V tenía cinco motores F-1, los más grandes de una sola cámara que han volado.",
        "Cada uno empujaba casi tres veces más que un Raptor.",
        "[serious] Pero hacer un motor así de grande casi fracasa.",
        "En las pruebas, el fuego dentro de la cámara empezaba a vibrar, y en milésimas de segundo destruía el motor.",
        "Los ingenieros llegaron a detonar pequeñas bombas dentro de la cámara encendida, para ver si el motor se recuperaba solo.",
        "Tardaron más de tres años en resolverlo.",
        "Lo lograron, y ningún F-1 falló así en vuelo. Pero la lección quedó: un motor gigante es lentísimo y carísimo de perfeccionar.",
    ]},
    {"id": "n1", "frases": [
        "Al otro lado del mundo, los soviéticos tomaron el camino contrario.",
        "Su cohete lunar, el N1, tenía treinta motores en la primera etapa.",
        "Si uno fallaba, un sistema de control apagaba también el del lado opuesto, para que el cohete no se desviara.",
        "En teoría, podía perder varios y seguir volando.",
        "[sighs] En la práctica, voló cuatro veces. [short pause] Y falló las cuatro.",
        "El tres de julio de mil novecientos sesenta y nueve, la bomba de oxígeno de uno de los motores explotó justo al despegar.",
        "El cohete apenas se levantó, cayó sobre su plataforma, y la destruyó. Reconstruirla tomó un año y medio.",
        "[thoughtful] El problema no eran los treinta motores. Era que, cuando uno fallaba, se llevaba a sus vecinos con él.",
    ]},
    {"id": "falcon", "frases": [
        "SpaceX ya había apostado por muchos motores antes de Starship.",
        "Su Falcon 9 tiene nueve.",
        "En octubre de dos mil doce, en una misión hacia la Estación Espacial, uno de esos nueve motores se apagó a los setenta y nueve segundos de vuelo.",
        "Los otros ocho siguieron encendidos un poco más de tiempo, y la cápsula Dragon llegó a la Estación de todos modos.",
        "Un satélite que viajaba de pasajero sí se perdió. Pero la misión principal se salvó.",
        "Y en el Falcon Heavy, SpaceX juntó tres primeras etapas: veintisiete motores encendidos a la vez.",
    ]},
    {"id": "fallas", "frases": [
        "[short pause] Esa es la primera razón: con muchos motores, perder uno no es el fin.",
        "Elon Musk lo resumió así: si la falla de un motor queda aislada de los demás y del cuerpo del cohete, más motores hacen al cohete más confiable, no menos.",
        "Esa es justo la lección del N1.",
        "En febrero de dos mil veintitrés, SpaceX encendió por primera vez el Super Heavy completo, atado al suelo.",
        "De los treinta y tres, arrancaron treinta y uno. El equipo apagó uno antes de empezar, y otro se detuvo solo.",
        "[amused] Y aun así, según Musk, seguían siendo suficientes para llegar a órbita.",
    ]},
    {"id": "fabrica", "frases": [
        "La segunda razón está en la fábrica.",
        "Un motor gigante se construye casi a mano, uno por uno, y cada error cuesta años.",
        "Un motor más pequeño se puede fabricar en serie, como en una línea de autos.",
        "A finales de dos mil veintidós, SpaceX ya fabricaba más de un Raptor al día.",
        "Y se prueban encendidos en McGregor, Texas, antes de subir a un cohete.",
        "Y cuantos más fabricas, más aprendes y más barato sale cada uno. Un motor que falla en tierra es una lección. Uno que falla en el aire, una catástrofe.",
    ]},
    {"id": "aterrizaje", "frases": [
        "Y la tercera razón es la más importante para Starship: volver a casa.",
        "Al despegar, el cohete pesa miles de toneladas y necesita toda la fuerza.",
        "Pero al regresar, la etapa está casi vacía. Si encendiera los treinta y tres motores, saldría disparada hacia arriba.",
        "Con un solo motor gigante, no habría forma de frenar con suavidad.",
        "Con muchos motores pequeños, basta con encender unos cuantos.",
        "Para frenar, se encienden los trece de adentro.",
        "Y al final, solo los tres del centro, que giran para colocar el cohete justo entre los brazos de la torre.",
        "Los veinte de afuera ya hicieron su trabajo. Ahora es el turno de la precisión.",
    ]},
    {"id": "vuelos", "frases": [
        "[serious] Pero treinta y tres motores también son treinta y tres oportunidades de que algo salga mal.",
        "En el primer vuelo, en abril de dos mil veintitrés, varios motores se apagaron durante el ascenso. El cohete perdió el control, giró sin separarse, y terminó en una explosión.",
        "Siete meses después, en el segundo vuelo, los treinta y tres funcionaron hasta la separación por primera vez.",
        "En marzo de dos mil veinticinco, en el octavo vuelo, dos de los trece motores no volvieron a encender para el regreso.",
        "Y aun así, el propulsor llegó a la torre y lo atraparon.",
        "Y en el vuelo quince, el trece de noviembre, despegó con los treinta y tres Raptor tres.",
        "Su regreso se cortó por falta de combustible, y la captura se canceló. Pero la nave, arriba, sí fue atrapada.",
    ]},
    {"id": "nave", "frases": [
        "Y la nave tiene su propia cuenta.",
        "Arriba van otros seis Raptor. Con el propulsor, son treinta y nueve motores en un solo cohete.",
        "Cada uno se puede cambiar, revisar o reemplazar, como una pieza más.",
        "En lugar de un motor perfecto, Starship apuesta por muchos motores buenos, baratos y repetibles.",
    ]},
    {"id": "contras", "frases": [
        "[thoughtful] ¿Tiene desventajas? Claro.",
        "Más motores significan más tuberías, más válvulas, más cables, y más formas de fallar.",
        "Si un motor explota, puede dañar a los que tiene al lado. Por eso cada uno necesita su propia protección.",
        "Y encender treinta y tres motores al mismo tiempo, todos sincronizados, es un problema de control enorme.",
        "Parte de la respuesta de SpaceX es el Raptor tres: más simple y más ligero que el anterior.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "[short pause] Así que, ¿por qué treinta y tres?",
        "Porque así un motor que falla no detiene la misión. Porque se pueden fabricar en serie. Y porque solo con muchos motores pequeños se puede frenar con la precisión suficiente para volver a la torre.",
        "El N1 demostró que muchos motores pueden ser una trampa. Starship intenta demostrar que, bien hechos, son la salida.",
        "Si quieres ver cómo les va en el próximo vuelo, explicado en tres dimensiones,",
        "suscríbete a T Menos Cero. Nos vemos en el próximo despegue.",
    ]},
]

for _e in ESCENAS[1:-1]:
    _e.setdefault("pre", 0.5)
    _e.setdefault("post", 0.6)
for _id, _p in {"raptor": 1.0, "anillos": 1.2, "saturno": 1.5, "n1": 1.5, "falcon": 1.2, "fallas": 1.2, "fabrica": 1.2,
                "aterrizaje": 1.5, "vuelos": 1.5}.items():
    next(e for e in ESCENAS if e["id"] == _id)["post"] = _p
ESCENAS[0]["post"] = 0.3
ESCENAS[-1]["pre"] = 0.3
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo="Cinematic space-engineering explainer underscore: deep pulsing analog synth bass, precise ticking percussion, wide airy pads, "
           "curious and confident like a rocket launch webcast, instrumental only, no vocals.",
    escenas={e["id"]: ("", 0) for e in ESCENAS},
    tramos=[(["gancho", "raptor"], "biblioteca"), (["anillos", "saturno"], "biblioteca"), (["n1", "falcon"], "biblioteca"),
            (["fallas", "fabrica", "aterrizaje"], "biblioteca"), (["vuelos", "nave", "contras", "cierre"], "biblioteca")])

SFX_ELEVEN = {
    "hud": dict(prompt="Short soft digital interface beep, mission control telemetry readout, clean and quiet", seg=0.5, variantes=4),
    "tic": dict(prompt="Very short soft digital tick, a data row appearing on a screen", seg=0.3, variantes=3),
    "whoosh": dict(prompt="Deep smooth cinematic whoosh, camera moving fast through space", seg=1.3, variantes=3),
    "pulso": dict(prompt="Low cinematic sub bass hit with short reverb tail, dramatic title impact", seg=2.0, variantes=2),
    "ignicion": dict(prompt="Single rocket engine ignition: sharp pop then a steady powerful roar", seg=2.5, variantes=2),
    "rugido": dict(prompt="Massive rocket launch: dozens of engines roaring together, deep crackling thunder", seg=4.0),
    "apagado": dict(prompt="Rocket engine shutting down: roar cutting off into a hiss", seg=1.5),
    "explosion": dict(prompt="Distant massive explosion, deep boom rolling across flat land", seg=3.0),
    "vibra": dict(prompt="Violent resonant rumble growing into a metallic rattle, combustion instability", seg=2.0),
    "alarma": dict(prompt="Mission control abort alert: two low urgent electronic tones", seg=1.2),
    "fabrica": dict(prompt="Factory assembly line: pneumatic tools, metallic clanks and a conveyor hum", seg=3.0),
    "gira": dict(prompt="Hydraulic actuator moving a heavy rocket nozzle: short servo whine", seg=1.0, variantes=2),
    "brazos": dict(prompt="Giant mechanical steel arms closing on a launch tower: hydraulic whine and heavy metal clank", seg=2.5),
    "sello": dict(prompt="Rubber stamp slammed onto paper, firm thump", seg=0.6, variantes=2),
    "campana": dict(prompt="Bright clean notification chime, two rising bell notes", seg=1.0),
}
