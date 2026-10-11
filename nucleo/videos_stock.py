# -*- coding: utf-8 -*-
"""Video de apoyo (b-roll) para documentales: Pexels y Pixabay (licencia gratuita, uso comercial) y, como respaldo, yt-dlp.

Las claves NO se copian a este proyecto: se leen en tiempo de ejecución de PEXELS_API_KEY / PIXABAY_API_KEY (variables de entorno o el
.env de C:\\googleimagenes). Nunca se imprimen.

Uso:
  python videos_stock.py buscar "old book pages turning" [n]        lista candidatos de Pexels+Pixabay (id, duración, tamaño, autor, url)
  python videos_stock.py bajar pexels 123456 nombre --dir clips      descarga el archivo HD más cercano a 1920x1080 y anota creditos_clips.json
  python videos_stock.py miniaturas "candle flame" 6 --dir clips/_m  baja las miniaturas de la búsqueda para elegir a ojo
  python videos_stock.py yt "consulta" [n]                           (respaldo) busca en YouTube videos con licencia Creative Commons
  python videos_stock.py ytbuscar "Sam Altman interview" [n]         busca en YouTube (id, duración, canal, título, url) para elegir un extracto
  python videos_stock.py ytbajar <url> nombre --desde 1:10 --hasta 1:22 --dir clips
                                                                     baja SOLO ese tramo (<=720p, sin audio salvo --audio) a clips/<nombre>.mp4 y
                                                                     anota url, canal y tramo en creditos_clips.json
                                                                     (si YouTube pide verificación anti-bot: --cookies chrome|edge|firefox|<cookies.txt>,
                                                                      que usa la sesión del usuario: preguntarle antes)
Todo lo que baja aquí se pinta en B/N de tinta con noir.clip_noir / noir_real.clip_real (docs/estilo_noir.md § «Medios reales»).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "FabricaAnimaciones/1.0 (jairedson5@gmail.com)"}
ENV_EXTRA = r"C:\googleimagenes\.env"


def clave(nombre):
    v = os.environ.get(nombre)
    if v:
        return v.strip()
    try:
        for ln in open(ENV_EXTRA, encoding="utf-8", errors="ignore"):
            m = re.match(rf"\s*{nombre}\s*=\s*(.+?)\s*$", ln)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    except OSError:
        pass
    return None


def _json(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())


def pexels(consulta, n=8, orientacion="landscape"):
    k = clave("PEXELS_API_KEY")
    if not k:
        return []
    d = _json("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        dict(query=consulta, per_page=n, orientation=orientacion, size="medium")), {"Authorization": k})
    out = []
    for v in d.get("videos", []):
        archivos = [f for f in v["video_files"] if f.get("file_type") == "video/mp4" and f.get("width")]
        out.append(dict(fuente="pexels", id=v["id"], dur=v["duration"], w=v["width"], h=v["height"], autor=v["user"]["name"],
                        url=v["url"], miniatura=v.get("image"), archivos=[dict(w=f["width"], h=f["height"], fps=f.get("fps"), link=f["link"]) for f in archivos]))
    return out


def pixabay(consulta, n=8):
    k = clave("PIXABAY_API_KEY")
    if not k:
        return []
    d = _json("https://pixabay.com/api/videos/?" + urllib.parse.urlencode(dict(key=k, q=consulta, per_page=max(3, n), video_type="film")))
    out = []
    for v in d.get("hits", []):
        vs = v["videos"]
        archivos = [dict(w=x["width"], h=x["height"], fps=None, link=x["url"]) for x in vs.values() if x.get("url")]
        out.append(dict(fuente="pixabay", id=v["id"], dur=v["duration"], w=max(a["w"] for a in archivos), h=max(a["h"] for a in archivos),
                        autor=v["user"], url=v["pageURL"], miniatura=vs.get("tiny", {}).get("thumbnail") or v.get("picture_id"), archivos=archivos))
    return out


def buscar(consulta, n=8):
    return pexels(consulta, n) + pixabay(consulta, n)


def elegir_archivo(v, ancho=1920):
    """El archivo cuyo ancho se acerca más a `ancho` sin bajar de 1280 si es posible."""
    a = sorted(v["archivos"], key=lambda f: (abs(f["w"] - ancho) if f["w"] >= 1280 else 10000 + abs(f["w"] - ancho)))
    return a[0]


def descargar(v, destino):
    f = elegir_archivo(v)
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    req = urllib.request.Request(f["link"], headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(destino, "wb") as o:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            o.write(b)
    return f


def anotar(carpeta, nombre, v, f):
    ruta = os.path.join(carpeta, "creditos_clips.json")
    datos = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    datos[nombre] = dict(fuente=v["fuente"], id=v["id"], autor=v["autor"], url=v["url"], resolucion=f"{f['w']}x{f['h']}", licencia="Pexels License" if v["fuente"] == "pexels" else "Pixabay Content License")
    json.dump(datos, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def yt_cc(consulta, n=6):
    """Respaldo: busca en YouTube con licencia Creative Commons (yt-dlp). Devuelve lista de (id, titulo, duración, canal)."""
    cmd = ["yt-dlp", f"ytsearch{n * 4}:{consulta}", "--dump-json", "--no-download", "--flat-playlist"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    vistos = []
    for ln in r.stdout.splitlines():
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        vistos.append((d.get("id"), d.get("title"), d.get("duration"), d.get("channel")))
    return vistos[:n * 4]


def _yt(args, **k):
    return subprocess.run([sys.executable, "-m", "yt_dlp", *args], capture_output=True, text=True, encoding="utf-8", errors="ignore", **k)


def yt_buscar(consulta, n=8):
    """Busca en YouTube (yt-dlp, sin descargar). Devuelve dicts: id, titulo, dur (s), canal, url. Ordenados como YouTube."""
    r = _yt([f"ytsearch{n}:{consulta}", "--dump-json", "--no-download", "--flat-playlist"])
    out = []
    for ln in r.stdout.splitlines():
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        out.append(dict(id=d.get("id"), titulo=d.get("title"), dur=d.get("duration"), canal=d.get("channel") or d.get("uploader"),
                        url=d.get("url") or f"https://www.youtube.com/watch?v={d.get('id')}"))
    return out


def _cookies(cookies):
    """--cookies: ruta a un cookies.txt, o el nombre de un navegador (chrome, edge, firefox) para usar su sesión de YouTube."""
    if not cookies:
        return []
    return ["--cookies", cookies] if os.path.isfile(cookies) else ["--cookies-from-browser", cookies]


def _error_yt(r):
    txt = (r.stderr or r.stdout or "")[-700:]
    if "not a bot" in txt or "429" in txt or "Sign in" in txt:
        txt = ("YouTube pide verificación anti-bot para bajar este video (bloqueo temporal de la IP).\n"
               "  1) reintentar más tarde; 2) o pasar --cookies chrome|edge|firefox|<cookies.txt> (usa la sesión del navegador del usuario:\n"
               "     PREGUNTARLE antes); 3) o cambiar de fuente: Pexels/Pixabay (videos_stock.py buscar/bajar).\n") + txt
    return txt


def yt_bajar(url, nombre, carpeta="clips", desde=None, hasta=None, alto=720, audio=False, cookies=None):
    """Baja un extracto (desde..hasta, en 'm:ss' o 'h:mm:ss'; sin tramo = el video entero, ¡cuidado con el peso!) de un video de YouTube
    a <carpeta>/<nombre>.mp4 con yt-dlp + ffmpeg, <= `alto` px. Anota en creditos_clips.json la url, el canal y el tramo. Devuelve la ruta."""
    r = _yt(["--dump-single-json", "--no-download", "--no-playlist", *_cookies(cookies), url])
    try:
        meta = json.loads(r.stdout)
    except ValueError:
        raise SystemExit("yt-dlp no pudo leer el video:\n" + _error_yt(r))
    os.makedirs(carpeta, exist_ok=True)
    destino = os.path.join(carpeta, nombre + ".mp4")
    fmt = (f"bv*[height<={alto}][ext=mp4]+ba[ext=m4a]/b[height<={alto}][ext=mp4]/b[height<={alto}]" if audio
           else f"bv*[height<={alto}][ext=mp4]/bv*[height<={alto}]/b[height<={alto}]")
    cmd = ["-f", fmt, "--no-playlist", "--merge-output-format", "mp4", "-o", os.path.join(carpeta, nombre + ".%(ext)s"), "--force-overwrites"]
    if desde or hasta:
        cmd += ["--download-sections", f"*{desde or '0'}-{hasta or 'inf'}", "--force-keyframes-at-cuts"]
    r = _yt(cmd + _cookies(cookies) + [url])
    if not os.path.exists(destino):
        crudo = [f for f in os.listdir(carpeta) if f.startswith(nombre + ".") and not f.endswith((".part", ".ytdl", ".json"))]
        if not crudo:
            raise SystemExit("no se bajó nada:\n" + _error_yt(r))
        # yt-dlp dejó otro contenedor (webm...): a mp4 para que noir/docu_fx.Clip lo abra
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(carpeta, crudo[0]), "-c:v", "libx264", "-crf", "20",
                        *(["-c:a", "aac"] if audio else ["-an"]), destino], check=False)
        if os.path.exists(destino):
            os.remove(os.path.join(carpeta, crudo[0]))
    ruta = os.path.join(carpeta, "creditos_clips.json")
    datos = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    datos[nombre] = dict(fuente=str(meta.get("extractor_key") or "youtube").lower(), id=meta.get("id"), autor=meta.get("channel") or meta.get("uploader"), titulo=meta.get("title"),
                         url=meta.get("webpage_url") or url, tramo=f"{desde or '0'}-{hasta or 'fin'}",
                         licencia=meta.get("license") or "YouTube: extracto corto transformado a tinta, con crédito")
    json.dump(datos, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return destino


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["buscar", "bajar", "miniaturas", "yt", "ytbuscar", "ytbajar"])
    ap.add_argument("a", nargs="?")
    ap.add_argument("b", nargs="?")
    ap.add_argument("c", nargs="?")
    ap.add_argument("--dir", default="clips")
    ap.add_argument("--desde", default=None, help="ytbajar: inicio del tramo (m:ss)")
    ap.add_argument("--hasta", default=None, help="ytbajar: fin del tramo (m:ss)")
    ap.add_argument("--alto", type=int, default=720, help="ytbajar: altura máxima")
    ap.add_argument("--audio", action="store_true", help="ytbajar: conserva el audio (por defecto solo imagen)")
    ap.add_argument("--cookies", default=None, help="ytbajar: navegador (chrome|edge|firefox) o cookies.txt si YouTube pide verificación")
    x = ap.parse_args()
    if x.modo == "ytbuscar":
        for v in yt_buscar(x.a, int(x.b or 8)):
            d = int(v["dur"] or 0)
            print(f"{v['id']}  {d // 60}:{d % 60:02d}  {str(v['canal'])[:22]:22s} {str(v['titulo'])[:70]}  {v['url']}")
        return
    if x.modo == "ytbajar":
        print("ok", yt_bajar(x.a, x.b, x.dir, x.desde, x.hasta, x.alto, x.audio, x.cookies))
        return
    if x.modo == "buscar":
        for v in buscar(x.a, int(x.b or 6)):
            f = elegir_archivo(v)
            print(f"{v['fuente']:8s} {v['id']:>10} {v['dur']:>3}s {v['w']}x{v['h']}  {v['autor'][:22]:22s} {v['url']}")
    elif x.modo == "miniaturas":
        os.makedirs(x.dir, exist_ok=True)
        for v in buscar(x.a, int(x.b or 6)):
            if v.get("miniatura"):
                try:
                    req = urllib.request.Request(v["miniatura"], headers=UA)
                    open(os.path.join(x.dir, f"{v['fuente']}_{v['id']}.jpg"), "wb").write(urllib.request.urlopen(req, timeout=30).read())
                    print(v["fuente"], v["id"], v["dur"], "s", v["w"], "x", v["h"])
                except Exception as e:
                    print("fallo miniatura", v["id"], e)
    elif x.modo == "bajar":
        fuente, vid, nombre = x.a, x.b, x.c
        cand = [v for v in buscar_id(fuente, vid)]
        if not cand:
            sys.exit("no encontrado")
        v = cand[0]
        f = descargar(v, os.path.join(x.dir, nombre + ".mp4"))
        anotar(x.dir, nombre, v, f)
        print("ok", nombre, f["w"], "x", f["h"])
    else:
        for i in yt_cc(x.a, int(x.b or 6)):
            print(i)


def buscar_id(fuente, vid):
    if fuente == "pexels":
        k = clave("PEXELS_API_KEY")
        v = _json(f"https://api.pexels.com/videos/videos/{vid}", {"Authorization": k})
        archivos = [dict(w=f["width"], h=f["height"], fps=f.get("fps"), link=f["link"]) for f in v["video_files"] if f.get("file_type") == "video/mp4" and f.get("width")]
        return [dict(fuente="pexels", id=v["id"], dur=v["duration"], w=v["width"], h=v["height"], autor=v["user"]["name"], url=v["url"], archivos=archivos)]
    k = clave("PIXABAY_API_KEY")
    d = _json("https://pixabay.com/api/videos/?" + urllib.parse.urlencode(dict(key=k, id=vid)))
    out = []
    for v in d.get("hits", []):
        archivos = [dict(w=x["width"], h=x["height"], fps=None, link=x["url"]) for x in v["videos"].values() if x.get("url")]
        out.append(dict(fuente="pixabay", id=v["id"], dur=v["duration"], w=max(a["w"] for a in archivos), h=max(a["h"] for a in archivos), autor=v["user"], url=v["pageURL"], archivos=archivos))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
