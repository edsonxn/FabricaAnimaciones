# -*- coding: utf-8 -*-
"""Servidor de vista previa de UN video (lo lanza el panel; no se usa a mano).

Dibuja cuadros con el MISMO motor del render final (`render.Renderizador.cuadro`), así que lo que se ve es
exactamente lo que saldrá en el MASTER. Se ejecuta en la carpeta del video con PYTHONPATH = video;nucleo:

    python preview_worker.py --puerto 9001 --token abc

Endpoints (todos piden ?token=): /info  /frame?t=&w=[&s=&rel=1]  /audio  /onda  /clip (POST)  /clip/estado  /clip.mp4
  Escenas guardadas: /escenas  /escena (POST id,w,procs,forzar)  /escena/estado?job=  /escena.mp4?id=  /escenas/conservar (POST)
Se cierra solo tras 10 min sin uso (y sin clip ni escena en curso).

«Renderizar escena»: dibuja la escena con el codificador del render final y deja sus segmentos en `segmentos/`
(anotados en `segmentos/preview_origen.json`, ver cache_escenas.py): el render completo los reutiliza. Además
guarda `previews/escena_<id>.mp4` (con audio) para reproducirla fluida en la propia vista previa.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from multiprocessing import Pool
from urllib.parse import parse_qs, urlparse

import cv2
import numpy as np

import cache_escenas as CE

CARPETA = os.getcwd()
NUCLEO = os.path.dirname(os.path.abspath(__file__))
FIRMA0 = CE.firma_codigo(CARPETA, NUCLEO)        # código con el que arranca este motor (antes de importar render)

import render as RN  # noqa: E402
from motor import FPS, H, VERTICAL, W  # noqa: E402

PREV = os.path.join(CARPETA, "previews")
TOKEN = ""
OCIOSO_S = 600
PIEZA = 30             # cuadros por pieza de la escena: 3 por segmento, así los 12 procesos se reparten parejo

_R = None
_cerrojo = threading.Lock()
_cache = OrderedDict()
_ultimo_seq = {"n": 0}
_uso = {"t": time.time()}
_clips = {}            # id -> dict(estado, progreso, ruta, error)
_jobs = {}             # id -> dict(estado, progreso, fase, escena, error): escenas que se guardan para el render final


# ------------------------------------------------------------------ cuadros
def _redimensionar(img, ancho):
    if ancho and ancho < img.shape[1]:
        alto = int(round(img.shape[0] * ancho / img.shape[1]))
        return cv2.resize(img, (ancho, alto), interpolation=cv2.INTER_AREA)
    return img


def cuadro_jpeg(t, ancho, seq=None):
    """JPEG del cuadro en t (segundos). Devuelve None si una petición más nueva lo hizo obsoleto."""
    i = max(0, min(RN.NFRAMES - 1, int(round(t * FPS))))
    clave = (i, ancho)
    if clave in _cache:
        _cache.move_to_end(clave)
        return _cache[clave]
    with _cerrojo:
        if seq is not None and seq < _ultimo_seq["n"]:
            return None
        if clave in _cache:
            return _cache[clave]
        img = _redimensionar(_R.cuadro(i / FPS), ancho)
        ok, buf = cv2.imencode(".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 84])
        datos = buf.tobytes()
        _cache[clave] = datos
        while len(_cache) > 240:
            _cache.popitem(last=False)
        return datos


# ------------------------------------------------------------------ audio y onda
def ruta_audio():
    """m4a liviano para el navegador (el final.wav es de 24 bits y pesa decenas de MB)."""
    wav = os.path.join(CARPETA, "audio", "final.wav")
    if not os.path.isfile(wav):
        return None
    os.makedirs(PREV, exist_ok=True)
    m4a = os.path.join(PREV, "_preview_audio.m4a")
    if not os.path.isfile(m4a) or os.path.getmtime(m4a) < os.path.getmtime(wav):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "aac", "-b:a", "128k", m4a], check=True)
    return m4a


def onda(n=1600):
    wav = os.path.join(CARPETA, "audio", "final.wav")
    if not os.path.isfile(wav):
        return []
    import soundfile as sf
    x, sr = sf.read(wav, dtype="float32", always_2d=True)
    m = np.abs(x).max(axis=1)
    paso = max(1, len(m) // n)
    m = m[: paso * (len(m) // paso)].reshape(-1, paso).max(axis=1)
    return [round(float(v), 3) for v in m]


# ------------------------------------------------------------------ clip suave (paralelo)
def _trozo_clip(args):
    i0, i1, ruta, ancho = args
    alto = int(round(H * ancho / W)) if ancho < W else H
    ancho = min(ancho, W)
    tmp = ruta + ".tmp.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ancho}x{alto}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
           "-g", "30", "-threads", "2", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        img = _redimensionar(RN._R.cuadro(i / FPS), ancho)
        p.stdin.write(np.ascontiguousarray(img).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    os.replace(tmp, ruta)
    return ruta


def _hacer_clip(cid, t0, t1, ancho, procs):
    c = _clips[cid]
    try:
        os.makedirs(PREV, exist_ok=True)
        i0, i1 = int(round(t0 * FPS)), min(RN.NFRAMES, int(round(t1 * FPS)))
        tam = max(6, -(-(i1 - i0) // procs))          # un trozo por proceso: el arranque se paga una sola vez
        trozos = [(i, min(i + tam, i1), os.path.join(PREV, f"_clip_{cid}_{k:03d}.mp4"), ancho)
                  for k, i in enumerate(range(i0, i1, tam))]
        procs = RN.procesos_seguros(min(procs, len(trozos)))
        hechos = 0
        with Pool(procs, initializer=RN._init) as pool:
            for _ in pool.imap_unordered(_trozo_clip, trozos):
                hechos += 1
                c["progreso"] = hechos / len(trozos)
        lista = os.path.join(PREV, f"_clip_{cid}.txt")
        with open(lista, "w") as f:
            for _, _, r, _ in trozos:
                f.write(f"file '{os.path.basename(r)}'\n")
        sal = os.path.join(PREV, f"_clip_{cid}.mp4")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista]
        wav = os.path.join(CARPETA, "audio", "final.wav")
        if os.path.isfile(wav):
            cmd += ["-ss", f"{i0 / FPS:.3f}", "-t", f"{(i1 - i0) / FPS:.3f}", "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest"]
        else:
            cmd += ["-c", "copy"]
        subprocess.run(cmd + [sal], check=True)
        for _, _, r, _ in trozos:
            os.remove(r)
        os.remove(lista)
        c.update(estado="listo", progreso=1.0, ruta=sal)
    except Exception as e:                     # noqa: BLE001
        c.update(estado="error", error=str(e))


def _limpiar_clips_viejos(conservar=6):
    try:
        mp4 = sorted((os.path.join(PREV, f) for f in os.listdir(PREV) if re.match(r"^_clip_\w+\.mp4$", f)),
                     key=os.path.getmtime)
        for f in mp4[:-conservar]:
            os.remove(f)
    except OSError:
        pass


# ------------------------------------------------------------------ escena guardada (segmentos del render final + mp4 fluido)
def _ocupado():
    return any(c["estado"] == "trabajando" for c in list(_clips.values()) + list(_jobs.values()))


def render_completo_en_curso():
    """¿Hay un render completo escribiendo segmentos? Dos escritores en segmentos/ y 12+12 procesos no se mezclan."""
    seg = os.path.join(CARPETA, "segmentos")
    try:
        for f in os.listdir(seg):
            if f.endswith(".tmp.mp4") and time.time() - os.path.getmtime(os.path.join(seg, f)) < 120:
                return True
    except OSError:
        pass
    try:
        import psutil
        for p in psutil.process_iter(["pid", "cmdline"]):
            c = p.info["cmdline"] or []
            if p.pid == os.getpid() or "video" not in c or not ("render" in c or "fab.py" in c):
                continue
            try:
                if os.path.normcase(p.cwd()) != os.path.normcase(CARPETA):
                    continue
            except Exception:                  # noqa: BLE001  (sin permiso para leer su carpeta: se asume que sí)
                pass
            return True
    except Exception:                          # noqa: BLE001
        pass
    return False


def _hacer_escena(jid, esc, ancho, procs, forzar):
    j = _jobs[jid]
    d = os.path.join(PREV, f"_esc_{jid}")
    try:
        libre = shutil.disk_usage(CARPETA).free
        if libre < 1.5e9:
            raise RuntimeError(f"queda poco disco libre ({libre / 1e9:.1f} GB): libera espacio antes de renderizar")
        i0, i1 = int(round(esc["t0"] * FPS)), min(RN.NFRAMES, int(round(esc["t1"] * FPS)))
        k0, k1 = CE.rango_segmentos(i0, i1, RN.NFRAMES)
        os.makedirs("segmentos", exist_ok=True)
        os.makedirs(d, exist_ok=True)
        preset = RN._info_segmentos(CE.SEG, os.environ.get("FAB_PRESET", "medium"))
        firma = CE.firma_codigo(CARPETA, NUCLEO)
        if firma != FIRMA0:
            raise RuntimeError("el código cambió desde que arrancó el motor: pulsa «Recargar motor» y vuelve a intentarlo")
        man = CE.leer(CARPETA)
        if not forzar:                          # segmentos de un render completo hecho DESPUÉS de la última edición: ya sirven
            CE.adoptar(CARPETA, NUCLEO, [k for k in range(k0, k1) if CE.estado_seg(CARPETA, k, man, firma) == "ajeno"], firma)
            man = CE.leer(CARPETA)
        hacer = [k for k in range(k0, k1) if forzar or CE.estado_seg(CARPETA, k, man, firma) != "vigente"]
        if hacer and render_completo_en_curso():     # nunca dos escritores en segmentos/
            raise RuntimeError("un render completo de este video está escribiendo segmentos/: espera a que termine")
        j.update(fase="dibujando", reusados=(k1 - k0) - len(hacer), dibujados=len(hacer), segs=k1 - k0)
        tareas = [(a, min(a + PIEZA, RN.NFRAMES), os.path.join(d, f"p_{k:04d}_{n}.mp4"), preset)
                  for k in hacer for n in range(CE.SEG // PIEZA)
                  for a in [k * CE.SEG + n * PIEZA] if a < RN.NFRAMES]
        if tareas:
            hechos = 0
            with Pool(RN.procesos_seguros(min(procs, len(tareas))), initializer=RN._init) as pool:
                for _ in pool.imap_unordered(RN._trozo, tareas):
                    hechos += 1
                    j["progreso"] = 0.88 * hechos / len(tareas)
        j.update(fase="uniendo")
        for k in hacer:                         # 3 piezas -> seg_NNNN.mp4 (copia de flujo; mismo códec que el render final)
            piezas = sorted(f for f in os.listdir(d) if f.startswith(f"p_{k:04d}_"))
            lista = os.path.join(d, f"l_{k:04d}.txt")
            with open(lista, "w") as f:
                f.writelines(f"file '{p}'\n" for p in piezas)
            sal = CE.ruta_seg(CARPETA, k) + ".tmp.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", sal],
                           check=True)
            os.replace(sal, CE.ruta_seg(CARPETA, k))
        if CE.firma_codigo(CARPETA, NUCLEO) != firma:
            raise RuntimeError("el código cambió mientras se renderizaba: esos segmentos no se guardan para el render final; "
                               "recarga el motor y renderiza otra vez")
        CE.anotar(CARPETA, hacer, firma)
        j.update(fase="preparando el video", progreso=0.92)
        _empaquetar(esc, ancho, firma, k0, k1, d)
        j.update(estado="listo", progreso=1.0, fase="listo")
    except Exception as e:                      # noqa: BLE001
        j.update(estado="error", error=str(e) or e.__class__.__name__)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _empaquetar(esc, ancho, firma, k0, k1, d, hilos=None):
    """mp4 liviano (con audio) de la escena a partir de sus segmentos ya hechos (ver `cache_escenas.empaquetar_escena`)."""
    CE.empaquetar_escena(CARPETA, esc["id"], k0, k1, RN.NFRAMES, FPS, ancho, W, firma, hilos=hilos)


_auto = {"t": 0.0}


def autocompletar(ancho=960):
    """Escenas cuyos segmentos ya valen con el código actual (los dejó el render completo, o una escena fluida) pero que aún no
    tienen su mp4 de la vista previa: lo arma sin dibujar nada (segundos) para que queden en verde sin pulsar «Renderizar» una
    por una. Solo con segmentos «vigentes» (anotados con la firma actual): nunca adivina por fechas y no toca las ámbar."""
    if time.time() - _auto["t"] < 20 or _ocupado() or render_completo_en_curso():
        return
    _auto["t"] = time.time()
    try:
        if shutil.disk_usage(CARPETA).free < 4e8:
            return
        firma = CE.firma_codigo(CARPETA, NUCLEO)
        if firma != FIRMA0:                     # código cambiado desde que arrancó el motor: «Recargar motor»
            return
        hechas = {e["id"] for e in CE.listar(CARPETA, NUCLEO)}
        man, pend = CE.leer(CARPETA), []
        for esc in RN.TL["escenas"]:
            if esc["id"] in hechas:
                continue
            k0, k1 = CE.rango_segmentos(int(round(esc["t0"] * FPS)), min(RN.NFRAMES, int(round(esc["t1"] * FPS))), RN.NFRAMES)
            if all(CE.estado_seg(CARPETA, k, man, firma) == "vigente" for k in range(k0, k1)):
                pend.append((esc, k0, k1))
    except Exception:                           # noqa: BLE001  (esto es un extra: nunca debe tumbar el motor)
        return
    if not pend:
        return
    jid = f"auto{int(time.time())}"
    # escena="" a propósito: la ventana sigue el progreso pero no salta ni reproduce ninguna escena al terminar
    _jobs[jid] = dict(estado="trabajando", progreso=0.0, fase=f"armando {len(pend)} escenas ya renderizadas", escena="", id=jid,
                      t_ini=time.time())
    threading.Thread(target=_autocompletar_hilo, args=(jid, pend, firma, ancho), daemon=True).start()


def _autocompletar_hilo(jid, pend, firma, ancho):
    j = _jobs[jid]
    d = os.path.join(PREV, f"_esc_{jid}")
    try:
        for n, (esc, k0, k1) in enumerate(pend):
            if CE.firma_codigo(CARPETA, NUCLEO) != firma:
                break                           # cambió el código a la mitad: lo ya armado vale, lo demás se deja
            j.update(progreso=n / len(pend), fase=f"armando «{esc['id']}» ({n + 1}/{len(pend)})")
            _empaquetar(esc, ancho, firma, k0, k1, d, hilos=2)
        j.update(estado="listo", progreso=1.0, fase="listo")
    except Exception as e:                      # noqa: BLE001
        j.update(estado="error", error=str(e) or e.__class__.__name__)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def resumen_escenas():
    autocompletar()
    trabajando = [dict(job=k, **{x: v[x] for x in ("estado", "progreso", "fase", "escena", "reusados", "dibujados") if x in v})
                  for k, v in _jobs.items() if v["estado"] == "trabajando"]
    return dict(entradas=CE.listar(CARPETA, NUCLEO), job=trabajando[0] if trabajando else None,
                codigo_al_dia=CE.firma_codigo(CARPETA, NUCLEO) == FIRMA0, render_completo=render_completo_en_curso())


# ------------------------------------------------------------------ servidor
def info():
    tl = RN.TL
    return dict(
        video=os.path.basename(CARPETA), titulo=tl.get("titulo"), total=tl["total"], fps=FPS, w=W, h=H,
        vertical=bool(VERTICAL), audio=os.path.isfile(os.path.join(CARPETA, "audio", "final.wav")),
        escenas=[dict(id=e["id"], t0=e["t0"], t1=e["t1"], titulo=e.get("titulo") or e["id"]) for e in tl["escenas"]],
        transiciones=[dict(t0=x["t0"], t1=x["t1"], tipo=x["tipo"]) for x in tl["transiciones"]],
        frases=[dict(t0=f["t0"], t1=f["t1"], texto=f["texto"]) for e in tl["escenas"] for f in e["frases"]],
    )


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _enviar(self, codigo, cuerpo, tipo, extra=None):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(cuerpo)

    def _archivo(self, ruta, tipo):
        """Sirve un archivo con soporte de Range (el <audio>/<video> del navegador lo necesita para saltar)."""
        tam = os.path.getsize(ruta)
        rango = self.headers.get("Range")
        a, b = 0, tam - 1
        if rango:
            m = re.match(r"bytes=(\d*)-(\d*)", rango)
            if m:
                if m.group(1):
                    a = int(m.group(1))
                    b = int(m.group(2)) if m.group(2) else tam - 1
                elif m.group(2):
                    a = max(0, tam - int(m.group(2)))
        b = min(b, tam - 1)
        with open(ruta, "rb") as f:
            f.seek(a)
            datos = f.read(b - a + 1)
        extra = {"Accept-Ranges": "bytes"}
        if rango:
            extra["Content-Range"] = f"bytes {a}-{b}/{tam}"
        self._enviar(206 if rango else 200, datos, tipo, extra)

    def _q(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        return u.path, q

    def do_OPTIONS(self):
        self._enviar(204, b"", "text/plain", {"Access-Control-Allow-Methods": "GET,POST,OPTIONS"})

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        ruta, q = self._q()
        try:
            if q.get("token") != TOKEN:
                return self._enviar(403, b"", "text/plain")
            _uso["t"] = time.time()
            if ruta == "/info":
                self._enviar(200, json.dumps(info(), ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            elif ruta == "/frame":
                t = float(q.get("t", 0))
                ancho = int(q.get("w", 960))
                seq = None
                if q.get("rel") == "1" and "s" in q:
                    seq = int(q["s"])
                    _ultimo_seq["n"] = max(_ultimo_seq["n"], seq)
                datos = cuadro_jpeg(t, ancho, seq)
                if datos is None:
                    return self._enviar(204, b"", "text/plain")
                self._enviar(200, datos, "image/jpeg")
            elif ruta == "/audio":
                m4a = ruta_audio()
                if not m4a:
                    return self._enviar(404, b"", "text/plain")
                self._archivo(m4a, "audio/mp4")
            elif ruta == "/onda":
                self._enviar(200, json.dumps(onda()).encode("utf-8"), "application/json")
            elif ruta == "/clip/estado":
                c = _clips.get(q.get("id", ""))
                if not c:
                    return self._enviar(404, b"", "text/plain")
                self._enviar(200, json.dumps({k: v for k, v in c.items() if k != "ruta"}).encode("utf-8"), "application/json")
            elif ruta == "/clip.mp4":
                c = _clips.get(q.get("id", ""))
                if not c or c.get("estado") != "listo":
                    return self._enviar(404, b"", "text/plain")
                self._archivo(c["ruta"], "video/mp4")
            elif ruta == "/escenas":
                self._enviar(200, json.dumps(resumen_escenas()).encode("utf-8"), "application/json")
            elif ruta == "/escena/estado":
                j = _jobs.get(q.get("job", ""))
                if not j:
                    return self._enviar(404, b"", "text/plain")
                # `transcurrido` viene del motor: la estimación del panel no se reinicia si cierras y reabres la ventana
                self._enviar(200, json.dumps(dict(j, transcurrido=time.time() - j.get("t_ini", time.time()))).encode("utf-8"),
                             "application/json")
            elif ruta == "/escena.mp4":
                e = CE.leer_escenas(CARPETA).get(q.get("id", ""))
                f = os.path.join(PREV, e["mp4"]) if e else ""
                if not e or not os.path.isfile(f):
                    return self._enviar(404, b"", "text/plain")
                self._archivo(f, "video/mp4")
            else:
                self._enviar(404, b"", "text/plain")
        except ConnectionError:
            pass
        except Exception as e:                 # noqa: BLE001
            try:
                self._enviar(500, str(e).encode("utf-8", "replace"), "text/plain; charset=utf-8")
            except ConnectionError:
                pass

    def do_POST(self):
        ruta, q = self._q()
        try:
            if q.get("token") != TOKEN:
                return self._enviar(403, b"", "text/plain")
            _uso["t"] = time.time()
            if ruta == "/escena":
                esc = next((e for e in RN.TL["escenas"] if e["id"] == q.get("id")), None)
                if not esc:
                    return self._enviar(404, b'{"error":"esa escena no existe en el timeline"}', "application/json")
                if _ocupado():
                    return self._enviar(409, b'{"error":"ya hay un render de la vista previa en curso"}', "application/json")
                if render_completo_en_curso():           # solo se permite si la escena ya está hecha por ese render: no se dibuja nada
                    k0, k1 = CE.rango_segmentos(int(round(esc["t0"] * FPS)), min(RN.NFRAMES, int(round(esc["t1"] * FPS))), RN.NFRAMES)
                    listos = len(CE.sin_dibujar(CARPETA, NUCLEO, range(k0, k1)))
                    if q.get("forzar") == "1" or listos < k1 - k0:
                        falta = f"le faltan {k1 - k0 - listos} de {k1 - k0} tramos" if q.get("forzar") != "1" else "no se puede forzar"
                        return self._enviar(409, json.dumps({"error": f"hay un render completo de este video en marcha y a esta escena {falta}: "
                                                             "espera a que termine (el panel marca en verde las escenas que ya están listas) "
                                                             "o usa los cuadros; no se renderizan dos cosas a la vez"}).encode("utf-8"),
                                            "application/json")
                jid = f"{int(time.time())}"
                _jobs[jid] = dict(estado="trabajando", progreso=0.0, fase="preparando", escena=esc["id"], id=jid, t_ini=time.time())
                threading.Thread(target=_hacer_escena, daemon=True,
                                 args=(jid, esc, int(q.get("w", 960)), int(q.get("procs", 12)), q.get("forzar") == "1")).start()
                self._enviar(200, json.dumps({"job": jid}).encode("utf-8"), "application/json")
            elif ruta == "/escenas/conservar":
                ids = [x for x in q.get("ids", "").split(",") if x] or None
                n = CE.conservar_escenas(CARPETA, NUCLEO, ids)
                self._enviar(200, json.dumps({"conservadas": n}).encode("utf-8"), "application/json")
            elif ruta == "/clip":
                if _ocupado():
                    return self._enviar(409, b'{"error":"ya hay un render de la vista previa en curso"}', "application/json")
                t0 = max(0.0, float(q["t0"]))
                t1 = min(float(RN.TOTAL), float(q["t1"]))
                if t1 - t0 < 0.5:
                    return self._enviar(400, b'{"error":"rango muy corto"}', "application/json")
                t1 = min(t1, t0 + 60)
                cid = f"{int(time.time())}"
                _clips[cid] = dict(estado="trabajando", progreso=0.0, id=cid, t0=t0, t1=t1)
                _limpiar_clips_viejos()
                threading.Thread(target=_hacer_clip, daemon=True,
                                 args=(cid, t0, t1, int(q.get("w", 960)), int(q.get("procs", 8)))).start()
                self._enviar(200, json.dumps({"id": cid}).encode("utf-8"), "application/json")
            else:
                self._enviar(404, b"", "text/plain")
        except ConnectionError:
            pass
        except Exception as e:                 # noqa: BLE001
            try:
                self._enviar(500, str(e).encode("utf-8", "replace"), "text/plain; charset=utf-8")
            except ConnectionError:
                pass


def _vigilar_ocio():
    while True:
        time.sleep(30)
        if time.time() - _uso["t"] > OCIOSO_S and not _ocupado():
            print("cerrando por inactividad", flush=True)
            os._exit(0)


def main():
    global _R, TOKEN
    ap = argparse.ArgumentParser()
    ap.add_argument("--puerto", type=int, required=True)
    ap.add_argument("--token", required=True)
    a = ap.parse_args()
    TOKEN = a.token
    cv2.setNumThreads(4)
    _R = RN.Renderizador()
    srv = ThreadingHTTPServer(("127.0.0.1", a.puerto), Manejador)
    threading.Thread(target=_vigilar_ocio, daemon=True).start()
    threading.Thread(target=lambda: ruta_audio(), daemon=True).start()      # deja listo el m4a
    print(f"LISTO {a.puerto}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
