# -*- coding: utf-8 -*-
"""Prueba de voces graves de la biblioteca pública de ElevenLabs para ramses_ii (4-nov-2026). Cuenta 2."""
import sys, os, requests
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as T
AQUI = os.path.dirname(os.path.abspath(__file__))
FRASE = ("[serious] En 1976, un hombre que llevaba más de tres mil años muerto recibió un pasaporte. [short pause] "
         "En la casilla de profesión, se cuenta que escribieron: rey. [long pause] Fallecido.")
VOCES = dict(ludovico="GTY55jD77hLBRrnQOhNk", salvatore="t3eeeqhBjrUqcrPvDqUn", hugo="HIkzxzvsigFIynXHHKhU",
             uqenn="7l94t51oArRmdopaZXn5", josue="SAGbayTufdvOWwIvhMH2")
k = dict(T.cuentas())[2]
for n, vid in VOCES.items():
    out = os.path.join(AQUI, f"{n}.mp3")
    if os.path.exists(out): continue
    r = requests.post(f"{T.URL}/text-to-speech/{vid}?output_format=mp3_44100_128", headers={"xi-api-key": k},
                      json=dict(text=FRASE, model_id="eleven_v4_turbo", seed=7, language_code="es",
                                voice_settings=dict(stability=0.5)), timeout=120)
    print(n, r.status_code, r.headers.get("character-cost"), r.text[:200] if r.status_code != 200 else "")
    if r.status_code == 200: open(out, "wb").write(r.content)
