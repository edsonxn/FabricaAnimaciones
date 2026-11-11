# -*- coding: utf-8 -*-
"""Escribe youtube.json (calco de tes_seres_poderosos/_youtube.py): capítulos desde timeline + avisos, fuentes UESP de _investigacion.md
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
nom.update(intro="Las 10 builds más rotas de Skyrim", cr1="Correo: las voces", ag1="Gracias por comentar", cr2="Correo: «tanta AI»",
           cr3="Correo: el talento", cierre="El top y tu build")
caps = []
for e in t["escenas"]:
    if e["id"] in ("campana", "p10b", "p6b"):
        continue
    s = int(round(e["t0"]))
    caps.append(f"{s // 60}:{s % 60:02d} {nom.get(e['id'], e['id'])}")
F = list(dict.fromkeys(u.rstrip(").,;»") for u in re.findall(r"https://\S+", open(os.path.join(AQUI, "_investigacion.md"), encoding="utf-8").read())))
cred = " · ".join(dict.fromkeys(v["canal"] for k, v in json.load(open(os.path.join(AQUI, "fuentes.json"), encoding="utf-8")).items()
                               if k.startswith("scene-") and isinstance(v, dict) and v.get("canal")))
N = "\n"
d = ("Una piedra, una raza, cuatro prendas… y el juego deja de tener dificultad. Estas son las 10 builds más ROTAS de Skyrim, del arquero "
     "que hace todo el mundo al alquimista que borra el juego: el Arquero Fantasma, el Carterista Envenenador, el Titiritero, el Señor de los "
     "Vampiros, el Nigromante Infinito, el Asesino de la Hermandad, el Mago Sin Coste, el Pararrayos, el Artesano Legendario y el Dios del "
     "Boticario. Con su raza, su piedra, sus ventajas, el equipo y dónde se consigue. Cada dato comprobado en UESP." + N + N +
     "Narra Johnny, con MariCarmen y el Profeta de visita." + N + N +
     "Gracias a @launionsovietica3315, @JinbeiDLuffy, @REaPEK.papulol, @estebato2448 y @DJRaygadaVargas por comentar; y a @npc_1261, "
     "@edgarvillalobos1492 y @YetRise por el correo con críticas, que también leemos." + N + N +
     "CAPÍTULOS" + N + N.join(caps) + N + N +
     "¿Cuál falta? Déjalo en los comentarios: leemos todos, los que nos felicitan y los que nos corrigen." + N + N +
     "FUENTES (cada dato, con su enlace):" + N + N.join(F) +
     N + "NOTA: el ranking es nuestro; los errores del juego base los marcamos como error (el parche no oficial corrige varios)." + N + N +
     "VIDEO RECOMENDADO: Las 15 armas más PODEROSAS de Skyrim → https://youtu.be/m6Pk4FLQGuc" + N + N +
     "MÚSICA: The Elder Scrolls V: Skyrim, Dawnguard y Dragonborn (Jeremy Soule) — Bethesda Softworks / ZeniMax.")
pie = N + N + "#skyrim #elderscrolls #builds"
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


yt = dict(titulo="Las 10 builds más ROTAS de Skyrim",
          titulos_alternativos=["Las 10 builds más ROTAS de Skyrim (y dónde conseguir todo)",
                                "10 builds de Skyrim que ROMPEN el juego, del arquero al alquimista infinito"],
          descripcion=_cabe(d, gp, pie),
          etiquetas=["builds rotas skyrim", "mejores builds skyrim", "skyrim build", "build mas rota de skyrim", "skyrim en español",
                     "bucle de alquimia", "fortify restoration", "mago sin coste skyrim", "absorcion de hechizos", "señor de los vampiros",
                     "nigromante skyrim", "hermandad oscura", "arquero sigilo skyrim", "piedras guardianas", "elder scrolls",
                     "cronicas de tamriel"],
          categoria=20, idioma="es", idioma_audio="es", miniatura="salida/miniatura.jpg", subtitulos="salida/tes_builds_rotas.srt")
json.dump(yt, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(yt["descripcion"].encode("utf-8")), "bytes;", len(caps), "capítulos;", caps[1], caps[-2])
