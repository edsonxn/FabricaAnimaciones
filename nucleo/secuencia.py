# -*- coding: utf-8 -*-
"""Motor SECUENCIA: video = clips e imágenes generados en Google Flow, uno por «beat» de la narración.
Departamento aparte de la Fábrica (heredado del proyecto Platitube): la voz, la música y la mezcla son las
etapas de siempre; aquí solo se decide QUÉ medio va en cada instante y se arma el video.

  python fab.py <v> beats            timeline.json -> beats.json (cortes en pausas reales de la voz)
  python fab.py <v> prompts          valida prompts.json contra beats.json -> flow/prompts.txt + flow/escenas.json
  python fab.py <v> servir [min]     sirve flow/escenas.json a la página de Flow (para lanzar el lote sin pegar prompts)
  python fab.py <v> ingesta [carpeta] [--espera 0]   copia scene-XXX.* de Descargas/<carpeta> a medios/ hasta completar
  python fab.py <v> medios           hojas de revisión previews/medios_NN.jpg (20 por hoja, con su frase)
  python fab.py <v> video [--borrador] [--tramo 0-60]   arma salida/video_sin_audio.mp4 (y audio/ambiente.wav)
  python fab.py <v> ambiente         solo audio/ambiente.wav: el sonido propio de los clips de Flow, que `mezcla` suma bajo la voz

guion.py:  MOTOR = "secuencia"  y opcionalmente
  SECUENCIA = dict(video_s=120, clip_s=8, img_s=4.0, rapido_hasta=300, img_s_lento=6.0, fundido=0.2,
                   combinar=False, carpeta_descargas="flow-<video>",
                   ambiente=0.5, ambiente_por={"scene-004": 0.0},     # volumen del audio de los clips (0 = mudo), general y por clip
                   recorte_clip=0.0, recorte_por={"scene-003": 0.05})  # recorte por lado de los clips (quita marcos de viñeta)
  clips_s=[10]*7 + [8]   # opcional: duración de CADA clip en orden (mezcla 10 s y 8 s para gastar todos los puntos);
                         # sustituye a video_s/clip_s y cada beat de video lleva su `clip_s`
Detalle del estilo y del flujo: docs/estilo_secuencia_flow.md
"""
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time

DEF = dict(video_s=120.0, clip_s=8.0, img_s=4.0, rapido_hasta=300.0, img_s_lento=6.0, fundido=0.2,
           combinar=False, carpeta_descargas=None, ambiente=0.5, ambiente_por={},
           video_calidad="360p")       # 360p cuesta menos puntos; se baja con «720p · Resolución mejorada» (gratis)
SIN_DIALOGO = "Sin diálogo, sin conversación entre personajes, sin voces audibles."
EXT_VIDEO = (".mp4", ".webm", ".mov")
EXT_IMG = (".jpg", ".jpeg", ".png", ".webp")
FPS = int(os.environ.get("FAB_FPS", "30"))
try:                    # formato del video: guion.py -> FORMATO = "vertical" (1080x1920, reels) o "horizontal" (1920x1080)
    import guion as _g
    VERTICAL = getattr(_g, "FORMATO", "horizontal") == "vertical"
except Exception:
    VERTICAL = False
W, H = (1080, 1920) if VERTICAL else (1920, 1080)
ASPECTO = "9:16" if VERTICAL else "16:9"         # el mismo que hay que pedirle a Flow (setConfig aspectRatio)


def cfg():
    import guion as g
    c = dict(DEF)
    c.update(getattr(g, "SECUENCIA", {}))
    if c.get("clips_s"):                    # lista de duraciones por clip: manda sobre video_s
        c["video_s"] = float(sum(c["clips_s"]))
        c["clip_s"] = max(c["clips_s"], key=c["clips_s"].count)
    if not c["carpeta_descargas"]:
        c["carpeta_descargas"] = "flow-" + os.path.basename(os.getcwd())
    return c


def cargar_beats():
    if not os.path.exists("beats.json"):
        raise SystemExit("Falta beats.json: corre antes `python fab.py <video> beats`")
    return json.load(open("beats.json", encoding="utf-8"))


# ------------------------------------------------------------------ beats
def _palabras(tl):
    out = []
    for e in tl["escenas"]:
        for fr in e["frases"]:
            for k, w in enumerate(fr["words"]):
                out.append(dict(w=w["w"], s=w["s"], e=w["e"], ini_frase=(k == 0)))
    return out


def _cortes(pal, a, b, paso):
    """Cortes dentro de [a, b] cada ~paso s, puestos en la pausa real más cercana (inicio de frase o tras puntuación)."""
    n = max(1, int(round((b - a) / paso)))
    cand = []
    for i in range(1, len(pal)):
        p, q = pal[i - 1], pal[i]
        if not (a < q["s"] < b):
            continue
        hueco = max(0.0, q["s"] - p["e"])
        bono = 0.0
        if q["ini_frase"]:
            bono = 0.45
        elif p["w"][-1:] in ".?!;:":
            bono = 0.35
        elif p["w"][-1:] == ",":
            bono = 0.22
        bono += min(0.2, hueco * 0.5)
        cand.append((q["s"] - min(hueco / 2, 0.12), bono))
    cortes, previo = [], a
    for k in range(1, n):
        obj = a + (b - a) * k / n
        mejor = None
        for tc, bono in cand:
            if tc <= previo + paso * 0.5 or tc >= b - paso * 0.5 or abs(tc - obj) > paso * 0.4:
                continue
            costo = abs(tc - obj) / paso - bono * 0.6
            if mejor is None or costo < mejor[0]:
                mejor = (costo, tc)
        if mejor is None:                             # sin pausa cerca: corta en el inicio de palabra más próximo
            libres = [tc for tc, _ in cand if previo + paso * 0.4 < tc < b - paso * 0.4]
            if not libres:
                continue
            mejor = (0, min(libres, key=lambda x: abs(x - obj)))
        cortes.append(round(mejor[1], 3))
        previo = mejor[1]
    return cortes


def _frontera(pal, t, total):
    """Mueve una frontera de zona al inicio de frase más cercano (para no partir una frase entre video e imagen)."""
    if t <= 0 or t >= total:
        return max(0.0, min(t, total))
    ini = [p["s"] for p in pal if p["ini_frase"]]
    return min(ini, key=lambda x: abs(x - t)) - 0.08 if ini else t


def _pausa(pal, t):
    """Inicio de palabra más cercano a t que venga tras una pausa real (inicio de frase o tras puntuación)."""
    cand = [q["s"] - 0.08 for p, q in zip(pal, pal[1:]) if q["ini_frase"] or p["w"][-1:] in ".,?!;:"]
    return min(cand, key=lambda x: abs(x - t)) if cand else t


def beats():
    c = cfg()
    tl = json.load(open("timeline.json", encoding="utf-8"))
    pal, total = _palabras(tl), tl["total"]
    f_video = _frontera(pal, min(c["video_s"], total), total) if c["video_s"] > 0 else 0.0
    f_rapido = _frontera(pal, min(c["rapido_hasta"], total), total)
    f_rapido = max(f_rapido, f_video)
    zonas = [(f_video, f_rapido, c["img_s"], "imagen"), (f_rapido, total, c["img_s_lento"], "imagen")]
    if f_video > 0 and c.get("clips_s"):     # duraciones mezcladas: un tramo por grupo de clips iguales seguidos
        grupos, a = [], 0.0
        for dur in c["clips_s"]:
            if grupos and grupos[-1][0] == dur:
                grupos[-1][1] += 1
            else:
                grupos.append([dur, 1])
        acum = 0.0
        for i, (dur, n) in enumerate(grupos):
            acum += dur * n
            b = f_video if i == len(grupos) - 1 else _pausa(pal, f_video * acum / c["video_s"])
            zonas.insert(i, (a, b, float(dur), "video"))
            a = b
    elif f_video > 0:
        zonas.insert(0, (0.0, f_video, c["clip_s"], "video"))
    lim = []
    for a, b, paso, tipo in zonas:
        if b - a < 0.5:
            continue
        ts = [a] + _cortes(pal, a, b, paso) + [b]
        lim += [(ts[i], ts[i + 1], tipo, paso) for i in range(len(ts) - 1)]
    out = []
    for k, (a, b, tipo, paso) in enumerate(lim):
        texto = " ".join(p["w"] for p in pal if a - 0.13 <= p["s"] < b - 0.13)
        d = dict(id=f"scene-{k + 1:03d}", t0=round(a, 3), t1=round(b, 3), tipo=tipo, texto=texto)
        if tipo == "video":
            d["clip_s"] = int(paso)
        if tipo == "video" and c["combinar"]:        # dos escenas en un clip: se parte en la pausa más cercana a la mitad
            medio = (_cortes(pal, a, b, (b - a) / 2) or [(a + b) / 2])[0]
            d.update(t_medio=round(medio, 3),
                     texto_a=" ".join(p["w"] for p in pal if a - 0.13 <= p["s"] < medio - 0.13),
                     texto_b=" ".join(p["w"] for p in pal if medio - 0.13 <= p["s"] < b - 0.13))
        out.append(d)
    out[0]["t0"], out[-1]["t1"] = 0.0, total
    json.dump(out, open("beats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nv = sum(1 for x in out if x["tipo"] == "video")
    ds = [x["t1"] - x["t0"] for x in out]
    print(f"beats.json: {len(out)} beats = {nv} de video + {len(out) - nv} de imagen · total {total:.1f}s")
    for nombre, sel in (("video", [x for x in out if x["tipo"] == "video"]), ("imagen", [x for x in out if x["tipo"] == "imagen"])):
        if sel:
            d = [x["t1"] - x["t0"] for x in sel]
            print(f"  {nombre}: {len(sel)}  dur media {sum(d) / len(d):.1f}s  (mín {min(d):.1f}, máx {max(d):.1f})")
    for x in out:
        if "texto_a" in x:
            print(f"{x['id']} {x['t0']:7.2f}-{x['t1']:7.2f} V A: {x['texto_a'][:90]}")
            print(f"{'':10}{x['t_medio']:7.2f}{'':10} B: {x['texto_b'][:90]}")
            continue
        print(f"{x['id']} {x['t0']:7.2f}-{x['t1']:7.2f} {'V' if x['tipo'] == 'video' else ' '} {x['texto'][:110]}")
    if os.path.exists("prompts.json"):
        print("\nOJO: ya existía prompts.json; si cambió el número o el contenido de los beats, revísalo (`fab.py <v> prompts`).")
    return min(ds)


# ------------------------------------------------------------------ prompts
def prompts():
    c = cfg()
    bs = cargar_beats()
    if not os.path.exists("prompts.json"):
        json.dump({b["id"]: "" for b in bs}, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        raise SystemExit(f"Creé prompts.json vacío con {len(bs)} entradas: escribe un prompt por beat y vuelve a correr.")
    pr = json.load(open("prompts.json", encoding="utf-8"))
    ids = [b["id"] for b in bs]
    faltan = [i for i in ids if not str(pr.get(i, "")).strip()]
    sobran = [i for i in pr if i not in ids]
    if faltan or sobran:
        raise SystemExit(f"prompts.json no cuadra con beats.json · sin prompt: {faltan[:12]}{'…' if len(faltan) > 12 else ''} · sobran: {sobran[:12]}")
    avisos, esc, lineas = [], [], []
    for b in bs:
        p = " ".join(str(pr[b["id"]]).split())
        if b["tipo"] == "video" and "sin diálogo" not in p.lower():
            p = p.rstrip() + " " + SIN_DIALOGO
        if len(p) < 120:
            avisos.append(f"{b['id']}: prompt muy corto ({len(p)} car.), ¿lleva estilo, personaje y escenario?")
        e = dict(sceneId=b["id"], prompt=p, mediaType="video" if b["tipo"] == "video" else "image")
        if b["tipo"] == "video":
            e["videoDuration"] = str(int(b.get("clip_s", c["clip_s"])))
            if c["combinar"] and "scene two" not in p.lower():
                avisos.append(f"{b['id']}: clip combinado sin «scene two» (ver plantilla en docs/estilo_secuencia_flow.md)")
        esc.append(e)
        lineas.append(p)
    os.makedirs("flow", exist_ok=True)
    open("flow/prompts.txt", "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    json.dump(esc, open("flow/escenas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nv = sum(1 for e in esc if e["mediaType"] == "video")
    print(f"flow/prompts.txt y flow/escenas.json: {len(esc)} prompts ({nv} video + {len(esc) - nv} imagen)")
    durs = sorted({e["videoDuration"] for e in esc if e["mediaType"] == "video"}, key=int)
    print(f"Flow: {nv} clips de {' y '.join(durs) or int(c['clip_s'])} s en {c['video_calidad']}" + (" (2 escenas por clip)" if c["combinar"] else "")
          + f" · {ASPECTO} · carpeta de descarga «{c['carpeta_descargas']}»")
    for a in avisos:
        print("  aviso:", a)


# ------------------------------------------------------------------ medios
def dir_medios():
    """medios/ pesa (clips de video): nace en E: con junction, igual que salida/ y segmentos/."""
    if not os.path.exists("medios"):
        try:
            import mover_pesados as MP
            if os.path.isdir(os.path.splitdrive(MP.DESTINO)[0] + "\\"):
                dst = os.path.join(MP.DESTINO, "videos", os.path.basename(os.getcwd()), "medios")
                os.makedirs(dst, exist_ok=True)
                MP.crear_junction(os.path.abspath("medios"), dst)
        except Exception as ex:                      # sin E: o sin permiso: carpeta normal
            print(f"(aviso) medios/ queda en C: ({ex})")
        os.makedirs("medios", exist_ok=True)
    return "medios"


def medio_de(b):
    """Archivo real del beat (el tipo lo decide la extensión que de verdad llegó, no lo planeado)."""
    for ext in EXT_VIDEO + EXT_IMG:
        r = os.path.join("medios", b["id"] + ext)
        if os.path.exists(r) and os.path.getsize(r) > 2000:
            return r
    return None


def ingesta(args):
    c = cfg()
    bs = cargar_beats()
    espera = 0.0
    if "--espera" in args:
        i = args.index("--espera")
        espera = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    carpeta = args[0] if args else c["carpeta_descargas"]
    if not os.path.isabs(carpeta):
        carpeta = os.path.join(os.path.expanduser("~"), "Downloads", carpeta)
    dir_medios()
    ids = {b["id"] for b in bs}
    print(f"ingesta: {carpeta} -> medios/ ({len(ids)} beats; espera {'sin límite' if espera == 0 else f'{espera:.0f} s'})", flush=True)
    t_ini, ultimo, tam_previo, raros = time.time(), time.time(), {}, set()
    while True:
        for ruta in sorted(glob.glob(os.path.join(carpeta, "scene-*"))):
            nombre = os.path.basename(ruta)
            m = re.fullmatch(r"(scene-\d{3,})(\.\w+)", nombre)
            if not m or m.group(2).lower() not in EXT_VIDEO + EXT_IMG:
                if not nombre.endswith((".crdownload", ".tmp")) and nombre not in raros:
                    raros.add(nombre)
                    print(f"  (ignoro) {nombre}", flush=True)
                continue
            sid, ext = m.group(1), m.group(2).lower()
            if sid not in ids:
                continue
            tam = os.path.getsize(ruta)
            if tam_previo.get(ruta) != tam:           # todavía se está escribiendo: espera a que el tamaño se repita
                tam_previo[ruta] = tam
                continue
            dst = os.path.join("medios", sid + ext)
            if os.path.exists(dst) and os.path.getsize(dst) == tam:
                continue
            for viejo in glob.glob(os.path.join("medios", sid + ".*")):
                os.remove(viejo)
            shutil.copy2(ruta, dst)
            ultimo = time.time()
            hechos = sum(1 for b in bs if medio_de(b))
            print(f"  {sid}{ext}  ({hechos}/{len(bs)})", flush=True)
        faltan = [b["id"] for b in bs if not medio_de(b)]
        if not faltan:
            print(f"COMPLETO: {len(bs)}/{len(bs)} medios en {time.time() - t_ini:.0f} s")
            return
        if espera and time.time() - ultimo > espera:
            print(f"SIN NOVEDAD en {espera:.0f} s. Faltan {len(faltan)}: {' '.join(faltan[:40])}")
            sys.exit(2)
        time.sleep(4)


def medios_hoja():
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    bs = cargar_beats()
    os.makedirs("previews", exist_ok=True)
    cw, ch, cols, fil = (270, 480, 10, 2) if VERTICAL else (480, 270, 5, 4)
    fnt = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
    fch = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    n_hojas = math.ceil(len(bs) / (cols * fil))
    for h in range(n_hojas):
        hoja = Image.new("RGB", (cols * cw, fil * (ch + 46)), (18, 18, 20))
        d = ImageDraw.Draw(hoja)
        for k, b in enumerate(bs[h * cols * fil:(h + 1) * cols * fil]):
            x, y = (k % cols) * cw, (k // cols) * (ch + 46)
            r = medio_de(b)
            if r:
                if r.lower().endswith(EXT_VIDEO):
                    cap = cv2.VideoCapture(r)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * 0.5))
                    ok, im = cap.read()
                    cap.release()
                else:
                    im = cv2.imdecode(np.fromfile(r, np.uint8), cv2.IMREAD_COLOR)
                    ok = im is not None
                if ok:
                    im = cv2.resize(_cubrir(im, cw, ch), (cw, ch), interpolation=cv2.INTER_AREA)
                    hoja.paste(Image.fromarray(im[:, :, ::-1]), (x, y))
            else:
                d.rectangle([x + 2, y + 2, x + cw - 3, y + ch - 3], outline=(170, 40, 40), width=3)
                d.text((x + cw // 2 - 28, y + ch // 2 - 12), "FALTA", font=fnt, fill=(230, 80, 80))
            etiqueta = f"{b['id'][6:]} {'VIDEO ' if (r or '').lower().endswith(EXT_VIDEO) else ''}{b['t0']:.0f}s"
            d.text((x + 6, y + ch + 2), etiqueta, font=fnt, fill=(255, 214, 90))
            d.text((x + 6, y + ch + 24), b["texto"][:cw // 8 + 2], font=fch, fill=(225, 225, 225))
        ruta = f"previews/medios_{h + 1:02d}.jpg"
        hoja.save(ruta, quality=88)
        print(ruta)
    faltan = [b["id"] for b in bs if not medio_de(b)]
    print(f"{len(bs) - len(faltan)}/{len(bs)} medios" + (f" · faltan: {' '.join(faltan[:30])}" if faltan else ""))


# ------------------------------------------------------------------ armado
def _cubrir(im, w, h):
    """Recorta al aspecto w:h (centrado) sin deformar."""
    ih, iw = im.shape[:2]
    if iw * h > ih * w:
        nw = int(round(ih * w / h))
        x = (iw - nw) // 2
        return im[:, x:x + nw]
    nh = int(round(iw * h / w))
    y = (ih - nh) // 2
    return im[y:y + nh]


class Imagen:
    """Imagen fija con movimiento de cámara lento (zoom + deriva), distinto y determinista por beat."""

    def __init__(self, ruta, b, k, cam=None):
        import cv2
        import numpy as np
        self.cam = cam                               # cámara dirigida (efectos.py CAMARA): dict(a=(zoom, cx, cy), b=(zoom, cx, cy))
        if ruta.lower().endswith(EXT_VIDEO):         # un clip usado como imagen fija (repasos de la capa de efectos): su cuadro central
            cap = cv2.VideoCapture(ruta)
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * 0.5))
            im = cap.read()[1]
            cap.release()
        else:
            im = cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_COLOR)
        if im is None:
            raise SystemExit(f"No pude leer {ruta}")
        im = _cubrir(im, W, H)
        self.SW, self.SH = int(W * 1.3), int(H * 1.3)
        inter = cv2.INTER_AREA if im.shape[1] > self.SW else cv2.INTER_LANCZOS4
        self.im = cv2.resize(im, (self.SW, self.SH), interpolation=inter)
        self.t0, self.dur = b["t0"], max(0.5, b["t1"] - b["t0"])
        modo = (k * 7 + 3) % 6                       # acercar, alejar y cuatro derivas: nunca dos seguidas iguales
        amp = min(0.10, 0.045 + 0.011 * self.dur)    # más recorrido cuanto más dura la imagen en pantalla
        z = [(1.0, 1 + amp), (1 + amp, 1.0), (1.04, 1.04 + amp * 0.6), (1.04 + amp * 0.6, 1.04),
             (1.02, 1.02 + amp * 0.8), (1.02 + amp * 0.8, 1.02)][modo]
        d = [(0, 0, 0, 0), (0, 0, 0, 0), (-1, 0, 1, 0), (1, 0, -1, 0), (0, 0.6, 0, -0.6), (0.7, -0.5, -0.7, 0.5)][modo]
        self.z, self.d = z, d

    def cuadro(self, t):
        import cv2
        import numpy as np
        u = (t - self.t0) / self.dur                 # sin tope: durante el fundido de salida sigue moviéndose
        if self.cam:                                 # dirigida: de a=(zoom, cx, cy) a b=(zoom, cx, cy), con arranque y frenado suaves
            e = max(0.0, min(1.0, u))
            e = e * e * (3 - 2 * e)
            (z0, x0, y0), (z1, x1, y1) = self.cam["a"], self.cam["b"]
            z = max(1.0, z0 + (z1 - z0) * e)
            esc = z * W / self.SW
            holg_x, holg_y = (z - 1) * W / 2, (z - 1) * H / 2
            dx, dy = -(x0 + (x1 - x0) * e) * holg_x, -(y0 + (y1 - y0) * e) * holg_y   # cx=1: encuadra el borde derecho
            M = np.float32([[esc, 0, W / 2 - esc * self.SW / 2 + dx], [0, esc, H / 2 - esc * self.SH / 2 + dy]])
            return cv2.warpAffine(self.im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        z = self.z[0] + (self.z[1] - self.z[0]) * u
        z = max(1.0, z)
        esc = z * W / self.SW * 1.0
        holg_x, holg_y = (z - 1) * W / 2, (z - 1) * H / 2
        dx = (self.d[0] + (self.d[2] - self.d[0]) * u) * holg_x * 0.9
        dy = (self.d[1] + (self.d[3] - self.d[1]) * u) * holg_y * 0.9
        dx, dy = max(-holg_x, min(holg_x, dx)), max(-holg_y, min(holg_y, dy))
        M = np.float32([[esc, 0, W / 2 - esc * self.SW / 2 + dx], [0, esc, H / 2 - esc * self.SH / 2 + dy]])
        return cv2.warpAffine(self.im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


class Clip:
    """Clip de video de Flow ajustado a la duración del beat (0,6x–1,6x); si aún sobra beat, congela el último cuadro."""

    def __init__(self, ruta, b, k):
        import cv2
        self.cap = cv2.VideoCapture(ruta)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 24.0
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.n < 2:
            raise SystemExit(f"Clip vacío o ilegible: {ruta}")
        self.t0, self.dur = b["t0"], max(0.5, b["t1"] - b["t0"])
        self.vel = vel_clip(self.n / self.fps, self.dur)
        self.i, self.ult = -1, None
        c = cfg()
        self.rec = float(c.get("recorte_por", {}).get(b["id"], c.get("recorte_clip", 0.0)))   # fracción que se recorta por lado

    def cuadro(self, t):
        import cv2
        obj = int(max(0.0, t - self.t0) * self.vel * self.fps)
        obj = min(obj, self.n - 1)
        while self.i < obj:
            ok, f = self.cap.read()
            if not ok:
                break
            self.i += 1
            self.ult = f
        f = self.ult
        if self.rec > 0:                              # quita el marco de viñeta que Flow a veces dibuja en el borde
            h, w = f.shape[:2]
            dx, dy = int(w * self.rec), int(h * self.rec)
            f = f[dy:h - dy, dx:w - dx]
        f = _cubrir(f, W, H)
        if f.shape[1] != W:
            f = cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA if f.shape[1] > W else cv2.INTER_LANCZOS4)
        return f


def vel_clip(dur_clip, dur_beat):
    return max(0.6, min(1.6, dur_clip / max(0.5, dur_beat)))


def ambiente():
    """audio/ambiente.wav: el audio de cada clip de Flow en su beat, a la misma velocidad que su imagen, igualado de
    nivel entre clips y con el volumen de SECUENCIA (ambiente / ambiente_por). `mezcla` lo suma por debajo de la voz."""
    import numpy as np
    import soundfile as sf
    from sinte import SR
    c = cfg()
    bs = cargar_beats()
    N = int(bs[-1]["t1"] * SR)
    out = np.zeros((N, 2), np.float32)
    os.makedirs("audio", exist_ok=True)
    tmp, usados = os.path.join("audio", "_amb_tmp.wav"), 0
    for b in bs:
        r = medio_de(b)
        vol = float(c["ambiente_por"].get(b["id"], c["ambiente"]))
        if not r or not r.lower().endswith(EXT_VIDEO) or vol <= 0:
            continue
        info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type", "-of", "json", r],
                              capture_output=True, text=True).stdout
        info = json.loads(info or "{}")
        if not any(st.get("codec_type") == "audio" for st in info.get("streams", [])):
            continue
        dur = b["t1"] - b["t0"]
        vel = vel_clip(float(info["format"]["duration"]), dur)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", r, "-vn", "-af", f"atempo={vel:.4f}", "-ar", str(SR), "-ac", "2",
                        "-t", f"{dur:.3f}", tmp], check=True)
        x, _ = sf.read(tmp, always_2d=True, dtype="float32")
        rms = float(np.sqrt(np.mean(x ** 2) + 1e-12))
        if rms < 1e-4:                                # clip mudo
            continue
        x *= min(8.0, 0.05 / rms) * vol / 0.5          # todos los clips al mismo nivel; `vol` escala desde el 50 % de referencia
        f = min(int(0.2 * SR), len(x) // 3)
        x[:f] *= np.linspace(0, 1, f)[:, None]
        x[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(b["t0"] * SR)
        out[i:i + len(x)] += x[:N - i]
        usados += 1
    if os.path.exists(tmp):
        os.remove(tmp)
    if usados == 0:
        if os.path.exists("audio/ambiente.wav"):
            os.remove("audio/ambiente.wav")
        print("ambiente: ningún clip con audio (o volumen 0): la mezcla va sin ambiente")
        return
    out = np.tanh(out * 2.0) / 2.0                    # picos suaves: un golpe fuerte de un clip no debe saturar
    sf.write("audio/ambiente.wav", out, SR, subtype="PCM_16")
    print(f"audio/ambiente.wav: {usados} clips con su sonido (volumen general {c['ambiente']:.0%})")


def servir(args):
    """Puente local con la página de Flow (solo acepta a https://flow.google.com), en http://127.0.0.1:8791:
      GET  /escenas.json        entrega flow/escenas.json (para lanzar el lote con una llamada corta)
      POST /medio/scene-XXX     recibe los bytes del resultado y los guarda en medios/scene-XXX.jpg|.mp4
      POST /video_listo/scene-XXX   clip en 360p: toma de Descargas la «720p mejorada» que bajó Flow y la guarda en medios/
    La página manda cada resultado con RECOLECTOR_JS (docs/estilo_secuencia_flow.md): así no dependemos de las descargas
    de Chrome. Se apaga solo al completar todas las escenas o al pasar `min` minutos sin novedad (por defecto 20)."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    datos = open("flow/escenas.json", "rb").read()
    ids = [e["sceneId"] for e in json.loads(datos)]
    minutos = float(args[0]) if args else 20.0
    dir_medios()
    estado = dict(ultimo=time.time())
    EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "video/mp4": ".mp4", "video/webm": ".webm"}

    def hechos():
        return [i for i in ids if any(os.path.exists(os.path.join("medios", i + x)) for x in EXT_VIDEO + EXT_IMG)]

    DESC = os.path.join(os.path.expanduser("~"), "Downloads")
    reclamados = set()

    def reclamar(sid, espera=50.0):
        """El .mp4 más nuevo de Descargas (hasta 2 niveles) que apareció en los últimos 3 min y nadie reclamó: es la descarga
        «720p mejorada» de la escena que acaba de terminar (la cola va de una en una). Devuelve su alto o None."""
        fin = time.time() + espera
        propio = os.path.join(DESC, cfg()["carpeta_descargas"], sid + ".mp4")
        while time.time() < fin:
            # flowscrap guarda cada clip con su nombre: si existe, es ESE (11-oct-2026: tras reiniciar `servir`, el
            # «más nuevo sin reclamar» volvió a dar el clip anterior y los clips quedaron corridos una posición)
            cands = [r for r in glob.glob(os.path.join(DESC, "*.mp4")) + glob.glob(os.path.join(DESC, "*", "*.mp4"))
                     if r not in reclamados and time.time() - os.path.getmtime(r) < 180]
            if os.path.exists(propio):
                cands = [propio]
            if cands:
                r = max(cands, key=os.path.getmtime)
                t1 = os.path.getsize(r)
                time.sleep(1.5)
                if os.path.getsize(r) == t1 and t1 > 20000:      # ya no crece: descarga completa
                    alto = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height",
                                           "-of", "csv=p=0", r], capture_output=True, text=True).stdout.strip()
                    for viejo in glob.glob(os.path.join("medios", sid + ".*")):
                        os.remove(viejo)
                    shutil.copy2(r, os.path.join("medios", sid + ".mp4"))
                    reclamados.add(r)
                    return int(alto) if alto.isdigit() else 0
            time.sleep(2)
        return None

    class M(BaseHTTPRequestHandler):
        def _cab(self, codigo, cuerpo=b""):
            self.send_response(codigo)
            self.send_header("Access-Control-Allow-Origin", "https://flow.google.com")
            self.send_header("Access-Control-Allow-Private-Network", "true")
            self.send_header("Access-Control-Allow-Headers", "content-type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def do_OPTIONS(self):
            self._cab(204)

        def do_GET(self):
            ruta = self.path.split("?")[0]
            if ruta == "/escenas.json":
                return self._cab(200, datos)
            if ruta == "/estado":
                h = hechos()
                return self._cab(200, json.dumps(dict(hechos=len(h), total=len(ids), faltan=[i for i in ids if i not in h])).encode())
            self._cab(404)

        def do_POST(self):
            v = re.fullmatch(r"/video_listo/(scene-\d{3,})", self.path.split("?")[0])
            if v and v.group(1) in ids:
                alto = reclamar(v.group(1))
                if alto is None:
                    print(f"  {v.group(1)}: no apareció la descarga mejorada en Descargas", flush=True)
                    return self._cab(404)
                estado["ultimo"] = time.time()
                print(f"  {v.group(1)}.mp4  descarga mejorada, {alto} px de alto  ({len(hechos())}/{len(ids)})", flush=True)
                return self._cab(200, json.dumps(dict(alto=alto)).encode())
            m = re.fullmatch(r"/medio/(scene-\d{3,})", self.path.split("?")[0])
            ext = EXT.get((self.headers.get("Content-Type") or "").split(";")[0].strip())
            n = int(self.headers.get("Content-Length") or 0)
            if not m or m.group(1) not in ids or not ext or not (2000 < n < 400_000_000):
                return self._cab(400)
            cuerpo = self.rfile.read(n)
            for viejo in glob.glob(os.path.join("medios", m.group(1) + ".*")):
                os.remove(viejo)
            open(os.path.join("medios", m.group(1) + ext), "wb").write(cuerpo)
            estado["ultimo"] = time.time()
            print(f"  {m.group(1)}{ext}  {n / 1e6:.1f} MB  ({len(hechos())}/{len(ids)})", flush=True)
            self._cab(200, b"{}")

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 8791), M)
    srv.timeout = 5
    print(f"puente Flow: {len(ids)} escenas en http://127.0.0.1:8791 (se apaga tras {minutos:.0f} min sin novedad)", flush=True)
    while True:
        srv.handle_request()
        if len(hechos()) == len(ids):
            print(f"COMPLETO: {len(ids)}/{len(ids)} medios")
            return
        if time.time() - estado["ultimo"] > minutos * 60:
            h = hechos()
            print(f"SIN NOVEDAD en {minutos:.0f} min: {len(h)}/{len(ids)}. Faltan: {' '.join(i for i in ids if i not in h)[:600]}")
            sys.exit(2)


class Falta:
    """Solo con --borrador: tarjeta oscura con el id y la frase, para ver el ritmo antes de que Flow termine."""

    def __init__(self, b):
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
        im = Image.new("RGB", (W, H), (22, 22, 26))
        d = ImageDraw.Draw(im)
        d.text((90, 80), f"{b['id']} · {b['tipo']} · {b['t1'] - b['t0']:.1f} s", font=ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 54), fill=(255, 214, 90))
        f2, y = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 46), 220
        linea = ""
        for p in b["texto"].split():
            if len(linea) + len(p) > (34 if VERTICAL else 62):
                d.text((90, y), linea, font=f2, fill=(230, 230, 230))
                y, linea = y + 64, ""
            linea += p + " "
        d.text((90, y), linea, font=f2, fill=(230, 230, 230))
        self.f = np.asarray(im)[:, :, ::-1].copy()

    def cuadro(self, t):
        return self.f


def _fuente(b, k, borrador, capa=None):
    r = medio_de(b)
    if r is None:
        if borrador:
            return Falta(b)
        raise SystemExit(f"Falta el medio de {b['id']} (medios/{b['id']}.jpg|.mp4). Usa --borrador para armar con tarjetas.")
    return Clip(r, b, k) if r.lower().endswith(EXT_VIDEO) else Imagen(r, b, k, capa.camaras.get(b["id"]) if capa else None)


def video(args):
    import cv2
    c = cfg()
    bs = cargar_beats()
    borrador = "--borrador" in args
    tramo = None
    if "--tramo" in args:
        a, b_ = args[args.index("--tramo") + 1].split("-")
        tramo = (float(a), float(b_))
    total = bs[-1]["t1"]
    f0, f1 = (0, int(round(total * FPS))) if not tramo else (int(tramo[0] * FPS), int(min(total, tramo[1]) * FPS))
    if not borrador:
        faltan = [b["id"] for b in bs if not medio_de(b) and b["t1"] > f0 / FPS and b["t0"] < f1 / FPS]
        if faltan:
            raise SystemExit(f"Faltan {len(faltan)} medios: {' '.join(faltan[:40])}")
    os.makedirs("salida", exist_ok=True)
    salida = "salida/video_sin_audio.mp4" if not tramo else f"salida/tramo_{int(tramo[0])}_{int(tramo[1])}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", os.environ.get("FAB_PRESET", "medium"),
                           "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    import secuencia_fx
    capa = secuencia_fx.cargar()                      # efectos.py del video (cámara dirigida, golpes, rótulos); None = armado de siempre
    if capa:
        print(f"  con efectos.py: {len(capa.fx)} efectos, {len(capa.rot)} rótulos, {len(capa.camaras)} cámaras dirigidas", flush=True)
    fund0 = float(c["fundido"])
    fund = fund0
    k, act, prev, t_ini = None, None, None, time.time()
    for f in range(f0, f1):
        t = f / FPS
        kk = next((i for i, b in enumerate(bs) if b["t0"] <= t < b["t1"]), len(bs) - 1)
        if kk != k:
            prev = act if (k is not None and kk == k + 1) else None
            k, act = kk, _fuente(bs[kk], kk, borrador, capa)
            if capa:
                act, fund = capa.envolver(act, bs[kk]), capa.fundido(bs[kk]["id"], fund0)
        img = act.cuadro(t)
        if prev is not None and fund > 0:
            u = (t - bs[k]["t0"]) / fund
            if u < 1.0:
                u = u * u * (3 - 2 * u)
                if c.get("transicion") == "slideleft":      # motor yt (Warcraft): el clip nuevo empuja al anterior hacia la izquierda
                    import numpy as np
                    d = int(round(u * W))
                    img = np.concatenate([prev.cuadro(t)[:, d:], img[:, :d]], axis=1) if 0 < d < W else img
                else:
                    img = cv2.addWeighted(prev.cuadro(t), 1 - u, img, u, 0)
            else:
                prev = None
        if capa:
            img = capa.aplicar(img, t)
        ff.stdin.write(img.tobytes())
        if (f - f0) % (FPS * 20) == 0:
            hecho = (f - f0 + 1) / max(1, f1 - f0)
            print(f"  {t:7.1f}s / {total:.1f}s  {hecho * 100:4.0f}%  {bs[k]['id']}  ({time.time() - t_ini:.0f}s)", flush=True)
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg falló al codificar")
    print(f"listo: {salida}  {os.path.getsize(salida) / 1e6:.1f} MB  en {time.time() - t_ini:.0f}s")
    if not tramo:
        ambiente()


if __name__ == "__main__":
    orden, resto = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if orden == "beats":
        beats()
    elif orden == "prompts":
        prompts()
    elif orden == "ingesta":
        ingesta(resto)
    elif orden == "medios":
        medios_hoja()
    elif orden == "servir":
        servir(resto)
    elif orden == "ambiente":
        ambiente()
    elif orden == "video":
        video(resto)
    else:
        raise SystemExit(__doc__)
