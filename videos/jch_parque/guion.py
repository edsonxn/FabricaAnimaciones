# -*- coding: utf-8 -*-
"""REEL «Los jardines y el parque de Juchipila» para la página de Facebook «Que pasa en Juchipila» (E:\\PaginaFace).
Secuencia de imágenes de Flow (ilustración, 9:16) + efectos + voz Chatterbox (Dan) + música Lyria. 1 min.
Receta: docs/estilo_secuencia_fx.md y docs/estilo_secuencia_flow.md § «Formato vertical»; publicación: E:\\PaginaFace\\CLAUDE.md.

FUENTES de cada dato (consultadas el 8-oct-2026; todas deben ir a post.json → fuentes):
- Plan Municipal de Desarrollo 2021-2024 de Juchipila (http://www.juchipila.gob.mx/41/Juchipila-PMD-2021-2024.pdf), sección TURISMO:
  · Jardín Madero: «formó parte del primer panteón de Juchipila. Su nombre original era "Plazuela Segovia" en honor al fundador de
    la ciudad Fray Antonio de Segovia», frente al Templo San Francisco de Asís; rosales y palmeras.
  · Jardín Juárez: «plaza que data del año 1943», frente al Palacio Municipal, planta cuadrangular, bancas de hierro forjado,
    plantas de ornato y palmeras, «al centro un kiosco de planta octagonal».
  · Parque Municipal: «La primera piedra fue colocada el 18 de mayo de 1949 por el Presidente de la República el C. Lic. Miguel
    Alemán»; 2.7 hectáreas; áreas verdes, instalaciones deportivas, pista para correr, gimnasio al aire libre, juegos infantiles,
    comedores, sanitarios y teatro al aire libre.
  · Mercado 27 de Septiembre: primera piedra el 18 de mayo de 1949 por Miguel Alemán; inaugurado un año más tarde.
  · Fundación: frailes Antonio de Segovia y Miguel de Bolonia (misma sección histórica del plan, § Época Colonial).
- Documento de patrimonio de Zacatecas (https://labestad.reduaz.mx/web/turismo/patrimonew/ejecutivo/023.pdf): la villa se fundó
  «en el mes de enero, día 20, poco más o menos, del año de 1542» con los indígenas bajados del Mixtón por los dos frailes; el
  jardín está frente a la presidencia, con kiosco al centro; la feria regional de Juchipila se hace en el jardín a mediados de
  enero (San Sebastián y aniversario de la fundación).
- Nota local con ERROR de año: Imagen Zacatecas, 28-ene-2018 (https://imagenzac.com.mx/estado/en-el-olvido-el-parque-central-de-juchipila)
  dice «18 de mayo de 1929, por Miguel Alemán»; Alemán fue presidente de 1946 a 1952, así que vale 1949 (Plan Municipal).
- NO se afirma: fecha de inauguración del parque, quién hizo el kiosco, qué había antes de 1943 en el Jardín Juárez, el año
  de la torre/templo (la fecha «1627» no se pudo confirmar). Eso se pregunta a los vecinos en el cierre.
Whisper/voz: «Mixtón», «caxcanes» (alias abajo si los transcribe mal).
"""

TITULO = "Los jardines y el parque de Juchipila"
ARCHIVO = "jch_parque"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 240          # compás de 1 s: el motor redondea cada escena a compases; en un reel no sobra tiempo
GAP = 0.2
SUBTITULOS = False
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
ALIAS_QA = {"cascanes": "caxcanes", "cajcanes": "caxcanes", "cazcanes": "caxcanes", "mixton": "mixtón", "misto": "mixtón",
            "dos siete": "dos punto siete"}    # Whisper escribe «2.7»

SECUENCIA = dict(
    video_s=0,          # todo imágenes (pedido de Edson: secuencia de imágenes de Flow)
    clip_s=8,
    img_s=3.0,          # ritmo de reel: ~20 imágenes por minuto, cortes en pausas reales de la voz
    rapido_hasta=300,
    img_s_lento=3.0,
    fundido=0.2,
    ambiente=0.0,
    ambiente_por={},
    carpeta_descargas="flow-jch_parque",
)

# Ficha visual: se repite PALABRA POR PALABRA en cada prompt donde aparezca (triple anclaje). En inglés porque va tal cual a Flow.
FICHA = dict(
    estilo="Flat vector illustration for a vertical nine by sixteen animated history reel, warm illustrated storybook look, "
           "bold clean shapes, thin dark outlines, soft two-tone cel shading, muted warm palette of terracotta, ochre, sage green "
           "and deep teal, golden light, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette",
    personajes={
        "FRAY ANTONIO": "a humble Franciscan friar in his forties with a short dark beard and a tonsure, wearing a patched "
                        "grey-brown wool habit with a white rope belt and leather sandals",
        "FRAY MIGUEL": "a younger Franciscan friar, clean-shaven, round kind face, wearing the same grey-brown wool habit with a "
                       "white rope belt",
        "CAXCAN FAMILIES": "sixteenth-century Caxcan indigenous men, women and children in simple undyed cotton tunics and wraps, "
                           "dark hair, sandals, some carrying baskets and clay jars, tired but calm",
        "TOWNSPEOPLE": "Mexican townspeople of the nineteen forties: men in straw hats and white shirts, women in long cotton "
                       "dresses with rebozos, children in simple clothes",
        "THE OFFICIAL": "a well-dressed official of the late nineteen forties in a dark suit and a fedora hat, holding a trowel, "
                        "a generic figure with no resemblance to any real person",
    },
    objeto="THE KIOSK: an octagonal bandstand gazebo with eight slender iron columns, a low iron railing and a domed roof with a "
           "small finial, painted cream and sage green, at the center of a square plaza paved in stone, with cast-iron benches "
           "and palm trees around it; no clock, no modern lights, no signs",
    epoca="A small town in the Juchipila canyon of Zacatecas, Mexico, with dry mountains in the distance, mesquite and ash trees, "
          "adobe and stone walls and clay tile roofs; NOT any specific real building; no modern cars, no wires, no plastic",
    cierre="No text, no letters, no words, no numbers, no logos, no watermark, no modern objects.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {}

# Música: SIEMPRE Lyria (docs/estilo_secuencia_flow.md § Música). Desde la carpeta del video: python ..\..\nucleo\lyria_tramos.py
LYRIA = dict(
    estilo="Warm, nostalgic acoustic documentary score for a short story about a small Mexican town plaza: nylon-string guitar, "
           "soft marimba, gentle strings, a distant wooden flute and light brushed percussion. Tender and humble, never epic, "
           "never sad, always calm.",
    escenas={
        "gancho": ("Quiet and reflective opening: a lone nylon-string guitar and a very soft low string pad, curious and slightly "
                   "mysterious, almost empty.", 2),
        "fundacion": ("Tender and solemn: slow nylon guitar arpeggio with warm cello and a distant wooden flute, humble and "
                      "hopeful, gently building.", 3),
        "jardin": ("A calm turn toward a sunny small-town plaza: light marimba and acoustic guitar with a gentle waltz feel, "
                   "soft brushed percussion, nostalgic and warm.", 4),
        "parque": ("Proud and open: warm strings and guitar rising together, a gentle swell, the feeling of a whole town "
                   "gathering, widening.", 5),
        "cierre": ("Return to the opening guitar figure, now warm and resolved with soft marimba, then a slow fade-out to "
                   "silence.", 3),
    },
    tramos=[
        (["gancho", "fundacion", "jardin", "parque", "cierre"],
         "Begin from near silence. End with a natural slow fade-out to silence."),
    ],
)

ESCENAS = [
    {"id": "gancho", "pre": 0.4, "post": 0.15, "frases": [
        "Una parte del jardincito frente al templo de San Francisco fue el primer panteón de Juchipila.",
        "Hoy tiene rosales y palmeras.",
    ]},
    {"id": "fundacion", "pre": 0.15, "post": 0.15, "frases": [
        "Todo empezó en enero de mil quinientos cuarenta y dos.",
        "Dos frailes franciscanos, Antonio de Segovia y Miguel de Bolonia, bajaron de paz a los caxcanes que sobrevivieron al Mixtón.",
        "Con ellos se fundó la villa.",
        "Aquel jardincito se llamó Plazuela Segovia, en honor al fundador.",
    ]},
    {"id": "jardin", "pre": 0.15, "post": 0.15, "frases": [
        "Pasaron cuatro siglos.",
        "El Jardín Juárez, frente al Palacio Municipal, data de mil novecientos cuarenta y tres.",
        "Bancas de hierro forjado, palmeras, y al centro un kiosco de ocho lados.",
    ]},
    {"id": "parque", "pre": 0.15, "post": 0.15, "frases": [
        "Seis años después, el dieciocho de mayo de mil novecientos cuarenta y nueve, el presidente Miguel Alemán puso la primera piedra del Parque Municipal.",
        "Ese mismo día puso la del Mercado Veintisiete de Septiembre.",
        "Hoy son dos punto siete hectáreas con pista, juegos y teatro al aire libre.",
    ]},
    {"id": "cierre", "pre": 0.15, "post": 0.6, "frases": [
        "Cada enero, la feria regional llena el jardín.",
        "De cuándo se inauguró el parque, no hemos encontrado la fecha.",
        "Si tú la sabes, cuéntanosla en los comentarios.",
    ]},
]
