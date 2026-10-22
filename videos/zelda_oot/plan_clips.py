# -*- coding: utf-8 -*-
"""Plan de clips por FRASE de zelda_oot (22-oct-2026): cada frase -> lista de (id de YouTube, segundo) ya MIRADOS en hojas de
contacto propias (previews/_scan/*.jpg, un cuadro cada 15-20 s con el segundo impreso). `python plan_clips.py` escribe
busquedas.json: cada beat toma la siguiente fuente de la frase donde EMPIEZA (si se acaban, repite la última +12 s).
Serie base: ZeldaCentral «Ocarina of Time Switch Online N64 100% Walkthrough» (1080p60, marco gris de NSO a los lados).
"""
import json
import os
import re

P = {1: "N6rM3KhqHIo", 2: "MJxGJpBja_w", 3: "BAnsTh2fHmU", 4: "Q53ffTZRmQk", 11: "FO9OG9QXGS4", 13: "M--gXMSdJxY",
     19: "Iafrj7w_pz8", 21: "r-1CZGBr3hQ", 22: "csFvvR08QFY", 24: "quu9fmNlsGk", 25: "OLY3yMVtNLE", 34: "m29XeXRn-2Y",
     35: "F2Pp2qU3QWI"}
REMAKE, AONUMA = "8v8eDMh1o3g", "PQvD3p2yGwc"
VACA1, VACA2 = "QWSfkKtvW7Q", "ilcZ33Zbgls"
PESCA1, PESCA2, PESCA3 = "ns5BG-zKPYI", "7sXQ12vNm2s", "lEA1iZ6ZHY8"
VENT_HD, VENT_CMP = "MaUCTYb1VtI", "P9uRTESdxAc"
GOSSIP = "x7uGxymMbSs"
SM64, TOEI, DD64, MQ = "a2ADSzJowNc", "r3zr0hoQggU", "TRNtifmbWPM", "IFldCvi-4cY"
MM, WW, TP, ALTTP, Z1 = "DZjrIHXIrIM", "t75ACgMtVgA", "netDXmwuHn0", "uMFUlFiCTbE", "1wwKfKKaDCw"
DS_AGUA, MOLINO = "m3ucPjOjDtk", "PuyZIui07BM"


def p(n, s):
    return (P[n], s)


PLAN = {
    "intro_0": [(REMAKE, 20), (REMAKE, 60)],
    "intro_1": [p(35, 1323), p(1, 33)],
    "intro_2": [p(2, 890), p(3, 558)],
    "intro_3": [(VACA1, 44), p(19, 258), p(25, 423)],
    "intro_4": [p(13, 978), p(22, 63)],
    "origen_0": [(SM64, 300), (SM64, 700)],
    "origen_1": [p(1, 228), p(1, 378)],
    "origen_2": [p(34, 1103), (SM64, 1000), p(34, 1143)],
    "origen_3": [p(2, 978), p(3, 573)],
    "origen_4": [p(2, 333), p(2, 348)],
    "origen_5": [(TOEI, 200), (TOEI, 330)],
    "origen_6": [p(21, 978), p(11, 453), p(34, 1263)],
    "origen_7": [(DD64, 70), p(35, 1338)],
    "origen_8": [p(13, 513), p(13, 528)],
    "origen_9": [p(22, 78), p(22, 1203)],
    "lore_0": [p(1, 378), p(1, 618)],
    "lore_1": [p(1, 168), p(1, 873)],
    "lore_2": [p(2, 603), p(2, 693)],
    "lore_3": [p(3, 18), p(3, 108), p(3, 243)],
    "lore_4": [p(13, 528), p(13, 573), p(13, 643)],
    "lore_5": [p(11, 1053), p(13, 678)],
    "lore_6": [p(13, 978), p(13, 1128), p(25, 93)],
    "lore_7": [p(13, 1023), p(21, 1038), p(13, 1083)],
    "lore_8": [p(35, 603), p(35, 708), p(35, 783)],
    "p12_0": [p(3, 588)],
    "p12_1": [(VACA2, 15), (VACA1, 8)],
    "p12_2": [(VACA2, 50), (VACA1, 30)],
    "p12_3": [p(1, 258), (VACA1, 50)],
    "p12_4": [(VACA2, 80), p(3, 828)],
    "p11_0": [(PESCA2, 30)],
    "p11_1": [(PESCA2, 60), (PESCA1, 5)],
    "p11_2": [(PESCA1, 30), (PESCA2, 200)],
    "p11_3": [(PESCA1, 60), (PESCA3, 100)],
    "p11_4": [(PESCA3, 140), (PESCA2, 280)],
    "p10_0": [p(3, 18)],
    "p10_1": [p(3, 243), p(3, 273)],
    "p10_2": [(VENT_HD, 5), (VENT_CMP, 40)],
    "p10_3": [(VENT_HD, 22), (VENT_CMP, 90)],
    "p10_4": [(VENT_CMP, 170), (VENT_CMP, 200)],
    "p9_0": [(GOSSIP, 3)],
    "p9_1": [(GOSSIP, 12), (GOSSIP, 22)],
    "p9_2": [(GOSSIP, 32)],
    "p9_3": [(GOSSIP, 45), (GOSSIP, 55)],
    "p9_4": [(GOSSIP, 66), (GOSSIP, 75)],
    "p8_0": [p(4, 708)],
    "p8_1": [p(4, 813), p(4, 828)],
    "p8_2": [p(11, 453), p(4, 738)],
    "p8_3": [p(4, 843), p(11, 888)],
    "p8_4": [p(11, 888), p(4, 768)],
    "p7_0": [p(22, 1263)],
    "p7_1": [p(22, 63), p(22, 573)],
    "p7_2": [p(22, 333), p(22, 498), p(22, 633), p(22, 1353)],
    "p7_3": [p(22, 213), p(22, 1428), p(22, 1473)],
    "p7_4": [p(22, 1788), p(22, 1848), p(22, 1053)],
    "p7_5": [p(22, 1893), p(22, 1918)],
    "p6_0": [p(24, 48)],
    "p6_1": [p(24, 333), p(24, 708)],
    "p6_2": [p(24, 213), p(24, 693), p(24, 678)],
    "p6_3": [p(24, 843), p(24, 903), p(24, 1113)],
    "p6_4": [(AONUMA, 30), (AONUMA, 120)],
    "p6_5": [(DS_AGUA, 300), (DS_AGUA, 600)],
    "p5_0": [p(19, 3)],
    "p5_1": [p(19, 168), p(19, 213)],
    "p5_2": [p(19, 258), p(19, 498)],
    "p5_3": [p(34, 1263), p(34, 1483)],
    "p5_4": [p(34, 1343), p(34, 1403)],
    "p5_5": [p(34, 1163), p(35, 228)],
    "p4_0": [(DD64, 30)],
    "p4_1": [(DD64, 110), (DD64, 200)],
    "p4_2": [(DD64, 300), p(35, 1338)],
    "p4_3": [(DD64, 600)],
    "p4_4": [(MM, 200), (MM, 600)],
    "p4_5": [(MQ, 3000), (MQ, 9000)],
    "p3_0": [p(2, 813)],
    "p3_1": [p(2, 828), p(3, 438)],
    "p3_2": [p(3, 453), p(3, 873), p(22, 1848)],
    "p3_3": [p(2, 843), p(3, 888)],
    "p3_4": [p(2, 858), p(3, 468)],
    "p2_0": [(MOLINO, 10)],
    "p2_1": [(MOLINO, 25), (MOLINO, 45), p(25, 408)],
    "p2_2": [(MOLINO, 60)],
    "p2_3": [p(25, 348), p(25, 423), p(25, 468)],
    "p2_4": [p(25, 438), p(25, 483)],
    "p2_5": [p(25, 498), p(25, 393)],
    "p1_0": [p(35, 708)],
    "p1_1": [p(35, 783), p(35, 828)],
    "p1_2": [p(25, 93), p(35, 1248)],
    "p1_3": [p(13, 753), p(13, 783)],
    "p1_4": [(WW, 600), (WW, 1500), (MM, 900), (TP, 120)],
    "p1_5": [(ALTTP, 3000), (Z1, 2000)],
    "p1_6": [p(35, 1158), p(35, 1173)],
    "p1_7": [(REMAKE, 120), (REMAKE, 200)],
    "cierre_0": [(VACA1, 50), (PESCA1, 40), p(19, 303), p(25, 438)],
    "cierre_1": [p(34, 1303), p(21, 1003)],
    "cierre_2": [p(25, 423), p(19, 768)],
    "cierre_3": [p(35, 1323), p(1, 33), p(3, 963)],
}

def _limpio(s):
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", s)).strip().lower()


if __name__ == "__main__":
    import re
    import sys
    aqui = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, aqui)
    import guion
    frases = [(f"{e['id']}_{i}", _limpio(f)) for e in guion.ESCENAS for i, f in enumerate(e["frases"])]
    beats = json.load(open(os.path.join(aqui, "beats.json"), encoding="utf-8"))
    usados, out = {}, {}
    for b in beats:
        cab = _limpio(b["texto"])[:40]
        fid = next((k for k, t in frases if cab and cab in t), None)
        if fid is None:                                    # el beat empieza a mitad de frase: la más parecida
            fid = max(frases, key=lambda kt: sum(w in kt[1] for w in cab.split()))[0]
        lista = PLAN.get(fid) or PLAN[fid.rsplit("_", 1)[0] + "_0"]
        n = usados.get(fid, 0)
        vid, s = lista[n] if n < len(lista) else (lista[-1][0], lista[-1][1] + 12 * (n - len(lista) + 1))
        usados[fid] = n + 1
        out[b["id"]] = {"url": f"https://youtu.be/{vid}", "desde": s}
        print(b["id"], fid, vid, s, round(b["t1"] - b["t0"], 1))
    json.dump(out, open(os.path.join(aqui, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats -> busquedas.json")
