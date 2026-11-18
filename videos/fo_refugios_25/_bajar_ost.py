# -*- coding: utf-8 -*-
"""BANDA SONORA OFICIAL de varios Fallout para fo_refugios_25 (comprobada con yt-dlp el 17-nov-2026).
- FO3 / New Vegas / 76 / 4: canal oficial «Inon Zur» (YouTube Music), álbum del juego comprobado en los metadatos
  (`album` = «Fallout 3», «Fallout New Vegas», «Fallout 76[: Steel Dawn]», «Fallout 4[: Music from Far Harbor…]»).
  Ojo: «Behemoth», «Ashes and Sand», «The Ferals», «Fortress» son de FO3; «The Infiltrator», «Uninvited»,
  «Covert Action», «Dust & Danger» son de FO4; «Industrial De-Evolution» es de New Vegas; «Our Way of Life…» es de 76.
- FO1 (Mark Morgan) y Tactics (Inon Zur): NO hay canal oficial ni álbum en YouTube Music → ripeos del juego/CD
  original subidos por fans (TheStableDweller, Nukapedia: The Fallout Wiki, Dimitris Krommidas). Audio original,
  sin covers ni remixes, pero sin metadatos de álbum.
- FO4: los mismos 16 de fo_nunca_f4 (se copian de ahí si existen, con prefijo fo4_).
Todo instrumental (sin canciones de radio con letra).          python _bajar_ost.py"""
import json, os, shutil, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
OST = os.path.join(AQUI, "audio", "ost")
F4 = os.path.join(AQUI, "..", "fo_nunca_f4", "audio", "ost")
Z = "Inon Zur, Fallout"
# slug: (id, titulo, canal, album, artista, duracion_s, tipo)
P = {
    # Fallout 3
    "fo3_main_title":          ("zaCdY1mfctw", "Main Title", "Inon Zur", "Fallout 3", Z, 125, "tema/épica"),
    "fo3_what_remains":        ("YbDCjEsPF7M", "What Remains", "Inon Zur", "Fallout 3", Z, 212, "calma oscura"),
    "fo3_wandering_the_wastes": ("C-b0YyBJ4tU", "Wandering the Wastes", "Inon Zur", "Fallout 3", Z, 206, "exploración"),
    "fo3_forgotten":           ("jERnmZ898aI", "Forgotten", "Inon Zur", "Fallout 3", Z, 215, "inquietante"),
    "fo3_unwelcome_guest":     ("eoLKQ8IQn5c", "Unwelcome Guest", "Inon Zur", "Fallout 3", Z, 218, "tensión"),
    "fo3_the_ferals":          ("wfjCJfL27Is", "The Ferals", "Inon Zur", "Fallout 3", Z, 197, "tensión"),
    "fo3_metal_on_metal":      ("DG1uQYcZxRA", "Metal on Metal", "Inon Zur", "Fallout 3", Z, 208, "combate"),
    "fo3_behemoth":            ("qj1GeDtpiG0", "Behemoth", "Inon Zur", "Fallout 3", Z, 164, "combate"),
    # Fallout: New Vegas
    "fnv_main_title":          ("QTw6EONlwZU", "Main Title", "Inon Zur", "Fallout New Vegas", Z, 128, "tema/calma"),
    "fnv_monsters_of_the_mojave": ("e4tp6MJeYWg", "Monsters of the Mojave", "Inon Zur", "Fallout New Vegas", Z, 257, "exploración/tensión"),
    "fnv_rubble_of_the_forgotten": ("FcyWMA1C7aM", "Rubble of the Forgotten", "Inon Zur", "Fallout New Vegas", Z, 235, "inquietante"),
    "fnv_industrial_de_evolution": ("wH66lSczM0A", "Industrial De-Evolution", "Inon Zur", "Fallout New Vegas", Z, 242, "inquietante"),
    "fnv_hail_caesar":         ("BFMAwHZkC44", "Hail Caesar", "Inon Zur", "Fallout New Vegas", Z, 262, "combate/marcial"),
    # Fallout 76
    "fo76_main_theme":         ("CarjSEcId_Q", "Main Theme", "Inon Zur", "Fallout 76", Z, 160, "tema/épica"),
    "fo76_landscape_lament":   ("F0mMhnUwVwA", "Landscape Lament", "Inon Zur", "Fallout 76", Z, 258, "calma"),
    "fo76_the_grafton_damned": ("cxCaVd7v8Io", "The Grafton Damned", "Inon Zur", "Fallout 76", Z, 275, "tensión"),
    "fo76_something_lurking":  ("c8kU91HBXMc", "Something Lurking", "Inon Zur", "Fallout 76: Steel Dawn", Z, 132, "tensión"),
    "fo76_scorched_earth":     ("mIslglIcxD8", "Scorched Earth", "Inon Zur", "Fallout 76", Z, 134, "combate"),
    # Fallout 1 (Mark Morgan) — ripeos del juego, sin canal oficial
    "fo1_vault_of_the_future": ("Uf7l_em3nrs", "Fallout 1 Soundtrack - Vault of the Future (Vault 13)", "TheStableDweller", None, "Mark Morgan", 244, "calma oscura (refugio)"),
    "fo1_city_of_the_dead":    ("XZctTNwrjHA", "Fallout 1 Soundtrack - City of the Dead (Necropolis)", "TheStableDweller", None, "Mark Morgan", 207, "inquietante"),
    "fo1_vats_of_goo":         ("dn3UDyLf9-A", "Fallout 1 Soundtrack - Vats of Goo (Mariposa Military Base and Fallout intro)", "TheStableDweller", None, "Mark Morgan", 201, "tensión"),
    "fo1_a_traders_life":      ("WIKthieb1Q8", "Fallout 1 Soundtrack - A Trader's Life.", "Nukapedia: The Fallout Wiki", None, "Mark Morgan", 243, "calma"),
    # Fallout Tactics (Inon Zur) — ripeo del soundtrack promocional, sin canal oficial
    "fot_haunted_desolation":  ("kGrAPXD-ecg", "Inon Zur-Fallout:Tactics--Track 10--Haunted Desolation", "Dimitris Krommidas", None, "Inon Zur", 232, "inquietante"),
    "fot_urban_landscapes":    ("396_b_WcXIQ", "Inon Zur-Fallout:Tactics--Track 12--Urban Landscapes", "Dimitris Krommidas", None, "Inon Zur", 229, "tensión"),
    # Fallout 4 (los 16 de fo_nunca_f4)
    "fo4_main_theme":          ("6YmUufemZSM", "Fallout 4 Main Theme", "Inon Zur", "Fallout 4", Z, 182, "tema/épica"),
    "fo4_glowing_sea_1":       ("XryN39S0zAA", "Wandering - The Glowing Sea, Pt. 1", "Inon Zur", "Fallout 4", Z, 208, "inquietante"),
    "fo4_glowing_sea_2":       ("77gpBnXND7c", "Wandering - The Glowing Sea, Pt. 2", "Inon Zur", "Fallout 4", Z, 125, "inquietante"),
    "fo4_welcome_far_harbor":  ("9VxGiDjBOLM", "Welcome to Far Harbor", "Inon Zur", "Fallout 4: Music from Far Harbor & Nuka World", Z, 66, "calma"),
    "fo4_lost_memories":       ("0NzzOkfa0kQ", "Lost Memories", "Inon Zur", "Fallout 4: Music from Far Harbor & Nuka World", Z, 248, "calma melancólica"),
    "fo4_the_commonwealth":    ("pbslbSOk_WE", "The Commonwealth", "Inon Zur", "Fallout 4", Z, 251, "exploración"),
    "fo4_science_secrecy":     ("atnlfmD8rVE", "Science & Secrecy", "Inon Zur", "Fallout 4", Z, 238, "tensión"),
    "fo4_honor_steel":         ("zrGbbRFbanM", "Honor & Steel", "Inon Zur", "Fallout 4", Z, 256, "épica/marcial"),
    "fo4_imagine_utopia":      ("Z9ZcBefzBDU", "Imagine Utopia", "Inon Zur", "Fallout 4", Z, 173, "calma"),
    "fo4_lone_wandering":      ("3w4nHNhX0UE", "Lone Wandering", "Inon Zur", "Fallout 4", Z, 264, "calma"),
    "fo4_rebuild_renew":       ("ZpufeaQuPEo", "Rebuild, Renew", "Inon Zur", "Fallout 4", Z, 371, "calma"),
    "fo4_combat_ready":        ("le3suDzRpjg", "Combat Ready", "Inon Zur", "Fallout 4", Z, 122, "combate"),
    "fo4_dominant_species":    ("Oe-Az46cBcE", "Dominant Species", "Inon Zur", "Fallout 4", Z, 122, "combate"),
    "fo4_enough_is_enough":    ("a7zz7K-q89o", "Enough Is Enough", "Inon Zur", "Fallout 4", Z, 138, "combate"),
    "fo4_rise_and_prevail":    ("arwJMohPTd8", "Rise and Prevail", "Inon Zur", "Fallout 4", Z, 135, "combate"),
    "fo4_critical_chance":     ("TYPJpsBTNMc", "A Critical Chance", "Inon Zur", "Fallout 4", Z, 118, "combate"),
}

os.makedirs(OST, exist_ok=True)
fallos = []
for s, (i, *_r) in P.items():
    dst = os.path.join(OST, s + ".wav")
    if not os.path.exists(dst) and s.startswith("fo4_"):
        src = os.path.join(F4, s[4:] + ".wav")
        if os.path.exists(src):
            shutil.copy2(src, dst)
    if not os.path.exists(dst):
        subprocess.run(["python", "-m", "yt_dlp", "-q", "--no-warnings", "-x", "--audio-format", "wav",
                        "-o", os.path.join(OST, s + ".%(ext)s"), "https://youtu.be/" + i])
    ok = os.path.exists(dst)
    if not ok:
        fallos.append(s)
    print("ok" if ok else "x ", s)

json.dump({s: dict(id=i, titulo=t, canal=c, album=a, artista=ar, duracion=d, tipo=ti)
           for s, (i, t, c, a, ar, d, ti) in P.items()},
          open(os.path.join(OST, "_ids.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"{len(P) - len(fallos)}/{len(P)} pistas" + (f" · FALTAN: {fallos}" if fallos else ""))
