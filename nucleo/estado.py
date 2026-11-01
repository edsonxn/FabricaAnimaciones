# -*- coding: utf-8 -*-
"""Estado de los videos para retomar el trabajo en una conversación nueva sin leer el proyecto entero.

  python fab.py estado             tabla de todos los videos (etapas deducidas de los archivos + líneas de ESTADO.md)
  python fab.py estado <video>     ESTADO.md de ese video + etapas + los archivos .py tocados más recientemente
  python fab.py continuar <texto>  «continúa el video …»: encuentra el video por nombre, título o alias (p. ej. «las 1200») y
                                   dice qué TRAMO sigue según la sección «## Sesiones» de su ESTADO.md (protocolo: docs/sesiones.md)
  python fab.py continuar          videos con tramos pendientes

Cada video tiene `videos/<v>/ESTADO.md` (plantilla en videos/_plantilla/ESTADO.md). Las líneas `- canal:`, `- etapa:` y
`- siguiente:` de su cabecera son las que se muestran en la tabla; el resto es libre (≤ 60 líneas)."""
import glob
import os
import re
import sys
import time
import unicodedata

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


# ====================================================================== videos en tramos (docs/sesiones.md)
_VACIAS = {"el", "la", "los", "las", "de", "del", "video", "videos", "continua", "continúa", "sigue", "con", "y", "a", "en", "un", "una"}


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s.replace(".", "").replace("_", " "))


def sesiones(texto):
    """Sección «## Sesiones» de un ESTADO.md -> (alias, leer, filas[(n, tramo, estado, nota)], texto_de_la_seccion)."""
    m = re.search(r"^## Sesiones.*?$(.*?)(?=^## |\Z)", texto, re.M | re.S)
    if not m:
        return None
    sec = m.group(0).rstrip()
    alias = re.search(r"^- alias:\s*(.*)$", sec, re.M)
    leer = re.search(r"^- leer al empezar:\s*(.*)$", sec, re.M)
    filas = []
    for ln in sec.splitlines():
        if ln.startswith("|") and not re.match(r"^\|\s*[-#:]", ln):
            c = [x.strip() for x in ln.strip("|").split("|")]
            if len(c) >= 3 and c[0] and c[0][0].isdigit():
                filas.append((c[0], c[1], c[2], c[3] if len(c) > 3 else ""))
    return (alias.group(1).strip() if alias else "", leer.group(1).strip() if leer else "", filas, sec)


def _hecho(estado):
    return "✅" in estado or estado.lower().startswith(("hecho", "listo", "ok"))


def sin_registrar(carpeta, max_n=10):
    """Archivos del video más nuevos que su ESTADO.md: trabajo de una sesión que se cortó (tokens agotados o cambio de cuenta)
    antes de anotarlo. Devuelve (total, [(mtime, ruta relativa)]) de más nuevo a más viejo."""
    try:
        t0 = os.path.getmtime(os.path.join(carpeta, "ESTADO.md")) + 60
    except OSError:
        return 0, []
    nuevos = []
    for pat in ("*.py", "*.md", "*.json", os.path.join("previews", "*.jpg"), os.path.join("previews", "*.mp4"),
                os.path.join("salida", "*.mp4")):
        for f in glob.glob(os.path.join(carpeta, pat)):
            if os.path.basename(f) != "ESTADO.md" and os.path.getmtime(f) > t0:
                nuevos.append((os.path.getmtime(f), os.path.relpath(f, carpeta)))
    nuevos.sort(reverse=True)
    return len(nuevos), nuevos[:max_n]


def continuar(texto):
    q = [w for w in _norm(texto).split() if w not in _VACIAS]
    cands = []
    for v in sorted(os.listdir(VIDEOS)):
        c = os.path.join(VIDEOS, v)
        if v.startswith("_") or not os.path.isdir(c):
            continue
        t = _leer(os.path.join(c, "ESTADO.md"))
        ses = sesiones(t)
        pajar = _norm(v + " " + (t.splitlines()[0] if t else "") + " " + (ses[0] if ses else ""))
        pal = pajar.split()
        if q and all(any(p.startswith(w) or w in p for p in pal) for w in q):
            cands.append((v, t, ses))
    if not q:
        print("Videos con tramos pendientes (di «continúa el video <nombre>»):")
        for v in sorted(os.listdir(VIDEOS)):
            t = _leer(os.path.join(VIDEOS, v, "ESTADO.md"))
            ses = sesiones(t) if t else None
            if ses and any(not _hecho(f[2]) for f in ses[2]):
                hechos = sum(_hecho(f[2]) for f in ses[2])
                sig = next(f for f in ses[2] if not _hecho(f[2]))
                print(f"  {v:22} {hechos}/{len(ses[2])} tramos · siguiente: #{sig[0]} {sig[1]}" + (f"  (alias: {ses[0]})" if ses[0] else ""))
        return
    if not cands:
        sys.exit(f"No encontré ningún video para «{texto}». Mira `python fab.py estado` y usa el nombre de la carpeta.")
    exacto = [c for c in cands if _norm(c[0]).split() == q]
    if len(cands) > 1 and len(exacto) == 1:
        cands = exacto
    if len(cands) > 1:
        print(f"Varios videos encajan con «{texto}»: " + ", ".join(c[0] for c in cands) + ". Pregunta al usuario cuál.")
        return
    v, t, ses = cands[0]
    f = campos(t)
    print(f"== Retomar videos/{v} ==")
    for k in ("canal", "estilo", "etapa", "siguiente"):
        if f.get(k):
            print(f"- {k}: {f[k]}")
    n_nuevos, nuevos = sin_registrar(os.path.join(VIDEOS, v))
    if n_nuevos:
        print(f"\n⚠ TRABAJO SIN REGISTRAR: {n_nuevos} archivo(s) más nuevos que el ESTADO.md (¿la sesión anterior se cortó por tokens\n"
              "  o cambio de cuenta antes de anotarlo?). Más reciente primero:")
        for mt, rel in nuevos:
            print(f"    {time.strftime('%d-%b %H:%M', time.localtime(mt))}  {rel}")
        print("  Antes de seguir, CONCILIA: py_compile de los .py nuevos, mira las hojas de previews/ más recientes, grep de lo que\n"
              "  registran escenas.py/guion.py, y anota en el ESTADO.md lo que ya existe (docs/sesiones.md §6). No rehagas lo hecho.")
    if not ses:
        print("\n(Su ESTADO.md no tiene sección «## Sesiones»: lee el ESTADO.md entero, haz el plan de tramos (docs/sesiones.md),\n"
              " enséñalo al usuario para que elija y anótalo antes de empezar.)")
        return
    alias, leer, filas, sec = ses
    print("\n" + sec)
    pend = [x for x in filas if not _hecho(x[2])]
    if not pend:
        print("\nTodos los tramos están hechos: revisa «siguiente» arriba (subida/publicación) o pregunta al usuario.")
        return
    n, tramo, est, nota = pend[0]
    print(f"\n>>> TRAMO QUE SIGUE: #{n} · {tramo}" + (f"  ({est})" if est else "") + (f" — {nota}" if nota else ""))
    print(f">>> Lee al empezar: videos/{v}/ESTADO.md" + (f" + {leer}" if leer else "") + "  (nada más; el núcleo solo con grep)")
    print(">>> Al terminar el tramo (o si te quedas sin margen): marca la fila (✅ fecha · nota, o ◐ parcial: qué falta), actualiza\n"
          "    «- etapa:» y «- siguiente:», añade lecciones no obvias y di al usuario: «En una conversación nueva escribe: continúa el\n"
          f"    video {alias.split(',')[0].strip() if alias else v}».")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "continuar":
        continuar(" ".join(sys.argv[2:]))
    else:
        uno(sys.argv[1]) if len(sys.argv) > 1 else tabla()
