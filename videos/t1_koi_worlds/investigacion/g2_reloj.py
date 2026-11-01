# python g2_reloj.py <nombre> t1 t2 ...  -> cuadros_g2/<nombre>.png: marcador + reloj del HUD (720p) en cada segundo t del VOD, con la t escrita
import subprocess, sys, os
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
U = open("cuadros_g2/url720.txt").read().strip()
nom, ts = sys.argv[1], sys.argv[2:]
outs = []
for t in ts:
    o = f"cuadros_g2/_c_{t}.png"
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", t, "-i", U, "-frames:v", "1", "-vf",
                    f"crop=480:84:400:0,scale=600:-1,pad=760:ih:160:0,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{t}':x=8:y=30:fontsize=28:fontcolor=yellow", o], check=True)
    outs.append(o)
args = [FF, "-loglevel", "error", "-y"]
for o in outs: args += ["-i", o]
args += ["-filter_complex", f"vstack=inputs={len(outs)}" if len(outs) > 1 else "null", f"cuadros_g2/{nom}.png"]
subprocess.run(args, check=True)
for o in outs: os.remove(o)
print("ok", nom)
