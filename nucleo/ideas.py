# -*- coding: utf-8 -*-
"""Decidir el SIGUIENTE video de un canal con datos (no por ocurrencia).

  python fab.py ideas                        qué canales tienen búsquedas/competidores configurados y de cuándo es su informe
  python fab.py ideas <alias>                informe del canal con lo guardado (si no hay nada guardado, lo pide a YouTube)
  python fab.py ideas <alias> --actualizar   vuelve a pedir a YouTube lo de fuera (solo lectura; ~100 de cuota por búsqueda)
  python fab.py ideas <alias> --dias 90      ventana de «reciente» para los videos de fuera (por defecto 60)

Dos mitades:
  1. LO TUYO  (canales/metricas/panel/<alias>.json; fresco con `python fab.py canales --actualizar`): cada video público
     contra la mediana de su clase (Short / largo) del propio canal, con % visto y suscriptores ganados.
  2. LO DE FUERA: videos del nicho publicados en los últimos N días que rompieron la media DE SU PROPIO CANAL
     (× mediana = vistas del video / mediana de las últimas 50 subidas de ese canal, misma clase). Un ×8 en un canal de
     3 000 suscriptores es un formato que se puede repetir; un millón de vistas en un canal de 10 M no dice nada.

Configuración, en canales/<alias>.json:
  "ideas": {"idioma": "es", "region": "MX", "busquedas": ["...", "..."], "competidores": ["UC...", "@handle"],
            "dias": 60, "min_vistas": 1000, "filtro": ["historia"]}
  `filtro` (opcional): de lo hallado por búsqueda solo cuenta el video cuyo título trae alguna de esas palabras (quita el
  ruido de búsquedas amplias); los videos de `competidores` entran siempre.
Para aprender de las apuestas: en `publicados` de ese mismo archivo, `"formato": "<nombre corto>"` en cada video; el informe
agrupa lo tuyo por formato.

Salida: canales/metricas/ideas/<alias>.md (informe) y <alias>.json (datos crudos de fuera, con fecha).
"""
import datetime as dt
import json
import os
import statistics
import sys

import estadisticas as es
import youtube as yt

IDEAS = os.path.join(yt.CANALES, "metricas", "ideas")
MAX_CANALES = 25                 # canales de fuera que se miden por corrida (2 de cuota cada uno)
CORTO = 180                      # s; hasta aquí cuenta como Short (fuera no se puede preguntar video por video)
MADURO = 7                       # días; un video más joven no entra en medianas ni en el ranking de lo tuyo


def _cfg(alias):
    return json.load(open(os.path.join(yt.CANALES, alias + ".json"), encoding="utf-8"))


def _edad(iso, ahora):
    return max(0.0, (ahora - es._f(iso)).total_seconds() / 86400)


def _mediana(xs):
    return statistics.median(xs) if xs else 0


# ---------------------------------------------------------------- lo de fuera (YouTube Data API, solo lectura)
def _subidas(cid, canal):
    """Últimas 50 subidas públicas de un canal ajeno: [dict(id, titulo, fecha, dur, vistas)]."""
    pl = canal["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = [i["contentDetails"]["videoId"] for i in
           yt.api(cid, "GET", "/playlistItems", params=dict(part="contentDetails", playlistId=pl, maxResults=50)).get("items", [])]
    if not ids:
        return []
    vs = yt.api(cid, "GET", "/videos", params=dict(part="snippet,statistics,contentDetails", id=",".join(ids))).get("items", [])
    out = []
    for v in vs:
        dur = es._segundos(v["contentDetails"].get("duration"))
        if dur and v["snippet"].get("liveBroadcastContent", "none") == "none":
            out.append(dict(id=v["id"], titulo=v["snippet"]["title"], fecha=v["snippet"]["publishedAt"], dur=dur,
                            vistas=int(v.get("statistics", {}).get("viewCount", 0))))
    return out


def actualizar(alias, dias=None):
    cfg = _cfg(alias)
    cid, op = cfg["canal_id"], cfg.get("ideas") or {}
    dias = int(dias or op.get("dias") or 60)
    if not (op.get("busquedas") or op.get("competidores")):
        sys.exit(f'canales/{alias}.json no tiene "ideas": {{"busquedas": [...], "competidores": [...]}} (ver nucleo/ideas.py)')
    ahora = dt.datetime.now(dt.timezone.utc)
    desde = (ahora - dt.timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")
    avisos, cuota = [], 0

    # 1) búsquedas: lo más visto del nicho en la ventana
    hallados, por_canal = {}, {}                       # id de video -> búsqueda;  canal -> nº de aciertos
    for q in op.get("busquedas", []):
        p = dict(part="snippet", q=q, type="video", order="viewCount", publishedAfter=desde, maxResults=50)
        if op.get("idioma"):
            p["relevanceLanguage"] = op["idioma"]
        if op.get("region"):
            p["regionCode"] = op["region"]
        try:
            items = yt.api(cid, "GET", "/search", params=p).get("items", [])
            cuota += 100
        except RuntimeError as e:
            avisos.append(f"búsqueda «{q}»: {e}")
            continue
        for it in items:
            vid, ch = it["id"].get("videoId"), it["snippet"]["channelId"]
            if vid and ch != cid and vid not in hallados:
                hallados[vid] = q
                por_canal[ch] = por_canal.get(ch, 0) + 1
        print(f"  búsqueda «{q}»: {len(items)} videos", flush=True)

    # 2) competidores fijos (UC... o @handle)
    fijos = []
    for c in op.get("competidores", []):
        if c.startswith("UC"):
            fijos.append(c)
            continue
        try:
            r = yt.api(cid, "GET", "/channels", params=dict(part="id", forHandle=c)).get("items", [])
            cuota += 1
            fijos += [r[0]["id"]] if r else []
            if not r:
                avisos.append(f"competidor {c}: no existe ese handle")
        except RuntimeError as e:
            avisos.append(f"competidor {c}: {e}")

    # 3) medir cada canal contra sí mismo
    orden = fijos + [c for c, _ in sorted(por_canal.items(), key=lambda x: -x[1]) if c not in fijos]
    if len(orden) > MAX_CANALES:
        avisos.append(f"{len(orden)} canales hallados; se midieron los {MAX_CANALES} con más aciertos")
    orden = orden[:max(MAX_CANALES, len(fijos))]
    info = {}
    for i in range(0, len(orden), 50):
        for ch in yt.api(cid, "GET", "/channels", params=dict(part="snippet,statistics,contentDetails",
                                                            id=",".join(orden[i:i + 50]))).get("items", []):
            info[ch["id"]] = ch
        cuota += 1
    canales, videos = {}, []
    for ch_id in orden:
        ch = info.get(ch_id)
        if not ch:
            continue
        try:
            subidas = _subidas(cid, ch)
            cuota += 2
        except RuntimeError as e:
            avisos.append(f"{ch['snippet']['title']}: {e}")
            continue
        med = {}
        for clase, sel in (("short", lambda v: v["dur"] <= CORTO), ("largo", lambda v: v["dur"] > CORTO)):
            maduros = [v["vistas"] for v in subidas if sel(v) and _edad(v["fecha"], ahora) >= MADURO]
            med[clase] = _mediana(maduros) if len(maduros) >= 4 else None
        todos = _mediana([v["vistas"] for v in subidas])
        s = ch["statistics"]
        canales[ch_id] = dict(nombre=ch["snippet"]["title"], subs=None if s.get("hiddenSubscriberCount") else int(s.get("subscriberCount", 0)),
                              fijo=ch_id in fijos, aciertos=por_canal.get(ch_id, 0), mediana=med, n=len(subidas))
        for v in subidas:
            if v["fecha"] < desde or not (ch_id in fijos or v["id"] in hallados):   # de un canal hallado solo cuenta lo que salió en la búsqueda
                continue
            clase = "short" if v["dur"] <= CORTO else "largo"
            base = med[clase] or todos or 1
            videos.append(dict(v, canal=ch_id, clase=clase, x=round(v["vistas"] / max(base, 1), 2),
                               origen=hallados.get(v["id"]) or "competidor"))
    out = dict(alias=alias, fecha=ahora.isoformat(timespec="minutes"), dias=dias, cuota=cuota, avisos=avisos, canales=canales, videos=videos)
    os.makedirs(IDEAS, exist_ok=True)
    json.dump(out, open(os.path.join(IDEAS, alias + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"  {len(canales)} canales medidos, {len(videos)} videos recientes, ~{cuota} de cuota de YouTube", flush=True)
    return out


# ---------------------------------------------------------------- lo tuyo (datos del panel de estadísticas)
def propios(alias, cfg, ahora):
    ruta = os.path.join(es.DATOS, alias + ".json")
    if not os.path.isfile(ruta):
        return None
    d = json.load(open(ruta, encoding="utf-8"))
    formato = {x["id"]: x["formato"] for x in cfg.get("publicados", []) if x.get("id") and x.get("formato")}
    filas = []
    for v in d.get("videos", []):
        if v["estado"] != "public" or not v.get("fecha"):
            continue
        p = v["p"].get("90") or v["p"].get("28") or [None] * 4
        filas.append(dict(id=v["id"], titulo=v["titulo"], clase="short" if v.get("short") else "largo", vistas=v["vistas"],
                          edad=_edad(v["fecha"], ahora), visto=p[2], subs=p[3], formato=formato.get(v["id"])))
    med = {c: _mediana([f["vistas"] for f in filas if f["clase"] == c and f["edad"] >= MADURO]) for c in ("short", "largo")}
    for f in filas:
        f["x"] = round(f["vistas"] / max(med[f["clase"]], 1), 2)
    return dict(actualizado=d["actualizado"], suscriptores=d["suscriptores"], filas=filas, mediana=med)


# ---------------------------------------------------------------- informe
def _n(x):
    return "—" if x is None else f"{x:,.0f}".replace(",", " ")


def _t(s, n=70):
    s = s.replace("|", "/")
    return s if len(s) <= n else s[:n - 1] + "…"


def informe(alias, fuera):
    cfg, ahora = _cfg(alias), dt.datetime.now(dt.timezone.utc)
    op = cfg.get("ideas") or {}
    min_vistas = int(op.get("min_vistas", 1000))
    L = [f"# Ideas con datos — {cfg.get('nombre', alias)} ({ahora.astimezone().strftime('%d-%m-%Y')})", ""]

    yo = propios(alias, cfg, ahora)
    L += ["## 1. Lo tuyo"]
    if not yo:
        L += ["Sin datos del canal: `python fab.py canales --actualizar`.", ""]
    else:
        for clase, nombre in (("largo", "Largos"), ("short", "Shorts")):
            fs = sorted((f for f in yo["filas"] if f["clase"] == clase and f["edad"] >= MADURO), key=lambda f: -f["x"])
            if not fs:
                continue
            L += ["", f"**{nombre}: {len(fs)} videos con más de {MADURO} días, mediana {_n(yo['mediana'][clase])} vistas.**"
                  + ("  Muestra chica: son pistas, no conclusiones." if len(fs) < 8 else ""),
                  "", "| × mediana | vistas | % visto | subs | días | título |", "|---:|---:|---:|---:|---:|---|"]
            ver = fs if len(fs) <= 8 else fs[:5] + [None] + fs[-3:]
            for f in ver:
                L.append("| … | | | | | |" if f is None else
                         f"| ×{f['x']:g} | {_n(f['vistas'])} | {_n(f['visto'])} | {_n(f['subs'])} | {f['edad']:.0f} | {_t(f['titulo'])}"
                         + (f" `{f['formato']}`" if f["formato"] else "") + " |")
        grupos = {}
        for f in yo["filas"]:
            if f["formato"] and f["edad"] >= MADURO:
                grupos.setdefault(f["formato"], []).append(f)
        if grupos:
            L += ["", "**Por formato (apuestas anteriores):**", "", "| formato | videos | × mediana (mediana) | % visto (media) |", "|---|---:|---:|---:|"]
            for g, fs in sorted(grupos.items(), key=lambda x: -_mediana([f["x"] for f in x[1]])):
                vistos = [f["visto"] for f in fs if f["visto"] is not None]
                L.append(f"| {g} | {len(fs)} | ×{_mediana([f['x'] for f in fs]):g} | {_n(sum(vistos) / len(vistos)) if vistos else '—'} |")
        nuevos = [f for f in yo["filas"] if f["edad"] < MADURO]
        if nuevos:
            L += ["", f"Todavía sin madurar (< {MADURO} días): " + "; ".join(f"{_t(f['titulo'], 45)} ({_n(f['vistas'])})" for f in nuevos)]
        L += ["", f"Datos del canal del {yo['actualizado'].replace('T', ' ')}; {yo['suscriptores']} suscriptores.", ""]

    L += [f"## 2. Fuera: lo que rompió la media de su canal en los últimos {fuera['dias']} días", ""]
    cs = fuera["canales"]
    filtro = [p.lower() for p in op.get("filtro", [])]       # ruido de las búsquedas: el título debe traer alguna de estas palabras

    def del_nicho(v):
        return v["origen"] == "competidor" or not filtro or any(p in v["titulo"].lower() for p in filtro)
    buenos = sorted((v for v in fuera["videos"] if v["vistas"] >= min_vistas and v["x"] >= 1.5 and del_nicho(v)), key=lambda v: -v["x"])
    if not buenos:
        L += [f"Nada pasó de ×1,5 con al menos {min_vistas} vistas. Prueba otras búsquedas o agrega competidores.", ""]
    for clase, nombre in (("largo", "Largos"), ("short", f"Cortos (≤ {CORTO // 60} min)")):
        fs = [v for v in buenos if v["clase"] == clase][:20]
        if not fs:
            continue
        L += [f"**{nombre}**", "", "| × mediana | vistas | vistas/día | min | canal (subs) | título | enlace |", "|---:|---:|---:|---:|---|---|---|"]
        for v in fs:
            c = cs[v["canal"]]
            L.append(f"| ×{v['x']:g} | {_n(v['vistas'])} | {_n(v['vistas'] / max(_edad(v['fecha'], ahora), 1))} | {v['dur'] / 60:.1f} | "
                     f"{_t(c['nombre'], 28)} ({_n(c['subs'])}) | {_t(v['titulo'])} | https://youtu.be/{v['id']} |")
        L.append("")

    candidatos = sorted((c for c in cs.values() if not c["fijo"] and c["aciertos"] >= 2), key=lambda c: -c["aciertos"])[:8]
    if candidatos:
        L += ["## 3. Canales que se repiten en las búsquedas (candidatos a `competidores`)", ""]
        L += [f"- {c['nombre']} — {_n(c['subs'])} subs, {c['aciertos']} videos en las búsquedas, mediana largo {_n(c['mediana']['largo'])} / corto {_n(c['mediana']['short'])}"
              for c in candidatos]
        L.append("")
    if fuera["avisos"]:
        L += ["## Avisos", ""] + ["- " + a for a in fuera["avisos"]] + [""]
    L += ["## Cómo leerlo",
          "- **× mediana** compara cada video con lo normal de SU canal: mide el tema y el empaque (título, miniatura, gancho), no el tamaño del canal.",
          "- Pesa más un × alto en un canal chico (replicable) y un formato que aparece en VARIOS canales (no fue suerte).",
          "- De lo tuyo importa lo que repite: un formato con × alto y buen % visto se repite cambiando tema y gancho, con escenas nuevas.",
          f"- Datos de fuera del {fuera['fecha'][:16].replace('T', ' ')} UTC. Frescos: `python fab.py ideas {alias} --actualizar`."]
    texto = "\n".join(L) + "\n"
    os.makedirs(IDEAS, exist_ok=True)
    ruta = os.path.join(IDEAS, alias + ".md")
    open(ruta, "w", encoding="utf-8").write(texto)
    return texto, ruta


def lista():
    print(f"{'Canal':18s} {'Búsq.':>5s} {'Comp.':>5s}  Informe")
    for alias in es.alias_conocidos():
        op = _cfg(alias).get("ideas") or {}
        ruta = os.path.join(IDEAS, alias + ".json")
        fecha = json.load(open(ruta, encoding="utf-8"))["fecha"][:10] if os.path.isfile(ruta) else "—"
        print(f"{alias:18s} {len(op.get('busquedas', [])):>5d} {len(op.get('competidores', [])):>5d}  {fecha}")
    print("\nInforme de un canal: python fab.py ideas <alias> [--actualizar]")


def main():
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help", "ayuda"):
        print(__doc__)
        return
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--dias")]
    if not pos:
        return lista()
    alias = pos[0]
    if alias not in es.alias_conocidos():
        sys.exit(f"Canal desconocido '{alias}'. Opciones: {', '.join(es.alias_conocidos())}")
    dias = int(a[a.index("--dias") + 1]) if "--dias" in a else None
    ruta = os.path.join(IDEAS, alias + ".json")
    if "--actualizar" in a or dias or not os.path.isfile(ruta):
        print(f"Pidiendo a YouTube lo de fuera para {alias}…", flush=True)
        fuera = actualizar(alias, dias)
    else:
        fuera = json.load(open(ruta, encoding="utf-8"))
    texto, salida = informe(alias, fuera)
    print(texto)
    print("guardado:", os.path.relpath(salida, yt.RAIZ))


if __name__ == "__main__":
    main()
