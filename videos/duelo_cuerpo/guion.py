# -*- coding: utf-8 -*-
"""Cuerpo en Neón, 5.º largo (22-oct-2026): «¿Qué Le Pasa a Tu CUERPO Cuando Muere Alguien Que Amas?».
Primer video de la fórmula NUEVA (canales/formula/cuerpo_en_neon.md § «Revisión 22-oct»): título-situación, ~5 min,
escalera de tiempo (minutos → 24 h → semanas → meses → año) + 3 cosas para hoy + frase citable + pregunta a los comentarios.
Referencia: «¿Qué pasa cuando MUERE tu mamá? | según la ciencia» (POV: Psicologia, 5,4 K subs) 585 K, 6:46. Sale antes de
Día de Muertos (cierre con la ofrenda). Estilo «línea blanca + neón» (docs/estilo_linea_neon.md; modelo de archivos:
videos/nervio_vago/, sin reciclar escenas).

Hechos (ficha antes de escribir; Whisper nunca es fuente; DOI verificados en Crossref el 22-oct-2026):
- Gündel, O'Connor, Littrell, Fort, Lane 2003, Am J Psychiatry 160(11):1946-1953, doi:10.1176/appi.ajp.160.11.1946
  (Universidad de Arizona): fMRI de mujeres en duelo (madre o hermana, < 1 año) mirando la foto de la persona + palabras
  de duelo: corteza cingulada (anterior y posterior), frontal medial, cerebelo… zonas que también participan en el dolor.
- Mostofsky, Maclure, Sherwood, Tofler, Muller, Mittleman 2012, Circulation 125(3):491-496,
  doi:10.1161/CIRCULATIONAHA.111.061770 (Harvard / Beth Israel Deaconess; Determinants of MI Onset Study, 1985 pacientes
  entrevistados): riesgo de infarto ×21,1 en las 24 h tras la muerte de una persona significativa; baja cada día pero sigue
  elevado la primera semana.
- Wittstein et al. 2005, N Engl J Med 352:539-548, doi:10.1056/NEJMoa043046 (Johns Hopkins): «aturdimiento» del corazón
  tras estrés emocional súbito; catecolaminas 2-3 veces las de un infarto; recuperación de la función en semanas.
  Takotsubo = vasija japonesa para atrapar pulpos (nombre de médicos japoneses, 1990): el ventrículo se infla en la punta.
- Templin et al. 2015, N Engl J Med 373:929-938, doi:10.1056/NEJMoa1406761 (registro internacional, 1750 pacientes):
  89,8 % mujeres, edad media 66; complicaciones graves en el hospital comparables a un síndrome coronario agudo.
- Khanfer, Ryan, Aldred, Pharaoh, Lord, Phillips 2011, Brain Behav Immun 25(6):1182-1186, doi:10.1016/j.bbi.2011.03.008
  (Universidad de Birmingham): adultos mayores en duelo reciente → neutrófilos con menor estallido oxidativo (matan peor
  a las bacterias) y cociente cortisol:DHEAS más alto que en los controles.
- O'Connor, Wellisch, Stanton, Eisenberger, Irwin, Lieberman 2008, NeuroImage 42(2):969-972,
  doi:10.1016/j.neuroimage.2008.04.256: en el duelo complicado, los recordatorios del ser querido activan el núcleo
  accumbens (recompensa, anhelo); en el duelo no complicado, no.
- Mary-Frances O'Connor (psicóloga, Universidad de Arizona), «The Grieving Brain» (2022): el cerebro mantiene un «mapa»
  donde el ser querido está «aquí, ahora, cerca»; el duelo es aprender que ya no. (Paráfrasis, sin cita textual.)
- Prigerson, Shear, Reynolds 2022, JAMA Psychiatry 79(4):277-278, doi:10.1001/jamapsychiatry.2021.4201: trastorno de
  duelo prolongado en el DSM-5-TR (marzo de 2022), ≥ 12 meses en adultos (CIE-11: 6 meses; vigente desde 2022).
No se dibuja a O'Connor (persona viva): su idea se ilustra con el mapa.
"""

TITULO = "¿Qué Le Pasa a Tu CUERPO Cuando Muere Alguien Que Amas?"
ARCHIVO = "duelo_cuerpo"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 72
GAP = 0.30

# Falsos positivos de Whisper: «Uno:/Dos:/Y tres:» -> «1./2./3.», «diez» -> «10»
CER_MAX_POR_FRASE = {"hoy_1": 0.08, "hoy_3": 0.12, "hoy_5": 0.09}
TAIL_MAX_POR_FRASE = {}
# Voz del canal: «Alejandro Durán — Warm, Deep» (biblioteca pública de ElevenLabs), la de todos los largos del canal
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

SECUENCIA = dict(
    clips_s=[10] * 9,         # 9 x 10 s = 63 puntos (había 1 001 el 22-oct): el gancho y los primeros minutos en video
    combinar=True,            # dos escenas por clip con transición dibujada
    video_calidad="360p",
    img_s=4.0,
    rapido_hasta=400,         # video de ~5 min: todo a una imagen cada ~4 s
    img_s_lento=4.5,
    fundido=0.25,
    ambiente=0.0,             # el sonido de Flow no encaja con el estilo: SFX propios
    ambiente_por={},
    carpeta_descargas="flow-duelo_cuerpo",
)

FICHA = dict(
    estilo="Minimalist white line-art illustration on a pure black background, like a fine engraving drawn with thin white "
           "chalk-like lines and delicate hatching, high detail, monochrome white on black, with ONE key element outlined "
           "in glowing bright yellow neon light with a soft golden glow; cinematic horizontal sixteen by nine composition, "
           "full-bleed scene that fills the entire frame edge to edge, no border, no frame",
    personajes={
        "la señora": "a simple stick-figure-like older woman with a bald round white head, no hair, dot eyes, small round "
                     "glasses and a small expressive mouth, thin white line body, wearing a long fringed shawl (rebozo) "
                     "over a simple dress, drawn in white outline",
        "el esposo": "seen only in a framed photograph or as a faint dotted white outline: a stick-figure-like older man with "
                     "a bald round white head, dot eyes, a white moustache and a hat",
    },
    objeto="her heart: a glowing yellow neon heart inside her chest, drawn as a simple anatomical heart",
    epoca="present day in Mexico: a small home kitchen with a rotary-style wall phone, a bedroom at night, a hospital "
          "corridor, a street market, a living room with a Day of the Dead altar (ofrenda) with candles, marigolds, "
          "papel picado and framed photos",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no color other than white lines and yellow neon.",
)

TRANSICIONES = [("continua", 0.1)] * 30

# Música con Lyria adaptada al guion (antes: `fab.py biblioteca sugerir duelo_cuerpo`). Solo descripción musical, en inglés.
LYRIA = dict(
    estilo="Tender, intimate science-explainer score for a film drawn in white chalk lines on black with glowing yellow "
           "neon: soft felt piano, warm cello, slow analog pads, a faint heartbeat-like low pulse. Instrumental only, no "
           "vocals, never loud, always leaves space for a deep narrator voice.",
    escenas={
        "gancho": ("A phone call with terrible news: a single low piano note, a held breath, then a slow aching chord.", 4),
        "minutos": ("The body's alarm: a quick heartbeat pulse under trembling strings, restrained, not dramatic.", 4),
        "horas": ("The broken heart is real: a serious low cello line, a pulse that falters and steadies.", 5),
        "semanas": ("Weeks of fog: hazy pads, a slow clock-like tick, tired and gentle.", 4),
        "meses": ("The brain's map still waiting for them: a music-box motif that repeats and slowly changes.", 5),
        "anio": ("Waves of grief and calm: piano phrases that rise and fall like a tide, slowly brightening.", 4),
        "hoy": ("Three small steps: steady warm piano, a hopeful pulse, quietly confident.", 4),
        "cierre": ("Day of the Dead altar with candles: tender guitar-like plucks over warm strings, a soft final chord.", 4),
    },
    tramos=[(["gancho", "minutos", "horas"], "Begin from near silence with a single low piano note. End softly on a calm sustained pad."),
            (["semanas", "meses"], "Begin softly on a calm sustained pad. End softly on a calm sustained pad."),
            (["anio", "hoy", "cierre"], "Begin softly on a calm sustained pad. End with a warm final chord fading to silence.")])

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "[serious] Suena el teléfono a una hora rara. Contestas. Y alguien te dice que una persona que amas ya no está.",
        "En ese momento, algo se te cae por dentro. El pecho se aprieta, las piernas se aflojan, y el aire no alcanza.",
        "[short pause] No es solo tristeza. Es tu cuerpo entero reaccionando.",
        "[thoughtful] Hoy vamos a ver, minuto a minuto y mes a mes, qué le pasa a tu cuerpo cuando muere alguien que amas. Por qué el corazón roto existe de verdad. Y qué puedes hacer desde hoy para cuidarte.",
    ]},
    {"id": "minutos", "frases": [
        "[thoughtful] Los primeros minutos.",
        "Para tu cerebro, perder a alguien es una amenaza. Y responde como ante un peligro: suelta adrenalina y cortisol, las hormonas de la alarma.",
        "El corazón se acelera, la presión sube, los músculos se tensan. Por eso tiemblas, o sientes frío, o no puedes ni llorar.",
        "[curious] En 2003, en la Universidad de Arizona, midieron el cerebro de personas en duelo mientras miraban la foto de quien habían perdido.",
        "Se encendieron, entre otras, zonas que también trabajan cuando algo nos duele en el cuerpo.",
        "Por eso, que te duela el pecho de tristeza no es una forma de hablar.",
    ]},
    {"id": "horas", "frases": [
        "[serious] Las primeras 24 horas.",
        "En 2012, investigadores de Harvard entrevistaron a casi 2000 personas que habían sufrido un infarto.",
        "Y encontraron que, en el día siguiente a la muerte de alguien cercano, el riesgo de infarto se multiplicaba por 21.",
        "Luego iba bajando, día con día, pero seguía alto toda la primera semana.",
        "[thoughtful] Y hay algo todavía más extraño: el síndrome del corazón roto.",
        "Ante una noticia terrible, la oleada de adrenalina puede ser tan fuerte que la punta del corazón se queda casi sin moverse, y se infla como un globo.",
        "En Japón lo llamaron takotsubo, porque el corazón toma la forma de una vasija que usan los pescadores para atrapar pulpos.",
        "Se siente igual que un infarto: dolor en el pecho y falta de aire. Y en 9 de cada 10 casos, le pasa a mujeres, sobre todo después de los 50.",
        "[short pause] En la mayoría, el corazón recupera su forma en unas semanas. Pero no es inofensivo: si te duele el pecho, es a urgencias, siempre.",
    ]},
    {"id": "semanas", "frases": [
        "[thoughtful] Las primeras semanas.",
        "La alarma no se apaga del todo. El cortisol sigue alto, y el sueño se rompe: te despiertas de madrugada, o no puedes levantarte.",
        "Se te olvidan las cosas. Dejas las llaves en el refri, no te acuerdas de lo que ibas a decir. Muchos le llaman la niebla del duelo.",
        "[curious] Y tus defensas bajan. En 2011, en Inglaterra, compararon a adultos mayores en duelo con otros de su misma edad.",
        "En los que acababan de perder a alguien, los glóbulos blancos que atacan a las bacterias funcionaban peor. Y la balanza de sus hormonas del estrés estaba cargada hacia el cortisol.",
        "Por eso no es raro enfermarse en los meses de un duelo. No es debilidad. Es un cuerpo cansado de estar en alerta.",
    ]},
    {"id": "meses", "frases": [
        "[thoughtful] Los primeros meses.",
        "Aquí pasa algo que parece de película. Volteas porque oyes una voz parecida en la calle. Agarras el teléfono para contarle algo. Pones dos platos en la mesa.",
        "[short pause] No te estás volviendo loco.",
        "La psicóloga Mary-Frances O'Connor, que estudia el cerebro en duelo, lo explica con un mapa.",
        "Tu cerebro tiene un mapa donde esa persona siempre está. Siempre contesta, siempre llega a cenar.",
        "Y ese mapa no se borra con una noticia. Se reescribe despacio, con cada día que vives sin ella.",
        "[serious] A veces, ese mapa se atora. En 2008, ese mismo grupo de Arizona vio que, en las personas a las que el duelo no les aflojaba, la foto de su ser querido encendía el circuito de la recompensa: el mismo de los antojos.",
        "El cerebro seguía buscando a esa persona, como quien busca algo que necesita para vivir.",
    ]},
    {"id": "anio", "frases": [
        "[thoughtful] El primer año.",
        "Para la mayoría, el dolor no desaparece, pero cambia. Llega en olas: un cumpleaños, una canción, una fecha.",
        "Y entre ola y ola, el cuerpo vuelve a dormir, a comer, y a reírse sin culpa.",
        "[serious] Pero si pasa un año y el dolor no afloja nada, y no te deja vivir, eso tiene nombre: duelo prolongado.",
        "Desde 2022 es un diagnóstico oficial, y tiene tratamiento. Pedir ayuda no es olvidar a quien se fue.",
    ]},
    {"id": "hoy", "frases": [
        "[thoughtful] Entonces, ¿qué puedes hacer desde hoy? Tres cosas sencillas.",
        "Uno: dale a tu cuerpo señales de que está a salvo. Come algo caliente, aunque sea poco. Duérmete a la misma hora. Sal a caminar diez minutos con luz de día.",
        "Tu alarma necesita pruebas de que el peligro ya pasó.",
        "Dos: no lo cargues solo. Habla de esa persona, en voz alta, con alguien que la conoció.",
        "Contar sus historias ayuda a tu cerebro a reescribir el mapa, sin borrarla.",
        "Y tres: escucha a tu pecho. Si te duele, te falta el aire, o el corazón late raro, no lo dejes para mañana. Ve a urgencias.",
    ]},
    {"id": "cierre", "frases": [
        "[thoughtful] En México, cada 1 y 2 de noviembre, ponemos una ofrenda. Su foto, su comida favorita, su música, las velas encendidas.",
        "[short pause] Y sin saberlo, hacemos justo eso: hablar de ellos, en compañía, y dejarles un lugar en el mapa.",
        "Porque el duelo duele tanto por una sola razón: es del tamaño de lo que amaste.",
        "[sighs] Si quieres, cuéntame en los comentarios a quién vas a recordar este año. Aquí también hay un lugar para ellos.",
    ]},
]
