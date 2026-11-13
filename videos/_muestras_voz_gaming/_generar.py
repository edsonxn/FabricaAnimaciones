# -*- coding: utf-8 -*-
"""Muestras de voz para Crónicas del gaming (12-nov-2026): el usuario quiere probar una voz GRAVE y PROFUNDA como la del
Profeta para el siguiente video, y que el público vote entre la nueva y Hope. Misma frase para todas, turbo, cuenta 2.
Uso: python _generar.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

MODELO = "eleven_v4_turbo"
TEXTO = ("Nintendo dijo que el remake de Ocarina of Time era fiel al original. [short pause] Fiel. [long pause] "
         "Y luego quitó tres cosas que llevaban veintiocho años ahí, sin decírselo a nadie. [short pause] "
         "[sarcastic] Pero tranquilo, que tú no las ibas a buscar... ¿o sí?")
VOCES = {   # nombre: voice_id (biblioteca /v1/shared-voices, sin las voces que ya usan otros canales)
    "00_hope_actual": "tnSpp4vdxKPjI9w0GnoV",      # Hope: la voz actual del canal (referencia)
    "00_profeta_ref": "HNSF1CTQmub252yhXROX",      # el Profeta (Runa y Tamriel): referencia de lo que pide, NO candidata
    "01_salvatore": "t3eeeqhBjrUqcrPvDqUn",        # Salvatore - Epic, Deep & Trustworthy (Latinoamérica, mayor, místico)
    "02_miguel": "k8cFOyAg7B9qwBlDDNTC",           # Miguel - Deep, Rich and Cinematic (Latinoamérica, voz de tráiler)
    "03_ludovico": "GTY55jD77hLBRrnQOhNk",         # Ludovico - Soothing, Bassy, Booming (Latinoamérica)
    "04_santiago": "VXZKNah1ssrzM8c81OiY",         # Santiago - Gravelly and commanding (Latinoamérica, mayor)
    "05_carlos_aguilar": "8MeTTgXVwMEhRVfblXOj",   # Carlos Aguilar - Resonate and Powerful (Latinoamérica)
    "06_david_misterio": "K3TeN3ZVK8WnOeJ0NYqZ",   # David - Deep, Attractive, Mysterious (Latinoamérica, terror/misterio)
    "07_francis": "7UB6WMKyZDj19XRGC8Sb",          # Francis - Deep, Touching (Latinoamérica)
    "08_arconte": "QtPMrakdgePQIUwOX7Ut",          # Arconte - Evocative, Deep and Elegant (España)
}
AQUI = os.path.dirname(os.path.abspath(__file__))
E._activa = next(i for i, (n, _) in enumerate(E.cuentas()) if n == 2)
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
