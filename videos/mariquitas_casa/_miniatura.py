# -*- coding: utf-8 -*-
"""MINIATURAS para Flow (Imagen · 16:9 · Nano Banana 2.1 · x4 = 0 puntos). Receta nueva (22-oct-2026): una persona
haciendo/viviendo la escena, el bicho grande, un cuarto con color, 1-2 palabras. Escribe flow/miniaturas.json."""
import json
import os

import guion

F = guion.FICHA
H = F["personajes"]["human"]
B = ("a big cartoon orange Asian lady beetle with black spots, a white head with a black M-shaped mark and big round "
     "sleepy eyes")
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "saturated colors, very high contrast and readable at small size, sixteen by nine horizontal, full-bleed, no border, "
        "no frame. ")

P = {
    "scene-901": BASE + f"A cozy living room window in late autumn with orange trees outside. The window frame and curtain are "
                 f"covered with dozens of orange lady beetles. On the right, {H} pulling back the curtain with a shocked "
                 f"face. In the center, large and close to the viewer, {B}, waving. At the top left, huge thick black "
                 "handwritten marker words \"WHY HERE?\" on two short lines with a thin white outline, the word HERE in red. "
                 "Only these two words, spelled exactly, no other text, no numbers, no logos.",
    "scene-902": BASE + f"A cutaway of a cozy house wall in winter showing a hidden space between the walls packed with "
                 f"hundreds of sleeping orange lady beetles in tiny scarves. In front, large and close to the viewer, {B} "
                 f"peeking out of a crack near a window. On the right, {H} holding a mug and staring at it. At the top "
                 "left, huge thick black handwritten marker words \"ALL WINTER?\" on two short lines with a thin white "
                 "outline, the word WINTER in red. Only these two words, spelled exactly, no other text, no numbers, no logos.",
}

if __name__ == "__main__":
    os.makedirs("flow", exist_ok=True)
    json.dump({k: " ".join(v.split()) for k, v in P.items()}, open("flow/miniaturas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("flow/miniaturas.json:", list(P))
