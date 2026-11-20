# -*- coding: utf-8 -*-
"""Genera youtube.json de cod_mandela3 (capítulos del timeline real, créditos de fuentes.json y de audio/ost/_catalogo.txt)."""
import glob
import json
import os

T = json.load(open("timeline.json", encoding="utf-8"))
t0 = {e["id"]: e["t0"] + e.get("pre", 0) for e in T["escenas"]}
CAP = [("intro", "Expediente 141: parte 3"), ("p20", "#20 ¿Gaz en Modern Warfare 2?"), ("p19", "#19 Max Ammo y el cargador"),
       ("p18", "#18 La nuke de Call of Duty 4"), ("p17", "#17 El hombre del menú de Black Ops"), ("p16", "#16 Speed Cola en el balcón"),
       ("p15", "#15 La carne de Black Ops 2"), ("p14", "#14 Extinction no era de Battlefield"), ("p13", "#13 La frase de Reznov"),
       ("p12", "#12 One in the Chamber… y un intruso"), ("p11", "#11 La bufanda de Ghost"), ("p10", "#10 Los dos capitanes Price"),
       ("p09", "#9 El poste de Piccadilly"), ("p08", "#8 Mule Kick en Nacht"), ("p07", "#7 La frase de Prípiat"),
       ("p06", "#6 El mapa soleado que no existe"), ("p05", "#5 La Ray Gun Mark II"), ("p04", "#4 Remember, no Russian"),
       ("p03", "#3 El brazo de Jackson"), ("p02", "#2 El zombi de Nuketown"), ("p01", "#1 Menéndez en la celda"),
       ("cierre", "Expediente cerrado")]


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
desc = ("¿Gaz salía en Modern Warfare 2? ¿Max Ammo te llenaba el cargador? ¿Menéndez acabó en una celda? Parte 3 de los efectos Mandela de "
        "Call of Duty: 20 recuerdos de la comunidad, varios mandados por ustedes en los comentarios, contra lo que de verdad hay en el "
        "juego, comprobado en pantalla.\n\n"
        "En el número 12 alguien nos robó el micrófono: se llama Turbo. ¿Se queda en el expediente o lo echamos? Vota en los "
        "comentarios: «QUE SE QUEDE» o «FUERA TURBO».\n\nCAPÍTULOS\n" + caps +
        "\n\nFUENTES:\nWiki de Call of Duty (transcripciones de All Ghillied Up, Their Land, Their Blood y Vendetta; Gaz, John Price, "
        "Price (World War II), Max Ammo, Mule Kick, Nacht der Untoten, Farm, Zombie Flesh, Extinction, One in the Chamber, Piccadilly, "
        "No Russian, Volker, Nuketown Zombies, Nuk3town, Mannequin, Alpha Omega, Ray Gun Mark II, Vengeance, Raul Menendez) — "
        "https://callofduty.fandom.com\nHilos de r/CODZombies, r/CallOfDuty, r/ModernWarfareII, r/modernwarfare, r/MandelaEffect y "
        "r/Retconned con los recuerdos de la comunidad — https://www.reddit.com\n\n"
        "MÚSICA Y SONIDO: bandas sonoras oficiales de Call of Duty: Harry Gregson-Williams y Stephen Barton («Scout Sniper Pripyat»), "
        "Hans Zimmer y Lorne Balfe («Estate Betrayal», «Takedown»), Jack Wall («Judgment Day», «DeFalco's Theme», «Trabzon Airfield»), "
        "Kevin Sherwood («Damned 100ae»), Sarah Schachner («Piccadilly Circus»), Sean Murray («NVA Last Stand», «Heart of the Reich»), "
        "Michael Giacchino («Call of Duty»), y los temas de Call of Duty: Ghosts (Extinction) y Black Ops 7. "
        "Audio del juego: Infinity Ward, Treyarch, Sledgehammer, Raven / Activision.\n\n"
        "GAMEPLAY DE: " + gameplay + " y más creadores. Gracias a todos.\n\n#callofduty #efectomandela #codzombies")
# YouTube: descripción ≤ 5000 (cuenta bytes; 19-nov-2026 la de Turbo dio 5123 y la API la rechazó): enlaces hasta 4900 bytes
_n = len(vids)
while len(desc.replace("{GP}", " · ".join("https://youtu.be/" + v for v in vids[:_n])).encode("utf-8")) > 4900:
    _n -= 1
desc = desc.replace("{GP}", " · ".join("https://youtu.be/" + v for v in vids[:_n]))
srt = sorted(glob.glob("salida/*.srt"))
Y = {"titulo": "Los 20 EFECTOS MANDELA de Call of Duty, parte 3",
     "titulos_alternativos": ["20 cosas de Call of Duty que recuerdas MAL, parte 3", "Los 20 EFECTOS MANDELA de CoD que TÚ recordaste 3"],
     "descripcion": desc,
     "etiquetas": ["call of duty", "efecto mandela", "efecto mandela call of duty", "cod zombies", "menendez", "no russian", "gaz",
                   "reznov", "max ammo", "nuketown", "ray gun mark 2", "black ops", "modern warfare", "call of duty en español",
                   "expediente 141"],
     "categoria": 20, "idioma": "es", "idioma_audio": "es", "miniatura": "salida/miniatura.jpg",
     "subtitulos": srt[0].replace(os.sep, "/") if srt else None}
json.dump(Y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(desc), "caracteres,", len(desc.encode("utf-8")), "bytes;", _n, "de", len(vids), "videos de gameplay enlazados; srt:", Y["subtitulos"])
print(caps)
