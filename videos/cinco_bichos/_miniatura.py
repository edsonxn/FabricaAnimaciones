# -*- coding: utf-8 -*-
"""Lote temporal de MINIATURAS para Flow: escribe flow/escenas.json con scene-901..903 (imágenes).
Después, `python fab.py cinco_bichos prompts` restaura el escenas.json del video. Receta del nicho:
dibujo sobre fondo claro, 2-4 palabras manuscritas en inglés entre comillas y flecha curva al sujeto."""
import json
import os

import guion

F = guion.FICHA["personajes"]
M, WO, EA, J, D = F["mantis"], F["wolf"], F["earwig"], F["jumper"], F["dauber"]
BASE = ("YouTube thumbnail, hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright "
        "colors, clean plain off-white background, very high contrast and readable at small size, sixteen by nine horizontal, "
        "full-bleed, no border, no frame. ")

P = {
    "scene-901": BASE + f"On the right two thirds of the frame, three friendly cartoon bugs sit side by side on a white window "
                 f"sill: in the middle, big and close to the viewer, {J}, looking straight out of the picture; on its left "
                 f"{M}; on its right {WO}. A giant cartoon red flyswatter hovers threateningly above them. On the left, huge "
                 "thick black handwritten marker words \"NEVER KILL THESE\" on three short lines, the word KILL in red, with "
                 "one thick curved black arrow pointing from the words to the middle spider. Only these three words, "
                 "spelled exactly, no other text, no numbers, no logos.",
    "scene-902": BASE + f"In the lower right, three friendly cartoon bugs huddle together looking up with worried faces: in the "
                 f"middle {J}, on its left {D}, on its right {EA}. Directly above them, a giant cartoon sneaker sole is about "
                 "to stomp down, with a few motion lines. On the left, huge thick black handwritten marker words \"DON'T "
                 "SQUISH THEM\" on three short lines, the word SQUISH in red, with one thick curved black arrow pointing "
                 "from the words to the bugs. Only these three words, spelled exactly, no other text, no logos.",
    "scene-903": BASE + f"On the left, a gigantic hand-drawn red number \"5\" with a thick black outline filling the left third of "
                 f"the frame, and below it the handwritten black marker words \"NEVER KILL\" on two lines. On the right, five "
                 f"small friendly cartoon bugs in a row looking at the viewer: {M}, {WO}, {EA}, {J} and {D}, with a thick "
                 "curved black arrow pointing to them from the number. Only the number five and the words NEVER KILL, "
                 "spelled exactly, no other text, no logos.",
}

os.makedirs("flow", exist_ok=True)
json.dump([dict(sceneId=k, prompt=" ".join(v.split()), mediaType="image") for k, v in P.items()],
          open("flow/escenas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("flow/escenas.json: miniaturas", list(P))
