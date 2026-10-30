# -*- coding: utf-8 -*-
"""Base de bt_mundos_ranking (30-oct-2026): recorta los mapas de los 8 mundos de la Guía oficial de Nintendo (2000) y baja la OST.
    python preparar_base.py mapas      recorta mapas/g_<mundo>.jpg -> mapas/<mundo>.jpg
    python preparar_base.py ost        audio/ost/<nombre>.wav (ripeo del juego en «Video-Game OST HQ»; ids de bt_jiggies_crueles)
"""
import os
import subprocess
import sys
import time

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(AQUI, "mapas")
# (x0, y0, x1, y1) sobre la página a 300 dpi: solo el mapa, sin la cabecera ni el texto de la guía
CORTES = {"mt": (54, 1428, 2480, 2990), "ggm": (54, 943, 2480, 2965), "ww": (54, 808, 2480, 3070), "jrl": (54, 970, 2480, 3100),
          "tdl": (0, 1590, 2430, 3020), "gi": (54, 916, 2430, 3070), "hfp": (0, 916, 2480, 3070), "ccl": (108, 970, 2480, 3030)}
OST = {"tema": "BMANBzwNzQc", "jiggywiggy": "TWNZhhXDaYk", "isla": "L1RjVwP-_g8", "spiral": "SZU-zfl8m9U", "jinjo": "A-WmrMEcdgo",
       "overture": "91wxWjunKyk", "plan": "I0MVRZQtNaU", "problema": "sMAkn3GVfYE", "seleccion": "jp0YEyMtlBw", "funngames": "ydOxMYEaW-g",
       "mt": "v7G89M5ntGA", "ggm": "_jdz9ojcRaA", "ggm_cuevas": "1pYuUmbO-UI", "ordnance": "PyNTR9qiqY0", "ww": "rcDMwOBF3-o",
       "jrl": "T5fU7m-jR_s", "atlantis": "u5IxTRJB7_k", "tdl": "sbeoTUSMdLE", "gi": "DZIJBIz8dWU", "gi_dentro": "lxLOoXrvR94",
       "gi_elevador": "wD8e-ywYQKE", "hfp_lava": "D9BV4k2Hi-4", "hfp_hielo": "QlGGZhyKEzM", "ccl": "N_JBA5JVulQ", "mary": "wh5VCKslyrQ",
       "vs_terry": "VTW0gQ6ulmU", "vs_chilli": "vRxgiVRCOgQ", "vs_klungo": "YgU_pmAfSLc", "vs_mingy": "bdOkIgqgxJI", "vs_patch": "OjrFhMfEh7k",
       "vs_targitzan": "j1IoQ40U9kc", "creditos": "hqJU1FqkZFc", "fin": "uw6-2qGHUQQ", "fallo": "6Oe8McjC2SY"}


def mapas():
    for k, caja in CORTES.items():
        im = Image.open(os.path.join(MAP, f"g_{k}.jpg")).convert("RGB").crop(caja)
        im.save(os.path.join(MAP, k + ".jpg"), quality=92)
        print(k, im.size)
    Image.open(os.path.join(MAP, "c_isle.png")).convert("RGB").save(os.path.join(MAP, "isla.jpg"), quality=93)
    open(os.path.join(MAP, "_fuentes.txt"), "w", encoding="utf-8").write(
        "Mapas de mundos: Banjo-Tooie, Official Nintendo Player's Guide (2000), escaneo 600 DPI de archive.org\n"
        "https://archive.org/details/banjo-tooie-official-nintendo-players-guide-2000-kitsunebi (págs. 26, 36, 46, 56, 66, 76, 90, 100)\n"
        "Isla: banjokazooie.fandom.com File:IsleO'Hags.png\n")


def ost():
    d = os.path.join(AQUI, "audio", "ost")
    os.makedirs(d, exist_ok=True)
    for n, i in OST.items():
        s = os.path.join(d, n + ".wav")
        if os.path.exists(s):
            continue
        r = subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "-x", "--audio-format", "wav", "-o",
                            os.path.join(d, n + ".%(ext)s"), "https://youtu.be/" + i], capture_output=True, text=True)
        print(n, "ok" if os.path.exists(s) else "FALLO " + r.stderr[-200:], flush=True)
        time.sleep(4)


if __name__ == "__main__":
    {"mapas": mapas, "ost": ost}[sys.argv[1]]()
