# -*- coding: utf-8 -*-
"""EN VIVO: un directo que se genera y se edita solo mientras se ve, y que cambia de tema cuando se lo piden.

    python fab.py envivo [canal] [--tema "…"] [--modelo sonnet|haiku] [--voz Raul] [--puerto 8790] [--abrir]

- Pantalla (lo que se transmite; en OBS como «Fuente de navegador»): http://127.0.0.1:8790/
- Ventanita de control (cambiar tema, votación, pausa):            http://127.0.0.1:8790/control

Cómo funciona: un hilo «productor» mantiene un búfer de BUFER bloques listos (~20-30 s cada uno): el director
(Claude por `claude -p`, GUIONISTAS a la vez) escribe 4-6 frases y elige pegatina/clip/rótulo de cada una, la voz de Windows las dice y las
imágenes que falten se bajan de la wiki del juego. La pantalla pide el siguiente bloque ~4 s antes de que acabe el
actual. Un cambio de tema tira el búfer (lo ya escrito para el tema viejo) y el siguiente bloque abre con un puente.
Votación: cada bloque trae 3 temas posibles; al pedir el siguiente bloque se cuenta el voto y el ganador manda.
Todo lo dicho queda en _sesiones/<fecha>/guion.jsonl (para cortar después un video o Shorts del directo).
"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import re
import sys
import threading
import time
from collections import deque

from flask import Flask, abort, jsonify, request, send_file, send_from_directory

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
from envivo import director, voz                           # noqa: E402
from envivo.biblioteca import CANALES, VIDEOS, Biblioteca  # noqa: E402

BUFER = 2           # bloques listos por delante del que está al aire: más = menos riesgo de hueco, más tarda un cambio de tema
GUIONISTAS = 2      # llamadas a `claude -p` a la vez (cada una ~8 s de arranque + ~3 s por frase)


class Directo:
    def __init__(self, canal, tema, modelo, voz_nombre, velocidad):
        self.canal, self.cfg = canal, CANALES[canal]
        self.modelo, self.voz, self.velocidad = modelo, voz_nombre, velocidad
        self.carpeta = os.path.join(AQUI, "_sesiones", time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.carpeta, exist_ok=True)
        self.bib = Biblioteca(canal, os.path.join(AQUI, "_cache", canal))
        self.cv = threading.Condition()
        self.tema, self.tema_ver = tema or self.cfg["tema_inicial"], 0
        self.ultimo_tema = None           # tema del último bloque escrito (para saber si toca puente)
        self.cola, self.historial = [], []
        self.al_aire, self.frase_al_aire = None, -1
        self.opciones, self.votos, self.votacion = [], {}, False
        self.pausado, self.estado, self.n = False, "arrancando", 0
        self.anuncio = None
        self.log = deque(maxlen=60)
        self.tiempos = deque(maxlen=10)
        self.seq, self.en_curso, self.listos = 0, {}, {}
        self.enfoques, self.enfoques_ver, self.vers_abiertas = deque(), 0, set()
        self._apunta(f"biblioteca: {len(self.bib.pegatinas)} pegatinas, {len(self.bib.clips)} clips, {len(self.bib.ost)} pistas de OST")
        threading.Thread(target=self._productor, daemon=True).start()

    def _apunta(self, txt):
        self.log.append(time.strftime("%H:%M:%S ") + txt)
        print(txt, flush=True)

    # --- control -------------------------------------------------------------------------------
    def cambiar_tema(self, tema, origen="control", conservar=0):
        """Tira el búfer del tema viejo. conservar=1 (votación): deja sonar un bloque más mientras se escribe el ganador,
        así no hay hueco. Desde el control queda 1 bloque de RELLENO (sin marca): la pantalla lo pone solo si el tema
        nuevo aún no está y lo deja a media frase en cuanto llega (el primer bloque nuevo tarda ~25 s en escribirse)."""
        tema = (tema or "").strip()[:120]
        if not tema:
            return
        with self.cv:
            for s in self.cola[:conservar]:
                s["conservado"] = True                  # la pantalla no lo descarta aunque sea del tema viejo
            quedan = max(conservar, 1)
            tirados = [s["id"] for s in self.cola[quedan:]]
            self.historial = [h for h in self.historial if h[0] not in tirados]
            del self.cola[quedan:]
            self.tema, self.tema_ver = tema, self.tema_ver + 1
            self.anuncio = {"tema": tema, "origen": origen, "t": time.time()}
            self.cv.notify_all()
        self._apunta(f"TEMA NUEVO ({origen}): {tema}" + (f" · se tiraron {len(tirados)} bloques del búfer" if tirados else ""))

    def votar(self, opcion):
        with self.cv:
            if opcion in self.opciones:
                self.votos[opcion] = self.votos.get(opcion, 0) + 1

    def siguiente(self, espera=20.0):
        """La pantalla pide el próximo bloque. Antes cuenta la votación (si está activa y hubo votos)."""
        if self.votacion and self.votos:
            ganador = max(self.votos, key=self.votos.get)
            self.votos = {}
            if ganador != self.tema:
                self.cambiar_tema(ganador, origen="votación", conservar=1)
        fin = time.time() + espera
        with self.cv:
            while not self.cola and time.time() < fin:
                self.cv.wait(timeout=0.5)
            if not self.cola:
                return {"espera": True, "tema": self.tema, "anuncio": self.anuncio, "estado": self.estado}
            seg = self.cola.pop(0)
            self.al_aire, self.frase_al_aire = seg, 0
            self.opciones, self.votos = list(seg.get("opciones", [])), {}
            self.cv.notify_all()
        return seg

    # --- productor -----------------------------------------------------------------------------
    # GUIONISTAS bloques se escriben a la vez: cada bloque propone 2 «proximos» subtemas y cada guionista toma uno
    # (sabe qué escriben los otros para no pisarse). Se entregan a la cola en orden de despacho (seq).
    def _productor(self):
        while True:
            with self.cv:
                while not self._puede_despachar():
                    self.cv.wait(timeout=1)
                tema, ver = self.tema, self.tema_ver
                if self.enfoques_ver != ver:
                    self.enfoques, self.enfoques_ver = deque(), ver
                primero = not any(j["ver"] == ver for j in self.en_curso.values()) and ver not in self.vers_abiertas
                enfoque = self.enfoques.popleft() if self.enfoques else None
                puente = self.ultimo_tema if primero and self.ultimo_tema and self.ultimo_tema != tema else None
                self.vers_abiertas.add(ver)
                paralelo = [j["enfoque"] or j["tema"] for j in self.en_curso.values() if j["ver"] == ver]
                hist = [h[1] for h in self.historial]
                self.seq += 1
                job = {"seq": self.seq, "tema": tema, "ver": ver, "enfoque": enfoque, "t0": time.time()}
                self.en_curso[self.seq] = job
                self.estado = f"escribiendo {len(self.en_curso)} ({self.modelo})"
            # tras un cambio de tema, el primer bloque es corto: el giro llega antes
            n_frases = 4 if primero else 6
            threading.Thread(target=self._trabajo, args=(job, puente, hist, paralelo, n_frases), daemon=True).start()

    def _puede_despachar(self):
        if self.pausado or len(self.en_curso) >= GUIONISTAS:
            return False
        vigentes = [j for j in self.en_curso.values() if j["ver"] == self.tema_ver]
        if len(self.cola) + len(vigentes) >= BUFER + 1:
            return False
        # un segundo guionista solo arranca si hay un subtema para él (si no, escribirían lo mismo)
        return not vigentes or bool(self.enfoques and self.enfoques_ver == self.tema_ver)

    def _trabajo(self, job, puente, hist, paralelo, n_frases):
        seg = None
        try:
            seg = self._producir(job["tema"], puente, hist, job["ver"], enfoque=job["enfoque"], paralelo=paralelo, n_frases=n_frases,
                                 sid=f"b{job['seq']:03d}")
        except Exception as e:                       # nunca se cae el directo: se reintenta
            self._apunta(f"error al producir: {e!r}")
            time.sleep(2)
        with self.cv:
            self.en_curso.pop(job["seq"], None)
            if seg and job["ver"] == self.tema_ver and self.enfoques_ver == job["ver"]:
                for p in seg.get("proximos", []):
                    if len(self.enfoques) < 4:
                        self.enfoques.append(p)
            self.listos[job["seq"]] = seg
            self._entregar()
            self.estado = f"escribiendo {len(self.en_curso)} ({self.modelo})" if self.en_curso else "listo"
            self.cv.notify_all()
        if seg:
            self.tiempos.append(time.time() - job["t0"])
            self._apunta(f"listo {seg['id']} «{seg['titulo']}» ({seg['dur']:.0f} s de voz, hecho en {time.time() - job['t0']:.0f} s"
                         + (f", enfoque «{job['enfoque']}»" if job["enfoque"] else "") + ")")

    def _entregar(self):
        """Pasa a la cola los bloques terminados en orden de despacho (con self.cv tomado)."""
        while True:
            pend = sorted(set(self.listos) | set(self.en_curso))
            if not pend or pend[0] not in self.listos:
                return
            seg = self.listos.pop(pend[0])
            if not seg:
                continue
            if seg["ver"] != self.tema_ver:
                self._apunta(f"bloque «{seg['titulo']}» descartado (cambió el tema mientras se escribía)")
                continue
            self.cola.append(seg)
            nombrado = ", ".join(dict.fromkeys((f["peg"] or {}).get("nombre", "") for f in seg["frases"] if f["peg"]))
            self.historial.append((seg["id"], f"[{seg['tema']}] {seg.get('resumen', '')} (ya enseñado: {nombrado})"))
            self.ultimo_tema = seg["tema"]
            with open(os.path.join(self.carpeta, "guion.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(seg, ensure_ascii=False) + "\n")

    def _producir(self, tema, puente, hist, ver=None, enfoque=None, paralelo=(), n_frases=6, sid="b000"):
        pegs, clips = self.bib.candidatos(tema + (" " + enfoque if enfoque else ""))
        catalogo = self.bib.texto_catalogo(pegs, clips)
        t0 = time.time()
        d, crudo = director.escribir(self.cfg, tema, hist, catalogo, transicion_de=puente, modelo=self.modelo,
                                     carpeta=os.path.join(AQUI, "_sesiones", "_claude"),
                                     vigente=lambda: ver is None or ver == self.tema_ver,
                                     enfoque=enfoque, paralelo=paralelo, n_frases=n_frases)
        if crudo == "cancelado":
            self._apunta("escritura cortada: cambió el tema")
            return None
        if not d:
            self._apunta("el director no devolvió JSON; reintento: " + (crudo or "")[:120].replace("\n", " "))
            return None
        t_guion = time.time() - t0
        frases = d["frases"][:7]
        with cf.ThreadPoolExecutor(6) as ex:
            f_voz = ex.submit(voz.sintetizar, [f["texto"] for f in frases], self.carpeta, sid, self.voz, self.velocidad)
            f_web = {i: ex.submit(self.bib.buscar_web, f.get("buscar") or f.get("etiqueta"))     # respaldo: la etiqueta
                     for i, f in enumerate(frases) if f.get("pegatina") not in self.bib.pegatinas and (f.get("buscar") or f.get("etiqueta"))}
            audios = f_voz.result()
            webs = {i: fu.result() for i, fu in f_web.items()}
        salida, total = [], 0.0
        for i, f in enumerate(frases):
            wav, dur = audios[i]
            peg = None
            if f.get("pegatina") in self.bib.pegatinas:
                v, slug = f["pegatina"].split("/", 1)
                e = self.bib.pegatinas[f["pegatina"]]
                peg = {"url": f"/pv/{v}/{slug}.png", "rec": f"/pv/{v}/_rec/{slug}.png" if e["rec"] else None,
                       "nombre": f.get("etiqueta") or re.sub(r"\s*\(.*?\)", "", e["desc"]) or slug.replace("_", " ")}
            elif webs.get(i):
                peg = {"url": "/web/" + os.path.basename(webs[i]), "rec": None, "nombre": f.get("etiqueta") or f.get("buscar")}
            clip = f.get("clip") if f.get("clip") in self.bib.clips and f.get("clip") not in self.bib.usados[-12:] else self.bib.clip_para(f["texto"])
            if clip:
                self.bib.usar_clip(clip)
            if f.get("pegatina") in self.bib.pegatinas:
                self.bib.peg_usadas.append(f["pegatina"])
            salida.append({"texto": f["texto"], "dur": dur, "audio": "/s/" + os.path.basename(wav) if wav else None,
                           "peg": peg, "clip": f"/cv/{clip}.mp4" if clip else None,
                           "rotulo": (f.get("rotulo") or None),
                           "ficha": f["ficha"] if isinstance(f.get("ficha"), dict) and f["ficha"].get("nombre") else None})
            total += dur + 0.25
        self._apunta(f"{sid}: guion {t_guion:.0f} s · {sum(1 for s in salida if s['peg'])}/{len(salida)} con imagen")
        return {"id": sid, "tema": tema, "titulo": d.get("titulo") or tema, "resumen": d.get("resumen", ""),
                "opciones": [o for o in d.get("opciones", []) if isinstance(o, str)][:3], "frases": salida,
                "proximos": [o for o in d.get("proximos", []) if isinstance(o, str)][:2],
                "dur": total, "puente": bool(puente), "ver": ver, "origen": (self.anuncio or {}).get("origen") if puente else None}

    def estado_json(self):
        with self.cv:
            al = self.al_aire
            return {"canal": self.cfg["nombre"], "tema": self.tema, "tema_ver": self.tema_ver, "bufer": [s["titulo"] for s in self.cola],
                    "bufer_s": round(sum(s["dur"] for s in self.cola)), "estado": self.estado, "pausado": self.pausado,
                    "votacion": self.votacion, "opciones": self.opciones, "votos": self.votos,
                    "al_aire": {"id": al["id"], "titulo": al["titulo"], "tema": al["tema"],
                                "frase": al["frases"][self.frase_al_aire]["texto"] if al and 0 <= self.frase_al_aire < len(al["frases"]) else ""} if al else None,
                    "tiempo_medio": round(sum(self.tiempos) / len(self.tiempos), 1) if self.tiempos else None,
                    "modelo": self.modelo, "anuncio": self.anuncio, "log": list(self.log)[-14:]}


def crear_app(d):
    app = Flask(__name__, static_folder=None)

    @app.get("/")
    def pantalla():
        return send_from_directory(AQUI, "pantalla.html")

    @app.get("/control")
    def control():
        return send_from_directory(AQUI, "control.html")

    @app.get("/api/siguiente")
    def api_siguiente():
        return jsonify(d.siguiente(float(request.args.get("espera", 20))))

    @app.get("/api/estado")
    def api_estado():
        return jsonify(d.estado_json())

    @app.get("/api/ost")
    def api_ost():
        pistas = list(range(len(d.bib.ost)))
        random.shuffle(pistas)
        return jsonify([f"/ost/{i}" for i in pistas])

    @app.post("/api/tema")
    def api_tema():
        d.cambiar_tema((request.get_json(silent=True) or {}).get("tema"))
        return jsonify(ok=True)

    @app.post("/api/votar")
    def api_votar():
        d.votar((request.get_json(silent=True) or {}).get("opcion"))
        return jsonify(ok=True, votos=d.votos)

    @app.post("/api/ajuste")
    def api_ajuste():
        j = request.get_json(silent=True) or {}
        with d.cv:
            if "votacion" in j:
                d.votacion = bool(j["votacion"])
            if "pausado" in j:
                d.pausado = bool(j["pausado"])
            if j.get("modelo") in ("haiku", "sonnet", "opus"):
                d.modelo = j["modelo"]
            d.cv.notify_all()
        return jsonify(ok=True)

    @app.post("/api/progreso")
    def api_progreso():
        j = request.get_json(silent=True) or {}
        if d.al_aire and j.get("id") == d.al_aire["id"]:
            d.frase_al_aire = int(j.get("frase", 0))
        return jsonify(ok=True)

    def _seguro(base, rel):
        ruta = os.path.abspath(os.path.join(base, rel))         # abspath y no realpath: medios/ suele ser junction a D: o E:
        if not ruta.startswith(os.path.abspath(base) + os.sep) or not os.path.isfile(ruta):
            abort(404)
        return ruta

    @app.get("/pv/<v>/<slug>")
    @app.get("/pv/<v>/_rec/<slug>")
    def pegatina(v, slug):
        sub = "_rec" if "/_rec/" in request.path else ""
        return send_file(_seguro(VIDEOS, os.path.join(v, "pegatinas", sub, slug)), max_age=3600)

    @app.get("/fuente/bahnschrift.ttf")
    def fuente():                                   # la letra del kit de Tamriel (mg_tes.fuente): Bahnschrift Condensed
        return send_file(os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "bahnschrift.ttf"), max_age=86400)

    @app.get("/cv/<v>/<sc>")
    def clip(v, sc):
        return send_file(_seguro(VIDEOS, os.path.join(v, "medios", sc)), conditional=True, max_age=3600)

    @app.get("/ost/<int:i>")
    def ost(i):
        if not 0 <= i < len(d.bib.ost):
            abort(404)
        return send_file(d.bib.ost[i], conditional=True, max_age=3600)

    @app.get("/s/<nombre>")
    def audio(nombre):
        return send_file(_seguro(d.carpeta, nombre), max_age=3600)

    @app.get("/web/<nombre>")
    def web(nombre):
        return send_file(_seguro(d.bib.cache, nombre), max_age=3600)

    return app


def abrir(puerto):
    import shutil
    import subprocess
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{puerto}/")
    edge = shutil.which("msedge") or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge):                     # la ventanita de control, como app pequeña
        subprocess.Popen([edge, f"--app=http://127.0.0.1:{puerto}/control", "--window-size=440,820"])
    else:
        webbrowser.open(f"http://127.0.0.1:{puerto}/control")


def main():
    ap = argparse.ArgumentParser(description="EN VIVO: directo generado y editado en tiempo real")
    ap.add_argument("canal", nargs="?", default="cronicas_tamriel", choices=sorted(CANALES))
    ap.add_argument("--tema", default=None)
    ap.add_argument("--modelo", default="sonnet", help="sonnet (por defecto: mejor lore y sarcasmo, 12-17 s por bloque) | haiku (respaldo)")
    ap.add_argument("--voz", default="Raul", help="voz OneCore de Windows: Raul, Sabina (es-MX), Pablo, Helena, Laura (es-ES)")
    ap.add_argument("--velocidad", type=int, default=1, help="-10..10")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("PORT", 8790)))
    ap.add_argument("--abrir", action="store_true", help="abre la pantalla y la ventanita de control")
    a = ap.parse_args()
    d = Directo(a.canal, a.tema, a.modelo, a.voz, a.velocidad)
    print(f"EN VIVO · {d.cfg['nombre']} · tema «{d.tema}»\n  pantalla: http://127.0.0.1:{a.puerto}/\n  control:  http://127.0.0.1:{a.puerto}/control", flush=True)
    if a.abrir:
        threading.Timer(1.0, abrir, args=(a.puerto,)).start()
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)     # sin una línea por cada petición
    crear_app(d).run(host="127.0.0.1", port=a.puerto, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
