# -*- coding: utf-8 -*-
"""Comentarios de los canales (el usuario, 27-oct-2026; Warcraft, Tamriel, Runa Caída y Crónicas del gaming).

Dos usos:
  1. ANTES DE CADA VIDEO (28-oct-2026): de qué se queja la gente y qué sugiere con muchos ♥:
       python fab.py yt comentarios <canal> [dias]      -> canales/comentarios/<alias>.json + NUEVOS / QUEJAS / SUGERENCIAS
  2. Enseñar en el video el comentario de quien lo pidió, para que se sienta tomado en cuenta: tarjeta de comentario
     dibujada con los datos REALES (avatar, @usuario, texto, ♥) como pegatina de la plantilla yt:
       python fab.py yt comentario <video> <canal> <id del comentario>   -> videos/<video>/pegatinas/com_<id>.png
     y en efectos.py: peg(en, "com_<id>", "", tam=760, x=.30, y=.30)
Reglas: nunca inventar ni editar el texto (se puede cortar con «…»); nunca un comentario para burlarse de alguien;
solo comentarios de los últimos meses y públicos. Contestar se hace aparte, con borrador aprobado por el usuario.
"""
import datetime as dt
import io
import json
import os
import re
import sys
import textwrap

import requests
from PIL import Image, ImageDraw, ImageFont

try:
    import youtube as yt
except ImportError:
    from nucleo import youtube as yt

DIR = os.path.join(yt.CANALES, "comentarios")
_FD = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]


def _alias(cid):
    for f in os.listdir(yt.CANALES):
        if f.endswith(".json"):
            try:
                if json.load(open(os.path.join(yt.CANALES, f), encoding="utf-8")).get("canal_id") == cid:
                    return f[:-5]
            except (ValueError, OSError):
                pass
    return cid


def leer(cid, dias=21):
    """Hilos de comentarios de los últimos `dias` días; marca si el canal ya contestó."""
    lim = (dt.datetime.utcnow() - dt.timedelta(days=dias)).isoformat() + "Z"
    hilos, tok = [], None
    for _ in range(5):
        p = dict(part="snippet,replies", allThreadsRelatedToChannelId=cid, order="time", maxResults=100, textFormat="plainText")
        if tok:
            p["pageToken"] = tok
        r = yt.api(cid, "GET", "/commentThreads", params=p)
        hilos += r.get("items", [])
        tok = r.get("nextPageToken")
        if not tok or hilos[-1]["snippet"]["topLevelComment"]["snippet"]["publishedAt"] < lim:
            break
    out = []
    for h in hilos:
        top = h["snippet"]["topLevelComment"]
        s = top["snippet"]
        if s["publishedAt"] < lim or s.get("authorChannelId", {}).get("value") == cid:
            continue
        resp = h.get("replies", {}).get("comments", [])
        out.append(dict(id=top["id"], video=s.get("videoId"), autor=s["authorDisplayName"], avatar=s.get("authorProfileImageUrl"),
                        fecha=s["publishedAt"][:10], likes=s.get("likeCount", 0), texto=s["textDisplay"],
                        respuestas=h["snippet"]["totalReplyCount"],
                        contestado=any(c["snippet"].get("authorChannelId", {}).get("value") == cid for c in resp)))
    vids = sorted({c["video"] for c in out if c["video"]})
    tit = {}
    for i in range(0, len(vids), 50):
        for v in yt.api(cid, "GET", "/videos", params=dict(part="snippet", id=",".join(vids[i:i + 50]))).get("items", []):
            tit[v["id"]] = v["snippet"]["title"]
    for c in out:
        c["titulo"] = tit.get(c["video"], "")
    return out


# Pistas para clasificar (28-oct-2026). Solo ordenan la lectura: la conclusión sale de LEER los comentarios.
QUEJA = re.compile(r"\b(ia|ai|voz|voces|robot\w*|error\w*|errad\w*|falso|mentira\w*|se dice|se pronuncia|pronuncia\w*|"
                   r"te falt\w+|muy largo|redond\w+|aburr\w+|dislike|clickbait|no entend\w+|no tiene sentido|sin sonido|"
                   r"no tiene sonido|fuentes|despropósito|no sabes|no es lo tuyo|no entendiste)\b", re.I)
SUGERENCIA = re.compile(r"\b(haz|has un|hagas|deber[ií]as|podr[ií]as|pr[oó]ximo|ojal[aá]|v[ií]deo de|recomiendo|recomendar|"
                        r"estar[ií]a genial|toca la|toca el|habla de|hablar de|me gustar[ií]a|quisiera|siguiente|parte 2|"
                        r"segunda parte|te falt\w+|integraras|deber[ií]an)\b", re.I)


def _tiene(c, pistas):
    return bool(pistas.search(c["texto"]))


def _ver(c):
    return f"  ♥{c['likes']:<3} {'  ' if c['contestado'] else '· '}{c['id']}  {c['autor']}: {c['texto'][:110].replace(chr(10), ' ')}"


def guardar(canal, dias=21):
    """Lee, guarda y resume: NUEVOS desde la última lectura, QUEJAS y SUGERENCIAS (ordenadas por ♥)."""
    cid = yt.resolver_canal(canal)
    alias = _alias(cid)
    os.makedirs(DIR, exist_ok=True)
    ruta = os.path.join(DIR, f"{alias}.json")
    previo = json.load(open(ruta, encoding="utf-8")) if os.path.isfile(ruta) else {}
    visto = {c["id"]: c.get("visto", previo.get("fecha")) for c in previo.get("comentarios", [])}
    hoy = dt.date.today().isoformat()
    cs = leer(cid, dias)
    for c in cs:
        c["visto"] = visto.get(c["id"], hoy)
    json.dump(dict(fecha=hoy, dias=dias, comentarios=cs), open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nuevos = [c for c in cs if c["id"] not in visto] if visto else cs
    pend = [c for c in cs if not c["contestado"]]
    print(f"{alias}: {len(cs)} comentarios en {dias} d, {len(pend)} sin contestar, "
          f"{len(nuevos)} nuevos desde {previo.get('fecha', 'siempre')} -> {ruta}")
    porlikes = lambda xs: sorted(xs, key=lambda c: -c["likes"])
    for titulo, grupo, n in (("NUEVOS", nuevos, 25), ("QUEJAS (de qué se queja la gente)", [c for c in cs if _tiene(c, QUEJA)], 15),
                             ("SUGERENCIAS (lo que piden)", [c for c in cs if _tiene(c, SUGERENCIA)], 15)):
        print(f"\n{titulo}: {len(grupo)}")
        for c in porlikes(grupo)[:n]:
            print(_ver(c))
    return cs


# ---------------------------------------------------------------- tarjeta de comentario (pegatina)
def _f(nombres, tam):
    r = next((os.path.join(c, n) for n in nombres for c in _FD if os.path.exists(os.path.join(c, n))), "C:/Windows/Fonts/segoeui.ttf")
    return ImageFont.truetype(r, tam)


def _hace(fecha):
    d = (dt.date.today() - dt.date.fromisoformat(fecha)).days
    return "hoy" if d < 1 else f"hace {d} día{'s' if d > 1 else ''}" if d < 7 else f"hace {d // 7} semana{'s' if d >= 14 else ''}" \
        if d < 31 else f"hace {d // 30} mes{'es' if d >= 60 else ''}"


def _es_emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0xFE0F, 0x200D)


def _linea(d, x, y, texto, fuente, emo):
    """Texto con emojis (27-oct-2026: «☝🏻🧐» salía como cuadritos): los emojis van con Segoe UI Emoji a color."""
    trozos, act = [], ""
    for ch in texto:
        if 0x1F3FB <= ord(ch) <= 0x1F3FF:      # tono de piel: sin raqm sale como un cuadro suelto
            continue
        if act and _es_emoji(ch) != _es_emoji(act[-1]):
            trozos.append(act)
            act = ""
        act += ch
    if act:
        trozos.append(act)
    for t in trozos:
        if _es_emoji(t[0]):
            d.text((x, y + 2), t, font=emo, embedded_color=True)
            x += d.textlength(t, font=emo)
        else:
            d.text((x, y), t, font=fuente, fill=(241, 241, 241))
            x += d.textlength(t, font=fuente)


def tarjeta(c, salida, ancho=1000, max_lineas=5):
    """Tarjeta tipo comentario de YouTube (modo oscuro) con los datos REALES; PNG con transparencia."""
    nombre, cuerpo, meta = _f(("Roboto-Medium.ttf", "segoeuib.ttf"), 34), _f(("Roboto-Regular.ttf", "segoeui.ttf"), 38), \
        _f(("Roboto-Regular.ttf", "segoeui.ttf"), 30)
    lineas = []
    for parrafo in c["texto"].splitlines() or [""]:
        lineas += textwrap.wrap(parrafo, 44) or [""]
    if len(lineas) > max_lineas:
        lineas = lineas[:max_lineas]
        lineas[-1] = lineas[-1].rstrip(" .,") + "…"
    pad, av = 40, 96
    alto = pad * 2 + 50 + 52 * len(lineas) + 64
    im = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, ancho - 1, alto - 1), 28, fill=(15, 15, 15, 235), outline=(255, 255, 255, 40), width=2)
    try:
        foto = Image.open(io.BytesIO(requests.get(c["avatar"], timeout=20).content)).convert("RGBA").resize((av, av))
    except Exception:
        foto = Image.new("RGBA", (av, av), (90, 90, 110, 255))
    m = Image.new("L", (av, av), 0)
    ImageDraw.Draw(m).ellipse((0, 0, av - 1, av - 1), fill=255)
    im.paste(foto, (pad, pad), m)
    x = pad + av + 28
    d.text((x, pad - 2), c["autor"], font=nombre, fill=(241, 241, 241))
    d.text((x + d.textlength(c["autor"], font=nombre) + 16, pad + 2), _hace(c["fecha"]), font=meta, fill=(170, 170, 170))
    y = pad + 50
    emo = _f(("seguiemj.ttf",), 34)
    for ln in lineas:
        _linea(d, x, y, ln, cuerpo, emo)
        y += 52
    d.text((x, y + 14), f"👍  {c['likes']}" if c["likes"] else "👍", font=_f(("seguiemj.ttf",), 30), fill=(200, 200, 200),
           embedded_color=True)
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    im.save(salida)
    return salida


def pegatina(video, canal, id_com):
    """Busca el comentario en canales/comentarios/<alias>.json (o lo pide a la API) y deja la pegatina en el video."""
    cid = yt.resolver_canal(canal)
    ruta = os.path.join(DIR, f"{_alias(cid)}.json")
    cs = json.load(open(ruta, encoding="utf-8"))["comentarios"] if os.path.isfile(ruta) else []
    c = next((x for x in cs if x["id"] == id_com), None)
    if c is None:
        it = yt.api(cid, "GET", "/comments", params=dict(part="snippet", id=id_com, textFormat="plainText")).get("items", [])
        if not it:
            sys.exit(f"No encuentro el comentario {id_com}")
        s = it[0]["snippet"]
        c = dict(id=id_com, autor=s["authorDisplayName"], avatar=s.get("authorProfileImageUrl"), fecha=s["publishedAt"][:10],
                 likes=s.get("likeCount", 0), texto=s["textDisplay"])
    sal = tarjeta(c, os.path.join(yt.RAIZ, "videos", video, "pegatinas", f"com_{id_com}.png"))
    print(f"pegatina -> {sal}\n  en efectos.py: peg(<seg>, \"com_{id_com}\", \"\", tam=760, x=.30, y=.30)")
