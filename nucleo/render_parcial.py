# -*- coding: utf-8 -*-
"""Render PARCIAL de un video dibujado por código: solo el principio (0..HASTA s) para verlo antes de hacer las demás escenas.

    python fab.py <video> video --hasta 563 [--procs 12]      (el panel lo ve como un render normal, con sus barritas)

- HASTA se redondea hacia abajo a un múltiplo de 3 s (tamaño de segmento), así no queda ningún segmento cortado y el
  render completo posterior reutiliza todo lo hecho aquí (mismas rutas segmentos/seg_NNNN.mp4).
- Escribe segmentos/parcial.json {"hasta": s, "nframes": n}: el panel limita el avance a ese tramo; `fab.py <v> video` sin --hasta lo borra.
- Une los segmentos y le pone el audio (audio/final.wav si existe) -> salida/<video>_AVANCE.mp4. NO toca el MASTER.
- Las escenas aún sin hacer no se dibujan (en escenas.py usa una clase de relleno, ver videos/sociedad_1200/_reg.py).
- Está aparte de render.py a propósito: render.py entra en la firma del código que decide si un segmento guardado sigue vigente.
"""
import json
import os
import subprocess
import sys
import time

import render as R


def main():
    a = sys.argv
    hasta = float(a[a.index("--hasta") + 1])
    procs = int(a[a.index("--procs") + 1]) if "--procs" in a else 12
    tam = 90
    seg_s = tam / R.FPS
    F = min(R.NFRAMES, int(hasta // seg_s) * tam)
    if F <= 0:
        raise SystemExit("--hasta debe ser al menos 3 s")
    os.makedirs("segmentos", exist_ok=True)
    os.makedirs("salida", exist_ok=True)
    preset = R._info_segmentos(tam, os.environ.get("FAB_PRESET", "medium"))
    with open("segmentos/parcial.json", "w", encoding="utf-8") as f:
        json.dump(dict(hasta=F / R.FPS, nframes=F), f)
    try:           # misma revisión que render.video(): lo hecho con código anterior se rehace, lo vigente se reutiliza
        import cache_escenas
        nucleo = os.path.dirname(os.path.abspath(R.__file__))
        cache_escenas.depurar(os.getcwd(), nucleo)
        cache_escenas.FIRMA_RENDER = cache_escenas.firma_codigo(os.getcwd(), nucleo)
    except Exception as e:                     # noqa: BLE001
        print(f"(aviso) no se pudo revisar los segmentos de la vista previa: {e}", flush=True)
    tareas = [(i, i + tam, f"segmentos/seg_{i // tam:04d}.mp4", preset) for i in range(0, F, tam)]
    faltan = sum(1 for _, _, r, _ in tareas if not (os.path.exists(r) and os.path.getsize(r) > 1000))
    print(f"render parcial 0..{F / R.FPS:.0f} s: {faltan} de {len(tareas)} segmentos por renderizar, {procs} procesos", flush=True)
    t0 = time.time()
    with R._SinSuspender():
        R._repartir(tareas, R.procesos_seguros(procs), procs, t0)
    lista = "segmentos/lista_parcial.txt"
    with open(lista, "w") as f:
        for _, _, ruta, _ in tareas:
            f.write(f"file '{os.path.basename(ruta)}'\n")
    nombre = os.path.basename(os.getcwd())
    out = f"salida/{nombre}_AVANCE.mp4"
    audio = ["-i", "audio/final.wav", "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"] if os.path.exists("audio/final.wav") else []
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, *audio,
                    "-c:v", "copy", "-t", f"{F / R.FPS:.3f}", "-movflags", "+faststart", out], check=True)
    print(f"listo: {out}  (0..{F / R.FPS:.0f} s, {time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
