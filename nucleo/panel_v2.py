# -*- coding: utf-8 -*-
"""Panel v2 «Lienzo» (21-oct-2026): backend de http://127.0.0.1:8765/v2 (página nucleo/panel_v2.html).

Un lienzo tipo MiniMax Design: cada video es un tablero con TODO lo producido (guion y voz, imágenes y clips, audio,
pruebas, MASTER) que se puede ver y reproducir ahí mismo; arriba, CPU, RAM, GPU, discos y procesos en vivo.
Lo carga panel.py (`_v2()`) y lo RECARGA SOLO si este archivo cambia: editarlo no exige reiniciar el panel.
Solo lee, salvo las miniaturas (previews/_v2/), el audio liviano para el navegador (previews/_v2/*.m4a) y el
«mostrar en carpeta» (abre el Explorador). `P` = el módulo panel.py en marcha (lo asigna panel.py al cargar).

  /v2                          la página
  /api/v2/sistema              CPU, RAM, discos, E/S, red, GPU y procesos de la fábrica (agrupados por trabajo)
  /api/v2/estado               el estado de /api/estado al instante (el último calculado; el siguiente, en segundo plano)
  /api/v2/portadas             portada de cada proyecto (miniatura de YouTube > MASTER > hoja > última prueba > medio)
  /api/v2/recursos?video=X     todo lo producido de un video, agrupado por carpeta y por columna del tablero
  /api/v2/guion?video=X        escenas y frases (con su toma elegida en voz/final), ESTADO.md y youtube.json
  /v2/archivo/<v>/<ruta>       un archivo del video (con Range: se adelanta en <video>/<audio>)
  /v2/mini/<v>/<ruta>?w=320    miniatura cacheada (cuadro del clip o imagen reducida; PNG si tiene transparencia)
  /v2/oir/<v>/<ruta>           .wav grande -> .m4a liviano cacheado (música/mezclas float32 de cientos de MB)
  POST /api/v2/revelar         {video, ruta}: abre el Explorador con ese archivo seleccionado
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import threading
import time
from urllib.parse import parse_qs, urlparse

try:
    import psutil
except ImportError:                    # sin psutil el lienzo funciona igual, solo sin CPU/RAM ni E/S
    psutil = None

P = None                               # panel.py en marcha (lo asigna panel._v2)
AQUI = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(AQUI, "panel_v2.html")
SIN_VENTANA = getattr(subprocess, "CREATE_NO_WINDOW", 0)

EXT_VID = (".mp4", ".webm", ".mov", ".m4v")
EXT_IMG = (".jpg", ".jpeg", ".png", ".webp", ".gif")
EXT_AUD = (".wav", ".mp3", ".ogg", ".m4a", ".flac")
EXT_TXT = (".md", ".txt", ".srt", ".json")
TIPOS = {".mp4": "video/mp4", ".webm": "video/webm", ".mov": "video/quicktime", ".m4v": "video/mp4",
         ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif",
         ".wav": "audio/wav", ".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".m4a": "audio/mp4", ".flac": "audio/flac",
         ".md": "text/plain; charset=utf-8", ".txt": "text/plain; charset=utf-8", ".srt": "text/plain; charset=utf-8",
         ".json": "application/json; charset=utf-8"}
# carpetas que no son «lo producido»: trozos del render, tomas de voz (la voz sale en el guion), código y cachés
NO_CARPETAS = {"segmentos", "__pycache__", "voz", "datos", "cands", "_minis", "_v2", "node_modules", ".git", "flow"}
MAX_GRUPO = 400                        # archivos por grupo que se mandan al lienzo (el resto se cuenta)
MAX_SUBGRUPOS = 4                      # con más subcarpetas con medios (p. ej. piezas/<25 hojas>) se juntan en un grupo


def _tipo(nombre):
    e = os.path.splitext(nombre)[1].lower()
    return "v" if e in EXT_VID else "i" if e in EXT_IMG else "a" if e in EXT_AUD else "x" if e in EXT_TXT else None


def _orden_natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


# ======================================================================== sistema
# Lo mide UN hilo en segundo plano (cada 2 s mientras alguien mira el lienzo) y la petición devuelve la última lectura
# al instante: con renders en marcha psutil tarda segundos por cada proceso protegido y `tasklist` llegó a 5 minutos.
# Los procesos salen de UNA llamada a Windows (NtQuerySystemInformation, lo mismo que usa el Administrador de tareas).
FABRICA = ("python", "pythonw", "ffmpeg", "ffprobe", "yt-dlp", "node")
EPOCA_NT = 116444736000000000          # 1601 -> 1970 en unidades de 100 ns
NO_OTROS = ("", "idle", "system", "registry", "memory compression", "secure system")


def _compartido():
    """Estado que sobrevive a las recargas de este módulo (vive en panel.py)."""
    return P.__dict__.setdefault("_V2_SIS", {"v": None, "pedido": 0.0, "hilo": None, "cerrojo": threading.Lock(),
                                             "cmd": {}, "prev": None, "io": None, "t_proc": 0.0, "proc": ([], [], 0, 0),
                                             "discos": (0.0, []), "gpu": (0.0, None)})


def _instantanea():
    """{pid: (ppid, nombre, memoria_bytes, cpu_100ns, creado_100ns)} de TODOS los procesos en una sola llamada."""
    import ctypes
    import struct
    ntdll = ctypes.WinDLL("ntdll")
    largo, devuelto = 1 << 20, ctypes.c_ulong(0)
    while True:
        buf = ctypes.create_string_buffer(largo)
        st = ntdll.NtQuerySystemInformation(5, buf, largo, ctypes.byref(devuelto)) & 0xFFFFFFFF   # SystemProcessInformation
        if st == 0:
            break
        if st != 0xC0000004:                                     # STATUS_INFO_LENGTH_MISMATCH: buffer más grande
            raise OSError(f"NtQuerySystemInformation {st:#x}")
        largo = devuelto.value + (1 << 16)
    base, raw, out, off = ctypes.addressof(buf), buf.raw, {}, 0
    while True:                                                  # SYSTEM_PROCESS_INFORMATION de 64 bits
        nxt, = struct.unpack_from("<I", raw, off)
        crea, usr, ker = struct.unpack_from("<qqq", raw, off + 32)
        nlen, = struct.unpack_from("<H", raw, off + 56)
        ptr, = struct.unpack_from("<Q", raw, off + 64)
        pid, ppid = struct.unpack_from("<QQ", raw, off + 80)
        ws, = struct.unpack_from("<Q", raw, off + 144)
        nombre = raw[ptr - base: ptr - base + nlen].decode("utf-16-le", "replace") if ptr and nlen else ""
        out[pid] = (ppid, nombre, ws, usr + ker, crea)
        if not nxt:
            break
        off += nxt
    return out


def _num(s):
    s = (s or "").strip()
    return float(s) if re.match(r"^-?\d+(\.\d+)?$", s) else None


def _gpu():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,"
                            "power.draw,power.limit,fan.speed", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=8, creationflags=SIN_VENTANA)
        c = [x.strip() for x in r.stdout.strip().split("\n")[0].split(",")]
        d = dict(nombre=c[0], uso=_num(c[1]), mem=_num(c[2]), mem_total=_num(c[3]), temp=_num(c[4]), watts=_num(c[5]),
                 watts_max=_num(c[6]), ventilador=_num(c[7]), procesos=[])
        r = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,used_memory", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=8, creationflags=SIN_VENTANA)
        for linea in r.stdout.strip().splitlines():
            p = [x.strip() for x in linea.split(",")]
            if p and p[0].isdigit():
                d["procesos"].append(dict(pid=int(p[0]), mem=_num(p[1]) if len(p) > 1 else None))
        return d
    except Exception:                                    # noqa: BLE001  (sin nvidia-smi: sin tarjeta)
        return None


def _discos():
    out = []
    parts = psutil.disk_partitions(all=False) if psutil else []
    letras = [p.mountpoint for p in parts if "fixed" in (p.opts or "") or p.fstype] or ["C:\\", "E:\\"]
    for m in letras:
        try:
            u = shutil.disk_usage(m)
        except OSError:
            continue
        out.append(dict(unidad=m.rstrip("\\"), libre_gb=round(u.free / 1e9, 1), total_gb=round(u.total / 1e9),
                        pct=round(100 * u.used / u.total, 1) if u.total else 0))
    return out


def _video_de(texto):
    m = re.search(r"videos[\\/]+([\w\-]+)", texto or "")
    return m.group(1) if m else None


def _rol(nombre, cmd, cwd=None):
    """(qué es, video) de un proceso de la fábrica, leído de su línea de comandos."""
    c = " ".join(cmd) if isinstance(cmd, (list, tuple)) else (cmd or "")
    vid = _video_de(c) or _video_de(cwd)
    if "panel.py" in c or re.search(r"fab\.py\s+panel\b", c):
        return "Panel de la fábrica", None
    if "preview_worker" in c:
        return "Motor de vista previa", vid
    if "chatterbox_server" in c:
        return "Chatterbox · servidor de voz", None
    m = re.search(r"fab\.py\s+([\w\-]+)(?:\s+([\w\-]+))?", c)
    if m:
        a, b = m.group(1), m.group(2) or ""
        if P and os.path.isfile(os.path.join(P.VIDEOS, a, "guion.py")):          # fab.py <video> <etapa>
            return f"fab.py {b or 'todo'}", a
        return f"fab.py {a} {b}".strip(), None
    m = re.search(r"-m\s+([\w\.]+)", c)
    if m:
        return f"{m.group(1)} (módulo)", vid
    m = re.search(r"([\w\-]+\.py)\b", c)
    if m:
        return m.group(1), vid
    return nombre, vid


def _cmd(c, pid, crea):
    """Línea de comandos (y carpeta, para `python -m`) de un proceso: se lee UNA vez por proceso."""
    k = (pid, crea)
    if k not in c["cmd"]:
        cmd, cwd = [], None
        try:
            pr = psutil.Process(pid)
            cmd = pr.cmdline()
            if "-m" in cmd:
                cwd = pr.cwd()
        except Exception:                                # noqa: BLE001
            pass
        c["cmd"][k] = (cmd, cwd)
    return c["cmd"][k]


def _procesos(c, ncpu):
    """Procesos de la fábrica agrupados por TRABAJO (un render = fab.py + sus 12 procesos + ffmpeg) y el resto del
    equipo agrupado por programa, con la CPU medida entre dos instantáneas."""
    ahora, snap = time.time(), _instantanea()
    prev, c["prev"] = c["prev"], (ahora, snap)
    dt = ahora - prev[0] if prev else 0.0

    def cpu_de(pid, t, crea):
        q = prev[1].get(pid) if prev and dt > 0 else None
        return max(0.0, (t - q[3]) / 1e7 / dt / ncpu * 100) if q and q[4] == crea else 0.0

    fab, otros = {}, {}
    for pid, (ppid, nombre, ws, t, crea) in snap.items():
        base = nombre.lower()[:-4] if nombre.lower().endswith(".exe") else nombre.lower()
        cpu = cpu_de(pid, t, crea)
        if base in FABRICA:
            cmd, cwd = _cmd(c, pid, crea)
            rol, vid = _rol(base, cmd, cwd)
            fab[pid] = dict(pid=pid, ppid=ppid, nombre=base, rol=rol, video=vid, cpu=cpu, ram=ws / 1048576,
                            desde=int((crea - EPOCA_NT) / 1e7), cmd=" ".join(cmd)[-260:])
        elif pid > 4 and base not in NO_OTROS:
            o = otros.setdefault(base, dict(nombre=base, n=0, cpu=0.0, ram=0.0))
            o["n"] += 1
            o["cpu"] += cpu
            o["ram"] += ws / 1048576
    vivos = set(snap)
    c["cmd"] = {k: v for k, v in c["cmd"].items() if k[0] in vivos}

    def raiz(p):                                     # el antepasado de la fábrica más alto (fab.py, panel.py…)
        visto = 0
        while p["ppid"] in fab and visto < 12:
            p, visto = fab[p["ppid"]], visto + 1
        return p

    trabajos = {}
    for p in fab.values():
        r = raiz(p)
        tr = trabajos.setdefault(r["pid"], dict(r, hijos=[], cpu_total=0.0, ram_total=0.0))
        tr["cpu_total"] += p["cpu"]
        tr["ram_total"] += p["ram"]
        if p is not r:
            tr["hijos"].append(dict(pid=p["pid"], rol=p["rol"], nombre=p["nombre"], cpu=round(p["cpu"], 1), ram=round(p["ram"])))
    lista = []
    for tr in trabajos.values():
        modulos = sorted({h["rol"].replace(" (módulo)", "") for h in tr["hijos"] if h["rol"].endswith("(módulo)")})
        tr["etapa"] = ", ".join(modulos)
        tr["hijos"].sort(key=lambda h: -h["ram"])
        tr["cpu"], tr["cpu_total"], tr["ram"], tr["ram_total"] = (round(tr["cpu"], 1), round(tr["cpu_total"], 1),
                                                                  round(tr["ram"]), round(tr["ram_total"]))
        tr.pop("ppid", None)
        lista.append(tr)
    lista.sort(key=lambda x: -x["ram_total"])
    top = sorted(otros.values(), key=lambda o: -o["ram"])[:12]
    for o in top:
        o["cpu"], o["ram"] = round(o["cpu"], 1), round(o["ram"])
    n_py = sum(1 for p in fab.values() if p["nombre"].startswith("python"))
    n_ff = sum(1 for p in fab.values() if p["nombre"].startswith("ffmpeg"))
    return lista, top, n_py, n_ff


def _tasas(c):
    """MB/s de disco (lectura/escritura) y de red (bajada/subida) desde la lectura anterior."""
    ahora = time.time()
    d, r = psutil.disk_io_counters(), psutil.net_io_counters()
    out = dict(disco_lee=None, disco_esc=None, red_baja=None, red_sube=None)
    if c["io"] and ahora > c["io"][0]:
        t0, d0, r0 = c["io"]
        dt = ahora - t0
        out.update(disco_lee=round((d.read_bytes - d0.read_bytes) / dt / 1048576, 1),
                   disco_esc=round((d.write_bytes - d0.write_bytes) / dt / 1048576, 1),
                   red_baja=round((r.bytes_recv - r0.bytes_recv) / dt / 1048576, 2),
                   red_sube=round((r.bytes_sent - r0.bytes_sent) / dt / 1048576, 2))
    c["io"] = (ahora, d, r)
    return out


def _muestrear():
    """Una lectura completa (la llama el hilo de fondo): CPU/RAM/E-S cada vez, procesos cada 4 s, GPU cada 3 s,
    discos cada 10 s."""
    c = _compartido()
    ahora = time.time()
    d = dict(t=ahora)
    if ahora - c["discos"][0] > 10:
        c["discos"] = (ahora, _discos())
    if ahora - c["gpu"][0] > 3:
        c["gpu"] = (ahora, _gpu())
    d["discos"], d["gpu"] = c["discos"][1], c["gpu"][1]
    if psutil:
        ncpu = psutil.cpu_count() or 1
        vm = psutil.virtual_memory()
        d.update(cpu=dict(uso=psutil.cpu_percent(None), nucleos=psutil.cpu_percent(None, percpu=True), n=ncpu),
                 ram=dict(usado_gb=round((vm.total - vm.available) / 1e9, 1), total_gb=round(vm.total / 1e9, 1), pct=vm.percent),
                 io=_tasas(c))
        if ahora - c["t_proc"] > 4:
            try:
                c["proc"] = _procesos(c, ncpu)
            except Exception as e:                       # noqa: BLE001
                d["error_procesos"] = str(e)
            c["t_proc"] = ahora
        d["procesos"], d["otros"], d["n_python"], d["n_ffmpeg"] = c["proc"]
    if d["gpu"]:
        quien = {}
        for tr in d.get("procesos") or []:
            quien[tr["pid"]] = tr
            for h in tr["hijos"]:
                quien[h["pid"]] = tr
        d["gpu"] = dict(d["gpu"], procesos=[dict(g, rol=quien[g["pid"]]["rol"], video=quien[g["pid"]]["video"])
                                            for g in d["gpu"]["procesos"] if g["pid"] in quien])   # solo los de la fábrica
    c["v"] = d


def _hilo():
    """Muestreo en segundo plano; duerme si nadie mira el lienzo en 60 s. Siempre corre la versión vigente del módulo."""
    while True:
        c = P.__dict__.get("_V2_SIS") or {}
        if time.time() - c.get("pedido", 0) < 60:
            try:
                P._v2()._muestrear()
            except Exception as e:                       # noqa: BLE001
                c["error"] = str(e)
            time.sleep(2)
        else:
            time.sleep(1)


def sistema():
    c = _compartido()
    c["pedido"] = time.time()
    with c["cerrojo"]:
        if not (c["hilo"] and c["hilo"].is_alive()):
            c["hilo"] = threading.Thread(target=_hilo, daemon=True, name="lienzo-sistema")
            c["hilo"].start()
    v = c["v"]
    if not v:
        return dict(cargando=True, error=c.get("error"))
    return dict(v, edad=round(time.time() - v["t"], 1))


# ======================================================================== estado de los proyectos al instante
def estado_rapido():
    """El último estado del panel YA calculado, al instante, y el siguiente se calcula en segundo plano (una sola vez a la
    vez): con la CPU al 100 % por un render, escanear los ~90 videos llegó a tardar 4 minutos y el lienzo esperaba en
    blanco. Solo la primera lectura (sin nada calculado) hace esperar."""
    c = _compartido()
    v = P._est.get("v")
    if v is None:
        d = dict(P.estado_cache())
    else:
        if time.time() - P._est.get("t", 0) > 2.5:
            with c["cerrojo"]:
                h = c.get("hilo_est")
                if not (h and h.is_alive()):
                    c["hilo_est"] = threading.Thread(target=P.estado_cache, daemon=True, name="lienzo-estado")
                    c["hilo_est"].start()
        d = dict(v)
    d["avisos"] = P.LOC.recientes() if P.LOC else []
    d["voz"] = P.LOC.info() if P.LOC else dict(activo=False, destino="bocinas", modelo="inactivo", cola=0, voz="")
    d["edad"] = round(time.time() - P._est.get("t", time.time()), 1)
    return d


# ======================================================================== portadas y recursos
_POR = {"t": 0.0, "v": None}


def _archivos(carpeta):
    try:
        return [e for e in os.scandir(carpeta) if e.is_file()]
    except OSError:
        return []


def _subcarpetas(carpeta):
    try:
        return sorted((e for e in os.scandir(carpeta) if e.is_dir() and e.name not in NO_CARPETAS
                       and not e.name.startswith(".")), key=lambda e: e.name)
    except OSError:
        return []


def portadas():
    if _POR["v"] is not None and time.time() - _POR["t"] < 20:
        return _POR["v"]
    out = {}
    for n in os.listdir(P.VIDEOS):
        car = os.path.join(P.VIDEOS, n)
        if n.startswith("_") or not os.path.isfile(os.path.join(car, "guion.py")):
            continue
        sal = _archivos(os.path.join(car, "salida"))
        img = [e for e in sal if _tipo(e.name) == "i"]
        vid = [e for e in sal if _tipo(e.name) == "v"]
        elegido = (next((e for e in img if "miniatura" in e.name.lower()), None) or (img[0] if img else None)
                   or next((e for e in vid if "MASTER" in e.name), None) or (max(vid, key=lambda e: e.stat().st_mtime) if vid else None))
        rel = "salida/" + elegido.name if elegido else None
        if not rel:
            pv = [e for e in _archivos(os.path.join(car, "previews")) if _tipo(e.name) == "i"]
            hoja = next((e for e in pv if e.name in ("final_hoja.jpg", "hoja_render.jpg", "miniaturas.jpg")), None)
            elegido = hoja or (max(pv, key=lambda e: e.stat().st_mtime) if pv else None)
            rel = "previews/" + elegido.name if elegido else None
        if not rel:
            md = sorted((e for e in _archivos(os.path.join(car, "medios")) if _tipo(e.name) in ("i", "v")),
                        key=lambda e: _orden_natural(e.name))
            if md:
                elegido, rel = md[0], "medios/" + md[0].name
        if rel:
            out[n] = dict(r=rel, m=int(elegido.stat().st_mtime))
    _POR.update(t=time.time(), v=out)
    return out


def _columna(grupo, items):
    raiz = grupo.split("/")[0]
    if raiz == "salida" or raiz.startswith("miniatura"):
        return "entrega"
    if raiz.startswith("previews"):
        return "pruebas"
    if (items and all(i["t"] in ("a", "x") for i in items)) or raiz in ("audio", "sfx") or raiz.startswith("sfx"):
        return "audio"
    return "visual"


def recursos(nombre):
    car = P._car_video(nombre)
    if not car:
        return dict(error="video desconocido")
    grupos, firma = [], 0.0

    def items(rel, entradas, sub=""):
        nonlocal firma
        its = []
        for e in entradas:
            t = _tipo(e.name)
            if not t or ".tmp" in e.name or "_tmp." in e.name or (t == "x" and rel not in ("salida", "audio")):
                continue
            st = e.stat()
            its.append(dict(n=(sub + "/" if sub else "") + e.name, r=(rel + "/" if rel else "") + (sub + "/" if sub else "") + e.name,
                            t=t, b=st.st_size, m=int(st.st_mtime)))
            firma = max(firma, st.st_mtime)
        return its

    def agrega(rel, its, nota=""):
        if not its:
            return
        if rel.startswith("previews"):
            its.sort(key=lambda i: -i["m"])                       # pruebas: lo último primero
        else:
            its.sort(key=lambda i: _orden_natural(i["n"]))
        grupos.append(dict(id=rel or "raiz", nombre=rel or "raíz del video", nota=nota, total=len(its), items=its[:MAX_GRUPO],
                           columna=_columna(rel, its) if rel else ("audio" if all(i["t"] == "a" for i in its) else "visual"),
                           tipos={k: sum(1 for i in its if i["t"] == k) for k in "viax"}))

    agrega("", [i for i in items("", _archivos(car)) if i["t"] != "x"])
    for d in _subcarpetas(car):
        agrega(d.name, items(d.name, _archivos(d.path)))
        nietos = [(s.name, items(d.name, _archivos(s.path), s.name)) for s in _subcarpetas(d.path)]
        nietos = [(n, its) for n, its in nietos if its]
        if len(nietos) > MAX_SUBGRUPOS:                           # piezas/<25 hojas>: un solo grupo, con la subcarpeta en el nombre
            agrega(d.name + "/*", [i for _, its in nietos for i in its], nota=f"{len(nietos)} carpetas")
        else:
            for n, its in nietos:
                for i in its:
                    i["n"] = i["n"].split("/", 1)[1]
                agrega(d.name + "/" + n, its)
    textos = {k: P.mt(os.path.join(car, k)) for k in ("guion.py", "timeline.json", "ESTADO.md", "youtube.json")}
    return dict(video=nombre, grupos=grupos, firma=int(firma), firma_textos=int(max(textos.values() or [0])),
                n_voz=len([1 for e in _archivos(os.path.join(car, "voz", "final")) if e.name.endswith(".wav")]))


def guion(nombre):
    car = P._car_video(nombre)
    if not car:
        return dict(error="video desconocido")
    g = P.parsear_guion(os.path.join(car, "guion.py"))
    tl = P.leer_json(os.path.join(car, "timeline.json"), {}) or {}
    voces = {e.name[:-4] for e in _archivos(os.path.join(car, "voz", "final")) if e.name.endswith(".wav")}
    por_id = {e.get("id"): e for e in tl.get("escenas", []) if isinstance(e, dict)}
    escenas = []
    for i, e in enumerate(g.get("ESCENAS") or []):
        if not isinstance(e, dict):
            continue
        t = por_id.get(e.get("id")) or {}
        tf = t.get("frases") or []
        frases = []
        for j, f in enumerate(e.get("frases") or []):
            txt = f if isinstance(f, str) else (f.get("texto") or f.get("t") or str(f)) if isinstance(f, dict) else str(f)
            x = tf[j] if j < len(tf) and isinstance(tf[j], dict) else {}
            key = x.get("key") or f"{e.get('id')}_{j}"
            frases.append(dict(key=key, texto=txt, t0=x.get("t0"), voz=key in voces))
        escenas.append(dict(id=e.get("id") or f"escena_{i + 1}", t0=t.get("t0"), t1=t.get("t1"), frases=frases))
    estado = ""
    try:
        with open(os.path.join(car, "ESTADO.md"), encoding="utf-8", errors="replace") as f:
            estado = f.read(20000)
    except OSError:
        pass
    yt = P.leer_json(os.path.join(car, "youtube.json"), None)
    return dict(video=nombre, titulo=g.get("TITULO") or nombre, estilo=g.get("ESTILO_VISUAL", ""), motor=g.get("MOTOR", ""),
                escenas=escenas, total=tl.get("total"), estado_md=estado, youtube=yt)


# ======================================================================== archivos, miniaturas y audio liviano
def _real(nombre, rel):
    """Ruta real de <video>/<rel> si es un archivo permitido dentro del video (vale si la subcarpeta es un junction)."""
    car = P._car_video(nombre)
    partes = [x for x in (rel or "").replace("\\", "/").split("/") if x]
    if not car or not partes or any(x in (".", "..") or ":" in x for x in partes) or not _tipo(partes[-1]):
        return None
    real = os.path.realpath(os.path.join(car, *partes))
    base = os.path.realpath(os.path.join(car, partes[0])) if len(partes) > 1 else car
    dentro = real.startswith(base + os.sep) if len(partes) > 1 else os.path.dirname(real) == car
    return real if dentro and os.path.isfile(real) else None


_sem_mini = threading.BoundedSemaphore(3)             # no más de 3 miniaturas a la vez (no estorbar a un render)


def mini(nombre, rel, ancho):
    real = _real(nombre, rel)
    if not real or _tipo(real) not in ("i", "v"):
        return None, None
    ancho = max(64, min(960, ancho))
    st = os.stat(real)
    clave = hashlib.sha1(f"{rel}|{int(st.st_mtime)}|{st.st_size}|{ancho}".encode("utf-8")).hexdigest()[:20]
    dst_dir = os.path.join(P.VIDEOS, nombre, "previews", "_v2")
    for ext, tipo in ((".jpg", "image/jpeg"), (".png", "image/png")):
        dst = os.path.join(dst_dir, clave + ext)
        if os.path.isfile(dst):
            return open(dst, "rb").read(), tipo
    import cv2
    import numpy as np
    with _sem_mini:
        if _tipo(real) == "v":
            cap = cv2.VideoCapture(real)
            n = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (0.3 if n > 300 else 0.5)))
            ok, im = cap.read()
            cap.release()
        else:
            im = cv2.imdecode(np.fromfile(real, np.uint8), cv2.IMREAD_UNCHANGED)
            ok = im is not None
        if not ok or im is None:
            return None, None
        if im.dtype != np.uint8:                              # PNG de 16 bits
            im = (im / 257).astype(np.uint8)
        if im.ndim == 2:
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        alfa = im.shape[2] == 4 and im[:, :, 3].min() < 250
        if im.shape[2] == 4 and not alfa:
            im = im[:, :, :3]
        h, w = im.shape[:2]
        if w > ancho:
            im = cv2.resize(im, (ancho, max(1, round(h * ancho / w))), interpolation=cv2.INTER_AREA)
        os.makedirs(dst_dir, exist_ok=True)
        ext, tipo = (".png", "image/png") if alfa else (".jpg", "image/jpeg")
        ok, buf = cv2.imencode(ext, im, [cv2.IMWRITE_JPEG_QUALITY, 80] if ext == ".jpg" else [cv2.IMWRITE_PNG_COMPRESSION, 6])
        if not ok:
            return None, None
        datos = buf.tobytes()
        tmp = os.path.join(dst_dir, clave + ".tmp" + ext)
        with open(tmp, "wb") as f:
            f.write(datos)
        os.replace(tmp, os.path.join(dst_dir, clave + ext))
        return datos, tipo


_oir_lock = threading.Lock()


def oir(nombre, rel):
    """.wav -> previews/_v2/<clave>.m4a (aac 160k): la música float32 de 300 MB pesa ~5 MB y empieza a sonar ya."""
    real = _real(nombre, rel)
    if not real or not real.lower().endswith(".wav"):
        return real
    if os.path.getsize(real) < 25 * 1048576:
        return real
    st = os.stat(real)
    clave = hashlib.sha1(f"{rel}|{int(st.st_mtime)}|{st.st_size}".encode("utf-8")).hexdigest()[:20]
    m4a = os.path.join(P.VIDEOS, nombre, "previews", "_v2", clave + ".m4a")
    with _oir_lock:
        if not os.path.isfile(m4a):
            os.makedirs(os.path.dirname(m4a), exist_ok=True)
            tmp = m4a[:-4] + "_tmp.m4a"
            r = subprocess.run([P._ffmpeg("ffmpeg"), "-y", "-loglevel", "error", "-i", real, "-ac", "2", "-c:a", "aac", "-b:a", "160k",
                                "-movflags", "+faststart", tmp], capture_output=True, timeout=600, creationflags=SIN_VENTANA)
            if r.returncode != 0 or not os.path.isfile(tmp):
                return real
            os.replace(tmp, m4a)
    return m4a


def revelar(nombre, rel):
    real = _real(nombre, rel) if rel else P._car_video(nombre)
    if not real:
        raise ValueError("archivo desconocido")
    if os.path.isdir(real):
        subprocess.Popen(["explorer", real])
    else:
        subprocess.Popen(["explorer", "/select,", real])
    return dict(ok=True)


# ======================================================================== rutas (las llama panel.Manejador)
def _vivo():
    """El lector del agente (agente_vivo.py), recargado si cambió, como este módulo: no exige reiniciar el panel."""
    import importlib
    import agente_vivo as m
    t = os.path.getmtime(m.__file__)
    c = _compartido()
    if c.get("vivo_t") not in (None, t):
        m = importlib.reload(m)
    c["vivo_t"] = t
    return m


_VIVO = {"t": 0.0}


def proyecto_vivo(nombre):
    """Etapas del video para /v2/vivo: del último estado calculado, sin pedir otro escaneo más de una vez cada 20 s."""
    if not nombre:
        return None
    if time.time() - _VIVO["t"] > 20:
        _VIVO["t"] = time.time()
        estado_rapido()
    v = P._est.get("v") or {}
    p = next((x for x in v.get("proyectos") or [] if x.get("nombre") == nombre), None)
    if not p:
        return None
    E = p.get("etapas") or {}
    return dict(titulo=p.get("titulo") or nombre, canal=p.get("canal"), progreso=p.get("progreso") or 0, etapa_actual=p.get("etapa_actual"),
                etapas=[dict(id=e["id"], nombre=e["nombre"], estado=(E.get(e["id"]) or {}).get("estado"),
                             progreso=(E.get(e["id"]) or {}).get("progreso") or 0, detalle=(E.get(e["id"]) or {}).get("detalle") or "")
                        for e in v.get("etapas") or [] if e["id"] in E])


def _json(h, d, cache="no-store"):
    h._enviar(200, json.dumps(d, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", cache=cache)


def get(h, ruta):
    q = parse_qs(urlparse(h.path).query)
    arg = lambda k, d="": (q.get(k) or [d])[0]                       # noqa: E731
    if ruta in ("/v2", "/v2/", "/v2/index.html"):
        return h._enviar(200, open(HTML, "rb").read(), "text/html; charset=utf-8")
    if ruta.rstrip("/") == "/v2/vivo":
        return h._enviar(200, open(os.path.join(AQUI, "panel_vivo.html"), "rb").read(), "text/html; charset=utf-8", cache="no-cache")
    if ruta == "/api/v2/agente":
        try:
            desde = int(arg("desde", "0"))
        except ValueError:
            desde = 0
        r = _vivo().eventos(arg("sesion"), arg("video"), desde)
        r["proyecto"] = proyecto_vivo(r.get("video"))
        return _json(h, r)
    if ruta == "/api/v2/agente/sesiones":
        return _json(h, _vivo().sesiones())
    if ruta.startswith("/v2/vivo/img/"):
        partes = ruta[len("/v2/vivo/img/"):].split("/")
        real = _vivo().imagen(*partes) if len(partes) == 2 else None
        if not real:
            return h._enviar(404, b"", "text/plain")
        return h._enviar(200, open(real, "rb").read(), "image/jpeg", cache="max-age=86400")
    if ruta == "/api/v2/sistema":
        return _json(h, sistema())
    if ruta == "/api/v2/estado":
        return _json(h, estado_rapido())
    if ruta == "/api/v2/portadas":
        return _json(h, portadas())
    if ruta == "/api/v2/recursos":
        return _json(h, recursos(arg("video")))
    if ruta == "/api/v2/guion":
        return _json(h, guion(arg("video")))
    for pref in ("/v2/archivo/", "/v2/mini/", "/v2/oir/"):
        if ruta.startswith(pref):
            partes = ruta[len(pref):].split("/", 1)
            if len(partes) != 2:
                return h._enviar(404, b"", "text/plain")
            nombre, rel = partes
            if pref == "/v2/mini/":
                try:
                    ancho = int(arg("w", "320"))
                except ValueError:
                    ancho = 320
                datos, tipo = mini(nombre, rel, ancho)
                if not datos:
                    return h._enviar(404, b"", "text/plain")
                return h._enviar(200, datos, tipo, cache="max-age=86400")
            real = oir(nombre, rel) if pref == "/v2/oir/" else _real(nombre, rel)
            if not real:
                return h._enviar(404, b"", "text/plain")
            tipo = TIPOS.get(os.path.splitext(real)[1].lower(), "application/octet-stream")
            if tipo.startswith(("text/", "application/json")):
                return h._enviar(200, open(real, "rb").read(), tipo)
            return P._servir_rango(h, real, tipo)
    h._enviar(404, b"no encontrado", "text/plain")


def post(h, ruta, datos):
    if ruta == "/api/v2/revelar":
        return _json(h, revelar(str(datos.get("video", "")), str(datos.get("ruta", ""))))
    h._enviar(404, b"", "text/plain")
