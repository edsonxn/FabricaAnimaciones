# -*- coding: utf-8 -*-
"""Pegatinas de «15 FARMEOS de ORO del 30 al 50 en WoW Forever» (25-nov-2026; adaptado de wow_ruta_profesiones/_pegatinas.py).
Una por cosa que NOMBRA la voz; identidad = id de Wowhead Forever o archivo concreto de la wiki.
- o_<slug> = ÍCONO de objeto/hechizo: id de videos/_investigacion_wow_oro_30_50.md («Qué se farmea») o del buscador de Wowhead Forever
  (www.wowhead.com/forever/search/suggestions-template) → tooltip de Wowhead FOREVER (nether.wowhead.com/forever/tooltip/<item|spell>/<id>;
  locale=0 inglés, locale=11 es-MX para comprobar el nombre) → wow.zamimg.com/images/wow/icons/large/<icon>.jpg (56 px, ampliado a 320).
- Criaturas y PNJ: modelo 3D de Wowhead FOREVER (webthumb classicplus, 300 px, ampliado x2). displayId = `linksButton.dataset.displayId`
  de la página www.wowhead.com/forever/npc=<id> (leída el 25-nov con el navegador; Rizz 3733 y Benjy 140701 coinciden con el campo «model»
  del mapa mundial de Wowhead Forever). Modelos de classicplus = el bicho tal como está en Forever (nada de modelos HD de retail).
- Lugares: ARCHIVO CONCRETO de warcraft.wiki.gg (imagen de la página del lugar; capturas oficiales de Forever «Zones Riverglades»;
  pantallas de carga de Classic). Nada de Hearthstone, TCG, cómic, fan art ni capturas posteriores a Cataclysm.
python _pegatinas.py [slug…] → pegatinas/<slug>.png (≤ 900 px) + pantallas/<slug>.jpg (1920, si el original es ≥ 1000) + previews/pegatinas_hoja.jpg
NO toca los com_*.png (tarjetas de comentarios)."""
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
for c in (PEG, PAN, os.path.join(D, "previews")):
    os.makedirs(c, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}
WIKI_API = "https://warcraft.wiki.gg/api.php"
PRENSA = "Blizzard, capturas oficiales de Forever (galería de prensa de WoW Forever)"

# slug: (archivo de warcraft.wiki.gg, recorte, qué es / identidad, escena(s))
WIKI = {
    "poblado_magram": ("Magram Village.jpg", None, "imagen de la página Magram Village (Poblado Magram, Desolace)", "p15"),
    "cueva_niebla_negra": ("Darkmist Cavern.jpg", None, "imagen de la página Darkmist Cavern (Cueva Niebla Negra, Marjal Revolcafango; se ve una araña Niebla Negra y telarañas)", "p14"),
    "poblado_murohelecho": ("Brackenwall Village.jpg", None, "imagen de la página Brackenwall Village (Poblado Murohelecho, Marjal Revolcafango; vendedores de la Horda)", "p14"),
    "theramore": ("Theramore.jpg", None, "archivo «Theramore» («Theramore skyline at sunset», página Theramore Isle: la isla intacta, antes de su destrucción en MoP; vendedores de la Alianza). CONFIANZA MEDIA: cielo rojizo del atardecer", "p14"),
    "lago_nazferiti": ("Lake Nazferiti.jpg", None, "imagen de la página Lake Nazferiti (Lago Nazferiti, Vega de Tuercespina). CONFIANZA MEDIA: sin fecha; hierba y agua con detalle moderno, puede ser captura de retail (el lago no cambió)", "p13"),
    "valle_velo_bruma": ("Mistvale Valley.jpg", None, "imagen de la página Mistvale Valley (Valle del Velo de Bruma, Vega de Tuercespina; captura antigua)", "p13"),
    "desierto_sal": ("Shimmering Flats.jpg", None, "imagen de la página Shimmering Flats (El Desierto de Sal, Las Mil Agujas; página Thousand Needles (Classic))", "p12"),
    "circuito_espejismo": ("Mirage Raceway.jpg", None, "imagen de la página Mirage Raceway (Circuito del Espejismo, El Desierto de Sal)", "p12"),
    "claros_del_rio": ("Zones Riverglades 035.jpg", None, "«Zones Riverglades» (galería de Forever) = Claros del Río; imagen principal de la página Riverglades", "p11 p04 p06"),
    "claros_del_rio_2": ("Zones Riverglades 040.jpg", None, "«Zones Riverglades» (galería de Forever) = Claros del Río (río al atardecer)", "p11 p04"),
    "puerto_polvomecha": ("Powderfuse Port.jpg", None, "imagen de la página Powderfuse Port (Puerto Polvomecha, Claros del Río; zona de Forever)", "p11"),
    "cortijo_wheeler": ("Wheeler's Grange.jpg", None, "archivo «Wheeler's Grange» = Cortijo de Wheeler (rótulo en inglés del mapa de Wowhead Forever en 54.8, 75.8 de Claros del Río; subido el 20-oct-2026)", "p04"),
    "barranco_lethlor": ("Lethlor Ravine.jpg", None, "imagen de la página Lethlor Ravine (Barranco Lethlor, Tierras Inhóspitas; página Badlands (Classic); se ven las crías volando). La otra de la página (Lethlor-Ravine.jpg) es de Cataclysm: descartada", "p10"),
    "cueva_stagalbog": ("Stagalbog Cave.jpg", None, "archivo «Stagalbog Cave» (página Stagalbog Cave, Pantano de las Penas)", "p09"),
    "puesto_juncobruma": ("Misty Reed Post.jpg", None, "imagen de la página Misty Reed Post (Puesto Juncobruma, Pantano de las Penas)", "p09"),
    "pantano_penas": ("Swamp of Sorrows.jpg", None, "imagen de la página Swamp of Sorrows (Pantano de las Penas; página Swamp of Sorrows (Classic))", "p06 p09"),
    "rocal": ("Stonard.jpg", None, "archivo «Stonard» (página Stonard = Rocal, Pantano de las Penas; vendedores de la Horda)", "p06"),
    "arenas_abisales": ("Abyssal Sands.jpg", None, "imagen de la página Abyssal Sands (Arenas Abisales, Tanaris; dunas con esqueleto de dinosaurio)", "p08"),
    "gadgetzan": ("Gadgetzan.jpg", None, "imagen «Gadgetzan» (páginas Gadgetzan y Tanaris (Classic))", "p08"),
    "dos_colosos": ("The Twin Colossals.jpg", None, "archivo «The Twin Colossals» (página Twin Colossals = Los Dos Colosos, Feralas)", "p07"),
    "campamento_mojache": ("Camp Mojache.jpg", None, "imagen de la página Camp Mojache (Campamento Mojache, Feralas; página Feralas (Classic))", "p07"),
    "bastion_plumaluna": ("Feathermoon Stronghold.jpg", None, "archivo «Feathermoon Stronghold» (Bastión Plumaluna en la isla, como en Classic; la «New-feathermoon» de la página es la de Cataclysm: descartada)", "p07"),
    "templo_sumergido": ("Temple of Atal'Hakkar loading screen.jpg", "carga_classic", "pantalla de carga del Templo de Atal'Hakkar = Templo Sumergido (Classic)", "p07"),
    "kargath": ("Kargath.jpg", None, "archivo «Kargath» (página Kargath, Tierras Inhóspitas; captura antigua)", "p05"),
    "explanada_espejismo": ("Mirage Flats.jpg", None, "imagen de la página Mirage Flats (Explanada del Espejismo, Tierras Inhóspitas)", "p05"),
    "gromgol": ("Grom'Gol Base Camp beach side.jpg", None, "archivo «Grom'Gol Base Camp beach side» (página Grom'gol Base Camp = Campamento Grom'Gol)", "p03"),
    "bahia_botin": ("Booty Bay.jpg", None, "imagen «Booty Bay» (páginas Booty Bay y Stranglethorn Vale (Classic))", "p03 p11"),
    "dominios_aplastacresta": ("Crushridge Hold.jpg", None, "imagen de la página Crushridge Hold (Dominios de los Aplastacresta, Montañas de Alterac)", "p02 intro"),
    "castillo_nethergarde": ("Nethergarde.jpg", None, "archivo «Nethergarde» (página Nethergarde Keep = Castillo de Nethergarde, Las Tierras Devastadas; el castillo entero, antes de la Legión)", "p01"),
    "alto_rapinadores": ("Rise of the Defiler.jpg", None, "imagen de la página Rise of the Defiler (Alto de los Rapiñadores, Las Tierras Devastadas)", "p01 intro"),
    "alto_rapinadores_2": ("Defiler's Peak.jpg", None, "archivo «Defiler's Peak» (página Rise of the Defiler: suelo rojo con círculos del Alto de los Rapiñadores)", "p01"),
    # "serpiente_enroscada": «Serpent's Coil Blasted Lands.jpg» DESCARTADA: el resumen del archivo dice «cata» (captura de Cataclysm)
    "guarida_onyxia": ("Onyxia's Lair loading screen.jpg", "carga_classic", "pantalla de carga de la Guarida de Onyxia (Classic)", "overgear"),
}
# Modelos 3D de Wowhead FOREVER: displayId de la página npc=<id> de Wowhead Forever (25-nov, navegador)
# slug: (displayId, npc, nombre es-MX / inglés, identidad, escena)
MODELOS = {
    # p15 Desolace
    "retador_magram": (2293, 4640, "Retador Magram / Magram Wrangler", "centauro (33-34), Poblado Magram", "p15"),
    "cazavientos_magram": (9429, 4641, "Cazavientos Magram / Magram Windchaser", "centauro (33-34), Poblado Magram", "p15"),
    "corremanadas_magram": (9430, 4643, "Corremanadas Magram / Magram Pack Runner", "centauro (34-35), Poblado Magram", "p15"),
    "zarposea_magram": (2716, 4662, "Zarpósea Magram / Magram Bonepaw", "hiena (37-38) de los centauros", "p15"),
    # p14 Marjal
    "arana_niebla_negra": (545, 4376, "Araña Niebla Negra / Darkmist Spider", "araña (35-36), Cueva Niebla Negra", "p14"),
    "ermitana_niebla_negra": (2538, 4378, "Ermitaña Niebla Negra / Darkmist Recluse", "araña (36-37), Cueva Niebla Negra", "p14"),
    # p13 Tuercespina
    "gorila_velo_bruma": (843, 1108, "Gorila Velo de Bruma / Mistvale Gorilla", "gorila (32-33), oeste del Lago Nazferiti", "p13"),
    "gorila_velo_bruma_anciano": (838, 1557, "Gorila Velo de Bruma anciano / Elder Mistvale Gorilla", "gorila (40-41), Valle del Velo de Bruma", "p13"),
    "mokk": (840, 1514, "Mokk el Salvaje / Mokk the Savage", "gorila jefe (44) que se invoca en oleadas con la misión La fiebre de Tuercespina", "p13"),
    "unbagwa": (4661, 1449, "Médico brujo Unbagwa / Witch Doctor Unbagwa", "PNJ de la misión La fiebre de Tuercespina (invoca a Mokk)", "p13"),
    # p12 Mil Agujas / Marjal
    "tortuga_brillavalva": (5052, 4142, "Tortuga brillavalva / Sparkleshell Tortoise", "tortuga (30-31), El Desierto de Sal", "p12"),
    "mordedor_brillavalva": (2308, 4143, "Mordedor brillavalva / Sparkleshell Snapper", "tortuga (34-35), El Desierto de Sal", "p12"),
    "cavapozos_fangorroca": (7840, 4399, "Cavapozos Fangorroca / Mudrock Borer", "tortuga (42-43), Marjal Revolcafango", "p12"),
    # p11 Claros del Río / Tuercespina sur
    "reptador_arena": (5557, 255901, "Reptador de arena / Sand Crawler", "cangrejo (36-37) de Claros del Río (PNJ nuevo de Forever)", "p11"),
    "reptador_arenas_sur": (9573, 2544, "Reptador de las arenas del sur / Southern Sand Crawler", "cangrejo (40-41), sur de Tuercespina", "p11"),
    "fimbo": (142111, 259962, "Fimbo Grasapuños / Fimbo Greasemitz", "PNJ de Puerto Polvomecha, misión Sabores de mar (PNJ nuevo de Forever)", "p11"),
    # p10 Tierras Inhóspitas
    "cria_lethlor": (715, 2725, "Scalding Whelp (sin es-MX) = las crías del Barranco Lethlor", "cría de dragón (41-43)", "p10"),
    # p09 Pantano de las Penas
    "murloc_marisma": (506, 747, "Múrloc de marisma / Marsh Murloc", "múrloc (41-42), Pantano de las Penas", "p09"),
    "vomitatintas_marisma": (1995, 750, "Vomitatintas de marisma / Marsh Inkspewer", "múrloc (42-43)", "p09"),
    "comecarnes_marisma": (391, 751, "Comecarnes de marisma / Marsh Flesheater", "múrloc (43-44)", "p09"),
    "oraculo_marisma": (386, 752, "Oráculo de marisma / Marsh Oracle", "múrloc (44-45); suelta la receta del té soleado", "p09"),
    # p08 Tanaris
    "hiena_llagapata": (1536, 5426, "Hiena Llagapata / Blisterpaw Hyena", "hiena (44-45), Arenas Abisales", "p08"),
    "roc_fuego": (7348, 5429, "Roc de fuego / Fire Roc", "roc (43-45), Arenas Abisales", "p08"),
    "roc": (3248, 5428, "Roc", "roc (41-43), Tanaris", "p08"),
    # p07 Feralas
    "tronador_groddoc": (3188, 5262, "Tronador Groddoc / Groddoc Thunderer", "gorila (49-50), norte de Feralas", "p07"),
    "patriarca_cueracero": (3200, 5274, "Patriarca Cueracero / Ironfur Patriarch", "oso (48-49), norte de Feralas", "p07"),
    "simio_groddoc": (3186, 5260, "Simio Groddoc / Groddoc Ape", "gorila (42-43), centro de Feralas", "p07"),
    "oso_cueracero": (3201, 5268, "Oso Cueracero / Ironfur Bear", "oso (41-42), centro de Feralas", "p07"),
    # p06 Pantano / Claros del Río
    "jaguar_pantano": (632, 767, "Jaguar del pantano / Swamp Jaguar", "felino (36-37), Pantano de las Penas", "p06"),
    "cazadora_llanagreste": (1933, 259055, "Cazadora llanagreste / Wildplains Huntress", "felino (38-39), Claros del Río (PNJ nuevo de Forever)", "p06"),
    # p05 Tierras Inhóspitas
    "elemental_roca_inferior": (1161, 2735, "Elemental de roca inferior / Lesser Rock Elemental", "elemental (37-39), junto a Kargath", "p05"),
    "elemental_roca": (171, 92, "Elemental de roca / Rock Elemental", "elemental (39-40), sur de Tierras Inhóspitas", "p05"),
    "elemental_roca_superior": (14328, 2736, "Elemental de roca superior / Greater Rock Elemental", "elemental (42-44), suroeste", "p05"),
    # p04 Claros del Río
    "coyote_llanuras": (161, 259267, "Coyote de las llanuras / Plains Coyote", "coyote (36-37), sur del Cortijo de Wheeler (PNJ nuevo de Forever)", "p04"),
    "merodeador_coyote": (161, 259263, "Merodeador coyote / Coyote Prowler", "coyote (36-37); MISMO modelo que el Coyote de las llanuras (displayId 161)", "p04"),
    "sootfur": (7339, 258522, "Sootfur (sin es-MX)", "coyote con nombre (38) de la misión Coyote Huntin'", "p04"),
    "benjy_wheeler": (140701, 258317, "Benjy Wheeler", "granjero del Cortijo de Wheeler, da Coyote Huntin' (PNJ nuevo de Forever)", "p04"),
    # p02 Alterac
    "ogro_aplastacresta": (11567, 2252, "Ogro Aplastacresta / Crushridge Ogre", "ogro (34-35), cuevas de Alterac", "p02"),
    "tosco_aplastacresta": (610, 2253, "Tosco Aplastacresta / Crushridge Brute", "ogro (35-36)", "p02"),
    "aplastador_aplastacresta": (655, 2254, "Aplastador Aplastacresta / Crushridge Mauler", "ogro élite (36-37) junto a la fortaleza", "p02"),
    "mago_aplastacresta": (6705, 2255, "Mago Aplastacresta / Crushridge Mage", "ogro élite (37-38) junto a la fortaleza", "p02"),
    "rizz": (3733, 2684, "Rizz Tornillosuelto / Rizz Loosebolt", "vendedor gnomo encerrado en una jaula, cueva del norte", "p02"),
    "lo_grosh": (11566, 2453, "Lo'Grosh", "ogro raro (39) de Alterac", "p02"),
    # p01 Las Tierras Devastadas
    "destripador_negro": (10824, 5982, "Destripador negro / Black Slayer", "carroñero (46-48), Las Tierras Devastadas", "intro p01"),
    "aguijonero_scorpok": (6068, 5988, "Aguijonero Scorpok / Scorpok Stinger", "escórpido (50-51)", "p01"),
    "hiena_risitas": (8050, 5984, "Hiena risitas famélica / Starving Snickerfang", "hiena (45-46)", "p01"),
    "lynnore": (6631, 7506, "Maga sangrienta Lynnore / Bloodmage Lynnore", "da El vigor del buitre (10 mollejas)", "p01"),
    "drazial": (6630, 7505, "Mago sangriento Drazial / Bloodmage Drazial", "da El golpe decisivo (2 mollejas)", "p01"),
}
# Íconos: slug: (tipo, id, qué dice la voz, escena)
ICONOS = {
    "o_equitacion": ("spell", 33388, "Aprendiz jinete (equitación de aprendiz, la montura del 40)", "intro"),
    "o_pano_seda": ("item", 4306, "Paño de seda", "p15 p02"),
    "o_tejido_magico": ("item", 4338, "Paño de tejido mágico", "p15 p03"),
    "o_mandibula_arana": ("item", 4585, "Mandíbula de araña chorreando", "p14"),
    "o_punta_pata_arana": ("item", 1074, "Punta de pata de araña dura", "p14"),
    "o_seda_arana_espesa": ("item", 4337, "Seda de araña espesa", "p14"),
    "o_seda_sombras": ("item", 10285, "Seda de las Sombras", "p14"),
    "o_colmillo_gorila": ("item", 2799, "Colmillo de gorila", "p13"),
    "o_pelo_gorila_burdo": ("item", 4096, "Pelo de gorila burdo", "p13 p07"),
    "o_fragmento_caparazon": ("item", 4556, "Fragmento de caparazón moteado", "p12"),
    "o_carne_tortuga": ("item", 3712, "Carne de tortuga", "p12"),
    "o_cola_escamosa": ("item", 4555, "Cola escamosa espesa", "p12"),
    "o_carne_cangrejo": ("item", 12206, "Carne de cangrejo tierna", "p11"),
    "o_carne_reptador": ("item", 268345, "Carne de reptador de arena (misión Sabores de mar)", "p11"),
    "o_ojo_murloc": ("item", 268344, "Ojo de múrloc de agua salada (misión Sabores de mar)", "p11"),
    "o_almeja_boca_grande": ("item", 7973, "Almeja de boca grande", "p11 p09"),
    "o_perla_oro": ("item", 13926, "Perla de oro", "p09"),
    "o_perla_negra": ("item", 7971, "Perla negra", "p09"),
    "o_perla_iridiscente": ("item", 5500, "Perla iridiscente", "p09"),
    "o_carne_almeja": ("item", 7974, "Carne de almeja sabrosa", "p09"),
    "o_serviola": ("item", 4603, "Serviola moteada cruda", "p09"),
    "o_aceite_pescado": ("item", 17058, "Aceite de pescado", "p09"),
    "o_receta_te_soleado": ("item", 249883, "Receta: té soleado (receta nueva de Forever)", "p09"),
    "o_te_soleado": ("item", 249869, "Té soleado (lo que crea la receta)", "p09"),
    "o_glandula_llamas": ("item", 4402, "Glándula de llamas pequeña", "p10"),
    "o_aji_aliento": ("item", 12217, "Ají aliento de dragón", "p10"),
    "o_vastago_oscuro": ("item", 10822, "Vástago oscuro (mascota)", "p10"),
    "o_corazon_draco": ("item", 4612, "Corazón de draco negro (misión)", "p10"),
    "o_melena_espesa": ("item", 4583, "Melena espesa", "p08 p04"),
    "o_pata_trofeo": ("item", 4584, "Pata de trofeo grande", "p08"),
    "o_cuero_grueso": ("item", 4304, "Cuero grueso", "p08 p03"),
    "o_cuero_pesado": ("item", 4234, "Cuero pesado (el «cuero» de jaguares y coyotes)", "p06 p04"),
    "o_carne_lobo_rojo": ("item", 12203, "Carne de lobo rojo", "p08 p04"),
    "o_carne_lobo_tierna": ("item", 12208, "Carne de lobo tierna", "p08"),
    "o_huevo_gigante": ("item", 12207, "Huevo gigante", "reglas burla0 p08"),
    "o_hueso_oso": ("item", 11411, "Hueso de oso grande (también es una maza gris)", "p07"),
    "o_mechon_gorila": ("item", 4099, "Mechón de pelo de gorila", "p07"),
    "o_mandibula_oso": ("item", 11408, "Mandíbula de oso", "p07"),
    "o_garra_oso": ("item", 11410, "Garra de oso indómito", "p07"),
    "o_costillar_oso": ("item", 11409, "Costillar de oso", "p07"),
    "o_cola_blanda": ("item", 1688, "Cola blanda larga", "p06"),
    "o_bigote_cerdas": ("item", 1686, "Bigote de cerdas", "p06"),
    "o_tierra_elemental": ("item", 7067, "Tierra elemental", "p05"),
    "o_piedra_lisa": ("item", 4552, "Trozo de piedra lisa", "p05"),
    "o_piedra_dentada": ("item", 4553, "Trozo de piedra dentado", "p05"),
    "o_piedra_inerte": ("item", 4784, "Piedra inerte", "p05"),
    "o_sal_roca": ("item", 8150, "Sal de roca", "p05"),
    "o_cola_tupida": ("item", 4582, "Cola tupida suave", "p04"),
    "o_colmillo_grande": ("item", 5637, "Colmillo grande (los «colmillos» de los coyotes)", "p04"),
    "o_valija_mitril": ("item", 21228, "Valija reforzada con mitril", "p03"),
    "o_anguila_petrea": ("item", 13422, "Anguila escama pétrea", "p03"),
    "o_pano_runico": ("item", 14047, "Paño rúnico (dentro de las valijas)", "p03"),
    "o_adornos_brillantes": ("item", 6532, "Adornos brillantes (el señuelo de pesca)", "p03"),
    "o_luremaster": ("spell", 1225455, "Luremaster = «Maestro del cebo» en es-MX (talento de Legado)", "p03"),
    "o_jarabe_agua": ("item", 8827, "Jarabe de caminar sobre el agua", "p03"),
    "o_expositor_pesca": ("item", 279965, "Expositor de pesca (objeto de campamento)", "p03"),
    "o_mena_hierro": ("item", 2772, "Mena de hierro", "p02"),
    "o_mena_mitril": ("item", 3858, "Mena de mitril", "p02 p10"),
    "o_mena_veraplata": ("item", 7911, "Mena de veraplata", "p02"),
    "o_mena_oro": ("item", 2776, "Mena de oro", "p02"),
    "o_mena_plata": ("item", 2775, "Mena de plata", "p02"),
    "o_pacificador": ("item", 6327, "The Pacifier = «El pacificador» (es-MX de Wowhead Classic; Forever no lo trae): LA MAZA de Lo'Grosh, a dos manos, azul, velocidad 4,00, nivel 36 en Forever; botín propio 3 de 104 en Wowhead Forever", "p02"),
    "o_molleja_buitre": ("item", 8396, "Molleja de buitre", "intro p01"),
    "o_papada_hiena": ("item", 8391, "Papada de hiena risitas (misión El vigor del buitre)", "p01"),
    "o_pinza_scorpok": ("item", 8393, "Pinza de scorpok (misión El golpe decisivo)", "p01"),
}
# objetos que se equipan: slug: (displayId del objeto en Wowhead Forever, nota) → pegatinas/eq_<slug>.jpg (visor 3D, sobre blanco)
EQUIPADO = {
    "o_hueso_oso": (1515, "Hueso de oso grande = maza de una mano gris (displayId 1515, página item=11411 de Wowhead Forever)"),
    "o_pacificador": (5136, "El pacificador = maza a dos manos (displayId 5136, botín de Lo'Grosh en la página npc=2453 de Wowhead Forever)"),
}
ICONO_DIRECTO = {   # slug: (nombre del ícono en zamimg, qué es, escena)
    "o_oro": ("inv_misc_coin_01", "ícono de monedas de oro (montura de 100, oro por hora; puntos de venta en los mapas)", "intro reglas fichas mapas"),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def wiki_info(nombres):
    out = {}
    for i in range(0, len(nombres), 20):
        q = urllib.parse.urlencode(dict(format="json", action="query", prop="imageinfo|fileusage", iiprop="url|size",
                                        fulimit=50, titles="|".join("File:" + n for n in nombres[i:i + 20])))
        for p in json.loads(get(WIKI_API + "?" + q))["query"]["pages"].values():
            ii = (p.get("imageinfo") or [{}])[0]
            out[p["title"][5:]] = dict(url=ii.get("url"), w=ii.get("width"), h=ii.get("height"),
                                       usado_en=[x["title"] for x in p.get("fileusage", [])])
    return out


def recortar(im, modo):
    W, H = im.size
    if modo == "carga_classic":   # marco de pergamino + logo de WoW arriba
        abajo = 0.79 if H / W > 0.78 else 0.825
        return im.crop((int(W * 0.015), int(H * 0.25), int(W * 0.985), int(H * abajo)))
    return im


def guardar(slug, im):
    if max(im.size) >= 1000:
        g = im.convert("RGB")
        g.thumbnail((1920, 1920), Image.LANCZOS)
        g.save(os.path.join(PAN, slug + ".jpg"), quality=92)
    if max(im.size) < 400:  # íconos y modelos pequeños: ampliar
        f = 320 / max(im.size) if slug.startswith("o_") else 2
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    im.thumbnail((900, 900), Image.LANCZOS)
    im.save(os.path.join(PEG, slug + ".png"))
    return im.size


def icono_url(nombre):
    return f"https://wow.zamimg.com/images/wow/icons/large/{nombre}.jpg"


def main(solo=None):
    credf = os.path.join(PEG, "_creditos.json")
    cred = json.load(open(credf, encoding="utf-8")) if os.path.isfile(credf) else {}
    quiere = (lambda s: s in solo) if solo else (lambda s: True)
    w = {k: v for k, v in WIKI.items() if quiere(k)}
    info = wiki_info(sorted({v[0] for v in w.values()})) if w else {}
    for slug, (arch, modo, que, esc) in w.items():
        ii = info.get(arch) or info.get(arch.replace("_", " "))
        if not ii or not ii["url"]:
            print("FALTA", slug, arch)
            continue
        im = recortar(Image.open(io.BytesIO(get(ii["url"]))).convert("RGBA"), modo)
        tam = guardar(slug, im)
        cred[slug] = dict(tipo="lugar", fuente="warcraft.wiki.gg", archivo="File:" + arch, url=ii["url"].split("?")[0],
                          pagina_archivo="https://warcraft.wiki.gg/wiki/File:" + urllib.parse.quote(arch.replace(" ", "_")),
                          identidad=que, usado_en=ii["usado_en"], escena=esc, original=f"{ii['w']}x{ii['h']}", recorte=modo,
                          pegatina=f"{tam[0]}x{tam[1]}", pantalla=os.path.isfile(os.path.join(PAN, slug + ".jpg")),
                          autor=PRENSA if arch.startswith(("Zones ", "Dungeon ")) else "captura/arte de Blizzard en la wiki")
        print(slug, tam)
    for slug, (did, npc, nombre, que, esc) in MODELOS.items():
        if not quiere(slug):
            continue
        url = f"https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/{did % 256}/{did}.webp"
        try:
            im = Image.open(io.BytesIO(get(url))).convert("RGBA")
        except Exception as e:
            print("FALTA modelo", slug, did, e)
            continue
        caja = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if caja:
            m = int(0.04 * max(im.size))
            im = im.crop((max(0, caja[0] - m), max(0, caja[1] - m), min(im.width, caja[2] + m), min(im.height, caja[3] + m)))
        tam = guardar(slug, im)
        cred[slug] = dict(tipo="criatura", fuente="Wowhead Forever (modelo 3D, webthumb classicplus)", url=url,
                          pagina=f"https://www.wowhead.com/forever/npc={npc}",
                          identidad=f"{nombre} (npc {npc}): {que}; displayId {did} (página de Wowhead Forever, 25-nov)",
                          escena=esc, pegatina=f"{tam[0]}x{tam[1]}", cara=f"caras/{slug}.png")
        print(slug, tam)
    for slug, (tipo, i, que, esc) in ICONOS.items():
        if not quiere(slug):
            continue
        j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/{tipo}/{i}?locale=0"))
        mx = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/{tipo}/{i}?locale=11")).get("name")
        url = icono_url(j["icon"])
        tam = guardar(slug, Image.open(io.BytesIO(get(url))).convert("RGBA"))
        cred[slug] = dict(tipo="objeto", fuente="Wowhead Forever (ícono)", url=url, tooltip=f"https://www.wowhead.com/forever/{tipo}={i}",
                          identidad=f"{tipo} {i}: {j.get('name')} / es-MX «{mx}» — {que}", icono=j["icon"], escena=esc,
                          pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, j.get("name"), "|", mx, "|", j["icon"])
    for slug, (n, que, esc) in ICONO_DIRECTO.items():
        if not quiere(slug):
            continue
        url = icono_url(n)
        tam = guardar(slug, Image.open(io.BytesIO(get(url))).convert("RGBA"))
        cred[slug] = dict(tipo="objeto", fuente="Wowhead (ícono genérico por nombre)", url=url, identidad=que, icono=n, escena=esc,
                          pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, n)
    for slug, (did, nota) in EQUIPADO.items():
        if not quiere(slug):
            continue
        url = f"https://wow.zamimg.com/modelviewer/classicplus/webthumbs/item/{did % 256}/{did}.png"
        im = Image.open(io.BytesIO(get(url))).convert("RGBA")
        fondo = Image.new("RGBA", im.size, (255, 255, 255, 255))
        fondo.alpha_composite(im)
        fondo.convert("RGB").save(os.path.join(PEG, "eq_" + slug + ".jpg"), quality=92)
        cred.setdefault(slug, {}).update(equipado=f"pegatinas/eq_{slug}.jpg", fuente_equipado=url, nota_equipado=nota)
        print("eq", slug, did)
    json.dump(dict(sorted(cred.items())), open(credf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hoja()


def hoja():
    fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png") and not f.startswith("com_"))
    col, cw, ch = 7, 300, 230
    h = Image.new("RGB", (col * cw, ((len(fs) + col - 1) // col) * ch), (40, 40, 40))
    d = ImageDraw.Draw(h)
    fnt = ImageFont.truetype("arialbd.ttf", 17)
    for n, f in enumerate(fs):
        im = Image.open(os.path.join(PEG, f)).convert("RGBA")
        tam = im.size
        im.thumbnail((cw - 10, ch - 42))
        x, y = (n % col) * cw + 5, (n // col) * ch + 5
        h.paste(im, (x, y), im)
        d.text((x, y + ch - 36), f[:-4][:28], fill=(255, 220, 80), font=fnt)
        d.text((x + 240, y + ch - 36), f"{tam[0]}", fill=(180, 180, 180), font=fnt)
    h.save(os.path.join(D, "previews", "pegatinas_hoja.jpg"), quality=85)
    print("hoja:", len(fs))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
