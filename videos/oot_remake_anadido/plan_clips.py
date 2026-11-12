# -*- coding: utf-8 -*-
"""Plan de clips POR BEAT de oot_remake_anadido (11-nov-2026): beat -> (id de YouTube, segundo), mirado en previews/_scan/*.jpg
(_scan.py) o ya verificado en oot_remake_eliminado / zelda_oot. `python plan_clips.py` escribe busquedas.json.
REMAKE: RM100 oLHiQX2wxrE (100 % 4K sin comentario, capítulos), L45 L45cq1H2d1s (cinemáticas GLP), LUN 8nSoklvmLkM (Espada
Maestra y Ganondorf, sin comentario), BOT MOj6mCoK1sE (5.ª botella), OPF opfv1K35uNE (Salón de los Enemigos Caídos), RED
XPvYWutj5ag (ReDead N64 vs Switch 2), VER niOLyw2vhCU (Máscara de la Verdad), SK Go0khcpjGEA (Skull Kid), SCR WLQUuD_9j9s
(Business Scrub, BeardBear), MAN Vh2jiWNbKIk (Mano Muerta), HIE -0cwlyMdre8 (GameSpot, audio fuera), DED d4PifU1Wd7o (ocarina),
VAC Rg8y2Pd1PgA (vacas de Master Quest, audio fuera), BR MUt7wPJIyaE (boss rush), AMI wuFfiTEr2yc (Direct: amiibo),
DIR/OVR/DEMO/KAE = material oficial/4K ya usado. N64: serie ZeldaCentral NSO (marco 0,131). GameCube: MQ EFhB23Z1OWw.
Audio original: 048 = «You're entertaining…» de Ganondorf (LUN 204,3 s tras «Escucha»); 055 = Darunia «I'd be a pile of gravel…»
(L45 12197,3 s tras «Darunia»).
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RM100, L45, LUN, BOT, OPF = "oLHiQX2wxrE", "L45cq1H2d1s", "8nSoklvmLkM", "MOj6mCoK1sE", "opfv1K35uNE"
RED, VER, SK, SCR, MAN, HIE, DED = "XPvYWutj5ag", "niOLyw2vhCU", "Go0khcpjGEA", "WLQUuD_9j9s", "Vh2jiWNbKIk", "-0cwlyMdre8", "d4PifU1Wd7o"
VAC, BR, AMI = "Rg8y2Pd1PgA", "MUt7wPJIyaE", "wuFfiTEr2yc"
DEMO, OVR, DIR, KAE = "PQvD3p2yGwc", "8v8eDMh1o3g", "wuFfiTEr2yc", "4dsfMqNJ_xI"
P01, P02, P11, P13, P22, P35, GOS = "N6rM3KhqHIo", "MJxGJpBja_w", "FO9OG9QXGS4", "M--gXMSdJxY", "csFvvR08QFY", "F2Pp2qU3QWI", "x7uGxymMbSs"
MQ = "EFhB23Z1OWw"
NSO = 0.131

PLAN = {
    1: (SK, 6),   # 2-5,5 s = fundido negro (MASTER 11-nov) 2: (VER, 288), 3: (L45, 10720), 4: (DIR, 7), 5: (OVR, 64), 6: (P01, 27), 7: (KAE, 4), 8: (SK, 10), 9: (DEMO, 548),
    # 12 koroks
    10: (RM100, 430), 11: (RM100, 520), 12: (RM100, 610), 13: (RM100, 700),
    # 11 Link actúa
    14: (P02, 800), 15: (DED, 12), 16: (HIE, 146),
    # 10 ocarina de Saria
    17: (RM100, 1760), 18: (RM100, 1790), 19: (P11, 1190), 20: (RM100, 6360),
    # 9 botella
    21: (BOT, 8), 22: (BOT, 28), 23: (P22, 340), 24: (BOT, 50),
    # 8 semilla del mercader
    25: (SCR, 20), 26: (SCR, 60), 27: (P13, 183), 28: (SCR, 100),
    # 7 ReDeads y Mano Muerta
    29: (RED, 58), 30: (RED, 88), 31: (MAN, 30),
    # crítica 1
    32: (BOT, 0), 33: (RM100, 5745),
    # 6 salón
    34: (OPF, 900), 35: (KAE, 20), 36: (OPF, 540), 37: (OPF, 880), 38: (BR, 60),
    # 5 máscara de la verdad
    39: (VER, 252), 40: (GOS, 20), 41: (VER, 396), 42: (HIE, 423), 43: (VER, 504),
    # crítica 2
    44: (RM100, 5732),
    # 4 Ganondorf
    45: (LUN, 172), 46: (P13, 640), 47: (P13, 690), 48: (LUN, 203.2), 49: (LUN, 215), 50: (LUN, 262), 51: (LUN, 240),
    # 3 sabios
    52: (P35, 605), 53: (P13, 760), 54: (L45, 10720), 55: (L45, 12196.3), 56: (L45, 12206), 57: (L45, 10745),
    # crítica 3
    58: (KAE, 40),
    # 2 Master Quest
    59: (MQ, 30), 60: (MQ, 90), 61: (MQ, 100), 62: (MQ, 150), 63: (MQ, 210),
    # 1 máscara 103
    64: (AMI, 30), 65: (AMI, 60), 66: (VER, 576), 67: (VER, 648), 68: (SK, 40), 69: (SK, 100),
    # cierre
    70: (RM100, 6390), 71: (DIR, 31), 72: (DEMO, 560), 73: (KAE, 4),
}
RECORTE = {k: NSO for k in (6, 14, 19, 23, 27, 46, 47, 52, 53)}
RECORTE.update({59: 0.125, 60: 0.125, 62: 0.125, 63: 0.125})   # MQ GameCube 4:3
AMBIENTE = {48: 0.9, 55: 0.9}

if __name__ == "__main__":
    out = {f"scene-{n:03d}": {"url": f"https://youtu.be/{v}", "desde": s} for n, (v, s) in sorted(PLAN.items())}
    assert len(out) == 73, len(out)
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats -> busquedas.json")
    print("recorte_por =", {f"scene-{k:03d}": v for k, v in sorted(RECORTE.items())})
    print("ambiente_por =", {f"scene-{k:03d}": v for k, v in sorted(AMBIENTE.items())})
