# -*- coding: utf-8 -*-
"""Voz con Applio (Edge TTS + conversión RVC), la voz de Crónicas de Warcraft. Lo llama tts_gen.py cuando guion.py trae
VOZ["motor"] = "applio".

guion.py:  VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal",
                      pitch=0, rate=0, idioma="es", referencia="<wav de muestra para la similitud de tts_select>")
Mismos parámetros que usaba el sistema viejo (C:\\googleimagenes\\applio-client.js): index_rate 0.75, protect 0.5,
f0 rmvpe, sin índice, contentvec. Edge TTS necesita internet; RVC corre en la GPU (no a la vez que un render ni Chatterbox).
Edge TTS es determinista: una sola toma por frase (las «semillas» se ignoran salvo la primera). Para variar una frase
que salió mal, se reescribe el texto en guion.py (cambio de texto = se regenera sola).
Paso 1 (Edge TTS) con el python de la Fábrica (edge-tts 7.3.0; el 7.2.8 de Applio da 403). Paso 2 (RVC): todas las
frases en UN proceso con el python de Applio (carga el modelo una vez): nucleo/applio_lote.py.
"""
import asyncio
import json
import os
import shutil
import subprocess
import tempfile

APPLIO = r"C:\applio2\Applio"
PY_APPLIO = os.path.join(APPLIO, "env", "python.exe")
LOTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "applio_lote.py")


async def _edge(trabajos, voz, rate, carpeta):
    """Paso 1 con el edge-tts de la Fábrica (el de Applio, 7.2.8, ya recibe 403 de Microsoft): mp3 crudo por frase."""
    import edge_tts
    for t in trabajos:
        t["crudo"] = os.path.join(carpeta, t["key"] + ".mp3")
        for intento in range(4):
            try:
                await edge_tts.Communicate(t["texto"], voz, rate=f"{rate:+d}%").save(t["crudo"])
                break
            except Exception as e:   # cortes de red de Microsoft: reintentar
                if intento == 3:
                    raise SystemExit(f"Edge TTS falló en {t['key']}: {e}")
                await asyncio.sleep(3 * (intento + 1))


def ruta_pth(rvc):
    if os.path.isabs(rvc):
        return rvc
    return os.path.join(APPLIO, "logs", "VOCES", rvc if rvc.endswith(".pth") else rvc + ".pth")


def generar(frases, seeds, solo, out):
    import config
    v = config.VOZ
    seed = seeds[0] if seeds else 1
    trabajos = []
    for esc, idx, texto in frases:
        key = f"{esc}_{idx}"
        if solo and key not in solo:
            continue
        path = os.path.abspath(f"{out}/{key}_s{seed}.wav")
        if not os.path.exists(path):
            trabajos.append(dict(key=key, texto=config.FRASES_TTS.get(key, texto), salida=path))
    if not trabajos:
        print("Applio: nada pendiente")
        return
    pth = ruta_pth(v.get("rvc", "RemyOriginal"))
    if not os.path.exists(pth):
        raise SystemExit(f"Applio: no existe el modelo RVC {pth}")
    job = dict(tts_voice=v.get("tts_voice", "fr-FR-RemyMultilingualNeural"), rate=int(v.get("rate", 0)),
               pitch=int(v.get("pitch", 0)), index_rate=v.get("index_rate", 0.75), protect=v.get("protect", 0.5),
               pth=pth, trabajos=trabajos)
    print(f"Applio: {len(trabajos)} frases con {os.path.basename(pth)} sobre {job['tts_voice']}", flush=True)
    tmp = tempfile.mkdtemp(prefix="applio_edge_")
    asyncio.run(_edge(trabajos, job["tts_voice"], job["rate"], tmp))
    fd, jp = tempfile.mkstemp(suffix=".json", prefix="applio_")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(job, f, ensure_ascii=False)
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([PY_APPLIO, LOTE, jp], cwd=APPLIO, env=env)
    os.remove(jp)
    shutil.rmtree(tmp, ignore_errors=True)
    faltan = [t["key"] for t in trabajos if not os.path.exists(t["salida"])]
    if r.returncode or faltan:
        raise SystemExit(f"Applio falló (código {r.returncode}); sin audio: {faltan[:20]}")
