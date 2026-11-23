# Baja las pegatinas (imágenes reales de Fallout Wiki) a pegatinas/<slug>.png (RGBA, lado máx. 1000 px).
# URLs de _investigacion_A/B.md (fo_enemigos_ocultos, 23-nov) + las que faltaban, sacadas por la API de la wiki (pageimages / imageinfo).
# Copia de videos/fo_nunca_f4/_pegatinas.py. Las "page:" se piden por pageimages. TODO se mira en
# previews/pegatinas_check_N.jpg (regla de identidad) antes de usarlo.
# --rec  → además recorta sin fondo (rembg) los slugs de RECORTAR como <slug>_rec.png
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).parent
OUT = AQUI / "pegatinas"
OUT.mkdir(exist_ok=True)
W = "https://static.wikia.nocookie.net/fallout/images/"
# slug: (url | "page:<Página>", qué muestra, juego, refugio)
P = {
    # ---- 15 Quinteto de la Reina (FO3) ----
    "e15_guardian": (W + "0/0b/Nest_guardian.jpg", "guardián del hormiguero", "FO3", "15"),
    "e15_grupo": (W + "7/76/Guardian_group.jpg", "grupo de guardianes", "FO3", "15"),
    "e15_reina": (W + "1/12/Marigold_ant_queen.jpg", "reina de Marigold", "FO3", "15"),
    "e15_lesko": ("page:Weston Lesko", "doctor Lesko", "FO3", "15"),
    "e15_marigold": ("page:Marigold station", "estación Marigold", "FO3", "15"),
    # ---- 14 cazador legendario (FNV) ----
    "e14_cazador": (W + "b/b1/LegendaryCazador.png", "cazador legendario", "FNV", "14"),
    "e14_mina": (W + "4/4a/Silver_Peak_Mine_interior.jpeg", "interior de Silver Peak", "FNV", "14"),
    "e14_exterior": (W + "6/6a/Silver_peak_mine_exterior.jpg", "exterior de la mina", "FNV", "14"),
    "e14_cueva": (W + "b/b5/Silver_Peak_Mine_cave.jpg", "cueva de la mina", "FNV", "14"),
    # ---- 13 Red Death (FO4 FH) ----
    "e13_red": ("file:FO4 Red Death Mirelurk.jpg", "Red Death (ojos rojos)", "FO4 FH", "13"),
    "e13_isla": ("file:Red Death Island.png", "isla del Red Death", "FO4 FH", "13"),
    "e13_marcador": ("file:FO4FH Red Death island map marker.png", "marcador en el mapa", "FO4 FH", "13"),
    "e13_mision": ("file:FO4FH The Great Hunt 1.png", "captura de la misión (verificar)", "FO4 FH", "13"),
    # ---- 12 Ruzka (FO3 PL) ----
    "e12_ruzka": (W + "4/4e/Ruzka.jpg", "Ruzka en su guarida", "FO3 PL", "12"),
    "e12_guarida": (W + "5/5c/Ruzka%27s_Lair.jpg", "la guarida", "FO3 PL", "12"),
    "e12_poster": (W + "a/a5/RuzkaPoster_Target.jpg", "cartel del circo", "FO3 PL", "12"),
    # ---- 11 Stripe (FNV OWB) ----
    "e11_stripe": (W + "3/32/Stripe.jpg", "Stripe", "FNV OWB", "11"),
    "e11_higgs": (W + "0/0a/Higgs_Village.jpg", "Higgs Village", "FNV OWB", "11"),
    # ---- 10 reina Nukalurk (FO4 NW) ----
    "e10_reina": ("file:Fo4NW Nukalurk queen.png", "reina Nukalurk", "FO4 NW", "10"),
    "e10_noche": ("file:Fo4NW Nukalurk queen at night.png", "reina de noche, brillo azul", "FO4 NW", "10"),
    "e10_carga": ("file:FO4NW Nukalurk Loading Screen.png", "pantalla de carga", "FO4 NW", "10"),
    "e10_planta": ("file:NukaColaBottlingPlant-NukaWorld.png", "planta embotelladora", "FO4 NW", "10"),
    "e10_quantum": ("page:Nuka-Cola Quantum (Fallout 4)", "botella de Nuka-Cola Quantum", "FO4", "10"),
    # ---- 9 Madre Curie III (FO3 BS) ----
    "e9_necrofaga": (W + "7/70/Mother_Curie_III_Ghoul.jpg", "Madre Curie como necrófaga", "FO3 BS", "9"),
    "e9_humana": (W + "2/2e/Mother_Curie.jpg", "Madre Curie humana", "FO3", "9"),
    "e9_megaton": ("page:Megaton", "Megatón", "FO3", "9"),
    "e9_bomba": ("page:Megaton atomic bomb", "la bomba de Megatón", "FO3", "9"),
    # ---- 8 Gabe (FNV OWB) ----
    "e8_gabe": (W + "9/94/Gabe.jpg", "Gabe", "FNV OWB", "8"),
    "e8_ladra": (W + "6/65/Gabe_barking.jpg", "Gabe ladrando", "FNV OWB", "8"),
    "e8_guarida": (W + "2/28/X-8_testing_facility_gabes_lair.jpg", "guarida en el X-8", "FNV OWB", "8"),
    "e8_borous": ("page:Dr. Borous", "doctor Borous", "FNV OWB", "8"),
    # ---- 7 alienígena (FO4) ----
    "e7_alien": ("file:Fallout 4 Alien Closeup.jpg", "alienígena de cerca", "FO4", "7"),
    "e7_ovni": ("file:Fo4 crashed UFO.png", "OVNI estrellado", "FO4", "7"),
    "e7_cayendo": ("file:Fo4 Crashing UFO.png", "OVNI cayendo", "FO4", "7"),
    "e7_noche": ("file:FO4 UFOcrashnight.jpg", "choque de noche", "FO4", "7"),
    "e7_blaster": ("page:Alien blaster pistol", "pistola blaster alienígena", "FO4", "7"),
    # ---- 6 sanguinario legendario (FNV) ----
    "e6_sanguinario": (W + "0/01/FNV_DeathclawAlpha.png", "sanguinario legendario (verificar)", "FNV", "6"),
    "e6_cueva": (W + "d/d4/Fallout_New_Vegas_Dead_Wind_Cavern.jpg", "entrada Dead Wind", "FNV", "6"),
    "e6_interior": (W + "9/9f/Dead_Wind_Cavern_interior.jpg", "interior Dead Wind", "FNV", "6"),
    "e6_mercy": ("page:Mercy", "Mercy, arma única", "FNV", "6"),
    # ---- 5 mutascorpio albino (FO3 BS) ----
    "e5_albino": (W + "8/89/Albino_radscorpion.png", "mutascorpio albino", "FO3 BS", "5"),
    "e5_reguladores": ("page:Regulator HQ", "cuartel de los Reguladores", "FO3", "5"),
    "e5_behemoth": ("page:Super mutant behemoth (Fallout 3)", "supermutante behemoth FO3", "FO3", "5"),
    "e5_jingwei": ("page:General Jingwei", "general Jingwei", "FO3 OA", "5"),
    # ---- 4 camaleón y mítico (FO4) ----
    "e4_mitico": ("file:FO4 Mythic Deathclaw.jpg", "sanguinario mítico", "FO4", "4"),
    "e4_camaleon": ("file:FO4 Chameleon Deathclaw Line-up.jpg", "camaleones de colores", "FO4", "4"),
    "e4_cigarrillo": ("page:Cigarette (Fallout 4)", "cigarrillo", "FO4", "4"),
    # ---- 3 Rawr (FNV LR) ----
    "e3_rawr": (W + "4/46/Rawr.jpg", "Rawr", "FNV LR", "3"),
    "e3_azotea": (W + "d/dd/Boxwood_Hotel_roof.jpg", "azotea del hotel Boxwood", "FNV LR", "3"),
    "e3_bengala": ("page:Flare gun", "pistola de bengalas", "FNV", "3"),
    "e3_puno": ("page:Fist of Rawr", "Puño de Rawr", "FNV LR", "3"),
    # ---- 2 Hundebarcos (FO4 FH) ----
    "e2_hundebarcos": ("file:Shipbreaker.png", "Hundebarcos", "FO4 FH", "2"),
    "e2_reptador": ("file:FO4FH Enraged fog crawler.png", "reptador de la Niebla (apoyo)", "FO4 FH", "2"),
    "e2_longfellow": ("page:Old Longfellow", "Viejo Longfellow", "FO4 FH", "2"),
    "e2_arpon": ("page:Skipper's Last Stand", "arpón único", "FO4 FH", "2"),
    # ---- 1 tochomosca legendaria (FNV OWB) ----
    "e1_tochomosca": (W + "e/e6/Legendary_bloatfly.jpg", "tochomosca legendaria en la cueva", "FNV OWB", "1"),
    "e1_tamano": (W + "f/f4/Legendary_Bloatfly.png", "comparación de tamaño", "FNV OWB", "1"),
    "e1_interior": (W + "f/f9/Mysterious_cave_interior.jpg", "interior cueva misteriosa", "FNV OWB", "1"),
    "e1_entrada": (W + "6/60/Mysterious_cave.jpg", "entrada cueva misteriosa", "FNV OWB", "1"),
    "e1_psycho": ("page:Psycho (Fallout: New Vegas)", "Psycho", "FNV", "1"),
    "e1_buffout": ("page:Buffout (Fallout: New Vegas)", "Buffout", "FNV", "1"),
    # ---- genéricos ----
    "gen_pipboy3000": ("page:Pip-Boy 3000 Mark IV", "Pip-Boy FO4", "FO4", "-"),
    "gen_vaultboy": ("page:Vault Boy", "Vault Boy", "saga", "-"),
}
RECORTAR = ["e15_lesko", "e14_cazador", "e10_quantum", "e8_borous", "e7_blaster", "e6_mercy", "e5_albino", "e5_jingwei",
            "e4_cigarrillo", "e3_bengala", "e3_puno", "e2_longfellow", "e2_arpon", "e1_tamano", "e1_psycho", "e1_buffout",
            "gen_pipboy3000", "gen_vaultboy", "e9_humana", "e1_tochomosca"]
UA = {"User-Agent": "Mozilla/5.0"}


def url_de(v):
    if v.startswith("file:"):
        t = urllib.parse.quote("File:" + v[5:])
        q = f"https://fallout.fandom.com/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles={t}"
        d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
        for p in d["query"]["pages"].values():
            return p["imageinfo"][0]["url"]
    if not v.startswith("page:"):
        return v
    t = urllib.parse.quote(v[5:])
    q = f"https://fallout.fandom.com/api.php?action=query&prop=pageimages&piprop=original&redirects=1&format=json&titles={t}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
    for p in d["query"]["pages"].values():
        return p.get("original", {}).get("source")


def bajar():
    fuentes = {}
    fp = OUT / "_fuentes.txt"
    if fp.exists():
        for ln in fp.read_text(encoding="utf-8").splitlines():
            if " | " in ln:
                s, u = ln.split(" | ", 1)
                fuentes[s] = u
    for slug, (v, *_r) in P.items():
        dst = OUT / f"{slug}.png"
        if dst.exists() and "--todo" not in sys.argv:
            continue
        try:
            u = url_de(v)
            raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
            im.thumbnail((1000, 1000), Image.LANCZOS)
            im.save(dst)
            fuentes[slug] = u
            print("ok", slug, im.size)
        except Exception as e:
            print("FALLO", slug, e)
    fp.write_text("\n".join(f"{s} | {fuentes[s]}" for s in P if s in fuentes) + "\n", encoding="utf-8")


def recortar():
    from rembg import remove
    for slug in RECORTAR:
        src = OUT / f"{slug}.png"
        dst = OUT / f"{slug}_rec.png"
        if not src.exists() or (dst.exists() and "--todo" not in sys.argv):
            continue
        im = remove(Image.open(src).convert("RGBA"))
        bb = im.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
        if bb:
            im = im.crop(bb)
        im.save(dst)
        print("rec", slug, im.size)


def hoja():
    """previews/pegatinas_check_N.jpg: miniatura + slug + qué es + juego (20 por hoja). Los _rec sobre damero."""
    from PIL import ImageDraw, ImageFont
    try:
        f1 = ImageFont.truetype("arialbd.ttf", 17)
        f2 = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    items = []
    for slug, (v, que, juego, ref) in P.items():
        for suf in ("", "_rec"):
            fp = OUT / f"{slug}{suf}.png"
            if fp.exists():
                items.append((fp, slug + suf, que, f"{juego} · R{ref}"))
    C, F, TW, TH = 5, 4, 340, 230
    prev = AQUI / "previews"
    for n in range(0, len(items), C * F):
        S = Image.new("RGB", (C * TW, F * (TH + 50)), (40, 40, 40))
        d = ImageDraw.Draw(S)
        for i, (fp, slug, que, jr) in enumerate(items[n:n + C * F]):
            x, y = (i % C) * TW, (i // C) * (TH + 50)
            im = Image.open(fp).convert("RGBA")
            im.thumbnail((TW - 10, TH - 6))
            if slug.endswith("_rec"):
                bg = Image.new("RGB", im.size, (255, 0, 255))
                bg.paste(im, (0, 0), im)
                im = bg.convert("RGBA")
            S.paste(im, (x + (TW - im.width) // 2, y + 3), im)
            d.text((x + 4, y + TH + 2), slug, fill=(255, 230, 0), font=f1)
            d.text((x + 4, y + TH + 24), f"{que[:38]} | {jr}", fill=(220, 220, 220), font=f2)
        out = prev / f"pegatinas_check_{n // (C * F) + 1}.jpg"
        S.save(out, quality=88)
        print(out)


if __name__ == "__main__":
    if "--hoja" not in sys.argv or "--bajar" in sys.argv:
        bajar()
    if "--rec" in sys.argv:
        recortar()
    if "--hoja" in sys.argv:
        hoja()
