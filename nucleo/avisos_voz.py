# -*- coding: utf-8 -*-
"""Proceso auxiliar del panel: sintetiza avisos con Chatterbox y los guarda como WAV de 16 bits.

Lo lanza nucleo/avisos.py (no se usa a mano). Protocolo por líneas (solo las que empiezan con '@@' son mensajes):
  entrada (stdin):  {"id": 3, "texto": "...", "salida": "ruta.wav", "seed": 7}
  salida (stdout):  @@LISTO                       (modelo cargado)
                    @@{"id": 3, "ok": true, "dur": 2.4}   |   @@{"id": 3, "ok": false, "error": "..."}
Al cerrarse stdin (EOF) el proceso termina y libera la GPU.
"""
import json
import sys

import torch
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


def main():
    cfg = json.loads(sys.argv[1])
    model = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
    model.prepare_conditionals(cfg["voz"], exaggeration=cfg["exaggeration"])
    print("@@LISTO", flush=True)
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        pet = json.loads(linea)
        try:
            torch.manual_seed(int(pet.get("seed", 7)))
            wav = model.generate(pet["texto"], language_id="es", exaggeration=cfg["exaggeration"],
                                 cfg_weight=cfg["cfg_weight"], temperature=cfg["temperature"])
            wav = wav.detach().cpu()
            pico = float(wav.abs().max()) or 1.0
            wav = wav / pico * 0.9                     # volumen parejo entre avisos
            ta.save(pet["salida"], wav, model.sr, encoding="PCM_S", bits_per_sample=16)
            print("@@" + json.dumps({"id": pet["id"], "ok": True, "dur": round(wav.shape[-1] / model.sr, 2)}), flush=True)
        except Exception as e:                        # un aviso fallido no debe matar al proceso
            print("@@" + json.dumps({"id": pet["id"], "ok": False, "error": str(e)[:200]}), flush=True)


if __name__ == "__main__":
    main()
