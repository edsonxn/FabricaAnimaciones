"""Render de cfo_kc_jugadas en 6 tramos paralelos y concat sin recomprimir -> salida/video_sin_audio.mp4.
Los trozos van a C: (TMP) porque E: anda casi lleno (28-oct-2026); solo el resultado unido va a salida/."""
import os
import subprocess
import time

R = r"C:\FabricaAnimaciones"
V = os.path.join(R, "videos", "cfo_kc_jugadas")
TMP = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "cfo_kc_par")
os.makedirs(TMP, exist_ok=True)
CORTES = [0, 175, 350, 525, 700, 875, 1050.0]
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render_par")
os.makedirs(LOG, exist_ok=True)
t0 = time.time()
procs = []
for k in range(6):
    a, b = CORTES[k], CORTES[k + 1]
    f = open(os.path.join(LOG, f"par_{k}.log"), "w", encoding="utf-8")
    procs.append((k, subprocess.Popen(["python", "fab.py", "cfo_kc_jugadas", "video", "--tramo", f"{a}-{b}", "--salida",
                                       os.path.join(TMP, f"par_{k}.mp4")], cwd=R, stdout=f, stderr=subprocess.STDOUT), f))
for k, p, f in procs:
    p.wait()
    f.close()
    print(f"par_{k}: código {p.returncode} · {time.time() - t0:.0f} s", flush=True)
lista = os.path.join(TMP, "par_lista.txt")
with open(lista, "w", encoding="utf-8") as fl:
    for k in range(6):
        fl.write(f"file 'par_{k}.mp4'\n")
r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy",
                    os.path.join(V, "salida", "video_sin_audio.mp4")], capture_output=True, text=True)
print("concat:", r.returncode, r.stderr[-400:], f"· total {time.time() - t0:.0f} s")
