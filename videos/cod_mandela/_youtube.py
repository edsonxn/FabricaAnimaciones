# -*- coding: utf-8 -*-
"""Escribe youtube.json: capítulos desde los puestos de efectos.py (cod_mandela) (anclas resueltas en timeline.json), fuentes (el gancho
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


caps = ["0:00 Expediente 141: tu memoria contra el juego"]
for en, n, tit in re.findall(r'puesto\("([^"]+)", (\d+), "([^"]+)"', fx):
    caps.append(f"{mmss(ancla(en) - .3)} #{n} {tit}")
caps.append(f"{mmss(ancla('Expediente cerrado'))} Tu turno")

F = ["Wiki de Call of Duty (transcripciones de Going Dark, Clean House, Loose Ends, Game Over, Breaking Point; Juggernog, Origins, Shadows of Evil) — https://callofduty.fandom.com",
     "Know Your Meme: Bravo Six, Going Dark · Ramirez, Do Everything! · Press F to Pay Respects — https://knowyourmeme.com",
     "Charlie Intel: el letrero de Standoff (27-jul-2021) — https://www.charlieintel.com/black-ops-cold-war-standoff-map-change-causes-big-debate/117742/",
     "Video de Standoff de 2015 — https://youtu.be/E6rpc8lIqFk",
     "Tráiler oficial de Modern Warfare (2019) — https://youtu.be/bH1lHCirCGI",
     "Fellow (los efectos Mandela que recopiló la comunidad) — https://youtu.be/MUHIbSFqEyg"]
cred = ""
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    lin = [l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]
    cred = " · ".join(l for l in lin if not l.lower().startswith("gameplay usado"))

d = ("Un letrero que miles juraron que era nuevo. Una botella que nunca dijo lo que leías. Una frase de Price que estás seguro de "
     "haber oído jugando. Estos son los 20 efectos Mandela más raros de Call of Duty: lo que recuerdas contra lo que de verdad hay en el "
     "juego, comprobado en pantalla.\n\nCAPÍTULOS\n" + "\n".join(caps) +
     "\n\nFUENTES:\n" + "\n".join(F) +
     "\n\nMÚSICA Y SONIDO: bandas sonoras oficiales de Call of Duty 4 (Harry Gregson-Williams y Stephen Barton), Modern Warfare 2 "
     "(Lorne Balfe y Hans Zimmer), Modern Warfare 3 (Brian Tyler) y Black Ops (Sean Murray); «115» de Kevin Sherwood y Elena Siegman. "
     "Audio del juego: Infinity Ward, Treyarch, Sledgehammer / Activision.")
pie = "\n\n#callofduty #efectomandela #codzombies"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
lim = 4700
def _b(x):
    return len(x.encode("utf-8"))
if _b(d) + _b(gp) + _b(pie) > lim:        # YouTube cuenta bytes (5 000), no caracteres: los acentos suman
    while _b(d) + _b(gp) + _b(pie) > lim - 40 and " · " in gp:
        gp = gp.rsplit(" · ", 1)[0]
    gp += " y más creadores. Gracias a todos."
yt = dict(titulo="Los 20 EFECTOS MANDELA más raros de Call of Duty",
          titulos_alternativos=["20 cosas de Call of Duty que recuerdas MAL", "Call of Duty: 20 recuerdos que nunca pasaron"],
          descripcion=d + gp + pie,
          etiquetas=["call of duty", "efecto mandela", "efecto mandela call of duty", "cod zombies", "juggernog", "bravo six going dark",
                     "press f to pay respects", "ramirez haz de todo", "standoff black ops 2", "black ops 2", "modern warfare 2",
                     "capitán price", "call of duty en español", "expediente 141"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg",
          subtitulos="salida/Los_20_EFECTOS_MANDELA_mas_raros_de_Call_of_Duty.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(_b(yt["descripcion"]), "bytes;", len(caps), "capítulos;", caps[1], "…", caps[-1])
