# -*- coding: utf-8 -*-
"""5 viajeros en el tiempo: de dónde salió realmente cada caso (documental de misterio, ~7 min, 16:9). Canal: Edsonxn.
Tablero de detective vivo (kit de videos/polybius/), voz Faraon (Chatterbox), Lyria, SIN subtítulos quemados.
Formato: cuenta atrás 5->1 de menos a más creíble, cada caso con «veredicto» y su ORIGEN rastreado (hipótesis del canal: título numerado,
canales/formula/edsonxn.md; referencia de fuera: Entre Misterios, cuenta atrás de viajeros en el tiempo).

Datos verificados (12-oct-2026; fuentes):
  - Andrew Carlssin: nació en el tabloide Weekly World News (artículo del 19-mar-2003; seguimiento del 29-abr-2003: «salió bajo fianza y desapareció»).
    Cifras del artículo: 800 dólares -> más de 350 millones en dos semanas. La SEC publicó en su sitio que las noticias parecían una broma y que no
    había presentado ninguna acción contra nadie así. Snopes lo ubica en el mismo tabloide (el de «Bat Boy»).
  - Rudolph Fentz: cuento «I'm Scared» de Jack Finney, Collier's, 15-sep-1951 (ficción: hombre de 1876 muerto por un taxi en Times Square en 1950,
    el policía halla su ficha de desaparecido de 1876). Ralph M. Holland (Akron, Ohio) lo reescribió como hecho en 1953 («A Voice from the Gallery»).
    El folclorista Chris Aubeck rastreó el origen (artículo «Desperately Seeking Rudolph», ~2002). Wikipedia «Rudolph Fentz», Snopes, hoaxes.org.
  - Mujer del estreno de «El circo» (Chaplin, 1928; imágenes extra del DVD, estreno en el Chinese Theatre de Hollywood): el cineasta irlandés George
    Clarke subió el fragmento el 19-oct-2010 diciendo que era un teléfono móvil; 1,4 millones de vistas en 9 días. Explicación de historiadores y
    archivistas (Philip Skroska, Washington University en San Luis; Christian Science Monitor; LiveScience): un audífono portátil de la época. NO confirmado.
  - John Titor: IRC «TimeTravel_0» 14-oct-2000; foros (Time Travel Institute) 2-nov-2000 a marzo de 2001; dijo ser soldado de 2036 enviado a 1975 por
    una IBM 5100 (la IBM 5100 salió en 1975). Predijo conflicto civil desde 2004, guerra civil hacia 2008 y guerra mundial en 2015: no ocurrieron.
    Salida: «líneas temporales» (muchos mundos). Autor no probado; el informe de 2009 (Hoax Hunter / Mike Lynch) apunta a Larry Haber y su hermano
    Richard; los Haber lo niegan. Wikipedia «John Titor». OJO: el artículo se contradice sobre los hermanos (otros nombres): no se nombran en el video.
  - Sir Victor Goddard (mariscal del aire): relato en su libro «Flight Towards Reality» (1975): tormenta, caída en espiral, salir de las nubes sobre el
    aeródromo de Drem (Escocia), abandonado desde 1919 y con uso ocasional 1933-1939, y verlo activo: aviones amarillos (uno monoplano que no reconoció)
    y mecánicos con overol azul (en la RAF eran de otro color). Fechas del propio Goddard: 1934 en una versión, 1935 en la mayoría. Drem se reabrió en 1939
    como sede de la 13.ª Escuela de Vuelo. Única fuente: su relato posterior; sin registros contemporáneos de la visión.
Pronunciación: voz española; los nombres ingleses van fonéticos en la narración (PRON) y con su ortografía real en pantalla.
"""

TITULO = "5 viajeros en el tiempo: de dónde salió realmente cada caso"
ARCHIVO = "viajeros_tiempo"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 96
GAP = 0.36
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)
MEZCLA = dict(musica=-22.0, sfx=-26.0)
SUBTITULOS = False          # el estilo dibuja su propio texto sincronizado; el .srt se genera igual

# token del guion -> texto que lee la voz española
PRON = {
    "{AC}": "Andru Carlsin",
    "{RF}": "Rúdolf Fents",
    "{JF}": "Yac Fini",
    "{TS}": "Taims Escuer",
    "{JT}": "Yon Táitor",
    "{VG}": "Víctor Gódard",
    "{DR}": "Drem",
    "{HW}": "Jolivud",
}
# lo que Whisper oye -> como está en el guion (minúsculas, sin tildes); lo usa qa.normaliza
ALIAS_QA = {
    "andrew carlson": "andru carlsin", "andrew carlison": "andru carlsin", "carlson": "carlsin", "carlison": "carlsin",
    "andrew carlssin": "andru carlsin", "andru carlsin": "andru carlsin", "andrew carlsin": "andru carlsin", "carlssin": "carlsin",
    "rudolph fentz": "rudolf fents", "rudolf fentz": "rudolf fents", "rudolf fents": "rudolf fents", "fentz": "fents", "rudolph": "rudolf",
    "jack finney": "yac fini", "yac fini": "yac fini", "jack finny": "yac fini", "yak fini": "yac fini", "finney": "fini",
    "times square": "taims escuer", "taims escuer": "taims escuer", "time square": "taims escuer",
    "john titor": "yon taitor", "yon taitor": "yon taitor", "john taitor": "yon taitor", "titor": "taitor", "taitor": "taitor",
    "victor goddard": "victor godard", "victor godard": "victor godard", "goddard": "godard", "godard": "godard", "godar": "godard",
    "hollywood": "jolivud", "jolivud": "jolivud", "drem": "drem", "dren": "drem",
}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "¿Y si alguien ya viajó en el tiempo, y lo tenemos grabado?",
        "En internet circulan decenas de historias de supuestos viajeros del futuro, con videos, documentos y hasta policías que los vieron.",
        "Elegí las cinco más famosas, y busqué de dónde salió cada una.",
        "Cuatro tienen un origen que se puede comprobar. La última descansa en la palabra de un solo hombre: un mariscal del aire británico.",
        "Vamos con la cuenta atrás. Del caso que menos aguanta, al que más.",
    ]},
    {"id": "carlssin", "frases": [
        "Número cinco. {AC}, el inversionista que sabía demasiado.",
        "En marzo de dos mil tres, medios de todo el mundo repitieron una noticia increíble.",
        "Un hombre había convertido ochocientos dólares en más de trescientos cincuenta millones en solo dos semanas, sin fallar una sola apuesta en la bolsa.",
        "Según la noticia, las autoridades lo arrestaron, y él confesó que venía del futuro.",
        "Pero la historia nació en un tabloide de supermercado, el mismo que antes había contado la vida de un niño murciélago.",
        "La comisión de valores de Estados Unidos, que supuestamente lo había detenido, aclaró que no existía ninguna acusación contra nadie así.",
        "Veredicto: una farsa de principio a fin.",
    ]},
    {"id": "fentz", "frases": [
        "Número cuatro. {RF}, el hombre que llegó tarde a su época.",
        "Nueva York, mil novecientos cincuenta. En plena {TS}, un taxi atropella a un hombre con ropa de otro siglo: patillas largas, sombrero de copa y botas abotonadas.",
        "En sus bolsillos, dicen, había dinero y papeles que ya nadie usaba, y la dirección de un hotel de mil ochocientos setenta y seis.",
        "Un policía investigó, y encontró el informe de un tal {RF}, desaparecido en mil ochocientos setenta y seis.",
        "Durante décadas, esta historia se repitió en libros y videos como un informe policial real. Pero ese informe no existe.",
        "El quince de septiembre de mil novecientos cincuenta y uno, una revista publicó un cuento de {JF}, llamado «Tengo miedo». Ahí está {RF}, con todo y taxi.",
        "En mil novecientos cincuenta y tres, un autor de Ohio lo reescribió como si hubiera pasado de verdad. Un folclorista siguió la pista hasta el cuento original.",
        "Veredicto: un personaje de ficción que se coló en las noticias.",
    ]},
    {"id": "chaplin", "frases": [
        "Número tres. La mujer del teléfono en una película de Chaplin.",
        "En mil novecientos veintiocho se estrenó en {HW} «El circo», y las cámaras grabaron a la gente que llegaba. Esas imágenes quedaron como extra en el disco de la película.",
        "En octubre de dos mil diez, un cineasta irlandés subió un fragmento a internet. Una mujer camina con la mano pegada a la oreja, y parece que habla sola.",
        "Dijo que era un teléfono celular. En nueve días, el video llegó a un millón cuatrocientas mil vistas.",
        "Historiadores y archivistas propusieron otra explicación: un audífono portátil de la época, de esos que se sostenían junto al oído.",
        "Nadie puede confirmarlo. Pero en mil novecientos veintiocho tampoco existía ninguna red a la que un celular pudiera conectarse.",
        "Veredicto: casi seguro, un audífono. Sin confirmar.",
    ]},
    {"id": "titor", "frases": [
        "Número dos. {JT}, el soldado del año dos mil treinta y seis.",
        "Entre noviembre de dos mil y marzo de dos mil uno, alguien con ese nombre escribió en foros de internet.",
        "Decía ser un soldado del año dos mil treinta y seis, enviado a mil novecientos setenta y cinco para recuperar una computadora: la I B M cinco mil cien.",
        "Esa computadora existió de verdad, y salió al mercado en mil novecientos setenta y cinco. Eso le dio un aire de credibilidad enorme.",
        "Pero sus predicciones fallaron: una guerra civil en Estados Unidos hacia dos mil ocho y una guerra mundial en dos mil quince. Ninguna ocurrió.",
        "Cuando se lo reclamaron, respondió que sus actos habían creado otra línea temporal. Una explicación que nunca se podrá comprobar.",
        "Nadie ha reconocido ser el autor. Un informe de dos mil nueve señaló a dos hermanos de Florida, y ellos lo niegan.",
        "Veredicto: casi seguro, un autor de internet que jugó con la ciencia ficción.",
    ]},
    {"id": "goddard", "frases": [
        "Número uno. El mariscal del aire que vio un aeródromo del futuro.",
        "Escocia, hacia mil novecientos treinta y cinco. El oficial {VG} vuela dentro de una tormenta tan violenta que, según su relato, su avión cae en espiral.",
        "Al salir de las nubes, ve debajo un aeródromo abandonado desde hacía años: {DR}.",
        "Pero ahora, cuenta, el lugar estaba lleno de vida. Aviones amarillos, uno de ellos un monoplano que no reconocía, y mecánicos con overoles azules.",
        "Y los mecánicos de la fuerza aérea británica no usaban azul.",
        "Años después, la base se reactivó y recibió una escuela de vuelo. Para él, ese era el futuro que había visto.",
        "Pero la única fuente es su propio relato, escrito en un libro de mil novecientos setenta y cinco, cuarenta años después. Y él mismo dio fechas distintas.",
        "Veredicto: ni probado ni desmentido. Y esa es la diferencia con los otros cuatro: aquí no hay un origen que rastrear, solo un hombre y su recuerdo.",
    ]},
    {"id": "patron", "frases": [
        "Si juntas los cinco casos, aparece un patrón.",
        "Una broma de tabloide. Un cuento de ciencia ficción. Un video ambiguo. Una cuenta anónima de foro. Y un recuerdo sin testigos.",
        "Ninguno dejó algo que puedas sostener en la mano: un objeto del futuro, un documento, una prueba que otra persona pueda revisar.",
        "Y todos crecieron del mismo modo: alguien copió la historia, la sacó de su contexto, y la repitió con más seguridad que la vez anterior.",
    ]},
    {"id": "cierre", "post": 9.0, "frases": [
        "Eso no demuestra que viajar en el tiempo sea imposible.",
        "Solo demuestra que, hasta hoy, ningún caso ha aguantado que le preguntes de dónde salió.",
        "Pero algo sí queda. Cada vez que oímos de alguien que volvió del futuro, una parte de nosotros quiere que sea cierto.",
        "Y tú, ¿qué prueba le pedirías a un viajero del tiempo para creerle?",
    ]},
]

# frases largas que hablan hasta el final (CER 0, transcripción completa): se acepta más cola
TAIL_MAX_POR_FRASE = {"fentz_1": 0.7, "goddard_1": 0.7, "chaplin_1": 0.5}

# aplica la pronunciación a todas las frases (la voz y el QA leen estos textos)
for _e in ESCENAS:
    _e["frases"] = [__import__("functools").reduce(lambda s, kv: s.replace(*kv), PRON.items(), f) for f in _e["frases"]]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)

LYRIA = dict(
    estilo=("Dark cinematic mystery documentary score in the style of a modern internet-mystery YouTube documentary: slow tense pads, "
            "deep pulsing sub-bass heartbeat, sparse piano, bowed strings, subtle ticking clock textures, occasional soft impacts. "
            "No drum kit, no big orchestral melody, no vocals."),
    escenas={
        "gancho": ("Hook: a sparse low drone, a slow ticking pulse building curiosity, a soft rising swell at the end.", 3),
        "carlssin": ("Light sly tension: pizzicato strings, a ticking rhythm, a knowing playful hint, sober.", 3),
        "fentz": ("Period mystery: soft piano, distant vintage textures, a steady low pulse, quiet unease, a reveal at the end.", 4),
        "chaplin": ("Curious and uncertain: sparse piano, high faint tones, a gentle questioning motif, ambiguous.", 3),
        "titor": ("Digital investigative: glitchy textures, pulsing bass, a ticking clock, small reveals, rising tension.", 4),
        "goddard": ("Haunting and epic: low strings, wind-like pads, a slow swelling drone, a sense of the uncanny, peak at the vision.", 5),
        "patron": ("Reflective analysis: pulsing bass, cold pads, restless piano, pieces clicking into place.", 4),
        "cierre": ("Ethereal pads and slow piano, the mystery remains, quiet and haunting, a faint tick at the very end, fades to silence.", 3),
    },
)
MUSICA = {
    "gancho": dict(sabor="tension", raiz=38),
    "carlssin": dict(sabor="tension", raiz=40),
    "fentz": dict(sabor="vacio", raiz=38),
    "chaplin": dict(sabor="vacio", raiz=41),
    "titor": dict(sabor="tension", raiz=36),
    "goddard": dict(sabor="tension", raiz=38),
    "patron": dict(sabor="espacio", raiz=40),
    "cierre": dict(sabor="vacio", raiz=38),
}
