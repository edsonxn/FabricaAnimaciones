# -*- coding: utf-8 -*-
"""Mira una fuente de YouTube SIN bajarla: N cuadros chicos repartidos (yt-dlp -g a ≤360p + ffmpeg -ss) en un mosaico de
640 px con el segundo de cada cuadro → previews/_muestras/<id>.jpg (26-nov-2026, wow_oro_30_50). Para elegir `desde` en
_busquedas.py antes de `bajar` (webcams, rótulos, otra zona, retail, servidor privado = fuera).
  python _muestras.py ID[:a-b] [ID ...] [-n 12]      a-b = rango en segundos (por defecto 10 %-92 % del video)"""
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
OUT = os.path.join("previews", "_muestras")
TW, TH, COLS = 160, 90, 4


def info(vid):
    r = subprocess.run(["yt-dlp", "-f", "bv*[height<=360]/bv*[height<=480]/b", "--print", "%(duration)s", "--print", "%(title)s",
                        "-g", "--no-warnings", f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=120)
    ln = [x for x in r.stdout.splitlines() if x.strip()]
    if len(ln) < 3:
        return None, None, None, (r.stderr or "")[-160:]
    return float(ln[0] or 0), ln[1], ln[2], None


def cuadro(url, t, dest):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.1f}", "-i", url, "-frames:v", "1",
                    "-vf", f"scale={TW}:{TH}", dest], capture_output=True, timeout=90)
    return os.path.exists(dest)


def muestra(arg, n):
    vid, _, rango = arg.partition(":")
    dur, titulo, url, err = info(vid)
    if not url:
        return f"{vid}: FALLÓ {err}"
    a, b = (dur * .10, dur * .92)
    if rango:
        a, b = [float(x) for x in rango.split("-")]
    ts = [a + (b - a) * k / max(1, n - 1) for k in range(n)]
    tmp = tempfile.mkdtemp()
    with ThreadPoolExecutor(6) as ex:
        oks = list(ex.map(lambda kt: cuadro(url, kt[1], os.path.join(tmp, f"{kt[0]}.png")), enumerate(ts)))
    filas = (n + COLS - 1) // COLS
    im = Image.new("RGB", (TW * COLS, (TH + 13) * filas + 14), (20, 20, 20))
    d = ImageDraw.Draw(im)
    d.text((3, 1), f"{vid} {int(dur)}s {titulo[:80]}", fill=(255, 220, 120))
    for k, (t, ok) in enumerate(zip(ts, oks)):
        x, y = (k % COLS) * TW, 14 + (k // COLS) * (TH + 13)
        if ok:
            im.paste(Image.open(os.path.join(tmp, f"{k}.png")).convert("RGB"), (x, y))
        d.text((x + 3, y + TH), f"{int(t)}", fill=(200, 255, 200))
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, f"{vid}.jpg"), quality=82)
    return f"{vid}: {int(dur)}s {sum(oks)}/{n} · {titulo[:70]}"


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 12
    if "-n" in args:
        n = int(args[args.index("-n") + 1])
        del args[args.index("-n"):args.index("-n") + 2]
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(lambda a: muestra(a, n), args):
            print(r, flush=True)
