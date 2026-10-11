# -*- coding: utf-8 -*-
"""Avisos por voz del panel: un vigilante detecta cambios en las etapas de los proyectos y un locutor los dice con
Chatterbox (proceso auxiliar avisos_voz.py, cargado solo cuando hace falta) por las bocinas de la PC y/o el navegador.

Configuración en panel_config.json (raíz del repo, no se versiona): activo, destino (bocinas|navegador|ambos), voz,
exaggeration, cfg_weight, temperature, ocioso_min (minutos sin avisos para descargar el modelo) e hitos (% de render).
Los WAV se guardan en panel_avisos/ (caché por texto): un aviso repetido no se vuelve a sintetizar.
"""
import hashlib
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
from collections import deque

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUCLEO = os.path.join(RAIZ, "nucleo")
DIR = os.path.join(RAIZ, "panel_avisos")
CONFIG = os.path.join(RAIZ, "panel_config.json")
INSTANTANEA = os.path.join(DIR, "instantanea.json")
DEFECTO = dict(activo=True, destino="bocinas", voz="C:/chatterbox_voices/Faraon.mp3", exaggeration=0.5,
               cfg_weight=0.4, temperature=0.8, ocioso_min=5, hitos=[25, 50, 75])
_lock = threading.Lock()


def leer_config():
    cfg = dict(DEFECTO)
    try:
        with open(CONFIG, encoding="utf-8") as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass
    if not os.path.isfile(cfg["voz"]):                       # sin la voz elegida: la del narrador
        cfg["voz"] = "C:/chatterbox_voices/Dan.mp3"
    return cfg


def guardar_config(cambios):
    with _lock:
        cfg = leer_config()
        for k in ("activo", "destino"):
            if k in cambios:
                cfg[k] = cambios[k]
        if cfg["destino"] not in ("bocinas", "navegador", "ambos"):
            cfg["destino"] = "bocinas"
        cfg["activo"] = bool(cfg["activo"])
        with open(CONFIG, "w", encoding="utf-8") as f:
            json.dump({k: cfg[k] for k in DEFECTO}, f, ensure_ascii=False, indent=1)
        return cfg


# ======================================================================== texto hablado
_UN = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce",
       "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno",
       "veintidós", "veintitrés", "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
_DEC = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
_CEN = {2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos", 7: "setecientos",
        8: "ochocientos", 9: "novecientos"}


def num_es(n):
    n = int(n)
    if n < 30:
        return _UN[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _DEC[d] + ("" if u == 0 else " y " + _UN[u])
    if n < 1000:
        if n == 100:
            return "cien"
        c, r = divmod(n, 100)
        return ("ciento" if c == 1 else _CEN[c]) + ("" if r == 0 else " " + num_es(r))
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        return ("mil" if m == 1 else num_es(m) + " mil") + ("" if r == 0 else " " + num_es(r))
    return str(n)


def hablar(texto):
    """Números a palabras y símbolos fuera, para que la voz no tropiece."""
    t = re.sub(r"\d+(?:\.\d{3})*", lambda m: num_es(int(m.group().replace(".", ""))), texto)
    t = re.sub(r"(?<![A-Za-z])MB(?![A-Za-z])", "megas", t)
    t = re.sub(r"(?<![A-Za-z])GB(?![A-Za-z])", "gigas", t)
    t = t.replace("%", " por ciento").replace("≈", "").replace("_", " ")
    return re.sub(r"\s+", " ", t).strip()


def minutos_es(seg):
    m = int(round(seg / 60.0))
    if m <= 0:
        return "menos de un minuto"
    return "un minuto" if m == 1 else f"{num_es(m)} minutos"


def nombre_corto(p):
    t = (p.get("titulo") or p["nombre"])
    t = re.split(r"[:—–|(]", t)[0]
    t = re.sub(r"[¿?¡!\"«»]", "", t).strip()
    return " ".join(t.split()[:8]) or p["nombre"]


# ======================================================================== locutor
class Locutor:
    def __init__(self):
        self.cola = queue.Queue()
        self.hist = deque(maxlen=40)
        self._id = 0
        self._mu = threading.Lock()
        self.worker = None
        self.resp = queue.Queue()
        self.modelo = "inactivo"            # inactivo | cargando | listo | error
        self.ultimo_uso = 0.0
        self.ocupado = False
        self.proximo_intento = 0.0
        os.makedirs(DIR, exist_ok=True)
        threading.Thread(target=self._bucle, daemon=True).start()
        threading.Thread(target=self._descargar_ocioso, daemon=True).start()

    # ---- API
    def decir(self, texto, motivo="aviso"):
        with self._mu:
            self._id += 1
            aviso = dict(id=self._id, texto=texto, t=time.time(), estado="generando", audio=None, motivo=motivo)
            self.hist.append(aviso)
        self.cola.put(aviso)
        return aviso["id"]

    def recientes(self, n=12):
        return [dict(a) for a in list(self.hist)[-n:]]

    def info(self):
        cfg = leer_config()
        return dict(activo=cfg["activo"], destino=cfg["destino"], modelo=self.modelo, cola=self.cola.qsize(),
                    voz=os.path.splitext(os.path.basename(cfg["voz"]))[0])

    # ---- proceso de Chatterbox
    def _leer_salida(self, proc):
        for linea in proc.stdout:
            if linea.startswith("@@"):
                self.resp.put(linea[2:].strip())
        self.resp.put("@@FIN")

    def _asegurar_worker(self, cfg):
        if self.worker and self.worker.poll() is None:
            return True
        if time.time() < self.proximo_intento:
            return False
        self.modelo = "cargando"
        env = dict(os.environ, PYTHONPATH=NUCLEO, PYTHONIOENCODING="utf-8")
        try:
            log = open(os.path.join(DIR, "worker_log.txt"), "a", encoding="utf-8")
            self.worker = subprocess.Popen(
                [sys.executable, "-m", "avisos_voz", json.dumps({k: cfg[k] for k in ("voz", "exaggeration", "cfg_weight", "temperature")})],
                cwd=RAIZ, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, text=True,
                encoding="utf-8", bufsize=1, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except OSError:
            self.modelo, self.proximo_intento = "error", time.time() + 60
            return False
        self.resp = queue.Queue()
        threading.Thread(target=self._leer_salida, args=(self.worker,), daemon=True).start()
        fin = time.time() + 240
        while time.time() < fin:
            try:
                m = self.resp.get(timeout=1)
            except queue.Empty:
                w = self.worker
                if w is None or w.poll() is not None:
                    break
                continue
            if m == "LISTO":
                self.modelo = "listo"
                return True
            if m == "FIN":
                break
        self.modelo, self.proximo_intento = "error", time.time() + 60
        self._matar_worker()
        return False

    def _matar_worker(self):
        w, self.worker = self.worker, None
        if w and w.poll() is None:
            try:
                w.stdin.close()
                w.wait(timeout=8)
            except Exception:
                w.kill()

    def _descargar_ocioso(self):
        while True:
            time.sleep(30)
            w = self.worker
            if w and w.poll() is None and self.cola.empty() and not self.ocupado and                     time.time() - self.ultimo_uso > leer_config()["ocioso_min"] * 60:
                self._matar_worker()
                self.modelo = "inactivo"

    def _sintetizar(self, aviso, hablado, cfg):
        """WAV de Chatterbox (en caché si ya existe). Devuelve la ruta o None si falló."""
        clave = hashlib.sha1((hablado + cfg["voz"] + str(cfg["exaggeration"])).encode("utf-8")).hexdigest()[:16]
        ruta = os.path.join(DIR, f"{clave}.wav")
        if os.path.isfile(ruta) and os.path.getsize(ruta) > 2000:
            return ruta
        if not self._asegurar_worker(cfg):
            return None
        try:
            self.worker.stdin.write(json.dumps({"id": aviso["id"], "texto": hablado, "salida": ruta, "seed": 7}) + "\n")
            self.worker.stdin.flush()
        except (OSError, ValueError):
            self.modelo = "error"
            self._matar_worker()
            return None
        fin = time.time() + 150
        while time.time() < fin:
            try:
                m = self.resp.get(timeout=1)
            except queue.Empty:
                if not self.worker or self.worker.poll() is not None:
                    break
                continue
            if m == "FIN":
                break
            try:
                r = json.loads(m)
            except ValueError:
                continue
            if r.get("id") == aviso["id"]:
                return ruta if r.get("ok") and os.path.isfile(ruta) else None
        self._matar_worker()
        self.modelo, self.proximo_intento = "error", time.time() + 60
        return None

    # ---- reproducción
    @staticmethod
    def _tocar_wav(ruta):
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"(New-Object Media.SoundPlayer '{ruta}').PlaySync()"], timeout=180,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    @staticmethod
    def _voz_windows(texto):
        """Respaldo si Chatterbox no está disponible: voz de Windows en español."""
        t = texto.replace("'", " ")
        ps = ("Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              "$v=$s.GetInstalledVoices() | Where-Object {$_.VoiceInfo.Culture.Name -like 'es-*'} | Select-Object -First 1; "
              "if($v){$s.SelectVoice($v.VoiceInfo.Name)}; $s.Speak('" + t + "')")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], timeout=120,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def _bucle(self):
        while True:
            aviso = self.cola.get()
            self.ocupado = True
            self.ultimo_uso = time.time()
            try:
                cfg = leer_config()
                hablado = hablar(aviso["texto"])
                ruta = self._sintetizar(aviso, hablado, cfg)
                self.ultimo_uso = time.time()
                if ruta:
                    aviso["audio"] = os.path.basename(ruta)
                    aviso["estado"] = "listo"
                else:
                    aviso["estado"] = "respaldo"
                if cfg["destino"] in ("bocinas", "ambos"):
                    if ruta:
                        self._tocar_wav(ruta)
                    else:
                        self._voz_windows(hablado)
                elif not ruta:
                    self._voz_windows(hablado)             # solo navegador pero sin audio: que igual se oiga
                aviso["hablado"] = True
            except Exception as e:
                aviso["estado"] = "error"
                aviso["error"] = str(e)[:120]
            finally:
                self.ultimo_uso = time.time()
                self.ocupado = False


# ======================================================================== vigilante de etapas
FRASES = {
    "voz": "la voz está generada", "seleccion": "la selección de voz terminó", "tiempo": "el tiempo está calculado",
    "musica": "la música está lista", "mezcla": "la mezcla de audio está lista", "video": "el render terminó",
    "final": "el video final está listo", "verificar": "la verificación terminó",
    "miniatura": "las miniaturas están listas", "metadatos": "los metadatos están listos",
    "subida": "ya está subido a YouTube",
}
NOMBRES = {"voz": "la voz", "seleccion": "la selección de voz", "tiempo": "el tiempo", "escenas": "las escenas",
           "musica": "la música", "sfx": "los efectos", "mezcla": "la mezcla", "video": "el render",
           "final": "el video final", "verificar": "la verificación", "miniatura": "la miniatura",
           "metadatos": "los metadatos", "subida": "la subida"}


class Vigilante(threading.Thread):
    def __init__(self, obtener_estado, locutor):
        super().__init__(daemon=True)
        self.obtener = obtener_estado
        self.loc = locutor
        self.prev = None
        self.hitos = {}
        self.parado = {}
        self.corriendo = {}
        self.silenciar_primero = False

    def _cargar(self):
        try:
            with open(INSTANTANEA, encoding="utf-8") as f:
                d = json.load(f)
            if time.time() - d.get("t", 0) < 24 * 3600:
                self.prev, self.hitos = d["proyectos"], {k: v for k, v in d.get("hitos", {}).items()}
        except (OSError, ValueError, KeyError):
            pass

    def _guardar(self, actual):
        try:
            with open(INSTANTANEA, "w", encoding="utf-8") as f:
                json.dump(dict(t=time.time(), proyectos=actual, hitos=self.hitos), f, ensure_ascii=False)
        except OSError:
            pass

    @staticmethod
    def _resumen(est):
        out = {}
        for p in est["proyectos"]:
            if not p.get("etapas"):
                continue
            out[p["nombre"]] = dict(
                corto=nombre_corto(p), progreso=p.get("progreso", 0), actual=p.get("etapa_actual"), archivado=bool(p.get("archivado")),
                etapas={k: dict(estado=v["estado"], progreso=v.get("progreso", 0), detalle=v.get("detalle", ""))
                        for k, v in p["etapas"].items()})
        return out

    def paso(self):
        est = self.obtener()
        actual = self._resumen(est)
        if self.prev is None:                                   # primer escaneo sin instantánea: solo línea base
            self.prev = actual
            for v, p in actual.items():
                self._hito(v, p, anunciar=False)
            self._guardar(actual)
            return
        frases = []
        cfg = leer_config()
        cfg_hitos = cfg.get("hitos", [25, 50, 75])
        for v, p in actual.items():
            a = self.prev.get(v)
            c = p["corto"]
            if a is None:                                        # proyecto nuevo
                frases.append(f"Hay un proyecto nuevo: {c}.")
                self._hito(v, p, anunciar=False)
                continue
            listas = [k for k, e in p["etapas"].items()
                      if e["estado"] == "listo" and a["etapas"].get(k, {}).get("estado") != "listo" and k in FRASES]
            if "video" in listas and "final" in listas:
                frases.append(f"{c}: el render y el video final están listos.")
                listas = [k for k in listas if k not in ("video", "final")]
            for k in listas:
                extra = ""
                if k == "tiempo":
                    m = re.search(r"(\d+):(\d\d)", p["etapas"][k]["detalle"])
                    if m:
                        extra = f", dura {minutos_es(int(m.group(1)) * 60 + int(m.group(2)))}"
                if k == "final":
                    m = re.search(r"(\d+) MB", p["etapas"][k]["detalle"])
                    if m:
                        extra = f", pesa {num_es(int(m.group(1)))} megas"
                frases.append(f"{c}: {FRASES[k]}{extra}.")
            for k, e in p["etapas"].items():                     # etapas que piden atención
                if e["estado"] == "atencion" and a["etapas"].get(k, {}).get("estado") != "atencion":
                    det = "; hay frases por regenerar" if k == "seleccion" else ""
                    frases.append(f"Atención en {c}: {NOMBRES.get(k, k)} necesita revisión{det}.")
            # etapa que se detuvo sin terminar (dos escaneos seguidos para no confundir con el cambio entre etapas)
            if p.get("actual"):
                self.corriendo[v] = p["actual"]
                self.parado.pop(v, None)
            elif self.corriendo.get(v):
                ea = self.corriendo[v]
                if p["etapas"].get(ea, {}).get("estado") == "listo":
                    self.corriendo.pop(v, None)
                else:
                    self.parado[v] = self.parado.get(v, 0) + 1
                    if self.parado[v] == 2:
                        frases.append(f"Atención: {NOMBRES.get(ea, ea)} de {c} se detuvo antes de terminar.")
                        self.corriendo.pop(v, None)
            if not p.get("archivado") and a.get("progreso", 0) < 0.999 <= p.get("progreso", 0):
                frases.insert(0, f"{c} quedó completo: todas las etapas están terminadas.")
            hito = self._hito(v, p, anunciar=True, hitos=cfg_hitos)
            if hito:
                frases.append(hito)
        self.prev = actual
        self._guardar(actual)
        if frases and cfg["activo"]:
            self.loc.decir(" ".join(frases[:4]), motivo="etapa")

    def _hito(self, v, p, anunciar, hitos=(25, 50, 75)):
        """Avance del render y de la voz por umbrales de porcentaje. Devuelve la frase o None."""
        salida = None
        for clave, hs, det in (("video", hitos, "el render"), ("voz", (50,), "la voz")):
            e = p["etapas"].get(clave)
            if not e:
                continue
            k = f"{v}:{clave}"
            if e["estado"] == "listo":
                self.hitos[k] = 100
                continue
            pct = e["progreso"] * 100
            m = max([h for h in hs if pct >= h] or [0])
            if m < self.hitos.get(k, 0) and self.hitos.get(k) != 100:
                self.hitos[k] = m                                # reinicio de la etapa
            elif m > self.hitos.get(k, 0) or (self.hitos.get(k) == 100 and pct < 20):
                if self.hitos.get(k) == 100:
                    self.hitos[k] = 0
                else:
                    self.hitos[k] = m
                    if anunciar and m:
                        resta = re.search(r"~(\d+):(\d\d) restantes", e["detalle"])
                        extra = ""
                        if resta:
                            seg = int(resta.group(1)) * 60 + int(resta.group(2))
                            mins = int(round(seg / 60.0))
                            extra = (" Falta menos de un minuto." if seg < 90 else
                                     " Falta aproximadamente un minuto." if mins == 1 else
                                     f" Faltan unos {num_es(mins)} minutos.")
                        salida = f"{p['corto']}: {det} va al {num_es(m)} por ciento.{extra}"
        return salida

    def run(self):
        self._cargar()
        time.sleep(4)
        while True:
            try:
                self.paso()
            except Exception as e:
                print("vigilante:", e, flush=True)
            time.sleep(3)
