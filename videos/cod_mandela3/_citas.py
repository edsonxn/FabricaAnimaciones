# -*- coding: utf-8 -*-
"""Citas de cod_mandela3 (19-nov-2026): baja SOLO el tramo de audio de cada cita y lo transcribe con palabras con tiempo
(faster-whisper en CPU: hay un render en la GPU). Uso: python _citas.py [slug ...]  -> audio/_citas/<slug>.m4a + tiempos."""
import os
import subprocess
import sys

from faster_whisper import WhisperModel

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "_citas")
os.makedirs(D, exist_ok=True)
# slug: (video, desde, hasta, idioma) — segundos de investigacion.md § D con margen
TAREAS = {
    "reznov1": ("2UAvWQgRRXQ", 20, 36, "en"),
    "reznov2": ("cnpYaxw8Q9A", 157, 172, "en"),
    "menu50": ("RRYmVb33VU0", 0, 9, "en"),
    "mision50": ("pESIUgBES4Y", 0, 12, "en"),
    "norussian": ("G7vBol8wud0", 89, 101, "en"),
    "japones": ("x7vvJm9jRVU", 8, 16, "ja"),
    "jackson07": ("jB-n_8zq9Qo", 50, 64, "en"),
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
