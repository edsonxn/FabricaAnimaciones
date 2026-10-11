# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video.
Beats de VIDEO (1-8): plantilla de dos escenas por clip (combinar=True); el 8 es de 8 s («first four seconds»)."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
A = F["personajes"]["cellar"]
W = F["personajes"]["widow"]
H = F["personajes"]["human"]
WEB = F["objeto"]
MOM = ("a female cartoon cellar spider with a tiny pale beige peanut-shaped body, a small round head with two big round "
       "gentle eyes with long eyelashes, eight extremely long hair-thin pale beige legs with thin dark bands at the knees")
HARV = ("a cartoon harvestman with a single round oval brown body with no waist, two small eyes on top, and eight extremely "
        "long thin dark brown legs")
CRANE = ("a cartoon crane fly with a long thin tan body, two narrow transparent wings and six dangling extremely long thin "
         "legs, with a clumsy goofy face")
HOUSE = "a big hairy brown cartoon house spider with thick legs and grumpy eyes"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
# Ronda 2 (11-oct-2026): Flow coló rótulos («STORAGE», «CARGO», «FURNACE», «whistle», «COUGH!») y marcos en 024/026
NOTXT = "every box, crate, jar and machine is plain and unlabeled with no writing on it"
EDGE = "the drawing runs off all four edges of the image, with no black outline, no frame and no border around it"
HOST = ("a cartoon television host man with short wavy brown hair, a round friendly face, a light blue shirt with rolled up "
        "sleeves and dark trousers")


def clip(a, trans, b, s=5):
    n = {5: "five", 4: "four"}[s]
    return f"Scene one, first {n} seconds: {a} Then {trans}. Scene two, last {n} seconds: {b}"


V = {
    1: clip(f"a dark suburban kitchen at two in the morning lit only by blue moonlight, {H} in pajama pants shuffling sleepily "
            "toward the sink holding an empty glass, yawning.",
            "a hand flips the light switch and a burst of warm light washes across the whole frame",
            f"the same kitchen now brightly lit, {H} frozen with the glass, staring up at the white ceiling corner where {A} "
            f"hangs in {WEB}."),
    2: clip(f"close-up of {A} hanging upside down, its tiny body floating in the middle of its impossibly long thin legs that "
            "radiate out like fine lines, softly swaying.",
            "the camera slowly pulls back through the silk threads of the web",
            f"a wide view of {WEB}, covered in grey dust and old fluff like it has been there for years, with {A} tiny in "
            f"its center, {FULL}."),
    3: clip(f"{H} pulls a broom out of a closet and raises it high toward the ceiling corner with a determined face.",
            "the broom freezes in mid air and the scene peels away like a turning sketchbook page, revealing scene two drawn underneath",
            f"{A} standing proudly in {WEB} like a tiny security guard, holding a tiny flashlight and keeping watch over the "
            "sleeping house below."),
    4: clip(f"{A} calmly facing {HOUSE} three times its size inside the tangled web, while an even bigger scarier spider "
            "peeks from behind.",
            "a gust of grey dust sweeps across the frame and when it passes we are in scene two",
            f"{W} lurking in a dark garage corner under a wooden shelf, its red hourglass glowing, a long dramatic shadow "
            "on the wall behind it."),
    5: clip(f"on a school playground, three cartoon kids whisper a secret, one cupping a hand to another's ear, a drawing of "
            "a long-legged spider with spooky glowing fangs on a sheet of paper in their hands.",
            "the ink lines of the scene come loose, swirl like ribbons and redraw themselves into scene two",
            f"{A} peeking out from behind a big old book lying open on a wooden desk under a warm lamp, with a mysterious "
            "little smile."),
    6: clip(f"a detective lineup wall with simple horizontal height lines and no numbers, three long-legged creatures "
            f"standing in a row under a spotlight: {HARV}, {CRANE}, and {A}.",
            "the camera pushes in quickly toward the three suspects",
            "the same three creatures in the lineup turning their heads to look at each other with confused faces, "
            "question marks floating above them."),
    7: clip(f"{HARV} walking across a sunny green lawn outside a suburban house, stepping over blades of grass and a "
            "fallen leaf.",
            "the harvestman walks toward the camera and covers the frame with its round brown body, then walks away to reveal scene two",
            f"{CRANE} flying clumsily at night around a glowing porch light, bumping into it with little impact stars."),
    8: clip(f"{CRANE} bumping clumsily into a window, while a much smaller normal mosquito flies next to it looking at it "
            "with a puzzled face.",
            "the camera tilts up quickly to the ceiling",
            f"the white ceiling corner of a living room with {A} in {WEB}, waving one long leg hello under a soft "
            "spotlight.", s=4),
}

I = {
    9: f"{A} standing on a wooden kitchen table next to a single grain of white rice exactly the same size as its body, "
       "both seen up close, the spider looking at the rice with curiosity.",
    10: f"Simple diagram on a plain off-white background: {A} with all eight legs stretched out straight, a dotted line along "
        "its tiny body and a much longer dotted line along one leg, the leg about six times longer.",
    11: f"Extreme close-up of one long pale beige leg of {A} showing the thin dark band at the knee joint like a striped "
        "sock, with the spider's big round eye peeking in from the corner of the frame.",
    12: f"Low angle view looking up at {WEB}, {A} in the middle, and the face of {H} at the bottom edge looking up at it, "
        f"{FULL}.",
    13: f"Side by side comparison on a plain off-white background: on the left a perfect neat round spiral orb web with a "
        f"little golden glow, on the right {WEB}, chaotic and messy.",
    14: f"Close-up of {WEB} with threads going in every direction like a tangled ball of yarn, a few grey dust bunnies stuck "
        f"in it like an abandoned attic, but {A} peeking out from the middle with alert eyes.",
    15: f"{A} in the middle of {WEB}, grinning slyly and rubbing two front legs together like it has a clever plan.",
    16: f"A cartoon mosquito flying straight into {WEB}, hitting several threads at once at different angles, little "
        "impact stars at each touching point.",
    17: f"The cartoon mosquito hopelessly tangled in many silk threads, legs wrapped up, annoyed face, while {HOUSE} steps "
        "onto the edge of the web in the background.",
    18: f"{HOUSE} placing one foot on a silk thread of {WEB}, and wavy vibration lines rippling along the threads toward the "
        "center.",
    19: f"{A} in its web with sleepy half-closed eyes, wearing tiny round thick glasses, the tips of its long legs resting "
        "gently on the silk threads.",
    20: f"Close-up of the long leg tips of {A} touching silk threads, glowing yellow vibration ripples traveling up the legs "
        "like signals through a telephone wire.",
    21: f"{A} hanging upside down in {WEB}, and a tiny red alarm bell tied into the threads ringing loudly with motion "
        "lines, the spider instantly alert.",
    22: f"{A} hanging upside down in the middle of {WEB} perfectly still and patient, a simple round wall clock with no "
        "numbers beside it, the sun moving across the window from morning to evening.",
    23: f"Cutaway of a suburban house at night under a big moon: in the bedroom {H} sleeps in bed, and in the ceiling corner "
        f"above, {A} catches a moth in its web.",
    24: f"A tiny boxing ring on a basement floor: in one corner {A}, thin and fragile, in the other corner {W}, big and "
        f"flexing, a small fly referee in the middle, dramatic spotlights, {EDGE}.",
    25: f"A big old-fashioned balance scale: {W} sits on one side pushing it all the way down, while {A} on the other side "
        "flies up into the air.",
    26: f"{W} flexing like a bodybuilder in a dark garage corner, glowing green drops of venom dripping from its fangs, lit "
        f"dramatically from below, {EDGE}.",
    27: "A plain white ambulance with a red stripe and no lettering, flashing lights on, parked outside a suburban house "
        f"at night, {FULL}.",
    28: f"{A} stretching its incredibly long legs as wide as possible like a giant open compass, with a confident smile, "
        f"while {W} looks up at it nervously.",
    29: f"{A} calmly touching {W} from far away with the tip of one very long leg, while the widow swings its short legs in "
        "the air and cannot reach, comic.",
    30: f"{W} stumbling into {WEB}, three legs caught in the threads, surprised face, while {A} watches calmly from a "
        "distance.",
    31: f"{A} hanging back and flinging long ribbons of white silk from its long back legs toward {W}, like a cowboy "
        "throwing a lasso.",
    32: f"Many white silk strands flying through the air in loops, landing one after another on {W}, who tries to dodge.",
    33: f"{W} almost completely wrapped in white silk like a mummy, only its angry eyes showing, while {A} wraps faster and "
        "faster with motion lines.",
    34: f"{A} carefully stepping close to the silk-wrapped {W}, delicately leaning down for one tiny careful bite, calm "
        "like a surgeon.",
    35: f"A cartoon scientist in a white lab coat kneeling in a garage with a magnifying glass, watching {A} next to a "
        "silk-wrapped black widow, writing in a notebook.",
    36: f"{A} standing proudly next to {HOUSE} four times bigger than its body, the big spider completely wrapped in silk.",
    37: f"A tidy garage with tools on the wall, shelves of boxes and the front of a car, {A} in a web high in the corner, "
        f"and {H} giving it a thumbs up, {FULL}.",
    38: f"A basement with a washing machine and stacked boxes: {W} hiding low under a shelf in the shadows, and {A} keeping "
        f"guard high above in the ceiling corner, {NOTXT}, {FULL}.",
    39: f"{A} tiptoeing sneakily across a white wall like a spy, leaving its own web behind, looking over its shoulder.",
    40: f"{A} stepping carefully into a different spider's flat sheet web that leads to a dark funnel hole where "
        f"{HOUSE} is hiding.",
    41: f"Close-up of one long leg of {A} plucking a single silk thread like a guitar string, small musical vibration "
        "lines around it.",
    42: f"Inside its dark funnel hideout, {HOUSE} perks up with big hungry eyes, a thought bubble above it showing a fat "
        "fly stuck in its web.",
    43: f"{HOUSE} rushing out of its funnel excitedly, tongue out, legs a blur, running toward the vibration.",
    44: f"{HOUSE} skidding to a stop in shock, face to face with {A}, who is waiting calmly with a tiny napkin tied around "
        "its neck.",
    45: "A calm marsh at sunrise with tall reeds, a cartoon man in a small rowing boat blowing a little wooden duck call, "
        f"three ducks swimming toward him curiously, {FULL}.",
    46: f"{A} blowing a tiny wooden duck call, while {HOUSE} wearing a silly yellow duck costume walks toward it, "
        "completely fooled.",
    47: f"A small brown house wren peeking hungrily through an open window into a room, staring at {A} in the ceiling "
        "corner.",
    48: f"{A} in its web doing a stretching warm-up like an athlete, lifting its long legs one by one, determined face.",
    49: f"{A} in its web while three threats approach from three sides: a bird beak, {HOUSE}, and a giant human finger.",
    50: f"A giant human finger getting close to {A} in its web, and the spider starting to shake with small motion lines.",
    51: f"{A} whirling around and around in its web so fast that its body becomes a circular spinning blur with motion "
        "streaks, like a spinning top.",
    52: f"The small brown wren squinting in confusion at the web, seeing five blurry ghost copies of {A} at once.",
    53: "The small brown wren with dizzy spiral eyes and little stars circling its head, completely lost in front of a "
        "spinning blur in the ceiling corner.",
    54: f"{H} vacuuming the ceiling with a long vacuum cleaner hose, and {A} vibrating wildly in the corner as the nozzle "
        "approaches.",
    55: f"{A} trying to disappear, half transparent, hiding behind one of its own thin legs, sweating nervously.",
    56: f"A school playground at recess with swings, a slide and a sandbox, cartoon kids gathered in a circle whispering a "
        f"secret, {FULL}.",
    57: "Inside a dark tent at a sleepover, a cartoon kid holding a flashlight under his chin telling a scary story to two "
        "wide-eyed friends, a giant shadow of a long-legged spider on the tent wall.",
    58: f"A spooky old horror movie style illustration: a giant monstrous version of {A} with glowing red eyes and huge "
        "fangs looming over a tiny town at night.",
    59: f"{A} laughing and shaking its head in its web, holding a small broken spooky monster mask of itself, on a plain "
        "light wall with nothing else around it.",
    60: "A cartoon scientist in a lab looking through a microscope at one tiny drop on a glass slide, shrugging and "
        "unimpressed, test tubes on the counter.",
    61: f"Close-up of {A} opening its mouth to show two tiny but real fangs, seen through a big round magnifying glass.",
    62: f"A simple cartoon television studio with big cameras and bright lights, {HOST} sitting at a table holding out his "
        "bare forearm, no logos, no screens with writing.",
    63: f"Close-up of the bare forearm of {HOST}, with {A} sitting on it about to bite, the host wincing with his eyes "
        "squeezed shut, in the television studio.",
    64: f"{HOST} sitting at the studio table smiling and shrugging, looking at a tiny red dot on his forearm with small wavy "
        "heat lines that are already fading.",
    65: f"Side by side: a menacing cartoon mosquito with a long needle nose, and {A} looking innocent and harmless, while "
        f"{H} scratches an itchy red mosquito bite on his arm.",
    66: f"{HARV} walking through the grass, holding up its empty legs and smiling innocently, no fangs at all.",
    67: f"{MOM} in her web holding her egg bundle close, with small hearts floating around her, warm soft light.",
    68: "A cartoon garden spider wrapping a round white silk egg sac on a leaf, then walking away waving goodbye to it.",
    69: f"{MOM} holding a round bundle of tiny pale pink eggs gently in her jaws, hanging in her web.",
    70: f"Close-up of {MOM} with a little bundle of round eggs held in her jaws, loosely wrapped in just a few threads of "
        "silk, blank calendar pages flying past behind her.",
    71: f"Tiny baby cellar spiders hatching from the egg bundle and clustering around {MOM} in her web, all with big eyes.",
    72: "Tiny baby cellar spiders walking away along silk threads toward different ceiling corners of a room, each "
        "carrying a tiny suitcase.",
    73: f"{A} sitting in its web next to an empty little plate, still smiling, dusty, with blank calendar pages falling "
        "around it.",
    74: f"A bird beak grabbing one long leg of {A}, and the spider escaping, leaving that leg behind and waving cheerfully.",
    75: f"{A} walking happily along the ceiling on seven long legs, one leg with a tiny bandage stump, two small musical "
        "notes floating near its head, no words.",
    76: f"An old version of {A} with fluffy grey eyebrows and a tiny walking cane, still sitting in the same ceiling corner.",
    77: f"{A} wearing a tiny backpack, standing on top of a big spinning cartoon globe of the Earth.",
    78: f"A warm green subtropical Asian landscape with rice terraces, palm trees and misty mountains, {A} sitting on a big "
        "leaf in the foreground.",
    79: f"{A} peeking out of a plain wooden crate on the deck of an old sailing ship crossing a blue ocean, seagulls above, "
        f"{NOTXT}.",
    80: "A simple round cartoon globe showing every continent dotted with tiny houses, each with a small long-legged spider "
        "in its window, except snowy Antarctica at the bottom with penguins and no houses.",
    81: f"A row of very different buildings: a city apartment block, a farmhouse, a small castle and a beach house, each "
        f"with {A} in a corner of one window.",
    82: f"An old Victorian living room with a grandfather clock, a rocking chair and a fireplace, dusty cobwebs hanging in "
        f"every corner of the ceiling, {FULL}.",
    83: f"{H} standing in a basement looking up in surprise at many cellar spiders in many ceiling corners, {FULL}.",
    84: f"{A} in its web eating a tiny gnat with a tiny fork and knife, like at a fancy restaurant.",
    85: f"A mosquito, a gnat, a moth, a housefly and a small beetle all caught nervously in {WEB}.",
    86: f"A cozy basement with an orange furnace and shelves, cellar spiders in every corner of the ceiling, {NOTXT}, {FULL}.",
    87: "Cutaway view of a basement at night full of hidden bugs, crickets, silverfish, flies and moths, with cellar spiders "
        "catching them from their webs.",
    88: f"{A} wearing a tiny pest control uniform and holding a flashlight, next to a small glowing red warning light on "
        "the wall.",
    89: f"{H} with a big magnifying glass looking at a spider in a ceiling corner, puzzled, scratching his head.",
    90: f"{A} lit from behind by a lamp so its pale body looks almost see-through and glowing.",
    91: f"{A} with its long legs stretching out of the frame on every side, seeming to go on forever.",
    92: f"Split image, top half and bottom half: at the top, {A} high in a bright ceiling corner; at the bottom, {W} low in "
        "a dark spot near the floor.",
    93: f"Close-up of {W} upside down showing its glossy round black belly with the bright red hourglass mark, its legs "
        "short and thick.",
    94: f"{W} hiding low under a wooden shelf in a garage, right next to a stack of firewood, in the shadows.",
    95: f"Old cardboard boxes stacked against the bottom of a garage door, {W} peeking from a gap between them, and "
        f"{A} high above in a corner.",
    96: f"{H} pulling his hands quickly away from a dark low shelf with a startled face, while {W} peeks out.",
    97: "A plain unlabeled spray can spraying a big grey cloud into the corner of a room, with a worried face drawn on the "
        "cloud.",
    98: f"The grey spray cloud hitting {A} and some flies at the same time, all of them coughing with eyes squeezed shut "
        "and tongues out, no speech bubbles, no words.",
    99: "A swarm of flies and cockroaches marching happily back into a kitchen, while the corner web above is empty and sad.",
    100: f"{H} relaxing in an armchair reading, while {A} works quietly in the ceiling corner, both content.",
    101: f"{H} sliding a clear plastic cup over {A} on the wall and slipping a sheet of paper underneath, carefully.",
    102: f"{H} standing on a step stool vacuuming old dusty webs out of the ceiling corners with a long hose.",
    103: f"{H} sealing a crack around a window frame with a caulking gun, and a small dehumidifier running in a damp "
         "basement next to him.",
    104: f"{A} packing a tiny suitcase and waving goodbye as it leaves through a gap under the door, on its own.",
    105: f"{H} on his phone keeping a safe distance from a garage shelf where {W} sits, a plain van with no lettering "
         "parked outside.",
    106: f"The kitchen at night again, {H} holding a glass of water and looking up with a gentle smile at {A} in {WEB}.",
    107: f"{A} as a night guard standing watch over the dark ceiling corner, holding a tiny flashlight with its long legs, "
         "the moon in the window.",
    108: f"{A} catching a mosquito in its web with one quick long leg.",
    109: f"{A} standing humbly next to a silk-wrapped {W} hanging like a trophy, giving a small modest shrug.",
    110: f"{H} putting the broom back in the closet and turning off the light, while {A} waves goodbye from the ceiling "
         "corner in the moonlight.",
}

bs = json.load(open("beats.json", encoding="utf-8"))
assert len(bs) == len(V) + len(I), (len(bs), len(V) + len(I))
out = {}
for k, b in enumerate(bs, 1):
    assert (b["tipo"] == "video") == (k in V), (b["id"], b["tipo"])
    out[b["id"]] = E + (V[k] if k in V else I[k]) + C
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts ({len(V)} video + {len(I)} imagen)")
