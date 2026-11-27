# -*- coding: utf-8 -*-
"""Clips reales (yt-dlp, 1080p máx.). Uso: python _clips.py   ·  CREDITO = rótulo «VIDEO: …» de cada clip."""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
CL = {
    "esa_intro": ("lGgcxqjEqCA", "*00:00-02:30"),
    "esa_hoy": ("lGgcxqjEqCA", "*07:25-11:30"),
    "esa_puro": ("lGgcxqjEqCA", "*12:40-13:40"),
    "esa_10m": ("lGgcxqjEqCA", "*15:30-16:20"),
    "esa_tumbos": ("lGgcxqjEqCA", "*16:20-17:50"),
    "esa_rocas": ("lGgcxqjEqCA", "*18:40-19:50"),
    "esa_estafeta": ("lGgcxqjEqCA", "*22:50-23:30"),
    "esa_tiri": ("lGgcxqjEqCA", "*25:50-26:50"),
    "hera_llegada": ("yPUISYM0kag", None),
    "hera_norte": ("Cbn0CIfQFrs", None),
    "hera_sur": ("GEF7skMzug4", None),
    "hera_trailer": ("lbWmTQxTdqs", None),
    "draco": ("N-OvnVdZP_8", None),
    "apl_festejo": ("ga-h1i0W7kU", None),
    "apl_sala": ("OLlGHIm-KIE", "*02:20-04:40"),
    "nasa_sala": ("4RA8Tfa6Sck", "*1:09:50-1:12:30"),
    "dart_lanz": ("XKRf6-NcMqI", "*22:30-24:30"),
    "dart_despl": ("XKRf6-NcMqI", "*1:17:45-1:19:30"),
    "hera_lanz": ("ljPZKwAN1IY", None),
    "hera_marte": ("V6swIjI-7RI", None),
    "hubble_aft": ("QRaI2jHeUYw", None),
    "hubble_x3": ("X-Ncnq-WCL8", None),
    "webb": ("jHMd_aZyNDI", None),
    "licia": ("tV-f3hONRwM", None),
    "licia_equipo": ("5rTPZFx21HU", None),
    "chel_pais": ("AKPWSBCmlcA", None),
    "chel_dash": ("EhNL-YJFxOM", None),
}
_C = {"esa": "ESA", "hera": "ESA", "draco": "NASA / JOHNS HOPKINS APL", "apl": "NASA / JOHNS HOPKINS APL",
      "nasa": "NASA", "dart": "SPACEX", "hubble": "NASA / ESA / HUBBLE", "webb": "ESA/WEBB · CC BY", "licia": "ASI / ARGOTEC",
      "chel": "ASTEROID DAY / EL PAÍS"}
CREDITO = {k: "VIDEO: " + next(v for p, v in _C.items() if k.startswith(p)) for k in CL}
CREDITO["licia_equipo"] = "VIDEO: ARGOTEC"
CREDITO["chel_pais"] = "VIDEO: EL PAÍS"
CREDITO["chel_dash"] = "VIDEO: ASTEROID DAY"
CREDITO["hubble_x3"] = "VIDEO: ESA/HUBBLE · CC BY"
CREDITO["hubble_aft"] = "VIDEO: NASA GODDARD / HUBBLE"
CREDITO["hera_lanz"] = "VIDEO: ESA / SPACEX"

if __name__ == "__main__":
    for nom, (vid, sec) in CL.items():
        dest = os.path.join(AQUI, "clips", nom + ".mp4")
        if os.path.exists(dest):
            continue
        cmd = ["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]",
               "--merge-output-format", "mp4", "-o", dest, f"https://www.youtube.com/watch?v={vid}"]
        if sec:
            cmd[1:1] = ["--download-sections", sec, "--force-keyframes-at-cuts"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(nom, "OK" if os.path.exists(dest) else "FALLÓ " + (r.stderr or "")[-200:], flush=True)
