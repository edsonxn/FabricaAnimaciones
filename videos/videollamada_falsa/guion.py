# -*- coding: utf-8 -*-
"""La videollamada donde nadie era real: el robo deepfake de Hong Kong (documental noir, ~6 min, 16:9). Canal: LogIA.
Estilo `noir` (nucleo/noir*.py, ejemplo videos/ia_noir/): cine negro en tinta y aguada, SOLO blanco y negro; el detective narra el caso.
Voz ElevenLabs «David» (0hh7H4ZVAtaGpm1VZyEN, elegida por el usuario) con eleven_v4 y ETIQUETAS DE ACTUACIÓN entre corchetes
(docs/voz.md § «Corchetes»): solo las lee el TTS; config.py las quita para Whisper, timeline y .srt. Sin subtítulos quemados.
Hechos (verificados el 7-oct-2026):
  - Policía de Hong Kong, rueda de prensa del vie 2-feb-2024 (CNN 4-feb-2024; BankInfoSecurity; SCMP): un empleado de finanzas de la
    oficina de Hong Kong de una multinacional recibió un mensaje que decía venir del director financiero (CFO), con sede en el Reino
    Unido, sobre una «transacción confidencial»; sospechó de phishing; lo invitaron a una videoconferencia con varios participantes
    que se veían y sonaban como colegas que reconocía: todos eran deepfakes («the only real person in the conference call»).
  - Hizo 15 transferencias a 5 cuentas bancarias de Hong Kong durante la semana siguiente: HK$200 millones (≈ US$25,6 millones).
    Lo descubrió al consultar con la oficina central. Denuncia: 29-ene-2024. Delito: obtención de propiedad mediante engaño.
  - Baron Chan (superintendente interino, ciberseguridad): «I believe the fraudster downloaded videos in advance and then used
    artificial intelligence to add fake voices to use in the video conference». Sin detenidos por este caso.
  - Mayo 2024 (FT, CNN, SCMP): la víctima era Arup, firma británica de ingeniería (~18.000 empleados; ingeniería estructural de la
    Ópera de Sídney). Arup: se usaron voces e imágenes falsas; ningún sistema interno fue comprometido; estabilidad financiera intacta.
  - Escena «senales» (The Standard / RTHK, 25-ago-2023; CNN 4-feb-2024): seis detenidos; con documentos de identidad robados a ocho
    personas hicieron hasta 90 solicitudes de préstamo y abrieron 54 cuentas; usaron un programa de cambio de cara para el
    reconocimiento facial (les funcionó una vez).
  - Reportes hasta 2025: investigación abierta, sin detenidos anunciados y dinero sin recuperar. En la narración: «hasta donde se sabe».
  - En pantalla (no en la voz): ARUP, HK$ 200 000 000, 15 → 5, 29 ENE 2024.
"""

TITULO = "La videollamada donde nadie era real"
ARCHIVO = "videollamada_falsa"
ESTILO_VISUAL = "noir"
DURACION = None
BPM = 84
SUBTITULOS = False
MEZCLA = dict(musica=-21.0, sfx=-24.0, fx=-17)      # fx = audio/fx.wav (SFX de ElevenLabs para el drama, fx_audio.py)
VOZ = dict(motor="elevenlabs", voice_id="0hh7H4ZVAtaGpm1VZyEN", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/videollamada_falsa/ref_david.mp3",
           tomas=1, stability=0.5)

ESCENAS = [
    {
        "id": "regla",
        "pre": 1.6,
        "frases": [
            "[thoughtful] En mi oficio aprendes una regla muy pronto. [short pause] No te fíes de lo que te cuentan. Fíate de lo que ves.",
            "[sighs] Esa regla murió una tarde de enero, en una oficina de Hong Kong.",
            "Un empleado entró a una videollamada con sus jefes. Vio sus caras. Escuchó sus voces. Obedeció sus órdenes.",
            "[whispers] Y en esa llamada, nadie era real. [short pause] Nadie, excepto él.",
        ],
    },
    {
        "id": "mensaje",
        "frases": [
            "[serious] Todo empezó con un mensaje. Venía, en apariencia, del director financiero de la empresa, desde el Reino Unido.",
            "Hablaba de una transacción confidencial. Urgente. De esas que no se comentan con nadie.",
            "[thoughtful] Y nuestro hombre hizo lo correcto: [short pause] sospechó. Pensó que era un engaño, de los de siempre.",
            "Pero quien escribió ese mensaje ya contaba con eso. [short pause] Así que le ofreció algo mejor que palabras.",
            "Lo invitó a una reunión. Con cámara.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "llamada",
        "frases": [
            "[curious] Imagínalo. Se conecta, y ahí están todos. El director financiero. Varios compañeros. Gente que reconoce.",
            "Las mismas caras. Las mismas voces. Los mismos gestos de siempre.",
            "[sighs] Y la duda se le fue del cuerpo. Porque uno puede desconfiar de un correo. [short pause] Pero no de sus propios ojos.",
            "En la reunión le dieron instrucciones. Él tomó nota. Y la llamada terminó.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "dinero",
        "frases": [
            "[serious] Durante la semana siguiente, hizo lo que le pidieron.",
            "Quince transferencias. [short pause] A cinco cuentas bancarias de Hong Kong.",
            "Doscientos millones de dólares de Hong Kong. [short pause] Más de veinticinco millones de dólares americanos.",
            "[thoughtful] Sin pistola. Sin pasamontañas. Sin forzar una sola cerradura. El botín salió por la puerta principal, con firma y con sello.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "descubre",
        "frases": [
            "Después, el empleado llamó a la oficina central para confirmar que todo había salido bien.",
            "[nervous] Al otro lado, nadie sabía de qué estaba hablando.",
            "No había transacción secreta. No había reunión. [short pause] El director financiero jamás estuvo en esa llamada.",
            "[sighs] El veintinueve de enero de dos mil veinticuatro, el caso llegó a la policía. Para entonces, el dinero ya no estaba.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "truco",
        "frases": [
            "[curious] ¿Cómo se fabrica una sala llena de fantasmas?",
            "La policía de Hong Kong tiene una hipótesis. Los estafadores descargaron videos públicos de esos directivos. Conferencias, entrevistas, presentaciones.",
            "[serious] Y con inteligencia artificial, les pusieron voces falsas que decían lo que ellos necesitaban.",
            "A eso lo llaman deepfake. [short pause] Una máscara hecha de datos, que cualquiera puede ponerse.",
            "[thoughtful] Antes, para suplantar a alguien, necesitabas a un actor. Hoy necesitas sus videos y una computadora.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "manual",
        "frases": [
            "[thoughtful] Pero la máscara era solo la mitad del truco. La otra mitad es más vieja que cualquier máquina.",
            "Primero, la autoridad. [short pause] Quien daba la orden era el jefe de los jefes.",
            "Segundo, el secreto. Una operación confidencial es una operación que no puedes consultar con nadie.",
            "Tercero, la prisa. [short pause] Cuando no hay tiempo para pensar, nadie piensa.",
            "[serious] Y cuarto, el grupo. Si todos en la sala parecen estar de acuerdo, ¿quién eres tú para decir que no?",
            "La inteligencia artificial puso las caras. [short pause] El resto lo puso un manual que los estafadores conocen desde hace un siglo.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "victima",
        "frases": [
            "Durante meses, nadie supo el nombre de la víctima. En mayo, la empresa lo confirmó.",
            "Era una firma británica de ingeniería con miles de empleados. [short pause] La misma que ayudó a levantar la Ópera de Sídney.",
            "[serious] Y aclaró algo que debería quitarte el sueño: nadie entró a sus sistemas. Ninguna computadora fue vulnerada.",
            "[whispers] No engañaron a las máquinas. [short pause] Engañaron a una persona.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "sinrostro",
        "frases": [
            "[sighs] Me gustaría decirte que atraparon a los culpables. [short pause] No puedo.",
            "Hasta donde se sabe, no hay detenidos por este golpe. No hay nombres. Y el dinero no ha vuelto.",
            "[thoughtful] Es el crimen perfecto de nuestra época: [short pause] ladrones sin rostro, que usaron el rostro de otros.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "senales",
        "frases": [
            "[serious] Y Hong Kong ya había visto las señales.",
            "Meses antes, la policía detuvo a seis personas por otra trama. Con documentos de identidad robados, pidieron noventa préstamos y abrieron cincuenta y cuatro cuentas bancarias.",
            "[curious] ¿Y cuando el banco les pedía mostrar la cara? [short pause] Usaban un programa para ponerse el rostro de otro.",
            "[thoughtful] La misma máscara sirve para las dos cosas: [short pause] para burlar a una máquina, y para burlar a un hombre.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "leccion",
        "frases": [
            "[serious] Y este caso no es una rareza. Es un aviso.",
            "Hoy basta con un poco de audio para clonar una voz, y con un poco de video para clonar una cara. Y todos hemos dejado de sobra en internet.",
            "Así que apunta la regla nueva, la que reemplaza a la vieja.",
            "[serious] Si alguien te pide dinero o secretos por una pantalla, [short pause] cuelga. Y llama tú, a un número que ya conocías.",
            "Acuerda una palabra clave con tu familia y con tu equipo. Una que no esté en ningún video.",
            "[thoughtful] Y desconfía de la prisa y del secreto. [short pause] Son las dos herramientas más viejas del oficio.",
        ],
        "pre": 0.7,
        "post": 1.1,
    },
    {
        "id": "cierre",
        "post": 3.5,
        "frases": [
            "[sighs] Yo me pasé la vida buscando mentirosos por la forma en que les temblaba la cara.",
            "Ahora la cara ya no tiembla. [short pause] Ahora la cara ni siquiera es suya.",
            "[thoughtful] Ver para creer. Eso decíamos. [short pause] Pues ya no alcanza.",
            "[whispers] Caso abierto.",
        ],
    },
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
MUSICA = {k["id"]: dict(sabor="tension", raiz=38) for k in ESCENAS}   # respaldo procedural (va Lyria)
# Ritmo dramático: pausas entre frases y aire entre escenas (las transiciones de tinta viven ahí)
GAP = 0.5
