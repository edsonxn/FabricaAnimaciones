# -*- coding: utf-8 -*-
"""Ramsés II, el faraón que se fabricó a sí mismo (~9 min, 16:9, Bitácora Perdida, línea «documental de personaje antiguo»).

Piloto del kit `nucleo/docu_antiguo.py` (docs/estilo_docu_antiguo.md): tomas de cine de Flow + grafismos sobre negro + artefactos reales.
Hilo: todo lo que creemos saber de Ramsés lo escribió él mismo; abre y cierra con el «pasaporte» de su momia (se cuenta, no consta).
Voz: Hugo M (ElevenLabs, biblioteca pública), elegida el 4-nov-2026 entre 5 graves (`prueba_voz/`; Ludovico y Salvatore ya son voces de Gaia).

Datos verificados (4-nov-2026) y fuentes:
  - Momia en París: llegó a Le Bourget el 26-sep-1976, recibida con honores militares; viajaba para frenar un hongo (Daedalea biennis) y fue
    esterilizada con rayos gamma en el Musée de l'Homme (Wikipedia «Ramesses II» § Mummy; Balout y Roubet, «La momie de Ramsès II», 1985).
  - PASAPORTE «profesión: rey (fallecido)»: SIN documento en ningún archivo (ni Museo Egipcio ni Musée de l'Homme); la imagen viral es un montaje
    de Heritage Daily; Toby Wilkinson lo llama mito urbano; USA Today/AFP lo dan como «reportado, sin documento» → en el guion: «se cuenta» y
    «nadie ha encontrado nunca ese documento» (History Revealed «Did Ramesses II really have a passport?»; BOOM Live; USA Today fact-check 2020).
  - Familia: Ramsés I fue visir y general de Horemheb, que murió sin hijos; dinastía XIX. Seti I hace corregente a Ramsés con ~14 años. Ramsés II
    sube al trono en 1279 a. C. con ~24 años; reina 66 años (1279-1213); muere con ~90; artritis, arteriosclerosis y abscesos dentales en la momia.
  - Kadesh (1274 a. C.): Muwatalli II; cuatro divisiones (Amón, Ra, Ptah, Set); dos shasu (beduinos) capturados dicen que los hititas están en
    Alepo (Boletín de Kadesh); emboscada a la división de Ra y luego al campamento de Amón; llegan los Ne'arin; resultado en tablas (Kadesh queda
    hitita). «La mayor batalla de carros conocida», ~5 000-6 000 carros en total (cifras estimadas → «se calcula»). Relieves en Abydos, Karnak,
    Luxor, Rameseo y Abu Simbel = 5 templos (Wikipedia «Battle of Kadesh»; Ancient Egypt Online; Biblical Archaeology Society).
  - Tratado (~1259 a. C.) con Hattusili III: no agresión, ayuda mutua, extradición de fugitivos; versión jeroglífica en Karnak y tablillas de
    arcilla hititas en los Museos Arqueológicos de Estambul. Réplica de cobre regalada por Turquía a la ONU en 1970 (Comunicado ONU HQ/246, 1970:
    «superb gift», U Thant; frente a la sala del Consejo de Seguridad). Boda con una princesa hitita (Maathorneferure, ~1245 a. C.).
  - Obras: Pi-Ramsés en el delta; Rameseo con coloso sentado de ~19 m; Abu Simbel con 4 colosos de ~20 m; el sol entra al santuario hacia el
    22-feb y el 22-oct; templo menor dedicado a Nefertari; usurpó estatuas de reyes anteriores reesculpiendo su nombre. Tumba de Nefertari QV66.
  - Hijos: listas de templos con ~50 hijos y ~50 hijas; le sucede Merenptah, su 13.er hijo (sobrevivió a 12 herederos).
    KV5: explorada a medias en 1825; su extensión la revela Kent Weeks en 1995; > 120 cámaras (más de 150 según Weeks, 2000), la mayor del
    Valle de los Reyes (Wikipedia «KV5»; Weeks, «The Lost Tomb», 1998).
  - Escondite DB320 en Deir el-Bahari: los sacerdotes reúnen momias reales (dinastía XXI); la familia Abd el-Rassul lo saquea desde ~1871; las
    autoridades lo vacían en julio de 1881 (Wikipedia «Royal Cache TT320»).
  - Belzoni saca de Tebas el Joven Memnón en 1816; llega al Museo Británico en 1818; Shelley publica «Ozymandias» en enero de 1818 (Ozymandias =
    versión griega de Usermaatra, nombre de trono de Ramsés; Diodoro de Sicilia). Traducción de los versos: dominio público.
  - Abu Simbel trasladado por la UNESCO entre 1964 y 1968: cortado en más de 1 000 bloques y elevado 65 m (UNESCO, «Nubia Campaign»).
  - Desfile Dorado de los Faraones, El Cairo, 3-abr-2021: 22 momias (18 reyes y 4 reinas) al Museo Nacional de la Civilización Egipcia.
"""

TITULO = "Ramsés II: el faraón que se fabricó a sí mismo"
ARCHIVO = "ramses_ii"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 90
GAP = 0.35
VOZ = dict(motor="elevenlabs", voice_id="HIkzxzvsigFIynXHHKhU",   # Hugo M - Deep & Mysterious (biblioteca pública)
           modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5)
MEZCLA = dict(musica=-22.0, sfx=-24.0)
SUBTITULOS = False
ALIAS_QA = {"muwatali": "muwatalli", "muatali": "muwatalli", "hatusili": "hattusili", "merneptah": "merenptah", "meremta": "merenptah",
            "oremheb": "horemheb", "vizir": "visir", "zed": "set", "rameceo": "rameseo", "osimandias": "ozymandias",
            "ocimandias": "ozymandias", "aswan": "asuan", "entebas": "en tebas", "titas": "hititas", "asentada": "sentada", "i": "primero"}
TAIL_MAX_POR_FRASE = {"kadesh_3": 1.1}      # acaba con fuerza en «Alepo» (CER 0 en 2 semillas, transcripción completa)
CER_MAX_POR_FRASE = {"tratado_4": 0.04}     # «arcilla hititas» con h muda: Whisper oye «arcilla y titas»
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.8, "frases": [
        "[serious] 26 de septiembre de 1976. Un avión aterriza en París con un pasajero que lleva más de tres mil años muerto.",
        "En la pista lo espera una guardia de honor del ejército francés, [short pause] como si llegara un jefe de Estado.",
        "Y se cuenta que traía pasaporte egipcio. [short pause] En la casilla de profesión decía: rey. [long pause] Fallecido.",
        "Nadie ha encontrado nunca ese documento. [short pause] Pero la historia se repite desde hace medio siglo, porque encaja exactamente con él.",
        "[thoughtful] ¿Quién era este hombre, para que tres milenios después de su muerte un país entero se cuadrara ante su momia?",
        "Se llamaba Ramsés. [short pause] Y casi todo lo que creemos saber de él, lo escribió él mismo.",
    ]},
    {"id": "nieto", "frases": [
        "Para entenderlo hay que empezar por algo que él prefería no contar: su familia no tenía sangre real.",
        "Su abuelo era un soldado de carrera, general y visir del faraón Horemheb.",
        "Horemheb murió sin hijos y le dejó el trono a aquel viejo militar. [short pause] Así nació la decimonovena dinastía.",
        "Ramsés Primero reinó apenas dos años. Su hijo, Seti, entendió el problema: una familia nueva necesita parecer eterna.",
        "Por eso, cuando su propio hijo tenía unos catorce años, Seti lo nombró corregente.",
        "El muchacho aprendió el oficio al lado de su padre: campañas en Libia y en Siria, obras por todo Egipto, y la lección más importante de todas.",
        "[serious] Un faraón no solo gobierna. [short pause] Un faraón se fabrica.",
        "En 1279 antes de Cristo, con unos 24 años, subió al trono Ramsés Segundo.",
    ]},
    {"id": "kadesh", "frases": [
        "Cinco años después llegó la prueba que define su leyenda: Kadesh, en la actual Siria.",
        "Enfrente estaba el imperio hitita, el otro gran poder de la época, al mando del rey Muwatalli Segundo.",
        "Ramsés marchaba hacia el norte con cuatro divisiones, cada una con el nombre de un dios: Amón, Ra, Ptah y Set.",
        "Cerca de Kadesh, sus hombres atraparon a dos nómadas shasu. [short pause] Le juraron al faraón que los hititas estaban lejos, en Alepo.",
        "[serious] Mentían. Eran espías. [short pause] Muwatalli lo esperaba escondido detrás de la ciudad.",
        "Ramsés acampó con la división de Amón casi sola, mientras los carros hititas caían sobre la división de Ra, que venía en camino.",
        "Fue, probablemente, la mayor batalla de carros que se conoce: se calcula que, entre los dos bandos, unos cinco mil.",
        "Según su propio relato, el faraón quedó rodeado y cargó él solo contra el enemigo. [short pause] Lo cierto es que resistió hasta que llegaron refuerzos.",
        "Al final, nadie ganó. Los hititas conservaron Kadesh, y Egipto volvió a casa sin la ciudad.",
        "[sighs] Pero Ramsés regresó con otra cosa: [short pause] una historia.",
        "La mandó tallar en los muros de cinco templos, de Abydos a Abu Simbel: el rey solo, gigantesco, aplastando a los hititas.",
        "Un empate convertido en victoria eterna. [short pause] Para muchos historiadores, una de las primeras grandes campañas de propaganda de la historia.",
    ]},
    {"id": "tratado", "frases": [
        "Lo que vino después es todavía más raro.",
        "Tras quince años de choques en la frontera, hacia 1259 antes de Cristo, los dos imperios firmaron la paz.",
        "Ramsés y el nuevo rey hitita, Hattusili Tercero, se prometieron no atacarse, ayudarse contra cualquier enemigo y devolverse a los fugitivos.",
        "Es el tratado de paz más antiguo que conservamos, y sobrevive por partida doble: en jeroglíficos, en los muros de Karnak…",
        "…y en tablillas de arcilla hititas que hoy se guardan en Estambul.",
        "[thoughtful] Una réplica en cobre, regalo de Turquía en 1970, está en la sede de la ONU, en Nueva York.",
        "Años después, el pacto se selló como se sellaba entonces: [short pause] Ramsés se casó con una princesa hitita.",
    ]},
    {"id": "constructor", "frases": [
        "Con la frontera en calma, Ramsés se dedicó a lo que mejor sabía hacer: [short pause] escribir su nombre en piedra.",
        "Levantó una capital nueva en el delta del Nilo: Pi-Ramsés, la casa de Ramsés.",
        "En Tebas construyó su templo funerario, el Rameseo, con una estatua suya sentada de casi veinte metros.",
        "Y en Nubia, en la frontera sur, mandó tallar una montaña entera: Abu Simbel.",
        "Cuatro colosos de veinte metros, todos con su cara, vigilan el río desde hace más de tres mil años.",
        "Dos veces al año, hacia el 22 de febrero y el 22 de octubre, el sol del amanecer atraviesa el templo y alumbra su estatua en el fondo del santuario.",
        "[deadpan] Pero Ramsés también tenía otra costumbre: borrar el nombre de faraones anteriores de sus estatuas y tallar el suyo encima.",
        "Por eso su nombre está por todo Egipto. [short pause] A veces, sobre obras que no eran suyas.",
    ]},
    {"id": "familia", "frases": [
        "Su gran esposa real fue Nefertari. Le dedicó el templo pequeño de Abu Simbel, y su tumba, en el Valle de las Reinas, es de las más bellas de Egipto.",
        "Pero no fue la única. Ramsés tuvo varias esposas reales y decenas de esposas menores.",
        "Y tuvo hijos. [short pause] Muchos. Las listas de sus templos nombran a unos cincuenta hijos y otras tantas hijas.",
        "En 1995, el egiptólogo Kent Weeks entró en una tumba del Valle de los Reyes que todos creían pequeña y sin interés: la KV5.",
        "Detrás de los escombros aparecieron pasillos y más pasillos: más de cien cámaras. [short pause] Era la tumba de sus hijos, la más grande de todo el valle.",
        "[sad] Porque ese fue el precio de su leyenda: vivió tanto, que enterró a doce herederos.",
        "Reinó sesenta y seis años. Murió hacia el 1213 antes de Cristo, con unos noventa años, artrítico y con los dientes destrozados.",
        "El trono pasó a Merenptah, su hijo número trece. [short pause] La mayoría de los egipcios no había conocido otro faraón.",
    ]},
    {"id": "escondite", "frases": [
        "Y entonces, su cuerpo empezó otro viaje.",
        "Los ladrones saquearon su tumba. Para salvarlas, los sacerdotes movieron en secreto varias momias reales, Ramsés entre ellas, a un escondite en los acantilados de Deir el-Bahari.",
        "Allí durmió casi tres mil años. Una familia de la zona lo descubrió y lo fue vendiendo pieza por pieza, hasta que en 1881 las autoridades lo vaciaron.",
    ]},
    {"id": "ozymandias", "frases": [
        "Mientras tanto, su piedra ya viajaba sola. En 1816, el aventurero Giovanni Belzoni arrastró desde Tebas un busto colosal suyo, rumbo a Londres.",
        "Su llegada inspiró al poeta inglés Percy Shelley a escribir, en 1818, su soneto más famoso: Ozymandias, el nombre que los griegos le daban a Ramsés.",
        "En el poema, en medio del desierto, solo queda una estatua rota con una inscripción.",
        "[serious] Mi nombre es Ozymandias, rey de reyes. [short pause] Mirad mis obras, poderosos, y desesperad.",
        "[thoughtful] Alrededor, nada. [short pause] Solo arena.",
        "Y el desierto casi gana. En los años sesenta, la presa de Asuán iba a inundar Abu Simbel para siempre.",
        "La UNESCO cortó el templo en más de mil bloques, y entre 1964 y 1968 lo volvió a armar sesenta y cinco metros más arriba.",
        "Diez años después, su momia se pudría por un hongo. Egipto la mandó a París, donde la esterilizaron con radiación y la devolvieron a casa.",
    ]},
    {"id": "cierre", "post": 1.4, "frases": [
        "En 2021, Ramsés cruzó El Cairo en un desfile dorado, junto a otros veintiún reyes y reinas, rumbo a su nuevo museo.",
        "Quería que nadie lo olvidara. Borró nombres, talló batallas que no ganó, convirtió montañas en retratos.",
        "[thoughtful] Y tres mil años después, seguimos tratándolo como a un rey. [short pause] Aunque su profesión diga: fallecido.",
        "Esto fue Bitácora Perdida. [short pause] Si quieres otra vida de antes de Cristo contada así, dinos en los comentarios a quién seguimos.",
    ]},
]

# SFX por ElevenLabs/biblioteca (nombres que usa SFX en escenas.py); sin repetir lo que el canal ya oyó
SFX_ELEVEN = {
    "jet_aterriza": dict(prompt="1970s turboprop military transport plane landing on a wet runway at night, engines winding down, distant", seg=4.0, variantes=1),
    "botas_firmes": dict(prompt="military honor guard snapping to attention, boots stamping in unison on wet asphalt, rifles slapped, night", seg=2.0, variantes=1),
    "neon_enciende": dict(prompt="old neon sign flickering on with electric buzz and crackle", seg=1.6, variantes=2),
    "golpe_grave": dict(prompt="deep cinematic low boom impact with long dark tail, documentary trailer hit", seg=2.5, variantes=3),
    "linterna_archivo": dict(prompt="flashlight click in a silent dusty archive room, faint paper rustle and distant hum", seg=3.0, variantes=1),
    "aire_tumba": dict(prompt="eerie hollow wind inside an ancient stone tomb, low dark drone", seg=4.0, variantes=1),
    "piedra_arrastre": dict(prompt="heavy stone block sliding and grinding slowly, deep rumble", seg=2.5, variantes=2),
    "viento_desierto": dict(prompt="desert wind at dusk with distant horses snorting and chariot wheels creaking", seg=4.0, variantes=1),
    "whoosh_suave": dict(prompt="soft low cinematic whoosh, smooth airy swipe", seg=1.2, variantes=3),
    "antorchas": dict(prompt="burning torches crackling in a large stone temple hall, soft echo", seg=3.5, variantes=2),
    # tramo 4 (Kadesh → cierre)
    "carros_carga": dict(prompt="ancient war chariots charging, many horses galloping, wooden wheels rattling, distant battle shouts, dust", seg=4.0, variantes=2),
    "tambor_guerra": dict(prompt="single deep ancient war drum hit with reverb in a desert, ominous", seg=2.0, variantes=2),
    "cincel_piedra": dict(prompt="metal chisel and wooden mallet striking stone, rhythmic carving, small chips falling", seg=3.0, variantes=2),
    "tablilla_arcilla": dict(prompt="clay tablet being set down on a stone table, soft scrape, dry and close", seg=1.5, variantes=1),
    "sello_cera": dict(prompt="heavy official seal stamped onto a document, firm thud", seg=1.2, variantes=1),
    "pluma_papel": dict(prompt="quill pen scratching on paper by candlelight, quiet room, rain on the window", seg=4.0, variantes=1),
    "agua_sube": dict(prompt="large body of water rising and rushing, deep flowing river, underwater rumble", seg=4.0, variantes=1),
    "cuerdas_tension": dict(prompt="thick ropes creaking under tension, heavy load pulled by many men, wood groaning", seg=3.0, variantes=1),
    "sierra_piedra": dict(prompt="industrial stone saw cutting through sandstone blocks, 1960s machinery, grinding", seg=3.0, variantes=1),
    "fuegos_artificiales": dict(prompt="fireworks bursting over a city at night with distant crowd cheering", seg=4.0, variantes=1),
    "vela_apaga": dict(prompt="candle flame blown out, soft puff and faint smoke hiss, silence", seg=1.5, variantes=2),
    "laboratorio_zumbido": dict(prompt="cold 1970s laboratory hum, fluorescent light buzz, machine powering up", seg=3.5, variantes=1),
}

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)

# Música con Lyria (nucleo/lyria.py): primero la biblioteca (`fab.py biblioteca sugerir ramses_ii`)
LYRIA = dict(
    estilo=("Dark cinematic documentary score about an ancient Egyptian pharaoh: low strings, deep drones, frame drums, oud and ney flute, "
            "distant choir, sparse piano. Slow, grave and mysterious like a true-crime history documentary; melodies kept low under a narrator."),
    escenas={
        "gancho": ("Cold open: low drone, a single frame drum hit, airport night ambience feeling, slow mysterious build.", 5),
        "nieto": ("Origins: soft oud and ney over low strings, a solemn dynastic theme slowly rising.", 6),
        "kadesh": ("War: pounding war drums, tense ostinato strings, chaos, then a hollow empty silence for the stalemate.", 6),
        "tratado": ("Peace: calm noble strings and a warm horn, diplomatic and stately.", 5),
        "constructor": ("Monuments: majestic slow brass and choir, the sun rising inside a temple, awe.", 6),
        "familia": ("Family and loss: intimate oud, mournful cello, a funeral lament for lost sons.", 6),
        "escondite": ("Hidden mummies: dark suspense, creeping low strings, secret cave.", 4),
        "ozymandias": ("Ozymandias: lonely desert wind, a solo voice, then a rising rescue theme for Abu Simbel.", 6),
        "cierre": ("Golden parade and epilogue: a grand processional theme fading into a single held note.", 5),
    },
    tramos=[
        (["gancho", "nieto"], "Begin from near silence with a low drone. End on a sustained grave tone that can cross-fade."),
        (["kadesh", "tratado"], "Start from the held tone, build to war drums, collapse into silence, resolve into a calm stately theme."),
        (["constructor", "familia"], "Start majestic and slow, end in a quiet mournful lament."),
        (["escondite", "ozymandias", "cierre"], "Start dark and secretive, open into lonely desert air, finish with a grand processional and a final held note."),
    ],
)
