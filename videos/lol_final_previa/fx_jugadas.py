# -*- coding: utf-8 -*-
"""Montaje de las JUGADAS de lol_final_previa: j1, j3_ctx, j3, j3_fin, j2, j4, j5, j6_ctx, j6, j6_fin (el resto, fx_escenas.py).
Lo ejecuta efectos.py con exec en su propio espacio: FX, AZUL, K, J, CLIP, TRAMO, SYNC, PZ, REBX, LENTA, MESA2, V3, VIVO, an, anillo,
flecha, intencion, zona, texto, tar, peg, cam, marcador() (FORMA 4), oro() (FORMA 5), TIEMPOS_3D, T0/T1/W/NX/ESC… vienen de allí.

FORMAS (ESTADO § Presentación ELEGIDA; se SUMAN al estilo): 4 (marcador) y 5 (oro del feed) en las seis jugadas;
  j1 = 3 · j2 = 2 + 6 · j3 = 1 + 8 + 2 (dentro de j3_3d.mp4) · j4 = 3 + 6 · j5 = 2 + 3 · j6 = 1 + 6 + 8 (dentro de j6_3d.mp4).
  FORMA 3 (pantalla dividida) = VENTANAS(): el VOD a cuadro entero + 2 ventanas con zoom que siguen a cada protagonista, como FX
  `mg` que lee el MISMO segundo del mp4 con cv2 (caché por proceso) y recorta en la posición MEDIDA del jugador (cuerpo, desde su
  placa en investigacion/../previews/cuadros/r_jN_<t>.jpg), interpolada entre cuadros medidos DENTRO de la misma toma.
  FORMA 6 = flecha fantasma blanca discontinua rotulada «LO QUE PODÍA HACER» / «POSIBILIDAD, NO LO QUE PASÓ» (j2, j4).
  FORMA 2 = MESA2(…) con cam="bullet" en mesas_3d.py (j2b en j2.mp4 t 69 · j5a en j5.mp4 t 46: los 10 medidos).
  FORMA 1 = el 3D entra desde el cuadro del juego (el VOD congelado se funde encima) y vuelve a él (TIEMPOS_3D → j3_3d/j6_3d.py).
Reglas: anillos solo en PIES medidos (datos_jN.md o rejilla2.py a 1280 px); rutas solo medidas; NUNCA más de x1 (SYNC/TRAMO
cortan); cada tramo sigue en el cuadro exacto de la pausa; repeticiones rotuladas; colores = lado del mapa (AZUL por partida).
"""
import cv2 as _cv2
import numpy as _np
from PIL import Image as _Img, ImageDraw as _Draw, ImageFilter as _Filt

K.update({"j1": 1490.7, "j2": 910.0, "j3": 1760.3, "j4": 1802.0, "j5": 1904.0, "j6": 1860.0, "j6_fin": 2249.0, "j6_baron": 1719.0})
BL = "blanco"


# ───────────────────────────────────────── FORMA 3 · pantalla dividida (ventanas con zoom) ─────────────────────────────────
_VCAP = {}          # ruta → [cap, fps, índice, cuadro]  (cada proceso de render tiene el suyo)
_VMARCO = {}


def _leer(ruta, s):
    c = _VCAP.get(ruta)
    if c is None:
        cap = _cv2.VideoCapture(ruta)
        c = _VCAP[ruta] = [cap, cap.get(_cv2.CAP_PROP_FPS) or 30.0, -1, None]
    obj = max(0, int(round(s * c[1])))
    if obj < c[2] or obj > c[2] + 90:
        c[0].set(_cv2.CAP_PROP_POS_FRAMES, obj)
        c[2] = obj - 1
    while c[2] < obj:
        ok, f = c[0].read()
        if not ok:
            break
        c[2], c[3] = c[2] + 1, f
    return c[3]


def _pos(keys, s):
    """posición medida (fracción) interpolada en el segundo s de la fuente, suavizada (media de ±0,35 s)"""
    def lin(u):
        if u <= keys[0][0]:
            return keys[0][1], keys[0][2]
        for (a, x0, y0), (b, x1, y1) in zip(keys, keys[1:]):
            if u <= b:
                k = (u - a) / (b - a) if b > a else 1.0
                return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
        return keys[-1][1], keys[-1][2]
    ps = [lin(s + d) for d in (-.35, -.17, 0, .17, .35)]
    return sum(p[0] for p in ps) / 5, sum(p[1] for p in ps) / 5


def _marco(nombre, sub, color, w, h):
    """sombra + filo dorado + placa de vidrio azul noche con el nombre (lenguaje de mg_lol); BGRA float, máscara del video"""
    k = (nombre, sub, color, w, h)
    if k in _VMARCO:
        return _VMARCO[k]
    M = 24
    W_, H_ = w + 2 * M, h + 2 * M
    sm = _Img.new("L", (W_, H_), 0)
    _Draw.Draw(sm).rectangle([M + 5, M + 9, M + w + 5, M + h + 9], fill=175)
    base = _Img.new("RGBA", (W_, H_), (0, 0, 0, 0))
    base.putalpha(sm.filter(_Filt.GaussianBlur(11)))
    ov = _Img.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = _Draw.Draw(ov)
    col = L.COL.get(color, L.ORO)
    d.rectangle([M - 2, M - 2, M + w + 1, M + h + 1], outline=L.ORO + (235,), width=3)
    d.rectangle([M + 1, M + 1, M + w - 2, M + h - 2], outline=(0, 0, 0, 120), width=1)
    d.polygon([(M + w - 34, M - 2), (M + w + 1, M - 2), (M + w + 1, M + 33)], fill=L.ORO + (235,))
    d.rectangle([M - 2, M - 2, M + 5, M + h + 1], fill=col + (255,))                       # barra del color del lado
    fn_, fs_ = L.fuente("Bold Condensed", 30), L.fuente("SemiBold Condensed", 19)
    tw = max(d.textlength(nombre.upper(), font=fn_), d.textlength((sub or "").upper(), font=fs_)) + 34
    py = M + h - 70
    d.rectangle([M + 12, py, M + 12 + tw, py + 58], fill=(9, 16, 32, 228), outline=L.ORO + (150,), width=1)
    d.rectangle([M + 12, py, M + 17, py + 58], fill=col + (255,))
    L._texto(d, (M + 28, py + 4), nombre.upper(), fn_, (245, 245, 250), "la", track=1)
    if sub:
        L._texto(d, (M + 28, py + 36), sub.upper(), fs_, col, "la", track=1)
    tag = "ZOOM"
    ft = L.fuente("Bold Condensed", 17)
    d.rectangle([M + 12, M + 10, M + 24 + d.textlength(tag, font=ft), M + 34], fill=(9, 16, 32, 210))
    L._texto(d, (M + 18, M + 12), tag, ft, L.ORO_C, "la", track=2)
    b = _np.asarray(base, _np.float32)[..., [2, 1, 0, 3]].copy()
    o = _np.asarray(ov, _np.float32)[..., [2, 1, 0, 3]].copy()
    _VMARCO[k] = (b, o, M)
    return _VMARCO[k]


def _ventana(ruta, desde, keys, nombre, sub, color, z, w, h):
    def fn(dt, dur, marcas):
        s = desde + max(0.0, dt)
        f = _leer(ruta, s)
        b, o, M = _marco(nombre, sub, color, w, h)
        out = b.copy()
        if f is not None:
            FH, FW = f.shape[:2]
            cx, cy = _pos(keys, s)
            cw, ch = FW / z, FH / z
            x0 = min(max(cx * FW - cw / 2, 0), FW - cw)
            y0 = min(max(cy * FH - ch / 2, 0), FH * .78 - ch)       # sin la franja del HUD de abajo
            cr = f[int(y0):int(y0 + ch), int(x0):int(x0 + cw)]
            out[M:M + h, M:M + w, :3] = _cv2.resize(cr, (w, h), interpolation=_cv2.INTER_LINEAR)
            out[M:M + h, M:M + w, 3] = 255
        a = o[..., 3:4] / 255.0
        out[..., :3] = o[..., :3] * a + out[..., :3] * (1 - a)
        out[..., 3:4] = o[..., 3:4] + out[..., 3:4] * (1 - a)
        return _np.clip(out, 0, 255).astype(_np.uint8)
    return fn


def VENTANAS(n, tramos, protas, z=2.2, ancho=.22, x=.865, ys=(.355, .595)):
    """FORMA 3 · sobre los tramos del VOD a x1 (los FX `video` que devuelven SYNC/TRAMO/J), una ventana con zoom por protagonista.
    protas = [dict(nombre, sub, color, slot 0|1, keys=[(s_fuente, cx, cy)] medidos, de/a opcionales en s de la fuente)]."""
    ruta = fuente(n)
    w = int(round(1920 * ancho))
    h = int(round(w * 9 / 16))
    out = []
    for p in protas:
        keys = p["keys"]
        s0, s1 = p.get("de", keys[0][0]), p.get("a", keys[-1][0])
        piezas = []
        for f in tramos:
            if f.get("tipo") != "video" or abs(f.get("vel", 1.0) - 1) > .03 or f["ruta"] != ruta:
                continue
            u0, u1 = max(s0, f["desde"]), min(s1, f["desde"] + f["a"] - f["de"])
            if u1 - u0 >= .2:
                piezas.append((f["de"] + u0 - f["desde"], f["de"] + u1 - f["desde"], u0))
        for i, (de, a, desde) in enumerate(piezas):
            ant = i > 0 and abs(piezas[i - 1][1] - de) < .06
            sig = i + 1 < len(piezas) and abs(piezas[i + 1][0] - a) < .06
            out.append(dict(tipo="mg", fn=_ventana(ruta, desde, keys, p["nombre"], p.get("sub"), p["color"], z, w, h), de=round(de, 3),
                            a=round(a, 3), marcas=[], x=x, y=ys[p["slot"]], entra=0 if ant else .3, sale=0 if sig else .3,
                            nombre=("pizarra · " if ant else "") + f"ventana {p['nombre']}", ver=.8))     # «pizarra»: sin whoosh al seguir tras un corte
    return out


def fantasma(pts, en, dur=.8):
    """FORMA 6: ruta fantasma (blanca, discontinua): una POSIBILIDAD, nunca lo que pasó"""
    return flecha(pts, BL, en, None, guion=True, dur=dur)


def congelado_que_funde(n, de, t, dur=.7):
    """FORMA 1: el cuadro del VOD congelado encima del 3D, fundiéndose (el 3D arranca en la pose de la cámara del juego)"""
    j = J(n, de, de + dur, t, 0)
    j["sale"] = dur
    return j


_VELO = {}


def velo(de, a, k):
    """oscurece el VOD bajo un gráfico grande (el FX `oscurecer` va ANTES que los `video` en el motor: aquí es un `mg` negro)"""
    def fn(dt, dur, marcas):
        if k not in _VELO:
            _VELO[k] = _np.dstack([_np.zeros((1080, 1920, 3), _np.uint8), _np.full((1080, 1920), int(255 * k), _np.uint8)])
        return _VELO[k]
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=[], x=.5, y=.5, entra=.4, sale=.4, nombre="pizarra · velo", ver=.5)


def tramos_de(lista):
    return [f for f in lista if f.get("tipo") == "video"]


# ================================================================== J1 · cuartos GEN vs LYON, partida 3 (GEN azul) · formas 3, 4, 5
AZUL = {"GEN"}
n = "j1"
e0, e1 = ESC("j1")
k0, k1, k2, k3 = "j1_0", "j1_1", "j1_2", "j1_3"
Q1, Q2 = 59.6, 61.2                       # pausas medidas (rejilla2: previews/cuadros/r_j1_59.6.jpg y r_j1_61.2.jpg)
a1 = W(k0, "Mira")                        # pausa 1 cuando dice «Mira a Ruler»
tv0 = Q1 - (a1 - e0)                      # el VIVO arranca de modo que, a x1, llega a la pausa
FX += VIVO("j1", n, tv0, "Cuartos · miércoles 4 de noviembre · partida 3", "GEN", H(n, tv0))
FX += [J(n, T0(k0), a1, tv0 + T0(k0) - e0, 1.0),
       tar(W(k0, "infernal"), a1 + .2, "Dragón infernal · Gen.G", "25:46", A, logo="GEN", x=.76, y=.17, tam=40)]
b1 = W(k1, "Chovy")
FX += PZ(n, a1, b1, Q1, [
    an(.52, .665, "Ruler", "XAYAH", "GEN", W(k0, "Ruler"), "Xayah", lado="der"),
    an(.375, .495, "Inspired", "TRUNDLE", "LYON", W(k1, "Inspired"), "Trundle", lado="izq", r=40),
    intencion([(.39, .53), (.40, .585), (.405, .64)], R, W(k1, "entra") + .1, "SOLO", off=(70, 0)),
    texto("SOBRE CANYON", "PANTHEON", .27, .70, W(k1, "Canyon") - .3, color=A, tam=30, icono="Pantheon"),
])
c1 = b1 + (Q2 - Q1)
FX += [J(n, b1, c1, Q1, 1.0)]
d1 = W(k2, "Inspired") - .3               # Inspired cae en 61,5: justo cuando la voz lo nombra
MURO = [(.0, .37), (.15, .355), (.30, .35), (.45, .33), (.55, .31), (.70, .29), (.85, .27), (1.0, .255)]   # cresta, r_j1_61.2
FX += PZ(n, c1, d1, Q2, [
    muro_2d(MURO, c1 + .15),
    an(.12, .585, "Chovy", "TALIYAH", "GEN", c1 + .35, "Taliyah", lado="der", r=42),
    texto("EL RÍO, PARTIDO EN DOS", "EL MURO DE TALIYAH", .66, .17, W(k1, "parte") - .1, color=Y, tam=34),
    an(.60, .665, "Ruler", None, "GEN", W(k1, "rio"), "Xayah", lado="der", r=40),
])
_j1 = SYNC(n, [(d1, Q2), (d1 + .7, 61.9), (W(k2, "Isles") + .3, 67.5), (W(k2, "Berserker") + .3, 73.0), (W(k3, "empieza"), None)])
_bar = W(k3, "Baron")
_j1 += SYNC(n, [(W(k3, "empieza"), 73.0 + W(k3, "empieza") - W(k2, "Berserker") - .3), (_bar, 90.0), (e1, None)])
FX += _j1
FX += VENTANAS(n, tramos_de(_j1), [
    dict(nombre="Ruler", sub="Xayah · Gen.G", color=A, slot=0, a=73.9,
         keys=[(61.2, .61, .57), (61.9, .60, .58), (66.2, .55, .58), (67.3, .53, .55), (72.0, .53, .51), (73.0, .53, .42), (73.9, .53, .40)]),
    dict(nombre="Chovy", sub="Taliyah · el muro", color=A, slot=1, a=73.4,
         keys=[(61.2, .12, .55), (61.9, .12, .55), (66.2, .21, .41), (67.3, .21, .45), (72.0, .13, .53), (73.0, .16, .56), (73.4, .16, .56)]),
    dict(nombre="Kiin", sub="Aurora · no cae", color=A, slot=0, de=74.6,
         keys=[(74.6, .51, .65), (75.0, .51, .65), (76.5, .58, .46), (78.0, .43, .57), (80.0, .40, .56)]),
])
_mj1 = [d1 + .3, W(k2, "Isles") + .3, W(k2, "Berserker") + .3]
FX += [marcador(d1 - .1, _bar + 2.5, "GEN", "LYON", [("der", 1), ("der", 4), ("der", 3)], _mj1, titulo="25:51 · Ruler, 3 por 0"),
       oro(W(k0, "infernal") - .3, e1 - .4, "118", 1500, 1600, [1546, 1551, 1557, 1563, 1580],
           [W(k0, "infernal") + .5] + _mj1 + [_bar], "GEN", "LYON", notas=[(1565, "GEN +3,0K")], x=.17, y=.32, escala=.5, desfase=5),
       tar(W(k2, "Tres"), T0(k3), "3 asesinatos en 12 segundos", "Ruler · 25:51 a 26:03 · cero bajas de Gen.G", A, logo="GEN", x=.5,
           y=.17, tam=38),
       tar(_bar, W(k3, "tres") - .1, "Gen.G empieza el Barón", "26:20", A, logo="GEN", x=.76, y=.17, tam=40),
       vs(W(k3, "tres"), e1, "GEN", "LYON", "Gen.G gana 3 a 0", "Cuartos · miércoles 4 de noviembre", ganador=0, y=.44)]

# ================================================================== J3 · semifinal GEN vs IG, partida 3 (IG azul) · formas 1, 8, 2 (3D), 4, 5
AZUL = {"IG"}
n = "j3"
J3D_J3 = os.path.join(_D, "medios", "_fuente", "j3_3d.mp4")
c0, c1 = ESC("j3_ctx")
FX += [J(n, c0, c1, 0.0, 1.0), velo(c0, c1, .5),
       oro(c0 + .3, c1 - .1, "130", 0, 1790, [1140, 1300, 1560, 1755],
           [W("j3_ctx_0", "diecinueve"), W("j3_ctx_1", "aguanta"), W("j3_ctx_1", "veintiseis"), c1 - .8], "IG", "GEN",
           titulo="Partida 3 · diferencia de oro", x=.56, y=.52, escala=.95, desfase=4),
       tar(W("j3_ctx_0", "Minuto"), W("j3_ctx_0", "Rookie"), "Invictus 10 - 3", "Minuto 19 · semifinal, sábado 7 de noviembre", A,
           logo="IG", x=.5, y=.12, tam=44),
       peg(W("j3_ctx_0", "Rookie"), "Rookie", "Rookie", A, "IG", "Locke · 6 asesinatos al minuto 19", dur=T1("j3_ctx_0") - W("j3_ctx_0", "Rookie") + .3,
           x=.12, y=.5, tam=330),
       tar(W("j3_ctx_1", "En"), c1, "Gen.G, 6 - 13", "Minuto 26 · todavía abajo", R, logo="GEN", x=.5, y=.12, tam=44)]
e0, e1 = ESC("j3")
v0 = W("j3_0", "Vamos")
G0_3D = 1815.0                            # el 3D arranca en 30:15, a x1 hasta la pausa de 30:23 (j3_3d.CONGELA)
tv0 = (G0_3D - K[n]) - (v0 - e0)
FX += VIVO("j3", n, tv0, "Semifinal · sábado 7 de noviembre · partida 3", "GEN", H(n, tv0))
FX += [J(n, T0("j3_0"), v0, tv0 + T0("j3_0") - e0, 1.0),
       tar(W("j3_0", "cuarto"), v0, "Invictus va por el alma", "Tiene 3 dragones · 30:16", A, logo="IG", x=.76, y=.17, tam=40)]
A3 = T0("j3_2") + 1.25                    # «Ahora vuelve al video»: el 3D regresa a la pose del juego y el VOD funde encima
TIEMPOS_3D["j3"] = dict(de=round(v0, 3), a=round(A3, 3),
                        reloj=[[round(v0, 3), G0_3D], [round(v0 + 8.21, 3), 1823.0], [round(A3 - 1.4, 3), 1823.0], [round(A3, 3), 1824.4]])
FX += [V3(v0, A3, J3D_J3, v0), congelado_que_funde(n, v0, G0_3D - K[n])]
m = W("j3_2", "Meiko")
_r = REBX(n, A3 - .4, 1824.0 - K[n], m, 62.0)
_r[0]["entra"] = .4
FX += _r
_s = W("j3_3", "TheShy")
p3 = _s + .6
FX += SYNC(n, [(m, 62.0), (W("j3_2", "JiaQi"), 67.0), (W("j3_2", "Wei"), 75.0), (_s, 108.0), (p3, 108.6)])
q3 = W("j3_4", "Baron") - (110.7 - 108.6)                # el Barón de las 31:11 cae cuando la voz lo dice
FX += PZ(n, p3, q3, 108.6, [
    an(.34, .565, "Ruler", "YUNARA · 4 ASESINATOS", "GEN", W("j3_3", "Cuatro"), "Yunara", lado="der"),
    texto("EL BARÓN", "3 089 DE VIDA · 31:08", .66, .30, p3 + .5, color=Y, tam=32),
])
FX += [J(n, q3, e1, 108.6, 1.0)]
_mj3 = [m, W("j3_2", "JiaQi"), W("j3_2", "Wei"), _s]
FX += [marcador(A3 - .2, W("j3_4", "Ahora"), "IG", "GEN", [("izq", 4), ("izq", 3), ("izq", 1), ("izq", 0)], _mj3, titulo="30:22 · la remontada"),
       oro(A3 - .2, e1 - .3, "130", 1790, 1890, [1821, 1822, 1827, 1835, 1868, 1871, 1877], [A3 + .3] + _mj3 + [W("j3_4", "Baron"), W("j3_4", "cuatrocientos")],
           "IG", "GEN", notas=[(1877, "GEN +1,4K")], x=.17, y=.32, escala=.5, desfase=4),
       tar(W("j3_3", "Cuatro"), W("j3_4", "Baron"), "4 asesinatos de Ruler", "30:22 a 31:08 · 46 segundos", R, logo="GEN", x=.76, y=.17, tam=40),
       tar(W("j3_4", "Baron"), W("j3_4", "Ahora"), "Barón para Gen.G", "31:11", R, logo="GEN", x=.76, y=.17, tam=40),
       tar(W("j3_4", "Ahora"), e1, "Gen.G +1,4K", "31:13 · por primera vez arriba en la partida", R, logo="GEN", x=.76, y=.17, tam=40)]
f0, f1 = ESC("j3_fin")
t_f = 108.6 + (e1 - q3)
FX += [J(n, f0, f1, t_f, 1.0), velo(f0, f1, .45)]
FX += repeticion(f0 + (137.7 - t_f), f0 + (137.7 - t_f) + 3.5, "Repetición de la transmisión")
FX += [oro(f0 + .2, W("j3_fin_1", "Tres") - .1, "130", 0, 2408, [1877, 2004, 2404], [f0 + 1.4, W("j3_fin_0", "pelea"), W("j3_fin_0", "base")],
           "IG", "GEN", notas=[(2004, "IG gana otra pelea"), (2404, "Nexo")], titulo="Partida 3 · la diferencia de oro entera",
           x=.5, y=.5, escala=.95, desfase=4),
       vs(W("j3_fin_1", "Tres"), f1, "IG", "GEN", "Gen.G gana 3 a 0", "Semifinal · sábado 7 de noviembre", ganador=1, y=.4),
       tar(W("j3_fin_1", "final"), f1, "Primera final desde 2017", "Entonces se llamaba Samsung Galaxy", R, logo="GEN", x=.5, y=.84, tam=46)]

# ================================================================== J2 · cuartos BLG vs DK, partida 1 (BLG azul) · formas 2, 6, 4, 5
AZUL = {"BLG"}
n = "j2"
e0, e1 = ESC("j2")
TV2, PJ2 = 40.6, 55.0                       # VIVO desde la toma 40,6 → 71,4 (sin cortes) · pausa medida en r_j2_55.jpg
a = e0 + (PJ2 - TV2)
b = W("j2_1", "adelante") + 1.8             # la pausa deja leer la FORMA 6 (Lucid cae ~1,6 s después de nombrarlo)
FX += VIVO("j2", n, TV2, "Cuartos · jueves 5 de noviembre · partida 1", "BLG", H(n, TV2))
FX += [J(n, T0("j2_0"), a, TV2 + T0("j2_0") - e0, 1.0),
       tar(W("j2_0", "Heraldo"), W("j2_0", "arriba") - .1, "Heraldo para Bilibili", "16:00", A, logo="BLG", x=.24, y=.17, tam=40)]
FX += PZ(n, a, b, PJ2, [
    an(.18, .25, "Xun", "NAAFIRI", "BLG", W("j2_0", "Xun"), "Naafiri", lado="der"),
    an(.27, .46, "Lucid", "DEMASIADO ADELANTE", "DK", W("j2_1", "Lucid"), "Qiyana", lado="izq", r=42),
    fantasma([(.29, .49), (.40, .575), (.52, .625), (.61, .645)], W("j2_1", "adelante") + .05),
    an(.64, .65, "Career", "RELL", "DK", W("j2_1", "adelante") + .3, "Rell", lado="der", r=38),
    texto("LO QUE PODÍA HACER", "QUEDARSE ATRÁS, CON CAREER · POSIBILIDAD, NO LO QUE PASÓ", .45, .70, W("j2_1", "adelante") + .4, color=BL, tam=30),
    intencion([(.49, .29), (.40, .35), (.31, .42)], A, b - .9, "BIN", off=(40, -40)),
])
mj2 = b + 14.0                            # 55 → 69 a x1: Lucid, Bin, Career, DOUBLE y la persecución
FX += [J(n, b, mj2, PJ2, 1.0)]
FX += MESA2("j2b", mj2, T0("j2_4"), H(n, 69.0))
k_sm = T0("j2_4") + 1.0
FX += [J(n, T0("j2_4"), k_sm, 69.0, 1.0), J(n, k_sm, e1, 77.15, 1.0)]       # corte a 77,2: «BLG Xun is on a killing spree!»
_mj2 = [b + 4.0, b + 7.0, b + 8.5, k_sm + .15]
FX += [marcador(b + 3.4, e1 - .3, "BLG", "DK", [("der", 1), ("izq", 0), ("der", 4), ("der", 2)], _mj2, titulo="16:09 · la pelea del Heraldo"),
       oro(W("j2_0", "arriba") - .3, e1 - .4, "098", 900, 1000, [964, 969, 973, 979, 988, 995],
           [W("j2_0", "oro"), b + 4.0, b + 8.5, W("j2_3", "lado"), k_sm + .15, e1 - .8], "BLG", "DK", notas=[(975, "Cambia de lado")],
           x=.83, y=.25, escala=.5, desfase=5),
       tar(W("j2_0", "arriba"), a + .6, "Dplus KIA +0,3K", "16:04", R, logo="DK", x=.24, y=.17, tam=40),
       tar(k_sm + .15, e1, "Bilibili 3 - 0 Dplus KIA", "Cuartos · jueves 5 de noviembre", A, logo="BLG", x=.5, y=.17, tam=40)]

# ================================================================== J4 · semifinal T1 vs BLG, partida 2 (T1 azul) · formas 3, 6, 4, 5
AZUL = {"T1"}
n = "j4"
e0, e1 = ESC("j4")
TV4 = 16.0
FX += VIVO("j4", n, TV4, "Semifinal · domingo 8 de noviembre · partida 2", "T1", H(n, TV4))
p = W("j4_0", "Ancestral") + .5                   # x1 hasta 28,6 (la toma 10,5 → 28,7 corta en 28,7)
p = min(p, e0 + (28.6 - TV4))
FX += [J(n, T0("j4_0"), p, TV4 + T0("j4_0") - e0, 1.0),
       tar(W("j4_0", "Minuto"), p, "Dragón Ancestral · T1", "30:28", A, logo="T1", x=.76, y=.17, tam=40)]
q = T0("j4_2") - 1.4                              # pausa en 94 (31:36, cae la 1.ª torre del nexo) y 1 s a x1 antes del corte
FX += PZ(n, p, q, 94.0, [
    zona(.48, .385, .085, .07, A, p + .2),
    fantasma([(.44, .43), (.33, .51), (.20, .60)], W("j4_1", "inhibidor") - .2),
    texto("LO QUE PODÍA HACER", "SALIR Y VOLVER · POSIBILIDAD, NO LO QUE PASÓ", .23, .70, W("j4_1", "inhibidor"), color=BL, tam=28),
    intencion([(.54, .40), (.64, .385), (.74, .37)], A, W("j4_1", "nexo") - .5, None),
    texto("LO QUE HIZO: IR POR EL NEXO", "«QUIEREN ACABAR CON ESTA PARTIDA JUSTO AHORA» · NARRADORES", .68, .56, W("j4_1", "nexo") - .3, color=A, tam=28),
])
FX += [tar(W("j4_1", "torres"), q, "Torres del centro", "31:13 y 31:24", A, logo="T1", x=.2, y=.25, tam=34),
       tar(W("j4_1", "inhibidor"), q, "2.º inhibidor", "31:27", A, logo="T1", x=.2, y=.35, tam=34),
       tar(W("j4_1", "nexo"), q, "Torres del nexo", "31:34 y 31:53", A, logo="T1", x=.2, y=.45, tam=34)]
r4 = q + 1.0
_j4 = [J(n, q, r4, 94.0, 1.0), J(n, r4, e1, 111.5, 1.0)]       # corte a 31:53,5: los 13 segundos de la pelea, a x1
FX += _j4
FX += VENTANAS(n, _j4, [
    dict(nombre="Faker", sub="Syndra · T1", color=A, slot=0,
         keys=[(111.5, .34, .46), (114.0, .63, .47), (116.5, .60, .60), (119.0, .68, .50), (121.5, .26, .45), (124.5, .37, .43), (126.5, .37, .43)]),
    dict(nombre="Viper", sub="Kai'Sa · Bilibili", color=R, slot=1, a=125.6,
         keys=[(111.5, .56, .33), (114.0, .67, .17), (116.5, .62, .42), (119.0, .70, .32), (121.5, .45, .46), (124.5, .42, .46), (125.6, .42, .46)]),
])
_mj4 = [r4 + (t - 111.5) for t in (112.0, 116.0, 118.0, 121.0, 125.0)]
FX += [marcador(r4 - .2, e1 - .2, "T1", "BLG", [("der", 2), ("der", 4), ("der", 1), ("der", 0), ("der", 3)], _mj4, titulo="31:54 · 13 segundos"),
       oro(r4 - .3, e1 - .3, "123", 1830, 1935, [1913, 1914, 1918, 1920, 1923, 1927], [r4] + _mj4, "T1", "BLG",
           notas=[(1925, "T1 +9,1K")], x=.17, y=.32, escala=.5, desfase=5),
       tar(W("j4_3", "Veintidos"), W("j4_3", "empata"), "Así acabó: 22 - 10", "T1 +9,8K a las 32:07 · ACE 32:11", A, logo="T1", x=.5, y=.17, tam=38),
       tar(W("j4_3", "empata"), e1, "Serie 1 - 1", "T1 gana la partida 2 · Faker 4/0", A, logo="T1", x=.5, y=.17, tam=38)]

# ================================================================== J5 · semifinal BLG vs T1, partida 3 (BLG azul) · formas 2, 3, 4, 5
AZUL = {"BLG"}
n = "j5"
e0, e1 = ESC("j5")
TV5 = 8.6
FX += VIVO("j5", n, TV5, "Semifinal · domingo 8 de noviembre · partida 3", "BLG", H(n, TV5))
u1 = T0("j5_1")
FX += [J(n, T0("j5_0"), u1, TV5 + T0("j5_0") - e0, 1.0)]
m0 = u1 + 2.2                              # corte a 43,8 (toma 37,1 → 48,8) y a x1 hasta 46: la mesa (los 10 medidos)
m1 = T0("j5_2") - .8
FX += [J(n, u1, m0, 43.8, 1.0)]
FX += MESA2("j5a", m0, m1, H(n, 46.0))
w_al, w_vi = W("j5_2", "infernal") + .1, W("j5_3", "torre") + .1
_j5 = SYNC(n, [(m1, 46.0), (W("j5_2", "Oner") + .1, 59.0), (W("j5_2", "Bin") + .2, 62.0), (W("j5_2", "Doran") + .2, 65.0), (w_al, 70.3),
               (W("j5_3", "Knight") + .1, 76.0), (w_vi, 79.0), (w_vi + 5.3, 84.3), (e1, None)])
FX += _j5
FX += VENTANAS(n, _j5, [
    dict(nombre="Viper", sub="Ezreal · Bilibili", color=A, slot=0, de=79.0, a=85.0,
         keys=[(79.0, .67, .34), (79.5, .67, .34), (81.0, .52, .44), (82.5, .40, .42), (84.5, .52, .35), (85.0, .52, .35)]),
    dict(nombre="Xun", sub="Pantheon · Bilibili", color=A, slot=1, de=79.0, a=85.0,
         keys=[(79.0, .47, .23), (79.5, .47, .23), (81.0, .40, .46), (82.5, .36, .37), (84.5, .38, .40), (85.0, .38, .40)]),
])
_mj5 = [W("j5_2", "Oner") + .1, W("j5_2", "Bin") + .2, W("j5_2", "Doran") + .2, W("j5_3", "Knight") + .1, w_vi + 3.0, w_vi + 3.5]
FX += [oro(T0("j5_0") + .2, u1, "124", 1200, 1960, [1351, 1952], [W("j5_0", "ocho"), W("j5_0", "cuatro")], "BLG", "T1",
           notas=[(1351, "8 - 8")], titulo="Partida 3 · diferencia de oro", x=.24, y=.3, escala=.62, desfase=5),
       tar(W("j5_0", "cuatro"), u1, "Bilibili +3,9K", "31:46 · el alma del dragón en juego", A, logo="BLG", x=.76, y=.17, tam=40),
       marcador(m1 - .2, e1 - .3, "BLG", "T1", [("der", 1), ("izq", 0), ("der", 0), ("izq", 2), ("der", 3), ("der", 4)], _mj5,
                titulo="32:43 · el alma infernal"),
       oro(m1 - .2, e1 - .4, "124", 1930, 2000, [1953, 1963, 1966, 1969, 1974, 1980, 1986], [m1 + .2] + _mj5[:4] + [w_vi, w_vi + 5.3], "BLG", "T1",
           x=.17, y=.32, escala=.5, desfase=5),
       tar(w_al, w_vi, "Alma infernal · Bilibili", "32:54 · su 4.º dragón", A, logo="BLG", x=.76, y=.17, tam=40),
       tar(W("j5_3", "resucitado"), w_vi + 5.3, "Viper resucitó a las 32:35", "Y vuelve a la pelea", A, icono="Ezreal", x=.5, y=.17, tam=38),
       tar(W("j5_4", "Cuatro"), e1, "4 por 2 · alma infernal", "Bilibili se pone 2 a 1", A, logo="BLG", dato="2-1", x=.5, y=.17, tam=40)]

# ================================================================== J6 · semifinal T1 vs BLG, partida 4 (T1 azul) · formas 1, 6, 8 (3D), 4, 5
AZUL = {"T1"}
c0, c1 = ESC("j6_ctx")
_bx = W("j6_ctx_1", "minuto", 1) - .4          # «un minuto después» (ojo: «un» también casa con «una»)
FX += [J("j6_baron", c0, _bx, 0.0, 1.0), J("j6_baron", _bx, c1, 41.0 - (W("j6_ctx_1", "Baron") - _bx), 1.0),
       velo(c0, T0("j6_ctx_1"), .5),
       oro(c0 + .3, T0("j6_ctx_1") - .1, "125", 0, 1700, [1020, 1677], [W("j6_ctx_0", "diecisiete"), W("j6_ctx_0", "veintiocho")], "T1", "BLG",
           notas=[(1677, "BLG +5,7K")], titulo="Partida 4 · diferencia de oro", x=.56, y=.52, escala=.95, desfase=5),
       tar(W("j6_ctx_0", "diez"), T0("j6_ctx_1"), "Bilibili 10 - 3", "Minuto 17 · domingo 8 de noviembre", R, logo="BLG", x=.5, y=.12, tam=44),
       tar(T0("j6_ctx_1"), _bx, "Repetición · la pelea del minuto 28", "T1 gana, con 2 asesinatos de Faker", A, logo="T1", x=.5, y=.84, tam=40),
       cam(W("j6_ctx_1", "Faker"), "Faker", "Faker · Akali", dur=_bx - W("j6_ctx_1", "Faker") + .2, x=.09, y=.3),
       tar(W("j6_ctx_1", "Baron"), c1, "Barón para T1", "29:20", A, logo="T1", x=.76, y=.17, tam=40)]
n = "j6"
J3D_J6 = os.path.join(_D, "medios", "_fuente", "j6_3d.mp4")
e0, e1 = ESC("j6")
v0 = W("j6_0", "Vamos")
G0_6 = 1926.0                              # 32:06: el 3D arranca sobre la torre central roja (j6_3d.JUEGO)
tv0 = (G0_6 - K[n]) - (v0 - e0)
FX += VIVO("j6", n, tv0, "Semifinal · domingo 8 de noviembre · partida 4", "T1", H(n, tv0))
FX += [J(n, T0("j6_0"), v0, tv0 + T0("j6_0") - e0, 1.0)]
A6 = T0("j6_3") + .4
TIEMPOS_3D["j6"] = dict(de=round(v0, 3), a=round(A6, 3), reloj=[
    [round(v0, 3), G0_6], [round(W("j6_1", "Cae"), 3), 1934.0], [round(W("j6_2", "Oner") + .3, 3), 1934.6],
    [round(W("j6_2", "Viper", fin=True) + .5, 3), 1935.0], [round(W("j6_2", "Knight"), 3), 1936.6], [round(A6, 3), 1937.2]])
FX += [V3(v0, A6, J3D_J6, v0), congelado_que_funde(n, v0, G0_6 - K[n])]
sv = W("j6_3", "salva")
_r = REBX(n, T0("j6_3"), 1937.2 - K[n], sv, 76.0)          # el VOD vuelve en el cuadro del final del 3D y rebobina al Ángel
_r[0]["entra"] = .4
FX += _r
p6 = sv + 1.0
q6 = W("j6_3", "cae") - (78.06 - 77.0)
FX += SYNC(n, [(sv, 76.0), (p6, 77.0)])
FX += PZ(n, p6, q6, 77.0, [
    texto("VIPER SE SALVA", "ÁNGEL DE LA GUARDA · 32:16", .70, .56, p6 + .1, color=R, tam=30, icono="Ashe"),
    an(.37, .43, "Bin", "RENEKTON · POR ARRIBA", "BLG", W("j6_3", "Bin"), "Renekton", lado="izq"),
    an(.465, .66, "Xun", "SKARNER · POR ABAJO", "BLG", W("j6_3", "Xun"), "Skarner", lado="der"),
    an(.56, .39, "Faker", "SOLO, AL NORTE", "T1", p6 + .4, "Akali", lado="der", r=38),
])
FX += SYNC(n, [(q6, 77.0), (W("j6_3", "cae"), 78.06), (W("j6_3", "cae", 1), 83.0), (W("j6_3", "Faker"), 87.0), (e1, None)])
_mj6 = [W("j6_3", "cae"), W("j6_3", "cae", 1), W("j6_3", "Faker")]
FX += [marcador(T0("j6_3") + .6, e1 - .3, "T1", "BLG", [("izq", 1), ("izq", 0), ("izq", 2)], _mj6, titulo="32:18 · 3 por 0"),
       oro(T0("j6_3") + .6, e1 - .3, "125", 1900, 1975, [1936, 1938, 1943, 1947, 1955], [T0("j6_3") + 1.0] + _mj6 + [W("j6_4", "ventaja")],
           "T1", "BLG", x=.83, y=.25, escala=.5, desfase=5),
       tar(W("j6_4", "Tres"), W("j6_4", "ventaja"), "3 por 0", "Sin una sola baja de Bilibili", R, logo="BLG", dato="3-0", x=.5, y=.17, tam=40),
       tar(W("j6_4", "ventaja"), e1, "Bilibili +2,5K", "32:27 · venía de +0,4K", R, logo="BLG", x=.5, y=.17, tam=40)]
n = "j6_fin"
e0, e1 = ESC("j6_fin")
nx = W("j6_fin_0", "nexo")
ts = 16.0 - (nx - e0)                      # x1: el nexo estalla (≈16,0) cuando la voz lo dice
L0 = e0 + (16.2 - ts)
L1 = L0 + (16.2 - 10.95) / .4
FX += [J(n, e0, L0, ts, 1.0),
       J(n, L0, L1, 10.95, .4, zoom=(1.75, .5, .84), zoom0=(1.0, .5, .5), zoom_en=8.2, zoom_dur=1.4),       # las cámaras de BLG
       J(n, L1, e1, 16.2, 1.0)]           # y a x1 la celebración: post de 14 s con el narrador («Se rompió la dinastía…», t 21)
FX += repeticion(L0, L0 + 3.5, "Cámara lenta · el nexo y las cámaras de Bilibili")
FX += [vs(W("j6_fin_1", "Tres"), W("j6_fin_1", "despide") - .1, "T1", "BLG", "Bilibili gana 3 a 1", "Semifinal · domingo 8 de noviembre",
          ganador=1, y=.42),
       elim(W("j6_fin_1", "despide"), W("j6_fin_1", "Bilibili") - .1, "T1", "T1", "Fuera del Mundial en semifinales", [W("j6_fin_1", "Mundial")]),
       tar(W("j6_fin_1", "Bilibili"), T0("j6_fin_2"), "Bilibili, otra vez en la final", "Dos años después de perder la anterior", R,
           logo="BLG", x=.5, y=.17, tam=42),
       tar(W("j6_fin_2", "reacciones"), L1 - .1, "La reacción de Bilibili", "Sus cámaras, al caer el nexo · 37:41", R, logo="BLG", x=.5, y=.17, tam=40)]
