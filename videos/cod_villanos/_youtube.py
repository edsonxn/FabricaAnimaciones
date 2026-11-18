# -*- coding: utf-8 -*-
"""Escribe youtube.json: capítulos desde los puestos de efectos.py (cod_villanos) (anclas resueltas en timeline.json), fuentes (el gancho
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


caps = ["0:00 Expediente 141: cómo murieron de verdad"]
for en, n, tit in re.findall(r'puesto\("([^"]+)", (\d+), "([^"]+)"', fx):
    caps.append(f"{mmss(ancla(en) - .3)} #{n} {tit}")
caps.append(f"{mmss(ancla('Expediente cerrado'))} Expediente cerrado")

F = ["Wiki de Call of Duty (fichas de cada villano y transcripciones de las misiones) — https://callofduty.fandom.com",
     "Perseus y la temporada 6 de Cold War — https://www.gamespot.com/articles/call-of-duty-season-6-cinematic-closes-out-the-black-ops-cold-war-storyline/1100-6497636/",
     "Mapamundi: NASA Visible Earth (Wikimedia Commons)"]
cred = ""
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    lin = [l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]
    cred = " · ".join(l for l in lin if not l.lower().startswith("gameplay usado"))

d = ("Uno murió a puñetazos en un callejón de Nueva York. Otro, colgado de un cable en Dubái. Otro sigue vivo aunque le "
     "dispararon con un Magnum. Y a uno lo viste morir con tus propios ojos... y el juego te mintió sobre quién lo mató. Estos son "
     "20 villanos de Call of Duty y cómo murieron REALMENTE, de World at War a Modern Warfare 4, con el juego en pantalla. "
     "Aviso: hay spoilers de Modern Warfare 4.\n\nCAPÍTULOS\n" + "\n".join(caps) +
     "\n\nFUENTES:\n" + "\n".join(F) +
     "\n\nMÚSICA Y SONIDO: bandas sonoras oficiales de Call of Duty 4, Modern Warfare 2 y 3, Black Ops, Black Ops II, Black Ops 6, "
     "Modern Warfare 2019, Infinite Warfare y WWII (Stephen Barton, Hans Zimmer, Lorne Balfe, Brian Tyler, Sean Murray, Jack Wall, "
     "Sarah Schachner, Wilbert Roget II). Audio del juego: Infinity Ward, Treyarch, Sledgehammer / Activision.")
pie = "\n\n#callofduty #villanos #makarov"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
lim = 4700
def _b(x):
    return len(x.encode("utf-8"))
if _b(d) + _b(gp) + _b(pie) > lim:        # YouTube cuenta bytes (5 000), no caracteres: los acentos suman
    while _b(d) + _b(gp) + _b(pie) > lim - 40 and " · " in gp:
        gp = gp.rsplit(" · ", 1)[0]
    gp += " y más creadores. Gracias a todos."
yt = dict(titulo="Cómo murió REALMENTE cada villano de Call of Duty",
          titulos_alternativos=["20 villanos de Call of Duty y cómo murieron DE VERDAD", "Call of Duty: así murió cada villano (no como recuerdas)"],
          descripcion=d + gp + pie,
          etiquetas=["call of duty", "villanos call of duty", "makarov", "muerte de makarov", "shepherd", "menendez", "steiner",
                     "reznov", "zakhaev", "graves", "modern warfare 4", "black ops", "call of duty en español", "expediente 141"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg",
          subtitulos="salida/Como_murio_REALMENTE_cada_villano_de_Call_of_Duty.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(_b(yt["descripcion"]), "bytes;", len(caps), "capítulos;", caps[1], "…", caps[-1])
