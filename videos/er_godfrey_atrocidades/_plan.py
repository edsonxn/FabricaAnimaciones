# -*- coding: utf-8 -*-
"""Plan de clips POR FRASE (19-nov-2026), hecho mirando hojas de contacto a 240p de cada fuente
(E:\\FabricaAnimaciones\\_tmp_hojas_godfrey\\h\\*.jpg: una hoja por fuente + hojas finas de los momentos exactos;
v\\v_NN.jpg = comprobación final de TODAS las opciones, 3 cuadros por clip a +0,5 / +4,3 / +8,1 s). Escribe plan_frases.json
(lo lee asignar_clips.py).
    python _plan.py
Fuentes limpias: SourceSpy91 4K sin comentarios (HUD normal: P6/P8/P20/P35/P37/P38/P47/P49/P50/SK), JustGamesBruh y ONGBAL
sin HUD (JG/ON, el combate de Godfrey completo), Draknalor186 (LD, solo las 2 cinemáticas, con subtítulos pequeños del
juego), Leomega sin HUD (LGf/LGs/LL/LGd/LFg/LMg/LMo/LMq/LGo/LR/LA, imagen algo lavada), BonfireVN intro (BV) y el modelo
de Serosh (BS), Games from Mars (GR, ecos de Márika con Melina, subtítulos del juego).
Ojo:
 - Marcas/rótulos: RT (Reckless Tommy) tiene rótulos de su canal a 0-12, 18-21 y 186-189 s y SUBSCRIBE al final (usar 95-180);
   MO tiene el MAPA a los 2 s (usar >= 22); LL/LGs/LGd/LFg/LMg/LMq/LMo/LGo/LR empiezan con el MAPA o la niebla (0-6 s) y
   acaban con «ENEMY FELLED» (no pasar del final); GS enseña un menú en el segundo 0; P6 2585-2590 y P8 2535-2565 / 2804-2848
   son menús; P20 588 y P37 4620 tienen un aviso de objeto de ~1 s; GR tiene el mapa a 382, 436, 480, 798, 832, 864 y menús a
   434, 478, 910 (los tramos elegidos caen entre medias). Shirrako, Fextralife, PowerPyx, IGN, Doms Roundtable: NO usados.
 - GR lleva un CONTADOR DE FPS verde diminuto arriba a la derecha (recortar o tapar con la ficha).
 - El jefe de P37 1620-1730 que parecía un trol con arma dorada es el «Erdtree Avatar» (comprobado en captura HD): descartado.
   No encontré un clip limpio de un trol con la Espada dorada de trol ni del monumento «trolls betray»: p2b_3..p2b_6 usan el
   trol picapiedras (ST) y piden PEGATINA del icono de la Espada dorada de trol.
 - El Sinluz de Leomega en LGo (Godrick) parece ir casi sin ropa: solo se usan sus cinemáticas (276, 300).
 - OW (plano fijo de los Picos) quedó FUERA: el mismo plano en varias frases.
 - Sin HUD: JG, ON, LD, BV, BS, GR (cinemáticas), Leomega. Con HUD normal del juego: SourceSpy91, RG, PE, MO, RT.
 - LD/GR/P35 636/P9 llevan SUBTÍTULOS DEL JUEGO en inglés (diálogos); BV, subtítulos pequeños del juego en la intro.
 - BS 20-77 es el VISOR DE MODELOS del juego (Serosh sobre fondo negro): solo de 2.ª opción.
 - OW es un plano FIJO de 4 min (niebla que se mueve): cuidado con freezedetect, mejor de 2.ª opción.
 - LD/JG/ON/P50/LGf/BS graban la MISMA cinemática: además de >= 20 s dentro de cada vídeo, este script pasa cada opción a
   «tiempo LD» (JG −27/−74, ON −1/−90, P50 −508/−827,5, LGf −10/−108, BS +108) y avisa si dos frases distintas enseñan el
   mismo momento (< 9 s). Repeticiones queridas: p1b_4 (preparación, el grito a +7,5 s) / p1c_0 (el grito y el rugido) y p1b_0
   (Serosh se materializa) / p1b_1 (le agarra la cabeza, 1 s de solape).
 - p2_8 (no p2_7) es la frase de los cadáveres empalados según el guion actual; p2_7 es la de los caballeros de Zamor.

MOMENTOS EXACTOS comprobados en hoja (segundos de la fuente):
 - Morgott muerto en el trono → llega Godfrey (fantasma dorado con Serosh) y se arrodilla: LD 0-30 (cadáver 0-12, Godfrey 13,
   arrodillado 18-30) = JG +27 = ON +1 = P50 +508.
 - Serosh translúcido se vuelve de carne: LD 113,5-119,5 (destellos 117-119) = JG +74 = ON +90 = P50 +827 = BS 0-15.
 - Godfrey le agarra la cabeza: LD 120-124; cara de Serosh ya corpórea 124,5-129; NEGRO (el crujido) 129,5-132;
   Serosh ensangrentado 132,5-135,5; Godfrey bañado en sangre 136-137,5; mancha de sangre 138-145; negro 145,5-151.
 - «I've given thee courtesy enough»: LD 164-169 (de espaldas arrancándose la armadura 164-172).
 - «Now I fight as Hoarah Loux! Warrior!»: LD 189,5-197,5 (puñetazos 190-194, rugido con los brazos abiertos 195,5-199,5)
   = JG 263,5-272 (negro a 273) = ON 279-288 (combate 291) = P50 1017-1025.
 - Muerte de Hoarah Loux: P50 1204-1218 (se arrodilla 1212-1214, se deshace 1214-1217, «LEGEND FELLED» 1221-1225);
   JG 358-369 («Thy strength befits a crown» JG 364-372 por Whisper; LEGEND FELLED 374).
 - Ecos de Márika (GR): Tercera iglesia 384-433 · Iglesia de la peregrinación 440-477 · Primera iglesia 866-909.
 - Hoarah Loux en la intro: BV 147-152 (fogonazo blanco 141-147; Máscara dorada desde 153). «Arise now, ye Tarnished» BV 125-128.
 - Monumento de Morne con su texto en pantalla: MO 22-45 · P6 117-130 (texto 126-129).
 - Retrato de Godfrey y Serosh en la sala del Vástago (Velo Tormentoso): P8 2831-2840 (2838: aviso de objeto).
 - Cadáveres de gigantes atravesados por estacas: P37 4614-4619 (vista del campo) y 4621-4645 (el Sinluz trepa por uno).
 - Forja de los gigantes (caldero en llamas, sin nadie): GR 1012-1020.

TRAMOS DE AUDIO del juego (voces solo en INGLÉS; medidos con faster-whisper medium.en + envolvente RMS en 300-3400 Hz):
 (a) «It's been a long while, Morgott.» (Godfrey, entrada en el Trono de Elden):
     https://youtu.be/LhXGJMZ1kpY  15.4 → 21.5 s   («It's» ~15,6 · «long while» 18,6-19,7 · silencio −60 dB 19,8-20,5 ·
     «Morgott» 20,55-21,25). Sin música encima: solo el ambiente de la sala; antes de 15,4 suena el «whoosh» de la aparición.
     Mismo audio: https://youtu.be/4doIpyiGKgQ 17.0 → 23.1 (ON = LD +1,6) · https://youtu.be/XMCh2vAi_Yc 42.6 → 48.6.
     Cortado → sfx/s_morgott.mp3 (6,1 s, −18 LUFS, fundidos 0,15 s; Whisper sobre el corte: «It's been a long while, Morgoth»).
 (b) «Now I fight as Hoarah Loux! … Warrior!»:
     https://youtu.be/LhXGJMZ1kpY  189.9 → 198.0 s   («Now» 190,2 · «Hoarah Loux» 192,1-193,4 · «WARRIOR!» 195,8-197,5;
     la cola de reverberación muere en 198,0; el vídeo acaba en 200,4). Debajo hay el rugido/ambiente de la cinemática (~−25 dB).
     Mismo audio: https://youtu.be/XMCh2vAi_Yc 259.4 → 268.9 · https://youtu.be/4doIpyiGKgQ (cinemática 2, ~279-288).
     Cortado → sfx/s_hoarah.mp3 (8,1 s, −18,6 LUFS integrado, fundidos 0,15 s; Whisper: «Now I fight … horror loom! | WARRIOR!»).
"""
import json
import os

F = {  # alias: (id, nota)
    # --- combate de Godfrey (cinemáticas y fases) ---
    "LD": ("LhXGJMZ1kpY", "Draknalor186: las 2 cinemáticas de Godfrey (Morgott muerto, Serosh, Hoarah Loux); subtítulos del juego pequeños"),
    "JG": ("XMCh2vAi_Yc", "JustGamesBruh 4K sin HUD: Godfrey/Hoarah Loux completo (cinem. 25-136 y 177-273, fases 136-177 y 273-372)"),
    "ON": ("4doIpyiGKgQ", "ONGBAL sin HUD: Godfrey/Hoarah Loux completo (cinem. 0-111 y 196-289, fases 111-196 y 289-366)"),
    "P50": ("rTz4PyJYphw", "SS91 Part 50: capital cinérea (342-500), Godfrey (cinem. 510-618 y 936-1026), muerte 1204-1220"),
    "LGf": ("E7LBpBZbO_A", "Leomega 4K: Godfrey y Hoarah Loux en la capital cinérea (imagen lavada)"),
    "LGs": ("5cUBWqUPbeQ", "Leomega sin HUD: Godfrey, sombra dorada (Leyndell)"),
    "BS": ("iHsyQ25oGfk", "BonfireVN: Serosh se materializa (0-15) y visor de modelos de Serosh (20-77)"),
    "BV": ("7BnZhJg91RQ", "BonfireVN, intro 4K (Hoarah Loux 145-152; «Arise now» 123-141)"),
    "GR": ("GRH4LNXKQt8", "Games from Mars: ecos de Márika con Melina (Tercera iglesia, Peregrinación, Primera iglesia) y la Forja"),
    # --- Velo Tormentoso, Morne, Caelid ---
    "P8": ("vjgNUcwhopI", "SS91 Part 8: Castillo de Velo Tormentoso (rótulo 9-12; retrato de Godfrey 2831-2840)"),
    "LGo": ("gNNFokXwZrY", "Leomega sin HUD: Godrick en Velo Tormentoso (cinemática del brazo de dragón 270-318)"),
    "MO": ("eQurI1KRErE", "Jason's Video Games Source: monumento del asedio de Morne con su texto (mapa a los 2 s)"),
    "P6": ("IkesCV_PYwI", "SS91 Part 6: Península del Llanto, monumento 117-130, Castillo de Morne, Bastardo leonino 2360-2565"),
    "LL": ("h_Zhwo5_xqA", "Leomega sin HUD: Bastardo leonino con el Espadón de hoja injertada (imagen lavada)"),
    "P20": ("nr2eazM_cNc", "SS91 Part 20: Caelid (rótulo 85), Iglesia en llamas ardiendo 575-608"),
    "LA": ("ovizSst8mBs", "Leomega sin HUD: Iglesia en llamas por dentro (58-72)"),
    "PE": ("rBjIP8O9HQ8", "Games Walkthrough 4K: Península del Llanto y rótulo «Church of Pilgrimage» (214)"),
    # --- Leyndell, hijos ---
    "P35": ("L4zVRGHc1yQ", "SS91 Part 35: Leyndell, tronos blancos (156-180), Morgott (cinem. 192-228, muerte 606-654, subtítulos)"),
    "LMg": ("dxyVbyZmTjY", "Leomega sin HUD: Morgott (cinem. 10-95, combate 100-370, muerte 375-405)"),
    "LMo": ("3h5IIdRbqGc", "Leomega sin HUD: Mohg y el capullo de Miquella (cinem. 12-110)"),
    "LMq": ("Mqi-s6M7xw8", "Leomega sin HUD: Mohg, el Augurio, en la catedral del Subsuelo"),
    "P49": ("QjakOuLJlpw", "SS91 Part 49: Subsuelo de los marginados (rótulo 120), cloacas, augurios"),
    "TB": ("bTtDqzGXoac", "Attila Bódi 4K: Leyndell, capital del Reino (imagen lavada)"),
    "LK": ("gKUiD8bSF2o", "LK 4K sin HUD: Meseta Altus, hierba y bosques dorados"),
    "P9": ("Huip3TdEOdU", "SS91 Part 9: Mesa Redonda (2050-2300)"),
    # --- gigantes ---
    "P37": ("gZ2QB9EO6K4", "SS91 Part 37: Picos de los gigantes (rótulo 1499, Ruinas de Zamor 1562, cadáveres empalados 4614-4645)"),
    "OW": ("XQfEYqYuzg8", "Old World Radio 2: Picos de los gigantes, plano FIJO con niebla (4 min)"),
    "P38": ("-q7O-BrN5Jg", "SS91 Part 38: Gigante de fuego (HUD)"),
    "LFg": ("ZnHanZyCR9w", "Leomega sin HUD: Gigante de fuego (cinem. del ojo 220-270)"),
    "ST": ("pGSYVs16qK4", "Leomega sin HUD: trol picapiedras (Túnel de Altus); NO lleva la Espada dorada de trol"),
    "RT": ("DJw2WTrxBXI", "Reckless Tommy 4K: Antiguo héroe de Zamor (rótulos del canal a 0-12, 18-21, 186-189: usar 95-180)"),
    # --- Serosh, Godefroy, Gurranq, Radahn, Farum Azula, DLC ---
    "LGd": ("TZiz2oUhSOM", "Leomega sin HUD: Godefroy el Injertado en su prisión eterna (Meseta Altus)"),
    "GS": ("SpT5r_I2VYU", "4KGameScape sin HUD: Gurranq (clérigo bestia) se transforma (36-62); menú en el s 0"),
    "RG": ("c5mltemiLdA", "ryurain: Gurranq en el Santuario bestial (HUD, subtítulos del juego, baja resolución)"),
    "LG": ("qyi-SaN0VyQ", "Leomega 4K: clérigo bestia (Gurranq) y Maliketh (imagen grisácea)"),
    "LR": ("8D_h_1cNz28", "Leomega sin HUD: Castillo Melena Roja (6-60) y Radahn con su armadura leonina (66-125)"),
    "P47": ("7oet6D34udo", "SS91 Part 47: Farum Azula, arena del Señor dragón Placidusax (cinem. 102-150; rótulo 600)"),
    "SK": ("6u3CMnhBSGA", "SS91 Shadow of the Erdtree Part 9: Fortaleza sombría (rótulo «Shadow Keep» 85)"),
}

P = {
    "intro_0": "JG 96, LGs 57, P50 582",
    "intro_1": "P50 640, LGf 196",
    "intro_2": "P6 420, LFg 160, P49 640",
    "intro_3": "ON 141, JG 150, P50 720",
    "intro_4": "LK 120, TB 84",
    "intro_5": "LGs 102, P50 1080",
    "intro_6": "LMo 24, LK 1130",
    "intro_7": "LMo 48, LK 600",
    "p5_0": "P8 6, P8 390",
    "p5_1": "P8 231, P8 75",
    "p5_2": "BV 23, P50 800, LGf 140",
    "p5_3": "P8 255, P8 120",
    "p5_4": "P8 2826, P50 860",
    "p5_5": "P8 1362, P8 141, P8 1962",
    "p5_6": "P8 285, LGs 80",
    "p5b_0": "P6 225, P6 141",
    "p5b_1": "MO 22, P6 117",
    "p5b_2": "P6 2440, P6 300",
    "p5b_3": "LL 22, P6 2395",
    "p5b_4": "P6 340, LL 60",
    "p5b_5": "LL 88, P6 2500",
    "p5b_6": "ON 99, LGs 123",
    "p5b_7": "P20 596, P20 85, LA 58",
    "p5b_8": "JG 330, ON 320",
    "p5b_9": "LK 430, LK 880",
    "p4_0": "LK 1060, P37 4470",
    "p4_1": "P37 1562, P8 1384",
    "p4_2": "GR 386",
    "p4_3": "GR 410, BV 45",
    "p4_4": "ON 300, LGf 350",
    "p4_5": "LGs 144, P50 680",
    "p4_6": "LR 30, LR 6",
    "p4b_0": "PE 212, PE 186",
    "p4b_1": "GR 441, GR 462",
    "p4b_2": "LGs 198, P38 330",
    "p4b_3": "P6 1965, P6 2050",
    "p4b_4": "P50 1040, JG 300",
    "p4b_5": "BV 147, BV 126",
    "p4b_6": "P8 30, P6 2598",
    "p4b_7": "LK 760, LK 1180",
    "p4b_8": "P50 342, LK 1020",
    "p3_0": "P35 196, LMg 30",
    "p3_1": "LMg 88, LMo 72",
    "p3_2": "P49 1010, LMq 24",
    "p3_3": "P49 118, P49 340",
    "p3_4": "P49 400, P49 720",
    "p3_5": "LMg 112, LMo 100",
    "p3_6": "P49 870, P49 1280",
    "p3_7": "P35 158, P49 1700, LMq 70",
    "p3b_0": "TB 2, P35 12",
    "p3b_1": "P49 1180, LGs 15",
    "p3b_2": "LMg 140, P35 216",
    "p3b_3": "P35 330, LMg 190",
    "p3b_4": "LMo 140, LMq 115",
    "p3b_5": "LD 2, JG 28, ON 3",
    "p3c_0": "JG 50, ON 24",
    "p3c_1": "LMg 400, P35 636",
    "p3c_2": "P49 1556, P49 1250",
    "p3c_3": "P47 126, P47 602",
    "p3c_4": "LK 950, P50 486",
    "p2_0": "LFg 330, P37 4446",
    "p2_1": "P37 1595, OW 30",
    "p2_2": "GR 866",
    "p2_3": "GR 890",
    "p2_4": "LFg 130, P38 125",
    "p2_5": "LFg 228, P38 180",
    "p2_6": "P37 1430, P37 1520",
    "p2_7": "RT 100, RT 130",
    "p2_8": "P37 4614, P37 4636",
    "p2b_0": "LFg 22, P38 100",
    "p2b_1": "GR 1012, LFg 260",
    "p2b_2": "LFg 480, GR 1054",
    "p2b_3": "ST 20, P37 1540",
    "p2b_4": "ST 44",
    "p2b_5": "ST 68",
    "p2b_6": "ST 92",
    "subs_0": "LK 1320, TB 44",
    "subs_1": "P50 384, LK 1420",
    "subs_2": "LK 1560, P9 2278",
    "subs_3": "LK 1350, LK 200",
    "p1_0": "LGf 23, P50 521",
    "p1_1": "P50 840, ON 165",
    "p1_2": "JG 75, BS 66",
    "p1_3": "P50 820, ON 185",
    "p1_4": "LGd 21, LGd 120",
    "p1_5": "GS 38, RG 260, LG 76",
    "p1_6": "LR 84, LR 300",
    "p1_7": "P50 760, LGf 176",
    "p1_8": "P50 541, LD 34",
    "p1b_0": "LD 112, BS 2",
    "p1b_1": "JG 193, ON 210",
    "p1b_2": "LD 133, P50 958",
    "p1b_3": "LD 160, JG 236",
    "p1b_4": "JG 256, LD 182",
    "p1c_0": "ON 280, P50 1020",
    "p1c_1": "ON 345, P50 1100",
    "p1c_2": "LK 1250, TB 24",
    "p1c_3": "P50 920, LGf 330",
    "p1c_4": "P50 1205, JG 358",
    "p1c_5": "P50 1226, LGs 170",
    "cierre_0": "P8 170, P6 360, LFg 400, P50 1060",
    "cierre_1": "LGo 276, BV 78",
    "cierre_2": "LGo 300, P50 900",
    "cierre_3": "SK 85, SK 320, SK 540",
    "cierre_4": "LK 1500, TB 64",
    "cierre_5": "BV 104, LR 400, LMo 180, LMg 300",
    "cierre_6": "LK 1620, LK 1460",
    "cierre_7": "BS 24, P50 880",
}

NOTAS = {  # nota específica del momento (se añade a la de la fuente)
    "p3b_5": "Morgott muerto en el trono; Godfrey aparece a +11 s y se arrodilla a +16 s",
    "p3c_0": "Godfrey arrodillado junto al cadáver de Morgott",
    "p1b_0": "Serosh translúcido se vuelve de carne (destellos a +5 s)",
    "p1b_1": "Godfrey agarra la cabeza de Serosh; cara corpórea; negro del crujido al final",
    "p1b_2": "Serosh ensangrentado tras el crujido y la mancha de sangre",
    "p1b_3": "«courtesy enough»: Hoarah de espaldas arrancándose la armadura",
    "p1b_4": "el grito «Now I fight as Hoarah Loux» sale a +7,5 s",
    "p1c_0": "rugido de Hoarah Loux y fase 2",
    "p1c_4": "Hoarah Loux cae, se arrodilla y se deshace",
    "p4_2": "eco de Márika en la Tercera iglesia (Melina)",
    "p4_3": "eco de Márika en la Tercera iglesia (Melina)",
    "p4b_1": "eco de Márika en la Iglesia de la peregrinación",
    "p2_2": "eco de Márika en la Primera iglesia",
    "p2_3": "eco de Márika en la Primera iglesia",
    "p4b_5": "Hoarah Loux en la intro / «Arise now, ye Tarnished»",
    "p5b_1": "monumento del asedio de Morne con su inscripción",
    "p5_4": "retrato de Godfrey y Serosh en la sala del Vástago",
    "p2_8": "cadáveres de gigantes atravesados por estacas",
}

MIN_SEP = 20


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


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    out = opciones()
    json.dump(out, open("plan_frases.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    usos = [(o["url"][-11:], o["desde"], k) for k, ops in out.items() for o in ops]
    choques = [(a, b) for i, a in enumerate(usos) for b in usos[i + 1:]
               if a[0] == b[0] and a[2] != b[2] and abs(a[1] - b[1]) < MIN_SEP]
    for a, b in choques:
        print("  MISMO PLANO:", a, b)
    R = {"LD": [(0, 201, 0)], "JG": [(25, 136, -27), (177, 273, -74)], "ON": [(0, 111, -1), (196, 289, -90)],
         "P50": [(510, 618, -508), (936, 1026, -827.5)], "LGf": [(12, 120, -10), (216, 310, -108)], "BS": [(0, 15, 108)]}
    eq = sorted((s_ + off, k, a) for k, v in P.items() for a, s_ in ((t.split()[0], int(t.split()[1])) for t in v.split(","))
                for a0, b0, off in R.get(a, []) if a0 <= s_ < b0)
    for i, x in enumerate(eq):
        for y in eq[i + 1:]:
            if y[0] - x[0] >= 9:
                break
            if x[1] != y[1] and {x[1], y[1]} not in ({"p1b_4", "p1c_0"}, {"p1b_0", "p1b_1"}):
                print("  MISMA CINEMÁTICA:", x, y)
    import guion
    claves = [f"{e['id']}_{i}" for e in guion.ESCENAS for i in range(len(e["frases"]))]
    print(len(out), "frases con plan; faltan:", [c for c in claves if c not in out], "sobran:", [c for c in out if c not in claves])
