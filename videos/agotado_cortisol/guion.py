# -*- coding: utf-8 -*-
"""Cuerpo en Neón, 2.º video (17-oct-2026): «Por qué estás agotado pero tu mente no se apaga de noche».
Estilo «línea blanca + neón» (docs/estilo_linea_neon.md; modelo: videos/freno_enojo/, sin reciclar escenas).
Fórmula: canales/formula/cuerpo_en_neon.md (misma de freno_enojo; variable = tema con señal fuera en 4 canales).

Hechos (ficha antes de escribir; Whisper nunca es fuente):
- Modelo de dos procesos del sueño (Borbély, 1982): presión de sueño (adenosina, se acumula despierto) + reloj circadiano.
- Cafeína = antagonista de receptores de adenosina; vida media ~5 h (rango 3-7 h en adultos sanos).
- Núcleo supraquiasmático (hipotálamo, sobre el quiasma óptico; ~20 000 neuronas, mm) recibe luz por las células
  ganglionares con melanopsina; de noche la glándula pineal libera melatonina.
- Cortisol: pico ~30-45 min tras despertar (respuesta de cortisol al despertar), mínimo cerca de la medianoche.
  Estrés crónico e insomnio se asocian a cortisol vespertino/nocturno más alto (eje HPA). Modelo de hiperactivación del
  insomnio; locus cerúleo = noradrenalina, alerta. «Sube y baja» cortisol/melatonina = simplificación prudente (ritmos opuestos).
- Efecto Zeigarnik (Bluma Zeigarnik, 1927): las tareas interrumpidas se recuerdan mejor que las terminadas.
- Scullin et al. 2018, J Exp Psychol Gen 147(1):139-146, doi:10.1037/xge0000374 (Baylor): 5 min escribiendo la lista de
  pendientes de mañana -> se durmieron ~9 min más rápido que quienes escribieron tareas terminadas; lista más detallada,
  más rápido.
- Haghayegh et al. 2019, Sleep Med Rev 46:124-135, doi:10.1016/j.smrv.2019.04.008: baño/ducha a 40-42,5 °C 1-2 h antes
  de dormir acorta la latencia ~10 min (36 %); vasodilatación distal -> baja la temperatura central (cae ~1 °C al dormir).
- Gooley et al. 2011, J Clin Endocrinol Metab 96(3):E463-72, doi:10.1210/jc.2010-2098 (Brigham and Women's / Harvard):
  luz de cuarto (< 200 lux) antes de dormir suprimió la melatonina y acortó su duración ~90 min.
- Barajado cognitivo («serial diverse imagining», Luc Beaudoin, Simon Fraser University): evidencia preliminar -> prudencia.
- Control de estímulos (Bootzin): levantarse si no se duerme en ~20 min; parte de la TCC-I, tratamiento de primera línea
  (American College of Physicians, 2016).
"""

TITULO = "Por qué estás agotado pero tu mente no se apaga de noche"
ARCHIVO = "agotado_cortisol"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 72
GAP = 0.30

# Falsos positivos de Whisper: «Uno.», «Dos.»… -> «1.», «2.»; «Zeigarnik» -> «Seygarnik»
CER_MAX_POR_FRASE = {"pendientes_1": 0.03, "lista_0": 0.22, "ducha_0": 0.24, "luz_0": 0.29, "barajar_0": 0.24,
                     "levantate_0": 0.15}
# Voz del canal: «Alejandro Durán — Warm, Deep» (biblioteca pública de ElevenLabs), la misma de freno_enojo
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    clips_s=[10] * 7,         # 7 x 10 s = 49 puntos (el usuario confirmó 50 puntos el 17-oct-2026), ~70 s de video
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.25,
    ambiente=0.0,             # el sonido de Flow no encaja con el estilo: SFX propios
    ambiente_por={},
    carpeta_descargas="flow-agotado_cortisol",
)

FICHA = dict(
    estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white "
           "chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined "
           "in glowing bright yellow neon light with a soft golden glow; cinematic horizontal sixteen by nine composition, "
           "full-bleed scene that fills the entire frame edge to edge, no border, no frame",
    personajes={
        "la mujer": "a simple stick-figure-like woman with a bald round white head, dot eyes and a small expressive mouth, "
                    "thin white line body, wearing loose pajamas drawn in white outline",
    },
    objeto="",
    epoca="present-day small apartment at night: bedroom with a bed, pillow, nightstand and window with the moon, "
          "bathroom with a shower, kitchen table, living room with a sofa",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion: solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Intimate nocturnal ambient score for a calm science explainer drawn in white chalk lines on black with glowing "
           "neon: soft felt piano, warm analog synth pads, a faint ticking-clock texture, subtle low pulse, airy night "
           "atmosphere. Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("Restless night: a quiet ticking pulse, a repeated unresolved piano figure, a mind that will not switch off.", 4),
        "relojes": ("Curious and mechanical: soft clockwork percussion, gentle arpeggios like sand falling through an hourglass.", 6),
        "cortisol": ("Uneasy tension: a nervous synth pulse that refuses to settle, low drone, alert and wired.", 6),
        "pendientes": ("Busy and cluttered: overlapping light plucks like open browser tabs, a looping restless motif.", 4),
        "truco": ("A turn toward hope: the pulse softens, a warm major chord opens.", 3),
        "lista": ("Calm focus: soft pencil-like plucks and a steady gentle piano, things being put in order.", 5),
        "ducha": ("Warm and flowing: liquid pads, gentle water-like textures, heat slowly fading into cool air.", 5),
        "luz": ("Dimming lights: pads gradually darkening and softening, tempo slowing, amber warmth.", 4),
        "barajar": ("Dreamy and playful: random soft bell tones drifting, floating, slightly surreal.", 4),
        "levantate": ("Patient and quiet: sparse piano, a slow walk, low lamp glow, no hurry.", 4),
        "combo": ("Warm resolution: the piano melody returns in a major key with soft strings, steady and confident.", 4),
        "cierre": ("Falling asleep: very soft pads fading out like sand settling, one last gentle warm chord.", 3),
    },
    tramos=[(["gancho", "relojes", "cortisol", "pendientes", "truco"],
             "Begin from near silence with a soft ticking pulse. End softly on a calm sustained pad."),
            (["lista", "ducha", "luz", "barajar", "levantate", "combo", "cierre"],
             "Begin softly on a calm sustained pad. End with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[tired] Las 11 de la noche. Llevas todo el día agotado, y por fin te arrastras a la cama.",
        "[sighs] Apagas la luz, cierras los ojos… y tu cabeza se enciende.",
        "[short pause] La junta de mañana. Lo que dijiste hace tres años. Ese mensaje que no contestaste.",
        "[curious] No estás roto. Dentro de ti hay dos relojes, y uno se quedó con el acelerador pisado.",
    ]},
    {"id": "relojes", "frases": [
        "[serious] El primero es un reloj de arena químico. Se llama adenosina.",
        "Cada hora que pasas despierto, tus neuronas queman energía y dejan este residuo, que se acumula como arena.",
        "Cuanta más adenosina, más te pesan los párpados. Eso es el cansancio.",
        "La cafeína tapa esos receptores. Y tarda unas 5 horas en bajar a la mitad: el café de las 4 sigue a medias a las 9.",
        "[thoughtful] El segundo reloj vive detrás de tus ojos: el núcleo supraquiasmático, más chico que un grano de arroz.",
        "Lee la luz. Y cuando oscurece, ordena soltar melatonina, la señal química de que ya es de noche.",
    ]},
    {"id": "cortisol", "frases": [
        "[serious] Y aquí entra el villano de la historia: el cortisol.",
        "Es la hormona del arranque. Sube en la mañana para despertarte, y debería caer a su punto más bajo cerca de la medianoche.",
        "Pero con un estrés que no se acaba, el sistema de alarma sigue mandando cortisol de noche.",
        "Y el cortisol y la melatonina se llevan como un sube y baja: mientras uno sigue arriba, al otro le cuesta subir.",
        "[sighs] El resultado: el reloj de arena, lleno. Pero la alarma, encendida.",
    ]},
    {"id": "pendientes", "frases": [
        "[curious] ¿Y por qué justo en la cama te asaltan los pendientes?",
        "En 1927, la psicóloga Bluma Zeigarnik notó que recordamos mejor las tareas interrumpidas que las terminadas.",
        "De día, el ruido las tapa. En el silencio de la noche, el cerebro abre todas las pestañas pendientes para no olvidarlas.",
    ]},
    {"id": "truco", "frases": [
        "[curious] La buena noticia: no hay que forzar el sueño. Hay que bajar la alarma y dejar que la arena haga lo suyo.",
        "Aquí van 5 formas. Y la primera te toma solo 5 minutos.",
    ]},
    {"id": "lista", "frases": [
        "[thoughtful] Uno. Saca los pendientes de tu cabeza.",
        "Antes de acostarte, escribe en papel todo lo que tienes que hacer mañana. Con detalle.",
        "En 2018, en la Universidad de Baylor, un grupo escribió su lista de pendientes 5 minutos antes de dormir.",
        "Se durmieron unos 9 minutos más rápido que quienes anotaron lo que ya habían terminado. Y entre más detallada la lista, mejor.",
        "Al cerebro le basta con saber que la pestaña quedó guardada.",
    ]},
    {"id": "ducha", "frases": [
        "[curious] Dos. Agua caliente, una hora antes.",
        "Para dormirte, la temperatura del centro de tu cuerpo tiene que bajar casi un grado.",
        "Una ducha caliente, una o dos horas antes de acostarte, manda la sangre a las manos y a los pies.",
        "Por ahí se escapa el calor, y el centro del cuerpo se enfría a tiempo. En promedio, te duermes unos 10 minutos antes.",
    ]},
    {"id": "luz", "frases": [
        "[serious] Tres. Apaga la luz de arriba.",
        "Tu reloj interno no sabe de focos: la luz fuerte le dice que todavía es de día.",
        "En un estudio de Harvard de 2011, la luz normal de una sala antes de dormir le recortó a la melatonina cerca de 90 minutos.",
        "La última hora, usa lámparas bajas y cálidas, y aleja el celular de tu cara.",
    ]},
    {"id": "barajar", "frases": [
        "[curious] Cuatro. Baraja tus pensamientos.",
        "Ya en la cama, elige una palabra cualquiera. Por ejemplo: pan.",
        "Con la primera letra, imagina cosas sin relación: una pera, un perro, un paraguas, un piano. Sin prisa.",
        "Cuando te aburras, pasa a la siguiente letra.",
        "Imita el pensamiento desordenado de cuando ya te estás quedando dormido. Hay poca investigación todavía, pero a mucha gente le funciona.",
    ]},
    {"id": "levantate", "frases": [
        "[thoughtful] Cinco. Si en unos 20 minutos no te duermes, levántate.",
        "Suena al revés, pero la cama tiene que significar dormir, no pelear con la almohada.",
        "Ve a otro cuarto con luz tenue, haz algo aburrido, y regresa solo cuando te pesen los ojos.",
        "Es parte de la terapia cognitivo conductual para el insomnio: el tratamiento que los médicos recomiendan primero, antes que las pastillas.",
    ]},
    {"id": "combo", "frases": [
        "[serious] El combo para esta noche.",
        "Ducha caliente una hora antes. Luces bajas. Y 5 minutos con la lista de mañana en papel.",
        "Si en la cama la mente arranca, baraja letras. Y si a los 20 minutos sigues despierto, levántate sin pelear.",
        "Y si te pasa casi todas las noches durante meses, vale la pena hablarlo con un médico.",
    ]},
    {"id": "cierre", "frases": [
        "[thoughtful] Las 11 de la noche. Apagas la luz y cierras los ojos.",
        "[short pause] Los pendientes están en el papel. La alarma, apagada.",
        "[sighs] Y esta vez, el único reloj que corre… es el de arena.",
    ]},
]
