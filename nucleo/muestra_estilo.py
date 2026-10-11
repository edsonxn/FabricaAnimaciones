# -*- coding: utf-8 -*-
"""Muestra de estilo: 10 cuadros distintos de un video SIN necesitar voz ni la etapa `tiempo`.

Lo lanza el panel (botón «Ver estilo»); también sirve a mano, desde la carpeta del video:
    PYTHONPATH=<video>;<nucleo> python muestra_estilo.py [n_cuadros]

- Si ya hay timeline.json (real o provisional) lo usa tal cual.
- Si no, construye uno PROVISIONAL en memoria-de-archivo (estima cuándo se dice cada palabra, ~3,2 palabras/s; en videos
  SIN_VOZ usa los compases del guion) para que las anclas `self.w("palabra")` de escenas.py encuentren su tiempo, dibuja
  los cuadros con el mismo `render.Renderizador.cuadro` del render final y BORRA ese timeline al terminar
  (nunca pisa uno real, y `python fab.py <video> tiempo` sigue siendo el que manda).
Salida en previews/muestra/: m_01.jpg … + muestra.json (tiempo y escena de cada cuadro) + estado.json (progreso).
"""
import json
import os
import re
import sys
import time
import traceback

CARPETA = os.getcwd()
SAL = os.path.join(CARPETA, "previews", "muestra")
ANCHO = 960


def estado(**kw):
    os.makedirs(SAL, exist_ok=True)
    kw["t"] = time.time()
    tmp = os.path.join(SAL, "estado.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(kw, f, ensure_ascii=False)
    os.replace(tmp, os.path.join(SAL, "estado.json"))


def timeline_provisional():
    """Mismo formato que linea_tiempo.py / linea_tiempo_mudo.py, con tiempos estimados."""
    import config
    bpm = float(config.BPM)
    beat = 60 / bpm
    unidad = 4
    barra = unidad * beat
    escenas, t = [], 0.0
    for k, e in enumerate(config.ESCENAS):
        esc = {kk: vv for kk, vv in e.items() if kk not in ("frases", "anclas")}
        t0 = t
        if config.SIN_VOZ:
            n = max(1, int(e.get("compases", 1)))
            frases = []
            fin_voz = t0
            t1 = t0 + n * barra
        else:
            tt = t0 + e.get("pre", 0.35)
            frases = []
            for i, tx in enumerate(e.get("frases") or []):
                t_f, ws = tt, []
                for w in tx.split():
                    dur = 0.12 + 0.045 * len(re.sub(r"\W", "", w))
                    ws.append(dict(w=w, s=round(tt, 3), e=round(tt + dur, 3)))
                    tt += dur
                    if w.endswith((",", ".", ":", "?", "!")):
                        tt += 0.22
                frases.append(dict(key=f"{e['id']}_{i}", texto=tx, t0=round(t_f, 3), t1=round(tt, 3), words=ws))
                tt += config.GAP
            fin_voz = tt - config.GAP
            tt += e.get("post", 0.4)
            n = max(1, int(-(-(tt - t0) // barra)))
            t1 = t0 + n * barra
        esc.update(t0=round(t0, 4), t1=round(t1, 4), compases=n, frases=frases, fin_voz=round(fin_voz, 3), beats=4 * n)
        escenas.append(esc)
        t = t1
    trans = [dict(t=a["t1"], t0=round(a["t1"] - 0.05, 4), t1=round(a["t1"] + 0.05, 4), tipo="continua", de=a["id"], a=b["id"])
             for a, b in zip(escenas, escenas[1:])]
    tl = dict(bpm=bpm, beat=beat, unidad=unidad, total=round(t, 3), titulo=config.TITULO, estilo=config.ESTILO_VISUAL,
              escenas=escenas, transiciones=trans, provisional=True)
    escenas[-1]["fin_musica"] = round(t - 3 * beat, 4)
    return tl


def elegir_tiempos(tl, n):
    """n instantes repartidos por TODAS las escenas (varios por escena si hay pocas), a media y última parte de cada una,
    que es cuando ya entró lo principal."""
    esc = tl["escenas"]
    if len(esc) >= n:
        idx = sorted({round(i * (len(esc) - 1) / (n - 1)) for i in range(n)}) if n > 1 else [0]
        cuentas = {i: 1 for i in idx}
    else:
        cuentas = {i: n // len(esc) + (1 if i < n % len(esc) else 0) for i in range(len(esc))}
    out = []
    for i, c in sorted(cuentas.items()):
        e = esc[i]
        d = e["t1"] - e["t0"]
        for j in range(c):
            fr = 0.62 if c == 1 else 0.3 + 0.55 * j / (c - 1)
            out.append((round(e["t0"] + d * fr, 2), e["id"]))
    return out[:n]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    ruta_tl = os.path.join(CARPETA, "timeline.json")
    temporal = not os.path.exists(ruta_tl)
    estado(estado="arrancando", hecho=0, total=n)
    try:
        if temporal:
            with open(ruta_tl, "w", encoding="utf-8") as f:
                json.dump(timeline_provisional(), f, ensure_ascii=False)
        tl = json.load(open(ruta_tl, encoding="utf-8"))
        import cv2
        cv2.setNumThreads(4)
        import render as RN
        from motor import FPS
        R = RN.Renderizador()
        tiempos = elegir_tiempos(tl, n)
        for viejo in os.listdir(SAL) if os.path.isdir(SAL) else []:
            if re.match(r"^m_\d+\.jpg$", viejo):
                os.remove(os.path.join(SAL, viejo))
        cuadros = []
        for k, (t, eid) in enumerate(tiempos, 1):
            estado(estado="dibujando", hecho=k - 1, total=len(tiempos))
            nombre = f"m_{k:02d}.jpg"
            try:
                img = R.cuadro(round(t * FPS) / FPS)
                if ANCHO < img.shape[1]:
                    img = cv2.resize(img, (ANCHO, int(round(img.shape[0] * ANCHO / img.shape[1]))), interpolation=cv2.INTER_AREA)
                cv2.imwrite(os.path.join(SAL, nombre), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 86])
                cuadros.append(dict(archivo=nombre, t=t, escena=eid))
            except Exception as ex:                       # un cuadro roto no tumba la muestra
                cuadros.append(dict(archivo=None, t=t, escena=eid, error=f"{type(ex).__name__}: {ex}"[:300]))
        with open(os.path.join(SAL, "muestra.json"), "w", encoding="utf-8") as f:
            json.dump(dict(cuadros=cuadros, provisional=bool(tl.get("provisional")), total=tl["total"],
                           estilo=tl.get("estilo", ""), generado=time.time()), f, ensure_ascii=False)
        estado(estado="listo", hecho=len(tiempos), total=len(tiempos))
    except SystemExit as ex:
        estado(estado="error", error=str(ex.code or "salida"))
    except Exception as ex:
        estado(estado="error", error=f"{type(ex).__name__}: {ex}", detalle=traceback.format_exc()[-1500:])
    finally:
        if temporal:
            try:
                os.remove(ruta_tl)
            except OSError:
                pass


if __name__ == "__main__":
    main()
