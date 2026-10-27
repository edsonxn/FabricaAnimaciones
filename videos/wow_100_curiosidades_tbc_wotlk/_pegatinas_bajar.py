# -*- coding: utf-8 -*-
"""Pegatinas REALES de wow_100_curiosidades_tbc_wotlk (24-oct-2026): imagen principal de la página de Wowpedia en Fandom
(API pageimages; warcraft.wiki.gg bloquea scripts) -> pegatinas/<slug>.png (RGBA, lado mayor <= 700 px); fuentes en
pegatinas/_fuentes.txt. Si la página no trae imagen, prueba list=allimages con el prefijo. MIRAR el mosaico antes de usarlas.
    python _pegatinas_bajar.py [slug ...]        (sin slugs: todas las que falten)
"""
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
API = "https://wowpedia.fandom.com/api.php?"

# slug -> título de Wowpedia (o "File:..." para una imagen concreta)
TITULOS = {
    # ---- MG «los 5 héroes de la expedición» (c100)
    "danath": "Danath Trollbane", "khadgar": "Khadgar", "kurdran": "Kurdran Wildhammer", "alleria": "Alleria Windrunner",
    "turalyon": "Turalyon",
    # ---- Península del Fuego Infernal
    "guldan": "Gul'dan", "segador_vil": "Fel Reaver", "aggonis": "Aggonis", "kazzak": "Doom Lord Kazzak",
    "caminante": "Doomwalker", "magtheridon": "Magtheridon", "orco_vil": "Fel orc", "kargath": "Kargath Bladefist",
    "nethekurse": "Grand Warlock Nethekurse",
    # ---- Marisma de Zangar
    "telredor": "Telredor", "vashj": "Lady Vashj", "esporelin": "Sporeling", "murcielespora": "Tiny Sporebat",
    "rondador": "The Lurker Below",
    # ---- Terokkar y Shattrath
    "murmur": "Murmur", "auchindoun": "Auchindoun", "arakkoa": "Arakkoa", "terokk": "Terokk", "haris": "Haris Pilton",
    "griftah": "Griftah", "l70etc": "Elite Tauren Chieftain", "vorenthal": "Voren'thal the Seer", "adal": "A'dal",
    "aldor": "Aldor", "zephyr": "Zephyr",
    # ---- Nagrand
    "oshugun": "Oshu'gun", "kure": "K'ure", "garrosh": "Garrosh Hellscream", "geyah": "Greatmother Geyah", "thrall": "Thrall",
    "corki": "Corki", "gurgthock": "Gurgthock", "mogor": "Mogor", "wodin": "Wodin the Troll-Servant", "halaa": "Halaa",
    "talbuk": "Talbuk",
    # ---- Montañas Filospada
    "gruul": "Gruul the Dragonkiller", "sablemane": "Baron Sablemane", "sabellian": "Sabellian",
    "gorgrom": "Gorgrom the Dragon-Eater", "goc": "Goc", "rexxar": "Rexxar", "misha": "Misha", "leoroxx": "Leoroxx",
    "ogrila": "Ogri'la", "vimgol": "Vim'gol the Vile", "toshley": "Toshley", "smiles": "Smiles O'Byron",
    # ---- Tormenta Abisal
    "area52": "Area 52", "ecodomo": "Eco-Dome Midrealm", "etereo": "Ethereal", "culuthas": "Culuthas",
    "kaelthas": "Kael'thas Sunstrider", "vargoth": "Archmage Vargoth", "dimensius": "Dimensius the All-Devouring",
    "saeed": "Captain Saeed",
    # ---- Valle Sombraluna
    "mano_guldan": "Hand of Gul'dan", "illidan": "Illidan Stormrage", "maiev": "Maiev Shadowsong", "akama": "Akama",
    "skyshatter": "Captain Skyshatter", "draco_abisal": "Nether drake", "teron": "Teron Gorefiend",
    # ---- Quel'Thalas, islas, Karazhan, Cavernas
    "muru": "M'uru", "velen": "Velen", "darkhan": "Dar'Khan Drathir", "arthas": "Arthas Menethil",
    "sylvanas": "Sylvanas Windrunner", "harrison": "Harrison Jones", "kessel": "Kessel", "exodar": "Exodar",
    "sironas": "Sironas", "aran": "Shade of Aran", "medivh": "Medivh", "kelthuzad": "Kel'Thuzad",
    "whitemane": "Sally Whitemane", "renault": "Renault Mograine", "jimmy": "Jimmy Vishas", "herod": "Herod",
    # ======== RASGANORTE (tramo 7, 26-oct-2026)
    # ---- Tundra Boreal
    "saurfang": "Varok Saurfang", "lathorius": "Archdruid Lathorius", "mamut": "Mammoth", "nesingwary": "Hemet Nesingwary",
    "mechazod": "Gearmaster Mechazod", "mecagnomo": "Mechagnome", "keristrasza": "Keristrasza", "malygos": "Malygos",
    "nexo": "The Nexus", "taunka": "Taunka",
    # ---- Fiordo Aquilonal
    "ymiron": "King Ymiron", "vrykul": "Vrykul", "ingvar": "Ingvar the Plunderer", "annhylde": "Annhylde the Caller",
    "valkyr": "Val'kyr", "boticario": "Royal Apothecary Society",
    # ---- Cementerio de Dragones
    "alexstrasza": "Alexstrasza", "reposo_dragon": "Wyrmrest Temple", "galakrond": "Galakrond", "naxxramas": "Naxxramas",
    "bolvar": "Bolvar Fordragon", "dranosh": "Dranosh Saurfang", "putress": "Grand Apothecary Putress", "varian": "Varian Wrynn",
    "puerta_colera": "Angrathar the Wrathgate", "orik": "Orik Trueheart", "malganis": "Mal'Ganis", "muradin": "Muradin Bronzebeard",
    "agonia_escarcha": "Frostmourne", "abbendis": "Grand General Abbendis",
    # ---- Colinas Pardas
    "ursoc": "Ursoc", "vordrassil": "Vordrassil", "furbolg": "Furbolg", "yogg": "Yogg-Saron", "gryan": "Gryan Stoutmantle",
    "arugal": "Archmage Arugal", "huargen": "Worgen",
    # ---- Zul'Drak (MG altares: los dioses)
    "rhunok": "Rhunok", "quetzlun": "Quetz'lun", "sseratus": "Sseratus", "akali": "Akali", "harkoa": "Har'koa",
    "drakkari": "Drakkari", "mamtoth": "Mam'toth", "gymer": "Gymer", "drakuru": "Drakuru", "rey_exanime": "Lich King",
    "voltarus": "Voltarus", "vladof": "Vladof the Butcher", "tharonja": "The Prophet Tharon'ja",
    # ---- Sholazar
    "freya": "Freya", "etymidian": "Etymidian", "loquenahak": "Loque'nahak", "oraculo": "Oracles",
    "corazon_frenetico": "Frenzyheart tribe", "protodraco_verde": "Green Proto-Drake",
    # ---- Cumbres Tormentosas (MG paradero: los tres Barbabronce)
    "k3": "K3", "hyldnir": "Hyldnir", "hodir": "Hodir", "thorim": "Thorim", "sif": "Sif", "loken": "Loken",
    "ppt": "Reins of the Time-Lost Proto-Drake", "vyragosa": "Vyragosa", "brann": "Brann Bronzebeard",
    "magni": "Magni Bronzebeard", "algalon": "Algalon the Observer", "mimiron": "Mimiron",
    "cabeza_mimiron": "Mimiron's Head",
    # ---- Dalaran, Canto de Cristal, Conquista del Invierno
    "crater_dalaran": "Dalaran Crater", "dalaran": "Dalaran", "korialstrasz": "Korialstrasz", "rhonin": "Rhonin",
    "vereesa": "Vereesa Windrunner", "minigob": "Minigob Manabonk", "archavon": "Archavon the Stone Watcher",
    "demoledor": "Wintergrasp Demolisher",
    # ---- Corona de Hielo
    "caballero_negro": "The Black Knight", "sindragosa": "Sindragosa", "alamuerte": "Deathwing", "westwind": "Barean Westwind",
    "martillo_orgrim": "Orgrim's Hammer", "rompecielos": "The Skybreaker", "tirion": "Tirion Fordring", "uther": "Uther the Lightbringer",
    "jaina": "Jaina Proudmoore", "bridenbrad": "Crusader Bridenbrad", "remulos": "Remulos",
}
# 2.ª vuelta tras MIRAR el mosaico (24-oct): la imagen de la página era otra cosa (Illidan = estatua de Cenarius, Medivh = un
# cuervo, Kel'Thuzad torturando a Alexandros, Sablemane = el dragón) o una escena oscura/diminuta
TITULOS.update({
    "adal": "File:A'dal TCG.jpg", "akama": "File:Akama HS.jpg", "danath": "File:Force Commander Danath Trollbane TCG.jpg",
    "draco_abisal": "File:Nether Drake HS.jpg", "esporelin": "File:Sporeling.jpg", "geyah": "File:Greatmother Geyah HS.jpg",
    "kargath": "File:Kargath Bladefist HS.jpg", "kelthuzad": "File:Kel'thuzadhuman.jpg", "illidan": "File:Illidan Stormrage TCG.jpg",
    "medivh": "File:Medivh, the Guardian HS.jpg", "misha": "File:Rexxar and Misha BFA.jpg", "rexxar": "File:Rexxar TCG.jpg",
    "sablemane": "File:Baron Sablemane.jpg", "sylvanas": "File:Sylvanas Windrunner in the Ghostlands.jpg",
    "teron": "File:Teron Gorefiend TCG.jpg", "thrall": "File:Thrall (Nagrand).jpg", "turalyon": "File:General Turalyon TCG.jpg",
    "arthas": "File:ArthasFrostmourneRF.jpg",
})

# Rasganorte, 2.ª vuelta tras MIRAR previews/peg_01-02.jpg (26-oct): Muradin era un cuadro de Magni, el Caballero Negro una
# figura de juguete, el Rey Exánime hielo vacío, Yogg-Saron era Sara, Tirion un cómic en B/N; el resto, capturas oscuras/diminutas
TITULOS.update({
    "nesingwary": "File:Hemet Nesingwary.jpg", "vrykul": "File:Vrykul Enforcer HS.jpg", "annhylde": "File:Annhylde HS.jpg",
    "bolvar": "File:Bolvar Fordragon at Wrath Gate.jpg", "putress": "File:Putress Raneman.jpg", "muradin": "File:MuradinWow.jpg",
    "abbendis": "File:Abbendis.jpg", "yogg": "File:Yogg-Saron HS.jpg", "rey_exanime": "File:Lich King Glenn Rane.jpg",
    "drakuru": "File:Overlord Drakuru.jpg", "freya": "File:Freya, Keeper of Nature HS.jpg", "oraculo": "File:Oracle Soo-rahm.jpg",
    "corazon_frenetico": "File:Frenzyheartguards.jpg", "hodir": "File:Hodir, Father of Giants Signature HS.jpg",
    "ppt": "File:Time-Lost Proto-Drake.jpg", "dalaran": "File:Dalaran City.jpg", "martillo_orgrim": "File:Orgrim's Hammer.jpg",
    "rompecielos": "File:The Skybreaker.jpg", "tirion": "File:Tirion Fordring TCG.jpg", "uther": "File:Uther HoW.jpg",
    "jaina": "File:Jaina Proudmoore TCG.jpg", "caballero_negro": "File:The Black Knight.jpg", "nexo": "File:The Nexus Art.jpg",
    "crater_mamtoth": "File:Mam'toth Crater.jpg", "ursoc": "File:Ursoc TCG.jpg",
})


def _json(q):
    return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(q), headers=UA), timeout=40))


def url_de(titulo):
    if titulo.startswith("File:"):
        for p in _json(dict(action="query", titles=titulo, prop="imageinfo", iiprop="url", format="json"))["query"]["pages"].values():
            if "imageinfo" in p:
                return p["imageinfo"][0]["url"]
        return None
    for p in _json(dict(action="query", titles=titulo, prop="pageimages", piprop="original", redirects=1,
                        format="json"))["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]
    pref = titulo.replace(" ", "_")
    for im in _json(dict(action="query", list="allimages", aiprefix=pref, ailimit=5, format="json"))["query"]["allimages"]:
        return im["url"]
    return None


def guardar(url, ruta):
    datos = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    im = Image.open(io.BytesIO(datos)).convert("RGBA")
    e = 700 / max(im.size)
    if e < 1:
        im = im.resize((int(im.width * e), int(im.height * e)), Image.LANCZOS)
    im.save(ruta)
    return im.size


def main(slugs):
    os.makedirs(PEG, exist_ok=True)
    fuentes = []
    for slug in slugs or TITULOS:
        ruta = os.path.join(PEG, slug + ".png")
        if os.path.exists(ruta) and slugs == []:
            continue
        try:
            url = url_de(TITULOS[slug])
            if not url:
                print("SIN IMAGEN", slug, TITULOS[slug])
                continue
            print("ok", slug, guardar(url, ruta), url.split("/revision")[0].rsplit("/", 1)[-1])
            fuentes.append(f"{slug}\t{url}")
        except Exception as e:                       # noqa: BLE001
            print("ERROR", slug, e)
    with open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8") as f:
        f.write("\n".join(fuentes) + ("\n" if fuentes else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
