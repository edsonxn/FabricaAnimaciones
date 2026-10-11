# -*- coding: utf-8 -*-
"""Busca retratos en Wikimedia Commons (dominio público): python _buscar_retratos.py "consulta" [n]"""
import json, re, sys, urllib.parse, urllib.request
UA = {"User-Agent": "FabricaAnimaciones/1.0 (proyecto educativo de videos de historia; contacto local)"}
def api(**p):
    p["format"] = "json"
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))
def buscar(q, n=8):
    d = api(action="query", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=n, prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=300)
    out = []
    for pg in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (pg.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "?")
        out.append((pg["title"], ii.get("width"), ii.get("height"), lic, ii.get("url")))
    return out
if __name__ == "__main__":
    for t, w, h, lic, u in buscar(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8):
        print(f"{t} | {w}x{h} | {lic}")
