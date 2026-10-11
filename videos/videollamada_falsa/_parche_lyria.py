# -*- coding: utf-8 -*-
"""Una vez: adapta _lyria_segmentos.py (copiado de ia_noir) a las 12 escenas de este video."""
import os
import re

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lyria_segmentos.py")
s = open(p, encoding="utf-8").read()
NUEVO = '''SEC = {
    "regla": ("Opening in the rain: a lonely muted trumpet over upright bass and soft brushes, a suspended chord, quiet suspense; a cold synthetic shimmer creeps in at the end.", 4),
    "mensaje": ("A slow ticking pulse, low piano motif, cold glassy electronic tones under noir bass, wary and restrained.", 4),
    "llamada": ("Eerie calm: sustained strings, a too-perfect celesta motif, something slightly wrong underneath, tension held back.", 5),
    "dinero": ("Driving low string ostinato with a steady pulse like a counting machine, staccato low brass accents, rising.", 7),
    "descubre": ("The floor drops: sudden sparse texture, a single low piano note repeating, cold dread, hollow room tone.", 5),
    "truco": ("Mysterious investigation: walking upright bass, brushes, a curious muted trumpet line, glitchy electronic details.", 5),
    "manual": ("Four clear steps, each a little more tense: ticking clock, low strings climbing, a dark waltz feel, strong accent at the end.", 7),
    "victima": ("A grave reveal: slow dark brass chords and low strings, wide and heavy, then a cold quiet pulse.", 6),
    "sinrostro": ("Bleak and empty: lonely muted trumpet in the rain over a low drone, unresolved harmony.", 5),
    "senales": ("Uneasy forward motion: ticking pulse, low string ostinato returning, dark electronic shimmer.", 6),
    "leccion": ("Resolve and warning: steady determined pulse, piano and strings gaining clarity and strength, the firmest moment of the score.", 8),
    "cierre": ("A slow solitary muted trumpet and piano theme in the rain, haunting and existential, fading out to silence.", 3),
}
TRAMOS = [
    (["regla", "mensaje", "llamada", "dinero"], "Begin from near silence with rain-like texture. End on a sustained low tone that can flow into the next piece. No loud ending."),
    (["descubre", "truco", "manual"], "Begin with a held low tone. Steady growth in tension. End on a sustained low tone, no loud ending."),
    (["victima", "sinrostro", "senales", "leccion", "cierre"], "Begin with a held low pulse. Grave and wide, build to the firmest intensity near the end, then calm down and end with a slow fade-out to silence."),
]'''
s2, n = re.subn(r"SEC = \{.*?\n\]", lambda m: NUEVO, s, count=1, flags=re.S)
assert n == 1
open(p, "w", encoding="utf-8", newline="\n").write(s2)
print("ok")
