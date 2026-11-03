# -*- coding: utf-8 -*-
"""Pegatinas REALES de pokemon_rojo_azul (3-nov-2026): arte oficial y lugares de Bulbapedia (imagen de la página),
archivos exactos de archives.bulbagarden.net, y personas, cajas y aparatos de Wikipedia. Receta de n64_secretos/bajar_pegatinas.py.
Fuentes en pegatinas/_fuentes.txt.
    python bajar_pegatinas.py            baja lo que falte (no repite lo que ya existe)
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas; jairedson5 at gmail)"}

WP = "https://en.wikipedia.org/w/api.php"
BP = "https://bulbapedia.bulbagarden.net/w/api.php"
BA = "https://archives.bulbagarden.net/w/api.php"

# slug: título de en.wikipedia (imagen del infobox)
WIKI = {
    "miyamoto": "Shigeru Miyamoto", "iwata": "Satoru Iwata", "yamauchi": "Hiroshi Yamauchi",
    "weatherford": "Carole Boston Weatherford",
    "game_boy": "Game Boy", "cable_link": "Game Link Cable", "c_rojo_azul": "Pokémon Red and Blue",
    "c_amarillo": "Pokémon Yellow", "c_oro_plata": "Pokémon Gold and Silver", "c_rojofuego": "Pokémon FireRed and LeafGreen",
    "c_dq2": "Dragon Quest II", "ultraseven": "Ultraseven", "corocoro": "CoroCoro Comic", "nintendo_power": "Nintendo Power",
    "game_freak": "Game Freak", "creatures": "Creatures Inc.", "daifuku": "Daifuku", "switch2": "Nintendo Switch 2",
    "creepypasta": "Creepypasta", "franquicia": "Pokémon",
}
# slug: página de Bulbapedia (su imagen principal = arte oficial de Sugimori / mapa del lugar)
BULBA = {
    "bulbasaur": "Bulbasaur (Pokémon)", "charmander": "Charmander (Pokémon)", "squirtle": "Squirtle (Pokémon)",
    "pikachu": "Pikachu (Pokémon)", "raichu": "Raichu (Pokémon)", "clefairy": "Clefairy (Pokémon)", "rhydon": "Rhydon (Pokémon)",
    "victreebel": "Victreebel (Pokémon)", "mew": "Mew (Pokémon)", "mewtwo": "Mewtwo (Pokémon)", "ditto": "Ditto (Pokémon)",
    "dragonite": "Dragonite (Pokémon)", "alakazam": "Alakazam (Pokémon)", "gengar": "Gengar (Pokémon)", "gastly": "Gastly (Pokémon)",
    "jynx": "Jynx (Pokémon)", "tauros": "Tauros (Pokémon)", "exeggutor": "Exeggutor (Pokémon)", "arcanine": "Arcanine (Pokémon)",
    "gyarados": "Gyarados (Pokémon)",
    "oak": "Professor Oak", "lance": "Lance", "red": "Red (game)", "blue": "Blue (game)", "ash": "Ash Ketchum", "gary": "Gary Oak",
    "missingno": "MissingNo.", "lavanda": "Lavender Town", "canela": "Cinnabar Island", "ss_anne": "S.S. Anne",
    "mansion_azulona": "Celadon Mansion", "cueva_celeste": "Cerulean Cave", "verde": "Viridian City", "carmin": "Vermilion City",
    "paleta": "Pallet Town", "azulona": "Celadon City",
    "pokeball": "Poké Ball", "masterball": "Master Ball", "rare_candy": "Rare Candy", "galleta_lava": "Lava Cookie",
    "pokedex": "Pokédex", "medallas": "Badge",
    "alto_mando": "Elite Four", "capsule_monsters": "Capsule Monsters",
    # personas de Game Freak/Creatures (Wikipedia no tiene foto libre; Bulbapedia sí)
    "tajiri": "Satoshi Tajiri", "sugimori": "Ken Sugimori", "morimoto": "Shigeki Morimoto", "ishihara": "Tsunekazu Ishihara",
    "nishida": "Atsuko Nishida",
}
# slug: archivo exacto de archives.bulbagarden.net (arte oficial a buen tamaño)
BA_ARCH = {
    "a_pikachu": "0025Pikachu.png", "a_mew": "0151Mew.png", "a_rhydon": "0112Rhydon.png", "a_ditto": "0132Ditto.png",
    "a_jynx": "0124Jynx.png", "a_dragonite": "0149Dragonite.png", "a_mewtwo": "0150Mewtwo.png", "a_clefairy": "0035Clefairy.png",
    "tajiri_joven": "Young Satoshi Tajiri.png", "camion": "Mew Under Truck.jpg", "capsule_portada": "Capsule Monsters Cover.jpg",
    "guia_rgb": "RGB guidebook.jpg", "ishihara_revista": "Tsunekaz Ishihara magazine interview.jpg",
    "morimoto_2016": "Shigeki Morimoto 2016.jpg", "tajiri_2016": "Satoshi Tajiri 2016.jpg",
}


def _abrir(url, timeout):
    for i in range(5):                                      # Wikimedia corta con 429 si se va rápido: espera y reintenta
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == 4:
                raise
            time.sleep(20 * (i + 1))


def _json(url):
    return json.load(_abrir(url, 40))


def _bajar(url, ruta):
    with _abrir(url, 60) as r, open(ruta, "wb") as f:
        f.write(r.read())


def imagen(base, titulo):
    """Archivo principal de la página: `page_image` de pageprops (incluye carátulas no libres, que pageimages no da)."""
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageprops|pageimages", piprop="name", format="json", redirects=1))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        pp = p.get("pageprops") or {}
        nombre = pp.get("page_image") or pp.get("page_image_free") or p.get("pageimage")
        if not nombre:
            return None
        # Bulbapedia guarda sus archivos en archives.bulbagarden.net
        return archivo(BA if "bulbapedia" in base else base, nombre)


def archivo(base, nombre):
    """URL del archivo; si es SVG, su PNG de 1200 px."""
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", iiurlwidth=1200, format="json"))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        u = ii.get("url")
        return ii.get("thumburl") if u and u.lower().split("?")[0].endswith(".svg") else u


def _existe(slug):
    return next((f for f in os.listdir(PEG) if os.path.splitext(f)[0] == slug), None)


def main():
    os.makedirs(PEG, exist_ok=True)
    reg_ruta = os.path.join(PEG, "_fuentes.txt")
    reg = open(reg_ruta, encoding="utf-8").read().splitlines() if os.path.exists(reg_ruta) else []
    hechos = {r.split(":", 1)[0] for r in reg}
    tareas = [(s, WP, "Wikipedia", t, False, 3) for s, t in WIKI.items()]
    tareas += [(s, BP, "Bulbapedia", t, False, 1) for s, t in BULBA.items()]
    tareas += [(s, BA, "archives.bulbagarden.net", t, True, 1) for s, t in BA_ARCH.items()]
    sin = []
    for slug, base, org, tit, es_archivo, pausa in tareas:
        if _existe(slug) and slug in hechos:
            continue
        try:
            u = archivo(base, tit) if es_archivo else imagen(base, tit)
            if not u:
                print("SIN", slug, tit)
                sin.append(slug)
                continue
            ext = os.path.splitext(urllib.parse.urlparse(u).path)[1].lower() or ".png"
            if ext not in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                print("FORMATO", slug, u)
                sin.append(slug)
                continue
            ext = ".jpg" if ext == ".jpeg" else ext
            r = os.path.join(PEG, slug + ext)
            if not os.path.exists(r):
                _bajar(u, r)
            reg = [x for x in reg if not x.startswith(slug + ":")] + [f"{slug}: {org} «{tit}» {u}"]
            print("ok", slug, ext, os.path.getsize(r) // 1024, "KB")
        except Exception as e:
            print("ERR", slug, e)
            sin.append(slug)
        time.sleep(pausa)
    with open(reg_ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(reg))
    print(f"\n{len(tareas) - len(sin)}/{len(tareas)} · sin imagen: {', '.join(sin) or '-'}")


if __name__ == "__main__":
    main()
