import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import imagenes_web as iw
GEN = {"User-Agent": "FabricaAnimaciones/1.0 python-urllib"}
iw.UA = GEN; iw._get.__defaults__ = (GEN, 40); iw.guardar_commons.__globals__["UA"] = GEN
c = json.load(open("imagenes/_cand/_cand.json", encoding="utf-8"))
por_titulo = {v["titulo"]: v for v in c.values()}
QUIERO = {"musk": "Elon Musk Colorado 2022 (cropped2)", "pata": "Falcon 9 landing leg in SpaceX headquarters",
          "orbcomm": "ORBCOMM-2 First-Stage Landing (23271687254)", "crs8": "CRS-8 first stage landing (26300510612)",
          "mechazilla": "Starship Booster Landing on Mechzilla (54064036815)", "lz1": "Falcon 9 first stage at LZ-1(two)",
          "hls": "HLS Starship rendering", "hls2": "Depict SpaceX", "aproxima": "Starship Booster Return on Final Approach (54063904149).jpg"}
for nom, frag in QUIERO.items():
    m = [v for t, v in por_titulo.items() if frag in t]
    if not m: print("NO", nom); continue
    time.sleep(4)
    try:
        print(nom, iw.guardar_commons(m[0], "imagenes", nom), m[0]["licencia"])
    except Exception as e:
        print("ERR", nom, e)
