# baja en 360p las fuentes candidatas y hace una hoja de cuadros con el segundo de cada uno (previews/_ref_<id>.jpg)
import subprocess, json, os, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
R = r"E:\FabricaAnimaciones\videos\fo_enemigos_ocultos\_ref"
ids = [l.split(" | ")[1] for l in open("_meta.txt", encoding="utf-8") if " | " in l and "ERR" not in l]
ids += [i for i in sys.argv[1:]]
def baja(i):
    out = os.path.join(R, i + ".mp4")
    if not os.path.exists(out):
        subprocess.run(["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=360][ext=mp4]/bv*[height<=360]/b[height<=360]",
                        "-o", out, "https://youtu.be/" + i], timeout=600)
    return i
def hoja(i):
    src = os.path.join(R, i + ".mp4"); dst = f"previews/_ref_{i}.jpg"
    if not os.path.exists(src) or os.path.exists(dst): return
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                             capture_output=True, text=True).stdout.strip() or 0)
    n = 20; C = 5; W, H = 220, 124
    S = Image.new("RGB", (C * W, (n // C) * (H + 16)), (20, 20, 20)); dr = ImageDraw.Draw(S)
    f = ImageFont.truetype("arialbd.ttf", 13)
    for k in range(n):
        t = d * (k + 0.5) / n
        tmp = os.path.join(R, f"_{i}_{k}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.1f}", "-i", src, "-frames:v", "1", "-vf", f"scale={W}:{H}", tmp])
        if os.path.exists(tmp):
            x, y = (k % C) * W, (k // C) * (H + 16)
            S.paste(Image.open(tmp), (x, y)); os.remove(tmp)
            dr.text((x + 3, y + H), f"{t:.0f}s", fill=(255, 220, 0), font=f)
    S.save(dst, quality=75)
with ThreadPoolExecutor(5) as ex:
    list(ex.map(baja, ids))
with ThreadPoolExecutor(4) as ex:
    list(ex.map(hoja, ids))
print("hojas:", len([i for i in ids if os.path.exists(f"previews/_ref_{i}.jpg")]), "de", len(ids))
