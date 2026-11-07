# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena (add-on funcionando en los videos con minuto de
videos/_investigacion_wow_addons_forever.md) con {"url","desde"}; lo que no tiene video = búsqueda genérica.
Las escenas casa* NO se bajan: sus clips salen de las grabaciones propias de OBS (_obs.py). 7-nov-2026."""
import json
import os
import re
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
import guion  # noqa: E402

BEL = "https://youtu.be/1GEmk7Fci2E"
WDA = "https://www.youtube.com/watch?v=xAGUIPWAS1I"
BBG = "https://www.youtube.com/watch?v=ep4GfiFXae8"
TOP = "https://www.youtube.com/watch?v=pzaHB-pB5MU"
SCO = "https://www.youtube.com/watch?v=8fyZKPy6wpE"
KEL = "https://www.youtube.com/watch?v=E3GHdyJiHzk"
G, NC = "WoW Forever gameplay", "WoW Forever no commentary"

SRC = {
    "intro": [["WoW Forever launch day", G], (BEL, 40), (WDA, 12), ["WoW Forever trailer", G], (KEL, 40), [NC], ["Stormwind no commentary"]],
    "serie": [(WDA, 26), (WDA, 38), (WDA, 46)],
    "c20": [(WDA, 78), (KEL, 300), (KEL, 312), (WDA, 90), (KEL, 324), (KEL, 336)],
    "c19": [["WoW Forever professions", "classic professions crafting"], ["WoW Forever merchant favor", "WoW Forever recipes"],
            ["classic crafting leveling", "blacksmithing classic"], ["WoW Forever recipes", "classic professions trainer"],
            [G], [NC], ["Stormwind no commentary"], ["Ironforge no commentary"]],
    "c18": [(SCO, 360), (SCO, 391), (SCO, 405), (SCO, 419), (SCO, 375), (SCO, 432)],
    "inm": [["Elwynn Forest no commentary"], ["Goldshire classic no commentary"], ["Northshire Abbey no commentary"]],
    "c17": [(BBG, 219), (BBG, 227), (BBG, 235), ["Elwynn Forest no commentary"], (BBG, 243), (BBG, 211)],
    "c16": [(BEL, 240), (BEL, 252), (BBG, 161), (BEL, 264), (KEL, 390), (KEL, 402), (BEL, 300)],
    "c15": [(BEL, 1095), (BEL, 1107), (WDA, 121), (BEL, 1119), (KEL, 450), (KEL, 462), (TOP, 40)],
    "c14": [["Barrens no commentary"], ["Westfall no commentary"], ["Loch Modan no commentary"], ["Duskwood no commentary"],
            ["Barrens classic no commentary"], ["Redridge Mountains no commentary"]],
    "c13": [(TOP, 142), (TOP, 156), (BBG, 269), (TOP, 172), (BBG, 281), (TOP, 190), (TOP, 206)],
    "gracias1": [["Stormwind no commentary"], [NC], ["Goldshire classic no commentary"], ["Ironforge no commentary"]],
    "c12": [["WoW Forever campfire", "campfire classic"], ["WoW Forever camp", "WoW Forever campfire"], ["campfire classic", "WoW Forever camp"],
            ["WoW Forever camp tent", "WoW Forever camp"], ["classic camping", "WoW Forever campfire"]],
    "c11": [(BEL, 960), (BEL, 972), (BEL, 984), ["mining herbalism classic", "herbalism classic"], (BEL, 996), (WDA, 101)],
    "burla1": [[G], [NC], ["Elwynn Forest no commentary"]],
    "c10": [(WDA, 284), (SCO, 781), (SCO, 793), ["Deadmines classic", "dungeon classic no commentary"], (SCO, 805), (WDA, 292),
            ["Wailing Caverns classic"], [NC]],
    "c09": [(BEL, 211), (BEL, 220), ["classic quest turn in", G], (BEL, 229), ["classic questing no commentary"], [NC]],
    "overgear": [["WoW Forever dungeon", "dungeon classic no commentary"], ["Deadmines classic"], ["Wailing Caverns classic"],
                 ["dungeon classic no commentary"], ["Shadowfang Keep classic"], [G], [NC]],
    "c08": [(BEL, 815), (BEL, 827), (KEL, 30), (KEL, 42), (KEL, 54), (BEL, 839), ["class trainer classic"]],
    "c07": [(KEL, 660), (KEL, 672), (KEL, 600), (KEL, 684), (BEL, 865), (BEL, 877)],
    "gracias2": [[G], [NC]],
    "c06": [(BEL, 652), (BEL, 664), (BBG, 110), (BEL, 676), (BBG, 122), (BEL, 688)],
    "c05": [(BEL, 121), (BEL, 133), (WDA, 164), (WDA, 176), (BBG, 366), (BBG, 378), (BEL, 145)],
    "c04": [(BEL, 705), (BEL, 717), (KEL, 1080), (KEL, 1092), (BEL, 729)],
    "c03": [(SCO, 90), (SCO, 120), (SCO, 150), (SCO, 180), (WDA, 304), (SCO, 240), (SCO, 300)],
    "c02": [(WDA, 201), (BBG, 247), (KEL, 930), (KEL, 942), (BBG, 259), (WDA, 213)],
    "c01": [(WDA, 53), (BEL, 912), (BEL, 924), (KEL, 90), (KEL, 102), (BEL, 936), (BEL, 948), (KEL, 114)],
    "cierre": [["Stormwind no commentary"], ["Elwynn Forest no commentary"], ["Goldshire classic no commentary"], [G], ["Stormwind sunset classic"]],
}


def _norm(s):
    s = re.sub(r"\[[^\]]+\]", " ", s)
    return re.sub(r"[^a-záéíóúñü0-9]+", " ", s.lower()).strip()


FRASES = [(e["id"], _norm(f)) for e in guion.ESCENAS for f in e["frases"]]


def escena_de(texto):
    t = _norm(texto)
    for eid, f in FRASES:
        if f[:40] and f[:40] in t:
            return eid
    for eid, f in FRASES:   # el beat empieza a mitad de una frase
        if t[:30] and t[:30] in f:
            return eid
    return None


if __name__ == "__main__":
    b = json.load(open("beats.json", encoding="utf-8"))
    out, cuenta, casa = {}, {}, []
    for x in b:
        eid = escena_de(x.get("texto", "")) or (out and list(cuenta)[-1]) or "intro"
        x["_esc"] = eid
        if eid.startswith("casa"):
            casa.append((x["id"], eid))
            out[x["id"]] = [G]          # marcador: el clip lo pone _obs.py antes de `bajar`
            cuenta[eid] = cuenta.get(eid, 0) + 1
            continue
        lst = SRC[eid]
        n = cuenta.get(eid, 0)
        cuenta[eid] = n + 1
        e = lst[n % len(lst)]
        if isinstance(e, tuple):
            url, desde = e
            out[x["id"]] = {"url": url, "desde": float(desde + 25 * (n // len(lst)))}
        else:
            out[x["id"]] = e
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({x["id"]: x["_esc"] for x in b}, open("_beat_escena.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(out), "beats ·", ", ".join(f"{k}:{v}" for k, v in cuenta.items()))
    print("casa (OBS):", casa)
