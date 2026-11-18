# -*- coding: utf-8 -*-
"""Asigna a cada beat un clip REAL del juego del refugio que se nombra (url + desde), repartiendo los beats de cada puesto a lo
largo del recorrido del video fuente (avanza con la historia). IDs y segundos: fichas «YouTube» de _investigacion_A/B/C.md.
Los puestos sin juego (55/56, 43, 68/69) llevan pasillos reales de un refugio del mismo juego que su recreación de Flow (la
recreación va encima como pant()).        python _clips.py   → busquedas.json
"""
import json

FUENTES = {   # escena: [(id, desde_s, hasta_s)]
    "intro": [("CPQ0BeLKchE", 5, 190), ("4td2SqKyxmI", 4630, 4690)],
    "p25": [("94O3FhAdANQ", 120, 1100)],                         # FO4, pasillos de refugio (recreación encima)
    "p24": [("yoPxWOfP3Sk", 5, 300), ("g-a0oa3a7F8", 60, 900)],   # FNV Refugio 21
    "p23": [("e0c_PI_i9Lk", 40, 2600)],                           # Far Harbor Refugio 118
    "p22": [("RIpspGxJAp0", 300, 900)],                           # FO4 atrio de refugio (recreación de la pantera encima)
    "p21": [("rJefnNa0aa0", 30, 1650), ("7Gu0AqAMVTY", 60, 700)], # Refugio 88
    "p20": [("4td2SqKyxmI", 708, 4500), ("g4TOaT-FAAE", 1290, 1780)],
    "p19": [("63NqNwe1H8Y", 30, 2200)],
    "p18": [("6-j7LGWoeys", 776, 2560)],
    "p17": [("YDcdskMy2h4", 60, 3500)],
    "p16": [("RIpspGxJAp0", 30, 1380), ("wSb--3wF4N4", 500, 870)],
    "p15a": [("q-U95qZzk9U", 5, 540)],
    "p15": [("q-U95qZzk9U", 300, 540)],
    "p14": [("UPfqMC-lJGM", 30, 1200), ("w5j6vsT7XrY", 0, 90)],
    "p13": [("4td2SqKyxmI", 3300, 3900), ("Rd0rCEx1Z9E", 0, 30)],   # FO3 pasillos de refugio + el mono del 77 (el cómic va en pegatinas/recreaciones)
    "p12": [("n3QDzmDqsmI", 120, 5000)],
    "p11": [("4td2SqKyxmI", 1900, 3200)],                         # FO3 pasillos de refugio (recreaciones 68/69 encima)
    "p10": [("QGTlKN9plis", 10, 840)],
    "p9": [("Y9afOYCCvCw", 5, 415), ("k814jGI1fI0", 5, 590)],
    "p8": [("swVjVj1nAuE", 60, 1570), ("74e3kEv1IwI", 4400, 4980)],   # EX8aqou8YHg tenía el juego en RUSO: fuera
    "p7a": [("QHzbAZR1oU8", 2210, 3800)],
    "p7": [("QHzbAZR1oU8", 3100, 4270)],
    "p6": [("x89C9Mzsr9c", 100, 3600)],
    "subs": [("4td2SqKyxmI", 4688, 4716)],   # salida del 101 (el video dura 4718 s: 4720 dejaba los clips vacíos)
    "p5": [("S8_XW-7PMPM", 287, 1500)],
    "p4": [("g4qd0wMX4M8", 20, 690)],
    "p3a": [("Yw-jZvfNuh8", 60, 3400)],
    "p3": [("Xa8Pq3k-BgU", 438, 515)],                            # cámara del sacrificio
    "p2": [("uCzB4nNG098", 10, 730), ("1GuEA4ghUE0", 10, 850)],
    "p1": [("gK4AlHIDd3A", 1858, 5340)],
    "cierre": [("4td2SqKyxmI", 4600, 4700)],
}

beats = json.load(open("beats.json", encoding="utf-8"))
tl = json.load(open("timeline.json", encoding="utf-8"))["escenas"]


def escena_de(t):
    for e in tl:
        if e["t0"] - 1e-6 <= t < e["t1"]:
            return e["id"]
    return tl[-1]["id"]


por = {}
for b in beats:
    por.setdefault(escena_de((b["t0"] + b["t1"]) / 2), []).append(b)
out = {}
for esc, bs in por.items():
    tramos = FUENTES[esc]
    total = sum(h - d for _, d, h in tramos)
    for k, b in enumerate(bs):
        pos = total * k / max(1, len(bs))       # reparto uniforme a lo largo del recorrido
        for vid, d, h in tramos:
            if pos < h - d:
                out[b["id"]] = {"url": "https://youtu.be/" + vid, "desde": round(d + pos, 1)}
                break
            pos -= h - d
FIJOS = {"scene-052": ("4td2SqKyxmI", 760), "scene-102": ("DjvSDpjxz7E", 150), "scene-103": ("DjvSDpjxz7E", 420),
         "scene-104": ("DjvSDpjxz7E", 700), "scene-167": ("Y9afOYCCvCw", 380), "scene-190": ("x89C9Mzsr9c", 160),
         "scene-196": ("x89C9Mzsr9c", 1300), "scene-215": ("g4qd0wMX4M8", 300), "scene-257": ("gK4AlHIDd3A", 2000),
         "scene-255": ("C8pH3Q2xhGg", 60), "scene-174": ("74e3kEv1IwI", 4520)}
for k, (v, d) in FIJOS.items():   # rehechos tras mirar las hojas de medios (negro, menú de pausa, botón de youtuber, otro juego)
    out[k] = {"url": "https://youtu.be/" + v, "desde": d}
out["scene-108"] = {"url": "https://youtu.be/q-U95qZzk9U", "desde": 141.4}   # «Gary» del clon a los 7,2 s, con la voz callada
json.dump(out, open("busquedas.json", "w", encoding="utf-8"), indent=1)
print(len(out), "beats con url+desde;", {e: len(v) for e, v in por.items()})
