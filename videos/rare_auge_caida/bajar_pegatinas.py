# -*- coding: utf-8 -*-
"""Pegatinas REALES de rare_auge_caida (28-oct-2026; receta de oot_remake_cambios/bajar_pegatinas.py): imagen principal de la
página de Wikipedia en inglés (`pilicense=any`: portadas, logos, consolas, retratos) o un archivo concreto de Wikimedia
Commons / Fandom. Guarda pegatinas/<slug>.<ext> (≤ 900 px) y las fuentes en pegatinas/_fuentes.txt; luego un mosaico
previews/pegatinas.jpg para MIRARLAS.
    python bajar_pegatinas.py
"""
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "FabricaAnimacionesPegatinas/1.1 (uso personal; python-urllib)"}

WIKI = {
    # consolas y empresas
    "zx_spectrum": "ZX Spectrum", "nes": "Nintendo Entertainment System", "snes": "Super Nintendo Entertainment System",
    "n64": "Nintendo 64", "gamecube": "GameCube", "gba": "Game Boy Advance", "xbox": "Xbox (console)", "x360": "Xbox 360",
    "kinect": "Kinect", "rare_logo": "Rare (company)", "ultimate_logo": "Ultimate Play the Game", "nintendo_logo": "Nintendo",
    "microsoft_logo": "Microsoft", "sgi": "Silicon Graphics", "free_radical": "Free Radical Design",
    "playtonic": "Playtonic Games", "expansion_pak": "Nintendo 64 accessories",
    # juegos
    "jetpac": "Jetpac", "atic_atac": "Atic Atac", "sabre_wulf": "Sabre Wulf", "knight_lore": "Knight Lore",
    "rc_pro_am": "R.C. Pro-Am", "battletoads": "Battletoads (video game)", "snake_rattle": "Snake Rattle 'n' Roll",
    "dkc": "Donkey Kong Country", "dkc2": "Donkey Kong Country 2: Diddy's Kong Quest", "ki": "Killer Instinct (1994 video game)",
    "goldeneye": "GoldenEye 007 (1997 video game)", "blast_corps": "Blast Corps", "dkr": "Diddy Kong Racing",
    "banjo_kazooie": "Banjo-Kazooie", "jfg": "Jet Force Gemini", "perfect_dark": "Perfect Dark", "dk64": "Donkey Kong 64",
    "banjo_tooie": "Banjo-Tooie", "conker": "Conker's Bad Fur Day", "sfa": "Star Fox Adventures",
    "ghoulies": "Grabbed by the Ghoulies", "kameo": "Kameo: Elements of Power", "pdz": "Perfect Dark Zero",
    "viva": "Viva Piñata (video game)", "nuts_bolts": "Banjo-Kazooie: Nuts & Bolts", "kinect_sports": "Kinect Sports",
    "rare_replay": "Rare Replay", "sot": "Sea of Thieves", "everwild": "Everwild", "yooka": "Yooka-Laylee",
    "timesplitters2": "TimeSplitters 2", "twelve_tales": "Conker's Bad Fur Day", "dinosaur_planet": "Dinosaur Planet (video game)",
    "goldeneye_xbla": "GoldenEye 007 (1997 video game)", "sabrewulf_gba": "Sabre Wulf (2004 video game)",
    "mr_pants": "It's Mr. Pants", "kinect_sports2": "Kinect Sports: Season Two", "avatars": "Xbox Avatars",
    # personas
    "tim_stamper": "Tim Stamper", "chris_stamper": "Chris Stamper", "miyamoto": "Shigeru Miyamoto",
    "yamauchi": "Hiroshi Yamauchi", "howard_lincoln": "Howard Lincoln", "ed_fries": "Ed Fries", "phil_spencer": "Phil Spencer (business executive)",
    "kirkhope": "Grant Kirkhope", "david_wise": "David Wise (composer)", "martin_hollis": "Martin Hollis",
    "gregg_mayles": "Gregg Mayles", "david_doak": "David Doak", "steve_mayles": "Steve Mayles",
    "pierce_brosnan": "Pierce Brosnan", "dkc3": "Donkey Kong Country 3: Dixie Kong's Double Trouble!",
    "activision_logo": "Activision", "matt_booty": "Matt Booty",
}
# personajes: imagen principal de la wiki de cada saga en Fandom (wiki, título)
FANDOM = {
    "donkey_kong": ("donkeykong", "Donkey Kong"), "diddy": ("donkeykong", "Diddy Kong"),
    "banjo": ("banjokazooie", "Banjo"), "kazooie": ("banjokazooie", "Kazooie"),
    "conker_personaje": ("conker", "Conker"), "joanna": ("perfectdark", "Joanna Dark"),
    "fox": ("starfox", "Fox McCloud"), "jetman": ("rare", "Jetman"), "sabreman": ("rare", "Sabreman"),
}
# archivos concretos (Commons) cuando la imagen de la página no sirve: slug -> URL de la API imageinfo o archivo
ARCHIVOS = {"microsoft_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Microsoft_logo_%282012%29.svg/960px-Microsoft_logo_%282012%29.svg.png",
            "x360": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Xbox-360-Pro-wController.jpg/960px-Xbox-360-Pro-wController.jpg",
            "expansion_pak": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/N64-Expansion-Pak.jpg/960px-N64-Expansion-Pak.jpg"}


def _json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def wiki_url(titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageimages", piprop="original", pilicense="any",
                                    redirects=1, format="json"))
    for p in _json("https://en.wikipedia.org/w/api.php?" + q)["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]
    return None


def _get(url, intentos=6):
    import time
    for k in range(intentos):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == intentos - 1:
                raise
            time.sleep(15 * (k + 1))


def wiki_urls(titulos):
    """Una consulta por cada 50 títulos -> {título pedido: URL original}."""
    out = {}
    for i in range(0, len(titulos), 45):
        lote = titulos[i:i + 45]
        q = urllib.parse.urlencode(dict(action="query", titles="|".join(lote), prop="pageimages", piprop="thumbnail",
                                        pithumbsize=960, pilicense="any", redirects=1, format="json"))
        j = json.loads(_get("https://en.wikipedia.org/w/api.php?" + q))["query"]
        alias = {t: t for t in lote}
        for r in j.get("normalized", []) + j.get("redirects", []):
            for t, v in list(alias.items()):
                if v == r["from"]:
                    alias[t] = r["to"]
        por = {p["title"]: p["thumbnail"]["source"] for p in j["pages"].values() if "thumbnail" in p}
        out.update({t: por.get(v) for t, v in alias.items()})
    return out


def fandom_url(wiki, titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageimages", piprop="original", redirects=1,
                                    format="json"))
    for p in json.loads(_get(f"https://{wiki}.fandom.com/api.php?" + q))["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]
    return None


def guardar(slug, url):
    data = _get(url)
    im = Image.open(io.BytesIO(data))
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    im.thumbnail((900, 900), Image.LANCZOS)
    ext = ".png" if im.mode == "RGBA" else ".jpg"
    ruta = os.path.join(PEG, slug + ext)
    im.save(ruta, quality=92) if ext == ".jpg" else im.save(ruta)
    return ruta


def svg_png(url):
    """Wikipedia sirve miniaturas PNG de los SVG: .../thumb/x/xy/Nombre.svg/800px-Nombre.svg.png"""
    if "/commons/" in url or "/en/" in url:
        partes = url.split("/")
        nombre = partes[-1]
        i = partes.index("wikipedia")
        thumb = "/".join(partes[:i + 2]) + "/thumb/" + "/".join(partes[i + 2:]) + f"/800px-{nombre}.png"
        return thumb
    return url


def mosaico():
    fs = sorted(f for f in os.listdir(PEG) if f.endswith((".png", ".jpg")))
    cols = 10
    W = 192
    hoja = Image.new("RGB", (cols * W, ((len(fs) + cols - 1) // cols) * (W + 22)), (40, 60, 50))
    d = ImageDraw.Draw(hoja)
    for k, f in enumerate(fs):
        im = Image.open(os.path.join(PEG, f)).convert("RGBA")
        im.thumbnail((W - 8, W - 8))
        x, y = (k % cols) * W, (k // cols) * (W + 22)
        hoja.paste(im, (x + (W - im.width) // 2, y + (W - im.height) // 2), im)
        d.text((x + 4, y + W + 2), f[:28], fill=(255, 255, 255))
    os.makedirs(os.path.join(AQUI, "previews"), exist_ok=True)
    hoja.save(os.path.join(AQUI, "previews", "pegatinas.jpg"), quality=82)


if __name__ == "__main__":
    os.makedirs(PEG, exist_ok=True)
    log = open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8")
    import time
    faltan = {s: t for s, t in WIKI.items() if not any(os.path.exists(os.path.join(PEG, s + e)) for e in (".png", ".jpg"))}
    urls = wiki_urls(sorted(set(faltan.values())))
    for slug, (wiki, tit) in FANDOM.items():
        if not any(os.path.exists(os.path.join(PEG, slug + e)) for e in (".png", ".jpg")):
            faltan[slug] = "fandom:" + tit
            try:
                urls["fandom:" + tit] = fandom_url(wiki, tit)
            except Exception as e:                   # noqa: BLE001
                print(f"  ✗ {slug}: {e}")
    for slug, titulo in faltan.items():
        try:
            url = ARCHIVOS.get(slug) or urls.get(titulo)
            if not url:
                print(f"  ✗ {slug}: sin imagen ({titulo})")
                continue
            r = guardar(slug, url)
            print(f"  {slug:16s} {os.path.basename(r)}  {url.split('?')[0][-60:]}", flush=True)
            log.write(slug + "\t" + url.split("?")[0] + "\n")
            time.sleep(6 if "wikimedia" in url else 1)
        except Exception as e:                       # noqa: BLE001
            print(f"  ✗ {slug}: {e}", flush=True)
    log.close()
    mosaico()
    print("previews/pegatinas.jpg")
