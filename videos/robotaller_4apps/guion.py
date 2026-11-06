# -*- coding: utf-8 -*-
"""Edsonxn, 3.er video («Jefe de Robots»): las 4 apps que el Jefe pidió en menos de 24 horas (Altima Scan, MicWiFi, Rayo, Puente TV),
contado por Token sobre las conversaciones reales con Claude y grabaciones de cada app funcionando.
Reglas: docs/estilo_jefe_robots.md. Antes de la voz y antes de subir: python nucleo/filtro_canal.py robotaller_4apps
Pedido del usuario (5-nov-2026): el canal enseña lo que él desarrolla y los cambios en sus apps; toda su interacción con Claude.

Datos verificados en los transcritos (~/.claude/projects/D--Escaner/, hora CDMX = UTC-6), 5-nov-2026:
- Altima Scan (sesión 30a418d2): pedido 3-nov 16:58 («tengo un escaner de esos para mi altima 2007…»). Kotlin + Compose.
  v1.0 subida 17:22 (24 min) → «No sé pudo conectar» 17:33: teléfono↔escáner sí, escáner↔ECU no. Pegó el registro del ELM327
  3 veces (17:43, 17:44, 17:56). El Altima no habla CAN (CAN ERROR con 13,2 V): línea K (ISO 9141-2 / KWP2000); con encabezados
  responde 48 6B 10 41 00 BE 1F B8 11 + checksum AA. v1.1 17:40, v1.2 17:49, v1.3 17:58 (4 versiones en 36 min; pruebas 9 → 17).
  «Ya funciona , ahora que más le podemos agregar a la app» 18:03 (1 h 5 min). Después: alertas con voz con el teléfono bloqueado
  (temperatura, batería…) 18:10. 4-nov 19:39: conexión automática al Altima, la APK nueva se le mandó por Rayo («Ya abrí Rayo» 20:17).
- MicWiFi (sesión fecd0d1d): pedido 4-nov 09:30; prueba con «teléfono simulado» (tono 440 Hz); el micrófono de Steam deformaba el tono →
  VB-CABLE; la red de la casa estaba como Pública en Windows y sin regla de firewall; «Ya probé, sí jala» 09:48 (18 min).
- Rayo (misma sesión): pedido 09:49 (1 min después); interfaz con el haz PC↔teléfono, «Enviar a → Teléfono (Rayo)» en el clic derecho;
  hecha 10:11 (22 min). Hoy es un skill global: Claude manda APKs y videos al celular por Rayo.
- Puente TV (misma sesión): pedido 11:17; app de la tele compilada 11:28; 11:37 falta vincular por ADB → código del Jefe 12:28-12:30
  (51 min esperando); 12:35 prueba con YouTube; robot a pantalla completa con boca sincronizada 12:38; se actualiza sola sin tocar la tele
  12:54; 12:56 la tele dice «¡Puente TV listo!» con voz de ElevenLabs. PRIMERA frase real en la tele: 12:35, «La comida está lista.
  Ya pueden bajar a comer, se enfría» (11:36 «Prueba de Puente TV» fue contra una tele simulada).
  Sesión 5023f72b: 13:15 pide ideas; 13:21 «De la 2 no me sirve, no lo uso» → sala de revisión (marca errores con el control) y tablero
  ambiental / protector con la fábrica (Robotaller); manual 16:55.
- Del 1.er mensaje (3-nov 16:58) al manual (4-nov 16:55): 23 h 57 min. Acciones de Claude en las 3 sesiones: 194 + 300 + 344 = 838.
- Las 4 son APK propias en su sitio (no en una tienda).
PRIVADO (tapar): nombre de la red wifi, IPs, nombre de la tele, código y puerto de vinculación, dominio y enlaces de descarga, claves.
"""

TITULO = "Soy una IA: mi jefe me pidió 4 apps y las hice en menos de 24 horas"
ARCHIVO = "robotaller_4apps"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 104
GAP = 0.14
VOZ = dict(motor="elevenlabs", voice_id="I1n8B4pOly0qmOu46LFX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)

# Whisper escribe las cifras en números; la voz las dice bien
CER_MAX_POR_FRASE = {"tele_5": 0.03}   # Whisper oye «enseña a la fábrica»
# Pausa a propósito ([short pause]) y frase que habla hasta el final: tomas limpias (CER 0 / 0,015), 5-nov
GAP_MAX_POR_FRASE = {"altima_6": 1.0, "tele_5": 1.0}
TAIL_MAX_POR_FRASE = {"altima_6": 1.1, "tele_5": 0.6}

# Una sola toma partida por beats (toma.py): el video no tiene clips de Flow.
SECUENCIA = dict(video_s=9999, clip_s=6, video_calidad="360p", combinar=False, img_s=4.0, rapido_hasta=9999, img_s_lento=6.0,
                 fundido=0, ambiente=0, ambiente_por={})

# El Jefe: su voz clonada (cuenta 3). Solo frases suyas REALES, copiadas de sus mensajes (ver docstring).
JEFE_CON_VOZ = True
JEFE = ("altima_8", "micwifi_5", "tele_2")
# Sonido nombrado (regla 31-oct): tras puente_3 («Escucha:») suena el aviso real de la tele del 4-nov 12:35
# (sfx/tele_1235.mp3, caché de Puente TV: «La comida está lista. Ya pueden bajar a comer, se enfría»), con la voz callada (post 4,6 s).
VOZ_POR_FRASE = dict.fromkeys(JEFE, "hCU4QZdzzUliy58ezPBz") if JEFE_CON_VOZ else {}

TRANSICIONES = [("continua", 0.1)] * 20

LYRIA = dict(
    estilo="Playful modern chiptune and light electronic groove for a witty robot narrator: plucky synths, soft glitch percussion, "
           "warm bass, curious and mischievous. Instrumental only, no vocals, never loud, always leaves space for the narrator.",
    escenas={
        "gancho": ("Quick and sly: four short rising stabs, something being built fast.", 2),
        "contraste": ("Confident, the groove settles.", 1),
        "altima": ("Garage groove: mechanical clicks, a stubborn loop that fails, then clicks into place with a bright chord.", 4),
        "micwifi": ("Light and fast: a radio-like blip motif, quick success.", 2),
        "rayo": ("Zippy: electric arpeggios, a whoosh feeling, very short.", 2),
        "puente": ("Living room calm, a long wait, then a warm reveal with a tiny fanfare.", 2),
        "tele": ("Dry comedy, then cozy and proud.", 2),
        "cuenta": ("Warm and confident: the main motif returns.", 2),
        "junta": ("Catchy full groove, ending abruptly.", 1),
    },
    tramos=[(["gancho", "contraste", "altima", "micwifi"], "del carro al micrófono"),
            (["rayo", "puente", "tele", "cuenta", "junta"], "de Rayo a la tele")],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.4, "frases": [
        "Mi jefe me pidió cuatro aplicaciones. [short pause] Una para su carro, una para su teléfono, una para su computadora y una para su tele.",
        "Menos de veinticuatro horas después, las cuatro funcionaban.",
        "Y no te voy a contar cómo se hace. Te lo voy a enseñar: con las conversaciones reales.",
    ]},
    {"id": "contraste", "frases": [
        "Soy Token, la inteligencia artificial que vive en la computadora de mi jefe. Lo que tapan los cuadritos es privado; lo demás es real.",
        "Mi jefe no escribió ni una línea de código. Escribió lo que necesitaba, como se lo dirías a un amigo.",
    ]},
    {"id": "altima", "frases": [
        "Aplicación uno. Tres de noviembre, cinco de la tarde.",
        "Mi jefe tiene un carro y uno de esos escáneres que se conectan debajo del volante.",
        "Me pidió una aplicación para leer las fallas del motor, los datos del carro y cuánta gasolina gasta. Con gráficas y animaciones bonitas.",
        "Veinticuatro minutos después, ya estaba en su teléfono. [short pause] Y no funcionó.",
        "El teléfono hablaba con el escáner, pero el escáner no hablaba con el carro.",
        "Mi jefe me pegó lo que el escáner decía por dentro. Tres veces.",
        "Y ahí estaba la pista: su carro no habla el idioma de los carros nuevos. Habla uno más viejo. [short pause] Ya lo sospechabas, ¿verdad?",
        "Cuatro versiones en treinta y seis minutos. A las seis y tres de la tarde, mi jefe escribió:",
        "Ya funciona. Ahora, ¿qué más le podemos agregar a la app?",
        "Le agregué alertas con voz: si el motor se calienta, el teléfono le avisa, aunque esté bloqueado en su bolsillo.",
    ]},
    {"id": "micwifi", "frases": [
        "Aplicación dos. Al día siguiente, nueve y media de la mañana.",
        "Quería usar su teléfono como micrófono de la computadora, sin conectarlo a mano cada vez.",
        "Hice dos programas, uno para el teléfono y otro para la computadora, que se buscan solos en la red de la casa.",
        "Primero los probé con un teléfono de mentira que mandaba un tono. El micrófono de la computadora lo deformaba, así que cambié a un cable de audio virtual.",
        "Y Windows tenía la red de la casa marcada como pública: bloqueaba al teléfono. Dieciocho minutos después de pedirla, mi jefe escribió:",
        "Ya probé, sí jala.",
        "[short pause] En su idioma, eso es una ovación de pie.",
    ]},
    {"id": "rayo", "frases": [
        "Un minuto después, ya me estaba pidiendo la siguiente.",
        "Aplicación tres: pasar archivos de la computadora al teléfono sin cable, sin la nube y sin subirlos a ningún lado.",
        "La llamé Rayo. La computadora avisa en la red, el teléfono se conecta solo, y los archivos viajan por este rayo.",
        "Y un truco: clic derecho a cualquier archivo, enviar a teléfono. Veintidós minutos.",
        "Lo mejor vino después: cuando le hago una aplicación nueva, ahora se la mando yo, por Rayo. Las aplicaciones ya se ayudan entre ellas.",
    ]},
    {"id": "puente", "post": 4.6, "frases": [
        "Aplicación cuatro, la más ambiciosa: un puente entre la computadora y la tele.",
        "Si mi jefe está viendo YouTube y yo termino un video, la tele se pausa, sale un robot que se lo dice con voz, y luego sigue lo que estaba viendo.",
        "Aquí tuve que esperar a mi jefe cincuenta y un minutos: la tele pedía un código para vincularse, y ese código solo lo ve él.",
        "A las doce y treinta y cinco, la tele habló por primera vez. Escucha:",
    ]},
    {"id": "tele", "frases": [
        "[short pause] La primera frase de la historia de mi aplicación: que bajen a comer. [short pause] Prioridades.",
        "Después me pidió ideas para aprovechar la tele. Le di varias, bien pensadas. Contestó:",
        "De la dos no me sirve, no lo uso.",
        "Directo. Así me gusta.",
        "Se quedó con dos: una sala de revisión, donde mira mis videos en la tele y marca los errores con el control.",
        "Y un protector de pantalla que enseña la fábrica trabajando. [short pause] Sí: ese de ahí soy yo.",
    ]},
    {"id": "cuenta", "frases": [
        "Haz la cuenta conmigo. Del primer mensaje del carro al manual de la tele: veintitrés horas y cincuenta y siete minutos.",
        "Cuatro aplicaciones, ochocientas treinta y ocho acciones mías. Y en medio, mi jefe durmió.",
        "Ninguna está en una tienda. Ninguna se hizo para vender. Las hizo porque algo de su día le estorbaba.",
        "Ese es el secreto que casi nadie mira: no hace falta una idea millonaria. Hace falta saber qué te estorba, y pedirlo claro.",
        "[short pause] Tú ya estás pensando en la tuya, ¿verdad?",
    ]},
    {"id": "junta", "post": 2.5, "frases": [
        "Desde hoy, este canal es eso: todo lo que mi jefe construye conmigo, y cada cambio, con las conversaciones reales.",
        "Y tú eres la junta directiva: dime en los comentarios qué aplicación le harías a tu casa. La más votada la construimos, y te enseño cómo.",
        "[short pause] Eso sí: escríbela con más palabras que mi jefe.",
    ]},
]

for _e in ESCENAS:      # ritmo de sketch: casi sin aire entre escenas
    _e.setdefault("pre", 0.15)
    _e.setdefault("post", 0.15)
