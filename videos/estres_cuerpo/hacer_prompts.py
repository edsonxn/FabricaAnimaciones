# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) a partir de beats.json: 7 clips combinados (0-73 s) + 145 imágenes. Estilo
«línea blanca + neón»: en cada prompt se nombra QUÉ va en neón amarillo; lo demás es línea blanca sobre negro.
Clips: nada de gargantas apretadas, asfixia ni cuerpos «por dentro» con gente triste (política de Flow, freno_enojo).
   python hacer_prompts.py"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
CH = F["personajes"]["el chico"]
ANAT = "anatomical illustration drawn in thin white engraving lines, no labels"
SIL = f"a transparent white outline of {CH}, standing, seen from the front"
NERV = "a long branching nerve running from the brain down the neck to the heart, lungs, stomach and intestines"

V = {  # clips combinados (7 x 10 s): (escena A, transición, escena B)
    "scene-001": (f"{CH} standing in a crowded city bus holding the overhead handrail, other passengers around him, his chest outline glowing yellow neon as he breathes fast",
                  "the bus doors open and the camera follows him out onto the street and into an office building, into scene two",
                  f"{CH} sitting at a desk in an open-plan office in front of a meeting room; a small glowing yellow neon knot spins gently in his belly"),
    "scene-002": (f"close-up of {CH} at his computer in the afternoon, rubbing his jaw with one hand, his jaw line glowing yellow neon",
                  "the computer screen turns into a pane of glass and the camera pulls back through it into scene two",
                  f"{CH} standing on a busy sidewalk while the city around him looks flat and far away, as if seen through thick glass; his own hands glow yellow neon"),
    "scene-003": (f"{CH} arriving at a sunny beach with a suitcase, smiling, a beach umbrella behind him",
                  "a big gust of wind blows sand across the frame and clears into scene two",
                  f"{CH} sitting in a beach chair wrapped in a blanket with a red nose, sneezing, a thermometer in his mouth glowing yellow neon"),
    "scene-004": (f"{SIL}; five small spots on his body glow yellow neon: chest, belly, jaw, the top of his head and one hand",
                  "the camera rises along the body up to the head and glides inside the skull into scene two",
                  f"a calm explorer version of {CH} with a flashlight walking along a winding path that is drawn like a map of the human body, the flashlight beam glowing yellow neon"),
    "scene-005": (f"side view of a human head as an {ANAT}; deep in the middle of the brain a small almond-shaped structure glows bright yellow neon",
                  "the almond-shaped structure pulses and the camera zooms into it, becoming scene two",
                  "an old red-painted fire alarm bell mounted on a dark wall, drawn in white lines, ringing with motion lines, the bell glowing yellow neon"),
    "scene-006": (f"{CH} on one side of the frame facing a huge lion drawn in white engraving lines, and on the other side the same young man facing a laptop showing an email icon; both the lion's eyes and the laptop glow yellow neon",
                  "the camera pushes down into his body to two small glands sitting on top of the kidneys, into scene two",
                  f"two small triangular glands sitting on top of two kidneys as an {ANAT}, shooting bright glowing yellow neon sparks upward"),
    "scene-007": (f"{CH} in a sprinter's starting stance on a running track, every muscle outline taut, his heart glowing yellow neon and beating fast",
                  "a second slow wave of light rolls across the frame from left to right and becomes scene two",
                  "a large slow ocean wave made of thin white lines rolling toward a small house, the crest of the wave glowing yellow neon"),
}

from _imagenes import I   # lista ordenada, un elemento por beat desde scene-008

# I va EN ORDEN: una imagen por beat a partir de scene-008 (comprobar con `python hacer_prompts.py --lista`).
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
        print(b["id"][6:], b["texto"][:60], "||", P[b["id"]][len(E):len(E) + 90].replace(CH, "CH").replace(SIL, "SIL"))
