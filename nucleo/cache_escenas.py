# -*- coding: utf-8 -*-
"""Escenas renderizadas desde la vista previa -> segmentos del render final (se renderiza una sola vez).

La vista previa renderiza una escena con el MISMO codificador que el render final y deja el resultado en
`segmentos/seg_NNNN.mp4` (tramos de 90 cuadros). El render completo (`render.video`) ya salta los segmentos
que existen, así que esos tramos no se vuelven a dibujar. Para que nunca se cuele un tramo viejo:

  * cada segmento hecho por la vista previa se anota en `segmentos/preview_origen.json` con la FIRMA del
    código que lo dibujó (+ tamaño y fecha del archivo, por si alguien lo reemplaza después);
  * `depurar()` (la llama `render.video`) borra los anotados cuya firma ya no es la del código actual;
  * los segmentos que NO están anotados (render completo normal, `--rehacer`) no se tocan: sigue valiendo
    el flujo de siempre.

La firma = contenido de los módulos que el render importa (cierre de imports desde `render.py`, calculado con
ast, igual en cualquier proceso) + `timeline.json` + `guion.py` + variables FAB_*. No cubre imágenes/datos
sueltos de la carpeta del video: si cambiaste uno, vuelve a renderizar la escena («Volver a renderizar»).
"""
import ast
import hashlib
import json
import os
import re
import threading
import time

SEG = 90                                  # cuadros por segmento (el mismo `tam` de render.video)
NOMBRE = "preview_origen.json"
_cerrojo = threading.RLock()
_memo = {}                                 # ruta -> (mtime_ns, tamaño, sha1)
_memo_cierre = {}                          # (car, nucleo) -> (huellas, lista de archivos)


_BLOQUE = re.compile(rb"^[ \t]*# cache_escenas: inicio.*?^[ \t]*# cache_escenas: fin[^\n]*\n", re.S | re.M)


def _sha(ruta):
    """sha1 del archivo SIN los bloques `# cache_escenas: inicio … # cache_escenas: fin` (el enganche de este módulo
    dentro de render.py no cambia ningún píxel: tocarlo no debe invalidar las escenas guardadas)."""
    st = os.stat(ruta)
    m = _memo.get(ruta)
    if m and m[0] == st.st_mtime_ns and m[1] == st.st_size:
        return m[2]
    with open(ruta, "rb") as f:
        h = hashlib.sha1(_BLOQUE.sub(b"", f.read())).hexdigest()
    _memo[ruta] = (st.st_mtime_ns, st.st_size, h)
    return h


def _ubicar(nombre, car, nucleo):
    """Misma prioridad que PYTHONPATH en el render: carpeta del video primero, luego nucleo."""
    for base in (car, nucleo):
        r = os.path.join(base, nombre + ".py")
        if os.path.isfile(r):
            return r
    return None


EXCLUIR = {"cache_escenas"}                # módulos que el render importa pero que no deciden ningún píxel


def _importados(ruta):
    try:
        arbol = ast.parse(_BLOQUE.sub(b"", open(ruta, "rb").read()))
    except (SyntaxError, ValueError, OSError):
        return set()
    out = set()
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import):
            out |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
            out.add(n.module.split(".")[0])
            out |= {a.name for a in n.names}          # `from kit import piezas`: por si es un módulo propio
    return out


def archivos_render(car, nucleo):
    """Archivos .py que influyen en lo que se dibuja: cierre de imports desde render.py (+ guion.py)."""
    clave = (car, nucleo)
    previo = _memo_cierre.get(clave)
    if previo:
        try:
            if all(os.stat(f).st_mtime_ns == m for f, m in previo[0]):
                return previo[1]
        except OSError:
            pass
    vistos, pila = {}, ["render", "guion"]
    while pila:
        nom = pila.pop()
        if nom in vistos or nom in EXCLUIR:
            continue
        r = _ubicar(nom, car, nucleo)
        vistos[nom] = r
        if r:
            pila.extend(n for n in _importados(r) if n not in vistos)
    arch = sorted(r for r in vistos.values() if r)
    huellas = [(f, os.stat(f).st_mtime_ns) for f in arch]
    _memo_cierre[clave] = (huellas, arch)
    return arch


def firma_codigo(car, nucleo):
    """Firma (sha1) del código + timeline + entorno que decide los píxeles. Barata: memoiza por mtime/tamaño."""
    h = hashlib.sha1()
    for f in archivos_render(car, nucleo):
        h.update((("v/" if os.path.dirname(f) == car else "n/") + os.path.basename(f)).encode())
        h.update(_sha(f).encode())
    tl = os.path.join(car, "timeline.json")
    h.update(_sha(tl).encode() if os.path.isfile(tl) else b"sin-timeline")
    h.update(f"FAB_ESTILO={os.environ.get('FAB_ESTILO', '')}".encode())     # fps/tamaño/preset ya los vigila segmentos/info.json
    return h.hexdigest()[:16]


# ------------------------------------------------------------------ manifiesto de segmentos hechos por la vista previa
def _ruta_manifiesto(car):
    return os.path.join(car, "segmentos", NOMBRE)


def ruta_seg(car, k):
    return os.path.join(car, "segmentos", f"seg_{k:04d}.mp4")


def leer(car):
    try:
        with open(_ruta_manifiesto(car), encoding="utf-8") as f:
            return json.load(f).get("segs", {})
    except (OSError, ValueError):
        return {}


def guardar(car, segs):
    os.makedirs(os.path.join(car, "segmentos"), exist_ok=True)
    tmp = _ruta_manifiesto(car) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"segs": segs}, f)
    os.replace(tmp, _ruta_manifiesto(car))


def _huella_archivo(ruta):
    st = os.stat(ruta)
    return [st.st_size, st.st_mtime_ns]


def anotar(car, ks, firma):
    """Anota los segmentos k (recién escritos por la vista previa) con la firma del código que los dibujó."""
    with _cerrojo:
        man = leer(car)
        for k in ks:
            man[str(k)] = [firma] + _huella_archivo(ruta_seg(car, k))
        guardar(car, man)


def estado_seg(car, k, man, firma):
    """'vigente' (anotado con esta firma), 'obsoleto' (anotado con otra), 'ajeno' (existe sin anotar o
    reemplazado) o 'falta'."""
    ruta = ruta_seg(car, k)
    if not os.path.isfile(ruta) or os.path.getsize(ruta) < 1000:
        return "falta"
    m = man.get(str(k))
    if not m or m[1:] != _huella_archivo(ruta):
        return "ajeno"
    return "vigente" if m[0] == firma else "obsoleto"


def rango_segmentos(i0, i1, nframes):
    """Segmentos [k0, k1) que cubren los cuadros [i0, i1)."""
    k0 = max(0, i0 // SEG)
    k1 = min(-(-nframes // SEG), -(-i1 // SEG))
    return k0, max(k1, k0 + 1)


def adoptar(car, nucleo, ks, firma, margen_s=900):
    """Segmentos de un render completo normal (sin anotar) cuyo archivo se EMPEZÓ a escribir más de `margen_s`
    después de la última edición del código/timeline: se dibujaron con el código actual, se anotan como vigentes.
    (st_ctime en Windows = creación del archivo = inicio de la codificación; el margen cubre los procesos del
    render que siguen con módulos viejos hasta reiniciarse.) Devuelve los k adoptados."""
    if not ks:
        return []
    limite = limite_adopcion(car, nucleo, margen_s)
    ok = [k for k in ks if os.stat(ruta_seg(car, k)).st_ctime > limite]
    if ok:
        anotar(car, ok, firma)
    return ok


FIRMA_RENDER = None      # la pone render.video() al arrancar: firma del código con el que dibujan sus procesos


def anotar_segmento(car, nucleo, ruta):
    """Durante un render completo, en cuanto termina un segmento: lo anota con la firma del arranque si el código no ha
    cambiado desde entonces. Así la escena queda «Ver fluida» al momento, sin esperar al final del render ni a los 15 min."""
    f0 = FIRMA_RENDER
    if not f0 or firma_codigo(car, nucleo) != f0:
        return False
    k = int(re.fullmatch(r"seg_(\d+)\.mp4", os.path.basename(ruta)).group(1))
    with _cerrojo:
        man = leer(car)
        if estado_seg(car, k, man, f0) != "ajeno":
            return False
        man[str(k)] = [f0] + _huella_archivo(ruta_seg(car, k))
        guardar(car, man)
    return True


def anotar_render(car, nucleo, firma0, t_ini, imprimir=print):
    """Al terminar un render completo: los segmentos que ESE render escribió (archivo creado desde `t_ini`, sin anotar) se
    anotan con `firma0` = la firma del código al arrancar (los procesos del render importan los módulos al arrancar). Así las
    escenas quedan verdes en la vista previa sin depender de la regla de los 15 min de `adoptar`. Si el código cambió mientras
    renderizaba no se sabe qué versión dibujó cada tramo: no se anota nada (siguen valiendo las reglas de siempre)."""
    if not firma0 or firma_codigo(car, nucleo) != firma0:
        if firma0:
            imprimir("(aviso) el código cambió durante el render: sus segmentos no se anotan para la vista previa")
        return []
    with _cerrojo:
        man = leer(car)
        nuevos = []
        for f in sorted(os.listdir(os.path.join(car, "segmentos"))):
            m = re.fullmatch(r"seg_(\d+)\.mp4", f)
            if not m:
                continue
            k, ruta = int(m.group(1)), os.path.join(car, "segmentos", f)
            if estado_seg(car, k, man, firma0) == "ajeno" and os.stat(ruta).st_ctime >= t_ini - 1:
                man[str(k)] = [firma0] + _huella_archivo(ruta)
                nuevos.append(k)
        if nuevos:
            guardar(car, man)
    if nuevos:
        imprimir(f"{len(nuevos)} segmentos de este render anotados para la vista previa (escenas en verde)")
    return nuevos


def limite_adopcion(car, nucleo, margen_s=900):
    """Un segmento sin anotar solo sirve si se empezó a escribir DESPUÉS de este instante (última edición del código + margen)."""
    arch = archivos_render(car, nucleo) + [os.path.join(car, "timeline.json")]
    return max(os.stat(f).st_mtime for f in arch if os.path.isfile(f)) + margen_s


def sin_dibujar(car, nucleo, ks, firma=None):
    """Los k de `ks` que ya están hechos y se reutilizan tal cual (vigentes, o de un render completo adoptable): no hay que
    dibujarlos otra vez. Lo usan el panel (qué escenas ya se pueden ver fluidas) y el motor de la vista previa."""
    firma = firma or firma_codigo(car, nucleo)
    man = leer(car)
    limite, out = None, []
    for k in ks:
        e = estado_seg(car, k, man, firma)
        if e == "vigente":
            out.append(k)
        elif e == "ajeno":
            if limite is None:
                limite = limite_adopcion(car, nucleo)
            if os.stat(ruta_seg(car, k)).st_ctime > limite:
                out.append(k)
    return out


def conservar(car, ks, firma):
    """El usuario da por buenos (código cambió pero no tocó esas escenas): reanota con la firma actual."""
    n = 0
    with _cerrojo:
        man = leer(car)
        for k in ks:
            m = man.get(str(k))
            ruta = ruta_seg(car, k)
            if m and os.path.isfile(ruta) and m[1:] == _huella_archivo(ruta):
                man[str(k)] = [firma] + m[1:]
                n += 1
        guardar(car, man)
    return n


def depurar(car, nucleo, imprimir=print):
    """Para el render completo: borra los segmentos de la vista previa hechos con código distinto al actual
    y limpia anotaciones huérfanas. Devuelve (reutilizables, descartados)."""
    if not os.path.isdir(os.path.join(car, "segmentos")):
        return 0, 0
    with _cerrojo:
        man = leer(car)
        if not man:
            return 0, 0
        firma = firma_codigo(car, nucleo)
        buenos, malos = [], []
        for k in sorted(man, key=int):
            e = estado_seg(car, int(k), man, firma)
            if e == "vigente":
                buenos.append(int(k))
            elif e == "obsoleto":
                malos.append(int(k))
                os.remove(ruta_seg(car, int(k)))
            if e in ("obsoleto", "falta", "ajeno"):
                man.pop(k)
        guardar(car, man)
    if buenos:
        imprimir(f"{len(buenos)} segmentos ya renderizados desde la vista previa se reutilizan (no se vuelven a dibujar)")
    if malos:
        imprimir(f"{len(malos)} segmentos de la vista previa estaban hechos con código anterior: se descartan y se rehacen "
                 f"({', '.join(f'{k * SEG}' for k in malos[:8])}{'…' if len(malos) > 8 else ''} = cuadro de inicio)")
    return len(buenos), len(malos)


# ------------------------------------------------------------------ escenas guardadas (mp4 de la vista previa)
def _ruta_escenas(car):
    return os.path.join(car, "previews", "escenas.json")


def leer_escenas(car):
    try:
        with open(_ruta_escenas(car), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def guardar_escenas(car, d):
    os.makedirs(os.path.join(car, "previews"), exist_ok=True)
    tmp = _ruta_escenas(car) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    os.replace(tmp, _ruta_escenas(car))


def listar(car, nucleo):
    """Escenas guardadas con su estado frente al código actual: 'vigente' u 'obsoleta' (o se omite si ya
    no existen sus segmentos/mp4)."""
    ent = leer_escenas(car)
    if not ent:
        return []
    firma = firma_codigo(car, nucleo)
    man = leer(car)
    out = []
    limite = None
    for id_, e in ent.items():
        mp4 = os.path.join(car, "previews", e["mp4"])
        if not os.path.isfile(mp4):
            continue
        estados = [estado_seg(car, k, man, firma) for k in range(e["k0"], e["k1"])]
        if "falta" in estados:
            continue
        if "ajeno" in estados:                 # del render completo aún sin anotar: vale si es adoptable (igual que sin_dibujar)
            if limite is None:
                limite = limite_adopcion(car, nucleo)
            try:
                if any(s == "ajeno" and os.stat(ruta_seg(car, k)).st_ctime <= limite
                       for k, s in zip(range(e["k0"], e["k1"]), estados)):
                    continue
            except OSError:
                continue
            if os.path.getmtime(mp4) < max(os.path.getmtime(ruta_seg(car, k)) for k in range(e["k0"], e["k1"])):
                continue                       # el mp4 es más viejo que los segmentos que dice mostrar
            estados = ["vigente" if s == "ajeno" else s for s in estados]
        ok = all(s == "vigente" for s in estados) and e.get("firma") == firma
        out.append(dict(id=id_, vt0=e["vt0"], vt1=e["vt1"], w=e["w"], mb=round(os.path.getsize(mp4) / 1e6, 1),
                        estado="vigente" if ok else "obsoleta", v=e.get("ts", 0), k0=e["k0"], k1=e["k1"]))
    return out


def conservar_escenas(car, nucleo, ids=None):
    """Da por vigentes las escenas obsoletas (todas, o solo `ids`). Devuelve cuántas."""
    firma = firma_codigo(car, nucleo)
    with _cerrojo:
        ent = leer_escenas(car)
        n = 0
        for e_ in listar(car, nucleo):
            if e_["estado"] != "obsoleta" or (ids and e_["id"] not in ids):
                continue
            conservar(car, range(e_["k0"], e_["k1"]), firma)
            ent[e_["id"]]["firma"] = firma
            n += 1
        guardar_escenas(car, ent)
    return n


def empaquetar_escena(car, id_, k0, k1, nframes, fps, ancho, w_full, firma, hilos=None, baja_prioridad=False):
    """mp4 liviano (con audio) de la escena a partir de sus segmentos 1080p ya hechos: no dibuja nada. Lo registra en
    escenas.json. Lo usan el motor de la vista previa y el panel (que las arma solo mientras corre el render completo)."""
    import subprocess
    car = os.path.abspath(car)
    vt0, vt1 = k0 * SEG / fps, min(k1 * SEG, nframes) / fps
    prev = os.path.join(car, "previews")
    os.makedirs(prev, exist_ok=True)
    sid = re.sub(r"[^\w\-]", "_", id_)
    lista = os.path.join(prev, f"_segs_{sid}_{os.getpid()}.txt")
    with open(lista, "w") as f:
        f.writelines("file '{}'\n".format(ruta_seg(car, k).replace("\\", "/")) for k in range(k0, k1))
    mp4 = f"escena_{sid}.mp4"
    tmp = os.path.join(prev, f"{mp4}.{os.getpid()}.tmp.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista]
    wav = os.path.join(car, "audio", "final.wav")
    if os.path.isfile(wav):
        cmd += ["-ss", f"{vt0:.3f}", "-t", f"{vt1 - vt0:.3f}", "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:a", "aac", "-b:a", "160k", "-shortest"]
    ancho = min(ancho, 1440)                 # el mp4 es solo para mirar: los segmentos a 1080p ya están guardados
    if ancho < w_full:
        cmd += ["-vf", f"scale={ancho}:-2:flags=area"]
    tope = "2M" if ancho <= 480 else "5M" if ancho <= 960 else "9M"      # el grano de película de ciertos estilos dispara el peso
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-maxrate", tope, "-bufsize", f"{2 * int(tope[:-1])}M",
            "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart"]
    if hilos:
        cmd += ["-threads", str(hilos)]
    extra = {}
    if baja_prioridad and os.name == "nt":
        extra["creationflags"] = 0x00004000 | 0x08000000          # BELOW_NORMAL_PRIORITY_CLASS | CREATE_NO_WINDOW
    try:
        subprocess.run(cmd + [tmp], check=True, **extra)
        os.replace(tmp, os.path.join(prev, mp4))
    finally:
        for p in (lista, tmp):
            try:
                os.remove(p)
            except OSError:
                pass
    registrar_escena(car, id_, k0, k1, vt0, vt1, min(ancho, w_full), mp4, firma)


def registrar_escena(car, id_, k0, k1, vt0, vt1, w, mp4, firma):
    with _cerrojo:
        ent = leer_escenas(car)
        ent[id_] = dict(k0=k0, k1=k1, vt0=vt0, vt1=vt1, w=w, mp4=mp4, firma=firma, ts=int(time.time()))
        guardar_escenas(car, ent)
