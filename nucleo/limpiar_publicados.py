# -*- coding: utf-8 -*-
"""Libera disco en los videos que YA son públicos en YouTube (22-oct-2026).

  python fab.py limpiar --publicados            simulación: qué se borraría y cuánto libera
  python fab.py limpiar --publicados --borrar   lo borra de verdad (sin papelera) y lo anota en el registro

Público = en canales/<alias>.json → publicados tiene `id` y es «public» o su fecha
(publicado / programado / publicar) ya pasó. Los subidos a futuro y las reservas privadas no se tocan.
Borra: videos (.mp4 .webm .mkv .mov .m4a .avi) en cualquier carpeta y los .wav fuera de voz/
(mezclas de audio/). Conserva: código, guion, ESTADO, timeline, imágenes, .srt, Lyria .mp3,
JSON/TXT y las tomas de voz .wav (pagadas; sirven para remontajes y Shorts).
"""
import datetime
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS = os.path.join(RAIZ, "videos")
VIDEO_EXT = {".mp4", ".webm", ".mkv", ".mov", ".m4a", ".avi"}
REGISTRO = r"E:\FabricaAnimaciones\_limpieza_publicados.txt"


def publicos():
    ahora = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M")
    pub = {}
    for f in glob.glob(os.path.join(RAIZ, "canales", "*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for p in (d.get("publicados") or []) if isinstance(d, dict) else []:
            v = p.get("video")
            if not (v and p.get("id")):
                continue
            fecha = p.get("publicado") or p.get("programado") or p.get("publicar") or ""
            if p.get("visibilidad") == "public" or (fecha and fecha <= ahora):
                pub[v] = (os.path.basename(f)[:-5], fecha)
    return pub, ahora


def pesados(video):
    """(ruta, bytes) de lo que se borra; sigue las junctions a E:."""
    base = os.path.join(VIDEOS, video)
    for r, _ds, fs in os.walk(base, followlinks=True):
        top = os.path.relpath(r, base).split(os.sep)[0]
        for x in fs:
            ext = os.path.splitext(x)[1].lower()
            if ext in VIDEO_EXT or (ext == ".wav" and top != "voz"):
                p = os.path.join(r, x)
                yield p, os.path.getsize(p)


def main():
    borrar = "--borrar" in sys.argv
    pub, ahora = publicos()
    total, log = 0, []
    for v in sorted(pub):
        if not os.path.isdir(os.path.join(VIDEOS, v)):
            continue
        archivos = list(pesados(v))
        sv = sum(s for _p, s in archivos)
        if not sv:
            continue
        for p, s in archivos:
            log.append(f"{s / 1e6:10.1f} MB  {p}")
            if borrar:
                os.remove(p)
        total += sv
        print(f"{sv / 1e9:6.2f} GB  {v}  ({pub[v][0]}, {pub[v][1] or 'sin fecha'})")
    print(f"TOTAL {total / 1e9:.1f} GB en {len(log)} archivos de {len(pub)} videos públicos",
          "— BORRADO" if borrar else "— simulación (añade --borrar para hacerlo)")
    if borrar and log:
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write(f"\n## {ahora} UTC — {total / 1e9:.1f} GB\n" + "\n".join(log) + "\n")
        print(f"Registro: {REGISTRO}")


if __name__ == "__main__":
    main()
