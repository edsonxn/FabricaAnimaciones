# -*- coding: utf-8 -*-
"""Lanza el render (reanuda segmentos hechos) pidiendo a Windows que NO suspenda el equipo mientras dura
(SetThreadExecutionState solo para este proceso; no cambia la configuración de energía). Conserva segmentos/
para arreglos por tramos (`video --rehacer`).   python _render_despierto.py [procesos]"""
import ctypes
import os
import subprocess
import sys
import time

V = "polybius"
RAIZ = r"C:\FabricaAnimaciones"
LOG = os.path.join(RAIZ, "videos", V, "render_log.txt")
ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001

procs = sys.argv[1] if len(sys.argv) > 1 else "5"
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
env = dict(os.environ, FAB_CRF="21", PYTHONIOENCODING="utf-8")
with open(LOG, "a", encoding="utf-8") as f:
    f.write(f"\n=== lanzado {time.strftime('%Y-%m-%d %H:%M:%S')} con {procs} procesos ===\n")
    f.flush()
    r = subprocess.run([sys.executable, "fab.py", V, "video", "--procs", procs], cwd=RAIZ, stdout=f, stderr=subprocess.STDOUT, env=env)
    f.write(f"=== fin {time.strftime('%Y-%m-%d %H:%M:%S')} código {r.returncode} ===\n")
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
