"""Compara YouTube contra lo registrado en canales/<alias>.json (`publicados`). SOLO LECTURA.

Uso (desde C:\\FabricaAnimaciones):
  python .claude\\skills\\actualizar-canales\\diferencias.py [alias ...] [--dias 14]

Sin alias recorre todos los canales conectados. Por canal informa:
  NUEVO     video subido en los últimos --dias días que no está en `publicados` (+ carpeta probable en videos/)
  CAMBIO    estado real en YouTube distinto del registrado (salió público, programado, otra fecha, volvió a privado)
  BORRADO   id registrado que ya no existe en el canal (¿lo borró el usuario en Studio?)
  Al final, por canal, la lista de lo que está privado SIN programar (lo que espera decisión del usuario).
No escribe nada: ni en YouTube ni en disco. Registrar lo hallado es trabajo del skill (SKILL.md).
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "nucleo"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import youtube as y  # noqa: E402


def _dur(iso):
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return iso or "?"
    h, mi, s = (int(x or 0) for x in m.groups())
    return f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"


def _norm(t):
    return re.sub(r"\W+", " ", (t or "").lower()).strip()


def _estado_real(v):
    st = v["status"]
    if st.get("publishAt"):
        return "programado", st["publishAt"]
    return st["privacyStatus"], None


def _carpetas_por_titulo():
    d = {}
    for f in glob.glob(os.path.join(RAIZ, "videos", "*", "youtube.json")):
        try:
            t = json.load(open(f, encoding="utf-8")).get("titulo")
        except Exception:
            continue
        if t:
            d[_norm(t)] = os.path.basename(os.path.dirname(f))
    return d


def _lotes(ids, n=50):
    for i in range(0, len(ids), n):
        yield ids[i:i + n]


def _registrado_dice(e):
    """Texto corto de lo que dice el registro (los canales usan campos distintos)."""
    partes = [str(e.get("visibilidad") or e.get("estado") or "?")]
    for k in ("programado", "publicar", "hueco_sugerido", "publicado"):
        if e.get(k):
            partes.append(f"{k}={e[k]}")
    return " ".join(partes)


def _ahora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _clasificar(e, real, cuando):
    """Devuelve None si el registro concuerda con YouTube, o ('SALIÓ'|'CAMBIO', explicación).
    Los canales usan campos distintos: visibilidad (public/private/programado/privado), programado, publicar,
    publicado (fecha = ya es público) y estado."""
    vis = str(e.get("visibilidad") or e.get("estado") or "").lower()
    fecha = e.get("programado") or e.get("publicar")
    dice_publico = vis in ("public", "publico", "público") or bool(e.get("publicado"))
    if real == "public":
        if dice_publico and not (fecha and fecha > _ahora()):
            return None
        if fecha and fecha > _ahora():
            return "SALIÓ", "antes de lo programado"
        return "SALIÓ", "ya es público (el registro lo da por privado/programado)"
    if real == "programado":
        if (fecha or "")[:16] == (cuando or "")[:16] and not dice_publico:
            return None
        return "CAMBIO", f"en YouTube está programado para {cuando}"
    # privado / no listado
    if dice_publico or fecha:
        return "CAMBIO", f"en YouTube está {real} y sin fecha"
    return None


def revisar(alias, dias, carpetas):
    ruta = os.path.join(RAIZ, "canales", f"{alias}.json")
    cfg = json.load(open(ruta, encoding="utf-8"))
    cid = cfg["canal_id"]
    reg = cfg.get("publicados", [])
    ids_reg = [e["id"] for e in reg if e.get("id")]
    print(f"\n== {alias} ({cfg.get('nombre', '')}) · {len(ids_reg)} registrados ==")

    # estado real de lo registrado (consulta por id: detecta también los borrados)
    real = {}
    for lote in _lotes(ids_reg):
        r = y.api(cid, "GET", "/videos", params=dict(part="snippet,status,contentDetails", id=",".join(lote)))
        for v in r.get("items", []):
            real[v["id"]] = v

    hubo = False
    ultimo = {}
    for e in reg:  # un id puede estar dos veces (subido, luego programado): manda la última entrada
        if e.get("id"):
            ultimo[e["id"]] = e
    for vid, e in ultimo.items():
        v = real.get(vid)
        if v is None:
            if str(e.get("visibilidad", "")).lower() == "borrado":
                continue  # ya anotado como borrado
            print(f"BORRADO  {vid}  «{e.get('titulo', '')}»  (registrado: {_registrado_dice(e)})")
            hubo = True
            continue
        est, cuando = _estado_real(v)
        c = _clasificar(e, est, cuando)
        if c:
            extra = f"  publicado {v['snippet'].get('publishedAt', '')}" if est == "public" else ""
            print(f"{c[0]:8s} {vid}  «{e.get('titulo', '')}»  {c[1]}{extra}  (registrado: {_registrado_dice(e)})")
            hubo = True

    # subidas viejas que el usuario debía borrar en Studio (`duplicados_para_borrar`)
    dups = [d for d in cfg.get("duplicados_para_borrar", []) if d.get("id")]
    if dups:
        vivos = set()
        for lote in _lotes([d["id"] for d in dups]):
            r = y.api(cid, "GET", "/videos", params=dict(part="status", id=",".join(lote)))
            vivos |= {v["id"] for v in r.get("items", [])}
        for d in dups:
            if d["id"] in vivos:
                print(f"POR BORRAR  {d['id']}  (sigue en el canal; el usuario la borra en Studio)")
            else:
                print(f"DUPLICADO YA BORRADO  {d['id']}  (quitar de duplicados_para_borrar)")
                hubo = True

    # videos recientes sin registrar
    up = y.api(cid, "GET", "/channels", params=dict(part="contentDetails", id=cid))["items"][0]
    lista = up["contentDetails"]["relatedPlaylists"]["uploads"]
    items = y.api(cid, "GET", "/playlistItems", params=dict(part="contentDetails", playlistId=lista, maxResults=50)).get("items", [])
    ids_up = [i["contentDetails"]["videoId"] for i in items]
    nuevos = [i for i in ids_up if i not in ids_reg]
    corte = (datetime.now(timezone.utc) - timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")
    antiguos = 0
    for lote in _lotes(nuevos):
        r = y.api(cid, "GET", "/videos", params=dict(part="snippet,status,contentDetails", id=",".join(lote)))
        for v in r.get("items", []):
            est, cuando = _estado_real(v)
            sub = v["snippet"].get("publishedAt", "")
            if sub < corte and not cuando:
                antiguos += 1
                continue
            carpeta = carpetas.get(_norm(v["snippet"]["title"]), "?")
            print(f"NUEVO    {v['id']}  {est}{' ' + cuando if cuando else ''}  subido {sub}  "
                  f"{_dur(v['contentDetails'].get('duration'))}  «{v['snippet']['title']}»  → videos/{carpeta}")
            hubo = True
    if antiguos:
        print(f"         ({antiguos} videos más antiguos que {dias} d sin registrar: se ignoran)")

    # privados sin programar = esperan decisión del usuario
    esperan = []
    for vid, v in real.items():
        est, _ = _estado_real(v)
        if est == "private":
            esperan.append(f"{vid} «{v['snippet']['title']}»")
    if esperan:
        print("SIN PROGRAMAR (privados registrados):")
        for t in esperan:
            print("   -", t)
    if not hubo:
        print("sin diferencias")


def main(argv):
    dias = 14
    if "--dias" in argv:
        i = argv.index("--dias")
        dias = int(argv[i + 1])
        del argv[i:i + 2]
    alias = argv or sorted(
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(os.path.join(RAIZ, "canales", "*.json"))
        if "canal_id" in json.load(open(f, encoding="utf-8"))
    )
    carpetas = _carpetas_por_titulo()
    for a in alias:
        try:
            revisar(a, dias, carpetas)
        except (RuntimeError, SystemExit, KeyError) as e:
            print(f"\n== {a} == ERROR: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
