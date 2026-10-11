# -*- coding: utf-8 -*-
"""Búsqueda y descarga de imágenes para documentales (sin claves de API).

Fuentes, de más a menos segura para publicar:
  1. Wikimedia Commons (`commons`): devuelve licencia y autor -> se guardan en `creditos.json` (dominio público / CC).
  2. Bing Images por scraping (`bing`), igual que C:\\googleimagenes\\index.js (atributo `m` de `a.iusc`, campo `murl`).
     Sin control de licencia: úsalo solo como referencia visual o para imágenes de fondo, y revisa el resultado.

Uso:  python imagenes_web.py commons "Voynich manuscript folio" 8 --dir imagenes
      python imagenes_web.py bing "Beinecke library Yale" 6 --dir imagenes
      python imagenes_web.py archivo "File:Voynich Manuscript (3).jpg" --dir imagenes --ancho 2400
      python imagenes_web.py persona "Alan Turing" 4 --dir imagenes --descargar   retratos REALES de un personaje (foto principal de
                                                                                  Wikipedia + Commons, con cara detectada, licencia
                                                                                  libre y créditos); nombres: alan_turing.jpg, _2, _3
      python imagenes_web.py creditos .                                           bloque de créditos (imagenes/ + clips/) para la
                                                                                  descripción de YouTube
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "FabricaAnimaciones/1.0 (jairedson5@gmail.com) python-urllib"}
UA_NAV = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"}


def _get(url, headers=UA, timeout=40):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            if i == 3:
                raise
            time.sleep(1.5 * (i + 1))


def _api(**k):
    k["format"] = "json"
    return json.loads(_get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(k)))


def _limpia(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def info_archivo(titulo, ancho=2400):
    """Metadatos de un archivo de Commons: url (reducida a `ancho` px), licencia, autor, descripción."""
    r = _api(action="query", titles=titulo, prop="imageinfo", iiprop="url|size|mime|extmetadata", iiurlwidth=ancho)
    p = next(iter(r["query"]["pages"].values()))
    if "imageinfo" not in p:
        return None
    ii = p["imageinfo"][0]
    md = ii.get("extmetadata", {})
    return dict(titulo=p["title"], url=ii.get("thumburl") or ii["url"], url_original=ii["url"], w=ii["width"], h=ii["height"],
                mime=ii["mime"], licencia=_limpia(md.get("LicenseShortName", {}).get("value")),
                autor=_limpia(md.get("Artist", {}).get("value"))[:160],
                descripcion=_limpia(md.get("ImageDescription", {}).get("value"))[:200],
                pagina="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p["title"].replace(" ", "_")))


def commons(consulta, n=8):
    """Busca archivos (imágenes) en Commons; devuelve lista de dicts con `info_archivo`."""
    r = _api(action="query", list="search", srsearch=consulta, srnamespace=6, srlimit=n * 3)
    salida = []
    for m in r["query"]["search"]:
        if not re.search(r"\.(jpe?g|png|tiff?)$", m["title"], re.I):
            continue
        i = info_archivo(m["title"])
        if i:
            salida.append(i)
        if len(salida) >= n:
            break
    return salida


def bing(consulta, n=8):
    """URLs de imágenes de Bing Images (scraping, sin API). Devuelve [(murl, título)]."""
    q = urllib.parse.quote(consulta)
    pag = _get(f"https://www.bing.com/images/search?q={q}&form=HDRSC2&first=1&cw=1177&ch=778", UA_NAV).decode("utf8", "ignore")
    salida = []
    for m in re.finditer(r'class="iusc"[^>]*\sm="([^"]+)"', pag):
        try:
            d = json.loads(html.unescape(m.group(1)))
        except Exception:
            continue
        u = d.get("murl")
        if u and u.startswith("http") and "bing.com" not in u:
            salida.append((u, d.get("t", "")))
        if len(salida) >= n:
            break
    return salida


def descargar(url, destino, headers=UA_NAV):
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    datos = _get(url, headers, timeout=60)
    with open(destino, "wb") as f:
        f.write(datos)
    return len(datos)


def _slug(t):
    t = re.sub(r"^File:", "", t)
    return re.sub(r"[^A-Za-z0-9._-]+", "_", t)[:80]


def guardar_commons(info, carpeta, nombre=None):
    """Descarga un resultado de `commons`/`info_archivo` y lo anota en creditos.json de la carpeta."""
    ext = os.path.splitext(urllib.parse.urlparse(info["url"]).path)[1] or ".jpg"
    nombre = (nombre or os.path.splitext(_slug(info["titulo"]))[0]) + ext
    ruta = os.path.join(carpeta, nombre)
    descargar(info["url"], ruta, UA)
    cr = os.path.join(carpeta, "creditos.json")
    datos = json.load(open(cr, encoding="utf-8")) if os.path.exists(cr) else {}
    datos[nombre] = {k: info[k] for k in ("titulo", "licencia", "autor", "pagina")}
    json.dump(datos, open(cr, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return ruta


# ------------------------------------------------------------------ retratos REALES de personajes (estilo noir y documental)
LIC_NO = re.compile(r"(^|[-\s])N[CD]($|[-\s])|fair use|all rights|copyrighted|non-?free", re.I)   # NC, ND y no libres: fuera
_CASCADAS = {}


def _wiki(lang, **k):
    k["format"] = "json"
    return json.loads(_get(f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(k)))


def foto_principal(nombre, langs=("es", "en")):
    """Nombre del archivo de Commons que Wikipedia usa como foto principal de la página `nombre` (o None)."""
    for lang in langs:
        try:
            r = _wiki(lang, action="query", titles=nombre, prop="pageimages", piprop="name", redirects=1)
            p = next(iter(r["query"]["pages"].values()))
            if p.get("pageimage"):
                return p["pageimage"]
            r = _wiki(lang, action="query", generator="search", gsrsearch=nombre, gsrlimit=1, prop="pageimages", piprop="name")
            for p in r.get("query", {}).get("pages", {}).values():
                if p.get("pageimage"):
                    return p["pageimage"]
        except Exception:
            continue
    return None


def caras_en(datos):
    """Caras (frontales o de perfil) detectadas en unos bytes de imagen: lista de (x, y, w, h) relativos al ancho de la imagen."""
    import cv2
    import numpy as np
    im = cv2.imdecode(np.frombuffer(datos, np.uint8), cv2.IMREAD_GRAYSCALE)
    if im is None:
        return []
    k = 800.0 / max(im.shape)
    if k < 1:
        im = cv2.resize(im, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
    im = cv2.equalizeHist(im)
    for f in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
        c = _CASCADAS.setdefault(f, cv2.CascadeClassifier(cv2.data.haarcascades + f))
        r = c.detectMultiScale(im, 1.1, 5, minSize=(max(40, im.shape[1] // 14),) * 2)
        if len(r):
            return [tuple(float(v) / im.shape[1] for v in q) for q in r]
    return []


def persona(nombre, n=4, langs=("es", "en")):
    """Candidatos de retrato REAL de una persona, ordenados (mejor primero). Cada uno: info_archivo + caras + puntaje + bytes.
    Fuentes: la foto principal de su página de Wikipedia y la búsqueda de Commons; solo licencias libres (se descartan NC/ND/fair use)."""
    cand, vistos = [], set()
    principal = foto_principal(nombre, langs)
    titulos = ["File:" + principal] if principal else []
    try:
        for m in _api(action="query", list="search", srsearch=nombre, srnamespace=6, srlimit=14)["query"]["search"]:
            if re.search(r"\.(jpe?g|png)$", m["title"], re.I):
                titulos.append(m["title"])
    except Exception:
        pass
    apellido = nombre.split()[-1].lower()
    for t in titulos:
        t = t.replace("_", " ")
        if t in vistos or len(cand) >= max(8, n * 2):
            continue
        vistos.add(t)
        i = info_archivo(t, 900)
        if not i or LIC_NO.search(i["licencia"] or "") or min(i["w"], i["h"]) < 400 or not i["mime"].startswith("image/"):
            continue
        try:
            datos = _get(i["url"], UA, 60)
        except Exception:
            continue
        caras = caras_en(datos)
        es_princ = bool(principal and t.endswith(principal.replace("_", " ")))
        pt = (3 if es_princ else 0) + (2 if len(caras) == 1 else -1 if len(caras) > 1 else -0.5)
        pt += 1 if caras and max(c[2] for c in caras) > 0.12 else 0
        pt += 1 if apellido in t.lower() else 0
        pt += 1 if min(i["w"], i["h"]) >= 1000 else 0
        cand.append(dict(i, caras=caras, puntaje=pt, bytes=datos, principal=es_princ))
    cand.sort(key=lambda c: -c["puntaje"])
    return cand[:n]


def guardar_persona(nombre, cands, carpeta):
    """Guarda los candidatos como <slug>.jpg, <slug>_2.jpg... y los anota en creditos.json (con la persona). Devuelve las rutas."""
    os.makedirs(carpeta, exist_ok=True)
    slug = nombre.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")):
        slug = slug.replace(a, b)
    slug = re.sub(r"[^a-z0-9]+", "_", slug).strip("_")
    cr = os.path.join(carpeta, "creditos.json")
    datos = json.load(open(cr, encoding="utf-8")) if os.path.exists(cr) else {}
    rutas = []
    for k, c in enumerate(cands):
        fn = f"{slug}.jpg" if k == 0 else f"{slug}_{k + 1}.jpg"
        ruta = os.path.join(carpeta, fn)
        open(ruta, "wb").write(c["bytes"])
        datos[fn] = dict(persona=nombre, titulo=c["titulo"], licencia=c["licencia"], autor=c["autor"], pagina=c["pagina"])
        rutas.append(ruta)
    json.dump(datos, open(cr, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return rutas


def creditos(raiz="."):
    """Bloque de créditos para la descripción de YouTube: imagenes/creditos.json (+ retratos/, fotos/) y clips/creditos_clips.json."""
    lineas = []
    for sub in ("imagenes", "retratos", "fotos"):
        ruta = os.path.join(raiz, sub, "creditos.json")
        if os.path.exists(ruta):
            for fn, d in json.load(open(ruta, encoding="utf-8")).items():
                quien = d.get("persona") or d.get("titulo", fn)
                lineas.append(f"- {quien}: foto de {d.get('autor') or 'autor desconocido'} · {d.get('licencia') or 'licencia libre'} · {d.get('pagina', '')}")
    ruta = os.path.join(raiz, "clips", "creditos_clips.json")
    if os.path.exists(ruta):
        for nom, d in json.load(open(ruta, encoding="utf-8")).items():
            lineas.append(f"- Video «{d.get('titulo') or nom}»: {d.get('autor', '')} · {d.get('licencia', '')} · {d.get('url', '')}")
    return "Créditos de imágenes y video:\n" + "\n".join(lineas) if lineas else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["commons", "bing", "archivo", "persona", "creditos"])
    ap.add_argument("consulta")
    ap.add_argument("n", nargs="?", type=int, default=8)
    ap.add_argument("--dir", default="imagenes")
    ap.add_argument("--ancho", type=int, default=2400)
    ap.add_argument("--descargar", action="store_true", help="guarda los resultados (si no, solo los lista)")
    a = ap.parse_args()
    if a.modo == "creditos":
        print(creditos(a.consulta))
        return
    if a.modo == "persona":
        cands = persona(a.consulta, a.n)
        for k, c in enumerate(cands):
            print(f"{k}: {c['titulo']} | {c['w']}x{c['h']} | {c['licencia']} | {c['autor'][:40]} | caras={len(c['caras'])} "
                  f"| puntaje={c['puntaje']:.1f}{' | PRINCIPAL' if c['principal'] else ''}")
        if not cands:
            print("sin candidatos libres: probar el nombre tal como está en Wikipedia o dejar una silueta dibujada")
        elif a.descargar:
            for r in guardar_persona(a.consulta, cands, a.dir):
                print("  ->", r)
        return
    if a.modo == "commons":
        for i in commons(a.consulta, a.n):
            print(f"{i['titulo']} | {i['w']}x{i['h']} | {i['licencia']} | {i['autor'][:50]}")
            if a.descargar:
                print("  ->", guardar_commons(i, a.dir))
    elif a.modo == "archivo":
        i = info_archivo(a.consulta, a.ancho)
        print(json.dumps(i, ensure_ascii=False, indent=1))
        if a.descargar and i:
            print("->", guardar_commons(i, a.dir))
    else:
        for k, (u, t) in enumerate(bing(a.consulta, a.n)):
            print(f"{k}: {u}  [{t[:60]}]")
            if a.descargar:
                try:
                    ext = os.path.splitext(urllib.parse.urlparse(u).path)[1] or ".jpg"
                    descargar(u, os.path.join(a.dir, f"bing_{_slug(a.consulta)}_{k}{ext}"))
                except Exception as e:
                    print("   fallo:", e)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
