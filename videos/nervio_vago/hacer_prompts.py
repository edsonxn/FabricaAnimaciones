# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) a partir de beats.json: 7 clips combinados (0-69 s) + 113 imágenes. Estilo
«línea blanca + neón»: en cada prompt se nombra QUÉ va en neón amarillo; lo demás es línea blanca sobre negro.
Clips: nada de gargantas apretadas, asfixia ni cuerpos «por dentro» con gente triste (política de Flow, freno_enojo); la
anatomía de los clips 6-7 va en un busto/maniquí de vidrio, no en una persona (estres_cuerpo: la cabeza anatómica se rechazó).
   python hacer_prompts.py [--lista]"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
CH = F["personajes"]["la chica"]
NEON = "glowing yellow neon"
BUST = "a classical marble bust of a young person seen in profile, drawn in fine white engraving lines"
MANI = "a transparent glass mannequin torso drawn in fine white lines, with a white line-art heart, lungs, stomach and intestines inside"

V = {  # clips combinados (7 x 10 s): (escena A, transición, escena B)
    "scene-001": (f"{CH} standing at a wooden lectern on the stage of a school auditorium, facing rows of seated audience, a small heart shape {NEON} floating above her head and beating fast",
                  "the camera pushes in slowly toward her hands on the lectern, into scene two",
                  f"close-up of the hands of {CH} holding paper notes that tremble slightly, tiny drops of sweat on her fingers {NEON}"),
    "scene-002": (f"a friendly classmate in the front row leaning forward and whispering to {CH} at the lectern, a soft swirl of breath between them {NEON}",
                  "the swirl of breath stretches into a long glowing cable and the camera follows it, into scene two",
                  f"{CH} raising one eyebrow with a skeptical smile while a long cable {NEON} slowly lights up along her transparent outline, from her head down to her belly"),
    "scene-003": (f"a white line-art outline of a young person seen from the side, standing calmly, one thin line {NEON} running from the back of the head down to the belly, a small heart beside it beating slowly",
                  "the camera pulls back and the figure shrinks into the screen of a smartphone held in a hand, into scene two",
                  f"a smartphone held in a hand, on its screen a big round magic button {NEON} surrounded by sparkles and tiny floating heart icons"),
    "scene-004": (f"a large old magnifying glass gliding over a white line-art map of a human figure, the rim of the magnifying glass {NEON}",
                  "the lens fills the frame and dissolves into a night sky with a crescent moon, into scene two",
                  f"an elderly 1920s scientist with round spectacles and a white moustache asleep in an old bed, a dream cloud above him {NEON} with two small frog hearts inside"),
    "scene-005": (f"five simple objects in a row on a wooden shelf: a feather, a folded towel, a microphone, a running shoe and a teacup, the shelf edge {NEON}",
                  "the camera tilts up from the shelf onto an old explorer's map pinned on the wall, into scene two",
                  f"an old explorer's map drawn in white lines showing the outline of a human body like a country, with mountains and rivers, a dotted route starting at the back of the head {NEON}"),
    "scene-006": (f"{BUST}; at the base of the skull, at the back of the neck, a small point of light {NEON} begins to glow",
                  "the camera slowly tilts down along the neck of the bust, into scene two",
                  f"{BUST}; a thin line {NEON} descends from the base of the skull down the side of the neck beside a large vessel, branching like a river delta"),
    "scene-007": (f"{MANI}; a thin glowing line {NEON} winds around the heart like a vine and enters the lungs",
                  "the camera follows the glowing line downward inside the glass torso, into scene two",
                  f"{MANI}; the same glowing line {NEON} wraps around the stomach, the liver and the coiled intestines like a vine"),
}

from _imagenes import I   # lista ordenada, un elemento por beat desde scene-008

beats = json.load(open("beats.json", encoding="utf-8"))
beats = beats["beats"] if isinstance(beats, dict) else beats
P = {}
for b in beats:
    k = b["id"]
    if k in V:
        a, tr, c = V[k]
        P[k] = f"{E}Scene one, first five seconds: {a}. Then {tr}. Scene two, last five seconds: {c}.{C}"
    else:
        P[k] = f"{E}{I[len(P) - len(V)]}.{C}"
assert len(P) == len(beats) == len(I) + len(V), (len(P), len(beats), len(I), len(V))
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(P), "prompts")
import sys
if "--lista" in sys.argv:
    for b in beats:
        print(b["id"][6:], b["texto"][:60], "||", P[b["id"]][len(E):len(E) + 90].replace(CH, "CH"))
