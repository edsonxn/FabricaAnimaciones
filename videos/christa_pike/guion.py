# -*- coding: utf-8 -*-
"""Christa Pike: la ejecución que no terminó (documental serio, ~8 min, 16:9). Canal: Edsonxn.
Estilo `documental` (calco de «Detrás del Enigma», ver CLAUDE.md «Estilo documental v3»), voz Faraon, SIN subtítulos quemados.
Hechos al 3-oct-2026: la historia sigue abierta (Pike hospitalizada, revisión independiente en curso). Revisar antes de publicar.

Datos verificados (texto completo en fuentes/*.txt; cada dato en al menos una fuente de agencia):
  - AP (3-oct-2026, abc7news.com / Al Jazeera / Fox 9 / Newsweek): el gobernador Bill Lee anunció el sábado 3-oct la renuncia de Frank Strada,
    comisionado del Departamento de Correcciones de Tennessee (cargo desde enero de 2023; antes, subdirector en Arizona). La ejecución
    fallida fue el miércoles 30-sep. Lee la llamó «deeply disturbing», ordenó una revisión independiente y suspendió las ejecuciones restantes
    del año. Strada dijo que el estado actuó «de acuerdo con el protocolo establecido». Abogados de Pike (Spivey, Gleason, Ferrell, Ihnen):
    «a systemic failure that goes far beyond any one person». Pike, en ventilador e inconsciente (escrito judicial del 2-oct); los abogados
    creen que las vías IV estaban mal colocadas y el pentobarbital fue a los tejidos; «apparently at no point did any member of the execution
    team realize that the IV lines were not correctly placed or that the veins had blown».
  - CBS News (sept-2025): la Corte Suprema de Tennessee fijó el 30-sep-2026 (Riverbend, Nashville). Colleen Slemmer (19) y Pike (18) eran
    alumnas de un programa de formación para jóvenes en Knoxville; la fiscalía sostuvo que Pike creyó que Slemmer quería quitarle a su novio;
    el novio (Tadaryl Shipp, 17) y una amiga (Shadolla Peterson) ayudaron; caja-cortadora y pentagrama durante «30 minutos o una hora» en una
    zona boscosa del campus de la UT; un jardinero declaró que el cuerpo estaba tan golpeado que lo confundió con un animal. Shipp: cadena
    perpetua; Peterson: libertad a prueba por declarar contra Pike. Pike, 20 años al ser sentenciada (1996), única mujer en el corredor de la
    muerte de Tennessee casi 30 años; demanda de 2022, acuerdo de sept-2024. Abogados: PTSD, bipolar, daño cerebral congénito, abuso sexual
    infantil, abandono y negligencia, sin presentarse en el juicio.
  - Wikipedia «Christa Pike» (con las fuentes de prensa): nació el 10-mar-1976 en Beckley (Virginia Occidental); centro juvenil de Carolina del
    Norte en 1991, liberada en marzo de 1993; asesinato el 12-ene-1995 en una planta de vapor abandonada, golpe con trozo de asfalto;
    rechazó un trato de cadena perpetua sin libertad condicional; sentencia 30-mar-1996 (electrocución); Corte Suprema de Tennessee confirmó
    en 1998; en 2001 y 2002 pidió abandonar apelaciones; 2004 condenada por intento de asesinato de otra presa (dijo que protegía a una
    compañera); 2012 plan de fuga frustrado (no la acusaron); Sexto Circuito 2019; certificación de fecha 30-sep-2025; TN Supreme Court
    rechazó el recurso el 23-sep-2026; clemencia negada 28-sep; SCOTUS rechazó 29-sep; el 30-sep el Sexto Circuito frenó la ejecución ~1 h
    antes y SCOTUS levantó la suspensión; cronología de la noche (testigos 6:41 pm CDT, persianas 7:26, queja de la vena 7:34, «piedra
    blanca» 7:41, persianas 7:46, segunda dosis, cortinas ~8:05-8:06, periodistas fuera 8:53, roncaba), ambulancia a Vanderbilt; brazos
    hinchados y quemados. Madre de Slemmer en sept-2026: «She did the crime. I think she should pay for it».
  - Newsweek (3-oct-2026): mayo de 2026, ejecución de Tony Carruthers detenida tras más de una hora sin lograr vía IV; Corinna Lain (U. de
    Richmond): caso sin precedentes en la era moderna de la inyección letal; Eric Berger (U. de Nebraska): Louisiana ex rel. Francis v.
    Resweber (1947) probablemente permite un segundo intento. Willie Francis (17 años) sobrevivió a la silla eléctrica el 3-may-1946 y fue
    ejecutado el 9-may-1947.
  - Discrepancias vistas y NO usadas: Al Jazeera dice que Pike tenía 18 al ser condenada (tenía 20); un resumen automático dio 1-oct como
    fecha del intento (fue 30-sep). Detalles de armas, cráneo y mutilaciones: omitidos a propósito (no aportan; respeto a la víctima).
Pronunciación: la voz es española; los nombres ingleses se escriben fonéticos en la narración (PRON) y en pantalla van con su ortografía real.
"""

TITULO = "Christa Pike: la ejecución que no terminó"
ARCHIVO = "christa_pike"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 96
GAP = 0.36
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)
MEZCLA = dict(musica=-22.0, sfx=-26.0)
SUBTITULOS = False          # el estilo dibuja su propio texto sincronizado; el .srt se genera igual

# --- pronunciación: token del guion -> texto que lee la voz española -----------------------------------------------------
PRON = {
    "{CP}": "Crista Paik",
    "{CR}": "Crista",
    "{CS}": "Colín Slémer",
    "{CO}": "Colín",
    "{TN}": "Tenesí",
    "{NA}": "Nashvil",
    "{KN}": "Nóxvil",
    "{BL}": "Bil Li",
    "{FS}": "Frank Estráda",
}
# lo que Whisper oye -> como está en el guion (minúsculas, sin tildes); lo usa qa.normaliza
ALIAS_QA = {
    "christa pike": "crista paik", "krista pike": "crista paik", "cristapaik": "crista paik", "crista pike": "crista paik",
    "christa": "crista", "krista": "crista", "cristal": "crista",
    "colleen": "colin", "colin": "colin", "colleen slemmer": "colin slemer", "slemmer": "slemer", "slemer": "slemer",
    "tennessee": "tenesi", "tenesi": "tenesi", "nashville": "nashvil", "knoxville": "noxvil", "noxville": "noxvil",
    "bill lee": "bil li", "billy": "bil", "frank strada": "frank estrada",
    "pike": "paik", "paique": "paik", "peik": "paik", "paick": "paik",
    "willie francis": "wili fransis", "willy francis": "wili fransis", "wily francis": "wili fransis", "willie frances": "wili fransis",
    "pentobarbital": "pentobarbital", "riverbend": "riverbend", "oscar smith": "oscar esmit", "oscar smit": "oscar esmit", "smith": "esmit",
}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "{NA}, {TN}. Miércoles, treinta de septiembre de dos mil veintiséis.",
        "Una mujer de cincuenta años está tendida en una camilla, con una vía puesta en el brazo.",
        "Detrás de una cortina, un grupo de testigos espera su muerte.",
        "Le inyectan una dosis. Pasan los minutos. Le inyectan otra.",
        "Y entonces sucede algo que nadie en esa sala sabe explicar.",
        "{CP} sigue respirando.",
    ]},
    {"id": "quien", "frases": [
        "Para entender cómo se llegó hasta ahí, hay que volver más de treinta años atrás.",
        "{CP} nació en mil novecientos setenta y seis, en Virginia Occidental.",
        "En mil novecientos noventa y uno la enviaron a un centro para menores en Carolina del Norte, donde pasó más de un año.",
        "En mil novecientos noventa y tres, con diecisiete años, se inscribió en un programa de capacitación para jóvenes en {KN}.",
    ]},
    {"id": "colleen", "frases": [
        "Allí conoció a {CS}.",
        "{CO} tenía diecinueve años y había nacido en Florida.",
        "Estudiaba computación, por consejo de su abuelo, que veía lo buena que era con las computadoras.",
    ]},
    {"id": "crimen", "frases": [
        "{CR} estaba convencida de que {CO} quería quitarle a su novio, un compañero de diecisiete años.",
        "Con él y con una amiga, planeó llevarla a un bosque, junto a una planta de vapor abandonada.",
        "El doce de enero de mil novecientos noventa y cinco, le dijeron que iban a hacer las paces.",
        "Allí, {CR} y su novio la golpearon y la torturaron durante entre media hora y una hora, según los registros del tribunal.",
        "{CO} suplicaba por su vida. Murió por un golpe en la cabeza con un trozo de asfalto.",
        "Un jardinero encontró el cuerpo. Estaba tan golpeado que, al principio, lo confundió con un animal.",
    ]},
    {"id": "juicio", "frases": [
        "La fiscalía le ofreció a {CR} un trato: declararse culpable a cambio de cadena perpetua. Ella lo rechazó.",
        "Su novio, que era menor, fue condenado a cadena perpetua. Su amiga declaró en su contra y recibió una condena sin cárcel.",
        "El treinta de marzo de mil novecientos noventa y seis, {CR}, de veinte años, fue condenada a morir en la silla eléctrica.",
        "Era una de las mujeres más jóvenes sentenciadas a muerte en el país.",
    ]},
    {"id": "corredor", "frases": [
        "Durante casi treinta años fue la única mujer en el corredor de la muerte de {TN}, casi siempre aislada del resto.",
        "En dos mil uno y en dos mil dos pidió que la ejecutaran y dejó de apelar. Después cambió de opinión.",
        "En dos mil cuatro la condenaron por intentar estrangular a otra presa, aunque ella aseguró que solo quería proteger a una compañera.",
        "En dos mil veintidós demandó al estado por recibir peores condiciones que los hombres, y en dos mil veinticuatro logró un acuerdo.",
    ]},
    {"id": "debate", "frases": [
        "Su caso divide a quienes miran la pena de muerte.",
        "Sus abogados sostienen que en el juicio nunca se presentó su historia: su edad, el abuso sexual que sufrió de niña, enfermedades mentales y un daño cerebral congénito.",
        "Amnistía Internacional y expertos de la ONU pidieron detener la ejecución.",
        "Pero del otro lado está la familia de {CO}. Su madre dijo en septiembre que {CR} tenía que pagar por lo que hizo.",
        "{CO} tampoco tuvo una segunda oportunidad.",
    ]},
    {"id": "camino", "frases": [
        "El treinta de septiembre de dos mil veinticinco, la Corte Suprema de {TN} fijó la fecha: un año exacto después.",
        "En mayo, el estado había detenido otra ejecución, después de más de una hora intentando, sin éxito, colocarle una vía al condenado.",
        "Los abogados de {CR} advirtieron que su historial médico podía complicar la inyección.",
        "El veintiocho de septiembre, el gobernador {BL} negó la clemencia. Al día siguiente, la Corte Suprema de Estados Unidos rechazó su último recurso.",
        "El día de la ejecución, un tribunal federal de apelaciones la detuvo, una hora antes. Horas después, la Corte Suprema levantó esa suspensión.",
    ]},
    {"id": "noche", "frases": [
        "Esa noche, en una prisión de máxima seguridad de {NA}, los testigos entraron a la sala a las seis y cuarenta y uno.",
        "A las siete y veintiséis se abrieron las persianas. {CR} estaba en la camilla, con la vía ya colocada en el brazo.",
        "Dijo que se iba de este mundo con amor, y que estaba en paz. Cantó una canción junto a su consejero espiritual.",
        "A las siete y treinta y cuatro se quejó: sentía que la vena del brazo estaba a punto de reventar.",
        "A las siete y cuarenta y uno, una piedra blanca apareció en una ventana de la pared. Se cree que era la señal de la primera dosis de pentobarbital.",
        "Las persianas se cerraron. Cuando se abrieron de nuevo, {CR} seguía moviéndose.",
        "El protocolo manda una segunda dosis si, a los cinco minutos, la persona sigue viva. Así se hizo.",
        "Hacia las ocho y cinco, las cortinas se cerraron otra vez. Los periodistas, al salir, dijeron que {CR} roncaba.",
        "Sus abogados pidieron atención médica inmediata. El protocolo no dice qué hacer si el condenado sigue vivo después de la segunda dosis.",
        "Una ambulancia se la llevó a un hospital universitario.",
    ]},
    {"id": "despues", "frases": [
        "Al día siguiente, sus abogados dijeron que estaba en estado crítico.",
        "Después, que seguía inconsciente, con un respirador, y que tenía ambos brazos hinchados, con ampollas y quemaduras.",
        "Creen que las vías estaban mal colocadas y que el fármaco fue al tejido, no a la sangre, sin que nadie en el equipo lo notara.",
        "El gobernador {BL} calificó lo ocurrido de profundamente perturbador. Ordenó una revisión independiente y suspendió las demás ejecuciones del año.",
        "Tres días después, el sábado tres de octubre, anunció la renuncia del director de prisiones del estado, {FS}.",
        "Él sostiene que su departamento actuó conforme al protocolo.",
        "Los abogados de {CR} respondieron: es una falla sistémica que va mucho más allá de una sola persona.",
        "La madre de {CO}, que viajó desde Florida para presenciar la ejecución, dijo que el estado le debe una disculpa.",
        "Dijo que, tras más de treinta años, lo único que quería era justicia.",
    ]},
    {"id": "historial", "frases": [
        "{TN} ya tenía un historial de problemas con sus ejecuciones.",
        "En abril de dos mil veintidós, el gobernador {BL} frenó a último momento la de Óscar Esmit, porque el estado no había seguido su propio protocolo.",
        "Una revisión independiente encontró fallas importantes, y las ejecuciones no se reanudaron hasta dos mil veinticinco.",
        "Desde entonces, el estado ha ejecutado a cuatro personas.",
        "La de {CR} fue la segunda ejecución fallida de este año.",
        "{FS} había llegado de Arizona en enero de dos mil veintitrés. A fines de dos mil veinticuatro, anunció que el estado usaría solo pentobarbital.",
    ]},
    {"id": "precedente", "frases": [
        "Una especialista en inyección letal dijo que no conoce un caso igual en la era moderna.",
        "Lo más parecido ocurrió en mil novecientos cuarenta y seis, en Luisiana.",
        "Un joven de diecisiete años, Wili Fransis, sobrevivió a la silla eléctrica.",
        "La Corte Suprema permitió un segundo intento, y lo ejecutaron un año después.",
        "Hoy, un profesor de derecho cree que ese precedente probablemente le permitiría a {TN} intentarlo otra vez.",
        "Los abogados de {CR} se preparan para impugnarlo.",
    ]},
    {"id": "cierre", "post": 11.0, "frases": [
        "Al cierre de este video, el tres de octubre de dos mil veintiséis, {CR} seguía hospitalizada, en estado crítico.",
        "Nadie ha explicado todavía qué falló esa noche.",
        "Y mientras el estado, los jueces y el país discuten qué hacer con {CP}, hay algo que ninguna revisión puede corregir.",
        "{CS} tenía diecinueve años.",
    ]},
]

# aplica la pronunciación a todas las frases (la voz y el QA leen estos textos)
for _e in ESCENAS:
    _e["frases"] = [__import__("functools").reduce(lambda s, kv: s.replace(*kv), PRON.items(), f) for f in _e["frases"]]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Somber cinematic true-crime documentary score in the style of a serious modern investigative documentary: slow low strings, "
            "sparse felt piano, a deep soft sub-bass pulse like a heartbeat, distant ambient textures, subtle ticking clock, occasional "
            "soft impacts. No drum kit, no big orchestral melody, no vocals, never triumphant, never sentimental."),
    escenas={
        "gancho": ("Hook: a sparse low drone, a single slow heartbeat pulse, thin high string harmonics building dread, a held swell and a sudden silence at the end.", 4),
        "quien": ("Quiet, bleak and human: solitary felt piano, soft low strings, cold air, a sense of a childhood lost.", 3),
        "colleen": ("Tender and sad: a gentle piano motif alone, warm sustained strings, a small hope that fades. Very soft.", 2),
        "crimen": ("Dark and tense but restrained: low pulsing bass, dissonant strings held long, no melody, dread without gore, a heavy hit at the end.", 5),
        "juicio": ("Cold procedural weight: steady low pulse, sparse piano notes like a ticking courtroom clock, sober and factual.", 4),
        "corredor": ("Isolation and passing years: slow ambient drone, distant metallic textures, a single piano note echoing, bleak and still.", 3),
        "debate": ("Two opposing weights: two alternating low string phrases, unresolved, questioning, moral gravity, building slightly.", 4),
        "camino": ("Countdown tension: a quickening quiet pulse, ticking, rising strings, inevitability building step by step.", 6),
        "noche": ("Peak of tension and dread, restrained: very slow heartbeat bass, long cold string clusters rising, silences, a final unresolved cluster. No release.", 8),
        "despues": ("Aftermath: shocked emptiness, soft low drone, sparse piano, slow unsettled resolve, quietly accusatory.", 5),
        "historial": ("Institutional unease: slow low strings, a ticking clock, sparse piano, cold and procedural, questions accumulating, a sense of a system under scrutiny.", 4),
        "precedente": ("Historical and thoughtful: old-world solemn strings, slow piano, a feeling of history repeating, grave.", 4),
        "cierre": ("Ethereal pads and a slow solitary piano, the question remains unanswered, quiet and haunting, final single note, fades to silence.", 3),
    },
)
MUSICA = {k["id"]: dict(sabor="tension", raiz=38) for k in ESCENAS}   # solo por si se corriera la música procedural (NO se usa: va Lyria)
