# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Tequisquiapan» (Short VERTICAL 1080x1920; kit de historia_aguascalientes),
con RELIEVE REAL.

Una sola rejilla en proyección de MERCATOR, con la llave "mx" para no tocar el kit:
  - "mx": de Celaya a Tula/Zimapán y de la Ciudad de México al sur de San Luis Potosí (lon -101.05.. -98.85, lat 22.45.. 19.05;
    más ALTA que ancha, ≈ 0,6:1, para la pantalla vertical con un poco de margen de cámara a los lados), 700 px por grado
    (caja entera z ≈ 0,76; el estado de Querétaro entero z ≈ 1,0; Tequis-San Juan-Bernal z 2,5-4; el pueblo z 5-8).
    Bajo el guache: sombreado con AWS Terrain Tiles (Terrarium z10 ≈ 143 m, datos/relieve_qro_terrarium_z10.npz); ríos y presas
    con SRTM15+ (15", datos/relieve_qro_srtm15.nc, ERDDAP srtm15plus); valles verdes (San Juan del Río-Tequis, Querétaro, Bajío),
    presas (Zimapán inundada sobre el relieve; Solís y Tepuxtepec de Natural Earth) y red de ríos calculada del relieve (D8).
    Estados de Natural Earth 10 m. Para bajar el relieve: `python _bajar_relieve.py`.
Los campos se calculan una vez (`python mapa.py`) y se guardan en datos/campos_mx.npz (int16, 1/8 de px).
"""
import json
import math
import os

import cv2
import numpy as np

import boceto as B
from motor import H, W, clamp01, lerp, prog

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(AQUI)
RAIZ = os.path.dirname(VIDEOS)
F_LAND = os.path.join(AQUI, "datos", "ne_10m_land.geojson")
F_PAISES = os.path.join(AQUI, "datos", "estados_mx.geojson")
F_RIOS = os.path.join(AQUI, "datos", "ne_10m_rivers_lake_centerlines.geojson")
F_LAGOS = os.path.join(AQUI, "datos", "ne_10m_lakes.geojson")
F_NC = os.path.join(AQUI, "datos", "relieve_qro_srtm15.nc")   # ERDDAP srtm15plus, z[(18.95):(22.55)][(-101.15):(-98.75)]
F_FINO = os.path.join(AQUI, "datos", "relieve_qro_terrarium_z10.npz")  # AWS Terrain Tiles (Terrarium z10 ≈ 143 m), sombreado y valles
DATOS = os.path.join(AQUI, "datos")
ESC_I16 = 8.0                        # los campos se guardan en int16 con 1/8 px de resolución
LAT_MEDIA = 20.75                    # para pasar px a metros (pendientes)


# ------------------------------------------------------------------ proyección de Mercator
def ymerc(lat):
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.asarray(lat, float)) / 2)))


def inv_ymerc(y):
    return np.degrees(2 * np.arctan(np.exp(np.radians(np.asarray(y, float)))) - np.pi / 2)


def U(lon):
    return np.asarray(lon, float)


def desU(u):
    return np.asarray(u, float)


class Rej:
    def __init__(self, nombre, lon0, lon1, lat0, lat1, pxdeg, envuelve=False):
        self.nombre, self.lon0, self.lon1, self.lat0, self.lat1 = nombre, lon0, lon1, lat0, lat1
        self.pxdeg, self.envuelve = pxdeg, envuelve
        self.Y0 = float(ymerc(lat0))
        self.FW = int(round((lon1 - lon0) * pxdeg))
        self.FH = int(round((self.Y0 - float(ymerc(lat1))) * pxdeg))
        self.campos = {}
        self.aux = None              # (FH, FW, 3) float32: luz del relieve, altitud 0..1, profundidad 0..1
        self.rios = []
        self._cel = {}

    def nat(self, lon):
        return np.asarray(lon, float)

    def proj(self, lon, lat):
        return (np.asarray(lon, float) - self.lon0) * self.pxdeg, (self.Y0 - ymerc(lat)) * self.pxdeg

    def proj_pts(self, P):
        P = np.asarray(P, float)
        x, y = self.proj(P[:, 0], P[:, 1])
        return np.stack([x, y], 1)

    def inv(self, x, y):
        return self.lon0 + np.asarray(x, float) / self.pxdeg, inv_ymerc(self.Y0 - np.asarray(y, float) / self.pxdeg)


REJ = {"mx": Rej("mx", -101.05, -98.85, 22.45, 19.05, 700.0)}   # llave "mx" para no tocar el kit; es Querétaro y su entorno
PXDEG_REF = REJ["mx"].pxdeg

# ------------------------------------------------------------------ paleta de guache (papel cálido, sierra ocre, valle verde, presas azules)
MAR = (168, 204, 212)
MAR_HONDO = (124, 168, 194)
MAR_CL = (204, 228, 224)
TIERRA = (236, 220, 184)
TIERRA_ALTA = (202, 174, 132)
TIERRA_CUMBRE = (236, 230, 216)
RIO = (88, 148, 196)
VALLE = (144, 180, 110)
AGUA_LAGO = (128, 184, 212)
# Querétaro va de los cañones de la Sierra Gorda (Jalpan ≈ 760 m, Moctezuma ≈ 300 m) al altiplano (1 800-2 000 m: Tequis 1 880,
# San Juan 1 920) y a las cumbres (El Gallo ≈ 3 100 m; Nevado de Toluca 4 680 m en el borde sur): la escala empieza en ALT_BASE
# (cañones = tierra baja, altiplano = medio, sierras ocre, > ~2 900 m casi blanco). En Ags era 1 500..3 000 m.
ALT_BASE, ALT_RANGO = 1150.0, 2400.0

COL = {
    # estados (Querétaro protagonista, vecinos más apagados)
    "edo_queretaro": (204, 92, 66),
    "queretaro_edo": (204, 92, 66),
    "territorio": (204, 72, 58),
    "edo_guanajuato": (98, 134, 184),
    "edo_hidalgo": (110, 150, 96),
    "edo_mexico": (214, 168, 80),
    "edo_cdmx": (196, 110, 120),
    "edo_san_luis_potosi": (150, 96, 150),
    "edo_slp": (150, 96, 150),
    "edo_michoacan": (176, 132, 80),
    "resto_mx": (196, 168, 120),
    "mexico_mod": (78, 148, 96),
    # municipio y pueblo
    "municipio_tequis": (214, 120, 64),
    "mancha_tequis": (210, 110, 70),
    "metro": (210, 110, 70),
    # regiones naturales
    "sierra_gorda": (110, 150, 96),
    "semidesierto": (214, 168, 80),
    "valle": VALLE,
    # pueblos originarios
    "otomies": (98, 134, 184),
    "chichimecas": (196, 120, 62),
    "pames": (226, 170, 60),
    "jonaces": (176, 132, 80),
    "purepechas": (150, 96, 150),
    "mexicas": (110, 150, 96),
    # colonia y siglo XIX
    "nueva_espana": (196, 168, 120),
    "insurgentes": (74, 146, 98),
    "realistas": (78, 112, 174),
    "federacion": (98, 150, 104),
    "liberales": (74, 138, 104),
    "conservadores": (150, 94, 158),
    "imperio": (150, 94, 158),
    "republica": (74, 138, 104),
    # siglo XX
    "porfiriato": (196, 146, 68),
    "revolucion": (198, 70, 60),
    "constitucionalistas": (198, 70, 60),
    "cristeros": (198, 70, 60),
    # agua
    "presas": AGUA_LAGO,
    "presa_zimapan": AGUA_LAGO,
    "presa_centenario": AGUA_LAGO,
}
COL_ESTADOS = {
    "Querétaro": (204, 92, 66), "Guanajuato": (98, 134, 184), "Hidalgo": (110, 150, 96), "México": (214, 168, 80),
    "San Luis Potosí": (150, 96, 150), "Michoacán": (176, 132, 80), "Distrito Federal": (196, 110, 120),
}
COL_CELDAS = [
    (214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
    (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110),
    (190, 140, 70), (120, 150, 190), (214, 100, 90), (98, 160, 120),
]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat); «aprox.» = sitio sin coordenada fiable
CIUDADES = {
    # el pueblo
    "tequisquiapan": (-99.8925, 20.5210), "plaza_tequis": (-99.8920, 20.5206),     # jardín Hidalgo y parroquia de Santa María
    "centro_geografico": (-99.8880, 20.5185),         # aprox. (monumento al centro geográfico de México, 1916, en el pueblo)
    "presa_centenario": (-99.9060, 20.4975),          # centro del embalse (INEGI 1:250 000), al SO del pueblo, sobre el río San Juan
    "bordo_blanco": (-99.9188, 20.4911), "san_nicolas": (-99.9369, 20.4745), "la_fuente": (-100.0350, 20.5511),
    "fuentezuelas": (-99.9815, 20.5547),              # localidades del municipio (INEGI)
    "rio_san_juan": (-99.8600, 20.5300),              # punto para rotular el río (entra por la presa Centenario y sigue al E/NE)
    # la zona
    "san_juan_rio": (-99.9958, 20.3886), "ezequiel_montes": (-99.8991, 20.6652), "bernal": (-99.9406, 20.7400),
    "pena_bernal": (-99.9461, 20.7481),               # la roca (cumbre 2 515 m; en el relieve de 143 m sale como un bulto de ≈ 2 290 m)
    "cadereyta": (-99.8167, 20.6942), "colon": (-100.0475, 20.7792), "pedro_escobedo": (-100.1406, 20.5011),
    # resto del estado
    "queretaro": (-100.3899, 20.5888), "corregidora": (-100.4436, 20.5375), "la_canada": (-100.3197, 20.6075),
    "cerro_campanas": (-100.4035, 20.5930), "huimilpan": (-100.2747, 20.3725), "amealco": (-100.1442, 20.1878),
    "toliman": (-99.9314, 20.9047), "penamiller": (-99.8150, 21.0533), "san_joaquin": (-99.5664, 20.9153),
    "pinal_amoles": (-99.6258, 21.1347), "jalpan": (-99.4733, 21.2172), "landa": (-99.3197, 21.1847),
    "arroyo_seco": (-99.6878, 21.5472), "sierra_gorda": (-99.5000, 21.1000), "semidesierto": (-99.8600, 20.9300),
    "presa_zimapan": (-99.5200, 20.6550),             # sobre el embalse (cortina ≈ -99.50, 20.66)
    # vecinos
    "celaya": (-100.8157, 20.5233), "apaseo": (-100.6170, 20.5450), "san_miguel_allende": (-100.7436, 20.9144),
    "huichapan": (-99.6500, 20.3756), "tula": (-99.3428, 20.0539), "zimapan": (-99.3800, 20.7380),
    "ixmiquilpan": (-99.2186, 20.4847), "aculco": (-99.8300, 20.1000), "polotitlan": (-99.8150, 20.2250),
    "jilotepec": (-99.5330, 19.9530), "toluca": (-99.6557, 19.2826), "acambaro": (-100.7220, 20.0310),
    "rio_verde": (-99.9940, 21.9300), "xichu": (-100.0570, 21.3000),
    # la capital del país cabe en la caja (abajo a la derecha): «mexico» es la posición real; «mexico_borde» = punto en el borde SE
    # en la dirección real desde Tequis (para una flecha que salga de cuadro en encuadres cerrados)
    "mexico": (-99.1332, 19.4326), "mexico_real": (-99.1332, 19.4326), "mexico_borde": (-98.92, 19.20),
    "ciudad_mexico": (-99.1332, 19.4326),
}

RUTAS_COMPLETAS = {        # trazado real (aprox.); RUTAS = estas mismas recortadas a la caja
    # Camino Real de Tierra Adentro: México → Cuautitlán → Huehuetoca → Tepeji → Arroyo Zarco (Aculco) → San Juan del Río →
    # Querétaro → Apaseo → Celaya → (Salamanca, fuera de la caja)
    "camino_real": [(-99.133, 19.433), (-99.18, 19.67), (-99.20, 19.83), (-99.34, 19.91), (-99.55, 20.00), (-99.78, 20.08),
                    (-99.87, 20.20), (-99.94, 20.31), (-99.996, 20.389), (-100.08, 20.45), (-100.18, 20.52), (-100.30, 20.57),
                    (-100.39, 20.589), (-100.50, 20.56), (-100.617, 20.545), (-100.816, 20.523), (-101.19, 20.57)],
    # vía México → Querétaro: Huehuetoca → Tula → Nopala → entra de Hidalgo, pasa al SUR de Tequisquiapan y por San Nicolás
    # (este tramo, del mapa municipal de INEGI 1:250 000) → San Juan del Río → Pedro Escobedo → Querétaro → Celaya.
    # Fuera del municipio la traza es aproximada.
    "tren": [(-99.133, 19.433), (-99.20, 19.83), (-99.343, 20.054), (-99.50, 20.20), (-99.64, 20.30), (-99.76, 20.44),
             (-99.8304, 20.5142), (-99.837, 20.5174), (-99.8424, 20.530), (-99.8469, 20.5301), (-99.8503, 20.5238),
             (-99.8516, 20.5113), (-99.8628, 20.5093), (-99.8785, 20.4996), (-99.8965, 20.4919), (-99.9033, 20.4825),
             (-99.919, 20.4785), (-99.9369, 20.4745), (-99.9482, 20.4662), (-99.9539, 20.4548), (-99.975, 20.42),
             (-99.996, 20.389), (-100.06, 20.44), (-100.141, 20.501), (-100.30, 20.565), (-100.39, 20.595), (-100.62, 20.55),
             (-100.816, 20.523), (-101.19, 20.57)],
}
RUTAS_FIJAS = {
    # ruta para visitar: San Juan del Río → Tequisquiapan → Ezequiel Montes → Peña de Bernal
    "ruta_turista": [(-99.9958, 20.3886), (-99.97, 20.42), (-99.935, 20.465), (-99.8920, 20.5206), (-99.895, 20.575),
                     (-99.905, 20.625), (-99.8991, 20.6652), (-99.920, 20.705), (-99.9403, 20.7406)],
    # solo Tequis → San Juan del Río (carretera 120, al SO)
    "tequis_sjr": [(-99.8920, 20.5206), (-99.935, 20.465), (-99.97, 20.42), (-99.9958, 20.3886)],
    # solo Tequis → Ezequiel Montes → Bernal
    "tequis_bernal": [(-99.8920, 20.5206), (-99.895, 20.575), (-99.905, 20.625), (-99.8991, 20.6652), (-99.920, 20.705),
                      (-99.9403, 20.7406)],
    # Ruta del Arte, Queso y Vino: San Juan del Río → Tequis → Ezequiel Montes → Cadereyta / Bernal → Colón
    "ruta_queso_vino": [(-99.9958, 20.3886), (-99.935, 20.465), (-99.8920, 20.5206), (-99.895, 20.575), (-99.8991, 20.6652),
                        (-99.8167, 20.6942), (-99.8991, 20.6652), (-99.9403, 20.7406), (-99.99, 20.765), (-100.0475, 20.7792)],
    # a la Sierra Gorda: Ezequiel Montes → Cadereyta → Vizarrón → Pinal de Amoles → Jalpan (carretera 120)
    "ruta_sierra": [(-99.8991, 20.6652), (-99.8167, 20.6942), (-99.72, 20.83), (-99.66, 20.95), (-99.6258, 21.1347),
                    (-99.55, 21.20), (-99.4733, 21.2172)],
}

CELDAS_SEMILLAS = {
    # centros APROXIMADOS de los 18 municipios de Querétaro (sin geometría oficial: celdas de Voronoi, se recortan al estado)
    # orden: Querétaro, Corregidora, El Marqués, Huimilpan, Pedro Escobedo, Amealco, San Juan del Río, Tequisquiapan, Ezequiel
    # Montes, Colón, Tolimán, Cadereyta, Peñamiller, San Joaquín, Pinal de Amoles, Jalpan, Landa, Arroyo Seco
    "municipios": [(-100.42, 20.72), (-100.44, 20.50), (-100.22, 20.68), (-100.27, 20.35), (-100.13, 20.48), (-100.10, 20.17),
                   (-99.98, 20.36), (-99.89, 20.53), (-99.93, 20.66), (-100.03, 20.80), (-99.93, 20.93), (-99.68, 20.75),
                   (-99.83, 21.06), (-99.57, 20.94), (-99.62, 21.14), (-99.47, 21.30), (-99.20, 21.18), (-99.65, 21.50)],
    # las 4 regiones del estado: Sierra Gorda, Semidesierto, Valles (Querétaro-San Juan), Sur (Amealco-Huimilpan)
    "regiones": [(-99.45, 21.25), (-99.85, 20.88), (-100.15, 20.55), (-100.15, 20.20)],
    "pueblos": [(-100.60, 21.80), (-99.40, 21.90), (-100.70, 20.30), (-99.20, 20.20), (-99.90, 19.60), (-99.90, 20.60)],
}
CELDAS_PAISES = {}

# ------------------------------------------------------------------ polígonos (lon, lat), aproximados (el contorno se tiembla a mano)
# valles fértiles: dentro de estos contornos holgados, el verde va donde el relieve es fondo de valle (`_valle_dem`)
VALLE_VERDE = [  # valle de San Juan del Río y Tequisquiapan (río San Juan), de Polotitlán a Ezequiel Montes
    (-100.10, 20.30), (-99.95, 20.22), (-99.82, 20.30), (-99.80, 20.50), (-99.85, 20.62), (-99.95, 20.62), (-100.05, 20.50),
]
VALLE_QRO = [(-100.55, 20.48), (-100.30, 20.45), (-100.12, 20.52), (-100.20, 20.70), (-100.45, 20.70)]   # valle de Querétaro
VALLE_BAJIO = [(-101.10, 20.40), (-100.60, 20.42), (-100.55, 20.65), (-101.10, 20.70)]                  # Bajío (Celaya)
VALLE_REL, VALLE_PEND = 45.0, 0.06         # m sobre el fondo local (radio ≈ 4 km) y pendiente máxima
# pueblos originarios hacia 1500-1550 (zonas aproximadas): otomíes en el sur y centro (Jilotepec, Huichapan, San Juan, Tequis,
# Querétaro, Amealco); chichimecas en el norte: pames en la Sierra Gorda y jonaces en el semidesierto
OTOMIES = [(-100.55, 20.40), (-100.45, 20.78), (-100.05, 20.86), (-99.70, 20.82), (-99.25, 20.70), (-99.15, 20.30),
           (-99.30, 19.85), (-99.75, 19.75), (-100.25, 19.95)]
PAMES = [(-100.20, 22.50), (-98.80, 22.50), (-98.80, 21.10), (-99.40, 20.95), (-99.75, 21.15), (-100.20, 21.40)]
JONACES = [(-100.20, 21.40), (-99.75, 21.15), (-99.40, 20.95), (-99.70, 20.82), (-100.05, 20.86), (-100.30, 21.00)]
AMP_PUEBLOS = 0.05           # temblor común de los territorios de los pueblos (sus rayas compartidas coinciden)
CHICHIMECAS_NORTE = [(-101.10, 22.50), (-100.20, 22.50), (-100.20, 21.40), (-100.30, 21.00), (-100.45, 20.78), (-101.10, 20.70)]
PUREPECHAS = [(-101.10, 20.40), (-100.55, 20.40), (-100.25, 19.95), (-100.30, 19.00), (-101.10, 19.00)]
MEXICAS = [(-99.75, 19.75), (-99.30, 19.85), (-98.80, 19.95), (-98.80, 19.00), (-99.90, 19.00)]
SIERRA_GORDA = [(-99.90, 21.10), (-99.75, 21.40), (-99.60, 21.70), (-99.10, 21.65), (-98.95, 21.35), (-99.15, 21.00),
                (-99.45, 20.85), (-99.70, 20.90)]
SEMIDESIERTO = [(-100.12, 20.82), (-100.00, 21.10), (-99.85, 21.15), (-99.70, 20.92), (-99.62, 20.78), (-99.78, 20.68),
                (-99.98, 20.68)]
# municipio de Tequisquiapan: contorno digitalizado del «Compendio de información geográfica municipal 2010» de INEGI (marco
# geoestadístico 2010, georreferenciado con sus 4 cruces de 100°05'/99°50' y 20°39'/20°26'); ≈ 374 km² (INEGI: 3,16 % del estado)
MUNICIPIO_TEQUIS = [
    (-100.0794, 20.6417), (-100.0041, 20.6520), (-100.0026, 20.6371), (-99.9914, 20.6355), (-99.9890, 20.6512), (-99.9700, 20.6531),
    (-99.9683, 20.6493), (-99.9658, 20.6358), (-99.9480, 20.6350), (-99.9463, 20.6245), (-99.9381, 20.6192), (-99.9325, 20.6264),
    (-99.9285, 20.6253), (-99.9279, 20.6306), (-99.9179, 20.6315), (-99.9125, 20.6220), (-99.8998, 20.6030), (-99.8938, 20.6015),
    (-99.8959, 20.5830), (-99.8896, 20.5861), (-99.8816, 20.5959), (-99.8739, 20.5901), (-99.8561, 20.5893), (-99.8495, 20.5836),
    (-99.8440, 20.5724), (-99.8519, 20.5716), (-99.8597, 20.5667), (-99.8686, 20.5676), (-99.8710, 20.5587), (-99.8600, 20.5516),
    (-99.8506, 20.5521), (-99.8516, 20.5448), (-99.8579, 20.5424), (-99.8467, 20.5437), (-99.8271, 20.5424), (-99.8343, 20.4779),
    (-99.8455, 20.4735), (-99.8522, 20.4672), (-99.8591, 20.4589), (-99.8724, 20.4643), (-99.8847, 20.4613), (-99.8946, 20.4667),
    (-99.9103, 20.4637), (-99.9128, 20.4449), (-99.9240, 20.4429), (-99.9375, 20.4315), (-99.9474, 20.4390), (-99.9539, 20.4579),
    (-99.9674, 20.4497), (-99.9638, 20.4633), (-99.9604, 20.4695), (-99.9659, 20.4748), (-99.9712, 20.4917), (-99.9967, 20.4993),
    (-99.9876, 20.5170), (-99.9950, 20.5150), (-100.0074, 20.5350), (-100.0152, 20.5351), (-100.0325, 20.5238), (-100.0345, 20.5437),
    (-100.0669, 20.5399), (-100.0576, 20.5325), (-100.0644, 20.5237), (-100.0709, 20.5351), (-100.0849, 20.5391), (-100.0772, 20.5620),
    (-100.0748, 20.5763), (-100.0652, 20.5745), (-100.0641, 20.6195), (-100.0775, 20.6239)]
MANCHA_TEQUIS = [  # zona urbana de la cabecera (INEGI 2010)
    (-99.9111, 20.5283), (-99.9004, 20.5290), (-99.8958, 20.5380), (-99.8902, 20.5442), (-99.8877, 20.5599), (-99.8855, 20.5609),
    (-99.8804, 20.5556), (-99.8825, 20.5378), (-99.8769, 20.5346), (-99.8737, 20.5241), (-99.8750, 20.5157), (-99.8806, 20.5084),
    (-99.8840, 20.5064), (-99.8907, 20.5075), (-99.8962, 20.5118), (-99.9006, 20.5139), (-99.9051, 20.5129), (-99.9106, 20.5193)]
PRESA_CENTENARIO = [  # cuerpo de agua al SO del pueblo (INEGI 2010), ≈ 3,8 km de largo
    (-99.8951, 20.5124), (-99.8963, 20.5055), (-99.9008, 20.5003), (-99.9042, 20.4972), (-99.9054, 20.4909), (-99.9088, 20.4878),
    (-99.9156, 20.4837), (-99.9189, 20.4848), (-99.9110, 20.4931), (-99.9098, 20.4993), (-99.9053, 20.5024), (-99.8985, 20.5076)]
METRO = [(-100.48, 20.53), (-100.42, 20.50), (-100.33, 20.55), (-100.30, 20.62), (-100.36, 20.68), (-100.45, 20.66),
         (-100.49, 20.60)]                                                      # zona metropolitana de Querétaro (aprox.)
INSURGENTES = [(-101.10, 20.40), (-100.30, 20.40), (-100.00, 20.80), (-100.50, 21.10), (-101.10, 21.10)]   # Bajío de 1810

# Ríos: Natural Earth 10 m trae el Lerma, el Moctezuma y el Verde, gruesos y sin el San Juan → la red de ríos sale del propio
# relieve SRTM15+ (`_rios_dem`: relleno de depresiones + D8 + acumulación; San Juan-Tequisquiapan, Moctezuma, Santa María,
# Extoraz, Tula, Lerma, Laja, Querétaro...).
RIOS_EXTRA = []
# Los ríos se calculan sobre el Terrarium remuestreado a una rejilla lon/lat de RIO_PASO (7,5" ≈ 230 m): con las celdas de 15" del
# SRTM15+ el cañón del San Juan (Tequis → Zimapán) quedaba tapado y el río salía hacia Ezequiel Montes.
RIO_PASO = 1.0 / 480.0
RIO_SUMIDERO, RIO_SUM_AREA = 10.0, 1600  # depresión de ≥ 10 m y ≥ 1 600 celdas (≈ 80 km²) = cuenca cerrada (las chicas son ruido)
RIO_A0 = 1040                # celdas de 7,5" (≈ 0,05 km² c/u) que drenan a un punto para que haya río (≈ 50 km²)
RIO_SUMIDERO_MAX = 30.0      # ...pero solo si es SOMERA: los cañones (San Juan, Moctezuma, Santa María) son más angostos que la celda
                             # de 15" y el relleno los ve como «cuencas» de 50-300 m de hondo; esas NO son sumidero (el río sigue)
# Presas: Zimapán (1993, en el cañón del San Juan + Tula) = relieve Terrarium inundado hasta la superficie del agua que vio el SRTM
# (≈ 1 565-1 570 m) desde una semilla, dentro de una caja; Centenario = polígono de INEGI; Solís y Tepuxtepec (Lerma) = Natural Earth.
PRESAS = {"presa_zimapan": ((-99.5251, 20.6598), 1570.0, (-99.80, -99.44, 20.45, 20.70))}


def _recortar(pts, rej, paso=0.01):
    """Recorta una ruta a la caja de la rejilla: se queda con el tramo continuo más largo dentro (puntos originales + extremos)."""
    P = np.asarray(pts, float)
    m = 0.02

    def dentro(q):
        return rej.lon0 + m < q[0] < rej.lon1 - m and rej.lat1 + m < q[1] < rej.lat0 - m

    tramos, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / paso))
        for k in range(n + 1):
            q = a + (b - a) * k / n
            if dentro(q):
                if k == n:
                    cur.append(("o", tuple(b)))
                elif not cur:
                    cur.append(("c", tuple(q)))
            elif cur:
                cur.append(("c", tuple(a + (b - a) * (k - 1) / n)))
                tramos.append(cur)
                cur = []
                break
    if cur:
        tramos.append(cur)
    T = max(tramos, key=len)
    return [(round(float(p[0]), 4), round(float(p[1]), 4)) for _, p in T]


RUTAS = {k: _recortar(v, REJ["mx"]) for k, v in RUTAS_COMPLETAS.items()}
RUTAS.update(RUTAS_FIJAS)


# ------------------------------------------------------------------ rasterización
def _anillos(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    return geom["coordinates"]


def _mask_geoms(rej, geoms):
    m = np.zeros((rej.FH, rej.FW), np.uint8)
    for g in geoms:
        for poly in _anillos(g):
            I = []
            for r in poly:
                P = np.asarray(r, float)
                x = (P[:, 0] - rej.lon0) * rej.pxdeg
                if x.max() < -50 or x.min() > rej.FW + 50:
                    continue
                y = (rej.Y0 - ymerc(np.clip(P[:, 1], -85, 85))) * rej.pxdeg
                I.append(np.rint(np.stack([x, y], 1) * 4).astype(np.int32).reshape(-1, 1, 2))
            if I:
                cv2.fillPoly(m, I, 255, cv2.LINE_8, 2)
    return m


def _mano(pts, paso=0.04, amp=0.10):
    P = np.asarray(pts, float)
    P = np.vstack([P, P[:1]])
    out = []
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / paso))
        for k in range(n):
            out.append(a + (b - a) * k / n)
    Q = np.array(out)
    lo, la = Q[:, 0], Q[:, 1]
    dx = (np.sin(lo * 2.3 + la * 1.7 + 0.4) * 0.6 + np.sin(lo * 5.1 - la * 4.3 + 1.9) * 0.3 + np.sin(lo * 11.0 + la * 9.0) * 0.12)
    dy = (np.sin(la * 2.1 - lo * 1.9 + 2.2) * 0.6 + np.sin(la * 4.7 + lo * 5.3 + 0.7) * 0.3 + np.sin(la * 10.0 - lo * 12.0) * 0.12)
    return np.stack([lo + amp * dx, la + amp * dy], 1)


def _mask_poli(rej, pts, mano=True, amp=None):
    m = np.zeros((rej.FH, rej.FW), np.uint8)
    Q = np.asarray(pts, float)
    ext = float(max(np.ptp(Q[:, 0]), np.ptp(Q[:, 1])))
    if amp is None:                                 # el temblor a mano, proporcional al tamaño (la mancha urbana no se deforma);
        amp = min(0.10, max(0.006, 0.05 * ext))     # con el MISMO amp, dos polígonos vecinos tiemblan igual en su raya común
    P = rej.proj_pts(_mano(pts, paso=amp * 0.4, amp=amp) if mano else pts)
    cv2.fillPoly(m, [np.rint(P * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
    return m


def _sdf(m):
    b = (m > 127).astype(np.uint8)
    if b.max() == 0:
        return np.full(m.shape, 4000.0, np.float32)
    din = cv2.distanceTransform(b, cv2.DIST_L2, 5)
    dout = cv2.distanceTransform(1 - b, cv2.DIST_L2, 5)
    return cv2.GaussianBlur((dout - din).astype(np.float32), (0, 0), 1.3)


def _i16(s):
    return np.clip(np.rint(s * ESC_I16), -32000, 32000).astype(np.int16)


_PAISES = None
_RIOS = None
RIOS_SI = {}                 # los ríos de Natural Earth aquí son gruesos (ver _rios_dem); se deja el mecanismo por subcadena
ESTADOS = ("Querétaro", "Guanajuato", "Hidalgo", "México", "San Luis Potosí", "Michoacán", "Distrito Federal")
CLAVE_EDO = {"Distrito Federal": "edo_cdmx"}


def _nombre(f):
    n = f["properties"].get("name") or ""
    return n.encode("latin-1", "ignore").decode("utf-8", "ignore") if "Ã" in n else n


def _clave(n):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", n) if unicodedata.category(c) != "Mn")
    return s.lower().replace(" ", "_")


def _estados(nombres):
    ks = {_clave(n) for n in nombres}
    return [f["geometry"] for f in _PAISES["features"] if _clave(_nombre(f)) in ks]


# ------------------------------------------------------------------ relieve SRTM15+ (rejilla del DEM → rejilla del mapa)
_DEM = None


def _dem():
    """(z, lat, lon) del relieve, lat y lon crecientes."""
    global _DEM
    if _DEM is None:
        from scipy.io import netcdf_file
        f = netcdf_file(F_NC, "r", mmap=False)
        var = "z" if "z" in f.variables else "altitude"
        z = f.variables[var][:].astype(np.float32).copy()
        lat_ = f.variables["latitude"][:].astype(np.float64).copy()
        lon_ = f.variables["longitude"][:].astype(np.float64).copy()
        if lat_[0] > lat_[-1]:
            z, lat_ = z[::-1].copy(), lat_[::-1].copy()
        _DEM = (z, lat_, lon_)
    return _DEM


def _a_rejilla(rej, arr, interp=cv2.INTER_LINEAR):
    """Lleva un arreglo en la rejilla del DEM a la rejilla del mapa (Mercator)."""
    _, lat_, lon_ = _dem()
    paso = float(lat_[1] - lat_[0])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float32)
    lon, lat = rej.inv(xs, ys)
    mi = ((lat - lat_[0]) / paso).astype(np.float32)
    mj = ((lon - lon_[0]) / float(lon_[1] - lon_[0])).astype(np.float32)
    return cv2.remap(arr.astype(np.float32), mj, mi, interp, borderMode=cv2.BORDER_REPLICATE)


def _alt_fina(rej):
    """Altitud en la rejilla del mapa desde el mosaico Terrarium z10 (Web Mercator, ≈ 143 m); si no está, la de SRTM15+."""
    if not os.path.exists(F_FINO):
        return _a_rejilla(rej, _dem()[0])
    d = np.load(F_FINO)
    return _fina_a_rejilla(rej, d["z"], d)


def _presa_fina(semilla, nivel, caja):
    """Máscara (mosaico Terrarium, 0/1) de una presa: lo conexo a la semilla que queda bajo `nivel` m, dentro de la caja."""
    d = np.load(F_FINO)
    z = d["z"]
    n = 256.0 * 2 ** int(d["zoom"])

    def px(lon, lat):
        return (int((lon + 180.0) / 360.0 * n - 256 * int(d["x0"])),
                int((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n - 256 * int(d["y0"])))
    a, b, c, e = caja
    xa, ya = px(a, e)
    xb, yb = px(b, c)
    sx, sy = px(*semilla)
    sub = z[ya:yb + 1, xa:xb + 1]
    _, lab = cv2.connectedComponents((sub <= nivel).astype(np.uint8), connectivity=4)
    m = np.zeros(z.shape, np.float32)
    m[ya:yb + 1, xa:xb + 1] = lab == lab[sy - ya, sx - xa]
    return m


def _fina_a_rejilla(rej, arr, d=None):
    """Lleva un arreglo del mosaico Terrarium (Web Mercator) a la rejilla del mapa."""
    d = np.load(F_FINO) if d is None else d
    n = 256.0 * 2 ** int(d["zoom"])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float64)
    lon = rej.lon0 + xs / rej.pxdeg
    ym = np.radians(rej.Y0 - ys / rej.pxdeg)                     # Mercator en radianes (rej usa grados)
    mx = ((lon + 180.0) / 360.0 * n - 256.0 * int(d["x0"])).astype(np.float32)
    my = ((1.0 - ym / math.pi) / 2.0 * n - 256.0 * int(d["y0"])).astype(np.float32)
    return cv2.remap(arr.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def _valle_dem(rej):
    """Fondos de valle (0/255): poca altura sobre el fondo local y poca pendiente, con bordes suaves."""
    e = cv2.GaussianBlur(_alt_fina(rej), (0, 0), 2.0)
    r = 25
    fondo = cv2.GaussianBlur(cv2.erode(e, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))), (0, 0), 8)
    px_m = 111320.0 * math.cos(math.radians(LAT_MEDIA)) / rej.pxdeg
    pend = np.hypot(cv2.Sobel(e, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(e, cv2.CV_32F, 0, 1, ksize=3)) / 8.0 / px_m
    v = ((e - fondo) < VALLE_REL) & (pend < VALLE_PEND)
    v = cv2.morphologyEx(v.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    v = cv2.morphologyEx(v, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return ((cv2.GaussianBlur(v.astype(np.float32), (0, 0), 3.0)) > 127).astype(np.uint8) * 255


def _dem_rios():
    """(z, lat, lon) para los ríos: el mosaico Terrarium llevado a una rejilla lon/lat regular de RIO_PASO (si no está, SRTM15+)."""
    if not os.path.exists(F_FINO):
        return _dem()
    d = np.load(F_FINO)
    z = d["z"]
    n = 256.0 * 2 ** int(d["zoom"])
    r = REJ["mx"]
    lat_ = np.arange(r.lat1 - 0.03, r.lat0 + 0.03, RIO_PASO)
    lon_ = np.arange(r.lon0 - 0.03, r.lon1 + 0.03, RIO_PASO)
    mx = ((lon_ + 180.0) / 360.0 * n - 256.0 * int(d["x0"])).astype(np.float32)
    my = ((1.0 - np.arcsinh(np.tan(np.radians(lat_))) / math.pi) / 2.0 * n - 256.0 * int(d["y0"])).astype(np.float32)
    MX, MY = np.meshgrid(mx, my)
    zz = cv2.remap(cv2.GaussianBlur(np.maximum(z, 0.0), (0, 0), 0.6), MX, MY, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return zz.astype(np.float32), lat_, lon_


def _rios_dem():
    """Red de ríos a partir del relieve: relleno de depresiones (priority-flood), D8 y acumulación de flujo.
    Devuelve [(puntos lon/lat, peso)]; el peso (6,9..9,6) crece con el log del área que drena."""
    import heapq
    z, lat_, lon_ = _dem_rios()
    ny, nx = z.shape
    f = z.astype(np.float64).copy()
    hecho = np.zeros((ny, nx), bool)
    heap = []
    for i in range(ny):
        for j in (0, nx - 1):
            heap.append((f[i, j], i, j))
            hecho[i, j] = True
    for j in range(1, nx - 1):
        for i in (0, ny - 1):
            heap.append((f[i, j], i, j))
            hecho[i, j] = True
    heapq.heapify(heap)
    vec = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while heap:
        e, i, j = heapq.heappop(heap)
        for di, dj in vec:
            a, b = i + di, j + dj
            if 0 <= a < ny and 0 <= b < nx and not hecho[a, b]:
                hecho[a, b] = True
                if f[a, b] <= e:
                    f[a, b] = e + 1e-3
                heapq.heappush(heap, (f[a, b], a, b))
    cx = math.cos(math.radians(float(lat_.mean())))
    P = np.pad(f, 1, mode="edge")
    best = np.zeros((ny, nx))
    dirn = np.full((ny, nx), -1, np.int64)
    for k, (di, dj) in enumerate(vec):
        dist = math.hypot(di, dj * cx)
        s = (f - P[1 + di:1 + di + ny, 1 + dj:1 + dj + nx]) / dist
        m = s > best
        best[m] = s[m]
        dirn[m] = k
    ii, jj = np.mgrid[0:ny, 0:nx]
    off_i = np.array([v[0] for v in vec])
    off_j = np.array([v[1] for v in vec])
    di_ = np.where(dirn >= 0, off_i[np.maximum(dirn, 0)], 0)
    dj_ = np.where(dirn >= 0, off_j[np.maximum(dirn, 0)], 0)
    abajo = np.where(dirn >= 0, (ii + di_) * nx + (jj + dj_), -1).ravel()
    borde = np.zeros((ny, nx), bool)
    borde[0, :] = borde[-1, :] = borde[:, 0] = borde[:, -1] = True
    abajo[borde.ravel()] = -1
    # cuencas cerradas (llanos de Ojuelos, altiplano potosino): una depresión rellenada más de RIO_SUMIDERO m es un sumidero; si no,
    # el relleno inventa ríos rectos que cruzan los llanos hasta el borde
    n, lab, st, _ = cv2.connectedComponentsWithStats(((f - z) > 1.0).astype(np.uint8), connectivity=8)
    hondo = np.zeros(n)
    np.maximum.at(hondo, lab.ravel(), (f - z).ravel())
    grande = (st[:, cv2.CC_STAT_AREA] >= RIO_SUM_AREA) & (hondo >= RIO_SUMIDERO) & (hondo <= RIO_SUMIDERO_MAX)
    grande[0] = False
    sumidero = grande[lab].ravel()
    abajo[sumidero] = -1
    orden = np.argsort(-f.ravel(), kind="stable")
    acc = np.ones(ny * nx)
    for k in orden:
        d = abajo[k]
        if d >= 0:
            acc[d] += acc[k]
    canal = (acc >= RIO_A0) & ~sumidero
    arriba = np.zeros(ny * nx, np.int32)
    src = np.nonzero(canal & (abajo >= 0))[0]
    np.add.at(arriba, abajo[src][canal[abajo[src]]], 1)
    cabezas = np.nonzero(canal & (arriba == 0))[0]
    visto = np.zeros(ny * nx, bool)
    out = []

    def peso(a):
        return np.clip(6.9 + 1.4 * np.log10(a / RIO_A0), 6.9, 9.6)

    for h in cabezas[np.argsort(-acc[cabezas])]:
        cam = []
        k = h
        while k >= 0 and canal[k]:
            cam.append(k)
            if visto[k]:
                break
            visto[k] = True
            k = abajo[k]
        if len(cam) < 3:
            continue
        cam = np.array(cam)
        lon = lon_[cam % nx]
        lat = lat_[cam // nx]
        L = np.stack([lon, lat], 1)
        if len(L) > 5:                                   # suaviza el zigzag del D8 (extremos fijos: siguen unidos al río mayor)
            K = np.ones(5) / 5
            Ls = L.copy()
            Ls[2:-2, 0] = np.convolve(L[:, 0], K, "valid")
            Ls[2:-2, 1] = np.convolve(L[:, 1], K, "valid")
            L = Ls
        if len(L) > 9:                                   # rejilla fina: un segundo suavizado más ancho
            K = np.ones(9) / 9
            Ls = L.copy()
            Ls[4:-4, 0] = np.convolve(L[:, 0], K, "valid")
            Ls[4:-4, 1] = np.convolve(L[:, 1], K, "valid")
            L = Ls
        pk = np.round(peso(acc[cam]) * 4) / 4
        a = 0
        for b in range(1, len(L) + 1):
            if b == len(L) or pk[b] != pk[a]:
                seg = L[a:min(b + 1, len(L))]
                if len(seg) >= 2:
                    out.append((seg, float(pk[a])))
                a = b
    return out


def _construir(rej):
    """Calcula todos los campos de la rejilla de Querétaro (se hace una vez y se guarda en datos/campos_mx.npz)."""
    global _PAISES, _RIOS
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    _RIOS = json.load(open(F_RIOS, encoding="utf-8"))
    lagos = json.load(open(F_LAGOS, encoding="utf-8"))
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    agua = _mask_geoms(rej, [f["geometry"] for f in lagos["features"] if f["geometry"]])      # Solís y Tepuxtepec (Lerma)
    M = {}
    for k, (sem, nivel, caja) in PRESAS.items():
        M[k] = (cv2.GaussianBlur(_fina_a_rejilla(rej, _presa_fina(sem, nivel, caja)), (0, 0), 0.8) > 0.5).astype(np.uint8) * 255
        agua = cv2.bitwise_or(agua, M[k])
    M["presa_centenario"] = _mask_poli(rej, PRESA_CENTENARIO, mano=False)
    agua = cv2.bitwise_or(agua, M["presa_centenario"])
    tierra = cv2.bitwise_and(tierra0, cv2.bitwise_not(agua))
    M["tierra"] = tierra
    M["presas"] = agua

    def P(pts, base=tierra, mano=True, amp=None):
        return cv2.bitwise_and(_mask_poli(rej, pts, mano, amp), base)

    def U_(*ms):
        out = ms[0].copy()
        for m in ms[1:]:
            out = cv2.bitwise_or(out, m)
        return out

    def menos(a, *bs):
        out = a.copy()
        for b in bs:
            out = cv2.bitwise_and(out, cv2.bitwise_not(b))
        return out

    def edos(*n):
        return cv2.bitwise_and(_mask_geoms(rej, _estados(n)), tierra)

    todos = sorted({_nombre(f) for f in _PAISES["features"]} - {""})
    mx = edos(*todos)
    qro = edos("Querétaro")
    M["mexico_mod"] = mx
    for n in ESTADOS:
        M[CLAVE_EDO.get(n, "edo_" + _clave(n))] = edos(n)
    M["edo_slp"] = M["edo_san_luis_potosi"]                    # alias corto
    M["queretaro_edo"] = qro                                    # alias
    M["territorio"] = qro                                       # alias: el territorio protagonista del kit
    M["resto_mx"] = menos(mx, edos(*ESTADOS))
    M["nueva_espana"] = mx                                      # todo esto era del reino de la Nueva España (Reino de México)
    M["valle"] = cv2.bitwise_and(U_(P(VALLE_VERDE), P(VALLE_QRO), P(VALLE_BAJIO)), _valle_dem(rej))
    M["metro"] = P(METRO)
    M["mancha_tequis"] = P(MANCHA_TEQUIS, mano=False)
    M["municipio_tequis"] = cv2.bitwise_and(P(MUNICIPIO_TEQUIS, mano=False), qro)     # INEGI 2010, recortado a la raya del estado (NE)
    M["sierra_gorda"] = cv2.bitwise_and(P(SIERRA_GORDA), qro)
    M["semidesierto"] = cv2.bitwise_and(P(SEMIDESIERTO), qro)
    for k, pol in (("otomies", OTOMIES), ("pames", PAMES), ("jonaces", JONACES), ("purepechas", PUREPECHAS),
                   ("mexicas", MEXICAS)):
        M[k] = P(pol, amp=AMP_PUEBLOS)
    M["insurgentes"] = P(INSURGENTES)
    M["chichimecas"] = U_(M["pames"], M["jonaces"], P(CHICHIMECAS_NORTE, amp=AMP_PUEBLOS))
    campos = {k: _i16(_sdf(v)) for k, v in M.items()}
    aux = _relieve(rej, tierra)
    rios = _rios(rej)
    return campos, {}, aux, rios


def _relieve(rej, tierra):
    """(FH, FW, 3): luz del sombreado (-1..1), altitud 0..1 (tierra) y profundidad 0..1 (agua), del relieve Terrarium z10."""
    e = np.maximum(_alt_fina(rej), 0.0)          # Terrarium trae unos pocos px negativos en la Huasteca (artefactos)
    es = cv2.GaussianBlur(e, (0, 0), 1.0)
    gx = cv2.Sobel(es, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(es, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    ys = np.arange(rej.FH, dtype=np.float32)
    _, lat = rej.inv(np.zeros_like(ys), ys)
    px_m = (111320.0 * np.cos(np.radians(lat)) / rej.pxdeg).astype(np.float32)[:, None]
    k = 9.0 / px_m
    luz = np.clip(k * (gx * 0.70 + gy * 0.70), -1.0, 1.0)
    luz = np.where(tierra > 127, luz, 0.0).astype(np.float32)
    alt01 = np.clip((e - ALT_BASE) / ALT_RANGO, 0, 1)
    prof = np.where(tierra > 127, 0.0, 0.35).astype(np.float32)        # las presas: agua clara, poco honda
    return np.stack([luz, alt01.astype(np.float32), prof], -1).astype(np.float32)


def _rios(rej):
    out = []
    for f in _RIOS["features"]:
        n = f["properties"].get("name") or ""
        pk = [v for k, v in RIOS_SI.items() if k in n]
        if not pk:
            continue
        g = f["geometry"]
        for c in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            P = np.asarray(c, float)
            if len(P) < 2:
                continue
            out.append((P, pk[0]))
    out += _rios_dem()
    for pts, peso in RIOS_EXTRA:
        out.append((np.asarray(pts, float), peso))
    return out


def preparar(nombres=("mx",)):
    os.makedirs(DATOS, exist_ok=True)
    for n in nombres:
        rej = REJ[n]
        campos, cel, aux, rios = _construir(rej)
        datos = {f"c_{k}": v for k, v in campos.items()}
        datos["aux"] = aux.astype(np.float16)
        datos["rios_pts"] = np.concatenate([r[0] for r in rios]).astype(np.float32)
        datos["rios_cortes"] = np.cumsum([0] + [len(r[0]) for r in rios]).astype(np.int64)
        datos["rios_peso"] = np.array([r[1] for r in rios], np.float32)
        np.savez_compressed(os.path.join(DATOS, f"campos_{n}.npz"), **datos)
        print(n, rej.FW, "x", rej.FH, "campos:", len(campos), "ríos:", len(rios), flush=True)


def _cargar_rej(rej):
    if rej.campos:
        return
    d = np.load(os.path.join(DATOS, f"campos_{rej.nombre}.npz"))
    for k in d.files:
        if k.startswith("c_"):
            rej.campos[k[2:]] = d[k]
    rej.aux = d["aux"].astype(np.float32) if "aux" in d.files else None
    pts, cortes, peso = d["rios_pts"].astype(np.float64), d["rios_cortes"], d["rios_peso"]
    rej.rios = [(pts[a:b], float(p)) for a, b, p in zip(cortes[:-1], cortes[1:], peso)]
    rej.r_pts = pts
    rej.r_cortes = cortes
    rej.r_peso = peso


ACT = None
CAMPOS = {}
CELDAS = {}
LON0 = LON1 = LAT0 = LAT1 = 0.0
FW = FH = 0


def usar(nombre="mx"):
    global ACT, CAMPOS, CELDAS, LON0, LON1, LAT0, LAT1, FW, FH
    rej = REJ["mx"]
    _cargar_rej(rej)
    ACT = rej
    CAMPOS = rej.campos
    CELDAS = dict(CELDAS_SEMILLAS)
    LON0, LON1, LAT0, LAT1, FW, FH = rej.lon0, rej.lon1, rej.lat0, rej.lat1, rej.FW, rej.FH


def cargar():
    _cargar_rej(REJ["mx"])
    if ACT is None:
        usar("mx")


def proj(lon, lat):
    return ACT.proj(lon, lat)


def proj_pts(P):
    return ACT.proj_pts(P)


def celdas(nombre):
    rej = ACT
    if nombre in rej._cel:
        return rej._cel[nombre]
    seeds = rej.proj_pts(CELDAS_SEMILLAS[nombre])
    ys, xs = np.mgrid[0:rej.FH:2, 0:rej.FW:2].astype(np.float32)
    d = np.stack([np.hypot(xs - sx, ys - sy) for sx, sy in seeds], 0)
    idx = np.argmin(d, 0).astype(np.uint8)
    ds = np.sort(d, 0)
    borde = ((ds[1] - ds[0]) * 0.5).astype(np.float32)
    idx = cv2.resize(idx, (rej.FW, rej.FH), interpolation=cv2.INTER_NEAREST)
    borde = cv2.resize(borde, (rej.FW, rej.FH), interpolation=cv2.INTER_LINEAR)
    rej._cel[nombre] = (idx, borde)
    return rej._cel[nombre]


# ------------------------------------------------------------------ cámara
class Cam:
    """Cámara: centro (lon, lat), zoom z (px de pantalla por px de la rejilla), giro (rad)."""

    def __init__(self, lon=-99.85, lat=20.83, z=1.0, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.rej = ACT if ACT is not None else REJ["mx"]
        self.lon, self.lat, self.z, self.rot = lon, lat, z, rot
        self.zn = z * PXDEG_REF / self.rej.pxdeg
        cx, cy = self.rej.proj(lon, lat)
        c, s = math.cos(rot) * self.zn, math.sin(rot) * self.zn
        self.M = np.float32([[c, -s, W / 2 - (c * cx - s * cy)], [s, c, H / 2 - (s * cx + c * cy)]])

    def pant(self, lon, lat):
        x, y = self.rej.proj(lon, lat)
        M = self.M
        return float(M[0, 0] * x + M[0, 1] * y + M[0, 2]), float(M[1, 0] * x + M[1, 1] * y + M[1, 2])

    def pant_pts(self, P):
        P = np.asarray(P, float)
        x, y = self.rej.proj(P[:, 0], P[:, 1])
        M = self.M
        return np.stack([M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]], 1)

    def proyectar(self, campo, relleno=4000.0):
        if campo.dtype == np.int16:
            r = cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=int(min(relleno * ESC_I16, 32000)))
            return r.astype(np.float32) * np.float32(self.zn / ESC_I16)
        r = cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)
        return r * np.float32(self.zn)

    def proyectar_crudo(self, img, relleno=0.0, interp=cv2.INTER_LINEAR):
        return cv2.warpAffine(img, self.M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)

    @property
    def escala(self):
        return self.z

    def limites(self):
        hw = W / 2 / (self.zn * self.rej.pxdeg)
        y = float(ymerc(self.lat))
        hh = H / 2 / (self.zn * self.rej.pxdeg)
        return self.lon - hw, self.lon + hw, float(inv_ymerc(y - hh)), float(inv_ymerc(y + hh))


# ------------------------------------------------------------------ pincel de guache
def _texturas():
    r = np.random.default_rng(7)
    lento = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 12, W // 12)).astype(np.float32), (0, 0), 3), (W, H), interpolation=cv2.INTER_CUBIC)
    trazos = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=16, sigmaY=5.0)
    lento = lento / (lento.std() + 1e-6)
    trazos = trazos / (trazos.std() + 1e-6)
    pincel = (0.020 * lento + 0.007 * trazos).astype(np.float32)
    grano = (B.PAPEL_F / (np.array(B.PAPEL, np.float32) / 255.0)).astype(np.float32)
    ruido = []
    for k in range(3):
        n = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 6, W // 6)).astype(np.float32), (0, 0), 1.6), (W, H), interpolation=cv2.INTER_CUBIC)
        ruido.append((n / (n.std() + 1e-6)).astype(np.float32))
    return pincel, grano, ruido


PINCEL, GRANO, RUIDO = _texturas()
_CERO = np.zeros((H, W), np.float32)

from numba import njit, prange            # noqa: E402


@njit(parallel=True, fastmath=True, cache=True)
def _pintar_nb(img, S, nz, pincel, grano, col, alfa, sombra, borde, amp, luz, kluz, y0, y1, x0, x1):
    h, w = S.shape
    for y in prange(y0, y1):
        for x in range(x0, x1):
            s = S[y, x] + amp * nz[y, x]
            if s > 2.0:
                continue
            a = 0.5 - s * 0.7692
            if a <= 0.0:
                continue
            if a > 1.0:
                a = 1.0
            a *= alfa
            d = -s * (1.0 / 70.0)
            if d < 0.0:
                d = 0.0
            if d > 1.0:
                d = 1.0
            lum = 1.0 - 0.07 * (1.0 - d) * borde
            if d < 1.0:
                xm = x - 1 if x > 0 else 0
                xp = x + 1 if x < w - 1 else w - 1
                ym = y - 1 if y > 0 else 0
                yp = y + 1 if y < h - 1 else h - 1
                gx = S[y, xp] - S[y, xm]
                gy = S[yp, x] - S[ym, x]
                nr = np.sqrt(gx * gx + gy * gy) + 1e-6
                sh = (gx * 0.55 + gy * 0.83) / nr
                band = (1.0 - d) * (1.0 - d)
                if sh > 0.0:
                    lum -= sombra * sh * band
                else:
                    lum -= 0.10 * sh * band
            k = lum * (1.0 + 1.2 * pincel[y, x]) * (1.0 + kluz * luz[y, x])
            for c in range(3):
                pig = col[c] * k * grano[y, x, c]
                img[y, x, c] = img[y, x, c] * (1.0 - a) + pig * a


@njit(parallel=True, fastmath=True, cache=True)
def _tierra_nb(img, S, nz, pincel, grano, aux, c_baja, c_alta, c_cumbre, c_mar, c_hondo, c_orilla, amp, y0, y1, x0, x1):
    h, w = S.shape
    for y in prange(y0, y1):
        for x in range(x0, x1):
            s = S[y, x] + amp * nz[y, x]
            luz = aux[y, x, 0]
            alt = aux[y, x, 1]
            pr = aux[y, x, 2]
            pc = 1.0 + 1.3 * pincel[y, x]
            if s > -2.0:
                u = pr ** 0.6
                o = 0.0
                if s < 46.0 and s > 0.0:
                    t = 1.0 - s / 46.0
                    o = t * t * 0.55
                for c in range(3):
                    m = c_mar[c] * (1.0 - u) + c_hondo[c] * u
                    m = m * (1.0 - o) + c_orilla[c] * o
                    img[y, x, c] = m * pc * grano[y, x, c]
            if s > 2.0:
                continue
            a = 0.5 - s * 0.7692
            if a <= 0.0:
                continue
            if a > 1.0:
                a = 1.0
            d = -s * (1.0 / 60.0)
            if d < 0.0:
                d = 0.0
            if d > 1.0:
                d = 1.0
            lum = 1.0 - 0.06 * (1.0 - d)
            if d < 1.0:
                xm = x - 1 if x > 0 else 0
                xp = x + 1 if x < w - 1 else w - 1
                ym = y - 1 if y > 0 else 0
                yp = y + 1 if y < h - 1 else h - 1
                gx = S[y, xp] - S[y, xm]
                gy = S[yp, x] - S[ym, x]
                nr = np.sqrt(gx * gx + gy * gy) + 1e-6
                sh = (gx * 0.55 + gy * 0.83) / nr
                band = (1.0 - d) * (1.0 - d)
                if sh > 0.0:
                    lum -= 0.13 * sh * band
                else:
                    lum -= 0.08 * sh * band
            lum *= (1.0 + 0.40 * luz) * (1.0 + 1.2 * pincel[y, x])
            ac = alt * 1.6
            if ac > 1.0:
                ac = 1.0
            sn = (alt - 0.72) * 4.0
            if sn < 0.0:
                sn = 0.0
            if sn > 1.0:
                sn = 1.0
            for c in range(3):
                col = c_baja[c] * (1.0 - ac) + c_alta[c] * ac
                col = col * (1.0 - sn) + c_cumbre[c] * sn
                pig = col * lum * grano[y, x, c]
                img[y, x, c] = img[y, x, c] * (1.0 - a) + pig * a


def _roi(S, margen=24):
    m = S[::8, ::8] < 3.0
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        return None
    return (max(0, ys.min() * 8 - margen), min(H, ys.max() * 8 + 8 + margen), max(0, xs.min() * 8 - margen), min(W, xs.max() * 8 + 8 + margen))


def _c(col):
    return np.array(col, np.float32) / 255.0


def pintar(img, S, color, alfa=1.0, fase=0, borde=1.0, sombra=0.24, ruido=1.0, luz=None, kluz=0.34):
    r = _roi(S)
    if r is None:
        return
    _pintar_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, _c(color), np.float32(alfa), np.float32(sombra), np.float32(borde),
               np.float32(4.0 * ruido), _CERO if luz is None else luz, np.float32(kluz if luz is not None else 0.0), r[0], r[1], r[2], r[3])


class Base:
    pass


def pintar_base(cam, fase=0):
    """Fondo: mar con profundidad, tierra con relieve de las Sierras Madres y el cinturón verde mesoamericano."""
    rej = cam.rej
    img = np.empty((H, W, 3), np.float32)
    S = cam.proyectar(rej.campos["tierra"])
    aux = cam.proyectar_crudo(rej.aux, 0.0)
    _tierra_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, aux, _c(TIERRA), _c(TIERRA_ALTA), _c(TIERRA_CUMBRE), _c(MAR_CL), _c(MAR_HONDO), _c((214, 234, 230)),
               np.float32(3.0), 0, H, 0, W)
    b = Base()
    b.S, b.luz = S, aux[..., 0].copy()
    Sv = cam.proyectar(rej.campos["valle"])
    pintar(img, Sv, VALLE, 0.72, fase, borde=0.35, sombra=0.08, ruido=0.6, luz=b.luz, kluz=0.28)
    return img, b


def pintar_rios(img, cam, base, t=0.0, alfa=0.92, minimo=None):
    """Ríos (pincelada azul) sobre tierra y territorios; grosor según el peso del río y el zoom."""
    rej = cam.rej
    if minimo is None:
        minimo = float(np.interp(math.log(max(cam.z, 0.05)), [math.log(1.0), math.log(3.0)], [8.3, 6.8]))
    Q = cam.pant_pts(rej.r_pts)
    Q16 = np.rint(Q * 16).astype(np.int32)
    capas = [[], [], []]
    for (a, b, p) in zip(rej.r_cortes[:-1], rej.r_cortes[1:], rej.r_peso):
        if p < minimo:
            continue
        seg = Q16[a:b]
        if len(seg) < 2 or seg[:, 0].max() < -320 or seg[:, 0].min() > (W + 20) * 16 or seg[:, 1].max() < -320 or seg[:, 1].min() > (H + 20) * 16:
            continue
        f = p - minimo
        capas[0 if f < 0.7 else (1 if f < 1.6 else 2)].append(seg)
    m = np.zeros((H, W), np.uint8)
    esc = max(0.7, min(2.6, cam.z / 2.2)) ** 0.65
    for g, L in enumerate(capas):
        if L:
            cv2.polylines(m, L, False, 255, max(1, int(round((2.2 + 1.9 * g) * esc))), cv2.LINE_AA, 4)
    tierra = (base.S < -1.0).astype(np.uint8) * 255
    m = cv2.multiply(m, tierra, scale=1 / 255.0)
    ys, xs = np.nonzero(m)
    if len(ys):
        a = (m[ys, xs].astype(np.float32) / 255.0)[:, None] * alfa
        col = _c(RIO) * (1 + 1.2 * PINCEL[ys, xs])[:, None] * GRANO[ys, xs]
        img[ys, xs] = img[ys, xs] * (1 - a) + col * a


_ROT = {}


def _mascara_rot(t, px, rot):
    k = (t, px, rot)
    if k not in _ROT:
        m = B.mascara_texto(t, px)
        if rot:
            h_, w_ = m.shape
            d = int(math.hypot(w_, h_)) + 4
            big = np.zeros((d, d), np.uint8)
            big[(d - h_) // 2:(d - h_) // 2 + h_, (d - w_) // 2:(d - w_) // 2 + w_] = m
            Mr = cv2.getRotationMatrix2D((d / 2, d / 2), math.degrees(rot), 1.0)
            m = cv2.warpAffine(big, Mr, (d, d))
            ys, xs = np.nonzero(m > 8)
            m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        _ROT[k] = m
    return _ROT[k]


def rotulo_mapa(img, txt, cam, lon, lat, px=40, alfa=0.42, color=(70, 96, 120), espaciado=True, rot=0.0):
    x, y = cam.pant(lon, lat)
    t = " ".join(txt) if espaciado else txt
    px = int(max(18, min(84, px * (cam.zn / 2.6) ** 0.45)))
    m = _mascara_rot(t, px, round(rot, 3))
    h_, w_ = m.shape
    x0, y0 = int(x - w_ / 2), int(y - h_ / 2)
    fuera = max(0.0, 30 - x0, x0 + w_ - (W - 30), 125 - y0, y0 + h_ - (H - 30))
    alfa *= max(0.0, 1.0 - fuera / 24.0)
    if alfa <= 0.01:
        return
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w_), min(H, y0 + h_)
    if xb <= xa or yb <= ya:
        return
    a = (m[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32) / 255.0)[..., None] * alfa
    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - a) + _c(color) * a


def mezcla_campos(a, b, k):
    k = float(min(1.0, max(0.0, k)))
    if k <= 0:
        return CAMPOS[a]
    if k >= 1:
        return CAMPOS[b]
    return cv2.addWeighted(CAMPOS[a], 1 - k, CAMPOS[b], k, 0)


if __name__ == "__main__":
    preparar()
