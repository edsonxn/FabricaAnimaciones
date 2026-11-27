# -*- coding: utf-8 -*-
"""Baja a audio/ost/ la OST OFICIAL (canales «- Topic») para «Las 20 cosas de Skyrim que PIERDES para siempre» (26-nov-2026): pistas de
Skyrim (Jeremy Soule) que Tamriel NO ha usado aún (comprobado contra audio/ost de todos los tes_*).
Busca por nombre (ytsearch5) y se queda con el primer resultado de un canal «- Topic».   python _bajar_ost.py
"""
import json
import os
import subprocess

PISTAS = {   # 26-nov tes_pierdes_siempre: pistas de Skyrim que NO usó tes_armaduras_poderosas (salió el 25-nov); ~17 min ≈ 16 secciones
    'watch_the_skies': 'Jeremy Soule Watch the Skies Skyrim',
    'masser': 'Jeremy Soule Masser Skyrim',
    'secunda': 'Jeremy Soule Secunda Skyrim',
    'awake': 'Jeremy Soule Awake Skyrim',
    'frostfall': 'Jeremy Soule Frostfall Skyrim',
    'a_winters_tale': "Jeremy Soule A Winter's Tale Skyrim",
    'tundra': 'Jeremy Soule Tundra Skyrim',
    'aurora': 'Jeremy Soule Aurora Skyrim',
    'streets_of_whiterun': 'Jeremy Soule Streets of Whiterun Skyrim',
    'seven_thousand_steps': 'Jeremy Soule Seven Thousand Steps Skyrim',
    'towers_and_shadows': 'Jeremy Soule Towers and Shadows Skyrim',
    'night_without_stars': 'Jeremy Soule Night Without Stars Skyrim',
    'the_city_gates': 'Jeremy Soule The City Gates Skyrim',
    'before_the_storm': 'Jeremy Soule Before the Storm Skyrim',
    'darkened_depths': 'Jeremy Soule Darkened Depths Skyrim',
    'death_in_the_darkness': 'Jeremy Soule Death in the Darkness Skyrim',
    'skyrims_dark_secret': "Jeremy Soule Skyrim's Dark Secret Skyrim",
    'beneath_the_ice': 'Jeremy Soule Beneath the Ice Skyrim',
    'standing_stones': 'Jeremy Soule Standing Stones Skyrim',
    'unbroken_road': 'Jeremy Soule Unbroken Road Skyrim',
    'distant_horizons': 'Jeremy Soule Distant Horizons Skyrim',
    'the_white_river': 'Jeremy Soule The White River Skyrim',
}
OUT = os.path.join("audio", "ost")
os.makedirs(OUT, exist_ok=True)
ids = {}
for slug, q in PISTAS.items():
    dest = os.path.join(OUT, slug + ".wav")
    r = subprocess.run(["python", "-m", "yt_dlp", "--flat-playlist", "-J", f"ytsearch6:{q}"], capture_output=True, text=True,
                       encoding="utf-8")
    try:
        ents = json.loads(r.stdout).get("entries", [])
    except ValueError:
        ents = []
    ent = next((e for e in ents if "topic" in (e.get("channel") or e.get("uploader") or "").lower()), None)
    if not ent:
        print("x (sin Topic)", slug)
        continue
    ids[slug] = dict(id=ent["id"], titulo=ent.get("title"), canal=ent.get("channel"))
    if not os.path.exists(dest):
        subprocess.run(["python", "-m", "yt_dlp", "-q", "-x", "--audio-format", "wav", "-o", os.path.join(OUT, slug + ".%(ext)s"),
                        "https://youtu.be/" + ent["id"]], capture_output=True)
    print("ok" if os.path.exists(dest) else "x", slug, ent["id"], ent.get("title"), "|", ent.get("channel"))
json.dump(ids, open(os.path.join(OUT, "_ids.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
