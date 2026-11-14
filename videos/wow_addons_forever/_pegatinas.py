# -*- coding: utf-8 -*-
"""Pegatinas de «Los 20 ADD-ONS de WoW Forever»: logos de cada add-on (CurseForge, de su propia página) + capturas oficiales
de su página (pantallas/) + íconos del juego (zamimg). URLs sacadas de videos/_investigacion_wow_addons_forever.md (7-nov-2026).
python _pegatinas.py → pegatinas/<slug>.png + pantallas/<slug>.jpg + previews/_hoja_peg.jpg (MIRARLA: cada imagen con su add-on)"""
import io
import os
import urllib.request

from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
os.makedirs(PEG, exist_ok=True)
os.makedirs(PAN, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}
F = "https://media.forgecdn.net/"

LOGOS = {  # slug: logo del add-on (thumbnail de CurseForge; se pide a 256 px y si falla a 64)
    "a_sparkles": "avatars/thumbnails/2098/80/64/64/639269174187288257.png",
    "a_books": "avatars/thumbnails/2067/965/64/64/639258707603401870.png",
    "a_camper": "avatars/thumbnails/2081/767/64/64/639263779352732857.jfif",
    "a_favorcraft": "avatars/thumbnails/2121/845/64/64/639276965217913355.png",
    "a_dialogkey": "avatars/thumbnails/1075/827/64/64/638613212992224809.jpg",
    "a_gatherlite": "avatars/thumbnails/1666/564/64/64/639060838045236664.png",
    "a_threat": "avatars/thumbnails/2060/233/64/64/639255291851063182.png",
    "a_wayfarer": "avatars/thumbnails/2091/693/64/64/639267147554128284.png",
    "a_immersion": "avatars/thumbnails/2179/151/64/64/639295550007431063.png",
    "a_lore": "avatars/thumbnails/2075/847/64/64/639261538663945017.png",
    "a_dialogueui": "avatars/thumbnails/966/26/64/64/638465114365047028.png",
    "a_spoken": "avatars/thumbnails/2123/272/64/64/639277523184843230.png",
    "a_spoken_es": "avatars/thumbnails/2123/345/64/64/639277526546951813.png",
    "a_training": "avatars/thumbnails/2111/909/64/64/639273738232522114.png",
    "a_dfl_journal": "avatars/thumbnails/2066/520/64/64/639258039685677327.png",
    "a_baganator": "avatars/thumbnails/956/327/64/64/638449029664561508.png",
    "a_openmap": "avatars/thumbnails/2166/401/64/64/639291472015127682.png",
    "a_auctionator": "avatars/thumbnails/1403/232/64/64/638909541952729618.png",
    "a_oneforall": "avatars/thumbnails/2151/847/64/64/639286533629970446.png",
    "a_leatrix": "avatars/thumbnails/483/32/64/64/637782408501667202.png",
    "a_questie": "avatars/thumbnails/351/162/64/64/637505206198965674.png",
}
CAPTURAS = {  # slug: captura oficial de la página del add-on (para pant()/pegatina grande)
    "s_sparkles": "attachments/2019/644/01-overview-jpg.jpg", "s_books": "attachments/2027/239/1-png.png",
    "s_camper": "attachments/1985/764/maphc-png.PNG", "s_favorcraft": "attachments/2060/597/favorcraftscreenshot-png.png",
    "s_favorcraft2": "attachments/2060/591/favorcraft_curseforge_introduction-jpg.jpg",
    "s_wayfarer": "attachments/2058/391/dd12d-d14d34do-ndondd12d_20261015_123619-png.png",
    "s_immersion": "attachments/1969/512/immersion-1-combat-jpg.jpg", "s_dialogueui": "attachments/829/429/wowscrnshot_032124_205549.jpg",
    "s_training": "attachments/2145/745/class-spells-png.png", "s_baganator": "attachments/1053/565/header-2024-12-30-categories.webp",
    "s_openmap": "attachments/2038/249/wowscrnshot_101126_015048-jpg.jpg", "s_auctionator": "attachments/548/332/2022-12-screenshot-tooltip.png",
    "s_oneforall": "attachments/2128/325/01_armory_gear_planner-jpg.jpg", "s_leatrix": "attachments/2117/940/leatrix-plus-hero-png.png",
    "s_questie": "attachments/258/916/4abi5yu.png", "s_questie2": "attachments/268/732/waypoints.png",
}
EXTRA = {"s_gatherlite": "https://raw.githubusercontent.com/wuild/gatherlite/master/gatherlite-elwynn-forever.png"}
ICONOS = {  # íconos del juego para las fichas
    "i_libro": "inv_misc_book_09", "i_collar": "inv_jewelry_necklace_07", "i_anillo": "inv_jewelry_ring_03", "i_arco": "inv_weapon_bow_08",
    "i_escudo": "inv_shield_06", "i_fogata": "spell_fire_fire", "i_comida": "inv_misc_food_15", "i_descanso": "spell_nature_sleep",
    "i_tienda": "inv_misc_tent", "i_herbo": "trade_herbalism", "i_mineria": "trade_mining", "i_pesca": "trade_fishing",
    "i_caja": "inv_crate_01", "i_oro": "inv_misc_coin_01", "i_mapa": "inv_misc_map_01", "i_espada": "inv_sword_04",
    "i_escudo_tanque": "ability_warrior_defensivestance", "i_calavera": "inv_misc_bone_humanskull_01", "i_mago": "classicon_mage",
    "i_brujo": "classicon_warlock", "i_cazador": "classicon_hunter", "i_libro_hech": "inv_misc_book_11", "i_nota": "inv_misc_note_01",
    "i_brujula": "inv_misc_spyglass_02", "i_boca": "spell_holy_silence", "i_bolsa": "inv_misc_bag_10", "i_montura": "ability_mount_ridinghorse",
}


def baja(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def main():
    hechos = []
    for slug, ruta in LOGOS.items():
        img = None
        for tam in ("256/256", "64/64"):
            try:
                img = Image.open(io.BytesIO(baja(F + ruta.replace("64/64", tam, 1)))).convert("RGBA")
                break
            except Exception:
                continue
        if img is None:
            print("FALTA logo", slug)
            continue
        if img.width < 256:
            img = img.resize((256, 256), Image.LANCZOS)
        img.save(os.path.join(PEG, slug + ".png"))
        hechos.append((slug, img))
    for slug, ruta in list(CAPTURAS.items()) + list(EXTRA.items()):
        try:
            img = Image.open(io.BytesIO(baja(ruta if ruta.startswith("http") else F + ruta))).convert("RGB")
        except Exception as e:
            print("FALTA captura", slug, e)
            continue
        img.save(os.path.join(PAN, slug + ".jpg"), quality=92)
        hechos.append((slug, img.convert("RGBA")))
    for slug, ico in ICONOS.items():
        try:
            img = Image.open(io.BytesIO(baja(f"https://wow.zamimg.com/images/wow/icons/large/{ico}.jpg"))).convert("RGBA")
        except Exception as e:
            print("FALTA icono", slug, e)
            continue
        img.resize((256, 256), Image.LANCZOS).save(os.path.join(PEG, slug + ".png"))
        hechos.append((slug, img))
    # hoja de control (previews/_hoja_peg.jpg)
    col, cw, ch = 8, 240, 200
    filas = (len(hechos) + col - 1) // col
    hoja = Image.new("RGB", (col * cw, filas * ch), (25, 25, 30))
    d = ImageDraw.Draw(hoja)
    for n, (slug, img) in enumerate(hechos):
        t = img.copy()
        t.thumbnail((cw - 20, ch - 40))
        x, y = (n % col) * cw, (n // col) * ch
        hoja.paste(t, (x + 10, y + 8), t)
        d.text((x + 10, y + ch - 26), slug, fill=(255, 255, 160))
    os.makedirs(os.path.join(D, "previews"), exist_ok=True)
    hoja.save(os.path.join(D, "previews", "_hoja_peg.jpg"), quality=85)
    print(len(hechos), "imágenes; hoja previews/_hoja_peg.jpg")


if __name__ == "__main__":
    main()
