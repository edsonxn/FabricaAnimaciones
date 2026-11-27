# -*- coding: utf-8 -*-
"""Escribe youtube.json (calco de tes_armaduras_poderosas/_youtube.py, 26-nov-2026): capítulos desde timeline + avisos, fuentes UESP de investigacion.md
y créditos de gameplay. YouTube mide BYTES (máx. 5 000)."""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")
t = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
fx = open(os.path.join(AQUI, "efectos.py"), encoding="utf-8").read()
nom = {"p" + n: f"#{n} {s}" for n, s in re.findall(r'aviso\("[^"]+", "?(\d+)"?, "([^"]+)"', fx)}
nom.update(intro="Las 15 cosas de Skyrim que pierdes para siempre", cr1="Correo: ¿nada divertido?", ag1="Gracias por comentar",
           cr2="Correo: el llorón", cr3="Correo: ¿secretos que todos conocen?", gema="Skuldafn: el lugar que te roba tres cosas",
           cierre="El top y tu pérdida")
caps = []
for e in t["escenas"]:
    if e["id"] in ("campana",):
        continue
    s = int(round(e["t0"]))
    caps.append(f"{s // 60}:{s % 60:02d} {nom.get(e['id'], e['id'])}")
F = list(dict.fromkeys(u.rstrip(").,;»*`") for u in re.findall(r"https://\S+", open(os.path.join(AQUI, "investigacion.md"), encoding="utf-8").read())))
cred = " · ".join(dict.fromkeys(v["canal"] for k, v in json.load(open(os.path.join(AQUI, "fuentes.json"), encoding="utf-8")).items()
                               if k.startswith("scene-") and isinstance(v, dict) and v.get("canal")))
N = "\n"
d = ("Un bastón que vale 1431 de oro y usas una sola vez, de llave. Un fuerte entero con cuatro maestros que pierdes por decirle que "
     "sí a un vampiro. Y un grito al que le falta su última palabra. Estas son las 15 cosas de Skyrim que PIERDES para siempre, sin "
     "consola y sin vuelta atrás: dónde están, cómo se pierden y cómo no caer. De las colmenas de Brillo Dorado al bastón de Nahkriin, "
     "pasando por la Embajada de Thalmor, Serana, la Corona dentada, el stalhrim y la Guardia del Alba." + N + N +
     "Gracias a @SrUnknown32, @JosueAlejandroPachecoBastidas, @creepynoodlesuvu, @sebastianmerino5943 y @achezeta5497 por comentar; "
     "y a @elianalera1925, @AdonsAdndna y @antonigirii por el correo con críticas, que también leemos." + N + N +
     "CAPÍTULOS" + N + N.join(caps) + N + N +
     "¿Cuál perdiste tú? ¿Cuál no sabías? Déjalo en los comentarios: leemos todos, los que nos felicitan y los que nos corrigen." + N + N +
     "¿Te gusta Fallout? Nuestro canal hermano RADIO YERMO es todo Fallout → https://www.youtube.com/@RadioYermo" + N + N +
     "FUENTES (cada dato, con su enlace):" + N + N.join(F) +
     N + "NOTA: el ranking es nuestro; los datos son del juego base en PC con todos los DLC (Dawnguard, Hearthfire y Dragonborn)." + N + N +
     "VIDEO RECOMENDADO: Las 15 misiones de Skyrim que NUNCA debes hacer → https://youtu.be/R4nzGhWuTmo" + N + N +
     "MÚSICA: The Elder Scrolls V: Skyrim, Dawnguard y Dragonborn (Jeremy Soule) — Bethesda Softworks / ZeniMax.")
pie = N + N + "#skyrim #elderscrolls #skyrimsecretos"
gp = "\n\nGAMEPLAY DE: " + cred + ". Gracias a todos los creadores."


def _cabe(d, gp, pie, tope=4850):
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


yt = dict(titulo="Las 15 cosas de Skyrim que PIERDES para siempre",
          titulos_alternativos=["15 cosas de Skyrim que PIERDES para siempre sin saberlo",
                                "Lo que PIERDES para siempre en Skyrim: 15 cosas"],
          descripcion=_cabe(d, gp, pie),
          etiquetas=["skyrim cosas que pierdes", "skyrim perdibles", "skyrim para siempre", "skyrim en español", "baston de nahkriin",
                     "invocar tormenta", "guardia del alba", "serana cura", "corona dentada", "stalhrim", "embajada thalmor",
                     "skyrim secretos", "elder scrolls", "cronicas de tamriel"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_pierdes_siempre.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"].encode("utf-8")), "bytes;", len(caps), "capítulos;", caps[1], caps[-2])
