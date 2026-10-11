# -*- coding: utf-8 -*-
"""Baja candidatos de b-roll libre (Pexels/Pixabay) a clips/stock/<tema>_<n>.mp4 para elegir a ojo. Créditos en clips/stock/creditos_clips.json."""
import os, sys, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import videos_stock as V

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "clips", "stock")
os.makedirs(D, exist_ok=True)
TEMAS = {
    "celdas": "prison cells row empty", "alambre": "barbed wire fence dark", "mazo": "judge gavel courtroom", "balanza": "scales of justice",
    "policia_noche": "police car lights night", "ambulancia": "ambulance flashing lights night", "hospital": "hospital corridor empty",
    "reloj": "clock ticking close up", "bosque_niebla": "foggy forest dark woods", "lluvia_ventana": "rain window night",
    "vela": "candle flame dark", "pc_antigua": "old computer monitor", "calendario": "calendar pages flipping", "periodico": "newspaper headlines press",
    "esposas": "handcuffs close up", "tormenta": "dark storm clouds timelapse", "pasillo_oscuro": "dark hallway corridor", "monitor_cardiaco": "heart monitor hospital",
    "suero": "IV drip hospital bed", "montanas_wv": "appalachian mountains aerial fog", "ciudad_noche": "city skyline night aerial", "camilla": "hospital gurney corridor",
    "ventana_celda": "prison window light bars", "documento": "legal documents signing desk", "carretera_noche": "highway night driving lights",
}
N = 3


def uno(item):
    tema, q = item
    out = []
    try:
        res = V.pexels(q, N) + V.pixabay(q, N)
    except Exception as e:
        return tema, f"FALLO búsqueda {e}"
    k = 0
    for v in res:
        if k >= N + 1:
            break
        ruta = os.path.join(D, f"{tema}_{k}.mp4")
        if os.path.exists(ruta) and os.path.getsize(ruta) > 100000:
            k += 1
            continue
        try:
            f = V.descargar(v, ruta)
            V.anotar(D, f"{tema}_{k}", v, f)
            out.append(f"{tema}_{k} {v['fuente']} {v['id']} {v['dur']}s {f['w']}x{f['h']}")
            k += 1
        except Exception as e:
            out.append(f"{tema}_{k} FALLO {e}")
    return tema, out


if __name__ == "__main__":
    sel = sys.argv[1:] or list(TEMAS)
    with ThreadPoolExecutor(4) as ex:
        for t, r in ex.map(uno, [(t, TEMAS[t]) for t in sel]):
            print(t, r, flush=True)
