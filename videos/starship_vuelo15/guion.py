# -*- coding: utf-8 -*-
"""El vuelo 15 de Starship, minuto a minuto, en 3D (~12 min, horizontal). 1.er video del canal T Menos Cero (`t_menos_cero`).
Kit LÍNEA 3D (`nucleo/linea3d.py` + `linea3d_starship.py`): 3D de líneas blancas sobre negro, HUD de misión con reloj T+ anclado
a la voz, alternado con video REAL de la retransmisión de SpaceX (yt-dlp, crédito SpaceX) con capas encima, y diagramas.
Voz ElevenLabs «Alberto Rodríguez». Sin subtítulos quemados.

Datos comprobados el 14-nov-2026 (Wikipedia «Starship flight 15», tabla de eventos de SpaceX; CNBC 14-nov «SpaceX, in a historic
first, catches upper stage of its Starship rocket»; space.com 14-nov «SpaceX still investigating why Starship Flight 15 booster
aborted 'chopsticks' landing catch»; Hot Air 13-nov):
  - Despegue 13-nov-2026 22:47:36 UTC (16:47:36 hora del centro, viernes 13) desde la plataforma orbital 2 (OLP-2) de Starbase.
  - Super Heavy B22 + Ship 42 (pintada «Don't Panic»), Block 3; 26 Starlink V3 (3 con cámaras para ver el escudo térmico).
  - T-3 s ignición del Super Heavy · T+58 s reducción de empuje para Max Q · T+2:19 MECO · T+2:21 separación en caliente ·
    T+2:26-3:02 quema de regreso (un motor no reencendió: 32 de 33 según la tabla) · T+6:10-6:35 quema de aterrizaje ·
    captura del propulsor ABORTADA: aborto automático (space.com: «no estaba donde debía estar»), desvío al golfo de México;
    Musk: «bajo rendimiento», poco combustible; se desintegró antes de tocar el agua (CNBC: explotó; FTS activado).
  - T+8:09 SECO · T+26:10-26:30 quema de inserción orbital con un motor · órbita 276 × 278 km, 30,5° · ~14 vueltas.
  - Despliegue T+35:01 → T+1:17:40 (~42 min). Puntos de control de regreso: Hawái T+1:27:46, Chile T+7:15:35, Hawái T+20:41:55.
  - Quema de salida de órbita T+21:35:57-21:36:07 · entrada T+22:10:46 · transónico T+22:29:34 · subsónico T+22:30:13 ·
    quema de aterrizaje T+22:32:16 · giro T+22:32:18 · 3→2 motores T+22:32:21 · 2→1 T+22:32:27 ·
    CAPTURA T+22:32:28 (≈ 21:20:03 UTC del 14-nov) en la torre de la plataforma 2.
  - Primera etapa superior que vuelve de órbita y aterriza de pie (Wikipedia); primer intento de atrapar las dos etapas (CNBC);
    misión más larga de Starship (récord del vuelo 14). Velocidad orbital en la retransmisión: ~26 400-26 500 km/h.
  - NASA cuenta con Starship (HLS) para llevar astronautas a la superficie de la Luna (CNBC).
Video real: retransmisión oficial de SpaceX vía VideoFromSpace (space.com): F0ltKM5qc7A (despegue; T+0 = seg 675 del video) y
KqGPHd7XAbs (reentrada y captura).
"""

TITULO = "Starship atrapó su nave al volver del ESPACIO: el vuelo 15 explicado en 3D"
ARCHIVO = "starship_vuelo15"
ESTILO_VISUAL = "documental"     # kit linea3d (3D de líneas blancas sobre negro) + video real de SpaceX con capas
DURACION = None
BPM = 240
GAP = 0.42
SUBTITULOS = False
MEZCLA = dict(musica=-24.0, sfx=-22.0, fx=-17.0)
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1,
           stability=0.5)
CER_MAX_POR_FRASE = {"cierre_1": 0.1, "cierre_2": 0.12, "cifras_1": 0.05, "vueltas_3": 0.05}     # Whisper: «bueno 15», «T-0»

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Esta nave acaba de dar catorce vueltas a la Tierra.",
        "Viajaba a más de veintiséis mil kilómetros por hora.",
        "Atravesó la atmósfera envuelta en plasma, y terminó así:",
        "atrapada en el aire por los brazos de la misma torre desde la que despegó.",
        "Nunca, en la historia de los cohetes, una etapa que llegó a órbita había vuelto a casa de pie.",
        "Pero su compañero, el propulsor, no tuvo la misma suerte.",
        "Este es el vuelo quince de Starship, minuto a minuto, en tres dimensiones.",
    ]},
    {"id": "presenta", "frases": [
        "Viernes trece de noviembre, cuatro y cuarenta y siete de la tarde, en Starbase, Texas, junto a la frontera con México.",
        "En la plataforma dos espera el cohete más grande que se ha construido.",
        "Abajo, el propulsor Super Heavy número veintidós, con treinta y tres motores Raptor.",
        "Arriba, la nave número cuarenta y dos, que lleva pintada una frase de la Guía del autoestopista galáctico: no entres en pánico.",
        "Es la tercera versión de Starship: más alta, con más combustible y con motores Raptor de tercera generación.",
        "Juntos miden unos ciento veinticuatro metros, más que un edificio de cuarenta pisos.",
        "A su lado, la torre de lanzamiento, con dos brazos gigantes que en SpaceX llaman palillos.",
        "Dentro de la nave viajan veintiséis satélites Starlink de nueva generación.",
        "Y la misión trae una meta que nadie había intentado: atrapar las dos partes del cohete con la torre.",
    ]},
    {"id": "plan", "frases": [
        "El plan, en tres partes.",
        "Primero, el propulsor empuja unos dos minutos y medio, se separa, y vuelve a Starbase para que la torre lo atrape.",
        "Segundo, la nave sigue hasta la órbita, suelta los satélites, y da catorce vueltas a la Tierra.",
        "Y tercero, casi un día después, la nave regresa al mismo lugar, para que la torre la atrape también.",
        "Si todo sale bien, ninguna de las dos partes toca el suelo, ni el mar.",
    ]},
    {"id": "despegue", "frases": [
        "Tres segundos antes de cero, se encienden los treinta y tres motores.",
        "Y a las cuatro, cuarenta y siete con treinta y seis segundos, Starship despega.",
        "Juntos, esos motores empujan con más fuerza que los de cualquier otro cohete de la historia.",
        "Visto desde abajo, así se ven los motores.",
        "Los trece del centro pueden girar para dirigir el cohete. Los veinte de fuera están fijos, y solo empujan.",
    ]},
    {"id": "maxq", "frases": [
        "A los cincuenta y ocho segundos, los motores bajan su potencia.",
        "Es Max Q: el momento en que el aire empuja con más fuerza contra el cohete.",
        "Si no aflojara, la estructura sufriría de más. Pasado ese punto, vuelve a acelerar.",
    ]},
    {"id": "separa", "frases": [
        "Dos minutos y diecinueve segundos: el propulsor apaga casi todos sus motores.",
        "Y dos segundos después pasa algo que parece un error: la nave enciende sus motores, todavía pegada al propulsor.",
        "Es la separación en caliente.",
        "El fuego de la nave sale por este anillo de rejillas que une las dos etapas.",
        "Así la nave nunca deja de empujar, y no pierde velocidad mientras se separa.",
        "Desde aquí, cada etapa sigue su propio camino.",
    ]},
    {"id": "propulsor", "frases": [
        "Ahora sigamos al propulsor.",
        "Da media vuelta en el vacío, y a los dos minutos y veintiséis segundos enciende sus motores para regresar a Starbase.",
        "Aquí aparece el primer problema: uno de sus motores no vuelve a encender.",
        "Aun así termina la quema, y cae de cola durante más de tres minutos, guiado por sus tres aletas de rejilla.",
        "A los seis minutos y diez segundos enciende otra vez, ya rumbo a los brazos de la torre.",
        "SpaceX ya había atrapado propulsores así en vuelos anteriores. Esta vez no pudo.",
        "Pero la computadora del propulsor decide sola: no está donde debería estar para intentar la captura.",
        "Así que aborta, y en lugar de la torre, se desvía al golfo de México.",
        "Elon Musk habló de bajo rendimiento y de poco combustible. SpaceX todavía investiga la causa.",
        "Poco antes de tocar el agua, el propulsor se desintegra.",
        "La primera captura doble tendrá que esperar.",
    ]},
    {"id": "orbita", "frases": [
        "Mientras tanto, la nave sigue subiendo con sus seis motores: tres para el aire y tres para el vacío.",
        "A los ocho minutos y nueve segundos los apaga.",
        "Ya viaja a más de veintiséis mil kilómetros por hora, casi en órbita.",
        "A los veintiséis minutos enciende un solo motor durante veinte segundos.",
        "Con ese empujón queda en órbita, a unos doscientos setenta y cinco kilómetros de altura, inclinada treinta grados y medio sobre el ecuador.",
    ]},
    {"id": "starlink", "frases": [
        "A los treinta y cinco minutos se abre una compuerta en el costado de la nave.",
        "Por ahí salen los satélites, uno por uno, como dulces de un dispensador.",
        "Son veintiséis Starlink de tercera generación, y tardan unos cuarenta y dos minutos en salir todos.",
        "Una nave como esta puede llevar hasta sesenta. En este vuelo fueron veintiséis.",
        "Tres de ellos llevan cámaras. Se quedan cerca para fotografiar el escudo térmico de la nave antes de que regrese.",
        "Y las imágenes en directo de la nave, como esta, llegan a la Tierra a través de la misma red Starlink.",
    ]},
    {"id": "vueltas", "frases": [
        "Luego viene la parte más larga del vuelo: casi veintidós horas en órbita.",
        "Cada vuelta dura una hora y media: cuarenta y cinco minutos de día, y cuarenta y cinco de noche.",
        "Y como la Tierra gira debajo, cada vuelta pasa por encima de lugares distintos.",
        "Hay tres puntos de control, llamados Hawái, Chile y Hawái otra vez, en los que los controladores revisan la nave.",
        "Deciden si está bien para intentar el regreso a la torre, o si debe caer en el océano.",
        "Las tres veces, la respuesta fue sí.",
    ]},
    {"id": "reentrada", "frases": [
        "A las veintiún horas y treinta y cinco minutos de vuelo, la nave enciende sus motores durante diez segundos, para frenar.",
        "Basta con eso para que empiece a caer.",
        "Unos treinta y cinco minutos después toca la atmósfera.",
        "Entra de panza, con el escudo térmico por delante: miles de losetas negras con forma de hexágono.",
        "El aire, aplastado delante de la nave, se calienta tanto que se vuelve plasma, y la envuelve en un brillo naranja.",
        "Sus cuatro alerones, dos delante y dos detrás, la mantienen estable, como un paracaidista en caída libre.",
        "Es la parte más peligrosa del viaje: en vuelos anteriores, ese calor llegó a derretir parte de un alerón.",
    ]},
    {"id": "llegada", "post": 3.5, "frases": [
        "Diecinueve minutos después de entrar, ya cerca de Starbase, baja de la velocidad del sonido.",
        "Sigue cayendo de panza hacia Starbase, frenada solo por el aire.",
        "A las veintidós horas, treinta y dos minutos y dieciséis segundos, enciende tres motores.",
        "En dos segundos gira de horizontal a vertical.",
        "Baja con tres motores, luego con dos, y al final con uno solo.",
        "Y se detiene justo entre los brazos de la torre.",
        "Veintidós horas, treinta y dos minutos y veintiocho segundos después del despegue, los brazos la atrapan.",
    ]},
    {"id": "lenta", "frases": [
        "Veámoslo otra vez, en cámara lenta.",
        "La nave baja con un motor, apenas a la altura de los brazos.",
        "Los brazos se cierran, y la nave se apoya en ellos por dos soportes que tiene bajo los alerones delanteros.",
        "Sin patas de aterrizaje, sin tocar el suelo.",
    ]},
    {"id": "importa", "frases": [
        "¿Y por qué importa tanto?",
        "El transbordador espacial volvía de órbita planeando, como un avión.",
        "Pero ninguna etapa que hubiera llegado a órbita había vuelto a aterrizar de pie.",
        "Atraparla con la torre ahorra el peso de las patas, y la deja justo donde se vuelve a cargar.",
        "Es la mitad del gran plan de SpaceX: un cohete que se reutiliza entero, como un avión.",
        "La otra mitad, atrapar también el propulsor, esta vez falló.",
        "Y no es solo un récord. La NASA cuenta con una versión de esta nave para llevar astronautas a la superficie de la Luna.",
        "Además, con veintidós horas y media, es la misión más larga de Starship hasta ahora.",
    ]},
    {"id": "sigue", "frases": [
        "¿Y ahora qué sigue?",
        "SpaceX tiene que averiguar qué le pasó al propulsor antes del próximo vuelo.",
        "Y la nave cuarenta y dos ya está en la torre. Por primera vez, los ingenieros pueden revisar pieza por pieza una Starship que volvió de órbita.",
        "Cada loseta del escudo, cada alerón y cada motor les dirá cuánto falta para volver a volar la misma nave.",
    ]},
    {"id": "cifras", "frases": [
        "Repasemos el vuelo en cifras.",
        "Veintidós horas y treinta y dos minutos de misión.",
        "Catorce vueltas a la Tierra.",
        "Veintiséis satélites en órbita.",
        "Treinta y tres motores para despegar, y uno solo al final, para detenerse entre los brazos.",
        "Una captura lograda, y otra pendiente.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Una nave atrapada, un propulsor perdido y veintiséis satélites en órbita.",
        "El vuelo quince no fue perfecto. Pero fue histórico.",
        "En T Menos Cero te explicamos cada lanzamiento así, en tres dimensiones.",
        "Suscríbete, y nos vemos en el próximo despegue.",
    ]},
]

for _e in ESCENAS[1:-1]:
    _e.setdefault("pre", 0.5)
    _e.setdefault("post", 0.5)
for _id, _p in {"despegue": 2.0, "separa": 1.2, "propulsor": 2.0, "starlink": 2.5, "reentrada": 2.5, "vueltas": 1.5}.items():
    next(e for e in ESCENAS if e["id"] == _id)["post"] = _p
ESCENAS[0]["post"] = 0.3
ESCENAS[-1]["pre"] = 0.3
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo="Cinematic space-launch underscore: deep pulsing analog synth bass, ticking countdown percussion, wide airy pads, "
           "minimal and precise like a rocket launch webcast, instrumental only, no vocals.",
    escenas={e["id"]: ("", 0) for e in ESCENAS},
    tramos=[(["gancho", "presenta", "plan"], "biblioteca"), (["despegue", "maxq", "separa"], "biblioteca"),
            (["propulsor", "orbita"], "biblioteca"), (["starlink", "vueltas"], "biblioteca"),
            (["reentrada", "llegada", "lenta"], "biblioteca"), (["importa", "sigue", "cifras", "cierre"], "biblioteca")])

SFX_ELEVEN = {
    "hud": dict(prompt="Short soft digital interface beep, mission control telemetry readout, clean and quiet", seg=0.5, variantes=4),
    "tic": dict(prompt="Very short soft digital tick, a data row appearing on a screen", seg=0.3, variantes=3),
    "ignicion": dict(prompt="Dozens of huge rocket engines igniting on a launch pad: crackling roar building into thunder", seg=4.0),
    "despegue": dict(prompt="Gigantic rocket liftoff, deep crackling thunderous roar heard from a few kilometers, sustained", seg=6.0),
    "viento": dict(prompt="Heavy aerodynamic buffeting and low rumbling wind on a rocket going supersonic", seg=3.0),
    "corte": dict(prompt="Rocket engines shutting down abruptly: roar cuts to silence with a low thump", seg=1.5),
    "caliente": dict(prompt="Violent rocket hot staging: upper stage engines ignite with a blast, metallic bang and fire roar", seg=3.0),
    "encendido": dict(prompt="Rocket engine relight in flight: short ignition pop then a steady powerful roar", seg=2.5, variantes=3),
    "falla": dict(prompt="Engine failing to ignite: sputtering cough, then a short electronic warning beep", seg=1.5),
    "rcs": dict(prompt="Cold gas thruster puffs, short pneumatic bursts of a spacecraft turning", seg=1.2, variantes=2),
    "whoosh": dict(prompt="Deep smooth cinematic whoosh, camera pulling far away", seg=1.3, variantes=3),
    "caida": dict(prompt="High-speed descent wind roar, a large object falling through the atmosphere", seg=3.0),
    "alarma": dict(prompt="Mission control abort alert: two low urgent electronic tones", seg=1.2),
    "explosion": dict(prompt="Distant massive explosion over the sea, deep boom rolling across water", seg=3.0),
    "apagado": dict(prompt="Soft engine cutoff in the vacuum of space, muffled rumble fading out", seg=1.2),
    "compuerta": dict(prompt="Spacecraft cargo door sliding open in space: low mechanical hum and soft clunk", seg=2.0),
    "satelite": dict(prompt="Small satellite released from a dispenser: soft spring push and faint click", seg=0.8, variantes=3),
    "plasma": dict(prompt="Spacecraft reentry plasma: roaring hiss of superheated air, deep rumble, crackling", seg=6.0),
    "estampido": dict(prompt="Double sonic boom heard from a distance, two sharp thunderous cracks", seg=1.5),
    "brazos": dict(prompt="Giant mechanical steel arms closing on a launch tower: hydraulic whine and heavy metal clank", seg=2.5),
    "toque": dict(prompt="Huge metal rocket settling onto steel arms: deep metallic thud and creak, engine hiss fading", seg=2.5),
    "campana": dict(prompt="Bright clean notification chime, two rising bell notes", seg=1.0),
    "pulso": dict(prompt="Low cinematic sub bass hit with short reverb tail, dramatic title impact", seg=2.0),
}
