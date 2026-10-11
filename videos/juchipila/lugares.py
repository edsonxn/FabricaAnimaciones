# -*- coding: utf-8 -*-
"""Lugares reales del video (lon, lat), registrados en el catálogo del kit de mapas para usarlos por nombre."""
import kz_mapa_dib as MD

LUGARES = {
    "juchipila": (-103.1176, 21.4103),        # cabecera (21°24′37″N 103°07′03″W)
    "las_ventanas": (-103.1133, 21.3722),     # Cerro de las Ventanas, ~5 km al sur de la cabecera
    "apozol": (-103.0830, 21.4670),
    "nochistlan": (-102.8430, 21.3660),
    "tlaltenango": (-103.3150, 21.7800),
    "jalpa": (-102.9700, 21.6350),
    "teul": (-103.4640, 21.4630),
    "moyahua": (-103.1630, 21.2680),
    "mixton": (-103.0500, 21.4350),           # peñol del Mixtón (entre Juchipila y Apozol; ubicación aproximada)
    "la_quemada": (-102.8400, 22.4400),       # sitio de Tuitlán / La Quemada (origen de la tradición de llegada de los caxcanes)
    "zacatecas": (-102.5832, 22.7709),
    "guadalajara": (-103.3496, 20.6597),
    "valladolid_esp": (-4.7245, 41.6523),
    "ocotlan": (-102.7740, 20.3530),
    "veracruz": (-96.1342, 19.1738),
    "mexico": (-99.1332, 19.4326),
    "tlaxcala": (-98.2370, 19.3139),
    "patzcuaro": (-101.6090, 19.5140),
    "culiacan": (-107.3940, 24.8091),
    "compostela": (-104.9000, 21.2300),
}
MD.CIUDADES.update(LUGARES)
