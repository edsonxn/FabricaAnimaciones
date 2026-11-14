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
nom.update(intro="Lo que esconde el teaser", voces="Siete voces compiten", cr1="Correo: crítica 1", ag1="Gracias por comentar", cr2="Correo: crítica 2",
           campana="Un dato", cr3="Correo: crítica 3", cierre="Tu turno: vota la voz")
caps = []
for e in t["escenas"]:
    if e["id"] in ("campana",):
        continue
    s = int(round(e["t0"]))
    caps.append(f"{s // 60}:{s % 60:02d} {nom.get(e['id'], e['id'])}")
import itertools
F = list(dict.fromkeys(re.findall(r"https://\S+", open(os.path.join(AQUI, "_investigacion.md"), encoding="utf-8").read())))
cred = " · ".join(dict.fromkeys(v["canal"] for k, v in json.load(open(os.path.join(AQUI, "fuentes.json"), encoding="utf-8")).items()
                               if k.startswith("scene-") and isinstance(v, dict) and v.get("canal")))   # sin creditos.txt: canales de fuentes.json
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    cred = " · ".join(l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip())
d = ("Ocho años después, Bethesda por fin le puso nombre: The Elder Scrolls VI: Sentinel. En un minuto de teaser hay una ciudad real, una reina "
     "nueva, una fecha exacta y una frase que podría deshacer lo que hiciste en Skyrim. Estos son 15 secretos del teaser, comprobados uno por uno.\n\n"
     "Hoy los cuentan SIETE VOCES que compiten entre ellas: Johnny, Edoardo, Hope, José, Mario, MariCarmen y el Profeta. "
     "¿Cuál se queda en el canal? Vota en los comentarios con un nombre. (Al Humano tras el Telón, crítico n.º 1 de este canal, no se le vota: él critica.)\n\n"
     "CAPÍTULOS\n" + "\n".join(caps) +
     "\n\nGracias a todos los que comentan: leemos todos los comentarios, los que nos felicitan y los que nos corrigen.\n\n"
     "FUENTES (cada dato, con su enlace):\n" + "\n".join(F) +
     "\nTeaser y video del 40 aniversario: Bethesda Softworks. Mapas: The Pocket Guide to the Empire, Daggerfall y ESO (UESP). Lo que Bethesda no ha "
     "confirmado lo decimos como teoría."
     "\n\nVIDEO RECOMENDADO: Las 15 armas más PODEROSAS de Skyrim → https://youtu.be/m6Pk4FLQGuc"
     "\n\nMÚSICA: The Elder Scrolls Online (Brad Derrick), The Elder Scrolls IV: Oblivion y III: Morrowind (Jeremy Soule) — Bethesda Softworks / ZeniMax.")
pie = "\n\n#skyrim #elderscrolls #tamriel"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
def _cabe(d, gp, pie, tope=4850):
    """YouTube mide BYTES (máx. 5 000): deja hasta 30 fuentes (las primeras, las de los datos clave), luego recorta los créditos
    de gameplay y, si aún no cabe, más fuentes."""
    b = lambda x: len(x.encode("utf-8"))
    cab, resto = d.split("FUENTES (cada dato, con su enlace):\n", 1)
    enl, cola = resto.split("\nTeaser y video del 40", 1)
    enl = enl.split("\n")
    junta = lambda: cab + "FUENTES (cada dato, con su enlace):\n" + "\n".join(enl) + "\nTeaser y video del 40" + cola
    while len(enl) > 30 and b(junta() + gp + pie) > tope:
        enl.pop()
    while b(junta() + gp + pie) > tope and " · " in gp:
        gp = gp.rsplit(" · ", 1)[0] + ". Gracias a todos los creadores."
        gp = gp.replace(". Gracias a todos los creadores.. Gracias", ". Gracias")
    while enl and b(junta() + gp + pie) > tope:
        enl.pop()
    return junta() + gp + pie


yt = dict(titulo="Los 15 SECRETOS del teaser de The Elder Scrolls VI: Sentinel",
          titulos_alternativos=["Elder Scrolls 6 se llama SENTINEL: 15 secretos del teaser", "El teaser de Elder Scrolls 6 esconde esto: 15 secretos"],
          descripcion=_cabe(d, gp, pie),
          etiquetas=["elder scrolls 6", "elder scrolls vi", "elder scrolls 6 sentinel", "sentinel", "the elder scrolls vi sentinel", "teaser elder scrolls 6",
                     "hammerfell", "elder scrolls 6 trailer", "skyrim", "todd howard", "elder scrolls lore", "lore en español", "cronicas de tamriel"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_sentinel_teaser.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"].encode("utf-8")), "bytes;", len(caps), "capítulos;", caps[1], caps[-2])
