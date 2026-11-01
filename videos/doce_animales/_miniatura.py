# -*- coding: utf-8 -*-
"""MINIATURAS para Flow (scene-901..903): `python _miniatura.py` imprime los prompts (se pegan en el navegador integrado,
Imagen · 16:9 · x1). Receta del nicho (docs/manual_wild_next_door.md): dibujo sobre fondo claro, 2-4 palabras manuscritas en
inglés entre comillas, flecha curva al sujeto y un elemento de amenaza (la pala del gancho)."""
import json
import os

import guion

F = guion.FICHA["personajes"]
PO, TO, SN, BA, LI = F["possum"], F["toad"], F["snake"], F["bat"], F["lizard"]
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "colors, clean plain off-white background, very high contrast and readable at small size, sixteen by nine horizontal, "
        "full-bleed, no border, no frame. ")

P = {
    "scene-901": BASE + f"On the right half of the frame, big and close to the viewer, {PO}, standing on its hind legs and "
                 "looking straight out of the picture with a worried face. Above it, a giant cartoon metal garden shovel "
                 "is raised, about to come down, with a few motion lines. On the left, huge thick black handwritten marker "
                 "words \"DON'T KILL HIM\" on three short lines, the word KILL in red, with one thick curved black arrow "
                 "pointing from the words to the opossum. Only these three words, spelled exactly, no other text, no "
                 "numbers, no logos.",
    "scene-902": BASE + f"In the lower right, five friendly cartoon backyard animals huddle together looking up with worried "
                 f"faces: in the middle and biggest {PO}; around it {TO}, {SN}, {BA} and {LI}. Directly above them, a "
                 "giant cartoon metal garden shovel is about to come down, with a few motion lines. On the left, huge "
                 "thick black handwritten marker words \"NEVER KILL THESE\" on three short lines, the word KILL in red, "
                 "with one thick curved black arrow pointing from the words to the animals. Only these three words, "
                 "spelled exactly, no other text, no logos.",
    "scene-903": BASE + f"On the left, a gigantic hand-drawn red number \"12\" with a thick black outline filling the left "
                 "third of the frame, and below it the handwritten black marker words \"NEVER KILL\" on two lines. On the "
                 f"right, five friendly cartoon backyard animals in a row looking at the viewer: {PO}, {TO}, {SN}, {BA} "
                 f"and {LI}, with a thick curved black arrow pointing to them from the number. Only the number twelve "
                 "and the words NEVER KILL, spelled exactly, no other text, no logos.",
}

if __name__ == "__main__":
    os.makedirs("flow", exist_ok=True)
    json.dump({k: " ".join(v.split()) for k, v in P.items()}, open("flow/miniaturas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("flow/miniaturas.json:", list(P))
