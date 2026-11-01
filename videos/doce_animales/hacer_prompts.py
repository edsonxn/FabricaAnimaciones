# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat, 195: 4 clips combinados + 191 imágenes) y clips_climax.json (3 clips para
efectos.py) con la FICHA de guion.py. Correr desde la carpeta del video.
Claves por TEXTO de beat (el inicio de `texto`), no por número: sobrevive a un nuevo troceo de `beats` (manual WND,
§ «Hallazgos de sin_medicina»). Tarjetas de cuenta regresiva (12…1): llevan el numeral como único texto."""
import json

import guion

F = guion.FICHA
P = F["personajes"]
E = F["estilo"] + ". "
C = " " + F["cierre"]
CN = (" The only text in the picture is that single red numeral, no letters, no other words, no logos, no watermark. "
      "No speech bubbles.")
(PO, LZ, BA, SN, TO, BB, DR, GS, GB, HF, MI, LB, LF, TK, H) = (P[k] for k in (
    "possum", "lizard", "bat", "snake", "toad", "bumble", "dragon", "garden", "beetle", "hover", "milli", "lady",
    "lantern", "tick", "human"))
YARD = F["objeto"]
WASP = ("a cartoon yellowjacket wasp with a sharp yellow and black striped body, two pairs of clear wings, long thin "
        "antennae, a narrow waist and a pointy stinger")
SC = "a simple cartoon scientist with a round white head, dot eyes, round glasses and a white lab coat"
DOG = "a cartoon golden retriever dog with floppy ears and a red collar"
FULL = "the scene filling the whole image to every edge with no white margin and no panel outline"
EDGE = "the drawing runs off all four edges of the image, with no black outline, no frame and no border around it"
NOTXT = "every box, bottle, can, sign and screen is plain and unlabeled with no writing on it"


def card(n, who):
    return (f"A huge hand-drawn red numeral \"{n}\" with a thick black outline on the left third of the frame, and on the "
            f"right {who}, on a plain light backyard background, {EDGE}.")


# Tarjetas: inicio del texto del beat -> (numeral, quién)
N = {
    "might be completely wrong. Number twelve": (12, f"{LB} standing proudly, its tiny silver knight helmet shining"),
    "Number eleven. The millipede": (11, f"{MI} curled into a neat spiral coil with a shy smile"),
    "Number ten. The one that looks like a wasp": (10, f"{HF} hovering in the air with a sly bluffing grin"),
    "Number nine. The black beetle": (9, f"{GB} running fast with its tiny red headlamp beam shining"),
    "and let it go by the garden. Number eight": (8, f"{GS} sitting in a big round web with a thick white zigzag"),
    "and hangs it near the web. Number seven": (7, f"{DR} zooming through the air with its wings blurred"),
    "eating mosquito larvae. Number six": (6, f"{BB} hovering with a big friendly grin"),
    "Number five. The toad": (5, f"{TO} sitting with raindrops bouncing off its tiny yellow rain hat"),
    "Number four. The snake in the garden": (4, f"{SN} coiled in a friendly S shape"),
    "want it gone. Number three": (3, f"{BA} hanging upside down from a branch and smiling"),
    "Number two. The little lizard": (2, f"{LZ} doing a push up on top of a wooden fence post"),
    "And now, number one": (1, f"{PO} standing tall with a proud grin"),
}

# Clips combinados (primeros 40 s): inicio del texto -> (escena A, transición, escena B)
VID = {
    "It is eleven at night": (
        f"night in {YARD}, {H} carrying a full plain trash bag down the driveway toward the metal trash cans at the curb "
        f"under a lone porch light",
        "a gust of dark night wind and dry leaves sweeps across the frame and when it passes we are in scene two",
        f"close on the dark gap behind the metal trash cans, where {PO} pokes out its pale pointy face and hisses with its "
        f"mouth wide open, while {H} jumps back startled"),
    "Beady black eyes": (
        f"extreme close-up of {PO} hissing at the camera, its beady black eyes shining in the porch light and its mouth wide "
        f"open showing many tiny sharp white teeth",
        "the camera pushes into its dark open mouth until the darkness fills the frame, and that dark shape becomes the dark "
        "doorway of the garden shed in scene two",
        f"{H} grabbing a plain shovel leaning on the garden shed at night, then freezing as {PO} looks up at him with big "
        f"sad beady eyes"),
    "That strange little animal": (
        f"{PO} sitting proudly on top of a metal trash can lid in the porch light like a good neighbor, waving one little paw "
        f"at {H}",
        "the ink lines of the scene come loose, swirl like ribbons and redraw themselves into scene two",
        f"a wide cutaway view of a house and backyard at dusk with hidden animals peeking out of the shadows: {SN} under a "
        f"bush, {TO} by the porch steps, {BA} under the roof edge and {GS} in its web between tomato plants"),
    "And they are quietly working": (
        f"the same backyard in morning light with the animals busy working like a little crew: {LB} eating aphids on a "
        f"rose, {TO} catching a slug and {BB} on a tomato flower",
        "the scene peels away like a turning sketchbook page, revealing scene two drawn underneath",
        f"a long row of small friendly cartoon backyard animals standing proudly on top of a wooden fence at sunset, a "
        f"ladybug, a millipede, a hover fly, a beetle, a yellow spider, a dragonfly, a bumblebee, a toad, a snake, a bat, a "
        f"lizard and an opossum, and {H} looking up at them amazed"),
}

# Imágenes: inicio del texto -> escena
I = {
    # gancho
    "And at the very end, two": f"{LF} and {TK} side by side on a tree trunk at night, scheming with sneaky narrow eyes and sinister grins, lit from below by a red glow, {FULL}",
    "Plus one famous number": f"{H} sitting on a sofa at night staring with wide eyes at a glowing smartphone whose screen shows only a cartoon picture of {PO} inside a golden star burst, {NOTXT}, {FULL}",
    "Five thousand ticks a summer": f"{PO} standing like a champion on top of a huge heap of tiny dark ticks, flexing proudly with sparkles around it, {FULL}",
    # 12 mariquita
    "The ladybug. Nobody wants": f"Close-up of {LB} sitting on a bright green rose leaf with a sweet smile, and {H} in the soft background smiling at it, {FULL}",
    "But a lot of people spray them": f"{H} spraying a plain spray bottle at a rose bush covered in tiny green aphids, and {LB} on a leaf caught in the mist with a shocked face, {NOTXT}, {FULL}",
    "And that is a mistake, because a ladybug": f"Low angle view of {LB} standing heroically on a rose stem against a bright blue sky, chest out, {FULL}",
    "tank built to eat aphids": f"{LB} drawn as a tiny armored tank rolling along a rose stem toward a crowd of panicking tiny green aphids, its silver knight helmet like a tank hatch, speed lines, {FULL}",
    "One ladybug can eat dozens": f"{LB} sitting at a tiny table with a napkin in front of a towering stack of plates piled with tiny green aphids, eating happily, {FULL}",
    "Its babies are even hungrier": f"Close-up of a ladybug larva on a leaf, a small long spiky black and orange creature shaped like a tiny alligator with six legs, munching aphids, while a giant cartoon thumb hovers above it ready to squish, {FULL}",
    "thinking they are pests": f"{H} gently picking up {LB} on the tip of one finger and looking at it closely in a sunny garden, {FULL}",
    "it leaves a yellow drop": f"Extreme close-up of a fingertip with {LB} on it and a tiny shiny yellow drop on the skin, and {H} making a grossed-out face in the background, {FULL}",
    "It is bitter blood": f"A cartoon sparrow spitting {LB} out of its beak with a disgusted face and its tongue out, the ladybug flying away unharmed with tiny yellow droplets at its leg joints, {FULL}",
    "Gross. And brilliant": f"{LB} winking at the viewer and giving a thumbs up with one leg, a sparkle on its silver knight helmet and a warm glow behind it, {FULL}",
    # 11 milpiés
    "of them curled up in the garage": f"A dim garage floor seen from above with dozens of small curled-up brown millipedes scattered near the door, and {H} standing in the doorway with a horrified face holding a broom, {NOTXT}, {FULL}",
    "But a millipede has no venom": f"{MI} standing calmly with an innocent face between a drawing of a wasp stinger and a drawing of a venom drop, each crossed out with a red circle-and-slash symbol, {FULL}",
    "and its tiny jaws are too weak": f"Extreme close-up of {MI} trying to nibble a giant cartoon fingertip with no effect at all, the finger not even noticing, {FULL}",
    "It does not even hunt": f"Low ground-level view under a log: {MI} happily munching a brown dead leaf on a damp piece of rotting wood, with moss and little mushrooms around, {FULL}",
    "And no, most of them do not have": f"{MI} raising its front end and looking down at its many little legs with a puzzled face and a puzzled swirl above its head, {FULL}",
    "Most have far fewer": f"{SC} kneeling at the mouth of a deep narrow drill hole in red desert ground, shining a flashlight down into the dark, {FULL}",
    "Australia found one with more": f"Cutaway of a deep underground hole in red soil, where a super long, very thin, pale cream millipede with hundreds and hundreds of tiny legs lies coiled in the dark, lit by a flashlight beam from above, {FULL}",
    "Inside your house, it dries out": f"{MI} lying on a dry white tile floor inside a house looking thirsty and tired, its gray beanie drooping, {FULL}",
    "Just sweep it into a dustpan": f"{H} gently sweeping {MI} into a dustpan with a small broom and carrying it out the back door toward a leafy flower bed, {FULL}",
    # 10 mosca sírfida
    "You are eating lunch on the porch": f"{H} sitting at a small table on a sunny back porch eating a sandwich with a glass of lemonade, a tiny striped insect approaching in the distance, {FULL}",
    "insect hovers right in front": f"Side view close-up of {H} going cross-eyed as {HF} hovers perfectly still right in front of his nose, {FULL}",
    "Your hand goes for the fly swatter": f"{H} frozen mid-swing with a plain fly swatter raised, while a big round magnifying glass in the foreground shows {HF} up close, {FULL}",
    "It is dressed up as a wasp": f"{HF} standing in front of a mirror trying on a yellow and black striped wasp costume with a pointy fake stinger, admiring itself, {FULL}",
    "It has no stinger at all": f"A cartoon sparrow on a branch backing away nervously from {HF}, which puffs out its striped body and makes a fake scary face, {FULL}",
    "Here is how to tell": f"Side view of {WASP}, its two pairs of wings spread wide with a soft glow, on a plain light garden background, {EDGE}",
    "and long antennae. A hover fly": f"A split picture: on the left {WASP} showing its long antennae, on the right {HF} showing its ONE single pair of wings, the two facing each other, {FULL}",
    "tiny antennae, and huge eyes": f"Extreme close-up of the head of {HF}: huge glossy red-brown eyes covering most of its head and very short tiny antennae, {EDGE}",
    "Adult hover flies pollinate": f"{HF} hovering over a bright yellow flower with its legs dusted in yellow pollen, flowers all around in a sunny garden, {FULL}",
    "Their babies are small green maggots": f"Close-up of a small pale green slug-like maggot with no legs crawling along a green leaf with a determined face, {FULL}",
    "eating aphids one after another": f"The small pale green maggot on a rose stem slurping up tiny green aphids one by one like spaghetti, while a line of aphids waits nervously, {FULL}",
    # 9 escarabajo de suelo
    "This is a ground beetle": f"Night on a stone patio under a porch light: {GB} stopping mid-run and turning to look at the viewer, its red headlamp on, {FULL}",
    "friends a gardener can have": f"{H} kneeling in a vegetable garden at night with a flashlight, and {GB} standing on his open palm, the two smiling at each other like best friends, {FULL}",
    "Ground beetles hunt at night": f"Low ground-level view of dark garden soil at night: {GB} chasing a slug, a snail and a caterpillar that flee in panic, lit by its red headlamp, {FULL}",
    "and the eggs of other pests": f"Close-up of {GB} gobbling a tiny cluster of pale round eggs hidden under a leaf on the soil, with a satisfied face, {FULL}",
    "A lot of the cutworms": f"Cutaway of a vegetable garden at night: a fat grey cutworm caterpillar sneaking toward a row of tiny seedlings holding a tiny plain axe, and {GB} jumping out from behind a pebble to stop it, {FULL}",
    "And one kind, the bombardier": f"Side view of a cartoon bombardier beetle, a small beetle with an orange head and orange legs and a dark blue-black shell, looking mischievous and aiming its rear end like a cannon, {FULL}",
    "fires a boiling hot spray": f"The bombardier beetle firing a hot puff of white steam out of its rear end with a small comic pop burst, a surprised cartoon frog jumping back, {FULL}",
    "If one gets inside, pick it up": f"{H} crouching on a kitchen floor and gently putting a clear plastic cup over {GB}, {FULL}",
    # 8 araña amarilla
    "The big yellow spider in your garden": f"A sunny vegetable garden in late summer with tall tomato plants, and between two of them a big round web with {GS} in the center, {FULL}",
    "A huge black and yellow spider": f"Close-up of {GS} on its web, its bright yellow and black body shining in the sun, {FULL}",
    "head down in a giant web": f"{H} peeking around a tomato plant with a terrified face at {GS} sitting head down in the middle of a giant web, {FULL}",
    "It is a yellow garden spider": f"{GS} sitting calmly in its web and tipping its tiny straw sun hat politely to {H}, who relaxes, {FULL}",
    "It only bites if you grab it": f"A split picture: on the left a cartoon bee and a big red swollen sting bump on an arm, on the right {GS} next to a tiny pink dot on an arm, much smaller, {FULL}",
    "Now look at the middle of the web": f"The camera pushing in toward the center of the round web of {GS}, with a big magnifying glass held up in the foreground, {FULL}",
    "white zigzag going up and down": f"Close-up of a thick bright white zigzag ribbon of silk running up and down through the center of the round web, {GS} scratching its head with one leg beside it, a puzzled swirl above, {FULL}",
    "Maybe to warn birds": f"A cartoon sparrow flying toward the web and swerving away at the last second after seeing the bright white zigzag, {GS} waving it off, {FULL}",
    "And every night, the spider eats": f"Night in the vegetable garden under moonlight: {GS} rolling up its own web like a ball of spaghetti and eating it, {FULL}",
    "and builds a fresh one": f"Early morning dew in the garden: {GS} spinning a brand new shiny round web between the same two tomato plants, little dew drops sparkling, {FULL}",
    "In the fall, she makes a round": f"An autumn garden with orange leaves: {GS} hugging a round brown papery egg sac the size of a grape, like a little paper ball, {FULL}",
    # 7 libélula
    "The dragonfly. A long time ago": f"An old-fashioned village pond long ago, simple cartoon villagers in old clothes pointing in fear at {DR}, which looks a bit like a long sewing needle, {FULL}",
    "Some said it could sew": f"{H} asleep in bed at night, and a spooky thought cloud above shows {DR} holding a giant needle and thread, the dragonfly looking confused at the idea, {FULL}",
    "It cannot. It has no stinger": f"{DR} resting politely on {H}'s finger with a calm smile beside a sunny pond, {FULL}",
    "But for a mosquito, the dragonfly": f"A tiny cartoon mosquito trembling in fear on a reed, looking up at the huge shadow of {DR} looming over it, {FULL}",
    "is a monster. It does not just chase": f"Low angle view of {DR} diving down over a pond like a fearsome jet fighter toward a fleeing mosquito, speed lines, {FULL}",
    "It predicts where the bug": f"Top-down view of a pond: the curved dotted flight path of a mosquito, and {DR} flying a straight dotted line to cut it off where the two paths meet at a small glowing circle, {FULL}",
    "Scientists who study dragonflies": f"{SC} sitting by a pond at a small field table with binoculars and a plain notebook, watching {DR} fly over the reeds, {FULL}",
    "catch up to ninety five percent": f"A big round pie chart almost entirely filled in bright green with just a tiny sliver of grey, and {DR} beside it flexing proudly, {FULL}",
    "A lion is lucky to win": f"A cartoon lion on a savanna panting and exhausted after a failed chase while a zebra runs away in the distance, and {DR} flying past the lion smugly, {FULL}",
    "And before it can even fly": f"Underwater cutaway of a pond: a dragonfly nymph, a chunky brown six-legged creature with no wings and big eyes, crawling on the muddy bottom among water weeds, {FULL}",
    # 6 abejorro
    "The bumblebee. It is big": f"Seen from inside a room: {BB} bonking into a window pane with a comic bump and little stars circling its head, {FULL}",
    "it sounds furious. But bumblebees": f"{BB} gently hugging a fluffy purple flower with a kind sleepy smile in soft warm light, {FULL}",
    "They only sting if you grab them": f"A cutaway of a bumblebee nest in a grassy hole in the ground with a few bumblebees calmly guarding the entrance, and {H} walking past at a safe distance, {FULL}",
    "And the males cannot sting": f"{BB} posing like a superhero with a little red cape fluttering behind it, standing on a yellow tomato flower, {FULL}",
    "Tomato flowers keep their pollen": f"A split picture: on the left a close-up cutaway of a yellow tomato flower with its pollen grains locked inside a closed cone, on the right a plain salt shaker, {NOTXT}, {FULL}",
    "A bumblebee grabs the flower": f"Close-up of {BB} hugging a small yellow tomato flower, its whole body vibrating with wiggly motion lines around it, {FULL}",
    "so fast that the pollen shakes": f"A cloud of bright yellow pollen bursting out of the tomato flower like salt from a shaker, while {BB} holds on with a delighted face, {FULL}",
    "It is called buzz pollination": f"A cartoon honeybee, slim and golden with brown stripes, shaking a tomato flower with all its might and getting nothing, sweating, while {BB} watches smugly, {FULL}",
    "If you grow tomatoes": f"{H} holding a big basket full of red tomatoes, green peppers and blueberries in a sunny garden, with {BB} sitting on top of the pile like a proud chef, {FULL}",
    # 5 sapo
    "You step outside on a rainy night": f"Wide view of a wet sidewalk at night in the rain under a streetlight: {H} in a raincoat stepping out of the front door, and {TO} sitting in the middle of the sidewalk, reflections in the puddles, {FULL}",
    "Bumpy, brown, and staring": f"Extreme close-up of the face of {TO} in the rain, staring straight at the viewer with big golden eyes, raindrops on its bumpy skin, {FULL}",
    "And you probably heard this one": f"Two simple cartoon kids with round white heads and dot eyes whispering on a playground, and a thought cloud above them shows a cartoon hand covered in lumpy bumps next to {TO}, {FULL}",
    "So let's settle it": f"{TO} sitting behind a tiny wooden judge's bench and banging a little gavel with a firm face, {H} listening, {FULL}",
    "Warts on people come from": f"A split picture: on the left small spiky round cartoon virus germs crowding around a human hand, on the right {TO} completely clean and germ-free, shrugging, {FULL}",
    "Those bumps on its skin": f"Cutaway close-up of the bumpy skin of {TO}, a magnifying glass showing tiny round glands inside the bumps like little pockets, {FULL}",
    "And the two big bumps behind": f"Side view close-up of the head of {TO}, the two big oval bumps behind its golden eyes glowing softly, {FULL}",
    "They make a bitter poison": f"A cartoon raccoon spitting out {TO} with a burning red mouth and steam coming out of its ears, the toad landing unharmed, {FULL}",
    "So a toad cannot hurt you": f"{DOG} sniffing curiously at {TO} on the backyard lawn, the toad looking worried, {FULL}",
    "If your dog grabs a toad": f"{DOG} holding {TO} in its mouth on the backyard lawn, its eyes going wide, {FULL}",
    "drooling or pawing at its mouth": f"{H} gently rinsing the mouth of {DOG} with a garden hose while holding a plain phone to his ear, {FULL}",
    "So why keep it?": f"{TO} at night under a porch light, its long sticky tongue shooting out to catch a beetle, {FULL}",
    "Beetles, slugs, cutworms": f"A conveyor belt carrying a beetle, a slug, a cutworm, an ant and a small spider toward the wide open mouth of {TO}, who wears a napkin, {FULL}",
    "A single toad can eat thousands": f"{TO} lying back on a leaf fat and happy with a round full belly in the summer sun, flowers all around, {FULL}",
    # 4 culebra rayada
    "A long, thin snake with stripes": f"Low ground-level view of a garden bed: {SN} sliding out from under a leafy bush across the grass, {FULL}",
    "But this is most likely a garter snake": f"A simple cartoon map of North America in soft green with no labels and no borders, dotted with tiny striped garter snakes, and {SN} waving in front of it, {FULL}",
    "And it is harmless to people": f"{SN} sitting next to {H} on the back porch steps, both smiling calmly, {FULL}",
    "It eats slugs, earthworms": f"{SN} with a napkin around its neck at a picnic blanket where a slug, an earthworm, a cricket, a small frog and a tiny mouse sit looking nervous, {FULL}",
    "If you grab it, it might bite": f"{H}'s hands grabbing {SN}, which twists around with its mouth open about to nip, {H} looking nervous, {FULL}",
    "It will cover your hands": f"{H} holding his hands far away from his body with a disgusted face as green wavy stink lines rise from his fingers, {SN} slithering away grinning, {FULL}",
    "That is its whole plan": f"{SN} escaping into the bushes with a cheeky smirk, a cloud of green stink behind it, and {H} holding his nose, {FULL}",
    "Of course, not every snake": f"{H} standing at a careful distance in a garden with his hands behind his back, looking at an unknown dark snake in the tall grass, {FULL}",
    "Just give it space": f"{SN} and {H} walking away from each other in opposite directions with relieved faces, a big empty stretch of lawn between them, {FULL}",
    # 3 murciélago
    "At dusk, something flutters": f"Wide view of the backyard at dusk under an orange and purple sky, a blurred dark shape fluttering over the fence, and {H} looking up, {FULL}",
    "Swooping, turning, diving": f"{BA} swooping and diving through the dusk sky along a looping path with motion lines, {FULL}",
    "It is not attacking you": f"{BA} catching a moth in mid-air with a happy face, while {H} below ducks for no reason, {FULL}",
    "Moths, beetles, and mosquitoes": f"A very dark night sky with only faint moonlight, and {BA} catching a moth, a beetle and a mosquito in the air, {FULL}",
    "They find them by shouting": f"{BA} with its mouth open sending out curved sound wave rings that bounce off a moth and come back to its big ears, {FULL}",
    "A single little brown bat": f"{BA} with a round full belly flying past a big full moon, a long trail of tiny insects being caught behind it, {FULL}",
    "Scientists have estimated": f"A cornfield at night with {BA} flying above, and a happy cartoon farmer in overalls and a straw hat holding a big stack of plain green paper bills, {FULL}",
    "every year, just by eating crop": f"{BA} swooping over rows of corn and snatching up moths that are chewing the leaves, {FULL}",
    "But here is the one rule": f"{BA} resting on the ground and a bare cartoon hand reaching toward it, stopped by a big red circle-and-slash symbol over the hand, {FULL}",
    "Most bats are healthy": f"A magnified cartoon view of tiny bullet-shaped virus germs floating, with {BA} looking worried in the corner, {FULL}",
    "And you cannot tell by looking": f"{BA} flying in circles inside a living room at night near the ceiling lamp, {H} peeking from behind the door, {FULL}",
    "close the room, open a window": f"{H} opening a window wide at night, and {BA} flying out of the window toward the moon, waving, {FULL}",
    "And if you wake up with a bat": f"{H} sitting up in bed in a dark bedroom, spotting {BA} hanging from the curtain rod, and holding a plain phone, {NOTXT}, {FULL}",
    "Outside, just let them hunt": f"{BA} flying proudly like a superhero over {YARD}, a crowd of mosquitoes fleeing in front of it, {FULL}",
    # 2 lagartija
    "In the western United States": f"A sunny western backyard with a wooden fence and dry golden hills behind it, {LZ} doing push ups on top of a fence post with motion lines, {FULL}",
    "of the fence post, flashing": f"Low angle close-up of {LZ} pushed up high on the fence post, showing off its bright blue belly patches shining in the sun, {FULL}",
    "It is the western fence lizard": f"{LZ} lounging belly up on the fence post with its sunglasses on, its bright blue belly patches visible, totally relaxed, {FULL}",
    "Those push ups are a message": f"{LZ} doing push ups on its fence post while a second, smaller fence lizard on the next post backs away, {FULL}",
    "But it has a secret": f"{SC} in an old-fashioned lab with a chunky old computer, looking into a microscope, with {LZ} in a glass tank beside the desk, {FULL}",
    "Young ticks love to feed": f"Close-up of {LZ} with a few tiny young ticks clinging near its ear, the lizard looking annoyed, {FULL}",
    "And when a tick carrying the germ": f"A magnified cutaway: a tiny tick drinking from the lizard's skin, and inside the tick a few small red wiggly spiral-shaped germs, {FULL}",
    "something in that blood kills": f"A magnified cutaway: glowing blue particles from the lizard's blood surrounding the red spiral germs and dissolving them, and a clean tick walking away with a surprised face, {FULL}",
    "Researchers think this may be": f"A simple cartoon map of the United States with no labels and no borders, the west coast in calm green with a little {LZ} on it, the northeast in hot red crowded with tiny ticks, {FULL}",
    "in California than in the Northeast": f"A split picture: on the left a sunny California hillside with golden grass and {LZ} sunbathing, on the right a dark leafy northeastern forest with many tiny ticks on the grass blades, {FULL}",
    "So if you see a blue belly": f"{H} leaning on the garden fence, smiling and giving a thumbs up to {LZ} doing push ups on its post, {FULL}",
    # 1 zarigüeya
    "To be exact, the Virginia opossum": f"{PO} sitting up very straight and posing politely in a cozy armchair with a tiny monocle, like a dignified gentleman, {FULL}",
    "The only marsupial": f"{PO} and a cartoon kangaroo standing side by side comparing their belly pouches, each with tiny babies peeking out, {FULL}",
    "When they get too big for the pouch": f"{PO} walking along the top of a wooden fence at night with tiny baby opossums riding on her back and holding on to her fur, {FULL}",
    "Sometimes more than ten": f"Close-up of {PO} looking exhausted but proud with a big crowd of tiny baby opossums piled on her back like a bus, {FULL}",
    "It has fifty teeth": f"Extreme close-up of {PO} smiling very wide as if at the dentist, showing a long row of many tiny pointy white teeth, a small dentist mirror held next to it, {FULL}",
    "That is why the hissing": f"{PO} hissing dramatically with its mouth wide open at {DOG}, but with nervous sweat drops on its forehead, {FULL}",
    "And if the bluff does not work": f"{PO} wobbling dizzily with swirly eyes, about to fall over in front of {DOG}, {FULL}",
    "It falls over, its tongue": f"{PO} lying stiff on its back on the grass with its eyes shut tight and its tongue hanging out, green stink lines rising, while {DOG} backs away holding its nose, {FULL}",
    "That is where the phrase": f"A little cartoon theater stage with red curtains where {PO} lies fainted on its back under a spotlight, and an audience of small backyard animals watches, {FULL}",
    "The fear switches it off": f"A cutaway of the head of {PO} showing a simple cartoon light switch inside flipped down to off, its body limp, {FULL}",
    "Snails, slugs, beetles, mice": f"{PO} at night under a fruit tree happily munching fallen rotten apples, with a snail and a slug on the ground nearby, {FULL}",
    "even roadkill": f"{PO} getting a check-up from a friendly cartoon vet in a white coat with a stethoscope, both smiling, a big green check mark on a plain chart, {FULL}",
    "One idea is that its body runs cooler": f"{PO} sitting calmly in a cool blue glow with a little thermometer in its mouth, next to a cartoon raccoon glowing hot red, {FULL}",
    "Which brings us back to that famous": f"{PO} on a giant golden trophy podium surrounded by a cartoon mountain of tiny ticks, cameras flashing, {FULL}",
    "You have probably seen it on a meme": f"{H} scrolling a smartphone that shows a funny cartoon picture of {PO}, with hearts and thumbs-up icons floating out of the phone, {NOTXT}, {FULL}",
    "It came from a real study": f"A clean lab with {SC} using tweezers to place tiny ticks on {PO}, which sits in a small cage looking unimpressed, {FULL}",
    "and most of the ticks disappeared": f"{PO} grooming its fur with its tongue like a cat while a few tiny ticks vanish in little puffs, and {SC} watches holding a plain clipboard, {FULL}",
    "Then they multiplied that out": f"{SC} at a blackboard drawing a row of little tick pictures that gets bigger and bigger toward the right like an avalanche, chalk in hand, {FULL}",
    "And the number exploded online": f"A burst of glowing phones flying through the night air like fireworks, each screen showing a tiny cartoon picture of {PO}, {NOTXT}, {FULL}",
    "looked inside the stomachs": f"An x-ray cutaway of the round belly of {PO}, with {SC} looking in through a big magnifying glass, the stomach holding only bits of fruit, a snail and a beetle, {FULL}",
    "They did not find a single tick": f"{SC} scratching their head over an empty glass dish with a puzzled swirl above, and {PO} shrugging innocently next to it, {FULL}",
    "The honest answer is": f"{PO} sitting on a small stool under a single spotlight on a dark stage, with a big puzzled swirl of stars above its head, {FULL}",
    "probably way too high": f"{PO} pushing a little broom along a night sidewalk under a streetlight, sweeping up snails and fallen fruit like a night cleanup worker, {FULL}",
    "Leave it alone, and it will move on": f"{PO} walking away down the sidewalk at dawn with a little bundle on a stick over its shoulder, looking back with a wave, {FULL}",
    # los 2 que sí
    "Now, I promised you two": f"A sudden mood shift: the backyard under a dark stormy red-tinted sky, and two sinister bug shadows stretched across the wooden fence, {FULL}",
    "The first one. The spotted lanternfly": f"{LF} resting on a tree trunk with its spotted wings folded, looking pretty with a sparkle around it, but its narrow eyes sneaky, {FULL}",
    "Gray wings with black spots": f"{LF} jumping into the air with its wings spread open, flashing its bright red hind wings with black spots, {FULL}",
    "But it does not belong here": f"{LF} sneaking off a cargo ship at a harbor carrying a tiny plain suitcase, plain shipping containers behind it, {NOTXT}, {FULL}",
    "and it was first found in Pennsylvania": f"Green rolling countryside with red barns and farmland, and {LF} arriving with its suitcase and looking around greedily, {FULL}",
    "It sucks the sap": f"A vineyard where a grapevine is covered in spotted lanternflies sucking the sap through tiny straws, the leaves dripping with sticky shiny goo and black sooty mold, {FULL}",
    "That is why officials": f"A cartoon official in a plain suit at a plain podium pointing firmly, in front of a crowd of surprised simple cartoon people, {NOTXT}, {FULL}",
    "Kill it. Squash it": f"A big cartoon sneaker stomping down toward {LF}, which leaps in panic, comic impact lines, {FULL}",
    "In the fall, look for its eggs": f"Close-up of a tree trunk with a flat gray smear like dried mud, and a magnifying glass revealing rows of tiny eggs under it, autumn leaves around, {FULL}",
    "fences, and even cars": f"{H} scraping a gray mud-like egg smear off a car door with a plain plastic card into a clear zip bag holding a little clear liquid, {NOTXT}, {FULL}",
    "And check your car before": f"{H} crouching in a driveway to look under a car bumper with a flashlight, the car with no license plate, {FULL}",
    "because they love to hitch": f"{LF} riding on the roof of a moving car down a highway, holding on with a grin, wind in its face, the car with no license plate, {FULL}",
    "The second one. The tick": f"{TK} on the tip of a tall grass blade with its front legs outstretched, waiting, a deer in the background of a meadow, {FULL}",
    "The young ones are about the size": f"Extreme close-up of a fingertip with a tiny dark young tick next to a single poppy seed, the two exactly the same size, {FULL}",
    "And they can carry the germ": f"A magnified cutaway of {TK} with a few small red wiggly spiral-shaped germs inside its body, the tick grinning sneakily, {FULL}",
    "If you find one stuck on your skin": f"On a plain light background, a lit match and a plain bottle of nail polish, each crossed out with a big red circle-and-slash symbol, and {TK} stuck on a patch of skin beside them, {NOTXT}, {FULL}",
    "and do not twist it": f"Close-up of an arm with {TK} attached, and a pair of fine pointed tweezers gripping the tick right at the skin, {FULL}",
    "and pull straight up": f"The fine tweezers lifting {TK} straight up off the skin in one slow steady motion, a dotted straight upward arrow beside it, {FULL}",
    "Then drop it in rubbing alcohol": f"{TK} sinking in a small clear jar of clear liquid with a sour face, next to a cartoon hand whose pinching fingers are crossed out with a red circle-and-slash symbol, {NOTXT}, {FULL}",
    "Wash the bite": f"{H} washing his arm at a bathroom sink with soap bubbles, a small thermometer resting on the sink, {FULL}",
    "tell your doctor": f"{H} talking with a friendly cartoon doctor in a white coat with a stethoscope in a bright clinic, {FULL}",
    "and maybe the possum, are fighting": f"{LZ} and {PO} standing side by side like bodyguards in front of {H}, facing off against a few small sneaky ticks, {FULL}",
    # cómo tenerlos cerca
    "So how do you keep the helpers": f"{H} putting a plain spray bottle away on a garden shelf with a smile, while {LB}, {BB} and {GB} cheer from the flowers, {NOTXT}, {FULL}",
    "It kills the hunters": f"A garden after spraying, a faint mist in the air, a few beetles and ladybugs lying knocked out on the ground, and a crowd of tiny green aphids marching back first with grins, {FULL}",
    "Leave a pile of leaves": f"A cozy corner of the backyard with a pile of autumn leaves and a few flat stones, {H} placing the last flat rock, {FULL}",
    "Toads, beetles, and millipedes": f"A cutaway of the leaf pile and flat rocks like a cozy apartment: {TO} in one room, {GB} in another and {MI} curled up in a third, all happy, {FULL}",
    "And when one of the small ones": f"{H} in a kitchen holding up a clear cup and a sheet of white paper like a magic trick, a small black beetle on the floor, {FULL}",
    "Slide a cup over it": f"{H} carrying a clear cup with a sheet of paper under it and a small black beetle inside, out through the back door into the garden, {FULL}",
    "Bats and snakes are the exception": f"{BA} and {SN} side by side on the porch steps looking innocent, and {H} keeping his distance with his hands up, {FULL}",
    # cierre circular
    "professional. So, back to that night": f"Night in {YARD}, the metal trash cans at the curb under the porch light, the same quiet scene as at the beginning, {FULL}",
    "The hiss. The teeth": f"Close-up of {PO} behind a metal trash can, mouth open in a hiss showing many tiny teeth, beady eyes shining in the porch light, {FULL}",
    "Now you know what is really standing": f"{PO} sitting by the metal trash cans looking tired, with tiny baby opossums peeking out of her belly pouch, soft warm porch light, {FULL}",
    "full of babies, eating the snails": f"{H} leaning a plain shovel back against the wall with a gentle smile, while {PO} eats a snail on the sidewalk nearby, {FULL}",
    "Go back inside": f"A wide night view of the house: {H} going back in through the lit front door, while {PO}, {TO}, {BA} and {GB} work around the yard under the moon, {FULL}",
    "If you want to meet more": f"Friendly backyard animals waving at the viewer from the top of a wooden fence at night: {PO}, {LZ}, {BA}, {SN} and {TO}, {FULL}",
    "I will see you next time": f"{PO} waving goodbye from the porch steps with tiny babies on her back, the porch light glowing under a calm starry night, {FULL}",
}

# Ronda 2 (19-oct-2026, originales en `medios/_ronda1/`): boca en forma de «3» (016), marco (044, 116), escarabajo de otro
# color (048), «zzz» (064), «BONK!» (074), científico con pelo (128), «OFF» en el interruptor (145), «CHAMPION» (149),
# carteles con garabatos (183)
I.update({
    "it leaves a yellow drop": f"Extreme close-up of a fingertip with {LB} on it and a tiny shiny yellow drop on the skin, and {H} in the background with a grossed-out face, a wrinkled nose and a simple wavy line for a mouth, {FULL}",
    "Ground beetles hunt at night": f"Low ground-level view of dark garden soil at night: {GB} chasing a slug, a snail and a caterpillar that flee in panic, lit by its red headlamp, {EDGE}, no white margin",
    "fires a boiling hot spray": f"The same cartoon bombardier beetle, a small beetle with an orange head, orange legs and a dark blue-black shell, firing a hot puff of white steam out of its rear end with a small comic pop burst, a surprised cartoon frog jumping back, {FULL}",
    "Some said it could sew": f"{H} asleep in bed at night with eyes closed, and a spooky thought cloud above shows {DR} holding a giant needle and thread, the dragonfly looking confused at the idea, no snoring letters, {FULL}",
    "The bumblebee. It is big": f"Seen from inside a room: {BB} bumping into a window pane with a plain yellow impact star burst and little stars circling its head, no sound effect words, {FULL}",
    "every year, just by eating crop": f"{BA} swooping over rows of corn at night and snatching up moths that are chewing the leaves, {EDGE}, no white margin",
    "But it has a secret": f"{SC}, a bald round white head with no hair at all, in an old-fashioned lab with a chunky old computer, looking into a microscope, with {LZ} in a glass tank beside the desk, {NOTXT}, {FULL}",
    "The fear switches it off": f"A cutaway of the head of {PO} showing a simple cartoon light switch inside flipped down, the switch plate completely blank, its body limp and its eyes shut, {FULL}",
    "Which brings us back to that famous": f"{PO} standing proudly on top of a plain shiny golden trophy cup on a plain podium, surrounded by a cartoon mountain of tiny ticks, cameras flashing, no banners and no signs, the trophy and podium completely blank, {FULL}",
    "It kills the hunters": f"A garden after spraying, a faint mist in the air, a few beetles and ladybugs lying knocked out on the ground, and a crowd of tiny green aphids marching back first with grins, no signs, no flags and no banners, {FULL}",
})

# Clips de clímax (FX `video` a cuadro entero en efectos.py; tramo 3). Uno continuo, sin dos escenas.
SIN_VOZ = " No dialogue, no conversation, no voices."
CLIMAX = {
    "clip_desmayo": (10, "Scene: at night on the backyard lawn under the porch light, "
                         f"{PO} hisses at {DOG} with its mouth wide open, then wobbles with dizzy swirly eyes, slowly tips "
                         "over and falls stiff on its back with its tongue hanging out, and the dog sniffs it, backs away "
                         f"and holds its nose, {FULL}."),
    "clip_linterna": (10, f"Scene: in a sunny vineyard, {LF} rests on a tree trunk with its spotted gray wings folded, then "
                          "suddenly jumps into the air and spreads its wings, flashing its bright red hind wings with "
                          "black spots in slow motion, and lands on a grapevine with a sneaky grin, the camera following "
                          f"it, {FULL}."),
    "clip_cierre": (6, f"Scene: a wide night view of the house and backyard, {H} walks back in through the lit front door "
                       f"and the porch light glows, while {PO} with tiny baby opossums on her back waddles past the metal "
                       f"trash cans across the lawn under the moon, the camera slowly pulling back, {FULL}."),
}


def busca(dic, texto, usadas):
    ks = [k for k in dic if texto.startswith(k)]
    assert len(ks) <= 1, (texto, ks)
    if ks:
        assert ks[0] not in usadas, ("clave repetida", ks[0])
        usadas.add(ks[0])
        return ks[0]


bs = json.load(open("beats.json", encoding="utf-8"))
out, usadas = {}, set()
for b in bs:
    t = b["texto"]
    kv, kn, ki = (busca(d, t, usadas) for d in (VID, N, I))
    assert sum(x is not None for x in (kv, kn, ki)) == 1, (b["id"], t)
    if kv:
        assert b["tipo"] == "video", b["id"]
        a, tr, c = VID[kv]
        out[b["id"]] = f"{E}Scene one, first five seconds: {a}. Then {tr}. Scene two, last five seconds: {c}, {FULL}.{C}"
    else:
        assert b["tipo"] == "imagen", b["id"]
        out[b["id"]] = E + (card(*N[kn]) + CN if kn else I[ki] + "." + C)
sobran = (set(VID) | set(N) | set(I)) - usadas
assert not sobran, sobran
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({k: dict(s=s, prompt=E + p + C + SIN_VOZ) for k, (s, p) in CLIMAX.items()},
          open("clips_climax.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"prompts.json: {len(out)} prompts ({len(N)} tarjetas, {len(VID)} clips) · clips_climax.json: {len(CLIMAX)} clips")
