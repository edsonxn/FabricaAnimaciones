# -*- coding: utf-8 -*-
"""Escribe youtube.json: capítulos desde los puestos de efectos.py (anclas resueltas en timeline.json), fuentes (el gancho
promete «las fuentes, en la descripción») y créditos de gameplay (salida/creditos.txt, `fab.py <v> fuentes`). Máx. 5 000 bytes."""
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")
t = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
fx = open(os.path.join(AQUI, "efectos.py"), encoding="utf-8").read()


def _n(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in w if not unicodedata.combining(c)))


pal = [(_n(w["w"]), w["s"]) for e in t["escenas"] for fr in e["frases"] for w in fr["words"]]
pal = [p for p in pal if p[0]]


def ancla(txt):
    txt, _, vez = txt.partition("#")
    vez, visto = int(vez or 1), 0
    ag = [_n(w) for w in txt.split() if _n(w)]
    for i in range(len(pal) - len(ag) + 1):
        if all(pal[i + j][0] == ag[j] for j in range(len(ag))):
            visto += 1
            if visto == vez:
                return pal[i][1]
    raise SystemExit(f"no encuentro «{txt}»")


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


caps = ["0:00 Expediente 141: lo que MW4 te escondió"]
for en, n, tit in re.findall(r'puesto\("([^"]+)", (\d+), "([^"]+)"', fx):
    caps.append(f"{mmss(ancla(en) - .3)} #{n} {tit}")
caps.append(f"{mmss(ancla('Si quieres el siguiente'))} Tu turno")

F = ["Captain Eggcellent — https://youtu.be/ZOxTN7cmPzg",
     "ThatWasAwesome — https://youtu.be/PijkhLoNBiI",
     "Inkslasher — https://youtu.be/ViJ6PJqh5As",
     "VANDELEY — https://youtu.be/7xrBR402DxA",
     "ICE KING — https://youtu.be/OMjaaua6-Dg",
     "Vandal — https://youtu.be/tarSw_pzbWk",
     "MDMarqués — https://youtu.be/u--bVYZmMo4",
     "TiHOME — https://youtu.be/MNrtzZlFnKw",
     "TheGamingRevolution (Soap) — https://youtu.be/RolY8zrM6kY"]
cred = ""
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    lin = [l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]
    cred = " · ".join(l for l in lin if not l.lower().startswith("gameplay usado"))

d = ("Le disparas a un cuadro en Corea del Norte y tu propio compañero te ejecuta. Una tele que nadie mira tiene una programación "
     "entera inventada. Y el secreto más grande del juego está después de los créditos. Estos son los 25 secretos que Modern Warfare 4 "
     "te escondió, comprobados uno por uno.\n\nCAPÍTULOS\n" + "\n".join(caps) +
     "\n\nFUENTES (los detalles se comprobaron en varios videos y en el juego):\n" + "\n".join(F) +
     "\nLo que el juego no confirma lo decimos como pregunta."
     "\n\nMÚSICA Y SONIDO: Call of Duty: Modern Warfare 4 Original Soundtrack — Stephen Barton y Jason Graves (Lakeshore Records). "
     "Audio del juego: Infinity Ward / Activision.")
pie = "\n\n#modernwarfare4 #callofduty #mw4"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
lim = 4700
def _b(x):
    return len(x.encode("utf-8"))
if _b(d) + _b(gp) + _b(pie) > lim:        # YouTube cuenta bytes (5 000), no caracteres: los acentos suman
    while _b(d) + _b(gp) + _b(pie) > lim - 40 and " · " in gp:
        gp = gp.rsplit(" · ", 1)[0]
    gp += " y más creadores. Gracias a todos."
yt = dict(titulo="Los 25 SECRETOS que Modern Warfare 4 te escondió",
          titulos_alternativos=["25 secretos de Modern Warfare 4 que no viste en la campaña",
                                "Modern Warfare 4 te esconde esto: 25 secretos de Infinity Ward"],
          descripcion=d + gp + pie,
          etiquetas=["modern warfare 4", "mw4", "call of duty modern warfare 4", "secretos modern warfare 4", "easter eggs mw4",
                     "modern warfare 4 secretos", "call of duty secretos", "capitán price", "gaz", "kate laswell",
                     "modern warfare 4 final", "call of duty en español", "expediente 141"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg",
          subtitulos="salida/Los_25_SECRETOS_que_Modern_Warfare_4_te_escondio.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(_b(yt["descripcion"]), "bytes;", len(caps), "capítulos;", caps[1], "…", caps[-1])
