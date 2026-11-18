# Baja las pegatinas (imágenes reales de Fallout Wiki, FO4) a pegatinas/<slug>.png (RGBA). URLs de _investigacion_A/B.md;
# las marcadas "page:" se piden por pageimages a la página de FO4 y se MIRAN en la hoja (regla de identidad).
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
P = {
    "servoarmadura": W + "d/df/FO4_Power_Armor_Infobox.png/revision/latest/scale-to-width-down/800",
    "armazon": W + "1/15/FO4_Power_Armor_Frame.png/revision/latest/scale-to-width-down/615",
    "nucleo_fusion": W + "2/2f/Fo4_fusion_core.png/revision/latest/scale-to-width-down/800",
    "sanctuary": W + "a/a5/Fo4_Sanctuary_Hills_Overview.png/revision/latest/scale-to-width-down/800",
    "borde_mar": W + "2/20/Edgeoftheglowingsea.png/revision/latest/scale-to-width-down/800",
    "crater_atomo": W + "d/d1/Craterofatom.png/revision/latest/scale-to-width-down/800",
    "tormenta_rad": W + "8/86/FO4_RadiationStorm.png/revision/latest/scale-to-width-down/800",
    "radaway": W + "2/2b/Fallout4_RadAway.png/revision/latest/scale-to-width-down/800",
    "radx": W + "1/19/Fallout4_Rad-X.png/revision/latest",
    "hazmat": W + "1/1a/FO4-nate-hazmat-suit.jpg/revision/latest/scale-to-width-down/571",
    "suicida": W + "7/70/FO4_super_mutant_suicider.jpg/revision/latest/scale-to-width-down/800",
    "kremvh": W + "8/86/Kremvh%27s_Tooth.png/revision/latest/scale-to-width-down/800",
    "cabezon_fuerza": W + "3/3e/Fo4strengthbobblehead.png/revision/latest",
    "cabezones": W + "a/a3/FO4FiguresComplete.png/revision/latest/scale-to-width-down/800",
    "baul": W + "d/df/FO4_Steamer_trunk.png/revision/latest",
    "caja_fuerte": W + "7/7b/FO4_Safe.png/revision/latest",
    "mama_murphy": W + "6/64/Mama_Murphy.jpg/revision/latest/scale-to-width-down/800",
    "sillon_murphy": W + "b/b9/Mama_Murphy%27s_chair.png/revision/latest",
    "kent": W + "f/f5/Kent_Connoly.jpg/revision/latest/scale-to-width-down/800",
    "sinjin": W + "4/46/Sinjin.png/revision/latest/scale-to-width-down/800",
    "traje_mortaja": W + "e/e0/Fo4Silver_Shroud_Costume_male.png/revision/latest/scale-to-width-down/572",
    "hospital_milton": W + "c/cb/Miltongeneralhospital.png/revision/latest/scale-to-width-down/800",
    "austin": W + "d/d2/Austin_Engill.png/revision/latest/scale-to-width-down/800",
    "curie": W + "8/89/Curie.jpg/revision/latest/scale-to-width-down/800",
    "puerta_r81": W + "e/e7/Vault_81door.jpg/revision/latest/scale-to-width-down/800",
    "enfermedad_rata": W + "2/20/Molerat_disease_Pip-Boy.jpg/revision/latest/scale-to-width-down/800",
    "preston": W + "5/58/FO4_PrestonGarvey_Infobox.png/revision/latest/scale-to-width-down/556",
    "shank": W + "1/1a/FO4NW_Shank.png/revision/latest/scale-to-width-down/800",
    "jefes_banda": W + "0/01/Fallout-4-raiders_underbosses.png/revision/latest/scale-to-width-down/800",
    "lorenzo": W + "6/6d/Lorenzos_suit.jpg/revision/latest/scale-to-width-down/800",
    "jack_cabot": W + "7/7d/Jack_Cabot.png/revision/latest/scale-to-width-down/800",
    "wilhelmina": W + "d/d8/Wilhelmina_Cabot.png/revision/latest/scale-to-width-down/800",
    "emogene": W + "1/1b/Emogene_young.png/revision/latest/scale-to-width-down/800",
    "casa_cabot": W + "e/e1/Cabot_House.jpg/revision/latest/scale-to-width-down/800",
    "manicomio": W + "8/84/Parsons_state_ext.png/revision/latest/scale-to-width-down/800",
    "suero": W + "f/fd/Fo4_mysterious_serum.png/revision/latest",
    "artefacto_lorenzo": W + "c/c1/Lorenzos_artifact_gun.png/revision/latest",
    "far_harbor": W + "7/76/FarHarborTown-FarHarbor.jpg/revision/latest/scale-to-width-down/800",
    "parque_eolico": W + "d/d8/FO4-FarHarbor-WindFarmMaintenance-Entrance.jpeg/revision/latest/scale-to-width-down/800",
    "condensador": W + "1/1d/Fog_condensor.png/revision/latest/scale-to-width-down/647",
    "tektus": W + "8/87/Fo4Tektus.jpg/revision/latest/scale-to-width-down/800",
    "longfellow": W + "b/b4/FH_Old_Longfellow.jpg/revision/latest/scale-to-width-down/800",
    "nucleo_isla": W + "0/05/FO4-FarHarbor-Nucleus-GeneralView.jpeg/revision/latest/scale-to-width-down/800",
    "mass_fusion": W + "d/d7/Mass_Fusion.png/revision/latest/scale-to-width-down/800",
    "minibomba": "page:Mini nuke (Fallout 4)",
    "dima": "page:DiMA",
    "kellogg": "page:Conrad Kellogg",
    "skinny_malone": "page:Skinny Malone",
    "desdemona": "page:Desdemona",
    "estimulante": W + "e/e7/Fallout4_Stimpak.png/revision/latest",
    "dunwich": "page:Dunwich Borers",
    "medford": "page:Medford Memorial Hospital",
}
UA = {"User-Agent": "Mozilla/5.0"}


def url_de(v):
    if not v.startswith("page:"):
        return v
    t = urllib.parse.quote(v[5:])
    q = f"https://fallout.fandom.com/api.php?action=query&prop=pageimages&pithumbsize=800&format=json&titles={t}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
    for p in d["query"]["pages"].values():
        return p.get("thumbnail", {}).get("source")


fuentes = []
for slug, v in P.items():
    dst = OUT / f"{slug}.png"
    if dst.exists() and "--todo" not in sys.argv:
        continue
    try:
        u = url_de(v)
        raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
        Image.open(io.BytesIO(raw)).convert("RGBA").save(dst)
        fuentes.append(f"{slug}: {u}")
        print("ok", slug)
    except Exception as e:
        print("FALLO", slug, e)
with open(OUT / "_fuentes.txt", "a", encoding="utf-8") as f:
    f.write("\n".join(fuentes) + "\n")
