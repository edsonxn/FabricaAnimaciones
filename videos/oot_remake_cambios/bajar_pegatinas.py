# -*- coding: utf-8 -*-
"""Pegatinas REALES de oot_remake_cambios (26-oct-2026; receta de majora_mask/bajar_pegatinas.py):
- copia de videos/zelda_oot/pegatinas las que ya existen (imágenes oficiales de zelda.fandom.com / Wikipedia),
- baja las nuevas (zelda.fandom.com API imageinfo; Wikipedia pageimages),
- recorta cuadros de los videos OFICIALES de Nintendo (amiibo, ocarina física, ZELDA NOTES, el tapiz) con ffmpeg a 1080p.
Fuentes en pegatinas/_fuentes.txt.
    python bajar_pegatinas.py
"""
import json
import os
import shutil
import subprocess
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
OOT = os.path.join(AQUI, "..", "zelda_oot", "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}

COPIAR = ["aonuma", "kondo", "link_nino", "navi", "n64", "ocarina", "epona", "botas_hierro", "skulltula", "mq_logo", "saria",
          "zelda_nina", "link_ocarina", "arbol_deku", "link_adulto", "malon"]
ZELDA = {
    "bolsa_adulto": ["OoT_Adult's_Wallet_Icon.png", "OoT3D_Adult's_Wallet_Icon.png"],
    "vendedor": ["OoT_Happy_Mask_Salesman_Artwork.png", "OoT3D_Happy_Mask_Salesman_Artwork.png"],
    "tirachinas": ["OoT3D_Fairy_Slingshot_Icon.png", "OoT_Fairy_Slingshot_Icon.png"],
    "arco": ["OoT3D_Fairy_Bow_Icon.png", "OoT_Fairy_Bow_Icon.png"],
    "gancho": ["OoT3D_Hookshot_Icon.png", "OoT_Hookshot_Icon.png"],
    "rupia": ["OoT_Green_Rupee_Model.png", "OoT3D_Green_Rupee_Model.png"],
    "mascara_keaton": ["OoT_Keaton_Mask_Icon.png", "OoT3D_Keaton_Mask_Icon.png"],
}
WIKI = {"oot3d": "The Legend of Zelda: Ocarina of Time 3D", "n3ds": "Nintendo 3DS", "switch2": "Nintendo Switch 2",
        "oot_n64": "The Legend of Zelda: Ocarina of Time"}
# cuadros de los videos oficiales: slug -> (id, segundo, recorte x0,y0,x1,y1 en fracción de 1920x1080)
CUADROS = {
    "amiibo": ("8v8eDMh1o3g", 264, (.25, .08, .75, .80)),
    "ocarina_fisica": ("PQvD3p2yGwc", 819, (.30, .20, .72, .95)),
    "zelda_notes": ("8v8eDMh1o3g", 251, (.18, .10, .98, .98)),
    "tapiz": ("r8eMoxo4ipE", 26, (.10, .05, .90, .80)),
    "hilos_menu": ("PQvD3p2yGwc", 578, (.0, .0, 1.0, 1.0)),
    "inventario": ("PQvD3p2yGwc", 112, (.0, .0, 1.0, 1.0)),
}


def _json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def _bajar(url, ruta):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(ruta, "wb") as f:
        f.write(r.read())


def zelda_url(nombre):
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", format="json"))
    for p in _json("https://zelda.fandom.com/api.php?" + q)["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]
    return None


def wiki_url(titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageimages", piprop="original", redirects=1, format="json"))
    for p in _json("https://en.wikipedia.org/w/api.php?" + q)["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]
    return None


def cuadro(slug, vid, t, rec):
    import cv2
    ruta = os.path.join(PEG, slug + ".jpg")
    if os.path.exists(ruta):
        return None
    tmp = os.path.join(PEG, "_c.mp4")
    subprocess.run(["yt-dlp", "-q", "-f", "bv*[height<=1080][height>=720]", "--download-sections", f"*{t}-{t + 1.5}",
                    "-o", tmp, "--force-overwrites", f"https://youtu.be/{vid}"], check=False)
    cap = cv2.VideoCapture(tmp)
    cap.set(cv2.CAP_PROP_POS_MSEC, 700)
    ok, f = cap.read()
    cap.release()
    os.remove(tmp)
    if not ok:
        return "sin cuadro"
    h, w = f.shape[:2]
    x0, y0, x1, y1 = rec
    cv2.imwrite(ruta, f[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)], [cv2.IMWRITE_JPEG_QUALITY, 92])
    return f"https://youtu.be/{vid}?t={t}"


def main():
    os.makedirs(PEG, exist_ok=True)
    fuentes = []
    for s in COPIAR:
        for e in (".png", ".jpg"):
            o = os.path.join(OOT, s + e)
            if os.path.exists(o) and not os.path.exists(os.path.join(PEG, s + e)):
                shutil.copy(o, os.path.join(PEG, s + e))
                fuentes.append(f"{s}\t(copiada de zelda_oot/pegatinas)")
    trabajos = [(s, ".png", lambda ns=ns: next((u for u in map(zelda_url, ns) if u), None)) for s, ns in ZELDA.items()]
    trabajos += [(s, ".jpg", lambda t=t: wiki_url(t)) for s, t in WIKI.items()]
    for slug, ext, buscar in trabajos:
        if any(os.path.exists(os.path.join(PEG, slug + e)) for e in (".png", ".jpg")):
            continue
        try:
            url = buscar()
            if not url:
                print("SIN IMAGEN", slug)
                continue
            e = ".png" if url.lower().split("?")[0].endswith(".png") else (".svg" if ".svg" in url.lower() else ext)
            _bajar(url, os.path.join(PEG, slug + e))
            fuentes.append(f"{slug}\t{url}")
            print("ok", slug)
        except Exception as ex:                       # noqa: BLE001
            print("ERROR", slug, ex)
    for slug, (vid, t, rec) in CUADROS.items():
        r = cuadro(slug, vid, t, rec)
        if r and r.startswith("http"):
            fuentes.append(f"{slug}\t{r} (cuadro del video oficial)")
            print("ok", slug)
        elif r:
            print("ERROR", slug, r)
    with open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8") as f:
        f.write("\n".join(fuentes) + ("\n" if fuentes else ""))


if __name__ == "__main__":
    main()
