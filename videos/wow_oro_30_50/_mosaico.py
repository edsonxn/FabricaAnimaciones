# -*- coding: utf-8 -*-
"""Hoja barata de clips rehechos: 3 cuadros (15/50/85 %) por beat, 640 px de ancho, con el beat, la fuente y el texto
de la voz → previews/_rehechos_<n>.jpg (26-nov-2026, wow_oro_30_50; idea de docs/estilo_secuencia_yt.md: «revisar los
rehechos en un mosaico propio es más barato que regenerar todas las hojas»).
  python _mosaico.py 12,15-18 [--nombre r1] [--por 6]"""
import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TW, TH = 208, 117


def ids(arg):
    out = []
    for p in arg.split(","):
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", p.strip())
        if m:
            out += list(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1))
    return out


def cuadros(ruta, tmp):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True)
    try:
        dur = float(r.stdout.strip() or 0)
    except ValueError:              # clip a medio escribir (bajar en curso)
        return [None, None, None]
    out = []
    for k, f in enumerate((.15, .5, .85)):
        d = os.path.join(tmp, f"{os.path.basename(ruta)}_{k}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{dur * f:.2f}", "-i", ruta, "-frames:v", "1",
                        "-vf", f"scale={TW}:{TH}", d], capture_output=True)
        out.append(d if os.path.exists(d) else None)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    nombre = a[a.index("--nombre") + 1] if "--nombre" in a else "r"
    por = int(a[a.index("--por") + 1]) if "--por" in a else 6
    lista = ids(a[0])
    beats = {b["id"]: b for b in json.load(open("beats.json", encoding="utf-8"))}
    fu = json.load(open("fuentes.json", encoding="utf-8"))
    tmp = tempfile.mkdtemp()
    for h in range(0, len(lista), por):
        grupo = lista[h:h + por]
        im = Image.new("RGB", (TW * 3 + 4, (TH + 28) * len(grupo)), (18, 18, 18))
        d = ImageDraw.Draw(im)
        for k, n in enumerate(grupo):
            bid = f"scene-{n:03d}"
            y = k * (TH + 28)
            r = fu.get(bid, {})
            d.text((3, y + 1), f"{n:03d} {r.get('video', '?')}@{int(r.get('desde', 0))}  {beats[bid]['texto'][:70]}", fill=(255, 220, 120))
            d.text((3, y + 13), beats[bid]["texto"][70:150], fill=(200, 200, 200))
            ruta = os.path.join("medios", bid + ".mp4")
            if os.path.exists(ruta):
                for j, c in enumerate(cuadros(ruta, tmp)):
                    if c:
                        im.paste(Image.open(c).convert("RGB"), (j * (TW + 2), y + 27))
        dest = os.path.join("previews", f"_rehechos_{nombre}_{h // por + 1}.jpg")
        im.save(dest, quality=82)
        print(dest)
