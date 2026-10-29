# -*- coding: utf-8 -*-
"""Casting de voces de personajes (ElevenLabs, biblioteca pública) para la Crematoria: cada candidato dice una línea EN PERSONAJE
con corchetes. No toca voz/. Uso: python _prueba_personajes.py [personaje …] → muestras_personajes/<personaje>_<n>_<voz>.mp3
y muestras_personajes/todas.mp3 (con la narradora presentando a cada uno)."""
import io
import os
import subprocess
import sys

import librosa

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import tts_eleven  # noqa: E402

NARRADORA = "BwV6RplmLHPGm7QVf6II"
OUT = os.path.join(AQUI, "muestras_personajes")
os.makedirs(OUT, exist_ok=True)

# personaje: (presentación de la narradora, línea en personaje, [(nombre, voice_id), …])
CASTING = {
    "alexandros": ("Alexandros Mograine, el Crematoria.",
                   "[serious] Mientras yo empuñe esta espada, ningún muerto volverá a levantarse en Lordaeron. [short pause] Ninguno.",
                   [("salvatore", "t3eeeqhBjrUqcrPvDqUn"), ("elder", "gSYqSbtMajxq5LUT0bNl")]),
    "tirion": ("Tirion Vadín.",
               "[sad] Hijo… [short pause] perdóname. Llegué tarde. [sighs] Siempre llego tarde.",
               [("arturo", "N2HSRirbsHTZ8DE2WqjB"), ("elder", "gSYqSbtMajxq5LUT0bNl")]),
    "renault": ("Renault Mograine, el hijo mayor.",
                "[whispers] Padre, la Plaga no te va a matar. [short pause] Yo sí.",
                [("enrique", "iDEmt5MnqUotdwCIVplo"), ("antonio", "htFfPSZGJwjBv1CL0aMD")]),
    "darion": ("Darion Mograine, el hijo menor.",
               "[angry] ¡Me arrancaste el corazón, Rey Exánime! [short pause] ¡Ahora vas a tener que arrancarme el alma!",
               [("alejandro", "byWOh4ohcovt7I8koF2I"), ("david", "qRUgOhnxGASxirG4fKjv")]),
    "taelan": ("Taelan Vadín.",
               "[excited] ¡Padre! [short pause] Sabía que vendrías. Te lo juro, lo sabía.",
               [("david", "qRUgOhnxGASxirG4fKjv"), ("antonio", "htFfPSZGJwjBv1CL0aMD")]),
    "isillien": ("El Gran Inquisidor Isillien.",
                 "[sarcastic] Qué conmovedor. El traidor vino a ver morir a su hijo. [short pause] Que así sea.",
                 [("murdock", "OLmSqlYzB06EIKJRy5b0"), ("odran", "HnC0hwQkrsAhaQN1Y2HD")]),
    "kelthuzad": ("Kel'Thuzad, el amo de Naxxramas.",
                  "[whispers] Tu padre sirve ahora a un señor más grande, muchacho. [short pause] Igual que pronto lo harás tú.",
                  [("ivan", "oqO5cdAzjE5Ik5xWIZRL"), ("mordred", "UFO0Yv86wqRxAt1DmXUu")]),
    "rey_exanime": ("El Rey Exánime.",
                    "[serious] Arrodíllate. [short pause] La muerte no es el final, Mograine. [whispers] Es el principio de tu servicio.",
                    [("miguel", "k8cFOyAg7B9qwBlDDNTC"), ("final_boss", "d3qrd1ge6zWDvUxIeXiH")]),
    "eitrigg": ("Eitrigg, el orco.",
                "[sighs] Un humano me perdonó la vida, y por eso lo perdió todo. [short pause] Los orcos no olvidamos esas deudas.",
                [("ragnar", "09BJBPASOGbr1evokbCu"), ("ludovico", "GTY55jD77hLBRrnQOhNk")]),
}


def tts(voz, texto, archivo):
    body = dict(text=texto, model_id="eleven_v4_turbo", seed=1, language_code="es", voice_settings=dict(stability=0.5))
    r = tts_eleven.post(f"text-to-speech/{voz}?output_format=mp3_44100_128", json=body, timeout=180)
    if r.status_code != 200:
        print("  ERROR", voz, r.status_code, r.text[:200])
        return None, 0
    open(archivo, "wb").write(r.content)
    y, sr = librosa.load(io.BytesIO(r.content), sr=None, mono=True)
    return len(y) / sr, int(r.headers.get("character-cost") or 0)


def main():
    pedidos = sys.argv[1:] or list(CASTING)
    orden, total = [], 0
    for per in pedidos:
        pres, linea, cands = CASTING[per]
        a = os.path.join(OUT, f"{per}_0_narradora.mp3")
        tts(NARRADORA, f"[thoughtful] {pres}", a)
        orden.append(a)
        for n, (nom, vid) in enumerate(cands, 1):
            f = os.path.join(OUT, f"{per}_{n}_{nom}.mp3")
            dur, c = tts(vid, linea, f)
            total += c
            if dur:
                print(f"{per:12s} {n} {nom:11s} {dur:5.2f}s costo {c}")
                orden.append(f)
    print("total", total, "créditos (sin contar a la narradora)")
    sil = os.path.join(OUT, "_sil.mp3")
    lista = os.path.join(OUT, "_lista.txt")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.9",
                    "-b:a", "128k", sil], check=True)
    with open(lista, "w", encoding="utf-8") as fh:
        for f in orden:
            fh.write(f"file '{f.replace(os.sep, '/')}'\nfile '{sil.replace(os.sep, '/')}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-ac", "1", "-ar", "44100",
                    "-b:a", "128k", os.path.join(OUT, "todas.mp3")], check=True)
    os.remove(sil)
    os.remove(lista)


if __name__ == "__main__":
    main()
