# -*- coding: utf-8 -*-
"""Escribe youtube.json: capítulos desde timeline.json, fuentes (Fallout Wiki) desde las investigaciones, créditos de gameplay
(canal de cada video usado en busquedas.json, con yt-dlp) y música (audio/ost/_ids.json).      python _youtube.py"""
import json
import re
import subprocess

tl = {e["id"]: e["t0"] for e in json.load(open("timeline.json", encoding="utf-8"))["escenas"]}
CAP = [("intro", "Buenos días, Yermo"), ("p25", "25 · Refugios 55 y 56"), ("p24", "24 · Refugio 21"), ("p23", "23 · Refugio 118"),
       ("p22", "22 · Refugio 43"), ("p21", "21 · Refugio 88"), ("p20", "20 · Refugio 101"), ("p19", "19 · Refugio 22"),
       ("p18", "18 · Refugio 106"), ("p17", "17 · Refugio 63"), ("p16", "16 · Refugio 81"), ("p15a", "15 · Refugio 108"),
       ("p14", "14 · Refugio 0"), ("p13", "13 · Refugio 77"), ("p12", "12 · Refugio 94"), ("p11", "11 · Refugios 68 y 69"),
       ("p10", "10 · Refugio 95"), ("p9", "9 · Refugio 111"), ("p8", "8 · Refugio 12"), ("p7a", "7 · Refugio 92"),
       ("p6", "6 · Refugio 87"), ("p5", "5 · Refugio 96"), ("p4", "4 · Refugio 51"), ("p3a", "3 · Refugio 11"),
       ("p2", "2 · Refugio 75"), ("p1", "1 · Refugio 112: el peor refugio de Fallout"), ("cierre", "Cierre")]


def mmss(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


caps = "\n".join(f"{'0:00' if k == 'intro' else mmss(tl[k])} {n}" for k, n in CAP)
fuentes = []
for f in ("_investigacion_A.md", "_investigacion_B.md", "_investigacion_C.md"):
    for u in re.findall(r"https://fallout\.fandom\.com/(?:es/)?wiki/[^\s)>,·`]+", open(f, encoding="utf-8").read()):
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
desc = f"""Buenos días, Yermo. Esto es Radio Yermo, con la transmisión más larga que hemos hecho: los 25 refugios más malvados, crueles y raros de Fallout, del aburrimiento como arma al peor refugio de toda la saga. Un refugio con una puerta que no cierra, otro con veinte hombres, diez mujeres y una pantera, otro donde cada año había que elegir a quién matar… y el hombre que diseñó los experimentos de Vault-Tec y se quedó un refugio para él solo.

Fallout 1, Fallout 3, New Vegas, Fallout 4, Fallout 76, Tactics y el lore oficial. Lo que no tiene imagen en ningún juego (los refugios 43, 55, 56, 68, 69, 77 y escenas como el día de la guerra en el Refugio 12) va como RECREACIÓN con los gráficos del juego, marcada en pantalla.

¿Cuál es el peor para ti? ¿El 112, el 75 o el 11? Te leemos en los comentarios.

CAPÍTULOS
{caps}

FUENTES (lore oficial, Fallout Wiki):
""" + "\n".join(fuentes[:60]) + f"""

MÚSICA: banda sonora oficial de {', '.join(juegos.values())} — Bethesda Softworks / ZeniMax / Interplay.

GAMEPLAY DE: {' · '.join(canales)}. Gracias a todos los creadores.

#fallout #falloutlore #radioyermo"""
y = dict(titulo="Los 25 refugios más MALVADOS de Fallout",
         titulos_alternativos=["25 refugios de Fallout que NUNCA fueron para salvarte", "El PEOR refugio de Fallout y otros 24 igual de crueles"],
         descripcion=desc,
         etiquetas=["fallout", "fallout lore", "refugios fallout", "vault tec", "refugio 112", "refugio 11", "refugio 75",
                    "tranquility lane", "fallout 3", "fallout 4", "fallout new vegas", "fallout 76", "lore de fallout en español",
                    "experimentos vault tec", "radio yermo"],
         categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/fo_refugios_25.srt")
json.dump(y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(desc), "caracteres ·", len(fuentes), "fuentes ·", len(canales), "canales")
