# -*- coding: utf-8 -*-
"""Trabajos en segundo plano del Estudio: producir un video (pipeline completo de la Fábrica), vista previa sin voz,
probar una voz y preparar voces clonadas. Un solo trabajo pesado a la vez (cola): la voz usa la GPU y el render
la memoria; correrlos juntos agota la memoria virtual de Windows."""
import glob
import json
import math
import os
import shutil
import subprocess
import sys
import threading
import time
import traceback

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
NUCLEO = os.path.join(RAIZ, "nucleo")
FFMPEG = shutil.which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\ffmpeg\bin\ffprobe.exe"
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)
import proyecto as P  # noqa: E402

try:
    from fab import _CandadoVoz          # mismo candado de GPU que la Fábrica (nunca dos voces a la vez)
except Exception:                         # pragma: no cover
    _CandadoVoz = None

COLA = threading.Lock()                   # un trabajo pesado a la vez
_procesos = {}                            # id_trabajo -> Popen en curso (para cancelar)
_cancelados = set()

# etapa -> (texto para el usuario, peso en la barra)
PASOS = [
    ("voz", "Grabando la narración", 22), ("seleccionar", "Eligiendo las mejores tomas de voz", 12),
    ("tiempo", "Sincronizando voz y animación", 3), ("comprobar", "Revisando las escenas", 3),
    ("musica", "Componiendo la música", 8), ("sfx", "Añadiendo efectos de sonido", 4),
    ("mezcla", "Mezclando el audio", 4), ("video", "Dibujando la animación", 40), ("final", "Últimos toques", 4),
]
MODULOS = {"voz": ["-m", "tts_gen"], "seleccionar": ["-m", "tts_select"], "tiempo": ["-m", "linea_tiempo"],
           "comprobar": ["-m", "comprobar"], "musica": ["-m", "musica"], "sfx": ["-m", "sfx"], "mezcla": ["-m", "mezcla"],
           "video": ["-m", "render", "video"], "final": ["-m", "final"]}


def entorno(carpeta):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([carpeta, AQUI, NUCLEO])
    env["PYTHONIOENCODING"] = "utf-8"
    env["PATH"] = os.path.dirname(FFMPEG) + os.pathsep + env.get("PATH", "")
    return env


_ESTADO = threading.Lock()


def _escribir_estado(carpeta, **kw):
    with _ESTADO:
        _escribir_estado_(carpeta, **kw)


def _escribir_estado_(carpeta, **kw):
    ruta = os.path.join(carpeta, "estado.json")
    prev = leer_estado(carpeta)
    prev.update(kw, t=time.time())
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(prev, f, ensure_ascii=False)
    for intento in range(6):
        try:
            os.replace(tmp, ruta)
            return
        except PermissionError:
            if intento == 5:
                try:
                    with open(ruta, "w", encoding="utf-8") as f:
                        json.dump(prev, f, ensure_ascii=False)
                except Exception:
                    pass
                try:
                    os.remove(tmp)
                except OSError:
                    pass
            else:
                time.sleep(0.04 * (2 ** intento))


def leer_estado(carpeta):
    try:
        with open(os.path.join(carpeta, "estado.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _matar(p):
    if p and p.poll() is None:
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
        else:
            p.kill()


def cancelar(clave):
    _cancelados.add(clave)
    _matar(_procesos.get(clave))


class Cancelado(Exception):
    pass


def _correr(clave, cmd, carpeta, log, gpu=False, descripcion=""):
    """Corre un paso y vuelca su salida al log. Lanza RuntimeError con las últimas líneas si falla."""
    if clave in _cancelados:
        raise Cancelado()
    ctx = _CandadoVoz(f"estudio {descripcion}") if (gpu and _CandadoVoz) else None
    if ctx:
        ctx.__enter__()
    try:
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"\n=== {' '.join(cmd[1:])} ===\n")
            f.flush()
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            p = subprocess.Popen(cmd, cwd=carpeta, env=entorno(carpeta), stdout=f, stderr=subprocess.STDOUT,
                                 creationflags=flags)
            _procesos[clave] = p
            rc = p.wait()
    finally:
        _procesos.pop(clave, None)
        if ctx:
            ctx.__exit__(None, None, None)
    if clave in _cancelados:
        raise Cancelado()
    if rc != 0:
        with open(log, encoding="utf-8", errors="replace") as f:
            cola = f.read()[-1500:]
        raise RuntimeError(f"falló «{descripcion}» (código {rc})\n{cola}")


# ------------------------------------------------------------------ producir un video
def _progreso_paso(carpeta, paso, n_frases):
    """0..1 dentro del paso, deducido de los archivos que va dejando."""
    if paso == "voz":
        return min(1.0, len(glob.glob(os.path.join(carpeta, "voz", "cands", "*.wav"))) / max(1, 2 * n_frases))
    if paso == "video":
        try:
            with open(os.path.join(carpeta, "timeline.json"), encoding="utf-8") as f:
                total = json.load(f)["total"]
            n = math.ceil(total * 30 / 90)
            return min(1.0, len(glob.glob(os.path.join(carpeta, "segmentos", "seg_*.mp4"))) / max(1, n))
        except Exception:
            return 0.0
    return 0.0


def producir(pid, procs=12):
    carpeta = os.path.join(P.PROYECTOS, pid)
    clave = "producir:" + pid
    _cancelados.discard(clave)
    _escribir_estado(carpeta, estado="en_cola", paso=None, pct=0, mensaje="Esperando turno…", error=None,
                     inicio=time.time())
    threading.Thread(target=_producir, args=(pid, carpeta, clave, procs), daemon=True).start()


def _producir(pid, carpeta, clave, procs):
    log = os.path.join(carpeta, "registro.txt")
    with COLA:
        if clave in _cancelados:                       # lo cancelaron mientras esperaba turno
            _cancelados.discard(clave)
            _escribir_estado(carpeta, estado="cancelado", paso=None, pct=0, mensaje="Cancelado")
            return
        n_frases = sum(len(e["frases"]) for e in P.cargar(pid)["escenas"])
        hecho = 0.0
        total_peso = sum(p for _, _, p in PASOS)
        vigilar = {"activo": True, "paso": None, "base": 0.0, "peso": 0}

        def vigia():
            while vigilar["activo"]:
                try:
                    if vigilar["paso"]:
                        u = _progreso_paso(carpeta, vigilar["paso"], n_frases)
                        _escribir_estado(carpeta, pct=round(100 * (vigilar["base"] + u * vigilar["peso"]) / total_peso, 1))
                except Exception:
                    pass
                time.sleep(1.5)
        threading.Thread(target=vigia, daemon=True).start()
        try:
            libre = shutil.disk_usage(carpeta).free / 2 ** 30
            if libre < 1.5:
                raise RuntimeError(f"Queda muy poco espacio en el disco ({libre:.1f} GB). Libera al menos 2 GB y vuelve a intentar.")
            for nombre in ("voz", "timeline.json", "audio", "segmentos", "salida"):   # producción limpia
                ruta = os.path.join(carpeta, nombre)
                if os.path.isdir(ruta):
                    shutil.rmtree(ruta, ignore_errors=True)
                elif os.path.exists(ruta):
                    os.remove(ruta)
            open(log, "w").close()
            py = sys.executable
            for paso, texto, peso in PASOS:
                vigilar.update(paso=paso, base=hecho, peso=peso)
                _escribir_estado(carpeta, estado="produciendo", paso=paso, mensaje=texto,
                                 pct=round(100 * hecho / total_peso, 1))
                if paso == "voz":
                    _correr(clave, [py] + MODULOS["voz"] + ["--seeds", "1", "2"], carpeta, log, gpu=True, descripcion=texto)
                elif paso == "seleccionar":
                    for ronda, seeds in enumerate((None, ["3", "4"], ["5", "6"])):
                        if seeds:
                            with open(os.path.join(carpeta, "voz", "regenerar.json"), encoding="utf-8") as f:
                                reg = json.load(f)
                            if not reg:
                                break
                            _escribir_estado(carpeta, mensaje=f"Repitiendo {len(reg)} frase(s) que no salieron claras")
                            _correr(clave, [py] + MODULOS["voz"] + ["--seeds", *seeds, "--solo", *reg], carpeta, log,
                                    gpu=True, descripcion="regrabar frases")
                        _correr(clave, [py] + MODULOS["seleccionar"], carpeta, log, gpu=True, descripcion=texto)
                    with open(os.path.join(carpeta, "voz", "regenerar.json"), encoding="utf-8") as f:
                        reg = json.load(f)
                    if reg:
                        p = P.cargar(pid)
                        malas = []
                        for k in reg:
                            i, j = k.rsplit("_", 1)
                            try:
                                malas.append(p["escenas"][int(i[1:]) - 1]["frases"][int(j)])
                            except Exception:
                                malas.append(k)
                        raise RuntimeError("La voz no logró decir con claridad estas frases; cámbialas por palabras más "
                                           "sencillas y vuelve a crear el video:\n• " + "\n• ".join(malas))
                elif paso == "video":
                    _correr(clave, [py] + MODULOS["video"] + ["--procs", str(procs)], carpeta, log, descripcion=texto)
                else:
                    _correr(clave, [py] + MODULOS[paso], carpeta, log, descripcion=texto)
                if paso == "tiempo":
                    with open(os.path.join(carpeta, "timeline.json"), encoding="utf-8") as f:
                        total = json.load(f)["total"]
                    if total > P.DURACION_MAX:
                        raise RuntimeError(f"Con la voz, el video dura {total:.0f} segundos y el máximo es 60. "
                                           "Quita una o dos frases y vuelve a crearlo.")
                    _escribir_estado(carpeta, duracion=round(total, 1))
                hecho += peso
            master = sorted(glob.glob(os.path.join(carpeta, "salida", "*_MASTER.mp4")))
            if not master:
                raise RuntimeError("El video no se generó (falta el archivo final).")
            _miniatura(master[0], os.path.join(carpeta, "portada.jpg"))
            shutil.rmtree(os.path.join(carpeta, "segmentos"), ignore_errors=True)       # ahorra disco
            vsa = os.path.join(carpeta, "salida", "video_sin_audio.mp4")
            if os.path.exists(vsa):
                os.remove(vsa)
            _escribir_estado(carpeta, estado="listo", paso=None, pct=100, mensaje="¡Tu video está listo!",
                             video=os.path.relpath(master[0], carpeta).replace(os.sep, "/"), fin=time.time())
        except Cancelado:
            _escribir_estado(carpeta, estado="cancelado", paso=None, mensaje="Cancelado", pct=0)
        except Exception as ex:
            msg = str(ex)
            corto = msg.split("\n")[0] if msg.startswith("falló") else msg
            _escribir_estado(carpeta, estado="error", paso=None, mensaje="Algo salió mal", error=corto,
                             detalle=(msg if msg.startswith("falló") else traceback.format_exc())[-2500:])
        finally:
            vigilar["activo"] = False
            _cancelados.discard(clave)


def _miniatura(video, salida):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "3", "-i", video, "-frames:v", "1", "-vf",
                    "scale=640:-2", salida], capture_output=True,
                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)


# ------------------------------------------------------------------ vista previa sin voz (cuadros sueltos)
def vista_previa(carpeta, n=6):
    """Cuadros del video SIN voz (tiempos estimados) con el mismo motor del render: ~5-20 s."""
    clave = "previa:" + carpeta
    if clave in _procesos:
        return

    def run():
        sal = os.path.join(carpeta, "previews", "muestra")
        shutil.rmtree(sal, ignore_errors=True)
        log = os.path.join(carpeta, "previa_log.txt")
        open(log, "w").close()
        try:
            _correr(clave, [sys.executable, os.path.join(NUCLEO, "muestra_estilo.py"), str(n)], carpeta, log,
                    descripcion="vista previa")
        except Exception as ex:
            os.makedirs(sal, exist_ok=True)
            with open(os.path.join(sal, "estado.json"), "w", encoding="utf-8") as f:
                json.dump(dict(estado="error", error=str(ex)[-600:]), f, ensure_ascii=False)
    threading.Thread(target=run, daemon=True).start()


def estado_previa(carpeta):
    sal = os.path.join(carpeta, "previews", "muestra")
    try:
        with open(os.path.join(sal, "estado.json"), encoding="utf-8") as f:
            est = json.load(f)
    except Exception:
        est = dict(estado="sin_previa")
    if est.get("estado") == "listo":
        try:
            with open(os.path.join(sal, "muestra.json"), encoding="utf-8") as f:
                est["cuadros"] = [c for c in json.load(f)["cuadros"] if c.get("archivo")]
        except Exception:
            est["cuadros"] = []
    return est


# ------------------------------------------------------------------ voces
def preparar_voz(origen, destino):
    """Convierte el audio subido (mp3, wav, m4a, ogg, webm del micrófono…) a la referencia que usa Chatterbox:
    wav mono 24 kHz, sin silencio inicial, volumen normalizado, máx. 20 s. Devuelve la duración en s."""
    r = subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", origen, "-ac", "1", "-ar", "24000", "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1,"
                        "loudnorm=I=-20:TP=-2:LRA=11", "-t", "20", destino], capture_output=True, text=True,
                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    if r.returncode != 0 or not os.path.exists(destino):
        raise RuntimeError("No pude leer ese audio. Prueba con un mp3, wav o m4a.")
    d = duracion(destino)
    if d < 5:
        os.remove(destino)
        raise RuntimeError(f"El audio es muy corto ({d:.1f} s). Necesito entre 8 y 20 segundos de voz clara.")
    return d


def duracion(ruta):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


_prueba_voz = {}


def probar_voz(vid, ref, salida, texto, expr=0.7):
    clave = "voz:" + vid
    _prueba_voz[vid] = dict(estado="trabajando", t=time.time())

    def run():
        log = salida + ".log"
        open(log, "w").close()
        try:
            with COLA:
                _correr(clave, [sys.executable, os.path.join(AQUI, "probar_voz.py"), ref, salida, f"{expr:.2f}", texto],
                        os.path.dirname(salida), log, gpu=True, descripcion="probar voz")
            _prueba_voz[vid] = dict(estado="listo", t=time.time())
        except Exception as ex:
            _prueba_voz[vid] = dict(estado="error", error=str(ex).split("\n")[0])
    threading.Thread(target=run, daemon=True).start()


def estado_prueba_voz(vid):
    return _prueba_voz.get(vid, dict(estado="nada"))


def ocupado():
    """¿Hay un trabajo pesado en marcha? (para avisar en la interfaz)."""
    return COLA.locked()


# ------------------------------------------------------------------ miniaturas de los dibujos (una sola vez)
def miniaturas_iconos(dir_iconos, carpeta_sistema):
    if os.path.isdir(dir_iconos) and len(os.listdir(dir_iconos)) >= 50:
        return

    def run():
        log = os.path.join(carpeta_sistema, "iconos_log.txt")
        try:
            _correr("iconos", [sys.executable, os.path.join(AQUI, "miniaturas_iconos.py"), dir_iconos], carpeta_sistema,
                    log, descripcion="miniaturas de dibujos")
        except Exception:
            pass
    threading.Thread(target=run, daemon=True).start()
