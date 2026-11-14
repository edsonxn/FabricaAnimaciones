import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
src, out, t0, paso, n = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
W, H, C = 320, 180, 6
fnt = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
filas = (n + C - 1) // C
im = Image.new("RGB", (W * C, H * filas))
for i in range(n):
    t = t0 + i * paso
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    if len(raw) == W * H * 3:
        im.paste(Image.frombytes("RGB", (W, H), raw), ((i % C) * W, (i // C) * H))
    ImageDraw.Draw(im).text(((i % C) * W + 5, (i // C) * H + 3), f"{t:.1f}", font=fnt, fill=(255, 230, 0), stroke_width=3, stroke_fill=(0, 0, 0))
im.save(out, quality=80)
print(out)
