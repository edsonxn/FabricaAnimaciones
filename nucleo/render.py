# -*- coding: utf-8 -*-
"""Render final: escenas + transiciones + subtítulos + progreso -> segmentos H.264 en paralelo -> concat.

Uso:
  python render.py prueba 12.5 28.1 ...     # cuadros sueltos a previews/
  python render.py video [--procs 13]       # video completo (sin audio) -> salida/video_sin_audio.mp4
"""
import json
import math
import os
import subprocess
import sys
import time
import multiprocessing as mp
import queue
import traceback

import cv2
import numpy as np

import config
import efectos as E
import escenas as S
import estilos
from motor import BLANCO, NEGRO, FPS, H, W, VERTICAL, Lienzo, a_uint8, ancho_texto, componer, e_back, prog, rect_red
from ritmo import env_bombo

TL = json.load(open("timeline.json", encoding="utf-8"))
CLASES = S.CLASES   # cada video define en su escenas.py: id de escena -> clase
TOTAL = TL["total"]
NFRAMES = int(round(TOTAL * FPS))
AMARILLO = (255, 214, 64)
LIM_CH, LIM_PAL = (17, 3) if VERTICAL else (24, 5)     # límites de cada trozo de subtítulo


# ------------------------------------------------------------ subtítulos
def trozos_subtitulos():
    """Agrupa palabras en trozos cortos; el título de cada ítem no se subtitula (ya está en pantalla)."""
    out = []
    for e in TL["escenas"]:
        for fi, f in enumerate(e["frases"]):
            if "num" in e and fi == 0:
                continue
            cur, nch = [], 0
            for w in f["words"]:
                txt = w["w"].strip()
                limpio = txt.rstrip(",.;:")
                cur.append(dict(w=limpio, s=w["s"], e=w["e"]))
                nch += len(limpio) + 1
                if nch > LIM_CH or len(cur) >= LIM_PAL or txt[-1] in ",.;:?!":
                    out.append(cur)
                    cur, nch = [], 0
            if cur:
                out.append(cur)
    for i, c in enumerate(out):
        ini = c[0]["s"] - 0.06
        fin = c[-1]["e"] + 0.35
        if i + 1 < len(out):
            fin = min(fin, out[i + 1][0]["s"] - 0.06)
        c_ = dict(ws=c, ini=ini, fin=max(fin, c[-1]["e"] + 0.02))
        out[i] = c_
    return out


TROZOS = trozos_subtitulos()


def dibujar_subtitulos(lz, t):
    act = [c for c in TROZOS if c["ini"] <= t < c["fin"]]
    if not act:
        return False
    c = act[0]
    px, borde = (74, 10) if VERTICAL else (56, 9)
    # una sola palabra activa: la última que ya empezó (y que no terminó hace rato)
    idx = -1
    for i, w in enumerate(c["ws"]):
        if t >= w["s"] - 0.03:
            idx = i
    if idx >= 0 and t > c["ws"][idx]["e"] + 0.25:
        idx = -1
    esp = ancho_texto(" ", "black", px) + 2 * borde
    kks = [1.1 if i == idx else 1.0 for i in range(len(c["ws"]))]
    anchos = [ancho_texto(w["w"], "black", px) * kk for w, kk in zip(c["ws"], kks)]
    total = sum(anchos) + esp * (len(anchos) - 1)
    k_in = e_back(prog(t, c["ini"], c["ini"] + 0.12), 1.4)
    cx = W / 2
    x = cx - total / 2
    y = H - 400 if VERTICAL else 992
    with lz.grupo(cx, y, 0.9 + 0.1 * k_in):
        with lz.grupo(-cx, -y):
            for i, (w, aw, kk) in enumerate(zip(c["ws"], anchos, kks)):
                dicha = t >= w["s"] - 0.03
                col = AMARILLO if i == idx else (BLANCO if dicha else (215, 215, 222))
                lz.texto(w["w"], x + aw / 2, y - (4 if i == idx else 0), px, "black", color=col, borde=NEGRO,
                         borde_px=borde, k=kk, temblor=0.0, capa=2)
                x += aw + esp
    return True


# ------------------------------------------------------------ progreso 1..10
ITEMS = [e for e in TL["escenas"] if "num" in e]


def dibujar_progreso(lz, t):
    if not ITEMS or t < ITEMS[0]["t0"] - 0.2:
        return False
    actual = 0
    for e in ITEMS:
        if t >= e["t0"]:
            actual = e["num"]
    fin = ITEMS[-1]["t1"]
    ancho, gap = 34, 8
    x0 = 960 - (10 * ancho + 9 * gap) / 2
    for i in range(10):
        n = i + 1
        x = x0 + i * (ancho + gap)
        if n < actual or t >= fin:
            col = AMARILLO
        elif n == actual:
            col = tuple(int(v) for v in np.array(AMARILLO) * (0.75 + 0.25 * env_bombo(t)))
        else:
            col = (70, 70, 90)
        lz.forma(rect_red(x, 16, ancho, 14, 7), col, NEGRO, 3, seed=500 + i, temblor=0.3, capa=2)
    return True


# ------------------------------------------------------------ cuadro completo
class Renderizador:
    def __init__(self):
        self.esc = [CLASES[e["id"]](e, i) for i, e in enumerate(TL["escenas"])]
        self.por_id = {e.id: e for e in self.esc}
        self.lz = Lienzo()

    def escena_en(self, t):
        for e in self.esc:
            if e.t0 <= t < e.t1:
                return e
        return self.esc[-1]

    def cuadro(self, t):
        img = None
        for k, tr in enumerate(TL["transiciones"]):
            if tr["tipo"] == "continua":      # plano secuencia: no hay corte que mezclar
                continue
            if tr["t0"] <= t < tr["t1"]:
                p = (t - tr["t0"]) / (tr["t1"] - tr["t0"])
                A = self.por_id[tr["de"]].render(self.lz, t)
                B = self.por_id[tr["a"]].render(self.lz, t)
                img = E.TRANSICIONES[tr["tipo"]](A, B, p, seed=k * 17 + 3)
                break
        if img is None:
            img = self.escena_en(t).render(self.lz, t)
        img = E.acabado(img, int(t * 10))
        self.lz.nuevo(t)
        a = dibujar_progreso(self.lz, t)
        b = False if (estilos.ACTUAL.get("subs_propios") or not config.SUBTITULOS) else dibujar_subtitulos(self.lz, t)
        if a or b:
            img = componer(img, self.lz.resolver(), estilo=False)
        return a_uint8(img)                 # a_uint8 ya recorta a [0, 1]: sin np.clip (una copia de 24 MB menos)


# ------------------------------------------------------------ paralelo
_R = None


def _init():
    global _R
    cv2.setNumThreads(1)
    try:                                  # un hilo de numba por proceso: ya hay un proceso por núcleo
        import numba
        numba.set_num_threads(1)
    except Exception:
        pass
    _R = Renderizador()


def _trozo(args):
    i0, i1, ruta, preset = args
    if os.path.exists(ruta) and os.path.getsize(ruta) > 1000:
        return ruta, 0.0
    tmp = ruta + ".tmp.mp4"
    # preset medium (antes slow, cambiado 2026-10-04): misma calidad medida (SSIM ±0,0003, PSNR ±0,01 dB), ~38 % menos
    # CPU de codificación y ~5 % más peso. NVENC descartado: el driver admite ~12 sesiones y con 12+ procesos fallaba.
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", preset,
           "-crf", os.environ.get("FAB_CRF", "18"), "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-g", "60", "-threads", "2", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for i in range(i0, i1):
        p.stdin.write(_R.cuadro(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg falló en {ruta}")
    os.replace(tmp, ruta)
    return ruta, time.time() - t0


def _obrero(cola, res, max_tareas=4):
    """Proceso de render: toma segmentos de la cola (hasta max_tareas y sale, para soltar memoria) y avisa al supervisor.
    Si se queda sin memoria, devuelve su segmento a la cola y sale sin tumbar el render."""
    _init()
    for _ in range(max_tareas):
        try:
            t = cola.get(timeout=2)
        except queue.Empty:
            return
        res.put(("ini", os.getpid(), t))
        try:
            ruta, dt = _trozo(t)
            res.put(("ok", os.getpid(), t, dt))
        except MemoryError:
            res.put(("mem", os.getpid(), t))
            return
        except Exception:
            res.put(("err", os.getpid(), t, traceback.format_exc()))
            return


def _memoria_libre():
    """(RAM libre, memoria virtual libre) en GB; None donde no se pueda medir."""
    try:
        import psutil
        ram = psutil.virtual_memory().available / 1e9
    except Exception:
        ram = None
    c = _commit_libre()
    return ram, (None if c is None else c / 1e9)


def _commit_libre():
    """Memoria virtual (commit) libre en bytes: es el límite que de verdad tumba el render en Windows
    (ArrayMemoryError aunque haya RAM libre). None si no se puede medir."""
    if os.name != "nt":
        return None
    import ctypes

    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    ms = MS()
    ms.dwLength = ctypes.sizeof(MS)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms)):
        return None
    return ms.ullAvailPageFile


def _procesos_pesados(min_gb=2.0):
    """Otros procesos que reservan mucha memoria virtual (p. ej. chatterbox_server.py, apps de IA)."""
    try:
        import psutil
    except Exception:
        return []
    out = []
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if p.pid == os.getpid():
                continue
            gb = p.memory_info().private / 1e9 if os.name == "nt" else p.memory_info().rss / 1e9
            if gb >= min_gb:
                cmd = " ".join(p.info["cmdline"] or [])[-70:] or p.info["name"]
                out.append((gb, p.pid, cmd))
        except Exception:
            pass
    return sorted(out, reverse=True)


def procesos_seguros(pedidos, gb_ram=1.5, gb_commit=2.2, reserva_gb=2.0):
    """Limita los procesos a la memoria libre: RAM (~1,5 GB por proceso) y memoria virtual comprometida
    (~2,2 GB por proceso contando su ffmpeg, medido 2026-10-04 en independencia_mx), dejando una reserva."""
    try:
        import psutil
        ram = psutil.virtual_memory().available
    except Exception:
        return pedidos
    cabe = int(ram / 1e9 / gb_ram)
    commit = _commit_libre()
    if commit is not None:
        cabe = min(cabe, int((commit / 1e9 - reserva_gb) / gb_commit))
    cabe = max(2, cabe)
    if cabe < pedidos:
        txt = f"RAM libre {ram / 1e9:.1f} GB" + (f", memoria virtual libre {commit / 1e9:.1f} GB" if commit is not None else "")
        print(f"{txt}: se usan {cabe} procesos en lugar de {pedidos}.")
        pesados = _procesos_pesados()
        if pesados:
            print("  Para usar más procesos, cierra lo que no necesites (memoria virtual reservada):")
            for gb, pid, cmd in pesados[:6]:
                print(f"    {gb:5.1f} GB  pid {pid}  {cmd}")
    return min(pedidos, cabe)


class _SinSuspender:
    """Evita que Windows se suspenda por inactividad mientras dura el render (solo mientras este proceso vive;
    no cambia la configuración de energía). El render v3 de independencia_mx perdió ~13 h con la PC dormida."""

    def __enter__(self):
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        return self

    def __exit__(self, *a):
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)


def _info_segmentos(tam, preset):
    """Lee/escribe segmentos/info.json. Si los segmentos que hay son de otro timeline (otro número de cuadros,
    fps o tamaño de trozo) se borran: ya no sirven. Devuelve el preset de x264 a usar: el de los segmentos
    existentes, para que el concat sin recomprimir no mezcle cabeceras distintas."""
    ruta = "segmentos/info.json"
    info = dict(nframes=NFRAMES, fps=FPS, tam=tam, w=W, h=H)
    segs = [x for x in os.listdir("segmentos") if x.startswith("seg_") and x.endswith(".mp4")]
    previo = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else None
    if segs and previo is not None and any(previo.get(k) != v for k, v in info.items()):
        print(f"los {len(segs)} segmentos existentes son de otro timeline ({previo}): se borran")
        for x in os.listdir("segmentos"):
            os.remove(os.path.join("segmentos", x))
        segs, previo = [], None
    if segs:
        preset = (previo or {}).get("preset", "slow")      # segmentos sin info.json = render anterior a 2026-10-04 (slow)
    info["preset"] = preset
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(info, f)
    return preset


def rehacer(rangos, tam=90):
    """Borra los segmentos que tocan los rangos de tiempo dados ("270-280", en segundos) para re-renderizar solo esos."""
    if not os.path.isdir("segmentos"):
        raise SystemExit("No hay segmentos/ que rehacer: corre el render completo.")
    borrados = set()
    for r in rangos:
        a, b = (float(x) for x in r.split("-"))
        f0, f1 = max(0, int(math.floor(a * FPS))), min(NFRAMES, int(math.ceil(b * FPS)))
        for k in range(f0 // tam, (max(f0, f1 - 1)) // tam + 1):
            ruta = f"segmentos/seg_{k:04d}.mp4"
            if os.path.exists(ruta):
                os.remove(ruta)
            borrados.add(k)
    print(f"segmentos a rehacer: {len(borrados)} ({', '.join(f'{k * tam / FPS:.0f}-{min(NFRAMES, (k + 1) * tam) / FPS:.0f}s' for k in sorted(borrados))})")


def _repartir(tareas, procs, max_procs, t0, gb_ram=1.5, gb_commit=2.2, reserva_gb=2.0, espera=30.0):
    """Supervisor del render: arranca con `procs` procesos y cada pocos segundos mira la memoria libre; si alcanza para
    otro proceso (y pasaron `espera` s desde el último, para que el nuevo ya ocupe su memoria) agrega uno, hasta
    `max_procs`. Si un proceso se queda sin memoria, su segmento vuelve a la cola y el objetivo baja en uno."""
    hechos = sum(1 for _, _, r, _ in tareas if os.path.exists(r) and os.path.getsize(r) > 1000)
    pend = [t for t in tareas if not (os.path.exists(t[2]) and os.path.getsize(t[2]) > 1000)]
    if not pend:
        return
    ctx = mp.get_context("spawn")
    cola, res = ctx.Queue(), ctx.Queue()
    for t in pend:
        cola.put(t)
    restan = len(pend)
    vivos = {}          # pid -> Process
    en_curso = {}       # pid -> tarea
    objetivo = procs
    t_sube = time.time()
    frena_hasta = 0.0

    def lanzar():
        pr = ctx.Process(target=_obrero, args=(cola, res), daemon=True)
        pr.start()
        vivos[pr.pid] = pr

    while restan > 0:
        # 1) mensajes de los procesos
        try:
            while True:
                m = res.get(timeout=1.0)
                tipo, pid, t = m[0], m[1], m[2]
                if tipo == "ini":
                    en_curso[pid] = t
                elif tipo == "ok":
                    en_curso.pop(pid, None)
                    restan -= 1
                    hechos += 1
                    print(f"[{hechos}/{len(tareas)}] {t[2]} {m[3]:.0f}s  (transcurrido {time.time() - t0:.0f}s, "
                          f"{len(vivos)} procesos)", flush=True)
                    # cache_escenas: inicio (este bloque no cuenta en la firma del código, ver cache_escenas._sha_codigo)
                    try:   # anotado al momento: el panel ya puede mostrar la escena fluida sin esperar al final del render
                        import cache_escenas
                        cache_escenas.anotar_segmento(os.getcwd(), os.path.dirname(os.path.abspath(__file__)), t[2])
                    except Exception:              # noqa: BLE001
                        pass
                    # cache_escenas: fin
                elif tipo == "mem":
                    en_curso.pop(pid, None)
                    cola.put(t)
                    objetivo = max(1, min(objetivo, len(vivos)) - 1)
                    frena_hasta = time.time() + 90
                    print(f"sin memoria en {t[2]}: vuelve a la cola; se baja a {objetivo} procesos", flush=True)
                elif tipo == "err":
                    for pr in vivos.values():
                        pr.terminate()
                    raise RuntimeError(f"falló el segmento {t[2]}:\n{m[3]}")
        except queue.Empty:
            pass
        # 2) procesos que terminaron (normal: hicieron sus 4 segmentos o ya no hay cola); si murieron a media tarea, se repite
        for pid, pr in list(vivos.items()):
            if not pr.is_alive():
                pr.join()
                del vivos[pid]
                t = en_curso.pop(pid, None)
                if t is not None:
                    cola.put(t)
                    print(f"un proceso terminó a media tarea ({t[2]}): vuelve a la cola", flush=True)
        # 3) subir de procesos si se liberó memoria
        ahora = time.time()
        en_cola = restan - len(en_curso)
        if (objetivo < max_procs and ahora - t_sube > espera and ahora > frena_hasta and en_cola > len(vivos) - len(en_curso)):
            ram, com = _memoria_libre()
            if (ram is None or ram >= gb_ram) and (com is None or com - reserva_gb >= gb_commit):
                objetivo += 1
                t_sube = ahora
                print(f"memoria libre (RAM {ram or 0:.1f} GB, virtual {com or 0:.1f} GB): se sube a {objetivo} procesos", flush=True)
        # 4) reponer procesos hasta el objetivo (sin pasar de lo que queda por hacer)
        while len(vivos) < min(objetivo, en_cola + len(en_curso)) and en_cola > 0:
            lanzar()
            if len(vivos) >= min(objetivo, restan):
                break
    for pr in vivos.values():
        pr.join(timeout=10)


def video(procs=12, tam=90):
    max_procs = procs
    procs = procesos_seguros(procs)
    os.makedirs("segmentos", exist_ok=True)
    os.makedirs("salida", exist_ok=True)
    preset = _info_segmentos(tam, os.environ.get("FAB_PRESET", "medium"))
    # cache_escenas: inicio (este bloque no cuenta en la firma del código, ver cache_escenas._sha_codigo)
    _ce_firma0, _ce_t0 = None, time.time()
    try:           # escenas renderizadas desde la vista previa del panel: se reutilizan; las hechas con código anterior se rehacen
        import cache_escenas
        cache_escenas.depurar(os.getcwd(), os.path.dirname(os.path.abspath(__file__)))
        _ce_firma0 = cache_escenas.firma_codigo(os.getcwd(), os.path.dirname(os.path.abspath(__file__)))
        cache_escenas.FIRMA_RENDER = _ce_firma0      # cada segmento se anota al terminarlo (ver _repartir)
    except Exception as e:                     # noqa: BLE001  (revisar esa caché nunca debe tumbar un render)
        print(f"(aviso) no se pudo revisar los segmentos de la vista previa: {e}", flush=True)
    # cache_escenas: fin
    tareas = [(i, min(i + tam, NFRAMES), f"segmentos/seg_{i // tam:04d}.mp4", preset) for i in range(0, NFRAMES, tam)]
    faltan = sum(1 for _, _, r, _ in tareas if not (os.path.exists(r) and os.path.getsize(r) > 1000))
    print(f"{faltan} de {len(tareas)} segmentos por renderizar, {procs} procesos, x264 {preset}", flush=True)
    t0 = time.time()
    with _SinSuspender():
        _repartir(tareas, procs, max_procs, t0)
    # cache_escenas: inicio (este bloque no cuenta en la firma del código, ver cache_escenas._sha_codigo)
    try:           # lo que dibujó ESTE render queda anotado: la vista previa del panel pinta esas escenas en verde
        import cache_escenas
        cache_escenas.anotar_render(os.getcwd(), os.path.dirname(os.path.abspath(__file__)), _ce_firma0, _ce_t0)
    except Exception as e:                     # noqa: BLE001
        print(f"(aviso) no se pudieron anotar los segmentos para la vista previa: {e}", flush=True)
    # cache_escenas: fin
    with open("segmentos/lista.txt", "w") as f:
        for _, _, ruta, _ in tareas:
            f.write(f"file '{os.path.basename(ruta)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "segmentos/lista.txt",
                    "-c", "copy", "salida/video_sin_audio.mp4"], check=True)
    print("listo: salida/video_sin_audio.mp4", f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    modo = sys.argv[1]
    if modo == "prueba":
        R = Renderizador()
        os.makedirs("previews", exist_ok=True)
        tiles = []
        for x in sys.argv[2:]:
            t = float(x)
            t0 = time.time()
            im = R.cuadro(t)
            print(f"{t:.2f}s {1000 * (time.time() - t0):.0f} ms")
            cv2.imwrite(f"previews/cuadro_{t:07.2f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
            sm = cv2.resize(im, (360, 640) if VERTICAL else (640, 360), interpolation=cv2.INTER_AREA)
            cv2.putText(sm, f"{t:.2f}", (8, sm.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(sm, f"{t:.2f}", (8, sm.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            tiles.append(sm)
        while len(tiles) % 3:
            tiles.append(np.zeros_like(tiles[0]))
        hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
        cv2.imwrite("previews/hoja_render.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    elif modo == "video":
        procs = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 12
        if "--rehacer" in sys.argv:          # --rehacer 270-280 545-550: solo esos tramos (los demás segmentos se reutilizan)
            i = sys.argv.index("--rehacer") + 1
            rangos = []
            while i < len(sys.argv) and not sys.argv[i].startswith("--"):
                rangos += [x for x in sys.argv[i].split(",") if x]
                i += 1
            rehacer(rangos)
        video(procs)
