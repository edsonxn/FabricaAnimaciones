# -*- coding: utf-8 -*-
"""Estado de los videos para retomar el trabajo en una conversación nueva sin leer el proyecto entero.

  python fab.py estado             tabla de todos los videos (etapas deducidas de los archivos + líneas de ESTADO.md)
  python fab.py estado <video>     ESTADO.md de ese video + etapas + los archivos .py tocados más recientemente

Cada video tiene `videos/<v>/ESTADO.md` (plantilla en videos/_plantilla/ESTADO.md). Las líneas `- canal:`, `- etapa:` y
`- siguiente:` de su cabecera son las que se muestran en la tabla; el resto es libre (≤ 60 líneas)."""
import glob
import os
import re
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS = os.path.join(RAIZ, "videos")


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8").read()
    except OSError:
        return ""


def campos(texto):
    """{clave: valor} de las líneas '- clave: valor' de la cabecera."""
    d = {}
    for m in re.finditer(r"^- (\w+):\s*(.*)$", texto, re.M):
        d.setdefault(m.group(1).lower(), m.group(2).strip())
    return d


def etapas(carpeta):
    """Banderas deducidas de los archivos: voz, tiempo, mezcla, MASTER, youtube.json."""
    j = lambda *p: os.path.join(carpeta, *p)
    guion = _leer(j("guion.py"))
    sin_voz = "SIN_VOZ = True" in guion
    voz = "-" if sin_voz else ("ok" if glob.glob(j("voz", "final", "*.wav")) else ("tomas" if os.path.isdir(j("voz", "cands")) else "no"))
    return dict(
        estilo=(re.search(r'^ESTILO_VISUAL\s*=\s*"(\w+)"', guion, re.M) or [None, "?"])[1],
        voz=voz,
        tiempo="ok" if os.path.exists(j("timeline.json")) else "no",
        mezcla="ok" if os.path.exists(j("audio", "final.wav")) else "no",
        master="ok" if glob.glob(j("salida", "*MASTER*.mp4")) else "no",
        yt="ok" if os.path.exists(j("youtube.json")) else "no",
    )


def _corto(s, n):
    return s if len(s) <= n else s[:n - 1] + "…"


def tabla():
    print(f"{'video':20} {'estilo':16} {'voz':5} {'tiem':4} {'mezc':4} {'MAST':4} {'yt':3} ESTADO.md (canal · etapa · siguiente)")
    for v in sorted(os.listdir(VIDEOS)):
        c = os.path.join(VIDEOS, v)
        if v.startswith("_") or not os.path.isdir(c):
            continue
        e = etapas(c)
        t = _leer(os.path.join(c, "ESTADO.md"))
        f = campos(t)
        resumen = " · ".join(x for x in (f.get("canal", ""), f.get("etapa", ""), f.get("siguiente", "")) if x) if t else "(sin ESTADO.md)"
        print(f"{v:20} {e['estilo']:16} {e['voz']:5} {e['tiempo']:4} {e['mezcla']:4} {e['master']:4} {e['yt']:3} {_corto(resumen, 150)}")


def uno(video):
    c = os.path.join(VIDEOS, video)
    if not os.path.isdir(c):
        sys.exit(f"No existe videos/{video}")
    e = etapas(c)
    print(f"[{video}] estilo={e['estilo']} voz={e['voz']} tiempo={e['tiempo']} mezcla={e['mezcla']} MASTER={e['master']} youtube.json={e['yt']}\n")
    t = _leer(os.path.join(c, "ESTADO.md"))
    print(t if t else "(sin ESTADO.md: créalo desde videos/_plantilla/ESTADO.md)")
    py = [p for p in glob.glob(os.path.join(c, "*.py")) if not os.path.basename(p).startswith("_parche")]
    py.sort(key=os.path.getmtime, reverse=True)
    print("\nArchivos .py tocados más recientemente (por dónde se quedó el trabajo):")
    for p in py[:8]:
        print(f"  {time.strftime('%d-%b %H:%M', time.localtime(os.path.getmtime(p)))}  {os.path.basename(p)}")


if __name__ == "__main__":
    uno(sys.argv[1]) if len(sys.argv) > 1 else tabla()
