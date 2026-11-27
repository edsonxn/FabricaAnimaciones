# -*- coding: utf-8 -*-
"""Coordenadas de «15 FARMEOS de ORO del 30 al 50 en WoW Forever» (25-nov-2026; adaptado de wow_ruta_profesiones/_coords_check.py).
Fuentes: INV = videos/_investigacion_wow_oro_30_50.md · WN = puntos de aparición del tooltip de PNJ de Wowhead Forever
(nether.wowhead.com/forever/tooltip/npc/<id>, campo map; centro = media de los puntos de la casilla de 5 % con más apariciones; leído el
25-nov, sale igual que la investigación) · WL = rótulo de subzona/pueblo del mapa mundial de Wowhead Forever (campo places; nombres es-MX de
/forever/mx/data/world-map) pasado a % de la zona con el rect de la zona · WP = pin de PNJ (vendedor, vuelo) del mismo archivo (campo pois;
side 1 = Alianza, 2 = Horda, 0 = los dos) · WM = nodos de recolección/pesca del mismo archivo (campo nodes).
Mapas de zona de zamimg: 1 % de la imagen = 1 de coordenada. Mapa «mundo» (teselas): coordenada de zona → lienzo (rect de la zona) → % del
recorte (mapas/_rects.json). Los x, y de PTS son los que van a P(x, y, rótulo, sub, foto) de mapa(...) en efectos.py.
5.º CAMPO OBLIGATORIO (cambio del usuario al kit, 25-nov): «icono» = o_<slug> de pegatinas/ (lo que se farmea ahí), cara del PNJ
(caras/<slug>.png) o ico:<ícono Wowhead>. «alt» = otra imagen real para el mismo punto (la cara de la criatura o la foto del lugar).
    python _coords_check.py      → previews/_coords_check_N.jpg (4 mapas por hoja, MIRARLAS) + aviso si falta algún ícono
    python _coords_check.py md   → imprime la tabla de _coords.md
Tipos: C = lugar con nombre · R = farmeo (grupo de criaturas, vetas, bancos) · P = PNJ · V = venta/vuelo · X = peligro (élites)."""
import json
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
I, WN, WL, WP, WM = "INV", "WN", "WL", "WP", "WM"
# rect de cada zona en el lienzo del mapa mundial de Wowhead Forever (campo places, kind=zone; leído el 25-nov)
ZR = {
    "desolace": [[12320, 15950], [16636, 18828]], "marjal": [[17320, 18336], [22360, 21696]],
    "tuercespina": [[35244, 25058], [41370, 29142]], "mil_agujas": [[16800, 20192], [21024, 23008]],
    "riverglades": [[39192, 20544], [43848, 23648]], "inhospitas": [[39372, 19990], [41760, 21582]],
    "pantano": [[39510, 23572], [41712, 25040]], "tanaris": [[16594, 22024], [23218, 26440]],
    "feralas": [[11160, 18656], [17832, 23104]], "alterac": [[36624, 12896], [39312, 14688]],
    "devastadas": [[38568, 24480], [41784, 26624]],
}
RECTS = json.load(open(os.path.join(D, "mapas", "_rects.json")))


def M(zona, x, y):
    """coordenada de zona → % del recorte «mundo»"""
    (x0, y0), (x1, y1) = ZR[zona]
    cx, cy = x0 + x / 100 * (x1 - x0), y0 + y / 100 * (y1 - y0)
    (a0, b0), (a1, b1) = RECTS["mundo"]["rect"]
    return round(100 * (cx - a0) / (a1 - a0), 1), round(100 * (cy - b0) / (b1 - b0), 1)


def m(zona, x, y, *resto):
    return M(zona, x, y) + resto


# clave: [(escena, x, y, rótulo, sub, icono, frase del guion, tipo, fuente, confianza, alt)]
PTS = {
    "desolace": [
        ("p15", 70.8, 76.8, "Poblado Magram", "33-38 · reaparecen más rápido", "o_pano_seda", "Los centauros del Poblado Magram, en Desolace", "C", WL, "ALTA", "poblado_magram"),
        ("p15", 67.6, 72.5, "Cazavientos y retadores", "33-34", "o_pano_seda", "con retadores, cazavientos y corremanadas", "R", WN, "ALTA (22 de 78 y 17 de 72 apariciones)", "cazavientos_magram"),
        ("p15", 72.5, 67.6, "Retadores y cazavientos", "segundo grupo", "o_pano_seda", "repartidos en varios grupos al sureste de la zona", "R", WN, "ALTA (10 + 10)", "retador_magram"),
        ("p15", 72.0, 76.7, "Corremanadas Magram", "34-35", "o_tejido_magico", "hacia el treinta y cinco empieza a caer el tejido mágico", "R", WN, "ALTA (10 de 51)", "corremanadas_magram"),
        ("p15", 67.8, 76.7, "Zarpósea Magram", "hienas 37-38", "zarposea_magram", "Ojo con sus hienas, las Zarpósea", "X", WN, "ALTA (solo 18 apariciones, mezcladas con los centauros)", "zarposea_magram"),
        ("p15", 55.5, 55.9, "Campamento del Espíritu Errante", "vende la Horda", "o_oro", "cuando la bolsa se llena, sales a vender", "V", WL, "ALTA (vendedor Muuran, side 2)", None),
        ("p15", 65.1, 8.3, "Punta de Nijel", "vende y vuela la Alianza", "o_oro", "cuando la bolsa se llena, sales a vender", "V", WL, "ALTA (5 vendedores + vuelo, side 1)", None),
    ],
    "marjal": [
        ("p14", 33.3, 22.8, "Cueva Niebla Negra", "35-38", "o_seda_sombras", "Las arañas de la Cueva Niebla Negra", "C", WL, "ALTA", "cueva_niebla_negra"),
        ("p14", 35.4, 22.3, "Arañas y ermitañas", "35-37", "o_seda_arana_espesa", "arañas Niebla Negra y ermitañas Niebla Negra", "R", WN, "ALTA (7 + 7; el grupo grande, 34.0, 21.8, está pegado al rótulo de la cueva)", "arana_niebla_negra"),
        ("p14", 34.5, 25.4, "Arañas Niebla Negra", "fuera de la cueva", "o_mandibula_arana", "Están fuera y dentro de la cueva, al norte del marjal", "R", WN, "ALTA (4 + 3)", "ermitana_niebla_negra"),
        ("p14", 36.3, 31.4, "Poblado Murohelecho", "vende la Horda", "o_oro", "La Horda vende al lado, en el Poblado Murohelecho", "V", WL, "ALTA (6 vendedores + vuelo, side 2)", "poblado_murohelecho"),
        ("p14", 65.0, 47.1, "Isla Theramore", "vende la Alianza", "o_oro", "La Alianza, en la Isla Theramore", "V", WL, "ALTA (13 vendedores + vuelo, side 1)", "theramore"),
        ("p12", 58.4, 61.7, "Cavapozos Fangorroca", "42-43", "o_almeja_boca_grande", "los cavapozos Fangorroca del Marjal Revolcafango", "R", WN, "ALTA (13 de 45)", "cavapozos_fangorroca"),
    ],
    "tuercespina": [
        ("p13", 37.7, 17.1, "Gorilas Velo de Bruma", "32-33 · 14 apariciones", "o_colmillo_gorila", "Los jóvenes viven al oeste del Lago Nazferiti", "R", WN, "ALTA (13 de 14)", "gorila_velo_bruma"),
        ("p13", 40.8, 16.0, "Lago Nazferiti", "", "o_pelo_gorila_burdo", "al oeste del Lago Nazferiti, en el norte de la selva", "C", WL, "ALTA", "lago_nazferiti"),
        ("p13", 32.5, 66.8, "Gorilas ancianos", "40-41 · Valle del Velo de Bruma", "o_colmillo_gorila", "Los ancianos, en el Valle del Velo de Bruma, más al sur", "R", WN, "ALTA (18 de 36; rótulo del valle 33.0, 66.2)", "gorila_velo_bruma_anciano"),
        ("p13", 35.2, 60.5, "Médico brujo Unbagwa", "La fiebre de Tuercespina", "unbagwa", "una misión, La fiebre de Tuercespina, pide colmillos", "P", WN, "ALTA", None),
        ("p13", 34.6, 62.2, "Mokk el Salvaje", "44 · sale en oleadas", "mokk", "para invocar a Mokk el Salvaje en oleadas", "P", WN, "ALTA (4 de 5 apariciones)", None),
        ("p13 p03", 31.9, 28.4, "Campamento Grom'Gol", "vende la Horda · buzón", "o_valija_mitril", "sales del Campamento Grom'Gol", "V", WL, "ALTA (8 vendedores + vuelo, side 2)", "gromgol"),
        ("p13", 38.2, 3.5, "Asentamiento Rebelde", "vende la Alianza", "o_oro", "(venta de la Alianza en el norte)", "V", WL, "MEDIA (1 vendedor, side 1)", None),
        ("p11", 33.6, 76.3, "Reptadores de las arenas del sur", "40-41 · almejas", "o_almeja_boca_grande", "los reptadores del sur de Tuercespina, cerca de Bahía del Botín", "R", WN, "MEDIA (solo 12 apariciones, en grupos de 2-3)", "reptador_arenas_sur"),
        ("p03", 27.1, 42.9, "Anguila escama pétrea", "5 bancos", "o_anguila_petrea", "también de los bancos de anguila escama pétrea", "R", WM, "ALTA", None),
        ("p03", 23.3, 57.2, "Anguila escama pétrea", "5 bancos", "o_anguila_petrea", "bajas por toda la costa oeste", "R", WM, "ALTA", None),
        ("p03", 27.4, 83.4, "Anguila escama pétrea", "8 bancos", "o_valija_mitril", "hasta Bahía del Botín, y vuelves", "R", WM, "ALTA", None),
        ("p03 p11", 27.2, 75.6, "Bahía del Botín", "vende (neutral)", "o_oro", "bajas por toda la costa oeste hasta Bahía del Botín", "V", WL, "ALTA (23 vendedores neutrales + vuelos)", "bahia_botin"),
    ],
    "mil_agujas": [
        ("p12", 70.8, 76.7, "El Desierto de Sal", "", "o_fragmento_caparazon", "Las tortugas brillavalva del Desierto de Sal", "C", WL, "ALTA", "desierto_sal"),
        ("p12", 73.2, 57.3, "Tortugas brillavalva", "30-31 · 71 apariciones", "o_carne_tortuga", "Son lentas, no pegan fuerte", "R", WN, "ALTA (15 de 71)", "tortuga_brillavalva"),
        ("p12", 82.7, 56.2, "Mordedores brillavalva", "34-35 · 64 apariciones", "o_fragmento_caparazon", "Los mordedores brillavalva están al este de las salinas", "R", WN, "ALTA (11 de 64)", "mordedor_brillavalva"),
        ("p12", 78.8, 62.5, "Cráter de la Comadreja", "", "o_cola_escamosa", "junto al Cráter de la Comadreja", "C", WL, "ALTA", None),
        ("p12", 80.4, 77.5, "Circuito del Espejismo", "vende (neutral)", "o_oro", "Y para vender, el Circuito del Espejismo, ahí mismo", "V", WL, "ALTA (7 vendedores, side 0)", "circuito_espejismo"),
    ],
    "riverglades": [
        ("p11", 71.6, 67.5, "Reptadores de arena", "36-37 · 85 apariciones", "o_carne_cangrejo", "Son los cangrejos de la costa, al sur del Puerto Polvomecha", "R", WN, "ALTA (14 de 85)", "reptador_arena"),
        ("p11", 76.8, 61.9, "Reptadores de arena", "", "o_carne_cangrejo", "sueltan carne de cangrejo tierna en cuatro de cada diez muertes", "R", WN, "ALTA (9)", "reptador_arena"),
        ("p11", 78.9, 55.2, "Puerto Polvomecha", "vende (neutral)", "o_oro", "al sur del Puerto Polvomecha", "V", WL, "ALTA (12 vendedores, side 0)", "puerto_polvomecha"),
        ("p11", 79.0, 54.2, "Fimbo Grasapuños", "Sabores de mar", "fimbo", "en el mismo puerto hay una misión con estos cangrejos, Sabores de mar", "P", WN, "ALTA (a 1 % del rótulo del puerto: usar uno u otro)", None),
        ("p06", 58.7, 52.8, "Cazadoras llanagreste", "38-39", "o_cola_blanda", "las cazadoras llanagreste, al sur de Rog'mar", "R", WN, "ALTA (10 de 26)", "cazadora_llanagreste"),
        ("p06", 59.6, 45.9, "Rog'mar", "vende y vuela la Horda", "o_oro", "al sur de Rog'mar", "V", WL, "ALTA (side 2)", None),
        ("p04", 54.8, 75.8, "Cortijo de Wheeler", "Benjy Wheeler", "benjy_wheeler", "Están al sur del Cortijo de Wheeler, en la zona nueva", "C", WL, "ALTA (Benjy en 54.8, 73.0)", "cortijo_wheeler"),
        ("p04", 54.5, 86.9, "Coyotes de las llanuras", "36-37 · siempre ~4 vivos", "o_cola_tupida", "Y reaparecen a lo loco", "R", WN, "ALTA (9 de 14; 5 más en 54.1, 83.5)", "coyote_llanuras"),
        ("p04", 54.4, 67.6, "Merodeadores coyote", "36-37", "o_melena_espesa", "Sueltan la cola tupida suave", "R", WN, "ALTA, pero quedan al NORTE del cortijo (67.6 < 75.8), no al sur", "merodeador_coyote"),
        ("p04", 54.2, 84.0, "Sootfur", "38 · misión de Benjy", "sootfur", "Hay un coyote con nombre, Sootfur", "P", WN, "ALTA (2 de 8; las otras 6 en 54.5, 86.2, encima del grupo de coyotes)", None),
        ("p04", 64.4, 83.0, "Fortaleza de Farholde", "vende y vuela (neutral)", "o_oro", "(venta más cercana a los coyotes)", "V", WL, "ALTA (11 vendedores + vuelo, side 0; el guion no la nombra)", None),
    ],
    "inhospitas": [
        ("p10", 82.5, 32.2, "Crías del Barranco Lethlor", "41-43 · 110 apariciones", "o_glandula_llamas", "al este de la zona, alrededor del barranco", "R", WN, "ALTA (21 de 110)", "cria_lethlor"),
        ("p10", 77.7, 62.8, "Crías del Barranco Lethlor", "", "o_vastago_oscuro", "Y sueltan una mascota, el Vástago oscuro", "R", WN, "ALTA (10)", "cria_lethlor"),
        ("p10", 79.2, 53.9, "Barranco Lethlor", "élites en el centro: por los bordes", "o_glandula_llamas", "Cuidado con los élites en el centro del barranco", "C", WL, "ALTA", "barranco_lethlor"),
        ("p10", 78.2, 46.2, "Vetas de mitril", "16 puntos en el este", "o_mena_mitril", "con vetas de mitril alrededor", "R", WM, "ALTA (78.0, 48.4 · 78.3, 43.9 · 78.4, 46.2)", None),
        ("p05", 17.6, 41.9, "Elementales inferiores", "37-39 · más desde el 13-nov", "o_piedra_inerte", "Los inferiores, del treinta y siete al treinta y nueve, junto a Kargath", "R", WN, "ALTA (16 de 58)", "elemental_roca_inferior"),
        ("p05", 4.3, 47.4, "Kargath", "vende y vuela la Horda", "o_oro", "junto a Kargath", "V", WL, "ALTA (side 2)", "kargath"),
        ("p05", 25.8, 45.0, "Lotwil Veriatus", "vendedor de los dos bandos", "o_oro", "(venta junto a los inferiores)", "V", WP, "ALTA (pin de vendedor, side 0; el guion no lo nombra)", None),
        ("p05", 43.1, 82.4, "Elementales de roca", "39-40", "o_tierra_elemental", "Los normales, al sur, junto a la Explanada del Espejismo", "R", WN, "ALTA (17 de 90)", "elemental_roca"),
        ("p05", 37.7, 72.0, "Explanada del Espejismo", "", "o_piedra_lisa", "junto a la Explanada del Espejismo", "C", WL, "ALTA", "explanada_espejismo"),
        ("p05", 2.8, 82.0, "Elementales superiores", "42-44", "o_sal_roca", "Y los superiores, del cuarenta y dos, al suroeste", "R", WN, "ALTA (18 de 83)", "elemental_roca_superior"),
        ("p05", 42.4, 52.6, "Jazzrik", "vende la Alianza", "o_oro", "(venta de la Alianza en el centro)", "V", WP, "ALTA (pin de vendedor, side 1, Valle de los Colmillos)", None),
    ],
    "pantano": [
        ("p09", 82.4, 92.1, "Múrlocs de marisma", "41-42 · playa", "o_almeja_boca_grande", "Hay cuatro tipos en la mitad sur de la playa", "R", WN, "ALTA (22 de 71)", "murloc_marisma"),
        ("p09", 86.4, 82.1, "Múrlocs y vomitatintas", "41-43", "o_perla_oro", "a veces, una perla", "R", WN, "ALTA (16 + 16)", "vomitatintas_marisma"),
        ("p09", 81.5, 80.7, "Puesto Juncobruma", "empieza aquí al 40", "o_carne_almeja", "Empieza por la playa al cuarenta, junto al Puesto Juncobruma", "C", WL, "ALTA", "puesto_juncobruma"),
        ("p09", 62.7, 87.2, "Oráculos y comecarnes", "43-45 · té soleado", "o_receta_te_soleado", "un grupo grande hacia la Cueva Stagalbog", "R", WN, "ALTA (19 + 19)", "oraculo_marisma"),
        ("p09", 66.1, 77.3, "Cueva Stagalbog", "demasiados juntos", "o_perla_negra", "La parte de la cueva, mejor más tarde", "C", WL, "ALTA", "cueva_stagalbog"),
        ("p06", 42.2, 42.4, "Jaguares del pantano", "36-37 · 184 apariciones", "o_cola_blanda", "Los jaguares del Pantano de las Penas", "R", WN, "ALTA (20 de 184)", "jaguar_pantano"),
        ("p06", 22.2, 42.4, "Jaguares del pantano", "oeste", "o_bigote_cerdas", "Sueltan colas y bigotes de felino", "R", WN, "ALTA (10)", "jaguar_pantano"),
        ("p06 p09 p01", 46.0, 53.8, "Rocal", "vende y vuela la Horda", "o_oro", "La Horda vende en Rocal, en medio del pantano", "V", WL, "ALTA (10 vendedores + vuelo, side 2)", "rocal"),
        ("p06", 26.4, 31.6, "El Puerto", "vendedor de los dos bandos", "o_oro", "un aviso para la Alianza", "V", WP, "MEDIA (Masat T'andr, side 0; el guion no lo nombra)", None),
    ],
    "tanaris": [
        ("p08", 44.4, 38.7, "Hienas Llagapata", "44-45", "o_melena_espesa", "Sueltan la melena espesa", "R", WN, "ALTA (7 de 60; hay más al este, 63.1, 43.1, fuera de las Arenas)", "hiena_llagapata"),
        ("p08", 48.5, 43.1, "Hienas Llagapata", "", "o_pata_trofeo", "y la pata de trofeo grande", "R", WN, "ALTA (6)", "hiena_llagapata"),
        ("p08", 47.5, 36.9, "Rocs de fuego", "43-45 · huevos gigantes", "o_huevo_gigante", "Y si pasa un roc, mátalo también", "R", WN, "ALTA (8 de 48; el grupo mayor, 48.6, 43.1, está encima de las hienas)", "roc_fuego"),
        ("p08", 45.4, 42.9, "Arenas Abisales", "triángulo de esqueletos", "o_carne_lobo_tierna", "las hienas Llagapata de las Arenas Abisales", "C", WL, "ALTA", "arenas_abisales"),
        ("p08", 51.2, 27.5, "Gadgetzan", "vende (neutral)", "o_oro", "Para vender, Gadgetzan, al norte de las dunas", "V", WL, "ALTA", "gadgetzan"),
    ],
    "feralas": [
        ("p07", 42.1, 21.9, "Tronadores Groddoc", "49-50", "o_mechon_gorila", "Tronadores Groddoc y patriarcas Cueracero", "R", WN, "ALTA (7 de 29)", "tronador_groddoc"),
        ("p07", 47.8, 27.3, "Patriarcas Cueracero", "48-49", "o_hueso_oso", "El hueso de oso grande, casi quince platas", "R", WN, "ALTA (9 de 44; el grupo mayor, 42.9, 22.1, está encima de los tronadores)", "patriarca_cueracero"),
        ("p07", 45.0, 22.7, "Los Dos Colosos", "", "o_mandibula_oso", "alrededor de Los Dos Colosos", "C", WL, "ALTA", "dos_colosos"),
        ("p07", 45.0, 25.4, "Gregan Brewspewer", "vendedor de los dos bandos", "o_oro", "(venta junto a los gorilas)", "V", WP, "ALTA (pin, side 0; el guion no lo nombra)", None),
        ("p07", 57.0, 53.9, "Simios Groddoc", "42-43 · solo 9", "o_pelo_gorila_burdo", "los simios Groddoc y los osos Cueracero del centro de la zona", "R", WN, "MEDIA (4 de 9 apariciones)", "simio_groddoc"),
        ("p07", 57.8, 56.8, "Osos Cueracero", "41-42", "o_garra_oso", "sueltan casi lo mismo, a menos nivel", "R", WN, "ALTA (13 de 109)", "oso_cueracero"),
        ("p07", 75.2, 43.8, "Campamento Mojache", "vende la Horda", "o_oro", "La Horda vende en el Campamento Mojache", "V", WL, "ALTA (side 2)", "campamento_mojache"),
        ("p07", 31.1, 44.6, "Bastión Plumaluna", "vende la Alianza", "o_oro", "y la Alianza en el Bastión Plumaluna", "V", WL, "ALTA (side 1)", "bastion_plumaluna"),
    ],
    "alterac": [
        ("p02", 51.2, 42.0, "Dominios de los Aplastacresta", "fortaleza", "o_pano_seda", "Junto a los Dominios de los Aplastacresta, la fortaleza de los ogros", "C", WL, "ALTA", "dominios_aplastacresta"),
        ("p02", 47.9, 34.2, "Cuenca de la Matanza", "cueva norte · 27 vetas", "o_mena_mitril", "dos cuevas, una al norte y otra al sur", "R", WL, "ALTA (rótulo es-MX; 27 vetas en 48.0, 33.2)", "ogro_aplastacresta"),
        ("p02", 52.8, 47.1, "38 vetas", "oro · hierro · plata · mitril · veraplata", "o_mena_oro", "En un solo rincón del mapa hay treinta y ocho vetas", "R", WM, "ALTA (11 oro · 8 hierro · 7 plata · 6 mitril · 6 veraplata); SIN rótulo de cueva", None),
        ("p02", 47.4, 61.6, "Ogros Aplastacresta", "34-35 · sur", "o_pano_seda", "Los ogros sueltan plata, paño de seda, grises y verdes", "R", WN, "ALTA (17 de 111)", "ogro_aplastacresta"),
        ("p02", 47.3, 35.3, "Rizz Tornillosuelto", "vendedor en una jaula", "rizz", "cerca de la cueva del norte hay un vendedor gnomo", "P", WN, "ALTA (side 0)", None),
        ("p02", 52.7, 47.3, "Lo'Grosh", "raro 39 · El pacificador", "lo_grosh", "en la misma zona de las vetas ronda un raro, Lo'Grosh", "P", WN, "ALTA (19 de 30; las otras 6 en 47.8, 33.4) — MISMO sitio que «38 vetas»", "o_pacificador"),
        ("p02", 46.3, 47.1, "Aplastadores y magos", "élite · no te acerques", "aplastador_aplastacresta", "cerca de la fortaleza están los aplastadores y los magos", "X", WN, "ALTA (aplastador 13 de 42 aquí y 18 en 42.1, 47.2, junto a las Ruinas de Alterac; magos 41.0, 43.0 y 45.7, 46.7)", "mago_aplastacresta"),
    ],
    "devastadas": [
        ("p01", 56.2, 36.5, "Destripadores negros", "46-48 · 32 apariciones", "o_molleja_buitre", "entre el Alto de los Rapiñadores y la Serpiente Enroscada", "R", WN, "ALTA (8 de 32)", "destripador_negro"),
        ("p01", 62.4, 26.8, "Destripadores negros", "", "o_molleja_buitre", "hay competencia, y gana quien está encima", "R", WN, "ALTA (5)", "destripador_negro"),
        ("p01", 55.0, 44.0, "Destripadores negros", "", "o_molleja_buitre", "Solo hay unos treinta y dos puntos de aparición", "R", WN, "ALTA (5: 54.4-55.8, 43.4-44.6)", "destripador_negro"),
        ("p01", 46.5, 19.1, "Destripadores negros", "", "o_molleja_buitre", "Solo hay unos treinta y dos puntos de aparición", "R", WN, "ALTA (4; +4 en 50.3, 17.1)", "destripador_negro"),
        ("p01", 48.0, 29.1, "Alto de los Rapiñadores", "", "o_molleja_buitre", "entre el Alto de los Rapiñadores", "C", WL, "ALTA", "alto_rapinadores"),
        ("p01", 63.9, 33.6, "Serpiente Enroscada", "", "o_molleja_buitre", "y la Serpiente Enroscada", "C", WL, "ALTA (sin foto: la de la wiki es de Cataclysm)", None),
        ("p01", 50.6, 14.4, "Lynnore y Drazial", "El vigor del buitre · El golpe decisivo", "lynnore", "la piden dos misiones de la misma zona", "P", WN, "ALTA (Drazial en 50.5, 14.2)", "drazial"),
        ("p01", 47.8, 18.1, "Aguijoneros Scorpok", "50-51 · desuello", "o_pinza_scorpok", "puedes desollar a los aguijoneros Scorpok", "R", WN, "ALTA (24 de 78)", "aguijonero_scorpok"),
        ("p01", 47.5, 22.2, "Hienas risitas famélicas", "45-46 · desuello", "o_papada_hiena", "y a las hienas risitas famélicas de la zona", "R", WN, "ALTA (23 de 78; comparten sitio con los scorpok)", "hiena_risitas"),
        ("p01", 65.9, 18.7, "Castillo de Nethergarde", "vuelo y venta de la Alianza", "ico:ability_mount_gryphon_01", "La Alianza llega volando al Castillo de Nethergarde", "V", WL, "ALTA (3 vendedores + vuelo, side 1)", "castillo_nethergarde"),
    ],
    # ---------------- mapa mundo (resumen y viajes)
    "mundo:intro15": [
        m("desolace", 70.8, 76.8, "intro cierre", "15", "Centauros · Desolace", "o_pano_seda", "Hoy van quince farmeos de oro del treinta al cincuenta", "C", WL, "ALTA", "retador_magram"),
        m("marjal", 33.3, 22.8, "intro cierre", "14", "Arañas · Marjal", "o_seda_arana_espesa", "", "C", WL, "ALTA", "arana_niebla_negra"),
        m("tuercespina", 37.7, 17.1, "intro cierre", "13", "Gorilas · Tuercespina", "o_colmillo_gorila", "", "R", WN, "ALTA", "gorila_velo_bruma"),
        m("mil_agujas", 73.2, 57.3, "intro cierre", "12", "Tortugas · Mil Agujas", "o_fragmento_caparazon", "", "R", WN, "ALTA", "tortuga_brillavalva"),
        m("riverglades", 71.6, 67.5, "intro cierre", "11", "Cangrejos · Claros del Río", "o_carne_cangrejo", "", "R", WN, "ALTA", "reptador_arena"),
        m("inhospitas", 82.5, 32.2, "intro cierre", "10", "Crías · Tierras Inhóspitas", "o_glandula_llamas", "", "R", WN, "ALTA", "cria_lethlor"),
        m("pantano", 82.4, 92.1, "intro cierre", "9", "Múrlocs · Pantano", "o_perla_oro", "", "R", WN, "ALTA", "murloc_marisma"),
        m("tanaris", 44.4, 38.7, "intro cierre", "8", "Hienas · Tanaris", "o_melena_espesa", "", "R", WN, "ALTA", "hiena_llagapata"),
        m("feralas", 42.1, 21.9, "intro cierre", "7", "Gorilas y osos · Feralas", "o_hueso_oso", "", "R", WN, "ALTA", "tronador_groddoc"),
        m("pantano", 42.2, 42.4, "intro cierre", "6", "Jaguares · Pantano", "o_cola_blanda", "", "R", WN, "ALTA", "jaguar_pantano"),
        m("inhospitas", 17.6, 41.9, "intro cierre", "5", "Elementales · Tierras Inhóspitas", "o_tierra_elemental", "", "R", WN, "ALTA", "elemental_roca_inferior"),
        m("riverglades", 54.5, 86.9, "intro cierre", "4", "Coyotes · Claros del Río", "o_cola_tupida", "", "R", WN, "ALTA", "coyote_llanuras"),
        m("tuercespina", 27.4, 83.4, "intro cierre", "3", "Valijas · costa de Tuercespina", "o_valija_mitril", "", "R", WM, "ALTA", None),
        m("alterac", 52.8, 47.1, "intro cierre", "2", "Ogros y vetas · Alterac", "o_mena_oro", "", "R", WM, "ALTA", "ogro_aplastacresta"),
        m("devastadas", 56.2, 36.5, "intro cierre", "1", "Buitres · Tierras Devastadas", "o_molleja_buitre", "", "R", WN, "ALTA", "destripador_negro"),
    ],
    "mundo:r30": [
        m("mil_agujas", 73.2, 57.3, "resumen", "Tortugas · Desierto de Sal", "30-36", "o_fragmento_caparazon", "las tortugas del Desierto de Sal", "R", WN, "ALTA", "tortuga_brillavalva"),
        m("tuercespina", 37.7, 17.1, "resumen", "Gorilas · Tuercespina", "32-35", "o_colmillo_gorila", "los gorilas de Tuercespina", "R", WN, "ALTA", "gorila_velo_bruma"),
        m("desolace", 70.8, 76.8, "resumen", "Centauros · Desolace", "33-38", "o_pano_seda", "y los centauros de Desolace", "C", WL, "ALTA", "retador_magram"),
    ],
    "mundo:r35": [
        m("marjal", 33.3, 22.8, "resumen", "Arañas · Marjal", "35-38", "o_seda_arana_espesa", "las arañas del marjal", "C", WL, "ALTA", "arana_niebla_negra"),
        m("alterac", 52.8, 47.1, "resumen", "Cuevas · Alterac", "34-38", "o_mena_oro", "las cuevas de Alterac", "R", WM, "ALTA", "ogro_aplastacresta"),
        m("pantano", 42.2, 42.4, "resumen", "Jaguares · Pantano", "36-39", "o_cola_blanda", "los jaguares del pantano", "R", WN, "ALTA", "jaguar_pantano"),
        m("riverglades", 54.5, 86.9, "resumen", "Coyotes · Claros del Río", "36-40", "o_cola_tupida", "los coyotes de Claros del Río", "R", WN, "ALTA", "coyote_llanuras"),
        m("inhospitas", 17.6, 41.9, "resumen", "Elementales inferiores", "37-39", "o_piedra_inerte", "y los primeros elementales de roca", "R", WN, "ALTA", "elemental_roca_inferior"),
    ],
    "mundo:r40": [
        m("inhospitas", 82.5, 32.2, "resumen", "Crías · Barranco Lethlor", "40-44", "o_glandula_llamas", "las crías del Barranco Lethlor", "R", WN, "ALTA", "cria_lethlor"),
        m("inhospitas", 2.8, 82.0, "resumen", "Elementales superiores", "42-44", "o_tierra_elemental", "los elementales superiores", "R", WN, "ALTA", "elemental_roca_superior"),
        m("tuercespina", 33.6, 76.3, "resumen", "Cangrejos · sur de Tuercespina", "40-41", "o_almeja_boca_grande", "los cangrejos del sur de Tuercespina", "R", WN, "ALTA", "reptador_arenas_sur"),
        m("pantano", 82.4, 92.1, "resumen", "Múrlocs · Pantano", "41-45", "o_perla_oro", "y los múrlocs del Pantano de las Penas", "R", WN, "ALTA", "murloc_marisma"),
    ],
    "mundo:r45": [
        m("tanaris", 44.4, 38.7, "resumen", "Hienas · Tanaris", "44-46", "o_melena_espesa", "las hienas de Tanaris", "R", WN, "ALTA", "hiena_llagapata"),
        m("feralas", 42.1, 21.9, "resumen", "Gorilas y osos · Feralas", "47-50", "o_hueso_oso", "los gorilas y osos de Feralas", "R", WN, "ALTA", "tronador_groddoc"),
        m("devastadas", 56.2, 36.5, "resumen", "Buitres · Tierras Devastadas", "46-50", "o_molleja_buitre", "y los buitres de Las Tierras Devastadas", "R", WN, "ALTA", "destripador_negro"),
        m("tuercespina", 27.4, 83.4, "resumen", "Pesca de valijas", "cualquier nivel", "o_valija_mitril", "La pesca de valijas, en cualquier momento", "R", WM, "ALTA", None),
    ],
    "mundo:p04": [
        m("riverglades", 54.5, 86.9, "p04", "Coyotes · Claros del Río", "36-40", "o_cola_tupida", "Y desde ahí pasas directo a Tierras Inhóspitas", "R", WN, "ALTA", "coyote_llanuras"),
        m("inhospitas", 17.6, 41.9, "p04", "Elementales · Tierras Inhóspitas", "37-39", "o_piedra_inerte", "a los elementales del número cinco", "R", WN, "ALTA", "elemental_roca_inferior"),
    ],
    "mundo:p01": [
        m("pantano", 46.0, 54.6, "p01", "Rocal (vuelo de la Horda)", "Pantano de las Penas", "ico:ability_mount_wyvern_01", "Y la Horda, desde el vuelo del Pantano de las Penas", "V", WP, "ALTA (maestro de vuelo Breyk)", "rocal"),
        m("devastadas", 65.9, 18.7, "p01", "Castillo de Nethergarde", "vuelo de la Alianza", "ico:ability_mount_gryphon_01", "La Alianza llega volando al Castillo de Nethergarde", "V", WL, "ALTA", "castillo_nethergarde"),
        m("devastadas", 56.2, 36.5, "p01", "Destripadores negros", "46-48", "o_molleja_buitre", "Los destripadores negros de Las Tierras Devastadas", "R", WN, "ALTA", "destripador_negro"),
    ],
}
# las tuplas «mundo» salen como (x, y, escena, rótulo, …): se reordenan a (escena, x, y, rótulo, …)
for k, v in PTS.items():
    if k.startswith("mundo"):
        PTS[k] = [(t[2], t[0], t[1]) + t[3:] for t in v]
COLOR = {"C": (255, 60, 60), "R": (255, 230, 0), "P": (255, 140, 255), "V": (80, 255, 120), "X": (255, 140, 0)}


def fuente(n):
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


_ICO = {}


def icono(f):
    """imagen del 5.º campo: o_* → pegatinas/, ico:<n> → zamimg, criatura/PNJ → caras/ (o pegatinas/)."""
    if f in _ICO:
        return _ICO[f]
    im = None
    if f.startswith("ico:"):
        try:
            im = Image.open(__import__("io").BytesIO(urllib.request.urlopen(urllib.request.Request(
                f"https://wow.zamimg.com/images/wow/icons/large/{f[4:]}.jpg", headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()))
        except Exception:
            im = None
    else:
        for c in ("caras", "pegatinas"):
            p = os.path.join(D, c, f + ".png")
            if os.path.isfile(p):
                im = Image.open(p)
                break
    _ICO[f] = im.convert("RGBA") if im else None
    return _ICO[f]


def revisar():
    malos = []
    for k, pts in PTS.items():
        for t in pts:
            for f in (t[5], t[10]):
                if f and icono(f) is None:
                    malos.append((k, t[3], f))
    for x in malos:
        print("FALTA imagen:", x)
    return not malos


def hojas():
    F = fuente(15)
    minis = []
    for k, pts in PTS.items():
        m_ = k.split(":")[0]
        im = Image.open(os.path.join(D, "mapas", m_ + ".jpg")).convert("RGB")
        im = im.resize((1024, round(1024 * im.height / im.width)))
        W, H = im.size
        d = ImageDraw.Draw(im)
        for e, x, y, r, sub, ico, frase, t, *_ in pts:
            px, py = x / 100 * W, y / 100 * H
            i = icono(ico)
            if i is not None:
                i = i.copy()
                i.thumbnail((30, 30))
                im.paste(i.convert("RGB"), (int(px - 36), int(py - 15)), i if i.mode == "RGBA" else None)
            d.ellipse((px - 6, py - 6, px + 6, py + 6), outline=COLOR[t], width=3)
            d.text((px + 8, py - 8), f"{r} [{x:.1f},{y:.1f}]", fill=COLOR[t], font=F, stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((8, H - 24), k, fill=(0, 255, 255), font=fuente(20), stroke_width=2, stroke_fill=(0, 0, 0))
        minis.append(im.resize((960, round(960 * H / W))))
    por = 4
    for k in range(0, len(minis), por):
        lote = minis[k:k + por]
        alto = max(mi.height for mi in lote)
        g = Image.new("RGB", (2 * 960, ((len(lote) + 1) // 2) * alto), (20, 20, 20))
        for i, mi in enumerate(lote):
            g.paste(mi, ((i % 2) * 960, (i // 2) * alto))
        g.save(os.path.join(D, "previews", f"_coords_check_{k // por + 1}.jpg"), quality=85)
    print(len(minis), "mapas;", (len(minis) + por - 1) // por, "hojas;", sum(len(v) for v in PTS.values()), "puntos")


def md():
    print("| Mapa | Escena | x, y (% del mapa) | Rótulo | Subrótulo | Ícono (5.º campo) | Alt. | Frase del guion | Tipo | Fuente | Confianza |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, pts in PTS.items():
        for e, x, y, r, sub, ico, frase, t, f, c, alt in pts:
            print(f"| `{k}` | {e} | {x:.1f}, {y:.1f} | {r} | {sub} | `{ico}` | {('`' + alt + '`') if alt else '—'} | "
                  f"{('«' + frase + '»') if frase and not frase.startswith('(') else frase or '—'} | {t} | {f} | {c} |")


if __name__ == "__main__":
    if sys.argv[1:] == ["md"]:
        md()
    else:
        revisar()
        hojas()
