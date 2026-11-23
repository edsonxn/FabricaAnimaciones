# -*- coding: utf-8 -*-
"""Busca TEXTO QUEMADO AJENO en los clips de gameplay (subtítulos de youtuber, rótulos, títulos de otro canal) con OCR local.
13-nov-2026 (el usuario, tes_reina_loba: «el video detrás tiene texto que no debe ir» = subtítulos en inglés «and grab the tombs
key on him» bajo una pegatina). `_hoja_clips.py` solo mira 2 cuadros chicos por clip y los subtítulos van y vienen: esto mira
UN cuadro por segundo de cada clip.

22-nov-2026 (el usuario: «arréglalo»): marcaba 168 de 210 clips en wow_errores_60 y 146 de 185 en er_rykard, casi todo HUD del
propio juego (chat, medidores de daño, nombres, misión), que la regla (15) de docs/estilo_secuencia_yt.md SÍ permite: la lista
no servía y se revisaba a mano. Ahora solo cuenta el texto con forma de AJENO, por la caja que da el OCR:
  · SUBTÍTULO: centrado (centro a ≤ 15 % del medio), en el tercio de abajo, letra ≥ 3 % del alto y ancho ≥ 15 %;
  · RÓTULO: centrado y ancho (≥ 35 %) con letra ≥ 4 %, a cualquier altura;
  · TÍTULO/MARCA GRANDE: letra ≥ 6 % del alto, en cualquier sitio.
Subtítulo y rótulo piden además una FRASE (≥ 12 letras en la línea: los nombres flotantes de jugadores y PNJ son más cortos);
el título grande, ≥ 4 letras. El OCR a veces pega las palabras («andgrabthetombskeyonhim»): por eso cuenta letras, no palabras.
El HUD (letra chica, esquinas y bordes: chat, medidores, misión, minimapa) queda fuera. Confianza ≥ 0,6.
Probado el 22-nov con 18 clips de wow_errores_60 (todos marcados antes: 0 ahora) y dos controles con texto quemado a propósito
(subtítulo amarillo abajo y título grande arriba: los dos salen).

    python nucleo/texto_clips.py <v> [-j 4] [--clips 12,15]   OCR + filtro → previews/texto_clips.json (+ _cajas.json)
    python nucleo/texto_clips.py <v> --refiltrar               re-filtra las cajas guardadas sin volver a pasar el OCR
    python nucleo/texto_clips.py <v> --todo                    como antes: TODO el texto, HUD incluido
→ lista en pantalla de los clips con texto ajeno (segundo y lo leído) → `bajar N --rehacer`.
`previews/texto_clips_cajas.json` guarda todas las cajas de cada cuadro: para cambiar umbrales basta `--refiltrar` (segundos)."""
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = .6
SUB_DX, SUB_Y, SUB_H, SUB_W = .15, .66, .03, .15   # subtítulo: centrado, abajo, letra y ancho mínimos (fracción del cuadro)
ROT_W, ROT_H = .35, .04                            # rótulo centrado y ancho
GRANDE_H = .06                                     # título o marca de agua grande
FRASE, NOMBRE = 12, 4                              # letras mínimas: subtítulo/rótulo, título grande
_ocr = None


def _lee(img):
    """(W, H, [[x0, y0, x1, y1, texto, conf], …]) de un cuadro."""
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    res, _ = _ocr(img)
    from PIL import Image
    with Image.open(img) as im:
        W, H = im.size
    cajas = []
    for caja, txt, conf in res or []:
        xs, ys = [p[0] for p in caja], [p[1] for p in caja]
        cajas.append([round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys)), txt.strip(), round(float(conf), 3)])
    return W, H, cajas


def _palabras(lineas):
    return [w for l in lineas for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ']{3,}", l)]


def _letras(t):
    return len(re.findall(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü]", t))


def _forma(c, W, H):
    """'grande' | 'subtitulo' | 'rotulo' | None (HUD, nombres flotantes u otro texto chico/de borde)."""
    x0, y0, x1, y1, txt = c[:5]
    w, h = (x1 - x0) / W, (y1 - y0) / H
    cx, cy = (x0 + x1) / 2 / W, (y0 + y1) / 2 / H
    n = _letras(txt)
    if "<" in txt or ">" in txt:  # título de PNJ/mascota/hermandad bajo el nombre flotante («<Goldbond's Minion>»): es del juego
        return None
    if h >= GRANDE_H and n >= NOMBRE:
        return "grande"
    centrado = abs(cx - .5) <= SUB_DX
    if centrado and cy >= SUB_Y and h >= SUB_H and w >= SUB_W and n >= FRASE:
        return "subtitulo"
    if centrado and w >= ROT_W and h >= ROT_H and n >= FRASE:
        return "rotulo"
    return None


def filtrar(info, todo=False):
    """[(segundo, [líneas]), …] de los cuadros con texto ajeno, a partir de las cajas guardadas de un clip."""
    W, H, cuadros = info["W"], info["H"], info["cuadros"]
    out = []
    for s, cajas in cuadros:
        if todo:
            lineas = [c[4] for c in cajas if c[5] >= CONF]
            if len(_palabras(lineas)) >= 2:
                out.append((s, lineas))
            continue
        lineas = [c[4] for c in cajas if c[5] >= CONF and _forma(c, W, H)]
        if lineas:
            out.append((s, lineas))
    return out


def clip(ruta):
    """(nombre, {W, H, n, cuadros: [[segundo, cajas], …]}) — solo guarda los cuadros con algo leído."""
    info = {"W": 960, "H": 540, "n": 0, "cuadros": []}
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", ruta, "-vf", "fps=1,scale=960:-2", "-q:v", "3",
                        os.path.join(tmp, "c_%03d.jpg")], check=False)
        fotos = sorted(os.listdir(tmp))
        info["n"] = len(fotos)
        for f in fotos:
            W, H, cajas = _lee(os.path.join(tmp, f))
            info["W"], info["H"] = W, H
            if cajas:
                info["cuadros"].append([int(f[2:5]) - 1, cajas])
    return os.path.basename(ruta)[:-4], info


def main():
    a = sys.argv[1:]
    v = a[0]
    j = int(a[a.index("-j") + 1]) if "-j" in a else 4
    todo = "--todo" in a
    prev = os.path.join(RAIZ, "videos", v, "previews")
    ruta_cajas = os.path.join(prev, "texto_clips_cajas.json")
    if "--refiltrar" in a:
        cajas = json.load(open(ruta_cajas, encoding="utf-8"))
        total = len(cajas)
    else:
        med = os.path.join(RAIZ, "videos", v, "medios")
        clips = sorted(f for f in os.listdir(med) if f.startswith("scene-") and f.endswith(".mp4"))
        if "--clips" in a:
            quiero = {f"scene-{int(x):03d}.mp4" for x in a[a.index("--clips") + 1].split(",")}
            clips = [c for c in clips if c in quiero]
        total = len(clips)
        try:  # con --clips se conservan las cajas del resto de clips
            cajas = json.load(open(ruta_cajas, encoding="utf-8")) if "--clips" in a else {}
        except (OSError, ValueError):
            cajas = {}
        with ProcessPoolExecutor(j) as ex:
            for nombre, info in ex.map(clip, [os.path.join(med, c) for c in clips]):
                cajas[nombre] = info
        os.makedirs(prev, exist_ok=True)
        json.dump(cajas, open(ruta_cajas, "w", encoding="utf-8"), ensure_ascii=False)
    res = {}
    for nombre in sorted(cajas):
        hallado = filtrar(cajas[nombre], todo)
        if hallado:
            res[nombre] = hallado
            print(f"⚠ {nombre}: texto en {len(hallado)} s → " + " | ".join(" / ".join(l) for _, l in hallado[:3])[:160], flush=True)
    sal = os.path.join(prev, "texto_clips.json")
    json.dump(res, open(sal, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    que = "con texto (TODO, HUD incluido)" if todo else "con texto ajeno (subtítulos, rótulos, títulos; el HUD no cuenta)"
    print(f"\n{len(res)} de {len(cajas)} clips {que} → {sal}")
    if res:
        print("rehacer: python fab.py", v, "bajar", ",".join(str(int(k[6:])) for k in sorted(res) if k[6:].isdigit()), "--rehacer  (o cambiar la fuente)")


if __name__ == "__main__":
    main()
