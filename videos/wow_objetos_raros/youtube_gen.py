# -*- coding: utf-8 -*-
"""Escribe youtube.json de wow_objetos_raros: capítulos con la línea de tiempo real (timeline.json) y créditos de
gameplay (salida/creditos.txt, `fab.py <v> fuentes`), de música (audio/creditos_musica.txt, `musica_wow.py`) y de mapas.
Uso (desde la carpeta del video):   python youtube_gen.py"""
import json
import re
import sys

CAP = {
    "intro": "Intro", "c12": "Puño de Verigan", "c11": "Sable de hielo de Cuna del Invierno", "c10": "Ferromazo",
    "c09": "Corcel nefasto", "c08": "Quel'Serrar", "c07": "Rhok'delar", "c06": "Riendas de destrero de la muerte",
    "c05": "Sulfuras, Mano de Ragnaros", "c04": "Crematoria corrupta", "c03": "Trueno Furioso", "c02": "Atiesh",
    "c01": "El Cetro del Mar de Dunas y el tanque negro", "cierre": "¿Cuáles vuelven en Forever?",
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
    desc = ("Sulfuras, Trueno Furioso, Atiesh, el tanque negro qiraji... Estos son los 12 objetos más raros de World of Warcraft "
            "Vanilla, en cuenta regresiva del más difícil de ver al que casi nadie tuvo nunca, con el MAPA del juego para "
            "enseñar dónde se consiguen y la ruta de cada cadena de misiones. Y cuáles podrían volver con World of Warcraft "
            "Forever, que sale el 4 de noviembre de 2026.\n\n"
            "CAPÍTULOS\n" + "\n".join(caps) + "\n\n"
            "Datos verificados en Wowpedia, warcraft.wiki.gg y Wowhead (Classic), con los nombres de la localización oficial "
            "en español. Mapas: Wowhead Classic. Las probabilidades de botín son estimaciones de la comunidad salvo donde se "
            "indica.\n\n"
            "Música: " + ", ".join(musica[:-1]) + " y " + musica[-1] + ", banda sonora original de World of Warcraft "
            "(© Blizzard Entertainment).\n\n"
            "GAMEPLAY DE: " + ", ".join(canales) + ". Gracias a todos los creadores.\n\n"
            "Suscríbete para más contenido de World of Warcraft. ⚔️\n\n#worldofwarcraft #wowclassic #wowforever")
    d = dict(
        titulo="Los 12 objetos más RAROS de WoW Vanilla (y cuáles vuelven en Forever)",
        titulos_alternativos=["12 objetos de WoW Vanilla que CASI NADIE tuvo",
                              "Sulfuras, Atiesh y el tanque negro: los objetos más RAROS de WoW Classic"],
        descripcion=desc,
        etiquetas=["wow classic", "objetos raros wow", "wow vanilla", "wow forever", "world of warcraft forever",
                   "sulfuras", "thunderfury", "trueno furioso", "atiesh", "quel'serrar", "rhok'delar", "tanque negro qiraji",
                   "señor del escarabajo", "deathcharger", "legendarios wow", "world of warcraft", "wow en español",
                   "cronicas de warcraft"],
        categoria=20, idioma="es", idioma_audio="es",
        miniatura="salida/miniatura.jpg", subtitulos="salida/wow_objetos_raros.srt",
    )
    assert len(desc) < 5000, len(desc)
    json.dump(d, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"youtube.json: {len(caps)} capítulos, {len(canales)} canales de gameplay, descripción de {len(desc)} caracteres")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
