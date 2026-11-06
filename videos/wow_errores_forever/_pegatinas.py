# -*- coding: utf-8 -*-
"""Pegatinas de «Los 25 ERRORES de WoW Forever»: íconos reales del juego (zamimg, por nombre de ícono) e imágenes de
personajes/lugares (Wowpedia en Fandom). Copiado de wow_objetos_secretos_forever/_pegatinas.py (6-nov-2026).
python _pegatinas.py   → pegatinas/<slug>.png + pantallas/<slug>.jpg + previews/_hoja_peg.jpg (MIRARLA)"""
import io
import json
import os
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
os.makedirs(PEG, exist_ok=True)
os.makedirs(PAN, exist_ok=True)
os.makedirs(os.path.join(D, "previews"), exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}

ICONOS = {  # slug: nombre del ícono del juego
    "i_abisario": "spell_shadow_summonvoidwalker", "i_manafago": "spell_shadow_summonfelhunter", "i_ritual": "spell_shadow_twilight",
    "i_fogata": "spell_fire_fire", "i_bolsa": "inv_misc_bag_10", "i_bolsa_comp": "inv_misc_bag_07_green", "i_libro": "inv_misc_book_09",
    "i_caballo": "ability_mount_ridinghorse", "i_corcel_vil": "spell_nature_swiftness", "i_destrero": "ability_mount_charger",
    "i_oro": "inv_misc_coin_01", "i_caja": "inv_crate_01", "i_comida": "inv_misc_food_15", "i_etiqueta": "inv_misc_note_01",
    "i_furia": "spell_holy_sealoffury", "i_mineria": "trade_mining", "i_herbo": "trade_herbalism", "i_desuello": "inv_misc_pelt_wolf_01",
    "i_alquimia": "trade_alchemy", "i_herreria": "trade_blacksmithing", "i_encanta": "trade_engraving", "i_ingenieria": "trade_engineering",
    "i_peleteria": "inv_misc_armorkit_17", "i_sastreria": "trade_tailoring", "i_pesca": "trade_fishing", "i_kodo": "ability_mount_kodo_01",
    "i_libro_hech": "inv_misc_book_11", "i_tienda": "inv_misc_tent", "i_estandarte": "inv_banner_01", "i_vela": "inv_misc_candle_02",
    "i_collar": "inv_jewelry_necklace_07", "i_anillo": "inv_jewelry_ring_03", "i_baston": "inv_staff_08", "i_piedra": "inv_stone_04",
    "i_reloj": "inv_misc_pocketwatch_01", "i_descanso": "spell_nature_sleep", "i_mapa": "inv_misc_map_01", "i_mago": "classicon_mage",
    "i_brujo": "classicon_warlock", "i_sacerdote": "classicon_priest", "i_paladin": "classicon_paladin", "i_picaro": "classicon_rogue",
    "i_cazador": "classicon_hunter", "i_guerrero": "classicon_warrior", "i_druida": "classicon_druid", "i_chaman": "classicon_shaman",
    "i_alianza": "inv_bannerpvp_02", "i_horda": "inv_bannerpvp_01", "i_hermandad": "inv_shirt_guildtabard_01", "i_espada": "inv_sword_04",
}
WIKI = {  # slug: título de Wowpedia
    "voidwalker": "Voidwalker", "felhunter": "Felhunter", "warlock": "Warlock", "meeting_stone": "Meeting Stone",
    "ritual": "Ritual of Summoning", "zeppelin": "Zeppelin", "auberdine": "Auberdine", "menethil": "Menethil Harbor",
    "wetlands": "Wetlands", "darkshore": "Darkshore", "tanaris": "Tanaris", "blackfathom": "Blackfathom Deeps",
    "lordaeron": "Ruins of Lordaeron", "garon": "Garon Wendell", "owen": "Owen Thadd", "strahad": "Strahad Farsan",
    "ratchet": "Ratchet", "kodo": "Kodo", "lich_king": "Lich King", "aggrend": "Josh Greenfield", "westfall": "Westfall",
    "barrens": "The Barrens", "loch_modan": "Loch Modan", "hillsbrad": "Hillsbrad Foothills", "redridge": "Redridge Mountains",
    "crossroads": "The Crossroads", "stormwind": "Stormwind City", "undercity": "Undercity", "gnomeregan": "Gnomeregan",
    "trol": "Troll", "valle_pruebas": "Valley of Trials", "elwynn": "Elwynn Forest", "jabali": "Boar", "crocolisco": "Crocolisk",
    "tiburon": "Shark", "nerzhul": "Ner'zhul", "ironforge": "Ironforge", "catedral": "Cathedral of Light", "orgrimmar": "Orgrimmar",
    "thunder_bluff": "Thunder Bluff", "darnassus": "Darnassus", "skyborne": "Skyborne", "deadmines": "Deadmines",
    "wailing": "Wailing Caverns", "onyxia": "Onyxia", "mago": "Mage", "sacerdote": "Priest", "paladin": "Paladin", "picaro": "Rogue",
    "kalimdor": "Kalimdor", "reinos_este": "Eastern Kingdoms", "costasur": "Southshore",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return r.read()


for slug, ico in ICONOS.items():
    if os.path.exists(os.path.join(PEG, slug + ".png")):
        continue
    try:
        im = Image.open(io.BytesIO(get(f"https://wow.zamimg.com/images/wow/icons/large/{ico}.jpg"))).convert("RGBA")
        im.resize((320, 320), Image.LANCZOS).save(os.path.join(PEG, slug + ".png"))
        print(slug, "ok", flush=True)
    except Exception as e:
        print("FALLO", slug, ico, e, flush=True)


def wiki(titulos):
    q = urllib.parse.urlencode(dict(action="query", prop="pageimages", piprop="original", redirects=1, format="json",
                                    titles="|".join(titulos)))
    return json.loads(get("https://wowpedia.fandom.com/api.php?" + q))["query"]


t = [(s, v) for s, v in WIKI.items() if not os.path.exists(os.path.join(PEG, s + ".png"))]
for k in range(0, len(t), 40):
    q = wiki([v for _, v in t[k:k + 40]])
    nombres = {x["from"]: x["to"] for x in q.get("redirects", [])}
    norm = {x["from"]: x["to"] for x in q.get("normalized", [])}
    pags = {p["title"]: p for p in q["pages"].values()}
    for slug, titulo in t[k:k + 40]:
        n = norm.get(titulo, titulo)
        n = nombres.get(n, n)
        url = pags.get(n, {}).get("original", {}).get("source")
        if not url:
            print("SIN IMAGEN", slug, titulo, flush=True)
            continue
        try:
            im = Image.open(io.BytesIO(get(url))).convert("RGBA")
            print(slug, im.size, flush=True)
            grande = im.copy()
            grande.thumbnail((1920, 1920))
            if max(im.size) >= 1000:
                grande.convert("RGB").save(os.path.join(PAN, slug + ".jpg"), quality=92)
            im.thumbnail((700, 700))
            im.save(os.path.join(PEG, slug + ".png"))
        except Exception as e:
            print("FALLO", slug, e, flush=True)

fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png") and not f.startswith("com_"))
col = 12
hoja = Image.new("RGB", (col * 160, (len(fs) // col + 1) * 180), (40, 40, 40))
d = ImageDraw.Draw(hoja)
for n, f in enumerate(fs):
    im = Image.open(os.path.join(PEG, f)).convert("RGBA")
    im.thumbnail((150, 150))
    x, y = (n % col) * 160 + 5, (n // col) * 180 + 5
    hoja.paste(im, (x, y), im)
    d.text((x, y + 155), f[:-4][:22], fill="white")
hoja.save(os.path.join(D, "previews", "_hoja_peg.jpg"), quality=85)
print("hoja lista:", len(fs))
