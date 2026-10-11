# -*- coding: utf-8 -*-
"""Mapa con relieve REAL para el estilo Kurzgesagt (México y alrededores), reutilizable por cualquier video de historia de México.

Datos (nucleo/datos/, generados por kz_mapa_datos.py): relieve y batimetría NOAA ETOPO1 (1'), polígonos de países y lagos Natural Earth 50 m
(dominio público) y ríos calculados del propio relieve.

Proyección (la misma de siempre): X = (lon + 101) * K * cos(22°), Y = -(lat - 21) * K  (px a zoom 1, K = 100). Cámara = (lon, lat, z):
el punto cae en el centro de la pantalla (960, 540).

Uso en una toma:
    M = kz_mapa.MAPA                      # singleton con carga perezosa
    bg = lambda t: M.base(cam(t), t)      # fondo (np.float32 H x W x 3 en [0, 1]): mar con profundidad, tierra con relieve, ríos, costa
    ... en dibujar(lz, t): iconos, ciudades, rutas, ejércitos y rótulos encima (kz_mapa_dib.py)
Coste ~0,1 s por cuadro (todo el color se calcula a media resolución).
"""
import json
import math
import os

import cv2
import numpy as np

from motor import W, H, catmull

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
K = 100.0
KX = math.cos(math.radians(22.0))
NODATA = -32000.0
WH, HH = W // 2, H // 2


def XY(lon, lat):
    return (np.asarray(lon, float) + 101.0) * K * KX, -(np.asarray(lat, float) - 21.0) * K


def _suave_np(x, a, b):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------------------------------- paletas
def _rampa(puntos, n):
    """puntos: [(valor, (r, g, b)), ...] -> tabla (n, 3) float32 en [0, 1] interpolada linealmente, valores en [0, n)."""
    v = np.array([p[0] for p in puntos], float)
    c = np.array([p[1] for p in puntos], float) / 255.0
    xs = np.arange(n, dtype=float)
    return np.stack([np.interp(xs, v, c[:, k]) for k in range(3)], 1).astype(np.float32)


# tierra: altitud en m (índice = m / 10): seca y húmeda (colores limpios, sin barro: las sombras se mezclan hacia violeta, no hacia negro)
_ALT = [(0, (244, 218, 160)), (15, (244, 214, 152)), (70, (246, 208, 142)), (140, (247, 198, 122)), (220, (238, 168, 110)), (300, (214, 136, 108)),
        (380, (182, 124, 128)), (440, (210, 192, 208)), (490, (248, 248, 255)), (600, (255, 255, 255))]
_ALT_H = [(0, (100, 192, 128)), (15, (112, 196, 124)), (70, (150, 204, 120)), (140, (178, 206, 116)), (220, (126, 186, 112)), (300, (98, 156, 114)),
          (380, (156, 134, 128)), (440, (210, 192, 208)), (490, (248, 248, 255)), (600, (255, 255, 255))]
# mar: profundidad en m (índice = m / 10); plano desde 1600 m para que no se note el borde de la ventana de datos
_MAR = [(0, (112, 214, 222)), (20, (72, 184, 216)), (120, (50, 140, 214)), (300, (36, 100, 190)), (800, (28, 70, 160)), (1600, (22, 52, 128)), (6000, (22, 52, 128))]

_C_SOMBRA = np.array([70, 50, 126], np.float32) / 255.0
_C_LUZ = np.array([255, 246, 218], np.float32) / 255.0
_C_ORILLA = np.array([1.0, 0.97, 0.86], np.float32)
_C_AGUA = np.array([0.34, 0.68, 0.92], np.float32)
SECO = _rampa(_ALT, 600)
HUMEDO = _rampa(_ALT_H, 600)
FONDO_MAR = _rampa(_MAR, 600)

TIERRA = (222, 168, 104)
ORO = (255, 206, 72)
ROJO_REAL = (226, 84, 78)
VERDE_INS = (96, 206, 140)
AZUL_REG = (86, 150, 230)

# humedad aproximada (0 desierto ... 1 selva): pocos «focos» húmedos y secos sobre un gradiente norte-sur. Es dirección de arte, no un dato climático
_HUM_BASE = lambda lat: 0.40 - 0.028 * np.clip(lat - 17.0, 0, 20)
_HUMEDOS = [(-97.4, 21.0, 2.4, 0.46), (-96.0, 18.6, 2.6, 0.50), (-92.8, 17.9, 3.2, 0.60), (-91.0, 15.8, 2.2, 0.45), (-99.8, 17.2, 2.4, 0.38),
            (-96.0, 16.2, 2.0, 0.32), (-105.0, 20.4, 1.9, 0.34), (-104.2, 23.4, 1.6, 0.20), (-107.0, 26.6, 1.5, 0.24), (-89.0, 17.6, 2.4, 0.36),
            (-92.5, 15.4, 1.3, 0.36), (-98.2, 19.6, 1.4, 0.26), (-100.8, 19.4, 1.5, 0.26), (-102.2, 18.7, 1.6, 0.22), (-99.5, 24.5, 1.0, 0.16)]
_SECOS = [(-112.5, 29.0, 4.5, 0.40), (-114.0, 26.0, 3.0, 0.40), (-104.5, 29.0, 3.5, 0.34), (-102.0, 26.8, 3.0, 0.34), (-110.5, 31.0, 3.2, 0.30),
          (-89.0, 21.0, 1.9, 0.26), (-97.5, 20.0, 0.6, 0.10), (-98.2, 18.2, 1.0, 0.18), (-103.5, 32.0, 4.0, 0.30)]


def _humedad(lon, lat):
    h = _HUM_BASE(lat) * np.ones_like(lon)
    for (lo, la, s, a) in _HUMEDOS:
        h = h + a * np.exp(-(((lon - lo) / s) ** 2 + ((lat - la) / (s * 0.8)) ** 2))
    for (lo, la, s, a) in _SECOS:
        h = h - a * np.exp(-(((lon - lo) / s) ** 2 + ((lat - la) / (s * 0.8)) ** 2))
    return np.clip(h, 0.0, 1.0).astype(np.float32)


def _clima_global(lon, lat):
    """(humedad 0..1, altitud extra en m) para tierra SIN datos de relieve: dirección de arte, no un dato climático. Sahara seco, trópicos verdes, hielo en Groenlandia,
    Andes, Rocosas y Alpes elevados."""
    hum = np.full_like(lon, 0.45)
    alt = np.zeros_like(lon)
    for dst, terminos in ((hum, _HUM_T), (alt, _ALT_T)):
        for a, lo, la, sx, sy, norte in terminos:
            g = np.exp(-(((lon - lo) / sx) ** 2 + ((lat - la) / sy) ** 2))
            dst += a * (g * (lat > 60) if norte else g)
    return np.clip(hum, 0.0, 1.0).astype(np.float32), alt.astype(np.float32)


def _clima_global_rejilla(lon1, lat1):
    """_clima_global sobre la rejilla lat1 (alto) x lon1 (ancho) de una cámara sin rotación. Cada gaussiana es
    separable (g = gx(lon) * gy(lat)), así que la suma de todas es una multiplicación de matrices (alto x n) @ (n x ancho):
    ~0,19 s -> pocos ms por cuadro de mapa, con el mismo resultado (diferencias de redondeo, ~1e-6)."""
    lon1 = np.asarray(lon1, np.float64)
    lat1 = np.asarray(lat1, np.float64)
    hum = np.full((len(lat1), len(lon1)), 0.45)
    alt = np.zeros((len(lat1), len(lon1)))
    for dst, terminos in ((hum, _HUM_T), (alt, _ALT_T)):
        A = np.stack([a * np.exp(-((lat1 - la) / sy) ** 2) * ((lat1 > 60) if norte else 1.0)
                      for a, lo, la, sx, sy, norte in terminos], 1)
        B = np.stack([np.exp(-((lon1 - lo) / sx) ** 2) for a, lo, la, sx, sy, norte in terminos], 0)
        dst += A @ B
    return np.clip(hum, 0.0, 1.0).astype(np.float32), alt.astype(np.float32)


# Términos de _clima_global: (amplitud con signo, lon, lat, sx, sy, solo al norte de 60°). Dirección de arte: Amazonia y
# Congo húmedos, Sahara/Atacama/desiertos de EE. UU. y Arabia secos, Europa e Iberia matizadas; Andes, Rocosas, Alpes,
# Atlas, Pirineos y Groenlandia elevados.
_HUM_T = [(0.45, -60, -3, 22, 9, 0), (0.40, 18, 0, 16, 9, 0), (0.35, -80, 6, 6, 5, 0), (0.30, 100, 0, 1, 1, 0),
          (-0.60, 8, 24, 28, 7, 0), (-0.40, -69, -22, 7, 8, 0), (-0.35, -105, 34, 14, 7, 0), (-0.40, 38, 28, 12, 7, 0),
          (-0.25, -68, -42, 6, 10, 0), (0.15, 10, 50, 22, 8, 0),
          (0.34, 2, 47, 5, 3.4, 0), (0.28, -2, 52, 6, 3, 0), (0.38, -6.0, 43.3, 5, 0.9, 0), (0.20, 12, 43, 4, 3, 0),
          (0.25, 9, 49, 5, 2.5, 0), (-0.42, -3.8, 39.8, 5, 2.2, 0), (-0.38, -5, 37.4, 4, 1.3, 0), (-0.25, -1, 40.2, 2, 2, 0),
          (-0.30, -100, 62, 40, 10, 0)]
_ALT_T = [(3400, -76, -10, 6, 20, 0), (2600, -110, 44, 7, 12, 0), (2800, 9, 46.5, 7, 2.2, 0), (2000, -5, 31, 6, 3, 0),
          (1500, -3, 42.5, 3, 1.0, 0), (2400, -45, 72, 24, 9, 1),
          (1400, 30, 8, 9, 8, 0), (1300, 16, -22, 8, 8, 0), (1100, -52, -15, 9, 9, 0), (900, 25, 60, 14, 6, 0)]


class Ventana:
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
    """Singleton perezoso. `base(cam, t)` -> fondo del mapa; `proy(cam, lon, lat)` -> pantalla."""

    def __init__(self):
        self._ok = False

    # ------------------------------------------------------------------ carga
    def _cargar(self):
        if self._ok:
            return
        self.vent = []
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
        self.paises = {k: [np.array(p, np.float32) for p in v] for k, v in json.load(open(os.path.join(DATOS, "paises.json"))).items()}
        self.lagos = [dict(nombre=l["nombre"], pts=np.array(l["pts"], np.float32)) for l in json.load(open(os.path.join(DATOS, "lagos.json")))]
        # lagos históricos del valle de México (Texcoco, Xochimilco-Chalco), aproximados a mano y suavizados
        for nombre, pts in (("Texcoco", [(-99.04, 19.62), (-98.93, 19.58), (-98.88, 19.48), (-98.93, 19.38), (-99.02, 19.36), (-99.08, 19.42), (-99.07, 19.52)]),
                            ("Xochimilco", [(-99.12, 19.30), (-99.02, 19.30), (-98.97, 19.22), (-99.05, 19.16), (-99.14, 19.2)])):
            self.lagos.append(dict(nombre=nombre, pts=np.array(catmull(np.array(pts, float), 6, True), np.float32)))
        self.vec_mx = [p for p in self.paises["Mexico"]]
        self.vec_otros = [p for k, v in self.paises.items() if k != "Mexico" for p in v]
        self.yy2, self.xx2 = np.mgrid[0:HH, 0:WH].astype(np.float32)
        rng = np.random.default_rng(7)
        n = rng.normal(0, 1, (270, 480)).astype(np.float32)
        self._ruido = cv2.GaussianBlur(n, (0, 0), 3.0) * 3.0 + cv2.GaussianBlur(rng.normal(0, 1, (270, 480)).astype(np.float32), (0, 0), 1.2)
        self._ok = True

    # ------------------------------------------------------------------ máscara de tierra (para colocar cosas solo en el mar)
    def _mascara_tierra(self):
        if getattr(self, "_mt", None) is not None:
            return
        self._cargar()
        res = 10.0                                              # celdas por grado
        self._mt0 = (-135.0, -58.0)
        w, h = int(200 * res), int(135 * res)
        m = np.zeros((h, w), np.uint8)
        for pols in self.paises.values():
            for p in pols:
                q = np.stack([(p[:, 0] - self._mt0[0]) * res, (p[:, 1] - self._mt0[1]) * res], 1)
                cv2.fillPoly(m, [np.round(q).astype(np.int32)], 255)
        self._mt = m
        self._mt_res = res

    def es_tierra(self, lon, lat):
        """True donde hay tierra (según los polígonos de países), vectorizado."""
        self._mascara_tierra()
        i = np.clip(((np.asarray(lat) - self._mt0[1]) * self._mt_res).astype(int), 0, self._mt.shape[0] - 1)
        j = np.clip(((np.asarray(lon) - self._mt0[0]) * self._mt_res).astype(int), 0, self._mt.shape[1] - 1)
        return self._mt[i, j] > 0

    def picos(self):
        """Máximos locales (> 2000 m) de todas las ventanas: array [lon, lat, altitud] ordenado de mayor a menor."""
        self._cargar()
        if getattr(self, "_picos", None) is None:
            L = []
            for v in self.vent:
                a = v.pir[1]
                k = 5
                mx = cv2.dilate(a, np.ones((2 * k + 1, 2 * k + 1), np.uint8))
                ys, xs = np.nonzero((a >= mx) & (a > 2000))
                lat = v.lat0 + (ys * 2 + 0.5) * v.paso
                lon = v.lon0 + (xs * 2 + 0.5) * v.paso
                L.append(np.stack([lon, lat, a[ys, xs]], 1))
            p = np.concatenate(L)
            self._picos = p[np.argsort(-p[:, 2])]
        return self._picos

    # ------------------------------------------------------------------ geometría
    @staticmethod
    def proy(cam, lon, lat):
        lo, la, z = cam
        x, y = XY(lon, lat)
        x0, y0 = XY(lo, la)
        return 960 + (x - x0) * z, 540 + (y - y0) * z

    @staticmethod
    def inv(cam, sx, sy):
        lo, la, z = cam
        x0, y0 = XY(lo, la)
        X = x0 + (sx - 960) / z
        Y = y0 + (sy - 540) / z
        return X / (K * KX) - 101.0, 21.0 - Y / K

    def _poly_px(self, cam, p):
        x, y = self.proy(cam, p[:, 0], p[:, 1])
        return np.stack([x, y], 1)

    def _mascara(self, cam, polys):
        m = np.zeros((H, W), np.uint8)
        L = []
        for p in polys:
            q = self._poly_px(cam, p)
            if q[:, 0].max() < -50 or q[:, 0].min() > W + 50 or q[:, 1].max() < -50 or q[:, 1].min() > H + 50:
                continue
            L.append(np.round(q * 16).astype(np.int32))
        if L:
            cv2.fillPoly(m, L, 255, cv2.LINE_AA, 4)
        return m

    def _relieve_generico(self, cam):
        """Relieve de relleno (vecinos y vistas lejanas): ruido fractal anclado a lon/lat, a media resolución."""
        lo, la, z = cam
        lon = lo + (self.xx2 * 2 - 960) / (z * K * KX)
        lat = la - (self.yy2 * 2 - 540) / (z * K)
        r = cv2.remap(self._ruido, ((lon * 9.0) % 480).astype(np.float32), ((lat * 9.0) % 270).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
        return 600.0 + 420.0 * r

    # ------------------------------------------------------------------ base
    def base(self, cam, t=0.0, exag=7.0, mostrar_rios=True, rios_umbral=1.5, sombra=1.0, rio_color=None):
        """Fondo del mapa para la cámara cam = (lon, lat, z). float32 H x W x 3 en [0, 1]."""
        self._cargar()
        ppg = K * cam[2]
        nivel = int(np.clip(math.floor(math.log2(max(1.0, 60.0 / ppg))), 0, 3))
        lon_h = cam[0] + (self.xx2 * 2 - 960) / (cam[2] * K * KX)
        lat_h = cam[1] - (self.yy2 * 2 - 540) / (cam[2] * K)
        # ---- relieve de todas las ventanas que se ven (con mezcla suave en sus bordes)
        elev = np.full((HH, WH), -3000.0, np.float32)
        hum = np.full((HH, WH), 0.45, np.float32)
        w_dato = np.zeros((HH, WH), np.float32)
        for v in self.vent:
            if not v.toca(cam):
                continue
            A = v.afin_h(cam, nivel)
            e_i = cv2.warpAffine(v.pir[nivel], A, (WH, HH), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=NODATA)
            h_i = cv2.warpAffine(v.pir_h[nivel], A, (WH, HH), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
            d = np.minimum(np.minimum(lon_h - v.lon_min, v.lon_max - lon_h), np.minimum(lat_h - v.lat_min, v.lat_max - lat_h))
            w_i = np.clip(d / 3.0, 0.0, 1.0)
            w_i = w_i * w_i * (3 - 2 * w_i)
            mejor = (e_i > -7000) & (w_i > w_dato)
            elev = np.where(mejor, e_i, elev)
            hum = np.where(mejor, h_i, hum)
            w_dato = np.where(mejor, w_i, w_dato)
        m_mx = self._mascara(cam, self.vec_mx)
        m_ot = self._mascara(cam, self.vec_otros)
        tierra = np.maximum(m_mx, m_ot)
        tierra_h = cv2.resize(tierra, (WH, HH), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        mx_h = cv2.resize(m_mx, (WH, HH), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        lod = float(_suave_np(np.float32(cam[2]), 0.40, 0.22))     # 1 = vista lejana (Atlántico): el relieve de datos se funde con el genérico
        gen = self._relieve_generico(cam)
        hum_g, alt_g = _clima_global_rejilla(lon_h[0], lat_h[:, 0])     # la cámara no rota: lon solo varía en x, lat en y
        gen_g = np.maximum(120.0, gen * 0.75 + alt_g)
        # tierra que no es México: relieve real donde hay datos (EE. UU. del sur, Cuba, Iberia, Francia…) y genérico fuera de ellos (mezcla continua)
        vecino = (tierra_h > 0.5) & (mx_h < 0.5)
        elev = np.where(vecino, elev * w_dato + gen_g * (1 - w_dato), elev)
        hum = np.where(vecino, hum_g, hum)
        # el mar se funde hacia el azul profundo plano en los bordes de las ventanas de datos (sin costuras)
        elev = np.where(elev < 0, elev * w_dato + (-2600.0) * (1 - w_dato), elev)
        if lod > 0.0:
            elev = np.where(tierra_h > 0.5, elev * (1 - lod) + gen_g * lod, elev * (1 - lod) - 2600.0 * lod)
            hum = np.where(tierra_h > 0.5, hum * (1 - lod) + hum_g * lod, hum)
        elev_t = np.maximum(elev, 12.0)
        # ---- sombreado: del relieve suavizado a escala de pantalla (menos grumos)
        sig = max(1.6, 1.5 * ppg / 60.0 / 2.0)
        es = cv2.GaussianBlur(np.where(tierra_h > 0.5, elev_t, 0.0).astype(np.float32), (0, 0), sig)
        gx = cv2.Sobel(es, cv2.CV_32F, 1, 0, ksize=3) / 8.0
        gy = cv2.Sobel(es, cv2.CV_32F, 0, 1, ksize=3) / 8.0
        k = exag / (111320.0 / ppg * 2.0)
        sh = np.clip(0.5 - k * (gx * 0.70 + gy * 0.70), 0.0, 1.0)
        # ---- tierra
        ei = np.clip(elev_t / 10.0, 0, 599).astype(np.int32)
        seco = SECO[ei]
        col = seco + (HUMEDO[ei] - seco) * np.clip(hum, 0, 1)[..., None]
        osc = np.clip((0.5 - sh) * 2.0, 0, 1)[..., None] * sombra
        lit = np.clip((sh - 0.5) * 2.0, 0, 1)[..., None] * sombra
        col = col * (1 - 0.34 * osc) + _C_SOMBRA * (0.34 * osc)
        col = col * (1 - 0.20 * lit) + _C_LUZ * (0.20 * lit)
        gris = col.mean(-1, keepdims=True)
        mxk = mx_h[..., None]
        col = col * mxk + (col * 0.72 + gris * 0.28) * 0.90 * (1 - mxk)
        # ---- mar
        di = np.clip(-np.minimum(elev, -6.0) / 10.0, 0, 599).astype(np.int32)
        mar = FONDO_MAR[di]
        q4 = cv2.resize(tierra_h, (WH // 4, HH // 4), interpolation=cv2.INTER_AREA)
        gl = cv2.resize(cv2.GaussianBlur(q4, (0, 0), 1.5 + 2.5 * min(cam[2], 3.0) ** 0.5), (WH, HH), interpolation=cv2.INTER_LINEAR)
        mar = mar + (np.array([0.50, 0.84, 0.88], np.float32) - mar) * (gl[..., None] ** 1.6) * 0.40
        wx, wy = XY(lon_h, lat_h)                                     # coordenadas del mundo: el brillo del agua se mueve con el mapa, no con la pantalla
        ola = (0.5 + 0.5 * np.sin(wx * 0.030 + wy * 0.017 + t * 0.9) * np.sin(wy * 0.026 - t * 0.5)).astype(np.float32)   # XY da float64: sin esto TODO el mapa (y su posproceso) iba en float64
        mar = mar * (1 + 0.03 * (ola - 0.5))[..., None]
        th = tierra_h[..., None]
        img = cv2.resize(col * th + mar * (1 - th), (W, H), interpolation=cv2.INTER_LINEAR)
        # ---- lagos y ríos (a resolución completa, solo donde hay)
        self._agua(img, cam, ppg, mostrar_rios and cam[2] >= 0.36, rios_umbral, tierra, rio_color)
        # ---- orilla clara y fina
        orilla = cv2.GaussianBlur(tierra, (0, 0), 1.1)
        ys, xs = np.nonzero((orilla > 46) & (orilla < 209))
        if len(ys):
            b = np.clip(1 - np.abs(orilla[ys, xs].astype(np.float32) / 255.0 - 0.5) * 3.4, 0, 1)[:, None] * 0.50
            img[ys, xs] = img[ys, xs] + (_C_ORILLA - img[ys, xs]) * b
        return np.clip(img, 0, 1, out=img)

    # ------------------------------------------------------------------ lagos y ríos
    def _agua(self, img, cam, ppg, rios, extra, mex, rio_color):
        L = []
        for lg in self.lagos:
            q = self._poly_px(cam, lg["pts"])
            if q[:, 0].max() < -20 or q[:, 0].min() > W + 20 or q[:, 1].max() < -20 or q[:, 1].min() > H + 20:
                continue
            L.append(np.round(q * 16).astype(np.int32))
        if L:
            m = np.zeros((H, W), np.uint8)
            cv2.fillPoly(m, L, 255, cv2.LINE_AA, 4)
            ys, xs = np.nonzero(m)
            if len(ys):
                a = (m[ys, xs].astype(np.float32) / 255.0)[:, None]
                img[ys, xs] = img[ys, xs] * (1 - a) + np.array([0.30, 0.62, 0.86], np.float32) * a
        if not rios:
            return
        # umbral de flujo según el zoom: lejos solo los grandes (ln(1 + celdas acumuladas))
        umbral = float(np.interp(np.log(max(ppg, 1.0)), [np.log(40), np.log(120), np.log(300), np.log(700)], [6.4, 5.7, 5.0, 4.4])) + extra
        x, y = self.proy(cam, self.r_lon, self.r_lat)
        Q = np.round(np.stack([x, y], 1) * 16).astype(np.int32)
        ln = self.r_ln
        capa = np.zeros((H, W), np.uint8)
        gruesos = [[], [], []]
        for a, b in zip(self.r_cortes[:-1], self.r_cortes[1:]):
            l = ln[a:b]
            if l[-1] < umbral:                       # el flujo crece río abajo: si el final no llega al umbral, ningún punto llega
                continue
            ini = int(np.argmax(l >= umbral))
            seg = Q[a + ini:b]
            if len(seg) < 3 or seg[:, 0].max() < -320 or seg[:, 0].min() > (W + 20) * 16 or seg[:, 1].max() < -320 or seg[:, 1].min() > (H + 20) * 16:
                continue
            f = float(l[-1]) - umbral
            gruesos[0 if f < 0.9 else (1 if f < 1.9 else 2)].append(seg)
        esc = max(1.0, ppg / 100.0) ** 0.5
        for g, Lr in enumerate(gruesos):
            if Lr:
                cv2.polylines(capa, Lr, False, 255, max(1, int(round((1.6 + g * 1.1) * esc))), cv2.LINE_AA, 4)
        if mex is not None:
            capa = cv2.multiply(capa, mex, scale=1 / 255.0)
        ys, xs = np.nonzero(capa)
        if len(ys):
            a = (capa[ys, xs].astype(np.float32) / 255.0)[:, None] * 0.92
            img[ys, xs] = img[ys, xs] * (1 - a) + (np.asarray(rio_color, np.float32) / 255.0 if rio_color is not None else _C_AGUA) * a


MAPA = Mapa()
