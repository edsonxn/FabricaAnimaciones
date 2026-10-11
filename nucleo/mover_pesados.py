# -*- coding: utf-8 -*-
"""Mueve carpetas pesadas de los videos (salida/, segmentos/, previews/…) a otro disco y deja en su lugar un
junction (enlace de carpeta de NTFS, sin permisos de administrador): fab.py, el panel y el render siguen usando la
ruta de siempre, pero los bytes viven en el otro disco.

    python nucleo/mover_pesados.py                      # SOLO muestra qué movería (salida*/ de todos los videos)
    python nucleo/mover_pesados.py --aplicar            # lo mueve
    python nucleo/mover_pesados.py --aplicar --subs segmentos,previews satoshi_nakamoto
    python nucleo/mover_pesados.py --deshacer salida satoshi_nakamoto     # lo trae de vuelta a C:

Destino: variable FAB_PESADOS o E:\\FabricaAnimaciones (disco USB: conéctalo antes; si no está, esas rutas fallan).
Seguro: copia (robocopy) -> verifica tamaños -> renombra el original -> crea el junction -> comprueba -> borra el
original. Si algo falla (archivo en uso, disco lleno) vuelve atrás y no pierde nada. No mueve nada que esté en uso.
"""
import fnmatch
import os
import shutil
import stat
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS = os.path.join(RAIZ, "videos")
DESTINO = os.environ.get("FAB_PESADOS", r"E:\FabricaAnimaciones")


def es_enlace(p):
    try:
        return bool(os.lstat(p).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (OSError, AttributeError):
        return False


def crear_junction(enlace, destino):
    """Junction de NTFS sin lanzar procesos (cmd /c mklink falló con WinError 1455 cuando Windows se queda sin memoria virtual)."""
    try:
        import _winapi
        _winapi.CreateJunction(destino, enlace)
    except (ImportError, AttributeError):
        r = subprocess.run(["cmd", "/c", "mklink", "/J", enlace, destino], capture_output=True, text=True)
        if r.returncode:
            raise OSError(r.stdout.strip() or r.stderr.strip())


def tam(p):
    return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs)


def archivos(p):
    return {os.path.relpath(os.path.join(d, f), p): os.path.getsize(os.path.join(d, f))
            for d, _, fs in os.walk(p) for f in fs}


def candidatas(patrones, videos):
    out = []
    for v in sorted(os.listdir(VIDEOS)):
        if videos and v not in videos or v.startswith("_") or not os.path.isdir(os.path.join(VIDEOS, v)):
            continue
        for s in sorted(os.listdir(os.path.join(VIDEOS, v))):
            p = os.path.join(VIDEOS, v, s)
            if os.path.isdir(p) and not s.endswith("__moviendo") and any(fnmatch.fnmatch(s, pat) for pat in patrones):
                out.append((v, s, p))
    return out


def mover(v, s, src, aplicar):
    dst = os.path.join(DESTINO, "videos", v, s)
    if es_enlace(src):
        return f"  {v}/{s}: ya está en otro disco ({os.path.realpath(src)})"
    n = tam(src)
    if not aplicar:
        return f"  {v}/{s}: {n / 1e6:8.0f} MB  ->  {dst}"
    libre = shutil.disk_usage(os.path.splitdrive(DESTINO)[0] + "\\").free
    if n * 1.05 > libre:
        return f"  {v}/{s}: NO cabe en el destino ({n / 1e9:.1f} GB > {libre / 1e9:.1f} GB libres)"
    os.makedirs(dst, exist_ok=True)
    rc = subprocess.run(["robocopy", src, dst, "/E", "/COPY:DAT", "/DCOPY:DAT", "/R:1", "/W:1", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"],
                        capture_output=True).returncode
    if rc >= 8:
        return f"  {v}/{s}: ERROR copiando (robocopy {rc}); el original sigue intacto"
    a, b = archivos(src), archivos(dst)
    malos = [k for k, t in a.items() if b.get(k) != t]
    if malos:
        return f"  {v}/{s}: la copia no coincide ({len(malos)} archivos, p. ej. {malos[0]}); el original sigue intacto"
    viejo = src + "__moviendo"
    try:
        os.rename(src, viejo)                                    # falla si algo lo tiene abierto
    except OSError as e:
        return f"  {v}/{s}: en uso, no se mueve ({e}); el original sigue intacto"
    try:
        crear_junction(src, dst)
        if archivos(src) != b:
            raise OSError("el enlace no muestra los mismos archivos")
    except Exception as e:                                       # noqa: BLE001
        try:
            if es_enlace(src):
                os.rmdir(src)
            os.rename(viejo, src)
        except OSError as e2:
            return f"  {v}/{s}: ATENCIÓN, el original quedó en {viejo} ({e2}); la copia está en {dst}"
        return f"  {v}/{s}: no se pudo crear el enlace ({e}); todo quedó como estaba"
    shutil.rmtree(viejo)
    return f"  {v}/{s}: movido {n / 1e6:.0f} MB  ->  {dst}"


def retomar(aplicar):
    """Carpetas que quedaron a medio mover (`X__moviendo` sin `X`): si la copia en el destino coincide, se termina; si no, se restaura."""
    for v in sorted(os.listdir(VIDEOS)):
        base = os.path.join(VIDEOS, v)
        if not os.path.isdir(base):
            continue
        for s in os.listdir(base):
            if not s.endswith("__moviendo"):
                continue
            src, viejo = os.path.join(base, s[:-len("__moviendo")]), os.path.join(base, s)
            dst = os.path.join(DESTINO, "videos", v, s[:-len("__moviendo")])
            if os.path.exists(src):
                print(f"  {v}/{s}: existe también {os.path.basename(src)}; revisa a mano")
                continue
            ok = os.path.isdir(dst) and archivos(viejo) == archivos(dst)
            print(f"  {v}/{s}: a medio mover; copia en destino {'completa' if ok else 'incompleta'} -> {'terminar' if ok else 'restaurar'}")
            if not aplicar:
                continue
            try:
                if ok:
                    crear_junction(src, dst)
                    if archivos(src) != archivos(dst):
                        raise OSError("el enlace no muestra los mismos archivos")
                    shutil.rmtree(viejo)
                    print(f"    terminado: {src} -> {dst}")
                else:
                    os.rename(viejo, src)
                    print("    restaurado")
            except OSError as e:
                if es_enlace(src):
                    os.rmdir(src)
                    os.rename(viejo, src)
                print(f"    no se pudo ({e}); el original queda en {src if os.path.exists(src) else viejo}")


def deshacer(v, s):
    src = os.path.join(VIDEOS, v, s)
    if not es_enlace(src):
        return f"  {v}/{s}: no es un enlace; nada que deshacer"
    dst = os.path.realpath(src)
    os.rmdir(src)                                                # quita solo el junction, no su contenido
    rc = subprocess.run(["robocopy", dst, src, "/E", "/MOVE", "/COPY:DAT", "/DCOPY:DAT", "/R:1", "/W:1", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"],
                        capture_output=True).returncode
    return f"  {v}/{s}: traído de vuelta a C: (robocopy {rc})"


def main():
    a = sys.argv[1:]
    aplicar = "--aplicar" in a
    patrones = ["salida*"]
    if "--subs" in a:
        patrones = a[a.index("--subs") + 1].split(",")
    if "--deshacer" in a:
        i = a.index("--deshacer")
        s, vids = a[i + 1], a[i + 2:]
        for v in vids:
            print(deshacer(v, s))
        return
    videos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--subs")]
    if not os.path.isdir(os.path.splitdrive(DESTINO)[0] + "\\"):
        raise SystemExit(f"No encuentro el disco de destino ({DESTINO}). Conéctalo o define FAB_PESADOS.")
    os.makedirs(DESTINO, exist_ok=True)
    retomar(aplicar)
    print(("MOVIENDO" if aplicar else "SIMULACIÓN (usa --aplicar)") + f" -> {DESTINO}")
    total = 0
    for v, s, p in candidatas(patrones, videos):
        if not es_enlace(p):
            total += tam(p)
        try:
            print(mover(v, s, p, aplicar), flush=True)
        except Exception as e:                                   # noqa: BLE001  (p. ej. sin memoria para lanzar robocopy)
            print(f"  {v}/{s}: ERROR {e.__class__.__name__}: {e}; se sigue con la siguiente (el original no se toca antes de la copia verificada)", flush=True)
    print(f"total {'procesado' if aplicar else 'a mover'}: {total / 1e9:.1f} GB")


if __name__ == "__main__":
    main()
