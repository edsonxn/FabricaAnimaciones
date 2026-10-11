# -*- coding: utf-8 -*-
"""Renderizado de las escenas creadas (escenas 1 a 15, de 0.0s a 555.0s):
   - Genera segmentos de 90 cuadros (3 s) en la carpeta 'segmentos/' exactamente como nucleo/render.py.
   - Si un segmento ya existe y es válido, lo reutiliza (no duplica trabajo).
   - Utiliza maxtasksperchild y recolección de basura para evitar saturación de memoria en Windows.
   - Concatena los 185 segmentos en salida/independencia_escenas_1_a_15_sin_audio.mp4.
   - Mezcla con audio/final.wav (recortado a 555.0 s) a AAC 320k en salida/independencia_escenas_1_a_15.mp4.
   - Genera subtítulos salida/independencia_escenas_1_a_15.srt.
"""
import gc
import json
import os
import subprocess
import sys
import time
from multiprocessing import Pool

import render as R
from motor import FPS, H, W

T0 = 0.0
T1 = 555.0  # Fin de escena 15 (iturbide)
TAM = 90    # Mismo tamaño de trozo que nucleo/render.py (3 segundos a 30 FPS)
NFRAMES_PARCIAL = int(round(T1 * FPS))  # 16650 cuadros (185 segmentos)


def _trozo_seguro(args):
    res = R._trozo(args)
    gc.collect()
    return res


def srt_parcial(ruta, t_max):
    TL = json.load(open("timeline.json", encoding="utf-8"))
    def ts(x):
        h, r = divmod(x, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
    n = 0
    with open(ruta, "w", encoding="utf-8") as f:
        for e in TL["escenas"]:
            if e["t0"] >= t_max:
                break
            for fr in e["frases"]:
                if fr["t0"] >= t_max:
                    break
                n += 1
                t_fin = min(fr["t1"], t_max)
                f.write(f"{n}\n{ts(fr['t0'])} --> {ts(t_fin)}\n{fr['texto']}\n\n")


def main():
    procs = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 4
    procs = R.procesos_seguros(procs)
    print(f"=== Renderizado de escenas creadas 1 a 15 (0.0s a {T1}s) ===", flush=True)
    print(f"Cuadros totales: {NFRAMES_PARCIAL} | Procesos concurrentes: {procs}", flush=True)

    os.makedirs("segmentos", exist_ok=True)
    os.makedirs("salida", exist_ok=True)

    tareas = [(i, min(i + TAM, NFRAMES_PARCIAL), f"segmentos/seg_{i // TAM:04d}.mp4")
              for i in range(0, NFRAMES_PARCIAL, TAM)]
    total_tareas = len(tareas)
    
    # Contar cuántos ya están listos
    ya_hechos = sum(1 for _, _, r in tareas if os.path.exists(r) and os.path.getsize(r) > 1000)
    print(f"Total segmentos: {total_tareas} (90 cuadros / 3s c/u) | Ya listos: {ya_hechos}", flush=True)

    t0 = time.time()
    hechos = 0
    with Pool(procs, initializer=R._init, maxtasksperchild=8) as pool:
        for ruta, dt in pool.imap_unordered(_trozo_seguro, tareas):
            hechos += 1
            elapsed = time.time() - t0
            pct = (hechos / total_tareas) * 100.0
            print(f"[{hechos}/{total_tareas}] ({pct:.1f}%) {ruta} {dt:.1f}s (tiempo transcurrido: {elapsed:.0f}s)", flush=True)

    print(f"\nTodos los segmentos completados en {time.time() - t0:.0f}s. Ensamblando video...", flush=True)

    lista_txt = "segmentos/lista_parcial.txt"
    with open(lista_txt, "w") as f:
        for _, _, ruta in tareas:
            f.write(f"file '{os.path.basename(ruta)}'\n")

    vid_sin_audio = "salida/independencia_escenas_1_a_15_sin_audio.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", lista_txt, "-c", "copy", vid_sin_audio], check=True)
    print(f"Video sin audio ensamblado: {vid_sin_audio}", flush=True)

    master_parcial = "salida/independencia_escenas_1_a_15.mp4"
    print("Mezclando con audio/final.wav (pista maestra 0.0s a 555.0s)...", flush=True)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", vid_sin_audio,
        "-ss", "0", "-t", str(T1),
        "-i", "audio/final.wav",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-movflags", "+faststart",
        "-metadata", "title=La Independencia de México (Escenas 1-15)",
        master_parcial
    ], check=True)

    srt_path = "salida/independencia_escenas_1_a_15.srt"
    srt_parcial(srt_path, T1)

    print(f"\n========================================================")
    print(f"¡RENDER PARCIAL LISTO EXITOSAMENTE!")
    print(f"Video con audio: {master_parcial} ({os.path.getsize(master_parcial) / 1e6:.1f} MB)")
    print(f"Subtítulos: {srt_path}")
    print(f"Duración: {T1}s (9 min 15 s) - Escenas 1 a 15 completas")
    print(f"Los segmentos en 'segmentos/' se conservaron para reutilizarse en el render final completo.")
    print(f"========================================================", flush=True)


if __name__ == "__main__":
    main()
