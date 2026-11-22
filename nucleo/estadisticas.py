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
RAIZ_VIDEOS = os.path.join(os.path.dirname(yt.CANALES), "videos")
SALIDA = os.path.join(yt.CANALES, "metricas", "panel_canales.html")
PLANTILLA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estadisticas.html")
PERIODOS = (7, 28, 90)
DIAS_SERIE = 180                      # el doble del periodo mayor: permite comparar contra el periodo anterior
# Orden FIJO de color: el color sigue al canal, no a su posición. Un canal nuevo se agrega AL FINAL.
ORDEN = ["kuriox", "edsonxn", "pieza_oculta", "bitacora_perdida", "cronopapel", "sapiens_con_wifi", "logia",
         "wild_next_door"]
MET_DIA = "views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,comments,shares"


def alias_conocidos(con_suspendidos=False):
    """Alias de canales/<alias>.json que tienen canal_id, en el orden fijo de color. Los que llevan `"suspendido"`
    (el usuario los pausó, p. ej. Edsonxn el 21-oct-2026) no salen en el calendario, las estadísticas ni
    `canales --actualizar`, salvo con `con_suspendidos=True`."""
    vistos = []
    for ruta in sorted(glob.glob(os.path.join(yt.CANALES, "*.json"))):
        try:
            d = json.load(open(ruta, encoding="utf-8"))
            if d.get("canal_id") and (con_suspendidos or not d.get("suspendido")):
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


def _logo(snippet):
    th = snippet.get("thumbnails") or {}
    return (th.get("medium") or th.get("high") or th.get("default") or {}).get("url")


def poner_logos():
    """Agrega `logo` a canales/metricas/panel/<alias>.json sin pedir todo lo demás (una lectura de /channels por canal)."""
    for alias in alias_conocidos(con_suspendidos=True):
        ruta = os.path.join(DATOS, alias + ".json")
        if not os.path.isfile(ruta):
            continue
        d = json.load(open(ruta, encoding="utf-8"))
        try:
            ch = yt.api(d["canal_id"], "GET", "/channels", params=dict(part="snippet", id=d["canal_id"]))["items"][0]
        except Exception as e:
            print(f"  {alias}: sin logo ({e})")
            continue
        d["logo"] = _logo(ch["snippet"])
        json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"  {alias}: {d['logo']}")


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
               videos_totales=int(s.get("videoCount", 0)), avisos=[],
               logo=_logo(ch["snippet"]))     # foto de perfil: la usan los huecos por llenar de la ruleta del panel

    dias = yt._reporte(cid, (hoy - dt.timedelta(days=DIAS_SERIE)).isoformat(), hasta, metrics=MET_DIA, dimensions="day", sort="day")
    if dias and "error" in dias[0]:
        out["avisos"].append("Analytics: " + dias[0]["error"])
        dias = []
    out["dias"] = [[d["day"], d["views"], d["estimatedMinutesWatched"], d["subscribersGained"], d["subscribersLost"],
                    d["likes"], d["comments"], d["shares"]] for d in dias]

    # misma serie, solo la parte de Shorts (el panel resta para obtener los largos)
    cortos = yt._reporte(cid, (hoy - dt.timedelta(days=DIAS_SERIE)).isoformat(), hasta, metrics=MET_DIA,
                         dimensions="day,creatorContentType", filters="creatorContentType==shorts", sort="day")
    if cortos and "error" in cortos[0]:
        out["avisos"].append("Analytics (Shorts): " + cortos[0]["error"])
        cortos = []
    out["dias_s"] = [[d["day"], d["views"], d["estimatedMinutesWatched"], d["subscribersGained"], d["subscribersLost"],
                      d["likes"], d["comments"], d["shares"]] for d in cortos]

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
        if "#shorts" in v["titulo"].lower():        # nuestros Shorts siempre lo llevan; vale también para los programados
            v["short"] = True
        elif v["dur"] > 180:
            v["short"] = False
        elif v["short"] is None and v["dur"] > 0:      # dur 0 = YouTube aún lo procesa: sin decidir (cuenta como largo)
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
    """Cobertura del canal: `vacio` = primer hueco del ciclo SIN video LARGO (último programado, o último público, + ciclo). Los Shorts no cuentan."""
    ahora = ahora or dt.datetime.now(dt.timezone.utc)
    ciclo = ciclo_dias(cfg)
    # Los Shorts no cuentan para la cobertura (el usuario, 12-oct y 21-oct-2026: «son extras»): solo videos largos.
    # Short = marcado por YouTube, o con #Shorts en el título, o registrado `"short": true` en publicados (un Short
    # programado de 60-180 s o aún en proceso (dur 0) no lo detecta la duración)
    reg_short = {x["id"] for x in cfg.get("publicados", []) if x.get("id") and x.get("short")}
    largos = [v for v in d.get("videos", []) if not (v.get("short") or v["id"] in reg_short
                                                       or "#shorts" in (v.get("titulo") or "").lower())]
    # Lo subido/programado después de la última lectura de YouTube (o con la cuota agotada) cuenta igual si ya está
    # registrado en canales/<alias>.json → publicados (regla del usuario, 13-oct-2026: el panel se actualiza al empezar y
    # al terminar cada video)
    vistos = {v["id"] for v in d.get("videos", [])}
    # Y si la última lectura lo vio PRIVADO sin fecha pero después se publicó o programó (registrado en publicados), gana el
    # registro (el usuario, 22-nov-2026: mpm_takis salía «atrasado» en el panel ya público)
    reg = {x["id"]: x for x in cfg.get("publicados", []) if x.get("id")}
    for v in largos:
        x = reg.get(v["id"])
        if x and v.get("estado") == "private" and (x.get("programado") or (x.get("publicado") and x.get("visibilidad") == "public")):
            v.update(fecha=x.get("programado") or x["publicado"], estado="programado" if x.get("programado") else "public", registro=True)
    for x in cfg.get("publicados", []):
        f = x.get("programado") or x.get("publicado")
        if x.get("id") and x["id"] not in vistos and f and not x.get("short") and "#shorts" not in (x.get("titulo") or "").lower():
            largos.append(dict(id=x["id"], titulo=x.get("titulo", x.get("video", "")), fecha=f,
                               estado="programado" if x.get("programado") else "public", registro=True))
    con_fecha = [v for v in largos if v.get("fecha") and v["estado"] in ("public", "programado")]
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
                sin_fecha=[corto(v) for v in largos if v["estado"] == "private" and (v.get("fecha") or "") > mes
                           and v["id"] not in no_van])


def en_produccion(proyectos=None):
    """{alias: [proyectos de videos/ todavía sin subir]} a partir del estado del panel de producción."""
    try:
        if proyectos is None:
            import panel
            proyectos = panel.estado()["proyectos"]
        out = {}
        for p in proyectos:
            # los Shorts (verticales) son extras: no cuentan como «en producción» del calendario (el usuario, 21-oct-2026)
            if p.get("canal") and p.get("formato") != "vertical" and not (
                    p.get("publicado") or p.get("archivado") or p.get("oculto") or p.get("error")):
                E = p.get("etapas") or {}
                etapa = p.get("etapa_actual") or next((k for k in E if E[k].get("estado") not in ("listo", "omitido")), None)
                mini, final = mini_obra(p["nombre"])
                out.setdefault(p["canal"], []).append(dict(video=p["nombre"], titulo=p.get("titulo") or p["nombre"],
                                                           progreso=round(min(1, p.get("progreso") or 0), 2), etapa=p.get("etapa_actual"),
                                                           etapa_n=ETAPA_N.get(etapa, etapa or ""), mini=mini, mini_final=final))
        return out
    except Exception:                                # el calendario no depende de esto
        return {}


ETAPA_N = {"guion": "Guion", "voz": "Voz", "seleccion": "Selección", "tiempo": "Tiempo", "escenas": "Escenas", "beats": "Beats",
           "prompts": "Prompts", "flow": "Flow", "musica": "Música", "sfx": "Efectos", "mezcla": "Mezcla", "video": "Render",
           "final": "Final", "verificar": "Verificar", "miniatura": "Miniatura", "metadatos": "Metadatos", "subida": "Subida"}


def mini_obra(video):
    """(ruta /media/…, es_la_final) de la imagen que «se construye» en la ruleta de producción: la miniatura de
    youtube.json o salida/, y si todavía no existe, un boceto (previews/_mini, luego cualquier cuadro de previews/)."""
    car = os.path.join(RAIZ_VIDEOS, video)
    try:
        m = (json.load(open(os.path.join(car, "youtube.json"), encoding="utf-8")).get("miniatura") or "").replace("\\", "/")
    except Exception:
        m = ""
    finales = ([m] if m.split("/")[0] in ("salida", "previews") else []) + ["salida/miniatura.jpg"] + sorted(
        os.path.relpath(x, car).replace("\\", "/") for x in glob.glob(os.path.join(car, "salida", "*_mini_*.jpg")))
    for f in finales:
        if os.path.isfile(os.path.join(car, f)):
            return f"/media/{video}/{f}", True
    bocetos = sorted(glob.glob(os.path.join(car, "previews", "_mini", "*.jpg"))) + sorted(
        glob.glob(os.path.join(car, "previews", "*.jpg")), key=lambda x: (not re.search(r"(medios|promesas|fx)_\d", x), x))
    for x in bocetos:
        return "/media/{}/{}".format(video, os.path.relpath(x, car).replace("\\", "/")), False
    return None, False


def huecos(cal, cfg, n, ahora=None):
    """Los siguientes `n` huecos del canal sin video largo: el primero es `cal.vacio` (o, si ya pasó, el siguiente horario a
    partir de ahora = canal atrasado) y luego uno por ciclo, a la hora de `horario.utc`. [(datetime, atrasado), …]"""
    ahora = ahora or dt.datetime.now(dt.timezone.utc)
    hm = re.match(r"(\d{1,2}):(\d{2})", str((cfg.get("horario") or {}).get("utc") or ""))
    s = _f(cal["vacio"])
    atrasado = s < ahora
    if atrasado:
        s = ahora
    if hm:                                           # a la hora del canal ese mismo día; si ya pasó, al día siguiente
        h = s.replace(hour=int(hm[1]), minute=int(hm[2]), second=0, microsecond=0)
        s = h if h > ahora and (h >= s or not atrasado) else h + dt.timedelta(days=1)
    return [(s + dt.timedelta(days=cal["ciclo"] * i), atrasado and i == 0) for i in range(n)]


def huecos_produccion(prod, cal, cfg, ahora=None):
    """A cada video en producción (el más avanzado primero) le toca el siguiente hueco del canal (`huecos`). Es lo que la
    ruleta de producción cuelga sobre la de publicaciones (19-nov-2026)."""
    for x, (s, tarde) in zip(prod, huecos(cal, cfg, len(prod), ahora)):
        x["sale"] = s.strftime("%Y-%m-%dT%H:%M:%SZ")
        x["atrasado"] = tarde
    return prod


def huecos_libres(cal, cfg, n_prod, dias=10, maximo=3, ahora=None):
    """Huecos que NADIE está llenando (ni programado ni en producción) en los próximos `dias`, al menos el primero: la
    ruleta los cuelga con el logo del canal para ver qué canal necesita un video nuevo (el usuario, 19-nov-2026)."""
    ahora = ahora or dt.datetime.now(dt.timezone.utc)
    hs = huecos(cal, cfg, n_prod + maximo, ahora)[n_prod:]
    out = [dict(sale=s.strftime("%Y-%m-%dT%H:%M:%SZ"), atrasado=tarde) for k, (s, tarde) in enumerate(hs)
           if k == 0 or s <= ahora + dt.timedelta(days=dias)]
    return out


def miniaturas_locales(d, cfg, dias=4):
    """{id: "/media/<video>/salida/miniatura.jpg"} de lo programado o recién salido: la ruleta de publicaciones del panel
    las enseña porque YouTube no da la miniatura de un video que sigue en privado (el usuario, 19-nov-2026)."""
    desde = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=dias)).isoformat()
    ids = {v["id"] for v in d.get("videos", []) if v.get("estado") == "programado" or (v.get("fecha") or "") >= desde}
    out = {}
    for x in cfg.get("publicados", []):
        f = x.get("programado") or x.get("publicado") or ""
        if not (x.get("id") and x.get("video")) or (x["id"] not in ids and f < desde):
            continue
        carpeta = os.path.join(RAIZ_VIDEOS, x["video"])
        try:
            m = json.load(open(os.path.join(carpeta, "youtube.json"), encoding="utf-8")).get("miniatura") or "salida/miniatura.jpg"
        except Exception:
            m = "salida/miniatura.jpg"
        m = m.replace("\\", "/")
        if m.split("/")[0] in ("salida", "previews") and os.path.isfile(os.path.join(carpeta, m)):
            out[x["id"]] = f"/media/{x['video']}/{m}"
    return out


def datos_panel(proyectos=None):
    canales, prod = [], en_produccion(proyectos)
    orden = alias_conocidos(con_suspendidos=True)    # el color sale de la lista completa: suspender uno no recolorea a los demás
    for alias in alias_conocidos():
        ruta = os.path.join(DATOS, alias + ".json")
        cfg = json.load(open(os.path.join(yt.CANALES, alias + ".json"), encoding="utf-8"))
        if os.path.isfile(ruta):
            d = json.load(open(ruta, encoding="utf-8"))
        else:
            # Canal nuevo sin `canales --actualizar` todavía (Mil por Minuto, 19-nov-2026): sin métricas, pero sus videos en
            # producción y su calendario (de canales/<alias>.json → horario/publicados) sí salen en la ruleta y en «La obra»
            # (el usuario, 19-nov-2026: «hay 2 proyectos activos en construcción y solo puedo ver 1»)
            d = dict(alias=alias, canal_id=cfg.get("canal_id"), nombre=cfg.get("nombre") or alias, actualizado=None,
                     suscriptores=0, vistas_totales=0, videos_totales=0, avisos=["Sin estadísticas todavía: python fab.py canales --actualizar"],
                     dias=[], dias_s=[], videos=[], sin_datos=True)
        d["color"] = orden.index(alias) % 8
        d["cal"] = calendario(d, cfg)
        # `"sin_seguimiento"` = canal que no estamos moviendo: fuera del calendario, sus estadísticas siguen (el usuario, 19-nov-2026)
        d["seguimiento"] = not cfg.get("sin_seguimiento")
        d["minis"] = miniaturas_locales(d, cfg)
        d["prod"] = huecos_produccion(sorted(prod.get(alias, []), key=lambda x: -x["progreso"]), d["cal"], cfg)
        d["libres"] = huecos_libres(d["cal"], cfg, len(d["prod"])) if d["seguimiento"] else []
        canales.append(d)
    return dict(generado=dt.datetime.now().isoformat(timespec="minutes"), periodos=list(PERIODOS), canales=canales)


def html_panel(proyectos=None):
    datos = datos_panel(proyectos)
    return open(PLANTILLA, encoding="utf-8").read().replace(
        "__DATA__", json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))


def tabla_calendario():
    """Lo que se mira al empezar el día: canales ordenados por quién se queda antes sin video."""
    cs = sorted((c for c in datos_panel()["canales"] if c["seguimiento"]), key=lambda c: c["cal"]["dias"])
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
    viejo = min((c["actualizado"] for c in cs if c.get("actualizado")), default="—")
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
