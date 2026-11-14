# -*- coding: utf-8 -*-
"""2.ª ronda de voces para Expediente 141 (2-nov-2026): el usuario quiere «soldado adulto, como de sargento».
Le gustó Damián (1.ª ronda) y entra de referencia con el texto nuevo. Latinas, maduras, roncas o de mando; sin El Faraón (= Runa Caída).
Uso (desde la carpeta de un video, porque tts_eleven importa config): python <ruta>/_generar_sargento.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

MODELO = "eleven_v4_turbo"
TEXTO = ("[serious] Atención, soldado. [short pause] Llevas semanas jugando Modern Warfare 4 y crees que ya lo viste todo. "
         "[short pause] Error. [long pause] Los desarrolladores escondieron veinticinco secretos a plena vista, "
         "[short pause] y hoy los vamos a sacar uno por uno. [sighs] El número uno te va a obligar a jugar la campaña otra vez. "
         "[long pause] [amused] Y si tú también disparaste primero y preguntaste después, [short pause] [deadpan] "
         "descansa: aquí nadie te va a juzgar.")
VOCES = {   # nombre: voice_id (ElevenLabs: nombre y etiquetas)
    "s0_damian": "BPwS5yO6aXvwg8auqNwS",          # Damián - Deep, Rich & Resonant (referencia, le gustó al usuario)
    "s1_santiago": "VXZKNah1ssrzM8c81OiY",        # Santiago - Gravelly and commanding (Latinoamérica, mayor)
    "s2_hugo_guerrero": "OhX3N1ymJnjcWrWhh53P",   # Hugo Guerrero (México, grave, algo ronca)
    "s3_emilio": "DV9FrN0pQkPWIoxW5dvT",          # Emilio - Weathered and Grounded (México, curtida)
    "s4_paul_urbina": "r2goToszgNLUzvFARGqy",     # Paul Urbina - Latino Male, gravelly (mayor)
    "s5_chris": "re0pzsXzyvweLpAwMscE",           # Chris (México, disciplinada, autoritaria)
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
