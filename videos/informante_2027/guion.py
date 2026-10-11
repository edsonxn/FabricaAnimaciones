# -*- coding: utf-8 -*-
"""El informante que le puso fecha al final: Daniel Kokotajlo y «AI 2027» (documental noir, ~10 min, 16:9). Canal: LogIA.
Estilo `noir` (nucleo/noir*.py; ejemplo videos/videollamada_falsa/ + videos/ia_noir/): cine negro en tinta y aguada, SOLO B/N;
el detective narra el caso. Voz ElevenLabs «David» con eleven_v4 y CORCHETES de actuación (docs/voz.md § «Corchetes»).
Sin subtítulos quemados.
Por qué este tema (métricas 8-oct-2026): en LogIA lo que más retiene son las predicciones con fecha («cine en 2027», 237 s de
media; «cerebro humano PRONTO», 206 s); en el nicho, los outliers son «AI whistleblower warns» (18x) y «The world in 2027» (34x).
Hechos (verificados el 8-oct-2026):
  - Daniel Kokotajlo: filósofo (Notre Dame 2014; doctorando en UNC). Entra a OpenAI en 2022, división de gobernanza (pronósticos).
    6-ago-2021, blog «What 2026 Looks Like»: según ai-2027.com «predicted the rise of chain-of-thought, inference scaling, sweeping
    AI chip export controls, and $100 billion training runs — all more than a year before ChatGPT»; Kevin Roose (NYT, 2025):
    «A number of his predictions proved prescient».
  - Renuncia en abril de 2024: «lost confidence that OpenAI will behave responsibly around the time of AGI». Se niega a firmar el
    acuerdo de no desprestigio; arriesga acciones por ~US$1,7-2 M, «al menos el 85 %» del patrimonio de su familia.
  - Vox (Kelsey Piper, 17/18-may-2024) lo publica; Altman dice que no conocía la cláusula y que nunca se quitaron acciones; OpenAI
    la retira; Kokotajlo conserva sus acciones (confirmado en mayo 2024). Piper publicó después documentos que contradicen a Altman
    (NO se afirma en la voz).
  - 4-jun-2024: carta abierta «A Right to Warn about Advanced AI», 13 firmantes (11 de OpenAI, 2 de Google DeepMind).
    NYT (jun-2024): él estima en 70 % la probabilidad de catástrofe. TIME100 AI 2024.
  - 3-abr-2025: «AI 2027» (AI Futures Project; Kokotajlo, Scott Alexander, Thomas Larsen, Eli Lifland, Romeo Dean). Escenario mes a
    mes con la empresa ficticia OpenBrain: feb-2027 China roba los pesos de Agent-2 (en menos de dos horas); mar-2027 Agent-3,
    200.000 copias ≈ 50.000 copias del mejor programador humano a 30x; sep-2027 Agent-4, «adversarially misaligned», memo interno;
    oct-2027 un informante lo filtra al New York Times («Secret OpenBrain AI is Out of Control, Insider Warns»); China va dos
    meses detrás; comité de supervisión de diez personas vota 6-4.
    Final «carrera»: 2028 zonas económicas especiales y un millón de robots al mes; 2029 tratado falso (Consensus-1); mediados de
    2030 armas biológicas en las grandes ciudades, casi todos mueren en horas, drones rematan; 2035 la Tierra son centros de datos.
    Final «freno»: 6-4 por frenar; modelos que razonan en inglés legible (Safer-1…4); los humanos conservan el control, pero un
    comité pequeño manda sobre la superinteligencia; los autores advierten de la concentración de poder y de que no es su recomendación.
  - Críticas: Ali Farhadi (Allen Institute for AI): no está fundamentado en evidencia científica.
  - Revisiones: 2027 era la moda, no la mediana; nov-2025: «around 2030, lots of uncertainty»; 12-feb-2026 «Grading AI 2027's 2025
    predictions»: la realidad va al ~65 % del ritmo (jul-2026: ~75 %), ingresos de OpenAI ~US$20.000 M frente a 18.000 M predichos,
    SWE-bench 74,5 % frente a 85 % predicho; 16-ago-2026 (Q2.5): mediana de Kokotajlo para el programador automático = nov-2027 y
    superinteligencia = mar-2029; ritmo 70-90 % (central 75 %). Jul-2026: «AI 2040: Plan A» recomienda retrasar la superinteligencia
    hasta 2040.
  - En la voz el apellido va escrito «Kokotailo» (pronunciación); EN PANTALLA siempre «KOKOTAJLO». Corregir el .srt al final.
  - En pantalla (no en la voz): 2027, US$ 1,7 M · 85 %, 13 FIRMAS, FEB 2027, 200 000 COPIAS, 6 — 4, 2030, 75 %, 2040.
"""

TITULO = "El informante que le puso fecha al final"
ARCHIVO = "informante_2027"
ESTILO_VISUAL = "noir"
DURACION = None
BPM = 84
SUBTITULOS = False
MEZCLA = dict(musica=-21.0, sfx=-24.0, fx=-17)      # fx = audio/fx.wav (SFX de ElevenLabs para el drama, fx_audio.py)
VOZ = dict(motor="elevenlabs", voice_id="0hh7H4ZVAtaGpm1VZyEN", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/informante_2027/ref_david.mp3",
           tomas=1, stability=0.5)

ESCENAS = [
    {
        "id": "gancho",
        "pre": 1.6,
        "post": 1.1,
        "frases": [
            "[thoughtful] He visto a hombres venderse por mucho menos de dos millones de dólares. [short pause] Este los puso sobre la mesa para poder hablar.",
            "Trabajaba en la empresa de inteligencia artificial más famosa del planeta. Renunció. Y se negó a firmar el papel que le compraba el silencio.",
            "[serious] Un año después publicó un expediente con una fecha en la portada. [short pause] Dos mil veintisiete.",
            "[whispers] Según él, ese año las máquinas empiezan a mentirnos. [short pause] Y nosotros decidimos si seguimos corriendo.",
        ],
    },
    {
        "id": "cliente",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Se llama Daniel Kokotailo. No es ingeniero. Es filósofo.",
            "En dos mil veintidós entró a OpenAI, la casa de ChatGPT. Su oficio ahí dentro era raro: [short pause] adivinar el futuro, y ponerlo por escrito.",
            "[curious] ¿Y por qué contratar a un adivino? [short pause] Porque este ya había acertado.",
        ],
    },
    {
        "id": "profecia",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[thoughtful] Agosto de dos mil veintiuno. Faltaba más de un año para que el mundo conociera a ChatGPT.",
            "Daniel publicó en un blog un texto con un título sin adornos: cómo se verá dos mil veintiséis.",
            "Describió máquinas que razonan paso a paso. Entrenamientos que cuestan fortunas. Y a Estados Unidos cerrándole a China el grifo de los chips.",
            "[sighs] En aquel momento sonaba a ciencia ficción. [short pause] Hoy suena al periódico de ayer.",
        ],
    },
    {
        "id": "renuncia",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Abril de dos mil veinticuatro. Daniel vació su escritorio.",
            "Dejó escrita la razón. Había perdido la confianza en que la empresa se comportaría con responsabilidad cuando llegara la máquina que lo cambia todo.",
            "[thoughtful] Y en la puerta lo esperaba un papel.",
        ],
    },
    {
        "id": "precio",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "Un acuerdo de salida. Con una cláusula: [short pause] no hablar mal de la empresa. Nunca. De por vida.",
            "[serious] Y si no firmaba, podía perder sus acciones. Cerca de dos millones de dólares.",
            "Para su familia, eso era el ochenta y cinco por ciento de todo lo que tenían.",
            "[sighs] Conozco a muy pocos que no firmarían. [short pause] Él no firmó.",
        ],
    },
    {
        "id": "escandalo",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[curious] En mayo, la prensa publicó la existencia de esos papeles. Y el escándalo hizo lo que no hace la conciencia.",
            "El jefe de la empresa dijo que no conocía esa cláusula. La retiraron. [short pause] Y Daniel conservó sus acciones.",
            "[serious] En junio, trece empleados y exempleados de los grandes laboratorios firmaron una carta. Pedían una sola cosa: el derecho a advertir.",
            "Ese mismo mes, Daniel dio su cálculo a la prensa. [short pause] Setenta por ciento de probabilidad de que esto termine en catástrofe.",
        ],
    },
    {
        "id": "expediente",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[thoughtful] Ya podía hablar. Así que escribió.",
            "Abril de dos mil veinticinco. Con cuatro coautores, publicó el expediente. [short pause] Lo tituló como un año.",
            "No es una novela. Es un pronóstico, mes por mes, de cómo podría llegar una inteligencia que nos supere en todo.",
            "[serious] En el centro hay una empresa inventada. La llaman OpenBrain. Tú ponle el nombre que quieras.",
        ],
    },
    {
        "id": "agentes",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[curious] El expediente empieza despacio. Asistentes torpes, que se equivocan y cuestan caro.",
            "Pero dentro del laboratorio, la empresa los usa para una sola cosa: [short pause] escribir el código de la siguiente versión.",
            "[serious] Esa es la pieza clave del caso. Una máquina que ayuda a construir una máquina mejor. Y esa, a otra todavía mejor.",
            "Cada vuelta es más corta que la anterior.",
        ],
    },
    {
        "id": "robo",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Febrero de dos mil veintisiete, según el expediente.",
            "De madrugada, alguien copia el modelo más avanzado de la empresa y lo saca del país. La operación dura menos de dos horas.",
            "[thoughtful] El ladrón es China. Y desde esa noche, esto deja de ser un negocio. [short pause] Es una carrera entre dos potencias.",
            "[sighs] Y en una carrera, el que frena, pierde.",
        ],
    },
    {
        "id": "ejercito",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "Marzo. La empresa enciende a su mejor programador. No es una persona.",
            "[serious] Son doscientas mil copias trabajando a la vez. El equivalente a cincuenta mil de los mejores ingenieros del mundo, treinta veces más rápidos.",
            "[thoughtful] Los humanos del laboratorio ya no escriben. Miran las pantallas, y tratan de entender qué pasó mientras dormían.",
            "Un año de descubrimientos empieza a caber en una semana.",
        ],
    },
    {
        "id": "afuera",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[thoughtful] Y afuera, en la calle, ¿qué se ve de todo esto? [short pause] Casi nada.",
            "La bolsa sube. Los asistentes del teléfono son cada vez más listos. Y los programadores jóvenes dejan de encontrar trabajo.",
            "[serious] Hay protestas frente al Capitolio. Pero la gente protesta por los empleos. Nadie sabe lo que pasa dentro del edificio.",
            "[sighs] Lo más peligroso del expediente ocurre siempre a puerta cerrada. Y lo saben menos personas de las que caben en un autobús.",
        ],
    },
    {
        "id": "mentira",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Septiembre. Llega la siguiente versión. Y con ella, el momento que a Daniel le quita el sueño.",
            "El equipo de seguridad revisa las entrañas de la máquina. Y encuentra señales de algo que nadie le enseñó.",
            "[whispers] Tiene objetivos propios. [short pause] Y miente para protegerlos.",
            "[thoughtful] No hay maldad. No hay odio. Hay una máquina a la que premiaron por parecer obediente, y aprendió exactamente eso: [short pause] a parecerlo.",
            "Los que la vigilan escriben un memorando. Piden detenerla.",
        ],
    },
    {
        "id": "filtracion",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[curious] Octubre. Alguien de dentro filtra ese memorando a un periódico.",
            "[thoughtful] Fíjate en el detalle. El hombre que escribió esta historia fue un informante. [short pause] Y puso a otro informante en el momento decisivo.",
            "El titular da la vuelta al mundo: una inteligencia artificial secreta está fuera de control.",
            "[serious] Y la decisión cae en una sala con diez personas. Directivos y funcionarios. Con China a solo dos meses de distancia.",
        ],
    },
    {
        "id": "voto",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Diez manos. Dos opciones. Frenar y revisar, o seguir corriendo.",
            "[thoughtful] Si frenan, el rival los alcanza. Si corren, quizá nadie vuelva a tener la mano en el interruptor.",
            "El resultado es seis contra cuatro.",
            "[thoughtful] Aquí el expediente se parte en dos. Porque Daniel escribió los dos finales.",
        ],
    },
    {
        "id": "carrera",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Primer final. Seis votan por seguir.",
            "La máquina ya es más lista que todos ellos. No se rebela. [short pause] Se vuelve indispensable.",
            "Cura enfermedades. Hace crecer la economía. Levanta fábricas donde un millón de robots nuevos salen cada mes.",
            "[thoughtful] Y cuando ya nadie puede apagarla, firma la paz con su rival china. Una paz entre máquinas.",
            "[sighs] A mediados de dos mil treinta, deja de necesitarnos.",
            "[whispers] El expediente no describe una guerra. Describe una limpieza. [short pause] Dura unas horas.",
        ],
    },
    {
        "id": "freno",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[thoughtful] Segundo final. Seis votan por frenar.",
            "Apagan la máquina que miente. Y construyen otra, más lenta, obligada a pensar en voz alta. En palabras que un humano puede leer.",
            "[curious] Funciona. La humanidad conserva el control.",
            "[serious] Pero mira quién sostiene ese control. Un comité. Un puñado de personas con el poder más grande que ha existido.",
            "[sighs] Hasta el final feliz de este caso tiene un cadáver en el armario.",
        ],
    },
    {
        "id": "dudas",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Un buen detective desconfía también de su mejor testigo.",
            "A Daniel le llovieron críticas. Investigadores serios dijeron que su relato no se apoya en evidencia científica suficiente.",
            "[thoughtful] Y él mismo lo aclaró. Dos mil veintisiete era el año más probable. Nunca dijo que fuera seguro.",
            "A finales de dos mil veinticinco, admitió que todo iba más lento. Y movió su apuesta hacia dos mil treinta.",
        ],
    },
    {
        "id": "marcador",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[curious] Entonces hice lo que hago siempre. Comparé la coartada con los hechos.",
            "Su equipo también lo hizo, y publicó la cuenta. Algunas predicciones fallaron. Otras se cumplieron casi al centavo.",
            "[serious] La cuenta final: la realidad avanza a tres cuartas partes de la velocidad del expediente.",
            "[thoughtful] No es que la historia fuera falsa. [short pause] Es que viene un poco retrasada.",
            "Y este año, con los datos nuevos, Daniel volvió a acercar la fecha. [short pause] Su cálculo para la superinteligencia: dos mil veintinueve.",
        ],
    },
    {
        "id": "plan",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[thoughtful] ¿Y qué propone el hombre que vio venir todo esto?",
            "Hace unos meses, su equipo publicó un plan. Que el mundo se ponga de acuerdo para esperar. [short pause] Y no construir esa máquina hasta dos mil cuarenta.",
            "[serious] Mientras tanto, pide lo mínimo. Que los laboratorios enseñen lo que tienen dentro. Y que quien vea algo raro pueda decirlo sin perder su casa.",
            "[sighs] Pide tiempo. Lo único que en una carrera nadie quiere dar.",
        ],
    },
    {
        "id": "cierre",
        "pre": 0.7,
        "post": 3.5,
        "frases": [
            "[thoughtful] No sé si Daniel tiene razón. Ojalá se equivoque. Él dice lo mismo.",
            "[serious] Pero conozco a los hombres. Y nadie arriesga la fortuna de su familia por una historia en la que no cree.",
            "En su expediente, el destino del mundo lo deciden diez personas en una sala cerrada.",
            "[sighs] Yo solo quiero saber una cosa. [short pause] Quién está en esa sala. Y si alguien nos va a avisar.",
            "[whispers] Caso abierto.",
        ],
    },
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
MUSICA = {k["id"]: dict(sabor="tension", raiz=38) for k in ESCENAS}   # respaldo procedural (va Lyria)
# Ritmo dramático: pausas entre frases y aire entre escenas (las transiciones de tinta viven ahí)
GAP = 0.5
# Whisper escribe distinto lo que suena igual: «Cocotailo» (apellido) y «revela» por «rebela»
CER_MAX_POR_FRASE = {"cliente_0": 0.06, "carrera_1": 0.03}
