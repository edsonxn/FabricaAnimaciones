# Ubica lugares en mapas/commonwealth.png (mapa real del Pip-Boy, 2048²) a partir de los recortes del Pip-Boy de la wiki
# (mapas/_recortes/FO4_map_*.jpg). El ícono de cada lugar se leyó a mano EN EL RECORTE junto a su rótulo (px del recorte);
# el recorte se registra contra el mapa por template matching multiescala del recorte ENTERO y el punto se proyecta.
# Comprobación: previews/_coords_check.jpg (recorte | mapa en el mismo encuadre) y previews/_coords.jpg.
import json

import cv2
import numpy as np

R = "mapas/_recortes/"
# recorte: [(slug, nombre en pantalla, (x, y) del ícono en el recorte)]
PUNTOS = {
    "FO4_map_Sanctuary.jpg": [("sanctuary", "Sanctuary Hills", (252, 158))],
    "Crater_of_Atom_map.jpg": [("crater_atomo", "Cráter del Átomo", (221, 207))],
    "FO4_map_Medford_Mem_Hosp.jpg": [("medford", "Hospital de Medford", (378, 438))],
    "FO4_map_Milton_general_Hospital.jpg": [("milton", "Hospital Milton General", (455, 88))],
    "FO4_map_Mass_Fusion_Building.jpg": [("mass_fusion", "Mass Fusion", (1012, 107)), ("goodneighbor", "Goodneighbor", (1055, 205)),
                                         ("diamond_city", "Diamond City", (283, 565))],
    "FO4_map_Vault_81.jpg": [("refugio81", "Refugio 81", (688, 228))],
    "FO4_map_Dunwich_Borers.jpg": [("dunwich", "Dunwich Borers", (275, 345)), ("manicomio", "Manicomio Estatal Parsons", (132, 178))],
    "FO4_map_Cabot_House.jpg": [("casa_cabot", "Casa Cabot", (597, 446)), ("instituto", "Ruinas del C.I.T. (Instituto)", (243, 505))],
}


def gris(im):
    return cv2.GaussianBlur(im[:, :, 1], (3, 3), 0).astype(np.float32)


mapa_c = cv2.imread("mapas/commonwealth.png")
mapa = gris(mapa_c)
H, W = mapa.shape
res, filas = {}, []
for arch, pts in PUNTOS.items():
    t = cv2.imread(R + arch)
    tg = gris(t)
    th, tw = tg.shape
    mejor = (-1, 0, (0, 0))
    for esc in np.concatenate([np.linspace(0.30, 0.50, 41), np.linspace(0.60, 0.95, 71)]):
        r = cv2.resize(tg, (int(tw * esc), int(th * esc)), interpolation=cv2.INTER_AREA)
        m = cv2.matchTemplate(mapa, r, cv2.TM_CCOEFF_NORMED)
        _, v, _, p = cv2.minMaxLoc(m)
        if v > mejor[0]:
            mejor = (v, esc, p)
    v, esc, (ox, oy) = mejor
    print(f"{arch:40s} score={v:.3f} esc={esc:.3f} origen=({ox},{oy})")
    for slug, nom, (px, py) in pts:
        mx, my = ox + px * esc, oy + py * esc
        res[slug] = dict(xy=[round(mx / W, 4), round(my / H, 4)], nombre=nom, recorte=arch, escala=round(float(esc), 3),
                         score=round(float(v), 3))
        print(f"   {slug:13s} -> ({mx / W:.4f}, {my / H:.4f})")
        # fila de comprobación: recorte alrededor del ícono | mapa alrededor del punto, mismo encuadre
        a = t[max(0, py - 120):py + 120, max(0, px - 160):px + 160].copy()
        cv2.circle(a, (min(px, 160), min(py, 120)), 22, (0, 0, 255), 2)
        rr = 120 * esc
        x0, y0 = int(mx - 160 * esc), int(my - rr)
        b = mapa_c[max(0, y0):int(my + rr), max(0, x0):int(mx + 160 * esc)].copy()
        b = cv2.resize(b, (int(b.shape[1] / esc), int(b.shape[0] / esc)))
        cv2.circle(b, (int((mx - max(0, x0)) / esc), int((my - max(0, y0)) / esc)), 22, (0, 0, 255), 2)
        fila = np.zeros((260, 680, 3), np.uint8)
        fila[20:20 + a.shape[0], 0:a.shape[1]] = a
        fila[20:20 + min(240, b.shape[0]), 350:350 + min(320, b.shape[1])] = b[:240, :320]
        cv2.putText(fila, f"{nom}  ({mx / W:.3f},{my / H:.3f})", (4, 14), 0, 0.45, (0, 255, 255), 1)
        filas.append(fila)
json.dump(res, open("mapas/_coords.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cols = 2
while len(filas) % cols:
    filas.append(np.zeros_like(filas[0]))
hoja = np.vstack([np.hstack(filas[i:i + cols]) for i in range(0, len(filas), cols)])
cv2.imwrite("previews/_coords_check.jpg", hoja)
g = mapa_c.copy()
for s, d in res.items():
    x, y = int(d["xy"][0] * W), int(d["xy"][1] * H)
    cv2.circle(g, (x, y), 14, (0, 0, 255), 4)
    cv2.putText(g, s, (x + 16, y + 6), 0, 1.0, (255, 255, 255), 3)
cv2.imwrite("previews/_coords.jpg", cv2.resize(g, (1200, 1200)))
