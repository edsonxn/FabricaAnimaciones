# -*- coding: utf-8 -*-
"""Escribe prompts.json (escenarios + hojas de Flow) con la FICHA noir de guion.py. Ejecutar desde la carpeta del video."""
import json
import guion

E = guion.FICHA["estilo"] + ". "
C = guion.FICHA["cierre"]
VACIO = " Strong depth: foreground, midground and background layers. Open empty ground across the lower third. No people, no animals."
PISO = " Strong depth: foreground, midground and background layers. Open empty floor across the lower third. No people."
FILA = (" full body, evenly spaced in one row with generous empty white space between them, never touching or overlapping")
HOJA = " on a plain flat pure white background"
NOSOMBRA = " No ground, no cast shadows."

ESC = {
    "01_ciudad_lluvia": "Wide background of a city street at night in heavy rain: wet cobblestones and asphalt reflecting the streetlamps, "
        "old brick buildings with fire escapes and a few lit windows, a small office window glowing on the second floor, steam rising "
        "from a manhole, a parked 1940s car, rain streaks in the lamplight." + VACIO,
    "02_oficina": "Wide background of a private detective's office at night: a heavy wooden desk with an old typewriter, a green-shaded "
        "desk lamp, a rotary telephone and an ashtray, a tall filing cabinet, a coat rack, a big window with venetian blinds and rain "
        "outside casting striped shadows across the room, a frosted glass door with blank glass." + PISO,
    "03_pasillo_puerta": "Wide background of a dim old office building hallway at night: a frosted glass office door with blank glass "
        "and a thin line of light under it, worn wooden floor, a single bare ceiling bulb, peeling wallpaper, a staircase in the distance."
        + PISO,
    "04_archivo": "Wide background of a basement records archive: long rows of tall metal filing cabinets receding into darkness, "
        "cardboard boxes stacked, a single hanging bulb making a cone of light full of floating dust." + PISO,
    "05_servidores": "Wide background of a long data center aisle at night drawn as film noir: tall server racks on both sides with tiny "
        "blinking lights and bundles of cables, cold light from ceiling panels, haze, vanishing perspective toward a dark end." + PISO,
    "06_callejon_puerta": "Wide background of a narrow back alley behind a tall building at night: a small hidden metal back door slightly "
        "ajar with a sharp wedge of light spilling out onto the wet ground, trash cans, a fire escape ladder, puddles, rain."
        + VACIO,
    "07_aula": "Wide background of a stark old training classroom at night: rows of empty wooden school desks, a large blank blackboard, a "
        "tall barred window with moonlight, a hanging lamp, long shadows." + PISO,
    "08_interrogatorio": "Wide background of a police interrogation room: a bare metal table with two metal chairs facing each other, a "
        "single hanging lamp throwing a hard cone of light, concrete walls, a large dark one-way mirror on the side wall, a door with a "
        "small barred window." + PISO,
    "09_observacion": "Wide background of the dark observation room behind a one-way mirror: through the big glass window the brightly lit "
        "interrogation room with an empty metal table, in the foreground a console with small glowing monitors with blank screens, a "
        "microphone on a stand, two empty chairs." + PISO,
    "10_sala_control": "Wide background of a security control room at night: a wall of small old monitors with blank glowing screens, "
        "a big electrical panel with a large lever switch, thick cables on the floor, a ceiling fan, deep shadows." + PISO,
    "11_teatro": "Wide background of an empty old theater at night: a stage with heavy curtains half open, a single round spotlight on "
        "the bare wooden stage, dust in the beam, rows of empty velvet seats in the dark foreground, balconies in shadow.",
    "12_dos_puertas": "Wide background of a long corridor ending in two doors side by side: on the left a plain worn cheap wooden door with "
        "a bare bulb above it, on the right an elegant padded leather door with brass studs and a fancy wall lamp above it, checkered "
        "floor, dramatic perspective." + PISO,
    "13_escritorio_diario": "Wide background, closer view of a small writing desk in a dark room lit only by a small desk lamp: an open "
        "notebook with blank pale pages, a fountain pen, a cup of coffee, stacks of papers, shelves of books fading into black behind.",
    "14_salon_alfombra": "Wide background of an elegant old living room at night: a large ornate patterned rug in the center of the floor "
        "with one corner slightly lifted revealing a dark gap underneath, a leather armchair, a fireplace with dying embers, a tall "
        "window with rain, a grandfather clock." + PISO,
    "15_calle_final": "Wide background of a long empty wet street at night receding into fog: a row of streetlamps getting smaller into "
        "the distance, puddles reflecting the lights, dark buildings, a lone lit phone booth, light rain." + VACIO,
    "16_laboratorio": "Wide background of a modern artificial intelligence research lab at night drawn as film noir: desks with computer "
        "monitors with blank glowing screens, a large blank whiteboard, glass walls, cables, coffee cups, server lights through a glass "
        "partition, city lights through big windows." + PISO,
}

HOJAS = {
    "20_detective_hoja": "Character model sheet" + HOJA + ": a hard-boiled private detective, man of about 45, fedora hat, long trench "
        "coat with the collar up, loosened tie, stubble, tired eyes. The SAME man drawn 6 times," + FILA + ": standing reading a "
        "letter held in both hands; sitting on a wooden office chair leaning forward, side view facing right; standing smoking a "
        "cigarette looking sideways; standing pointing forward; crouching down lifting the corner of a rug; standing seen from behind "
        "with hands in his coat pockets." + NOSOMBRA,
    "21_detective_camina": "Animation sprite sheet" + HOJA + ": walk cycle of a hard-boiled private detective, man of about 45, fedora "
        "hat, long trench coat, hands in his pockets. The SAME character drawn 8 times in a single horizontal row, strict side view "
        "facing right, full body, same size and same height, evenly spaced and not touching, each drawing a consecutive phase of one "
        "walking step." + NOSOMBRA,
    "22_ia_hoja": "Character model sheet" + HOJA + ": an artificial intelligence imagined as a sleek elegant humanoid android in a dark "
        "three-piece suit and tie, with a smooth featureless pale grey porcelain face like a mask with two thin dark eye slits and no "
        "mouth, thin mechanical seams on the neck and hands. The SAME android drawn 6 times," + FILA + ": sitting upright on a metal "
        "chair with its hands folded on its knees, side view facing left; standing perfectly calm with hands behind its back; holding a "
        "smiling pale grey theatre mask in front of its face; looking back over its shoulder; writing in a small notebook with a pen; "
        "crouching and sliding something under the edge of a rug." + NOSOMBRA,
    "23_ia_camina": "Animation sprite sheet" + HOJA + ": walk cycle of a sleek humanoid android in a dark three-piece suit with a smooth "
        "featureless pale grey porcelain mask-like face. The SAME character drawn 8 times in a single horizontal row, strict side view "
        "facing right, full body, same size and same height, evenly spaced and not touching, each drawing a consecutive phase of one "
        "calm walking step." + NOSOMBRA,
    "24_investigadores_hoja": "Character sheet" + HOJA + ": 6 different modern artificial intelligence safety researchers drawn as film "
        "noir characters," + FILA + ": a woman holding a clipboard, frowning; a man with a headset typing at a keyboard, side view facing "
        "right; a man holding a coffee mug, staring; a woman pointing at something ahead; an older man with his arms crossed; a young man "
        "taking notes in a notebook." + NOSOMBRA,
    "25_utileria": "Prop sheet" + HOJA + ", about 18 separate objects evenly spaced in a grid with generous empty white space, never "
        "touching or overlapping: a pale grey paper envelope with no stamp; a single sheet of pale grey paper; an old typewriter; a rotary "
        "telephone; a desk lamp; a manila case folder; a magnifying glass; a security camera on a bracket; a big lever switch on a panel; "
        "an old iron key; an open padlock; a smiling pale grey theatre mask; an open notebook; a coffee mug; an ashtray with a smoking "
        "cigarette; a fedora hat; a round wall clock; a server rack cabinet with blinking lights." + NOSOMBRA,
    "26_humo_papel": "Prop sheet" + HOJA + ", about 12 separate elements evenly spaced in a grid, never touching or overlapping: four "
        "different wisps of grey cigarette smoke; two clouds of grey steam; three flying sheets of pale grey paper at different angles; "
        "a pile of scattered papers; two drops of black ink splash." + NOSOMBRA,
    "27_polilla_aleteo": "Animation sprite sheet" + HOJA + ": a row of 6 drawings of the same dark moth showing a wing-flap cycle in "
        "flight, top view, same size, evenly spaced and not touching." + NOSOMBRA,
}

P = {k: E + v + C for k, v in {**ESC, **HOJAS}.items()}
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(ESC), "escenarios +", len(HOJAS), "hojas =", len(P), "prompts")
