# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_sinluz_atrocidades (16-nov-2026; nombres en _investigacion/dossier.md):
pageimages por página) a pegatinas/<slug>.png (≤ 700 px) y pantallas/<slug>.jpg (≥ 1000 px); fuentes en */_fuentes.txt.
Las que ya bajaron Malenia/Ranni/Miquella se copian de sus carpetas (misma imagen real, no es una escena).
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

ARCHIVOS = {"aguja_miquella": "ER Icon Key Item Miquella's Needle.png", "rencor_rykard": "ER Icon Spell Rykard's Rancor.png", "pesar_shabriri": "ER Icon Talisman Shabriri's Woe.png"}
PANTALLAS = {}
PAGINAS_NUEVAS = {   # escenas nuevas p5c/p4c/p3d/p3e/p2d/p1d (16-nov, relevo 1)
    "millicent": "Millicent", "protesis_millicent": "Millicent's Prosthesis", "pesar_daedicar": "Daedicar's Woe",
    "mascara_consorte": "Consort's Mask", "aguja_miquella": "Miquella's Needle", "placidusax": "Dragonlord Placidusax",
    "caballero_tanith": "Tanith's Knight",
}
PANT_NUEVAS = {"elphael": "Elphael, Brace of the Haligtree", "zamor": "Ruins of Zamor"}
PAGINAS = {   # slug: página de la wiki inglesa (pageimages = imagen del infobox; MIRAR en pegatinas_check: algunas son paisajes)
    "tanith": "Tanith", "rykard": "Rykard, Lord of Blasphemy", "serpiente": "God-Devouring Serpent", "rya": "Rya",
    "istvan": "Old Knight Istvan", "rileigh": "Rileigh the Idle", "juno": "Juno Hoslow", "disparo_magma": "Magma Shot",
    "hoja_serpiente": "Serpentbone Blade", "camafeo": "Taker's Cameo", "rencor_rykard": "Rykard's Rancor",
    "recuerdo_blasfemo": "Remembrance of the Blasphemous", "runa_rykard": "Rykard's Great Rune", "tonico": "Tonic of Forgetfulness",
    "uva_shabriri": "Shabriri Grape", "uva_dactilograma": "Fingerprint Grape", "sello_frenetico": "Frenzied Flame Seal",
    "piedra_frenetica": "Frenzyflame Stone", "pesar_shabriri": "Shabriri's Woe", "marioneta_nepheli": "Nepheli Loux Puppet",
    "marioneta_zampaheces": "Dung Eater Puppet", "marioneta_therolina": "Finger Maiden Therolina Puppet",
    "ambar_estelar": "Amber Starlight", "zampaheces": "Dung Eater", "runa_nonatos": "Great Rune of the Unborn",
    "recuerdo_luna": "Remembrance of the Full Moon Queen", "lagrima_larval": "Larval Tear", "mausoleo": "Walking Mausoleum",
    "sobretodo_mausoleo": "Mausoleum Surcoat", "runa_reparadora": "Mending Rune of the Fell Curse", "maldicion_semillero": "Seedbed Curse",
    "shabriri": "Shabriri", "favor_sangre": "Lord of Blood's Favor", "medalla_sangre": "Pureblood Knight's Medal",
    "recuerdo_rennala_jefa": "Rennala, Queen of the Full Moon", "raiz_mortuoria": "Deathroot",
}
PAGINAS_PANT = {   # imágenes grandes para pant() (paisajes del infobox)
    "mansion_volcan": "Volcano Manor", "capital_cinerea": "Leyndell, Ashen Capital", "tres_hermanas": "Three Sisters",
    "academia": "Academy of Raya Lucaria", "santuario_bestia": "Bestial Sanctum", "iglesia_inhibicion": "Church of Inhibition",
    "subsuelo": "Subterranean Shunning-Grounds", "monte_gelmir": "Mt. Gelmir", "capilla_espera": "Chapel of Anticipation",
}
COPIAS = {   # slug: (video, slug allí) — misma imagen real ya bajada en videos anteriores de Runa
    "seluvis": ("er_ranni_atrocidades", "seluvis"), "pocion_seluvis": ("er_ranni_atrocidades", "pocion_seluvis"),
    "brebaje": ("er_ranni_atrocidades", "brebaje"), "marioneta_dolores": ("er_ranni_atrocidades", "marioneta_dolores"),
    "marioneta_jarwight": ("er_ranni_atrocidades", "marioneta_jarwight"), "nepheli": ("er_ranni_atrocidades", "nepheli"),
    "pidia": ("er_ranni_atrocidades", "pidia"), "ranni": ("er_ranni_atrocidades", "ranni"), "ranni_npc": ("er_ranni_atrocidades", "ranni_npc"),
    "gurranq": ("er_ranni_atrocidades", "gurranq"), "raiz": ("er_ranni_atrocidades", "raiz"), "maliketh": ("er_melina_atrocidades", "maliketh"),
    "maliketh_jefe": ("er_melina_atrocidades", "maliketh_jefe"), "runa_muerte": ("er_ranni_atrocidades", "runa_muerte"),
    "gideon": ("er_godrick_atrocidades", "gideon"), "sellen": ("er_radahn_atrocidades", "sellen"), "rennala": ("er_godrick_atrocidades", "rennala"),
    "radahn": ("er_radahn_atrocidades", "radahn_render"), "runa_radahn": ("er_radahn_atrocidades", "runa_radahn"),
    "recuerdo_azote": ("er_radahn_atrocidades", "recuerdo_azote"), "nokron": ("er_radahn_atrocidades", "nokron"),
    "estrellas": ("er_radahn_atrocidades", "estrellas_colapso"), "leonard": ("er_radahn_atrocidades", "leonard"),
    "hyetta": ("er_melina_atrocidades", "hyetta"), "vyke": ("er_mohg_atrocidades", "vyke"), "irina": ("er_godrick_atrocidades", "irina"),
    "edgar": ("er_godrick_atrocidades", "edgar"), "varre": ("er_godrick_atrocidades", "varre"), "varre_cara": ("er_mohg_atrocidades", "varre_cara"),
    "pano_limpio": ("er_mohg_atrocidades", "pano_limpio"), "pano_rojo": ("er_mohg_atrocidades", "pano_rojo"), "mohg": ("er_mohg_atrocidades", "mohg"),
    "melina": ("er_melina_atrocidades", "melina"), "melina_retrato": ("er_melina_atrocidades", "melina_retrato"),
    "melina_fuego": ("er_melina_atrocidades", "melina_fuego"), "forja": ("er_melina_atrocidades", "forja"),
    "gigante_fuego": ("er_melina_atrocidades", "gigante_fuego"), "picos_gigantes": ("er_melina_atrocidades", "picos_gigantes"),
    "llama_frenetica": ("er_melina_atrocidades", "llama_frenetica"), "tres_dedos": ("er_melina_atrocidades", "tres_dedos_peg"),
    "camara_frenetica": ("er_melina_atrocidades", "camara_frenetica"), "torrentera": ("er_melina_atrocidades", "torrentera"),
    "medallon_rold": ("er_melina_atrocidades", "medallon_rold"), "morgott": ("er_morgott_atrocidades", "morgott_icono"),
    "recuerdo_injertado": ("er_godrick_atrocidades", "recuerdo_injertado"), "godrick": ("er_godrick_atrocidades", "godrick"),
    "enia": ("er_godrick_atrocidades", "enia"), "marika": ("er_godrick_atrocidades", "marika"), "radagon": ("er_mohg_atrocidades", "radagon"),
    "yura": ("er_mohg_atrocidades", "yura"), "farum_azula": ("er_melina_atrocidades", "farum_azula"), "mesa_redonda": ("er_melina_atrocidades", "mesa_redonda"),
    "miquella": ("er_godrick_atrocidades", "miquella"), "malenia": ("er_godrick_atrocidades", "malenia"), "godwyn": ("er_godrick_atrocidades", "godwyn"),
    "messmer": ("er_godrick_atrocidades", "messmer"), "godfrey": ("er_godrick_atrocidades", "godfrey"), "orden_aureo": ("er_melina_atrocidades", "orden_aureo"),
    "arbol_menor": ("er_melina_atrocidades", "arbol_menor"), "llama_burn": ("er_melina_atrocidades", "llama_burn"),
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
    trabajos += [(s, os.path.join(PAN, s + ".jpg"), lambda t=t: url_pagina(t), False) for s, t in PAGINAS_PANT.items()]
    trabajos += [(s, os.path.join(PEG, s + ".png"), lambda t=t: url_pagina(t), True) for s, t in PAGINAS_NUEVAS.items()]
    trabajos += [(s, os.path.join(PAN, s + ".jpg"), lambda t=t: url_pagina(t), False) for s, t in PANT_NUEVAS.items()]
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
