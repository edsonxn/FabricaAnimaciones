# -*- coding: utf-8 -*-
"""Elementos que se dibujan ENCIMA del mapa con relieve (kz_mapa.py): ciudades como mini-dioramas isométricos, banderas, ondas, rutas con flujo, ejércitos en marcha,
montañas/volcanes sobre las cumbres reales del relieve, rótulos de región, brújula y escala. Todo en vector sobre el Lienzo (cámara = (lon, lat, z) como en kz_mapa)."""
import math

import cv2
import numpy as np

import kz_iso as I
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_obj as O
import kz_gente_iso as G
import kz_mapa as KM
import kz_ui as U
import plano as P
from motor import W, H, circulo, elipse, rect_red, h01, catmull, prog, smooth, e_back, e_out, ancho_texto

M = KM.MAPA

CIUDADES = {
    "mexico": (-99.13, 19.43), "dolores": (-100.93, 21.16), "guanajuato": (-101.26, 21.02), "queretaro": (-100.39, 20.59), "valladolid": (-101.19, 19.70),
    "guadalajara": (-103.35, 20.67), "calderon": (-102.97, 20.62), "monte_cruces": (-99.35, 19.30), "aculco": (-99.83, 20.10), "chihuahua": (-106.09, 28.63),
    "acatita": (-101.40, 26.90), "cuautla": (-98.94, 18.81), "chilpancingo": (-99.50, 17.55), "acapulco": (-99.92, 16.85), "oaxaca": (-96.73, 17.06),
    "veracruz": (-96.13, 19.18), "iguala": (-99.54, 18.35), "cordoba": (-96.93, 18.89), "apatzingan": (-102.35, 19.09), "temalaca": (-97.60, 18.30),
    "puebla": (-98.20, 19.04), "zacatecas": (-102.58, 22.77), "san_luis": (-100.98, 22.15), "soto_marina": (-97.75, 23.75), "caracuaro": (-101.07, 19.00),
    "tampico": (-97.86, 22.23), "san_blas": (-105.3, 21.5), "zitacuaro": (-100.36, 19.43), "madrid": (-3.70, 40.42), "cadiz": (-6.29, 36.53), "lisboa": (-9.14, 38.72), "paris": (2.35, 48.86), "londres": (-0.12, 51.50), "roma": (12.50, 41.90), "berlin": (13.40, 52.52), "ecatepec": (-99.06, 19.60), "tehuacan": (-97.39, 18.46),
}

INS = (96, 206, 140)
REAL = (226, 84, 78)
TRI = [((46, 160, 80), 1 / 3), ((250, 250, 244), 1 / 3), ((210, 50, 62), 1 / 3)]


def _scr(cam, lugar):
    lo, la = CIUDADES[lugar] if isinstance(lugar, str) else lugar
    x, y = M.proy(cam, lo, la)
    return float(x), float(y)


# ------------------------------------------------------------------------------------------------ ciudades
def ciudad(lz, cam, lugar, t, t0=0.0, tam=1.0, tipo="pueblo", bando=None, llama=False, nombre=None, px=30, alfa=1.0, color_nombre=U.COL["morado"], semilla=1):
    """Mini-diorama isométrico sobre el mapa: baldosa de tierra con iglesia/casas (pueblo), muchas casas (ciudad), muros (fuerte) o casas+muelle (puerto). Aparece con el «pop» del original."""
    k = U.pop(t, t0)
    if k <= 0.01:
        return
    sx, sy = _scr(cam, lugar)
    if sx < -140 or sx > W + 140 or sy < -140 or sy > H + 140:
        return
    # con el mapa lejano los íconos se achican (antes medían lo mismo y 12 ciudades se apilaban en México)
    tam = tam * float(np.clip((cam[2] / 0.7) ** 0.75, 0.30, 1.0))
    # ... y los que se encimarían con uno ya dibujado en este cuadro se encogen hasta desaparecer (reaparecen al acercar la cámara)
    r_i = 46.0 * tam * 0.62
    oc = getattr(lz, "ocupado", None)
    if oc is not None:
        vis = 1.0
        for (ox, oy, orr) in oc:
            u = math.hypot(sx - ox, sy - oy) / (r_i + orr + 1e-6)
            vis = min(vis, float(smooth(np.clip((u - 0.80) / 0.40, 0.0, 1.0))))
        k *= vis
        if k <= 0.01:
            return
        oc.append((sx, sy, r_i * k))
    z = tam * 0.62 * k
    iso = I.Iso(0, 0, 0, z, sx0=sx, sy0=sy)
    with lz.capa(2):
        # baldosa flotante con sombra
        w = 62 if tipo != "ciudad" else 88
        lz.relleno(iso.pts([(-w / 2 + 5, -w / 2 + 6, -7), (w / 2 + 5, -w / 2 + 6, -7), (w / 2 + 5, w / 2 + 6, -7), (-w / 2 + 5, w / 2 + 6, -7)]), (10, 8, 40), alfa=0.30 * alfa)
        I.isla(lz, iso, -w / 2, -w / 2, w / 2, w / 2, color_top=(230, 206, 150), esp=8, c_tierra=(168, 118, 84), c_roca=(122, 96, 120), sombra=False, seed=semilla)
        m = I.Mundo()
        if tipo == "pueblo":
            A.iglesia(m, -8, -22, w=16, largo=26, h_nave=16, muro=A.CANTERA, techo=A.TEJA, torres=1, cupula_c=False)
            A.casa_colonial(m, -26, -2, 18, 14, 11, muro=A.CAL, eje="x", ventanas=1, puerta=False, seed=semilla)
            A.casa_colonial(m, 10, 2, 16, 14, 11, muro=A.OCRE, eje="x", ventanas=1, puerta=False, seed=semilla + 1)
        elif tipo == "ciudad":
            A.iglesia(m, -10, -34, w=22, largo=34, h_nave=22, muro=A.CANTERA, techo=A.TEJA, torres=2, cupula_c=True)
            for i, (cx, cy, ww, dd) in enumerate(((-38, -6, 22, 16), (-12, 6, 20, 14), (14, 8, 24, 14), (-36, 14, 16, 14), (26, -14, 14, 18))):
                A.casa_colonial(m, cx, cy, ww, dd, 12 + 3 * h01(semilla, i), muro=[A.CAL, A.OCRE, A.ROSA, A.AZUL][i % 4], eje="x", ventanas=1, puerta=False, seed=i)
        elif tipo == "fuerte":
            for (x0, y0, ww, dd) in ((-24, -24, 48, 6), (-24, 18, 48, 6), (-24, -24, 6, 48), (18, -24, 6, 48)):
                I.caja(lz, iso, x0, y0, ww, dd, 12, (214, 196, 178))
            I.caja(lz, iso, -6, -6, 12, 12, 16, (226, 208, 188))
        elif tipo == "puerto":
            A.casa_colonial(m, -22, -12, 22, 14, 11, muro=A.CAL, eje="x", ventanas=1, puerta=False, seed=2)
            A.casa_colonial(m, 4, -10, 18, 14, 11, muro=A.OCRE, eje="x", ventanas=1, puerta=False, seed=3)
            B.muelle(m, -20, 12, largo=40, ancho=7, h=3)
        m.dibujar(lz, iso)
        if bando is not None:
            col = INS if bando == "ins" else (REAL if bando == "real" else bando)
            bandera_mapa(lz, sx + 14 * z * 1.2, sy - 28 * z * 1.2, col, t, z * 1.2)
        if llama:
            O.fuego(lz, iso, 0, 0, 0.9 * z / 0.62, t, semilla, z=4, halo=True)
        if nombre:
            U.llamada(lz, sx, sy - 44 * z - 6, nombre, color=color_nombre, px=px, k=1.0, alfa=alfa)


def bandera_mapa(lz, x, y, color, t, s=1.0, franjas=None):
    k = s
    lz.relleno(rect_red(x - 1.0 * k, y - 22 * k, 2.0 * k, 24 * k, 0.5 * k), (110, 76, 60))
    cols = franjas or [(color, 1.0)]
    n = 8
    y0 = 0.0
    for col, fr in cols:
        up, dn = [], []
        for i in range(n + 1):
            u = i / n
            off = 1.6 * math.sin(t * 6.0 - u * 4.5) * u
            up.append((x + 1.0 * k + u * 16 * k, y - 22 * k + (13 * y0 + off) * k))
            dn.append((x + 1.0 * k + u * 16 * k, y - 22 * k + (13 * (y0 + fr) + off) * k))
        lz.relleno(np.array(up + dn[::-1]), col)
        y0 += fr


def etiqueta(lz, cam, lugar, texto, t, t0=0.0, px=28, color=U.COL["morado"], dy=-34, dx=0.0, lado="abajo", alfa=1.0):
    k = U.pop(t, t0)
    if k <= 0.01:
        return
    sx, sy = _scr_p(cam, lugar)
    if -200 < sx < W + 200 and -100 < sy < H + 100:
        U.llamada(lz, sx + dx, sy + dy, texto, color=color, px=px, k=k, cola=lado, alfa=alfa)


def _scr_p(cam, lugar):
    return _scr(cam, lugar)


# ------------------------------------------------------------------------------------------------ ondas, rutas y ejércitos
def onda(lz, cam, lugar, t, t0, dur=2.2, r_deg=4.0, color=(255, 236, 170), n=3, ancho=6.0, periodo=0.35, alfa=0.85):
    """Anillos que se expanden desde la ciudad a lo ancho del mapa (la campana que se oye en todo el país)."""
    sx, sy = _scr(cam, lugar)
    R = r_deg * KM.K * cam[2]
    for k_ in range(n):
        u = prog(t - k_ * periodo, t0, t0 + dur)
        if 0 < u < 1:
            rr = R * (1 - (1 - u) ** 2)
            th = np.linspace(0, 2 * math.pi, 96)
            lz.trazo(np.stack([sx + rr * np.cos(th), sy + rr * np.sin(th)], 1), (*color[:3], int(255 * alfa * (1 - u) ** 1.3)), ancho * (1 - 0.55 * u) * max(0.6, cam[2] ** 0.3), cerrado=True, afinar=False, temblor=0.0, capa=2)
            lz.relleno(np.stack([sx + rr * np.cos(th), sy + rr * np.sin(th)], 1), color, alfa=0.05 * (1 - u) * alfa, capa=2)


def ruta(lz, cam, pts, color=(255, 214, 84), frac=1.0, t=0.0, ancho=7.0, flecha=True, curv=0.0, retorna=False, punta=True):
    """Línea discontinua con flujo desde el primer punto hasta `frac` del recorrido, con punta de flecha. pts = [(lon, lat) | nombre, ...]. Devuelve el punto de pantalla de la cabeza."""
    if frac <= 0.002:
        return None
    ll = [CIUDADES[p] if isinstance(p, str) else p for p in pts]
    x, y = M.proy(cam, np.array([p[0] for p in ll]), np.array([p[1] for p in ll]))
    q = np.stack([x, y], 1)
    if len(q) == 2:
        c = (q[0] + q[1]) / 2 + np.array([-(q[1][1] - q[0][1]), q[1][0] - q[0][0]]) * curv
        from motor import bezier
        q = np.array(bezier(tuple(q[0]), tuple(c), tuple(c), tuple(q[1]), 48), float)
    elif len(q) > 2:
        q = np.array(catmull(q, 10), float)
    z = max(0.5, cam[2] ** 0.35)
    P.discontinua(lz, q, color, ancho=ancho * z, largo=30 * z, hueco=20 * z, fase=-t * 55 * z, frac=frac, capa=2)
    seg = np.hypot(*np.diff(q, axis=0).T)
    d = np.r_[0, np.cumsum(seg)]
    s = d[-1] * min(1.0, frac)
    i = int(np.clip(np.searchsorted(d, s, side="right") - 1, 0, len(q) - 2))
    f = (s - d[i]) / max(d[i + 1] - d[i], 1e-6)
    cab = q[i] + (q[i + 1] - q[i]) * f
    if flecha and punta and frac < 0.999 or (flecha and punta and frac >= 0.999):
        v = (q[min(i + 1, len(q) - 1)] - q[i])
        v = v / max(np.hypot(*v), 1e-6)
        nn = np.array([-v[1], v[0]])
        L = 20 * z
        lz.relleno(np.array([cab + v * L, cab - v * L * 0.5 + nn * L * 0.65, cab - v * L * 0.5 - nn * L * 0.65]), color, capa=2)
    return float(cab[0]), float(cab[1])


def punto_ruta(cam, pts, u):
    """Punto de pantalla a la fracción u de la ruta (misma interpolación que `ruta`)."""
    ll = [CIUDADES[p] if isinstance(p, str) else p for p in pts]
    x, y = M.proy(cam, np.array([p[0] for p in ll]), np.array([p[1] for p in ll]))
    q = np.stack([x, y], 1)
    if len(q) > 2:
        q = np.array(catmull(q, 10), float)
    seg = np.hypot(*np.diff(q, axis=0).T)
    d = np.r_[0, np.cumsum(seg)]
    s = d[-1] * min(max(u, 0.0), 1.0)
    i = int(np.clip(np.searchsorted(d, s, side="right") - 1, 0, len(q) - 2))
    f = (s - d[i]) / max(d[i + 1] - d[i], 1e-6)
    p = q[i] + (q[i + 1] - q[i]) * f
    v = q[i + 1] - q[i]
    v = v / max(np.hypot(*v), 1e-6)
    return float(p[0]), float(p[1]), v


def ejercito(lz, x, y, n, bando="ins", t=0.0, s=1.0, dir=1, marcha=True, bandera=True, semilla=0, polvo=True, estandarte=None):
    """Grupo de n soldaditos planos en marcha (con desfase propio), bandera y nube de polvo, de ~26 px de alto a s=1."""
    col = INS if bando == "ins" else (REAL if bando == "real" else bando)
    k = s
    if polvo:
        for i in range(5):
            u = (t * 0.8 + i / 5) % 1.0
            lz.relleno(circulo(x - dir * (6 + 26 * u) * k, y + 2 * k - 3 * u * k, (4 + 8 * u) * k, 10), (236, 226, 206), alfa=0.5 * (1 - u), capa=2)
    cuad = min(n, 12)
    for i in range(cuad):
        fx = (i % 4) * 9 - 13
        fy = (i // 4) * 5 - 5
        ph = t * 8 + h01(semilla, i) * 6.28
        bob = abs(math.sin(ph)) * 1.4 * k if marcha else 0
        px, py = x + (fx * dir) * k, y + fy * k - bob
        lz.relleno(elipse(px, py + 1.0 * k, 4.4 * k, 1.6 * k, 0, 10), (30, 24, 70), alfa=0.25, capa=2)
        sw = math.sin(ph) * 2.2 * k if marcha else 0
        lz.relleno(rect_red(px - 2.2 * k + sw, py - 6 * k, 1.6 * k, 6 * k, 0.5 * k), (60, 50, 70), capa=2)
        lz.relleno(rect_red(px + 0.6 * k - sw, py - 6 * k, 1.6 * k, 6 * k, 0.5 * k), (60, 50, 70), capa=2)
        lz.relleno(rect_red(px - 3 * k, py - 14 * k, 6 * k, 8.4 * k, 2 * k), col, capa=2)
        lz.relleno(circulo(px, py - 17.4 * k, 3.0 * k, 10), (228, 176, 128), capa=2)
        lz.relleno(elipse(px, py - 19.2 * k, 4.8 * k, 1.3 * k, 0, 10), (236, 198, 120) if bando == "ins" else (40, 44, 100), capa=2)
        if bando != "ins" or i % 3 == 0:
            lz.relleno(rect_red(px + 3.6 * k * dir, py - 20 * k, 1.0 * k, 14 * k, 0.3 * k), (96, 70, 52), capa=2)
    if bandera:
        bandera_mapa(lz, x + (cuad > 8) * 0 + 14 * k * dir, y - 4 * k, col, t, 1.1 * k, franjas=estandarte)


def montes(lz, cam, min_alt=None, alfa=1.0, t=0.0):
    """Montañas y volcanes dibujados como iconos con 3 tonos sobre las cumbres reales del relieve (picos de ETOPO), con nieve en los volcanes."""
    M._cargar()
    z = cam[2]
    if min_alt is None:
        min_alt = 3500 if z < 0.7 else (2900 if z < 1.5 else 2300)
    p = M.picos()
    sel = p[p[:, 2] >= min_alt]
    x, y = M.proy(cam, sel[:, 0], sel[:, 1])
    ok = (x > -60) & (x < W + 60) & (y > -80) & (y < H + 60)
    x, y, alt = x[ok], y[ok], sel[ok, 2]
    celdas = set()
    sp = 46 if z < 1.5 else 54
    for xi, yi, ai in zip(x, y, alt):
        key = (int(xi // sp), int(yi // (sp * 0.8)))
        if key in celdas:
            continue
        celdas.add(key)
        s = (0.55 + 0.9 * min(1.0, (ai - 2000) / 3400.0)) * max(0.7, min(2.2, z ** 0.45)) * 26
        _monte(lz, xi, yi, s, ai, alfa)


def _monte(lz, x, y, s, alt, alfa=1.0):
    base = (184, 130, 112) if alt < 4200 else (170, 150, 168)
    h = s * 1.05
    lz.relleno(elipse(x + s * 0.2, y + 1, s * 1.05, s * 0.28, 0, 14), (30, 24, 70), alfa=0.22 * alfa, capa=2)
    lz.relleno(np.array([[x - s, y], [x, y - h], [x + s, y]]), P.oscurecer(base, 0.3), alfa=alfa, capa=2)
    lz.relleno(np.array([[x - s, y], [x, y - h], [x + s * 0.05, y]]), base, alfa=alfa, capa=2)
    lz.relleno(np.array([[x - s * 0.55, y - h * 0.48], [x, y - h], [x + s * 0.05, y - h * 0.40], [x - s * 0.20, y - h * 0.30]]), P.aclarar(base, 0.2), alfa=alfa, capa=2)
    if alt > 3900:
        lz.relleno(np.array([[x - s * 0.34, y - h * 0.68], [x, y - h], [x + s * 0.34, y - h * 0.68], [x + s * 0.12, y - h * 0.58], [x - s * 0.02, y - h * 0.72], [x - s * 0.18, y - h * 0.58]]), (250, 250, 255), alfa=alfa, capa=2)


# ------------------------------------------------------------------------------------------------ rótulos y decoración
def region(lz, cam, texto, lonlat, px=30, rot=0.0, alfa=0.75, color=(255, 255, 255), espacio=0.18, z_min=0.0, z_max=99.0):
    """Nombre de región/mar con letras espaciadas, semitransparente (SIERRA MADRE OCCIDENTAL, GOLFO DE MÉXICO…)."""
    if not (z_min <= cam[2] <= z_max):
        return
    x, y = M.proy(cam, lonlat[0], lonlat[1])
    p = px * max(0.7, min(1.5, cam[2] ** 0.25))
    letras = list(texto)
    anchos = [ancho_texto(c, "geo", int(p)) + p * espacio for c in letras]
    tot = sum(anchos)
    c, s_ = math.cos(rot), math.sin(rot)
    cur = -tot / 2
    for ch, a in zip(letras, anchos):
        if ch != " ":
            cx = cur + a / 2
            lz.texto(ch, x + cx * c, y + cx * s_, int(p), "geo", color=color, borde=None, alfa=alfa, rot=rot, temblor=0.0, capa=2)
        cur += a


def brujula(lz, x, y, s=1.0, alfa=0.9):
    k = s
    lz.relleno(circulo(x, y, 34 * k, 28), (255, 255, 255), alfa=0.16 * alfa, capa=2)
    for ang, col in ((-math.pi / 2, (250, 190, 40)), (math.pi / 2, (255, 255, 255)), (0, (255, 255, 255)), (math.pi, (255, 255, 255))):
        L = 30 * k if col != (250, 190, 40) else 36 * k
        lz.relleno(np.array([[x + math.cos(ang) * L, y + math.sin(ang) * L], [x + math.cos(ang + 1.57) * 6 * k, y + math.sin(ang + 1.57) * 6 * k], [x, y], [x + math.cos(ang - 1.57) * 6 * k, y + math.sin(ang - 1.57) * 6 * k]]),
                   col, alfa=alfa, capa=2)
    lz.texto("N", x, y - 48 * k, int(22 * k), "geo", color=(255, 255, 255), borde=None, alfa=alfa, temblor=0.0, capa=2)


def escala(lz, x, y, cam, km=200, alfa=0.9):
    """Barra de escala (km) según el zoom: 1° de latitud = 111 km = K*z px."""
    px = km / 111.0 * KM.K * cam[2]
    lz.relleno(rect_red(x, y, px, 5, 2), (255, 255, 255), alfa=alfa, capa=2)
    lz.texto(f"{km} km", x + px / 2, y - 18, 22, "geo", color=(255, 255, 255), borde=None, alfa=alfa, temblor=0.0, capa=2)


def cuadricula_geo(lz, cam, paso=5, alfa=0.14):
    """Meridianos y paralelos tenues con su etiqueta en el borde."""
    lo, la, z = cam
    x0, y0 = M.inv(cam, 0, 0)
    x1, y1 = M.inv(cam, W, H)
    lons = np.arange(math.floor(x0 / paso) * paso, x1 + paso, paso)
    lats = np.arange(math.floor(y1 / paso) * paso, y0 + paso, paso)
    for lon in lons:
        xs, _ = M.proy(cam, lon, la)
        lz.relleno(rect_red(xs - 0.8, 0, 1.6, H, 0.3), (255, 255, 255), alfa=alfa, capa=2)
        lz.texto(f"{abs(int(lon))}°{'O' if lon < 0 else 'E'}", xs + 4, H - 18, 17, "geo", color=(255, 255, 255), borde=None, alfa=0.5, temblor=0.0, capa=2, ancla=(0.0, 0.5))
    for lat in lats:
        _, ys = M.proy(cam, lo, lat)
        lz.relleno(rect_red(0, ys - 0.8, W, 1.6, 0.3), (255, 255, 255), alfa=alfa, capa=2)
        lz.texto(f"{int(lat)}°N", 10, ys - 12, 17, "geo", color=(255, 255, 255), borde=None, alfa=0.5, temblor=0.0, capa=2, ancla=(0.0, 0.5))


def insignia_batalla(lz, cam, lugar, t, t0, año=None, s=1.0, color=(226, 70, 70)):
    """Espadas cruzadas en un disco rojo (batalla) con el año en una cápsula."""
    k = U.pop(t, t0)
    if k <= 0.01:
        return
    sx, sy = _scr(cam, lugar)
    with lz.capa(2):
        with lz.grupo(sx, sy, k * s):
            lz.relleno(circulo(3, 5, 26, 24), (10, 6, 40), alfa=0.25)
            lz.relleno(circulo(0, 0, 26, 24), color)
            lz.relleno(circulo(0, 0, 21, 24), P.oscurecer(color, 0.18))
            for sg in (-1, 1):
                lz.relleno(np.array([[sg * 17, -17], [sg * 20, -14], [-sg * 14, 17], [-sg * 17, 14]]), (250, 250, 252))
                lz.relleno(np.array([[-sg * 17, -17], [-sg * 14, -20], [sg * 17, 14], [sg * 14, 17]]), (214, 220, 232))
            lz.relleno(circulo(0, 0, 4, 10), (250, 190, 40))
        if año:
            U.llamada(lz, sx, sy - 34 * k * s, str(año), color=U.COL["oscuro"], px=24, k=k, cola="abajo")


def pais(lz, cam, nombre, color, alfa=0.35, borde=None, ancho=4.0, t=0.0, latido=0.0):
    """Rellena (y perfila) los polígonos de un país de Natural Earth sobre el mapa."""
    M._cargar()
    for p in M.paises.get(nombre, []):
        q = M._poly_px(cam, p)
        if q[:, 0].max() < -50 or q[:, 0].min() > W + 50 or q[:, 1].max() < -50 or q[:, 1].min() > H + 50:
            continue
        lz.relleno(q, color, alfa=alfa, capa=2)
        if borde is not None:
            lz.trazo(q, (*borde[:3], 255), ancho * (1 + latido * 0.25 * math.sin(t * 5)), cerrado=True, afinar=False, temblor=0.0, capa=2, paso=3.0)


def barco_plano(lz, x, y, s=1.0, t=0.0, dir=1, vela=(250, 244, 230), casco=(120, 80, 60), alfa=1.0):
    """Galeón de vela en pantalla (para el mapa): casco, dos mástiles, velas hinchadas, cabeceo."""
    k = s
    bob = 2.2 * math.sin(t * 2.0) * k
    y = y + bob
    lz.relleno(elipse(x, y + 4 * k, 30 * k, 6 * k, 0, 16), (10, 30, 90), alfa=0.30 * alfa, capa=2)
    lz.relleno(np.array([(-26, -10), (26, -10), (22, 2), (-18, 4), (-30, -4)], float) * [dir, 1] * k + [x, y], P.oscurecer(casco, 0.2), alfa=alfa, capa=2)
    lz.relleno(np.array([(-26, -10), (26, -10), (24, -6), (-26, -6)], float) * [dir, 1] * k + [x, y], casco, alfa=alfa, capa=2)
    for mx, hh in ((-6, 44), (12, 38)):
        lz.relleno(rect_red((x + (mx - 0.8) * dir * k), y - (10 + hh) * k, 1.6 * k, hh * k, 0.4 * k), (100, 70, 56), alfa=alfa, capa=2)
        vw = 15 * (0.9 + 0.1 * math.sin(t * 2 + mx))
        lz.relleno(np.array([(mx - vw * 0.5, -(10 + hh) + 3), (mx + vw * 0.7, -(10 + hh) + 3), (mx + vw * 0.45, -(10 + hh * 0.35)), (mx - vw * 0.4, -(10 + hh * 0.35))], float) * [dir, 1] * k + [x, y], vela, alfa=alfa, capa=2)
        lz.relleno(np.array([(mx - vw * 0.5, -(10 + hh) + 3), (mx + vw * 0.2, -(10 + hh) + 3), (mx + vw * 0.1, -(10 + hh * 0.35)), (mx - vw * 0.4, -(10 + hh * 0.35))], float) * [dir, 1] * k + [x, y], P.oscurecer(vela, 0.16), alfa=alfa, capa=2)
    lz.relleno(np.array([(12, -50), (22, -48), (12, -44)], float) * [dir, 1] * k + [x, y], (206, 66, 66), alfa=alfa, capa=2)


def corona(lz, x, y, s=1.0, alfa=1.0, t=0.0):
    k = s
    lz.relleno(np.array([(-18, 0), (-20, -22), (-9, -10), (0, -26), (9, -10), (20, -22), (18, 0)], float) * k + [x, y], (250, 206, 70), alfa=alfa, capa=2)
    lz.relleno(np.array([(-18, 0), (18, 0), (18, 6), (-18, 6)], float) * k + [x, y], (226, 160, 40), alfa=alfa, capa=2)
    for dx, col in ((-9, (214, 52, 70)), (0, (60, 150, 230)), (9, (214, 52, 70))):
        lz.relleno(circulo(x + dx * k, y + 3 * k, 2.4 * k, 8), col, alfa=alfa, capa=2)
    lz.halo(x, y - 10 * k, 40 * k, (255, 226, 130), alfa=0.35 * alfa * (0.8 + 0.2 * math.sin(t * 4)), capa=2)


# ------------------------------------------------------------------------------------------------ vida en el mar
def _delfin(lz, x, y, s, ang, alfa=1.0, ballena=False):
    """Delfín/ballena de perfil saltando (cuerpo en arco, vientre claro, aleta dorsal y cola), centrado en (x, y) con inclinación `ang`."""
    c, sn = math.cos(ang), math.sin(ang)

    def R(pts):
        a = np.asarray(pts, float) * s
        return np.stack([x + a[:, 0] * c - a[:, 1] * sn, y + a[:, 0] * sn + a[:, 1] * c], 1)

    cuerpo = (70, 100, 150) if not ballena else (52, 70, 118)
    vientre = (206, 220, 238)
    lz.relleno(R([(-22, 2), (-12, -6), (6, -7), (20, -3), (27, 1), (20, 4), (4, 7), (-12, 6)]), cuerpo, alfa=alfa, capa=2)
    lz.relleno(R([(-10, 3), (6, 2), (20, 3), (22, 2), (20, 4), (4, 7), (-12, 6)]), vientre, alfa=alfa, capa=2)
    lz.relleno(R([(-22, 2), (-30, -7), (-26, 1), (-31, 8)]), cuerpo, alfa=alfa, capa=2)
    lz.relleno(R([(-2, -6), (4, -14), (8, -6)]), P.oscurecer(cuerpo, 0.2), alfa=alfa, capa=2)
    lz.relleno(circulo(x + (18 * c - -1 * sn) * s, y + (18 * sn + -1 * c) * s, 0.9 * s, 6), (255, 255, 255), alfa=alfa, capa=2)


def _niveles(ppg, objetivo_px):
    """Niveles de rejilla (celdas de 2**n grados) vecinos al tamaño de celda deseado en pantalla, con su peso de fundido: [(nivel, peso), ...]."""
    n = math.log2(objetivo_px / ppg)
    n0 = math.floor(n)
    f = n - n0
    return [(n0, 1.0 - f), (n0 + 1, f)]


def _celdas(cam, paso):
    x0, y0 = M.inv(cam, 0, 0)
    x1, y1 = M.inv(cam, W, H)
    lon_a, lon_b = min(x0, x1) - paso, max(x0, x1) + paso
    lat_a, lat_b = min(y0, y1) - paso, max(y0, y1) + paso
    if (lon_b - lon_a) / paso * (lat_b - lat_a) / paso > 9000:
        return [], []
    return np.arange(math.floor(lon_a / paso), math.ceil(lon_b / paso)), np.arange(math.floor(lat_a / paso), math.ceil(lat_b / paso))


def _cresta(lz, x, y, L, ancho, color, alfa):
    """Cresta de ola: arco fino como POLÍGONO con alfa real (los trazos con alfa se pintan como suma de luz y siempre salían blancos opacos: no se podían fundir)."""
    if alfa < 0.02:
        return
    u = np.linspace(0, 1, 7)
    cx = x + L * (u - 0.5) * 2
    cy = y - 0.35 * L * np.sin(math.pi * u)
    dx, dy = np.gradient(cx), np.gradient(cy)
    n = np.hypot(dx, dy) + 1e-9
    nx, ny = -dy / n * ancho * 0.5, dx / n * ancho * 0.5
    grosor = np.sin(math.pi * np.clip(u, 0.02, 0.98)) ** 0.6 + 0.25
    arriba = np.stack([cx + nx * grosor, cy + ny * grosor], 1)
    abajo = np.stack([cx - nx * grosor, cy - ny * grosor], 1)[::-1]
    lz.relleno(np.vstack([arriba, abajo]), color, alfa=alfa, capa=2, temblor=0.0)


def mar_vivo(lz, cam, t, seed=1, densidad=1.0, fauna=True, barcos=True, color=(255, 255, 255)):
    """Vida sobre el MAR del mapa (solo donde no hay tierra): crestas de ola que respiran, delfines y ballenas que saltan con salpicadura y barcos lejanos que navegan.
    Todo está ANCLADO A LA GEOGRAFÍA con celdas de lon/lat de tamaño fijo por NIVEL (potencias de 2): al hacer zoom los niveles se funden uno en otro (nunca se
    redimensiona la rejilla), así ninguna cresta resbala sobre el mapa ni «salta» y no hay efecto de paralaje con el agua."""
    M._cargar()
    lo, la, z = cam
    ppg = KM.K * z
    k = max(0.5, min(2.4, z ** 0.35)) * 12
    # ---- crestas: rejilla fina
    for lvl, peso in _niveles(ppg * max(0.3, densidad), 56.0):
        if peso < 0.03:
            continue
        paso = 2.0 ** lvl
        sd = seed + 1000 * (lvl + 8)
        cs, fs = _celdas(cam, paso)
        for i in cs:
            ii = int(i) & 0x7fffffff
            for j in fs:
                jj = int(j) & 0x7fffffff
                hh = h01(ii, jj, sd)
                if hh > 0.34:
                    continue
                lon = (i + h01(ii, jj, sd + 5)) * paso
                lat = (j + h01(ii, jj, sd + 7)) * paso
                if M.es_tierra(lon, lat):
                    continue
                sx, sy = M.proy(cam, lon, lat)
                if sx < -40 or sx > W + 40 or sy < -40 or sy > H + 40:
                    continue
                al = (0.50 + 0.30 * (0.5 + 0.5 * math.sin(t * 1.6 + hh * 40.0))) * peso
                L = k * (0.9 + 0.8 * h01(ii, jj, sd + 23))
                _cresta(lz, float(sx), float(sy), L, max(1.3, 1.8 * z ** 0.3), color, al)
    if not (fauna or barcos) or z <= 0.18:
        return
    # ---- fauna y barcos: rejilla gruesa (≈ una cosa cada 230 px) con su propio fundido entre niveles
    for lvl, peso in _niveles(ppg, 230.0):
        if peso < 0.03:
            continue
        paso = 2.0 ** lvl
        sd = seed + 1000 * (lvl + 8) + 500
        cs, fs = _celdas(cam, paso)
        for i in cs:
            ii = int(i) & 0x7fffffff
            for j in fs:
                jj = int(j) & 0x7fffffff
                r = h01(ii, jj, sd + 11)
                es_delfin = fauna and r < 0.14
                es_barco = barcos and (not es_delfin) and r < 0.14 + 0.26
                if not (es_delfin or es_barco):
                    continue
                lon = (i + 0.15 + 0.7 * h01(ii, jj, sd + 5)) * paso
                lat = (j + 0.15 + 0.7 * h01(ii, jj, sd + 7)) * paso
                if M.es_tierra(lon, lat):
                    continue
                sx, sy = M.proy(cam, lon, lat)
                if sx < -60 or sx > W + 60 or sy < -60 or sy > H + 60:
                    continue
                if es_delfin:                                      # ballena o delfín que salta (ciclo de ~6 s)
                    per = 5.5 + 3 * h01(ii, jj, sd + 13)
                    u = ((t + 10 * h01(ii, jj, sd + 17)) % per) / per
                    if u < 0.22:
                        v = u / 0.22
                        ar = math.sin(math.pi * v)
                        dx = (v - 0.5) * 6 * k
                        dy = -ar * 5.0 * k
                        ang = (v - 0.5) * 2.2
                        _delfin(lz, float(sx) + dx, float(sy) + dy, 0.9 * k / 12 * 2.2, ang, alfa=peso, ballena=(h01(ii, jj, sd + 19) > 0.6))
                        if 0.0 < v < 0.18 or 0.82 < v < 1.0:
                            for g in range(7):
                                lz.relleno(circulo(float(sx) + dx * 0.4 + 11 * k / 12 * g * (1 if v < 0.5 else -1) * 0.5, float(sy) - 10 * k / 12 - 14 * k / 12 * abs(math.sin(g)), 1.6 * k / 12 * 2, 6), color, alfa=0.7 * peso, capa=2)
                else:                                              # barco lejano que navega (deriva lenta, siempre sobre el mismo mar)
                    d = 1 if h01(ii, jj, sd + 31) > 0.5 else -1
                    bx = float(sx) + 16 * z * math.sin(t * 0.05 + h01(ii, jj, sd + 29) * 6.28)
                    barco_plano(lz, bx, float(sy), 0.35 * max(0.8, z ** 0.3), t, dir=d, alfa=0.9 * peso)


def medallon(lz, x, y, r, quien, t, emocion="neutro", borde=(250, 206, 90), fondo=(60, 40, 110), alfa=1.0, seed=0, habla=0.0, k=1.0):
    """Retrato en círculo con borde dorado (para mapas): se recorta el retrato al disco."""
    import kz_retrato as RT
    import kz_retrato_real as RR
    if k <= 0.01:
        return
    if RR.hay(quien):                       # personaje histórico real: retrato de época en medallón dorado
        return RR.medallon(lz, x, y, r + 7, quien, t, emocion, borde, fondo, alfa, seed, habla, k)
    th = np.linspace(0, 2 * math.pi, 64)
    disco = np.stack([x + r * k * np.cos(th), y + r * k * np.sin(th)], 1)
    lz.relleno(circulo(x + 4, y + 6, r * k + 4, 36), (10, 6, 40), alfa=0.28 * alfa, capa=2)
    lz.relleno(circulo(x, y, r * k + 7, 36), borde, alfa=alfa, capa=2)
    lz.relleno(disco, fondo, alfa=alfa, capa=2)
    with lz.capa(2):
        with lz.recorte(disco):
            RT.retrato(lz, x, y + r * k * 0.95, r * k * 0.55, quien, t, emocion=emocion, habla=habla, alfa=alfa, seed=seed, luz_borde=None)


def montes_lista(lz, cam, picos, alfa=1.0):
    """Montañas en posiciones dadas [(lon, lat, altitud_m), ...] (para zonas sin datos de relieve: Pirineos, Alpes…)."""
    z = cam[2]
    for (lon, lat, alt) in picos:
        x, y = M.proy(cam, lon, lat)
        if -60 < x < W + 60 and -80 < y < H + 60:
            s = (0.55 + 0.9 * min(1.0, (alt - 2000) / 3400.0)) * max(0.7, min(2.2, z ** 0.45)) * 26
            _monte(lz, float(x), float(y), s, alt, alfa)


def pueblo(lz, cam, lugar, nombre, t, t0=0.0, color=(255, 255, 255), px=24, solo_desde=1.2):
    """Punto de población con anillo y nombre pequeño (para dar densidad geográfica sin tapar el mapa). Solo se dibuja con el zoom alto."""
    k = U.pop(t, t0)
    if k <= 0.01 or cam[2] < solo_desde:
        return
    lo, la = CIUDADES[lugar] if isinstance(lugar, str) else lugar
    x, y = M.proy(cam, lo, la)
    if x < -60 or x > W + 60 or y < -40 or y > H + 40:
        return
    with lz.capa(2):
        lz.relleno(circulo(float(x), float(y), 9 * k, 14), (20, 14, 60), alfa=0.35)
        lz.relleno(circulo(float(x), float(y), 7 * k, 14), color)
        lz.relleno(circulo(float(x), float(y), 3.4 * k, 10), (214, 70, 76))
        P.rotulo(lz, float(x), float(y) + 22 * k, nombre, px=int(px * k), k=1.0, color=(255, 255, 255), sombra=0.7, alfa=min(1.0, k))
