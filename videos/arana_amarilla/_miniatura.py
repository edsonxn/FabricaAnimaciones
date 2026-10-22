# -*- coding: utf-8 -*-
"""MINIATURAS para Flow (scene-901..902): `python _miniatura.py` escribe flow/miniaturas.json (se escriben en el navegador
integrado, Imagen · 16:9 · Nano Banana 2.1 · x2 = 0 puntos). Receta del nicho (docs/manual_wild_next_door.md): dibujo sobre
fondo claro, 2-4 palabras manuscritas en inglés entre comillas, flecha curva al sujeto y un elemento de amenaza."""
import json
import os

import guion

F = guion.FICHA
G = F["personajes"]["garden"]
WEB = F["objeto"]
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "colors, clean plain off-white background, very high contrast and readable at small size, sixteen by nine horizontal, "
        "full-bleed, no border, no frame. ")

P = {
    "scene-901": BASE + f"On the right half of the frame, big and close to the viewer, {G}, hanging head down in the center "
                 f"of {WEB}, looking straight out of the picture with a worried face. A giant cartoon wooden stick held by a "
                 "hand comes in from the top edge, raised and about to swat the web, with a few motion lines. On the left, "
                 "huge thick black handwritten marker words \"DON'T KILL HER\" on three short lines, the word KILL in red, "
                 "with one thick curved black arrow pointing from the words to the spider. Only these three words, spelled "
                 "exactly, no other text, no numbers, no logos.",
    "scene-902": BASE + f"On the right half of the frame, big and close to the viewer, {G}, hanging head down in the center "
                 f"of {WEB}, raising two legs in fear. A giant cartoon bug spray can held by a hand comes in from the "
                 "bottom right corner, nozzle pointed at the spider, its label completely blank. On the left, huge thick "
                 "black handwritten marker words \"DON'T SPRAY HER\" on three short lines, the word SPRAY in red, with one "
                 "thick curved black arrow pointing from the words to the spider. Only these three words, spelled exactly, "
                 "no other text, no numbers, no logos.",
}

if __name__ == "__main__":
    os.makedirs("flow", exist_ok=True)
    json.dump({k: " ".join(v.split()) for k, v in P.items()}, open("flow/miniaturas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("flow/miniaturas.json:", list(P))
