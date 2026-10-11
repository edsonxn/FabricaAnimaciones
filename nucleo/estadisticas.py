# -*- coding: utf-8 -*-
"""Panel general de estadísticas de TODOS los canales (un solo HTML, sin servidor ni dependencias).

  python fab.py estadisticas                 arma el panel con los datos guardados y lo abre
  python fab.py estadisticas --actualizar    antes pide los datos frescos a YouTube (Data API + Analytics, solo lectura)
  python fab.py estadisticas --actualizar kuriox logia     solo esos canales
  python fab.py estadisticas --no-abrir      no abre el navegador
  python fab.py canales [--actualizar]       INICIO DE DÍA: tabla de qué canal se queda antes sin video programado

El mismo panel vive en la pestaña «Canales» del panel de producción (python fab.py panel --abrir), con botón para
actualizar los datos y el ciclo de cada canal editable.

Datos por canal:  canales/metricas/panel/<alias>.json   (serie diaria de 180 días, videos, vistas por periodo)
Panel:            canales/metricas/panel_canales.html   (plantilla: nucleo/estadisticas.html)
Analytics llega con 2-3 días de retraso; las cifras públicas (suscriptores, vistas totales) son del momento.
"""
import datetime as dt
import glob
import json
import os
import re
import sys
import webbrowser
from concurrent.futures import ThreadPoolExecutor

import requests

import youtube as yt

DATOS = os.path.join(yt.CANALES, "metricas", "panel")
SALIDA = os.path.join(yt.CANALES, "metricas", "panel_canales.html")
PLANTILLA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estadisticas.html")
PERIODOS = (7, 28, 90)
DIAS_SERIE = 180                      # el doble del periodo mayor: permite comparar contra el periodo anterior
# Orden FIJO de color: el color sigue al canal, no a su posición. Un canal nuevo se agrega AL FINAL.
ORDEN = ["kuriox", "edsonxn", "pieza_oculta", "bitacora_perdida", "cronopapel", "sapiens_con_wifi", "logia",
         "wild_next_door"]
MET_DIA = "views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,comments,shares"


def alias_conocidos():
    """Alias de canales/<alias>.json que tienen canal_id, en el orden fijo de color."""
    vistos = []
    for ruta in sorted(glob.glob(os.path.join(yt.CANALES, "*.json"))):
        try:
            if json.load(open(ruta, encoding="utf-8")).get("canal_id"):
                vistos.append(os.path.splitext(os.path.basename(ruta))[0])
        except Exception:
            pass
    return [a for a in ORDEN if a in vistos] + [a for a in vistos if a not in ORDEN]


def _segundos(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def _es_short(vid):
    """youtube.com/shorts/<id> responde 200 si es Short y redirige a /watch si no. None = no se pudo saber."""
    try:
        r = requests.head("https://www.youtube.com/shorts/" + vid, allow_redirects=False, timeout=20)
        return True if r.status_code == 200 else False if r.status_code in (301, 302, 303) else None
    except Exception:
        return None


def actualizar(alias):
    cfg = json.load(open(os.path.join(yt.CANALES, alias + ".json"), encoding="utf-8"))
    cid = cfg["canal_id"]
    ruta = os.path.join(DATOS, alias + ".json")
    previo = json.load(open(ruta, encoding="utf-8")) if os.path.isfile(ruta) else {}
    shorts = {v["id"]: v.get("short") for v in previo.get("videos", [])}
    hoy = dt.date.today()
    hasta = hoy.isoformat()
    ch = yt.api(cid, "GET", "/channels", params=dict(part="snippet,statistics,contentDetails", id=cid))["items"][0]
    s = ch["statistics"]
    out = dict(alias=alias, canal_id=cid, nombre=ch["snippet"]["title"], actualizado=dt.datetime.now().isoformat(timespec="minutes"),
               suscriptores=int(s.get("subscriberCount", 0)), vistas_totales=int(s.get("viewCount", 0)),
               videos_totales=int(s.get("videoCount", 0)), avisos=[])

    dias = yt._reporte(cid, (hoy - dt.timedelta(days=DIAS_SERIE)).isoformat(), hasta, metrics=MET_DIA, dimensions="day", sort="day")
    if dias and "error" in dias[0]:
        out["avisos"].append("Analytics: " + dias[0]["error"])
        dias = []
    out["dias"] = [[d["day"], d["views"], d["estimatedMinutesWatched"], d["subscribersGained"], d["subscribersLost"],
                    d["likes"], d["comments"], d["shares"]] for d in dias]

    # vistas de cada video dentro de cada periodo (para que la tabla de videos obedezca el filtro de periodo)
    por_periodo = {}
    for p in PERIODOS:
        filas = yt._reporte(cid, (hoy - dt.timedelta(days=p)).isoformat(), hasta, dimensions="video", sort="-views", maxResults=200,
                            metrics="views,estimatedMinutesWatched,averageViewPercentage,subscribersGained,likes")
        por_periodo[p] = {f["video"]: f for f in filas if "video" in f}

    # lista de videos: las subidas más recientes + cualquiera con vistas en el periodo
    ids, pagina = [], None
    while len(ids) < 200:
        r = yt.api(cid, "GET", "/playlistItems", params=dict(part="contentDetails", maxResults=50, pageToken=pagina,
                                                            playlistId=ch["contentDetails"]["relatedPlaylists"]["uploads"]))
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        pagina = r.get("nextPageToken")
        if not pagina:
            break
    ids += [v for p in PERIODOS for v in por_periodo[p] if v not in ids]
    crudos = []
    for i in range(0, len(ids), 50):
        crudos += yt.api(cid, "GET", "/videos", params=dict(part="snippet,status,statistics,contentDetails",
                                                           id=",".join(ids[i:i + 50]))).get("items", [])
    videos = []
    for v in crudos:
        st, dur = v["status"], _segundos(v["contentDetails"].get("duration"))
        estado = "programado" if st.get("publishAt") and st["privacyStatus"] == "private" else st["privacyStatus"]
        fila = dict(id=v["id"], titulo=v["snippet"]["title"], estado=estado, fecha=st.get("publishAt") or v["snippet"].get("publishedAt"),
                    dur=dur, vistas=int(v.get("statistics", {}).get("viewCount", 0)), likes=int(v.get("statistics", {}).get("likeCount", 0)),
                    comentarios=int(v.get("statistics", {}).get("commentCount", 0)), short=shorts.get(v["id"]), p={})
        for p in PERIODOS:
            f = por_periodo[p].get(v["id"])
            if f:
                fila["p"][str(p)] = [f["views"], f["estimatedMinutesWatched"], round(f["averageViewPercentage"], 1), f["subscribersGained"]]
        videos.append(fila)
    # Short o largo: más de 3 min nunca es Short; si no, se pregunta a YouTube (solo los públicos, y una sola vez)
    dudosos = [v for v in videos if v["dur"] <= 180 and v["estado"] == "public" and v["short"] is None]
    with ThreadPoolExecutor(8) as ex:
        for v, r in zip(dudosos, ex.map(lambda v: _es_short(v["id"]), dudosos)):
            v["short"] = r
    for v in videos:
        if v["dur"] > 180:
            v["short"] = False
        elif v["short"] is None:
            v["short"] = v["dur"] <= 60
    out["videos"] = videos
    os.makedirs(DATOS, exist_ok=True)
    json.dump(out, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    v28 = sum(d[1] for d in out["dias"][-28:])
    print(f"  {out['nombre']:20s} subs={out['suscriptores']:<6} vistas 28 d={v28:<7} videos={len(videos)}"
          + ("  AVISO: " + "; ".join(out["avisos"]) if out["avisos"] else ""), flush=True)
    return out


# ---------------------------------------------------------------- calendario: ¿qué canal se queda antes sin video?
def _f(iso):
    return dt.datetime.fromisoformat(iso[:19] + "+00:00")


def ciclo_dias(cfg):
    """Cada cuántos días publica el canal: `horario.ciclo_dias` > `horario.separacion_min_horas` > 7 (plan semanal)."""
    h = cfg.get("horario") or {}
    if h.get("ciclo_dias"):
        return float(h["ciclo_dias"])
    return float(h["separacion_min_horas"]) / 24 if h.get("separacion_min_horas") else 7.0


def guardar_ciclo(alias, dias):
    """Fija `horario.ciclo_dias` en canales/<alias>.json (lo usa el panel; solo cambia el pronóstico, no el freno de youtube.py)."""
    if alias not in alias_conocidos() or not 1 <= float(dias) <= 60:
        raise ValueError("canal o ciclo no válido")
    ruta = os.path.join(yt.CANALES, alias + ".json")
    texto = open(ruta, encoding="utf-8").read()
    cfg = json.loads(texto)
    cfg.setdefault("horario", {})["ciclo_dias"] = int(dias) if float(dias) == int(dias) else float(dias)
    open(ruta, "w", encoding="utf-8").write(json.dumps(cfg, ensure_ascii=False, indent=2) + ("\n" if texto.endswith("\n") else ""))
    return cfg["horario"]["ciclo_dias"]


def nivel(dias):
    return "atrasado" if dias < 0 else "urgente" if dias <= 3 else "pronto" if dias <= 7 else "bien"


def calendario(d, cfg, ahora=None):
    """Cobertura del canal: `vacio` = primer hueco del ciclo SIN video (último programado, o último público, + ciclo)."""
    ahora = ahora or dt.datetime.now(dt.timezone.utc)
    ciclo = ciclo_dias(cfg)
    con_fecha = [v for v in d.get("videos", []) if v.get("fecha") and v["estado"] in ("public", "programado")]
    prog = sorted((v for v in con_fecha if v["estado"] == "programado" and _f(v["fecha"]) > ahora), key=lambda v: v["fecha"])
    salidos = sorted((v for v in con_fecha if _f(v["fecha"]) <= ahora), key=lambda v: v["fecha"])
    base = _f(prog[-1]["fecha"]) if prog else _f(salidos[-1]["fecha"]) if salidos else ahora - dt.timedelta(days=ciclo)
    vacio = base + dt.timedelta(days=ciclo)
    no_van = {x["id"] for x in cfg.get("duplicados_para_borrar", [])} | {
        x["id"] for x in cfg.get("publicados", []) if "NO publicar" in (x.get("nota") or "")}
    mes = (ahora - dt.timedelta(days=30)).isoformat()

    def corto(v):
        return dict(id=v["id"], titulo=v["titulo"], fecha=v["fecha"], short=bool(v.get("short")))
    return dict(ciclo=ciclo, vacio=vacio.strftime("%Y-%m-%dT%H:%M:%SZ"), dias=round((vacio - ahora).total_seconds() / 86400, 1),
                programados=[corto(v) for v in prog], ultimo=corto(salidos[-1]) if salidos else None,
                sin_fecha=[corto(v) for v in d.get("videos", []) if v["estado"] == "private" and (v.get("fecha") or "") > mes
                           and v["id"] not in no_van])


def en_produccion(proyectos=None):
    """{alias: [proyectos de videos/ todavía sin subir]} a partir del estado del panel de producción."""
    try:
        if proyectos is None:
            import panel
            proyectos = panel.estado()["proyectos"]
        out = {}
        for p in proyectos:
            if p.get("canal") and not (p.get("publicado") or p.get("archivado") or p.get("oculto") or p.get("error")):
                out.setdefault(p["canal"], []).append(dict(video=p["nombre"], titulo=p.get("titulo") or p["nombre"],
                                                           progreso=round(min(1, p.get("progreso") or 0), 2), etapa=p.get("etapa_actual")))
        return out
    except Exception:                                # el calendario no depende de esto
        return {}


def datos_panel(proyectos=None):
    canales, prod = [], en_produccion(proyectos)
    for i, alias in enumerate(alias_conocidos()):
        ruta = os.path.join(DATOS, alias + ".json")
        if os.path.isfile(ruta):
            d = json.load(open(ruta, encoding="utf-8"))
            d["color"] = i % 8
            d["cal"] = calendario(d, json.load(open(os.path.join(yt.CANALES, alias + ".json"), encoding="utf-8")))
            d["prod"] = sorted(prod.get(alias, []), key=lambda x: -x["progreso"])
            canales.append(d)
    return dict(generado=dt.datetime.now().isoformat(timespec="minutes"), periodos=list(PERIODOS), canales=canales)


def html_panel(proyectos=None):
    datos = datos_panel(proyectos)
    return open(PLANTILLA, encoding="utf-8").read().replace(
        "__DATA__", json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))


def tabla_calendario():
    """Lo que se mira al empezar el día: canales ordenados por quién se queda antes sin video."""
    cs = sorted(datos_panel()["canales"], key=lambda c: c["cal"]["dias"])
    if not cs:
        sys.exit("Todavía no hay datos: corre  python fab.py canales --actualizar")
    DIA = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    print(f"{'Canal':18s} {'Estado':9s} {'Sin video desde':16s} {'Faltan':>7s}  {'Ciclo':>5s}  Prog.  En producción")
    for c in cs:
        k, v = c["cal"], _f(c["cal"]["vacio"]).astimezone()
        falta = f"{k['dias']:.0f} d" if k["dias"] >= 0 else f"-{-k['dias']:.0f} d"
        prod = ", ".join(f"{p['video']} {p['progreso'] * 100:.0f}%" for p in c["prod"][:3]) or "—"
        print(f"{c['nombre'][:18]:18s} {nivel(k['dias']).upper():9s} {DIA[v.weekday()]} {v.strftime('%d-%m %H:%M'):12s} {falta:>7s}  "
              f"{k['ciclo']:>4g}d  {len(k['programados']):>4d}   {prod}")
    viejo = min(c["actualizado"] for c in cs)
    print(f"\nDatos de YouTube del {viejo.replace('T', ' ')} (hora local). «Sin video desde» = último programado/publicado + ciclo."
          "\nFrescos: python fab.py canales --actualizar   ·   Interactivo: python fab.py panel --abrir, pestaña «Canales».")


def actualizar_seguro(alias, intentos=3):
    """`actualizar` con reintentos: YouTube a veces contesta un 401 pasajero con un token válido."""
    for i in range(intentos):
        try:
            return actualizar(alias)
        except RuntimeError as e:
            if "HTTP 401" not in str(e) or i == intentos - 1:
                raise


def generar(abrir=True):
    if not glob.glob(os.path.join(DATOS, "*.json")):
        sys.exit("Todavía no hay datos: corre  python fab.py estadisticas --actualizar")
    html = html_panel()
    open(SALIDA, "w", encoding="utf-8").write(html)
    print("panel:", os.path.relpath(SALIDA, yt.RAIZ))
    if abrir:
        webbrowser.open("file:///" + SALIDA.replace("\\", "/"))


def main():
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help", "ayuda"):
        print(__doc__)
        return
    if "--actualizar" in a:
        pedidos = [x for x in a if not x.startswith("--") and x != "calendario"] or alias_conocidos()
        print(f"Pidiendo datos a YouTube de {len(pedidos)} canal(es)…", flush=True)
        for alias in pedidos:
            try:
                actualizar_seguro(alias)
            except (Exception, SystemExit) as e:        # un canal sin token o caído no tumba a los demás
                print(f"  {alias}: NO se actualizó ({e})", flush=True)
    if a and a[0] == "calendario":
        return tabla_calendario()
    generar(abrir="--no-abrir" not in a)


if __name__ == "__main__":
    main()
