# -*- coding: utf-8 -*-
"""Coordenadas de «La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (25-nov-2026; adaptado de wow_errores_60/_coords_check.py).
Fuentes: INV = videos/_investigacion_wow_ruta_profesiones.md (coordenadas de Wowhead Forever: pines del mapa mundial [WHF-MAP] y /way de los
entrenadores [WP-TR], comprobadas entre sí); WHF = pin del mapa mundial de Wowhead Forever (nether.wowhead.com/forever/data/world-map, leído
el 25-nov: mazmorras); WHF-lugar = rótulo de subzona/pueblo del mismo archivo (campo places), pasado a % de la zona con el rect de la zona.
Mapas de zona (zamimg, wiki Hyjal) y recortes con el rect EXACTO de la zona/capital (ventormenta, orgrimmar, forjaz, peste_este):
1 % de la imagen = 1 de coordenada. Mapa «mundo» (teselas): coordenada de zona → lienzo (rect de la zona) → % del recorte (mapas/_rects.json).
Los x, y de PTS son los que van a P(x, y, rótulo, sub, foto) de mapa(...) en efectos.py.
    python _coords_check.py      → previews/_coords_check_N.jpg (4 mapas por hoja, MIRARLAS)
    python _coords_check.py md   → imprime la tabla de _coords.md
Tipos: C = centro (pueblo/campamento) · R = punto de ruta/recolección · M = entrada de mazmorra · P = PNJ (entrenador, vendedor)."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
I, W_, WL = "INV", "WHF", "WHF-lugar"
# rect de cada zona en el lienzo del mapa mundial de Wowhead Forever (campo places, kind=zone/capital; leído el 25-nov)
ZR = {
    "durotar": [[18268, 14648], [23344, 18032]], "elwynn": [[35902, 21958], [39234, 24180]],
    "humedales": [[37750, 16398], [41720, 19044]], "argenteos": [[34064, 12736], [38096, 15424]],
    "laderas": [[36352, 13952], [39424, 16000]], "alterac": [[36624, 12896], [39312, 14688]],
    "arathi": [[38208, 14464], [41664, 16768]], "mil_agujas": [[16800, 20192], [21024, 23008]],
    "riverglades": [[39192, 20544], [43848, 23648]], "interior": [[38888, 12928], [42584, 15392]],
    "tanaris": [[16594, 22024], [23218, 26440]], "ungoro": [[15872, 22112], [19424, 24480]],
    "frondavil": [[14808, 9536], [20328, 13216]], "hyjal": [[17270, 10332], [20604, 12554]],
    "tuercespina": [[35244, 25058], [41370, 29142]], "baldios": [[13866, 14836], [23594, 21322]],
    "crestagrana": [[38990, 22568], [41074, 23958]], "feralas": [[11160, 18656], [17832, 23104]],
    "pantano": [[39510, 23572], [41712, 25040]], "sierra_espolon": [[13268, 13584], [17956, 16710]],
    "inhospitas": [[39372, 19990], [41760, 21582]], "desolace": [[12320, 15950], [16636, 18828]],
    "vallefresno": [[14752, 11898], [20288, 15588]], "marjal": [[17320, 18336], [22360, 21696]],
    "loch_modan": [[39290, 18644], [41938, 20410]],
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


# clave: [(escena, x, y, rótulo, subrótulo, foto, frase del guion, tipo, fuente, confianza)]
#   clave = nombre del mapa; «mundo:pNN» = el mapa mundo con los puntos de esa parada (la clave antes de «:» es el archivo)
PTS = {
    # ---------------- zonas iniciales
    "durotar": [
        ("reglas p01", 40.5, 68.1, "Norzsh", "entrenador júnior de minería", "norzsh", "un entrenador júnior en cada uno", "P", I, "ALTA"),
        ("p01", 43.8, 64.7, "Vetas de cobre pobres", "Valle de los Retos", "o_mena_cobre", "vetas de cobre pobres en los valles de inicio", "R", I, "ALTA (densidad n=25)"),
        ("p01", 53.1, 25.5, "Cobre", "1-65", "o_mena_cobre", "Del uno al sesenta y cinco, cobre, en cualquier zona inicial", "R", I, "ALTA (n=17)"),
        ("p04", 44.3, 65.2, "Flor de paz marchita", "1-70", "o_flor_paz", "versiones marchitas y atrofiadas", "R", I, "ALTA (n=27)"),
        ("p06", 42.9, 23.2, "Jabalíes moteados", "desuello 1-75", "o_prof_desuello", "jabalíes en Durotar", "R", I, "ALTA"),
    ],
    "elwynn": [
        ("reglas p01", 47.2, 32.2, "Kelsey Fargo", "entrenadora júnior de minería", "kelsey_fargo", "un entrenador júnior en cada uno", "P", I, "ALTA"),
        ("p01", 42.0, 76.8, "Cobre", "1-65", "o_mena_cobre", "Del uno al sesenta y cinco, cobre", "R", I, "ALTA (n=13)"),
        ("p04", 54.2, 44.5, "Hojaplata atrofiada", "1-70", "o_hojaplata", "versiones marchitas y atrofiadas", "R", I, "ALTA (n=19)"),
        ("p06", 44.1, 71.1, "Jabalíes y lobos", "desuello 1-75", "o_prof_desuello", "o lobos en el Bosque de Elwynn", "R", I, "ALTA"),
        ("p09", 64.8, 70.6, "Kitta Vientofuego", "encantamiento experto (A)", "kitta", "Kitta Vientofuego, en lo alto de la Torre de Azora", "P", I, "ALTA"),
        ("p09", 65.8, 68.1, "Torre de Azora", "", "torre_azora", "en lo alto de la Torre de Azora", "C", WL, "ALTA"),
        ("p11", 52.4, 62.4, "Lago de Cristal", "pesca 1-75", "o_cana_pescar", "Todos los entrenadores de inicio están junto al agua", "R", I, "ALTA"),
    ],
    "mulgore": [
        ("p01", 56.7, 53.4, "Cueva de cobre", "5 vetas, reaparición rápida", "o_mena_cobre", "En Mulgore hay una cueva con cinco vetas de cobre", "R", I, "MEDIA (casilla más densa n=33; la cueva exacta no tiene pin)"),
        ("p01", 34.6, 53.2, "Excavación de Bael'dun", "forja", "", "La forja más cerca está en la Excavación de Bael'dun", "C", WL, "ALTA"),
    ],
    "teldrassil": [
        ("p01", 56.9, 27.6, "Fragmentos de ámbar", "", "o_mena_cobre", "ahora pican fragmentos de ámbar", "R", I, "ALTA (n=17)"),
        ("p01", 53.0, 51.1, "Fragmentos de ámbar grandes", "", "o_mena_cobre", "ahora pican fragmentos de ámbar", "R", I, "ALTA"),
        ("p01", 58.2, 41.5, "Fanorran Stilloak", "entrenador júnior de minería", "", "un entrenador júnior en cada uno", "P", I, "ALTA"),
    ],
    # ---------------- tramos medios
    "humedales": [
        ("p01", 47.3, 62.2, "Cueva de estaño", "Alianza · 65-125", "o_mena_estano", "La Alianza, en una cueva de Los Humedales llena de estaño", "R", I, "ALTA (14 vetas de incendicita en la casilla)"),
        ("p04", 38.5, 60.5, "Sitio de Excavación", "plano del invernadero (Shadetooth)", "excavacion_humedales", "el plano del invernadero lo suelta Shadetooth, en Los Humedales", "M", W_, "ALTA (pin de mazmorra)"),
        ("p06", 34.5, 49.7, "Excavación de Whelgar", "desuello 130-150 (A)", "o_prof_desuello", "La Alianza, a Loch Modan y luego a Los Humedales", "R", WL, "ALTA"),
    ],
    "argenteos": [
        ("p01", 58.1, 72.8, "Cueva de estaño", "Horda · 65-125", "o_mena_estano", "la Horda, en el Bosque de Argénteos", "R", I, "ALTA (n=13)"),
        ("p04", 54.5, 76.6, "Brezospina", "70-115", "o_brezospina", "marregal y brezospina en el Bosque de Argénteos", "R", I, "ALTA (n=12)"),
        ("p04", 54.6, 27.0, "Marregal", "70-115", "o_marregal", "marregal y brezospina en el Bosque de Argénteos", "R", I, "ALTA"),
    ],
    "laderas": [
        ("p01", 28.3, 55.7, "Estaño", "Horda · 65-125", "o_mena_estano", "o en Laderas de Trabalomas", "R", I, "ALTA"),
        ("p04", 36.5, 56.1, "Sangrerregia", "115-170", "o_sangrerregia", "Laderas de Trabalomas o Sierra Espolón", "R", I, "ALTA"),
        ("p06", 57.8, 27.4, "Osos y leones", "desuello 150-160", "o_prof_desuello", "la cueva de yetis de Laderas de Trabalomas", "R", I, "ALTA"),
        ("p08", 63.7, 20.8, "Daryl Stack", "sastrería artesano (H)", "daryl_stack", "Daryl Stack, en el Molino Tarren de Laderas", "P", I, "ALTA"),
        ("p08", 61.5, 20.0, "Molino Tarren", "", "molino_tarren", "en el Molino Tarren de Laderas", "C", WL, "ALTA"),
    ],
    "alterac": [
        ("p06", 36.5, 85.9, "Cueva de yetis", "desuello 150-225", "o_prof_desuello", "la cueva de yetis de Laderas de Trabalomas", "R", I, "ALTA (Wowhead la pone en Alterac, en el borde con Laderas)"),
        ("p02", 19.7, 63.4, "Alard Schmied", "herrería 1-225 (A)", "", "Alard Schmied, en Dalaran, enseña hasta el doscientos veinticinco", "P", I, "ALTA"),
        ("p08", 17.7, 60.4, "Charles Worth", "sastrería 1-225 (A)", "", "la Alianza tiene además a Charles Worth en Dalaran", "P", I, "ALTA"),
        ("p09", 16.8, 62.3, "Vanessa Sellers", "encantamiento 1-225 (A)", "", "La Alianza tiene además a Vanessa Sellers, en Dalaran", "P", I, "ALTA"),
        ("p08 p09", 16.7, 68.8, "Ciudad de Dalaran", "rueca · recuperador arcano", "ciudad_dalaran", "un centinela inestable, en la Ciudad de Dalaran", "M", W_, "ALTA (pin de mazmorra)"),
    ],
    "arathi": [
        ("p01", 54.4, 76.0, "Hierro", "125-175", "o_mena_hierro", "hierro y oro, en las Tierras Altas de Arathi", "R", I, "ALTA"),
        ("p01", 33.2, 44.7, "Hierro", "125-175", "o_mena_hierro", "hierro y oro, en las Tierras Altas de Arathi", "R", I, "ALTA"),
        ("p01", 84.5, 32.8, "Oro", "155-175", "o_mena_oro", "hierro y oro, en las Tierras Altas de Arathi", "R", I, "ALTA"),
        ("p04", 56.6, 35.1, "Mostacho de Khadgar", "170-205", "o_mostacho_khadgar", "la Vega de Tuercespina o Arathi", "R", I, "ALTA"),
        ("p12", 27.0, 58.8, "Deneb Camino", "libro de experto (A)", "deneb", "lo vende Deneb Camino en Arathi para la Alianza", "P", I, "ALTA"),
        ("p12", 73.4, 36.8, "Doctor Gregory Victor", "Atenciones médicas (H)", "gregory_victor", "el doctor Gregory Victor en Sentencia, en Arathi", "P", I, "ALTA"),
        ("p12", 73.9, 35.8, "Sentencia", "", "", "en Sentencia, en Arathi", "C", WL, "ALTA"),
    ],
    "mil_agujas": [
        ("p01", 12.7, 34.8, "Hierro", "125-175", "o_mena_hierro", "o en Las Mil Agujas", "R", I, "ALTA"),
        ("p01", 43.3, 35.5, "Hierro", "125-175", "o_mena_hierro", "o en Las Mil Agujas", "R", I, "ALTA"),
    ],
    "riverglades": [
        ("p01", 55.5, 44.7, "Hierro: 133 vetas", "la zona con más hierro", "o_mena_hierro", "más vetas de hierro que ninguna otra zona del mapa", "R", I, "ALTA (casilla más densa)"),
        ("p01", 77.8, 52.0, "Grungle", "entrenador de minería", "", "(entrenador de la zona nueva; no lo nombra la voz)", "P", I, "ALTA"),
        ("p03", 77.6, 50.8, "Kor'gar", "esquema del tubo de torio", "", "o con Kor'gar, en Claros del Río", "P", I, "ALTA"),
        ("p06", 65.2, 53.1, "Cuero pesado", "bestias de las llanuras", "o_cuero_pesado", "tiene bestias que dan mucho cuero pesado", "R", I, "ALTA"),
        ("p06", 58.4, 55.6, "Cuero pesado", "", "o_cuero_pesado", "tiene bestias que dan mucho cuero pesado", "R", I, "ALTA"),
    ],
    "interior": [
        ("p01", 56.7, 43.9, "Mitril y veraplata", "175-245", "o_mena_mitril", "mitril y veraplata, en Tierras del Interior", "R", I, "ALTA (n=11 de cada)"),
        ("p04", 57.6, 42.6, "Champiñón fantasma", "cueva · 230-270", "o_champinon_fantasma", "Tierras del Interior con solea y champiñón fantasma", "R", I, "ALTA (n=9)"),
        ("p04", 65.4, 47.4, "Solea", "230-270", "o_solea", "Tierras del Interior con solea", "R", I, "ALTA"),
        ("p07", 13.4, 43.3, "Drakk Stonehand", "peletería artesano (A)", "drakk", "Drakk Stonehand, en Tierras del Interior", "P", I, "ALTA"),
    ],
    "tanaris": [
        ("p01", 33.5, 44.6, "Mitril y veraplata", "175-245", "o_mena_mitril", "o en Tanaris", "R", I, "ALTA"),
        ("p01", 55.1, 74.6, "Mitril y veraplata", "175-245", "o_mena_mitril", "o en Tanaris", "R", I, "ALTA"),
        ("p02 p03 p10", 51.2, 27.5, "Gadgetzan", "Derotain · Buzzek · Dirge", "gadgetzan", "Buzzek Giracorchete, en Gadgetzan", "C", WL, "ALTA (Derotain 51.4, 28.6 · Buzzek 52.2, 27.6 · Dirge 52.6, 28.0: el mismo pueblo)"),
        ("p04", 44.9, 34.7, "Flor de fuego", "205-230", "", "Tanaris o La Garganta de Fuego", "R", I, "ALTA"),
        ("p04", 46.9, 65.5, "Loto cárdeno", "205-230", "", "Tanaris o La Garganta de Fuego", "R", I, "ALTA"),
    ],
    # ---------------- final de la ruta
    "ungoro": [
        ("p01", 67.3, 15.9, "Torio pequeño", "245-275", "o_mena_torio", "torio pequeño en Un'Goro", "R", I, "ALTA (n=12)"),
        ("p06", 36.0, 35.2, "Diemetradones y pterrordáctilos", "desuello 280-300", "o_cuero_basto", "los diemetradones y pterrordáctilos de Un'Goro", "R", I, "ALTA"),
        ("p06", 35.5, 46.0, "Diemetradones", "", "o_cuero_basto", "los diemetradones y pterrordáctilos de Un'Goro", "R", I, "ALTA"),
        ("p06", 43.6, 7.2, "Refugio de los Mariscales", "", "", "(punto de partida de la guía)", "C", WL, "ALTA (referencia)"),
    ],
    "frondavil": [
        ("p01", 36.2, 54.6, "Torio pequeño", "245-275", "o_mena_torio", "o en Frondavil", "R", I, "ALTA"),
        ("p04", 53.6, 14.9, "Hojasueño", "270-300", "o_hojasueno", "Frondavil, con hojasueño", "R", I, "ALTA"),
        ("p04", 42.9, 43.6, "Flor de plaga", "270-300", "", "y flor de plaga, hasta el trescientos", "R", I, "ALTA"),
        ("p04", 44.8, 85.0, "Gromsanguina", "270-300", "", "(no la nombra la voz)", "R", I, "ALTA"),
        ("p05", 51.5, 82.0, "Maestro micólogo Shurome", "alquimia 1-300 (los dos bandos)", "shurome", "Shurome, en el Santuario Esmeralda de Frondavil", "P", I, "ALTA"),
        ("p05", 50.9, 81.3, "Santuario Esmeralda", "", "", "en el Santuario Esmeralda de Frondavil", "C", WL, "ALTA"),
    ],
    "cuna_invierno": [
        ("p01", 55.9, 85.8, "Torio rico", "275-300", "o_mena_torio", "torio rico en Cuna del Invierno", "R", I, "ALTA (n=9)"),
        ("p03", 61.2, 38.2, "Vista Eterna", "esquema del tubo de torio", "", "El esquema del tubo se compra en Cuna del Invierno", "C", WL, "MEDIA (Xizzer Fizzbolt sin coordenada: se marca el pueblo)"),
    ],
    "peste_este": [
        ("p01", 47.1, 54.6, "Torio rico", "275-300", "o_mena_torio", "en la Peste del Este", "R", I, "ALTA"),
        ("p03 p08", 26.1, 10.4, "Stratholme", "Ezra Grimm · Baronesa Anastari", "stratholme", "suelta Ezra Grimm en Stratholme", "M", W_, "ALTA (pin de mazmorra)"),
    ],
    "estepas": [
        ("p01", 65.4, 35.8, "Torio rico", "275-300", "o_mena_torio", "o en Las Estepas Ardientes", "R", I, "ALTA"),
        ("p01 p02", 27.9, 40.2, "Montaña Roca Negra", "Profundidades: Latifuego · Argelmach", "profundidades_roca_negra", "el Embajador Latifuego, en Profundidades de Roca Negra", "M", WL, "ALTA el rótulo de subzona (el pin de mazmorra 22.6, 7.5 es el portal interior y cae en la franja de La Garganta de Fuego)"),
    ],
    "hyjal": [
        ("p01", 63.6, 86.7, "Torio rico", "más de 100 vetas", "o_mena_torio", "Monte Hyjal tiene, además, más de cien vetas de torio rico", "R", I, "ALTA (casilla densa)"),
        ("p01", 76.3, 75.4, "Torio rico", "", "o_mena_torio", "más de cien vetas de torio rico", "R", I, "ALTA"),
        ("intro p01", 35.6, 83.3, "Torio pesado", "la mena nueva", "o_mena_torio_pesada", "la mena de torio pesada, en unas ciento veinte vetas", "R", I, "ALTA"),
        ("intro p01", 35.8, 47.6, "Torio pesado", "", "o_mena_torio_pesada", "la mena de torio pesada", "R", I, "ALTA"),
        ("intro p01", 64.5, 86.0, "Torio pesado", "", "o_mena_torio_pesada", "la mena de torio pesada", "R", I, "ALTA"),
        ("p03", 60.2, 61.4, "Kayleena Encantaflores", "ingeniería artesano", "kayleena", "Kayleena Encantaflores, en Monte Hyjal", "P", I, "ALTA"),
        ("p04", 44.3, 75.2, "Hojapesadilla", "hierba nueva", "o_hojapesadilla", "la hojapesadilla, la salvia demoníaca y el loto de la muerte", "R", I, "ALTA (n=11)"),
        ("p04", 45.2, 86.8, "Salvia demoníaca", "hierba nueva", "o_salvia_demoniaca", "la salvia demoníaca", "R", I, "ALTA (n=13)"),
        ("p04", 62.6, 33.8, "Salvia demoníaca", "", "o_salvia_demoniaca", "la salvia demoníaca", "R", I, "ALTA"),
        ("p06", 74.3, 36.6, "Cuero basto", "", "o_cuero_basto", "Y en Monte Hyjal, cuero basto", "R", I, "ALTA"),
        ("p08 p12", 48.2, 33.6, "Pexmit", "difícil de encontrar", "pexmit", "Lo vende Pexmit, en Monte Hyjal", "P", I, "ALTA (pin de PNJ raro)"),
        ("p12", 13.0, 52.8, "Ortak Lomgok", "Flora Antigua (H)", "ortak", "una misión de Ortak Lomgok, en Flora Antigua", "P", I, "ALTA"),
        ("p08", 13.6, 53.0, "Kal'tinzan", "misión de los puños (H)", "", "o la Horda lo saca con una misión", "P", I, "ALTA"),
    ],
    # ---------------- entrenadores y vendedores
    "tuercespina": [
        ("p02", 29.0, 75.4, "Brikk Finoficio", "herrería artesano", "brikk", "Brikk Finoficio, en Bahía del Botín, a los dos bandos", "P", I, "ALTA"),
        ("p11", 27.4, 77.0, "Viejo Heming", "libro de pesca de experto", "viejo_heming", "un libro que vende el Viejo Heming, en Bahía del Botín", "P", I, "ALTA"),
        ("p04", 35.1, 15.2, "Mostacho de Khadgar", "170-205", "o_mostacho_khadgar", "la Vega de Tuercespina", "R", I, "ALTA (n=14)"),
        ("p04", 45.7, 35.9, "Espina de oro", "170-205", "", "pálida, espina de oro y mostacho de Khadgar", "R", I, "ALTA"),
    ],
    "baldios": [
        ("p02", 49.8, 29.4, "Campamento de Favor (H)", "Logística y suministros de Durotar", "o_cajon_arrebatado", "La Horda lo tiene al oeste de El Cruce, en Los Baldíos", "C", I, "ALTA (vendedores 49.4-49.8, 28.8-30.0)"),
        ("p02", 52.1, 30.6, "El Cruce", "", "", "al oeste de El Cruce", "C", WL, "ALTA (referencia)"),
        ("p06", 61.2, 54.7, "Fuerte del Norte", "raptores: desuello 75-150 (H)", "o_prof_desuello", "a los raptores y zancudos al oeste de Fuerte del Norte", "R", I, "ALTA"),
        ("p06", 60.2, 33.8, "Zhevras y zancudos", "", "o_prof_desuello", "a los raptores y zancudos", "R", I, "ALTA"),
    ],
    "crestagrana": [
        ("p02", 10.8, 72.4, "Campamento de Favor (A)", "Autoridad Comercial de Azeroth", "o_cajon_arrebatado", "la Alianza en Tres Caminos, al oeste de Crestagrana", "C", I, "ALTA (Nina Fuegocertero; vendedores 8.4-11.2, 71.0-74.6)"),
        ("p10", 67.1, 69.9, "Whimsyfin", "pez nuevo (27 bancos)", "o_whimsyfin", "el Whimsyfin, que solo se pesca en Crestagrana", "R", I, "ALTA (mediana de 27 bancos)"),
    ],
    "orgrimmar": [
        ("p02", 82.3, 23.0, "Saru Steelfury", "herrería experto", "saru_steelfury", "Saru Steelfury en Orgrimmar", "P", I, "ALTA"),
        ("p03", 76.0, 25.1, "Roxxik", "ingeniería experto", "roxxik", "con Roxxik en Orgrimmar", "P", I, "ALTA"),
    ],
    "forjaz": [
        ("p02", 52.4, 41.2, "Bengus Deepforge", "herrería experto", "bengus_deepforge", "o Bengus Deepforge en Forjaz", "P", I, "ALTA"),
        ("p03", 68.5, 43.5, "Springspindle", "ingeniería experto", "springspindle", "o con Springspindle en Forjaz", "P", I, "ALTA"),
    ],
    "ventormenta": [
        ("p08", 53.3, 81.5, "Georgio Bolero", "sastrería experto", "georgio_bolero", "Georgio Bolero en Ventormenta", "P", I, "ALTA (mapa de ciudad de Forever; WP-TR y WHF coinciden)"),
    ],
    "feralas": [
        ("p05", 32.6, 43.8, "Kylanna", "alquimia artesano (A)", "kylanna", "y Kylanna, en Feralas, para la Alianza", "P", I, "ALTA"),
        ("p05", 31.1, 44.6, "Bastión Plumaluna", "", "", "", "C", WL, "ALTA (referencia)"),
        ("p06", 54.6, 56.5, "Vega Cicatriz Feral", "yetis: desuello 225-280", "o_cuero_grueso", "los yetis de la Vega Cicatriz Feral, en Feralas", "R", WL, "ALTA"),
        ("p07", 74.4, 43.1, "Hahrana Pielférrea", "peletería artesano (H)", "hahrana", "Hahrana Pielférrea, en Feralas, para la Horda", "P", I, "ALTA"),
        ("p07", 75.2, 43.8, "Campamento Mojache", "", "", "", "C", WL, "ALTA (referencia)"),
        ("p11", 63.2, 52.2, "Río Verdantis", "Ahi de Feralas", "", "y el Río Verdantis, en Feralas", "R", I, "ALTA"),
    ],
    "pantano": [
        ("p05", 48.5, 55.8, "Rogvar", "alquimia artesano (H)", "rogvar", "Rogvar, en el Pantano de las Penas, para la Horda", "P", I, "ALTA"),
        ("p11", 70.0, 52.9, "Templo de Atal'Hakkar", "cabaña de pesca (Jammal'an)", "templo_sumergido", "el profeta Jammal'an, en el Templo Sumergido", "M", WL, "ALTA el rótulo (el pin de mazmorra 77.3, 35.9 cae en la orilla)"),
    ],
    "sierra_espolon": [
        ("p09", 49.2, 57.2, "Hgarth", "encantamiento experto (H)", "hgarth", "Hgarth, en un risco sobre el Refugio Roca del Sol", "P", I, "ALTA"),
        ("p09", 47.8, 60.8, "Refugio Roca del Sol", "", "refugio_roca_sol", "sobre el Refugio Roca del Sol", "C", WL, "ALTA"),
        ("p04", 35.0, 64.2, "Hierba cardenal", "115-170", "", "Laderas de Trabalomas o Sierra Espolón", "R", I, "ALTA"),
    ],
    "inhospitas": [
        ("p09", 44.2, 12.2, "Uldaman", "Annora: encantamiento artesano", "annora", "solo lo enseña Annora, en Uldaman", "M", WL, "ALTA (rótulo de Uldaman; Annora en la entrada trasera)"),
    ],
    "desolace": [
        ("p10", 26.2, 69.8, "Wulan", "libro de cocina de experto (H)", "wulan", "Wulan en Aldea Cazasombras, en Desolace", "P", I, "ALTA"),
        ("p10 p11", 25.3, 70.4, "Aldea Cazasombras", "", "", "en Aldea Cazasombras", "C", WL, "ALTA"),
    ],
    "vallefresno": [
        ("p10", 49.4, 67.0, "Shandrina", "libro de cocina de experto (A)", "shandrina", "Shandrina en el Lago Mystral, en Vallefresno", "P", I, "ALTA"),
        ("p10", 51.7, 73.4, "Lago Mystral", "", "", "en el Lago Mystral", "C", WL, "ALTA"),
        ("p11", 16.5, 11.0, "Cavernas de Brazanegra", "expositor de pesca (Gelihast)", "brazanegra", "Gelihast, en las Cavernas de Brazanegra", "M", W_, "ALTA (pin de mazmorra)"),
    ],
    "marjal": [
        ("p11", 58.4, 60.0, "Nat Pagle", "pesca artesano", "nat_pagle", "la misión de Nat Pagle, en el Marjal", "P", I, "ALTA"),
        ("p08", 66.2, 51.8, "Timothy Worthington", "sastrería artesano (A)", "timothy_worthington", "Timothy Worthington, en Theramore", "P", I, "ALTA"),
        ("p12", 67.6, 48.8, "Doctor Gustaf VanHowzen", "Atenciones médicas (A)", "vanhowzen", "el doctor Gustaf VanHowzen, en Theramore", "P", I, "ALTA"),
        ("p08 p12", 65.0, 47.1, "Theramore", "", "", "en Theramore", "C", WL, "ALTA"),
        ("p12", 36.4, 30.4, "Balai Lok'Wein", "libro de experto (H)", "balai", "Balai Lok'Wein en el Marjal para la Horda", "P", I, "ALTA"),
    ],
    "azshara": [
        ("p11", 58.3, 56.3, "Almeja bocazas", "226 bancos", "o_almeja_bocazas", "más de trescientos cincuenta bancos de almejas bocazas y de langostas", "R", I, "ALTA (mediana)"),
        ("p11", 61.4, 57.4, "Langosta garraoscura", "132 bancos", "o_langosta_garraoscura", "y de langostas", "R", I, "ALTA (mediana)"),
    ],
    "shendralas": [
        ("p07", 42.6, 78.1, "Jarael", "peletería 1-225", "", "o Jarael en Shen'dralas", "P", I, "ALTA"),
        ("p08", 43.4, 77.8, "Melanori", "sastrería 1-225", "", "y en Shen'dralas está Melanori", "P", I, "ALTA"),
    ],
    "loch_modan": [
        ("p06", 63.2, 40.8, "Cocodrilos, osos y jabalíes", "desuello 75-130 (A)", "o_prof_desuello", "La Alianza, a Loch Modan", "R", I, "ALTA"),
        ("p04", 65.5, 42.9, "Brezospina", "70-115", "o_brezospina", "o en Loch Modan", "R", I, "ALTA"),
    ],
    "bosque_ocaso": [
        ("p06", 62.8, 68.2, "Huargos Nightbane", "desuello 150-225", "o_prof_desuello", "O los huargos del Bosque del Ocaso", "R", I, "ALTA"),
        ("p06", 64.6, 35.6, "Huargos Nightbane", "", "o_prof_desuello", "O los huargos del Bosque del Ocaso", "R", I, "ALTA"),
    ],
    "paramos": [
        ("p02 p03 p10", 38.2, 77.5, "Las Minas de la Muerte", "Gilnid · Sneed · Cocinitas", "minas_muerte", "lo suelta Gilnid, en Las Minas de la Muerte", "M", W_, "ALTA (pin de mazmorra)"),
    ],
    # ---------------- mapa mundo: una ruta por parada
    "mundo:p01": [
        m("durotar", 53.1, 25.5, "p01", "Durotar", "cobre 1-65 (H)", "o_mena_cobre", "Del uno al sesenta y cinco, cobre", "R", I, "ALTA"),
        m("elwynn", 42.0, 76.8, "p01", "Elwynn", "cobre 1-65 (A)", "o_mena_cobre", "Del uno al sesenta y cinco, cobre", "R", I, "ALTA"),
        m("humedales", 47.3, 62.2, "p01", "Los Humedales", "estaño 65-125 (A)", "o_mena_estano", "una cueva de Los Humedales llena de estaño", "R", I, "ALTA"),
        m("argenteos", 58.1, 72.8, "p01", "Argénteos", "estaño 65-125 (H)", "o_mena_estano", "en el Bosque de Argénteos", "R", I, "ALTA"),
        m("arathi", 54.4, 76.0, "p01", "Arathi", "hierro y oro 125-175", "o_mena_hierro", "en las Tierras Altas de Arathi", "R", I, "ALTA"),
        m("mil_agujas", 43.3, 35.5, "p01", "Las Mil Agujas", "hierro 125-175", "o_mena_hierro", "o en Las Mil Agujas", "R", I, "ALTA"),
        m("riverglades", 55.5, 44.7, "p01", "Claros del Río", "133 vetas de hierro", "o_mena_hierro", "más vetas de hierro que ninguna otra zona", "R", I, "ALTA"),
        m("interior", 56.7, 43.9, "p01", "Tierras del Interior", "mitril 175-245", "o_mena_mitril", "en Tierras del Interior", "R", I, "ALTA"),
        m("tanaris", 33.5, 44.6, "p01", "Tanaris", "mitril 175-245", "o_mena_mitril", "o en Tanaris", "R", I, "ALTA"),
        m("ungoro", 67.3, 15.9, "p01", "Un'Goro", "torio 245-300", "o_mena_torio", "torio pequeño en Un'Goro", "R", I, "ALTA"),
        m("hyjal", 63.6, 86.7, "p01", "Monte Hyjal", "torio rico y pesado", "o_mena_torio_pesada", "Monte Hyjal tiene, además, más de cien vetas de torio rico", "R", I, "ALTA"),
    ],
    "mundo:p04": [
        m("durotar", 44.3, 65.2, "p04", "Durotar", "1-70", "o_flor_paz", "flor de paz y hojaplata en cualquier zona inicial", "R", I, "ALTA"),
        m("elwynn", 54.2, 44.5, "p04", "Elwynn", "1-70", "o_hojaplata", "flor de paz y hojaplata", "R", I, "ALTA"),
        m("argenteos", 54.5, 76.6, "p04", "Argénteos", "70-115", "o_brezospina", "en el Bosque de Argénteos", "R", I, "ALTA"),
        m("laderas", 36.5, 56.1, "p04", "Laderas", "115-170", "o_sangrerregia", "Laderas de Trabalomas", "R", I, "ALTA"),
        m("tuercespina", 35.1, 15.2, "p04", "Tuercespina", "170-205", "o_mostacho_khadgar", "la Vega de Tuercespina", "R", I, "ALTA"),
        m("tanaris", 46.9, 65.5, "p04", "Tanaris", "205-230", "", "Tanaris o La Garganta de Fuego", "R", I, "ALTA"),
        m("interior", 57.6, 42.6, "p04", "Tierras del Interior", "230-270", "o_champinon_fantasma", "Tierras del Interior", "R", I, "ALTA"),
        m("frondavil", 53.6, 14.9, "p04", "Frondavil", "270-300", "o_hojasueno", "y Frondavil", "R", I, "ALTA"),
        m("hyjal", 44.3, 75.2, "p04", "Monte Hyjal", "3 hierbas nuevas", "o_hojapesadilla", "en Monte Hyjal hay tres hierbas nuevas", "R", I, "ALTA"),
    ],
    "mundo:p06": [
        m("durotar", 42.9, 23.2, "p06", "Durotar", "1-75 (H)", "o_prof_desuello", "jabalíes en Durotar", "R", I, "ALTA"),
        m("elwynn", 44.1, 71.1, "p06", "Elwynn", "1-75 (A)", "o_prof_desuello", "lobos en el Bosque de Elwynn", "R", I, "ALTA"),
        m("baldios", 61.2, 54.7, "p06", "Los Baldíos", "75-150 (H)", "o_prof_desuello", "la Horda va a Los Baldíos", "R", I, "ALTA"),
        m("loch_modan", 63.2, 40.8, "p06", "Loch Modan", "75-130 (A)", "o_prof_desuello", "La Alianza, a Loch Modan", "R", I, "ALTA"),
        m("humedales", 34.5, 49.7, "p06", "Los Humedales", "130-150 (A)", "o_prof_desuello", "y luego a Los Humedales", "R", I, "ALTA"),
        m("alterac", 36.5, 85.9, "p06", "Cueva de yetis", "150-225", "o_prof_desuello", "la cueva de yetis de Laderas de Trabalomas", "R", I, "ALTA"),
        m("feralas", 54.6, 56.5, "p06", "Vega Cicatriz Feral", "225-280", "o_cuero_grueso", "los yetis de la Vega Cicatriz Feral", "R", I, "ALTA"),
        m("ungoro", 36.0, 35.2, "p06", "Un'Goro", "280-300", "o_cuero_basto", "los diemetradones y pterrordáctilos de Un'Goro", "R", I, "ALTA"),
    ],
    "mundo:p02": [
        m("baldios", 49.8, 29.4, "p02", "Campamento de Favor (H)", "Los Baldíos", "o_cajon_arrebatado", "al oeste de El Cruce, en Los Baldíos", "C", I, "ALTA"),
        m("crestagrana", 10.8, 72.4, "p02", "Campamento de Favor (A)", "Tres Caminos", "o_cajon_arrebatado", "la Alianza en Tres Caminos", "C", I, "ALTA"),
        m("tuercespina", 29.0, 75.4, "p02", "Brikk Finoficio", "herrería artesano", "brikk", "Brikk Finoficio, en Bahía del Botín", "P", I, "ALTA"),
        m("tanaris", 51.4, 28.6, "p02", "Derotain Sorbelodo", "piezas imperiales", "derotain", "en Tanaris, Derotain Sorbelodo", "P", I, "ALTA"),
    ],
    "mundo:p05": [
        m("pantano", 48.5, 55.8, "p05", "Rogvar", "artesano (H)", "rogvar", "Rogvar, en el Pantano de las Penas", "P", I, "ALTA"),
        m("feralas", 32.6, 43.8, "p05", "Kylanna", "artesano (A)", "kylanna", "Kylanna, en Feralas", "P", I, "ALTA"),
        m("frondavil", 51.5, 82.0, "p05", "Shurome", "1-300, los dos bandos", "shurome", "Shurome, en el Santuario Esmeralda de Frondavil", "P", I, "ALTA"),
    ],
    "mundo:p07": [
        m("feralas", 74.4, 43.1, "p07", "Hahrana Pielférrea", "artesano (H)", "hahrana", "Hahrana Pielférrea, en Feralas", "P", I, "ALTA"),
        m("interior", 13.4, 43.3, "p07", "Drakk Stonehand", "artesano (A)", "drakk", "Drakk Stonehand, en Tierras del Interior", "P", I, "ALTA"),
    ],
    "mundo:p09": [
        m("sierra_espolon", 49.2, 57.2, "p09", "Hgarth", "experto (H)", "hgarth", "Hgarth, en Sierra Espolón", "P", I, "ALTA"),
        m("elwynn", 64.8, 70.6, "p09", "Kitta Vientofuego", "experto (A)", "kitta", "Kitta Vientofuego, en la Torre de Azora", "P", I, "ALTA"),
        m("inhospitas", 44.2, 12.2, "p09", "Annora · Uldaman", "artesano", "annora", "solo lo enseña Annora, en Uldaman", "M", WL, "ALTA"),
    ],
    "mundo:p11": [
        m("tuercespina", 27.4, 77.0, "p11", "Viejo Heming", "Bahía del Botín", "viejo_heming", "el Viejo Heming, en Bahía del Botín", "P", I, "ALTA"),
        m("marjal", 58.4, 60.0, "p11", "Nat Pagle", "Marjal", "nat_pagle", "la misión de Nat Pagle, en el Marjal", "P", I, "ALTA"),
        m("feralas", 63.2, 52.2, "p11", "Río Verdantis", "Feralas", "", "y el Río Verdantis, en Feralas", "R", I, "ALTA"),
        m("desolace", 25.3, 70.4, "p11", "Costa de Desolace", "Aldea Cazasombras", "", "Desolace", "R", WL, "MEDIA (la guía no da el punto de la costa: se marca el pueblo)"),
    ],
    "mundo:p12": [
        m("arathi", 73.9, 35.8, "p12", "Sentencia", "Doctor Gregory Victor (H)", "gregory_victor", "el doctor Gregory Victor en Sentencia", "C", WL, "ALTA"),
        m("marjal", 65.0, 47.1, "p12", "Theramore", "Doctor Gustaf VanHowzen (A)", "vanhowzen", "el doctor Gustaf VanHowzen, en Theramore", "C", WL, "ALTA"),
        m("hyjal", 48.2, 33.6, "p12", "Pexmit", "Monte Hyjal", "pexmit", "El manual lo vende Pexmit, en Monte Hyjal", "P", I, "ALTA"),
    ],
}
# las tuplas «mundo» salen como (x, y, escena, rótulo, …): se reordenan a (escena, x, y, rótulo, …)
for k, v in PTS.items():
    if k.startswith("mundo"):
        PTS[k] = [(t[2], t[0], t[1]) + t[3:] for t in v]
COLOR = {"C": (255, 60, 60), "R": (255, 230, 0), "M": (80, 200, 255), "P": (255, 140, 255)}


def fuente(n):
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def hojas():
    F = fuente(15)
    minis = []
    for k, pts in PTS.items():
        m_ = k.split(":")[0]
        im = Image.open(os.path.join(D, "mapas", m_ + ".jpg")).convert("RGB")
        im = im.resize((1024, round(1024 * im.height / im.width)))
        W, H = im.size
        d = ImageDraw.Draw(im)
        for e, x, y, r, sub, foto, frase, t, *_ in pts:
            px, py = x / 100 * W, y / 100 * H
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
    print(len(minis), "mapas;", (len(minis) + por - 1) // por, "hojas")


def md():
    print("| Mapa | Escena | x, y (% del mapa) | Rótulo | Subrótulo | Foto (pegatina) | Frase del guion | Tipo | Fuente | Confianza |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for k, pts in PTS.items():
        for e, x, y, r, sub, foto, frase, t, f, c in pts:
            print(f"| `{k}` | {e} | {x:.1f}, {y:.1f} | {r} | {sub} | {('`' + foto + '`') if foto else '—'} | «{frase}» | {t} | {f} | {c} |")


if __name__ == "__main__":
    md() if sys.argv[1:] == ["md"] else hojas()
