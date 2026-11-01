# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat, TODO IMAGEN) a partir de beats.json. Estilo «línea blanca + neón»: en cada
prompt se nombra QUÉ va en neón amarillo; lo demás es línea blanca sobre negro.   python hacer_prompts.py"""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
MUJ = F["personajes"]["la mujer"]
ANAT = "anatomical illustration drawn in thin white engraving lines, no labels"
CUARTO = "a small bedroom at night with a bed, a nightstand and a window showing the moon"
RELOJ = "a round clock with a blank face and no numbers"

V = {  # clips combinados (7 x 10 s): (escena A, transición, escena B)
    "scene-001": (f"{MUJ} drags her feet through a dark apartment hallway at night, shoulders slumped, exhausted, a heavy glowing yellow neon backpack on her back",
                  "she pushes open her bedroom door and the camera follows her through the doorway into scene two",
                  f"{MUJ} collapses face down onto her bed in {CUARTO}; her pillow glows soft yellow neon"),
    "scene-002": (f"{MUJ} lying in bed pulls the cord of a bedside lamp and closes her eyes in the dark; then inside her round head a big glowing yellow neon light bulb flicks on",
                  "the camera pushes into the glowing bulb until its light fills the frame, and the light opens into scene two",
                  f"{MUJ} lies awake staring at the ceiling while thought bubbles float above her: a meeting table, two people talking, a phone with an unanswered message glowing yellow neon"),
    "scene-003": (f"a transparent outline of {MUJ} standing; inside her chest two clocks side by side, an hourglass and {RELOJ}; the round clock glows yellow neon and its hands spin very fast",
                  "the camera pushes into the hourglass until it fills the frame and becomes scene two",
                  "a large antique hourglass standing on a dark wooden table, its falling sand glowing bright yellow neon, intricate engraved frame"),
    "scene-004": (f"microscopic view of neurons as an {ANAT}: branching nerve cells firing tiny white sparks of energy, one neuron glowing yellow neon",
                  "the sparks fall slowly like sand and the camera follows them down into scene two",
                  f"tiny glowing yellow neon grains drifting away from the neurons and piling up like sand dunes between the white line-art brain cells, {ANAT}"),
    "scene-005": (f"{MUJ} sitting at a kitchen table at night with very heavy drooping eyelids, weighed down by small glowing yellow neon sandbags",
                  "she lifts a coffee cup and the camera dives into the dark coffee into scene two",
                  f"macro view of a nerve cell surface with keyhole-shaped receptors; small coffee-bean shaped molecules glowing yellow neon float in and plug the keyholes, {ANAT}"),
    "scene-006": ("a coffee cup on a desk next to a window; outside, the afternoon sun sets and the moon rises while the steam from the cup, glowing yellow neon, keeps rising in a long ribbon",
                  "the camera glides toward the window and through the glass into scene two",
                  f"side view of a human head as an {ANAT}; behind the eyes, where the optic nerves cross, a tiny cluster the size of a grain of rice glows bright yellow neon"),
    "scene-007": (f"{MUJ} at a window at dusk watching the sun go down behind the rooftops; light rays enter her eyes and travel as a glowing yellow neon line into her head",
                  "the sky darkens to night and the camera travels into the center of her head into scene two",
                  f"a small pine-cone shaped gland deep in the center of a white line-art brain releasing glowing yellow neon droplets like gentle fireflies, {ANAT}"),
}

I = {
    "scene-008": f"a dark theater stage with a heavy curtain opening; a spotlight falls on a sinister tall shadowy figure made of thin white lines wearing a top hat, his outline and eyes glowing yellow neon",
    "scene-009": f"{MUJ} jumping out of bed in the morning with arms stretched up, a bright sunrise in the window, a glowing yellow neon arrow rising through her body like a rocket",
    "scene-010": f"a gentle curved line like a hill drawn across the black frame, a sun on the left high point and a moon at the right low point, the curve glowing yellow neon",
    "scene-011": f"{MUJ} in bed at night, eyes wide open, while a glowing yellow neon fire alarm siren on the bedroom wall keeps flashing",
    "scene-012": f"a children's seesaw in a dark playground at night: one end weighed down by a heavy glowing yellow neon boulder, the other end stuck high in the air with a small white moon sitting on it",
    "scene-013": f"close-up of the moon on the high end of a seesaw unable to come down, small white motion lines, the seesaw beam glowing yellow neon",
    "scene-014": f"a giant hourglass in {CUARTO}, its bottom completely full of sand that glows soft yellow neon",
    "scene-015": f"an old mechanical alarm bell ringing on a nightstand, hammer blurred with motion, the bell glowing bright yellow neon, the sleeping room around it",
    "scene-016": f"{MUJ} in bed under the covers while a swarm of floating sticky notes and papers circles above her head; one note glows yellow neon",
    "scene-017": f"a nineteen-twenties Berlin cafe drawn in white lines: a young woman psychologist with short hair and a notebook watching a waiter carrying trays, the notebook glowing yellow neon",
    "scene-018": f"a table with two stacks of papers: a neat finished pile drawn in faint white lines and a messy unfinished pile glowing bright yellow neon",
    "scene-019": f"a busy noisy city street during the day drawn in white lines with cars and people, and a tiny glowing yellow neon note in a pocket of {MUJ} walking among them",
    "scene-020": f"a dark bedroom where dozens of floating window panels like open browser tabs fill the air above the bed of {MUJ}, every panel outline glowing yellow neon",
    "scene-021": f"{MUJ} sitting relaxed at the edge of her bed, a soft glowing yellow neon sunrise-like smile shape above her, calm",
    "scene-022": f"a hand slowly turning down a big volume knob on a wall alarm panel, the knob glowing yellow neon, the alarm lights dimming",
    "scene-023": f"five glowing yellow neon fireflies hovering in a row above a sleeping cat on a windowsill at night",
    "scene-024": f"{MUJ} pulling a long glowing yellow neon ribbon of tangled thoughts out of the top of her head with both hands, like a magician's scarf",
    "scene-025": f"{MUJ} sitting at a kitchen table at night writing on a notepad with a pencil; the notepad lines are only wavy scribbles, the pencil tip glows yellow neon",
    "scene-026": f"close-up of a hand writing a long detailed list of wavy scribbled lines with small checkboxes on a notepad; the pencil glows yellow neon",
    "scene-027": f"a university campus at night drawn in white lines: a brick building with a tall clock tower without numbers and big trees, one window glowing yellow neon",
    "scene-028": f"a sleep laboratory room with several beds and volunteers lying down with sensor wires on their heads, one notepad on a nightstand glowing yellow neon",
    "scene-029": f"two volunteers in lab beds side by side: one already asleep with a glowing yellow neon crescent moon above her head, the other still awake",
    "scene-030": f"a very long scroll of paper unrolling across the frame covered in tiny scribbled wavy lines, the scroll's edge glowing yellow neon",
    "scene-031": f"a filing cabinet drawer closing gently with a click, a glowing yellow neon folder safely tucked inside, in a dark office",
    "scene-032": f"a bathroom at night drawn in white lines, a shower head pouring hot water with rising steam, the steam glowing yellow neon",
    "scene-033": f"a full body outline of {MUJ} standing as an {ANAT}; her core torso glows warm yellow neon like an inner furnace",
    "scene-034": f"{MUJ} standing under a hot shower with her eyes closed, steam swirling; the water stream glows yellow neon",
    "scene-035": f"a white line-art human body with the blood vessels branching to the hands and feet, the hands and feet glowing bright yellow neon, {ANAT}",
    "scene-036": f"warm heat waves leaving the open hands of {MUJ} as she lies in bed, the heat waves glowing yellow neon and drifting into the cool night air",
    "scene-037": f"{MUJ} already asleep in bed under a blanket, a soft glowing yellow neon crescent moon hanging above her, a few drifting stars",
    "scene-038": f"a ceiling light fixture in a living room being switched off by a wall switch; the switch glows yellow neon",
    "scene-039": f"a confused rooster standing on a dark rooftop at night crowing at a bright ceiling lamp shining through a window, the lamp glowing yellow neon",
    "scene-040": f"a hospital sleep research room drawn in white lines: a volunteer sitting in an armchair under a bright ordinary ceiling light, a blood sample tube on a tray, the ceiling light glowing yellow neon",
    "scene-041": f"a long ribbon of night drawn as a dark path with a glowing yellow neon moon, being cut shorter by a pair of large scissors",
    "scene-042": f"a cozy bedroom corner with a small low lamp on the floor giving a warm glow, the lamp shade glowing soft yellow neon, {MUJ} reading a book in an armchair",
    "scene-043": f"{MUJ} placing her smartphone face down on a shelf far from the bed; the phone edge glows yellow neon",
    "scene-044": f"{MUJ} lying in bed with closed eyes; above her head floats a single loaf of bread drawn in white lines glowing yellow neon",
    "scene-045": f"a round loaf of bread on a wooden board in a dark kitchen, the crust outline glowing yellow neon",
    "scene-046": f"a pear and a small dog floating gently in the dark above a sleeping pillow, the pear glowing yellow neon",
    "scene-047": f"an umbrella and an upright piano floating dreamily in a starry night sky, the umbrella glowing yellow neon",
    "scene-048": f"a deck of playing cards being shuffled in mid-air, cards fanning out in an arc, one card glowing yellow neon, the cards blank with no symbols",
    "scene-049": f"surreal dreamy collage floating in the dark: a fish, a key, a hot air balloon and a teacup drifting apart, the balloon glowing yellow neon",
    "scene-050": f"{MUJ} smiling slightly as she drifts asleep, her pillow softly glowing yellow neon",
    "scene-051": f"{MUJ} lying awake in bed glancing at {RELOJ} on her nightstand, the clock glowing yellow neon",
    "scene-052": f"{MUJ} sitting up and getting out of bed in the dark, putting her feet into slippers that glow yellow neon",
    "scene-053": f"{MUJ} wrestling with a big fluffy pillow on the bed like a boxing match, the pillow glowing yellow neon, comic",
    "scene-054": f"{MUJ} sitting on a sofa in a dim living room folding laundry, a small table lamp glowing soft yellow neon",
    "scene-055": f"{MUJ} walking back toward her bedroom door yawning, the doorway framed in soft glowing yellow neon",
    "scene-056": f"a doctor with round glasses sitting across from a patient in a calm consulting room drawn in white lines, a notebook between them glowing yellow neon",
    "scene-057": f"a small pill bottle pushed aside on a table while a glowing yellow neon pillow takes the center",
    "scene-058": f"a still life on a dark table: a towel, a bar of soap and a steaming shower head, the steam glowing yellow neon",
    "scene-059": f"a nightstand with a dimmed lamp and a notepad with a pencil, the notepad glowing yellow neon",
    "scene-060": f"{MUJ} in bed with a few floating dream objects shuffling above her like cards, one glowing yellow neon",
    "scene-061": f"{MUJ} calmly walking out of her bedroom in slippers, a softly glowing yellow neon trail behind her",
    "scene-062": f"a wall calendar with blank pages flipping by in the wind in a dark bedroom, the pages edged in glowing yellow neon, no numbers",
    "scene-063": f"{MUJ} talking with a kind doctor in a quiet clinic, the doctor's stethoscope glowing yellow neon",
    "scene-064": f"wide shot of {CUARTO}, {MUJ} switching off the bedside lamp and closing her eyes; the moon in the window glows yellow neon",
    "scene-065": f"a notepad resting on the nightstand next to a silent alarm bell covered by a cloth, the notepad glowing yellow neon",
    "scene-066": f"{MUJ} sleeping peacefully in bed while a tall hourglass beside the bed lets its glowing yellow neon sand fall slowly",
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
assert len(P) == len(beats) == len(I) + len(V), (len(P), len(beats), len(I), len(V))
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(P), "prompts")
