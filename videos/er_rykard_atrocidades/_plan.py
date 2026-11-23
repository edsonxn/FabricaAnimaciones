# -*- coding: utf-8 -*-
"""Plan de clips POR FRASE (22-nov-2026), hecho mirando hojas de contacto a 240p de cada fuente
(E:\\FabricaAnimaciones\\_tmp_hojas_rykard\\h\\*.jpg: una hoja por fuente + hojas finas «fino_*» de los momentos exactos;
v\\v_NN.jpg = comprobación final de TODAS las opciones, 3 cuadros por clip a +0,5 / +4,3 / +8,1 s). Escribe plan_frases.json
(lo lee asignar_clips.py).
    python _plan.py
Fuentes limpias: SourceSpy91 4K sin comentarios con HUD normal (P28 monte Gelmir, P29 Mansión, P30 Rykard, P12 Academia,
P46 Farum Azula), pgp (EL, la cinemática de la fase 2 entera, sin HUD), VynPlays 4K (YJ, combate + cinemática + muerte),
Kelvyn Acevedo (KG, imagen LAVADA de poco contraste: solo Ghiza, Tanith y Rya), Jaemekon (JM, Ghiza), Terry Goodwin (GH
fantasma, BE Bernahl, TA Tanith: diálogos con subtítulos del juego), Soul Cat y Kevin B (GD/GK, Gideon en su despacho: plano
fijo), Stratek (PE Parches, RS Rogier: plano fijo; máx. 1-2 por puesto), Indyrael (RG Rogier), Zero Manga Hunter (PC, Parches
te tira por el precipicio), SBG (PA, Parches tras Rykard), Aethersong / IAmToastMan / ShyKatana / PANxWAR (AT/TM/SK/PW: la
virgen raptora bajo la noria de Raya Lucaria, el traslado y el jefe doble), Sunless_Solaire (RY, todas las escenas de Rya SIN
el Sinluz en pantalla, con carteles negros del canal entre escenas), BonfireVN (GW, el cadáver de Godwyn), WilliamDoe (WD,
Maliketh con la Garra blasfema), Nutler (NU, el monumento del asalto con su texto), Veloketh (MS, Messmer sin HUD), GameOnDude
(RN, cinemáticas de Rennala), 4KGameScape (RA, final de Ranni), Leomega (LR, Radahn, imagen lavada), Part Time Gamer (GN,
Noble sacrodermo).
Ojo (marcas, menús, mapas, rótulos; segundos de la fuente):
 - P29: menús 520-530, 640, 1030, 1560, 1780, 2180-2190, 2270, 2990-3020, 3400, 3890-3900, 4350, 4570, 4720-4730; MAPA 2210,
   2240-2250, 4740-4750; negro 360, 2220, 4760; destello del sol 120; aviso de objeto 10, 140-146 (es el ALMA ESTANCADA: vale),
   4673-4676 (el retrato), 4278; «INVADER VANQUISHED» 324; diálogos con subtítulos del juego (Tanith 200-250, 800-830; fantasma
   398-491). El invasor rojo de 290-322 es el inquisidor Ghiza con su rueda (316-320).
 - P30: menús 16-31, 56-72, 412-448, 656-660, 680-692; MAPA 484, 624-628, 708-712; negro 12, 196, 716; pantalla de carga 488-492.
   La lanza Cazador de serpientes clavada en el montón de cadáveres: 44-52 (se recoge a 52-55: aviso de objeto).
   Cinemática de la fase 2 = 200-276 (= EL +200); muerte 376-388; Tanith 496-552 y Bernahl 560-620 con subtítulos.
 - P28: menús 108, 648, 756, 1140-1152, 1428, 2592, 2616, 2964, 3336-3384, 4008, 4596, 4656-4668, 4704; MAPA 1200, 1992, 2484,
   2844, 3672, 3876; negro 2052, 2832; aviso de invasión 595-598 (Anastasia: NO es Parches). Vírgenes raptoras por las laderas
   180-500; campamentos en ruinas con empalizadas 5545-5650.
 - EL (76 s): fogonazo de fuego BLANCO-amarillo 50-55 (no cruzarlo). YJ: negro 72 y 148, «DEMIGOD FELLED» 216 (HUD del juego);
   la cinemática YJ 76-147 = EL +75,4.
 - KG: logo del canal 0-6; menús 448-456, 624-632, 992-1008, 1088, 1320-1328; MAPA 640-648, 824, 928, 1096-1104, 1336.
 - JM: destello blanco de un hechizo a 36; «INVADER VANQUISHED» 44.
 - PC: negro 26-29 y 66; fogonazo dorado 54-64.  PE: corte a 52 (otro plano fijo 54-86).  GH/BE/TA: logo «ELDEN RING» al final
   (GH 135+, BE 68+, TA 66+).  PA: menú a 50.  RS: rótulo de Stratek a 100-110, menú 330.  RG: menús 46, 68, 72.
 - AT: MAPA 6, 132-138, 732+; pantalla de carga 120; menús 636-648.  TM: carga 102-105.  SK: FLECHA BLANCA del youtuber a 60-62,
   MAPA 27 y 96-99, carga 81-84.  PW: RÓTULOS del youtuber 0-3 y 20-27, pantalla verde 256.
 - RY: carteles negros del canal (texto) 36-47, 60-71, 228-239, 360-371, 462-467, 586-588, 640-645, 655-660, 694-699.
 - GW: negro 0, 27-30, 177+.  NU: MAPA en cada cambio de zona (30, 66, 84, 114, 144, 168, 204, 228, 252, 294, 342, 390, 432),
   negro 427, menú 428-431; el monumento del monte Gelmir con su texto en pantalla 419-426.  MS: negro 8 y 288.
 - RN: negro 12 y 192-198.  RA: logo «ELDEN RING» 156+.  LR: MAPA 0, negro 126.  GN: «GREAT ENEMY FELLED» 72.
 - CONTADORES DE FPS: ninguno visto en estas fuentes (sí la HUD del juego en SS91/YJ/AT/TM/SK/PW/WD/GN).
 - DESCARTADOS: Soul Cat de Farum Azula (zcj3vSb5KyM, 0ume4hyz0cE: texto de anotaciones arriba), Lux85 (rótulos «MALIKETH
   BLACK BLADE» y juego en italiano), DanteMundus (imagen desaturada), opossum (Sinluz casi desnudo), WRETCH_Gaming (juego en
   francés), V Games (juego en ruso), Axiom (marca «AXIOM GAMES» abajo a la izquierda: era el único con la armadura de caballero
   de Gelmir puesta), PlaystationSaurus (imagen gris), Fextralife/Shirrako/Gamerpillar/VaatiVidya/IGN/PowerPyx/Zullie/cad5150.
 - SIN CLIP LIMPIO del casco de penacho rojo de los caballeros de Gelmir (p5_3, p3_7): se usa la Tumba del héroe de Gelmir
   (P28 2940-3350, donde está la armadura) y hace falta PEGATINA del casco y de la armadura (ER_Icon).
 - MISMO MOMENTO: EL/YJ/P30 graban la MISMA cinemática; este script pasa cada opción a «tiempo EL» (YJ −75,4, P30 −200) y avisa
   si dos frases distintas enseñan el mismo momento (< 9 s). También avisa si un url+segundo coincide (± 3 s) con lo que ya
   usaron er_sinluz_atrocidades y er_godfrey_atrocidades (plan_frases.json y busquedas.json).
 - «YOU DIED» (la virgen te mata): TM 97-98 (por eso TM 84 y no 90), y seguro en AT ~115-119 y SK ~79-80 (antes de la carga).
 - P29 tiene muchos avisos de objeto de ~1 s en las celdas (878, 920, 1004…) y P29 2150-2178 es la MESA REDONDA (no la mansión).
 - Repeticiones queridas dentro de una frase: p3b_8 (EL 58 → YJ 140 sigue la misma cinemática: Rykard dice la frase mientras
   suena s_rykard.mp3) y p1b_6 (YJ 213 muerte → YJ 222 la arena vacía donde suena «A serpent never dies»).

MOMENTOS EXACTOS comprobados en hoja (segundos de la fuente):
 - Rykard se revela (cara, ojo): EL 18-26 · la serpiente se alza 8-16 · Rykard y el Sinluz 28-32 · cabeza de la serpiente 34-48
   (la empuñadura asoma de la boca ~48) · Rykard con la Hoja blasfema ya fuera 56-66 («Join the Serpent King, as family» 61,3-66,0;
   «Together, we will devour the very gods!» 67,4-71,9).
 - Muerte de Rykard: YJ 212-216 («DEMIGOD FELLED» 216; la frase de la muerte suena 220-231 sobre la arena vacía) · P30 376-388.
 - Inquisidor Ghiza con su rueda: P29 290-322 · KG 1378-1408 (= wdGZrHkRv4M 22:58-23:28) · JM 22-42.
 - Fantasma del caballero de Gelmir (subtítulos «Someone, please, kill him…»): P29 398-491 · GH 18-132.
 - Alma estancada del camino (columna verde + su texto): P29 136-146.
 - Monumento del asalto a la Mansión con su inscripción: NU 419-426.
 - La virgen bajo la noria: noria TM 21-57 / AT 30-60 / SK 30-57; la virgen TM 60-99, AT 90-114, SK 57-78, PW 4-16;
   llegada a la Cámara subterránea de la inquisición: TM 108-123, AT 126-366 («LOST GRACE DISCOVERED» 366), SK 87-95;
   jefe doble de vírgenes raptoras: PW 148-208, AT 588-624.
 - Templo de Eiglay: combate con el Noble sacrodermo P29 3060-3300; el altar 3369-3378.  Hombres serpiente: P29 2084-2098,
   4018-4026 (látigo de fuego).  Vírgenes en la mansión: P29 1700-1720, 3642-3723, 4590-4620.
 - Retrato en la mansión: P29 4673-4676.  Celdas y jaulas colgantes (cámaras de tortura): P29 860-1010, 4380-4550.
 - Rya en Liurnia (sin el Sinluz): RY 0-24 y 72-216 · en la mansión RY 264-348, 516-576 · serpiente (Zorayas) RY 366-459 ·
   sentada entre velas («Kill me, please») RY 589-637 · su muerte RY 646-652.
 - Bernahl invade en Farum Azula: P46 5420-5580 (Ira de Gelmir: lava del suelo 5510-5513, 5528, 5537-5543).
 - Garra blasfema contra Maliketh (columna roja): WD 136, 160-164, 188-192, 204-212, 260.
 - Rogier en la Mesa Redonda: RG 0-74, RS 130-590.  Cadáver de Godwyn: GW 3-12, 96-104.  Ranni con la luna: RA 120-138.

TRAMOS DE AUDIO del juego (voces solo en INGLÉS; medidos con faster-whisper medium.en por palabra + envolvente RMS 250-3400 Hz;
cortados con ffmpeg: atrim + fundidos 0,06/0,12 s + silencio entre tramos + atempo si hace falta + loudnorm a −18 LUFS en
2 pasadas; MP3 192 kbps; cada corte vuelto a pasar por Whisper):
 (a) Rykard «Join the Serpent King, as family… Together, we will devour the very gods!»
     Fuente SIN MÚSICA: https://youtu.be/EQICJLV9i6g («Rykard - Boss Voice Only», solo la voz del juego):
       «Join … family» 17.95 → 22.30 s  +  «Together, … gods!» 23.18 → 28.10 s   (entre medias, silencio −55 dB).
     La frase entera a velocidad natural dura 9,3 s y NO cabe en post 7,5: dos versiones en sfx/:
       s_rykard.mp3          7,46 s  (los 2 tramos con 0,12 s entre ellos, atempo 1,265: tono intacto) −18,2 LUFS
                             Whisper: «Join the Serpent King, as family. Together, we will devour the very gods!» (con la frase
                             como prompt; sin prompt: «Join myself and King Aslamidee! Together we will devour the very core!»,
                             igual que sobre el audio original sin tocar).
       s_rykard_natural.mp3  9,46 s  (velocidad real, 0,15 s entre tramos) −18,3 LUFS → usar si se sube el post a ~9,6.
     Mismo audio con la música de la cinemática: https://youtu.be/eljrH9jvANE 61.3 → 66.1 + 67.3 → 72.0 (Join 61,34 · family
     65,78 · Together 67,38 · gods 71,84) · https://youtu.be/yjnnv3ib_t4 136.7 → 146.3.
 (b) Rya «Kill me, please.»  https://youtu.be/5IkIEt8YlW4  628.90 → 631.40 s  (Kill 629,06 · me 629,64 · please 630,62-631,06;
     silencio −80 dB alrededor; sin música).
       s_rya.mp3        2,54 s, −18,2 LUFS. Whisper: «Kill me, please.»
       s_rya_largo.mp3  6,29 s (+ 0,3 s + «Free me from this accursed frame.» 636.50 → 639.95), −17,9 LUFS. Whisper: «Kill me.
                        Please. Free me from this accursed frame.» → NO cabe en post 4,5 (usar si se sube a ~6,5).
 (c) Rykard al morir «No one will hold me captive. A serpent never dies.»
     Fuente SIN MÚSICA: https://youtu.be/EQICJLV9i6g  «No one will hold me captive.» 36.55 → 41.80 s  +  «A serpent never dies.»
     45.05 → 48.98 s (No 36,66 · captive 40,88-41,52 · A 45,20 · dies 47,96-48,80).
       s_serpiente.mp3          6,43 s (0,1 s entre tramos, atempo 1,45: tono intacto, se nota más rápido) −18,5 LUFS.
                                Whisper: «No one will hold me captive. A serpent never dies.» (con prompt; sin prompt: «No one
                                will open captive. I serve and never die.», igual que sobre el original).
       s_serpiente_natural.mp3  9,70 s (velocidad real, 0,2 s entre tramos) −18,4 LUFS → usar si se sube el post a ~9,8.
     Con la música del combate: https://youtu.be/yjnnv3ib_t4 ~219.9 → 224.4 + 227.35 → 231.45 · https://youtu.be/bVWauAYPe60
     ~384-397 (música alta: Whisper no la entiende).
"""
import json
import os

F = {  # alias: (id, nota)
    "P28": ("EZvmZR4s3b8", "SS91 Part 28: monte Gelmir (laderas, campamentos en ruinas, vírgenes raptoras, Tumba del héroe de Gelmir)"),
    "P29": ("YS1P-_MROO0", "SS91 Part 29: Mansión del Volcán (Tanith, Ghiza, fantasma, celdas, ciudad de los penados, Templo de Eiglay)"),
    "P30": ("bVWauAYPe60", "SS91 Part 30: Serpiente devoradioses y Rykard (cinem. 200-276, muerte 376-388, Tanith y Bernahl después)"),
    "P12": ("kqvqNB5JoA0", "SS91 Part 12: Academia de Raya Lucaria"),
    "P46": ("9nmqal7jH9A", "SS91 Part 46: Farum Azula, la ciudad en ruinas (Bernahl invade 5420-5580)"),
    "EL": ("eljrH9jvANE", "pgp 4K: cinemática de la fase 2 de Rykard (sin HUD; fogonazo 50-55)"),
    "YJ": ("yjnnv3ib_t4", "VynPlays 4K: Serpiente y Rykard (combate, cinemática 76-147, muerte 212-231)"),
    "KG": ("wdGZrHkRv4M", "Kelvyn Acevedo 4K: Mansión del Volcán (imagen lavada; Tanith 190-240, Rya 550-616, Ghiza 1378-1414)"),
    "JM": ("d7Lg5R8Np-4", "Jaemekon: el inquisidor Ghiza invade la Mansión del Volcán"),
    "GD": ("kZ4pC3lkIKU", "Soul Cat 720p: Gideon Ofnir habla de Rykard (plano fijo en su despacho de la Mesa Redonda)"),
    "GK": ("fYz6wYgdZfw", "Kevin B: Gideon Ofnir sobre Rykard (plano fijo, Mesa Redonda)"),
    "PE": ("0U52CsjKPrY", "Stratek: Parches antes y después del «atajo» de la virgen (plano fijo; subtítulos del juego)"),
    "PC": ("onpson1sZsI", "Zero Manga Hunter: cinemática de Parches empujándote por el precipicio del monte Gelmir"),
    "PA": ("ijNdEQdToEs", "SBG: Parches tras la muerte de Rykard (subtítulos del juego)"),
    "GH": ("d7shRsbbjvI", "Terry Goodwin 4K: el fantasma del caballero de Gelmir pide matar a Rykard (subtítulos del juego)"),
    "BE": ("Ifw3P9rXaRY", "Terry Goodwin: Bernahl tras la muerte de Rykard (subtítulos del juego)"),
    "TA": ("ClYjAC9k01g", "Terry Goodwin: Tanith tras la muerte de Rykard (subtítulos del juego)"),
    "AT": ("TxnoanwFw4g", "Aethersong: la virgen raptora de Raya Lucaria, la Cámara subterránea de la inquisición y el jefe doble"),
    "TM": ("lXRPwD_6s2w", "IAmToastMan: la noria de Raya Lucaria, la virgen y el traslado a la Mansión del Volcán"),
    "SK": ("yWDl221XY8U", "ShyKatana: la noria de Raya Lucaria y la virgen (flecha del youtuber a 60-62)"),
    "PW": ("iOk8MMMWPo4", "PANxWAR: la virgen de Raya Lucaria y el jefe doble de vírgenes raptoras (rótulos 0-3 y 20-27)"),
    "RY": ("5IkIEt8YlW4", "Sunless_Solaire: todas las escenas de Rya/Zorayas sin el Sinluz en pantalla (carteles negros entre escenas)"),
    "RG": ("qGULKKS0C0A", "Indyrael: Rogier en la Mesa Redonda (plano fijo)"),
    "RS": ("EbTt4y1bEVc", "Stratek: Rogier en la Mesa Redonda (plano fijo; rótulo a 100-110)"),
    "GW": ("vhmkUYSyMfE", "BonfireVN: el cadáver de Godwyn (cámara libre, sin HUD)"),
    "WD": ("YP2xEGbkkR8", "WilliamDoe: Maliketh, la Hoja Negra, con la Garra blasfema (columna roja)"),
    "NU": ("VhY4e2TbWxI", "Nutler: monumentos con espada; el del asalto a la Mansión del Volcán 419-426"),
    "MS": ("X8lPYwvHCv4", "Veloketh: Messmer el Empalador, cinemática y combate sin HUD"),
    "RN": ("vpBRYiQ5bio", "GameOnDude 4K: Rennala, reina de la Luna llena (cinemáticas sin HUD)"),
    "RA": ("W4K4iaLfcug", "4KGameScape: final de Ranni (Ranni y la luna)"),
    "LR": ("8D_h_1cNz28", "Leomega sin HUD: Radahn (imagen lavada)"),
    "GN": ("JLBgrzC55Ss", "Part Time Gamer 4K: Noble sacrodermo en el Templo de Eiglay"),
}

P = {
    "intro_0": "EL 18, P29 40, P28 5196",
    "intro_1": "YJ 16, P30 140",
    "intro_2": "P29 880, P28 356, P29 70",
    "intro_3": "WD 156, WD 140",
    "intro_4": "P28 24, P29 60",
    "intro_5": "P28 5640, P28 120",
    "intro_6": "P29 168, P28 228",
    "intro_7": "MS 48, MS 40",
    "intro_8": "MS 104, MS 176",
    "intro_9": "MS 300, MS 72",
    "p5_0": "P29 862, P29 4440",
    "p5_1": "GD 2, GK 2",
    "p5_2": "GD 20, P29 3850",
    "p5_3": "P28 3084, P28 3168, P28 3000",
    "p5_4": "KG 200, P29 186, P29 270",
    "p5_5": "P29 1050, AT 360, P29 1012",
    "p5_6": "PW 188, P29 4460",
    "p5b_0": "P29 960, P29 4480",
    "p5b_1": "P29 936, P29 3800",
    "p5b_2": "P29 776, P29 4230",
    "p5b_3": "P29 291, KG 1378, JM 22",
    "p5b_4": "P29 313, KG 1401",
    "p5b_5": "P29 302, KG 1390",
    "p5b_6": "P29 4292, P29 4400",
    "p5b_7": "P29 4668, P29 1716",
    "p4_0": "PW 6, P29 1700",
    "p4_1": "P12 76, PE 10",
    "p4_2": "TM 72, P29 3712",
    "p4_3": "TM 30, AT 36, SK 36",
    "p4_4": "AT 96, SK 63, TM 84",
    "p4_5": "TM 108, AT 150, SK 106",
    "p4_6": "PW 172, AT 596",
    "p4b_0": "P29 3642, PW 200",
    "p4b_1": "P29 3696, AT 106",
    "p4b_2": "P28 284, P29 4604, P28 396",
    "p4b_3": "AT 200, SK 120",
    "p4b_4": "PE 60, AT 230",
    "p4b_5": "PC 30, PC 2",
    "p4b_6": "PC 40, P28 1384",
    "p4b_7": "P28 48, P28 5180",
    "p4b_8": "TM 60, P29 4616",
    "p3_0": "P28 168, P29 82",
    "p3_1": "GK 18, P28 132",
    "p3_2": "NU 417, P28 5545",
    "p3_3": "P28 5620, P29 50",
    "p3_4": "P30 110, YJ 40",
    "p3_5": "EL 28, P30 172",
    "p3_6": "P29 136, P29 126",
    "p3_7": "P28 3180, P28 3204",
    "p3b_0": "P30 150, P30 120",
    "p3b_1": "P30 44, P29 4270",
    "p3b_2": "P29 398, GH 20",
    "p3b_3": "GH 50, P29 428",
    "p3b_4": "P29 464, GH 90",
    "p3b_5": "P29 491, GH 2",
    "p3b_6": "EL 40, YJ 116",
    "p3b_7": "P30 452, P30 466",
    "p3b_8": "EL 58, YJ 140",
    "p3c_0": "P29 1330, P28 5250",
    "p3c_1": "TA 10, P30 520",
    "p2_0": "RY 366, P29 2096",
    "p2_1": "P30 284, YJ 4",
    "p2_2": "P29 2082, P29 4016",
    "p2_3": "EL 8, P30 80",
    "p2_4": "P30 334, YJ 156",
    "p2_5": "P28 4536, P29 2310",
    "p2_6": "P29 3060, P29 3318",
    "p2_7": "P29 3100, GN 12, P29 3200",
    "p2_8": "P29 3369, P29 3384",
    "p2b_0": "RY 0, RY 88",
    "p2b_1": "RY 132, RY 180",
    "p2b_2": "RY 417, KG 560",
    "p2b_3": "RY 300, RY 526",
    "p2b_4": "RY 390, RY 548",
    "p2b_5": "RY 616, RY 440",
    "p2c_0": "RY 647, RY 598",
    "p2c_1": "RY 750, RY 700",
    "p2c_2": "P29 4420, P29 896",
    "p2c_3": "P46 5506, P28 4552",
    "subs_0": "P28 5208, P28 36",
    "subs_1": "YJ 168, P30 346",
    "subs_2": "P28 3744, P12 100",
    "subs_3": "P28 5140, P28 3732",
    "subs_4": "P28 5520, P29 1300",
    "subs_5": "YJ 180, P28 5300",
    "p1_0": "WD 128, P46 4560",
    "p1_1": "P46 400, P46 4620",
    "p1_2": "P46 5450, P46 5470",
    "p1_3": "WD 200, WD 214",
    "p1_4": "RA 18, WD 116",
    "p1_5": "RA 120, RA 102",
    "p1_6": "RG 10, RS 200",
    "p1_7": "GW 5, GW 96",
    "p1b_0": "P30 308, YJ 192",
    "p1b_1": "WD 182, WD 236",
    "p1b_2": "YJ 204, P30 184",
    "p1b_3": "P30 320, YJ 60",
    "p1b_4": "P30 390, YJ 232",
    "p1b_5": "BE 4, P30 576, BE 30",
    "p1b_6": "YJ 213, YJ 222",
    "p1c_0": "WD 252, WD 264",
    "p1c_1": "PA 10, PA 30",
    "p1c_2": "P29 1270, P29 2440",
    "p1c_3": "KG 216, P29 2320",
    "cierre_0": "P29 4510, PW 156, GW 120",
    "cierre_1": "TA 40, P30 508",
    "cierre_2": "P30 596, BE 50",
    "cierre_3": "P30 404, YJ 28",
    "cierre_4": "RN 278, LR 108, RA 132",
    "cierre_5": "RN 60, MS 248, LR 280",
    "cierre_6": "P28 3756, P28 60",
    "cierre_7": "P28 492, SK 72",
}

NOTAS = {  # nota específica del momento (se añade a la de la fuente)
    "intro_0": "Rykard se revela en la cinemática (cara y ojo)",
    "intro_3": "Garra blasfema contra Maliketh (columna roja a +4 s)",
    "p5_1": "Gideon en su despacho (plano fijo)",
    "p5_3": "Tumba del héroe de Gelmir, donde está la armadura: PEGATINA del casco de penacho rojo",
    "p3_7": "Tumba del héroe de Gelmir: PEGATINA de la Armadura de caballero de Gelmir",
    "p5_5": "ciudad de los penados / Cámara subterránea de la inquisición",
    "p5b_3": "el inquisidor Ghiza (rojo) invade con su rueda",
    "p5b_4": "la Rueda de Ghiza girando",
    "p5b_5": "Ghiza de cerca (máscara de vendas y túnica)",
    "p5b_7": "retrato en la mansión (aviso de objeto encima) / virgen raptora",
    "p4_3": "la gran noria de la Academia",
    "p4_4": "la virgen raptora atrapa al Sinluz",
    "p4_5": "llegada a la Cámara subterránea de la inquisición (río de lava, «Volcano Manor»)",
    "p4_6": "jefe doble de vírgenes raptoras",
    "p4b_5": "Parches te tira por el precipicio",
    "p3_2": "monumento del asalto con su inscripción a +2 s",
    "p3_6": "alma estancada en el camino de la mansión (columna verde + su texto)",
    "p3b_1": "la lanza Cazador de serpientes clavada en el montón de cadáveres (+3 s)",
    "p3b_2": "el fantasma del caballero de Gelmir: «Someone, please, kill him…»",
    "p3b_4": "el fantasma: «Whatever that thing is, it is no longer Praetor Rykard»",
    "p3b_6": "la serpiente abre la boca y asoma la Hoja blasfema (antes del fogonazo de 50 s)",
    "p3b_8": "Rykard con la Hoja blasfema dice «Join the Serpent King, as family… devour the very gods»",
    "p2_2": "hombres serpiente (látigo de fuego en P29 4020)",
    "p2_7": "Noble sacrodermo en el Templo de Eiglay",
    "p2_8": "altar del Templo de Eiglay",
    "p2b_2": "Rya en forma de serpiente (Zorayas)",
    "p2b_5": "Rya sentada entre velas: «Kill me, please»",
    "p2c_0": "muerte de Rya",
    "p2c_3": "Bernahl lanza la Ira de Gelmir (lava del suelo)",
    "p1_2": "Bernahl invade en Farum Azula",
    "p1_6": "Rogier en la Mesa Redonda",
    "p1_7": "el cadáver de Godwyn",
    "p1b_5": "Bernahl: «So, you killed Rykard?… Even he was prepared to meet a wretched end»",
    "p1b_6": "muerte de Rykard; su frase suena sobre la arena vacía (YJ 220-231)",
    "p1c_1": "Parches: «daddy ambition… lady blasphemy»",
    "cierre_1": "Tanith: «Our lord is immortal, and will one day rise again, stronger»",
}

MIN_SEP = 9
CINE = {"EL": [(0, 76, 0)], "YJ": [(76, 148, -75.4)], "P30": [(200, 277, -200)]}
DUR = {"GD": 36, "GK": 34, "EL": 76, "JM": 53, "PA": 58, "TA": 74, "BE": 75, "PC": 71, "RG": 74, "PE": 87, "GH": 140,
       "GW": 184, "NU": 503, "RA": 162, "YJ": 241, "TM": 126, "SK": 147, "PW": 261, "AT": 745, "RY": 776}


def opciones():
    out = {}
    for k, v in P.items():
        ops = []
        for t in v.split(","):
            a, s = t.split()
            vid, nota = F[a]
            n = nota + (" · " + NOTAS[k] if k in NOTAS else "")
            ops.append({"url": f"https://youtu.be/{vid}", "desde": int(s), "nota": n})
        out[k] = ops
    return out


def usados_antes():
    """url+segundo que ya usaron los videos del Sinluz y de Godfrey."""
    u = []
    for f in ("../er_sinluz_atrocidades/plan_frases.json", "../er_sinluz_atrocidades/busquedas.json",
              "../er_godfrey_atrocidades/plan_frases.json", "../er_godfrey_atrocidades/busquedas.json"):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        pila = [d]
        while pila:
            x = pila.pop()
            if isinstance(x, dict):
                if x.get("url") and x.get("desde") is not None:
                    u.append((x["url"][-11:], float(x["desde"]), f.split("/")[1]))
                pila.extend(x.values())
            elif isinstance(x, list):
                pila.extend(x)
    return u


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    out = opciones()
    json.dump(out, open("plan_frases.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    usos = [(o["url"][-11:], o["desde"], k) for k, ops in out.items() for o in ops]
    for i, a in enumerate(usos):
        for b in usos[i + 1:]:
            if a[0] == b[0] and a[2] != b[2] and abs(a[1] - b[1]) < MIN_SEP:
                print("  MISMO PLANO:", a, b)
    eq = sorted((s_ + off, k, a) for k, v in P.items() for a, s_ in ((t.split()[0], int(t.split()[1])) for t in v.split(","))
                for a0, b0, off in CINE.get(a, []) if a0 <= s_ < b0)
    for i, x in enumerate(eq):
        for y in eq[i + 1:]:
            if y[0] - x[0] >= MIN_SEP:
                break
            if x[1] != y[1]:
                print("  MISMA CINEMÁTICA:", x, y)
    antes = usados_antes()
    for vid, s, k in usos:
        for vid2, s2, f in antes:
            if vid == vid2 and abs(s - s2) <= 3:
                print("  YA USADO EN", f, ":", k, vid, s, "~", s2)
    ids = {v[0]: a for a, v in F.items()}
    for vid, s, k in usos:
        d = DUR.get(ids[vid])
        if d and s + 8.6 > d:
            print("  PASA DEL FINAL:", k, ids[vid], s, "dur", d)
    import guion
    claves = [f"{e['id']}_{i}" for e in guion.ESCENAS for i in range(len(e["frases"]))]
    print(len(out), "frases con plan; faltan:", [c for c in claves if c not in out], "sobran:", [c for c in out if c not in claves])
