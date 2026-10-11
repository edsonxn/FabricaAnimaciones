# -*- coding: utf-8 -*-
"""Escribe un flow/escenas.json TEMPORAL con los candidatos de miniatura (scene-901..). Después de recibirlos:
`python fab.py teflon_sarten prompts` restaura el escenas.json del video. Manual: Platitube/docs/manual-miniaturas.md."""
import json

BASE = ("Handcrafted claymation style, stop-motion animation aesthetic, textured matte modeling clay, visible subtle clay "
        "fingerprints, detailed miniature set, sixteen by nine horizontal YouTube thumbnail, one single unified shot, no collage, "
        "full-bleed image with no border and no frame. ")
LUZ = ("Detailed miniature clay environment of a nineteen thirties chemistry laboratory with dark wooden benches and glass flasks, "
       "dramatic contrast, subtle cinematic bokeh and depth of field. Cinematic studio rim lighting, high contrast, clean "
       "composition, the bottom-right corner kept dark and empty. ")
TEXTO = ("In the top-left, the words \"¿Y EL GAS?\" appear as three-dimensional letters hand-sculpted entirely out of modeling clay, "
         "with the same tactile stop-motion texture as the rest of the scene, thick chunky uppercase block letters standing "
         "upright like sculpted props, alternating letter by letter between pure bright yellow clay and pure red clay, lit by the "
         "same rim lighting, casting a soft shadow, slight playful tilt. No other text, no logos, no watermark.")
QUIMICO = ("a clay figure of a slim twenty-seven year old nineteen thirties chemist with short dark brown side-parted hair, thick "
           "eyebrows, white lab coat over a white shirt and a dark red tie")

P = {
    "scene-901": f"{BASE}Large in the right two thirds, {QUIMICO}, with exaggerated astonishment, wide eyes and jaw dropped, holding up "
                 "close to the camera the two halves of a small grey steel gas cylinder that has just been sawn in half, its hollow "
                 "inside completely coated with bright white waxy powder that spills out and glows in the light. "
                 f"{LUZ}{TEXTO}",
    "scene-902": f"{BASE}In the center, a small grey steel gas cylinder with a brass valve clamped in an iron bench vise, sawn open "
                 "down the middle, with a bright white glowing waxy powder pouring out of the cut like snow; right behind it, "
                 f"{QUIMICO}, leaning in very close with an exaggerated shocked face, wide eyes and open mouth, still holding a "
                 f"metal hacksaw in one hand. {LUZ}{TEXTO}",
}
json.dump([dict(sceneId=k, prompt=v, mediaType="image") for k, v in P.items()], open("flow/escenas.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(len(P), "candidatos de miniatura en flow/escenas.json")
