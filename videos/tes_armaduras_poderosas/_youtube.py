# -*- coding: utf-8 -*-
"""Escribe youtube.json (calco de tes_seres_poderosos/_youtube.py): capítulos desde timeline + avisos, fuentes UESP de investigacion.md
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
nom.update(intro="Las 20 armaduras más poderosas de Skyrim", cr1="Correo: una sola voz", ag1="Gracias por comentar",
           cr2="Correo: la recompensa", honor="Menciones de honor", gema="Por qué el hierro protege igual", cierre="El top y tu armadura")
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
d = ("Una máscara que invoca a un sacerdote dragón cuando vas a morir, una coraza que exige sacrificar a tu seguidor y un casco que "
     "escupe vapor. Estas son las 20 ARMADURAS más poderosas de Skyrim, con sus números, su truco y dónde se consigue cada una: del "
     "Semblante de Mzund a la armadura daédrica, pasando por Konahrik, el equipo de Miraak, la Cota de ébano, el stalhrim y las placas de "
     "dragón. Y al final, por qué una armadura de hierro puede protegerte igual que la mejor del juego." + N + N +
     "Esta vez narra solo el Profeta: leímos sus comentarios sobre las voces." + N + N +
     "Gracias a @RelatorNoctambulo, @zaarondarklord6196, @Reyes3019, @Ivan-g9l2n y @CarlosLopez-x9j por comentar; y a @frankortiz7101, "
     "@Lagartija_Vaquera y @stratosincaster4500 por el correo con críticas, que también leemos." + N + N +
     "CAPÍTULOS" + N + N.join(caps) + N + N +
     "¿Cuál falta? ¿Cuál te pones tú? Déjalo en los comentarios: leemos todos, los que nos felicitan y los que nos corrigen." + N + N +
     "¿Te gusta Fallout? Nuestro canal hermano RADIO YERMO es todo Fallout → https://www.youtube.com/@RadioYermo" + N + N +
     "FUENTES (cada dato, con su enlace):" + N + N.join(F) +
     N + "NOTA: el ranking es nuestro; los valores son del juego base en PC con todos los DLC (Dawnguard, Hearthfire y Dragonborn)." + N + N +
     "VIDEO RECOMENDADO: Las 15 armas más PODEROSAS de Skyrim → https://youtu.be/m6Pk4FLQGuc" + N + N +
     "MÚSICA: The Elder Scrolls V: Skyrim, Dawnguard y Dragonborn (Jeremy Soule) — Bethesda Softworks / ZeniMax.")
pie = N + N + "#skyrim #elderscrolls #armaduras"
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


yt = dict(titulo="Las 20 ARMADURAS más poderosas de Skyrim",
          titulos_alternativos=["Las 20 ARMADURAS más poderosas de Skyrim y dónde conseguirlas",
                                "20 ARMADURAS de Skyrim que te hacen casi inmortal"],
          descripcion=_cabe(d, gp, pie),
          etiquetas=["armaduras skyrim", "mejores armaduras skyrim", "armadura mas poderosa skyrim", "skyrim en español",
                     "armadura daedrica", "konahrik", "miraak", "cota de ebano", "stalhrim", "armadura de placas de dragon",
                     "armadura de ruiseñor", "tope de armadura skyrim", "elder scrolls", "cronicas de tamriel"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_armaduras_poderosas.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"].encode("utf-8")), "bytes;", len(caps), "capítulos;", caps[1], caps[-2])
