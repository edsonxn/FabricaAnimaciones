# -*- coding: utf-8 -*-
"""2.ª prueba (11-nov-2026): el usuario quiere al Profeta «épico, malhumorado»: enojado, gruñón, gritón, decepcionado y a ratos con
la voz quebrada. Mismo pasaje de Mohg (puesto 4, más largo). Dos variantes para decidir si los gritos entran (la regla del 2-nov
prohíbe [shouts]; aquí se llama a la API directa, sin tts_eleven.sin_etiquetas, para poder oírlo):
  C_profeta_emociones.mp3       enojado/gruñón/decepcionado/quebrado, SIN etiqueta de grito (solo signos ¡!)
  D_profeta_emociones_gritos.mp3 lo mismo + [shouting] en dos remates
Estabilidad «Creative» (0.0) para que actúe más. Uso: python canales/muestras_voz/runa_profeta/_generar_emociones.py"""
import os
import subprocess
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

AQUI = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
VID = "HNSF1CTQmub252yhXROX"

BASE = ("[grumpy] Si le dices que sí, te entrega un paño de juramento blanco. El Favor del Señor de la Sangre. [short pause] "
        "[angry] Y la prueba final: {G1}¡empapa el paño con la sangre de una doncella! [long pause] "
        "[sighs] Y lo explica con toda la calma del mundo. [sarcastic] Normalmente, este ritual implicaría matar a tu propia doncella. "
        "Pero como no tienes doncella, sirve la de cualquiera. [short pause] "
        "[frustrated] Normalmente. ¡Como si fuera un trámite! O sea, que los caballeros de Mohg, uno a uno, mataban a la doncella "
        "que los guiaba. [disappointed] A la persona que se suponía que iba a acompañarlos hasta el Círculo de Elden. [long pause] "
        "[voice breaking] O el tercer camino. Matar a Irina, la chica ciega del Puente del Sacrificio. [short pause] La que solo te pide... "
        "que le lleves una carta a su padre. [long pause] "
        "[growls] Y para Varré, da igual cuál. [angry] {G2}¡Mientras sangre!")
VARIANTES = {
    "C_profeta_emociones": BASE.format(G1="", G2=""),
    "D_profeta_emociones_gritos": BASE.format(G1="[shouting] ", G2="[shouting] "),
}

s = E.saldos()
E._activa = max(range(len(s)), key=lambda i: s[i][1] or 0)
for nombre, texto in VARIANTES.items():
    ruta = os.path.join(AQUI, nombre + ".mp3")
    if os.path.exists(ruta):
        continue
    for estab in (0.0, 0.5):
        r = E.post(f"text-to-speech/{VID}?output_format=mp3_44100_128", timeout=180,
                   json=dict(text=texto, model_id="eleven_v4_turbo", seed=7, language_code="es",
                             voice_settings=dict(stability=estab)))
        if r.status_code == 200:
            break
        print(nombre, "estabilidad", estab, "→", r.status_code, r.text[:200])
    else:
        sys.exit(1)
    crudo = ruta + ".tmp.mp3"
    open(crudo, "wb").write(r.content)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", crudo, "-af", "loudnorm=I=-16", "-ar", "44100", "-b:a", "160k", ruta],
                   check=True)
    os.remove(crudo)
    print(nombre, "estabilidad", estab, "costo", r.headers.get("character-cost"))
print("saldos", E.saldos())
