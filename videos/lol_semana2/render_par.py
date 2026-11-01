"""Render del ACTO A de lol_semana2 en 6 tramos paralelos y concat sin recomprimir -> salida/video_sin_audio.mp4.
Los trozos van a C: (TMP); solo el resultado unido va a salida/ (E:). Requiere E: montado. python videos/lol_semana2/render_par.py"""
import json
import os
import subprocess
import time

R = r"C:\FabricaAnimaciones"
V = os.path.join(R, "videos", "lol_semana2")
TMP = os.path.join(os.environ.get("TEMP", r"C:\Windows\Temp"), "lol_semana2_par")
os.makedirs(TMP, exist_ok=True)
TOTAL = json.load(open(os.path.join(V, "timeline.json"), encoding="utf-8"))["total"]
N = 6
CORTES = [round(TOTAL * k / N, 3) for k in range(N + 1)]
LOG = os.path.join(TMP, "logs")
os.makedirs(LOG, exist_ok=True)
subprocess.run(["python", os.path.join(V, "investigacion", "cortes_voz.py")], check=True)   # nunca cortar la voz dentro de una palabra
t0 = time.time()
SIMULTANEOS = 4          # con 6 se agotó la memoria (31-oct-2026); par_<k>.ok = tramo bueno, se salta al reanudar
pendientes = [k for k in range(N) if not os.path.exists(os.path.join(TMP, f"par_{k}.ok"))]
print("pendientes:", pendientes, flush=True)
vivos, fallos = [], []
while pendientes or vivos:
    while pendientes and len(vivos) < SIMULTANEOS:
        k = pendientes.pop(0)
        a, b = CORTES[k], CORTES[k + 1]
        f = open(os.path.join(LOG, f"par_{k}.log"), "w", encoding="utf-8")
        vivos.append((k, subprocess.Popen(["python", "fab.py", "lol_semana2", "video", "--tramo", f"{a}-{b}", "--salida",
                                           os.path.join(TMP, f"par_{k}.mp4")], cwd=R, stdout=f, stderr=subprocess.STDOUT), f))
    for item in vivos[:]:
        k, p, f = item
        if p.poll() is None:
            continue
        f.close()
        vivos.remove(item)
        print(f"par_{k}: código {p.returncode} · {time.time() - t0:.0f} s", flush=True)
        if p.returncode == 0:
            open(os.path.join(TMP, f"par_{k}.ok"), "w").close()
        else:
            fallos.append(k)
    time.sleep(3)
if fallos:
    raise SystemExit(f"tramos fallidos {fallos}: no se une nada; revisa {LOG} y relanza (se reanuda)")
lista = os.path.join(TMP, "par_lista.txt")
with open(lista, "w", encoding="utf-8") as fl:
    for k in range(N):
        fl.write(f"file 'par_{k}.mp4'" + chr(10))
r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy",
                    os.path.join(V, "salida", "video_sin_audio.mp4")], capture_output=True, text=True)
print("concat:", r.returncode, r.stderr[-400:], f"· total {time.time() - t0:.0f} s")
# vista previa del acto A con su audio completo (audio/final.wav lo deja `mezcla`)
r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-i", os.path.join(V, "salida", "video_sin_audio.mp4"), "-i",
                    os.path.join(V, "audio", "final.wav"), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest",
                    "-movflags", "+faststart", os.path.join(V, "salida", "lol_semana2_ACTO_A.mp4")], capture_output=True, text=True)
print("mux:", r.returncode, r.stderr[-400:])
