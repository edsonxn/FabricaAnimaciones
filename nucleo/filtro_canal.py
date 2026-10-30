# -*- coding: utf-8 -*-
"""LISTA ROJA del canal Edsonxn («Jefe de Robots»): nada privado sale en un video. Se corre sobre guion, efectos y descripción
ANTES de la voz y otra vez antes de subir; si encuentra algo, sale con código 1 y el video no avanza.

  python nucleo/filtro_canal.py <v>

Desde el 30-oct-2026 (el usuario) solo se protegen TRES canales: Crónicas de Warcraft, Crónicas de Tamriel y Runa Caída, sin nombre, imagen ni logo,
y lo que los delata (alias wow_/tes_/er_, sus juegos, sus videos, el patrocinador y su código). Los demás canales se pueden mostrar y mencionar.
Siempre revisa además correos, claves, enlaces y dominios propios, dinero y datos personales. Doc: docs/estilo_jefe_robots.md.
"""
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTEGIDOS = ("cronicas_warcraft", "cronicas_tamriel", "runa_caida")
SENALES = ("crónicas de warcraft", "cronicas de warcraft", "crónicas de tamriel", "cronicas de tamriel", "runa caída", "runa caida", "warcraft", "world of warcraft",
           "azeroth", "tamriel", "skyrim", "elder scrolls", "elden ring", "malenia", "radagon", "miquella", "ranni", "márika", "marika", "darrowshire",
           "virus sencillo", "server-troyano", "troyano", "programa espia", "programa espía", "cambiar icono a un virus", "gaia_crematoria", "la crematoria", "gaia_eterna", "gaia eterna",   # historias de WoW: su arte delata
           "overgear", "cronicas10", "clicknbusiness", "panel_remoto", "ngrok", "client_secret", "elevenlabs_api", "pagina.py")
PREFIJOS = ("wow_", "tes_", "er_")
PATRONES = (("correo", r"[\w.+-]+@[\w-]+\.\w{2,}"),
            ("clave", r"\b(?:sk|pk|AIza|ghp|ya29)[-_][\w-]{12,}"),
            ("enlace", r"https?://(?!youtu\.be|www\.youtube\.com)\S+"),
            ("id de voz", r"\b[A-Za-z0-9]{20}\b"),
            ("dinero", r"(?:\$|US\$|MXN|dólares|pesos)\s*\d|\d+\s*(?:dólares|pesos|usd)\b|ingresos?\s+de"),
            ("ruta", r"[A-Z]:[\\/]\w+"))


def nombres():
    """Todo lo que no puede salir: los tres protegidos, sus señales y cada video suyo."""
    out = set(SENALES) | set(PROTEGIDOS)
    for alias in PROTEGIDOS:
        ruta = os.path.join(RAIZ, "canales", alias + ".json")
        if os.path.exists(ruta):
            d = json.load(open(ruta, encoding="utf-8"))
            out |= {str(x).lower() for p in d.get("publicados", []) if isinstance(p, dict) for x in (p.get("video"), p.get("titulo")) if x and len(str(x)) > 3}
            out |= {str(d.get("nombre") or "").lower()} - {""}
    for v in os.listdir(os.path.join(RAIZ, "videos")):
        if v.lower().startswith(PREFIJOS):
            out.add(v.lower())
    return sorted(out, key=len, reverse=True)


def rojo():
    """Una sola expresión con todo lo protegido, para filtrar la API del panel en las grabaciones."""
    return re.compile(r"(?<!\w)(?:" + "|".join(re.escape(n) for n in nombres()) + r"|(?:wow|tes|er)_[a-z0-9_]+)(?!\w)", re.I)


def revisar(texto):
    hallazgos = []
    bajo = texto.lower()
    for n in nombres():
        if re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", bajo):
            hallazgos.append(("protegido", n))
    for tipo, patron in PATRONES:
        hallazgos += [(tipo, m.group(0)) for m in re.finditer(patron, texto)]
    return hallazgos


def video(v):
    carpeta = os.path.join(RAIZ, "videos", v)
    malo = []
    for nombre in ("guion.py", "efectos.py", "toma.py", "descripcion.txt"):
        ruta = os.path.join(carpeta, nombre)
        if os.path.exists(ruta):
            lineas = open(ruta, encoding="utf-8").read().splitlines()
            texto = "\n".join(x for x in lineas if not x.startswith("VOZ"))   # el id de la voz de Token no sale en pantalla
            malo += [(nombre, *h) for h in revisar(texto)]
    return malo


if __name__ == "__main__":
    malo = video(sys.argv[1])
    for archivo, tipo, txt in malo:
        print(f"LISTA ROJA  {archivo}: {tipo}: {txt}")
    print("limpio" if not malo else f"{len(malo)} hallazgo(s): no avanzar")
    sys.exit(1 if malo else 0)
