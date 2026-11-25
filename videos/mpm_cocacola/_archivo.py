# -*- coding: utf-8 -*-
"""METRAJE < 720p como VENTANA DE ARCHIVO (docs/estilo_secuencia_yt.md § METRAJE DE ARCHIVO < 720p), marco naranja del canal.
    python _archivo.py          baja enteros a medios/_archivo/ y arma medios/scene-NNN.mp4 de los beats de abajo
"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
ARC = os.path.join(AQUI, "medios", "_archivo")
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
# beat: (id del video, segundo de inicio)
TRAMOS = {   # mpm_cocacola (24-nov-2026): película de 1939 (bcatrD251VA, 480p) y camiones de los 40 (7wFEz_z0XhY, 480p)
    "scene-002": ("bcatrD251VA", 285), "scene-003": ("bcatrD251VA", 294), "scene-012": ("bcatrD251VA", 303),
    "scene-013": ("bcatrD251VA", 313), "scene-016": ("bcatrD251VA", 274), "scene-017": ("bcatrD251VA", 580),
    "scene-018": ("bcatrD251VA", 592), "scene-021": ("bcatrD251VA", 878), "scene-089": ("bcatrD251VA", 669),
    "scene-090": ("bcatrD251VA", 940), "scene-014": ("bcatrD251VA", 330), "scene-015": ("bcatrD251VA", 345), "scene-019": ("7wFEz_z0XhY", 247), "scene-020": ("7wFEz_z0XhY", 262),
}


def bajar(vid):
    os.makedirs(ARC, exist_ok=True)
    out = os.path.join(ARC, vid + "_raw.mp4")
    if not os.path.exists(out):
        subprocess.run(["yt-dlp", "-f", "bv*+ba/b", "--merge-output-format", "mp4", "-o", out,
                        f"https://www.youtube.com/watch?v={vid}"], check=True)
    return out


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def armar():
    beats = {b["id"]: b for b in json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))}
    fuentes_p = os.path.join(AQUI, "fuentes.json")
    fuentes = json.load(open(fuentes_p, encoding="utf-8")) if os.path.exists(fuentes_p) else {}
    for sid, (vid, t0) in TRAMOS.items():
        raw = bajar(vid)
        d = beats[sid]["t1"] - beats[sid]["t0"] + 0.6
        total = dur(raw)
        if t0 + d > total:                      # anuncio corto: el tramo se recorta al final y se ralentiza un poco
            t0 = max(0.0, total - d)
        vel = 1.0
        if total < d:
            vel = total / d
            t0 = 0.0
        out = os.path.join(AQUI, "medios", sid + ".mp4")
        filtro = (f"[0:v]setpts=PTS/{vel:.4f},split[a][b];"
                  "[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=24:2,eq=brightness=-0.22[fondo];"
                  "[b]scale=-2:860,pad=iw+16:ih+16:8:8:color=0xFF6A1A[vent];"
                  "[fondo][vent]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]")
        subprocess.run([FF, "-y", "-v", "error", "-ss", f"{t0:.2f}", "-i", raw, "-t", f"{d / vel:.2f}",
                        "-filter_complex", filtro, "-map", "[v]", "-t", f"{d:.2f}", "-an", "-c:v", "libx264", "-preset", "fast",
                        "-crf", "18", out], check=True)
        fuentes[sid] = dict(fuentes.get(sid, {}), video=vid, desde=t0, url=f"https://www.youtube.com/watch?v={vid}", _archivo=True)
        print("ok", sid, vid, f"{t0:.1f}s", f"{d:.1f}s", f"vel {vel:.2f}" if vel < 1 else "")
    json.dump(fuentes, open(fuentes_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bq_p = os.path.join(AQUI, "busquedas.json")
    bq = json.load(open(bq_p, encoding="utf-8"))
    for sid, (vid, t0) in TRAMOS.items():
        bq[sid] = {"url": f"https://www.youtube.com/watch?v={vid}", "desde": t0, "_archivo": True}
    json.dump(bq, open(bq_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    armar()
