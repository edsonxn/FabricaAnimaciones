# -*- coding: utf-8 -*-
"""Plan de clips POR FRASE (10-nov-2026), hecho mirando hojas de contacto a 240p de cada fuente. Escribe plan_frases.json
(lo lee asignar_clips.py). Fuentes limpias: Leomega sin HUD, SS91 4K, Stratek (diálogos), capturas cortas verificadas.
    python _plan.py
"""
import json

F = {  # alias: (id, nota)
    "V": ("Yp6mfzUQlfM", "Stratek: Varré (diálogos, subtítulos)"),
    "LM": ("3h5IIdRbqGc", "Leomega sin HUD: Mohg, Señor de la Sangre"),
    "P42": ("4Z8-aJTKg8A", "SS91 Part 42: Mohg (HUD)"),
    "P41": ("0TgCfhikJic", "SS91 Part 41: Palacio de Mohgwyn (HUD)"),
    "PE": ("K1-34ZvTJAc", "Pineapple Express 4K HDR: palacio de Mohgwyn (HUD)"),
    "SN": ("BP_qVfDR1fo", "SS91 Part 40: Campo sacroníveo (HUD)"),
    "P5": ("dEeH4J4nBes", "SS91 Part 5: Península Llorosa (HUD)"),
    "HT": ("basUQB7ThKU", "SS91 Part 43: Árbol Hierático (HUD)"),
    "OK": ("ppwQbZM7GVQ", "Leomega sin HUD: Okina"),
    "VY": ("o5ExdrF182U", "Leomega sin HUD: Vyke, Iglesia de la Inhibición"),
    "EL": ("DJqh_VLXdlY", "Leomega sin HUD: Eleonora"),
    "YU": ("GjDz__-bfj8", "Stratek: Yura (subtítulos)"),
    "GI": ("QiBbpaIssO0", "Stratek: Gideon (subtítulos)"),
    "WM": ("ZSg1RYVt9as", "Night Cricket: Máscaras Blancas sin nombre en el pantano (HUD)"),
    "NO": ("D6J4Hz5_FW8", "Hacx7: noble sanguino (HUD; logo a los 44 s)"),
    "MG": ("TcpmEqDp3SE", "CJAC: invasión a Magnus en las Ruinas de Sanguifuria (HUD)"),
    "TA": ("53_o-_cxUsQ", "Zeonis: Garras de hemofuego (HUD)"),
    "SH": ("GXalZFL8-ZQ", "SpookyFairy: Grillete de Mohg sobre el Augurio (HUD)"),
    "VI": ("pW19OvhIE8k", "Lionheart: invasión a Varré y su muerte (HUD, subtítulos)"),
    "RB": ("VYUotEGwKro", "BertieGaming: Ríos de Sangre contra Mohg (HUD)"),
    "NE": ("HhNFpTSOs3I", "I.Eat.Games: Nerijus (OJO rótulos 30-140 s; usar ≥150)"),
    "ES": ("GAnqUZcKDE8", "Andrew Preston 4K: Esgar (HUD)"),
    "MA": ("D_iqjI2p7F4", "[SHIRRAKO] Malenia en las raíces (recorte .09)"),
    "MO": ("Mqi-s6M7xw8", "Leomega sin HUD: Mohg, el Augurio"),
    "SU": ("QjakOuLJlpw", "SS91 Part 49: Subsuelo de los marginados (HUD)"),
    "BV": ("7BnZhJg91RQ", "BonfireVN, intro 4K"),
    "P1": ("eG7fOBSQMes", "SS91 Part 1: Necrolimbo"),
    "NC": ("OS5zDzVp4JA", "Leomega sin HUD: Caballería nocturna"),
    "AN": ("6208qZmD8M4", "Stratek: Ansbach (subtítulos)"),
    "RC": ("ZNyINUjidKM", "Veloketh sin HUD: Radahn consorte"),
    "HE": ("PVsx41tJn_4", "MELOO (54 s, HUD): Radahn roba el corazón"),
    "MR": ("dxyVbyZmTjY", "Leomega sin HUD: Morgott"),
    "MV": ("0NXs2RvWdxA", "Veloketh sin HUD: Morgott"),
    "TR": ("wKPmbLmoHhA", "SS91 Part 3: Torrentera por Necrolimbo"),
    "R9": ("Huip3TdEOdU", "SS91 Part 9: Mesa Redonda"),
    "R7": ("aw0k-em6sZs", "SS91 Part 7: camino a Velo Tormentoso / Mesa Redonda"),
    "AL": ("gKUiD8bSF2o", "LK, Altus 4K sin HUD"),
    "ME": ("d2FRpV9KrkY", "Melina junto al Sinluz (subtítulos)"),
}

P = {
    "intro_0": "LM 120, P42 153, LM 204", "intro_1": "P41 528, PE 30, LM 12", "intro_2": "BV 98, MR 60, P42 238",
    "intro_3": "RC 272, RC 80, AN 270", "intro_4": "LM 72, P41 360, WM 156", "intro_5": "LM 168, P42 289, RB 27",
    "intro_6": "RB 63, TA 12, LM 216",
    "p5_0": "NE 150, SN 750", "p5_1": "P1 1100, V 0", "p5_2": "V 5, V 40",
    "p5b_0": "R7 24, R7 263, V 286", "p5b_1": "V 374, R9 2315", "p5b_2": "V 390, V 404", "p5b_3": "V 425, SN 750, NE 165",
    "p5b_4": "V 443, SN 618", "p5b_5": "MG 11, MG 30, AL 214", "p5b_6": "V 476, V 486", "p5b_7": "SN 772, WM 182, NE 153",
    "p5b_8": "TR 36, P41 528, LM 24", "p5b_9": "R7 1092, R9 2100", "p5b_10": "YU 0, YU 92", "p5b_11": "NE 150, NC 52, NE 168",
    "p5b_12": "EL 48, EL 112, EL 144", "p5b_13": "OK 9, OK 54, OK 81", "p5b_14": "SN 706, NE 172",
    "p4_0": "P5 360, V 529", "p4_1": "V 484, V 500, LM 108", "p4_2": "V 512", "p4_3": "V 530, V 545", "p4_4": "V 545, V 556",
    "p4_5": "ME 287, ME 1051, BV 196", "p4_6": "P1 324, VY 0, VY 13", "p4_7": "P5 150, P5 330, P5 372", "p4_8": "V 566, SN 640",
    "p4_9": "V 577, V 588",
    "p4b_0": "V 595, V 600", "p4b_1": "V 606, V 612", "p4b_2": "V 618",
    "p4c_0": "V 632, V 642", "p4c_1": "LM 24, P42 34, LM 84", "p4c_2": "V 660, V 670", "p4c_3": "VI 5, VI 30, V 726",
    "p4c_4": "VI 120, VI 135, LM 72", "p4c_5": "P41 552, PE 562, LM 12", "p4c_6": "P41 672, PE 2310, TR 50",
    "p3_0": "WM 26, WM 156", "p3_1": "WM 52, WM 182, WM 260", "p3_2": "WM 208, WM 234, P41 648", "p3_3": "V 714, VI 15, WM 286",
    "p3_4": "PE 30, P41 744", "p3_5": "WM 130, WM 160", "p3_6": "PE 1398, P41 336, PE 2386", "p3_7": "HT 128, HT 256, P41 408",
    "p3_8": "P41 432, SU 200, MO 40",
    "p3b_0": "NO 12, NO 24, PE 258", "p3b_1": "NO 28, NO 16", "p3b_2": "P41 768, P41 792, P41 840", "p3b_3": "MG 11, NO 8, MG 44",
    "p3b_4": "ES 10, ES 20, SU 136", "p3b_5": "P41 312, P41 696, P41 720", "p3b_6": "LM 30, P42 51, LM 60, P42 68",
    "p3b_7": "PE 562, PE 866, PE 2234", "p3b_8": "PE 486, P41 552", "p3b_9": "MR 60, MV 84, MO 100",
    "p2_0": "LM 24, P42 34", "p2_1": "SN 431, GI 78, HT 64", "p2_2": "HT 704, HT 128, RC 660", "p2_3": "MA 38, MA 70, LM 96",
    "p2_4": "P41 20, SN 486, SN 541", "p2_5": "LM 72, LM 84, P42 85", "p2_6": "LM 60, P42 68", "p2_7": "LM 90, P42 102, LM 36",
    "p2_8": "LM 80",
    "p2b_0": "LM 60, P42 68, TA 12", "p2b_1": "SN 772, WM 182, NE 155", "p2b_2": "LM 36, LM 48, P42 51",
    "p2b_3": "AN 270, AN 192, AN 210", "p2b_4": "LM 216, P42 204", "p2b_5": "LM 240, P42 255, RB 36", "p2b_6": "TR 18, P41 552",
    "p2b_7": "PE 2234, LM 60",
    "p1_0": "LM 168, P42 323", "p1_1": "SU 192, SU 200, SH 48", "p1_2": "MO 4, MO 58, MO 136", "p1_3": "MR 104, MO 160, P42 340",
    "p1_4": "RB 72, P42 357, LM 252", "p1_5": "LM 144, P42 170, LM 192", "p1_6": "LM 204, P42 221, RB 45",
    "p1_7": "P42 153, P42 221, LM 180", "p1_8": "LM 150",
    "p1b_0": "P42 272, P42 289, LM 228", "p1b_1": "LM 264, P42 306", "p1b_2": "P42 323, LM 276", "p1b_3": "TA 12, TA 16, RB 18",
    "p1b_4": "SN 750, WM 260, P41 840", "p1b_5": "RB 54, RB 81, LM 288", "p1b_6": "LM 84, P42 102, LM 36",
    "p1b_7": "BV 84, BV 98, BV 105", "p1b_8": "RB 9, OK 63, RB 90", "p1b_9": "RB 27, NE 165, SN 783", "p1b_10": "LM 320",
    "p1c_0": "LM 336, HE 18, P42 380", "p1c_1": "PE 2234, LM 60, PE 866",
    "cierre_0": "NE 153, V 600, LM 168, WM 182, LM 24", "cierre_1": "PE 30, P41 96, PE 562", "cierre_2": "P41 528, LM 12, TR 36",
    "cierre_3": "TR 50, P41 672", "cierre_4": "TR 6, TR 30, TR 66", "cierre_5": "BV 84, R7 1092", "cierre_6": "LM 84, LM 108",
    "cierre_7": "BV 46, RC 290, MV 84", "cierre_8": "SN 783, NE 150, LM 168",
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
print(len(out), "frases con plan; faltan:", [c for c in claves if c not in out], "sobran:", [c for c in out if c not in claves])
