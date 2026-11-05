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
nom.update(intro="Una raza entera, en un instante: nadie", voces="Ronda 2: el marcador de las siete voces", cr1="Correo: «yarl», no «jarl»", ag1="Gracias por comentar", cr2="Correo: la voz femenina",
           campana="Un dato", cr3="Correo: Kyrim", cierre="Tu turno: ¿qué les pasó? y vota la voz")
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
d = ("Una raza entera, con ciudades bajo tierra, máquinas de vapor y un dios de latón, desapareció en un solo instante. Sin tumbas. Solo sus "
     "máquinas, que siguen trabajando casi cuatro mil años después. Estos son 20 secretos de la desaparición de los dwemer que Skyrim te esconde, "
     "de por qué los llamas enanos al experimento de Arniel Gane, comprobados uno por uno en UESP.\n\n"
     "Ronda 2: vuelven las SIETE VOCES que compiten, ahora con el marcador real de vuestros votos: Johnny, Edoardo, Hope, José, Mario, MariCarmen "
     "y el Profeta. ¿Cuál se queda en el canal? Vota en los comentarios con un nombre. (El Humano tras el Telón, crítico n.º 1 del canal, hoy narra "
     "el número 6.)\n\n"
     "Gracias a @chuymoreno6820 por pedir este tema, y a @federicoherrera2105 por la corrección: se dice «yarl».\n\n"
     "CAPÍTULOS\n" + "\n".join(caps) +
     "\n\nGracias a todos los que comentan: leemos todos los comentarios, los que nos felicitan y los que nos corrigen.\n\n"
     "FUENTES (cada dato, con su enlace):\n" + "\n".join(F) +
     "\nNOTA: lo que el juego no confirma lo decimos como teoría."
     "\n\nVIDEO RECOMENDADO: Los 15 SECRETOS del teaser de The Elder Scrolls VI: Sentinel → https://youtu.be/TM5ivAWiF0o"
     "\n\nMÚSICA: The Elder Scrolls V: Skyrim y III: Morrowind (Jeremy Soule), The Elder Scrolls Online (Brad Derrick) — Bethesda Softworks / ZeniMax.")
pie = "\n\n#skyrim #dwemer #elderscrolls"
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


yt = dict(titulo="¿Qué pasó con los DWEMER? Los 20 secretos de su desaparición que Skyrim te esconde",
          titulos_alternativos=["Los DWEMER no murieron: 20 secretos de su desaparición en Skyrim", "Skyrim te deja repetir la desaparición de los DWEMER: 20 secretos"],
          descripcion=_cabe(d, gp, pie),
          etiquetas=["dwemer", "que paso con los dwemer", "desaparicion de los dwemer", "skyrim dwemer", "enanos skyrim", "blackreach", "arniel gane",
                     "kagrenac", "numidium", "falmer", "skyrim lore", "elder scrolls lore", "lore en español", "cronicas de tamriel", "skyrim secretos"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_dwemer_desaparicion.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"].encode("utf-8")), "bytes;", len(caps), "capítulos;", caps[1], caps[-2])
