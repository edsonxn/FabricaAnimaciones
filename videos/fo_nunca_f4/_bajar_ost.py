# -*- coding: utf-8 -*-
"""OST OFICIAL de Fallout 4 (Inon Zur, canal oficial; álbum «Fallout 4» / «Music from Far Harbor & Nuka World» comprobado en los
metadatos con yt-dlp el 17-nov-2026; «Behemoth» es de Fallout 3 → fuera).   python _bajar_ost.py"""
import json, os, subprocess
P = {"main_theme": "6YmUufemZSM", "glowing_sea_1": "XryN39S0zAA", "glowing_sea_2": "77gpBnXND7c", "welcome_far_harbor": "9VxGiDjBOLM",
     "lost_memories": "0NzzOkfa0kQ", "the_commonwealth": "pbslbSOk_WE", "science_secrecy": "atnlfmD8rVE", "honor_steel": "zrGbbRFbanM",
     "imagine_utopia": "Z9ZcBefzBDU", "lone_wandering": "3w4nHNhX0UE", "rebuild_renew": "ZpufeaQuPEo", "combat_ready": "le3suDzRpjg",
     "dominant_species": "Oe-Az46cBcE", "enough_is_enough": "a7zz7K-q89o", "rise_and_prevail": "arwJMohPTd8", "critical_chance": "TYPJpsBTNMc"}
os.makedirs("audio/ost", exist_ok=True)
for s, i in P.items():
    if not os.path.exists(f"audio/ost/{s}.wav"):
        subprocess.run(["python", "-m", "yt_dlp", "-q", "-x", "--audio-format", "wav", "-o", f"audio/ost/{s}.%(ext)s", "https://youtu.be/" + i])
    print("ok" if os.path.exists(f"audio/ost/{s}.wav") else "x", s)
json.dump({s: dict(id=i, canal="Inon Zur") for s, i in P.items()}, open("audio/ost/_ids.json", "w"), indent=1)
