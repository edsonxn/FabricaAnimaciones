# -*- coding: utf-8 -*-
"""Guía de estudio 3 para SEXTO B de la primaria Benito Juárez de Juchipila, Zac.: CIENCIAS (lo que viene en su cuaderno).
Video PERSONAL (sin canal, no se sube), HORIZONTAL ~8 min. Pedido del usuario (9-nov-2026): «hay que hacer otro igual, mismo estilo,
pero de esta info» + 6 fotos del cuaderno (fuente/, enderezadas en propios/cuaderno/).
ESTILO: el MISMO de videos/amaya_estudio2/ (acuarela pintada a mano por código + «el profe Tilde» de kit_amaya.papa + voz NEUTRAL
Alberto Rodríguez). Pocos chistes y cortos (moco héroe, autogol), mnemotecnias nuevas, 4 «pausa y contesta» con silencio real.

Fotos: materia («La materia es todo lo que ocupa un lugar en el espacio y tiene masa»; «¿Cómo podemos saber que los gases son
materia? Porque cuando hicimos el experimento y bajamos… llegó a un punto donde ya no bajaba») · aire (78.08 % nitrógeno, 20.95 %
oxígeno, 0.93 % argón y 0.04 % otros gases en menor concentración) · atmosfera (Nuestros saberes 108-109: capa de gases que se
mantiene alrededor de un planeta por la gravedad; funciones: regula el clima, ayuda a la vida con el movimiento del agua y el aire
que respiran los seres vivos; gas = estado de agregación sin forma ni volumen definido; ¿por qué en un recipiente?) · jeringa
(punta tapada: empujar cuesta y regresa rápido, duele el dedo por la presión; jalar cuesta y regresa; «las partículas no se pueden
juntar más») · inmune1 (preguntas 1-7: defender de bacterias, hongos, virus y sustancias extrañas; 1.ª barrera piel, vellos, sudor,
lágrimas, mucosa; inmunidad innata; glóbulos blancos = leucocitos; granulocitos, monocitos y linfocitos; granulocitos: gránulos que
secretan enzimas) · inmune2 (13-19: linfocitos B → productoras de anticuerpos + células B de memoria; antígeno; anticuerpo; vacunas
= memoria, virus debilitados o partes; comer saludable, ejercicio, dormir bien; autoinmunes = ataca a las células buenas).
Faltan las preguntas 8-12 en las fotos: monocitos → macrófagos, linfocitos T y B (dato de libro de texto, nivel primaria).
"""

TITULO = "Sexto B: Ciencias para su examen (materia, gases, atmósfera y sistema inmunitario)"
ARCHIVO = "sextob_ciencias"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit acuarela.py; docs/estilo_acuarela_pincel.md)
DURACION = None
BPM = 200
GAP = 0.32
FPS = 24
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-24.0, sfx=-24.0, fx=-10.0)
SUBTITULOS = False
ALIAS_QA = {}
# Whisper escribe los porcentajes con cifras («78.08%»): el audio está bien
CER_MAX_POR_FRASE = {"aire_0": 0.14, "aire_1": 0.10, "aire_2": 0.12}
TAIL_MAX_POR_FRASE = {"jeringa_1": 1.2, "defensa_2": 1.2, "resp3_0": 1.2}   # medidas: se apagan a cero
MUSICA = {}
LYRIA = dict(
    estilo="Warm playful storybook score for a kid's science study guide: marimba, ukulele, glockenspiel, pizzicato; low in the mix.",
    escenas={
        "gancho": ("Playful hello.", 4), "materia": ("Curious.", 4), "gas": ("Airy, floating.", 4), "jeringa": ("Experiment.", 4),
        "preg1": ("Thinking.", 3), "resp1": ("Small win.", 3), "atmosfera": ("Wide, airy.", 4), "aire": ("Counting.", 4),
        "preg2": ("Thinking.", 3), "resp2": ("Small win.", 3), "defensa": ("Heroic castle.", 4), "leucocitos": ("Playful march.", 4),
        "linfocitos": ("Clever.", 4), "preg3": ("Thinking.", 3), "resp3": ("Small win.", 3), "vacunas": ("Sporty.", 4),
        "autoinmune": ("Light.", 4), "preg4": ("Thinking.", 3), "resp4": ("Win.", 3), "repaso": ("Quick recap.", 4),
        "cierre": ("Tender.", 3),
    },
    tramos=[(["gancho", "materia", "gas", "jeringa", "preg1", "resp1"], ""), (["atmosfera", "aire", "preg2", "resp2"], ""),
            (["defensa", "leucocitos", "linfocitos", "preg3", "resp3"], ""),
            (["vacunas", "autoinmune", "preg4", "resp4", "repaso", "cierre"], "")],
)
TRANSICIONES = [("continua", 0.3)] * 20   # plano secuencia: los cambios los dibuja escenas.py

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "¡Hola otra vez, sexto B de la Benito Juárez! [short pause] Soy el profe Tilde, y hoy traigo bata de científico, porque me llegaron las fotos de su cuaderno de Ciencias.",
        "Hoy toca: la materia y los gases, el experimento de la jeringa, la atmósfera, y el sistema inmunitario, el ejército que los defiende.",
        "Igual que la vez pasada: cuando les diga «pausa y contesta», pausen el video y contesten en voz alta. ¿Listos? Arrancamos.",
    ]},
    {"id": "materia", "frases": [
        "Primero: ¿qué es la materia? Como dice su cuaderno: la materia es todo lo que ocupa un lugar en el espacio y tiene masa.",
        "Una banca es materia. El agua es materia. Ustedes son materia. Truco: háganle dos preguntas. ¿Ocupa lugar? ¿Tiene masa? Si las dos son sí, es materia.",
        "¿Y el aire? No se ve, pero cuando inflan un globo, el aire ocupa ese lugar. Y un globo inflado pesa tantito más que uno desinflado. El aire también es materia.",
    ]},
    {"id": "gas", "frases": [
        "La materia puede estar en tres estados: sólido, líquido y gaseoso. El gas es un estado de agregación de la materia sin forma ni volumen definido.",
        "Una piedra tiene su propia forma. El agua toma la forma del vaso. Pero un gas se reparte por todo el espacio que encuentre.",
        "Por eso los gases necesitan estar guardados en un recipiente, como el tanque de gas de la casa. Si no, se escapan.",
    ]},
    {"id": "jeringa", "frases": [
        "Y para comprobar que los gases son materia, hicieron el experimento de la jeringa: tapan la punta con el dedo y empujan el émbolo.",
        "Al principio baja, pero cada vez cuesta más, hasta que llega un punto donde ya no baja. Y si lo sueltan, regresa de golpe. ¡Hasta duele el dedo por la presión!",
        "Y si tapan la punta y jalan el émbolo, cuesta mucho subirlo, y al soltarlo, se regresa rápido.",
        "¿Por qué pasa? Porque adentro hay aire. Sus partículas se aprietan, pero llega un punto en que ya no se pueden juntar más, y empujan de regreso.",
    ]},
    {"id": "preg1", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: ¿cómo podemos saber que los gases son materia?",
    ]},
    {"id": "resp1", "pre": 0.2, "frases": [
        "Porque ocupan un lugar: en la jeringa, el aire no dejó que el émbolo bajara hasta el fondo. Y si ocupa lugar y tiene masa, es materia. ¡Eso!",
    ]},
    {"id": "atmosfera", "frases": [
        "Ahora, la atmósfera. Es una capa de gases que rodea a un planeta, y se queda ahí, pegadita, por la fuerza de gravedad.",
        "Es como una cobija invisible alrededor de la Tierra.",
        "Y tiene funciones importantes: regula el clima, y ayuda a la vida en el planeta, con el movimiento del agua y con el aire que respiran los seres vivos.",
    ]},
    {"id": "aire", "frases": [
        "¿Y de qué está hecho ese aire? Apunten. Setenta y ocho punto cero ocho por ciento es nitrógeno.",
        "Veinte punto noventa y cinco por ciento es oxígeno, el que respiramos.",
        "Cero punto noventa y tres por ciento es argón. Y el cero punto cero cuatro por ciento son otros gases que hay en menor concentración, como el dióxido de carbono.",
        "Truco: imaginen que el aire es un salón de cien alumnos. Setenta y ocho son nitrógeno, veintiuno son oxígeno, y uno es argón. Los demás gases son una migajita.",
    ]},
    {"id": "preg2", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta, y ojo, que hay trampa: ¿cuál es el gas que más hay en el aire?",
    ]},
    {"id": "resp2", "pre": 0.2, "frases": [
        "¡El nitrógeno! Con setenta y ocho por ciento. Mucha gente dice oxígeno, pero el oxígeno es solo como el veintiuno. ¡No caigan!",
    ]},
    {"id": "defensa", "frases": [
        "Último tema, y el más largo: el sistema inmunitario, también llamado sistema inmunológico, o sistema de defensa.",
        "Es el sistema que defiende al cuerpo humano de invasores como bacterias, hongos y virus, y de sustancias extrañas que entran.",
        "Imaginen su cuerpo como un castillo. La primera barrera de defensa son las murallas: la piel, los vellos, el sudor, las lágrimas y la mucosa, o sea, el moco. Sí: el moco es un héroe.",
        "A esa primera barrera se le llama inmunidad innata. Innata quiere decir que naces con ella.",
    ]},
    {"id": "leucocitos", "frases": [
        "Y si un invasor se brinca la muralla, salen los soldados: los glóbulos blancos, que son células que forman parte del sistema inmunitario.",
        "Su otro nombre es leucocitos. Leuco quiere decir blanco.",
        "Hay tres tipos: granulocitos, monocitos y linfocitos. Truco: gatos, monos y leones.",
        "Los granulocitos tienen granitos: pequeñas partículas que sueltan enzimas para atacar a los invasores.",
        "Los monocitos crecen y se vuelven macrófagos, que se comen a los microbios. Macrófago quiere decir que come mucho.",
    ]},
    {"id": "linfocitos", "frases": [
        "Y los linfocitos son los más listos. Hay de dos tipos. Los linfocitos T se encargan de destruir las células infectadas por bacterias y virus.",
        "Y los linfocitos B se convierten en células que fabrican anticuerpos, y en células B de memoria, que recuerdan al antígeno que invadió el cuerpo.",
        "¿Y qué es un antígeno? Es lo que viene de fuera: toxinas, bacterias, virus, o pedacitos de ellos. Truco: antígeno rima con ajeno.",
        "Y el anticuerpo se pega al invasor, como una calcomanía que dice «¡este es!», para que el sistema inmunitario lo pueda destruir. Y fíjense: anticuerpo lleva la palabra cuerpo, porque lo fabrica su cuerpo.",
    ]},
    {"id": "preg3", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: ¿de qué otro nombre se les conoce a los glóbulos blancos? ¿Y cuáles son sus tres tipos?",
    ]},
    {"id": "resp3", "pre": 0.2, "frases": [
        "Leucocitos. Y sus tipos: granulocitos, monocitos y linfocitos. Gatos, monos y leones. ¡Muy bien!",
    ]},
    {"id": "vacunas", "frases": [
        "Ahora, las vacunas. Su función es activar el sistema inmunitario, para que desarrolle una memoria contra un virus o una bacteria.",
        "Están elaboradas con virus debilitados, o con partes de ellos. Es como un partido de práctica: el cuerpo entrena contra un rival flojito, y cuando llega el de verdad, ya se lo sabe.",
    ]},
    {"id": "autoinmune", "frases": [
        "¿Y qué son las enfermedades autoinmunes? Es cuando el sistema inmunitario se confunde, y ataca a las células buenas de su propio cuerpo.",
        "Auto quiere decir uno mismo, como en autobiografía. Es como meter un autogol.",
        "Y para mantener su sistema inmunitario en buen estado: coman saludable, hagan ejercicio, y duerman bien.",
    ]},
    {"id": "preg4", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: ¿de qué están elaboradas las vacunas?",
    ]},
    {"id": "resp4", "pre": 0.2, "frases": [
        "De virus debilitados, o de partes de ellos. Y sirven para que el cuerpo tenga memoria. ¡Eso!",
    ]},
    {"id": "repaso", "frases": [
        "Repaso exprés. Materia: ocupa lugar y tiene masa. El gas no tiene forma ni volumen definido; por eso va en un recipiente. Y la jeringa prueba que el aire ocupa lugar.",
        "Atmósfera: una capa de gases que se queda por la gravedad. Setenta y ocho de nitrógeno, casi veintiuno de oxígeno.",
        "Defensa: la primera barrera es la inmunidad innata. Leucocitos: gatos, monos y leones. Antígeno, ajeno. Anticuerpo, lo hace tu cuerpo. Vacuna, partido de práctica. Y autoinmune, autogol.",
    ]},
    {"id": "cierre", "post": 2.0, "frases": [
        "Sexto B: logro desbloqueado, ya tienen todo lo de su cuaderno de Ciencias. Repásenlo antes de dormir, que dormir bien también cuida su sistema inmunitario.",
        "Échenle ganas. Yo sé que pueden. [short pause] ¡Mucho éxito en su examen, sexto B!",
    ]},
]
