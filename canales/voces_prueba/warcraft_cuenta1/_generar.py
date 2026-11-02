# -*- coding: utf-8 -*-
"""Candidatas para Crónicas de Warcraft con la CUENTA 1 de ElevenLabs (la de más saldo, que no puede clonar), 2-nov-2026.
Misma prueba para todas (burla + narración, sin [whispers] ni [excited]); referencia = el clon (cuentas 2 y 3).
Las voces de la biblioteca compartida se usan por id sin añadirlas a la cuenta.
Uso (desde la carpeta de un video, porque tts_eleven importa config): python <ruta>/_generar.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

MODELO = "eleven_v4_turbo"
TEXTO = ("[amused] Y hablando de gustos raros, también nos llegan comentarios como este. [short pause] [sarcastic] Totalmente de "
         "acuerdo en algo: el asco es algo muy personal. [short pause] [laughs softly] Por eso acabo de explicarte cómo bailarle a "
         "una babosa en una cloaca: [deadpan] aquí respetamos todos los gustos. [long pause] Al principio de la beta de World of "
         "Warcraft Forever, comértela te convertía en un múrloc o en un ogro, y la gente estaba encantada. [sighs] Blizzard aclaró "
         "que eso era un efecto provisional, [short pause] y ahora te convierte en un orco vestido de ninja o de pirata. "
         "[mischievously] O sea que en algún parche volverás a ser múrloc, [short pause] y esta vez a propósito.")
VOCES = {   # nombre: voice_id (ElevenLabs: nombre y etiquetas)
    "1_johnny": "HMCmDsbKeaSZp5LMOYKR",     # Johnny - Mocking, Sarcastic and Rich (España; base de Sarcastica)
    "2_tony": "lRf3yb6jZby4fn3q3Q7M",       # Tony - Witty, Upbeat and Engaging (México; biblioteca)
    "3_jorge": "HAsl3FenyWHYwECSP6Hl",      # Jorge - Measured, Calm, Warm (Latinoamérica; biblioteca)
    "4_edoardo": "YqZLNYWZm98oKaaLZkUA",    # Edoardo - Dark, Measured, Natural (Latinoamérica)
    "5_joan": "69MPtsbmUppiEyKo3zhT",       # Joan - Deep Mystery and warm (Latinoamérica)
    "6_jc": "4XUsiqPDK4UACIM2BILe",         # JC - Energetic News Broadcaster (Latinoamérica)
    "7_jose": "y2ijeTfmnXjzheHO6zeN",       # Jose - Agradable voz de locutor (México)
    "8_ginyin": "nMPrFLO7QElx9wTR0JGo",     # Ginyin - Energetic, Clear and Engaging
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
