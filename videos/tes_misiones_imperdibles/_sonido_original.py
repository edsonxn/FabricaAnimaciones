# -*- coding: utf-8 -*-
"""Sonido original (regla del 26-oct-2026) en los beats de guion.SECUENCIA["ambiente_por"], 27-oct:
    python _sonido_original.py creditos   devuelve título y canal reales a fuentes.json (`bajar --url` los deja «fijado a mano»)
    python _sonido_original.py habla      Whisper sobre cada clip con audio: ¿habla alguien encima (narrador, streamer)?
    python _sonido_original.py nivel      sonoridad de cada clip (los mudos o casi no aportan: quitarlos de ambiente_por)
Los clips se rebajaron con el MISMO video y segundo que ya estaban aprobados (`bajar N --url ... --desde ...`).
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion  # noqa: E402

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
IDS = [k for k, v in guion.SECUENCIA["ambiente_por"].items() if v > 0]


def creditos():
    fu = json.load(open("fuentes.json", encoding="utf-8"))
    for k in IDS:
        e = fu[k]
        if e.get("titulo") != "(fijado a mano)":
            continue
        r = subprocess.run(["yt-dlp", "--skip-download", "--no-warnings", "--print", "%(title)s|%(uploader)s",
                            f"https://youtu.be/{e['video']}"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        t, c = (r.stdout.strip().split("|", 1) + [""])[:2]
        if t:
            e["titulo"], e["canal"] = t, c
            print(k, t, "|", c)
    json.dump(fu, open("fuentes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _wav(k):
    w = os.path.join("audio", f"_so_{k}.wav")
    subprocess.run([FF, "-y", "-v", "error", "-i", os.path.join("medios", k + ".mp4"), "-vn", "-ac", "1", "-ar", "16000", w], check=True)
    return w


def habla():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cuda", compute_type="float16")
    for k in IDS:
        w = _wav(k)
        segs, info = m.transcribe(w, vad_filter=True)
        txt = " ".join(s.text.strip() for s in segs)
        print(f"{k} [{info.language} {info.language_probability:.2f}] {txt[:160] or '(sin habla)'}", flush=True)
        os.remove(w)


def nivel():
    import pyloudnorm as pyln
    import soundfile as sf
    for k in IDS:
        w = _wav(k)
        x, sr = sf.read(w)
        print(f"{k} {pyln.Meter(sr).integrated_loudness(x):6.1f} LUFS")
        os.remove(w)


def _cuadros_pts(ruta, w=96, h=54):
    """Cuadros pequeños (gris) y su tiempo, en la misma referencia que el audio decodificado sin -ss."""
    import re
    import numpy as np
    p = subprocess.run([FF, "-v", "info", "-i", ruta, "-map", "0:v", "-vf", f"scale={w}:{h},format=gray,showinfo", "-f", "rawvideo",
                        "-pix_fmt", "gray", "pipe:"], capture_output=True)
    ts = [float(m) for m in re.findall(rb"pts_time:\s*([-\d.]+)", p.stderr)]
    fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)
    n = min(len(ts), len(fr))
    return fr[:n], np.array(ts[:n])


def alinear(ids, aprobados):
    """El audio original SIN tocar la imagen aprobada: baja el tramo con audio y margen, busca por imagen dónde empieza el clip
    aprobado y le pega el audio de ese instante (`bajar --url` con audio cambia el keyframe y la imagen, 27-oct-2026)."""
    import shutil
    import numpy as np
    fu = json.load(open("fuentes.json", encoding="utf-8"))
    tmp = os.path.join("audio", "_alinear")
    for k in ids:
        os.makedirs(tmp, exist_ok=True)
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        ap = os.path.join(aprobados, k + ".mp4")
        e = fu[k]
        a, b = max(0.0, e["desde"] - 6), e["desde"] + 20
        subprocess.run(["yt-dlp", f"https://www.youtube.com/watch?v={e['video']}", "-f",
                        "bv*[height<=1080][height>=720][vcodec^=avc1]+ba/bv*[height<=1080][height>=720]+ba",
                        "--download-sections", f"*{a:.1f}-{b:.1f}", "-o", os.path.join(tmp, "c.%(ext)s"), "--no-warnings",
                        "--quiet", "--no-playlist"], check=True)
        crudo = os.path.join(tmp, next(f for f in os.listdir(tmp) if f.startswith("c.")))
        fa, _ = _cuadros_pts(ap)
        fb, tb = _cuadros_pts(crudo)
        ta = np.arange(len(fa)) / 30.0
        idx = list(range(0, len(fa), 10))
        mejor = (1e9, 0.0)
        for j in range(len(fb)):
            t0 = tb[j]
            kk = np.searchsorted(tb, t0 + ta[idx])
            if kk[-1] >= len(fb):
                break
            d = float(np.mean([np.abs(fa[i] - fb[q]).mean() for i, q in zip(idx, kk)]))
            mejor = min(mejor, (d, t0))
        dif, t0 = mejor
        L = len(fa) / 30.0
        wav = os.path.join(tmp, "a.wav")
        subprocess.run([FF, "-y", "-v", "error", "-i", crudo, "-map", "0:a", "-af", "aresample=async=1:first_pts=0", "-ac", "2",
                        "-ar", "48000", wav], check=True)
        nuevo = os.path.join("medios", k + "_so.mp4")
        subprocess.run([FF, "-y", "-v", "error", "-i", ap, "-ss", f"{t0:.3f}", "-i", wav, "-t", f"{L:.3f}", "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", nuevo], check=True)
        ok = dif < 8
        print(f"{k}: inicio {t0:.2f} s del tramo · diferencia {dif:.1f} {'OK' if ok else '✗ NO CUADRA: se queda mudo'}", flush=True)
        if ok:
            os.replace(nuevo, os.path.join("medios", k + ".mp4"))
        else:
            os.remove(nuevo)
            shutil.copy(ap, os.path.join("medios", k + ".mp4"))
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "alinear":    # python _sonido_original.py alinear <carpeta con los aprobados> [scene-014 ...]
        alinear(sys.argv[3:] or IDS, sys.argv[2])
    else:
        {"creditos": creditos, "habla": habla, "nivel": nivel}[sys.argv[1]]()
