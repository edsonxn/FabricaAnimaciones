"""Render de ig_lyon_worlds en 6 tramos paralelos y concat sin recomprimir -> salida/video_sin_audio.mp4."""
import os
import subprocess
import time

R = r"C:\FabricaAnimaciones"
V = os.path.join(R, "videos", "ig_lyon_worlds")
CORTES = [520, 563.33, 606.67, 650, 691.5, 733, 774.55]  # 2.ª pasada: solo par_4 y par_5 (27-oct)
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render_par")
os.makedirs(LOG, exist_ok=True)
t0 = time.time()
procs = []
for k in range(6):
    a, b = CORTES[k], CORTES[k + 1]
    f = open(os.path.join(LOG, f"par_{k}.log"), "w", encoding="utf-8")
    procs.append((k, subprocess.Popen(["python", "fab.py", "ig_lyon_worlds", "video", "--tramo", f"{a}-{b}", "--salida",
                                       f"salida/fix_{k}.mp4"], cwd=R, stdout=f, stderr=subprocess.STDOUT), f))
for k, p, f in procs:
    p.wait()
    f.close()
    print(f"par_{k}: código {p.returncode} · {time.time() - t0:.0f} s", flush=True)
lista = os.path.join(V, "salida", "par_lista.txt")
with open(lista, "w", encoding="utf-8") as fl:
    for k in range(6):
        fl.write(f"file 'par_{k}.mp4'\n")
r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy",
                    os.path.join(V, "salida", "video_sin_audio.mp4")], capture_output=True, text=True)
print("concat:", r.returncode, r.stderr[-400:], f"· total {time.time() - t0:.0f} s")
