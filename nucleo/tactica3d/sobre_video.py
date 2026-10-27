# -*- coding: utf-8 -*-
"""Elementos 3D SOBRE EL VIDEO REAL (27-oct-2026): convierte la pizarra 2D de una pausa (mg_tactica: anillo, flecha, zona,
texto, foco con x, y en fracción del cuadro) en una escena de nucleo/tactica3d en modo «video» —anillos tumbados en el
suelo en perspectiva, columna de luz sobre cada jugador marcado, flechas que se levantan en arco y dan sombra, zonas con
borde de luz— y la registra para renderizarla como capa transparente.

En efectos.py:   FX += pizarra3d("j6_cohete", de, a, els, "41:45", fondo=(fuente(6), 124.8))
Render:          python nucleo/tactica3d/sobre_video.py <video>      (solo las capas nuevas o cambiadas)
"""
import hashlib
import json
import os
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REGISTRO = []          # [(carpeta_capas, nombre, spec, fondo)]


def web(ruta):
    return "/" + os.path.relpath(os.path.abspath(ruta), RAIZ).replace("\\", "/")


def de_pizarra(de, a, els, pilares=True):
    """lista de elementos de mg_tactica.pizarra → escena 3D en modo video (mismos instantes)"""
    E = dict(modo="video", de=de, a=a, anillos=[], flechas=[], zonas=[], pilares=[], etiquetas=[], oscurecer=[], carteles=[])
    for i, e in enumerate(els):
        t, en, sale = e["tipo"], e.get("en", de), e.get("sale", a)
        col = e.get("color", "amarillo")
        if t == "foco":
            E["oscurecer"].append(dict(de=en, a=sale, k=e.get("k", .4)))
        elif t == "anillo":
            rpx = e.get("r", 70)
            E["anillos"].append(dict(u=e["x"], v=e["y"], r=rpx / 1920, color=col, en=en, sale=sale))
            if pilares and rpx <= 80:                     # un jugador: columna de luz encima
                E["pilares"].append(dict(u=e["x"], v=e["y"], r=rpx / 1920 * .55, color=col, en=en + .1, sale=sale, alto=7))
            if e.get("etiqueta"):
                lado, m = e.get("lado", "arriba"), rpx * .9 + 34
                dx, dy = {"arriba": (0, -m), "abajo": (0, m * .8), "izq": (-m, -10), "der": (m, -10)}[lado]
                et = dict(de=en + .15, a=sale, u=e["x"], v=e["y"], alto=0, texto=e["etiqueta"], sub=e.get("sub"),
                          color=col, dx=dx, dy=dy, tam=30)
                if e.get("icono"):
                    et["icono"] = web(e["icono"])
                E["etiquetas"].append(et)
        elif t == "flecha":
            fid = f"f{i}"
            E["flechas"].append(dict(id=fid, pts=e["pts"], color=col, en=en, dur=e.get("dur", .6), sale=sale,
                                     guion=e.get("guion", False), alto=e.get("alto", 2.6), grosor=.75))
            if e.get("etiqueta"):
                ox, oy = e.get("off", (0, -50))
                E["etiquetas"].append(dict(de=en + e.get("dur", .6) * .7, a=sale, flecha=fid, texto=e["etiqueta"], color=col,
                                           dx=ox, dy=oy, tam=28))
        elif t == "zona":
            E["zonas"].append(dict(pts=e["pts"], color=col, en=en, sale=sale, alfa=e.get("alfa", .2)))
        elif t == "texto":
            E["carteles"].append(dict(de=en, a=sale, texto=e["texto"], sub=e.get("sub"), color=col, y=e["y"] * 1080 - 30,
                                      tam=e.get("tam", 40)))
    return E


def registrar(carpeta, nombre, spec, fondo=None):
    REGISTRO.append((carpeta, nombre, spec, fondo))
    return os.path.join(carpeta, nombre)


def _huella(spec):
    return hashlib.sha1(json.dumps(spec, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def renderizar(forzar=False):
    """escribe <carpeta>/<nombre>.json y renderiza las capas cuyo contenido cambió"""
    hechas = 0
    for carpeta, nombre, spec, fondo in REGISTRO:
        os.makedirs(carpeta, exist_ok=True)
        base = os.path.join(carpeta, nombre)
        spec = dict(spec)
        if fondo:                                       # cuadro del VOD para revisar (?fondo=1); no entra en la capa
            img = base + "_fondo.jpg"
            if not os.path.exists(img):
                subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-ss", str(fondo[1]), "-i", fondo[0],
                                "-frames:v", "1", "-q:v", "3", img])
            spec["fondo"] = web(img)
        h = _huella(spec)
        js = base + ".json"
        viejo = json.load(open(js, encoding="utf-8")).get("_huella") if os.path.exists(js) else None
        if not forzar and viejo == h and os.path.exists(base + "_alfa.mp4"):
            continue
        spec["_huella"] = h
        json.dump(spec, open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "render3d.py"), js, base + ".mp4"], check=True)
        hechas += 1
    print(f"capas 3D sobre video: {len(REGISTRO)} ({hechas} renderizadas)")


if __name__ == "__main__":
    v = sys.argv[1]
    d = os.path.join(RAIZ, "videos", v)
    sys.path[:0] = [d, os.path.join(RAIZ, "nucleo"), os.path.dirname(os.path.abspath(__file__))]   # el efectos.py del VIDEO
    os.chdir(d)
    import importlib
    importlib.import_module("efectos")
    importlib.import_module("sobre_video").renderizar("--forzar" in sys.argv)   # el registro vive en el módulo importado
