# -*- coding: utf-8 -*-
"""Escribe youtube.json de wow_100_curiosidades_tbc_wotlk (receta de wow_curiosidades_kalimdor/youtube_gen.py): capítulos POR ZONA
(100 curiosidades no caben como capítulos sueltos y en YouTube se navegan mejor por zona) con la línea de tiempo real, créditos de
gameplay (salida/creditos.txt) y de música (audio/creditos_musica.txt, `musica_wow.py`).
Uso (desde la carpeta del video):   python youtube_gen.py"""
import json
import re
import sys

import guion

ZONA = dict(fuego="Península del Fuego Infernal", zangar="Marisma de Zangar", terokkar="Bosque de Terokkar y Shattrath",
            nagrand="Nagrand", filospada="Montañas Filospada", tormenta="Tormenta Abisal", sombraluna="Valle Sombraluna",
            quelthalas="Quel'Thalas", azuremyst="Isla Bruma Azur", karazhan="Karazhan", cavernas="Cavernas del Tiempo",
            boreal="Tundra Boreal", fiordo="Fiordo Aquilonal", dragones="Cementerio de Dragones", pardas="Colinas Pardas",
            zuldrak="Zul'Drak", sholazar="Cuenca de Sholazar", cumbres="Las Cumbres Tormentosas", dalaran="Dalaran",
            invierno="Conquista del Invierno", corona="Corona de Hielo")


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main():
    tl = json.load(open("timeline.json", encoding="utf-8"))
    caps, previa = ["0:00 Intro"], None
    for e in tl["escenas"]:
        n = re.fullmatch(r"c(\d{3})", e["id"])
        if not n:
            continue
        z = guion.ZONA_DE[e["id"]]
        if z != previa:
            nums = [int(k[1:]) for k, v in guion.ZONA_DE.items() if v == z and k[1:].isdigit()]
            rango = f"#{max(nums)}" + (f"-{min(nums)}" if len(nums) > 1 else "")
            caps.append(f"{mmss(e['t0'])} {ZONA[z]} ({rango})")
            previa = z
    cierre = next(e for e in tl["escenas"] if e["id"] == "cierre")
    caps.append(f"{mmss(cierre['t0'])} Cierre")
    clips = open("salida/creditos.txt", encoding="utf-8").read().splitlines()[1:]
    canales = []
    for l in clips:
        m = re.search(r" — (.+?): https://", l)
        if m and m.group(1).strip() and m.group(1) not in canales:
            canales.append(m.group(1))
    musica = [l[2:].split(" — ")[0] for l in open("audio/creditos_musica.txt", encoding="utf-8").read().splitlines() if l.startswith("- ")]
    cab = ("Una ciudad que dejó un cráter al mudarse, un enano que todo el mundo cree muerto, una banda de empleados de Blizzard "
           "tocando en una taberna y un goblin que te borra la memoria al salir del pueblo. Estas son 100 curiosidades, secretos y "
           "easter eggs de Burning Crusade y Wrath of the Lich King, en cuenta regresiva y zona por zona, del Portal Oscuro al "
           "Trono Helado. Todas las puedes ir a ver: en cada una te digo dónde pararte.\n\n"
           "CAPÍTULOS\n" + "\n".join(caps) + "\n\n"
           "Datos verificados en Wowpedia y Wowhead, con los nombres de la localización oficial en español.\n\n"
           "Música: " + ", ".join(musica[:-1]) + " y " + musica[-1] + ", banda sonora original de World of Warcraft "
           "(© Blizzard Entertainment).\n\n")
    pie = "\n\nSuscríbete para más contenido de World of Warcraft. ⚔️\n\n#worldofwarcraft #burningcrusade #wotlk"
    lista, resto = [], 0
    for c in canales:                       # 182 canales: los que quepan bajo el límite de 5 000 caracteres
        prueba = cab + "GAMEPLAY DE: " + ", ".join(lista + [c]) + f", y {len(canales) - len(lista) - 1} canales más." + pie
        if len(prueba) > 4950:
            break
        lista.append(c)
    resto = len(canales) - len(lista)
    desc = cab + "GAMEPLAY DE: " + ", ".join(lista) + (f", y {resto} canales más" if resto else "") + ". Gracias a todos los creadores." + pie
    d = dict(
        titulo="100 CURIOSIDADES y secretos de Burning Crusade y Wrath que puedes ir a ver",
        titulos_alternativos=["100 SECRETOS de Terrallende y Rasganorte que pasaste corriendo (WoW)",
                              "100 easter eggs de Burning Crusade y Wrath of the Lich King que casi nadie vio"],
        descripcion=desc,
        etiquetas=["curiosidades wow", "secretos wow", "easter eggs wow", "burning crusade", "wrath of the lich king", "wotlk",
                   "tbc classic", "wotlk classic", "terrallende", "rasganorte", "shattrath", "dalaran", "corona de hielo",
                   "elite tauren chieftain", "bridenbrad", "harrison jones", "lore de warcraft", "world of warcraft",
                   "wow en español", "cronicas de warcraft"],
        categoria=20, idioma="es", idioma_audio="es",
        miniatura="salida/miniatura.jpg", subtitulos="salida/wow_100_curiosidades_tbc_wotlk.srt",
    )
    assert len(desc) < 5000, len(desc)
    json.dump(d, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"youtube.json: {len(caps)} capítulos, {len(lista)}/{len(canales)} canales de gameplay, descripción de {len(desc)} caracteres")
    print("\n".join(caps))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
