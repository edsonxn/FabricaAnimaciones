# -*- coding: utf-8 -*-
"""Corre DENTRO del python de Applio (C:\\applio2\\Applio\\env\\python.exe, cwd = carpeta de Applio). Lo lanza tts_applio.py.

Uso: applio_lote.py trabajo.json  con {pitch, index_rate, protect, pth, trabajos: [{key, crudo, salida}]}
`crudo` = audio de Edge TTS ya generado por tts_applio.py; aquí solo se convierte con RVC a `salida`.
El conversor RVC se importa una vez para todo el lote.
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from core import import_voice_converter  # noqa: E402

job = json.load(open(sys.argv[1], encoding="utf-8"))
vc = import_voice_converter()
for n, t in enumerate(job["trabajos"], 1):
    os.makedirs(os.path.dirname(t["salida"]), exist_ok=True)
    vc.convert_audio(
        pitch=job["pitch"], index_rate=job["index_rate"], volume_envelope=1, protect=job["protect"], f0_method="rmvpe",
        audio_input_path=t["crudo"], audio_output_path=t["salida"], model_path=job["pth"], index_path="",
        split_audio=False, f0_autotune=False, f0_autotune_strength=1.0, proposed_pitch=False,
        proposed_pitch_threshold=155.0, clean_audio=False, clean_strength=0.5, export_format="WAV",
        embedder_model="contentvec", embedder_model_custom=None, sid=0, formant_shifting=None, formant_qfrency=None,
        formant_timbre=None, post_process=None, reverb=None, pitch_shift=None, limiter=None, gain=None,
        distortion=None, chorus=None, bitcrush=None, clipping=None, compressor=None, delay=None, sliders=None)
    print(f"[{n}/{len(job['trabajos'])}] {t['salida']}", flush=True)
