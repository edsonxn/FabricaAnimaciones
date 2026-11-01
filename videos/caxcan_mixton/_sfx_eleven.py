# -*- coding: utf-8 -*-
"""SFX grabados con ElevenLabs (sound-generation) para lo que el procedural no da: multitudes, batalla, derrumbe, perros, caballos,
cañón, caracol, metate, bebé, hierro candente, galeón (21-oct-2026; el usuario recargó saldo: cuenta 3). Salta los que ya están en
sfx/. Uso: desde C:\\FabricaAnimaciones, `python videos/caxcan_mixton/_sfx_eleven.py`."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import tts_eleven as E  # noqa: E402

SONIDOS = {
    "multitud_grito": ("Thousands of indigenous warriors on a mountaintop roaring a war cry in unison, epic, outdoors, long echo in a canyon", 6),
    "multitud_canto": ("A crowd of indigenous people singing and chanting joyfully at night around a bonfire, clay flutes and log drums", 8),
    "derrumbe": ("Rockslide: many big boulders tumbling and crashing down a steep rocky slope, deep rumble, dust, outdoors", 6),
    "batalla": ("Distant 16th century battle: war cries, clashing swords and wooden clubs, arrows whistling, chaos, outdoors", 10),
    "perros": ("Several big war mastiffs barking aggressively in the distance on a dusty road, outdoors", 5),
    "caballos": ("Armored horses neighing and snorting nervously, hooves stamping on dry ground, outdoors", 4),
    "canonazo": ("A 16th century bronze cannon firing, deep boom with a long echo rolling through a canyon", 4),
    "caracol": ("A conch shell trumpet blown long and deep, indigenous Mexican ritual horn, echo in a canyon", 4),
    "metate": ("Stone mano grinding corn on a stone metate, slow rhythmic scraping of stone on stone, close, quiet room", 8),
    "bebe": ("A newborn baby crying softly and then cooing, in a small quiet adobe room", 4),
    "hierro": ("A red-hot branding iron pressed on skin-like leather, loud sharp sizzle and hiss, smoke", 3),
    "incendio": ("A village burning: large fire roaring, thatched roofs crackling, wooden beams cracking and collapsing", 8),
    "arcabuz": ("Several matchlock arquebus gunshots fired one after another, outdoors, echo", 3),
    "tormenta": ("Heavy rainstorm on a rocky mountain, sheets of rain on rocks and mud, low thunder rumbling", 10),
    "galeon": ("Wooden sailing ship at sea: hull creaking, waves splashing against the hull, wind in the canvas sails", 8),
    "marcha": ("A huge army marching: thousands of footsteps, armor clinking, war drums far away, outdoors", 8),
    "latigo": ("A single leather whip crack, outdoors", 1),
}

os.makedirs(os.path.join(AQUI, "sfx"), exist_ok=True)
gasto = 0
for n, (txt, dur) in SONIDOS.items():
    dst = os.path.join(AQUI, "sfx", n + ".mp3")
    if os.path.exists(dst):
        continue
    r = E.post("sound-generation", timeout=180, json=dict(text=txt, duration_seconds=max(0.5, min(float(dur), 22)),
                                                          prompt_influence=0.45))
    if r.status_code != 200:
        print(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:200]}")
        continue
    open(dst, "wb").write(r.content)
    gasto += int(r.headers.get("character-cost") or 0)
    print(f"sfx/{n}.mp3  {dur} s", flush=True)
print("créditos:", gasto)
