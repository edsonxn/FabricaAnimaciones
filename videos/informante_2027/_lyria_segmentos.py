# -*- coding: utf-8 -*-
"""Música con Lyria en TRAMOS (Lyria devuelve ~3 min como máximo por pieza). Cada tramo cubre un grupo de escenas con su propio arco;
se unen con fundido cruzado en los límites de escena y se guardan en audio/musica.wav (float32, 48 kHz, estéreo, duración exacta).
Prompt neutro (el filtro de entrada de Lyria rechaza palabras sensibles) y reintentos.   python _lyria_segmentos.py [generar|armar|todo]"""
import json
import os
import subprocess
import sys
import time
import urllib.error

import numpy as np
import soundfile as sf

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import lyria  # noqa: E402

TL = json.load(open("timeline.json", encoding="utf-8"))
ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
ORDEN = [e["id"] for e in TL["escenas"]]
SEC = {
    "gancho": ("Opening in the rain: a lonely muted trumpet over upright bass and soft brushes, a suspended chord, quiet suspense; a cold synthetic shimmer creeps in at the end.", 4),
    "cliente": ("Curious investigation: walking upright bass, brushes, a wry muted trumpet phrase, light and inquisitive.", 4),
    "profecia": ("A ticking pulse and low piano motif, something foreseen: glassy electronic tones under noir bass, a slow rise.", 5),
    "renuncia": ("Sparse and resolute: solo piano with low strings, a man walking away, restrained.", 4),
    "precio": ("Weighing a decision: slow dark waltz feel, low strings, a heavy accent near the end, then quiet.", 6),
    "escandalo": ("Newsroom energy: brisk brushed drums, walking bass, staccato low brass accents, rising tension.", 6),
    "expediente": ("Typewriter-like ticking rhythm, low string ostinato begins, mysterious and methodical.", 5),
    "agentes": ("Mechanical curiosity: pizzicato and soft electronic pulses, slowly accelerating pattern.", 5),
    "robo": ("Night heist: tense low pulse, hushed, then a driving string ostinato like a chase.", 7),
    "ejercito": ("Vast and cold: wide synthetic pads and a relentless pulse multiplying, awe and unease.", 7),
    "afuera": ("Street level in the rain: lonely muted trumpet, distant crowd-like texture, uneasy calm.", 4),
    "mentira": ("Creeping dread: sustained dissonant strings, a too-perfect celesta motif, something wrong underneath, slow build.", 7),
    "filtracion": ("Urgent newsroom pulse returning, low brass, tension tightening toward a decision.", 7),
    "voto": ("Held breath: ticking clock, a single low piano note repeating, suspended harmony, strong accent at the end.", 8),
    "carrera": ("Relentless driving ostinato growing colder and bigger, then the texture empties out into a bleak, almost silent drone.", 9),
    "freno": ("A cautious dawn: warmer strings and piano, relief that never fully resolves, a dark undertone at the end.", 5),
    "dudas": ("Skeptical and dry: walking bass, brushes, a questioning muted trumpet line.", 4),
    "marcador": ("Methodical counting pulse, piano and pizzicato, steady forward motion, slightly hopeful.", 5),
    "plan": ("Resolve and warning: steady determined pulse, piano and strings gaining clarity, an hourglass-like ticking.", 6),
    "cierre": ("A slow solitary muted trumpet and piano theme in the rain, haunting and existential, fading out to silence.", 3),
}
TRAMOS = [
    (["gancho", "cliente", "profecia", "renuncia", "precio"], "Begin from near silence with rain-like texture. End on a sustained low tone that can flow into the next piece. No loud ending."),
    (["escandalo", "expediente", "agentes", "robo", "ejercito"], "Begin with a held low tone. Steady growth in tension. End on a sustained low tone, no loud ending."),
    (["afuera", "mentira", "filtracion", "voto"], "Begin quietly with a held low tone. Slow build to a tense peak at the very end, ending on a sustained low tone."),
    (["carrera", "freno", "dudas"], "Begin with a held low pulse. The first section is the darkest and biggest of the whole score, then it empties out. End on a sustained low tone, no loud ending."),
    (["marcador", "plan", "cierre"], "Begin with a held low pulse. Gain clarity and firmness, then calm down and end with a slow fade-out to silence."),
]


def limites(ids):
    t0 = ESC[ids[0]]["t0"]
    i = ORDEN.index(ids[-1])
    t1 = ESC[ORDEN[i + 1]]["t0"] if i + 1 < len(ORDEN) else TOTAL
    return t0, t1


def prompt_tramo(ids, nota):
    t0, t1 = limites(ids)
    dur = t1 - t0
    l = [f"Cinematic film noir score: smoky 1940s noir jazz (muted trumpet, upright bass, brushed drums, lonely piano) blended with modern "
         f"cinematic tension (low string ostinatos, deep sub pulses, ticking). Never cheerful. Total length: exactly {lyria.mmss(dur)} "
         f"({int(round(dur))} seconds). Instrumental only, no vocals, no singing, no spoken words. It must leave room for a narrator: keep the middle frequencies "
         f"calm, no lead melody competing with speech. {nota}", ""]
    for k, i in enumerate(ids):
        e = ESC[i]
        s = e["t0"] - t0
        j = ORDEN.index(i)
        f = (ESC[ORDEN[j + 1]]["t0"] if j + 1 < len(ORDEN) else TOTAL) - t0
        d, inten = SEC[i]
        l.append(f"[{lyria.mmss(s)} - {lyria.mmss(f)}] Section {k + 1}: Intensity {inten}/10. {d}")
    return "\n".join(l)


def generar():
    os.makedirs("audio", exist_ok=True)
    for n, (ids, nota) in enumerate(TRAMOS, 1):
        ruta = f"audio/lyria_tramo{n}.mp3"
        if os.path.exists(ruta) and os.path.getsize(ruta) > 100000:
            print("ya existe", ruta)
            continue
        texto = prompt_tramo(ids, nota)
        open(f"audio/prompt_tramo{n}.txt", "w", encoding="utf-8").write(texto)
        for intento in range(1, 9):
            t = time.time()
            try:
                datos, mime, _ = lyria.generar(texto)
            except urllib.error.HTTPError as e:
                print(f"tramo {n} intento {intento}: HTTP {e.code} {e.read()[:100]}; reintento", flush=True)
                time.sleep(3)
                continue
            open(ruta, "wb").write(datos)
            d = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout.strip()
            lim = limites(ids)
            print(f"tramo {n}: {ruta} {float(d):.1f} s (pedido {lim[1] - lim[0]:.1f} s; {time.time() - t:.0f} s de generación, intento {intento})", flush=True)
            break
        else:
            print(f"tramo {n}: sin éxito")


def cargar(n, objetivo):
    """Convierte el tramo a wav float32 48 kHz estéreo y lo ajusta a `objetivo` s (alarga hasta un 12 % sin cambiar el tono; si sobra, recorta)."""
    ruta = f"audio/lyria_tramo{n}.mp3"
    wav = f"audio/_t{n}.wav"
    d = float(subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout.strip())
    r = d / objetivo
    filtro = []
    if 0.88 <= r < 0.995:
        filtro = ["-filter:a", f"atempo={r:.5f}"]
    elif 1.005 < r <= 1.12:
        filtro = ["-filter:a", f"atempo={r:.5f}"]          # acelera un poco para que quepa sin cortar el final
    subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-i", ruta, *filtro, "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", wav], check=True)
    x, sr = sf.read(wav, always_2d=True)
    os.remove(wav)
    n_obj = int(round(objetivo * sr))
    if len(x) < n_obj:
        x = np.vstack([x, np.zeros((n_obj - len(x), 2))])
    return x[:n_obj].astype(np.float32), sr, d


def armar(cruce=3.0):
    sr = 48000
    out = np.zeros((int(round(TOTAL * sr)), 2), np.float32)
    for n, (ids, _) in enumerate(TRAMOS, 1):
        t0, t1 = limites(ids)
        x, sr, d = cargar(n, (t1 - t0) + cruce)               # cada tramo se extiende `cruce` s sobre el siguiente
        i0 = int(round(t0 * sr))
        seg = x[:min(len(x), len(out) - i0)].copy()
        nf = int(cruce * sr)
        if n > 1:                                             # entrada con fundido (potencia constante)
            seg[:nf] *= np.sin(np.linspace(0, np.pi / 2, nf))[:, None]
        if n < len(TRAMOS):                                   # salida con fundido
            seg[-nf:] *= np.cos(np.linspace(0, np.pi / 2, nf))[:, None]
        out[i0:i0 + len(seg)] += seg
        print(f"tramo {n}: {t0:.1f}-{t1:.1f} s (original {d:.1f} s)")
    fi, fo = int(0.6 * sr), int(3.0 * sr)
    out[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.5
    out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    sf.write("audio/musica.wav", out, sr, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / sr:.2f} s)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if modo in ("generar", "todo"):
        generar()
    if modo in ("armar", "todo"):
        armar()
