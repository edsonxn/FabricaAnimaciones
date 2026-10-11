# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video.
Beats 1-7 = clips de video de 10 s con DOS escenas y transición dibujada; el resto, imagen."""
import json

import guion

F = guion.FICHA
E = F["estilo"] + ". "
C = " " + F["cierre"]
H = F["personajes"]["human"]
Y = F["objeto"]
EY = "with big round expressive eyes"
MON = f"a cartoon monarch butterfly with bright orange wings with black veins and white dots, {EY}"
BEE = f"a small round cartoon honey bee with yellow and black stripes, {EY}"
BUM = f"a big fat fuzzy cartoon bumble bee queen with a tiny gold crown, {EY}"
LADY = f"a round red cartoon ladybug with black spots, {EY}"
STINK = f"a cartoon stink bug with a flat brown shield-shaped body, {EY}"
WOOL = f"a fuzzy cartoon woolly bear caterpillar with black fur at both ends and a rusty orange band in the middle, {EY}"
CLOAK = f"a cartoon mourning cloak butterfly with dark maroon wings edged with a pale yellow border and a row of blue dots, {EY}"
MOSQ = f"a skinny gray-brown cartoon mosquito with a thin plain body without stripes, long thin legs and a long needle nose, {EY}"
ANT = f"small black cartoon ants {EY}"
FIRE = f"a cartoon firefly with a glowing yellow tail, {EY}"
CIC = f"a pale brown cartoon young cicada with big front digging claws, {EY}"
NYM = f"a stubby green-brown cartoon dragonfly nymph with no wings, six legs, {EY}"
MANT = f"a green cartoon praying mantis with folded front arms, {EY}"
CRICK = f"a brown cartoon cricket, {EY}"
SNOWF = "tiny black cartoon snow fleas, each a little dark blue-black oval with two short antennae and dot eyes"
OFF = "Simple diagram on a plain off-white background:"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"


def clip(a, t, b):
    return f"Scene one, first five seconds: {a} Then {t} Scene two, last five seconds: {b}"


P = {
    1: clip(f"wide view of {Y} on a bright summer day, grass waving, flowers swaying, dozens of tiny insects flying everywhere, the camera slowly pushing in.",
            "the camera dives down into the flower bed and a big yellow flower fills the whole frame, and its round center becomes the background of scene two.",
            f"close-up among the flowers where {BEE} lands on a petal, {CRICK} rubs its wings in the grass below, and {MOSQ} lands on the arm of {H}, who slaps at it."),
    2: clip(f"the summer backyard seen from grass level, crowded with ants marching, beetles crawling, bees and butterflies flying in every direction, lively and busy.",
            "a wave of pale blue frost sweeps across the frame from left to right, redrawing everything it touches in cold blue and white ink.",
            "the very same backyard at dawn covered in white frost, completely still and empty, not one insect, a single leaf falling slowly."),
    3: clip("the frozen silent backyard under snow, bare oak tree, frozen pond, a tiny wooden grave marker shaped like a blank plank stuck in the snow, cold wind blowing.",
            "the snow melts away in a spreading circle of green as if someone wiped the page clean, and the ink lines redraw themselves with leaves and flowers.",
            "the same backyard on a sunny spring morning, flowers opening, and bees, butterflies, ants and ladybugs popping out from everywhere at once."),
    4: clip(f"{H} standing in the snowy backyard scratching his head and looking around, a big question mark popping up above him, the camera circling slightly.",
            "the question mark grows until it fills the frame, then its ink lines come loose, swirl like ribbons and redraw themselves into scene two.",
            f"{MON} flying high over a simple cartoon map of North America, and as it passes, a small green caterpillar on a leaf below turns into a block of shiny blue ice."),
    5: clip(f"inside a cozy living room, {H} reading on a sofa while the camera slowly pushes into the wall behind him, revealing in cutaway several small cartoon bugs asleep inside the wall.",
            "the scene peels away like a turning sketchbook page, revealing scene two drawn underneath.",
            f"{OFF[:-1]} style, a small green cartoon beetle {EY} standing next to a big cartoon thermometer whose blue liquid drops lower and lower, the beetle starting to shiver and turn pale blue."),
    6: clip("an autumn garden where a cold blue wind blows across the frame, and a small green cartoon beetle on a leaf slows down, stiffens and gets covered in frost crystals.",
            "a splash of black ink spreads across the frame and washes away to reveal scene two.",
            "a secret meeting under a mushroom: a bee, an ant, a ladybug, a butterfly and a caterpillar gathered around a tiny table looking at a blank blueprint, nodding and pointing like generals with a plan."),
    7: clip("a fast funny montage in one continuous shot: a butterfly zooms away to the right with a tiny suitcase, then a group of ladybugs hug together in a tight shivering pile.",
            "a gust of falling autumn leaves sweeps across the frame and when it passes we are in scene two.",
            "an ant digging straight down into the soil with a tiny shovel, a stink bug sneaking through a window into a house, and a caterpillar sitting calmly as a block of ice forms around it, giving a thumbs up."),
    8: f"A row of five small cartoon insects lined up on a twig like contestants: a monarch butterfly, a honey bee, a ladybug, a woolly caterpillar and an ant, all {EY}, autumn leaves behind them.",
    9: f"{MON} at the edge of an autumn garden waving goodbye with one wing, a tiny suitcase beside it, orange leaves falling.",
    10: "A simple cartoon map of North America seen from above with dozens of tiny orange butterflies streaming south from Canada and the United States, drawn with soft dotted trails.",
    11: f"A balance scale with {MON} on one side and a single metal paper clip on the other, the paper clip side lower, on a wooden desk.",
    12: f"A long line of cartoon monarch butterflies flying over desert, rivers and mountains toward distant green forested peaks under a big sky, a dotted trail behind them, {FULL}.",
    13: "A mountain fir forest where every tree trunk and branch is completely covered by thousands of orange monarch butterflies clustered together like orange leaves, soft sunlight.",
    14: f"{MON} flying alone over a hill holding a tiny blank folded map upside down and looking unsure, with small question marks around it.",
    15: f"{MON} in a sunny summer garden next to a small sand hourglass that is almost empty, flowers around.",
    16: f"A strong determined {MON[2:]} wearing a tiny aviator cap and goggles, standing on a late-summer sunflower, with a much bigger sand hourglass full of sand beside it.",
    17: "A single cartoon monarch butterfly flying toward a sunset over mountains, seen from behind, tiny and brave against a huge orange sky.",
    18: f"A big green cartoon dragonfly {EY} flying south next to a monarch butterfly, both looking sideways at each other in surprise.",
    19: "A weather radar screen in a control room showing a big green blob shaped like a swarm, while a huge swarm of cartoon dragonflies flies past the window outside, a cartoon weather person with a round white head looking puzzled.",
    20: "A white wooden beehive box in a snowy garden with a tiny thread of warm air rising from it, snow on its roof, bare trees behind.",
    21: f"{BEE} standing at the hive entrance with tiny crossed arms and a stubborn face, refusing to leave, snowflakes falling around.",
    22: "Cutaway view of the inside of a beehive in winter showing hundreds of small cartoon bees packed into one tight round ball on the honeycomb, with a larger queen bee in the very center.",
    23: f"Close-up of {BEE} shivering hard with small vibration lines around its body, its wings held perfectly still, other bees pressed around it.",
    24: "Cutaway of the winter bee ball drawn like a heat map, glowing warm orange and red in the center with a tiny sun symbol, and cool blue on the outer edge.",
    25: "A snow-covered beehive in a blizzard seen from outside, with a small cutaway window showing the warm orange glowing ball of bees inside.",
    26: "Top view of the round ball of cartoon bees with curved arrows showing bees moving from the cold blue outer ring to the warm orange middle, like taking turns.",
    27: "Honeycomb cells full of golden honey in summer light, with cartoon bees pouring honey from tiny buckets into the cells.",
    28: "A cartoon bee in winter feeding a spoon of honey into a tiny glowing furnace with a little door, other bees warming their feet around it.",
    29: f"{BUM} standing apart from a small round bumble bee nest in the grass, looking back at it, autumn leaves falling.",
    30: "A quiet empty bumble bee nest under frosty grass with a few tiny wilted flowers laid beside it, soft gray light, calm and a little sad.",
    31: f"{BUM} flying away alone over frosty grass, determined, with a rising sun behind her.",
    32: f"{BUM} digging a small round hole in the soil with her front legs, dirt flying behind her, autumn leaves on the ground.",
    33: f"Cutaway view of soil under snow showing {BUM} curled up asleep alone in a small round chamber a few inches below the surface, with a tiny pillow.",
    34: f"{BUM} waking up and climbing out of a hole in spring grass, stretching, with crocus flowers blooming around her.",
    35: f"{BUM} flying very low over spring grass, peering down at the ground with one leg shading her eyes, while {H} watches curiously.",
    36: f"{BUM} happily inspecting an old mouse hole in the ground under a tuft of grass like a house buyer, giving a thumbs up.",
    37: "A big pile of cartoon ladybugs in tiny sleeping bags and nightcaps having a sleepover under a piece of bark, some with tiny pillows.",
    38: "A mountain rock and a fallen log in autumn completely covered with thousands of red cartoon ladybugs clustered together like a red carpet.",
    39: "Cutaway view of an old log showing a crack inside packed tight with red cartoon ladybugs snuggled side by side.",
    40: f"{OFF} a tight cluster of red cartoon ladybugs hugging, with a small warm orange glow around the group and a single blue water drop crossed out beside them.",
    41: f"{LADY} asleep with a tiny switch on its side turned to off, a small round belly, and little z-shaped sleep swirls drawn as curly lines above it.",
    42: f"{STINK} standing on a windowsill outside a cozy lit house in autumn, looking through the glass with wide greedy eyes, rubbing its front legs together.",
    43: f"A line of three cartoon bugs, {STINK}, a gray cartoon fly and an orange cartoon lady beetle, sneaking along the outside wall of a house on tiptoe.",
    44: "Close-up of a window frame and house siding with a tiny gap, and a cartoon stink bug squeezing its flat body through the gap, only its back legs still outside.",
    45: f"{STINK} inside a house walking right past a full fruit bowl with its eyes closed and nose up, ignoring it, with a fork-and-knife symbol and a heart symbol both crossed out in red beside it.",
    46: "Cutaway view of the inside of a house wall with pink insulation, where several cartoon stink bugs sleep peacefully in a row, each with a tiny blanket.",
    47: f"{H} lying on a sofa looking up in surprise at {STINK} walking slowly across the white ceiling, looking lost and sleepy, snow visible through the window.",
    48: "A theater stage with red curtains opening and a single spotlight on a small empty leaf in the center, dramatic and mysterious.",
    49: f"A friendly portrait of {WOOL}, crawling on an autumn leaf, looking at the viewer.",
    50: f"{WOOL} shaking its head no at a signpost with two blank arrow boards, one pointing to a sunny beach scene and one pointing to a cozy house.",
    51: f"{WOOL} curled into a tight ring under a brown leaf while frost crystals creep over its fur and it turns icy blue.",
    52: "A woolly caterpillar curled in a ring and frozen completely solid like a little ice sculpture, pale blue, with a tiny heart symbol beside it that has stopped, snow all around.",
    53: f"{OFF} {WOOL} drinking from a tiny bottle of bright green liquid marked only with a snowflake symbol, its body filling with green from the tail up.",
    54: "Close-up diagram of round cartoon body cells, each wrapped in a green protective glow, with sharp blue ice crystals outside that cannot get in.",
    55: f"{WOOL} in spring sunshine shaking off the last drops of melted ice and strolling away across green grass, whistling, with small flowers around.",
    56: f"{CLOAK} raising one wing like a student with an idea, a small lightbulb above its head, on a bare winter branch.",
    57: f"{CLOAK} standing proudly on tree bark in falling snow, wearing a tiny scarf.",
    58: f"Cutaway of a tree trunk in winter showing {CLOAK} with wings folded, wedged snugly into a narrow crack under the bark, snow outside.",
    59: f"{CLOAK} flying over a meadow that is still half covered in melting snow, the very first butterfly of spring, with one early yellow flower below.",
    60: "A bare winter bush with several twigs and dry leaves, where one twig and one leaf are drawn with tiny hidden closed eyes, like a find-the-hidden-object puzzle.",
    61: "A green and black striped cartoon swallowtail caterpillar on a twig beginning to wrap itself into a brown chrysalis, half transformed.",
    62: "A brown chrysalis attached to a branch that looks almost exactly like a short broken twig, next to a real broken twig for comparison, with a magnifying glass showing its tiny closed eyes.",
    63: "A large brown silk cocoon hanging from a bare winter branch wrapped in a dry leaf, swaying among other dead leaves, snow falling.",
    64: f"{H} in a winter coat walking through a snowy garden looking straight at a bare bush, not noticing the cocoon and the chrysalis hanging right in front of his nose.",
    65: "Cutaway view of a cocoon showing inside a sleeping cartoon moth half formed, with folded patterned wings slowly taking shape, drawn with soft glowing lines.",
    66: f"{MOSQ} peeking out from behind a snowy tree with a sneaky grin, while {H} in the background groans with his hand on his forehead.",
    67: f"Cutaway of a hollow log in snow with several of {MOSQ[2:]} hanging inside asleep, wings folded.",
    68: f"A dark basement corner and a round storm drain opening, with a few cartoon mosquitoes resting on the wall, and on the right a female mosquito laying a row of tiny dark eggs at the edge of a puddle.",
    69: "A frozen puddle in winter seen in cutaway, with tiny dark cartoon mosquito eggs locked inside the ice, each with a small calm sleeping face.",
    70: "The same puddle in spring with the ice melting, and tiny cartoon mosquito larvae wriggling out of the eggs into the water, sunshine above.",
    71: f"A cloud of cartoon mosquitoes rising from a spring puddle toward {H}, who has just stepped outside in a t-shirt with a happy face that is turning to alarm.",
    72: "Cutaway of soil under a lawn in late autumn showing a column of small black cartoon ants carrying their eggs downward through a tunnel, deeper and deeper, with a dotted frost line drawn across the soil above them.",
    73: "Cutaway of a deep underground ant chamber in winter with small black cartoon ants huddled in a tight group around a larger queen ant, the tunnel above blocked with a plug of soil.",
    74: "A small ant hill in a snowy lawn with a tiny blank wooden sign hanging on a tiny chain across its entrance, like a closed shop.",
    75: "A summer night garden with glowing yellow firefly lights floating over the grass, and an arrow of dotted light leading down into the soil.",
    76: f"{FIRE} flying over a summer meadow at dusk next to a tiny calendar page with only a few days marked by small check marks.",
    77: "Cutaway of soil and a strip of bark showing a small cartoon firefly larva, a flat segmented dark body with big round eyes, crawling through a tunnel and chasing a tiny cartoon snail.",
    78: "Cutaway of soil under snow showing a cartoon firefly larva curled up asleep, its tail giving a soft green glow that lights the little chamber, two snowflake symbols above the ground.",
    79: "Cutaway of deep soil with tree roots reaching down, and a long ladder going far below the ant chambers toward a faint light at the bottom.",
    80: f"Cutaway of soil showing {CIC} hugging a thick tree root and drinking from it through a tiny straw, looking content.",
    81: f"Cutaway of soil with {CIC} sitting calmly underground while above ground four small versions of the same oak tree show the seasons passing, snow, flowers, green leaves, orange leaves.",
    82: f"A summer tree trunk at night with dozens of cartoon cicadas climbing out of small holes in the ground and up the bark, one already singing with musical swirls drawn as curly lines.",
    83: f"{H} mowing an ordinary green lawn, completely unaware, while a cutaway below shows hundreds of pale cartoon cicada nymphs sitting in the soil under his feet, all looking up.",
    84: "A frozen backyard pond in winter with snow on the banks and bare cattails, calm and still, a small round window drawn in the ice showing dark water below.",
    85: f"Underwater view below the pond ice, with {NYM} crawling on the muddy bottom among water plants, wide awake, light filtering through the ice above.",
    86: f"Underwater view below the ice of {NYM} lunging and catching a tiny cartoon water bug with its extended jaw, bubbles rising.",
    87: f"{OFF[:-1]} style cutaway of a pond in winter with a layer of ice on top colored pale blue and the water at the bottom colored slightly warmer, a small thermometer at the bottom, and a relaxed dragonfly nymph resting there.",
    88: "A frosty autumn meadow at dusk with tall dry grass and a few last flowers wilting, quiet and empty, a single leaf falling.",
    89: f"{CRICK}, a green cartoon grasshopper and {MANT} sitting together on a frosty log at sunset, looking at the horizon, calm and peaceful.",
    90: "A cartoon grasshopper gently pushing tiny eggs into the soil with the tip of its body, and a cricket doing the same nearby, autumn leaves around.",
    91: f"{MANT} on a twig carefully covering a cluster of eggs with white foam, the foam hardening into a tan ridged case shaped like a tiny sleeping bag.",
    92: "Cutaway of a tan praying mantis egg case on a snowy twig, showing rows and rows of tiny sleeping baby mantises tucked inside like in bunk beds.",
    93: "A snowy winter twig with a tan mantis egg case on it and a few empty dry leaves below, the faint outlines of tiny mantises visible inside, soft morning light.",
    94: "A bright sunny winter day in a snowy backyard with a bare oak tree, blue shadows on the snow, sparkling light.",
    95: f"{H} in a winter coat crouching at the base of a tree and looking through a magnifying glass at snow sprinkled with hundreds of tiny black specks like pepper.",
    96: f"Extreme close-up of the snow surface with {SNOWF}, hopping and strolling happily across the snow, one wearing tiny sunglasses.",
    97: f"{OFF} one tiny black cartoon snow flea with a transparent body, inside it small shield shapes blocking sharp blue ice crystals from growing.",
    98: "A cartoon scientist with a round white head, dot eyes, glasses and a white lab coat in a laboratory looking through a microscope at a tiny black snow flea, with a medical cooler box on the table beside it.",
    99: f"{Y} in winter covered with snow, quiet, with faint soft glowing dots drawn under the snow, under the bark and in the pond to show hidden life everywhere.",
    100: "Cutaway of a snowy garden showing many small cartoon bugs asleep in different hiding places at once: under leaves, inside stems, under bark and in the soil, each with a tiny pillow.",
    101: "Three hiding places shown together in one garden scene without panel borders: a pile of brown dead leaves, a clump of dry hollow flower stems, and an old mossy log by a wooden fence, each with a pair of tiny sleepy eyes peeking out.",
    102: f"{H} in autumn raking every last leaf into big paper yard bags lined up at the curb, with tiny worried eyes peeking out of the top of one bag.",
    103: "A paper yard bag at the curb with a cutaway showing inside a sleeping butterfly chrysalis, a firefly larva and a bumble bee queen among the leaves.",
    104: f"{H} smiling and leaning his rake against the fence, leaving a soft layer of autumn leaves under the oak tree and in the flower bed, a ladybug on a leaf giving him a thumbs up.",
    105: f"{Y} under deep snow at blue dusk, with warm light in the window of the house behind it.",
    106: "A single cutaway picture of a winter yard showing all four hiding places at once: ants and a cicada in the soil, a butterfly under tree bark, stink bugs inside a house wall, and a dragonfly nymph under pond ice.",
    107: "Many small cartoon bugs in their separate hiding places all opening one eye at the same moment as a warm ray of sunlight reaches them through the melting snow.",
    108: f"{Y} on the first warm spring morning, snow gone, flowers opening, and bees, butterflies, ladybugs, ants and fireflies bursting out everywhere in a joyful noisy crowd, {H} smiling in the middle.",
}

beats = json.load(open("beats.json", encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
assert all((b["tipo"] == "video") == (k < 7) for k, b in enumerate(beats))
out = {b["id"]: E + P[k + 1] + C for k, b in enumerate(beats)}
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts")
