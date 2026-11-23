# -*- coding: utf-8 -*-
"""Genera youtube.json de cod_mandela_zombies (capítulos del timeline real, créditos de fuentes.json y de audio/ost/_catalogo.txt)."""
import glob
import json
import os

T = json.load(open("timeline.json", encoding="utf-8"))
t0 = {e["id"]: e["t0"] + e.get("pre", 0) for e in T["escenas"]}
CAP = [("intro", "Expediente 141: los zombis"), ("p20", "#20 ¿Nixon, convertido en zombi?"), ("p19", "#19 Las últimas palabras de Nikolai"),
       ("p18", "#18 El mapa de zombis en llamas"), ("p17", "#17 El zombi misterioso de Verrückt"), ("p16", "#16 La escopeta del banco de Town"),
       ("p15", "#15 Quick Revive, dos a la vez"), ("p14", "#14 La Type 100 de World at War"), ("p13", "#13 El escudo de Richtofen"),
       ("p12", "#12 La Thundergun no mataba siempre"), ("p11", "#11 Puntos por tirarte frente a las máquinas"), ("p10", "#10 ¿Cuántos golpes con Juggernog?"),
       ("p09", "#9 Moon en blanco y negro"), ("p08", "#8 El avión de Nacht der Untoten"), ("p07", "#7 Rebirth, el mapa que no existe"),
       ("p06", "#6 Tombstone en solitario"), ("p05", "#5 La Thundergat"), ("p04", "#4 Si caes, no te arrastres"),
       ("p03", "#3 La Thundergun en la campaña"), ("p02", "#2 El puente de TranZit"), ("p01", "#1 La Ray Gun en la campaña de World at War"),
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
desc = ("¿La Ray Gun salía en la campaña de World at War? ¿La Thundergun en una misión de Black Ops? ¿Arrastrarte al caer te desangra "
        "más rápido? 20 efectos Mandela del modo Zombies de Call of Duty: recuerdos de la comunidad, dos mandados por ustedes en los "
        "comentarios, contra lo que de verdad hay en el juego, comprobado en pantalla y hasta en su código.\n\n"
        "¿Qué recuerdas tú de los zombis que nadie más recuerda? Escríbelo: si es bueno, sale en el siguiente expediente.\n\nCAPÍTULOS\n" + caps +
        "\n\nFUENTES:\nWiki de Call of Duty (Ray Gun, Little Resistance, Thundergun, Numbers, «Five», Gorod Krovi, Verrückt, Town, "
        "Remington 870 MCS, Quick Revive, Type 100, Zombie Shield, Perk-a-Cola, Juggernog, Ascension, Nacht der Untoten, Hard Landing, "
        "Rebirth, Rebirth Island, Tombstone Soda, Blundergat, TranZit) — https://callofduty.fandom.com\nScript _zm_laststand.gsc de "
        "Black Ops II (Plutonium, t6-scripts) — https://github.com/plutoniummod/t6-scripts\nHilos de r/CODZombies, r/MandelaEffect e "
        "r/Infinitewarfare con los recuerdos de la comunidad — https://www.reddit.com\n\n"
        "MÚSICA Y SONIDO: bandas sonoras oficiales de los Zombies de Call of Duty: Kevin Sherwood («Damned», «Samantha's Lullaby», "
        "«Samantha's Dream», «Dead Fragment», «Coming Home», temas de Nacht der Untoten) y Treyarch («Echoes of the Damned», «Damned 8»). "
        "Audio del juego: Treyarch / Activision.\n\n"
        "GAMEPLAY DE: " + gameplay + " y más creadores. Gracias a todos.\n\n#callofduty #efectomandela #codzombies")
# YouTube: descripción ≤ 5000 (cuenta bytes; 19-nov-2026 la de Turbo dio 5123 y la API la rechazó): enlaces hasta 4900 bytes
_n = len(vids)
while len(desc.replace("{GP}", " · ".join("https://youtu.be/" + v for v in vids[:_n])).encode("utf-8")) > 4900:
    _n -= 1
desc = desc.replace("{GP}", " · ".join("https://youtu.be/" + v for v in vids[:_n]))
srt = sorted(glob.glob("salida/*.srt"))
Y = {"titulo": "Los 20 EFECTOS MANDELA de los Zombies de Call of Duty",
     "titulos_alternativos": ["20 cosas de CoD Zombies que recuerdas MAL", "20 EFECTOS MANDELA del modo Zombies de CoD"],
     "descripcion": desc,
     "etiquetas": ["call of duty", "efecto mandela", "efecto mandela call of duty", "cod zombies", "zombies", "ray gun", "thundergun",
                   "world at war", "black ops", "tranzit", "juggernog", "nacht der untoten", "call of duty en español", "expediente 141"],
     "categoria": 20, "idioma": "es", "idioma_audio": "es", "miniatura": "salida/miniatura.jpg",
     "subtitulos": srt[0].replace(os.sep, "/") if srt else None}
json.dump(Y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(desc), "caracteres,", len(desc.encode("utf-8")), "bytes;", _n, "de", len(vids), "videos de gameplay enlazados; srt:", Y["subtitulos"])
print(caps)
