# -*- coding: utf-8 -*-
"""Montaje de las JUGADAS de t1_blg_caida: g4a, g3a, g1, g2, g3r, g3, g4, faker_e (el resto, fx_escenas.py). Lo ejecuta efectos.py con exec.
Formas (las de lol_final_previa, se SUMAN): 4 (marcador NFL) y 5 (oro en vivo del feed) en cada jugada; mesa 3D con cámara normal en g3
(j5a, los 10 medidos); Grieta 3D de la G4 con cámara NUEVA (j6_3d.py: órbita lateral, no la de la previa); pausas con chip del reloj;
rebobinados y repeticiones rotuladas. Anillos SOLO en pies medidos (j6 t 77 de datos_j6.md). Datos: investigacion/datos_g1.md, datos_g3a.md,
datos_g4a.md, datos_j4..j6.md, datos_relleno.md § j4b. Nada pasa de x1 (SYNC/SYNC2 cortan o pausan)."""
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



K.update({"g1_j1": 917.0, "g1_j2": 1220.0, "g1_j3": 1416.0})

# ================================================================== G1 · BLG azul, T1 rojo (datos_g1.md) · formas 4 (marcador) y 5 (oro) + pausas
AZUL = {"BLG"}
g = "g1_"
e0, e1 = ESC("g1")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
n = "g1_j1"
FX += VIVO("g1", n, 0.0, "Semifinal · domingo 8 de noviembre · partida 1", "BLG", "15:17")      # en vivo: «¡Se lo roba!» (t 4)
f0 = T0(k0)
rb = W(k0, "roba")
FX += REBX(n, f0, f0 - e0, max(rb, f0 + 1.3), 4.0)                        # rebobina y el robo cae cuando la voz dice «roba»
pz = rb + 1.6
FX += PZ(n, rb, pz, 4.0, [texto("HERALDO ROBADO", "XUN · NAAFIRI · 15:21", .5, .2, rb + .1, color=A, tam=34, icono="Naafiri")])
_g1a = SYNC2(n, [(pz, 4.0), (W(k0, "pelea"), 9.0), (W(k0, "Bin"), 20.0), (W(k1, "Peyz"), 23.0), (W(k1, "Faker"), 26.0),
                 (W(k1, "Doran"), 31.0), (T0(k2), 36.0)])
FX += _g1a
_mg1 = [W(k0, "Bin"), W(k1, "Peyz"), W(k1, "Faker"), W(k1, "Doran")]
FX += [marcador(W(k0, "pelea"), T0(k2) - .2, "BLG", "T1", [("izq", 0), ("der", 3), ("der", 2), ("der", 0)], _mg1, titulo="15:37 · la primera pelea"),
       oro(W(k0, "pelea"), T0(k2) - .2, "122", 900, 965, [922, 937, 940, 943, 948], [W(k0, "pelea") + .2] + _mg1, "BLG", "T1",
           notas=[(948, "Bilibili +1,6K")], x=.83, y=.25, escala=.5, desfase=5),
       cam(W(k1, "Knight"), "Knight", "Knight · Orianna", dur=T0(k2) - W(k1, "Knight"), x=.08, y=.3, tam=190),
       tar(W(k1, "Tres"), T0(k2), "3 por 1 · Bilibili", "Doble de Knight: Faker y Doran", A, logo="BLG", dato="3-1", x=.5, y=.17, tam=40)]
n = "g1_j2"
b2 = T0(k2)
gt = W(k2, "gratis")
FX += SYNC2(n, [(b2, 2.0), (W(k2, "Oner"), 7.0), (W(k2, "Baron"), 14.0), (gt, 39.0), (W(k2, "Doran"), 56.0), (T0(k3), 58.0)])
FX += [tar(b2 + .1, W(k2, "Oner"), "Minuto 20", "Partida 1", "oro", x=.5, y=.17, tam=40),
       pv(W(k2, "Viper"), "Viper", "Viper · Corki", dur=2.6, x=.11, y=.3, tam=280),
       cam(W(k2, "Oner") + .1, "Oner", "Oner · cae a las 20:27", dur=W(k2, "gratis") - W(k2, "Oner"), x=.08, y=.62, tam=190),
       tar(W(k2, "Baron"), gt, "T1 no disputa el Barón", "Sin jungla: nadie con Castigo", R, logo="T1", x=.5, y=.17, tam=40),
       tar(gt, W(k2, "Doran"), "Barón para Bilibili", "21:00 · «un objetivo gratuito» (narradores)", A, logo="BLG", x=.5, y=.17, tam=40),
       tar(W(k2, "Doran"), T0(k3) + .2, "Knight caza a Doran", "21:17", A, icono="Orianna", x=.5, y=.17, tam=40),
       oro(W(k2, "Oner"), T0(k3), "122", 1200, 1300, [1227, 1260, 1277], [W(k2, "Oner") + .2, gt, W(k2, "Doran")], "BLG", "T1",
           notas=[(1277, "Bilibili +5,1K")], x=.83, y=.25, escala=.5, desfase=5)]
n = "g1_j3"
b3, b4 = T0(k3), T0(k4)
FX += [*FZ("g1_j3", b3, W(k3, "veinticuatro"), 0.0, 1.12, chip="23:36"), velo(b3, W(k3, "veinticuatro"), .3),
       tar(b3 + .1, W(k3, "veinticuatro"), "4 torres en 2 minutos", "Y el inhibidor de abajo · 23:15", A, logo="BLG", dato="7-3", x=.5, y=.17, tam=40)]
_mg3 = [W(k3, "ON"), W(k3, "responde"), W(k3, "responde") + .6, W(k3, "cuatro", 1), W(k3, "cuatro", 1) + .4]
FX += SYNC2(n, [(W(k3, "veinticuatro"), 11.0), (W(k3, "ON"), 17.0), (W(k3, "responde"), 20.0), (W(k3, "cuatro", 1), 43.0), (b4, 46.0),
                (e1, None)])
FX += [marcador(W(k3, "veinticuatro"), e1 - .3, "BLG", "T1", [("izq", 4), ("der", 1), ("der", 4), ("der", 0), ("der", 3)], _mg3,
                titulo="23:53 · la base de T1"),
       tar(W(k3, "cuatro", 1), b4 + .2, "4 por 1 en la base", "Oner, Keria, Doran y Peyz", A, logo="BLG", dato="4-1", x=.5, y=.17, tam=40),
       mg(L.premio("Partida 1 · el mejor", JUG("Knight"), "Knight", EQ("BLG"), ["8 asesinatos · 0 muertes · 9 asistencias", "Orianna"],
                   color="azul", sub="Medio · Bilibili"), b4, e1, [W(k4, "ocho"), W(k4, "morir")], y=.5, nombre="premio Knight g1"),
       velo(b4, e1, .4)]

K.update({"g3_j1": 180.0, "g3_j2": 577.0, "g3_j3": 1320.0, "g2_faker": 1057.0})

# ================================================================== G3 ARRANQUE · BLG azul (datos_g3a.md A1, A2): Doran cae a las 03:35 y a las 10:08
AZUL = {"BLG"}
g = "g3a_"
e0, e1 = ESC("g3a")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
n = "g3_j1"
# en vivo 4 s antes de la voz: 03:22 Doran solo frente a Bin (t 22) → la voz arranca en t 26
FX += VIVO("g3a", n, 22.0, "Semifinal · partida 3", "BLG", "03:22")
FX += SYNC2(n, [(T0(k0), 26.0), (W(k0, "Xun"), 29.0), (W(k0, "aturde"), 30.0), (W(k0, "Bin"), 31.0), (W(k0, "torre"), 35.0), (T0(k1), 36.0)])
FX += [tar(W(k0, "Partida"), W(k0, "Xun"), "Partida 3 · minuto 3", "Doran · Ambessa contra Bin · Gnar", R, logo="T1", x=.27, y=.27, tam=40),
       pv(W(k0, "Xun"), "Xun", "Xun · Pantheon", dur=2.8, x=.11, y=.36, tam=300),
       tar(W(k0, "torre"), T0(k1) + .2, "03:35 · Xun mata a Doran", "Asistencia de Bin", A, logo="BLG", x=.27, y=.27, tam=40),
       dict(tipo="destello", en=W(k0, "torre"), fuerza=.3)]
FX += [*FZ(n, T0(k1), T0(k2), 36.0, 1.14, .5, .4), velo(T0(k1), T0(k2), .35),
       tar(T0(k1) + .1, T0(k2) + .2, "«La línea que tenían que ganar…»", "«…ahora la tienen en su contra» · narradores, en vivo", "oro", x=.5, y=.84, tam=48)]
n = "g3_j2"
FX += SYNC2(n, [(T0(k2), 14.0), (W(k2, "Bin"), 19.5), (W(k2, "torre"), 21.0), (W(k2, "definitiva"), 23.5), (W(k2, "alcanza"), 27.0),
                (W(k2, "Viper", 1), 31.0), (T0(k3), 33.0), (e1, None)])
FX += [tar(T0(k2) + .1, W(k2, "Bin"), "Minuto 10", "Partida 3", "oro", x=.5, y=.17, tam=40),
       marcador(W(k2, "Bin") - .2, T0(k3), "BLG", "T1", [("der", 0)], [W(k2, "Viper", 1)], titulo="10:08 · buceo bajo la torre"),
       tar(W(k2, "definitiva"), W(k2, "Viper", 1), "La definitiva de Doran", "Salta hacia Xun… y no lo alcanza", R, icono="Ambessa", x=.5, y=.17, tam=40),
       tar(W(k2, "Viper", 1), T0(k3), "10:08 · Viper remata a Doran", "Doran 0/2", A, icono="Ezreal", x=.5, y=.17, tam=40),
       mg(L.duelo((JUG("Doran"), "Doran", EQ("T1"), R, "Ambessa"), (JUG("Bin"), "Bin", EQ("BLG"), A, "Gnar"), "Minuto 10",
                  [("Muertes", "2", "0", 1.0, .02, 1), ("Súbditos", "75", "102", 75 / 102, 1.0, 1), ("Oro", "−1,1K", "+1,1K", .4, 1.0, 1)]),
          T0(k3), e1 + .2, [W(k3, "Dos"), W(k3, "Bin"), W(k3, "mil")], y=.5, nombre="duelo Doran-Bin g3"),
       velo(T0(k3), e1, .45)]

# ================================================================== G3 REMONTADA · BLG azul (datos_g3a.md A3, g3_j3 HUD = t + 1320): de 7-4 a 8-8
g = "g3r_"
e0, e1 = ESC("g3r")
k0, k1, k2 = (g + str(i) for i in range(3))
n = "g3_j3"
FX += FZ(n, e0, T0(k0), 0.0, 1.08)          # 22:00 congelado con acercamiento: el muro cruza el río
FX += [pizarra(e0, T0(k0), [], "22:00"),
       tar(e0 + .2, T0(k0), "Partida 3 · minuto 22", "Bilibili 7 - 4 · +1,0K", A, logo="BLG", x=.27, y=.27, tam=40)]
FX += SYNC2(n, [(T0(k0), 0.0), (W(k1, "roba"), 2.0), (W(k1, "ON"), 4.0), (W(k1, "Bin"), 9.0), (W(k1, "Xun"), 11.0), (W(k2, "Keria"), 16.0),
                (W(k2, "Knight"), 22.0), (W(k2, "remata"), 30.0), (W(k2, "remata") + .8, 31.0), (e1, 40.0)])
_mgr = [W(k1, "ON"), W(k1, "Bin"), W(k1, "Xun"), W(k2, "Keria"), W(k2, "remata")]
FX += [tar(W(k0, "muro"), T0(k1), "El muro de Knight", "Taliyah · cruza el río", A, icono="Taliyah", x=.27, y=.27, tam=40),
       tar(W(k1, "roba"), W(k1, "ON"), "Oner se lo roba", "Dragón infernal · 22:01", R, icono="JarvanIV", x=.27, y=.27, tam=40),
       marcador(W(k1, "roba"), e1 - .3, "BLG", "T1", [("izq", 4), ("izq", 0), ("izq", 1), ("der", 4), ("izq", 2)], _mgr, titulo="22:01 · la remontada"),
       oro(W(k1, "roba"), e1 - .3, "124", 1310, 1370, [1326, 1329, 1334, 1337, 1341, 1355, 1360], [W(k1, "roba") + .2] + _mgr + [W(k2, "oro")],
           "BLG", "T1", x=.83, y=.25, escala=.5, desfase=5),
       cam(W(k1, "Faker"), "Faker", "Faker · Ahri", dur=W(k1, "Peyz") - W(k1, "Faker") + .3, x=.08, y=.3, tam=190),
       tar(W(k2, "remata"), e1, "De 7 - 4 a 8 - 8", "22:33 · T1 +1,0K · Faker, 2 asesinatos", R, logo="T1", dato="8-8", x=.5, y=.17, tam=44)]

# ================================================================== FAKER EN LA PARTIDA 2 · T1 azul (datos_g3a.md B, g2_faker HUD = t + 1057)
AZUL = {"T1"}
g = "faker_e_"
e0, e1 = ESC("faker_e")
k0, k1, k2 = (g + str(i) for i in range(3))
n = "g2_faker"
FX += SYNC2(n, [(e0, 4.0), (W(k0, "torre"), 8.3), (W(k1, "aturde"), 8.8), (W(k1, "Doran"), 9.5), (W(k1, "remata"), 12.9), (T0(k2), 13.5)])
ep = W(k1, "aturde") + .1
FX += [tar(e0 + .1, W(k0, "Bin"), "Partida 2 · minuto 17", "BLG +2,4K", R, logo="BLG", x=.27, y=.27, tam=40),
       pv(W(k0, "Bin"), "Bin", "Bin · Camille · solo", dur=3.0, x=.11, y=.36, tam=300),
       tar(W(k1, "Faker"), W(k1, "Llegan"), "Dispersar a los Débiles", "La E de Syndra · 17:46", A, icono="Syndra", x=.27, y=.27, tam=40),
       tar(W(k1, "remata"), T0(k2) + .2, "17:50 · Oner remata a Bin", "Asistencias: Faker, Doran y Keria", A, logo="T1", x=.27, y=.27, tam=40),
       dict(tipo="destello", en=ep, fuerza=.3)]
# la repetición del VOD (t 37,5-42): la misma E sobre Knight, minutos antes (17:03-17:08)
FX += [J(n, T0(k2), W(k2, "Knight") - .2, 13.5 + 0, 0, zoom=(1.12, .5, .5), zoom0=(1.0, .5, .5), zoom_dur=1.5),
       pizarra(T0(k2), W(k2, "Knight") - .2, [], "17:50"),
       *LENTA(n, W(k2, "Knight") - .2, e1, 42.0, vel=.6, sub="Repetición · la misma E sobre Knight, 17:03"),
       tar(T0(k2) + .1, W(k2, "Knight"), "«Faker la hace de nuevo»", "Narradores, en vivo", "oro", x=.5, y=.84, tam=48),
       tar(W(k2, "asesinato"), e1, "Sin asesinato", "Pero la jugada fue suya", A, logo="T1", x=.5, y=.84, tam=48)]

K.update({"j4b": 1382.0, "j4": 1802.0, "j5": 1904.0, "j6": 1860.0, "j6_fin": 2249.0})

# ================================================================== G2 · T1 azul (datos_relleno.md § j4b, HUD = t + 1382; cierre j4, HUD = t + 1802)
AZUL = {"T1"}
g = "g2_"
e0, e1 = ESC("g2")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
n = "j4b"
FX += VIVO("g2", n, 0.0, "Semifinal · domingo 8 de noviembre · partida 2", "T1", "23:02")
rob = W(k1, "robado")
_g2 = SYNC2(n, [(T0(k0), 6.0), (W(k1, "foso"), 9.0), (W(k1, "Oner"), 11.0), (rob, 13.3), (W(k2, "ON"), 16.3), (W(k2, "Xun"), 19.6),
                (W(k2, "reloj"), 20.2), (W(k2, "Oner"), 21.8), (W(k2, "Keria"), 35.5), (W(k3, "teleportacion"), 36.4), (W(k3, "Viper"), 40.7),
                (W(k3, "Knight"), 46.2), (T0(k4), 47.0)])
FX += _g2
_mg2 = [W(k2, "ON"), W(k2, "Xun"), W(k2, "Oner"), W(k2, "Keria"), W(k3, "Viper"), W(k3, "Knight")]
FX += [tar(W(k0, "Minuto"), W(k0, "alma"), "Minuto 23 · T1", "Barón y 3 dragones · T1 +1,1K", A, logo="T1", x=.27, y=.27, tam=40),
       tar(W(k0, "alma"), rob, "El 4.º dragón = el alma", "El del océano", "oro", x=.27, y=.27, tam=40),
       cam(W(k1, "Oner"), "Oner", "Oner · Lee Sin", dur=rob - W(k1, "Oner") + .6, x=.08, y=.3, tam=190),
       tar(rob, T0(k2) + .2, "¡Robado!", "23:15 · alma del océano para T1", A, logo="T1", x=.5, y=.17, tam=46),
       dict(tipo="destello", en=rob, fuerza=.4),
       marcador(W(k2, "ON") - .3, T0(k4) - .2, "T1", "BLG", [("der", 4), ("der", 1), ("izq", 1), ("izq", 4), ("der", 3), ("der", 2)], _mg2,
                titulo="23:17 · la pelea del alma"),
       oro(W(k1, "foso"), T0(k4) - .2, "123", 1370, 1450, [1382, 1395, 1401, 1404, 1423, 1442, 1448], [W(k1, "foso") + .2, rob] + _mg2[1:3]
           + _mg2[3:], "T1", "BLG", x=.83, y=.25, escala=.5, desfase=6),
       tar(W(k2, "reloj"), W(k2, "Pero"), "Reloj de arena de Zhonya", "Faker no recibe daño", A, icono="Syndra", x=.27, y=.27, tam=40),
       tar(W(k3, "teleportacion"), W(k3, "Cuatro"), "Vuelve Faker", "Con la teleportación", A, icono="SummonerTeleport", x=.27, y=.27, tam=40),
       tar(W(k3, "Cuatro"), T0(k4) + .2, "4 por 2 para T1", "Faker remata a Knight · 23:48", A, logo="T1", dato="4-2", x=.5, y=.17, tam=44)]
FX += [J("j4", T0(k4), T0(k4) + 12.5, 16.0, 1.0), J("j4", T0(k4) + 12.5, e1, 111.5, 1.0),
       tar(W(k4, "ancestral"), W(k4, "veintidos"), "Dragón ancestral · T1", "30:28", A, logo="T1", x=.76, y=.17, tam=40),
       tar(W(k4, "veintidos"), W(k4, "Asi"), "T1 gana 22 a 10", "Serie 1 - 1", A, logo="T1", dato="1-1", x=.5, y=.17, tam=44),
       grande(W(k4, "Asi"), e1, "Así gana T1", "Cuando el río es suyo: 4 dragones a 0", "oro", y=.82, tam=70)]

# ================================================================== G3 · BLG azul (datos_j5.md, HUD = t + 1904): la pelea del alma infernal
AZUL = {"BLG"}
g = "g3_"
e0, e1 = ESC("g3")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
n = "j5"
TV5 = 8.6
FX += VIVO("g3", n, TV5, "Semifinal · domingo 8 de noviembre · partida 3", "BLG", H(n, TV5))
FX += SYNC2(n, [(T0(k0), TV5 + T0(k0) - e0), (T0(k1), 40.0), (T1(k1) - .2, 45.5)])
FX += [oro(T0(k0) + .2, T0(k1), "124", 1200, 1960, [1500, 1930], [W(k0, "remontada"), W(k0, "treinta")], "BLG", "T1",
           notas=[(1500, "T1 arriba")], titulo="Partida 3 · diferencia de oro", x=.5, y=.5, escala=.9, desfase=5),
       velo(T0(k0), T0(k1), .35),
       tar(W(k1, "infernal"), T1(k1), "Dragón infernal", "Si es de Bilibili: el alma", "oro", x=.76, y=.17, tam=40)]
m0, m1 = T1(k1) - .2, W(k2, "Viper") - .3
FX += MESA2("j5a", m0, m1, H(n, 46.0))
FX += SYNC(n, [(m1, 46.0), (W(k2, "resucita"), 50.5), (W(k3, "Oner"), 59.0), (W(k3, "Bin"), 62.0), (W(k3, "Doran"), 65.0),
               (W(k3, "alma"), 70.3), (W(k4, "Knight"), 76.0), (W(k4, "torre"), 79.0), (W(k4, "Peyz"), 82.0), (W(k4, "Peyz") + 2.3, 84.3)])
FX += SYNC2(n, [(W(k4, "Peyz") + 2.3, 84.3), (e1, 89.0)])
_mg3 = [W(k3, "Oner"), W(k3, "Bin"), W(k3, "Doran"), W(k4, "Knight"), W(k4, "Peyz"), W(k4, "Keria")]
FX += [tar(W(k2, "resucita"), T0(k3), "Ángel de la Guarda", "Viper vuelve · 32:35", A, icono="Ezreal", x=.76, y=.17, tam=40),
       marcador(T0(k3) - .2, e1 - .3, "BLG", "T1", [("der", 1), ("izq", 0), ("der", 0), ("izq", 2), ("der", 3), ("der", 4)], _mg3,
                titulo="32:43 · el alma infernal"),
       oro(T0(k3) - .2, e1 - .4, "124", 1930, 2000, [1953, 1963, 1966, 1969, 1974, 1980, 1986], [T0(k3)] + _mg3, "BLG", "T1",
           x=.83, y=.25, escala=.5, desfase=5),
       tar(W(k3, "alma"), T0(k4) + .2, "Alma infernal · Bilibili", "32:54 · su 4.º dragón", A, logo="BLG", x=.5, y=.17, tam=40),
       tar(W(k4, "doble"), W(k4, "Baron"), "Doble de Viper", "Peyz y Keria · 33:06", A, icono="Ezreal", x=.5, y=.17, tam=40),
       tar(W(k4, "Baron"), e1, "Bilibili 2 - 1", "Gana la partida 3, 19 a 10", A, logo="BLG", dato="2-1", x=.5, y=.17, tam=44)]

# ================================================================== G4 · T1 azul (datos_j6.md, HUD = t + 1860): la pelea final, en 3D con cámara NUEVA
AZUL = {"T1"}
g = "g4_"
e0, e1 = ESC("g4")
k0, k1, k2, k3, k4, k5 = (g + str(i) for i in range(6))
n = "j6"
J3D_J6 = os.path.join(_D, "medios", "_fuente", "j6_3d.mp4")
v0 = T0(k0)
G0_6 = 1926.0
tv0 = (G0_6 - K[n]) - (v0 - e0)
FX += VIVO("g4", n, tv0, "Semifinal · domingo 8 de noviembre · partida 4", "T1", H(n, tv0))
A6 = T0(k2) + .4
TIEMPOS_3D["j6"] = dict(de=round(v0, 3), a=round(A6, 3), reloj=[
    [round(v0, 3), G0_6], [round(W(k0, "tira"), 3), 1934.0], [round(W(k1, "Oner") + .3, 3), 1934.6],
    [round(W(k1, "Viper", fin=True) + .5, 3), 1935.0], [round(W(k1, "resucita"), 3), 1936.0], [round(A6, 3), 1937.2]])
FX += [V3(v0, A6, J3D_J6, v0), congelado_que_funde(n, v0, G0_6 - K[n])]
sv = W(k2, "llegan")
_r = REBX(n, T0(k2), 1937.2 - K[n], sv, 76.0)
_r[0]["entra"] = .4
FX += _r
p6 = sv + 1.0
q6 = W(k3, "Oner") - (78.06 - 77.0)
FX += SYNC(n, [(sv, 76.0), (p6, 77.0)])
FX += PZ(n, p6, q6, 77.0, [
    texto("VIPER SIGUE VIVO", "ÁNGEL DE LA GUARDA · 32:16", .70, .56, p6 + .1, color=R, tam=30, icono="Ashe"),
    an(.37, .43, "Bin", "RENEKTON · POR ARRIBA", "BLG", W(k2, "Bin"), "Renekton", lado="izq"),
    an(.465, .66, "Xun", "SKARNER · POR ABAJO", "BLG", W(k2, "Xun"), "Skarner", lado="der"),
    an(.56, .39, "Faker", "SOLO, DETRÁS DE KNIGHT Y ON", "T1", W(k2, "Faker"), "Akali", lado="der", r=38),
])
FX += SYNC(n, [(q6, 77.0), (W(k3, "Oner"), 78.06), (W(k3, "Doran"), 83.0), (W(k3, "Faker"), 87.0), (T0(k5), None)])
_mg6 = [W(k3, "Oner"), W(k3, "Doran"), W(k3, "Faker")]
FX += [marcador(T0(k3) - .2, T0(k5) - .3, "T1", "BLG", [("izq", 1), ("izq", 0), ("izq", 2)], _mg6, titulo="32:18 · 3 por 0"),
       oro(T0(k3) - .2, T0(k5) - .3, "125", 1900, 1975, [1936, 1938, 1943, 1947, 1955], [T0(k3)] + _mg6 + [T0(k4)], "T1", "BLG",
           x=.83, y=.25, escala=.5, desfase=5),
       tar(W(k3, "nueve"), T0(k4), "3 de T1 en 9 segundos", "Y nadie de Bilibili", R, logo="BLG", dato="3-0", x=.5, y=.17, tam=40),
       tar(T0(k4), T0(k5), "Los narradores, en vivo", "«T1 fuerza la pelea y se sobreextiende»", "oro", x=.5, y=.17, tam=40)]
n = "j6_fin"
nx = W(k5, "nexo")
ts = max(0.0, 16.0 - (nx - T0(k5)))
FX += [J(n, T0(k5), e1, ts, 1.0),
       tar(W(k5, "alma"), W(k5, "nexo"), "Alma de montaña y Barón", "34:55 y 35:54 · Bilibili", R, logo="BLG", x=.5, y=.17, tam=40),
       tar(nx, W(k5, "rompio"), "Cae el nexo · 37:42", "Bilibili 3 - 1 T1", R, logo="BLG", dato="3-1", x=.5, y=.17, tam=44),
       dict(tipo="destello", en=nx, fuerza=.5),
       elim(W(k5, "rompio"), e1, "T1", "T1", "Se rompió la dinastía", [W(k5, "dinastia")])]

# ================================================================== G4 ARRANQUE · T1 azul (datos_g4a.md): la Vayne, las larvas, Doran 10:52 y el foso 17:33
K.update({"g4_j1": 485.0, "g4_j2": 637.0, "g4_j3": 1025.0})
AZUL = {"T1"}
g = "g4a_"
e0, e1 = ESC("g4a")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
n = "g4_draft"
FX += VIVO("g4a", n, 4.0, "Semifinal · partida 4 · el draft", "T1", "Draft")          # en vivo: la Vayne (t 8) y «¡Ay, no puede ser!»
FX += SYNC2(n, [(T0(k0), 4.0 + T0(k0) - e0), (W(k0, "Vayne"), 18.0), (T0(k1), 22.0)])
FX += [abanico(W(k0, "Renekton") - .1, W(k0, "narradores"), [(CARGA("Renekton"), "Bin · Renekton"), (CARGA("Vayne"), "Doran · Vayne")],
               [W(k0, "Renekton"), W(k0, "Vayne")], y=.47, tam=360, nombre="abanico Vayne"),
       tar(W(k0, "Vayne"), W(k0, "narradores"), "Vayne: última selección del draft", "1,1 % de elección en el torneo · 0 - 1", R, icono="Vayne", x=.5, y=.86, tam=40),
       velo(W(k0, "Vayne"), W(k0, "narradores"), .4),
       tar(W(k0, "narradores"), T0(k1) + .2, "«¡No puede ser!» · «Estoy en shock»", "Los narradores, en vivo", "oro", x=.5, y=.84, tam=48)]
n = "g4_j1"
FX += SYNC2(n, [(T0(k1), 14.0), (W(k1, "Viper"), 21.5), (W(k1, "Keria"), 44.0), (W(k1, "Peyz"), 52.0), (T0(k2), 55.0)])
_m4a = [W(k1, "Viper"), W(k1, "Keria"), W(k1, "Peyz")]
FX += [tar(T0(k1) + .1, W(k1, "Viper"), "Minuto 8 · las larvas del vacío", "Oner, solo en el foso", R, icono="MonkeyKing", x=.27, y=.27, tam=40),
       marcador(W(k1, "Viper") - .3, T0(k2) - .2, "T1", "BLG", [("izq", 1), ("izq", 4), ("izq", 3)], _m4a, titulo="08:26 · 3 en 30 segundos"),
       oro(W(k1, "Viper") - .3, T0(k2) - .2, "125", 480, 550, [506, 528, 536, 542], [W(k1, "Viper")] + _m4a[1:] + [T0(k2) - .5], "T1", "BLG",
           notas=[(542, "Bilibili +1,9K")], x=.83, y=.25, escala=.5, desfase=5)]
n = "g4_j2"
FX += SYNC2(n, [(T0(k2), 2.0), (W(k2, "Xun"), 2.5), (W(k2, "torre"), 7.0), (W(k2, "remata"), 15.0), (T0(k3), 16.0)])
FX += [tar(T0(k2) + .1, W(k2, "Xun"), "Minuto 10", "Doran −0,6K contra Bin", R, logo="T1", x=.27, y=.27, tam=40),
       pv(W(k2, "Xun"), "Xun", "Xun · Skarner", dur=2.6, x=.11, y=.36, tam=300),
       tar(W(k2, "remata"), T0(k3) + .2, "10:52 · Bin mata a Doran", "Bajo su torre", A, icono="Renekton", x=.27, y=.27, tam=40)]
n = "g4_j3"
f3 = W(k3, "foso")
FX += [*FZ(n, T0(k3), f3, 1.0, 1.12, chip="17:06"), velo(T0(k3), f3, .3),
       mg(L.duelo((JUG("Doran"), "Doran", EQ("T1"), "azul", "Vayne"), (JUG("Bin"), "Bin", EQ("BLG"), "rojo", "Renekton"), "Minuto 17",
                  [("Súbditos", "126", "150", 126 / 150, 1.0, 1), ("Oro", "−1,1K", "+1,1K", .55, 1.0, 1)]),
          T0(k3) + .1, f3, [W(k3, "Doran"), W(k3, "mil")], y=.5, nombre="duelo Doran-Bin g4")]
FX += SYNC2(n, [(f3, 24.0), (W(k3, "cuatro"), 26.5), (W(k3, "mata"), 28.0), (W(k3, "dragon", 1), 40.0), (e1, None)])
_m4c = [W(k3, "mata"), W(k3, "mata") + .6, W(k3, "cuatro", 1), W(k3, "cuatro", 1) + .4]
FX += [marcador(f3, e1 - .3, "T1", "BLG", [("izq", 3), ("izq", 4), ("izq", 1), ("izq", 0)], _m4c, titulo="17:33 · el foso del dragón"),
       tar(W(k3, "cuatro"), W(k3, "mata"), "La definitiva de ON", "Seraphine atrapa a cuatro", R, icono="Seraphine", x=.27, y=.27, tam=40),
       tar(W(k3, "dragon", 1), e1, "3 - 10 · Bilibili +4,7K", "17:47 · y el dragón", R, logo="BLG", dato="3-10", x=.5, y=.17, tam=44)]
