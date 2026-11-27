# -*- coding: utf-8 -*-
"""Plan de clips POR FRASE (27-nov-2026) de «5 atrocidades de Maliketh que el juego te ESCONDIÓ», hecho mirando hojas de
contacto a 240p de cada fuente (E:\\FabricaAnimaciones\\_tmp_hojas_maliketh\\h\\*.jpg: una hoja por fuente o por tramo del
longplay + hojas finas de 1-4 s de los momentos exactos; v\\v_NN.jpg = comprobación final de TODAS las opciones, 4 cuadros
por clip a -2 / +0,5 / +4,3 / +8,1 s del segundo elegido). Escribe plan_frases.json (lo lee asignar_clips.py).
    python _plan.py
Fuentes limpias (sin comentarista, facecam ni mods): SourceSpy91 «Part NN» sin comentarios (M Maliketh, DB Montedrago y el
Santuario de la bestia, DT Torre Sagrada de Caelid, DR Raíz profunda / Mesa Redonda, P36 Tierras prohibidas, FA Farum Azula,
P2F Catacumbas del Cuchillo Negro; HUD normal y subtítulos del juego en los diálogos); Veloketh (MV Maliketh sin HUD); ONGBAL
(ON Maliketh sin HUD); Leomega (LG, Gurranq → Maliketh, imagen algo grisácea); SpT5r (GS, Gurranq y la cinemática); ryurain
(RG, todos los diálogos de Gurranq, subtítulos del juego, oscuro); Ephesus (GD1, matar a Gurranq); Stratek (DS el caballero D,
RS Rogier: planos fijos con subtítulos); Games from Mars (GM, las DOS muertes de Maliketh); gárgolas (BK1, BK2, BK3, VG1, VG2);
tráiler de la historia oficial (TRN); intro del juego (BV); Godwyn (GW); Tiche contra Maliketh (TM, baja calidad); y para el
cierre Rykard (P30), Ghiza (JM), Rennala/Rellana (RN), Parches (PE), Gideon (GDF), Melina (ME), Malenia (MA), Radahn (LR),
Ranni (RA), Altus (LK), Catacumbas del Cuchillo Negro de Liurnia (BKC, jugador con ropa roja).
Descartadas: GD2 (jugador desnudo), GD3 (intro del canal «Cammysta» 0-5), PEG (jugador sin camisa, rótulos), TI (no se
distingue a Tiche), BKA (asesina demasiado oscura, ENEMY FELLED 130), WD (combate genérico), HJ6EIysyst8 (720p máx.).
Ojo (marcas, menús, mapas, rótulos; segundos de la fuente):
 - M: «LEGEND FELLED» 389-391, aviso de objeto 392-394, negros 243, 395, 440-448, 484-496; rótulo «Leyndell, Ashen Capital»
   536; MAPA 544-548; menús 560-596; subtítulo «Witless Tarnished…» 378-388.
 - MV: LEGEND FELLED 510, negro 515. ON: subtítulos 5-10 y ≈ 270, oscuro 285-295. GS: menú 0, negro 35.
 - LG: MAPA 0, negros 75, 270-280, 315-330; rótulo 370; LOST GRACE 375.  GM: LEGEND FELLED 85 y 100.
 - RG: menús 45, 80, 315, 360, 432; YOU DIED 130; cargas 135-155; rótulo «Bestial Sanctum» 160.
 - DB: MAPA 320-330, 400, 1010, 1070, 2130; rótulo «Greyoll's Dragonbarrow» 1084; ENEMY FELLED ≈ 1392; aviso 1396-1400;
   menús 1410-1444, 1490-1492 (breve), 1516-1524 (breve), 1550-1576; LOST GRACE 1544.
 - DT: rótulo 30-32; GREAT RUNE RESTORED ≈ 411; menús 420-430, 1531-1560; GREAT ENEMY FELLED 1489; aviso 1492, ≈ 1525;
   MAPA 1590.  DR: MAPA 60-75, 780, 1830; cargas 90-150, 1320, 1605; rótulo «Deeproot Depths» 1530, 1785.
 - FA: menús 60, 2280, 2340, 3750, 4500, 5220, 6780-6810; MAPA 3600; rótulo «Crumbling Farum Azula» 472-474, 6840.
 - P2F: menús 4055-4110, 4160, 4205; ENEMY FELLED 4034.  BK2: ENEMY FELLED 294, aviso 300.  BK3: rótulo 5, aviso 130.
 - VG1: tarjeta de SUSCRIPCIÓN del canal 0-12 (empezar ≥ 15).  VG2: GREAT ENEMY FELLED 115, aviso 125.
 - JM: INVADER VANQUISHED 45.  P30: LOST GRACE 10, menús 20-30, 60-70.  ME: LOST GRACE 120, menús 260, 380.
 - TRN: clasificación 0, negro 40 y 70, logos 205+.  BV: negro 44-45, 56-58, 67+.
MOMENTOS EXACTOS comprobados en hoja:
 - Cinemática Gurranq → Maliketh: M 172-242 (Gurranq arrodillado 172-176, la mano 180-188, LA HOJA LE SALE DEL CUERPO 196-212,
   Maliketh revelado 216-242) = MV 100-170 = ON 65-130 = LG 80-145 = GS 40-105.  Fase 2 «Oh Muerte» (fogonazo rojo) M 249-258,
   MV 185-195.  Muerte: M 378-388 · MV ≈ 497 · ON ≈ 268 · GM 70-80 («Witless Tarnished») y GM 88-97 («Forgive me, Marika»).
   Se deshace y la Runa de la Muerte: M 404-432 = MV 520-545 = ON 300-320 = LG 230-265.  Narración, Árbol ardiendo y Leyndell
   en ceniza: M 452-532 = LG 285-365.
 - Santuario de la bestia: cabalgada DB 1086-1132 (de frente 1118-1132); gárgola DB 1134-1390; escalinata 1446-1458, puerta
   1460-1466, interior 1470-1476; Gurranq 1478-1534 («Strange… something else» = 4.ª raíz ≈ 1500-1504); salida 1586-1598.
 - Gurranq se lanza contra ti: RG 180-235; GD1 0-120, muere 122 (estallido blanco).  Esqueletos: P2F 3557-3572, 3787-3799.
 - Torre Sagrada de Caelid: DT 34-56 (al fondo), apóstol sacrodermo 1040-1486, sala del espadón 1495-1521.
 - Noche de los Cuchillos Negros (las asesinas apuñalan a Godwyn): BV 59-66.  Márika: BV 46-54.  Círculo roto: TRN 75-90.
 - Tiche (blanca) contra Maliketh: TM 8-22.  Gárgola de las Tierras prohibidas: P36 1390-1540; BK3 10-125.
"""
import json
import os

F = {  # alias: (id, nota)
    "M": ("Pqy93_M67Jg", "SS91 Part 48: Clérigo bestia y Maliketh (HUD; cinemática 172-242)"),
    "MV": ("QSF8X-0GiuU", "Veloketh: Maliketh sin HUD"),
    "ON": ("ijn3476GmKU", "ONGBAL: Maliketh sin HUD"),
    "LG": ("qyi-SaN0VyQ", "Leomega: Gurranq → Maliketh (imagen algo grisácea)"),
    "GS": ("SpT5r_I2VYU", "Gurranq y la cinemática de Maliketh (sin HUD)"),
    "RG": ("c5mltemiLdA", "ryurain: diálogos de Gurranq (subtítulos del juego, oscuro)"),
    "GD1": ("naCmyx_ZUyw", "Ephesus: atacar a Gurranq hasta matarlo (HUD; muere 122)"),
    "GM": ("Pxrcjovrevc", "Games from Mars: las dos muertes de Maliketh (subtítulos del juego)"),
    "DB": ("nY_GWYSBz_Y", "SS91 Part 31: Montedrago y el Santuario de la bestia (HUD)"),
    "DT": ("vXwBJr-fLM8", "SS91 Part 23: Torre Sagrada de Caelid y el apóstol sacrodermo (HUD)"),
    "DR": ("KNOGSI89eQo", "SS91 Part 32: Mesa Redonda, D y la Raíz profunda"),
    "DS": ("q-YL48Rr7L0", "Stratek: el caballero D (plano fijo, subtítulos)"),
    "P36": ("klpmiK6UEjw", "SS91 Part 36: Tierras prohibidas y su gárgola"),
    "FA": ("9nmqal7jH9A", "SS91 Part 46: Farum Azula"),
    "P2F": ("wBp1Br0773o", "SS91: catacumbas con esqueletos (HUD, oscuro)"),
    "BK1": ("IFzgkNRVfJA", "gárgola del Santuario de la bestia (HUD)"),
    "BK2": ("fQjCJnVTrY4", "gárgola del Santuario de la bestia, luminoso (HUD)"),
    "BK3": ("HaJOgAg90AY", "gárgola de las Tierras prohibidas (HUD)"),
    "VG1": ("Ucx7rNbTomE", "gárgolas denodadas (HUD)"),
    "VG2": ("HIAPDjsKH50", "gárgola denodada (HUD)"),
    "TRN": ("K_03kFqWfqs", "tráiler de la historia oficial"),
    "BV": ("7BnZhJg91RQ", "intro del juego"),
    "GW": ("vhmkUYSyMfE", "Godwyn el Dorado"),
    "TM": ("5LwjI7xlTG0", "Tiche contra Maliketh (baja calidad)"),
    "RS": ("EbTt4y1bEVc", "Stratek: Rogier en la Mesa Redonda (plano fijo, subtítulos)"),
    "RA": ("W4K4iaLfcug", "final de Ranni"),
    "BKC": ("AeID0Nvn9Tc", "Catacumbas del Cuchillo Negro, Liurnia (HUD)"),
    "LK": ("gKUiD8bSF2o", "Altiplano de Altus dorado y el Árbol Áureo"),
    "JM": ("d7Lg5R8Np-4", "la Mansión del Volcán y la rueda de Ghiza"),
    "P30": ("bVWauAYPe60", "Rykard (cinemática 200-270)"),
    "RN": ("vpBRYiQ5bio", "Rellana y Rennala"),
    "PE": ("0U52CsjKPrY", "Parches (subtítulos del juego)"),
    "GDF": ("kZ4pC3lkIKU", "Gideon en la Mesa Redonda (subtítulos)"),
    "ME": ("d2FRpV9KrkY", "Melina"),
    "MA": ("kS5bYCb3ZRg", "Malenia (cinemática 90-170)"),
    "LR": ("8D_h_1cNz28", "Radahn (cinemática 70-120)"),
}

P = {
    "intro_0": "FA 386, M 216, MV 150",
    "intro_1": "M 250, MV 186, ON 196",
    "introb_0": "MV 292, M 302, ON 210",
    "introb_1": "RG 26, LG 30",
    "introb_2": "DB 1150, DS 30, DT 1060",
    "introb_3": "MV 335, M 322, ON 240",
    "introb_4": "ON 230, MV 380",
    "introb_5": "MV 410, ON 145, M 280",
    "p5_0": "BK2 40, DB 1160, VG2 30",
    "p5_1": "DB 1100, DB 1118",
    "p5_2": "DB 1136, BK2 60, BK1 130",
    "p5_3": "DB 1378, BK2 282, BK3 112",
    "p5_4": "VG2 20, VG1 20, BK2 120",
    "p5_5": "BK2 180, BK1 200, DB 1250",
    "p5_6": "VG2 60, VG1 60",
    "p5b_0": "VG1 100, BK2 230, DB 1300",
    "p5b_1": "VG2 90, BK1 260, DB 1200",
    "p5b_2": "M 230, MV 200, ON 156",
    "p5b_3": "BK3 40, MV 225, VG1 140",
    "p5b_4": "P36 1100, P36 1400, BK3 15",
    "p5b_5": "DB 1448, BK3 80, P36 1450",
    "p4_0": "DS 100, DR 1150, DS 200",
    "p4_1": "RG 36, DB 1478",
    "p4_2": "P2F 3557, P2F 3792, DR 642",
    "p4_3": "DR 655, BV 32",
    "p4_4": "LK 500, DR 678",
    "p4_5": "P2F 3736, RG 255, DB 1528",
    "p4b_0": "DS 15, DR 475, DS 45",
    "p4b_1": "DS 130, DR 500, DR 1165",
    "p4b_2": "RG 52, DS 400",
    "p4b_3": "DB 1462, RG 66",
    "p4b_4": "DB 1498, RG 330",
    "p4b_5": "RG 350, RG 340",
    "p4b_6": "RG 395, RG 376",
    "p4c_0": "RG 185, GD1 20",
    "p4c_1": "RG 225, GD1 60",
    "p4c_2": "RG 366, GD1 90",
    "p4c_3": "JM 30, JM 10",
    "p4c_4": "P30 222, P30 232",
    "p3_0": "MV 20, ON 20, M 60",
    "p3_1": "M 172, MV 103, RG 290",
    "p3_2": "FA 539, FA 586, FA 5787",
    "p3_3": "FA 4330, MV 40, ON 40",
    "p3_4": "RG 270",
    "p3_5": "MV 60, M 100",
    "p3_6": "MV 240, M 346, ON 250",
    "p3_7": "BV 90, BV 170, TRN 130",
    "p3_8": "M 182, RG 205, MV 80",
    "p3b_0": "M 414, MV 531",
    "p3b_1": "GW 35, DR 1400",
    "p3b_2": "LK 440, LK 230",
    "p3b_3": "M 198, MV 131, ON 90",
    "p3b_4": "M 428, LG 256",
    "p3c_0": "FA 6006, FA 4400, M 4",
    "p3c_1": "MV 450, ON 176, M 364",
    "p3c_2": "M 18, FA 5962, MV 470",
    "p2_0": "DT 1075, DT 1100",
    "p2_1": "MV 305, M 270",
    "p2_2": "DT 40, DT 1150, DT 70",
    "p2_3": "DT 1513, DT 1200, DT 1497",
    "p2_4": "ME 175, DT 1250, DT 1310",
    "p2_5": "MV 320, ON 186, M 312",
    "p2b_0": "DT 1350, DT 1400, DT 1440",
    "p2b_1": "DT 1460, MV 360, M 332",
    "p2b_2": "DT 1474, DT 340, DT 360",
    "p2b_3": "MV 395, DT 1170",
    "p2b_4": "DT 1220, DT 1280",
    "p2b_5": "DT 52, DT 380",
    "subs_0": "FA 4345, FA 1320",
    "subs_1": "FA 4380, MV 420",
    "subs_2": "FA 410, FA 4420",
    "subs_3": "FA 4450, FA 6015",
    "subs_4": "MV 440, MV 215",
    "p1_0": "TRN 30, GW 60",
    "p1_1": "RS 120, TRN 47",
    "p1_2": "GW 75, GW 110",
    "p1_3": "TM 10, TM 30",
    "p1_4": "TRN 17, RA 28, GW 44",
    "p1_5": "M 293, MV 260",
    "p1_6": "BKC 20, BKC 200, BKC 400",
    "p1_7": "BKC 300, P2F 3880, BKC 620",
    "p1_8": "BV 62, P2F 3950",
    "p1_9": "GW 90, BKC 100",
    "p1b_0": "M 404, LG 233",
    "p1b_1": "ON 166, MV 175",
    "p1b_2": "MV 345, ON 220",
    "p1b_3": "GD1 40, GD1 80",
    "p1b_4": "GD1 100, GD1 106",
    "p1c_0": "GD1 117, GD1 123",
    "p1c_1": "TRN 80, BV 200",
    "p1c_2": "MV 460, GM 35",
    "p1d_0": "MV 487, MV 250",
    "p1d_1": "M 472, LG 305",
    "p1d_2": "M 456, LG 290",
    "p1d_3": "DS 420, DR 1180, MV 30",
    "cierre_0": "DB 1180, DS 440, DT 1330",
    "cierre_1": "GM 25, GM 45",
    "cierre_2": "GM 58, MV 270",
    "cierreb_0": "GM 71, M 378",
    "cierreb_1": "RG 420, LG 205",
    "cierrec_0": "GM 88, GM 91",
    "cierrec_1": "MV 280, LG 215",
    "cierrec_2": "GM 5, GM 15",
    "cierrec_3": "M 510, LG 352",
    "cierrec_4": "RN 66, RN 38, PE 70, GDF 10",
    "cierrec_5": "MA 140, LR 96, RA 60",
    "cierrec_6": "LK 720, LK 620",
    "cierrec_7": "RG 404, DB 1588",
}

NOTAS = {  # nota específica del momento (se añade a la de la fuente)
    "intro_0": "Farum Azula flotando en la tormenta · Maliketh revelado en la cinemática",
    "intro_1": "fase 2: el fogonazo rojo de «Oh Muerte»",
    "introb_1": "Gurranq en su santuario",
    "introb_2": "la gárgola · el caballero D · el apóstol sacrodermo",
    "introb_4": "Márika (intro del juego)",
    "p5_1": "la cabalgada por Montedrago y el Santuario de la bestia de frente",
    "p5_2": "el Fiel de la Hoja Negra (gárgola) en la puerta",
    "p5_3": "la gárgola cae",
    "p5b_4": "el camino de las Tierras prohibidas y su gárgola",
    "p5b_5": "la escalinata del santuario",
    "p4_2": "esqueletos que se levantan",
    "p4_3": "la noche (tráiler) · raíces de la Raíz profunda",
    "p4_4": "raíces · el Árbol Áureo",
    "p4b_0": "D, con los subtítulos del juego",
    "p4b_4": "la 4.ª raíz: «Strange… something else»",
    "p4c_3": "la rueda de Ghiza",
    "p4c_4": "Rykard",
    "p3_2": "hombres bestia de Farum Azula",
    "p3b_0": "la Runa de la Muerte",
    "p3b_1": "Godwyn, el Príncipe de la Muerte",
    "p3b_3": "la hoja le sale del cuerpo",
    "p2_2": "la Torre Sagrada de Caelid · el apóstol sacrodermo",
    "p2_3": "la sala del Espadón del exterminador de dioses",
    "p2_4": "Melina",
    "p1_1": "Rogier en la Mesa Redonda · Godwyn muerto (tráiler)",
    "p1_3": "Tiche (blanca) contra Maliketh",
    "p1_4": "las manos de Ranni (tráiler) · final de Ranni · Godwyn",
    "p1_6": "Catacumbas del Cuchillo Negro de Liurnia",
    "p1_8": "la Noche de los Cuchillos Negros: las asesinas apuñalan a Godwyn",
    "p1c_0": "Gurranq muere (estallido blanco)",
    "p1c_1": "el Círculo de Elden se rompe (tráiler)",
    "cierreb_0": "«Witless Tarnished…» (subtítulo del juego)",
    "cierrec_0": "«Forgive me, Marika…» (subtítulo del juego)",
    "cierrec_3": "Leyndell en ceniza",
    "cierrec_4": "Rennala · Rellana · Parches · Gideon",
    "cierrec_5": "Malenia · Radahn · Ranni",
}

MIN_SEP = 9
EQUIV = {}
CINE = {  # mismas cinemáticas y la misma muerte en varias partidas → tiempo M
    "M": [(172, 243, 0), (370, 540, 0)],
    "MV": [(100, 171, 67), (490, 558, -117)],
    "ON": [(65, 131, 110), (260, 327, 114)],
    "LG": [(80, 146, 100), (225, 370, 172)],
    "GS": [(40, 106, 132)],
}
DUR = {"M": 612, "MV": 558, "ON": 326, "LG": 379, "GS": 108, "RG": 443, "GD1": 133, "GM": 100, "DB": 2771, "DT": 1605,
       "DR": 2392, "DS": 508, "P36": 1594, "FA": 6887, "P2F": 7315, "BK1": 456, "BK2": 402, "BK3": 261, "VG1": 289,
       "VG2": 143, "TRN": 229, "BV": 243, "GW": 183, "TM": 59, "RS": 612, "RA": 165, "BKC": 797, "LK": 1661, "JM": 52,
       "P30": 718, "RN": 385, "PE": 87, "GDF": 36, "ME": 1668, "MA": 818, "LR": 619}


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
        if "er_maliketh" in f:
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
