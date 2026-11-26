# -*- coding: utf-8 -*-
"""Pegatinas de «La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (25-nov-2026; adaptado de wow_errores_60/_pegatinas.py).
Una por cosa que NOMBRA la voz; identidad = id de Wowhead Forever o archivo concreto de la wiki.
- o_<slug> = ÍCONO de objeto/hechizo/receta: id de videos/_investigacion_wow_ruta_profesiones.md («En pantalla») o del buscador de
  Wowhead Forever (www.wowhead.com/forever/search/suggestions-template) → API de tooltips de Wowhead FOREVER
  (nether.wowhead.com/forever/tooltip/<item|spell>/<id>; locale=0 inglés, locale=11 es-MX para comprobar el nombre)
  → wow.zamimg.com/images/wow/icons/large/<icon>.jpg (56 px, ampliado a 320: solo rel/cam/ficha).
  Los 12 íconos de profesión salen del hechizo de la profesión (Minería 2575, Herrería 2018…), también por tooltip.
- PNJ con pin en el mapa mundial de Wowhead Forever (nether.wowhead.com/forever/data/world-map, campo «model» del PNJ, leído el 25-nov):
  modelo 3D de Wowhead Forever (webthumb classicplus) = el PNJ tal como está en Forever.
- Jefes que sueltan planos y lugares: ARCHIVO CONCRETO de warcraft.wiki.gg (capturas del juego de la página del PNJ; capturas oficiales de
  Forever «Zones_*», «Dungeon_*», «Camping_Players_*»; pantallas de carga de Classic). Nada de Hearthstone, TCG, cómic, fan art ni Retail nuevo.
python _pegatinas.py [slug…] → pegatinas/<slug>.png (≤ 900 px) + pantallas/<slug>.jpg (1920, si el original es ≥ 1000) + previews/pegatinas_hoja.jpg
NO toca los com_*.png (tarjetas de comentarios: _com_tarjetas.py)."""
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
#   recorte: None · "carga_classic" (800x600 / 1280x1024 con marco y logo)
WIKI = {
    # --- lugares
    "monte_hyjal": ("Zones Hyjal 025.png", None, "«Zones Hyjal» (galería de Forever) = Monte Hyjal, zona de Forever", "intro p01 p04 p08 p12"),
    "monte_hyjal_2": ("Zones Hyjal 032.jpg", None, "«Zones Hyjal» (galería de Forever) = Monte Hyjal", "p01 p03"),
    "claros_del_rio": ("Zones Riverglades 035.jpg", None, "«Zones Riverglades» (galería de Forever) = Claros del Río; imagen principal de la página Riverglades", "p01 p03 p04 p06"),
    "claros_del_rio_2": ("Zones Riverglades 039.jpg", None, "«Zones Riverglades» (galería de Forever) = Claros del Río", "p01"),
    "shendralas": ("Zones Shendralas 024.jpg", None, "«Zones Shendralas» (galería de Forever) = Shen'dralas", "p07 p08"),
    "campamento": ("Camping Players 063.jpg", None, "«Camping Players» (galería de Forever; páginas Camping y World of Warcraft: Forever) = campamento", "intro reglas p10"),
    "campamento_2": ("Camping Players 064.jpg", None, "«Camping Players» (galería de Forever) = campamento", "p10"),
    "profundidades_roca_negra": ("Blackrock Depths loading screen.jpg", "carga_classic", "pantalla de carga de Profundidades de Roca Negra (Classic)", "p01 p02"),
    "minas_muerte": ("The Deadmines loading screen.jpg", "carga_classic", "pantalla de carga de Las Minas de la Muerte (Classic; imagen principal de la página Deadmines)", "p02 p03 p10"),
    "stratholme": ("Stratholme loading screen.jpg", "carga_classic", "pantalla de carga de Stratholme (Classic)", "p03 p08"),
    "scholomance": ("Scholomance loading screen.jpg", "carga_classic", "pantalla de carga de Scholomance (Classic)", "p05 p07"),
    "cuevas_lamentos": ("Wailing Caverns loading screen.jpg", "carga_classic", "pantalla de carga de las Cuevas de los Lamentos (Classic)", "p06 p10"),
    "uldaman": ("Uldaman loading screen.jpg", "carga_classic", "pantalla de carga de Uldaman (Classic)", "p09"),
    "templo_sumergido": ("Temple of Atal'Hakkar loading screen.jpg", "carga_classic", "pantalla de carga del Templo de Atal'Hakkar = Templo Sumergido (Classic)", "p11"),
    "brazanegra": ("Blackfathom Deeps loading screen.jpg", "carga_classic", "pantalla de carga de las Cavernas de Brazanegra (Classic)", "p11"),
    "ciudad_dalaran": ("Dungeon Dalaran 073.jpg", None, "«Dungeon Dalaran» (galería de Forever; página City of Dalaran) = Ciudad de Dalaran", "p08 p09"),
    "bancal_creador": ("Dungeon ShaperTerrace 068.jpg", None, "«Shaper Terrace dungeon» (galería de Forever) = Bancal del Creador", "p09"),
    "excavacion_humedales": ("Dungeon ExcavationSite 055.jpg", None, "«Dungeon ExcavationSite» (galería de Forever; página Excavation Site: Wetlands)", "p04"),
    "torre_azora": ("Azora.jpg", None, "imagen de la página Tower of Azora (Torre de Azora, Elwynn)", "p09"),
    "refugio_roca_sol": ("Sun Rock Retreat.jpg", None, "imagen de la página Sun Rock Retreat (Refugio Roca del Sol, Sierra Espolón; captura de Classic)", "p09"),
    "gadgetzan": ("Gadgetzan.jpg", None, "imagen «Gadgetzan» (página Gadgetzan y Tanaris (Classic))", "p02 p03 p10"),
    "molino_tarren": ("Tarren Mill.jpg", None, "imagen «Tarren Mill» (página Tarren Mill y Hillsbrad Foothills (Classic))", "p08"),
    # --- jefes que sueltan planos y PNJ sin modelo en el mapa de Forever
    "embajador_latifuego": ("Flamelash.jpg", None, "imagen de la página Ambassador Flamelash (Embajador Latifuego, Profundidades de Roca Negra)", "p01"),
    "gilnid": ("Gilnid.jpg", None, "archivo «Gilnid» (página Gilnid, Las Minas de la Muerte; captura del juego)", "p02"),
    "argelmach": ("Golem Lord Argelmach.jpg", None, "archivo «Golem Lord Argelmach» (página del Señor gólem Argelmach; captura del juego, no el cómic)", "p02"),
    "sneed": ("Sneed.jpg", None, "archivo «Sneed» (página Sneed, Las Minas de la Muerte; captura del juego)", "p03"),
    "ezra_grimm": ("Ezra Grimm.jpg", None, "archivo «Ezra Grimm» (página Ezra Grimm, Stratholme)", "p03"),
    "ras_levescarcha": ("Ras Frostwhisper.jpg", None, "archivo «Ras Frostwhisper» (página Ras Frostwhisper = Ras Levescarcha, Scholomance; no el HS)", "p05"),
    "lady_anacondra": ("Lady Anacondra.jpg", None, "archivo «Lady Anacondra» (página Lady Anacondra, Cuevas de los Lamentos; no el HS)", "p06"),
    "vectus": ("Vectus.jpg", None, "imagen de la página Vectus (Scholomance)", "p07"),
    "baronesa_anastari": ("Baroness Anastari.jpg", None, "imagen de la página Baroness Anastari (Baronesa Anastari, Stratholme)", "p08"),
    "annora": ("Annora.jpg", None, "imagen de la página Annora (maestra de encantamiento en Uldaman)", "p09"),
    "lord_serpentis": ("Lord Serpentis.jpg", None, "imagen de la página Lord Serpentis (Cuevas de los Lamentos)", "p10"),
    "cocinitas": ("Cookie.jpg", None, "archivo «Cookie» (página Cookie = Cocinitas, Las Minas de la Muerte; captura del juego, no el HS)", "p10"),
    "dirge": ("Dirge Quikcleave.jpg", None, "imagen de la página Dirge Quikcleave (Dirge Hojágil, Gadgetzan: misión de cocina de artesano)", "p10"),
    "gelihast": ("Gelihast.jpg", None, "imagen de la página Gelihast (Cavernas de Brazanegra)", "p11"),
    "jammalan": ("Jammal'an.jpg", None, "imagen de la página Jammal'an the Prophet (Templo Sumergido)", "p11"),
}
# Modelos 3D de Wowhead FOREVER: displayId = campo «model» del pin del PNJ en nether.wowhead.com/forever/data/world-map (25-nov)
MODELOS = {
    "norzsh": (145037, "Norzsh (npc 267328), entrenador JÚNIOR de minería de Durotar (PNJ nuevo de Forever)", "reglas p01"),
    "kelsey_fargo": (144024, "Kelsey Fargo (npc 247226), entrenadora JÚNIOR de minería de Elwynn (PNJ nuevo de Forever)", "reglas p01"),
    "saru_steelfury": (1377, "Saru Steelfury (npc 3355), herrería experto, Orgrimmar", "p02"),
    "bengus_deepforge": (3097, "Bengus Deepforge (npc 4258), herrería experto, Forjaz", "p02"),
    "brikk": (7161, "Brikk Keencraft / Brikk Finoficio (npc 2836), herrería artesano, Bahía del Botín", "p02"),
    "derotain": (14668, "Derotain Mudsipper / Derotain Sorbelodo (npc 14567), Tanaris: misiones de piezas imperiales", "p02"),
    "roxxik": (10472, "Roxxik (npc 11017), ingeniería experto, Orgrimmar", "p03"),
    "springspindle": (3117, "Springspindle Fizzlegear (npc 5174), ingeniería experto, Forjaz", "p03"),
    "kayleena": (142809, "Kaylaena Springwhisper / Kayleena Encantaflores (npc 249235), ingeniería artesano, Monte Hyjal (PNJ nuevo de Forever)", "p03"),
    "rogvar": (4380, "Rogvar (npc 1386), alquimia artesano (Horda), Pantano de las Penas", "p05"),
    "kylanna": (7018, "Kylanna Windwhisper (npc 7948), alquimia artesano (Alianza), Feralas", "p05"),
    "shurome": (141677, "Master Mycologist Shurome / Maestro micólogo Shurome (npc 259585), alquimia 1-300, Frondavil (PNJ nuevo de Forever)", "p05"),
    "una": (2127, "Una (npc 3007), peletería experto, Cima del Trueno", "p07"),
    "telonis": (2270, "Telonis (npc 4212), peletería experto, Darnassus", "p07"),
    "hahrana": (10623, "Hahrana Ironhide / Hahrana Pielférrea (npc 11098), peletería artesano (Horda), Feralas", "p07"),
    "drakk": (10622, "Drakk Stonehand (npc 11097), peletería artesano (Alianza), Tierras del Interior", "p07"),
    "josef_gregorian": (2634, "Josef Gregorian (npc 4576), sastrería experto, Entrañas", "p08"),
    "georgio_bolero": (1502, "Georgio Bolero (npc 1346), sastrería experto, Ventormenta", "p08"),
    "daryl_stack": (3655, "Daryl Stack (npc 2399), sastrería artesano (Horda), Molino Tarren", "p08"),
    "timothy_worthington": (10587, "Timothy Worthington (npc 11052), sastrería artesano (Alianza), Theramore", "p08"),
    "pexmit": (121882, "Pexmit (npc 266901), vendedor raro de Monte Hyjal (PNJ nuevo de Forever)", "p08 p12"),
    "hgarth": (10611, "Hgarth (npc 11074), encantamiento experto (Horda), Sierra Espolón", "p09"),
    "kitta": (10610, "Kitta Firewind / Kitta Vientofuego (npc 11072), encantamiento experto (Alianza), Torre de Azora", "p09"),
    "wulan": (12036, "Wulan (npc 12033), vende el libro de cocina de experto (Horda), Desolace", "p10"),
    "shandrina": (2068, "Shandrina (npc 3955), vende el libro de cocina de experto (Alianza), Vallefresno", "p10"),
    "viejo_heming": (4491, "Old Man Heming / Viejo Heming (npc 2626), libro de pesca de experto, Bahía del Botín", "p11"),
    "nat_pagle": (13099, "Nat Pagle (npc 12919), misión de pesca de artesano, Marjal Revolcafango", "p11"),
    "deneb": (1506, "Deneb Walker / Deneb Camino (npc 2805), libro de primeros auxilios de experto (Alianza), Arathi", "p12"),
    "balai": (13529, "Balai Lok'Wein (npc 13476), libro de primeros auxilios de experto (Horda), Marjal", "p12"),
    "gregory_victor": (12928, "Doctor Gregory Victor (npc 12920), Atenciones médicas (Horda), Sentencia", "p12"),
    "vanhowzen": (12930, "Doctor Gustaf VanHowzen (npc 12939), Atenciones médicas (Alianza), Theramore", "p12"),
    "ortak": (136513, "Ortak Lomgok (npc 244512), cocinero y posadero de la Horda en Flora Antigua, Monte Hyjal (PNJ nuevo de Forever)", "p12"),
}
# Íconos: slug: (tipo, id, qué dice la voz, escena)
ICONOS = {
    # --- las 12 profesiones (hechizo de la profesión)
    "o_prof_mineria": ("spell", 2575, "profesión Minería", "reglas p01 combos"),
    "o_prof_herreria": ("spell", 2018, "profesión Herrería", "reglas p02 combos"),
    "o_prof_ingenieria": ("spell", 4036, "profesión Ingeniería", "reglas p03 combos"),
    "o_prof_herboristeria": ("spell", 2366, "profesión Herboristería", "reglas p04 combos"),
    "o_prof_alquimia": ("spell", 2259, "profesión Alquimia", "reglas p05 combos"),
    "o_prof_desuello": ("spell", 8613, "profesión Desuello", "reglas p06 combos"),
    "o_prof_peleteria": ("spell", 2108, "profesión Peletería", "reglas p07 combos"),
    "o_prof_sastreria": ("spell", 3908, "profesión Sastrería", "reglas p08 combos"),
    "o_prof_encantamiento": ("spell", 7411, "profesión Encantamiento", "reglas p09 legado combos"),
    "o_prof_cocina": ("spell", 2550, "profesión Cocina", "reglas p10 combos"),
    "o_prof_pesca": ("spell", 7620, "profesión Pesca", "reglas p11 combos"),
    "o_prof_primeros_auxilios": ("spell", 3273, "profesión Primeros auxilios", "reglas p12 combos"),
    # --- intro / reglas
    "o_pocion_sanacion_sublime": ("item", 13446, "Poción de sanación sublime", "intro p12 cierre"),
    "o_telar": ("item", 279959, "Telar (objeto de campamento de sastrería, 300)", "intro p08"),
    "o_hoguera_basica": ("item", 279981, "Hoguera básica (la de oficial y experto usan el mismo ícono)", "intro p10"),
    "o_bolsa_componentes_lino": ("spell", 1257013, "Bolsa de componentes de lino (la de lana: mismo ícono)", "reglas p08 combos"),
    # --- p01 minería
    "o_mena_cobre": ("item", 2770, "Mena de cobre", "p01"),
    "o_mena_estano": ("item", 2771, "Mena de estaño", "p01"),
    "o_mena_plata": ("item", 2775, "Mena de plata", "p01"),
    "o_mena_hierro": ("item", 2772, "Mena de hierro", "p01"),
    "o_mena_oro": ("item", 2776, "Mena de oro", "p01"),
    "o_mena_mitril": ("item", 3858, "Mena de mitril", "p01"),
    "o_mena_veraplata": ("item", 7911, "Mena de veraplata", "p01"),
    "o_mena_torio": ("item", 10620, "Mena de torio", "p01"),
    "o_mena_torio_pesada": ("item", 248815, "Mena de torio pesada (única mena nueva, Monte Hyjal)", "intro p01 cierre"),
    "o_barra_torio_pesada": ("item", 251291, "Barra de torio pesada (se funde en la Fundición de magma)", "p01"),
    "o_pirita": ("item", 249391, "Pirita (escaso)", "p01"),
    "o_bauxita": ("item", 249425, "Bauxita (escaso)", "p01"),
    "o_pecblenda": ("item", 249426, "Pecblenda (escaso)", "p01"),
    "o_barra_azerotio": ("item", 249726, "Barra de azerotio", "p01"),
    "o_fundicion_magma": ("item", 279952, "Fundición de magma (objeto de campamento, 300)", "p01"),
    "o_magnetita": ("item", 279960, "Magnetita (objeto de campamento, 20)", "p01"),
    "o_jardin_rocoso": ("item", 279948, "Jardín rocoso (objeto de campamento, 140)", "p01"),
    # --- p02 herrería
    "o_piedra_pulir_burda": ("item", 3478, "Piedra de pulir burda", "p02"),
    "o_barra_bronce": ("item", 2841, "Barra de bronce", "p02"),
    "o_brazales_hierro_verde": ("item", 3835, "Brazales de hierro verde", "p02"),
    "o_barra_torio": ("item", 12359, "Barra de torio (500-1200 en el último tramo)", "p02 p03 combos"),
    "o_diseno_peto_bendecidas": ("item", 251446, "Diseño: peto de placas bendecidas", "p02"),
    "o_cajon_arrebatado": ("item", 248549, "Cajón arrebatado (Waylaid Crate) del Favor de comerciante", "p02"),
    "o_rueda_afilar": ("item", 279944, "Rueda de afilar (objeto de campamento, 20)", "p02"),
    "o_yunque": ("item", 279988, "Yunque (objeto de campamento, 140)", "p02"),
    "o_forja_maestra": ("item", 279955, "Forja maestra (objeto de campamento, 300)", "p02"),
    # --- p03 ingeniería
    "o_polvo_explosivo_tosco": ("item", 4357, "Polvo explosivo tosco", "p03"),
    "o_llave_arco_voltaico": ("item", 6219, "Llave inglesa de arco voltaico", "p03"),
    "o_oveja_explosiva": ("item", 4384, "Oveja explosiva", "p03"),
    "o_tubo_torio": ("item", 16000, "Tubo de torio", "p03"),
    "o_dinamita_saft": ("item", 260792, "Dinamita SAF-T", "p03"),
    "o_bolsa_bombas_cobre": ("item", 285275, "Bolsa de bombas de cobre (arma arrojadiza sin munición)", "p03"),
    "o_parapente_goblin": ("item", 260825, "Parapente goblin ultraliviano", "p03"),
    "o_robot_componentes": ("item", 279950, "Robot de componentes (objeto de campamento, 20)", "p03"),
    "o_robot_reparacion": ("item", 279949, "Robot de reparación (objeto de campamento, 140)", "p03"),
    "o_banco_anarquista": ("item", 279989, "Banco de trabajo de anarquista (objeto de campamento, 300)", "p03"),
    # --- burla0
    "o_barra_cobre": ("item", 2840, "Barra de cobre (el «lingote de cobre» de la burla a Goca)", "burla0"),
    # --- p04 herboristería
    "o_flor_paz": ("item", 2447, "Flor de paz", "p04 p12"),
    "o_hojaplata": ("item", 765, "Hojaplata", "p04"),
    "o_marregal": ("item", 785, "Marregal", "p04"),
    "o_brezospina": ("item", 2450, "Brezospina", "p04"),
    "o_sangrerregia": ("item", 3356, "Sangrerregia", "p04"),
    "o_mostacho_khadgar": ("item", 3358, "Mostacho de Khadgar", "p04"),
    "o_solea": ("item", 8838, "Solea", "p04"),
    "o_champinon_fantasma": ("item", 8845, "Champiñón fantasma", "p04"),
    "o_hojasueno": ("item", 13463, "Hojasueño", "p04"),
    "o_hojapesadilla": ("item", 248823, "Hojapesadilla (hierba nueva de Monte Hyjal)", "p04"),
    "o_salvia_demoniaca": ("item", 248821, "Salvia demoníaca (hierba nueva de Monte Hyjal)", "p04"),
    "o_loto_muerte": ("item", 248822, "Loto de la muerte (hierba nueva de Monte Hyjal)", "p04"),
    "o_semillas": ("item", 268415, "Semillas de hierbas comunes", "p04"),
    "o_invernadero": ("item", 279964, "Invernadero (objeto de campamento, 140)", "p04"),
    "o_injertador": ("item", 279947, "Injertador de semillas (objeto de campamento, 300)", "p04"),
    "o_vela_incienso": ("item", 279962, "Vela de incienso (objeto de campamento, 20)", "p04"),
    # --- p05 alquimia
    "o_elixir_fuerza_menor": ("spell", 1245250, "Elixir de fuerza menor (receta nueva de Forever)", "p05"),
    "o_elixir_defensa_menor": ("spell", 7183, "Elixir de defensa menor", "p05"),
    "o_tinte_ceruleo": ("item", 249409, "Tinte cerúleo", "p05 p08"),
    "o_tinte_magenta": ("item", 249430, "Tinte magenta", "p05"),
    "o_tinte_esmeralda": ("item", 249431, "Tinte verde esmeralda", "p05"),
    "o_elixir_oso_pardo": ("item", 250351, "Elixir del oso pardo", "p05"),
    "o_pozo_mana": ("item", 279956, "Pozo de maná (objeto de campamento, 20)", "p05"),
    "o_fermentador": ("item", 279970, "Fermentador (objeto de campamento, 140)", "p05"),
    "o_laboratorio_alquimia": ("item", 279990, "Laboratorio de alquimia (objeto de campamento, 300)", "p05"),
    # --- p06 desuello
    "o_cuero_ligero": ("item", 2318, "Cuero ligero", "p06 p07"),
    "o_cuero_pesado": ("item", 4234, "Cuero pesado", "p06"),
    "o_cuero_grueso": ("item", 4304, "Cuero grueso", "p07"),
    "o_cuero_basto": ("item", 8170, "Cuero basto", "p06 p07"),
    "o_cuero_pristino": ("item", 249427, "Cuero prístino", "p06"),
    "o_pellejo_pristino": ("item", 249428, "Pellejo prístino", "p06"),
    "o_escama_pristina": ("item", 249429, "Escama prístina", "p06"),
    "o_cuchillo_afilado": ("item", 269716, "Cuchillo para desollar afilado (+3, Horda)", "p06"),
    "o_silla_campamento": ("item", 279979, "Silla de campamento (objeto de campamento, 20)", "p06"),
    "o_guia_campo": ("item", 279969, "Guía de campo (objeto de campamento, 140)", "p06"),
    "o_banco_trampero": ("item", 279938, "Banco de trabajo de trampero (objeto de campamento, 300)", "p06"),
    # --- p07 peletería
    "o_zapatos_gamuza": ("item", 252467, "Zapatos de gamuza azul", "p07"),
    "o_patron_zapatos_gamuza": ("item", 252859, "Patrón: zapatos de gamuza azul", "p07"),
    "o_tienda_campamento": ("item", 279978, "Tienda de campamento (objeto de campamento, 20)", "p07 combos"),
    "o_expositor_curtido": ("item", 279941, "Expositor de curtido (objeto de campamento, 125)", "p07 combos"),
    "o_maquina_coser": ("item", 279945, "Máquina de coser (objeto de campamento, 300)", "p07"),
    # --- p08 sastrería
    "o_pano_lino": ("item", 2589, "Paño de lino", "p08"),
    "o_pano_seda": ("item", 4306, "Paño de seda", "p08"),
    "o_tejido_magico": ("item", 4338, "Paño de tejido mágico", "p08"),
    "o_pano_runico": ("item", 14047, "Paño rúnico", "p07 p08"),
    "o_hilo_runico": ("item", 14341, "Hilo rúnico", "p08"),
    "o_bolsa_tejido_magico_roja": ("item", 10051, "Bolsa de tejido mágico roja (14 casillas tras el hotfix)", "p08"),
    "o_patron_punos_runicos": ("item", 254124, "Patrón: puños de paño rúnico", "p08"),
    "o_estandarte_faccion": ("item", 279972, "Estandarte de facción (objeto de campamento, 20)", "p08"),
    "o_rueca": ("item", 279943, "Rueca (objeto de campamento, 140)", "p08"),
    # --- p09 encantamiento
    "o_mota_magia": ("item", 247786, "Mota de magia (reactivo nuevo de vendedor)", "p09"),
    "o_polvo_extrano": ("item", 10940, "Polvo extraño", "p09"),
    "o_esencia_magica_inferior": ("item", 10938, "Esencia mágica inferior", "p09"),
    "o_varita_novato": ("item", 247789, "Varita de práctica de novato", "p09"),
    "o_vara_arcanita": ("item", 16206, "Vara de arcanita (la vara rúnica de arcanita)", "p09"),
    "o_encantar_collar": ("spell", 1249059, "Encantar collar: agilidad (fórmula de Favor)", "p09"),
    "o_laud_encantado": ("item", 279976, "Laúd encantado (objeto de campamento, 20)", "p09"),
    "o_recuperador_arcano": ("item", 279985, "Recuperador arcano (objeto de campamento, 140)", "p09"),
    "o_forja_arcana": ("item", 279987, "Forja arcana (objeto de campamento, 300)", "p09"),
    "o_esencia_maleable": ("item", 274030, "Esencia maleable de la Naturaleza", "p09"),
    # --- p10 cocina

    "o_madera_simple": ("item", 4470, "Madera simple", "p10"),
    "o_libro_cocina_expertos": ("item", 16072, "Libro de cocina para expertos", "p10"),
    "o_huevo_gigante": ("item", 12207, "Huevo gigante", "p10"),
    "o_carne_almeja": ("item", 7974, "Carne de almeja sabrosa", "p10"),
    "o_queso_alterac": ("item", 8932, "Queso curado de Alterac", "p10"),
    "o_whimsyfin": ("item", 251524, "Whimsyfin (pez nuevo)", "p10"),
    "o_delicia_whimsyfin": ("item", 251525, "Savory Whimsyfin Delight (el plato del pez nuevo)", "p10"),
    "o_festin_cocinitas": ("item", 279957, "Festín de Cocinitas (objeto de campamento, 140)", "p10"),
    "o_varilla_cocinitas": ("item", 5198, "Varilla de remover de Cocinitas (Cookie's Stirring Rod)", "p10"),
    # --- p11 pesca
    "o_cana_pescar": ("item", 6256, "Caña de pescar", "p11"),
    "o_adorno_lustroso": ("item", 6529, "Adorno lustroso", "p11"),
    "o_adornos_brillantes": ("item", 6532, "Adornos brillantes", "p11"),
    "o_libro_pesca": ("item", 16083, "Pesca para expertos: La lubina y tú", "p11"),
    "o_cuenco_pescado": ("item", 279967, "Cuenco de pescado = la pecera (objeto de campamento, 20)", "p11"),
    "o_expositor_pesca": ("item", 279965, "Expositor de pesca (objeto de campamento, 140)", "p11"),
    "o_cabana_pesca": ("item", 279966, "Cabaña de pesca (objeto de campamento, 300)", "p11"),
    "o_almeja_bocazas": ("item", 7973, "Almeja bocazas", "p11"),
    "o_langosta_garraoscura": ("item", 13888, "Langosta garraoscura", "p11"),
    # --- p12 primeros auxilios
    "o_pocion_sanacion_menor": ("spell", 1244431, "Poción de sanación menor (receta de Primeros auxilios)", "p12"),
    "o_pocion_sanacion": ("spell", 1244433, "Poción de sanación (receta de Primeros auxilios)", "p05 p12"),
    "o_manual_sublime": ("item", 255729, "Manual: Poción de sanación sublime", "p12"),
    "o_cataplasma_simple": ("spell", 1259342, "Cataplasma simple", "p12"),
    "o_torniquete_lana": ("item", 255720, "Torniquete de lana", "p12"),
    "o_venda_lino": ("item", 1251, "Venda de lino", "p12 burla0"),
    "o_venda_runica_gruesa": ("item", 14530, "Venda de paño rúnico gruesa", "p12"),
    "o_libro_primeros_auxilios": ("item", 16084, "Primeros auxilios para expertos: Entre vendas", "p12"),
    "o_equipo_primeros_auxilios": ("item", 279968, "Equipo de primeros auxilios (objeto de campamento, 20)", "p12"),
    "o_estudio_toxinas": ("item", 279940, "Estudio de toxinas (objeto de campamento, 140)", "p12"),
    "o_laboratorio_peste": ("item", 279951, "Laboratorio de médico de la peste (objeto de campamento, 300)", "p12"),
}
ICONO_DIRECTO = {   # slug: (nombre del ícono en zamimg, qué es, escena)
    "o_oro": ("inv_misc_coin_01", "ícono de monedas de oro (costes de entrenamiento)", "reglas p08 p12"),
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
    if modo == "carga_classic":   # marco de pergamino + logo de WoW arriba (las de 5:4, 1280x1024, tienen el marco más alto)
        abajo = 0.79 if H / W > 0.78 else 0.825
        return im.crop((int(W * 0.015), int(H * 0.25), int(W * 0.985), int(H * abajo)))
    return im


ACLARAR = set()


def aclarar(im):
    a = im.getchannel("A") if im.mode == "RGBA" else None
    rgb = im.convert("RGB").point(lambda v: round(255 * (v / 255) ** 0.6))
    if a:
        rgb.putalpha(a)
    return rgb


def guardar(slug, im):
    if slug in ACLARAR:
        im = aclarar(im)
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
    cred = json.load(open(credf, encoding="utf-8")) if solo and os.path.isfile(credf) else {}
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
        cred[slug] = dict(fuente="warcraft.wiki.gg", archivo="File:" + arch, url=ii["url"].split("?")[0],
                          pagina_archivo="https://warcraft.wiki.gg/wiki/File:" + urllib.parse.quote(arch.replace(" ", "_")),
                          identidad=que, usado_en=ii["usado_en"], escena=esc, original=f"{ii['w']}x{ii['h']}", recorte=modo,
                          aclarada=slug in ACLARAR, pegatina=f"{tam[0]}x{tam[1]}",
                          autor=PRENSA if arch.startswith(("Zones ", "Dungeon ", "Raid ", "Camping ")) else "captura/arte de Blizzard en la wiki")
        print(slug, tam)
    for slug, (did, que, esc) in MODELOS.items():
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
        cred[slug] = dict(fuente="Wowhead Forever (modelo 3D)", url=url, identidad=que + f"; displayId {did} (mapa mundial de Wowhead Forever)",
                          escena=esc, pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, tam)
    for slug, (tipo, i, que, esc) in ICONOS.items():
        if not quiere(slug):
            continue
        j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/{tipo}/{i}?locale=0"))
        mx = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/{tipo}/{i}?locale=11")).get("name")
        url = icono_url(j["icon"])
        tam = guardar(slug, Image.open(io.BytesIO(get(url))).convert("RGBA"))
        cred[slug] = dict(fuente="Wowhead Forever (ícono)", url=url, tooltip=f"https://www.wowhead.com/forever/{tipo}={i}",
                          identidad=f"{tipo} {i}: {j.get('name')} / es-MX «{mx}» — {que}", icono=j["icon"], escena=esc,
                          pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, j.get("name"), "|", mx, "|", j["icon"])
    for slug, (n, que, esc) in ICONO_DIRECTO.items():
        if not quiere(slug):
            continue
        url = icono_url(n)
        tam = guardar(slug, Image.open(io.BytesIO(get(url))).convert("RGBA"))
        cred[slug] = dict(fuente="Wowhead (ícono genérico por nombre)", url=url, identidad=que, escena=esc, pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, n)
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
