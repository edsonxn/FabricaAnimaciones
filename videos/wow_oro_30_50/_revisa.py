# -*- coding: utf-8 -*-
"""Revisión de efectos.py ANTES de `fx hoja` (subagente C, 26-nov-2026; junta _huecos.py, _bordes.py y la regla de anclas únicas):
  1. ANCLAS: cada texto de en/de/a/marcas debe salir UNA sola vez en la voz (si no, `ancla()` toma la primera y el FX cae en
     otro puesto); marcas fuera de su FX (< 0 o > duración).
  2. HUECOS > 4 s sin pegatina, MG, mapa, pantalla, apoyo ni rótulo (regla del 3-nov).
  3. EFECTOS CORTOS (< 2,5 s) y rótulos sin `dur`.
  4. BORDES y ENCIMADOS: caja de lo nítido de cada MG/pegatina en 5 momentos (como _bordes.py) + caja de cada APOYO;
     fuera del 4 % del borde o dos a la vez que se pisan (> 8 % del menor).
  5. DENSIDAD por minuto (las clases de nucleo/chequeo_yt.py).
    python _revisa.py [--sin-bordes]      (desde la carpeta del video; escribe previews/revisa.txt)"""
import os
import re
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import secuencia_fx as SF  # noqa: E402

W, H = 1920, 1080
MARGEN = int(.04 * W) * 0 + 40          # 4 % del alto ≈ 43 px; se usa 40 px a cada lado
usos = {}
_orig = SF.Capa.ancla


def ancla(self, x):
    if isinstance(x, str) and not re.fullmatch(r"scene-\d{3,}(:fin)?", x):
        m = re.fullmatch(r"(.*?)(?:#(\d+))?(\|fin)?", x, re.S)
        aguja = [SF._norm(w) for w in m.group(1).split()]
        aguja = [w for w in aguja if w]
        if not m.group(2):
            n = sum(all(self.pal[i + j][0] == aguja[j] for j in range(len(aguja))) for i in range(len(self.pal) - len(aguja) + 1))
            usos[m.group(1)] = n
    return _orig(self, x)


SF.Capa.ancla = ancla
capa = SF.cargar()
mmss = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
L = []
rep = [k for k, n in usos.items() if n > 1]
L.append(f"ANCLAS: {len(usos)} textos · {len(rep)} repetidos")
for k in rep:
    L.append(f"  REPETIDA ×{usos[k]}: «{k}»")
for d in capa.fx:
    if d["tipo"] in ("mg", "pantalla"):
        dur = d["a"] - d["de"]
        for i, m in enumerate(d.get("_marcas", [])):
            if m < -.05 or m > dur + .05:
                L.append(f"  MARCA FUERA {mmss(d['de'])} {d.get('nombre')} marca {i}: {m:+.2f} s (dura {dur:.1f})")
        # la «madera» descifra el rótulo del último punto en ~2 s (hoja fx 26-nov: «LYNNORE Y XBDF» al salir)
        if "mapa madera" in (d.get("nombre") or "") and d.get("_marcas") and dur - max(d["_marcas"]) < 2.2:
            L.append(f"  MADERA CORTA {mmss(d['de'])} {d.get('nombre')}: {dur - max(d['_marcas']):.1f} s tras la última marca")

# ---------------------------------------------------------------- huecos
iv = [(d["de"], d["a"]) for d in capa.fx if d["tipo"] in ("mg", "pantalla", "imagen", "video")]
iv += [(r["de"], r["a"]) for r in capa.rot]
iv.sort()
t, huecos = 0.0, []
for de, a in iv:
    if de - t > 4:
        huecos.append((t, de))
    t = max(t, a)
if capa.total - t > 4:
    huecos.append((t, capa.total))
L.append(f"HUECOS > 4 s: {len(huecos)} ({sum(b - a for a, b in huecos):.0f} s)")
for a, b in huecos:
    L.append(f"  {mmss(a)}  {b - a:4.1f} s")

# ---------------------------------------------------------------- cortos
cortos = [d for d in capa.fx if d["tipo"] in ("mg", "pantalla", "imagen") and d["a"] - d["de"] < 2.5]
L.append(f"CORTOS < 2,5 s: {len(cortos)}")
for d in cortos:
    L.append(f"  {mmss(d['de'])} {d['a'] - d['de']:.1f} s  {d.get('nombre', d['tipo'])}")

# ---------------------------------------------------------------- bordes y encimados
if "--sin-bordes" not in sys.argv:
    def caja(img):
        a = img[..., 3].astype(np.int16)
        luz = img[..., :3].max(axis=2).astype(np.int16)
        m = (a > 200) & (luz > 110)
        if not m.any():
            return None
        ys, xs = np.nonzero(m)
        return xs.min(), ys.min(), xs.max(), ys.max()

    items = []
    for d in capa.fx:
        if d["tipo"] == "imagen":                       # apoyos (tooltips, fichas de interfaz)
            w = d.get("ancho", .5)
            w = w * W if w <= 1 else w
            try:
                from PIL import Image
                im = Image.open(d["ruta"])
                h = w * im.height / im.width
            except OSError:
                h = .30 * H
            cx, cy = d.get("x", .5) * W, d.get("y", .5) * H
            items.append(dict(nombre=f"apoyo {os.path.basename(d['ruta'])}", de=d["de"], a=d["a"], caja=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)))
            continue
        if d["tipo"] != "mg":
            continue
        dur = d["a"] - d["de"]
        union = None
        # pegatinas: solo en reposo (la entrada «cae/vuela» y la salida pasan fuera del cuadro a propósito); MG: todo el tramo
        muestras = (.3, .5, .7, .85) if (d.get("nombre") or "").startswith("pegatina") else (.15, .4, .65, .85, .97)
        for u in muestras:
            try:
                img = d["fn"](float(u * dur), float(dur), d["_marcas"])
            except Exception as e:      # noqa: BLE001
                L.append(f"  ERROR {mmss(d['de'])} {d.get('nombre')}: {e}")
                break
            c = caja(img)
            if c is None:
                continue
            cx, cy = d.get("x", .5) * W, d.get("y", .5) * H
            x0, y0 = cx - img.shape[1] / 2 + c[0], cy - img.shape[0] / 2 + c[1]
            x1, y1 = cx - img.shape[1] / 2 + c[2], cy - img.shape[0] / 2 + c[3]
            union = (x0, y0, x1, y1) if union is None else (min(union[0], x0), min(union[1], y0), max(union[2], x1), max(union[3], y1))
        if union:
            items.append(dict(nombre=d.get("nombre", "mg"), de=d["de"], a=d["a"], caja=union))
    for r in capa.rot:                                   # rótulos de texto: caja aproximada
        tam = r.get("tam", 120)
        w = len(r.get("texto", "")) * tam * .62
        cx, cy = r.get("x", .5) * W, r.get("y", .5) * H
        items.append(dict(nombre=f"ROTULO {r.get('texto')}", de=r["de"], a=r["a"], caja=(cx - w / 2, cy - tam * .6, cx + w / 2, cy + tam * .6)))
    fuera = enc = 0
    for it in items:
        x0, y0, x1, y1 = it["caja"]
        f = {k: round(v) for k, v in (("izq", MARGEN - x0), ("der", x1 - (W - MARGEN)), ("arriba", MARGEN - y0),
                                       ("abajo", y1 - (H - MARGEN))) if v > 0}
        if f:
            fuera += 1
            L.append(f"FUERA  {mmss(it['de'])}-{mmss(it['a'])}  {it['nombre']}  {f}")
    items.sort(key=lambda i: i["de"])
    for i, p in enumerate(items):
        for q in items[i + 1:]:
            if q["de"] >= p["a"]:
                break
            t = min(p["a"], q["a"]) - max(p["de"], q["de"])
            if t < .35:
                continue
            ax0, ay0, ax1, ay1 = p["caja"]
            bx0, by0, bx1, by1 = q["caja"]
            iw, ih = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
            if iw <= 0 or ih <= 0:
                continue
            menor = min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0))
            if iw * ih > .08 * menor:
                enc += 1
                L.append(f"ENCIMA {mmss(max(p['de'], q['de']))} ({t:.1f} s)  {p['nombre']}  ×  {q['nombre']}  ({iw * ih / menor:.0%})")
    L.append(f"BORDES: {len(items)} piezas · {fuera} fuera · {enc} encimadas")

# ---------------------------------------------------------------- densidad
import chequeo_yt as CH  # noqa: E402
import efectos as EF  # noqa: E402
cuenta = {}
for d in EF.FX:
    c = CH.clase(d)
    if c:
        cuenta[c] = cuenta.get(c, 0) + 1
mins = capa.total / 60
L.append("DENSIDAD por minuto: " + " · ".join(f"{c} {cuenta.get(c, 0) / mins:.1f} ({cuenta.get(c, 0)})"
                                               for c in ("fichas", "mg", "mapas", "pegatinas", "comentarios", "pantallas"))
         + f" · apoyos {len(EF.APOYOS) / mins:.1f} ({len(EF.APOYOS)})")
os.makedirs("previews", exist_ok=True)
open(os.path.join("previews", "revisa.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
