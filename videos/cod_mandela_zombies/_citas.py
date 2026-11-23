# -*- coding: utf-8 -*-
"""Citas de cod_mandela_zombies (22-nov-2026): baja SOLO el tramo de audio de cada cita y lo transcribe con palabras con tiempo
(faster-whisper en CPU: hay un render en la GPU). Uso: python _citas.py [slug ...]  -> audio/_citas/<slug>.m4a + tiempos."""
import os
import subprocess
import sys

from faster_whisper import WhisperModel

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "_citas")
os.makedirs(D, exist_ok=True)
# slug: (video, desde, hasta, idioma) — segundos de investigacion.md § D con margen
TAREAS = {
    "nixon": ("iYkE5v8KzQw", 46, 60, "en"),
    "nikolai": ("H-hHlX77ips", 85, 104, "en"),
    "raygun": ("WDjR3vkOQeU", 30, 60, "ja"),
}
pedidas = sys.argv[1:] or list(TAREAS)
m = WhisperModel("small", device="cpu", compute_type="int8")
for slug in pedidas:
    vid, a, b, lang = TAREAS[slug]
    out = os.path.join(D, slug + ".m4a")
    if not os.path.exists(out):
        subprocess.run(["yt-dlp", "-q", "--no-warnings", "-f", "bestaudio[ext=m4a]/bestaudio", "--download-sections", f"*{a}-{b}",
                        "-o", out, "https://youtu.be/" + vid])
    if not os.path.exists(out):
        print(slug, "SIN AUDIO")
        continue
    segs, _ = m.transcribe(out, language=lang, word_timestamps=True, vad_filter=False)
    print(f"== {slug} ({vid} desde {a} s)")
    for s in segs:
        print("   " + " ".join(f"{w.word.strip()}@{a + w.start:.1f}" for w in s.words))
    sys.stdout.flush()
