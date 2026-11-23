# -*- coding: utf-8 -*-
"""Asigna a cada beat un clip REAL del juego del enemigo que se nombra (url + desde), repartido a lo largo de los tramos buenos
de cada fuente. Tramos elegidos mirando las hojas `previews/_ref_<id>.jpg` (23-nov): fuera Pip-Boy, menús, tarjetas de
título/suscripción, textos de youtuber y overlays.        python _clips.py   → busquedas.json
"""
import json

FUENTES = {   # escena: [(id, desde_s, hasta_s)]
    "intro": [("5N66OjAJOIE", 25, 45)],
    "p15": [("vuJ1zMph02I", 140, 170), ("dVJ-hXV5bMI", 60, 75), ("vuJ1zMph02I", 80, 100), ("dVJ-hXV5bMI", 296, 350)],   # FO3 hormigas de fuego / Marigold
    "p14": [("do1na2zU5T4", 5, 190), ("2T-UG1aCQe0", 40, 70), ("2T-UG1aCQe0", 215, 230)],
    "p13": [("MIhAHBTbu1U", 150, 300), ("MIhAHBTbu1U", 400, 440), ("L-r8Mv8jqW0", 55, 90)],
    "p12": [("1rW8dHtS2qM", 36, 75), ("jeYfArHD6Ms", 140, 150), ("jeYfArHD6Ms", 270, 340), ("jeYfArHD6Ms", 515, 530)],
    "p11": [("E8hX1JMjGMM", 24, 62), ("E8hX1JMjGMM", 76, 95), ("OAeR7uEqvBc", 40, 50), ("OAeR7uEqvBc", 75, 135), ("sFEK5tktCfs", 415, 425)],
    "p10": [("H44w-CUjNWM", 0, 42), ("Gccv--zasTk", 3, 98), ("w-FRA-nDiqo", 119, 210)],
    "p9": [("iDmX5UZsaCg", 15, 50), ("G8yoty09p3Y", 600, 650), ("iDmX5UZsaCg", 84, 98)],
    "p8": [("7bxQXSiELNA", 50, 135), ("KZP98bx-P_8", 72, 112), ("7bxQXSiELNA", 540, 560)],
    "p7a": [("1-QfUHtSjYs", 26, 40)],
    "p7": [("1-QfUHtSjYs", 40, 66), ("hYSpqXhfjcA", 75, 175), ("1-QfUHtSjYs", 110, 150)],
    "p6": [("zzFJ5GTZV0E", 6, 85), ("pV3ivAo1jEA", 230, 750)],
    "p5": [("aoUnFsc-oPw", 23, 48), ("_ohQaZST530", 2, 60)],   # iiUheoD8-cc solo 480p: bajar lo rechaza
    "subs": [("pV3ivAo1jEA", 20, 30), ("pV3ivAo1jEA", 830, 890)],
    "p4": [("RgJvfn6InIc", 2, 60), ("9OKbOKYDrhE", 30, 60), ("9OKbOKYDrhE", 90, 130), ("g7Bv3ObZD3A", 8, 240)],
    "p3": [("utMrEAQJFUI", 10, 95), ("utMrEAQJFUI", 118, 330), ("utMrEAQJFUI", 335, 435), ("exUxJk8vCB4", 20, 42)],
    "p2": [("1lnmR31LJb0", 20, 84), ("1lnmR31LJb0", 112, 192), ("Vsu_NSN07qQ", 0, 125), ("1lnmR31LJb0", 210, 250)],
    "p1": [("5N66OjAJOIE", 13, 50), ("5N66OjAJOIE", 72, 100), ("4E3julOqGkI", 20, 66)],
    "cierre": [("OAeR7uEqvBc", 90, 120)],
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
        pos = total * k / max(1, len(bs))
        for vid, d, h in tramos:
            if pos < h - d:
                out[b["id"]] = {"url": "https://youtu.be/" + vid, "desde": round(d + pos, 1)}
                break
            pos -= h - d
# beats con el momento exacto que nombra la voz (escenas importantes, 23-nov)
FIJOS = {"scene-001": ("5N66OjAJOIE", 25), "scene-002": ("H44w-CUjNWM", 28), "scene-003": ("jeYfArHD6Ms", 278),
         "scene-004": ("L-r8Mv8jqW0", 60), "scene-005": ("4E3julOqGkI", 42),
         "scene-022": ("L-r8Mv8jqW0", 70), "scene-054": ("7bxQXSiELNA", 578), "scene-055": ("7bxQXSiELNA", 545),
         "scene-059": ("1-QfUHtSjYs", 42), "scene-060": ("hYSpqXhfjcA", 78), "scene-061": ("1-QfUHtSjYs", 114),
         "scene-062": ("1-QfUHtSjYs", 130), "scene-063": ("hYSpqXhfjcA", 133),
         "scene-008": ("vuJ1zMph02I", 151), "scene-046": ("iDmX5UZsaCg", 37), "scene-047": ("iDmX5UZsaCg", 17),
         "scene-056": ("7bxQXSiELNA", 120), "scene-063": ("1-QfUHtSjYs", 140), "scene-089": ("utMrEAQJFUI", 150),
         "scene-090": ("1lnmR31LJb0", 40), "scene-096": ("5N66OjAJOIE", 30),   # tras mirar previews/medios_*.jpg: negro, subtítulos, blanco, texto de youtuber, pantalla de carga
         "scene-040": ("H44w-CUjNWM", 8), "scene-041": ("w-FRA-nDiqo", 140), "scene-048": ("iDmX5UZsaCg", 86),
         "scene-050": ("vuJ1zMph02I", 212), "scene-054": ("7bxQXSiELNA", 100), "scene-049": ("vuJ1zMph02I", 240), "scene-092": ("1lnmR31LJb0", 120),
         "scene-094": ("Vsu_NSN07qQ", 92),   # chequeo OCR 23-nov: subtítulos del juego en inglés fuera
         "scene-104": ("OAeR7uEqvBc", 95), "scene-105": ("1-QfUHtSjYs", 46), "scene-106": ("jeYfArHD6Ms", 516),
         "scene-107": ("5N66OjAJOIE", 36)}
for k, (v, d) in FIJOS.items():
    out[k] = {"url": "https://youtu.be/" + v, "desde": d}
json.dump(out, open("busquedas.json", "w", encoding="utf-8"), indent=1)
print(len(out), "beats con url+desde;", {e: len(v) for e, v in por.items()})
