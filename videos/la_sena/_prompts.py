"""Prompts de Flow (Nano Banana 2.1 · 16:9 · x2) para «La seña» y las diapositivas del taller «Antes de decir que sí».

Escribe prompts.json (clave → prompt). Todos empiezan con FICHA (lo valida `flow_integrado.py paquete`).
Receta: docs/estilo_pegatina_flow.md §1. Escenarios vacíos (el código pone a la gente), hojas en fondo blanco puro,
ciclos mirando a la DERECHA. Evitar objetos blancos en hojas (se pierden al recortar).
"""
import json
import os

FICHA = ("Hand-painted 2D cut-out animation art, contemporary Mexican picture book style: clean dark-brown ink outlines, "
         "flat gouache colors with soft painted shading and visible paper grain, warm dusty palette (adobe ochre, faded "
         "terracotta, cement gray, nopal green, turquoise sky, guava pink accents). Present day, a small working-class town "
         "in the Juchipila canyon of southern Zacatecas, Mexico; authentic rural Mexican details, nothing American.")

PUEBLO = ("unplastered gray cinder-block houses with rebar sticking out of the flat concrete roofs, black plastic water tanks "
          "on the roofs, patches of corrugated metal sheet, tangled power lines on concrete poles")
CERROS = "dry reddish canyon hills with huizache trees, nopal cactus and agave"
TORRES = "the two uneven bell towers and dome of the town sanctuary"
FIN = "No people, no animals. No text, no letters, no numbers, no watermark."

# Fichas físicas (iguales en todas las hojas y ciclos)
ANGEL8 = ("ÁNGEL as an 8-year-old Mexican boy: small and skinny, light-brown skin, short black hair with a cowlick, big ears, "
          "gap-toothed smile, faded red t-shirt, cheap blue shorts, worn plastic sandals")
TONO13 = ("TOÑO as a 13-year-old Mexican boy: lanky, brown skin, short black hair shaved on the sides, thick eyebrows, "
          "faded green tank top, old rolled-up jeans, sneakers with holes")
ANGEL14 = ("ÁNGEL, a 14-year-old Mexican boy in third year of a public secondary school: skinny, light-brown skin, short black "
           "hair with a cowlick, big ears, school uniform: maroon V-neck sweater with a small embroidered crest, white shirt "
           "collar, gray trousers, worn-out black sneakers, old black backpack")
ANGEL_GRAD = ("ÁNGEL, the same 14-year-old Mexican boy on his graduation day: skinny, light-brown skin, black hair combed back "
              "with gel, big ears, ironed light-blue long-sleeve shirt, maroon tie, gray trousers, polished black shoes")
TONO19 = ("TOÑO, a 19-year-old Mexican construction worker: tall and lean, brown skin, short black hair shaved on the sides, "
          "thick eyebrows, thin mustache, broad warm smile, faded gray t-shirt and jeans stained with cement dust, old brown "
          "work boots, a worn faded red cap")
TONO19B = ("TOÑO, the same 19-year-old Mexican young man months later: tall and lean, brown skin, hair shaved on the sides, "
           "thin mustache, thinner face with tired eyes and dark circles, black hoodie, a thin silver chain, a new black "
           "flat-brim cap, brand-new bright sneakers drawn with light gray shading and dark outlines")
ROSA = ("ROSA, their mother, a 42-year-old Mexican woman: short and sturdy, brown skin, black hair with gray streaks in a low "
        "bun, tired kind eyes, flowered apron over a simple purple blouse, dark skirt, plastic sandals")
PAPA = ("the father, a 40-year-old Mexican man: mustache, brown cowboy hat, plaid shirt, jeans, boots, a backpack")


def fondo(desc, fin=FIN):
    return f"{FICHA} {desc} {fin}"


def hoja(ficha, poses, quien="character"):
    n = len(poses)
    return (f"{FICHA} Character model sheet on a plain flat pure white background: {ficha}. The SAME {quien} drawn {n} "
            f"times, full body, evenly spaced in one row with generous empty white space between them, never touching or "
            f"overlapping: " + "; ".join(poses) + ". No ground, no cast shadows. No text, no letters, no watermark.")


def ciclo(ficha, tipo, n, paso):
    return (f"{FICHA} Animation sprite sheet on a plain flat pure white background: {tipo} cycle of {ficha}. The SAME "
            f"character drawn {n} times in a single horizontal row, strict side view facing right, full body, same size and "
            f"same height, evenly spaced with wide gaps and never touching, each drawing a consecutive phase of one {paso}. "
            f"No ground line, no cast shadows. No text, no letters, no watermark.")


def rejilla(n, objetos):
    return (f"{FICHA} Prop sheet on a plain flat pure white background: {n} separate objects arranged in an even grid with "
            f"generous white space, never touching or overlapping, each drawn whole: " + "; ".join(objetos) +
            ". No cast shadows. No text, no letters, no watermark.")


P = {}

# ── Escenarios (vacíos) ──────────────────────────────────────────────────────────────────────────────────
P["01_cuesta_tarde"] = fondo(
    "Wide background of a steep street climbing a hill in a poor neighborhood of the town at golden sunset: rough cement "
    f"street with old cobblestone patches, a pile of construction sand at the bottom of the slope, {PUEBLO}, a metal door "
    "painted turquoise, a tiny corner shop with a rolled-up metal shutter and a faded painted wall. Strong depth: foreground "
    "the cracked cement curb and a nopal growing in a paint bucket, midground the street going up the slope, background "
    f"{CERROS} and {TORRES} glowing in the sunset. Open empty street across the lower third.")
P["02_cuesta_tarde_b"] = fondo(
    "Wide background of the SAME steep neighborhood street seen from the bottom looking up the slope, on a different sunset "
    f"with pink clouds: rough cement street with cobblestone patches, {PUEBLO}, a turquoise metal door, a bougainvillea "
    "climbing a wall. Strong depth: foreground a pile of construction sand and a curb, midground the slope going up, "
    "background the top of the hill against a pink and orange sky. Open empty street across the lower third.")
P["03_puerta_noche"] = fondo(
    "Wide background of the front of a humble family house at night: unplastered gray cinder-block wall, a rusty metal door "
    "half open with warm yellow light coming out, a single bare light bulb above the door, a geranium planted in a paint "
    "bucket, a plastic chair on the sidewalk. Strong depth: foreground cracked sidewalk, midground the open door, background "
    "a dark street going down the hill, a few lit windows of neighboring houses and the dark silhouette of the hills under a "
    "deep blue starry sky. Open empty sidewalk across the lower third.")
P["04_cocina_noche_lluvia"] = fondo(
    "Interior background of a humble Mexican kitchen at night during heavy rain: old corrugated metal roof with a leak "
    "dripping into a blue plastic bucket on the cement floor, a gas stove with a clay pot of beans, a wooden table covered "
    "with a flowered plastic tablecloth, a tortilla basket, scattered paper bills on the table, a store calendar on the "
    "wall, a small framed Virgin of Guadalupe, a small window with burglar bars and rain running down the glass, one warm "
    "ceiling bulb. Strong depth: foreground the table edge, midground the stove and the bucket, background the window and "
    "shelves with plastic dishes. Open empty floor across the lower third.")
P["05_cocina_dia"] = fondo(
    "Interior background of the SAME humble Mexican kitchen on a sunny morning months later: the roof is now NEW shiny "
    "corrugated metal sheets, the blue plastic bucket lies upside down in a corner, a gas stove with a clay pot, a wooden "
    "table with a flowered plastic tablecloth, a small framed Virgin of Guadalupe, a framed photo on the wall, a window "
    "with burglar bars and warm sunlight coming in, the rusty metal front door visible on one side. Strong depth: "
    "foreground the table edge, midground the stove, background the door and the window. Open empty floor across the "
    "lower third.")
P["06_azotea_atardecer"] = fondo(
    "Wide background on the flat concrete rooftop of an unfinished cinder-block house at golden sunset: rebar rods sticking "
    "up from unfinished columns, a black water tank, a clothesline with colorful clothes, a few stacked cinder blocks, a "
    "plastic bucket, the rooftop edge in the foreground where two people could sit. Strong depth: midground other rooftops "
    f"of the neighborhood with water tanks and antennas, background the town below, {TORRES} and {CERROS} under an orange "
    "and pink sky. Open empty rooftop across the lower third.")
P["07_azotea_noche"] = fondo(
    "Wide background on the SAME flat concrete rooftop of an unfinished cinder-block house at night: rebar rods, a black "
    "water tank, a clothesline, stacked cinder blocks, a narrow cement staircase coming up from below. Strong depth: "
    f"midground dark rooftops with water tanks, background the town lights below, {TORRES} softly lit, the black hills and "
    "a deep blue sky full of stars. Open empty rooftop across the lower third.")
P["08_parada_amanecer"] = fondo(
    "Wide background of a small roadside bus stop with a little concrete shelter beside a two-lane highway at dawn in the "
    "Juchipila canyon: low mist in the valley, guava orchards and agave fields beside the road, a blank metal road sign, "
    f"power poles, {CERROS} turning pink with the first light. Strong depth: foreground gravel shoulder and dry grass, "
    "midground the shelter and the road, background the misty canyon. Open empty roadside across the lower third.")
P["09_secundaria_patio"] = fondo(
    "Wide background of the courtyard of a Mexican public secondary school in a small town on a sunny morning: single-story "
    "classroom buildings of cinder block painted in two institutional colors (cream on top, maroon below), an open covered "
    "corridor with a flat concrete roof on steel columns, windows with green steel bars, a concrete court covered by a "
    "curved corrugated metal arch roof on steel trusses, two basketball hoops, a flagpole, a small school snack stand with "
    "a metal shutter, trees planted inside painted tires, a perimeter wall with a steel gate. Strong depth: foreground the "
    f"court lines, midground the classrooms, background {CERROS}. Open empty court across the lower third.")
P["10_salon"] = fondo(
    "Interior background of a classroom in a Mexican public secondary school: rows of old metal-frame student desks with "
    "wooden writing arms, a whiteboard, a teacher's desk with stacked notebooks, windows with steel bars and dusty sunlight, "
    "a ceiling fan, a small Mexican flag pinned on the wall, crumpled paper on the floor. Strong depth: foreground two desks, "
    "midground the rows, background the whiteboard and windows. Open empty floor across the lower third.")
P["11_cancha_graduacion"] = fondo(
    "Wide background of the school's concrete court under a curved corrugated metal arch roof, decorated for a secondary "
    "school graduation in the late afternoon: strings of colorful papel picado tissue-paper flags hanging across, a long "
    "table with a maroon tablecloth and flower arrangements at the far end, balloons, a sound speaker on a stand, rows of "
    "chairs ONLY at the far back. Strong depth: foreground open concrete floor, midground the papel picado and the court, "
    f"background the open sides with {CERROS} in warm light. Open empty concrete floor across the lower half.")
P["12_reja_calle"] = fondo(
    "Background seen from inside the school court looking out through the perimeter steel fence and its open gate at "
    "golden late afternoon: through the bars a dusty street outside, an old parked pickup truck, a concrete power pole, a "
    "small tree, a wall with a faded painted mural. Strong depth: foreground blurred strings of papel picado, midground the "
    "fence and gate, background the street going down the hill toward the highway and the hills. Open empty sidewalk "
    "outside the fence.", "No people. No text, no letters, no numbers, no watermark.")
P["13_recamara_amanecer"] = fondo(
    "Interior background of a small shared bedroom of two brothers at dawn: two narrow beds, one perfectly made and empty, "
    "the other messy, cinder-block walls painted light blue and peeling, a poster of a soccer player silhouette, clothes on "
    "a chair, a fabric sheet used as a curtain, cold blue morning light through a small barred window. Strong depth: "
    "foreground the messy bed corner, midground the empty made bed, background the window. Open empty floor across the "
    "lower third.")
P["14_jalpa_panorama"] = fondo(
    "Wide panoramic background of the town seen from a hill at dusk: flat-roofed cinder-block houses spread across the "
    f"valley of the Juchipila canyon, {TORRES} rising above the main plaza with its trees, the highway crossing the valley, "
    "guava orchards and fields, the canyon mountains in layered ridges, the first house lights turning on, a violet and "
    "orange sky. Strong depth: foreground dry grass, a huizache tree and a big rock, midground the town, background the "
    "mountains. Open empty hilltop across the lower third.")
P["15_plaza_jalpa"] = fondo(
    "Wide background of the main plaza of the town on a sunny afternoon: a green wrought-iron kiosk, iron benches, trimmed "
    f"laurel trees, the stone facade of the sanctuary with its two uneven bell towers and dome, colonial arcades, small food "
    "stalls with colorful awnings, papel picado above a street. Strong depth: foreground the plaza paving and a bench, "
    "midground the kiosk and trees, background the sanctuary. Open empty plaza across the lower third.")
P["16_huerta_guayaba"] = fondo(
    "Wide background of a guava orchard in the canyon on a bright morning: rows of guava trees with yellow fruit, stacked "
    "wooden harvest crates, an aluminum ladder, a dirt path, a small irrigation canal, "
    f"{CERROS} in the background. Strong depth: foreground guava branches and fallen fruit, midground the rows of trees, "
    "background the hills. Open empty dirt path across the lower third.")

# ── Hojas de personajes ──────────────────────────────────────────────────────────────────────────────────
P["21_angel8_hoja"] = hoja(ANGEL8, [
    "sitting on the ground in a pile of sand laughing with both arms up",
    "standing doing a secret sign: two fingers pointing at his own eyes",
    "standing pointing two fingers forward at someone with a big grin",
    "standing at a doorway crying silently holding the hem of his shirt",
    "waving goodbye with one hand, sleepy face"], "boy")
P["22_tono13_hoja"] = hoja(TONO13, [
    "running forward bent over with both arms extended as if pushing a bicycle seat",
    "standing waving one arm high and laughing",
    "standing doing a secret sign: two fingers pointing at his own eyes",
    "pointing two fingers forward at someone with a grin",
    "standing serious with one arm stretched sideways and down as if resting his hand on a smaller boy's shoulder"], "boy")
P["23_angel14_hoja"] = hoja(ANGEL14, [
    "sitting cross-legged eating a taco and laughing",
    "sitting looking down at a smartphone with a tempted half smile, face lit by the screen",
    "standing angry shouting with fists down",
    "standing crying silently, wiping his eyes with his sleeve",
    "standing doing a secret sign: two fingers pointing at his own eyes",
    "standing pointing two fingers forward at someone"], "boy")
P["24_angel_grad_hoja"] = hoja(ANGEL_GRAD, [
    "standing nervous holding a rolled certificate tied with a maroon ribbon",
    "looking back over his shoulder searching for someone",
    "doing the secret sign with two fingers to his own eyes while holding the certificate",
    "pointing two fingers forward with tears and a smile",
    "standing still with tears running down and a small smile"], "boy")
P["25_tono19_hoja"] = hoja(TONO19, [
    "sitting cross-legged on the floor eating a taco and laughing",
    "sitting reaching sideways with a sly grin as if stealing food",
    "kneeling repairing the chain of a small bicycle",
    "sitting on a chair soaked by rain looking at a smartphone with a serious tired face lit by the screen",
    "standing laughing with a hand on his chest"], "young man")
P["26_tono19b_hoja"] = hoja(TONO19B, [
    "sitting on a chair eating while looking sideways toward a door with wary eyes",
    "standing leaning forward gripping with both hands as if holding someone's shoulders, intense face",
    "standing with tears in his eyes, mouth open speaking, face breaking",
    "standing doing a secret sign: two fingers pointing at his own eyes, sad smile",
    "walking away seen from behind with hands in his hoodie pocket"], "young man")
P["27_rosa_hoja"] = hoja(ROSA, [
    "cooking at a stove seen from the side facing right",
    "asleep sitting with her head on her folded arms",
    "blessing someone: making the sign of the cross with her thumb, arm raised to a taller person's forehead",
    "sitting on a plastic chair holding a brown handbag on her lap, crying and smiling",
    "standing clapping with tears and a proud smile"], "woman")
P["28_papa_hoja"] = hoja(PAPA, [
    "hugging pose with both arms open",
    "walking away seen from behind carrying the backpack",
    "standing with his hat in his hand looking down",
    "standing whispering with one arm stretched down to the side as if on a boy's shoulder"], "man")
P["29_vals_hoja"] = (
    f"{FICHA} Character model sheet on a plain flat pure white background: {ROSA}, dancing a slow waltz with her son, "
    f"{ANGEL_GRAD}. The SAME couple drawn 4 times in one row, full body, evenly spaced with generous white space, never "
    "touching each other's copies, showing four phases of a slow waltz turn, her eyes wet with tears and both smiling. "
    "No ground, no cast shadows. No text, no letters, no watermark.")
P["30_gente_hoja"] = (
    f"{FICHA} Model sheet on a plain flat pure white background of 7 DIFFERENT people from the town, full body, evenly "
    "spaced in one row, never touching or overlapping: an 8-year-old neighborhood boy riding an old small red bicycle seen "
    "from the side facing right; a school principal woman in a blazer holding a microphone; a male school prefect with a "
    "whistle; an old woman sitting on a plastic chair; a young man riding a motorcycle slowly seen from the side facing "
    "right, wearing a cap; a teenage boy classmate in a maroon school sweater laughing; a teenage girl classmate in a "
    "maroon school sweater with a ponytail. No ground, no cast shadows. No text, no letters, no watermark.")
P["31_graduacion_gente_hoja"] = (
    f"{FICHA} Model sheet on a plain flat pure white background of 7 DIFFERENT people at a secondary school graduation, "
    "full body, evenly spaced in one row, never touching: a teenage girl graduate in a light-blue blouse sitting on a gray "
    "plastic chair; a teenage boy graduate in a light-blue shirt and maroon tie sitting on a gray plastic chair; a mother "
    "standing holding up a smartphone to record; a father in a cowboy hat clapping; a grandmother with a rebozo smiling; a "
    "little girl in a party dress holding a balloon; a teacher in a suit holding a stack of rolled certificates. No ground, "
    "no cast shadows. No text, no letters, no watermark.")

# ── Ciclos (mirando a la derecha) ────────────────────────────────────────────────────────────────────────
P["41_angel14_camina"] = ciclo(ANGEL14, "walk", 8, "walking step")
P["42_tono19b_camina"] = ciclo(TONO19B, "walk", 8, "walking step")
P["43_angel8_bici"] = ciclo(ANGEL8 + ", riding a small red bicycle", "bicycle riding", 6, "pedal turn")
P["44_papa_camina"] = ciclo(PAPA, "walk", 8, "walking step")
P["45_perro_camina"] = ciclo("a skinny caramel-colored Mexican street dog with floppy ears", "walk", 6, "trotting step")
P["46_zanate_vuelo"] = (
    f"{FICHA} Animation sprite sheet on a plain flat pure white background: a row of 6 drawings of the same black "
    "great-tailed grackle bird in flight, side view facing right, evenly spaced and never touching, showing one wing-flap "
    "cycle. No text, no letters, no watermark.")

# ── Utilería y naturaleza ────────────────────────────────────────────────────────────────────────────────
P["51_utileria_casa"] = rejilla(16, [
    "a blue plastic bucket", "a worn faded red cap dusty with cement", "a pair of brand-new sneakers with light gray "
    "shading", "a cheap smartphone with a plain black screen", "a framed photo of a smiling man in a cowboy hat next to a "
    "pickup truck", "a rolled certificate tied with a maroon ribbon", "a plate of refried beans", "a stack of corn "
    "tortillas wrapped in an embroidered red cloth", "an old small red bicycle seen from the side", "a black backpack",
    "a brown woman's handbag", "a shiny new corrugated metal roof sheet", "a pile of construction sand", "a small framed "
    "Virgin of Guadalupe", "a gray plastic chair", "a black hoodie folded"])
P["52_utileria_fiesta"] = rejilla(12, [
    "a long string of colorful papel picado tissue-paper flags", "a second string of papel picado in pink and green",
    "a bunch of colorful balloons (no white)", "a microphone on a stand", "a black sound speaker", "a bouquet of red "
    "roses wrapped in cellophane", "a graduation cake with maroon frosting", "a stack of gray plastic chairs", "a small "
    "Mexican flag on a pole", "a folding table with a maroon tablecloth", "a tissue box", "a folded small paper note"])
P["53_naturaleza"] = rejilla(10, [
    "a huizache tree", "a big nopal cactus", "an agave plant", "a guava tree with yellow fruit", "two brown rocks",
    "a bougainvillea bush in a paint bucket", "a tuft of dry grass", "a small pink sunset cloud", "a pile of guavas",
    "a concrete power pole with tangled wires"])

if __name__ == "__main__":
    for k, v in P.items():
        assert v.startswith(FICHA), k
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(P, f, ensure_ascii=False, indent=1)
    print(f"{len(P)} prompts → {ruta}")
