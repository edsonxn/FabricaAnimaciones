# -*- coding: utf-8 -*-
"""Genera prompts.json (un prompt por beat) desde la FICHA de guion.py. Los beats NO se regeneran: están a mano en beats.json.
Uso (desde la carpeta del video):  python _prompts_gen.py"""
import json
import sys

sys.path.insert(0, ".")
import guion as G

F = G.FICHA
S, C, EP = F["estilo"].rstrip(". ") + ".", F["cierre"], F["epoca"].rstrip(". ") + "."
P = F["personajes"]
K = F["objeto"]
FA = f"FRAY ANTONIO ({P['FRAY ANTONIO']})"
FM = f"FRAY MIGUEL ({P['FRAY MIGUEL']})"
CX = f"CAXCAN FAMILIES ({P['CAXCAN FAMILIES']})"
TP = f"TOWNSPEOPLE ({P['TOWNSPEOPLE']})"
OF = f"THE OFFICIAL ({P['THE OFFICIAL']})"
CHURCH = ("an old plain stone church with a single bell tower standing on the left side of its facade, a simple arched wooden door, "
          "no clock, no decorations")

ESCENAS = {
    1: f"Wide vertical view of a small paved garden plaza with rose beds and benches in front of {CHURCH}, present day, mid-morning "
       f"golden light, a few locals in casual everyday clothes sitting on stone benches. Church in the upper third, garden in the lower "
       f"two thirds. {EP}",
    2: f"The same {CHURCH}, but the small space in front of it is an old village cemetery of long ago: simple wooden crosses and low "
       f"stone slabs in the earth, a few small candles glowing, soft evening mist, a solemn quiet mood, cooler blue-grey and ochre light. "
       f"No people. {EP}",
    3: f"The same small garden in front of {CHURCH}, now in full bloom: red and pink rose bushes in neat beds, tall slender palm trees, "
       f"stone-paved walkway with carved stone edges, the church tower behind, small birds, warm cheerful morning light. {EP}",
    4: f"Wide vertical dawn landscape of a mountain canyon in January: a winding river with a strip of green trees between steep dry "
       f"mountains, a rocky flat-topped hill far in the distance, soft golden-pink sunrise light, mist in the valley, sky in the upper "
       f"third. No people. {EP}",
    5: f"Medium-full shot of two friars standing side by side on a rocky dirt mountain trail, looking toward the viewer with kind, "
       f"determined faces, open hands in a gesture of peace. On the left {FA}. On the right {FM}. Dry hills and mesquite trees behind "
       f"them, soft morning light. Subjects centered, open sky above. {EP}",
    6: f"Vertical diagonal composition: {FA} and {FM} walk at the front leading a long line of {CX} down a steep rocky mountain trail "
       f"toward a green river valley far below. The families are thin and tired but calm, carrying baskets and clay jars. A peaceful "
       f"descent, no weapons, no violence, cool morning light. {EP}",
    7: f"In a green clearing beside a river, {FA} and {FM} raise a tall wooden cross while {CX} gather around and start building the "
       f"first simple huts and a small chapel frame of branches and adobe. Hopeful, warm daylight, mountains in the background. {EP}",
    8: f"A small early colonial plaza of packed earth next to a humble stone chapel with one bell tower, a plain stone cross in the "
       f"middle of the plaza. {FA} stands beside the cross with a raised hand blessing the little square, while a few villagers watch "
       f"respectfully. Golden afternoon light, clay tile roofs. {EP}",
    9: f"A large antique brass hourglass in the center foreground with golden sand falling. Inside and behind it a small town plaza "
       f"appears as a layered time-lapse: at the bottom a bare dirt plaza with a stone cross, in the middle a plaza with young trees, at "
       f"the top a plaza with tall palm trees, with the sky moving from sunrise to sunset. Warm ochre and teal light. {EP}",
    10: f"A square town plaza in the nineteen forties seen from a corner, in front of a stately two-storey municipal palace with a stone "
        f"arcade of round arches, wooden balconies and a clay tile roof. {TP} stroll along the paths under young trees. Warm afternoon "
        f"light, a flagpole with a plain tricolor flag. Building in the upper half, plaza in the lower half. {EP}",
    11: f"Nineteen forties construction of a new square plaza: workers in straw hats and white shirts lay stone paving, plant young "
        f"palm trees and set cast-iron benches delivered on a wooden cart; a surveyor drives a wooden stake into the ground. {TP} "
        f"watch curiously. Bright sunny day, dust in the air. {EP}",
    12: f"Close-up detail of a wrought-iron park bench with ornate curled armrests and a slatted wooden seat under the trunk of a tall "
        f"palm tree, dappled sunlight on the ground, an elderly man in a straw hat sitting at one end reading, blurred plaza in the "
        f"background. Nineteen forties. {EP}",
    13: f"{K}. Shot from slightly above and in front so the eight sides of the structure are clearly visible, centered in a square "
        f"plaza. {TP} walk on the stone paths around it. Golden hour light. {EP}",
    14: f"Nineteen forties: {TP} gather on a large empty field with young trees at the edge of a small town, full of anticipation, "
        f"children running, a wooden platform being built at one side, a hot bright sky. Crowd in the lower two thirds. {EP}",
    15: f"A festive wooden podium decorated with plain bunting and Mexican flags stands in front of a large open field, in front of a "
        f"cheering crowd of {TP} in hats. Colorful paper streamers, a sunny May day, the mountains in the distance. {EP}",
    16: f"Medium shot of {OF} standing at the edge of a foundation trench holding a mason's trowel over a large squared stone slab, "
        f"with a mason in a straw hat beside him and a crowd applauding behind. Flags and bunting behind them. {EP}",
    17: f"Close-up of the sleeve of a dark suit and a mason's weathered hands setting a large squared cornerstone with a trowel and "
        f"fresh mortar into a foundation trench, the blurred boots and hats of a crowd behind. Warm light, shallow depth of field. {EP}",
    18: f"A second building site beside the first: the foundation of a new market, with baskets of fresh fruit and vegetables, guavas, "
        f"chiles and mangoes, stacked beside it and vendors in aprons watching, while {OF} sets another cornerstone. Town rooftops in "
        f"the background. Warm sunny light. {EP}",
    19: "Bird's-eye vertical view of a large green town park in the present day: an oval running track, a football field, tall trees "
        "with round canopies, curving paths, a playground, a small open-air stage with stepped seating, tiny people strolling, a few "
        "town rooftops at the edge. Teal and green palette with warm golden light. No text.",
    20: "Three-level vertical composition of a town park in the present day. At the bottom, joggers on a red running track. In the "
        "middle, children playing on a slide and swings. At the top, a semicircular open-air theatre with a small stage and stepped "
        "seats under tall trees. Cheerful, golden light. " + C,
    21: f"{K}. Night festival in the plaza: string lights, paper streamers, families, vendors with balloons and sweets, a brass band "
        f"with tuba and drums playing on the kiosk, small fireworks in the dark blue sky, warm glowing colors, joyful crowd of "
        f"{TP}. {EP}",
    22: "An old wooden desk in an archive room: a thick open ledger with yellowed ruled pages that are blank, a few faded sepia "
        "photographs of a plaza with blurred figures, a brass magnifying glass, a small lamp with warm glow, dust motes in the light. "
        "A mood of searching and curiosity. No readable writing anywhere.",
    23: f"An elderly man with a white mustache and straw hat gestures as he tells a story to a young woman who listens smiling, both "
        f"sitting on a wrought-iron bench in a town plaza at golden sunset, the octagonal kiosk softly blurred behind them. Warm, "
        f"friendly mood, generic locals. {EP}",
}

out = {}
for n, txt in ESCENAS.items():
    p = txt if txt.rstrip().endswith(C) else f"{txt.rstrip()} {C}"
    out[f"scene-{n:03d}"] = f"{S} {p}"
    assert "scene-%03d" % n in [b["id"] for b in json.load(open("beats.json", encoding="utf-8"))]
assert len(out) == len(json.load(open("beats.json", encoding="utf-8"))), "faltan prompts"
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts; largo medio", sum(map(len, out.values())) // len(out))
