# -*- coding: utf-8 -*-
"""RUTAS sobre el VOD (28-oct-2026, `cfo_kc_worlds`): la ruta que hizo cada jugador, dibujada pegada al SUELO de la propia
transmisión (como el telestrador de la NFL), para la repetición en cámara lenta.

En el minimapa los iconos se enciman en las peleas (rastrear.py); en la vista principal cada jugador lleva su BARRA DE VIDA
(cuadro de nivel + relleno rojo o azul del equipo, ~100×8 px en 1080p), que no se confunde. Cada `paso` s:
1. movimiento de la CÁMARA: phaseCorrelate entre cuadros consecutivos (zona de juego a 1/4, sin el HUD) → desplazamiento
   acumulado: mundo = pantalla + cámara (en px de 1080p; vale mientras la cámara solo se desliza, como en las peleas);
2. barras: relleno rojo/azul de 40-140×4-16 px → el EXTREMO IZQUIERDO del relleno (no cambia con la vida);
3. identidad: a mano en el primer cuadro (--inicio Nombre:A|R:x,y = extremo izquierdo de su barra) y luego continuidad
   (Hungarian por equipo, salto máximo `gate` px por paso). Si la cámara corta (salto > 200 px) el tramo se parte.
uso:
  python nucleo/tactica3d/rastros_vod.py <clip.mp4> <t0> <t1> --inicio Kino:R:908,214 Yeon:A:581,298 ... \
        [--paso .1] [--salida rastros.json] [--hoja hoja.jpg]
Lo dibuja `mg_tactica.rastros_vod(datos, …)` sobre el FX `video` del clip (mismo t0/vel).
"""
import argparse
import json

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment

JUEGO_Y = 780                 # por debajo, el HUD de la transmisión
PIES = 118                    # px de 1080p entre el extremo de la barra y los pies del campeón (aprox.)


def barras(f):
    g = f[:JUEGO_Y]
    hsv = cv2.cvtColor(g, cv2.COLOR_BGR2HSV)
    out = []
    for eq, m in (("R", cv2.inRange(hsv, (0, 140, 110), (8, 255, 255)) | cv2.inRange(hsv, (170, 140, 110), (180, 255, 255))),
                  ("A", cv2.inRange(hsv, (95, 120, 120), (114, 255, 255)))):
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 9), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            if 12 <= w <= 140 and 4 <= h <= 16 and w / h > 2.5 and a > .5 * w * h:
                # el relleno debe tener el marco oscuro de la barra justo encima/debajo
                out.append((eq, float(x), float(y + h / 2)))
    return out


def camara(prev, cur):
    a = cv2.cvtColor(cv2.resize(prev[:JUEGO_Y], None, fx=.25, fy=.25), cv2.COLOR_BGR2GRAY).astype(np.float32)
    b = cv2.cvtColor(cv2.resize(cur[:JUEGO_Y], None, fx=.25, fy=.25), cv2.COLOR_BGR2GRAY).astype(np.float32)
    win = cv2.createHanningWindow(a.shape[::-1], cv2.CV_32F)
    (dx, dy), resp = cv2.phaseCorrelate(a, b, win)
    return -dx * 4, -dy * 4, resp


def rastrear(clip, t0, t1, inicio, paso=.1, gate=70):
    cap = cv2.VideoCapture(clip)
    nombres = list(inicio)
    eqs = {n: inicio[n][0] for n in nombres}
    pos = {n: np.array(inicio[n][1:], float) for n in nombres}     # en coordenadas de MUNDO
    cam = np.zeros(2)
    out_cam, pts = [], {n: [] for n in nombres}
    prev = None
    for t in np.arange(t0, t1 + 1e-6, paso):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        if not ok:
            break
        if prev is not None:
            dx, dy, resp = camara(prev, f)
            if abs(dx) > 200 or abs(dy) > 200 or resp < .05:
                out_cam.append([round(float(t), 2), None, None])          # corte de cámara
                prev = f
                for n in nombres:
                    pts[n].append([round(float(t), 2), None, None])
                continue
            cam += (dx, dy)
        prev = f
        out_cam.append([round(float(t), 2), round(float(cam[0]), 1), round(float(cam[1]), 1)])
        dets = [(e, x + cam[0], y + cam[1]) for e, x, y in barras(f)]
        hecho = set()
        for eq in ("A", "R"):
            js = [n for n in nombres if eqs[n] == eq]
            ds = [d for d in dets if d[0] == eq]
            if not js or not ds:
                continue
            C = np.array([[np.hypot(d[1] - pos[n][0], d[2] - pos[n][1]) for d in ds] for n in js])
            ri, ci = linear_sum_assignment(C)
            for i, j in zip(ri, ci):
                if C[i, j] <= gate * paso / .1:
                    n = js[i]
                    pos[n] = np.array(ds[j][1:])
                    pts[n].append([round(float(t), 2), round(float(pos[n][0]), 1), round(float(pos[n][1]), 1)])
                    hecho.add(n)
        for n in nombres:
            if n not in hecho:
                pts[n].append([round(float(t), 2), None, None])
    return dict(t0=t0, paso=paso, pies=PIES, cam=out_cam,
                jug={n: dict(eq=eqs[n], pts=pts[n]) for n in nombres})


def hoja(datos, clip, ruta, n=6):
    cap = cv2.VideoCapture(clip)
    cams = [c for c in datos["cam"] if c[1] is not None]
    idx = np.linspace(0, len(cams) - 1, n).astype(int)
    tiles = []
    for k in idx:
        t, cx, cy = cams[k]
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        for nom, j in datos["jug"].items():
            col = (255, 170, 60) if j["eq"] == "A" else (60, 60, 255)
            ant = None
            for tt, x, y in j["pts"]:
                if tt > t:
                    break
                if x is None:
                    ant = None
                    continue
                q = (int(x - cx + 50), int(y - cy + datos["pies"]))
                if ant:
                    cv2.line(f, ant, q, col, 4, cv2.LINE_AA)
                ant = q
            if ant:
                cv2.circle(f, ant, 9, col, -1)
                cv2.putText(f, nom, (ant[0] + 10, ant[1] + 30), 0, 1, (255, 255, 255), 2)
        cv2.putText(f, f"t={t:.1f}", (20, 60), 0, 1.5, (0, 255, 255), 3)
        tiles.append(cv2.resize(f, (640, 360)))
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(ruta, np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("t0", type=float)
    ap.add_argument("t1", type=float)
    ap.add_argument("--inicio", nargs="+", required=True, help="Nombre:A|R:x,y")
    ap.add_argument("--paso", type=float, default=.1)
    ap.add_argument("--salida")
    ap.add_argument("--hoja")
    a = ap.parse_args()
    ini = {}
    for s in a.inicio:
        n, e, xy = s.split(":")
        x, y = map(float, xy.split(","))
        ini[n] = (e, x, y)
    d = rastrear(a.clip, a.t0, a.t1, ini, a.paso)
    for n, j in d["jug"].items():
        print(f"{n:10s} {sum(p[1] is not None for p in j['pts'])}/{len(j['pts'])}")
    if a.salida:
        json.dump(d, open(a.salida, "w", encoding="utf-8"))
    if a.hoja:
        hoja(d, a.clip, a.hoja)


if __name__ == "__main__":
    main()


def camara_clip(clip, paso=.1):
    """trayectoria de la cámara de todo el clip: [[t, cx, cy] o [t, None, None] en los cortes], leyendo en orden"""
    cap = cv2.VideoCapture(clip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cada = max(1, round(paso * fps))
    out, prev, cam, k = [], None, np.zeros(2), 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if k % cada == 0:
            t = round(k / fps, 2)
            if prev is not None:
                dx, dy, resp = camara(prev, f)
                if abs(dx) > 200 or abs(dy) > 200 or resp < .05:
                    cam = np.zeros(2)
                    out.append([t, None, None])
                else:
                    cam += (dx, dy)
                    out.append([t, round(float(cam[0]), 1), round(float(cam[1]), 1)])
            else:
                out.append([t, 0.0, 0.0])
            prev = f
        k += 1
    return out


def ruta_en(cam, t_ref, puntos, ancho=1920, alto=1080):
    """puntos [(t, x, y)] en FRACCIÓN del cuadro t → mismas posiciones en el cuadro t_ref (fracción), con la cámara.
    Si entre t y t_ref hay un corte de cámara, ese punto se descarta."""
    def c(t):
        k = min(range(len(cam)), key=lambda i: abs(cam[i][0] - t))
        return cam[k], k
    (_, rx, ry), kr = c(t_ref)
    out = []
    for t, x, y in puntos:
        (_, cx, cy), k = c(t)
        a, b = sorted((k, kr))
        if cx is None or rx is None or any(q[1] is None for q in cam[a + 1:b + 1]):
            continue
        out.append((round(x + (cx - rx) / ancho, 4), round(y + (cy - ry) / alto, 4)))
    return out


if __name__ == "__main__" and False:
    pass
