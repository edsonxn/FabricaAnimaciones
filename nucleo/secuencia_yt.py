# -*- coding: utf-8 -*-
"""Motor SECUENCIA YT: el video = un clip de gameplay de YouTube (yt-dlp) por «beat» de la narración.
Es la fuente de medios del motor SECUENCIA (nucleo/secuencia.py) para Crónicas de Warcraft (y luego Tamriel / Runa
Caída): `beats` y `video` son los de siempre; aquí solo se buscan, bajan y cortan los clips a medios/scene-NNN.mp4.

  python fab.py <v> beats              timeline.json -> beats.json (cortes en pausas reales, ~clip_s por beat)
  python fab.py <v> busquedas          crea/valida busquedas.json (Claude escribe UNA búsqueda por beat, en inglés)
  python fab.py <v> bajar [ids] [--rehacer] [--q "texto"] [--url URL --desde S] [-j 4]
                                        busca, elige tramo, baja y corta; registra la fuente en fuentes.json
  python fab.py <v> fuentes            lista beat -> video/canal/segundo y escribe salida/creditos.txt
  python fab.py <v> medios             hojas previews/medios_NN.jpg (MÍRALAS y rehaz los clips malos)
  python fab.py <v> video              arma el video (transición `slideleft` si SECUENCIA lo pide)

busquedas.json: {"scene-001": "Thrall Orgrimmar", "scene-002": ["Kith'ix raid", "WoW raid boss 12.1.5"],
                 "scene-003": {"url": "https://youtu.be/…", "desde": 312.5}}
  - texto o lista de textos (respaldos en orden); 2-4 palabras, nombre propio en INGLÉS primero (YouTube devuelve
    CERO con varios nombres propios juntos; ver docs/estilo_secuencia_yt.md). El sufijo del juego se añade solo.
  - {"url", "desde"} fija un video y su segundo exacto (para lo que hay que enseñar sí o sí).

guion.py:  MOTOR = "secuencia"   SECUENCIA = dict(fuente="yt", video_s=99999, clip_s=8.6, transicion="slideleft",
           fundido=0.35, ambiente=0.0, yt=dict(sufijo="World of Warcraft", min_s=90, max_min=240, alto=1080))
"""
import concurrent.futures as cf
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading

import secuencia as S

DEF_YT = dict(sufijo="", min_s=90, max_min=240, alto=1080, candidatos=12, margen=0.12, evitar_canales=[],
              evitar_palabras=["reaction", "react", "podcast", "tier list", "news", "shorts", "#shorts", "trailer reaction"],
              separacion=6, oscuro=0.07, quieto=0.012)
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
_lock = threading.Lock()


def cfg_yt():
    c = S.cfg()
    y = dict(DEF_YT)
    y.update(c.get("yt", {}))
    return c, y


def _cookies():
    if os.environ.get("YT_DLP_COOKIES_FILE"):
        return ["--cookies", os.environ["YT_DLP_COOKIES_FILE"]]
    if os.environ.get("YT_DLP_COOKIES_BROWSER"):
        return ["--cookies-from-browser", os.environ["YT_DLP_COOKIES_BROWSER"]]
    return []


def cargar_fuentes():
    if os.path.exists("fuentes.json"):
        return json.load(open("fuentes.json", encoding="utf-8"))
    return {"_busquedas": {}}


def guardar_fuentes(fu):
    with _lock:
        tmp = "fuentes.json.tmp"
        json.dump(fu, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, "fuentes.json")


# ------------------------------------------------------------------ busquedas.json
def _consultas(v):
    if isinstance(v, str):
        return [v] if v.strip() else []
    if isinstance(v, list):
        return [x for x in v if str(x).strip()]
    if isinstance(v, dict):
        return [x for x in ([v["q"]] if isinstance(v.get("q"), str) else v.get("q", [])) if str(x).strip()]
    return []


def busquedas():
    bs = S.cargar_beats()
    if not os.path.exists("busquedas.json"):
        json.dump({b["id"]: "" for b in bs}, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for b in bs:
            print(f"{b['id']} {b['t0']:7.1f}s  {b['texto'][:110]}")
        raise SystemExit(f"\nCreé busquedas.json vacío con {len(bs)} entradas: una búsqueda (o lista, o {{url, desde}}) por beat.")
    bq = json.load(open("busquedas.json", encoding="utf-8"))
    ids = [b["id"] for b in bs]
    faltan = [i for i in ids if not (_consultas(bq.get(i)) or (isinstance(bq.get(i), dict) and bq[i].get("url")))]
    sobran = [i for i in bq if i not in ids]
    if faltan or sobran:
        raise SystemExit(f"busquedas.json no cuadra con beats.json · vacías: {faltan[:15]}{'…' if len(faltan) > 15 else ''} · sobran: {sobran[:15]}")
    avisos = []
    for i in ids:
        for q in _consultas(bq[i]):
            n = len(q.split())
            if n > 5:
                avisos.append(f"{i}: «{q}» tiene {n} palabras (YouTube devuelve poco o nada con búsquedas largas)")
            if re.search(r"[áéíóúñ¿¡]", q.lower()):
                avisos.append(f"{i}: «{q}» parece español; el gameplay se busca mejor en inglés")
    seguidas = [ids[k] for k in range(1, len(ids)) if _consultas(bq[ids[k]])[:1] == _consultas(bq[ids[k - 1]])[:1] != []]
    print(f"busquedas.json OK: {len(ids)} beats")
    if seguidas:
        print(f"  aviso: misma búsqueda que el beat anterior en {', '.join(seguidas[:10])} (se tomará otro tramo, pero varía)")
    for a in avisos[:30]:
        print("  aviso:", a)


# ------------------------------------------------------------------ búsqueda y elección
def _buscar(q, y, fu):
    clave = f"{q}|{y['candidatos']}"
    if clave in fu["_busquedas"]:
        return fu["_busquedas"][clave]
    r = subprocess.run(["yt-dlp", f"ytsearch{y['candidatos']}:{q}", "--flat-playlist", "--dump-json", "--no-warnings"] + _cookies(),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=60)
    out = []
    for ln in r.stdout.splitlines():
        try:
            j = json.loads(ln)
        except ValueError:
            continue
        out.append(dict(id=j.get("id"), titulo=j.get("title") or "", canal=j.get("channel") or j.get("uploader") or "",
                        dur=float(j.get("duration") or 0)))
    with _lock:
        fu["_busquedas"][clave] = out
    return out


def _apto(v, y):
    t = (v["titulo"] + " " + v["canal"]).lower()
    if not v["id"] or v["dur"] < y["min_s"] or v["dur"] > y["max_min"] * 60:
        return False
    if any(p.lower() in t for p in y["evitar_palabras"]):
        return False
    return not any(c.lower() == v["canal"].lower() for c in y["evitar_canales"])


def _tramo(v, beat_id, L, y, usados):
    """Segundo de inicio dentro del video, lejos de intros/outros y de tramos ya usados de ese mismo video."""
    a = max(15.0, v["dur"] * y["margen"])
    b = v["dur"] * (1 - y["margen"]) - L
    if b <= a:
        return None
    rnd = random.Random(int(hashlib.md5((beat_id + v["id"]).encode()).hexdigest()[:8], 16))
    previos = [u for u in usados if u[0] == v["id"]]
    for _ in range(25):
        t = rnd.uniform(a, b)
        if all(abs(t - p[1]) > L + 20 for p in previos):
            return round(t, 1)
    return None


def _bajar_tramo(vid, desde, L, y, destino, tmpdir):
    """Baja [desde, desde+L+1] solo video y lo deja en `destino` a W×H, 30 fps, h264, sin audio."""
    os.makedirs(tmpdir, exist_ok=True)
    for f in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, f))
    url = f"https://www.youtube.com/watch?v={vid}"
    fmt = f"bv*[height<={y['alto']}][height>=720][vcodec^=avc1]/bv*[height<={y['alto']}][height>=720]"
    r = subprocess.run(["yt-dlp", url, "-f", fmt, "--download-sections", f"*{desde:.1f}-{desde + L + 1.5:.1f}",
                        "-o", os.path.join(tmpdir, "c.%(ext)s"), "--no-warnings", "--no-playlist", "--quiet"] + _cookies(),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=300)
    bajado = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if not f.endswith(".part")]
    if r.returncode != 0 or not bajado:
        err = " ".join(l for l in (r.stderr or "").splitlines() if "ERROR" in l)[:200]
        return f"yt-dlp: {err or r.returncode}"
    W, H = S.W, S.H
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={S.FPS}"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.4", "-i", bajado[0], "-t", f"{L:.3f}", "-an",
                        "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", destino],
                       capture_output=True, text=True)
    return None if r.returncode == 0 and os.path.exists(destino) else f"ffmpeg: {r.stderr[-200:]}"


def _juzgar(ruta, y):
    """Rechaza lo que se ve mal sin mirarlo: negro/oscuro casi entero o casi quieto (menús, pantallas de carga)."""
    import cv2
    import numpy as np
    cap = cv2.VideoCapture(ruta)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fr = []
    for k in range(6):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (0.08 + 0.16 * k)))
        ok, f = cap.read()
        if ok:
            fr.append(cv2.resize(f, (160, 90)).astype(np.float32) / 255)
    cap.release()
    if len(fr) < 3:
        return "ilegible"
    luz = float(np.mean([f.mean() for f in fr]))
    mov = float(np.mean([np.abs(fr[i] - fr[i - 1]).mean() for i in range(1, len(fr))]))
    if luz < y["oscuro"]:
        return f"oscuro ({luz:.2f})"
    if mov < y["quieto"]:
        return f"quieto ({mov:.3f})"
    if y.get("caras", True) and _webcam(ruta):
        return "cámara del streamer (cara fija en una esquina)"
    return None


_haar = None


def _webcam(ruta):
    """¿Hay una webcam de streamer? Cara (Haar) que se queda QUIETA en el mismo sitio en ≥ 3 de 4 cuadros y fuera del
    centro, mientras el juego se mueve. Una «cara» del escenario se desplaza con la cámara del juego (probado 13-oct)."""
    import cv2
    global _haar
    with _lock:
        if _haar is None:
            _haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(ruta)
    n, cajas = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), []
    for k in range(4):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (0.1 + 0.25 * k)))
        ok, f = cap.read()
        if not ok:
            continue
        g = cv2.cvtColor(cv2.resize(f, (960, 540)), cv2.COLOR_BGR2GRAY)
        with _lock:
            cajas.append([(x + w / 2, y + h / 2) for x, y, w, h in _haar.detectMultiScale(g, 1.1, 7, minSize=(36, 36))])
    cap.release()
    for cx, cy in (c for fr in cajas for c in fr):
        if 960 * 0.3 < cx < 960 * 0.7 and 540 * 0.25 < cy < 540 * 0.75:
            continue                                   # centro del plano: personaje del juego, no webcam
        igual = sum(any(abs(cx - x) < 12 and abs(cy - y) < 12 for x, y in fr) for fr in cajas)
        if igual >= 3:
            return True
    return False


def _uno(b, entrada, y, fu, usados_global, forzar_q=None, forzar_url=None, forzar_desde=None):
    L = round(b["t1"] - b["t0"] + 0.3, 3)
    destino = os.path.join("medios", b["id"] + ".mp4")
    tmpdir = os.path.join("medios", "_tmp_" + b["id"])
    try:
        url = forzar_url or (entrada.get("url") if isinstance(entrada, dict) else None)
        if url:
            vid = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url).group(1)
            desde = float(forzar_desde if forzar_desde is not None else (entrada.get("desde", 30) if isinstance(entrada, dict) else 30))
            err = _bajar_tramo(vid, desde, L, y, destino, tmpdir)
            if err:
                return b["id"], f"FALLÓ fijo {vid}@{desde}: {err}"
            reg = dict(video=vid, desde=desde, titulo="(fijado a mano)", canal="", q="")
        else:
            qs = [forzar_q] if forzar_q else _consultas(entrada)
            sufijo = y["sufijo"]
            reg, motivos = None, []
            for q in qs:
                qq = q if (not sufijo or sufijo.lower() in q.lower() or "wow" in q.lower().split()) else f"{q} {sufijo}"
                cands = [v for v in _buscar(qq, y, fu) if _apto(v, y)]
                with _lock:          # los videos usados en beats cercanos van al final: variedad
                    cerca = {u[0] for u in usados_global if abs(u[2] - b["t0"]) < y["separacion"] * 9}
                cands.sort(key=lambda v: v["id"] in cerca)
                for v in cands[:10]:
                    with _lock:
                        desde = _tramo(v, b["id"], L, y, usados_global)
                    if desde is None:
                        continue
                    err = _bajar_tramo(v["id"], desde, L, y, destino, tmpdir)
                    if err:
                        motivos.append(err[:60])
                        continue
                    malo = _juzgar(destino, y)
                    if malo:
                        motivos.append(f"{v['id']} {malo}")
                        os.remove(destino)
                        continue
                    reg = dict(video=v["id"], desde=desde, titulo=v["titulo"], canal=v["canal"], q=qq)
                    break
                if reg:
                    break
            if not reg:
                return b["id"], f"FALLÓ ({len(motivos)} probados): {'; '.join(motivos[-4:]) or 'sin resultados aptos'}"
        with _lock:
            usados_global.append((reg["video"], reg["desde"], b["t0"]))
            fu[b["id"]] = reg
        guardar_fuentes(fu)
        return b["id"], f"ok  {reg['video']}@{reg['desde']:.0f}s  {reg['canal'][:22]} · {reg['titulo'][:60]}"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def bajar(args):
    c, y = cfg_yt()
    bs = S.cargar_beats()
    if not os.path.exists("busquedas.json"):
        raise SystemExit("Falta busquedas.json: corre `python fab.py <v> busquedas` y escríbelas.")
    bq = json.load(open("busquedas.json", encoding="utf-8"))
    S.dir_medios()
    fu = cargar_fuentes()
    rehacer = "--rehacer" in args
    def opt(n):
        return args[args.index(n) + 1] if n in args else None
    q, url, desde, j = opt("--q"), opt("--url"), opt("--desde"), int(opt("-j") or 4)
    pedidos = set()
    for k, a in enumerate(args):
        if a.startswith("-") or (k > 0 and args[k - 1] in ("--q", "--url", "--desde", "-j")):
            continue
        for p in a.split(","):          # 12  ·  12-18  ·  scene-012
            m = re.fullmatch(r"(?:scene-)?(\d+)(?:-(\d+))?", p)
            if m:
                pedidos.update(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1))
    sel = [b for b in bs if (not pedidos or int(b["id"][6:]) in pedidos)]
    if rehacer or q or url:
        for b in sel:
            r = os.path.join("medios", b["id"] + ".mp4")
            if os.path.exists(r):
                os.remove(r)
            fu.pop(b["id"], None)
    sel = [b for b in sel if not S.medio_de(b)]
    usados = [(r["video"], r["desde"], next((b["t0"] for b in bs if b["id"] == k), 0)) for k, r in fu.items() if k != "_busquedas"]
    print(f"bajar: {len(sel)} clips ({j} a la vez) · {S.W}x{S.H} {S.FPS} fps · sufijo «{y['sufijo']}»", flush=True)
    fallos = []
    with cf.ThreadPoolExecutor(max_workers=j) as ex:
        futs = [ex.submit(_uno, b, bq.get(b["id"], ""), y, fu, usados, q, url, desde) for b in sel]
        for f in cf.as_completed(futs):
            i, msg = f.result()
            print(f"  {i} {msg}", flush=True)
            if msg.startswith("FALLÓ"):
                fallos.append(i)
    guardar_fuentes(fu)
    hechos = sum(1 for b in bs if S.medio_de(b))
    print(f"{hechos}/{len(bs)} clips en medios/" + (f" · fallaron: {' '.join(sorted(fallos))} (cambia su búsqueda y repite)" if fallos else ""))
    print("Siguiente: `python fab.py <v> medios` y MIRA las hojas (caras de streamer, menús, otro juego, texto encima → --rehacer).")


def fuentes():
    bs = S.cargar_beats()
    fu = cargar_fuentes()
    vistos, lineas = {}, []
    for b in bs:
        r = fu.get(b["id"])
        if not r:
            print(f"{b['id']}  —")
            continue
        print(f"{b['id']} {b['t0']:7.1f}s  {r['video']}@{r['desde']:6.0f}s  {r['canal'][:20]:20} {r['titulo'][:60]}")
        vistos.setdefault(r["video"], r)
    os.makedirs("salida", exist_ok=True)
    for vid, r in vistos.items():
        lineas.append(f"{r['titulo']} — {r['canal']}: https://youtu.be/{vid}" if r["canal"] else f"https://youtu.be/{vid}")
    open("salida/creditos.txt", "w", encoding="utf-8").write("Gameplay usado (créditos):\n" + "\n".join(lineas) + "\n")
    print(f"\n{len(vistos)} videos distintos · salida/creditos.txt (pégalo en la descripción)")


if __name__ == "__main__":
    orden, resto = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if orden == "busquedas":
        busquedas()
    elif orden == "bajar":
        bajar(resto)
    elif orden == "fuentes":
        fuentes()
    else:
        raise SystemExit(__doc__)
