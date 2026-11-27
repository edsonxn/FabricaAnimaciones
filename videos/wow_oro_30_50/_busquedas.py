# -*- coding: utf-8 -*-
"""Escribe busquedas.json: UNA entrada por beat ({"url","desde"}), en orden, pensada contra la FRASE de ese beat (lo que la voz
nombra se ve). Copiado de wow_ruta_profesiones/_busquedas.py (26-nov-2026, subagente A de clips).
Cómo se eligió cada fuente: `_buscar_fuentes.py` → `_candidatos.txt` (yt-dlp ytsearch por puesto) y luego `_muestras.py` (12 cuadros
de cada fuente sin bajarla → previews/_muestras/<id>.jpg) MIRADOS uno a uno; el `desde` cae en un cuadro visto.
Fuera tras mirarlas: WEBCAM (todo Studen Albatroz, Frostadamus ANA932N3edk, Atacas, SoupaSoka, FsnMWtep3lM, uhUVBXjX2-c,
BaEIoE2bk4I, EyUgW_6s-_E, nJXSRz1t5_A, L9iJKSAgKo0, GjubIUWCEug), láminas de otro canal (Realm Gaming yzYMMH7eZVU / 8IGloZdV8JM,
Cynara G3VrXE5Zsu8, Porowl, Jaqumo), logo del canal (Haste 5Pq0vfd4M84, RyBot), subtítulos quemados (e3373N3IA1I), cámara de retrato
y «>> 10x» (uYabrwVbA30), retail (vA2PLurPf18, gyodPugWRp4, tcBNPl9sUrk), noche/oscuro (aoNg6ZTgBCU, V9q4XfM8O3w, tv0DrBT9CIg),
planos quietos (jtBZkBLmSSI, vtz6KNGJLWI, 92vlShqUwbw).
Fuentes principales: BarakGage «500 …» (gameplay sin rótulos: centauros de Desolace, gorilas Velo de Bruma, ogros Aplastacresta,
bestias de Las Tierras Devastadas, elementales de tierra; al final venden en la ciudad), Meisio (Desolace, Badlands, Swamp of Sorrows,
Blasted Lands, Feralas, Stranglethorn, Alterac; Vanilla), Azeroth Ambience y Riverglades de Forever, Azeroth Wayfarer (Feralas,
Tanaris, Blasted Lands, Classic/TBC), quest guides limpias (Bue «The Decisive Striker», Mudrock, Mokk, Lo'Grosh, Sootfur).
OJO: FHyOCXfqTd8 y tPrE1iMupgE (Cueva Niebla Negra) y xmJmTzLUn8k (hienas Llagapata) son de un cliente posterior a Classic (interfaz
de Cataclysm), con los mismos modelos y la misma zona: dudosos, a mirar en la hoja.
`python _busquedas.py --check` = solo comprueba BEATS (nº de entradas = nº de beats, ids sin duración, offsets fuera, tramos
repetidos < 15 s y tramos < 15 s de uno usado en OTRO video, regla «no reciclar escenas»)."""
import glob
import json
import os
import re
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def Y(i):
    return "https://www.youtube.com/watch?v=" + i


# Atajos (id · qué enseña · cuadros mirados)
CEN = "cKUdY1tO_sY"     # BarakGage, centauros de Desolace (81-384 combate; 566-688 vende en la ciudad)
DESO = "agf2NHPHn0I"    # Meisio, Desolace Vanilla (1165 poblado, 1433 bestia, 1701 atardecer)
DMC = "FHyOCXfqTd8"     # Cueva Niebla Negra con arañas verdes (28-49 fuera, 70-155 dentro) · cliente Cata
DMC2 = "tPrE1iMupgE"    # Everyquest, Cueva Niebla Negra (35 fuera, 50-172 dentro) · cliente Cata
DWM = "mhZ9pQxeHzg"     # Marjal Revolcafango Classic (1292-2018 costa/arena)
BRK = "6M-qAITCOxo"     # Poblado Murohelecho (119-142)
THF = "RqPkxcbyNps"     # Theramore (330-577 la torre del faro)
GOR = "gCCbA-4HP-w"     # BarakGage, gorilas Velo de Bruma (92-370; 643-781 vende)
STVM = "CocRRyd-mis"    # Meisio, Tuercespina gameplay (1165-3312 selva)
STVA = "5DInpqWarTY"    # Tuercespina ambience (387 selva, 2120 campamento, 2986 costa)
MOKK = "CePtRaE3Sgs"    # Mokk el Salvaje (105 Mokk, 177-250 gorilas en la selva)
SF = "OFCHZAwE70A"      # Tomosak, El Desierto de Sal Classic (197-490, 931-1372 sal; 1519 Circuito del Espejismo)
MUD = "pQUaI5x6T9w"     # tortugas Fangorroca, Marjal (53-490)
RIVA = "N1oab1U4vcE"    # Azeroth Ambience, Claros del Río (2090 costa con barco, 5363 cortijo, 10818 torres)
RIVB = "yCxEqGLFkxY"    # Claros del Río ambience (942 pueblo, 1345-1747 río, 2552 puerto, 4565 rocas rojas)
BBF = "5pBk-dvSLIk"     # pesca en el muelle de Bahía del Botín (1329+ con hoguera)
CLAM = "WzVbdJH62gw"    # Clamlette Surprise: Tanaris (106-345) y almejas bajo el agua (425-823)
WH1 = "fvPEp_Eoif8"     # crías escaldantes, Barranco Lethlor (112-865)
WH2 = "p4M4YGzhdSw"     # crías escaldantes (380-3215, marcos de add-on abajo)
WH3 = "FdJGBG4tpQo"     # crías, Barranco Lethlor (61-430)
MUR = "uXfShCrgYBU"     # MMO Unlocked (Forever), múrlocs en la playa del Pantano de las Penas (106-300, 381-426)
TURT = "Y8jnaxp5XG4"    # botín de tortugas de Tanaris: bolsas con almejas (270-422)
SOSM = "2MdgWiy2G2E"    # Meisio, Pantano de las Penas (628 Rocal, 1165, 1701 bestia, 2506 costa)
SOSF = "fedyKJwDMRo"    # Forever, cazador en el Pantano de las Penas (155-1426)
HYE = "xmJmTzLUn8k"     # Everyquest, hienas Llagapata en las dunas (64-217) · cliente Cata
ROC = "YW6SNBBT3MA"     # rocs de fuego entre los esqueletos de las Arenas Abisales (43-402)
TANM = "Xs0Ch-ecOOc"    # Meisio, Tanaris Classic (2790 edificios)
TANW = "cyHmrabJ3eA"    # Azeroth Wayfarer, Tanaris (457-3867 dunas)
FERW = "XbVkci_8oVk"    # Azeroth Wayfarer, Feralas 43-44 (531-4887)
FERM = "dSz-qa1iBJY"    # Meisio, Feralas Vanilla (896-1165 gorila/Groddoc, 1433-2238 selva)
HUNT = "4TOvB5zg4vo"    # Forever, Claros del Río: cazadoras (11-54)
ELEM = "7xWRj5hv1n8"    # BarakGage, elementales de tierra en Tierras Inhóspitas (74-350; 460-626 vende)
BADM = "bWr3nnslZGw"    # Meisio, Tierras Inhóspitas Vanilla (360 Kargath, 1701 campamento goblin, 1970)
BADQ = "MRMiTCulm8I"    # Quest Ambience, Tierras Inhóspitas Classic (2238 puerta de Kargath)
COY = "_u4J4IFhKLg"     # Forever, bestias de Claros del Río (15-71, 105-139)
DMF = "sXkQ09MZUzI"     # Feria de la Luna Negra en Forever (57-305)
ZEZ = "DUmEhAy-e2Y"     # zezsigaming, farmeos de Forever con cronómetro (172 cortijo, 212-292 colinas)
SOOT = "6oz8K8LvTrE"    # Forever, cueva de Sootfur (9-90)
TRUNK = "ivKkomlytwc"   # Forever, pesca de valijas en la costa de Tuercespina (60-373; 417-552 abre valijas)
OGR = "3x1PrbChs5Q"     # BarakGage, ogros Aplastacresta (100-174, 323, 473 cueva, 547-622)
OGRB = "GLDaOMexZUY"    # Bue, Crushridge Bounty Classic (177-376 nieve)
LOG = "HCk0awfBAVw"     # cueva azul de Alterac y Lo'Grosh (30-277; 187 Lo'Grosh)
OGRF = "5LL7AilOtoc"    # Forever, ogros Aplastacresta (77-125)
ALTM = "YTJHwf1GZd8"    # Meisio, Trabalomas y Alterac (2881-3345 nieve)
BLQ = "zPAYBFwmTr4"     # Bue, The Decisive Striker: Las Tierras Devastadas (21-178)
BLW = "awO0j9R6AcU"     # Azeroth Wayfarer, Las Tierras Devastadas TBC Classic (371-1201, 2030-3414)
BLB = "ViTYXEQ9M88"     # BarakGage, bestias de Las Tierras Devastadas (59-280; 324-501 vende)
BLM = "Eciydcfo2M4"     # Meisio, Las Tierras Devastadas Vanilla (1701 Castillo de Nethergarde)
BLF = "0jBQNc0A7jc"     # Forever, vuelo sobre Las Tierras Devastadas (17-118)
RIDE = "HmsBzSMGlKM"    # Forever, instructor de equitación (68-77 ventana)
TAL = "IuAQ1Brg6NA"     # instructor de clase + talentos (14-129)
TRN = "TRYuJ04wdRE"     # Forever, instructor de guerrero de Valanaar
MNT = "s0UgqWRk-mM"     # Forever, monturas (355-597 montado)
PAL = "UMh80-64QLc"     # Forever, paladín humano sin comentarios
DWF = "8aBwVTAnZLI"     # Forever, paladín enano (longplay)
SCH = "rsAN0MpTZcw"     # Forever, Scholomance (1060, 2040)
STR = "i3gnRDz9mgw"     # Forever, Stratholme
ONY = "cULw3cMPvPs"     # Onyxia sin comentarios

# UNA entrada por beat, en orden (scene-001 … scene-175). Comentario = lo que dice la voz en ese beat.
BEATS = [
    # gancho
    (RIDE, 72),     # 001 nivel 40, instructor de equitación, abres la bolsa
    (TAL, 40),      # 002 instructor de clase, doble especialización
    (ZEZ, 172),     # 003 un jugador probó farmeos con cronómetro
    (BLB, 59),      # 004 cráter negro de Las Tierras Devastadas, el buitre
    (LOG, 35),      # 005 cueva de Alterac con vetas y un vendedor enjaulado
    (CEN, 142),     # 006 quince farmeos: qué matar, dónde, a quién vender
    (BLF, 29),      # 007 del que menos al que más; el uno sin profesión
    # comentarios del gancho
    (MNT, 360),     # 008 llegó al cuarenta con montura
    (GOR, 712),     # 009 se quedó con tres de oro (vende en la ciudad)
    (TRN, 25),      # 010 entrenamientos y profesiones; Azazel
    (RIVA, 11909),  # 011 un solo objeto, en una zona vacía
    # reglas
    (STR, 1161),    # 012 mazmorras: cinco por hora
    (RIVB, 1747),   # 013 el oro está en el mundo abierto
    (ROC, 43),      # 014 los huevos gigantes se hundieron
    (BLB, 330),     # 015 lo que paga el vendedor
    (BLQ, 84),      # 016 cualquier clase; el buitre no pregunta
    (CEN, 627),     # 017 la ficha de cada farmeo (bolsas)
    # 15 centauros Magram
    (CEN, 81),      # 018 número quince, Poblado Magram, Desolace
    (CEN, 200),     # 019 retadores, cazavientos, corremanadas
    (CEN, 263),     # 020 Blizzard: reaparecen más rápido
    (DESO, 1165),   # 021 nadie lo ha medido
    (CEN, 324),     # 022 monedas y paño de seda
    (DESO, 1433),   # 023 las hienas Zarpósea
    (CEN, 370),     # 024 entras, matas, la bolsa se llena
    # 14 arañas Niebla Negra
    (DMC, 40),      # 025 vender. Número catorce: Cueva Niebla Negra
    (DWM, 1534),    # 026 fuera y dentro de la cueva, norte del marjal
    (DMC, 85),      # 027 arañas y ermitañas; mandíbula
    (DMC2, 60),     # 028 punta de pata; seda de araña espesa
    (DMC, 125),     # 029 seda de las Sombras; sastres
    (DMC2, 115),    # 030 pocas apariciones; el raro de la cueva
    (BRK, 119),     # 031 Poblado Murohelecho; la Alianza en la Isla
    (THF, 577),     # 032 Theramore
    # overgear (gameplay neutro de World of Warcraft)
    (PAL, 3881),    # 033 saber jugar tu personaje
    (PAL, 1238),    # 034 coaching por voz o texto
    (SCH, 1060),    # 035 talentos, rotación, errores
    (DWF, 15591),   # 036 las guías no siempre van al día
    (ONY, 480),     # 037 camino del sesenta; Onyxia
    (SCH, 2040),    # 038 consumibles, equipo previo
    (ELEM, 184),    # 039 más oro por hora en estos quince
    (DWF, 24347),   # 040 lo que aprendes se queda contigo
    (RIVA, 4272),   # 041 código CRONICAS10
    # 13 gorilas Velo de Bruma
    (GOR, 92),      # 042 número trece, gorilas Velo de Bruma
    (GOR, 230),     # 043 sin misión de matarlos
    (STVM, 1165),   # 044 Lago Nazferiti; Valle del Velo de Bruma
    (GOR, 299),     # 045 pelo y colmillo de gorila
    (MOKK, 100),    # 046 La fiebre de Tuercespina, Mokk el Salvaje
    (GOR, 161),     # 047 cinco o seis de oro por hora
    (GOR, 355),     # 048 pocos gorilas; rinde solo
    (MOKK, 200),    # 049 baja a los ancianos
    # burla Lalo
    (PAL, 1766),    # 050 clip bait
    (ROC, 76),      # 051 los huevos gigantes, de un oro a quince platas
    (RIVA, 7545),   # 052 quince lugares que casi nadie farmea
    # 12 tortugas brillavalva
    (SF, 197),      # 053 número doce, El Desierto de Sal
    (SF, 344),      # 054 no son las de Tanaris
    (SF, 490),      # 055 fragmento de caparazón moteado
    (SF, 931),      # 056 carne de tortuga
    (SF, 1078),     # 057 cuatro platas por tortuga
    (SF, 1225),     # 058 Cráter de la Comadreja
    (SF, 1519),     # 059 Circuito del Espejismo
    (MUD, 132),     # 060 cavapozos Fangorroca del Marjal
    # gracias
    (PAL, 2400),    # 061 Alexander
    (DWF, 9753),    # 062 poco tiempo para jugar
    (DWF, 12672),   # 063 David, Rolazabal
    (RIVB, 942),    # 064 suscríbete
    # 11 reptadores de arena
    (RIVA, 2090),   # 065 número once, Claros del Río
    (RIVB, 2552),   # 066 cangrejos al sur del Puerto Polvomecha
    (RIVA, 3181),   # 067 carne de cangrejo tierna
    (RIVB, 1345),   # 068 la compran los cocineros
    (BBF, 1329),    # 069 cocina en doscientos: guiso
    (RIVB, 2620),   # 070 misión Sabores de mar
    (STVA, 2986),   # 071 reptadores del sur de Tuercespina
    (CLAM, 425),    # 072 dentro de las almejas hay perlas
    # 10 crías del Barranco Lethlor
    (WH1, 112),     # 073 número diez, crías que escupen fuego
    (WH1, 279),     # 074 este de la zona; glándula
    (WH2, 663),     # 075 ají aliento de dragón
    (WH3, 153),     # 076 Vástago oscuro
    (WH1, 447),     # 077 corazón de draco negro
    (WH2, 1230),    # 078 cien crías por un corazón; experiencia
    (WH2, 2081),    # 079 vetas de mitril; élites
    (WH1, 614),     # 080 por los bordes
    # burla Pkponcho
    (PAL, 5900),    # 081 Pkponcho
    (DWF, 27266),   # 082 tú eres el segundo
    # 9 múrlocs del Pantano de las Penas
    (MUR, 106),     # 083 número nueve, múrlocs
    (MUR, 152),     # 084 cuatro tipos; Cueva Stagalbog
    (MUR, 198),     # 085 almeja de boca grande
    (TURT, 270),    # 086 perla de oro
    (TURT, 371),    # 087 perla negra e iridiscente
    (MUR, 244),     # 088 monedas, serviola, botas épicas
    (MUR, 289),     # 089 oráculos: té soleado
    (SOSM, 2506),   # 090 carne de almeja; la playa
    (MUR, 395),     # 091 Puesto Juncobruma
    # 8 hienas Llagapata
    (HYE, 64),      # 092 número ocho, hienas Llagapata
    (ROC, 207),     # 093 rocs de fuego
    (HYE, 102),     # 094 melena espesa, pata de trofeo
    (HYE, 140),     # 095 cuero grueso, carne de lobo
    (HYE, 178),     # 096 carne de lobo tierna
    (CLAM, 266),    # 097 triángulo por los esqueletos de dinosaurio
    (ROC, 370),     # 098 huevos a veinte platas
    (TANM, 2790),   # 099 Gadgetzan
    (TANW, 798),    # 100 si estas dunas están llenas
    # gracias
    (RIVB, 4100),   # 101 Lunatic, Brasil
    (DWF, 30185),   # 102 BiNWinslou
    (FERW, 2511),   # 103 gracias; número siete
    # 7 gorilas y osos de Feralas
    (FERM, 890),    # 104 Tronadores Groddoc, patriarcas Cueracero
    (FERM, 1165),   # 105 Los Dos Colosos
    (FERW, 2907),   # 106 hueso de oso grande
    (FERM, 1433),   # 107 mandíbula de oso, garra
    (FERM, 1701),   # 108 misión previa al Templo Sumergido
    (FERW, 3303),   # 109 simios del centro
    (FERM, 2238),   # 110 Campamento Mojache, Bastión Plumaluna
    # 6 jaguares del Pantano de las Penas
    (SOSM, 1701),   # 111 número seis, jaguares
    (SOSF, 386),    # 112 colas y bigotes de felino
    (SOSF, 733),    # 113 desuello y hierbas
    (SOSM, 628),    # 114 Rocal
    (HUNT, 11),     # 115 plan B: cazadoras de Claros del Río
    (SOSF, 1080),   # 116 diez de oro por hora
    (SOSM, 1165),   # 117 número cinco
    # 5 elementales de roca
    (ELEM, 74),     # 118 elementales de roca
    (ELEM, 129),    # 119 aparecen más seguido
    (BADM, 360),    # 120 Kargath; Explanada del Espejismo
    (ELEM, 239),    # 121 superiores; grises de piedra
    (ELEM, 295),    # 122 tierra elemental
    (ELEM, 350),    # 123 diez de oro por hora
    (BADQ, 2238),   # 124 Kargath
    (BADM, 1701),   # 125 campamentos goblin
    (BADM, 1970),   # 126 el nueve de diciembre
    # 4 coyotes de Claros del Río
    (COY, 15),      # 127 número cuatro, coyotes
    (RIVA, 5450),   # 128 sur del Cortijo de Wheeler
    (COY, 60),      # 129 cola tupida suave
    (DMF, 62),      # 130 Feria de la Luna Negra
    (ZEZ, 212),     # 131 media hora con cronómetro
    (ZEZ, 252),     # 132 el jugador del treinta y nueve
    (SOOT, 17),     # 133 Sootfur
    (RIVB, 4565),   # 134 pasas a Tierras Inhóspitas
    # 3 pesca de valijas
    (TRUNK, 60),    # 135 número tres, pesca en Tuercespina
    (TRUNK, 104),   # 136 restos flotantes
    (TRUNK, 149),   # 137 bancos de anguila
    (TRUNK, 462),   # 138 qué hay dentro (bolsas)
    (TRUNK, 194),   # 139 Maestro del cebo
    (TRUNK, 507),   # 140 cuatro valijas en un lance
    (TRUNK, 238),   # 141 quince a cuarenta por hora
    (TRUNK, 283),   # 142 ciento setenta de oro
    (BBF, 423),     # 143 expositor de pesca; caminar sobre el agua
    (STVA, 2120),   # 144 Grom'Gol, costa oeste, Bahía del Botín
    (TRUNK, 545),   # 145 las valijas se abren
    # 2 cuevas de ogros de Alterac
    (OGR, 100),     # 146 número dos, ogros de Alterac
    (OGRB, 210),    # 147 Dominios de los Aplastacresta, dos cuevas
    (LOG, 97),      # 148 vetas de cinco minerales
    (LOG, 140),     # 149 treinta y ocho vetas
    (OGR, 174),     # 150 los ogros sueltan plata y seda
    (LOG, 180),     # 151 Rizz Tornillosuelto; Lo'Grosh
    (LOG, 225),     # 152 El pacificador; cuevas vacías
    (OGRF, 77),     # 153 treinta de oro por hora
    (OGR, 547),     # 154 aplastadores y magos élite
    (OGR, 473),     # 155 quédate en las cuevas
    # 1 destripadores negros
    (BLQ, 21),      # 156 número uno, destripadores negros
    (BLW, 647),     # 157 cráteres negros; molleja
    (BLQ, 52),      # 158 El vigor del buitre
    (BLQ, 110),     # 159 El golpe decisivo; 92 objetos
    (BLB, 103),     # 160 cuarenta y uno de oro por hora
    (BLQ, 140),     # 161 noventa platas por buitre
    (BLW, 924),     # 162 treinta y dos puntos de aparición
    (BLB, 191),     # 163 Scorpok; competencia
    (BLM, 1701),    # 164 Castillo de Nethergarde
    (SOSM, 660),    # 165 vuelo del Pantano de las Penas
    # la ruta por nivel
    (SF, 1372),     # 166 del treinta al treinta y cinco
    (ALTM, 3036),   # 167 del treinta y cinco al cuarenta
    (WH1, 530),     # 168 del cuarenta al cuarenta y cinco
    (TANW, 2162),   # 169 del cuarenta y cinco al cincuenta
    (BLW, 2307),    # 170 buitres; la pesca
    (ELEM, 571),    # 171 mira lo que paga el vendedor
    # cierre
    (BLF, 93),      # 172 del centauro al buitre
    (RIVA, 10818),  # 173 cuéntame en los comentarios
    (MNT, 597),     # 174 suscríbete; sin montura
    (RIVA, 13000),  # 175 nos vemos en Azeroth
]

# FIJADO A MANO por beat (revisión de las hojas de `medios`): gana sobre BEATS al regenerar. Motivo en _rehacer.txt.
RG = "i5mudUrqOks"       # RageGaming (Forever), valijas: 90 restos flotantes, 139 campamento, 189-224 talentos de Legado,
                        # 228-245 pesca (dice «cuatro valijas en un lance» en 225-232), 683 Grom'Gol, 732 abre valijas, 831 sobre el agua
RIZZ = "g3ZDEW8FyOE"    # Bue, ruta a Rizz Tornillosuelto en Alterac (46-55 cueva, 98-107 Rizz)
MAG = "p7eF63I1s8Q"     # Bue, Gelkis = matar centauros MAGRAM en su poblado (15-38 tiendas, 60-95 torre, 106-140 combate)
FIJO = {   # ronda 0b (antes de mirar las hojas): momentos exactos hallados con los subtítulos (yt-dlp --write-auto-subs) y muestras
    "scene-136": (RG, 85), "scene-139": (RG, 195), "scene-143": (RG, 135), "scene-144": (RG, 680),
    "scene-145": (RG, 728),
    "scene-086": (MUR, 347), "scene-087": (MUR, 372), "scene-091": (MUR, 450),
    "scene-151": (RIZZ, 97), "scene-152": (LOG, 180), "scene-149": (LOG, 140), "scene-148": (LOG, 97),
    # ronda 1 (mosaicos _rehechos_a*, 3 cuadros por clip): motivo en _rehacer.txt
    "scene-003": (COY, 110), "scene-010": (TAL, 80), "scene-039": (COY, 135), "scene-042": (GOR, 265),
    "scene-018": (MAG, 14), "scene-019": (MAG, 29), "scene-020": (MAG, 78), "scene-021": (MAG, 62), "scene-022": (MAG, 120),
    "scene-024": (MAG, 138), "scene-107": (FERM, 1000), "scene-111": (SOSF, 155),
    "scene-131": (COY, 38), "scene-132": (HUNT, 40), "scene-150": (OGR, 323),
    "scene-154": (OGRB, 330), "scene-159": (BLQ, 165), "scene-171": (BLB, 420),
    # ronda 3 (texto_clips: OCR 1 cuadro/s)
    "scene-009": ("ndWzTAd9h38", 318), "scene-017": (BLB, 465),
}


def _duraciones():
    """id -> segundos: de los registros de _muestras*.log y de _candidatos.json."""
    d = {}
    for f in glob.glob("_muestras*.log"):
        for ln in open(f, encoding="utf-8", errors="replace"):
            m = re.match(r"([\w-]{11}): (\d+)s ", ln)
            if m:
                d[m.group(1)] = float(m.group(2))
    try:
        c = json.load(open("_candidatos.json", encoding="utf-8"))
        for qs in c.values():
            for lst in qs.values():
                for x in lst:
                    try:
                        d.setdefault(x[0], float(x[1]))
                    except (TypeError, ValueError, IndexError):
                        pass
    except Exception:
        pass
    return d


DUR = _duraciones()


def _otros():
    """(video, desde) ya usados en OTROS videos (regla «no reciclar escenas entre videos»)."""
    out = []
    for f in glob.glob("../*/fuentes.json"):
        if os.path.abspath(f) == os.path.abspath("fuentes.json"):
            continue
        try:
            for k, r in json.load(open(f, encoding="utf-8")).items():
                if not k.startswith("_") and isinstance(r, dict) and r.get("video"):
                    out.append((r["video"], float(r.get("desde", 0)), f.split(os.sep)[-2] if os.sep in f else f))
        except Exception:
            pass
    return out


def desde_seguro(i, desde):
    """Nunca más allá de la duración (deja 15 s de margen); si se pasa, da la vuelta."""
    dur = DUR.get(i)
    if not dur:
        return float(desde)
    tope = max(1.0, dur - 15)
    return float(desde % tope) if desde > tope else float(desde)


def lista():
    out = list(BEATS)
    for k, v in FIJO.items():
        n = int(k[-3:]) - 1
        if 0 <= n < len(out):
            out[n] = v
    return out


def comprobar():
    b = json.load(open("beats.json", encoding="utf-8")) if os.path.exists("beats.json") else []
    L = lista()
    print(f"{len(L)} entradas · {len(b)} beats" + ("" if len(L) == len(b) else "  ← NO COINCIDEN"))
    sin = sorted({i for i, _ in L if i not in DUR})
    malos = [f"{n + 1:03d}:{i}@{d}>{DUR[i]:.0f}" for n, (i, d) in enumerate(L) if i in DUR and d > DUR[i] - 15]
    rep = []
    for n, (i, d) in enumerate(L):
        for m in range(n):
            if L[m][0] == i and abs(L[m][1] - d) < 15:
                rep.append(f"{m + 1:03d}/{n + 1:03d}:{i}@{d}")
    otros = _otros()
    recic = [f"{n + 1:03d}:{i}@{d}≈{v}@{dd:.0f}" for n, (i, d) in enumerate(L) for (vi, dd, v) in otros
             if vi == i and abs(dd - d) < 15]
    print("sin duración:", sin or "-")
    print("offset fuera (se corrige solo):", malos or "-")
    print("tramos repetidos (< 15 s):", rep or "-")
    print("tramos ya usados en otro video (< 15 s):", recic or "-")
    print(len({i for i, _ in L}), "fuentes distintas")
    return len(L) == len(b) and not sin and not rep and not recic


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if comprobar() else 1)
    b = json.load(open("beats.json", encoding="utf-8"))
    L = lista()
    if len(L) != len(b):
        raise SystemExit(f"BEATS tiene {len(L)} entradas y hay {len(b)} beats: corrige antes de escribir busquedas.json")
    out = {x["id"]: {"url": Y(i), "desde": desde_seguro(i, d)} for x, (i, d) in zip(b, L)}
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats → busquedas.json ·", len({i for i, _ in L}), "fuentes")
