# -*- coding: utf-8 -*-
"""Escribe youtube.json con capítulos sacados de timeline.json y créditos de fuentes.json."""
import collections, json

tl = json.load(open("timeline.json", encoding="utf-8"))
t0 = {e["id"]: e["frases"][0]["t0"] if e.get("frases") else e.get("t0", 0) for e in tl["escenas"]}
CAP = [("intro", "Los objetos que Blizzard escondió"), ("c15", "#15 Delicia de descarrioaleta sabrosa"), ("c14", "#14 Saltavientos musical: la rana que canta"), ("c13", "#13 Babosa agitada"),
       ("c12", "#12 Cría de crocolisco"), ("overgear", "Patrocinio: Overgear"), ("c11", "#11 Banana dorada"), ("c10", "#10 Crisálida transformadora"), ("c09", "#9 Cercenarrocas"),
       ("c08", "#8 Sortija de contramaestre"), ("c07", "#7 Don del galope"), ("c06", "#6 Loto negro a 50 de oro"), ("c05", "#5 Riendas de destrero de la muerte"), ("c04", "#4 La Llave de piedra"),
       ("c03", "#3 Shen'Serrar"), ("c02", "#2 Las 75 monturas ocultas"), ("c01", "#1 El primer legendario"), ("cierre", "Cierre")]
mm = lambda s: f"{int(s) // 60}:{int(s) % 60:02d}"
cap = "\n".join(f"{mm(0 if k == 'intro' else t0[k])} {n}" for k, n in CAP)
f = json.load(open("fuentes.json", encoding="utf-8"))
c = collections.Counter((x.get("canal") or "").strip() for k, x in f.items() if k.startswith("scene") and isinstance(x, dict))
canales = " · ".join(n for n, _ in c.most_common(16) if n)
d = f"""World of Warcraft Forever tiene más de 31 000 objetos y Blizzard escondió las estadísticas de 12 594: no sabes qué hacen hasta que alguien en el mundo consigue uno. Estos son los 15 objetos secretos que los jugadores encontraron en la beta, del 15 al 1, desde la rana que se consigue cantando hasta el legendario con el nombre borrado.

VIDEO PATROCINADO POR OVERGEAR
🎓 Coaching de WoW Forever en modo self-play: juegas tú con tu personaje todo el tiempo y un profesional verificado te guía por voz. Talentos, rotación, mazmorras nuevas, plan de equipo para las bandas o duelos, y pagas solo las horas que necesites.
🔥 10 % DE DESCUENTO con el código CRONICAS10
👉 https://overgear.com/games/wow-forever/coaching?utm_source=youtube&utm_medium=influence&utm_content=cronicas10&utm_campaign=051026

CAPÍTULOS
{cap}

Todo sale de la beta (terminó el 23 de octubre): algún número puede cambiar ya con el juego abierto. Lo del legendario es especulación sobre datos de la beta.
Los comentarios que salen en el video son reales: todos se leen y se toman en cuenta para mejorar el canal.

FUENTES
Wowhead: tooltips y noticias de Forever (Serenal, Jurdi, Slesh) · Icy Veins (Anshlun, PopTop, Neryssa) · PC Gamer (Tyler Colp) · Kami Labs · Mobalytics (PhaseShifter) · Raid Forever · wowf.io · wowforever.be · wago.tools · Warcraft Wiki

MÚSICA: banda sonora original de World of Warcraft (© Blizzard Entertainment): Stormwind, Feralas, Undercity, Dun Morogh, Durotar, Ironforge, Orgrimmar, Molten Core, Legends of Azeroth, Thunder Bluff y Darnassus (Wowmusicable) y Eastern Plaguelands (Blizzard Fields).
GAMEPLAY DE: {canales} · y más creadores de la comunidad. Gracias a todos. El canto de las ranas: TiffyMissWiffy.

Suscríbete para más contenido de World of Warcraft. ⚔️

#wowforever #worldofwarcraft #wowclassic"""
y = dict(titulo="Los 15 OBJETOS SECRETOS de WoW Forever que nadie te explica",
         titulos_alternativos=["Blizzard escondió 12 594 objetos en WoW Forever: estos son los mejores", "15 objetos secretos de WoW Forever que tienes que buscar YA"],
         descripcion=d, etiquetas=["wow forever", "world of warcraft forever", "wow forever objetos secretos", "wow forever secretos", "wow forever objetos ocultos", "wow forever guia", "wow forever mercado negro",
                                   "wow forever legendario", "wow forever monturas", "wow forever mascotas", "cercenarrocas", "banana dorada", "wow classic", "world of warcraft", "wow en español", "cronicas de warcraft"],
         promocion_pagada=True, categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/" + "Los_15_OBJETOS_SECRETOS_de_WoW_Forever_que_nadie_te_explica.srt")
json.dump(y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(d)); print(cap)
