# -*- coding: utf-8 -*-
"""Cuerpo en Neón, 4.º largo (21-oct-2026): «Tu nervio vago: el freno que apaga la ansiedad».
Estilo «línea blanca + neón» (docs/estilo_linea_neon.md; modelos: videos/estres_cuerpo/, videos/agotado_cortisol/, sin
reciclar escenas). Fórmula: canales/formula/cuerpo_en_neon.md. Tema elegido por el usuario (21-oct) entre 3 con datos:
Rebelde-Mente «Haz Esto y Activa tu Nervio Vago…» ×4,43 (1 M vistas). Variable: tema monográfico de ~9 min (entre los de
~5 min y el recopilatorio de 13 min). Técnicas DISTINTAS de estres_cuerpo (allí: suspiro, panza, tensar, agua fría, abrazos).

Hechos (ficha antes de escribir; Whisper nunca es fuente; DOI verificados en Crossref + PubMed el 21-oct-2026):
- Vago = X par craneal; nace en el bulbo raquídeo (tronco encefálico); sale por el agujero yugular, baja por la vaina
  carotídea; laringe (laríngeo recurrente), corazón, pulmones, estómago, hígado, intestino hasta ~2/3 del colon. Dos nervios
  (izquierdo y derecho). «Vagus» = errante en latín. Principal nervio parasimpático.
- ~80 % de fibras aferentes: Breit et al. 2018, Front Psychiatry 9:44, doi:10.3389/fpsyt.2018.00044.
- Loewi 1921, Pflügers Arch 189:239-242, doi:10.1007/BF01738910. Relato del propio Loewi: noche antes del domingo de Pascua
  de 1921 despierta, apunta, no entiende la nota; la noche siguiente a las 3 a. m. vuelve la idea y va al laboratorio (Graz).
  Dos corazones de rana; el líquido del corazón estimulado frena al segundo. «Vagusstoff» = acetilcolina. Nobel 1936 (con Dale).
- Ritmo intrínseco del nodo sinusal ~100 lpm (90-110); en reposo el tono vagal lo baja a ~60-80. Arritmia sinusal
  respiratoria: inhalar acelera, exhalar frena. HRV (variabilidad) = índice más usado del tono vagal; la bajan estrés
  crónico, poco sueño, sedentarismo, alcohol. Atletas de resistencia: bradicardia de reposo (en parte vagal).
- Síncope vasovagal = la causa más común de desmayo; posición: acostarse con piernas elevadas. Desmayo sin causa clara o
  durante ejercicio = consultar.
- Borovikova, Tracey et al. 2000, Nature 405:458-462, doi:10.1038/35013070 (Feinstein, Manhasset, Nueva York): estimular el
  vago en ratas con endotoxemia atenuó el TNF y el choque. «Reflejo inflamatorio».
- Koopman et al. 2016, PNAS 113(29):8284-8289, doi:10.1073/pnas.1605635113: implante de estimulación vagal en artritis
  reumatoide; bajaron citocinas y la gravedad. FDA aprobó el SetPoint System para AR el 30-jul-2025 (PMA P240039).
- VNS implantado: epilepsia (FDA 1997), depresión resistente (FDA 2005). tVNS auricular: evidencia mixta.
- Resonancia ~6 respiraciones/min (0,1 Hz): máxima arritmia sinusal (Lehrer); exhalación más larga que la inhalación.
- Jungmann et al. 2018, JMIR Form Res 2(2):e10257, doi:10.2196/10257 (Universidad de Luxemburgo): frío con termodo en el
  cuello (lado derecho), mejilla y antebrazo, intervalos de 16 s; en el cuello subió la HRV y bajó la frecuencia cardiaca.
- Vickhoff et al. 2013, Front Psychol 4:334, doi:10.3389/fpsyg.2013.00334 (Gotemburgo): jóvenes de 18 años; tararear, himno,
  mantra lento; el canto pautado sube la arritmia sinusal y los corazones aceleran y frenan a la vez.
- Kok et al. 2013, Psychol Sci 24(7):1123-1132, doi:10.1177/0956797612470827 (UNC Chapel Hill): meditación de bondad vs
  lista de espera; más emociones positivas -> más tono vagal, mediado por sentirse conectado (espiral ascendente). Con
  críticas publicadas (Heathers et al. 2015): decirlo con prudencia.
"""

TITULO = "Tu nervio vago: el freno que apaga la ansiedad"
ARCHIVO = "nervio_vago"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 72
GAP = 0.30

# Falsos positivos de Whisper: «Uno:» -> «1.», «Loewi» -> «Lowy/Loewy», «Tracey» -> «Tracy», «neurocirujano» -> «neurocilujano»
CER_MAX_POR_FRASE = {"loewi_1": 0.03, "loewi_10": 0.03, "inflamacion_1": 0.03,
                     "tecnicas_1": 0.25, "tecnicas_4": 0.40, "tecnicas_8": 0.70, "tecnicas_12": 0.50}
TAIL_MAX_POR_FRASE = {}
# Voz del canal: «Alejandro Durán — Warm, Deep» (biblioteca pública de ElevenLabs), la de todos los largos del canal
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    clips_s=[10] * 7,         # 7 x 10 s = 49 puntos (el usuario, 21-oct: «50 puntos en Flow, aprovéchalos en las primeras escenas»)
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=240,
    img_s_lento=5.0,          # video de ~9 min: ~105 imágenes
    fundido=0.25,
    ambiente=0.0,             # el sonido de Flow no encaja con el estilo: SFX propios
    ambiente_por={},
    carpeta_descargas="flow-nervio_vago",
)

FICHA = dict(
    estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white "
           "chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined "
           "in glowing bright yellow neon light with a soft golden glow; cinematic horizontal sixteen by nine composition, "
           "full-bleed scene that fills the entire frame edge to edge, no border, no frame",
    personajes={
        "la chica": "a simple stick-figure-like young woman with a bald round white head, no hair, dot eyes and a small "
                    "expressive mouth, thin white line body, wearing a long scarf and a cardigan drawn in white outline",
        "Loewi": "an elderly 1920s European scientist drawn in realistic fine white engraving, round spectacles, white "
                 "moustache, bald top with short side hair, dark three-piece suit under a white lab coat",
    },
    objeto="the vagus nerve: one long branching glowing yellow neon line running from the base of the brain down the neck, "
           "around the heart and lungs, to the stomach and the intestines",
    epoca="present day: a school auditorium with rows of seats and a lectern, a small apartment at night, a park, a bathroom "
          "with a shower, a choir rehearsal room; and a 1921 laboratory in Graz, Austria, with glass flasks and brass apparatus",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.",
)

TRANSICIONES = [("continua", 0.1)] * 40

# Música con Lyria adaptada al guion: solo descripción musical, en inglés. Tramos <= ~170 s.
LYRIA = dict(
    estilo="Calm modern science-explainer score for a film drawn in white chalk lines on black with glowing yellow neon: "
           "soft felt piano, warm analog synth pads, a gentle heartbeat-like low pulse, airy breathing textures. "
           "Instrumental only, no vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("Stage fright: a fast nervous heartbeat pulse and a trembling high string, then a hopeful open chord.", 5),
        "cable": ("Mapping a long nerve through the body: a slow descending arpeggio, wondering, like following a river.", 6),
        "loewi": ("A 1921 night-time discovery: delicate music-box piano, ticking clock, rising curiosity, a soft eureka swell.", 6),
        "tono": ("The heart's brake: a pulse that gently speeds up and slows down with breathing, warm and steady.", 6),
        "falla": ("When the brake fails: a tense held drone, then a sudden drop and a hollow fading tone, careful and serious.", 5),
        "inflamacion": ("Hidden healing: a soft modern-lab texture, small glimmering plucks, quietly impressive.", 5),
        "mitos": ("Internet myths: a light ironic plucked rhythm that stops, then an honest calm pad.", 4),
        "tecnicas": ("Training the brake: steady confident piano, slow breathing pads, gentle humming-like warm tones.", 6),
        "cierre": ("Back on stage, now calm: the opening motif slowed down, warm final chord fading to silence.", 3),
    },
    tramos=[(["gancho", "cable"], "Begin from near silence with a nervous heartbeat pulse. End softly on a calm sustained pad."),
            (["loewi"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["tono", "falla"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["inflamacion", "mitos"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["tecnicas"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["cierre"], "Begin softly on a calm sustained pad. End with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[serious] Te toca hablar frente a todos. El corazón te golpea el pecho, te sudan las manos, y la voz empieza a temblar.",
        "Alguien te dice: respira hondo. Y tú piensas: qué consejo tan inútil.",
        "[short pause] Pero no lo es. Ese consejo jala un cable que llevas dentro desde que naciste.",
        "[curious] Un cable que baja de tu cerebro hasta tu panza, y que frena tu corazón miles de veces al día.",
        "Se llama nervio vago. Y en internet lo venden como el botón mágico contra la ansiedad.",
        "Hoy vamos a ver qué es de verdad, cómo se descubrió gracias a un sueño, qué pasa cuando falla, qué es mito, y cinco formas de entrenarlo que sí tienen ciencia.",
    ]},
    {"id": "cable", "frases": [
        "[thoughtful] Empecemos por el mapa.",
        "El nervio vago nace en el tronco del cerebro, justo donde el cerebro se une con la médula, detrás de la nuca.",
        "Sale del cráneo, baja por el cuello junto a las grandes arterias, y se va ramificando.",
        "Toca la garganta y las cuerdas vocales. Envuelve el corazón. Se mete en los pulmones. Y abraza el estómago, el hígado, y buena parte del intestino.",
        "Por eso se llama así. Vago viene del latín, y significa errante, el que vagabundea.",
        "[curious] Y en realidad no es uno. Son dos, uno por cada lado del cuerpo, como dos cables paralelos.",
        "Es la pieza central de lo que llamamos el sistema parasimpático: el modo de descansar y digerir.",
        "Si la alarma del estrés es el acelerador, el vago es el freno.",
        "[serious] Pero lo más sorprendente es hacia dónde viaja la información.",
        "Unas 8 de cada 10 fibras del vago no bajan órdenes. Suben noticias del cuerpo: cómo late el corazón, cómo está la panza, cuánto aire entra.",
        "Tu cerebro escucha a tu cuerpo mucho más de lo que le habla. Y eso va a ser clave para todo lo demás.",
    ]},
    {"id": "loewi", "frases": [
        "[thoughtful] Ahora, la historia de cómo se descubrió que este nervio habla. Y empieza con un sueño.",
        "Austria, 1921. La noche antes del domingo de Pascua, el farmacólogo Otto Loewi despierta de madrugada con una idea.",
        "La apunta en un papelito y se vuelve a dormir. [short pause] En la mañana, no entiende su propia letra.",
        "[sighs] Pasa el día desesperado. Y a la noche siguiente, a las 3 de la mañana, la idea regresa.",
        "Esta vez no se arriesga. Se levanta y se va directo al laboratorio.",
        "Toma dos corazones de rana, que siguen latiendo dentro de un líquido salado. Al primero le deja conectado su nervio vago.",
        "Estimula ese nervio con electricidad, y el corazón late más lento. Hasta ahí, nada nuevo.",
        "[curious] Luego toma el líquido que bañaba ese primer corazón, y lo pasa al segundo, uno que no tiene ningún nervio.",
        "Y el segundo corazón también se frena.",
        "[serious] El nervio había soltado algo en el líquido. Una sustancia química que llevaba el mensaje de frenar.",
        "Loewi la llamó la sustancia del vago. Hoy la conocemos como acetilcolina.",
        "Fue la primera prueba de que los nervios se comunican con químicos. Y en 1936 le dio el premio Nobel.",
    ]},
    {"id": "tono", "frases": [
        "[thoughtful] Esa misma sustancia está frenando tu corazón ahora mismo.",
        "Tu corazón tiene su propio marcapasos. Si lo dejaras solo, sin nervios, latiría unas 100 veces por minuto.",
        "Si estás sentado con 60 o 70, es porque el vago tiene el pie en el freno, todo el tiempo.",
        "[curious] Y ese freno se mueve con tu respiración. Cuando tomas aire, el vago afloja y el corazón acelera. Cuando lo sueltas, vuelve a pisar, y el corazón va más lento.",
        "Por eso un corazón sano no late como un metrónomo. Cambia un poquito entre latido y latido.",
        "A ese cambio se le llama variabilidad de la frecuencia cardiaca. Y es la forma más usada de medir qué tan ágil está tu freno, lo que se llama tono vagal.",
        "Mucha variabilidad en reposo suele ir con un freno ágil, que pisa y suelta rápido. Poca variabilidad, con un cuerpo que se quedó en alerta.",
        "Muchos relojes inteligentes ya la miden, y te la muestran por las mañanas.",
        "[serious] ¿Y qué es lo que la baja? Lo de siempre: el estrés que no se apaga, dormir poco, no moverse, y el alcohol.",
    ]},
    {"id": "falla", "frases": [
        "[serious] Ahora, qué pasa cuando el freno falla.",
        "Si el freno está flojo, la alarma se queda encendida más de lo necesario. El corazón tarda en bajar después de un susto, la digestión se vuelve pesada, y cuesta desconectarse de noche.",
        "[curious] Pero también puede pasar lo contrario: un frenazo.",
        "Hay gente que ve sangre, o una aguja, y se desmaya. No es debilidad. Es el vago.",
        "Primero sube la alarma. Y de golpe, el freno se pisa con todo: el corazón baja, los vasos se abren, la presión cae, y al cerebro le llega menos sangre por unos segundos.",
        "Se llama síncope vasovagal, y es la causa más común de desmayo.",
        "[thoughtful] Si sientes que viene, acuéstate y sube las piernas antes de caerte. Y si te desmayas sin una razón clara, o haciendo ejercicio, eso sí hay que revisarlo con un médico.",
    ]},
    {"id": "inflamacion", "frases": [
        "[curious] Y el vago guardaba otro secreto, que se descubrió apenas en el año 2000.",
        "En un laboratorio de Nueva York, el equipo del neurocirujano Kevin Tracey estimuló el nervio vago de unas ratas con una inflamación masiva en todo el cuerpo.",
        "Y la inflamación bajó. El nervio le había ordenado al sistema inmune que se calmara.",
        "Lo llamaron el reflejo inflamatorio. El vago no solo frena el corazón: también le baja el volumen a la inflamación.",
        "[serious] En 2016 lo probaron en personas con artritis reumatoide, con un pequeño implante que estimula el vago desde el cuello. Muchos mejoraron.",
        "Y en 2025, Estados Unidos aprobó el primer implante de este tipo para esa enfermedad.",
        "Desde los años noventa ya se usan implantes en el vago para algunos tipos de epilepsia, y después, para depresiones que no responden a otros tratamientos.",
        "Es decir: estimular este nervio es medicina real. Pero con un aparato y un cirujano, no con un truco.",
    ]},
    {"id": "mitos", "frases": [
        "[thoughtful] Y aquí entra internet.",
        "Busca nervio vago en redes y vas a encontrar de todo: masajes en la oreja que curan la ansiedad, golpecitos en el pecho, un truco de 30 segundos que reinicia tu sistema nervioso.",
        "[serious] Seamos claros. No hay botón de reinicio. Tu freno no se arregla en 30 segundos, igual que un músculo no se hace fuerte con una sola sentadilla.",
        "Hay estimuladores eléctricos que se ponen en la oreja, y se están investigando, pero los resultados todavía son mixtos.",
        "Lo que sí tiene datos es más aburrido, y funciona mejor: cosas pequeñas, repetidas, que entrenan el freno día a día.",
    ]},
    {"id": "tecnicas", "frases": [
        "[curious] Aquí van cinco.",
        "[thoughtful] Uno: exhala más largo de lo que inhalas.",
        "¿Recuerdas que el freno se pisa al soltar el aire? Pues alarga esa parte. Toma aire en 4 tiempos, y suéltalo en 6, o en 8.",
        "Cerca de 6 respiraciones por minuto, el corazón y la respiración entran en sintonía, y la variabilidad sube al máximo. Con 5 minutos al día ya estás entrenando el freno.",
        "[thoughtful] Dos: frío en el cuello.",
        "En 2018, en la Universidad de Luxemburgo, pusieron frío en pulsos cortos sobre un lado del cuello de voluntarios sanos, más o menos por donde pasa el vago.",
        "Comparado con no hacer nada, el corazón bajó, y la variabilidad subió.",
        "Una toalla fría en el cuello o en la cara, en un mal momento, es un freno rápido. Nunca hielo directo en la piel, y si tienes problemas del corazón, pregunta antes.",
        "[thoughtful] Tres: canta.",
        "El vago mueve los músculos de la garganta y de las cuerdas vocales. Y cantar te obliga a algo que casi nunca haces: soltar el aire muy, muy despacio.",
        "En 2013, en Suecia, midieron el corazón de jóvenes de 18 años cantando juntos. Con frases largas y lentas, la variabilidad subía, y sus corazones empezaban a acelerar y frenar casi al mismo tiempo.",
        "En la regadera, en el coche, con la radio. Tararear también cuenta.",
        "[thoughtful] Cuatro: muévete.",
        "Los corredores de fondo tienen el pulso en reposo muy bajo, a veces de 50 o menos. Parte de ese secreto es un freno vagal entrenado.",
        "No hace falta un maratón. Caminar rápido, nadar, bailar, casi todos los días. Eso, junto con dormir bien, es lo que más sube la variabilidad a largo plazo.",
        "[thoughtful] Y cinco: la gente.",
        "Recuerda que el vago sube noticias del cuerpo al cerebro. Una charla tranquila, una risa, la voz de alguien de confianza: tu cuerpo las lee como señal de que estás a salvo.",
        "En 2013, en la Universidad de Carolina del Norte, un estudio encontró que las personas que se sentían más conectadas con otros en su día a día mejoraban su tono vagal.",
        "[short pause] Y con un freno más ágil, les resultaba más fácil volver a conectar. Una espiral que sube. Todavía se discute, pero la idea es preciosa: cuidarte también es juntarte.",
    ]},
    {"id": "cierre", "frases": [
        "[serious] Así que la próxima vez que te toque hablar frente a todos, y alguien te diga respira hondo… hazle caso. Pero a tu manera.",
        "Poco aire para entrar. Mucho tiempo para salir.",
        "[short pause] Tu corazón va a bajar un poquito con cada exhalación. Porque ahí dentro, del cerebro a la panza, hay un cable que frena por ti miles de veces al día.",
        "[sighs] El freno siempre estuvo ahí. Solo había que saber dónde pisarlo.",
    ]},
]
