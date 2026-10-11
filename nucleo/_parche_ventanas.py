# -*- coding: utf-8 -*-
"""Parche: el mapa soporta varias ventanas de relieve (México y Europa occidental). Regenera relieve_mx.npz y crea relieve_eu.npz."""
import os
import re

# ------------------------------------------------------------------ 1) kz_mapa_datos.py
p = 'kz_mapa_datos.py'
s = open(p, encoding='utf-8').read()

s = s.replace("def rios(alt, umbral=260):", "def rios(alt, lat0=LAT0, lon0=LON0, umbral=260):")
s = s.replace("        lat = LAT0 + ii * PASO\n        lon = LON0 + jj * PASO\n", "        lat = lat0 + ii * PASO\n        lon = lon0 + jj * PASO\n")

a = s.index("def main():")
nuevo = '''VENTANAS = {
    "mx": os.path.join(RAIZ, "videos", "independencia_mx", "datos", "relieve_mx_etopo1.nc"),
    "eu": os.path.join(RAIZ, "videos", "independencia_mx", "datos", "relieve_eu_etopo1.nc"),
}


def ventana(nombre):
    """Lee un .nc de NOAA ETOPO1 (altitud en m), calcula los ríos y guarda nucleo/datos/relieve_<nombre>.npz."""
    from scipy.io import netcdf_file
    f = netcdf_file(VENTANAS[nombre], "r", mmap=False)
    alt = f.variables["altitude"][:].astype(np.int16).copy()
    lat = f.variables["latitude"][:].copy()
    lon = f.variables["longitude"][:].copy()
    lat0, lon0 = float(lat[0]), float(lon[0])
    print(nombre, "relieve", alt.shape, alt.min(), alt.max(), "lat0", lat0, "lon0", lon0)
    rs, acc = rios(alt, lat0, lon0)
    print("  ríos:", len(rs), "tramos")
    pts = np.concatenate(rs)
    cortes = np.cumsum([0] + [len(r) for r in rs]).astype(np.int32)
    np.savez_compressed(os.path.join(SAL, f"relieve_{nombre}.npz"), alt=alt, lat0=lat0, lon0=lon0, paso=PASO, rios_pts=pts, rios_cortes=cortes, acc=np.log1p(acc).astype(np.float16))


def main():
    os.makedirs(SAL, exist_ok=True)
    for nombre in VENTANAS:
        if os.path.isfile(VENTANAS[nombre]):
            ventana(nombre)
    json.dump(paises(), open(os.path.join(SAL, "paises.json"), "w"), separators=(",", ":"))
    json.dump(lagos(), open(os.path.join(SAL, "lagos.json"), "w"), separators=(",", ":"))
    for n in sorted(os.listdir(SAL)):
        print(n, os.path.getsize(os.path.join(SAL, n)) // 1024, "KB")


if __name__ == "__main__":
    main()
'''
s = s[:a] + nuevo
open(p, 'w', encoding='utf-8').write(s)

# ------------------------------------------------------------------ 2) kz_mapa.py
p = 'kz_mapa.py'
s = open(p, encoding='utf-8').read()

# 2a) clase Ventana
s = s.replace("class Mapa:\n    \"\"\"Singleton perezoso.", '''class Ventana:
    """Una ventana rectangular de relieve ETOPO1 (1' de arco) con su pirámide de niveles, humedad y ríos calculados."""

    def __init__(self, nombre, ruta, hum_fn):
        d = np.load(ruta)
        self.nombre = nombre
        self.alt = d["alt"].astype(np.float32)
        self.lat0, self.lon0, self.paso = float(d["lat0"]), float(d["lon0"]), float(d["paso"])
        h, w = self.alt.shape
        self.lat_min, self.lat_max = self.lat0, self.lat0 + (h - 1) * self.paso
        self.lon_min, self.lon_max = self.lon0, self.lon0 + (w - 1) * self.paso
        lat = self.lat0 + np.arange(h, dtype=np.float32)[:, None] * self.paso
        lon = self.lon0 + np.arange(w, dtype=np.float32)[None, :] * self.paso
        self.hum = hum_fn(lon * np.ones((h, 1), np.float32), lat * np.ones((1, w), np.float32))
        self.pir = [self.alt]
        self.pir_h = [self.hum]
        self.escalas = [1.0]
        for _ in range(3):
            self.pir.append(cv2.pyrDown(self.pir[-1]))
            self.pir_h.append(cv2.pyrDown(self.pir_h[-1]))
            self.escalas.append(self.escalas[-1] * 2)
        rp = d["rios_pts"]
        self.r_lon, self.r_lat, self.r_ln = rp[:, 0].astype(np.float64), rp[:, 1].astype(np.float64), np.log1p(rp[:, 2]).astype(np.float32)
        self.r_cortes = d["rios_cortes"].astype(np.int64)

    def afin_h(self, cam, nivel):
        """Matriz 2x3: destino a media resolución (x, y) -> índices (j, i) del nivel de la pirámide (WARP_INVERSE_MAP)."""
        lo, la, z = cam
        e = self.escalas[nivel]
        x0, y0 = XY(lo, la)
        kj = 1.0 / (z * K * KX * self.paso * e)
        aj = ((x0 - 960 / z) / (K * KX) - 101.0 - self.lon0) / (self.paso * e) - (e - 1) / (2.0 * e)
        ki = -1.0 / (z * K * self.paso * e)
        ai = (21.0 - (y0 - 540 / z) / K - self.lat0) / (self.paso * e) - (e - 1) / (2.0 * e)
        A = np.array([[kj, 0, aj], [0, ki, ai], [0, 0, 1.0]])
        S = np.array([[2.0, 0, 0.5], [0, 2.0, 0.5], [0, 0, 1.0]])
        return (A @ S)[:2]

    def toca(self, cam):
        """¿La ventana aparece en pantalla para esta cámara?"""
        lo, la, z = cam
        dx = 960 / (z * K * KX)
        dy = 540 / (z * K)
        return not (lo + dx < self.lon_min or lo - dx > self.lon_max or la + dy < self.lat_min or la - dy > self.lat_max)


class Mapa:
    """Singleton perezoso.''', 1)

# 2b) _cargar con ventanas
a = s.index("        d = np.load(os.path.join(DATOS, \"relieve_mx.npz\"))")
b = s.index("        self.paises = {k:")
nuevo = '''        self.vent = []
        for nombre, fn in (("mx", _humedad), ("eu", lambda lo, la: _clima_global(lo, la)[0])):
            ruta = os.path.join(DATOS, f"relieve_{nombre}.npz")
            if os.path.isfile(ruta):
                self.vent.append(Ventana(nombre, ruta, fn))
        v0 = self.vent[0]
        self.lat0, self.lon0, self.paso = v0.lat0, v0.lon0, v0.paso            # compatibilidad: la ventana de México
        # ríos de todas las ventanas en un solo arreglo (con sus cortes desplazados)
        self.r_lon = np.concatenate([v.r_lon for v in self.vent])
        self.r_lat = np.concatenate([v.r_lat for v in self.vent])
        self.r_ln = np.concatenate([v.r_ln for v in self.vent])
        cortes, off = [np.array([0], np.int64)], 0
        for v in self.vent:
            cortes.append(v.r_cortes[1:] + off)
            off += len(v.r_lon)
        self.r_cortes = np.concatenate(cortes)
'''
s = s[:a] + nuevo + s[b:]
s = s.replace("        self.alt = alt\n        h, w = alt.shape\n", "")
open(p, 'w', encoding='utf-8').write(s)
print('ok parte 1')
