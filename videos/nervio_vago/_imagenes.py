# -*- coding: utf-8 -*-
"""Lista ORDENADA de imágenes: una por beat desde scene-008 hasta scene-120 (113). El número del comentario es el beat."""
from guion import FICHA

CH = FICHA["personajes"]["la chica"]
LO = FICHA["personajes"]["Loewi"]
ANAT = "anatomical illustration drawn in thin white engraving lines, no labels"
SIL = f"a transparent white outline of {CH}, standing, seen from the front"
NEON = "glowing yellow neon"
LAB = "a 1921 university laboratory in Graz with glass flasks, brass apparatus and a smoked-drum recorder"

I = [
    f"a lone traveler in an ancient Roman cloak with a walking staff wandering along an old Roman road lined with cypress trees and stone milestones, his lantern {NEON}",  # 008
    f"a long winding river seen from above, wandering through hills, fields and small villages, the river {NEON}",  # 009
    f"{SIL}; two thin parallel lines run down the left and right sides of her neck to her belly, both lines {NEON}",  # 010
    f"a large old-fashioned control panel with two big levers and many small dials without numbers, one lever {NEON}",  # 011
    f"{CH} lying on a sofa after dinner with a sleeping cat on her lap, an empty plate on the table, her belly glowing soft yellow neon",  # 012
    f"two car pedals seen from the driver's seat, accelerator and brake, drawn in fine engraving, the brake pedal {NEON}",  # 013
    f"a long railway track drawn in perspective climbing a hill toward a distant city, a small train on it {NEON}",  # 014
    f"the cut end of a thick cable seen up close, made of ten thin wires; eight wire ends {NEON} and two plain white",  # 015
    f"tiny messengers climbing up a long rope ladder from a heart and a stomach toward a brain at the top, carrying envelopes {NEON}",  # 016
    f"a white line-art brain wearing big headphones, a cable {NEON} running down from it to a heart, two lungs and a stomach below",  # 017
    f"{CH} sitting on a park bench with her eyes closed and one hand on her belly, a soft wave {NEON} rising from her belly to her head",  # 018
    f"an ornate antique key lying on a dark cloth, the key {NEON}",  # 019
    f"a wooden desk in an old laboratory with a brass microscope, a frog in a glass jar and a notebook with blank pages, the microscope lamp {NEON}",  # 020
    f"a crescent moon over the rooftops and chimneys of an old European city at night, the moon {NEON}",  # 021
    f"an old Austrian city at night in 1921 with church towers, a clock tower and cobblestone streets, the window of one church tower {NEON}",  # 022
    f"{LO} sitting up suddenly in his bed at night in old-fashioned pajamas, eyes wide open, a light bulb above his head {NEON}",  # 023
    f"close-up of an old man's hand quickly scribbling on a tiny scrap of paper on a bedside table beside a candle, the candle flame {NEON}",  # 024
    f"{LO} in morning sunlight at his breakfast table holding a tiny scrap of paper covered in messy unreadable squiggles, frowning and puzzled, the squiggles {NEON}",  # 025
    f"{LO} pacing back and forth in his dark study at night beside a tall grandfather clock, the clock pendulum {NEON}",  # 026
    f"{LO} asleep in bed with a dream cloud above him showing two small frog hearts, the dream cloud {NEON}",  # 027
    f"{LO} walking fast in a long coat and hat through an empty cobblestone street at night toward a university building, a single street lamp {NEON}",  # 028
    f"{LAB}: two small frog hearts beating inside two glass vessels of clear liquid on the bench, both hearts {NEON}",  # 029
    f"close-up of one glass vessel with a tiny frog heart and a thin nerve thread still attached to it, the nerve thread {NEON}",  # 030
    f"an old 1920s electrical stimulator with brass coils sending a small spark into the nerve of the frog heart, the spark {NEON}, a slow wavy line on a smoked-drum recorder",  # 031
    f"{LO}'s hand lifting a glass pipette full of liquid out of the first vessel in {LAB}, the liquid {NEON}",  # 032
    f"a glass pipette dripping liquid into a second glass vessel holding another tiny frog heart with no nerve attached, the falling drops {NEON}",  # 033
    f"the second tiny frog heart beating slowly in its glass vessel, a slow wavy line traced on a smoked-drum recorder beside it, the heart {NEON}",  # 034
    f"tiny molecules drawn as little balls and sticks floating like messengers carrying small envelopes, the molecules {NEON}",  # 035
    f"{LO} smiling in {LAB}, holding up a small glass flask to the light, the flask {NEON}",  # 036
    f"a single molecule model of balls and sticks floating above the point where a nerve ending touches a heart muscle fiber, the molecule {NEON}, engraving",  # 037
    f"two nerve cells almost touching with a tiny gap between their branches, little droplets crossing the gap {NEON}, engraving",  # 038
    f"{LO} in a formal tailcoat on a grand stage under a crystal chandelier receiving a medal, an audience in evening dress, the medal {NEON}",  # 039
    f"{CH} sitting calmly on a couch at home reading a book, a small heart outline in her chest {NEON}",  # 040
    f"a human heart as an {ANAT}, a tiny spark generator in its upper right corner {NEON}",  # 041
    f"an old wooden metronome ticking very fast with motion lines, the pendulum {NEON}",  # 042
    f"a sneaker resting gently on a brake pedal, the pedal connected by a long cable to a heart, the cable {NEON}",  # 043
    f"{CH} breathing in slowly by an open window, her chest rising, a swirl of air entering her nose {NEON}",  # 044
    f"a heart beside a pulse line whose beats get closer together, the pulse line {NEON}, a small arrow of air flowing in",  # 045
    f"{CH} with eyes closed exhaling a long ribbon of breath that floats across the room, the ribbon {NEON}",  # 046
    f"an old metronome standing still beside a heart, the heart {NEON} and the metronome plain white",  # 047
    f"a long horizontal line of heartbeat peaks with gaps of slightly different widths between them, the line {NEON}",  # 048
    f"a gently undulating wave like an ocean swell drawn above a row of heartbeat peaks, the wave {NEON}",  # 049
    f"a racing bicycle's handlebar with a hand squeezing the brake lever, the brake cable {NEON}",  # 050
    f"an agile cat landing on top of a garden fence and stopping perfectly balanced, its paws {NEON}",  # 051
    f"a meerkat standing stiffly on guard on a mound in the desert, its eyes {NEON}",  # 052
    f"{CH} sitting up in bed in the morning looking at a smartwatch on her wrist, the watch screen {NEON}, no numbers",  # 053
    f"{CH} slumped on the sofa late at night with a laptop, a phone and piles of papers, a dim lamp, her phone screen {NEON}",  # 054
    f"a car's brake pedal with its cable snapped in two, the broken cable end sparking {NEON}",  # 055
    f"an old alarm bell on the wall of an empty apartment at night still ringing with motion lines, the bell {NEON}",  # 056
    f"{CH} lying awake in bed at night staring at the ceiling, a half-eaten dinner on the nightstand, her belly glowing faint yellow neon",  # 057
    f"a bicycle skidding to a sudden stop on a street, the rear wheel locked with skid marks, the brake {NEON}",  # 058
    f"{CH} sitting in a clinic chair while a nurse prepares a syringe for a blood test, {CH} turning pale with dizzy swirl eyes, the syringe {NEON}",  # 059
    f"a heart with a long nerve cable pulled hard like a car's hand brake lever, the cable {NEON}",  # 060
    f"an old pressure gauge with its needle dropping toward the bottom, the needle {NEON}, no numbers",  # 061
    f"{CH} fainting, sliding down gently against a clinic wall, little stars circling her head {NEON}",  # 062
    f"a crowded hospital waiting room drawn in white lines, one person in the crowd swaying dizzy with little stars around their head {NEON}",  # 063
    f"{CH} lying on the floor of a clinic with her legs raised on a chair while a kind nurse kneels beside her, the chair {NEON}",  # 064
    f"a friendly doctor with a stethoscope listening to the heart of {CH} in a consulting room, the stethoscope {NEON}",  # 065
    f"an old locked treasure chest slowly opening with light spilling out, the light {NEON}",  # 066
    f"a modern research laboratory with tall windows, scientists in lab coats at long benches with computers and microscopes, one monitor {NEON}, no text",  # 067
    f"a white laboratory rat in a clean cage, small flame shapes rising from its body {NEON}, representing inflammation",  # 068
    f"the same white laboratory rat calm and healthy in its cage, a soft calming wave {NEON} passing over it",  # 069
    f"tiny white immune cells drawn as little soldiers lowering their spears as a long nerve {NEON} passes above them",  # 070
    f"a big old radio volume knob being turned down by a hand, the knob {NEON}, small flames in the background shrinking",  # 071
    f"two swollen hands with knotted knuckles resting on a kitchen table, and on the patient's chest below the collarbone a tiny implanted device {NEON}",  # 072
    f"an older woman happily opening a jar with her hands in a sunny kitchen, her knuckles glowing soft yellow neon",  # 073
    f"a small implantable medical device with a thin wire lying on a sterile metal tray, the device {NEON}",  # 074
    f"a white line-art brain with calm wave lines around it, a thin wire running down from it to a small device, the wire {NEON}",  # 075
    f"a small round medical implant resting in the open palm of a gloved hand under a bright round lamp, the implant {NEON}",  # 076 (la del cirujano falló en Flow, 21-oct)
    f"a stage magician's top hat and wand on a small table, crossed out by a big X shape {NEON}",  # 077
    f"{CH} lying on her bed scrolling her phone, dozens of tiny video thumbnails floating out of the screen, the phone {NEON}",  # 078
    f"two small scenes floating out of a phone: a person rubbing their own earlobe and a person tapping their chest with fingertips, the phone outline {NEON}",  # 079
    f"a giant round power button on the chest of a white outline figure, the power button {NEON}",  # 080
    f"the same giant round power button cracked and crumbling into pieces, the pieces {NEON}",  # 081
    f"{CH} in a gym doing a single squat holding a tiny dumbbell and looking at her arm with disappointment, the dumbbell {NEON}",  # 082
    f"side view of a head with a small clip-on electrical device attached to the outer ear, a balance scale in the background, the device {NEON}",  # 083
    f"a plain wooden box holding simple things: a folded towel, a pair of sneakers, a songbook and a scarf, the edge of the lid {NEON}",  # 084
    f"a long staircase of many small steps climbing into the distance, the top step {NEON}",  # 085
    f"{CH} sitting by a window exhaling a long slow stream of air through her lips, the stream {NEON}",  # 086
    f"a balloon slowly deflating beside a heart, its air flowing out in a long stream {NEON}",  # 087
    f"{CH} breathing calmly with her eyes closed next to a large hourglass, the falling sand {NEON}",  # 088
    f"two wave lines, one of breathing and one of heartbeat, overlapping perfectly in rhythm, the merged wave {NEON}",  # 089
    f"{CH} sitting cross-legged on her bed in the morning with her eyes closed, a small sand timer beside her {NEON}",  # 090
    f"a folded cold wet towel beside a bowl of ice cubes on a bathroom counter, the ice cubes {NEON}",  # 091
    f"a university laboratory where a volunteer sits in a chair while a small cooling device touches the side of her neck, the device {NEON}",  # 092
    f"side view of a neck as an {ANAT}, the nerve {NEON} running beside the big artery, a small snowflake shape next to it",  # 093
    f"a heartbeat line slowing down with wider gaps between the beats, the line {NEON}, a small snowflake shape above it",  # 094
    f"{CH} at a bathroom sink pressing a folded cold towel against the side of her neck with her eyes closed, the towel {NEON}",  # 095
    f"{CH} singing happily in the shower with her mouth open, musical notes floating up through the steam, the notes {NEON}",  # 096
    f"side view of a throat as an {ANAT} showing the voice box, a thin nerve branch {NEON} reaching it",  # 097
    f"{CH} holding one long sung note, a long flowing ribbon of sound leaving her mouth {NEON}",  # 098
    f"a choir rehearsal room in Sweden with tall windows, a grand piano and rows of chairs, the conductor's baton {NEON}",  # 099
    f"a group of eighteen-year-old students singing together in a choir, blank music stands, musical notes floating above them {NEON}",  # 100
    f"a row of small hearts side by side, all beating in perfect sync, linked by one wave line {NEON}",  # 101
    f"{CH} driving a small car with the window down, humming along with the car radio, the radio dial {NEON}",  # 102
    f"long-distance runners on a country road at dawn, the lead runner's sneakers {NEON}",  # 103
    f"a runner resting on a bench after a race, two fingers on the wrist feeling a calm slow pulse, a slow heart outline {NEON}",  # 104
    f"{CH} walking briskly through a park with tall trees and a pond, her sneakers {NEON}",  # 105
    f"{CH} dancing alone in her living room wearing headphones, a record player beside her, the headphones {NEON}",  # 106
    f"{CH} sleeping peacefully in bed under a window with a crescent moon, the moon {NEON}",  # 107
    f"{CH} and two friends sitting at a café table talking calmly, steam rising from their cups, the steam {NEON}",  # 108
    f"{CH} laughing with her grandmother on a porch, the grandmother's hand resting on hers, their hands {NEON}",  # 109
    f"a university campus in North Carolina with a brick bell tower, old oak trees and students walking, the top of the bell tower {NEON}",  # 110
    f"a network of simple stick figures connected to each other by thin lines like a web, the connecting lines {NEON}",  # 111
    f"{CH} hugging a friend on a train station platform, the space between their hearts {NEON}",  # 112
    f"a spiral staircase rising upward seen from below, the spiral handrail {NEON}",  # 113
    f"a group of friends sitting around a campfire at night under the stars, the campfire {NEON}",  # 114
    f"{CH} standing again at a lectern in a school auditorium facing rows of seated audience, the small lectern lamp {NEON}",  # 115
    f"close-up of {CH} at the lectern taking a short calm breath through her nose, a small swirl of air {NEON}",  # 116
    f"{CH} at the lectern exhaling slowly, a long ribbon of breath {NEON} floating out over the audience",  # 117
    f"{SIL} at a lectern; a single nerve {NEON} runs from her brain down her neck, around her heart and down to her belly",  # 118
    f"{CH} smiling and speaking confidently from the lectern, the audience in the rows smiling back, her heart {NEON}",  # 119
    f"a single sneaker resting gently on a brake pedal on a dark floor with wide empty space around it, the brake pedal {NEON}",  # 120
]
