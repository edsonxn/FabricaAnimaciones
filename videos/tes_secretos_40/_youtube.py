# -*- coding: utf-8 -*-
"""Escribe youtube.json: capítulos desde timeline + avisos, fuentes UESP (se prometen en el gancho) y créditos. Máx. 5 000 caracteres."""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")
t = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
fx = open(os.path.join(AQUI, "efectos.py"), encoding="utf-8").read()
nom = {"p" + n: f"#{n} {s}" for n, s in re.findall(r'aviso\("[^"]+", "?(\d+)"?, "([^"]+)"', fx)}
nom["p40"] = "#40 La poción del arquero"
nom.update(intro="Lo que Skyrim te esconde", cierre="Tu turno")
caps = []
for e in t["escenas"]:
    s = int(round(e["t0"]))
    caps.append(f"{s // 60}:{s % 60:02d} {nom.get(e['id'], e['id'])}")
U = "https://en.uesp.net/wiki/"
F = ["Skyrim:Paarthurnax_(dragon)", "Skyrim:Esbern", "Lore:Cicero's_Journal_-_Volume_3", "Lore:Cicero's_Journal_-_Volume_2", "Skyrim:Brand-Shei",
     "General:Erik_West", "Lore:Thalmor_Dossier:_Ulfric_Stormcloak", "Lore:Thalmor_Dossier:_Esbern", "Lore:Jurgen_Windcaller", "Skyrim:Frostflow_Lighthouse",
     "Lore:Skorm_Snow-Strider's_Journal", "Skyrim:Unfinished_Quests", "Skyrim:Inaccessible_Cells", "Skyrim:Game_Jam", "Skyrim:Easter_Eggs"]
cred = ""
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    cred = " · ".join(l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip())
d = ("Llevas años jugando a Skyrim y sigue escondiéndote cosas. Una cárcel donde peleabas por tu libertad, un vendedor de Riften con pasado de novela, "
     "una sopa de cinco monedas que te da doce minutos de ataques poderosos, y un dragón en el que quizá no deberías confiar. Estos son 40 secretos, "
     "comprobados uno por uno.\n\nCAPÍTULOS\n" + "\n".join(caps) +
     "\n\nGracias a todos los que comentan: los leemos todos, y hoy corregimos un error que nos señalaron.\n\nFUENTES: The Unofficial Elder Scrolls Pages (UESP). Las principales:\n" +
     "\n".join(U + x.replace("'", "%27") for x in F) +
     "\nNombres en español e imágenes: The Elder Scrolls Wiki (Fandom) y UESP. Mapa: SR-map-Skyrim (UESP). Lo que el juego no confirma lo decimos como pregunta."
     "\n\nVIDEO RECOMENDADO: Las 25 misiones de Skyrim que NUNCA debes saltarte https://youtu.be/C16mqQHbK08"
     "\n\nMÚSICA Y SONIDO: The Elder Scrolls V: Skyrim Original Soundtrack — Jeremy Soule / Bethesda Softworks.")
pie = "\n\n#skyrim #elderscrolls #tamriel"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
if len(d) + len(gp) + len(pie) > 4600:        # YouTube cuenta bytes (5 000), no caracteres: los acentos suman
    gp = gp[:4600 - len(d) - len(pie) - 40].rsplit(" · ", 1)[0] + " y más creadores. Gracias a todos."
yt = dict(titulo="Los 40 SECRETOS de Skyrim que nadie te contó",
          titulos_alternativos=["40 secretos de Skyrim que no viste en cientos de horas", "Skyrim te esconde esto: 40 secretos que nadie te contó"],
          descripcion=d + gp + pie,
          etiquetas=["skyrim", "secretos de skyrim", "skyrim secretos", "skyrim curiosidades", "curiosidades skyrim", "paarthurnax", "cicerón skyrim",
                     "brand shei", "ulfric thalmor", "skyrim lore", "skyrim lore español", "elder scrolls", "skyrim en español", "cronicas de tamriel"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_secretos_40.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"]), "caracteres;", len(caps), "capítulos;", caps[1], caps[-2])
