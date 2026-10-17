# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) a partir de beats.json. Estilo «línea blanca + neón»: en cada prompt se nombra
QUÉ va en neón amarillo; lo demás es línea blanca sobre negro.   python hacer_prompts.py"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
HOM, MUJ = F["personajes"]["el hombre"], F["personajes"]["la mujer"]
ANAT = "anatomical illustration drawn in thin white engraving lines, no labels"

V = {  # clips combinados: (escena A, transición, escena B)
    "scene-001": (f"in a small kitchen at night, {MUJ} argues and gestures angrily while {HOM} stands silent with his arms "
                  f"crossed and lips pressed shut; inside his chest outline his heart glows in bright yellow neon",
                  "the camera pushes into the round wall clock whose hands spin very fast, and the clock face becomes scene two",
                  f"the same kitchen, calmer: {MUJ} comes back and gently places her hand on his shoulder, apologizing; "
                  f"{HOM} looks at her and his eyes fill with tears that glow in yellow neon"),
    # 1.ª versión («a glowing yellow neon knot tightens around his throat») rechazada por política de Flow (16-oct-2026)
    "scene-002": (f"close-up of {HOM} with a sad face and glistening eyes; a glowing yellow neon teardrop forms in the corner "
                  f"of his eye and rolls slowly down his cheek",
                  "his body slowly turns transparent like glass and the camera dives inside it into scene two",
                  "inside the transparent body: thin white veins full of tiny glowing yellow neon molecules flowing and "
                  "swirling like a chemical storm"),
    "scene-003": (f"{HOM} stands alone inside a large glowing yellow neon ring on dark rocky ground, fists raised, facing "
                  f"an empty opponent who never arrives, dust drifting",
                  "the camera pushes into the side of his round head and the white lines redraw themselves into scene two",
                  f"side view of a human head with the brain as an {ANAT}; deep inside, a small almond-shaped amygdala "
                  f"glows and pulses in bright yellow neon"),
    "scene-004": ("the glowing yellow neon amygdala flashes like an alarm light and fires bright electric sparks in a "
                  f"fraction of a second, inside a white line-art brain, {ANAT}",
                  "the sparks race downward and the camera follows them into scene two",
                  f"the hypothalamus lights up in yellow neon and a glowing yellow neon nerve signal runs down the spinal "
                  f"cord like a burning fuse, along a white line-art spine and torso, {ANAT}"),
    "scene-005": (f"back view of a human torso as an {ANAT}: two kidneys with the small adrenal glands sitting on top of "
                  f"them, the adrenal glands glowing bright yellow neon",
                  "the camera follows a glowing droplet into a blood vessel, into scene two",
                  f"the adrenal glands squirt glowing yellow neon droplets into a white blood vessel and a white line-art "
                  f"heart starts beating fast, glowing yellow neon, {ANAT}"),
    "scene-006": (f"a white line-art human liver releasing glowing yellow neon sparks of sugar into the bloodstream like "
                  f"fuel pouring into a tank, {ANAT}",
                  "the sparks spread outward through the veins and the view pulls back to scene two",
                  f"full body of {HOM} standing: glowing yellow neon blood rushes into his arms and legs and his fists "
                  f"clench tight"),
    "scene-007": (f"extreme close-up of the eye of {HOM}: the pupil dilates and his vision narrows into a dark tunnel "
                  f"whose rim glows yellow neon, the angry woman tiny at the end",
                  "the tunnel spirals open and widens into scene two",
                  f"{HOM} stands completely frozen and still in the dark kitchen while his whole body outline glows yellow "
                  f"neon, charged like a battery, but he does not move at all"),
}

I = {  # imágenes: una por beat
    "scene-008": f"{HOM} sitting frozen on a kitchen chair; inside his chest a full fuel tank and a revving engine glow in bright yellow neon",
    "scene-009": f"{MUJ} walks out through a doorway; inside the transparent head of {HOM}, a foot slams a glowing yellow neon brake pedal",
    "scene-010": f"a human torso and head as an {ANAT}; the long wandering vagus nerve runs from the brainstem down the neck to the heart, lungs and belly, glowing in bright yellow neon",
    "scene-011": "a car drawn in thin white lines braking hard on a dark road, long skid marks, its brake disc glowing red hot in yellow neon",
    "scene-012": f"close-up of {HOM}: a glowing yellow neon knot in his throat and glowing yellow neon tears running from his eyes",
    "scene-013": "a foot gently and slowly pressing a glowing yellow neon brake pedal, soft motion lines, calm",
    "scene-014": "a dark forest crossroads drawn in white lines with two paths; at the end of the left path a campfire burns in bright yellow neon flames",
    "scene-015": "a gentle path sloping down a white line-art hill at night, a single glowing yellow neon feather floating slowly down",
    "scene-016": "a long dark stone corridor drawn in white lines with five hanging lanterns in a row, all five glowing yellow neon",
    "scene-017": f"{HOM} sitting calmly on a chair, eyes closed; a large outline of lungs glows bright yellow neon inside his chest",
    "scene-018": f"{HOM} inhaling deeply through his nose, white swirls of air flowing in, his lungs glowing yellow neon as they fill, plus one small extra puff of air",
    "scene-019": f"microscopic view of lung alveoli like clusters of grapes as an {ANAT}; deflated sacs reinflating and glowing yellow neon",
    "scene-020": f"{HOM} exhaling slowly through pursed lips, a long ribbon of breath flowing out, the ribbon glowing yellow neon",
    "scene-021": "two ribbons of breath floating side by side in the dark, a short white one and a long one twice as long glowing yellow neon",
    "scene-022": f"a human heart as an {ANAT} with the vagus nerve wrapped around it glowing yellow neon, gently slowing the heartbeat",
    "scene-023": "a heartbeat line drawn across the black frame, its spikes getting slower and calmer, the line glowing yellow neon",
    "scene-024": f"a quiet university research lab at night with arched windows and palm trees outside, drawn in white lines; a volunteer sits breathing with sensors on the chest, the volunteer's lungs glowing yellow neon",
    "scene-025": f"{HOM} with relaxed dropping shoulders while a heavy glowing yellow neon storm cloud above his head shrinks away",
    "scene-026": f"{HOM} pushing against a brick wall with all his strength, the muscles of his arms glowing yellow neon",
    "scene-027": f"a human body muscle map as an {ANAT}; glowing yellow neon electric signals run along the nerves into the muscles",
    "scene-028": f"{HOM} sitting on a chair pressing his feet hard into the floor and clenching both fists, his fists glowing yellow neon",
    "scene-029": f"{HOM} (bald round white head, no hair) letting go suddenly, arms hanging loose and relaxed, the yellow neon glow leaving his hands as drifting sparks",
    "scene-030": f"close-up of muscle fibers as an {ANAT}, burning glowing yellow neon sparks of sugar like fuel in a furnace",
    "scene-031": "a tightly compressed coil spring suddenly released and stretching loose, the spring glowing yellow neon",
    "scene-032": "a vintage nineteen-thirties doctor's office drawn in white lines: an old physician with round glasses and a white coat writing at a wooden desk while a patient lies relaxed on a couch, the patient's outline glowing yellow neon",
    "scene-033": "a seal diving deep under dark water drawn in white lines, bubbles rising, the seal's heart glowing yellow neon",
    "scene-034": f"{HOM} in a small bathroom splashing cold water on his face over a sink, the water splash glowing yellow neon",
    "scene-035": "close-up of a simple face with cold water droplets on the forehead, around the eyes and on the cheekbones, those three areas glowing yellow neon",
    "scene-036": f"a human head in profile as an {ANAT}; the trigeminal nerve with its three branches spreading across the face glows bright yellow neon; absolutely no labels, no letters, no annotation marks anywhere",
    "scene-037": f"{HOM} floating calmly underwater with eyes closed, bubbles rising toward a distant surface, his heart glowing yellow neon",
    "scene-038": f"a human heart as an {ANAT} glowing yellow neon, with a large curved downward arrow beside it, beating slower",
    "scene-039": "a dog shaking its whole body vigorously after running, drawn in white lines, the motion lines around it glowing yellow neon",
    "scene-040": "a gazelle leaping away from a lion across a white line-art savanna at night, the gazelle glowing yellow neon",
    "scene-041": f"{HOM} in a backyard at night shaking his hands loosely as if shaking off water, his hands glowing yellow neon with motion lines",
    "scene-042": f"{HOM} doing quick squats in a backyard at night, his legs glowing yellow neon",
    "scene-043": f"the big leg and back muscles of a human body as an {ANAT}, glowing yellow neon and burning sparks of fuel",
    "scene-044": f"a white blood vessel as an {ANAT} where glowing yellow neon droplets slowly dim and fade out one by one",
    "scene-045": f"close-up of the calm eye of {HOM} opening wide, a wide fan of yellow neon rays spreading to both sides",
    "scene-046": f"{HOM} staring down a dark narrow tunnel where only a small circle is visible, the tunnel rim glowing yellow neon",
    "scene-047": f"{HOM} in a living room with his head still, a wide glowing yellow neon arc around him reaching both upper corners of the room",
    "scene-048": f"{HOM} sitting relaxed on a sofa looking out a big window at a wide night landscape, the horizon line glowing yellow neon",
    "scene-049": f"close-up of the chest of {HOM} with a ribcage outline, a tight glowing yellow neon knot loosening and untying",
    "scene-050": f"the small kitchen at night: {MUJ} says something sharp and a small glowing yellow neon lightning bolt flashes above the head of {HOM}",
    "scene-051": f"{HOM} breathing quietly at the kitchen table while {MUJ} looks away, his lungs glowing yellow neon",
    "scene-052": f"{HOM} at a bathroom sink with wet face, clenching both fists, his fists glowing yellow neon",
    "scene-053": "a round kitchen wall clock with only tick marks and no numerals, its hands moving forward, the clock outline glowing yellow neon",
    "scene-054": f"{MUJ} comes back into the kitchen with open hands, gently apologizing, her outline glowing soft yellow neon",
    "scene-055": f"{HOM} calm with a relaxed throat, a glowing yellow neon storm cloud above him breaking apart into tiny stars",
    "scene-056": f"{HOM} and {MUJ} sitting together at the kitchen table, he listens calmly, a warm lamp above them glowing yellow neon",
    "scene-057": "a small house at night seen from outside under a starry sky, a crescent moon glowing yellow neon above the roof, one warm window",
}

beats = json.load(open("beats.json", encoding="utf-8"))
beats = beats["beats"] if isinstance(beats, dict) else beats
P = {}
for b in beats:
    k = b["id"]
    if k in V:
        a, tr, c = V[k]
        P[k] = f"{E}Scene one, first five seconds: {a}. Then {tr}. Scene two, last five seconds: {c}.{C}"
    else:
        P[k] = f"{E}{I[k]}.{C}"
assert len(P) == len(beats), (len(P), len(beats))
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(P), "prompts")
