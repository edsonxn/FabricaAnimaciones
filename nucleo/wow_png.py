# -*- coding: utf-8 -*-
"""Imágenes REALES de WoW vanilla para los escenarios dibujados (pedido del usuario, 15-oct-2026: «más WoW real»).

  python nucleo/wow_png.py "Hakkar" "Spirit Healer" "Ironforge Guard" ...   busca el PNJ en Wowhead (classic), saca su
        modelo y baja el render oficial con fondo transparente (300x300) a nucleo/datos/wow_png/npc_<modelo>.png
  python nucleo/wow_png.py --hoja                                            hoja de contacto previews: datos/wow_png/_hoja.jpg
  ruta = wow_png.png("Hakkar")                                               ruta del PNG (lo baja si falta; la búsqueda
                                                                             necesita el navegador; el índice la evita)
  rgba = wow_png.recorte_clip(ruta_mp4, seg, caja=(x0, y0, x1, y1))          recorte de un cuadro de un clip real con el
                                                                             fondo quitado (transparent_background)

Wowhead bloquea curl y Chrome sin ventana (CloudFront): la búsqueda abre Chrome FUERA de la pantalla y pide las páginas con
fetch desde dentro. El modelo sale de `WH.Gatherer.addData(1, 4, {"<npc>":{"name_enus":..,"model":N}})`; el render vive
en wow.zamimg.com/modelviewer/classic/webthumbs/npc/<N % 256>/<N>.webp (sin bloqueo). Crédito: «Modelos: Blizzard
Entertainment, vía Wowhead».
"""
import json
import os
import re
import sys
import urllib.request

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, "datos", "wow_png")
INDICE = os.path.join(CARPETA, "indice.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def _indice():
    if os.path.exists(INDICE):
        with open(INDICE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _guardar_indice(ind):
    os.makedirs(CARPETA, exist_ok=True)
    with open(INDICE, "w", encoding="utf-8") as f:
        json.dump(ind, f, ensure_ascii=False, indent=1, sort_keys=True)


def _clave(nombre):
    return nombre.strip().lower()


def buscar(nombres, version="classic"):
    """Nombre en inglés del PNJ -> {"npc": id, "model": id, "nombre": nombre exacto}. Guarda en el índice."""
    from playwright.sync_api import sync_playwright
    ind = _indice()
    falta = [n for n in nombres if _clave(n) not in ind]
    if not falta:
        return {n: ind[_clave(n)] for n in nombres}
    base = "https://www.wowhead.com/%s" % version
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="chrome", headless=False, args=["--window-position=-2600,0"])
        pg = nav.new_page()
        pg.goto(base + "/npc=6491", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(5000)
        trae = "async (u) => { const r = await fetch(u); return await r.text(); }"
        for n in falta:
            npc = None
            if re.fullmatch(r"\d+", n.strip()):
                npc = int(n)
            else:
                html = pg.evaluate(trae, base + "/search?q=" + urllib.request.quote(n))
                for bloque in re.findall(r'<script type="application/json" id="data\.[^"]*">(.*?)</script>', html, re.S):
                    try:
                        datos = json.loads(bloque)
                    except ValueError:
                        continue
                    if not isinstance(datos, list):
                        continue
                    for d in datos:
                        if isinstance(d, dict) and "classification" in d and _clave(str(d.get("name", ""))) == _clave(n):
                            npc = int(d["id"])
                            break
                    if npc:
                        break
            if not npc:
                print("  ✗ no encontré el PNJ «%s»" % n)
                continue
            html = pg.evaluate(trae, base + "/npc=%d" % npc)
            m = re.search(r'"%d":\{"name_enus":"((?:[^"\\]|\\.)*)","model":(\d+)' % npc, html)
            if not m:
                print("  ✗ «%s» (npc %d) sin modelo" % (n, npc))
                continue
            ind[_clave(n)] = {"npc": npc, "model": int(m.group(2)), "nombre": m.group(1)}
            print("  ✓ %s -> npc %d, modelo %s" % (m.group(1), npc, m.group(2)))
            _guardar_indice(ind)
        nav.close()
    return {n: ind.get(_clave(n)) for n in nombres}


def bajar(model, version="classic"):
    """Render oficial del modelo (fondo transparente) -> PNG RGBA recortado a su silueta. Devuelve la ruta."""
    from PIL import Image
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, "npc_%d.png" % int(model))
    if os.path.exists(ruta):
        return ruta
    url = "https://wow.zamimg.com/modelviewer/%s/webthumbs/npc/%d/%d.webp" % (version, int(model) % 256, int(model))
    tmp = ruta + ".webp"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r, \
            open(tmp, "wb") as f:
        f.write(r.read())
    im = Image.open(tmp).convert("RGBA")
    a = np.asarray(im)[..., 3]
    ys, xs = np.nonzero(a > 8)
    if len(ys):
        im = im.crop((max(0, xs.min() - 2), max(0, ys.min() - 2), min(im.width, xs.max() + 3), min(im.height, ys.max() + 3)))
    im.save(ruta)
    os.remove(tmp)
    return ruta


def png(nombre, version="classic"):
    """Ruta del PNG de un PNJ por su nombre en inglés (o su id de PNJ)."""
    info = _indice().get(_clave(nombre)) or buscar([nombre], version).get(nombre)
    if not info:
        raise KeyError("PNJ sin render: %s" % nombre)
    return bajar(info["model"], version)


def recorte_clip(ruta_mp4, seg, caja=None, umbral=0.5):
    """Cuadro real de un clip (segundo `seg`), recortado a `caja` (px del clip) y con el fondo quitado -> RGBA uint8."""
    import cv2
    cap = cv2.VideoCapture(ruta_mp4)
    cap.set(cv2.CAP_PROP_POS_MSEC, seg * 1000.0)
    ok, f = cap.read()
    cap.release()
    if not ok:
        raise IOError("sin cuadro en %s @ %.2f" % (ruta_mp4, seg))
    if caja:
        x0, y0, x1, y1 = caja
        f = f[y0:y1, x0:x1]
    rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
    from PIL import Image
    from transparent_background import Remover
    global _REM
    try:
        _REM
    except NameError:
        _REM = Remover(mode="base")
    m = np.asarray(_REM.process(Image.fromarray(rgb), type="map").convert("L"), np.float32) / 255.0
    a = np.clip((m - umbral * 0.6) / 0.4, 0, 1)
    return np.dstack([rgb, (a * 255).astype(np.uint8)])


def hoja():
    """Hoja de contacto de todo lo bajado (para mirarla)."""
    import cv2
    from PIL import Image
    ind = _indice()
    celdas = []
    for k, v in sorted(ind.items()):
        r = os.path.join(CARPETA, "npc_%d.png" % v["model"])
        if not os.path.exists(r):
            continue
        im = np.asarray(Image.open(r).convert("RGBA")).astype(np.float32) / 255.0
        h, w = im.shape[:2]
        s = 200.0 / max(h, w)
        im = cv2.resize(im, (max(1, int(w * s)), max(1, int(h * s))), interpolation=cv2.INTER_AREA)
        c = np.full((236, 220, 3), 0.86, np.float32)
        y0, x0 = 4 + (200 - im.shape[0]) // 2, (220 - im.shape[1]) // 2
        a = im[..., 3:4]
        c[y0:y0 + im.shape[0], x0:x0 + im.shape[1]] = c[y0:y0 + im.shape[0], x0:x0 + im.shape[1]] * (1 - a) + im[..., :3] * a
        cv2.putText(c, v["nombre"][:24], (4, 228), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 1, cv2.LINE_AA)
        celdas.append(c)
    if not celdas:
        return None
    cols = 6
    filas = [np.hstack(celdas[i:i + cols] + [np.full_like(celdas[0], 1.0)] * (cols - len(celdas[i:i + cols])))
             for i in range(0, len(celdas), cols)]
    out = os.path.join(CARPETA, "_hoja.jpg")
    cv2.imwrite(out, cv2.cvtColor((np.vstack(filas) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--hoja":
        print(hoja())
    elif args:
        for n, info in buscar(args).items():
            if info:
                print("  %s -> %s" % (n, bajar(info["model"])))
        print(hoja())
    else:
        print(__doc__)
