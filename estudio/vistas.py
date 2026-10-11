# -*- coding: utf-8 -*-
"""Vistas previas de 20 s por estilo (estudio/vistas/<estilo>.mp4 + .json con su origen).

1) Si ya hay un video TERMINADO con ese estilo se recortan sus primeros 20 s: primero proyectos del Estudio, luego videos
   de la Fábrica (videos/*/salida/*_MASTER.mp4 cuyo ESTILO_VISUAL coincide).
2) Si no hay ninguno, «Generar» dibuja una muestra de 20 s con el guion de muestra: animación + música + efectos, SIN
   narración (no usa la GPU: render, musica y sfx; el audio se mezcla aquí con ffmpeg). Va por la cola de trabajos pesados."""
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SEG = 20
import proyecto as P  # noqa: E402
DIR = os.path.join(P.DATOS, "vistas")       # en E: junto a los proyectos
import trabajos as T  # noqa: E402

_estado = {}            # estilo -> dict(estado, pct, mensaje, error)
_NO_VENTANA = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def info(eid):
    """Vista disponible: dict(url_ver, origen, formato) o None; más el estado si se está generando."""
    out = dict(trabajo=_estado.get(eid))
    f = os.path.join(DIR, eid + ".json")
    if os.path.exists(f) and os.path.exists(os.path.join(DIR, eid + ".mp4")):
        try:
            with open(f, encoding="utf-8") as fh:
                out.update(json.load(fh))
            out["ver"] = int(os.path.getmtime(os.path.join(DIR, eid + ".mp4")))
        except Exception:
            pass
    return out


def _recortar(origen, eid, meta, desde=0):
    os.makedirs(DIR, exist_ok=True)
    tmp = os.path.join(DIR, eid + ".tmp.mp4")
    r = subprocess.run([T.FFMPEG, "-y", "-loglevel", "error", "-ss", str(desde), "-i", origen, "-t", str(SEG),
                        "-vf", "scale='if(gt(iw,ih),-2,720)':'if(gt(iw,ih),720,-2)'", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp],
                       capture_output=True, text=True, creationflags=_NO_VENTANA)
    if r.returncode != 0 or not os.path.exists(tmp):
        raise RuntimeError("ffmpeg no pudo recortar: " + (r.stderr or "")[-300:])
    os.replace(tmp, os.path.join(DIR, eid + ".mp4"))
    with open(os.path.join(DIR, eid + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)


def buscar_existente(eid):
    """Primer video terminado con ese estilo (Estudio y luego Fábrica) -> (ruta, meta) o None."""
    for f in sorted(glob.glob(os.path.join(P.PROYECTOS, "*", "proyecto.json")), key=os.path.getmtime, reverse=True):
        carpeta = os.path.dirname(f)
        if os.path.basename(carpeta).startswith("_"):
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                p = json.load(fh)
        except Exception:
            continue
        m = glob.glob(os.path.join(carpeta, "salida", "*_MASTER.mp4"))
        if p.get("estilo") == eid and m and T.leer_estado(carpeta).get("estado") == "listo":
            return m[0], dict(origen="video", titulo=p.get("titulo"), formato=p.get("formato", "horizontal"))
    if eid in P.ESTILOS_BASE:
        for g in sorted(glob.glob(os.path.join(RAIZ, "videos", "*", "guion.py"))):
            try:
                src = open(g, encoding="utf-8").read()
            except Exception:
                continue
            e = re.search(r"^ESTILO_VISUAL\s*=\s*[\"'](\w+)", src, re.M)
            m = [x for x in glob.glob(os.path.join(os.path.dirname(g), "salida", "*_MASTER.mp4")) if os.path.exists(x)]
            if e and e.group(1) == eid and m:
                t = re.search(r"^TITULO\s*=\s*[\"'](.+?)[\"']", src, re.M)
                fmt = re.search(r"^FORMATO\s*=\s*[\"'](\w+)", src, re.M)
                return m[0], dict(origen="fabrica", titulo=t.group(1) if t else os.path.basename(os.path.dirname(g)),
                                  formato=fmt.group(1) if fmt else "horizontal")
    return None


def completar_desde_videos(eids):
    """Al arrancar y tras cada video terminado: crea las vistas que se puedan sacar de videos existentes."""
    for eid in eids:
        if os.path.exists(os.path.join(DIR, eid + ".mp4")):
            continue
        hallado = buscar_existente(eid)
        if hallado:
            try:
                _recortar(hallado[0], eid, hallado[1])
            except Exception as ex:
                print(f"vista {eid}: {ex}", flush=True)


def generar(eid, escribir_proyecto, procs=8):
    """escribir_proyecto(carpeta) escribe guion.py/escenas.py de la muestra con ese estilo."""
    if (_estado.get(eid) or {}).get("estado") in ("cola", "generando"):
        return
    _estado[eid] = dict(estado="cola", pct=0, mensaje="Esperando turno…")
    threading.Thread(target=_generar, args=(eid, escribir_proyecto, procs), daemon=True).start()


def _generar(eid, escribir_proyecto, procs):
    carpeta = os.path.join(P.PROYECTOS, "_vista_" + eid)
    clave = "vista:" + eid
    vigila = {"on": True}
    try:
        with T.COLA:
            _estado[eid] = dict(estado="generando", pct=2, mensaje="Preparando la muestra")
            shutil.rmtree(carpeta, ignore_errors=True)
            escribir_proyecto(carpeta)
            log = os.path.join(carpeta, "registro.txt")
            open(log, "w").close()
            py = sys.executable
            T._correr(clave, [py, "-c", "import json, muestra_estilo; json.dump(muestra_estilo.timeline_provisional(), "
                                        "open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False)"],
                      carpeta, log, descripcion="tiempos de la muestra")
            with open(os.path.join(carpeta, "timeline.json"), encoding="utf-8") as f:
                n_seg = math.ceil(json.load(f)["total"] * 30 / 90)

            def vigia():
                while vigila["on"]:
                    hechos = len(glob.glob(os.path.join(carpeta, "segmentos", "seg_*.mp4")))
                    if _estado[eid].get("paso") == "video":
                        _estado[eid].update(pct=round(10 + 75 * hechos / max(1, n_seg)))
                    time.sleep(1.5)
            threading.Thread(target=vigia, daemon=True).start()
            _estado[eid].update(paso="video", mensaje="Dibujando 20 segundos de animación", pct=10)
            T._correr(clave, [py] + T.MODULOS["video"] + ["--procs", str(procs)], carpeta, log, descripcion="dibujar muestra")
            _estado[eid].update(paso="musica", mensaje="Componiendo la música", pct=86)
            T._correr(clave, [py] + T.MODULOS["musica"], carpeta, log, descripcion="música")
            _estado[eid].update(paso="sfx", mensaje="Efectos de sonido", pct=92)
            T._correr(clave, [py] + T.MODULOS["sfx"], carpeta, log, descripcion="efectos")
            _estado[eid].update(paso="final", mensaje="Últimos toques", pct=96)
            os.makedirs(DIR, exist_ok=True)
            tmp = os.path.join(DIR, eid + ".tmp.mp4")
            r = subprocess.run([T.FFMPEG, "-y", "-loglevel", "error", "-i", os.path.join(carpeta, "salida", "video_sin_audio.mp4"),
                                "-i", os.path.join(carpeta, "audio", "musica.wav"), "-i", os.path.join(carpeta, "audio", "sfx.wav"),
                                "-filter_complex", "[1:a]volume=0.8[m];[2:a]volume=0.6[s];[m][s]amix=inputs=2:normalize=0,"
                                "loudnorm=I=-16:TP=-1.5[a]", "-map", "0:v", "-map", "[a]", "-t", str(SEG),
                                "-vf", "scale=-2:720", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp],
                               capture_output=True, text=True, creationflags=_NO_VENTANA)
            if r.returncode != 0 or not os.path.exists(tmp):
                raise RuntimeError("no se pudo armar el video: " + (r.stderr or "")[-300:])
            os.replace(tmp, os.path.join(DIR, eid + ".mp4"))
            with open(os.path.join(DIR, eid + ".json"), "w", encoding="utf-8") as f:
                json.dump(dict(origen="muestra", titulo="Muestra de 20 s (sin narración)", formato="horizontal"), f,
                          ensure_ascii=False)
            _estado.pop(eid, None)
    except T.Cancelado:
        _estado[eid] = dict(estado="error", error="Cancelado")
    except Exception as ex:
        _estado[eid] = dict(estado="error", error=str(ex).split("\n")[0][:300])
    finally:
        vigila["on"] = False
        shutil.rmtree(carpeta, ignore_errors=True)


def borrar(eid):
    for ext in (".mp4", ".json"):
        try:
            os.remove(os.path.join(DIR, eid + ext))
        except OSError:
            pass


# ------------------------------------------------------------------ estilos PREMIUM (motor propio; vitrina con un video real)
# Se producen a medida en la Fábrica (motores propios: mapas ETOPO, isométrico, fotos con paralaje, boceto trazo a trazo);
# el Estudio automático no los imita bien, así que se muestran con un tramo de 20 s de un video ya armado y no se eligen.
CANALES = [
    dict(id="pro_kz_iso", nombre="Kurzgesagt isométrico", canal="Bitácora Perdida", video="independencia_mx", desde=150,
         descripcion="Dioramas isométricos, multitudes animadas y retratos reales en marco dorado."),
    dict(id="pro_mapas", nombre="Mapas con relieve real", canal="Bitácora Perdida", video="independencia_mx", desde=345, portada_t=350,
         descripcion="Mapas con relieve, ríos y ciudades reales; ejércitos y rutas animados."),
    dict(id="pro_kz_plano", nombre="Kurzgesagt ilustrado", canal="Bitácora Perdida", video="teotihuacan", desde=100,
         descripcion="Ilustración plana con profundidad, luces y personajes."),
    dict(id="pro_kz_vertical", nombre="Kurzgesagt vertical (Shorts)", canal="Kuriox", video="historia_60", desde=0,
         descripcion="Formato vertical rápido, una época por golpe de música."),
    dict(id="pro_mapa_guache", nombre="Mapa pintado (boceto y guache)", canal="Cronopapel", video="historia_espana", desde=40,
         descripcion="Mapa pintado a mano con relieve real, reinos que cambian y pegatinas."),
    dict(id="pro_documental", nombre="Documental de misterio", canal="Edsonxn", video="voynich", desde=8, portada_t=24,
         descripcion="Fotos y documentos con paralaje, polaroids, texto serif y atmósfera oscura."),
    dict(id="pro_crimen", nombre="Crimen real / noticia", canal="Edsonxn", video="christa_pike", desde=36, portada_t=49,
         descripcion="Motion graphics dibujados, mapas, fechas y fotos de archivo."),
    dict(id="pro_guache", nombre="Libro ilustrado (guache)", canal="Experimentos", video="pelea_meme", desde=5,
         descripcion="Ilustración de libro infantil en gouache, paleta cálida y textura de papel."),
]


def completar_canales(dir_portadas):
    """Recorta (una vez) el tramo de 20 s y saca la portada de cada estilo Premium."""
    for c in CANALES:
        m = glob.glob(os.path.join(RAIZ, "videos", c["video"], "salida", "*_MASTER.mp4"))
        if not m:
            continue
        if not os.path.exists(os.path.join(DIR, c["id"] + ".mp4")):
            src = open(os.path.join(RAIZ, "videos", c["video"], "guion.py"), encoding="utf-8").read()
            t = re.search(r"^TITULO\s*=\s*[\"'](.+?)[\"']", src, re.M)
            fmt = re.search(r"^FORMATO\s*=\s*[\"'](\w+)", src, re.M)
            try:
                _recortar(m[0], c["id"], dict(origen="canal", titulo=t.group(1) if t else c["video"], canal=c["canal"],
                                              formato=fmt.group(1) if fmt else "horizontal"), desde=c["desde"])
            except Exception as ex:
                print(f"vista {c['id']}: {ex}", flush=True)
        portada = os.path.join(dir_portadas, c["id"] + ".jpg")
        if not os.path.exists(portada) or os.path.getsize(portada) < 2000:      # falta o quedó rota (disco lleno)
            os.makedirs(dir_portadas, exist_ok=True)
            subprocess.run([T.FFMPEG, "-y", "-loglevel", "error", "-ss", str(c.get("portada_t", c["desde"] + 8)), "-i", m[0], "-frames:v", "1",
                            "-vf", "scale=640:-2", "-q:v", "3", portada], capture_output=True, creationflags=_NO_VENTANA)
