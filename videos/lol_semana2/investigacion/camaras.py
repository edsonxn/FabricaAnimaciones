# Cámara de cada fuente (para las rutas medidas): python investigacion/camaras.py g1_j1 g1_j2 ... → investigacion/cam_<n>.json
import json, os, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(D, "..", "..", "nucleo", "tactica3d"))
import rastros_vod as RV
for n in sys.argv[1:]:
    out = os.path.join(D, "investigacion", f"cam_{n}.json")
    if os.path.exists(out):
        continue
    cam = RV.camara_clip(os.path.join(D, "medios", "_fuente", n + ".mp4"))
    json.dump(cam, open(out, "w"))
    print(n, len(cam), "cortes:", [c[0] for c in cam if c[1] is None][:20])
