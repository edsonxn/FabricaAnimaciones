# -*- coding: utf-8 -*-
"""PARTE del canal Edsonxn («Jefe de Robots»): cifras reales de lo que hicieron los agentes, para el guion de cada semana.
Lee los transcritos de Claude Code línea por línea y solo CUENTA: nunca guarda texto de mensajes, comandos ni archivos.

  python nucleo/parte_semanal.py                 todo lo que hay
  python nucleo/parte_semanal.py 2026-10-24      desde esa fecha
  python nucleo/parte_semanal.py 2026-10-24 2026-10-30

Escribe canales/formula/edsonxn_parte.json. Resta la zona horaria: un día es un día en CDMX.
"""
import collections
import datetime as dt
import glob
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESIONES = os.path.expanduser("~/.claude/projects/C--FabricaAnimaciones")
SALIDA = os.path.join(RAIZ, "canales", "formula", "edsonxn_parte.json")
ZONA = dt.timedelta(hours=-6)
EDITAN = ("Edit", "Write", "NotebookEdit")
ORDENAN = ("Bash", "PowerShell")


def _fecha(s):
    try:
        return (dt.datetime.fromisoformat(s.replace("Z", "+00:00")) + ZONA).strftime("%Y-%m-%d")
    except (AttributeError, ValueError):
        return None


def _es_del_usuario(d, c):
    if d.get("isMeta") or d.get("isSidechain") or d.get("isCompactSummary"):
        return False
    if isinstance(c, str):
        return not c.lstrip().startswith("<")
    return isinstance(c, list) and any(b.get("type") == "text" and not b.get("text", "").lstrip().startswith("<") for b in c)


def contar(desde=None, hasta=None):
    t = collections.Counter()
    herramientas = collections.Counter()
    dias = collections.Counter()
    vistos = set()
    sesiones = set()
    ayudantes = set()
    archivos = glob.glob(os.path.join(SESIONES, "*.jsonl")) + glob.glob(os.path.join(SESIONES, "*", "subagents", "agent-*.jsonl"))
    for ruta in archivos:
        ayudante = "subagents" in ruta
        with open(ruta, encoding="utf-8", errors="ignore") as f:
            for linea in f:
                if '"timestamp"' not in linea[:4000] and '"timestamp"' not in linea:
                    continue
                try:
                    d = json.loads(linea)
                except ValueError:
                    continue
                dia = _fecha(d.get("timestamp"))
                if not dia or (desde and dia < desde) or (hasta and dia > hasta):
                    continue
                msg = d.get("message") or {}
                c = msg.get("content")
                if d.get("type") == "assistant":
                    (ayudantes if ayudante else sesiones).add(ruta)
                    mid = msg.get("id")
                    if mid and mid not in vistos:
                        vistos.add(mid)
                        u = msg.get("usage") or {}
                        t["tokens_salida"] += u.get("output_tokens", 0) or 0
                    for b in c if isinstance(c, list) else ():
                        if b.get("type") == "tool_use":
                            n = b.get("name", "?")
                            herramientas[n] += 1
                            t["acciones"] += 1
                            dias[dia] += 1
                            t["comandos"] += n in ORDENAN
                            t["ediciones"] += n in EDITAN
                            t["investigacion"] += n in ("WebSearch", "WebFetch")
                elif d.get("type") == "user":
                    if not ayudante and _es_del_usuario(d, c):
                        t["mensajes_del_jefe"] += 1
                    for b in c if isinstance(c, list) else ():
                        if b.get("type") == "tool_result" and b.get("is_error"):
                            t["fallos"] += 1
    return dict(desde=desde or min(dias, default=None), hasta=hasta or max(dias, default=None), sesiones=len(sesiones),
                ayudantes=len(ayudantes), dias_activos=len(dias), **t, dia_mas_activo=max(dias.items(), key=lambda x: x[1], default=None),
                herramientas=herramientas.most_common(12))


def commits(desde=None, hasta=None):
    a = ["git", "-C", RAIZ, "log", "--format=%ad", "--date=short"]
    fechas = [x for x in subprocess.run(a, capture_output=True, text=True).stdout.split()
              if (not desde or x >= desde) and (not hasta or x <= hasta)]
    return dict(commits=len(fechas), modulos_python=len(glob.glob(os.path.join(RAIZ, "nucleo", "*.py"))))


if __name__ == "__main__":
    desde = sys.argv[1] if len(sys.argv) > 1 else None
    hasta = sys.argv[2] if len(sys.argv) > 2 else None
    r = {**contar(desde, hasta), **commits(desde, hasta)}
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print(json.dumps(r, ensure_ascii=False, indent=2))
