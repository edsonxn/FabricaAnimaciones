# -*- coding: utf-8 -*-
"""Conexión con YouTube (Data API v3) — portado de RemoGravity/scripts/youtube_manager.js a Python, sin
dependencias extra (solo requests).

Credenciales:
  - Cliente OAuth: canales/youtube_client_secrets.json (o la ruta en FAB_YT_SECRETS).
  - Tokens por canal: canales/tokens/youtube_tokens_<UC...>.json (mismo formato que RemoGravity/googleimagenes:
    access_token, refresh_token, scope, token_type, expiry_date en ms). Si no existe ahí, se busca en las carpetas
    de EXTERNOS; al renovarse, el token se guarda en canales/tokens (el original no se toca).
  - Un canal se nombra por su ID (UC...) o por el nombre de su archivo en canales/ (p. ej. just_homo_sapiens).

Uso (desde C:\\FabricaAnimaciones):
  python fab.py yt conectar [puerto]              abre el navegador para autorizar un canal (el usuario inicia sesión)
  python fab.py yt canales                        canales conectados y su estado
  python fab.py yt videos <canal>                 últimos videos del canal (incluye privados/borradores)
  python fab.py yt metricas <canal> [dias]        radiografía del canal (Analytics) -> canales/metricas/*.json
  python fab.py yt canal <canal>                  aplica canales/<canal>.json: descripción, palabras clave, idioma,
                                                  país y banner (el nombre y la foto de perfil solo se cambian en Studio)
  python fab.py yt aplicar <video> <canal> <id>   aplica videos/<video>/youtube.json a un video ya subido
  python fab.py yt subir <video> <canal> [private|unlisted|public] [--publicar 2026-10-01T15:00:00Z]
  python fab.py yt publicar <canal> <id> [public|unlisted|private] [--programar 2026-10-01T15:00:00Z]
"""
import glob
import http.server
import json
import os
import sys
import threading
import time
import urllib.parse
import webbrowser

import requests

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANALES = os.path.join(RAIZ, "canales")
TOKENS = os.path.join(CANALES, "tokens")
EXTERNOS = ["C:/googleimagenes", os.path.expanduser("~/OneDrive/Documents/RemoGravity")]
SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/yt-analytics.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl"]      # force-ssl: necesario para subir subtítulos
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"


# ---------------------------------------------------------------- credenciales
def secretos():
    rutas = [os.environ.get("FAB_YT_SECRETS"), os.path.join(CANALES, "youtube_client_secrets.json")]
    for r in rutas:
        if r and os.path.isfile(r):
            d = json.load(open(r, encoding="utf-8"))
            c = d.get("installed") or d.get("web") or {}
            return c["client_id"], c["client_secret"]
    sys.exit("Falta canales/youtube_client_secrets.json (cliente OAuth de Google Cloud).")


def resolver_canal(canal):
    """UC... o alias (nombre de un canales/<alias>.json con 'canal_id')."""
    if canal.startswith("UC"):
        return canal
    ruta = os.path.join(CANALES, canal + ".json")
    if os.path.isfile(ruta):
        return json.load(open(ruta, encoding="utf-8"))["canal_id"]
    sys.exit(f"Canal desconocido '{canal}': usa su ID (UC...) o crea canales/{canal}.json")


def ruta_token(cid):
    propio = os.path.join(TOKENS, f"youtube_tokens_{cid}.json")
    if os.path.isfile(propio):
        return propio
    for d in EXTERNOS:
        r = os.path.join(d, f"youtube_tokens_{cid}.json")
        if os.path.isfile(r):
            return r
    sys.exit(f"No hay token para {cid}. Conéctalo con: python fab.py yt conectar")


def guardar_token(cid, tok):
    os.makedirs(TOKENS, exist_ok=True)
    json.dump(tok, open(os.path.join(TOKENS, f"youtube_tokens_{cid}.json"), "w", encoding="utf-8"), indent=2)


def access_token(cid):
    tok = json.load(open(ruta_token(cid), encoding="utf-8"))
    if tok.get("expiry_date", 0) / 1000 - time.time() > 90:
        return tok["access_token"]
    if not tok.get("refresh_token"):
        sys.exit(f"El token de {cid} caducó y no tiene refresh_token: vuelve a conectar el canal.")
    cid_oauth, secreto = secretos()
    r = requests.post("https://oauth2.googleapis.com/token", data=dict(
        client_id=cid_oauth, client_secret=secreto, refresh_token=tok["refresh_token"], grant_type="refresh_token"))
    if r.status_code != 200:
        err = r.json().get("error", r.text)
        sys.exit(f"No se pudo renovar el token de {cid} ({err}). Si el token lo creó otra app (otro cliente OAuth), "
                 "reconecta el canal con: python fab.py yt conectar")
    nuevo = r.json()
    tok.update(access_token=nuevo["access_token"], expiry_date=int((time.time() + nuevo["expires_in"]) * 1000),
               token_type=nuevo.get("token_type", "Bearer"))
    if "scope" in nuevo:
        tok["scope"] = nuevo["scope"]
    guardar_token(cid, tok)
    return tok["access_token"]


def api(cid, metodo, ruta, base=API, **kw):
    h = kw.pop("headers", {})
    h["Authorization"] = "Bearer " + access_token(cid)
    r = requests.request(metodo, base + ruta, headers=h, timeout=kw.pop("timeout", 120), **kw)
    if r.status_code >= 400:
        try:
            msg = r.json()["error"]["message"]
        except Exception:
            msg = r.text[:400]
        raise RuntimeError(f"YouTube API {metodo} {ruta}: HTTP {r.status_code}: {msg}")
    return r.json() if r.content else {}


# ---------------------------------------------------------------- conectar (OAuth local)
def conectar(puerto=3000):
    cid_oauth, secreto = secretos()
    redirect = f"http://localhost:{puerto}/oauth2callback"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(dict(
        client_id=cid_oauth, redirect_uri=redirect, response_type="code", scope=" ".join(SCOPES),
        access_type="offline", prompt="consent select_account"))
    listo = threading.Event()

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            q = urllib.parse.urlparse(self.path)
            if q.path != "/oauth2callback":
                self.send_response(302)
                self.send_header("Location", url)
                self.end_headers()
                return
            code = urllib.parse.parse_qs(q.query).get("code", [None])[0]
            if not code:
                self._html("<h2>Falta el código de autorización.</h2>")
                return
            r = requests.post("https://oauth2.googleapis.com/token", data=dict(
                code=code, client_id=cid_oauth, client_secret=secreto, redirect_uri=redirect,
                grant_type="authorization_code"))
            if r.status_code != 200:
                self._html(f"<h2>Error obteniendo el token: {r.text[:300]}</h2>")
                return
            t = r.json()
            tok = dict(access_token=t["access_token"], refresh_token=t.get("refresh_token"), scope=t.get("scope"),
                       token_type=t.get("token_type", "Bearer"),
                       expiry_date=int((time.time() + t["expires_in"]) * 1000))
            ch = requests.get(API + "/channels", params=dict(part="snippet", mine="true"),
                              headers={"Authorization": "Bearer " + tok["access_token"]}).json()
            item = (ch.get("items") or [{}])[0]
            chid, nombre = item.get("id", "main"), item.get("snippet", {}).get("title", "Canal")
            guardar_token(chid, tok)
            print(f"Conectado: {nombre} ({chid}) -> canales/tokens/youtube_tokens_{chid}.json")
            self._html(f"<h2>&#9989; {nombre} conectado</h2><p>Ya puedes cerrar esta ventana.</p>")
            listo.set()

        def _html(self, cuerpo):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<html><body style='font-family:sans-serif;padding:40px'>{cuerpo}</body></html>".encode())

    srv = http.server.HTTPServer(("localhost", puerto), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"Abre este enlace, elige la cuenta y el canal, y acepta los permisos:\n  http://localhost:{puerto}/auth")
    webbrowser.open(f"http://localhost:{puerto}/auth")
    listo.wait()
    srv.shutdown()


# ---------------------------------------------------------------- consultas
def ids_con_token():
    """Canales de este proyecto: tokens propios + los que tienen su canales/<alias>.json (no toca otros canales)."""
    ids = {os.path.basename(f)[len("youtube_tokens_"):-5] for f in glob.glob(os.path.join(TOKENS, "youtube_tokens_UC*.json"))}
    for f in glob.glob(os.path.join(CANALES, "*.json")):
        try:
            ids.add(json.load(open(f, encoding="utf-8"))["canal_id"])
        except (KeyError, ValueError, TypeError):
            pass
    return sorted(ids)


def canales():
    for cid in ids_con_token():
        try:
            it = api(cid, "GET", "/channels", params=dict(part="snippet,statistics,brandingSettings", id=cid))["items"][0]
            idioma = it.get("brandingSettings", {}).get("channel", {}).get("defaultLanguage", "-")
            print(f"OK   {cid}  {it['snippet']['title']}  subs={it['statistics'].get('subscriberCount')}  idioma={idioma}")
        except (RuntimeError, SystemExit) as e:
            print(f"--   {cid}  {e}")


def videos(cid, n=25):
    up = api(cid, "GET", "/channels", params=dict(part="contentDetails", id=cid))["items"][0]
    pl = up["contentDetails"]["relatedPlaylists"]["uploads"]
    items = api(cid, "GET", "/playlistItems", params=dict(part="contentDetails", playlistId=pl, maxResults=n)).get("items", [])
    ids = [i["contentDetails"]["videoId"] for i in items]
    if not ids:
        print("(sin videos)")
        return []
    vs = api(cid, "GET", "/videos", params=dict(part="snippet,status,contentDetails", id=",".join(ids))).get("items", [])
    for v in vs:
        st = v["status"]
        print(f"{v['id']}  {st['privacyStatus']:8s} {st.get('uploadStatus', ''):9s} {v['contentDetails'].get('duration', '')}"
              f"  {v['snippet']['title']}")
    return vs


# ---------------------------------------------------------------- escritura
def _branding(cid):
    it = api(cid, "GET", "/channels", params=dict(part="brandingSettings", id=cid))["items"][0]
    return it.get("brandingSettings", {})


def configurar_canal(cid, cfg):
    """channels.update exige el brandingSettings completo: se lee el actual y se combina."""
    b = _branding(cid)
    ch = b.setdefault("channel", {})
    if cfg.get("descripcion") is not None:
        ch["description"] = cfg["descripcion"]
    if cfg.get("palabras_clave"):
        ch["keywords"] = " ".join(f'"{k}"' if " " in k else k for k in cfg["palabras_clave"])
    if cfg.get("idioma"):
        ch["defaultLanguage"] = cfg["idioma"]
    if cfg.get("pais"):
        ch["country"] = cfg["pais"]
    if cfg.get("banner"):
        ruta = cfg["banner"] if os.path.isabs(cfg["banner"]) else os.path.join(RAIZ, cfg["banner"])
        r = api(cid, "POST", "/channelBanners/insert", base=UPLOAD, params=dict(uploadType="media"),
                data=open(ruta, "rb").read(), headers={"Content-Type": "image/jpeg"})
        b.setdefault("image", {})["bannerExternalUrl"] = r["url"]
        print("banner subido")
    api(cid, "PUT", "/channels", params=dict(part="brandingSettings"), json=dict(id=cid, brandingSettings=b))
    print("canal actualizado: descripción, palabras clave, idioma" + (", país" if cfg.get("pais") else ""))


def _meta(carpeta):
    return json.load(open(os.path.join(carpeta, "youtube.json"), encoding="utf-8"))


def _snippet(m, previo=None):
    s = dict(previo or {})
    s.update(title=m["titulo"], description=m["descripcion"], tags=m.get("etiquetas", []),
             categoryId=str(m.get("categoria", 27)), defaultLanguage=m.get("idioma", "es"),
             defaultAudioLanguage=m.get("idioma_audio", m.get("idioma", "es")))
    for k in ("thumbnails", "localized", "channelTitle", "publishedAt", "channelId", "liveBroadcastContent"):
        s.pop(k, None)
    return s


def miniatura_y_subtitulos(cid, vid, carpeta, m):
    if m.get("miniatura"):
        ruta = os.path.join(carpeta, m["miniatura"])
        tipo = "image/png" if ruta.endswith(".png") else "image/jpeg"
        api(cid, "POST", "/thumbnails/set", base=UPLOAD, params=dict(videoId=vid, uploadType="media"),
            data=open(ruta, "rb").read(), headers={"Content-Type": tipo})
        print("miniatura aplicada:", os.path.basename(ruta))
    if m.get("subtitulos"):
        try:
            existentes = api(cid, "GET", "/captions", params=dict(part="snippet", videoId=vid)).get("items", [])
        except RuntimeError as e:
            if "scope" not in str(e):
                raise
            print("subtítulos NO cargados: el token no tiene el permiso youtube.force-ssl. Reconecta el canal con "
                  "'python fab.py yt conectar' o sube el .srt a mano en Studio > Subtítulos.")
            return
        if any(c["snippet"]["language"].startswith(m.get("idioma", "es")) and c["snippet"].get("trackKind") != "asr"
               for c in existentes):
            print("subtítulos ya cargados (se dejan como están)")
            return
        meta = json.dumps(dict(snippet=dict(videoId=vid, language=m.get("idioma", "es"), name="Español")))
        srt = open(os.path.join(carpeta, m["subtitulos"], ), "rb").read()
        limite = "fab_limite_7c1"
        cuerpo = (f"--{limite}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n"
                  f"--{limite}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + srt + f"\r\n--{limite}--".encode()
        api(cid, "POST", "/captions", base=UPLOAD, params=dict(part="snippet", uploadType="multipart"),
            data=cuerpo, headers={"Content-Type": f"multipart/related; boundary={limite}"})
        print("subtítulos .srt cargados")


def aplicar(carpeta, cid, vid):
    """Actualiza título, descripción, etiquetas, categoría e idioma de un video existente (no cambia su visibilidad)."""
    m = _meta(carpeta)
    v = api(cid, "GET", "/videos", params=dict(part="snippet,status", id=vid))["items"][0]
    st = {k: v["status"][k] for k in ("privacyStatus", "embeddable", "license", "publicStatsViewable", "publishAt")
          if k in v["status"]}
    st["selfDeclaredMadeForKids"] = bool(m.get("para_ninos", False))
    api(cid, "PUT", "/videos", params=dict(part="snippet,status"),
        json=dict(id=vid, snippet=_snippet(m, v["snippet"]), status=st))
    print(f"metadatos aplicados a {vid} (visibilidad: {st['privacyStatus']})")
    miniatura_y_subtitulos(cid, vid, carpeta, m)


def _reporte(cid, desde, hasta, **p):
    """YouTube Analytics v2 (scope yt-analytics.readonly). Devuelve lista de dicts; [] si no hay datos."""
    p.update(ids="channel==MINE", startDate=desde, endDate=hasta)
    r = requests.get("https://youtubeanalytics.googleapis.com/v2/reports", params=p,
                     headers={"Authorization": "Bearer " + access_token(cid)}, timeout=60)
    d = r.json()
    if "error" in d:
        return [{"error": d["error"].get("message", "")}]
    cols = [h["name"] for h in d.get("columnHeaders", [])]
    return [dict(zip(cols, fila)) for fila in d.get("rows", [])]


def metricas(cid, alias=None, dias=28):
    """Radiografía del canal para decidir qué cambiar: totales, por video (con retención), tráfico, dispositivos,
    países y edades. Guarda una copia en canales/metricas/ para comparar con el tiempo.
    Los datos de Analytics llegan con 2-3 días de retraso."""
    import datetime as dt
    hoy = dt.date.today()
    hasta = hoy.isoformat()
    desde = (hoy - dt.timedelta(days=dias)).isoformat()
    ch = api(cid, "GET", "/channels", params=dict(part="snippet,statistics,contentDetails", id=cid))["items"][0]
    out = dict(fecha=hasta, canal=ch["snippet"]["title"], estadisticas=ch["statistics"], ventana_dias=dias)
    met = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares"
    out["totales_ventana"] = _reporte(cid, desde, hasta, metrics=met)
    out["totales_historicos"] = _reporte(cid, "2015-01-01", hasta, metrics=met)
    out["trafico"] = _reporte(cid, desde, hasta, metrics="views,estimatedMinutesWatched",
                              dimensions="insightTrafficSourceType", sort="-views")
    out["busquedas"] = _reporte(cid, desde, hasta, metrics="views", dimensions="insightTrafficSourceDetail",
                                filters="insightTrafficSourceType==YT_SEARCH", sort="-views", maxResults=15)
    out["dispositivos"] = _reporte(cid, desde, hasta, metrics="views", dimensions="deviceType", sort="-views")
    out["paises"] = _reporte(cid, desde, hasta, metrics="views,averageViewPercentage", dimensions="country",
                             sort="-views", maxResults=10)
    out["edad_genero"] = _reporte(cid, desde, hasta, metrics="viewerPercentage", dimensions="ageGroup,gender")
    # por video: datos públicos (Data API) + analytics y curva de retención de cada uno
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = api(cid, "GET", "/playlistItems", params=dict(part="contentDetails", playlistId=pl, maxResults=15)).get("items", [])
    ids = [i["contentDetails"]["videoId"] for i in items]
    vids = api(cid, "GET", "/videos", params=dict(part="snippet,status,statistics,contentDetails", id=",".join(ids))).get("items", []) if ids else []
    out["videos"] = []
    for v in vids:
        fila = dict(id=v["id"], titulo=v["snippet"]["title"], estado=v["status"]["privacyStatus"],
                    publicado=v["snippet"].get("publishedAt"), programado=v["status"].get("publishAt"),
                    duracion=v["contentDetails"]["duration"], stats=v.get("statistics", {}))
        if v["status"]["privacyStatus"] == "public":
            a = _reporte(cid, v["snippet"]["publishedAt"][:10], hasta, metrics=met, filters=f"video=={v['id']}")
            fila["analytics"] = a[0] if a else {}
            ret = _reporte(cid, v["snippet"]["publishedAt"][:10], hasta, metrics="audienceWatchRatio",
                           dimensions="elapsedVideoTimeRatio", filters=f"video=={v['id']}")
            fila["retencion"] = {f"{r['elapsedVideoTimeRatio']:.2f}": round(r["audienceWatchRatio"], 3)
                                 for r in ret if "elapsedVideoTimeRatio" in r and int(round(r["elapsedVideoTimeRatio"] * 100)) % 10 == 0}
        out["videos"].append(fila)
    os.makedirs(os.path.join(CANALES, "metricas"), exist_ok=True)
    ruta = os.path.join(CANALES, "metricas", f"{alias or cid}_{hasta}.json")
    json.dump(out, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # resumen legible
    s = out["estadisticas"]
    print(f"== {out['canal']}  suscriptores={s.get('subscriberCount')}  vistas={s.get('viewCount')}  videos={s.get('videoCount')}")
    for nombre in ("totales_ventana", "totales_historicos"):
        print(f"-- {nombre}: {out[nombre][0] if out[nombre] else 'sin datos'}")
    for nombre in ("trafico", "busquedas", "dispositivos", "paises", "edad_genero"):
        filas = out[nombre]
        print(f"-- {nombre}: " + ("sin datos (canal pequeño o sin vistas en la ventana)" if not filas else
                                  "; ".join(" ".join(str(x) for x in f.values()) for f in filas[:10])))
    for v in out["videos"]:
        a = v.get("analytics", {})
        print(f"-- {v['estado']:8s} {v['titulo'][:55]:55s} vistas={v['stats'].get('viewCount', '-')} "
              f"likes={v['stats'].get('likeCount', '-')} %visto={a.get('averageViewPercentage', '-')} "
              f"dur_media={a.get('averageViewDuration', '-')}s" + (f" programado={v['programado']}" if v.get("programado") else ""))
        if v.get("retencion"):
            print("     retención (fracción del video: audiencia relativa):", v["retencion"])
    print("guardado:", os.path.relpath(ruta, RAIZ))
    return out


def cambiar_visibilidad(cid, vid, privacidad="public", publicar=None):
    """Hace público (o no listado / privado) un video ya subido, o lo programa con publicar=ISO (UTC)."""
    v = api(cid, "GET", "/videos", params=dict(part="status", id=vid))["items"][0]
    st = {k: v["status"][k] for k in ("embeddable", "license", "publicStatsViewable", "selfDeclaredMadeForKids")
          if k in v["status"]}
    st.setdefault("selfDeclaredMadeForKids", v["status"].get("madeForKids", False))
    st["privacyStatus"] = "private" if publicar else privacidad
    if publicar:
        st["publishAt"] = publicar
    r = api(cid, "PUT", "/videos", params=dict(part="status"), json=dict(id=vid, status=st))
    print(f"{vid}: {r['status']['privacyStatus']}" + (f", se publica {publicar}" if publicar else "")
          + f"  https://youtu.be/{vid}")


def subir(carpeta, cid, privacidad="private", publicar=None):
    m = _meta(carpeta)
    video = glob.glob(os.path.join(carpeta, "salida", "*_MASTER.mp4"))[0]
    status = dict(privacyStatus="private" if publicar else privacidad, selfDeclaredMadeForKids=bool(m.get("para_ninos")),
                  embeddable=True, publicStatsViewable=True)
    if publicar:
        status["publishAt"] = publicar
    tam = os.path.getsize(video)
    ini = requests.post(UPLOAD + "/videos", params=dict(uploadType="resumable", part="snippet,status"),
                        headers={"Authorization": "Bearer " + access_token(cid),
                                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)},
                        json=dict(snippet=_snippet(m), status=status))
    if ini.status_code != 200:
        raise RuntimeError(f"No se pudo iniciar la subida: {ini.text[:400]}")
    destino, pos, TROZO = ini.headers["Location"], 0, 32 * 1024 * 1024
    with open(video, "rb") as f:
        while pos < tam:
            f.seek(pos)
            datos = f.read(TROZO)
            r = requests.put(destino, data=datos, headers={
                "Authorization": "Bearer " + access_token(cid),
                "Content-Range": f"bytes {pos}-{pos + len(datos) - 1}/{tam}"}, timeout=600)
            if r.status_code in (200, 201):
                vid = r.json()["id"]
                break
            if r.status_code != 308:
                raise RuntimeError(f"Subida interrumpida (HTTP {r.status_code}): {r.text[:300]} — vuelve a intentar")
            pos = int(r.headers["Range"].split("-")[1]) + 1 if "Range" in r.headers else pos
            print(f"  subido {pos / tam:5.1%}", flush=True)
    print(f"video subido: https://youtu.be/{vid} ({status['privacyStatus']}"
          + (f", se publica {publicar}" if publicar else "") + ")")
    miniatura_y_subtitulos(cid, vid, carpeta, m)
    return vid


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "ayuda"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "conectar":
        conectar(int(a[1]) if len(a) > 1 else 3000)
    elif cmd == "canales":
        canales()
    elif cmd == "videos":
        videos(resolver_canal(a[1]))
    elif cmd == "canal":
        cfg = json.load(open(os.path.join(CANALES, a[1] + ".json"), encoding="utf-8"))
        configurar_canal(resolver_canal(a[1]), cfg)
    elif cmd == "aplicar":
        aplicar(os.path.join(RAIZ, "videos", a[1]), resolver_canal(a[2]), a[3])
    elif cmd == "metricas":
        metricas(resolver_canal(a[1]), a[1] if not a[1].startswith("UC") else None, int(a[2]) if len(a) > 2 else 28)
    elif cmd == "publicar":
        pub = a[a.index("--programar") + 1] if "--programar" in a else None
        priv = next((x for x in a[3:] if x in ("private", "unlisted", "public")), "public")
        cambiar_visibilidad(resolver_canal(a[1]), a[2], priv, pub)
    elif cmd == "subir":
        pub = a[a.index("--publicar") + 1] if "--publicar" in a else None
        priv = next((x for x in a[3:] if x in ("private", "unlisted", "public")), "private")
        subir(os.path.join(RAIZ, "videos", a[1]), resolver_canal(a[2]), priv, pub)
    else:
        sys.exit(f"Comando desconocido '{cmd}'. Usa: python fab.py yt ayuda")


if __name__ == "__main__":
    main()
