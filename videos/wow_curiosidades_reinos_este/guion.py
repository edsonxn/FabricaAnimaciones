# -*- coding: utf-8 -*-
"""GUION · 62 curiosidades de los Reinos del Este (Crónicas de Warcraft, motor SECUENCIA YT, ~31 min).
Flujo y reglas: docs/estilo_secuencia_yt.md · estilo «gema» (cuenta regresiva, chistes secos).

Pedido del usuario (17-oct-2026): mínimo 60 curiosidades, ~30 min; empezar con las que casi nadie conoce, luego alternar
menos populares / populares, y dejar la menos conocida y más curiosa al final. Enfoque: Reinos del Este de CLASSIC (como
llegan a WoW Forever, 4-nov-2026); lo de Cataclysm o Wrath solo para contrastar.
Orden: 62-59 rarísimas · 58-7 alternando poco conocida (B) / popular (C) · 6-1 rarísimas, y la n.º 1 la más rara.

Verificado en la web el 17-oct-2026 (warcraft.wiki.gg, wowpedia, Wowhead, Warcraft Tavern, Icy Veins, Engadget):
- Malown: llaves de los buzones del mensajero de fuera; cada buzón suelta 3 carteros no-muertos de élite; conjunto «Postmaster».
- CLUCK!: /chicken 25-50+ veces, pienso especial del granjero Saldean (Páramos), dárselo desde su diálogo (si lo usas, te lo comes);
  huevo -> gallina de los Páramos. Horda solo desde el parche 3.1.0 (en Classic, solo Alianza).
- Aldea Piroleña: huargen de élite de noche (hostiles a ambos bandos); de día los guardias son de Ventormenta; grilletes.
- Gahz'ranka: cebo de Nat Pagle tras devolverle su cinta de medir (vasija en un campamento de ZG), 5 peces de aguas turbias
  junto al altar (~330 de pesca), una vez por instancia.
- Barov: Weldon (Alianza, Tierras de la Peste del Oeste) y Alexi (Horda, El Baluarte); 4 escrituras: Caer Darrow, Rémol,
  Molino Tarren, Costasur; cada uno manda a su bando a matar al hermano.
- Myzrael: elemental de tierra encerrada por gigantes de montaña creados por los titanes; se la invoca y se la vuelve a atar.
- Young Lovers: referencia a los Hatfield-McCoy (NO a Romeo y Julieta); poción de invisibilidad; casados en el granero de WoD.
- Stitches: Abercrombie la hace como «regalo» para el alcalde de Villa Oscura; el pregonero anuncia su avance (nivel: sin dato fiable).
- Lothos: sintonización desde nivel 55; se puede saltar por la ventana junto a él y caer dentro del Núcleo de Magma.
- Aeródromo de Forjaz: sin nombre en el mapa hasta 4.0.3a; las misiones del esfuerzo de guerra de Ahn'Qiraj aluden a él.
- Quel'Thalas: tierra sin terminar al norte (Kotaku); se dice como lo que es, especulación de jugadores.
- Valle de Alterac: partidas de horas y hasta días (Wowhead/Engadget); Korrak se fue en el 1.10.
- Bucaneros Velasangre: guerra con Bahía del Botín, matar a sus guardias; sombrero de almirante con loro; pierdes los goblins.
- OOX-09/HL: baliza rara en las Tierras del Interior; 3 robots (Interior, Feralas, Tanaris) -> pollo mecánico.
- Concurso de pesca: domingos de 14 a 16 h (servidor), 40 peces sabrosos moteados a Riggle Bassbait; caña de arcanita.
- Aurius (Stratholme): medallón de fe del cofre tras Malor; entra a ayudar contra el barón y muere; en el lore es hijo del
  barón (Aurius Rivendare, warcraft.wiki.gg).
- Ashbringer corrupta (Naxxramas, Cuatro Jinetes): los Escarlata se arrodillan; en la Catedral el espíritu de Alexandros
  Mograine habla a través de la hoja y confronta al comandante Escarlata (su hijo Renault). NO se cuenta cómo acaba (las
  fuentes discrepan). Quitado por dudoso: Chromie en Andorhal, nivel de Stitches, «se comparte barra de vida» de Los Siete.
Los Siete con Blancanieves es una lectura nuestra de los nombres (se dice como tal, no como dato oficial).

Sin patrocinio: el usuario pidió este video SIN Overgear (17-oct-2026).
"""

TITULO = "62 curiosidades de los Reinos del Este que casi nadie conoce"
ARCHIVO = "wow_curiosidades_reinos_este"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")

# Grafía que lee el TTS (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md; con traducción oficial, se usa esa)
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "Classic": "Clásic", "Azeroth": "Azeróth",
    "The Burning Crusade": "De Bérnin Kruséid", "Burning Crusade": "Bérnin Kruséid", "Cataclysm": "Cataclísm", "Warcraft tres": "uárcraft tres", "Warlords of Draenor": "Uórlords of Dréinor", "Hearthstone": "Járzston",
    "Arthas": "Ársas", "Alterac": "Álterac", "Zul'Gurub": "Zul Gurúb", "Stratholme": "Strázolm", "Gurubashi": "Gurubáshi", "Thrall": "Zrál", "Orgrimmar": "Orgrímar",
    # personajes
    "Malown": "Málaun", "Gahz'ranka": "Gás ránka", "Nat Pagle": "Nat Péiguel", "Weldon": "Uéldon", "Barov": "Bárov",
    "Myzrael": "Mízrael", "Hogger": "Jóguer", "Maybell Maclure": "Méibel Maklúr", "Tommy Joe Stonefield": "Tómi Yóu Stónfild",
    "Stonefield": "Stónfild", "Maclure": "Maklúr", "Hatfield": "Játfild", "McCoy": "Makói", "Thoradin": "Tóradin",
    "Leeroy Jenkins": "Líroi Yénkins", "Leeroy": "Líroi", "Pals for Life": "Pals for Láif", "Edwin VanCleef": "Édguin Van Clíf",
    "VanCleef": "Van Clíf", "Norgannon": "Nórganon", "Thaurissan": "Táurisan", "Anger'rel": "Ánguer rel",
    "Seeth'rel": "Síz rel", "Dope'rel": "Dóup rel", "Gloom'rel": "Glúm rel", "Vile'rel": "Váil rel", "Hate'rel": "Jéit rel",
    "Doom'rel": "Dúm rel", "Executus": "Ekzékutus", "too soon": "tú sún", "you no take candle": "yu nou téik kándel", "PvP": "pi vi pi", "Lothos Riftwaker": "Lózos Ríftueiker",
    "Lothos": "Lózos", "Rivendare": "Ríven der", "Aurius": "Áurius", "Alexandros": "Alexándros", "Renault": "Renó", "Ysida Harmon": "Isída Jármon", "Stitches": "Stíchis",
    "Abercrombie": "Ábercrombi", "Hemet Nesingwary": "Jémet Nésinguari", "Nesingwary": "Nésinguari", "Hemingway": "Jéminguei",
    "Bangalash": "Bángalash", "Loksey": "Lóksi", "release the hounds": "rilís de jáunds", "Ernest": "Érnest", "Simpson": "Símpson", "Burns": "Berns", "Mograine": "Mográin",
    "Monty": "Mónti", "OOX-09/HL": "o o equis cero nueve", "Short John Mithril": "Short Yon Mízril", "Kel'Thuzad": "Kel Zúzad",
    "Terenas": "Terénas", "Medivh": "Médiv", "Riggle Bassbait": "Rígel Básbeit", "Ivus": "Ívus", "Lokholar": "Lókjolar",
    "Plugger Spazzring": "Plóguer Spásring", "Grim Guzzler": "Grim Gásler", "Tirion Fordring": "Tírion Fórdring",
    "Tirion": "Tírion", "Taelan": "Táelan", "Isillien": "Isílien", "Pamela Redpath": "Pámela Rédpaz", "Pamela": "Pámela",
    "Joseph Redpath": "Yósef Rédpaz", "Dagran": "Dágran", "Alexstrasza": "Alekstrásha", "Gnomeregan": "Nomérégan",
    "Ysondre": "Isóndre", "Lethon": "Lézon", "Emeriss": "Émeris", "Taerar": "Teérar", "Turalyon": "Turálion",
    "Khadgar": "Kádgar", "Kurdran": "Kúrdran", "Thekal": "Zékal", "Mandokir": "Mándokir", "razzashi": "rasáshi",
    "Aedelas Blackmoore": "Édelas Blákmur", "Kazzak": "Kásak", "Ravenholdt": "Révenjolt", "Kirin Tor": "Kírin Tor",
    "Atal'Hakkar": "Atal Jákar", "Hakkar": "Jákar", "Ysera": "Iséra", "Dathrohan": "Dázrojan", "Balnazzar": "Balnásar",
    "Varimathras": "Varimázras", "Quel'Thalas": "Kel Zálas", "Ahn'Qiraj": "An Kiráj", "Saldean": "Sáldin",
    "CLUCK": "Clák", "R. O. I. D. S.": "erre, o, i, de, ese", "Nethergarde": "Nézergard", "Caer Darrow": "Kéir Dárrou",
    "Darrowshire": "Dárrou shair", "Scholomance": "Escolománs", "Stromgarde": "Estrómgard", "Kul Tiras": "Kul Tíras",
    "Naxxramas": "Naksrámas", "Karazhan": "Karazán", "Gadgetzan": "Gádguetsan", "Lady Katrana Prestor": "Léidi Katrána Préstor",
    "Katrana Prestor": "Katrána Préstor", "Onyxia": "Oníxia", "Anduin": "Ánduin", "Varian Wrynn": "Várian Rin",
    "Uldaman": "Uldáman", "Kotaku": "Kotáku", "Lordaeron": "Lordéron",
    "Ashbringer": "Ásh bringuer", "Grim Batol": "Grim Bátol", "Seradane": "Séradein", "Draenor": "Dréinor", "Menethil": "Ménezil",
    "Dun Morogh": "Dun Mórog", "troggs": "trogs", "atal'ai": "atal ái", "Genn": "Guen", "Andorhal": "Ándorjal", "Durnholde": "Dúrnjold",
    "Elwynn": "Élguin", "Número once": "Número ónse", "Sylvanas": "Silvánas",
}

# Whisper escribe distinto lo que Remy dice (cifras «sesenta y dos» -> 62, Stratholme -> «Strassholm», Elwynn -> «Elgin»,
# Velasangre -> «de la sangre», Grim Batol -> «Green Battle»…); revisado por hyp el 18-oct, sin oír cada toma
CER_MAX_POR_FRASE = {"c41_1": 0.08, "c11_0": 0.07, "c05_2": 0.07, "c62_0": 0.07, "c61_0": 0.07, "c61_1": 0.07, "c61_2": 0.07, "c60_1": 0.07, "c60_3": 0.07, "c59_1": 0.07, "c58_0": 0.07, "c58_1": 0.07, "c57_3": 0.07, "c56_1": 0.07, "c55_0": 0.07, "c55_1": 0.07, "c55_2": 0.07, "c54_0": 0.07, "c54_1": 0.07, "c54_2": 0.07, "c54_3": 0.07, "c53_1": 0.07, "c53_3": 0.07, "c50_0": 0.07, "c50_2": 0.07, "c50_3": 0.11, "c49_0": 0.07, "c49_2": 0.07, "c48_2": 0.07, "c48_3": 0.07, "c45_0": 0.07, "c45_1": 0.07, "c44_1": 0.07, "c44_3": 0.07, "c43_2": 0.07, "c41_0": 0.07, "c40_2": 0.07, "c39_2": 0.07, "c38_1": 0.07, "c38_3": 0.07, "c37_1": 0.07, "c36_0": 0.07, "c36_2": 0.07, "c35_1": 0.07, "c35_2": 0.07, "c34_0": 0.07, "c34_1": 0.07, "c33_1": 0.07, "c33_2": 0.07, "c31_3": 0.07, "c30_1": 0.07, "c29_1": 0.07, "c29_3": 0.07, "c27_1": 0.07, "c27_2": 0.07, "c26_2": 0.07, "c25_3": 0.07, "c24_1": 0.07, "c24_3": 0.07, "c23_2": 0.07, "c22_0": 0.07, "c21_0": 0.07, "c21_1": 0.07, "c21_2": 0.07, "c21_3": 0.07, "c20_0": 0.07, "c20_2": 0.07, "c20_3": 0.07, "c19_1": 0.07, "c17_1": 0.07, "c17_2": 0.07, "c16_1": 0.07, "c14_2": 0.07, "c14_3": 0.07, "c13_1": 0.07, "c13_2": 0.07, "c12_0": 0.07, "c11_2": 0.07, "c09_0": 0.07, "c09_1": 0.07, "c08_0": 0.07, "c08_2": 0.07, "c07_1": 0.07, "c07_2": 0.07, "c07_3": 0.07, "c06_0": 0.07, "c06_3": 0.07, "c04_0": 0.07, "c04_3": 0.07, "c03_0": 0.07, "c03_3": 0.07, "c03_5": 0.07, "c02_2": 0.07, "c01_2": 0.07, "c01_6": 0.07, "c42_3": 0.08}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # el audio del gameplay no se usa (se bajan solo imágenes)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Thraex", "Video Game Collector", "TheLtColonel", "Jansn Benchmarks", "Platinum WoW", "WoWAholics101"]),   # guías con recuadros/mapas, marca DRDEEPWOUND, benchmark con FPS (18-oct)
    # barras negras incrustadas que cazó la revisión del MASTER (18-oct): 051 laterales, 092 cinemática 2,35:1, 186 finas
    recorte_por={"scene-051": 0.06, "scene-092": 0.13, "scene-186": 0.06},
)

TRANSICIONES = [("continua", 0.1)] * 70

# Ánimo de cada curiosidad para Lyria (sin nombres propios: el filtro los rechaza). `tramos` (<= 175 s) se escriben en la
# sesión 2, con la línea de tiempo real de `tiempo` (~11 tramos para 31 min).
_ANIMO = {
    "misterio": ("hushed mystery, low strings and celesta, something hidden", 4),
    "humor": ("wry and playful, pizzicato strings, light hand percussion", 4),
    "aventura": ("adventurous travelling theme, frame drums, warm horns", 4),
    "epico": ("grand and heroic, full brass, choir pads", 4),
    "oscuro": ("dark and ominous, low choir, tolling bells, slow pulse", 4),
    "triste": ("melancholic and tender, solo strings, soft harp", 4),
    "fuego": ("fiery and driving, heavy drums, low brass, forge rhythm", 4),
    "taberna": ("dwarven tavern bounce, lute and fiddle, stomping rhythm", 4),
}
_ESC_ANIMO = {
    "c62": "oscuro", "c61": "misterio", "c60": "humor", "c59": "humor", "c58": "humor", "c57": "misterio",
    "c56": "humor", "c55": "humor", "c54": "epico", "c53": "humor", "c52": "aventura", "c51": "oscuro", "c50": "fuego",
    "c49": "misterio", "c48": "epico", "c47": "oscuro", "c46": "oscuro", "c45": "aventura", "c44": "misterio",
    "c43": "humor", "c42": "oscuro", "c41": "aventura", "c40": "aventura", "c39": "oscuro", "c38": "humor",
    "c37": "aventura", "c36": "oscuro", "c35": "humor", "c34": "epico", "c33": "taberna", "c32": "misterio",
    "c31": "triste", "c30": "oscuro", "c29": "triste", "c28": "epico", "c27": "oscuro", "c26": "aventura",
    "c25": "misterio", "c24": "misterio", "c23": "epico", "c22": "taberna", "c21": "triste", "c20": "humor",
    "c19": "misterio", "c18": "fuego", "c17": "oscuro", "c16": "epico", "c15": "humor", "c14": "oscuro",
    "c13": "misterio", "c12": "taberna", "c11": "misterio", "c10": "fuego", "c09": "oscuro", "c08": "oscuro",
    "c07": "oscuro", "c06": "aventura", "c05": "misterio", "c04": "oscuro", "c03": "triste", "c02": "humor",
}
LYRIA = dict(
    estilo="Epic fantasy orchestral underscore like a classic high-fantasy MMORPG soundtrack: warm horns, low strings, "
           "frame drums, choir pads, instrumental only, no vocals, steady and unobtrusive under narration.",
    escenas=dict({"intro": ("curious and inviting, a map unrolling, light percussion building", 6),
                  "c01": ("sacred and awe-struck, choir rising to a solemn triumphant peak", 8),
                  "cierre": ("resolved and a little mischievous, warm horns fading out", 4)},
                 **{k: _ANIMO[v] for k, v in _ESC_ANIMO.items()}),
    tramos=[   # <= 175 s cada uno (timeline del 18-oct, 1856 s)
        (["intro", "c62", "c61", "c60", "c59"], "Begin softly from near silence with a curious pulse. End on a sustained held chord, gently."),   # 0-155 s (155.0 s)
        (["c58", "c57", "c56", "c55", "c54"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 155-302 s (147.5 s)
        (["c53", "c52", "c51", "c50", "c49"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 302-460 s (157.5 s)
        (["c48", "c47", "c46", "c45", "c44"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 460-602 s (142.5 s)
        (["c43", "c42", "c41", "c40", "c39", "c38"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 602-765 s (162.5 s)
        (["c37", "c36", "c35", "c34", "c33", "c32"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 765-918 s (152.5 s)
        (["c31", "c30", "c29", "c28", "c27", "c26"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 918-1075 s (157.5 s)
        (["c25", "c24", "c23", "c22", "c21"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 1075-1220 s (145.0 s)
        (["c20", "c19", "c18", "c17", "c16", "c15", "c14"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 1220-1388 s (167.5 s)
        (["c13", "c12", "c11", "c10", "c09", "c08"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 1388-1540 s (152.5 s)
        (["c07", "c06", "c05", "c04", "c03"], "Begin on a sustained held chord. End on a sustained held chord, gently."),   # 1540-1705 s (165.0 s)
        (["c02", "c01", "cierre"], "Begin on a sustained held chord. Climb to a solemn triumphant peak, then settle and fade out to silence at the end."),   # 1705-1856 s (151.2 s)
    ],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En los Reinos del Este hay un cartero muerto que sigue repartiendo el correo, y una gallina que te da una misión si le cacareas lo suficiente.",
        "Y hay una espada que hace arrodillarse a un ejército entero en cuanto cruzas la puerta.",
        "Todo eso está en el World of Warcraft original, y todo eso vuelve el cuatro de noviembre con World of Warcraft Forever.",
        "Estas son sesenta y dos curiosidades de los Reinos del Este, en cuenta regresiva.",
        "Empiezo con algunas que casi nadie conoce, y luego voy alternando entre las de culto y las que seguro ya oíste en alguna taberna.",
        "La número uno es la más rara de todas, una que la mayoría de los jugadores nunca vio con sus propios ojos.",
    ]},
    {"id": "c62", "frases": [
        "Número sesenta y dos. En Stratholme hay un jefe que es, literalmente, el cartero de la ciudad.",
        "Cada buzón que abres suelta a tres carteros no-muertos de élite, que vienen a cobrarte el envío.",
        "Abre los tres buzones y aparece él, el jefe de correos Malown, convertido en fantasma.",
        "Y lo mejor es lo que suelta, un conjunto completo de cartero, con piezas que solo salen de este señor.",
    ]},
    {"id": "c61", "frases": [
        "Número sesenta y uno. En Zul'Gurub hay un jefe que no se busca, se pesca.",
        "Se llama Gahz'ranka, es una serpiente marina gigante y vive escondida en el agua de la banda.",
        "Para sacarla necesitas un cebo especial que vende Nat Pagle, el pescador más famoso del juego, pero solo si antes le devuelves su cinta de medir.",
        "Luego hay que pescar cinco peces en unas aguas turbias alrededor del altar del dios de la sangre, y las guías piden unos trescientos treinta de pesca.",
    ]},
    {"id": "c60", "frases": [
        "Número sesenta. En las Tierras Devastadas venden esteroides para héroes.",
        "En el castillo de Nethergarde hay dos magos que te cambian partes de monstruos por consumibles.",
        "Uno de sus frascos se llama, con todas sus letras, R. O. I. D. S., y en inglés eso se lee igual que el apodo de los esteroides.",
        "Es la única droga de gimnasio con nombre oficial en todo Azeroth, y te la prepara un mago con bata.",
    ]},
    {"id": "c59", "frases": [
        "Número cincuenta y nueve. Dos hermanos que mandan a cada bando a matar al otro.",
        "La familia Barov era dueña de medio Lordaeron, y el padre cambió su castillo de Caer Darrow a la Plaga a cambio de inmortalidad.",
        "De la familia quedan dos herederos, Weldon, que sigue siendo humano y está con la Alianza, y Alexi, que es un renegado y vive en El Baluarte, con la Horda.",
        "Los dos quieren las escrituras de la familia, que están perdidas dentro de la Scholomance.",
        "Y en otra misión, cada uno le pide a su bando que de paso le haga el favor de matar al hermano.",
    ]},
    {"id": "c58", "frases": [
        "Número cincuenta y ocho, y vamos con un clásico de verdad, porque hablamos de Hogger.",
        "Es un gnoll de élite de nivel once que se pasea por el sur del Bosque de Elwynn, y para muchos fue el primer muro del juego.",
        "Llegabas a nivel ocho con tu espada de principiante, creías que podías solo, y en tres golpes estabas en el cementerio.",
        "Se volvió tan famoso que Blizzard lo convirtió en carta de Hearthstone, en jefe de las Mazmorras de Ventormenta y en un meme de más de veinte años.",
    ]},
    {"id": "c57", "frases": [
        "Número cincuenta y siete. Una princesa en apuros en las Tierras Altas de Arathi que, en realidad, no estaba en apuros.",
        "Todo empieza con unos fragmentos brillantes en una garganta llena de kobolds, y una voz que te pide ayuda.",
        "La voz se llama Myzrael, dice ser una princesa atrapada, y te va pidiendo cosas, motas de energía, piedras de atadura, que mates a un guardián de piedra.",
        "Hasta que la invocas, y resulta que Myzrael es un elemental de tierra que los gigantes de montaña, creados por los titanes, encerraron bajo Arathi.",
        "La encerraron por algo, claro, y la última misión consiste en pelear contra la princesa que acabas de liberar y volver a atarla con sus propios grilletes.",
    ]},
    {"id": "c56", "frases": [
        "Número cincuenta y seis. Tú no llevar vela.",
        "Es la frase más famosa de los kobolds de Elwynn, los que excavan las minas con una vela encima de la cabeza.",
        "En inglés gritaban you no take candle, y se volvió uno de los primeros memes del juego.",
    ]},
    {"id": "c55", "frases": [
        "Número cincuenta y cinco. En una granja de Elwynn hay una telenovela completa.",
        "Dos familias de granjeros, los Stonefield y los Maclure, viven peleadas, cada una en su lado del camino.",
        "Y en medio están Maybell Maclure y Tommy Joe Stonefield, que están enamorados y no se pueden ver.",
        "Y no es Romeo y Julieta, como piensa casi todo el mundo, es una referencia a los Hatfield y los McCoy, la pelea de familias más famosa de Estados Unidos.",
    ]},
    {"id": "c54", "frases": [
        "Número cincuenta y cuatro. Todos los humanos de Azeroth vienen de Arathi.",
        "Hace casi tres mil años, el caudillo Thoradin unió a las tribus humanas en el reino de Arathor, con capital en la ciudad de Strom.",
        "De Arathor salieron después los demás reinos humanos, Ventormenta, Lordaeron, Gilneas, Kul Tiras, Alterac y Dalaran.",
        "Lo que queda de aquella cuna es Stromgarde, y en Classic está tomada por ogros, trols y ladrones del Sindicato, así que la humanidad empezó en un barrio peligroso.",
    ]},
    {"id": "c53", "frases": [
        "Número cincuenta y tres. El grito más famoso de la historia de los videojuegos se dio en los Reinos del Este.",
        "Un grupo de la hermandad Pals for Life planea la entrada con todo detalle, hasta con un treinta y dos punto treinta y tres por ciento de supervivencia.",
        "Y mientras hablan, un paladín que estaba lejos del teclado vuelve, grita su propio nombre y entra corriendo solo.",
        "Leeroy Jenkins. El grupo entero muere, y él solo alcanza a decir que por lo menos tiene pollo.",
    ]},
    {"id": "c52", "frases": [
        "Número cincuenta y dos. Los enanos descubren que antes eran de piedra.",
        "En Uldaman, en las Tierras Inhóspitas, hay unos discos de los titanes, los Discos de Norgannon.",
        "Los titanes crearon a los terráneos, unos seres de piedra, para darle forma al mundo.",
        "Con el tiempo, una maldición, la Maldición de la Carne, los fue convirtiendo en carne y hueso, y de ellos descienden los enanos.",
    ]},
    {"id": "c51", "frases": [
        "Número cincuenta y uno. Las Minas de la Muerte nacieron de una factura sin pagar.",
        "Después de la Segunda Guerra, los canteros reconstruyeron Ventormenta piedra por piedra.",
        "Cuando terminaron, la nobleza de la ciudad se negó a pagarles, y su líder, Edwin VanCleef, se llevó a los canteros y fundó la Hermandad Defias.",
        "Desde entonces viven escondidos bajo los Páramos de Poniente, en una mina donde están armando un barco pirata entero.",
    ]},
    {"id": "c50", "frases": [
        "Número cincuenta. En las Profundidades de Roca Negra hay siete enanos, y no son los del cuento.",
        "Hace siglos, el hechicero Thaurissan y siete de sus aliados Hierro Negro quisieron invocar un elemental para ganar la guerra contra los otros enanos.",
        "Les salió Ragnaros, el señor del fuego, y el ritual los mató a los siete.",
        "Y fíjate en los nombres, Anger'rel, Seeth'rel, Dope'rel, Gloom'rel, Vile'rel, Hate'rel y Doom'rel, que en inglés son ira, rabia, tontería, tristeza, vileza, odio y perdición.",
        "Siete enanos con su humor puesto en el nombre. Es difícil no pensar en Blancanieves, solo que estos invocaron el apocalipsis.",
    ]},
    {"id": "c49", "frases": [
        "Número cuarenta y nueve. Ragnaros nunca te enseñó las piernas.",
        "En el Núcleo de Magma, el mayordomo Executus te entrega al señor del fuego, que sale de la lava furioso porque lo despertaron antes de tiempo.",
        "Su grito es too soon, demasiado pronto, y lleva veinte años siendo meme.",
        "Pero en toda la pelea solo lo ves de la cintura para arriba, porque está metido en la lava hasta el ombligo.",
        "Hubo que esperar seis años, hasta las Tierras de Fuego de Cataclysm, para verlo de pie, y resultó que sí tenía piernas.",
    ]},
    {"id": "c48", "frases": [
        "Número cuarenta y ocho. La ventana más útil de la Montaña Roca Negra.",
        "Para entrar al Núcleo de Magma, en teoría hay que cruzar las Profundidades de Roca Negra enteras, en grupos de cinco, hasta el portal del fondo.",
        "Por eso existe Lothos Riftwaker, un personaje al pie de la montaña que te da la misión de sintonización desde el nivel cincuenta y cinco.",
        "Y si ya estás sintonizado, puedes saltar por la ventana que está junto a Lothos y caer directo dentro del Núcleo de Magma.",
    ]},
    {"id": "c47", "frases": [
        "Número cuarenta y siete. La guerra que nadie programó.",
        "En las Laderas de Trabalomas hay dos pueblos casi frente a frente, Costasur de la Alianza y Molino Tarren de la Horda.",
        "En los primeros meses no había campos de batalla, así que los jugadores se organizaban solos y se atacaban durante horas.",
        "Para mucha gente de la vieja guardia, el mejor PvP del World of Warcraft original fue un pleito de vecinos en una colina.",
    ]},
    {"id": "c46", "frases": [
        "Número cuarenta y seis. En el Bosque del Ocaso hay un monstruo que camina hasta el pueblo.",
        "Abercrombie, un ermitaño que parece un viejito inofensivo, te pide ingredientes para una supuesta receta, y tú se los llevas.",
        "En realidad está armando una abominación, y se la quiere regalar al alcalde de Villa Oscura.",
        "Cuando terminas su cadena, la abominación, Stitches, sale del cementerio y empieza a caminar por el camino principal.",
        "El pregonero del pueblo va anunciando cada paso que da, y Stitches va aplastando a los guardias que salen a frenarlo.",
    ]},
    {"id": "c45", "frases": [
        "Número cuarenta y cinco. La pandemia de Sangre Corrupta empezó en la Vega de Tuercespina.",
        "En septiembre de dos mil cinco abrió Zul'Gurub, y su jefe final, Hakkar, lanzaba una maldición que saltaba de jugador en jugador.",
        "Se suponía que no saldría de la banda, pero las mascotas de los cazadores la sacaron al mundo.",
        "Fue tan realista que unos epidemiólogos la estudiaron después como modelo de cómo reacciona la gente durante un brote.",
    ]},
    {"id": "c44", "frases": [
        "Número cuarenta y cuatro. Para ser pirata, primero hay que matar policías.",
        "Los Bucaneros Velasangre son los piratas que asedian Bahía del Botín, y empiezan odiándote.",
        "Para subir su reputación hay que hacer algo que casi nadie hace, declararle la guerra a Bahía del Botín y matar a sus guardias goblin.",
        "Y el premio, al llegar a amistoso, es el sombrero de almirante Velasangre, que invoca un loro.",
    ]},
    {"id": "c43", "frases": [
        "Número cuarenta y tres. En el trono de Ventormenta había un dragón.",
        "En el World of Warcraft original, el rey Varian Wrynn está desaparecido, y el que se sienta en el trono es su hijo Anduin, un niño.",
        "A su lado, como consejera, está Lady Katrana Prestor, una noble elegante que siempre tiene la respuesta correcta.",
        "La cadena de la Alianza para entrar a la guarida de Onyxia revela la verdad, porque Katrana Prestor es Onyxia, la hija de Alamuerte, disfrazada de humana.",
    ]},
    {"id": "c42", "frases": [
        "Número cuarenta y dos. En el Tranvía Subterráneo hay un enano cazando ratas.",
        "En una de sus estaciones está Monty, que tiene un problema serio de ratas en las vías.",
        "Te da una flauta y una misión, tocarla para que las ratas te sigan y llevárselas a él.",
        "Así que en la ciudad más avanzada de la Alianza, tu personaje termina como el flautista de Hamelín, rodeado de ratas.",
    ]},
    {"id": "c41", "frases": [
        "Número cuarenta y uno. La carrera del barón.",
        "En la parte no-muerta de Stratholme, el barón Rivendare tiene presa a Ysida Harmon.",
        "Cuando cruzas cierta puerta, el propio barón te avisa que tienes cuarenta y cinco minutos antes de ejecutarla.",
        "Y encima, el barón puede soltar las riendas del destrero de la muerte, uno de los corceles más buscados de Classic, con una probabilidad bajísima.",
    ]},
    {"id": "c40", "frases": [
        "Número cuarenta. Hay un pollo robot perdido en las Tierras del Interior.",
        "Si cazas en la zona, muy de vez en cuando te cae una baliza de socorro.",
        "La baliza te lleva a un robot con forma de gallina, el OOX-09/HL, estrellado cerca de un río.",
        "Pero hay tres robots así, perdidos en tres zonas del mundo, las Tierras del Interior, Feralas y Tanaris.",
        "Si los rescatas a los tres, el gnomo te regala tu propio pollo mecánico como mascota.",
    ]},
    {"id": "c39", "frases": [
        "Número treinta y nueve. La plaga de Lordaeron empezó en un granero.",
        "Andorhal, en las Tierras de la Peste del Oeste, era una ciudad agrícola y el centro de reparto de grano del reino.",
        "Kel'Thuzad y su Culto de los Malditos mezclaron la plaga con el grano y lo repartieron desde ahí a todo el norte.",
        "Quien comía ese grano moría, y luego se levantaba como no-muerto al servicio del Rey Exánime.",
    ]},
    {"id": "c38", "frases": [
        "Número treinta y ocho. El libro que llenó tus bolsas.",
        "En la Vega de Tuercespina vive Hemet Nesingwary, un cazador que escribió un libro, Las verdes colinas de Tuercespina.",
        "El libro se deshizo, y sus páginas andan desperdigadas por toda la jungla, cayéndoles a trols y a gorilas.",
        "Y el nombre es un chiste literario, porque Nesingwary es un guiño a Ernest Hemingway, que escribió Las verdes colinas de África.",
    ]},
    {"id": "c37", "frases": [
        "Número treinta y siete. En el Monasterio Escarlata hay una referencia a Los Simpson.",
        "En la Biblioteca, el maestro de canes Loksey te recibe gritando que suelten a los perros.",
        "En inglés grita release the hounds, la misma frase del señor Burns cada vez que alguien se acerca a su mansión.",
        "Y en la Catedral está la pareja más famosa de Classic, el comandante Mograine y la alta inquisidora Melenablanca.",
        "Tiras a Mograine, ella entra corriendo, te duerme a todo el grupo y lo resucita gritando que se levante su campeón.",
    ]},
    {"id": "c36", "frases": [
        "Número treinta y seis. Cada domingo, Tuercespina se llena de pescadores.",
        "Es el concurso de pesca de Tuercespina, cada domingo de dos a cuatro de la tarde, hora del servidor.",
        "La meta es pescar cuarenta peces sabrosos moteados y llevárselos a Riggle Bassbait, en Bahía del Botín, antes que nadie.",
        "El premio gordo es una caña de arcanita, de las mejores cañas de pescar de Classic.",
    ]},
    {"id": "c35", "frases": [
        "Número treinta y cinco. Entrañas está debajo de la capital de Lordaeron.",
        "Cuando entras a Entrañas, primero cruzas las ruinas de la ciudad de Lordaeron y su salón del trono.",
        "Es el mismo salón donde Arthas, recién corrompido, mató a su padre, el rey Terenas, en Warcraft tres.",
        "Y en la sala real, junto a Sylvanas, hay un demonio de pie que nadie cuestiona, pero de él hablamos casi al final.",
    ]},
    {"id": "c34", "frases": [
        "Número treinta y cuatro. Cada tres horas, un cofre desata una guerra en la Vega de Tuercespina.",
        "En la Arena Gurubashi aparece un pirata goblin, Short John Mithril, y suelta un cofre en el centro.",
        "Quien lo abre se queda con el botín, y la arena es zona de todos contra todos, sin bandos ni grupos que valgan.",
        "Y lo normal era que el cofre lo abriera un pícaro invisible mientras los demás se mataban por él.",
    ]},
    {"id": "c33", "frases": [
        "Número treinta y tres. Las bajas más absurdas de Azeroth suceden en una taberna dentro de una mazmorra.",
        "En las Profundidades de Roca Negra está el Grim Guzzler, un bar de enanos Hierro Negro con tabernero, música y borrachos.",
        "Pero si empiezas a llevarte las jarras de la barra sin pagar, el tabernero, Plugger Spazzring, se enoja y el bar entero se te echa encima.",
    ]},
    {"id": "c32", "frases": [
        "Número treinta y dos. Karazhan estaba en el mapa, pero cerrada.",
        "En el Paso de la Muerte se ve la torre de Medivh desde lejos, y en el juego original su puerta principal no abre.",
        "Blizzard la abrió como banda en The Burning Crusade, y se volvió una de las bandas más queridas de la historia del juego.",
    ]},
    {"id": "c31", "frases": [
        "Número treinta y uno, la mitad del camino. La historia más triste de las Tierras de la Peste del Este empieza en una cabaña.",
        "Tirion Fordring, el paladín al que expulsaron de su orden por defender a un orco, vive exiliado en una cabaña junto a un lago.",
        "Te pide que busques a su hijo, Taelan, que ahora es un alto mando de la Cruzada Escarlata en Vega del Amparo.",
        "Pero al salir, el gran inquisidor Isillien les tiende una emboscada y mata a Taelan delante de ti.",
        "Tirion llega al galope, y llega tarde. Es de las escenas más duras de Classic, y casi nadie la vio, porque es una cadena larga en zona de nivel alto.",
    ]},
    {"id": "c30", "frases": [
        "Número treinta. Hay una pirámide flotando sobre las Tierras de la Peste del Este.",
        "En el último parche grande del juego original llegó Naxxramas, una necrópolis flotante sobre el Bosque de la Plaga, muy cerca de Stratholme.",
        "Era la banda más difícil del juego, y muy pocos jugadores en el mundo la vieron completa antes de The Burning Crusade.",
    ]},
    {"id": "c29", "frases": [
        "Número veintinueve. En las Tierras de la Peste del Este hay una niña fantasma buscando su muñeca.",
        "En las ruinas de Darrowshire, entre casas quemadas, aparece Pamela Redpath, una niña que sigue esperando a su papá.",
        "Te pide que encuentres su muñeca, que quedó rota en pedazos repartidos por el pueblo.",
        "Lo que Pamela no sabe es que su padre, el capitán Joseph Redpath, cayó defendiendo Darrowshire y la Plaga lo corrompió.",
    ]},
    {"id": "c28", "frases": [
        "Número veintiocho. Había batallas del Valle de Alterac que duraban días.",
        "El Valle de Alterac original era una guerra de verdad, con cuarenta jugadores por bando, comandantes, misiones y refuerzos que no se acababan.",
        "Hay jugadores que cuentan que entraban, jugaban un par de horas, se iban a dormir y al día siguiente seguían en la misma batalla.",
    ]},
    {"id": "c27", "frases": [
        "Número veintisiete. En Los Humedales hay una fortaleza cerrada con una historia horrible.",
        "Al este de la zona se ve la entrada de Grim Batol, una antigua fortaleza enana tallada en la montaña.",
        "En el juego original no se puede entrar, y los orcos Faucedraco que rondan la zona son lo que queda de quienes la ocuparon.",
        "Esos orcos tuvieron ahí prisionera a Alexstrasza, la reina de los dragones rojos, para criar dragones de guerra para la Horda.",
    ]},
    {"id": "c26", "frases": [
        "Número veintiséis. Ventormenta no tenía puerto.",
        "Para tomar un barco, la Alianza tenía que irse hasta el Puerto de Menethil, en Los Humedales, o bajar hasta Bahía del Botín.",
        "El puerto de Ventormenta llegó con la expansión del Rey Exánime, para mandar a la flota a Rasganorte.",
    ]},
    {"id": "c25", "frases": [
        "Número veinticinco. En el Bosque del Ocaso hay una puerta al Sueño Esmeralda.",
        "En la Arboleda del Crepúsculo, un claro de árboles enormes en medio del bosque, hay un portal hacia el Sueño Esmeralda.",
        "De esos portales salían los dragones de la Pesadilla, cuatro dragones verdes corrompidos que eran jefes de mundo.",
        "Ysondre, Lethon, Emeriss y Taerar aparecían en alguno de los portales, y servidores enteros se movilizaban para tumbarlos.",
    ]},
    {"id": "c24", "frases": [
        "Número veinticuatro. Había un reino entero detrás de un muro.",
        "Al sur del Bosque de Argénteos se levanta la Muralla de Cringris, que el rey Genn Cringris mandó construir para aislar a Gilneas del mundo.",
        "En el juego original, Gilneas aparece en el mapa, pero está cerrada, y su gran puerta nunca se abre.",
        "Blizzard la abrió en Cataclysm como zona de inicio de los huargen, y entonces se entendió por qué había tantos huargen en esa esquina del mapa.",
    ]},
    {"id": "c23", "frases": [
        "Número veintitrés. En la entrada de Ventormenta hay estatuas de gente desaparecida.",
        "Al cruzar el puente, el Valle de los Héroes tiene estatuas de los héroes de la Segunda Guerra.",
        "Están Turalyon, Alleria Brisaveloz, Khadgar, Danath Aterratrols y Kurdran Martillo Salvaje.",
        "Todos ellos cruzaron el Portal Oscuro para cerrarlo desde Draenor, y nunca volvieron.",
        "Cuando llegó The Burning Crusade, los jugadores cruzaron el portal y se encontraron a varios de esos héroes vivos al otro lado.",
    ]},
    {"id": "c22", "frases": [
        "Número veintidós. La hija del rey de Forjaz se casó con el enemigo.",
        "La princesa Moira Barbabronce, hija de Magni, desapareció, y en Forjaz creen que la secuestraron los Hierro Negro.",
        "Y cuando llegas al fondo de las Profundidades de Roca Negra, ella está junto al emperador Dagran Thaurissan, y cuando lo derrotas, en lugar de darte las gracias, te reclama haber matado a su esposo.",
        "Además, durante la pelea ella lo cura, y si la matas a ella, fallas la misión de rescate, así que muchos grupos acababan discutiendo.",
    ]},
    {"id": "c21", "frases": [
        "Número veintiuno. En las Laderas de Trabalomas está la cárcel donde creció Thrall.",
        "El castillo de Durnholde, al sur de la zona, era un campo de internamiento de orcos después de la Segunda Guerra.",
        "Ahí, el teniente general Aedelas Blackmoore crió a un bebé orco como gladiador, y le puso Thrall, que en inglés significa esclavo.",
        "Thrall escapó de Durnholde, liberó a los orcos de los campos y terminó fundando la nueva Horda y la ciudad de Orgrimmar.",
    ]},
    {"id": "c20", "frases": [
        "Número veinte. Los gnomos empezaban en casa ajena.",
        "En el World of Warcraft original, los gnomos no tienen zona de inicio propia, empiezan en el Valle de Crestanevada, con los enanos.",
        "La razón es que perdieron su ciudad, porque Gnomeregan fue invadida por los troggs, y para echarlos, los gnomos soltaron una radiación que acabó con ellos mismos.",
        "Así que los gnomos son refugiados que viven en Ciudad Manitas, un barrio de Forjaz, con su ciudad radiactiva a unos pasos.",
    ]},
    {"id": "c19", "frases": [
        "Número diecinueve. Hay una mansión de pícaros escondida en las montañas.",
        "En las Montañas de Alterac, por un camino casi oculto que sale de las Laderas de Trabalomas, está la mansión Ravenholdt.",
        "Mucha gente jugó años en Trabalomas sin saber que a unos metros, montaña arriba, había una mansión llena de asesinos tomando el té.",
    ]},
    {"id": "c18", "frases": [
        "Número dieciocho. Nefarian te llama por tu clase.",
        "En la Guarida Alanegra, el jefe final, Nefarian, que es hermano de Onyxia, grita el nombre de una clase cada cierto tiempo y le aplica un castigo distinto.",
        "Grita guerreros y los fuerza a la actitud rabiosa, grita cazadores y les rompe el arco, grita sacerdotes y sus curaciones empiezan a hacer daño.",
        "Grita druidas y los atrapa en forma felina, y grita magos y empiezan a convertir en oveja a sus propios compañeros.",
    ]},
    {"id": "c17", "frases": [
        "Número diecisiete. En el Bosque del Ocaso nunca sale el sol.",
        "La zona está siempre en penumbra, aunque en Elwynn, a unos pasos, sea mediodía.",
        "Según el lore, ese bosque era parte de Elwynn, verde y luminoso, y se fue oscureciendo bajo la sombra de Karazhan y, después, de la Pesadilla.",
    ]},
    {"id": "c16", "frases": [
        "Número dieciséis. Las monturas más deseadas de Classic estaban en una jungla.",
        "En Zul'Gurub, dos jefes pueden soltar monturas épicas, el sumo sacerdote Thekal un tigre y el señor de sangre Mandokir un raptor.",
        "Cuando Zul'Gurub cambió con Cataclysm, dejaron de poder conseguirse, y en Classic vuelven a estar en juego.",
    ]},
    {"id": "c15", "frases": [
        "Número quince. La Feria de la Luna Negra llegaba a Villadorada.",
        "En el juego original, la feria montaba sus carpas unas semanas a las afueras de Villadorada, en Elwynn, y otras semanas en Mulgore.",
        "Y luego se iba, sin avisar a nadie, y te dejaba con los boletos en la mano.",
    ]},
    {"id": "c14", "frases": [
        "Número catorce. El Portal Oscuro estaba apagado.",
        "En las Tierras Devastadas está el Portal Oscuro, el mismo que trajo a la Horda a Azeroth.",
        "Y cerca de él se paseaba un jefe de mundo, Lord Kazzak, un demonio de la Legión.",
        "Kazzak se curaba cada vez que mataba a un jugador, así que mientras más gente moría, más difícil era tumbarlo.",
    ]},
    {"id": "c13", "frases": [
        "Número trece. En el Pantano de las Penas hay un templo hundido a propósito.",
        "El Templo de Atal'Hakkar lo construyeron los trols atal'ai para adorar a Hakkar, el dios de la sangre.",
        "Cuando intentaron traerlo al mundo, Ysera, la aspecto de los dragones verdes, hundió el templo en el pantano y dejó a sus dragones vigilándolo.",
        "Y el templo esconde un acertijo, seis estatuas que hay que activar en un orden exacto para que aparezca un jefe oculto.",
    ]},
    {"id": "c12", "frases": [
        "Número doce. La verdadera capital de la Alianza era Forjaz.",
        "En el papel, la capital es Ventormenta, pero en el juego original casi todos los jugadores de la Alianza vivían en Forjaz.",
        "La casa de subastas y el banco estaban a unos pasos, y alrededor la gente se juntaba a comerciar, a buscar grupo y a presumir.",
    ]},
    {"id": "c11", "frases": [
        "Número once. Dalaran estaba metida en una burbuja.",
        "En las Montañas de Alterac, junto a un lago, hay una ciudad entera encerrada en una cúpula violeta.",
        "En el World of Warcraft original, el Kirin Tor la está reconstruyendo detrás de un escudo mágico, y no se puede entrar.",
        "En el Rey Exánime la levantaron entera y se la llevaron volando a Rasganorte, dejando un cráter, pero en Classic la burbuja sigue ahí.",
    ]},
    {"id": "c10", "frases": [
        "Número diez, y entramos a las diez últimas. Un solo volcán tiene cinco instancias.",
        "Dentro de la Montaña Roca Negra están las Profundidades de Roca Negra, la Cumbre de Roca Negra inferior y superior, el Núcleo de Magma y la Guarida Alanegra.",
        "Y todas cuentan la misma guerra, con los enanos Hierro Negro abajo, el Vuelo Negro arriba y Ragnaros en el fondo.",
    ]},
    {"id": "c09", "frases": [
        "Número nueve. La Cruzada Escarlata de Stratholme la dirigía un demonio.",
        "En la parte viva de Stratholme, el líder de la Cruzada es el gran cruzado Dathrohan, el hombre que más odia a la Plaga en todo Lordaeron.",
        "Lo enfrentas al final de esa parte de la mazmorra, y en plena pelea se transforma, porque en realidad es Balnazzar, un señor del terror.",
        "Los señores del terror son los demonios que ayudaron a crear la Plaga, así que la orden más fanática contra los no-muertos la dirigía uno de sus inventores.",
    ]},
    {"id": "c08", "frases": [
        "Número ocho. Los huargen llegaron a los Reinos del Este por culpa de un mago.",
        "En el castillo de Colmillo Oscuro vive el archimago Arugal, un mago de Dalaran desesperado por frenar a la Plaga.",
        "Para conseguirlo invocó a los huargen desde otro mundo, convencido de que podría controlarlos.",
        "Y en la aldea que está a los pies del castillo, la maldición de Arugal guarda un secreto que veremos dentro de muy poco.",
    ]},
    {"id": "c07", "frases": [
        "Número siete. Al lado de Sylvanas siempre hubo un traidor.",
        "En la sala real de Entrañas, el demonio que te prometí está de pie junto a la Dama Oscura, y se llama Varimathras.",
        "Es un señor del terror, y además es hermano de Balnazzar, el demonio de Stratholme.",
        "Años después, en el Rey Exánime, Varimathras traiciona a Sylvanas y se queda con Entrañas. Estaba junto al trono desde el primer día, esperando.",
    ]},
    {"id": "c06", "frases": [
        "Número seis. Encima de Forjaz había un aeropuerto que oficialmente no existía.",
        "Al noreste de la ciudad, entre las montañas nevadas de Dun Morogh, hay un valle alto con una pista de aterrizaje enana.",
        "En el juego original no tenía ni nombre en el mapa, y para llegar había que escalar montañas con mucha paciencia, o caer planeando desde arriba.",
        "Lo curioso es que las misiones del esfuerzo de guerra de Ahn'Qiraj mencionan a personajes en ese aeródromo, aunque en el juego están dentro de Forjaz.",
    ]},
    {"id": "c05", "frases": [
        "Número cinco. Al norte del continente había tierra sin terminar.",
        "Más allá de las Tierras de la Peste del Este, el mapa del juego original se acaba en montañas, pero la tierra sigue.",
        "Ahí está Quel'Thalas, el reino de los altos elfos, que en Classic no existe como zona en la que se pueda entrar.",
        "Algunos jugadores encontraron formas de colarse y vieron un pedazo de terreno a medio hacer, con árboles, sin misiones y sin nadie.",
        "No es oficial, pero muchos lo ven como un primer esbozo del bosque Canción Eterna, que Blizzard terminó para The Burning Crusade.",
    ]},
    {"id": "c04", "frases": [
        "Número cuatro. En el Bosque de Argénteos hay un pueblo que cambia con la hora del día.",
        "De día, la Aldea Piroleña parece un pueblo gilneano normal, con guardias humanos y gente trabajando.",
        "Pero Arugal maldijo a sus habitantes, y cuando cae la noche, se convierten en huargen.",
        "Los centinelas pasan a ser huargen de élite, y desde ese momento atacan a la Horda y a la Alianza por igual.",
        "Muchísimos jugadores pasaron de día, hicieron su misión y nunca supieron que al anochecer el pueblo entero se transforma.",
    ]},
    {"id": "c03", "frases": [
        "Número tres. En Stratholme hay un paladín que espera la batalla de su vida.",
        "En una capilla de la parte no-muerta de la ciudad está Aurius, un paladín de la Mano de Plata que casi cae ante la Plaga.",
        "Está tan débil que no puede salir de ahí, y te pide un medallón de fe que quedó guardado en un cofre, detrás de un cruzado fanático.",
        "Si se lo llevas, cuando llegas a la pelea contra el barón Rivendare, la puerta se abre y entra Aurius a pelear a tu lado.",
        "Lucha con todo lo que le queda, y al terminar la pelea cae herido de muerte.",
        "Y según el lore, el hombre contra el que acaba de dar la vida es su propio padre, porque Aurius es hijo del barón Rivendare.",
    ]},
    {"id": "c02", "frases": [
        "Número dos. Hay una misión escondida que solo aparece si le cacareas a una gallina.",
        "Te paras frente a cualquier gallina del juego y usas el gesto de gallina, una y otra vez.",
        "Si tienes suerte, la gallina te ofrece una misión que se llama, con toda la seriedad del mundo, CLUCK.",
        "Te pide un pienso especial que vende el granjero Saldean, en los Páramos de Poniente.",
        "Y aquí está la trampa, porque si usas el pienso desde tus bolsas, te lo comes tú.",
        "Hay que dárselo desde la propia gallina, en su opción de diálogo, y a cambio pone un huevo.",
        "De ese huevo sale tu propia gallina de mascota, y en Classic es cosa solo de la Alianza, porque la Horda tuvo que esperar hasta el Rey Exánime.",
    ]},
    {"id": "c01", "frases": [
        "Número uno. Un jefe que se pesca, un cartero fantasma y una gallina con misión, y aun así esta curiosidad gana a todas.",
        "Es la Crematoria, la Ashbringer, la espada más legendaria de la Luz, y en el juego original existe una versión corrupta.",
        "La suelta en Naxxramas uno de los Cuatro Jinetes, el alto señor Mograine, levantado por la Plaga como caballero de la muerte.",
        "Conseguirla exigía cuarenta personas en la banda más difícil del juego, y luego, que te tocara a ti, así que en cada servidor la tuvo un puñado de jugadores.",
        "Si entras al Monasterio Escarlata con esa espada equipada, los cruzados dejan de atacarte, se giran hacia ti y se arrodillan.",
        "Y si llegas a la Catedral, el espíritu de Alexandros Mograine, el dueño original de la espada, habla a través de la hoja.",
        "Se dirige al comandante de la Catedral, el mismo Mograine que Melenablanca resucitaba una y otra vez, porque ese comandante es su hijo, Renault.",
        "Renault traicionó a su propio padre, lo mató con su propia espada, y esa traición fue la que corrompió la Ashbringer.",
        "Así que el comandante que tumbaste decenas de veces a nivel treinta y tantos era el villano de la historia más grande de la Luz, y lo tenías delante sin saberlo.",
        "Y en Forever, si el contenido llega como en Classic, la espada y su secreto vuelven a estar ahí.",
    ]},
    {"id": "cierre", "frases": [
        "Y esas son las sesenta y dos curiosidades de los Reinos del Este.",
        "Si me quedo con una idea, es que este continente estaba lleno de pistas desde el primer día, el portal apagado, la muralla de Gilneas, las estatuas del valle y el demonio junto a Sylvanas.",
        "En Forever vuelves a pisar todo esto desde nivel uno, así que dime en los comentarios cuál de estas vas a ir a buscar primero.",
        "Al final, en Azeroth, lo más difícil no es tumbar a Ragnaros, es convencer a una gallina de que te dé una misión.",
    ]},
]
