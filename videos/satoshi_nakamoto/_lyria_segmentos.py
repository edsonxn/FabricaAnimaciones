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
    "gancho": ("Opening: a low drone and a ticking clock, a glassy arpeggio slowly appears, a pulse builds, a deep hit, then a sudden stop.", 5),
    "origen": ("Urgent and modern: a driving low synth pulse, staccato cellos, news-like tension, then a quieter curious motif as something new begins.", 5),
    "genesis": ("Discovery: a mysterious digital arpeggio over a steady pulse, a soft reveal swell, secrecy and wonder.", 5),
    "fantasma": ("A ghost: sparse piano notes over a cold pad and a light pulse that slowly fades out to near silence at the end.", 4),
    "fortuna": ("Weight: deep sub bass, slow heavy pulses, something enormous and untouched, rising to a firm accent.", 5),
    "perfil": ("Analysis: a clean rhythmic pulse, ticking hi-hat, data-like arpeggios, focused and methodical, gently rising.", 5),
    "dorian": ("Media frenzy: a faster pulse, rising tension, a chase rhythm with taut strings, then an eerie twist at the end.", 6),
    "hal": ("Human and melancholic: soft felt piano over a warm pulse, a running rhythm in the middle, a tender sad close.", 4),
    "szabo": ("Puzzle: a mysterious plucked motif, curious and questioning, steady pulse.", 5),
    "wright": ("Swagger that turns sour: a confident groove, then distorted bass, courtroom gravity and a final heavy accent.", 7),
    "todd": ("Shifting theories: unsettled pulse, two alternating motifs, ghostly pads, unresolved.", 5),
    "leroux": ("Dark intrigue: low pulsing bass, tense muted strings, a cold metallic texture, restrained.", 6),
    "back": ("The last name: tension builds steadily to the peak of the whole score, relentless pulse, rising strings, no release.", 8),
    "archivo": ("Hidden files: a hushed low pulse, sparse ticks, suspense held.", 5),
    "espejo": ("Reflection: the pulse drops away, an airy pad and a soft glassy motif.", 3),
    "cierre": ("Resolution without answer: a slow solitary piano motif over a warm pad, haunting, final note and a slow fade to silence.", 3),
}
TRAMOS = [
    (["gancho", "origen", "genesis"], "Begin from silence. End on a sustained low tone that can flow into the next piece. No loud ending."),
    (["fantasma", "fortuna", "perfil"], "Begin with a held low tone. Steady forward momentum. End on a sustained tone, no loud ending."),
    (["dorian", "hal", "szabo"], "Begin with a held low tone and a pulse. Keep momentum. End on a sustained tone, no loud ending."),
    (["wright", "todd", "leroux"], "Begin with a held low tone and a groove. End on a sustained unresolved tone, no loud ending."),
    (["back", "archivo", "espejo", "cierre"], "Begin with a held low tone. Build to the strongest intensity of the score, then calm down and end with a slow fade-out to silence."),
]


def limites(ids):
    t0 = ESC[ids[0]]["t0"]
    i = ORDEN.index(ids[-1])
    t1 = ESC[ORDEN[i + 1]]["t0"] if i + 1 < len(ORDEN) else TOTAL
    return t0, t1


def prompt_tramo(ids, nota):
    t0, t1 = limites(ids)
    dur = t1 - t0
    l = [f"Modern investigative documentary score with forward momentum: a steady pulsing synth bass, ticking hi-hat, low cello ostinatos, glassy digital "
         f"arpeggios, occasional deep impacts. No big drum kit, no big orchestral melody, never cheerful, never sentimental. Total length: exactly {lyria.mmss(dur)} "
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
