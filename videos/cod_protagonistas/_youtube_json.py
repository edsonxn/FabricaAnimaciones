# -*- coding: utf-8 -*-
"""Genera youtube.json de cod_protagonistas (capítulos del timeline real, créditos de fuentes.json y de audio/ost/_catalogo.txt)."""
import glob
import json
import os

T = json.load(open("timeline.json", encoding="utf-8"))
t0 = {e["id"]: e["t0"] + e.get("pre", 0) for e in T["escenas"]}
CAP = [("intro", "Expediente 141: los protagonistas"), ("p20", "#20 Nick Reyes · Infinite Warfare"), ("p19", "#19 Logan Walker · Ghosts"),
       ("p18", "#18 Alex Keller · Modern Warfare 2019"), ("p17", "#17 Paul Jackson · Call of Duty 4"), ("p16", "#16 Al-Fulani · Call of Duty 4"),
       ("p15", "#15 Joseph Allen · Modern Warfare 2"), ("p14", "#14 Yuri · Modern Warfare 3"), ("p13", "#13 Case · Black Ops 6"),
       ("p12", "#12 Section · Black Ops 2 y 7"), ("p11", "#11 Roach y Ghost originales"), ("p10", "#10 Ghost del reinicio"),
       ("p09", "#9 Viktor Reznov"), ("p08", "#8 Soap original"), ("p07", "#7 Frank Woods"), ("p06", "#6 Bell · Cold War"),
       ("p05", "#5 Alex Mason"), ("p04", "#4 El jugador de Black Ops 3"), ("p03", "#3 Gaz · los dos"), ("p02", "#2 Soap del reinicio"),
       ("p01", "#1 Capitán Price · Modern Warfare 4"), ("cierre", "Expediente cerrado")]


def mmss(s):
    s = int(s)
    return f"{s // 60}:{s % 60:02d}"


caps = "\n".join(f"{'0:00' if k == 'intro' else mmss(t0[k])} {n}" for k, n in CAP)
F = json.load(open("fuentes.json", encoding="utf-8"))
vids = []
for k in sorted(F):
    v = F[k].get("video") if isinstance(F[k], dict) else None
    if v and v not in vids:
        vids.append(v)
gameplay = "{GP}"
desc = ("Price, Soap, Gaz, Ghost, Mason, Woods, Reznov: los manejaste a todos, y casi ninguno terminó como crees. Uno estaba muerto "
        "desde la segunda misión, otro murió de viejo con 104 años, y al capitán Price lo mataron en Modern Warfare 4. 20 protagonistas de "
        "Call of Duty y cómo acabó realmente cada uno, juego por juego, con la escena en pantalla.\n\nAVISO: spoilers de Modern Warfare 4 "
        "y Black Ops 7.\n\n¿Qué protagonista crees que merecía otro final? Escríbelo: los mejores comentarios salen en el siguiente expediente."
        "\n\nCAPÍTULOS\n" + caps +
        "\n\nFUENTES:\nWiki de Call of Duty (fichas de cada personaje y transcripciones de Operation Blood Storm, The Ghost Killer, Into "
        "the Furnace, Aftermath, The Coup, No Russian, Blood Brothers, Dust to Dust, Checkmate, Judgment Day, Loose Ends, Vorkuta, The Final "
        "Countdown, Suffer With Me, New World, Life, Counter Attack, Trojan Horse y Greater Good) — https://callofduty.fandom.com\n"
        "COD POD ep. 003 «Canonizing Black Ops Lore» (Treyarch, 10-oct-2024) y VentureBeat (9-jun-2024) sobre el canon de Bell y Alex Mason.\n\n"
        "MÚSICA: bandas sonoras oficiales de Call of Duty: Sarah Schachner («Modern Warfare II», «Hindsight», «Modern Warfare III», «Old "
        "Comrades»), Jack Wall («Bell's Theme»), Brian Tyler («I Stand Alone»), Harry Gregson-Williams y Stephen Barton («Crew Expendable», "
        "«Advanced Soldier Overture»), David Buckley («Rorke Files»), Sean Murray («Reznov Theme») y Wilbert Roget II («A Brotherhood of "
        "Heroes»). Audio del juego: Infinity Ward / Treyarch / Sledgehammer / Activision.\n\n"
        "GAMEPLAY DE: " + gameplay + " y más creadores. Gracias a todos.\n\n#callofduty #modernwarfare4 #blackops7")
# YouTube: descripción ≤ 5000 (cuenta bytes; 19-nov-2026 la de Turbo dio 5123 y la API la rechazó): enlaces hasta 4900 bytes
_n = len(vids)
while len(desc.replace("{GP}", " · ".join("https://youtu.be/" + v for v in vids[:_n])).encode("utf-8")) > 4900:
    _n -= 1
desc = desc.replace("{GP}", " · ".join("https://youtu.be/" + v for v in vids[:_n]))
srt = sorted(glob.glob("salida/*.srt"))
Y = {"titulo": "Cómo acabó REALMENTE cada protagonista de Call of Duty",
     "titulos_alternativos": ["Así MURIERON los 20 protagonistas de Call of Duty", "20 PROTAGONISTAS de Call of Duty y su final real"],
     "descripcion": desc,
     "etiquetas": ["call of duty", "protagonistas de call of duty", "capitan price", "price muere", "modern warfare 4", "mw4 final",
                   "soap", "gaz", "ghost", "alex mason", "frank woods", "reznov", "black ops 7", "call of duty en español", "expediente 141"],
     "categoria": 20, "idioma": "es", "idioma_audio": "es", "miniatura": "salida/miniatura.jpg",
     "subtitulos": srt[0].replace(os.sep, "/") if srt else None}
json.dump(Y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(desc), "caracteres,", len(desc.encode("utf-8")), "bytes;", _n, "de", len(vids), "videos de gameplay enlazados; srt:", Y["subtitulos"])
print(caps)
