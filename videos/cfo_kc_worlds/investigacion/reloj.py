# python reloj.py <videoId> <nombre> t1 t2 ...  -> cuadros_kc/<nombre>.jpg con el marcador+reloj de cada t (en orden, de arriba abajo)
import subprocess, sys, os
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
vid, nom, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
uf = f"cuadros_kc/url_{vid}.txt"
if not os.path.exists(uf):
    u = subprocess.run(["yt-dlp", "--no-warnings", "-g", "-f", "bv*[height<=720][ext=mp4]/bv*[height<=720]", f"https://youtu.be/{vid}"],
                       capture_output=True, text=True).stdout.split()
    open(uf, "w").write([x for x in u if x.startswith("http")][0])
U = open(uf).read().strip()
outs = []
for t in ts:
    o = f"cuadros_kc/_r_{t}.jpg"
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", t, "-i", U, "-frames:v", "1", "-vf", "crop=240:80:520:0,scale=300:-1", o], check=True)
    outs.append(o)
args = [FF, "-loglevel", "error", "-y"]
for o in outs: args += ["-i", o]
args += ["-filter_complex", f"vstack=inputs={len(outs)}" if len(outs) > 1 else "null", f"cuadros_kc/{nom}.jpg"]
subprocess.run(args, check=True)
for o in outs: os.remove(o)
print("ok", nom, ts)
