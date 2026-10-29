# -*- coding: utf-8 -*-
"""Baja las imágenes REALES del juego (warcraft.wiki.gg api.php; la web normal bloquea curl, la API no) a pegatinas/_orig/
y los iconos de objetos de Wowhead (nether.wowhead.com tooltip → icon) como pegatinas/_orig/icono_<icon>.jpg.
Escribe pegatinas/_fuentes.json (slug → URL). Uso (desde la carpeta del video): python _bajar_reales.py"""
import json
import os
import urllib.parse
import urllib.request

API = "https://warcraft.wiki.gg/api.php"
H = {"User-Agent": "FabricaBot/1.0"}
DST = "pegatinas/_orig"

# slug → archivo de la wiki (captura del modelo del juego o arte oficial de Blizzard)
ARCHIVOS = {
    "alexandros": "MograineDK.jpg",                       # Highlord Mograine de Naxxramas (caballero de la muerte a caballo)
    "alexandros_vivo": "Mograine Flashback.jpg",          # Alexandros vivo con la Crematoria (para el medallón)
    "alexandros_espiritu": "Mograine Spirit.jpg",         # espíritu de Alexandros, «La luz del alba» (WotLK)
    "renault": "Scarlet Commander Mograine.jpg",
    "darion": "Darion Mograine.jpg",
    "tirion": "Tirion Fordring.jpg",                      # ermitaño de Classic
    "tirion_highlord": "Tirion Coliseum.jpg",
    "taelan": "Taelan Fordring.jpg",
    "isillien": "Isillien1.jpg",
    "kelthuzad": "Kel'Thuzad.jpg",                        # arte oficial de Naxxramas (2006)
    "rey_exanime": "Lich King HoR.jpg",
    "eitrigg": "Eitrigg.jpg",
    "balnazzar": "Balnazzar.jpg",
    "dathrohan": "Dathrohan.jpg",
    "ribalimpia": "High Inquisitor Fairbanks.jpg",
    "magni": "Magni in Cataclysm.jpg",
    "zeliek": "Sir Zeliek.jpg",
    "korthazz": "Thane Korthazz.jpg",
    "blaumeux": "Lady Blaumeux.jpg",
    "myranda": "Myranda the Hag.jpg",
    "renfray": "Artist Renfray.jpg",
    "koltira": "Koltira Deathweaver.jpg",
    "thassarian": "Thassarian-ebonhold.jpg",
    "orbaz": "Orbaz Bloodbane.jpg",
    "maxwell": "Maxwell Tyrosus in Cataclysm.jpg",
    "barthilas": "Magistrate Barthilas CoT.jpg",
    "uther": "Uther Stratholme.jpg",
    "zabra": "Zabra Legion.jpg",
    "naxxramas": "Naxxramas.jpg",
    "capilla": "Light's Hope Chapel.jpg",
    "monasterio": "Scarlet Monastery 11.jpg",
    "stratholme": "Stratholme gates2.jpg",
    "acherus": "Acherus.jpg",
    "torre_taelan": "Taelan's Tower (Classic).jpg",
    "crematoria": "AshbringerModel.png",
    "crematoria_corrupta": "Corrupted Ashbringer hq.png",
    "agonia_escarcha": "FrostmourneLegion.png",
}
# slug → (id de objeto, rama de Wowhead)
ITEMS = {"crematoria": (13262, "classic"), "crematoria_corrupta": (22691, "classic"), "martillo_taelan": (14613, "classic"),
         "simbolo_honor": (14625, "classic"), "cuadro": (14679, "classic"), "obsequio": (14872, "classic"),
         "fragmento_alma": (51317, "wotlk"), "marca_fordring": (15411, "classic")}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60).read()


def url_archivo(f):
    q = API + "?" + urllib.parse.urlencode({"action": "query", "titles": "File:" + f, "prop": "imageinfo", "iiprop": "url",
                                            "format": "json"})
    pg = list(json.loads(get(q))["query"]["pages"].values())[0]
    return pg["imageinfo"][0]["url"] if "imageinfo" in pg else None


if __name__ == "__main__":
    os.makedirs(DST, exist_ok=True)
    fuentes = {}
    for slug, f in ARCHIVOS.items():
        u = url_archivo(f)
        if not u:
            print("FALTA", slug, f)
            continue
        ext = ".png" if f.lower().endswith(".png") else ".jpg"
        out = os.path.join(DST, slug + ext)
        if not os.path.exists(out):
            open(out, "wb").write(get(u))
        fuentes[slug] = u.split("?")[0]
    iconos = {}
    for slug, (iid, rama) in ITEMS.items():
        d = json.loads(get(f"https://nether.wowhead.com/{rama}/tooltip/item/{iid}?locale=0"))
        ic = d["icon"]
        u = f"https://wow.zamimg.com/images/wow/icons/large/{ic}.jpg"
        out = os.path.join(DST, f"icono_{ic}.jpg")
        if not os.path.exists(out):
            open(out, "wb").write(get(u))
        iconos[slug] = ic
        fuentes["icono_" + slug] = u
        fuentes["icono_" + slug + "_item"] = f"https://www.wowhead.com/{rama}/item={iid} ({d['name']})"
    json.dump(fuentes, open("pegatinas/_fuentes.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(ARCHIVOS), "imágenes,", len(iconos), "iconos:", iconos)
