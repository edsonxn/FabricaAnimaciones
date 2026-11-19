# -*- coding: utf-8 -*-
"""Arte de «La obra» (vista RTS del panel y de la tele): recorta los dibujos de Flow (fondo magenta) en sprites PNG con
transparencia y hace las texturas de suelo repetibles.

  python nucleo/obra/preparar_arte.py           flow/*.jpg  ->  img/*.png  (+ img/hoja.jpg para revisarlos)
  python nucleo/obra/preparar_arte.py aldeanos [--sin-html]  flow/ald_<anim>.jpg -> img/ald_<anim>[_0-7].png + aldeanos.json
                                                (+ img/hoja_aldeanos.jpg; escribe ALD_META en panel_obra.html)

Los originales de Flow (Nano Banana 2.1, 19-nov-2026; prompts en el docstring de abajo) viven en flow/. Estilo pedido:
«classic late-1990s isometric medieval real-time strategy», arte nuevo, nada copiado de ningún juego.
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
FLOW = os.path.join(AQUI, "flow")
IMG = os.path.join(AQUI, "img")

# hoja -> nombres de sus piezas en orden de lectura (filas de arriba abajo, luego izquierda a derecha); alto final en px
HOJAS = {
    "edificio_1": (["cimientos"], 330),
    "edificio_2": (["armazon"], 400),
    "edificio_3": (["taller"], 400),
    "recursos": (["madera", "silicio", "componentes", "pelicula"], 120),
    "adornos": (["roca", "piedras", "arbusto", "arbusto_flor", "tocon", "barril", "cajas", "carretilla", "costal", "cerca"], 70),
    "arboles": (["roble", "pino", "abedul", "castano", "pino_chico", "arce"], 210),
}
# alto propio de algunas piezas (relativo al de su hoja)
ALTO = {"piedras": 40, "cerca": 55, "costal": 50, "barril": 55, "pino_chico": 150, "arbusto": 60, "arbusto_flor": 60, "roca": 70}


def alfa(rgb):
    """Transparencia por distancia al magenta, con borde suave y sin halo rosa (despill)."""
    a = rgb.astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = np.minimum(r, b) - g                     # cuánto «magenta» tiene el pixel
    al = np.clip(1 - (m - 60) / 90, 0, 1)        # m >= 150: fondo; m <= 60: objeto
    tope = np.maximum(g, np.minimum(r, b) - np.clip(m, 0, None) * (1 - al))
    a[..., 0] = np.minimum(r, np.maximum(tope, g + (r - g) * al))
    a[..., 2] = np.minimum(b, np.maximum(tope, g + (b - g) * al))
    return np.dstack([np.clip(a, 0, 255), al * 255]).astype(np.uint8)


def piezas(rgba, n):
    """Las `n` manchas más grandes (cada una con sus pedacitos cercanos), en orden de lectura."""
    sol = rgba[..., 3] > 40
    lab, k = ndimage.label(ndimage.binary_dilation(sol, iterations=9))
    tam = ndimage.sum(sol, lab, range(1, k + 1))
    mayores = sorted(np.argsort(tam)[::-1][:n] + 1)
    cajas = [ndimage.find_objects((lab == i).astype(int))[0] for i in mayores]
    alto = rgba.shape[0]
    cajas.sort(key=lambda s: (round((s[0].start + s[0].stop) / 2 / (alto / 2.2)), s[1].start))   # filas, luego x
    out = []
    for s in cajas:
        i = lab[s]
        mancha = np.bincount(i[i > 0].ravel()).argmax()
        p = rgba[s].copy()
        p[..., 3] = np.where(i == mancha, p[..., 3], 0)
        out.append(p)
    return out


def recortar(p):
    ys, xs = np.nonzero(p[..., 3] > 8)
    return p[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def repetible(ruta, lado=512):
    """Textura que se repite sin costura: centro del dibujo mezclado con su versión desplazada media vuelta."""
    im = np.asarray(Image.open(ruta).convert("RGB"), dtype=np.float32)
    h, w = im.shape[:2]
    c = im[(h - lado) // 2:(h + lado) // 2, (w - lado) // 2:(w + lado) // 2]
    rod = np.roll(c, (lado // 2, lado // 2), axis=(0, 1))
    t = np.linspace(0, 1, lado)
    peso = (1 - np.abs(2 * t - 1))
    wgt = np.clip(np.outer(peso, peso) * 3, 0, 1)[..., None]
    return Image.fromarray((c * wgt + rod * (1 - wgt)).astype(np.uint8))


# ------------------------------------------------------------------ aldeanos (hojas de animación de Flow, 19-nov-2026)
# Cada hoja: el mismo aldeano mirando a la derecha, túnica azul pura (#1f4fff) para teñirla con el color del canal.
ALDEANOS = {"caminar": 12, "cargar": 8, "hacha": 6, "martillo": 6, "recoger": 6, "pico": 6,
            # ocio (19-nov, el usuario: «cuando un aldeano esté inactivo ponlo dormido o sentado con alguna animación»)
            "dormir": 6, "sentado": 6, "estirarse": 6, "platicar": 6}
# cuadros reordenados para que todas las herramientas sigan el convenio del hacha: golpe = cuadro 4, recupera = 5
ORDEN = {"pico": [0, 2, 3, 4, 5, 1]}
POR_AREA = ("dormir", "sentado")
ALD_ALTO = 80            # alto del aldeano de pie en el archivo (en pantalla, la mitad)
# los 8 colores de canal de panel_obra.html (const COL)
COL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]


def _hsv(rgb):
    r, g, b = [rgb[..., i] / 255.0 for i in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    return h, np.where(mx > 0, (mx - mn) / (mx + 1e-6), 0), mx


def _rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
    sel = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    out = np.zeros(h.shape + (3,))
    for k, trio in enumerate(sel):
        m = i == k
        for c in range(3):
            out[..., c][m] = trio[c][m]
    return np.clip(out * 255, 0, 255)


def tunica(rgb):
    """Peso 0..1 de «túnica azul» por pixel (borde suave contra piel, cinturón y contorno)."""
    h, s, v = _hsv(rgb.astype(np.float32))
    dh = np.abs(h - 0.632)                                     # tono de #1f4fff
    return np.clip(1 - (dh - 0.05) / 0.05, 0, 1) * np.clip((s - 0.35) / 0.2, 0, 1) * np.clip((v - 0.12) / 0.12, 0, 1)


def tenir(rgba, hexcol):
    """La túnica con el tono del canal: mismo sombreado, saturación y brillo escalados a los del color destino."""
    rgb = rgba[..., :3].astype(np.float32)
    w = tunica(rgb)[..., None]
    h, s, v = _hsv(rgb)
    n = int(hexcol[1:], 16)
    th, ts, tv = [x.item() for x in _hsv(np.array([[[n >> 16, n >> 8 & 255, n & 255]]], dtype=np.float32))]
    nuevo = _rgb(np.full_like(h, th), np.clip(s * ts / 0.88, 0, 1), np.clip(v * tv, 0, 1))
    out = rgba.copy()
    out[..., :3] = np.clip(rgb * (1 - w) + nuevo * w, 0, 255).astype(np.uint8)
    return out


def cuadros(hoja):
    """Cuadros de una hoja: [(rgba recortado, ancla_x, ancla_y)] en orden de lectura, a escala de archivo."""
    rgb = np.asarray(Image.open(os.path.join(FLOW, hoja + ".jpg")).convert("RGB"))
    rgba = alfa(rgb)
    sol = rgba[..., 3] > 40
    tun = (tunica(rgb) > 0.5) & sol
    tun = ndimage.binary_opening(tun, iterations=1)
    lt, k = ndimage.label(ndimage.binary_dilation(tun, structure=np.ones((31, 7))))   # une túnica arriba/abajo del cinturón y mangas
    lt = np.where(tun, lt, 0)
    tam = ndimage.sum(tun, lt, range(1, k + 1))
    ids = [i + 1 for i in range(k) if tam[i] > 0.25 * tam.max()]
    cen = ndimage.center_of_mass(tun, lt, ids)                 # (y, x) de cada túnica
    bb = ndimage.find_objects(lt)
    alt_t = np.median([bb[i - 1][0].stop - bb[i - 1][0].start for i in ids])
    area_t = float(np.median([tam[i - 1] for i in ids]))       # para acostado/sentado (la túnica cambia de forma)
    filas = []                                                 # agrupar túnicas en filas por su y
    for j in sorted(range(len(ids)), key=lambda j: cen[j][0]):
        if filas and abs(cen[j][0] - np.mean([cen[q][0] for q in filas[-1]])) < alt_t:
            filas[-1].append(j)
        else:
            filas.append([j])
    orden = [j for f in filas for j in sorted(f, key=lambda q: cen[q][1])]
    # cada pedazo sólido va con la túnica que contiene (o la más cercana: cajas, herramientas sueltas)
    ls, m = ndimage.label(ndimage.binary_dilation(sol, iterations=2))
    dueno = np.zeros(m + 1, int) - 1
    cy, cx = np.array([c[0] for c in cen]), np.array([c[1] for c in cen])
    partido = {}
    for p in range(1, m + 1):
        dentro = [j for j, i in enumerate(ids) if np.any(tun & (ls == p) & (lt == i))]
        if len(dentro) == 1:
            dueno[p] = dentro[0]
        elif len(dentro) > 1:
            partido[p] = dentro                                # dos cuadros pegados: se parte por columnas
        else:
            yy, xx = ndimage.center_of_mass(sol & (ls == p))
            if np.isnan(yy):
                continue
            dueno[p] = int(np.argmin(np.hypot((cy - yy) * 2, cx - xx)))
    asig = np.where(sol, dueno[ls], -1)
    X = np.arange(rgb.shape[1])[None, :].repeat(rgb.shape[0], 0)
    for p, js in partido.items():
        js = sorted(js, key=lambda q: cx[q])
        cortes = [(cx[a] + cx[b]) / 2 for a, b in zip(js, js[1:])]
        zona = (ls == p) & sol
        asig[zona] = np.array(js)[np.searchsorted(cortes, X[zona])]
    alto_pie = []
    for j in orden:
        msk = asig == j
        ys, xs = np.nonzero(tun & (lt == ids[j]))
        col = msk[:, max(0, xs.min()):xs.max() + 1]           # piso = fila más baja bajo la túnica (botas)
        alto_pie.append(np.nonzero(col.any(1))[0].max())
    # piso común por fila de la hoja (la mediana: el pie levantado o el hacha abajo no lo mueven)
    piso = {}
    for f in filas:
        med = np.median([alto_pie[orden.index(j)] for j in f])
        for j in f:
            piso[j] = med
    # escala: el aldeano de pie (cabeza a botas) mide ALD_ALTO
    persona = np.median([alto_pie[orden.index(j)] - np.nonzero((asig == j).any(1))[0].min() for j in orden])
    k = ALD_ALTO / persona if hoja in ("ald_caminar", "ald_cargar") else None
    out = []
    for j in orden:
        msk = asig == j
        ys, xs = np.nonzero(msk)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        p = rgba[y0:y1, x0:x1].copy()
        p[..., 3] = np.where(msk[y0:y1, x0:x1], p[..., 3], 0)
        out.append((p, cx[j] - x0, piso[j] - y0 + 1))
    return out, k, (alt_t, area_t)


def aldeanos(escribir_html=True):
    """flow/ald_<anim>.jpg -> img/ald_<anim>.png (tira de cuadros iguales) + 8 tintas + img/aldeanos.json."""
    import json
    datos, hechas = {}, {}
    k_ref = t_ref = None
    for anim, n in ALDEANOS.items():
        if not os.path.exists(os.path.join(FLOW, f"ald_{anim}.jpg")):
            print(f"  ald_{anim}: no hay hoja en flow/ (se usa otra animación)")
            continue
        cs, k, alt_t = cuadros(f"ald_{anim}")
        if len(cs) != n:
            print(f"  ¡ald_{anim}: salieron {len(cs)} cuadros y esperaba {n}!")
        if k is not None and k_ref is None:
            k_ref, t_ref, a_ref = k, alt_t[0], alt_t[1]
        if anim in ORDEN and len(cs) == len(ORDEN[anim]):
            cs = [cs[i] for i in ORDEN[anim]]
        hechas[anim] = (cs, alt_t[0], alt_t[1])
    for anim, (cs, alt_t, area_t) in hechas.items():
        if anim in POR_AREA:                                   # acostado o sentado: misma cantidad de túnica
            esc = k_ref * (a_ref / area_t) ** 0.5
        else:
            esc = k_ref * t_ref / alt_t                        # misma túnica = mismo tamaño en todas las hojas
        izq = max(ax for _, ax, _ in cs) * esc
        der = max(p.shape[1] - ax for p, ax, _ in cs) * esc
        arr = max(ay for _, _, ay in cs) * esc
        aba = max(p.shape[0] - ay for p, _, ay in cs) * esc
        W, H, AX, AY = int(np.ceil(izq + der)) + 2, int(np.ceil(arr + aba)) + 2, int(np.ceil(izq)) + 1, int(np.ceil(arr)) + 1
        tira = Image.new("RGBA", (W * len(cs), H), (0, 0, 0, 0))
        for i, (p, ax, ay) in enumerate(cs):
            im = Image.fromarray(p)
            im = im.resize((max(1, round(im.width * esc)), max(1, round(im.height * esc))), Image.LANCZOS)
            tira.alpha_composite(im, (i * W + AX - round(ax * esc), AY - round(ay * esc)))
        tira.save(os.path.join(IMG, f"ald_{anim}.png"), optimize=True)
        base = np.asarray(tira)
        for c, hx in enumerate(COL):
            Image.fromarray(tenir(base, hx)).save(os.path.join(IMG, f"ald_{anim}_{c}.png"), optimize=True)
        datos[anim] = {"n": len(cs), "w": W, "h": H, "ax": AX, "ay": AY}
        print(f"  ald_{anim:9s} {len(cs)} cuadros de {W}x{H}, ancla ({AX},{AY})")
    with open(os.path.join(IMG, "aldeanos.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    # las medidas también van dentro de panel_obra.html (la línea «const ALD_META = …; // ALD_META»)
    import re
    html = os.path.join(os.path.dirname(AQUI), "panel_obra.html")
    t = open(html, encoding="utf-8").read()
    t2 = re.sub(r"const ALD_META = .*?; // ALD_META", "const ALD_META = " + json.dumps(datos, separators=(",", ":")) + "; // ALD_META", t)
    if escribir_html and t2 != t:
        open(html, "w", encoding="utf-8", newline="").write(t2)
        print("  panel_obra.html: ALD_META al día")
    # hoja de revisión: cada tira en 2 tintas sobre pasto gris
    filas = [Image.open(os.path.join(IMG, f"ald_{a}_{c}.png")) for a in datos for c in (0, 3)]
    Wt = max(f.width for f in filas)
    rev = Image.new("RGB", (Wt, sum(f.height + 6 for f in filas)), (96, 110, 96))
    y = 0
    for f in filas:
        rev.paste(f, (0, y), f)
        y += f.height + 6
    rev.save(os.path.join(IMG, "hoja_aldeanos.jpg"), quality=82)


def main():
    import sys
    os.makedirs(IMG, exist_ok=True)
    if sys.argv[1:2] == ["aldeanos"]:
        aldeanos(escribir_html="--sin-html" not in sys.argv)
        return
    hechos = []
    for hoja, (nombres, alto) in HOJAS.items():
        rgba = alfa(np.asarray(Image.open(os.path.join(FLOW, hoja + ".jpg")).convert("RGB")))
        ps = piezas(rgba, len(nombres))
        if len(ps) != len(nombres):
            print(f"  ¡{hoja}: salieron {len(ps)} piezas y esperaba {len(nombres)}!")
        for nom, p in zip(nombres, ps):
            im = Image.fromarray(recortar(p))
            h = ALTO.get(nom, alto) * 2                 # el doble: se ve nítido de cerca y la tele lo reduce
            im = im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
            im.save(os.path.join(IMG, nom + ".png"), optimize=True)
            hechos.append(nom)
            print(f"  {nom:14s} {im.width}x{im.height}")
    for t in ("pasto", "tierra"):
        repetible(os.path.join(FLOW, t + ".jpg")).save(os.path.join(IMG, t + ".jpg"), quality=88)
    # hoja de revisión sobre gris, para mirar los bordes a mano
    ims = [Image.open(os.path.join(IMG, n + ".png")) for n in hechos]
    W = 1600
    hoja = Image.new("RGB", (W, 900), (96, 110, 96))
    x = y = fila = 0
    for im in ims:
        im.thumbnail((180, 180))
        if x + im.width > W:
            x, y, fila = 0, y + fila + 10, 0
        hoja.paste(im, (x, y), im)
        x += im.width + 10
        fila = max(fila, im.height)
    hoja.save(os.path.join(IMG, "hoja.jpg"), quality=80)


if __name__ == "__main__":
    main()
