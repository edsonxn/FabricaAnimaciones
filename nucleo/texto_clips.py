# -*- coding: utf-8 -*-
"""Busca TEXTO QUEMADO en los clips de gameplay (subtítulos de youtuber, rótulos, títulos de otro canal) con OCR local.
13-nov-2026 (el usuario, tes_reina_loba: «el video detrás tiene texto que no debe ir» = subtítulos en inglés «and grab the tombs
key on him» bajo una pegatina). `_hoja_clips.py` solo mira 2 cuadros chicos por clip y los subtítulos van y vienen: esto mira
UN cuadro por segundo de cada clip.

    python nucleo/texto_clips.py <v> [-j 4] [--clips 12,15]
→ videos/<v>/previews/texto_clips.json + lista en pantalla de los clips con texto (segundo y lo leído) → `bajar N --rehacer`.
Ignora lo corto (brújula N/E/S/O, números del HUD): marca un cuadro si lee ≥ 2 palabras de ≥ 3 letras con confianza ≥ 0,6."""
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ocr = None


def _lee(img):
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    res, _ = _ocr(img)
    out = []
    for caja, txt, conf in res or []:
        if float(conf) >= .6:
            out.append(txt.strip())
    return out


def _palabras(lineas):
    return [w for l in lineas for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ']{3,}", l)]


def clip(ruta):
    """[(segundo, [líneas]), …] de los cuadros con texto."""
    hallado = []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", ruta, "-vf", "fps=1,scale=960:-2", "-q:v", "3",
                        os.path.join(tmp, "c_%03d.jpg")], check=False)
        for f in sorted(os.listdir(tmp)):
            lineas = _lee(os.path.join(tmp, f))
            if len(_palabras(lineas)) >= 2:
                hallado.append((int(f[2:5]) - 1, lineas))
    return os.path.basename(ruta)[:-4], hallado


def main():
    a = sys.argv[1:]
    v = a[0]
    j = int(a[a.index("-j") + 1]) if "-j" in a else 4
    med = os.path.join(RAIZ, "videos", v, "medios")
    clips = sorted(f for f in os.listdir(med) if f.startswith("scene-") and f.endswith(".mp4"))
    if "--clips" in a:
        quiero = {f"scene-{int(x):03d}.mp4" for x in a[a.index("--clips") + 1].split(",")}
        clips = [c for c in clips if c in quiero]
    res = {}
    with ProcessPoolExecutor(j) as ex:
        for nombre, hallado in ex.map(clip, [os.path.join(med, c) for c in clips]):
            if hallado:
                res[nombre] = hallado
                print(f"⚠ {nombre}: texto en {len(hallado)} s → " + " | ".join(" / ".join(l) for _, l in hallado[:3])[:160], flush=True)
    sal = os.path.join(RAIZ, "videos", v, "previews", "texto_clips.json")
    json.dump(res, open(sal, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(res)} de {len(clips)} clips con texto quemado → {sal}")
    if res:
        print("rehacer: python fab.py", v, "bajar", ",".join(str(int(k[6:])) for k in sorted(res)), "--rehacer  (o cambiar la fuente)")


if __name__ == "__main__":
    main()
