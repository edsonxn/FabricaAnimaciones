# -*- coding: utf-8 -*-
"""Capítulos de YouTube desde timeline.json y los avisos de efectos.py."""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")
t = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
fx = open(os.path.join(AQUI, "efectos.py"), encoding="utf-8").read()
nom = {"p" + n: f"#{n} {s}" for n, s in re.findall(r'"Misión · número (\d+)", "([^"]+)"', fx)}
nom.update(intro="Las misiones que NO debes saltarte", cierre="Tu turno")
for e in t["escenas"]:
    s = int(round(e["t0"]))
    print(f"{s // 60}:{s % 60:02d} {nom[e['id']]}")
