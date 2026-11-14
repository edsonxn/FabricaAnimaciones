# -*- coding: utf-8 -*-
"""Comparativa de voz para Runa Caída (11-nov-2026): el usuario quiere probar «el Profeta» (ElevenLabs God - Deep, Powerful,
HNSF1CTQmub252yhXROX) en lugar de Chatterbox Faraon. Mismo párrafo del video de Mohg (puesto 4, p4_4 + p4_5):
A = la toma Faraon ya grabada en er_mohg_atrocidades (sin gastar GPU); B = el Profeta en eleven_v4_turbo, escritura normal.
Uso: python canales/muestras_voz/runa_profeta/_generar.py"""
import os
import subprocess
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

AQUI = os.path.dirname(os.path.abspath(__file__))
MOHG = r"C:\FabricaAnimaciones\videos\er_mohg_atrocidades\voz\final"
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
TEXTO = ("Y lo explica con toda la calma del mundo. Normalmente, este ritual implicaría matar a tu propia doncella "
         "y renegar de la sabiduría de los Dos Dedos. [short pause] Pero como no tienes doncella, sirve la sangre "
         "de la doncella de cualquiera. [long pause] [sarcastic] Normalmente. [short pause] O sea, que para entrar en la orden, "
         "los caballeros de Mohg, uno a uno, mataban a la doncella que los guiaba. [short pause] A la persona que se suponía "
         "que iba a acompañarlos hasta el Círculo de Elden.")
VID = "HNSF1CTQmub252yhXROX"

# A: Faraon (la actual), las dos tomas reales unidas con 0,6 s de silencio
a = os.path.join(AQUI, "A_actual_faraon.mp3")
if not os.path.exists(a):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", os.path.join(MOHG, "p4_4.wav"), "-i", os.path.join(MOHG, "p4_5.wav"),
                    "-filter_complex", "[0]apad=pad_dur=0.6[x];[x][1]concat=n=2:v=0:a=1,loudnorm=I=-16[o]", "-map", "[o]",
                    "-ar", "44100", "-b:a", "160k", a], check=True)

# B: el Profeta, cuenta con más saldo
b = os.path.join(AQUI, "B_profeta.mp3")
if not os.path.exists(b):
    s = E.saldos()
    print("saldos", s)
    E._activa = max(range(len(s)), key=lambda i: s[i][1] or 0)
    r = E.post(f"text-to-speech/{VID}?output_format=mp3_44100_128", timeout=120,
               json=dict(text=TEXTO, model_id="eleven_v4_turbo", seed=7, language_code="es",
                         voice_settings=dict(stability=0.5)))
    if r.status_code != 200:
        sys.exit(f"ElevenLabs {r.status_code} {r.text[:300]}")
    crudo = b + ".tmp.mp3"
    open(crudo, "wb").write(r.content)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", crudo, "-af", "loudnorm=I=-16", "-ar", "44100", "-b:a", "160k", b],
                   check=True)
    os.remove(crudo)
    print("costo", r.headers.get("character-cost"))

# Comparativa en un solo archivo: A, 1,5 s de silencio, B
ab = os.path.join(AQUI, "comparativa_A_faraon_B_profeta.mp3")
subprocess.run([FF, "-y", "-loglevel", "error", "-i", a, "-i", b, "-filter_complex",
                "[0]apad=pad_dur=1.5[x];[x][1]concat=n=2:v=0:a=1[o]", "-map", "[o]", "-b:a", "160k", ab], check=True)
print("listo", ab)
