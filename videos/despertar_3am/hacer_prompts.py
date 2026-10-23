# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) a partir de beats.json: 9 clips combinados (0-91 s) + 61 imágenes. Estilo
«línea blanca + neón»: en cada prompt se nombra QUÉ va en neón amarillo; lo demás es línea blanca sobre negro.
Clips: nada de gargantas apretadas, asfixia ni cuerpos «por dentro» con gente triste (política de Flow, freno_enojo); la
anatomía de los clips va en un maniquí de vidrio o sola, nunca dentro del señor (estres_cuerpo, nervio_vago). Figuras:
«medium close-up» + escenario concreto, o Nano Banana deja la figura diminuta sobre negro (duelo_cuerpo).
   python hacer_prompts.py [--lista]"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
SR = F["personajes"]["el señor"]
NEON = "glowing yellow neon"
RELOJ = "an old twin-bell alarm clock with a blank face without numbers, its two hands pointing to three o'clock"
MANI = "a transparent glass mannequin torso drawn in fine white lines, with a white line-art heart, lungs and brain inside"
BRAIN = "a white line-art human brain seen from the side, drawn in fine engraving lines, no labels"
CUARTO = "a small Mexican bedroom at night with a window showing a crescent moon, a wooden nightstand with a lamp and a glass of water"

V = {  # clips combinados (9 x 10 s): (escena A, transición, escena B)
    "scene-001": (f"medium close-up of {SR} lying in bed in {CUARTO}, his eyes suddenly opening in the dark, on the nightstand {RELOJ}, the alarm clock {NEON}",
                  "the camera pushes in slowly toward the alarm clock, into scene two",
                  f"extreme close-up of {RELOJ}, the clock hands {NEON} trembling slightly as the seconds tick"),
    "scene-002": (f"wide view of {CUARTO}, everything silent and still, a cat asleep at the foot of the bed, the crescent moon in the window {NEON}",
                  "the camera glides toward the bed, into scene two",
                  f"medium close-up of {SR} sitting up in bed in the dark, small swirling lines of thoughts spinning around his head like a whirlwind, the swirling lines {NEON}"),
    "scene-003": (f"a sleeping Mexican town at night seen from above, rows of rooftops with water tanks and a church dome, three windows lit {NEON} among many dark windows",
                  "the camera flies slowly over the rooftops, into scene two",
                  f"inside one lit window: a woman in a nightgown sitting awake on the edge of her bed, a bedside lamp {NEON}"),
    "scene-004": (f"a long staircase of stone steps descending into the night sky with a moon and stars, a small clock face without numbers on each step, the first step {NEON}",
                  "the camera walks slowly down the steps, into scene two",
                  f"{MANI}, lying horizontal as if asleep on a wooden bed frame, a small alarm bell {NEON} resting quietly inside the head"),
    "scene-005": (f"medium close-up of {SR} pulling up the blanket and closing his eyes in bed, a reading lamp clicking off, the lamp {NEON}",
                  "the camera sinks down below the bed as if into dark water, into scene two",
                  f"a calm ocean at night seen from the side with long slow waves rising and falling in a steady rhythm, the line of the waves {NEON}"),
    # 1.ª versión con «a small sleeping figure floating» en la cueva: rechazada por la política de menores (23-oct)
    "scene-006": (f"a deep underwater cave below the ocean waves with slow swaying seaweed, smooth rocks and a soft round pillow resting on the sea floor, the sea floor {NEON}",
                  "the camera turns toward a small workshop at the bottom of the sea, into scene two",
                  f"{BRAIN} being gently washed by a slow stream of water like a river cleaning stones, the stream of water {NEON}"),
    "scene-007": (f"a tall hourglass in which the sand falls fast at first and then slows to a thin trickle, the falling sand {NEON}",
                  "the camera pulls back and the hourglass becomes the moon, into scene two",
                  f"the ocean waves at night growing smaller and smaller toward the horizon, the first big wave {NEON}"),
    "scene-008": (f"{MANI} lying asleep, its heart beating slowly and calmly {NEON}",
                  "the camera pulls back to reveal an old thermometer standing beside it, into scene two",
                  f"an old glass thermometer on a nightstand beside a sleeping figure, the line inside slowly going down, the thermometer line {NEON}"),
    "scene-009": (f"a 1970s hospital sleep laboratory at night: a volunteer asleep in a bed with a thin tube in his arm, a nurse with a clipboard and an old wall clock without numbers, the tube {NEON}",
                  "the camera moves along the tube to a row of small glass vials, into scene two",
                  f"a long row of small glass blood sample vials on a lab rack, each one a little darker than the last, the first vial {NEON}"),
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
        print(b["id"][6:], b["texto"][:60], "||", P[b["id"]][len(E):len(E) + 90].replace(SR, "SR"))
