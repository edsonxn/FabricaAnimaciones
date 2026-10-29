# -*- coding: utf-8 -*-
"""Prueba de la voz clonada de Gaia Eterna (ElevenLabs BwV6RplmLHPGm7QVf6II) con corchetes de emoción, para el canal nuevo con el
estilo de «Pamela» (wow_darrowshire: cuento narrado + pegatina Flow). No toca ningún video.
Uso: python _prueba_voz.py            → muestras/NN_<nombre>.mp3 + muestras/todas.mp3 + muestras/resumen.txt
     python _prueba_voz.py 3 7        → solo esas pruebas (por número)
Usa tts_eleven.post(): empieza por la primera cuenta con saldo y salta sola a la siguiente."""
import io
import os
import re
import subprocess
import sys

import librosa

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "nucleo"))
import tts_eleven  # noqa: E402

VOZ = "BwV6RplmLHPGm7QVf6II"   # «Zyan gameplay 2», clonada: SOLO existe en la cuenta 2 (las otras dan voice_not_found)
tts_eleven._activa = [n for n, _ in tts_eleven.cuentas()].index(2)
OUT = os.path.join(AQUI, "muestras")
os.makedirs(OUT, exist_ok=True)

BASE = ("Nadie volvió a ver a la niña. [short pause] Pero cada noche, a la misma hora, "
        "alguien encendía una vela en la ventana.")
# (nombre, texto, modelo, stability)
PRUEBAS = [
    # 1-3: la misma frase sin etiquetas y con las tres estabilidades que aceptan v3/v4
    ("base_sin_etiquetas", "Nadie volvió a ver a la niña. Pero cada noche, a la misma hora, alguien encendía una vela en la ventana.",
     "eleven_v4_turbo", 0.5),
    ("base_creativa_st0", BASE, "eleven_v4_turbo", 0.0),
    ("base_natural_st05", BASE, "eleven_v4_turbo", 0.5),
    ("base_robusta_st1", BASE, "eleven_v4_turbo", 1.0),
    ("base_v4_completo", BASE, "eleven_v4", 0.5),
    # emociones, una por muestra (cuento de lore, como Darrowshire)
    ("whispers", "[whispers] Y entonces, en el sótano, algo respondió. [short pause] Con su misma voz.",
     "eleven_v4_turbo", 0.5),
    ("sighs", "[sighs] Su madre la esperó durante once años. [short pause] Nunca cerró la puerta con llave.",
     "eleven_v4_turbo", 0.5),
    ("sad", "[sad] Lo último que le dijo fue «vuelvo antes de que oscurezca». [short pause] Y no volvió.",
     "eleven_v4_turbo", 0.5),
    ("softly", "[softly] «No tengas miedo», le dijo la anciana. «El bosque solo se lleva a los que corren.»",
     "eleven_v4_turbo", 0.5),
    ("thoughtful", "[thoughtful] Hay leyendas que nacen de una mentira. [short pause] Y otras que nacen de algo que nadie quiso contar.",
     "eleven_v4_turbo", 0.5),
    ("curious", "[curious] ¿Por qué un pueblo entero dejaría la mesa servida… y se iría a mitad de la cena?",
     "eleven_v4_turbo", 0.5),
    ("serious", "[serious] En 1347 llegaron doce barcos al puerto de Mesina. [short pause] En la mayoría ya no quedaba nadie vivo.",
     "eleven_v4_turbo", 0.5),
    ("nervous", "[nervous] Los guardias contaron a los prisioneros otra vez. [short pause] Eran trece. Esa mañana habían sido doce.",
     "eleven_v4_turbo", 0.5),
    ("excited", "[excited] ¡Y ahí estaba! Después de doscientos años, la ciudad perdida seguía bajo la arena.",
     "eleven_v4_turbo", 0.5),
    ("laughs", "[laughs] Claro que el rey no le creyó. [short pause] Nadie le cree a un cocinero que dice haber visto un dragón.",
     "eleven_v4_turbo", 0.5),
    ("sarcastic", "[sarcastic] Un plan perfecto: esconder el tesoro en el único lugar que todo el reino estaba vigilando.",
     "eleven_v4_turbo", 0.5),
    ("angry_shouting", "El capitán subió a la muralla. [shouting] «¡Nadie abandona esta puerta! ¡Nadie!»",
     "eleven_v4_turbo", 0.5),
    ("crying", "[crying] «Perdóname», escribió en la última página. «Perdóname por no haber llegado a tiempo.»",
     "eleven_v4_turbo", 0.5),
    # mezcla en un mismo párrafo (como se escribe un guion real)
    ("mezcla_parrafo",
     "[thoughtful] Era un pueblo pequeño, de los que en un mapa ni siquiera notarías. [short pause] Tenía un pozo, una herrería "
     "y una niña que cantaba cada tarde. [sighs] Hasta que una tarde, dejó de cantar. [whispers] Y el pozo empezó a hacerlo por ella.",
     "eleven_v4_turbo", 0.5),
]


def una(n, nombre, texto, modelo, st):
    body = dict(text=texto, model_id=modelo, seed=1, language_code="es", voice_settings=dict(stability=st))
    r = tts_eleven.post(f"text-to-speech/{VOZ}?output_format=mp3_44100_128", json=body, timeout=180)
    if r.status_code != 200:
        raise SystemExit(f"{n} {nombre}: ElevenLabs {r.status_code}: {r.text[:300]}")
    p = os.path.join(OUT, f"{n:02d}_{nombre}.mp3")
    open(p, "wb").write(r.content)
    y, sr = librosa.load(io.BytesIO(r.content), sr=None, mono=True)
    dur = len(y) / sr
    pal = len(re.sub(r"\[[^\]]*\]", " ", texto).split())
    costo = int(r.headers.get("character-cost") or 0)
    cuenta = tts_eleven.cuentas()[tts_eleven._activa][0]
    linea = f"{n:02d} {nombre:20s} {modelo:16s} st={st:<3} {dur:5.2f}s {pal / dur:4.2f} pal/s  costo {costo} (cuenta {cuenta})"
    print(linea, flush=True)
    return p, linea, costo


def main():
    pedidas = {int(a) for a in sys.argv[1:]}
    hechas, total = [], 0
    for n, (nombre, texto, modelo, st) in enumerate(PRUEBAS, 1):
        if pedidas and n not in pedidas:
            continue
        p, linea, costo = una(n, nombre, texto, modelo, st)
        hechas.append((p, linea, texto))
        total += costo
    print(f"total {total} créditos")
    with open(os.path.join(OUT, "resumen.txt"), "w", encoding="utf-8") as f:
        for p, linea, texto in hechas:
            f.write(f"{linea}\n    {texto}\n")
        f.write(f"total {total} créditos\n")
    if pedidas:
        return
    # todas seguidas, con 1,2 s de silencio entre muestras, para oírlas de corrido
    lista = os.path.join(OUT, "_lista.txt")
    sil = os.path.join(OUT, "_silencio.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "1.2",
                    "-b:a", "128k", sil], check=True)
    with open(lista, "w", encoding="utf-8") as f:
        for p, _, _ in hechas:
            f.write(f"file '{p.replace(os.sep, '/')}'\nfile '{sil.replace(os.sep, '/')}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-ac", "1", "-ar", "44100",
                    "-b:a", "128k", os.path.join(OUT, "todas.mp3")], check=True)
    os.remove(lista)
    os.remove(sil)


if __name__ == "__main__":
    main()
