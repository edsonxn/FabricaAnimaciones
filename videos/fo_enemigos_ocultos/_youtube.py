# -*- coding: utf-8 -*-
"""Escribe youtube.json: capítulos desde timeline.json, fuentes (Fallout Wiki) desde las investigaciones, créditos de gameplay
(canal de cada video usado en busquedas.json, con yt-dlp) y música (audio/ost/_ids.json).      python _youtube.py"""
import json
import re
import subprocess

tl = {e["id"]: e["t0"] for e in json.load(open("timeline.json", encoding="utf-8"))["escenas"]}
CAP = [("intro", "Buenos días, Yermo"), ("p15", "15 · El Quinteto de la Reina (FO3)"), ("p14", "14 · El cazador legendario (NV)"),
       ("p13", "13 · El Red Death (Far Harbor)"), ("p12", "12 · Ruzka, la osa maravilla (Point Lookout)"), ("p11", "11 · Stripe (Old World Blues)"),
       ("p10", "10 · La reina Nukalurk (Nuka-World)"), ("p9", "9 · Madre Curie III (Broken Steel)"), ("p8", "8 · Gabe (Old World Blues)"),
       ("p7a", "7 · El alienígena del OVNI (FO4)"), ("p6", "6 · El sanguinario legendario (NV)"), ("p5", "5 · El mutascorpio albino (FO3)"),
       ("p4", "4 · Sanguinarios camaleón y mítico (FO4)"), ("p3", "3 · Rawr (Lonesome Road)"), ("p2", "2 · Hundebarcos (Far Harbor)"),
       ("p1", "1 · La tochomosca legendaria (Old World Blues)"), ("cierre", "Cierre")]


def mmss(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


caps = "\n".join(f"{'0:00' if k == 'intro' else mmss(tl[k])} {n}" for k, n in CAP)
fuentes = []
for f in ("_investigacion_A.md", "_investigacion_B.md"):
    for u in re.findall(r"https://fallout\.fandom\.com/(?:es/)?wiki/[^\s)>,·`;]+", open(f, encoding="utf-8").read()):
        if u not in fuentes and "File:" not in u:
            fuentes.append(u)
ids = sorted({v["url"].rsplit("/", 1)[1] for v in json.load(open("busquedas.json", encoding="utf-8")).values()})
canales = []
for i in ids:
    r = subprocess.run(["python", "-m", "yt_dlp", "--print", "%(channel)s", "https://youtu.be/" + i], capture_output=True, text=True,
                       encoding="utf-8")
    c = r.stdout.strip()
    if c and c not in canales:
        canales.append(c)
juegos = {"fo1": "Fallout (Mark Morgan)", "fo3": "Fallout 3 (Inon Zur)", "fnv": "Fallout: New Vegas (Inon Zur)",
          "fo4": "Fallout 4 (Inon Zur)", "fo76": "Fallout 76 (Inon Zur)", "fot": "Fallout Tactics"}
desc = f"""Buenos días, Yermo. Hoy en Radio Yermo: los 15 enemigos ocultos de Fallout 3, New Vegas y Fallout 4 que casi nadie llegó a ver. Una osa de circo que sigue jugando con su pelota roja doscientos años después, un perro gigante que al morir se vuelve atómico, un monstruo marino legendario que cabe en una cubeta, un alienígena escondido en una cueva… y el enemigo más fuerte de todo New Vegas, que resulta ser una mosca.

¿Cuántos encontraste tú? ¿Alguien vio a Stripe? Te leemos en los comentarios.

CAPÍTULOS
{caps}

FUENTES (lore oficial, Fallout Wiki):
""" + "\n".join(fuentes[:60]) + f"""

MÚSICA: banda sonora oficial de {', '.join(juegos.values())} — Bethesda Softworks / ZeniMax / Interplay.

GAMEPLAY DE: {' · '.join(canales)}. Gracias a todos los creadores.

#fallout #falloutlore #radioyermo"""
y = dict(titulo="15 ENEMIGOS ocultos de Fallout que casi nadie vio",
         titulos_alternativos=["15 enemigos SECRETOS de Fallout que te perdiste", "El enemigo MÁS fuerte de New Vegas es una mosca"],
         descripcion=desc,
         etiquetas=["fallout", "enemigos ocultos fallout", "secretos de fallout", "fallout 3", "fallout new vegas", "fallout 4",
                    "tochomosca legendaria", "legendary bloatfly", "rawr", "stripe", "gabe old world blues", "hundebarcos", "shipbreaker",
                    "red death", "ruzka", "sanguinario mitico", "lore de fallout en español", "radio yermo"],
         categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/fo_enemigos_ocultos.srt")
json.dump(y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(desc), "caracteres ·", len(fuentes), "fuentes ·", len(canales), "canales")
