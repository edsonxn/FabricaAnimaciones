# -*- coding: utf-8 -*-
"""Pegatinas REALES de majora_mask (23-oct-2026): imágenes oficiales de zelda.fandom.com (API imageinfo) a pegatinas/<slug>.png
y las 24 máscaras a pegatinas/mascaras/NN_<slug>.png; fuentes en pegatinas/_fuentes.txt. Fotos de personas: Wikipedia.
    python bajar_pegatinas.py
"""
import json
import os
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}

ZELDA = {
    "link": "MM_Link_Artwork.png", "link_epona": "MM_Link_Epona_Artwork.png", "link_tatl": "MM_Link_Tatl_Artwork.png",
    "link_deku": "MM_Deku_Link_Artwork.png", "skull_kid": "MM_Skull_Kid_Artwork.png",
    "skull_kid_oot": "OoT_Skull_Kid_Artwork.png", "majora": "MM_Majora's_Mask_Render.png", "tatl": "MM_Tatl_Artwork.png",
    "tael": "MM_Tael_Artwork.png", "vendedor": "MM_Happy_Mask_Salesman_Artwork.png", "luna": "MM_Moon_intro.png",
    "cartero": "MM_Postman_Artwork.png", "madame_aroma": "MM_Madame_Aroma_Artwork.png", "romani": "MM_Romani_Artwork.png",
    "cremia": "MM_Cremia_Artwork.png", "ellos": "MM_Them.jpg", "anju": "MM_Anju_Artwork.png", "kafei": "MM_Kafei_Artwork.png",
    "kafei_nino": "MM_Kafei_Keaton_Mask_Artwork.png", "mascara_sol": "MM_SunMask.png", "darmani": "MM_Darmani_III_Artwork.png",
    "mikau": "MM_Mikau_Artwork.png", "tumba_mikau": "MM_MikauGrave.png", "lulu": "MM_Lulu_Artwork.png",
    "mayordomo": "MM_Deku_Butler_Artwork.png", "hijo_mayordomo": "MM_Deku_Butler's_Son_Model.png", "rey_deku": "MM_Deku_King_Artwork.png",
    "link_fiera": "MM_Fierce_Deity_Link_Artwork.png", "buho": "MM_OwlStatueClosed.png", "ocarina": "MM_Ocarina_of_Time_Icon.png",
    "bombers": "MM_Bombers_Artwork.png", "cuaderno": "MM_Bombers'_Notebook_Icon.png", "ciudad_reloj": "MM_Clock_Town_Artwork.png",
    "nino_majora": "MM_Moon_Child_Majora_Model.png", "nino_odolwa": "MM_Moon_Child_Odolwa_Model.png",
    "nino_goht": "MM_Moon_Child_Goht_Model.png", "nino_gyorg": "MM_Moon_Child_Gyorg_Model.png",
    "nino_twinmold": "MM_Moon_Child_Twinmold_Model.png", "link_ocarina": "MM_Link_Playing_the_Ocarina_of_Time.png",
    "link_goron": "MM_Link_Goron_Mask_Artwork.png", "reloj_sol": "MM_Termina_Clock_Sun.png",
}
# las 24 máscaras en el orden de la pantalla de máscaras
MASCARAS = ["Postman's_Hat", "All-Night_Mask", "Blast_Mask", "Stone_Mask", "Great_Fairy's_Mask", "Deku_Mask",
            "Keaton_Mask", "Bremen_Mask", "Bunny_Hood", "Don_Gero's_Mask", "Mask_of_Scents", "Goron_Mask",
            "Romani's_Mask", "Circus_Leader's_Mask", "Kafei's_Mask", "Couple's_Mask", "Mask_of_Truth", "Zora_Mask",
            "Kamaro's_Mask", "Gibdo_Mask", "Garo's_Mask", "Captain's_Hat", "Giant's_Mask", "Fierce_Deity's_Mask"]
WIKI = {   # personas y hardware (Wikipedia en inglés, imagen principal de la página)
    "aonuma": "Eiji Aonuma", "miyamoto": "Shigeru Miyamoto", "koizumi": "Yoshiaki Koizumi", "kondo": "Koji Kondo",
    "expansion_pak": "Expansion Pak", "vrs": "Hey You, Pikachu!", "lola": "Run Lola Run",
}


def _json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def _bajar(url, ruta):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(ruta, "wb") as f:
        f.write(r.read())


def zelda_url(nombre):
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", format="json"))
    for p in _json("https://zelda.fandom.com/api.php?" + q)["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]
    return None


def wiki_url(titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageimages", piprop="original", redirects=1, format="json"))
    for p in _json("https://en.wikipedia.org/w/api.php?" + q)["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]
    return None


def main():
    os.makedirs(os.path.join(PEG, "mascaras"), exist_ok=True)
    fuentes = []
    trabajos = [(s, os.path.join(PEG, s + os.path.splitext(n)[1].lower()), lambda n=n: zelda_url(n)) for s, n in ZELDA.items()]
    for i, m in enumerate(MASCARAS):
        def u(m=m):
            return zelda_url(f"MM_{m}_Icon.png") or zelda_url(f"MM3D_{m}_Icon.png")
        trabajos.append((f"mascaras/{i + 1:02d}_{m.lower()}", os.path.join(PEG, "mascaras", f"{i + 1:02d}.png"), u))
    for s, t in WIKI.items():
        trabajos.append((s, os.path.join(PEG, s + ".jpg"), lambda t=t: wiki_url(t)))
    for slug, ruta, buscar in trabajos:
        if os.path.exists(ruta):
            continue
        try:
            url = buscar()
            if not url:
                print("SIN IMAGEN", slug)
                continue
            if not ruta.endswith(".png") and url.lower().split("?")[0].endswith(".png"):
                ruta = os.path.splitext(ruta)[0] + ".png"
            _bajar(url, ruta)
            fuentes.append(f"{slug}\t{url}")
            print("ok", slug)
        except Exception as e:                       # noqa: BLE001
            print("ERROR", slug, e)
    with open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8") as f:
        f.write("\n".join(fuentes) + ("\n" if fuentes else ""))


if __name__ == "__main__":
    main()
