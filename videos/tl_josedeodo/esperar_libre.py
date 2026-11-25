# -*- coding: utf-8 -*-
"""Regla del usuario (11-nov-2026): «Antes de lanzar, asegúrate que no hay otro. Si lo hay, pausa el tuyo hasta que terminen los otros.»
Espera (sin matar nada) a que NO haya procesos pesados de OTROS: render de `fab.py … video`, render_par, render3d.py, Edge sin ventana de
tactica3d, ffmpeg largos (> 60 s), Whisper (seleccionar / idioma_voz) o Chatterbox/Applio. Sale con 0 cuando está libre.
uso: python esperar_libre.py [--max 7200] [--cada 60]   y luego lanza lo pesado."""
import os
import sys
import time

import psutil

PATRONES = ("render_par", "render3d.py", "render_parcial", "chatterbox", "applio", "tts_select", "idioma_voz", "mesas_3d.py", "_3d.py")
MIO = {os.getpid(), os.getppid()}


def pesados():
    out = []
    ahora = time.time()
    for p in psutil.process_iter(["pid", "name", "cmdline", "create_time"]):
        if p.info["pid"] in MIO:
            continue
        cmd = " ".join(p.info["cmdline"] or []).lower()
        try:
            cmd = "[" + os.path.basename(p.cwd()) + "] " + cmd
        except Exception:
            pass
        n = (p.info["name"] or "").lower()
        if n.startswith("python") and (any(x in cmd for x in PATRONES) or (" video" in cmd and "fab.py" in cmd)
                                       or "secuencia video" in cmd or "-m secuencia" in cmd):
            out.append((p.info["pid"], cmd[:120]))
        elif n == "ffmpeg.exe" and ahora - (p.info["create_time"] or ahora) > 60:
            out.append((p.info["pid"], "ffmpeg " + cmd[:100]))
        elif n == "msedge.exe" and "--headless" in cmd:
            out.append((p.info["pid"], "edge headless (tactica3d)"))
    return out


if __name__ == "__main__":
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 7200
    cada = int(sys.argv[sys.argv.index("--cada") + 1]) if "--cada" in sys.argv else 60
    t0 = time.time()
    while True:
        ps = pesados()
        if not ps:
            print("LIBRE")
            sys.exit(0)
        if time.time() - t0 > mx:
            print("SIGUE OCUPADO tras", mx, "s:", ps[:3])
            sys.exit(1)
        print(time.strftime("%H:%M"), "ocupado:", "; ".join(f"{a} {b}" for a, b in ps[:3]), flush=True)
        time.sleep(cada)
