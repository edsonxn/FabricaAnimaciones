# Hoja de cuadros de una fuente local: python g2_hoja.py <fuente> <nombre> <crop|full> <ancho> <cols> <K> t1 t2 ...
# crop = "w:h:x:y" sobre 1080p ("full" = cuadro entero). Rotula cada cuadro con t de la fuente y reloj HUD = t + K.
import subprocess, sys, os
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
src, nom, crop, ancho, cols, K = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
ts = sys.argv[7:]
outs = []
for t in ts:
    h = float(t) + K
    lab = f"t{float(t):.1f} HUD {int(h // 60):02d}\\:{h % 60:04.1f}"
    vf = (f"crop={crop}," if crop != "full" else "") + f"scale={ancho}:-2,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{lab}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.7"
    o = f"cuadros_g2/_h_{t}.png"
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", t, "-i", src, "-frames:v", "1", "-vf", vf, o], check=True)
    outs.append(o)
while len(outs) % cols: outs.append(outs[-1])
filas = len(outs) // cols
args = [FF, "-loglevel", "error", "-y"]
for o in outs: args += ["-i", o]
fc = "".join(f"[{i}]" for i in range(len(outs))) + f"xstack=inputs={len(outs)}:layout=" + "|".join(
    f"{'+'.join(['w0'] * (i % cols)) or '0'}_{'+'.join(['h0'] * (i // cols)) or '0'}" for i in range(len(outs)))
args += ["-filter_complex", fc, f"cuadros_g2/{nom}.jpg"]
subprocess.run(args, check=True)
for o in set(outs): os.remove(o)
print("ok", nom)
