# -*- coding: utf-8 -*-
"""Música con Lyria ADAPTADA AL GUION, en TRAMOS (Lyria devuelve ~3 min como máximo por pieza), para videos de más de 3 minutos.
Generaliza `videos/christa_pike/_lyria_segmentos.py`. Lee `timeline.json` y el diccionario `LYRIA` de guion.py:
    LYRIA = dict(
        estilo="Warm curious documentary score: pizzicato strings, marimba, ...",      # solo descripción musical, en inglés
        escenas={"gancho": ("descripción musical de esa escena", intensidad 1-10), ...}, # una por id de ESCENAS
        tramos=[(["gancho", "promesa"], "Begin from silence. End on a held soft tone..."), ...],  # grupos de escenas seguidas, <= ~170 s
    )
Cada tramo se pide con los tiempos reales de sus escenas, se ajusta con `atempo` (hasta ±12 %) y se une con fundido cruzado de 3 s en
`audio/musica.wav` (float32, 48 kHz, estéreo, duración exacta), que es lo que espera `mezcla`. NO correr `musica` (procedural) después.
El filtro de entrada de Lyria rechaza palabras sensibles y nombres propios: el prompt va neutro («Section k», solo música) y con reintentos.

Uso (desde la carpeta del video):   python ../../nucleo/lyria_tramos.py [generar|armar|todo|prompt]
Los mp3 de cada tramo quedan en audio/lyria_tramoN.mp3; para rehacer uno, bórralo y vuelve a correr.
"""
import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.error

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lyria  # noqa: E402

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"C:\ffmpeg\bin\ffprobe.exe"
MAX_TRAMO = 175.0


def cargar_cfg():
    spec = importlib.util.spec_from_file_location("guion", os.path.join(os.getcwd(), "guion.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    cfg = getattr(g, "LYRIA", None)
    if not cfg or not cfg.get("tramos"):
        sys.exit("guion.py necesita LYRIA = dict(estilo=..., escenas={...}, tramos=[([ids], nota), ...])")
    return cfg


TL = json.load(open("timeline.json", encoding="utf-8"))
ESC = {e["id"]: e for e in TL["escenas"]}
ORDEN = [e["id"] for e in TL["escenas"]]
TOTAL = TL["total"]
CFG = cargar_cfg()
TRAMOS = CFG["tramos"]


def fin(i):
    j = ORDEN.index(i)
    return ESC[ORDEN[j + 1]]["t0"] if j + 1 < len(ORDEN) else TOTAL


def limites(ids):
    return ESC[ids[0]]["t0"], fin(ids[-1])


def comprobar():
    usados = [i for ids, _ in TRAMOS for i in ids]
    if usados != ORDEN:
        sys.exit(f"LYRIA['tramos'] debe cubrir todas las escenas en orden.\n  guion: {ORDEN}\n  tramos: {usados}")
    for ids, _ in TRAMOS:
        t0, t1 = limites(ids)
        if t1 - t0 > MAX_TRAMO:
            sys.exit(f"tramo {ids[0]}..{ids[-1]} dura {t1 - t0:.0f} s (> {MAX_TRAMO:.0f} s): pártelo en dos")


def prompt_tramo(ids, nota):
    t0, t1 = limites(ids)
    dur = t1 - t0
    l = [f"{CFG['estilo']} Total length: exactly {lyria.mmss(dur)} ({int(round(dur))} seconds). Instrumental only, no vocals, no singing, "
         f"no spoken words. It must leave room for a narrator: keep the middle frequencies calm, no lead melody competing with speech. {nota}", ""]
    for k, i in enumerate(ids):
        d, inten = CFG.get("escenas", {}).get(i, ("the underscore continues in the same mood", 4))
        l.append(f"[{lyria.mmss(ESC[i]['t0'] - t0)} - {lyria.mmss(fin(i) - t0)}] Section {k + 1}: Intensity {inten}/10. {d}")
    return "\n".join(l)


def duracion(ruta):
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                                capture_output=True, text=True).stdout.strip())


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
            t0, t1 = limites(ids)
            print(f"tramo {n}: {ruta} {duracion(ruta):.1f} s (pedido {t1 - t0:.1f} s; {time.time() - t:.0f} s de generación, intento {intento})", flush=True)
            break
        else:
            sys.exit(f"tramo {n}: sin éxito tras 8 intentos (revisar palabras del prompt en audio/prompt_tramo{n}.txt)")


def recortar_silencios(ruta, inicio, fin):
    """Quita el silencio del inicio y/o del final de un tramo (Lyria suele dejar 2-3 s): en una unión los dos silencios
    seguidos más el fundido hacían un hueco audible (arana_techo, 11-oct-2026). Devuelve un wav temporal o la ruta tal cual."""
    if not (inicio or fin):
        return ruta
    quita = "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.1:detection=rms"
    f = [quita] if inicio else []
    if fin:
        f += ["areverse", quita, "areverse"]
    sal = ruta.rsplit(".", 1)[0] + "_sin_silencio.wav"
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", ruta, "-af", ",".join(f), "-c:a", "pcm_f32le", sal], check=True)
    return sal


def cargar(n, objetivo):
    """Tramo a float32 48 kHz estéreo ajustado a `objetivo` s (atempo hasta ±12 %; si aún falta, silencio; si sobra, recorte).
    Antes quita el silencio de las uniones: el inicio de los tramos 2..N y el final de los tramos 1..N-1."""
    ruta, wav = f"audio/lyria_tramo{n}.mp3", f"audio/_t{n}.wav"
    ruta = recortar_silencios(ruta, inicio=n > 1, fin=n < len(TRAMOS))
    d = duracion(ruta)
    r = d / objetivo
    filtro = ["-filter:a", f"atempo={r:.5f}"] if (0.88 <= r < 0.995 or 1.005 < r <= 1.12) else []
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", ruta, *filtro, "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", wav], check=True)
    x, sr = sf.read(wav, always_2d=True)
    os.remove(wav)
    if ruta.endswith("_sin_silencio.wav"):
        os.remove(ruta)
    n_obj = int(round(objetivo * sr))
    if len(x) < n_obj:
        x = np.vstack([x, np.zeros((n_obj - len(x), 2))])
    return x[:n_obj].astype(np.float32), sr, d


def armar(cruce=3.0):
    sr = 48000
    out = np.zeros((int(round(TOTAL * sr)), 2), np.float32)
    nf = int(cruce * sr)
    for n, (ids, _) in enumerate(TRAMOS, 1):
        t0, t1 = limites(ids)
        x, sr, d = cargar(n, (t1 - t0) + cruce)               # cada tramo se extiende `cruce` s sobre el siguiente
        i0 = int(round(t0 * sr))
        seg = x[:min(len(x), len(out) - i0)].copy()
        if n > 1:                                             # entrada con fundido (potencia constante)
            seg[:nf] *= np.sin(np.linspace(0, np.pi / 2, nf))[:, None]
        if n < len(TRAMOS):                                   # salida con fundido
            seg[-nf:] *= np.cos(np.linspace(0, np.pi / 2, nf))[:, None]
        out[i0:i0 + len(seg)] += seg
        aviso = "" if 0.88 <= d / ((t1 - t0) + cruce) <= 1.12 else "  ¡OJO: fuera de ±12 %, queda silencio o recorte!"
        print(f"tramo {n}: {t0:.1f}-{t1:.1f} s (original {d:.1f} s){aviso}")
    fi, fo = int(0.6 * sr), int(3.0 * sr)
    out[:fi] *= np.linspace(0, 1, fi)[:, None] ** 1.5
    out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    sf.write("audio/musica.wav", out, sr, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / sr:.2f} s)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    comprobar()
    modo = sys.argv[1] if len(sys.argv) > 1 else "todo"
    if modo == "prompt":
        for ids, nota in TRAMOS:
            print(prompt_tramo(ids, nota), "\n" + "-" * 60)
    if modo in ("generar", "todo"):
        generar()
    if modo in ("armar", "todo"):
        armar()
