# -*- coding: utf-8 -*-
"""Plan de clips POR FRASE (24-nov-2026) de «Las 5 peores atrocidades de Messmer QUE IGNORASTE», hecho mirando hojas de
contacto a 240p de cada fuente (E:\\FabricaAnimaciones\\_tmp_hojas_messmer\\h\\*.jpg: una hoja por fuente o por tramo del
longplay + hojas finas «f*» de 1 s de los momentos exactos; v\\v_NN.jpg = comprobación final de TODAS las opciones, 3 cuadros
por clip a +0,5 / +4,3 / +8,1 s del corte real de yt-dlp). Escribe plan_frases.json (lo lee asignar_clips.py).
    python _plan.py
Fuentes limpias: SourceSpy91 longplay 4K sin comentarios (L, -7P1VNhon6E: HUD normal, subtítulos del juego en los diálogos;
CORTE PROBADO pasado 70 000 s: 74 900 y 75 200 a 360p y 1080p bajan bien) y su «Part 11» (P11 = el MISMO metraje que L
71 529-75 330: el Almacén de especímenes y Messmer), «Part 12» (P12: Rauh, el 2.º León y Romina) y «Part 13» (P13: la Yesca
quema el árbol sellado y aparece Enir-Ilim); Stride (ST, Messmer SIN HUD ni subtítulos: cinemáticas, combate y muerte);
Veloketh (MS, Messmer sin HUD; VL, el León Danzante sin HUD); Sword Saint Gaming (SS, las 2 cinemáticas de Messmer con
subtítulos del juego); Dan Allen Gaming (DA, cinemática del León + combate); tráiler oficial BANDAI NAMCO Europe (TR, franjas
negras de panorámico en todo el tráiler); Stratek (SG Anciana + cinemática del canto, SC el Cornamentado, SQ Queelign: planos
fijos con subtítulos del juego; máx. 1-2 por puesto); Soul Cat (SCG: el Sinluz CON la Cabeza de bestia divina ante la Anciana;
SQ2: Queelign invade Belurat, 720p algo lavado); Cezar Nicolae (CN, Queelign en Belurat); Lorebringer (LB, el Cornamentado
tras matar a Messmer); SpookyFairy (SF, Messmer con el Cornamentado invocado); Arbuckle (AR Andreas / HR Huw: catacumbas);
XsCity Gaming (XF, Caballero de Fuego y la Lluvia de fuego); 30 Something Gaming (SR, Llanura de las Tumbas y Ruinas calcinadas).
Ojo (marcas, menús, mapas, rótulos; segundos de la fuente):
 - L: rótulos de zona del juego 20475 «Scadu Altus», 20833 «Church of the Crusade», 27028 «Fort of Reprimand», 27754, 27952,
   41846 «Shadow Keep, Church District», 42608, 62290 «Scadu Altus», 62405 y 63777/63819 «Shadow Keep», 75315; «LOST GRACE
   DISCOVERED» 9605, 26686, 42632, 44332, 62125; «INVADER VANQUISHED» ~9837; «RECUSANT VANQUISHED» 20877-20880; «BLOODY FINGER
   VANQUISHED» 63801; «DEMIGOD FELLED» 75150; menús 20583-20595, 20639-20643, 20899-20903, 26698-26710, 26968, 27184-27202,
   27454-27478, 27862-27868, 44305-44317, 62135-62140, 62255-62265, 63831, 63972-64002, 74787-74805, 74829-74847, 75189-75204,
   75505-75511, 1304-1392; MAPA 256, 1248, 1408, 20687, 20735-20739, 20939, 27100-27112, 27736-27742, 42638-42644,
   44357-44364, 62150-62155, 62230, 62270-62275, 74811-74814, 75306; negro 800, 1256, 20675, 28042, 41834, 44341, 62280,
   64059-64062, 74868, 75036-75039, 75219, 75303, 75499; diálogos con subtítulos del juego: Leda 20495-20551 y 20603-20635
   (la línea «Queen Marika commanded Sir Messmer to purge the tower folk» ~20530), la Anciana (1.ª visita) ~11301-11397,
   Cornamentado tras Messmer 75231-75300, otros NPC 27874-27898, 42326-42398. Avisos de objeto de ~1 s por todas partes
   (20563, 20611, 20807-20811, 26944, 27076, 27090-27094, 27592, 27604, 28168, 38936-38941 = la ceniza de Huw en el altar,
   35050-35060, 41909-41912, 63780-63782, 75385, 75439, 75565-75567; en Belurat 9301-9305, 9909-9911, 11555-11565).
   Visto en la COMPROBACIÓN (v_NN) y por eso cambiado: «LOST GRACE DISCOVERED» a 27958 (el corte cae en el fotograma clave
   anterior), «ENEMY FELLED» ~28158, menú ~26748, rótulo «Belurat, Tower Settlement» 9155-9158, 11421 y 12926.
 - L Belurat (sección 8949-13160): Belurat por fuera 8949-8965 · puertas talladas 8973-8981, 12406-12414, 12686-12694 ·
   plaza en ruinas 9157-9173 · fuente 9301 · Queelign invade 9800-9832 («INVADER VANQUISHED» 9833, menús 9839-9853) ·
   tejados 9957-10125, 12806-12838 · panorámica de Belurat arrasada 12358-12374 · escalinata 12718-12766 · MAPA 9293, 9693,
   12910, 13110, 13126-13134 · negro 9349, 12382, 12418, 12918 · menús 9845-9861, 12294-12318, 12782-12798, 12950, 13054-13086.
 - P11 (= L + 71 529): negro 0-10, 3338-3340, 3504-3510; menús 940, 1390, 1570-1580, 1820-1830, 2140, 2660-2670, 3260-3270,
   3300-3310, 3660-3670, 3690; MAPA 540, 1940, 2310, 2680, 3280; rótulo «Specimen Storehouse» 470, 1140, 2320, 2520, 2860;
   «DEMIGOD FELLED» 3618-3620 (+ aviso 3622-3624); subtítulos pequeños del juego en las cinemáticas; diálogos 610-660,
   2400-2510, 3700-3770.
 - P12: negro 0; aviso 140, 308-312; «ENEMY FELLED» 304; MAPA 328-332; oscuro 336-340; «Ancient Ruins of Rauh» 344;
   «LEGEND FELLED» 496; «LOST GRACE DISCOVERED» 516.   P13: negro 0, 36-40, 108, 140-144; «Enir-Ilim» 200.
 - TR: negro 0-17, 25, 48-53, 87-89, 108-115, 133, 140; logo/fecha/precompra 160+ (TR 99 ya cae en el negro de 108: TR 97).
 - ST: negro 0, 75, 231-234; «DEMIGOD FELLED» 487-489; menú 490+.   SS: negro 0, 75, 120-123; tarjeta final del youtuber 189+.
   MS: negro 12 (y 8, 288 según el plan de Rykard).   VL: «LEGEND FELLED» 321-333.   DA: HUD 0-6 y 84+.
 - SG: subtítulos del juego en todo; cinemática del canto 174-242.  SC: «HOST VANQUISHED» 246, «DEMIGOD FELLED» 264.
   SF: rótulo «Specimen Storehouse» 0, «DEMIGOD FELLED» 189.  SQ: «INVADER VANQUISHED» 18, rótulo 42, plano fijo 44-122.
   SQ2: MAPA 9-15 y 198+, «INVADER VANQUISHED» 186.  CN: «INVADER VANQUISHED» 93, menú 99.  SCG: menú 0, aviso 123.
   P12: aviso de objeto ~84 (por eso P12 92/160 y no 84).
 - AR/HR (Arbuckle): tarjeta de SUSCRIPCIÓN del youtuber 0-6, MAPA 9-15, «Leave a Like» AR 105-108 / HR 99-102.
   XF: aviso de objeto 80-106, MAPA 108+.  SR: palacio de Mohg 0-160 (menús 12-30, mapas 36-60), rótulo «Gravesite Plain» 168,
   menús 198 y 282-288, tutoriales 648-654 y 708-720, aviso 660, MAPA 732.
 - CONTADORES DE FPS / MARCAS: ninguna en las fuentes usadas. DESCARTADOS: burgerarcade (jlNOo6j6enY, io8vQP4x6Ts,
   X6kN2zoP4a0: ICONO naranja fijo abajo a la derecha = marca de agua), pgp (logo), Shirrako, Fextralife/IGN/ConCon/PowerPyx/
   Zullie/cad5150/NeoJetty, KilledTheBoss (hUkK5loZso4: imagen lavada), Smoothy (EWx5ndStb1I: oscurísimo), Ape Knight
   (0xiPUq1MEV8: rótulo «LOL that's embarrassing» a 75 y el jugador con una caja en la cabeza), BonfireVN «sin la capa»
   (lV2fzuneIDI: MOD que le quita la capa al León), Stratek 6m4rlHbjecA (el Cornamentado contra Messmer: 26 s con «DEMIGOD
   FELLED» a 9 s, no da 9 s limpios), KMB GAMING / Mark Chaivasin / babazolo / Brunoborne / ClipPlayTru (no hicieron falta).
 - MISMO METRAJE: P11 = L 71 529-75 330 (el script pasa P11 a tiempo L). MISMA CINEMÁTICA de Messmer: ST/SS/MS/L/P11 graban
   las mismas dos cinemáticas; el script las pasa a «tiempo P11» (entrada 3338-3416, fase 2 3460-3574) y avisa si dos frases
   distintas enseñan el mismo momento (< 9 s). También avisa si un url+segundo coincide (± 3 s) con lo que ya usaron los
   demás videos del canal (videos/er_*/plan_frases.json y busquedas.json; MS ya lo usó Rykard a 40/48/72/104/176/248/300).
 - SIN CLIP LIMPIO (hace falta PEGATINA o pantalla): los iconos y descripciones de objeto (Insignia de cruzada, Tornado de bestia
   divina, Cabeza de bestia divina, Potaje de escorpión, Mayal de serpiente, Túnica de cordón trenzado, Bendición y Runa de
   Márika, Yesca, Recuerdo del Empalador, Casco/Armadura de Caballero de Fuego y de Caballero Negro, Capucha de Salza, Lluvia de
   fuego, cenizas de Andreas, Huw, Hilde, Queelign y de soldado de Messmer, Grasa de fuego, Botella de perfume ígneo, Escudo con
   blasón de serpiente); los cuerpos EMPALADOS solo existen en el tráiler (TR 74-78 la criatura atravesada, TR 90-97 siluetas
   en postes ardiendo): en el juego no encontré ni uno (ni ante la Fortaleza sombría ni en el Fuerte de la reprimenda); el
   ataúd de Andreas y el alma estancada de las Ruinas calcinadas tampoco (se usan las catacumbas y las ruinas calcinadas).

MOMENTOS EXACTOS comprobados en hoja (segundos de la fuente):
 - Messmer, cinemática de entrada: P11 3342-3354 te mira desde lo alto (= L 74871-74883) · 3356-3360 de pie · 3362-3370 ojo de
   la serpiente · 3372-3378 serpiente alada · 3384-3388 casco con alas · 3390-3396 la mano y la llama · 3398-3406 la llama en la
   arena · 3408-3414 la cara con la llama («In the embrace of Messmer's flame») · combate 3416. Igual en ST/SS +3340 (ST 3-73,
   SS 3-73) y MS +3325 (MS 18-88).
 - Fase 2: P11 3462-3472 de pie · 3474-3484 se tapa la cara (≈ «lloró») · 3486-3494 · 3496 la mano al ojo · 3498-3502 EL OJO CON
   EL SELLO DE GRACIA · 3504-3510 negro · 3512-3530 la mano arranca el sello · 3534-3546 sala · 3548-3556 la serpiente de fuego
   brota · 3558-3564 la cara rodeada de serpientes · 3566-3572 las fauces. ST = P11 −3276 (ST 186-297; ojo ST 225-228; negro
   231-234), SS = P11 −3385 (SS 78-188), L = P11 +71 529.
 - Muerte de Messmer: ST 476-483 se arrodilla y se deshace («Mother… Marika…»), destello 484, «DEMIGOD FELLED» 487 · P11
   3604-3614 (subtítulos del juego), destello 3615, «DEMIGOD FELLED» 3618 (= L 75133-75150).
 - El Cornamentado tras la muerte: L 75231-75300 (= P11 3702-3771, subtítulos) · LB 8-71 · «oh madre, oh amadísima esposa e hijo»
   SC 339-366 (primer plano).  Con Messmer en la arena: SF 33-186 (invocado).  En la llanura: SC 0-190.
 - La Anciana cornamentada: SG 15-96, 120-171, 243-381 (subtítulos) · L 11302-11392 (1.ª visita: «another of Messmer's peons»,
   «our lands were by thy kind set aflame») y 12958-13046 (tras el León: «Have my son accompany thee to war» ~13016, «Take
   vengeance upon Messmer and his lot» ~13033) · con la
   Cabeza de bestia divina puesta: SCG 33-141.  Cinemática del León con el canto: DA 9-84 (cabeza 27-42, se alza 66-84),
   SG 174-242 (dos versiones: cabeza 180-189 y 216-222), VL 0-27, y en el longplay L 12419-12434 el teatro, 12436-12455 la
   cabeza (el canto), 12457-12475 se alza, 12476-12493 de pie; combate 12496+ (negro 12418). DA = L −12409.
 - El León Danzante: VL 27-318 (tornado 183-195, rayos 198/228/258, hielo 150/207/270-282, muere 318, «LEGEND FELLED» 321),
   DA 84-189, P12 172-304 (el 2.º León, en Rauh).
 - Queelign: Belurat CN 39-90, SQ2 96-185, L 9800-9832; Iglesia de la Cruzada L 20839 aparece, 20841-20846 su frase
   (subtítulos), 20847-20876 combate, 20877 «RECUSANT VANQUISHED»; SQ 2-16 te mata («Queen Marika, behold…»), 22-40.
 - Leda: L 20495-20551 (la línea de la purga ~20530) y con el Cornamentado 20603-20635.
 - Caballeros de Fuego (rojos): L 44425-44445, 44496-44549, 42452-42464, 42518-42530, 42170 · P11 1100-1130 (látigo de fuego
   1120), 1480-1500, 1690-1710, 2090-2120, 3066-3090 (espadón en llamas = L 74595-74619) · el del PUENTE a Rauh (Lluvia de fuego,
   columnas rojas 75400 y 75413): L 75394-75423 · XF 8-78.
 - Caballeros Negros: altar de Huw L 38911-38935 (la ceniza 38936) · L 38896-38905 · Catacumbas de Grieta Neblinosa L 35012-35049.
 - Almacén de especímenes: P11 50-120, 960-1080 (montaña de cuerpos 1000-1020), 2400-2610. Rauh: P12 4-168, L 75523-75703.
   Yesca: P13 44-80 el árbol sellado arde, 84-136 Enir-Ilim. Romina: P12 368-496.
 - Tráiler: jaulas ardiendo 54-58 · soldados con lanzas 62-66 · Messmer sobre la pira 67-73 · CRIATURA ATRAVESADA por lanzas
   74-78 · cara/serpiente 79-86 · siluetas empaladas en postes 90-97 · ruinas y árbol 99-107.
 - Fortaleza sombría por fuera: L 62295-62304 (desde el Altiplano) · Distrito de la iglesia inundado L 42800-42854.
 - Llanura de las Tumbas: L 96-128 (llegada), tumbas 144-216, 736-1016, 1424-1512 · Ruinas calcinadas (ceniza): SR 516-618,
   cementerio SR 624-690.  Fuerte de la reprimenda: L 26680-28400 (patíbulos 27064-27094, celdas 27424, 27598-27616).
"""
import json
import os

F = {  # alias: (id, nota)
    "L": ("-7P1VNhon6E", "SourceSpy91 longplay 4K del DLC (sin comentarios, HUD normal)"),
    "P11": ("8JuyynvvTqw", "SS91 Part 11: Almacén de especímenes y Messmer (= longplay 71 529-75 330)"),
    "P12": ("wroVoQBemN4", "SS91 Part 12: Antiguas ruinas de Rauh, el 2.º León y Romina"),
    "P13": ("ZlKrbp3j1hQ", "SS91 Part 13: la Yesca quema el árbol sellado (44-80) y Enir-Ilim"),
    "ST": ("PoTk3y9244M", "Stride 4K: Messmer SIN HUD (cinemáticas 3-73 y 186-297, combate, muerte 476-483)"),
    "MS": ("X8lPYwvHCv4", "Veloketh: Messmer sin HUD (cinemática 18-88, combate)"),
    "SS": ("8alB4qSX3C0", "Sword Saint Gaming 4K: las 2 cinemáticas de Messmer (subtítulos del juego; tarjeta final 189+)"),
    "TR": ("6uT8wGtB3yQ", "tráiler oficial BANDAI NAMCO Europe (franjas negras de panorámico)"),
    "VL": ("C9F2U1-Ae0w", "Veloketh: el León Danzante sin HUD (cinemática 0-27, muere 318)"),
    "DA": ("xlxpsNvkRnY", "Dan Allen Gaming 4K: cinemática del León (9-84) y combate"),
    "SG": ("p3JX1YVDYc0", "Stratek: la Anciana cornamentada (plano fijo, subtítulos) y la cinemática del canto 174-242"),
    "SCG": ("92r3FQACq3g", "Soul Cat: el Sinluz con la Cabeza de bestia divina ante la Anciana (oscuro)"),
    "SC": ("INoq5UMCr-o", "Stratek: el Cornamentado (plano fijo, subtítulos)"),
    "LB": ("Sfo5u4vWJ-4", "Lorebringer: el Cornamentado tras matar a Messmer (plano fijo, subtítulos)"),
    "SF": ("bAmMwfmzo_Q", "SpookyFairy: Messmer con el Cornamentado invocado"),
    "SQ": ("3wQCfgdGfec", "Stratek: Queelign («Queen Marika, behold…» 3-11)"),
    "SQ2": ("LtYFKnkuFLI", "Soul Cat 720p: Belurat y Queelign invade (96-185)"),
    "CN": ("p8QPYrECmo4", "Cezar Nicolae: Queelign invade Belurat (39-90)"),
    "AR": ("KtmNwqWoK1o", "Arbuckle: Catacumbas de Grieta Neblinosa (Andreas)"),
    "HR": ("-nuXyX89JZc", "Arbuckle: Catacumbas del río Escorpión (Huw)"),
    "XF": ("be0ss-h9NhQ", "XsCity Gaming: un Caballero de Fuego y su Lluvia de fuego"),
    "SR": ("kaXob8M_4Yk", "30 Something Gaming: Llanura de las Tumbas y Ruinas calcinadas"),
}

P = {
    "intro_0": "L 62298, ST 102, ST 315",
    "intro_1": "P11 3343, ST 56, MS 82",
    "introb_0": "P11 3420, ST 84",
    "introb_1": "TR 54, SR 516, L 12358",
    "introb_2": "L 44425, VL 210, SG 15",
    "introb_3": "L 96, ST 126, P11 3430",
    "introb_4": "ST 144, MS 120, P11 3440",
    "introb_5": "ST 159, SF 60",
    "introb_6": "SQ2 132, L 28090",
    "p5_0": "L 35686, L 152",
    "p5_1": "L 44496, P11 1108",
    "p5_2": "P11 1480, P11 2100, L 42452",
    "p5_3": "P11 1118, P11 3068",
    "p5_4": "ST 273, ST 237, ST 324",
    "p5_5": "L 28102, L 62340",
    "p5_6": "ST 219, L 38896",
    "p5b_0": "L 38911, L 35012",
    "p5b_1": "L 35560, AR 30",
    "p5b_2": "L 38943, HR 39",
    "p5b_3": "L 38922, ST 198",
    "p5b_4": "AR 72, HR 18",
    "p5b_5": "SR 624, L 1424",
    "p5b_6": "L 42098, L 42056",
    "p5b_7": "L 736, L 1032, SR 672",
    "p5b_8": "L 112, L 1480",
    "p4_0": "XF 20, P11 1690",
    "p4_1": "L 75394, L 75362",
    "p4_2": "L 75405, XF 0, SR 552",
    "p4_3": "L 28120, L 63849",
    "p4_4": "L 42164, L 63834, L 27158",
    "p4_5": "L 42152, L 42518, L 28132",
    "p4_6": "P12 60, L 75661",
    "p4_7": "P12 8, L 75613",
    "p4_8": "L 75523, P12 124",
    "p4_9": "P13 44, P13 56, P13 68",
    "p4b_0": "P11 1020, P11 50, P11 960",
    "p4b_1": "P11 2620, P11 670",
    "p4b_2": "P12 372, P12 404, P12 436",
    "p4b_3": "P12 148, L 27016, L 62315",
    "p4b_4": "L 20479, L 1168",
    "p4b_5": "L 12814, L 12718",
    "p3_0": "TR 75, VL 36",
    "p3_1": "ST 360, MS 150",
    "p3_2": "L 20495, TR 64, SR 540",
    "p3_3": "L 12421, DA 10",
    "p3_4": "VL 183, DA 132",
    "p3_5": "TR 90, TR 97, P13 116",
    "p3_6": "P12 200, ST 405",
    "p3b_0": "VL 60, DA 120",
    "p3b_1": "L 12437, SG 180",
    "p3b_2": "L 12457, DA 66, SG 228",
    "p3b_3": "SG 144, VL 240",
    "p3b_4": "SCG 36, SCG 75",
    "p3b_5": "VL 303, SCG 105",
    "p3c_0": "SQ2 48, L 9915",
    "p3c_1": "SQ2 60, L 10123",
    "p3c_2": "L 39097, L 35735",
    "p2_0": "L 9867, L 12830",
    "p2_1": "L 11302, SG 6",
    "p2_2": "L 11322, SG 48",
    "p2_3": "L 11372, SR 576, L 12960",
    "p2_4": "SQ2 18, L 9579",
    "p2_5": "L 9161, L 9723",
    "p2_6": "L 10091, L 10035",
    "p2b_0": "SC 0, L 20627, SC 54",
    "p2b_1": "L 13016, L 13032, SF 33",
    "p2c_0": "SF 48, SF 153",
    "p2c_1": "SF 87, SF 123",
    "p2c_2": "LB 12, ST 282, L 75240",
    "p2c_3": "SC 339, SC 354",
    "p2c_4": "SR 600, L 168, SR 612",
    "p2c_5": "L 20523, L 20539, L 20507",
    "p2c_6": "L 42068, L 42116",
    "p2c_7": "SC 87, P13 126",
    "subs_0": "L 62350, P12 160",
    "subs_1": "L 1056, L 26656",
    "subs_2": "L 1200, L 26758",
    "subs_3": "L 44541, L 42530",
    "p1_0": "CN 54, SQ2 165",
    "p1_1": "SQ2 96, L 9800",
    "p1_2": "SQ 2, L 9812, CN 42",
    "p1_3": "L 20859, SQ 28",
    "p1_4": "L 20847, SQ2 141",
    "p1_5": "L 9822, SQ2 174",
    "p1_6": "L 27040, L 35021",
    "p1_7": "L 63785, L 28175",
    "p1b_0": "L 9251, L 35038, L 9411",
    "p1b_1": "SS 13, SF 3",
    "p1b_2": "ST 24, SS 36, MS 61",
    "p1c_0": "ST 135, P11 3450",
    "p1c_1": "ST 171, MS 135, P11 3582",
    "p1c_2": "L 28228, L 27970",
    "p1c_3": "ST 186, ST 384, ST 420",
    "p1c_4": "P12 100, L 75577",
    "p1c_5": "L 42806, ST 396",
    "cierre_0": "HR 54, L 75415, SG 120",
    "cierre_1": "L 26716, L 1504, TR 118",
    "cierre_2": "ST 249, L 75063",
    "cierre_3": "ST 455, ST 465, P11 3594",
    "cierreb_0": "P11 3604, ST 474",
    "cierreb_1": "P13 80, L 42842",
    "cierreb_2": "L 61860, L 61940, L 61995",
    "cierreb_3": "VL 105, MS 160",
    "cierreb_4": "L 1072, P12 24",
    "cierreb_5": "CN 66, SQ2 153",
}

NOTAS = {  # nota específica del momento (se añade a la de la fuente)
    "intro_0": "la Fortaleza sombría desde el Altiplano · Messmer con la lanza en llamas · fase 2 con las serpientes",
    "intro_1": "Messmer te mira desde lo alto → la llama de su mano y su cara mientras suena «Those stripped of the Grace of Gold…»",
    "introb_1": "jaulas ardiendo (tráiler) · Ruinas calcinadas · Belurat arrasada",
    "introb_2": "Caballero de Fuego · el León Danzante · la Anciana",
    "p5_1": "Caballeros de Fuego (armadura roja)",
    "p5_3": "el látigo de fuego del Caballero de Fuego («sus llamas son como serpientes») · espadón en llamas",
    "p5_4": "fase 2: la serpiente de fuego brota · la mano arranca el sello · Messmer con las serpientes",
    "p5_6": "EL OJO CON EL SELLO DE GRACIA (ST 225-228; negro a 231) · un Caballero Negro peleando («no todos sus hombres lo aceptaron»)",
    "p5b_0": "Caballeros Negros ante el altar de Huw (Catacumbas del río Escorpión)",
    "p5b_1": "Catacumbas de Grieta Neblinosa (donde está Andreas): PEGATINA de su ceniza",
    "p5b_2": "Catacumbas del río Escorpión (donde está Huw): PEGATINA de su ceniza",
    "p5b_3": "el altar de Huw · Messmer se tapa la cara (fase 2)",
    "p5b_5": "cementerio de la Llanura de las Tumbas: PEGATINA de las Cenizas de soldado de Messmer",
    "p4_1": "el Caballero de Fuego del PUENTE a las Antiguas ruinas de Rauh (el que suelta la Lluvia de fuego)",
    "p4_2": "Lluvia de fuego: columnas rojas a L 75400 y 75413",
    "p4_8": "las Antiguas ruinas de Rauh",
    "p4_9": "la Yesca quema el árbol sellado (P13 44-80)",
    "p4b_0": "el Almacén de especímenes (montaña de cuerpos P11 1000-1020)",
    "p4b_2": "Romina, la santa del brote, en la Iglesia del Brote",
    "p3_0": "tráiler: la criatura atravesada por lanzas entre las llamas",
    "p3_2": "Leda · tráiler: la purga · Ruinas calcinadas",
    "p3_3": "Belurat · cinemática del León",
    "p3_4": "el León lanza su TORNADO (VL 186-195)",
    "p3_5": "tráiler: siluetas empaladas en postes ardiendo · Enir-Ilim, la torre",
    "p3b_1": "cinemática del canto de la Anciana (subtítulos del juego)",
    "p3b_4": "el Sinluz CON la Cabeza de bestia divina ante la Anciana",
    "p2_1": "la Anciana cornamentada en su almacén de Belurat",
    "p2b_1": "la Anciana · Messmer con el Cornamentado invocado (suena «Messmer, foe of my beloved people…»)",
    "p2c_2": "el Cornamentado tras la muerte de Messmer · la cara de Messmer rodeada de serpientes",
    "p2c_3": "el Cornamentado en primer plano («O mother, O most cherished wife and child» SC 354-362)",
    "p2c_4": "Ruinas calcinadas (suelo de ceniza) y la Llanura de las Tumbas",
    "p2c_5": "Leda: «Queen Marika commanded Sir Messmer to purge the tower folk» (~L 20530, subtítulos)",
    "p1_2": "Queelign (espíritu rojo) invade Belurat y te mata (SQ 3-11)",
    "p1_3": "Queelign con su espadón en forma de lanza (Iglesia de la Cruzada)",
    "p1_5": "Queelign vencido (antes de «INVADER VANQUISHED»): PEGATINA de la Insignia de cruzada",
    "p1b_1": "entras en la sala: Messmer de pie antes de hablar",
    "p1b_2": "«Mongrel intruder… Mother, wouldst thou truly Lordship sanction…»: ojo de la serpiente, serpiente alada, casco",
    "cierre_1": "Fuerte de la reprimenda (la Bendición de Márika está en un cadáver a sus afueras): PEGATINA del objeto",
    "cierre_2": "la mano que arrancó el sello · la sala de Messmer",
    "cierre_3": "Messmer cae (suena «Mother… Marika… A curse upon thee»)",
    "cierreb_0": "Messmer muere de pie entre serpientes (P11 3604-3614) · se arrodilla y se deshace (ST 476-483)",
    "cierreb_2": "Bayle el Temible",
}

MIN_SEP = 9
EQUIV = {"P11": ("L", 71529)}  # P11 = el mismo metraje que L desde 71 529
CINE = {  # mismas cinemáticas de Messmer → tiempo P11
    "P11": [(3338, 3416, 0), (3460, 3575, 0)],
    "L": [(74867, 74945, -71529), (74989, 75104, -71529)],
    "ST": [(0, 77, 3340), (186, 298, 3276)],
    "SS": [(0, 77, 3340), (77, 189, 3385)],
    "MS": [(0, 90, 3325)],
    # cinemática del León Danzante (con el canto de la Anciana) → tiempo L
    "DA": [(9, 85, 12409)],
    "SG": [(174, 206, 12256), (206, 243, 12220)],
}
CINE["L"] = CINE["L"] + [(12419, 12494, 0)]
DUR = {"P12": 521, "P13": 3183, "ST": 487, "MS": 627, "SS": 188, "TR": 159, "VL": 320, "DA": 256, "SG": 766, "SCG": 141,
       "SC": 389, "LB": 71, "SF": 188, "SQ": 122, "SQ2": 185, "CN": 92, "AR": 104, "HR": 92, "XF": 79, "SR": 731}


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
    """url+segundo que ya usaron los demás videos del canal (videos/er_*/plan_frases.json y busquedas.json)."""
    import glob
    u = []
    for f in sorted(glob.glob("../er_*/plan_frases.json") + glob.glob("../er_*/busquedas.json")):
        if "er_messmer" in f:
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        pila = [d]
        while pila:
            x = pila.pop()
            if isinstance(x, dict):
                if x.get("url") and x.get("desde") is not None:
                    u.append((x["url"][-11:], float(x["desde"]), os.path.basename(os.path.dirname(f))))
                pila.extend(x.values())
            elif isinstance(x, list):
                pila.extend(x)
    return u


def lista():
    """[(alias, segundo, clave)] de todo el plan."""
    return [(a, int(s), k) for k, v in P.items() for a, s in (t.split() for t in v.split(","))]


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    out = opciones()
    json.dump(out, open("plan_frases.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    usos = [(EQUIV[a][0] if a in EQUIV else a, s + (EQUIV[a][1] if a in EQUIV else 0), k) for a, s, k in lista()]
    for i, a in enumerate(usos):
        for b in usos[i + 1:]:
            if a[0] == b[0] and a[2] != b[2] and abs(a[1] - b[1]) < MIN_SEP:
                print("  MISMO PLANO:", a, b)
    eq = sorted((s + off, k, a) for a, s, k in lista() for a0, b0, off in CINE.get(a, []) if a0 <= s < b0)
    for i, x in enumerate(eq):
        for y in eq[i + 1:]:
            if y[0] - x[0] >= MIN_SEP:
                break
            if x[1] != y[1]:
                print("  MISMA CINEMÁTICA:", x, y)
    antes = usados_antes()
    ids = {v[0]: a for a, v in F.items()}
    for a, s, k in lista():
        for vid2, s2, f in antes:
            if F[a][0] == vid2 and abs(s - s2) <= 3:
                print("  YA USADO EN", f, ":", k, a, s, "~", s2)
    for a, s, k in lista():
        d = DUR.get(a)
        if d and s + 9 > d:
            print("  PASA DEL FINAL:", k, a, s, "dur", d)
    import guion
    claves = [f"{e['id']}_{i}" for e in guion.ESCENAS for i in range(len(e["frases"]))]
    print(sum(len(v) for v in out.values()), "opciones;", len({F[a][0] for a, _, _ in lista()}), "fuentes")
    print(len(out), "frases con plan; faltan:", [c for c in claves if c not in out], "sobran:", [c for c in out if c not in claves])
