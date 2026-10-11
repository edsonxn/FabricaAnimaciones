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
    "gancho": ("Opening: a sparse low drone, a slow heartbeat-like pulse, thin high string harmonics slowly rising, a held swell and a sudden silence at the end.", 4),
    "quien": ("Quiet and bleak: solitary felt piano, soft low strings, cold air.", 3),
    "colleen": ("Tender and sad: a gentle piano motif alone, warm sustained strings. Very soft.", 2),
    "crimen": ("Dark and tense but restrained: low pulsing bass, long dissonant strings, no melody, a heavy hit at the end.", 5),
    "juicio": ("Cold and procedural: steady low pulse, sparse piano notes like a ticking clock, sober.", 4),
    "corredor": ("Isolation and passing years: slow ambient drone, distant metallic textures, a single piano note echoing, bleak and still.", 3),
    "debate": ("Two alternating low string phrases in conversation, unresolved, serious, building slightly.", 4),
    "camino": ("Countdown tension: a quickening quiet pulse, ticking, rising strings, inevitability.", 6),
    "noche": ("Peak tension, restrained: very slow bass pulse, long cold string clusters rising, silences, a final unresolved cluster. No release.", 8),
    "despues": ("Aftermath: empty and stunned, soft low drone, sparse piano, slow and unsettled.", 5),
    "historial": ("Institutional unease: slow low strings, a ticking clock, sparse piano, cold and procedural.", 4),
    "precedente": ("Reflective: old-world solemn strings, slow piano, a feeling of history repeating.", 4),
    "cierre": ("Ethereal pads and a slow solitary piano, the question remains open, quiet, one final note, fades to silence.", 3),
}
TRAMOS = [
    (["gancho", "quien", "colleen", "crimen", "juicio", "corredor"], "Begin from silence. End on a sparse sustained low tone that can flow into the next piece. No loud ending."),
    (["debate", "camino", "noche"], "Begin with a held low tone. The tension grows steadily across the whole piece and peaks in the last section, then stops on an unresolved sustained note."),
    (["despues", "historial", "precedente", "cierre"], "Begin with a held low tone, calm and sorrowful. End with a natural slow fade-out to silence."),
]


def limites(ids):
    t0 = ESC[ids[0]]["t0"]
    i = ORDEN.index(ids[-1])
    t1 = ESC[ORDEN[i + 1]]["t0"] if i + 1 < len(ORDEN) else TOTAL
    return t0, t1


def prompt_tramo(ids, nota):
    t0, t1 = limites(ids)
    dur = t1 - t0
    l = [f"Somber cinematic documentary score: slow low strings, sparse felt piano, a deep soft sub-bass pulse, distant ambient textures, subtle ticking clock, "
         f"occasional soft impacts. No drum kit, no big orchestral melody, never triumphant, never sentimental. Total length: exactly {lyria.mmss(dur)} "
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
