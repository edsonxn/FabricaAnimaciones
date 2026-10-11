# -*- coding: utf-8 -*-
"""Genera una frase de prueba con una voz (clonada o de la biblioteca) para escucharla en el Estudio.
Uso: python probar_voz.py <referencia.wav|mp3> <salida.wav> <expresividad> <texto...>"""
import sys

import torch
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

ref, salida, expr, texto = sys.argv[1], sys.argv[2], float(sys.argv[3]), " ".join(sys.argv[4:])
modelo = ChatterboxMultilingualTTS.from_pretrained(device="cuda" if torch.cuda.is_available() else "cpu", t3_model="v3")
modelo.prepare_conditionals(ref, exaggeration=expr)
torch.manual_seed(1)
wav = modelo.generate(texto, language_id="es", exaggeration=expr, cfg_weight=0.3, temperature=0.8)
ta.save(salida, wav, modelo.sr)
print("ok", salida)
