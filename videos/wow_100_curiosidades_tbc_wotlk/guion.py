# -*- coding: utf-8 -*-
"""GUION · 100 curiosidades, secretos y easter eggs de Burning Crusade y Wrath que puedes ir a ver (Crónicas de Warcraft,
motor SECUENCIA YT, ~48-50 min). Flujo y reglas: docs/estilo_secuencia_yt.md · estilo «gema» (cuenta regresiva, chistes secos).

Pedido del usuario (23-oct-2026): «100 curiosidades que no sabíamos de TBC + WotLK que podemos visitar o comprobar en el mapa,
mostrando lugares», mínimo 45 minutos; luego: «agrégale Easter eggs y secretos».
Orden (decisión de Claude, para que los MAPAS CON RUTA cuenten un viaje): cuenta regresiva 100 → 1 recorriendo las zonas en
orden geográfico: Terrallende (100-61) → Quel'Thalas, islas draenei, Karazhan y Cavernas (60-51) → Rasganorte (50-1), de la
Tundra Boreal a la Corona de Hielo. La n.º 1 no es un lugar: es una persona (Bridenbrad). Cada curiosidad dice DÓNDE pararse.
Contexto (web, 23-oct-2026): los reinos del 20.º aniversario están en Burning Crusade durante 2026 y Wrath se espera en 2027
(Blizzard Watch, abr-2026); WoW Forever sale el 4-nov-2026. El gancho: todo esto se puede ir a ver hoy (TBC Classic / retail).

Verificado en la web el 23-oct-2026 (warcraft.wiki.gg, Wowpedia, Wowhead):
- Vieja Trabalomas: Kel'Thuzad humano en el camino al norte de Costasur con Helcular; Whitemane, Renault Mograine y Jimmy Vishas
  niños jugando; Herod el abusivo; en la posada se reúnen futuros Escarlata y hablan de la Ashbringer.
- Salón Púrpura: portal en la planta baja de la Ciudadela Violeta → salón en lo alto. Refugio de Vargoth: sala aparte, solo con
  el libro «Las escuelas de magia arcana: Maestría» del logro Educación Superior (Higher Learning).
- Griftah: Ciudad Baja; exiliado una temporada, vendía en la entrada suroeste con Jadaar y Asric vigilándolo; readmitido en 2.3.
- Costa Olvidada: fantasmas de la Primera Legión; Orik Trueheart, elixir de hierba del lodo; «The Forgotten Tale» / «The Truth
  Shall Set Us Free»; no saben que Arthas los traicionó.
- Baron Sablemane: en el Círculo de Sangre (Blade's Edge); cadena «Pay the Baron a Visit» → Gorgrom → «Showdown» (Goc).
- Pozas de Aggonar: la causa de la muerte del señor del foso es desconocida; su sangre vil corrompió el manantial draenei; Aggonis.
- Área 52: debuff «A-52 Neuralyzer» al salir («the flash of light you did not see did not erase your memories»); agentes de traje.
- Estación Toshley: Tosche Station (Star Wars; misión de los convertidores de energía), ataque de bichos de Starship Troopers,
  Smiles O'Byron = Miles O'Brien (Star Trek), francotiradores con frases de los fantasmas de StarCraft.
- Bridenbrad: Vigilia Silenciosa (noreste de la Corona de Hielo); «A Tale of Valor» de Tirion → Alexstrasza, Remulos, A'dal;
  A'dal libera su espíritu para que la Plaga no lo levante. El homenaje a una persona real (hermano de un empleado de Blizzard
  fallecido de cáncer) es conocimiento general del canal; se dice sin nombre.
- Minigob Manabonk: banco de Dalaran, oveja 30 s, se teletransporta; manda por correo la varita «The Mischief Maker» (solo en
  Dalaran); desde 3.1.
- Salas Arrasadas heroico: 80 minutos tras Nethekurse para llegar a Kargath; prisioneros ejecutados si tardas.
- Puerta de Camino (Sholazar): dos interruptores (Percha y Mirador de los Hacedores) → Un'Goro; el Etymidian.
- L70ETC: banda real de empleados de Blizzard; última vez en BlizzCon 2014 (Metallica les cerró). Que tocan en la Taberna Fin del
  Mundo es conocimiento del canal; se dice «cada cierto tiempo», sin horario.
Lo demás es lore conocido (Wowpedia) escrito de memoria y con cautela; nombres es-MX dudosos marcados abajo (⚠) para
comprobarlos en Wowhead es-MX ANTES de la voz (lección de wow_curiosidades_kalimdor).
⚠ es-MX por confirmar: Lodazal Muerto (Dead Mire), El Rondador de las Profundidades (The Lurker Below), Agujero Portátil
(Portable Hole), Puesto Primasol (Sunspring Post), Sangrelodo (Murkblood), Ruedo de Sangre (Ring of Blood) vs Círculo de
Sangre (Circle of Blood), Bastión Señor del Trueno (Thunderlord Stronghold), Vigilia Silenciosa (Silent Vigil), Percha/Mirador
de los Hacedores, Nacidos de la Escarcha (Frostborn), Salón Púrpura, Educación Superior (Higher Learning), Hacedor de Travesuras
(The Mischief Maker), Embate Escarlata (Scarlet Onslaught), Arroyoplata (Silverbrook), Fauces Pardas (Grizzlemaw), Bastión
Vientogarda (Wintergarde Keep), Puerto Embestida (Onslaught Harbor), Cornisa Ámbar (Amber Ledge), Cicatriz Muerta (Dead Scar).
Cifras del borrador (23-oct): 8 877 palabras ≈ 53 min a 0,358 s/palabra; ~420 frases, ninguna > 200 c ni <= 4 palabras.

SIN Overgear (el usuario, 23-oct-2026: «sin overgear está bien, 53 minutos, hazlo entero»); escena borrada antes de la voz.
Música: BANDA SONORA ORIGINAL del juego (regla del canal, 23-oct), un tema por zona (`ZONA_DE` abajo), NUNCA Lyria.
"""

TITULO = "100 curiosidades, secretos y easter eggs de Burning Crusade y Wrath que puedes ir a ver"
ARCHIVO = "wow_100_curiosidades_tbc_wotlk"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
           idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")

# Grafía que lee el TTS (grafías del canal: C:\googleimagenes\FONETICA_CHECKLIST.md; con traducción oficial, se usa esa)
FONETICA = {
    "World of Warcraft Forever": "uórld of uárcraft Foréver", "World of Warcraft": "uórld of uárcraft", "Forever": "Foréver",
    "Blizzard": "Blízard", "BlizzCon": "Blízcon", "Classic": "Clásic", "Azeroth": "Azeróth", "Overgear": "Óverguir",
    "self-play": "sélf pléi", "CRONICAS10": "Crónicas diez", "Burning Crusade": "Bérnin Kruséid", "Wrath": "Raz",
    "Cataclysm": "Cataclísm", "Dragonflight": "Drágonflait", "Warcraft tres": "uárcraft tres", "Metallica": "Metálica",
    # Terrallende
    "Lothar": "Lótar", "Danath Trollbane": "Dánaz Trólbein", "Khadgar": "Kádgar", "Kurdran Wildhammer": "Kúrdran Uáildjamer",
    "Alleria": "Aléria", "Turalyon": "Turálion", "Gul'dan": "Gúldan", "Aggonar": "Agónar", "Aggonis": "Agónis",
    "Telhamat": "Télamat", "Kazzak": "Kásak", "Kil'jaeden": "Kil Yéiden", "Caminante del Destino": "Dúm uóker", "Magtheridon": "Magtéridon",
    "Illidan": "Ilidán", "Kargath": "Kárgaz", "Nethekurse": "Nézekers", "Telredor": "Télredor", "Vashj": "Vash",
    "Esporaggar": "Esporágar", "Auchindoun": "Áukindun", "Murmur": "Mérmer", "Skettis": "Skétis", "Terokk": "Térok",
    "Sha'tari": "Shatári", "Shattrath": "Shátraz", "Haris Pilton": "Járis Pílton", "Gigantique": "Yigantík",
    "Griftah": "Gríftah", "Level Setenta Elite Tauren Chieftain": "Lével Séventi Elít Táuren Chíftein", "Voren'thal": "Vórental",
    "Kael'thas": "Kéltas", "A'dal": "Adál", "Aldor": "Áldor", "Zephyr": "Zéfir", "Oshu'gun": "Oshugún", "Genedar": "Guénedar",
    "Argus": "Árgus", "K'ure": "Kúre", "Garrosh": "Gárrosh", "Grom": "Grom", "Geyah": "Guéya", "Thrall": "Zrál",
    "Corki": "Córki", "Cho'war": "Chóuar", "Gurgthock": "Gúrgzok", "Wodin": "Uódin", "Mogor": "Mógor", "Halaa": "Jalá",
    "Oshu'gun": "Oshugún", "Alamuerte": "Alamuerte", "Sabellian": "Sabélian", "Gruul": "Grúl", "Baron Sablemane": "Báron Séibelmein",
    "Gorgrom": "Górgrom", "Goc": "Goc", "Rexxar": "Réksar", "Misha": "Mísha", "mok'nathal": "mok názal", "Leoroxx": "Leóroks",
    "Ogri'la": "Ogrilá", "apexis": "apéxis", "Simon": "Sáimon", "Vim'gol": "Vímgol", "Toshley": "Tóshli", "Tosche Station": "Tóshi Stéishon",
    "Star Wars": "Star Uórs", "Luke Skywalker": "Luk Skáiuoker", "Starship Troopers": "Stárship Trúpers", "Smiles O'Byron": "Smáils Obáiron",
    "O'Brien": "Obráien", "Star Trek": "Star Trek", "StarCraft": "Stárcraft", "Hombres de Negro": "Hombres de Negro",
    "Ultris": "Últris", "Culuthas": "Culúzas", "Kirin'Var": "Kírin Var", "Kirin Tor": "Kírin Tor", "Vargoth": "Várgoz",
    "Dimensius": "Diménsius", "Saeed": "Saíd", "Karabor": "Kárabor", "Maiev": "Máiev", "Akama": "Akáma",
    "Skyshatter": "Skáishater", "Teron Gorefiend": "Téron Górfiend", "Gorefiend": "Górfiend",
    # Quel'Thalas, islas, Karazhan, Cavernas
    "M'uru": "Múru", "Velen": "Vélen", "Arthas": "Ársas", "Deatholme": "Dézjolm", "Dar'Khan Drathir": "Dárkan Drázir",
    "Sylvanas": "Silvánas", "Harrison Jones": "Járrison Yóns", "Indiana Jones": "Indiána Yóns", "Zul'Aman": "Zul Amán",
    "Uldum": "Úldum", "Draenor": "Dréinor", "Quel'Danas": "Kel Dánas", "Kessel": "Késsel", "Han Solo": "Jan Sólo",
    "Exodar": "Éksodar", "Sironas": "Sirónas", "Karazhan": "Karazán", "Medivh": "Médiv", "Nielas Aran": "Níelas Áran",
    "Oz": "Os", "Romulo": "Rómulo", "Julianne": "Yulián", "Kel'Thuzad": "Kel Zúzad", "Helcular": "Jélcular",
    "Sally Whitemane": "Sáli Uáitmein", "Renault Mograine": "Renó Mográin", "Jimmy Vishas": "Yími Víshas", "Herod": "Jérod",
    # Rasganorte
    "Varok Colmillosauro": "Vórok Colmillosauro", "D. E. H. T. A.": "de, e, hache, te, a", "PETA": "péta", "Lathorius": "Latórius",
    "Hemet Nesingwary": "Jémet Nésinguari", "Nesingwary": "Nésinguari", "Fizzcrank": "Físcrank", "Mechazod": "Mékazod",
    "Keristrasza": "Keristrása", "Coldarra": "Coldárra", "Malygos": "Máligos", "Transitus": "Tránsitus", "Oculus": "Óculus",
    "Taunka'le": "Taunkalé", "taunka": "táunka", "Nafsavar": "Nífelvar", "Ymiron": "Ímiron", "Lordaeron": "Lordéron",
    "Utgarde": "Útgard", "Ingvar": "Íngvar", "Annhylde": "Ánjild", "val'kyr": "válkir", "Agamand": "Ágamand",
    "Alexstrasza": "Alekstrásha", "Galakrond": "Gálakrond", "Naxxramas": "Naksrámas", "Angrathar": "Ángrazar", "Putress": "Pútres",
    "Bolvar": "Bólvar", "Saurfang": "Sáurfang", "Varian": "Várian", "Orik Trueheart": "Órik Trújart", "Mal'Ganis": "Mal Gánis",
    "Muradin Barbabronce": "Múradin Barbabronce", "Muradin": "Múradin", "Abbendis": "Abéndis", "Vordrassil": "Vordrásil",
    "Yogg-Saron": "Yog Sáron", "Ursoc": "Úrsoc", "Gryan Stoutmantle": "Gráian Stáutmantel", "Defias": "Defías", "Arugal": "Árugal",
    "Drakil'jin": "Drakílyin", "Drakkari": "Drakári", "Rhunok": "Rúnok", "Quetz'lun": "Kétslun", "Sseratus": "Serátus",
    "Akali": "Akáli", "Har'koa": "Jarkóa", "Mam'toth": "Mámtoz", "Gymer": "Guímer", "Drakuru": "Drakúru", "Voltarus": "Voltárus",
    "Vladof": "Vládof", "Tharon'ja": "Zarónya", "Drak'Tharon": "Drak Zárón", "Sholazar": "Sholásar", "Un'Goro": "Ungóro",
    "Freya": "Fréya", "Etymidian": "Etimídian", "Loque'nahak": "Lóke nájak", "K tres": "ka tres", "K dos": "ka dos",
    "Brunnhildar": "Brúnjildar", "Hyldnir": "Jíldnir", "Hodir": "Jódir", "Thorim": "Zórim", "Sif": "Sif", "Loken": "Lóken",
    "Ulduar": "Úlduar", "Vyragosa": "Viragósa", "Yorg Stormheart": "Yorg Stórmjart", "Brann": "Bran", "Magni": "Mágni",
    "Forjaz": "Forjaz", "Algalon": "Álgalon", "Mimiron": "Mímiron", "Krasus": "Krásus", "Korialstrasz": "Koriálstras",
    "Rhonin": "Rónin", "Vereesa": "Verísa", "Richard Knaak": "Ríchard Nak", "Minigob Manacapón": "Mínigob Manacapón",
    "Shandaral": "Shándaral", "Archavon": "Árkavon", "Sindragosa": "Sindragósa", "Barean Westwind": "Bérian Uéstuind",
    "Stratholme": "Strázolm", "Tirion": "Tírion", "Uther": "Úzer", "Jaina": "Yéina", "Bridenbrad": "Bráidenbrad",
    "Remulos": "Rémulos", "Número once": "Número ónse",
    "Lady Vashj": "Léidi Vash", "Kessel Run": "Késsel Ran", "Dalaran": "Dálaran", "Mulgore": "Múlgor", "Quel'Thalas": "Kel Zálas",
    "Zul'Drak": "Zul Drak", "Lord Kazzak": "Lord Kásak", "Hibergarde": "Ibergárd", "Kael": "Kéil", "wyvern": "uáivern", "Gelidar": "Guelidár", "Nafsavar": "Náfsavar",
}

# Whisper escribe distinto lo que Remy dice bien (cifras «noventa y ocho» -> 98, Terrallende -> «Terrayende», trol -> «troll»,
# vrykul -> «brikul», Naxxramas -> «Najrama»…): revisado por hyp el 24-oct con un filtro de nombres/cifras, sin oír cada toma;
# solo se reescribieron c059_3 («O algo parecido.» suelto) y c084_3 («con pleito» -> «completo»), y se añadió fonética a Kael y wyvern.
CER_MAX_POR_FRASE = {"c060_2": 0.08, "intro_1": 0.03, "c100_0": 0.04, "c100_2": 0.11, "c100_3": 0.03, "c098_0": 0.03, "c096_0": 0.04, "c096_1": 0.05, "c096_3": 0.08, "c095_1": 0.06, "c094_0": 0.04, "c094_1": 0.03, "c094_2": 0.04, "c092_1": 0.04, "c092_3": 0.03, "c091_0": 0.03, "c088_0": 0.07, "c087_2": 0.03, "c086_0": 0.04, "c086_1": 0.03, "c086_3": 0.07, "c085_0": 0.04, "c084_1": 0.05, "c082_0": 0.02, "c082_1": 0.05, "c081_2": 0.04, "c080_0": 0.04, "c080_1": 0.05, "c080_2": 0.03, "c079_1": 0.03, "c079_3": 0.05, "c076_1": 0.04, "c075_0": 0.03, "c075_1": 0.06, "c074_0": 0.04, "c074_1": 0.05, "c074_2": 0.03, "c072_1": 0.02, "c072_2": 0.03, "c071_0": 0.03, "c071_1": 0.07, "c069_2": 0.04, "c068_1": 0.03, "c067_0": 0.03, "c067_3": 0.03, "c064_0": 0.03, "c064_1": 0.04, "c064_2": 0.07, "c063_0": 0.03, "c062_1": 0.06, "c061_2": 0.03, "c059_0": 0.03, "c057_0": 0.03, "c057_1": 0.11, "c056_2": 0.03, "c055_0": 0.05, "c055_1": 0.04, "c055_3": 0.04, "c053_2": 0.05, "c051_1": 0.06, "c051_2": 0.09, "c048_1": 0.03, "c048_2": 0.03, "c047_1": 0.03, "c046_1": 0.03, "c044_0": 0.03, "c044_1": 0.03, "c044_3": 0.04, "c043_0": 0.03, "c043_3": 0.03, "c042_0": 0.05, "c041_2": 0.03, "c041_3": 0.03, "c039_0": 0.05, "c039_1": 0.04, "c038_2": 0.04, "c037_1": 0.03, "c034_0": 0.03, "c034_1": 0.03, "c033_1": 0.05, "c032_2": 0.04, "c031_0": 0.03, "c030_0": 0.03, "c030_1": 0.09, "c029_1": 0.04, "c029_2": 0.05, "c028_1": 0.04, "c027_0": 0.03, "c027_2": 0.03, "c026_1": 0.04, "c025_0": 0.03, "c025_3": 0.05, "c022_0": 0.05, "c019_0": 0.05, "c019_1": 0.06, "c018_2": 0.03, "c018_3": 0.03, "c016_1": 0.04, "c014_0": 0.05, "c014_1": 0.04, "c012_1": 0.04, "c012_2": 0.03, "c012_3": 0.02, "c011_2": 0.04, "c010_1": 0.06, "c008_2": 0.03, "c007_1": 0.06, "c005_1": 0.06, "c005_3": 0.03, "c002_1": 0.03, "c002_2": 0.04, "c001_1": 0.05, "c001_2": 0.02, "cierre_3": 0.03}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo del canal en el sistema viejo)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,           # duración de la transición
    ambiente=0.0,           # el audio del gameplay no se usa (se bajan solo imágenes)
    yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080,
            evitar_canales=["Thraex", "Video Game Collector", "TheLtColonel", "Jansn Benchmarks", "Platinum WoW", "WoWAholics101"]),
    recorte_por={},
)

TRANSICIONES = [("continua", 0.1)] * 110

# Zona de cada curiosidad: la música es la BANDA SONORA ORIGINAL de esa zona (musica_wow.py, un tema por bloque) y el mapa con
# ruta del bloque se arma con estas mismas claves en efectos.py.
_BLOQUES = [
    ("fuego", range(100, 93, -1)), ("zangar", range(93, 89, -1)), ("terokkar", range(89, 82, -1)),
    ("nagrand", range(82, 76, -1)), ("filospada", range(76, 70, -1)), ("tormenta", range(70, 65, -1)),
    ("sombraluna", range(65, 60, -1)), ("quelthalas", range(60, 55, -1)), ("azuremyst", range(55, 53, -1)),
    ("karazhan", range(53, 51, -1)), ("cavernas", range(51, 50, -1)),
    ("boreal", range(50, 44, -1)), ("fiordo", range(44, 41, -1)), ("dragones", range(41, 34, -1)),
    ("pardas", range(34, 30, -1)), ("zuldrak", range(30, 24, -1)), ("sholazar", range(24, 20, -1)),
    ("cumbres", range(20, 13, -1)), ("dalaran", range(13, 8, -1)), ("invierno", range(8, 7, -1)), ("corona", range(7, 0, -1)),
]
ZONA_DE = {f"c{n:03d}": z for z, r in _BLOQUES for n in r}
ZONA_DE.update(intro="fuego", cierre="corona")
assert len([k for k in ZONA_DE if k[1:].isdigit()]) == 100

# Ánimo por zona (solo lo usa `musica_wow.py` para elegir tema; Lyria NO se pide en este canal)
_ANIMO_ZONA = {
    "fuego": "fiery and martial, war drums", "zangar": "wet, glowing, mysterious", "terokkar": "sacred, hushed, city of light",
    "nagrand": "open plains, warm and nostalgic", "filospada": "harsh mountain, ogres and giants", "tormenta": "arcane, electric, strange",
    "sombraluna": "dark, volcanic, demonic", "quelthalas": "elven, elegant, melancholic", "azuremyst": "crystalline, hopeful",
    "karazhan": "haunted mansion, eerie", "cavernas": "timeless, wistful", "boreal": "cold wind, marching", "fiordo": "nordic, horns, longships",
    "dragones": "solemn, bones in the snow", "pardas": "rustic, hunting horn, pines", "zuldrak": "troll drums, ruined ziggurats",
    "sholazar": "lush jungle, titan machinery", "cumbres": "giant storms, thunder, awe", "dalaran": "arcane city, violet, playful",
    "invierno": "siege drums", "corona": "frozen citadel, dread and grief",
}
LYRIA = dict(
    estilo="(NO SE USA: música original del juego, docs/musica_biblioteca.md § canales de videojuegos)",
    escenas={k: (_ANIMO_ZONA[z], 4) for k, z in ZONA_DE.items()},
    tramos=[],   # se escriben en la sesión 2 con la línea de tiempo real de `tiempo` (<= 175 s cada uno; ~18 tramos para 50 min)
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "Cien lugares, dos expansiones y una sola regla: todo lo que te voy a contar lo puedes ir a ver con tus propios pies, o con tu propia montura voladora.",
        "Terrallende y Rasganorte están llenos de secretos que pasaste corriendo rumbo al siguiente signo de exclamación.",
        "Una ciudad que dejó un cráter al mudarse, un enano que todo el mundo cree muerto, una banda de empleados de Blizzard tocando en una taberna.",
        "Y un goblin que te borra la memoria al salir del pueblo.",
        "Vamos a recorrer las dos expansiones zona por zona, del Portal Oscuro al Trono Helado, y en cada parada te digo exactamente dónde pararte.",
        "Son cien, así que ponte cómodo. Y espera al número uno, porque no es un lugar: es una persona.",
    ]},
    # ───────── TERRALLENDE · Península del Fuego Infernal (100-94) ─────────
    {"id": "c100", "frases": [
        "Número cien. El Bastión del Honor es la base más vieja de la Alianza en Terrallende, y lleva veinte años esperando refuerzos.",
        "La fundaron los Hijos de Lothar, la expedición que cruzó el Portal Oscuro al final de la Segunda Guerra y se quedó atrapada cuando el portal se cerró.",
        "Su comandante, Danath Trollbane, sigue ahí; Khadgar te espera en Shattrath, y Kurdran Wildhammer en el Valle Sombraluna, con sus grifos.",
        "De los cinco héroes que cruzaron, dos no aparecen por ningún lado: Alleria y Turalyon. En Ventormenta tienen estatua, y en Terrallende, nada.",
    ]},
    {"id": "c099", "frases": [
        "Número noventa y nueve. El camino que va del Portal Oscuro a la Ciudadela del Fuego Infernal se llama Camino de la Gloria, y está pavimentado con huesos.",
        "La Horda de Gul'dan lo construyó con los restos de los draenei que masacró, para que cada guerrero orco marchara sobre su victoria.",
        "Bájate de la montura y mira el suelo: las calaveras y las costillas están modeladas una por una.",
        "Es la primera carretera de la expansión, y nadie la ve, porque todos van viendo el mapa.",
    ]},
    {"id": "c098", "frases": [
        "Número noventa y ocho. En la Península del Fuego Infernal hay algo que escuchas antes de verlo: el Segador vil.",
        "Es una máquina de la Legión del tamaño de una casa que patrulla el centro de la zona, y sus pasos suenan a cientos de metros.",
        "Si lo ves aparecer en el horizonte y estás a nivel sesenta, ya es tarde; con un golpe te manda al cementerio.",
        "Hoy sigue ahí, patrullando el mismo circuito que en dos mil siete, como un guardia de seguridad al que nadie ha ido a relevar.",
    ]},
    {"id": "c097", "frases": [
        "Número noventa y siete. Las Pozas de Aggonar eran un manantial sagrado de los draenei, hasta que un señor del foso se murió encima.",
        "Aggonar cayó ahí, nadie sabe cómo, y su sangre vil envenenó el agua; sus huesos siguen en medio de las pozas, enormes.",
        "Los draenei del Templo de Telhamat te mandan a limpiarlas, y lo que sale del fondo es Aggonis, lo que quedó de su esencia.",
        "Ve a verlo: es uno de los pocos jefes de misión que literalmente nació de un charco.",
    ]},
    {"id": "c096", "frases": [
        "Número noventa y seis. Lord Kazzak se mudó. En Classic vivía en las Tierras Devastadas, y en Burning Crusade apareció en lo alto del Trono de Kil'jaeden.",
        "Es la montaña del norte de la península donde la Legión abrió su puerta a Terrallende, y Kazzak la vigila como jefe de mundo, con título nuevo.",
        "Sube con montura voladora y lo ves ahí, esperando a cuarenta personas que ya no van.",
        "Su colega Caminante del Destino hace lo mismo frente al Templo Oscuro; luego pasamos a saludarlo.",
    ]},
    {"id": "c095", "frases": [
        "Número noventa y cinco. Debajo de la Ciudadela del Fuego Infernal hay un señor del foso encadenado, y la Horda de Illidan lo usa como refinería.",
        "Magtheridon gobernó Terrallende hasta que Illidan lo derrotó y lo colgó de cadenas en su propia fortaleza.",
        "Su sangre gotea a los barriles del Horno de Sangre, y con ella los orcos de la Mano Arrasada se convierten en orcos viles rojos.",
        "Puedes entrar a verlo encadenado en su guarida, y si llevas veinticuatro amigos, soltarlo un rato.",
    ]},
    {"id": "c094", "frases": [
        "Número noventa y cuatro. Las Salas Arrasadas en heroico tienen un reloj que nadie te explica: una hora y veinte para llegar a Kargath Puño Maldito.",
        "Cuando cae el brujo Nethekurse empieza la cuenta, y al fondo hay prisioneros de tu facción esperando al verdugo.",
        "Cada tanto Kargath grita que va a ejecutar a otro, y lo cumple; si llegas tarde, te encuentras los cuerpos.",
        "Es la única mazmorra de la expansión donde perder el tiempo mata a alguien que no eres tú.",
    ]},
    # ───────── Marisma de Zangar (93-90) ─────────
    {"id": "c093", "frases": [
        "Número noventa y tres. En la Marisma de Zangar no hay árboles: lo que parecen árboles son hongos de cuarenta metros.",
        "Y los draenei construyeron un pueblo entero encima de uno de ellos, Telredor, al que se sube en un elevador.",
        "Desde arriba se ve toda la marisma, con las esporas flotando y los hongos gigantes brillando de azul por la noche.",
        "Es la única capital de zona a la que llegas por ascensor, y no, no se puede saltar; ya lo intentó medio servidor.",
    ]},
    {"id": "c092", "frases": [
        "Número noventa y dos. Al este de la marisma hay un lago que ya no existe, el Lodo Muerto, y es un adelanto de lo que iba a pasar con toda la zona.",
        "Las bombas de vapor de los naga de Lady Vashj drenan el agua hacia el Reserva Colmillo Torcido, y los lagos bajan a la vista.",
        "Los druidas de la Expedición Cenarion miden el nivel del agua en misiones, y tú vas a sabotear las bombas una por una.",
        "El Lodo Muerto sigue seco hoy; era la parte de la marisma que Vashj ya había terminado.",
    ]},
    {"id": "c091", "frases": [
        "Número noventa y uno. Esporaggar es el único pueblo de Terrallende donde la población son hongos que caminan y hablan.",
        "Los esporelines te piden ayuda contra los lores del lodo, y subir reputación con ellos tiene premio: una mascota murcielespora diminuta.",
        "Hablan en una especie de balbuceo, te llaman amigo, y son los únicos vecinos de la marisma que no quieren matarte.",
        "Está escondido al oeste, detrás de los hongos más grandes; la mitad de los jugadores no lo pisó jamás.",
    ]},
    {"id": "c090", "frases": [
        "Número noventa. La entrada del Reserva Colmillo Torcido está bajo el agua, en medio del Lago Serpiente.",
        "Tienes que bucear hasta el fondo y meterte por una tubería enorme que te escupe en el vestíbulo de las mazmorras.",
        "Y adentro, en la Caverna Santuario Serpiente, el segundo jefe no se busca: se pesca.",
        "El Rondador de abajo sale si lanzas la caña en un estanque extraño frente a su plataforma; es el único jefe de banda que ha mordido un anzuelo.",
    ]},
    # ───────── Bosque de Terokkar y Shattrath (89-83) ─────────
    {"id": "c089", "frases": [
        "Número ochenta y nueve. Auchindoun era la ciudad de los muertos de los draenei, hasta que el Consejo de la Sombra la hizo explotar desde adentro.",
        "Los brujos de Gul'dan invocaron a Murmur, una esencia de puro sonido, y la onda expansiva arrancó el bosque de alrededor.",
        "Por eso los Yermos de Hueso son blancos y planos: son el cráter, y lo que cruje bajo tus pies son restos de la ciudad.",
        "Hoy Auchindoun son cuatro mazmorras en un hoyo, y Murmur sigue al fondo del Laberinto de las Sombras.",
    ]},
    {"id": "c088", "frases": [
        "Número ochenta y ocho. Skettis, la ciudad de los arakkoa, está en las copas de los árboles del sur de Terokkar, y sin montura voladora no existe.",
        "Fue la primera zona del juego hecha exclusivamente para gente con alas, con misiones diarias de la Guardia del Cielo Sha'tari.",
        "Ahí vive la sombra de Terokk, el rey arakkoa, al que invocas en una cima con un ritual y unos cuantos amigos.",
        "Si subiste de nivel a pie, pasaste debajo de una ciudad entera sin verla.",
    ]},
    {"id": "c087", "frases": [
        "Número ochenta y siete. En la Taberna del Fin del Mundo de Shattrath hay una elfa de sangre que vende una bolsa de veintidós espacios por mil doscientas monedas de oro.",
        "Se llama Haris Pilton, con sus perritos, sus lentes oscuros y la socialité en el nombre, y la bolsa se llama, textualmente, Bolsa gigantesca, con comillas.",
        "En Wrath subió la apuesta: una bolsa de veinticuatro espacios por diez mil monedas de oro.",
        "La gente lo compraba, igual que la gente real compraba lo otro. La parodia estaba completa.",
    ]},
    {"id": "c086", "frases": [
        "Número ochenta y seis. En el Bajo Arrabal de Shattrath hay un trol que vende amuletos milagrosos, y todos son basura.",
        "Griftah ofrece el jabón con cuerda y collares que prometen protegerte de cosas que no existen, y el texto de cada uno lo admite si lo lees.",
        "Lo echaron de la ciudad una temporada por estafador; siguió vendiendo en la entrada, con un guardia revisándole la mercancía.",
        "Volvieron a dejarlo entrar en el parche dos punto tres. Sigue ahí, con la misma sonrisa, y la gente le sigue comprando.",
    ]},
    {"id": "c085", "frases": [
        "Número ochenta y cinco. En la misma taberna de Shattrath toca una banda de metal formada por empleados de Blizzard.",
        "Se llaman Level Setenta Elite Tauren Chieftain: cinco músicos de la Horda, con sus instrumentos y su show de luces, en un escenario de taberna.",
        "La banda existe de verdad; tocaron en cada BlizzCon hasta que Metallica les cerró el show en dos mil catorce.",
        "Espera un rato junto al escenario de la Taberna del Fin del Mundo y los ves salir a tocar, con público de elfos borrachos.",
    ]},
    {"id": "c084", "frases": [
        "Número ochenta y cuatro. En Shattrath tienes que elegir bando, y el bando de los elfos de sangre existe por una visión.",
        "Voren'thal el Vidente desertó de Kael'thas con sus magos y se rindió ante A'dal, el naaru, porque soñó que su destino estaba en Shattrath.",
        "Los draenei del Aldor no les creen ni una palabra, y cuando te unes a uno, el otro te ve como traidor para siempre.",
        "Las dos facciones viven en terrazas opuestas de la misma ciudad, mirándose desde arriba, como vecinos de un edificio que llevan años peleados.",
    ]},
    {"id": "c083", "frases": [
        "Número ochenta y tres. Junto a A'dal hay un elfo de sangre discreto llamado Zephyr que vende viajes en el tiempo.",
        "Si los Vigilantes del Tiempo te respetan lo suficiente, te teletransporta directo a las Cavernas del Tiempo, en Tanaris, al otro lado del universo.",
        "Es la agencia de viajes más exclusiva del juego, y la mayoría pasó a su lado mil veces sin hablarle.",
        "Luego lo vamos a usar: las Cavernas también guardan un secreto de esta lista.",
    ]},
    # ───────── Nagrand (82-77) ─────────
    {"id": "c082", "frases": [
        "Número ochenta y dos. La montaña de cristal de Nagrand, Oshu'gun, no es una montaña: es una nave espacial.",
        "Es la Genedar, la nave con la que los draenei huyeron de Argus, estrellada hace siglos, y dentro agoniza K'ure, uno de los naaru que la pilotaba.",
        "Los orcos la tenían por sagrada porque ahí hablaban con sus ancestros; en realidad era la energía del naaru moribundo.",
        "Puedes entrar: hay una grieta en la base y un pasillo que baja hasta el corazón de la nave.",
    ]},
    {"id": "c081", "frases": [
        "Número ochenta y uno. En Garadar, el pueblo de los orcos marrones, hay un orco joven deprimido sentado en una choza: Garrosh Grito Infernal.",
        "Se avergüenza de ser hijo de Grom, porque cree que su padre solo fue el primero en beber la sangre del demonio.",
        "La Gran Madre Geyah, la abuela de Thrall, lo cuida, y cuando terminas la zona, Thrall en persona viene a contarle cómo murió Grom.",
        "Esa escena es el origen de todo lo que Garrosh hizo después; y lo vas a ver en la Tundra Boreal, muy cambiado.",
    ]},
    {"id": "c080", "frases": [
        "Número ochenta. Corki es un niño orco de Garadar al que secuestran tres veces en la misma zona.",
        "Primero lo tienen los Sangrelodo en el Puesto Primasol, luego los ogros en la Colina Mazo de Guerra, y luego otro ogro, Cho'war.",
        "La misión de la tercera se llama, literalmente, Corki desapareció otra vez.",
        "Lo rescatas, vuelve a casa, y la siguiente vez que pasas ya no está. Nagrand tenía un problema de supervisión infantil.",
    ]},
    {"id": "c079", "frases": [
        "Número setenta y nueve. En el norte de Nagrand hay un pozo de peleas con un goblin promotor que te va a seguir el resto de tu vida.",
        "Gurgthock organiza combates en un pozo con su ayudante Wodin, y la pelea final es contra Mogor, el ogro que grita que te va a hacer puré.",
        "Vuelve en Zul'Drak con el Anfiteatro de la Angustia, luego en las Tierras Altas Crepusculares, luego en la Hermandad de Camorristas.",
        "Es el único empresario de Azeroth con sucursales en tres expansiones; de pequeño emprendedor, nada.",
    ]},
    {"id": "c078", "frases": [
        "Número setenta y ocho. Nagrand tiene dos lugares a los que, sin montura voladora, simplemente no se puede llegar.",
        "La Meseta Elemental, al norte, donde los elementales sueltan las motas que medio servidor granjeaba para vender.",
        "Y la Cordillera del Crepúsculo, al oeste, un pedazo de tierra flotante con dos campamentos de la Legión y sus hornos de forja.",
        "Si subiste de nivel a pie, en tu mapa hay dos manchas que nunca se iluminaron.",
    ]},
    {"id": "c077", "frases": [
        "Número setenta y siete. Halaa es un pueblo en una isla flotante que cambia de dueño varias veces al día, y se conquista bombardeando desde un wyvern.",
        "El bando que lo controla tiene vendedores, y el otro vuela encima tirando bombas de fuego hasta que los guardias caen.",
        "Las recompensas se pagan en fragmentos de cristal de Oshu'gun y en marcas de batalla, con monturas de talbuk.",
        "Fue el primer pueblo del juego que se gana y se pierde, y en los servidores llenos no tuvo paz jamás.",
    ]},
    # ───────── Montañas Filospada (76-71) ─────────
    {"id": "c076", "frases": [
        "Número setenta y seis. En las Montañas Filospada hay dragones negros clavados en los picos, como mariposas en un corcho.",
        "Alamuerte mandó a su hijo Sabellian con parte de su linaje a Draenor, y los gronn los cazaron uno por uno.",
        "Gruul se ganó el apellido Asesino de Dragones ensartándolos en las agujas de piedra, y ahí siguen los esqueletos, con las alas abiertas.",
        "Vuela despacio sobre la zona y cuéntalos: son más de los que te acuerdas.",
    ]},
    {"id": "c075", "frases": [
        "Número setenta y cinco. En el Círculo de Sangre, un barón humano elegante te pide ayuda contra los gronn, con mucha educación.",
        "Se llama Baron Sablemane, y no es humano ni barón: es Sabellian, el hijo de Alamuerte, en forma mortal.",
        "Quiere venganza por los dragones de los picos, y te usa a ti para matar a Gorgrom el Devoradragones y a Goc.",
        "El juego nunca te lo dice de frente; lo descubres por sus misiones, o muchos años después, cuando volvió en Dragonflight.",
    ]},
    {"id": "c074", "frases": [
        "Número setenta y cuatro. Rexxar, el héroe de Warcraft tres, está sentado en la Bastión Señor del Trueno de las Filospada, con su osa Misha.",
        "Volvió a Terrallende a buscar a su gente, los mok'nathal, mitad orcos y mitad ogros, que viven en una aldea al este.",
        "Su padre, Leoroxx, lo echó de la aldea hace años, y sigue sin querer recibirlo; tú haces de mensajero entre los dos.",
        "El campeón de la Horda de Durotar vive exiliado por su propio padre, en una fortaleza prestada.",
    ]},
    {"id": "c073", "frases": [
        "Número setenta y tres. En lo alto de las Filospada hay ogros que meditan, hablan con calma y resuelven acertijos: Ogri'la.",
        "Los cristales apexis de la meseta los volvieron inteligentes, y para ganarte su confianza juegas con reliquias apexis a un juego de luces de colores.",
        "Es, exactamente, un Simon: cuatro luces, una secuencia, y si fallas, te electrocuta.",
        "Fue la primera vez que el juego metió un juguete de los ochenta como misión diaria.",
    ]},
    {"id": "c072", "frases": [
        "Número setenta y dos. Cerca de Ogri'la hay un círculo de runas en el que no pasa nada, hasta que cinco personas se paran una en cada runa al mismo tiempo.",
        "Entonces aparece Vim'gol el Vil, un demonio enorme, y hay que matarlo antes de que termine su ritual.",
        "No hay letrero, ni guía, ni pista: lo descubres si lees la misión de los ogros o si tienes amigos.",
        "Es uno de los pocos secretos del juego que exige cinco jugadores de carne y hueso parados en el lugar correcto.",
    ]},
    {"id": "c071", "frases": [
        "Número setenta y uno. Estación de Toshley, el puesto de los gnomos en las Filospada, es un homenaje a todas las películas del espacio a la vez.",
        "Toshley es la Tosche Station de Star Wars, y una misión se llama Recoger unos convertidores de energía, la frase de Luke Skywalker.",
        "Los bichos que atacan el campamento son el ataque de Starship Troopers, y el ingeniero Smiles O'Byron es el jefe O'Brien de Star Trek.",
        "Los francotiradores dicen frases de los fantasmas de StarCraft; los gnomos nunca supieron hacer una base sin referencias.",
    ]},
    # ───────── Tormenta Abisal (70-66) ─────────
    {"id": "c070", "frases": [
        "Número setenta. Si sales de Área cincuenta y dos a pie, un destello te pega en la cara y te deja un efecto llamado Neuralizador A cincuenta y dos.",
        "El texto dice: el destello de luz que no viste no te borró la memoria. Es el neuralizador de Hombres de Negro.",
        "Los agentes de la zona van de traje negro con lentes oscuros, y el nombre del pueblo es el Área cincuenta y uno, más uno.",
        "Es el chiste mejor escondido de la expansión, porque la mayoría salió del pueblo volando y nunca lo vio.",
    ]},
    {"id": "c069", "frases": [
        "Número sesenta y nueve. En la Tormenta Abisal hay burbujas verdes con bosque adentro, en medio de un desierto púrpura.",
        "Son los ecodomos, construidos por los etéreos del Protectorado para salvar los últimos animales de Draenor mientras el continente se deshace.",
        "Adentro hay talbuks, ciervos y hasta un bosque; afuera, la nada, flotando en el Vacío Abisal.",
        "Son los únicos zoológicos de Azeroth, y los cuidan unos seres de vendas y energía que ni siquiera son de este planeta.",
    ]},
    {"id": "c068", "frases": [
        "Número sesenta y ocho. Una de las forjas de maná de Kael'thas explotó, y lo que dejó es un agujero al Vacío.",
        "La Forja de Maná Ultris saltó por los aires, y en el cráter flotan criaturas del Vacío y un gigante llamado Culuthas.",
        "Las otras siguen bombeando energía del Vacío Abisal para la flota de Kael, y tú las vas apagando una por una.",
        "Ultris es el aviso de qué pasa cuando un príncipe elfo chupa demasiado del enchufe.",
    ]},
    {"id": "c067", "frases": [
        "Número sesenta y siete. En el Poblado Kirin'Var, un pueblo de magos de Dalaran destruido por Kael'thas, los habitantes siguen ahí, fantasmas.",
        "Vagan entre las casas quemadas, y en la Torre Violeta queda vivo un solo mago, el Archimago Vargoth, encerrado por una maldición.",
        "Te habla a través de una imagen, y de premio te da su bastón, que invoca su copia donde quieras, para que te dé consejos no pedidos.",
        "Vargoth vuelve en Wrath, en Dalaran, y ahí también lo vamos a encontrar.",
    ]},
    {"id": "c066", "frases": [
        "Número sesenta y seis. En la Tormenta Abisal flota una esfera negra del tamaño de una fortaleza que se está comiendo todo.",
        "Es Dimensius el Devoratodo, un dios del Vacío, y los etéreos del Protectorado te reclutan en un escuadrón para enfrentarlo.",
        "El Capitán Saeed te lleva marchando con su tropa hasta el lugar, y la batalla es contra una cosa que no tiene cara ni cuerpo.",
        "Fue el primer señor del Vacío del juego, mucho antes de que el Vacío se volviera la trama principal.",
    ]},
    # ───────── Valle Sombraluna (65-61) ─────────
    {"id": "c065", "frases": [
        "Número sesenta y cinco. En el Valle Sombraluna hay un volcán con forma de mano abierta, y se llama Mano de Gul'dan.",
        "Gul'dan usó la Cifra de la Condena para separar a los orcos de los elementos, y la tierra respondió abriéndose en una erupción con forma de garra.",
        "Desde entonces el valle es ceniza, y el volcán sigue escupiendo elementales de fuego furiosos.",
        "Desde el aire la forma de los dedos es perfecta; es el letrero más grande de Draenor, y dice quién tuvo la culpa.",
    ]},
    {"id": "c064", "frases": [
        "Número sesenta y cuatro. El Templo Oscuro no lo construyeron Illidan ni la Horda: es el Templo de Karabor, el lugar más sagrado de los draenei.",
        "La Horda lo tomó, luego Magtheridon, y al final Illidan se sentó en la cima a gritar que no estás preparado.",
        "Y en la puerta, afuera, patrulla Caminante del Destino, un jefe de mundo mecánico que mata a todo el que llega sin banda.",
        "Puedes ir a verlo hoy: sigue custodiando una entrada por la que ya nadie necesita pasar.",
    ]},
    {"id": "c063", "frases": [
        "Número sesenta y tres. Maiev Cantosombrío, la guardiana que persiguió a Illidan diez mil años, está presa en una jaula del Valle Sombraluna.",
        "Akama y sus Lengua de Ceniza la mantienen en la Jaula de la Guardiana, y tú puedes bajar a hablar con ella.",
        "Te dice, con la humildad de siempre, que ella sola bastaba, y que necesita que la liberen para terminar el trabajo.",
        "Al final del Templo Oscuro aparece a ayudarte contra Illidan y se queda con la última palabra.",
    ]},
    {"id": "c062", "frases": [
        "Número sesenta y dos. En el Arrecife del Ala Abisal, al sur del valle, te disfrazan de orco Faucedraco y te ponen a trabajar para el enemigo.",
        "Las diarias incluyen una carrera aérea contra los pilotos de los Faucedraco, con el Capitán Skyshatter de jefe final.",
        "Si subes la reputación hasta exaltado, los dragones del Ala Abisal te regalan uno de los suyos como montura.",
        "Y en la ceremonia final aparece Illidan en persona, y todos los orcos descubren que eras tú el espía.",
    ]},
    {"id": "c061", "frases": [
        "Número sesenta y uno. Hay una misión en el Valle Sombraluna en la que no juegas tú: juegas como Teron Gorefiend.",
        "El espíritu del primer caballero de la muerte te pide que recuperes sus reliquias, y al final te posee para matar a un dragón.",
        "Lo haces, con sus poderes, sintiéndote invencible, y en cuanto terminas, Gorefiend se va libre a servir a Illidan.",
        "Acabas de resucitar a un jefe del Templo Oscuro con tus propias manos; luego lo pagas en la banda.",
    ]},
    # ───────── Quel'Thalas e Isla de Quel'Danas (60-56) ─────────
    {"id": "c060", "frases": [
        "Número sesenta. Debajo de Lunargenta, en la sede de los Caballeros de Sangre, hay un ángel encadenado, y los paladines le exprimen la Luz.",
        "Kael'thas capturó al naaru M'uru en el Castillo de la Tempestad y lo mandó a su ciudad como regalo para su nueva orden.",
        "Durante toda la expansión puedes bajar a verlo, con su luz apagándose, hasta que en el parche dos punto cuatro Kael lo roba de vuelta.",
        "Su corazón acaba en manos de Velen, y con él se vuelve a encender la Fuente del Sol; el prisionero resultó ser el remedio.",
    ]},
    {"id": "c059", "frases": [
        "Número cincuenta y nueve. Hay una franja de tierra muerta que cruza Quel'Thalas de sur a norte, y es la huella de un ejército.",
        "La Cicatriz Muerta es el camino que siguió Arthas con la Plaga hasta la Fuente del Sol, y en veinte años no ha crecido ni una hoja.",
        "Puedes caminarla completa, de las Tierras Fantasma a Lunargenta, con los no-muertos todavía arrastrándose en fila.",
        "En el extremo sur está la Ciudad de la Muerte, donde Dar'Khan Drathir, el mago que vendió la ciudad a Arthas, sigue vivo, o algo parecido.",
    ]},
    {"id": "c058", "frases": [
        "Número cincuenta y ocho. En las Tierras Fantasma están las ruinas de la Aguja Brisaveloz, la casa de Sylvanas, y hay algo suyo tirado en el suelo.",
        "Un collar, el collar de la Dama, que una aparición te entrega, y la misión te manda a llevárselo a Entrañas.",
        "Cuando se lo das, Sylvanas se queda callada, aparecen los espíritus de su familia y canta el Lamento de los Altonato.",
        "Es la única vez en todo el juego que la Reina Alma en Pena canta, y empieza en una torre en ruinas que casi nadie visita.",
    ]},
    {"id": "c057", "frases": [
        "Número cincuenta y siete. Harrison Jones, el Indiana Jones de Azeroth, debutó en Zul'Aman, golpeando un gong en la puerta.",
        "Llegó en el parche dos punto tres, con su sombrero y su látigo, y es quien abre la banda de los trols amani.",
        "Después lo encuentras en las Colinas Pardas, en Uldum y en Draenor, siempre a punto de perder el sombrero.",
        "Su siguiente parada está en esta misma lista; es un hombre con el pasaporte muy sellado.",
    ]},
    {"id": "c056", "frases": [
        "Número cincuenta y seis. La Isla de Quel'Danas fue la primera vez que un servidor entero tuvo que construir algo entre todos.",
        "La Ofensiva Sol Devastado abría vendedores, un portal y una posada conforme el servidor completaba misiones diarias; los servidores lentos vivieron semanas sin tienda.",
        "Y en la Bancal del Magister está Kael'thas, con su frase inmortal: el Castillo de la Tempestad fue solo un contratiempo.",
        "Lo dice después de que ya lo mataste una vez. Hay gente que no sabe perder.",
    ]},
    # ───────── Islas draenei (55-54) ─────────
    {"id": "c055", "frases": [
        "Número cincuenta y cinco. En la Isla Bruma Azur hay un draenei llamado Kessel que te pide hacer, textualmente, la Carrera de Kessel.",
        "Te monta en un elekk en la Encrucijada de Kessel y te manda a avisar a tres aldeas de un ataque; el chiste es Han Solo presumiendo su Kessel Run.",
        "Y toda la isla está regada de pedazos de nave, porque el Exodar no es una ciudad: es un ala del Castillo de la Tempestad que se estrelló.",
        "Si entras al Castillo en Terrallende, los pasillos son idénticos a los de la capital draenei.",
    ]},
    {"id": "c054", "frases": [
        "Número cincuenta y cuatro. La Isla Bruma de Sangre es roja porque está irradiada.",
        "Los cristales de la Espiral Vectorial, el pedazo de nave que cayó ahí, envenenaron el agua, la tierra y a los animales.",
        "Los elfos de sangre de Sironas aprovechan la radiación para sus experimentos, y tú vas a bajarles la luz.",
        "Es la única zona inicial del juego en la que el color del paisaje es una advertencia sanitaria.",
    ]},
    # ───────── Karazhan (53-52) ─────────
    {"id": "c053", "frases": [
        "Número cincuenta y tres. En Karazhan, el fantasma que te prohibía moverte con su círculo de fuego es el papá de Medivh.",
        "La Sombra de Aran es Nielas Aran, el mago de la corte de Ventormenta que engendró al Guardián, encerrado en la biblioteca de su propio hijo.",
        "Y en el teatro de la torre se representa una obra al azar: el Mago de Oz, Caperucita Roja, o Romulo y Julianne.",
        "Sube a la Terraza del Maestro al final: desde ahí Medivh miraba el cielo mientras planeaba abrir el Portal Oscuro.",
    ]},
    {"id": "c052", "frases": [
        "Número cincuenta y dos. Detrás de Karazhan, en el cementerio, hay una cripta con la puerta cerrada que nunca se abrió oficialmente.",
        "Adentro, y esto lo conocemos por la gente que entró con trucos, hay salas con cadáveres colgados de los pies dentro del agua: los pecadores invertidos.",
        "También hay una cámara de huesos y pasillos sin salida; Blizzard la construyó completa y nunca la usó.",
        "La puerta se ve desde afuera, en el Paso de la Muerte; es el lugar más perturbador del juego y está a unos metros de la entrada de la banda.",
    ]},
    # ───────── Cavernas del Tiempo (51) ─────────
    {"id": "c051", "frases": [
        "Número cincuenta y uno. En las Cavernas del Tiempo, las Antiguas Laderas de Trabalomas te dejan ver Costasur antes de la Plaga, con sus vecinos famosos.",
        "Por el camino del norte camina un humano llamado Kel'Thuzad, todavía vivo, acompañado por el nigromante Helcular.",
        "Y en el pueblo juegan tres niños: Sally Melenablanca, Renault Mograine y el pequeño Jimmy Vishas, con Herod el abusivo rondando.",
        "Son los futuros jefes del Monasterio Escarlata jugando a las escondidas; el juego te enseña a los villanos cuando todavía eran niños.",
    ]},
    # ───────── RASGANORTE · Tundra Boreal (50-45) ─────────
    {"id": "c050", "frases": [
        "Número cincuenta. En el Bastión Grito de Guerra de la Tundra Boreal manda un orco que acabamos de ver llorando en Nagrand.",
        "Garrosh Grito Infernal llegó a Rasganorte como señor supremo de la expedición de la Horda, y ya no se avergüenza de nada.",
        "Le grita a Varok Colmillosauro, el veterano que trató de contenerlo, y manda a cargar contra la Alianza antes que contra la Plaga.",
        "Entre un pueblo y el otro hay una expansión de distancia, y es la mejor forma de ver cómo se fabrica un tirano.",
    ]},
    {"id": "c049", "frases": [
        "Número cuarenta y nueve. En la Tundra Boreal hay un campamento de druidas que persigue cazadores, y se llama D. E. H. T. A.",
        "Druidas por el Trato Ético y Humano de los Animales: la parodia de PETA, con el Archidruida Lathorius al frente.",
        "Sus misiones te mandan a liberar mamuts de las trampas, matar cazadores y recoger sus orejas, lo cual es muy ético.",
        "El enemigo es la expedición de Hemet Nesingwary, que puso su campamento al otro lado del continente; ahí también vamos.",
    ]},
    {"id": "c048", "frases": [
        "Número cuarenta y ocho. En la Pista de Aterrizaje de Palanqueta, un robot enorme te cuenta de dónde vienen los gnomos de verdad.",
        "El Maestro de Engranajes Mechazod se activa en los géiseres y explica que los gnomos eran mecagnomos, máquinas de los titanes, hasta que la Maldición de la Carne los volvió de carne.",
        "Mechazod ofrece curarlos, es decir, convertirlos otra vez en robots, y los gnomos de la pista dicen que gracias, pero no.",
        "Fue el primer lugar donde el juego confirmó que el origen de una raza entera era una avería.",
    ]},
    {"id": "c047", "frases": [
        "Número cuarenta y siete. Keristrasza, la dragona roja que te ayuda en toda la cadena de Gelidar, termina siendo un jefe que tú mismo matas.",
        "Ella pelea contigo contra el azul Malygos, hasta que él la captura y la congela como su consorte, dentro del Nexo.",
        "Cuando entras a la mazmorra, el último jefe es ella, pidiendo que la liberes de la única manera posible.",
        "Es la misión más triste de la tundra, y la mayoría la hizo apurada para subir de nivel.",
    ]},
    {"id": "c046", "frases": [
        "Número cuarenta y seis. La isla de Gelidar tiene un puente que no se ve: el Escudo de Tránsito.",
        "Los magos de Kirin Tor levantaron un campamento mágico oculto frente al Nexo de Malygos, y la entrada es un portal en el Saliente Ámbar.",
        "Desde ahí se ve la Guerra del Nexo: Malygos robando la magia del mundo con sus anillos, los dragones rojos y azules peleando en el aire.",
        "Y adentro de la isla están el Nexo, el Oculus y el Ojo de la Eternidad; tres instancias en una roca del tamaño de un pueblo.",
    ]},
    {"id": "c045", "frases": [
        "Número cuarenta y cinco. En el Poblado Taunka'le viven los primos de los tauren que se quedaron en el frío, y son otra cosa.",
        "Los taunka tienen el pelaje más denso, el carácter más duro y una filosofía distinta: no piden permiso a los espíritus, los doblegan.",
        "Son parientes de los tauren de Mulgore, separados hace milenios, y ni unos ni otros sabían que los otros existían.",
        "Se unen a la Horda en Rasganorte con un juramento de sangre, y son los únicos vecinos de la tundra que no quieren comerse a nadie.",
    ]},
    # ───────── Fiordo Aquilonal (44-42) ─────────
    {"id": "c044", "frases": [
        "Número cuarenta y cuatro. En el Fiordo Aquilonal el juego te cuenta de dónde salieron los humanos, y la respuesta son los vrykul.",
        "En Nafsavar, con un elixir, ves el eco del rey Ymiron ordenando matar a los bebés que nacían débiles y pequeños.",
        "Algunos padres los escondieron y los sacaron de Rasganorte; esos bebés débiles son los ancestros de Ventormenta y Lordaeron.",
        "Puedes ir a Nafsavar y ver la escena; la raza humana entera es una desobediencia de hace miles de años.",
    ]},
    {"id": "c043", "frases": [
        "Número cuarenta y tres. En la Fortaleza de Utgarde, el jefe final se muere a la mitad de la pelea, y lo resucita una mujer con alas.",
        "Ingvar el Saqueador cae, y Annhylde la Invocadora baja del techo a levantarlo como no-muerto para la segunda fase.",
        "Fue la primera val'kyr que vio el juego, dos años antes de que Sylvanas las convirtiera en su nuevo modelo de negocio.",
        "Y el fiordo está lleno de ellas, ahí se fabrican; Utgarde es la escuela.",
    ]},
    {"id": "c042", "frases": [
        "Número cuarenta y dos. En Nuevo Agamand, el pueblo de los Renegados del fiordo, los boticarios prueban una peste nueva con prisioneros vrykul.",
        "Te mandan a recoger ingredientes y a aplicar el veneno a los enfermos, con misiones alegres y nombres de receta de cocina.",
        "Es la Sociedad Real de Boticarios perfeccionando el mismo producto que unas zonas después explota en la Puerta de Cólera.",
        "Si haces las misiones de la Horda en orden, eres cómplice del mayor crimen de guerra de Rasganorte sin enterarte.",
    ]},
    # ───────── Cementerio de Dragones (41-35) ─────────
    {"id": "c041", "frases": [
        "Número cuarenta y uno. El Cementerio de Dragones se llama así porque es, literalmente, a donde los dragones van a morir.",
        "Alrededor del Templo del Reposo del Dragón hay cinco santuarios, uno por vuelo, y los huesos salen de la nieve en toda la zona.",
        "La Plaga llegó a levantar esos huesos: en el santuario Obsidiana y en el Azur hay dragones muertos caminando.",
        "Y en la cima del templo está Alexstrasza en persona, Reina de los Dragones, recibiendo visitas de nivel setenta y dos.",
    ]},
    {"id": "c040", "frases": [
        "Número cuarenta. En el centro del Cementerio hay un esqueleto que se ve desde cualquier punto de la zona: Galakrond.",
        "Es el protodragón del que descienden todos los dragones, un monstruo devorador de su propia especie, muerto hace una eternidad.",
        "La Plaga excava entre sus costillas para levantar protodragones, y tú bajas ahí a quemarles los planes.",
        "Puedes caminar dentro de su caja torácica; la cabeza sola es más grande que una posada.",
    ]},
    {"id": "c039", "frases": [
        "Número treinta y nueve. Naxxramas se mudó. En Classic flotaba sobre las Tierras de la Peste; en Wrath flota sobre el Cementerio de Dragones.",
        "La necrópolis voló de un continente a otro con Kel'Thuzad a bordo, y la Plaga la estacionó encima del Fortaleza de Hibergarde.",
        "Desde el bastión se ve la sombra en el cielo todo el día, y la gente de abajo vive con eso.",
        "Es el único edificio del juego que ha estado en dos continentes sin que nadie lo cargara.",
    ]},
    {"id": "c038", "frases": [
        "Número treinta y ocho. La Puerta de Cólera es el lugar de la cinemática más famosa del juego, y puedes pararte en el mismo punto.",
        "Angrathar, con el campo de batalla todavía lleno de catapultas, la mancha verde de la peste de Putress y los cuerpos de Bolvar y Saurfang el joven.",
        "En Wrath original, esa escena abría la Batalla por Entrañas, con Thrall y Varian; Cataclysm la borró del juego.",
        "En Classic sigue completa; es la única forma de volver a jugar la misión que hizo llorar a medio servidor.",
    ]},
    {"id": "c037", "frases": [
        "Número treinta y siete. En la Costa Olvidada, al sureste del Cementerio, hay barcos quemados y soldados fantasmas que todavía esperan órdenes de Arthas.",
        "Son la Primera Legión de Lordaeron, los hombres que Arthas trajo a cazar a Mal'Ganis, y a los que les quemó los barcos para que no volvieran.",
        "Orik Trueheart te da un elixir para entrar al mundo espiritual y oír sus historias: ninguno sabe que su príncipe los traicionó.",
        "Les prometió que volverían a casa; llevan veinte años en la playa esperando el barco.",
    ]},
    {"id": "c036", "frases": [
        "Número treinta y seis. En la Caverna Agonía de Escarcha puedes ver el momento exacto en que Arthas tomó la espada y perdió el alma.",
        "Una visión repite la escena: Muradin Barbabronce leyendo la inscripción, la espada volando a la mano del príncipe, el enano cayendo con el hielo.",
        "Todo el mundo salió de ahí convencido de que Muradin murió; el juego nunca lo dice.",
        "Guarda ese detalle: en las Cumbres Tormentosas hay un enano con amnesia que va a aparecer en esta lista.",
    ]},
    {"id": "c035", "frases": [
        "Número treinta y cinco. Los Escarlata que destruiste como caballero de la muerte no murieron: huyeron en barco a Rasganorte y se llaman Embate Escarlata.",
        "Nueva Vega del Amparo, en el Cementerio, es su ciudad nueva, con la Gran General Abbendis siguiendo una voz que dice ser la Luz.",
        "Fundaron un pueblo entero, con catedral y puerto, para seguir una voz en la cabeza de una sola persona.",
        "Quién es la voz lo descubres en la Corona de Hielo; también está en esta lista, casi al final.",
    ]},
    # ───────── Colinas Pardas (34-31) ─────────
    {"id": "c034", "frases": [
        "Número treinta y cuatro. Fauceparda, la capital de los furbolgs de las Colinas Pardas, está construida dentro del tocón de un árbol del mundo fallido.",
        "Vordrassil lo plantaron los druidas hace milenios, y sus raíces llegaron hasta la prisión de Yogg-Saron; lo tuvieron que destruir.",
        "Los furbolgs resucitaron ahí a su dios oso, Ursoc, y volvió corrompido por las raíces, enloquecido.",
        "Tú lo matas en las raíces del árbol; el dios de los furbolgs muere por culpa del jardín de los elfos.",
    ]},
    {"id": "c033", "frases": [
        "Número treinta y tres. En las Colinas Pardas la Alianza manda a los granjeros de Páramos de Poniente a pelear una guerra en la nieve.",
        "La Brigada de los Páramos de Poniente, con Gryan Stoutmantle al frente, el mismo de la milicia de Classic, tiene su campamento al norte de la zona.",
        "Es la única unidad del juego que pasó de perseguir a los Defias con horquillas a pelear contra la Horda en Rasganorte.",
        "Reconoces a los personajes de las misiones de nivel diez, unos años después y a treinta grados bajo cero.",
    ]},
    {"id": "c032", "frases": [
        "Número treinta y dos. Los tramperos de Arroyoplata, en las Colinas Pardas, son muy amables, hasta que cae la luna y se convierten en huargen.",
        "Arugal, el mago del Castillo de Colmillo Oscuro que creó la maldición, murió en Classic; el Rey Exánime lo levantó como sombra y lo mandó aquí.",
        "Está en la Isla Luna de Sangre, dirigiendo a los huargen de Rasganorte desde el más allá; tú lo matas por segunda vez.",
        "El canal ya contó la historia de Arugal; esta es la secuela que casi nadie jugó.",
    ]},
    {"id": "c031", "frases": [
        "Número treinta y uno. Harrison Jones, segunda aparición: las Ruinas de Drakil'jin, en las Colinas Pardas, con el gong, el sombrero y una trampa.",
        "Te pide que lo saques de un templo trol lleno de guardias de piedra, mientras él grita que esto es para el museo.",
        "Después se queda tranquilo en el campamento, hasta que lo arrastran a Uldum en Cataclysm.",
        "Un arqueólogo que aparece en cada expansión, siempre metido en un templo que no es suyo.",
    ]},
    # ───────── Zul'Drak (30-25) ─────────
    {"id": "c030", "frases": [
        "Número treinta. Los trols Drakkari de Zul'Drak sacrificaron a sus propios dioses para sobrevivir a la Plaga, y puedes ver los altares.",
        "Mataron a Rhunok el oso, a Quetz'lun la serpiente alada, a Sseratus, a Akali el rinoceronte, para beberse su poder.",
        "Har'koa, la leopardo de las nieves, es la única que queda viva, encadenada en su altar, y es ella quien te cuenta la traición.",
        "Es la única civilización del juego que se comió a sus dioses y aun así perdió la guerra.",
    ]},
    {"id": "c029", "frases": [
        "Número veintinueve. En el centro de Zul'Drak hay un cráter enorme con hielo adentro, y es la tumba de un dios que prefirió explotar.",
        "Mam'toth, el dios mamut, se destruyó a sí mismo cuando los Drakkari fueron a sacrificarlo, y la explosión se llevó el altar y a los sacerdotes.",
        "Lo que quedó es el Altar de Mam'toth: un hoyo en la ciudad, con sus restos y los trols que no alcanzaron a correr.",
        "Único caso de dios que eligió volarse antes que dejarse comer; el cráter se ve desde el aire.",
    ]},
    {"id": "c028", "frases": [
        "Número veintiocho. En Zul'Drak hay una misión en la que no caminas: viajas sentado en el hombro de un gigante de la tormenta.",
        "Gymer, el rey de los gigantes, está preso en Zul'Drak, y cuando lo liberas te sube y recorren la ciudad pisando trols.",
        "Él agarra enemigos, los lanza, y tú le dices a quién; es la venganza del Rey de la Tormenta.",
        "Dura cinco minutos y es lo más poderoso que te vas a sentir en toda la expansión, sin contar la banda.",
    ]},
    {"id": "c027", "frases": [
        "Número veintisiete. Drakuru, el trol simpático al que ayudaste en las Colinas Pardas, es ahora un caballero de la muerte al servicio del Rey Exánime.",
        "En Zul'Drak te disfraza de guerrero de la Plaga y te hace trabajar para él en Voltarus, el zigurat flotante.",
        "Al final, el Rey Exánime en persona te dice que Drakuru ya no le sirve, y te manda matarlo.",
        "Pasaste dos zonas trabajando para los dos lados a la vez; el único que lo tenía claro era Arthas.",
    ]},
    {"id": "c026", "frases": [
        "Número veintiséis. Gurgthock, el goblin de las peleas de Nagrand, abrió su segunda sucursal en Zul'Drak: el Anfiteatro de la Angustia.",
        "Mismo pozo, mismo ayudante trol, Wodin, y una cartelera de monstruos que termina con Vladof el Carnicero.",
        "La recompensa final es un anillo o un arma épica; la recompensa real es volver a oír al goblin anunciando la pelea.",
        "Es la mejor pista de que, en Azeroth, el negocio de las peleas clandestinas nunca quiebra.",
    ]},
    {"id": "c025", "frases": [
        "Número veinticinco. En la Fortaleza de Drak'Tharon, el último jefe te convierte en esqueleto, y peleas como esqueleto.",
        "El Profeta Tharon'ja te roba la carne a mitad de la pelea: tu personaje queda en huesos, con habilidades nuevas, y luego te la devuelve.",
        "Es la única mazmorra en la que el grupo entero juega con un personaje que no es el suyo.",
        "Y es una buena pista de lo que hace la Plaga con los trols; Drak'Tharon es un matadero elegante.",
    ]},
    # ───────── Cuenca de Sholazar (24-21) ─────────
    {"id": "c024", "frases": [
        "Número veinticuatro. La Cuenca de Sholazar es una reserva natural de los titanes, con pilares de piedra que la sellan como un invernadero.",
        "Es la hermana del Cráter de Un'Goro, con la misma selva, los mismos pilares y la misma guardiana: Freya, la vigilante.",
        "Uno de los pilares cayó, en la Avalancha, y por ese hueco la Plaga empezó a entrar al jardín.",
        "El Avatar de Freya te recibe en persona, cosa que no hacen muchas diosas, y te pone a reparar la cerca.",
    ]},
    {"id": "c023", "frases": [
        "Número veintitrés. En Sholazar hay una puerta de los titanes que te lleva a Un'Goro, al otro lado del planeta, caminando.",
        "La puerta se activa con dos interruptores, en el Pedestal de los Creadores y en el Mirador de los Creadores, y al pasar apareces en Kalimdor.",
        "Del otro lado despiertas al Etymidian, un gigante de piedra que patrulla el cráter desde entonces.",
        "Es el único viaje intercontinental gratis del juego, y lo usan cuatro personas.",
    ]},
    {"id": "c022", "frases": [
        "Número veintidós. Hemet Nesingwary llegó a Sholazar con su tercer campamento base, tras Vallefresno y Tuercespina, y aquí está la presa definitiva.",
        "Loque'nahak, el leopardo espectral, aparece cada muchas horas en cualquiera de varios puntos de la cuenca.",
        "Para los cazadores era la mascota más buscada del juego: una bestia espiritual que medio servidor acampó turnándose.",
        "Si quieres verla, trae café; si quieres domarla, trae amigos que te avisen.",
    ]},
    {"id": "c021", "frases": [
        "Número veintiuno. En Sholazar tienes que elegir entre dos tribus, y la elección correcta trae un dragón.",
        "Los Oráculos, ranas místicas, y los Corazón Frenético, lobos chaparros, se odian; tú matas al líder de una y la otra te adopta.",
        "Si eliges a los Oráculos, su huevo misterioso, que compras cada semana, puede traer un protodraco verde.",
        "La mayoría eligió a los lobos porque son más simpáticos, y se quedó sin montura por tener buen gusto.",
    ]},
    # ───────── Cumbres Tormentosas (20-14) ─────────
    {"id": "c020", "frases": [
        "Número veinte. La base goblin de las Cumbres Tormentosas se llama K tres, y el chiste es la montaña.",
        "Es el K dos de la vida real, la segunda cima del mundo, con un número más, porque los goblins no se quedan atrás.",
        "Desde K tres se ven las tormentas de Ulduar, y los goblins venden de todo mientras los gigantes de hielo pelean arriba.",
        "Es tu primera parada en la zona, y ya te está contando un chiste de alpinismo.",
    ]},
    {"id": "c019", "frases": [
        "Número diecinueve. En el Poblado Brunnhildar, las vrykul de hielo no aceptan hombres, así que el juego te convierte en mujer.",
        "Las Hyldnir te capturan, te disfrazan de guerrera vrykul gigante, con trenzas, y compites en sus pruebas para ganarte el favor de Hodir.",
        "Montas sus osos, peleas en su arena y cazas protodracos; todo eso con tres metros de estatura y una voz que no es la tuya.",
        "Es la cadena de misiones más larga de las Cumbres, y la mayoría la hizo sin pensar en lo que llevaba puesto.",
    ]},
    {"id": "c018", "frases": [
        "Número dieciocho. En lo alto del Templo de las Tormentas hay un dios sentado que no se mueve, y lleva milenios sin moverse: Thorim.",
        "Su esposa, Sif, fue asesinada, y le hicieron creer que fueron los gigantes de hielo; el culpable fue su hermano Loken.",
        "Thorim dejó de gobernar y se sentó a mirar la nieve; Loken tomó Ulduar y la zona entera con sus enanos de hierro.",
        "Tú le llevas las pruebas al templo, y baja a pelear con Loken en Ulduar; ir a ver a un dios deprimido es una misión real.",
    ]},
    {"id": "c017", "frases": [
        "Número diecisiete. En las Cumbres Tormentosas vuela una montura que muchísima gente buscó durante años sin verla jamás: el Protodraco Perdido en el Tiempo.",
        "Aparece en varias rutas, cada muchas horas, compartiendo lugar con una dragona azul, Vyragosa, que es la que normalmente te sale.",
        "Quien lo mata se lleva la montura garantizada; por eso hay gente que lleva años estacionada en una roca mirando el cielo.",
        "Si ves a alguien quieto en lo alto de las Cumbres, no está desconectado: está trabajando.",
    ]},
    {"id": "c016", "frases": [
        "Número dieciséis. El enano que todo el mundo cree muerto en la Caverna Agonía de Escarcha está vivo, y gobierna un pueblo en las Cumbres.",
        "Se hace llamar Yorg Stormheart, rey de los enanos de Fuerte Escarcha, y no recuerda quién es: el hielo le borró la memoria.",
        "Es Muradin Barbabronce, el hermano del rey de Forjaz, y tú eres quien lo descubre, gracias a Brann, el otro hermano.",
        "Los tres Barbabronce están repartidos: Magni en Forjaz, Brann en Ulduar y Muradin con amnesia entre gigantes.",
    ]},
    {"id": "c015", "frases": [
        "Número quince. En Ulduar hay un jefe que la mayoría de los jugadores jamás vio, y no está escondido: está en el planetario.",
        "Algalon el Observador solo aparece si derrotas a los cuatro guardianes en su modo difícil, y te da una hora para intentarlo.",
        "Es un enviado de los titanes que viene a decidir si Azeroth se reinicia desde cero; si lo convences, manda la señal de que el planeta vale la pena.",
        "El Planetario Celestial sigue ahí, cerrado para casi todos, con un juez que lleva años esperando visitas.",
    ]},
    {"id": "c014", "frases": [
        "Número catorce. La montura más rara de Wrath es la cabeza de un gnomo robot, y se consigue haciendo enojar a un dios antiguo.",
        "Mimiron, el guardián ingeniero, construyó un vehículo con su propia cara, y Yogg-Saron lo suelta solo si lo derrotas sin que ningún guardián te ayude.",
        "Veinticinco personas, el jefe final en su versión más difícil, y una tasa de caída que convierte la montura en un trofeo de servidor.",
        "La Cabeza de Mimiron sigue siendo el objeto que más identifica a los que raidearon en dos mil nueve.",
    ]},
    # ───────── Dalaran y Bosque Canto de Cristal (13-9) ─────────
    {"id": "c013", "frases": [
        "Número trece. Dalaran dejó un cráter. Si vas a las Laderas de Trabalomas, en los Reinos del Este, hay un hoyo enorme donde estaba la ciudad.",
        "En Classic era una burbuja violeta impenetrable; los magos levantaron la ciudad completa y la volaron a Rasganorte, para enfrentar a Malygos.",
        "El cráter se quedó, y Cataclysm lo convirtió en un lago; la ciudad flota ahora sobre el Bosque Canto de Cristal.",
        "Es la única mudanza en la historia del juego que dejó daños estructurales en un continente.",
    ]},
    {"id": "c012", "frases": [
        "Número doce. En Dalaran, la plataforma de vuelo se llama Alto de Krasus, y Krasus no es un mago: es un dragón.",
        "Korialstrasz, consorte de Alexstrasza, vivió siglos entre los Kirin Tor con forma de elfo y ese nombre.",
        "La ciudad la dirige Rhonin, el héroe de las novelas, casado con Vereesa Brisaveloz, la hermana de Sylvanas, que lidera a los elfos de la Alianza.",
        "Dalaran es, básicamente, una ciudad administrada por los personajes de los libros de Richard Knaak.",
    ]},
    {"id": "c011", "frases": [
        "Número once. En la Ciudadela Violeta hay un portal que casi nadie cruza, y sube a un salón escondido en lo alto de la torre: el Salón Púrpura.",
        "Y si encuentras ocho libros de magia repartidos por la ciudad, que aparecen y desaparecen, el logro Educación Superior abre otra sala secreta.",
        "Es el Refugio del Archimago Vargoth, el mismo de Kirin'Var, que te regala un familiar Kirin Tor como mascota.",
        "Dalaran tiene más cuartos secretos que cualquier ciudad del juego, y la mayoría pasó un año entero sin abrir uno.",
    ]},
    {"id": "c010", "frases": [
        "Número diez. En el banco de Dalaran, un gnomo te convierte en oveja, se ríe y se teletransporta, y luego te pide perdón por correo.",
        "Minigob Manacapón anda suelto desde el parche tres punto uno, y después de la broma te llega una carta con una varita: el Hacedor de Travesuras.",
        "Sirve para convertir en oveja a otro jugador, solo dentro de Dalaran, para que la cadena siga.",
        "Es el único personaje del juego cuyo trabajo es molestar a la gente y repartir las herramientas para seguir molestando.",
    ]},
    {"id": "c009", "frases": [
        "Número nueve. El Bosque Canto de Cristal, debajo de Dalaran, es la zona más bonita de la expansión y no tiene casi misiones.",
        "Los árboles son de cristal porque los dragones azules lo cristalizaron en una batalla antigua contra los Altonato de Shandaral, y así se quedó.",
        "Hay dos campamentos, un par de misiones, y el resto es paisaje; los diseñadores lo dejaron como patio de la ciudad.",
        "Vale la pena bajar a caminarlo: es un bosque entero que parece sonar a vidrio cuando lo cruzas.",
    ]},
    # ───────── Conquista del Invierno (8) ─────────
    {"id": "c008", "frases": [
        "Número ocho. El Lago Conquista del Invierno es una zona entera dedicada a una guerra de asedio con vehículos, y tiene una banda escondida.",
        "Cada dos horas y media los dos bandos se pelean la fortaleza con catapultas y demoledores que construyes en talleres.",
        "El que gana abre la Cámara de Archavon, una banda con cuatro jefes a la que solo el dueño del lago puede entrar a saquear.",
        "Es la única banda del juego cuya puerta la abre un resultado de PvP; si perdiste, vuelve en dos horas y media.",
    ]},
    # ───────── Corona de Hielo (7-1) ─────────
    {"id": "c007", "frases": [
        "Número siete. El Torneo Argenta, en el norte de la Corona de Hielo, no existía al salir la expansión; lo construyeron frente a tus ojos.",
        "En el parche tres punto uno aparecieron las obras, y semana a semana se levantó la carpa, las gradas y después el Coliseo de los Cruzados.",
        "Ahí se justa a caballo contra campeones de cada ciudad, y un Caballero Negro se cuela al torneo a matar gente en plena justa.",
        "Es el único lugar del juego donde el enemigo es la Plaga y la diaria es ganar un torneo medieval.",
    ]},
    {"id": "c006", "frases": [
        "Número seis. La dragona de hielo que vuela sobre la Ciudadela de la Corona de Hielo tiene una tumba en la misma zona, y se llama Caída de Sindragosa.",
        "Sindragosa era la consorte de Malygos, y murió en la Guerra de los Ancestros, destrozada por el Alma de Dragón de Alamuerte.",
        "Sus huesos quedaron en la Corona de Hielo diez mil años, hasta que el Rey Exánime la levantó como su dracoliche.",
        "El cráter de su caída tiene su silueta, y se puede visitar; el jefe de la banda empezó siendo un fósil.",
    ]},
    {"id": "c005", "frases": [
        "Número cinco. En Puerto del Embate, los Escarlata que seguían a una voz descubren quién les hablaba: Mal'Ganis.",
        "El Gran Almirante Barean Westwind, su líder, era el señor del terror disfrazado, el mismo demonio que empujó a Arthas a Stratholme.",
        "Tú lo expones en una misión, y los Escarlata que destruiste dos veces caen por tercera vez, por fin con razón.",
        "Mal'Ganis se escapa, como siempre; es el villano con más huidas del juego.",
    ]},
    {"id": "c004", "frases": [
        "Número cuatro. Sobre la Corona de Hielo vuelan dos barcos de guerra, uno por facción, y puedes subirte en pleno vuelo.",
        "El Martillo de Orgrim y el Rompecielos patrullan la zona dando vueltas, con misiones, vendedores y cañones a bordo.",
        "Hay que volar hasta ellos, aterrizar en la cubierta y aguantarse el vértigo; son los únicos pueblos del juego en movimiento.",
        "Luego los dos se encuentran dentro de la Ciudadela, y se disparan entre sí mientras tú saltas de un barco al otro.",
    ]},
    {"id": "c003", "frases": [
        "Número tres. El Pináculo de los Cruzados, el campamento de Tirion en la Corona de Hielo, lo construyes tú con misiones.",
        "Al llegar es una colina vacía; terminas la cadena de la Vanguardia Argenta y aparece un fuerte completo, con torre, vendedores y Tirion al frente.",
        "Fue uno de los primeros usos del cambio de fases en el mundo abierto: el mapa cambia según lo que tú hiciste.",
        "Dos jugadores en la misma colina pueden ver cosas distintas; uno ve nieve, el otro ve una fortaleza.",
    ]},
    {"id": "c002", "frases": [
        "Número dos. En las Cámaras de Reflexión, el Rey Exánime en persona te persigue por un pasillo, y no se puede ganar.",
        "Tocas la espada Agonía de Escarcha, aparece Uther, aparece Arthas, y la única salida es correr mientras él rompe muro tras muro de hielo.",
        "Jaina o Sylvanas, según tu bando, te sacan en un barco, y Arthas se queda en la orilla, mirando.",
        "Es la única mazmorra donde el jefe final no se mata: se huye de él, y te deja un recuerdo de lo que viene arriba.",
    ]},
    {"id": "c001", "frases": [
        "Número uno. En el noreste de la Corona de Hielo hay un paladín agonizando en una colina, en la Vigilia Silenciosa, y Tirion te manda a salvarlo.",
        "Es el Cruzado Bridenbrad, y vas por una cura con Alexstrasza, con Remulos en el Claro de la Luna y con A'dal en Shattrath; ninguno puede curarlo.",
        "A'dal baja a Rasganorte en persona y se lleva su espíritu a la Luz, para que la Plaga no lo levante jamás.",
        "Bridenbrad existió: es el hermano de un empleado de Blizzard que murió de cáncer, y la cadena de misiones es su funeral.",
        "Se puede visitar, y vale la pena ir callado.",
    ]},
    {"id": "cierre", "frases": [
        "Y esas son las cien. Dos continentes, cien lugares, y todos siguen ahí, esperando a que alguien baje de la montura.",
        "Si me quedo con una, es el cráter de Dalaran: la prueba de que en este juego hasta las ciudades se van, pero el mapa se acuerda.",
        "Dime en los comentarios cuál no conocías, y cuál vas a ir a comprobar primero; yo apuesto que el gnomo del banco.",
        "Y si llegaste hasta aquí sin saltarte ninguna, tienes más paciencia que Thorim.",
    ]},
]
