# -*- coding: utf-8 -*-
"""Prueba rápida de tomas generadas (la corre agente_tomas.py en un proceso aparte, con tiempo límite).

    (cwd = carpeta del proyecto; PYTHONPATH = proyecto;estudio;nucleo)
    python probar_toma.py <borrador.py> <salida_dir> <id1,id2,...> [n_cuadros]

Dibuja n cuadros repartidos por cada toma (con el timeline real o uno PROVISIONAL estimado, que se borra al terminar)
y mide: errores (con la línea del borrador), cobertura (cuánto del cuadro tiene dibujo encima del fondo) y movimiento
(diferencia entre dos cuadros separados 0,4 s). Escribe <salida_dir>/resultado.json y los .jpg.
"""
import importlib.util
import json
import os
import sys
import time
import traceback

os.environ["ESTUDIO_TOMA_ESTRICTO"] = "1"
CARPETA = os.getcwd()


def _traza(ex, borrador):
    tb = traceback.extract_tb(ex.__traceback__)
    lineas = []
    for fr in tb:
        if os.path.abspath(fr.filename) == os.path.abspath(borrador):
            lineas.append(f"línea {fr.lineno}: {fr.line}")
    ultimo = tb[-1] if tb else None
    donde = f" (en {os.path.basename(ultimo.filename)}:{ultimo.lineno} {ultimo.name})" if ultimo else ""
    return f"{type(ex).__name__}: {ex}{donde}" + ("\n" + "\n".join(lineas[-4:]) if lineas else "")


def main():
    borrador, sal, ids = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    os.makedirs(sal, exist_ok=True)
    ruta_tl = os.path.join(CARPETA, "timeline.json")
    temporal = not os.path.exists(ruta_tl)
    res = {}
    try:
        if temporal:
            import muestra_estilo as M
            with open(ruta_tl, "w", encoding="utf-8") as f:
                json.dump(M.timeline_provisional(), f, ensure_ascii=False)
        import cv2
        import numpy as np
        cv2.setNumThreads(4)
        from motor import Lienzo, a_uint8, W
        import efectos as E
        tl = json.load(open(ruta_tl, encoding="utf-8"))
        spec = importlib.util.spec_from_file_location("tomas_borrador", borrador)
        try:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            TOMAS = mod.TOMAS
        except Exception as ex:
            for i in ids:
                res[i] = dict(error=_traza(ex, borrador), cuadros=[])
            raise SystemExit(0)
        lz = Lienzo()
        for idx, d in enumerate(tl["escenas"]):
            if d["id"] not in ids:
                continue
            r = res[d["id"]] = dict(error=None, cuadros=[], t0=d["t0"], t1=d["t1"])
            fab = TOMAS.get(d["id"])
            if fab is None:
                r["error"] = f"El borrador no define TOMAS['{d['id']}']"
                continue
            try:
                esc = fab(d, idx)
            except Exception as ex:
                r["error"] = "Al preparar: " + _traza(ex, borrador)
                continue
            dur = d["t1"] - d["t0"]
            tiempos = [d["t0"] + dur * f for f in ([0.12, 0.35, 0.58, 0.8, 0.95] if n >= 5 else [0.2, 0.55, 0.9])[:n]]
            movs = []
            for j, t in enumerate(tiempos):
                try:
                    t_ = time.time()
                    img = esc.render(lz, t)
                    ms = (time.time() - t_) * 1000
                    img2 = esc.render(lz, t + 0.4)
                    bg = np.asarray(esc.fondo(t), dtype=np.float32)
                    if bg.max() > 1.5:
                        bg = bg / 255.0
                    a = np.asarray(img, dtype=np.float32)
                    cob = float((np.abs(a - bg[..., :3]).max(-1) > 0.07).mean()) if bg.shape[:2] == a.shape[:2] else -1
                    mov = float(np.abs(a - np.asarray(img2, dtype=np.float32)).mean() * 255)
                    movs.append(mov)
                    u8 = a_uint8(E.acabado(img, int(t * 10)))
                    ancho = 960
                    u8 = cv2.resize(u8, (ancho, int(round(u8.shape[0] * ancho / u8.shape[1]))), interpolation=cv2.INTER_AREA)
                    nombre = f"{d['id']}_{j + 1}.jpg"
                    cv2.imwrite(os.path.join(sal, nombre), cv2.cvtColor(u8, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 85])
                    r["cuadros"].append(dict(archivo=nombre, t=round(t, 2), cobertura=round(cob, 3), movimiento=round(mov, 2),
                                             ms=round(ms)))
                except Exception as ex:
                    r["error"] = f"Al dibujar t={t:.2f}s: " + _traza(ex, borrador)
                    break
            r["sfx"] = len(esc.sfx)
    except SystemExit:
        pass
    except Exception as ex:
        res["_general"] = dict(error=f"{type(ex).__name__}: {ex}", detalle=traceback.format_exc()[-1500:])
    finally:
        if temporal:
            try:
                os.remove(ruta_tl)
            except OSError:
                pass
        with open(os.path.join(sal, "resultado.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
