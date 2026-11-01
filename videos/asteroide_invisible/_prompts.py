# -*- coding: utf-8 -*-
"""Escribe prompts.json (escenarios + hojas de Flow) con la FICHA de guion.py. Ejecutar desde la carpeta del video."""
import json
import guion

E = guion.FICHA["estilo"] + ". "
C = guion.FICHA["cierre"]
VACIO = " Strong depth: foreground, midground and background layers. Open empty ground across the lower third. No people, no animals."
FILA = (" full body, evenly spaced in one row with generous empty white space between them, never touching or overlapping")
HOJA = " on a plain flat pure white background"
NOSOMBRA = " No ground, no cast shadows."

ESC = {
    "01_espacio_tierra": "Wide background in deep space: planet Earth large on the lower right, half in night with glowing orange city "
        "lights, thin luminous blue atmosphere rim, the Sun's enormous white-orange glare flooding in from the left edge, a cold starfield, "
        "wide empty dark space in the upper left. No spacecraft, no asteroids.",
    "02_sistema_solar": "Wide background of the inner solar system seen from above at a low angle: the glowing Sun on the left, small "
        "Mercury and Venus, the blue Earth with its Moon in the center, small red Mars on the right, faint dust and a dim starfield, "
        "lots of empty dark space. No orbits drawn, no asteroids.",
    "03_cheliabinsk": "Wide background of a Russian city on a frozen winter morning in 2013: snowy street, grey Soviet apartment blocks "
        "with many glass windows, bare frozen trees, chimney smoke, the low pale winter Sun rising on the left horizon, cold pink-orange "
        "sky." + VACIO,
    "04_observatorio": "Wide background of an observatory in the Atacama desert of Chile at dusk: white telescope domes on a mountain "
        "ridge, one dome open with its telescope pointing low toward the horizon where the Sun has just set, deep blue and burning orange "
        "twilight, the first stars, dry rocks in the foreground." + VACIO,
    "05_sala_observatorio": "Wide background of a small observatory control room at night: a desk with three computer monitors glowing "
        "blue with blank screens, an office chair, a cold coffee mug, a window showing the open dome and stars, the room lit only by "
        "the screens. Open empty floor across the lower third. No people.",
    "06_sala_crisis": "Wide background of a planetary defense crisis room: a dark big room with a giant curved glowing wall screen "
        "(blank, plain dark blue), rows of desks with monitors, red emergency lights on the ceiling, cold blue light. Open empty floor "
        "across the lower third. No people.",
    "07_ciudad_noche": "Wide background of a huge Latin American city at 4 in the morning seen from a hillside neighborhood: an ocean "
        "of city lights, distant skyscrapers, dark mountains, a black sky with stars, rooftops with water tanks and antennas in the "
        "foreground." + VACIO,
    "08_recamara": "Wide background of a small apartment bedroom at night: an unmade bed, a nightstand, clothes on a chair, a big "
        "window with the city lights outside, the room in deep blue darkness. Open empty floor across the lower third. No people.",
    "09_autopista": "Wide background of a highway leaving a big city at dawn, completely jammed with cars with red tail lights in "
        "both directions, an overpass, police lights flashing, dark blue dawn sky with ONE unusually bright star low on the horizon. "
        "Open empty road shoulder across the lower third. No people visible.",
    "10_sala_mediodia": "Wide background of an apartment living room at noon: a sofa, a small table, potted plants, a huge glass window "
        "and balcony door showing the city skyline under a clear blue sky, a clothesline with hanging shirts on the balcony. Open empty "
        "floor across the lower third. No people.",
    "11_calle_mediodia": "Wide background of a residential street of a Latin American city at noon: two-story houses with glass "
        "windows, a small shop with a big glass window, parked cars, trees, power lines, wide clear sky, the city skyline far away "
        "on the horizon." + VACIO,
    "12_calle_destruida": "Wide background of the same kind of residential street just after a massive shock wave: every window "
        "shattered, torn roofs, fallen trees, snapped power lines, overturned car, glass and debris on the ground, brown-orange dusty "
        "sky with smoke." + VACIO,
    "13_zona_cero": "Wide aerial background of an enormous fresh impact crater about 7 km wide, its floor glowing with molten rock, "
        "a ring of flattened burning forest and city ruins around it, a gigantic column of dust and fire rising, dark orange sky.",
    "14_columna": "Wide background seen from 90 km away: city outskirts and hills on the horizon, and beyond them a colossal "
        "mushroom-like column of dust and fire rising into the stratosphere, the sky turned dark orange and brown." + VACIO,
    "15_sistema_exterior": "Wide background of the cold outer solar system: deep black-blue space, the distant Sun as a small bright "
        "star, faint icy blue Neptune, scattered frozen bodies and faint dust, enormous emptiness.",
    "16_marte": "Wide background in space: the red planet Mars large on the right side with craters and dust, black space with faint "
        "stars, a lot of empty dark space on the left.",
    "17_atardecer": "Wide background of a lonely hill at sunset overlooking a distant city: a huge red-orange Sun touching the horizon, "
        "a burning sky fading into dark indigo above, dry grass and a lone tree in the foreground." + VACIO,
}

HOJAS = {
    "20_asteroide_hoja": "Prop sheet" + HOJA + ", 6 separate space objects evenly spaced in a grid, never touching or overlapping: "
        "a huge dark charcoal potato-shaped rocky asteroid covered in craters (three different angles of the SAME asteroid); a small "
        "jagged rock fragment; the same asteroid wrapped in burning orange-white plasma with a short fiery trail pointing up-left, "
        "entering the atmosphere; a dark comet nucleus with a long pale blue tail pointing right." + NOSOMBRA,
    "21_astronoma_hoja": "Character model sheet" + HOJA + ": a Chilean astronomer, woman of about 35, dark hair in a ponytail, glasses, "
        "grey hoodie, dark jeans, a lanyard. The SAME woman drawn 5 times," + FILA + ": sitting on an office chair leaning toward a "
        "screen, side view facing right; standing with a hand over her mouth in shock; holding a phone to her ear talking urgently; "
        "pointing forward; sitting with her head in her hands." + NOSOMBRA,
    "22_persona_hoja": "Character model sheet" + HOJA + ": an ordinary Latin American man of about 30, messy dark hair, grey t-shirt, "
        "jeans and sneakers. The SAME man drawn 5 times," + FILA + ": standing staring at a glowing phone in his hand, face lit from "
        "below; standing looking up at the sky shielding his eyes with a hand; crouching on the floor covering his head with his arms; "
        "standing frozen staring forward in terror; pressed back against a wall, terrified." + NOSOMBRA,
    "23_persona_corre": "Animation sprite sheet" + HOJA + ": run cycle of an ordinary Latin American man of about 30, messy dark hair, "
        "grey t-shirt, jeans and sneakers, running in panic. The SAME character drawn 8 times in a single horizontal row, strict side "
        "view facing right, full body, same size and same height, evenly spaced and not touching, each drawing a consecutive phase of "
        "one running stride." + NOSOMBRA,
    "24_gente_hoja": "Character sheet" + HOJA + ": 6 different ordinary people of a Latin American city," + FILA + ": a mother holding "
        "her small daughter; an old man with a cane looking up at the sky; a teenager filming the sky with a phone; a woman in office "
        "clothes pointing up at the sky; a little boy hugging a teddy bear; a man carrying a suitcase, looking back." + NOSOMBRA,
    "25_mujer_corre": "Animation sprite sheet" + HOJA + ": run cycle of a young woman in a red jacket and jeans running in panic. The "
        "SAME character drawn 8 times in a single horizontal row, strict side view facing right, full body, same size and same height, "
        "evenly spaced and not touching, each drawing a consecutive phase of one running stride." + NOSOMBRA,
    "26_funcionarios_hoja": "Character sheet" + HOJA + ": 6 different people of a planetary defense crisis team," + FILA + ": a "
        "military general in uniform talking on a phone; a scientist holding a tablet; a man with a headset at a console, side view; "
        "a woman scientist staring up in disbelief; an official in a dark suit with his hands on his head; an engineer slumped on a "
        "chair." + NOSOMBRA,
    "27_vehiculos": "Prop sheet" + HOJA + ", 8 separate vehicles, strict side view facing right, evenly spaced in a grid, never "
        "touching or overlapping: a compact car, a pickup truck, a city bus, an ambulance, a police car, a yellow taxi, a delivery van, "
        "a motorcycle with rider." + NOSOMBRA,
    "28_utileria": "Prop sheet" + HOJA + ", about 16 separate objects evenly spaced in a grid with generous empty white space, never "
        "touching or overlapping: a smartphone with a glowing red emergency alert screen, a big observatory telescope, a radar dish, a "
        "small boxy spacecraft with two long solar panels, an infrared space telescope with a sunshield, a rocket, a broken window "
        "frame with shards of glass, five flying glass shards, a clothesline with shirts, a traffic light, a flying sheet of corrugated "
        "roof metal, an uprooted tree, a burning chunk of rock, a red siren light, an alarm clock, a pair of binoculars." + NOSOMBRA,
    "29_aves_aleteo": "Animation sprite sheet" + HOJA + ": a row of 6 drawings of the same black crow showing a wing-flap cycle in "
        "flight, strict side view facing right, same size, evenly spaced and not touching." + NOSOMBRA,
    "30_fuego_humo": "Prop sheet" + HOJA + ", about 12 separate elements evenly spaced in a grid, never touching or overlapping: four "
        "different tall orange flames, three dark grey smoke clouds, two brown dust clouds, a cluster of glowing embers, two burning "
        "debris chunks." + NOSOMBRA,
}

P = {k: E + v + C for k, v in {**ESC, **HOJAS}.items()}
json.dump(P, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(ESC), "escenarios +", len(HOJAS), "hojas =", len(P), "prompts")
