# -*- coding: utf-8 -*-
"""Rellena {CAPITULOS} de videos/<v>/youtube.json con los tiempos reales de timeline.json (inicio de cada escena) y
un título en inglés por escena. Uso: python videos/_capitulos_wnd.py <v>"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TITULOS = {
    "arana_escusado": {"hook": "A spider on the toilet at midnight", "ride": "The biggest water slide on Earth",
                       "float": "Why many spiders don't sink", "sewer": "A long night in the sewer",
                       "coma": "The spiders that came back from the dead", "back": "Can it climb back up?",
                       "home": "The twist: it lived there", "deal": "What to do instead", "outro": "Back to midnight"},
    "mariquitas_casa": {"hook": "Hundreds of beetles on your house", "who": "Not a ladybug: the Asian lady beetle",
                        "choose": "Why they pick your house", "inside": "Inside your walls all winter",
                        "wake": "Why they wake up too early", "defense": "The smell, the stains and the bite",
                        "spring": "What happens in spring", "deal": "How to get them out", "outro": "The snowbird"},
    "chinche_invierno": {"hook": "A stink bug on your sleeve", "who": "Meet the brown marmorated stink bug",
                         "invade": "26,000 bugs in one house", "winter": "The roommate that sleeps all winter",
                         "warm": "Why they wake up on warm days", "smell": "The cilantro smell",
                         "spring": "Spring: where the story turns", "deal": "What to do with it",
                         "outro": "The perfect roommate"},
    "hormigas_cocina": {"hook": "The ant line that always comes back", "trail": "The invisible map",
                        "few": "You only see a tiny part of the colony", "smell": "The rotten coconut test",
                        "split": "Why spraying can make it worse", "dead": "What happens to the ants you squish",
                        "deal": "What actually works", "outro": "Erase the map"},
    "telarana_rota": {"hook": "Back by morning", "all": "Home, fridge and job in one",
                      "drop": "The safety line", "rebuild": "Rebuilding overnight (and eating the old web)",
                      "move": "When a spider gives up and moves", "cobwebs": "The dusty cobwebs secret",
                      "deal": "What to do with a web on your door", "outro": "The tiny builder"},
    "polilla_foco": {"hook": "Moths around your porch light", "myth": "The old moon theory",
                     "trap": "What really happens: the autopilot trap", "night": "A long night at the light",
                     "cost": "Why it matters: the night shift of pollination", "deal": "How to help them",
                     "outro": "Let it find the real sky"},
    "arana_crias": {"hook": "A lumpy spider in the garage", "who": "Meet the wolf spider mom",
                    "ride": "The longest piggyback ride", "squish": "What happens if you squish her",
                    "after": "What happens to the babies", "bite": "Is she dangerous?",
                    "deal": "What to do instead of the boot", "outro": "The whole family goes home"},
}


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


v = sys.argv[1]
d = os.path.join(AQUI, v)
tl = json.load(open(os.path.join(d, "timeline.json"), encoding="utf-8"))
tit = TITULOS[v]
lineas = []
for e in tl["escenas"]:
    i = e.get("id")
    t0 = e.get("t0", e.get("inicio", e.get("ini")))
    if i in tit and t0 is not None:
        lineas.append(f"{mmss(0 if not lineas else t0)} {tit[i]}")
yj = os.path.join(d, "youtube.json")
y = json.load(open(yj, encoding="utf-8"))
y["descripcion"] = y["descripcion"].replace("{CAPITULOS}", "\n".join(lineas))
json.dump(y, open(yj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(lineas))
