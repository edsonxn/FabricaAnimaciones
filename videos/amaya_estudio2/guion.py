# -*- coding: utf-8 -*-
"""CAMBIO 7-nov (el usuario, vía la sesión principal): YA NO es para Amaya ni con papá → dedicado a SEXTO B de la primaria Benito
Juárez de Juchipila, Zac.; voz NEUTRAL Alberto Rodríguez; presentadora = «la profe Tilde», maestra chibi en acuarela inventada
(kit_amaya.papa ahora la dibuja a ella; la cara del usuario no sale); solo 3 chistes cortos (lag, «mente sin cerebro», logro
desbloqueado) con vocabulario gamer que no caduca. Lo de abajo es el plan original.

Guía de estudio 2 para Amaya: ESPAÑOL (lo que viene en su cuaderno) — video PERSONAL (sin canal, no se sube), HORIZONTAL ~6 min.
ESTILO: el MISMO del video 1 (videos/amaya_independencia/): acuarela pintada a mano por código + papá real (kit_amaya.papa) + su voz
clonada (ElevenLabs cuenta 2).

Pedido del usuario (7-nov-2026): «ahí hay fotos de lo que debe estudiar, hagamos un segundo video con eso». Las 13 fotos
(fuente/IMG-20261107-WA0019..31, WhatsApp) son su cuaderno de ESPAÑOL, no de Historia:
  WA0019 La autobiografía (texto en el que una persona cuenta su propia vida; 1.ª persona «Yo nací en Juchipila»; hechos reales;
         sueños/metas; en orden) · WA0020 Los adverbios (modifican al verbo: cómo, cuándo...; ejemplos Santiago corre rápidamente,
         Juan llegó ayer, Natalia estudia mucho, los niños estudian aquí; tabla de 7 tipos: lugar, tiempo, modo, cantidad,
         afirmación, negación, duda) · WA0021/22/27 dividir en sílabas y encerrar la tónica (pirata, caracol, molécula, tocino,
         jamón, lámpara; rápido, manzana, música, reloj...) · WA0023 agudas (cajón, menú, motor...) · WA0024 graves: llevan tilde
         cuando NO terminan en n, s o vocal (Méndez, césped, fácil, póker; cama, cara) · WA0025 La carta informal (lugar y fecha,
         saludo + nombre, asunto (cuerpo), despedida, firma) · WA0026 clasificación (relámpago, cartón, túnel, ciudad, ejército,
         difícil, campeón, máquina, caballo, química, ventana, felicidad) · WA0028 reglas: agudas con tilde si terminan en n, s,
         vocal (camarón / calor) · WA0029 La anécdota (relato breve de un hecho curioso o divertido; qué ocurrió, dónde, cuándo,
         quiénes estaban, cómo me sentí) · WA0030 aguda/grave/esdrújula = última/penúltima/antepenúltima (es-CUE-la) ·
         WA0031 esdrújulas siempre llevan tilde (América, México, ejército, música, molécula, libélula, relámpago, teléfono,
         Jerónimo, Verónica).
ERROR EN EL CUADERNO (WA0026): «Túnel → esdrújula». Es GRAVE (tú-nel, 2 sílabas; tilde por terminar en l). El video lo usa como
«pregunta trampa» y se lo dice con cariño. Nada contradice al video 1 (Historia).

Métodos para 12 años: pregunta → respuesta corta → truco; pocos bloques; mnemotecnias nuevas («esdrújula es esdrújula», contar de
reversa, hermanos peleados, «siempre» como mamá con el suéter, preguntarle al verbo, «con mente pero sin cerebro», «La Sopa Aguada
Da Fuerza» = Lugar, Saludo, Asunto, Despedida, Firma); 4 «pausa y contesta» con silencio real (post 3,2 s + cuenta 3-2-1) y repaso.
Referencia rápida al video 1: «Hoy Me Gusta Ir». Forma de hablar del papá: «a ver», «o sea», «fíjate», «chido», «¿sale?».
"""

TITULO = "Sexto B: Español para su examen (sílabas, acentos, adverbios y textos)"
ARCHIVO = "amaya_estudio2"
ESTILO_VISUAL = "documental"      # escenas que dibujan el cuadro entero (kit acuarela.py; docs/estilo_acuarela_pincel.md)
DURACION = None
BPM = 200
GAP = 0.32
FPS = 24
# 7-nov (el usuario): voz NEUTRAL, no la suya → Alberto Rodríguez (latino neutro, la de Cronopapel)
VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-24.0, sfx=-24.0, fx=-10.0)
SUBTITULOS = False
ALIAS_QA = {}
# Whisper escribe «n, s, l» por «ene, ese, ele»: el audio está bien
CER_MAX_POR_FRASE = {"reglas_1": 0.10, "reglas_2": 0.05, "resp2_0": 0.09, "adverbios_2": 0.04}
# autobio_0 termina con énfasis pero se apaga a cero (medido): no está cortada
TAIL_MAX_POR_FRASE = {"autobio_0": 1.2, "silabas_1": 1.25, "adverbios_2": 1.25, "anecdota_1": 1.25, "resp4_0": 1.25, "repaso_1": 1.25}  # medidas: se apagan a cero
MUSICA = {}
LYRIA = dict(
    estilo="Warm playful storybook score for a kid's study guide: marimba, ukulele, glockenspiel, pizzicato; low in the mix.",
    escenas={
        "gancho": ("Playful hello.", 4), "silabas": ("Curious, clapping rhythm.", 4), "clasif": ("Bouncy.", 4),
        "preg1": ("Thinking.", 3), "resp1": ("Small win.", 3), "reglas": ("Light, clever.", 4), "preg2": ("Thinking.", 3),
        "resp2": ("Small win.", 3), "adverbios": ("Playful walking.", 4), "preg3": ("Thinking.", 3), "resp3": ("Small win.", 3),
        "autobio": ("Tender storytelling.", 4), "anecdota": ("Funny.", 4), "carta": ("Gentle, warm.", 4),
        "preg4": ("Thinking.", 3), "resp4": ("Win.", 3), "repaso": ("Quick recap.", 4), "cierre": ("Tender, loving.", 3),
    },
    tramos=[(["gancho", "silabas", "clasif", "preg1", "resp1"], ""), (["reglas", "preg2", "resp2", "adverbios", "preg3", "resp3"], ""),
            (["autobio", "anecdota", "carta"], ""), (["preg4", "resp4", "repaso", "cierre"], "")],
)
TRANSICIONES = [("continua", 0.3)] * 17   # plano secuencia: los cambios los dibuja escenas.py

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "¡Hola, sexto B de la Benito Juárez! [short pause] Soy el profe Tilde. Aquí tengo las fotos de su cuaderno de Español, y con eso vamos a repasar para el examen.",
        "Hoy toca: sílabas, acentos, adverbios, la autobiografía, la anécdota y la carta informal. Son varias cosas, pero cortitas, ¿va?",
        "Cuando les diga «pausa y contesta», pausen el video y contesten en voz alta. ¿Listos? Arrancamos.",
    ]},
    {"id": "silabas", "frases": [
        "Primero, las sílabas. Una sílaba es cada golpecito de voz. Aplaudan conmigo: es, cue, la. Tres aplausos, tres sílabas.",
        "Y siempre hay una que suena más fuerte: la sílaba tónica. En escuela es «cue». Como cuando gritan en el estadio: ¡campeón! La fuerza va en el «ón».",
        "Para encontrarla, las sílabas se cuentan desde el final: la última, la penúltima y la antepenúltima.",
    ]},
    {"id": "clasif", "frases": [
        "Y según dónde caiga la fuerza, la palabra tiene nombre. Si cae en la última, es aguda, como camarón o cartón.",
        "Si cae en la penúltima, es grave: árbol, caballo, ventana. Y fíjense: Juchipila también es grave.",
        "Y si cae en la antepenúltima, es esdrújula: máquina, relámpago, México.",
        "Truco: la palabra esdrújula es esdrújula. Es, drú, ju, la. Se pone de ejemplo solita.",
        "Y otro: cuenta de reversa, como camión que se echa para atrás. Última, aguda. Penúltima, grave. Antepenúltima, esdrújula.",
    ]},
    {"id": "preg1", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: la palabra música, ¿es aguda, grave o esdrújula?",
    ]},
    {"id": "resp1", "pre": 0.2, "frases": [
        "¡Esdrújula! Mú, si, ca: la fuerza va en la antepenúltima. Eso.",
    ]},
    {"id": "reglas", "frases": [
        "Ahora, ¿cuándo llevan tilde? La tilde es esa rayita que va arriba de la vocal.",
        "Las agudas llevan tilde cuando terminan en ene, ese o vocal. Camarón termina en ene: lleva tilde. Calor termina en erre: no lleva.",
        "Las graves hacen justo lo contrario: llevan tilde cuando no terminan en ene, ese o vocal. Árbol, fácil y césped, sí llevan. Cama y cara, no.",
        "Son como hermanos peleados: usan las mismas tres letras, pero cada uno hace lo opuesto.",
        "Y las esdrújulas llevan tilde siempre, siempre, siempre. Como el lag cuando ya vas a ganar. Teléfono, Verónica, Jerónimo: todas con tilde.",
    ]},
    {"id": "preg2", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta, y ojo, que hay trampa: túnel, ¿es aguda, grave o esdrújula?",
    ]},
    {"id": "resp2", "pre": 0.2, "frases": [
        "¡Grave! Tú, nel: solo tiene dos sílabas, y la fuerte es la penúltima. Lleva tilde porque termina en ele, no en ene, ese o vocal.",
        "Ojo: en el cuaderno quedó como esdrújula; corríjanlo. Truco: una esdrújula necesita mínimo tres sílabas.",
    ]},
    {"id": "adverbios", "frases": [
        "Siguiente tema: los adverbios. Son palabras que acompañan al verbo y nos dicen cómo, cuándo, dónde o cuánto se hace una acción.",
        "Como en su cuaderno: Santiago corre rápidamente. Juan llegó ayer. Natalia estudia mucho. Los niños estudian aquí.",
        "Truco: pregúntenle al verbo. ¿Dónde? Es de lugar. ¿Cuándo? De tiempo. ¿Cómo? De modo. ¿Cuánto? De cantidad.",
        "Y hay tres más que opinan: sí y también, de afirmación. No y nunca, de negación. Y quizá y probablemente, de duda.",
        "Dato chido: muchas palabras que terminan en mente son adverbios de modo, como rápidamente o cuidadosamente. Tienen mente, pero no cerebro.",
        "Otro ejemplo: el perro ladra mucho. Mucho es de cantidad. Y si digo «el perro ladra siempre», eso es de tiempo.",
    ]},
    {"id": "preg3", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: en la frase «Juan llegó... ayer», ¿cuál es el adverbio? ¿Y de qué tipo es?",
    ]},
    {"id": "resp3", "pre": 0.2, "frases": [
        "Ayer. Contesta la pregunta ¿cuándo?, así que es de tiempo. ¡Eso!",
    ]},
    {"id": "autobio", "frases": [
        "Ahora, dos textos que cuentan cosas de la vida. La autobiografía: auto es uno mismo, bio es vida, y grafía es escribir. O sea: escribir tu propia vida.",
        "Se escribe en primera persona, con «yo». Como en su cuaderno: «Yo nací en Juchipila». Cuenta hechos reales, en orden, y puede decir tus sueños y tus metas.",
    ]},
    {"id": "anecdota", "frases": [
        "Y la anécdota es un relato breve de algo curioso o divertido que pasó. La autobiografía es toda la película; la anécdota es un solo clip chistoso.",
        "Para escribirla, contesta cinco preguntas: ¿qué ocurrió?, ¿dónde?, ¿cuándo?, ¿quiénes estaban? y ¿cómo me sentí?",
        "Imagínense una: el domingo, en la cocina, mi primo quiso voltear un hot cake en el aire, y se quedó pegado en el techo. Estábamos todos, y nos moríamos de risa. Ahí están las cinco.",
    ]},
    {"id": "carta", "frases": [
        "Último tema: la carta informal. Es la que le escribes a alguien de confianza: un amigo, su abuela o su prima.",
        "Tiene cinco partes, de arriba a abajo. Primero, lugar y fecha. Luego, el saludo con el nombre: «Querido sexto B».",
        "Después, el asunto, que es el cuerpo: lo que le quieres contar. Luego, la despedida. Y hasta abajo, la firma de quien escribe.",
        "Truco para las cinco: La Sopa Aguada Da Fuerza. Lugar, Saludo, Asunto, Despedida y Firma.",
    ]},
    {"id": "preg4", "pre": 0.3, "post": 3.2, "frases": [
        "Pausa y contesta: ¿cuáles son las cinco partes de la carta informal?",
    ]},
    {"id": "resp4", "pre": 0.2, "frases": [
        "Lugar y fecha, saludo, asunto, despedida y firma. La Sopa Aguada Da Fuerza. ¡Muy bien!",
    ]},
    {"id": "repaso", "frases": [
        "Repaso exprés. Agudas, la fuerza en la última. Graves, en la penúltima. Esdrújulas, en la antepenúltima, y siempre con tilde.",
        "Adverbios: dónde, cuándo, cómo, cuánto, y sí, no, quizá. Autobiografía: toda tu vida, con «yo». Anécdota: un clip, con cinco preguntas. Y la carta: La Sopa Aguada Da Fuerza.",
    ]},
    {"id": "cierre", "post": 2.0, "frases": [
        "Sexto B: logro desbloqueado, ya tienen todo lo de su cuaderno. Y no se olviden: La Sopa Aguada Da Fuerza. Repásenlo antes de dormir.",
        "Échenle ganas. Yo sé que pueden. [short pause] ¡Mucho éxito en su examen, sexto B!",
    ]},
]
