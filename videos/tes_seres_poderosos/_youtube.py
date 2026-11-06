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
nom.update(intro="¿Quién es el más poderoso de Tamriel?", voces="El marcador de las siete voces", cr1="Correo: el posh",
           ag1="Gracias por comentar", dato="El dato del Humano tras el Telón", campana="Un dato", cierre="El podio y vota la voz")
caps = []
for e in t["escenas"]:
    if e["id"] in ("campana",):
        continue
    s = int(round(e["t0"]))
    caps.append(f"{s // 60}:{s % 60:02d} {nom.get(e['id'], e['id'])}")
import itertools
F = list(dict.fromkeys(re.findall(r"https://\S+", open(os.path.join(AQUI, "_investigacion_ranking.md"), encoding="utf-8").read())))
cred = " · ".join(dict.fromkeys(v["canal"] for k, v in json.load(open(os.path.join(AQUI, "fuentes.json"), encoding="utf-8")).items()
                               if k.startswith("scene-") and isinstance(v, dict) and v.get("canal")))   # sin creditos.txt: canales de fuentes.json
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    cred = " · ".join(l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip())
N = "\n"
d = ("Un nigromante que quiso ser dios, un dragón que se come el mundo, un gólem de latón que conquistó un continente… y alguien que "
     "está soñando todo esto. Estos son los 20 seres más poderosos de The Elder Scrolls, del mortal al Soñador: Mannimarco, Divayth Fyr, Miraak, "
     "Pelinal, Dagoth Ur, Vivec, Alduin, el Sangre de Dragón, Talos, el Numidium, Molag Bal, Mehrunes Dagon, Sheogorath, Hermaeus Mora, Magnus, "
     "Akatosh, Lorkhan, Padomay, Anu y el Godhead. Cada dato comprobado en UESP." + N + N +
     "Las SIETE VOCES se pelean el ranking: Johnny, Edoardo, Hope, José, Mario, MariCarmen y el Profeta, que ganó vuestra votación de Sentinel y "
     "hoy se queda con el top seis. ¿Cuál se queda en el canal? Vota en los comentarios con un nombre. (El Humano tras el Telón da UN dato.)" + N + N +
     "Gracias a @saidavalera403, @amadeoamaya7606 y @alleyva por votar, y a @krisstianblackgao1726 por acordarse del Humano." + N + N +
     "CAPÍTULOS" + N + N.join(caps) + N + N +
     "Gracias a todos los que comentan: leemos todos los comentarios, los que nos felicitan y los que nos corrigen." + N + N +
     "FUENTES (cada dato, con su enlace):" + N + N.join(F) +
     N + "NOTA: el ranking es nuestro; lo que el lore no confirma lo decimos como teoría o leyenda." + N + N +
     "VIDEO RECOMENDADO: ¿Qué pasó con los DWEMER? Los 20 secretos de su desaparición → https://youtu.be/b0iLKv6r2Tw" + N + N +
     "MÚSICA: The Elder Scrolls IV: Oblivion y III: Morrowind (Jeremy Soule) — Bethesda Softworks / ZeniMax.")
pie = N + N + "#elderscrolls #skyrim #lore"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
def _cabe(d, gp, pie, tope=4850):
    """YouTube mide BYTES (máx. 5 000): deja hasta 30 fuentes (las primeras, las de los datos clave), luego recorta los créditos
    de gameplay y, si aún no cabe, más fuentes."""
    b = lambda x: len(x.encode("utf-8"))
    cab, resto = d.split("FUENTES (cada dato, con su enlace):\n", 1)
    enl, cola = resto.split("\nNOTA:", 1)
    enl = enl.split("\n")
    junta = lambda: cab + "FUENTES (cada dato, con su enlace):\n" + "\n".join(enl) + "\nNOTA:" + cola
    while len(enl) > 30 and b(junta() + gp + pie) > tope:
        enl.pop()
    while b(junta() + gp + pie) > tope and " · " in gp:
        gp = gp.rsplit(" · ", 1)[0] + ". Gracias a todos los creadores."
        gp = gp.replace(". Gracias a todos los creadores.. Gracias", ". Gracias")
    while enl and b(junta() + gp + pie) > tope:
        enl.pop()
    return junta() + gp + pie


yt = dict(titulo="Los 20 seres más PODEROSOS de Tamriel",
          titulos_alternativos=["Los 20 seres más PODEROSOS de The Elder Scrolls, del mortal al Soñador",
                                "¿Quién es el MÁS PODEROSO de Tamriel? 20 seres, de Mannimarco al Soñador"],
          descripcion=_cabe(d, gp, pie),
          etiquetas=["seres mas poderosos de tamriel", "el mas poderoso de elder scrolls", "elder scrolls lore", "skyrim lore", "lore en español",
                     "principes daedricos", "akatosh", "lorkhan", "alduin", "talos", "numidium", "dagoth ur", "vivec", "mannimarco", "miraak",
                     "hermaeus mora", "sheogorath", "anu padomay", "godhead", "chim", "cronicas de tamriel"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_seres_poderosos.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"].encode("utf-8")), "bytes;", len(caps), "capítulos;", caps[1], caps[-2])
