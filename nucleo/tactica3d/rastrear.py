# -*- coding: utf-8 -*-
"""Rastreador del MINIMAPA de una transmisión de LoL Esports (28-oct-2026): la ruta de CADA jugador en una jugada.

Antes las rutas de nucleo/tactica3d se medían a mano en hojas con rejilla (videos/lol_worlds_2026/j6_3d.py). Esto las saca
solo, cada `paso` s:
1. recorta el minimapa (1640,800 de 276 px en 1920×1080: el mismo encuadre u, v que usa la escena 3D);
2. DETECTA los iconos de campeón como círculos (HoughCircles sobre el minimapa ×3: en la prueba halló los 10 exactos;
   buscar el arte de Data Dragon por todo el mapa NO sirve, da saltos por todas partes);
3. en el primer cuadro reparte los círculos entre los 10 campeones (Hungarian con el icono de Data Dragon) — o a mano con
   --inicio Nombre=x,y (px del minimapa) cuando la hoja «inicio» muestra algún error;
4. los SIGUE: cada jugador se queda con el círculo cercano que más se parece a SU propio icono en el video (plantilla que se
   actualiza), con salto lejano solo si el parecido es muy claro (Destello, TP, regreso a base). Sin círculo = None (muerto
   o tapado por otro icono): la escena 3D lo salta.
Revisar SIEMPRE las hojas (inicio con nombres + rastros en 6 momentos) y corregir a mano lo raro en el .py de la escena.

uso:
  python nucleo/tactica3d/rastrear.py <clip.mp4> <t0> <t1> --iconos <dir> --jug Wei:Nocturne:A Rookie:Annie:A ... \
         [--paso .25] [--reloj N] [--inicio Wei=59,132 ...] [--salida pistas.json] [--hoja hoja.jpg]
  --reloj N  → segundo de juego = t del clip + N (cada punto lleva [t, u, v, parecido, g])
"""
import argparse
import json
import os

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment

X0, Y0, LADO = 1640, 800, 276          # minimapa de la transmisión (1920×1080)
ESC = 3                                 # el minimapa se amplía ×3 para detectar
COLOR = {"A": (255, 170, 60), "R": (60, 60, 255)}
S = 40
_MASK = np.zeros((S, S), np.uint8)
cv2.circle(_MASK, (S // 2, S // 2), int(S * .40), 255, -1)


def _feat(img):
    lab = cv2.cvtColor(cv2.resize(img, (S, S), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2LAB).astype(np.float32)
    v = lab[_MASK > 0]
    v = (v - v.mean(0)) / (v.std(0) + 1e-3)
    return v.ravel() / np.sqrt(v.size)


def sim(a, b):
    return float(np.dot(a, b))


def plantillas_dd(ruta):
    """icono cuadrado de Data Dragon con varios recortes (el minimapa acerca un poco el arte)"""
    t = cv2.imread(ruta)
    h = t.shape[0]
    return [_feat(t[int(h * c):h - int(h * c), int(h * c):h - int(h * c)]) for c in (.06, .12, .18, .24)]


def leer(cap, t):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        return None
    if f.shape[1] != 1920:
        f = cv2.resize(f, (1920, 1080))
    return f[Y0:Y0 + LADO, X0:X0 + LADO]


def detectar(mini, param2=19):
    """círculos de icono → [(x, y, feat)] en px del minimapa"""
    big = cv2.resize(mini, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_CUBIC)
    g = cv2.GaussianBlur(cv2.cvtColor(big, cv2.COLOR_BGR2GRAY), (5, 5), 1.5)
    c = cv2.HoughCircles(g, cv2.HOUGH_GRADIENT, dp=1, minDist=22, param1=90, param2=param2, minRadius=27, maxRadius=40)
    out = []
    for x, y, r in (c[0] if c is not None else []):
        rr = int(r * .82)
        y0, y1, x0, x1 = int(y) - rr, int(y) + rr, int(x) - rr, int(x) + rr
        if y0 < 0 or x0 < 0 or y1 > big.shape[0] or x1 > big.shape[1]:
            continue
        out.append((x / ESC, y / ESC, _feat(big[y0:y1, x0:x1]), big[y0:y1, x0:x1].copy(), _aro(big, x, y, r)))
    return out


def _aro(big, x, y, r):
    """equipo por el color del aro del icono: 'A' (azul), 'R' (rojo) o None si no está claro"""
    hsv = cv2.cvtColor(big[max(0, int(y - r - 4)):int(y + r + 5), max(0, int(x - r - 4)):int(x + r + 5)], cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot(xx - (x - max(0, int(x - r - 4))), yy - (y - max(0, int(y - r - 4))))
    m = (d > r * .82) & (d < r * 1.08) & (hsv[..., 1] > 90) & (hsv[..., 2] > 90)
    hue = hsv[..., 0][m]
    if hue.size < 20:
        return None
    az = ((hue > 92) & (hue < 118)).mean()
    ro = ((hue < 10) | (hue > 165)).mean()
    return "A" if az > ro + .15 else "R" if ro > az + .15 else None


def local(mini, parche, pos, radio):
    """busca el parche propio del jugador (su icono en un cuadro anterior) cerca de pos → (x, y, ncc)"""
    big = cv2.resize(mini, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_CUBIC)
    h, w = parche.shape[:2]
    cx, cy = pos[0] * ESC, pos[1] * ESC
    r = radio * ESC
    x0, y0 = int(max(0, cx - r - w / 2)), int(max(0, cy - r - h / 2))
    x1, y1 = int(min(big.shape[1], cx + r + w / 2)), int(min(big.shape[0], cy + r + h / 2))
    zona = big[y0:y1, x0:x1]
    if zona.shape[0] < h or zona.shape[1] < w:
        return None
    m = cv2.matchTemplate(zona, parche, cv2.TM_CCOEFF_NORMED)
    _, v, _, (lx, ly) = cv2.minMaxLoc(m)
    return ((x0 + lx + w / 2) / ESC, (y0 + ly + h / 2) / ESC, float(v))


def rastrear(clip, t0, t1, jugadores, iconos, paso=.25, inicio=None, gate=9.0, salto=.55):
    cap = cv2.VideoCapture(clip)
    ts = [round(float(t), 3) for t in np.arange(t0, t1 + 1e-6, paso)]
    cuadros = [leer(cap, t) for t in ts]
    dets = [detectar(m) if m is not None else [] for m in cuadros]
    # círculos FIJOS (torres, iconos del mapa): se parecen a la MEDIANA de todos los cuadros (el fondo sin jugadores)
    validos = [m for m in cuadros if m is not None]
    fondo = np.median(np.stack(validos[::max(1, len(validos) // 40)]), axis=0).astype(np.uint8)
    fbig = cv2.resize(fondo, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_CUBIC)

    def _fijo(d):
        x, y, pc = d[0] * ESC, d[1] * ESC, d[3]
        h, w = pc.shape[:2]
        z = fbig[int(y - h / 2):int(y - h / 2) + h, int(x - w / 2):int(x - w / 2) + w]
        if z.shape[:2] != (h, w):
            return False
        return cv2.matchTemplate(z, pc, cv2.TM_CCOEFF_NORMED)[0, 0] > .6
    dets = [[d for d in ds if not _fijo(d)] for ds in dets]
    n = len(jugadores)
    dd = [plantillas_dd(os.path.join(iconos, c + ".png")) for _, c, _ in jugadores]
    # ── inicio: reparto con Data Dragon (o a mano)
    pos, ref, par = [None] * n, [None] * n, [None] * n
    d0 = dets[0]
    if d0:
        cost = np.array([[(1 - max(sim(f, t) for t in dd[i])) + (5 if eq and eq != jugadores[i][2] else 0)
                          for (_, _, f, _, eq) in d0] for i in range(n)])
        ri, ci = linear_sum_assignment(cost)
        for i, j in zip(ri, ci):
            pos[i], ref[i], par[i] = d0[j][:2], d0[j][2], d0[j][3]
    for nom, (x, y) in (inicio or {}).items():
        i = [j[0] for j in jugadores].index(nom)
        k = int(np.argmin([np.hypot(dx - x, dy - y) for dx, dy, *_ in d0]))
        pos[i], ref[i], par[i] = d0[k][:2], d0[k][2], d0[k][3]
    pistas = [[] for _ in range(n)]
    for k, (t, ds) in enumerate(zip(ts, dets)):
        if k == 0:
            for i in range(n):
                pistas[i].append([t, *(np.round(np.array(pos[i]) / LADO, 4).tolist() if pos[i] else [None, None]), 1.0])
            continue
        big = 1e3
        cost = np.full((n, max(len(ds), 1)), big)
        for i in range(n):
            for j, (x, y, f, _, eq) in enumerate(ds):
                if eq and eq != jugadores[i][2]:
                    continue
                s = max(sim(f, ref[i]) if ref[i] is not None else -1, max(sim(f, t_) for t_ in dd[i]) * .8)
                if pos[i] is None:
                    cost[i, j] = (1 - s) if s > salto else big
                    continue
                dist = np.hypot(x - pos[i][0], y - pos[i][1])
                if dist <= gate * paso / .25 + 3:
                    cost[i, j] = .5 * dist / gate + (1 - s)
                elif s > salto:
                    cost[i, j] = 1.2 + (1 - s)      # salto lejano: solo si nadie cercano lo explica mejor
        ri, ci = linear_sum_assignment(cost) if ds else ([], [])
        hecho = set()
        for i, j in zip(ri, ci):
            if cost[i, j] >= big:
                continue
            x, y, f, pc, _ = ds[j]
            s = sim(f, ref[i]) if ref[i] is not None else 0
            if s < .25 and pos[i] is not None and np.hypot(x - pos[i][0], y - pos[i][1]) > 4:
                continue                            # círculo cercano pero de otro aspecto: que decida la búsqueda local
            pos[i] = (x, y)
            ref[i] = f if ref[i] is None else ref[i] * .85 + f * .15
            if s > .5:
                par[i] = pc
            pistas[i].append([t, round(x / LADO, 4), round(y / LADO, 4), round(s, 3)])
            hecho.add(i)
        for i in range(n):
            if i in hecho:
                continue
            q = local(cuadros[k], par[i], pos[i], gate * paso / .25 + 4) if (par[i] is not None and pos[i] and
                                                                             cuadros[k] is not None) else None
            if q and q[2] > .62:
                pos[i] = q[:2]
                pistas[i].append([t, round(q[0] / LADO, 4), round(q[1] / LADO, 4), round(q[2], 3)])
            else:
                pistas[i].append([t, None, None, 0.0])
    out = {nom: dict(campeon=c, equipo=e, puntos=pistas[i]) for i, (nom, c, e) in enumerate(jugadores)}
    return out, ts, cuadros, dets


def limpiar(puntos, vmax=.03, ventana=5, cada=1.0, reloj=0.0):
    """pista cruda [[t, u, v, parecido, ...]] → puntos para la escena 3D [[g, u, v(, "salto")]]: quita saltos sueltos (más
    rápidos que vmax de mapa por s y que no se sostienen 3 muestras), mediana móvil y una muestra cada `cada` s. Un hueco
    (muerte, tapado) o un salto sostenido (Destello, TP, base) se marca «salto» para que la ficha no cruce el mapa."""
    pts = [q for q in puntos if q[1] is not None]
    buenos = []
    for k, q in enumerate(pts):
        if buenos:
            p = buenos[-1]
            dt = max(q[0] - p[0], 1e-3)
            if np.hypot(q[1] - p[1], q[2] - p[2]) / dt > vmax * 4:
                sig = pts[k + 1:k + 3]                   # ¿se sostiene?
                if len(sig) < 2 or any(np.hypot(r[1] - q[1], r[2] - q[2]) > .03 for r in sig):
                    continue
        buenos.append(q)
    if not buenos:
        return []
    arr = np.array([[q[0], q[1], q[2]] for q in buenos])
    h = ventana // 2
    suave = [[arr[i, 0], *np.median(arr[max(0, i - h):i + h + 1, 1:], axis=0)] for i in range(len(arr))]
    out, ult = [], None
    for t, u, v in suave:
        if ult is not None and t - ult[0] < cada - 1e-6:
            continue
        p = [round(t + reloj, 2), round(float(u), 4), round(float(v), 4)]
        if ult is not None and (t - ult[0] > 2.5 * cada or np.hypot(u - ult[1], v - ult[2]) > vmax * (t - ult[0]) * 3):
            p.append("salto")
        out.append(p)
        ult = (t, u, v)
    return out


def hoja_inicio(pistas, mini, dets, ruta):
    im = cv2.resize(mini, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_CUBIC)
    for x, y, *_ in dets:
        cv2.circle(im, (int(x * ESC), int(y * ESC)), 30, (0, 255, 255), 1)
    for nom, p in pistas.items():
        t, u, v, _ = p["puntos"][0][:4]
        if u is None:
            continue
        q = (int(u * LADO * ESC), int(v * LADO * ESC))
        cv2.putText(im, f"{nom} {p['campeon']}", (q[0] - 40, q[1] + 46), cv2.FONT_HERSHEY_SIMPLEX, .5,
                    COLOR.get(p["equipo"]), 2, cv2.LINE_AA)
        cv2.putText(im, f"{int(u * LADO)},{int(v * LADO)}", (q[0] - 25, q[1] - 34), cv2.FONT_HERSHEY_SIMPLEX, .4,
                    (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(ruta, im)


def hoja(pistas, ts, cuadros, ruta, n=6, escala=2):
    """rastros acumulados (últimos 12 s) sobre el minimapa en n momentos (para revisar)"""
    idx = np.linspace(0, len(ts) - 1, n).astype(int)
    tiles = []
    for k in idx:
        if cuadros[k] is None:
            continue
        im = cv2.resize(cuadros[k], None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)
        for nombre, p in pistas.items():
            col = COLOR.get(p["equipo"], (0, 255, 255))
            ant = None
            for t, u, v, *_ in p["puntos"][:k + 1]:
                if u is None or t < ts[k] - 12:
                    ant = None
                    continue
                q = (int(u * LADO * escala), int(v * LADO * escala))
                if ant:
                    cv2.line(im, ant, q, col, 2, cv2.LINE_AA)
                ant = q
            t, u, v, *_ = p["puntos"][k]
            if u is not None:
                q = (int(u * LADO * escala), int(v * LADO * escala))
                cv2.circle(im, q, 5, col, -1)
                cv2.putText(im, nombre[:7], (q[0] + 6, q[1] - 6), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255), 1,
                            cv2.LINE_AA)
        cv2.putText(im, f"t={ts[k]:.1f}", (8, 22), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 255), 2)
        tiles.append(im)
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(ruta, np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("t0", type=float)
    ap.add_argument("t1", type=float)
    ap.add_argument("--iconos", required=True)
    ap.add_argument("--jug", nargs="+", required=True, help="Nombre:Campeon:A|R")
    ap.add_argument("--paso", type=float, default=.25)
    ap.add_argument("--inicio", nargs="*", default=[], help="Nombre=x,y (px del minimapa en el primer cuadro)")
    ap.add_argument("--reloj", type=float, help="segundo de juego = t + N")
    ap.add_argument("--salida")
    ap.add_argument("--hoja")
    a = ap.parse_args()
    jug = [tuple(j.split(":")) for j in a.jug]
    ini = {s.split("=")[0]: tuple(float(v) for v in s.split("=")[1].split(",")) for s in a.inicio}
    pistas, ts, cuadros, dets = rastrear(a.clip, a.t0, a.t1, jug, a.iconos, a.paso, ini)
    for nombre, p in pistas.items():
        ok = [q for q in p["puntos"] if q[1] is not None]
        print(f"{nombre:12s} {p['campeon']:10s} puntos {len(ok)}/{len(p['puntos'])} "
              f"parecido medio {np.mean([q[3] for q in ok]) if ok else 0:.2f}")
        if a.reloj is not None:
            for q in p["puntos"]:
                q.append(round(q[0] + a.reloj, 2))
    if a.salida:
        json.dump(pistas, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, default=float)
    if a.hoja:
        hoja(pistas, ts, cuadros, a.hoja)
        hoja_inicio(pistas, cuadros[0], dets[0], a.hoja.replace(".jpg", "_inicio.jpg"))


if __name__ == "__main__":
    main()
