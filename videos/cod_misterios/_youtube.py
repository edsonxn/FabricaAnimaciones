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


caps = ["0:00 Expediente 141: lo que nadie ha podido explicar"]
for en, n, tit in re.findall(r'puesto\("([^"]+)", (\d+), "([^"]+)"', fx):
    caps.append(f"{mmss(ancla(en) - .3)} #{n} {tit}")
caps.append(f"{mmss(ancla('Expediente cerrado'))} Expediente cerrado")

F = ["Wiki de Call of Duty (Private Eye, Russman, Kino der Toten, Hangar 18, Spectre, Mob of the Dead: cifrados, Alex Mason) — https://callofduty.fandom.com",
     "La escena restaurada del final de MW3 — https://youtu.be/De7Axarv12E",
     "MrRoflWaffles: el corazón de Der Eisendrache y el Morse de Blundell — https://youtu.be/TPSPqrS0gG0 · https://youtu.be/par2G9SZ0KY",
     "Reddit r/CODZombies: la solución del cifrado ADFGX (sep-2018) — https://www.reddit.com/r/CODZombies/comments/9cyws2/",
     "Rocket Sloth: el mensaje de Ironclad y el fantasma de Vacant — https://youtu.be/4lCfOU8MgkA · https://youtu.be/xEiWuwjTQZQ",
     "El video original del fantasma de Vacant (2008) — https://youtu.be/eW2lZ_G4gww",
     "Treyarch: Pawn Takes Pawn, la historia — https://youtu.be/TgQHWD2KYwY",
     "Lemponaut y CodeNamePizza (misterios de Zombies) — https://youtu.be/2M4ZknQZYJ0 · https://youtu.be/f5VZ19blWGs"]
cred = ""
p = os.path.join(AQUI, "salida", "creditos.txt")
if os.path.exists(p):
    lin = [l.strip() for l in open(p, encoding="utf-8").read().splitlines() if l.strip()]
    cred = " · ".join(l for l in lin if not l.lower().startswith("gameplay usado"))

d = ("Una cara que aparece medio segundo en Alcatraz y nadie sabe de quién es. Una voz que Treyarch cambió en dos días. Un corazón "
     "escondido tres años y medio. Un hombre de traje que lleva quince años dentro del disco de Modern Warfare 3. Estos son los 30 "
     "misterios y leyendas más raros de Call of Duty: unos resueltos leyendo el código del juego, otros todavía abiertos. Todo con el "
     "juego en pantalla.\n\nCAPÍTULOS\n" + "\n".join(caps) +
     "\n\nFUENTES:\n" + "\n".join(F) +
     "\n\nMÚSICA Y SONIDO: bandas sonoras oficiales de Call of Duty: Ghosts (David Buckley), Black Ops II (Jack Wall), Modern Warfare "
     "2019 e Infinite Warfare (Sarah Schachner) y «Abracadavre» de Kevin Sherwood (Ascension). Audio del juego: Infinity Ward, "
     "Treyarch, Sledgehammer / Activision.")
pie = "\n\n#callofduty #codzombies #misterios"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."
lim = 4700
def _b(x):
    return len(x.encode("utf-8"))
if _b(d) + _b(gp) + _b(pie) > lim:        # YouTube cuenta bytes (5 000), no caracteres: los acentos suman
    while _b(d) + _b(gp) + _b(pie) > lim - 40 and " · " in gp:
        gp = gp.rsplit(" · ", 1)[0]
    gp += " y más creadores. Gracias a todos."
yt = dict(titulo="Los 30 MISTERIOS más raros de Call of Duty",
          titulos_alternativos=["30 misterios de Call of Duty que NADIE ha resuelto", "Call of Duty: 30 secretos que siguen sin explicación"],
          descripcion=d + gp + pie,
          etiquetas=["call of duty", "misterios call of duty", "easter eggs call of duty", "cod zombies", "mob of the dead", "der eisendrache",
                     "shadows of evil", "samantha maxis", "reznov", "modern warfare 3", "warzone bunker 11", "fantasma de vacant",
                     "call of duty en español", "expediente 141"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg",
          subtitulos="salida/Los_30_MISTERIOS_mas_raros_de_Call_of_Duty.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(_b(yt["descripcion"]), "bytes;", len(caps), "capítulos;", caps[1], "…", caps[-1])
