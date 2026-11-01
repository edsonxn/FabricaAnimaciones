# -*- coding: utf-8 -*-
"""Música con Lyria ADAPTADA AL GUION, en TRAMOS (Lyria devuelve ~3 min como máximo por pieza), para videos de más de 3 minutos.
Generaliza `videos/christa_pike/_lyria_segmentos.py`. Lee `timeline.json` y el diccionario `LYRIA` de guion.py:
    LYRIA = dict(
        estilo="Warm curious documentary score: pizzicato strings, marimba, ...",      # solo descripción musical, en inglés
        escenas={"gancho": ("descripción musical de esa escena", intensidad 1-10), ...}, # una por id de ESCENAS
        tramos=[(["gancho", "promesa"], "Begin from silence. End on a held soft tone..."), ...],  # grupos de escenas seguidas, <= ~170 s
        reemplazos={"overgear": dict(archivo=r"medios/_overgear/musica_promo.mp3", desde=0, db=0)},  # opcional: otra música en esa escena
    )
Cada tramo se pide con los tiempos reales de sus escenas, se ajusta con `atempo` (hasta ±12 %) y se une con fundido cruzado de 3 s en
`audio/musica.wav` (float32, 48 kHz, estéreo, duración exacta), que es lo que espera `mezcla`. NO correr `musica` (procedural) después.
El filtro de entrada de Lyria rechaza palabras sensibles y nombres propios: el prompt va neutro («Section k», solo música) y con reintentos.

Uso (desde la carpeta del video):   python ../../nucleo/lyria_tramos.py [generar|armar|todo|prompt|manual]
Los mp3 de cada tramo quedan en audio/lyria_tramoN.mp3; para rehacer uno, bórralo y vuelve a correr.

SIN SALDO EN LA API (HTTP 402, 14-oct-2026) o a propósito (`manual`): la música se genera A MANO en Google AI Studio
(aistudio.google.com, generador de música Lyria: deja crear algunas piezas gratis sin API). Se escribe la hoja
audio/PROMPTS_AI_STUDIO.md con el prompt de cada tramo; cada pieza bajada se guarda como audio/lyria_tramoN.<mp3|wav|m4a|ogg>
y `armar` (o `fab.py <v> musica`) la usa igual que la de la API. Si falta algún tramo, `armar` deja silencio ahí y avisa
(sirve para la vista previa con solo los primeros tramos).
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
    mudo = not any(e["frases"] for e in TL["escenas"])       # SIN_VOZ: la música lleva el montaje, la melodía puede mandar
    hueco = ("There is no narrator: the music carries the film, with a clear lead melody." if mudo else
             "It must leave room for a narrator: keep the middle frequencies calm, no lead melody competing with speech.")
    l = [f"{CFG['estilo']} Total length: exactly {lyria.mmss(dur)} ({int(round(dur))} seconds). Instrumental only, no vocals, no singing, "
         f"no spoken words. {hueco} {nota}", ""]
    for k, i in enumerate(ids):
        d, inten = CFG.get("escenas", {}).get(i, ("the underscore continues in the same mood", 4))
        l.append(f"[{lyria.mmss(ESC[i]['t0'] - t0)} - {lyria.mmss(fin(i) - t0)}] Section {k + 1}: Intensity {inten}/10. {d}")
    return "\n".join(l)


def duracion(ruta):
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                                capture_output=True, text=True).stdout.strip())


EXTS = ("mp3", "wav", "m4a", "ogg", "flac")


def ruta_tramo(n):
    """La pieza del tramo n: la de la API (audio/lyria_tramoN.mp3) o la bajada a mano de Google AI Studio (cualquier formato)."""
    for e in EXTS:
        r = f"audio/lyria_tramo{n}.{e}"
        if os.path.exists(r) and os.path.getsize(r) > 50000:
            return r
    return None


def hoja_manual():
    """Hoja para generar a mano en Google AI Studio los tramos -> audio/PROMPTS_AI_STUDIO.md."""
    os.makedirs("audio", exist_ok=True)
    l = [f"# Música Lyria a mano en Google AI Studio — {os.path.basename(os.getcwd())}", "",
         "1. aistudio.google.com → generador de música (Lyria). Pega el prompt de cada tramo tal cual (en inglés).",
         "2. Pide la duración indicada (o la más cercana): `armar` la ajusta hasta ±12 %; si queda corta, silencio al final.",
         "3. Baja la pieza y guárdala en `audio/` con el nombre indicado (mp3, wav, m4a u ogg).",
         "4. Avisa a Claude (o corre `python fab.py <video> musica`): arma `audio/musica.wav` con fundidos de 3 s.", ""]
    for n, (ids, nota) in enumerate(TRAMOS, 1):
        t0, t1 = limites(ids)
        hecho = ruta_tramo(n)
        l.append(f"## Tramo {n} — {lyria.mmss(t0)} a {lyria.mmss(t1)} del video ({int(round(t1 - t0))} s) · "
                 f"{', '.join(ids)}" + (f" · YA ESTÁ ({hecho})" if hecho else ""))
        l += ["", f"Guardar como: `audio/lyria_tramo{n}.mp3` (o .wav)", "", "```", prompt_tramo(ids, nota), "```", ""]
    open("audio/PROMPTS_AI_STUDIO.md", "w", encoding="utf-8").write(chr(10).join(l))
    return "audio/PROMPTS_AI_STUDIO.md"


def generar():
    os.makedirs("audio", exist_ok=True)
    for n, (ids, nota) in enumerate(TRAMOS, 1):
        ruta = f"audio/lyria_tramo{n}.mp3"
        if ruta_tramo(n):
            print("ya existe", ruta_tramo(n))
            continue
        texto = prompt_tramo(ids, nota)
        open(f"audio/prompt_tramo{n}.txt", "w", encoding="utf-8").write(texto)
        for intento in range(1, 9):
            t = time.time()
            try:
                datos, mime, _ = lyria.generar(texto)
            except urllib.error.HTTPError as e:
                if e.code == 402:                             # sin saldo prepagado: no sirve reintentar
                    hoja = hoja_manual()
                    sys.exit(f"Lyria por API sin saldo (HTTP 402). Genera la música A MANO en Google AI Studio con {hoja} y "
                             f"guarda cada pieza como audio/lyria_tramoN.mp3 (o .wav); luego `armar` (fab.py <v> musica).")
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
    ruta, wav = ruta_tramo(n), f"audio/_t{n}.wav"
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


def reemplazar(out, sr, esc, rep):
    """Durante la escena `esc` suena otra música (p. ej. la del patrocinio): rep = dict(archivo=ruta, desde=s, db=0, cruce=1.5).
    Se iguala al RMS que tenía la Lyria en ese tramo (+db) para que la mezcla y el ducking no cambien, se repite si es corta, y
    entra/sale con fundido cruzado de potencia constante centrado en los bordes de la escena."""
    t0, t1 = ESC[esc]["t0"], fin(esc)
    cr = float(rep.get("cruce", 1.5))
    a, b = int(round(max(0.0, t0 - cr / 2) * sr)), int(round(min(TOTAL, t1 + cr / 2) * sr))
    wav = "audio/_reemplazo.wav"
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(rep.get("desde", 0)), "-i", rep["archivo"], "-ar", str(sr), "-ac", "2",
                    "-c:a", "pcm_f32le", wav], check=True)
    x, _ = sf.read(wav, always_2d=True)
    os.remove(wav)
    x = np.tile(x, (int(np.ceil((b - a) / len(x))), 1))[:b - a].astype(np.float32)
    rms = lambda y: float(np.sqrt(np.mean(y.astype(np.float64) ** 2)) + 1e-9)   # noqa: E731
    x *= rms(out[a:b]) / rms(x) * 10 ** (rep.get("db", 0.0) / 20)
    nf = int(cr * sr)
    g = np.ones(b - a, np.float32)                       # ganancia de la música nueva; la Lyria recibe la complementaria
    g[:nf] = np.sin(np.linspace(0, np.pi / 2, nf))
    g[-nf:] = np.cos(np.linspace(0, np.pi / 2, nf))
    out[a:b] = out[a:b] * np.sqrt(1 - g ** 2)[:, None] + x * g[:, None]
    print(f"reemplazo {esc}: {t0:.1f}-{t1:.1f} s ← {os.path.basename(rep['archivo'])} ({rep.get('db', 0.0):+.1f} dB sobre el RMS de la Lyria)")


def armar(cruce=3.0):
    sr = 48000
    out = np.zeros((int(round(TOTAL * sr)), 2), np.float32)
    nf = int(cruce * sr)
    for n, (ids, _) in enumerate(TRAMOS, 1):
        t0, t1 = limites(ids)
        if not ruta_tramo(n):                                 # aún no está (p. ej. vista previa con los primeros tramos)
            print(f"tramo {n}: {t0:.1f}-{t1:.1f} s  ¡FALTA audio/lyria_tramo{n}.*: queda en silencio!")
            continue
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
    for esc, rep in CFG.get("reemplazos", {}).items():
        reemplazar(out, sr, esc, rep)
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
    if modo == "manual":
        print("hoja para Google AI Studio:", hoja_manual())
    if modo in ("generar", "todo"):
        generar()
    if modo in ("armar", "todo"):
        armar()
