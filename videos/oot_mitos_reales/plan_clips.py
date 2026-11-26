# -*- coding: utf-8 -*-
"""Plan de clips POR BEAT de oot_mitos_reales (26-nov-2026): beat -> (id de YouTube, segundo), sacado de clips_catalogo.md
(agente, ~150 clips mirados en previews/_scan/*.jpg) y de previews/_scan/mm_epona.jpg. `python plan_clips.py` escribe busquedas.json
e imprime recorte_por / ambiente_por para guion.SECUENCIA.
71 = «Escucha»: el canto de la versión 1.0 (VENGE 80-87 s, comprobado con Whisper + Demucs por el agente) con la voz callada.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RM100, L45, KAE, DEMO = "oLHiQX2wxrE", "L45cq1H2d1s", "4dsfMqNJ_xI", "PQvD3p2yGwc"
ENB, XOQ = "ENBFiQ9u9oI", "XOQVzWFc-ww"
P01, P02, P03, P04, P11, P13 = "N6rM3KhqHIo", "MJxGJpBja_w", "BAnsTh2fHmU", "Q53ffTZRmQk", "FO9OG9QXGS4", "M--gXMSdJxY"
P22, P25, LP = "csFvvR08QFY", "OLY3yMVtNLE", "GmxkUNP-Xv0"
MQ, SEEDY, ECK, MKH = "EFhB23Z1OWw", "TUHI4Hdd7ZM", "L4KGvhidTVs", "b-ztcKpKe-Y"
EA, SW, BCA, DYKG, GS, GOS, VGZ = "rAQv-H-lqEg", "IqTz8bI_dS4", "yeEwafQrBuk", "xNkVrMBLh94", "ZbmIjimU9e0", "x7uGxymMbSs", "VgZgYI0DUCY"
PMZ, ZYS, NAE = "pMzN9Y5LnW4", "zysBRevyjEI", "NaEeWMV_f_E"
GDQ, BS, SD, VENGE, DW = "PNbkv_DJ0f0", "HD1N0OUS8HI", "DEAoR_GS540", "VjEP27ub2iw", "2x_pqyrf9lA"
MMP23, MMP01 = "rZSgjaL77QQ", "7xAeJ9DY1Fw"
NSO = 0.131

PLAN = {   # 76 beats (26-nov, tras quitar la escena de la votación de voz; antes 79: previews/_plan_clips_79.py)
    # intro / contexto
    1: (P01, 26), 2: (KAE, 40), 3: (L45, 138), 4: (P13, 1728), 5: (DEMO, 620), 6: (P13, 515),
    # 12 locha
    7: (SEEDY, 24), 8: (ECK, 143), 9: (SEEDY, 96), 10: (MKH, 48),
    # 11 cucos
    11: (P04, 295), 12: (ENB, 77), 13: (ENB, 86), 14: (ENB, 548),
    # 10 Epona (falso)
    15: (P03, 818), 16: (RM100, 10440), 17: (P13, 1410), 18: (MMP23, 222),
    # 9 corredor
    19: (RM100, 25344), 20: (EA, 99), 21: (EA, 150), 22: (RM100, 25360),
    # com1 gracias
    23: (KAE, 30), 24: (RM100, 26643),
    # 8 Stalchildren
    25: (P03, 967), 26: (SW, 392), 27: (BCA, 22), 28: (SW, 402),
    # 7 Ura Zelda
    29: (GS, 60), 30: (GS, 126), 31: (DYKG, 852), 32: (MQ, 84), 33: (MMP01, 166),
    # 6 búho = Rauru
    34: (KAE, 60), 35: (P02, 947), 36: (GOS, 15), 37: (L45, 8558), 38: (P02, 960),
    # com2 granja del puente
    39: (P11, 1265), 40: (P11, 1283), 41: (VGZ, 22), 42: (RM100, 4727),
    # 5 Templo de las Sombras
    43: (LP, 46955), 44: (P25, 611), 45: (LP, 47004), 46: (P25, 740), 47: (P25, 765), 48: (XOQ, 2885),
    # 4 Fado / Grog
    49: (P22, 150), 50: (P22, 511), 51: (P22, 158), 52: (RM100, 43632), 53: (RM100, 43260),
    # 3 sangre / media luna
    54: (ZYS, 24), 55: (ZYS, 9), 56: (PMZ, 10), 57: (MQ, 192), 58: (P04, 950),
    # 2 Trifuerza
    59: (P13, 600), 60: (BS, 506), 61: (BS, 516), 62: (GDQ, 2846), 63: (DW, 2862), 64: (GDQ, 2868), 65: (BS, 538),
    # 1 canto del Templo del Fuego
    66: (VENGE, 0), 67: (VENGE, 40), 68: (VENGE, 80), 69: (RM100, 37451), 70: (VENGE, 132), 71: (RM100, 26538), 72: (NAE, 186),
    # cierre
    73: (P03, 1000), 74: (DEMO, 628), 75: (ENB, 556), 76: (P11, 1295),
}
_NSO_IDS = {P01, P02, P03, P04, P11, P13, P22, P25, LP, MMP23, MMP01}
RECORTE = {k: NSO for k, (v, s) in PLAN.items() if v in _NSO_IDS}
RECORTE.update({k: 0.125 for k in (8, 12, 13, 32, 57)})   # 4:3 con bandas: ECK, ENB/XOQ N64, MQ GameCube
RECORTE.update({k: (0.03, 0.02, 0.03, 0.17) for k in (26, 28)})          # SwankyBox: marco naranja y su logo abajo
RECORTE.update({k: (0.375, 0.165, 0.01, 0.215) for k in (62, 63, 64)})   # GDQ: solo la ventana del juego
RECORTE.update({k: (0.0, 0.135, 0.0, 0.135) for k in (54, 55, 56)})   # Censored Gaming: franjas negras de 13,3 % arriba y abajo (medidas)
AMBIENTE = {68: 0.95}   # el canto se OYE (la OST se aparta y la voz está callada en el post de p1)

if __name__ == "__main__":
    out = {f"scene-{n:03d}": {"url": f"https://youtu.be/{v}", "desde": s} for n, (v, s) in sorted(PLAN.items())}
    assert len(out) == 76, len(out)
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats -> busquedas.json")
    print("recorte_por =", {f"scene-{k:03d}": v for k, v in sorted(RECORTE.items())})
    print("ambiente_por =", {f"scene-{k:03d}": v for k, v in sorted(AMBIENTE.items())})
