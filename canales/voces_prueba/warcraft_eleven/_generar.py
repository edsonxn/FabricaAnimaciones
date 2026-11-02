# -*- coding: utf-8 -*-
"""Prueba de voz: clon en ElevenLabs de la voz Applio de Crónicas de Warcraft (Remy + RVC RemyOriginal), con corchetes
(el usuario, 2-nov-2026). El clon vive SOLO en la cuenta 3 (`sm2N86ydG2QhV8LIVa9b`), hecho con 152 s de voz/final de
wow_objetos_secretos_forever. Mismas frases que ese video, para compararlas con las tomas de Applio (applio_*.mp3).
Uso (desde la carpeta de un video, porque tts_eleven importa config): python <ruta>/_generar.py"""
import os
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

VOICE = "sm2N86ydG2QhV8LIVa9b"
MODELO = "eleven_v4_turbo"
VIDEO = r"C:\FabricaAnimaciones\videos\wow_objetos_secretos_forever"
PRUEBAS = {   # nombre: (texto con corchetes, tomas de Applio con las mismas frases)
    "1_gancho": ("[intrigued] World of Warcraft Forever tiene más de treinta y un mil objetos, [short pause] y Blizzard escondió "
                 "las estadísticas de doce mil quinientos noventa y cuatro. [short pause] Puedes ver que existen, "
                 "[whispers] pero no qué hacen, [normal] hasta que alguien en el mundo consigue uno y el juego se lo revela a todos.",
                 ["intro_0", "intro_1"]),
    "2_burla": ("[amused] Y hablando de gustos raros, también nos llegan comentarios como este. [short pause] "
                "[sarcastic] Totalmente de acuerdo en algo: el asco es algo muy personal. [short pause] "
                "[laughs softly] Por eso acabo de explicarte cómo bailarle a una babosa en una cloaca: "
                "[deadpan] aquí respetamos todos los gustos.",
                ["burla1_0", "burla1_1", "burla1_2"]),
    "3_narracion": ("Al principio de la beta, comértela te convertía en un múrloc o en un ogro, [excited] y la gente estaba encantada. "
                    "[sighs] Blizzard aclaró que eso era un efecto provisional que no debía estar ahí, [short pause] y ahora te "
                    "convierte en un orco vestido de ninja o de pirata. [mischievously] O sea que en algún parche de Forever "
                    "volverás a ser múrloc, [short pause] y esta vez a propósito.",
                    ["c15_4", "c15_5", "c15_7"]),
}
AQUI = os.path.dirname(os.path.abspath(__file__))
E._activa = [n for n, _ in E.cuentas()].index(3)
total = 0
for nombre, (texto, tomas) in PRUEBAS.items():
    ruta = os.path.join(AQUI, f"eleven_{nombre}.mp3")
    if not os.path.exists(ruta):
        r = E.post(f"text-to-speech/{VOICE}?output_format=mp3_44100_128", timeout=120,
                   json=dict(text=texto, model_id=MODELO, seed=7, language_code="es", voice_settings=dict(stability=0.5)))
        if r.status_code != 200:
            raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
        open(ruta, "wb").write(r.content)
        c = int(r.headers.get("character-cost") or 0)
        total += c
        print(nombre, len(texto), "caracteres, costo", c, flush=True)
    ref = os.path.join(AQUI, f"applio_{nombre}.wav")
    if not os.path.exists(ref):   # las mismas frases con la voz actual, para comparar
        partes = []
        for k in tomas:
            a, sr = sf.read(os.path.join(VIDEO, "voz", "final", f"{k}.wav"))
            partes += [a, np.zeros(int(sr * 0.35))]
        sf.write(ref, np.concatenate(partes), sr, subtype="PCM_16")
print("créditos gastados", total, "· saldos", E.saldos())
