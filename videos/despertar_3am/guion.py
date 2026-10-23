# -*- coding: utf-8 -*-
"""Cuerpo en Neón, 6.º largo (23-oct-2026): «¿Por Qué Te DESPIERTAS a las 3 de la Mañana?».
2.º video de la fórmula NUEVA (canales/formula/cuerpo_en_neon.md § «Revisión 22-oct»): título-situación, ~5 min,
escalera de tiempo (la noche hora por hora: 11 · 1 · 3 · 3:15 · antes del amanecer) + 3 cosas para hoy + frase citable +
pregunta a los comentarios. Sustituye a `corazon_roto` (n.º 2 de la tanda): el takotsubo ya lo cuentan `duelo_cuerpo` y su
Short la misma semana. Referencia (vidIQ, 23-oct): «¿Te despiertas a las 3 AM? ¡Tu cuerpo pide ayuda!» (drkhoob Spanish,
63 K subs) 4,4 M, 12:43; «Si te despiertas con la boca seca…» (Oswaldo Restrepo) ×180. Estilo «línea blanca + neón»
(docs/estilo_linea_neon.md; modelo de archivos: videos/duelo_cuerpo/, sin reciclar escenas).

Hechos (ficha antes de escribir; Whisper nunca es fuente; DOI verificados en Crossref el 23-oct-2026):
- Weitzman, Fukushima, Nogeire, Roffwarg, Gallagher, Hellman 1971, J Clin Endocrinol Metab 33(1):14-22,
  doi:10.1210/jcem-33-1-14: el cortisol sale en pulsos; mínimo en las primeras horas del sueño y sube en la segunda mitad
  de la noche hasta su pico al despertar.
- Ohayon 2008, J Psychiatr Res 43(1):48-54, doi:10.1016/j.jpsychires.2008.02.001 (8 937 adultos de EE. UU.): el 35,5 %
  se despierta de noche al menos 3 noches por semana.
- Ohayon, Carskadon, Guilleminault, Vitiello 2004, Sleep 27(7):1255-1273, doi:10.1093/sleep/27.7.1255 (metaanálisis): con
  la edad baja el sueño profundo (ondas lentas) y sube el tiempo despierto después de dormirse.
- Ebrahim, Shapiro, Williams, Fenwick 2013, Alcohol Clin Exp Res 37(4):539-549, doi:10.1111/acer.12006: el alcohol
  adelanta el sueño profundo en la primera mitad y rompe la segunda mitad de la noche.
- Tubbs, Fernandez, Grandner, Perlis, Klerman 2022, Front Netw Physiol 1:830338, doi:10.3389/fnetp.2021.830338 («The Mind
  After Midnight»): hipótesis de que despierto de madrugada la mente se inclina a lo negativo y a decidir peor.
- Tang, Schmidt, Harvey 2007, J Behav Ther Exp Psychiatry 38(1):40-55, doi:10.1016/j.jbtep.2005.07.004 (Oxford): vigilar
  el reloj aumentó la preocupación y alargó el tiempo para dormirse.
- Scullin, Krueger, Ballard, Pruett, Bliwise 2018, J Exp Psychol Gen 147(1):139-146, doi:10.1037/xge0000374 (Baylor,
  polisomnografía, 57 adultos): 5 min escribiendo la lista de pendientes de mañana → se durmieron más rápido que los que
  escribieron lo ya hecho (~9 min de diferencia).
- Ekirch 2001, Am Hist Rev 106(2):343-386, doi:10.1086/ahr/106.2.343: en la Europa preindustrial se hablaba de «primer
  sueño» y «segundo sueño», con un rato despierto a media noche.
Sin cifra: ciclos de ~90 min, la temperatura mínima de madrugada, despertares breves que no se recuerdan (fisiología de
manual). Lo del «hígado a las 3» (medicina china) no tiene medición: se nombra como creencia, sin burla.
"""

TITULO = "¿Por Qué Te DESPIERTAS a las 3 de la Mañana?"
ARCHIVO = "despertar_3am"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 72
GAP = 0.30

# Falsos positivos de Whisper: «La 1» -> «La una», «Uno:/Dos:» -> «1./2.», «Ekirch» -> «Eckert», «te dé» -> «te des»
CER_MAX_POR_FRASE = {"una_0": 0.08, "historia_1": 0.07, "hoy_1": 0.08, "hoy_3": 0.08}
TAIL_MAX_POR_FRASE = {}
# Voz del canal: «Alejandro Durán — Warm, Deep» (biblioteca pública de ElevenLabs), la de todos los largos del canal
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    clips_s=[10] * 9,         # 9 x 10 s = 63 puntos: el gancho y la primera parte de la noche en video
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=400,         # video de ~5 min: todo a una imagen cada ~4 s
    img_s_lento=4.5,
    fundido=0.25,
    ambiente=0.0,             # el sonido de Flow no encaja con el estilo: SFX propios
    ambiente_por={},
    carpeta_descargas="flow-despertar_3am",
)

FICHA = dict(
    estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white "
           "chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined "
           "in glowing bright yellow neon light with a soft golden glow; cinematic horizontal sixteen by nine composition, "
           "full-bleed scene that fills the entire frame edge to edge, no border, no frame",
    personajes={
        "el señor": "a simple stick-figure-like older man with a bald round white head, no hair, dot eyes, a small white "
                    "moustache and a small expressive mouth, thin white line body, wearing striped pajamas, drawn in white "
                    "outline",
    },
    objeto="his inner alarm clock: an old twin-bell alarm clock without numbers whose hands point to three o'clock",
    epoca="present day in Mexico: a small bedroom at night with a window, a nightstand and a lamp, a dark hallway, a small "
          "kitchen with a glass of water, the town rooftops under the moon",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (antes: `fab.py biblioteca sugerir despertar_3am`). Solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Calm nocturnal science-explainer score for a film drawn in white chalk lines on black with glowing yellow neon: "
           "soft felt piano, a gentle music-box, slow analog pads, a faint clock-like tick. Instrumental only, no vocals, "
           "never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("Waking in the dark at 3 a.m.: a single soft piano note, a faint ticking clock, a held breath.", 4),
        "once": ("Falling into deep sleep: slow descending pads, warm and heavy, like sinking into water.", 4),
        "una": ("The body at its minimum: almost still, cool airy pads, a slow low pulse.", 4),
        "tres": ("The inner alarm clock winds up: a music-box motif that slowly speeds up, a soft rising pulse.", 5),
        "mente": ("Thoughts at 3 a.m. turn dark: a minor piano figure that loops and grows a bit uneasy, restrained.", 4),
        "empeora": ("Things that make it worse: a curious plucked rhythm, light and steady.", 4),
        "historia": ("Candlelit old village night, first and second sleep: a gentle old-world lute-like melody.", 4),
        "hoy": ("Three small steps: steady warm piano, a calm hopeful pulse.", 4),
        "cierre": ("Back to sleep before dawn: tender lullaby piano, the ticking fades, a soft final chord.", 4),
    },
    tramos=[(["gancho", "once", "una"], "Begin from near silence with a single soft piano note. End softly on a calm sustained pad."),
            (["tres", "mente", "empeora"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["historia", "hoy", "cierre"], "Begin softly on a calm sustained pad. End with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[whispers] Abres los ojos. Está oscuro. Miras el reloj… y otra vez son las tres de la mañana.",
        "[thoughtful] No hay ruido, no tienes ganas de ir al baño, nadie te habló. Y aun así, ahí estás: despierto, con la cabeza dándole vueltas a todo.",
        "[short pause] Si te pasa, no eres el único. En un estudio con casi 9000 adultos, más de 1 de cada 3 se despertaba de noche, al menos tres veces por semana.",
        "Hoy vamos a ver, hora por hora, qué hace tu cuerpo mientras duermes. Por qué tantos se despiertan justo a esa hora. Y qué hacer para volver a dormir.",
    ]},
    {"id": "once", "frases": [
        "[calm] Las 11 de la noche.",
        "Te acuestas, y en unos minutos el cerebro baja de marcha. El sueño no es parejo: va en ciclos de una hora y media, como olas que suben y bajan.",
        "Y las primeras olas son las más hondas. Ahí está el sueño profundo, el que repara los músculos y limpia el cerebro.",
        "[curious] Casi todo el sueño profundo de la noche se gasta en las primeras horas. Después, ya no regresa igual.",
    ]},
    {"id": "una", "frases": [
        "[calm] La 1 de la mañana.",
        "Tu cuerpo está en su punto más bajo. El corazón late más lento, la presión baja y la temperatura sigue bajando hasta la madrugada.",
        "Y la hormona del estrés, el cortisol, está casi en cero. En 1971, en Nueva York, la midieron cada 20 minutos durante toda la noche.",
        "Vieron que se apaga al empezar a dormir. Pero no se queda apagada.",
    ]},
    {"id": "tres", "frases": [
        "[thoughtful] Las 3 de la mañana.",
        "Justo en la segunda mitad de la noche, el cortisol empieza a subir otra vez, en pequeños pulsos. Es tu despertador interno, preparándote para la mañana.",
        "Al mismo tiempo, las olas del sueño ya son más bajitas: más sueño ligero, más sueños.",
        "Y al final de cada ola, todos nos despertamos un momento. Normalmente, no lo recuerdas. Te acomodas la almohada y sigues.",
        "[short pause] El problema es cuando ese despertar coincide con el cortisol subiendo. Entonces ya no es un momento. Abres los ojos del todo.",
        "[curious] Y con los años pasa más. Al juntar decenas de estudios, se vio que el sueño profundo se va adelgazando con la edad, y el tiempo despierto a media noche crece.",
        "Por eso, después de los 50, despertarse de madrugada es de lo más común. No es que algo esté mal.",
    ]},
    {"id": "mente", "frases": [
        "[serious] Las 3 y cuarto.",
        "Ya estás despierto, y empieza lo peor: la cabeza. Las deudas, la salud, los hijos, aquella frase que dijiste hace años.",
        "[thoughtful] A esa hora, todo parece más grave. Y tiene explicación.",
        "En 2022, investigadores de Harvard y Arizona propusieron una idea: la mente despierta después de la medianoche se inclina hacia lo negativo.",
        "La parte del cerebro que pone freno y perspectiva está cansada, y el cuerpo está programado para dormir, no para pensar.",
        "[short pause] Por eso, un problema a las 3 de la mañana parece un abismo. Y a las 9, con luz, es solo un pendiente.",
    ]},
    {"id": "empeora", "frases": [
        "[curious] Hay cosas que lo empeoran.",
        "La copa de la noche. El alcohol te ayuda a caer dormido, pero en la segunda mitad de la noche rompe el sueño y te despierta.",
        "Los bochornos de la menopausia, que encienden el cuerpo de golpe. Y la vejiga, que con la edad pide ir al baño de madrugada.",
        "En internet hay quien dice que a las 3 es la hora del hígado. Lo que sí está medido es el cortisol, y el sueño que se hace más ligero.",
        "[serious] Y si roncas fuerte, o te despiertas ahogándote, eso no es estrés: puede ser apnea del sueño. Eso lo tiene que ver un médico.",
    ]},
    {"id": "historia", "frases": [
        "[thoughtful] Y ahora, algo que quizá te tranquilice.",
        "El historiador Roger Ekirch revisó diarios, cartas y juicios de hace siglos, en Europa.",
        "Y encontró que la gente hablaba de dos sueños: el primer sueño, y el segundo sueño. Entre uno y otro, se despertaban un rato a media noche.",
        "Rezaban, platicaban con su pareja, cuidaban el fuego. Y luego se volvían a dormir.",
        "[short pause] A nadie le parecía raro. Despertarse a media noche era parte de la noche.",
    ]},
    {"id": "hoy", "frases": [
        "[thoughtful] Entonces, ¿qué hacer cuando te despiertas a las 3? Tres cosas.",
        "Uno: no mires el reloj. En Oxford, a quienes les hicieron vigilar la hora, se preocuparon más y tardaron más en dormirse.",
        "Voltea el reloj, o deja el celular lejos de la cama.",
        "Dos: si en unos 20 minutos no te vuelves a dormir, levántate. Ve a otro cuarto con luz baja, y haz algo tranquilo hasta que te dé sueño.",
        "Así tu cerebro deja de asociar la cama con dar vueltas.",
        "Y tres: vacía la cabeza antes de acostarte. En 2018, en Texas, quienes escribieron 5 minutos la lista de pendientes del día siguiente se durmieron más rápido.",
        "Lo que queda en el papel, ya no tiene que cuidarlo tu cabeza a las 3 de la mañana.",
    ]},
    {"id": "cierre", "frases": [
        "[calm] Así que la próxima vez que abras los ojos de madrugada, recuerda: no te estás rompiendo. Tu cuerpo está haciendo lo que hace cada noche.",
        "[short pause] Despertarse no es el problema. El problema es pelearse con la noche.",
        "[thoughtful] Y cuéntame en los comentarios: ¿a qué hora te despiertas tú? ¿Y qué haces para volver a dormir?",
    ]},
]
