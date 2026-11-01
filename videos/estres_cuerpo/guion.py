# -*- coding: utf-8 -*-
"""Cuerpo en Neón, 3.er video (20-oct-2026): «5 cosas que el estrés le hace a tu cuerpo sin que te des cuenta».
Estilo «línea blanca + neón» (docs/estilo_linea_neon.md; modelos: videos/freno_enojo/, videos/agotado_cortisol/, sin reciclar
escenas). Fórmula: canales/formula/cuerpo_en_neon.md. Variable nueva pedida por el usuario (20-oct): video LARGO de ~12 min
que cubre VARIOS temas (5 zonas del cuerpo, cada una con su técnica) en vez de una emoción + 5 técnicas de ~5 min.

Hechos (ficha antes de escribir; Whisper nunca es fuente; DOI verificados en Crossref el 20-oct-2026):
- Alarma: amígdala -> hipotálamo -> rama simpática (adrenalina desde la médula suprarrenal, segundos) y eje HPA
  (CRH -> ACTH -> cortisol, minutos). Freno: sistema parasimpático, sobre todo el nervio vago («descansar y digerir»).
- Nervio vago: ~80 % de sus fibras son aferentes (del cuerpo al cerebro). Breit et al. 2018, Front Psychiatry 9:44,
  doi:10.3389/fpsyt.2018.00044. Al exhalar el freno vagal baja el ritmo cardiaco (arritmia sinusal respiratoria).
- Estrés -> respiración rápida y alta (pecho, músculos accesorios del cuello) -> sensación de opresión / «no me entra aire».
  AVISO de seguridad: dolor de pecho fuerte, nuevo o con falta de aire = urgencias primero.
- Balban et al. 2023, Cell Rep Med 4(1):100895, doi:10.1016/j.xcrm.2022.100895 (Stanford, Huberman y Spiegel): ~100
  personas, 5 min diarios durante un mes; el suspiro cíclico (2 inhalaciones por la nariz + exhalación larga por la boca)
  mejoró el ánimo más que la meditación de atención plena y bajó la frecuencia respiratoria en reposo.
- Sistema nervioso entérico: ~500 millones de neuronas (rango citado 200-600 M). Con la alarma, la sangre se va a los
  músculos, el estómago se vacía más lento y el colon puede acelerarse («mariposas», nudo, ir al baño antes de un examen).
- Respiración diafragmática lenta (~6 por minuto) = estímulo vagal; se usa en trastornos digestivos funcionales.
- Músculos: el estrés sube el tono muscular (preparación para pelear/huir); bruxismo de vigilia asociado al estrés;
  cefalea tensional = el dolor de cabeza más común. Relajación muscular progresiva (Edmund Jacobson, 1929-1938).
  Manzoni et al. 2008, BMC Psychiatry 8:41, doi:10.1186/1471-244X-8-41: el entrenamiento en relajación reduce la ansiedad
  con efecto mediano a grande (meta-análisis de 27 estudios).
- Despersonalización/desrealización: Hunter, Sierra y David 2004, Soc Psychiatry Psychiatr Epidemiol 39:9-18,
  doi:10.1007/s00127-004-0701-4: episodios pasajeros a lo largo de la vida en 26-74 % de la población; el trastorno ~1-2 %.
  Mecanismo prudente: con ansiedad extrema el cerebro amortigua las señales emocionales y del cuerpo (como un fusible).
- Reflejo de inmersión: agua fría en la cara (frente, ojos, mejillas) -> nervio trigémino -> vago -> baja el ritmo cardiaco.
  Es la habilidad TIP de la terapia dialéctico conductual. 5-4-3-2-1 = técnica de anclaje con poca investigación formal.
- Cohen, Tyrrell y Smith 1991, N Engl J Med 325:606-612, doi:10.1056/NEJM199108293250903: 394 voluntarios sanos con gotas
  nasales de virus del resfriado; a más estrés, más infecciones y más resfriados, en escalera (dosis-respuesta).
- Cohen et al. 2015, Psychol Sci 26(2):135-147, doi:10.1177/0956797614559284 (Carnegie Mellon): 404 adultos; 14 noches
  de entrevistas sobre conflictos y abrazos; luego virus del resfriado. El apoyo y los abrazos amortiguaron el riesgo de
  infección ligado al conflicto; entre los infectados, más abrazos = síntomas menos graves.
- Hiperventilación: respirar de más baja el CO2 de la sangre (hipocapnia) -> hormigueo, mareo, más sensación de ahogo.
- ~90 % de la serotonina del cuerpo se produce en el intestino (células enterocromafines); no es la misma reserva del cerebro.
- Kiecolt-Glaser et al. 1995, Lancet 346:1194-1196, doi:10.1016/S0140-6736(95)92899-5 (Ohio State): 13 cuidadoras de un
  familiar con demencia vs 13 controles; biopsia de 3,5 mm en el brazo; cicatrizó 9 días más lento (~24 %).
- Posición de reposo mandibular: labios juntos, dientes separados, lengua en el paladar.
- Cortisol sostenido -> el sistema inmune se desregula (agudo lo activa, crónico lo frena): simplificación prudente.
"""

TITULO = "5 cosas que el estrés le hace a tu cuerpo sin que te des cuenta"
ARCHIVO = "estres_cuerpo"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 72
GAP = 0.30

CER_MAX_POR_FRASE = {"defensas_5": 0.03}   # Whisper: «Kiecolt-Glaser» -> «Kicold Glaser»
# Cola alta pero transcripción completa (CER 0 y 0,014): terminan hablando hasta el final del wav
TAIL_MAX_POR_FRASE = {"mandibula_6": 1.05, "defensas_5": 0.6}
# Voz del canal: «Alejandro Durán — Warm, Deep» (biblioteca pública de ElevenLabs), la misma de freno_enojo y agotado_cortisol
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    clips_s=[10] * 7,         # 7 x 10 s = 49 puntos (el usuario: «tenemos 50 puntos de Flow, aprovéchalos al inicio», 20-oct)
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=240,
    img_s_lento=5.5,          # video de 12 min: ~130 imágenes
    fundido=0.25,
    ambiente=0.0,             # el sonido de Flow no encaja con el estilo: SFX propios
    ambiente_por={},
    carpeta_descargas="flow-estres_cuerpo",
)

FICHA = dict(
    estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white "
           "chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined "
           "in glowing bright yellow neon light with a soft golden glow; cinematic horizontal sixteen by nine composition, "
           "full-bleed scene that fills the entire frame edge to edge, no border, no frame",
    personajes={
        "el chico": "a simple stick-figure-like young man with a bald round white head, no hair, dot eyes and a small "
                    "expressive mouth, thin white line body, wearing a hoodie and sneakers drawn in white outline",
    },
    objeto="",
    epoca="present-day big city: crowded bus, open-plan office with desks and screens, small kitchen, street crossing, "
          "classroom before an exam, waiting room of a clinic, rooftop at dusk",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.",
)

TRANSICIONES = [("continua", 0.1)] * 40

# Música con Lyria adaptada al guion: solo descripción musical, en inglés. Tramos <= ~170 s.
LYRIA = dict(
    estilo="Calm modern science-explainer score for a film drawn in white chalk lines on black with glowing yellow neon: "
           "soft felt piano, warm analog synth pads, a gentle heartbeat-like low pulse, airy breathing textures. "
           "Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("A normal stressful day: a quick restless pulse, city hum, an unresolved piano figure.", 5),
        "alarma": ("The body's alarm system: a mechanical ticking build-up, then a sharp low swell, curious and tense.", 6),
        "pecho": ("Tight chest: short shallow synth breaths, a compressed pulse that slowly loosens into long exhaling pads.", 6),
        "panza": ("Unsettled stomach: wobbly bubbling plucks and a low churning drone that calms into a slow round groove.", 6),
        "mandibula": ("Clenched tension: a stiff, held string note and tight muted percussion that release into soft warmth.", 6),
        "fuera": ("Feeling far away: muffled, distant, dreamy reverb pads, like hearing through glass, then a clear cold "
                  "bright tone that brings you back.", 6),
        "defensas": ("Hidden battle: a soft marching pulse of tiny defenders, slightly worried, then warm and protective.", 6),
        "combo": ("Taking control: the piano motif returns steady and confident with soft strings.", 4),
        "cierre": ("Calm resolution: the same day, now breathing slowly; warm final chord fading to silence.", 3),
    },
    tramos=[(["gancho", "alarma"], "Begin from near silence with a quick restless pulse. End on a held low tone."),
            (["pecho"], "Begin on a held low tone. End softly on a calm sustained pad."),
            (["panza"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["mandibula"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["fuera"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["defensas"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["combo", "cierre"], "Begin softly on a calm sustained pad. End with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[serious] Un martes cualquiera. Vas en el camión, tarde otra vez, y sientes el pecho apretado.",
        "En la oficina, la panza se te revuelve antes de la junta.",
        "Por la tarde te duele la quijada, y ni sabías que llevabas horas apretando los dientes.",
        "[short pause] Por momentos todo se ve raro, lejano, como si vieras tu vida desde afuera.",
        "[sighs] Y justo cuando por fin llegan las vacaciones… te enfermas.",
        "[curious] No son cinco problemas distintos. Es uno solo, y no vive en tu cabeza. Vive en tu cuerpo.",
        "Hoy vamos a recorrer los cinco lugares donde el estrés se esconde, qué está pasando ahí dentro, y cómo apagar cada uno.",
    ]},
    {"id": "alarma", "frases": [
        "[thoughtful] Primero, conoce a la responsable. Dentro de tu cerebro hay una alarma del tamaño de una almendra: la amígdala.",
        "Cuando detecta peligro, no pregunta si es un león o un correo de tu jefe. Dispara igual.",
        "En segundos, tus glándulas suprarrenales sueltan adrenalina: el corazón acelera, los músculos se tensan, la respiración se dispara.",
        "Y en unos minutos llega la segunda ola: el cortisol, la hormona que mantiene la alarma encendida.",
        "[serious] Ese sistema es perfecto para escapar de un depredador. Dura unos minutos y luego se apaga.",
        "El problema es que hoy el peligro no se va. Son el tráfico, las deudas, los mensajes, todos los días.",
        "Una alarma que nunca se apaga deja de ser una alarma. Se vuelve el ruido de fondo de tu vida, y tu cuerpo lo paga en lugares muy concretos.",
        "[curious] Por suerte, tu cuerpo también tiene un freno. Un cable larguísimo que baja del cerebro hasta la panza: el nervio vago.",
        "Vago viene del latín, y significa errante, vagabundo. Porque este nervio pasea por casi todo: la garganta, el corazón, los pulmones, el estómago, el intestino.",
        "Cuando la alarma acelera, el vago es el que dice: tranquilo, ya pasó. Descansa y digiere.",
        "Y las cinco técnicas de hoy tienen algo en común: todas jalan ese freno.",
    ]},
    {"id": "pecho", "frases": [
        "[serious] Lugar número uno: el pecho.",
        "Con la alarma encendida, respiras rápido y alto, con la parte de arriba del pecho, como si fueras a correr.",
        "Hasta los músculos del cuello se ponen a jalar aire. Y esos músculos chiquitos se cansan y se acalambran.",
        "[short pause] Por eso sientes el pecho cerrado, o que el aire no te llena, aunque tus pulmones estén perfectamente bien.",
        "Y aquí viene la trampa: como sientes que te falta aire, respiras todavía más rápido. Pero en realidad te sobra.",
        "Al respirar de más, sacas demasiado dióxido de carbono de la sangre. Y eso provoca hormigueo en las manos, mareo, y más sensación de ahogo.",
        "[serious] Tu cuerpo lee esas señales como peligro, y la alarma sube otro escalón. Es un círculo que se alimenta solo.",
        "Ojo: si el dolor de pecho es fuerte, nuevo, o viene con falta de aire, eso no es para un video. Es para urgencias.",
        "[curious] Pero si es la opresión de siempre, aquí va un dato curioso: cada vez que sacas el aire, tu corazón late un poquito más lento.",
        "Al exhalar, el nervio vago pisa el freno. Al inhalar, lo suelta. Tu respiración es el pedal.",
        "[thoughtful] Técnica uno: el suspiro fisiológico.",
        "Toma aire por la nariz. Y sin soltarlo, toma un poquito más, otra vez por la nariz, hasta llenar del todo.",
        "Ahora sácalo lento por la boca, largo, hasta vaciarte.",
        "En 2023, en la Universidad de Stanford, un centenar de personas practicó una respiración durante 5 minutos al día, por un mes.",
        "Quienes hicieron este suspiro mejoraron su ánimo más que quienes hicieron meditación, y su respiración en reposo se volvió más lenta.",
        "[short pause] Dos inhalaciones por la nariz. Una exhalación larga por la boca. Con una o dos veces ya se nota.",
    ]},
    {"id": "panza", "frases": [
        "[curious] Lugar número dos: la panza.",
        "En las paredes de tu intestino hay unos 500 millones de neuronas. Tantas, que a veces lo llaman el segundo cerebro.",
        "Y no solo digiere. Ahí se fabrica la mayor parte de la serotonina de tu cuerpo, una de las sustancias que también usa tu cerebro para el ánimo.",
        "Y está conectado directo con el primero, por el mismo nervio vago.",
        "Lo sorprendente es la dirección: unas 8 de cada 10 fibras de ese nervio no bajan órdenes. Suben noticias, de la panza al cerebro.",
        "[serious] Cuando suena la alarma, tu cuerpo decide que digerir puede esperar. La sangre se va a los músculos de brazos y piernas.",
        "El estómago se vacía más lento, y por eso sientes la comida como piedra.",
        "Y el colon, en cambio, a veces se acelera. Por eso hay gente que corre al baño antes de un examen.",
        "[short pause] Las famosas mariposas no son poesía. Es tu intestino reaccionando a la alarma.",
        "Y como las noticias suben, la panza revuelta le confirma al cerebro que algo anda mal. Y la alarma suena más fuerte.",
        "[thoughtful] Técnica dos: respira con la panza.",
        "Pon una mano en el pecho y otra en el ombligo. Al tomar aire, solo debe subir la mano de abajo, como un globo que se infla.",
        "Inhala contando hasta 4, y saca el aire contando hasta 6. Así, unas 6 respiraciones por minuto.",
        "El diafragma, al bajar, masajea los órganos y estimula el nervio vago justo donde nace la conversación con tu intestino.",
        "Se usa en tratamientos para problemas digestivos ligados al estrés. Hazlo 5 minutos antes de comer, y tu panza recibe el mensaje: ya puedes trabajar.",
    ]},
    {"id": "mandibula", "frases": [
        "[curious] Lugar número tres: la quijada, los hombros y el cuello.",
        "Haz una prueba ahora mismo. ¿Tus dientes se están tocando? ¿Tus hombros están cerca de tus orejas?",
        "[short pause] Si dijiste que sí, no eres el único.",
        "La alarma prepara a tus músculos para pelear o huir. Los deja tensos, listos, y se le olvida avisarles cuando ya pasó el peligro.",
        "Mucha gente aprieta los dientes de día sin darse cuenta, frente a la pantalla, en el tráfico, leyendo un mensaje.",
        "Esa tensión sube por las sienes y la nuca. Y se vuelve el dolor de cabeza más común del mundo: el de tipo tensional.",
        "[serious] Y lo peor: un músculo que lleva horas tenso deja de sentirse tenso. Tu cerebro se acostumbra a la tensión, y la toma por normal.",
        "[thoughtful] Técnica tres: tensa para soltar.",
        "Se llama relajación muscular progresiva, y la inventó un médico de Chicago, Edmund Jacobson, hace casi cien años.",
        "Aprieta los puños con fuerza, 5 segundos. Y suelta de golpe. Quédate 10 segundos sintiendo cómo se aflojan.",
        "Luego los hombros: súbelos hasta las orejas, aguanta… y déjalos caer. Después la quijada: aprieta y suelta, con la boca entreabierta.",
        "El truco es el contraste. Al tensar a propósito, tu cerebro vuelve a notar la diferencia entre tenso y suelto.",
        "Y para la quijada, aprende su posición de descanso: labios juntos, dientes separados, y la lengua tocando suavemente el paladar.",
        "Los dientes solo deberían tocarse para masticar y tragar. El resto del día, deberían estar separados.",
        "Pega una nota pequeña en tu monitor o en el espejo. Cada vez que la veas, revisa: ¿dientes separados? ¿hombros abajo?",
        "Y si te despiertas con la quijada adolorida o los dientes desgastados, puede que también aprietes de noche. Eso ya es para el dentista.",
        "Un análisis de 27 estudios encontró que este tipo de entrenamiento baja la ansiedad de forma clara. Y solo toma unos minutos.",
    ]},
    {"id": "fuera", "frases": [
        "[thoughtful] Lugar número cuatro. Este es el más raro, y el que más asusta: sentirte fuera de tu cuerpo.",
        "Ves tus manos y parecen de otra persona. El mundo se ve plano, como detrás de un vidrio, como una película.",
        "[short pause] Si te ha pasado, respira: tiene nombre. Se llama despersonalización, y es mucho más común de lo que crees.",
        "Los estudios calculan que entre un cuarto y tres cuartos de la gente lo ha sentido alguna vez, casi siempre en épocas de mucho estrés o de poco sueño.",
        "[serious] Una explicación es que, cuando la alarma se queda demasiado tiempo al máximo, el cerebro baja el volumen de las emociones y de las señales del cuerpo.",
        "Funciona como un fusible: para que no te quemes, desconecta un poco. Y esa desconexión se siente como estar lejos.",
        "No es que te estés volviendo loco. Es un mecanismo de protección que se pasó de largo.",
        "[serious] Lo que lo empeora es el miedo a la sensación misma. Te asustas de sentirte raro, la alarma sube, y el fusible desconecta todavía más.",
        "Por eso saber qué es ya ayuda: le quita gasolina a ese círculo.",
        "[curious] Técnica cuatro: agua fría en la cara.",
        "Llena un recipiente con agua fría, o usa una toalla mojada con hielo, y ponla sobre la frente, los ojos y las mejillas durante unos 30 segundos.",
        "Es el reflejo de inmersión, el mismo que tienen los delfines y las focas al sumergirse. Los nervios de tu cara mandan la señal y el nervio vago frena el corazón.",
        "Los terapeutas lo usan para bajar una crisis en segundos. Y el frío te devuelve, de golpe, a tu piel.",
        "[thoughtful] Después, ancla tus sentidos: nombra 5 cosas que ves, 4 que puedes tocar, 3 que oyes, 2 que hueles y 1 que saboreas.",
        "Hay poca investigación formal sobre este conteo, pero obliga al cerebro a volver a lo que tiene enfrente.",
        "Si esa sensación no se va en semanas, o te pasa sin estrés de por medio, vale la pena contarlo a un profesional.",
    ]},
    {"id": "defensas", "frases": [
        "[curious] Lugar número cinco. El que no se siente, pero se nota: tus defensas.",
        "En 1991, en Inglaterra, unos investigadores hicieron algo que hoy suena a película.",
        "Reunieron a 394 voluntarios sanos, les midieron el estrés, y les pusieron en la nariz gotas con virus del resfriado.",
        "[serious] El resultado fue como una escalera: cuanto más estrés tenía alguien, más probable era que se infectara y se enfermara.",
        "Una explicación: el cortisol en dosis cortas activa tus defensas, pero cuando se queda alto semanas y semanas, las desordena y las frena.",
        "Y no solo con virus. En 1995, en la Universidad Estatal de Ohio, Janice Kiecolt-Glaser le hizo una pequeña herida en el brazo a dos grupos de mujeres.",
        "Un grupo cuidaba de un familiar con demencia, con estrés todos los días. El otro, no.",
        "[serious] A las cuidadoras, la misma herida les tardó 9 días más en cerrar. Casi una cuarta parte más de tiempo.",
        "[short pause] Y ese famoso resfriado de vacaciones tiene su lógica: semanas de alarma, y en cuanto aflojas, tus defensas ya iban cansadas.",
        "[thoughtful] Técnica cinco: abrazos. En serio.",
        "En 2015, en la Universidad Carnegie Mellon, Sheldon Cohen, uno de los autores de aquel estudio, llamó a 404 adultos durante 14 noches.",
        "Les preguntaba si habían tenido peleas ese día, y cuántos abrazos habían recibido. Luego, otra vez, gotas con virus.",
        "Los que se sentían apoyados estaban más protegidos contra el riesgo de infección que traen los conflictos.",
        "Y entre los que sí se enfermaron, los que recibían más abrazos tuvieron síntomas más leves.",
        "[curious] El contacto con alguien de confianza le dice a tu alarma algo que ninguna pastilla le dice igual: no estás solo, puedes bajar la guardia.",
        "Un abrazo largo, una llamada, una comida con alguien que te quiere. Es medicina, aunque no venga en caja.",
    ]},
    {"id": "combo", "frases": [
        "[serious] Recapitulemos. Cinco lugares, cinco frenos.",
        "Pecho apretado: suspiro fisiológico, dos inhalaciones y una exhalación larga.",
        "Panza revuelta: respira con el abdomen, 4 para entrar y 6 para salir.",
        "Quijada y hombros: tensa y suelta, músculo por músculo.",
        "Sensación de estar lejos: agua fría en la cara, y cinco cosas que ves.",
        "Y para tus defensas: abrazos, compañía, alguien de confianza.",
        "[curious] No tienes que hacerlas todas hoy. Escoge la del lugar donde más te pega el estrés, y practícala un minuto al día, cuando estés tranquilo.",
        "Así, cuando llegue el mal momento, tu cuerpo ya conoce el camino. Un freno que se practica responde más rápido.",
        "[thoughtful] Ninguna sustituye a un médico si algo se queda o empeora. Pero todas jalan el mismo cable: el freno que tu cuerpo ya trae de fábrica.",
    ]},
    {"id": "cierre", "frases": [
        "[thoughtful] Un martes cualquiera. Vas en el camión, tarde otra vez, y sientes el pecho apretado.",
        "[short pause] Pero esta vez sabes lo que es. Tomas aire dos veces por la nariz, y lo sueltas despacio.",
        "[sighs] La alarma sigue ahí. Solo que ahora… tú sabes dónde está el freno.",
    ]},
]
