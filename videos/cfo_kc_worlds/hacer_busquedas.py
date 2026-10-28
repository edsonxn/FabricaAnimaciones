# -*- coding: utf-8 -*-
"""Escribe busquedas.json: a cada beat de beats.json, un tramo EXACTO de un VOD (url + desde) según la sección del guion.
Los tramos EN VIVO de las jugadas (beat largo sin voz) van al segundo justo de la pelea; los demás rotan por fuentes de la
sección, avanzando el segundo para no repetir plano. python videos/cfo_kc_worlds/hacer_busquedas.py"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))
Y = "https://youtu.be/"
TLCFO, MKCFO, T1CFO = "FATvv4Lk7IU", "sLoG6iB0L2Q", "cmct78Iytg8"
KCAL, KCLY, KCBLG, C9KC, KCMVK = "8txB9yg9FNc", "jToExBjYenQ", "Lo6V52lXc94", "2xC2Jpk_duM", "4uxGpP2TG38"
FUENTES = {
    "gancho": [(TLCFO, 2690), (KCAL, 1815), (T1CFO, 1100), (C9KC, 2780), (TLCFO, 2560), (KCAL, 2340)],
    "juego": [(KCBLG, 600), (MKCFO, 700), (KCLY, 900), (T1CFO, 700)],
    "cfo_historia": [(TLCFO, 600), (MKCFO, 1300), (T1CFO, 1400), (TLCFO, 1200), (MKCFO, 1900)],
    "cfo_camino": [(MKCFO, 2300), (T1CFO, 1700), (TLCFO, 1800), (MKCFO, 1000), (T1CFO, 900)],
    "cfo_jugadores": [(T1CFO, 1090), (TLCFO, 2200), (MKCFO, 1600)],
    "kc_historia": [(KCMVK, 4300), (KCAL, 900), (KCLY, 1500), (KCBLG, 1200), (KCMVK, 4500), (KCAL, 1500)],
    "kc_camino": [(C9KC, 1500), (KCLY, 2000), (KCBLG, 2100), (KCAL, 2000), (KCMVK, 4700), (C9KC, 2200)],
    "kc_jugadores": [(KCBLG, 1800), (KCLY, 1100), (KCAL, 1300)],
    "duelos": [(TLCFO, 1500), (KCAL, 1100), (T1CFO, 1250), (KCBLG, 2300), (MKCFO, 1450), (KCLY, 2400), (TLCFO, 2300)],
    "claves": [(KCLY, 1800), (T1CFO, 2072), (TLCFO, 2540), (C9KC, 2760), (KCBLG, 2500), (MKCFO, 1990)],
    "cierre": [(TLCFO, 2700), (C9KC, 2785), (KCAL, 1822), (T1CFO, 1840)],
}
# tramo EN VIVO (beat largo sin voz) de cada jugada: el segundo del VOD donde empieza
VIVO = {"jugada1": (TLCFO, 2470 + 64), "jugada2": (T1CFO, 2010 + 50), "jugada3": (KCAL, 1750 + 58),
        "jugada4": (C9KC, 2640 + 128)}
# beats del ANÁLISIS: el FX `video` tapa el cuadro entero; el clip de abajo es solo de relleno
RELLENO = {"jugada1": (TLCFO, 2100), "jugada2": (T1CFO, 1500), "jugada3": (KCAL, 1600), "jugada4": (C9KC, 2400),
           "jugada1_rep": (TLCFO, 2150), "jugada2_rep": (T1CFO, 1550), "jugada3_rep": (KCAL, 1650), "jugada4_rep": (C9KC, 2450)}


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
                vivos[sid] = b["id"]
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
    print(len(out), "beats; en vivo:", vivos)


if __name__ == "__main__":
    main()
