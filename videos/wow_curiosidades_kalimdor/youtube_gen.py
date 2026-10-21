# -*- coding: utf-8 -*-
"""Escribe youtube.json de wow_curiosidades_kalimdor: capítulos con la línea de tiempo real (timeline.json) y créditos de
gameplay (salida/creditos.txt, `fab.py <v> fuentes`) y de música (audio/creditos_musica.txt, `musica_wow.py`).
Uso (desde la carpeta del video):   python youtube_gen.py"""
import json
import re
import sys

CAP = {
    "intro": "Intro", "c30": "El diablillo de La Masacre", "c29": "El cementerio de los kodos", "c28": "La gorila robot",
    "c27": "¿Dónde está la esposa de Mankrik?", "c26": "Ringo y los Beatles", "c25": "¿Alguien dijo Thunderfury?",
    "c24": "La secta del sótano de Orgrimmar", "c23": "La pesadilla de Naralex", "c22": "Agua de Azshara para Ragnaros",
    "c21": "La Isla de los GM", "c20": "Gahz'rilla y el mazo", "c19": "Linken es Link", "c18": "El origen de los centauros",
    "c17": "El sable de escarcha", "c16": "El fuerte que no aceptó la paz", "c15": "Rey de los ogros",
    "c14": "Un dios convertido en zarzas", "c13": "Las flores cantoras", "c12": "Goblins contra gnomos",
    "c11": "El traidor de los Lanza Negra", "c10": "La broma del yeti", "c09": "El monumento a Grom",
    "c08": "El defecto de Teldrassil", "c07": "Las puertas de Ahn'Qiraj", "c06": "Malfurion en coma",
    "c05": "50 DKP minus", "c04": "La espada forjada por Onyxia", "c03": "El fantasma de la Costa Oscura",
    "c02": "El grito de Rajaxx", "c01": "La puerta de Uldum", "cierre": "Cierre",
}


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main():
    tl = json.load(open("timeline.json", encoding="utf-8"))
    caps = []
    for e in tl["escenas"]:
        n = re.fullmatch(r"c(\d\d)", e["id"])
        caps.append(f"{mmss(e['t0'])} {'#' + str(int(n.group(1))) + ' ' if n else ''}{CAP[e['id']]}")
    clips = open("salida/creditos.txt", encoding="utf-8").read().splitlines()[1:]
    canales = []
    for l in clips:
        m = re.search(r" — (.+?): https://", l)
        if m and m.group(1) not in canales:
            canales.append(m.group(1))
    musica = [l[2:].split(" — ")[0] for l in open("audio/creditos_musica.txt", encoding="utf-8").read().splitlines() if l.startswith("- ")]
    desc = ("Un goblin que revive kodos moribundos para vendérselos a una caravana, un diablillo que te reta a perseguirlo "
            "recitando rimas y una puerta de los titanes que se quedó seis años cerrada. Estas son 30 curiosidades de Kalimdor "
            "del World of Warcraft original, en cuenta regresiva: de las que casi nadie conoce a la más rara de todas, justo "
            "antes de que vuelvan con World of Warcraft Forever el 4 de noviembre de 2026.\n\n"
            "CAPÍTULOS\n" + "\n".join(caps) + "\n\n"
            "Datos verificados en Wowpedia y Wowhead, con los nombres de la localización oficial en español.\n\n"
            "Música: " + ", ".join(musica[:-1]) + " y " + musica[-1] + ", banda sonora original de World of Warcraft "
            "(© Blizzard Entertainment).\n\n"
            "GAMEPLAY DE: " + ", ".join(canales) + ". Gracias a todos los creadores.\n\n"
            "Suscríbete para más contenido de World of Warcraft. ⚔️\n\n#worldofwarcraft #wowclassic #wowforever")
    d = dict(
        titulo="30 CURIOSIDADES de Kalimdor que casi nadie conoce (WoW Classic)",
        titulos_alternativos=["30 SECRETOS de Kalimdor que nunca viste en WoW Classic",
                              "La puerta de Uldum, Mankrik y 28 secretos más de Kalimdor"],
        descripcion=desc,
        etiquetas=["wow classic", "curiosidades wow", "secretos wow classic", "kalimdor", "kalimdor wow",
                   "world of warcraft curiosidades", "wow forever", "world of warcraft forever", "esposa de mankrik",
                   "thunderfury", "uldum", "ahn'qiraj", "señor de los escarabajos", "quel'serrar", "la masacre",
                   "lore de warcraft", "world of warcraft", "wow en español", "cronicas de warcraft"],
        categoria=20, idioma="es", idioma_audio="es",
        miniatura="salida/miniatura.jpg", subtitulos="salida/wow_curiosidades_kalimdor.srt",
    )
    assert len(desc) < 5000, len(desc)
    json.dump(d, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"youtube.json: {len(caps)} capítulos, {len(canales)} canales de gameplay, descripción de {len(desc)} caracteres")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
