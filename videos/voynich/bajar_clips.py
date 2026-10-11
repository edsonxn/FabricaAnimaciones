# -*- coding: utf-8 -*-
"""Descarga el video de apoyo (Pexels/Pixabay) del documental. Créditos en clips/creditos_clips.json."""
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import videos_stock as V

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "clips")
os.makedirs(D, exist_ok=True)
CLIPS = {
    "paginas1": ("pexels", 35972510), "paginas2": ("pexels", 13617608), "paginas3": ("pexels", 7235016),
    "vela": ("pexels", 12550702), "vela2": ("pexels", 12123574),
    "pluma": ("pexels", 7977624), "escribir": ("pexels", 11137423),
    "polvo": ("pexels", 36637658), "polvo2": ("pexels", 30922259),
    "biblioteca": ("pexels", 29241899), "pagina_cerca": ("pexels", 4061881),
    "praga": ("pexels", 20640019), "praga_reloj": ("pexels", 20640178),
    "maquina": ("pexels", 34143147), "maquina2": ("pexels", 6980925),
    "codigo": ("pexels", 31699019), "codigo2": ("pexels", 30162924),
    "microscopio": ("pexels", 9373536), "microscopio2": ("pexels", 4121620),
    "monedas": ("pexels", 6327801), "monedas2": ("pexels", 30804767),
    "mapa_vela": ("pexels", 10480415), "mapa_lupa": ("pexels", 7431747),
    "reloj_bolsillo": ("pexels", 10284259), "reloj_oscuro": ("pexels", 30084927),
    "tinta": ("pexels", 18333375), "humo": ("pexels", 4320605), "proyector": ("pexels", 855120),
    "carta_lupa": ("pexels", 6979937), "carta": ("pexels", 7347571),
    "papel_fuego": ("pexels", 8828893), "fichas": ("pexels", 6550666),
}


def uno(item):
    nombre, (fuente, vid) = item
    ruta = os.path.join(D, nombre + ".mp4")
    if os.path.exists(ruta) and os.path.getsize(ruta) > 100000:
        return nombre, "ya"
    try:
        v = V.buscar_id(fuente, vid)[0]
        f = V.descargar(v, ruta)
        V.anotar(D, nombre, v, f)
        return nombre, f"{f['w']}x{f['h']} {os.path.getsize(ruta) // 1024} KB"
    except Exception as e:
        return nombre, f"FALLO {e}"


with ThreadPoolExecutor(4) as ex:
    for n, r in ex.map(uno, CLIPS.items()):
        print(n, r, flush=True)
