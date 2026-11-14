# -*- coding: utf-8 -*-
"""Candidatas de voz para Crónicas de Call of Duty (canal nuevo, 2-nov-2026), CUENTA 1 de ElevenLabs.
Latinas, graves y poco usadas en la biblioteca (se evitan Miguel «Deep, Rich» por sobreusada y El Faraón por sonar a Runa Caída).
Misma prueba para todas (gancho + narración + burla); las voces de la biblioteca compartida se usan por id sin añadirlas.
Uso (desde la carpeta de un video, porque tts_eleven importa config): python <ruta>/_generar.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

MODELO = "eleven_v4_turbo"
TEXTO = ("[serious] Llevas semanas jugando Modern Warfare 4. [short pause] Pero hay cosas que los desarrolladores escondieron "
         "a plena vista, [short pause] y casi nadie las ha visto. [long pause] Hoy vamos a encontrarlas todas: veinticinco "
         "secretos, [short pause] de menos a más. [sighs] Y sí, el número uno te va a hacer volver a jugar la campaña. "
         "[long pause] [amused] Si tú también disparaste primero y preguntaste después, [short pause] tranquilo: "
         "[deadpan] aquí no juzgamos a nadie.")
VOCES = {   # nombre: voice_id (ElevenLabs: nombre y etiquetas)
    "1_damian": "BPwS5yO6aXvwg8auqNwS",     # Damián - Deep, Rich & Resonant (Latinoamérica; biblioteca)
    "2_brian_cortez": "fk9Z59P6ZsSa6Wv2ZO34",  # Brian Cortez - Narrative, Persuasive (Latinoamérica)
    "3_ricardo_peralta": "CRd8Hcm56JNs2lcw5bbH",  # Ricardo Peralta - Narrator (Latinoamérica)
}
AQUI = os.path.dirname(os.path.abspath(__file__))
E._activa = 0   # cuenta 1
total = 0
for nombre, vid in VOCES.items():
    ruta = os.path.join(AQUI, f"{nombre}.mp3")
    if os.path.exists(ruta):
        continue
    r = E.post(f"text-to-speech/{vid}?output_format=mp3_44100_128", timeout=120,
               json=dict(text=TEXTO, model_id=MODELO, seed=7, language_code="es", voice_settings=dict(stability=0.5)))
    if r.status_code != 200:
        print(nombre, "ElevenLabs", r.status_code, r.text[:200], flush=True)
        continue
    open(ruta, "wb").write(r.content)
    c = int(r.headers.get("character-cost") or 0)
    total += c
    print(nombre, "costo", c, flush=True)
print("créditos gastados", total, "· saldos", E.saldos())
