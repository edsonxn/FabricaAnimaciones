"""Render completo con supervisor de memoria. Es el que lanza `fab.py <v> video` (antes `-m render video`).

Por qué un módulo aparte (25-nov-2026, historia_aztecas): `cache_escenas` firma los segmentos guardados con el código de
`render.py` y todo lo que importa; cualquier cambio ahí, aunque no toque un píxel, borra los segmentos de TODOS los
videos en su siguiente render. El reparto de procesos no decide ningún píxel, así que vive aquí: `render.py` no cambia
y este archivo se puede mejorar sin invalidar nada (no está en el cierre de imports de render.py ni de guion.py).

Qué arregla respecto al supervisor de render.py (se colgó 1,5 h cuando otra sesión ocupó 10 GB de RAM):
- arranca con pocos procesos (≤ 4) y sube de a uno con lo que MIDE que gasta cada proceso (antes suponía 1,5 GB);
- la falta de memoria también llega como SystemError de OpenCV o como tubería rota de ffmpeg: el segmento se repite;
- si la RAM libre baja de la reserva se quita un proceso; si no cabe ni uno, el render se PAUSA y lo dice en el log;
- un segmento que lleva más de FAB_ATASCO_S (600 s) sin terminar se da por trabado: se mata su proceso y se repite;
- al salir por error se sueltan las colas (antes el proceso principal se quedaba colgado sin escribir nada).

Uso (desde la carpeta del video, con nucleo en PYTHONPATH, igual que render.py):
  python -m render_seguro video [--procs 12] [--rehacer 270-280 ...]
Variables: FAB_PROCS_INICIO (4), FAB_ATASCO_S (600).
"""
import multiprocessing as mp
import os
import queue
import sys
import time
import traceback

import render as R

_SEÑALES_MEMORIA = ("MemoryError", "Unable to allocate", "Insufficient memory", "out of memory",
                    "returned a result with an exception set", "Errno 22", "Errno 32", "BrokenPipe", "Errno 12")


def es_memoria(e, tb):
    """¿El error es falta de memoria? OpenCV la envuelve en SystemError («returned a result with an exception set») y
    si ffmpeg muere sin RAM, escribir en su tubería da OSError Errno 22/32."""
    return isinstance(e, (MemoryError, BrokenPipeError)) or any(s in tb for s in _SEÑALES_MEMORIA)


def _obrero(cola, res, max_tareas=4):
    """Proceso de render: toma segmentos de la cola (hasta max_tareas y sale, para soltar memoria) y avisa al supervisor.
    Si se queda sin memoria, devuelve su segmento a la cola y sale sin tumbar el render."""
    R._init()
    for _ in range(max_tareas):
        try:
            t = cola.get(timeout=2)
        except queue.Empty:
            return
        res.put(("ini", os.getpid(), t))
        try:
            ruta, dt = R._trozo(t)
            res.put(("ok", os.getpid(), t, dt))
        except Exception as e:                   # noqa: BLE001
            tb = traceback.format_exc()
            res.put(("mem", os.getpid(), t) if es_memoria(e, tb) else ("err", os.getpid(), t, tb))
            return


def _gb_por_proceso(pids):
    """Memoria privada máxima (GB) de los procesos de render vivos, contando su ffmpeg; None si no se puede medir."""
    try:
        import psutil
    except Exception:
        return None
    mx = None
    for pid in pids:
        try:
            p = psutil.Process(pid)
            gb = sum((q.memory_info().private if os.name == "nt" else q.memory_info().rss)
                     for q in [p] + p.children()) / 1e9
            mx = gb if mx is None else max(mx, gb)
        except Exception:
            pass
    return mx


def repartir(tareas, procs, max_procs, t0, gb_ram=1.5, gb_commit=2.2, reserva_gb=2.0, espera=30.0, atasco_s=None):
    """Supervisor: misma interfaz que render._repartir (ver la cabecera del módulo para lo que cambia)."""
    atasco_s = atasco_s or float(os.environ.get("FAB_ATASCO_S", "600"))
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
    inicio = {}         # pid -> hora en que empezó su tarea
    objetivo = procs
    t_sube = time.time()
    frena_hasta = 0.0
    t_mide = 0.0
    pausado = False

    def lanzar():
        pr = ctx.Process(target=_obrero, args=(cola, res), daemon=True)
        pr.start()
        vivos[pr.pid] = pr

    try:
        while restan > 0:
            # 1) mensajes de los procesos
            try:
                while True:
                    m = res.get(timeout=1.0)
                    tipo, pid, t = m[0], m[1], m[2]
                    if tipo == "ini":
                        en_curso[pid] = t
                        inicio[pid] = time.time()
                    elif tipo == "ok":
                        en_curso.pop(pid, None)
                        inicio.pop(pid, None)
                        restan -= 1
                        hechos += 1
                        print(f"[{hechos}/{len(tareas)}] {t[2]} {m[3]:.0f}s  (transcurrido {time.time() - t0:.0f}s, "
                              f"{len(vivos)} procesos)", flush=True)
                        try:   # anotado al momento: el panel ya puede mostrar la escena fluida sin esperar al final
                            import cache_escenas
                            cache_escenas.anotar_segmento(os.getcwd(), os.path.dirname(os.path.abspath(R.__file__)), t[2])
                        except Exception:              # noqa: BLE001
                            pass
                    elif tipo == "mem":
                        en_curso.pop(pid, None)
                        inicio.pop(pid, None)
                        cola.put(t)
                        objetivo = max(1, min(objetivo, len(vivos)) - 1)
                        frena_hasta = time.time() + 90
                        print(f"sin memoria en {t[2]}: vuelve a la cola; se baja a {objetivo} procesos", flush=True)
                    elif tipo == "err":
                        raise RuntimeError(f"falló el segmento {t[2]}:\n{m[3]}")
            except queue.Empty:
                pass
            ahora = time.time()
            # 2) procesos que terminaron (normal: hicieron sus 4 segmentos o ya no hay cola); si murieron a media tarea
            #    o su segmento lleva más de atasco_s sin terminar (trabado), el segmento se repite
            for pid, pr in list(vivos.items()):
                trabado = pr.is_alive() and pid in inicio and ahora - inicio[pid] > atasco_s
                if trabado:
                    print(f"{en_curso[pid][2]} lleva {ahora - inicio[pid]:.0f}s sin terminar: se da por trabado", flush=True)
                    pr.terminate()
                if trabado or not pr.is_alive():
                    pr.join(timeout=10)
                    del vivos[pid]
                    inicio.pop(pid, None)
                    t = en_curso.pop(pid, None)
                    if t is not None:
                        cola.put(t)
                        print(f"un proceso terminó a media tarea ({t[2]}): vuelve a la cola", flush=True)
            # 3) medir lo que gasta de verdad cada proceso (cada 20 s)
            if vivos and ahora - t_mide > 20:
                t_mide = ahora
                gb = _gb_por_proceso(list(vivos))
                if gb is not None and gb * 1.15 > gb_ram:
                    if gb * 1.15 - gb_ram >= 0.25 or gb_ram <= 1.5:      # solo se avisa cuando cambia de verdad
                        print(f"cada proceso usa ~{gb:.1f} GB: se calcula con {gb * 1.15:.1f} GB por proceso", flush=True)
                    gb_ram = gb_commit = gb * 1.15
            ram, com = R._memoria_libre()
            # 4) poca memoria (otra sesión la ocupó): un proceso menos; los que sobran salen al acabar su segmento
            if ram is not None and ram < reserva_gb and objetivo > 1 and ahora > frena_hasta:
                objetivo -= 1
                frena_hasta = ahora + 60
                print(f"RAM libre {ram:.1f} GB: se baja a {objetivo} procesos", flush=True)
            # 5) subir de procesos si se liberó memoria
            en_cola = restan - len(en_curso)
            if (objetivo < max_procs and ahora - t_sube > espera and ahora > frena_hasta
                    and en_cola > len(vivos) - len(en_curso)):
                if (ram is None or ram - reserva_gb >= gb_ram) and (com is None or com - reserva_gb >= gb_commit):
                    objetivo += 1
                    t_sube = ahora
                    print(f"memoria libre (RAM {ram or 0:.1f} GB, virtual {com or 0:.1f} GB): se sube a {objetivo} procesos",
                          flush=True)
            # 6) reponer procesos hasta el objetivo, solo si cabe otro en memoria (si no cabe ni uno: pausa)
            while len(vivos) < min(objetivo, en_cola + len(en_curso)) and en_cola > 0:
                ram, com = R._memoria_libre()
                cabe = ((ram is None or ram - reserva_gb / 2 >= gb_ram)
                        and (com is None or com - reserva_gb / 2 >= gb_commit))
                if not cabe:
                    if not vivos and not pausado:
                        pausado = True
                        print(f"PAUSA: RAM libre {ram or 0:.1f} GB, cada proceso necesita ~{gb_ram:.1f} GB; "
                              f"el render sigue solo cuando se libere memoria", flush=True)
                    break
                if pausado:
                    pausado = False
                    print(f"memoria libre otra vez (RAM {ram or 0:.1f} GB): sigue el render", flush=True)
                lanzar()
                if len(vivos) >= min(objetivo, restan):
                    break
            if pausado:
                time.sleep(4)
    finally:
        for pr in vivos.values():
            if restan > 0 and pr.is_alive():
                pr.terminate()
        for q in (cola, res):           # sin esto, salir con datos en la cola deja colgado el proceso principal
            q.cancel_join_thread()
            q.close()
    for pr in vivos.values():
        pr.join(timeout=10)


_procesos_seguros_orig = R.procesos_seguros


def procesos_inicio(pedidos, gb_ram=2.5, gb_commit=2.5, reserva_gb=2.0):
    """Procesos con los que ARRANCA el render: pocos (≤ FAB_PROCS_INICIO, 4) a 2,5 GB cada uno; repartir() sube luego."""
    return min(_procesos_seguros_orig(pedidos, gb_ram=gb_ram, gb_commit=gb_commit, reserva_gb=reserva_gb),
               int(os.environ.get("FAB_PROCS_INICIO", "4")), pedidos)


def instalar():
    """Pone este supervisor en el módulo render (para render.video y quien llame a render._repartir)."""
    R._repartir = repartir
    R.procesos_seguros = procesos_inicio


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "video":
        raise SystemExit("uso: python -m render_seguro video [--procs N] [--rehacer t0-t1 ...]")
    instalar()
    procs = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 12
    if "--rehacer" in sys.argv:          # --rehacer 270-280 545-550: solo esos tramos (los demás segmentos se reutilizan)
        i = sys.argv.index("--rehacer") + 1
        rangos = []
        while i < len(sys.argv) and not sys.argv[i].startswith("--"):
            rangos += [x for x in sys.argv[i].split(",") if x]
            i += 1
        R.rehacer(rangos)
    R.video(procs)
