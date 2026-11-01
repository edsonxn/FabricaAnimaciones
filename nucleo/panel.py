# -*- coding: utf-8 -*-
"""Panel web local: muestra el avance de las etapas de TODOS los proyectos de videos/ (los nuevos aparecen solos).

    python fab.py panel [--puerto 8765] [--abrir]      ->  http://127.0.0.1:8765

No modifica nada (salvo lanzar el worker de vista previa, ver `preview_worker.py`): solo lee archivos (guion.py, voz/, timeline.json, audio/, segmentos/, salida/, youtube.json,
canales/*.json) y procesos en marcha. Cada etapa se deduce de los archivos que deja:
  guion · voz · selección · tiempo · escenas · música · efectos · mezcla · video · final · verificar ·
  miniatura · metadatos (youtube.json) · subida (canales/*.json -> publicados).
"""
import argparse
import ast
import glob
import json
import math
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import avisos as AV
import uso_panel as UP
VIDEOS = os.path.join(RAIZ, "videos")
CANALES = os.path.join(RAIZ, "canales")
HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel.html")
USO_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_uso.js")     # registrador de uso (ver uso_panel.py)
FPS, TAM_SEG = 30, 90            # deben coincidir con motor.FPS y render.video(tam=90)

ETAPAS = [
    ("guion", "Guion"), ("voz", "Voz"), ("seleccion", "Selección"), ("tiempo", "Tiempo"), ("escenas", "Escenas"),
    ("beats", "Beats"), ("prompts", "Prompts"), ("flow", "Flow"),          # solo motor secuencia (los demás no las tienen)
    ("musica", "Música"), ("sfx", "Efectos"), ("mezcla", "Mezcla"), ("video", "Render"), ("final", "Final"),
    ("verificar", "Verificar"), ("miniatura", "Miniatura"), ("metadatos", "Metadatos"), ("subida", "YouTube"),
]
# módulo de python -> etapa (para reconocer qué corre dentro de `fab.py <video> todo`)
MODULOS = {"tts_gen": "voz", "tts_select": "seleccion", "linea_tiempo": "tiempo", "musica": "musica", "sfx": "sfx",
           "mezcla": "mezcla", "render": "video", "final": "final", "verificar": "verificar", "miniatura": "miniatura"}
ETAPA_FAB = {"voz": "voz", "seleccionar": "seleccion", "tiempo": "tiempo", "musica": "musica", "sfx": "sfx",
             "mezcla": "mezcla", "video": "video", "final": "final", "verificar": "verificar",
             "miniatura": "miniatura", "comprobar": "escenas", "escena": "escenas", "prueba": "escenas",
             "fx": "sfx", "beats": "beats", "prompts": "prompts", "servir": "flow", "ingesta": "flow", "medios": "flow", "bajar": "flow", "busquedas": "flow", "fuentes": "flow", "ambiente": "video"}


# ======================================================================== utilidades
def mt(ruta):
    try:
        return os.path.getmtime(ruta)
    except OSError:
        return 0.0


def existe(ruta):
    return os.path.isfile(ruta)


def contar(carpeta, patron=None, excluir=None):
    n = 0
    try:
        for e in os.scandir(carpeta):
            if e.is_file() and (patron is None or re.search(patron, e.name)) and \
                    (excluir is None or not re.search(excluir, e.name)):
                n += 1
    except OSError:
        pass
    return n


def leer_json(ruta, defecto=None):
    try:
        with open(ruta, encoding="utf-8-sig") as f:      # -sig: un JSON guardado con BOM (PowerShell 5.1) no desaparece del panel
            return json.load(f)
    except Exception:
        return defecto


def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def parsear_guion(ruta):
    """Lee TITULO, ESTILO_VISUAL, DURACION, FORMATO, ARCHIVO y ESCENAS de guion.py sin ejecutarlo."""
    datos = {}
    try:
        arbol = ast.parse(open(ruta, encoding="utf-8").read())
    except Exception:
        return datos
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 and isinstance(nodo.targets[0], ast.Name):
            try:
                datos[nodo.targets[0].id] = ast.literal_eval(nodo.value)
            except Exception:
                v = nodo.value               # VOZ = dict(motor="elevenlabs", tomas=1, ...): sin esto el panel suponía 4 tomas
                if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "dict" and not v.args:
                    d = {}
                    for kw in v.keywords:
                        try:
                            d[kw.arg] = ast.literal_eval(kw.value)
                        except Exception:
                            pass
                    datos[nodo.targets[0].id] = d
    return datos


# ======================================================================== procesos y sistema
_cache = {"t": 0.0, "procs": [], "gpu": None}
_lock = threading.Lock()


def _refrescar_sistema():
    procs = []
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId,ParentProcessId,CommandLine,"
             "@{n='T';e={[int64]([datetimeoffset]$_.CreationDate).ToUnixTimeSeconds()}} "      # T = epoch de arranque
             "| ConvertTo-Json -Compress"], capture_output=True, text=True, timeout=15, encoding="utf-8",
            errors="replace", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        d = json.loads(r.stdout) if r.stdout.strip() else []
        procs = [d] if isinstance(d, dict) else d
    except Exception:
        procs = []
    gpu = None
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
                            "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=8,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        u, m, tot = [float(x) for x in r.stdout.strip().split("\n")[0].split(",")]
        gpu = dict(uso=u, mem=m, mem_total=tot)
    except Exception:
        pass
    with _lock:
        _cache.update(t=time.time(), procs=procs, gpu=gpu)


def sistema(forzar=False):
    if forzar or time.time() - _cache["t"] > 5:
        _refrescar_sistema()
    with _lock:
        return list(_cache["procs"]), _cache["gpu"]


def etapas_en_curso(procs, videos):
    """{video: etapa} según las líneas de comando de los procesos python en marcha."""
    activo = {}
    todos = []
    for p in procs:
        cmd = (p.get("CommandLine") or "")
        m = re.search(r"fab\.py\s+(\S+)\s+(\S+)", cmd)
        if m and m.group(1) in videos:
            v, et = m.group(1), m.group(2)
            if et == "todo":
                todos.append(v)
                activo.setdefault(v, "guion")
            elif et in ETAPA_FAB:
                activo[v] = ETAPA_FAB[et]
            continue
    hijos = set()
    for p in procs:
        cmd = (p.get("CommandLine") or "")
        m = re.search(r"-m\s+(tts_gen|tts_select|linea_tiempo|musica|sfx|mezcla|final|render|verificar|miniatura)\b",
                      cmd)
        if m:
            hijos.add(MODULOS[m.group(1)])
    if len(todos) == 1 and hijos:                # `todo` de un solo video: la etapa la dan sus hijos
        activo[todos[0]] = sorted(hijos, key=[e for e, _ in ETAPAS].index)[-1]
    return activo


# ======================================================================== registro de lo publicado
def publicados():
    out = {}
    for ruta in glob.glob(os.path.join(CANALES, "*.json")):
        d = leer_json(ruta, {})
        if not isinstance(d, dict):
            continue
        for p in d.get("publicados", []) or []:
            if isinstance(p, dict) and p.get("video"):
                out[p["video"]] = dict(p, canal=d.get("nombre") or os.path.basename(ruta)[:-5])
    return out


def canales_suspendidos():
    """Alias de canales/<alias>.json con `"suspendido"` (el usuario pausó el canal): sus proyectos nacen ocultos
    y el canal sale del filtro del panel (salvo con «Ocultos»)."""
    out = set()
    for ruta in glob.glob(os.path.join(CANALES, "*.json")):
        d = leer_json(ruta, {})
        if isinstance(d, dict) and d.get("suspendido"):
            out.add(os.path.basename(ruta)[:-5])
    return out


# ======================================================================== registros de texto
def limpiar_log(txt, n=6):
    lineas = []
    for l in re.split(r"[\r\n]+", txt):
        l = l.strip()
        if not l or "it/s" in l or "s/it" in l or re.search(r"\d+%\|", l) or "Warning" in l or "warn" in l:
            continue
        lineas.append(l[:170])
    return lineas[-n:]


def ultimo_log(carpeta):
    logs = [p for p in glob.glob(os.path.join(carpeta, "*.txt")) if re.search(r"log", os.path.basename(p))]
    if not logs:
        return None, []
    ruta = max(logs, key=mt)
    try:
        with open(ruta, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 6000))
            txt = f.read().decode("utf-8", errors="replace")
    except OSError:
        return None, []
    return os.path.basename(ruta), limpiar_log(txt)


def eta_render(carpeta):
    """(hechos, total, transcurrido s) del último render, leyendo '[k/n] ... (transcurrido Ns)' en los logs."""
    mejor = None
    for ruta in glob.glob(os.path.join(carpeta, "*.txt")):
        try:
            with open(ruta, "rb") as f:
                f.seek(0, os.SEEK_END)
                f.seek(max(0, f.tell() - 4000))
                txt = f.read().decode("utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(r"\[(\d+)/(\d+)\].*transcurrido (\d+)s", txt):
            cand = (mt(ruta), int(m.group(1)), int(m.group(2)), int(m.group(3)))
            if mejor is None or cand[0] >= mejor[0]:
                mejor = cand
    return mejor[1:] if mejor else None


# ======================================================================== voz y selección en vivo (tts_gen / tts_select)
# Igual que el render: todo sale de disco (voz/cands, voz/eval.json, voz/final, voz/regenerar.json) y de la línea de comandos del
# proceso hijo (`-m tts_gen --seeds ... --solo ...`), así que vale aunque la etapa se haya lanzado desde cualquier terminal.
CER_OK = 0.012                                           # = tts_select.CER_MAX (solo para pintar las tomas; quien decide es tts_select)
_RE_TOMA = re.compile(r"^(.+)_s(\d+)\.wav$")
_dur_wav = {}                                            # {(ruta, mtime): segundos}
_muestras_sel = {}                                       # {(video, pid): [(t, tomas evaluadas)]}  ritmo de la evaluación de Whisper


def proceso_hijo(procs, video, modulo, etapas_fab):
    """(proceso `-m <modulo>` de `fab.py <video> <etapa>`, ¿hay un fab.py de ese video en marcha?)."""
    padres = set()
    for p in procs:
        m = re.search(r"fab\.py\s+(\S+)\s+(\S+)", p.get("CommandLine") or "")
        if m and m.group(1) == video and m.group(2) in etapas_fab:
            padres.add(p.get("ProcessId"))
    hijos = [p for p in procs if re.search(rf"-m\s+{modulo}\b", p.get("CommandLine") or "")]
    propios = [p for p in hijos if p.get("ParentProcessId") in padres]
    if propios:
        return propios[0], True
    # la GPU de voz es de uno a la vez (fab.py: _CandadoVoz): si solo hay un hijo y el padre es este video, es el suyo
    return (hijos[0] if len(hijos) == 1 and padres else None), bool(padres)


def _args(cmd, flag):
    m = re.search(rf"{flag}((?:\s+[^\s-][^\s]*)+)", cmd or "")
    return m.group(1).split() if m else None


def _segundos_wav(ruta, mtime):
    k = (ruta, mtime)
    if k not in _dur_wav:
        try:
            import wave
            with wave.open(ruta, "rb") as w:
                _dur_wav[k] = w.getnframes() / float(w.getframerate())
        except Exception:                                # noqa: BLE001  (wav a medio escribir o float32 que wave no abre)
            try:
                import soundfile as sf
                _dur_wav[k] = sf.info(ruta).duration
            except Exception:                            # noqa: BLE001
                _dur_wav[k] = 0.0
    return _dur_wav[k]


def _frases_voz(car, g):
    """[(escena, key, texto)] en el orden del guion (textos.json si ESCENAS no se puede leer sin ejecutar guion.py)."""
    out = [(e["id"], f"{e['id']}_{i}", t) for e in (g.get("ESCENAS") or []) if isinstance(e, dict) and e.get("id")
           for i, t in enumerate(e.get("frases", []))]
    if out:
        return out
    tx = leer_json(os.path.join(car, "voz", "textos.json"), {}) or {}
    return [(k.rsplit("_", 1)[0], k, t) for k, t in tx.items()]


def _ritmo(tiempos):
    """Segundos por unidad a partir de los mtimes de lo terminado (mediana de los últimos intervalos)."""
    ts = sorted(tiempos)[-12:]
    if len(ts) < 2:
        return None
    dif = sorted(b - a for a, b in zip(ts, ts[1:]))
    return max(0.2, dif[len(dif) // 2])


def _tomas(car):
    """{key: {seed: (ruta, mtime)}} de voz/cands."""
    out = {}
    try:
        for e in os.scandir(os.path.join(car, "voz", "cands")):
            m = _RE_TOMA.match(e.name)
            if m and e.is_file():
                out.setdefault(m.group(1), {})[int(m.group(2))] = (e.path, e.stat().st_mtime)
    except OSError:
        pass
    return out


def _corto(t, n=70):
    t = re.sub(r"\[[^\]]*\]\s*", "", str(t)).strip()            # sin corchetes de actuación
    return t if len(t) <= n else t[:n - 1] + "…"


def cola_voz(procs, nombre):
    """Texto mientras `fab.py` espera la GPU de voz (otro proyecto la usa: voz_gpu.lock dice quién) o arranca el proceso hijo."""
    try:
        with open(os.path.join(RAIZ, "voz_gpu.lock"), encoding="utf-8", errors="replace") as f:
            quien = "".join(c for c in f.read(200) if c.isprintable()).strip()
    except OSError:
        quien = ""
    v = quien.split()[0] if quien else ""
    vivo = v and v != nombre and any(re.search(rf"fab\.py\s+{re.escape(v)}\s", p.get("CommandLine") or "") for p in procs)
    return f"en cola: la GPU de voz la usa «{quien}»; empieza cuando termine" if vivo else "arrancando (cargando el proceso)…"


def info_voz(car, g, proc, ahora=None):
    """Avance en vivo de `tts_gen`: tomas hechas/por hacer, la que se genera ahora, ritmo, hora de término y una fila por
    escena (o por frase, si se regeneran pocas con --solo)."""
    ahora = ahora or time.time()
    cmd = proc.get("CommandLine") or ""
    t_ini = float(proc.get("T") or ahora)
    seeds = [int(s) for s in (_args(cmd, "--seeds") or ["1", "2", "3", "4"]) if s.isdigit()]
    solo = _args(cmd, "--solo")
    frases = _frases_voz(car, g)
    obj = [f for f in frases if not solo or f[1] in solo]
    tomas = _tomas(car)
    hechos, nuevos, actual, durs = 0, [], None, 0.0
    for esc, key, _ in obj:
        for s in seeds:
            r = tomas.get(key, {}).get(s)
            if r:
                hechos += 1
                if r[1] >= t_ini - 2:
                    nuevos.append(r[1])
                    durs += _segundos_wav(r[0], r[1])
            elif actual is None:
                actual = (key, s)
    total = len(obj) * len(seeds)
    spt = _ritmo(nuevos)
    eta = (max(nuevos) + (total - hechos) * spt) if spt and actual else None
    ultima = None
    if nuevos:
        k, s, (ruta, m) = max(((k, s, v) for k, d in tomas.items() for s, v in d.items() if v[1] >= t_ini - 2), key=lambda x: x[2][1])
        ultima = dict(nombre=f"{k}_s{s}", dur=_segundos_wav(ruta, m), t=m)
    texto = {k: t for _, k, t in frases}
    if actual:
        n_fr = [k for _, k, _ in obj].index(actual[0]) + 1
        ahora_txt = (f"generando la frase {n_fr}/{len(obj)} ({actual[0]}, toma s{actual[1]}): «{_corto(texto.get(actual[0], ''))}»"
                     if nuevos or ahora - t_ini > 90 else "cargando el modelo de voz…")
    else:
        ahora_txt = "terminando…"

    def celda(key, s):
        r = tomas.get(key, {}).get(s)
        return ("n" if r[1] >= t_ini - 2 else "r") if r else ("f" if actual == (key, s) else "-")

    filas = []
    if len(obj) <= 14:                                   # pocas frases (--solo): una fila por frase, un cuadrito por toma
        for i, (esc, key, t) in enumerate(obj):
            cel = "".join(celda(key, s) for s in seeds)
            h = sum(c in "nr" for c in cel)
            filas.append(dict(n=i + 1, nombre=key, info=f"{len(seeds)} tomas", celdas=cel, tip=_corto(t, 200),
                              estado="lista" if h == len(seeds) else "en_curso" if "f" in cel else "pendiente",
                              st=f"{h}/{len(seeds)} tomas"))
    else:                                                # video completo: una fila por escena, un cuadrito por frase
        orden = []
        for esc, key, t in obj:
            if not orden or orden[-1][0] != esc:
                orden.append((esc, []))
            orden[-1][1].append(key)
        for i, (esc, keys) in enumerate(orden):
            cel, listas = "", 0
            for key in keys:
                c = [celda(key, s) for s in seeds]
                listas += all(x in "nr" for x in c)
                cel += "f" if "f" in c else "n" if all(x == "n" for x in c) else "r" if all(x in "nr" for x in c) \
                    else "p" if any(x in "nr" for x in c) else "-"
            filas.append(dict(n=i + 1, nombre=esc, info=f"{len(keys)} frases", celdas=cel, tip="",
                              estado="lista" if listas == len(keys) else "en_curso" if "f" in cel else "pendiente",
                              st=f"{listas}/{len(keys)} frases"))
    chips = [["Tomas", f"{hechos}/{total}"], ["Frases", f"{len(obj)}" + (f" de {len(frases)} (solo las que se regeneran)" if solo else "")],
             ["Semillas", " ".join(f"s{s}" for s in seeds)], ["Transcurrido", "@el"]]
    if spt:
        chips.append(["Ritmo", f"1 toma cada {spt:.1f} s".replace(".", ",")])
    if durs:
        chips.append(["Audio generado", mmss(durs)])
    if ultima:
        chips.append(["Última", f"{ultima['nombre']} · {ultima['dur']:.1f} s".replace(".", ",")])
    vz = g.get("VOZ") if isinstance(g.get("VOZ"), dict) else {}
    chips.append(["Motor", "ElevenLabs" if vz.get("motor") == "elevenlabs" else "Chatterbox"])
    return dict(etapa="voz", titulo="Voz en vivo", t_ini=t_ini, ahora=ahora_txt, hechos=hechos, total=total, eta_fin=eta,
                unidad="tomas", chips=chips, filas=filas, ultimo=max(nuevos) if nuevos else None,
                ayuda="Cada cuadrito es " + ("una toma (semilla)" if len(obj) <= 14 else "una frase") +
                      ": verde = generada ahora, verde tenue = ya estaba, mitad = algunas tomas, parpadea = generándose, gris = pendiente.")


def info_seleccion(car, g, proc, nombre, ahora=None):
    """Avance en vivo de `tts_select`: 1) Whisper evalúa cada toma nueva, 2) elige la mejor por frase, 3) limpia y alinea
    palabras (voz/final/<key>.wav)."""
    ahora = ahora or time.time()
    t_ini = float(proc.get("T") or ahora)
    frases = _frases_voz(car, g)
    tomas = _tomas(car)
    nombres = sorted(f"{k}_s{s}.wav" for k, d in tomas.items() for s in d)
    ev_p = os.path.join(car, "voz", "eval.json")
    ev = leer_json(ev_p, None)
    if ev is None:                                       # a medio escribir: el último bueno
        ev = _muestras_sel.get(("ev", nombre), {})
    _muestras_sel[("ev", nombre)] = ev
    pend = [n for n in nombres if n not in ev]
    reg_p = os.path.join(car, "voz", "regenerar.json")
    reg = leer_json(reg_p, []) if mt(reg_p) >= t_ini - 2 else None
    finales = {}
    try:
        for e in os.scandir(os.path.join(car, "voz", "final")):
            if e.name.endswith(".wav") and e.stat().st_mtime >= t_ini - 2:
                finales[e.name[:-4]] = e.stat().st_mtime
    except OSError:
        pass
    # ritmo de la evaluación: muestras (t, evaluadas) que va tomando el panel (eval.json no guarda horas)
    clave = (nombre, proc.get("ProcessId"))
    mu = [x for x in _muestras_sel.get(clave, []) if x[0] > ahora - 180] + [(ahora, len(nombres) - len(pend))]
    _muestras_sel[clave] = mu
    eta = None
    if pend:
        ev_n = len(nombres) - len(pend)
        hechos, total, unidad = ev_n, len(nombres), "tomas evaluadas"
        if mt(ev_p) < t_ini - 2 and ahora - t_ini < 600 and len({x[1] for x in mu}) < 2:
            fase, ahora_txt = "carga", "cargando Whisper large-v3 y la voz de referencia…"
        else:
            fase = "evalua"
            k = _RE_TOMA.match(pend[0])
            ahora_txt = f"1/3 · Whisper escucha la toma {pend[0][:-4]}: «{_corto(dict((x[1], x[2]) for x in frases).get(k.group(1) if k else '', ''))}»"
        if mu[-1][1] > mu[0][1] and mu[-1][0] > mu[0][0]:
            eta = ahora + len(pend) * (mu[-1][0] - mu[0][0]) / (mu[-1][1] - mu[0][1])
    elif reg is None:
        fase, ahora_txt = "elige", "2/3 · eligiendo la mejor toma de cada frase…"
        hechos, total, unidad = 0, max(1, len(frases)), "frases alineadas"
    else:
        fase = "alinea"
        objetivo = max(1, len(frases) - len(reg))
        hechos, total, unidad = min(len(finales), objetivo), objetivo, "frases alineadas"
        sig = next((k for _, k, _ in frases if k not in finales and k not in reg), None)
        ahora_txt = (f"3/3 · limpiando y alineando palabra por palabra: {sig}" if sig else "3/3 · guardando palabras.json…")
        spt = _ritmo(finales.values())
        if spt and sig:
            eta = max(finales.values()) + (objetivo - hechos) * spt
    # filas: una por escena, un cuadrito por toma (verde = Whisper la entiende bien, rojo = con errores, gris = sin evaluar)
    pend_s = set(pend)
    orden = []
    for esc, key, t in frases:
        if not orden or orden[-1][0] != esc:
            orden.append((esc, []))
        orden[-1][1].append(key)
    filas, malas_tot, ok_tot = [], 0, 0
    for i, (esc, keys) in enumerate(orden):
        cel, ok_f, malas, regen = "", 0, 0, []
        for key in keys:
            for s in sorted(tomas.get(key, {})):
                n = f"{key}_s{s}.wav"
                m = ev.get(n)
                if n in pend_s:
                    cel += "f" if pend and n == pend[0] else "-"
                elif m and m.get("cer", 1) <= CER_OK:
                    cel += "n"
                else:
                    cel += "x"
                    malas += 1
            cel += "|"
            if key in finales:
                ok_f += 1
            if reg and key in reg:
                regen.append(key)
        ok_tot += ok_f
        malas_tot += malas
        st = (f"{ok_f}/{len(keys)} alineadas" if fase == "alinea" else f"{malas} tomas con errores" if malas else "sin errores") + \
             (f" · regenerar {', '.join(regen)}" if regen else "")
        estado = "error" if regen else "lista" if (fase == "alinea" and ok_f == len(keys)) else \
            "en_curso" if "f" in cel or (fase == "alinea" and 0 < ok_f < len(keys)) else "pendiente"
        filas.append(dict(n=i + 1, nombre=esc, info=f"{len(keys)} frases", celdas=cel.rstrip("|"), tip="", estado=estado, st=st))
    chips = [["Tomas evaluadas", f"{len(nombres) - len(pend)}/{len(nombres)}"], ["Con errores", str(malas_tot)],
             ["Transcurrido", "@el"]]
    if len(mu) >= 2 and mu[-1][1] > mu[0][1] and pend:
        chips.append(["Ritmo", f"{(mu[-1][1] - mu[0][1]) / (mu[-1][0] - mu[0][0]) * 60:.0f} tomas/min"])
    if reg is not None:
        chips.append(["Frases que pasan", f"{len(frases) - len(reg)}/{len(frases)}"])
        chips.append(["Regenerar", ", ".join(reg) if reg else "ninguna"])
    return dict(etapa="seleccion", titulo="Selección en vivo", t_ini=t_ini, ahora=ahora_txt, hechos=hechos, total=total,
                eta_fin=eta, unidad=unidad, chips=chips, filas=filas, fase=fase,
                ayuda="Pasos: 1) Whisper escucha cada toma nueva, 2) se elige la mejor por frase, 3) se limpia y se alinea palabra "
                      "por palabra. Cada cuadrito es una toma: verde = Whisper la transcribe bien (CER ≤ 1,2 %), rojo = con errores, "
                      "parpadea = escuchándola, gris = sin evaluar; las rayitas separan frases.")


# ======================================================================== render en vivo (avance real por segmento y por escena)
# Todo sale de los archivos de segmentos/ (el render puede haberse lanzado desde cualquier terminal): en Windows st_ctime es la
# creación del archivo = inicio de la codificación del segmento (os.replace del .tmp lo conserva) y st_mtime = su final.
SEG_S = TAM_SEG / FPS                                    # segundos de video por segmento
_RE_SEG = re.compile(r"^seg_(\d+)\.mp4(\.tmp\.mp4)?$")
try:
    import cache_escenas as CE
except Exception:                                        # noqa: BLE001  (sin él solo se pierde el aviso «ya se ve fluida»)
    CE = None


def inicio_render(procs, video):
    """Epoch (s) en que arrancó el render de `video`: el `-m render` hijo de `fab.py <video> video|todo` (o ese fab.py)."""
    padres = {}
    for p in procs:
        m = re.search(r"fab\.py\s+(\S+)\s+(\S+)", p.get("CommandLine") or "")
        if m and m.group(1) == video and m.group(2) in ("video", "todo"):
            padres[p.get("ProcessId")] = p.get("T")
    hijos = [p.get("T") for p in procs if p.get("ParentProcessId") in padres and p.get("T")
             and re.search(r"-m\s+render\b", p.get("CommandLine") or "")]
    if hijos:
        return float(min(hijos))
    ts = [t for t in padres.values() if t]
    return float(min(ts)) if ts else None


def leer_segmentos(car, t_ini):
    """({k: (ctime, mtime, bytes)} de los terminados, {k: ctime} de los que se están escribiendo)."""
    listos, vuelo = {}, {}
    try:
        for e in os.scandir(os.path.join(car, "segmentos")):
            m = _RE_SEG.match(e.name)
            if not m or not e.is_file():
                continue
            st, k = e.stat(), int(m.group(1))
            if m.group(2):
                if st.st_ctime >= t_ini - 5:             # un .tmp huérfano de un render viejo no cuenta
                    vuelo[k] = st.st_ctime
            elif st.st_size > 1000:
                listos[k] = (st.st_ctime, st.st_mtime, st.st_size)
    except OSError:
        pass
    return listos, vuelo


def calcular_render(escenas, nframes, listos, vuelo, t_ini, ahora, aptos=None):
    """Avance del render a partir de lo que hay en disco. Función pura (se puede probar «reproduciendo» un render ya hecho).

    Estimación: los procesos (W) se miden por cuántos segmentos se solapan en el tiempo; el costo de un segmento es el promedio
    de los últimos terminados (mtime - ctime); lo que falta se mide en «segmentos enteros» (los que se están escribiendo cuentan
    por lo que les queda) y rinde W / costo por segundo. Lo que cambia sin parar (hora de término) va en `vivo`; el resto solo
    cambia al empezar o terminar un segmento, para que el panel no se repinte a cada rato."""
    total = math.ceil(nframes / TAM_SEG)
    nuevos = {k: v for k, v in listos.items() if v[0] >= t_ini - 2}      # los demás los reutiliza el render (ya existían)
    ev = [(c, 1) for c, _, _ in nuevos.values()] + [(m - 0.5, -1) for _, m, _ in nuevos.values()] + [(c, 1) for c in vuelo.values()]
    cur = mx = 0
    for _, d in sorted(ev, key=lambda x: (x[0], x[1])):                # a la misma hora primero terminan, luego empiezan
        cur += d
        mx = max(mx, cur)
    W = max(mx, len(vuelo), 1)
    ds = [m - c for c, m, _ in sorted(nuevos.values(), key=lambda v: v[1])]
    rec = ds[-max(2 * W, 8):]
    costo = sum(rec) / len(rec) if rec else None

    def falta(k_max):
        """Segundos hasta que estén listos todos los segmentos <= k_max."""
        if not costo:
            return None
        resto, cola = 0.0, 0.0
        for k in range(min(k_max, total - 1) + 1):
            if k in listos:
                continue
            if k in vuelo:
                e = ahora - vuelo[k]
                resto += max(0.15, 1 - e / costo)
                cola = max(cola, costo - e, 0.15 * costo)
            else:
                resto += 1
        return max(resto * costo / W, cola)

    filas, esc_fin = [], {}
    for i, e in enumerate(escenas):
        i0, i1 = int(round(e["t0"] * FPS)), min(nframes, int(round(e["t1"] * FPS)))
        k0 = max(0, i0 // TAM_SEG)
        k1 = max(k0 + 1, min(total, -(-i1 // TAM_SEG)))
        ks = range(k0, k1)
        celdas = "".join(("r" if k not in nuevos else "d") if k in listos else ("f" if k in vuelo else "p") for k in ks)
        hechos = sum(1 for k in ks if k in listos)
        estado = ("lista" if hechos == len(ks) else "en_curso" if any(k in vuelo for k in ks)
                  else "parcial" if hechos else "pendiente")
        fluida = estado == "lista" and (aptos is None or all(k in aptos for k in ks))
        f = falta(k1 - 1) if estado != "lista" else None
        if f is not None:
            esc_fin[e["id"]] = ahora + f
        nombre = e.get("titulo") or str(e["id"]).replace("_", " ")
        filas.append(dict(id=e["id"], n=i + 1, nombre=nombre[:1].upper() + nombre[1:], t0=round(e["t0"], 2), t1=round(e["t1"], 2),
                          k0=k0, k1=k1, celdas=celdas, hechos=hechos, estado=estado, fluida=fluida,
                          vieja=estado == "lista" and not fluida))
    f_total = falta(total - 1) if len(listos) < total else 0.0
    return dict(
        t_ini=t_ini, total=total, hechos=len(listos), reusados=len(listos) - len(nuevos), vuelo=sorted(vuelo), procs=W,
        seg_s=round(costo, 1) if costo else None, ritmo=round(costo / W / SEG_S, 2) if costo else None,
        duracion=round(nframes / FPS, 1), video_s=round(min(nframes / FPS, len(listos) * SEG_S), 1),
        mb=round(sum(v[2] for v in listos.values()) / 1e6, 1), fase="uniendo" if len(listos) >= total else "dibujando",
        ahora_en=[f["id"] for f in filas if "f" in f["celdas"]], escenas=filas,
        vivo=dict(ahora=ahora, eta_fin=(ahora + f_total) if f_total is not None else None, esc_fin=esc_fin))


_prearmado = {"hilo": None, "fallas": {}}               # (car, id) -> nº de fallas


def prearmar(car, tl, r):
    """Mientras corre el render completo, arma en segundo plano (ffmpeg en prioridad baja, 2 hilos, de una en una) el mp4 de
    la vista previa de cada escena que ya quedó completa: así «▶ Ver fluida» la reproduce al instante en vez de esperar ~15 s."""
    if CE is None or not r or (_prearmado["hilo"] and _prearmado["hilo"].is_alive()):
        return
    listas = [e for e in r["escenas"] if e["fluida"] and _prearmado["fallas"].get((car, e["id"]), 0) < 2]
    if not listas:
        return
    try:
        hechas = {e["id"] for e in CE.listar(car, NUCLEO) if e["estado"] == "vigente"}
    except Exception:                                    # noqa: BLE001
        return
    pend = [e for e in listas if e["id"] not in hechas]
    if not pend:
        return
    e = pend[0]
    nframes = int(round(float(tl["total"]) * FPS))

    def hilo():
        try:
            w = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                                    "-of", "csv=p=0", CE.ruta_seg(car, e["k0"])], capture_output=True, text=True,
                                   creationflags=0x08000000 if os.name == "nt" else 0).stdout.strip() or 1920)
            CE.empaquetar_escena(car, e["id"], e["k0"], e["k1"], nframes, FPS, 960, w, CE.firma_codigo(car, NUCLEO),
                                 hilos=2, baja_prioridad=True)
        except Exception:                                # noqa: BLE001  (si falla, «Ver fluida» la arma como antes)
            _prearmado["fallas"][(car, e["id"])] = _prearmado["fallas"].get((car, e["id"]), 0) + 1

    _prearmado["hilo"] = threading.Thread(target=hilo, daemon=True)
    _prearmado["hilo"].start()


def info_render(car, tl, t_proc, ahora=None):
    """Avance del render en curso de un video (ver `calcular_render`); None si el timeline no tiene escenas."""
    escenas = tl.get("escenas") or []
    if not escenas or not tl.get("total"):
        return None
    nframes = int(round(float(tl["total"]) * FPS))
    parcial = leer_json(os.path.join(car, "segmentos", "parcial.json"), {}) or {}     # `fab.py <v> video --hasta S` (nucleo/render_parcial.py)
    if parcial.get("nframes"):                           # render parcial: el avance se mide solo sobre ese tramo
        nframes = min(nframes, int(parcial["nframes"]))
        escenas = [e for e in escenas if e["t0"] * FPS < nframes]
    ahora = ahora or time.time()
    t_ini = t_proc or ahora
    listos, vuelo = leer_segmentos(car, t_ini)
    aptos = limite = edicion = None
    if CE is not None and listos:                        # ¿la vista previa podría reutilizarlos sin dibujar? (ver cache_escenas.sin_dibujar)
        try:
            nucleo = os.path.dirname(os.path.abspath(__file__))
            aptos = set(CE.sin_dibujar(car, nucleo, sorted(listos)))
            limite = round(CE.limite_adopcion(car, nucleo))
            ult = max((a for a in CE.archivos_render(car, nucleo) + [os.path.join(car, "timeline.json")] if os.path.isfile(a)), key=mt)
            edicion = [os.path.basename(ult), round(mt(ult))]
        except Exception:                                # noqa: BLE001
            aptos = limite = edicion = None
    r = calcular_render(escenas, nframes, listos, vuelo, t_ini, ahora, aptos)
    r["parcial"] = nframes / FPS if parcial.get("nframes") else None
    r["limite"] = limite         # un segmento sin anotar solo se reutiliza si se empezó a dibujar después de esta hora
    r["edicion"] = edicion       # [archivo, epoch] de la última edición del código que decide los píxeles (la causa de los «no reutilizable»)
    return r


def progreso_secuencia(car, procs, ahora=None):
    """salida/progreso_render.json de un render del motor SECUENCIA si sigue vivo (lo escribe secuencia.video cada ~2 s);
    None si no hay render en marcha. Vivo = su pid sigue entre los python en marcha o lo reescribió hace < 15 s."""
    p = leer_json(os.path.join(car, "salida", "progreso_render.json"), None)
    if not isinstance(p, dict) or p.get("estado") not in ("dibujando", "codificando", "ambiente"):
        return None
    ahora = ahora or time.time()
    pids = {x.get("ProcessId") for x in procs or []}
    if p.get("pid") in pids or ahora - float(p.get("ahora") or 0) < 15:
        return p
    return None


def info_render_secuencia(car, tl, p, ahora=None):
    """Avance de un render del motor SECUENCIA con la misma forma que `calcular_render`, para la tarjeta «Render en vivo».
    secuencia.video dibuja de una sola pasada (sin segmentos en disco): el avance es el cuadro actual de su archivo de
    progreso; los cuadritos son tramos de 3 s del video (verde = dibujado, parpadea = el que dibuja ahora)."""
    ahora = ahora or time.time()
    fps = int(p.get("fps") or FPS)
    f0, f1 = int(p["f0"]), int(p["f1"])
    fr = min(f1, max(f0, int(p.get("frame") or f0)))
    t_ini = float(p.get("inicio") or ahora)
    hechos_f, tot_f = fr - f0, max(1, f1 - f0)
    vel = hechos_f / max(1e-6, float(p.get("ahora") or ahora) - t_ini) if hechos_f else 0.0    # cuadros por segundo de reloj
    fase = "uniendo" if p.get("estado") in ("codificando", "ambiente") else "dibujando"
    eta_fin = (ahora + (f1 - fr) / vel) if vel else (ahora if fase == "uniendo" else None)
    total = math.ceil(tot_f / TAM_SEG)
    k_act = (fr - f0) // TAM_SEG                         # tramo de 3 s (contado desde f0) que se está dibujando
    escenas = [e for e in (tl.get("escenas") or []) if e["t1"] * fps > f0 and e["t0"] * fps < f1] or \
              [dict(id="video", titulo="video completo", t0=f0 / fps, t1=f1 / fps)]
    filas, esc_fin = [], {}
    for i, e in enumerate(escenas):
        i0, i1 = max(f0, int(round(e["t0"] * fps))), min(f1, int(round(e["t1"] * fps)))
        k0 = (i0 - f0) // TAM_SEG
        k1 = max(k0 + 1, -(-(i1 - f0) // TAM_SEG))
        ks = range(k0, k1)
        celdas = "".join("d" if (k + 1) * TAM_SEG + f0 <= fr else "f" if k == k_act and fase == "dibujando" else "p" for k in ks)
        hechos = celdas.count("d")
        estado = "lista" if fr >= i1 else "en_curso" if i0 <= fr < i1 else "pendiente"
        if estado != "lista" and vel:
            esc_fin[e["id"]] = ahora + (i1 - fr) / vel
        nombre = e.get("titulo") or str(e["id"]).replace("_", " ")
        filas.append(dict(id=e["id"], n=i + 1, nombre=nombre[:1].upper() + nombre[1:], t0=round(e["t0"], 2), t1=round(e["t1"], 2),
                          k0=k0, k1=k1, celdas=celdas, hechos=hechos, estado=estado, fluida=False, vieja=False))
    try:
        mb = os.path.getsize(os.path.join(car, p.get("salida") or "")) / 1e6
    except OSError:
        mb = 0.0
    video_s, dur = hechos_f / fps, tot_f / fps
    tramo = p.get("tramo")
    det = f"{mmss(video_s)}/{mmss(dur)} de video" + (f" (tramo {tramo[0]:g}-{tramo[1]:g} s)" if tramo else "") \
        + (f" · {p['beat']}" if p.get("beat") else "")
    if fase == "uniendo":
        det += " · cerrando el mp4" if p.get("estado") == "codificando" else " · sonido ambiente de los clips"
    elif eta_fin:
        det += f" · ~{mmss(max(0, eta_fin - ahora))} restantes · termina {time.strftime('%H:%M', time.localtime(eta_fin))}"
    return dict(
        motor="secuencia", t_ini=t_ini, total=total, hechos=min(total, hechos_f // TAM_SEG), reusados=0,
        vuelo=[k_act] if fase == "dibujando" and fr < f1 else [], procs=1, seg_s=None,
        ritmo=round((float(p.get("ahora") or ahora) - t_ini) / video_s, 2) if video_s else None,
        duracion=round(dur, 1), video_s=round(video_s, 1), mb=round(mb, 1), fase=fase,
        progreso=hechos_f / tot_f, beat=p.get("beat"), beat_i=p.get("beat_i"), nbeats=p.get("nbeats"),
        tramo=tramo, estado_sec=p.get("estado"), detalle=det,
        ahora_en=[f["id"] for f in filas if f["estado"] == "en_curso"], escenas=filas, parcial=None, limite=None, edicion=None,
        vivo=dict(ahora=ahora, eta_fin=eta_fin, esc_fin=esc_fin))


# ======================================================================== análisis de un proyecto
# ======================================================================== canal de cada proyecto (fondo de la tarjeta)
def _canales_panel():
    """(alias, nombre) de cada canales/<alias>.json con «nombre»: un canal nuevo (Warcraft, Tamriel, Runa…) sale solo,
    sin tocar esta lista (22-oct: la lista fija se quedó sin ellos y sus videos caían en «Experimento»)."""
    out = []
    for ruta in sorted(glob.glob(os.path.join(CANALES, "*.json"))):
        d = leer_json(ruta, {})
        if isinstance(d, dict) and d.get("nombre"):
            out.append((os.path.basename(ruta)[:-5], d["nombre"]))
    return out


CANALES_PANEL = _canales_panel()
CANAL_NOMBRES = dict(CANALES_PANEL, experimento="Experimento")
# proyectos sin canal publicado ni mención en su guion.py (se puede fijar otro con `"canal": "<alias>"` en videos/<v>/panel.json)
CANAL_POR_VIDEO = dict(sol_apagado="kuriox", historia_60="kuriox", zacatecas_vox="bitacora_perdida", voynich="edsonxn")
FONDOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_fondos")


def _plano(s):
    import unicodedata
    return re.sub(r"[^a-z0-9]+", "_", "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                                              if unicodedata.category(c) != "Mn")).strip("_")


def canal_de(nombre, car, pub_canal, meta):
    """Alias del canal (clave de CANAL_NOMBRES) al que pertenece el proyecto: panel.json > canal donde se publicó >
    línea «- canal:» del ESTADO.md > «Canal X» en el docstring del guion > tabla fija > «experimento»."""
    por_nombre = {_plano(n): a for a, n in CANALES_PANEL}       # «Plastitube» -> pieza_oculta (alias distinto del nombre)
    # el ESTADO.md antes que el guion: un video --yt heredaba «Crónicas de Warcraft» del docstring de la plantilla (31-oct, n64_secretos)
    estado = ""
    try:
        m = re.search(r"(?im)^-\s*canal:\s*`?([^\n·(`]+)", open(os.path.join(car, "ESTADO.md"), encoding="utf-8", errors="replace").read(1500))
        estado = m.group(1) if m else ""
    except OSError:
        pass
    for c in (meta.get("canal"), pub_canal, estado):
        k = _plano(c) if c else ""
        k = k if k in CANAL_NOMBRES else por_nombre.get(k)
        if k:
            return k
    try:
        cab = _plano(open(os.path.join(car, "guion.py"), encoding="utf-8", errors="replace").read(1500))
        # el canal que se nombra PRIMERO (alias o nombre: «Crónicas de Warcraft» -> cronicas_de_warcraft), no el primero
        # de la lista: un guion de Warcraft que cita la voz de LogIA más abajo sigue siendo de Warcraft
        pos = [(i, alias) for alias, nom in CANALES_PANEL for i in (cab.find(alias), cab.find(_plano(nom))) if i >= 0]
        if pos:
            return min(pos)[1]
    except OSError:
        pass
    return CANAL_POR_VIDEO.get(nombre, "experimento")


def analizar(nombre, activo, pub, inicios=None, procs=None, susp=()):
    car = os.path.join(VIDEOS, nombre)
    g = parsear_guion(os.path.join(car, "guion.py"))
    escenas = g.get("ESCENAS") or []
    frases = sum(len(e.get("frases", [])) for e in escenas if isinstance(e, dict))
    archivo = g.get("ARCHIVO")
    tl = leer_json(os.path.join(car, "timeline.json"), {}) or {}
    tl_t = mt(os.path.join(car, "timeline.json"))
    total = float(tl.get("total") or 0.0)
    E = {}

    def st(clave, estado, prog=None, detalle="", t=0.0):
        E[clave] = dict(estado=estado, progreso=(1.0 if estado == "listo" else (prog or 0.0)), detalle=detalle,
                        t=t)

    st("guion", "listo", detalle=f"{len(escenas)} escenas · {frases} frases", t=mt(os.path.join(car, "guion.py")))

    # voz: tomas por frase = VOZ["tomas"] del guion; si falta, 1 con ElevenLabs (tts_eleven) y 4 con Chatterbox (tts_gen --seeds)
    vz = g.get("VOZ") if isinstance(g.get("VOZ"), dict) else {}
    try:
        tomas = max(1, int(vz.get("tomas") or (1 if vz.get("motor") == "elevenlabs" else 4)))
    except (TypeError, ValueError):
        tomas = 4
    cands = contar(os.path.join(car, "voz", "cands"), r"\.wav$")
    finales = contar(os.path.join(car, "voz", "final"), r"\.wav$")
    reg = leer_json(os.path.join(car, "voz", "regenerar.json"), None)
    objetivo = max(1, frases * tomas)
    t_voz = mt(os.path.join(car, "voz", "textos.json"))
    if cands >= objetivo:
        st("voz", "listo", detalle=f"{cands} tomas", t=t_voz)
    elif frases and finales >= frases and not reg:
        # la selección ya eligió una toma por frase: la voz está generada aunque se hayan usado menos tomas (--seeds) o se hayan borrado
        st("voz", "listo", detalle=f"{finales} frases con toma elegida" + (f" · {cands} tomas" if cands else ""), t=t_voz)
    elif cands:
        st("voz", "parcial", cands / objetivo, f"{cands}/{objetivo} tomas")
    else:
        st("voz", "pendiente")

    # selección
    pal = leer_json(os.path.join(car, "voz", "palabras.json"), None)
    voz_s = sum(v.get("dur", 0) for v in pal.values()) if isinstance(pal, dict) else 0
    if frases and finales >= frases and not reg:
        st("seleccion", "listo", detalle=f"{finales} frases · voz {mmss(voz_s)} · CER 0", t=mt(os.path.join(car, "voz", "eval.json")))
    elif reg:
        st("seleccion", "atencion", finales / max(frases, 1), f"regenerar: {', '.join(reg[:4])}")
    elif finales:
        st("seleccion", "parcial", finales / max(frases, 1), f"{finales}/{frases} frases")
    else:
        st("seleccion", "pendiente")

    # sin narración propia (SIN_VOZ) o con audio ya grabado (AUDIO_EXTERNO): no hay voz que generar ni seleccionar
    motivo_sin_voz = "sin narración" if g.get("SIN_VOZ") else "audio externo" if g.get("AUDIO_EXTERNO") else None
    if motivo_sin_voz:
        for k in ("voz", "seleccion"):
            E[k] = dict(estado="omitido", progreso=1.0, detalle=f"no aplica: {motivo_sin_voz}", t=0.0)

    # tiempo
    if tl and tl.get("provisional"):
        st("tiempo", "atencion", 0.5, "timeline provisional (falta ejecutar tiempo)")
    elif tl:
        st("tiempo", "listo", detalle=f"{mmss(total)} · {tl.get('bpm', '?')} BPM · {len(tl.get('escenas', []))} escenas", t=tl_t)
    else:
        st("tiempo", "pendiente")

    # escenas
    ep = os.path.join(car, "escenas.py")
    if existe(ep):
        n = sum(1 for _ in open(ep, encoding="utf-8", errors="replace"))
        mods = contar(car, r"\.py$") - 2
        st("escenas", "listo", detalle=f"{n} líneas" + (f" · +{mods} módulos" if mods > 0 else ""), t=mt(ep))
    else:
        st("escenas", "pendiente")

    # master (para render/final)
    masters = [p for p in glob.glob(os.path.join(car, "salida", "*_MASTER.mp4"))]
    master = masters[0] if masters else None
    sin_audio = existe(os.path.join(car, "salida", "video_sin_audio.mp4")) or existe(os.path.join(car, "video_sin_audio.mp4"))
    # audio
    for clave, arch, dep in (("musica", "musica.wav", tl_t), ("sfx", "sfx.wav", tl_t), ("mezcla", "final.wav", tl_t)):
        ruta = os.path.join(car, "audio", arch)
        if existe(ruta):
            if dep and mt(ruta) < dep - 1 and not (master and mt(master) >= dep):
                st(clave, "atencion", 1.0, "anterior al timeline actual: rehacer", mt(ruta))
            else:
                st(clave, "listo", detalle=f"{os.path.getsize(ruta) / 1e6:.0f} MB", t=mt(ruta))
        else:
            st(clave, "pendiente")

    nseg_total = math.ceil(total * FPS / TAM_SEG) if total else 0
    segs = contar(os.path.join(car, "segmentos"), r"^seg_\d+\.mp4$")
    tmp = contar(os.path.join(car, "segmentos"), r"\.tmp\.mp4$")
    if master or sin_audio or (nseg_total and segs >= nseg_total):
        st("video", "listo", detalle=f"{nseg_total} segmentos" if nseg_total else "", t=mt(master or os.path.join(car, "salida", "video_sin_audio.mp4")))
    elif segs or tmp:
        info = eta_render(car)
        det = f"{segs}/{nseg_total} segmentos" + (f" (+{tmp} en curso)" if tmp else "")
        par = leer_json(os.path.join(car, "segmentos", "parcial.json"), {}) or {}
        if par.get("hasta"):
            det = f"render parcial 0-{mmss(par['hasta'])}: {segs}/{math.ceil(par['nframes'] / TAM_SEG)} segmentos" + (f" (+{tmp} en curso)" if tmp else "")
        if info and info[0]:
            hechos, tot, seg_t = info
            resta = seg_t / max(hechos, 1) * max(tot - hechos, 0)
            det += f" · ~{mmss(resta)} restantes"
        st("video", "parcial", segs / max(nseg_total, 1), det)
    else:
        st("video", "pendiente")

    sec = render = None                          # render: avance real del render (por segmento y escena) mientras corre
    if g.get("MOTOR") == "secuencia":            # video hecho con clips e imágenes de Google Flow (nucleo/secuencia.py)
        sec = secuencia_info(car, tl_t)
        sec["yt"] = g.get("ESTILO_VISUAL") == "secuencia_yt"        # clips de gameplay con yt-dlp: no hay prompts ni Flow
        medios_txt = "clips de yt-dlp" if sec["yt"] else "medios"
        E.pop("escenas", None)
        nb = sec["total"]
        if not nb:
            st("beats", "pendiente")
        elif sec["beats_viejos"]:
            st("beats", "atencion", 1.0, "anteriores al timeline actual: rehacer", sec["beats_t"])
        else:
            st("beats", "listo", detalle=f"{nb} beats · {sec['n_video']} video + {nb - sec['n_video']} imagen", t=sec["beats_t"])
        if nb and sec["prompts"] >= nb:
            st("prompts", "listo", detalle=f"{sec['prompts']} prompts", t=sec["prompts_t"])
        elif sec["prompts"]:
            st("prompts", "parcial", sec["prompts"] / max(nb, 1), f"{sec['prompts']}/{nb} prompts")
        else:
            st("prompts", "pendiente")
        if sec["yt"]:
            E.pop("prompts", None)
        if nb and sec["hechos"] >= nb:
            st("flow", "listo", detalle=f"{nb} {medios_txt} " + ("bajados" if sec["yt"] else "recibidos"), t=sec["ultimo"])
        elif sec["hechos"]:
            det = f"{sec['hechos']}/{nb} {medios_txt}"
            if sec["eta_fin"]:
                det += f" · ~{mmss(max(0, sec['eta_fin'] - time.time()))} restantes"
            st("flow", "en_curso" if sec["activo"] else "parcial", sec["hechos"] / nb, det, sec["ultimo"])
        else:
            st("flow", "pendiente")
        if master or sin_audio:
            st("video", "listo", detalle="armado con secuencia", t=mt(master or os.path.join(car, "salida", "video_sin_audio.mp4")))
        else:
            st("video", "pendiente")
        # «Efectos» del motor secuencia = audio/fx.wav (`fab.py <v> fx`, SFX de efectos.py), no audio/sfx.wav del motor dibujado
        fx = os.path.join(car, "audio", "fx.wav")
        efx = os.path.join(car, "efectos.py")
        if existe(fx):
            if existe(efx) and mt(efx) > mt(fx) + 1 and not (master and mt(master) >= mt(efx)):
                st("sfx", "atencion", 1.0, "efectos.py cambió después de audio/fx.wav: rehacer `fx`", mt(fx))
            else:
                n_sfx = contar(os.path.join(car, "sfx"), r"\.mp3$")
                st("sfx", "listo", detalle="audio/fx.wav" + (f" · {n_sfx} SFX" if n_sfx else ""), t=mt(fx))
        elif not existe(os.path.join(car, "audio", "sfx.wav")):
            try:
                pistas = re.search(r"^PISTAS\s*=\s*\[(.*?)^\]", open(efx, encoding="utf-8", errors="replace").read(), re.M | re.S)
            except OSError:
                pistas = None
            if pistas and re.search(r"dict\(|\{", re.sub(r"#[^\n]*", "", pistas.group(1))):   # la plantilla trae ejemplos comentados
                st("sfx", "pendiente", detalle="efectos.py tiene PISTAS: falta `fab.py <v> fx`")
            else:
                E["sfx"] = dict(estado="omitido", progreso=1.0, detalle="no aplica: efectos.py sin PISTAS de sonido", t=0.0)
        prog_sec = progreso_secuencia(car, procs)
        if prog_sec:
            try:
                render = info_render_secuencia(car, tl, prog_sec)
            except Exception:                        # noqa: BLE001  (un fallo aquí no debe tumbar el panel)
                render = None
            if render:
                E["video"] = dict(estado="en_curso", progreso=render["progreso"], detalle=render["detalle"], t=time.time())

    if master:
        mb = os.path.getsize(master) / 1e6
        srt = glob.glob(os.path.join(car, "salida", "*.srt"))
        st("final", "listo", detalle=f"{mb:.0f} MB" + (" · con .srt" if srt else " · sin .srt"), t=mt(master))
    else:
        st("final", "pendiente")

    hoja = os.path.join(car, "previews", "final_hoja.jpg")
    if master and existe(hoja) and mt(hoja) >= mt(master) - 5:
        st("verificar", "listo", detalle="hoja final_hoja.jpg", t=mt(hoja))
    else:
        st("verificar", "pendiente")

    minis = sorted(glob.glob(os.path.join(car, "salida", "*_mini_*.jpg")))
    if minis:
        st("miniatura", "listo", detalle=f"{len(minis)} variantes", t=max(mt(p) for p in minis))
    else:
        st("miniatura", "pendiente")

    yj = leer_json(os.path.join(car, "youtube.json"), None)
    if yj:
        st("metadatos", "listo", detalle=(yj.get("titulo") or "")[:60], t=mt(os.path.join(car, "youtube.json")))
    else:
        st("metadatos", "pendiente")

    p = pub.get(nombre)
    if p:
        if not p.get("programado") and p.get("publicar") and not p.get("publicado"):
            p = dict(p, programado=p["publicar"])     # registros con la fecha en «publicar» (la mitad de canales/*.json)
        cuando = p.get("publicado") or p.get("programado") or p.get("subido") or ""
        et = "publicado" if p.get("publicado") else "programado" if p.get("programado") else             f"subido ({p.get('visibilidad', 'privado')})"
        st("subida", "listo", detalle=f"{et} {cuando[:16].replace('T', ' ')} · {p.get('canal', '')}")
    else:
        st("subida", "pendiente")

    # video ya en YouTube: el producto está terminado (los intermedios se borran al liberar disco) -> 100 %
    if p:
        for k, e in E.items():
            if e["estado"] != "listo" and k != activo.get(nombre):
                E[k] = dict(estado="listo", progreso=1.0, detalle="completado (ya en YouTube)", t=0.0)

    # proyecto archivado (p. ej. un prototipo reemplazado por otra versión): lo pendiente "no aplica"
    meta = leer_json(os.path.join(car, "panel.json"), {}) or {}
    if meta.get("archivado"):
        for k, e in E.items():
            if e["estado"] in ("pendiente", "parcial", "atencion"):
                E[k] = dict(estado="omitido", progreso=1.0, detalle="no aplica: " + (meta.get("motivo") or "archivado"), t=0.0)

    # etapa en curso (proceso vivo)
    en_curso = activo.get(nombre)
    if render and not en_curso:                      # render de secuencia lanzado sin fab.py (`python -m secuencia video`)
        en_curso = "video"
    if en_curso in E and E[en_curso]["estado"] != "listo":
        E[en_curso]["estado"] = "en_curso"
    elif en_curso in E:
        E[en_curso]["activo"] = True

    if en_curso == "video" and not sec:              # motor dibujado: el avance sale de segmentos/ (el de secuencia ya está arriba)
        try:
            render = info_render(car, tl, (inicios or {}).get(nombre))
        except Exception:                            # noqa: BLE001  (un fallo aquí no debe tumbar el panel)
            render = None
        prearmar(car, tl, render)
        if render and render["total"]:               # re-render con un MASTER previo: la etapa no está «lista» mientras dibuja
            fin = render["vivo"]["eta_fin"]
            det = f"{render['hechos']}/{render['total']} segmentos" + (f" (+{len(render['vuelo'])} en curso)" if render["vuelo"] else "")
            if fin:
                det += f" · ~{mmss(max(0, fin - time.time()))} restantes · termina {time.strftime('%H:%M', time.localtime(fin))}"
            E["video"].update(estado="en_curso", progreso=render["hechos"] / render["total"], detalle=det, activo=False)

    voz_vivo = None                                  # avance en vivo de la voz o de la selección (tomas, frase en curso, ETA)
    if en_curso in ("voz", "seleccion"):
        try:
            mod, fabs = ("tts_gen", ("voz", "todo")) if en_curso == "voz" else ("tts_select", ("seleccionar", "todo"))
            hijo, _ = proceso_hijo(procs or [], nombre, mod, fabs)
            if hijo:
                voz_vivo = info_voz(car, g, hijo) if en_curso == "voz" else info_seleccion(car, g, hijo, nombre)
            else:
                voz_vivo = dict(etapa=en_curso, titulo=("Voz" if en_curso == "voz" else "Selección") + " en vivo", espera=True,
                                ahora=cola_voz(procs or [], nombre))
        except Exception:                            # noqa: BLE001  (un fallo aquí no debe tumbar el panel)
            voz_vivo = None
        if voz_vivo and voz_vivo.get("total"):
            det = f"{voz_vivo['hechos']}/{voz_vivo['total']} {voz_vivo['unidad']}"
            if voz_vivo.get("eta_fin"):
                det += f" · ~{mmss(max(0, voz_vivo['eta_fin'] - time.time()))} restantes"
            E[en_curso].update(estado="en_curso", progreso=voz_vivo["hechos"] / voz_vivo["total"], detalle=det, activo=False)

    canal = canal_de(nombre, car, (p or {}).get("canal"), meta)
    prog_total = sum(v["progreso"] for v in E.values()) / len(E)
    log_nombre, log_lineas = ultimo_log(car)
    fotos = [os.path.basename(x) for x in minis][:3]
    hojas = [h for h in ("final_hoja.jpg", "hoja_render.jpg", "miniaturas.jpg") if existe(os.path.join(car, "previews", h))]
    actividad = max([mt(car)] + [v["t"] for v in E.values()] + [mt(os.path.join(car, "segmentos")), mt(os.path.join(car, "voz", "cands"))])
    try:                                             # «editado»: solo archivos del proyecto (guion.py, ESTADO.md, efectos…); borrar o limpiar carpetas no cuenta
        editado = max([mt(e.path) for e in os.scandir(car) if e.is_file() and e.name != "panel.json"] or [0.0])
    except OSError:
        editado = 0.0
    return dict(
        nombre=nombre, titulo=g.get("TITULO") or nombre, archivo=archivo, estilo=g.get("ESTILO_VISUAL", ""),
        formato=g.get("FORMATO", "horizontal"), duracion=total or g.get("DURACION"), frases=frases,
        escenas=len(escenas), progreso=prog_total, etapa_actual=en_curso, etapas=E, actividad=actividad, editado=editado,
        log=dict(archivo=log_nombre, lineas=log_lineas), miniaturas=fotos, hojas=hojas,
        master=os.path.basename(master) if master else None, publicado=bool(p),
        oculto=bool(meta.get("oculto", bool(p) or canal in susp)),   # lo ya en YouTube o de un canal suspendido nace oculto (salvo `"oculto": false`)
        suspendido=canal in susp, archivado=bool(meta.get("archivado")), reemplazado_por=meta.get("reemplazado_por"),
        nota=meta.get("motivo"), canal=canal, canal_nombre=CANAL_NOMBRES[canal], render=render, secuencia=sec, voz_vivo=voz_vivo,
        montaje=None if sec else montaje_resumen(car),
    )


EXT_MEDIO = (".mp4", ".webm", ".mov", ".jpg", ".jpeg", ".png", ".webp")


def _medio(car, sid):
    for ext in EXT_MEDIO:
        r = os.path.join(car, "medios", sid + ext)
        if existe(r):
            return r
    return None


def secuencia_info(car, tl_t):
    """Avance de un video del motor secuencia: beats, prompts y medios de Flow (con ritmo y hora estimada de término)."""
    beats = leer_json(os.path.join(car, "beats.json"), []) or []
    prompts = leer_json(os.path.join(car, "prompts.json"), {}) or {}
    bt = mt(os.path.join(car, "beats.json"))
    lista, tiempos, falt_v, falt_i = [], [], 0, 0
    for b in beats:
        r = _medio(car, b["id"])
        esv = b.get("tipo") == "video"
        if r:
            tiempos.append(mt(r))
        elif esv:
            falt_v += 1
        else:
            falt_i += 1
        lista.append(dict(id=b["id"], t0=b["t0"], t1=b["t1"], tipo=b.get("tipo", "imagen"), texto=b.get("texto", ""),
                          medio=(os.path.splitext(r)[1].lower() if r else None), mt=int(mt(r)) if r else 0,
                          prompt=bool(str(prompts.get(b["id"], "")).strip())))
    ahora = time.time()
    ultimo = max(tiempos) if tiempos else 0.0
    rec = sorted(t for t in tiempos if t > ahora - 900)
    activo = bool(rec) and ahora - rec[-1] < 240 and (falt_v + falt_i) > 0
    ritmo = eta = None
    if activo and len(rec) >= 3 and rec[-1] > rec[0]:
        ritmo = (len(rec) - 1) / (rec[-1] - rec[0])                    # medios por segundo en los últimos 15 min
        eta = rec[-1] + (falt_i or falt_v) / ritmo                      # primero se acaban las imágenes; los clips van aparte
    return dict(total=len(beats), n_video=sum(1 for b in beats if b.get("tipo") == "video"), hechos=len(tiempos),
                faltan_video=falt_v, faltan_imagen=falt_i, prompts=sum(1 for x in lista if x["prompt"]),
                prompts_t=mt(os.path.join(car, "prompts.json")), beats_t=bt, beats_viejos=bool(bt and tl_t and bt < tl_t - 1),
                ultimo=ultimo, activo=activo, por_min=(ritmo * 60 if ritmo else None), eta_fin=eta, beats=lista)


def medio_mini(nombre, sid):
    """Miniatura 320x180 de un medio (imagen o cuadro central del clip), guardada en previews/_minis para no rehacerla."""
    car = os.path.realpath(os.path.join(VIDEOS, nombre))
    if os.path.dirname(car) != os.path.realpath(VIDEOS) or not re.match(r"^scene-\d{3,}$", sid or ""):
        return None
    r = _medio(car, sid)
    if not r:
        return None
    dst = os.path.join(car, "previews", "_minis", f"{sid}_{int(mt(r))}.jpg")
    if not existe(dst):
        import cv2
        import numpy as np
        if r.lower().endswith((".mp4", ".webm", ".mov")):
            cap = cv2.VideoCapture(r)
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * 0.5))
            ok, im = cap.read()
            cap.release()
        else:
            im = cv2.imdecode(np.fromfile(r, np.uint8), cv2.IMREAD_COLOR)
            ok = im is not None
        if not ok:
            return None
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        im = cv2.resize(im, (320, 180), interpolation=cv2.INTER_AREA)
        cv2.imencode(".jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(dst)
    return open(dst, "rb").read()


def estado():
    procs, gpu = sistema()
    try:
        nombres = sorted(d for d in os.listdir(VIDEOS)
                         if not d.startswith("_") and existe(os.path.join(VIDEOS, d, "guion.py")))
    except OSError:
        nombres = []
    activo = etapas_en_curso(procs, set(nombres))
    inicios = {v: inicio_render(procs, v) for v, et in activo.items() if et == "video"}
    pub, susp = publicados(), canales_suspendidos()
    proyectos = []
    for n in nombres:
        try:
            proyectos.append(analizar(n, activo, pub, inicios, procs, susp))
        except Exception as e:                       # un proyecto roto no debe tumbar el panel
            proyectos.append(dict(nombre=n, titulo=n, error=str(e), etapas={}, progreso=0, actividad=0))
    try:
        libre = shutil.disk_usage(RAIZ).free / 1e9
    except OSError:
        libre = None
    return dict(generado=time.time(), proyectos=proyectos, etapas=[dict(id=i, nombre=nm) for i, nm in ETAPAS],
                sistema=dict(disco_libre_gb=libre, gpu=gpu, procesos_python=len(procs)))


# ======================================================================== estado compartido y avisos
_est = {"t": 0.0, "v": None}
_est_lock = threading.Lock()
LOC = None                     # AV.Locutor (se crea en main)
VOZ_CFG = {"cliente_audio": 0.0}


def estado_cache(max_edad=2.0):
    """Un solo escaneo por ~2 s aunque lo pidan la página y el vigilante a la vez."""
    with _est_lock:
        if time.time() - _est["t"] > max_edad or _est["v"] is None:
            _est["v"] = estado()
            _est["t"] = time.time()
        return _est["v"]


def ocultar_proyecto(nombre, oculto):
    """Marca/desmarca un proyecto como oculto en el panel (clave `oculto` de videos/<v>/panel.json; no borra nada)."""
    car = os.path.realpath(os.path.join(VIDEOS, nombre))
    if not nombre or nombre.startswith("_") or os.path.dirname(car) != os.path.realpath(VIDEOS) or not os.path.isdir(car):
        raise ValueError("proyecto desconocido")
    ruta = os.path.join(car, "panel.json")
    meta = leer_json(ruta, {}) or {}
    pub = publicados()
    if oculto:
        meta["oculto"] = True
    elif nombre in pub or canal_de(nombre, car, (pub.get(nombre) or {}).get("canal"), meta) in canales_suspendidos():
        meta["oculto"] = False       # ya en YouTube o de un canal suspendido: se oculta solo, así que «mostrar» se guarda explícito
    else:
        meta.pop("oculto", None)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    with _est_lock:
        _est["t"] = 0.0              # que el siguiente estado ya lo refleje
    return dict(video=nombre, oculto=bool(oculto))


def estado_completo():
    d = dict(estado_cache())
    d["avisos"] = LOC.recientes() if LOC else []
    d["voz"] = LOC.info() if LOC else dict(activo=False, destino="bocinas", modelo="inactivo", cola=0, voz="")
    return d


# ======================================================================== galería de estilos
# Un ejemplo REAL (video ya producido) por estilo, en nucleo/datos/galeria.json. `archivos`: el primero que exista en
# videos/<video>/salida/ se reproduce. Se relee en cada petición: editar el JSON no exige reiniciar el panel.
# Los cuadros de muestra se sacan con ffmpeg a videos/<video>/previews/galeria_N.jpg (carpeta ignorada por git).
GALERIA_JSON = os.path.join(RAIZ, "nucleo", "datos", "galeria.json")
FRACCIONES = (0.10, 0.34, 0.60, 0.86)
_gal_lock = threading.Lock()
_gal_en_curso = set()


def _ffmpeg(nombre):
    ruta = shutil.which(nombre)
    if ruta:
        return ruta
    c = os.path.join("C:\\ffmpeg\\bin", nombre + ".exe")
    return c if os.path.exists(c) else nombre


def _video_galeria(g):
    base = os.path.join(VIDEOS, g["video"], "salida")
    for a in g["archivos"]:
        if existe(os.path.join(base, a)):
            return a
    return None


def _duracion(ruta):
    try:
        out = subprocess.run([_ffmpeg("ffprobe"), "-v", "error", "-show_entries", "stream=width,height:format=duration",
                              "-of", "json", ruta], capture_output=True, text=True, timeout=30).stdout
        j = json.loads(out)
        s = (j.get("streams") or [{}])[0]
        return float(j["format"]["duration"]), int(s.get("width") or 1920), int(s.get("height") or 1080)
    except Exception:
        return 0.0, 1920, 1080


_meta_gal = {}


def _meta_video(ruta):
    k = (ruta, mt(ruta))
    if k not in _meta_gal:
        _meta_gal[k] = _duracion(ruta)
    return _meta_gal[k]


def _cuadros_galeria(g):
    """Genera (si faltan o están viejos) los cuadros de muestra del video de un estilo."""
    arch = _video_galeria(g)
    if not arch:
        return
    ruta = os.path.join(VIDEOS, g["video"], "salida", arch)
    dur, _, _ = _meta_video(ruta)
    if dur <= 0:
        return
    pv = os.path.join(VIDEOS, g["video"], "previews")
    os.makedirs(pv, exist_ok=True)
    for i, f in enumerate(FRACCIONES):
        sal = os.path.join(pv, f"galeria_{i}.jpg")
        if existe(sal) and mt(sal) >= mt(ruta):
            continue
        tmp = sal + ".tmp.jpg"
        subprocess.run([_ffmpeg("ffmpeg"), "-y", "-loglevel", "error", "-ss", f"{dur * f:.2f}", "-i", ruta, "-frames:v", "1",
                        "-vf", "scale='min(720,iw)':-2", "-q:v", "3", tmp], capture_output=True, timeout=120)
        if existe(tmp):
            os.replace(tmp, sal)


def _lanzar_cuadros(g):
    with _gal_lock:
        if g["id"] in _gal_en_curso:
            return
        _gal_en_curso.add(g["id"])

    def trabajo():
        try:
            _cuadros_galeria(g)
        except Exception:
            pass
        finally:
            with _gal_lock:
                _gal_en_curso.discard(g["id"])
    threading.Thread(target=trabajo, daemon=True).start()


def _catalogo():
    with open(GALERIA_JSON, encoding="utf-8") as f:
        return json.load(f)


def galeria():
    cat = _catalogo()
    items, pendientes = [], 0
    for g in cat["estilos"]:
        arch = _video_galeria(g)
        if not arch:
            continue
        ruta = os.path.join(VIDEOS, g["video"], "salida", arch)
        dur, w, h = _meta_video(ruta)
        pv = os.path.join(VIDEOS, g["video"], "previews")
        cuadros = [f"galeria_{i}.jpg" for i in range(len(FRACCIONES))
                   if existe(os.path.join(pv, f"galeria_{i}.jpg")) and mt(os.path.join(pv, f"galeria_{i}.jpg")) >= mt(ruta)]
        if len(cuadros) < len(FRACCIONES):
            pendientes += 1
            _lanzar_cuadros(g)
        titulo = parsear_guion(os.path.join(VIDEOS, g["video"], "guion.py")).get("TITULO") if os.path.exists(
            os.path.join(VIDEOS, g["video"], "guion.py")) else g["video"]
        d = {k: g.get(k, "") for k in ("id", "nombre", "estilo", "canal", "video", "desc", "uso", "extra")}   # una entrada sin «uso»/«extra» tumbaba la pestaña entera
        d.update(archivo=arch, titulo=titulo or g["video"], duracion=dur, vertical=h > w, cuadros=cuadros,
                 mb=round(os.path.getsize(ruta) / 1048576), version=int(mt(ruta)))
        items.append(d)
    return dict(estilos=items, sin_ejemplo=cat.get("sin_ejemplo", []), pendientes=pendientes)


def servir_video(handler, ruta_rel):
    """Sirve salida/*.mp4 con soporte de Range (necesario para adelantar/retroceder en <video>)."""
    partes = ruta_rel.split("/", 1)
    if len(partes) != 2:
        return handler._enviar(404, b"", "text/plain")
    base = os.path.realpath(os.path.join(VIDEOS, partes[0], "salida"))
    real = os.path.realpath(os.path.join(base, partes[1]))
    if not real.startswith(base + os.sep) or not real.lower().endswith(".mp4") or not existe(real):
        return handler._enviar(404, b"", "text/plain")
    _servir_rango(handler, real, "video/mp4")


def _servir_rango(handler, real, tipo):
    tam = os.path.getsize(real)
    ini, fin = 0, tam - 1
    m = re.match(r"bytes=(\d*)-(\d*)", handler.headers.get("Range") or "")
    codigo = 200
    if m and (m.group(1) or m.group(2)):
        if m.group(1):
            ini = int(m.group(1))
            if m.group(2):
                fin = min(int(m.group(2)), tam - 1)
        else:
            ini = max(0, tam - int(m.group(2)))
        if ini > fin or ini >= tam:
            handler.send_response(416)
            handler.send_header("Content-Range", f"bytes */{tam}")
            handler.end_headers()
            return
        codigo = 206
    handler.send_response(codigo)
    handler.send_header("Content-Type", tipo)
    handler.send_header("Accept-Ranges", "bytes")
    handler.send_header("Content-Length", str(fin - ini + 1))
    if codigo == 206:
        handler.send_header("Content-Range", f"bytes {ini}-{fin}/{tam}")
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    with open(real, "rb") as f:
        f.seek(ini)
        resto = fin - ini + 1
        while resto > 0:
            trozo = f.read(min(1 << 20, resto))
            if not trozo:
                break
            handler.wfile.write(trozo)
            resto -= len(trozo)


# ======================================================================== montaje (motor secuencia yt)
# Línea de tiempo viva de un video de clips de yt-dlp: el navegador reproduce cada clip de medios/ en su beat, con la voz
# de voz/final/ encima, y los huecos se van llenando conforme `bajar` deja clips. Solo lectura.
def _car_video(nombre):
    """Carpeta real de videos/<nombre>. Vale si es un junction a otro disco (desde el 24-oct-2026 hay videos movidos a
    E:/FabricaAnimaciones/videos_desde_C): se valida el NOMBRE (una sola carpeta, sin rutas), no el destino del enlace."""
    if not nombre or nombre in (".", "..") or any(c in nombre for c in "/\\:"):
        return None
    enlace = os.path.join(VIDEOS, nombre)
    return os.path.realpath(enlace) if existe(os.path.join(enlace, "guion.py")) else None


def detalle_voz(nombre, etapa):
    """Las barritas de Voz / Selección aunque la etapa no esté corriendo (clic en su casilla del panel, 19-oct-2026):
    las mismas filas que el «en vivo», calculadas sobre lo que hay en disco (voz/cands, eval.json, regenerar.json, voz/final)."""
    car = _car_video(nombre)
    if not car:
        return dict(error="video desconocido")
    g = parsear_guion(os.path.join(car, "guion.py"))
    tomas = _tomas(car)
    if etapa == "voz":
        vz = g.get("VOZ") if isinstance(g.get("VOZ"), dict) else {}
        n = max(1, int(vz.get("tomas") or (1 if vz.get("motor") == "elevenlabs" else 4)))
        seeds = sorted({s for d in tomas.values() for s in d}) or list(range(1, n + 1))
        seeds = seeds[:max(n, 1)] if vz.get("motor") != "elevenlabs" else seeds
        d = info_voz(car, g, {"CommandLine": "--seeds " + " ".join(map(str, seeds)), "T": 1})
        faltan = d["total"] - d["hechos"]
        d.update(titulo="Voz · lo que hay en disco", ahora=f"faltan {faltan} tomas" if faltan else "todas las tomas generadas",
                 eta_fin=None, chips=[c for c in d["chips"] if c[0] not in ("Transcurrido", "Ritmo", "Última")])
    else:
        d = info_seleccion(car, g, {"T": 1, "ProcessId": "disco"}, nombre)
        reg = leer_json(os.path.join(car, "voz", "regenerar.json"), None)
        ev = leer_json(os.path.join(car, "voz", "eval.json"), {}) or {}
        sin_eval = sum(1 for k, dd in tomas.items() for s in dd if f"{k}_s{s}.wav" not in ev)
        d.update(titulo="Selección · lo que hay en disco", eta_fin=None,
                 ahora=(f"{sin_eval} tomas sin evaluar" if sin_eval else
                        f"regenerar: {', '.join(reg)}" if reg else "todas las frases tienen toma elegida"))
        fin_dir = os.path.join(car, "voz", "final")
        n_fin = len([1 for e in os.scandir(fin_dir) if e.name.endswith(".wav")]) if os.path.isdir(fin_dir) else 0
        d["chips"] = [["Tomas evaluadas", str(len(ev))], ["Con toma elegida", str(n_fin)],
                      ["Para regenerar", str(len(reg or []))]]
    d.update(t_ini=time.time(), disco=True)
    return d


def montaje(nombre):
    car = _car_video(nombre)
    if not car:
        return dict(error="video desconocido")
    if parsear_guion(os.path.join(car, "guion.py")).get("MOTOR") != "secuencia":
        return montaje_codigo(car, nombre)
    tl = leer_json(os.path.join(car, "timeline.json"), {}) or {}
    sec = secuencia_info(car, mt(os.path.join(car, "timeline.json")))
    fuentes = leer_json(os.path.join(car, "fuentes.json"), {}) or {}
    for b in sec["beats"]:
        f = fuentes.get(b["id"]) or {}
        b["fuente"] = " · ".join(str(x) for x in (f.get("canal"), f.get("titulo")) if x)
        b["q"] = f.get("q", "")
    frases = [dict(key=f["key"], t0=f["t0"], t1=f["t1"], voz=existe(os.path.join(car, "voz", "final", f["key"] + ".wav")))
              for e in tl.get("escenas", []) for f in e.get("frases", []) if f.get("key")]
    total = tl.get("total") or (sec["beats"][-1]["t1"] if sec["beats"] else 0)
    sec["total_beats"] = sec.pop("total")
    # capa de efectos ya exportada por `fab.py <v> fx montaje`: apoyos (PNG encima) y tramos con MG/videos (mp4 compuesto)
    rfx = os.path.join(car, "previews", "montaje_fx.json")
    fx = leer_json(rfx, {}) or {}
    fx["viejo"] = bool(fx) and mt(os.path.join(car, "efectos.py")) > mt(rfx)
    fx["hay_efectos"] = existe(os.path.join(car, "efectos.py"))
    mus = os.path.join(car, "audio", "musica.wav")
    return dict(video=nombre, total=total, frases=frases, fx=fx, musica=existe(mus), musica_t=mt(mus), **sec)


# ---- montaje de los videos dibujados por código (20-oct-2026): cada escena de timeline.json es un bloque que se reproduce
# fluido con su «escena fluida» (previews/escena_<id>.mp4) o con el borrador de `fab.py <v> montaje` (previews/montaje/<id>.mp4)
def _escenas_montaje(car):
    """[(escena, archivo servido, offset en el mp4, origen)] de lo que ya se puede ver, sin calcular firmas (barato)."""
    tl = leer_json(os.path.join(car, "timeline.json"), {}) or {}
    fl = leer_json(os.path.join(car, "previews", "escenas.json"), {}) or {}
    bo = leer_json(os.path.join(car, "previews", "montaje", "info.json"), {}) or {}
    out = []
    for e in tl.get("escenas", []):
        f, b = fl.get(e["id"]), bo.get(e["id"])
        if f and existe(os.path.join(car, "previews", f["mp4"])) and not (b and b.get("ts", 0) > f.get("ts", 0)
                                                                            and existe(os.path.join(car, "previews", "montaje", e["id"] + ".mp4"))):
            out.append((e, "fl/" + f["mp4"], max(0.0, e["t0"] - f["vt0"]), "fluida", f))
        elif b and existe(os.path.join(car, "previews", "montaje", e["id"] + ".mp4")):
            out.append((e, "esc/" + e["id"] + ".mp4", 0.0, "borrador", b))
        else:
            out.append((e, None, 0.0, None, None))
    return tl, out


def montaje_resumen(car):
    if not existe(os.path.join(car, "timeline.json")):
        return None
    _, es = _escenas_montaje(car)
    return dict(hechos=sum(1 for x in es if x[1]), total=len(es))


def montaje_codigo(car, nombre):
    tl, es = _escenas_montaje(car)
    g = parsear_guion(os.path.join(car, "guion.py"))
    firma, vig = None, {}
    if CE is not None:
        try:
            firma = CE.firma_codigo(car, NUCLEO)
            vig = {x["id"]: x["estado"] for x in CE.listar(car, NUCLEO)}
        except Exception:                                # noqa: BLE001
            firma, vig = None, {}
    textos = {e.get("id"): " ".join(e.get("frases") or []) for e in g.get("ESCENAS") or [] if isinstance(e, dict)}
    beats = []
    for e, arch, off, origen, d in es:
        viejo = False
        if origen == "fluida":
            viejo = vig.get(e["id"]) == "obsoleta" if firma else False
        elif origen == "borrador":
            viejo = (firma and d.get("firma") != firma) or d.get("t0") != e["t0"] or d.get("t1") != e["t1"]
        mini = bool(arch)            # la del borrador; la de una escena fluida se saca de su mp4 al pedirla (servir_montaje)
        beats.append(dict(id=e["id"], etq=e["id"], t0=e["t0"], t1=e["t1"], texto=textos.get(e["id"], ""),
                          medio=arch or "", url=f"/montaje/{nombre}/{arch}" if arch else "", off=round(off, 3),
                          mt=int(mt(os.path.join(car, "previews", arch.replace("esc/", "montaje/").replace("fl/", ""))))
                          if arch else 0, origen=origen or "", viejo=bool(viejo),
                          mini=f"/montaje/{nombre}/esc/{e['id']}.jpg" if mini else "", vel=1))
    total = tl.get("total") or (beats[-1]["t1"] if beats else 0)
    # escenas del guion que aún no tienen voz (no están en timeline.json): en gris, con la duración estimada por palabras
    hay = {b["id"] for b in beats}
    t = total
    for e in g.get("ESCENAS") or []:
        if isinstance(e, dict) and e.get("id") and e["id"] not in hay:
            txt = textos.get(e["id"], "")
            dur = max(4.0, len(txt.split()) / 2.7)
            beats.append(dict(id=e["id"], etq=e["id"], t0=round(t, 2), t1=round(t + dur, 2), texto=txt, medio="", url="", off=0,
                              mt=0, origen="", viejo=False, mini="", plan=True))
            t += dur
    frases = [dict(key=f["key"], t0=f["t0"], t1=f["t1"], voz=existe(os.path.join(car, "voz", "final", f["key"] + ".wav")))
              for e in tl.get("escenas", []) for f in e.get("frases", []) if f.get("key")]
    fin = os.path.join(car, "audio", "final.wav")
    mezcla = existe(fin) and mt(fin) >= mt(os.path.join(car, "timeline.json"))     # la mezcla vale si es posterior a «tiempo»
    mus = fin if mezcla else os.path.join(car, "audio", "musica.wav")
    prog = leer_json(os.path.join(car, "previews", "montaje", "progreso.json"), None)
    activo = bool(prog) and time.time() - mt(os.path.join(car, "previews", "montaje", "progreso.json")) < 300
    hechos = sum(1 for b in beats if b["medio"])
    return dict(video=nombre, codigo=True, total=t, total_voz=total, beats=beats, frases=frases, hechos=hechos,
                total_beats=len(beats), viejos=sum(1 for b in beats if b["viejo"]), plan=sum(1 for b in beats if b.get("plan")),
                activo=activo, progreso=prog if activo else None, fx={}, musica=existe(mus), musica_t=mt(mus),
                musica_src="mezcla" if mezcla else "musica", mezcla=mezcla)


_cerrojo_mus = threading.Lock()


def _musica_montaje(car, fuente="musica"):
    """audio/musica.wav (float32, cientos de MB) -> previews/montaje_musica.m4a liviana para el navegador; se rehace si cambia.
    fuente="mezcla": audio/final.wav (voz + música + SFX) -> previews/montaje_mezcla.m4a (videos por código)."""
    wav = os.path.join(car, "audio", "final.wav" if fuente == "mezcla" else "musica.wav")
    m4a = os.path.join(car, "previews", f"montaje_{fuente}.m4a")
    if not existe(wav):
        return None
    with _cerrojo_mus:
        if not existe(m4a) or mt(m4a) < mt(wav):
            os.makedirs(os.path.dirname(m4a), exist_ok=True)
            tmp = m4a[:-4] + "_tmp.m4a"
            r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-i", wav, "-ac", "2", "-c:a", "aac",
                                "-b:a", "128k", "-movflags", "+faststart", tmp], capture_output=True, timeout=600)
            if r.returncode != 0 or not existe(tmp):
                return None
            os.replace(tmp, m4a)
    return m4a


def servir_montaje(handler, ruta_rel):
    """/montaje/<video>/clip/<scene-id>  ·  /montaje/<video>/voz/<key>.wav  ·  /montaje/<video>/fx/<archivo>
    (apoyos/*.png y previews/montaje_fx/*.mp4)  (con Range, para saltar dentro del clip)."""
    partes = ruta_rel.split("/")
    car = _car_video(partes[0]) if len(partes) == 3 else None
    real = tipo = None
    if car and partes[1] == "clip" and re.match(r"^scene-\d{3,}$", partes[2]):
        real = _medio(car, partes[2])
        tipo = mimetypes.guess_type(real)[0] if real else None
    elif car and partes[1] == "voz" and re.match(r"^[\w-]+\.wav$", partes[2]):
        real, tipo = os.path.join(car, "voz", "final", partes[2]), "audio/wav"
    elif car and partes[1] == "musica" and partes[2] in ("musica.m4a", "mezcla.m4a"):
        real, tipo = _musica_montaje(car, partes[2][:-4]), "audio/mp4"
    elif car and partes[1] == "esc" and re.match(r"^[\w-]+\.(mp4|jpg)$", partes[2]):        # borradores de `fab.py <v> montaje`
        real = os.path.join(car, "previews", "montaje", partes[2])
        tipo = "video/mp4" if partes[2].endswith(".mp4") else "image/jpeg"
        f = (leer_json(os.path.join(car, "previews", "escenas.json"), {}) or {}).get(partes[2][:-4])
        if tipo == "image/jpeg" and not existe(real) and f and existe(os.path.join(car, "previews", f["mp4"])):
            os.makedirs(os.path.dirname(real), exist_ok=True)       # miniatura de una escena fluida: su cuadro del medio
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{(f['vt1'] - f['vt0']) / 2:.2f}",
                            "-i", os.path.join(car, "previews", f["mp4"]), "-frames:v", "1", "-vf", "scale=240:-2", "-q:v", "5",
                            real], capture_output=True, timeout=60)
    elif car and partes[1] == "fl" and re.match(r"^escena_[\w-]+\.mp4$", partes[2]):        # escenas fluidas de la vista previa
        real, tipo = os.path.join(car, "previews", partes[2]), "video/mp4"
    elif car and partes[1] == "fx" and re.match(r"^[\w-]+\.(png|mp4)$", partes[2]):
        png = partes[2].endswith(".png")
        real = os.path.join(car, "apoyos" if png else os.path.join("previews", "montaje_fx"), partes[2])
        tipo = "image/png" if png else "video/mp4"
    if not real or not existe(real):
        return handler._enviar(404, b"", "text/plain")
    _servir_rango(handler, real, tipo or "application/octet-stream")


# ======================================================================== vista previa (workers)
# Un proceso `preview_worker.py` por video, lanzado bajo demanda; el navegador le habla directo (puerto + token).
NUCLEO = os.path.dirname(os.path.abspath(__file__))
NO_CODIGO = {"panel.py", "muestra_estilo.py", "avisos.py", "avisos_voz.py", "youtube.py", "vox.py", "lyria.py"}   # no afectan al render
PREVIEWS = {}                                  # video -> dict(proc, puerto, token, firma)
_cerrojo_prev = threading.Lock()


def _firma_codigo(nombre):
    """Última modificación de lo que el render importa: si cambia, el worker se reinicia solo."""
    car = os.path.join(VIDEOS, nombre)
    arch = glob.glob(os.path.join(car, "*.py")) + [os.path.join(car, "timeline.json")]
    arch += [f for f in glob.glob(os.path.join(NUCLEO, "*.py")) if os.path.basename(f) not in NO_CODIGO]
    return max(mt(f) for f in arch)


def _puerto_libre():
    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _worker_listo(pv):
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{pv['puerto']}/info?token={pv['token']}", timeout=1.5) as r:
            return r.status == 200
    except Exception:
        return False


def _detener_worker(nombre):
    pv = PREVIEWS.pop(nombre, None)
    if pv and pv["proc"].poll() is None:
        pv["proc"].kill()


def vista_previa(nombre, forzar_reinicio=False):
    """Asegura el worker del video y devuelve su estado para el navegador."""
    if not re.match(r"^[\w\-]+$", nombre or ""):
        return dict(estado="error", error="nombre de video no válido")
    car = os.path.join(VIDEOS, nombre)
    if not existe(os.path.join(car, "timeline.json")):
        return dict(estado="error", error="este video aún no tiene timeline.json (corre la etapa «tiempo»)")
    with _cerrojo_prev:
        pv = PREVIEWS.get(nombre)
        firma = _firma_codigo(nombre)
        if pv and (pv["proc"].poll() is not None or forzar_reinicio or pv["firma"] < firma):
            _detener_worker(nombre)
            pv = None
        if not pv:
            import secrets
            os.makedirs(os.path.join(car, "previews"), exist_ok=True)
            puerto, token = _puerto_libre(), secrets.token_hex(8)
            env = dict(os.environ, PYTHONPATH=os.pathsep.join([car, NUCLEO]), PYTHONIOENCODING="utf-8")
            log = open(os.path.join(car, "previews", "_preview.log"), "w", encoding="utf-8")
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            proc = subprocess.Popen([sys.executable, os.path.join(NUCLEO, "preview_worker.py"), "--puerto", str(puerto),
                                     "--token", token], cwd=car, env=env, stdout=log, stderr=subprocess.STDOUT,
                                    creationflags=flags)
            pv = PREVIEWS[nombre] = dict(proc=proc, puerto=puerto, token=token, firma=firma, t=time.time())
    if pv["proc"].poll() is not None:
        try:
            cola = open(os.path.join(car, "previews", "_preview.log"), encoding="utf-8", errors="replace").read()[-600:]
        except OSError:
            cola = ""
        return dict(estado="error", error="el worker se cerró: " + cola)
    if _worker_listo(pv):
        return dict(estado="listo", puerto=pv["puerto"], token=pv["token"])
    return dict(estado="arrancando", segundos=round(time.time() - pv["t"]))


# ======================================================================== muestra de estilo (sin voz ni «tiempo»)
MONTAJES = {}                  # video -> Popen de `fab.py <v> montaje` (borradores del montaje de videos por código)


def montaje_dibujar(nombre):
    """Lanza `python fab.py <v> montaje` en segundo plano: dibuja a 640x360 las escenas sin borrador o con borrador viejo."""
    car = _car_video(nombre)
    if not car:
        return dict(error="video desconocido")
    proc = MONTAJES.get(nombre)
    if proc and proc.poll() is None:
        return dict(ok=True, ya=True)
    os.makedirs(os.path.join(car, "previews", "montaje"), exist_ok=True)
    log = open(os.path.join(car, "previews", "montaje", "_montaje.log"), "w", encoding="utf-8")
    MONTAJES[nombre] = subprocess.Popen([sys.executable, os.path.join(RAIZ, "fab.py"), nombre, "montaje"], cwd=RAIZ,
                                        env=dict(os.environ, PYTHONIOENCODING="utf-8"), stdout=log, stderr=subprocess.STDOUT,
                                        creationflags=0x00004000 | getattr(subprocess, "CREATE_NO_WINDOW", 0))   # prioridad baja
    return dict(ok=True)


MUESTRAS = {}                  # video -> Popen de muestra_estilo.py


def muestra(nombre, lanzar=False):
    """10 cuadros distintos para ver el estilo de un video aunque aún no tenga timeline.json (ver muestra_estilo.py)."""
    if not re.match(r"^[\w\-]+$", nombre or ""):
        return dict(estado="error", error="nombre de video no válido")
    car = os.path.join(VIDEOS, nombre)
    if not existe(os.path.join(car, "escenas.py")):
        return dict(estado="error", error="este video aún no tiene escenas.py")
    sal = os.path.join(car, "previews", "muestra")
    proc = MUESTRAS.get(nombre)
    corriendo = bool(proc and proc.poll() is None)
    if lanzar and not corriendo:
        os.makedirs(sal, exist_ok=True)
        for f in ("estado.json", "muestra.json"):
            try:
                os.remove(os.path.join(sal, f))
            except OSError:
                pass
        env = dict(os.environ, PYTHONPATH=os.pathsep.join([car, NUCLEO]), PYTHONIOENCODING="utf-8")
        log = open(os.path.join(sal, "_muestra.log"), "w", encoding="utf-8")
        MUESTRAS[nombre] = subprocess.Popen([sys.executable, os.path.join(NUCLEO, "muestra_estilo.py")], cwd=car, env=env,
                                            stdout=log, stderr=subprocess.STDOUT,
                                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        corriendo = True
    est = leer_json(os.path.join(sal, "estado.json"), None)
    if corriendo and (not est or est.get("estado") in ("listo", "error")) and lanzar:
        est = dict(estado="arrancando", hecho=0, total=10)
    if not est:
        return dict(estado="vacio")
    if not corriendo and est.get("estado") in ("arrancando", "dibujando"):       # el proceso murió sin avisar
        est = dict(estado="error", error="el proceso se cerró antes de terminar (mira previews/muestra/_muestra.log)")
    out = dict(est)
    if out.get("estado") == "listo":
        out.update(leer_json(os.path.join(sal, "muestra.json"), {}) or {})
    return out


# ======================================================================== pestaña «Canales» (nucleo/estadisticas.py)
CAN = dict(activo=False, hecho=0, total=0, errores=[])
_can_lock = threading.Lock()


def canales_html():
    """Calendario (qué canal se queda sin video) + estadísticas, con los datos guardados en canales/metricas/panel/."""
    import estadisticas as ES
    return ES.html_panel(estado_cache(30)["proyectos"])


def canales_actualizar():
    """Pide datos frescos a YouTube (solo lectura) en segundo plano; el avance se lee en /api/canales/progreso."""
    import estadisticas as ES
    from concurrent.futures import ThreadPoolExecutor
    with _can_lock:
        if CAN["activo"]:
            return dict(CAN)
        alias = ES.alias_conocidos()
        CAN.update(activo=True, hecho=0, total=len(alias), errores=[])

    def uno(a):
        try:
            ES.actualizar_seguro(a)
        except (Exception, SystemExit) as e:         # un canal sin token o caído no tumba a los demás
            CAN["errores"].append(f"{a}: {e}"[:220])
        CAN["hecho"] += 1

    def tarea():
        try:
            with ThreadPoolExecutor(4) as ex:
                list(ex.map(uno, alias))
        finally:
            CAN["activo"] = False
    threading.Thread(target=tarea, daemon=True).start()
    return dict(CAN)


# ======================================================================== panel v2 «Lienzo» (nucleo/panel_v2.py + panel_v2.html)
_V2 = {"mod": None, "t": 0.0}
_v2_lock = threading.Lock()


def _v2():
    """El backend del lienzo, recargado si cambió su archivo: editar panel_v2.py NO exige reiniciar el panel."""
    import importlib
    ruta = os.path.join(NUCLEO, "panel_v2.py")
    with _v2_lock:
        t = mt(ruta)
        if _V2["mod"] is None or t != _V2["t"]:
            import panel_v2 as m
            if _V2["mod"] is not None:
                m = importlib.reload(m)
            m.P = sys.modules[__name__]
            _V2.update(mod=m, t=t)
        return _V2["mod"]


# ======================================================================== servidor
class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _enviar(self, codigo, cuerpo, tipo, cache="no-store"):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        ruta = unquote(urlparse(self.path).path)
        try:
            if ruta in ("/", "/index.html"):
                self._enviar(200, open(HTML, "rb").read(), "text/html; charset=utf-8")
            elif ruta.startswith("/propuesta/") and re.match(r"^/propuesta/panel_v\d+\.html$", ruta):      # versión nueva del panel a prueba (skill analizar-uso-panel)
                real = os.path.join(os.path.dirname(HTML), "propuestas_panel", os.path.basename(ruta))
                if not existe(real):
                    return self._enviar(404, b"", "text/plain")
                self._enviar(200, open(real, "rb").read(), "text/html; charset=utf-8")
            elif ruta == "/uso.js":
                self._enviar(200, open(USO_JS, "rb").read(), "application/javascript; charset=utf-8")
            elif ruta == "/api/estado":
                self._enviar(200, json.dumps(estado_completo(), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/api/estilos":
                self._enviar(200, json.dumps(galeria(), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/canales":
                self._enviar(200, canales_html().encode("utf-8"), "text/html; charset=utf-8")
            elif ruta == "/api/canales/progreso":
                self._enviar(200, json.dumps(CAN, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            elif ruta.startswith("/video/"):
                servir_video(self, ruta[len("/video/"):])
            elif ruta.startswith("/montaje/"):
                servir_montaje(self, ruta[len("/montaje/"):])
            elif ruta == "/api/detalle_voz":
                q = parse_qs(urlparse(self.path).query)
                d = detalle_voz((q.get("video") or [""])[0], (q.get("etapa") or ["voz"])[0])
                self._enviar(200, json.dumps(d, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            elif ruta == "/api/montaje":
                nombre = (parse_qs(urlparse(self.path).query).get("video") or [""])[0]
                self._enviar(200, json.dumps(montaje(nombre), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/api/preview":
                nombre = (parse_qs(urlparse(self.path).query).get("video") or [""])[0]
                self._enviar(200, json.dumps(vista_previa(nombre), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/api/muestra":
                nombre = (parse_qs(urlparse(self.path).query).get("video") or [""])[0]
                self._enviar(200, json.dumps(muestra(nombre), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/api/medio_mini":
                q = parse_qs(urlparse(self.path).query)
                datos = medio_mini((q.get("video") or [""])[0], (q.get("id") or [""])[0])
                if datos is None:
                    return self._enviar(404, b"", "text/plain")
                self._enviar(200, datos, "image/jpeg", cache="max-age=86400")
            elif ruta.startswith("/audio/"):
                nombre = os.path.basename(ruta)
                real = os.path.join(AV.DIR, nombre)
                if not re.match(r"^[0-9a-f]{16}\.wav$", nombre) or not existe(real):
                    return self._enviar(404, b"", "text/plain")
                self._enviar(200, open(real, "rb").read(), "audio/wav", cache="max-age=3600")
            elif ruta.startswith("/fondo/") and re.match(r"^/fondo/[a-z_]+\.svg$", ruta):
                real = os.path.join(FONDOS, os.path.basename(ruta))
                if not existe(real):
                    return self._enviar(404, b"", "text/plain")
                self._enviar(200, open(real, "rb").read(), "image/svg+xml", cache="max-age=300")
            elif ruta.startswith("/media/"):
                partes = ruta[len("/media/"):].split("/", 1)
                if len(partes) != 2:
                    return self._enviar(404, b"", "text/plain")
                carpeta = os.path.join(VIDEOS, partes[0])
                real = os.path.realpath(os.path.join(carpeta, partes[1]))
                sub = partes[1].replace("\\", "/").split("/")[0]
                # base = la subcarpeta ya resuelta: si previews/ o salida/ son un junction a otro disco (mover_pesados.py), vale igual
                base = os.path.realpath(os.path.join(carpeta, sub))
                permitido = sub in ("previews", "salida") and real.startswith(base + os.sep) \
                    and real.lower().endswith((".jpg", ".jpeg", ".png"))
                if not permitido or not existe(real):
                    return self._enviar(404, b"", "text/plain")
                self._enviar(200, open(real, "rb").read(), mimetypes.guess_type(real)[0] or "image/jpeg",
                             cache="max-age=120")
            elif ruta in ("/v2", "/v2/") or ruta.startswith(("/v2/", "/api/v2/")):
                _v2().get(self, ruta)
            else:
                self._enviar(404, b"no encontrado", "text/plain")
        except ConnectionError:
            pass
        except Exception as e:
            try:
                self._enviar(500, str(e).encode("utf-8", "replace"), "text/plain; charset=utf-8")
            except ConnectionError:
                pass


    def do_POST(self):
        ruta = urlparse(self.path).path
        try:
            n = int(self.headers.get("Content-Length") or 0)
            datos = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
            if ruta == "/api/uso":
                UP.guardar(datos.get("eventos"))
                self._enviar(204, b"", "text/plain")
            elif ruta == "/api/voz":
                cfg = AV.guardar_config({k: datos[k] for k in ("activo", "destino") if k in datos})
                self._enviar(200, json.dumps(cfg).encode("utf-8"), "application/json")
            elif ruta == "/api/ocultar":
                self._enviar(200, json.dumps(ocultar_proyecto(str(datos.get("video", "")), bool(datos.get("oculto", True)))).encode("utf-8"),
                             "application/json")
            elif ruta == "/api/muestra":
                self._enviar(200, json.dumps(muestra(str(datos.get("video", "")), lanzar=True), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/api/montaje/dibujar":
                self._enviar(200, json.dumps(montaje_dibujar(str(datos.get("video", ""))), ensure_ascii=False).encode("utf-8"),
                             "application/json; charset=utf-8")
            elif ruta == "/api/preview/reiniciar":
                self._enviar(200, json.dumps(vista_previa(datos.get("video", ""), forzar_reinicio=True),
                                             ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            elif ruta == "/api/canales/actualizar":
                self._enviar(200, json.dumps(canales_actualizar(), ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
            elif ruta == "/api/canales/ciclo":
                import estadisticas as ES
                self._enviar(200, json.dumps(dict(ciclo=ES.guardar_ciclo(str(datos.get("alias", "")), datos.get("dias", 0)))).encode("utf-8"),
                             "application/json")
            elif ruta == "/api/probar" and LOC:
                LOC.decir(datos.get("texto") or "Panel de la fábrica listo. Este es un aviso de prueba.", motivo="prueba")
                self._enviar(200, b"{}", "application/json")
            elif ruta.startswith("/api/v2/"):
                _v2().post(self, ruta, datos)
            else:
                self._enviar(404, b"", "text/plain")
        except ConnectionError:
            pass
        except Exception as e:
            try:
                self._enviar(500, str(e).encode("utf-8", "replace"), "text/plain; charset=utf-8")
            except ConnectionError:
                pass


def main():
    global LOC
    ap = argparse.ArgumentParser()
    ap.add_argument("--puerto", type=int, default=8765)
    ap.add_argument("--abrir", action="store_true")
    ap.add_argument("--lienzo", action="store_true", help="con --abrir, abre el lienzo v2 (/v2) en vez del panel clásico")
    ap.add_argument("--json", action="store_true", help="imprime el estado y sale")
    ap.add_argument("--sin-voz", action="store_true", help="no arranca el vigilante de avisos por voz")
    a = ap.parse_args()
    if a.json:
        sys.stdout.reconfigure(encoding="utf-8")
        sistema(forzar=True)
        print(json.dumps(estado(), ensure_ascii=False, indent=1))
        return
    ThreadingHTTPServer.request_queue_size = 128     # el lienzo pide muchas miniaturas a la vez: con 5 (por defecto) Windows rechazaba las demás
    srv = ThreadingHTTPServer(("127.0.0.1", a.puerto), Manejador)
    url = f"http://127.0.0.1:{a.puerto}"
    print(f"Panel en {url}  ·  lienzo (v2) en {url}/v2  (Ctrl+C para cerrar)", flush=True)
    threading.Thread(target=_refrescar_sistema, daemon=True).start()
    if not a.sin_voz:
        LOC = AV.Locutor()
        AV.Vigilante(estado_cache, LOC).start()
        print("Avisos por voz activos (config: panel_config.json)", flush=True)
    if a.abrir:
        import webbrowser
        webbrowser.open(url + ("/v2" if a.lienzo else ""))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
