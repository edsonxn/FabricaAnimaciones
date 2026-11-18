# Ubica lugares en mapas/commonwealth.png casando el recorte del Pip-Boy de la wiki (FO4_map_<lugar>.jpg, marcador al centro)
# por template matching en varias escalas. Salida: mapas/_coords.json {slug: [x, y] en fracción 0-1, escala, score} + hoja.
import json
import urllib.parse
import urllib.request

import cv2
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
LUGARES = {
    "sanctuary": "FO4_map_Sanctuary", "crater_atomo": "Crater_of_Atom_map", "medford": "FO4_map_Medford_Mem_Hosp",
    "mass_fusion": "FO4_map_Mass_Fusion", "goodneighbor": "FO4_map_Goodneighbor", "milton": "FO4_map_Milton",
    "refugio81": "FO4_map_Vault_81", "dunwich": "FO4_map_Dunwich_Borers", "manicomio": "FO4_map_Parsons",
    "casa_cabot": "FO4_map_Cabot_House", "diamond_city": "FO4_map_Diamond_City", "borde_mar": "FO4_map_Edge_of_the_Glowing_Sea",
    "instituto": "FO4_map_CIT",
}


def buscar_archivo(pref):
    q = ("https://fallout.fandom.com/api.php?action=query&list=allimages&format=json&ailimit=5&aiprop=url&aiprefix="
         + urllib.parse.quote(pref))
    d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
    im = d.get("query", {}).get("allimages", [])
    return (im[0]["name"], im[0]["url"]) if im else (None, None)


mapa = cv2.imread("mapas/commonwealth.png", cv2.IMREAD_GRAYSCALE)
H, W = mapa.shape
res, hoja = {}, cv2.cvtColor(mapa, cv2.COLOR_GRAY2BGR)
for slug, pref in LUGARES.items():
    nombre, url = buscar_archivo(pref)
    if not url:
        print("SIN ARCHIVO", slug, pref)
        continue
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    t = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_GRAYSCALE)
    th, tw = t.shape
    c = t[th // 2 - th // 4: th // 2 + th // 4, tw // 2 - tw // 4: tw // 2 + tw // 4]   # centro (evita marcos y textos)
    mejor = (-1, None, None)
    for esc in np.linspace(0.70, 0.86, 33):
        r = cv2.resize(c, (max(8, int(c.shape[1] * esc)), max(8, int(c.shape[0] * esc))))
        if r.shape[0] >= H or r.shape[1] >= W:
            continue
        m = cv2.matchTemplate(mapa, r, cv2.TM_CCOEFF_NORMED)
        _, v, _, p = cv2.minMaxLoc(m)
        if v > mejor[0]:
            mejor = (v, esc, (p[0] + r.shape[1] / 2, p[1] + r.shape[0] / 2))
    v, esc, (x, y) = mejor
    res[slug] = dict(xy=[round(x / W, 4), round(y / H, 4)], escala=round(float(esc), 3), score=round(float(v), 3), archivo=nombre)
    print(f"{slug:14s} {nombre:45s} score={v:.3f} esc={esc:.2f} xy=({x / W:.3f},{y / H:.3f})")
    cv2.circle(hoja, (int(x), int(y)), 14, (0, 0, 255), 3)
    cv2.putText(hoja, slug, (int(x) + 16, int(y)), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 255, 255), 2)
json.dump(res, open("mapas/_coords.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cv2.imwrite("previews/_coords.jpg", cv2.resize(hoja, (1100, 1100)))
