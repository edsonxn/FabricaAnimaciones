# -*- coding: utf-8 -*-
"""Escribe busquedas.json: UNA entrada por beat ({"url","desde"}), en orden, pensada contra la FRASE de ese beat (lo que la voz
nombra se ve). Copiado de wow_errores_60/_busquedas.py (25-nov-2026), pero con la lista escrita beat a beat (BEATS) en vez de
por escena: la asignación de beats a escenas por texto falla en varias frases partidas (114, 157, 175, 179, 197, 199, 200).
Candidatos: `_buscar_fuentes.py` → `_candidatos.txt` (yt-dlp ytsearch). Un cuadro de cada fuente nueva se miró antes en hojas
(yt-dlp -g + ffmpeg -ss, sin bajar el video; muestreo denso cada 20 s en las de profesiones): fuera webcams (Borta,
MilleusPRO, warmane_ttv, BasedBellagio, TLo_5bG9HVQ, ZJ5WFDkLmrI), rótulos/títulos de guía encima (Scatter «EXPLOSIVES»,
Mobalytics «MINING», Graysfordays, dIlm8YLYB58, XDfRZfIMxGw, dARGlaGpJ64, Boophie, RestedXP de YJV6TprYEhE, KROZNIAS con
marco, subtítulos de 99EvgZrLwVg), retail (VN_7G5ryjAI, wUW3H2XJmpQ), imagen fija (JYTsVHcnaw8), banda negra (Old Man
Aggros) y la Blizzcon (Q-azB9f_GgM, Tgmqj33pzIM con webcam).
Fuentes principales: el video OFICIAL «Forever 101» (7P-i2zipbeM: campamentos, ventana de profesión de primeros auxilios con
pociones, peletería, entrenadores) y «What is WoW Forever?» (dvueCoFTkCk); la serie de Kaychak «Everything You Need to Know
About <profesión>» (gameplay de Forever con la ventana de profesión abierta; ENTRE sus fichas de objetos, que se evitan por
tramo); The Quiet Noodle «Human Hunter Journey» #06/#15 (silent, minería e ingeniería en Ventormenta, campamento en Elwynn);
pesca sin narrar (Carpathian Pack Theramore, Finnea Valanaar, SirSoapyy Cima del Trueno, Great Sea); ambientes de Forever ya
probados en wow_ruta_forever / wow_errores_60 (Azeroth Ambience, Wanderer's Hearth, NoloFaija, Ambient AFK, Long Rest Gran
Forja, fwengli por zona, DankeyKong y Esshow en mazmorras) y, para zonas viejas sin cambios, Meisio (Classic).
Evitar NFGames cQrWYBvskro / Ak0z7iSgH38 / TNI8WYnd04E / 9nZzTkK2Up8 (contador FPS|GPU arriba a la derecha).
`python _busquedas.py --check` = solo comprueba BEATS (nº de entradas = nº de beats, ids sin duración, offsets fuera,
tramos repetidos < 15 s)."""
import json
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def Y(i):
    return "https://www.youtube.com/watch?v=" + i


# Atajos
OF, WI = "7P-i2zipbeM", "dvueCoFTkCk"                      # oficiales de Blizzard (Forever 101 · What is WoW Forever?)
KMIN, KBS, KHERB, KSKIN = "BgZ5wT1I2lM", "Wd-g0Ovq_ns", "Escu3hZr6KY", "ahGpihPDmoI"   # Kaychak (Forever)
KALC, KLW, KTAI, KENC = "Fa-m_rCbNyo", "FaTWDJK7lRY", "_wb0uJ6JyZA", "s5isRnNljQw"
QN15, QN06 = "pfrtljRoutU", "mshxsH45j_g"                   # The Quiet Noodle, silent (minería e ingeniería; campamento)
THF, VAL, TBF, SEA = "RqPkxcbyNps", "1_V3FNh04B4", "fJ-Iw0Ju5Gg", "OYdSrBLCAaA"   # pesca: Theramore, Valanaar, Cima, mar
HYH = "WfUGw_UQS24"                                         # herboristería en Monte Hyjal (Forever)
HYJ, HYJ3, HYJ4, HYJ5 = "bUUN-RVAgZM", "QVin8qs0h4A", "eK06h9XuCvI", "55HBXBVUhn0"   # Monte Hyjal (capítulos en _candidatos)
MUL, TB, ORG, SW, TRD = "QAGqdbWCmBM", "BMPzO8CNuf8", "kZ79hHwLD7Q", "M50FQ2tRfnc", "dCN8NDX_9jI"
GF, GF2, DAR, UC, DAL, DALM = "kVLvo9cc1VA", "UhaBDdrBBAw", "vdpNu_Y1LqI", "DWg6fGdz6RQ", "kqan4pO91m8", "UZ7tLg_H-6c"
RIV, RIV2, RIV3 = "yCxEqGLFkxY", "N1oab1U4vcE", "ZDOvf5r8TC0"   # Claros del Río (Riverglades)
WETF, WET, SIL, ARA, ARA2 = "lvKtYowar-M", "ucWROaciLsQ", "KixNNeyjlbU", "jOJC-qG3v9g", "bQXbsVQotFc"
HIN, TAN, TAN2, UG, FEL, FER = "mRNqMdyJ-Wk", "_ciyszkqp8U", "Ngpi1TkXOJA", "mlzkgjTETX4", "ntdRpGZAgkY", "7W2i__XIZm4"
WS, EPL, BAR, BAR2, DUR_ = "63Kdh9JTEoQ", "g_bDII8Gofc", "3KISbNT5vNM", "ss1UBuxjDYQ", "CpsfPD8JOZg"
LOCH, DARK, ASH, HILLS, HILLS2 = "k8cxGSAmxEU", "iSmlVgquXcU", "niUqkQa8JnE", "YTJHwf1GZd8", "w-XXzLGrDw0"
STV, BB, STV2, DESO, SWAMP = "5DInpqWarTY", "t7M5yl2Y78A", "6H5hypjnLE8", "agf2NHPHn0I", "fedyKJwDMRo"
REDR, REDR2, ELW, STON, SG = "KGVdQ9qrp8c", "qtNLHvY926Q", "pepk2VjNNbo", "-6DqrXkNAHc", "A9dzFCjg2Bo"
AZS, SHEN, SKY = "e0TSZHUcnsg", "1ZBGXQP49Js", "AAymw7k7jR4"
DM, DM2, WC, BFD, GNOM, ULD = "xgPyJ9lGKaQ", "KABxlvoO63I", "Nzq3dPw0i1k", "xvcEWz8LUsY", "58BBfrSSpa8", "nZkVwoqAuwE"
BRD, BRD2, BRD3, SCH, SCH2 = "xlkl375-ic4", "rX3LNFZF74A", "WWUxcpmAexg", "rsAN0MpTZcw", "kifKvOCaaj4"
STRU, STRL, SHT, ONY = "i3gnRDz9mgw", "aXx72ExidLE", "jbPm5SLQm9U", "5bSGHYQTbQQ"
AH, CHK, LOOP2, DWP = "YIhM35KjtyA", "UMh80-64QLc", "sdAXLJUlags", "8aBwVTAnZLI"

# UNA entrada por beat, en orden (scene-001 … scene-218). Comentario = lo que dice la voz en ese beat.
BEATS = [
    # intro
    (KALC, 150),   # 001 el alquimista ya no hace pociones de sanación
    (HYJ, 400),    # 002 mena nueva en Monte Hyjal que no se funde
    (OF, 138),     # 003 telar con 300 · 28 millones de objetos de campamento
    (KBS, 90),     # 004 sin campamento te faltan estaciones de recetas
    (WI, 85),      # 005 zona por zona; hoy la otra ruta
    (KBS, 130),    # 006 doce profesiones, cuatro tramos, Alianza y Horda
    (QN15, 1690),  # 007 recetas nuevas, materiales nuevos
    (KHERB, 250),  # 008 empezamos por la recolección
    # reglas
    (OF, 197),     # 009 nueve principales y tres secundarias (entrenador orco)
    (VAL, 684),    # 010 cocina, pesca y primeros auxilios
    (QN06, 1745),  # 011 entrenar cuesta… (Therum Deepforge, herrero experto)
    (GF, 740),     # 012 rangos y niveles (Gran Forja)
    (QN15, 605),   # 013 hay que viajar a buscar al artesano (vuelo en grifo)
    (MUL, 3000),   # 014 entrenadores júnior en las zonas iniciales
    (KBS, 165),    # 015 ventana propia con la tecla K, quinta ranura
    (KENC, 30),    # 016 su valor está en lo que fabricas
    (WI, 228),     # 017 el campamento
    # overgear
    (SCH, 1500),   # 018 Overgear, coaching
    (CHK, 3000),   # 019 sesiones por voz o texto, juegas tú
    (STRU, 900),   # 020 talentos, rotación, errores
    (RIV3, 2000),  # 021 rama de talentos; camino del 60
    (ONY, 3000),   # 022 bandas del 9 de diciembre, Onyxia
    (KALC, 290),   # 023 consumibles de las profesiones
    (CHK, 4500),   # 024 lo que aprendes se queda
    (BRD3, 1500),  # 025 código CRONICAS10
    # p01 minería
    (KMIN, 450),   # 026 parada uno, minería, cobre
    (SKY, 2000),   # 027 vetas pobres en los valles de inicio
    ("4B0QugZ3uqs", 105),  # 028 elfos de la noche, ámbar (Teldrassil)
    (KMIN, 290),   # 029 cueva de Mulgore con cinco vetas
    (WETF, 1500),  # 030 estaño: cueva de Los Humedales
    (ARA, 2000),   # 031 hierro y oro: Arathi o Mil Agujas
    (RIV, 1100),   # 032 Claros del Río, 130 vetas de hierro
    (HIN, 1500),   # 033 mitril: Tierras del Interior o Tanaris
    (UG, 1500),    # 034 torio: Un'Goro, Frondavil, Cuna…
    (QN15, 1390),  # 035 fundir mena comprada
    (KMIN, 330),   # 036 pirita, bauxita, pecblenda
    (KMIN, 30),    # 037 Monte Hyjal: mena de torio pesada
    (GF, 1600),    # 038 no se funde en ninguna forja; fundición de magma
    (BRD, 1500),   # 039 Profundidades de Roca Negra; magnetita
    (KMIN, 420),   # 040 jardín rocoso; vetas de torio en Hyjal
    (HYJ3, 1450),  # 041 para los últimos puntos, es el sitio
    # p02 herrería
    (KBS, 210),    # 042 herrería, piedras de afilar
    (KBS, 250),    # 043 bronce: varas, leotardos, brazales
    (ORG, 1800),   # 044 experto en Orgrimmar (Saru Steelfury)
    (GF2, 1150),   # 045 Forjaz, la gran fragua
    (DARK, 1500),  # 046 en Darnassus no hay herrero: Auberdine
    (KBS, 290),    # 047 brazales de hierro verde, placas de mitril
    (BB, 1500),    # 048 Brikk Finoficio, Bahía del Botín
    (KBS, 370),    # 049 500-1200 barras de torio
    (KBS, 505),    # 050 ocho planos de placas bendecidas
    (HYJ4, 600),   # 051 el peto, arpías de Monte Hyjal
    (BAR, 2000),   # 052 campamento de mercaderes al oeste de El Cruce
    (REDR, 1500),  # 053 Tres Caminos, oeste de Crestagrana
    (QN06, 190),   # 054 campamento: rueda de afilar
    (DM, 2500),    # 055 Gilnid, Las Minas de la Muerte
    (BRD2, 1000),  # 056 Argelmach, Profundidades de Roca Negra
    # julsi
    (STRL, 1500),  # 057 piedras de afilar con venenos y Viento Furioso
    (QN06, 1150),  # 058 Julsikakku: minería 145, herrería 120
    (RIV2, 5000),  # 059 rumbo a la zona nueva
    # p03 ingeniería
    (OF, 226),     # 060 parada tres, ingeniería (taller gnomo)
    (QN15, 1450),  # 061 polvo explosivo, tornillos de cobre
    (QN15, 1570),  # 062 Orgrimmar o Forjaz; bombas, dinamita
    (QN15, 1870),  # 063 marcos de bronce
    (TAN, 2300),   # 064 ovejas explosivas; Gadgetzan
    (HYJ5, 500),   # 065 Kayleena Encantaflores, Monte Hyjal
    (WS, 1500),    # 066 tubos de torio; Cuna del Invierno
    (TB, 1500),    # 067 en Cima del Trueno no hay ingeniero
    (GNOM, 1500),  # 068 el gnomo ya no recibe sus 15 puntos
    (QN15, 1990),  # 069 explosivos seguros
    (QN15, 125),   # 070 parapente goblin
    (QN06, 245),   # 071 objetos de campamento: robots
    (DM, 3000),    # 072 Sneed, Las Minas de la Muerte
    # burla0 (Goca)
    (LOOP2, 3600),  # 073 la ruta del 1 al 60
    (ORG, 3000),   # 074 un video para cada facción
    (SW, 5000),    # 075 el lingote de la Alianza pesa lo mismo
    (QN15, 1030),  # 076 donde sí cambian, los entrenadores
    # gracias1
    (ELW, 3000),   # 077 Jesús, desde 2005, nostalgia
    (REDR2, 1500),  # 078 Óscar y Crestagrana
    (DWP, 26300),  # 079 Barón Rata va por el 30
    (WI, 145),     # 080 World of Warcraft sigue vivo
    # p04 herboristería
    (KHERB, 190),  # 081 parada cuatro, herboristería
    (MUL, 1500),   # 082 flor de paz y hojaplata en zona inicial
    (SIL, 1640),   # 083 Bosque de Argénteos, Loch Modan, Costa Oscura
    (HILLS, 600),  # 084 Laderas de Trabalomas o Sierra Espolón
    (STV, 1500),   # 085 Vega de Tuercespina o Arathi; Claros del Río
    (SG, 1500),    # 086 Tanaris o La Garganta de Fuego
    (FEL, 1500),   # 087 Tierras del Interior y Frondavil
    (HYH, 370),    # 088 tres hierbas nuevas en Monte Hyjal
    (KHERB, 12),   # 089 loto de la muerte de cualquier hierba de Hyjal
    (KHERB, 290),  # 090 semillas e invernadero
    (KHERB, 350),  # 091 injertador de semillas
    (KHERB, 372),  # 092 vela de incienso (campamento)
    (WET, 1500),   # 093 Los Humedales; parada cinco
    # p05 alquimia
    (KALC, 550),   # 094 elixir de fuerza menor
    (KALC, 690),   # 095 pociones de maná, elixires
    (FER, 1500),   # 096 receta en Feralas, Tuercespina o Tanaris
    (KALC, 330),   # 097 transmutaciones, elixir de defensa superior
    (HYH, 550),    # 098 mil hierbas
    (SWAMP, 700),  # 099 Rogvar, Pantano de las Penas
    (FEL, 2500),   # 100 Shurome, Santuario Esmeralda de Frondavil
    (KALC, 210),   # 101 las pociones de sanación ya no son del alquimista
    (KALC, 85),    # 102 ganó tintes
    (KLW, 570),    # 103 los piden la sastrería y la peletería
    (KALC, 430),   # 104 recetas de Favor; campamento
    (KALC, 250),   # 105 laboratorio de alquimia
    (SCH, 2500),   # 106 Ras Levescarcha, Scholomance
    # burla1 (Crisis)
    (AH, 120),     # 107 el video del oro
    (TRD, 720),    # 108 vende esto ya
    (KMIN, 230),   # 109 una veta de torio libre no espera
    # p06 desuello
    (KSKIN, 300),  # 110 parada seis, desuello
    (KSKIN, 30),   # 111 cinco veces su nivel
    (DUR_, 2500),  # 112 jabalíes en Durotar; Los Baldíos
    (BAR2, 1118),  # 113 raptores al oeste de Fuerte del Norte
    (HILLS, 2500),  # 114 cueva de yetis de Laderas
    (FER, 2000),   # 115 yetis de la Vega Cicatriz Feral; Un'Goro
    (BAR, 3000),   # 116 cuchillo afilado, misión en Los Baldíos
    ("jEr94Z_MGmE", 150),  # 117 cada criatura se desuella una vez
    (KSKIN, 190),  # 118 cuero prístino
    (RIV3, 1500),  # 119 Claros del Río: cuero pesado
    (HYJ4, 900),   # 120 Monte Hyjal: cuero basto; silla de campamento
    (WC, 600),     # 121 Lady Anacondra, Cuevas de los Lamentos
    (KSKIN, 410),  # 122 banco de trampero; parada siete
    # p07 peletería
    (KLW, 85),     # 123 peletería (ventana oficial)
    (TB, 2500),    # 124 Una en Cima del Trueno
    (SHEN, 1100),  # 125 Telonis, Jarael en Shen'dralas
    (FER, 1000),   # 126 Hahrana Pielférrea en Feralas
    (HIN, 2500),   # 127 Drakk Stonehand, Tierras del Interior
    (KLW, 150),    # 128 zapatos de gamuza azul
    (KLW, 210),    # 129 brazales y sombrero de gamuza azul
    (KLW, 275),    # 130 máquina de coser; 81 recetas de Favor
    (KLW, 430),    # 131 expositor de curtido
    (OF, 108),     # 132 la tienda de campamento
    (OF, 153),     # 133 experiencia de descanso
    (SCH2, 1500),  # 134 Vectus en Scholomance
    # p08 sastrería
    (KTAI, 150),   # 135 parada ocho, sastrería
    (CHK, 1500),   # 136 la tela te cae de los enemigos
    (UC, 1772),    # 137 Josef Gregorian en Entrañas
    (DAL, 4860),   # 138 Charles Worth en Dalaran
    (HILLS2, 1530),  # 139 Molino Tarren de Laderas
    (THF, 1489),   # 140 Theramore
    (KTAI, 255),   # 141 bolsas de tejido mágico rojas
    (HYJ3, 650),   # 142 Pexmit en Monte Hyjal
    (KTAI, 300),   # 143 mil cuatrocientos paños rúnicos
    (KTAI, 390),   # 144 bolsas de componentes
    (KALC, 30),    # 145 tinte cerúleo del alquimista
    (QN06, 210),   # 146 estandarte de facción (campamento)
    (DALM, 600),   # 147 centinela inestable, Ciudad de Dalaran
    (KTAI, 25),    # 148 el telar
    (KALC, 470),   # 149 un campamento con telar
    (STRU, 1500),  # 150 Baronesa Anastari; parada nueve
    # p09 encantamiento
    (KENC, 45),    # 151 mota de magia
    (KENC, 295),   # 152 recetas de nivel bajo
    (KENC, 70),    # 153 polvo extraño, varitas
    (STON, 1500),  # 154 Hgarth, Refugio Roca del Sol
    (ELW, 5000),   # 155 Torre de Azora, Elwynn
    (ULD, 1200),   # 156 Annora en Uldaman
    (QN15, 1330),  # 157 vara rúnica de arcanita
    (KENC, 210),   # 158 collares con Favor
    (KENC, 95),    # 159 encantamientos de arma nuevos
    (KENC, 330),   # 160 laúd encantado (campamento)
    (DALM, 1500),  # 161 Sombra del archimago, Ciudad de Dalaran
    (SHT, 1500),   # 162 Nanaya, Bancal del Creador
    # legado
    (BRD3, 3000),  # 163 sin encantador ese material no existe
    (QN06, 1450),  # 164 puntos de Legado
    (KHERB, 430),  # 165 la recolección no da puntos
    (QN06, 2050),  # 166 árbol de Legado de profesiones
    # burla2 (SoyoyoS)
    (SW, 8000),    # 167 el video del oro
    (ORG, 600),    # 168 basura, saludos
    (TRD, 1620),   # 169 embajador de Ventormenta
    (SW, 11000),   # 170 correcciones; parada diez
    # p10 cocina
    (KMIN, 390),   # 171 cocina, enciende el campamento
    ("A2iGSyxP93Q", 160),  # 172 hoguera básica
    (OF, 93),      # 173 alguien enciende la hoguera
    (QN06, 228),   # 174 te sientas un minuto
    ("A2iGSyxP93Q", 180),  # 175 hoguera de experto; 28 millones
    (TBF, 1472),   # 176 pececitos, pargo, siluro
    (DESO, 1500),  # 177 Wulan, Aldea Cazasombras, Desolace
    (ASH, 2500),   # 178 Vallefresno; misión de Gadgetzan
    (VAL, 1539),   # 179 serviolas, sopa de pargo nocturno
    (QN06, 1990),  # 180 comida con experiencia; recetas de Favor
    (REDR, 2500),  # 181 descarrioaleta de Crestagrana
    (WC, 1500),    # 182 Lord Serpentis, Cuevas de los Lamentos
    (DM, 3500),    # 183 Cocinitas, Las Minas de la Muerte
    # p11 pesca
    (SEA, 365),    # 184 cofres en mar abierto
    (TBF, 5153),   # 185 zona inicial, junto al agua
    (LOCH, 2160),  # 186 capitales, Baldíos, Loch Modan…
    (BB, 2500),    # 187 Viejo Heming, Bahía del Botín
    (THF, 790),    # 188 Nat Pagle, Marjal Revolcafango
    (TAN2, 600),   # 189 Frondavil, Feralas… Tanaris
    (THF, 2316),   # 190 la pecera (campamento)
    (VAL, 2394),   # 191 expositor de pesca
    (BFD, 600),    # 192 Gelihast, Cavernas de Brazanegra
    (STV2, 1500),  # 193 concurso de pesca de Tuercespina
    (AZS, 1500),   # 194 costa de Azshara
    # p12 primeros auxilios
    (VAL, 3000),   # 195 parada doce
    (KALC, 175),   # 196 la que más cambió
    (OF, 123),     # 197 las pociones de sanación son de primeros auxilios
    (KALC, 270),   # 198 vendas de lino o pociones menores
    (KHERB, 70),   # 199 cataplasma simple, flor de paz
    (ARA, 3000),   # 200 Deneb Camino en Arathi
    (ARA2, 1500),  # 201 Gregory Victor en Sentencia, Arathi
    (ARA, 1000),   # 202 salvas a quince heridos
    (KTAI, 330),   # 203 vendas de tejido mágico y paño rúnico
    (HYJ3, 950),   # 204 Pexmit, Monte Hyjal
    (HYJ, 1800),   # 205 Ortak Lomgok; torniquete
    (WI, 10),      # 206 equipo de primeros auxilios (campamento)
    (EPL, 1500),   # 207 laboratorio de médico de la peste
    (SCH, 600),    # 208 las pociones para la banda las haces tú
    # combos
    (WI, 128),     # 209 qué dos profesiones llevo
    (QN06, 1330),  # 210 minería con herrería o ingeniería
    (HYH, 640),    # 211 herboristería con alquimia
    (KLW, 530),    # 212 desuello con peletería
    (KTAI, 410),   # 213 sastrería con encantamiento
    (VAL, 2000),   # 214 las tres secundarias para todos
    # cierre
    (HYJ4, 700),   # 215 de la mena que no se funde…
    (OF, 76),      # 216 cuéntame qué dos profesiones llevas
    (WI, 188),     # 217 si tu hermandad no tiene encantador
    (WI, 30),      # 218 nos vemos en Azeroth
]

# FIJADO A MANO por beat (revisión de las hojas de `medios`): gana sobre BEATS al regenerar. Motivo en _rehacer.txt.
FIJO = {   # ronda 0 (bajar): OYdSrBLCAaA sin formato >= 720p
    "scene-184": (THF, 300),
    # ronda 1 (25-nov, hojas medios_01..11 + texto_clips): motivo en _rehacer.txt
    "scene-004": (KBS, 150), "scene-006": (QN06, 1270), "scene-011": (GF2, 2595), "scene-016": (QN06, 1570),
    "scene-017": ("A2iGSyxP93Q", 140), "scene-023": (QN15, 1510), "scene-041": (HYJ, 3050), "scene-043": (KBS, 230),
    "scene-051": (HYJ4, 630), "scene-060": (QN15, 1750), "scene-072": (DM2, 1500), "scene-076": (QN06, 1630),
    "scene-088": (HYH, 470), "scene-089": (HYH, 610), "scene-097": (QN06, 2110), "scene-103": (QN06, 1870),
    "scene-104": (KALC, 450), "scene-105": (QN06, 2230), "scene-106": (SCH, 2560), "scene-109": (KMIN, 50),
    "scene-110": (KSKIN, 320), "scene-119": (RIV, 2000), "scene-131": (KLW, 290), "scene-135": (QN06, 2170),
    "scene-141": (QN15, 1810), "scene-142": (HYJ3, 700), "scene-160": (LOOP2, 3630), "scene-198": (KALC, 310),
    "scene-206": ("A2iGSyxP93Q", 200), "scene-212": (QN15, 1930), "scene-218": (MUL, 6000),
    # ronda 2 (hoja de 3 cuadros de los rehechos)
    "scene-023": (QN06, 1390), "scene-043": (QN15, 430), "scene-106": (SCH2, 2200), "scene-131": (QN06, 2290),
    "scene-141": (QN15, 490), "scene-142": (HYJ, 1300), "scene-198": (QN15, 1630),
    # ronda 3 (25-nov, hojas de promesas: fichas grandes de objetos en inglés detrás de los gráficos)
    "scene-123": (QN15, 1100), "scene-143": (QN15, 2050), "scene-213": (QN06, 2400),
}


def _duraciones():
    """id -> segundos, de _candidatos.json de este video y de los dos videos de donde salen muchas fuentes."""
    d = {}
    for f in ("_candidatos.json", "../wow_ruta_forever/_candidatos.json", "../wow_errores_60/_candidatos.json"):
        try:
            c = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for qs in c.values():
            for lst in qs.values():
                for x in lst:
                    try:
                        d.setdefault(x[0], float(x[1]))
                    except (TypeError, ValueError, IndexError):
                        pass
    return d


DUR = _duraciones()


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
    print("sin duración:", sin or "-")
    print("offset fuera (se corrige solo):", malos or "-")
    print("tramos repetidos (< 15 s):", rep or "-")
    return len(L) == len(b) and not sin and not rep


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
