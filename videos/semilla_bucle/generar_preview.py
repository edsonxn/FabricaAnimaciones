# -*- coding: utf-8 -*-
"""Genera el preview completo (hoja de contactos 4x4 y video MP4 540x960 con audio)
para revisión previa antes del render final 1080x1920.
"""
import json
import math
import os
import subprocess
import sys
import time
from multiprocessing import Pool

import cv2
import numpy as np

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath("../../nucleo"))
sys.path.insert(0, os.path.abspath("."))

import escenas as S

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
FPS = 30
NFRAMES = int(round(TOTAL * FPS))
W, H = 1080, 1920
PW, PH = 540, 960  # Resolución del preview fluido

os.makedirs("previews", exist_ok=True)
os.makedirs("previews/segmentos", exist_ok=True)


def a_uint8(img):
    return np.clip(img * 255 + 0.5, 0, 255).astype(np.uint8)


# ==============================================================================
# 1. GENERACIÓN DE HOJA DE CONTACTOS (16 FOTOGRAMAS CLAVE)
# ==============================================================================
def generar_hoja_contactos():
    print("--- Generando Hoja de Contactos (16 cuadros clave) ---", flush=True)
    m = S.CLASES["vuelo"](S._ESC["vuelo"], 0)

    puntos = [
        (0.00, "00.00s | Vuelo (Inicio Pompon)"),
        (2.00, "02.00s | Vuelo (Tierra gira)"),
        (4.50, "04.50s | Vuelo (Despegue)"),
        (6.80, "06.80s | Vuelo (Ascenso espiral)"),
        (8.50, "08.50s | Viento (Mariposa)"),
        (10.50, "10.50s | Viento (Colinas verdes)"),
        (13.00, "13.00s | Tormenta (Rayo y trueno)"),
        (15.20, "15.20s | Tormenta (Gota gigante)"),
        (17.50, "17.50s | Grieta (Impacto elastico)"),
        (19.80, "19.80s | Grieta (Bufanda / Zzz)"),
        (22.50, "22.50s | Brote (Raices profundas)"),
        (24.80, "24.80s | Brote (Tallo elastico)"),
        (27.50, "27.50s | Flor (Diente de leon 360)"),
        (29.80, "29.80s | Flor (Abeja poliniza)"),
        (33.50, "33.50s | Morfosis (Crayon blanco)"),
        ((NFRAMES - 1) / FPS, f"{(NFRAMES - 1) / FPS:.2f}s | Cierre (Bucle identico)"),
    ]

    cuadros = []
    for idx, (t, etiqueta) in enumerate(puntos):
        im_float = m.render(None, t)
        im_u8 = a_uint8(im_float)

        # Guardar cuadros primero y ultimo
        if idx == 0:
            cv2.imwrite("previews/f_primero.png", cv2.cvtColor(im_u8, cv2.COLOR_RGB2BGR))
        elif idx == len(puntos) - 1:
            cv2.imwrite("previews/f_ultimo.png", cv2.cvtColor(im_u8, cv2.COLOR_RGB2BGR))

        # Redimensionar para la hoja (270x480 cada tile)
        tile = cv2.resize(im_u8, (270, 480), interpolation=cv2.INTER_AREA)
        tile_bgr = cv2.cvtColor(tile, cv2.COLOR_RGB2BGR)

        # Banner de texto
        cv2.rectangle(tile_bgr, (0, 0), (270, 32), (25, 25, 25), -1)
        cv2.putText(tile_bgr, etiqueta, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)
        cuadros.append(tile_bgr)

    # Rejilla 4x4 (1080 x 1920)
    filas = []
    for r in range(4):
        fila = np.hstack(cuadros[r * 4 : (r + 1) * 4])
        filas.append(fila)
    hoja = np.vstack(filas)

    ruta_hoja = "previews/hoja_completa.jpg"
    cv2.imwrite(ruta_hoja, hoja, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(f"Hoja guardada en {ruta_hoja} ({hoja.shape[1]}x{hoja.shape[0]})", flush=True)


# ==============================================================================
# 2. GENERACION DEL VIDEO PREVIEW 540x960 CON AUDIO
# ==============================================================================
_trabajador_m = None


def _init_trabajador():
    global _trabajador_m
    _trabajador_m = S.CLASES["vuelo"](S._ESC["vuelo"], 0)


def _render_segmento(args):
    i0, i1, ruta_salida = args
    tmp_salida = ruta_salida + ".tmp.mp4"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{PW}x{PH}",
        "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", "-g", "30",
        tmp_salida
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        t = i / FPS
        im_float = _trabajador_m.render(None, t)
        im_u8 = a_uint8(im_float)
        sm = cv2.resize(im_u8, (PW, PH), interpolation=cv2.INTER_AREA)
        proc.stdin.write(sm.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"Error renderizando segmento {ruta_salida}")
    os.replace(tmp_salida, ruta_salida)
    return ruta_salida


def generar_video_preview(num_procs=8):
    print(f"\n--- Generando Video Preview MP4 (540x960 @ 30 FPS, {TOTAL:.2f}s) ---", flush=True)
    tam_segmento = 60  # 2 segundos por segmento
    tareas = []
    for k, i in enumerate(range(0, NFRAMES, tam_segmento)):
        i_fin = min(i + tam_segmento, NFRAMES)
        ruta_seg = f"previews/segmentos/seg_{k:03d}.mp4"
        tareas.append((i, i_fin, ruta_seg))

    t_inicio = time.time()
    hechos = 0
    with Pool(num_procs, initializer=_init_trabajador) as pool:
        for _ in pool.imap_unordered(_render_segmento, tareas):
            hechos += 1
            print(f"  [{hechos}/{len(tareas)}] segmentos listos ({time.time() - t_inicio:.1f}s)", flush=True)

    # Concatenar segmentos
    lista_txt = "previews/segmentos/lista.txt"
    with open(lista_txt, "w") as f:
        for _, _, ruta in tareas:
            f.write(f"file '{os.path.basename(ruta)}'\n")

    video_preview = "previews/semilla_bucle_preview.mp4"
    audio_wav = "audio/final.wav"

    print("Concatenando y sincronizando con audio/final.wav...", flush=True)
    cmd_final = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", lista_txt,
        "-i", audio_wav,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        video_preview
    ]
    subprocess.run(cmd_final, check=True)
    duracion = time.time() - t_inicio
    peso_mb = os.path.getsize(video_preview) / (1024 * 1024)
    print(f"Video Preview COMPLETO listo en {video_preview} ({peso_mb:.2f} MB, {duracion:.1f}s)", flush=True)


if __name__ == "__main__":
    generar_hoja_contactos()
    generar_video_preview()
