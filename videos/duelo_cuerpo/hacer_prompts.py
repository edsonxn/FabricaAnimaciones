# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) a partir de beats.json: 9 clips combinados (0-91 s) + 65 imágenes. Estilo
«línea blanca + neón»: en cada prompt se nombra QUÉ va en neón amarillo; lo demás es línea blanca sobre negro.
Clips: nada de gargantas apretadas, asfixia ni cuerpos «por dentro» con gente triste (política de Flow, freno_enojo); la
anatomía de los clips va en un maniquí de vidrio o sola, nunca dentro de la señora (estres_cuerpo, nervio_vago).
   python hacer_prompts.py [--lista]"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
SE = F["personajes"]["la señora"]
NEON = "glowing yellow neon"
MANI = "a transparent glass mannequin torso drawn in fine white lines, with a white line-art heart and lungs inside"
BRAIN = "a white line-art human brain seen from the side, drawn in fine engraving lines, no labels"

V = {  # clips combinados (9 x 10 s): (escena A, transición, escena B)
    "scene-001": (f"{SE} in a small home kitchen at night answering an old wall telephone with a curly cord, the telephone receiver {NEON}",
                  "the camera pushes in slowly toward her face, into scene two",
                  f"close-up of {SE} slowly lowering the telephone receiver, a small heart shape {NEON} on her chest sinking gently downward like a falling leaf"),
    "scene-002": (f"{SE} leaning back against the kitchen counter, her knees bending, a small heart shape {NEON} on her chest beating fast, a round wall clock behind her",
                  "the camera pulls back and the kitchen dissolves into darkness, into scene two",
                  f"a white line outline of a human figure standing seen from the front, small sparks {NEON} spreading from the chest to the arms, the legs and the head like a wave"),
    "scene-003": (f"a long winding road drawn in perspective with small stone milestones receding toward the horizon, an old pocket watch lying at the start of the road, the watch hands {NEON}",
                  "the camera flies along the road toward the horizon, into scene two",
                  f"{MANI}; a jagged crack of light {NEON} slowly runs down the middle of the heart"),
    "scene-004": (f"{SE} at sunrise opening the window of her kitchen, a potted plant on the windowsill and a warm cup of tea in her hand, the steam of the tea {NEON}",
                  "the warm light fades into darkness, into scene two",
                  f"{BRAIN}, inside it a small old brass alarm bell ringing, the bell {NEON} with ripples of warning spreading out"),
    "scene-005": (f"two small white line-art kidneys each wearing a tiny gland on top like a little hat, the glands releasing glowing droplets {NEON} into a branching blood vessel",
                  "the droplets flow along the vessel upward, into scene two",
                  f"{MANI}; the heart inside beats fast {NEON} and thin white lines of tense muscle tighten across the shoulders"),
    "scene-006": (f"{SE} sitting on a wooden chair wrapped in her shawl, her hands trembling slightly around a cup, tiny zigzag lines around her, the steam of the cup {NEON}",
                  "the camera pulls back and the room turns into a modern laboratory, into scene two",
                  f"a modern brain scanner machine in a university laboratory, a person lying on the table sliding into it, a small screen above showing a framed photograph {NEON}"),
    "scene-007": (f"{BRAIN}, cut in half to show the inside, a curved band deep in the middle slowly lighting up {NEON}",
                  "the camera pulls back and the brain becomes a window at night, into scene two",
                  f"{SE} standing by a window at night with one hand on her chest, a small heart shape {NEON} under her hand"),
    "scene-008": (f"an old wall clock with a single hand completing one full slow circle, a small sun and a small moon drawn around its face, the clock hand {NEON}",
                  "the camera turns away from the clock into a long hallway, into scene two",
                  f"a long hospital corridor with beds, researchers with clipboards talking with older patients, the clipboard of the nearest researcher {NEON}"),
    "scene-009": (f"a small house at night with a black ribbon bow on the front door and the windows dark, the porch lamp {NEON}",
                  "the camera pushes slowly toward the door, into scene two",
                  f"{MANI}; behind it many small heart outlines lined up in rows like a crowd, the heart inside the mannequin {NEON}"),
}

from _imagenes import I   # lista ordenada, un elemento por beat desde scene-010

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
        print(b["id"][6:], b["texto"][:60], "||", P[b["id"]][len(E):len(E) + 90].replace(SE, "SE"))
