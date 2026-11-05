# -*- coding: utf-8 -*-
"""Voz del EN VIVO con ElevenLabs (el usuario, 4-nov-2026, noche): las 7 voces de la biblioteca usadas en Crónicas de Tamriel.

Misma firma que `voz.sintetizar`. `eleven_v4_turbo` con corchetes de actuación, nunca [whispers]/[excited]/[shouts]
(`tts_eleven.SIEMPRE_FUERA`). PCM a 24 kHz → .wav (duración exacta). `tts_eleven.post` salta sola de cuenta sin saldo (la 1 está
en 0); si ninguna puede o la API falla, esa frase sale con la voz de Windows (`voz.py`) y `sin_saldo` queda en True.
Gasto: ~0,2 créditos por carácter (≈ 11 000-15 000 por hora de directo; docs/estilo_envivo.md § Costos).
"""
import os
import re
import sys
import threading
import wave
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if "config" not in sys.modules:                       # tts_eleven importa el config de un VIDEO; aquí no hay video
    import types
    sys.modules["config"] = types.SimpleNamespace(VOZ={})
import tts_eleven                                     # noqa: E402
from envivo import voz as voz_windows                 # noqa: E402

# las 7 de la biblioteca compartida de ElevenLabs que ya sonaron en Tamriel (videos/tes_dwemer_desaparicion/guion.py);
# «el Humano tras el Telón» (clon del usuario, cuentas 2 y 3) no entra: es su voz, no un narrador del directo
VOCES = {"Johnny": "HMCmDsbKeaSZp5LMOYKR", "Edoardo": "YqZLNYWZm98oKaaLZkUA", "Hope": "tnSpp4vdxKPjI9w0GnoV",
         "José": "y2ijeTfmnXjzheHO6zeN", "Mario": "tomkxGQGz4b1kE0EM722", "MariCarmen": "YDDaC9XKjODs7hY78qEW",
         "el Profeta": "HNSF1CTQmub252yhXROX"}
SR = 24000
gastado = {"creditos": 0, "caracteres": 0}
sin_saldo = False
_candado = threading.Lock()


def limpiar(t):
    t = re.sub(r"\[([^\]]+)\]\s*", lambda m: "" if any(x in m.group(1).lower() for x in tts_eleven.SIEMPRE_FUERA) else m.group(0), t)
    return re.sub(r"\s+", " ", t.replace("«", "").replace("»", "").replace("*", "")).strip()


def preparar(voz="Johnny", canal=None):
    if voz not in VOCES:
        raise ValueError(f"voz de ElevenLabs desconocida: {voz} (hay: {', '.join(VOCES)})")


def saldos():
    try:
        return [(n, s) for n, s in tts_eleven.saldos()]
    except Exception:
        return []


def _una(texto, ruta, voz):
    global sin_saldo
    body = {"text": limpiar(texto), "model_id": "eleven_v4_turbo", "voice_settings": {"stability": 0.5}, "language_code": "es"}
    try:
        r = tts_eleven.post(f"text-to-speech/{VOCES[voz]}?output_format=pcm_{SR}", json=body, timeout=60)
    except SystemExit as e:
        r = None
        print("ElevenLabs:", e, flush=True)
    if r is None or r.status_code != 200:
        sin_saldo = sin_saldo or (r is not None and r.status_code in (401, 402))
        print(f"ElevenLabs falló ({getattr(r, 'status_code', '?')}): voz de Windows para esta frase", flush=True)
        (w, d), = voz_windows.sintetizar([texto], os.path.dirname(ruta), os.path.basename(ruta)[:-4] + "_win")
        return w, d
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(r.content)
    with _candado:
        gastado["creditos"] += int(r.headers.get("character-cost") or 0)
        gastado["caracteres"] += len(body["text"])
    return ruta, len(r.content) / 2 / SR


def sintetizar(textos, carpeta, base, voz="Johnny", velocidad=None, vigente=None, voces=None):
    """textos -> [(ruta_wav, segundos)]. `voces` = una voz por frase (relevo y discusión); si no, todas con `voz`."""
    os.makedirs(carpeta, exist_ok=True)

    def hacer(i):
        t = textos[i]
        if vigente and not vigente():
            return None, max(1.5, len(limpiar(t)) / 15.0)
        v = (voces[i] if voces and i < len(voces) else voz)
        if v not in VOCES:                            # «windows» u otra: la de Windows
            (w, d), = voz_windows.sintetizar([t], carpeta, f"{base}_{i:02d}w")
            return w, d
        return _una(t, os.path.join(carpeta, f"{base}_{i:02d}.wav"), v)
    with ThreadPoolExecutor(4) as ex:                # en paralelo: un bloque de 6 frases en ~2-4 s
        return list(ex.map(hacer, range(len(textos))))


def factor():
    return None
