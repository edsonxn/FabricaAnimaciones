# -*- coding: utf-8 -*-
"""Lanza el render (reanuda segmentos hechos) pidiendo a Windows que NO suspenda el equipo mientras dura
(SetThreadExecutionState solo para este proceso; no cambia la configuración de energía). Al terminar, borra segmentos/
si el video sin audio quedó bien (el disco C: va justo).   python _render_despierto.py [procesos]"""
import ctypes
import os
import shutil
import subprocess
import sys
import time

V = "satoshi_nakamoto"
RAIZ = r"C:\FabricaAnimaciones"
LOG = os.path.join(RAIZ, "videos", V, "render_log.txt")
ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001

procs = sys.argv[1] if len(sys.argv) > 1 else "4"
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
env = dict(os.environ, FAB_CRF="21", PYTHONIOENCODING="utf-8")
with open(LOG, "a", encoding="utf-8") as f:
    f.write(f"\n=== relanzado {time.strftime('%Y-%m-%d %H:%M:%S')} con {procs} procesos ===\n")
    f.flush()
    r = subprocess.run([sys.executable, "fab.py", V, "video", "--procs", procs], cwd=RAIZ, stdout=f, stderr=subprocess.STDOUT, env=env)
    sal = os.path.join(RAIZ, "videos", V, "salida", "video_sin_audio.mp4")
    if r.returncode == 0 and os.path.exists(sal) and os.path.getsize(sal) > 100_000_000:
        shutil.rmtree(os.path.join(RAIZ, "videos", V, "segmentos"), ignore_errors=True)
        f.write("segmentos/ borrados (video_sin_audio.mp4 listo)\n")
    f.write(f"=== fin {time.strftime('%Y-%m-%d %H:%M:%S')} código {r.returncode} ===\n")
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
