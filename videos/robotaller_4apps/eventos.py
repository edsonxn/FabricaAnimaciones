# -*- coding: utf-8 -*-
"""Índice de eventos del Robotaller de cada sesión real (seq, hora, tipo, título) → capturas/eventos_<n>.txt, para elegir tramos en capturas.py.
  python eventos.py"""
import json
import os
import urllib.request

SES = {"altima": "30a418d2-", "apps": "fecd0d1d-", "ideas": "5023f72b-", "auto": "bd7d4bbf-"}
CARP = os.path.expanduser("~/.claude/projects/D--Escaner")


def sid(pref):
    return next(f[:-6] for f in os.listdir(CARP) if f.startswith(pref) and f.endswith(".jsonl"))


def todos(s):
    """Todos los eventos de la sesión (la API solo manda los 160 últimos): se leen con agente_vivo aquí mismo."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../nucleo"))
    import agente_vivo as AV
    return {e["seq"]: e for e in AV._sesion(s).eventos}


if __name__ == "__main__":
    os.makedirs("capturas", exist_ok=True)
    for n, p in SES.items():
        s = sid(p)
        vistos = todos(s)
        with open(f"capturas/eventos_{n}.txt", "w", encoding="utf-8") as f:
            f.write(f"# {n} {s}\n")
            for k in sorted(vistos):
                e = vistos[k]
                f.write(f"{k}\t{str(e.get('t', ''))[:19]}\t{e.get('tipo')}\t{str(e.get('titulo', ''))[:110]}\n")
        print(n, s, len(vistos), "eventos", min(vistos or [0]), "-", max(vistos or [0]))
