# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_melina_atrocidades (27-oct-2026): eldenring.fandom.com (API imageinfo por archivo y
pageimages por página) a pegatinas/<slug>.png (≤ 700 px) y pantallas/<slug>.jpg (≥ 1000 px); fuentes en */_fuentes.txt.
Las de personajes que ya bajaron Malenia/Ranni/Miquella se copian de sus carpetas (misma imagen real, no es una escena).
    python bajar_pegatinas.py
"""
import io
import json
import os
import shutil
import urllib.parse
import urllib.request

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
PAN = os.path.join(AQUI, "pantallas")
VID = os.path.dirname(AQUI)
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
API = "https://eldenring.fandom.com/api.php?"

ARCHIVOS = {   # slug: archivo de la wiki
    "melina": "ER_Render_Melina.png", "melina_media": "ER_Render_Melina05.png", "melina_capucha": "Melina_Cloacked.png",
    "melina_retrato": "Melina-portrait.png", "melina_wiki": "Melina.webp", "melina_fuego": "Melina_on_fire.jpg",
    "silbato": "ER_Icon_Tool_Spectral_Steed_Whistle.png", "hoja_invocacion": "ER_Icon_weapon_Blade_of_Calling.png",
    "yesca_messmer": "ER_Icon_Key_Item_Messmer's_Kindling.png", "arbol_menor": "ER_Icon_Spell_Minor_Erdtree.png",
    "medallon_rold": "ER_Icon_Key_Item_Rold_Medallion.png", "llama_surge": "ER_Icon_Spell_Surge,_O_Flame!.png",
    "llama_burn": "ER_Icon_Spell_Burn,_O_Flame!.png", "frasco_rojo": "ER_Icon_Flask_crimson_tears_4.png",
    "frasco_azul": "ER_Icon_Flask_cerulean_tears_4.png", "ojo_sello": "C2180_Tattoo_a.png", "morgott": "Morgott_Icon.png",
    "lectora": "ER_NPC_Finger_Reader_Crone_(Stormhill)_(1.1).png", "gigante_fuego": "ER_Fire_Giant_(1.1).png",
    "olla_frenetica": "Frenzied_Flame_Pot.png",
}
PANTALLAS = {
    "forja1": "Eldenringmelinaforge1.jpg", "forja2": "Eldenringmelinaforge2.jpg", "forja3": "Eldenringmelinaforge3.jpg",
    "forja4": "Eldenringmelinaforge4.jpg", "arbol_arde": "Melina_burns_the_Erdtree.jpg", "frenesi1": "Eldenringddmelina1.jpg",
    "frenesi2": "Eldenringddmelina2.jpg", "frenesi_final": "Melina_during_the_Frenzied_Flame_ending.jpg",
    "melina_revela": "Melina_reveal.png", "melina_capa": "Melina_cloacked_2.png", "melina_render2": "ER_Render_Melina02.png",
    "melina_render3": "ER_Render_Melina03.png", "melina_render6": "ER_Render_Melina06.png", "cuarto_secreto": "Melina_Hidden_Room_2.jpg",
    "capital_ceniza": "ER_Leyndell,_Ashen_Capital.png", "capital": "ER_Leyndell,_Royal_Capital.png", "arbol": "Erdtree.jpg",
    "espinas": "ER_Erdtree_Thorns.png", "gigante": "ER_Fire_Giant.png", "picos": "ER_Erdtree_Avatar_Mountaintops.png",
    "tres_dedos": "Three_Fingers.webp", "invocada": "Eldenringmelinasummon.jpg",
}
PAGINAS = {   # slug: página (su imagen principal)
    "boc": "Boc the Seamster", "enia": "Finger Reader Enia", "torrentera": "Torrent", "tres_dedos_peg": "Three Fingers",
    "messmer_jefe": "Messmer the Impaler", "maliketh_jefe": "Maliketh, the Black Blade", "farum_azula": "Crumbling Farum Azula",
    "mesa_redonda": "Roundtable Hold", "forja": "Forge of the Giants", "picos_gigantes": "Mountaintops of the Giants",
    "camara_frenetica": "Frenzied Flame Proscription", "tercera_iglesia": "Third Church of Marika", "mariposa": "Smoldering Butterfly",
    "valquirias": "Millicent's Sisters", "reina_ojo": "Godskin Apostle", "cementerio": "Stranded Graveyard", "hyetta": "Hyetta",
    "llama_frenetica": "Frenzied Flame", "orden_aureo": "Golden Order", "dos_dedos_peg": "Two Fingers",
    "aldea_chamanes": "Shaman Village", "gurranq_peg": "Gurranq, Beast Clergyman",
}
COPIAS = {   # slug: (video, slug allí)
    "marika": ("er_malenia_atrocidades", "marika"), "radagon": ("er_malenia_atrocidades", "radagon"),
    "malenia": ("er_malenia_atrocidades", "malenia_icono"), "miquella": ("er_malenia_atrocidades", "miquella_nino"),
    "ranni": ("er_malenia_atrocidades", "ranni"), "godrick": ("er_malenia_atrocidades", "godrick"),
    "godfrey": ("er_malenia_atrocidades", "godfrey"), "millicent": ("er_malenia_atrocidades", "millicent"),
    "gideon": ("er_malenia_atrocidades", "gideon"), "godwyn": ("er_ranni_atrocidades", "godwyn"),
    "maliketh": ("er_ranni_atrocidades", "maliketh"), "espada_maliketh": ("er_ranni_atrocidades", "espada_maliketh"),
    "runa_muerte": ("er_ranni_atrocidades", "runa_muerte"), "muerte_destinada": ("er_ranni_atrocidades", "muerte_destinada"),
    "dos_dedos": ("er_ranni_atrocidades", "dos_dedos"), "cuchillo_negro": ("er_ranni_atrocidades", "cuchillo_negro"),
    "messmer": ("er_miquella_atrocidades", "messmer"),
}


def _json(q):
    return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(q), headers=UA), timeout=40))


def url_archivo(n):
    for p in _json(dict(action="query", titles="File:" + n, prop="imageinfo", iiprop="url", format="json"))["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]


def url_pagina(t):
    for p in _json(dict(action="query", titles=t, prop="pageimages", piprop="original", redirects=1, format="json"))["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]


def guardar(url, ruta, peg):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
    im = Image.open(io.BytesIO(data))   # vienen en WebP aunque digan .png: reabrir y guardar con PIL
    if peg:
        im = im.convert("RGBA")
        im.thumbnail((700, 700), Image.LANCZOS)
        im.save(ruta)
    else:
        im = im.convert("RGB")
        if im.width > 2400:
            im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
        im.save(ruta, quality=92)
    return im.size


def main():
    os.makedirs(PEG, exist_ok=True)
    os.makedirs(PAN, exist_ok=True)
    fuentes = {PEG: [], PAN: []}
    for s, (v, o) in COPIAS.items():
        src = os.path.join(VID, v, "pegatinas", o + ".png")
        dst = os.path.join(PEG, s + ".png")
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            fuentes[PEG].append(f"{s}\tcopia de videos/{v}/pegatinas/{o}.png")
    trabajos = [(s, os.path.join(PEG, s + ".png"), lambda n=n: url_archivo(n), True) for s, n in ARCHIVOS.items()]
    trabajos += [(s, os.path.join(PAN, s + ".jpg"), lambda n=n: url_archivo(n), False) for s, n in PANTALLAS.items()]
    trabajos += [(s, os.path.join(PEG, s + ".png"), lambda t=t: url_pagina(t), True) for s, t in PAGINAS.items()]
    for slug, ruta, buscar, peg in trabajos:
        if os.path.exists(ruta):
            continue
        try:
            url = buscar()
            if not url:
                print("SIN IMAGEN", slug)
                continue
            tam = guardar(url, ruta, peg)
            fuentes[PEG if peg else PAN].append(f"{slug}\t{url}")
            print("ok", slug, tam)
        except Exception as e:                       # noqa: BLE001
            print("ERROR", slug, e)
    for d, fs in fuentes.items():
        with open(os.path.join(d, "_fuentes.txt"), "a", encoding="utf-8") as f:
            f.write("\n".join(fs) + ("\n" if fs else ""))


if __name__ == "__main__":
    main()
