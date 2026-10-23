# -*- coding: utf-8 -*-
"""Prompts de MINIATURA (A y B) de los videos 3-7 de la tanda de Wild Next Door (22-oct-2026). Receta nueva: una persona
haciendo la acción, el bicho grande y expresivo, un cuarto con color, 1-2 palabras gigantes. Flow: Imagen · 16:9 ·
Nano Banana 2.1 · x4 = 0 puntos. Escribe videos/<v>/flow/miniaturas.json. Uso: python videos/_miniaturas_wnd.py"""
import importlib.util
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "saturated colors, very high contrast and readable at small size, sixteen by nine horizontal, full-bleed, no border, "
        "no frame. ")


def texto(palabras, roja):
    return (f"At the top left, huge thick black handwritten marker words \"{palabras}\" on two short lines with a thin white "
            f"outline, the word {roja} in red. Only these words, spelled exactly, no other text, no numbers, no logos.")


def ficha(v):
    sp = importlib.util.spec_from_file_location("g_" + v, os.path.join(AQUI, v, "guion.py"))
    g = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(g)
    return g.FICHA["personajes"]


P = {}
H = ficha("chinche_invierno")["human"]
B = "a big cartoon brown shield-shaped stink bug with white bands on its antennae and big sleepy eyes"
P["chinche_invierno"] = {
    "scene-901": BASE + f"A cozy living room at night by a glowing reading lamp. {H} sitting in an armchair, looking down "
                 f"in surprise at {B} resting on his flannel sleeve, big and close to the viewer. " + texto("LET IT LIVE?", "LIVE"),
    "scene-902": BASE + f"A snowy window at night seen from inside a warm living room. {B} sleeping on the windowsill under "
                 f"a tiny blanket, big and close to the viewer, while {H} peeks at it with a mug. " + texto("ALL WINTER?", "WINTER"),
}
H = ficha("hormigas_cocina")["human"]
A = "a line of cartoon dark brown ants marching across a kitchen counter to a sugar bowl"
P["hormigas_cocina"] = {
    "scene-901": BASE + f"A bright kitchen counter. A giant human thumb from {H} is about to squish {A}; the closest ant, "
                 "big and close to the viewer, looks up at the thumb with huge eyes. Behind the wall, a cutaway shows a huge "
                 "hidden ant colony with thousands of ants and a queen. " + texto("MORE COMING", "MORE"),
    "scene-902": BASE + f"A kitchen counter with a sugar bowl and {A}. {H} in a yellow apron and pink rubber gloves aims a "
                 "spray can with a blank label at them, while a crack in the wall shows three new ant nests splitting off. "
                 + texto("DON'T SPRAY", "SPRAY"),
}
H = ficha("telarana_rota")["human"]
S = "a big cartoon gray-brown porch spider with a plump abdomen, hairy banded legs and big expressive eyes"
P["telarana_rota"] = {
    "scene-901": BASE + f"A front porch at night under a glowing porch light. {H} swinging a broom through a round spider "
                 f"web, threads flying, while {S} dangles on a single silk thread in the foreground, big and close to the "
                 "viewer, looking annoyed. " + texto("NOW WHAT?", "WHAT"),
    "scene-902": BASE + f"A front porch at sunrise: a perfect new round spider web glistening with dew exactly where it was, "
                 f"{S} sitting proudly in the center, big and close to the viewer, while {H} stares at it in disbelief "
                 "holding a broom. " + texto("BACK ALREADY?", "BACK"),
}
H = ficha("polilla_foco")["human"]
M = "a big fluffy cartoon tan moth with soft patterned wings, feathery antennae and dizzy spiral eyes"
P["polilla_foco"] = {
    "scene-901": BASE + f"A glowing white porch light on a house wall at night. {M} flying in a dizzy circle around the "
                 "light with curved motion lines, big and close to the viewer, other moths circling behind. "
                 f"{H} at the door looking up. " + texto("TRAPPED?", "TRAPPED"),
    "scene-902": BASE + f"A porch light at night, and {M} upside down next to the bulb with a confused face, big and close "
                 f"to the viewer, a tiny broken compass beside it. {H} reaching for the light switch. " + texto("NOT LOVE", "NOT"),
}
H = ficha("arana_crias")["human"]
W = ("a big cartoon brown wolf spider mother with a fuzzy striped body and a tiny pink bandana, dozens of tiny pale baby "
     "spiders piled on her back")
P["arana_crias"] = {
    "scene-901": BASE + f"A garage floor at night under a bare light bulb. A giant work boot of {H} hovering above {W}, "
                 "big and close to the viewer; the babies look up at the boot with huge eyes. " + texto("WAIT!", "WAIT"),
    "scene-902": BASE + f"A garage floor: {W}, big and close to the viewer, carrying her babies like a crowded school bus, "
                 f"while {H} lowers a bucket gently over her. " + texto("DON'T STOMP", "STOMP"),
}

if __name__ == "__main__":
    for v, d in P.items():
        os.makedirs(os.path.join(AQUI, v, "flow"), exist_ok=True)
        json.dump({k: " ".join(t.split()) for k, t in d.items()},
                  open(os.path.join(AQUI, v, "flow", "miniaturas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    lista = [" ".join(t.split()) for d in P.values() for t in d.values()]
    json.dump(lista, open(os.path.join(AQUI, "_miniaturas_wnd.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(len(lista), "prompts:", ", ".join(f"{v} A/B" for v in P))
