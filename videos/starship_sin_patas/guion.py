# -*- coding: utf-8 -*-
"""¿Por qué Starship NO tiene patas? La verdadera razón de los palillos (~11 min, horizontal). 2.º video de T Menos Cero.
Kit LÍNEA 3D (`nucleo/linea3d.py` + `linea3d_starship.py` + `linea3d_cohetes.py`) + VIDEO REAL de cada suceso que nombra la voz
(yt-dlp, con crédito) + fotos reales en marcos de alambre. Voz ElevenLabs «Alberto Rodríguez». Sin subtítulos quemados.
Datos comprobados el 14-nov-2026: `datos.md` (fuentes al final). Nada de cifras sin fuente: sin masa de patas de Super Heavy,
sin velocidad ni precisión de captura, sin «13 motores» en la quema de aterrizaje.
Clips (crédito): SpaceX (f5 hI9HQfCAw64, f6 CMGiNKcVSek, f7 Pn6e1O5bEyA, «How Not to Land» bvim4rsNHkQ, «The Falcon has landed»
ANv5UfZsvZQ, CRS-8 sYmQQn_ZSys, SN10 gA6ppby3JC8, SN15 7CZTLogln34); VideoFromSpace (f8 _YYGHhHmNtQ, f11 M8Bu2fFKOUM, vuelo 15
KqGPHd7XAbs); CNN (Ob1oxxIPWzk, B22 sobre el golfo).
"""

TITULO = "¿Por qué Starship NO tiene patas? La verdadera razón de los palillos"
ARCHIVO = "starship_sin_patas"
ESTILO_VISUAL = "documental"     # kit linea3d + video real con capas
DURACION = None
BPM = 240
GAP = 0.42
SUBTITULOS = False
MEZCLA = dict(musica=-24.0, sfx=-22.0, fx=-17.0)
CER_MAX_POR_FRASE = {"precio_2": 0.05, "torre_3": 0.05, "contras_1": 0.05, "cierre_2": 0.05, "cierre_3": 0.12, "historial_7": 0.05}
GAP_MAX_POR_FRASE = {"contras_1": 0.9}   # pausa natural entre oraciones   # Whisper: «Mechacilla», «Stardaze», «T-Cero»
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1,
           stability=0.5)

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Este es el cohete más grande que se ha construido.",
        "Y cuando vuelve del espacio, no aterriza sobre patas, como los demás cohetes.",
        "Lo atrapan en el aire, con dos brazos gigantes de la misma torre desde la que despegó.",
        "El Falcon 9, el otro cohete de SpaceX, sí tiene patas. Y con ellas cambió la historia de los cohetes.",
        "Entonces, ¿por qué Starship no?",
        "La respuesta tiene que ver con el peso, con el tiempo, y con un plan mucho más ambicioso que solo aterrizar.",
        "Esta es la verdadera razón de los palillos.",
    ]},
    {"id": "falcon", "frases": [
        "Empecemos por el cohete que sí tiene patas.",
        "La primera etapa del Falcon 9 lleva cuatro, plegadas contra el cuerpo durante el despegue.",
        "Son de fibra de carbono y aluminio, y abiertas miden unos dieciocho metros de punta a punta.",
        "El cohete frena con sus propios motores, y las patas se abren en los últimos segundos, justo antes de tocar el suelo.",
        "Y no hay segunda oportunidad: el Falcon 9 no puede quedarse flotando. Incluso con un solo motor al mínimo, empuja más de lo que pesa la etapa casi vacía.",
        "Así que su frenado tiene que terminar justo en el instante en que toca el suelo.",
        "Así aterrizó por primera vez, el veintiuno de diciembre de dos mil quince, en Cabo Cañaveral.",
        "Unos meses después lo logró sobre una barcaza, en medio del océano.",
        "Y desde entonces, un mismo propulsor ha llegado a volar treinta y siete veces.",
    ]},
    {"id": "precio", "frases": [
        "Pero las patas tienen un precio.",
        "Las cuatro pesan casi dos toneladas: cerca de una décima parte de lo que pesa la etapa vacía.",
        "Y en un cohete, cada kilo de más se paga en combustible, o en carga que ya no puedes subir.",
        "Además, las patas pueden fallar.",
        "En enero de dos mil dieciséis, una pata de este Falcon 9 no se trabó. El cohete se inclinó, cayó, y explotó sobre la barcaza.",
        "Y aunque todo salga bien, el cohete queda lejos de su plataforma.",
        "Si aterrizó en una barcaza, tarda días solo en volver a puerto. Luego hay que levantarlo con grúas, transportarlo, y prepararlo otra vez.",
    ]},
    {"id": "prototipos", "frases": [
        "Y aquí viene lo curioso: al principio, este cohete también tenía patas.",
        "Los primeros prototipos de la nave aterrizaban sobre unas patas cortas.",
        "En marzo de dos mil veintiuno, el prototipo SN10 tocó el suelo con demasiada fuerza. Sus patas no aguantaron, y minutos después explotó.",
        "Dos meses más tarde, el SN15 por fin aterrizó entero.",
        "Pero SpaceX ya pensaba en algo mucho más grande: el propulsor Super Heavy, de más de setenta metros y treinta y tres motores.",
        "Para un cohete así, unas patas tendrían que ser enormes. Y cada tonelada contaría.",
    ]},
    {"id": "idea", "frases": [
        "El treinta de diciembre de dos mil veinte, Elon Musk anunció un plan que parecía una broma.",
        "Ningún cohete de ese tamaño había sido atrapado así.",
        "Iban a atrapar el propulsor con el brazo de la torre de lanzamiento.",
        "Su razón cabía en un mensaje: ahorra el peso y el costo de las patas,",
        "y permite poner el propulsor sobre la mesa de lanzamiento al instante, listo para volar otra vez en menos de una hora.",
        "Ese es el verdadero objetivo: no solo recuperar el cohete, sino usarlo como un avión. Aterrizar, cargar combustible, y despegar.",
        "La torre deja de ser solo una plataforma. Se convierte en las patas del cohete.",
    ]},
    {"id": "torre", "frases": [
        "Así funciona. La torre de Starbase, en Texas, mide ciento cuarenta y seis metros.",
        "Por fuera sube y baja un carro con dos brazos enormes. Lo mueve un cabrestante en la base, con cables que pasan por una polea en lo alto.",
        "Un sistema hidráulico abre y cierra los brazos, como unos palillos chinos. Por eso en SpaceX los llaman así: los palillos.",
        "Los aficionados le pusieron otro nombre a la torre: Mechazilla.",
        "El propulsor no se apoya de cualquier manera.",
        "Sus aletas de rejilla, arriba, hacen de asas: son lo que se posa sobre los rieles de los brazos.",
        "Todo el peso del cohete cuelga de ahí, a decenas de metros del suelo.",
    ]},
    {"id": "captura", "frases": [
        "Ahora veamos una captura paso a paso.",
        "Tras separarse de la nave, el propulsor da media vuelta y enciende sus motores para regresar a la costa.",
        "Cae de cola durante varios minutos, guiado por sus aletas de rejilla.",
        "Mientras tanto, la torre lo espera con los brazos abiertos, a la altura justa.",
        "Si algo no está perfecto, en el cohete o en la torre, la captura se cancela y el propulsor cae en el mar.",
        "De sus treinta y tres motores, solo los trece del centro pueden girar para dirigirlo. Y son ellos los que hacen la parte fina.",
        "Ya cerca, enciende sus motores para frenar, y al final solo quedan los tres del centro.",
        "Se desliza de lado hasta quedar entre los brazos, flota un instante, y los palillos se cierran.",
    ]},
    {"id": "historial", "frases": [
        "¿Y cuántas veces ha funcionado?",
        "La primera fue el trece de octubre de dos mil veinticuatro, en el quinto vuelo. Al primer intento.",
        "En el sexto vuelo, la torre se dañó durante el despegue, y la captura se canceló. El propulsor terminó en el golfo de México.",
        "En enero de dos mil veinticinco, el séptimo vuelo lo logró otra vez,",
        "y en marzo, el octavo también, aunque dos de sus motores no volvieron a encender.",
        "En el noveno vuelo, el propulsor del séptimo despegó otra vez. Fue el primer Super Heavy reutilizado.",
        "Después, SpaceX pasó seis vuelos sin intentar otra captura. Hizo pruebas en el mar, con propulsores reutilizados.",
        "Y estrenó la tercera versión del cohete, más alta y con motores nuevos. Sus primeros propulsores bajaron al golfo, y no todos lo hicieron con suavidad.",
        "En el vuelo quince, el trece de noviembre, volvió a intentarlo. Pero el propulsor detectó un problema, abortó por su cuenta, y se perdió sobre el golfo.",
        "En total: tres propulsores atrapados, en cinco intentos.",
    ]},
    {"id": "nave", "frases": [
        "Pero en ese mismo vuelo pasó algo que nunca se había visto.",
        "La nave, la parte de arriba, volvió de órbita después de catorce vueltas a la Tierra, y la torre también la atrapó.",
        "Es la primera nave atrapada por una torre de lanzamiento.",
        "Veintidós horas y media después del despegue, con un solo motor encendido, se detuvo entre los brazos.",
        "Y es más difícil que con el propulsor: llega cayendo de panza, gira a vertical en el último momento, y baja frenando hasta quedar entre los brazos.",
        "Se apoya en ellos por unos puntos reforzados cerca de la punta, junto a sus alerones delanteros.",
        "Si la nave tuviera patas, cargaría ese peso todo el viaje: al subir, en órbita, y de regreso.",
    ]},
    {"id": "contras", "frases": [
        "Entonces, ¿los palillos son mejores que las patas? No siempre.",
        "Sin torre, no hay dónde aterrizar. Hoy solo una torre en el mundo puede atrapar una nave: la de la plataforma dos de Starbase. Otras se construyen en Florida.",
        "Y si una captura sale mal, no solo se arriesga el cohete, también la torre, que es mucho más difícil de reemplazar.",
        "En la Luna tampoco hay torres. Por eso la versión lunar de Starship, la que la NASA usará para llevar astronautas, sí tiene patas.",
        "Allá la gravedad es seis veces menor, y unas patas pesan poco.",
        "Y el Falcon 9 seguirá con las suyas, porque muchas veces aterriza en barcazas en medio del mar, donde no cabe una torre.",
    ]},
    {"id": "cuentas", "frases": [
        "Pongámoslo lado a lado.",
        "Con patas, el cohete carga peso extra en cada vuelo. Con palillos, ese peso se queda en tierra, en la torre.",
        "Con patas, puede aterrizar en tierra o en el mar. Con palillos, solo donde hay una torre.",
        "Con patas, el cohete termina lejos y hay que traerlo de vuelta. Con palillos, ya está en casa.",
        "Y si algo falla, con patas se pierde el cohete. Con palillos, también se arriesga la torre.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Patas o palillos: las dos ideas buscan lo mismo, un cohete que vuelva y vuele otra vez.",
        "El Falcon 9 lo consigue aterrizando casi donde sea. Starship apuesta por algo más grande: que lo atrapen justo donde despega, para volar de nuevo casi de inmediato.",
        "Si quieres ver cómo lo intentan en el próximo vuelo, explicado en tres dimensiones,",
        "suscríbete a T Menos Cero. Nos vemos en el próximo despegue.",
    ]},
]

for _e in ESCENAS[1:-1]:
    _e.setdefault("pre", 0.5)
    _e.setdefault("post", 0.6)
for _id, _p in {"falcon": 1.0, "precio": 1.5, "prototipos": 1.5, "captura": 1.5, "historial": 1.5, "nave": 1.5}.items():
    next(e for e in ESCENAS if e["id"] == _id)["post"] = _p
ESCENAS[0]["post"] = 0.3
ESCENAS[-1]["pre"] = 0.3
TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo="Cinematic space-engineering explainer underscore: deep pulsing analog synth bass, precise ticking percussion, wide airy pads, "
           "curious and confident like a rocket launch webcast, instrumental only, no vocals.",
    escenas={e["id"]: ("", 0) for e in ESCENAS},
    tramos=[(["gancho", "falcon"], "biblioteca"), (["precio", "prototipos"], "biblioteca"), (["idea", "torre"], "biblioteca"),
            (["captura", "historial"], "biblioteca"), (["nave", "contras", "cuentas", "cierre"], "biblioteca")])

SFX_ELEVEN = {
    "hud": dict(prompt="Short soft digital interface beep, mission control telemetry readout, clean and quiet", seg=0.5, variantes=4),
    "tic": dict(prompt="Very short soft digital tick, a data row appearing on a screen", seg=0.3, variantes=3),
    "whoosh": dict(prompt="Deep smooth cinematic whoosh, camera moving fast through space", seg=1.3, variantes=3),
    "pulso": dict(prompt="Low cinematic sub bass hit with short reverb tail, dramatic title impact", seg=2.0, variantes=2),
    "patas": dict(prompt="Rocket landing legs unfolding: pneumatic hiss and heavy mechanical clunk locking into place", seg=1.8),
    "aterriza": dict(prompt="Rocket booster touching down on a concrete pad: deep engine roar cutting off, low thud, hiss", seg=3.0),
    "vuelco": dict(prompt="Huge metal tube tipping over and crashing onto a steel deck, then a muffled explosion", seg=3.0),
    "explosion": dict(prompt="Distant massive explosion, deep boom rolling across flat land", seg=3.0),
    "brazos": dict(prompt="Giant mechanical steel arms closing on a launch tower: hydraulic whine and heavy metal clank", seg=2.5, variantes=2),
    "toque": dict(prompt="Huge metal rocket settling onto steel arms: deep metallic thud and creak, engine hiss fading", seg=2.5),
    "cabrestante": dict(prompt="Industrial winch reeling steel cable, low motor hum and rhythmic clicking", seg=2.5),
    "encendido": dict(prompt="Rocket engine relight in flight: short ignition pop then a steady powerful roar", seg=2.5, variantes=2),
    "caida": dict(prompt="High-speed descent wind roar, a large object falling through the atmosphere", seg=3.0),
    "alarma": dict(prompt="Mission control abort alert: two low urgent electronic tones", seg=1.2),
    "pesa": dict(prompt="Heavy metal weight dropping onto a scale, deep clunk with a short ring", seg=1.2),
    "sello": dict(prompt="Rubber stamp slammed onto paper, firm thump", seg=0.6, variantes=2),
    "campana": dict(prompt="Bright clean notification chime, two rising bell notes", seg=1.0),
}
