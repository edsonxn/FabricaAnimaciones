# -*- coding: utf-8 -*-
"""Render final: escenas + transiciones + subtítulos + progreso -> segmentos H.264 en paralelo -> concat.

Uso:
  python render.py prueba 12.5 28.1 ...     # cuadros sueltos a previews/
  python render.py video [--procs 13]       # video completo (sin audio) -> salida/video_sin_audio.mp4
"""
import json
import math
import os
import subprocess
import sys
import time
from multiprocessing import Pool

import cv2
import numpy as np

import efectos as E
import escenas as S
from motor import BLANCO, NEGRO, FPS, H, W, Lienzo, a_uint8, ancho_texto, componer, e_back, prog, rect_red
from ritmo import env_bombo

TL = json.load(open("timeline.json", encoding="utf-8"))
CLASES = S.CLASES   # cada video define en su escenas.py: id de escena -> clase
TOTAL = TL["total"]
NFRAMES = int(round(TOTAL * FPS))
AMARILLO = (255, 214, 64)


# ------------------------------------------------------------ subtítulos
def trozos_subtitulos():
    """Agrupa palabras en trozos cortos; el título de cada ítem no se subtitula (ya está en pantalla)."""
    out = []
    for e in TL["escenas"]:
        for fi, f in enumerate(e["frases"]):
            if "num" in e and fi == 0:
                continue
            cur, nch = [], 0
            for w in f["words"]:
                txt = w["w"].strip()
                limpio = txt.rstrip(",.;:")
                cur.append(dict(w=limpio, s=w["s"], e=w["e"]))
                nch += len(limpio) + 1
                if nch > 24 or len(cur) >= 5 or txt[-1] in ",.;:?!":
                    out.append(cur)
                    cur, nch = [], 0
            if cur:
                out.append(cur)
    for i, c in enumerate(out):
        ini = c[0]["s"] - 0.06
        fin = c[-1]["e"] + 0.35
        if i + 1 < len(out):
            fin = min(fin, out[i + 1][0]["s"] - 0.06)
        c_ = dict(ws=c, ini=ini, fin=max(fin, c[-1]["e"] + 0.02))
        out[i] = c_
    return out


TROZOS = trozos_subtitulos()


def dibujar_subtitulos(lz, t):
    act = [c for c in TROZOS if c["ini"] <= t < c["fin"]]
    if not act:
        return False
    c = act[0]
    px, borde = 56, 9
    # una sola palabra activa: la última que ya empezó (y que no terminó hace rato)
    idx = -1
    for i, w in enumerate(c["ws"]):
        if t >= w["s"] - 0.03:
            idx = i
    if idx >= 0 and t > c["ws"][idx]["e"] + 0.25:
        idx = -1
    esp = ancho_texto(" ", "black", px) + 2 * borde
    kks = [1.1 if i == idx else 1.0 for i in range(len(c["ws"]))]
    anchos = [ancho_texto(w["w"], "black", px) * kk for w, kk in zip(c["ws"], kks)]
    total = sum(anchos) + esp * (len(anchos) - 1)
    k_in = e_back(prog(t, c["ini"], c["ini"] + 0.12), 1.4)
    x = 960 - total / 2
    y = 992
    with lz.grupo(960, y, 0.9 + 0.1 * k_in):
        with lz.grupo(-960, -y):
            for i, (w, aw, kk) in enumerate(zip(c["ws"], anchos, kks)):
                dicha = t >= w["s"] - 0.03
                col = AMARILLO if i == idx else (BLANCO if dicha else (215, 215, 222))
                lz.texto(w["w"], x + aw / 2, y - (4 if i == idx else 0), px, "black", color=col, borde=NEGRO,
                         borde_px=borde, k=kk, temblor=0.0, capa=2)
                x += aw + esp
    return True


# ------------------------------------------------------------ progreso 1..10
ITEMS = [e for e in TL["escenas"] if "num" in e]


def dibujar_progreso(lz, t):
    if not ITEMS or t < ITEMS[0]["t0"] - 0.2:
        return False
    actual = 0
    for e in ITEMS:
        if t >= e["t0"]:
            actual = e["num"]
    fin = ITEMS[-1]["t1"]
    ancho, gap = 34, 8
    x0 = 960 - (10 * ancho + 9 * gap) / 2
    for i in range(10):
        n = i + 1
        x = x0 + i * (ancho + gap)
        if n < actual or t >= fin:
            col = AMARILLO
        elif n == actual:
            col = tuple(int(v) for v in np.array(AMARILLO) * (0.75 + 0.25 * env_bombo(t)))
        else:
            col = (70, 70, 90)
        lz.forma(rect_red(x, 16, ancho, 14, 7), col, NEGRO, 3, seed=500 + i, temblor=0.3, capa=2)
    return True


# ------------------------------------------------------------ cuadro completo
class Renderizador:
    def __init__(self):
        self.esc = [CLASES[e["id"]](e, i) for i, e in enumerate(TL["escenas"])]
        self.por_id = {e.id: e for e in self.esc}
        self.lz = Lienzo()

    def escena_en(self, t):
        for e in self.esc:
            if e.t0 <= t < e.t1:
                return e
        return self.esc[-1]

    def cuadro(self, t):
        img = None
        for k, tr in enumerate(TL["transiciones"]):
            if tr["tipo"] == "continua":      # plano secuencia: no hay corte que mezclar
                continue
            if tr["t0"] <= t < tr["t1"]:
                p = (t - tr["t0"]) / (tr["t1"] - tr["t0"])
                A = self.por_id[tr["de"]].render(self.lz, t)
                B = self.por_id[tr["a"]].render(self.lz, t)
                img = E.TRANSICIONES[tr["tipo"]](A, B, p, seed=k * 17 + 3)
                break
        if img is None:
            img = self.escena_en(t).render(self.lz, t)
        img = E.acabado(img, int(t * 10))
        self.lz.nuevo(t)
        a = dibujar_progreso(self.lz, t)
        b = dibujar_subtitulos(self.lz, t)
        if a or b:
            img = componer(img, self.lz.resolver(), estilo=False)
        return a_uint8(np.clip(img, 0, 1))


# ------------------------------------------------------------ paralelo
_R = None


def _init():
    global _R
    cv2.setNumThreads(1)
    _R = Renderizador()


def _trozo(args):
    i0, i1, ruta = args
    if os.path.exists(ruta) and os.path.getsize(ruta) > 1000:
        return ruta, 0.0
    tmp = ruta + ".tmp.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-g", "60", "-threads", "2", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(i0, i1):
        p.stdin.write(_R.cuadro(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg falló en {ruta}")
    os.replace(tmp, ruta)
    return ruta, time.time() - t0


def procesos_seguros(pedidos, gb_por_proceso=1.5):
    """Limita los procesos a la memoria realmente libre (cada proceso de render usa ~1.5 GB)."""
    try:
        import psutil
        libre = min(psutil.virtual_memory().available, psutil.virtual_memory().available + psutil.swap_memory().free)
        cabe = max(2, int(libre / 1e9 / gb_por_proceso))
    except Exception:
        return pedidos
    if cabe < pedidos:
        print(f"memoria libre {libre / 1e9:.1f} GB: se usan {cabe} procesos en lugar de {pedidos}")
    return min(pedidos, cabe)


def video(procs=13, tam=90):
    procs = procesos_seguros(procs)
    os.makedirs("segmentos", exist_ok=True)
    os.makedirs("salida", exist_ok=True)
    tareas = [(i, min(i + tam, NFRAMES), f"segmentos/seg_{i // tam:04d}.mp4") for i in range(0, NFRAMES, tam)]
    t0 = time.time()
    hechos = 0
    with Pool(procs, initializer=_init) as pool:
        for ruta, dt in pool.imap_unordered(_trozo, tareas):
            hechos += 1
            print(f"[{hechos}/{len(tareas)}] {ruta} {dt:.0f}s  (transcurrido {time.time() - t0:.0f}s)", flush=True)
    with open("segmentos/lista.txt", "w") as f:
        for _, _, ruta in tareas:
            f.write(f"file '{os.path.basename(ruta)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "segmentos/lista.txt",
                    "-c", "copy", "salida/video_sin_audio.mp4"], check=True)
    print("listo: salida/video_sin_audio.mp4", f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    modo = sys.argv[1]
    if modo == "prueba":
        R = Renderizador()
        os.makedirs("previews", exist_ok=True)
        tiles = []
        for x in sys.argv[2:]:
            t = float(x)
            t0 = time.time()
            im = R.cuadro(t)
            print(f"{t:.2f}s {1000 * (time.time() - t0):.0f} ms")
            cv2.imwrite(f"previews/cuadro_{t:07.2f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
            sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
            cv2.putText(sm, f"{t:.2f}", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(sm, f"{t:.2f}", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            tiles.append(sm)
        while len(tiles) % 3:
            tiles.append(np.zeros_like(tiles[0]))
        hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
        cv2.imwrite("previews/hoja_render.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    elif modo == "video":
        procs = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 13
        video(procs)
