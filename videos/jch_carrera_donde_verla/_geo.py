# -*- coding: utf-8 -*-
"""Datos geográficos reales del tramo de la CAIN Road Race (km 78 caseta de Jesús María → km 105 Moyahua).
  python _geo.py ruta      trazo completo de OSM (OSRM overview=full) → geo/ruta.json  (lon, lat, s en metros)
  python _geo.py lugares   poblados, parajes, puentes, miradores y caminos de OSM (Overpass) → geo/osm.json
  python _geo.py curvas    análisis de curvatura + desnivel → geo/curvas.json y tabla en pantalla
Fuentes: OpenStreetMap (© colaboradores de OSM), relieve Terrarium/SRTM (teselas de AWS)."""
import json
import math
import os
import sys
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(AQUI, "geo")
os.makedirs(GEO, exist_ok=True)
CASETA = (-103.15350, 21.09010)     # caseta fitozoosanitaria de Jesús María (km 78): techumbre vista en Esri World Imagery z18
INI = CASETA
FIN = (-103.15911, 21.26135)        # Los Burritos de Moyahua, sobre la carretera (fin del reconocimiento oficial de la ruta)
UA = {"User-Agent": "geo-escolar/1.0"}


def hav(a, b):
    R = 6371000.0
    la1, la2 = math.radians(a[1]), math.radians(b[1])
    dl = math.radians(b[0] - a[0]); dp = la2 - la1
    h = math.sin(dp / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def baja(url, data=None):
    rq = urllib.request.Request(url, data=data, headers=UA)
    return urllib.request.urlopen(rq, timeout=120).read()


def ruta():
    """Trazo = eje de la carretera federal 54 en OSM (geo/mex54.json, encadenado desde geo/osm.json), de la caseta
    fitozoosanitaria (techumbre vista en el satélite, 21.09010 N 103.15350 O) a Los Burritos de Moyahua (fin del
    reconocimiento oficial «Practica Ruta CAIN Road Race 2026» de Alice Reyes 97)."""
    ch = json.load(open(os.path.join(GEO, "mex54.json")))
    ia = min(range(len(ch)), key=lambda i: hav(ch[i], CASETA))
    ib = min(range(len(ch)), key=lambda i: hav(ch[i], FIN))
    co = [[c[0], c[1]] for c in ch[ia:ib + 1]]
    s = [0.0]
    for i in range(1, len(co)):
        s.append(s[-1] + hav(co[i - 1], co[i]))
    json.dump({"coords": co, "s": s, "dist": s[-1]}, open(os.path.join(GEO, "ruta.json"), "w"))
    print(len(co), "puntos;", round(s[-1]), "m; de", co[0], "a", co[-1])


def lugares():
    R = json.load(open(os.path.join(GEO, "ruta.json")))
    lo = [c[0] for c in R["coords"]]; la = [c[1] for c in R["coords"]]
    bb = f"{min(la) - 0.03},{min(lo) - 0.04},{max(la) + 0.03},{max(lo) + 0.04}"
    q = f"""[out:json][timeout:90];
(
  node["place"]({bb});
  node["tourism"]({bb});
  node["natural"="peak"]({bb});
  node["amenity"~"fuel|restaurant|fast_food|hospital|clinic"]({bb});
  way["bridge"]["highway"]({bb});
  way["highway"~"trunk|primary|secondary|tertiary|unclassified|residential|track"]({bb});
  way["waterway"~"river|stream"]["name"]({bb});
);
out body geom;"""
    for srv in ("https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"):
        try:
            d = json.loads(baja(srv, urllib.parse.urlencode({"data": q}).encode()))
            break
        except Exception as e:
            print("falló", srv, e)
    json.dump(d, open(os.path.join(GEO, "osm.json"), "w"))
    print(len(d["elements"]), "elementos")
    for e in d["elements"]:
        t = e.get("tags", {})
        if e["type"] == "node" and (t.get("name") or t.get("tourism")):
            print("NODO", t.get("place") or t.get("tourism") or t.get("amenity") or t.get("natural"), "|", t.get("name"), "|",
                  round(e["lat"], 5), round(e["lon"], 5), "| pob", t.get("population"))
    vistos = set()
    for e in d["elements"]:
        t = e.get("tags", {})
        if e["type"] == "way" and (t.get("bridge") or t.get("waterway")) and (t.get("name"), t.get("ref")) not in vistos:
            vistos.add((t.get("name"), t.get("ref")))
            g = e["geometry"][len(e["geometry"]) // 2]
            print("VIA", "puente" if t.get("bridge") else t.get("waterway"), "|", t.get("name"), "|", t.get("ref"), "|",
                  round(g["lat"], 5), round(g["lon"], 5))



# ---------------------------------------------------------------- relieve y curvas
def _tesela(z, x, y, tipo):
    import io
    from PIL import Image
    d = os.path.join(GEO, "teselas", tipo, str(z)); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f"{x}_{y}.{'png' if tipo == 'dem' else 'jpg'}")
    if not os.path.exists(f):
        u = (f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png" if tipo == "dem" else
             f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")
        for k in range(4):
            try:
                open(f, "wb").write(baja(u)); break
            except Exception as e:
                if k == 3:
                    raise
    return Image.open(f)


def xy_tesela(lon, lat, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def mosaico(lon0, lat0, lon1, lat1, z, tipo):
    """Mosaico de teselas que cubre la caja. Devuelve (imagen o matriz de alturas, x0, y0) con x0, y0 = tesela de la esquina."""
    import numpy as np
    from PIL import Image
    xa, ya = xy_tesela(lon0, lat1, z); xb, yb = xy_tesela(lon1, lat0, z)
    X0, Y0, X1, Y1 = int(xa), int(ya), int(xb), int(yb)
    W, H = (X1 - X0 + 1) * 256, (Y1 - Y0 + 1) * 256
    im = Image.new("RGB", (W, H))
    for x in range(X0, X1 + 1):
        for y in range(Y0, Y1 + 1):
            im.paste(_tesela(z, x, y, tipo).convert("RGB"), ((x - X0) * 256, (y - Y0) * 256))
    if tipo == "dem":
        a = np.asarray(im).astype(np.float64)
        return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768, X0, Y0
    return im, X0, Y0


def altura_de(dem, X0, Y0, z, lon, lat):
    import numpy as np
    x, y = xy_tesela(lon, lat, z)
    px, py = (x - X0) * 256 - 0.5, (y - Y0) * 256 - 0.5
    i, j = int(math.floor(px)), int(math.floor(py))
    fx, fy = px - i, py - j
    i = max(0, min(dem.shape[1] - 2, i)); j = max(0, min(dem.shape[0] - 2, j))
    return (dem[j, i] * (1 - fx) * (1 - fy) + dem[j, i + 1] * fx * (1 - fy) + dem[j + 1, i] * (1 - fx) * fy
            + dem[j + 1, i + 1] * fx * fy)


def remuestrea(co, paso=10.0):
    """Trazo cada `paso` metros en coordenadas locales (este, norte en m) + lon/lat."""
    lat0 = sum(c[1] for c in co) / len(co)
    kx = 111320.0 * math.cos(math.radians(lat0)); ky = 110540.0
    P = [((c[0] - INI[0]) * kx, (c[1] - INI[1]) * ky) for c in co]
    out = [P[0]]; resto = paso
    for a, b in zip(P, P[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1]); u = 0.0
        while d - u >= resto:
            u += resto
            out.append((a[0] + (b[0] - a[0]) * u / d, a[1] + (b[1] - a[1]) * u / d)); resto = paso
        resto -= d - u
    return out, kx, ky


def curvas():
    import numpy as np
    R = json.load(open(os.path.join(GEO, "ruta.json")))
    co = R["coords"]
    P, kx, ky = remuestrea(co, 10.0)
    P = np.array(P)
    n = len(P)
    # rumbo suavizado con ventana de 30 m
    d = P[3:] - P[:-3]
    rum = np.unwrap(np.arctan2(d[:, 0], d[:, 1]))          # rumbo en rad, cada 10 m
    lo = [min(c[0] for c in co) - 0.02, max(c[0] for c in co) + 0.02]
    la = [min(c[1] for c in co) - 0.02, max(c[1] for c in co) + 0.02]
    dem, X0, Y0 = mosaico(lo[0], la[0], lo[1], la[1], 13, "dem")
    alt = np.array([altura_de(dem, X0, Y0, 13, INI[0] + p[0] / kx, INI[1] + p[1] / ky) for p in P])
    print("altura: inicio %.0f m, fin %.0f m, mín %.0f (km %.1f), máx %.0f (km %.1f)" % (
        alt[0], alt[-1], alt.min(), alt.argmin() / 100, alt.max(), alt.argmax() / 100))
    # giro acumulado en ventanas de 200 m (20 pasos)
    V = 20
    giro = np.array([abs(rum[min(len(rum) - 1, i + V)] - rum[i]) for i in range(len(rum))]) * 180 / math.pi
    # curvas individuales: tramos donde |d rumbo / ds| > 1°/10 m... radio < 120 m
    k = np.abs(np.gradient(rum)) / 10.0                   # rad/m
    rad = 1 / np.maximum(k, 1e-6)
    cur = []; i = 0
    while i < len(rum):
        if rad[i] < 150:
            j = i
            sgn = np.sign(rum[min(i + 1, len(rum) - 1)] - rum[i])
            while j + 1 < len(rum) and rad[j + 1] < 220 and np.sign(rum[j + 1] - rum[j]) == sgn:
                j += 1
            ang = abs(rum[j] - rum[i]) * 180 / math.pi
            if ang >= 25:
                m = (i + j) // 2 + 1
                cur.append(dict(s=float(m * 10), ang=float(ang), rmin=float(rad[i:j + 1].min()), largo=float((j - i) * 10),
                                lon=float(INI[0] + P[m][0] / kx), lat=float(INI[1] + P[m][1] / ky), alt=float(alt[m]),
                                lado="der" if sgn > 0 else "izq"))
            i = j + 1
        else:
            i += 1
    print(len(cur), "curvas de ≥ 25° con radio < 150 m")
    json.dump(dict(curvas=cur, alt=[float(a) for a in alt[::5]], n=n, kx=kx, ky=ky), open(os.path.join(GEO, "curvas.json"), "w"))
    print("\nLas 25 más cerradas (ángulo girado):")
    for c in sorted(cur, key=lambda c: -c["ang"])[:25]:
        print("  km %5.2f  %4.0f°  radio mín %3.0f m  largo %3.0f m  %s  alt %4.0f  (%.5f, %.5f)" % (
            c["s"] / 1000, c["ang"], c["rmin"], c["largo"], c["lado"], c["alt"], c["lat"], c["lon"]))
    print("\nDensidad por kilómetro (curvas, giro total):")
    for kmi in range(0, 28):
        cc = [c for c in cur if kmi * 1000 <= c["s"] < (kmi + 1) * 1000]
        a0 = alt[min(n - 1, kmi * 100)]
        print("  km %2d: %2d curvas, %4.0f° girados, alt %4.0f m  %s" % (kmi, len(cc), sum(c["ang"] for c in cc), a0,
                                                                     "#" * int(sum(c["ang"] for c in cc) / 40)))


if __name__ == "__main__":
    globals()[sys.argv[1]]()
