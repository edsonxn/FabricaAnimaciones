# -*- coding: utf-8 -*-
"""Sonidos del video: SFX de ElevenLabs (sfx/<nombre>.mp3) y cama musical de Lyria (audio/lyria.mp3).
Cada archivo se genera una sola vez (cuesta créditos); borra el archivo para regenerarlo.

    python sonidos.py            genera lo que falte
    python sonidos.py --sin-musica
"""
import base64
import json
import os
import sys
import time
import urllib.request

import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
TOKENS = os.path.join(AQUI, "..", "..", "canales", "tokens")

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "whoosh": ("Fast airy whoosh swoosh transition, short", 0.8),
    "latigo": ("Quick sharp swish whip pan transition, very short", 0.6),
    "boom": ("Deep comedic bass boom thud hit with short reverb tail, meme vine boom style", 1.5),
    "pop": ("Bright cartoon bubble pop, very short, clean", 0.5),
    "ding": ("Bright positive success ding, checkmark notification chime, clean", 1.0),
    "scratch": ("Vinyl record scratch, abrupt DJ record stop", 1.0),
    "glitch": ("Digital glitch static burst, stutter, short", 0.8),
    "subida": ("Short tense riser sweep building up fast, ending abruptly", 1.5),
    "drama": ("Dramatic orchestral suspense sting, comedic dun dun duuun", 2.0),
    "trinquete": ("Cargo ratchet strap being tightened, fast metallic ratchet clicks", 1.6),
    "puerta": ("Heavy semi truck trailer metal door slamming shut and steel latch locking, loud clang", 1.6),
    "claxon": ("Semi truck air horn, two short loud blasts", 1.6),
    "rapido": ("Tape fast forward whir, cartoon speed up sound", 1.8),
    "golpe": ("Tight punchy sub bass impact hit, short and dry", 0.8),
}

MUSICA = ("Upbeat playful Latin urban instrumental beat for a funny trucker vlog: bouncy tuba-style bass line, bright plucked "
          "requinto guitar riff, punchy claps and trap hi-hats, regional mexicano meets trap groove, 100 BPM, energetic and "
          "cheeky from the very first second, no intro build-up. Total length: about 50 seconds. Instrumental only, no vocals, "
          "no singing, no spoken words. Keep the mid frequencies light so a person talking stays clear on top.")


def sfx():
    clave = open(os.path.join(TOKENS, "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
    gasto = 0
    for n, (txt, dur) in SFX.items():
        if os.path.exists(f"sfx/{n}.mp3"):
            continue
        for intento in range(4):
            r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers={"xi-api-key": clave}, timeout=180,
                              json=dict(text=txt, duration_seconds=max(0.5, float(dur)), prompt_influence=0.5))
            if r.status_code == 200:
                open(f"sfx/{n}.mp3", "wb").write(r.content)
                gasto += int(r.headers.get("character-cost") or 0)
                print(f"  sfx/{n}.mp3  {dur} s", flush=True)
                break
            if r.status_code not in (429, 500, 502, 503):
                raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
            time.sleep(5 * (intento + 1))
    print(f"ElevenLabs: {gasto} créditos en efectos", flush=True)


def musica():
    if os.path.exists("audio/lyria.mp3"):
        return
    clave = open(os.path.join(TOKENS, "google_ai_studio.txt"), encoding="utf-8").read().strip().split()[-1]
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions",
                                 data=json.dumps({"model": "lyria-3.5", "input": MUSICA}).encode(),
                                 headers={"x-goog-api-key": clave, "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())

    def buscar(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "data" and isinstance(v, str) and len(v) > 1000:
                    return v
                x = buscar(v)
                if x:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = buscar(v)
                if x:
                    return x
    b = buscar(r)
    if not b:
        raise SystemExit("Lyria no devolvió audio: " + json.dumps(r)[:400])
    open("audio/lyria.mp3", "wb").write(base64.b64decode(b))
    print("  audio/lyria.mp3", flush=True)


if __name__ == "__main__":
    sfx()
    if "--sin-musica" not in sys.argv:
        musica()
