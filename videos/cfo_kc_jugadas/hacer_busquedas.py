# -*- coding: utf-8 -*-
"""Escribe busquedas.json: a cada beat de beats.json, un tramo EXACTO de un VOD (url + desde) según la sección del guion.
Los tramos EN VIVO de las jugadas (beat largo sin voz) se piden al VOD y luego se SUSTITUYEN por el corte local de
medios/_fuente (cortar_vivos.py: imagen y narración alineadas, duración exacta del beat; lección 28-oct). Los demás rotan por
momentos de la sección, avanzando el segundo para no repetir plano. SIN SPOILER antes de cada desenlace (el usuario, 28-oct).
G1 = rTVyiDIg-n8 (VOD = HUD + 426) · G2 = irsYoLi62_U (VOD = HUD + 376). python videos/cfo_kc_jugadas/hacer_busquedas.py"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))
Y = "https://youtu.be/"
G1, G2 = "rTVyiDIg-n8", "irsYoLi62_U"
T1CFO, MKCFO = "cmct78Iytg8", "sLoG6iB0L2Q"          # T1 vs CFO y MKOI vs CFO (cfo_kc_worlds)
FUENTES = {
    "gancho": [(G1, 760), (G1, 905), (G1, 2440), (G1, 1700), (G1, 2700)],
    "juego": [(G1, 600), (G2, 520), (G1, 980), (G2, 700)],
    "camino": [(T1CFO, 1100), (MKCFO, 700), (T1CFO, 1700), (MKCFO, 1300), (T1CFO, 2072)],
    "draft1": [(G1, 300), (G1, 330), (G1, 360), (G1, 385)],
    "curva1": [(G1, 1900), (G1, 2600), (G1, 2200)],
    "draft2": [(G2, 290), (G2, 320), (G2, 345)],
    "claves": [(G1, 1800), (G2, 1300), (G1, 2250), (G2, 1050), (G1, 1500)],
    "numeros": [(G2, 1910), (G1, 2810), (G2, 1500), (G1, 1260)],
    "sigue": [(G2, 1925), (G1, 2795), (G2, 1700), (G1, 2000)],
    "cierre": [(G2, 1900), (G1, 2815)],
}
# tramo EN VIVO de cada jugada: (VOD, segundo del VOD donde empieza) = desde de la fuente local + t de inicio
VIVO = {"jugada1": (G1, 865 + 48), "jugada2": (G1, 1680 + 40), "jugada3": (G1, 2396 + 52), "jugada4": (G1, 2720 + 48),
        "jugada5": (G2, 851 + 60), "jugada6": (G2, 1486 + 40), "jugada7": (G2, 1821 + 43)}
# beats del ANÁLISIS: el FX `video` tapa el cuadro entero; el clip de abajo es solo de relleno
RELLENO = {k: (G1 if k[6] in "1234" else G2, s) for k, s in (
    ("jugada1", 1000), ("jugada2", 1400), ("jugada3", 2100), ("jugada4", 2500), ("jugada5", 600), ("jugada6", 1300),
    ("jugada7", 1700), ("jugada2_rep", 1450), ("jugada3_rep", 2150), ("jugada4_rep", 2550), ("jugada5_rep", 650),
    ("jugada6_rep", 1350), ("jugada7_rep", 1750))}


def main():
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    beats = json.load(open(os.path.join(D, "beats.json"), encoding="utf-8"))
    esc = [(e["id"], e["t0"], e["t1"], e["frases"][0]["t0"]) for e in tl["escenas"]]
    out, uso, vivos = {}, {}, {}
    for b in beats:
        mid = (b["t0"] + b["t1"]) / 2
        sid, e0, e1, f0 = next((s for s in esc if s[1] <= mid < s[2]), esc[-1])
        if sid in VIVO or sid in RELLENO:
            if sid in VIVO and b["t0"] < f0 - 1 and sid not in vivos:          # el beat largo previo a la primera frase
                v, s = VIVO[sid]
                vivos[sid] = (b["id"], round(b["t0"], 2), round(b["t1"], 2))
                out[b["id"]] = {"url": Y + v, "desde": s - max(0.0, b["t0"] - e0)}
                continue
            v, s = RELLENO[sid]
            k = uso.get(sid, 0)
            uso[sid] = k + 1
            out[b["id"]] = {"url": Y + v, "desde": s + 25 * k}
            continue
        lista = FUENTES[sid]
        k = uso.get(sid, 0)
        uso[sid] = k + 1
        v, s = lista[k % len(lista)]
        out[b["id"]] = {"url": Y + v, "desde": s + 30 * (k // len(lista))}
    json.dump(out, open(os.path.join(D, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(vivos, open(os.path.join(D, "vivos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats; en vivo:", vivos)


if __name__ == "__main__":
    main()
