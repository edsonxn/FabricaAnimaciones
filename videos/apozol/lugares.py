# -*- coding: utf-8 -*-
"""Lugares reales del video (lon, lat), registrados en el catálogo del kit de mapas para usarlos por nombre."""
import kz_mapa_dib as MD

LUGARES = {
    "apozol": (-103.0903, 21.4708),           # cabecera (21°28′15″N 103°05′25″W, Wikipedia ES)
    "juchipila": (-103.1176, 21.4103),
    "jalpa": (-102.9700, 21.6350),
    "mixton": (-103.0500, 21.4350),           # peñol del Mixtón (entre Juchipila y Apozol; ubicación aproximada)
    "nochistlan": (-102.8430, 21.3660),
    "tlaltenango": (-103.3150, 21.7800),
    "moyahua": (-103.1630, 21.2680),
    "villanueva": (-102.8830, 22.3550),
    "tabasco": (-102.9200, 21.8700),
    "mezquital": (-103.2700, 21.2250),
    "zacatecas": (-102.5832, 22.7709),
    "guadalajara": (-103.3496, 20.6597),
    "mexico": (-99.1332, 19.4326),
}
MD.CIUDADES.update(LUGARES)

# trazo aproximado de la carretera federal 54 entre Zacatecas y Guadalajara por el cañón (estilizado)
RUTA_54 = ["zacatecas", "villanueva", "tabasco", "jalpa", "apozol", "juchipila", "moyahua", "mezquital", (-103.30, 21.00), "guadalajara"]
