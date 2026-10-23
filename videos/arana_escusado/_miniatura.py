# -*- coding: utf-8 -*-
"""MINIATURAS para Flow (scene-901..902): `python _miniatura.py` escribe flow/miniaturas.json (navegador integrado,
Imagen · 16:9 · Nano Banana 2.1 · x2 = 0 puntos). Receta NUEVA (22-oct-2026, canales/formula/wild_next_door.md):
una persona HACIENDO la acción sobre el bicho, el bicho grande y expresivo, un cuarto con color (no fondo blanco),
1-2 palabras gigantes; nada de mascotas con accesorios de niño en primer plano."""
import json
import os

import guion

F = guion.FICHA
H = F["personajes"]["human"]
SP = ("a big cartoon brown house spider with a round tan abdomen with dark chevrons, eight thin banded legs and two huge "
      "round terrified eyes")
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "saturated colors, a small bathroom with bright light blue tiles at night with warm yellow light, very high "
        "contrast and readable at small size, sixteen by nine horizontal, full-bleed, no border, no frame. ")

P = {
    "scene-901": BASE + f"On the right two thirds, a white porcelain toilet seen from above at an angle with the lid up, "
                 f"the water swirling in a spiral. Inside the bowl, large and close to the viewer, {SP}, clinging to the "
                 f"inside wall just above the swirling water and looking up in panic. On the left edge, {H} pressing the "
                 "silver flush handle down with one finger, half asleep. At the top left, huge thick black handwritten "
                 "marker words \"STILL ALIVE?\" on two short lines with a thin white outline, the word ALIVE in red. Only "
                 "these two words, spelled exactly, no other text, no numbers, no logos.",
    "scene-902": BASE + f"A white porcelain toilet in the center with the water swirling down in a big spiral, and {SP} "
                 "spinning in the whirlpool with its legs flailing, big and close to the viewer. A cartoon hand in a "
                 "green bathrobe sleeve comes in from the right edge pushing the silver flush handle. At the top left, huge "
                 "thick black handwritten marker words \"NOW WHAT?\" on two short lines with a thin white outline, the word "
                 "WHAT in red, with one thick curved black arrow pointing to the spider. Only these two words, spelled "
                 "exactly, no other text, no numbers, no logos.",
}

if __name__ == "__main__":
    os.makedirs("flow", exist_ok=True)
    json.dump({k: " ".join(v.split()) for k, v in P.items()}, open("flow/miniaturas.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("flow/miniaturas.json:", list(P))
