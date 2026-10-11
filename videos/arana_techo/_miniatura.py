# -*- coding: utf-8 -*-
"""Lote temporal de MINIATURAS para Flow: escribe flow/escenas.json con scene-901 y scene-902 (imágenes).
Después, `python fab.py arana_techo prompts` restaura el escenas.json del video. Receta del nicho:
dibujo sobre fondo claro, 2-4 palabras manuscritas en inglés entre comillas y flecha curva al sujeto."""
import json
import os

import guion

F = guion.FICHA
A = F["personajes"]["cellar"]
W = F["personajes"]["widow"]
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "colors, clean plain off-white background, very high contrast and readable at small size, sixteen by nine horizontal, "
        "full-bleed, no border, no frame. ")

P = {
    "scene-901": BASE + f"On the right half, big and close: {A}, hanging from the top right corner of the frame by a few silk "
                 f"threads, calmly holding {W} below it, the widow tightly wrapped in white silk strands and looking shocked. "
                 "On the left half, huge thick black handwritten marker words \"NEVER KILL IT\" on three short lines, the "
                 "word KILL in red, with one thick curved black arrow pointing from the words to the pale spider. "
                 "Only these three words, spelled exactly, no other text, no logos.",
    "scene-902": BASE + f"In the upper right corner where two white walls meet the ceiling, {A} hangs proudly in a messy tangled "
                 f"cobweb with a confident smile. Below it, {W} is stuck upside down in the tangle, wrapped in silk, angry and "
                 "helpless. On the left, huge thick black handwritten marker words \"IT HUNTS WIDOWS\" on three short lines, "
                 "with one thick curved black arrow pointing to the pale spider. Only these three words, spelled exactly, "
                 "no other text, no logos.",
}

os.makedirs("flow", exist_ok=True)
json.dump([dict(sceneId=k, prompt=" ".join(v.split()), mediaType="image") for k, v in P.items()],
          open("flow/escenas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("flow/escenas.json: miniaturas", list(P))
