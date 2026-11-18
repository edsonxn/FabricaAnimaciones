# Ubica lugares en mapas/commonwealth.png con SIFT + RANSAC (invariante a escala) casando el recorte del Pip-Boy de la
# wiki (FO4_map_<lugar>.jpg, marcador al centro) contra el mapa real. Sustituye al template matching de _ubicar.py,
# que fallaba por la escala. Salida: mapas/_coords.json {slug: xy 0-1, escala, inliers} + previews/_coords.jpg.
import json
import os
import urllib.parse
import urllib.request

import cv2
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
LUGARES = {
    "sanctuary": "FO4_map_Sanctuary", "crater_atomo": "Crater_of_Atom_map", "medford": "FO4_map_Medford_Mem",
    "mass_fusion": "FO4_map_Mass_Fusion", "goodneighbor": "FO4_map_Goodneighbor", "milton": "FO4_map_Milton",
    "refugio81": "FO4_map_Vault_81", "dunwich": "FO4_map_Dunwich_Borers", "manicomio": "FO4_map_Parsons_State",
    "casa_cabot": "FO4_map_Cabot_House", "diamond_city": "FO4_map_Diamond_City", "borde_mar": "FO4_map_Edge_of_the_Glowing_Sea",
    "refugio111": "FO4_map_Vault_111", "concord": "FO4_map_Concord",
}
CACHE = "mapas/_recortes"
os.makedirs(CACHE, exist_ok=True)


def buscar_archivos(pref):
    q = ("https://fallout.fandom.com/api.php?action=query&list=allimages&format=json&ailimit=8&aiprop=url&aiprefix="
         + urllib.parse.quote(pref))
    d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
    return [(i["name"], i["url"]) for i in d.get("query", {}).get("allimages", [])]


def prep(g):
    return cv2.createCLAHE(2.0, (8, 8)).apply(g)


mapa_c = cv2.imread("mapas/commonwealth.png")
mapa = prep(mapa_c[:, :, 1])
H, W = mapa.shape
sift = cv2.SIFT_create(nfeatures=60000)
km, dm = sift.detectAndCompute(mapa, None)
bf = cv2.BFMatcher(cv2.NORM_L2)
res, hoja = {}, mapa_c.copy()
for slug, pref in LUGARES.items():
    cands = buscar_archivos(pref)
    if not cands:
        print("SIN ARCHIVO", slug, pref)
        continue
    nombre, url = cands[0]
    ruta = os.path.join(CACHE, nombre)
    if not os.path.exists(ruta):
        open(ruta, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())
    t = cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_COLOR)
    tg = prep(t[:, :, 1])
    th, tw = tg.shape
    kt, dt = sift.detectAndCompute(tg, None)
    if dt is None:
        print("sin rasgos", slug)
        continue
    ms = bf.knnMatch(dt, dm, k=2)
    good = [m for m, n in (p for p in ms if len(p) == 2) if m.distance < 0.8 * n.distance]
    if len(good) < 6:
        print(f"{slug:13s} {nombre:42s} pocos pares ({len(good)})")
        continue
    src = np.float32([kt[m.queryIdx].pt for m in good])
    dst = np.float32([km[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=6, maxIters=20000)
    n_in = int(inl.sum()) if inl is not None else 0
    if M is None:
        print(f"{slug:13s} sin transformación")
        continue
    esc = float(np.hypot(M[0, 0], M[1, 0]))
    cx, cy = M @ np.array([tw / 2, th / 2, 1.0])
    res[slug] = dict(xy=[round(cx / W, 4), round(cy / H, 4)], escala=round(esc, 3), inliers=n_in, pares=len(good),
                     archivo=nombre, tam=[tw, th])
    print(f"{slug:13s} {nombre:42s} inliers={n_in:4d}/{len(good):4d} esc={esc:.3f} xy=({cx / W:.3f},{cy / H:.3f})")
    # dibuja el contorno del recorte proyectado y el centro
    caja = np.float32([[0, 0, 1], [tw, 0, 1], [tw, th, 1], [0, th, 1]]) @ M.T
    cv2.polylines(hoja, [caja.astype(np.int32)], True, (0, 200, 255), 3)
    cv2.circle(hoja, (int(cx), int(cy)), 16, (0, 0, 255), 4)
    cv2.putText(hoja, slug, (int(cx) + 18, int(cy) + 8), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)
json.dump(res, open("mapas/_coords.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cv2.imwrite("previews/_coords.jpg", cv2.resize(hoja, (1400, 1400)))
