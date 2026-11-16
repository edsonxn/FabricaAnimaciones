# -*- coding: utf-8 -*-
"""Plan de clips POR FRASE (16-nov-2026), hecho mirando hojas de contacto a 240p de cada fuente
(E:\\FabricaAnimaciones\\_tmp_hojas_sinluz\\*.jpg: una hoja por fuente + v_NN.jpg = comprobación final de TODAS las opciones,
3 cuadros por clip a +0,5 / +4,3 / +8,1 s; v1/ y v2/ = rondas anteriores, v_NN = cambios de la última). Escribe plan_frases.json (lo lee asignar_clips.py).
Fuentes limpias: SourceSpy91 4K sin comentarios (HUD normal), Leomega sin HUD, capturas cortas sin comentarista verificadas,
y clips ya aprobados en los MASTER anteriores de Runa Caída (Melina, Radahn, Morgott, Mohg, Godrick).
    python _plan.py
Ojo: SF/SR llevan marca SHIRRAKO abajo a la derecha (recortar); FA tiene «YOU DIED» a los 47 s (no pasar de 38) y el Sinluz
con pelo rosa; LV enseña «SUBSCRIBE» a los 2-4 s (usar >= 14); SA tiene marca @sharkr33x a los 3 y 60-64 s; TN/TV/TD/TI/TR
terminan con logo de Elden Ring (no pasar del final); IS e QM son capturas de baja resolución (blandas); NN/NJ = marionetas
pequeñas en la pelea; P18/P29/P30/GM/GT/BT/RG/PS/HM/DD/TD/ID/ME llevan subtítulos del juego en inglés (son diálogos).
Evitados: Stratek (plano estático), J_Gaming (formato vertical con texto), Soul Cat de la uva (anotaciones arriba).

TRAMOS DE AUDIO del juego (audio original, sin comentarista; Elden Ring solo tiene voces en INGLÉS: no existe doblaje español):
 (1) Hyetta tocada con la llama frenética (p2b «Escúchala», post 9 s):
     https://youtu.be/KO_LxOGMm0k  20.0 → 31.5 s  «Oh, it burns… my eyes… my eyes… they're melting…»  (Whisper: «Oh» 20,4 · «melting» 30,0)
     + el «gracias» llega 17 s después (ella ya en el suelo): 48.5 → 52.3 s «Thank you… Thank you…» (Whisper 48,7 / 51,2).
     Para un solo tramo de 9-11 s: unir 20.0-27.5 («Oh, it burns… my eyes») + 48.5-52.3 («Thank you… thank you») con fundido corto.
     Alternativa misma escena: https://youtu.be/NvP4Tp1bO9I 315.3 → 325.5 («Oh, it burns… my eyes… they're melting») + 343.8 → 348.6 («Thank you. Thank you.»)
     (y https://youtu.be/6qUwwj5uvOk 171-182 + 200-204, mismo audio).
 (2) Melina en la Forja de los gigantes (p1 «Escúchala», post 10 s): https://youtu.be/GRH4LNXKQt8 (Games from Mars, «All Melina
     Dialogues», cinemática limpia con subtítulos; la escena de la Forja va de 1036 a 1120 s y tiene pausas largas entre frases):
     «O Erdtree, you shall burn.» 1043.8 → 1048.6 · «Burn for the sake of the new Lord.» 1064.8 → 1068.2 ·
     «Thank you for guiding me here.» 1084.3 → 1088.6 · «The one who walks alongside flame shall one day meet the road of
     Destined Death.» 1102.3 → 1112.7 · «Goodbye.» 1116.3 → 1117.4 (tiempos de Whisper por palabra).
     Un solo tramo continuo de 11 s: 1107.0 → 1118.0 (final de «…Destined Death» + «Goodbye»).
     Recomendado (≈ 10 s, con fundidos de 0,2 s): 1043.8-1048.6 + 1084.3-1088.6 + 1116.3-1117.4 («O Erdtree, you shall burn… Thank
     you for guiding me here… Goodbye»). El vídeo de esos segundos sirve de clip (alias GR).
"""
import json

F = {  # alias: (id, nota)
    # --- SourceSpy91 4K60 sin comentarios ---
    "P1": ("eG7fOBSQMes", "SS91 Part 1: Necrolimbo (Capilla de la espera, Varré)"),
    "P5": ("dEeH4J4nBes", "SS91 Part 5: Irina junto al Puente del Sacrificio (subtítulos)"),
    "P9": ("Huip3TdEOdU", "SS91 Part 9: Godrick, Mesa Redonda, Enia"),
    "P12": ("kqvqNB5JoA0", "SS91 Part 12: Academia de Raya Lucaria"),
    "P13": ("U-hb0vL5sgg", "SS91 Part 13: Rennala (biblioteca, huevo de ámbar, luna llena, renacer); 945-977 Gideon en su despacho, 997-1049 Enia (subtítulos)"),
    "P18": ("j2pqoZYSy7E", "SS91 Part 18: Ranni en su torre, Tres Hermanas, Seluvis y su encargo (subtítulos)"),
    "P21": ("yPBc_rVWq9U", "SS91 Part 21: Radahn"),
    "P24": ("OC9bSeqZgYw", "SS91 Part 24: cráter de la estrella y Nokron"),
    "P29": ("YS1P-_MROO0", "SS91 Part 29: Mansión del Volcán (Tanith, Rya, despacho, invasor; subtítulos)"),
    "P30": ("bVWauAYPe60", "SS91 Part 30: Serpiente devoradioses y Rykard"),
    "P35": ("L4zVRGHc1yQ", "SS91 Part 35: Morgott, tronos, espinas del Árbol"),
    "P38": ("-q7O-BrN5Jg", "SS91 Part 38: Gigante de fuego"),
    "P44": ("CN9X0Yk6BqE", "SS91 Part 44: Elphael, tutor del Árbol Hierático"),
    "P47": ("7oet6D34udo", "SS91 Part 47: arena del Señor dragón Placidusax"),
    "P51": ("jv-toQeW4lE", "SS91 Part 51: Bestia de Elden, final"),
    "P46": ("9nmqal7jH9A", "SS91 Part 46: Melina ardiendo, Farum Azula"),
    "P48": ("Pqy93_M67Jg", "SS91 Part 48: Maliketh"),
    "P49": ("QjakOuLJlpw", "SS91 Part 49: Subsuelo de los marginados"),
    "P50": ("rTz4PyJYphw", "SS91 Part 50: Leyndell, capital cinérea"),
    # --- Leomega sin HUD / otras 4K ya aprobadas ---
    "LR": ("8D_h_1cNz28", "Leomega sin HUD: Radahn y la estrella que cae"),
    "LG": ("qyi-SaN0VyQ", "Leomega 4K: Gurranq/Maliketh y capital cinérea (imagen grisácea)"),
    "LV": ("o5ExdrF182U", "Leomega sin HUD: invasión de Vyke junto a la Iglesia de la Inhibición (SUBSCRIBE a los 2-4 s)"),
    "LGf": ("E7LBpBZbO_A", "Leomega: Godfrey en la capital cinérea"),
    "LMo": ("3h5IIdRbqGc", "Leomega sin HUD: Mohg"),
    "BV": ("7BnZhJg91RQ", "BonfireVN, intro 4K"),
    "GR": ("GRH4LNXKQt8", "Games from Mars: todas las escenas de Melina; la Forja 1036-1120 (subtítulos)"),
    "ME": ("d2FRpV9KrkY", "Melina, todas sus escenas (subtítulos del juego)"),
    "SF": ("2OeHibcPujg", "[SHIRRAKO] Melina en la Forja (marca abajo a la derecha: recortar)"),
    "SR": ("3ITVOJedlPo", "[SHIRRAKO] Rennala (marca abajo a la derecha: recortar)"),
    "MD": ("L-7qooc9Lm0", "madredman 4K: la Forja de los gigantes, el Árbol ardiendo"),
    "MK": ("pecrcqqbrNE", "Maiko 4K: Tres Dedos y final de la Llama Frenética"),
    "CB": ("4XIeTCZRMtA", "Ctrl-Break 1080p: Melina tras heredar la llama frenética"),
    "TF": ("WnIequx79Lc", "TreeFrog 4K HDR: capital cinérea"),
    "NC": ("8tqCDM7ikOc", "Night Cricket: invasión de Edgar el Vengador"),
    "GG": ("Cc6o9P9Vj-Y", "GoonGoblin: cinemática de Malenia"),
    "RN": ("W4K4iaLfcug", "4KGameScape: final de Ranni"),
    # --- capturas cortas sin comentarista, verificadas aquí ---
    "GM": ("NegxKs8hpVg", "Games from Mars: sótano secreto de las marionetas de Seluvis (subtítulos)"),
    "IS": ("nt5AW6T82ZQ", "Indyrael: la marioneta de Sellen en el sótano (baja resolución)"),
    "FA": ("Jn0fgaiYiMk", "Faust Kellhound: el Brebaje ámbar y Ranni te mata (YOU DIED a los 47 s)"),
    "SA": ("Ly4f2A4hEzY", "Shark R: Meseta Altus y la gruta del Ámbar de luz estelar (marca IG a los 60-64 s)"),
    "TN": ("eBgwPG84YFA", "Terry Goodwin: la Poción de Seluvis a Nepheli en la Mesa Redonda (subtítulos)"),
    "TV": ("wGXvqHpxaJM", "Terry Goodwin: Nepheli en Velo Tormentoso (subtítulos)"),
    "TD": ("bJyERiLPuGk", "Terry Goodwin: el Zampaheces en su celda (subtítulos)"),
    "ID": ("EDSQiIvM9fU", "Indyrael: la Poción de Seluvis al Zampaheces (subtítulos)"),
    "NN": ("dJdqBGe3-QU", "NanoSunGaming: marioneta de Nepheli invocada (pequeña)"),
    "NJ": ("JL3HjlyaXX0", "NanoSunGaming: marioneta del jarróntropo invocada (pequeña)"),
    "OT": ("xpUganhtAW4", "ouchbox: marioneta de la doncella Therolina en combate"),
    "BT": ("D9pxwBVMrKk", "Brunoborne: Tanith comiéndose a Rykard (subtítulos)"),
    "GT": ("sJ3hbEi9loA", "Games from Mars: Tanith junto al cadáver de Rykard (subtítulos)"),
    "NR": ("2PIkBrpEXms", "Night Cricket: Rya en la Mansión del Volcán (subtítulos)"),
    "TI": ("dPFsoDcVNDM", "Terry Goodwin: invasión al viejo caballero Istvan, Colina Tormentosa (imagen lavada)"),
    "TR": ("ixmr7zjMqEk", "Terry Goodwin: invasión a Rileigh el holgazán, Meseta Altus"),
    "IJ": ("a5keqz0DCbc", "ImpalerVladTepes: invasión a Juno Hoslow, Picos de los gigantes"),
    "HV": ("MR4-ClmH37k", "Hat Creature: cadáver de la doncella en la Iglesia de la Inhibición (190-199)"),
    "RG": ("c5mltemiLdA", "ryurain: Gurranq y las nueve Raíces mortuorias (subtítulos)"),
    "AM": ("xP1soo9xRF0", "Anendale: Mausoleo errante caminando (cámara fija)"),
    "QM": ("gMLJy0QON7E", "Quezlalok: Mausoleo errante, soldados sin cabeza, romper las calaveras y entrar (baja resolución)"),
    "HM": ("NvP4Tp1bO9I", "Honored Madman: Hyetta, toda su historia (subtítulos)"),
    "DD": ("KO_LxOGMm0k", "Destined Death: Hyetta tocada con la llama frenética (subtítulos)"),
    "PG": ("r7Qf8x9tXzo", "PlaystationSaurus: sala del trono de Velo y el espíritu de la uva (subtítulos)"),
    "PS": ("EEMygkpKX08", "PlaystationSaurus: Shabriri en los Picos (subtítulos; imagen lavada)"),
    "BP": ("XrD_Nt2d84Q", "bad_on_pc: rótulo «Caria Manor» y el lugar de Pidia (oscuro)"),
    "TM": ("2jMBnMbGZss", "TrackstarOP: signo rojo en Elphael, invasión a Millicent y sus hermanas (rótulos del autor a los 6, 18, 96 s: usar 24-44)"),
    "GN": ("s2-dovDlRdg", "Games from Mars: la Aguja de Miquella en la arena de Placidusax (Sinluz casi desnudo; menú a los 58-60 s)"),
    "HF": ("dEwcTvkOnNw", "Herc: la Forja con la llama frenética, el Sinluz arde"),
    "DE": ("FuTinuf7ZhE", "final Bendición de la desesperación (Zampaheces; logo chico arriba a la derecha)"),
}

P = {
    "intro_0": "BV 46, BV 105, P9 162",
    "intro_1": "P9 900, P35 606, LR 513",
    "intro_2": "P1 324, P9 2100",
    "intro_3": "TN 6, P29 202, HM 10, HF 81",
    "intro_4": "SF 176, MD 84",
    "voto_0": "P9 230, P9 380",
    "voto_1": "P9 2100, P1 1340",
    "voto_2": "BV 196, P1 1355",
    "voto_3": "LMo 84, LMo 66",
    "voto_4": "P1 324, BV 126",
    "p5_0": "GM 93",
    "p5_1": "P18 296, P18 906, P18 928",
    "p5_2": "P18 940, P18 964, P18 988",
    "p5_3": "TN 6, TV 18, TD 12, P13 945",
    "p5_4": "TN 21, TN 36",
    "p5_5": "GM 96, GM 102",
    "p5b_0": "GM 21, GM 45, GM 60, GM 72",
    "p5b_1": "GM 93, OT 6, NN 6",
    "p5b_2": "NN 9, NN 54, TN 21",
    "p5b_3": "ID 18, TD 24, NJ 8",
    "p5b_4": "OT 6, OT 54, OT 51",
    "p5b_5": "IS 30, IS 48",
    "p5b_6": "P18 1004, FA 4, P18 360",
    "p5b_7": "SA 24, SA 45, FA 30",
    "p5b_8": "TV 36, TN 45",
    "p5c_0": "P18 1028, GM 93, BP 21",
    "p5c_1": "NN 54, TV 36, NN 24",
    "p5c_2": "NN 9, NN 60, TV 18",
    "p5c_3": "ID 57, ID 66, DE 111",
    "p5c_4": "P13 945, P13 965",
    "p5c_5": "GM 102, GM 108, P18 1028",
    "p5c_6": "GM 72, GM 78, GM 99",
    "p5c_7": "P13 965, GM 96, GM 75",
    "p4_0": "P29 176",
    "p4_1": "P29 150, P29 158, P29 202, P29 238",
    "p4_2": "P29 626, P29 818",
    "p4_3": "TI 13, TR 12, IJ 9",
    "p4_4": "TI 36, IJ 36, P29 824",
    "p4_5": "P30 262, P30 216",
    "p4_6": "P29 828, P29 278",
    "p4b_0": "P29 214, P30 48",
    "p4b_1": "P30 88, P30 96",
    "p4b_2": "P30 128, P30 160",
    "p4b_3": "P30 208, P30 240, P30 296",
    "p4b_4": "BT 8, GT 18, BT 20",
    "p4b_5": "P29 590, NR 64, BT 28",
    "p4b_6": "P1 1144, P1 1188",
    "p4b_7": "P1 1200, HV 190",
    "p4b_8": "HV 190, LV 16, HM 10",
    "p4c_0": "P29 214, P29 226, BT 32",
    "p4c_1": "P29 596, NR 76, NR 100",
    "p4c_2": "NR 120, P29 608, NR 64",
    "p4c_3": "GT 27, P30 216, P30 248",
    "p4c_4": "BT 92, BT 104, BT 120",
    "p4c_5": "P44 15, TM 24, TM 36",
    "p3_0": "P9 380",
    "p3_1": "P9 162, P9 194",
    "p3_2": "P9 2315, LR 513, P35 622",
    "p3_3": "P12 90, P13 48, P13 90",
    "p3_4": "P13 92, SR 60, P13 72",
    "p3_5": "P13 120, P13 300, P13 198",
    "p3_6": "P13 949, P13 268",
    "p3_7": "P13 486, P13 498",
    "p3d_0": "P13 288, SR 290, P13 330",
    "p3d_1": "P13 336, P13 204, P13 216",
    "p3d_2": "P13 90, SR 60, P13 492",
    "p3d_3": "P18 296, P13 498, P13 564",
    "p3b_0": "LR 75, LR 270, LR 300",
    "p3b_1": "LR 90, LR 375, P21 700",
    "p3b_2": "LR 435, LR 529, P21 1265, P24 126",
    "p3b_3": "P24 126, P24 360, LR 529",
    "p3b_4": "AM 4, QM 15",
    "p3b_5": "QM 50, QM 75, AM 116",
    "p3b_6": "QM 155, QM 195, AM 60",
    "p3e_0": "AM 160, QM 25, QM 200",
    "p3e_1": "P13 1005, P9 2315, P30 262",
    "p3e_2": "ME 688, BV 46",
    "p3e_3": "BV 105, LR 513, P35 622",
    "p3f_0": "P30 240, P30 208",
    "p3f_1": "P30 128, P30 296, P30 88",
    "p3f_2": "P30 262, P30 48",
    "p3c_0": "RG 0, RG 18",
    "p3c_1": "RG 60, RG 84",
    "p3c_2": "RG 114, RG 198, RG 216",
    "p3c_3": "RG 264, RG 384, RG 414",
    "p3c_4": "LG 120, P48 187, P48 221",
    "p3c_5": "RG 300, LG 132",
    "p3c_6": "P13 92, LR 300, RG 60, AM 4",
    "p2_0": "HM 10",
    "p2_1": "P5 340, P5 370, HM 5",
    "p2_2": "HM 10, HM 30",
    "p2_3": "PG 118, HM 30",
    "p2_4": "HM 50, HM 60, HM 123",
    "p2_5": "NC 20, NC 40, P5 395",
    "p2_6": "PG 15, PG 118, PG 130",
    "p2d_0": "HM 30, HM 10",
    "p2d_1": "HM 60, HM 70",
    "p2d_2": "PS 8, PS 24, PS 100",
    "p2d_3": "PS 128, HM 145, HM 15",
    "p2d_4": "HM 270, DD 56",
    "p2b_0": "HM 128, HM 138",
    "p2b_1": "HM 143, HM 155, HM 165",
    "p2b_2": "HM 190, LV 16, LV 36, LV 54",
    "p2b_3": "P49 136, HM 260, MK 0, MK 42",
    "p2b_4": "MK 42, MK 14, DD 6",
    "p2b_5": "DD 18, HM 312, DD 46",
    "p2c_0": "DD 46, HM 432",
    "p2c_1": "HV 190, HM 60",
    "p2c_2": "P5 340, NC 40, HM 15",
    "p2c_3": "BV 196, P1 1355",
    "p2c_4": "P9 2100, P1 1340, BV 196",
    "p1_0": "SF 168",
    "p1_1": "MD 84, P46 300",
    "p1_2": "ME 165, ME 207",
    "p1_3": "P35 300, P35 664, ME 874, ME 903",
    "p1_4": "P38 88, P38 195, ME 1440",
    "p1_5": "ME 1458, GR 1042, GR 1084, GR 1102",
    "p1b_0": "GR 1072, ME 1500, GR 1108",
    "p1b_1": "PS 52, PS 8",
    "p1b_2": "HF 54, HF 63, HF 81",
    "p1b_3": "MK 175, ME 1213, CB 2, ME 1238",
    "p1b_4": "ME 1226, MK 154, ME 1296",
    "p1b_5": "SF 205, MK 189",
    "p1d_0": "ME 357, ME 345",
    "p1d_1": "ME 1062, P9 2465, P9 2540",
    "p1d_2": "P47 545, GN 49, P47 140",
    "p1d_3": "P46 1000, MD 84",
    "p1d_4": "P51 300, RN 93, MK 154, DE 141, TF 106, GR 1108",
    "p1c_0": "TF 106, TF 122, LG 360",
    "p1c_1": "TD 24, DE 72, DE 111",
    "p1c_2": "DE 111, TD 26, DE 141",
    "p1c_3": "MD 84, HF 102, SF 176",
    "p1c_4": "P1 324, MK 189",
    "cierre_0": "GM 96, P30 262, P13 92, RG 300, HM 312, SF 176",
    "cierre_1": "P35 168, P9 162",
    "cierre_2": "P9 2100, P1 1340",
    "cierre_3": "P30 216, LGf 160, P48 289, SR 275, TD 12, P13 945",
    "cierre_4": "BV 46, GG 60, RN 93, LR 270, LMo 84, P9 162",
    "cierre_5": "P1 324, P1 466",
}

out = {}
for k, v in P.items():
    ops = []
    for t in v.split(","):
        a, s = t.split()
        vid, nota = F[a]
        ops.append({"url": f"https://youtu.be/{vid}", "desde": int(s), "nota": nota})
    out[k] = ops
json.dump(out, open("plan_frases.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import guion
claves = [f"{e['id']}_{i}" for e in guion.ESCENAS for i in range(len(e["frases"]))]
print(len(out), "frases con plan de", len(claves), "; faltan:", [c for c in claves if c not in out],
      "sobran:", [c for c in out if c not in claves])

