# -*- coding: utf-8 -*-
"""Estilos personales del Estudio: la interfaz guarda opciones sencillas (fondo, colores, trazo, letra…) y aquí se
traducen al diccionario de estilo del núcleo (ver nucleo/estilos.py). Se guardan en estudio/estilos.json."""
import json
import os
import re
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(AQUI, "estilos.json")

FONDOS = {           # nombre del núcleo -> nombre amable
    "liso": "Color liso", "degradado": "Degradado (cielo)", "plano": "Colores suaves que cambian",
    "pizarra": "Pizarra", "kraft": "Papel kraft", "cartulina": "Cartulina", "cosmos": "Espacio con nebulosa",
    "espacio": "Cielo nocturno", "rayos": "Rayos de cómic", "plasma": "Plasma psicodélico", "ondas": "Ondas",
    "rejilla": "Rejilla retro (synthwave)", "cueva": "Pared de cueva",
}
PALETAS = ["arcoiris", "fuego", "acido", "chicle", "oceano", "lima", "ocaso", "cosmos", "ocre", "neon"]
CON_PALETA = ("plano", "rayos", "plasma", "ondas", "cartulina", "rejilla")
LETRAS = {"snap": "Divertida", "geo": "Moderna", "print": "Escrita a mano", "black": "Gruesa", "show": "Cartel"}
COLORES = {"vivos": None, "pastel": "pastel", "acuarela": "acuarela", "oscuro": "oscuro", "mate": "mate"}


def _rgb(h, defecto=None):
    if not h or not re.fullmatch(r"#?[0-9a-fA-F]{6}", h):
        return defecto
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def _f(x, a, b, defecto):
    try:
        return max(a, min(b, float(x)))
    except (TypeError, ValueError):
        return defecto


def a_nucleo(e):
    """Opciones de la interfaz -> ESTILO_PERSONAL (lo lee estudio/escenas_estudio.py)."""
    fondo = e.get("fondo") if e.get("fondo") in FONDOS else "liso"
    pal = e.get("paleta") if e.get("paleta") in PALETAS else "arcoiris"
    c1 = [v / 255 for v in _rgb(e.get("color_fondo"), [246, 238, 220])]
    c2 = [v / 255 for v in _rgb(e.get("color_fondo2"), [190, 220, 250])]
    if fondo == "liso":
        f = ("liso", {"color": c1, "lineas": False})
    elif fondo == "degradado":
        f = ("degradado", {"arriba": c1, "abajo": c2})
    elif fondo in CON_PALETA:
        f = (fondo, {"pal": pal})
    elif fondo == "cueva":
        f = ("cueva", {"tinte": 0.3})
    else:
        f = (fondo, {})
    pegatina = bool(e.get("pegatina"))
    d = {
        "base": e.get("base") or "limpio",
        "descripcion": f"Estilo personal «{e.get('nombre', 'sin nombre')}»",
        "tinta": _rgb(e.get("tinta")),
        "relleno": COLORES.get(e.get("colores"), None),
        "wob": _f(e.get("temblor"), 0, 3, 1.0),
        "sticker": pegatina, "borde_sticker": [255, 251, 242] if pegatina else None, "grosor_sticker": 13,
        "sombra": _f(e.get("sombra"), 0, 0.6, 0.2),
        "textura_trazo": 0.0,
        "brillo_neon": _f(e.get("neon"), 0, 1, 0.0),
        "grano": _f(e.get("textura"), 0, 0.08, 0.02),
        "vineta": bool(e.get("vineta", True)),
        "fuente_titulos": e.get("letra") if e.get("letra") in LETRAS else "snap",
        "color_particulas": _rgb(e.get("particulas"), [255, 255, 255]),
        "color_halo": _rgb(e.get("particulas"), [255, 255, 255]),
        "fondos": {k: f for k in ("titulo", "antes", "hoy", "libre")},
    }
    if d["tinta"] is None:
        d.pop("tinta")                      # se queda la del estilo base
    return d


def cargar():
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar(lista):
    tmp = ARCHIVO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ARCHIVO)


def guardar_uno(e):
    lista = [x for x in cargar() if x.get("id") != e.get("id")]
    if not e.get("id"):
        e["id"] = "personal_" + time.strftime("%Y%m%d%H%M%S")
    e["nombre"] = (e.get("nombre") or "Mi estilo").strip()[:30]
    lista.append(e)
    guardar(lista)
    return e


def buscar(eid):
    return next((x for x in cargar() if x.get("id") == eid), None)


def borrar(eid):
    guardar([x for x in cargar() if x.get("id") != eid])
