# -*- coding: utf-8 -*-
"""Música de fondo con Lyria (Google AI Studio), estructurada por las escenas del guion.

Lee `timeline.json` (tiempos reales de cada escena) y el diccionario opcional `LYRIA` de guion.py:
    LYRIA = dict(estilo="dark cinematic mystery documentary score ...",
                 escenas={"gancho": ("descripción musical", intensidad 1-10), ...})
Genera `audio/lyria_<k>.mp3` (uno o varios candidatos) y con `--usar k` los convierte a `audio/musica.wav` (float32, 48 kHz, estéreo, duración
exacta del video, entrada y salida suaves), que es lo que espera `mezcla`. La clave se lee de canales/tokens/google_ai_studio.txt (no se imprime).

Uso (desde la carpeta del video):
    python lyria.py --n 2                 genera 2 candidatos con lyria-3.5
    python lyria.py --usar 1              convierte el candidato 1 a audio/musica.wav
    python lyria.py --prompt              solo muestra el prompt
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

import numpy as np

CLAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "canales", "tokens", "google_ai_studio.txt")
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"


def clave():
    return open(CLAVE, encoding="utf-8").read().strip().split()[-1]


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def prompt(TL, cfg):
    estilo = cfg.get("estilo", "Dark cinematic mystery documentary score, instrumental only, no vocals, no lyrics.")
    total = TL["total"]
    lineas = [f"{estilo} Total length: exactly {mmss(total)} ({int(round(total))} seconds). Instrumental only, no vocals, no singing, no spoken words. "
              "It must leave room for a narrator: keep the middle frequencies calm, no lead melody competing with speech. End with a natural fade-out.", ""]
    esc = TL["escenas"]
    for k, e in enumerate(esc):
        desc, inten = cfg.get("escenas", {}).get(e["id"], ("underscore continues, tense and mysterious", 4))
        t0 = e["t0"]
        t1 = esc[k + 1]["t0"] if k + 1 < len(esc) else total
        lineas.append(f"[{mmss(t0)} - {mmss(t1)}] {e['id'].capitalize()}: Intensity {inten}/10. {desc}")
    return "\n".join(lineas)


def generar(texto, modelo="lyria-3.5"):
    cuerpo = {"model": modelo, "input": texto}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions", data=json.dumps(cuerpo).encode(),
                                 headers={"x-goog-api-key": clave(), "Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())

    def buscar(o):
        if isinstance(o, dict):
            for kk, v in o.items():
                if kk == "data" and isinstance(v, str) and len(v) > 1000:
                    return v, o.get("mime_type") or o.get("mimeType") or ""
                x = buscar(v)
                if x:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = buscar(v)
                if x:
                    return x
    b = buscar(r)
    if not b:
        raise RuntimeError("Lyria no devolvió audio: " + json.dumps(r)[:500])
    letra = ""
    try:
        for s in r.get("steps", []):
            for c in s.get("content", []) or []:
                if c.get("type") == "text":
                    letra += c.get("text", "")
    except Exception:
        pass
    return base64.b64decode(b[0]), b[1], letra


def a_wav(entrada, salida, total, fade_in=0.6, fade_out=3.0, estirar=True):
    """Convierte a float32 48 kHz estéreo, recorta/rellena a `total` s y aplica entrada/salida suaves.
    Si el candidato es más corto que el video (Lyria suele dar ~3:00), lo alarga sin cambiar el tono (ffmpeg atempo) hasta un 12 %."""
    tmp = salida + ".tmp.wav"
    filtro = []
    if estirar:
        d = float(subprocess.run([FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", entrada],
                                 capture_output=True, text=True).stdout.strip())
        r = d / total
        if 0.88 <= r < 0.995:
            filtro = ["-filter:a", f"atempo={r:.5f}"]
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", entrada, *filtro, "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", tmp], check=True)
    import soundfile as sf
    x, sr = sf.read(tmp, always_2d=True)
    n = int(round(total * sr))
    if len(x) < n:                                   # más corto: silencio al final (la cola natural ya decae)
        x = np.vstack([x, np.zeros((n - len(x), x.shape[1]))])
    x = x[:n].copy()
    fi, fo = int(fade_in * sr), int(fade_out * sr)
    x[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.5
    x[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    sf.write(salida, x.astype(np.float32), sr, subtype="FLOAT")
    os.remove(tmp)
    return len(x) / sr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--modelo", default="lyria-3.5")
    ap.add_argument("--usar", type=int, default=None)
    ap.add_argument("--prompt", action="store_true")
    a = ap.parse_args()
    TL = json.load(open("timeline.json", encoding="utf-8"))
    import config
    cfg = getattr(config._g, "LYRIA", {}) if hasattr(config, "_g") else {}
    os.makedirs("audio", exist_ok=True)
    if a.usar is not None:
        d = a_wav(f"audio/lyria_{a.usar}.mp3", "audio/musica.wav", TL["total"])
        print(f"audio/musica.wav listo ({d:.2f} s) desde lyria_{a.usar}.mp3")
        return
    texto = prompt(TL, cfg)
    print(texto)
    if a.prompt:
        return
    for k in range(1, a.n + 1):
        t = time.time()
        datos, mime, letra = generar(texto, a.modelo)
        ext = ".mp3" if "mpeg" in mime or "mp3" in mime else ".wav"
        ruta = f"audio/lyria_{k}{ext}"
        open(ruta, "wb").write(datos)
        # duración real
        d = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout.strip()
        print(f"candidato {k}: {ruta}  {float(d):.1f} s  ({time.time() - t:.0f} s de generación)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
