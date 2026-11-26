# -*- coding: utf-8 -*-
"""Montaje de las JUGADAS de tl_josedeodo: gancho, blg, al1, cfo, los2, los3 (el resto, fx_escenas.py). Helpers copiados de t1_blg_caida. Lo ejecuta efectos.py con exec.
Formas (las de lol_final_previa, se SUMAN): 4 (marcador NFL) y 5 (oro en vivo del feed) en cada jugada; mesa 3D con cámara normal en g3
(j5a, los 10 medidos); Grieta 3D de la G4 con cámara NUEVA (j6_3d.py: órbita lateral, no la de la previa); pausas con chip del reloj;
rebobinados y repeticiones rotuladas. Anillos SOLO en pies medidos (j6 t 77 de datos_j6.md). Datos: investigacion/datos_g1.md, datos_g3a.md,
datos_g4a.md, datos_j4..j6.md, datos_relleno.md § j4b. Nada pasa de x1 (SYNC/SYNC2 cortan o pausan)."""
import cv2 as _cv2
import numpy as _np
from PIL import Image as _Img, ImageDraw as _Draw, ImageFilter as _Filt

K.update({"blg_j1": 643.7, "blg_j2": 1038.6, "al_j1": 1696.0, "al_j2": 1009.0, "cfo_j1": 2000.0, "lotl_j1": 2063.0, "lotl_j2": 2364.5,
          "lotl_zest": 2767.0})
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




# ───────────────────────── 2.ª versión (25-nov-2026): jugadas SIN cortes (cadenas de investigacion/huecos.py; voz espaciada) + PLAN 3D +
# ÓRBITAS 360° (mesas_3d.py, cam="orbita") con flechas en arco y rutas medidas. El usuario: «combinando todas, sobre todo cámara 3D rotando y
# flechas parabólicas, rutas». Una pausa = dos anclas al mismo segundo de la fuente (SYNC2 congela y la mesa va encima).
import sys as _sys

_sys.path.insert(0, os.path.join(_D, "investigacion"))
import huecos as _H  # noqa: E402

CAD = _H.CADENAS


def anc(a):
    tipo, k, pal, i, _ = a
    if tipo == "esc":
        return ESC(k)[0]
    if tipo == "ini":
        return T0(k)
    return W(k, pal, i)


def CADENA(nom, fin=None, extra=()):
    """los tramos del VOD de una cadena: x1; si la voz es más larga, PAUSA en el cuadro (chip); nunca salta (SYNC2)"""
    pares = []
    for a in CAD[nom]:
        s = a[4]
        if isinstance(s, tuple):
            s = s[2] + anc(a) - ESC(s[1])[0]
        pares.append((anc(a), s))
    pares += list(extra)
    if fin is not None:
        pares.append((fin, None))
    return SYNC2(n, pares)


def pausa_de(t_a, s_a, t_b, s_b):
    """lo que dura la pausa que SYNC2 pone al empezar el intervalo (si la voz es más larga que la fuente)"""
    return max(0.0, (t_b - t_a) - (s_b - s_a))


# ================================================================== BLG · TLAW azul (datos_blg.md; blg_j1 HUD = t + 643,7; blg_j2 HUD = t + 1038,6)
AZUL = {"TLAW"}
g = "blg_"
e0, e1 = ESC("blg")
k0, k1, k2 = (g + str(i) for i in range(3))
n = "blg_j1"
tv = 15.0 - (T0(k0) - e0)                   # en vivo de 10:52 a 10:58 (Liquid empieza el dragón) y ahí el PLAN 3D
FX += VIVO("blg", n, tv, "Partida 2 · Liquid vs Bilibili", "BLG", H(n, tv))
xu = W(k0, "Xun")
FX += [J(n, T0(k0), xu, 15.0, 0)] + MESA2("blg_plan", T0(k0), xu, H(n, 15.0))
FX += CADENA("blg_a")                        # 10:58 → 11:06 seguido (la voz espera en «… y con el castigo»)
rb = W(k0, "roba")
yy = W(k1, "Y")
FX += [J(n, rb, yy, 23.0, 0)] + MESA2("blg_orb", rb, yy, H(n, 23.0))        # ÓRBITA en el robo
FX += [tar(W(k0, "Jarvan"), W(k0, "Minuto"), "Josedeodo · Jarvan IV", "Contra Xun · Lee Sin", A, icono="JarvanIV", x=.27, y=.27, tam=40),
       cam(xu, "Xun", "Xun · Lee Sin", dur=rb - xu + .2, x=.08, y=.3, tam=190),
       tar(rb, yy, "¡Dragón robado! · 11:06", "Xun · con el castigo", R, logo="BLG", x=.5, y=.12, tam=40),
       dict(tipo="destello", en=rb, fuerza=.45)]
FX += [*LENTA(n, yy, W(k1, "minuto"), 54.0, vel=.6, sub="Repetición · «era 50-50», narradores"),
       tar(W(k1, "larvas"), W(k1, "minuto"), "Larvas y Heraldo", "También de Xun", R, logo="BLG", x=.5, y=.84, tam=46)]
n = "blg_j2"
FX += CADENA("blg_b")
FX += [tar(W(k1, "minuto"), W(k1, "mata"), "Minuto 17", "Josedeodo salta sobre Viper", A, icono="JarvanIV", x=.27, y=.27, tam=40),
       tar(W(k1, "mata"), T0(k2) + .2, "17:54 · Xun mata a Josedeodo", "ON lo inmoviliza · BLG +2,4K", R, logo="BLG", x=.27, y=.27, tam=40),
       dict(tipo="destello", en=W(k1, "mata"), fuerza=.35)]
FX += [*FZ(n, T0(k2), e1, 38.0, 1.12), velo(T0(k2), e1, .5),
       mg(L.duelo((JUG("Josedeodo"), "Josedeodo", EQ("TLAW"), A, "Jarvan IV"), (JUG("Xun"), "Xun", EQ("BLG"), R, "Lee Sin"),
                  "Partida 2 · los junglas", [("Asesinatos", "0", "2", .05, 1.0, 1), ("Muertes", "4", "1", 1.0, .25, 1),
                                              ("Guardianes", "10", "23", 10 / 23, 1.0, 1)]),
          T0(k2) + .1, e1 + .2, [W(k2, "dos"), W(k2, "diecisiete"), W(k2, "cuatro")], y=.5, nombre="duelo Josedeodo-Xun"),
       tar(W(k2, "diecisiete"), e1 + .2, "Bilibili 17 - 2 Liquid", "Partida 2 · 2.ª derrota", R, logo="BLG", dato="17-2", x=.5, y=.9, tam=40)]

# ================================================================== AL G1 · TLAW rojo, 1.ª selección (datos_al.md; al_j1 HUD = t + 1696)
AZUL = {"AL"}
g = "al1_"
e0, e1 = ESC("al1")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
n = "al_j1"
FX += VIVO("al1", n, 0.0, "Partida 1 · Anyone's Legend vs Liquid", "TLAW", H(n, 0.0))
FX += [J(n, T0(k0), T0(k1), T0(k0) - e0, 1.0),
       peg(W(k0, "Lee"), CARGA("LeeSin"), "Lee Sin", R, "TLAW", "1.ª selección de Liquid · Josedeodo", dur=T0(k1) - W(k0, "Lee") + .1,
           x=.2, y=.5, tam=380)]
FX += CADENA("al1_a")
fl = W(k1, "flanco")
FX += PZ(n, fl, W(k1, "atrapa"), 23.5, [                                       # PASO A PASO: la pausa con telestrador
    an(.21, .24, "Morgan y Josedeodo", "POR EL FLANCO", "TLAW", fl + .1, "Camille", lado="der"),
    flecha([(.21, .24), (.30, .36), (.38, .47)], R, fl + .5, "ENTRAN POR DETRÁS", off=(120, -10), guion=True, dur=.7),
    texto("LOS 5 DE ANYONE'S LEGEND", "FRENTE A YEON, COREJJ Y QUID", .50, .88, fl + .3, color=A, tam=28),
])
FX += CADENA("al1_b")
jp = W(k1, "Josedeodo", 1)
ye = W(k2, "Yeon")
orb = pausa_de(jp, 26.4, ye, 34.4)
FX += MESA2("al1_orb", jp, jp + orb, H(n, 26.4))                              # ÓRBITA: la patada sobre Hope
FX += SYNC2(n, [(jp, 26.4)] + [(anc(a), a[4]) for a in CAD["al1_c"]])
_ma = [W(k2, "Yeon"), W(k2, "triple") - .4, W(k2, "triple"), W(k2, "Yeon", 1), W(k2, "CoreJJ"), W(k2, "pero"), W(k2, "Breathe")]
FX += CADENA("al1_d", fin=e1)
FX += [marcador(jp + orb + .2, T0(k3) - .2, "TLAW", "AL", [("der", 3), ("der", 1), ("der", 4), ("izq", 3), ("izq", 4), ("der", 2), ("der", 0)],
                _ma, titulo="28:44 · el ACE"),
       tar(W(k2, "triple"), W(k2, "Anyone"), "Triple de Yeon", "Hope, Tarzan y Kael", R, icono="Lucian", x=.27, y=.27, tam=40),
       tar(W(k2, "Breathe"), T0(k3) + .2, "¡ACE! · 29:02", "Josedeodo remata a Breathe", R, logo="TLAW", dato="5-2", x=.5, y=.17, tam=46),
       dict(tipo="destello", en=W(k2, "Breathe"), fuerza=.45),
       tar(W(k3, "alma"), W(k3, "Josedeodo"), "Alma de nube · Liquid", "29:28", R, logo="TLAW", x=.76, y=.17, tam=40),
       mg(L.premio("Con Lee Sin · 1.ª selección", JUG("Josedeodo"), "Josedeodo", EQ("TLAW"), ["3 asesinatos · 0 muertes · 8 asistencias",
                                                                                               "Liquid gana 16 a 5"], color="rojo",
                   sub="Partida 1 contra Anyone's Legend"),
          W(k3, "Josedeodo"), e1 + .2, [W(k3, "tres"), W(k3, "dieciseis")], y=.5, nombre="premio al1")]

# ================================================================== CFO · TLAW azul, Lee Sin con 1.ª selección (datos_cfo.md; cfo_j1 HUD = t + 2000)
# Josedeodo muere a las 34:24 (t 64,3; «CFO Rest has slain TLAW Josedeodo»), no 34:29: se ve entera, a x1, y la órbita sale de ese cuadro
AZUL = {"TLAW"}
g = "cfo_"
e0, e1 = ESC("cfo")
k0, k1, k2 = (g + str(i) for i in range(3))
n = "cfo_j1"
tv = 56.0 - (T0(k1) - e0)                    # en vivo hasta 34:16 y ahí el PLAN 3D
FX += VIVO("cfo", n, tv, "Partida 1 · Liquid vs CTBC Flying Oyster", "CFO", H(n, tv))
FX += [J(n, T0(k0), T0(k1), tv + T0(k0) - e0, 1.0),
       peg(W(k0, "Lee"), CARGA("LeeSin"), "Lee Sin", A, "TLAW", "1.ª selección de Liquid · y perdió", dur=T0(k1) - W(k0, "Lee") + .1,
           x=.2, y=.5, tam=380)]
FX += MESA2("cfo_plan", T0(k1), T0(k2), H(n, 56.0))                           # PLAN: Josedeodo espera; Kino lo va a sacar
rm = W(k2, "remata")
el = W(k2, "El")
orb = pausa_de(rm, 64.3, el, 79.4)
FX += CADENA("cfo_a", extra=[(el, 79.4)])
FX += MESA2("cfo_orb", rm, rm + orb, H(n, 64.3))                              # ÓRBITA en la muerte (34:24)
FX += SYNC2(n, [(el, 79.4)] + [(anc(a), a[4]) for a in CAD["cfo_b"]] + [(e1, None)])
_mc = [W(k2, "Kino") + .8, rm, rm + .4]
FX += [tar(W(k1, "Minuto"), W(k1, "Pero"), "Minuto 34 · Liquid 10 - 5", "Pero CTBC: 4 dragones y el alma de montaña", A, logo="TLAW",
           x=.27, y=.12, tam=36),
       cam(W(k2, "Josedeodo"), "Josedeodo", "Josedeodo · espera el robo", dur=rm - W(k2, "Josedeodo") + .3, x=.08, y=.3, tam=190),
       marcador(W(k2, "Kino") - .2, rm + orb - .1, "TLAW", "CFO", [("izq", 1), ("der", 1), ("izq", 2)], _mc, titulo="34:24 · el ancestral"),
       dict(tipo="destello", en=rm, fuerza=.4),
       tar(rm + orb, el, "Josedeodo, fuera · 34:24", "Y CTBC sigue con el ancestral", R, logo="CFO", x=.5, y=.84, tam=40),
       tar(el, W(k2, "Baron"), "Ancestral para CTBC", "34:39", R, logo="CFO", x=.5, y=.17, tam=44),
       tar(W(k2, "Baron"), W(k2, "Liquid"), "Y el Barón", "35:16", R, logo="CFO", x=.5, y=.17, tam=44),
       tar(W(k2, "Liquid"), e1 + .2, "CTBC 12 - 11 Liquid", "1.ª derrota · con el Lee Sin", R, logo="CFO", dato="12-11", x=.5, y=.17, tam=44)]

# ================================================================== LOS G3 · TLAW azul (datos_lotl.md J1, lotl_j1 HUD = t + 2063): la pelea del muro
# la pausa y la mesa (bullet) salen de la REPETICIÓN (t 96, otra toma); luego vuelve al directo en el mismo segundo (34:41)
AZUL = {"TLAW"}
g = "los3_"
e0, e1 = ESC("los3")
k0, k1, k2, k3, k4, k5 = (g + str(i) for i in range(6))
n = "lotl_j1"
FX += VIVO("los3", n, 0.0, "Partida 3 · la de la eliminación", "LOS", H(n, 0.0))
FX += CADENA("los3_a")
FX += [tar(W(k0, "recortado"), T0(k1), "De -7 000 a -3 300", "Y el Barón encima · 34:2x", A, logo="TLAW", x=.27, y=.27, tam=40),
       tar(W(k1, "infernal"), T0(k2), "Dragón infernal", "Los Grandes ya tiene 3", "oro", x=.76, y=.17, tam=40)]
mu = W(k2, "muro")
nr = "lotl_rep"          # la REPETICIÓN (sin reloj en pantalla): HUD ≈ t + 1985 por los avisos (t 96 = dragón 34:41, t 102 = Yeon 34:44-47)
EXT[nr] = ("tl_josedeodo", "lotl_j1")
K[nr] = 1985.0
FX += [*repeticion(T0(k2), T0(k2) + 3.0, "La repetición de la transmisión"), J(nr, T0(k2), mu, 96.0 - (mu - T0(k2)), 1.0)]
jo = W(k2, "Josedeodo")
FX += PZ(nr, mu, jo, 96.0, [
    muro_2d([(.06, .265), (.2, .255), (.32, .255), (.44, .25), (.56, .235), (.66, .22)], mu + .1, color=R),
    texto("EL MURO DE FEISTY", "TALIYAH · CRUZA EL RÍO", .78, .18, mu + .2, color=R, tam=30, icono="Taliyah"),
    an(.38, .23, "CoreJJ", "DEL OTRO LADO", "TLAW", W(k2, "CoreJJ"), "Lulu", lado="izq", r=38),
    an(.55, .26, "Quid", "DEL OTRO LADO", "TLAW", W(k2, "Quid"), "Viktor", lado="der", r=38),
])
FX += MESA2("los3", jo, T0(k3), H(nr, 96.0))
_ml = [W(k3, "Ackerman"), W(k3, "Zest")]
FX += CADENA("los3_b")
FX += [tar(W(k3, "dragon"), W(k3, "Ackerman"), "Liquid gana el dragón", "34:41", A, logo="TLAW", x=.27, y=.27, tam=40),
       marcador(W(k3, "Ackerman") - .3, T0(k4), "TLAW", "LOS", [("izq", 3), ("izq", 1)], _ml, titulo="34:44 · dentro del foso"),
       peg(W(k3, "Zest"), "Josedeodo", "Josedeodo", A, "TLAW", "Lo mata Zest · 34:46", dur=T0(k4) - W(k3, "Zest") + .2, x=.12, y=.62, tam=200,
           gris=True),
       tar(W(k3, "doble"), T0(k4) + .2, "Triple de Zest", "Tristana · 4 - 11", R, icono="Tristana", x=.5, y=.17, tam=44),
       dict(tipo="destello", en=W(k3, "triple"), fuerza=.4)]
FX += [*FZ(n, T0(k4), T0(k5), 30.1, 1.14), velo(T0(k4), T0(k5), .35),
       tar(T0(k4) + .1, T0(k5) + .2, "«Ya la tenía en las manos»", "Narradores, en vivo · «y se equivocan garrafal»", "oro", x=.5, y=.84, tam=48)]
FX += [J("lotl_j2", T0(k5), W(k5, "fuera"), 22.0, 1.0),
       tar(W(k5, "alma"), W(k5, "fuera"), "Alma, ancestral y partida", "Los Grandes 2 - 1 Liquid", R, logo="LOS", dato="2-1", x=.5, y=.17, tam=44),
       J("lotl_zest", W(k5, "fuera"), e1, 20.0, 1.0), velo(W(k5, "fuera"), e1, .45),
       elim(W(k5, "fuera"), e1 + .2, "TLAW", "Team Liquid", "Fuera del Mundial · 3 - 4", [W(k5, "Mundial")])]


K.update({"los1_curse": 690.5, "los2_j1": 955.8, "los2_j2": 2105.8})

# ================================================================== GANCHO · LOS G1, TLAW rojo (datos_los2.md § B, los1_curse HUD = t + 690,5)
AZUL = {"LOS"}
g = "gancho_"
e0, e1 = ESC("gancho")
k0 = g + "0"
n = "los1_curse"
FX += CADENA("gancho")
yg = W(k0, "y")
x0 = yg + 1.9                                # 12:08 (t 37,5): el 1 contra 1 → ÓRBITA; luego sigue a x1 hasta el DOUBLE KILL (12:11, t 40,5)
FX += [J(n, yg, x0, 35.6, 1.0), J(n, x0, x0 + 4.0, 37.5, 0)] + MESA2("gancho_orb", x0, x0 + 4.0, H(n, 37.5)) + [J(n, x0 + 4.0, e1, 37.5, 1.0)]
dk = x0 + 4.0 + 3.0
FX += [mg(L.apertura("¿CULPA DE JOSEDEODO?", "Sus 7 partidas del Mundial · pausa por pausa"), e0, W(k0, "Viernes") + .3, x=.5, y=.5,
          nombre="apertura"),
       dict(tipo="destello", en=.15, fuerza=.7),
       tar(W(k0, "Viernes") + .3, W(k0, "Minuto"), "Viernes 30 de octubre", "Liquid vs Los Grandes · el que pierde, se va", "oro", logo="TLAW",
           x=.27, y=.17, tam=44),
       cam(W(k0, "Josedeodo"), "Josedeodo", "Josedeodo · Nocturne", dur=x0 - W(k0, "Josedeodo"), x=.08, y=.3, tam=190),
       tar(W(k0, "Zest"), x0, "12:03 · Josedeodo mata a Zest", "Con la definitiva de Nocturne", R, icono="Nocturne", x=.27, y=.17, tam=40),
       tar(x0 + 4.0, dk, "1 contra 1", "Josedeodo nivel 8 · Curse nivel 9", "oro", x=.5, y=.17, tam=44),
       tar(dk, e1 + .2, "12:11 · DOUBLE KILL de Curse", "«José no tiene destello… y ñam, ñam, ñam» · narradores", R, logo="LOS",
           x=.5, y=.84, tam=44),
       dict(tipo="destello", en=dk, fuerza=.45)]

# ================================================================== GANCHO 2 · la acusación y el menú
g = "gancho2_"
e0, e1 = ESC("gancho2")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [*FZ("los1_curse", e0, b1, 42.0, 1.15), velo(e0, b1, .4),
       peg(W(k0, "persona"), "Josedeodo", "¿Josedeodo?", A, "TLAW", "Jungla · Team Liquid", dur=W(k0, "entrenador") - W(k0, "persona"), x=.5,
           y=.5, tam=480, gris=True),
       tar(W(k0, "entrenador"), b1 + .2, "Spawn", "El entrenador de Team Liquid", R, logo="TLAW", dato="?", x=.5, y=.5, tam=80),
       dict(tipo="destello", en=W(k0, "entrenador"), fuerza=.35)]
FX += [*REB("los1_curse", b1, 42.0, 30.0), J("al_j1", b1 + 1.2, b2, 40.0, 1.0),
       tar(W(k1, "siete"), W(k1, "draft"), "7 partidas", "Del Mundial 2026", "oro", x=.5, y=.84, tam=52),
       tar(W(k1, "draft"), b2 + .2, "Draft por draft", "Pausa por pausa", "oro", x=.5, y=.84, tam=52)]
FX += [J("lotl_j1", b2, e1, 2.0, 1.0), velo(b2, e1, .55),
       mg(L.menu([(CARGA("LeeSin"), "Los 7 drafts", "amarillo"), (JUG("Josedeodo"), "Sus números", "azul"),
                  (CARGA("Taliyah"), "La pelea en 3D", "oro")]),
          W(k2, "drafts") - .2, e1 + .2, [W(k2, "drafts"), W(k2, "numeros"), W(k2, "pelea")], y=.52, nombre="menu")]

# ================================================================== SU MEJOR PARTIDA (LOS G2, TLAW rojo; Xin Zhao pick 4 de rojo)
AZUL = {"LOS"}
g = "mejor_"
e0, e1 = ESC("mejor")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [J("los2_j2", e0, b1, 3.0, 1.0), velo(e0, b1, .5),
       grande(e0 + .1, W(k0, "asesinatos"), "Lo que nadie cuenta", None, "oro", tam=96),
       tar(W(k0, "asesinatos"), W(k0, "campeon"), "Su partida con más asesinatos", "Y con más daño · de las 7", "oro", logo="TLAW", x=.5, y=.5, tam=70),
       peg(W(k0, "campeon"), CARGA("XinZhao"), "Xin Zhao", R, "TLAW", "Elegido en la 2.ª ronda del draft", dur=b1 - W(k0, "campeon") + .2, x=.5,
           y=.5, tam=480)]
FX += [J("los2_j1", b1, e1, 0.0, 1.0),
       peg(W(k1, "Lee"), CARGA("LeeSin"), "Lee Sin", A, "LOS", "Baneado por Los Grandes", dur=W(k1, "Xin") - W(k1, "Lee"), x=.2, y=.5, tam=340,
           gris=True),
       cam(W(k1, "Xin"), "Josedeodo", "Josedeodo · Xin Zhao", dur=e1 - W(k1, "Xin") + .2, x=.08, y=.3, tam=190)]

# ================================================================== LOS G2 · TLAW rojo (datos_los2.md; los2_j1 HUD = t + 955,8 · los2_j2 HUD = t + 2105,8)
g = "los2_"
e0, e1 = ESC("los2")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
n = "los2_j1"
tv = max(0.0, 24.0 - (T0(k0) - e0))
FX += VIVO("los2", n, tv, "Partida 2 · Los Grandes vs Liquid", "TLAW", H(n, tv))
hz = W(k0, "Heraldo")
FX += CADENA("los2_a", extra=[(W(k0, "Curse"), 27.0)])
FX += PZ(n, W(k0, "Curse"), T0(k1), 27.0, [                                    # PASO A PASO: el Heraldo, con Curse debajo
    texto("HERALDO PARA LIQUID", "JOSEDEODO · 16:23", .5, .14, hz + .1, color=R, tam=30, icono="SummonerSmite"),
    an(.33, .37, "Josedeodo", "XIN ZHAO · SE LO LLEVA", "TLAW", W(k0, "Curse") + .1, "XinZhao", lado="izq"),
    an(.45, .65, "Curse", "JARVAN IV · JUSTO DEBAJO", "LOS", W(k0, "Curse") + .4, "JarvanIV", lado="der"),
])
FX += CADENA("los2_b")
du = W(k1, "Duduhh")
y1 = W(k1, "Y", 1)
FX += MESA2("los2_orb", du, y1, H(n, 36.5))                                   # ÓRBITA: cae Duduhh; la ruta de la caza a Feisty
FX += SYNC2(n, [(du, 36.5)] + [(anc(a), a[4]) for a in CAD["los2_c"]])
_m2 = [du, du + .5, W(k1, "mata", 1)]
FX += [marcador(y1, T0(k2), "TLAW", "LOS", [("der", 3), ("der", 1), ("der", 2)], [y1 + .2, y1 + .6, W(k1, "mata", 1)], titulo="16:32 · la pelea del Heraldo"),
       tar(y1, W(k1, "mata", 1), "16:32 · Duduhh, fuera", "Y Josedeodo va por Feisty", R, logo="TLAW", x=.27, y=.27, tam=40),
       tar(W(k1, "mata", 1), T0(k2) + .2, "16:45 · Josedeodo mata a Feisty", "«Is on a rampage» · Liquid +3,0K", R, logo="TLAW", x=.27, y=.27, tam=40),
       dict(tipo="destello", en=W(k1, "mata", 1), fuerza=.35)]
FX += [J(n, T0(k2), T0(k3), 72.0, 1.0), *repeticion(T0(k2), T0(k2) + 3.0, "La repetición de la transmisión"),
       tar(T0(k2) + .3, T0(k3) + .2, "«Josedeodo, demostrando por qué…»", "«…es el mejor jugador de su equipo» · narradores", "oro", x=.5, y=.84, tam=46)]
n = "los2_j2"
FX += CADENA("los2_d")
FX += [tar(W(k3, "Minuto"), W(k3, "cae"), "Minuto 35 · el Anciano", "Curse, dentro de su propio Cataclismo", R, icono="JarvanIV", x=.27, y=.27, tam=40),
       tar(W(k3, "cae"), W(k3, "Feisty"), "35:41 · CoreJJ mata a Curse", "Liquid 10 - 8", R, logo="TLAW", x=.27, y=.27, tam=40),
       tar(W(k3, "Feisty"), W(k3, "ancestral"), "35:48 · Josedeodo mata a Feisty", "Otra vez", R, icono="XinZhao", x=.27, y=.27, tam=40),
       tar(W(k3, "ancestral"), T0(k4) + .2, "Anciano para Liquid", "36:09 · sin perder a nadie", R, logo="TLAW", x=.5, y=.17, tam=44),
       dict(tipo="destello", en=W(k3, "ancestral"), fuerza=.4)]
FX += [*FZ(n, T0(k4), e1, 66.0, 1.12), velo(T0(k4), e1, .5),
       mg(L.premio("Su mejor partida", JUG("Josedeodo"), "Josedeodo", EQ("TLAW"), ["5 asesinatos · 1 muerte · 10 asistencias",
                                                                                 "Liquid 15 - 8 · 5 dragones", "Serie 1 - 1"],
                   color="rojo", sub="Xin Zhao · 2.ª ronda del draft"),
          T0(k4) + .1, e1 + .2, [W(k4, "cinco"), W(k4, "quince"), W(k4, "empata")], y=.5, nombre="premio los2")]
