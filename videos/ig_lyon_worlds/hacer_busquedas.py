# -*- coding: utf-8 -*-
"""Escribe busquedas.json: a cada beat de beats.json, un tramo EXACTO de un VOD (url + desde) según la sección del guion.
Los tramos EN VIVO de las jugadas (beat largo sin voz) van al segundo justo de la pelea; los demás rotan por fuentes de la
sección, avanzando el segundo para no repetir plano. python videos/ig_lyon_worlds/hacer_busquedas.py"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))
Y = "https://youtu.be/"
IGHLE, TSWIG, LYTSW, LYGEN1 = "rxkYf8BOHSQ", "mva8OALSadc", "feWyEjzJmKc", "zNTyYcB20Mg"
FUENTES = {
    "gancho": [(IGHLE, 1930), (LYGEN1, 2500), ("7XexqRIbtLU", 5168), (TSWIG, 1812), (LYTSW, 1356), (LYGEN1, 2562)],
    "juego": [("Oix7cBcGmgM", 120), ("Oix7cBcGmgM", 520), ("Oix7cBcGmgM", 900), ("Oix7cBcGmgM", 1300)],
    "ig_historia": [("7XexqRIbtLU", 5100), ("7XexqRIbtLU", 5150), ("7XexqRIbtLU", 5190), ("7XexqRIbtLU", 5230),
                    ("m16dnebeasw", 420), (TSWIG, 640)],
    "ig_camino": [("m16dnebeasw", 900), (TSWIG, 980), (IGHLE, 700), ("m16dnebeasw", 1400)],
    "ig_jugadores": [(IGHLE, 1290), (TSWIG, 1250), (IGHLE, 1530)],
    "lyon_historia": [("uJKrx1BCzwA", 4), ("XJ4eX-j9tMA", 70), ("7Rd52QMrOWI", 8885), ("XJ4eX-j9tMA", 300), ("uJKrx1BCzwA", 40),
                      ("XJ4eX-j9tMA", 520), (LYTSW, 700), ("N157oBk7iGI", 900)],
    "lyon_camino": [(LYTSW, 1700), ("N157oBk7iGI", 1600), (LYGEN1, 1250), ("N157oBk7iGI", 2400)],
    "claves": [("o5HDC3Xp6qY", 600), ("oyEuf2odwdY", 900), ("m16dnebeasw", 1100), (IGHLE, 900), ("o5HDC3Xp6qY", 1200)],
    "cierre": [("VzymjkPh5wk", 400), ("0QU9ZWDhpC0", 700), ("VzymjkPh5wk", 1000), (LYGEN1, 2580), (IGHLE, 2010)],
}
# tramo EN VIVO (beat largo sin voz) de cada jugada: el segundo del VOD donde empieza la pelea
VIVO = {"jugada1": (IGHLE, 1840 + 94), "jugada2": (TSWIG, 1700 + 104), "jugada3": (LYTSW, 1280 + 73),
        "jugada4": (LYGEN1, 2360 + 136)}
# beats del ANÁLISIS: el FX `video` tapa el cuadro entero; el clip de abajo es solo de relleno
RELLENO = {"jugada1": (IGHLE, 1400), "jugada2": (TSWIG, 1400), "jugada3": (LYTSW, 1000), "jugada4": (LYGEN1, 1800)}


def main():
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    beats = json.load(open(os.path.join(D, "beats.json"), encoding="utf-8"))
    esc = [(e["id"], e["t0"], e["t1"], e["frases"][0]["t0"]) for e in tl["escenas"]]
    out, uso, vivos = {}, {}, {}
    for b in beats:
        mid = (b["t0"] + b["t1"]) / 2
        sid, e0, e1, f0 = next((s for s in esc if s[1] <= mid < s[2]), esc[-1])
        if sid in VIVO:
            if b["t0"] < f0 - 1 and sid not in vivos:          # el beat largo previo a la primera frase
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
