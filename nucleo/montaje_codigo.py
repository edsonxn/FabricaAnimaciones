# -*- coding: utf-8 -*-
"""MONTAJE de los videos dibujados por código (pedido del usuario, 20-oct-2026: «la vista previa tarda mucho y no se ve bien;
quiero el montaje como en Warcraft y Tamriel, con lo que lleva construido»).

El «🎞 Montaje» del panel reproduce fluido cada escena de timeline.json con la voz y la música (o la mezcla) encima. De cada
escena usa, por orden: su «escena fluida» de la vista previa (previews/escena_<id>.mp4) o el borrador que deja este comando
en previews/montaje/<id>.mp4 (640x360, 12 fps, mudo: el panel pone el audio). Lo que aún no está dibujado sale como hueco y las
escenas del guion que todavía no tienen voz, en gris. Si el código cambia, el borrador viejo se sigue viendo (marcado ámbar)
hasta que se rehace.

  python fab.py <v> montaje                 dibuja las escenas sin borrador o con borrador viejo (las que no tienen escena fluida)
  python fab.py <v> montaje gancho arena    solo esas
  python fab.py <v> montaje --todo          todas, aunque tengan escena fluida
  opciones: --fps 12  --ancho 640  --procs 8
Avance en previews/montaje/progreso.json (el panel lo enseña). Corre en el proceso del video: no a la vez que la voz."""
import json
import os
import subprocess
import sys
import time
from multiprocessing import Pool

os.environ.setdefault("FAB_SS", "1")          # borrador: supersampling 1 (el MASTER no se toca)

import cv2  # noqa: E402
import numpy as np  # noqa: E402

import cache_escenas as CE  # noqa: E402

CARPETA = os.getcwd()
NUCLEO = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(CARPETA, "previews", "montaje")
INFO = os.path.join(DIR, "info.json")
PROG = os.path.join(DIR, "progreso.json")


def leer_info():
    try:
        with open(INFO, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _escribir(ruta, d):
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    os.replace(tmp, ruta)


def _trozo(args):
    import render as RN
    ts, ruta, ancho, alto, fps = args
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ancho}x{alto}",
                          "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt",
                          "yuv420p", "-g", str(fps), "-threads", "1", ruta], stdin=subprocess.PIPE)
    for t in ts:
        img = RN._R.cuadro(t)
        if img.shape[1] != ancho:
            img = cv2.resize(img, (ancho, alto), interpolation=cv2.INTER_AREA)
        p.stdin.write(np.ascontiguousarray(img).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    return len(ts)


def main(args):
    def opt(nombre, defecto):
        if nombre in args:
            i = args.index(nombre)
            v = args[i + 1]
            del args[i:i + 2]
            return int(v)
        return defecto
    fps, ancho, procs = opt("--fps", 12), opt("--ancho", 640), opt("--procs", 8)
    todo = "--todo" in args
    ids = [a for a in args if not a.startswith("--")]
    firma = CE.firma_codigo(CARPETA, NUCLEO)
    import render as RN
    from motor import W, H
    alto = int(round(H * ancho / W)) // 2 * 2
    fluidas = {e["id"] for e in CE.listar(CARPETA, NUCLEO) if e["estado"] == "vigente"}
    info = leer_info()
    pend = []
    for e in RN.TL["escenas"]:
        if ids and e["id"] not in ids:
            continue
        if not ids and not todo and e["id"] in fluidas:
            continue
        b = info.get(e["id"]) or {}
        ok = (b.get("firma") == firma and b.get("t0") == e["t0"] and b.get("t1") == e["t1"]
              and os.path.isfile(os.path.join(DIR, e["id"] + ".mp4")))
        if ids or not ok:
            pend.append(e)
    if not pend:
        print("montaje: todas las escenas ya tienen borrador o escena fluida al día")
        return
    os.makedirs(DIR, exist_ok=True)
    total = sum(int((e["t1"] - e["t0"]) * fps) for e in pend)
    hechos, t_ini = 0, time.time()
    prog = dict(pid=os.getpid(), t_ini=t_ini, total=total, hechos=0, escenas=[e["id"] for e in pend], escena=None)
    procs = RN.procesos_seguros(procs)
    print(f"montaje: {len(pend)} escenas, {total} cuadros a {ancho}x{alto} y {fps} fps con {procs} procesos")
    try:
        with Pool(procs, initializer=RN._init) as pool:
            for e in pend:
                prog.update(escena=e["id"], hechos=hechos)
                _escribir(PROG, prog)
                ts = [e["t0"] + k / fps for k in range(int((e["t1"] - e["t0"]) * fps))]
                tam = max(6, -(-len(ts) // procs))
                trozos = [(ts[a:a + tam], os.path.join(DIR, f"_{e['id']}_{a // tam:03d}.mp4"), ancho, alto, fps)
                          for a in range(0, len(ts), tam)]
                for n in pool.imap_unordered(_trozo, trozos):
                    hechos += n
                    prog["hechos"] = hechos
                    _escribir(PROG, prog)
                lista = os.path.join(DIR, f"_{e['id']}.txt")
                with open(lista, "w") as f:
                    f.writelines(f"file '{os.path.basename(r)}'\n" for _, r, *_ in trozos)
                tmp = os.path.join(DIR, f"_{e['id']}_tmp.mp4")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy",
                                "-movflags", "+faststart", tmp], check=True)
                os.replace(tmp, os.path.join(DIR, e["id"] + ".mp4"))
                for _, r, *_ in trozos:
                    os.remove(r)
                os.remove(lista)
                # miniatura de la escena para la línea de tiempo (cuadro del medio del borrador)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{(e['t1'] - e['t0']) / 2:.2f}", "-i",
                                os.path.join(DIR, e["id"] + ".mp4"), "-frames:v", "1", "-vf", "scale=240:-2", "-q:v", "5",
                                os.path.join(DIR, e["id"] + ".jpg")], check=False)
                info = leer_info()
                info[e["id"]] = dict(firma=firma, t0=e["t0"], t1=e["t1"], fps=fps, w=ancho, ts=int(time.time()))
                _escribir(INFO, info)
                print(f"  {e['id']}: listo ({hechos}/{total} cuadros, {time.time() - t_ini:.0f} s)", flush=True)
    finally:
        try:
            os.remove(PROG)
        except OSError:
            pass
    if CE.firma_codigo(CARPETA, NUCLEO) != firma:
        print("montaje: OJO, el código cambió mientras dibujaba; vuelve a correrlo para tener lo último")
    print(f"montaje: listo en {time.time() - t_ini:.0f} s → previews/montaje/ (panel: 🎞 Montaje)")


if __name__ == "__main__":
    main(sys.argv[1:])
